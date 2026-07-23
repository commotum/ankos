#!/usr/bin/env python3
"""Preview/apply a blind-worker merge or typed coordinator proposal."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import sys
from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

import build_worker_bundle
import audit_transaction
import validate_audit
from audit_contract import (
    ASSET_HEADER,
    CANDIDATE_FIELDS,
    CROSS_REFERENCE_HEADER,
    FINGERPRINT_FIELDS,
    GOAL_DIR,
    READING_HEADER,
    REVIEW_HISTORY_FIELDS,
    close_candidate_change,
    close_path_change,
    close_review_event,
    close_route_change,
    close_search_change,
)


READING_NAME = "reading-ledger.csv"
CANDIDATE_NAME = "candidate-ledger.jsonl"
ROUTE_NAME = "cross-reference-ledger.csv"
ASSET_NAME = "asset-ledger.csv"
SEARCH_NAME = "search-rounds.json"
REVIEW_HISTORY_NAME = "review-history.jsonl"
MANIFEST_NAME = "corpus-manifest.json"
UNITS_NAME = "source-units.jsonl"
GUARDRAILS_NAME = "guardrails.json"

WRITE_NAMES = (
    CANDIDATE_NAME,
    ROUTE_NAME,
    READING_NAME,
    ASSET_NAME,
    SEARCH_NAME,
    REVIEW_HISTORY_NAME,
)
SNAPSHOT_NAMES = (
    MANIFEST_NAME,
    UNITS_NAME,
    READING_NAME,
    CANDIDATE_NAME,
    ROUTE_NAME,
    ASSET_NAME,
    SEARCH_NAME,
    REVIEW_HISTORY_NAME,
    GUARDRAILS_NAME,
)


class MergeError(ValueError):
    """The worker output cannot be merged without weakening an invariant."""


def _plan_validation_token(
    original_bytes: Mapping[str, bytes],
    original_modes: Mapping[str, int],
    proposed_bytes: Mapping[str, bytes],
) -> str:
    """Bind every immutable plan-state byte and mode to one digest."""

    expected_original = set(SNAPSHOT_NAMES)
    expected_proposed = set(WRITE_NAMES)
    if (
        set(original_bytes) != expected_original
        or set(original_modes) != expected_original
        or set(proposed_bytes) != expected_proposed
    ):
        raise MergeError(
            "prepared plan state maps differ from the closed artifact contract"
        )

    digest = hashlib.sha256()

    def add(payload: bytes) -> None:
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)

    add(b"goal-4-validated-plan-v1")
    for label, names, values in (
        (b"original-bytes", SNAPSHOT_NAMES, original_bytes),
        (b"proposed-bytes", WRITE_NAMES, proposed_bytes),
    ):
        add(label)
        for name in names:
            value = values[name]
            if not isinstance(value, bytes):
                raise MergeError(
                    f"prepared plan byte payload is invalid: {name}"
                )
            add(name.encode("utf-8"))
            add(value)
    add(b"original-modes")
    for name in SNAPSHOT_NAMES:
        mode = original_modes[name]
        if (
            isinstance(mode, bool)
            or not isinstance(mode, int)
            or mode < 0
            or mode > 0o777
        ):
            raise MergeError(f"prepared plan mode is invalid: {name}")
        add(name.encode("utf-8"))
        add(mode.to_bytes(2, "big"))
    return digest.hexdigest()


def _freeze_plan_state(
    original_bytes: Mapping[str, bytes],
    original_modes: Mapping[str, int],
    proposed_bytes: Mapping[str, bytes],
) -> tuple[
    Mapping[str, bytes],
    Mapping[str, int],
    Mapping[str, bytes],
    str,
]:
    frozen_original_bytes = MappingProxyType(dict(original_bytes))
    frozen_original_modes = MappingProxyType(dict(original_modes))
    frozen_proposed_bytes = MappingProxyType(dict(proposed_bytes))
    validation_token = _plan_validation_token(
        frozen_original_bytes,
        frozen_original_modes,
        frozen_proposed_bytes,
    )
    return (
        frozen_original_bytes,
        frozen_original_modes,
        frozen_proposed_bytes,
        validation_token,
    )


@dataclass(frozen=True)
class MergePlan:
    bundle: Path
    goal_dir: Path
    worker_id: str
    stage: int
    discovery_epoch: int
    review_ids: tuple[str, ...]
    review_mode: str
    source_paths: tuple[str, ...]
    candidate_ids: dict[str, str]
    route_ids: dict[str, str]
    evidence_ids: dict[str, str]
    evidence_group_ids: dict[str, str]
    reading_update_count: int
    asset_update_count: int
    worker_uncertainties: tuple[str, ...]
    original_bytes: Mapping[str, bytes]
    original_modes: Mapping[str, int]
    proposed_bytes: Mapping[str, bytes]
    validation_token: str

    def preview(self) -> dict[str, Any]:
        return {
            "worker_id": self.worker_id,
            "bundle": str(self.bundle),
            "goal_dir": str(self.goal_dir),
            "stage": self.stage,
            "discovery_epoch": self.discovery_epoch,
            "review_ids": list(self.review_ids),
            "review_mode": self.review_mode,
            "source_paths": list(self.source_paths),
            "mappings": {
                "candidates": self.candidate_ids,
                "routes": self.route_ids,
                "evidence": self.evidence_ids,
                "evidence_groups": self.evidence_group_ids,
            },
            "changes": {
                "reading_updates": self.reading_update_count,
                "asset_updates": self.asset_update_count,
                "candidate_appends": len(self.candidate_ids),
                "route_appends": len(self.route_ids),
                "review_event_appends": len(self.review_ids),
            },
            "worker_uncertainties": list(self.worker_uncertainties),
            "search_ledger_preserved": (
                self.proposed_bytes[SEARCH_NAME]
                == self.original_bytes[SEARCH_NAME]
            ),
            "search_rounds_preserved": True,
            "search_vocabulary_preserved": True,
            "search_fixed_point_cleared": (
                self.review_mode == "REOPEN"
            ),
            "search_ledger_sha256": hashlib.sha256(
                self.proposed_bytes[SEARCH_NAME]
            ).hexdigest(),
        }


@dataclass(frozen=True)
class SearchAppendPlan:
    proposal: Path
    goal_dir: Path
    coordinator_id: str
    epoch: int
    source_paths: tuple[str, ...]
    search_round_id: str
    trigger_hit_ids: tuple[str, ...]
    review_ids: tuple[str, ...]
    reading_update_count: int
    asset_update_count: int
    candidate_update_count: int
    candidate_append_count: int
    route_append_count: int
    original_bytes: Mapping[str, bytes]
    original_modes: Mapping[str, int]
    proposed_bytes: Mapping[str, bytes]
    validation_token: str

    def preview(self) -> dict[str, Any]:
        before_fixed_point = json.loads(
            self.original_bytes[SEARCH_NAME]
        ).get("fixed_point")
        after_fixed_point = json.loads(
            self.proposed_bytes[SEARCH_NAME]
        ).get("fixed_point")
        return {
            "proposal_kind": "SEARCH_APPEND",
            "proposal": str(self.proposal),
            "goal_dir": str(self.goal_dir),
            "coordinator_id": self.coordinator_id,
            "epoch": self.epoch,
            "source_paths": list(self.source_paths),
            "search_round_id": self.search_round_id,
            "trigger_hit_ids": list(self.trigger_hit_ids),
            "review_ids": list(self.review_ids),
            "changes": {
                "reading_updates": self.reading_update_count,
                "asset_updates": self.asset_update_count,
                "candidate_updates": self.candidate_update_count,
                "candidate_appends": self.candidate_append_count,
                "route_appends": self.route_append_count,
                "search_round_appends": 1,
                "review_event_appends": len(self.review_ids),
            },
            "search_ledger_preserved": False,
            "search_fixed_point_cleared": (
                before_fixed_point is not None
                and after_fixed_point is None
            ),
            "search_fixed_point_established": (
                before_fixed_point is None
                and after_fixed_point is not None
            ),
            "search_ledger_sha256": hashlib.sha256(
                self.proposed_bytes[SEARCH_NAME]
            ).hexdigest(),
            "review_history_sha256": hashlib.sha256(
                self.proposed_bytes[REVIEW_HISTORY_NAME]
            ).hexdigest(),
        }


@dataclass(frozen=True)
class RouteResolutionPlan:
    proposal: Path
    goal_dir: Path
    coordinator_id: str
    epoch: int
    stage: int
    source_paths: tuple[str, ...]
    review_ids: tuple[str, ...]
    route_update_count: int
    original_bytes: Mapping[str, bytes]
    original_modes: Mapping[str, int]
    proposed_bytes: Mapping[str, bytes]
    validation_token: str

    def preview(self) -> dict[str, Any]:
        return {
            "proposal_kind": "ROUTE_RESOLUTION",
            "proposal": str(self.proposal),
            "goal_dir": str(self.goal_dir),
            "coordinator_id": self.coordinator_id,
            "epoch": self.epoch,
            "stage": self.stage,
            "source_paths": list(self.source_paths),
            "review_ids": list(self.review_ids),
            "changes": {
                "route_updates": self.route_update_count,
                "review_event_appends": 1,
            },
        }


@dataclass(frozen=True)
class CandidateRevisionPlan:
    proposal: Path
    goal_dir: Path
    coordinator_id: str
    epoch: int
    source_paths: tuple[str, ...]
    review_ids: tuple[str, ...]
    candidate_update_count: int
    candidate_append_count: int
    reading_update_count: int
    asset_update_count: int
    original_bytes: Mapping[str, bytes]
    original_modes: Mapping[str, int]
    proposed_bytes: Mapping[str, bytes]
    validation_token: str

    def preview(self) -> dict[str, Any]:
        return {
            "proposal_kind": "CANDIDATE_REVISION",
            "proposal": str(self.proposal),
            "goal_dir": str(self.goal_dir),
            "coordinator_id": self.coordinator_id,
            "epoch": self.epoch,
            "stage": 18,
            "source_paths": list(self.source_paths),
            "review_ids": list(self.review_ids),
            "changes": {
                "candidate_updates": self.candidate_update_count,
                "candidate_appends": self.candidate_append_count,
                "reading_updates": self.reading_update_count,
                "asset_updates": self.asset_update_count,
                "review_event_appends": 1,
            },
        }


Plan = (
    MergePlan
    | SearchAppendPlan
    | RouteResolutionPlan
    | CandidateRevisionPlan
)


SEARCH_APPEND_PROPOSAL_FIELDS = (
    "schema_version",
    "proposal_kind",
    "coordinator_id",
    "epoch",
    "source_paths",
    "base_artifact_sha256",
    "reading_updates",
    "asset_updates",
    "candidate_updates",
    "route_appends",
    "proposed_search",
)
ROUTE_RESOLUTION_PROPOSAL_FIELDS = (
    "schema_version",
    "proposal_kind",
    "coordinator_id",
    "epoch",
    "base_artifact_sha256",
    "route_updates",
)
CANDIDATE_REVISION_PROPOSAL_FIELDS = (
    "schema_version",
    "proposal_kind",
    "coordinator_id",
    "epoch",
    "base_artifact_sha256",
    "candidate_updates",
    "reading_updates",
    "asset_updates",
)
READING_ENRICHMENT_SCALARS = {
    "review_disposition",
    "source_status",
    "uncertainty",
    "evidence_statement",
}
READING_ENRICHMENT_ARRAYS = {
    "secondary_roles",
    "candidate_ids",
    "route_ids",
}
ASSET_ENRICHMENT_ARRAYS = {"candidate_ids", "route_ids"}
CANDIDATE_ENRICHMENT_IMMUTABLE = {
    "id",
    "record_status",
    "provisional_name",
    "discovery_stage",
    "discovery_anchor",
    "evidence_reassignments",
}


def _search_append_proposal_schema() -> dict[str, Any]:
    digest_properties = {
        name: {"type": "string", "pattern": "^[0-9a-f]{64}$"}
        for name in WRITE_NAMES
    }
    string_row = {"type": "string"}
    return {
        "type": "object",
        "required": list(SEARCH_APPEND_PROPOSAL_FIELDS),
        "properties": {
            "schema_version": {"const": 1},
            "proposal_kind": {"const": "SEARCH_APPEND"},
            "coordinator_id": {"type": "string", "minLength": 1},
            "epoch": {"type": "integer", "minimum": 1},
            "source_paths": {
                "type": "array",
                "items": {"type": "string", "minLength": 1},
                "uniqueItems": True,
            },
            "base_artifact_sha256": {
                "type": "object",
                "required": list(WRITE_NAMES),
                "properties": digest_properties,
                "additionalProperties": False,
            },
            "reading_updates": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": READING_HEADER,
                    "properties": {
                        field: string_row for field in READING_HEADER
                    },
                    "additionalProperties": False,
                },
            },
            "asset_updates": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ASSET_HEADER,
                    "properties": {
                        field: string_row for field in ASSET_HEADER
                    },
                    "additionalProperties": False,
                },
            },
            "candidate_updates": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": CANDIDATE_FIELDS,
                    "properties": {
                        field: {} for field in CANDIDATE_FIELDS
                    },
                    "additionalProperties": False,
                },
            },
            "route_appends": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": CROSS_REFERENCE_HEADER,
                    "properties": {
                        field: string_row
                        for field in CROSS_REFERENCE_HEADER
                    },
                    "additionalProperties": False,
                },
            },
            "proposed_search": {"type": "object"},
        },
        "additionalProperties": False,
    }


def _coordinator_base_properties(kind: str) -> dict[str, Any]:
    return {
        "schema_version": {"const": 1},
        "proposal_kind": {"const": kind},
        "coordinator_id": {"type": "string", "minLength": 1},
        "epoch": {"type": "integer", "minimum": 1},
        "base_artifact_sha256": {
            "type": "object",
            "required": list(WRITE_NAMES),
            "properties": {
                name: {
                    "type": "string",
                    "pattern": "^[0-9a-f]{64}$",
                }
                for name in WRITE_NAMES
            },
            "additionalProperties": False,
        },
    }


def _route_resolution_proposal_schema() -> dict[str, Any]:
    properties = _coordinator_base_properties("ROUTE_RESOLUTION")
    properties["route_updates"] = {
        "type": "array",
        "minItems": 1,
        "items": {
            "type": "object",
            "required": CROSS_REFERENCE_HEADER,
            "properties": {
                field: {"type": "string"}
                for field in CROSS_REFERENCE_HEADER
            },
            "additionalProperties": False,
        },
    }
    return {
        "type": "object",
        "required": list(ROUTE_RESOLUTION_PROPOSAL_FIELDS),
        "properties": properties,
        "additionalProperties": False,
    }


def _candidate_revision_proposal_schema() -> dict[str, Any]:
    properties = _coordinator_base_properties("CANDIDATE_REVISION")
    properties.update(
        {
            "candidate_updates": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": CANDIDATE_FIELDS,
                    "properties": {
                        field: {} for field in CANDIDATE_FIELDS
                    },
                    "additionalProperties": False,
                },
            },
            "reading_updates": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": READING_HEADER,
                    "properties": {
                        field: {"type": "string"}
                        for field in READING_HEADER
                    },
                    "additionalProperties": False,
                },
            },
            "asset_updates": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ASSET_HEADER,
                    "properties": {
                        field: {"type": "string"}
                        for field in ASSET_HEADER
                    },
                    "additionalProperties": False,
                },
            },
        }
    )
    return {
        "type": "object",
        "required": list(CANDIDATE_REVISION_PROPOSAL_FIELDS),
        "properties": properties,
        "additionalProperties": False,
    }


def _read_csv(path: Path, header: list[str]) -> list[dict[str, str]]:
    try:
        payload = path.read_bytes()
    except OSError as exc:
        raise MergeError(f"cannot read {path}: {exc}") from exc
    return _read_csv_bytes(payload, path.name, header)


def _read_csv_bytes(
    payload: bytes,
    label: str,
    header: list[str],
) -> list[dict[str, str]]:
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise MergeError(f"{label} is not UTF-8") from exc
    reader = csv.DictReader(io.StringIO(text, newline=""))
    if reader.fieldnames != header:
        raise MergeError(f"{label} header mismatch: {reader.fieldnames!r}")
    rows = list(reader)
    if any(None in row for row in rows):
        raise MergeError(f"{label} contains an over-wide row")
    return rows


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    try:
        return validate_audit.load_jsonl(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise MergeError(str(exc)) from exc


def _json_array(value: object, label: str) -> list[str]:
    try:
        result = json.loads(value) if isinstance(value, str) else None
    except json.JSONDecodeError as exc:
        raise MergeError(f"{label} is not valid JSON") from exc
    if (
        not isinstance(result, list)
        or not all(isinstance(item, str) for item in result)
        or len(result) != len(set(result))
    ):
        raise MergeError(f"{label} must be a JSON array of unique strings")
    return result


def _map_id(value: object, mapping: dict[str, str], label: str) -> str:
    if not isinstance(value, str) or value not in mapping:
        raise MergeError(f"{label} contains a nonlocal or unmapped reference: {value!r}")
    return mapping[value]


def _map_id_list(
    value: object,
    mapping: dict[str, str],
    label: str,
) -> list[str]:
    if (
        not isinstance(value, list)
        or not all(isinstance(item, str) for item in value)
        or len(value) != len(set(value))
    ):
        raise MergeError(f"{label} must be an array of unique local IDs")
    return [_map_id(item, mapping, label) for item in value]


def _map_csv_id_array(
    value: object,
    mapping: dict[str, str],
    label: str,
    *,
    original_value: object,
    reopened: bool,
) -> str:
    values = _json_array(value, label)
    original_values = _json_array(original_value, f"{label} authoritative input")
    retained = [item for item in values if item not in mapping]
    if reopened:
        if retained != original_values:
            raise MergeError(
                f"{label} reopened pass must retain existing global links "
                "exactly and in order"
            )
    elif retained:
        raise MergeError(
            f"{label} initial pass contains nonlocal or pre-existing links: "
            f"{retained}"
        )
    mapped = [
        mapping[item] if item in mapping else item
        for item in values
    ]
    return json.dumps(mapped, ensure_ascii=False, separators=(",", ":"))


def _sequence(
    values: list[str],
    prefix: str,
    width: int,
    label: str,
) -> int:
    seen: set[str] = set()
    for value in values:
        if value in seen:
            raise MergeError(f"{label} ID collision: {value}")
        seen.add(value)
    expected = [
        f"{prefix}{index:0{width}d}" for index in range(1, len(values) + 1)
    ]
    if values != expected:
        raise MergeError(f"{label} IDs are not a complete append-only sequence")
    return len(values)


def _allocate_mapping(
    local_values: list[str],
    existing_values: list[str],
    *,
    local_prefix: str,
    global_prefix: str,
    local_width: int,
    global_width: int,
    label: str,
) -> dict[str, str]:
    _sequence(local_values, local_prefix, local_width, f"worker {label}")
    first = _sequence(
        existing_values,
        global_prefix,
        global_width,
        f"global {label}",
    )
    if first + len(local_values) >= 10**global_width:
        raise MergeError(f"{label} ID space is exhausted")
    mapping = {
        local: f"{global_prefix}{first + offset:0{global_width}d}"
        for offset, local in enumerate(local_values, start=1)
    }
    collisions = set(mapping.values()) & set(existing_values)
    if collisions:
        raise MergeError(f"{label} ID collision: {sorted(collisions)}")
    return mapping


def _candidate_local_sequences(
    proposals: list[dict[str, Any]],
) -> tuple[list[str], list[str], list[str]]:
    candidate_ids: list[str] = []
    evidence_records: list[tuple[str, str]] = []
    evidence_group_ids: list[str] = []
    for index, candidate in enumerate(proposals):
        if not isinstance(candidate, dict):
            raise MergeError(f"candidate_proposals[{index}] is not an object")
        candidate_id = candidate.get("id")
        if not isinstance(candidate_id, str):
            raise MergeError(f"candidate_proposals[{index}] lacks a string ID")
        candidate_ids.append(candidate_id)
        evidence = candidate.get("source_evidence")
        if not isinstance(evidence, list):
            raise MergeError(f"candidate {candidate_id} source_evidence is not an array")
        for evidence_index, item in enumerate(evidence):
            if not isinstance(item, dict):
                raise MergeError(
                    f"candidate {candidate_id} evidence {evidence_index} is not an object"
                )
            evidence_id = item.get("evidence_id")
            group_id = item.get("evidence_group_id")
            if not isinstance(evidence_id, str) or not isinstance(group_id, str):
                raise MergeError(
                    f"candidate {candidate_id} has incomplete evidence identifiers"
                )
            evidence_records.append((evidence_id, group_id))

    # Candidate records group evidence by owner, but the frozen E/G allocation
    # traverses source anchors globally. Worker-local WE IDs encode that
    # traversal, so recover the flat order from the IDs before allocating.
    evidence_records.sort(key=lambda item: item[0])
    evidence_ids = [evidence_id for evidence_id, _ in evidence_records]
    _sequence(evidence_ids, "WE", 6, "worker evidence")
    seen_groups: set[str] = set()
    for _, group_id in evidence_records:
        if group_id not in seen_groups:
            seen_groups.add(group_id)
            evidence_group_ids.append(group_id)
    _sequence(
        evidence_group_ids,
        "WG",
        6,
        "worker evidence-group",
    )
    return candidate_ids, evidence_ids, evidence_group_ids


def _existing_evidence_sequences(
    candidates: list[dict[str, Any]],
) -> tuple[list[str], list[str]]:
    evidence_ids: list[str] = []
    group_first_evidence: dict[str, int] = {}
    for candidate in candidates:
        evidence = candidate.get("source_evidence")
        if not isinstance(evidence, list):
            raise MergeError(
                f"global candidate {candidate.get('id', '<unknown>')} has malformed evidence"
            )
        for item in evidence:
            if not isinstance(item, dict):
                raise MergeError("global candidate ledger has malformed evidence")
            evidence_id = item.get("evidence_id")
            group_id = item.get("evidence_group_id")
            if not isinstance(evidence_id, str) or not isinstance(group_id, str):
                raise MergeError("global candidate ledger has incomplete evidence IDs")
            evidence_ids.append(evidence_id)
            if (
                not evidence_id.startswith("E")
                or not evidence_id[1:].isdigit()
            ):
                raise MergeError(
                    f"global candidate ledger has invalid evidence ID {evidence_id}"
                )
            evidence_number = int(evidence_id[1:])
            group_first_evidence[group_id] = min(
                evidence_number,
                group_first_evidence.get(group_id, evidence_number),
            )
    if len(evidence_ids) != len(set(evidence_ids)):
        raise MergeError("global evidence ID collision")
    evidence_ids.sort(key=lambda value: int(value[1:]))
    group_ids = sorted(
        group_first_evidence,
        key=lambda value: group_first_evidence[value],
    )
    return evidence_ids, group_ids


def _require_list(value: object, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise MergeError(f"{label} is not an array")
    return value


def _rewrite_candidate(
    source: dict[str, Any],
    candidate_ids: dict[str, str],
    route_ids: dict[str, str],
    evidence_ids: dict[str, str],
    evidence_group_ids: dict[str, str],
) -> dict[str, Any]:
    candidate = deepcopy(source)
    local_id = source.get("id", "<unknown>")
    candidate["id"] = _map_id(source.get("id"), candidate_ids, "candidate.id")

    mapped_evidence: list[dict[str, Any]] = []
    for item in _require_list(
        candidate.get("source_evidence"),
        f"candidate {local_id}.source_evidence",
    ):
        if not isinstance(item, dict):
            raise MergeError(f"candidate {local_id} has non-object evidence")
        mapped = deepcopy(item)
        mapped["evidence_id"] = _map_id(
            item.get("evidence_id"),
            evidence_ids,
            f"candidate {local_id}.source_evidence.evidence_id",
        )
        mapped["evidence_group_id"] = _map_id(
            item.get("evidence_group_id"),
            evidence_group_ids,
            f"candidate {local_id}.source_evidence.evidence_group_id",
        )
        mapped_evidence.append(mapped)
    candidate["source_evidence"] = mapped_evidence

    fingerprint = candidate.get("fingerprint")
    if not isinstance(fingerprint, dict) or set(fingerprint) != set(
        FINGERPRINT_FIELDS
    ):
        raise MergeError(f"candidate {local_id} has an incomplete fingerprint")
    mapped_fingerprint: dict[str, Any] = {}
    for field in FINGERPRINT_FIELDS:
        value = deepcopy(fingerprint[field])
        if not isinstance(value, dict):
            raise MergeError(f"candidate {local_id}.{field} is not an object")
        value["evidence_ids"] = _map_id_list(
            value.get("evidence_ids"),
            evidence_ids,
            f"candidate {local_id}.{field}.evidence_ids",
        )
        mapped_fingerprint[field] = value
    candidate["fingerprint"] = mapped_fingerprint

    field_support = candidate.get("field_support")
    if not isinstance(field_support, dict) or set(field_support) != set(
        FINGERPRINT_FIELDS
    ):
        raise MergeError(f"candidate {local_id} has incomplete field_support")
    candidate["field_support"] = {
        field: field_support[field] for field in FINGERPRINT_FIELDS
    }

    for collection_name in ("parameters", "variants"):
        mapped_collection: list[dict[str, Any]] = []
        for item in _require_list(
            candidate.get(collection_name),
            f"candidate {local_id}.{collection_name}",
        ):
            if not isinstance(item, dict):
                raise MergeError(
                    f"candidate {local_id}.{collection_name} has a non-object item"
                )
            mapped = deepcopy(item)
            mapped["evidence_ids"] = _map_id_list(
                item.get("evidence_ids"),
                evidence_ids,
                f"candidate {local_id}.{collection_name}.evidence_ids",
            )
            mapped_collection.append(mapped)
        candidate[collection_name] = mapped_collection

    mapped_relations: list[dict[str, Any]] = []
    for item in _require_list(
        candidate.get("related_candidate_ids"),
        f"candidate {local_id}.related_candidate_ids",
    ):
        if not isinstance(item, dict):
            raise MergeError(f"candidate {local_id} has a non-object relation")
        mapped = deepcopy(item)
        mapped["candidate_id"] = _map_id(
            item.get("candidate_id"),
            candidate_ids,
            f"candidate {local_id}.related_candidate_ids.candidate_id",
        )
        mapped["evidence_ids"] = _map_id_list(
            item.get("evidence_ids"),
            evidence_ids,
            f"candidate {local_id}.related_candidate_ids.evidence_ids",
        )
        mapped_relations.append(mapped)
    candidate["related_candidate_ids"] = mapped_relations

    candidate["cross_reference_ids"] = _map_id_list(
        candidate.get("cross_reference_ids"),
        route_ids,
        f"candidate {local_id}.cross_reference_ids",
    )

    mapped_reassignments: list[dict[str, Any]] = []
    for item in _require_list(
        candidate.get("evidence_reassignments"),
        f"candidate {local_id}.evidence_reassignments",
    ):
        if not isinstance(item, dict):
            raise MergeError(
                f"candidate {local_id} has a non-object evidence reassignment"
            )
        mapped = deepcopy(item)
        mapped["from_evidence_id"] = _map_id(
            item.get("from_evidence_id"),
            evidence_ids,
            f"candidate {local_id}.evidence_reassignments.from_evidence_id",
        )
        mapped_targets: list[dict[str, str]] = []
        for target in _require_list(
            item.get("targets"),
            f"candidate {local_id}.evidence_reassignments.targets",
        ):
            if not isinstance(target, dict):
                raise MergeError(
                    f"candidate {local_id} has a non-object reassignment target"
                )
            mapped_targets.append(
                {
                    "candidate_id": _map_id(
                        target.get("candidate_id"),
                        candidate_ids,
                        f"candidate {local_id} reassignment candidate_id",
                    ),
                    "evidence_id": _map_id(
                        target.get("evidence_id"),
                        evidence_ids,
                        f"candidate {local_id} reassignment evidence_id",
                    ),
                }
            )
        mapped["targets"] = mapped_targets
        mapped_reassignments.append(mapped)
    candidate["evidence_reassignments"] = mapped_reassignments

    if set(candidate) != set(CANDIDATE_FIELDS):
        raise MergeError(f"candidate {local_id} fields differ from the global schema")
    return {field: candidate[field] for field in CANDIDATE_FIELDS}


def _candidate_anchor_path(
    candidate: dict[str, Any],
    unit_by_id: dict[str, dict[str, Any]],
    asset_by_physical_path: dict[str, dict[str, str]],
) -> str:
    """Resolve a blind-worker candidate's owning review path."""
    candidate_id = candidate.get("id", "<unknown>")
    anchor = candidate.get("discovery_anchor")
    if not isinstance(anchor, dict):
        raise MergeError(f"candidate {candidate_id} has no discovery anchor")
    kind = anchor.get("kind")
    anchor_id = anchor.get("id")
    if kind == "SOURCE_UNIT" and isinstance(anchor_id, str):
        source_unit = unit_by_id.get(anchor_id)
        if source_unit is not None and isinstance(source_unit.get("path"), str):
            return source_unit["path"]
    elif kind == "IMAGE" and isinstance(anchor_id, str):
        asset = asset_by_physical_path.get(anchor_id)
        if asset is not None and isinstance(asset.get("assignment_path"), str):
            return asset["assignment_path"]
    elif kind == "SEARCH_HIT":
        raise MergeError(
            f"blind worker candidate {candidate_id} cannot use a search-hit "
            "discovery anchor"
        )
    raise MergeError(
        f"candidate {candidate_id} discovery anchor does not resolve to "
        "an assigned source path"
    )


