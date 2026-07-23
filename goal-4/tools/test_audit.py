from __future__ import annotations

import copy
import importlib.util
import csv
import json
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
    review_history = MODULE.load_jsonl(goal / "review-history.jsonl")
    return (
        manifest,
        units,
        reading,
        candidates,
        routes,
        assets,
        search,
        review_history,
    )


def append_history_event(
    history,
    manifest,
    units,
    reading,
    assets,
    source_path,
    epoch,
    mode,
    reviewer,
    prior_rounds,
):
    document = next(
        item for item in manifest["documents"] if item["path"] == source_path
    )
    prior_path_event = next(
        (
            item
            for item in reversed(history)
            if item.get("source_paths") == [source_path]
        ),
        None,
    )
    event = MODULE.close_review_event(
        {
            "review_id": f"V{len(history) + 1:06d}",
            "epoch": epoch,
            "stage": MODULE.stage_for_document(document),
            "mode": mode,
            "reviewer": reviewer,
            "source_paths": [source_path],
            "source_unit_ids": [
                item["id"] for item in units if item["path"] == source_path
            ],
            "asset_ids": [
                item["asset_id"]
                for item in assets
                if item["assignment_path"] == source_path
            ],
            "previous_path_result_sha256": (
                prior_path_event["result_projection_sha256"]
                if prior_path_event is not None
                else None
            ),
            "trigger_search_kind": None,
            "trigger_hit_ids": [],
        },
        {item["id"]: item for item in units},
        {item["source_unit_id"]: item for item in reading},
        {item["asset_id"]: item for item in assets},
        history[-1]["event_sha256"] if history else None,
        prior_rounds,
    )
    return [*history, event]


def test_initial_harness_is_valid() -> None:
    values = load()
    assert MODULE.validate_objects(*values) == []


def test_required_harness_mutations_fail() -> None:
    values = load()
    assert MODULE.mutation_checks(*values) == []


def test_schema_files_are_frozen() -> None:
    assert MODULE.validate_schema_files(MODULE.GOAL_DIR) == []


def test_search_query_ids_follow_global_encounter_order() -> None:
    def query(query_id: str):
        return {
            "query_id": query_id,
            "family": "query-order fixture",
            "pattern": "__QUERY_ORDER_FIXTURE__",
            "mode": "LITERAL",
            "case_sensitive": True,
            "whole_word": False,
            "scope_paths": ["fixture.md"],
        }

    positive_multi_round = [
        {"queries": [query("Q0001"), query("Q0002")]},
        {"queries": [query("Q0003")]},
    ]
    assert MODULE.search_query_id_sequence_errors(positive_multi_round) == []

    invalid = {
        "reversed": [{"queries": [query("Q0002"), query("Q0001")]}],
        "duplicate": [{"queries": [query("Q0001"), query("Q0001")]}],
        "skipped": [{"queries": [query("Q0001"), query("Q0003")]}],
        "cross-round": [
            {"queries": [query("Q0001"), query("Q0003")]},
            {"queries": [query("Q0002")]},
        ],
    }
    for label, rounds in invalid.items():
        assert MODULE.search_query_id_sequence_errors(rounds) == [
            "search query IDs are not a complete append-only Q sequence"
        ], label


