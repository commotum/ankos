from __future__ import annotations

import importlib.util
import csv
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate_audit.py")
sys.path.insert(0, str(MODULE_PATH.parent))
SPEC = importlib.util.spec_from_file_location("validate_audit", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def load():
    goal = MODULE.GOAL_DIR
    manifest = MODULE.json.loads(
        (goal / "corpus-manifest.json").read_text(encoding="utf-8")
    )
    units = MODULE.verify_corpus.load_units(goal / "source-units.jsonl")
    reading = MODULE.load_csv(goal / "reading-ledger.csv", MODULE.READING_HEADER)
    candidates = MODULE.load_jsonl(goal / "candidate-ledger.jsonl")
    routes = MODULE.load_csv(
        goal / "cross-reference-ledger.csv",
        MODULE.CROSS_REFERENCE_HEADER,
    )
    assets = MODULE.load_csv(goal / "asset-ledger.csv", MODULE.ASSET_HEADER)
    search = MODULE.json.loads(
        (goal / "search-rounds.json").read_text(encoding="utf-8")
    )
    return manifest, units, reading, candidates, routes, assets, search


def test_initial_harness_is_valid() -> None:
    values = load()
    assert MODULE.validate_objects(*values) == []


def test_required_harness_mutations_fail() -> None:
    values = load()
    assert MODULE.mutation_checks(*values) == []


def test_schema_files_are_frozen() -> None:
    assert MODULE.validate_schema_files(MODULE.GOAL_DIR) == []


def test_sealed_worker_bundle_is_sanitized_and_hash_bound(tmp_path: Path) -> None:
    bundle = tmp_path / "bundle"
    build = MODULE_PATH.with_name("build_worker_bundle.py")
    created = subprocess.run(
        [
            sys.executable,
            str(build),
            "--output",
            str(bundle),
            "--worker-id",
            "test-worker",
            "--stage",
            "5",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert created.returncode == 0, created.stderr
    verified = subprocess.run(
        [sys.executable, str(build), "--verify", str(bundle)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert verified.returncode == 0, verified.stderr

    manifest = json.loads((bundle / "allowed-manifest.json").read_text())
    assert manifest["execution_requirements"]["network_allowed"] is False
    assert manifest["source_unit_count"] > 0
    assert manifest["asset_count"] > 0
    all_paths = [row["path"] for row in manifest["allowed_inputs"]]
    assert not any(".git" in path or "goal-1" in path for path in all_paths)
    for path in (bundle / "input").rglob("*"):
        assert path.stat().st_mode & 0o222 == 0
        if path.is_file():
            assert path.stat().st_nlink == 1


def test_completed_empty_worker_output_is_exact_and_accepted(
    tmp_path: Path,
) -> None:
    bundle = tmp_path / "bundle"
    build_path = MODULE_PATH.with_name("build_worker_bundle.py")
    subprocess.run(
        [
            sys.executable,
            str(build_path),
            "--output",
            str(bundle),
            "--worker-id",
            "complete-worker",
            "--stage",
            "4",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    output_path = bundle / "output" / "output.json"
    output = json.loads(output_path.read_text())
    output["prohibited_input_nonuse"] = True
    with (bundle / "input" / "reading-input.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        readings = list(csv.DictReader(handle))
    for row in readings:
        row.update(
            {
                "review_status": "REVIEWED",
                "review_disposition": "NO_CONSTRUCTION",
                "source_status": "CLEAR",
                "secondary_roles": "[]",
                "candidate_ids": "[]",
                "route_ids": "[]",
                "evidence_statement": "No qualifying construction in this unit.",
                "review_stage": "4",
                "reviewer": "complete-worker",
            }
        )
    with (bundle / "input" / "asset-input.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        assets = list(csv.DictReader(handle))
    for row in assets:
        row.update(
            {
                "inspection_status": "SCREENED",
                "visual_role": "DECORATIVE",
                "source_status": "CLEAR",
                "risk_flags": "[]",
                "original_resolution_status": "NOT_REQUIRED",
                "transcription_status": "NOT_REQUIRED",
                "candidate_ids": "[]",
                "route_ids": "[]",
                "evidence_statement": "No construction-bearing visual content.",
                "review_stage": "4",
                "reviewer": "complete-worker",
            }
        )
    output["reading_updates"] = readings
    output["asset_updates"] = assets
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    completed = subprocess.run(
        [
            sys.executable,
            str(build_path),
            "--verify",
            str(bundle),
            "--verify-output",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr


def test_worker_bundle_detects_input_mutation(tmp_path: Path) -> None:
    bundle = tmp_path / "bundle"
    build = MODULE_PATH.with_name("build_worker_bundle.py")
    subprocess.run(
        [
            sys.executable,
            str(build),
            "--output",
            str(bundle),
            "--worker-id",
            "mutation-worker",
            "--stage",
            "4",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    brief = bundle / "input" / "brief.md"
    brief.chmod(0o644)
    brief.write_text(brief.read_text() + "\nmutation\n")
    verified = subprocess.run(
        [sys.executable, str(build), "--verify", str(bundle)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert verified.returncode != 0
    assert "hash/size mismatch" in verified.stderr


def test_full_harness_runs_from_relocated_copy(tmp_path: Path) -> None:
    relocated = tmp_path / "ankos"
    source_target = relocated / "ref" / "A-New-Kind-of-Science"
    source_target.parent.mkdir(parents=True)
    shutil.copytree(
        MODULE.REPO_ROOT / "ref" / "A-New-Kind-of-Science",
        source_target,
        copy_function=os.link,
    )
    shutil.copytree(
        MODULE.GOAL_DIR,
        relocated / "goal-4",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    validator = relocated / "goal-4" / "tools" / "validate_audit.py"
    completed = subprocess.run(
        [sys.executable, str(validator), "--self-test"],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    assert "validated blind audit harness and mutation checks" in completed.stdout


def test_reconciliation_schemas_are_typed_and_closed() -> None:
    import audit_contract
    import build_worker_bundle

    schemas = audit_contract.schema_documents()
    classification = {
        "candidate_id": "B0001",
        "catalog_action": "ADD_CATALOG_ENTRY",
        "semantic_role": "NATIVE_TRANSITION_OR_GENERATOR",
        "semantic_subtype": None,
        "family_action": "NEW_SEMANTIC_FAMILY",
        "family_relations": [
            {
                "relation": "MEMBER_OF",
                "target_kind": "SEMANTIC_FAMILY",
                "target_id": "F0001",
                "evidence_ids": ["E000001"],
                "rationale": "Direct family relation.",
            }
        ],
        "rationale": "Fixture classification.",
        "evidence_ids": ["E000001"],
        "proof_packets": [
            {
                "proof_case": "new_semantic_family",
                "obligations": [
                    {
                        "obligation_id": "new_family_01",
                        "status": "PROVED",
                        "evidence_ids": ["E000001"],
                        "argument": "Fixture proof.",
                    }
                ],
                "nearest_candidate_ids": [],
                "non_preservation_witness": "Fixture witness.",
                "reopen_trigger": None,
            }
        ],
        "hostile_review_required": True,
    }
    classification_schema = schemas[
        "reconciliation/classification-row.schema.json"
    ]
    assert build_worker_bundle.json_schema_errors(
        classification, classification_schema
    ) == []
    classification["catalog_action"] = "ARBITRARY"
    assert build_worker_bundle.json_schema_errors(
        classification, classification_schema
    )

    coverage = {
        "coverage_id": "C0001",
        "candidate_ids": ["B0001"],
        "existing_t_ids": ["T01"],
        "proposed_t_ids": [],
        "source_unit_ids": ["U000001"],
        "image_paths": [],
        "evidence_ids": ["E000001"],
        "reconciliation_result": "REDISCOVERED",
        "rationale": "Fixture coverage.",
    }
    coverage_schema = schemas["reconciliation/coverage-row.schema.json"]
    assert build_worker_bundle.json_schema_errors(coverage, coverage_schema) == []
    coverage["existing_t_ids"] = ["T99"]
    assert build_worker_bundle.json_schema_errors(coverage, coverage_schema)
