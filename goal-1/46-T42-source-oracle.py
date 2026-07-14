#!/usr/bin/env python3
"""Fail-closed primary-source audit for T42 CF-driven substitutions.

The Book's executable construction is a finite schedule of ordinary binary
substitutions.  A continued-fraction result supplies ``(a0,a1,...,a[m-1])``;
the source program executes ``Reverse[Rest[...]]`` and applies one generated
rule to every old occurrence at each event.  The offset ``Floor[h]`` belongs
to the observed mechanical word, not to substitution state.

This audit closes the strict page-162 main span, the native page-903 Notes
construction, related mechanical-word/digital-slope/billiard evidence, every
physical row of the actual flattened Index, all split-corpus owners, and all
twelve candidate rasters.  It also freezes two important source boundaries:
``ContinuedFraction[h,m]`` has m terms but ``Rest`` supplies only m-1 rules,
and the four page-162 profile identities/visible coefficient rows are limited
raster transcription rather than prose-derived fixtures.

The oracle is dependency-free, repo-relative, silent on import, deterministic,
and deliberately rejects ``python -O``.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path


if not __debug__:
    raise RuntimeError("T42 source oracle requires assertions; do not use -O")


SCRIPT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BOOK = SCRIPT_ROOT / "ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md"
INDEX_FIRST_LINE = 20826
INDEX_CONTENT_FIRST_LINE = 20828
INDEX_CONTENT_LAST_LINE = 22456
EXPECTED_BOOK_LINES = 22_498
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


def digest(values: set[int] | frozenset[int]) -> str:
    return hashlib.sha256(",".join(map(str, sorted(values))).encode("ascii")).hexdigest()


def digest_records(records: set[str] | frozenset[str] | list[str] | tuple[str, ...]) -> str:
    return hashlib.sha256("\n".join(sorted(records)).encode("utf-8")).hexdigest()


def digest_framed_records(records: set[str]) -> str:
    payload = bytearray()
    for record in sorted(records):
        encoded = record.encode("utf-8")
        payload.extend(len(encoded).to_bytes(8, "big"))
        payload.extend(encoded)
    return hashlib.sha256(bytes(payload)).hexdigest()


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


# Redundant discovery lanes.  Q00 proves that the catalog name is external
# vocabulary.  Q07 closes all twelve raster candidates without a broad image
# glob.  Q02/Q13 independently bind the exact Notes schedule.
QUERIES = {
    "Q00": r"Continued-Fraction-Driven Substitution Systems?",
    "Q01": (
        r"generalized substitution system|"
        r"rule at each step.{0,120}continued fraction|"
        r"successive terms in each continued fraction"
    ),
    "Q02": (
        r"Relation to substitution systems|"
        r"Reverse.{0,120}Rest.{0,120}ContinuedFraction|"
        r"Floor\[h\] \+ Fold"
    ),
    "Q03": (
        r"Floor\[\(n\+1\)h\] - Floor\[nh\]|"
        r"Floor\[\(n\+1\)#\] - Floor\[n#\]"
    ),
    "Q04": r"Digital slope representation|digital slopes",
    "Q05": r"Billiards?|billiard trajectories",
    "Q06": (
        r"and continued fractions, 914|and sine curves, 147|"
        r"Continued fractions, 143, 914|Substitution systems, 82-87"
    ),
    "Q07": (
        r"_page_(?:162_Figure_1|918_Figure_16|"
        r"931_Figure_(?:9|10|11|12|13)|"
        r"986_Picture_(?:4|5|6|7|8))\.jpeg"
    ),
    "Q08": (
        r"ContinuedFraction\[h, m\]|"
        r"first n terms.{0,80}continued fraction|ContinuedFraction\[x, n\]"
    ),
    "Q09": (
        r"GoldenRatio.{0,180}substitution system|"
        r"sqrt\{2\}.{0,180}substitution system|"
        r"quadratic.{0,180}continued fraction.{0,180}substitution"
    ),
    "Q10": (
        r"Page 147 · Substitution systems|"
        r"more complicated sequence of substitution rules"
    ),
    "Q11": (
        r"continued fraction.{0,220}substitution|"
        r"substitution.{0,220}continued fraction"
    ),
    "Q12": (
        r"axis crossings?.{0,220}substitution|"
        r"sine curves.{0,160}substitution"
    ),
    "Q13": r"first m rules|yield far more than m elements",
}


STRICT_MAIN_CONTENT = line_set("1850,1852,1854,1856,1858")
STRICT_NOTES_CONTENT = line_set("12587,12589,12591,12593,12595")

NATIVE_EVIDENCE = STRICT_MAIN_CONTENT | STRICT_NOTES_CONTENT

RELATION_EVIDENCE = line_set(
    "12581,12583,12585,12986,"
    "13111,13113,13115,13117,13119,13121,13123,13125,13127,"
    "13170,13172,"
    "14923,14925,14927,14929,14931,14933"
)

CONTROL_EVIDENCE = line_set(
    "982,984,986,"
    "1786,1792,1794,1828,11531,"
    "13030,13032,13034,13052,13054,13056,13060,13062,13070,13072,"
    "13074,13084,13086,13096,13100"
)

RETAINED = NATIVE_EVIDENCE | RELATION_EVIDENCE | CONTROL_EVIDENCE

EXCLUDED_CLASS = {
    "unrelated_substitution_constructions": line_set(
        "5012,6984,14155,16418,16446,16875"
    ),
    "other_number_or_map_siblings": line_set("13219,14468,15517"),
    "continuous_billiard_sibling": line_set("16115"),
}
EXCLUDED = frozenset().union(*EXCLUDED_CLASS.values())


# Independent Book-wide vocabulary closure, not derived from QUERIES.
BOOK_BROAD_PATTERN = (
    r"continued fractions?|continued-fraction|generalized substitution|"
    r"substitution rules?|digital slope|billiards?"
)
BOOK_BROAD_CANDIDATES = line_set(
    "1786,1792,1794,1828,1850,1852,1856,1858,5012,6984,11531,"
    "12587,12593,12595,12986,13030,13034,13052,13054,13056,13060,"
    "13062,13070,13072,13074,13084,13096,13100,13111,13172,13219,"
    "14155,14468,14923,15517,16115,16418,16446,16875"
)


# The actual flattened physical Index is closed independently of query hits.
INDEX_BROAD_PATTERN = (
    r"continued fractions?|continued-fraction|generalized substitution|"
    r"substitution rules?|substitution systems?|digital slopes?|billiards?|"
    r"axis crossings?|mechanical words?"
)
INDEX_BROAD_CANDIDATES = line_set(
    "20828,20850,20910,20914,20918,20940,20944,20946,20957,20965,"
    "20972,20980,21014,21032,21038,21044,21054,21068,21080,21088,"
    "21114,21162,21168,21173,21185,21187,21189,21193,21195,21207,"
    "21213,21223,21233,21264,21288,21329,21337,21360,21432,21473,"
    "21497,21513,21525,21535,21652,21656,21681,21683,21687,21703,"
    "21711,21735,21761,21779,21783,21801,21815,21845,21891,21899,"
    "21915,21923,21929,21933,21982,21994,21998,22016,22096,22110,"
    "22114,22120,22132,22134,22136,22138,22144,22146,22148,22150,"
    "22272,22285,22352,22378,22380,22390,22432,22444,22452"
)

INDEX_CLASS = {
    "native": line_set("21044,22144,22146"),
    "relation": line_set("20828,20914,21185,21187,21193,21337,21525,22114"),
}
INDEX_CLASS["control"] = INDEX_BROAD_CANDIDATES - frozenset().union(
    *INDEX_CLASS.values()
)
INDEX_SEMANTIC_UNIVERSE = frozenset().union(*INDEX_CLASS.values())

INDEX_ENTRY_GUARDS = {
    20828: ("and sine curves, 146", "and substitution systems, 892, 904"),
    20914: ("Billiards model, 971, 1022",),
    21044: ("Continued fractions, 143, 914–915", "and sine curves, 147"),
    21185: ("as term in continued fraction, 913",),
    21187: ("Fibonacci substitution system", "and sine curves, 147"),
    21193: ("and digital slopes, 916",),
    21337: ("idealized billiards, 1022",),
    21525: ("and continued fractions, 914", "idealized billiards, 1022"),
    22114: ("ergodicity of billiards, 1022",),
    22144: ("and billiard trajectories, 971", "and continued fractions, 914"),
    22146: ("and sine curves, 147, 917",),
}

INDEX_FLATTENING_SENTINELS = {
    20828: ("Preface are not included in this index",),
    21044: ("Continental drift as non-math theory",),
    21525: ("Movie effects",),
    22144: ("Substitution systems, 82-87",),
    22452: ("Z transforms and spectra of substitution systems",),
}


IMAGE_RE = re.compile(r"^!\[[^\]]*\]\(([^)]+)\)$")
NATIVE_IMAGE_LINES = line_set("1854")
RELATION_IMAGE_LINES = line_set(
    "12583,13119,13121,13123,13125,13127,14925,14927,14929,14931,14933"
)
CONTROL_IMAGE_LINES: frozenset[int] = frozenset()
GOVERNED_IMAGE_LINES = (
    NATIVE_IMAGE_LINES | RELATION_IMAGE_LINES | CONTROL_IMAGE_LINES
)
EXCLUDED_IMAGE_LINES: frozenset[int] = frozenset()
CANDIDATE_IMAGE_LINES = GOVERNED_IMAGE_LINES
UNRESOLVED_IMAGE_LINES: frozenset[int] = frozenset()

# Epistemic use of raster content.  Physical bytes remain hash-bound in both
# classes, but BOOK1854 also supplies limited visual transcription: the four
# profile identities, visible CF rows, and icon orientation are not prose.
HASH_BOUND_IMAGE_LINES = GOVERNED_IMAGE_LINES
LIMITED_TRANSCRIBED_IMAGE_LINES = NATIVE_IMAGE_LINES
PIXEL_REPLAYED_IMAGE_LINES: frozenset[int] = frozenset()

IMAGE_ROLE_RECORDS = (
    "1854:native:hash-bound+limited-transcribed:page162 four profile rows visible coefficients and icon orientation",
    "12583:relation:hash-bound:page903 fractional-orbit observer",
    "13119:relation:hash-bound:page916 digital-slope panel a",
    "13121:relation:hash-bound:page916 digital-slope panel b",
    "13123:relation:hash-bound:page916 digital-slope panel c",
    "13125:relation:hash-bound:page916 digital-slope panel d",
    "13127:relation:hash-bound:page916 digital-slope panel e",
    "14925:relation:hash-bound:page971 billiard panel a",
    "14927:relation:hash-bound:page971 billiard panel b",
    "14929:relation:hash-bound:page971 billiard panel c",
    "14931:relation:hash-bound:page971 billiard panel d",
    "14933:relation:hash-bound:page971 billiard panel e",
)

IMAGE_CANDIDATE_SCOPES = {
    "strict-page162": (1850, 1858, NATIVE_IMAGE_LINES),
    "page903-mechanical-word": (12581, 12595, line_set("12583")),
    "page916-digital-slope": (
        13111, 13129, line_set("13119,13121,13123,13125,13127")
    ),
    "page971-billiards": (
        14923, 14935, line_set("14925,14927,14929,14931,14933")
    ),
}

IMAGE_ASSEMBLY_BOUNDARIES = (
    "page162:one composite plate:four profiles:profile labels coefficients icons and traces require limited transcription",
    "page903:one observer plate:not substitution configuration or executable rule data",
    "page916:five-panel assembly:line renderings remain observers not rule tables",
    "page971:five-panel assembly:trajectories remain relations not coefficient or itinerary sources",
    "authority:text BOOK12587-12591 supplies rho schedule seed and fold mechanics",
    "authority:raster BOOK1854 supplies only declared limited transcription and never executable pixel replay",
)


SOURCE_SEMANTIC_GUARDS = (
    ("t13_variable_support", 984, ("number of elements can change", "each one of these elements is replaced"), ()),
    ("t13_self_rule", 986, ("each element of a particular color", "fixed block of new elements"), ()),
    ("main_driver", 1850, ("rule at each step", "term in the continued fraction representation"), ()),
    ("main_periodic", 1852, ("continued fraction representation is purely repetitive",), ()),
    ("main_raster", 1854, ("_page_162_Figure_1.jpeg",), ("Cos[x]", "ContinuedFraction")),
    ("main_word_observer", 1856, ("axis crossing", "black", "white"), ()),
    ("main_rule_raster", 1856, ("rule determined as shown on the left", "going up the page"), ()),
    ("main_boundary", 1858, ("more than two sine functions", "no longer seems"), ()),
    ("mechanical_context", 12581, ("successive multiples", "particle bouncing"), ()),
    ("notes_schedule_claim", 12587, ("first m rules", "not a rational number", "continued fraction form"), ()),
    ("notes_rule_codec", 12589, ("Map", "Table", "Reverse", "Rest", "ContinuedFraction"), ()),
    ("notes_seed_fold", 12591, ("Floor[h] + Fold", "Flatten", "{0}", "rules"), ()),
    ("notes_periodic", 12593, ("quadratic equation", "continued fraction form is repetitive"), ()),
    ("notes_fixed_presets", 12595, ("neighbor-independent substitution system", "GoldenRatio", "sqrt{2}", "sqrt{3}"), ()),
    ("t40_term_count", 13030, ("first n terms", "ContinuedFraction"), ()),
    ("t40_iteration", 13032, ("Floor[NestList", "n-1"), ()),
    ("t40_inverse", 13034, ("FromContinuedFraction",), ()),
    ("digital_slope", 13111, ("Digital slope representation", "Floor[nh] - Floor[(n-1)h]", "substitution rules"), ()),
    ("cosine_count", 13170, ("two families of zeros", "Floor[(n+1)#] - Floor[n#]"), ()),
    ("sine_variant", 13172, ("more complicated sequence of substitution rules", "-1/2 is inserted"), ("Reverse", "ContinuedFraction")),
    ("billiard_relation", 14923, ("successive terms in the continued fraction form", "related to substitution systems"), ("Reverse", "Fold")),
)


SOURCE_DEFECT_RECORDS = (
    "term-count:BOOK12587 says first-m-rules but BOOK12589 Rest of an m-term CF supplies m-1 rules",
    "m-equals-one:an m=1 coefficient query yields an empty rule schedule and the unchanged one-symbol seed",
    "irrational-scope:BOOK12587 states the construction for h that is not rational; rational completion is a typed extension",
    "observer-offset:BOOK12591 adds Floor[h] outside Fold so a0 is not substitution state or a rule event",
    "orientation:BOOK12589 reverses the natural CF tail exactly once; BOOK1856 displays successive steps going up the page",
    "raster-profiles:BOOK1854 profile identities and visible coefficient rows are limited transcription not prose-derived fixtures",
    "raster-icons:BOOK1856 delegates the exact icon presentation to the left side of BOOK1854",
    "sine-underspecified:BOOK13172 gives a half-shifted observer but no executable coefficient-to-rule schedule",
    "digital-slope-boundary:BOOK13111 is an observer/reconstruction relation and not T42 transition state",
    "billiard-boundary:BOOK14923 states a relation but supplies neither rule codec nor substitution trace",
)


SOURCE_MODEL_RECORDS = (
    "classification:classes-1-2-3-only:no-new-execution-algebra",
    "base:T13-finite-ordered-word-all-occurrences-self-read-ordered-generation-concat",
    "domain:discrete-t-plus-1D-variable-length-ordered-word",
    "alphabet:binary-data-symbols-with-unbounded-positive-coefficients-kept-outside-symbol-rank",
    "configuration:visible-finite-schedule-cursor-times-nonempty-binary-word",
    "lossless-lowering:uniform-PhaseIndex-times-Bit-word",
    "frontier:all-old-occurrences-at-the-current-visible-phase",
    "neighborhood:self-symbol-plus-visible-current-coefficient",
    "rule:rho-a-zero-is-zero-to-the-a-minus-1-then-one",
    "rule:rho-a-one-is-zero-to-the-a-minus-1-then-one-zero",
    "update:old-snapshot-source-ordered-child-concatenation",
    "update:cursor-advance-and-word-replacement-commit-atomically",
    "seed:exactly-one-zero-symbol",
    "schedule:natural-CF-a0-tail-reversed-exactly-once",
    "schedule:m-natural-terms-produce-m-minus-1-events",
    "completion:finite-schedule-exhaustion-is-visible-and-distinct-from-fixed-point-or-empty-word",
    "boundary:T40-owns-complete-replay-verified-CF-query-result-and-provenance",
    "boundary:T42-must-not-accept-forgeable-detached-digests-or-coefficient-tuples-as-T40-proof",
    "boundary:explicit-schedule-source-needs-its-own-complete-typed-provenance",
    "boundary:T41-owns-source-functions-zero-families-and-count-queries",
    "boundary:Floor-h-and-mechanical-word-views-do-not-feed-back-into-transition-state",
    "boundary:raster-is-never-an-executable-rule-table-or-pixel-replayed-program",
    "source:page162-limited-transcription-remains-separate-from-prose-rule-authority",
    "runner:FRONTIER-select-NEIGHBORHOOD-read-RULE-write-UPDATE-apply",
    "forbidden:no-T42-state-class-update-algebra-executor-family-dispatch-callback-or-hidden-interpreter",
)


AUXILIARY_SEMANTIC_GUARDS = (
    ("catalog", 43, ("Continued-Fraction-Driven Substitution Systems",), ()),
    ("taxonomy", 1160, ("Continued-Fraction-Driven Substitution Systems",), ()),
    ("taxonomy", 1164, ("State is a sequence of symbols",), ()),
    ("taxonomy", 1165, ("continued-fraction expansion",), ()),
    ("taxonomy", 1166, ("determine which substitution rule is used at each step",), ()),
    ("taxonomy", 1171, ("Ordinary substitution systems use the same replacement rule",), ()),
    ("taxonomy", 1172, ("rule schedule is driven",), ()),
    ("taxonomy", 1179, ("coefficient_source",), ()),
    ("taxonomy", 1180, ("rule_generator",), ()),
    ("taxonomy", 1181, ("step_policy",), ()),
    ("atlas", 89, ("Substitution Systems",), ()),
    ("atlas", 91, ("number of elements can grow or shrink",), ()),
)


SPLIT_OMISSION_GROUPS = {
    "abridged-main-continued-fraction-mechanics": line_set("1786,1792,1794"),
}
SPLIT_OMISSION_LINES = frozenset().union(*SPLIT_OMISSION_GROUPS.values())

SPLIT_BOUNDARY_WITNESSES = (
    "t13:BOOK984->CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:301",
    "main:BOOK1850->CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:309",
    "main-image:BOOK1854->CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:313",
    "notes:BOOK12587->BACK-MATTER/Index/Index.md:490",
    "digital:BOOK13111->BACK-MATTER/Index/Index.md:1014",
    "sine:BOOK13170->BACK-MATTER/Index/Index.md:1073",
    "billiard:BOOK14923->BACK-MATTER/Index/Index.md:2824",
    "actual-index:BOOK20828->BACK-MATTER/Colophon/Colophon.md:3385",
)


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
    if line_no in {982, 984, 986}:
        return (
            "CHAPTERS/3-The-World-of-Simple-Programs/"
            f"The-World-of-Simple-Programs.md:{line_no - 683}"
        )
    if line_no == 1828:
        return "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:287"
    if 1850 <= line_no <= 1858:
        return (
            "CHAPTERS/4-Systems-Based-on-Numbers/"
            f"Systems-Based-on-Numbers.md:{line_no - 1541}"
        )
    if line_no == 11531:
        return (
            "CHAPTERS/12-The-Principle-of-Computational-Equivalence/"
            "The-Principle-of-Computational-Equivalence.md:2912"
        )
    if 12581 <= line_no <= 13172:
        return f"BACK-MATTER/Index/Index.md:{line_no - 12097}"
    if 14923 <= line_no <= 14933:
        return f"BACK-MATTER/Index/Index.md:{line_no - 12099}"
    if INDEX_CONTENT_FIRST_LINE <= line_no <= INDEX_CONTENT_LAST_LINE:
        return f"BACK-MATTER/Colophon/Colophon.md:{line_no - 17443}"
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


def rho_block(coefficient: int, bit: int) -> tuple[int, ...]:
    assert type(coefficient) is int and coefficient > 0
    assert type(bit) is int and bit in (0, 1)
    return (0,) * (coefficient - 1) + (1,) + ((0,) if bit else ())


def logic_records() -> set[str]:
    icon_rows = {
        f"rho:{coefficient}:{bit}:{''.join(map(str, rho_block(coefficient, bit)))}"
        for coefficient in range(1, 6)
        for bit in (0, 1)
    }
    natural = (0, 1, 1, 2, 1, 4, 2)
    schedule = tuple(reversed(natural[1:]))
    assert schedule == (2, 4, 1, 2, 1, 1)
    assert len(schedule) == len(natural) - 1
    assert tuple(reversed(schedule)) == natural[1:]
    assert len((0,)[1:]) == 0
    return icon_rows | {
        "schedule:0,1,1,2,1,4,2->2,4,1,2,1,1",
        "term-count:7-natural-terms->6-events",
        "m1:one-natural-term->zero-events",
        "seed:0",
        "observer-offset:Floor[h]-outside-substitution-word",
    }


def parse_args(args: list[str]) -> tuple[bool, str | None]:
    json_mode = False
    positional: list[str] = []
    usage = "usage: 46-T42-source-oracle.py [--json] [BOOK]"
    for argument in args:
        if argument == "--json":
            if json_mode:
                raise SystemExit(usage)
            json_mode = True
        elif argument.startswith("-"):
            raise SystemExit(usage)
        else:
            positional.append(argument)
    if len(positional) > 1:
        raise SystemExit(usage)
    return json_mode, positional[0] if positional else None


# Frozen expectations.  Values are filled from the independently readable
# declarations above and checked again against live source bytes below.
EXPECTED_QUERY = {
    "Q00": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q01": (5, 5, 0, "f8710b2412ad4651b7ef6b7dd3f223776e65ce5f7d84103bfb45b2f90ddca50f"),
    "Q02": (3, 3, 0, "c302cd43d2b3e7bbd3faf8a98495f12d2593d0a118f2a21956ec1d66653a20e7"),
    "Q03": (2, 2, 0, "46bf2b5dd51adba53799df7585565a95b9e1c9c9bb9ac015ef1030be3b7a107f"),
    "Q04": (3, 1, 2, "0d751f12ba7f85ba919f039f9c0d417bbabcea269af3c784feeabe4cfc070739"),
    "Q05": (8, 2, 6, "218bc647ed1de067f8d0f2672353ae5bc201885b5c5f67c1205382c2e69d7391"),
    "Q06": (12, 0, 12, "dc3179fa806b86967b60167d7821a0f1bf8932d8a2585fb7967eb3d1eee4f837"),
    "Q07": (12, 12, 0, "076dc9462bf81a5c4ee5628f077b0318ce13d72160d4166748c7da09a77ec082"),
    "Q08": (2, 2, 0, "70e3084ca419653bf9368faea602e9093bd7e6f89178238549753553a9cb1a06"),
    "Q09": (5, 3, 2, "ecad1c7ba382ab83cd05c04c25c729a219eadb93919a5431c9af02c5b205681b"),
    "Q10": (2, 2, 0, "53743c47381079219e0772dc6113709972eb62065d6bc20dbe7f8fe01a5f3fa6"),
    "Q11": (11, 7, 4, "3ad792c7fc762952dc19d52d9be8b2dc6a8fcdddb757c216169f3c208620f668"),
    "Q12": (2, 1, 1, "b32b8340716f95a0e2f9ee5f31c9fc9298de6c22f6cd8a6916f027a5783a72be"),
    "Q13": (1, 1, 0, "cf878cbcfed31d52f7201f160152dcdf3c0a9400cc359bb1704a05f31116f272"),
}
EXPECTED_QUERY_PATTERNS = (
    14,
    "431aef4dc96605835af9c080e969b2aa7e33c92ffbdc9dd160e9e7ea9bb7ddfe",
)
EXPECTED_SET = {
    "union": (48, "0e15f97decaaf6b6cd492dffad6455abfa02e5fbffd676bf66a0e4e853e87c70"),
    "pre_index": (29, "46ad8aa0113cb3046450b9e98db938722377124c009744c283fcc7515ad633a6"),
    "index_candidates": (19, "e0093fc12df9fdf7f43c1777b4dbd2cc66e2b0ca009ab103fb6eb3d04f91df92"),
    "query_native": (8, "79994680a50ad2e2b43bee6b7e86978f1f6f3ffdb007836ee8897b5f37be3d6e"),
    "query_relation": (15, "116d7bc1dafa3a933a7bb0308769aba11babd581a5d9bcad5984a3714956d764"),
    "query_control": (3, "ced58456e954dbecde59d508bb4522d6a0387ab0ac4e5ccae220184377a73970"),
    "query_excluded": (3, "34a442aa7bf2593bf2faae82572f070857bc701819d87730456af0c09386cd54"),
    "native": (10, "aa23b79551181be1320b7b227dcff99a920ce49f200407862dc231460d112e64"),
    "relation": (21, "2088fffbb28958699c878d85a46ce4e873ad95c0cf46bfefab7ff20d3ea34249"),
    "control": (23, "87e1bb1c46b1424a7865a56b9b3c5ca2606f45688cd36db8ed011ff13f6d9bb6"),
    "retained": (54, "4b7ac00ba6ef95c5b320b47f06c7da41b52141e2dbb02fda8f7daa06fa3d6041"),
    "excluded": (10, "dd8e7d905d15e6bedcced24683f9ade32f66761d1985585db0e16c83d8dc409f"),
}
EXPECTED_EXCLUDED_CLASS = {
    "unrelated_substitution_constructions": (6, "f4562ffd4bda5f7807a81ef97e6ad43413568d8a5356db2539c10cd09d1c4a29"),
    "other_number_or_map_siblings": (3, "33a8f3390310f6f7363288164f1484aff1e5b72a7d1d95563f394a32c378077b"),
    "continuous_billiard_sibling": (1, "edb3d63a27ebe39be135e098b4c94c24baf8d15be87f30fd606e54bee3a7d725"),
}
EXPECTED_BOOK_BROAD = {
    "candidate": (39, "ffbb3932df2b3c8a7e685606d258b53fca412616bd980feb082547157acdf175"),
    "native": (7, "918cc877b420f30fd49c00cc8e704bddebd7b880a55c200a26b9f71a3c5e39a3"),
    "relation": (4, "3de10a93c704adb58deed4f2d3a0cfb6b34e460dcbc75a94f7771ad2de308165"),
    "control": (18, "2b536082c690f27f9adcfe5e808677328d193c78325cfd1516379a79e0215dc4"),
    "excluded": (10, "dd8e7d905d15e6bedcced24683f9ade32f66761d1985585db0e16c83d8dc409f"),
}
EXPECTED_BOOK_BROAD_PATTERN_DIGEST = "6c82bec5d5841f99d267d2118c8476e0692cce476fb75cb1d3eaf5a6e422c494"
EXPECTED_INDEX_CLASS = {
    "native": (3, "34a183690752fe116d7d40d86e274df650e07999e6b2e4385babe027cc453801"),
    "relation": (8, "a1662b930c56719c1299b605640fcd8a0702e6209cb7fc91b559f9ea3424d3fd"),
    "control": (78, "dcc56644a9d3eed6d9e0d28957adfa0f3b4f5e12ad6b3192b168cba107fdc6cf"),
}
EXPECTED_INDEX_CONTENT = (
    897,
    "cfd508d5257c960ee983107dbf36edb3956358cbf26a3f480ee2ecf28aca75fe",
)
EXPECTED_INDEX_QUERY_MISSES = (
    70,
    "c4e5e5d45f81549b06bc536d37ae13ab52fe3ae1111f2f054cdb352ff1816f4d",
)
EXPECTED_INDEX_BROAD = (
    89,
    "051c16e838e3c444ed17f5b9ae0b3a1848d88629de9e7ef46d42bdf787762588",
)
EXPECTED_INDEX_DISPOSITION = {
    **EXPECTED_INDEX_CLASS,
    "unrelated": (808, "72812bae94b39a740c6d6fe6ea5c6b6fcce64d1a6fd6b2eb65084aba98da5028"),
}
EXPECTED_STRICT_MAIN_PARTITION = {
    "native": (5, "cdbd7d8b31b86c20d9479e4752e928f994af9b6f75083748502727e2b42c1306"),
    "relation": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "control": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "content": (5, "cdbd7d8b31b86c20d9479e4752e928f994af9b6f75083748502727e2b42c1306"),
}
EXPECTED_STRICT_NOTES_PARTITION = {
    "native": (5, "d4873fed46bf4a37ef7c7bedab9f3029ade58dac3658b0c68ba75b44d3eb11c1"),
    "relation": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "control": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "content": (5, "d4873fed46bf4a37ef7c7bedab9f3029ade58dac3658b0c68ba75b44d3eb11c1"),
}
EXPECTED_IMAGE_ROLE_PARTITION = {
    "native": (1, "f7ec2d2600c8998dd7ebb42ea2367dc30615d60a801383b4bcb319a5b376e6aa"),
    "relation": (11, "00bd70cfd79fd39cae2ddd384be3aaec1a513dad8b2740441d24a01e49d76005"),
    "control": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
}
EXPECTED_IMAGE_LEDGER = {
    "candidate_images": (12, "076dc9462bf81a5c4ee5628f077b0318ce13d72160d4166748c7da09a77ec082"),
    "governed_images": (12, "076dc9462bf81a5c4ee5628f077b0318ce13d72160d4166748c7da09a77ec082"),
    "excluded_images": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
}
EXPECTED_IMAGE_ASSET_MANIFEST = (
    12,
    "881c5c67fbf2aa6eb6bc6b8b0417b77df0057e24d657e72a08aac4f58d8cd2f5",
)
EXPECTED_RECORDS = {
    "semantic_guards": (21, "8112094ad87f1787f5650c4565fa78b822ee66cb80fa541a1255000bfefbcdb0"),
    "auxiliary_guards": (12, "b84109cafd1ae17a38fb7dcbffa45c92bff07a3b2bfeca322a9f3c03a82a4753"),
    "source_defects": (10, "c137056750f4ef29b5ba6e13d87819fefda33c6ca153d4862ec5570c692e863b"),
    "source_model": (25, "029bb5300680a73e18d29514c2d0f09faae857e2a1b00bc0dfcc0208b1baa742"),
    "image_roles": (12, "55161c0c700d86e0d513257bbd71861799946d7c617c18df71a35992df42809e"),
    "image_candidate_scopes": (4, "615705f9cf237254229715d1f22dcd873ce7b1f54102939f9ba940a8671d07dc"),
    "image_assembly_boundaries": (6, "5551ae2505d58b77967fd4dd336baef06110ec2c2673a4099cc88f11ddc7e438"),
    "excluded_line_hashes": (10, "220bf942fa96861e59bcd4f3502c4920ca0d1fe99e84ebfa2b52cad0cb425b1c"),
    "index_guards": (11, "467b1716325211c146f1aae08f0c7e1daef0c1e87c14bcf72bb5b6c394b2d08a"),
    "index_sentinels": (5, "72a8925a92877e7df8d2bde530e8e69ea3e49e856133b0c5bc25fa1ad4cce70d"),
    "index_dispositions": (897, "a59d61595547e58c06174a9de03e94bab30651ab258aeafb546697c51c7397b5"),
    "strict_main_dispositions": (5, "c3d025ac38e59d0ca0e0e68e87992cc7b2bf5c4d5aa3c602ce60067f503a8da8"),
    "strict_notes_dispositions": (5, "82c7798fd3a64b4d1980c1c2978a5a7fa2a55b142f9746051fc2bb45367ee468"),
    "split_boundary_witnesses": (8, "15f345d287cacea666c7def29e35ac23a8bde6e1a02af729d2b494be7729e6f4"),
}
EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
EXPECTED_SPLIT_MANIFEST_DIGEST = "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"
EXPECTED_SPLIT_CROSSWALK = (
    951,
    "e27565beb758a1fc38ba91e6ed88b51f88f0dfaa520a19119fa2b0ee3b5dbe06",
)
EXPECTED_SPLIT_CLASSES = {
    "EXACT": (
        927,
        "8544ef044b1262829e282d3796e944c4cb06c7a457ed7a72ff13c2f6bbcd3a2e",
        "775bcab706da1f6ccb2593795abd2367bee5be08c1d8c15daefe8fc0effa4b8b",
    ),
    "IMAGE_BASENAME": (
        12,
        "076dc9462bf81a5c4ee5628f077b0318ce13d72160d4166748c7da09a77ec082",
        "cbf5fa1defc30c189b27c03108997fe96686fccf657f542e44ae73f3b31343ee",
    ),
    "NORMALIZED": (
        9,
        "a0cf3d7306114a00b46afca8fb31c2a6b27b933a34203a34dce2ee6223afd9c6",
        "fa182a28d4f28dcd98a80ead6944e0ac98f6e0b46b5c06b7e23bd7c6720c526d",
    ),
    "OMITTED": (
        3,
        "702320d4042566d3575303518f06f2f8620f59e09b38d95f332dad5cd0831293",
        "d6d25144364ee45b8a9604ee7f4c9fb584c77035a08b7f223b36984618a4e4e1",
    ),
}
EXPECTED_SPLIT_NORMALIZED_MINIMUM = 0.995885
EXPECTED_LOGIC_RECORDS = (
    15,
    "96190c836c5526e2d4693132d7d7ca11a4cc25603e485a63662dbae8f1f3b289",
)
EXPECTED_AUDIT_DIGEST = "2726957389d256722469424e41ea2e92188ba5e30d7ab52c4df2598dd7250aa6"


def main(argv: list[str] | None = None) -> int:
    json_mode, argument = parse_args(sys.argv[1:] if argv is None else argv)
    book, source_root, repo_root = resolve_book(argument)
    atlas = source_root / "ANKoS-Atlas.md"
    catalog = repo_root / "ref/notes/CA-Types.csv"
    taxonomy = repo_root / "ref/notes/CA-Types.md"

    raw = book.read_bytes()
    lines = raw.decode("utf-8").splitlines()
    at = lambda number: lines[number - 1]
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
    query_partition = (
        set(NATIVE_EVIDENCE), set(RELATION_EVIDENCE),
        set(CONTROL_EVIDENCE), set(EXCLUDED),
    )
    sets = {
        "union": union,
        "pre_index": pre_index,
        "index_candidates": index_candidates,
        "query_native": pre_index & set(NATIVE_EVIDENCE),
        "query_relation": pre_index & set(RELATION_EVIDENCE),
        "query_control": pre_index & set(CONTROL_EVIDENCE),
        "query_excluded": pre_index & set(EXCLUDED),
        "native": set(NATIVE_EVIDENCE),
        "relation": set(RELATION_EVIDENCE),
        "control": set(CONTROL_EVIDENCE),
        "retained": set(RETAINED),
        "excluded": set(EXCLUDED),
    }
    set_ok = (
        set(sets) == set(EXPECTED_SET)
        and pre_index <= set().union(*query_partition)
        and sum(len(values & pre_index) for values in query_partition) == len(pre_index)
        and not RETAINED & EXCLUDED
        and frozenset().union(NATIVE_EVIDENCE, RELATION_EVIDENCE, CONTROL_EVIDENCE)
        == RETAINED
        and sum(map(len, (NATIVE_EVIDENCE, RELATION_EVIDENCE, CONTROL_EVIDENCE)))
        == len(RETAINED)
    )
    for name, values in sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_SET.get(name)
        set_ok &= good
        check("set_" + name, good, *actual)
    for name, values in EXCLUDED_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_EXCLUDED_CLASS.get(name)
        set_ok &= good
        check("excluded_" + name, good, *actual)
    set_ok &= (
        set(EXCLUDED_CLASS) == set(EXPECTED_EXCLUDED_CLASS)
        and frozenset().union(*EXCLUDED_CLASS.values()) == EXCLUDED
        and sum(map(len, EXCLUDED_CLASS.values())) == len(EXCLUDED)
    )
    check("query_partition", set_ok, len(pre_index - set().union(*query_partition)))

    book_broad_actual = {
        number
        for number, line in enumerate(lines[: INDEX_FIRST_LINE - 1], 1)
        if re.search(BOOK_BROAD_PATTERN, line, re.IGNORECASE)
    }
    book_broad_sets = {
        "candidate": book_broad_actual,
        "native": book_broad_actual & set(NATIVE_EVIDENCE),
        "relation": book_broad_actual & set(RELATION_EVIDENCE),
        "control": book_broad_actual & set(CONTROL_EVIDENCE),
        "excluded": book_broad_actual & set(EXCLUDED),
    }
    broad_union = set().union(
        book_broad_sets["native"], book_broad_sets["relation"],
        book_broad_sets["control"], book_broad_sets["excluded"],
    )
    book_broad_pattern_actual = digest_records({BOOK_BROAD_PATTERN})
    book_broad_ok = (
        book_broad_actual == set(BOOK_BROAD_CANDIDATES)
        and broad_union == book_broad_actual
        and sum(len(book_broad_sets[name]) for name in ("native", "relation", "control", "excluded"))
        == len(book_broad_actual)
        and book_broad_pattern_actual == EXPECTED_BOOK_BROAD_PATTERN_DIGEST
        and set(book_broad_sets) == set(EXPECTED_BOOK_BROAD)
    )
    for name, values in book_broad_sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_BOOK_BROAD.get(name)
        book_broad_ok &= good
        check("book_broad_" + name, good, *actual)
    check("book_broad_pattern", book_broad_pattern_actual == EXPECTED_BOOK_BROAD_PATTERN_DIGEST, book_broad_pattern_actual)
    check("book_broad_closure", book_broad_ok, len(book_broad_actual - broad_union))

    strict_main_sets = {
        "native": set(NATIVE_EVIDENCE & STRICT_MAIN_CONTENT),
        "relation": set(RELATION_EVIDENCE & STRICT_MAIN_CONTENT),
        "control": set(CONTROL_EVIDENCE & STRICT_MAIN_CONTENT),
        "content": set(STRICT_MAIN_CONTENT),
    }
    strict_main_live = {
        number for number in range(1850, 1859) if at(number).strip()
    }
    strict_main_ok = (
        strict_main_live == set(STRICT_MAIN_CONTENT)
        and set().union(*(strict_main_sets[name] for name in ("native", "relation", "control")))
        == strict_main_live
        and sum(len(strict_main_sets[name]) for name in ("native", "relation", "control"))
        == len(strict_main_live)
    )
    for name, values in strict_main_sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_STRICT_MAIN_PARTITION.get(name)
        strict_main_ok &= good
        check("strict_main_" + name, good, *actual)
    check("strict_main_closure", strict_main_ok, len(strict_main_live ^ set(STRICT_MAIN_CONTENT)))

    strict_notes_sets = {
        "native": set(NATIVE_EVIDENCE & STRICT_NOTES_CONTENT),
        "relation": set(RELATION_EVIDENCE & STRICT_NOTES_CONTENT),
        "control": set(CONTROL_EVIDENCE & STRICT_NOTES_CONTENT),
        "content": set(STRICT_NOTES_CONTENT),
    }
    strict_notes_live = {
        number for number in range(12587, 12596) if at(number).strip()
    }
    strict_notes_ok = (
        strict_notes_live == set(STRICT_NOTES_CONTENT)
        and set().union(*(strict_notes_sets[name] for name in ("native", "relation", "control")))
        == strict_notes_live
        and sum(len(strict_notes_sets[name]) for name in ("native", "relation", "control"))
        == len(strict_notes_live)
    )
    for name, values in strict_notes_sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_STRICT_NOTES_PARTITION.get(name)
        strict_notes_ok &= good
        check("strict_notes_" + name, good, *actual)
    check("strict_notes_closure", strict_notes_ok, len(strict_notes_live ^ set(STRICT_NOTES_CONTENT)))

    index_actual_content = {
        number
        for number in range(INDEX_CONTENT_FIRST_LINE, INDEX_CONTENT_LAST_LINE + 1)
        if at(number).strip()
    }
    index_broad_actual = {
        number
        for number in index_actual_content
        if re.search(INDEX_BROAD_PATTERN, at(number), re.IGNORECASE)
    }
    index_query_misses = index_broad_actual - index_candidates
    index_unrelated = index_actual_content - set(INDEX_SEMANTIC_UNIVERSE)
    index_disposition = {**INDEX_CLASS, "unrelated": frozenset(index_unrelated)}
    index_content_actual = (len(index_actual_content), digest(index_actual_content))
    index_broad_metric = (len(index_broad_actual), digest(index_broad_actual))
    index_miss_metric = (len(index_query_misses), digest(index_query_misses))
    index_records, index_guards_ok = occurrence_records(INDEX_ENTRY_GUARDS, lines)
    sentinel_records, sentinels_ok = occurrence_records(INDEX_FLATTENING_SENTINELS, lines)
    index_ok = (
        at(INDEX_FIRST_LINE) == "#### Index"
        and at(22458) == "#### Colophon"
        and index_content_actual == EXPECTED_INDEX_CONTENT
        and index_broad_actual == set(INDEX_BROAD_CANDIDATES)
        and index_broad_metric == EXPECTED_INDEX_BROAD
        and index_miss_metric == EXPECTED_INDEX_QUERY_MISSES
        and index_candidates <= index_broad_actual
        and INDEX_SEMANTIC_UNIVERSE == INDEX_BROAD_CANDIDATES
        and set(INDEX_CLASS) == set(EXPECTED_INDEX_CLASS)
        and frozenset().union(*INDEX_CLASS.values()) == INDEX_SEMANTIC_UNIVERSE
        and sum(map(len, INDEX_CLASS.values())) == len(INDEX_SEMANTIC_UNIVERSE)
        and set().union(*(set(values) for values in index_disposition.values()))
        == index_actual_content
        and sum(map(len, index_disposition.values())) == len(index_actual_content)
        and set(INDEX_ENTRY_GUARDS) == set(INDEX_CLASS["native"] | INDEX_CLASS["relation"])
        and index_guards_ok and sentinels_ok
    )
    check("index_content", index_content_actual == EXPECTED_INDEX_CONTENT, *index_content_actual)
    check("index_broad", index_broad_metric == EXPECTED_INDEX_BROAD, *index_broad_metric)
    check("index_query_misses", index_miss_metric == EXPECTED_INDEX_QUERY_MISSES, *index_miss_metric)
    for name, values in INDEX_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_INDEX_CLASS.get(name)
        index_ok &= good
        check("index_class_" + name, good, *actual)
    for name, values in index_disposition.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_INDEX_DISPOSITION.get(name)
        index_ok &= good
        check("index_disposition_" + name, good, *actual)
    check("index_closure", index_ok, len(index_actual_content - set().union(*(set(v) for v in index_disposition.values()))))

    semantic_records = {
        f"{kind}:{number}:{'|'.join(positive)}!{'|'.join(negative)}"
        for kind, number, positive, negative in SOURCE_SEMANTIC_GUARDS
    }
    semantic_ok = all(
        positive
        and all(needle in at(number) for needle in positive)
        and all(needle not in at(number) for needle in negative)
        for _, number, positive, negative in SOURCE_SEMANTIC_GUARDS
    )

    auxiliary_sources = {
        "catalog": catalog.read_text(encoding="utf-8").splitlines(),
        "taxonomy": taxonomy.read_text(encoding="utf-8").splitlines(),
        "atlas": atlas.read_text(encoding="utf-8").splitlines(),
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
        and not hits["Q00"]
    )

    defect_records = set(SOURCE_DEFECT_RECORDS)
    model_records = set(SOURCE_MODEL_RECORDS)
    image_role_records = set(IMAGE_ROLE_RECORDS)
    candidate_scope_records = {
        f"{name}:{start}-{end}:{','.join(map(str, sorted(expected)))}"
        for name, (start, end, expected) in IMAGE_CANDIDATE_SCOPES.items()
    }
    exclusion_hash_records = {
        f"{number}:{hashlib.sha256(at(number).encode('utf-8')).hexdigest()}"
        for number in EXCLUDED
    }
    index_guard_records = index_records
    index_disposition_records = {
        f"{role}:{number}:{hashlib.sha256(at(number).encode('utf-8')).hexdigest()}"
        for role, values in index_disposition.items() for number in values
    }
    strict_main_records = {
        f"{role}:{number}:{hashlib.sha256(at(number).encode('utf-8')).hexdigest()}"
        for role, values in strict_main_sets.items() if role != "content"
        for number in values
    }
    strict_notes_records = {
        f"{role}:{number}:{hashlib.sha256(at(number).encode('utf-8')).hexdigest()}"
        for role, values in strict_notes_sets.items() if role != "content"
        for number in values
    }
    record_actuals = {
        "semantic_guards": (len(semantic_records), digest_records(semantic_records)),
        "auxiliary_guards": (len(auxiliary_records), digest_records(auxiliary_records)),
        "source_defects": (len(defect_records), digest_records(defect_records)),
        "source_model": (len(model_records), digest_records(model_records)),
        "image_roles": (len(image_role_records), digest_records(image_role_records)),
        "image_candidate_scopes": (len(candidate_scope_records), digest_records(candidate_scope_records)),
        "image_assembly_boundaries": (len(IMAGE_ASSEMBLY_BOUNDARIES), digest_records(IMAGE_ASSEMBLY_BOUNDARIES)),
        "excluded_line_hashes": (len(exclusion_hash_records), digest_records(exclusion_hash_records)),
        "index_guards": (len(index_guard_records), digest_records(index_guard_records)),
        "index_sentinels": (len(sentinel_records), digest_records(sentinel_records)),
        "index_dispositions": (len(index_disposition_records), digest_records(index_disposition_records)),
        "strict_main_dispositions": (len(strict_main_records), digest_records(strict_main_records)),
        "strict_notes_dispositions": (len(strict_notes_records), digest_records(strict_notes_records)),
        "split_boundary_witnesses": (len(SPLIT_BOUNDARY_WITNESSES), digest_records(SPLIT_BOUNDARY_WITNESSES)),
    }
    record_ok = (
        set(record_actuals) == set(EXPECTED_RECORDS)
        and semantic_ok and auxiliary_ok
        and len(defect_records) == len(SOURCE_DEFECT_RECORDS)
        and len(model_records) == len(SOURCE_MODEL_RECORDS)
        and len(image_role_records) == len(IMAGE_ROLE_RECORDS)
    )
    for name, actual in record_actuals.items():
        good = actual == EXPECTED_RECORDS.get(name)
        record_ok &= good
        check("record_" + name, good, *actual)
    check("record_contracts", record_ok)

    image_partition = {
        "native": NATIVE_IMAGE_LINES,
        "relation": RELATION_IMAGE_LINES,
        "control": CONTROL_IMAGE_LINES,
    }
    image_ledger = {
        "candidate_images": CANDIDATE_IMAGE_LINES,
        "governed_images": GOVERNED_IMAGE_LINES,
        "excluded_images": EXCLUDED_IMAGE_LINES,
    }
    image_roles_actual = {
        name: (len(values), digest(values)) for name, values in image_partition.items()
    }
    image_ledger_actual = {
        name: (len(values), digest(values)) for name, values in image_ledger.items()
    }
    candidate_scope_ok = True
    candidate_scope_union: set[int] = set()
    book_images = {
        number
        for number, line in enumerate(lines, 1)
        if IMAGE_RE.fullmatch(line)
    }
    for _, (start, end, expected) in IMAGE_CANDIDATE_SCOPES.items():
        actual = {number for number in book_images if start <= number <= end}
        candidate_scope_ok &= actual == set(expected)
        candidate_scope_union.update(actual)
    images_ok = (
        image_roles_actual == EXPECTED_IMAGE_ROLE_PARTITION
        and image_ledger_actual == EXPECTED_IMAGE_LEDGER
        and frozenset().union(*image_partition.values()) == GOVERNED_IMAGE_LINES
        and sum(map(len, image_partition.values())) == len(GOVERNED_IMAGE_LINES)
        and CANDIDATE_IMAGE_LINES == GOVERNED_IMAGE_LINES | EXCLUDED_IMAGE_LINES
        and not GOVERNED_IMAGE_LINES & EXCLUDED_IMAGE_LINES
        and not UNRESOLVED_IMAGE_LINES
        and candidate_scope_ok
        and candidate_scope_union == set(CANDIDATE_IMAGE_LINES)
        and LIMITED_TRANSCRIBED_IMAGE_LINES == NATIVE_IMAGE_LINES
        and HASH_BOUND_IMAGE_LINES == GOVERNED_IMAGE_LINES
        and LIMITED_TRANSCRIBED_IMAGE_LINES <= HASH_BOUND_IMAGE_LINES
        and not PIXEL_REPLAYED_IMAGE_LINES
    )
    for name, actual in image_roles_actual.items():
        check("images_" + name, actual == EXPECTED_IMAGE_ROLE_PARTITION.get(name), *actual)
    for name, actual in image_ledger_actual.items():
        check("images_" + name, actual == EXPECTED_IMAGE_LEDGER.get(name), *actual)

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
        path for path in source_root.rglob("*.md")
        if path.resolve() not in {book.resolve(), atlas.resolve()}
    )
    relative_paths = [path.relative_to(source_root).as_posix() for path in split_paths]
    split_manifest = [
        f"{relative}\0{len(path.read_bytes())}\0{sha256(path)}"
        for path, relative in zip(split_paths, relative_paths, strict=True)
    ]
    split_manifest_ok = (
        len(split_paths) == EXPECTED_SPLIT_FILE_COUNT
        and digest_records(relative_paths) == EXPECTED_SPLIT_PATHS_DIGEST
        and digest_records(split_manifest) == EXPECTED_SPLIT_MANIFEST_DIGEST
    )
    check("split_manifest", split_manifest_ok, len(split_paths), digest_records(relative_paths), digest_records(split_manifest))

    split_text: dict[str, str] = {}
    for path, relative in zip(split_paths, relative_paths, strict=True):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            split_text[f"{relative}:{number}"] = line

    crosswalk_lines = RETAINED | frozenset(index_actual_content)
    crosswalk_records: set[str] = set()
    class_lines: dict[str, set[int]] = {
        name: set() for name in ("EXACT", "IMAGE_BASENAME", "NORMALIZED", "OMITTED")
    }
    class_records: dict[str, set[str]] = {name: set() for name in class_lines}
    normalized_scores: list[float] = []
    split_join_ok = True
    omission_reason_by_line = {
        number: reason for reason, values in SPLIT_OMISSION_GROUPS.items()
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
    split_class_actual = {
        name: (len(class_lines[name]), digest(class_lines[name]), digest_records(class_records[name]))
        for name in class_lines
    }
    normalized_minimum = min(normalized_scores, default=1.0)
    split_join_ok &= (
        crosswalk_actual == EXPECTED_SPLIT_CROSSWALK
        and split_class_actual == EXPECTED_SPLIT_CLASSES
        and round(normalized_minimum, 6) == EXPECTED_SPLIT_NORMALIZED_MINIMUM
        and len(crosswalk_records) == len(crosswalk_lines)
        and set().union(*class_lines.values()) == set(crosswalk_lines)
        and sum(map(len, class_lines.values())) == len(crosswalk_lines)
        and class_lines["OMITTED"] == set(SPLIT_OMISSION_LINES)
    )
    check("split_crosswalk", split_join_ok, *crosswalk_actual, f"normalized_min={normalized_minimum:.6f}")
    for name, actual in split_class_actual.items():
        check("split_class_" + name, actual == EXPECTED_SPLIT_CLASSES.get(name), *actual)

    actual_logic_records = logic_records()
    logic_actual = (len(actual_logic_records), digest_records(actual_logic_records))
    logic_ok = logic_actual == EXPECTED_LOGIC_RECORDS
    check("source_logic", logic_ok, *logic_actual)

    unresolved_total = (
        len(pre_index - set().union(*query_partition))
        + len(book_broad_actual - broad_union)
        + len(strict_main_live ^ set(STRICT_MAIN_CONTENT))
        + len(strict_notes_live ^ set(STRICT_NOTES_CONTENT))
        + len(index_actual_content - set().union(*(set(v) for v in index_disposition.values())))
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
        f"book-broad:{name}:{len(values)}:{digest(values)}" for name, values in book_broad_sets.items()
    } | {
        f"strict-main:{name}:{len(values)}:{digest(values)}" for name, values in strict_main_sets.items()
    } | {
        f"strict-notes:{name}:{len(values)}:{digest(values)}" for name, values in strict_notes_sets.items()
    } | {
        f"index:{name}:{len(values)}:{digest(values)}" for name, values in index_disposition.items()
    } | {
        f"record:{name}:{count}:{record_digest}" for name, (count, record_digest) in record_actuals.items()
    } | {
        f"split:{name}:{count}:{line_digest}:{record_digest}"
        for name, (count, line_digest, record_digest) in split_class_actual.items()
    } | {
        f"book-broad-pattern:{book_broad_pattern_actual}",
        f"index-content:{index_content_actual[0]}:{index_content_actual[1]}",
        f"index-broad:{index_broad_metric[0]}:{index_broad_metric[1]}",
        f"index-query-misses:{index_miss_metric[0]}:{index_miss_metric[1]}",
        f"image-manifest:{image_manifest_actual[0]}:{image_manifest_actual[1]}",
        f"image-boundary:hash-bound={len(HASH_BOUND_IMAGE_LINES)}:limited={len(LIMITED_TRANSCRIBED_IMAGE_LINES)}:pixel-replayed={len(PIXEL_REPLAYED_IMAGE_LINES)}",
        f"logic:{logic_actual[0]}:{logic_actual[1]}",
        f"unresolved:{unresolved_total}",
    }
    audit_digest = digest_records(audit_records)
    check("audit_digest", audit_digest == EXPECTED_AUDIT_DIGEST, audit_digest)

    if json_mode:
        payload = {
            "audit_digest": audit_digest,
            "book_broad": {
                "candidate": len(book_broad_actual),
                "excluded": len(book_broad_sets["excluded"]),
                "unresolved": len(book_broad_actual - broad_union),
            },
            "images": {
                "candidate": len(CANDIDATE_IMAGE_LINES),
                "control": len(CONTROL_IMAGE_LINES),
                "excluded": len(EXCLUDED_IMAGE_LINES),
                "hash_bound": len(HASH_BOUND_IMAGE_LINES),
                "limited_transcribed": len(LIMITED_TRANSCRIBED_IMAGE_LINES),
                "native": len(NATIVE_IMAGE_LINES),
                "relation": len(RELATION_IMAGE_LINES),
                "unresolved": len(UNRESOLVED_IMAGE_LINES),
            },
            "index": {
                "content": len(index_actual_content),
                "query_misses": len(index_query_misses),
                "relevant": len(INDEX_SEMANTIC_UNIVERSE),
                "unrelated": len(index_unrelated),
                "unresolved": 0,
            },
            "queries": len(QUERIES),
            "query_union": len(union),
            "retained": len(RETAINED),
            "split_crosswalk": len(crosswalk_records),
            "status": "PASS" if ok else "FAIL",
            "strict_main": len(STRICT_MAIN_CONTENT),
            "strict_notes": len(STRICT_NOTES_CONTENT),
            "unresolved_total": unresolved_total,
        }
        print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    else:
        for name, good, metrics in output:
            print(name, "OK" if good else "MISMATCH", *metrics)
        print(
            "T42 source oracle:", "PASS" if ok else "FAIL",
            f"audit={audit_digest}",
            f"queries={len(QUERIES)}/union={len(union)}",
            f"book-broad={len(book_broad_actual)}/closure={len(book_broad_actual - broad_union)}",
            f"retained={len(RETAINED)}(N/R/C={len(NATIVE_EVIDENCE)}/{len(RELATION_EVIDENCE)}/{len(CONTROL_EVIDENCE)})",
            f"strict-main={len(STRICT_MAIN_CONTENT)}/strict-notes={len(STRICT_NOTES_CONTENT)}",
            f"index={len(index_actual_content)}(N/R/C/X={len(INDEX_CLASS['native'])}/{len(INDEX_CLASS['relation'])}/{len(INDEX_CLASS['control'])}/{len(index_unrelated)})",
            f"images={len(CANDIDATE_IMAGE_LINES)}(N/R/C={len(NATIVE_IMAGE_LINES)}/{len(RELATION_IMAGE_LINES)}/{len(CONTROL_IMAGE_LINES)},hash-bound/limited={len(HASH_BOUND_IMAGE_LINES)}/{len(LIMITED_TRANSCRIBED_IMAGE_LINES)})",
            f"split={len(crosswalk_records)}",
            f"unresolved={unresolved_total}",
        )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