def _provenance_anchor_path(
    anchor: object,
    *,
    unit_by_id: dict[str, dict[str, Any]],
    asset_by_physical_path: dict[str, dict[str, str]],
    search_hit_paths: dict[str, str],
) -> str | None:
    if not isinstance(anchor, dict):
        return None
    anchor_id = anchor.get("id")
    if not isinstance(anchor_id, str):
        return None
    if anchor.get("kind") == "SOURCE_UNIT":
        unit = unit_by_id.get(anchor_id)
        return unit.get("path") if isinstance(unit, dict) else None
    if anchor.get("kind") == "IMAGE":
        asset = asset_by_physical_path.get(anchor_id)
        return (
            asset.get("assignment_path")
            if isinstance(asset, dict)
            else None
        )
    if anchor.get("kind") == "SEARCH_HIT":
        return search_hit_paths.get(anchor_id)
    return None


def _replace_rows(
    rows: list[dict[str, str]],
    updates: list[dict[str, str]],
    *,
    id_field: str,
    assigned_ids: set[str],
    candidate_ids: dict[str, str],
    route_ids: dict[str, str],
    label: str,
    reopened: bool,
    expected_review_epoch: int,
) -> list[dict[str, str]]:
    original_by_id = {row[id_field]: row for row in rows}
    by_id: dict[str, dict[str, str]] = {}
    for update in updates:
        identifier = update.get(id_field)
        if not identifier:
            raise MergeError(f"{label} update lacks {id_field}")
        if identifier in by_id:
            raise MergeError(f"{label} update collision: {identifier}")
        if identifier not in assigned_ids:
            raise MergeError(f"{label} update is outside the bundle: {identifier}")
        if update.get("review_epoch") != str(expected_review_epoch):
            raise MergeError(
                f"{label} {identifier}.review_epoch differs from bundle "
                f"epoch {expected_review_epoch}"
            )
        mapped = dict(update)
        original = original_by_id[identifier]
        mapped["candidate_ids"] = _map_csv_id_array(
            update.get("candidate_ids"),
            candidate_ids,
            f"{label} {identifier}.candidate_ids",
            original_value=original.get("candidate_ids"),
            reopened=reopened,
        )
        mapped["route_ids"] = _map_csv_id_array(
            update.get("route_ids"),
            route_ids,
            f"{label} {identifier}.route_ids",
            original_value=original.get("route_ids"),
            reopened=reopened,
        )
        by_id[identifier] = mapped
    if set(by_id) != assigned_ids:
        missing = sorted(assigned_ids - set(by_id))
        raise MergeError(f"{label} output has a partial mapping; missing={missing}")
    return [by_id.get(row[id_field], row) for row in rows]


