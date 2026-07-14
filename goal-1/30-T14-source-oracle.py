#!/usr/bin/env python3
"""Frozen source-evidence audit for T14 contextual substitution.

The canonical Chapter 3 construction is called a ``neighbor-dependent
substitution system`` and the Notes implement its displayed one-sided case
with overlapping adjacent-pair reads.  This oracle freezes the complete
line-oriented search union, dispositions, actual-Index routes, split-source
reverse joins, and the extraction limitations used by the T14 source audit.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


if not __debug__:
    raise RuntimeError("T14 source oracle requires assertions; do not use -O")


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


# Q01 deliberately sweeps every occurrence of the broad family name: all 288
# lines were read and dispositioned.  Q02 follows 1L/D1L/Lindenmayer aliases.
# Q03/Q08 freeze the Notes implementation and exact four-row table.  Q04--Q10
# cover defining context, boundary, output, page, scheduling, and growth terms.
# Q11/Q12 freeze useful absences: the source never names this type
# "contextual/context-sensitive substitution" and gives no pad/wrap/sentinel
# boundary alternative coupled to substitution systems.
QUERIES = {
    "Q00": r"\bneighbor(?:[\s-]*)dependent(?:[\s-]+)substitution systems?\b",
    "Q01": r"\bsubstitution systems?\b",
    "Q02": r"\b(?:D?1L|L) systems?\b|\bLindenmayer\b",
    "Q03": r"\bSS2EvolveList\b|Flatten\[Partition\[#,\s*2,\s*1\]",
    "Q04": (
        r"(?:rules?|replacement|color)[^.]{0,180}\bdepend[^.]{0,180}"
        r"(?:\bneighbors?\b|immediately to its right)|"
        r"\bimmediately to its right\b"
    ),
    "Q05": (
        r"\brightmost element is always dropped\b|"
        r"\bno rule is given for how to replace it\b|"
        r"\baway from the right-hand edge\b"
    ),
    "Q06": (
        r"\btotal number of elements never decreases\b|"
        r"\bevery single element should be replaced by at least one new element\b|"
        r"\belements can simply disappear\b|"
        r"\balways yielding just one cell\b"
    ),
    "Q07": r"\bpage 85\b|\bpages? 85[–-]8[578]\b|\b85[–-]87\b",
    "Q08": (
        r"\\\{\\\{1,\s*1\\\}.*\\\{1,\s*0\\\}.*"
        r"\\\{0,\s*1\\\}.*\\\{0,\s*0\\\}"
    ),
    "Q09": (
        r"\b(?:operate|operating|operates) in parallel on all the elements\b|"
        r"\breplacing each element in such a string by a new sequence of elements\b"
    ),
    "Q10": r"\bfor neighbor-dependent rules, any form of growth can in principle\b",
    "Q11": (
        r"\bcontext(?:ual|[- ](?:dependent|sensitive)) substitution systems?\b|"
        r"\bcontext[- ]sensitive L systems?\b"
    ),
    "Q12": (
        r"\b(?:pad(?:ded|ding)? with (?:a )?blank|wrap(?:ped|ping)?|"
        r"special boundary symbol)\b.{0,160}\bsubstitution systems?\b|"
        r"\bsubstitution systems?\b.{0,160}\b(?:pad(?:ded|ding)? with "
        r"(?:a )?blank|wrap(?:ped|ping)?|special boundary symbol)\b"
    ),
}

DIRECT_NAME_STREAM_RX = re.compile(
    r"\bneighbor(?:[\s-]*)dependent(?:[\s-]+)substitution systems?\b",
    re.IGNORECASE,
)


# Expected tuple: total, pre-Index, actual-Index, digest of ascending line set.
EXPECTED_QUERY = {
    "Q00": (7, 6, 1, "f37901fb3b77c8a4c4f80bf0456322ee203ce5dc42ca86523323a23d0bc13f8b"),
    "Q01": (288, 213, 75, "3f49076beb5b70231b930b882a16d2ed56dee504de8dcccb40e13d8f9a782c3a"),
    "Q02": (9, 4, 5, "b4b84b2c1ba9fff3da3ecfb0bcdf3f15212b09ff151d6bd3061e734928d576f0"),
    "Q03": (1, 1, 0, "e4819c5162b90e09b16feb72c7fc33e3361360ae8866a49b704dabc3e7aa0c86"),
    "Q04": (12, 12, 0, "71a8d3864743a7a7ec8967a8a550c098dfbd95b6285b5f141b7aa194c2cd333a"),
    "Q05": (2, 2, 0, "999f14eeb9aa68925d54a327ab0defaf28bd9fd884589ab566d3c19dca9e763b"),
    "Q06": (3, 3, 0, "a383c3152b1d59fc16d66f9e99650db5d252e2303a7af7989d4d1fe23fdab6ce"),
    "Q07": (8, 5, 3, "03b1966bccb7fd3ee3381dd86ea5348c5804229f2c029efef05de8f48134cf60"),
    "Q08": (2, 2, 0, "2c21fd729936b5372f164a5f484a1e61883ae72e57e978973658a2b3be5a7c40"),
    "Q09": (1, 1, 0, "8dfd13f4376053626e97eb7221d469013cae9bc031027e64f0db2ec114f8ffd9"),
    "Q10": (1, 1, 0, "efd36eeefc0e70b5a6a8b2b1e40373760c25bbdf13ea0281c13e1bade536f33a"),
    "Q11": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q12": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
}


# Search-hit lines retained after every pre-Index query hit was inspected.
# Cross-family lines are retained only when they establish a boundary or a
# followed relation: T15 deletion, T28 two-dimensional context, generalized
# left-to-right non-overlap, CA emulation, and encoding use are not silently
# promoted into native T14 semantics.
MATCHED_RETAINED = frozenset(
    {
        984,
        1018,
        1022,
        1026,
        1028,
        1046,
        1050,
        1052,
        1058,
        1060,
        1062,
        2350,
        2356,
        5928,
        5952,
        8022,
        8024,
        8028,
        12109,
        12111,
        12113,
        12115,
        12136,
        12251,
        13806,
        16404,
        18788,
    }
)

# Non-query lines required to preserve defining context, figures, source
# extraction defects, and the exact distinction from generalized block-match
# rewriting and the two-dimensional sibling.
GOVERNED_CONTINUATIONS = frozenset(
    {
        982,
        986,
        1020,
        1024,
        1030,
        2352,
        5944,
        5948,
        5954,
        8026,
        12117,
        13808,
        13810,
    }
)
RETAINED = MATCHED_RETAINED | GOVERNED_CONTINUATIONS


EXPECTED_SET = {
    "union": (308, "17902ddb945809f7b2c66adbb5372a20a4fedb723093891db54dc6f28a6ef484"),
    "pre_index_union": (231, "a5b2d7348d117d40130205dc7d708a4857bcb170ec85cb59eb6a5af0f45a4fb7"),
    "index": (77, "3ad1376a743e1cc0193b21c27c06b51410da403e3ec5fbcee9f6e05f49c75462"),
    "matched_retained": (27, "0d2ff2bd13cb2a79f4145f31bfe7682f5d96a8285530bced52fed8113ae6368c"),
    "governed_continuations": (13, "b153a078ad3d00b7f41ea3e9177ebfa4a9076e0539f778e50c56632aee25eab4"),
    "retained": (40, "24213ee950c26341f210496994a3b91202ccb5c560c1b078192ee85a8b33410a"),
    "excluded": (204, "0721f005cf8d1ec233b98b04bd89222b87f18bb1f5533ac6615fb19f6902b2ef"),
}

INDEX_RELEVANT = frozenset({20828, 21068, 21422, 21461, 21652, 22114, 22144})
EXPECTED_INDEX_RELEVANT_DIGEST = (
    "2d1105dc73aa25ed6b2855cc7aa996f2dc7a72b7f1dd3fcb2cdf0fc4cf366e54"
)
EXPECTED_INDEX_EXCLUDED = (
    70,
    "215ec5e6dfc3d3d4a7f485bf534b12573fcfcec666545094b19d75d80c712424",
)


EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = (
    "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
)
EXPECTED_SPLIT_MANIFEST_DIGEST = (
    "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"
)
EXPECTED_SPLIT_QUERY_RECORDS = (
    306,
    "4a6e598c161353f5d742e9cc2d71a2d371477d9364b7c355a6df17922b3383a2",
)
EXPECTED_SPLIT_EXACT_QUERY_RECORDS = (
    276,
    "c906397eff9ddbb38672f996844f6d0802bc69d193f179f58d51d846ec602c5e",
)

# Every non-exact split query hit was manually joined to its canonical
# monolith line.  Differences are punctuation, OCR repair, heading emphasis,
# merged/split prose, or image-path conventions; none adds source semantics.
SPLIT_NONEXACT_QUERY_WITNESSES = {
    "BACK-MATTER/Colophon/Colophon.md:4909": (22352,),
    "BACK-MATTER/Colophon/Colophon.md:90": (17533,),
    "BACK-MATTER/Index/Index.md:11": (12099,),
    "BACK-MATTER/Index/Index.md:1171": (13268,),
    "BACK-MATTER/Index/Index.md:154": (12249,),
    "BACK-MATTER/Index/Index.md:1584": (13683,),
    "BACK-MATTER/Index/Index.md:166": (12261,),
    "BACK-MATTER/Index/Index.md:23": (12111,),
    "BACK-MATTER/Index/Index.md:259": (12356,),
    "BACK-MATTER/Index/Index.md:48": (12136,),
    "BACK-MATTER/Index/Index.md:887": (12984,),
    "CHAPTERS/10-Processes-of-Perception-and-Analysis/Processes-of-Perception-and-Analysis.md:689": (7278,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:249": (7950,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:251": (7952,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:321": (8022,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:327": (8028,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:329": (8030,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:601": (8318,),
    "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:375": (1058,),
    "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:309": (1850,),
    "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:315": (1856,),
    "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:317": (1858,),
    "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:165": (2308,),
    "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:177": (2320,),
    "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:203": (2350,),
    "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:209": (2356,),
    "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:217": (2366,),
    "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:339": (2508,),
    "CHAPTERS/9-Fundamental-Physics/Fundamental-Physics.md:825": (5990,),
    "FRONT-MATTER/Preface/Preface.md:58": (144,),
}
EXPECTED_SPLIT_NONEXACT_QUERY_RECORDS_DIGEST = (
    "886db49ee3a72ac0e12ef2a222a53f277b10b747da6ca74a204c64588adba9ce"
)
EXPECTED_SPLIT_DIRECT_NAME_PATHS = frozenset(
    {
        "BACK-MATTER/Colophon/Colophon.md",
        "BACK-MATTER/Index/Index.md",
        "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md",
    }
)
EXPECTED_SPLIT_DIRECT_NAME_PATHS_DIGEST = (
    "a52d54720ea6515c196c9bdb6f6a24f2bb346042d39c8b0634c3940c9d36d6ff"
)

EXPECTED_EXACT_RETAINED_MIRRORS = (
    29,
    "705ae0ef1e634f911a94718c973f5411b5b9d4937c576367e2859f338d55eb85",
)
SPLIT_NONEXACT_RETAINED = frozenset(
    {1020, 1058, 2350, 2352, 2356, 8022, 8026, 8028, 12111, 12115, 12136}
)
EXPECTED_SPLIT_NONEXACT_RETAINED_DIGEST = (
    "cec3bb703fa4d262d2711907d20cf3fcdb78ed8f1ef7462149d9f9a6f59f4da6"
)
SPLIT_NONEXACT_RETAINED_WITNESSES = {
    1020: "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:337",
    1058: "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:375",
    2350: "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:203",
    2352: "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:205",
    2356: "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:209",
    8022: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:321",
    8026: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:325",
    8028: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:327",
    12111: "BACK-MATTER/Index/Index.md:23",
    12136: "BACK-MATTER/Index/Index.md:48",
}
SPLIT_OMITTED_RETAINED = frozenset({12115})
EXPECTED_SPLIT_RETAINED_WITNESS_DIGEST = (
    "eba3ae442b05ead2cc079df345432ee43912eec8b70822da3914583b9cc081e7"
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


def notes_step(word: list[int]) -> list[int]:
    """Exact list semantics of BOOK:12111-12113 for its complete binary table."""

    table = {
        (1, 1): (0, 1),
        (1, 0): (1, 0),
        (0, 1): (0,),
        (0, 0): (0, 1),
    }
    result: list[int] = []
    for index in range(max(0, len(word) - 1)):
        result.extend(table[(word[index], word[index + 1])])
    return result


def main() -> int:
    if len(sys.argv) > 2:
        raise SystemExit("usage: 30-T14-source-oracle.py [BOOK]")
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
        and len(DIRECT_NAME_STREAM_RX.findall(text)) == 8
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
        and "Neighbor-dependent substitution systems, 85–87" in lines[21651]
        and "neighbor-dependent, 85-87" in lines[22143]
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

    # Freeze the source's exact executable content and its limitations.  The
    # Notes table is total over Bit^2 and has no empty row.  Nevertheless, the
    # right-endpoint eligibility rule makes [0,1] shrink from two elements to
    # one, so BOOK:1026 can only describe the two displayed trajectories, not
    # a theorem for every seed.  Zero eligible pairs for n < 2 is distinct
    # from a table row whose replacement word is empty (the T15 boundary).
    notes_ok = (
        "rules depend not only on the color of a single element" in lines[1017]
        and "element immediately to its right" in lines[1017]
        and "rightmost element is always dropped" in lines[1021]
        and "no rule is given for how to replace it" in lines[1021]
        and "total number of elements never decreases" in lines[1025]
        and "elements can simply disappear" in lines[1027]
        and "For a neighbor-dependent substitution system" in lines[12108]
        and "\\{\\{1, 1\\} \\rightarrow \\{0, 1\\}" in lines[12110]
        and "\\{0, 1\\} \\rightarrow \\{0\\}" in lines[12110]
        and "Partition[#, 2, 1]" in lines[12112]
        and lines[12114] == "where the initial condition for the first example on page 85 is"
        and lines[12115] == ""
        and lines[12116].startswith("- Page 83 · Properties.")
        and notes_step([0, 1]) == [0]
        and len(notes_step([0, 1])) < 2
        and notes_step([]) == []
        and notes_step([1]) == []
        and notes_step([0, 1, 1, 0]) == [0, 0, 1, 1, 0]
    )
    ok &= notes_ok
    print("notes_semantics", "OK" if notes_ok else "MISMATCH")

    structural = (
        MATCHED_RETAINED == matched_retained
        and not GOVERNED_CONTINUATIONS & union
        and pre_index_union == matched_retained | excluded
        and not matched_retained & excluded
        and not RETAINED & index
        and len(union | GOVERNED_CONTINUATIONS) == 321
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
    split_direct_name_stream_hits: set[str] = set()
    all_split_records: set[str] = set()
    for path, relative in zip(split_paths, relative_paths, strict=True):
        split_document = path.read_text(encoding="utf-8")
        if DIRECT_NAME_STREAM_RX.search(split_document):
            split_direct_name_stream_hits.add(relative)
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
        and split_direct_name_stream_hits == EXPECTED_SPLIT_DIRECT_NAME_PATHS
        and digest_records(split_direct_name_stream_hits)
        == EXPECTED_SPLIT_DIRECT_NAME_PATHS_DIGEST
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
        print("split_direct_name_stream_hits", sorted(split_direct_name_stream_hits))

    exact_retained_mirror = {n for n in RETAINED if lines[n - 1] in split_texts}
    split_nonexact_retained = set(RETAINED) - exact_retained_mirror
    witness_records = set(SPLIT_NONEXACT_RETAINED_WITNESSES.values())
    retained_split_ok = (
        (len(exact_retained_mirror), digest(exact_retained_mirror))
        == EXPECTED_EXACT_RETAINED_MIRRORS
        and split_nonexact_retained == SPLIT_NONEXACT_RETAINED
        and digest(split_nonexact_retained)
        == EXPECTED_SPLIT_NONEXACT_RETAINED_DIGEST
        and set(SPLIT_NONEXACT_RETAINED_WITNESSES) | set(SPLIT_OMITTED_RETAINED)
        == split_nonexact_retained
        and witness_records <= all_split_records
        and digest_records(witness_records)
        == EXPECTED_SPLIT_RETAINED_WITNESS_DIGEST
        and all(lines[n - 1] not in split_texts for n in SPLIT_OMITTED_RETAINED)
    )
    ok &= retained_split_ok
    print(
        "split_retained",
        "OK" if retained_split_ok else "MISMATCH",
        len(exact_retained_mirror),
        len(split_nonexact_retained),
        digest(exact_retained_mirror),
        digest(split_nonexact_retained),
        sorted(SPLIT_OMITTED_RETAINED),
    )

    atlas_lines = ATLAS.read_text(encoding="utf-8").splitlines()
    atlas_hits = {
        n
        for n, line in enumerate(atlas_lines, 1)
        if any(rx.search(line) for rx in compiled.values())
    }
    atlas_ok = (
        len(atlas_lines) == EXPECTED_ATLAS_LINES
        and atlas_hits == EXPECTED_ATLAS_QUERY_LINES
        and digest(atlas_hits) == EXPECTED_ATLAS_QUERY_DIGEST
        and not compiled["Q00"].search("\n".join(atlas_lines))
        and not compiled["Q03"].search("\n".join(atlas_lines))
        and not compiled["Q11"].search("\n".join(atlas_lines))
        and not compiled["Q12"].search("\n".join(atlas_lines))
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
        and catalog_lines[14] == "Neighbor-Dependent Substitution Systems,"
        and len(set(catalog_lines[1:])) == 45
        and "## 14. Neighbor-Dependent Substitution Systems" in taxonomy_text
    )
    ok &= catalog_ok
    print("catalog", "OK" if catalog_ok else "MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
