#!/usr/bin/env python3
"""Author the governed Stage 12 route-resolution proposal.

The helper closes the 24 previously discovered incoming routes whose literal
landings were read during the Chapter 8 main/Notes sequential review, all 23
new Stage-12 WITHIN_STAGE routes, and the 10 Stage-12 CROSS_RANGE routes whose
literal page targets actually land inside the reviewed Stage-12 sources.
Routes are frozen by both their current global route ID and immutable
five-field identity:

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
EXPECTED_REACHABLE_CROSS_RANGE_COUNT = 10
EXPECTED_UPDATE_COUNT = 57
EXPECTED_OUTGOING_COUNT = 46
EXPECTED_OUTGOING_IDENTITY_SHA256 = (
    "TO_BE_FILLED"
)
EXPECTED_SPEC_SHA256 = (
    "TO_BE_FILLED"
)
EXPECTED_PRESERVATION_SHA256 = (
    "TO_BE_FILLED"
)

ROUTE_ID = re.compile(r"^R[0-9]{6}$")
UNIT_ID = re.compile(r"^U[0-9]{6}$")
ASSET_ID = re.compile(r"^A[0-9]{6}$")


class AuthoringError(ValueError):
    """The current audit state cannot safely receive this proposal."""


@dataclass(frozen=True)
class RouteSpec:
    """One source-grounded route closure."""

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
    (
        "R000712",
        "U002099",
        "",
        "PAGE",
        "page 377",
        "Observed paired eddies behind an obstacle",
        "U002090-U002091",
        "A001129",
        (
            "The landing is the labeled photographic catalog of physical "
            "fluid flows and its caption; the obstacle-wake panels visibly "
            "supply the paired-eddy comparison, not a native update law."
        ),
    ),
    (
        "R000713",
        "U002100",
        "",
        "PAGE",
        "page 377",
        "Flow phenomena at changing speed",
        "U002090-U002091",
        "A001129",
        (
            "The landing is the labeled photographic catalog of laminar, "
            "vortical, turbulent, and related flow regimes; it is "
            "observational comparison evidence rather than a transition "
            "rule."
        ),
    ),
    (
        "R000714",
        "U002116",
        "",
        "PAGE",
        "page 378",
        "Microscopic particle randomness in the lattice-gas example",
        "U002092-U002094",
        "A001130",
        (
            "The landing supplies the discrete triangular-lattice particles, "
            "displayed collision rules, reflecting plate and injection "
            "conditions, together with microscopic and block-averaged views."
        ),
    ),
    (
        "R000715",
        "U002123",
        "",
        "PAGE",
        "page 377",
        "Catalog of fluid-flow patterns",
        "U002090-U002091",
        "A001129",
        (
            "The landing is the reviewed labeled photographic catalog and "
            "caption of typical physical flow patterns; it supplies the "
            "requested comparison catalog without native fluid mechanics."
        ),
    ),
    (
        "R000717",
        "U002166",
        "",
        "SECTION",
        "two sections from now",
        "Mollusc-shell cellular-automaton pigmentation patterns",
        "U002346-U002354",
        "A001169 A001170",
        (
            "The landing compares natural shell pigmentation with "
            "one-dimensional cellular automata, states the line-by-line "
            "neighbor-update hypothesis, and supplies both natural-shell and "
            "complete symmetric-rule visual witnesses."
        ),
    ),
    (
        "R000719",
        "U002204",
        "",
        "SECTION",
        "the next section",
        "Geometry and relative growth rates in plants and animals",
        (
            "U002235-U002238 U002286-U002290 U002292-U002307 "
            "U002334-U002340"
        ),
        "A001158 A001159 A001160 A001161 A001162 A001165",
        (
            "The landing anchors the Growth of Plants and Animals section, "
            "states directly that geometry and relative growth rates "
            "determine the resulting plant forms, then gives the geometric "
            "consequences of differential growth for plant disks, horns and "
            "mollusc shells and the later comparison across animal forms."
        ),
    ),
    (
        "R000720",
        "U002242",
        "",
        "PAGE",
        "the next page",
        "Parameter sequences for three-way branching substitution systems",
        "U002249-U002250",
        "A001150",
        (
            "The landing supplies the reviewed array of graphical three-way "
            "substitution-rule variants and their limiting forms; the "
            "caption identifies relative-length rows and 15-degree angle "
            "increments across each row."
        ),
    ),
    (
        "R000721",
        "U002245",
        "",
        "PAGE",
        "page 403",
        "Examples of natural leaf shapes",
        "U002251-U002252",
        "A001151",
        (
            "The landing supplies the natural-leaf photographic comparison "
            "and caption, including its size range and explicit comparison "
            "to the generated forms on the facing page."
        ),
    ),
    (
        "R000722",
        "U002246",
        "",
        "PAGE",
        "the next page",
        "Substitution-system outlines resembling leaves",
        "U002249-U002250",
        "A001150",
        (
            "The landing supplies nine rows of graphical three-way "
            "substitution rules and limiting leaf-like outlines, with "
            "relative lengths and systematic angle variation stated in the "
            "caption."
        ),
    ),
    (
        "R000723",
        "U002258",
        "",
        "PAGE",
        "the previous pages",
        "Complex leaf-shape substitution patterns",
        "U002249-U002252",
        "A001150 A001151",
        (
            "The two landing clusters pair the complex limiting "
            "substitution patterns and their rule-variation caption with the "
            "reviewed natural-leaf comparison."
        ),
    ),
    (
        "R000724",
        "U002260",
        "",
        "PAGE",
        "the next page",
        "Full parameter array for symmetric binary branching",
        "U002265-U002266",
        "A001153",
        (
            "The landing supplies the full two-parameter array of ten-step "
            "symmetric two-branch substitutions and states how image "
            "position encodes the right-hand branch-tip parameter."
        ),
    ),
    (
        "R000725",
        "U002262",
        "",
        "PAGE",
        "the next page",
        "Symmetric branching parameter array",
        "U002265-U002266",
        "A001153",
        (
            "The landing supplies the full reviewed parameter array and its "
            "captioned correspondence between array position and the "
            "symmetric two-branch substitution rule."
        ),
    ),
    (
        "R000726",
        "U002262",
        "",
        "PAGE",
        "Page 407",
        "Peephole overlap maps over branching-rule parameter space",
        "U002267-U002268",
        "A001154",
        (
            "The landing supplies four peephole-overlap parameter maps, "
            "their black-to-white overlap interpretation, and magnified "
            "nested boundaries."
        ),
    ),
    (
        "R000727",
        "U002283",
        "",
        "PAGE",
        "the top of the facing page",
        "Damping variants of the phyllotaxis concentration model",
        "U002284-U002285",
        "A001157",
        (
            "The landing supplies the 100%, 95%, 75%, 50%, 25%, 5% and 0% "
            "damping variants and explains their memory interpretation and "
            "golden-angle convergence."
        ),
    ),
    (
        "R000728",
        "U002288",
        "",
        "PAGE",
        "page 409",
        "Natural plant geometries using the golden angle",
        "U002275-U002276",
        "A001155",
        (
            "The landing supplies reviewed natural plant arrangements and "
            "states that their differing geometries share an original "
            "successive-element angle close to 137.5 degrees."
        ),
    ),
    (
        "R000729",
        "U002301",
        "",
        "PAGE",
        "the facing page",
        "Differentially grown disk forms",
        "U002293-U002296",
        "A001160",
        (
            "The landing defines radial differences in added material and "
            "shows the corresponding relaxed flat, cup, wavy and "
            "self-overlapping disk forms."
        ),
    ),
    (
        "R000730",
        "U002307",
        "",
        "PAGE",
        "the previous page",
        "Base mollusc-shell growth rule and three examples",
        "U002302-U002305",
        "A001162",
        (
            "The landing states progressive addition at the shell opening, "
            "differential growth and displacement, and supplies the three "
            "reviewed rule/profile/evolution examples."
        ),
    ),
    (
        "R000731",
        "U002312",
        "",
        "PAGE",
        "the previous page",
        "Five shell-growth parameter sweeps",
        "U002306-U002307",
        "A001165",
        (
            "The landing supplies the five labeled sweeps for scale increase, "
            "opening displacement, opening size, opening shape, and "
            "differential material addition."
        ),
    ),
    (
        "R000732",
        "U002317",
        "",
        "PAGE",
        "page 412",
        "Differential-growth disk model",
        "U002293-U002296",
        "A001160",
        (
            "The landing gives the radial material profiles, equal-cell "
            "relaxation condition, and resulting three-dimensional disk "
            "forms."
        ),
    ),
    (
        "R000733",
        "U002352",
        "",
        "PAGE",
        "the bottom of the facing page",
        "Complete symmetric binary nearest-neighbor rule array",
        "U002350-U002352",
        "A001170",
        (
            "The landing supplies the complete labeled array of symmetric "
            "binary nearest-neighbor rules and outputs from random starts, "
            "together with the shell-pattern comparison."
        ),
    ),
    (
        "R000734",
        "U002359",
        "",
        "PAGE",
        "the facing page",
        "Natural animal pigmentation examples",
        "U002357-U002358",
        "A001171",
        (
            "The landing supplies the reviewed natural-animal pigmentation "
            "examples and notes the recurrence of similar patterns across "
            "very different animals."
        ),
    ),
    (
        "R000735",
        "U002364",
        "",
        "PAGE",
        "the next page",
        "Weight-parameter array for pigmentation cellular automata",
        "U002365-U002366",
        "A001173",
        (
            "The landing supplies the full stationary-pattern array and "
            "states the distance-2 and distance-3 weight ranges encoded down "
            "and across the page."
        ),
    ),
    (
        "R000736",
        "U002367",
        "",
        "PAGE",
        "the top of the facing page",
        "Anisotropic stripe-producing pigmentation rules",
        "U002368-U002369",
        "A001174",
        (
            "The landing supplies vertical- and horizontal-stripe "
            "anisotropic evolutions and states how horizontal versus "
            "vertical neighbor weights differ in the two rules."
        ),
    ),
    (
        "R000748",
        "U006899",
        "",
        "PAGE",
        "page 378",
        "cellular-automaton fluids",
        "U002092-U002094",
        "A001130",
        (
            "The landing supplies the triangular-lattice particle cellular "
            "automaton, displayed collision rules, reflecting plate and "
            "particle injection, and both microscopic and block-averaged "
            "velocity views."
        ),
    ),
    (
        "R000750",
        "U006909",
        "",
        "PAGE",
        "page 378",
        "global CA flow results",
        "U002092-U002094",
        "A001130",
        (
            "The landing states that the simple local particle rules produce "
            "the global flow pattern around the plate and supplies both the "
            "individual-particle evolution and its coarse-grained velocity "
            "field."
        ),
    ),
    (
        "R000754",
        "U006917",
        "",
        "PAGE",
        "page 377",
        "Bénard convection",
        "U002090-U002091",
        "A001129",
        (
            "The labeled physical-flow catalog contains the reviewed Bénard "
            "convection panel and caption as observational comparison "
            "evidence; it supplies no native convection state or update law."
        ),
    ),
    (
        "R000759",
        "U006929",
        "",
        "PAGE",
        "page 1012",
        "reaction–diffusion biological form",
        "U006981-U006983",
        "",
        (
            "The landing gives the two-chemical linear reaction-diffusion "
            "equation, wavelength-selective instability, Turing's finite-"
            "difference/random-start construction, nonlinear saturation "
            "boundary, and biological-pattern context."
        ),
    ),
    (
        "R000762",
        "U006934",
        "",
        "PAGE",
        "page 1006",
        "branching-model properties",
        "U006941-U006946",
        "A000038",
        (
            "The landing gives the complex branching parameterization, "
            "existence and connectedness conditions, explicit gap test, "
            "boundary facts, pruning method, and reviewed parameter-space "
            "witness. The extraction does not preserve a clean printed-page "
            "break between pages 1006 and 1007."
        ),
    ),
    (
        "R000769",
        "U006952",
        "",
        "PAGE",
        "page 1011",
        "discrete symmetry",
        "U006972",
        "",
        (
            "The exact page-1011 landing discusses growth schemes, tumors, "
            "pollen, radiolarians, self-assembly, animal behavior, and "
            "regular polyhedral pollen forms; the expected discrete-symmetry "
            "construction is absent."
        ),
    ),
    (
        "R000770",
        "U006952",
        "",
        "PAGE",
        "page 1010",
        "harmonic growth",
        "U006969",
        "",
        (
            "The landing's general constraints on growth state that a "
            "two-dimensional surface remains flat when its local growth "
            "rate is a harmonic function and contrast the corresponding "
            "three-dimensional constraint."
        ),
    ),
    (
        "R000774",
        "U006969",
        "",
        "PAGE",
        "page 1007",
        "harmonic flat growth",
        "U006952",
        "",
        (
            "The landing gives the local-growth transformation and states "
            "that a flat surface remains flat precisely when the logarithm "
            "of the growth factor is harmonic. The extraction does not "
            "preserve a clean printed-page break between pages 1006 and "
            "1007; the following-page visual A000049 is not claimed."
        ),
    ),
    (
        "R000781",
        "U006975",
        "",
        "PAGE",
        "page 428",
        "shell-pattern CA",
        "U002364-U002366",
        "A001173",
        (
            "The landing gives the distance-weighted two-dimensional "
            "cellular-automaton pigmentation model and its full reviewed "
            "array of stationary shell-like patterns across the two "
            "weight parameters."
        ),
    ),
    (
        "R000784",
        "U006981",
        "",
        "PAGE",
        "page 1004",
        "diffusion in development",
        "U006929",
        "",
        (
            "The landing records the early chemical-messenger hypothesis "
            "for embryo growth and Turing's reaction-diffusion model for "
            "biological pigmentation and structural pattern formation."
        ),
    ),
)

ROUTE_SPECS = tuple(route_spec(*row) for row in _ROUTE_DATA)

INCOMING_ROUTE_IDS = tuple(
    spec.route_id for spec in ROUTE_SPECS[:EXPECTED_INCOMING_COUNT]
)
WITHIN_STAGE_ROUTE_IDS = (
    "R000712",
    "R000713",
    "R000714",
    "R000715",
    "R000717",
    *tuple(f"R{number:06d}" for number in range(719, 737)),
)
REACHABLE_CROSS_RANGE_ROUTE_IDS = (
    "R000748",
    "R000750",
    "R000754",
    "R000759",
    "R000762",
    "R000769",
    "R000770",
    "R000774",
    "R000781",
    "R000784",
)
STAGE_CLOSURE_ROUTE_IDS = (
    *WITHIN_STAGE_ROUTE_IDS,
    *REACHABLE_CROSS_RANGE_ROUTE_IDS,
)
OUTGOING_ROUTE_IDS = (
    "R000709",
    "R000710",
    "R000711",
    "R000716",
    "R000718",
    *tuple(
        f"R{number:06d}"
        for number in range(737, 788)
        if f"R{number:06d}" not in REACHABLE_CROSS_RANGE_ROUTE_IDS
    ),
)
STAGE_ROUTE_IDS = tuple(
    f"R{number:06d}" for number in range(709, 788)
)


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
    """Return the canonical digest payload for every deferred route."""

    return {
        "preexisting_stage13_route": {
            "route_id": DEFERRED_ROUTE_ID,
            "identity": list(DEFERRED_ROUTE_IDENTITY),
            "boundary": DEFERRED_ROUTE_BOUNDARY,
        },
        "stage12_outgoing_route_ids": list(OUTGOING_ROUTE_IDS),
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
    if (
        tuple(route_ids[:EXPECTED_INCOMING_COUNT]) != INCOMING_ROUTE_IDS
        or tuple(route_ids[EXPECTED_INCOMING_COUNT:])
        != STAGE_CLOSURE_ROUTE_IDS
    ):
        raise AuthoringError("incoming/Stage-12 route partition drifted")
    if (
        len(INCOMING_ROUTE_IDS) != EXPECTED_INCOMING_COUNT
        or len(WITHIN_STAGE_ROUTE_IDS) != EXPECTED_WITHIN_COUNT
        or len(REACHABLE_CROSS_RANGE_ROUTE_IDS)
        != EXPECTED_REACHABLE_CROSS_RANGE_COUNT
        or len(OUTGOING_ROUTE_IDS) != EXPECTED_OUTGOING_COUNT
        or len(STAGE_ROUTE_IDS) != EXPECTED_STAGE_ROUTE_COUNT
        or set(WITHIN_STAGE_ROUTE_IDS) & set(OUTGOING_ROUTE_IDS)
        or set(REACHABLE_CROSS_RANGE_ROUTE_IDS) & set(OUTGOING_ROUTE_IDS)
        or set(WITHIN_STAGE_ROUTE_IDS)
        & set(REACHABLE_CROSS_RANGE_ROUTE_IDS)
        or set(WITHIN_STAGE_ROUTE_IDS)
        | set(REACHABLE_CROSS_RANGE_ROUTE_IDS)
        | set(OUTGOING_ROUTE_IDS)
        != set(STAGE_ROUTE_IDS)
    ):
        raise AuthoringError("Stage 12 route partition is not exhaustive")
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


def outgoing_identity_payload(
    routes_by_id: dict[str, dict[str, str]],
) -> list[dict[str, Any]]:
    """Return the frozen immutable identities of Stage 12 outgoing routes."""

    return [
        {
            "route_id": route_id,
            "identity": list(route_identity(routes_by_id[route_id])),
        }
        for route_id in OUTGOING_ROUTE_IDS
    ]


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
    """Build the exact 57-row Stage 12 route-resolution proposal."""

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

    observed_stage_routes = {
        row["route_id"]: row
        for row in routes
        if row["owning_stage"] == "12"
    }
    if (
        len(observed_stage_routes) != EXPECTED_STAGE_ROUTE_COUNT
        or set(observed_stage_routes) != set(STAGE_ROUTE_IDS)
    ):
        raise AuthoringError("Stage 12 route-ID allocation drifted")
    observed_within = {
        route_id
        for route_id, row in observed_stage_routes.items()
        if row["closure_scope"] == "WITHIN_STAGE"
    }
    observed_cross_range = {
        route_id
        for route_id, row in observed_stage_routes.items()
        if row["closure_scope"] == "CROSS_RANGE"
    }
    if (
        observed_within != set(WITHIN_STAGE_ROUTE_IDS)
        or observed_cross_range
        != set(REACHABLE_CROSS_RANGE_ROUTE_IDS) | set(OUTGOING_ROUTE_IDS)
    ):
        raise AuthoringError("Stage 12 route-scope partition drifted")
    outgoing_digest = payload_sha256(
        outgoing_identity_payload(routes_by_id)
    )
    if outgoing_digest != EXPECTED_OUTGOING_IDENTITY_SHA256:
        raise AuthoringError(
            "Stage 12 outgoing route identities drifted: "
            f"{outgoing_digest} != {EXPECTED_OUTGOING_IDENTITY_SHA256}"
        )
    for route_id in OUTGOING_ROUTE_IDS:
        require_pending_route(
            routes_by_id[route_id],
            label=f"outgoing {route_id}",
        )

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
        if spec.route_id in WITHIN_STAGE_ROUTE_IDS:
            if (
                before["owning_stage"] != "12"
                or before["closure_scope"] != "WITHIN_STAGE"
            ):
                raise AuthoringError(
                    f"governed route is not WITHIN_STAGE: {spec.route_id}"
                )
        elif spec.route_id in REACHABLE_CROSS_RANGE_ROUTE_IDS:
            if (
                before["owning_stage"] != "12"
                or before["closure_scope"] != "CROSS_RANGE"
            ):
                raise AuthoringError(
                    "governed Stage 12 route is not CROSS_RANGE: "
                    f"{spec.route_id}"
                )
        elif (
            spec.route_id not in INCOMING_ROUTE_IDS
            or before["owning_stage"] == "12"
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
        "coordinator_id": "ch08-everyday-route-closure-e2",
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
            "Chapter 8 route specification valid: "
            f"incoming={EXPECTED_INCOMING_COUNT} "
            f"within={EXPECTED_WITHIN_COUNT} "
            "reachable-cross-range="
            f"{EXPECTED_REACHABLE_CROSS_RANGE_COUNT} "
            f"preserved-outgoing={EXPECTED_OUTGOING_COUNT} "
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
        "route-ID-and-identity-keyed closures."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
