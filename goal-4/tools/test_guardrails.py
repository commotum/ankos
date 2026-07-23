from __future__ import annotations

import copy
import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate_guardrails.py")
SPEC = importlib.util.spec_from_file_location("validate_guardrails", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_frozen_guardrails_validate() -> None:
    data = MODULE.load_guardrails()
    assert MODULE.validate(data) == []


def test_required_mutations_fail() -> None:
    data = MODULE.load_guardrails()
    assert MODULE.run_mutation_checks(data) == []


def test_forbidden_blind_field_is_rejected() -> None:
    data = copy.deepcopy(MODULE.load_guardrails())
    data["blind_candidate_fields"].append("api_fit")
    errors = MODULE.validate(data)
    assert any("overlap forbidden fields" in error for error in errors)


def test_missing_fingerprint_field_is_rejected() -> None:
    data = copy.deepcopy(MODULE.load_guardrails())
    data["fingerprint_fields"].remove("witness_semantics")
    errors = MODULE.validate(data)
    assert "fingerprint_fields do not match the frozen contract" in errors
