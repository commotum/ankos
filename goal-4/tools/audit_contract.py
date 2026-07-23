"""Shared structural contract for Goal 4 audit ledgers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


GOAL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = GOAL_DIR.parent

READING_HEADER = [
    "source_unit_id",
    "document_order",
    "path",
    "block_kind",
    "byte_start",
    "byte_end",
    "line_start",
    "line_end",
    "global_line_start",
    "global_line_end",
    "unit_sha256",
    "review_status",
    "review_disposition",
    "source_status",
    "secondary_roles",
    "candidate_ids",
    "route_ids",
    "evidence_statement",
    "review_stage",
    "reviewer",
]

CROSS_REFERENCE_HEADER = [
    "route_id",
    "source_unit_id",
    "literal_target",
    "route_kind",
    "expected_topic",
    "owning_stage",
    "status",
    "target_unit_ids",
    "attempts",
    "vocabulary_terms",
    "defect_boundary",
]

ASSET_HEADER = [
    "asset_id",
    "link_id",
    "physical_path",
    "sha256",
    "bytes",
    "source_path",
    "source_unit_id",
    "assignment_path",
    "assignment_stage",
    "assignment_basis",
    "reference_status",
    "inspection_status",
    "visual_role",
    "risk_flags",
    "original_resolution_status",
    "transcription_status",
    "candidate_ids",
    "evidence_statement",
    "review_stage",
    "reviewer",
    "uncertainty",
]

READING_DISPOSITIONS = [
    "CANDIDATE",
    "SUPPORTS_CANDIDATE",
    "CROSS_REFERENCE",
    "REPRESENTATION_OR_OBSERVER",
    "APPLICATION_OR_EMULATION",
    "HISTORICAL_ONLY",
    "NO_CONSTRUCTION",
    "SOURCE_DEFECT_OR_AMBIGUITY",
]
SOURCE_STATUSES = ["CLEAR", "AMBIGUOUS", "DEFECTIVE", "CONFLICTING"]
SECONDARY_ROLES = [
    "PROPERTY_OR_RESTRICTION",
    "SEED_INPUT_OR_BOUNDARY",
    "BEHAVIOR_OR_OUTCOME",
    "REPRESENTATION",
    "OBSERVER_OR_ANALYZER",
    "APPLICATION",
    "EMULATION",
    "COMPOSITION_OR_COUPLING",
    "IMPLEMENTATION_DETAIL",
    "CONTROL_OR_COMPARISON",
    "HISTORICAL_MENTION",
    "EXTERNAL_ONLY",
    "SOURCE_DEFECT",
]
EVIDENCE_STRENGTHS = [
    "LEAD_ONLY",
    "DIRECT_IDENTITY",
    "DIRECT_PARTIAL_MECHANICS",
    "DIRECT_COMPLETE_MECHANICS",
    "CORROBORATING",
    "CONTEXTUAL",
    "DEFECT_LIMITED",
]
EVIDENCE_MODALITIES = [
    "PROSE",
    "FORMULA",
    "CODE",
    "TABLE",
    "CAPTION",
    "IMAGE",
    "CROSS_REFERENCE",
]
FIELD_SUPPORT_STATUSES = [
    "SUPPORTED",
    "NOT_APPLICABLE",
    "UNKNOWN_FROM_SOURCE",
    "CONFLICTING_SOURCE",
]
FINGERPRINT_FIELDS = [
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
]
CANDIDATE_FIELDS = [
    "id",
    "record_status",
    "provisional_name",
    "aliases",
    "discovery_stage",
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
]
FORBIDDEN_BLIND_FIELDS = [
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
]

VISUAL_ROLES = [
    "NATIVE_EVIDENCE",
    "RELATION",
    "CONTROL",
    "OBSERVER",
    "DECORATIVE",
    "SOURCE_DEFECT",
]
VISUAL_RISK_FLAGS = [
    "CONSTRUCTION_BEARING",
    "TEXT_BEARING",
    "AMBIGUOUS",
    "CAPTION_INCOMPLETE",
]
ROUTE_KINDS = ["PAGE", "SECTION", "NOTES", "INDEX", "ALIAS", "OTHER"]
ROUTE_STATUSES = ["PENDING", "RESOLVED", "MISSING_TARGET_FINAL"]
SEARCH_HIT_DISPOSITIONS = [
    "GOVERNED_CANDIDATE_OR_SUPPORT",
    "DUPLICATE",
    "CROSS_REFERENCE",
    "CONTROL_OR_RELATIONSHIP",
    "EXCLUSION",
]


def _string_array(enum: list[str] | None = None) -> dict[str, Any]:
    item: dict[str, Any] = {"type": "string"}
    if enum is not None:
        item["enum"] = enum
    return {"type": "array", "items": item, "uniqueItems": True}


def _csv_row_schema(
    title: str,
    header: list[str],
    properties: dict[str, Any],
) -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": title,
        "type": "object",
        "required": header,
        "properties": properties,
        "additionalProperties": False,
    }


def fingerprint_value_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "required": ["status", "value", "evidence_ids", "reason"],
        "properties": {
            "status": {"type": "string", "enum": FIELD_SUPPORT_STATUSES},
            "value": {"type": ["string", "null"]},
            "evidence_ids": _string_array(),
            "reason": {"type": "string"},
        },
        "additionalProperties": False,
    }


def candidate_schema(id_pattern: str = "^B[0-9]{4}$") -> dict[str, Any]:
    evidence_schema = {
        "type": "object",
        "required": [
            "evidence_id",
            "source_unit_id",
            "image_path",
            "strength",
            "modality",
            "claim",
            "fingerprint_fields",
        ],
        "properties": {
            "evidence_id": {"type": "string"},
            "source_unit_id": {"type": ["string", "null"]},
            "image_path": {"type": ["string", "null"]},
            "strength": {"type": "string", "enum": EVIDENCE_STRENGTHS},
            "modality": {"type": "string", "enum": EVIDENCE_MODALITIES},
            "claim": {"type": "string"},
            "fingerprint_fields": _string_array(FINGERPRINT_FIELDS),
        },
        "additionalProperties": False,
    }
    parameter_schema = {
        "type": "object",
        "required": ["name", "source_description", "evidence_ids"],
        "properties": {
            "name": {"type": "string"},
            "source_description": {"type": "string"},
            "evidence_ids": _string_array(),
        },
        "additionalProperties": False,
    }
    relation_schema = {
        "type": "object",
        "required": ["candidate_id", "relation", "evidence_ids", "uncertainty"],
        "properties": {
            "candidate_id": {"type": "string", "pattern": id_pattern},
            "relation": {
                "type": "string",
                "enum": [
                    "POSSIBLY_SAME_AS",
                    "POSSIBLE_VARIANT_OF",
                    "SOURCE_COMPARE",
                ],
            },
            "evidence_ids": _string_array(),
            "uncertainty": {"type": "string"},
        },
        "additionalProperties": False,
    }
    properties: dict[str, Any] = {
        "id": {"type": "string", "pattern": id_pattern},
        "record_status": {
            "type": "string",
            "enum": ["ACTIVE", "MERGED_REDIRECT", "SPLIT_SUPERSEDED"],
        },
        "provisional_name": {"type": "string", "minLength": 1},
        "aliases": _string_array(),
        "discovery_stage": {"type": "integer", "minimum": 4, "maximum": 18},
        "source_unit_ids": _string_array(),
        "source_evidence": {"type": "array", "items": evidence_schema},
        "source_status": _string_array(SOURCE_STATUSES),
        "image_witnesses": _string_array(),
        "evidence_strength": _string_array(EVIDENCE_STRENGTHS),
        "field_support": {
            "type": "object",
            "required": FINGERPRINT_FIELDS,
            "properties": {
                field: {"type": "string", "enum": FIELD_SUPPORT_STATUSES}
                for field in FINGERPRINT_FIELDS
            },
            "additionalProperties": False,
        },
        "fingerprint": {
            "type": "object",
            "required": FINGERPRINT_FIELDS,
            "properties": {
                field: fingerprint_value_schema() for field in FINGERPRINT_FIELDS
            },
            "additionalProperties": False,
        },
        "parameters": {"type": "array", "items": parameter_schema},
        "variants": {"type": "array", "items": parameter_schema},
        "missing_mechanics": _string_array(),
        "uncertainties": _string_array(),
        "related_candidate_ids": {"type": "array", "items": relation_schema},
        "cross_reference_ids": _string_array(),
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Blind candidate record",
        "type": "object",
        "required": CANDIDATE_FIELDS,
        "properties": properties,
        "additionalProperties": False,
    }


def schema_documents() -> dict[str, dict[str, Any]]:
    reading_properties = {
        field: {"type": "string"} for field in READING_HEADER
    }
    reading_properties.update(
        {
            "review_status": {"type": "string", "enum": ["PENDING", "REVIEWED"]},
            "review_disposition": {
                "type": "string",
                "enum": [""] + READING_DISPOSITIONS,
            },
            "source_status": {"type": "string", "enum": [""] + SOURCE_STATUSES},
        }
    )
    cross_properties = {
        field: {"type": "string"} for field in CROSS_REFERENCE_HEADER
    }
    cross_properties["route_kind"] = {"type": "string", "enum": ROUTE_KINDS}
    cross_properties["status"] = {"type": "string", "enum": ROUTE_STATUSES}
    asset_properties = {
        field: {"type": "string"} for field in ASSET_HEADER
    }
    asset_properties.update(
        {
            "reference_status": {
                "type": "string",
                "enum": ["REFERENCED", "UNREFERENCED_PHYSICAL"],
            },
            "inspection_status": {
                "type": "string",
                "enum": ["PENDING", "SCREENED"],
            },
            "visual_role": {"type": "string", "enum": [""] + VISUAL_ROLES},
            "original_resolution_status": {
                "type": "string",
                "enum": ["NOT_REVIEWED", "NOT_REQUIRED", "REVIEWED"],
            },
            "transcription_status": {
                "type": "string",
                "enum": ["NOT_APPLICABLE", "NOT_REQUIRED", "CHECKED"],
            },
        }
    )
    query_schema = {
        "type": "object",
        "required": ["query_id", "family", "pattern", "flags", "scope_paths"],
        "properties": {
            "query_id": {"type": "string", "pattern": "^Q[0-9]{4}$"},
            "family": {"type": "string"},
            "pattern": {"type": "string"},
            "flags": _string_array(),
            "scope_paths": _string_array(),
        },
        "additionalProperties": False,
    }
    hit_schema = {
        "type": "object",
        "required": [
            "hit_id",
            "query_id",
            "source_unit_id",
            "context_sha256",
            "disposition",
            "candidate_ids",
            "route_ids",
            "rationale",
        ],
        "properties": {
            "hit_id": {"type": "string", "pattern": "^H[0-9]{6}$"},
            "query_id": {"type": "string", "pattern": "^Q[0-9]{4}$"},
            "source_unit_id": {"type": "string", "pattern": "^U[0-9]{6}$"},
            "context_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
            "disposition": {
                "type": "string",
                "enum": SEARCH_HIT_DISPOSITIONS,
            },
            "candidate_ids": _string_array(),
            "route_ids": _string_array(),
            "rationale": {"type": "string", "minLength": 1},
        },
        "additionalProperties": False,
    }
    round_schema = {
        "type": "object",
        "required": [
            "round_id",
            "queries",
            "tool_assumptions",
            "result_ids",
            "result_digest",
            "hits",
            "new_vocabulary",
            "new_candidates",
            "new_evidence_groups",
            "new_routes",
            "rerun_digest",
        ],
        "properties": {
            "round_id": {"type": "string", "pattern": "^S[0-9]{3}$"},
            "queries": {"type": "array", "items": query_schema},
            "tool_assumptions": _string_array(),
            "result_ids": _string_array(),
            "result_digest": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
            "hits": {"type": "array", "items": hit_schema},
            "new_vocabulary": _string_array(),
            "new_candidates": _string_array(),
            "new_evidence_groups": _string_array(),
            "new_routes": _string_array(),
            "rerun_digest": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        },
        "additionalProperties": False,
    }
    fixed_point_schema = {
        "type": "object",
        "required": [
            "round_id",
            "zero_delta",
            "rerun_reproduced",
            "result_digest",
        ],
        "properties": {
            "round_id": {"type": "string", "pattern": "^S[0-9]{3}$"},
            "zero_delta": {"const": True},
            "rerun_reproduced": {"const": True},
            "result_digest": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        },
        "additionalProperties": False,
    }
    search_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Blind search rounds",
        "type": "object",
        "required": [
            "schema_version",
            "phase",
            "tool_assumptions",
            "vocabulary",
            "rounds",
            "fixed_point",
        ],
        "properties": {
            "schema_version": {"const": 1},
            "phase": {"const": "blind_discovery"},
            "tool_assumptions": _string_array(),
            "vocabulary": _string_array(),
            "rounds": {"type": "array", "items": round_schema},
            "fixed_point": {"oneOf": [{"type": "null"}, fixed_point_schema]},
        },
        "additionalProperties": False,
    }
    classification_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Stage 20 classification row",
        "type": "object",
        "required": [
            "candidate_id",
            "catalog_action",
            "semantic_role",
            "semantic_subtype",
            "family_action",
            "family_relations",
            "rationale",
            "evidence_ids",
            "hostile_review_required",
        ],
        "properties": {
            "candidate_id": {"type": "string", "pattern": "^B[0-9]{4}$"},
            "catalog_action": {"type": "string"},
            "semantic_role": {"type": "string"},
            "semantic_subtype": {"type": ["string", "null"]},
            "family_action": {"type": "string"},
            "family_relations": {"type": "array"},
            "rationale": {"type": "string"},
            "evidence_ids": _string_array(),
            "hostile_review_required": {"type": "boolean"},
        },
        "additionalProperties": False,
    }
    coverage_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Stage 19+ coverage join row",
        "type": "object",
        "required": [
            "candidate_id",
            "existing_t_ids",
            "proposed_t_id",
            "source_unit_ids",
            "reconciliation_result",
        ],
        "properties": {
            "candidate_id": {"type": "string", "pattern": "^B[0-9]{4}$"},
            "existing_t_ids": _string_array(),
            "proposed_t_id": {"type": ["string", "null"]},
            "source_unit_ids": _string_array(),
            "reconciliation_result": {"type": "string"},
        },
        "additionalProperties": False,
    }
    reading_schema = _csv_row_schema(
        "Blind reading-ledger row", READING_HEADER, reading_properties
    )
    cross_schema = _csv_row_schema(
        "Blind cross-reference row",
        CROSS_REFERENCE_HEADER,
        cross_properties,
    )
    asset_schema = _csv_row_schema(
        "Blind asset-ledger row", ASSET_HEADER, asset_properties
    )
    worker_output_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Sealed blind-worker output",
        "type": "object",
        "required": [
            "worker_id",
            "bundle_sha256",
            "prompt_sha256",
            "schema_sha256",
            "allowed_manifest_sha256",
            "prohibited_input_nonuse",
            "reading_updates",
            "candidate_proposals",
            "asset_updates",
            "route_proposals",
            "uncertainties",
        ],
        "properties": {
            "worker_id": {"type": "string"},
            "bundle_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
            "prompt_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
            "schema_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
            "allowed_manifest_sha256": {
                "type": "string",
                "pattern": "^[0-9a-f]{64}$",
            },
            "prohibited_input_nonuse": {"const": True},
            "reading_updates": {"type": "array", "items": reading_schema},
            "candidate_proposals": {
                "type": "array",
                "items": candidate_schema("^W[0-9]{4}$"),
            },
            "asset_updates": {"type": "array", "items": asset_schema},
            "route_proposals": {"type": "array", "items": cross_schema},
            "uncertainties": _string_array(),
        },
        "additionalProperties": False,
    }
    return {
        "blind/reading-ledger-row.schema.json": reading_schema,
        "blind/candidate-record.schema.json": candidate_schema(),
        "blind/cross-reference-row.schema.json": cross_schema,
        "blind/asset-ledger-row.schema.json": asset_schema,
        "blind/search-rounds.schema.json": search_schema,
        "blind/worker-output.schema.json": worker_output_schema,
        "reconciliation/classification-row.schema.json": classification_schema,
        "reconciliation/coverage-row.schema.json": coverage_schema,
    }


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")
