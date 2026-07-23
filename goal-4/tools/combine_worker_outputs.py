#!/usr/bin/env python3
"""Combine completed disjoint blind-worker bundles into one union bundle.

The combiner is deliberately semantic-neutral.  It does not decide that two
worker candidates are identical.  Every input candidate remains distinct, and
all worker-local identifiers are reallocated from the union assignment's
frozen discovery-anchor traversal.

Only the pristine scaffold of the union bundle may be replaced.  Completed
input bundles and the proposed union output are verified with the existing
bundle verifier, and the written output deliberately retains
``prohibited_input_nonuse=false`` for the separate declaration gate.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import stat
import sys
from contextlib import ExitStack
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import audit_transaction
import build_worker_bundle
import prepare_review_output
from audit_contract import (
    ASSET_HEADER,
    CANDIDATE_FIELDS,
    FINGERPRINT_FIELDS,
    GOAL_DIR,
    READING_HEADER,
    canonical_json_bytes,
)


LOCAL_CANDIDATE_RE = re.compile(r"^W[0-9]{4}$")
GLOBAL_CANDIDATE_RE = re.compile(r"^B[0-9]{4}$")
LOCAL_ROUTE_RE = re.compile(r"^WR[0-9]{4}$")
GLOBAL_ROUTE_RE = re.compile(r"^R[0-9]{6}$")
LOCAL_EVIDENCE_RE = re.compile(r"^WE[0-9]{6}$")
LOCAL_EVIDENCE_GROUP_RE = re.compile(r"^WG[0-9]{6}$")


class CombineError(ValueError):
    """The sealed inputs cannot safely produce the requested union output."""


@dataclass(frozen=True)
class BundleSnapshot:
    """Validated bundle data and the bytes that must remain stable."""

    path: Path
    manifest: dict[str, Any]
    reading: list[dict[str, str]]
    assets: list[dict[str, str]]
    output: dict[str, Any]
    tracked_bytes: dict[str, bytes]


@dataclass(frozen=True)
class CombineSummary:
    """Counts from one successful atomic union authoring operation."""

    sub_bundle_count: int
    reading_count: int
    asset_count: int
    candidate_count: int
    evidence_count: int
    evidence_group_count: int
    route_count: int


def _regular_directory(path: Path, label: str) -> Path:
    if path.is_symlink():
        raise CombineError(f"{label} cannot be a symlink: {path}")
    try:
        resolved = path.resolve(strict=True)
        mode = resolved.stat(follow_symlinks=False).st_mode
    except OSError as exc:
        raise CombineError(f"cannot inspect {label}: {path}: {exc}") from exc
    if not stat.S_ISDIR(mode):
        raise CombineError(f"{label} is not a directory: {resolved}")
    return resolved


def _tracked_paths(bundle: Path) -> dict[str, Path]:
    return {
        "manifest": bundle / "allowed-manifest.json",
        "reading": bundle / "input" / "reading-input.csv",
        "assets": bundle / "input" / "asset-input.csv",
        "output": bundle / "output" / "output.json",
    }


def _read_tracked_bytes(bundle: Path) -> dict[str, bytes]:
    try:
        return {
            label: path.read_bytes()
            for label, path in _tracked_paths(bundle).items()
        }
    except OSError as exc:
        raise CombineError(f"cannot snapshot bundle {bundle}: {exc}") from exc


def _load_snapshot(bundle: Path) -> BundleSnapshot:
    tracked = _read_tracked_bytes(bundle)
    try:
        manifest = json.loads(tracked["manifest"])
        output = json.loads(tracked["output"])
    except json.JSONDecodeError as exc:
        raise CombineError(f"bundle JSON is malformed at {bundle}: {exc}") from exc
    if not isinstance(manifest, dict):
        raise CombineError(f"bundle manifest is not an object: {bundle}")
    if not isinstance(output, dict):
        raise CombineError(f"bundle output is not an object: {bundle}")
    reading = prepare_review_output.load_csv_exact(
        bundle / "input" / "reading-input.csv",
        READING_HEADER,
        f"{bundle} reading input",
    )
    assets = prepare_review_output.load_csv_exact(
        bundle / "input" / "asset-input.csv",
        ASSET_HEADER,
        f"{bundle} asset input",
    )
    return BundleSnapshot(
        path=bundle,
        manifest=manifest,
        reading=reading,
        assets=assets,
        output=output,
        tracked_bytes=tracked,
    )


def _verify_bundle(
    bundle: Path,
    *,
    goal_dir: Path,
    completed: bool,
    override: dict[str, Any] | None = None,
) -> None:
    errors = build_worker_bundle.verify_bundle(
        bundle,
        require_completed_output=completed,
        goal_dir=goal_dir,
        worker_output_override=override,
    )
    if errors:
        raise CombineError(
            f"bundle verification failed for {bundle}:\n- "
            + "\n- ".join(errors)
        )


def _require_string_array(value: object, label: str) -> list[str]:
    if (
        not isinstance(value, list)
        or not all(isinstance(item, str) for item in value)
        or len(value) != len(set(value))
    ):
        raise CombineError(f"{label} must be an array of unique strings")
    return list(value)


def _parse_csv_links(value: object, label: str) -> list[str]:
    if not isinstance(value, str):
        raise CombineError(f"{label} must be a JSON string array")
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise CombineError(f"{label} is not valid JSON") from exc
    return _require_string_array(parsed, label)


def _positive_integer(value: object, label: str) -> int:
    if isinstance(value, int) and not isinstance(value, bool) and value >= 1:
        return value
    raise CombineError(f"{label} must be a positive integer")


def _canonical_positive_text(value: object, label: str) -> int:
    if (
        isinstance(value, str)
        and re.fullmatch(r"[1-9][0-9]*", value)
    ):
        return int(value)
    raise CombineError(f"{label} must be a canonical positive integer string")


def _anchor_key(
    anchor: object,
    *,
    label: str,
    epoch: int,
    unit_order: dict[str, int],
    image_order: dict[str, int],
) -> tuple[int, int, int]:
    if not isinstance(anchor, dict):
        raise CombineError(f"{label} lacks a discovery anchor")
    anchor_epoch = _positive_integer(anchor.get("epoch"), f"{label}.epoch")
    if anchor_epoch != epoch:
        raise CombineError(
            f"{label} epoch {anchor_epoch} differs from union epoch {epoch}"
        )
    kind = anchor.get("kind")
    anchor_id = anchor.get("id")
    if not isinstance(anchor_id, str):
        raise CombineError(f"{label}.id must be a string")
    if kind == "SOURCE_UNIT":
        order = unit_order.get(anchor_id)
    elif kind == "IMAGE":
        order = image_order.get(anchor_id)
    else:
        raise CombineError(
            f"{label} must use a SOURCE_UNIT or IMAGE anchor, not {kind!r}"
        )
    if order is None:
        raise CombineError(f"{label} anchor is outside the union assignment")
    ordinal = _positive_integer(anchor.get("ordinal"), f"{label}.ordinal")
    return (anchor_epoch, order, ordinal)


def _route_anchor_key(
    route: dict[str, str],
    *,
    label: str,
    epoch: int,
    unit_order: dict[str, int],
    asset_order: dict[str, int],
) -> tuple[int, int, int]:
    route_epoch = _canonical_positive_text(
        route.get("discovery_epoch"),
        f"{label}.discovery_epoch",
    )
    if route_epoch != epoch:
        raise CombineError(
            f"{label} epoch {route_epoch} differs from union epoch {epoch}"
        )
    kind = route.get("discovery_kind")
    discovery_id = route.get("discovery_id")
    if kind == "SOURCE_UNIT":
        order = unit_order.get(discovery_id)
    elif kind == "IMAGE":
        order = asset_order.get(discovery_id)
    else:
        raise CombineError(
            f"{label} must use a SOURCE_UNIT or IMAGE anchor, not {kind!r}"
        )
    if order is None:
        raise CombineError(f"{label} anchor is outside the union assignment")
    ordinal = _canonical_positive_text(
        route.get("discovery_ordinal"),
        f"{label}.discovery_ordinal",
    )
    return (route_epoch, order, ordinal)


def _unique_anchor_keys(
    entries: list[tuple[tuple[int, int, int], Any]],
    label: str,
) -> None:
    seen: set[tuple[int, int, int]] = set()
    for key, _ in entries:
        if key in seen:
            raise CombineError(f"{label} discovery-anchor key is duplicated: {key}")
        seen.add(key)


def _map_required(
    value: object,
    *,
    origin: int,
    mapping: dict[tuple[int, str], str],
    pattern: re.Pattern[str],
    label: str,
) -> str:
    if not isinstance(value, str) or not pattern.fullmatch(value):
        raise CombineError(f"{label} is not a valid local identifier: {value!r}")
    result = mapping.get((origin, value))
    if result is None:
        raise CombineError(f"{label} refers to an undeclared local identifier")
    return result


def _map_required_array(
    value: object,
    *,
    origin: int,
    mapping: dict[tuple[int, str], str],
    pattern: re.Pattern[str],
    label: str,
) -> list[str]:
    values = _require_string_array(value, label)
    return [
        _map_required(
            item,
            origin=origin,
            mapping=mapping,
            pattern=pattern,
            label=label,
        )
        for item in values
    ]


def _rewrite_csv_links(
    value: object,
    *,
    origin: int,
    local_mapping: dict[tuple[int, str], str],
    local_pattern: re.Pattern[str],
    global_pattern: re.Pattern[str],
    label: str,
) -> str:
    rewritten: list[str] = []
    for item in _parse_csv_links(value, label):
        if local_pattern.fullmatch(item):
            mapped = local_mapping.get((origin, item))
            if mapped is None:
                raise CombineError(
                    f"{label} refers to an undeclared local identifier {item}"
                )
            rewritten.append(mapped)
        elif global_pattern.fullmatch(item):
            rewritten.append(item)
        else:
            raise CombineError(f"{label} contains an invalid identifier {item}")
    if len(rewritten) != len(set(rewritten)):
        raise CombineError(f"{label} rewriting creates duplicate identifiers")
    return json.dumps(rewritten, ensure_ascii=False, separators=(",", ":"))


def _rewrite_candidate(
    source: dict[str, Any],
    *,
    origin: int,
    candidate_map: dict[tuple[int, str], str],
    evidence_map: dict[tuple[int, str], str],
    group_map: dict[tuple[int, str], str],
    route_map: dict[tuple[int, str], str],
) -> dict[str, Any]:
    if set(source) != set(CANDIDATE_FIELDS):
        raise CombineError("candidate fields differ from the frozen contract")
    candidate = deepcopy(source)
    local_id = source.get("id")
    candidate["id"] = _map_required(
        local_id,
        origin=origin,
        mapping=candidate_map,
        pattern=LOCAL_CANDIDATE_RE,
        label="candidate.id",
    )
    if source.get("record_status") != "ACTIVE":
        raise CombineError(f"input candidate {local_id} is not ACTIVE")
    if source.get("evidence_reassignments") != []:
        raise CombineError(
            f"input candidate {local_id} contains coordinator-owned "
            "evidence reassignments"
        )

    evidence_rows = source.get("source_evidence")
    if not isinstance(evidence_rows, list):
        raise CombineError(f"candidate {local_id}.source_evidence is not an array")
    rewritten_evidence: list[dict[str, Any]] = []
    for item in evidence_rows:
        if not isinstance(item, dict):
            raise CombineError(f"candidate {local_id} has non-object evidence")
        rewritten = deepcopy(item)
        rewritten["evidence_id"] = _map_required(
            item.get("evidence_id"),
            origin=origin,
            mapping=evidence_map,
            pattern=LOCAL_EVIDENCE_RE,
            label=f"candidate {local_id}.evidence_id",
        )
        rewritten["evidence_group_id"] = _map_required(
            item.get("evidence_group_id"),
            origin=origin,
            mapping=group_map,
            pattern=LOCAL_EVIDENCE_GROUP_RE,
            label=f"candidate {local_id}.evidence_group_id",
        )
        rewritten_evidence.append(rewritten)
    rewritten_evidence.sort(key=lambda item: int(item["evidence_id"][2:]))
    candidate["source_evidence"] = rewritten_evidence

    fingerprint = source.get("fingerprint")
    if not isinstance(fingerprint, dict) or set(fingerprint) != set(
        FINGERPRINT_FIELDS
    ):
        raise CombineError(f"candidate {local_id} has an incomplete fingerprint")
    rewritten_fingerprint: dict[str, Any] = {}
    for field in FINGERPRINT_FIELDS:
        record = fingerprint[field]
        if not isinstance(record, dict):
            raise CombineError(f"candidate {local_id}.{field} is not an object")
        rewritten = deepcopy(record)
        rewritten["evidence_ids"] = _map_required_array(
            record.get("evidence_ids"),
            origin=origin,
            mapping=evidence_map,
            pattern=LOCAL_EVIDENCE_RE,
            label=f"candidate {local_id}.{field}.evidence_ids",
        )
        rewritten_fingerprint[field] = rewritten
    candidate["fingerprint"] = rewritten_fingerprint

    field_support = source.get("field_support")
    if not isinstance(field_support, dict) or set(field_support) != set(
        FINGERPRINT_FIELDS
    ):
        raise CombineError(f"candidate {local_id} has incomplete field_support")
    candidate["field_support"] = {
        field: field_support[field] for field in FINGERPRINT_FIELDS
    }

    for collection_name in ("parameters", "variants"):
        source_collection = source.get(collection_name)
        if not isinstance(source_collection, list):
            raise CombineError(
                f"candidate {local_id}.{collection_name} is not an array"
            )
        rewritten_collection: list[dict[str, Any]] = []
        for item in source_collection:
            if not isinstance(item, dict):
                raise CombineError(
                    f"candidate {local_id}.{collection_name} has a non-object item"
                )
            rewritten = deepcopy(item)
            rewritten["evidence_ids"] = _map_required_array(
                item.get("evidence_ids"),
                origin=origin,
                mapping=evidence_map,
                pattern=LOCAL_EVIDENCE_RE,
                label=f"candidate {local_id}.{collection_name}.evidence_ids",
            )
            rewritten_collection.append(rewritten)
        candidate[collection_name] = rewritten_collection

    relations = source.get("related_candidate_ids")
    if not isinstance(relations, list):
        raise CombineError(
            f"candidate {local_id}.related_candidate_ids is not an array"
        )
    rewritten_relations: list[dict[str, Any]] = []
    for item in relations:
        if not isinstance(item, dict):
            raise CombineError(f"candidate {local_id} has a non-object relation")
        rewritten = deepcopy(item)
        rewritten["candidate_id"] = _map_required(
            item.get("candidate_id"),
            origin=origin,
            mapping=candidate_map,
            pattern=LOCAL_CANDIDATE_RE,
            label=f"candidate {local_id}.related_candidate_ids.candidate_id",
        )
        rewritten["evidence_ids"] = _map_required_array(
            item.get("evidence_ids"),
            origin=origin,
            mapping=evidence_map,
            pattern=LOCAL_EVIDENCE_RE,
            label=f"candidate {local_id}.related_candidate_ids.evidence_ids",
        )
        rewritten_relations.append(rewritten)
    candidate["related_candidate_ids"] = rewritten_relations

    candidate["cross_reference_ids"] = _map_required_array(
        source.get("cross_reference_ids"),
        origin=origin,
        mapping=route_map,
        pattern=LOCAL_ROUTE_RE,
        label=f"candidate {local_id}.cross_reference_ids",
    )
    candidate["evidence_reassignments"] = []
    return {field: candidate[field] for field in CANDIDATE_FIELDS}


def _manifest_paths(manifest: dict[str, Any], label: str) -> list[str]:
    paths = manifest.get("source_paths")
    if (
        not isinstance(paths, list)
        or not paths
        or not all(isinstance(item, str) and item for item in paths)
        or len(paths) != len(set(paths))
    ):
        raise CombineError(f"{label} source_paths is not a nonempty unique array")
    return list(paths)


def _allocate_and_rewrite(
    sub_snapshots: list[BundleSnapshot],
    combined: BundleSnapshot,
) -> tuple[dict[str, Any], CombineSummary]:
    manifest = combined.manifest
    stage = manifest.get("stage")
    epoch = manifest.get("discovery_epoch")
    if not isinstance(stage, int) or isinstance(stage, bool):
        raise CombineError("union manifest stage is invalid")
    if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 1:
        raise CombineError("union manifest discovery_epoch is invalid")
    union_paths = _manifest_paths(manifest, "union manifest")

    flattened_paths: list[str] = []
    flattened_reading: list[dict[str, str]] = []
    flattened_assets: list[dict[str, str]] = []
    for index, snapshot in enumerate(sub_snapshots):
        if snapshot.manifest.get("stage") != stage:
            raise CombineError(f"sub-bundle {index} stage differs from union")
        if snapshot.manifest.get("discovery_epoch") != epoch:
            raise CombineError(f"sub-bundle {index} epoch differs from union")
        flattened_paths.extend(
            _manifest_paths(snapshot.manifest, f"sub-bundle {index} manifest")
        )
        flattened_reading.extend(snapshot.reading)
        flattened_assets.extend(snapshot.assets)
    if flattened_paths != union_paths:
        raise CombineError(
            "sub-bundle source paths are not an exact ordered partition "
            "of the union assignment"
        )
    if len(flattened_paths) != len(set(flattened_paths)):
        raise CombineError("sub-bundle source path assignments overlap")
    if flattened_reading != combined.reading:
        raise CombineError(
            "sub-bundle reading inputs are not the exact ordered union projection"
        )
    if flattened_assets != combined.assets:
        raise CombineError(
            "sub-bundle asset inputs are not the exact ordered union projection"
        )

    assigned_units = {
        row["source_unit_id"]: row for row in combined.reading
    }
    assigned_assets = {
        row["asset_id"]: row for row in combined.assets
    }
    if len(assigned_units) != len(combined.reading):
        raise CombineError("union reading assignment has duplicate source-unit IDs")
    if len(assigned_assets) != len(combined.assets):
        raise CombineError("union asset assignment has duplicate asset IDs")
    unit_order, asset_order, image_order = (
        build_worker_bundle.discovery_anchor_orders(
            assigned_units,
            assigned_assets,
        )
    )

    candidate_entries: list[
        tuple[tuple[int, int, int], tuple[int, str], dict[str, Any]]
    ] = []
    evidence_entries: list[
        tuple[tuple[int, int, int], tuple[int, str], tuple[int, str]]
    ] = []
    route_entries: list[
        tuple[tuple[int, int, int], tuple[int, str], dict[str, str]]
    ] = []
    for origin, snapshot in enumerate(sub_snapshots):
        candidates = snapshot.output.get("candidate_proposals")
        routes = snapshot.output.get("route_proposals")
        if not isinstance(candidates, list) or not all(
            isinstance(item, dict) for item in candidates
        ):
            raise CombineError(f"sub-bundle {origin} candidates are malformed")
        if not isinstance(routes, list) or not all(
            isinstance(item, dict) for item in routes
        ):
            raise CombineError(f"sub-bundle {origin} routes are malformed")
        for candidate in candidates:
            local_id = candidate.get("id")
            if not isinstance(local_id, str) or not LOCAL_CANDIDATE_RE.fullmatch(
                local_id
            ):
                raise CombineError(
                    f"sub-bundle {origin} has an invalid candidate ID"
                )
            candidate_key = _anchor_key(
                candidate.get("discovery_anchor"),
                label=f"sub-bundle {origin} candidate {local_id}",
                epoch=epoch,
                unit_order=unit_order,
                image_order=image_order,
            )
            candidate_entries.append(
                (candidate_key, (origin, local_id), candidate)
            )
            evidence = candidate.get("source_evidence")
            if not isinstance(evidence, list):
                raise CombineError(
                    f"sub-bundle {origin} candidate {local_id} evidence is malformed"
                )
            for record in evidence:
                if not isinstance(record, dict):
                    raise CombineError(
                        f"sub-bundle {origin} candidate {local_id} has "
                        "non-object evidence"
                    )
                evidence_id = record.get("evidence_id")
                group_id = record.get("evidence_group_id")
                if (
                    not isinstance(evidence_id, str)
                    or not LOCAL_EVIDENCE_RE.fullmatch(evidence_id)
                    or not isinstance(group_id, str)
                    or not LOCAL_EVIDENCE_GROUP_RE.fullmatch(group_id)
                ):
                    raise CombineError(
                        f"sub-bundle {origin} candidate {local_id} has invalid "
                        "evidence identifiers"
                    )
                evidence_key = _anchor_key(
                    record.get("discovery_anchor"),
                    label=(
                        f"sub-bundle {origin} candidate {local_id} "
                        f"evidence {evidence_id}"
                    ),
                    epoch=epoch,
                    unit_order=unit_order,
                    image_order=image_order,
                )
                evidence_entries.append(
                    (
                        evidence_key,
                        (origin, evidence_id),
                        (origin, group_id),
                    )
                )
        for route in routes:
            local_id = route.get("route_id")
            if not isinstance(local_id, str) or not LOCAL_ROUTE_RE.fullmatch(
                local_id
            ):
                raise CombineError(f"sub-bundle {origin} has an invalid route ID")
            route_key = _route_anchor_key(
                route,
                label=f"sub-bundle {origin} route {local_id}",
                epoch=epoch,
                unit_order=unit_order,
                asset_order=asset_order,
            )
            route_entries.append((route_key, (origin, local_id), route))

    _unique_anchor_keys(
        [(key, local) for key, local, _ in candidate_entries],
        "candidate",
    )
    _unique_anchor_keys(
        [(key, local) for key, local, _ in evidence_entries],
        "evidence",
    )
    _unique_anchor_keys(
        [(key, local) for key, local, _ in route_entries],
        "route",
    )
    candidate_entries.sort(key=lambda item: item[0])
    evidence_entries.sort(key=lambda item: item[0])
    route_entries.sort(key=lambda item: item[0])

    candidate_map = {
        local: f"W{index:04d}"
        for index, (_, local, _) in enumerate(candidate_entries, 1)
    }
    evidence_map = {
        local: f"WE{index:06d}"
        for index, (_, local, _) in enumerate(evidence_entries, 1)
    }
    group_map: dict[tuple[int, str], str] = {}
    for _, _, group in evidence_entries:
        if group not in group_map:
            group_map[group] = f"WG{len(group_map) + 1:06d}"
    route_map = {
        local: f"WR{index:04d}"
        for index, (_, local, _) in enumerate(route_entries, 1)
    }
    if len(candidate_map) != len(candidate_entries):
        raise CombineError("candidate IDs collide across a sub-bundle")
    if len(evidence_map) != len(evidence_entries):
        raise CombineError("evidence IDs collide across a sub-bundle")
    if len(route_map) != len(route_entries):
        raise CombineError("route IDs collide across a sub-bundle")

    rewritten_candidates = [
        _rewrite_candidate(
            candidate,
            origin=origin,
            candidate_map=candidate_map,
            evidence_map=evidence_map,
            group_map=group_map,
            route_map=route_map,
        )
        for _, (origin, _), candidate in candidate_entries
    ]

    rewritten_routes: list[dict[str, str]] = []
    for _, (origin, local_id), route in route_entries:
        rewritten = deepcopy(route)
        rewritten["route_id"] = route_map[(origin, local_id)]
        rewritten_routes.append(rewritten)

    combined_worker = manifest.get("worker_id")
    if not isinstance(combined_worker, str) or not combined_worker:
        raise CombineError("union manifest worker_id is invalid")
    rewritten_reading: list[dict[str, str]] = []
    rewritten_assets: list[dict[str, str]] = []
    for origin, snapshot in enumerate(sub_snapshots):
        reading_updates = snapshot.output.get("reading_updates")
        asset_updates = snapshot.output.get("asset_updates")
        if not isinstance(reading_updates, list) or not all(
            isinstance(item, dict) for item in reading_updates
        ):
            raise CombineError(f"sub-bundle {origin} reading updates are malformed")
        if not isinstance(asset_updates, list) or not all(
            isinstance(item, dict) for item in asset_updates
        ):
            raise CombineError(f"sub-bundle {origin} asset updates are malformed")
        if [
            row.get("source_unit_id") for row in reading_updates
        ] != [
            row["source_unit_id"] for row in snapshot.reading
        ]:
            raise CombineError(
                f"sub-bundle {origin} reading update order differs from its input"
            )
        if [
            row.get("asset_id") for row in asset_updates
        ] != [
            row["asset_id"] for row in snapshot.assets
        ]:
            raise CombineError(
                f"sub-bundle {origin} asset update order differs from its input"
            )
        for source in reading_updates:
            row = deepcopy(source)
            row["candidate_ids"] = _rewrite_csv_links(
                source.get("candidate_ids"),
                origin=origin,
                local_mapping=candidate_map,
                local_pattern=LOCAL_CANDIDATE_RE,
                global_pattern=GLOBAL_CANDIDATE_RE,
                label=(
                    f"sub-bundle {origin} reading "
                    f"{source.get('source_unit_id')}.candidate_ids"
                ),
            )
            row["route_ids"] = _rewrite_csv_links(
                source.get("route_ids"),
                origin=origin,
                local_mapping=route_map,
                local_pattern=LOCAL_ROUTE_RE,
                global_pattern=GLOBAL_ROUTE_RE,
                label=(
                    f"sub-bundle {origin} reading "
                    f"{source.get('source_unit_id')}.route_ids"
                ),
            )
            row["review_stage"] = str(stage)
            row["reviewer"] = combined_worker
            rewritten_reading.append(
                {field: row[field] for field in READING_HEADER}
            )
        for source in asset_updates:
            row = deepcopy(source)
            row["candidate_ids"] = _rewrite_csv_links(
                source.get("candidate_ids"),
                origin=origin,
                local_mapping=candidate_map,
                local_pattern=LOCAL_CANDIDATE_RE,
                global_pattern=GLOBAL_CANDIDATE_RE,
                label=(
                    f"sub-bundle {origin} asset "
                    f"{source.get('asset_id')}.candidate_ids"
                ),
            )
            row["route_ids"] = _rewrite_csv_links(
                source.get("route_ids"),
                origin=origin,
                local_mapping=route_map,
                local_pattern=LOCAL_ROUTE_RE,
                global_pattern=GLOBAL_ROUTE_RE,
                label=(
                    f"sub-bundle {origin} asset "
                    f"{source.get('asset_id')}.route_ids"
                ),
            )
            row["review_stage"] = str(stage)
            row["reviewer"] = combined_worker
            rewritten_assets.append(
                {field: row[field] for field in ASSET_HEADER}
            )

    uncertainties: list[str] = []
    for origin, snapshot in enumerate(sub_snapshots):
        values = snapshot.output.get("uncertainties")
        for value in _require_string_array(
            values,
            f"sub-bundle {origin}.uncertainties",
        ):
            if value not in uncertainties:
                uncertainties.append(value)

    template = prepare_review_output.expected_template(
        combined.path,
        manifest,
    )
    proposed = deepcopy(template)
    proposed.update(
        {
            "prohibited_input_nonuse": False,
            "reading_updates": rewritten_reading,
            "candidate_proposals": rewritten_candidates,
            "asset_updates": rewritten_assets,
            "route_proposals": rewritten_routes,
            "uncertainties": uncertainties,
        }
    )
    summary = CombineSummary(
        sub_bundle_count=len(sub_snapshots),
        reading_count=len(rewritten_reading),
        asset_count=len(rewritten_assets),
        candidate_count=len(rewritten_candidates),
        evidence_count=len(evidence_map),
        evidence_group_count=len(group_map),
        route_count=len(rewritten_routes),
    )
    return proposed, summary


def _snapshot_unchanged(snapshot: BundleSnapshot) -> None:
    current = _read_tracked_bytes(snapshot.path)
    if current != snapshot.tracked_bytes:
        raise CombineError(f"bundle changed during combination: {snapshot.path}")


def combine_worker_outputs(
    sub_bundles: list[Path],
    combined_bundle: Path,
    *,
    goal_dir: Path = GOAL_DIR,
) -> CombineSummary:
    """Atomically author one union output from two or more completed bundles."""

    if len(sub_bundles) < 2:
        raise CombineError("at least two completed sub-bundles are required")
    raw_paths = [combined_bundle, *sub_bundles]
    resolved = [
        _regular_directory(
            path,
            "combined bundle" if index == 0 else f"sub-bundle {index}",
        )
        for index, path in enumerate(raw_paths)
    ]
    combined = resolved[0]
    subs = resolved[1:]
    if len(resolved) != len(set(resolved)):
        raise CombineError("combined and sub-bundle paths must be distinct")

    goal = _regular_directory(goal_dir, "Goal 4 directory")
    with ExitStack() as stack:
        for bundle in sorted(resolved, key=lambda path: str(path)):
            stack.enter_context(prepare_review_output.output_lock(bundle))
        try:
            stack.enter_context(audit_transaction.read_guard(goal))
        except audit_transaction.TransactionError as exc:
            raise CombineError(str(exc)) from exc

        sub_snapshots: list[BundleSnapshot] = []
        for bundle in subs:
            _verify_bundle(
                bundle,
                goal_dir=goal,
                completed=True,
            )
            snapshot = _load_snapshot(bundle)
            if snapshot.output.get("prohibited_input_nonuse") is not True:
                raise CombineError(
                    f"sub-bundle is not declaration-complete: {bundle}"
                )
            sub_snapshots.append(snapshot)

        combined_snapshot = _load_snapshot(combined)
        template = prepare_review_output.expected_template(
            combined,
            combined_snapshot.manifest,
        )
        _verify_bundle(
            combined,
            goal_dir=goal,
            completed=False,
            override=template,
        )
        scaffold = prepare_review_output.scaffold_output(
            template,
            combined_snapshot.reading,
            combined_snapshot.assets,
        )
        if combined_snapshot.output != scaffold:
            raise CombineError(
                "combined output is not the exact pristine nonsemantic scaffold"
            )

        proposed, summary = _allocate_and_rewrite(
            sub_snapshots,
            combined_snapshot,
        )
        completed_override = deepcopy(proposed)
        completed_override["prohibited_input_nonuse"] = True
        _verify_bundle(
            combined,
            goal_dir=goal,
            completed=True,
            override=completed_override,
        )

        for snapshot in sub_snapshots:
            _verify_bundle(
                snapshot.path,
                goal_dir=goal,
                completed=True,
            )
            _snapshot_unchanged(snapshot)
        _snapshot_unchanged(combined_snapshot)

        prepare_review_output.atomic_replace(
            combined / "output" / "output.json",
            canonical_json_bytes(proposed),
            combined_snapshot.tracked_bytes["output"],
        )
        return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Combine completed disjoint sealed worker bundles into a pristine "
            "sealed union bundle."
        )
    )
    parser.add_argument("combined_bundle", type=Path)
    parser.add_argument("sub_bundles", nargs="+", type=Path)
    parser.add_argument(
        "--goal-dir",
        type=Path,
        default=GOAL_DIR,
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()
    try:
        summary = combine_worker_outputs(
            args.sub_bundles,
            args.combined_bundle,
            goal_dir=args.goal_dir,
        )
    except (
        CombineError,
        prepare_review_output.PreparationError,
        audit_transaction.TransactionError,
        OSError,
        csv.Error,
        json.JSONDecodeError,
    ) as exc:
        print(f"worker-output combination failed: {exc}", file=sys.stderr)
        return 1
    print(
        "combined completed worker outputs: "
        f"sub_bundles={summary.sub_bundle_count} "
        f"reading={summary.reading_count} "
        f"assets={summary.asset_count} "
        f"candidates={summary.candidate_count} "
        f"evidence={summary.evidence_count} "
        f"groups={summary.evidence_group_count} "
        f"routes={summary.route_count} "
        "declaration=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
