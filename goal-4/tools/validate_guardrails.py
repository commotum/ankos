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
    "LEAD_ONLY",
    "DIRECT_IDENTITY",
    "DIRECT_PARTIAL_MECHANICS",
    "DIRECT_COMPLETE_MECHANICS",
    "CORROBORATING",
    "CONTEXTUAL",
    "DEFECT_LIMITED",
}
EXPECTED_FIELD_SUPPORT = {
    "SUPPORTED",
    "NOT_APPLICABLE",
    "UNKNOWN_FROM_SOURCE",
    "CONFLICTING_SOURCE",
}
EXPECTED_SOURCE_STATUSES = {
    "CLEAR",
    "AMBIGUOUS",
    "DEFECTIVE",
    "CONFLICTING",
}
EXPECTED_MODALITIES = {
    "PROSE",
    "FORMULA",
    "CODE",
    "TABLE",
    "CAPTION",
    "IMAGE",
    "CROSS_REFERENCE",
}
EXPECTED_VISUAL_ROLES = {
    "NATIVE_EVIDENCE",
    "RELATION",
    "CONTROL",
    "OBSERVER",
    "DECORATIVE",
    "SOURCE_DEFECT",
}
EXPECTED_VISUAL_RISK_FLAGS = {
    "CONSTRUCTION_BEARING",
    "TEXT_BEARING",
    "AMBIGUOUS",
    "CAPTION_INCOMPLETE",
}
EXPECTED_LIFECYCLE_PROOF_KINDS = {
    "PROVISIONAL_COMPARISON",
    "ALIAS_IDENTITY",
    "CO_REFERENCE_IDENTITY",
    "PROVED_DUPLICATE_IDENTITY",
    "SPLIT_DISTINCTION",
}
EXPECTED_MERGE_IDENTITY_PROOFS = {
    "ALIAS_IDENTITY",
    "CO_REFERENCE_IDENTITY",
    "PROVED_DUPLICATE_IDENTITY",
}
EXPECTED_BLIND_CANDIDATE_FIELDS = {
    "id",
    "record_status",
    "provisional_name",
    "aliases",
    "discovery_stage",
    "discovery_anchor",
    "source_unit_ids",
    "source_evidence",
    "source_status",
    "image_witnesses",
    "evidence_strength",
    "field_support",
    "fingerprint",
    "parameters",
    "variants",
    "missing_mechanics",
    "uncertainties",
    "related_candidate_ids",
    "cross_reference_ids",
    "evidence_reassignments",
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
        "SOLVER_OR_NUMERICAL_METHOD",
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
    "proposed_t_ids",
    "catalog_mapping",
    "catalog_action",
    "catalog_verdict",
    "semantic_role",
    "family_action",
    "existing_family",
    "nearest_family",
    "reuse_verdict",
    "equivalence_verdict",
    "novelty_verdict",
    "api_fit",
    "api_mapping",
    "implementation_target",
    "implementation_priority",
    "implementation_cost",
    "executor",
    "runtime_class",
    "runtime_support",
}
EXPECTED_FAMILY_RELATIONS = {
    "MEMBER_OF",
    "INSTANCE_OF",
    "RESTRICTS",
    "SEEDS",
    "REPRESENTS",
    "OBSERVES",
    "APPLIES",
    "EMULATES",
    "SOLVES",
    "COMPOSES",
    "ALIASES",
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
    capture_rule = data.get("candidate_capture_rule")
    if not isinstance(capture_rule, dict):
        errors.append("candidate_capture_rule must be an object")
    else:
        for key in (
            "necessary",
            "sufficient",
            "nonqualifying",
            "formula_boundary",
            "unnamed_boundary",
        ):
            if not isinstance(capture_rule.get(key), str) or not capture_rule[key].strip():
                errors.append(f"candidate_capture_rule.{key} must be non-empty")

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
        allocation_order = policy.get("allocation_order", "")
        for required_phrase in (
            "immutable discovery epoch",
            "frozen audit traversal",
            "first unread canonical path",
            "Stage 4 local-search hits",
            "chapter followed by its paired Notes",
            "Stage 17 Index",
            "Stage 18 saturation",
            "reopened blind pass increments the epoch",
            "prior search-prefix closure",
            "active epoch",
            "root merge",
        ):
            if required_phrase not in allocation_order:
                errors.append(
                    "candidate_id_policy.allocation_order lacks "
                    f"{required_phrase!r}"
                )
    evidence_id_policy = data.get("evidence_id_policy")
    if not isinstance(evidence_id_policy, str) or not all(
        phrase in evidence_id_policy
        for phrase in (
            "E###### identifiers are unique and contiguous",
            "strictly increasing E order",
            "global evidence stream in numeric E order",
            "later E may append to an earlier active B",
            "G###### identifiers are contiguous",
            "minimum allocated E identifier",
        )
    ):
        errors.append("evidence_id_policy is incomplete")

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
    for key, expected in (
        ("field_support_statuses", EXPECTED_FIELD_SUPPORT),
        ("source_statuses", EXPECTED_SOURCE_STATUSES),
        ("evidence_modalities", EXPECTED_MODALITIES),
    ):
        values = data.get(key)
        if not isinstance(values, list) or set(values) != expected:
            errors.append(f"{key} does not match the frozen vocabulary")
        elif _duplicates(values):
            errors.append(f"{key} contains duplicates")
    uncertainty_contract = data.get("source_uncertainty_contract")
    if not isinstance(uncertainty_contract, str) or not all(
        phrase in uncertainty_contract
        for phrase in (
            "CLEAR requires an empty uncertainty boundary",
            "require a meaningful nonempty boundary",
            "SOURCE_DEFECT_OR_AMBIGUITY",
            "SOURCE_DEFECT cannot be CLEAR",
            "Pending rows carry no adjudicated uncertainty",
        )
    ):
        errors.append("source_uncertainty_contract is incomplete")
    review_epoch_contract = data.get("review_epoch_contract")
    if not isinstance(review_epoch_contract, str) or not all(
        phrase in review_epoch_contract
        for phrase in (
            "PENDING reading or asset row has a blank review_epoch",
            "positive active global review_epoch",
            "INITIAL review may therefore occur in any active epoch",
            "formal re-review opens the next epoch with REOPEN",
            "SEARCH_ENRICHMENT does not change review_epoch",
            "Epoch 1 may end after a partial canonical prefix",
            "matching review event at the same epoch",
            "immutable INITIAL/REOPEN history paths",
            "before the next epoch begins",
            "zero-discovery pass",
        )
    ) or any(
        stale in review_epoch_contract
        for stale in (
            "1 for its initial review",
            "Epoch-1 LOCAL coverage is exact",
        )
    ):
        errors.append("review_epoch_contract is incomplete")
    review_history_contract = data.get("review_history_contract")
    if not isinstance(review_history_contract, str) or not all(
        phrase in review_history_contract
        for phrase in (
            "review-history.jsonl",
            "append-only V###### hash chain",
            "exactly one canonical source path",
            "complete ordered reading/asset result snapshot",
            "independently recomputable digest",
            "chains previous_path_result_sha256",
            "INITIAL and REOPEN record full semantic review snapshots",
            "INITIAL consumes the first unread canonical path",
            "SEARCH_ENRICHMENT stays in the active epoch",
            "typed non-EXCLUSION trigger H IDs",
            "latest path snapshot exactly equals current full rows",
        )
    ):
        errors.append("review_history_contract is incomplete")
    enrichment_contract = data.get("search_enrichment_contract")
    if not isinstance(enrichment_contract, str) or not all(
        phrase in enrichment_contract
        for phrase in (
            "hit-addressed reading",
            "additive secondary/candidate/route arrays",
            "exact same-path, same-epoch",
            "non-EXCLUSION trigger hit",
            "exact unit",
            "Asset changes are limited",
            "cannot change completion metadata",
            "At least one allowed delta",
        )
    ):
        errors.append("search_enrichment_contract is incomplete")
    for key in ("evidence_application", "visual_evidence_rule"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(f"{key} must be non-empty")
    for key, expected in (
        ("visual_roles", EXPECTED_VISUAL_ROLES),
        ("visual_risk_flags", EXPECTED_VISUAL_RISK_FLAGS),
    ):
        values = data.get(key)
        if not isinstance(values, list) or set(values) != expected:
            errors.append(f"{key} does not match the frozen vocabulary")
        elif _duplicates(values):
            errors.append(f"{key} contains duplicates")
    if not isinstance(data.get("discovery_anchor_contract"), str) or not data[
        "discovery_anchor_contract"
    ].strip():
        errors.append("discovery_anchor_contract must be non-empty")
    lifecycle = data.get("lifecycle_relation_contract")
    if not isinstance(lifecycle, dict) or set(lifecycle) != {
        "proof_kinds",
        "merge_identity_proof_kinds",
        "merge_evidence_strength",
        "split_proof_kind",
        "split_rationale_fields",
        "provisional_proof_kind",
    }:
        errors.append("lifecycle_relation_contract fields are invalid")
    else:
        proof_kinds = lifecycle["proof_kinds"]
        if (
            not isinstance(proof_kinds, list)
            or not all(isinstance(item, str) for item in proof_kinds)
            or set(proof_kinds) != EXPECTED_LIFECYCLE_PROOF_KINDS
            or _duplicates(proof_kinds)
        ):
            errors.append("lifecycle proof kinds do not match the frozen contract")
        merge_proofs = lifecycle["merge_identity_proof_kinds"]
        if (
            not isinstance(merge_proofs, list)
            or not all(isinstance(item, str) for item in merge_proofs)
            or set(merge_proofs) != EXPECTED_MERGE_IDENTITY_PROOFS
            or _duplicates(merge_proofs)
        ):
            errors.append(
                "merge identity proof kinds do not match the frozen contract"
            )
        if lifecycle["merge_evidence_strength"] != "DIRECT_IDENTITY":
            errors.append("merge identity proof must require DIRECT_IDENTITY")
        if lifecycle["split_proof_kind"] != "SPLIT_DISTINCTION":
            errors.append("split proof kind must be SPLIT_DISTINCTION")
        if lifecycle["split_rationale_fields"] != [
            "before_rationale",
            "after_rationale",
        ]:
            errors.append("split rationale fields are not exact")
        if lifecycle["provisional_proof_kind"] != "PROVISIONAL_COMPARISON":
            errors.append("provisional lifecycle proof kind is invalid")
    route_scopes = data.get("route_closure_scopes")
    if not isinstance(route_scopes, dict) or set(route_scopes) != {
        "WITHIN_STAGE",
        "CROSS_RANGE",
    }:
        errors.append("route_closure_scopes do not match the frozen contract")
    elif any(
        not isinstance(value, str) or not value.strip()
        for value in route_scopes.values()
    ):
        errors.append("route_closure_scopes definitions must be non-empty")
    search_language = data.get("search_query_language")
    if (
        not isinstance(search_language, dict)
        or set(search_language) != {"modes", "fields", "execution"}
        or search_language.get("modes") != ["LITERAL", "REGEX"]
        or set(search_language.get("fields", []))
        != {
            "query_id",
            "family",
            "pattern",
            "mode",
            "case_sensitive",
            "whole_word",
            "scope_paths",
        }
        or not isinstance(search_language.get("execution"), str)
        or not search_language["execution"].strip()
    ):
        errors.append("search_query_language does not match the frozen contract")

    blind_fields = data.get("blind_candidate_fields")
    if not isinstance(blind_fields, list) or not blind_fields:
        errors.append("blind_candidate_fields must be a non-empty list")
        blind_field_set: set[str] = set()
    else:
        blind_field_set = set(blind_fields)
        if blind_field_set != EXPECTED_BLIND_CANDIDATE_FIELDS:
            errors.append("blind_candidate_fields do not match the frozen contract")
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

    axis_rules = data.get("final_axis_rules")
    if not isinstance(axis_rules, dict):
        errors.append("final_axis_rules must be an object")
    else:
        for key in (
            "semantic_role_primary",
            "axis_local_insufficiency",
            "existing_family_reference",
            "failed_reuse_rule",
        ):
            if not isinstance(axis_rules.get(key), str) or not axis_rules[key].strip():
                errors.append(f"final_axis_rules.{key} must be non-empty")

    family_relations = data.get("family_relations")
    if not isinstance(family_relations, list) or set(family_relations) != (
        EXPECTED_FAMILY_RELATIONS
    ):
        errors.append("family_relations do not match the frozen vocabulary")
    elif _duplicates(family_relations):
        errors.append("family_relations contain duplicates")
    if not isinstance(data.get("family_relation_rule"), str) or not data[
        "family_relation_rule"
    ].strip():
        errors.append("family_relation_rule must be non-empty")

    proofs = data.get("proof_obligations")
    if not isinstance(proofs, dict) or set(proofs) != EXPECTED_PROOFS:
        errors.append("proof_obligations do not match the required cases")
    else:
        for key, obligations in proofs.items():
            if not isinstance(obligations, list) or not obligations:
                errors.append(f"proof_obligations.{key} must be non-empty")
            elif any(not isinstance(item, str) or not item.strip() for item in obligations):
                errors.append(f"proof_obligations.{key} contains an empty obligation")
            elif _duplicates(obligations):
                errors.append(f"proof_obligations.{key} contains duplicates")

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
        context_mode = isolation.get("context_mode")
        if not isinstance(context_mode, str) or not all(
            token in context_mode.lower() for token in ("sealed", "sandbox")
        ):
            errors.append("worker isolation must require a sealed sandbox")

    schema_policy = data.get("blind_schema_policy")
    if not isinstance(schema_policy, dict):
        errors.append("blind_schema_policy must be an object")
    else:
        for key in (
            "allowlist_only",
            "additional_properties",
            "generic_extension_objects_allowed",
            "separate_reconciliation_schema_until_stage_19",
        ):
            if not isinstance(schema_policy.get(key), bool):
                errors.append(f"blind_schema_policy.{key} must be boolean")
        if schema_policy.get("allowlist_only") is not True:
            errors.append("blind schemas must be allowlist-only")
        if schema_policy.get("additional_properties") is not False:
            errors.append("blind schemas must reject additional properties")
        if schema_policy.get("generic_extension_objects_allowed") is not False:
            errors.append("blind schemas must reject generic extension objects")
        if schema_policy.get("separate_reconciliation_schema_until_stage_19") is not True:
            errors.append("reconciliation schemas must remain separate until Stage 19")
        patterns = schema_policy.get("free_text_review_patterns")
        if not isinstance(patterns, list) or len(patterns) < 6:
            errors.append("blind free-text review patterns are incomplete")
        post_freeze = schema_policy.get("post_freeze_policy")
        if not isinstance(post_freeze, str) or not post_freeze.strip():
            errors.append("blind post-freeze policy must be non-empty")

    freeze = data.get("blind_freeze_requirements")
    if not isinstance(freeze, list) or len(freeze) < 6:
        errors.append("blind_freeze_requirements must contain the full closure contract")
    elif not any(
        "Stage 4 through 17 review-history" in requirement
        and "(stage, epoch)" in requirement
        and "exact LOCAL-round scope union" in requirement
        and "before a later epoch can begin" in requirement
        and "before the Stage 18 saturation fixed point" in requirement
        and "zero-discovery passes" in requirement
        for requirement in freeze
        if isinstance(requirement, str)
    ):
        errors.append(
            "blind_freeze_requirements lack exact pre-saturation LOCAL coverage"
        )
    triggers = data.get("close_review_triggers")
    if not isinstance(triggers, list) or len(triggers) < 6:
        errors.append("close_review_triggers must define hostile-review coverage")
    if not isinstance(data.get("saturation_fixed_point"), str) or not data[
        "saturation_fixed_point"
    ].strip():
        errors.append("saturation_fixed_point must be non-empty")

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

    open_schema = copy.deepcopy(data)
    open_schema["blind_schema_policy"]["additional_properties"] = True
    mutations.append(("blind schema permits additional properties", open_schema))

    missing_solver = copy.deepcopy(data)
    missing_solver["final_classification_vocabularies"]["semantic_role"].remove(
        "SOLVER_OR_NUMERICAL_METHOD"
    )
    mutations.append(("missing solver/numerical-method role", missing_solver))

    missing_reassignment = copy.deepcopy(data)
    missing_reassignment["blind_candidate_fields"].remove(
        "evidence_reassignments"
    )
    mutations.append(
        ("missing tombstone evidence reassignment field", missing_reassignment)
    )

    missing_visual_risk = copy.deepcopy(data)
    missing_visual_risk["visual_risk_flags"].remove("TEXT_BEARING")
    mutations.append(("missing visual risk flag", missing_visual_risk))

    missing_uncertainty_boundary = copy.deepcopy(data)
    missing_uncertainty_boundary["source_uncertainty_contract"] = (
        "Source quality is recorded."
    )
    mutations.append(
        ("missing exact source uncertainty boundary", missing_uncertainty_boundary)
    )

    missing_review_epoch = copy.deepcopy(data)
    missing_review_epoch["review_epoch_contract"] = (
        "Reviewed rows may have an epoch."
    )
    mutations.append(
        ("missing source review epoch contract", missing_review_epoch)
    )

    stale_review_epoch = copy.deepcopy(data)
    stale_review_epoch["review_epoch_contract"] = (
        "Every PENDING reading or asset row has a blank review_epoch. Every "
        "reviewed row has a positive review_epoch, with 1 for its initial "
        "review and a formal re-review later. Epoch-1 LOCAL coverage is exact."
    )
    mutations.append(("stale scalar review epoch contract", stale_review_epoch))

    missing_review_history = copy.deepcopy(data)
    del missing_review_history["review_history_contract"]
    mutations.append(("missing append-only review history", missing_review_history))

    missing_enrichment_contract = copy.deepcopy(data)
    del missing_enrichment_contract["search_enrichment_contract"]
    mutations.append(
        ("missing typed search enrichment", missing_enrichment_contract)
    )

    missing_evidence_id_policy = copy.deepcopy(data)
    del missing_evidence_id_policy["evidence_id_policy"]
    mutations.append(
        ("missing append-compatible E/G allocation", missing_evidence_id_policy)
    )

    open_search_language = copy.deepcopy(data)
    open_search_language["search_query_language"]["fields"].append("command")
    mutations.append(("open-ended search query language", open_search_language))

    duplicate_proof = copy.deepcopy(data)
    duplicate_proof["proof_obligations"]["same_family"].append(
        duplicate_proof["proof_obligations"]["same_family"][0]
    )
    mutations.append(("duplicate proof obligation", duplicate_proof))

    generic_merge_proof = copy.deepcopy(data)
    generic_merge_proof["lifecycle_relation_contract"][
        "merge_evidence_strength"
    ] = "DIRECT_COMPLETE_MECHANICS"
    mutations.append(
        ("generic mechanics permits lifecycle merge", generic_merge_proof)
    )

    missing_split_rationale = copy.deepcopy(data)
    missing_split_rationale["lifecycle_relation_contract"][
        "split_rationale_fields"
    ] = ["after_rationale"]
    mutations.append(
        ("split lifecycle loses before rationale", missing_split_rationale)
    )

    missing_local_coverage = copy.deepcopy(data)
    missing_local_coverage["blind_freeze_requirements"] = [
        requirement
        for requirement in missing_local_coverage["blind_freeze_requirements"]
        if "Stage 4 through 17 review-history" not in requirement
    ]
    mutations.append(
        ("freeze omits exact LOCAL-round coverage", missing_local_coverage)
    )

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