def _append_jsonl(original: bytes, rows: list[dict[str, Any]]) -> bytes:
    if not rows:
        return original
    separator = b"" if not original or original.endswith(b"\n") else b"\n"
    additions = b"".join(
        (
            json.dumps(
                row,
                ensure_ascii=False,
                separators=(",", ":"),
            )
            + "\n"
        ).encode("utf-8")
        for row in rows
    )
    return original + separator + additions


def _append_csv(
    original: bytes,
    header: list[str],
    rows: list[dict[str, str]],
) -> bytes:
    if not rows:
        return original
    serialized = build_worker_bundle.csv_bytes(header, rows)
    _, body = serialized.split(b"\n", 1)
    separator = b"" if original.endswith(b"\n") else b"\n"
    return original + separator + body


def _load_output(payload: bytes) -> dict[str, Any]:
    try:
        output = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MergeError(f"cannot load worker output: {exc}") from exc
    if not isinstance(output, dict):
        raise MergeError("worker output is not an object")
    return output


def _read_jsonl_bytes(payload: bytes, label: str) -> list[dict[str, Any]]:
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise MergeError(f"{label} is not UTF-8") from exc
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line:
            raise MergeError(f"{label} contains a blank line at {line_number}")
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise MergeError(
                f"{label} line {line_number} is invalid JSON"
            ) from exc
        if not isinstance(value, dict):
            raise MergeError(f"{label} line {line_number} is not an object")
        rows.append(value)
    return rows


def _jsonl_bytes(rows: list[dict[str, Any]]) -> bytes:
    return b"".join(
        (
            json.dumps(row, ensure_ascii=False, separators=(",", ":"))
            + "\n"
        ).encode("utf-8")
        for row in rows
    )


