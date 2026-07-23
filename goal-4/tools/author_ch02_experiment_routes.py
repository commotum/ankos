#!/usr/bin/env python3
"""Author the governed Stage 6 Chapter 2 route-resolution proposal."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

import audit_transaction
import merge_worker_output
from audit_contract import GOAL_DIR, canonical_json_bytes


ROUTE_TARGETS = {
    "R000001": {
        "units": ["U000204", "U000206", "U000207"],
        "assets": ["A001164"],
        "attempt": (
            "Resolved the printed page 27 pointer to the reviewed Rule 30 "
            "prose definition, lookup diagram, and single-black-cell context; "
            "the target does not separately state infinite-support boundary "
            "mechanics."
        ),
    },
    "R000002": {
        "units": ["U000219", "U000228", "U000229"],
        "assets": ["A001215"],
        "attempt": (
            "Resolved the printed page 32 pointer to the reviewed Rule 110 "
            "prose definition, lookup diagram, and evolution caption."
        ),
    },
    "R000004": {
        "units": ["U000215", "U000216"],
        "assets": ["A001179"],
        "attempt": (
            "Resolved the printed page 29 pointer to the reviewed 500-step "
            "Rule 30 evolution and its single-cell-run caption."
        ),
    },
    "R000016": {
        "units": [
            "U005009",
            "U005010",
            "U005011",
            "U005012",
            "U005013",
            "U005014",
            "U005015",
            "U005016",
            "U005017",
            "U005018",
            "U005019",
            "U005020",
            "U005021",
            "U005022",
            "U005023",
            "U005024",
            "U005025",
            "U005026",
            "U005027",
            "U005028",
            "U005029",
            "U005030",
            "U005031",
            "U005032",
            "U005033",
            "U005034",
            "U005035",
            "U005036",
        ],
        "assets": [],
        "attempt": (
            "Resolved the printed page 867 pointer to the reviewed built-in "
            "CellularAutomaton interface, output slicing, and rule forms."
        ),
    },
    "R000017": {
        "units": [
            "U005084",
            "U005085",
            "U005093",
            "U005094",
            "U005095",
            "U005096",
            "U005097",
            "U005098",
            "U005099",
            "U005100",
            "U005101",
            "U005102",
            "U005103",
            "U005104",
            "U005105",
            "U005106",
        ],
        "assets": [],
        "attempt": (
            "Resolved the printed page 869 pointer to the reviewed algebraic "
            "and Boolean rule representations and their value encoding."
        ),
    },
    "R000055": {
        "units": [
            "U005172",
            "U005173",
            "U005174",
            "U005175",
            "U005176",
            "U005177",
        ],
        "assets": [
            "A000372",
            "A000373",
            "A000374",
            "A000375",
            "A000376",
        ],
        "attempt": (
            "Resolved the printed page 873 pointer to the reviewed classical "
            "labyrinth procedure text and its five construction images."
        ),
    },
    "R000070": {
        "units": [
            "U005113",
            "U005114",
            "U005115",
            "U005116",
            "U005117",
            "U005118",
            "U005123",
            "U005124",
            "U005125",
            "U005126",
            "U005127",
        ],
        "assets": [],
        "attempt": (
            "Resolved the printed page 870 pointer to the reviewed Rule 90, "
            "binomial-modulo-k, and additive-cellular-automaton formulas."
        ),
    },
    "R000073": {
        "units": ["U005225"],
        "assets": [],
        "attempt": (
            "Resolved the printed page 875 pointer to the reviewed Leonardo "
            "geometrical-constraint and rule-based-picture passage; the "
            "target names constrained patterns but supplies no fuller "
            "Leonardo construction law."
        ),
    },
    "R000088": {
        "units": ["U005137", "U005138"],
        "assets": ["A000362"],
        "attempt": (
            "Resolved the printed page 871 pointer to the reviewed "
            "BitXor/munching-squares mechanics and construction image; this "
            "grounds the source's later historical name “munching foos”."
        ),
    },
}

LATE_ROUTE_TARGETS = {
    "R000097": {
        "units": [
            "U000149",
            "U000150",
            "U000151",
            "U000152",
            "U000153",
        ],
        "assets": ["A001057"],
        "attempt": (
            "Resolved the printed page 19 pointer to the reviewed 1981 "
            "systematic all-program experiment, its reproduced output and "
            "caption, and the cellular-automaton co-reference; no lookup "
            "table or boundary convention is inferred from the historical "
            "image."
        ),
    },
}


class AuthoringError(ValueError):
    """The current audit state cannot safely receive this proposal."""


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def atomic_create(path: Path, payload: bytes) -> None:
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


def build_proposal(goal_dir: Path, *, late: bool = False) -> dict[str, Any]:
    goal_dir = goal_dir.resolve()
    if goal_dir != GOAL_DIR.resolve():
        raise AuthoringError("this reproducer is bound to the canonical Goal 4")

    routes = read_csv(goal_dir / merge_worker_output.ROUTE_NAME)
    units = {
        row["id"]
        for row in read_jsonl(goal_dir / merge_worker_output.UNITS_NAME)
    }
    assets = {
        row["asset_id"]
        for row in read_csv(goal_dir / merge_worker_output.ASSET_NAME)
    }
    history = read_jsonl(goal_dir / merge_worker_output.REVIEW_HISTORY_NAME)
    expected_terminal_mode = "SEARCH_APPEND" if late else "INITIAL"
    if not history or history[-1].get("mode") != expected_terminal_mode:
        raise AuthoringError(
            f"expected terminal Stage 6 {expected_terminal_mode} event"
        )
    epoch = history[-1].get("epoch")
    if epoch != 1:
        raise AuthoringError(f"unexpected active epoch: {epoch!r}")

    route_by_id = {row["route_id"]: row for row in routes}
    targets = LATE_ROUTE_TARGETS if late else ROUTE_TARGETS
    if set(targets) - set(route_by_id):
        raise AuthoringError("one or more governed routes are absent")
    if late and any(
        route_by_id[route_id]["status"] != "RESOLVED"
        for route_id in ROUTE_TARGETS
    ):
        raise AuthoringError("initial Chapter 2 route closure is incomplete")

    updates: list[dict[str, str]] = []
    for route_id, target in targets.items():
        row = deepcopy(route_by_id[route_id])
        if row["status"] != "PENDING":
            raise AuthoringError(f"{route_id} is not PENDING")
        if row["target_unit_ids"] != "[]" or row["target_asset_ids"] != "[]":
            raise AuthoringError(f"{route_id} already has target links")
        if row["attempts"] != "[]":
            raise AuthoringError(f"{route_id} already has resolution attempts")
        missing_units = set(target["units"]) - units
        missing_assets = set(target["assets"]) - assets
        if missing_units or missing_assets:
            raise AuthoringError(
                f"{route_id} has missing targets: "
                f"units={sorted(missing_units)} assets={sorted(missing_assets)}"
            )
        row["status"] = "RESOLVED"
        row["target_unit_ids"] = json.dumps(
            target["units"], separators=(",", ":")
        )
        row["target_asset_ids"] = json.dumps(
            target["assets"], separators=(",", ":")
        )
        row["attempts"] = json.dumps(
            [target["attempt"]], separators=(",", ":")
        )
        updates.append(row)

    return {
        "schema_version": 1,
        "proposal_kind": "ROUTE_RESOLUTION",
        "coordinator_id": (
            "ch02-experiment-late-route-closure-e1"
            if late
            else "ch02-experiment-route-closure-e1"
        ),
        "epoch": epoch,
        "base_artifact_sha256": {
            name: hashlib.sha256((goal_dir / name).read_bytes()).hexdigest()
            for name in merge_worker_output.WRITE_NAMES
        },
        "route_updates": updates,
    }


def main() -> int:
    if len(sys.argv) not in {2, 3} or (
        len(sys.argv) == 3 and sys.argv[1] != "--late"
    ):
        print(
            f"usage: {Path(sys.argv[0]).name} [--late] OUTPUT_JSON",
            file=sys.stderr,
        )
        return 2
    late = len(sys.argv) == 3
    output_path = Path(sys.argv[-1])
    try:
        with audit_transaction.read_guard(GOAL_DIR):
            proposal = build_proposal(GOAL_DIR, late=late)
            atomic_create(output_path, canonical_json_bytes(proposal))
    except (OSError, json.JSONDecodeError, AuthoringError, ValueError) as exc:
        print(f"Chapter 2 route authoring failed: {exc}", file=sys.stderr)
        return 1
    print(
        f"authored Chapter 2 route closure: "
        f"updates={len(proposal['route_updates'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
