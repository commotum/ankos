#!/usr/bin/env python3
"""Validate the frozen Goal 4 blind-discovery guardrails."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any


GOAL_DIR = Path(__file__).resolve().parents[1]
GUARDRAILS_PATH = GOAL_DIR / "guardrails.json"

EXPECTED_DISPOSITIONS = {
    "CANDIDATE",
    "SUPPORTS_CANDIDATE",
    "CROSS_REFERENCE",
    "REPRESENTATION_OR_OBSERVER",
    "APPLICATION_OR_EMULATION",
    "HISTORICAL_ONLY",
    "NO_CONSTRUCTION",
    "SOURCE_DEFECT_OR_AMBIGUITY",
}
EXPECTED_EVIDENCE = {
    "DIRECT_COMPLETE",
    "DIRECT_PARTIAL",
    "DIRECT_IDENTITY_ONLY",
    "CORROBORATING",
    "VISUAL_EXPLICIT",
    "VISUAL_CONTEXT_ONLY",
    "DEFECT_LIMITED",
}
EXPECTED_FINGERPRINT_FIELDS = {
    "object_kind",
    "native_time",
    "carrier",
    "support",
    "topology",
    "structural_invariants",
    "alphabet_or_value_schema",
    "complete_state",
    "visible_history",
    "control_state",
    "seed",
    "input",
    "boundary",
    "external_data",
    "frontier_or_activation",
    "schedule",
    "read_dependencies_or_neighborhood",
    "law_kind",
    "rule_relation_constraint_function_or_probability_law",
    "write_replacement_assembly_or_commit",
    "result_kind",
    "successor_cardinality",
    "determinism_branching_or_measure",
    "termination_completion_failure",
    "witness_semantics",
    "parameters_and_variants",
    "excluded_observers_and_representations",
    "evidence_limit",
}
EXPECTED_CLASSIFICATIONS = {
    "catalog_action": {
        "EXISTING_ENTRY_SUFFICIENT",
        "EXISTING_ENTRY_NEEDS_CORRECTION",
        "ADD_CATALOG_ENTRY",
        "NO_SEPARATE_CATALOG_ENTRY",
        "INSUFFICIENT_BOOK_EVIDENCE",
    },
    "semantic_role": {
        "NATIVE_TRANSITION_OR_GENERATOR",
        "STOCHASTIC_OR_BRANCHING_PROCESS",
        "INPUT_PROCESSOR_OR_TRANSDUCER",
        "RELATION_CONSTRAINT_OR_MODEL_SET",
        "IMMUTABLE_DEFINITION_OR_QUERY",
        "SPECIALIZATION_OR_PRESET",
        "PROPERTY_OR_RESTRICTION",
        "SEED_INPUT_OR_BOUNDARY_CLASS",
        "COMPOSITION_OR_HYBRID",
        "REPRESENTATION_CODEC_OR_OBSERVER",
        "APPLICATION_OR_EMULATION",
        "DUPLICATE_OR_ALIAS",
        "SOURCE_INSUFFICIENT_ROLE",
    },
    "family_action": {
        "EXISTING_SEMANTIC_FAMILY",
        "NEW_SEMANTIC_FAMILY",
        "SOURCE_INSUFFICIENT_FOR_FAMILY",
    },
}
EXPECTED_PROOFS = {
    "same_family",
    "specialization_preset_property_seed",
    "composition_hybrid",
    "representation_observer_application_emulation",
    "new_catalog_entry",
    "new_semantic_family",
    "source_insufficient",
}
REQUIRED_FORBIDDEN_FIELDS = {
    "t_ids",
    "catalog_mapping",
    "catalog_action",
    "semantic_role",
    "family_action",
    "existing_family",
    "api_fit",
    "api_mapping",
    "implementation_target",
    "runtime_support",
}


def _duplicates(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for value in values:
        if value in seen and value not in duplicates:
            duplicates.append(value)
        seen.add(value)
    return duplicates


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if data.get("schema_version") != 1:
        errors.append("schema_version must equal 1")
    if data.get("phase") != "blind_discovery":
        errors.append("phase must equal blind_discovery")

    policy = data.get("candidate_id_policy")
    if not isinstance(policy, dict):
        errors.append("candidate_id_policy must be an object")
    else:
        pattern = policy.get("pattern")
        try:
            compiled = re.compile(pattern) if isinstance(pattern, str) else None
        except re.error:
            compiled = None
        if compiled is None or compiled.fullmatch("B0001") is None:
            errors.append("candidate ID pattern must accept B0001")
        if compiled is not None and compiled.fullmatch("T0001") is not None:
            errors.append("candidate ID pattern must reject T0001")
        for key in (
            "allocation_order",
            "worker_policy",
            "reuse_policy",
            "split_policy",
            "merge_policy",
        ):
            if not isinstance(policy.get(key), str) or not policy[key].strip():
                errors.append(f"candidate_id_policy.{key} must be non-empty")

    eligibility = data.get("eligibility_criteria")
    if not isinstance(eligibility, list) or len(eligibility) < 5:
        errors.append("at least five eligibility criteria are required")
    else:
        ids: list[str] = []
        for index, criterion in enumerate(eligibility):
            if not isinstance(criterion, dict):
                errors.append(f"eligibility criterion {index} must be an object")
                continue
            ids.append(str(criterion.get("id", "")))
            for key in ("id", "capture_when", "do_not_capture_when"):
                if not isinstance(criterion.get(key), str) or not criterion[key].strip():
                    errors.append(f"eligibility criterion {index}.{key} must be non-empty")
        if _duplicates(ids):
            errors.append("eligibility criterion IDs must be unique")

    dispositions = data.get("reading_dispositions")
    if not isinstance(dispositions, list):
        errors.append("reading_dispositions must be a list")
    else:
        if set(dispositions) != EXPECTED_DISPOSITIONS:
            errors.append("reading_dispositions do not match the frozen vocabulary")
        if _duplicates(dispositions):
            errors.append("reading_dispositions contain duplicates")
    rules = data.get("reading_disposition_rules")
    if not isinstance(rules, dict) or set(rules) != EXPECTED_DISPOSITIONS:
        errors.append("every reading disposition must have exactly one rule")
    elif any(not isinstance(value, str) or not value.strip() for value in rules.values()):
        errors.append("reading disposition rules must be non-empty")

    strengths = data.get("evidence_strengths")
    if not isinstance(strengths, dict) or set(strengths) != EXPECTED_EVIDENCE:
        errors.append("evidence_strengths do not match the frozen vocabulary")
    elif any(not isinstance(value, str) or not value.strip() for value in strengths.values()):
        errors.append("evidence strength definitions must be non-empty")

    blind_fields = data.get("blind_candidate_fields")
    if not isinstance(blind_fields, list) or not blind_fields:
        errors.append("blind_candidate_fields must be a non-empty list")
        blind_field_set: set[str] = set()
    else:
        blind_field_set = set(blind_fields)
        if _duplicates(blind_fields):
            errors.append("blind_candidate_fields contain duplicates")

    forbidden = data.get("forbidden_blind_fields")
    if not isinstance(forbidden, list):
        errors.append("forbidden_blind_fields must be a list")
        forbidden_set: set[str] = set()
    else:
        forbidden_set = set(forbidden)
        if not REQUIRED_FORBIDDEN_FIELDS.issubset(forbidden_set):
            errors.append("forbidden_blind_fields is missing required phase barriers")
        if _duplicates(forbidden):
            errors.append("forbidden_blind_fields contain duplicates")
    overlap = blind_field_set & forbidden_set
    if overlap:
        errors.append(f"blind fields overlap forbidden fields: {sorted(overlap)}")

    fingerprint = data.get("fingerprint_fields")
    if not isinstance(fingerprint, list):
        errors.append("fingerprint_fields must be a list")
    else:
        if set(fingerprint) != EXPECTED_FINGERPRINT_FIELDS:
            errors.append("fingerprint_fields do not match the frozen contract")
        if _duplicates(fingerprint):
            errors.append("fingerprint_fields contain duplicates")

    vocabularies = data.get("final_classification_vocabularies")
    if not isinstance(vocabularies, dict) or set(vocabularies) != set(
        EXPECTED_CLASSIFICATIONS
    ):
        errors.append("final classification axes do not match the frozen contract")
    else:
        for axis, expected in EXPECTED_CLASSIFICATIONS.items():
            values = vocabularies.get(axis)
            if not isinstance(values, list) or set(values) != expected:
                errors.append(f"{axis} values do not match the frozen vocabulary")
            elif _duplicates(values):
                errors.append(f"{axis} contains duplicates")

    proofs = data.get("proof_obligations")
    if not isinstance(proofs, dict) or set(proofs) != EXPECTED_PROOFS:
        errors.append("proof_obligations do not match the required cases")
    else:
        for key, obligations in proofs.items():
            if not isinstance(obligations, list) or not obligations:
                errors.append(f"proof_obligations.{key} must be non-empty")
            elif any(not isinstance(item, str) or not item.strip() for item in obligations):
                errors.append(f"proof_obligations.{key} contains an empty obligation")

    isolation = data.get("worker_isolation")
    if not isinstance(isolation, dict):
        errors.append("worker_isolation must be an object")
    else:
        for key in ("allowed_inputs", "forbidden_inputs", "output_contract"):
            value = isolation.get(key)
            if not isinstance(value, list) or not value:
                errors.append(f"worker_isolation.{key} must be a non-empty list")
        forbidden_text = "\n".join(isolation.get("forbidden_inputs", []))
        for required in (
            "CA-Types.csv",
            "goal-1/",
            "goal-2/",
            "api.md",
            "simple_programs.md",
            "src/ca/",
        ):
            if required not in forbidden_text:
                errors.append(f"worker isolation does not forbid {required}")

    freeze = data.get("blind_freeze_requirements")
    if not isinstance(freeze, list) or len(freeze) < 6:
        errors.append("blind_freeze_requirements must contain the full closure contract")

    return errors


def run_mutation_checks(data: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    mutations: list[tuple[str, dict[str, Any]]] = []

    missing_eligibility = copy.deepcopy(data)
    missing_eligibility["eligibility_criteria"] = []
    mutations.append(("missing eligibility criteria", missing_eligibility))

    leaked_field = copy.deepcopy(data)
    leaked_field["blind_candidate_fields"].append("catalog_action")
    mutations.append(("classification leakage into blind fields", leaked_field))

    bad_id_pattern = copy.deepcopy(data)
    bad_id_pattern["candidate_id_policy"]["pattern"] = "^T[0-9]{4}$"
    mutations.append(("T-style candidate IDs", bad_id_pattern))

    missing_proof = copy.deepcopy(data)
    del missing_proof["proof_obligations"]["new_semantic_family"]
    mutations.append(("missing new-family proof obligation", missing_proof))

    weak_isolation = copy.deepcopy(data)
    weak_isolation["worker_isolation"]["forbidden_inputs"] = []
    mutations.append(("missing worker isolation barrier", weak_isolation))

    for name, mutated in mutations:
        if not validate(mutated):
            failures.append(f"mutation unexpectedly passed: {name}")

    return failures


def load_guardrails(path: Path = GUARDRAILS_PATH) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("guardrails root must be an object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        data = load_guardrails()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"guardrails load failed: {exc}", file=sys.stderr)
        return 1

    errors = validate(data)
    if args.self_test:
        errors.extend(run_mutation_checks(data))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    suffix = " and mutation checks" if args.self_test else ""
    print(f"validated Goal 4 guardrails{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
