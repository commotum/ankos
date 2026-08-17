#!/usr/bin/env python3
"""Author the governed Stage 9 Chapter 5 route-resolution proposal.

Routes are selected only by their immutable five-field identity:

    (source_unit_id, source_asset_id, route_kind,
     literal_target, expected_topic)

The proposal closes the exhaustive incoming route set whose literal target is
in the reviewed Chapter 5 assignment and every Stage-9 WITHIN_STAGE route.
The Stage-9 CROSS_RANGE partition is proved present and left untouched.
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
    "CHAPTERS/05-Two-Dimensions-and-Beyond/05-Two-Dimensions-and-Beyond.md",
    "BACK-MATTER/NOTES/05-Two-Dimensions-and-Beyond-Notes.md",
)
EXPECTED_SPEC_COUNTS = {"incoming": 16, "within": 20}
EXPECTED_UPDATE_COUNT = 36
EXPECTED_UNTOUCHED_CROSS_RANGE_COUNT = 26
EXPECTED_SPEC_SHA256 = (
    "3b413287da41a0d0b22502a9aad25427872ddad22b9286bfac3987eb33c8c5f3"
)
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


ROUTE_SPECS = (
    route_spec(
        "incoming",
        "U005008",
        "",
        "PAGE",
        "higher-dimensional cellular automata on page 927",
        "higher-dimensional cellular-automaton native mechanics",
        (
            "U006088 U006089 U006090 U006091 U006092 U006093 "
            "U006096 U006097 U006098 U006099 U006100 U006101"
        ),
        "",
        (
            "Resolved printed Notes page 927 to U006088-U006093 and "
            "U006096-U006101. These units give executable axial-neighbor, "
            "full 3^d-neighbor, and arbitrary-offset cellular-automaton "
            "steps and exact rule-number decoding in any dimension. The "
            "separate 3D rendering helper and rule-count table are excluded "
            "from native mechanics."
        ),
    ),
    route_spec(
        "incoming",
        "U005119",
        "",
        "PAGE",
        "fractal dimension ... (see page 933)",
        "fractal-dimension definition applied to Rule 90",
        "U006193 U006194 U006195 U006196",
        "A000551",
        (
            "Resolved printed Notes page 933 to U006193-U006196/A000551, "
            "which define dimension by the small-scale grid-square count "
            "(1/a)^d and state its limitations. Rule 90 is the origin-side "
            "application; the target does not relabel the illustrated "
            "generic nested patterns as Rule 90."
        ),
    ),
    route_spec(
        "incoming",
        "U005119",
        "",
        "PAGE",
        "a Sierpinski pattern (see page 934)",
        "Sierpinski-pattern construction and Rule 90 correspondence",
        (
            "U001034 U001035 U001036 U001037 "
            "U006145 U006146 U006149 U006150 U006151 U006152 U006153 "
            "U006154 U006155 U006156 U006157 U006158 U006159 U006197"
        ),
        "A000874 A000875",
        (
            "Resolved the literal page-934 Sierpinski identification at "
            "U006197 together with the reviewed page-187 block-substitution "
            "rule U001034-U001037/A000874-A000875 and its exact executable "
            "form and equivalent constructions at U006145-U006159. The "
            "Rule-90 correspondence is attribution supplied by the origin; "
            "page 934 itself supplies the historical Sierpinski identity, "
            "not a Rule-90 label."
        ),
    ),
    route_spec(
        "incoming",
        "U005166",
        "",
        "PAGE",
        "See also page 929.",
        "rule-based design and weaving construction boundary",
        "U006121",
        "",
        (
            "Resolved printed Notes page 929 to the cellular-automaton-art "
            "passage in U006121. It bounds the design construction to 2D "
            "cellular automata, periodic boundary conditions for repeating "
            "squares, optional extra colors, and a multi-tuft display "
            "choice; it does not turn weaving or display advice into a new "
            "native rule family."
        ),
    ),
    route_spec(
        "incoming",
        "U005168",
        "",
        "PAGE",
        "(Compare page 929.)",
        "rule-selection and evaluation methods for generated designs",
        "U006121",
        "",
        (
            "Resolved printed Notes page 929 to U006121. The target records "
            "practical design controls—periodic boundaries, color count, "
            "and visual cell-to-tuft scale—but gives no independent rule "
            "search or quality-scoring algorithm. The closure preserves "
            "that source-limited boundary."
        ),
    ),
    route_spec(
        "incoming",
        "U005232",
        "",
        "PAGE",
        "generalized 2D cellular automata ... (see page 928)",
        "Ulam generalized two-dimensional growth automata",
        "U006114 U006115 U006116",
        "A000526",
        (
            "Resolved printed Notes page 928 to U006114-U006116/A000526, "
            "which give the Ulam history-dependent growth construction, "
            "orthogonal offsets, retained-history state, component filters, "
            "and 120-step witness. Later ablations and the pure code-12 "
            "cellular automaton remain separate constructions."
        ),
    ),
    route_spec(
        "incoming",
        "U005274",
        "",
        "PAGE",
        "page 936",
        "random Boolean-network construction",
        "U006238",
        "",
        (
            "Resolved printed Notes page 936 to U006238. It defines random "
            "Boolean networks as network cellular automata whose node rules "
            "are independently chosen from the 2^(2^s) Boolean functions "
            "with s inputs, and states the resulting finite-state evolution "
            "semantics. Ensemble observations are not promoted into the "
            "native update rule."
        ),
    ),
    route_spec(
        "incoming",
        "U005276",
        "",
        "PAGE",
        "page 930",
        "Paterson two-dimensional Turing-machine worms",
        "U006134 U006135 U006136",
        "",
        (
            "Resolved printed Notes page 930 to the executable generic 2D "
            "Turing-machine step U006134-U006135 and the Paterson-Conway "
            "worm description U006136. The target establishes a 2D Turing "
            "machine whose head state records motion direction and reports "
            "the hexagonal-grid survey, but does not provide any particular "
            "worm transition table."
        ),
    ),
    route_spec(
        "incoming",
        "U005278",
        "",
        "PAGE",
        "page 934",
        "fractal generation constructions",
        "U006193 U006197 U006198 U006199 U006200 U006201",
        "A000553 A000554",
        (
            "Resolved printed Notes page 934 to U006197-U006201/"
            "A000553-A000554, with U006193 supplying the inverse-square-root "
            "Julia generator used there. This bounded target covers the "
            "historical fractal context and the explicit Julia/Mandelbrot "
            "generation relations, not every geometrical substitution "
            "system in the chapter."
        ),
    ),
    route_spec(
        "incoming",
        "U005281",
        "",
        "PAGE",
        "page 934",
        "Mandelbrot-set iteration",
        "U006193 U006198 U006199 U006200 U006201",
        "A000553 A000554",
        (
            "Resolved printed Notes page 934 to U006193 and "
            "U006198-U006201/A000553-A000554. These units give the "
            "inverse-square-root Julia iteration from z=0 and the equivalent "
            "Mandelbrot bounded-orbit test z -> z^2+c, together with direct "
            "Julia-set and magnification witnesses."
        ),
    ),
    route_spec(
        "incoming",
        "U005363",
        "",
        "PAGE",
        "page 927",
        "higher-dimensional cellular automata",
        (
            "U006088 U006089 U006090 U006091 U006092 U006093 "
            "U006096 U006097 U006098 U006099 U006100 U006101"
        ),
        "",
        (
            "Resolved printed Notes page 927 to U006088-U006093 and "
            "U006096-U006101, the reviewed d-dimensional axial/full "
            "neighborhood and arbitrary-offset cellular-automaton "
            "implementations. Rule counts, symmetry classes, and rendering "
            "are deliberately outside this native-mechanics closure."
        ),
    ),
    route_spec(
        "incoming",
        "U005385",
        "",
        "PAGE",
        "page 945",
        "finite group construction",
        "U006336",
        "",
        (
            "Resolved printed Notes page 945 to U006336, which characterizes "
            "a finite group or semigroup through a multiplication table "
            "satisfying the referenced algebraic constraints and records "
            "the classification boundary. The adjacent group-count plot is "
            "an observer and is not treated as construction mechanics."
        ),
    ),
    route_spec(
        "incoming",
        "U005511",
        "",
        "PAGE",
        "page 190",
        "two-dimensional geometrical substitution systems",
        "U001046 U001047 U001048 U001049 U006185",
        "A000879 A000880",
        (
            "Resolved printed page 190 to U001046-U001049/"
            "A000879-A000880 and the exact page-190 complex replacement map "
            "in U006185. The target is the overlap-producing geometrical "
            "substitution preset; overlap is an outcome, while repeated "
            "application of the two-image affine map is the native law."
        ),
    ),
    route_spec(
        "incoming",
        "U005515",
        "",
        "PAGE",
        "page 189",
        "paperfolding/geometrical substitution construction",
        "U001042 U001043 U001044 U001045 U006184 U006185",
        "A000877 A000878",
        (
            "Resolved printed page 189 to U001042-U001045/"
            "A000877-A000878 and U006184-U006185. The target gives the "
            "orientation-sensitive two-square geometrical replacement map "
            "and explicitly relates its dragon-curve result to doubled 1D "
            "paperfolding paths. That relationship does not collapse the "
            "two native constructions into one state space."
        ),
    ),
    route_spec(
        "incoming",
        "U005534",
        "",
        "PAGE",
        "page 189",
        "two-dimensional geometrical substitution systems",
        "U001042 U001043 U001044 U001045 U006185",
        "A000877 A000878",
        (
            "Resolved printed page 189 to U001042-U001045/"
            "A000877-A000878 and the exact iterated complex map U006185. "
            "These targets specify orientation-sensitive replacement of "
            "each square by two smaller squares from a one-square seed and "
            "its nested result."
        ),
    ),
    route_spec(
        "incoming",
        "U005548",
        "",
        "PAGE",
        "page 938",
        "multiway string-rewriting systems",
        (
            "U006240 U006241 U006242 U006243 U006244 U006245 "
            "U006246 U006247 U006248 U006249 U006250 U006261"
        ),
        "",
        (
            "Resolved printed page 938's string/term-rewrite identity at "
            "U006261 together with the reviewed native multiway mechanics "
            "U006240-U006250: all positional matches of every replacement "
            "are generated, results are unioned, and unmatched strings are "
            "dropped in the shown implementation. Historical aliases do "
            "not create additional construction identities."
        ),
    ),
    route_spec(
        "within",
        "U000965",
        "",
        "PAGE",
        "page 173",
        "two-dimensional CA rule-code numbering",
        "U000973 U000974",
        "A000849",
        (
            "Resolved printed page 173 to U000973-U000974/A000849. The "
            "caption orders the ten outer-totalistic cases from all-white "
            "center/neighbors through progressively more black neighbors "
            "and reads the outputs as base-2 digits of the rule code."
        ),
    ),
    route_spec(
        "within",
        "U000968",
        "",
        "PAGE",
        "page 173",
        "two-dimensional CA rule-code numbering",
        "U000973 U000974",
        "A000849",
        (
            "Resolved printed page 173 to the same explicit code convention "
            "at U000973-U000974/A000849. This establishes why the earlier "
            "exactly-one-or-four rule is code 942 without importing the "
            "different general-neighborhood convention from the Notes."
        ),
    ),
    route_spec(
        "within",
        "U000981",
        "",
        "PAGE",
        "page 178",
        "approximate-circle two-dimensional cellular automaton",
        "U000990 U000991",
        "A000854",
        (
            "Resolved printed page 178 to U000990-U000991/A000854. The "
            "caption supplies code 746, its exact eight-neighbor retaining/"
            "whitening cases, the seven-cell-row seed, 400-step result, and "
            "approximately 0.37t radius."
        ),
    ),
    route_spec(
        "within",
        "U000982",
        "",
        "PAGE",
        "pages 179–181",
        "eight-neighbor exactly-three retaining cellular automaton",
        (
            "U000982 U000983 U000984 U000992 U000993 U000996 U000997 "
            "U000998 U000999 U001000 U001001 U001002"
        ),
        "A000855 A000856 A000857 A000858 A000859 A000860",
        (
            "Resolved printed pages 179-181 to U000982-U000984, "
            "U000992-U000993, and U000996-U001002/A000855-A000860. The "
            "bounded set gives the exactly-three-of-eight retaining rule "
            "(code 174826), the seed-length sweep, and the row-of-eleven "
            "long evolution. Stacked and stage views remain witnesses, not "
            "extra state dimensions."
        ),
    ),
    route_spec(
        "within",
        "U000983",
        "",
        "PAGE",
        "top of page 179",
        "seed-length sweep for exactly-three retaining CA",
        "U000982 U000983 U000992 U000993",
        "A000855",
        (
            "Resolved the top of printed page 179 to U000982-U000983 and "
            "U000992-U000993/A000855. These units give the code-174826 "
            "exactly-three-of-eight retaining rule, the minimum three-black "
            "growth condition, and the 60-step sweep over row lengths."
        ),
    ),
    route_spec(
        "within",
        "U000984",
        "",
        "PAGE",
        "page 181",
        "row-of-eleven evolution for exactly-three retaining CA",
        (
            "U000982 U000984 U000998 U000999 U001000 U001001 U001002"
        ),
        "A000857 A000858 A000859 A000860",
        (
            "Resolved printed page 181 to U000982/U000984 and "
            "U000998-U001002/A000857-A000860. The target is the "
            "row-of-eleven evolution under the exactly-three-of-eight "
            "retaining rule for hundreds of steps; the four images are "
            "successive-stage witnesses."
        ),
    ),
    route_spec(
        "within",
        "U000995",
        "",
        "PAGE",
        "pages 182 and 183",
        "three-dimensional cellular-automaton examples",
        (
            "U000994 U000995 U001003 U001004 U001005 "
            "U001006 U001007 U001008"
        ),
        "A000861 A000862 A000863 A000864",
        (
            "Resolved printed pages 182-183 to U000994-U000995 and "
            "U001003-U001008/A000861-A000864. They give the six-face "
            "any-one and exactly-one rules and the 26-neighbor exactly-one "
            "and exactly-two rules, with their seeds. Projection and "
            "stacking choices are not promoted into native carriers."
        ),
    ),
    route_spec(
        "within",
        "U001005",
        "",
        "PAGE",
        "page 171",
        "two-dimensional nested cellular-automaton analog",
        "U000966 U000967 U000968 U000969 U000970 U000971",
        "A000847 A000848",
        (
            "Resolved the page-171 analog to code 942 at U000966-U000968/"
            "A000847, with U000969-U000971/A000848 establishing its nested "
            "successive-time stacking witness. The stacked 3D display is "
            "kept distinct from the native two-dimensional CA state."
        ),
    ),
    route_spec(
        "within",
        "U001016",
        "",
        "PAGE",
        "page 186",
        "complex four-state two-dimensional Turing-machine rule",
        (
            "U001016 U001023 U001024 U001025 U001026 "
            "U001027 U001028 U001029 U001030 U001031"
        ),
        "A000870 A000871 A000872 A000873",
        (
            "Resolved printed page 186 to the long head-path witnesses "
            "U001027-U001031/A000872-A000873, joined to the exact preceding "
            "rule-(e) panel and rule table U001016/U001023-U001026/"
            "A000870-A000871. This supplies the four-state rule and blank "
            "tape seed instead of inferring mechanics from the path alone."
        ),
    ),
    route_spec(
        "within",
        "U001147",
        "",
        "PAGE",
        "page 205",
        "rapid-growth multiway rule",
        "U001133 U001134",
        "A000897",
        (
            "Resolved printed page 205 to U001133-U001134/A000897, the "
            "third illustrated page-205 preset whose state count is "
            "Fibonacci[t+1]. Original-resolution comparison identifies this "
            "as the rule later called (k); the page-207 evolution is an "
            "observer and is not substituted for the rule glyphs."
        ),
    ),
    route_spec(
        "within",
        "U001150",
        "",
        "PAGE",
        "page 205",
        "multiway rules (d) and (f)",
        "U001136 U001137 U001139",
        "A000895 A000898",
        (
            "Resolved rules (d) and (f) by original-resolution glyph "
            "matching from the page-208 survey to the two page-205 presets "
            "at U001137/A000895 and U001136/A000898, with U001139 supplying "
            "their growth/period context. No match is inferred from visual "
            "behavior alone."
        ),
    ),
    route_spec(
        "within",
        "U001150",
        "",
        "PAGE",
        "previous page",
        "multiway rule (k)",
        "U001145 U001146 U001147",
        "A000903",
        (
            "Resolved the literal previous-page target to "
            "U001145-U001147/A000903, which identify the rapid-growth "
            "multiway evolution later labelled rule (k), its all-white-"
            "initial-state result family, Fibonacci[t+1] state count, and "
            "first-appearance formula. The page does not independently "
            "transcribe the graphical replacement law, so this closure does "
            "not silently widen to the earlier page-205 rule panel."
        ),
    ),
    route_spec(
        "within",
        "U001206",
        "",
        "PAGE",
        "pages 214 and 215",
        "ordering of local-template constraints",
        (
            "U001184 U001185 U001186 U001187 U001188 "
            "U006286 U006287 U006288"
        ),
        "A000572 A000913 A000914",
        (
            "Resolved printed pages 214-215 to U001184-U001188/"
            "A000913-A000914 and the exact numbering rule "
            "U006286-U006288/A000572. Constraint n selects the 1-bit "
            "positions in its 32-digit binary expansion against the shown "
            "ordered template list; the 171 panels are the sufficient "
            "repetitive-pattern witnesses labelled by minimal constraint."
        ),
    ),
    route_spec(
        "within",
        "U001212",
        "",
        "PAGE",
        "page 216",
        "required-template constraint family",
        "U001190 U001191 U001192 U001193",
        "A000915",
        (
            "Resolved printed page 216 to U001190-U001193/A000915. This "
            "family requires every local neighborhood to match an allowed "
            "template and additionally requires one designated template to "
            "occur somewhere; the panels are concrete repetitive results, "
            "not an evolution schedule."
        ),
    ),
    route_spec(
        "within",
        "U006112",
        "",
        "PAGE",
        "page 171",
        "cellular automaton code 942 underlying the displayed slices",
        "U000966 U000967 U000968",
        "A000847",
        (
            "Resolved printed page 171 to U000966-U000968/A000847. These "
            "units give the single-black seed and code-942 rule: become "
            "black for exactly one or all four orthogonal black neighbors, "
            "otherwise retain the center. The Notes slice image remains an "
            "observer of this native evolution."
        ),
    ),
    route_spec(
        "within",
        "U006121",
        "",
        "PAGE",
        "page 177",
        "main-text cellular automaton code 175850 construction",
        "U000986 U000987 U000988 U000989",
        "A000852 A000853",
        (
            "Resolved printed page 177 to U000986-U000989/"
            "A000852-A000853. The caption supplies the row-of-seven seed "
            "and code-175850 eight-neighbor rule: black for exactly three "
            "or five black neighbors and otherwise retain the center."
        ),
    ),
    route_spec(
        "within",
        "U006121",
        "",
        "PAGE",
        "page 178",
        "main-text cellular automaton code 746 construction",
        "U000990 U000991",
        "A000854",
        (
            "Resolved printed page 178 to U000990-U000991/A000854, which "
            "give code 746, its exact eight-neighbor black/retain/white "
            "cases, the row-of-seven seed, and the approximate-circle "
            "growth result."
        ),
    ),
    route_spec(
        "within",
        "U006121",
        "",
        "PAGE",
        "page 181",
        "main-text cellular automaton code 174826 construction",
        (
            "U000982 U000984 U000992 U000993 "
            "U000998 U000999 U001000 U001001 U001002"
        ),
        "A000855 A000857 A000858 A000859 A000860",
        (
            "Resolved printed page 181's long evolution at "
            "U000984/U000998-U001002/A000857-A000860 together with the "
            "explicit code-174826 exactly-three-of-eight retaining rule at "
            "U000982/U000992-U000993/A000855. This avoids treating the "
            "page-181 stage views as a complete rule specification."
        ),
    ),
    route_spec(
        "within",
        "U006123",
        "",
        "PAGE",
        "page 183",
        "underlying rules for 3D projection panels (a) and (b)",
        "U001006 U001007 U001008",
        "A000863 A000864",
        (
            "Resolved printed page 183 to U001006-U001008/"
            "A000863-A000864. Panels (a) and (b) use all 26 face-or-corner "
            "neighbors and become black for exactly one and exactly two "
            "black neighbors respectively, from the stated single-cell and "
            "three-cell-line seeds. The Notes projection is only a view."
        ),
    ),
    route_spec(
        "within",
        "U006139",
        "",
        "PAGE",
        "page 185",
        "rules for 2D Turing-machine head paths (a) through (e)",
        (
            "U001016 U001017 U001018 U001019 U001020 U001021 "
            "U001022 U001023 U001024 U001025 U001026"
        ),
        "A000866 A000867 A000868 A000869 A000870 A000871",
        (
            "Resolved printed page 185 to U001016-U001026/"
            "A000866-A000871. Original-resolution panels provide the five "
            "four-state rule tables (a)-(e), their all-white tape seed, "
            "head-state/direction actions, and displayed step counts. The "
            "500-step Notes paths remain derived observers."
        ),
    ),
)


UNTOUCHED_CROSS_RANGE_IDENTITIES = (
    (
        "U000974",
        "",
        "PAGE",
        "page 60",
        "earlier cellular-automaton code convention",
    ),
    (
        "U001033",
        "",
        "PAGE",
        "page 82",
        "one-dimensional substitution-system mechanics",
    ),
    (
        "U001038",
        "",
        "PAGE",
        "page 83",
        "one-dimensional substitution-system nested patterns",
    ),
    (
        "U001052",
        "",
        "PAGE",
        "page 85",
        "neighbor interaction in one-dimensional substitution systems",
    ),
    (
        "U001057",
        "",
        "SECTION",
        "Chapter 3",
        "parallel and sequential one-dimensional substitution schedules",
    ),
    (
        "U001062",
        "",
        "SECTION",
        "Chapter 9",
        "order-independent higher-dimensional sequential substitution",
    ),
    (
        "U001113",
        "",
        "SECTION",
        "Chapter 9",
        "network-system variants for space and spacetime",
    ),
    (
        "U001129",
        "",
        "PAGE",
        "page 88",
        "sequential substitution replacement rules",
    ),
    (
        "U001216",
        "",
        "OTHER",
        "rule 60 elementary one-dimensional cellular automaton",
        "constraint correspondence with elementary cellular automaton rule 60",
    ),
    (
        "U001217",
        "",
        "OTHER",
        "rule 30 cellular automaton",
        (
            "constraint correspondence with a shifted elementary cellular "
            "automaton rule-30 pattern"
        ),
    ),
    (
        "U006078",
        "",
        "PAGE",
        "page 929",
        "other lattice constructions",
    ),
    (
        "U006121",
        "",
        "PAGE",
        "page 1092",
        "additive cellular-automaton rules",
    ),
    (
        "U006121",
        "",
        "PAGE",
        "page 980",
        "cellular automaton code 175850",
    ),
    (
        "U006168",
        "",
        "PAGE",
        "page 583",
        "non-white-background substitution systems and their nested structure",
    ),
    (
        "U006192",
        "",
        "PAGE",
        "pages 407 and 1006",
        "parameter-space sets for geometric substitution systems",
    ),
    (
        "U006208",
        "",
        "PAGE",
        "page 1127",
        "sigma-function scan of an infinite grid quadrant",
    ),
    (
        "U006226",
        "",
        "SECTION",
        "Chapter 9",
        "undirected-network update rules",
    ),
    (
        "U006273",
        "",
        "PAGE",
        "page 508",
        "network substitution systems",
    ),
    (
        "U006273",
        "",
        "PAGE",
        "page 1141",
        "multiway tag systems",
    ),
    (
        "U006276",
        "",
        "PAGE",
        "page 504",
        "multiway systems in fundamental physics",
    ),
    (
        "U006310",
        "",
        "PAGE",
        "page 932",
        "exact Penrose tile subdivision",
    ),
    (
        "U006318",
        "",
        "PAGE",
        "page 981",
        "exact Ising-model energy law",
    ),
    (
        "U006318",
        "",
        "PAGE",
        "page 757",
        "correspondence systems",
    ),
    (
        "U006336",
        "",
        "PAGE",
        "page 1073",
        "Hadamard matrix property",
    ),
    (
        "U006336",
        "",
        "PAGE",
        "page 887",
        "finite group/semigroup multiplication-table constraints",
    ),
    (
        "U006338",
        "",
        "PAGE",
        "page 1129",
        "formula constraints and expression complexity",
    ),
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
    if review["review_stage"] != "9":
        raise AuthoringError(
            f"{label} unit was not closed by Stage 9: {unit_id}"
        )
    if (
        unit.get("path") not in STAGE_PATHS
        or review["path"] != unit.get("path")
    ):
        raise AuthoringError(
            f"{label} unit lies outside Stage 9: {unit_id}"
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
    if asset["review_stage"] != "9":
        raise AuthoringError(
            f"{label} asset was not closed by Stage 9: {asset_id}"
        )
    if asset["assignment_path"] not in STAGE_PATHS:
        raise AuthoringError(
            f"{label} asset lies outside Stage 9: {asset_id}"
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
    """Build the exact 36-row identity-keyed Stage 9 closure proposal."""

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
    if terminal.get("review_id") != "V000023":
        raise AuthoringError("expected terminal history event V000023")
    if terminal.get("mode") != "INITIAL" or terminal.get("stage") != 9:
        raise AuthoringError(
            "expected the terminal combined Stage 9 INITIAL event"
        )
    if tuple(terminal.get("source_paths", ())) != STAGE_PATHS:
        raise AuthoringError(
            "terminal review event is not the combined Stage 9 assignment"
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
        if row["owning_stage"] == "9"
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
            "Stage 9 WITHIN_STAGE route set differs from the governed map: "
            f"missing={missing!r} extra={extra!r}"
        )
    for row in observed_within_rows:
        require_pending_route(row, label="Stage 9 WITHIN_STAGE")

    expected_cross = set(UNTOUCHED_CROSS_RANGE_IDENTITIES)
    observed_cross_rows = [
        row
        for row in routes
        if row["owning_stage"] == "9"
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
            "Stage 9 CROSS_RANGE partition drifted: "
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
                before["owning_stage"] != "9"
                or before["closure_scope"] != "WITHIN_STAGE"
            ):
                raise AuthoringError(
                    "within-stage route metadata drifted: "
                    f"{spec.identity!r}"
                )
        else:
            if (
                before["owning_stage"] == "9"
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
        "coordinator_id": "ch05-dimensions-route-closure-e2",
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
                f"Chapter 5 route specification check failed: {exc}",
                file=sys.stderr,
            )
            return 1
        print(
            "Chapter 5 route specification valid: "
            f"incoming=16 within=20 untouched-cross=26 sha256={digest}"
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
        print(f"Chapter 5 route authoring failed: {exc}", file=sys.stderr)
        return 1
    print(
        "authored Chapter 5 route closure: "
        f"updates={len(proposal['route_updates'])} "
        f"sha256={hashlib.sha256(canonical_json_bytes(proposal)).hexdigest()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
