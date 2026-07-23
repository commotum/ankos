from __future__ import annotations

import importlib.util
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
