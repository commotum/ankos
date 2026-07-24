#!/usr/bin/env python3
"""Author the governed Stage 10 Chapter 6 route-resolution proposal.

Routes are selected only by their immutable five-field identity:

    (source_unit_id, source_asset_id, route_kind,
     literal_target, expected_topic)

The proposal closes the exhaustive incoming route set whose literal target is
in the reviewed Chapter 6 assignment and every Stage-10 WITHIN_STAGE route.
The Stage-10 CROSS_RANGE partition is proved present and left untouched.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import sys
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import audit_transaction
import merge_worker_output
from audit_contract import (
    ASSET_HEADER,
    CROSS_REFERENCE_HEADER,
    GOAL_DIR,
    READING_HEADER,
    canonical_json_bytes,
)


IDENTITY_FIELDS = (
    "source_unit_id",
    "source_asset_id",
    "route_kind",
    "literal_target",
    "expected_topic",
)
STAGE_PATHS = (
    "CHAPTERS/06-Starting-from-Randomness.md",
    "BACK-MATTER/NOTES/06-Starting-from-Randomness-Notes.md",
)
EXPECTED_SPEC_COUNTS = {"incoming": 14, "within": 58}
EXPECTED_UPDATE_COUNT = 72
EXPECTED_UNTOUCHED_CROSS_RANGE_COUNT = 107
EXPECTED_SPEC_SHA256 = "TO_BE_COMPUTED"
UNIT_ID = re.compile(r"^U[0-9]{6}$")
ASSET_ID = re.compile(r"^A[0-9]{6}$")


class AuthoringError(ValueError):
    """The current audit state cannot safely receive this proposal."""


@dataclass(frozen=True)
class RouteSpec:
    """One source-grounded route closure."""

    origin: str
    identity: tuple[str, str, str, str, str]
    target_unit_ids: tuple[str, ...]
    target_asset_ids: tuple[str, ...]
    attempt: str


def route_spec(
    origin: str,
    source_unit_id: str,
    source_asset_id: str,
    route_kind: str,
    literal_target: str,
    expected_topic: str,
    target_unit_ids: str,
    target_asset_ids: str,
    attempt: str,
) -> RouteSpec:
    """Keep the embedded route map compact while retaining exact IDs."""

    return RouteSpec(
        origin=origin,
        identity=(
            source_unit_id,
            source_asset_id,
            route_kind,
            literal_target,
            expected_topic,
        ),
        target_unit_ids=tuple(target_unit_ids.split()),
        target_asset_ids=tuple(target_asset_ids.split()),
        attempt=attempt,
    )


ROUTE_SPECS: tuple[RouteSpec, ...] = ()


UNTOUCHED_CROSS_RANGE_IDENTITIES: tuple[
    tuple[str, str, str, str, str], ...
] = ()


def embedded_spec_payload() -> list[dict[str, Any]]:
    """Return the exact canonical projection governed by this route map."""

    return [
        {
            "origin": spec.origin,
            "identity": dict(zip(IDENTITY_FIELDS, spec.identity, strict=True)),
            "target_unit_ids": list(spec.target_unit_ids),
            "target_asset_ids": list(spec.target_asset_ids),
            "attempt": spec.attempt,
        }
        for spec in ROUTE_SPECS
    ]


def spec_sha256(payload: list[dict[str, Any]]) -> str:
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def validate_embedded_specs() -> str:
    """Fail if the checked-in governed route projection drifts."""

    origins: dict[str, int] = {}
    identities: set[tuple[str, str, str, str, str]] = set()
    for index, spec in enumerate(ROUTE_SPECS, start=1):
        origins[spec.origin] = origins.get(spec.origin, 0) + 1
        if spec.origin not in EXPECTED_SPEC_COUNTS:
            raise AuthoringError(
                f"embedded route {index} has unknown origin {spec.origin!r}"
            )
        if spec.identity in identities:
            raise AuthoringError(
                f"embedded route identity is duplicated: {spec.identity!r}"
            )
        identities.add(spec.identity)
        source_unit_id, source_asset_id, route_kind, target, topic = (
            spec.identity
        )
        if not UNIT_ID.fullmatch(source_unit_id):
            raise AuthoringError(
                f"embedded route {index} has invalid source unit"
            )
        if source_asset_id and not ASSET_ID.fullmatch(source_asset_id):
            raise AuthoringError(
                f"embedded route {index} has invalid source asset"
            )
        if route_kind not in {"PAGE", "SECTION", "OTHER"}:
            raise AuthoringError(
                f"embedded route {index} has unexpected route kind"
            )
        if not target or not topic or not spec.attempt:
            raise AuthoringError(
                f"embedded route {index} has an empty governed claim"
            )
        if not spec.target_unit_ids and not spec.target_asset_ids:
            raise AuthoringError(
                f"embedded route {index} has no governed target"
            )
        if (
            len(spec.target_unit_ids) != len(set(spec.target_unit_ids))
            or len(spec.target_asset_ids) != len(set(spec.target_asset_ids))
        ):
            raise AuthoringError(
                f"embedded route {index} repeats a target ID"
            )
        if any(
            not UNIT_ID.fullmatch(unit_id)
            for unit_id in spec.target_unit_ids
        ):
            raise AuthoringError(
                f"embedded route {index} has an invalid target unit"
            )
        if any(
            not ASSET_ID.fullmatch(asset_id)
            for asset_id in spec.target_asset_ids
        ):
            raise AuthoringError(
                f"embedded route {index} has an invalid target asset"
            )
    if origins != EXPECTED_SPEC_COUNTS:
        raise AuthoringError(f"embedded route counts drifted: {origins!r}")
    if len(ROUTE_SPECS) != EXPECTED_UPDATE_COUNT:
        raise AuthoringError("embedded route update total drifted")
    if (
        len(UNTOUCHED_CROSS_RANGE_IDENTITIES)
        != EXPECTED_UNTOUCHED_CROSS_RANGE_COUNT
        or len(set(UNTOUCHED_CROSS_RANGE_IDENTITIES))
        != EXPECTED_UNTOUCHED_CROSS_RANGE_COUNT
    ):
        raise AuthoringError("untouched CROSS_RANGE partition drifted")
    if identities & set(UNTOUCHED_CROSS_RANGE_IDENTITIES):
        raise AuthoringError(
            "an untouched CROSS_RANGE identity entered the closure map"
        )
    digest = spec_sha256(embedded_spec_payload())
    if digest != EXPECTED_SPEC_SHA256:
        raise AuthoringError(
            "embedded route-map projection digest drifted: "
            f"{digest} != {EXPECTED_SPEC_SHA256}"
        )
    return digest


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not line:
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise AuthoringError(
                f"{path.name}:{line_number} is not a JSON object"
            )
        rows.append(value)
    return rows


def read_csv_strict(
    path: Path,
    expected_header: list[str],
) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != expected_header:
            raise AuthoringError(f"{path.name} header drifted")
        rows = list(reader)
    if any(
        None in row or any(value is None for value in row.values())
        for row in rows
    ):
        raise AuthoringError(f"{path.name} contains a malformed row")
    return rows


def atomic_create(path: Path, payload: bytes) -> None:
    """Create a proposal exactly once without following symlinks."""

    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o600)
    try:
        view = memoryview(payload)
        while view:
            written = os.write(descriptor, view)
            if written <= 0:
                raise OSError("short write while creating proposal")
            view = view[written:]
        os.fsync(descriptor)
    except BaseException:
        os.close(descriptor)
        try:
            path.unlink()
        except OSError:
            pass
        raise
    else:
        os.close(descriptor)
    directory = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


def route_identity(row: dict[str, str]) -> tuple[str, str, str, str, str]:
    return tuple(row[field] for field in IDENTITY_FIELDS)  # type: ignore[return-value]


def parsed_string_list(value: str, *, label: str) -> list[str]:
    parsed = json.loads(value)
    if not isinstance(parsed, list) or not all(
        isinstance(item, str) for item in parsed
    ):
        raise AuthoringError(f"{label} is not a string array")
    return parsed


def require_reviewed_unit(
    unit_id: str,
    units: dict[str, dict[str, Any]],
    reading: dict[str, dict[str, str]],
    *,
    label: str,
) -> None:
    unit = units.get(unit_id)
    review = reading.get(unit_id)
    if unit is None or review is None:
        raise AuthoringError(f"{label} unit does not exist: {unit_id}")
    if review["review_status"] != "REVIEWED":
        raise AuthoringError(f"{label} unit is not reviewed: {unit_id}")
    if review["review_stage"] != "10":
        raise AuthoringError(
            f"{label} unit was not closed by Stage 10: {unit_id}"
        )
    if (
        unit.get("path") not in STAGE_PATHS
        or review["path"] != unit.get("path")
    ):
        raise AuthoringError(
            f"{label} unit lies outside Stage 10: {unit_id}"
        )


def require_screened_asset(
    asset_id: str,
    assets: dict[str, dict[str, str]],
    *,
    label: str,
) -> None:
    asset = assets.get(asset_id)
    if asset is None:
        raise AuthoringError(f"{label} asset does not exist: {asset_id}")
    if asset["inspection_status"] != "SCREENED":
        raise AuthoringError(f"{label} asset is not screened: {asset_id}")
    if asset["review_stage"] != "10":
        raise AuthoringError(
            f"{label} asset was not closed by Stage 10: {asset_id}"
        )
    if asset["assignment_path"] not in STAGE_PATHS:
        raise AuthoringError(
            f"{label} asset lies outside Stage 10: {asset_id}"
        )
    if asset["source_status"] != "CLEAR":
        raise AuthoringError(
            f"{label} target asset is not clear: {asset_id}"
        )
    if asset["original_resolution_status"] != "REVIEWED":
        raise AuthoringError(
            f"{label} target asset lacks original-resolution review: "
            f"{asset_id}"
        )


def require_pending_route(row: dict[str, str], *, label: str) -> None:
    if row["status"] != "PENDING":
        raise AuthoringError(f"{label} route is not PENDING")
    if row["target_unit_ids"] != "[]" or row["target_asset_ids"] != "[]":
        raise AuthoringError(f"{label} route already carries target claims")
    parsed_string_list(row["attempts"], label=f"{label} attempts")
    parsed_string_list(
        row["vocabulary_terms"],
        label=f"{label} vocabulary_terms",
    )


def build_proposal(goal_dir: Path) -> dict[str, Any]:
    """Build the exact 72-row identity-keyed Stage 10 closure proposal."""

    goal_dir = goal_dir.resolve()
    if goal_dir != GOAL_DIR.resolve():
        raise AuthoringError("this reproducer is bound to canonical Goal 4")
    validate_embedded_specs()

    routes = read_csv_strict(
        goal_dir / merge_worker_output.ROUTE_NAME,
        CROSS_REFERENCE_HEADER,
    )
    reading_rows = read_csv_strict(
        goal_dir / merge_worker_output.READING_NAME,
        READING_HEADER,
    )
    asset_rows = read_csv_strict(
        goal_dir / merge_worker_output.ASSET_NAME,
        ASSET_HEADER,
    )
    units_rows = read_jsonl(goal_dir / merge_worker_output.UNITS_NAME)
    history = read_jsonl(
        goal_dir / merge_worker_output.REVIEW_HISTORY_NAME
    )
    if not history:
        raise AuthoringError("review history is empty")
    terminal = history[-1]
    if terminal.get("review_id") != "V000027":
        raise AuthoringError("expected terminal history event V000027")
    if terminal.get("mode") != "INITIAL" or terminal.get("stage") != 10:
        raise AuthoringError(
            "expected the terminal combined Stage 10 INITIAL event"
        )
    if tuple(terminal.get("source_paths", ())) != STAGE_PATHS:
        raise AuthoringError(
            "terminal review event is not the combined Stage 10 assignment"
        )
    epoch = terminal.get("epoch")
    if epoch != 2:
        raise AuthoringError(f"expected active epoch 2, got {epoch!r}")

    units: dict[str, dict[str, Any]] = {}
    for unit in units_rows:
        unit_id = unit.get("id")
        if not isinstance(unit_id, str) or unit_id in units:
            raise AuthoringError(
                "source-units.jsonl has invalid/duplicate IDs"
            )
        units[unit_id] = unit
    reading = {row["source_unit_id"]: row for row in reading_rows}
    assets = {row["asset_id"]: row for row in asset_rows}
    if len(reading) != len(reading_rows) or len(assets) != len(asset_rows):
        raise AuthoringError("review ledgers contain duplicate identities")

    routes_by_identity: dict[
        tuple[str, str, str, str, str],
        list[dict[str, str]],
    ] = {}
    for row in routes:
        routes_by_identity.setdefault(route_identity(row), []).append(row)

    expected_within = {
        spec.identity for spec in ROUTE_SPECS if spec.origin == "within"
    }
    observed_within_rows = [
        row
        for row in routes
        if row["owning_stage"] == "10"
        and row["closure_scope"] == "WITHIN_STAGE"
    ]
    observed_within = {
        route_identity(row) for row in observed_within_rows
    }
    if (
        len(observed_within_rows) != EXPECTED_SPEC_COUNTS["within"]
        or observed_within != expected_within
    ):
        missing = sorted(expected_within - observed_within)
        extra = sorted(observed_within - expected_within)
        raise AuthoringError(
            "Stage 10 WITHIN_STAGE route set differs from the governed map: "
            f"missing={missing!r} extra={extra!r}"
        )
    for row in observed_within_rows:
        require_pending_route(row, label="Stage 10 WITHIN_STAGE")

    expected_cross = set(UNTOUCHED_CROSS_RANGE_IDENTITIES)
    observed_cross_rows = [
        row
        for row in routes
        if row["owning_stage"] == "10"
        and row["closure_scope"] == "CROSS_RANGE"
    ]
    observed_cross = {
        route_identity(row) for row in observed_cross_rows
    }
    if (
        len(observed_cross_rows) != EXPECTED_UNTOUCHED_CROSS_RANGE_COUNT
        or observed_cross != expected_cross
    ):
        missing = sorted(expected_cross - observed_cross)
        extra = sorted(observed_cross - expected_cross)
        raise AuthoringError(
            "Stage 10 CROSS_RANGE partition drifted: "
            f"missing={missing!r} extra={extra!r}"
        )
    for row in observed_cross_rows:
        require_pending_route(row, label="untouched CROSS_RANGE")

    updates: list[dict[str, str]] = []
    matched_route_ids: set[str] = set()
    origin_counts = {"incoming": 0, "within": 0}
    for spec in ROUTE_SPECS:
        matches = routes_by_identity.get(spec.identity, [])
        if len(matches) != 1:
            raise AuthoringError(
                "governed route identity did not match exactly once: "
                f"{spec.identity!r} matches={len(matches)}"
            )
        before = matches[0]
        route_id = before["route_id"]
        if route_id in matched_route_ids:
            raise AuthoringError(
                f"allocated route row matched twice: {route_id}"
            )
        matched_route_ids.add(route_id)
        require_pending_route(before, label="governed")
        if spec.origin == "within":
            if (
                before["owning_stage"] != "10"
                or before["closure_scope"] != "WITHIN_STAGE"
            ):
                raise AuthoringError(
                    "within-stage route metadata drifted: "
                    f"{spec.identity!r}"
                )
        else:
            if (
                before["owning_stage"] == "10"
                or before["closure_scope"] == "WITHIN_STAGE"
            ):
                raise AuthoringError(
                    "incoming route was reclassified as within-stage: "
                    f"{spec.identity!r}"
                )

        source_unit_id, source_asset_id, _, _, _ = spec.identity
        if source_unit_id:
            source_review = reading.get(source_unit_id)
            if (
                source_unit_id not in units
                or source_review is None
                or source_review["review_status"] != "REVIEWED"
            ):
                raise AuthoringError(
                    f"route source unit is not reviewed: {source_unit_id}"
                )
        if source_asset_id:
            source_asset = assets.get(source_asset_id)
            if (
                source_asset is None
                or source_asset["inspection_status"] != "SCREENED"
            ):
                raise AuthoringError(
                    f"route source asset is not screened: {source_asset_id}"
                )

        for unit_id in spec.target_unit_ids:
            require_reviewed_unit(
                unit_id,
                units,
                reading,
                label="target",
            )
        for asset_id in spec.target_asset_ids:
            require_screened_asset(asset_id, assets, label="target")

        prior_attempts = parsed_string_list(
            before["attempts"],
            label=f"{route_id} attempts",
        )
        prior_vocabulary = parsed_string_list(
            before["vocabulary_terms"],
            label=f"{route_id} vocabulary_terms",
        )
        if not prior_vocabulary:
            raise AuthoringError(f"{route_id} has empty route vocabulary")

        update = deepcopy(before)
        update["status"] = "RESOLVED"
        update["target_unit_ids"] = json.dumps(
            spec.target_unit_ids,
            separators=(",", ":"),
        )
        update["target_asset_ids"] = json.dumps(
            spec.target_asset_ids,
            separators=(",", ":"),
        )
        update["attempts"] = json.dumps(
            [*prior_attempts, spec.attempt],
            separators=(",", ":"),
            ensure_ascii=False,
        )
        update["vocabulary_terms"] = json.dumps(
            prior_vocabulary,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        if route_identity(update) != spec.identity:
            raise AuthoringError("route update changed its immutable identity")
        updates.append(update)
        origin_counts[spec.origin] += 1

    if (
        origin_counts != EXPECTED_SPEC_COUNTS
        or len(updates) != EXPECTED_UPDATE_COUNT
        or len(matched_route_ids) != EXPECTED_UPDATE_COUNT
    ):
        raise AuthoringError(
            f"route update counts drifted: {origin_counts!r}"
        )
    if matched_route_ids & {
        row["route_id"] for row in observed_cross_rows
    }:
        raise AuthoringError(
            "an untouched CROSS_RANGE route entered the update set"
        )

    return {
        "schema_version": 1,
        "proposal_kind": "ROUTE_RESOLUTION",
        "coordinator_id": "ch06-randomness-route-closure-e2",
        "epoch": epoch,
        "base_artifact_sha256": {
            name: hashlib.sha256((goal_dir / name).read_bytes()).hexdigest()
            for name in merge_worker_output.WRITE_NAMES
        },
        "route_updates": updates,
    }


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--check-spec":
        try:
            digest = validate_embedded_specs()
        except (OSError, json.JSONDecodeError, AuthoringError) as exc:
            print(
                f"Chapter 6 route specification check failed: {exc}",
                file=sys.stderr,
            )
            return 1
        print(
            "Chapter 6 route specification valid: "
            f"incoming=14 within=58 untouched-cross=107 sha256={digest}"
        )
        return 0

    if len(sys.argv) != 2:
        print(
            f"usage: {Path(sys.argv[0]).name} OUTPUT_JSON\n"
            f"       {Path(sys.argv[0]).name} --check-spec",
            file=sys.stderr,
        )
        return 2
    output_path = Path(sys.argv[1])
    try:
        with audit_transaction.read_guard(GOAL_DIR):
            proposal = build_proposal(GOAL_DIR)
            atomic_create(output_path, canonical_json_bytes(proposal))
    except (
        OSError,
        json.JSONDecodeError,
        AuthoringError,
        ValueError,
    ) as exc:
        print(f"Chapter 6 route authoring failed: {exc}", file=sys.stderr)
        return 1
    print(
        "authored Chapter 6 route closure: "
        f"updates={len(proposal['route_updates'])} "
        f"sha256={hashlib.sha256(canonical_json_bytes(proposal)).hexdigest()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