def test_stage18_requires_every_local_stage_before_saturation() -> None:
    manifest, units, reading, candidates, routes, assets, _, _ = load()
    assert candidates == []
    assert routes == []
    document_by_path = {
        document["path"]: document for document in manifest["documents"]
    }
    for row in reading:
        row.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": "1",
                "review_disposition": "NO_CONSTRUCTION",
                "source_status": "CLEAR",
                "uncertainty": "",
                "secondary_roles": "[]",
                "candidate_ids": "[]",
                "route_ids": "[]",
                "evidence_statement": "No qualifying construction in this fixture unit.",
                "review_stage": str(
                    MODULE.stage_for_document(document_by_path[row["path"]])
                ),
                "reviewer": "closure-fixture",
            }
        )
    for row in assets:
        row.update(
            {
                "inspection_status": "SCREENED",
                "review_epoch": "1",
                "visual_role": "DECORATIVE",
                "source_status": "CLEAR",
                "risk_flags": "[]",
                "original_resolution_status": "NOT_REQUIRED",
                "transcription_status": "NOT_REQUIRED",
                "candidate_ids": "[]",
                "route_ids": "[]",
                "evidence_statement": "No construction-bearing visual content.",
                "review_stage": row["assignment_stage"],
                "reviewer": "closure-fixture",
                "uncertainty": "",
            }
        )
    history = []
    for document in sorted(
        manifest["documents"],
        key=lambda item: (
            MODULE.stage_for_document(item),
            int(item["order"]),
        ),
    ):
        history = append_history_event(
            history,
            manifest,
            units,
            reading,
            assets,
            document["path"],
            1,
            "INITIAL",
            "closure-fixture",
            [],
        )

    rounds = []
    query_number = 1
    for stage in range(4, 18):
        scope_paths = [
            document["path"]
            for document in manifest["documents"]
            if MODULE.stage_for_document(document) == stage
        ]
        round_record = {
            "round_id": f"S{len(rounds) + 1:03d}",
            "epoch": 1,
            "kind": "LOCAL",
            "owning_stage": stage,
            "queries": [
                {
                    "query_id": f"Q{query_number:04d}",
                    "family": "zero-result closure fixture",
                    "pattern": "__AUDIT_HARNESS_IMPOSSIBLE_MATCH_71A9C2__",
                    "mode": "LITERAL",
                    "case_sensitive": True,
                    "whole_word": False,
                    "scope_paths": scope_paths,
                }
            ],
            "tool_assumptions": ["Deterministic zero-result fixture."],
            "result_ids": [],
            "result_digest": "",
            "hits": [],
            "new_vocabulary": [],
            "new_candidates": [],
            "new_evidence_groups": [],
            "new_routes": [],
            "rerun_digest": "",
        }
        digest = MODULE.search_result_digest(round_record)
        round_record["result_digest"] = digest
        round_record["rerun_digest"] = digest
        rounds.append(round_record)
        query_number += 1

    saturation = {
        "round_id": f"S{len(rounds) + 1:03d}",
        "epoch": 1,
        "kind": "SATURATION",
        "owning_stage": 18,
        "queries": [
            {
                "query_id": f"Q{query_number:04d}",
                "family": "zero-result saturation fixture",
                "pattern": "__AUDIT_HARNESS_IMPOSSIBLE_MATCH_71A9C2__",
                "mode": "LITERAL",
                "case_sensitive": True,
                "whole_word": False,
                "scope_paths": [
                    document["path"] for document in manifest["documents"]
                ],
            }
        ],
        "tool_assumptions": ["Deterministic zero-result fixture."],
        "result_ids": [],
        "result_digest": "",
        "hits": [],
        "new_vocabulary": [],
        "new_candidates": [],
        "new_evidence_groups": [],
        "new_routes": [],
        "rerun_digest": "",
    }
    saturation_digest = MODULE.search_result_digest(saturation)
    saturation["result_digest"] = saturation_digest
    saturation["rerun_digest"] = saturation_digest
    rounds.append(saturation)
    search = {
        "schema_version": 1,
        "phase": "blind_discovery",
        "tool_assumptions": ["Deterministic zero-result fixture."],
        "vocabulary": [],
        "rounds": rounds,
        "fixed_point": {
            "round_id": saturation["round_id"],
            "zero_delta": True,
            "rerun_reproduced": True,
            "result_digest": saturation_digest,
        },
    }
    assert MODULE.validate_objects(
        manifest,
        units,
        reading,
        candidates,
        routes,
        assets,
        search,
        history,
        {18},
        True,
    ) == []

    reopened_reading = copy.deepcopy(reading)
    reopened_assets = copy.deepcopy(assets)
    reopened_path = next(
        document["path"]
        for document in manifest["documents"]
        if MODULE.stage_for_document(document) == 4
    )
    for row in reopened_reading:
        if row["path"] == reopened_path:
            row["review_epoch"] = "2"
    for row in reopened_assets:
        if row["assignment_path"] == reopened_path:
            row["review_epoch"] = "2"
    reopened_search = copy.deepcopy(search)
    reopened_local = {
        "round_id": "S016",
        "epoch": 2,
        "kind": "LOCAL",
        "owning_stage": 4,
        "queries": [
            {
                "query_id": "Q0016",
                "family": "zero-result reopened fixture",
                "pattern": "__AUDIT_HARNESS_IMPOSSIBLE_MATCH_71A9C2__",
                "mode": "LITERAL",
                "case_sensitive": True,
                "whole_word": False,
                "scope_paths": [reopened_path],
            }
        ],
        "tool_assumptions": ["Deterministic zero-result fixture."],
        "result_ids": [],
        "result_digest": "",
        "hits": [],
        "new_vocabulary": [],
        "new_candidates": [],
        "new_evidence_groups": [],
        "new_routes": [],
        "rerun_digest": "",
    }
    reopened_local_digest = MODULE.search_result_digest(reopened_local)
    reopened_local["result_digest"] = reopened_local_digest
    reopened_local["rerun_digest"] = reopened_local_digest
    reopened_saturation = copy.deepcopy(saturation)
    reopened_saturation["round_id"] = "S017"
    reopened_saturation["epoch"] = 2
    reopened_saturation["queries"][0]["query_id"] = "Q0017"
    reopened_saturation_digest = MODULE.search_result_digest(
        reopened_saturation
    )
    reopened_saturation["result_digest"] = reopened_saturation_digest
    reopened_saturation["rerun_digest"] = reopened_saturation_digest
    reopened_search["rounds"].extend(
        [reopened_local, reopened_saturation]
    )
    reopened_search["fixed_point"] = {
        "round_id": "S017",
        "zero_delta": True,
        "rerun_reproduced": True,
        "result_digest": reopened_saturation_digest,
    }
    reopened_history = append_history_event(
        history,
        manifest,
        units,
        reopened_reading,
        reopened_assets,
        reopened_path,
        2,
        "REOPEN",
        "closure-fixture",
        search["rounds"],
    )
    assert MODULE.validate_objects(
        manifest,
        units,
        reopened_reading,
        candidates,
        routes,
        reopened_assets,
        reopened_search,
        reopened_history,
        {18},
        True,
    ) == []

    missing_reopen_local = copy.deepcopy(reopened_search)
    missing_reopen_local["rounds"].pop(-2)
    missing_reopen_local["rounds"][-1]["round_id"] = "S016"
    missing_reopen_local["rounds"][-1]["queries"][0]["query_id"] = "Q0016"
    missing_reopen_digest = MODULE.search_result_digest(
        missing_reopen_local["rounds"][-1]
    )
    missing_reopen_local["rounds"][-1][
        "result_digest"
    ] = missing_reopen_digest
    missing_reopen_local["rounds"][-1][
        "rerun_digest"
    ] = missing_reopen_digest
    missing_reopen_local["fixed_point"] = {
        "round_id": "S016",
        "zero_delta": True,
        "rerun_reproduced": True,
        "result_digest": missing_reopen_digest,
    }
    missing_reopen_errors = MODULE.validate_objects(
        manifest,
        units,
        reopened_reading,
        candidates,
        routes,
        reopened_assets,
        missing_reopen_local,
        reopened_history,
        {18},
        True,
    )
    assert any(
        "review-epoch 2 LOCAL-round coverage" in error
        for error in missing_reopen_errors
    )

    saturation_only = copy.deepcopy(search)
    saturation_only["rounds"] = [saturation_only["rounds"][-1]]
    saturation_only["rounds"][0]["round_id"] = "S001"
    saturation_only["rounds"][0]["queries"][0]["query_id"] = "Q0001"
    saturation_only_digest = MODULE.search_result_digest(
        saturation_only["rounds"][0]
    )
    saturation_only["rounds"][0]["result_digest"] = saturation_only_digest
    saturation_only["rounds"][0]["rerun_digest"] = saturation_only_digest
    saturation_only["fixed_point"] = {
        "round_id": "S001",
        "zero_delta": True,
        "rerun_reproduced": True,
        "result_digest": saturation_only_digest,
    }
    saturation_only_errors = MODULE.validate_objects(
        manifest,
        units,
        reading,
        candidates,
        routes,
        assets,
        saturation_only,
        history,
        {18},
        True,
    )
    assert any(
        "review-epoch 1 LOCAL-round coverage" in error
        for error in saturation_only_errors
    )


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


