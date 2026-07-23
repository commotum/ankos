from __future__ import annotations

import importlib.util
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
