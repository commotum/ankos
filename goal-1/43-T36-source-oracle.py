#!/usr/bin/env python3
"""Fail-closed primary-source audit for T36 digit-reversal arithmetic.

The oracle treats ``src/ca`` as the shared SimplePrograms substrate.  The
strict construction is a t+0D exact positive integer whose closed unary rule
encodes canonical base-2 digits, reverses that finite word, decodes it, and
adds the result.  Fixed-width and growing-width Notes variants are explicitly
tagged profiles; FFT, Walsh, and quasi-Monte-Carlo digit permutations are
relations rather than temporal reversal-add evolution.

Searches, line classifications, actual-Index routes, split-corpus joins, and
opaque image identities are frozen independently.  Raster pixels and damaged
Wolfram Language fragments are never promoted into mechanics.
"""

from __future__ import annotations

import hashlib
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path


if not __debug__:
    raise RuntimeError("T36 source oracle requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "ref/A-New-Kind-of-Science"
DEFAULT_BOOK = SOURCE_ROOT / "A-New-Kind-of-Science.md"
ATLAS = SOURCE_ROOT / "ANKoS-Atlas.md"
CATALOG = ROOT / "ref/notes/CA-Types.csv"
TAXONOMY = ROOT / "ref/notes/CA-Types.md"

INDEX_FIRST_LINE = 20826
EXPECTED_BOOK_LINES = 22498
EXPECTED_BOOK_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"
EXPECTED_ATLAS_SHA256 = "5ffab93f0007bbeb5da60af7cc08570f9a358c9f9f94e37c5e00f9fc0997bc8a"
EXPECTED_CATALOG_SHA256 = "26cef05af1155f80bc301900d2df95469a90de027ba860730519d25d096c2b73"
EXPECTED_TAXONOMY_SHA256 = "4c30fe079b2fb8f69e4c8c0dde3d59065227d4224cbe4b7693a17c0126cc3f1a"


# Redundant mechanics, formula, observer, relation, false-positive, and actual
# Index lanes.  Broad positional-code lanes are intentional; every pre-Index
# result is dispositioned below rather than silently filtered.
QUERIES = {
    "Q00": r"Digit-Reversal Arithmetic Systems?",
    "Q01": (
        r"write its base 2 digits in reverse order|"
        r"same rule as on the previous page, but now starting with the number 512|"
        r"Continuation of the pattern on the facing page, starting at the millionth step"
    ),
    "Q02": (
        r"digit sequences, then one sees complex patterns|"
        r"systems based on numbers there is usually no such locality|"
        r"carry.{0,80}propagate arbitrarily far|"
        r"details of underlying rules again do not seem to have a crucial effect|"
        r"lack of locality.{0,180}localized structures"
    ),
    "Q03": (
        r"Page 125.{0,20}Reversal-addition systems|"
        r"From Digits\[Reverse\[Integer Digits\[n, 2\]|"
        r"generalized palindrome|effective period of 4 steps|"
        r"fixed length, dropping any carries on the left|"
        r"often in base 10.{0,100}1939"
    ),
    "Q04": (
        r"Digit reversal\. Sequences of the form|Table\[FromDigits\[|"
        r"Reverse\[IntegerDigits\[n, k, m\]|"
        r"fast Fourier transform.{0,180}quasi-Monte Carlo|"
        r"Johannes van der Corput in 1935"
    ),
    "Q05": (
        r"_page_140_Picture_5\.jpeg|_page_141_Picture_2\.jpeg|"
        r"_page_142_Picture_2\.jpeg|_page_920_Figure_12\.jpeg|"
        r"_page_920_Picture_20\.jpeg|_page_920_Picture_21\.jpeg|"
        r"_page_920_Picture_22\.jpeg"
    ),
    "Q06": r"Reverse\[Integer ?Digits",
    "Q07": r"From ?Digits\[Reverse\[Integer ?Digits",
    "Q08": r"BitReverseOrder|RitReverseOrder",
    "Q09": (
        r"known as dvadic or Palev order|"
        r"Raymond Paley introduced the dyadic basis|"
        r"Fourier\[data\].{0,200}BitReverseOrder"
    ),
    "Q10": (
        r"quasi-random irrational number multiple.{0,120}digit reversal|"
        r"quasi-Monte Carlo methods based on simple sequences"
    ),
    "Q11": (
        r"write its base 2 digits in reverse order|"
        r"Reverse\[IntegerDigits\[n, 2\]|"
        r"digit reversal \(see page 905\) sequences"
    ),
    "Q12": (
        r"Recursive Sequences|Iterated run-length encoding|"
        r"Digit count sequences|Iterated bitwise operations"
    ),
    "Q13": (
        r"_page_139_Figure_1\.jpeg|_page_143_Figure_1\.jpeg|"
        r"_page_920_Figure_8\.jpeg|_page_920_Figure_30\.jpeg|"
        r"_page_921_Picture_[3-7]\.jpeg"
    ),
    "Q14": (
        r"Turing machine \(f\) operates like a base 2 counter|"
        r"Page 905 gives another example of a reversible system based on numbers"
    ),
    "Q15": (
        r"Bit reversal.{0,180}systems based on, 125|Butterfly network, 905|"
        r"Digit reversal systems, 125.{0,20}905|"
        r"FFT \(fast Fourier transform\).{0,80}digit reversal sequences in, 905|"
        r"Halton \(digit reversal\) sequences|"
        r"Monte Carlo methods.{0,700}and digit reversal, 905|"
        r"Palindrome systems, 125-127|"
        r"Quasi-Monte Carlo methods.{0,180}digit reversal, 905|"
        r"Reversal-addition systems, 125.{0,20}905|"
        r"Shuffle-exchange process, 905|"
        r"van der Corput.{0,180}digit reversal sequences, 905|"
        r"Wozniakowski \(digit reversal\) sequences, 905"
    ),
    "Q16": r"digit reversal",
    "Q17": r"Reverse\[",
}


def line_set(spec: str) -> frozenset[int]:
    result: set[int] = set()
    for item in filter(None, map(str.strip, spec.split(","))):
        if "-" in item:
            start, end = map(int, item.split("-", 1))
            result.update(range(start, end + 1))
        else:
            result.add(int(item))
    return frozenset(result)


# Complete governed evidence.  A line need not be a regex hit: captions,
# formulas split across lines, structural boundaries, and relation blocks are
# closed deliberately.  The partitions are semantic dispositions, not storage
# classes or requests for family-specific runtime types.
NATIVE_EVIDENCE = line_set(
    "1531,1533,1535,1537,1539,1541,1543,1545,1547,1549,1551,1553,"
    "12635,12637,12639,12641,12643,12645"
)
RELATION_EVIDENCE = line_set(
    "8838,12646,12648,12650,12652,12654,12656,12658,"
    "17313,17315,17317,17319,17329,17350,17352,17354,17356,17611,20738"
)
CONTROL_EVIDENCE = line_set(
    "1370,1439,1523,1529,1555,1567,12054,12505,12623,12631,12633,"
    "12660,12662,12664,12666,12668,12670,12672,12674,12676,12678,"
    "12680,12682,12684,12686,12688,12692,12767,16072"
)
RETAINED = NATIVE_EVIDENCE | RELATION_EVIDENCE | CONTROL_EVIDENCE

EXCLUDED_CLASS = {
    "unrelated_positional_code": line_set(
        "11268,11637,12236,13103,13516,13520,13717,14578,15069"
    ),
    "other_machine_or_encoding_code": line_set(
        "16018,16068,17136,18910,18914,18918,19006,19169,19397,"
        "19416,19998,20190,20192"
    ),
    "broad_reverse_or_sequence_syntax_collisions": line_set(
        "10930,10982,12226,12424,12513,12519,13036,13058,13511,"
        "13709,13733,13766,14021,14077,14994,15824,16391,16851,"
        "17518,17539,17648,18572,18799,18904,18935,19369"
    ),
}
EXCLUDED = frozenset().union(*EXCLUDED_CLASS.values())


IMAGE_RE = re.compile(r"^!\[[^\]]*\]\(([^)]+)\)$")
NATIVE_IMAGE_LINES = line_set("1543,1547,1551,12641")
RELATION_IMAGE_LINES = line_set("12654,12656,12658")
CONTROL_IMAGE_LINES = frozenset()
GOVERNED_IMAGE_LINES = (
    NATIVE_IMAGE_LINES | RELATION_IMAGE_LINES | CONTROL_IMAGE_LINES
)
EXCLUDED_IMAGE_LINES = line_set(
    "1523,1565,12633,12674,12678,12680,12682,12684,12686"
)
CANDIDATE_IMAGE_LINES = GOVERNED_IMAGE_LINES | EXCLUDED_IMAGE_LINES
UNRESOLVED_IMAGE_LINES = frozenset()


INDEX_CLASS = {
    "native_alias_routes": line_set("20914,21088,21731,21933"),
    "algorithm_and_history_routes": line_set(
        "20942,21185,21233,21525,21877,22114,22394,22434"
    ),
}
INDEX_ROUTED = frozenset().union(*INDEX_CLASS.values())
INDEX_ENTRY_GUARDS = {
    20914: ("Bit reversal", "systems based on, 125"),
    20942: ("Butterfly network, 905",),
    21088: ("Digit reversal systems, 125–127, 905",),
    21185: ("FFT (fast Fourier transform)", "digit reversal sequences in, 905"),
    21233: ("Halton (digit reversal) sequences",),
    21525: ("Monte Carlo methods", "and digit reversal, 905"),
    21731: ("Palindrome systems, 125-127",),
    21877: ("Quasi-Monte Carlo methods", "and digit reversal, 905"),
    21933: ("Reversal-addition systems, 125–127, 905",),
    22114: ("Shuffle-exchange process, 905",),
    22394: ("van der Corput", "and digit reversal sequences, 905"),
    22434: ("Wozniakowski (digit reversal) sequences, 905",),
}

# These neighboring tokens are negative structural sentinels for flattened
# multi-column extraction.  They prove occurrence ownership hazards; they are
# expressly not claimed as T36 content.
INDEX_FLATTENING_SENTINELS = {
    20914: ("randomness generation in, 968",),
    21088: ("Digit count sequences, 905",),
    21525: ("MoebiusMu",),
    21933: ("Reversible 3 n + 1 problem, 905",),
    22434: ("Will Wozniakowski",),
}

INDEX_EXCLUDED_CLASS = {
    "recursive_sequence_and_neighbor_column_collisions": line_set(
        "21050,21090,21114,21162,21193,21253,21275,21338,21360,"
        "21683,21899,21923,21998,22144"
    ),
}
INDEX_EXCLUDED = frozenset().union(*INDEX_EXCLUDED_CLASS.values())
INDEX_EXCLUDED_GUARDS = {
    21050: ("and recursive sequences, 907", "iterated run-length encoding"),
    21090: ("and recursive sequences, 131, 906",),
    21114: ("and recursive sequences, 906",),
    21162: ("and recursive sequences, 906",),
    21193: ("in recursive sequences, 130",),
    21253: ("and recursive sequences, 880, 907",),
    21275: ("and recursive sequences, 907",),
    21338: ("Iterated bitwise operations, 906",),
    21360: ("Iterated run-length encoding, 905",),
    21683: ("in recursive sequences, 130", "in digit count sequences, 905"),
    21899: ("in recursive sequences, 130",),
    21923: ("Recursive sequences, 128–131",),
    21998: ("from iterated bitwise operations",),
    22144: ("in iterated run-length encoding, 905",),
}

# Independent Index-only closure lanes.  The union must equal all twelve
# routed rows, not merely the Index rows happened upon by the main queries.
INDEX_CLOSURE_QUERIES = {
    "core_system_aliases": (
        r"Bit reversal.*systems based on, 125|Digit reversal systems, 125|"
        r"Palindrome systems, 125-127|Reversal-addition systems, 125"
    ),
    "algorithm_aliases": (
        r"Butterfly network, 905|FFT \(fast Fourier transform\).*digit reversal|"
        r"Halton \(digit reversal\)|Monte Carlo methods.*digit reversal, 905|"
        r"Quasi-Monte Carlo methods.*digit reversal, 905|"
        r"Shuffle-exchange process, 905|van der Corput.*digit reversal|"
        r"Wozniakowski \(digit reversal\)"
    ),
    "literal_digit_reversal": r"digit reversal",
    "page905_named_networks": r"Butterfly network, 905|Shuffle-exchange process, 905",
}


SOURCE_MODEL_RECORDS = (
    "category:deterministic discrete singleton t+0D transition system",
    "strict-state:one arbitrary-precision positive integer",
    "strict-program:base two and canonical no-leading-zero digit codec",
    "frontier:reuse T34 UniqueScalar selector",
    "neighborhood:reuse complete self read at the unique scalar locus",
    "rule:encode canonical digits then reverse then decode then exact add",
    "rule-data:closed positional expression nodes rather than callbacks",
    "intermediate:reversed word may have leading zero and need not be canonical",
    "update:reuse same-locus typed assignment and atomic UPDATE",
    "successor:one deterministic successor for every strict positive state",
    "growth:reverse contribution is positive so strict state is strictly increasing",
    "termination:no strict fixed point cycle palindrome halt or visual-period halt",
    "observer:digit rows localized structures crops and widths do not feed back",
    "empirical:effective period four describes visible organization not state equality",
    "empirical:seed512 has no reported repetition through one million steps only",
    "empirical:the million-step value has 568418 base-two digits",
    "generalization:base b at least two changes program identity and must be explicit",
    "zero-extension:zero requires a declared canonical single-zero convention",
    "negative-extension:negative values require a declared sign codec and are not strict",
    "fixed-width:width m is immutable program data and left carry is dropped",
    "fixed-width:successor is addition modulo b to the power m",
    "growing-width:configuration retains both numeric value and semantic width",
    "growing-width:one left digit is added every event even when that digit is zero",
    "representation:canonical integer and canonical digit word commute one event at a time",
    "representation:width word and value-width product commute without hidden event time",
    "relation:fixed-width Table enumerates a digit-reversal permutation not a temporal run",
    "relation:Walsh and FFT BitReverseOrder are algorithmic reorderings",
    "relation:quasi-Monte-Carlo and van-der-Corput sequences do not feed reversal-add state",
    "relation:Turing counter reverse display is a control not T36 mechanics",
    "control:page905 reversible number system is the T35 sibling not T36 reversibility",
    "source-defect:BOOK12637 inserts spaces into FromDigits and IntegerDigits",
    "source-defect:BOOK17313 misspells dyadic and Paley",
    "source-defect:BOOK17315 corrupts BitReverseOrder and its argument pattern",
    "source-defect:BOOK21525 flattens Monte Carlo ownership beside MoebiusMu text",
    "source-defect:BOOK22434 displaces Will before the Wozniakowski entry",
    "duplicate:Recursive Sequences at BOOK1555 and BOOK12688 requires structural ownership",
    "image-boundary:seven governed assets and nine excluded neighbor assets are explicit",
    "architecture:no DigitReversalState assignment UPDATE executor or runner branch",
    "architecture:closed codec transform nodes are the smallest required runtime delta",
    "domain-vocabulary:DOMAIN is t plus dimensional support and strict T36 is t+0D",
)


# Filled with immutable observed counts and digests below.  These values bind
# the result sets rather than merely asserting that searches returned something.
EXPECTED_QUERY: dict[str, tuple[int, int, int, str]] = {}
EXPECTED_SET: dict[str, tuple[int, str]] = {}
EXPECTED_EXCLUDED_CLASS: dict[str, tuple[int, str]] = {}
EXPECTED_EXCLUDED_LINE_GUARDS: tuple[int, str] = (0, "")
EXPECTED_INDEX_CLASS: dict[str, tuple[int, str]] = {}
EXPECTED_INDEX_EXCLUDED_CLASS: dict[str, tuple[int, str]] = {}
EXPECTED_INDEX_EXCLUDED_GUARDS: tuple[int, str] = (0, "")
EXPECTED_INDEX_CLOSURE: dict[str, tuple[int, str]] = {}
EXPECTED_INDEX_CLOSURE_UNION: tuple[int, str] = (0, "")
EXPECTED_INDEX_GUARDS: tuple[int, str] = (0, "")
EXPECTED_IMAGE_PARTITION: dict[str, tuple[int, str]] = {}
EXPECTED_IMAGE_LEDGER: dict[str, tuple[int, str]] = {}
EXPECTED_IMAGE_ASSET_MANIFEST: tuple[int, str] = (0, "")
EXPECTED_SOURCE_MODEL: tuple[int, str] = (0, "")


# The split corpus is independently hash-bound before any provenance join.
EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
EXPECTED_SPLIT_MANIFEST_DIGEST = "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"
EXPECTED_SPLIT_CROSSWALK: tuple[int, str] = (0, "")
EXPECTED_SPLIT_CLASSES: dict[str, tuple[int, str, str]] = {}
EXPECTED_SPLIT_NORMALIZED_MINIMUM = 0.0


EXPECTED_TRACE_16 = (
    16, 17, 34, 51, 102, 153, 306, 459, 882, 1197, 2646, 4347,
    11484, 15273, 24864, 25443, 50886,
)
EXPECTED_TRACE_512 = (
    512, 513, 1026, 1539, 3078, 4617, 9234, 13851, 27702, 41553,
    76950, 130815, 261630, 392445, 784122, 1175031, 3138792,
)


# Explicit repair witnesses prevent a low fuzzy-text score from masquerading
# as provenance.  Each pair is structurally located first, then guarded by the
# damaged monolith fragment and the independently repaired split fragment.
SPLIT_STRUCTURAL_REPAIRS = {
    12637: (
        "BACK-MATTER/Index/Index.md:540",
        "From Digits[Reverse[Integer Digits",
        "FromDigits[Reverse[IntegerDigits",
    ),
    17313: (
        "BACK-MATTER/Index/Index.md:5214",
        "dvadic or Palev order",
        "dyadic or Paley order",
    ),
    17315: (
        "BACK-MATTER/Index/Index.md:5216",
        "RitReverseOrder[a 1",
        "BitReverseOrder[a_]",
    ),
    17319: (
        "BACK-MATTER/Index/Index.md:5220",
        "2^{s, s}",
        "{2^s, 2^s}",
    ),
}


def digest(values: set[int] | frozenset[int]) -> str:
    payload = ",".join(map(str, sorted(values))).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def digest_records(records: set[str] | list[str] | tuple[str, ...]) -> str:
    payload = "\n".join(sorted(records)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_line(line: str) -> str:
    text = unicodedata.normalize("NFKD", line).lower().replace("\\", "")
    return " ".join(re.findall(r"[a-z0-9]+", text))


def compact_line(line: str) -> str:
    return normalized_line(line).replace(" ", "")


def crosswalk_evidence(monolith: str, split: str) -> tuple[str, float]:
    if monolith == split:
        return "EXACT", 1.0
    left_image = IMAGE_RE.fullmatch(monolith.strip())
    right_image = IMAGE_RE.fullmatch(split.strip())
    if left_image and right_image:
        equal = Path(left_image.group(1)).name == Path(right_image.group(1)).name
        return "IMAGE_BASENAME", 1.0 if equal else 0.0
    score = SequenceMatcher(
        None, compact_line(monolith), compact_line(split), autojunk=False
    ).ratio()
    return "NORMALIZED", score


def split_owner_record(line_no: int) -> str:
    """Return the unique structural split owner for a governed Book line."""

    candidates: list[str] = []
    if line_no == 1370:
        candidates.append(
            "CHAPTERS/4-Systems-Based-on-Numbers/"
            "Systems-Based-on-Numbers.md:1"
        )
    if 1439 <= line_no <= 1567:
        candidates.append(
            "CHAPTERS/4-Systems-Based-on-Numbers/"
            f"Systems-Based-on-Numbers.md:{line_no - 1396}"
        )
    if line_no == 8838:
        candidates.append(
            "CHAPTERS/12-The-Principle-of-Computational-Equivalence/"
            f"The-Principle-of-Computational-Equivalence.md:{line_no - 8615}"
        )
    if line_no == 12054:
        candidates.append(
            "CHAPTERS/12-The-Principle-of-Computational-Equivalence/"
            "The-Principle-of-Computational-Equivalence.md:3435"
        )
    if 12505 <= line_no <= 12767:
        candidates.append(f"BACK-MATTER/Index/Index.md:{line_no - 12097}")
    if line_no == 16072:
        candidates.append("BACK-MATTER/Index/Index.md:3973")
    if line_no in {17313, 17315, 17317, 17319}:
        candidates.append(f"BACK-MATTER/Index/Index.md:{line_no - 12099}")
    if line_no in {17329, 17350, 17352, 17354, 17356}:
        candidates.append(f"BACK-MATTER/Index/Index.md:{line_no - 12097}")
    if line_no == 17611:
        candidates.append("BACK-MATTER/Colophon/Colophon.md:168")
    if line_no == 20738:
        candidates.append("BACK-MATTER/Colophon/Colophon.md:3295")
    if line_no in INDEX_ROUTED | INDEX_EXCLUDED:
        candidates.append(
            f"BACK-MATTER/Colophon/Colophon.md:{line_no - 17443}"
        )
    if len(candidates) != 1:
        raise ValueError(f"line {line_no} has {len(candidates)} split owners")
    return candidates[0]


def encode_digits(n: int, base: int, width: int | None = None) -> tuple[int, ...]:
    if base < 2 or n < 0:
        raise ValueError("digits require base >= 2 and nonnegative integer")
    if n == 0:
        digits = [0]
    else:
        digits: list[int] = []
        value = n
        while value:
            digits.append(value % base)
            value //= base
        digits.reverse()
    if width is not None:
        if width < 1 or len(digits) > width:
            raise ValueError("value does not fit declared positive width")
        digits = [0] * (width - len(digits)) + digits
    return tuple(digits)


def decode_digits(digits: tuple[int, ...], base: int) -> int:
    if base < 2 or not digits or any(d < 0 or d >= base for d in digits):
        raise ValueError("invalid finite digit word")
    value = 0
    for digit in digits:
        value = value * base + digit
    return value


def strict_step(n: int, base: int = 2) -> int:
    if n <= 0:
        raise ValueError("strict T36 state is positive")
    word = encode_digits(n, base)
    return n + decode_digits(tuple(reversed(word)), base)


def fixed_step(n: int, base: int, width: int) -> int:
    word = encode_digits(n, base, width)
    return (n + decode_digits(tuple(reversed(word)), base)) % (base**width)


def growing_step(state: tuple[int, int], base: int) -> tuple[int, int]:
    n, width = state
    word = encode_digits(n, base, width)
    successor = n + decode_digits(tuple(reversed(word)), base)
    if successor >= base ** (width + 1):
        raise AssertionError("one declared new digit cannot contain successor")
    return successor, width + 1


def trace(seed: int, count: int, base: int = 2) -> tuple[int, ...]:
    values = [seed]
    for _ in range(count):
        values.append(strict_step(values[-1], base))
    return tuple(values)


def main() -> int:
    if len(sys.argv) > 2:
        raise SystemExit("usage: 43-T36-source-oracle.py [BOOK]")
    book = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else DEFAULT_BOOK
    raw = book.read_bytes()
    lines = raw.decode("utf-8").splitlines()
    at = lambda line_no: lines[line_no - 1]
    source_ok = (
        len(lines) == EXPECTED_BOOK_LINES
        and hashlib.sha256(raw).hexdigest() == EXPECTED_BOOK_SHA256
        and sha256(ATLAS) == EXPECTED_ATLAS_SHA256
        and sha256(CATALOG) == EXPECTED_CATALOG_SHA256
        and sha256(TAXONOMY) == EXPECTED_TAXONOMY_SHA256
    )
    ok = source_ok
    print("source", "OK" if source_ok else "MISMATCH")

    hits: dict[str, set[int]] = {}
    for name, pattern in QUERIES.items():
        rx = re.compile(pattern, re.IGNORECASE)
        found = {
            line_no
            for line_no, line in enumerate(lines, 1)
            if rx.search(line)
        }
        hits[name] = found
        actual = (
            len(found),
            sum(n < INDEX_FIRST_LINE for n in found),
            sum(n >= INDEX_FIRST_LINE for n in found),
            digest(found),
        )
        good = actual == EXPECTED_QUERY.get(name)
        ok &= good
        print(name, "OK" if good else "MISMATCH", *actual)

    union = set().union(*hits.values())
    pre_index = {line_no for line_no in union if line_no < INDEX_FIRST_LINE}
    index_candidates = union - pre_index
    index = index_candidates - set(INDEX_EXCLUDED)
    declared_pre_index = set(RETAINED | EXCLUDED)
    unresolved_pre = pre_index - declared_pre_index
    retained_unmatched = set(RETAINED) - pre_index
    sets = {
        "union": union,
        "pre_index_union": pre_index,
        "index_candidates": index_candidates,
        "index": index,
        "index_excluded": set(INDEX_EXCLUDED),
        "native": set(NATIVE_EVIDENCE),
        "relation": set(RELATION_EVIDENCE),
        "control": set(CONTROL_EVIDENCE),
        "retained": set(RETAINED),
        "excluded": set(EXCLUDED),
        "retained_query_hits": pre_index & set(RETAINED),
        "governed_continuations": retained_unmatched,
    }
    for name, values in sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_SET.get(name)
        ok &= good
        print(name, "OK" if good else "MISMATCH", *actual)

    exclusion_ok = (
        set().union(*EXCLUDED_CLASS.values()) == set(EXCLUDED)
        and sum(map(len, EXCLUDED_CLASS.values())) == len(EXCLUDED)
        and not EXCLUDED & RETAINED
    )
    for name, values in EXCLUDED_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_EXCLUDED_CLASS.get(name)
        exclusion_ok &= good
        print("excluded_" + name, "OK" if good else "MISMATCH", *actual)
    excluded_line_guard_records = {
        f"{line_no}:{hashlib.sha256(at(line_no).encode('utf-8')).hexdigest()}"
        for line_no in EXCLUDED
    }
    excluded_line_guards_actual = (
        len(excluded_line_guard_records),
        digest_records(excluded_line_guard_records),
    )
    exclusion_ok &= (
        excluded_line_guards_actual == EXPECTED_EXCLUDED_LINE_GUARDS
        and all(line_no < INDEX_FIRST_LINE for line_no in EXCLUDED)
    )
    print(
        "excluded_line_occurrence_guards",
        "OK" if excluded_line_guards_actual == EXPECTED_EXCLUDED_LINE_GUARDS else "MISMATCH",
        *excluded_line_guards_actual,
    )
    classification_ok = (
        exclusion_ok
        and not unresolved_pre
        and pre_index <= declared_pre_index
        and not NATIVE_EVIDENCE & RELATION_EVIDENCE
        and not NATIVE_EVIDENCE & CONTROL_EVIDENCE
        and not RELATION_EVIDENCE & CONTROL_EVIDENCE
    )
    ok &= classification_ok
    print(
        "unresolved_pre_index",
        "OK" if classification_ok else "MISMATCH",
        len(unresolved_pre),
        *sorted(unresolved_pre),
    )

    index_ok = (
        set().union(*INDEX_CLASS.values()) == index == set(INDEX_ROUTED)
        and sum(map(len, INDEX_CLASS.values())) == len(index)
        and set().union(*INDEX_EXCLUDED_CLASS.values()) == set(INDEX_EXCLUDED)
        and sum(map(len, INDEX_EXCLUDED_CLASS.values())) == len(INDEX_EXCLUDED)
        and not INDEX_EXCLUDED & INDEX_ROUTED
        and index_candidates == set(INDEX_ROUTED | INDEX_EXCLUDED)
    )
    for name, values in INDEX_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_INDEX_CLASS.get(name)
        index_ok &= good
        print("index_" + name, "OK" if good else "MISMATCH", *actual)
    for name, values in INDEX_EXCLUDED_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_INDEX_EXCLUDED_CLASS.get(name)
        index_ok &= good
        print("index_excluded_" + name, "OK" if good else "MISMATCH", *actual)
    guard_records = {
        f"{line_no}:{'|'.join(needles)}"
        for line_no, needles in INDEX_ENTRY_GUARDS.items()
    }
    sentinel_records = {
        f"{line_no}:{'|'.join(needles)}"
        for line_no, needles in INDEX_FLATTENING_SENTINELS.items()
    }
    excluded_index_guard_records = {
        f"{line_no}:{'|'.join(needles)}"
        for line_no, needles in INDEX_EXCLUDED_GUARDS.items()
    }
    excluded_index_guards_actual = (
        len(excluded_index_guard_records),
        digest_records(excluded_index_guard_records),
    )
    guards_ok = (
        set(INDEX_ENTRY_GUARDS) == set(INDEX_ROUTED)
        and all(
            all(needle in at(line_no) for needle in needles)
            for line_no, needles in INDEX_ENTRY_GUARDS.items()
        )
        and (len(guard_records), digest_records(guard_records))
        == EXPECTED_INDEX_GUARDS
        and set(INDEX_FLATTENING_SENTINELS) <= set(INDEX_ROUTED)
        and all(
            all(needle in at(line_no) for needle in needles)
            for line_no, needles in INDEX_FLATTENING_SENTINELS.items()
        )
        and set(INDEX_EXCLUDED_GUARDS) == set(INDEX_EXCLUDED)
        and all(
            all(needle in at(line_no) for needle in needles)
            for line_no, needles in INDEX_EXCLUDED_GUARDS.items()
        )
        and excluded_index_guards_actual == EXPECTED_INDEX_EXCLUDED_GUARDS
    )
    index_ok &= guards_ok
    ok &= index_ok
    print(
        "index_entry_occurrence_guards",
        "OK" if guards_ok else "MISMATCH",
        len(guard_records),
        digest_records(guard_records),
        "flattening_sentinels",
        len(sentinel_records),
        digest_records(sentinel_records),
    )
    print(
        "index_excluded_occurrence_guards",
        "OK" if excluded_index_guards_actual == EXPECTED_INDEX_EXCLUDED_GUARDS else "MISMATCH",
        *excluded_index_guards_actual,
    )
    print("unresolved_index", "OK" if index_ok else "MISMATCH", len(index ^ set(INDEX_ROUTED)))

    closure_hits: dict[str, set[int]] = {}
    closure_ok = True
    for name, pattern in INDEX_CLOSURE_QUERIES.items():
        rx = re.compile(pattern, re.IGNORECASE)
        found = {
            line_no
            for line_no in range(INDEX_FIRST_LINE, len(lines) + 1)
            if rx.search(at(line_no))
        }
        closure_hits[name] = found
        actual = (len(found), digest(found))
        good = actual == EXPECTED_INDEX_CLOSURE.get(name)
        closure_ok &= good
        print("index_closure_" + name, "OK" if good else "MISMATCH", *actual)
    closure_union = set().union(*closure_hits.values())
    closure_actual = (len(closure_union), digest(closure_union))
    closure_ok &= (
        closure_actual == EXPECTED_INDEX_CLOSURE_UNION
        and closure_union == set(INDEX_ROUTED)
    )
    ok &= closure_ok
    print(
        "index_closure_union_equals_routed_boundary",
        "OK" if closure_ok else "MISMATCH",
        *closure_actual,
        "delta",
        *sorted(closure_union ^ set(INDEX_ROUTED)),
    )

    # Seven governed and nine excluded image references form the exact shared
    # source/asset-oracle interface.  Bind every candidate asset without
    # interpreting pixels.
    image_sets = {
        "native": NATIVE_IMAGE_LINES,
        "relation": RELATION_IMAGE_LINES,
        "control": CONTROL_IMAGE_LINES,
    }
    image_ledger = {
        "candidate_images": CANDIDATE_IMAGE_LINES,
        "governed_images": GOVERNED_IMAGE_LINES,
        "excluded_images": EXCLUDED_IMAGE_LINES,
    }
    images_ok = (
        set().union(*image_sets.values()) == set(GOVERNED_IMAGE_LINES)
        and sum(map(len, image_sets.values())) == len(GOVERNED_IMAGE_LINES)
        and CANDIDATE_IMAGE_LINES == GOVERNED_IMAGE_LINES | EXCLUDED_IMAGE_LINES
        and not GOVERNED_IMAGE_LINES & EXCLUDED_IMAGE_LINES
        and not UNRESOLVED_IMAGE_LINES
    )
    for name, values in image_sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_IMAGE_PARTITION.get(name)
        images_ok &= good
        print("images_" + name, "OK" if good else "MISMATCH", *actual)
    for name, values in image_ledger.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_IMAGE_LEDGER.get(name)
        images_ok &= good
        print(name, "OK" if good else "MISMATCH", *actual)

    image_manifest: set[str] = set()
    image_paths_ok = True
    for line_no in CANDIDATE_IMAGE_LINES:
        match = IMAGE_RE.fullmatch(at(line_no))
        image_paths_ok &= match is not None
        if match is None:
            continue
        basename = Path(match.group(1)).name
        matches = list(SOURCE_ROOT.rglob(basename))
        image_paths_ok &= len(matches) == 1
        if len(matches) != 1:
            continue
        asset = matches[0]
        relative = asset.relative_to(SOURCE_ROOT).as_posix()
        image_manifest.add(
            f"{line_no}->{relative}\0{asset.stat().st_size}\0{sha256(asset)}"
        )
    image_manifest_actual = (len(image_manifest), digest_records(image_manifest))
    images_ok &= (
        image_paths_ok
        and len(image_manifest) == len(CANDIDATE_IMAGE_LINES)
        and image_manifest_actual == EXPECTED_IMAGE_ASSET_MANIFEST
    )
    ok &= images_ok
    print(
        "exact_7_governed_9_excluded_image_interface",
        "OK" if images_ok else "MISMATCH",
        *image_manifest_actual,
    )

    # Primary formula, empirical qualifications, and explicit profile variants.
    main_ok = (
        "write its base 2 digits in reverse order" in at(1545)
        and "add the resulting number to the original one" in at(1545)
        and "starts with the number 16" in at(1545)
        and "After 180 steps" in at(1545)
        and "starting with the number 512" in at(1549)
        and "never seems to take on any kind of simple repetitive form" in at(1549)
        and "starting at the millionth step" in at(1553)
        and "extends about 700 times the width" in at(1553)
        and trace(16, 16) == EXPECTED_TRACE_16
        and trace(512, 16) == EXPECTED_TRACE_512
    )
    ok &= main_ok
    print("source_strict_base2_reversal_add_rule_and_seeds", "OK" if main_ok else "MISMATCH")

    notes_formula_ok = (
        "Page 125 · Reversal-addition systems" in at(12635)
        and "From Digits[Reverse[Integer Digits[n, 2]], 2]" in at(12637)
        and "FromDigits[Reverse[IntegerDigits[n, 2]], 2]" not in at(12637)
        and "generalized palindrome" in at(12639)
        and "at least one digit every two steps" in at(12639)
        and "effective period of 4 steps" in at(12639)
        and "n = 512" in at(12639)
        and "at least a million steps" in at(12639)
        and "568418 base 2 digits" in at(12639)
        and "fixed length, dropping any carries on the left" in at(12643)
        and "one new digit on the left at every step, even when it is 0" in at(12643)
        and "often in base 10" in at(12645)
        and "at least as long ago as 1939" in at(12645)
    )
    ok &= notes_formula_ok
    print("source_notes_formula_profiles_and_qualified_observations", "OK" if notes_formula_ok else "MISMATCH")

    codec_ok = (
        encode_digits(0, 2) == (0,)
        and encode_digits(2, 2) == (1, 0)
        and decode_digits((0, 1), 2) == 1
        and strict_step(2) == 3
        and strict_step(12, 2) == 15
        and strict_step(12, 10) == 33
        and all(strict_step(n) > n for n in range(1, 4097))
        and all(decode_digits(encode_digits(n, b), b) == n for b in range(2, 17) for n in range(1024))
    )
    ok &= codec_ok
    print("source_closed_canonical_codec_transform_exact_unbounded", "OK" if codec_ok else "MISMATCH")

    profile_ok = (
        fixed_step(1, 2, 1) == 0
        and strict_step(1, 2) == 2
        and growing_step((1, 1), 2) == (2, 2)
        and growing_step((1, 2), 2) == (3, 3)
        and growing_step((1, 1), 2)[0] != growing_step((1, 2), 2)[0]
    )
    ok &= profile_ok
    print("source_width_profiles_visible_and_information_loss_counterexample", "OK" if profile_ok else "MISMATCH")

    relation_ok = (
        "Digit reversal. Sequences of the form" in at(12646)
        and "Table[FromDigits[" in at(12648)
        and "Reverse[IntegerDigits[n, k, m]], k]" in at(12650)
        and "fast Fourier transform" in at(12652)
        and "quasi-Monte Carlo schemes" in at(12652)
        and "Johannes van der Corput in 1935" in at(12652)
        and "BitReverseOrder" in at(17350)
        and "fast Fourier transform" in at(17354)
        and "BitReverseOrder[data]" in at(17356)
        and "digit reversal (see page 905) sequences" in at(17611)
        and "quasi-Monte Carlo methods based on simple sequences" in at(20738)
    )
    ok &= relation_ok
    print("source_fixed_width_enumeration_FFT_Walsh_QMC_relations", "OK" if relation_ok else "MISMATCH")

    boundaries_ok = (
        "systems based on numbers there is usually no such locality" in at(1533)
        and "carry" in at(1535)
        and "propagate arbitrarily far" in at(1535)
        and "details of underlying rules" in at(1539)
        and "Recursive Sequences" in at(1555)
        and "reverse of the base 2 digit sequences of successive numbers" in at(12054)
        and "Page 905 gives another example of a reversible system based on numbers" in at(16072)
        and "Iterated run-length encoding" in at(12660)
        and "Digit count sequences" in at(12668)
        and "Iterated bitwise operations" in at(12676)
    )
    ok &= boundaries_ok
    print("source_neighbor_relations_and_T37_boundary_are_controls", "OK" if boundaries_ok else "MISMATCH")

    source_defects_ok = (
        "dvadic or Palev order" in at(17313)
        and "RitReverseOrder[a 1" in at(17315)
        and "dyadic or Paley order" not in at(17313)
        and "BitReverseOrder[a_]" not in at(17315)
        and "Monte Carlo methods" in at(21525)
        and "MoebiusMu" in at(21525)
        and "and digit reversal, 905" in at(21525)
        and "Will Wozniakowski (digit reversal) sequences, 905" in at(22434)
    )
    ok &= source_defects_ok
    print("source_OCR_and_flattened_Index_hazards_guarded", "OK" if source_defects_ok else "MISMATCH")

    split_paths = sorted(
        path
        for path in SOURCE_ROOT.rglob("*.md")
        if path.resolve() not in {DEFAULT_BOOK.resolve(), ATLAS.resolve()}
    )
    relative_paths = [path.relative_to(SOURCE_ROOT).as_posix() for path in split_paths]
    manifest = [
        f"{relative}\0{len(path.read_bytes())}\0{sha256(path)}"
        for path, relative in zip(split_paths, relative_paths, strict=True)
    ]
    split_manifest_ok = (
        len(split_paths) == EXPECTED_SPLIT_FILE_COUNT
        and digest_records(relative_paths) == EXPECTED_SPLIT_PATHS_DIGEST
        and digest_records(manifest) == EXPECTED_SPLIT_MANIFEST_DIGEST
    )
    ok &= split_manifest_ok
    print(
        "split_manifest",
        "OK" if split_manifest_ok else "MISMATCH",
        len(split_paths),
        digest_records(relative_paths),
        digest_records(manifest),
    )

    split_text: dict[str, str] = {}
    for path, relative in zip(split_paths, relative_paths, strict=True):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            split_text[f"{relative}:{line_no}"] = line

    crosswalk_lines = RETAINED | INDEX_ROUTED | INDEX_EXCLUDED
    crosswalk_records: set[str] = set()
    owner_records: set[str] = set()
    class_lines: dict[str, set[int]] = {
        "EXACT": set(),
        "IMAGE_BASENAME": set(),
        "NORMALIZED": set(),
        "STRUCTURAL_REPAIR": set(),
    }
    class_records: dict[str, set[str]] = {name: set() for name in class_lines}
    normalized_scores: list[float] = []
    split_join_ok = True
    for line_no in sorted(crosswalk_lines):
        try:
            owner = split_owner_record(line_no)
        except ValueError:
            split_join_ok = False
            continue
        if owner in owner_records or owner not in split_text:
            split_join_ok = False
            continue
        owner_records.add(owner)
        mode, score = crosswalk_evidence(at(line_no), split_text[owner])
        if line_no in SPLIT_STRUCTURAL_REPAIRS:
            expected_owner, monolith_guard, split_guard = SPLIT_STRUCTURAL_REPAIRS[line_no]
            split_join_ok &= (
                owner == expected_owner
                and monolith_guard in at(line_no)
                and split_guard in split_text[owner]
                and mode == "NORMALIZED"
            )
            mode = "STRUCTURAL_REPAIR"
        if mode not in class_lines:
            split_join_ok = False
            continue
        if mode == "NORMALIZED":
            normalized_scores.append(score)
            split_join_ok &= score >= 0.98
        elif mode != "STRUCTURAL_REPAIR":
            split_join_ok &= score == 1.0
        record = f"{line_no}->{owner}:{mode}:{score:.6f}"
        crosswalk_records.add(record)
        class_lines[mode].add(line_no)
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
    normalized_minimum = min(normalized_scores, default=0.0)
    duplicate_candidates = {
        line_no
        for line_no, line in enumerate(lines, 1)
        if line == at(1555)
    }
    split_join_ok &= (
        crosswalk_actual == EXPECTED_SPLIT_CROSSWALK
        and class_actual == EXPECTED_SPLIT_CLASSES
        and round(normalized_minimum, 6) == EXPECTED_SPLIT_NORMALIZED_MINIMUM
        and len(crosswalk_records) == len(crosswalk_lines)
        and len(owner_records) == len(crosswalk_lines)
        and set().union(*class_lines.values()) == set(crosswalk_lines)
        and sum(map(len, class_lines.values())) == len(crosswalk_lines)
        and duplicate_candidates == {1555, 12688}
        and split_owner_record(1555).endswith(":159")
        and split_owner_record(12688).endswith(":591")
        and "FromDigits" in split_text[split_owner_record(12637)]
        and "IntegerDigits" in split_text[split_owner_record(12637)]
        and "dyadic or Paley order" in split_text[split_owner_record(17313)]
        and "BitReverseOrder[a_]" in split_text[split_owner_record(17315)]
    )
    ok &= split_join_ok
    print(
        "split_structural_reverse_join_OCR_repairs_and_duplicate_hazard",
        "OK" if split_join_ok else "MISMATCH",
        *crosswalk_actual,
        f"normalized_min={normalized_minimum:.6f}",
    )
    for name, actual in class_actual.items():
        print("split_class_" + name, *actual)

    catalog_lines = CATALOG.read_text(encoding="utf-8").splitlines()
    taxonomy_text = TAXONOMY.read_text(encoding="utf-8")
    catalog_ok = (
        len(catalog_lines) == 46
        and catalog_lines[36] == "Digit-Reversal Arithmetic Systems,"
        and len(set(catalog_lines[1:])) == 45
        and "## 36. Digit-Reversal Arithmetic Systems" in taxonomy_text
        and "State is a single integer" in taxonomy_text
        and "digit sequence is transformed" in taxonomy_text
        and not hits["Q00"]
    )
    ok &= catalog_ok
    print("catalog_taxonomy_vocabulary_only_absent_from_primary_Book", "OK" if catalog_ok else "MISMATCH")

    model_actual = (len(SOURCE_MODEL_RECORDS), digest_records(SOURCE_MODEL_RECORDS))
    architecture_ok = (
        model_actual == EXPECTED_SOURCE_MODEL
        and main_ok
        and notes_formula_ok
        and codec_ok
        and profile_ok
        and relation_ok
        and boundaries_ok
        and source_defects_ok
    )
    ok &= architecture_ok
    print(
        "source_fit_T34_unary_event_plus_closed_codec_transform_no_new_executor",
        "OK" if architecture_ok else "MISMATCH",
        *model_actual,
    )

    unresolved_total = (
        len(unresolved_pre)
        + len(index ^ set(INDEX_ROUTED))
        + (len(crosswalk_lines) - len(crosswalk_records))
        + len(UNRESOLVED_IMAGE_LINES)
        + (len(CANDIDATE_IMAGE_LINES) - len(image_manifest))
    )
    unresolved_ok = unresolved_total == 0
    ok &= unresolved_ok
    print("unresolved_total", "OK" if unresolved_ok else "MISMATCH", unresolved_total)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
