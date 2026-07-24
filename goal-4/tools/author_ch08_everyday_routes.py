#!/usr/bin/env python3
"""Author the governed Stage 12 route-resolution proposal.

The helper closes the 24 previously discovered incoming routes whose literal
landings were read during the Chapter 8 main/Notes sequential review, plus
all 23 new Stage-12 WITHIN_STAGE routes. Routes are frozen by both their
current global route ID and immutable five-field identity:

    (source_unit_id, source_asset_id, route_kind,
     literal_target, expected_topic)

Resolution is locational.  When the exact landing does not contain the
expected mechanics, the appended attempt records that boundary explicitly;
it does not borrow a nearby construction or create candidate links.  R000543
remains PENDING because its page-1017 target belongs to Stage 13, whose source
is outside this helper's evidence boundary.
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
    "CHAPTERS/08-Implications-for-Everyday-Systems.md",
    "BACK-MATTER/NOTES/08-Implications-for-Everyday-Systems-Notes.md",
)
EXPECTED_PREVIOUS_REVIEW_ID = "V000034"
EXPECTED_PREVIOUS_EVENT_SHA256 = (
    "d1f928b7fa742c246d5f63de164f56139b6a7fdf367a7575f75633e0239e6357"
)
EXPECTED_TERMINAL_REVIEW_ID = "V000035"
EXPECTED_TERMINAL_REVIEWER = "ch08-union"
EXPECTED_STAGE_UNIT_COUNT = 510
EXPECTED_STAGE_ASSET_COUNT = 86
EXPECTED_STAGE_ROUTE_COUNT = 79
EXPECTED_INCOMING_COUNT = 24
EXPECTED_WITHIN_COUNT = 23
EXPECTED_UPDATE_COUNT = 47
EXPECTED_OUTGOING_COUNT = 56
EXPECTED_OUTGOING_IDENTITY_SHA256 = "TO_BE_FILLED"
EXPECTED_SPEC_SHA256 = (
    "2d680994e6fb874695ad3773e28ab40f3fc0af512482f52c819a8a250ddd9cb3"
)
EXPECTED_PRESERVATION_SHA256 = (
    "cbc445c7d640ebdfc399077148cfcd509441d925795e49206bd98ff92ce59b96"
)

ROUTE_ID = re.compile(r"^R[0-9]{6}$")
UNIT_ID = re.compile(r"^U[0-9]{6}$")
ASSET_ID = re.compile(r"^A[0-9]{6}$")


class AuthoringError(ValueError):
    """The current audit state cannot safely receive this proposal."""


@dataclass(frozen=True)
class RouteSpec:
    """One source-grounded incoming-route closure."""

    route_id: str
    identity: tuple[str, str, str, str, str]
    target_unit_ids: tuple[str, ...]
    target_asset_ids: tuple[str, ...]
    attempt: str


def expand_ids(value: str, *, prefix: str) -> tuple[str, ...]:
    """Expand compact inclusive ID ranges without weakening exactness."""

    result: list[str] = []
    width = 6
    pattern = re.compile(
        rf"^(?P<prefix>{re.escape(prefix)})(?P<start>[0-9]{{{width}}})"
        rf"(?:-(?P<end_prefix>{re.escape(prefix)})?"
        rf"(?P<end>[0-9]{{{width}}}))?$"
    )
    for token in value.split():
        match = pattern.fullmatch(token)
        if match is None:
            raise AuthoringError(f"invalid compact {prefix} ID token: {token}")
        start = int(match.group("start"))
        end = int(match.group("end") or start)
        if end < start:
            raise AuthoringError(f"descending compact ID range: {token}")
        result.extend(
            f"{prefix}{number:0{width}d}"
            for number in range(start, end + 1)
        )
    if len(result) != len(set(result)):
        raise AuthoringError(f"duplicate expanded {prefix} IDs: {value!r}")
    return tuple(result)


def route_spec(
    route_id: str,
    source_unit_id: str,
    source_asset_id: str,
    route_kind: str,
    literal_target: str,
    expected_topic: str,
    target_unit_ids: str,
    target_asset_ids: str,
    finding: str,
) -> RouteSpec:
    """Build one exact route-ID-and-identity-keyed closure."""

    units = expand_ids(target_unit_ids, prefix="U")
    assets = expand_ids(target_asset_ids, prefix="A")
    if not units and not assets:
        raise AuthoringError("a resolved route specification has no target")
    landing = ", ".join((*units, *assets))
    return RouteSpec(
        route_id=route_id,
        identity=(
            source_unit_id,
            source_asset_id,
            route_kind,
            literal_target,
            expected_topic,
        ),
        target_unit_ids=units,
        target_asset_ids=assets,
        attempt=(
            f"Inspected {literal_target!r} at the exact reviewed landing "
            f"{landing}. {finding}"
        ),
    )


# The compact ranges are authoring notation only.  Every proposal field
# contains the fully expanded canonical IDs.
_ROUTE_DATA: tuple[tuple[str, ...], ...] = (
    (
        "R000010",
        "U004952",
        "",
        "PAGE",
        "See page 999",
        "1973 two-dimensional particle cellular-automaton mechanics",
        "U006911",
        "",
        (
            "The landing identifies Wolfram's 1973 square-grid system as "
            "having discrete particle positions and velocities and records "
            "its failure to generate the randomness needed for standard "
            "large-scale fluid behavior; no local update or collision table "
            "is printed there."
        ),
    ),
    (
        "R000086",
        "U005267",
        "",
        "PAGE",
        "page 999",
        "hard-sphere molecular dynamics",
        "U006911",
        "",
        (
            "The landing historically identifies idealized two-dimensional "
            "hard-sphere molecular-dynamics simulations, but supplies no "
            "hard-sphere state, collision law, or integration schedule."
        ),
    ),
    (
        "R000101",
        "U005292",
        "",
        "PAGE",
        "page 378",
        "cellular-automaton fluid construction",
        "U002092-U002094",
        "A001130",
        (
            "The landing supplies the triangular-lattice particle system, "
            "its displayed collision rules, plate reflection, regular "
            "particle injection, and individual- versus block-averaged "
            "velocity observers."
        ),
    ),
    (
        "R000105",
        "U000471",
        "",
        "PAGE",
        (
            "On page 400 I will use similar systems to discuss the growth "
            "of actual trees and leaves."
        ),
        "substitution systems applied to tree and leaf growth",
        "U002238-U002243 U002246-U002250",
        "A001149 A001150",
        (
            "The two landing clusters give fixed three-way stem "
            "substitution, its plant-branching evolution, and the "
            "length/angle variants whose limiting outlines resemble leaves."
        ),
    ),
    (
        "R000148",
        "U005497",
        "",
        "PAGE",
        "page 1006",
        "GoldenRatio angular point generator",
        "U006949-U006950",
        "A000046",
        (
            "The mapped landing supplies the GoldenRatio rotation, its "
            "Fibonacci approximants, and the explicit nth-point projection "
            "formula with a checked visual witness. The extraction does not "
            "preserve a clean printed-page break between pages 1006 and "
            "1007, so that locator ambiguity is retained explicitly."
        ),
    ),
    (
        "R000156",
        "U005530",
        "",
        "PAGE",
        "page 1005",
        "L-system plant-generation mechanics",
        "U006934",
        "",
        (
            "The landing supplies the complex-number branching-tip "
            "iteration and identifies L systems as models of connection "
            "patterns in plants; it does not print a separate L-system "
            "grammar."
        ),
    ),
    (
        "R000237",
        "U006192",
        "",
        "PAGE",
        "pages 407 and 1006",
        "parameter-space sets for geometric substitution systems",
        (
            "U002262-U002263 U002267-U002268 "
            "U006941-U006946"
        ),
        "A001154 A000038",
        (
            "The main landing defines peephole overlap maps over branching "
            "parameters, while the Notes landing gives the complex "
            "parameterization, connectedness/gap test, boundary facts, "
            "pruning method, and reviewed map witnesses."
        ),
    ),
    (
        "R000295",
        "U006110",
        "",
        "PAGE",
        "the 9-neighbor examples on page 373",
        "nine-neighbor growth-rule examples",
        "U002064-U002066",
        "A001126",
        (
            "The landing gives irreversible square-grid Moore-neighborhood "
            "growth examples whose accepted neighbor counts and initial row "
            "lengths are legible in the original-resolution image. The "
            "surviving caption begins mid-sentence, and that source defect "
            "is not repaired by inference."
        ),
    ),
    (
        "R000319",
        "U006162",
        "",
        "PAGE",
        "compare page 1005",
        (
            "alternate formula comparison for the complex-affine "
            "Sierpiński coordinate enumerator"
        ),
        "U006933-U006934",
        "",
        (
            "The landing gives the alternate complex-number representation "
            "of branch-tip positions and its explicit nested Outer/Times "
            "iteration; it does not itself label the construction "
            "Sierpiński."
        ),
    ),
    (
        "R000338",
        "U006202",
        "",
        "PAGE",
        "pages 407 and 1006",
        "parameter-space sets analogous to the Mandelbrot set",
        (
            "U002262-U002263 U002267-U002268 "
            "U006941-U006947"
        ),
        "A001154 A000038",
        (
            "The landing shared with R000237 supplies the complete "
            "peephole/connectedness parameter-space construction, and "
            "U006947 explicitly records its qualified analogy to the "
            "Mandelbrot set."
        ),
    ),
    (
        "R000387",
        "U006310",
        "",
        "PAGE",
        "see page 994",
        "fivefold-symmetry comparison for the Penrose tiling",
        "U006885",
        "",
        (
            "The landing provides only a comparison: quasicrystals may have "
            "approximate pentagonal or icosahedral symmetry, unlike periodic "
            "patterns. It supplies no Penrose-tiling construction or rule."
        ),
    ),
    (
        "R000442",
        "U006346",
        "",
        "PAGE",
        "page 1012",
        "reaction-diffusion pattern-formation construction lead",
        "U006981-U006983",
        "",
        (
            "The landing states the two-chemical linear "
            "reaction-diffusion equation, wavelength-selective instability, "
            "Turing's finite-difference/random-start setup, nonlinear "
            "saturation boundary, and subsequent application context."
        ),
    ),
    (
        "R000575",
        "U006596",
        "",
        "PAGE",
        "page 997",
        "fluid turbulence",
        "U006899-U006903",
        "",
        (
            "The landing gives the Navier-Stokes continuum model and "
            "records its derivation, numerical/discretization limits, "
            "high-Reynolds-number turbulence boundary, and shock-regime "
            "limitations."
        ),
    ),
    (
        "R000584",
        "U006600",
        "",
        "PAGE",
        "page 1001",
        "ocean surfaces",
        "U006918",
        "",
        (
            "The landing observes regular ripples at low wind speed and "
            "random creases at higher speed, attributing the latter mainly "
            "to intrinsic water dynamics; it gives no native ocean-surface "
            "update law."
        ),
    ),
    (
        "R000590",
        "U006607",
        "",
        "PAGE",
        "page 999",
        "long-time tails",
        "U006911",
        "",
        (
            "The landing records the 1967 observation of long-time tails and "
            "their fluid-like interpretation only; it prints no tail law or "
            "measurement procedure."
        ),
    ),
    (
        "R000593",
        "U006611",
        "",
        "PAGE",
        "page 1013",
        "biological pigmentation randomness",
        "U006986",
        "",
        (
            "The landing discusses randomness entering pigmentation models "
            "through initial conditions, bilateral correlations, and "
            "lineage-dependent gene expression; it does not add a separate "
            "pigmentation transition law."
        ),
    ),
    (
        "R000594",
        "U006613",
        "",
        "PAGE",
        "page 1011",
        "neural randomness",
        "U006972",
        "",
        (
            "The landing mentions repetitive brain rhythms and conjectures "
            "small cell collections that generate intrinsically random "
            "behavior, but supplies no neural-randomness state or update."
        ),
    ),
    (
        "R000595",
        "U006615",
        "",
        "PAGE",
        "page 1011",
        "biological randomness",
        "U006972",
        "",
        (
            "The landing surveys random physiological motion and foraging "
            "walks and conjectures small intrinsic-randomness generators; "
            "it does not specify a general biological-randomness law."
        ),
    ),
    (
        "R000638",
        "U006685",
        "",
        "PAGE",
        "page 1003",
        "lognormal distributions",
        "U006924",
        "",
        (
            "The landing says only that human weights are closer to a "
            "lognormal distribution while discussing smooth traits; no "
            "lognormal density, generator, or fitting procedure is printed."
        ),
    ),
    (
        "R000650",
        "U006736",
        "",
        "PAGE",
        "page 994",
        "DLA details",
        "U006885",
        "",
        (
            "The landing gives the random-walk-and-stick DLA process, its "
            "Laplace-equation growth-probability formulation, and a "
            "three-color conserved-gray-cell cellular-automaton analog with "
            "its stated rule-dependence."
        ),
    ),
    (
        "R000685",
        "U006823",
        "",
        "PAGE",
        "page 1007",
        "position-dependent circle packings",
        "U006949-U006951",
        "A000046",
        (
            "The exact page-1007 landing contains phyllotaxis mathematics, "
            "history, projection formulas, and their visual witness; the "
            "expected position-dependent circle-packing topic is absent."
        ),
    ),
    (
        "R000688",
        "U006843",
        "",
        "PAGE",
        "page 1007",
        "minimal surfaces",
        "U006949-U006951",
        "A000046",
        (
            "The exact page-1007 landing contains phyllotaxis mathematics, "
            "history, projection formulas, and their visual witness; the "
            "expected minimal-surface topic is absent."
        ),
    ),
    (
        "R000691",
        "U006843",
        "",
        "PAGE",
        "page 1003",
        "protein structure",
        "U006927",
        "",
        (
            "The landing describes fibrous and globular proteins, helices, "
            "sheets, random-walk-like regions, energy near-degeneracy, and "
            "folding dynamics, but gives no executable protein-folding law."
        ),
    ),
    (
        "R000697",
        "U006846",
        "",
        "PAGE",
        "page 1001",
        "continuous instability patterns",
        "U006918",
        "",
        (
            "The exact page-1001 landing contains observational discussion "
            "of ocean-surface ripples and random creases, together with "
            "other natural examples; the expected continuous-instability "
            "PDE or construction is absent."
        ),
    ),
)

ROUTE_SPECS = tuple(route_spec(*row) for row in _ROUTE_DATA)


DEFERRED_ROUTE_ID = "R000543"
DEFERRED_ROUTE_IDENTITY = (
    "U006519",
    "",
    "PAGE",
    "page 1017",
    "reversible cellular automata",
)
DEFERRED_ROUTE_BOUNDARY = (
    "Printed page 1017 belongs to Stage 13. No Stage 13 source was opened, "
    "and the route remains PENDING without target or defect claims."
)


def embedded_spec_payload() -> dict[str, Any]:
    """Return the canonical digest payload for all closure judgments."""

    return {
        "starting_review_id": EXPECTED_PREVIOUS_REVIEW_ID,
        "stage_paths": list(STAGE_PATHS),
        "terminal_review_id": EXPECTED_TERMINAL_REVIEW_ID,
        "terminal_reviewer": EXPECTED_TERMINAL_REVIEWER,
        "routes": [
            {
                "route_id": spec.route_id,
                "identity": list(spec.identity),
                "target_unit_ids": list(spec.target_unit_ids),
                "target_asset_ids": list(spec.target_asset_ids),
                "attempt": spec.attempt,
            }
            for spec in ROUTE_SPECS
        ],
    }


def preservation_payload() -> dict[str, Any]:
    """Return the canonical digest payload for the deferred Stage 13 route."""

    return {
        "route_id": DEFERRED_ROUTE_ID,
        "identity": list(DEFERRED_ROUTE_IDENTITY),
        "boundary": DEFERRED_ROUTE_BOUNDARY,
    }


def payload_sha256(payload: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def validate_embedded_specs() -> tuple[str, str]:
    """Fail closed if any route-map or preservation judgment drifts."""

    route_ids = [spec.route_id for spec in ROUTE_SPECS]
    identities = [spec.identity for spec in ROUTE_SPECS]
    if (
        len(ROUTE_SPECS) != EXPECTED_UPDATE_COUNT
        or len(set(route_ids)) != EXPECTED_UPDATE_COUNT
        or len(set(identities)) != EXPECTED_UPDATE_COUNT
    ):
        raise AuthoringError("route specifications are missing or duplicated")
    if route_ids != sorted(route_ids):
        raise AuthoringError("route specifications are not in canonical order")
    if DEFERRED_ROUTE_ID in route_ids:
        raise AuthoringError("deferred Stage 13 route entered the closure set")
    for spec in ROUTE_SPECS:
        source_unit_id, source_asset_id, _, _, _ = spec.identity
        if ROUTE_ID.fullmatch(spec.route_id) is None:
            raise AuthoringError(f"invalid route ID: {spec.route_id}")
        if UNIT_ID.fullmatch(source_unit_id) is None:
            raise AuthoringError(
                f"invalid route source unit: {source_unit_id}"
            )
        if source_asset_id and ASSET_ID.fullmatch(source_asset_id) is None:
            raise AuthoringError(
                f"invalid route source asset: {source_asset_id}"
            )
        if (
            not spec.target_unit_ids
            and not spec.target_asset_ids
        ) or not spec.attempt.strip():
            raise AuthoringError(
                f"incomplete route closure: {spec.route_id}"
            )
        if any(
            UNIT_ID.fullmatch(item) is None
            for item in spec.target_unit_ids
        ):
            raise AuthoringError(
                f"invalid target unit in {spec.route_id}"
            )
        if any(
            ASSET_ID.fullmatch(item) is None
            for item in spec.target_asset_ids
        ):
            raise AuthoringError(
                f"invalid target asset in {spec.route_id}"
            )

    spec_digest = payload_sha256(embedded_spec_payload())
    preservation_digest = payload_sha256(preservation_payload())
    if spec_digest != EXPECTED_SPEC_SHA256:
        raise AuthoringError(
            "embedded route specification digest drifted: "
            f"{spec_digest} != {EXPECTED_SPEC_SHA256}"
        )
    if preservation_digest != EXPECTED_PRESERVATION_SHA256:
        raise AuthoringError(
            "embedded preservation digest drifted: "
            f"{preservation_digest} != {EXPECTED_PRESERVATION_SHA256}"
        )
    return spec_digest, preservation_digest


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                raise AuthoringError(
                    f"{path.name}:{line_number} is unexpectedly blank"
                )
            row = json.loads(line)
            if not isinstance(row, dict):
                raise AuthoringError(
                    f"{path.name}:{line_number} is not an object"
                )
            rows.append(row)
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


def require_pending_route(row: dict[str, str], *, label: str) -> None:
    if row["status"] != "PENDING":
        raise AuthoringError(f"{label} route is not PENDING")
    if row["target_unit_ids"] != "[]" or row["target_asset_ids"] != "[]":
        raise AuthoringError(f"{label} route already carries target claims")
    if row["defect_boundary"] != "":
        raise AuthoringError(f"{label} route carries a defect boundary")
    parsed_string_list(row["attempts"], label=f"{label} attempts")
    vocabulary = parsed_string_list(
        row["vocabulary_terms"],
        label=f"{label} vocabulary_terms",
    )
    if not vocabulary:
        raise AuthoringError(f"{label} route has empty vocabulary")


def require_reviewed_unit(
    unit_id: str,
    units: dict[str, dict[str, Any]],
    reading: dict[str, dict[str, str]],
) -> None:
    unit = units.get(unit_id)
    review = reading.get(unit_id)
    if unit is None or review is None:
        raise AuthoringError(f"target unit does not exist: {unit_id}")
    if review["review_status"] != "REVIEWED":
        raise AuthoringError(f"target unit is not reviewed: {unit_id}")
    if review["review_stage"] != "12":
        raise AuthoringError(
            f"target unit was not closed by Stage 12: {unit_id}"
        )
    if (
        unit.get("path") not in STAGE_PATHS
        or review["path"] != unit.get("path")
    ):
        raise AuthoringError(f"target unit lies outside Stage 12: {unit_id}")


def require_screened_asset(
    asset_id: str,
    assets: dict[str, dict[str, str]],
) -> None:
    asset = assets.get(asset_id)
    if asset is None:
        raise AuthoringError(f"target asset does not exist: {asset_id}")
    if asset["inspection_status"] != "SCREENED":
        raise AuthoringError(f"target asset is not screened: {asset_id}")
    if (
        asset["review_stage"] != "12"
        or asset["assignment_path"] not in STAGE_PATHS
    ):
        raise AuthoringError(
            f"target asset lies outside Stage 12: {asset_id}"
        )
    if asset["source_status"] != "CLEAR":
        raise AuthoringError(f"target asset is not clear: {asset_id}")
    if asset["original_resolution_status"] != "REVIEWED":
        raise AuthoringError(
            f"target asset lacks original-resolution review: {asset_id}"
        )


def build_proposal(goal_dir: Path) -> dict[str, Any]:
    """Build the exact 24-row Stage 12 incoming-route proposal."""

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
    if len(history) < 2:
        raise AuthoringError("review history is too short")
    previous = history[-2]
    terminal = history[-1]
    if (
        previous.get("review_id") != EXPECTED_PREVIOUS_REVIEW_ID
        or previous.get("event_sha256") != EXPECTED_PREVIOUS_EVENT_SHA256
    ):
        raise AuthoringError("Stage 12 does not start from frozen V000034")
    if terminal.get("review_id") != EXPECTED_TERMINAL_REVIEW_ID:
        raise AuthoringError(
            f"expected terminal history event {EXPECTED_TERMINAL_REVIEW_ID}"
        )
    if terminal.get("previous_event_sha256") != EXPECTED_PREVIOUS_EVENT_SHA256:
        raise AuthoringError("terminal event does not descend from V000034")
    if terminal.get("mode") != "INITIAL" or terminal.get("stage") != 12:
        raise AuthoringError(
            "expected the terminal combined Stage 12 INITIAL event"
        )
    if terminal.get("reviewer") != EXPECTED_TERMINAL_REVIEWER:
        raise AuthoringError("terminal Stage 12 reviewer identity drifted")
    if tuple(terminal.get("source_paths", ())) != STAGE_PATHS:
        raise AuthoringError(
            "terminal review event is not the combined Stage 12 assignment"
        )
    if len(terminal.get("route_changes", ())) != EXPECTED_STAGE_ROUTE_COUNT:
        raise AuthoringError("terminal Stage 12 route-change count drifted")
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
    routes_by_id = {row["route_id"]: row for row in routes}
    if (
        len(reading) != len(reading_rows)
        or len(assets) != len(asset_rows)
        or len(routes_by_id) != len(routes)
    ):
        raise AuthoringError("a canonical ledger contains duplicate identities")

    stage_units = [
        row
        for row in reading_rows
        if row["review_stage"] == "12" and row["path"] in STAGE_PATHS
    ]
    stage_assets = [
        row
        for row in asset_rows
        if row["review_stage"] == "12"
        and row["assignment_path"] in STAGE_PATHS
    ]
    if (
        len(stage_units) != EXPECTED_STAGE_UNIT_COUNT
        or any(row["review_status"] != "REVIEWED" for row in stage_units)
    ):
        raise AuthoringError("combined Stage 12 unit coverage drifted")
    if (
        len(stage_assets) != EXPECTED_STAGE_ASSET_COUNT
        or any(row["inspection_status"] != "SCREENED" for row in stage_assets)
    ):
        raise AuthoringError("combined Stage 12 asset coverage drifted")

    deferred = routes_by_id.get(DEFERRED_ROUTE_ID)
    if (
        deferred is None
        or route_identity(deferred) != DEFERRED_ROUTE_IDENTITY
        or deferred["owning_stage"] == "12"
        or deferred["closure_scope"] != "CROSS_RANGE"
    ):
        raise AuthoringError("deferred Stage 13 route identity drifted")
    require_pending_route(deferred, label=DEFERRED_ROUTE_ID)

    updates: list[dict[str, str]] = []
    for spec in ROUTE_SPECS:
        before = routes_by_id.get(spec.route_id)
        if before is None:
            raise AuthoringError(f"governed route is absent: {spec.route_id}")
        if route_identity(before) != spec.identity:
            raise AuthoringError(
                f"governed route identity drifted: {spec.route_id}"
            )
        if (
            before["owning_stage"] == "12"
            or before["closure_scope"] != "CROSS_RANGE"
        ):
            raise AuthoringError(
                f"governed route is not incoming: {spec.route_id}"
            )
        require_pending_route(before, label=spec.route_id)

        source_unit_id, source_asset_id, _, _, _ = spec.identity
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
            require_reviewed_unit(unit_id, units, reading)
        for asset_id in spec.target_asset_ids:
            require_screened_asset(asset_id, assets)

        prior_attempts = parsed_string_list(
            before["attempts"],
            label=f"{spec.route_id} attempts",
        )
        prior_vocabulary = parsed_string_list(
            before["vocabulary_terms"],
            label=f"{spec.route_id} vocabulary_terms",
        )

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
        if (
            update["route_id"] != spec.route_id
            or route_identity(update) != spec.identity
            or update["defect_boundary"] != ""
        ):
            raise AuthoringError(
                f"route update changed immutable fields: {spec.route_id}"
            )
        updates.append(update)

    if len(updates) != EXPECTED_UPDATE_COUNT:
        raise AuthoringError("route update count drifted")

    return {
        "schema_version": 1,
        "proposal_kind": "ROUTE_RESOLUTION",
        "coordinator_id": "ch08-everyday-incoming-route-closure-e2",
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
            spec_digest, preservation_digest = validate_embedded_specs()
        except (OSError, json.JSONDecodeError, AuthoringError) as exc:
            print(
                f"Chapter 8 route specification check failed: {exc}",
                file=sys.stderr,
            )
            return 1
        print(
            "Chapter 8 incoming-route specification valid: "
            f"resolved={EXPECTED_UPDATE_COUNT} "
            f"deferred={DEFERRED_ROUTE_ID} "
            f"spec-sha256={spec_digest} "
            f"preservation-sha256={preservation_digest}"
        )
        return 0
    if len(sys.argv) != 2:
        print(
            "usage: author_ch08_everyday_routes.py OUTPUT_JSON",
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
        print(f"Chapter 8 route authoring failed: {exc}", file=sys.stderr)
        return 1
    print(
        f"Wrote {output_path} with {len(proposal['route_updates'])} "
        "route-ID-and-identity-keyed incoming closures."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
