from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("verify_corpus.py")
SPEC = importlib.util.spec_from_file_location("verify_corpus", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def load() -> tuple[dict, list[dict], bytes]:
    manifest = MODULE.json.loads(MODULE.MANIFEST_PATH.read_text(encoding="utf-8"))
    units_bytes = MODULE.UNITS_PATH.read_bytes()
    units = MODULE.load_units(MODULE.UNITS_PATH)
    return manifest, units, units_bytes


def test_corpus_artifacts_verify_independently() -> None:
    manifest, units, units_bytes = load()
    assert MODULE.verify_loaded(manifest, units, MODULE.REPO_ROOT, units_bytes) == []


def test_required_corpus_mutations_fail() -> None:
    manifest, units, units_bytes = load()
    assert MODULE.mutation_checks(
        manifest, units, MODULE.REPO_ROOT, units_bytes
    ) == []


def test_verifier_runs_from_relocated_copy(tmp_path: Path) -> None:
    relocated = tmp_path / "ankos"
    source_target = relocated / "ref" / "A-New-Kind-of-Science"
    source_target.parent.mkdir(parents=True)
    shutil.copytree(
        MODULE.REPO_ROOT / "ref" / "A-New-Kind-of-Science",
        source_target,
        copy_function=os.link,
    )
    goal_target = relocated / "goal-4"
    tools_target = goal_target / "tools"
    tools_target.mkdir(parents=True)
    for path in (
        MODULE_PATH,
        MODULE.MANIFEST_PATH,
        MODULE.UNITS_PATH,
    ):
        target = (
            tools_target / path.name
            if path.parent.name == "tools"
            else goal_target / path.name
        )
        shutil.copy2(path, target)

    completed = subprocess.run(
        [sys.executable, str(tools_target / "verify_corpus.py"), "--self-test"],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    assert "verified corpus map and mutation checks" in completed.stdout
