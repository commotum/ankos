#!/usr/bin/env python3
"""Author the governed Stage 7 Chapter 3 route-resolution proposal.

The governed routes are selected only by their immutable five-field identity:

    (source_unit_id, source_asset_id, route_kind,
     literal_target, expected_topic)

Allocated route IDs are deliberately treated as output trace data and are
never used to select a route.
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
    "CHAPTERS/03-The-World-of-Simple-Programs/03-The-World-of-Simple-Programs.md",
    "BACK-MATTER/NOTES/03-The-World-of-Simple-Programs-Notes/03-The-World-of-Simple-Programs-Notes.md",
)
EXPECTED_SPEC_COUNTS = {"incoming": 11, "within": 16}
EXPECTED_SPEC_SHA256 = (
    "93976805b02bc1d8ec3087394b5ab1b2a203b1da64c569aa3acb25444f50327d"
)
UNIT_ID = re.compile(r"^U[0-9]{6}$")
ASSET_ID = re.compile(r"^A[0-9]{6}$")


class AuthoringError(ValueError):
    """The current audit state cannot safely receive this proposal."""


@dataclass(frozen=True)
class RouteSpec:
    """One closed target claim from the reviewed Stage 7 route map."""

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
    """Keep the embedded route table compact without hiding any target IDs."""

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


ROUTE_SPECS = (
    route_spec(
        "incoming",
        "U004946",
        "",
        "SECTION",
        "Chapter 3 uses standard computer science models",
        "Turing-machine and register-machine native mechanics",
        (
            "U000433 U000434 U000435 U000436 U000437 U000543 U000545 "
            "U000546 U000547 U000549 U000550 U005409 U005410 U005411 "
            "U005412 U005413 U005414 U005415 U005575 U005576 U005577 "
            "U005578 U005579"
        ),
        "A001595 A001596 A000769",
        (
            "Resolved the Chapter 3 section pointer to reviewed native "
            "mechanics for both models: tape/head/state transitions in "
            "U000433-U000437 and executable Turing-machine semantics in "
            "U005409-U005415; program-counter/register state and "
            "increment/decrement-jump semantics in U000543, U000545-U000550 "
            "and U005575-U005579. A001595-A001596 and A000769 are the direct "
            "rule/program witnesses. This closure does not absorb "
            "low-level-language applications into either native model."
        ),
    ),
    route_spec(
        "incoming",
        "U004966",
        "",
        "PAGE",
        "The numbering of rules is discussed on page 53.",
        "elementary cellular-automaton rule-number decoding",
        "U000323 U000324 U000325",
        "A001441",
        (
            "Resolved printed page 53 to the reviewed 0-255 elementary-rule "
            "numbering passage and diagram. U000323-U000325 and A001441 "
            "explicitly map the eight ordered binary outputs to the base-2 "
            "digits of the rule number."
        ),
    ),
    route_spec(
        "incoming",
        "U004997",
        "",
        "PAGE",
        "explicit replacements for all possible blocks ... (see page 60)",
        "general one-dimensional cellular-automaton rule schema",
        "U000350 U000351 U000352 U000353 U005360 U005361 U005362 U005363",
        "A001507",
        (
            "Resolved the printed page-60 pointer with a bounded split: "
            "U000350-U000353 and A001507 are the main-text three-color "
            "totalistic worked specialization, while U005360-U005363 state "
            "and implement the general k-color, range-r one-dimensional rule "
            "schema and rule-number decoding. The general mechanics come "
            "from the Notes units; the main example alone must not be "
            "described as the fully general schema."
        ),
    ),
    route_spec(
        "incoming",
        "U005008",
        "",
        "PAGE",
        "implementation of totalistic cellular automata on page 886",
        "totalistic cellular-automaton rule decoding and implementation",
        "U005364 U005365 U005366 U005367 U005368 U005369",
        "",
        (
            "Resolved printed page 886 to U005364-U005369. These reviewed "
            "units give nearest-neighbor and general-range totalistic step "
            "functions and the exact base-k code-number decoder used to "
            "construct TotalisticCARule values."
        ),
    ),
    route_spec(
        "incoming",
        "U005009",
        "",
        "PAGE",
        "see also page 886",
        "general built-in cellular-automaton profile semantics",
        (
            "U005360 U005361 U005362 U005363 U005364 U005365 U005366 "
            "U005367 U005368 U005369 U005370"
        ),
        "",
        (
            "Resolved printed page 886 to the reviewed general/totalistic "
            "common framework. U005370 explicitly distinguishes the "
            "ListConvolve weight profiles used by the built-in "
            "CellularAutomaton representation, with U005360-U005369 "
            "providing the two rule forms and decoders it unifies."
        ),
    ),
    route_spec(
        "incoming",
        "U005117",
        "",
        "PAGE",
        "the one produced by rule 60 (see page 58)",
        "Rule 60 cellular-automaton mechanics",
        "U000337 U000338 U000339 U005329 U005331",
        "A001496",
        (
            "Resolved printed page 58 to the reviewed nested-rule panel and "
            "Rule 60 identity at U000337-U000339/A001496, with the exact "
            "local law Mod[p + q, 2] supplied by U005329 and U005331. No "
            "off-picture boundary convention is inferred."
        ),
    ),
    route_spec(
        "incoming",
        "U005214",
        "",
        "PAGE",
        "the nested form on page 892",
        "nested paperfolding construction",
        "U005515 U005516",
        "A000424",
        (
            "Resolved printed page 892 to U005515-U005516 and A000424. The "
            "text gives the successive-fold substitution recurrence and the "
            "image is the corresponding right-angle path, so the nested "
            "paperfolding construction is directly reviewed rather than "
            "inferred from a filename."
        ),
    ),
    route_spec(
        "incoming",
        "U005250",
        "",
        "PAGE",
        "page 893",
        "Thue substitution-system construction",
        (
            "U000457 U000459 U000462 U000463 U005458 U005459 U005460 "
            "U005461 U005529"
        ),
        "A001602 A001604",
        (
            "Resolved printed page 893 to the reviewed Thue identity/history "
            "in U005529, joined to the explicit Thue-Morse sequence laws in "
            "U005458-U005461 and the construction-bearing substitution "
            "rule/evolution witnesses U000457, U000459, U000462-U000463, "
            "A001602 and A001604. The history paragraph alone is not treated "
            "as complete native mechanics."
        ),
    ),
    route_spec(
        "incoming",
        "U005253",
        "",
        "PAGE",
        "page 894",
        "Post tag-system mechanics",
        "U005558",
        "",
        (
            "Resolved printed page 894 to U005558. That reviewed unit states "
            "Post's first-symbol restriction and gives both a concrete "
            "binary three-symbol-deletion preset and a concrete three-color "
            "two-symbol-deletion preset, including their append blocks and "
            "reported behavior bounds."
        ),
    ),
    route_spec(
        "incoming",
        "U005272",
        "",
        "PAGE",
        "page 81",
        "Minsky simple Turing-machine mechanics",
        "U000433 U000434 U000435 U000436 U000437 U000449 U000450 U000451 U000452",
        "A001595 A001596 A001599 A001600 A001601",
        (
            "Resolved printed page 81 to the reviewed complex four-state "
            "Turing-machine preset and its rule/full/compressed views at "
            "U000449-U000452/A001599-A001601, with native tape/head/state "
            "mechanics at U000433-U000437/A001595-A001596. The Stage 7 "
            "target does not identify this preset as Minsky's; the closure "
            "resolves the page pointer and mechanics without inventing an "
            "attribution."
        ),
    ),
    route_spec(
        "incoming",
        "U005286",
        "",
        "PAGE",
        "See page 112.",
        "random-initial-condition versus intrinsic-randomness evidence",
        "U000630 U000631 U000632",
        "",
        (
            "Resolved printed page 112 to U000630-U000632. U000631 "
            "explicitly contrasts complicated behavior found with random "
            "initial conditions against the overlooked simple-seed Rule 30 "
            "example, and U000632 records the later exhaustive simple-"
            "initial-condition survey. This is historical experimental "
            "evidence; random input is not folded into Rule 30's native "
            "transition law."
        ),
    ),
    route_spec(
        "within",
        "U000381",
        "",
        "PAGE",
        "the last two cellular automata from page 66",
        "code-1635 and code-2049 page-66 trajectories continued for 3000 steps",
        "U000374 U000375 U000376",
        "A001552 A001553",
        (
            "Resolved the backward page-66 pointer to the second and third "
            "initial localized-structure examples U000374-U000376/"
            "A001552-A001553. U000373/A001551 is deliberately excluded "
            "because the source says the last two. A001552 is unlabeled and "
            "A001553 has a spill-label ambiguity, so the code-1635/code-2049 "
            "identities are corroborated by the ordered, labeled "
            "continuations U000377-U000380 rather than claimed as clean "
            "labels on the target assets."
        ),
    ),
    route_spec(
        "within",
        "U000481",
        "",
        "PAGE",
        "our original pictures of substitution systems on page 82",
        "the original fixed-size-element substitution-system pictures",
        "U000457 U000458 U000459",
        "A001602 A001603",
        (
            "Resolved printed page 82 to the two reviewed fixed-size-box "
            "substitution rule/evolution images and their caption at "
            "U000457-U000459/A001602-A001603. This target supports the "
            "representation comparison without turning the view into a new "
            "native law."
        ),
    ),
    route_spec(
        "within",
        "U000482",
        "",
        "PAGE",
        "our original pictures of substitution systems on page 82",
        "the original fixed-size-element substitution-system pictures",
        "U000457 U000458 U000459",
        "A001602 A001603",
        (
            "Resolved the repeated printed page-82 pointer to "
            "U000457-U000459/A001602-A001603, where each element is drawn at "
            "the same size. The target is the original presentation being "
            "compared, not a separate construction from the creation/"
            "destruction preset."
        ),
    ),
    route_spec(
        "within",
        "U000493",
        "",
        "SECTION",
        "The substitution systems that we discussed in the previous section",
        "the preceding parallel substitution-system family and mechanics",
        "U000453 U000454 U000455 U000456",
        "",
        (
            "Resolved the previous-section pointer to U000453-U000456, which "
            "define variable-length sequences and parallel replacement of "
            "every element by a color-specific block independent of "
            "neighbors. The target establishes the parallel baseline "
            "contrasted with sequential substitution."
        ),
    ),
    route_spec(
        "within",
        "U000524",
        "",
        "PAGE",
        (
            "the first three ordinary neighbor-independent substitution "
            "systems shown on page 83"
        ),
        "tag/substitution cycle correspondence",
        "U000455 U000456 U000462 U000463",
        "A001604",
        (
            "Resolved printed page 83 to the first three panels in "
            "A001604/U000462-U000463, with the neighbor-independent parallel "
            "replacement semantics at U000455-U000456. The closure records "
            "a correspondence after complete tag cycles; it does not merge "
            "tag and substitution identities."
        ),
    ),
    route_spec(
        "within",
        "U000525",
        "",
        "PAGE",
        "neighbor-independent substitution system of the kind we discussed on page 83",
        "one-deletion tag-system equivalence profile",
        "U000455 U000456 U000462 U000463",
        "A001604",
        (
            "Resolved printed page 83 to the reviewed neighbor-independent "
            "substitution family and its displayed page-83 presets at "
            "U000455-U000456, U000462-U000463 and A001604. The source "
            "supports behavioral/evolution correspondence for one-deletion "
            "tags, not candidate identity collapse."
        ),
    ),
    route_spec(
        "within",
        "U000530",
        "",
        "SECTION",
        "the tag systems that we discussed in the previous section",
        "the preceding ordinary tag-system family and mechanics",
        "U000516 U000517 U000518",
        "",
        (
            "Resolved the previous-section pointer to U000516-U000518, which "
            "define an ordinary tag state and its fixed-prefix deletion "
            "followed by a removed-color-dependent append block. Later one- "
            "and two-deletion examples are variants, not needed to identify "
            "the contrasted ordinary mechanism."
        ),
    ),
    route_spec(
        "within",
        "U000536",
        "",
        "PAGE",
        "the third neighbor-independent substitution system shown on page 83",
        "cyclic-tag case (c) nested-form correspondence",
        "U000462 U000463",
        "A001604",
        (
            "Resolved printed page 83 to the third page-83 substitution "
            "panel in A001604/U000462-U000463. It is the Fibonacci-related "
            "case (c); the route records the claimed nested-form "
            "correspondence and does not identify the cyclic-tag and "
            "substitution rules as the same native object."
        ),
    ),
    route_spec(
        "within",
        "U000539",
        "",
        "PAGE",
        "the third neighbor-independent substitution system shown on page 83",
        "cyclic-tag case (c) nested-form correspondence",
        "U000462 U000463",
        "A001604",
        (
            "Resolved the repeated printed page-83 pointer to the third "
            "substitution panel in A001604/U000462-U000463. The target "
            "supports the alternate-step nested-form comparison for "
            "cyclic-tag case (c), not a native-law merge."
        ),
    ),
    route_spec(
        "within",
        "U000589",
        "",
        "SECTION",
        (
            "our study of substitution systems earlier in this chapter ... "
            "studying mobile automata"
        ),
        "the earlier substitution-system and mobile-automaton construction sections",
        "U000389 U000390 U000391 U000392 U000420 U000454 U000455 U000456",
        "",
        (
            "Resolved the two-part earlier-section claim to "
            "U000454-U000456 for variable-length substitution support and "
            "to U000389-U000392 plus U000420 for single-active-cell, "
            "nonparallel mobile updates that still produce complexity. The "
            "target is the exact evidence for the conclusion, not every "
            "example in either section."
        ),
    ),
    route_spec(
        "within",
        "U000602",
        "",
        "PAGE",
        "totalistic type described on page 60",
        "base definition of totalistic cellular automata",
        "U000350 U000351 U000352 U000353",
        "A001507",
        (
            "Resolved printed page 60 to U000350-U000353/A001507, where the "
            "three-color totalistic family, neighborhood average, seven "
            "cases and base-3 code convention are introduced. The later "
            "k-color comparison remains a family extension, not the target "
            "definition."
        ),
    ),
    route_spec(
        "within",
        "U000637",
        "",
        "PAGE",
        "the example shown on page 74",
        "extended mobile automaton found after correcting compression criteria",
        "U000410 U000411 U000412 U000413 U000414",
        "A001586 A001587 A001588",
        (
            "Resolved printed page 74 to the reviewed neighbor-writing "
            "random-color mobile preset at U000410-U000414/"
            "A001586-A001588, including its construction-bearing rule strip, "
            "full evolution and compressed history. Compression is an "
            "observer, not extra native update state."
        ),
    ),
    route_spec(
        "within",
        "U000638",
        "",
        "PAGE",
        "the example shown on page 75",
        "extended mobile automaton found after removing search assumptions",
        "U000415 U000416 U000417 U000418 U000419",
        "A001589 A001590 A001591",
        (
            "Resolved printed page 75 to the reviewed neighbor-writing "
            "random-motion mobile preset at U000415-U000419/"
            "A001589-A001591, including rule, trajectory and compressed "
            "position evidence. The historical search assumptions remain "
            "discovery context, not part of the preset."
        ),
    ),
    route_spec(
        "within",
        "U005404",
        "",
        "PAGE",
        "pages 73, 74 and 75",
        "mobile-automaton rule tables for motion plots",
        (
            "U000404 U000405 U000406 U000407 U000408 U000409 U000410 "
            "U000411 U000412 U000413 U000414 U000415 U000416 U000417 "
            "U000418 U000419"
        ),
        (
            "A001583 A001584 A001585 A001586 A001587 A001588 A001589 "
            "A001590 A001591"
        ),
        (
            "Resolved printed pages 73-75 to the three reviewed "
            "neighbor-writing mobile presets: nested "
            "U000404-U000409/A001583-A001585, random-color "
            "U000410-U000414/A001586-A001588, and random active-cell motion "
            "U000415-U000419/A001589-A001591. The Notes motion plots are "
            "observations of these rules, not replacement definitions."
        ),
    ),
    route_spec(
        "within",
        "U005429",
        "",
        "PAGE",
        "page 81",
        "localized Turing-machine rule and seed backgrounds",
        "U000449 U000450 U000451 U000452",
        "A001599 A001600 A001601",
        (
            "Resolved printed page 81 to the reviewed four-state "
            "Turing-machine preset and its rule/full/compressed views at "
            "U000449-U000452/A001599-A001601. The localized repetitive "
            "backgrounds are supplied by the Notes route source and "
            "A000413-A000417; they remain seed variants rather than being "
            "invented as content of the page-81 target."
        ),
    ),
    route_spec(
        "within",
        "U005568",
        "",
        "PAGE",
        "Rule (e) from the main text",
        "mechanical cyclic-tag rule (e) preset",
        "U000536 U000538 U000539",
        "A000767",
        (
            "Resolved Rule (e) to the reviewed five-preset cyclic-tag figure "
            "and caption at U000536, U000538-U000539/A000767. The mechanical "
            "trough and overflow failure are implementation/application "
            "facts from the route source, not additions to Rule (e)'s "
            "native cyclic-tag law."
        ),
    ),
)


def embedded_spec_payload() -> list[dict[str, Any]]:
    """Return the exact canonical projection governed by the route map."""

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
    """Fail if the checked-in route projection is malformed or drifts."""

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
        if route_kind not in {"PAGE", "SECTION"}:
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
        raise AuthoringError(
            f"embedded route counts drifted: {origins!r}"
        )
    digest = spec_sha256(embedded_spec_payload())
    if digest != EXPECTED_SPEC_SHA256:
        raise AuthoringError(
            "embedded route-map projection digest drifted: "
            f"{digest} != {EXPECTED_SPEC_SHA256}"
        )
    return digest


def source_map_payload(path: Path) -> list[dict[str, Any]]:
    """Load only the governed claims from an external route-map artifact."""

    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or raw.get("schema_version") != 1:
        raise AuthoringError("route map does not use schema version 1")
    payload: list[dict[str, Any]] = []
    for origin, field in (
        ("incoming", "incoming_routes"),
        ("within", "within_stage_routes"),
    ):
        rows = raw.get(field)
        if not isinstance(rows, list):
            raise AuthoringError(f"route map {field} is not an array")
        for index, row in enumerate(rows, start=1):
            if not isinstance(row, dict):
                raise AuthoringError(
                    f"route map {field}[{index}] is not an object"
                )
            identity = row.get("identity")
            resolution = row.get("resolution")
            if not isinstance(identity, dict) or not isinstance(
                resolution, dict
            ):
                raise AuthoringError(
                    f"route map {field}[{index}] lacks identity/resolution"
                )
            if set(identity) != set(IDENTITY_FIELDS):
                raise AuthoringError(
                    f"route map {field}[{index}] identity fields drifted"
                )
            if resolution.get("decision") != "RESOLVE":
                raise AuthoringError(
                    f"route map {field}[{index}] is not a RESOLVE decision"
                )
            units = resolution.get("target_unit_ids")
            assets = resolution.get("target_asset_ids")
            attempt = resolution.get("attempt")
            if (
                not isinstance(units, list)
                or not all(isinstance(value, str) for value in units)
                or not isinstance(assets, list)
                or not all(isinstance(value, str) for value in assets)
                or not isinstance(attempt, str)
            ):
                raise AuthoringError(
                    f"route map {field}[{index}] has malformed targets"
                )
            payload.append(
                {
                    "origin": origin,
                    "identity": {
                        name: identity[name] for name in IDENTITY_FIELDS
                    },
                    "target_unit_ids": units,
                    "target_asset_ids": assets,
                    "attempt": attempt,
                }
            )
    return payload


def compare_source_map(path: Path) -> None:
    """Prove that the checked-in projection makes no extra target claims."""

    expected = embedded_spec_payload()
    observed = source_map_payload(path)
    if observed != expected:
        raise AuthoringError(
            "external route map differs from the embedded governed projection"
        )
    if spec_sha256(observed) != EXPECTED_SPEC_SHA256:
        raise AuthoringError("external route-map projection digest drifted")


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
    if any(None in row or any(value is None for value in row.values()) for row in rows):
        raise AuthoringError(f"{path.name} contains a malformed row")
    return rows


def atomic_create(path: Path, payload: bytes) -> None:
    """Create a proposal exactly once, durably, and without symlink following."""

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
    if review["review_stage"] != "7":
        raise AuthoringError(
            f"{label} unit was not closed by Stage 7: {unit_id}"
        )
    if unit.get("path") not in STAGE_PATHS or review["path"] != unit.get("path"):
        raise AuthoringError(
            f"{label} unit lies outside the Stage 7 source paths: {unit_id}"
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
    if asset["review_stage"] != "7":
        raise AuthoringError(
            f"{label} asset was not closed by Stage 7: {asset_id}"
        )
    if asset["assignment_path"] not in STAGE_PATHS:
        raise AuthoringError(
            f"{label} asset lies outside the Stage 7 source paths: {asset_id}"
        )


def build_proposal(goal_dir: Path) -> dict[str, Any]:
    """Build the exact 27-row identity-keyed Stage 7 closure proposal."""

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
    if terminal.get("mode") != "INITIAL" or terminal.get("stage") != 7:
        raise AuthoringError(
            "expected the terminal combined Stage 7 INITIAL review event"
        )
    if tuple(terminal.get("source_paths", ())) != STAGE_PATHS:
        raise AuthoringError(
            "terminal review event is not the combined Stage 7 assignment"
        )
    epoch = terminal.get("epoch")
    if isinstance(epoch, bool) or not isinstance(epoch, int) or epoch < 1:
        raise AuthoringError(f"invalid active review epoch: {epoch!r}")

    units: dict[str, dict[str, Any]] = {}
    for unit in units_rows:
        unit_id = unit.get("id")
        if not isinstance(unit_id, str) or unit_id in units:
            raise AuthoringError("source-units.jsonl has invalid/duplicate IDs")
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
    observed_within = {
        route_identity(row)
        for row in routes
        if row["owning_stage"] == "7"
        and row["closure_scope"] == "WITHIN_STAGE"
        and row["status"] == "PENDING"
    }
    if observed_within != expected_within:
        missing = sorted(expected_within - observed_within)
        extra = sorted(observed_within - expected_within)
        raise AuthoringError(
            "Stage 7 WITHIN_STAGE route set differs from the governed map: "
            f"missing={missing!r} extra={extra!r}"
        )

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
        if before["status"] != "PENDING":
            raise AuthoringError(
                f"governed route is not PENDING: {spec.identity!r}"
            )
        if (
            before["target_unit_ids"] != "[]"
            or before["target_asset_ids"] != "[]"
            or before["attempts"] != "[]"
        ):
            raise AuthoringError(
                "governed route already carries target claims or attempts: "
                f"{spec.identity!r}"
            )
        if spec.origin == "within":
            if (
                before["owning_stage"] != "7"
                or before["closure_scope"] != "WITHIN_STAGE"
            ):
                raise AuthoringError(
                    "within-stage route metadata drifted: "
                    f"{spec.identity!r}"
                )
        else:
            if (
                before["owning_stage"] == "7"
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
            [spec.attempt],
            separators=(",", ":"),
            ensure_ascii=False,
        )
        if route_identity(update) != spec.identity:
            raise AuthoringError("route update changed its immutable identity")
        updates.append(update)
        origin_counts[spec.origin] += 1

    if origin_counts != EXPECTED_SPEC_COUNTS or len(updates) != 27:
        raise AuthoringError(
            f"route update counts drifted: {origin_counts!r}"
        )
    if len(matched_route_ids) != 27:
        raise AuthoringError("route selection did not produce 27 unique rows")

    return {
        "schema_version": 1,
        "proposal_kind": "ROUTE_RESOLUTION",
        "coordinator_id": "ch03-programs-route-closure-e1",
        "epoch": epoch,
        "base_artifact_sha256": {
            name: hashlib.sha256((goal_dir / name).read_bytes()).hexdigest()
            for name in merge_worker_output.WRITE_NAMES
        },
        "route_updates": updates,
    }


def main() -> int:
    if len(sys.argv) in {2, 3} and sys.argv[1] == "--check-spec":
        try:
            digest = validate_embedded_specs()
            if len(sys.argv) == 3:
                compare_source_map(Path(sys.argv[2]))
        except (OSError, json.JSONDecodeError, AuthoringError) as exc:
            print(f"Chapter 3 route specification check failed: {exc}", file=sys.stderr)
            return 1
        suffix = " source-map=matched" if len(sys.argv) == 3 else ""
        print(
            "Chapter 3 route specification valid: "
            f"incoming=11 within=16 sha256={digest}{suffix}"
        )
        return 0

    if len(sys.argv) != 2:
        print(
            f"usage: {Path(sys.argv[0]).name} OUTPUT_JSON\n"
            f"       {Path(sys.argv[0]).name} --check-spec [ROUTE_MAP_JSON]",
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
        print(f"Chapter 3 route authoring failed: {exc}", file=sys.stderr)
        return 1
    print(
        "authored Chapter 3 route closure: "
        f"updates={len(proposal['route_updates'])} "
        f"sha256={hashlib.sha256(canonical_json_bytes(proposal)).hexdigest()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
