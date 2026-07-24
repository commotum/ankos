#!/usr/bin/env python3
"""Author the governed Stage 11 Chapter 7 route-resolution proposal.

Routes are selected only by their immutable five-field identity:

    (source_unit_id, source_asset_id, route_kind,
     literal_target, expected_topic)

The proposal closes the exhaustive genuinely reachable incoming route set and
every Stage-11 WITHIN_STAGE route.  The complete Stage-11 CROSS_RANGE
partition and the one mixed incoming route are proved present and left
PENDING.  A route resolution is a locational closure: where the landing page
does not supply the expected mechanics, the appended attempt says so
explicitly and does not substitute adjacent or Notes-only mechanics.
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
    "CHAPTERS/07-Mechanisms-in-Programs-and-Nature.md",
    "BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes.md",
)
EXPECTED_TERMINAL_REVIEW_ID = "V000031"
EXPECTED_TERMINAL_REVIEWER = "ch07-union"
EXPECTED_SPEC_COUNTS = {"incoming": 22, "within": 41}
EXPECTED_UPDATE_COUNT = 63
EXPECTED_STAGE_UNIT_COUNT = 713
EXPECTED_STAGE_ASSET_COUNT = 194
EXPECTED_STAGE_ROUTE_COUNT = 141
EXPECTED_UNTOUCHED_CROSS_RANGE_COUNT = 100
EXPECTED_DEFERRED_MIXED_COUNT = 1
EXPECTED_SPEC_SHA256 = (
    "b302292926ebba64e44857aa9b5481d5308713d846d1af5bb4eed9fc480cc8a2"
)
EXPECTED_PRESERVATION_SHA256 = (
    "c2d2b5eed2f0a19fe1072cbfd32dd0ee78e79058d4ba5a5164196a6fb0d897ac"
)

UNIT_ID = re.compile(r"^U[0-9]{6}$")
ASSET_ID = re.compile(r"^A[0-9]{6}$")
PAGE_EXPRESSION = re.compile(
    r"\bpages?\s+"
    r"(?P<body>[0-9]{2,4}"
    r"(?:\s*(?:,|and|or|through|to|-)\s*[0-9]{2,4})*)",
    re.IGNORECASE,
)
NUMBER = re.compile(r"[0-9]{2,4}")
MAIN_PRINTED_PAGE_RANGE = range(297, 361)
NOTES_PRINTED_PAGE_RANGE = range(969, 991)


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
        result.extend(f"{prefix}{number:0{width}d}" for number in range(start, end + 1))
    if len(result) != len(set(result)):
        raise AuthoringError(f"duplicate expanded {prefix} IDs: {value!r}")
    return tuple(result)


def route_spec(
    origin: str,
    source_unit_id: str,
    source_asset_id: str,
    route_kind: str,
    literal_target: str,
    expected_topic: str,
    target_unit_ids: str,
    target_asset_ids: str,
    finding: str,
    attempt_override: str = "",
) -> RouteSpec:
    """Build one exact identity-keyed route specification."""

    units = expand_ids(target_unit_ids, prefix="U")
    assets = expand_ids(target_asset_ids, prefix="A")
    if not units and not assets:
        raise AuthoringError("a resolved route specification has no target")
    landing = ", ".join((*units, *assets))
    attempt = attempt_override or (
        f"Inspected {literal_target!r} at the exact reviewed landing "
        f"{landing}. {finding}"
    )
    return RouteSpec(
        origin=origin,
        identity=(
            source_unit_id,
            source_asset_id,
            route_kind,
            literal_target,
            expected_topic,
        ),
        target_unit_ids=units,
        target_asset_ids=assets,
        attempt=attempt,
    )


# The compact ranges below expand into the exact target IDs written to the
# proposal.  They are notation only; no range token enters the ledger.
_ROUTE_DATA: tuple[tuple[str, ...], ...] = (
    # Reachable incoming routes.
    (
        "incoming", "U004951", "", "PAGE",
        "middle-square random number generator (see page 975)",
        "middle-square initial-state generator mechanics",
        "U006664-U006665", "",
        "The Notes landing states the middle-square state update directly.",
    ),
    (
        "incoming", "U005193", "", "PAGE",
        "Compare the Apollonian packing of page 986.",
        "Apollonian circle-packing construction",
        "U006820-U006823", "A000004",
        "The landing identifies the Apollonian packing and its recursive tangency construction.",
    ),
    (
        "incoming", "U005236", "", "PAGE",
        "linear feedback shift registers (see page 974)",
        "linear feedback shift-register native update mechanics",
        "U006649-U006659", "A000683",
        "The landing supplies the shift-register state, feedback taps, update, and period context.",
    ),
    (
        "incoming", "U005248", "", "PAGE",
        "page 972",
        "three-body dynamical-system construction",
        "U006622-U006631", "A000673 A000680 A000681",
        (
            "The landing gives the exact Sitnikov special-case ODE and its "
            "nearby-orbit witnesses; the general three-body gravitational "
            "force law requested by the route is not printed there."
        ),
    ),
    (
        "incoming", "U005258", "", "PAGE",
        "page 974",
        "pseudorandom number-generator constructions",
        "U006638-U006669", "A000682 A000683",
        "The landing surveys congruential, shuffle, shift-register, and cellular-automaton generators.",
    ),
    (
        "incoming", "U005273", "", "PAGE",
        "page 971",
        "Lorenz differential-equation relation",
        "U006620", "",
        "The landing supplies only historical/relational Lorenz context; the Lorenz ODE is absent.",
    ),
    (
        "incoming", "U005485", "", "PAGE",
        "page 975",
        "Fibonacci modulo-k periods",
        "U006661-U006662", "",
        "The Fibonacci-mod-k recurrence is explicit, but the requested period formula is absent.",
    ),
    (
        "incoming", "U005604", "", "PAGE",
        "page 989",
        "balanced bracket sequence construction",
        "U006847-U006853", "A000011 A000012",
        "The landing defines balanced-parenthesis generation and its nested-expression interpretation.",
    ),
    (
        "incoming", "U005635", "", "PAGE",
        "page 971",
        "Lorenz differential-equation dynamics",
        "U006620", "",
        "The landing supplies only historical/relational Lorenz context; the Lorenz ODE and dynamics are absent.",
    ),
    (
        "incoming", "U006121", "", "PAGE",
        "page 980",
        "cellular automaton code 175850",
        "U006742-U006743", "A000728",
        "The third image panel identifies code 175850; decoding its rule number still depends on page 927.",
    ),
    (
        "incoming", "U006318", "", "PAGE",
        "page 981",
        "exact Ising-model energy law",
        "U006762-U006765", "A000738",
        "The landing states e[s], m[s], and the cyclic-boundary convention exactly.",
    ),
    (
        "incoming", "U006078", "", "PAGE",
        "see page 981",
        "reversible-rule phase-transition comparison for dimensional phenomena",
        "U006776-U006785", "A000739 A000740",
        "The landing supplies the reversible-rule phase-transition comparison and its finite witnesses.",
    ),
    (
        "incoming", "U006121", "", "PAGE",
        "discussed on page 979",
        "fixed-interior and cycling-region behavior of cellular automaton code 746",
        "U006740-U006743 U001798-U001803", "A000701 A000728 A001056",
        "The Notes and main landing identify code 746 and the fixed/cycling regions; the zero-neighbor case remains unstated.",
    ),
    (
        "incoming", "U006126", "", "PAGE",
        "the Voronoi region (see page 987)",
        "Voronoi-cell derivation of nearest-neighbor lattice adjacency",
        "U006832-U006835", "A000008",
        "The landing defines the Voronoi-region adjacency construction.",
    ),
    (
        "incoming", "U006163", "", "PAGE",
        "see page 358",
        "odd-multiplicity coordinate-enumerator correspondence",
        "U001977-U001982", "A001111-A001114",
        "The landing gives the rule-90/rule-150 identities and witnesses; an odd-multiplicity coordinate formula is absent.",
    ),
    (
        "incoming", "U001423", "", "SECTION",
        "the next few chapters",
        "natural-system stability from intrinsic randomness",
        "U001742-U001759 U006673-U006676", "A001045-A001047",
        "The main and Notes landing supply the intrinsic-randomness stability relation and its probabilistic/noisy examples.",
    ),
    (
        "incoming", "U001478", "", "PAGE",
        "page 338",
        "equal-density rule-184 nested patterns",
        "U001817-U001821", "A001060",
        "The landing gives the equal-density rule-184 transition witness.",
    ),
    (
        "incoming", "U006427", "", "PAGE",
        "page 339",
        "contrasting cellular-automaton density response",
        "U001822 U001824-U001826", "A001061",
        "The landing gives the density-response transition; its exact numeric code appears only in Notes U006757/A000733 and no decoded table is printed.",
    ),
    (
        "incoming", "U006441", "", "PAGE",
        "page 349",
        "stripe reduction of two-dimensional configurations",
        "U001882-U001887", "A001078",
        "All ten two-dimensional cellular-automaton codes are explicit, but a stripe-reduction law is not stated.",
    ),
    (
        "incoming", "U006449", "", "PAGE",
        "page 981",
        "critical-point nesting",
        "U006790 U006854", "",
        "The landing states and corroborates the critical-point nesting relation.",
    ),
    (
        "incoming", "U006449", "", "PAGE",
        "page 983",
        "renormalization-group universality",
        "U006790 U006854", "",
        "The landing supplies the renormalization/universality relation at the source's stated level.",
    ),
    (
        "incoming", "U006450", "", "PAGE",
        "page 989",
        "limits of renormalization for cellular automata",
        "U006854", "",
        "The landing supplies only the stated analogy/limit; no explicit renormalization-group operator is printed.",
    ),

    # Stage-11 WITHIN_STAGE routes.
    (
        "within", "U001933", "", "PAGE",
        "page 339",
        "the local rule and phase-selection quantity of the binary cellular automaton",
        "U001822 U001824-U001826", "A001061",
        "The landing supplies the transition and phase-selection quantity; the exact numeric code is Notes-only.",
    ),
    (
        "within", "U006596", "", "PAGE",
        "page 299",
        "main discussion defining the three randomness mechanisms",
        "U001594-U001611", "A001029-A001031",
        "The landing distinguishes environmental, initial-condition, and intrinsic mechanisms.",
    ),
    (
        "within", "U006598", "", "PAGE",
        "page 312",
        "pegboard randomness",
        "U001680 U001682-U001684", "A001039",
        "The landing gives the pegboard mechanism and its distribution witness.",
    ),
    (
        "within", "U006600", "", "PAGE",
        "page 301",
        "stochastic models",
        "U001599-U001601 U001612-U001630", "",
        "The landing and continued discussion delimit stochastic/environmental modeling without inventing a page-local law.",
    ),
    (
        "within", "U006600", "", "PAGE",
        "page 302",
        "random walks and electronic noise",
        "U001616-U001630", "",
        "The landing discusses random walks, Brownian motion, and electronic noise; it does not print a formal walk law.",
    ),
    (
        "within", "U006600", "", "PAGE",
        "page 328",
        "random walks",
        "U001773-U001784", "A001048-A001050",
        "The landing gives the random-walk construction and its two-dimensional witnesses.",
    ),
    (
        "within", "U006606", "", "PAGE",
        "page 303",
        "spark chambers and physical randomness",
        "U001622-U001630", "",
        "The landing gives the spark/noise-amplifier physical-randomness discussion.",
    ),
    (
        "within", "U006610", "", "PAGE",
        "page 317",
        "programmatic randomness",
        "U001696-U001715", "A001042",
        "The landing gives the rule-30 programmatic-randomness mechanism and witness.",
    ),
    (
        "within", "U006617", "", "PAGE",
        "page 305",
        "spinning and tossing",
        "U001638-U001646", "A001032 A001033",
        "The landing gives the spinning/tossing mechanisms and their outcome witnesses.",
    ),
    (
        "within", "U006621", "", "PAGE",
        "page 313",
        "three-body problem",
        "U001686-U001692", "A001040",
        "The landing gives the restricted three-body behavior and witness.",
    ),
    (
        "within", "U006626", "", "PAGE",
        "page 314",
        "Sitnikov-type simple case",
        "U001686-U001692", "A001040",
        "This is a co-reference landing only; the exact Sitnikov ODE is supplied by Notes U006626-U006629/A000681.",
    ),
    (
        "within", "U006630", "", "PAGE",
        "page 314",
        "solar-system randomness",
        "U001686-U001692", "A001040",
        "The landing supplies the page-level solar-system relation, not independently specified solar-system mechanics.",
    ),
    (
        "within", "U006633", "", "PAGE",
        "page 316",
        "intrinsic generation and algorithmic randomness",
        "U001693-U001695", "",
        "The landing identifies the intrinsic-generation section and its algorithmic-randomness claim.",
    ),
    (
        "within", "U006633", "", "PAGE",
        "page 317",
        "Mathematica cellular-automaton randomness",
        "U001696-U001715", "A001042",
        "The landing gives the cellular-automaton randomness construction and witness.",
    ),
    (
        "within", "U006633", "", "PAGE",
        "page 321",
        "cellular-automaton random generators",
        "U001728-U001732", "",
        "The landing compares cellular-automaton and congruential generators; it contains no new exact cellular-automaton table.",
    ),
    (
        "within", "U006634", "", "PAGE",
        "page 321",
        "perfect card shuffling",
        "U001728-U001732", "",
        "",
        (
            "Inspected the complete p321 landing U001728–U001732. It compares "
            "rule 30 with linear congruential generators and discusses "
            "intrinsic randomness; it contains no card-shuffle identity, "
            "permutation, or mechanics. Perfect-shuffle mechanics are "
            "supplied only by Notes U006634–U006637/A000682."
        ),
    ),
    (
        "within", "U006673", "", "PAGE",
        "page 323",
        "repeatable randomness",
        "U001742-U001745", "",
        "The landing defines repeatable randomness at the stated level.",
    ),
    (
        "within", "U006673", "", "PAGE",
        "page 324",
        "probabilistic rules",
        "U001746-U001752", "A001045",
        "The landing gives the probabilistic-rule construction and witness.",
    ),
    (
        "within", "U006673", "", "PAGE",
        "page 325",
        "noisy cellular automata",
        "U001755-U001759", "A001046 A001047",
        "The landing gives noisy cellular-automaton variants and witnesses.",
    ),
    (
        "within", "U006677", "", "PAGE",
        "page 326",
        "repeatably random experiments",
        "U001760-U001765", "",
        "The landing gives the repeatably-random experiment relation.",
    ),
    (
        "within", "U006695", "", "PAGE",
        "page 328",
        "random walks",
        "U001773-U001784", "A001048-A001050",
        "The landing gives the random-walk construction and its one- and two-dimensional witnesses.",
    ),
    (
        "within", "U006705", "", "PAGE",
        "page 330",
        "boundaries of random-walk particle clouds",
        "U001781-U001784", "A001050",
        "The landing gives the two-dimensional cloud/boundary witness.",
    ),
    (
        "within", "U006719", "", "PAGE",
        "page 331",
        "basic aggregation model",
        "U001785-U001788", "A001051",
        "The landing gives the basic aggregation rule and witness.",
    ),
    (
        "within", "U006727", "", "PAGE",
        "page 332",
        "generalized aggregation models",
        "U001789-U001795", "A001052-A001055",
        "The landing gives the generalized aggregation variants and witnesses.",
    ),
    (
        "within", "U006736", "", "PAGE",
        "page 333",
        "diffusion-limited aggregation",
        "U001796-U001801", "",
        "",
        (
            "Inspected complete p333 U001796–U001801. It discusses intrinsic "
            "randomness yielding smooth growth, gives no DLA identity/random-"
            "walk attachment law, and transitions toward code 746 on the "
            "following page. DLA is defined only by Notes "
            "U006736–U006739/A000707,A000721."
        ),
    ),
    (
        "within", "U006740", "", "PAGE",
        "page 334",
        "cellular-automaton code 746",
        "U001798 U001802 U001803", "A001056",
        "The landing identifies code 746 and its fixed-interior/cycling-region witness.",
    ),
    (
        "within", "U006751", "", "PAGE",
        "page 336",
        "domain interfaces",
        "U001804 U001806-U001809", "A001058 A001059",
        "The landing gives the domain-interface construction and witnesses.",
    ),
    (
        "within", "U006755", "", "PAGE",
        "page 339",
        "one-dimensional transitions",
        "U001822 U001824-U001826", "A001061",
        "The landing gives the one-dimensional transition and phase-selection witness.",
    ),
    (
        "within", "U006759", "", "PAGE",
        "page 340",
        "two-dimensional transitions",
        "U001827-U001829", "A001062",
        "The landing gives the two-dimensional transition witness.",
    ),
    (
        "within", "U006788", "", "PAGE",
        "page 339",
        "finite-size exceptions near the transition",
        "U001822 U001824-U001826", "A001061",
        "The landing gives the finite-size transition exceptions and witness.",
    ),
    (
        "within", "U006791", "", "PAGE",
        "page 325",
        "probabilistic cellular automata",
        "U001746-U001759", "A001045-A001047",
        "The landing gives the probabilistic and noisy cellular-automaton construction family.",
    ),
    (
        "within", "U006792", "", "PAGE",
        "page 341",
        "rate equations",
        "U001830 U001832-U001838", "A001063-A001066",
        "The landing gives the rate-equation relation and witnesses; the exact p=p^2(3-2p) equation is Notes-only.",
    ),
    (
        "within", "U006800", "", "PAGE",
        "page 343",
        "constraint distribution",
        "U001847-U001852", "A001067 A001068",
        "The landing gives the constraint-distribution construction and witnesses.",
    ),
    (
        "within", "U006800", "", "PAGE",
        "page 346",
        "constraint implementation",
        "U001861-U001871", "A001071-A001074",
        "The landing gives the iterative constraint implementation and witnesses.",
    ),
    (
        "within", "U006804", "", "PAGE",
        "page 347",
        "non-strict iterative procedure",
        "U001872-U001877", "A001075",
        "The landing gives the non-strict iterative procedure and witness.",
    ),
    (
        "within", "U006807", "", "PAGE",
        "page 347",
        "iterative improvement",
        "U001872-U001877", "A001075",
        "The landing gives the iterative-improvement procedure and witness.",
    ),
    (
        "within", "U006812", "", "PAGE",
        "page 346",
        "optimization cost landscape",
        "U001861-U001871", "A001071-A001074",
        "The landing gives the optimization/constraint landscape and witnesses.",
    ),
    (
        "within", "U006813", "", "PAGE",
        "page 349",
        "2D cellular automata and circle packing",
        "U001882-U001894", "A001078-A001080",
        "The mixed landing closes to both exact clusters: U001882-U001887/A001078 for the two-dimensional cellular-automaton invariant query and U001888-U001894/A001079-A001080 for circle/sphere packing.",
    ),
    (
        "within", "U006814", "", "PAGE",
        "page 350",
        "unequal-circle packing procedure",
        "U001895-U001897", "A001081",
        "The landing gives the unequal-circle packing procedure and witness.",
    ),
    (
        "within", "U006843", "", "PAGE",
        "page 351",
        "protein folding",
        "U001898-U001900", "",
        "",
        (
            "Inspected complete p351 U001898–U001900. It contains only "
            "general claims that complex biological form is explained by "
            "explicit evolution/growth rather than constraint satisfaction; "
            "it has no protein, amino-acid, energy, folding, chaperone, or "
            "prion mechanics. Protein-folding discussion is only Notes "
            "U006843."
        ),
    ),
    (
        "within", "U006846", "", "PAGE",
        "page 358",
        "nesting in numbers",
        "U001975", "",
        "The landing supplies the nesting-in-digit-sequences relation.",
    ),
)

ROUTE_SPECS = tuple(route_spec(*row) for row in _ROUTE_DATA)


# Every Stage-11 CROSS_RANGE obligation is frozen by exact immutable identity.
# These rows remain PENDING; this helper never opens or infers later targets.
UNTOUCHED_CROSS_RANGE_IDENTITIES: tuple[
    tuple[str, str, str, str, str], ...
] = (
    ("U001842", "", "PAGE", "page 211", "the complete local rule for the square-array constraint"),
    ("U002007", "", "SECTION", "Chapter 5", "constraint systems that generate nested patterns"),
    ("U006596", "", "PAGE", "page 552", "definition of randomness"),
    ("U006596", "", "PAGE", "page 1135", "free will and determinism"),
    ("U006596", "", "PAGE", "page 911", "random-looking mathematical digit sequences"),
    ("U006596", "", "PAGE", "page 997", "fluid turbulence"),
    ("U006597", "", "PAGE", "page 1192", "applications of randomness"),
    ("U006598", "", "PAGE", "page 969", "physical randomness sources"),
    ("U006598", "", "PAGE", "page 974", "card shuffling and pseudorandom generators"),
    ("U006600", "", "PAGE", "page 588", "random-variable models"),
    ("U006600", "", "PAGE", "page 1192", "Monte Carlo applications"),
    ("U006600", "", "PAGE", "page 1001", "ocean surfaces"),
    ("U006604", "", "PAGE", "page 918", "Weierstrass function"),
    ("U006604", "", "PAGE", "page 586", "substitution-system spectra"),
    ("U006606", "", "PAGE", "page 971", "dice and roulette imperfections"),
    ("U006607", "", "PAGE", "page 999", "long-time tails"),
    ("U006610", "", "PAGE", "page 1064", "quantum randomness"),
    ("U006611", "", "PAGE", "page 1013", "biological pigmentation randomness"),
    ("U006613", "", "PAGE", "page 1011", "neural randomness"),
    ("U006615", "", "PAGE", "page 1011", "biological randomness"),
    ("U006618", "", "PAGE", "page 914", "continued fractions"),
    ("U006618", "", "PAGE", "page 903", "substitution systems"),
    ("U006618", "", "PAGE", "page 1022", "billiards"),
    ("U006621", "", "PAGE", "page 920", "information content of initial conditions"),
    ("U006621", "", "PAGE", "page 955", "nonrepetitive dynamics"),
    ("U006621", "", "PAGE", "page 586", "frequency recognition of chaos"),
    ("U006621", "", "PAGE", "page 1177", "weather instability"),
    ("U006621", "", "PAGE", "page 1132", "three-body computation"),
    ("U006621", "", "SECTION", "Chapter 12", "computational irreducibility and universality"),
    ("U006630", "", "PAGE", "page 1021", "solar-system evolution"),
    ("U006633", "", "PAGE", "page 1067", "algorithmic randomness"),
    ("U006633", "", "PAGE", "page 603", "finite cellular-automaton randomness deviations"),
    ("U006633", "", "SECTION", "Chapter 4", "random-looking number systems"),
    ("U006639", "", "PAGE", "page 903", "runs in number generators"),
    ("U006642", "", "PAGE", "page 962", "all starting values of modular maps"),
    ("U006648", "", "PAGE", "page 1089", "LCG cryptanalysis"),
    ("U006649", "", "PAGE", "page 951", "additive cellular automata"),
    ("U006656", "", "PAGE", "page 1094", "Cantor-set geometry of generators"),
    ("U006659", "", "PAGE", "page 1087", "tap-vector representation"),
    ("U006659", "", "PAGE", "page 963", "primitive-polynomial periods"),
    ("U006659", "", "PAGE", "page 1084", "primitive polynomials"),
    ("U006660", "", "PAGE", "page 1088", "nonlinear feedback shift registers"),
    ("U006661", "", "PAGE", "page 891", "Fibonacci recurrences"),
    ("U006663", "", "PAGE", "page 598", "stream ciphers"),
    ("U006663", "", "PAGE", "page 1085", "DES"),
    ("U006668", "", "PAGE", "page 1090", "quadratic-generator predictability"),
    ("U006669", "", "PAGE", "page 260", "finite rule-30 periods"),
    ("U006669", "", "PAGE", "page 603", "cellular-automaton generators"),
    ("U006673", "", "PAGE", "page 591", "probabilistic cellular automata"),
    ("U006676", "", "PAGE", "page 464", "PDE approximations to cellular automata"),
    ("U006685", "", "PAGE", "page 1003", "lognormal distributions"),
    ("U006694", "", "PAGE", "page 969", "1/f noise"),
    ("U006704", "", "PAGE", "page 1082", "random-walk power spectra"),
    ("U006715", "", "PAGE", "page 163", "diffusion equation"),
    ("U006727", "", "PAGE", "page 213", "neighborhood templates"),
    ("U006727", "", "PAGE", "page 927", "aggregation rule numbering"),
    ("U006731", "", "PAGE", "page 1036", "confluence"),
    ("U006736", "", "PAGE", "page 994", "DLA details"),
    ("U006742", "", "PAGE", "page 177", "other growth rules"),
    ("U006742", "", "PAGE", "page 181", "other growth rules"),
    ("U006786", "", "PAGE", "page 989", "nested random patterns"),
    ("U006786", "", "PAGE", "page 1149", "nested random patterns"),
    ("U006787", "", "PAGE", "page 435", "reversible evolution"),
    ("U006790", "", "PAGE", "page 273", "nested phase competition"),
    ("U006790", "", "PAGE", "page 955", "renormalization group"),
    ("U006791", "", "PAGE", "page 591", "directed percolation"),
    ("U006792", "", "PAGE", "page 953", "probabilistic cellular-automaton approximations"),
    ("U006794", "", "PAGE", "page 1078", "wave superpositions"),
    ("U006800", "", "PAGE", "page 940", "rules versus constraints"),
    ("U006800", "", "PAGE", "page 1145", "NP completeness"),
    ("U006800", "", "PAGE", "page 954", "one-dimensional constraint algorithm"),
    ("U006806", "", "PAGE", "page 901", "Gray code"),
    ("U006813", "", "PAGE", "page 1105", "biological optimization"),
    ("U006813", "", "PAGE", "page 1143", "NP completeness history"),
    ("U006813", "", "PAGE", "page 927", "rule-number scheme"),
    ("U006813", "", "PAGE", "page 43", "ancient hexagonal circle packing"),
    ("U006813", "", "PAGE", "page 987", "circle packing"),
    ("U006820", "", "PAGE", "page 509", "Apollonian tangency network"),
    ("U006823", "", "PAGE", "page 1007", "position-dependent circle packings"),
    ("U006824", "", "PAGE", "page 929", "Voronoi cells of close packings"),
    ("U006832", "", "PAGE", "page 929", "lattice Voronoi cells"),
    ("U006843", "", "PAGE", "page 1007", "minimal surfaces"),
    ("U006843", "", "PAGE", "page 1039", "soap-film surfaces"),
    ("U006843", "", "PAGE", "page 1003", "protein structure"),
    ("U006843", "", "PAGE", "page 1184", "protein folding"),
    ("U006845", "", "PAGE", "page 587", "uniform frequency spectra"),
    ("U006845", "", "PAGE", "page 1062", "quantum-field fluctuations"),
    ("U006846", "", "PAGE", "page 138", "rational digit repetition"),
    ("U006846", "", "PAGE", "page 144", "continued-fraction repetition"),
    ("U006846", "", "PAGE", "page 1001", "continuous instability patterns"),
    ("U006846", "", "SECTION", "Chapter 4", "number systems with nested behavior"),
    ("U006850", "", "PAGE", "page 939", "context-free languages"),
    ("U006854", "", "PAGE", "page 273", "rule-184 nesting"),
    ("U006854", "", "PAGE", "page 983", "statistical-mechanics sampling"),
    ("U006854", "", "PAGE", "page 955", "rescaling and renormalization"),
    ("U006854", "", "PAGE", "page 26", "additive cellular automata"),
    ("U006868", "", "PAGE", "page 977", "random walks"),
    ("U006868", "", "PAGE", "page 969", "power-law steps"),
    ("U006869", "", "PAGE", "page 1142", "algorithm structures"),
    ("U006869", "", "PAGE", "page 1045", "topological defects"),
)


# This route cannot be partially closed: printed page 986 is in Stage 11, but
# printed page 1029 is not.  It remains pending until both targets are
# reviewed.
DEFERRED_MIXED_INCOMING_IDENTITIES: tuple[
    tuple[str, str, str, str, str], ...
] = (
    (
        "U006126",
        "",
        "PAGE",
        "Compare pages 1029 and 986",
        "crystallographic terminology and Voronoi-region shape comparison",
    ),
)


# These source-limited boundaries explain why four outgoing routes must not be
# opportunistically "resolved" from Stage 11.  Pending rows cannot carry a
# defect boundary under the ledger schema, so the helper freezes the notes
# alongside their immutable identities without mutating the rows.
PRESERVED_OBLIGATION_BOUNDARIES: dict[
    tuple[str, str, str, str, str], str
] = {
    (
        "U006676", "", "PAGE", "page 464",
        "PDE approximations to cellular automata",
    ): (
        "Stage 11 carries only the claim that a cellular-automaton-to-PDE "
        "approximation exists; it supplies no target PDE or operator."
    ),
    (
        "U006715", "", "PAGE", "page 163",
        "diffusion equation",
    ): (
        "Stage 11 carries only the random-walk-average-to-diffusion "
        "relation; the equation target remains unresolved."
    ),
    (
        "U006727", "", "PAGE", "page 927",
        "aggregation rule numbering",
    ): "The later rule-number target is required to decode the aggregation code.",
    (
        "U006813", "", "PAGE", "page 927",
        "rule-number scheme",
    ): "The later rule-number target is required to decode the cited codes.",
}


def embedded_spec_payload() -> dict[str, Any]:
    """Return the canonical digest payload for all closure judgments."""

    return {
        "stage_paths": list(STAGE_PATHS),
        "terminal_review_id": EXPECTED_TERMINAL_REVIEW_ID,
        "terminal_reviewer": EXPECTED_TERMINAL_REVIEWER,
        "routes": [
            {
                "origin": spec.origin,
                "identity": list(spec.identity),
                "target_unit_ids": list(spec.target_unit_ids),
                "target_asset_ids": list(spec.target_asset_ids),
                "attempt": spec.attempt,
            }
            for spec in ROUTE_SPECS
        ],
    }


def preservation_payload() -> dict[str, Any]:
    """Return the canonical digest payload for every untouched obligation."""

    return {
        "stage_cross_range": [
            list(identity)
            for identity in sorted(UNTOUCHED_CROSS_RANGE_IDENTITIES)
        ],
        "mixed_incoming": [
            list(identity)
            for identity in sorted(DEFERRED_MIXED_INCOMING_IDENTITIES)
        ],
        "source_limited_boundaries": [
            {"identity": list(identity), "boundary": boundary}
            for identity, boundary in sorted(
                PRESERVED_OBLIGATION_BOUNDARIES.items()
            )
        ],
    }


def payload_sha256(payload: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def validate_embedded_specs() -> tuple[str, str]:
    """Fail closed if any frozen route or preservation judgment drifts."""

    identities = [spec.identity for spec in ROUTE_SPECS]
    origins = {
        origin: sum(spec.origin == origin for spec in ROUTE_SPECS)
        for origin in EXPECTED_SPEC_COUNTS
    }
    if origins != EXPECTED_SPEC_COUNTS:
        raise AuthoringError(f"route specification counts drifted: {origins}")
    if (
        len(ROUTE_SPECS) != EXPECTED_UPDATE_COUNT
        or len(set(identities)) != EXPECTED_UPDATE_COUNT
    ):
        raise AuthoringError("route specifications are missing or duplicated")
    if any(
        spec.origin not in EXPECTED_SPEC_COUNTS
        or (not spec.target_unit_ids and not spec.target_asset_ids)
        or not spec.attempt.strip()
        for spec in ROUTE_SPECS
    ):
        raise AuthoringError("route specification has incomplete closure data")
    for spec in ROUTE_SPECS:
        source_unit_id, source_asset_id, _, _, _ = spec.identity
        if source_unit_id and UNIT_ID.fullmatch(source_unit_id) is None:
            raise AuthoringError(f"invalid route source unit: {source_unit_id}")
        if source_asset_id and ASSET_ID.fullmatch(source_asset_id) is None:
            raise AuthoringError(
                f"invalid route source asset: {source_asset_id}"
            )
        if any(UNIT_ID.fullmatch(item) is None for item in spec.target_unit_ids):
            raise AuthoringError(f"invalid target unit in {spec.identity!r}")
        if any(
            ASSET_ID.fullmatch(item) is None for item in spec.target_asset_ids
        ):
            raise AuthoringError(f"invalid target asset in {spec.identity!r}")

    cross = set(UNTOUCHED_CROSS_RANGE_IDENTITIES)
    mixed = set(DEFERRED_MIXED_INCOMING_IDENTITIES)
    if (
        len(UNTOUCHED_CROSS_RANGE_IDENTITIES)
        != EXPECTED_UNTOUCHED_CROSS_RANGE_COUNT
        or len(cross) != EXPECTED_UNTOUCHED_CROSS_RANGE_COUNT
    ):
        raise AuthoringError("Stage 11 CROSS_RANGE identity set drifted")
    if (
        len(DEFERRED_MIXED_INCOMING_IDENTITIES)
        != EXPECTED_DEFERRED_MIXED_COUNT
        or len(mixed) != EXPECTED_DEFERRED_MIXED_COUNT
    ):
        raise AuthoringError("mixed incoming identity set drifted")
    if set(identities) & cross or set(identities) & mixed or cross & mixed:
        raise AuthoringError("closed and preserved route partitions overlap")
    if not set(PRESERVED_OBLIGATION_BOUNDARIES).issubset(cross):
        raise AuthoringError("a preserved boundary is not a Stage 11 route")

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


def printed_page_numbers(literal_target: str) -> tuple[int, ...]:
    """Extract only numbers grammatically governed by page/pages."""

    pages: list[int] = []
    for match in PAGE_EXPRESSION.finditer(literal_target):
        pages.extend(int(value) for value in NUMBER.findall(match.group("body")))
    return tuple(pages)


def page_in_stage11(page: int) -> bool:
    return page in MAIN_PRINTED_PAGE_RANGE or page in NOTES_PRINTED_PAGE_RANGE


def classify_stage11_page_target(literal_target: str) -> str:
    """Return REACHABLE, MIXED, or NONE for the printed-page assignment."""

    pages = printed_page_numbers(literal_target)
    if not pages or not any(page_in_stage11(page) for page in pages):
        return "NONE"
    if all(page_in_stage11(page) for page in pages):
        return "REACHABLE"
    return "MIXED"


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
    if review["review_stage"] != "11":
        raise AuthoringError(
            f"{label} unit was not closed by Stage 11: {unit_id}"
        )
    if (
        unit.get("path") not in STAGE_PATHS
        or review["path"] != unit.get("path")
    ):
        raise AuthoringError(
            f"{label} unit lies outside Stage 11: {unit_id}"
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
    if asset["review_stage"] != "11":
        raise AuthoringError(
            f"{label} asset was not closed by Stage 11: {asset_id}"
        )
    if asset["assignment_path"] not in STAGE_PATHS:
        raise AuthoringError(
            f"{label} asset lies outside Stage 11: {asset_id}"
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
    if row["defect_boundary"] != "":
        raise AuthoringError(f"{label} pending route carries a defect boundary")
    parsed_string_list(row["attempts"], label=f"{label} attempts")
    parsed_string_list(
        row["vocabulary_terms"],
        label=f"{label} vocabulary_terms",
    )


def build_proposal(goal_dir: Path) -> dict[str, Any]:
    """Build the exact 63-row identity-keyed Stage 11 closure proposal."""

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
    if terminal.get("review_id") != EXPECTED_TERMINAL_REVIEW_ID:
        raise AuthoringError(
            f"expected terminal history event {EXPECTED_TERMINAL_REVIEW_ID}"
        )
    if terminal.get("mode") != "INITIAL" or terminal.get("stage") != 11:
        raise AuthoringError(
            "expected the terminal combined Stage 11 INITIAL event"
        )
    if terminal.get("reviewer") != EXPECTED_TERMINAL_REVIEWER:
        raise AuthoringError("terminal Stage 11 reviewer identity drifted")
    if tuple(terminal.get("source_paths", ())) != STAGE_PATHS:
        raise AuthoringError(
            "terminal review event is not the combined Stage 11 assignment"
        )
    if len(terminal.get("route_changes", ())) != EXPECTED_STAGE_ROUTE_COUNT:
        raise AuthoringError("terminal Stage 11 route-change count drifted")
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

    stage_units = [
        row
        for row in reading_rows
        if row["review_stage"] == "11" and row["path"] in STAGE_PATHS
    ]
    stage_assets = [
        row
        for row in asset_rows
        if row["review_stage"] == "11"
        and row["assignment_path"] in STAGE_PATHS
    ]
    if (
        len(stage_units) != EXPECTED_STAGE_UNIT_COUNT
        or any(row["review_status"] != "REVIEWED" for row in stage_units)
    ):
        raise AuthoringError("combined Stage 11 unit coverage drifted")
    if (
        len(stage_assets) != EXPECTED_STAGE_ASSET_COUNT
        or any(row["inspection_status"] != "SCREENED" for row in stage_assets)
    ):
        raise AuthoringError("combined Stage 11 asset coverage drifted")

    routes_by_identity: dict[
        tuple[str, str, str, str, str],
        list[dict[str, str]],
    ] = {}
    for row in routes:
        routes_by_identity.setdefault(route_identity(row), []).append(row)

    qualitative_incoming = {
        spec.identity
        for spec in ROUTE_SPECS
        if spec.origin == "incoming"
        and classify_stage11_page_target(spec.identity[3]) == "NONE"
    }
    expected_incoming = {
        spec.identity for spec in ROUTE_SPECS if spec.origin == "incoming"
    }
    observed_incoming_rows: list[dict[str, str]] = []
    observed_mixed_rows: list[dict[str, str]] = []
    for row in routes:
        if (
            row["owning_stage"] == "11"
            or row["closure_scope"] != "CROSS_RANGE"
            or row["status"] != "PENDING"
        ):
            continue
        classification = classify_stage11_page_target(row["literal_target"])
        if (
            classification == "REACHABLE"
            or route_identity(row) in qualitative_incoming
        ):
            observed_incoming_rows.append(row)
        elif classification == "MIXED":
            observed_mixed_rows.append(row)

    observed_incoming = {
        route_identity(row) for row in observed_incoming_rows
    }
    if (
        len(observed_incoming_rows) != EXPECTED_SPEC_COUNTS["incoming"]
        or observed_incoming != expected_incoming
    ):
        missing = sorted(expected_incoming - observed_incoming)
        extra = sorted(observed_incoming - expected_incoming)
        raise AuthoringError(
            "incoming Stage 11 route set differs from the governed map: "
            f"missing={missing!r} extra={extra!r}"
        )
    for row in observed_incoming_rows:
        require_pending_route(row, label="incoming Stage 11")

    expected_mixed = set(DEFERRED_MIXED_INCOMING_IDENTITIES)
    observed_mixed = {route_identity(row) for row in observed_mixed_rows}
    if (
        len(observed_mixed_rows) != EXPECTED_DEFERRED_MIXED_COUNT
        or observed_mixed != expected_mixed
    ):
        missing = sorted(expected_mixed - observed_mixed)
        extra = sorted(observed_mixed - expected_mixed)
        raise AuthoringError(
            "mixed incoming Stage 11 route set drifted: "
            f"missing={missing!r} extra={extra!r}"
        )
    for row in observed_mixed_rows:
        require_pending_route(row, label="deferred mixed incoming")

    expected_within = {
        spec.identity for spec in ROUTE_SPECS if spec.origin == "within"
    }
    observed_within_rows = [
        row
        for row in routes
        if row["owning_stage"] == "11"
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
            "Stage 11 WITHIN_STAGE route set differs from the governed map: "
            f"missing={missing!r} extra={extra!r}"
        )
    for row in observed_within_rows:
        require_pending_route(row, label="Stage 11 WITHIN_STAGE")

    expected_cross = set(UNTOUCHED_CROSS_RANGE_IDENTITIES)
    observed_cross_rows = [
        row
        for row in routes
        if row["owning_stage"] == "11"
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
            "Stage 11 CROSS_RANGE partition drifted: "
            f"missing={missing!r} extra={extra!r}"
        )
    for row in observed_cross_rows:
        require_pending_route(row, label="untouched CROSS_RANGE")

    if (
        len(observed_within_rows) + len(observed_cross_rows)
        != EXPECTED_STAGE_ROUTE_COUNT
    ):
        raise AuthoringError("Stage 11 route partition is not exhaustive")

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
                before["owning_stage"] != "11"
                or before["closure_scope"] != "WITHIN_STAGE"
            ):
                raise AuthoringError(
                    "within-stage route metadata drifted: "
                    f"{spec.identity!r}"
                )
        elif (
            before["owning_stage"] == "11"
            or before["closure_scope"] != "CROSS_RANGE"
        ):
            raise AuthoringError(
                "incoming route metadata drifted: "
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
    preserved_ids = {
        row["route_id"]
        for row in (*observed_cross_rows, *observed_mixed_rows)
    }
    if matched_route_ids & preserved_ids:
        raise AuthoringError("a preserved route entered the update set")

    return {
        "schema_version": 1,
        "proposal_kind": "ROUTE_RESOLUTION",
        "coordinator_id": "ch07-mechanisms-route-closure-e2",
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
                f"Chapter 7 route specification check failed: {exc}",
                file=sys.stderr,
            )
            return 1
        print(
            "Chapter 7 route specification valid: "
            f"incoming={EXPECTED_SPEC_COUNTS['incoming']} "
            f"within={EXPECTED_SPEC_COUNTS['within']} "
            f"untouched-cross={EXPECTED_UNTOUCHED_CROSS_RANGE_COUNT} "
            f"deferred-mixed={EXPECTED_DEFERRED_MIXED_COUNT} "
            f"spec-sha256={spec_digest} "
            f"preservation-sha256={preservation_digest}"
        )
        return 0
    if len(sys.argv) != 2:
        print(
            "usage: author_ch07_mechanisms_routes.py OUTPUT_JSON",
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
        print(f"Chapter 7 route authoring failed: {exc}", file=sys.stderr)
        return 1
    print(
        f"Wrote {output_path} with {len(proposal['route_updates'])} "
        "identity-keyed route closures."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
