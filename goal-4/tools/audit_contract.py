"""Shared structural contract for Goal 4 audit ledgers."""

from __future__ import annotations

import hashlib
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
    "review_epoch",
    "review_disposition",
    "source_status",
    "uncertainty",
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
    "source_asset_id",
    "discovery_epoch",
    "discovery_kind",
    "discovery_id",
    "discovery_ordinal",
    "literal_target",
    "route_kind",
    "expected_topic",
    "owning_stage",
    "closure_scope",
    "status",
    "target_unit_ids",
    "target_asset_ids",
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
    "review_epoch",
    "visual_role",
    "source_status",
    "risk_flags",
    "original_resolution_status",
    "transcription_status",
    "candidate_ids",
    "route_ids",
    "evidence_statement",
    "review_stage",
    "reviewer",
    "uncertainty",
]

REVIEW_HISTORY_FIELDS = [
    "review_id",
    "epoch",
    "stage",
    "mode",
    "reviewer",
    "source_paths",
    "source_unit_ids",
    "asset_ids",
    "prior_search_round_count",
    "prior_search_rounds_sha256",
    "previous_path_result_sha256",
    "trigger_search_kind",
    "trigger_hit_ids",
    "candidate_changes",
    "input_projection_sha256",
    "result_snapshot",
    "result_projection_sha256",
    "previous_event_sha256",
    "event_sha256",
]
REVIEW_MODES = ["INITIAL", "REOPEN", "SEARCH_ENRICHMENT"]
SEARCH_ENRICHMENT_TRIGGER_KINDS = ["LOCAL", "SATURATION"]
CANDIDATE_CHANGE_FIELDS = [
    "action",
    "candidate_id",
    "previous_candidate_result_sha256",
    "before_candidate",
    "before_candidate_sha256",
    "after_candidate",
    "after_candidate_sha256",
]
CANDIDATE_CHANGE_ACTIONS = ["CREATE", "UPDATE"]
READING_REVIEW_RESULT_FIELDS = [
    "source_unit_id",
    "review_status",
    "review_epoch",
    "review_disposition",
    "source_status",
    "uncertainty",
    "secondary_roles",
    "candidate_ids",
    "route_ids",
    "evidence_statement",
    "review_stage",
    "reviewer",
]
ASSET_REVIEW_RESULT_FIELDS = [
    "asset_id",
    "inspection_status",
    "review_epoch",
    "visual_role",
    "source_status",
    "risk_flags",
    "original_resolution_status",
    "transcription_status",
    "candidate_ids",
    "route_ids",
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
ROUTE_CLOSURE_SCOPES = ["WITHIN_STAGE", "CROSS_RANGE"]
ROUTE_STATUSES = ["PENDING", "RESOLVED", "MISSING_TARGET_FINAL"]
SEARCH_HIT_DISPOSITIONS = [
    "GOVERNED_CANDIDATE_OR_SUPPORT",
    "DUPLICATE",
    "CROSS_REFERENCE",
    "CONTROL_OR_RELATIONSHIP",
    "EXCLUSION",
]
LIFECYCLE_PROOF_KINDS = [
    "PROVISIONAL_COMPARISON",
    "ALIAS_IDENTITY",
    "CO_REFERENCE_IDENTITY",
    "PROVED_DUPLICATE_IDENTITY",
    "SPLIT_DISTINCTION",
]
MERGE_IDENTITY_PROOF_KINDS = {
    "ALIAS_IDENTITY",
    "CO_REFERENCE_IDENTITY",
    "PROVED_DUPLICATE_IDENTITY",
}
CATALOG_ACTIONS = [
    "EXISTING_ENTRY_SUFFICIENT",
    "EXISTING_ENTRY_NEEDS_CORRECTION",
    "ADD_CATALOG_ENTRY",
    "NO_SEPARATE_CATALOG_ENTRY",
    "INSUFFICIENT_BOOK_EVIDENCE",
]
SEMANTIC_ROLES = [
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
]
SEMANTIC_SUBTYPES = [
    "SPECIALIZATION",
    "PRESET",
    "PROPERTY",
    "RESTRICTION",
    "SEED_CLASS",
    "INPUT_CLASS",
    "BOUNDARY_CLASS",
    "REPRESENTATION",
    "CODEC",
    "OBSERVER",
    "ANALYZER",
    "APPLICATION",
    "EMULATION",
    "SOLVER",
    "NUMERICAL_METHOD",
]
FAMILY_ACTIONS = [
    "EXISTING_SEMANTIC_FAMILY",
    "NEW_SEMANTIC_FAMILY",
    "SOURCE_INSUFFICIENT_FOR_FAMILY",
]
FAMILY_RELATIONS = [
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
]
PROOF_CASES = [
    "same_family",
    "specialization_preset_property_seed",
    "composition_hybrid",
    "representation_observer_application_emulation",
    "new_catalog_entry",
    "new_semantic_family",
    "source_insufficient",
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


def candidate_schema(
    id_pattern: str = "^B[0-9]{4}$",
    evidence_id_pattern: str = "^E[0-9]{6}$",
    evidence_group_pattern: str = "^G[0-9]{6}$",
) -> dict[str, Any]:
    evidence_schema = {
        "type": "object",
        "required": [
            "evidence_id",
            "evidence_group_id",
            "discovery_anchor",
            "source_unit_id",
            "image_path",
            "strength",
            "modality",
            "claim",
            "fingerprint_fields",
        ],
        "properties": {
            "evidence_id": {
                "type": "string",
                "pattern": evidence_id_pattern,
            },
            "evidence_group_id": {
                "type": "string",
                "pattern": evidence_group_pattern,
            },
            "discovery_anchor": {
                "type": "object",
                "required": ["epoch", "kind", "id", "ordinal"],
                "properties": {
                    "epoch": {"type": "integer", "minimum": 1},
                    "kind": {
                        "type": "string",
                        "enum": ["SOURCE_UNIT", "IMAGE", "SEARCH_HIT"],
                    },
                    "id": {"type": "string"},
                    "ordinal": {"type": "integer", "minimum": 1},
                },
                "additionalProperties": False,
            },
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
        "required": [
            "candidate_id",
            "relation",
            "proof_kind",
            "evidence_ids",
            "before_rationale",
            "after_rationale",
            "uncertainty",
        ],
        "properties": {
            "candidate_id": {"type": "string", "pattern": id_pattern},
            "relation": {
                "type": "string",
                "enum": [
                    "POSSIBLY_SAME_AS",
                    "POSSIBLE_VARIANT_OF",
                    "SOURCE_COMPARE",
                    "MERGED_INTO",
                    "SPLIT_INTO",
                ],
            },
            "proof_kind": {
                "type": "string",
                "enum": LIFECYCLE_PROOF_KINDS,
            },
            "evidence_ids": _string_array(),
            "before_rationale": {"type": "string"},
            "after_rationale": {"type": "string"},
            "uncertainty": {"type": "string"},
        },
        "additionalProperties": False,
    }
    evidence_reassignment_schema = {
        "type": "object",
        "required": ["from_evidence_id", "targets"],
        "properties": {
            "from_evidence_id": {"type": "string"},
            "targets": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": ["candidate_id", "evidence_id"],
                    "properties": {
                        "candidate_id": {
                            "type": "string",
                            "pattern": id_pattern,
                        },
                        "evidence_id": {"type": "string"},
                    },
                    "additionalProperties": False,
                },
            },
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
        "discovery_anchor": {
            "type": "object",
            "required": ["epoch", "kind", "id", "ordinal"],
            "properties": {
                "epoch": {"type": "integer", "minimum": 1},
                "kind": {
                    "type": "string",
                    "enum": ["SOURCE_UNIT", "IMAGE", "SEARCH_HIT"],
                },
                "id": {"type": "string"},
                "ordinal": {"type": "integer", "minimum": 1},
            },
            "additionalProperties": False,
        },
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
        "evidence_reassignments": {
            "type": "array",
            "items": evidence_reassignment_schema,
        },
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
            "review_epoch": {
                "type": "string",
                "pattern": "^(?:|[1-9][0-9]*)$",
            },
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
    cross_properties["discovery_kind"] = {
        "type": "string",
        "enum": ["SOURCE_UNIT", "IMAGE", "SEARCH_HIT"],
    }
    cross_properties["closure_scope"] = {
        "type": "string",
        "enum": ROUTE_CLOSURE_SCOPES,
    }
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
            "review_epoch": {
                "type": "string",
                "pattern": "^(?:|[1-9][0-9]*)$",
            },
            "visual_role": {"type": "string", "enum": [""] + VISUAL_ROLES},
            "source_status": {"type": "string", "enum": [""] + SOURCE_STATUSES},
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
        "required": [
            "query_id",
            "family",
            "pattern",
            "mode",
            "case_sensitive",
            "whole_word",
            "scope_paths",
        ],
        "properties": {
            "query_id": {"type": "string", "pattern": "^Q[0-9]{4}$"},
            "family": {"type": "string"},
            "pattern": {"type": "string"},
            "mode": {"type": "string", "enum": ["LITERAL", "REGEX"]},
            "case_sensitive": {"type": "boolean"},
            "whole_word": {"type": "boolean"},
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
            "epoch",
            "kind",
            "owning_stage",
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
            "epoch": {"type": "integer", "minimum": 1},
            "kind": {"type": "string", "enum": ["LOCAL", "SATURATION"]},
            "owning_stage": {"type": "integer", "minimum": 4, "maximum": 18},
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
    reading_snapshot_schema = {
        "type": "object",
        "required": READING_REVIEW_RESULT_FIELDS,
        "properties": {
            field: {"type": "string"}
            for field in READING_REVIEW_RESULT_FIELDS
        },
        "additionalProperties": False,
    }
    reading_snapshot_schema["properties"].update(
        {
            "source_unit_id": {
                "type": "string",
                "pattern": "^U[0-9]{6}$",
            },
            "review_status": {"const": "REVIEWED"},
            "review_epoch": {
                "type": "string",
                "pattern": "^[1-9][0-9]*$",
            },
            "review_disposition": {
                "type": "string",
                "enum": READING_DISPOSITIONS,
            },
            "source_status": {"type": "string", "enum": SOURCE_STATUSES},
        }
    )
    asset_snapshot_schema = {
        "type": "object",
        "required": ASSET_REVIEW_RESULT_FIELDS,
        "properties": {
            field: {"type": "string"} for field in ASSET_REVIEW_RESULT_FIELDS
        },
        "additionalProperties": False,
    }
    asset_snapshot_schema["properties"].update(
        {
            "asset_id": {"type": "string", "pattern": "^A[0-9]{6}$"},
            "inspection_status": {"const": "SCREENED"},
            "review_epoch": {
                "type": "string",
                "pattern": "^[1-9][0-9]*$",
            },
            "visual_role": {"type": "string", "enum": VISUAL_ROLES},
            "source_status": {"type": "string", "enum": SOURCE_STATUSES},
            "original_resolution_status": {
                "type": "string",
                "enum": ["NOT_REQUIRED", "REVIEWED"],
            },
            "transcription_status": {
                "type": "string",
                "enum": ["NOT_APPLICABLE", "NOT_REQUIRED", "CHECKED"],
            },
        }
    )
    review_result_snapshot_schema = {
        "type": "object",
        "required": [
            "schema_version",
            "source_path",
            "reading_results",
            "asset_results",
        ],
        "properties": {
            "schema_version": {"const": 1},
            "source_path": {"type": "string", "minLength": 1},
            "reading_results": {
                "type": "array",
                "items": reading_snapshot_schema,
            },
            "asset_results": {
                "type": "array",
                "items": asset_snapshot_schema,
            },
        },
        "additionalProperties": False,
    }
    candidate_change_schema = {
        "type": "object",
        "required": CANDIDATE_CHANGE_FIELDS,
        "properties": {
            "action": {
                "type": "string",
                "enum": CANDIDATE_CHANGE_ACTIONS,
            },
            "candidate_id": {
                "type": "string",
                "pattern": "^B[0-9]{4}$",
            },
            "previous_candidate_result_sha256": {
                "oneOf": [
                    {"type": "null"},
                    {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                ]
            },
            "before_candidate": {
                "oneOf": [{"type": "null"}, candidate_schema()]
            },
            "before_candidate_sha256": {
                "oneOf": [
                    {"type": "null"},
                    {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                ]
            },
            "after_candidate": candidate_schema(),
            "after_candidate_sha256": {
                "type": "string",
                "pattern": "^[0-9a-f]{64}$",
            },
        },
        "additionalProperties": False,
    }
    review_history_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Append-only blind review-history event",
        "type": "object",
        "required": REVIEW_HISTORY_FIELDS,
        "properties": {
            "review_id": {"type": "string", "pattern": "^V[0-9]{6}$"},
            "epoch": {"type": "integer", "minimum": 1},
            "stage": {"type": "integer", "minimum": 4, "maximum": 17},
            "mode": {"type": "string", "enum": REVIEW_MODES},
            "reviewer": {"type": "string", "minLength": 1},
            "source_paths": _string_array(),
            "source_unit_ids": {
                "type": "array",
                "items": {
                    "type": "string",
                    "pattern": "^U[0-9]{6}$",
                },
                "uniqueItems": True,
            },
            "asset_ids": {
                "type": "array",
                "items": {
                    "type": "string",
                    "pattern": "^A[0-9]{6}$",
                },
                "uniqueItems": True,
            },
            "prior_search_round_count": {
                "type": "integer",
                "minimum": 0,
            },
            "prior_search_rounds_sha256": {
                "type": "string",
                "pattern": "^[0-9a-f]{64}$",
            },
            "previous_path_result_sha256": {
                "oneOf": [
                    {"type": "null"},
                    {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                ]
            },
            "trigger_search_kind": {
                "oneOf": [
                    {"type": "null"},
                    {
                        "type": "string",
                        "enum": SEARCH_ENRICHMENT_TRIGGER_KINDS,
                    },
                ]
            },
            "trigger_hit_ids": {
                "type": "array",
                "items": {
                    "type": "string",
                    "pattern": "^H[0-9]{6}$",
                },
                "uniqueItems": True,
            },
            "candidate_changes": {
                "type": "array",
                "items": candidate_change_schema,
            },
            "input_projection_sha256": {
                "type": "string",
                "pattern": "^[0-9a-f]{64}$",
            },
            "result_snapshot": review_result_snapshot_schema,
            "result_projection_sha256": {
                "type": "string",
                "pattern": "^[0-9a-f]{64}$",
            },
            "previous_event_sha256": {
                "oneOf": [
                    {"type": "null"},
                    {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                ]
            },
            "event_sha256": {
                "type": "string",
                "pattern": "^[0-9a-f]{64}$",
            },
        },
        "additionalProperties": False,
    }
    family_relation_schema = {
        "type": "object",
        "required": [
            "relation",
            "target_kind",
            "target_id",
            "evidence_ids",
            "rationale",
        ],
        "properties": {
            "relation": {"type": "string", "enum": FAMILY_RELATIONS},
            "target_kind": {
                "type": "string",
                "enum": ["CANDIDATE", "SEMANTIC_FAMILY"],
            },
            "target_id": {
                "type": "string",
                "pattern": "^(?:B[0-9]{4}|F[0-9]{4})$",
            },
            "evidence_ids": {
                "type": "array",
                "items": {
                    "type": "string",
                    "pattern": "^E[0-9]{6}$",
                },
                "uniqueItems": True,
                "minItems": 1,
            },
            "rationale": {"type": "string", "minLength": 1},
        },
        "additionalProperties": False,
    }
    proof_obligation_schema = {
        "type": "object",
        "required": ["obligation_id", "status", "evidence_ids", "argument"],
        "properties": {
            "obligation_id": {"type": "string", "minLength": 1},
            "status": {
                "type": "string",
                "enum": ["PROVED", "NOT_APPLICABLE", "SOURCE_INSUFFICIENT"],
            },
            "evidence_ids": {
                "type": "array",
                "items": {
                    "type": "string",
                    "pattern": "^E[0-9]{6}$",
                },
                "uniqueItems": True,
            },
            "argument": {"type": "string", "minLength": 1},
        },
        "additionalProperties": False,
    }
    proof_packet_schema = {
        "type": "object",
        "required": [
            "proof_case",
            "obligations",
            "nearest_candidate_ids",
            "non_preservation_witness",
            "reopen_trigger",
        ],
        "properties": {
            "proof_case": {"type": "string", "enum": PROOF_CASES},
            "obligations": {
                "type": "array",
                "items": proof_obligation_schema,
                "minItems": 1,
            },
            "nearest_candidate_ids": {
                "type": "array",
                "items": {
                    "type": "string",
                    "pattern": "^B[0-9]{4}$",
                },
                "uniqueItems": True,
            },
            "non_preservation_witness": {"type": ["string", "null"]},
            "reopen_trigger": {"type": ["string", "null"]},
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
            "proof_packets",
            "hostile_review_required",
        ],
        "properties": {
            "candidate_id": {"type": "string", "pattern": "^B[0-9]{4}$"},
            "catalog_action": {"type": "string", "enum": CATALOG_ACTIONS},
            "semantic_role": {"type": "string", "enum": SEMANTIC_ROLES},
            "semantic_subtype": {
                "oneOf": [
                    {"type": "null"},
                    {"type": "string", "enum": SEMANTIC_SUBTYPES},
                ]
            },
            "family_action": {"type": "string", "enum": FAMILY_ACTIONS},
            "family_relations": {
                "type": "array",
                "items": family_relation_schema,
            },
            "rationale": {"type": "string", "minLength": 1},
            "evidence_ids": {
                "type": "array",
                "items": {
                    "type": "string",
                    "pattern": "^E[0-9]{6}$",
                },
                "uniqueItems": True,
                "minItems": 1,
            },
            "proof_packets": {
                "type": "array",
                "items": proof_packet_schema,
                "minItems": 1,
            },
            "hostile_review_required": {"type": "boolean"},
        },
        "additionalProperties": False,
    }
    coverage_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Stage 19+ coverage join row",
        "type": "object",
        "required": [
            "coverage_id",
            "candidate_ids",
            "existing_t_ids",
            "proposed_t_ids",
            "source_unit_ids",
            "image_paths",
            "evidence_ids",
            "reconciliation_result",
            "rationale",
        ],
        "properties": {
            "coverage_id": {"type": "string", "pattern": "^C[0-9]{4}$"},
            "candidate_ids": {
                "type": "array",
                "items": {"type": "string", "pattern": "^B[0-9]{4}$"},
                "uniqueItems": True,
            },
            "existing_t_ids": {
                "type": "array",
                "items": {
                    "type": "string",
                    "pattern": "^T(?:0[1-9]|[1-3][0-9]|4[0-5])$",
                },
                "uniqueItems": True,
            },
            "proposed_t_ids": {
                "type": "array",
                "items": {"type": "string", "pattern": "^T[0-9]{2,}$"},
                "uniqueItems": True,
            },
            "source_unit_ids": {
                "type": "array",
                "items": {"type": "string", "pattern": "^U[0-9]{6}$"},
                "uniqueItems": True,
            },
            "image_paths": _string_array(),
            "evidence_ids": {
                "type": "array",
                "items": {
                    "type": "string",
                    "pattern": "^E[0-9]{6}$",
                },
                "uniqueItems": True,
            },
            "reconciliation_result": {
                "type": "string",
                "enum": [
                    "REDISCOVERED",
                    "CORRECTION_REQUIRED",
                    "PROPOSED_ADDITION",
                    "NO_SEPARATE_ENTRY",
                    "DUPLICATE_OR_ALIAS",
                    "INSUFFICIENT_BOOK_EVIDENCE",
                    "UNMATCHED_EXISTING_OBLIGATION",
                ],
            },
            "rationale": {"type": "string", "minLength": 1},
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
                "items": candidate_schema(
                    "^W[0-9]{4}$",
                    "^WE[0-9]{6}$",
                    "^WG[0-9]{6}$",
                ),
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
        "blind/review-history-event.schema.json": review_history_schema,
        "blind/search-rounds.schema.json": search_schema,
        "blind/worker-output.schema.json": worker_output_schema,
        "reconciliation/classification-row.schema.json": classification_schema,
        "reconciliation/coverage-row.schema.json": coverage_schema,
    }


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def review_input_projection(
    event: dict[str, Any],
    unit_by_id: dict[str, dict[str, Any]],
    asset_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Return the immutable corpus/input projection bound by a review event."""
    return {
        "schema_version": 1,
        "review_id": event["review_id"],
        "epoch": event["epoch"],
        "stage": event["stage"],
        "mode": event["mode"],
        "reviewer": event["reviewer"],
        "source_paths": event["source_paths"],
        "prior_search_round_count": event["prior_search_round_count"],
        "prior_search_rounds_sha256": event[
            "prior_search_rounds_sha256"
        ],
        "previous_path_result_sha256": event[
            "previous_path_result_sha256"
        ],
        "trigger_search_kind": event["trigger_search_kind"],
        "trigger_hit_ids": event["trigger_hit_ids"],
        "source_units": [
            {
                "source_unit_id": unit_id,
                "path": unit_by_id[unit_id]["path"],
                "sha256": unit_by_id[unit_id]["sha256"],
            }
            for unit_id in event["source_unit_ids"]
        ],
        "assets": [
            {
                "asset_id": asset_id,
                "physical_path": asset_by_id[asset_id]["physical_path"],
                "assignment_path": asset_by_id[asset_id]["assignment_path"],
                "sha256": asset_by_id[asset_id]["sha256"],
            }
            for asset_id in event["asset_ids"]
        ],
    }


def review_result_projection(
    event: dict[str, Any],
    reading_by_id: dict[str, dict[str, Any]],
    asset_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Return the exact current result projection for a review event."""
    return {
        "schema_version": 1,
        "source_path": event["source_paths"][0],
        "reading_results": [
            {
                field: reading_by_id[unit_id][field]
                for field in READING_REVIEW_RESULT_FIELDS
            }
            for unit_id in event["source_unit_ids"]
        ],
        "asset_results": [
            {
                field: asset_by_id[asset_id][field]
                for field in ASSET_REVIEW_RESULT_FIELDS
            }
            for asset_id in event["asset_ids"]
        ],
    }


def review_event_sha256(event: dict[str, Any]) -> str:
    """Hash one closed history event, excluding only its own digest field."""
    return canonical_sha256(
        {
            field: event[field]
            for field in REVIEW_HISTORY_FIELDS
            if field != "event_sha256"
        }
    )


def close_candidate_change(
    action: str,
    after_candidate: dict[str, Any],
    before_candidate: dict[str, Any] | None = None,
    previous_candidate_result_sha256: str | None = None,
) -> dict[str, Any]:
    """Close one candidate CREATE/UPDATE version record."""
    return {
        "action": action,
        "candidate_id": after_candidate["id"],
        "previous_candidate_result_sha256": (
            previous_candidate_result_sha256
        ),
        "before_candidate": before_candidate,
        "before_candidate_sha256": (
            canonical_sha256(before_candidate)
            if before_candidate is not None
            else None
        ),
        "after_candidate": after_candidate,
        "after_candidate_sha256": canonical_sha256(after_candidate),
    }


def close_review_event(
    core: dict[str, Any],
    unit_by_id: dict[str, dict[str, Any]],
    reading_by_id: dict[str, dict[str, Any]],
    asset_by_id: dict[str, dict[str, Any]],
    previous_event_sha256: str | None,
    prior_search_rounds: list[dict[str, Any]],
) -> dict[str, Any]:
    """Close a new append-only review event with canonical projections/hashes."""
    event = {
        "review_id": core["review_id"],
        "epoch": core["epoch"],
        "stage": core["stage"],
        "mode": core["mode"],
        "reviewer": core["reviewer"],
        "source_paths": list(core["source_paths"]),
        "source_unit_ids": list(core["source_unit_ids"]),
        "asset_ids": list(core["asset_ids"]),
        "prior_search_round_count": len(prior_search_rounds),
        "prior_search_rounds_sha256": canonical_sha256(prior_search_rounds),
        "previous_path_result_sha256": core.get(
            "previous_path_result_sha256"
        ),
        "trigger_search_kind": core.get("trigger_search_kind"),
        "trigger_hit_ids": list(core.get("trigger_hit_ids", [])),
        "candidate_changes": list(core.get("candidate_changes", [])),
        "input_projection_sha256": "",
        "result_snapshot": {},
        "result_projection_sha256": "",
        "previous_event_sha256": previous_event_sha256,
        "event_sha256": "",
    }
    event["input_projection_sha256"] = canonical_sha256(
        review_input_projection(event, unit_by_id, asset_by_id)
    )
    event["result_snapshot"] = review_result_projection(
        event, reading_by_id, asset_by_id
    )
    event["result_projection_sha256"] = canonical_sha256(
        event["result_snapshot"]
    )
    event["event_sha256"] = review_event_sha256(event)
    return event