def _load_json_object_bytes(payload: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MergeError(f"{label} is invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise MergeError(f"{label} root is not an object")
    return value


def _load_search_append_proposal(
    path: Path,
) -> tuple[bytes, dict[str, Any]]:
    if not path.is_file() or path.is_symlink():
        raise MergeError(f"SEARCH_APPEND proposal is missing or unsafe: {path}")
    try:
        payload = path.read_bytes()
    except OSError as exc:
        raise MergeError(f"cannot read SEARCH_APPEND proposal: {exc}") from exc
    proposal = _load_json_object_bytes(payload, "SEARCH_APPEND proposal")
    if payload != build_worker_bundle.canonical_json_bytes(proposal):
        raise MergeError("SEARCH_APPEND proposal is not canonically serialized")
    schema_errors = build_worker_bundle.json_schema_errors(
        proposal,
        _search_append_proposal_schema(),
        "search-append-proposal",
    )
    if schema_errors:
        raise MergeError(
            "SEARCH_APPEND proposal schema failed:\n- "
            + "\n- ".join(schema_errors)
        )
    return payload, proposal


def _load_coordinator_proposal(
    path: Path,
    *,
    kind: str,
    schema: dict[str, Any],
) -> tuple[bytes, dict[str, Any]]:
    if not path.is_file() or path.is_symlink():
        raise MergeError(f"{kind} proposal is missing or unsafe: {path}")
    try:
        payload = path.read_bytes()
    except OSError as exc:
        raise MergeError(f"cannot read {kind} proposal: {exc}") from exc
    proposal = _load_json_object_bytes(payload, f"{kind} proposal")
    if payload != build_worker_bundle.canonical_json_bytes(proposal):
        raise MergeError(f"{kind} proposal is not canonically serialized")
    schema_errors = build_worker_bundle.json_schema_errors(
        proposal,
        schema,
        f"{kind.lower().replace('_', '-')}-proposal",
    )
    if schema_errors:
        raise MergeError(
            f"{kind} proposal schema failed:\n- "
            + "\n- ".join(schema_errors)
        )
    return payload, proposal


def _is_exact_prefix(old: list[Any], new: list[Any]) -> bool:
    return len(new) >= len(old) and new[: len(old)] == old


def _validate_string_array_additions(
    old_value: object,
    new_value: object,
    label: str,
) -> tuple[list[str], list[str]]:
    old = _json_array(old_value, f"{label} prior")
    new = _json_array(new_value, f"{label} proposed")
    if not _is_exact_prefix(old, new):
        raise MergeError(f"{label} may append values but cannot delete or reorder")
    return old, new[len(old) :]


def _candidate_new_evidence(
    old: dict[str, Any] | None,
    new: dict[str, Any],
    *,
    trigger_hits: dict[str, dict[str, Any]],
    round_evidence_groups: set[str],
) -> set[str]:
    candidate_id = new.get("id", "<unknown>")
    evidence = new.get("source_evidence")
    if not isinstance(evidence, list) or not all(
        isinstance(item, dict) for item in evidence
    ):
        raise MergeError(f"candidate {candidate_id} has malformed source_evidence")
    prior_evidence: list[dict[str, Any]] = []
    if old is not None:
        old_evidence = old.get("source_evidence")
        if not isinstance(old_evidence, list) or not all(
            isinstance(item, dict) for item in old_evidence
        ):
            raise MergeError(
                f"existing candidate {candidate_id} has malformed source_evidence"
            )
        prior_evidence = old_evidence
        if not _is_exact_prefix(prior_evidence, evidence):
            raise MergeError(
                f"candidate {candidate_id} must preserve prior evidence "
                "as an exact prefix"
            )
    appended = evidence[len(prior_evidence) :]
    if not appended:
        raise MergeError(
            f"candidate {candidate_id} update lacks appended search evidence"
        )
    evidence_ids: set[str] = set()
    for item in appended:
        evidence_id = item.get("evidence_id")
        group_id = item.get("evidence_group_id")
        anchor = item.get("discovery_anchor")
        if (
            not isinstance(evidence_id, str)
            or not isinstance(group_id, str)
            or not isinstance(anchor, dict)
            or anchor.get("kind") != "SEARCH_HIT"
            or anchor.get("id") not in trigger_hits
        ):
            raise MergeError(
                f"candidate {candidate_id} appended evidence is not anchored "
                "to the new search hits"
            )
        if group_id not in round_evidence_groups:
            raise MergeError(
                f"candidate {candidate_id} appended evidence group {group_id} "
                "is absent from the new search round delta"
            )
        hit = trigger_hits[anchor["id"]]
        source_unit_id = item.get("source_unit_id")
        if (
            source_unit_id is not None
            and source_unit_id != hit.get("source_unit_id")
        ):
            raise MergeError(
                f"candidate {candidate_id} appended evidence source differs "
                "from its trigger hit"
            )
        evidence_ids.add(evidence_id)
    return evidence_ids


def _mechanics_changes_use_new_evidence(
    old: dict[str, Any],
    new: dict[str, Any],
    new_evidence_ids: set[str],
) -> None:
    candidate_id = new["id"]
    old_fingerprint = old.get("fingerprint")
    new_fingerprint = new.get("fingerprint")
    if not isinstance(old_fingerprint, dict) or not isinstance(
        new_fingerprint,
        dict,
    ):
        raise MergeError(f"candidate {candidate_id} has malformed fingerprint")
    for field in FINGERPRINT_FIELDS:
        if old_fingerprint.get(field) == new_fingerprint.get(field):
            continue
        value = new_fingerprint.get(field)
        evidence_ids = value.get("evidence_ids") if isinstance(value, dict) else None
        if not isinstance(evidence_ids, list) or not (
            set(evidence_ids) & new_evidence_ids
        ):
            raise MergeError(
                f"candidate {candidate_id} changed fingerprint field {field} "
                "without newly appended evidence"
            )
    for collection_name in ("parameters", "variants", "related_candidate_ids"):
        old_items = old.get(collection_name)
        new_items = new.get(collection_name)
        if not isinstance(old_items, list) or not isinstance(new_items, list):
            raise MergeError(
                f"candidate {candidate_id}.{collection_name} is malformed"
            )
        if not _is_exact_prefix(old_items, new_items):
            raise MergeError(
                f"candidate {candidate_id}.{collection_name} must preserve "
                "prior entries exactly"
            )
        for item in new_items[len(old_items) :]:
            evidence_ids = item.get("evidence_ids") if isinstance(item, dict) else None
            if not isinstance(evidence_ids, list) or not (
                set(evidence_ids) & new_evidence_ids
            ):
                raise MergeError(
                    f"candidate {candidate_id}.{collection_name} changed "
                    "without newly appended evidence"
                )


def _validate_enrichment_candidate_update(
    old: dict[str, Any] | None,
    new: dict[str, Any],
    *,
    trigger_hits: dict[str, dict[str, Any]],
    round_evidence_groups: set[str],
) -> None:
    candidate_id = new.get("id")
    if not isinstance(candidate_id, str):
        raise MergeError("candidate update lacks a string ID")
    if set(new) != set(CANDIDATE_FIELDS):
        raise MergeError(
            f"candidate {candidate_id} fields differ from the global schema"
        )
    if old is not None:
        if old.get("record_status") != "ACTIVE":
            raise MergeError(
                f"only ACTIVE candidate {candidate_id} may be enriched"
            )
        for field in CANDIDATE_ENRICHMENT_IMMUTABLE:
            if new.get(field) != old.get(field):
                raise MergeError(
                    f"candidate {candidate_id} enrichment changes immutable "
                    f"field {field}"
                )
        if new == old:
            raise MergeError(f"candidate {candidate_id} update is unchanged")

    new_evidence_ids = _candidate_new_evidence(
        old,
        new,
        trigger_hits=trigger_hits,
        round_evidence_groups=round_evidence_groups,
    )
    if old is None:
        if new.get("record_status") != "ACTIVE":
            raise MergeError(
                f"new search candidate {candidate_id} must be ACTIVE"
            )
        anchor = new.get("discovery_anchor")
        if (
            not isinstance(anchor, dict)
            or anchor.get("kind") != "SEARCH_HIT"
            or anchor.get("id") not in trigger_hits
        ):
            raise MergeError(
                f"new candidate {candidate_id} is not anchored to a new hit"
            )
        return

    for field in (
        "aliases",
        "source_unit_ids",
        "image_witnesses",
        "source_status",
        "evidence_strength",
        "cross_reference_ids",
    ):
        old_values = old.get(field)
        new_values = new.get(field)
        if (
            not isinstance(old_values, list)
            or not isinstance(new_values, list)
            or not _is_exact_prefix(old_values, new_values)
        ):
            raise MergeError(
                f"candidate {candidate_id}.{field} deletes or rewrites "
                "prior provenance"
            )
    _mechanics_changes_use_new_evidence(old, new, new_evidence_ids)


def _canonical_audit_paths(
    manifest: dict[str, Any],
    requested: list[str],
    *,
    allow_empty: bool = False,
) -> list[str]:
    document_by_path = {
        document["path"]: document for document in manifest["documents"]
    }
    if (
        (not requested and not allow_empty)
        or len(requested) != len(set(requested))
        or any(path not in document_by_path for path in requested)
    ):
        raise MergeError(
            "source_paths must be unique corpus documents"
        )
    canonical = sorted(
        requested,
        key=lambda path: (
            validate_audit.stage_for_document(document_by_path[path]),
            int(document_by_path[path]["order"]),
        ),
    )
    if requested != canonical:
        raise MergeError(
            "source_paths are not in canonical audit order"
        )
    return canonical


def _ordered_audit_paths(
    manifest: dict[str, Any],
    paths: set[str],
) -> list[str]:
    document_by_path = {
        document["path"]: document for document in manifest["documents"]
    }
    if not paths or any(path not in document_by_path for path in paths):
        raise MergeError("derived source paths are empty or outside the corpus")
    return sorted(
        paths,
        key=lambda path: (
            validate_audit.stage_for_document(document_by_path[path]),
            int(document_by_path[path]["order"]),
        ),
    )


def _validate_monotonic_search_append(
    current: dict[str, Any],
    proposed: dict[str, Any],
    *,
    epoch: int,
) -> dict[str, Any]:
    required_fields = {
        "schema_version",
        "phase",
        "tool_assumptions",
        "vocabulary",
        "rounds",
        "fixed_point",
    }
    if set(current) != required_fields or set(proposed) != required_fields:
        raise MergeError("search state differs from the closed root contract")
    if (
        proposed["schema_version"] != current["schema_version"]
        or proposed["phase"] != current["phase"]
    ):
        raise MergeError("SEARCH_APPEND changes schema or phase")
    for field in ("tool_assumptions", "vocabulary"):
        old_values = current.get(field)
        new_values = proposed.get(field)
        if (
            not isinstance(old_values, list)
            or not isinstance(new_values, list)
            or len(new_values) != len(set(new_values))
            or not _is_exact_prefix(old_values, new_values)
        ):
            raise MergeError(
                f"SEARCH_APPEND may only append unique {field}"
            )
    current_rounds = current.get("rounds")
    proposed_rounds = proposed.get("rounds")
    if (
        not isinstance(current_rounds, list)
        or not isinstance(proposed_rounds, list)
        or len(proposed_rounds) != len(current_rounds) + 1
        or proposed_rounds[: len(current_rounds)] != current_rounds
    ):
        raise MergeError(
            "SEARCH_APPEND must preserve all rounds exactly and append one"
        )
    if current.get("fixed_point") is not None:
        raise MergeError(
            "SEARCH_APPEND cannot extend a certified fixed point; reopen it first"
        )
    new_round = proposed_rounds[-1]
    if (
        not isinstance(new_round, dict)
        or new_round.get("epoch") != epoch
        or new_round.get("kind") not in {"LOCAL", "SATURATION"}
    ):
        raise MergeError(
            "appended search round must be LOCAL or SATURATION in the active epoch"
        )
    hits = new_round.get("hits")
    if not isinstance(hits, list):
        raise MergeError("SEARCH_APPEND round hits must be an array")
    return new_round


def _snapshot(goal_dir: Path) -> tuple[dict[str, bytes], dict[str, int]]:
    payloads: dict[str, bytes] = {}
    modes: dict[str, int] = {}
    for name in SNAPSHOT_NAMES:
        path = goal_dir / name
        if not path.is_file() or path.is_symlink():
            raise MergeError(f"global audit artifact is missing or unsafe: {path}")
        payloads[name] = path.read_bytes()
        modes[name] = path.stat().st_mode & 0o777
    return payloads, modes


def _require_base_artifact_digests(
    proposal: dict[str, Any],
    original_bytes: dict[str, bytes],
    kind: str,
) -> None:
    expected = {
        name: hashlib.sha256(original_bytes[name]).hexdigest()
        for name in WRITE_NAMES
    }
    if proposal.get("base_artifact_sha256") != expected:
        raise MergeError(
            f"{kind} base artifact digests are stale or incomplete"
        )


def _load_audit_state(
    original_bytes: dict[str, bytes],
) -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
    list[dict[str, str]],
    list[dict[str, Any]],
    list[dict[str, str]],
    list[dict[str, str]],
    dict[str, Any],
    list[dict[str, Any]],
]:
    return (
        _load_json_object_bytes(
            original_bytes[MANIFEST_NAME],
            MANIFEST_NAME,
        ),
        _read_jsonl_bytes(original_bytes[UNITS_NAME], UNITS_NAME),
        _read_csv_bytes(
            original_bytes[READING_NAME],
            READING_NAME,
            READING_HEADER,
        ),
        _read_jsonl_bytes(
            original_bytes[CANDIDATE_NAME],
            CANDIDATE_NAME,
        ),
        _read_csv_bytes(
            original_bytes[ROUTE_NAME],
            ROUTE_NAME,
            CROSS_REFERENCE_HEADER,
        ),
        _read_csv_bytes(
            original_bytes[ASSET_NAME],
            ASSET_NAME,
            ASSET_HEADER,
        ),
        _load_json_object_bytes(
            original_bytes[SEARCH_NAME],
            SEARCH_NAME,
        ),
        _read_jsonl_bytes(
            original_bytes[REVIEW_HISTORY_NAME],
            REVIEW_HISTORY_NAME,
        ),
    )


def _latest_path_result_digests(
    review_history: list[dict[str, Any]],
) -> dict[str, str]:
    return {
        change["source_path"]: change["result_projection_sha256"]
        for event in review_history
        for change in event.get("path_changes", [])
        if isinstance(change, dict)
        and isinstance(change.get("source_path"), str)
        and isinstance(change.get("result_projection_sha256"), str)
    }


def _latest_version_digests(
    review_history: list[dict[str, Any]],
    *,
    changes_field: str,
    id_field: str,
    digest_field: str,
) -> dict[str, str]:
    return {
        change[id_field]: change[digest_field]
        for event in review_history
        for change in event.get(changes_field, [])
        if isinstance(change, dict)
        and isinstance(change.get(id_field), str)
        and isinstance(change.get(digest_field), str)
    }


def _canonical_candidate_record(
    raw: dict[str, Any],
) -> dict[str, Any]:
    candidate = {field: raw[field] for field in CANDIDATE_FIELDS}
    if isinstance(candidate.get("fingerprint"), dict):
        candidate["fingerprint"] = {
            field: candidate["fingerprint"][field]
            for field in FINGERPRINT_FIELDS
            if field in candidate["fingerprint"]
        }
    return candidate


def _validate_stage_prerequisites(
    *,
    stage: int,
    manifest: dict[str, Any],
    units: list[dict[str, Any]],
    reading: list[dict[str, str]],
    candidates: list[dict[str, Any]],
    routes: list[dict[str, str]],
    assets: list[dict[str, str]],
    search: dict[str, Any],
    review_history: list[dict[str, Any]],
) -> None:
    prerequisite_stages = set(range(4, stage))
    if not prerequisite_stages:
        return
    errors = validate_audit.validate_objects(
        manifest,
        units,
        reading,
        candidates,
        routes,
        assets,
        search,
        review_history=review_history,
        require_stages=prerequisite_stages,
    )
    if errors:
        raise MergeError(
            f"stage {stage} merge prerequisites failed:\n- "
            + "\n- ".join(errors)
        )


def _review_sequence(history: list[dict[str, Any]]) -> int:
    identifiers: list[str] = []
    for index, event in enumerate(history):
        if not isinstance(event, dict) or set(event) != set(
            REVIEW_HISTORY_FIELDS
        ):
            raise MergeError(
                f"review-history event {index} differs from the frozen schema"
            )
        review_id = event.get("review_id")
        if not isinstance(review_id, str):
            raise MergeError(f"review-history event {index} lacks a review_id")
        identifiers.append(review_id)
    return _sequence(
        identifiers,
        "V",
        6,
        "review-history",
    )


def _active_review_epoch(history: list[dict[str, Any]]) -> int:
    _review_sequence(history)
    if not history:
        return 1
    return max(
        _positive_epoch(event.get("epoch"), f"review {event.get('review_id')}")
        for event in history
    )


def _validate_current_epoch_local_search_closed(
    *,
    history: list[dict[str, Any]],
    search: dict[str, Any],
    epoch: int,
) -> None:
    expected: dict[int, set[str]] = {}
    for event in history:
        if event.get("epoch") != epoch:
            continue
        stage = event.get("stage")
        paths = event.get("source_paths")
        if (
            not isinstance(stage, int)
            or isinstance(stage, bool)
            or not isinstance(paths, list)
            or not all(isinstance(path, str) for path in paths)
        ):
            raise MergeError(
                f"review {event.get('review_id')} has malformed search scope"
            )
        expected.setdefault(stage, set()).update(paths)
    if not expected:
        raise MergeError(
            f"cannot advance beyond epoch {epoch} without a review-history scope"
        )

    actual: dict[int, set[str]] = {}
    rounds = search.get("rounds")
    if not isinstance(rounds, list):
        raise MergeError("search rounds are not an array")
    for round_record in rounds:
        if (
            not isinstance(round_record, dict)
            or round_record.get("kind") != "LOCAL"
            or round_record.get("epoch") != epoch
        ):
            continue
        stage = round_record.get("owning_stage")
        queries = round_record.get("queries")
        if not isinstance(stage, int) or not isinstance(queries, list):
            raise MergeError("current-epoch LOCAL search round is malformed")
        for query in queries:
            if not isinstance(query, dict) or not isinstance(
                query.get("scope_paths"),
                list,
            ):
                raise MergeError("current-epoch LOCAL query scope is malformed")
            scope_paths = query["scope_paths"]
            if not all(isinstance(path, str) for path in scope_paths):
                raise MergeError("current-epoch LOCAL query scope is malformed")
            actual.setdefault(stage, set()).update(scope_paths)

    for stage in sorted(set(expected) | set(actual)):
        expected_paths = expected.get(stage, set())
        actual_paths = actual.get(stage, set())
        if actual_paths != expected_paths:
            raise MergeError(
                f"cannot advance beyond epoch {epoch}: Stage {stage} LOCAL "
                "search scopes are not closed "
                f"(expected={sorted(expected_paths)}, actual={sorted(actual_paths)})"
            )


def _validate_stage18_context_ready(
    *,
    label: str,
    manifest: dict[str, Any],
    history: list[dict[str, Any]],
    reading: list[dict[str, str]],
    assets: list[dict[str, str]],
    search: dict[str, Any],
) -> None:
    """Require exhausted blind review/local context before final route absence."""

    canonical_paths = {
        document["path"] for document in manifest["documents"]
    }
    reviewed_paths = {
        path
        for event in history
        if event.get("mode") in {"INITIAL", "REOPEN"}
        for path in event.get("source_paths", [])
        if isinstance(path, str)
    }
    if (
        any(row.get("review_status") != "REVIEWED" for row in reading)
        or any(
            row.get("inspection_status") != "SCREENED" for row in assets
        )
        or reviewed_paths != canonical_paths
    ):
        raise MergeError(
            f"{label} requires complete sequential source review and "
            "asset screening"
        )

    expected_scopes: dict[tuple[int, int], set[str]] = {}
    for event in history:
        if event.get("mode") not in {"INITIAL", "REOPEN"}:
            continue
        stage = event.get("stage")
        epoch = event.get("epoch")
        source_paths = event.get("source_paths")
        if (
            isinstance(stage, bool)
            or not isinstance(stage, int)
            or isinstance(epoch, bool)
            or not isinstance(epoch, int)
            or not isinstance(source_paths, list)
            or not all(isinstance(path, str) for path in source_paths)
        ):
            raise MergeError(
                f"{label} encountered malformed review scope"
            )
        expected_scopes.setdefault((stage, epoch), set()).update(
            source_paths
        )

    rounds = search.get("rounds")
    if not isinstance(rounds, list):
        raise MergeError(f"{label} search rounds are not an array")
    for (stage, epoch), expected_paths in sorted(expected_scopes.items()):
        local_rounds = [
            round_record
            for round_record in rounds
            if isinstance(round_record, dict)
            and round_record.get("kind") == "LOCAL"
            and round_record.get("owning_stage") == stage
            and round_record.get("epoch") == epoch
        ]
        actual_paths = {
            path
            for round_record in local_rounds
            for query in round_record.get("queries", [])
            if isinstance(query, dict)
            for path in query.get("scope_paths", [])
            if isinstance(path, str)
        }
        if not local_rounds or actual_paths != expected_paths:
            raise MergeError(
                f"{label} requires exact LOCAL search closure "
                f"for Stage {stage} epoch {epoch} "
                f"(expected={sorted(expected_paths)}, "
                f"actual={sorted(actual_paths)})"
            )
    active_epochs = [
        event.get("epoch")
        for event in history
        if isinstance(event, dict)
        and isinstance(event.get("epoch"), int)
        and not isinstance(event.get("epoch"), bool)
    ]
    if not active_epochs:
        raise MergeError(f"{label} has no active review epoch")
    active_epoch = max(active_epochs)
    if not validate_audit.has_full_corpus_saturation(
        search,
        epoch=active_epoch,
        canonical_paths=canonical_paths,
    ):
        raise MergeError(
            f"{label} requires a Stage 18 SATURATION search round in "
            f"the active review epoch {active_epoch} with exact "
            "full-corpus scope"
        )


def _validate_search_vocabulary_replay(
    search: dict[str, Any],
    *,
    label: str,
) -> None:
    """Require top-level vocabulary to be the exact ordered round replay."""

    rounds = search.get("rounds")
    vocabulary = search.get("vocabulary")
    if not isinstance(rounds, list) or not isinstance(vocabulary, list):
        raise MergeError(f"{label} search vocabulary state is malformed")
    replayed: list[str] = []
    for round_record in rounds:
        if not isinstance(round_record, dict) or not isinstance(
            round_record.get("new_vocabulary"),
            list,
        ):
            raise MergeError(f"{label} search vocabulary delta is malformed")
        new_vocabulary = round_record["new_vocabulary"]
        if not all(isinstance(value, str) for value in new_vocabulary):
            raise MergeError(f"{label} search vocabulary delta is malformed")
        replayed.extend(new_vocabulary)
    if vocabulary != replayed:
        raise MergeError(
            f"{label} top-level vocabulary differs from exact ordered "
            "round new_vocabulary replay"
        )


def _path_is_complete(
    path: str,
    reading: list[dict[str, str]],
    assets: list[dict[str, str]],
) -> bool:
    path_reading = [row for row in reading if row.get("path") == path]
    path_assets = [
        row for row in assets if row.get("assignment_path") == path
    ]
    return bool(path_reading) and all(
        row.get("review_status") == "REVIEWED" for row in path_reading
    ) and all(
        row.get("inspection_status") == "SCREENED" for row in path_assets
    )


def _validate_stage_path_prefix(
    *,
    stage: int,
    source_paths: tuple[str, ...],
    manifest: dict[str, Any],
    reading: list[dict[str, str]],
    assets: list[dict[str, str]],
) -> None:
    canonical_paths = build_worker_bundle.ordered_stage_paths(manifest, stage)
    if list(source_paths) != [
        path for path in canonical_paths if path in set(source_paths)
    ]:
        raise MergeError("bundle source paths are not in canonical manifest order")
    selected = set(source_paths)
    for path in source_paths:
        position = canonical_paths.index(path)
        for earlier in canonical_paths[:position]:
            if earlier not in selected and not _path_is_complete(
                earlier,
                reading,
                assets,
            ):
                raise MergeError(
                    f"cannot merge {path} while earlier canonical document "
                    f"{earlier} remains pending"
                )


def _positive_epoch(value: object, label: str) -> int:
    if isinstance(value, int) and not isinstance(value, bool) and value >= 1:
        return value
    if (
        isinstance(value, str)
        and value.isdigit()
        and not value.startswith("0")
        and int(value) >= 1
    ):
        return int(value)
    raise MergeError(f"{label} has an invalid discovery/review epoch: {value!r}")


def _validate_reopen_prerequisites(
    *,
    manifest: dict[str, Any],
    units: list[dict[str, Any]],
    reading: list[dict[str, str]],
    candidates: list[dict[str, Any]],
    routes: list[dict[str, str]],
    assets: list[dict[str, str]],
    search: dict[str, Any],
    review_history: list[dict[str, Any]],
    active_epoch: int,
) -> None:
    errors = validate_audit.validate_objects(
        manifest,
        units,
        reading,
        candidates,
        routes,
        assets,
        search,
        review_history=review_history,
    )
    if errors:
        raise MergeError(
            "reopened merge requires a valid current blind-audit state:\n- "
            + "\n- ".join(errors)
        )
    _validate_current_epoch_local_search_closed(
        history=review_history,
        search=search,
        epoch=active_epoch,
    )


def prepare_merge(
    bundle: Path,
    *,
    goal_dir: Path = GOAL_DIR,
) -> MergePlan:
    """Plan one worker merge from a cooperative atomic ledger snapshot."""
    try:
        with audit_transaction.read_guard(goal_dir):
            return _prepare_merge_locked(bundle, goal_dir=goal_dir)
    except audit_transaction.TransactionError as exc:
        raise MergeError(str(exc)) from exc


def _prepare_merge_locked(
    bundle: Path,
    *,
    goal_dir: Path = GOAL_DIR,
) -> MergePlan:
    """Return a fully validated, read-only merge plan."""

    bundle = bundle.resolve()
    goal_dir = goal_dir.resolve()
    bundle_paths = {
        "manifest": bundle / "allowed-manifest.json",
        "reading": bundle / "input" / "reading-input.csv",
        "assets": bundle / "input" / "asset-input.csv",
        "output": bundle / "output" / "output.json",
    }
    try:
        bundle_bytes = {
            label: path.read_bytes() for label, path in bundle_paths.items()
        }
    except OSError as exc:
        raise MergeError(f"cannot snapshot bundle: {exc}") from exc
    verification_errors = build_worker_bundle.verify_bundle(
        bundle,
        require_completed_output=True,
        goal_dir=goal_dir,
    )
    if verification_errors:
        raise MergeError(
            "bundle verification failed:\n- " + "\n- ".join(verification_errors)
        )
    for label, path in bundle_paths.items():
        if path.read_bytes() != bundle_bytes[label]:
            raise MergeError(f"bundle changed during verification: {label}")

    original_bytes, original_modes = _snapshot(goal_dir)
    try:
        manifest = json.loads(original_bytes[MANIFEST_NAME])
        units = validate_audit.verify_corpus.load_units(goal_dir / UNITS_NAME)
        reading = _read_csv(goal_dir / READING_NAME, READING_HEADER)
        candidates = _read_jsonl(goal_dir / CANDIDATE_NAME)
        routes = _read_csv(goal_dir / ROUTE_NAME, CROSS_REFERENCE_HEADER)
        assets = _read_csv(goal_dir / ASSET_NAME, ASSET_HEADER)
        search = json.loads(original_bytes[SEARCH_NAME])
        review_history = _read_jsonl(goal_dir / REVIEW_HISTORY_NAME)
        bundle_manifest = json.loads(bundle_bytes["manifest"])
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise MergeError(f"cannot load merge state: {exc}") from exc
    if not isinstance(manifest, dict) or not isinstance(search, dict):
        raise MergeError("global manifest/search root is not an object")
    if not isinstance(bundle_manifest, dict):
        raise MergeError("bundle manifest is not an object")
    stage = bundle_manifest.get("stage")
    discovery_epoch = bundle_manifest.get("discovery_epoch")
    if (
        not isinstance(stage, int)
        or isinstance(stage, bool)
        or not 4 <= stage <= 17
    ):
        raise MergeError("bundle manifest has an invalid stage")
    if (
        not isinstance(discovery_epoch, int)
        or isinstance(discovery_epoch, bool)
        or discovery_epoch < 1
    ):
        raise MergeError("bundle manifest has an invalid discovery_epoch")
    source_paths_value = bundle_manifest.get("source_paths")
    if not isinstance(source_paths_value, list) or not all(
        isinstance(item, str) for item in source_paths_value
    ):
        raise MergeError("bundle manifest has invalid source_paths")
    source_paths = tuple(source_paths_value)
    source_path_set = set(source_paths)

    bundle_reading = _read_csv_bytes(
        bundle_bytes["reading"],
        "reading-input.csv",
        READING_HEADER,
    )
    bundle_assets = _read_csv_bytes(
        bundle_bytes["assets"],
        "asset-input.csv",
        ASSET_HEADER,
    )
    current_reading_projection = [
        row for row in reading if row["path"] in source_path_set
    ]
    current_asset_projection = [
        row for row in assets if row["assignment_path"] in source_path_set
    ]
    if bundle_reading != current_reading_projection:
        raise MergeError("stale reading-input projection differs from global rows")
    if bundle_assets != current_asset_projection:
        raise MergeError("stale asset-input projection differs from global rows")

    try:
        review_mode = build_worker_bundle.projection_review_mode(
            bundle_reading,
            bundle_assets,
        )
    except ValueError as exc:
        raise MergeError(f"merge mode is ambiguous: {exc}") from exc
    reopened = review_mode == "REOPEN"
    active_epoch = _active_review_epoch(review_history)
    _validate_stage_path_prefix(
        stage=stage,
        source_paths=source_paths,
        manifest=manifest,
        reading=reading,
        assets=assets,
    )
    if reopened:
        if not review_history:
            raise MergeError(
                "reopened merge has no authoritative prior review-history event"
            )
        expected_epoch = active_epoch + 1
        if discovery_epoch != expected_epoch:
            raise MergeError(
                f"reopened discovery epoch {discovery_epoch} is not the next "
                f"review epoch {expected_epoch}"
            )
        _validate_reopen_prerequisites(
            manifest=manifest,
            units=units,
            reading=reading,
            candidates=candidates,
            routes=routes,
            assets=assets,
            search=search,
            review_history=review_history,
            active_epoch=active_epoch,
        )
    else:
        if discovery_epoch != active_epoch:
            raise MergeError(
                f"initial forward discovery epoch {discovery_epoch} differs "
                f"from the active review epoch {active_epoch}"
            )
        _validate_stage_prerequisites(
            stage=stage,
            manifest=manifest,
            units=units,
            reading=reading,
            candidates=candidates,
            routes=routes,
            assets=assets,
            search=search,
            review_history=review_history,
        )

    output = _load_output(bundle_bytes["output"])
    forbidden_paths = validate_audit.forbidden_keys(output)
    if forbidden_paths:
        raise MergeError(
            "worker output contains forbidden blind fields: "
            + ", ".join(forbidden_paths)
        )
    patterns, pattern_errors = validate_audit.load_blind_text_patterns()
    if pattern_errors:
        raise MergeError("; ".join(pattern_errors))
    text_leaks = validate_audit.blind_text_leaks(
        output,
        patterns,
        "worker-output",
    )
    if text_leaks:
        raise MergeError(
            "worker output contains forbidden reconciliation text: "
            + "; ".join(text_leaks[:10])
        )

    proposals_value = output.get("candidate_proposals")
    route_proposals_value = output.get("route_proposals")
    reading_updates_value = output.get("reading_updates")
    asset_updates_value = output.get("asset_updates")
    uncertainties_value = output.get("uncertainties")
    if not isinstance(proposals_value, list) or not all(
        isinstance(row, dict) for row in proposals_value
    ):
        raise MergeError("candidate_proposals is not an object array")
    if not isinstance(route_proposals_value, list) or not all(
        isinstance(row, dict) for row in route_proposals_value
    ):
        raise MergeError("route_proposals is not an object array")
    if not isinstance(reading_updates_value, list) or not all(
        isinstance(row, dict) for row in reading_updates_value
    ):
        raise MergeError("reading_updates is not an object array")
    if not isinstance(asset_updates_value, list) or not all(
        isinstance(row, dict) for row in asset_updates_value
    ):
        raise MergeError("asset_updates is not an object array")
    if not isinstance(uncertainties_value, list) or not all(
        isinstance(item, str) for item in uncertainties_value
    ):
        raise MergeError("uncertainties is not a string array")

    proposals = list(proposals_value)
    route_proposals = list(route_proposals_value)
    reading_updates = list(reading_updates_value)
    asset_updates = list(asset_updates_value)
    worker_uncertainties = tuple(uncertainties_value)

    local_candidates, local_evidence, local_groups = _candidate_local_sequences(
        proposals
    )
    local_routes = [
        str(row.get("route_id"))
        for row in route_proposals
        if isinstance(row.get("route_id"), str)
    ]
    if len(local_routes) != len(route_proposals):
        raise MergeError("route proposal has an invalid route_id")

    existing_candidate_ids = [str(row.get("id", "")) for row in candidates]
    existing_route_ids = [row.get("route_id", "") for row in routes]
    candidate_mapping = _allocate_mapping(
        local_candidates,
        existing_candidate_ids,
        local_prefix="W",
        global_prefix="B",
        local_width=4,
        global_width=4,
        label="candidate",
    )
    route_mapping = _allocate_mapping(
        local_routes,
        existing_route_ids,
        local_prefix="WR",
        global_prefix="R",
        local_width=4,
        global_width=6,
        label="route",
    )
    existing_evidence, existing_groups = _existing_evidence_sequences(candidates)
    evidence_mapping = _allocate_mapping(
        local_evidence,
        existing_evidence,
        local_prefix="WE",
        global_prefix="E",
        local_width=6,
        global_width=6,
        label="evidence",
    )
    group_mapping = _allocate_mapping(
        local_groups,
        existing_groups,
        local_prefix="WG",
        global_prefix="G",
        local_width=6,
        global_width=6,
        label="evidence-group",
    )

    mapped_candidates = [
        _rewrite_candidate(
            row,
            candidate_mapping,
            route_mapping,
            evidence_mapping,
            group_mapping,
        )
        for row in proposals
    ]
    mapped_routes: list[dict[str, str]] = []
    for row in route_proposals:
        mapped = dict(row)
        mapped["route_id"] = _map_id(
            row.get("route_id"),
            route_mapping,
            "route.route_id",
        )
        mapped_routes.append(mapped)

    assigned_reading_ids = {
        row["source_unit_id"] for row in bundle_reading
    }
    assigned_asset_ids = {row["asset_id"] for row in bundle_assets}
    proposed_reading = _replace_rows(
        reading,
        reading_updates,
        id_field="source_unit_id",
        assigned_ids=assigned_reading_ids,
        candidate_ids=candidate_mapping,
        route_ids=route_mapping,
        label="reading",
        reopened=reopened,
        expected_review_epoch=discovery_epoch,
    )
    proposed_assets = _replace_rows(
        assets,
        asset_updates,
        id_field="asset_id",
        assigned_ids=assigned_asset_ids,
        candidate_ids=candidate_mapping,
        route_ids=route_mapping,
        label="asset",
        reopened=reopened,
        expected_review_epoch=discovery_epoch,
    )
    proposed_candidates = candidates + mapped_candidates
    proposed_routes = routes + mapped_routes
    proposed_search = deepcopy(search)
    if reopened:
        proposed_search["fixed_point"] = None

    worker_id = str(bundle_manifest.get("worker_id"))
    unit_by_id = {unit["id"]: unit for unit in units}
    result_reading_by_id = {
        row["source_unit_id"]: row for row in proposed_reading
    }
    result_asset_by_id = {row["asset_id"]: row for row in proposed_assets}
    result_asset_by_physical_path = {
        row["physical_path"]: row for row in proposed_assets
    }
    candidate_changes: list[dict[str, Any]] = []
    for candidate in mapped_candidates:
        anchor_path = _candidate_anchor_path(
            candidate,
            unit_by_id,
            result_asset_by_physical_path,
        )
        if anchor_path not in source_path_set:
            raise MergeError(
                f"candidate {candidate['id']} discovery anchor lies outside "
                "the worker assignment"
            )
        candidate_changes.append(
            close_candidate_change("CREATE", candidate)
        )
    candidate_changes.sort(
        key=lambda change: int(change["candidate_id"][1:])
    )
    if [
        change["candidate_id"] for change in candidate_changes
    ] != [
        candidate["id"] for candidate in mapped_candidates
    ]:
        raise MergeError(
            "candidate proposal order differs from global candidate ID order"
        )
    next_review_number = _review_sequence(review_history) + 1
    prior_event_sha256 = (
        review_history[-1]["event_sha256"] if review_history else None
    )
    latest_path_result_sha256 = {
        path_change["source_path"]: path_change[
            "result_projection_sha256"
        ]
        for event in review_history
        if isinstance(event, dict)
        for path_change in event.get("path_changes", [])
        if isinstance(path_change, dict)
        and isinstance(path_change.get("source_path"), str)
        and isinstance(
            path_change.get("result_projection_sha256"),
            str,
        )
    }
    review_id = f"V{next_review_number:06d}"
    review_event_core: dict[str, Any] = {
        "review_id": review_id,
        "epoch": discovery_epoch,
        "stage": stage,
        "mode": review_mode,
        "reviewer": worker_id,
        "source_paths": list(source_paths),
    }
    path_changes: list[dict[str, Any]] = []
    for source_path in source_paths:
        path_core = {
            "source_path": source_path,
            "source_unit_ids": [
                row["source_unit_id"]
                for row in bundle_reading
                if row["path"] == source_path
            ],
            "asset_ids": [
                row["asset_id"]
                for row in bundle_assets
                if row["assignment_path"] == source_path
            ],
            "previous_path_result_sha256": (
                latest_path_result_sha256.get(source_path)
                if review_mode == "REOPEN"
                else None
            ),
        }
        try:
            path_changes.append(
                close_path_change(
                    review_event_core,
                    path_core,
                    unit_by_id,
                    result_reading_by_id,
                    result_asset_by_id,
                )
            )
        except KeyError as exc:
            raise MergeError(
                f"cannot bind review event {review_id} path "
                f"{source_path} to its exact projection: {exc}"
            ) from exc
    route_changes = [
        close_route_change("CREATE", route)
        for route in mapped_routes
    ]
    route_changes.sort(key=lambda change: int(change["route_id"][1:]))
    prior_search_result_sha256 = next(
        (
            event["search_change"]["after_search_sha256"]
            for event in reversed(review_history)
            if isinstance(event, dict)
            and isinstance(event.get("search_change"), dict)
            and isinstance(
                event["search_change"].get("after_search_sha256"),
                str,
            )
        ),
        None,
    )
    search_change = (
        close_search_change(
            search,
            proposed_search,
            prior_search_result_sha256,
        )
        if proposed_search != search
        else None
    )
    review_event_core.update(
        {
            "path_changes": path_changes,
            "candidate_changes": candidate_changes,
            "route_changes": route_changes,
            "search_change": search_change,
        }
    )
    try:
        review_event = close_review_event(
                review_event_core,
                prior_event_sha256,
        )
    except KeyError as exc:
        raise MergeError(
            f"cannot close atomic review event {review_id}: {exc}"
        ) from exc
    review_event = {
        field: review_event[field] for field in REVIEW_HISTORY_FIELDS
    }
    review_events = [review_event]
    proposed_review_history = review_history + review_events

    validation_errors = validate_audit.validate_objects(
        manifest,
        units,
        proposed_reading,
        proposed_candidates,
        proposed_routes,
        proposed_assets,
        proposed_search,
        review_history=proposed_review_history,
    )
    if validation_errors:
        raise MergeError(
            "proposed global state failed validation:\n- "
            + "\n- ".join(validation_errors)
        )

    proposed_bytes = {
        CANDIDATE_NAME: _append_jsonl(
            original_bytes[CANDIDATE_NAME],
            mapped_candidates,
        ),
        ROUTE_NAME: _append_csv(
            original_bytes[ROUTE_NAME],
            CROSS_REFERENCE_HEADER,
            mapped_routes,
        ),
        READING_NAME: build_worker_bundle.csv_bytes(
            READING_HEADER,
            proposed_reading,
        ),
        ASSET_NAME: build_worker_bundle.csv_bytes(
            ASSET_HEADER,
            proposed_assets,
        ),
        SEARCH_NAME: (
            original_bytes[SEARCH_NAME]
            if not reopened
            else build_worker_bundle.canonical_json_bytes(proposed_search)
        ),
        REVIEW_HISTORY_NAME: _append_jsonl(
            original_bytes[REVIEW_HISTORY_NAME],
            review_events,
        ),
    }
    if original_bytes[SEARCH_NAME] != (goal_dir / SEARCH_NAME).read_bytes():
        raise MergeError("search ledger changed while preparing the merge")
    for label, path in bundle_paths.items():
        if path.read_bytes() != bundle_bytes[label]:
            raise MergeError(f"verified bundle changed during merge planning: {label}")

    (
        original_bytes,
        original_modes,
        proposed_bytes,
        validation_token,
    ) = _freeze_plan_state(
        original_bytes,
        original_modes,
        proposed_bytes,
    )
    return MergePlan(
        bundle=bundle,
        goal_dir=goal_dir,
        worker_id=worker_id,
        stage=stage,
        discovery_epoch=discovery_epoch,
        review_ids=tuple(event["review_id"] for event in review_events),
        review_mode=review_mode,
        source_paths=source_paths,
        candidate_ids=candidate_mapping,
        route_ids=route_mapping,
        evidence_ids=evidence_mapping,
        evidence_group_ids=group_mapping,
        reading_update_count=len(reading_updates),
        asset_update_count=len(asset_updates),
        worker_uncertainties=worker_uncertainties,
        original_bytes=original_bytes,
        original_modes=original_modes,
        proposed_bytes=proposed_bytes,
        validation_token=validation_token,
    )


def prepare_search_append(
    proposal_path: Path,
    *,
    goal_dir: Path = GOAL_DIR,
) -> SearchAppendPlan:
    """Plan SEARCH_APPEND from a cooperative atomic ledger snapshot."""
    try:
        with audit_transaction.read_guard(goal_dir):
            return _prepare_search_append_locked(
                proposal_path,
                goal_dir=goal_dir,
            )
    except audit_transaction.TransactionError as exc:
        raise MergeError(str(exc)) from exc


def _prepare_search_append_locked(
    proposal_path: Path,
    *,
    goal_dir: Path = GOAL_DIR,
) -> SearchAppendPlan:
    """Validate one atomic SEARCH_APPEND proposal without writing it."""

    proposal_path = proposal_path.resolve()
    goal_dir = goal_dir.resolve()
    proposal_bytes, proposal = _load_search_append_proposal(proposal_path)
    original_bytes, original_modes = _snapshot(goal_dir)

    declared_base = proposal["base_artifact_sha256"]
    expected_base = {
        name: hashlib.sha256(original_bytes[name]).hexdigest()
        for name in WRITE_NAMES
    }
    if declared_base != expected_base:
        raise MergeError(
            "SEARCH_APPEND base artifact digests are stale or incomplete"
        )

    try:
        manifest = _load_json_object_bytes(
            original_bytes[MANIFEST_NAME],
            MANIFEST_NAME,
        )
        units = _read_jsonl_bytes(original_bytes[UNITS_NAME], UNITS_NAME)
        reading = _read_csv_bytes(
            original_bytes[READING_NAME],
            READING_NAME,
            READING_HEADER,
        )
        candidates = _read_jsonl_bytes(
            original_bytes[CANDIDATE_NAME],
            CANDIDATE_NAME,
        )
        routes = _read_csv_bytes(
            original_bytes[ROUTE_NAME],
            ROUTE_NAME,
            CROSS_REFERENCE_HEADER,
        )
        assets = _read_csv_bytes(
            original_bytes[ASSET_NAME],
            ASSET_NAME,
            ASSET_HEADER,
        )
        search = _load_json_object_bytes(
            original_bytes[SEARCH_NAME],
            SEARCH_NAME,
        )
        review_history = _read_jsonl_bytes(
            original_bytes[REVIEW_HISTORY_NAME],
            REVIEW_HISTORY_NAME,
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise MergeError(f"cannot load current audit state: {exc}") from exc

    current_errors = validate_audit.validate_objects(
        manifest,
        units,
        reading,
        candidates,
        routes,
        assets,
        search,
        review_history,
    )
    if current_errors:
        raise MergeError(
            "SEARCH_APPEND requires a valid current audit state:\n- "
            + "\n- ".join(current_errors)
        )

    epoch = proposal["epoch"]
    active_epoch = _active_review_epoch(review_history)
    if epoch != active_epoch:
        raise MergeError(
            f"SEARCH_APPEND epoch {epoch} differs from active epoch "
            f"{active_epoch}"
        )
    source_paths = tuple(
        _canonical_audit_paths(
            manifest,
            proposal["source_paths"],
            allow_empty=True,
        )
    )
    source_path_set = set(source_paths)
    reading_by_id = {row["source_unit_id"]: row for row in reading}
    asset_by_id = {row["asset_id"]: row for row in assets}
    unit_by_id = {unit["id"]: unit for unit in units}
    document_by_path = {
        document["path"]: document for document in manifest["documents"]
    }
    for path in source_paths:
        if not _path_is_complete(path, reading, assets):
            raise MergeError(
                f"SEARCH_APPEND path is not already fully reviewed: {path}"
            )

    proposed_search = proposal["proposed_search"]
    try:
        search_schema = json.loads(
            (
                goal_dir
                / "schemas"
                / "blind"
                / "search-rounds.schema.json"
            ).read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise MergeError(f"cannot load search schema: {exc}") from exc
    search_schema_errors = build_worker_bundle.json_schema_errors(
        proposed_search,
        search_schema,
        "proposed-search",
    )
    if search_schema_errors:
        raise MergeError(
            "proposed search schema failed:\n- "
            + "\n- ".join(search_schema_errors)
        )
    new_round = _validate_monotonic_search_append(
        search,
        proposed_search,
        epoch=epoch,
    )
    search_round_id = new_round.get("round_id")
    if not isinstance(search_round_id, str):
        raise MergeError("appended search round lacks a round_id")
    hit_rows = new_round.get("hits", [])
    trigger_hits: dict[str, dict[str, Any]] = {}
    authorizing_hits: dict[str, dict[str, Any]] = {}
    hit_paths: dict[str, str] = {}
    candidate_ids_by_unit: dict[str, set[str]] = {}
    route_ids_by_unit: dict[str, set[str]] = {}
    candidate_ids_by_path: dict[str, set[str]] = {}
    route_ids_by_path: dict[str, set[str]] = {}
    for hit in hit_rows:
        if not isinstance(hit, dict):
            raise MergeError("appended search round contains a non-object hit")
        hit_id = hit.get("hit_id")
        unit_id = hit.get("source_unit_id")
        if (
            not isinstance(hit_id, str)
            or hit_id in trigger_hits
            or not isinstance(unit_id, str)
            or unit_id not in unit_by_id
        ):
            raise MergeError("appended search round has invalid trigger hits")
        trigger_hits[hit_id] = hit
        path = unit_by_id[unit_id]["path"]
        hit_paths[hit_id] = path
        candidate_links = hit.get("candidate_ids")
        route_links = hit.get("route_ids")
        if not isinstance(candidate_links, list) or not all(
            isinstance(value, str) for value in candidate_links
        ):
            raise MergeError(f"search hit {hit_id} has invalid candidate links")
        if not isinstance(route_links, list) or not all(
            isinstance(value, str) for value in route_links
        ):
            raise MergeError(f"search hit {hit_id} has invalid route links")
        if hit.get("disposition") == "EXCLUSION":
            if candidate_links or route_links:
                raise MergeError(
                    f"EXCLUSION hit {hit_id} cannot authorize semantic links"
                )
            continue
        authorizing_hits[hit_id] = hit
        candidate_ids_by_unit.setdefault(unit_id, set()).update(candidate_links)
        route_ids_by_unit.setdefault(unit_id, set()).update(route_links)
        candidate_ids_by_path.setdefault(path, set()).update(candidate_links)
        route_ids_by_path.setdefault(path, set()).update(route_links)

    reading_updates = proposal["reading_updates"]
    reading_update_by_id: dict[str, dict[str, str]] = {}
    snapshot_changed_paths: set[str] = set()
    for update in reading_updates:
        unit_id = update["source_unit_id"]
        if unit_id in reading_update_by_id:
            raise MergeError(f"duplicate enrichment reading update: {unit_id}")
        old = reading_by_id.get(unit_id)
        if old is None:
            raise MergeError(f"enrichment reading update is unknown: {unit_id}")
        path = old["path"]
        if path not in source_path_set:
            raise MergeError(
                f"enrichment reading update lies outside source_paths: {unit_id}"
            )
        if update == old:
            raise MergeError(f"enrichment reading update is unchanged: {unit_id}")
        if unit_id not in candidate_ids_by_unit and unit_id not in route_ids_by_unit:
            if not any(
                hit.get("source_unit_id") == unit_id
                for hit in authorizing_hits.values()
            ):
                raise MergeError(
                    f"reading {unit_id} changed without a new search hit"
                )
        allowed = READING_ENRICHMENT_SCALARS | READING_ENRICHMENT_ARRAYS
        for field in READING_HEADER:
            if field not in allowed and update[field] != old[field]:
                raise MergeError(
                    f"reading {unit_id} changes completion/identity field {field}"
                )
        for field in READING_ENRICHMENT_ARRAYS:
            _, additions = _validate_string_array_additions(
                old[field],
                update[field],
                f"reading {unit_id}.{field}",
            )
            if field == "candidate_ids" and not set(additions).issubset(
                candidate_ids_by_unit.get(unit_id, set())
            ):
                raise MergeError(
                    f"reading {unit_id} adds candidate links absent from its hit"
                )
            if field == "route_ids" and not set(additions).issubset(
                route_ids_by_unit.get(unit_id, set())
            ):
                raise MergeError(
                    f"reading {unit_id} adds route links absent from its hit"
                )
        reading_update_by_id[unit_id] = update
        snapshot_changed_paths.add(path)
    proposed_reading = [
        reading_update_by_id.get(row["source_unit_id"], row)
        for row in reading
    ]

    asset_updates = proposal["asset_updates"]
    asset_update_by_id: dict[str, dict[str, str]] = {}
    for update in asset_updates:
        asset_id = update["asset_id"]
        if asset_id in asset_update_by_id:
            raise MergeError(f"duplicate enrichment asset update: {asset_id}")
        old = asset_by_id.get(asset_id)
        if old is None:
            raise MergeError(f"enrichment asset update is unknown: {asset_id}")
        path = old["assignment_path"]
        if path not in source_path_set:
            raise MergeError(
                f"enrichment asset update lies outside source_paths: {asset_id}"
            )
        if update == old:
            raise MergeError(f"enrichment asset update is unchanged: {asset_id}")
        for field in ASSET_HEADER:
            if field not in ASSET_ENRICHMENT_ARRAYS and update[field] != old[field]:
                raise MergeError(
                    f"asset {asset_id} changes visual/completion field {field}"
                )
        for field in ASSET_ENRICHMENT_ARRAYS:
            _, additions = _validate_string_array_additions(
                old[field],
                update[field],
                f"asset {asset_id}.{field}",
            )
            permitted = (
                candidate_ids_by_path
                if field == "candidate_ids"
                else route_ids_by_path
            )
            if not set(additions).issubset(permitted.get(path, set())):
                raise MergeError(
                    f"asset {asset_id} adds {field} absent from path hits"
                )
        asset_update_by_id[asset_id] = update
        snapshot_changed_paths.add(path)
    proposed_assets = [
        asset_update_by_id.get(row["asset_id"], row) for row in assets
    ]

    candidate_updates = proposal["candidate_updates"]
    candidate_by_id = {candidate["id"]: candidate for candidate in candidates}
    latest_candidate_result_sha256: dict[str, str] = {}
    for event in review_history:
        for change in event["candidate_changes"]:
            latest_candidate_result_sha256[change["candidate_id"]] = change[
                "after_candidate_sha256"
            ]
    candidate_update_by_id: dict[str, dict[str, Any]] = {}
    candidate_changes: list[dict[str, Any]] = []
    appended_candidates: list[dict[str, Any]] = []
    appended_evidence: list[dict[str, Any]] = []
    round_evidence_groups = set(new_round.get("new_evidence_groups", []))
    for raw_update in candidate_updates:
        update = {
            field: raw_update[field] for field in CANDIDATE_FIELDS
        }
        if isinstance(update.get("fingerprint"), dict):
            update["fingerprint"] = {
                field: update["fingerprint"][field]
                for field in FINGERPRINT_FIELDS
                if field in update["fingerprint"]
            }
        candidate_id = update.get("id")
        if not isinstance(candidate_id, str) or candidate_id in candidate_update_by_id:
            raise MergeError("candidate updates have invalid or duplicate IDs")
        old = candidate_by_id.get(candidate_id)
        _validate_enrichment_candidate_update(
            old,
            update,
            trigger_hits=authorizing_hits,
            round_evidence_groups=round_evidence_groups,
        )
        if candidate_id not in {
            value
            for hit in authorizing_hits.values()
            for value in hit.get("candidate_ids", [])
        }:
            raise MergeError(
                f"candidate {candidate_id} update is absent from trigger hits"
            )
        prior_evidence_count = (
            len(old["source_evidence"]) if old is not None else 0
        )
        new_evidence = update["source_evidence"][prior_evidence_count:]
        appended_evidence.extend(new_evidence)
        candidate_update_by_id[candidate_id] = update
        if old is None:
            appended_candidates.append(update)
            candidate_changes.append(
                close_candidate_change("CREATE", update)
            )
        else:
            previous_candidate_digest = (
                latest_candidate_result_sha256.get(candidate_id)
            )
            if previous_candidate_digest is None:
                raise MergeError(
                    f"candidate {candidate_id} lacks a prior version digest"
                )
            candidate_changes.append(
                close_candidate_change(
                    "UPDATE",
                    update,
                    before_candidate=old,
                    previous_candidate_result_sha256=(
                        previous_candidate_digest
                    ),
                )
            )
    candidate_changes.sort(
        key=lambda change: int(change["candidate_id"][1:])
    )

    existing_candidate_ids = [candidate["id"] for candidate in candidates]
    appended_candidate_ids = [
        candidate["id"] for candidate in appended_candidates
    ]
    _sequence(
        existing_candidate_ids + appended_candidate_ids,
        "B",
        4,
        "proposed candidate",
    )
    existing_evidence_ids, existing_group_ids = _existing_evidence_sequences(
        candidates
    )
    appended_evidence_ids = [
        str(evidence.get("evidence_id")) for evidence in appended_evidence
    ]
    _sequence(
        existing_evidence_ids + appended_evidence_ids,
        "E",
        6,
        "proposed evidence",
    )
    seen_groups = set(existing_group_ids)
    appended_group_ids: list[str] = []
    for evidence in appended_evidence:
        group_id = evidence.get("evidence_group_id")
        if not isinstance(group_id, str):
            raise MergeError("appended evidence lacks an evidence group")
        if group_id not in seen_groups:
            seen_groups.add(group_id)
            appended_group_ids.append(group_id)
    _sequence(
        existing_group_ids + appended_group_ids,
        "G",
        6,
        "proposed evidence-group",
    )
    if appended_group_ids != new_round.get("new_evidence_groups"):
        raise MergeError(
            "appended candidate evidence groups differ from search-round delta"
        )
    proposed_candidates = [
        candidate_update_by_id.get(candidate["id"], candidate)
        for candidate in candidates
    ] + appended_candidates

    route_appends = proposal["route_appends"]
    appended_route_ids: list[str] = []
    for route in route_appends:
        route_id = route["route_id"]
        if route_id in appended_route_ids:
            raise MergeError(f"duplicate appended route: {route_id}")
        appended_route_ids.append(route_id)
        if (
            route.get("discovery_kind") != "SEARCH_HIT"
            or route.get("discovery_id") not in authorizing_hits
            or route_id
            not in route_ids_by_path.get(
                hit_paths.get(route.get("discovery_id"), ""),
                set(),
            )
        ):
            raise MergeError(
                f"appended route {route_id} is not tied to a new trigger hit"
            )
    _sequence(
        [route["route_id"] for route in routes] + appended_route_ids,
        "R",
        6,
        "proposed route",
    )
    if appended_route_ids != new_round.get("new_routes"):
        raise MergeError(
            "appended routes differ from the search-round route delta"
        )
    proposed_routes = routes + route_appends

    if appended_candidate_ids != new_round.get("new_candidates"):
        raise MergeError(
            "appended candidates differ from the search-round candidate delta"
        )
    if proposed_search.get("fixed_point") is not None:
        _validate_stage18_context_ready(
            label="fixed-point establishment",
            manifest=manifest,
            history=review_history,
            reading=proposed_reading,
            assets=proposed_assets,
            search=proposed_search,
        )
        _validate_search_vocabulary_replay(
            proposed_search,
            label="fixed-point establishment",
        )
        pending_route_ids = [
            route["route_id"]
            for route in proposed_routes
            if route.get("status") == "PENDING"
        ]
        if pending_route_ids:
            raise MergeError(
                "fixed-point establishment requires all cross-reference "
                "routes to be terminal; pending="
                + ",".join(pending_route_ids)
            )
    if snapshot_changed_paths != source_path_set:
        raise MergeError(
            "SEARCH_APPEND source_paths must equal changed row/asset snapshots"
        )

    next_review_number = _review_sequence(review_history) + 1
    prior_event_sha256 = (
        review_history[-1]["event_sha256"] if review_history else None
    )
    latest_path_result_sha256 = {
        path_change["source_path"]: path_change[
            "result_projection_sha256"
        ]
        for event in review_history
        if isinstance(event, dict)
        for path_change in event.get("path_changes", [])
        if isinstance(path_change, dict)
        and isinstance(path_change.get("source_path"), str)
        and isinstance(
            path_change.get("result_projection_sha256"),
            str,
        )
    }
    proposed_reading_by_id = {
        row["source_unit_id"]: row for row in proposed_reading
    }
    proposed_asset_by_id = {row["asset_id"]: row for row in proposed_assets}
    coordinator_id = proposal["coordinator_id"]
    review_id = f"V{next_review_number:06d}"
    event_core: dict[str, Any] = {
        "review_id": review_id,
        "epoch": epoch,
        "stage": new_round["owning_stage"],
        "mode": "SEARCH_APPEND",
        "reviewer": coordinator_id,
        "source_paths": list(source_paths),
    }
    path_changes: list[dict[str, Any]] = []
    for path in source_paths:
        previous_path_digest = latest_path_result_sha256.get(path)
        if previous_path_digest is None:
            raise MergeError(
                f"SEARCH_APPEND path lacks prior result history: {path}"
            )
        path_changes.append(
            close_path_change(
                event_core,
                {
                    "source_path": path,
                    "source_unit_ids": [
                        unit["id"]
                        for unit in units
                        if unit["path"] == path
                    ],
                    "asset_ids": [
                        asset["asset_id"]
                        for asset in assets
                        if asset["assignment_path"] == path
                    ],
                    "previous_path_result_sha256": (
                        previous_path_digest
                    ),
                },
                unit_by_id,
                proposed_reading_by_id,
                proposed_asset_by_id,
            )
        )
    route_changes = [
        close_route_change("CREATE", route) for route in route_appends
    ]
    route_changes.sort(key=lambda change: int(change["route_id"][1:]))
    previous_search_result_sha256 = next(
        (
            event["search_change"]["after_search_sha256"]
            for event in reversed(review_history)
            if isinstance(event, dict)
            and isinstance(event.get("search_change"), dict)
            and isinstance(
                event["search_change"].get("after_search_sha256"),
                str,
            )
        ),
        None,
    )
    event_core.update(
        {
            "path_changes": path_changes,
            "candidate_changes": candidate_changes,
            "route_changes": route_changes,
            "search_change": close_search_change(
                search,
                proposed_search,
                previous_search_result_sha256,
            ),
        }
    )
    event = close_review_event(event_core, prior_event_sha256)
    event = {field: event[field] for field in REVIEW_HISTORY_FIELDS}
    review_events = [event]
    proposed_review_history = review_history + review_events

    validation_errors = validate_audit.validate_objects(
        manifest,
        units,
        proposed_reading,
        proposed_candidates,
        proposed_routes,
        proposed_assets,
        proposed_search,
        proposed_review_history,
    )
    if validation_errors:
        raise MergeError(
            "proposed SEARCH_APPEND failed full validation:\n- "
            + "\n- ".join(validation_errors)
        )

    proposed_bytes = {
        CANDIDATE_NAME: _jsonl_bytes(proposed_candidates),
        ROUTE_NAME: _append_csv(
            original_bytes[ROUTE_NAME],
            CROSS_REFERENCE_HEADER,
            route_appends,
        ),
        READING_NAME: build_worker_bundle.csv_bytes(
            READING_HEADER,
            proposed_reading,
        ),
        ASSET_NAME: build_worker_bundle.csv_bytes(
            ASSET_HEADER,
            proposed_assets,
        ),
        SEARCH_NAME: build_worker_bundle.canonical_json_bytes(
            proposed_search
        ),
        REVIEW_HISTORY_NAME: _append_jsonl(
            original_bytes[REVIEW_HISTORY_NAME],
            review_events,
        ),
    }
    if proposal_path.read_bytes() != proposal_bytes:
        raise MergeError("SEARCH_APPEND proposal changed during validation")
    for name, expected in original_bytes.items():
        path = goal_dir / name
        if (
            not path.is_file()
            or path.is_symlink()
            or path.read_bytes() != expected
            or (path.stat().st_mode & 0o777) != original_modes[name]
        ):
            raise MergeError(
                f"global audit state changed during SEARCH_APPEND planning: {name}"
            )

    (
        original_bytes,
        original_modes,
        proposed_bytes,
        validation_token,
    ) = _freeze_plan_state(
        original_bytes,
        original_modes,
        proposed_bytes,
    )
    return SearchAppendPlan(
        proposal=proposal_path,
        goal_dir=goal_dir,
        coordinator_id=coordinator_id,
        epoch=epoch,
        source_paths=source_paths,
        search_round_id=search_round_id,
        trigger_hit_ids=tuple(authorizing_hits),
        review_ids=tuple(event["review_id"] for event in review_events),
        reading_update_count=len(reading_updates),
        asset_update_count=len(asset_updates),
        candidate_update_count=(
            len(candidate_updates) - len(appended_candidates)
        ),
        candidate_append_count=len(appended_candidates),
        route_append_count=len(route_appends),
        original_bytes=original_bytes,
        original_modes=original_modes,
        proposed_bytes=proposed_bytes,
        validation_token=validation_token,
    )


def prepare_route_resolution(
    proposal_path: Path,
    *,
    goal_dir: Path = GOAL_DIR,
) -> RouteResolutionPlan:
    """Plan one governed route-closure transaction."""
    try:
        with audit_transaction.read_guard(goal_dir):
            return _prepare_route_resolution_locked(
                proposal_path,
                goal_dir=goal_dir,
            )
    except audit_transaction.TransactionError as exc:
        raise MergeError(str(exc)) from exc


def _prepare_route_resolution_locked(
    proposal_path: Path,
    *,
    goal_dir: Path,
) -> RouteResolutionPlan:
    proposal_path = proposal_path.resolve()
    goal_dir = goal_dir.resolve()
    proposal_bytes, proposal = _load_coordinator_proposal(
        proposal_path,
        kind="ROUTE_RESOLUTION",
        schema=_route_resolution_proposal_schema(),
    )
    original_bytes, original_modes = _snapshot(goal_dir)
    _require_base_artifact_digests(
        proposal,
        original_bytes,
        "ROUTE_RESOLUTION",
    )
    try:
        (
            manifest,
            units,
            reading,
            candidates,
            routes,
            assets,
            search,
            review_history,
        ) = _load_audit_state(original_bytes)
    except (KeyError, TypeError, ValueError) as exc:
        raise MergeError(f"cannot load current audit state: {exc}") from exc
    current_errors = validate_audit.validate_objects(
        manifest,
        units,
        reading,
        candidates,
        routes,
        assets,
        search,
        review_history,
    )
    if current_errors:
        raise MergeError(
            "ROUTE_RESOLUTION requires a valid current audit state:\n- "
            + "\n- ".join(current_errors)
        )
    epoch = proposal["epoch"]
    if epoch != _active_review_epoch(review_history):
        raise MergeError("ROUTE_RESOLUTION must use the active review epoch")

    unit_by_id = {unit["id"]: unit for unit in units}
    asset_by_id = {asset["asset_id"]: asset for asset in assets}
    route_by_id = {route["route_id"]: route for route in routes}
    document_by_path = {
        document["path"]: document for document in manifest["documents"]
    }
    latest_route_digests = _latest_version_digests(
        review_history,
        changes_field="route_changes",
        id_field="route_id",
        digest_field="after_route_sha256",
    )
    route_updates = proposal["route_updates"]
    update_by_id: dict[str, dict[str, str]] = {}
    route_changes: list[dict[str, Any]] = []
    resolution_paths: set[str] = set()
    operating_stage = 4
    missing_target_final_requested = False
    immutable_fields = set(CROSS_REFERENCE_HEADER) - {
        "status",
        "target_unit_ids",
        "target_asset_ids",
        "attempts",
        "vocabulary_terms",
        "defect_boundary",
    }
    for update in route_updates:
        route_id = update["route_id"]
        if route_id in update_by_id:
            raise MergeError(f"duplicate route resolution update: {route_id}")
        before = route_by_id.get(route_id)
        if before is None:
            raise MergeError(f"route resolution is unknown: {route_id}")
        if before["status"] != "PENDING":
            raise MergeError(
                f"route resolution requires an existing PENDING row: {route_id}"
            )
        if update["status"] not in {"RESOLVED", "MISSING_TARGET_FINAL"}:
            raise MergeError(
                f"route {route_id} does not close to a terminal status"
            )
        if any(update[field] != before[field] for field in immutable_fields):
            raise MergeError(
                f"route {route_id} changes immutable discovery/source fields"
            )
        if update == before:
            raise MergeError(f"route resolution is unchanged: {route_id}")
        for field in (
            "target_unit_ids",
            "target_asset_ids",
            "attempts",
            "vocabulary_terms",
        ):
            prior_values = _json_array(
                before[field],
                f"route {route_id} prior {field}",
            )
            new_values = _json_array(
                update[field],
                f"route {route_id} proposed {field}",
            )
            if not _is_exact_prefix(prior_values, new_values):
                raise MergeError(
                    f"route {route_id}.{field} rewrites prior entries"
                )
        if update["status"] == "MISSING_TARGET_FINAL":
            missing_target_final_requested = True
            operating_stage = 18
            source_unit = unit_by_id.get(update["source_unit_id"])
            source_asset = asset_by_id.get(update["source_asset_id"])
            if source_unit is not None:
                resolution_paths.add(source_unit["path"])
            elif source_asset is not None:
                resolution_paths.add(source_asset["assignment_path"])
            else:
                raise MergeError(
                    f"route {route_id} has no resolvable source anchor"
                )
        else:
            target_paths: set[str] = set()
            for unit_id in _json_array(
                update["target_unit_ids"],
                f"route {route_id}.target_unit_ids",
            ):
                unit = unit_by_id.get(unit_id)
                if unit is None:
                    raise MergeError(
                        f"route {route_id} targets unknown unit {unit_id}"
                    )
                target_paths.add(unit["path"])
            for asset_id in _json_array(
                update["target_asset_ids"],
                f"route {route_id}.target_asset_ids",
            ):
                asset = asset_by_id.get(asset_id)
                if asset is None:
                    raise MergeError(
                        f"route {route_id} targets unknown asset {asset_id}"
                    )
                target_paths.add(asset["assignment_path"])
            if not target_paths:
                raise MergeError(
                    f"RESOLVED route {route_id} has no governed target"
                )
            resolution_paths.update(target_paths)
            if operating_stage != 18:
                operating_stage = max(
                    operating_stage,
                    *(
                        validate_audit.stage_for_document(
                            document_by_path[path]
                        )
                        for path in target_paths
                    ),
                )
        previous_digest = latest_route_digests.get(route_id)
        if previous_digest is None:
            raise MergeError(f"route {route_id} lacks a prior version digest")
        route_changes.append(
            close_route_change(
                "UPDATE",
                update,
                before_route=before,
                previous_route_result_sha256=previous_digest,
            )
        )
        update_by_id[route_id] = update
    if missing_target_final_requested:
        _validate_stage18_context_ready(
            label="MISSING_TARGET_FINAL",
            manifest=manifest,
            history=review_history,
            reading=reading,
            assets=assets,
            search=search,
        )
        _validate_search_vocabulary_replay(
            search,
            label="MISSING_TARGET_FINAL",
        )
    route_changes.sort(key=lambda change: int(change["route_id"][1:]))
    source_paths = tuple(_ordered_audit_paths(manifest, resolution_paths))
    proposed_routes = [
        update_by_id.get(route["route_id"], route) for route in routes
    ]
    latest_path_digests = _latest_path_result_digests(review_history)
    event_core: dict[str, Any] = {
        "review_id": f"V{_review_sequence(review_history) + 1:06d}",
        "epoch": epoch,
        "stage": operating_stage,
        "mode": "ROUTE_RESOLUTION",
        "reviewer": proposal["coordinator_id"],
        "source_paths": list(source_paths),
    }
    reading_by_id = {row["source_unit_id"]: row for row in reading}
    asset_result_by_id = {row["asset_id"]: row for row in assets}
    path_changes: list[dict[str, Any]] = []
    for path in source_paths:
        previous_digest = latest_path_digests.get(path)
        if previous_digest is None:
            raise MergeError(
                f"route-resolution path lacks prior result history: {path}"
            )
        path_changes.append(
            close_path_change(
                event_core,
                {
                    "source_path": path,
                    "source_unit_ids": [
                        unit["id"] for unit in units if unit["path"] == path
                    ],
                    "asset_ids": [
                        asset["asset_id"]
                        for asset in assets
                        if asset["assignment_path"] == path
                    ],
                    "previous_path_result_sha256": previous_digest,
                },
                unit_by_id,
                reading_by_id,
                asset_result_by_id,
            )
        )
    event_core.update(
        {
            "path_changes": path_changes,
            "candidate_changes": [],
            "route_changes": route_changes,
            "search_change": None,
        }
    )
    prior_event = (
        review_history[-1]["event_sha256"] if review_history else None
    )
    event = close_review_event(event_core, prior_event)
    proposed_history = review_history + [event]
    validation_errors = validate_audit.validate_objects(
        manifest,
        units,
        reading,
        candidates,
        proposed_routes,
        assets,
        search,
        proposed_history,
    )
    if validation_errors:
        raise MergeError(
            "proposed ROUTE_RESOLUTION failed full validation:\n- "
            + "\n- ".join(validation_errors)
        )
    proposed_bytes = {
        name: original_bytes[name] for name in WRITE_NAMES
    }
    proposed_bytes[ROUTE_NAME] = build_worker_bundle.csv_bytes(
        CROSS_REFERENCE_HEADER,
        proposed_routes,
    )
    proposed_bytes[REVIEW_HISTORY_NAME] = _append_jsonl(
        original_bytes[REVIEW_HISTORY_NAME],
        [event],
    )
    if proposal_path.read_bytes() != proposal_bytes:
        raise MergeError("ROUTE_RESOLUTION proposal changed during validation")
    (
        original_bytes,
        original_modes,
        proposed_bytes,
        validation_token,
    ) = _freeze_plan_state(
        original_bytes,
        original_modes,
        proposed_bytes,
    )
    return RouteResolutionPlan(
        proposal=proposal_path,
        goal_dir=goal_dir,
        coordinator_id=proposal["coordinator_id"],
        epoch=epoch,
        stage=operating_stage,
        source_paths=source_paths,
        review_ids=(event["review_id"],),
        route_update_count=len(route_updates),
        original_bytes=original_bytes,
        original_modes=original_modes,
        proposed_bytes=proposed_bytes,
        validation_token=validation_token,
    )


def prepare_candidate_revision(
    proposal_path: Path,
    *,
    goal_dir: Path = GOAL_DIR,
) -> CandidateRevisionPlan:
    """Plan one Stage-18 candidate lifecycle transaction."""
    try:
        with audit_transaction.read_guard(goal_dir):
            return _prepare_candidate_revision_locked(
                proposal_path,
                goal_dir=goal_dir,
            )
    except audit_transaction.TransactionError as exc:
        raise MergeError(str(exc)) from exc


def _prepare_candidate_revision_locked(
    proposal_path: Path,
    *,
    goal_dir: Path,
) -> CandidateRevisionPlan:
    proposal_path = proposal_path.resolve()
    goal_dir = goal_dir.resolve()
    proposal_bytes, proposal = _load_coordinator_proposal(
        proposal_path,
        kind="CANDIDATE_REVISION",
        schema=_candidate_revision_proposal_schema(),
    )
    original_bytes, original_modes = _snapshot(goal_dir)
    _require_base_artifact_digests(
        proposal,
        original_bytes,
        "CANDIDATE_REVISION",
    )
    try:
        (
            manifest,
            units,
            reading,
            candidates,
            routes,
            assets,
            search,
            review_history,
        ) = _load_audit_state(original_bytes)
    except (KeyError, TypeError, ValueError) as exc:
        raise MergeError(f"cannot load current audit state: {exc}") from exc
    current_errors = validate_audit.validate_objects(
        manifest,
        units,
        reading,
        candidates,
        routes,
        assets,
        search,
        review_history,
    )
    if current_errors:
        raise MergeError(
            "CANDIDATE_REVISION requires a valid current audit state:\n- "
            + "\n- ".join(current_errors)
        )
    if any(row["review_status"] != "REVIEWED" for row in reading) or any(
        row["inspection_status"] != "SCREENED" for row in assets
    ):
        raise MergeError(
            "CANDIDATE_REVISION requires complete source and asset review"
        )
    epoch = proposal["epoch"]
    if epoch != _active_review_epoch(review_history):
        raise MergeError("CANDIDATE_REVISION must use the active review epoch")

    candidate_by_id = {
        candidate["id"]: candidate for candidate in candidates
    }
    latest_candidate_digests = _latest_version_digests(
        review_history,
        changes_field="candidate_changes",
        id_field="candidate_id",
        digest_field="after_candidate_sha256",
    )
    candidate_update_by_id: dict[str, dict[str, Any]] = {}
    candidate_changes: list[dict[str, Any]] = []
    appended_candidates: list[dict[str, Any]] = []
    appended_evidence: list[dict[str, Any]] = []
    definitive_evidence_ids: set[str] = set()
    prefix_fields = (
        "aliases",
        "source_unit_ids",
        "source_evidence",
        "source_status",
        "image_witnesses",
        "evidence_strength",
        "parameters",
        "variants",
        "missing_mechanics",
        "uncertainties",
        "related_candidate_ids",
        "cross_reference_ids",
        "evidence_reassignments",
    )
    for raw_update in proposal["candidate_updates"]:
        update = _canonical_candidate_record(raw_update)
        candidate_id = update["id"]
        if candidate_id in candidate_update_by_id:
            raise MergeError(
                f"duplicate candidate revision update: {candidate_id}"
            )
        before = candidate_by_id.get(candidate_id)
        if before is None:
            appended_candidates.append(update)
            candidate_changes.append(
                close_candidate_change("CREATE", update)
            )
            prior_evidence_count = 0
            prior_relation_count = 0
        else:
            if update == before:
                raise MergeError(
                    f"candidate revision is unchanged: {candidate_id}"
                )
            for field in (
                "id",
                "provisional_name",
                "discovery_stage",
                "discovery_anchor",
            ):
                if update[field] != before[field]:
                    raise MergeError(
                        f"candidate {candidate_id} changes immutable {field}"
                    )
            before_status = before["record_status"]
            after_status = update["record_status"]
            if (
                before_status != "ACTIVE"
                and after_status != before_status
            ) or (
                before_status == "ACTIVE"
                and after_status
                not in {
                    "ACTIVE",
                    "MERGED_REDIRECT",
                    "SPLIT_SUPERSEDED",
                }
            ):
                raise MergeError(
                    f"candidate {candidate_id} has an invalid lifecycle transition"
                )
            for field in prefix_fields:
                old_values = before[field]
                new_values = update[field]
                if (
                    not isinstance(old_values, list)
                    or not isinstance(new_values, list)
                    or not _is_exact_prefix(old_values, new_values)
                ):
                    raise MergeError(
                        f"candidate {candidate_id}.{field} rewrites prior provenance"
                    )
            previous_digest = latest_candidate_digests.get(candidate_id)
            if previous_digest is None:
                raise MergeError(
                    f"candidate {candidate_id} lacks a prior version digest"
                )
            candidate_changes.append(
                close_candidate_change(
                    "UPDATE",
                    update,
                    before_candidate=before,
                    previous_candidate_result_sha256=previous_digest,
                )
            )
            prior_evidence_count = len(before["source_evidence"])
            prior_relation_count = len(before["related_candidate_ids"])
        appended_evidence.extend(
            update["source_evidence"][prior_evidence_count:]
        )
        for relation in update["related_candidate_ids"][
            prior_relation_count:
        ]:
            if (
                isinstance(relation, dict)
                and relation.get("relation")
                in {"MERGED_INTO", "SPLIT_INTO"}
            ):
                definitive_evidence_ids.update(
                    evidence_id
                    for evidence_id in relation.get("evidence_ids", [])
                    if isinstance(evidence_id, str)
                )
        candidate_update_by_id[candidate_id] = update
    candidate_changes.sort(
        key=lambda change: int(change["candidate_id"][1:])
    )
    proposed_candidates = [
        candidate_update_by_id.get(candidate["id"], candidate)
        for candidate in candidates
    ] + appended_candidates
    _sequence(
        [candidate["id"] for candidate in proposed_candidates],
        "B",
        4,
        "proposed candidate",
    )
    proposed_evidence_ids, proposed_group_ids = (
        _existing_evidence_sequences(proposed_candidates)
    )
    _sequence(proposed_evidence_ids, "E", 6, "proposed evidence")
    _sequence(proposed_group_ids, "G", 6, "proposed evidence-group")
    proposed_candidate_ids = {
        candidate["id"] for candidate in proposed_candidates
    }

    reading_by_id = {row["source_unit_id"]: row for row in reading}
    reading_update_by_id: dict[str, dict[str, str]] = {}
    revision_paths: set[str] = set()
    for update in proposal["reading_updates"]:
        unit_id = update["source_unit_id"]
        if unit_id in reading_update_by_id:
            raise MergeError(
                f"duplicate candidate-revision reading update: {unit_id}"
            )
        before = reading_by_id.get(unit_id)
        if before is None:
            raise MergeError(
                f"candidate-revision reading row is unknown: {unit_id}"
            )
        changed_fields = {
            field for field in READING_HEADER if update[field] != before[field]
        }
        if changed_fields != {"candidate_ids"}:
            raise MergeError(
                f"candidate revision may change only reading candidate_ids: {unit_id}"
            )
        if not set(
            _json_array(
                update["candidate_ids"],
                f"reading {unit_id}.candidate_ids",
            )
        ).issubset(proposed_candidate_ids):
            raise MergeError(
                f"reading {unit_id} links an unknown candidate"
            )
        reading_update_by_id[unit_id] = update
        revision_paths.add(before["path"])
    proposed_reading = [
        reading_update_by_id.get(row["source_unit_id"], row)
        for row in reading
    ]

    asset_by_id = {row["asset_id"]: row for row in assets}
    asset_update_by_id: dict[str, dict[str, str]] = {}
    for update in proposal["asset_updates"]:
        asset_id = update["asset_id"]
        if asset_id in asset_update_by_id:
            raise MergeError(
                f"duplicate candidate-revision asset update: {asset_id}"
            )
        before = asset_by_id.get(asset_id)
        if before is None:
            raise MergeError(
                f"candidate-revision asset row is unknown: {asset_id}"
            )
        changed_fields = {
            field for field in ASSET_HEADER if update[field] != before[field]
        }
        if changed_fields != {"candidate_ids"}:
            raise MergeError(
                f"candidate revision may change only asset candidate_ids: {asset_id}"
            )
        if not set(
            _json_array(
                update["candidate_ids"],
                f"asset {asset_id}.candidate_ids",
            )
        ).issubset(proposed_candidate_ids):
            raise MergeError(f"asset {asset_id} links an unknown candidate")
        asset_update_by_id[asset_id] = update
        revision_paths.add(before["assignment_path"])
    proposed_assets = [
        asset_update_by_id.get(row["asset_id"], row) for row in assets
    ]

    unit_by_id = {unit["id"]: unit for unit in units}
    asset_by_physical_path = {
        asset["physical_path"]: asset for asset in assets
    }
    search_hit_paths = {
        hit["hit_id"]: unit_by_id[hit["source_unit_id"]]["path"]
        for round_record in search.get("rounds", [])
        if isinstance(round_record, dict)
        for hit in round_record.get("hits", [])
        if isinstance(hit, dict)
        and isinstance(hit.get("hit_id"), str)
        and hit.get("source_unit_id") in unit_by_id
    }
    evidence_by_id = {
        evidence["evidence_id"]: evidence
        for candidate in proposed_candidates
        for evidence in candidate["source_evidence"]
        if isinstance(evidence, dict)
        and isinstance(evidence.get("evidence_id"), str)
    }
    evidence_to_scope = list(appended_evidence) + [
        evidence_by_id[evidence_id]
        for evidence_id in sorted(definitive_evidence_ids)
        if evidence_id in evidence_by_id
    ]
    for evidence in evidence_to_scope:
        path = _provenance_anchor_path(
            evidence.get("discovery_anchor"),
            unit_by_id=unit_by_id,
            asset_by_physical_path=asset_by_physical_path,
            search_hit_paths=search_hit_paths,
        )
        if path is None:
            raise MergeError(
                "candidate revision evidence has no canonical source path"
            )
        revision_paths.add(path)
    source_paths = tuple(_ordered_audit_paths(manifest, revision_paths))
    latest_path_digests = _latest_path_result_digests(review_history)
    event_core: dict[str, Any] = {
        "review_id": f"V{_review_sequence(review_history) + 1:06d}",
        "epoch": epoch,
        "stage": 18,
        "mode": "CANDIDATE_REVISION",
        "reviewer": proposal["coordinator_id"],
        "source_paths": list(source_paths),
    }
    proposed_reading_by_id = {
        row["source_unit_id"]: row for row in proposed_reading
    }
    proposed_asset_by_id = {
        row["asset_id"]: row for row in proposed_assets
    }
    path_changes: list[dict[str, Any]] = []
    for path in source_paths:
        previous_digest = latest_path_digests.get(path)
        if previous_digest is None:
            raise MergeError(
                f"candidate-revision path lacks prior result history: {path}"
            )
        path_changes.append(
            close_path_change(
                event_core,
                {
                    "source_path": path,
                    "source_unit_ids": [
                        unit["id"] for unit in units if unit["path"] == path
                    ],
                    "asset_ids": [
                        asset["asset_id"]
                        for asset in assets
                        if asset["assignment_path"] == path
                    ],
                    "previous_path_result_sha256": previous_digest,
                },
                unit_by_id,
                proposed_reading_by_id,
                proposed_asset_by_id,
            )
        )
    event_core.update(
        {
            "path_changes": path_changes,
            "candidate_changes": candidate_changes,
            "route_changes": [],
            "search_change": None,
        }
    )
    prior_event = (
        review_history[-1]["event_sha256"] if review_history else None
    )
    event = close_review_event(event_core, prior_event)
    proposed_history = review_history + [event]
    validation_errors = validate_audit.validate_objects(
        manifest,
        units,
        proposed_reading,
        proposed_candidates,
        routes,
        proposed_assets,
        search,
        proposed_history,
    )
    if validation_errors:
        raise MergeError(
            "proposed CANDIDATE_REVISION failed full validation:\n- "
            + "\n- ".join(validation_errors)
        )
    proposed_bytes = {
        name: original_bytes[name] for name in WRITE_NAMES
    }
    proposed_bytes[CANDIDATE_NAME] = _jsonl_bytes(proposed_candidates)
    proposed_bytes[READING_NAME] = build_worker_bundle.csv_bytes(
        READING_HEADER,
        proposed_reading,
    )
    proposed_bytes[ASSET_NAME] = build_worker_bundle.csv_bytes(
        ASSET_HEADER,
        proposed_assets,
    )
    proposed_bytes[REVIEW_HISTORY_NAME] = _append_jsonl(
        original_bytes[REVIEW_HISTORY_NAME],
        [event],
    )
    if proposal_path.read_bytes() != proposal_bytes:
        raise MergeError("CANDIDATE_REVISION proposal changed during validation")
    (
        original_bytes,
        original_modes,
        proposed_bytes,
        validation_token,
    ) = _freeze_plan_state(
        original_bytes,
        original_modes,
        proposed_bytes,
    )
    return CandidateRevisionPlan(
        proposal=proposal_path,
        goal_dir=goal_dir,
        coordinator_id=proposal["coordinator_id"],
        epoch=epoch,
        source_paths=source_paths,
        review_ids=(event["review_id"],),
        candidate_update_count=(
            len(proposal["candidate_updates"]) - len(appended_candidates)
        ),
        candidate_append_count=len(appended_candidates),
        reading_update_count=len(proposal["reading_updates"]),
        asset_update_count=len(proposal["asset_updates"]),
        original_bytes=original_bytes,
        original_modes=original_modes,
        proposed_bytes=proposed_bytes,
        validation_token=validation_token,
    )


def _assert_snapshot_unchanged(
    plan: Plan,
) -> None:
    for name, expected in plan.original_bytes.items():
        path = plan.goal_dir / name
        if (
            not path.is_file()
            or path.is_symlink()
            or path.read_bytes() != expected
            or (path.stat().st_mode & 0o777) != plan.original_modes[name]
        ):
            raise MergeError(f"global audit state changed concurrently: {name}")


def _assert_plan_integrity(plan: Plan) -> None:
    """Reject any plan whose frozen, validated state was replaced or changed."""

    for label, values in (
        ("original_bytes", plan.original_bytes),
        ("original_modes", plan.original_modes),
        ("proposed_bytes", plan.proposed_bytes),
    ):
        if not isinstance(values, MappingProxyType):
            raise MergeError(f"prepared plan {label} map is not frozen")
    current_token = _plan_validation_token(
        plan.original_bytes,
        plan.original_modes,
        plan.proposed_bytes,
    )
    if current_token != plan.validation_token:
        raise MergeError("prepared plan validation token mismatch")


def apply_merge(plan: Plan) -> None:
    """Commit a validated plan through the shared durable transaction."""

    _assert_plan_integrity(plan)
    _assert_snapshot_unchanged(plan)
    try:
        audit_transaction.apply_transaction(
            plan.goal_dir,
            {
                name: plan.original_bytes[name]
                for name in audit_transaction.ARTIFACT_NAMES
            },
            {
                name: plan.proposed_bytes[name]
                for name in audit_transaction.ARTIFACT_NAMES
            },
            {
                name: plan.original_modes[name]
                for name in audit_transaction.ARTIFACT_NAMES
            },
        )
    except audit_transaction.TransactionError as exc:
        raise MergeError(str(exc)) from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "bundle",
        type=Path,
        nargs="?",
        help="sealed sequential-review worker bundle",
    )
    parser.add_argument(
        "--search-append",
        type=Path,
        help="closed SEARCH_APPEND coordinator proposal JSON",
    )
    parser.add_argument(
        "--route-resolution",
        type=Path,
        help="closed ROUTE_RESOLUTION coordinator proposal JSON",
    )
    parser.add_argument(
        "--candidate-revision",
        type=Path,
        help="closed CANDIDATE_REVISION coordinator proposal JSON",
    )
    parser.add_argument("--goal-dir", type=Path, default=GOAL_DIR)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="commit the validated proposal through a durable transaction",
    )
    parser.add_argument(
        "--recover",
        action="store_true",
        help="exclusively recover or retire a pending durable transaction",
    )
    args = parser.parse_args()
    try:
        proposal_inputs = [
            args.bundle,
            args.search_append,
            args.route_resolution,
            args.candidate_revision,
        ]
        if args.recover:
            if any(value is not None for value in proposal_inputs) or args.apply:
                raise MergeError(
                    "--recover cannot be combined with a proposal or --apply"
                )
            try:
                result = audit_transaction.recover_transaction(args.goal_dir)
            except audit_transaction.TransactionError as exc:
                raise MergeError(str(exc)) from exc
            print(
                json.dumps(
                    {
                        "mode": "recovered",
                        "action": result.action,
                        "transaction_id": result.transaction_id,
                        "journal_state": result.journal_state,
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0
        if sum(value is not None for value in proposal_inputs) != 1:
            raise MergeError(
                "provide exactly one worker bundle, --search-append, "
                "--route-resolution, or --candidate-revision proposal"
            )
        plan: Plan
        if args.search_append is not None:
            plan = prepare_search_append(
                args.search_append,
                goal_dir=args.goal_dir,
            )
        elif args.route_resolution is not None:
            plan = prepare_route_resolution(
                args.route_resolution,
                goal_dir=args.goal_dir,
            )
        elif args.candidate_revision is not None:
            plan = prepare_candidate_revision(
                args.candidate_revision,
                goal_dir=args.goal_dir,
            )
        else:
            bundle = args.bundle
            if bundle is None:
                raise MergeError("worker bundle input is missing")
            plan = prepare_merge(bundle, goal_dir=args.goal_dir)
        if args.apply:
            apply_merge(plan)
        summary = plan.preview()
        summary["mode"] = "applied" if args.apply else "dry-run"
        print(json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False))
        return 0
    except (MergeError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"merge failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
