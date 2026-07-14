#!/usr/bin/env python3
"""Frozen source-evidence audit for T10 Extended Mobile Automata.

The book does not use the catalog phrase ``Extended Mobile Automata``.  The
audited construction is the unnamed extension introduced in Chapter 3 and
made executable in the Notes for page 73.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


if not __debug__:
    raise RuntimeError("T10 source oracle requires assertions; do not use -O")


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


# Q00 and Q08 deliberately freeze important absences.  Q15 is a hostile
# multiple-cell/block-wording control; its three hits are other constructions.
QUERIES = {
    "Q00": r"\bextended[- ]mobile[- ]automat(?:on|a)s?\b|\bmobile[- ]automat(?:on|a)s?[- ]extensions?\b",
    "Q01": r"\bmobile automat(?:on|a)s?\b",
    "Q02": r"\bactive cells?\b",
    "Q03": r"\bimmediate neighbors?\b",
    "Q04": r"\b(?:4,294,967,296|4294967296)\b",
    "Q05": r"\b(?:MAStep|MAEvolveList|GMAStep)\b",
    "Q06": r"\bpage 73\b",
    "Q07": (
        r"(?:\b(?:extend|extends|extended|extending|extension|widen|widens|"
        r"widened|widening|wider|multiple-cell|multi-cell)\b.{0,120}\b"
        r"(?:mobile automat(?:on|a)s?|active cells?|immediate neighbors?)\b|"
        r"\b(?:mobile automat(?:on|a)s?|active cells?|immediate neighbors?)\b"
        r".{0,120}\b(?:extend|extends|extended|extending|extension|widen|"
        r"widens|widened|widening|wider|multiple-cell|multi-cell)\b)"
    ),
    "Q08": r"\b(?:replacement blocks?|block replacements?|replacement windows?|write windows?|write scopes?|multiple-cell updates?|multi-cell updates?|three-cell replacements?)\b",
    "Q09": r"\b(?:one cell at a time|single cell gets updated|active cell is the only one that ever gets updated|only the single active cell[^.]{0,48}updated)\b",
    "Q10": (
        r"(?:\b(?:move|moves|moved|moving|displacement|position)\b.{0,48}\b"
        r"(?:active cell|left or right)\b|\bactive cell\b.{0,48}\b"
        r"(?:move|moves|moved|moving|displacement|position|left or right)\b)"
    ),
    "Q11": r"\b(?:generalized|reversible|network|2D|two-dimensional|universal) mobile automat(?:on|a)s?\b",
    "Q12": r"\b(?:sequential automata|mobile cellular automata?|moving automata?|moving automaton|moving head|mobile machines?)\b",
    "Q13": r"\b(?:compressed (?:evolution|form|version)|active cell motion|position of the active cell)\b",
    "Q14": r"(?:\bJoin\[Take\[list\b|\bReplace\[Take\[list\b|\bReplacePart\[list\b)",
    "Q15": (
        r"(?:\b(?:update|updates|updated|updating)\b.{0,80}\b"
        r"(?:three|multiple|several) cells?\b|\b(?:three|multiple|several)"
        r" cells?\b.{0,80}\b(?:update|updates|updated|updating)\b|"
        r"\b(?:update|updates|updated|updating)\b.{0,80}\btriples? of cells?\b|"
        r"\bblocks? of cells?\b.{0,80}\b(?:updated|replaced)\b)"
    ),
    "Q16": r"\b(?:65,536|65536)\b",
    "Q17": r"\bnew_(?:left|self|right)\b|\bnew (?:left|self|center|right) (?:cell )?(?:color|value)\b",
}

DIRECT_NAME_STREAM_RX = re.compile(
    r"\bextended(?:[\s-]+)mobile(?:[\s-]+)automat(?:on|a)s?\b",
    re.IGNORECASE,
)


# Expected tuple: total, pre-Index, actual-Index, digest of ascending line set.
EXPECTED_QUERY = {
    "Q00": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q01": (119, 98, 21, "23c6b5e4bad9762c9a62feeeb99eb23893381f2ad117e73be41fe66083e6ff7a"),
    "Q02": (47, 44, 3, "df89c0dd0715aaf9b0ad33a5f43f460d92472c9ce31a23ce8b28f57b4ee903f5"),
    "Q03": (18, 18, 0, "37176e796904fc27891633c3b6667cc0093dd2dcb0042ec436e008ef8f3f9109"),
    "Q04": (8, 8, 0, "1b54bce141e4e20a64650fec97a2014e7f8c9e42254afae7bf4784fb87bb7f04"),
    "Q05": (7, 7, 0, "a408c1ff93a37f286e946221b04fd47cdae18492796aeb2c892654f5ac24d1cb"),
    "Q06": (2, 2, 0, "da1a603a58559561656a88655fb1e01b2be44f8e5e6f9f09f224bd6825e4f7a6"),
    "Q07": (1, 1, 0, "1de4842b42fa3db35fc4cf058a02acb057a8df02d0d3cdc96e686551aee25a39"),
    "Q08": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q09": (4, 4, 0, "85c7f6bafb584bf5f7e719edbe4f7199ba0f114a1b0457852d24e7aa154f203c"),
    "Q10": (17, 17, 0, "ce98f33534a6badea99110ea4861785b43bedd5edda86b806cd621c4249f7dd1"),
    "Q11": (13, 11, 2, "f437f66f9daf922e6fbb73c98a6dbd8bb173ccfab8a832b20ad6d01e21068b69"),
    "Q12": (1, 0, 1, "2754f6e1f004d4298d7ed6444c52385d98a70aee827877053ef7d43e519ac10f"),
    "Q13": (19, 18, 1, "5222865723cd25be46c00c3ac2a3619322e3998f63bb24803097d81271312a00"),
    "Q14": (5, 5, 0, "5aa9e15666ee4fb901bb43455af19fd54c9744f0e162e821d0a37e182cdadbbc"),
    "Q15": (3, 3, 0, "d745b5e74f70430fbe65b9b62902191a212b11d6e98c5205844f4aba8d09c823"),
    "Q16": (7, 7, 0, "f74b1d053b7e0bee072fbb9a0a043f8c59d273b75ae57f2fcc4d1c3f6fd85b6b"),
    "Q17": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
}


# Search-matched lines retained after reading every hit in context.  This set
# includes explicit negative-boundary evidence (ordinary mobile shorthand and
# emulation-only relations) so later design prose cannot silently generalize it.
MATCHED_RETAINED = frozenset(map(int, """
852 854 856 862 864 874 878 880 882 890 898 904 912 914 916 918 924 934
940 948 982 5818 5820 5836 5874 5926 5928 5930 5938 7924 7926 7930 7936
8004 8008 8010 8012 8014 11957 11965 11968 11969 11970 11976 11977 11982
11991 11993 11995 12002 12008 12010 13679 14275 16066 16388 16398 16400
16442 16648 16652 16654 18352 18361 18457 18463
""".split()))

# Adjacent lines needed to keep rule tables, executable bodies, and contrasts
# complete.  None is a search hit; each is governed by a retained lead line.
GOVERNED_CONTINUATIONS = frozenset(map(int, """
850 884 942 11960 11961 11962 11973 11985 11986 11987 11988 16068 16391
16392 16393 16396 16444 18355 18356 18357 18358 18460
""".split()))

RETAINED = MATCHED_RETAINED | GOVERNED_CONTINUATIONS


EXPECTED_SET = {
    "union": (183, "e9d4066e4446c0ea8481ef9ba215f9fce60400019b3484064887cead0f7af421"),
    "pre_index_union": (161, "2db28b904b6ca916e65380fb9260a6f3373e826b842df8e31b1a1046784504f4"),
    "index": (22, "7e730c202bc5917d39e6577bcac44d8adfd6e6157446e801aa61312ea2da84e4"),
    "matched_retained": (66, "d37c71575e055766bc0bf9da5cb849eb17095343afff4d2d1fff7ae00f838ffa"),
    "governed_continuations": (22, "c06c01bb611b445f49a2248414ee1ef69fc681d38215cead30851d4a0d60495e"),
    "retained": (88, "b840e59085605f26a24f07a1100fa4ccc4390be1eb37a274a8e6e68588681f1c"),
    "excluded": (95, "f29475a403fc0f7f0cebc41ebab511d2c76904a14e7a815205a16ce43c642b10"),
}


EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = (
    "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
)
EXPECTED_SPLIT_MANIFEST_DIGEST = (
    "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"
)
EXPECTED_SPLIT_QUERY_RECORDS = (
    183,
    "edf3bea6dd86a63a33df9d3cea120981a9d3e508463bef8db37bd8c3487fd7c0",
)
EXPECTED_SPLIT_EXACT_QUERY_RECORDS = (
    171,
    "212b49b594d33a0e6bd8ed80234d6b961fe1f21203e92f151d535a010480e272",
)

# These are the only split query records whose complete physical line is not
# byte-identical to a monolith query-hit line.  Values name the canonical line
# or the two canonical fragments that the split extraction joined.
SPLIT_NONEXACT_QUERY_WITNESSES = {
    "BACK-MATTER/Colophon/Colophon.md:4909": (22352,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:225": (7926, 7936),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:229": (7930,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:235": (7936,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:271": (7972,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:371": (8076,),
    "CHAPTERS/2-The-Crucial-Experiment/The-Crucial-Experiment.md:27": (428, 430),
    "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:171": (854,),
    "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:179": (862,),
    "CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Mechanisms-in-Programs-and-Nature.md:421": (3844,),
    "CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Mechanisms-in-Programs-and-Nature.md:707": (4136,),
    "CHAPTERS/9-Fundamental-Physics/Fundamental-Physics.md:301": (5466,),
}
EXPECTED_SPLIT_NONEXACT_QUERY_RECORDS_DIGEST = (
    "7eb7db7815805d305ccc2e0c0245787792fefa540764622ee87067227c231b1d"
)

EXPECTED_EXACT_RETAINED_MIRRORS = (
    83,
    "a071716f2e43b59170c708be0374e7e2c00a658f7ca15d9186286a8fa28593b0",
)
SPLIT_NONEXACT_RETAINED = frozenset({854, 862, 7926, 7930, 7936})
EXPECTED_SPLIT_NONEXACT_RETAINED_DIGEST = (
    "1e40484140ac51a673b2c76ae2eef4c207a4b2a4a0c67705b3dbc9c710c9f870"
)

EXPECTED_ATLAS_LINES = 542
EXPECTED_ATLAS_QUERY_LINES = frozenset({7, 81, 83})
EXPECTED_ATLAS_QUERY_DIGEST = (
    "926e91fc268887f329d5dc56aa7d9863a70bb011f2d57d2863fafffe822a83ad"
)


def digest(lines: set[int] | frozenset[int]) -> str:
    payload = ",".join(map(str, sorted(lines))).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_records(records: set[str] | list[str]) -> str:
    payload = "\n".join(sorted(records)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    if len(sys.argv) > 2:
        raise SystemExit("usage: 28-T10-source-oracle.py [BOOK]")
    book = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else DEFAULT_BOOK
    raw = book.read_bytes()
    lines = raw.decode("utf-8").splitlines()
    source_ok = (
        len(lines) == EXPECTED_BOOK_LINES
        and hashlib.sha256(raw).hexdigest() == EXPECTED_BOOK_SHA256
        and sha256(ATLAS) == EXPECTED_ATLAS_SHA256
        and sha256(CATALOG) == EXPECTED_CATALOG_SHA256
        and sha256(TAXONOMY) == EXPECTED_TAXONOMY_SHA256
        and DIRECT_NAME_STREAM_RX.search(raw.decode("utf-8")) is None
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
        print(name, "OK" if good else "MISMATCH", *actual[:3], actual[3])

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
        good = len(values) == expected_count and (
            expected_digest is None or actual_digest == expected_digest
        )
        ok &= good
        print(name, "OK" if good else "MISMATCH", len(values), actual_digest)

    structural = (
        MATCHED_RETAINED == matched_retained
        and not GOVERNED_CONTINUATIONS & union
        and pre_index_union == matched_retained | excluded
        and not matched_retained & excluded
        and not RETAINED & index
        and len(union | GOVERNED_CONTINUATIONS) == 205
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

    compiled = {name: re.compile(pattern, re.IGNORECASE) for name, pattern in QUERIES.items()}
    monolith_query_text = {lines[n - 1] for n in union}
    split_records: set[str] = set()
    split_exact_records: set[str] = set()
    split_nonexact_records: set[str] = set()
    split_texts: set[str] = set()
    split_q00: set[str] = set()
    split_direct_name_stream_hits: set[str] = set()
    for path, relative in zip(split_paths, relative_paths, strict=True):
        split_document = path.read_text(encoding="utf-8")
        if DIRECT_NAME_STREAM_RX.search(split_document):
            split_direct_name_stream_hits.add(relative)
        for line_no, line in enumerate(split_document.splitlines(), 1):
            split_texts.add(line)
            matching = {name for name, rx in compiled.items() if rx.search(line)}
            if not matching:
                continue
            record = f"{relative}:{line_no}"
            split_records.add(record)
            if "Q00" in matching:
                split_q00.add(record)
            if line in monolith_query_text:
                split_exact_records.add(record)
            else:
                split_nonexact_records.add(record)

    split_query_ok = (
        (len(split_records), digest_records(split_records)) == EXPECTED_SPLIT_QUERY_RECORDS
        and (len(split_exact_records), digest_records(split_exact_records))
        == EXPECTED_SPLIT_EXACT_QUERY_RECORDS
        and split_nonexact_records == set(SPLIT_NONEXACT_QUERY_WITNESSES)
        and digest_records(split_nonexact_records)
        == EXPECTED_SPLIT_NONEXACT_QUERY_RECORDS_DIGEST
        and not split_q00
        and not split_direct_name_stream_hits
        and all(
            1 <= canonical <= EXPECTED_BOOK_LINES
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
    )

    exact_retained_mirror = {n for n in RETAINED if lines[n - 1] in split_texts}
    split_nonexact_retained = set(RETAINED) - exact_retained_mirror
    retained_split_ok = (
        (len(exact_retained_mirror), digest(exact_retained_mirror))
        == EXPECTED_EXACT_RETAINED_MIRRORS
        and split_nonexact_retained == SPLIT_NONEXACT_RETAINED
        and digest(split_nonexact_retained)
        == EXPECTED_SPLIT_NONEXACT_RETAINED_DIGEST
        and all(
            any(canonical in targets for targets in SPLIT_NONEXACT_QUERY_WITNESSES.values())
            for canonical in split_nonexact_retained
        )
    )
    ok &= retained_split_ok
    print(
        "split_retained",
        "OK" if retained_split_ok else "MISMATCH",
        len(exact_retained_mirror),
        len(split_nonexact_retained),
        digest(exact_retained_mirror),
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
        and not compiled["Q04"].search("\n".join(atlas_lines))
        and DIRECT_NAME_STREAM_RX.search("\n".join(atlas_lines)) is None
    )
    ok &= atlas_ok
    print(
        "atlas",
        "OK" if atlas_ok else "MISMATCH",
        len(atlas_lines),
        len(atlas_hits),
        digest(atlas_hits),
    )

    catalog_lines = CATALOG.read_text(encoding="utf-8").splitlines()
    taxonomy_text = TAXONOMY.read_text(encoding="utf-8")
    catalog_ok = (
        len(catalog_lines) == 46
        and catalog_lines[10] == "Extended Mobile Automata,"
        and len(set(catalog_lines[1:])) == 45
        and "## 10. Extended Mobile Automata" in taxonomy_text
    )
    ok &= catalog_ok
    print("catalog", "OK" if catalog_ok else "MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
