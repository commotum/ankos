#!/usr/bin/env python3
"""Preview or apply one verified blind-worker output to the global audit ledgers."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import shutil
import sys
import tempfile
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import build_worker_bundle
import validate_audit
from audit_contract import (
    ASSET_HEADER,
    CANDIDATE_FIELDS,
    CROSS_REFERENCE_HEADER,
    FINGERPRINT_FIELDS,
    GOAL_DIR,
    READING_HEADER,
    REVIEW_HISTORY_FIELDS,
    canonical_sha256,
    review_event_sha256,
    review_input_projection,
    review_result_projection,
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
    original_bytes: dict[str, bytes]
    original_modes: dict[str, int]
    proposed_bytes: dict[str, bytes]

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
    evidence_ids: list[str] = []
    evidence_group_ids: list[str] = []
    seen_groups: set[str] = set()
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
            evidence_ids.append(evidence_id)
            if group_id not in seen_groups:
                seen_groups.add(group_id)
                evidence_group_ids.append(group_id)
    return candidate_ids, evidence_ids, evidence_group_ids


def _existing_evidence_sequences(
    candidates: list[dict[str, Any]],
) -> tuple[list[str], list[str]]:
    evidence_ids: list[str] = []
    group_ids: list[str] = []
    seen_groups: set[str] = set()
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
            if group_id not in seen_groups:
                seen_groups.add(group_id)
                group_ids.append(group_id)
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


def _global_max_epoch(
    reading: list[dict[str, str]],
    candidates: list[dict[str, Any]],
    routes: list[dict[str, str]],
    assets: list[dict[str, str]],
    search: dict[str, Any],
) -> int:
    epochs: list[int] = []
    for row in reading:
        value = row.get("review_epoch", "")
        if value:
            epochs.append(_positive_epoch(value, f"reading {row.get('source_unit_id')}"))
    for row in assets:
        value = row.get("review_epoch", "")
        if value:
            epochs.append(_positive_epoch(value, f"asset {row.get('asset_id')}"))
    for candidate in candidates:
        candidate_id = candidate.get("id", "<unknown>")
        anchor = candidate.get("discovery_anchor")
        if not isinstance(anchor, dict):
            raise MergeError(f"candidate {candidate_id} lacks a discovery anchor")
        epochs.append(
            _positive_epoch(
                anchor.get("epoch"),
                f"candidate {candidate_id}",
            )
        )
        evidence = candidate.get("source_evidence")
        if not isinstance(evidence, list):
            raise MergeError(f"candidate {candidate_id} has malformed evidence")
        for item in evidence:
            if not isinstance(item, dict) or not isinstance(
                item.get("discovery_anchor"),
                dict,
            ):
                raise MergeError(
                    f"candidate {candidate_id} has malformed evidence anchor"
                )
            epochs.append(
                _positive_epoch(
                    item["discovery_anchor"].get("epoch"),
                    f"candidate {candidate_id} evidence",
                )
            )
    for route in routes:
        epochs.append(
            _positive_epoch(
                route.get("discovery_epoch"),
                f"route {route.get('route_id')}",
            )
        )
    rounds = search.get("rounds")
    if not isinstance(rounds, list):
        raise MergeError("search rounds are not an array")
    for index, round_record in enumerate(rounds):
        if not isinstance(round_record, dict):
            raise MergeError(f"search round {index} is not an object")
        epochs.append(
            _positive_epoch(
                round_record.get("epoch"),
                f"search round {index}",
            )
        )
    return max(epochs, default=0)


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
    input_asset_by_id = {row["asset_id"]: row for row in assets}
    result_reading_by_id = {
        row["source_unit_id"]: row for row in proposed_reading
    }
    result_asset_by_id = {row["asset_id"]: row for row in proposed_assets}
    next_review_number = _review_sequence(review_history) + 1
    prior_event_sha256 = (
        review_history[-1]["event_sha256"] if review_history else None
    )
    review_events: list[dict[str, Any]] = []
    for offset, source_path in enumerate(source_paths):
        review_id = f"V{next_review_number + offset:06d}"
        review_event: dict[str, Any] = {
            "review_id": review_id,
            "epoch": discovery_epoch,
            "stage": stage,
            "mode": review_mode,
            "reviewer": worker_id,
            "source_paths": [source_path],
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
            "input_projection_sha256": "",
            "result_projection_sha256": "",
            "previous_event_sha256": prior_event_sha256,
            "event_sha256": "",
        }
        try:
            review_event["input_projection_sha256"] = canonical_sha256(
                review_input_projection(
                    review_event,
                    unit_by_id,
                    input_asset_by_id,
                )
            )
            review_event["result_projection_sha256"] = canonical_sha256(
                review_result_projection(
                    review_event,
                    result_reading_by_id,
                    result_asset_by_id,
                )
            )
        except KeyError as exc:
            raise MergeError(
                f"cannot bind review event {review_id} to its exact "
                f"projection: {exc}"
            ) from exc
        review_event["event_sha256"] = review_event_sha256(review_event)
        review_event = {
            field: review_event[field] for field in REVIEW_HISTORY_FIELDS
        }
        review_events.append(review_event)
        prior_event_sha256 = review_event["event_sha256"]
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
    )


def _assert_snapshot_unchanged(plan: MergePlan) -> None:
    for name, expected in plan.original_bytes.items():
        path = plan.goal_dir / name
        if not path.is_file() or path.is_symlink() or path.read_bytes() != expected:
            raise MergeError(f"global audit state changed concurrently: {name}")


def apply_merge(plan: MergePlan) -> None:
    """Commit a validated plan from same-filesystem staging files."""

    _assert_snapshot_unchanged(plan)
    stage = Path(
        tempfile.mkdtemp(
            prefix=".merge-worker-output-",
            dir=plan.goal_dir,
        )
    )
    new_root = stage / "new"
    old_root = stage / "old"
    attempted: list[str] = []
    cleanup_stage = True
    try:
        new_root.mkdir()
        old_root.mkdir()
        for name in WRITE_NAMES:
            new_path = new_root / name
            old_path = old_root / name
            new_path.write_bytes(plan.proposed_bytes[name])
            old_path.write_bytes(plan.original_bytes[name])
            mode = plan.original_modes[name]
            new_path.chmod(mode)
            old_path.chmod(mode)

        _assert_snapshot_unchanged(plan)
        for name in WRITE_NAMES:
            if (plan.goal_dir / name).read_bytes() != plan.original_bytes[name]:
                raise MergeError(f"global audit state changed concurrently: {name}")
            # Record the target before replacement.  If os.replace commits and
            # then an asynchronous exception is delivered before it returns,
            # the rollback must conservatively restore this target too.
            attempted.append(name)
            os.replace(new_root / name, plan.goal_dir / name)

        for name in SNAPSHOT_NAMES:
            path = plan.goal_dir / name
            expected = (
                plan.proposed_bytes[name]
                if name in plan.proposed_bytes
                else plan.original_bytes[name]
            )
            if (
                not path.is_file()
                or path.is_symlink()
                or path.read_bytes() != expected
            ):
                if name in plan.proposed_bytes:
                    raise MergeError(
                        f"applied ledger differs from staged bytes: {name}"
                    )
                raise MergeError(
                    f"global audit state changed concurrently: {name}"
                )
            if (path.stat().st_mode & 0o777) != plan.original_modes[name]:
                if name in plan.proposed_bytes:
                    raise MergeError(
                        f"applied ledger mode differs from staged mode: {name}"
                    )
                raise MergeError(
                    f"global audit state mode changed concurrently: {name}"
                )
    except BaseException as exc:
        rollback_errors: list[str] = []
        for name in reversed(attempted):
            try:
                os.replace(old_root / name, plan.goal_dir / name)
            except BaseException as rollback_exc:
                rollback_errors.append(
                    f"{name}: {type(rollback_exc).__name__}: {rollback_exc}"
                )
        if rollback_errors:
            cleanup_stage = False
            raise MergeError(
                f"merge failed ({exc}); rollback also failed: "
                + "; ".join(rollback_errors)
                + f"; staged recovery files remain at {stage}"
            ) from exc
        raise
    finally:
        if cleanup_stage:
            shutil.rmtree(stage, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--goal-dir", type=Path, default=GOAL_DIR)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="write the validated proposal through same-filesystem staging files",
    )
    args = parser.parse_args()
    try:
        plan = prepare_merge(args.bundle, goal_dir=args.goal_dir)
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
