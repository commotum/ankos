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
EXPECTED_SPEC_SHA256 = (
    "17c340e52471357e5bbc1c26d9579312aea0b2c015a0bb3dacb451ab006ee5cf"
)
EXPECTED_CROSS_RANGE_SHA256 = (
    "d6ae9a4090e14a8a2035a99f07ce1445f158c0ec4fda8f87937593d6f0683034"
)
UNIT_ID = re.compile(r"^U[0-9]{6}$")
ASSET_ID = re.compile(r"^A[0-9]{6}$")
PRINTED_PAGE = re.compile(r"\bpages?\s+([0-9]{2,4})", re.IGNORECASE)
CHAPTER6_PRINTED_PAGE_RANGE = range(223, 297)


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


ROUTE_SPECS: tuple[RouteSpec, ...] = (
    route_spec(
        "incoming",
        "U004871",
        "",
        "PAGE",
        "11 of the 15 kinds from page 292",
        "persistent-structure definitions and their relation to Rule 110 behavior",
        "U001562 U001567 U001568",
        "A001023",
        (
            "Resolved printed page 292 to U001562/U001567-U001568 and "
            "A001023. The target identifies the rule-110 background and "
            "the labelled persistent-structure family, including extension "
            "and phase qualifications; collision behavior remains on later "
            "pages."
        ),
    ),
    route_spec(
        "incoming",
        "U004953",
        "",
        "PAGE",
        "see page 232",
        "elementary cellular automata with random initial conditions",
        (
            "U001259 U001264 U001269 U001270 U001271 "
            "U001272 U001273 U001278 U001279 U001280"
        ),
        "A000941",
        (
            "Resolved printed page 232 to U001272-U001273/A000941, joined "
            "to the four-class definitions in U001259/U001264/U001269-"
            "U001271/U001278-U001280. The page surveys symmetric elementary "
            "rules from random initial conditions; it is not a new rule "
            "numbering convention."
        ),
    ),
    route_spec(
        "incoming",
        "U005149",
        "",
        "PAGE",
        "details of rule 110 ... on page 229",
        "Rule 110 detailed mechanics and behavior",
        "U001254 U001255 U001256 U001257 U001258",
        "A000935 A000936",
        (
            "Resolved printed page 229 to U001254-U001258/A000935-A000936. "
            "It directly shows rule 110 from random initial conditions, "
            "localized structures, their motion and interaction, and the "
            "700-step continuation. The target refers back to page 32 for "
            "the lookup table, so it does not independently restate all "
            "eight rule outputs."
        ),
    ),
    route_spec(
        "incoming",
        "U005149",
        "",
        "PAGE",
        "Localized structures ... are shown on page 292.",
        "Rule 110 localized-structure definitions",
        "U001562 U001567 U001568",
        "A001023",
        (
            "Resolved printed page 292 to U001562/U001567-U001568/A001023. "
            "These are the labelled stationary, moving, and extendible "
            "rule-110 structures on the periodic background; later "
            "collision panels are not substituted for the definitions."
        ),
    ),
    route_spec(
        "incoming",
        "U005233",
        "",
        "PAGE",
        "The Game of Life ... (see page 249)",
        "Conway Life transition, neighborhood, and seed mechanics",
        "U001329 U001336 U001338 U001339 U001340 U001341",
        "A000960 A000962 A000963 A000964",
        (
            "Resolved printed page 249 to U001329/U001336/U001338-U001341 "
            "and A000960/A000962-A000964. U001341 gives the exact "
            "eight-neighbor Life transition and code 224 while the panels "
            "show the evolution and history-slice representation. The page "
            "does not prescribe one privileged seed."
        ),
    ),
    route_spec(
        "incoming",
        "U005233",
        "",
        "PAGE",
        "code 20 k = 2, r = 2 totalistic rule from page 283",
        "binary range-2 totalistic code 20 lookup and code convention",
        "U001519 U001525 U001526 U001531 U001532 U001533",
        "A001012 A001015",
        (
            "Resolved printed page 283 to U001519/U001525-U001526/"
            "U001531-U001533 and A001012/A001015. It identifies the binary "
            "next-nearest-neighbor code-20 preset and its exhaustive "
            "small-seed survival survey. The page supplies neither the "
            "totalistic digit ordering nor a complete lookup table, so "
            "those mechanics remain source-side context."
        ),
    ),
    route_spec(
        "incoming",
        "U005236",
        "",
        "PAGE",
        "limited number of cells (compare page 259)",
        "finite additive cellular-automaton correspondence",
        (
            "U001383 U001384 U001385 U001386 U001387 "
            "U001388 U001389 U001390 U001391"
        ),
        "A000975",
        (
            "Resolved printed page 259 to U001383-U001391/A000975. The "
            "target defines cyclic finite-size cellular automata, their "
            "2^n state bound, inevitable repetition, and size-dependent "
            "periods. It does not specialize the native rule to an additive "
            "one; that qualification comes from the route origin."
        ),
    ),
    route_spec(
        "incoming",
        "U005288",
        "",
        "PAGE",
        "page 231",
        "four cellular-automaton behavior classes",
        (
            "U001259 U001260 U001262 U001263 U001264 U001265 U001266 "
            "U001267 U001268 U001269 U001270 U001271 U001278 U001279 "
            "U001280"
        ),
        "A000937 A000938 A000939 A000940",
        (
            "Resolved printed page 231 to U001259-U001280 and "
            "A000937-A000940, restricted to the classification statement "
            "and definitions: uniform class 1, fixed or short-period class "
            "2, apparently random class 3, and localized interacting class "
            "4 behavior from random initial conditions."
        ),
    ),
    route_spec(
        "incoming",
        "U005342",
        "",
        "PAGE",
        "page 263",
        "Rule 22 complex initial conditions",
        "U001405 U001406 U001407 U001408 U001409 U001410",
        "A000979 A000980",
        (
            "Resolved printed page 263 to U001405-U001410/A000979-A000980. "
            "The target compares a single-cell nested rule-22 history with "
            "several still-simple seeds and identifies the final illustrated "
            "seed as producing random-looking behavior. It does not claim "
            "that every finite seed does so."
        ),
    ),
    route_spec(
        "incoming",
        "U005629",
        "",
        "PAGE",
        "page 277",
        "infinite path-tree unfolding of networks",
        "U001492 U001493 U001494 U001495 U001496 U001497 U001498",
        "A001007",
        (
            "Resolved printed page 277 to U001492-U001498/A001007. The "
            "finite labelled networks compactly denote all allowed "
            "sequences as paths, including the all-sequence start, the "
            "one-loop rule-255 image, and the two-node rule-4 image. An "
            "explicit infinite path tree is the unfolding of this network, "
            "not an additional native construction in the target."
        ),
    ),
    route_spec(
        "incoming",
        "U006236",
        "",
        "PAGE",
        "page 259",
        "finite-size cellular-automaton comparison for homogeneous-network automata",
        (
            "U001383 U001384 U001385 U001386 U001387 "
            "U001388 U001389 U001390 U001391"
        ),
        "A000975",
        (
            "Resolved printed page 259 to U001383-U001391/A000975, the "
            "finite cyclic one-dimensional cellular-automaton baseline with "
            "2^n possible states and eventual repetition. The target does "
            "not discuss homogeneous-network carriers, so the closure "
            "preserves the route as a comparison rather than importing a "
            "network update law."
        ),
    ),
    route_spec(
        "incoming",
        "U006238",
        "",
        "SECTION",
        "Chapter 6",
        "behavior classes of random Boolean networks",
        (
            "U001259 U001260 U001262 U001263 U001264 U001265 U001266 "
            "U001267 U001268 U001269 U001270 U001271 U001278 U001279 "
            "U001280"
        ),
        "A000937 A000938 A000939 A000940",
        (
            "Resolved the Chapter 6 classification target to "
            "U001259-U001280/A000937-A000940. These units define four "
            "behavior classes for cellular automata started from random "
            "initial conditions. Chapter 6 does not independently define "
            "random Boolean networks or establish a network-specific class "
            "test, so the target is only the cited comparison framework."
        ),
    ),
    route_spec(
        "incoming",
        "U006284",
        "",
        "PAGE",
        "See also page 266",
        "one-dimensional constraint periodicity comparison",
        (
            "U001425 U001426 U001427 U001428 "
            "U001429 U001430 U001431"
        ),
        "A000983 A000984 A000985 A000986",
        (
            "Resolved printed page 266 to U001425-U001431/"
            "A000983-A000986. It gives rule-30 fixed-block initial "
            "conditions with simple periodic behavior and explicitly joins "
            "their discovery to constraint satisfaction. The target is a "
            "periodicity comparison, not the general constraint solver."
        ),
    ),
    route_spec(
        "incoming",
        "U006285",
        "",
        "PAGE",
        "page 225",
        "cellular-automaton convergence to invariant configurations",
        "U001237 U001238 U001239 U001240",
        "A000927",
        (
            "Resolved printed page 225 to U001237-U001240/A000927. It shows "
            "rules 4, 108, 218, and 232 converging from random starts to "
            "fixed or short-period structure sets whose placement depends "
            "on the input. The target does not assert a unique invariant "
            "configuration for every rule."
        ),
    ),
    route_spec(
        "within",
        "U001302",
        "",
        "PAGE",
        "page 232",
        "rule columns restricting possible behavior classes",
        "U001272 U001273",
        "A000941",
        (
            "Resolved printed page 232 to U001272-U001273/A000941, the "
            "ordered survey of symmetric nearest-neighbor binary rules that "
            "leave all-white fixed. The source page is the exact column "
            "population to which U001302's class-1-or-2 restriction applies."
        ),
    ),
    route_spec(
        "within",
        "U001326",
        "",
        "PAGE",
        "page 248",
        "one-dimensional slices of two-dimensional evolution",
        (
            "U001324 U001325 U001326 U001327 U001330 "
            "U001331 U001332 U001333 U001334 U001335"
        ),
        "A000957 A000958 A000959",
        (
            "Resolved printed page 248 to U001324-U001335/"
            "A000957-A000959. The full-state panels establish the 2D "
            "evolutions and U001334-U001335/A000959 give the time-stacked "
            "one-dimensional slices used to compare their classes with 1D "
            "cellular automata."
        ),
    ),
    route_spec(
        "within",
        "U001327",
        "",
        "PAGE",
        "page 248",
        "class-4 two-dimensional slice examples",
        (
            "U001324 U001325 U001326 U001327 U001330 "
            "U001331 U001332 U001333 U001334 U001335"
        ),
        "A000957 A000958 A000959",
        (
            "Resolved printed page 248 to U001324-U001335/"
            "A000957-A000959. U001334-U001335 identify class-3 and class-4 "
            "slice appearances; U001327 limits the class-4 examples to "
            "repetitive backgrounds. The slices are observers of the 2D "
            "rules, not new 1D update laws."
        ),
    ),
    route_spec(
        "within",
        "U001327",
        "",
        "PAGE",
        "page 229",
        "rule-110 repetitive background comparison",
        "U001254 U001255 U001256 U001257 U001258",
        "A000935 A000936",
        (
            "Resolved printed page 229 to U001254-U001258/A000935-A000936, "
            "which show rule 110 organizing a random start into localized "
            "structures on an ordered background. The exact 14-cell, "
            "7-step background is specified later in U001558/U001561, so "
            "it is not retroactively attributed to this page."
        ),
    ),
    route_spec(
        "within",
        "U001329",
        "",
        "PAGE",
        "page 249",
        "Game of Life and its one-dimensional slice",
        "U001329 U001336 U001338 U001339 U001340 U001341",
        "A000960 A000962 A000963 A000964",
        (
            "Resolved printed page 249 to U001329/U001336/U001338-U001341 "
            "and A000960/A000962-A000964. The target includes Life's exact "
            "eight-neighbor transition and the fading-history slice that "
            "makes its class-4 comparison visible."
        ),
    ),
    route_spec(
        "within",
        "U001433",
        "",
        "PAGE",
        "page 255",
        "limited-size cellular-automaton systems",
        "U001367 U001368 U001369 U001370 U001371",
        "A000971",
        (
            "Resolved printed page 255 to U001367-U001371/A000971. The "
            "six-position cyclic-addition system gives the finite-state "
            "pigeonhole argument and at-most-six repetition bound used as "
            "the limited-size model; it is not itself a cellular automaton."
        ),
    ),
    route_spec(
        "within",
        "U001450",
        "",
        "PAGE",
        "page 263",
        "rule-22 initial conditions yielding rule-90 behavior",
        "U001405 U001406 U001407 U001408 U001409 U001410",
        "A000979 A000980",
        (
            "Resolved printed page 263 to U001405-U001410/A000979-A000980. "
            "The target establishes which shown simple rule-22 seeds remain "
            "nested and which produce random-looking behavior; it does not "
            "give a general block code from rule 22 to rule 90."
        ),
    ),
    route_spec(
        "within",
        "U001463",
        "",
        "PAGE",
        "page 264",
        "additivity and superposition",
        "U001411 U001412 U001413 U001414 U001415",
        "A000981",
        (
            "Resolved printed page 264 to U001411-U001415/A000981. The rule-"
            "90 panels and caption state that any finite-region initial "
            "condition is a superposition of translated single-cell nested "
            "histories, which is the exact additive comparison used here."
        ),
    ),
    route_spec(
        "within",
        "U001464",
        "",
        "PAGE",
        "page 264",
        "additivity and superposition",
        "U001411 U001412 U001413 U001414 U001415",
        "A000981",
        (
            "Resolved printed page 264 to U001411-U001415/A000981. The "
            "target supplies the empirical and textual superposition "
            "property for rule 90; U001464's generalized conclusion about "
            "all additive rules remains supported by its own source text."
        ),
    ),
    route_spec(
        "within",
        "U001522",
        "",
        "PAGE",
        "page 252",
        "moving structures and information communication",
        "U001353 U001354 U001355 U001356 U001357",
        "",
        (
            "Resolved printed page 252 to U001353-U001357. These units "
            "distinguish localized information retention in class 2, "
            "long-range spread in class 3, and conditional communication by "
            "moving localized structures in class 4. No separate message-"
            "passing update rule is introduced."
        ),
    ),
    route_spec(
        "within",
        "U001540",
        "",
        "PAGE",
        "page 268",
        "systematic constraint method for all fixed-period structures",
        "U001434 U001440 U001441",
        "A000989",
        (
            "Resolved printed page 268 to U001434/U001440-U001441/A000989, "
            "the exhaustive list of rule-30 configurations with periods at "
            "most ten and the stated period-11 width. The page demonstrates "
            "the result of a systematic search but does not transcribe the "
            "constraint-solving algorithm."
        ),
    ),
    route_spec(
        "within",
        "U001542",
        "",
        "PAGE",
        "page 282",
        "code-357 cellular automaton",
        "U001517 U001525 U001527 U001528 U001531",
        "A001013",
        (
            "Resolved printed page 282 to U001517/U001525/U001527-"
            "U001528/U001531 and A001013. The target identifies the "
            "three-color nearest-neighbor code-357 class-4 preset and its "
            "persistent-structure behavior; it does not give a full rule "
            "table."
        ),
    ),
    route_spec(
        "within",
        "U001544",
        "",
        "PAGE",
        "page 282",
        "code-357 cellular automaton",
        "U001517 U001525 U001527 U001528 U001531",
        "A001013",
        (
            "Resolved printed page 282 to the code-357 identity and witness "
            "at U001517/U001525/U001527-U001528/U001531/A001013. The later "
            "seed survey in U001544 is therefore joined to the correct "
            "preset without treating the survey as rule mechanics."
        ),
    ),
    route_spec(
        "within",
        "U001548",
        "",
        "PAGE",
        "page 282",
        "code-1329 cellular automaton",
        "U001517 U001525 U001529 U001530 U001531",
        "A001014",
        (
            "Resolved printed page 282 to U001517/U001525/U001529-"
            "U001531/A001014, which identify the three-color nearest-"
            "neighbor code-1329 class-4 preset and show its persistent "
            "structures. The full lookup table is not printed there."
        ),
    ),
    route_spec(
        "within",
        "U001550",
        "",
        "PAGE",
        "page 282",
        "code-1329 cellular automaton",
        "U001517 U001525 U001529 U001530 U001531",
        "A001014",
        (
            "Resolved printed page 282 to the code-1329 identity and witness "
            "at U001517/U001525/U001529-U001531/A001014. U001550's later "
            "structure survey is thus tied to the right preset without "
            "promoting a visual behavior panel into an update table."
        ),
    ),
    route_spec(
        "within",
        "U001563",
        "",
        "PAGE",
        "page 293",
        "rule-110 unbounded-growth example",
        "U001563 U001569 U001570",
        "A001024",
        (
            "Resolved printed page 293 to U001563/U001569-U001570/A001024. "
            "The target gives the width-41 seed embedded in the rule-110 "
            "background, the 77-step production cycle, central displacement, "
            "and left/right output spacings."
        ),
    ),
    route_spec(
        "within",
        "U001564",
        "",
        "PAGE",
        "pages 294–296",
        "rule-110 structure collisions",
        (
            "U001564 U001565 U001566 U001571 U001572 "
            "U001573 U001574 U001575 U001576"
        ),
        "A001025 A001026 A001027",
        (
            "Resolved printed pages 294-296 to U001564-U001566/"
            "U001571-U001576 and A001025-A001027. They show separation-"
            "dependent (o)/(j), (e)/(o), and long (l)/(i) collisions and "
            "bound the claim to observed interaction outcomes, not a closed "
            "collision algebra."
        ),
    ),
    route_spec(
        "within",
        "U001572",
        "",
        "PAGE",
        "page 292",
        "rule-110 persistent-structure labels",
        "U001562 U001567 U001568",
        "A001023",
        (
            "Resolved the page-292 labels used by the (o)/(j) collision to "
            "U001562/U001567-U001568/A001023. The labelled figure is the "
            "identity source; the page-294 panel remains the interaction "
            "witness."
        ),
    ),
    route_spec(
        "within",
        "U001574",
        "",
        "PAGE",
        "page 292",
        "rule-110 persistent-structure labels",
        "U001562 U001567 U001568",
        "A001023",
        (
            "Resolved the page-292 labels (e) and (o) to "
            "U001562/U001567-U001568/A001023. This keeps structure identity "
            "separate from the later collision result."
        ),
    ),
    route_spec(
        "within",
        "U001576",
        "",
        "PAGE",
        "page 292",
        "rule-110 persistent-structure labels",
        "U001562 U001567 U001568",
        "A001023",
        (
            "Resolved the page-292 labels (l) and (i) to "
            "U001562/U001567-U001568/A001023. The 4300-step outcome remains "
            "evidence about their collision, not part of either structure's "
            "definition."
        ),
    ),
    route_spec(
        "within",
        "U006341",
        "",
        "PAGE",
        "page 226",
        "printed source discussion of random-seed pattern densities",
        "U001241 U001242 U001243 U001244",
        "A000928 A000929",
        (
            "Resolved printed page 226 to U001241-U001244/A000928-A000929. "
            "The target shows rule 126 continuing indefinitely with "
            "random-looking behavior and small organized structures. It "
            "does not print the numerical long-run densities tabulated by "
            "the Notes source."
        ),
    ),
    route_spec(
        "within",
        "U006348",
        "",
        "PAGE",
        "page 232",
        "printed elementary-rule examples",
        "U001272 U001273",
        "A000941",
        (
            "Resolved printed page 232 to U001272-U001273/A000941, the "
            "complete illustrated sequence of symmetric nearest-neighbor "
            "binary rules satisfying the all-white fixed-state condition. "
            "The Notes formula selects rule numbers from this page."
        ),
    ),
    route_spec(
        "within",
        "U006348",
        "",
        "PAGE",
        "page 235",
        "printed states-of-matter and class-4 discussion",
        "U001281 U001282 U001283 U001284 U001285",
        "",
        (
            "Resolved printed page 235 to U001281-U001285. These units "
            "compare visual behavior classes with material and biological "
            "classifications, explain correlation with detailed properties, "
            "and introduce the following three-color class-4 examples. The "
            "analogy is not a material-state simulation."
        ),
    ),
    route_spec(
        "within",
        "U006348",
        "",
        "PAGE",
        "page 236",
        "three-color totalistic class-4 rule 1815 example",
        "U001285 U001286 U001287",
        "A000944",
        (
            "Resolved printed page 236 to U001285-U001287/A000944. The "
            "target identifies code 1815 as one of the three-color nearest-"
            "neighbor totalistic class-4 examples and supplies its 1500-"
            "step random-start witness, not a lookup table."
        ),
    ),
    route_spec(
        "within",
        "U006348",
        "",
        "PAGE",
        "page 237",
        "three-color totalistic class-4 rule 2007 example",
        "U001285 U001288 U001289",
        "A000945",
        (
            "Resolved printed page 237 to U001285/U001288-U001289/A000945. "
            "The target identifies code 2007 in the same three-color "
            "nearest-neighbor totalistic class-4 survey and supplies the "
            "long random-start witness."
        ),
    ),
    route_spec(
        "within",
        "U006348",
        "",
        "PAGE",
        "page 282",
        "three-color totalistic class-4 rule examples 357 and 1329",
        (
            "U001517 U001525 U001526 U001527 "
            "U001528 U001529 U001530 U001531"
        ),
        "A001012 A001013 A001014",
        (
            "Resolved printed page 282 to U001517/U001525-U001531 and "
            "A001012-A001014. It identifies code 357 and code 1329 as "
            "three-color nearest-neighbor class-4 presets alongside the "
            "binary range-2 code 20 example. The panels establish behavior, "
            "not complete rule tables."
        ),
    ),
    route_spec(
        "within",
        "U006350",
        "",
        "PAGE",
        "page 240",
        "printed undecidability discussion",
        (
            "U001293 U001298 U001299 U001300 U001301 U001302"
        ),
        "A000948 A000949 A000950 A000951",
        (
            "Resolved printed page 240 to U001293/U001298-U001302 and "
            "A000948-A000951. The target presents borderline class "
            "assignments and says that in most cases one must run the rule "
            "to determine its class. It does not itself prove the stronger "
            "formal undecidability result supplied by the Notes source."
        ),
    ),
    route_spec(
        "within",
        "U006350",
        "",
        "PAGE",
        "page 244",
        "printed continuous-cellular-automaton discussion",
        (
            "U001310 U001311 U001312 U001313 U001314 U001315 U001316 "
            "U001317 U001318 U001319 U001320 U001321 U001322 U001323"
        ),
        "A000953 A000954 A000955 A000956",
        (
            "Resolved printed page 244 to U001310-U001323/"
            "A000953-A000956. U001316 specifies the continuous averaging, "
            "constant addition, and fractional-part step; U001323 records "
            "the class-4 variants and the neighbor-difference display. The "
            "smooth parameter is a control, not a new update schedule."
        ),
    ),
    route_spec(
        "within",
        "U006351",
        "",
        "PAGE",
        "page 249",
        "printed Game of Life construction",
        "U001329 U001336 U001338 U001339 U001340 U001341",
        "A000960 A000962 A000963 A000964",
        (
            "Resolved printed page 249 to U001329/U001336/U001338-U001341 "
            "and A000960/A000962-A000964. U001341 is the exact Life "
            "eight-neighbor transition and the panels show its evolution "
            "and row-history observer."
        ),
    ),
    route_spec(
        "within",
        "U006351",
        "",
        "PAGE",
        "page 964",
        "localized structures in Life",
        "U006351 U006352 U006353 U006354 U006355",
        "",
        (
            "Resolved the printed-page-964 target to U006351-U006355. The "
            "page gives dense-array and sparse-position Life step "
            "implementations and U006351 states that many localized "
            "structures have been identified. It does not inventory or "
            "define those structures; the later page-979/980 examples are "
            "not silently substituted for this literal target."
        ),
    ),
    route_spec(
        "within",
        "U006362",
        "",
        "PAGE",
        "page 251",
        "printed perturbation-propagation properties",
        (
            "U001343 U001344 U001345 U001346 U001347 "
            "U001348 U001349 U001350 U001351 U001352"
        ),
        "A000965 A000966 A000967 A000968",
        (
            "Resolved printed page 251 to U001343-U001352/"
            "A000965-A000968. It defines the one-cell perturbation observer "
            "and distinguishes extinction, localization, uniform spreading, "
            "and sporadic spreading across the four classes. Numerical edge "
            "speeds remain in the Notes source."
        ),
    ),
    route_spec(
        "within",
        "U006365",
        "",
        "PAGE",
        "page 976",
        "two-dimensional difference-region shape and Central Limit context",
        "U006530 U006531 U006532",
        "A000623",
        (
            "Audited printed page 976 at U006530-U006532/A000623. The "
            "available target discusses continuous-system attractor types, "
            "logistic-map period doubling, and finite-state evolution "
            "networks; it contains no two-dimensional difference-region or "
            "Central Limit derivation. The route is closed to that exact "
            "source boundary without inventing the expected support."
        ),
    ),
    route_spec(
        "within",
        "U006369",
        "",
        "PAGE",
        "page 255",
        "printed cyclic-addition construction",
        "U001367 U001368 U001369 U001370 U001371",
        "A000971",
        (
            "Resolved printed page 255 to U001367-U001371/A000971. The "
            "target specifies a dot on six cyclic positions, fixed rightward "
            "displacement, wrapping, and the resulting period bound. The "
            "closed-form GCD formula remains in U006369."
        ),
    ),
    route_spec(
        "within",
        "U006372",
        "",
        "PAGE",
        "page 257",
        "printed cyclic-multiplication construction",
        "U001377 U001378 U001379 U001380 U001381",
        "A000973 A000974",
        (
            "Resolved printed page 257 to U001377-U001381/"
            "A000973-A000974. It gives the doubling-modulo-n step, "
            "Mod[2^t,n] position, multiplicative-order period for odd n, "
            "and the period-versus-size observer."
        ),
    ),
    route_spec(
        "within",
        "U006373",
        "",
        "PAGE",
        "page 260",
        "printed maximum-period discussion",
        "U001388 U001389 U001392 U001393",
        "A000976",
        (
            "Resolved printed page 260 to U001388-U001389/"
            "U001392-U001393/A000976. The target plots periods by finite "
            "size and states the rule-90, rule-30, rule-45, and rule-110 "
            "scalings against the 2^n state-count bound."
        ),
    ),
    route_spec(
        "within",
        "U006377",
        "",
        "PAGE",
        "page 963",
        "finite cellular-automaton state-count context",
        "U006347 U006348 U006349",
        "A000590",
        (
            "Audited printed page 963 at U006347-U006349/A000590. The "
            "available target gives the four-class discussion and empirical "
            "class-frequency survey by color count and range, but no finite-"
            "size k^n state-count formula. The closure records that exact "
            "limit rather than treating the frequency chart as a state "
            "enumeration."
        ),
    ),
    route_spec(
        "within",
        "U006385",
        "",
        "PAGE",
        "page 260",
        "rule-90 repetition-period figure assumptions",
        "U001392 U001393",
        "A000976",
        (
            "Resolved printed page 260 to U001392-U001393/A000976. The "
            "figure states the rule-90 maximum-period expression and the "
            "other rule scalings; U006385 supplies the explicit assumption "
            "and first finite-size exception behind that plotted curve."
        ),
    ),
    route_spec(
        "within",
        "U006386",
        "",
        "PAGE",
        "page 962",
        "finite-size period exceptions",
        "U006341 U006342 U006343 U006344 U006345 U006346",
        "A000589",
        (
            "Audited printed page 962 at U006341-U006346/A000589. The "
            "available target covers random-start densities, triangle "
            "statistics, algebraic rule forms, and continual randomness "
            "injection; it contains no finite-size period-exception table. "
            "The route is closed to that verified source boundary without "
            "promoting unrelated pattern panels."
        ),
    ),
    route_spec(
        "within",
        "U006390",
        "",
        "PAGE",
        "page 263",
        "printed rule-22 and rule-225 discussion",
        "U001405 U001406 U001407 U001408 U001409 U001410",
        "A000979 A000980",
        (
            "Resolved printed page 263 to U001405-U001410/A000979-A000980, "
            "the rule-22 random-start, single-cell nested, and alternate "
            "simple-seed comparison. Rule 225 is supplied only by the Notes "
            "source and is not attributed to these panels."
        ),
    ),
    route_spec(
        "within",
        "U006400",
        "",
        "PAGE",
        "page 264",
        "printed generalized-additivity construction",
        "U001411 U001412 U001413 U001414 U001415",
        "A000981",
        (
            "Resolved printed page 264 to U001411-U001415/A000981. The "
            "target demonstrates ordinary rule-90 superposition from "
            "single-cell histories. The generalized monoid operation and "
            "homomorphism law are the Notes-side generalization, not facts "
            "read from the printed panel."
        ),
    ),
    route_spec(
        "within",
        "U006432",
        "",
        "PAGE",
        "page 267",
        "printed repeating-block construction",
        "U001432 U001433 U001434 U001435 U001436 U001437 U001438 U001439",
        "A000987 A000988",
        (
            "Resolved printed page 267 to U001432-U001439/"
            "A000987-A000988. It proves that an infinitely repeated width-n "
            "block evolves like an n-cell cyclic system with period at most "
            "2^n and contrasts rule 30 with the two-block rule-126 special "
            "initial condition."
        ),
    ),
    route_spec(
        "within",
        "U006449",
        "",
        "PAGE",
        "page 269",
        "printed rule-emulation and renormalization discussion",
        "U001443 U001444 U001445 U001446 U001447 U001448 U001449",
        "A000990 A000991",
        (
            "Resolved printed page 269 to U001443-U001449/"
            "A000990-A000991. The target gives the explicit two-cell block "
            "encoding under which alternate rule-126 steps reproduce "
            "rule 90. It establishes exact block emulation, not a statistical "
            "renormalization-group flow."
        ),
    ),
    route_spec(
        "within",
        "U006451",
        "",
        "PAGE",
        "page 271",
        "printed additive-rule self-similarity discussion",
        (
            "U001451 U001452 U001453 U001454 U001455 U001456 U001457 "
            "U001458 U001459 U001460 U001461 U001462 U001463 U001464"
        ),
        "A000992 A000993 A000994 A000996 A000997 A000998",
        (
            "Resolved printed page 271 to U001451-U001464 and "
            "A000992-A000994/A000996-A000998. These units explain "
            "rule-90 block self-emulation, exhibit the rule-150 analog, and "
            "join both to additivity and nested form. The Notes algebraic "
            "prime-modulus generalization remains separate support."
        ),
    ),
    route_spec(
        "within",
        "U006471",
        "",
        "PAGE",
        "page 272",
        "printed nested-initial-condition examples",
        "U001470 U001471 U001472 U001473 U001474",
        "A001001 A001002",
        (
            "Resolved printed page 272 to U001470-U001474/"
            "A001001-A001002. It gives the two-symbol substitution seed for "
            "rule 184 and the resulting equal black/white stripe "
            "annihilation pattern. Other nested sequences pictured in the "
            "Notes are not relabelled as this preset."
        ),
    ),
    route_spec(
        "within",
        "U006474",
        "",
        "PAGE",
        "page 275",
        "printed discrete-attractor discussion",
        (
            "U001481 U001482 U001483 U001484 U001485 "
            "U001486 U001487 U001488 U001489 U001490 U001491"
        ),
        "A001005 A001006",
        (
            "Resolved printed page 275 to U001481-U001491/"
            "A001005-A001006. The target defines explicitly reached "
            "discrete attractors for rules 255 and 4, distinguishes a single "
            "all-black state from a constrained attractor set, and shows "
            "multiple basin members."
        ),
    ),
    route_spec(
        "within",
        "U006492",
        "",
        "PAGE",
        "page 279",
        "regular expressions for rule-110 sequence sets",
        "U001504 U001505 U001506",
        "A001009",
        (
            "Resolved printed page 279 to U001504-U001506/A001009. The "
            "target shows the rapidly growing finite networks of allowed "
            "sequences for class-3 and class-4 rules, including rule 110. "
            "The explicit regular expression is supplied by U006492, not "
            "transcribed from the figure."
        ),
    ),
    route_spec(
        "within",
        "U006493",
        "",
        "PAGE",
        "page 278",
        "printed finite-network growth properties",
        "U001499 U001500 U001501 U001502 U001503",
        "A001008",
        (
            "Resolved printed page 278 to U001499-U001503/A001008. These "
            "units show progressive restriction of allowed sequences for "
            "class-1 and class-2 rules and bound the displayed networks by "
            "about t^2 nodes. Exact per-rule node/edge formulas remain in "
            "the Notes."
        ),
    ),
    route_spec(
        "within",
        "U006531",
        "",
        "PAGE",
        "page 255",
        "cyclic-addition state graphs",
        "U001367 U001368 U001369 U001370 U001371",
        "A000971",
        (
            "Resolved printed page 255 to U001367-U001371/A000971, the "
            "native six-position cyclic-addition system whose complete-state "
            "graph is drawn in the Notes. The target supplies the transition "
            "law and repetition argument, not a second graph construction."
        ),
    ),
    route_spec(
        "within",
        "U006533",
        "",
        "PAGE",
        "page 257",
        "cyclic-multiplication state graphs",
        "U001377 U001378 U001379 U001380 U001381",
        "A000973 A000974",
        (
            "Resolved printed page 257 to U001377-U001381/"
            "A000973-A000974. These units give the doubling-modulo-n "
            "transition whose complete-state cycles and transient trees are "
            "drawn by U006533."
        ),
    ),
    route_spec(
        "within",
        "U006550",
        "",
        "PAGE",
        "page 975",
        "shift-rule cycle factors",
        (
            "U006521 U006522 U006523 U006524 U006525 "
            "U006526 U006527 U006528 U006529"
        ),
        "A000622",
        (
            "Audited printed page 975 at U006521-U006529/A000622. The "
            "available target treats temporal and spacetime entropies, their "
            "light-cone bound, and symbolic-dynamics history; it does not "
            "state the shift-rule cycle factorization cited by U006550. The "
            "closure records the verified page boundary without inventing a "
            "factor formula."
        ),
    ),
    route_spec(
        "within",
        "U006558",
        "",
        "PAGE",
        "page 283",
        "printed code-20 survival data",
        (
            "U001519 U001520 U001521 U001523 U001524 "
            "U001525 U001526 U001531 U001532 U001533"
        ),
        "A001012 A001015",
        (
            "Resolved printed page 283 to U001519-U001533 restricted to the "
            "code-20 discussion and A001012/A001015. It identifies the "
            "persistent seeds 151, 187, 189, 195, and 219 and the exhaustive "
            "under-nine-cell survey; the Notes source supplies aggregate "
            "million/billion-seed counts."
        ),
    ),
    route_spec(
        "within",
        "U006560",
        "",
        "PAGE",
        "page 290",
        "rule-110 periodic background",
        "U001557 U001558 U001560 U001561",
        "A001022",
        (
            "Resolved printed page 290 to U001557-U001558/"
            "U001560-U001561/A001022. It identifies rule 110 and the "
            "14-cell background block repeating every seven steps; the "
            "phase formula b[[Mod[x+4t,14]+1]] remains in the Notes."
        ),
    ),
    route_spec(
        "within",
        "U006562",
        "",
        "PAGE",
        "page 292",
        "printed rule-110 persistent structures",
        "U001562 U001567 U001568",
        "A001023",
        (
            "Resolved printed page 292 to U001562/U001567-U001568/A001023, "
            "the labelled rule-110 persistent-structure survey. The Notes "
            "source supplies the exact seed integers, periods, and "
            "displacements for those labels."
        ),
    ),
    route_spec(
        "within",
        "U006569",
        "",
        "PAGE",
        "page 290",
        "parallel copies of rule-110 persistent structures",
        "U001557 U001558 U001560 U001561",
        "A001022",
        (
            "Resolved printed page 290 to U001557-U001558/"
            "U001560-U001561/A001022. The random-start witness shows "
            "multiple disruptions travelling on the periodic rule-110 "
            "background. It does not define a distinct coupled-copy rule."
        ),
    ),
    route_spec(
        "within",
        "U006570",
        "",
        "PAGE",
        "page 293",
        "printed rule-110 glider-gun seed",
        "U001563 U001569 U001570",
        "A001024",
        (
            "Resolved printed page 293 to U001563/U001569-U001570/A001024. "
            "The target gives the width-41 block on the rule-110 background "
            "and its periodic unbounded-growth outputs; U006570 supplies the "
            "exact {n,w} integer encoding."
        ),
    ),
    route_spec(
        "within",
        "U006570",
        "",
        "PAGE",
        "page 294",
        "printed rule-110 collision invariant",
        "U001564 U001565 U001571 U001572",
        "A001025",
        (
            "Resolved printed page 294 to U001564-U001565/"
            "U001571-U001572/A001025, the separation sweep for structures "
            "(o) and (j). The modulo-14 conserved-width statement is "
            "supplied by U006570; the printed page gives collision outcomes, "
            "not its proof."
        ),
    ),
    route_spec(
        "within",
        "U006586",
        "",
        "PAGE",
        "page 263",
        "rule-22 history from an infinite-line Life seed",
        "U001405 U001406 U001407 U001408 U001409 U001410",
        "A000979 A000980",
        (
            "Resolved printed page 263 to U001405-U001410/A000979-A000980, "
            "the rule-22 histories from finite random and simple 1D seeds. "
            "The reduction from an infinite Life row is stated by U006586 "
            "and is not attributed to the printed 1D panels."
        ),
    ),
    route_spec(
        "within",
        "U006587",
        "",
        "PAGE",
        "page 287",
        "code-1329 spacefiller analog",
        "U001547 U001548 U001549 U001550 U001551",
        "A001019",
        (
            "Resolved printed page 287 to U001547-U001551/A001019. The "
            "target identifies stationary and moving code-1329 structures "
            "and U001551 introduces the period-256 moving part that leaves "
            "an unbounded trail; the full growth panel is on the following "
            "page. The Life spacefiller remains an analogy, not the same "
            "state or rule."
        ),
    ),
)


