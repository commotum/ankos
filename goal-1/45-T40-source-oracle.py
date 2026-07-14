#!/usr/bin/env python3
"""Fail-closed primary-source audit for T40 mathematical-constant expansions.

T40's native identity is an immutable exact-number/representation denotation
plus typed coefficient queries.  It is not a fabricated mutable constant or a
mandatory append-prefix transition.  The Book also gives explicit algorithms
(long division, a square-root digit machine, continued-fraction iteration)
whose visible work states may be represented by ordinary SimplePrograms; those
are realizations of the denotation, not hidden executor state or T40's identity.

The Book does not use the catalog label.  Twenty bounded, redundant query
lanes freeze discovery witnesses, while independent fixed universes close all
117 nonblank rows in the strict main section and all 897 nonblank rows in the
canonical physical Index block.  A separate 108-row vocabulary scan and a
65-row hostile page/vocabulary/continuation review must have no unexplained
match.  The chapter split is intentionally treated as an abridged summary:
compressed tables and omitted mechanics are explicit split dispositions
rather than silently invented matches.
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
INDEX_CONTENT_FIRST_LINE = 20828
INDEX_CONTENT_LAST_LINE = 22456
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


# Exactly twenty bounded lanes from the first-principles audit.  Q00 proves
# that the catalog label is external vocabulary; Q15/Q16 close every image candidate.
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
        r"non-?computable.{0,80}digit|Chaitin.{0,120}digit|"
        r"digits of.{0,40}sqrt.{0,120}cellular automata|"
        r"digit sequence.{0,100}data compression|"
        r"whose n<sup>th</sup> digit for any n|"
        r"examples of non-computable reals that can readily be defined|"
        r"number whose.{0,40}digit is 1 - f\[n, n\]|"
        r"involve looking at real numbers in terms of digits"
    ),
    "Q14": (
        r"Mathematical constants, 136-144|Continued fractions, 143, 914|"
        r"Digit sequences, 116-127, 136-142|Number representations, 142|"
        r"Normal numbers, 912|Rational numbers approximation by|"
        r"Plouffe, Simon|Khinchin \(Khinchin.s constant\)"
    ),
    "Q15": r"_page_(?:151_Figure_7|154_Figure_2|156_Figure_1)\.jpeg",
    "Q16": (
        r"_page_(?:98_Figure_2|99_(?:Figure_1|Picture_4)|132_Figure_10|"
        r"150_Figure_[1-5]|575_Figure_5|576_Figure_4|609_Picture_2|"
        r"776_Figure_2|"
        r"161_Figure_1|162_Figure_1|884_Figure_30|960_Figure_3|1099_Figure_1|"
        r"923_Figure_21|926_Figure_14|986_Picture_[4-8]|"
        r"1106_Picture_4|1108_Figure_13|1109_Picture_[56]|"
        r"1201_Picture_(?:4|6|9|10|11)|"
        r"916_Figure_12|917_Picture_11|918_Figure_2|"
        r"927_Figure_14|928_Figure_(?:9|11|13|22)|"
        r"929_Picture_1[1-6]|930_(?:Picture_(?:4|12|14)|Figure_10)|"
        r"931_Figure_(?:9|10|11|12|13|17)|"
        r"1085_(?:Figure_16|Picture_18))\.jpeg"
    ),
    "Q17": (
        r"^#### (?:\*\*)?(?:The Sequence of Primes|Mathematical Functions)"
        r"(?:\*\*)?$"
    ),
    "Q18": (
        r"Implementation of digit sequences|History of numbers|"
        r"History of digit sequences|Gray code ordering|Negative bases|Non-power bases|"
        r"Multiplicative digit sequences|Greek and Roman number systems|"
        r"Another early sign.{0,120}digit sequence of a number|"
        r"digits of.{0,40}pi.{0,60}other transcendental numbers|"
        r"John Venn.{0,80}digits|Carl Friedrich Gauss noted.{0,80}continued fractions|"
        r"continued fractions.{0,80}Carl Friedrich Gauss noted|"
        r"Repetition in numbers|Emile Borel had formulated.{0,80}normal numbers|"
        r"Page 560.{0,40}Number representations"
    ),
    "Q19": (
        r"60 \(base\) of Babylonian numbers|Negative bases, 902|"
        r"representation of, 902, 942|Unary representation of numbers|"
        r"Zeckendorff representation"
    ),
}


def digest(values: set[int] | frozenset[int]) -> str:
    return hashlib.sha256(
        ",".join(map(str, sorted(values))).encode("ascii")
    ).hexdigest()


def newline_number_digest(values: set[int] | frozenset[int]) -> str:
    return hashlib.sha256(
        "".join(f"{number}\n" for number in sorted(values)).encode("ascii")
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
    "654,998,1008,1014,1449,1846,1850,1852,1854,1856,"
    "6768,6772,6776,7116,"
    "11252,11260,11531,11532,11536,"
    "12503,12515,12524,12532,12536,12550,12552,12554,12555,12557,12569,"
    "12984,12986,12988,12990,"
    "12992,12996,13000,13004,13018,13020,13022,13023,13029,13062,"
    "13074,13076,13084,13092,13094,13096,13098,13102,13103,13111,"
    "13119,13121,13123,13125,13127,13219,14172,14176,14468,14923,"
    "14925,14927,14929,14931,14933,15517,17107,17130,17167,17171,"
    "17236,17599,17762,17851,17876,17878,20507,20588,20592,20594,20596,20598"
)
QUERY_CONTROL = line_set(
    "1619,1834,9246,12846,13134,13146,17101,19058,19074,19076,19078,19080"
)

EXCLUDED_CLASS = {
    "name_collision": line_set("146"),
    "generic_algorithm_cross_reference": line_set("17845,19345,19563"),
    "sibling_asset_observer": line_set(
        "1649,1651,1653,1655,1657,12844,12917,17593,17847,20584"
    ),
}
EXCLUDED = frozenset().union(*EXCLUDED_CLASS.values())


# This independent hostile-review lane scans the complete Book, not merely
# the hand-built query windows or the fixed strict/Index universes.  Its
# vocabulary is deliberately broader than T40: every pre-Index match is
# either retained as native/relation/control evidence or frozen below as a
# bounded sibling construction.  Index matches inherit the exhaustive
# physical-row disposition proved later.
BOOK_BROAD_VOCABULARY_PATTERN = (
    r"digit sequences?|"
    r"n(?:<sup>|\^\{?)?th(?:</sup>|\}?)?[^\n]{0,24}digit|"
    r"continued fractions?|normal numbers?|non-?computable reals?|"
    r"computable real numbers?|number representations?|"
    r"positional (?:notation|representations?)|negative bases?|"
    r"unary representation|zeckendorff representation|"
    r"(?:(?:binary|decimal|hexadecimal|base (?:2|10|16|60))"
    r"[^\n]{0,80}(?:digit|number|representation)|"
    r"(?:digit|number|representation)[^\n]{0,80}"
    r"(?:binary|decimal|hexadecimal|base (?:2|10|16|60)))"
)
BOOK_BROAD_EXCLUSION_CLASS = {
    "rule-machine-code-carriers": line_set(
        "720,1198,1204,2194,2922,3330,3336"
    ),
    "t36-t37-number-evolution-siblings": line_set(
        "1392,1394,1447,1451,1457,1461,1467,1475,1485,1489,1503,"
        "1525,1527,1531,1545,1601,1611,1613,1645"
    ),
    "t43-iterated-map-work-siblings": line_set(
        "1874,1876,1880,1882,1886,1898,1900,1908,1920,1924,1928,"
        "1932,1940,1944,1946,1950,2008"
    ),
    "other-simple-program-coordinate-encodings": line_set(
        "2484,2548,2674"
    ),
    "chaos-physical-sampling-observers": line_set(
        "3584,3594,3598,3600,3612,3614,3628,3636,3646,3652,3672,"
        "3724,3736,3744,4260,5916"
    ),
    "compression-crypto-computation-siblings": line_set(
        "7120,7272,7274,7312,7322,7388,7390,7406,7410,7424,7974,"
        "7990,8078,8834,8838,9002,9004,9010,9020,9058,9080,9216,"
        "9220,9268,9378,9651,10461,10988"
    ),
    "sibling-type-notes-before-t40": line_set(
        "11272,12054,12120,12255,12257,12609,12613,12631,12639,"
        "12643,12676,12751,12915"
    ),
    "t43-ca-sibling-notes": line_set(
        "13186,13231,13233,13235,13261,13263,13266,13268,13692,"
        "13764,14095,14237,14275,14299,14340,14857,14971,15002,15006"
    ),
    "downstream-philosophical-compression-siblings": line_set(
        "16246,17199,17202,17726,17758,17766,17772,17924"
    ),
    "generic-complexity-cost-analogies": line_set("19386,19401"),
}
BOOK_BROAD_EXCLUDED = frozenset().union(*BOOK_BROAD_EXCLUSION_CLASS.values())

# These rows are not broad-vocabulary hits; they are frozen because retained
# interrupted spans or control boundaries touch them directly.
SOURCE_SPAN_EXCLUSION_CLASS = {
    "interleaved-page26-sibling": line_set("11258"),
    "adjacent-history-siblings": line_set("11533,11535"),
}
SOURCE_SPAN_EXCLUDED = frozenset().union(*SOURCE_SPAN_EXCLUSION_CLASS.values())
SOURCE_SPAN_EXCLUSION_GUARDS = {
    11258: ("Page 26", "Pascal's triangle and rule 90"),
    11533: ("distribution of primes", "regularities"),
    11535: ("three-body problem",),
}


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
    "656,1848,1858,6766,6770,6774,6778,6780,6782,"
    "11250,11254,11256,"
    "12194,12196,12198,12200,12202,12204,12206,12540,12542,"
    "12505,12507,12509,12511,12513,12517-12520,12522,"
    "12526,12528,12530,12534,"
    "12587,12589,12591,12593,12595,"
    "12994,12998,13002,13006-13016,13025,13027,13064-13068,"
    "13078-13082,13105,13107,13109,13113,13115,13117,13129,13130,"
    "13132,13136,13138-13144,14170,14174,17105,"
    "17131-17133,17135-17137,17139,17141-17145,17147,17149-17151,"
    "17153,17155-17159,17161,17163,17165,17169,17173,17175,17176,17178,"
    "17234,17597,17760,17849,17853,17855,17857,17859,17861,"
    "17863,17865,17867-17872,17874,"
    "18211,18339,18341-18346,18348,19066,19068,19070,19072,19194,20117,"
    "20505,20586,20590"
)
CONTROL_CONTINUATIONS = line_set(
    "1663,12919,19082,19084,19086,19087,19089,19185,19187,"
    "19190,19244,19494-19507,19509,19526,19528"
)

NATIVE_EVIDENCE = QUERY_NATIVE | NATIVE_CONTINUATIONS | STRICT_MAIN_NATIVE
RELATION_EVIDENCE = QUERY_RELATION | RELATION_CONTINUATIONS
CONTROL_EVIDENCE = QUERY_CONTROL | CONTROL_CONTINUATIONS
RETAINED = NATIVE_EVIDENCE | RELATION_EVIDENCE | CONTROL_EVIDENCE


# The native Notes section for T40 is a second fixed source universe, not a
# collection assembled from successful regex hits.  Every nonblank row from
# the first Notes claim through the last substantive Notes row is already in
# one semantic evidence role and must remain so.
STRICT_NOTES_FIRST_LINE = 12921
STRICT_NOTES_LAST_LINE = 13144
STRICT_NOTES_CONTENT = line_set(
    "12921,12923,12925-12927,12929,12931,12933,12935,12937-12939,12941,"
    "12943,12945-12946,12948-12949,12951,12953-12956,12958,12960,12962,"
    "12964,12966,12968,12970,12972,12974,12976,12978,12980,12982,12984,"
    "12986,12988,12990,12992,12994,12996,12998,13000,13002,13004,"
    "13006-13010,13012,13014,13016,13018,13020,13022-13023,13025,13027,"
    "13029-13030,13032,13034,13036,13038,13040,13042,13044,13046,13048,"
    "13050,13052,13054,13056,13058,13060,13062,13064-13068,13070,13072,"
    "13074,13076,13078,13080-13082,13084,13086,13088,13090,13092,13094,"
    "13096,13098,13100,13102-13103,13105,13107,13109,13111,13113,13115,"
    "13117,13119,13121,13123,13125,13127,13129-13130,13132,13134,13136,"
    "13138-13142,13144"
)
STRICT_NOTES_DISPOSITION = {
    "native": NATIVE_EVIDENCE & STRICT_NOTES_CONTENT,
    "relation": RELATION_EVIDENCE & STRICT_NOTES_CONTENT,
    "control": CONTROL_EVIDENCE & STRICT_NOTES_CONTENT,
}


INDEX_CLASS = {
    "native": line_set(
        "20828,20908,20910,20916,20918,20946,21044,21054,21072,"
        "21088,21102,21189,21255,21329,21337,21360,21416,21473,"
        "21475,21501,21683,21705,21711,21735,21779,21793,21801,"
        "21891,21907,22136"
    ),
    "relation": line_set(
        "20836,20840,20846,20850,20862,20864,20868,20882,20904,20906,20914,20940,"
        "20942,20967,20972,21014,21022,21038,21042,21050,21080,"
        "21086,21090,21114,21132,21134,21148,21150,21162,21168,"
        "21172,21173,21181,21185,21187,21193,21195,21197,21203,"
        "21207,21213,21223,21231,21233,21264,21275,21277,21290,21333,"
        "21420,21432,21450,21454,21460,21497,21525,21586,21602,"
        "21642,21646,21648,21675,21687,21689,21695,21731,21771,21777,21803,"
        "21805,21813,21819,21841,21845,21877,21893,21903,21915,"
        "21923,21927,21929,21933,21982,21990,21994,22030,22080,"
        "22110,22112,22114,22120,22144,22146,22148,22150,22352,22380,"
        "22382,22394,22434,22452,22456"
    ),
    "control": line_set("20970,22096,22362,22386"),
}
INDEX_ROUTED = frozenset().union(*INDEX_CLASS.values())
INDEX_EXCLUDED = line_set(
    "20888,20965,20980,21108,21274,21338,21362,21471,21515,21545,"
    "21783,21881,21925,22016,22132,22412"
)
INDEX_SEMANTIC_UNIVERSE = INDEX_ROUTED

# This lane reproduces a deliberately broad hostile-review vocabulary scan
# over the fixed physical Index block.  It is independent of the hand-routed
# semantic rows; every match must be routed or explicitly excluded.
INDEX_BROAD_VOCABULARY_PATTERN = (
    r"digit|base [0-9]|binary|decimal|hexadec|continued fraction|"
    r"partial quotient|number representation|long division|integerdigits|"
    r"rational|irrational|radical|square root|normal number|leading digit|"
    r"recurring|concatenation sequence|digital slope|first digit|nth.?digit|"
    r"n\^.?th.*digit|transcendental|mathematical constant|catalan|"
    r"champernowne|stoneham|khinchin|power.?mod|plouffe|euclid.s algorithm|"
    r"[0-9]+ \(base\)|(?:negative|arbitrary|non-power) bases|"
    r"representation of, 902, 942|unary representation of numbers|"
    r"zeckendorff representation|Arithmetic algorithmic randomness|"
    r"computable numbers, 1128|computable reals, 1128|continuous computation, 1128|"
    r"(?:defining|of|and) algorithmic randomness"
)

# A separate independent page/vocabulary/flattened-continuation review found
# rows that the broad textual pattern cannot see.  Its positive and noisy
# candidates are intentionally frozen together, before semantic disposition.
INDEX_HOSTILE_AUDIT_CANDIDATES = line_set(
    "20836,20846,20862,20864,20868,20882,20888,20904,20906,20908,20940,20942,20965,"
    "20970,20980,21022,21042,21072,21080,21086,21090,21102,21108,"
    "21148,21181,21189,21233,21274,21275,21277,21290,21329,21333,21338,"
    "21362,21420,21454,21460,21471,21515,21545,21586,21602,21642,21646,21648,"
    "21731,21771,21777,21783,21803,21841,21877,21881,21903,21923,"
    "21925,22016,22112,22114,22120,22132,22146,22362,22382,22386,"
    "22412,22434,22452,22456"
)

INDEX_ENTRY_GUARDS = {
    20828: ("continued fraction for, 144", "digits of, 142"),
    20836: ("60 (base) of Babylonian numbers, 902", "5/2, multiplication system, 123"),
    20840: ("Addition cellular automata based on", "in digit sequences, 118"),
    20846: ("representing numbers using, 916",),
    20850: ("nested digit sequences",),
    20862: ("in hierarchy of numbers, 916", "Algorithmically simple integers, 916"),
    20864: ("and history of numbers, 902",),
    20868: ("Archimedes (Sicily, 287–212 BC)", "and  $\\pi$ , 911"),
    20882: ("Arithmetic algorithmic randomness in, 1067",),
    20904: ("and computing  $\\pi$ , 911",),
    20906: ("and computing *Sqrt*, 913",),
    20908: ("Base 1 (unary), 560, 1070", "Base 2 (binary), 116"),
    20910: ("Base 16 (hex)", "normal numbers, 912"),
    20914: ("leading digits", "Egyptian fractions"),
    20916: ("Bits in numbers, 116", "see also Digit sequences"),
    20918: ("Blocks", "normal numbers, 912"),
    20940: ("Bresenham's algorithm, 916",),
    20942: ("Buffon's needle (for evaluating  $\\pi$ ), 1192",),
    20946: ("Catalan (Catalan's constant)", "and digit sequences, 902"),
    20967: ("states vs. digit sequences, 950",),
    20970: ("Chaitin, Gregory J.", "and algorithmic randomness, 1068"),
    20972: ("Champernowne number", "normal numbers, 912"),
    21014: ("of number representations, 1070",),
    21022: ("of computing  $\\pi$ , 912",),
    21038: ("Concatenation sequences", "continued fractions for, 915"),
    21042: ("Constants mathematical, 136–144",),
    21044: ("Continued fraction map", "Continued fractions, 143, 914"),
    21050: ("Corollaries", "nested radicals"),
    21054: ("Cryptanalysis continued fraction for, 914", "digits of, 141"),
    21072: ("Decimal numbers, 116", "recurring, 138"),
    21080: ("minimal in rational numbers, 950",),
    21086: ("numbers generated from, 916",),
    21088: ("Digit sequences, 116-127, 136-142",),
    21090: ("DigitCount, 902", "lines on digital, 916"),
    21102: ("Divide (/)", "in terms of digits, 139"),
    21114: ("Dynamic programming", "Egyptian fractions"),
    21132: ("runs of digits",),
    21134: ("ENIAC (computer)", "and digits of  $\\pi$ , 911"),
    21148: ("as defining numbers, 916", "Transcendental equations"),
    21150: ("Equidistribution", "concatenation sequences"),
    21162: ("Exact solutions", "Euclid's algorithm"),
    21168: ("ExpIntegralEi", "Egyptian fractions"),
    21172: ("leading digits", "Factorial2"),
    21173: ("multiplicative digit sequences, 902",),
    21181: ("Feigenbaum's constant, 913",),
    21185: ("Feynman diagrams", "leading digits"),
    21187: ("Fibonacci number representation. 560, 1070",),
    21189: ("First digits, 914", "of powers, 903"),
    21193: ("and digital slopes, 916",),
    21195: ("Fractional linear transformations and continued fractions, 914",),
    21197: ("Fraenkel", "leading digits"),
    21203: ("applied to digit sequences, 731",),
    21207: ("and quadratic continued fractions, 915",),
    21213: ("Generalization", "Euclid's algorithm"),
    21223: ("Gibbs phenomenon", "Euclid's algorithm"),
    21231: ("Graphics3D", "concatenation sequences"),
    21233: ("Halton (digit reversal) sequences",),
    21255: ("Human thinking", "Hurwitz numbers"),
    21264: ("and continued fractions, 914<br>",),
    21275: ("and defining randomness, 1068",),
    21277: ("from rational integral, 916",),
    21290: ("IBM 7090 computer, and $\\pi$ , 911",),
    21329: ("IntegerDigits basic examples of, 854", "concatenation of 913"),
    21333: ("Integrate", "numbers generated by, 916"),
    21337: ("Irrational numbers", "iterated multiplication by, 903"),
    21360: ("Iterated division", "continued fractions, 143"),
    21416: ("Khinchin", "Khinchin's constant"),
    21420: ("KleinInvariantJ", "and almost integers, 915"),
    21432: ("and continued fractions, 915", "Lagrange points"),
    21450: ("LatticeReduce", "Leading digits"),
    21454: ("Leibniz, Gottfried W. v.", "and binary numbers, 902"),
    21460: ("Light as defining rationals, 916",),
    21473: ("Log (logarithm)", "computation of  $n^{th}$  digits"),
    21475: ("Long division, 139",),
    21497: ("Markov partitions and digit sequences, 901",),
    21501: ("Mathematical constants, 136-144",),
    21525: ("Multiplicative digit sequences, 902", "and continued fractions, 914"),
    21586: ("for  $\\pi$ , 912",),
    21602: ("Napier, John", "and binary numbers, 902"),
    21642: ("Needle, Buffon's for  $\\pi$ , 1192",),
    21646: ("Negative bases, 902", "Negative numbers"),
    21648: ("representation of, 902, 942",),
    21675: ("Nested radicals, 915",),
    21683: ("NestWhileList", "concatenation sequences"),
    21687: ("leading digits",),
    21689: ("for computing square roots, 913",),
    21695: ("Non-locality and Bell's inequalities", "in digit sequences, 730"),
    21705: ("Normal numbers, 912", "concatenation sequences"),
    21711: ("Number representations, 142",),
    21731: ("number of (DigitCount), 902", "Operator representations"),
    21735: ("Partial quotients", "in continued fractions, 914"),
    21771: ("Periods (number type), 916",),
    21777: ("Physical constants numerology for, 1025", "approximations to, 912"),
    21779: (
        "computation of nth digits in, 912",
        "continued fraction for, 143, 914",
        "digit sequence of, 136",
    ),
    21793: ("Plouffe, Simon", "computation of  $\\pi$"),
    21801: ("PolyLog (polylogarithms)", "and computing  $n^{th}$  digits, 912"),
    21803: ("Population count (DigitCount), 902", "Positional notation for numbers, 116"),
    21805: ("PowerMod", "digit sequences of, 119, 614, 749"),
    21813: ("leading digits in, 914",),
    21819: ("ProductLog", "concatenation sequences"),
    21841: ("use of base 2 in, 902",),
    21845: ("Pythagoreans", "continued fraction map"),
    21877: ("Quasi-Monte Carlo methods", "and digit reversal, 905"),
    21891: ("Radicals continued fractions for, 144", "digit sequences for, 139"),
    21893: ("from digits of  $\\pi$ , 136, 912", "in digit of square roots, 139"),
    21907: ("Rational numbers approximation by",),
    21915: ("Reciprocals", "Egyptian fractions"),
    21903: ("lines on digital, 916",),
    21923: ("Register machines, 97–102", "for computing Sqrt, 1114"),
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
    22112: ("Shortest descriptions", "for integers, 916"),
    22114: ("Slopes digital representation of, 916",),
    22120: ("Solomonoff, Ray J.", "and algorithmic randomness"),
    22136: ("Stoneham", "normal numbers, 912"),
    22144: ("Substitution systems, 82-87", "and continued fractions, 914"),
    22146: ("sequential, 88-92", "Sum, numbers generated from, 917"),
    22148: ("Superstrings", "runs of digits"),
    22150: ("Symbolic programming", "leading digits"),
    22352: ("Toffoli, Tommaso", "Egyptian fractions"),
    22362: (
        "and computable numbers, 1128, 1137",
        "and continuous computation, 1128",
        "and computable reals, 1128",
    ),
    22380: ("Two's complement number representation, 902, 942",),
    22382: ("Unary representation of numbers, 560, 1070",),
    22386: ("Undecidability, 753–757", "of algorithmic randomness, 1067"),
    22394: ("Valuation functions", "nested digit sequences"),
    22434: ("Wozniakowski (digit reversal) sequences, 905",),
    22452: ("Zeckendorff representation, 892, 1070",),
    22456: ("from rational integrals, 916", "Zeta (Riemann zeta function)"),
}

INDEX_EXCLUDED_GUARDS = {
    20888: ("Associative algebras, 801", "as generalizing numbers, 1168"),
    20965: ("Gray code sequence of, 352",),
    20980: ("Code 1893 on inspirational cover, 17",),
    21108: ("Dungeons & Dragons shapes of dice in, 971",),
    21274: ("and trinomial coefficients, 1091",),
    21338: ("Irreducible representations (of groups)",),
    21362: ("IUPAC chemical nomenclature",),
    21471: ("Littlewood, John E.", "and numbers of primes, 910"),
    21515: ("Melting points of alkanes, 1194",),
    21545: ("generating Euclidean spaces, 1036",),
    21783: ("Planck's constant, 1061",),
    21881: ("Racah coefficients, see 6 j symbols",),
    21925: ("inspirational book cover, 864",),
    22016: ("Rule 129 enumerating powers of 2, 641",),
    22132: ("Spectra (atomic)",),
    22412: ("Verhulst equation and iterated maps. 918",),
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
    "998,1008,1014,1449,1846,1854,6768,6776,7116,11252,"
    "12524,12552,12557,12992,12996,13000,13020,"
    "13076,13094,13098,14176,14925,14927,14929,14931,14933,17762,"
    "17876,17878,"
    "20588,20594,20596,20598,"
    "13119,13121,13123,13125,13127,17167,17171"
)
CONTROL_IMAGE_LINES = line_set("9246,13134")
GOVERNED_IMAGE_LINES = (
    NATIVE_IMAGE_LINES | RELATION_IMAGE_LINES | CONTROL_IMAGE_LINES
)
EXCLUDED_IMAGE_LINES = line_set(
    "1649,1651,1653,1655,1657,12844,12917,17593,17847,20584"
)
CANDIDATE_IMAGE_LINES = GOVERNED_IMAGE_LINES | EXCLUDED_IMAGE_LINES
UNRESOLVED_IMAGE_LINES = frozenset()

IMAGE_ROLE_RECORDS = (
    "998:relation:physical page98 neighbor-independent substitution observer invoked by page83",
    "1008:relation:physical page99 substitution-tree observer invoked by page84",
    "1014:relation:physical page99 substitution-branch observer invoked by page84",
    "1449:relation:physical page132 nested binary-digit observer invoked by page117",
    "1677:native:page151 pi base-two walk observer",
    "1711:native:page154 rational long-division work panels",
    "1744:native:page156 square-root product-state work panels",
    "1649:excluded:page150 sequence-property sibling observer a",
    "1651:excluded:page150 sequence-property sibling observer b",
    "1653:excluded:page150 sequence-property sibling observer c",
    "1655:excluded:page150 sequence-property sibling observer d",
    "1657:excluded:page150 sequence-property sibling observer e",
    "1846:relation:page161 trigonometric crossing-family source observer",
    "1854:relation:page162 continued-fraction-driven substitution observer",
    "6768:relation:physical page575 unary binary self-delimiting and Fibonacci observer invoked by page560",
    "6776:relation:physical page576 run-length observer invoked by page561 and page560 representation-e",
    "7116:relation:page609 block-frequency composite observer invoked by page594 Sturmian span",
    "9246:control:page776 Turing-complexity observer invoked by page761 resource boundary",
    "11252:relation:page884 cellular-automaton Cantor-map representation observer",
    "12524:relation:page916 Gray-code representation observer",
    "12552:relation:page917 negative-base representation observer",
    "12557:relation:page918 multiplicative-digit representation observer",
    "12844:excluded:page923 pre-T40 prime-section sibling observer",
    "12917:excluded:page926 aliquot-sum sibling observer",
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
    "14176:relation:page960 Pell continued-fraction size observer",
    "14925:relation:page986 billiard continued-fraction slope observer a",
    "14927:relation:page986 billiard continued-fraction slope observer b",
    "14929:relation:page986 billiard continued-fraction slope observer c",
    "14931:relation:page986 billiard continued-fraction slope observer d",
    "14933:relation:page986 billiard continued-fraction slope observer e",
    "17167:relation:physical page1085 representation-length observer invoked by page560 notes",
    "17171:relation:physical page1085 self-delimiting-completeness observer invoked by page560 notes",
    "17593:excluded:page1099 least-squares model-fit sibling observer",
    "17762:relation:page1106 rule-60 difference-table observer including pi digits",
    "17876:relation:page1109 base-two power-tree computation observer",
    "17878:relation:page1109 base-three conversion computation observer",
    "17847:excluded:page1108 visible-lattice-point sibling observer",
    "20584:excluded:page1201 preceding doubling-rule sibling observer",
    "20588:relation:page1201 minimal-CA repetitive-sequence context observer",
    "20594:relation:page1201 powers-of-two minimal-CA observer",
    "20596:relation:page1201 squares minimal-CA observer",
    "20598:relation:page1201 Thue-Morse minimal-CA observer",
)
IMAGE_ASSEMBLY_BOUNDARIES = (
    "cross-page-substitution:998,1008,1014,1449 are explicitly invoked by retained digit-codec relations",
    "page560-561:6768,6776 form representation and downstream run-length application observers",
    "continuation-assets:1846,1854,11252,14176 are governed by retained adjacent relation spans",
    "excluded-asset:17593 is a least-squares sibling observer, not the later Sturmian span",
    "excluded-boundaries:1649,1651,1653,1655,1657,12844,12917,17847,20584 belong to adjacent sibling spans",
    "page986:14925,14927,14929,14931,14933 form the billiard continued-fraction assembly",
    "page1201:20588,20594,20596,20598 govern minimal-CA sequence context and three targets",
    "page1106:17762 is a composite transformation observer, not a T40 digit generator",
    "page1109:17876,17878 compare whole-prefix methods despite a one-digit query",
    "cross-page-boundaries:7116 and 9246 are invoked Sturmian and resource-control observers",
    "page916-918:12524,12552,12557 are governed representation-relation assets",
    "page928:12992,12996,13000 form the concatenation-walk trilogy",
    "page929:13040,13042,13044,13046,13048,13050 form six residual panels",
    "page930:13094,13098 form the Euclidean-algorithm relation pair",
    "page931:13119,13121,13123,13125,13127 form five digital-slope panels",
    "main:1711 and 1744 have physical files but no split Markdown references",
    "paths:monolith references omit Images while split references include it",
    "boundary:all 63 candidate assets are hash-bound and supply no pixel-derived mechanics",
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
    (
        "pi_complexity_history",
        654,
        ("digit sequence of a number like", "more than a hundred digits", "appeared quite random"),
        (),
    ),
    ("pi_complexity_history_completion", 656, ("simple rules like those for computing", "produce complex results"), ()),
    (
        "cf_substitution_relation",
        1850,
        ("generalized substitution system", "continued fraction representation"),
        (),
    ),
    ("trigonometric_source_observer", 1848, ("adding together various sine functions", "ultimately repetitive", "chords"), ()),
    ("cf_substitution_interrupted_claim", 1852, ("square root", "purely repetitive"), ("generated pattern nested",)),
    ("cf_substitution_completion", 1858, ("generated pattern nested", "no particular connection"), ()),
    (
        "page560_encoding_context",
        6766,
        ("run-length encoding", "number \"53\"", "black and white cells"),
        (),
    ),
    (
        "page560_representation_caption",
        6770,
        ("unary", "ordinary binary or base 2", "self-delimiting", "binary-coded-ternary", "Fibonacci sequence"),
        (),
    ),
    ("page560_delimitation_problem", 6772, ("digit sequence", "short representation for a number", "no way to tell"), ()),
    (
        "page560_delimitation_schemes",
        6774,
        ("specification of how many digits", "two cells representing each digit", "non-integer base"),
        (),
    ),
    ("page561_representation_application", 6782, ("representation (e) from page 560", "run-length encoding", "compression is achieved"), ()),
    (
        "ca_cantor_map_relation",
        11250,
        ("state space of a 1D cellular automaton", "Cantor set", "continuous mapping"),
        (),
    ),
    ("ca_digit_map_relation", 11256, ("digits of rational numbers", "Rule 170", "classic shift map"), ()),
    ("ca_digit_map_completion", 11260, ("this map has the form Mod[2x, 1]", "page 153"), ()),
    (
        "pi_randomness_history",
        11532,
        ("digits of", "transcendental numbers", "apparent randomness", "process of calculation"),
        (),
    ),
    ("venn_pi_history", 11536, ("John Venn", "randomness of the digits"), ()),
    (
        "whole_positional_encode",
        12503,
        ("whole number n", "sequence of digits in base k", "Integer Digits[n, k]"),
        (),
    ),
    (
        "whole_positional_inverse",
        12505,
        ("Reverse[Mod[NestWhileList", "FromDigits[list, k]"),
        (),
    ),
    (
        "fractional_positional_query",
        12507,
        ("number x between 0 and 1", "first m digits", "RealDigits[x, k, m]"),
        (),
    ),
    (
        "fractional_residual_iteration",
        12509,
        ("Floor[k NestList[Mod[k#, 1]",),
        (),
    ),
    (
        "fractional_reconstruction_claim",
        12511,
        ("reconstruct an approximation", "FromDigits[{list, 0}, k]"),
        (),
    ),
    (
        "fractional_reconstruction_fold",
        12513,
        ("Fold[#1/k + #2", "Reverse[list]"),
        (),
    ),
    (
        "gray_code_relation",
        12515,
        ("Gray code ordering", "successive numbers", "differ in only one digit"),
        (),
    ),
    (
        "gray_code_construction",
        12519,
        ("Nest[Join", "Length[#] + Reverse[#]"),
        (),
    ),
    (
        "gray_code_observer_boundary",
        12522,
        ("digit sequence picture", "BitXor[i, Floor[i/2]]", "rule 60 cellular automaton"),
        (),
    ),
    ("substitution_digit_automaton", 12194, ("Connections with digit sequences", "substitution system", "successive digits"), ()),
    ("substitution_digit_automaton_rule", 12198, ("finite automaton", "digit sequences in base k", "nested structure"), ()),
    ("fibonacci_position_codec", 12204, ("generalize the notion of digit sequences", "base k", "Fibonacci"), ()),
    ("fibonacci_position_uniqueness", 12206, ("representation is unique", "adjacent 1's", "substitution system"), ()),
    ("symbolic_dynamics_boundary", 12528, ("symbolic dynamics approach", "digit sequence approach", "digit expansions"), ()),
    ("symbolic_dynamics_scope", 12530, ("only shifts", "simple operations", "not been seen"), ()),
    ("page117_substitution_relation", 12540, ("Substitution systems", "connections between digit sequences"), ()),
    (
        "number_history_scope",
        12532,
        ("History of numbers", "whole numbers", "rational numbers", "square roots"),
        (),
    ),
    (
        "explicit_representation_history",
        12534,
        ("explicit representation for numbers", "sequence of digits", "certain length"),
        (),
    ),
    (
        "arbitrary_base_history",
        12536,
        ("Babylonian base 60", "Hindu-Arabic base 10", "arbitrary bases"),
        (),
    ),
    (
        "negative_base_relation",
        12550,
        ("Negative bases", "From Digits[list, -k]", "base -2"),
        (),
    ),
    (
        "non_power_base_relation",
        12554,
        ("Non-power bases", "f[n] need not be", "representation is not generally unique"),
        (),
    ),
    (
        "multiplicative_digit_relation",
        12555,
        ("Multiplicative digit sequences", "combined not by addition but by multiplication"),
        (),
    ),
    ("direct_nth", 12943, ("without explicitly finding previous ones", "overwhelming probability"), ("certainly exact",)),
    ("finite_precision_probability", 12951, ("finite-precision arithmetic", "probability exists", "incorrect results"), ()),
    ("normality_base", 12976, ('normal" in a particular base', "does not imply anything"), ()),
    ("sqrt_invariant_claim", 12982, ("s^2 + 4r = 4^t n", "any rational number", "1 \\le n < 4"), ()),
    (
        "irrational_cf_substitution_seam",
        12587,
        ("any h that is not a rational number", "continued fraction form", "first m rules"),
        (),
    ),
    (
        "cf_tail_drops_integer_part",
        12589,
        ("Reverse", "Rest", "ContinuedFraction", "h, m"),
        (),
    ),
    (
        "signed_cf_integer_part",
        12591,
        ("Floor[h] + Fold", "original sequence"),
        (),
    ),
    (
        "quadratic_cf_periodicity",
        12593,
        ("solution to a quadratic equation", "continued fraction form is repetitive"),
        (),
    ),
    (
        "cf_substitution_examples",
        12595,
        ("neighbor-independent substitution system", "GoldenRatio", "sqrt{2}", "sqrt{3}"),
        (),
    ),
    ("continued_fraction_query", 13030, ("first n terms", "ContinuedFraction"), ()),
    ("continued_fraction_iteration", 13032, ("Floor[NestList[1/Mod[#, 1] &, x, n-1]]",), ()),
    ("continued_fraction_inverse", 13034, ("reconstructed", "FromContinuedFraction"), ()),
    ("unbounded_coefficients", 13052, ("terms in a continued fraction can be of any size",), ()),
    ("substitution_relation", 13062, ("nested structure", "substitution system"), ()),
    ("approximation_observer", 13088, ("closeness of successive rational approximations",), ()),
    ("euclid_relation", 13092, ("Euclid's algorithm", "ContinuedFraction[a/b]"), ()),
    ("digital_slope_relation", 13111, ("Digital slope representation", "Floor[nh] - Floor[(n-1)h]"), ()),
    ("gauss_cf_map_history", 13219, ("Carl Friedrich Gauss", "continued fractions", "FractionalPart[1/x]"), ()),
    ("pell_cf_relation", 14170, ("Pell equation", "infinitely many solutions", "smallest solution"), ()),
    ("pell_cf_observer", 14174, ("plotted below", "complicated variation", "1766319049"), ()),
    ("number_repetition_relation", 15517, ("Repetition in numbers", "digits in rational numbers", "continued fraction terms"), ()),
    ("randomness_history_scope", 17105, ("History", "statistical hypothesis testing", "tests for randomness"), ()),
    ("normal_number_history", 17107, ("Emile Borel", "normal numbers", "algorithmic randomness"), ()),
    ("page560_notes_heading", 17130, ("Page 560", "Number representations", "sequence of 1's and 0's"), ()),
    ("page560_notes_unary_binary", 17131, ("Unary", "Not self-delimited"), ()),
    ("page560_notes_length_prefix", 17133, ("Length prefixed", "unary specification of its length"), ()),
    ("page560_notes_binary_ternary", 17139, ("Binary-coded base 3", "pair of base 2 digits"), ()),
    ("page560_notes_fibonacci", 17147, ("Fibonacci encoding", "decomposes", "no pair of 1's"), ()),
    ("page560_notes_lengths", 17161, ("Lengths of representations", "GoldenRatio"), ()),
    ("page560_notes_completeness", 17169, ("Completeness", "valid representation", "complete number"), ()),
    ("page560_notes_distribution", 17173, ("different number representations", "different distributions", "Maximal compression"), ()),
    ("page560_notes_practical_boundary", 17175, ("Practical computing", "fixed length", "self-delimiting"), ()),
    ("page561_notes_application", 17178, ("Fibonacci encoding used in the main text", "length of the representation", "transcendental"), ()),
    ("pointer_encoding_context", 17234, ("self-delimiting representation", "encoded version", "purely nested sequence"), ()),
    ("sturmian_span", 17597, ("Block frequencies", "Sturmian type",), ()),
    ("sturmian_completion", 17599, ("page 916", "n^{th}", "irrational number"), ()),
    ("pi_difference_table_observer", 17760, ("Difference tables and polynomials", "additive cellular automaton", "digits of"), ()),
    ("power_ca_locality", 17849, ("Power cellular automata", "local cellular automaton operation", "invertible"), ()),
    ("negative_base_locality", 17851, ("locality in negative bases", "k = -6", "four neighboring cells"), ()),
    ("power_ca_behavior", 17853, ("class 3 systems", "small changes in initial conditions"), ()),
    ("particular_power_digit_cost", 17863, ("particular digit", "t Log[t]^2", "base k"), ()),
    ("base_conversion_cost", 17865, ("particular base k digit", "converting to base k", "takes about t divisions"), ()),
    ("single_power_digit_boundary", 17874, ("single digit", "no way", "all the other digits"), ()),
    ("power_algorithm_context", 17855, ("Computing powers", "repeated squaring", "IntegerDigits"), ()),
    ("bit_carrier_pluralism", 18211, ("bits of data", "represent information of absolutely any kind", "Numbers"), ()),
    ("multicolor_encoding_context", 18339, ("More colors", "three colors", "two colors"), ()),
    ("fibonacci_block_encoding", 18348, ("coding theory", "digit sequences", "Fibonacci number system"), ()),
    ("number_classification", 13136, ("Number classification", "undecidable", "same number"), ()),
    ("noncomputable_definition", 17101, ("formal descriptions", "algorithmically random", "Chaitin"), ()),
    ("noncomputable_coefficients", 19058, ("nth digit", "far from being computable", "halting problem"), ()),
    ("real_cf_encoding", 19066, ("real number x", "represented as a set of integers"), ()),
    ("real_cf_encoding_formula", 19068, ("ContinuedFraction[x]", "FoldList"), ()),
    ("real_encoding_cardinality", 19070, ("not finite", "Cantor's diagonal argument", "RealDigits[list]"), ()),
    ("infinite_configuration_digits", 19072, ("infinite configurations", "digit sequences of real numbers", "Cantor set"), ()),
    ("computable_real_definition", 19074, ("computable real numbers", "n<sup>th</sup> digit", "finite number of steps"), ()),
    ("noncomputable_reals_boundary", 19076, ("non-computable reals", "successive digits", "infinitely long time"), ()),
    ("diagonal_digit_boundary", 19078, ("Diagonal arguments", "nth base 2 digit", "1 - f[n, n]"), ()),
    ("continuous_digit_computation", 19080, ("Continuous computation", "real numbers in terms of digits", "discrete processes"), ()),
    ("arbitrary_real_register_boundary", 19082, ("register machines", "arbitrary real numbers", "primitive operations"), ()),
    ("continuous_program_boundary", 19084, ("continuous data", "programs themselves normally remain discrete", "finite formula"), ()),
    ("oracle_initial_condition_boundary", 19086, ("absolutely any digit sequence", "table for an oracle", "must address"), ()),
    ("constructible_real_boundary", 19087, ("Constructible reals", "successive digits", "mechanical processes"), ()),
    ("constructible_real_completion", 19089, ("robotics", "algebraic numbers", "degree 4"), ()),
    ("precision_resource_boundary", 19185, ("n-digit numbers", "pi", "n-digit precision", "bit operations"), ()),
    ("iterative_precision_resource", 19187, ("iterative procedure", "Log[n] steps", "n digits", "NIntegrate"), ()),
    ("bit_extraction_evaluator", 19194, ("extracts the digit", "base 2 digit sequence"), ()),
    ("short_computation_context", 19190, ("Short computations", "Some properties include"), ()),
    ("undecidability_digit_analogy", 19244, ("most numbers cannot be computable", "digit sequence of a real number"), ()),
    ("np_representation_context", 19494, ("NP completeness", "problems known to be NP-complete"), ()),
    ("complexity_representation_boundary", 19509, ("base 2 digit sequences", "not", "unary"), ()),
    ("resource_representation_boundary", 19526, ("appropriate number representations", "asymptotic growth rates", "polynomial time"), ()),
    ("resource_representation_completion", 19528, ("halting times", "undecidable", "P = NP"), ()),
    ("number_generalization_history", 20117, ("Generalization in mathematics", "positive integers", "decimals", "complex numbers"), ()),
    (
        "representation_pluralism",
        20507,
        ("Greek and Roman number systems", "base-10 positional notation", "base-2 positional notation", "many other quite different ways to represent numbers"),
        (),
    ),
    ("representation_pluralism_heading", 20505, ("Mathematical notation", "history and context", "not", "unique"), ()),
    ("minimal_ca_sequence_context", 20586, ("Minimal cellular automata for sequences", "simplest cellular automaton", "center column"), ()),
    ("minimal_ca_search_scope", 20590, ("all separations up to 15", "complex 350-step transient"), ()),
    ("minimal_ca_digit_boundary", 20592, ("powers of two", "digits of", "concatenation sequences"), ()),
    ("billiard_cf_relation", 14923, ("Billiards", "continued fraction form", "substitution systems"), ()),
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
    "BOOK654->656:pi-complexity sentence is interrupted by extraction whitespace",
    "BOOK1681:caption promises 4000 decimal digits but extraction contains only a prefix",
    "BOOK1683:caption promises 4000 binary digits but extraction is short and has extra separators",
    "BOOK1733:extracted sqrt-two binary row agrees for 32 zero-based bits then diverges from exact isqrt replay",
    "BOOK1740:square-root prose is duplicated and truncated at base-s phrase",
    "BOOK1746:printed If expression uses malformed brace syntax",
    "BOOK1750->1774:sentence is interrupted by page extraction and resumes later",
    "BOOK1782:base-two nested construction is runaway and truncated",
    "BOOK1798->1830:sentence is interrupted by table extraction and resumes later",
    "BOOK1852->1858:continued-fraction sentence is interrupted by a raster and caption",
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
    "BOOK11256->11260:CA digit-map sentence is interrupted by an unrelated Page 26 note",
    "BOOK17597->17599:Sturmian block-frequency sentence is split across extraction rows",
    "BOOK19087->19089:constructible-real sentence is split across extraction rows",
    "BOOK19526->19528:P-versus-NP sentence is split across extraction rows",
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
    "positional-source:whole and fractional encoders expose quotient or residual iteration and explicit inverses",
    "positional-canonical:terminating rational uses infinite zero tail not eventual base-minus-one tail",
    "representation-relations:unary length-prefixed binary-coded-base3 Fibonacci negative-base non-power Zeckendorff and multiplicative forms are scoped siblings not strict presets",
    "representation-codec-properties:self-delimitation uniqueness length completeness and distribution are typed invariants or observers",
    "continued-fraction:integer coefficients are unbounded",
    "continued-fraction-canonical:finite tail has final coefficient greater than one when length exceeds one",
    "continued-fraction-seam:arbitrary irrational h exposes signed Floor[h] integer part and substitution rules from remaining coefficients",
    "finite-prefix:lossy query result and never the complete exact value",
    "rendering:digit row walk histogram and coefficient plots are observers",
    "work-long-division:explicit discrete t-plus-0D exact remainder configuration",
    "work-long-division:Self read closed quotient-remainder rule atomic same-locus assignment",
    "work-square-root:explicit discrete t-plus-0D Product-r-s configuration",
    "work-square-root:both product components update atomically from one old snapshot",
    "work-square-root:literal source profile is integer-safe; rational repair is a sibling",
    "work-continued-fraction:explicit exact scalar fractional-reciprocal iteration with finite completion",
    "direct-access:nth coefficient evaluator need not fabricate preceding append events",
    "direct-access:some evaluator methods still require a whole prefix and return a typed resource outcome",
    "computability:exact definition alone does not guarantee executable coefficient access",
    "computability:arbitrary real carriers primitives and oracle-like initial digits require explicit constructive authority",
    "cardinality:infinite digit carriers are not finitely stored configurations without a constructive representation",
    "source-strength:finite-precision overwhelming probability is not exact certification",
    "architecture:no ConstantDigitsState T40 update executor runner branch family dispatch or callback",
    "architecture:optional work algorithms reuse existing SimplePrograms axes and branch-free runner",
    "architecture:no hidden remainder residual prefix cache precision state or CAS object",
    "architecture:representation diversity changes typed codecs and invariants not the shared SimpleProgram executor",
    "relation:realization certificate connects a work trace to a denotation query",
    "boundary:T36 supplies positional codecs without importing its transition identity",
    "boundary:T37 append state is not universal because direct nth access exists",
    "boundary:T41 supplies immutable closed-definition and query responsibilities",
    "boundary:T42 consumes coefficients but owns substitution evolution",
    "boundary:T43 scalar feedback maps can realize positional and continued-fraction queries",
    "boundary:T42 substitution and Sturmian observers consume digit or continued-fraction results without becoming T40 execution",
    "domain-vocabulary:DOMAIN means t plus dimensional task support not CA family",
    "source-epistemic:catalog taxonomy and atlas supply vocabulary rather than primary mechanics",
    "source-closure:Book-wide direct vocabulary and fixed Index rows are independently dispositioned",
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
SPLIT_RELATION_SUMMARY_OWNERS = {
    654: "CHAPTERS/2-The-Crucial-Experiment/The-Crucial-Experiment.md:237",
    656: "CHAPTERS/2-The-Crucial-Experiment/The-Crucial-Experiment.md:237",
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
    "Q13": (6, 6, 0, "0e8859ae1a47583384c73a09041cd08017b6dda9e7380a7746cae06dfa814ec3"),
    "Q14": (12, 0, 12, "7b99c1393251c1d6e507801a46576a77d9b33a78557f42bd2e29ffc26c5ff277"),
    "Q15": (3, 3, 0, "29e023f7db02bec1f2a16113a10f2ad22d45f9741ac3563d630c38b4ae641240"),
    "Q16": (60, 60, 0, "166c98e3619923d10930515737765f6b29301b597ac8b3688877ead3bdde96a8"),
    "Q17": (4, 4, 0, "8a4e0a5a0bdb3f5e00e29d2c34e66980cec3634c02ac67dbee9b0c5d2bc8c8fd"),
    "Q18": (26, 17, 9, "b63742f587b4fd1f241d17f717fa66ce7964997b2d5dd4136ba8629aac69aa88"),
    "Q19": (5, 0, 5, "dfd6b9bb5fb0d37bb9dec4176afc40f7273b06a1b7b2d732a66ffea2d3b5f71f"),
}
EXPECTED_QUERY_PATTERNS = (
    20,
    "4e6a271f92cfb7a83deb91a1791e0eada0d57c78b7c4a62f304bc7df5d91e2c5",
)
EXPECTED_SET = {
    "union": (213, "632a414af1ed9ee8fea00da0020def00f439d6b2b41853e537e7148b637754a3"),
    "pre_index": (158, "3ebdbc3027ab657e5ee2f70cdb709b74f6f6edae432226ab10634c84b770b7a5"),
    "index_candidates": (55, "f42d657863bef3a638029d7994ba498468a7bfb857f99a3249a08df1a6b2f3ae"),
    "query_native": (46, "90c5667940c7b23109fec16cce632cd493d64aa5bf3c6eeda290417cee80093d"),
    "query_relation": (86, "e34233b994c79cfa0d82a8a36d0d2b3d3f3d4da43987e937957b6600e203d96d"),
    "query_control": (12, "c3063ea0a806932d6d79c9fc345941c1eb947d4e7b94e08c265a05af639dcb3a"),
    "excluded": (14, "8513c01e9157208b3f8a2db0957813529069c650e41fdc469087c6a5000ff4d5"),
    "native": (169, "eba1f729ab1ed14b6809c181e74ac86b64a363c0bcecb684f7cdbdad8f76ca2b"),
    "relation": (238, "a52c2e003b4c93224dc5d4304863422ae9185c92a9262a7f80f1ad402e151aed"),
    "control": (40, "c3c30e3389017ed41fa713013e72ed3e1cf08e09bfe43d77f896757593e0facb"),
    "retained": (447, "e4816e3cb8dda0717df150d8f512879e5b2ae5b9c0ac6e4330dc681a10be9caf"),
    "retained_query": (144, "5e548024db44e16cade35bc4b2ce14d881f5919a1d18770eed633abd91efbb55"),
    "continuations": (303, "8fcedc50130861ee4cfd626e009df451ba6d30763e59fb2262b88e013945ddd5"),
}
EXPECTED_EXCLUDED_CLASS = {
    "name_collision": (1, "0a5b046d07f6f971b7776de682f57c5b9cdc8fa060db7ef59de82e721c8098f4"),
    "generic_algorithm_cross_reference": (3, "0af5fb1f1971b936e8052cc34fe7605caf6f6916a28992ff9485914a39d55704"),
    "sibling_asset_observer": (10, "d85a02abfd4febbc284b9e74bc18a42b8ef2c5f929f107d0db2e24fea6cc5659"),
}
EXPECTED_BOOK_BROAD = {
    "candidate": (309, "f8616458a4770352e42c8f8aeaa4d27033a6758e048885e88547ea044d3a90fc"),
    "pre_index": (242, "119434cf29172056756ec9b395ad8626004b5f405697eb9a4f92b562b507001e"),
    "index": (67, "cfbcf2b55bf813269371bcd9fc210c3f30600eb3e087ae127a128e191d16555b"),
    "retained": (110, "47066b70839f1acb79870788aef8ac403186192bd900b5e11bb4e829f0f50058"),
    "query_excluded": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "broad_excluded": (132, "b829a526b8ff53a1f4f8d86bd0b515e5ff885e6fb2c1be74c829261b9e94d942"),
}
EXPECTED_BOOK_BROAD_PATTERN_DIGEST = (
    "989b777b2985b7f3f604f439214479145fe87f2e8d2b3791b8298ee63b830815"
)
EXPECTED_BOOK_BROAD_EXCLUSION_CLASS = {
    "chaos-physical-sampling-observers": (16, "3db508b06d1f1f938318bd3488d3615471e3066d6fa4cbf95e4b4710bbef0b07"),
    "compression-crypto-computation-siblings": (28, "c0d5666d150ddc0598465616cf67de93f344c72c859a1fec01472ff514508833"),
    "downstream-philosophical-compression-siblings": (8, "a8337d93180c92a8529217ca3041701463ff64c0e85f76444df777431bddcdac"),
    "generic-complexity-cost-analogies": (2, "9153b98abebd3edccfca9c2be550748a98bba220bc57f63b576fa353b9bb6583"),
    "other-simple-program-coordinate-encodings": (3, "cda34754ceb647e6a204884d98188a6b9fd64a36821b92be88fcb2dde6783f0e"),
    "rule-machine-code-carriers": (7, "bb61d745deb05dc59c4822f4cc3f2c4d89fc79714ae559328f08c254dc4548e1"),
    "sibling-type-notes-before-t40": (13, "4f0b383579ada8269eb8fa030fe576960b67422e977cf9590c243921690ccd87"),
    "t36-t37-number-evolution-siblings": (19, "60cf2d6e7513e3ba54ff6c462e8d706a4d03d8e09ff6c6f5edacfba34b53927a"),
    "t43-ca-sibling-notes": (19, "24ba31ee9a1b0b25770ced215099ee474313a754b021d7ca288d994c3047121d"),
    "t43-iterated-map-work-siblings": (17, "16914fa3ace33bdb24bbced53ecd8e8fd85f27f0a8d75d3fa1511e7a0e5ee183"),
}
EXPECTED_BOOK_BROAD_DISPOSITIONS = (
    309,
    "2e8dcd55c14c61f241089816969a4f96a280b7c380a8403d46d7331a15424865",
)
EXPECTED_BOOK_BROAD_EXCLUSION_RECORDS = (
    132,
    "47ecf4cab81624f99c2aaf7840f62cd59dfc56d7bfa9fc40ff272b4509cb8b97",
)
EXPECTED_SOURCE_SPAN_EXCLUSION_RECORDS = (
    3,
    "27f2208c664055bcb55380b1879a6679a020b7e76eda7e9ce97ad00a1f21a37d",
)
EXPECTED_INDEX_CLASS = {
    "native": (30, "3b16acd55987dcf28f7ed4b681251e34c2e0bc176b3cb6b255450b18f735f181"),
    "relation": (102, "e0626897cab06433d60501dedd65eda889262fe2f0527c2e3359e063648cb88d"),
    "control": (4, "3c1e78895b082a66f1240b6708a78c9b6847b7a3f0f26a9cff0ed0b37603f863"),
}
EXPECTED_INDEX_CONTENT = (
    897,
    "cfd508d5257c960ee983107dbf36edb3956358cbf26a3f480ee2ecf28aca75fe",
)
EXPECTED_INDEX_BOUNDS = (20826, 20828, 22456, 22458)
EXPECTED_INDEX_BOUNDARY_TEXT = ("#### Index", "#### Colophon")
EXPECTED_INDEX_SEMANTIC_UNIVERSE = (
    136,
    "87390448e04cd950b9841b8ee761af9d467d7c67882266dacde1964e6e72be68",
)
EXPECTED_INDEX_QUERY_MISSES = (
    81,
    "c0c0d5c752cc8d8d00b46839f7e0737a34374868f5c80a28a6012d22782d916d",
)
EXPECTED_INDEX_BROAD_VOCABULARY = (
    114,
    "8406f1b9b58f72983c438d2e62a438c58d0305f13884c19e45c2df706e113949",
)
EXPECTED_INDEX_HOSTILE_AUDIT_CANDIDATES = (
    70,
    "a3d65822945b0a32facb4e88d24f0ad7372e1a4ba1a62cc8594881f101316607",
)
EXPECTED_INDEX_AUDIT_CANDIDATES = (
    150,
    "3b82a6d1c983df5264648ec31b608cb3bcc9160ee8c56c84e153aadf532bdc2d",
)
EXPECTED_INDEX_BROAD_PATTERN_DIGEST = (
    "7cecd1128c1cc938a264fa54fff531e757381528f63885c86fdc7e80ac8bece7"
)
EXPECTED_INDEX_DISPOSITION = {
    "native": EXPECTED_INDEX_CLASS["native"],
    "relation": EXPECTED_INDEX_CLASS["relation"],
    "control": EXPECTED_INDEX_CLASS["control"],
    "excluded": (16, "0cba561e4c20a6bac1b7ed2d58c255b8250b6fc5bb4da0449c382b50247b0411"),
    "unrelated": (745, "bd65cb29b27591d90e36016b12bdd8deb29be86d261e3beb80e4986a40c9985c"),
}
EXPECTED_STRICT_MAIN_PARTITION = {
    "native": (102, "bd76954762c925f2ecf6bf0fa97d9c15db19d598a297a9c56d74e12d1dc41d59"),
    "relation": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "control": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "excluded": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "structural": (15, "8b83af3e32debd18eab8f148b46b187ff2ca50001b037a5d5cd71f81989c5e54"),
    "content": (117, "6c39a18a84e5186f11f8082c2bc5380846269c7f67b62d759b9fea0bea0ea2a9"),
}
EXPECTED_STRICT_NOTES_BOUNDS = (12921, 13144)
EXPECTED_STRICT_NOTES_PARTITION = {
    "native": (58, "4ab54e30b13566048a6792fb4a6c4927d9eeeee02d8fa8a48329510ddc4ef8c3"),
    "relation": (67, "65468ee428fd50d0ef083d74016eb81caa7d8c97510b04300b6d50065769216e"),
    "control": (1, "71887428c764ac67b3bd6ce9f4212ff7e7fe6803e507b5b11345d7c6a6c95a1e"),
    "content": (126, "879d9d3e52bf0619b461288ee403d1dea7e6f75ad95648bfa12bcc3acac50e68"),
}
EXPECTED_IMAGE_PARTITION = {
    "native": (11, "45fe870caa33fa2cc0b702a8158564f987fb186a1742f1bbafc940cf8c738894"),
    "relation": (40, "02c92a8293eff7a00d1c4585a714fbbd07f7c2faa7a572b250b84437a4b90c63"),
    "control": (2, "b93adf13ddfe98860b89db8d689a2003e724ccb0eacac6e941e2155ad73e3bf8"),
    "governed": (53, "08c383d1c08ad614b047e1084f806d2807a159266a62555a55915e1ba33b53f5"),
    "excluded": (10, "d85a02abfd4febbc284b9e74bc18a42b8ef2c5f929f107d0db2e24fea6cc5659"),
    "candidate": (63, "e4094d8d30489b7029c902e9b69df6403915cfb776faa5723ebfe97d3d1b94b5"),
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
    63,
    "4685ebad9a58b1cc8082b4a03118ad1bcd1780706bceba2bf29184cd8df05b10",
)
EXPECTED_SOURCE_SEMANTIC_GUARDS = (
    139,
    "53d520ca9e8891eb17387fcfb24ffcaa5b0065f65789c3bf3d333147699ae478",
)
EXPECTED_SOURCE_DEFECT_GUARDS = (
    30,
    "9e1ecf0bd292fcbbde1a85814c65e9a7d505553db0343c4a4254262ab6d2c630",
)
EXPECTED_RECORDS = {
    "book_broad_dispositions": EXPECTED_BOOK_BROAD_DISPOSITIONS,
    "book_broad_exclusions": EXPECTED_BOOK_BROAD_EXCLUSION_RECORDS,
    "source_span_exclusions": EXPECTED_SOURCE_SPAN_EXCLUSION_RECORDS,
    "excluded_line_hashes": (14, "a18d47a88517e8ce233668933985276805f8e67824cee99512dcfceaa4bda69e"),
    "index_guards": (136, "5f323a3ad491e43ecaef6ffdd43648a9693d73fbd866be8cb56801139874b3df"),
    "index_excluded_guards": (16, "473fe5dcba32ca177fe1913efb1879f35f72492ee7fd3b2f9fe231025c20382b"),
    "index_dispositions": (897, "70d3496248542a9dcd3e02b6b6f9d472925993e292993b754a69a30053d30d2d"),
    "index_sentinels": (8, "129bc6a4ef7cc76b5020676e603a2b5621ef56354b8ca2cd2fb4361938791710"),
    "strict_main_dispositions": (117, "94bed33e54122c19903a478a562a10d69491890aef04978d417bb53b3b13db91"),
    "strict_notes_dispositions": (126, "3d4cb793dae2cfa4df4d14bb4070efeb32ccba45ebfc221234700c2734f645aa"),
    "semantic_guards": EXPECTED_SOURCE_SEMANTIC_GUARDS,
    "auxiliary_guards": (8, "bb1c06175c4a5856879b75936917159d7125f734ad6350cc26f618cb2da23b18"),
    "source_defects": EXPECTED_SOURCE_DEFECT_GUARDS,
    "source_model": (42, "1db5560d5effa43a81fcb3c35069ce514a34ee0041061ea8923b0a8c861c680f"),
    "image_roles": (63, "56e983f339a2df1d808ac56a43243ba1151756c845babae4a546472034d02ce7"),
    "image_assembly_boundaries": (18, "4c39bfee02a703db49afba0d7e75c8a63989e86aa3013cb9271052438318d2c7"),
    "split_omissions": (89, "0c3dc82ba4879e60782fa0459e4e12768e8e48f4b950474bdc731f382fab6c8f"),
    "split_boundary_witnesses": (7, "c32f23773dbe2707c96bde64ea3fd95445e3ff6efd2bb809718c22d28b9a9884"),
}
EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
EXPECTED_SPLIT_MANIFEST_DIGEST = "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"
EXPECTED_SPLIT_CROSSWALK = (
    1359,
    "ec95b7239b33d91e630888ed9fd428917ebcbe1354b1a326ff2887fbc2a74c9e",
)
EXPECTED_SPLIT_CLASSES = {
    "EXACT": (
        1175,
        "788095e3a5f2088f3bf9dbd85f90c40352966d44814463b9bcfa598408c493c5",
        "84af9621105e1fa7b2ce96ce25dc96693a5e291aa156f7e1863501f4c095c9d3",
    ),
    "IMAGE_BASENAME": (
        51,
        "fd395075505951a4bbdd0fa5bcc4b5c41b572f099df4807479a5413dfe79b242",
        "eef42970c64c5f758a6124a2b4a5273c060bdd4215ac424f0ab106ab08f1c4f1",
    ),
    "NORMALIZED": (
        28,
        "196009b2427d2d2b8d10096203710f1aa99fd36078ac2432bfdb29b0880810ae",
        "84aafc89781759d2d49c621657a831a8fff50b0316a8aed6fda6d17f98b6d672",
    ),
    "SUMMARY": (
        16,
        "9e5d9bc769625a2ebf160fdd1e83a4453c9e1e4865c12a11775ac227a5cfd4f8",
        "e6e3b8242849932c3170bc4b7da916d26933483d72e2ce69e2142b2b39c6a79e",
    ),
    "OMITTED": (
        89,
        "a2e7ef27e19c1dd7ca657f20b806754966e3a6d396a2dcbf864aa2a491d399b1",
        "0251161e7ee25fcf11bab72f0f7a389ac4bed5b2daceefb63a78b541b1e60748",
    ),
}
EXPECTED_SPLIT_NORMALIZED_MINIMUM = 0.995885
EXPECTED_LOGIC_RECORDS = (
    7,
    "d525310251895f506ca06d964ba736dd53ab659e07fed14d7fbe5422b1648754",
)
EXPECTED_AUDIT_DIGEST = "7bd67422250b13fa3077614e4e0637eb6bc2237627140dc8192961900b31ae9c"


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
    if line_no in {998, 1008, 1014}:
        return (
            "CHAPTERS/3-The-World-of-Simple-Programs/"
            f"The-World-of-Simple-Programs.md:{line_no - 683}"
        )
    if line_no == 1449:
        return (
            "CHAPTERS/4-Systems-Based-on-Numbers/"
            "Systems-Based-on-Numbers.md:53"
        )
    if line_no in SPLIT_MAIN_DIRECT_OWNERS:
        return SPLIT_MAIN_DIRECT_OWNERS[line_no]
    if line_no in SPLIT_MAIN_SUMMARY_OWNERS:
        return SPLIT_MAIN_SUMMARY_OWNERS[line_no]
    if line_no in SPLIT_RELATION_SUMMARY_OWNERS:
        return SPLIT_RELATION_SUMMARY_OWNERS[line_no]
    if 1846 <= line_no <= 1858:
        return (
            "CHAPTERS/4-Systems-Based-on-Numbers/"
            f"Systems-Based-on-Numbers.md:{line_no - 1541}"
        )
    if 6766 <= line_no <= 6782:
        return (
            "CHAPTERS/10-Processes-of-Perception-and-Analysis/"
            f"Processes-of-Perception-and-Analysis.md:{line_no - 6587}"
        )
    if line_no == 7116:
        return (
            "CHAPTERS/10-Processes-of-Perception-and-Analysis/"
            "Processes-of-Perception-and-Analysis.md:527"
        )
    if line_no == 9246:
        return (
            "CHAPTERS/12-The-Principle-of-Computational-Equivalence/"
            "The-Principle-of-Computational-Equivalence.md:629"
        )
    if 11250 <= line_no <= 11260 or 11531 <= line_no <= 11536:
        return (
            "CHAPTERS/12-The-Principle-of-Computational-Equivalence/"
            "The-Principle-of-Computational-Equivalence.md:"
            f"{line_no - 8619}"
        )
    if 12194 <= line_no <= 12206:
        return f"BACK-MATTER/Index/Index.md:{line_no - 12089}"
    if 12919 <= line_no <= 13146:
        return f"BACK-MATTER/Index/Index.md:{line_no - 12097}"
    if line_no == 13219:
        return f"BACK-MATTER/Index/Index.md:{line_no - 12097}"
    if line_no in {
        14170,
        14172,
        14174,
        14176,
        14468,
        14923,
        14925,
        14927,
        14929,
        14931,
        14933,
        15517,
        17101,
        17105,
        17107,
        17236,
    } or 17130 <= line_no <= 17234:
        return f"BACK-MATTER/Index/Index.md:{line_no - 12099}"
    if line_no >= 17597:
        return f"BACK-MATTER/Colophon/Colophon.md:{line_no - 17443}"
    chapter_12 = {11260: 2641, 11531: 2912}
    if line_no in chapter_12:
        return (
            "CHAPTERS/12-The-Principle-of-Computational-Equivalence/"
            "The-Principle-of-Computational-Equivalence.md:"
            f"{chapter_12[line_no]}"
        )
    if 12503 <= line_no <= 12557:
        return f"BACK-MATTER/Index/Index.md:{line_no - 12097}"
    if line_no == 12569:
        return "BACK-MATTER/Index/Index.md:472"
    if 12587 <= line_no <= 12595:
        return f"BACK-MATTER/Index/Index.md:{line_no - 12097}"
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

    strict_notes_actual_content = {
        number
        for number in range(STRICT_NOTES_FIRST_LINE, STRICT_NOTES_LAST_LINE + 1)
        if at(number).strip()
    }
    strict_notes_union = set().union(*STRICT_NOTES_DISPOSITION.values())
    strict_notes_overlap = (
        sum(map(len, STRICT_NOTES_DISPOSITION.values())) - len(strict_notes_union)
    )
    strict_notes_unresolved = (
        len(strict_notes_actual_content ^ strict_notes_union) + strict_notes_overlap
    )
    strict_notes_sets = {
        **STRICT_NOTES_DISPOSITION,
        "content": STRICT_NOTES_CONTENT,
    }
    strict_notes_ok = (
        (STRICT_NOTES_FIRST_LINE, STRICT_NOTES_LAST_LINE)
        == EXPECTED_STRICT_NOTES_BOUNDS
        and set(strict_notes_sets) == set(EXPECTED_STRICT_NOTES_PARTITION)
        and strict_notes_actual_content == strict_notes_union
        and strict_notes_union == set(STRICT_NOTES_CONTENT)
        and strict_notes_overlap == 0
        and STRICT_NOTES_CONTENT <= RETAINED
    )
    for name, values in strict_notes_sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_STRICT_NOTES_PARTITION.get(name)
        strict_notes_ok &= good
        check("strict_notes_" + name, good, *actual)
    check("strict_notes_partition", strict_notes_ok, strict_notes_unresolved)

    index_actual_content = {
        number
        for number in range(INDEX_CONTENT_FIRST_LINE, INDEX_CONTENT_LAST_LINE + 1)
        if at(number).strip()
    }
    index_broad_candidates = {
        number
        for number in index_actual_content
        if re.search(INDEX_BROAD_VOCABULARY_PATTERN, at(number), re.IGNORECASE)
    }
    index_audit_candidates = index_broad_candidates | set(INDEX_HOSTILE_AUDIT_CANDIDATES)
    index_unrelated = index_actual_content - set(INDEX_ROUTED) - set(INDEX_EXCLUDED)
    index_disposition = {
        **INDEX_CLASS,
        "excluded": INDEX_EXCLUDED,
        "unrelated": frozenset(index_unrelated),
    }
    index_disposition_union = set().union(*index_disposition.values())
    index_disposition_overlap = (
        sum(map(len, index_disposition.values())) - len(index_disposition_union)
    )
    index_candidate_unexplained = (
        index_audit_candidates - set(INDEX_ROUTED) - set(INDEX_EXCLUDED)
    )
    index_query_misses = set(INDEX_SEMANTIC_UNIVERSE) - index_candidates
    index_unresolved = (
        len(index_actual_content ^ index_disposition_union)
        + index_disposition_overlap
        + len(index_candidate_unexplained)
    )
    index_content_actual = (len(index_actual_content), digest(index_actual_content))
    index_bounds_actual = (
        INDEX_FIRST_LINE,
        INDEX_CONTENT_FIRST_LINE,
        INDEX_CONTENT_LAST_LINE,
        22458,
    )
    index_boundary_text_actual = (at(INDEX_FIRST_LINE), at(22458))
    index_universe_actual = (
        len(INDEX_SEMANTIC_UNIVERSE),
        digest(INDEX_SEMANTIC_UNIVERSE),
    )
    index_miss_actual = (len(index_query_misses), digest(index_query_misses))
    index_broad_actual = (
        len(index_broad_candidates),
        newline_number_digest(index_broad_candidates),
    )
    index_hostile_actual = (
        len(INDEX_HOSTILE_AUDIT_CANDIDATES),
        digest(INDEX_HOSTILE_AUDIT_CANDIDATES),
    )
    index_audit_candidate_actual = (
        len(index_audit_candidates),
        digest(index_audit_candidates),
    )
    index_pattern_actual = digest_records({INDEX_BROAD_VOCABULARY_PATTERN})
    index_ok = (
        set(INDEX_CLASS) == set(EXPECTED_INDEX_CLASS)
        and frozenset().union(*INDEX_CLASS.values()) == INDEX_ROUTED
        and sum(map(len, INDEX_CLASS.values())) == len(INDEX_ROUTED)
        and not INDEX_ROUTED & INDEX_EXCLUDED
        and INDEX_SEMANTIC_UNIVERSE == INDEX_ROUTED
        and index_candidates <= set(INDEX_SEMANTIC_UNIVERSE)
        and index_actual_content == index_disposition_union
        and index_disposition_overlap == 0
        and not index_candidate_unexplained
        and index_bounds_actual == EXPECTED_INDEX_BOUNDS
        and index_boundary_text_actual == EXPECTED_INDEX_BOUNDARY_TEXT
        and index_content_actual == EXPECTED_INDEX_CONTENT
        and index_universe_actual == EXPECTED_INDEX_SEMANTIC_UNIVERSE
        and index_miss_actual == EXPECTED_INDEX_QUERY_MISSES
        and index_broad_actual == EXPECTED_INDEX_BROAD_VOCABULARY
        and index_hostile_actual == EXPECTED_INDEX_HOSTILE_AUDIT_CANDIDATES
        and index_audit_candidate_actual == EXPECTED_INDEX_AUDIT_CANDIDATES
        and index_pattern_actual == EXPECTED_INDEX_BROAD_PATTERN_DIGEST
    )
    check("index_bounds", index_bounds_actual == EXPECTED_INDEX_BOUNDS, *index_bounds_actual)
    check(
        "index_boundary_text",
        index_boundary_text_actual == EXPECTED_INDEX_BOUNDARY_TEXT,
        *index_boundary_text_actual,
    )
    check("index_content", index_content_actual == EXPECTED_INDEX_CONTENT, *index_content_actual)
    check("index_semantic_universe", index_universe_actual == EXPECTED_INDEX_SEMANTIC_UNIVERSE, *index_universe_actual)
    check("index_query_misses", index_miss_actual == EXPECTED_INDEX_QUERY_MISSES, *index_miss_actual)
    check("index_broad_vocabulary", index_broad_actual == EXPECTED_INDEX_BROAD_VOCABULARY, *index_broad_actual)
    check("index_hostile_candidates", index_hostile_actual == EXPECTED_INDEX_HOSTILE_AUDIT_CANDIDATES, *index_hostile_actual)
    check("index_audit_candidates", index_audit_candidate_actual == EXPECTED_INDEX_AUDIT_CANDIDATES, *index_audit_candidate_actual)
    check("index_broad_pattern", index_pattern_actual == EXPECTED_INDEX_BROAD_PATTERN_DIGEST, index_pattern_actual)
    for name, values in INDEX_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_INDEX_CLASS.get(name)
        index_ok &= good
        check("index_" + name, good, *actual)
    index_records, index_guards_ok = occurrence_records(INDEX_ENTRY_GUARDS, lines)
    index_excluded_records, index_excluded_guards_ok = occurrence_records(
        INDEX_EXCLUDED_GUARDS, lines
    )
    sentinel_records, sentinels_ok = occurrence_records(INDEX_FLATTENING_SENTINELS, lines)
    index_ok &= (
        set(INDEX_ENTRY_GUARDS) == set(INDEX_ROUTED)
        and set(INDEX_EXCLUDED_GUARDS) == set(INDEX_EXCLUDED)
        and set(INDEX_FLATTENING_SENTINELS) <= set(INDEX_ROUTED)
        and index_guards_ok
        and index_excluded_guards_ok
        and sentinels_ok
    )
    for name, values in index_disposition.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_INDEX_DISPOSITION.get(name)
        index_ok &= good
        check("index_disposition_" + name, good, *actual)
    check(
        "index_candidate_closure",
        not index_candidate_unexplained,
        len(index_candidate_unexplained),
    )
    check("index_partition", index_ok, index_unresolved)

    book_broad_candidates = {
        number
        for number, line in enumerate(lines, 1)
        if re.search(BOOK_BROAD_VOCABULARY_PATTERN, line, re.IGNORECASE)
    }
    book_broad_pre_index = {
        number for number in book_broad_candidates if number < INDEX_FIRST_LINE
    }
    book_broad_index = book_broad_candidates - book_broad_pre_index
    book_broad_sets = {
        "candidate": book_broad_candidates,
        "pre_index": book_broad_pre_index,
        "index": book_broad_index,
        "retained": book_broad_candidates & set(RETAINED),
        "query_excluded": book_broad_candidates & set(EXCLUDED),
        "broad_excluded": book_broad_candidates & set(BOOK_BROAD_EXCLUDED),
    }
    book_broad_pre_partition = (
        NATIVE_EVIDENCE,
        RELATION_EVIDENCE,
        CONTROL_EVIDENCE,
        EXCLUDED,
        BOOK_BROAD_EXCLUDED,
    )
    book_broad_pre_union = set().union(
        *(set(values) & book_broad_pre_index for values in book_broad_pre_partition)
    )
    book_broad_pre_overlap = sum(
        len(set(values) & book_broad_pre_index)
        for values in book_broad_pre_partition
    ) - len(book_broad_pre_union)
    book_broad_unexplained = (
        book_broad_pre_index - book_broad_pre_union
    ) | (book_broad_index - set(INDEX_ROUTED))
    book_broad_pattern_actual = digest_records({BOOK_BROAD_VOCABULARY_PATTERN})
    book_broad_ok = (
        set(book_broad_sets) == set(EXPECTED_BOOK_BROAD)
        and book_broad_pattern_actual == EXPECTED_BOOK_BROAD_PATTERN_DIGEST
        and set(BOOK_BROAD_EXCLUSION_CLASS)
        == set(EXPECTED_BOOK_BROAD_EXCLUSION_CLASS)
        and frozenset().union(*BOOK_BROAD_EXCLUSION_CLASS.values())
        == BOOK_BROAD_EXCLUDED
        and sum(map(len, BOOK_BROAD_EXCLUSION_CLASS.values()))
        == len(BOOK_BROAD_EXCLUDED)
        and book_broad_pre_union == book_broad_pre_index
        and book_broad_pre_overlap == 0
        and book_broad_index <= set(INDEX_ROUTED)
        and not book_broad_unexplained
        and not BOOK_BROAD_EXCLUDED & RETAINED
        and not BOOK_BROAD_EXCLUDED & EXCLUDED
    )
    for name, values in book_broad_sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_BOOK_BROAD.get(name)
        book_broad_ok &= good
        check("book_broad_" + name, good, *actual)
    for name, values in BOOK_BROAD_EXCLUSION_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_BOOK_BROAD_EXCLUSION_CLASS.get(name)
        book_broad_ok &= good
        check("book_broad_excluded_" + name, good, *actual)
    check(
        "book_broad_pattern",
        book_broad_pattern_actual == EXPECTED_BOOK_BROAD_PATTERN_DIGEST,
        book_broad_pattern_actual,
    )

    book_broad_roles: dict[int, str] = {}
    for role, values in (
        ("native", NATIVE_EVIDENCE),
        ("relation", RELATION_EVIDENCE),
        ("control", CONTROL_EVIDENCE),
        ("query-excluded", EXCLUDED),
        ("broad-excluded", BOOK_BROAD_EXCLUDED),
    ):
        for number in book_broad_pre_index & set(values):
            book_broad_roles[number] = role
    for role, values in index_disposition.items():
        for number in book_broad_index & set(values):
            book_broad_roles[number] = "index-" + role
    book_broad_disposition_records = {
        f"{book_broad_roles[number]}:{number}:"
        f"{hashlib.sha256(at(number).encode('utf-8')).hexdigest()}"
        for number in book_broad_candidates
        if number in book_broad_roles
    }
    book_broad_disposition_actual = (
        len(book_broad_disposition_records),
        digest_records(book_broad_disposition_records),
    )
    book_broad_ok &= (
        len(book_broad_roles) == len(book_broad_candidates)
        and book_broad_disposition_actual == EXPECTED_BOOK_BROAD_DISPOSITIONS
    )
    check(
        "book_broad_dispositions",
        book_broad_disposition_actual == EXPECTED_BOOK_BROAD_DISPOSITIONS,
        *book_broad_disposition_actual,
    )
    check("book_broad_closure", book_broad_ok, len(book_broad_unexplained))

    book_broad_exclusion_records = {
        f"{reason}:{number}:"
        f"{hashlib.sha256(at(number).encode('utf-8')).hexdigest()}"
        for reason, values in BOOK_BROAD_EXCLUSION_CLASS.items()
        for number in values
    }
    source_span_exclusion_records = {
        f"{reason}:{number}:"
        f"{hashlib.sha256(at(number).encode('utf-8')).hexdigest()}"
        for reason, values in SOURCE_SPAN_EXCLUSION_CLASS.items()
        for number in values
    }
    source_span_ok = (
        set(SOURCE_SPAN_EXCLUSION_GUARDS) == set(SOURCE_SPAN_EXCLUDED)
        and frozenset().union(*SOURCE_SPAN_EXCLUSION_CLASS.values())
        == SOURCE_SPAN_EXCLUDED
        and sum(map(len, SOURCE_SPAN_EXCLUSION_CLASS.values()))
        == len(SOURCE_SPAN_EXCLUDED)
        and not SOURCE_SPAN_EXCLUDED & RETAINED
        and not SOURCE_SPAN_EXCLUDED & EXCLUDED
        and all(
            all(needle in at(number) for needle in needles)
            for number, needles in SOURCE_SPAN_EXCLUSION_GUARDS.items()
        )
        and (
            len(book_broad_exclusion_records),
            digest_records(book_broad_exclusion_records),
        )
        == EXPECTED_BOOK_BROAD_EXCLUSION_RECORDS
        and (
            len(source_span_exclusion_records),
            digest_records(source_span_exclusion_records),
        )
        == EXPECTED_SOURCE_SPAN_EXCLUSION_RECORDS
    )
    check("source_span_exclusions", source_span_ok, len(SOURCE_SPAN_EXCLUDED))

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
    strict_notes_disposition_records = {
        f"{role}:{number}:{hashlib.sha256(at(number).encode('utf-8')).hexdigest()}"
        for role, values in STRICT_NOTES_DISPOSITION.items()
        for number in values
    }
    index_disposition_records = {
        f"{role}:{number}:{hashlib.sha256(at(number).encode('utf-8')).hexdigest()}"
        for role, values in index_disposition.items()
        for number in values
    }
    omission_records = {
        f"{number}:{reason}"
        for reason, values in SPLIT_OMISSION_GROUPS.items()
        for number in values
    }
    record_actuals = {
        "book_broad_dispositions": book_broad_disposition_actual,
        "book_broad_exclusions": (
            len(book_broad_exclusion_records),
            digest_records(book_broad_exclusion_records),
        ),
        "source_span_exclusions": (
            len(source_span_exclusion_records),
            digest_records(source_span_exclusion_records),
        ),
        "excluded_line_hashes": (len(excluded_hash_records), digest_records(excluded_hash_records)),
        "index_guards": (len(index_records), digest_records(index_records)),
        "index_excluded_guards": (
            len(index_excluded_records),
            digest_records(index_excluded_records),
        ),
        "index_dispositions": (
            len(index_disposition_records),
            digest_records(index_disposition_records),
        ),
        "index_sentinels": (len(sentinel_records), digest_records(sentinel_records)),
        "strict_main_dispositions": (
            len(strict_disposition_records),
            digest_records(strict_disposition_records),
        ),
        "strict_notes_dispositions": (
            len(strict_notes_disposition_records),
            digest_records(strict_notes_disposition_records),
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
        and book_broad_ok
        and source_span_ok
        and SOURCE_DEFECT_GUARD_RECORDS == frozenset(SOURCE_DEFECT_RECORDS)
        and len(SOURCE_DEFECT_RECORDS) == len(SOURCE_DEFECT_GUARD_RECORDS)
        and len(SOURCE_MODEL_RECORDS) == len(set(SOURCE_MODEL_RECORDS))
        and SPLIT_OMISSION_LINES <= (RETAINED | STRICT_MAIN_CONTENT)
        and len(omission_records) == len(SPLIT_OMISSION_LINES)
        and sum(map(len, SPLIT_OMISSION_GROUPS.values())) == len(SPLIT_OMISSION_LINES)
        and set(SPLIT_MAIN_SUMMARY_OWNERS) <= set(STRICT_MAIN_CONTENT)
        and set(SPLIT_RELATION_SUMMARY_OWNERS) <= set(RETAINED)
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
    independent_crosswalk_universe = STRICT_MAIN_CONTENT | frozenset(index_actual_content)
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
            if number in SPLIT_MAIN_SUMMARY_OWNERS or number in SPLIT_RELATION_SUMMARY_OWNERS:
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
        and set(SPLIT_MAIN_SUMMARY_OWNERS) | set(SPLIT_RELATION_SUMMARY_OWNERS)
        == class_lines["SUMMARY"]
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
        + len(book_broad_unexplained)
        + (len(book_broad_candidates) - len(book_broad_roles))
        + strict_unresolved
        + strict_notes_unresolved
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
        f"book-broad:{name}:{len(values)}:{digest(values)}"
        for name, values in book_broad_sets.items()
    } | {
        f"book-broad-excluded:{name}:{len(values)}:{digest(values)}"
        for name, values in BOOK_BROAD_EXCLUSION_CLASS.items()
    } | {
        f"record:{name}:{count}:{record_digest}"
        for name, (count, record_digest) in record_actuals.items()
    } | {
        f"strict:{name}:{len(values)}:{digest(values)}"
        for name, values in strict_sets.items()
    } | {
        f"strict-notes:{name}:{len(values)}:{digest(values)}"
        for name, values in strict_notes_sets.items()
    } | {
        f"index-class:{name}:{len(values)}:{digest(values)}"
        for name, values in INDEX_CLASS.items()
    } | {
        f"index-disposition:{name}:{len(values)}:{digest(values)}"
        for name, values in index_disposition.items()
    } | {
        f"index-bounds:{':'.join(map(str, index_bounds_actual))}",
        f"index-boundary-text:{index_boundary_text_actual[0]}:{index_boundary_text_actual[1]}",
        f"index-content:{index_content_actual[0]}:{index_content_actual[1]}",
        f"index-semantic:{index_universe_actual[0]}:{index_universe_actual[1]}",
        f"index-query-misses:{index_miss_actual[0]}:{index_miss_actual[1]}",
        f"index-broad:{index_broad_actual[0]}:{index_broad_actual[1]}",
        f"index-hostile:{index_hostile_actual[0]}:{index_hostile_actual[1]}",
        f"index-audit-candidates:{index_audit_candidate_actual[0]}:{index_audit_candidate_actual[1]}",
        f"index-pattern:{index_pattern_actual}",
        f"index-candidate-unexplained:{len(index_candidate_unexplained)}",
        f"book-broad-pattern:{book_broad_pattern_actual}",
        f"book-broad-dispositions:{book_broad_disposition_actual[0]}:{book_broad_disposition_actual[1]}",
        f"book-broad-unexplained:{len(book_broad_unexplained)}",
        f"strict-unresolved:{strict_unresolved}",
        f"strict-notes-unresolved:{strict_notes_unresolved}",
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
            "book_broad": {
                "candidate": len(book_broad_candidates),
                "excluded": len(BOOK_BROAD_EXCLUDED),
                "index": len(book_broad_index),
                "pre_index": len(book_broad_pre_index),
                "retained": len(book_broad_candidates & set(RETAINED)),
                "unresolved": len(book_broad_unexplained),
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
            "strict_notes": {
                "content": len(STRICT_NOTES_CONTENT),
                "digest": digest(STRICT_NOTES_CONTENT),
                "unresolved": strict_notes_unresolved,
            },
            "index": {
                "audit_candidates": len(index_audit_candidates),
                "broad_candidates": len(index_broad_candidates),
                "content": len(index_actual_content),
                "digest": digest(index_actual_content),
                "excluded": len(INDEX_EXCLUDED),
                "query_misses": len(index_query_misses),
                "relevant": len(INDEX_SEMANTIC_UNIVERSE),
                "unrelated": len(index_unrelated),
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
            f"book-broad={len(book_broad_candidates)}(pre/index="
            f"{len(book_broad_pre_index)}/{len(book_broad_index)},"
            f"retained/excluded={len(book_broad_candidates & set(RETAINED))}/"
            f"{len(BOOK_BROAD_EXCLUDED)},closure={len(book_broad_unexplained)})",
            f"retained={len(RETAINED)}",
            f"strict-main={len(STRICT_MAIN_CONTENT)}(N/S="
            f"{len(STRICT_MAIN_NATIVE)}/{len(STRICT_MAIN_STRUCTURAL)},closure={strict_unresolved})",
            f"strict-notes={len(STRICT_NOTES_CONTENT)}(N/R/C="
            f"{len(STRICT_NOTES_DISPOSITION['native'])}/"
            f"{len(STRICT_NOTES_DISPOSITION['relation'])}/"
            f"{len(STRICT_NOTES_DISPOSITION['control'])},"
            f"closure={strict_notes_unresolved})",
            f"index={len(index_actual_content)}(N/R/C/X/U="
            f"{len(INDEX_CLASS['native'])}/{len(INDEX_CLASS['relation'])}/"
            f"{len(INDEX_CLASS['control'])}/{len(INDEX_EXCLUDED)}/"
            f"{len(index_unrelated)},query-misses={len(index_query_misses)},"
            f"closure={index_unresolved})",
            f"images={len(GOVERNED_IMAGE_LINES)}(N/R/C="
            f"{len(NATIVE_IMAGE_LINES)}/{len(RELATION_IMAGE_LINES)}/{len(CONTROL_IMAGE_LINES)})",
            f"split={len(crosswalk_records)}",
            f"unresolved={unresolved_total}",
        )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
