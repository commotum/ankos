#!/usr/bin/env python3
"""Frozen source-evidence audit for T15 creation/destruction substitution.

The catalog gives this continuation of Chapter 3 a convenient analytic name,
but the Book does not use that heading.  It says instead that elements can
disappear and that creation and destruction can balance.  This oracle freezes
the complete line-oriented search union, dispositions, actual-Index routes,
split-source reverse joins, and the important extraction limitations:

* the prose never literally says ``empty replacement`` or ``epsilon``;
* the displayed T15 rules live in images and have no Notes transcription;
* disappearance, a T14 source that is ineligible for lack of a right neighbor,
  and an extinction outcome are three different claims; and
* text-transcribed empty right-hand sides occur in a T17 tag rule, a T20
  bracket-string observer encoding, and a T30 multiway rewrite rule; none is a
  native T15 table and their different schedules are not interchangeable.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


if not __debug__:
    raise RuntimeError("T15 source oracle requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "ref/A-New-Kind-of-Science"
DEFAULT_BOOK = SOURCE_ROOT / "A-New-Kind-of-Science.md"
ATLAS = SOURCE_ROOT / "ANKoS-Atlas.md"
CATALOG = ROOT / "ref/notes/CA-Types.csv"
TAXONOMY = ROOT / "ref/notes/CA-Types.md"

INDEX_FIRST_LINE = 20826
EXPECTED_BOOK_LINES = 22498
EXPECTED_BOOK_SHA256 = (
    "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"
)
EXPECTED_ATLAS_SHA256 = (
    "5ffab93f0007bbeb5da60af7cc08570f9a358c9f9f94e37c5e00f9fc0997bc8a"
)
EXPECTED_CATALOG_SHA256 = (
    "26cef05af1155f80bc301900d2df95469a90de027ba860730519d25d096c2b73"
)
EXPECTED_TAXONOMY_SHA256 = (
    "4c30fe079b2fb8f69e4c8c0dde3d59065227d4224cbe4b7693a17c0126cc3f1a"
)


# Q00 freezes the absence of the catalog's analytic family name.  Q01 sweeps
# and dispositions every occurrence of the broad source family (all 288
# lines).  Q02--Q07 cover disappearance, creation/destruction, balance,
# extinction, and broad lexical false positives.  Q08--Q10 and Q16 freeze
# terminology absences rather than silently converting prose into notation.
# Q11--Q15 cover shared generation, nonempty predecessor, parallel schedule,
# order, and rendering.  Q17 follows L-system aliases.  Q18 covers every
# observed source arrow spelling plus list/string empty RHS notation.  It separates a T17
# empty appendant, a T20 observer's removal of literal ``e`` during bracket
# encoding, and a T30 multiway transition with an empty replacement string.
# Q19--Q21 close the adjacent T14, T16, and T17 schedule/outcome boundaries.
QUERIES = {
    "Q00": r"\bcreation(?:[\s-]+)destruction(?:[\s-]+)substitution systems?\b",
    "Q01": r"\bsubstitution systems?\b",
    "Q02": (
        r"\belements can simply disappear\b|"
        r"\brate of such disappearances\b|"
        r"\btoo (?:few|many) disappearances\b"
    ),
    "Q03": (
        r"\bcreation and destruction of elements\b|"
        r"\belements (?:are )?created and destroyed\b|"
        r"\baddition or subtraction of elements\b"
    ),
    "Q04": (
        r"\balmost perfectly balanced\b|"
        r"\bbalanced closely enough\b|"
        r"\bslow growth\b|"
        r"\bgrows? by only a fixed amount at each step\b|"
        r"\bincreasing .* only by a fixed amount at each step\b"
    ),
    "Q05": (
        r"\b(?:extinction|extinct)\b|"
        r"\b(?:die|dies|died|dying) out\b|"
        r"\ball (?:the )?elements are eventually removed from the sequence\b"
    ),
    "Q06": r"\bdisappear(?:s|ed|ing|ance|ances)?\b",
    "Q07": r"\bdestruct(?:ion|ive|ively)\b|\bdestroy(?:s|ed|ing)?\b",
    "Q08": (
        r"\bempty (?:replacement|block|word|string|sequence)\b|"
        r"\b(?:replacement|block|word|string|sequence) "
        r"(?:is |be |being )?empty\b|"
        r"\breplac(?:e|ed|ing) (?:it |them |an? element )?"
        r"(?:by|with) nothing\b|"
        r"\b(?:no|zero) new elements\b"
    ),
    "Q09": r"\berasing\b|\bnon[- ]?erasing\b|\berasure\b",
    "Q10": r"\bepsilon\b|ε",
    "Q11": r"\bSSEvolveList\b|Flatten\[# /\. rule\]",
    "Q12": (
        r"\btotal number of elements never decreases\b|"
        r"\bevery single element should be replaced by at least one new element\b"
    ),
    "Q13": (
        r"\boperate in parallel on all the elements\b|"
        r"\boperating in parallel on all the elements\b|"
        r"\breplacing each element in such a string by a new sequence of elements\b"
    ),
    "Q14": (
        r"\bonly the order of elements is ever significant\b|"
        r"\bchange its position as a result of the addition or subtraction\b"
    ),
    "Q15": (
        r"\bboxes representing each element are scaled to keep the total width "
        r"the same\b|\bon the right each box has a fixed size\b"
    ),
    "Q16": r"\bpages? 8[67]\b",
    "Q17": r"\b(?:D?0L|D?1L|L) systems?\b|\bLindenmayer\b",
    "Q18": r'(?:\\longrightarrow|\\rightarrow|\\mapsto|\\to|->|:>)\s*(?:\\?\{\s*\\?\}|"")',
    "Q19": (
        r"\brightmost element is always dropped\b|"
        r"\bno rule is given for how to replace it\b"
    ),
    "Q20": (
        r"\bfirst such sequence that is found\b|"
        r"\bonly one replacement is ever done at each step\b"
    ),
    "Q21": (
        r"Length\[#\] < n|"
        r"\ball (?:the )?elements are eventually removed from the sequence\b"
    ),
}

DIRECT_CREATION_STREAM_RX = re.compile(
    r"\bcreation and destruction of elements\b|"
    r"\belements (?:are )?created and destroyed\b|"
    r"\baddition or subtraction of elements\b",
    re.IGNORECASE,
)


# Expected tuple: total, pre-Index, actual-Index, digest of ascending line set.
EXPECTED_QUERY = {
    "Q00": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q01": (288, 213, 75, "3f49076beb5b70231b930b882a16d2ed56dee504de8dcccb40e13d8f9a782c3a"),
    "Q02": (1, 1, 0, "a73060afb61efe1b7c817645d00c342df02407f65435a64c88d251d56150ff42"),
    "Q03": (4, 4, 0, "f4dea89547829ca3eb90cc6ccf470ee57a981154790523aa2dd5369b631092bc"),
    "Q04": (8, 7, 1, "7b8f7c0d1c11ecb219054d99918619cbaac6d7f027d6f3144101788fe78f98a4"),
    "Q05": (22, 22, 0, "04cd218b1ffd2847fdb8f5969bb2047a858caece3ddff92b4451eda741a6831d"),
    "Q06": (15, 15, 0, "9955ae12f7baf0194ee8727547d47c8a9f8c27913f4533ee1a9e05c15d5ff691"),
    "Q07": (12, 12, 0, "7cf12db77e1f39d4720f7732abb6ab0cdbddf398d6e996c939a46dc24df7414b"),
    "Q08": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q09": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q10": (4, 3, 1, "7e24f58d15b7c14381f21dfa11736cd43c4085d0530882569af17d30989d71cc"),
    "Q11": (2, 2, 0, "ca6aa7158a3f2d0cb45814a50566200e59a6fe3695a4b59163dac98f7c11a705"),
    "Q12": (1, 1, 0, "582c0168ba17eac49642bc85ae623204069e8d6ea06cf45af11e7de46ea31d18"),
    "Q13": (1, 1, 0, "8dfd13f4376053626e97eb7221d469013cae9bc031027e64f0db2ec114f8ffd9"),
    "Q14": (1, 1, 0, "6db44caad5c968a5ec334024daa615d29998fa79f82797cc12141871d0ffbd7b"),
    "Q15": (1, 1, 0, "340ab11db8d1a7435cb4b4a0492a9eee7b8e388e3e4a1714bcd3b69df3d8f1e1"),
    "Q16": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q17": (9, 4, 5, "b4b84b2c1ba9fff3da3ecfb0bcdf3f15212b09ff151d6bd3061e734928d576f0"),
    "Q18": (3, 3, 0, "3d42270f3b8ff87a098061cea8e7386f61f5ba691c82e863dc91160ba66feb55"),
    "Q19": (1, 1, 0, "f00f2e7bca65e9f8409fdb3bcddfa031664224255d7bd2f6b3de8ff11ababe20"),
    "Q20": (2, 2, 0, "660eb1b620d8fcff0db511647b3516e8f26a1acc690c960127cc267f919954f4"),
    "Q21": (2, 2, 0, "a588fe146215a0363439a99ed7254df685585fe50fbadeabe313abe80d9ef0f9"),
}


# Search-hit lines retained after every pre-Index query hit was inspected.
# T13/T14/T16/T17 and CA-emulation lines are retained only as explicit
# boundaries or relations; they are not promoted into native T15 mechanics.
MATCHED_RETAINED = frozenset(
    {
        980,
        984,
        992,
        1018,
        1022,
        1026,
        1028,
        1030,
        1032,
        1038,
        1040,
        1042,
        1046,
        1050,
        1052,
        1054,
        1058,
        1060,
        1062,
        1132,
        2358,
        7940,
        7948,
        7950,
        12097,
        12099,
        12101,
        12109,
        12136,
        12251,
        12298,
        12300,
    }
)

# Non-query lines needed to preserve the fixed-array/neighbor-independent
# setup, all four T15 image references, the complete nonempty T14 predecessor
# table, and its source-order generation operator.
GOVERNED_CONTINUATIONS = frozenset(
    {982, 986, 1034, 1036, 1044, 1048, 12111, 12113}
)
RETAINED = MATCHED_RETAINED | GOVERNED_CONTINUATIONS

# Q18's non-T17 hits are explicitly excluded.  BOOK:12432 maps literal ``e``
# to an empty list only while observing a T20 expression as a bracket string.
# BOOK:13953 is a genuine empty-string T30 multiway rewrite, but its match and
# branching successor schedule is not T15 ordered generation.
EMPTY_RHS_EXCLUDED_CONTROLS = {
    12432: "T20 bracket-string observer encoding",
    13953: "T30 multiway empty-string transition",
}


EXPECTED_SET = {
    "union": (351, "e0a877e8d80f232e52fbe579f4baa1d4a4da14e8d8573b58d997207e50a39ead"),
    "pre_index_union": (273, "ca4b700251ed6fdb25ed5b5e9ecc70cff5e6ba94c02e341319dc68f0c57a8ea0"),
    "index": (78, "e811eee57e862b90876a86bfa6096928dc6e122e2ac31bac663397c7314e576f"),
    "matched_retained": (32, "5763517afb52b5b2c6843e5ab69f424d3d26ef7a45bb5936f95c04f6faa0cbd5"),
    "governed_continuations": (8, "c43d14e3c2e389ccd0d3fb8bc2f1767df0962596bd79eec328e06fb05af8a420"),
    "retained": (40, "03fc9177af658074d7a276757fcc742a1afb3e5fe976ec6b08d438c1a57f7e73"),
    "excluded": (241, "7c3a93ce4cf56e72940e48578ffd3347d4ef3544a327d0b3edbb6f82b43114f3"),
}

# The actual Index has no creation/destruction heading.  These are broad
# substitution/L-system routes to pages 82--87 plus the adjacent
# neighbor-independent boundary; the remaining 70 Index hits are navigation
# noise or unrelated uses of the query terms.
INDEX_RELEVANT = frozenset(
    {20828, 21068, 21422, 21461, 21652, 21656, 22114, 22144}
)
EXPECTED_INDEX_RELEVANT_DIGEST = (
    "ebacb9026b322176d8c00148695cd14a498b8cf532eb41a3e94a131658d0cdbe"
)
EXPECTED_INDEX_EXCLUDED = (
    70,
    "19c5b66001fde701ef924ccc31d14e66e98d3180b613df3ab685f46aa20116b6",
)


EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = (
    "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
)
EXPECTED_SPLIT_MANIFEST_DIGEST = (
    "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"
)
EXPECTED_SPLIT_QUERY_RECORDS = (
    350,
    "e2404716c0ac15af08929655a8de9b0c08f29a4cbdcadc27f3b5ed54cc4926d7",
)
EXPECTED_SPLIT_EXACT_QUERY_RECORDS = (
    321,
    "771931cf60fead5c4e6d82187701436f5e7bcd40c00efe916f5d1971a694bee5",
)

# Every non-exact split query hit is joined to its canonical monolith line.
# Differences are punctuation/OCR repair, merged prose, or image path style;
# none supplies a new T15 rule transcription.
SPLIT_NONEXACT_QUERY_WITNESSES = {
    "BACK-MATTER/Colophon/Colophon.md:4909": (22352,),
    "BACK-MATTER/Colophon/Colophon.md:90": (17533,),
    "BACK-MATTER/Index/Index.md:11": (12099,),
    "BACK-MATTER/Index/Index.md:1171": (13268,),
    "BACK-MATTER/Index/Index.md:154": (12249,),
    "BACK-MATTER/Index/Index.md:1584": (13683,),
    "BACK-MATTER/Index/Index.md:166": (12261,),
    "BACK-MATTER/Index/Index.md:203": (12298,),
    "BACK-MATTER/Index/Index.md:259": (12356,),
    "BACK-MATTER/Index/Index.md:48": (12136,),
    "BACK-MATTER/Index/Index.md:887": (12984,),
    "CHAPTERS/10-Processes-of-Perception-and-Analysis/Processes-of-Perception-and-Analysis.md:689": (7278,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:249": (7950,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:251": (7952,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:321": (8022,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:327": (8028,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:329": (8030,),
    "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:375": (1058,),
    "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:309": (1850,),
    "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:315": (1856,),
    "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:317": (1858,),
    "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:165": (2308,),
    "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:177": (2320,),
    "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:203": (2350,),
    "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:217": (2366,),
    "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:339": (2508,),
    "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:369": (2540,),
    "CHAPTERS/9-Fundamental-Physics/Fundamental-Physics.md:825": (5990,),
    "FRONT-MATTER/Preface/Preface.md:58": (144,),
}
EXPECTED_SPLIT_NONEXACT_QUERY_RECORDS_DIGEST = (
    "d620652df557f5f4b738dd00edd21ed09c6fc0c4c0038ff9d9531c4633306a81"
)
EXPECTED_SPLIT_DIRECT_CREATION_PATHS = frozenset(
    {"CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md"}
)
EXPECTED_SPLIT_DIRECT_CREATION_PATHS_DIGEST = (
    "d089d3ae5d4cdbf20820d4076948cf2efc00ee4788cf5d2dfd7dffa48ce8b87c"
)

EXPECTED_EXACT_RETAINED_MIRRORS = (
    30,
    "08e225459891a1a83162540779c46f4f97e990321eaf80515e33c9213bf04aab",
)
SPLIT_NONEXACT_RETAINED = frozenset(
    {1034, 1036, 1044, 1048, 1058, 7950, 12099, 12111, 12136, 12298}
)
EXPECTED_SPLIT_NONEXACT_RETAINED_DIGEST = (
    "e72328a98d94913fbe202baa74acf36dd0bb0f3bf20f285717474f73f406f6a9"
)
SPLIT_NONEXACT_RETAINED_WITNESSES = {
    1034: "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:351",
    1036: "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:353",
    1044: "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:361",
    1048: "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:365",
    1058: "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:375",
    7950: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:249",
    12099: "BACK-MATTER/Index/Index.md:11",
    12111: "BACK-MATTER/Index/Index.md:23",
    12136: "BACK-MATTER/Index/Index.md:48",
    12298: "BACK-MATTER/Index/Index.md:203",
}
EXPECTED_SPLIT_RETAINED_WITNESS_DIGEST = (
    "20d93540794ff4bb34d4ca34869b97c8a3efd9578437c4496783c4973ebbc09c"
)


EXPECTED_ATLAS_LINES = 542
EXPECTED_ATLAS_QUERY_LINES = frozenset({7, 89, 93, 181})
EXPECTED_ATLAS_QUERY_DIGEST = (
    "f452bb159d6a337808c86084e3600ac0a159579c7debc7d8b478b4ebae560e06"
)


def digest(lines: set[int] | frozenset[int]) -> str:
    payload = ",".join(map(str, sorted(lines))).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_records(records: set[str] | list[str]) -> str:
    payload = "\n".join(sorted(records)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def t14_notes_step(word: list[int]) -> list[int]:
    """Exact nonempty T14 table used only to guard the T14/T15 boundary."""

    table = {
        (1, 1): (0, 1),
        (1, 0): (1, 0),
        (0, 1): (0,),
        (0, 0): (0, 1),
    }
    assert all(table.values())
    result: list[int] = []
    for index in range(max(0, len(word) - 1)):
        result.extend(table[(word[index], word[index + 1])])
    return result


def main() -> int:
    if len(sys.argv) > 2:
        raise SystemExit("usage: 31-T15-source-oracle.py [BOOK]")
    book = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else DEFAULT_BOOK
    raw = book.read_bytes()
    text = raw.decode("utf-8")
    lines = text.splitlines()
    source_ok = (
        len(lines) == EXPECTED_BOOK_LINES
        and hashlib.sha256(raw).hexdigest() == EXPECTED_BOOK_SHA256
        and sha256(ATLAS) == EXPECTED_ATLAS_SHA256
        and sha256(CATALOG) == EXPECTED_CATALOG_SHA256
        and sha256(TAXONOMY) == EXPECTED_TAXONOMY_SHA256
        and len(DIRECT_CREATION_STREAM_RX.findall(text)) == 6
    )
    ok = source_ok
    print("source", "OK" if source_ok else "MISMATCH")

    hits: dict[str, set[int]] = {}
    for name, pattern in QUERIES.items():
        rx = re.compile(pattern, re.IGNORECASE)
        found = {n for n, line in enumerate(lines, 1) if rx.search(line)}
        hits[name] = found
        actual = (
            len(found),
            sum(n < INDEX_FIRST_LINE for n in found),
            sum(n >= INDEX_FIRST_LINE for n in found),
            digest(found),
        )
        good = actual == EXPECTED_QUERY[name]
        ok &= good
        print(name, "OK" if good else "MISMATCH", *actual)

    union = set().union(*hits.values())
    pre_index_union = {n for n in union if n < INDEX_FIRST_LINE}
    index = union - pre_index_union
    matched_retained = pre_index_union & MATCHED_RETAINED
    excluded = pre_index_union - MATCHED_RETAINED
    sets = {
        "union": union,
        "pre_index_union": pre_index_union,
        "index": index,
        "matched_retained": matched_retained,
        "governed_continuations": set(GOVERNED_CONTINUATIONS),
        "retained": set(RETAINED),
        "excluded": excluded,
    }
    for name, values in sets.items():
        expected_count, expected_digest = EXPECTED_SET[name]
        actual_digest = digest(values)
        good = len(values) == expected_count and actual_digest == expected_digest
        ok &= good
        print(name, "OK" if good else "MISMATCH", len(values), actual_digest)

    index_excluded = index - INDEX_RELEVANT
    index_ok = (
        INDEX_RELEVANT <= index
        and digest(INDEX_RELEVANT) == EXPECTED_INDEX_RELEVANT_DIGEST
        and (len(index_excluded), digest(index_excluded)) == EXPECTED_INDEX_EXCLUDED
        and "1L systems, 85–88, 893" in lines[20827]
        and "D1L systems, 85–87" in lines[21067]
        and "L systems, 82–87" in lines[21421]
        and "Lindenmayer, Aristid" in lines[21460]
        and "Neighbor-dependent substitution systems, 85–87" in lines[21651]
        and "Neighbor-independent substitution systems, 82–85" in lines[21655]
        and "and L systems, 893" in lines[22113]
        and "Substitution systems, 82-87" in lines[22143]
    )
    ok &= index_ok
    print(
        "actual_index",
        "OK" if index_ok else "MISMATCH",
        len(INDEX_RELEVANT),
        len(index_excluded),
        digest(INDEX_RELEVANT),
        digest(index_excluded),
    )

    # Freeze what the line source does and does not establish.  BOOK:1028
    # directly establishes disappearing elements and possible extinction, but
    # does not specify an empty word glyph or what a subsequent step on an
    # empty configuration means.  The exact T15 tables are image evidence.
    # BOOK:1022/T14 instead drops an endpoint because it has no eligible pair;
    # its complete Notes table has no empty row.  BOOK:12298 is a real empty
    # output, but for T17's different queue schedule.  BOOK:12432 is a second
    # syntactic empty RHS used only to erase ``e`` in a T20 bracket observer.
    # BOOK:13953 has a genuine T30 empty-string rewrite under a branching
    # match schedule.  Neither line is a T15 transition row.
    core_text = "\n".join(lines[1025:1052])
    source_semantics_ok = (
        lines[979] == "#### **Substitution Systems**"
        and "number of elements can change" in lines[983]
        and "each one of these elements is replaced by a new block" in lines[983]
        and "rightmost element is always dropped" in lines[1021]
        and "no rule is given for how to replace it" in lines[1021]
        and "every single element should be replaced by at least one new element" in lines[1025]
        and "elements can simply disappear" in lines[1027]
        and "pattern will quickly die out" in lines[1027]
        and "creation and destruction of elements is almost perfectly balanced" in lines[1029]
        and "rules allow both creation and destruction of elements" in lines[1031]
        and "total number of elements grows by only a fixed amount" in lines[1031]
        and "only the order of elements is ever significant" in lines[1045]
        and "addition or subtraction of elements to its left" in lines[1045]
        and "elements are created and destroyed" in lines[1051]
        and "operate in parallel on all the elements" in lines[1059]
        and lines[1053] == "#### **Sequential Substitution Systems**"
        and "first such sequence that is found" in lines[1061]
        and "every element is replaced at each step" in lines[2357]
        and "there is no fixed array of elements" in lines[7939]
        and "progressively larger numbers of cellular automaton steps" in lines[7949]
        and "SSEvolveList" in lines[12100]
        and "Flatten[# /. rule]" in lines[12100]
        and "For a neighbor-dependent substitution system" in lines[12108]
        and "Partition[#, 2, 1]" in lines[12112]
        and "any form of growth can in principle" in lines[12135]
        and lines[12135].endswith("in principle")
        and "1L systems correspond to the neighbor-dependent substitution systems" in lines[12250]
        and "\\{1, 0\\} \\rightarrow \\{\\}" in lines[12297]
        and "Length[#] < n, {\\}" in lines[12299]
        and not re.search(r"\b(?:empty|epsilon|erasing|erasure)\b|ε", core_text, re.I)
        and hits["Q02"] == {1028}
        and hits["Q03"] == {1030, 1032, 1046, 1052}
        and hits["Q08"] == set()
        and hits["Q09"] == set()
        and hits["Q10"] == {19751, 19976, 20454, 21148}
        and hits["Q18"] == {12298, 12432, 13953}
        and '"e" \\to \\{\\}' in lines[12431]
        and "sequence of opening and closing brackets" in lines[12427]
        and '"AB" \\to ""' in lines[13952]
        and "MWStep[rule_List" in lines[13945]
        and t14_notes_step([]) == []
        and t14_notes_step([1]) == []
        and t14_notes_step([0, 1]) == [0]
    )
    ok &= source_semantics_ok
    print("source_semantics", "OK" if source_semantics_ok else "MISMATCH")

    structural = (
        MATCHED_RETAINED == matched_retained
        and not GOVERNED_CONTINUATIONS & union
        and pre_index_union == matched_retained | excluded
        and not matched_retained & excluded
        and set(EMPTY_RHS_EXCLUDED_CONTROLS) <= excluded
        and not RETAINED & index
        and len(union | GOVERNED_CONTINUATIONS) == 359
    )
    ok &= structural
    print("structural", "OK" if structural else "MISMATCH")

    split_paths = sorted(
        path
        for path in SOURCE_ROOT.rglob("*.md")
        if path.resolve() not in {DEFAULT_BOOK.resolve(), ATLAS.resolve()}
    )
    relative_paths = [path.relative_to(SOURCE_ROOT).as_posix() for path in split_paths]
    split_manifest = [
        f"{relative}\0{len(path.read_bytes())}\0{sha256(path)}"
        for path, relative in zip(split_paths, relative_paths, strict=True)
    ]
    path_manifest_ok = (
        len(split_paths) == EXPECTED_SPLIT_FILE_COUNT
        and digest_records(relative_paths) == EXPECTED_SPLIT_PATHS_DIGEST
        and digest_records(split_manifest) == EXPECTED_SPLIT_MANIFEST_DIGEST
    )
    ok &= path_manifest_ok
    print(
        "split_manifest",
        "OK" if path_manifest_ok else "MISMATCH",
        len(split_paths),
        digest_records(relative_paths),
        digest_records(split_manifest),
    )

    compiled = {
        name: re.compile(pattern, re.IGNORECASE) for name, pattern in QUERIES.items()
    }
    monolith_query_text = {lines[n - 1] for n in union}
    split_records: set[str] = set()
    split_exact_records: set[str] = set()
    split_nonexact_records: set[str] = set()
    split_texts: set[str] = set()
    split_direct_creation_stream_hits: set[str] = set()
    all_split_records: set[str] = set()
    for path, relative in zip(split_paths, relative_paths, strict=True):
        split_document = path.read_text(encoding="utf-8")
        if DIRECT_CREATION_STREAM_RX.search(split_document):
            split_direct_creation_stream_hits.add(relative)
        for line_no, line in enumerate(split_document.splitlines(), 1):
            record = f"{relative}:{line_no}"
            all_split_records.add(record)
            split_texts.add(line)
            if not any(rx.search(line) for rx in compiled.values()):
                continue
            split_records.add(record)
            if line in monolith_query_text:
                split_exact_records.add(record)
            else:
                split_nonexact_records.add(record)

    split_query_ok = (
        (len(split_records), digest_records(split_records))
        == EXPECTED_SPLIT_QUERY_RECORDS
        and (len(split_exact_records), digest_records(split_exact_records))
        == EXPECTED_SPLIT_EXACT_QUERY_RECORDS
        and split_nonexact_records == set(SPLIT_NONEXACT_QUERY_WITNESSES)
        and digest_records(split_nonexact_records)
        == EXPECTED_SPLIT_NONEXACT_QUERY_RECORDS_DIGEST
        and split_direct_creation_stream_hits
        == EXPECTED_SPLIT_DIRECT_CREATION_PATHS
        and digest_records(split_direct_creation_stream_hits)
        == EXPECTED_SPLIT_DIRECT_CREATION_PATHS_DIGEST
        and all(
            canonical in union
            for targets in SPLIT_NONEXACT_QUERY_WITNESSES.values()
            for canonical in targets
        )
    )
    ok &= split_query_ok
    print(
        "split_query",
        "OK" if split_query_ok else "MISMATCH",
        len(split_records),
        len(split_exact_records),
        len(split_nonexact_records),
        digest_records(split_records),
        digest_records(split_exact_records),
        digest_records(split_nonexact_records),
    )
    if not split_query_ok:
        print("split_nonexact_records", sorted(split_nonexact_records))
        print(
            "split_direct_creation_stream_hits",
            sorted(split_direct_creation_stream_hits),
        )

    exact_retained_mirror = {n for n in RETAINED if lines[n - 1] in split_texts}
    split_nonexact_retained = set(RETAINED) - exact_retained_mirror
    witness_records = set(SPLIT_NONEXACT_RETAINED_WITNESSES.values())
    retained_split_ok = (
        (len(exact_retained_mirror), digest(exact_retained_mirror))
        == EXPECTED_EXACT_RETAINED_MIRRORS
        and split_nonexact_retained == SPLIT_NONEXACT_RETAINED
        and digest(split_nonexact_retained)
        == EXPECTED_SPLIT_NONEXACT_RETAINED_DIGEST
        and set(SPLIT_NONEXACT_RETAINED_WITNESSES) == split_nonexact_retained
        and witness_records <= all_split_records
        and digest_records(witness_records)
        == EXPECTED_SPLIT_RETAINED_WITNESS_DIGEST
    )
    ok &= retained_split_ok
    print(
        "split_retained",
        "OK" if retained_split_ok else "MISMATCH",
        len(exact_retained_mirror),
        len(split_nonexact_retained),
        digest(exact_retained_mirror),
        digest(split_nonexact_retained),
    )

    atlas_lines = ATLAS.read_text(encoding="utf-8").splitlines()
    atlas_hits = {
        n
        for n, line in enumerate(atlas_lines, 1)
        if any(rx.search(line) for rx in compiled.values())
    }
    atlas_text = "\n".join(atlas_lines)
    atlas_ok = (
        len(atlas_lines) == EXPECTED_ATLAS_LINES
        and atlas_hits == EXPECTED_ATLAS_QUERY_LINES
        and digest(atlas_hits) == EXPECTED_ATLAS_QUERY_DIGEST
        and not compiled["Q00"].search(atlas_text)
        and not compiled["Q02"].search(atlas_text)
        and not compiled["Q03"].search(atlas_text)
        and not compiled["Q08"].search(atlas_text)
        and not compiled["Q09"].search(atlas_text)
        and not compiled["Q18"].search(atlas_text)
    )
    ok &= atlas_ok
    print(
        "atlas",
        "OK" if atlas_ok else "MISMATCH",
        len(atlas_lines),
        len(atlas_hits),
        digest(atlas_hits),
        sorted(atlas_hits),
    )

    catalog_lines = CATALOG.read_text(encoding="utf-8").splitlines()
    taxonomy_text = TAXONOMY.read_text(encoding="utf-8")
    catalog_ok = (
        len(catalog_lines) == 46
        and catalog_lines[15] == "Creation-Destruction Substitution Systems,"
        and len(set(catalog_lines[1:])) == 45
        and "## 15. Creation-Destruction Substitution Systems" in taxonomy_text
        and "Replacement blocks may be empty." in taxonomy_text
        and "no separate policy is needed mathematically" in taxonomy_text
        and not compiled["Q00"].search(text)
    )
    ok &= catalog_ok
    print("catalog", "OK" if catalog_ok else "MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