UNTOUCHED_CROSS_RANGE_IDENTITIES: tuple[
    tuple[str, str, str, str, str], ...
] = tuple(
    tuple(line.split("\\t"))  # type: ignore[misc]
    for line in """U001233\\t\\tPAGE\\tpage 24\\tearlier presentation of rule 254
U001233\\t\\tPAGE\\tpage 53\\telementary cellular-automaton rule-number scheme
U001254\\t\\tPAGE\\tpage 32\\tearlier rule-110 discussion
U001311\\t\\tPAGE\\tpage 155\\tcontinuous cellular-automaton construction
U001316\\t\\tPAGE\\tpage 155\\tcontinuous cellular-automaton construction
U001358\\t\\tOTHER\\tlater in this book\\tinformation handling in systems in nature
U001366\\t\\tSECTION\\tthe next chapter\\tlimited-size repetition in nature
U001399\\t\\tPAGE\\tpage 27\\trule-30 simple-initial-condition construction
U001423\\t\\tSECTION\\tthe next few chapters\\tnatural-system stability from intrinsic randomness
U001431\\t\\tPAGE\\tpage 210\\tconstraint satisfaction for periodic behavior
U001470\\t\\tPAGE\\tpage 82\\tsubstitution-system construction
U001474\\t\\tPAGE\\tpage 83\\tsubstitution-system construction
U001478\\t\\tPAGE\\tpage 338\\tequal-density rule-184 nested patterns
U001559\\t\\tSECTION\\tChapter 11\\tcomputation and universality
U001560\\t\\tPAGE\\tpage 32\\tearlier rule-110 discussion
U006341\\t\\tPAGE\\tpage 953\\tmethod for estimating long-run cellular-automaton densities
U006343\\t\\tPAGE\\tpage 871\\trule-30 triangle-density analysis
U006344\\t\\tPAGE\\tpage 869\\talgebraic representation convention for elementary cellular automata
U006346\\t\\tPAGE\\tpage 1012\\treaction-diffusion pattern-formation construction lead
U006346\\t\\tPAGE\\tpage 880\\tself-gravitating-system construction lead
U006348\\t\\tPAGE\\tpage 597\\tdeviations among random initial conditions
U006348\\t\\tPAGE\\tpages 944 and 1193\\tstates-of-matter classification context
U006348\\t\\tPAGE\\tpage 70\\ttotalistic class-4 rule 1599 example
U006348\\t\\tPAGE\\tpage 67\\ttotalistic class-4 rule 1635 example
U006348\\t\\tPAGE\\tpage 68\\ttotalistic class-4 rule 2049 example
U006350\\t\\tPAGE\\tpage 1138\\tundecidability of cellular-automaton class tests
U006350\\t\\tPAGE\\tpage 922\\tcontinuous cellular-automaton mechanics
U006351\\t\\tPAGE\\tpage 877\\tGame of Life historical context
U006356\\t\\tPAGE\\tpage 183\\tcubic lattice convention
U006360\\t\\tPAGE\\tpage 154\\trandom digit sequences for continuous numbers
U006360\\t\\tPAGE\\tpage 1070\\trandomness for finite integer representations
U006360\\t\\tPAGE\\tpages 963 and 1038\\trandom networks as initial conditions for network systems
U006360\\t\\tPAGE\\tpage 920\\trandom initial conditions across other system classes
U006363\\t\\tPAGE\\tpage 601\\tone-sided perturbation propagation in rule 30
U006363\\t\\tPAGE\\tpage 871\\trule-30 nonrepetitive-region growth rate
U006367\\t\\tPAGE\\tpage 155\\texponential sensitivity analogy
U006367\\t\\tPAGE\\tpage 921\\tLyapunov exponents for number-based dynamical systems
U006369\\t\\tPAGE\\tpage 613\\tfull-period cyclic-addition parameter pairs
U006372\\t\\tPAGE\\tpage 1093\\tmultiplicative-order mechanics
U006372\\t\\tPAGE\\tpage 912\\tdigit-sequence repetition-period relation
U006386\\t\\tPAGE\\tpage 1087\\tlongest-period comparison across elementary rules and symmetries
U006388\\t\\tPAGE\\tpage 865\\tbitwise cellular-automaton representation
U006390\\t\\tPAGE\\tpage 58\\tsingle-cell rule-225 nested pattern
U006390\\t\\tPAGE\\tpage 949\\trule-22 difference-region spread rate
U006395\\t\\tPAGE\\tpage 955\\tnested patterns from modular-additive rules
U006395\\t\\tPAGE\\tpage 870\\talgebraic additive-rule analysis
U006399\\t\\tPAGE\\tpage 1087\\tpartial additivity
U006411\\t\\tPAGE\\tpage 886\\tassociative rule analogs
U006411\\t\\tPAGE\\tpage 956\\tgeneral associative-rule nesting results
U006413\\t\\tPAGE\\tpage 922\\tcontinuous additive cellular automata
U006413\\t\\tPAGE\\tpage 161\\tcontinuous-function local evolution
U006423\\t\\tPAGE\\tpage 949\\tdifference-pattern growth estimates
U006424\\t\\tPAGE\\tpage 870\\trule-90 superposition cell-count derivation
U006424\\t\\tPAGE\\tpage 602\\trule-90 density relation
U006427\\t\\tPAGE\\tpage 339\\tcontrasting cellular-automaton density response
U006429\\t\\tPAGE\\tpage 699\\trule-73 independent-region mechanics
U006432\\t\\tPAGE\\tpage 211\\tconstraint construction for repeating configurations
U006438\\t\\tPAGE\\tpage 960\\tspacetime-entropy growth of period-dividing counts
U006439\\t\\tPAGE\\tpage 958\\tfinite-complement language mechanics
U006440\\t\\tPAGE\\tpage 700\\tadditional repeating-configuration examples
U006441\\t\\tPAGE\\tpages 281 and 1118\\tlocalized-structure construction
U006441\\t\\tPAGE\\tpage 942\\ttwo-dimensional constraint mechanics
U006441\\t\\tPAGE\\tpage 1139\\tcomplexity of two-dimensional repeating configurations
U006441\\t\\tPAGE\\tpage 349\\tstripe reduction of two-dimensional configurations
U006442\\t\\tPAGE\\tpage 150\\titerated-map definition
U006442\\t\\tPAGE\\tpage 914\\tcontinued-fraction map mechanics
U006445\\t\\tPAGE\\tpage 961\\texplicit solutions of polynomial-map periodic points
U006448\\t\\tPAGE\\tpage 869\\tCantor-set view of cellular automata
U006449\\t\\tPAGE\\tpages 702 and 1118\\trule emulations
U006449\\t\\tPAGE\\tpage 981\\tcritical-point nesting
U006449\\t\\tPAGE\\tpage 983\\trenormalization-group universality
U006450\\t\\tPAGE\\tpage 989\\tlimits of renormalization for cellular automata
U006451\\t\\tPAGE\\tpage 952\\tprime-modulus additive rules
U006451\\t\\tPAGE\\tpage 870\\tadditive self-similarity
U006457\\t\\tPAGE\\tpage 58\\tfractal dimensions of rule-90 and rule-150 histories
U006457\\t\\tPAGE\\tpage 952\\tother additive-rule families used by the fractal-dimension analysis
U006459\\t\\tPAGE\\tpage 870\\tother additive-rule dimensions
U006461\\t\\tPAGE\\tpage 886\\tassociative cellular-automaton rules
U006468\\t\\tPAGE\\tpage 887\\tnoncommutative associative example
U006468\\t\\tPAGE\\tpage 952\\tgeneralized-additive implication for nested behavior
U006469\\t\\tPAGE\\tpage 701\\trule-45 nested background seed
U006469\\t\\tPAGE\\tpage 1186\\tpattern-equivalence counts
U006471\\t\\tPAGE\\tpage 83\\tnested sequence generators
U006471\\t\\tPAGE\\tpage 1091\\tnested initial-condition details
U006492\\t\\tPAGE\\tpage 939\\tregular-language mechanics
U006493\\t\\tPAGE\\tpage 891\\tregular-language and substitution-system connections
U006504\\t\\tPAGE\\tpage 1084\\ttopological entropy
U006504\\t\\tPAGE\\tpage 1138\\tundecidability of limiting entropy bounds
U006518\\t\\tPAGE\\tpage 83\\tsubstitution-system construction of nested Cantor sets
U006518\\t\\tPAGE\\tpage 869\\tcellular automata as global state-space maps
U006518\\t\\tPAGE\\tpages 601 and 1087\\tadditivity criteria for surjectivity
U006518\\t\\tPAGE\\tpage 957\\tminimal-automaton surjectivity test
U006518\\t\\tPAGE\\tpage 1085\\tsurjective cellular-automaton rules used as DES S-box input
U006519\\t\\tPAGE\\tpage 1017\\treversible cellular automata
U006520\\t\\tPAGE\\tpage 1138\\ttwo-dimensional undecidability of injectivity and surjectivity
U006527\\t\\tPAGE\\tpage 878\\tsliding-block codes as cellular automata
U006527\\t\\tPAGE\\tpage 869\\tlocality and continuity analogy
U006528\\t\\tPAGE\\tpage 876\\tself-reproduction and Garden-of-Eden context for cellular-automaton surjectivity
U006530\\t\\tPAGE\\tpage 922\\tordinary differential-equation attractors
U006531\\t\\tPAGE\\tpages 920 and 955\\tlogistic-map attractor progression
U006531\\t\\tPAGE\\tpage 938\\tTuring-machine accept-state grammars
U006542\\t\\tPAGE\\tpage 1087\\tlarge finite cellular-automaton state graphs
U006546\\t\\tPAGE\\tpage 950\\tspatial-period state counts
U006548\\t\\tPAGE\\tpage 950\\tprimitive spatial-period count used for exact shift cycles
U006552\\t\\tPAGE\\tpage 951\\tcycle lengths of finite additive cellular automata
U006570\\t\\tPAGE\\tpage 949\\tGame of Life native rule
U006591\\t\\tPAGE\\tpage 888\\tpersistent structures in Turing machines""".splitlines()
)


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
    if any(
        len(identity) != len(IDENTITY_FIELDS)
        for identity in UNTOUCHED_CROSS_RANGE_IDENTITIES
    ):
        raise AuthoringError("untouched CROSS_RANGE identity is malformed")
    cross_digest = hashlib.sha256(
        canonical_json_bytes(
            [
                dict(zip(IDENTITY_FIELDS, identity, strict=True))
                for identity in UNTOUCHED_CROSS_RANGE_IDENTITIES
            ]
        )
    ).hexdigest()
    if cross_digest != EXPECTED_CROSS_RANGE_SHA256:
        raise AuthoringError(
            "untouched CROSS_RANGE projection digest drifted: "
            f"{cross_digest} != {EXPECTED_CROSS_RANGE_SHA256}"
        )
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


def points_into_stage10(literal_target: str) -> bool:
    """Recognize the closed printed-page/section assignment for Chapter 6."""

    if literal_target.strip().casefold() == "chapter 6":
        return True
    return any(
        int(match.group(1)) in CHAPTER6_PRINTED_PAGE_RANGE
        for match in PRINTED_PAGE.finditer(literal_target)
    )


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

    expected_incoming = {
        spec.identity for spec in ROUTE_SPECS if spec.origin == "incoming"
    }
    observed_incoming_rows = [
        row
        for row in routes
        if row["owning_stage"] != "10"
        and row["closure_scope"] == "CROSS_RANGE"
        and row["status"] == "PENDING"
        and points_into_stage10(row["literal_target"])
    ]
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
            "incoming Stage 10 route set differs from the governed map: "
            f"missing={missing!r} extra={extra!r}"
        )
    for row in observed_incoming_rows:
        require_pending_route(row, label="incoming Stage 10")

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
            f"incoming=14 within=58 untouched-cross=107 "
            f"spec-sha256={digest} "
            f"cross-sha256={EXPECTED_CROSS_RANGE_SHA256}"
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