def test_worker_bundle_rejects_forbidden_free_text_worker_ids(
    tmp_path: Path,
) -> None:
    build = MODULE_PATH.with_name("build_worker_bundle.py")
    forbidden_ids = (
        "T02",
        "worker-t02-alpha",
        "reviewer-[t17]",
        "qa-ADD_CATALOG_ENTRY",
        "Api Fit Reviewer",
    )
    for index, worker_id in enumerate(forbidden_ids):
        bundle = tmp_path / f"forbidden-{index}"
        created = subprocess.run(
            [
                sys.executable,
                str(build),
                "--output",
                str(bundle),
                "--worker-id",
                worker_id,
                "--stage",
                "5",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        assert created.returncode != 0
        assert "forbidden blind priming" in created.stderr
        assert not bundle.exists()


def test_worker_bundle_verifier_rejects_tampered_priming_metadata(
    tmp_path: Path,
) -> None:
    bundle = tmp_path / "bundle"
    build = MODULE_PATH.with_name("build_worker_bundle.py")
    subprocess.run(
        [
            sys.executable,
            str(build),
            "--output",
            str(bundle),
            "--worker-id",
            "benign-worker",
            "--stage",
            "5",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    manifest_path = bundle / "allowed-manifest.json"
    original_manifest = manifest_path.read_bytes()
    manifest = json.loads(original_manifest)
    manifest["worker_id"] = "tampered-[t02]-worker"
    manifest_path.chmod(0o644)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    manifest_path.chmod(0o444)
    verified = subprocess.run(
        [sys.executable, str(build), "--verify", str(bundle)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert verified.returncode != 0
    assert "bundle manifest contains forbidden blind priming" in verified.stderr

    manifest_path.chmod(0o644)
    manifest_path.write_bytes(original_manifest)
    manifest_path.chmod(0o444)
    brief_path = bundle / "input" / "brief.md"
    brief_path.chmod(0o644)
    brief_path.write_text(
        brief_path.read_text(encoding="utf-8") + "\nReviewer T03 metadata.\n",
        encoding="utf-8",
    )
    brief_path.chmod(0o444)
    verified = subprocess.run(
        [sys.executable, str(build), "--verify", str(bundle)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert verified.returncode != 0
    assert "bundle brief contains forbidden blind priming" in verified.stderr


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
                "review_epoch": "1",
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
                "review_epoch": "1",
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
        copy_function=shutil.copy2,
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
