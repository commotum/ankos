#!/usr/bin/env python3
"""Author the governed Stage 8 Chapter 4 route-resolution proposal.

The governed routes are selected only by their immutable five-field identity:

    (source_unit_id, source_asset_id, route_kind,
     literal_target, expected_topic)

Allocated route IDs are deliberately treated as output trace data and are
never used to select a route.  The proposal resolves exactly the 23 incoming
routes proved to target Stage 8 and the 15 final Stage-8 WITHIN_STAGE routes.
The nine Stage-8 CROSS_RANGE proposals are frozen as an explicit untouched,
still-pending partition.
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
    "CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md",
    "BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes/04-Systems-Based-on-Numbers-Notes.md",
)
EXPECTED_SPEC_COUNTS = {"incoming": 23, "within": 15}
EXPECTED_UPDATE_COUNT = 38
EXPECTED_UNTOUCHED_CROSS_RANGE_COUNT = 9
EXPECTED_SPEC_SHA256 = (
    "7283078243ce21bf6a7c34f763b6fddc2421c8cd2132b9b0d63c5fc189d241c9"
)
UNIT_ID = re.compile(r"^U[0-9]{6}$")
ASSET_ID = re.compile(r"^A[0-9]{6}$")


class AuthoringError(ValueError):
    """The current audit state cannot safely receive this proposal."""


@dataclass(frozen=True)
class RouteSpec:
    """One closed target claim from the reviewed Stage 8 route map."""

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
    """Keep the embedded route table compact without hiding target IDs."""

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


# The incoming identities below are the exhaustive 23-route set from the
# independent Stage 8 route audit.  The attempts preserve the route delta's
# attribution, algorithm, locator, and defect boundaries.
ROUTE_SPECS = (
    route_spec(
        "incoming",
        "U000293",
        "",
        "PAGE",
        "the distribution of prime numbers (see page 132)",
        "prime-number generation and distribution",
        "U000739 U000740 U000741 U000742 U000743 U000744 U000745",
        "A000798 A000799",
        (
            "Resolved printed page 132 to the reviewed prime definition, "
            "sieve removal rule, sieve witness, and distribution discussion "
            "at U000739-U000745/A000798-A000799. The closure includes both "
            "generation and the requested distribution evidence without "
            "turning the plots into native sieve state."
        ),
    ),
    route_spec(
        "incoming",
        "U000294",
        "",
        "PAGE",
        "digit sequence of a number like pi ... (see page 136)",
        "digit-sequence construction for pi",
        "U000763 U000764 U000765 U000766 U000767 U000768",
        "A000805",
        (
            "Resolved printed page 136 to U000763-U000768/A000805, which "
            "define pi by the circle ratio and display/describe its base-2 "
            "digits. The target does not give an algorithm for generating "
            "those digits, so this closure is limited to number identity and "
            "the observed digit sequence."
        ),
    ),
    route_spec(
        "incoming",
        "U000297",
        "",
        "PAGE",
        "iterated maps ... discuss on page 149",
        "iterated-map native mechanics",
        "U000827 U000828 U000835 U000836",
        "A000813",
        (
            "Resolved printed page 149 to U000827-U000828 for the repeated "
            "unit-interval map class and U000835-U000836/A000813 for four "
            "concrete formulas, the displayed seed, and successive iterates. "
            "No continuous-CA coupling is imported into the base map class."
        ),
    ),
    route_spec(
        "incoming",
        "U005112",
        "",
        "PAGE",
        "compare page 153",
        "Rule 170 shift-map mechanics and correspondence",
        "U000833 U000835 U000836 U000842 U000850 U005972",
        "A000813",
        (
            "Resolved the comparison to the shift-map formula "
            "x -> FractionalPart[2 x], its base-2 left-shift semantics, and "
            "the page-153 sensitivity discussion at the bounded listed "
            "units/A000813. The target never calls the map Rule 170; that "
            "correspondence remains an attribution supplied by the origin."
        ),
    ),
    route_spec(
        "incoming",
        "U005114",
        "",
        "PAGE",
        "DigitCount[t, 2, 1] is plotted on page 902",
        "Rule 90 black-cell count function",
        "U005658 U005659 U005660 U005661",
        "A000438",
        (
            "Resolved printed Notes page 902 to U005658-U005661/A000438. "
            "Those targets state and plot DigitCount[n,2,1], its bounds, and "
            "alternate formulas. The Rule-90 attribution comes from the "
            "origin and is not invented as a target-page label."
        ),
    ),
    route_spec(
        "incoming",
        "U005114",
        "",
        "PAGE",
        "the connection with the picture on page 117",
        "Rule 90 black-cell position construction",
        "U000661 U000663 U000664 U000665 U000666",
        "A000780 A000781",
        (
            "Resolved printed page 117 to the successive-integer base-2 "
            "array at U000661 and U000663-U000666/A000780-A000781, where "
            "black positions are exactly 1-bit positions. Rule 90 remains "
            "origin-side correspondence context, not a label asserted by "
            "the target."
        ),
    ),
    route_spec(
        "incoming",
        "U005127",
        "",
        "PAGE",
        "See also page 922 for the continuous case.",
        "continuous analog of the additive-rule construction",
        "U006006 U006007 U006008 U006009",
        "A000506",
        (
            "Resolved printed Notes page 922 to U006006-U006009/A000506, "
            "which give the continuous additive update "
            "Mod[RotateLeft[list]+RotateRight[list],1] and its rational/"
            "irrational seed consequences. The target is the continuous "
            "analog, not a new discrete-rule identity."
        ),
    ),
    route_spec(
        "incoming",
        "U005232",
        "",
        "PAGE",
        "sequences based on numbers discussed on page 908",
        "Ulam's non-cellular one-dimensional number-sequence construction",
        "U005796 U005797 U005798 U005799",
        "A000461",
        (
            "Resolved printed Notes page 908 to U005796-U005799/A000461. "
            "The target starts from {1,2}, appends the least uniquely "
            "representable pair-sum, lists initial terms, and records its "
            "growth observations; it is kept distinct from cellular rules."
        ),
    ),
    route_spec(
        "incoming",
        "U005242",
        "",
        "PAGE",
        "pages 132 and 910",
        "prime-number generation",
        "U000740 U000741 U000742 U005810",
        "A000798",
        (
            "Resolved the two-page pointer to the sieve construction at "
            "U000740-U000742/A000798 and the indexed-prime/asymptotic "
            "computation discussion at U005810. Distribution observers are "
            "not promoted into the prime-generation law."
        ),
    ),
    route_spec(
        "incoming",
        "U005242",
        "",
        "PAGE",
        "pages 132 and 910",
        "perfect-number construction",
        "U005818",
        "",
        (
            "Resolved only the literal Notes-page-910 target U005818, which "
            "gives the exact perfect-number predicate "
            "DivisorSigma[1,n]-2n == 0. Printed page 132 contributes no "
            "perfect-number mechanics. The adjacent U005830 Euclid-Euler "
            "generator is intentionally excluded because it lies on the "
            "following Notes page; this preserves the documented locator "
            "mismatch without silently widening the route."
        ),
    ),
    route_spec(
        "incoming",
        "U005245",
        "",
        "PAGE",
        "pages 143 and 915",
        "continued-fraction construction from simple formulas",
        (
            "U000797 U000798 U000799 U000800 U000801 U000802 "
            "U005887 U005888 U005889 U005890"
        ),
        "",
        (
            "Resolved the paired targets to U000797-U000802 for the nested "
            "addition/division denotation and U005887-U005890 for the exact "
            "forward continued-fraction extraction and inverse fold. Later "
            "observers and the Euclidean correspondence are outside this "
            "narrow construction route."
        ),
    ),
    route_spec(
        "incoming",
        "U005245",
        "",
        "PAGE",
        "pages 143 and 915",
        "continued-fraction construction details",
        (
            "U000797 U000798 U000799 U000800 U000801 U000802 U000803 "
            "U000804 U000805 U000806 U000807 U000808 U000809 "
            "U005887 U005888 U005889 U005890 U005891 U005892 U005893 "
            "U005894 U005895 U005896 U005897 U005898 U005899 U005900 "
            "U005901 U005902 U005903 U005904 U005905 U005906 U005907 "
            "U005908 U005909 U005910 U005911 U005912 U005913 U005914 "
            "U005915 U005916"
        ),
        "A000480 A000481 A000482 A000483 A000484",
        (
            "Resolved the detailed route to the complete bounded main "
            "continued-fraction discussion U000797-U000809 and Notes "
            "algorithms, iterate views, measures, enumerator, and Euclidean "
            "correspondence U005887-U005916. A000480-A000484 are retained as "
            "observer/correspondence witnesses, not additional native state."
        ),
    ),
    route_spec(
        "incoming",
        "U005246",
        "",
        "PAGE",
        "page 136",
        "digit-sequence construction for pi",
        "U000763 U000764 U000765 U000766 U000767 U000768",
        "A000805",
        (
            "Resolved printed page 136 to the same bounded pi definition and "
            "displayed digit-sequence evidence as the other page-136 route. "
            "The target does not supply a digit-generation algorithm."
        ),
    ),
    route_spec(
        "incoming",
        "U005257",
        "",
        "PAGE",
        "page 904",
        "3 n + 1 iteration",
        (
            "U005689 U005690 U005691 U005692 U005693 U005694 U005695 "
            "U005696"
        ),
        "A000443",
        (
            "Resolved printed Notes page 904 to the total parity-conditioned "
            "3 n + 1 map, its convergence query, negative cycles, and "
            "stopping-time discussion at U005689-U005696. A000443 is "
            "DEFECTIVE/DEFECT_LIMITED: cases (a) and (b) are visible, while "
            "the clipped case-(c) formula contributes no inferred mechanics."
        ),
    ),
    route_spec(
        "incoming",
        "U005264",
        "",
        "PAGE",
        "page 918",
        "iterated-map construction class",
        "U005965 U005966 U005967 U005968",
        "",
        (
            "Resolved printed Notes page 918 to U005965-U005968, which "
            "identify repeated rational/smooth maps and give the explicit "
            "FractionalPart[1/x] and FractionalPart[a x] maps plus exact "
            "iterate formulas. Historical description alone is not used as "
            "mechanics."
        ),
    ),
    route_spec(
        "incoming",
        "U005280",
        "",
        "PAGE",
        "page 907",
        "Hofstadter recursive-sequence construction",
        "U005761 U000724 U000725 U000726 U000727",
        "A000796",
        (
            "Resolved the Hofstadter attribution at U005761 together with "
            "the non-fixed-lag recursive setup U000724-U000727 and exact "
            "case-(e) recurrence/seed visible in A000796. A000796 remains "
            "DEFECTIVE and may be used only at its reviewed DEFECT_LIMITED "
            "boundary; the historical attribution alone is not mechanics."
        ),
    ),
    route_spec(
        "incoming",
        "U000560",
        "",
        "PAGE",
        "As discussed on page 122",
        "arithmetic derivation of the register-machine zero-event value map",
        "U000690 U000693",
        "A000787 A000789",
        (
            "Resolved printed page 122 to U000690/U000693 and "
            "A000787/A000789, which give the parity-conditioned arithmetic "
            "rule, the register-machine value map, and the after-first-step "
            "factor-of-3 relation. The comparison is preserved without "
            "merging arithmetic-system and register-machine identities."
        ),
    ),
    route_spec(
        "incoming",
        "U005328",
        "",
        "PAGE",
        "page 901",
        "Gray-code rule ordering",
        "U005647 U005648 U005649 U005650",
        "A000437",
        (
            "Resolved printed Notes page 901 to U005647-U005650/A000437. "
            "The target defines successive one-digit Gray ordering, gives "
            "the recursive generator and direct "
            "BitXor[i,Floor[i/2]] position law, and supplies its ordering "
            "witness."
        ),
    ),
    route_spec(
        "incoming",
        "U005463",
        "",
        "PAGE",
        "page 904",
        "quadratic-irrational projection sequences",
        (
            "U005678 U005679 U005680 U005681 U005682 U005683 U005684 "
            "U005685"
        ),
        "A000440",
        (
            "Resolved printed Notes page 904 to the irrational-slope "
            "projection law and continued-fraction-derived substitution "
            "algorithm at U005678-U005685/A000440, including the repeating "
            "rule-list special case for quadratic irrationals. Projection "
            "and substitution identities remain distinct."
        ),
    ),
    route_spec(
        "incoming",
        "U005501",
        "",
        "PAGE",
        "page 128",
        "general recurrence-relation systems",
        "U000717 U000719 U000720 U000721 U000722 U000723",
        "A000795",
        (
            "Resolved printed page 128 to U000717 and U000719-U000723/"
            "A000795. The target defines dependence on earlier terms, "
            "distinguishes single- and multiple-lag forms, and supplies the "
            "concrete linear-recurrence presets without importing adjacent "
            "non-fixed-lag examples."
        ),
    ),
    route_spec(
        "incoming",
        "U005502",
        "",
        "PAGE",
        "page 117",
        "digit-sequence nested construction",
        "U000661 U000662 U000663 U000664 U000665 U000666",
        "A000780 A000781",
        (
            "Resolved printed page 117 to U000661-U000666/"
            "A000780-A000781. Repeated addition of 1 generates successive "
            "integers whose base-2 rows form the explicitly described nested "
            "digit pattern."
        ),
    ),
    route_spec(
        "incoming",
        "U005507",
        "",
        "PAGE",
        "page 904",
        "substitution sequences as irrational-slope projections",
        (
            "U005678 U005679 U005680 U005681 U005682 U005683 U005684 "
            "U005685"
        ),
        "A000440",
        (
            "Resolved printed Notes page 904 to the same bounded projection "
            "sequence and continued-fraction-to-substitution mechanics as "
            "the related route. The closure records the correspondence "
            "without collapsing the projection function and substitution "
            "generator."
        ),
    ),
    route_spec(
        "incoming",
        "U005635",
        "",
        "PAGE",
        "page 921",
        "iterated-map universal behavior",
        "U005990 U005991 U005992",
        "A000504",
        (
            "Resolved printed Notes page 921 to U005990-U005992/A000504, "
            "which give the smooth logistic-map period-doubling sequence and "
            "state universality for smooth one-hump maps. The image is the "
            "parameter-sweep witness, not a separate evolution law."
        ),
    ),
    # Final Stage-8-local identities come directly from the repaired main and
    # Notes worker outputs.  Optional U000836/U000882 pointers are included
    # because those final outputs deliberately emitted them.
    route_spec(
        "within",
        "U000833",
        "",
        "OTHER",
        "as the picture illustrates",
        "case (d) shift-map formula and trajectory in the illustrated four-map figure",
        "U000835 U000836",
        "A000813",
        (
            "Resolved the exact illustrated-pointer identity to "
            "U000835-U000836/A000813, where case (d)'s shift-map formula and "
            "trajectory are shown. No fabricated page locator is introduced."
        ),
    ),
    route_spec(
        "within",
        "U000836",
        "",
        "PAGE",
        "compare page 122",
        "earlier arithmetic systems based on repeated multiplication and their digit-sequence behavior",
        (
            "U000680 U000681 U000682 U000683 U000684 U000685 U000686 "
            "U000687 U000688 U000689 U000690 U000691 U000692 U000693"
        ),
        "A000786 A000787 A000788 A000789",
        (
            "Resolved the optional contextual comparison to the complete "
            "bounded page-122 arithmetic-system discussion "
            "U000680-U000693/A000786-A000789. It remains a source comparison "
            "and does not merge the page-150 iterated-map presets with those "
            "arithmetic constructions."
        ),
    ),
    route_spec(
        "within",
        "U000850",
        "",
        "PAGE",
        "the shift map—shown as case (d) on pages 150 and 151",
        "shift-map formula and simple/random initial-condition runs",
        "U000835 U000836 U000837 U000838",
        "A000813 A000814",
        (
            "Resolved pages 150-151 to U000835-U000838/"
            "A000813-A000814, which supply case (d)'s formula plus its simple "
            "and random initial-condition runs. The page-153 comparison "
            "remains an observer experiment around that fixed map."
        ),
    ),
    route_spec(
        "within",
        "U000857",
        "",
        "PAGE",
        "systems like (a) and (b) on pages 150 and 151",
        "iterated-map cases (a) and (b) from simple initial conditions",
        "U000835 U000836 U000837 U000838",
        "A000813 A000814",
        (
            "Resolved pages 150-151 to the displayed cases (a)/(b), formulas, "
            "and simple/random seed regimes at U000835-U000838/"
            "A000813-A000814. The intrinsic-randomness discussion is kept as "
            "a conclusion about these runs, not part of either map law."
        ),
    ),
    route_spec(
        "within",
        "U000865",
        "",
        "SECTION",
        "the iterated maps that we just discussed in the previous section",
        "unit-interval iterated-map family and scalar postprocessing mechanics",
        "U000827 U000828 U000835 U000836 U000837 U000838",
        "A000813 A000814",
        (
            "Resolved the previous-section half of the composition to the "
            "unit-interval iterated-map class and concrete scalar presets at "
            "U000827-U000828 and U000835-U000838/A000813-A000814. This "
            "provides the scalar postprocessing component without replacing "
            "the separate cross-range totalistic-CA route."
        ),
    ),
    route_spec(
        "within",
        "U000873",
        "",
        "PAGE",
        "exactly iterated map (a) from page 150",
        "unit-interval iterated map x -> FractionalPart[(3/2)x]",
        "U000835 U000836",
        "A000813",
        (
            "Resolved the exact map-(a) pointer to U000835-U000836/A000813, "
            "where x -> FractionalPart[(3/2)x] is printed. The continuous-CA "
            "candidate uses it as scalar postprocessing; the two native "
            "objects are not merged."
        ),
    ),
    route_spec(
        "within",
        "U000882",
        "",
        "PAGE",
        "the picture in the middle of page 160",
        "c=0.3299 additive continuous-CA continuation and adjacent-cell difference view",
        "U000885 U000886",
        "A000827",
        (
            "Resolved the optional observer pointer to U000885-U000886/"
            "A000827, the middle continuation and adjacent-cell difference "
            "view for c=0.3299. The route closes a display relation only and "
            "adds no native update mechanics."
        ),
    ),
    route_spec(
        "within",
        "U000886",
        "",
        "PAGE",
        "the same kind of rules as on the previous page",
        "additive-constant continuous-CA family and parameter presets",
        (
            "U000875 U000876 U000877 U000878 U000879 U000880 U000881 "
            "U000882 U000883 U000884"
        ),
        "A000824 A000825 A000826",
        (
            "Resolved the previous-page locator to U000875-U000884/"
            "A000824-A000826, which give the additive-constant rule family "
            "and displayed parameter presets. The corrected route kind "
            "remains PAGE and the continuation at U000885-U000886 is outside "
            "this prior-page target."
        ),
    ),
    route_spec(
        "within",
        "U000897",
        "",
        "PAGE",
        "the continuous cellular automaton on page 156",
        "pure-average continuous cellular automaton and its diffusion limit",
        "U000866 U000867 U000868 U000869",
        "A000822",
        (
            "Resolved printed page 156 to U000866-U000869/A000822, which "
            "define the pure left/self/right averaging continuous CA used in "
            "the diffusion limit. The PDE relation remains distinct from the "
            "discrete numerical evolution."
        ),
    ),
    route_spec(
        "within",
        "U000936",
        "",
        "PAGE",
        "the same equations as on the previous page",
        "three nonlinear PDE formulas and their shorter-time solutions",
        (
            "U000920 U000921 U000922 U000923 U000924 U000925 U000926 "
            "U000927 U000928"
        ),
        "A000834 A000835 A000836 A000837 A000838 A000839",
        (
            "Resolved the previous-page equations to U000920-U000928/"
            "A000834-A000839, the three nonlinear field equations and their "
            "shorter-time solutions. Numerical figures remain solution/"
            "observer evidence rather than equation identity."
        ),
    ),
    route_spec(
        "within",
        "U005728",
        "",
        "PAGE",
        "page 128",
        "coefficients, orders, and initial values of the page-128 linear recurrences",
        (
            "U000717 U000718 U000719 U000720 U000721 U000722 U000723"
        ),
        "A000795",
        (
            "Resolved printed page 128 to U000717-U000723/A000795, which "
            "supply the recurrence orders, coefficients, initial values, and "
            "examples missing from the Notes pointer."
        ),
    ),
    route_spec(
        "within",
        "U005802",
        "",
        "PAGE",
        "page 132",
        "sieve-of-Eratosthenes removal/filter procedure for generating the primes",
        "U000738 U000739 U000740 U000741 U000742",
        "A000798",
        (
            "Resolved the Notes page-132 sieve pointer to U000738-U000742/"
            "A000798. These units identify the prime sequence and state/show "
            "the repeated removal of larger multiples. Prime distribution "
            "plots and the separate Fermat congruence are outside this "
            "bounded procedure route."
        ),
    ),
    route_spec(
        "within",
        "U005820",
        "",
        "PAGE",
        "page 135",
        "necessary-and-sufficient sum-of-three-squares representability condition",
        "U000755 U000760",
        "A000802",
        (
            "Resolved printed page 135 to U000755/U000760 and A000802, which "
            "give case (c) and the exact excluded form 4^r(8s+7). Adjacent "
            "sum-of-squares counts are not substituted for this "
            "necessary-and-sufficient representability condition."
        ),
    ),
    route_spec(
        "within",
        "U005863",
        "",
        "PAGE",
        "page 141",
        "per-step update law for the digit-by-digit square-root construction",
        "U000786 U000787 U000788 U000789 U000790",
        "A000808",
        (
            "Resolved printed page 141 to U000786-U000790/A000808, the "
            "displayed digit-by-digit square-root state, invariant, and "
            "per-step digit choice. Newton and recurrence-ratio solvers "
            "remain separate constructions."
        ),
    ),
    route_spec(
        "within",
        "U005945",
        "",
        "PAGE",
        "page 903",
        "substitution rules for cosine/sine zero-spacing sequences",
        "U005681 U005682 U005683 U005684 U005685",
        "",
        (
            "Resolved printed Notes page 903 to U005681-U005685, which give "
            "the irrational-slope difference sequence and the "
            "continued-fraction-derived substitution rules used for the "
            "zero-spacing correspondence. The trigonometric zero observer "
            "and substitution generator remain distinct."
        ),
    ),
)


# These final Stage 8 proposals are intentionally outside ROUTE_SPECS.  The
# authoring preflight proves the exact partition still exists, is PENDING,
# and carries no target claims or attempts.
UNTOUCHED_CROSS_RANGE_IDENTITIES = (
    (
        "U000693",
        "",
        "PAGE",
        "the register machine shown on page 100",
        "register-machine realization and state encoding for the printed arithmetic map",
    ),
    (
        "U000792",
        "",
        "PAGE",
        "the substitution systems on page 83",
        "substitution-system construction of nested digit sequences",
    ),
    (
        "U000819",
        "",
        "OTHER",
        "a generalized substitution system",
        "base mechanics of generalized substitution systems used by the axis-crossing encoding",
    ),
    (
        "U000822",
        "",
        "PAGE",
        "the Fibonacci substitution system on page 83",
        "Fibonacci substitution-system mechanics and the analogous axis-crossing preset",
    ),
    (
        "U000865",
        "",
        "SECTION",
        "the totalistic cellular automaton rules that we discussed at the beginning of the last chapter",
        "discrete totalistic cellular-automaton base mechanics",
    ),
    (
        "U005657",
        "",
        "PAGE",
        "page 83",
        "replacement rule and seed for the rotated page-117 substitution preset",
    ),
    (
        "U005671",
        "",
        "PAGE",
        "page 614",
        "complicated base-6 powers-of-three pattern used for the cellular-automaton correspondence",
    ),
    (
        "U005927",
        "",
        "PAGE",
        "page 560",
        "integer-representation construction referenced without mechanics",
    ),
    (
        "U006010",
        "",
        "PAGE",
        "page 591",
        "rule choices, probabilities, and seeds for probabilistic cellular automata",
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
    target_defect_assets: set[str] = set()
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
        target_defect_assets.update(
            asset_id
            for asset_id in spec.target_asset_ids
            if asset_id in {"A000443", "A000796"}
        )
    if origins != EXPECTED_SPEC_COUNTS:
        raise AuthoringError(f"embedded route counts drifted: {origins!r}")
    if len(ROUTE_SPECS) != EXPECTED_UPDATE_COUNT:
        raise AuthoringError("embedded route update total drifted")
    if target_defect_assets != {"A000443", "A000796"}:
        raise AuthoringError(
            "embedded defect-limited target partition drifted"
        )
    if (
        len(UNTOUCHED_CROSS_RANGE_IDENTITIES)
        != EXPECTED_UNTOUCHED_CROSS_RANGE_COUNT
        or len(set(UNTOUCHED_CROSS_RANGE_IDENTITIES))
        != EXPECTED_UNTOUCHED_CROSS_RANGE_COUNT
    ):
        raise AuthoringError(
            "untouched Stage 8 CROSS_RANGE identity count drifted"
        )
    if identities & set(UNTOUCHED_CROSS_RANGE_IDENTITIES):
        raise AuthoringError(
            "a CROSS_RANGE identity was added to the resolution specs"
        )
    digest = spec_sha256(embedded_spec_payload())
    if digest != EXPECTED_SPEC_SHA256:
        raise AuthoringError(
            "embedded route-map projection digest drifted: "
            f"{digest} != {EXPECTED_SPEC_SHA256}"
        )
    return digest


def source_map_payload(path: Path) -> list[dict[str, Any]]:
    """Load only governed claims from an external route-map artifact."""

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
    """Prove that a source map makes no extra governed target claims."""

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
    if any(
        None in row or any(value is None for value in row.values())
        for row in rows
    ):
        raise AuthoringError(f"{path.name} contains a malformed row")
    return rows


def atomic_create(path: Path, payload: bytes) -> None:
    """Create a proposal exactly once, durably, without following symlinks."""

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
    if review["review_stage"] != "8":
        raise AuthoringError(
            f"{label} unit was not closed by Stage 8: {unit_id}"
        )
    if (
        unit.get("path") not in STAGE_PATHS
        or review["path"] != unit.get("path")
    ):
        raise AuthoringError(
            f"{label} unit lies outside the Stage 8 source paths: {unit_id}"
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
    if asset["review_stage"] != "8":
        raise AuthoringError(
            f"{label} asset was not closed by Stage 8: {asset_id}"
        )
    if asset["assignment_path"] not in STAGE_PATHS:
        raise AuthoringError(
            f"{label} asset lies outside the Stage 8 source paths: {asset_id}"
        )
    if asset_id in {"A000443", "A000796"}:
        if (
            asset["source_status"] != "DEFECTIVE"
            or asset["original_resolution_status"] != "REVIEWED"
        ):
            raise AuthoringError(
                f"{label} defect-limited asset boundary drifted: {asset_id}"
            )
    elif asset["source_status"] != "CLEAR":
        raise AuthoringError(
            f"{label} target asset is unexpectedly non-clear: {asset_id}"
        )


def require_unclaimed_pending_route(
    row: dict[str, str],
    *,
    label: str,
) -> None:
    if row["status"] != "PENDING":
        raise AuthoringError(f"{label} route is not PENDING")
    if (
        row["target_unit_ids"] != "[]"
        or row["target_asset_ids"] != "[]"
        or row["attempts"] != "[]"
    ):
        raise AuthoringError(
            f"{label} route already carries target claims or attempts"
        )


def build_proposal(goal_dir: Path) -> dict[str, Any]:
    """Build the exact 38-row identity-keyed Stage 8 closure proposal."""

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
    if terminal.get("mode") != "INITIAL" or terminal.get("stage") != 8:
        raise AuthoringError(
            "expected the terminal combined Stage 8 INITIAL review event"
        )
    if tuple(terminal.get("source_paths", ())) != STAGE_PATHS:
        raise AuthoringError(
            "terminal review event is not the combined Stage 8 assignment"
        )
    epoch = terminal.get("epoch")
    if isinstance(epoch, bool) or not isinstance(epoch, int) or epoch < 1:
        raise AuthoringError(f"invalid active review epoch: {epoch!r}")

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
    observed_within = {
        route_identity(row)
        for row in routes
        if row["owning_stage"] == "8"
        and row["closure_scope"] == "WITHIN_STAGE"
        and row["status"] == "PENDING"
    }
    if observed_within != expected_within:
        missing = sorted(expected_within - observed_within)
        extra = sorted(observed_within - expected_within)
        raise AuthoringError(
            "Stage 8 WITHIN_STAGE route set differs from the governed map: "
            f"missing={missing!r} extra={extra!r}"
        )

    expected_cross = set(UNTOUCHED_CROSS_RANGE_IDENTITIES)
    observed_cross_rows = [
        row
        for row in routes
        if row["owning_stage"] == "8"
        and row["closure_scope"] == "CROSS_RANGE"
    ]
    observed_cross = {
        route_identity(row) for row in observed_cross_rows
    }
    if observed_cross != expected_cross:
        missing = sorted(expected_cross - observed_cross)
        extra = sorted(observed_cross - expected_cross)
        raise AuthoringError(
            "Stage 8 CROSS_RANGE route set differs from the frozen untouched "
            f"partition: missing={missing!r} extra={extra!r}"
        )
    if len(observed_cross_rows) != EXPECTED_UNTOUCHED_CROSS_RANGE_COUNT:
        raise AuthoringError(
            "Stage 8 CROSS_RANGE route multiplicity drifted"
        )
    for row in observed_cross_rows:
        require_unclaimed_pending_route(row, label="untouched CROSS_RANGE")

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
        require_unclaimed_pending_route(before, label="governed")
        if spec.origin == "within":
            if (
                before["owning_stage"] != "8"
                or before["closure_scope"] != "WITHIN_STAGE"
            ):
                raise AuthoringError(
                    "within-stage route metadata drifted: "
                    f"{spec.identity!r}"
                )
        else:
            if (
                before["owning_stage"] == "8"
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

    if (
        origin_counts != EXPECTED_SPEC_COUNTS
        or len(updates) != EXPECTED_UPDATE_COUNT
    ):
        raise AuthoringError(
            f"route update counts drifted: {origin_counts!r}"
        )
    if len(matched_route_ids) != EXPECTED_UPDATE_COUNT:
        raise AuthoringError(
            "route selection did not produce 38 unique rows"
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
        "coordinator_id": "ch04-numbers-route-closure-e1",
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
            print(
                f"Chapter 4 route specification check failed: {exc}",
                file=sys.stderr,
            )
            return 1
        suffix = " source-map=matched" if len(sys.argv) == 3 else ""
        print(
            "Chapter 4 route specification valid: "
            f"incoming=23 within=15 untouched-cross=9 "
            f"sha256={digest}{suffix}"
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
        print(f"Chapter 4 route authoring failed: {exc}", file=sys.stderr)
        return 1
    print(
        "authored Chapter 4 route closure: "
        f"updates={len(proposal['route_updates'])} "
        f"sha256={hashlib.sha256(canonical_json_bytes(proposal)).hexdigest()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
