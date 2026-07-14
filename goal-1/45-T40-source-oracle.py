#!/usr/bin/env python3
"""Fail-closed primary-source audit for T40 mathematical-constant expansions.

T40's native identity is an immutable exact-number/representation denotation
plus typed coefficient queries.  It is not a fabricated mutable constant or a
mandatory append-prefix transition.  The Book also gives explicit algorithms
(long division, a square-root digit machine, continued-fraction iteration)
whose visible work states may be represented by ordinary SimplePrograms; those
are realizations of the denotation, not hidden executor state or T40's identity.

The Book does not use the catalog label.  Eighteen bounded, redundant query
lanes freeze discovery witnesses, while independent fixed universes close all
117 nonblank rows in the strict main section and all audited relevant rows in
the actual flattened Index.  The chapter split is intentionally treated as an
abridged summary: compressed tables and omitted mechanics are explicit split
dispositions rather than silently invented matches.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from fractions import Fraction
from pathlib import Path


if not __debug__:
    raise RuntimeError("T40 source oracle requires assertions; do not use -O")


SCRIPT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BOOK = SCRIPT_ROOT / "ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md"
INDEX_FIRST_LINE = 20826
EXPECTED_BOOK_LINES = 22498
EXPECTED_BOOK_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"
EXPECTED_ATLAS_SHA256 = "5ffab93f0007bbeb5da60af7cc08570f9a358c9f9f94e37c5e00f9fc0997bc8a"
EXPECTED_CATALOG_SHA256 = "26cef05af1155f80bc301900d2df95469a90de027ba860730519d25d096c2b73"
EXPECTED_TAXONOMY_SHA256 = "4c30fe079b2fb8f69e4c8c0dde3d59065227d4224cbe4b7693a17c0126cc3f1a"


def line_set(spec: str) -> frozenset[int]:
    result: set[int] = set()
    for item in filter(None, map(str.strip, spec.split(","))):
        if "-" in item:
            start, end = map(int, item.split("-", 1))
            result.update(range(start, end + 1))
        else:
            result.add(int(item))
    return frozenset(result)


# Exactly eighteen bounded lanes from the first-principles audit.  Q00 proves
# that the catalog label is external vocabulary; Q15/Q16 close all 24 images.
QUERIES = {
    "Q00": r"Mathematical-Constant Digit Systems?",
    "Q01": r"Mathematical Constants",
    "Q02": (
        r"first 4000 digits|first 20,000 digits|two hundred billion digits|"
        r"circumference.{0,100}diameter"
    ),
    "Q03": (
        r"digit sequences for various rational|number of the form p/q|"
        r"standard long division|remainder at each of the steps"
    ),
    "Q04": (
        r"procedure for generating.{0,80}square roots|two numbers r and s|"
        r"s\^2 \+ 4r"
    ),
    "Q05": (
        r"cube roots.{0,80}fourth roots|logarithms and exponentials|"
        r"only kinds of numbers that have repetitive"
    ),
    "Q06": (
        r"representation for a number|procedures for building up|"
        r"continued fraction representations?"
    ),
    "Q07": (
        r"Computing.{0,40}digits directly|PowerMod\[2|Simon Plouffe|"
        r"values of \*?PolyLog\*?"
    ),
    "Q08": (
        r"Digit sequence properties|normal in a particular base|"
        r"statistical tests of randomness|Stoneham"
    ),
    "Q09": (
        r"Nested digit sequences|Concatenation sequences|Runs of digits|"
        r"Leading digits"
    ),
    "Q10": (
        r"Page 143.{0,20}Continued fractions|Khinchin|Hurwitz numbers|"
        r"Jeffrey Shallit"
    ),
    "Q11": (
        r"Floor\[NestList\[1/Mod|FromContinuedFraction|Euclid.s algorithm|"
        r"Egyptian fractions|Nested radicals|Digital slope representation"
    ),
    "Q12": (
        r"continued fraction map|Iterated division|compare page 153|"
        r"continued fraction.{0,120}substitution"
    ),
    "Q13": (
        r"noncomputable.{0,80}digit|Chaitin.{0,120}digit|"
        r"digits of.{0,40}sqrt.{0,120}cellular automata|"
        r"digit sequence.{0,100}data compression"
    ),
    "Q14": (
        r"Mathematical constants, 136-144|Continued fractions, 143, 914|"
        r"Digit sequences, 116-127, 136-142|Number representations, 142|"
        r"Normal numbers, 912|Rational numbers approximation by|"
        r"Plouffe, Simon|Khinchin \(Khinchin.s constant\)"
    ),
    "Q15": r"_page_(?:151_Figure_7|154_Figure_2|156_Figure_1)\.jpeg",
    "Q16": (
        r"_page_(?:927_Figure_14|928_Figure_(?:9|11|13|22)|"
        r"929_Picture_1[1-6]|930_(?:Picture_(?:4|12|14)|Figure_10)|"
        r"931_Figure_(?:9|10|11|12|13|17))\.jpeg"
    ),
    "Q17": (
        r"^#### (?:\*\*)?(?:The Sequence of Primes|Mathematical Functions)"
        r"(?:\*\*)?$"
    ),
}


def digest(values: set[int] | frozenset[int]) -> str:
    return hashlib.sha256(
        ",".join(map(str, sorted(values))).encode("ascii")
    ).hexdigest()


def digest_records(records: set[str] | list[str] | tuple[str, ...]) -> str:
    return hashlib.sha256("\n".join(sorted(records)).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_book(argument: str | None) -> tuple[Path, Path, Path]:
    if argument is not None:
        book = Path(argument).resolve()
    elif DEFAULT_BOOK.is_file():
        book = DEFAULT_BOOK.resolve()
    else:
        candidate = (
            Path.cwd() / "ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md"
        ).resolve()
        if not candidate.is_file():
            raise FileNotFoundError("cannot locate default A New Kind of Science source")
        book = candidate
    return book, book.parent, book.parents[2]


# The pre-Index query universe is exhaustively dispositioned.  These are
# query hits, not every continuation retained below.
QUERY_NATIVE = line_set(
    "1665,1673,1675,1677,1679,1685,1687,1689,1707,1711,1713,1715,"
    "1740,1742,1744,1746,1748,1750,1772,1778,1784,1786,1792,1794,"
    "1828,12921,12943,12948,12958,12960,12972,12976,12982,13030,"
    "13032,13034,13040,13042,13044,13046,13048,13050,13052,13060,"
    "13086,13090"
)
QUERY_RELATION = line_set(
    "1850,1852,1856,11260,11531,12569,12984,12986,12988,12990,"
    "12992,12996,13000,13004,13018,13020,13022,13023,13029,13062,"
    "13074,13076,13084,13092,13094,13096,13098,13102,13103,13111,"
    "13119,13121,13123,13125,13127,14172,14468,14923,17236,17599,20592"
)
QUERY_CONTROL = line_set("1619,1834,12846,13134,13146,17101,19058")

EXCLUDED_CLASS = {
    "name_collision": line_set("146"),
    "unrelated_representation_context": line_set("6772"),
    "generic_algorithm_cross_reference": line_set("17845,19345,19563"),
}
EXCLUDED = frozenset().union(*EXCLUDED_CLASS.values())


# Query recall is not the closure proof.  Independently enumerate every
# nonblank/content row in the strict BOOK1665--1832 main section, including
# all table payloads and extraction artifacts.  N/R/C/X are semantic roles;
# STRUCTURAL rows carry only Markdown/table/page-extraction structure.
STRICT_MAIN_NATIVE = line_set(
    "1665,1667,1669,1671,1673,1675,1677,1679,1681,1683,1685,1687,"
    "1689,1691,1693,1695-1698,1700-1704,1707,1709,1711,1713,1715,"
    "1717,1719,1721,1723-1729,1733,1736,1738,1740,1742,1744,1746,"
    "1748,1750,1754,1756-1770,1772,1774,1776,1778,1780,1782,1784,"
    "1786,1789,1792,1794,1796,1798,1804,1806-1826,1828,1830,1832"
)
STRICT_MAIN_RELATION = frozenset()
STRICT_MAIN_CONTROL = frozenset()
STRICT_MAIN_EXCLUDED = frozenset()
STRICT_MAIN_STRUCTURAL = line_set(
    "1694,1699,1705,1722,1730,1732,1734,1752,1755,1788,1790,"
    "1800-1802,1805"
)
STRICT_MAIN_DISPOSITION = {
    "native": STRICT_MAIN_NATIVE,
    "relation": STRICT_MAIN_RELATION,
    "control": STRICT_MAIN_CONTROL,
    "excluded": STRICT_MAIN_EXCLUDED,
    "structural": STRICT_MAIN_STRUCTURAL,
}
STRICT_MAIN_CONTENT = frozenset().union(*STRICT_MAIN_DISPOSITION.values())


# Structural continuations preserve the mechanics and their epistemic
# qualifications even when no query regexp lands on the row itself.
NATIVE_CONTINUATIONS = line_set(
    "1667,1669,1671,1681,1683,1691,1709,1717,1719,1733,1736,1738,"
    "1774,1776,1780,1782,1789,1796,1798,1830,1832,"
    "12923,12925-12941,12945-12956,12962,12964,12966,12968,12970,"
    "12974,12978,12980,13036,13038,13054,13056,13058,13070,13072,"
    "13088,13100"
)
RELATION_CONTINUATIONS = line_set(
    "12994,12998,13002,13006-13016,13025,13027,13064-13068,"
    "13078-13082,13105,13107,13109,13113,13115,13117,13129,13130,"
    "13132,13136,13138-13144"
)
CONTROL_CONTINUATIONS = line_set("1663,12919")

NATIVE_EVIDENCE = QUERY_NATIVE | NATIVE_CONTINUATIONS | STRICT_MAIN_NATIVE
RELATION_EVIDENCE = QUERY_RELATION | RELATION_CONTINUATIONS
CONTROL_EVIDENCE = QUERY_CONTROL | CONTROL_CONTINUATIONS
RETAINED = NATIVE_EVIDENCE | RELATION_EVIDENCE | CONTROL_EVIDENCE


INDEX_CLASS = {
    "native": line_set(
        "20828,20910,20916,20918,20946,21044,21054,21088,21255,"
        "21337,21360,21416,21473,21475,21501,21683,21705,21711,"
        "21735,21779,21793,21801,21891,21907,22136"
    ),
    "relation": line_set(
        "20840,20850,20914,20967,20972,21014,21038,21050,21114,"
        "21132,21134,21150,21162,21168,21172,21173,21185,21187,"
        "21193,21195,21197,21203,21207,21213,21223,21231,21264,"
        "21432,21450,21497,21525,21675,21687,21689,21695,21805,"
        "21813,21819,21845,21893,21915,21927,21929,21933,21982,"
        "21990,21994,22030,22080,22110,22144,22148,22150,22352,"
        "22380,22394"
    ),
    "control": line_set("22096"),
}
INDEX_ROUTED = frozenset().union(*INDEX_CLASS.values())
INDEX_EXCLUDED = frozenset()
INDEX_RELEVANT_UNIVERSE = line_set(
    "20828,20840,20850,20910,20914,20916,20918,20946,20967,20972,"
    "21014,21038,21044,21050,21054,21088,21114,21132,21134,21150,"
    "21162,21168,21172,21173,21185,21187,21193,21195,21197,21203,"
    "21207,21213,21223,21231,21255,21264,21337,21360,21416,21432,"
    "21450,21473,21475,21497,21501,21525,21675,21683,21687,21689,"
    "21695,21705,21711,21735,21779,21793,21801,21805,21813,21819,"
    "21845,21891,21893,21907,21915,21927,21929,21933,21982,21990,"
    "21994,22030,22080,22096,22110,22136,22144,22148,22150,22352,"
    "22380,22394"
)

INDEX_ENTRY_GUARDS = {
    20828: ("continued fraction for, 144", "digits of, 142"),
    20840: ("Addition cellular automata based on", "in digit sequences, 118"),
    20850: ("nested digit sequences",),
    20910: ("Base 16 (hex)", "normal numbers, 912"),
    20914: ("leading digits", "Egyptian fractions"),
    20916: ("Bits in numbers, 116", "see also Digit sequences"),
    20918: ("Blocks", "normal numbers, 912"),
    20946: ("Catalan (Catalan's constant)", "and digit sequences, 902"),
    20967: ("states vs. digit sequences, 950",),
    20972: ("Champernowne number", "normal numbers, 912"),
    21014: ("of number representations, 1070",),
    21038: ("Concatenation sequences", "continued fractions for, 915"),
    21044: ("Continued fraction map", "Continued fractions, 143, 914"),
    21050: ("Corollaries", "nested radicals"),
    21054: ("Cryptanalysis continued fraction for, 914", "digits of, 141"),
    21088: ("Digit sequences, 116-127, 136-142",),
    21114: ("Dynamic programming", "Egyptian fractions"),
    21132: ("runs of digits",),
    21134: ("ENIAC (computer)", "and digits of  $\\pi$ , 911"),
    21150: ("Equidistribution", "concatenation sequences"),
    21162: ("Exact solutions", "Euclid's algorithm"),
    21168: ("ExpIntegralEi", "Egyptian fractions"),
    21172: ("leading digits", "Factorial2"),
    21173: ("multiplicative digit sequences, 902",),
    21185: ("Feynman diagrams", "leading digits"),
    21187: ("Fibonacci number representation. 560, 1070",),
    21193: ("and digital slopes, 916",),
    21195: ("Fractional linear transformations and continued fractions, 914",),
    21197: ("Fraenkel", "leading digits"),
    21203: ("applied to digit sequences, 731",),
    21207: ("and quadratic continued fractions, 915",),
    21213: ("Generalization", "Euclid's algorithm"),
    21223: ("Gibbs phenomenon", "Euclid's algorithm"),
    21231: ("Graphics3D", "concatenation sequences"),
    21255: ("Human thinking", "Hurwitz numbers"),
    21264: ("and continued fractions, 914<br>",),
    21337: ("Irrational numbers", "iterated multiplication by, 903"),
    21360: ("Iterated division", "continued fractions, 143"),
    21416: ("Khinchin", "Khinchin's constant"),
    21432: ("and continued fractions, 915", "Lagrange points"),
    21450: ("LatticeReduce", "Leading digits"),
    21473: ("Log (logarithm)", "computation of  $n^{th}$  digits"),
    21475: ("Long division, 139",),
    21497: ("Markov partitions and digit sequences, 901",),
    21501: ("Mathematical constants, 136-144",),
    21525: ("Multiplicative digit sequences, 902", "and continued fractions, 914"),
    21675: ("Nested radicals, 915",),
    21683: ("NestWhileList", "concatenation sequences"),
    21687: ("leading digits",),
    21689: ("for computing square roots, 913",),
    21695: ("Non-locality and Bell's inequalities", "in digit sequences, 730"),
    21705: ("Normal numbers, 912", "concatenation sequences"),
    21711: ("Number representations, 142",),
    21735: ("Partial quotients", "in continued fractions, 914"),
    21779: (
        "computation of nth digits in, 912",
        "continued fraction for, 143, 914",
        "digit sequence of, 136",
    ),
    21793: ("Plouffe, Simon", "computation of  $\\pi$"),
    21801: ("PolyLog (polylogarithms)", "and computing  $n^{th}$  digits, 912"),
    21805: ("PowerMod", "digit sequences of, 119, 614, 749"),
    21813: ("leading digits in, 914",),
    21819: ("ProductLog", "concatenation sequences"),
    21845: ("Pythagoreans", "continued fraction map"),
    21891: ("Radicals continued fractions for, 144", "digit sequences for, 139"),
    21893: ("from digits of  $\\pi$ , 136, 912", "in digit of square roots, 139"),
    21907: ("Rational numbers approximation by",),
    21915: ("Reciprocals", "Egyptian fractions"),
    21927: ("in digit sequences, 138",),
    21929: ("Repetitive sequences", "Egyptian fractions"),
    21933: ("Reversal, of digit sequences, 905",),
    21982: ("and continued fractions, 914",),
    21990: ("Roth, Klaus F.", "and rational approximations, 915"),
    21994: ("square root of, 956",),
    22030: ("Run-length encoding, 560", "as number representation, 914"),
    22080: ("Russian peasant method", "concatenation sequences"),
    22096: ("see also Digit sequences", "Semi-Thue systems"),
    22110: ("Shallit, Jeffrey O.", "and continued fractions, 914"),
    22136: ("Stoneham", "normal numbers, 912"),
    22144: ("Substitution systems, 82-87", "and continued fractions, 914"),
    22148: ("Superstrings", "runs of digits"),
    22150: ("Symbolic programming", "leading digits"),
    22352: ("Toffoli, Tommaso", "Egyptian fractions"),
    22380: ("Two's complement number representation, 902, 942",),
    22394: ("Valuation functions", "nested digit sequences"),
}

# A handful of witnesses prove that the actual flattened Index is located in
# the nominal Colophon split and that unrelated columns share physical lines.
INDEX_FLATTENING_SENTINELS = {
    21050: ("Corollaries",),
    21114: ("Dynamic programming",),
    21416: ("Karnaugh maps",),
    21779: ("computation of nth digits in, 912",),
    21793: ("Pluperfect numbers",),
    21891: ("Radicals continued fractions for, 144",),
    22110: ("Shallit, Jeffrey O.",),
    22352: ("Transmutation, in alchemy",),
}


IMAGE_RE = re.compile(r"^!\[[^\]]*\]\(([^)]+)\)$")
NATIVE_IMAGE_LINES = line_set(
    "1677,1711,1744,12960,13040,13042,13044,13046,13048,13050,13090"
)
RELATION_IMAGE_LINES = line_set(
    "12992,12996,13000,13020,13076,13094,13098,13119,13121,13123,13125,13127"
)
CONTROL_IMAGE_LINES = line_set("13134")
GOVERNED_IMAGE_LINES = (
    NATIVE_IMAGE_LINES | RELATION_IMAGE_LINES | CONTROL_IMAGE_LINES
)
EXCLUDED_IMAGE_LINES = frozenset()
CANDIDATE_IMAGE_LINES = GOVERNED_IMAGE_LINES
UNRESOLVED_IMAGE_LINES = frozenset()

IMAGE_ROLE_RECORDS = (
    "1677:native:page151 pi base-two walk observer",
    "1711:native:page154 rational long-division work panels",
    "1744:native:page156 square-root product-state work panels",
    "12960:native:page927 rational digit panels",
    "12992:relation:page928 concatenation digits",
    "12996:relation:page928 concatenation walk",
    "13000:relation:page928 leading-bit-dropped concatenation walk",
    "13020:relation:page928 Gray-code concatenation",
    "13040:native:page929 continued-fraction residual panel a",
    "13042:native:page929 continued-fraction residual panel b",
    "13044:native:page929 continued-fraction residual panel c",
    "13046:native:page929 continued-fraction residual panel d",
    "13048:native:page929 continued-fraction residual panel e",
    "13050:native:page929 continued-fraction residual panel f",
    "13076:relation:page930 concatenation continued-fraction term sizes",
    "13090:native:page930 rational-approximation quality observer",
    "13094:relation:page930 Euclidean algorithm integers",
    "13098:relation:page930 Euclidean algorithm real",
    "13119:relation:page931 digital-slope panel a",
    "13121:relation:page931 digital-slope panel b",
    "13123:relation:page931 digital-slope panel c",
    "13125:relation:page931 digital-slope panel d",
    "13127:relation:page931 digital-slope panel e",
    "13134:control:page931 operator-representation boundary",
)
IMAGE_ASSEMBLY_BOUNDARIES = (
    "page928:12992,12996,13000 form the concatenation-walk trilogy",
    "page929:13040,13042,13044,13046,13048,13050 form six residual panels",
    "page930:13094,13098 form the Euclidean-algorithm relation pair",
    "page931:13119,13121,13123,13125,13127 form five digital-slope panels",
    "main:1711 and 1744 have physical files but no split Markdown references",
    "paths:monolith references omit Images while split references include it",
    "boundary:all 24 assets are hash-bound and supply no pixel-derived mechanics",
)


# Exact textual claims.  Negative needles make a silent editorial repair fail.
SOURCE_SEMANTIC_GUARDS = (
    ("heading", 1665, ("Mathematical Constants",), ("Mathematical Functions",)),
    ("definition_vs_digits", 1673, ("simple definition", "circumference", "diameter"), ()),
    ("two_bases", 1675, ("first 4000 digits", "base 10", "base 2"), ()),
    ("walk_observer", 1679, ("curve drawn goes up", "digit is 1", "every time it is 0"), ()),
    ("terminating_zero_tail", 1689, ("0.3750000000", "normally suppressed"), ()),
    ("rational_period", 1707, ("number of the form p/q", "period of at most q-1"), ()),
    ("long_division", 1715, ("standard long division", "compares the values of 2r and q", "2r - q"), ("callback",)),
    ("sqrt_product_rule", 1740, ("two numbers r and s", "4(r-s-1)", "2(s+2)"), ()),
    ("sqrt_caption", 1746, ("setting r=n and s=0", "digits of s in base 2"), ()),
    ("representation_as_procedure", 1778, ("representation for a number", "procedure for constructing"), ()),
    ("continued_fraction_operations", 1786, ("continued fraction representations", "addition and division"), ()),
    ("continued_fraction_completion", 1794, ("rational numbers", "limited length", "go on forever"), ()),
    ("symbolic_evaluation_cost", 1796, ("symbolic expressions", "difficult", "actual value"), ()),
    ("representation_conclusion", 1832, ("intrinsic sense complex", "particular representation"), ()),
    ("direct_nth", 12943, ("without explicitly finding previous ones", "overwhelming probability"), ("certainly exact",)),
    ("finite_precision_probability", 12951, ("finite-precision arithmetic", "probability exists", "incorrect results"), ()),
    ("normality_base", 12976, ('normal" in a particular base', "does not imply anything"), ()),
    ("sqrt_invariant_claim", 12982, ("s^2 + 4r = 4^t n", "any rational number", "1 \\le n < 4"), ()),
    ("continued_fraction_query", 13030, ("first n terms", "ContinuedFraction"), ()),
    ("continued_fraction_iteration", 13032, ("Floor[NestList[1/Mod[#, 1] &, x, n-1]]",), ()),
    ("continued_fraction_inverse", 13034, ("reconstructed", "FromContinuedFraction"), ()),
    ("unbounded_coefficients", 13052, ("terms in a continued fraction can be of any size",), ()),
    ("substitution_relation", 13062, ("nested structure", "substitution system"), ()),
    ("approximation_observer", 13088, ("closeness of successive rational approximations",), ()),
    ("euclid_relation", 13092, ("Euclid's algorithm", "ContinuedFraction[a/b]"), ()),
    ("digital_slope_relation", 13111, ("Digital slope representation", "Floor[nh] - Floor[(n-1)h]"), ()),
    ("number_classification", 13136, ("Number classification", "undecidable", "same number"), ()),
    ("noncomputable_definition", 17101, ("formal descriptions", "algorithmically random", "Chaitin"), ()),
    ("noncomputable_coefficients", 19058, ("nth digit", "far from being computable", "halting problem"), ()),
    ("left_boundary", 1619, ("The Sequence of Primes",), ("Mathematical Constants",)),
    ("right_boundary", 1834, ("Mathematical Functions",), ("Mathematical Constants",)),
    ("notes_left_boundary", 12846, ("The Sequence of Primes",), ()),
    ("notes_right_boundary", 13146, ("Mathematical Functions",), ()),
    ("sqrt_extracted_bits", 1733, ("1.01101010000010011110011001100110111111",), ()),
    ("sqrt_duplicated_extraction", 1740, ("base s digits of s digits of s",), ()),
    ("gamma_duplication", 12974, ("Gamma[1/3] and Gamma[1/3]",), ()),
    ("truncated_randomly", 13084, ("continued fraction representation for a randomly",), ("chosen number",)),
)
SOURCE_SEMANTIC_GUARD_RECORDS = frozenset(
    f"{kind}:{line_no}:{'|'.join(positive)}!{'|'.join(negative)}"
    for kind, line_no, positive, negative in SOURCE_SEMANTIC_GUARDS
)

AUXILIARY_SEMANTIC_GUARDS = (
    ("catalog", 41, ("Mathematical-Constant Digit Systems,",), ()),
    ("taxonomy", 1103, ("## 40. Mathematical-Constant Digit Systems",), ()),
    ("taxonomy", 1107, ("exact mathematical constant or expression",), ()),
    ("taxonomy", 1120, ("no stepwise dynamical update",), ()),
    ("taxonomy", 1126, ("constant", "exact expression or named constant"), ()),
    ("taxonomy", 1129, ("term_count", "number of terms or digits"), ()),
    ("atlas", 141, ("Mathematical Constants",), ()),
    ("atlas", 143, ("simple mathematical definitions", "effectively random"), ()),
)

SOURCE_DEFECT_RECORDS = (
    "BOOK1681:caption promises 4000 decimal digits but extraction contains only a prefix",
    "BOOK1683:caption promises 4000 binary digits but extraction is short and has extra separators",
    "BOOK1733:extracted sqrt-two binary row agrees for 32 zero-based bits then diverges from exact isqrt replay",
    "BOOK1740:square-root prose is duplicated and truncated at base-s phrase",
    "BOOK1746:printed If expression uses malformed brace syntax",
    "BOOK1750->1774:sentence is interrupted by page extraction and resumes later",
    "BOOK1782:base-two nested construction is runaway and truncated",
    "BOOK1798->1830:sentence is interrupted by table extraction and resumes later",
    "BOOK1821:e-squared label is corrupted to a euro glyph",
    "BOOK12935:missing newline joins two pi algorithms",
    "BOOK12946-12948:direct-digit code is split by an empty extraction row",
    "BOOK12954:formula contains HTML superscript markup",
    "BOOK12968-12970:rational-period clause is duplicated and first copy incomplete",
    "BOOK12974:Gamma-one-third is duplicated; no second quantity may be invented",
    "BOOK12982:arbitrary-rational square-root claim is false for literal r-greater-than-s rule at n=11/5",
    "BOOK13002:concatenation sentence is incomplete and contains digit-bydigit typo",
    "BOOK13064-13068:substitution code is truncated",
    "BOOK13070->13072:continued-fraction sentence is split across extraction rows",
    "BOOK13084:sentence ends at randomly and has no extracted completion",
    "BOOK13103->13105:nested-radical sentence is split across extraction rows",
    "split-main:chapter file is an abridged summary and omits long-division and square-root mechanics",
    "image-paths:monolith omits Images directory while split corpus includes it",
    "split-routing:nominal BACK-MATTER/Index contains Notes rather than the actual flattened Index",
    "split-routing:actual flattened Index rows are stored in BACK-MATTER/Colophon",
)
SOURCE_DEFECT_GUARD_RECORDS = frozenset(SOURCE_DEFECT_RECORDS)

SOURCE_MODEL_RECORDS = (
    "category:immutable exact denotation plus typed pure representation query",
    "native-transition:no canonical configuration frontier neighborhood rule or update",
    "definition:closed exact arity-zero expression with primitive registry and provenance",
    "representation:tagged positional or simple-continued-fraction schema",
    "query:prefix count or coefficient-at index is scope not mutable state",
    "result:exact certified approximate probable completion unsupported unknown resource or failure",
    "positional:base at least two and digit coefficients bounded by base",
    "positional-canonical:terminating rational uses infinite zero tail not eventual base-minus-one tail",
    "continued-fraction:integer coefficients are unbounded",
    "continued-fraction-canonical:finite tail has final coefficient greater than one when length exceeds one",
    "finite-prefix:lossy query result and never the complete exact value",
    "rendering:digit row walk histogram and coefficient plots are observers",
    "work-long-division:explicit discrete t-plus-0D exact remainder configuration",
    "work-long-division:Self read closed quotient-remainder rule atomic same-locus assignment",
    "work-square-root:explicit discrete t-plus-0D Product-r-s configuration",
    "work-square-root:both product components update atomically from one old snapshot",
    "work-square-root:literal source profile is integer-safe; rational repair is a sibling",
    "work-continued-fraction:explicit exact scalar fractional-reciprocal iteration with finite completion",
    "direct-access:nth coefficient evaluator need not fabricate preceding append events",
    "computability:exact definition alone does not guarantee executable coefficient access",
    "source-strength:finite-precision overwhelming probability is not exact certification",
    "architecture:no ConstantDigitsState T40 update executor runner branch family dispatch or callback",
    "architecture:optional work algorithms reuse existing SimplePrograms axes and branch-free runner",
    "architecture:no hidden remainder residual prefix cache precision state or CAS object",
    "relation:realization certificate connects a work trace to a denotation query",
    "boundary:T36 supplies positional codecs without importing its transition identity",
    "boundary:T37 append state is not universal because direct nth access exists",
    "boundary:T41 supplies immutable closed-definition and query responsibilities",
    "boundary:T42 consumes coefficients but owns substitution evolution",
    "boundary:T43 scalar feedback maps can realize positional and continued-fraction queries",
    "domain-vocabulary:DOMAIN means t plus dimensional task support not CA family",
    "source-epistemic:catalog taxonomy and atlas supply vocabulary rather than primary mechanics",
)


# The clean Chapter 4 split is intentionally abridged.  Exact/normalized
# owners, explicit summaries, and explicit omissions are separate modes.
SPLIT_MAIN_DIRECT_OWNERS = {
    **{
        n: (
            "CHAPTERS/4-Systems-Based-on-Numbers/"
            f"Systems-Based-on-Numbers.md:{n - 1418}"
        )
        for n in range(1663, 1692, 2)
    },
    1619: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:201",
    1834: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:293",
    1850: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:309",
    1852: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:311",
    1856: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:315",
}
SPLIT_MAIN_SUMMARY_OWNERS = {
    1693: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:277",
    1695: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:277",
    1696: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:277",
    1697: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:277",
    1698: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:277",
    1700: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:278",
    1701: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:278",
    1823: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:282",
    1824: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:283",
    1825: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:284",
    1826: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:285",
    1828: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:287",
    1830: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:289",
    1832: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:291",
}
SPLIT_OMISSION_GROUPS = {
    "abridged-repeating-digit-table": line_set("1702-1704"),
    "rational-and-long-division-mechanics": line_set(
        "1707,1709,1711,1713,1715,1717,1719"
    ),
    "square-root-and-higher-root-data-tables": line_set(
        "1721,1723-1729,1754,1756-1770"
    ),
    "square-root-and-positional-mechanics": line_set(
        "1733,1736,1738,1740,1742,1744,1746,1748,1750,1772,1774"
    ),
    "representation-and-continued-fraction-mechanics": line_set(
        "1776,1778,1780,1782,1784,1786,1789,1792,1794,1796,1798"
    ),
    "abridged-continued-fraction-data-table": line_set("1804,1806-1822"),
    "strict-structural-extraction-rows": STRICT_MAIN_STRUCTURAL,
}
SPLIT_OMISSION_LINES = frozenset().union(*SPLIT_OMISSION_GROUPS.values())
SPLIT_BOUNDARY_WITNESSES = (
    "main-left:BOOK1663->CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:245",
    "main-first:BOOK1665->CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:247",
    "main-summary:BOOK1828->CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:287",
    "main-right:BOOK1834->CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:293",
    "notes-first:BOOK12921->BACK-MATTER/Index/Index.md:824",
    "notes-right:BOOK13146->BACK-MATTER/Index/Index.md:1049",
    "actual-index-first:BOOK20828->BACK-MATTER/Colophon/Colophon.md:3385",
)


# Frozen expectations follow their independently readable records above.
EXPECTED_QUERY = {
    "Q00": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q01": (5, 4, 1, "51039fbadd85a4f95f0ea91871a10142216e19412fbdf4bc5cf049614befb91b"),
    "Q02": (5, 5, 0, "ce913f4b8301f1e04917916df893d9dbfb7e720ca7129525030c14b66957b75a"),
    "Q03": (3, 3, 0, "6ce776ad724dc65726ef90211965a1454a033809dee578ecc1685bd8c9d92bcc"),
    "Q04": (4, 4, 0, "e4651f7d50217f898c5d83ca64799f93d312e6b481f99967d68d41d092fd3fb0"),
    "Q05": (4, 4, 0, "5b0e2fd166aa3184dfb0b6f4d02bb156168a4b0950ae2a6cb060d938c3dcd237"),
    "Q06": (14, 14, 0, "afccf448b8f881a1529546fcb634e850ecd954aa9aacbb8bb79e90766c6dcabc"),
    "Q07": (4, 4, 0, "2bf68dda703268006c7634a33cc21e7c836cf5f66fde1dc1987ed4bc6a5cb076"),
    "Q08": (3, 2, 1, "4eea9f92991dee3a43ba186da7280a69bfaceffccde6ec4c12d215d5ee3f1951"),
    "Q09": (34, 14, 20, "b9b9e01d30fc7b89eb7e845a1753c8aa2bed6f791a1ce6deff7a58b52c0790d1"),
    "Q10": (6, 4, 2, "d3951c5d658e62018a2c4cca367c16401025d13d792c3603f45fdeedee6f9d17"),
    "Q11": (23, 12, 11, "a1c38c2e18294e7f54c19022087466d05cb13a1530c4ba5c003108023fb3d514"),
    "Q12": (9, 5, 4, "c64a5b61c066aba945485b199125e1b0732aa5ec8e935a25e28b912c3734f285"),
    "Q13": (2, 2, 0, "6a8ea11b4ec5fdca405e59703e8853736502a0daffd3cd153c166cead6e74577"),
    "Q14": (12, 0, 12, "7b99c1393251c1d6e507801a46576a77d9b33a78557f42bd2e29ffc26c5ff277"),
    "Q15": (3, 3, 0, "29e023f7db02bec1f2a16113a10f2ad22d45f9741ac3563d630c38b4ae641240"),
    "Q16": (21, 21, 0, "2780612ef55f979f24f756be9a8532494bb13c4ecb6029715a649a89ba1274c4"),
    "Q17": (4, 4, 0, "8a4e0a5a0bdb3f5e00e29d2c34e66980cec3634c02ac67dbee9b0c5d2bc8c8fd"),
}
EXPECTED_QUERY_PATTERNS = (
    18,
    "8e2ca87c4588620a2f8d67128cb85ec633822fd3e1bde143bba74be8abadd7a9",
)
EXPECTED_SET = {
    "union": (144, "6dabdf0a8cb82dc2344bf3e0feed786a105af6cdbf6d182ff5d4c4eafd69c935"),
    "pre_index": (99, "39e469b9638ca0458a66f3e312e7bcaac5d61e5d6501b8781fd1d4ce1eb5e303"),
    "index_candidates": (45, "a352580c74fff6a60081acceaed2937c024e89c9cec5948b002f7c70504f79ba"),
    "query_native": (46, "90c5667940c7b23109fec16cce632cd493d64aa5bf3c6eeda290417cee80093d"),
    "query_relation": (41, "aaa1d5ac0262e3910c7d48c3428d1550dbaa488888807ad83b38f64e865b9f88"),
    "query_control": (7, "aa826f1310f068dd0ba264d1a4155fcd46ae2fe1f318c5dd5e159ac7eef21c2e"),
    "excluded": (5, "01c97a261db7b3a9cc557d83e011e5aa7a280433144e5df6d2b22bedd051f8f8"),
    "native": (169, "eba1f729ab1ed14b6809c181e74ac86b64a363c0bcecb684f7cdbdad8f76ca2b"),
    "relation": (84, "5a092550392b0923fe58837ef403cf294d8e8de6fe92d976117a44bdf5e618cd"),
    "control": (9, "350e9aec3d0ce5466da723cf905a398bcb183fcafee5963145a2e8d8149a564e"),
    "retained": (262, "0d7320af1896c9c5d27547dea20e8fb231f0f1f43a759158b98ca08c5e70cb86"),
    "retained_query": (94, "165209df95c945a005adeb119f6282d55c64b89f663beecee826dc08f7eecb52"),
    "continuations": (168, "f24f83df5825469c5512ab94efbe6a264731bd44fd1ef820449f76eaa70beb09"),
}
EXPECTED_EXCLUDED_CLASS = {
    "name_collision": (1, "0a5b046d07f6f971b7776de682f57c5b9cdc8fa060db7ef59de82e721c8098f4"),
    "unrelated_representation_context": (1, "45113af9c39c6636107b96fcdc1037686173b60eec2b3f4561b2d7d7b6c1252f"),
    "generic_algorithm_cross_reference": (3, "0af5fb1f1971b936e8052cc34fe7605caf6f6916a28992ff9485914a39d55704"),
}
EXPECTED_INDEX_CLASS = {
    "native": (25, "46e883d59f112ae1427bfd09299e7f457c5a2328d0f9326ebbc62421220cd3b3"),
    "relation": (56, "3d107040293822a0baf0c3be1a0f5aad69262921910f7c1b90a8824135ac0931"),
    "control": (1, "2754f6e1f004d4298d7ed6444c52385d98a70aee827877053ef7d43e519ac10f"),
}
EXPECTED_INDEX_RELEVANT_UNIVERSE = (
    82,
    "5e23e53aff0b8ea8b53ba588e44496d31ea600b8ebde0c5e36a8183b1eedae3d",
)
EXPECTED_INDEX_QUERY_MISSES = (
    37,
    "6aa6edc52301504475891b295fd59cd706295e90f9c2503d5ccdb22f629ae3f9",
)
EXPECTED_STRICT_MAIN_PARTITION = {
    "native": (102, "bd76954762c925f2ecf6bf0fa97d9c15db19d598a297a9c56d74e12d1dc41d59"),
    "relation": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "control": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "excluded": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "structural": (15, "8b83af3e32debd18eab8f148b46b187ff2ca50001b037a5d5cd71f81989c5e54"),
    "content": (117, "6c39a18a84e5186f11f8082c2bc5380846269c7f67b62d759b9fea0bea0ea2a9"),
}
EXPECTED_IMAGE_PARTITION = {
    "native": (11, "45fe870caa33fa2cc0b702a8158564f987fb186a1742f1bbafc940cf8c738894"),
    "relation": (12, "1733851c97444c9a966ea16d19b86a37310e23f393ee8ba1f8089e3a522c49a2"),
    "control": (1, "71887428c764ac67b3bd6ce9f4212ff7e7fe6803e507b5b11345d7c6a6c95a1e"),
    "governed": (24, "2dcad870ac6f500bf924a74b60c04093ae591911c688ef4f3bfb81b8130103ca"),
    "excluded": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "candidate": (24, "2dcad870ac6f500bf924a74b60c04093ae591911c688ef4f3bfb81b8130103ca"),
}
EXPECTED_IMAGE_ROLE_PARTITION = {
    "native": EXPECTED_IMAGE_PARTITION["native"],
    "relation": EXPECTED_IMAGE_PARTITION["relation"],
    "control": EXPECTED_IMAGE_PARTITION["control"],
}
EXPECTED_IMAGE_LEDGER = {
    "candidate_images": EXPECTED_IMAGE_PARTITION["candidate"],
    "governed_images": EXPECTED_IMAGE_PARTITION["governed"],
    "excluded_images": EXPECTED_IMAGE_PARTITION["excluded"],
}
EXPECTED_CANDIDATE_IMAGE_LINES = EXPECTED_IMAGE_PARTITION["candidate"]
EXPECTED_GOVERNED_IMAGE_LINES = EXPECTED_IMAGE_PARTITION["governed"]
EXPECTED_EXCLUDED_IMAGE_LINES = EXPECTED_IMAGE_PARTITION["excluded"]
EXPECTED_UNRESOLVED_IMAGE_LINES = (
    0,
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
)
EXPECTED_IMAGE_ASSET_MANIFEST = (
    24,
    "1cbfe8ffc3de77048a2d407c7ef63896dac86a8fc3ec83c7b00c1ea84e6f019e",
)
EXPECTED_SOURCE_SEMANTIC_GUARDS = (
    37,
    "7c09ef685b2770dc98b0b5d7b1ac8b6c8cb347ad8a5cd939e19af6d4663c8f74",
)
EXPECTED_SOURCE_DEFECT_GUARDS = (
    24,
    "833c24e7f3c44bc2737a48dc6cbc4a3cb02caf3cfc1d62d372b9ce42973753b2",
)
EXPECTED_RECORDS = {
    "excluded_line_hashes": (5, "d3b3134fe2e22ca121f65e3617dce002e45e1880600c264b4c5a100d9614efef"),
    "index_guards": (82, "8b5c9ce6a3cc644d42fc142e8f78e2b33f964671a9afb7883289fb8e7e33edfc"),
    "index_sentinels": (8, "129bc6a4ef7cc76b5020676e603a2b5621ef56354b8ca2cd2fb4361938791710"),
    "strict_main_dispositions": (117, "94bed33e54122c19903a478a562a10d69491890aef04978d417bb53b3b13db91"),
    "semantic_guards": EXPECTED_SOURCE_SEMANTIC_GUARDS,
    "auxiliary_guards": (8, "bb1c06175c4a5856879b75936917159d7125f734ad6350cc26f618cb2da23b18"),
    "source_defects": EXPECTED_SOURCE_DEFECT_GUARDS,
    "source_model": (32, "8ba5c526bd482ac86447e79c616bd3da5f678cc0c60fe4943a01d70cc71e6be0"),
    "image_roles": (24, "9f4b951e3444c26c6a256ef3461ec3132175efb2601f3b89c3073cb6d9f9689f"),
    "image_assembly_boundaries": (7, "60395054223bb245396b3936dda4349e63a68a6b6306efaf34c5f4484e51132b"),
    "split_omissions": (89, "0c3dc82ba4879e60782fa0459e4e12768e8e48f4b950474bdc731f382fab6c8f"),
    "split_boundary_witnesses": (7, "c32f23773dbe2707c96bde64ea3fd95445e3ff6efd2bb809718c22d28b9a9884"),
}
EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
EXPECTED_SPLIT_MANIFEST_DIGEST = "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"
EXPECTED_SPLIT_CROSSWALK = (
    359,
    "66f52a83007eb6c0a3fbf52165b07d1929b63a0ccc42c6512ba27a8874e81081",
)
EXPECTED_SPLIT_CLASSES = {
    "EXACT": (
        214,
        "7629cc72e9648e45f6b978aede0942792336e0d2d1ce715ae5586b988734f887",
        "6a65aabc68562dfb756654af3e0700ec1418f5f05342078bafd6855080d9bc0b",
    ),
    "IMAGE_BASENAME": (
        22,
        "f1c7069e4d51217045092da88b101b8c34b9c6d60af4080ce6e64d870245e061",
        "0b8db2d77d1426451dbdebffda4c817e79cbd2aa136773144314bf6a0ba1f56f",
    ),
    "NORMALIZED": (
        20,
        "8053cc358d079fdb7d26b173a13293be9795b12b09661319d1d6a7ce0914a80b",
        "7e405c6235eb29bfda60f31c47cc13fe670cf76a40d5e73dcdcabd111a231936",
    ),
    "SUMMARY": (
        14,
        "8ef33877220036f2939337015de6307a13ddb1a8a28f735d274e4be07239cd1e",
        "9d4863d9a7a0c61fda8f26e054e0a9ea3a1912dd9d9b8c9a79cd8b0afe5a100f",
    ),
    "OMITTED": (
        89,
        "a2e7ef27e19c1dd7ca657f20b806754966e3a6d396a2dcbf864aa2a491d399b1",
        "0251161e7ee25fcf11bab72f0f7a389ac4bed5b2daceefb63a78b541b1e60748",
    ),
}
EXPECTED_SPLIT_NORMALIZED_MINIMUM = 0.999817
EXPECTED_LOGIC_RECORDS = (
    7,
    "d525310251895f506ca06d964ba736dd53ab659e07fed14d7fbe5422b1648754",
)
EXPECTED_AUDIT_DIGEST = "a06531ed8bfcaf4a926ad4db4bc6eb32b2a2e77ed3171ee5f9be9e3c145f166e"


IMAGE_PARTITION = {
    "native": NATIVE_IMAGE_LINES,
    "relation": RELATION_IMAGE_LINES,
    "control": CONTROL_IMAGE_LINES,
}
IMAGE_LEDGER = {
    "candidate_images": CANDIDATE_IMAGE_LINES,
    "governed_images": GOVERNED_IMAGE_LINES,
    "excluded_images": EXCLUDED_IMAGE_LINES,
}


def normalized_line(line: str) -> str:
    text = unicodedata.normalize("NFKD", line).lower().replace("\\", "")
    return " ".join(re.findall(r"[a-z0-9]+", text))


def compact_line(line: str) -> str:
    return normalized_line(line).replace(" ", "")


def crosswalk_evidence(monolith: str, split: str) -> tuple[str, float]:
    if monolith == split:
        return "EXACT", 1.0
    left = IMAGE_RE.fullmatch(monolith.strip())
    right = IMAGE_RE.fullmatch(split.strip())
    if left and right:
        same = Path(left.group(1)).name == Path(right.group(1)).name
        return "IMAGE_BASENAME", 1.0 if same else 0.0
    score = SequenceMatcher(
        None, compact_line(monolith), compact_line(split), autojunk=False
    ).ratio()
    return "NORMALIZED", score


def split_owner_record(line_no: int) -> str:
    if line_no in SPLIT_MAIN_DIRECT_OWNERS:
        return SPLIT_MAIN_DIRECT_OWNERS[line_no]
    if line_no in SPLIT_MAIN_SUMMARY_OWNERS:
        return SPLIT_MAIN_SUMMARY_OWNERS[line_no]
    if 12919 <= line_no <= 13146:
        return f"BACK-MATTER/Index/Index.md:{line_no - 12097}"
    if line_no in {14172, 14468, 14923, 17101, 17236}:
        return f"BACK-MATTER/Index/Index.md:{line_no - 12099}"
    if line_no in {17599, 19058, 20592} or line_no >= INDEX_FIRST_LINE:
        return f"BACK-MATTER/Colophon/Colophon.md:{line_no - 17443}"
    chapter_12 = {11260: 2641, 11531: 2912}
    if line_no in chapter_12:
        return (
            "CHAPTERS/12-The-Principle-of-Computational-Equivalence/"
            "The-Principle-of-Computational-Equivalence.md:"
            f"{chapter_12[line_no]}"
        )
    if line_no == 12569:
        return "BACK-MATTER/Index/Index.md:472"
    if line_no == 12846:
        return "BACK-MATTER/Index/Index.md:749"
    raise ValueError(f"line {line_no} has no frozen split disposition")


def occurrence_records(
    guards: dict[int, tuple[str, ...]], lines: list[str]
) -> tuple[set[str], bool]:
    records = {f"{line_no}:{'|'.join(needles)}" for line_no, needles in guards.items()}
    valid = all(
        needles
        and all(needles)
        and 1 <= line_no <= len(lines)
        and all(needle in lines[line_no - 1] for needle in needles)
        for line_no, needles in guards.items()
    )
    return records, valid


def digest_framed_records(records: set[str]) -> str:
    payload = bytearray()
    for record in sorted(records):
        encoded = record.encode("utf-8")
        payload.extend(len(encoded).to_bytes(8, "big"))
        payload.extend(encoded)
    return hashlib.sha256(payload).hexdigest()


def long_division_step(r: int, q: int) -> tuple[int, int]:
    if type(r) is not int or type(q) is not int or q <= 0 or not 0 <= r < q:
        raise ValueError("long division requires exact integers with 0 <= r < q")
    doubled = 2 * r
    digit = int(doubled >= q)
    successor = doubled - digit * q
    assert digit in {0, 1} and 0 <= successor < q
    assert doubled == digit * q + successor
    return digit, successor


def positional_digits(value: Fraction, base: int, count: int) -> tuple[int, ...]:
    if not 0 <= value < 1 or base < 2 or count < 0:
        raise ValueError("invalid positional query")
    residual = value
    result: list[int] = []
    for _ in range(count):
        scaled = residual * base
        digit = scaled.numerator // scaled.denominator
        residual = scaled - digit
        assert 0 <= digit < base and 0 <= residual < 1
        result.append(digit)
    return tuple(result)


def continued_fraction(value: Fraction) -> tuple[int, ...]:
    coefficients: list[int] = []
    current = value
    while True:
        coefficient = current.numerator // current.denominator
        coefficients.append(coefficient)
        residual = current - coefficient
        if residual == 0:
            break
        current = 1 / residual
    return tuple(coefficients)


def sqrt_integer_step(r: int, s: int) -> tuple[int, int, int]:
    if type(r) is not int or type(s) is not int or r < 0 or s < 0 or s % 4:
        raise ValueError("strict square-root work state requires nonnegative integers")
    bit = int(r > s)
    if bit:
        successor = (4 * (r - s - 1), 2 * (s + 2))
    else:
        successor = (4 * r, 2 * s)
    next_r, next_s = successor
    assert next_r >= 0 and next_s >= 0 and next_s % 4 == 0
    assert next_s // 4 == 2 * (s // 4) + bit
    return bit, next_r, next_s


def sqrt_integer_bits(n: int, count: int) -> str:
    if type(n) is not int or not 1 <= n < 4 or count < 0:
        raise ValueError("strict source profile requires integer 1 <= n < 4")
    r, s = n, 0
    bits: list[str] = []
    for event in range(count):
        assert s * s + 4 * r == 4 ** (event + 1) * n
        assert s * s <= 4 ** (event + 1) * n < (s + 4) ** 2
        bit, r, s = sqrt_integer_step(r, s)
        bits.append(str(bit))
        assert s // 4 == math.isqrt(n * 4**event)
    return "".join(bits)


def logic_records() -> set[str]:
    long_checks = 0
    for q in range(2, 65):
        for r in range(q):
            long_division_step(r, q)
            long_checks += 1
    assert positional_digits(Fraction(1, 3), 2, 4) == (0, 1, 0, 1)
    assert positional_digits(Fraction(5, 16), 2, 4) == (0, 1, 0, 1)
    assert Fraction(1, 3) != Fraction(5, 16)
    assert continued_fraction(Fraction(7, 11)) == (0, 1, 1, 1, 3)
    assert continued_fraction(Fraction(3, 8)) == (0, 2, 1, 2)

    sqrt2 = sqrt_integer_bits(2, 48)
    sqrt3 = sqrt_integer_bits(3, 48)
    assert sqrt2 == "101101010000010011110011001100111111100111011110"
    assert sqrt3 == "110111011011001111010111010000101100001001100101"
    extracted = "101101010000010011110011001100110111111"
    mismatches = [
        index for index, pair in enumerate(zip(extracted, sqrt2)) if pair[0] != pair[1]
    ]
    assert mismatches and mismatches[0] == 32

    r0, s0 = Fraction(11, 5), Fraction(0)
    r1, s1 = 4 * (r0 - s0 - 1), 2 * (s0 + 2)
    r2, s2 = 4 * (r1 - s1 - 1), 2 * (s1 + 2)
    assert (r1, s1) == (Fraction(24, 5), Fraction(4))
    assert (r2, s2) == (Fraction(-4, 5), Fraction(12))
    assert r1 > s1 and not r1 >= s1 + 1
    assert (4 * r1, 2 * s1) == (Fraction(96, 5), Fraction(8))

    return {
        f"long-division:states={long_checks}:q=2..64",
        "positional-prefix-collision:1/3!=5/16:base2-prefix=0101",
        "continued-fraction:7/11=0,1,1,1,3:3/8=0,2,1,2",
        f"sqrt-integer:two-profiles:events={len(sqrt2) + len(sqrt3)}",
        f"sqrt2-extraction:first-mismatch-zero-based={mismatches[0]}:mismatches={len(mismatches)}",
        "sqrt-rational-defect:11/5:(11/5,0)->(24/5,4)->(-4/5,12)",
        "sqrt-rational-repair-sibling:threshold=r>=s+1:second=(96/5,8)",
    }


def parse_args(args: list[str]) -> tuple[bool, str | None]:
    json_mode = False
    positional: list[str] = []
    for argument in args:
        if argument == "--json":
            if json_mode:
                raise SystemExit("usage: 45-T40-source-oracle.py [--json] [BOOK]")
            json_mode = True
        elif argument.startswith("-"):
            raise SystemExit("usage: 45-T40-source-oracle.py [--json] [BOOK]")
        else:
            positional.append(argument)
    if len(positional) > 1:
        raise SystemExit("usage: 45-T40-source-oracle.py [--json] [BOOK]")
    return json_mode, positional[0] if positional else None


def main(argv: list[str] | None = None) -> int:
    json_mode, argument = parse_args(sys.argv[1:] if argv is None else argv)
    book, source_root, repo_root = resolve_book(argument)
    atlas = source_root / "ANKoS-Atlas.md"
    catalog = repo_root / "ref/notes/CA-Types.csv"
    taxonomy = repo_root / "ref/notes/CA-Types.md"

    raw = book.read_bytes()
    lines = raw.decode("utf-8").splitlines()
    at = lambda n: lines[n - 1]
    source_ok = (
        len(lines) == EXPECTED_BOOK_LINES
        and hashlib.sha256(raw).hexdigest() == EXPECTED_BOOK_SHA256
        and sha256(atlas) == EXPECTED_ATLAS_SHA256
        and sha256(catalog) == EXPECTED_CATALOG_SHA256
        and sha256(taxonomy) == EXPECTED_TAXONOMY_SHA256
    )
    ok = source_ok
    output: list[tuple[str, bool, tuple[object, ...]]] = []

    def check(name: str, good: bool, *metrics: object) -> None:
        nonlocal ok
        ok &= good
        output.append((name, good, metrics))

    check("source", source_ok, len(lines), hashlib.sha256(raw).hexdigest())

    pattern_records = {f"{name}:{pattern}" for name, pattern in QUERIES.items()}
    pattern_actual = (len(pattern_records), digest_records(pattern_records))
    query_contract_ok = (
        set(QUERIES) == set(EXPECTED_QUERY)
        and all(QUERIES.values())
        and pattern_actual == EXPECTED_QUERY_PATTERNS
    )
    check("query_contract", query_contract_ok, *pattern_actual)

    hits: dict[str, set[int]] = {}
    for name, pattern in QUERIES.items():
        found = {
            number
            for number, line in enumerate(lines, 1)
            if re.search(pattern, line, re.IGNORECASE)
        }
        hits[name] = found
        actual = (
            len(found),
            sum(number < INDEX_FIRST_LINE for number in found),
            sum(number >= INDEX_FIRST_LINE for number in found),
            digest(found),
        )
        check(name, actual == EXPECTED_QUERY.get(name), *actual)

    union = set().union(*hits.values())
    pre_index = {number for number in union if number < INDEX_FIRST_LINE}
    index_candidates = union - pre_index
    query_retained = set(QUERY_NATIVE | QUERY_RELATION | QUERY_CONTROL)
    sets = {
        "union": union,
        "pre_index": pre_index,
        "index_candidates": index_candidates,
        "query_native": set(QUERY_NATIVE),
        "query_relation": set(QUERY_RELATION),
        "query_control": set(QUERY_CONTROL),
        "excluded": set(EXCLUDED),
        "native": set(NATIVE_EVIDENCE),
        "relation": set(RELATION_EVIDENCE),
        "control": set(CONTROL_EVIDENCE),
        "retained": set(RETAINED),
        "retained_query": query_retained,
        "continuations": set(RETAINED) - query_retained,
    }
    set_contract_ok = set(sets) == set(EXPECTED_SET)
    for name, values in sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_SET.get(name)
        set_contract_ok &= good
        check("set_" + name, good, *actual)

    query_partition = (QUERY_NATIVE, QUERY_RELATION, QUERY_CONTROL, EXCLUDED)
    classification_ok = (
        set().union(*query_partition) == pre_index
        and sum(map(len, query_partition)) == len(pre_index)
        and QUERY_NATIVE <= NATIVE_EVIDENCE
        and QUERY_RELATION <= RELATION_EVIDENCE
        and QUERY_CONTROL <= CONTROL_EVIDENCE
        and not NATIVE_EVIDENCE & RELATION_EVIDENCE
        and not NATIVE_EVIDENCE & CONTROL_EVIDENCE
        and not RELATION_EVIDENCE & CONTROL_EVIDENCE
        and not RETAINED & EXCLUDED
    )
    for name, values in EXCLUDED_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_EXCLUDED_CLASS.get(name)
        classification_ok &= good
        check("excluded_" + name, good, *actual)
    classification_ok &= (
        set(EXCLUDED_CLASS) == set(EXPECTED_EXCLUDED_CLASS)
        and frozenset().union(*EXCLUDED_CLASS.values()) == EXCLUDED
        and sum(map(len, EXCLUDED_CLASS.values())) == len(EXCLUDED)
    )
    check("pre_index_partition", set_contract_ok and classification_ok, len(pre_index ^ set().union(*query_partition)))

    strict_actual_content = {
        number for number in range(1665, 1833) if at(number).strip()
    }
    strict_union = set().union(*STRICT_MAIN_DISPOSITION.values())
    strict_overlap = sum(map(len, STRICT_MAIN_DISPOSITION.values())) - len(strict_union)
    strict_unresolved = len(strict_actual_content ^ strict_union) + strict_overlap
    strict_sets = {**STRICT_MAIN_DISPOSITION, "content": STRICT_MAIN_CONTENT}
    strict_ok = (
        set(strict_sets) == set(EXPECTED_STRICT_MAIN_PARTITION)
        and strict_union == set(STRICT_MAIN_CONTENT)
        and strict_actual_content == set(STRICT_MAIN_CONTENT)
        and strict_overlap == 0
        and STRICT_MAIN_NATIVE <= NATIVE_EVIDENCE
        and not STRICT_MAIN_STRUCTURAL & RETAINED
    )
    for name, values in strict_sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_STRICT_MAIN_PARTITION.get(name)
        strict_ok &= good
        check("strict_main_" + name, good, *actual)
    check("strict_main_partition", strict_ok, strict_unresolved)

    index_query_misses = set(INDEX_RELEVANT_UNIVERSE) - index_candidates
    index_unresolved = (
        len(set(INDEX_RELEVANT_UNIVERSE) ^ set(INDEX_ROUTED))
        + len(index_candidates - set(INDEX_RELEVANT_UNIVERSE))
    )
    index_universe_actual = (
        len(INDEX_RELEVANT_UNIVERSE),
        digest(INDEX_RELEVANT_UNIVERSE),
    )
    index_miss_actual = (len(index_query_misses), digest(index_query_misses))
    index_ok = (
        set(INDEX_CLASS) == set(EXPECTED_INDEX_CLASS)
        and frozenset().union(*INDEX_CLASS.values()) == INDEX_ROUTED
        and sum(map(len, INDEX_CLASS.values())) == len(INDEX_ROUTED)
        and not INDEX_ROUTED & INDEX_EXCLUDED
        and INDEX_RELEVANT_UNIVERSE == INDEX_ROUTED
        and index_candidates <= set(INDEX_RELEVANT_UNIVERSE)
        and index_universe_actual == EXPECTED_INDEX_RELEVANT_UNIVERSE
        and index_miss_actual == EXPECTED_INDEX_QUERY_MISSES
    )
    check("index_relevant_universe", index_universe_actual == EXPECTED_INDEX_RELEVANT_UNIVERSE, *index_universe_actual)
    check("index_query_misses", index_miss_actual == EXPECTED_INDEX_QUERY_MISSES, *index_miss_actual)
    for name, values in INDEX_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_INDEX_CLASS.get(name)
        index_ok &= good
        check("index_" + name, good, *actual)
    index_records, index_guards_ok = occurrence_records(INDEX_ENTRY_GUARDS, lines)
    sentinel_records, sentinels_ok = occurrence_records(INDEX_FLATTENING_SENTINELS, lines)
    index_ok &= (
        set(INDEX_ENTRY_GUARDS) == set(INDEX_ROUTED)
        and set(INDEX_FLATTENING_SENTINELS) <= set(INDEX_ROUTED)
        and index_guards_ok
        and sentinels_ok
    )
    check("index_partition", index_ok, index_unresolved)

    semantic_records = set(SOURCE_SEMANTIC_GUARD_RECORDS)
    semantic_actual = (len(semantic_records), digest_records(semantic_records))
    semantic_ok = (
        semantic_actual == EXPECTED_SOURCE_SEMANTIC_GUARDS
        and len(semantic_records) == len(SOURCE_SEMANTIC_GUARDS)
        and all(
            kind
            and positive
            and all(needle in at(number) for needle in positive)
            and all(needle not in at(number) for needle in negative)
            for kind, number, positive, negative in SOURCE_SEMANTIC_GUARDS
        )
    )

    catalog_lines = catalog.read_text(encoding="utf-8").splitlines()
    taxonomy_lines = taxonomy.read_text(encoding="utf-8").splitlines()
    atlas_lines = atlas.read_text(encoding="utf-8").splitlines()
    auxiliary_sources = {
        "catalog": catalog_lines,
        "taxonomy": taxonomy_lines,
        "atlas": atlas_lines,
    }
    auxiliary_records = {
        f"{source}:{number}:{'|'.join(positive)}!{'|'.join(negative)}"
        for source, number, positive, negative in AUXILIARY_SEMANTIC_GUARDS
    }
    auxiliary_ok = (
        all(
            source in auxiliary_sources
            and positive
            and all(needle in auxiliary_sources[source][number - 1] for needle in positive)
            and all(needle not in auxiliary_sources[source][number - 1] for needle in negative)
            for source, number, positive, negative in AUXILIARY_SEMANTIC_GUARDS
        )
        and len(catalog_lines) == 46
        and len(set(catalog_lines[1:])) == 45
        and not hits["Q00"]
    )

    excluded_hash_records = {
        f"{number}:{hashlib.sha256(at(number).encode('utf-8')).hexdigest()}"
        for number in EXCLUDED
    }
    strict_disposition_records = {
        f"{role}:{number}:{hashlib.sha256(at(number).encode('utf-8')).hexdigest()}"
        for role, values in STRICT_MAIN_DISPOSITION.items()
        for number in values
    }
    omission_records = {
        f"{number}:{reason}"
        for reason, values in SPLIT_OMISSION_GROUPS.items()
        for number in values
    }
    record_actuals = {
        "excluded_line_hashes": (len(excluded_hash_records), digest_records(excluded_hash_records)),
        "index_guards": (len(index_records), digest_records(index_records)),
        "index_sentinels": (len(sentinel_records), digest_records(sentinel_records)),
        "strict_main_dispositions": (
            len(strict_disposition_records),
            digest_records(strict_disposition_records),
        ),
        "semantic_guards": semantic_actual,
        "auxiliary_guards": (len(auxiliary_records), digest_records(auxiliary_records)),
        "source_defects": (len(SOURCE_DEFECT_GUARD_RECORDS), digest_records(SOURCE_DEFECT_GUARD_RECORDS)),
        "source_model": (len(SOURCE_MODEL_RECORDS), digest_records(SOURCE_MODEL_RECORDS)),
        "image_roles": (len(IMAGE_ROLE_RECORDS), digest_records(IMAGE_ROLE_RECORDS)),
        "image_assembly_boundaries": (len(IMAGE_ASSEMBLY_BOUNDARIES), digest_records(IMAGE_ASSEMBLY_BOUNDARIES)),
        "split_omissions": (len(omission_records), digest_records(omission_records)),
        "split_boundary_witnesses": (len(SPLIT_BOUNDARY_WITNESSES), digest_records(SPLIT_BOUNDARY_WITNESSES)),
    }
    record_ok = set(record_actuals) == set(EXPECTED_RECORDS)
    for name, actual in record_actuals.items():
        good = actual == EXPECTED_RECORDS.get(name)
        record_ok &= good
        check("record_" + name, good, *actual)
    record_ok &= (
        semantic_ok
        and auxiliary_ok
        and SOURCE_DEFECT_GUARD_RECORDS == frozenset(SOURCE_DEFECT_RECORDS)
        and len(SOURCE_DEFECT_RECORDS) == len(SOURCE_DEFECT_GUARD_RECORDS)
        and len(SOURCE_MODEL_RECORDS) == len(set(SOURCE_MODEL_RECORDS))
        and SPLIT_OMISSION_LINES <= (RETAINED | STRICT_MAIN_CONTENT)
        and len(omission_records) == len(SPLIT_OMISSION_LINES)
        and sum(map(len, SPLIT_OMISSION_GROUPS.values())) == len(SPLIT_OMISSION_LINES)
        and set(SPLIT_MAIN_SUMMARY_OWNERS) <= set(STRICT_MAIN_CONTENT)
        and SPLIT_OMISSION_LINES
        == STRICT_MAIN_CONTENT
        - set(SPLIT_MAIN_DIRECT_OWNERS)
        - set(SPLIT_MAIN_SUMMARY_OWNERS)
    )
    check("semantic_and_record_contracts", record_ok)

    image_sets = {
        **IMAGE_PARTITION,
        "governed": GOVERNED_IMAGE_LINES,
        "excluded": EXCLUDED_IMAGE_LINES,
        "candidate": CANDIDATE_IMAGE_LINES,
    }
    images_ok = (
        set(image_sets) == set(EXPECTED_IMAGE_PARTITION)
        and {name: (len(values), digest(values)) for name, values in IMAGE_PARTITION.items()}
        == EXPECTED_IMAGE_ROLE_PARTITION
        and {name: (len(values), digest(values)) for name, values in IMAGE_LEDGER.items()}
        == EXPECTED_IMAGE_LEDGER
        and frozenset().union(*IMAGE_PARTITION.values()) == GOVERNED_IMAGE_LINES
        and sum(map(len, IMAGE_PARTITION.values())) == len(GOVERNED_IMAGE_LINES)
        and CANDIDATE_IMAGE_LINES == GOVERNED_IMAGE_LINES | EXCLUDED_IMAGE_LINES
        and not GOVERNED_IMAGE_LINES & EXCLUDED_IMAGE_LINES
        and (len(CANDIDATE_IMAGE_LINES), digest(CANDIDATE_IMAGE_LINES)) == EXPECTED_CANDIDATE_IMAGE_LINES
        and (len(GOVERNED_IMAGE_LINES), digest(GOVERNED_IMAGE_LINES)) == EXPECTED_GOVERNED_IMAGE_LINES
        and (len(EXCLUDED_IMAGE_LINES), digest(EXCLUDED_IMAGE_LINES)) == EXPECTED_EXCLUDED_IMAGE_LINES
        and (len(UNRESOLVED_IMAGE_LINES), digest(UNRESOLVED_IMAGE_LINES)) == EXPECTED_UNRESOLVED_IMAGE_LINES
    )
    for name, values in image_sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_IMAGE_PARTITION.get(name)
        images_ok &= good
        check("images_" + name, good, *actual)

    image_manifest: set[str] = set()
    image_paths_ok = True
    for number in CANDIDATE_IMAGE_LINES:
        match = IMAGE_RE.fullmatch(at(number))
        image_paths_ok &= match is not None
        if match is None:
            continue
        matches = list(source_root.rglob(Path(match.group(1)).name))
        image_paths_ok &= len(matches) == 1
        if len(matches) != 1:
            continue
        asset = matches[0]
        image_manifest.add(
            f"{number}->{asset.relative_to(source_root).as_posix()}\0"
            f"{asset.stat().st_size}\0{sha256(asset)}"
        )
    image_manifest_actual = (len(image_manifest), digest_framed_records(image_manifest))
    images_ok &= image_paths_ok and image_manifest_actual == EXPECTED_IMAGE_ASSET_MANIFEST
    check("image_manifest", images_ok, *image_manifest_actual)

    split_paths = sorted(
        path
        for path in source_root.rglob("*.md")
        if path.resolve() not in {book.resolve(), atlas.resolve()}
    )
    relative_paths = [path.relative_to(source_root).as_posix() for path in split_paths]
    manifest = [
        f"{relative}\0{len(path.read_bytes())}\0{sha256(path)}"
        for path, relative in zip(split_paths, relative_paths, strict=True)
    ]
    split_manifest_ok = (
        len(split_paths) == EXPECTED_SPLIT_FILE_COUNT
        and digest_records(relative_paths) == EXPECTED_SPLIT_PATHS_DIGEST
        and digest_records(manifest) == EXPECTED_SPLIT_MANIFEST_DIGEST
    )
    check("split_manifest", split_manifest_ok, len(split_paths), digest_records(relative_paths), digest_records(manifest))

    split_text: dict[str, str] = {}
    for path, relative in zip(split_paths, relative_paths, strict=True):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            split_text[f"{relative}:{number}"] = line

    # Split closure is driven by the independent strict-main and actual-Index
    # universes, not merely by rows reached through discovery regexes.
    independent_crosswalk_universe = STRICT_MAIN_CONTENT | INDEX_RELEVANT_UNIVERSE
    crosswalk_lines = RETAINED | independent_crosswalk_universe
    crosswalk_records: set[str] = set()
    class_lines: dict[str, set[int]] = {
        name: set() for name in ("EXACT", "IMAGE_BASENAME", "NORMALIZED", "SUMMARY", "OMITTED")
    }
    class_records: dict[str, set[str]] = {name: set() for name in class_lines}
    normalized_scores: list[float] = []
    split_join_ok = True
    omission_reason_by_line = {
        number: reason
        for reason, values in SPLIT_OMISSION_GROUPS.items()
        for number in values
    }
    for number in sorted(crosswalk_lines):
        if number in SPLIT_OMISSION_LINES:
            mode = "OMITTED"
            record = f"{number}->OMITTED:{omission_reason_by_line[number]}"
        else:
            try:
                owner = split_owner_record(number)
            except ValueError:
                split_join_ok = False
                continue
            if owner not in split_text:
                split_join_ok = False
                continue
            if number in SPLIT_MAIN_SUMMARY_OWNERS:
                mode = "SUMMARY"
                score = 1.0
            else:
                mode, score = crosswalk_evidence(at(number), split_text[owner])
                if mode == "NORMALIZED":
                    normalized_scores.append(score)
                    split_join_ok &= score >= 0.97
                else:
                    split_join_ok &= score == 1.0
            record = f"{number}->{owner}:{mode}:{score:.6f}"
        crosswalk_records.add(record)
        class_lines[mode].add(number)
        class_records[mode].add(record)

    crosswalk_actual = (len(crosswalk_records), digest_records(crosswalk_records))
    class_actual = {
        name: (
            len(class_lines[name]),
            digest(class_lines[name]),
            digest_records(class_records[name]),
        )
        for name in class_lines
    }
    normalized_minimum = min(normalized_scores, default=1.0)
    split_join_ok &= (
        crosswalk_actual == EXPECTED_SPLIT_CROSSWALK
        and class_actual == EXPECTED_SPLIT_CLASSES
        and round(normalized_minimum, 6) == EXPECTED_SPLIT_NORMALIZED_MINIMUM
        and len(crosswalk_records) == len(crosswalk_lines)
        and set().union(*class_lines.values()) == set(crosswalk_lines)
        and sum(map(len, class_lines.values())) == len(crosswalk_lines)
        and SPLIT_OMISSION_LINES == class_lines["OMITTED"]
        and set(SPLIT_MAIN_SUMMARY_OWNERS) == class_lines["SUMMARY"]
    )
    check("split_crosswalk", split_join_ok, *crosswalk_actual, f"normalized_min={normalized_minimum:.6f}")
    for name, actual in class_actual.items():
        check("split_class_" + name, actual == EXPECTED_SPLIT_CLASSES.get(name), *actual)

    actual_logic_records = logic_records()
    logic_actual = (len(actual_logic_records), digest_records(actual_logic_records))
    logic_ok = logic_actual == EXPECTED_LOGIC_RECORDS
    check("exact_logic", logic_ok, *logic_actual)

    unresolved_total = (
        len(pre_index ^ set().union(*query_partition))
        + strict_unresolved
        + index_unresolved
        + (len(crosswalk_lines) - len(crosswalk_records))
        + len(UNRESOLVED_IMAGE_LINES)
        + (len(CANDIDATE_IMAGE_LINES) - len(image_manifest))
    )
    check("unresolved_total", unresolved_total == 0, unresolved_total)

    audit_records = {
        f"query:{name}:{len(values)}:{digest(values)}" for name, values in hits.items()
    } | {
        f"set:{name}:{len(values)}:{digest(values)}" for name, values in sets.items()
    } | {
        f"record:{name}:{count}:{record_digest}"
        for name, (count, record_digest) in record_actuals.items()
    } | {
        f"strict:{name}:{len(values)}:{digest(values)}"
        for name, values in strict_sets.items()
    } | {
        f"index-class:{name}:{len(values)}:{digest(values)}"
        for name, values in INDEX_CLASS.items()
    } | {
        f"index-universe:{index_universe_actual[0]}:{index_universe_actual[1]}",
        f"index-query-misses:{index_miss_actual[0]}:{index_miss_actual[1]}",
        f"strict-unresolved:{strict_unresolved}",
        f"index-unresolved:{index_unresolved}",
    } | {
        f"split:{name}:{count}:{line_digest}:{record_digest}"
        for name, (count, line_digest, record_digest) in class_actual.items()
    } | {
        f"image-manifest:{image_manifest_actual[0]}:{image_manifest_actual[1]}",
        f"logic:{logic_actual[0]}:{logic_actual[1]}",
        f"unresolved:{unresolved_total}",
    }
    audit_digest = digest_records(audit_records)
    check("audit_digest", audit_digest == EXPECTED_AUDIT_DIGEST, audit_digest)

    if json_mode:
        payload = {
            "audit_digest": audit_digest,
            "images": {
                "candidate": len(CANDIDATE_IMAGE_LINES),
                "control": len(CONTROL_IMAGE_LINES),
                "excluded": len(EXCLUDED_IMAGE_LINES),
                "native": len(NATIVE_IMAGE_LINES),
                "relation": len(RELATION_IMAGE_LINES),
                "unresolved": len(UNRESOLVED_IMAGE_LINES),
            },
            "queries": len(QUERIES),
            "query_union": len(union),
            "retained": len(RETAINED),
            "strict_main": {
                "content": len(STRICT_MAIN_CONTENT),
                "digest": digest(STRICT_MAIN_CONTENT),
                "native": len(STRICT_MAIN_NATIVE),
                "structural": len(STRICT_MAIN_STRUCTURAL),
                "unresolved": strict_unresolved,
            },
            "index": {
                "digest": digest(INDEX_RELEVANT_UNIVERSE),
                "query_misses": len(index_query_misses),
                "relevant": len(INDEX_RELEVANT_UNIVERSE),
                "unresolved": index_unresolved,
            },
            "split_crosswalk": len(crosswalk_records),
            "status": "PASS" if ok else "FAIL",
            "unresolved_total": unresolved_total,
        }
        print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    else:
        for name, good, metrics in output:
            print(name, "OK" if good else "MISMATCH", *metrics)
        print(
            "T40 source oracle:",
            "PASS" if ok else "FAIL",
            f"audit={audit_digest}",
            f"queries={len(QUERIES)}/union={len(union)}",
            f"retained={len(RETAINED)}",
            f"strict-main={len(STRICT_MAIN_CONTENT)}(N/S="
            f"{len(STRICT_MAIN_NATIVE)}/{len(STRICT_MAIN_STRUCTURAL)},closure={strict_unresolved})",
            f"index={len(INDEX_ROUTED)}/query-misses={len(index_query_misses)}"
            f"/closure={index_unresolved}",
            f"images={len(GOVERNED_IMAGE_LINES)}(N/R/C="
            f"{len(NATIVE_IMAGE_LINES)}/{len(RELATION_IMAGE_LINES)}/{len(CONTROL_IMAGE_LINES)})",
            f"split={len(crosswalk_records)}",
            f"unresolved={unresolved_total}",
        )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
