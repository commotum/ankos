#!/usr/bin/env python3
"""Frozen source-evidence audit for T11 Generalized Mobile Automata.

The canonical monolith calls this construction ``generalized mobile
automata``.  This oracle freezes the complete line-oriented query union,
the read-and-disposition partition, governed context, split-source reverse
joins, and Atlas/catalog controls used by the T11 source audit.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


if not __debug__:
    raise RuntimeError("T11 source oracle requires assertions; do not use -O")


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


# Q01/Q02 deliberately sweep the broad family/control vocabulary, so every
# ordinary-mobile, Turing, emulation, causal-observer, variant, and Index false
# positive receives an explicit disposition.  Q09--Q11 freeze useful absences:
# the monolith has no literal "page 76" route, no multiple-active alias, and no
# collision/activity-layer API jargon.  Q10 does find only the Index alias
# "Sequential automata", which redirects to ordinary Mobile automata.
QUERIES = {
    "Q00": r"\bgeneralized[- ]mobile[- ]automat(?:on|a)s?\b",
    "Q01": r"\bmobile automat(?:on|a)s?\b",
    "Q02": r"\bactive cells?\b",
    "Q03": r"\b(?:GMAStep|nlist)\b",
    "Q04": (
        r"\b(?:more than one|any number of|limited number of|large numbers of|"
        r"almost all) cells? (?:can be|is|are|to be|ever become) active\b"
    ),
    "Q05": (
        r"\b(?:split in two|disappear entirely|active cells? proliferate "
        r"forever|creating an additional active cell|new active cells? end up "
        r"being created)\b"
    ),
    "Q06": (
        r"\b(?:new )?relative positions? of active cells?\b|"
        r"\bpositions? of active cells?\b"
    ),
    "Q07": (
        r"\brule[^.]{0,120}\bapplied to every cell that is active\b|"
        r"\bapplied to every cell that is active[^.]{0,120}\brule\b"
    ),
    "Q08": (
        r"\binterpolate between ordinary mobile automata and cellular "
        r"automata\b"
    ),
    "Q09": r"\bpage 76\b",
    "Q10": (
        r"\b(?:sequential automata|mobile cellular automata?|moving "
        r"automata?|moving automaton|moving heads?|multi-active|"
        r"multiple-active)\b|\b(?:multiple|many|several) active cells?\b"
    ),
    "Q11": (
        r"\b(?:write conflict policy|conflict policy|collision policy|"
        r"overlapping active neighborhoods?|simultaneous write conflicts?|"
        r"activity rule|active set|active layer)\b"
    ),
    "Q12": (
        r"\b(?:essentially like a cellular automaton|ordinary mobile automata "
        r"and cellular automata|all cells are active)\b"
    ),
    "Q13": (
        r"(?:Union\[Flatten\[nlist \+ na\]\]|"
        r"Transpose\[Map\[Replace\[Take\[list)"
    ),
    "Q14": r"\b(?:one|single|only one|just a single) active cells?\b",
    "Q15": (
        r"\b(?:split|splits|splitting|disappear|disappears|disappearing|"
        r"proliferate|proliferates|proliferating)\b.{0,100}\bactive cells?\b|"
        r"\bactive cells?\b.{0,100}\b(?:split|splits|splitting|disappear|"
        r"disappears|disappearing|proliferate|proliferates|proliferating)\b"
    ),
}

DIRECT_NAME_STREAM_RX = re.compile(
    r"\bgeneralized(?:[\s-]+)mobile(?:[\s-]+)automat(?:on|a)s?\b",
    re.IGNORECASE,
)


# Expected tuple: total, pre-Index, actual-Index, digest of ascending line set.
EXPECTED_QUERY = {
    "Q00": (6, 5, 1, "e67e6edf5d988ec1502fa47ef874f84f932ce615c78ef1976c586f367ba7262f"),
    "Q01": (119, 98, 21, "23c6b5e4bad9762c9a62feeeb99eb23893381f2ad117e73be41fe66083e6ff7a"),
    "Q02": (47, 44, 3, "df89c0dd0715aaf9b0ad33a5f43f460d92472c9ce31a23ce8b28f57b4ee903f5"),
    "Q03": (1, 1, 0, "c02425d39be49b9d068767d26991fd767ed37860b4f005f21da0f224a8419c9d"),
    "Q04": (4, 4, 0, "d3a0214d1ce0311a8d69092c7b98688b5957fc58ae1a991d2798bcb505ad08f8"),
    "Q05": (4, 4, 0, "203d26bfe587c52d131eaf3b2adf2a1f2b90f3c860437c17e9b0137c5e73437f"),
    "Q06": (1, 1, 0, "b0c87d71de0c2b5bfcd88fbde3e7ce8add9cb74a225d38dedcfd467de913dd67"),
    "Q07": (1, 1, 0, "1a5659493256d9eb296edea686b14dfd94116d21c8ab25ec0ca46a46f617067e"),
    "Q08": (1, 1, 0, "953815689985e39a762284426cd5884050ea56b7001aa332b18d44d8df0ba478"),
    "Q09": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q10": (1, 0, 1, "2754f6e1f004d4298d7ed6444c52385d98a70aee827877053ef7d43e519ac10f"),
    "Q11": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q12": (2, 2, 0, "e51546c23a3c6e819f5a8e9a706c6409f88c7905b1fb6d4175be1c4ea0eac0fd"),
    "Q13": (1, 1, 0, "c02425d39be49b9d068767d26991fd767ed37860b4f005f21da0f224a8419c9d"),
    "Q14": (8, 7, 1, "122115159f2e6402272cf87327f4c5fea532f1de1010bf9fdec840c4b345a3b9"),
    "Q15": (3, 3, 0, "7e8832ae46277834b744449b8df5df72fd1ca25fc2a5cf4dc86edadeef670dfb"),
}


# Search-hit lines retained after every pre-Index hit was read in context.
# Ordinary-mobile lines are included only where the generalized construction
# explicitly inherits or contrasts their fixed binary line, unique activity,
# local read, and source-cell result.  All other broad hits are dispositioned
# false positives (observers, emulations, sibling variants, or other systems).
MATCHED_RETAINED = frozenset(
    {
        848,
        852,
        854,
        856,
        862,
        864,
        914,
        916,
        918,
        920,
        924,
        928,
        930,
        934,
        982,
        11955,
        11957,
        11965,
        12008,
        12010,
    }
)

# Non-query lines needed for the section contrast and the three direct GMA
# plates.  Image-path lines are source continuations; visual semantics remain
# governed separately by the asset audit.
GOVERNED_CONTINUATIONS = frozenset({850, 858, 860, 922, 926, 932})
RETAINED = MATCHED_RETAINED | GOVERNED_CONTINUATIONS


# Filled from the first diagnostic run, then frozen below.
EXPECTED_SET = {
    "union": (130, "796e7dc0f8d55ee6ef7627939c87ee942d147ac44538d91afd9f8c1ab7aae514"),
    "pre_index_union": (108, "e420645cbf4c0ddaa39511d780394208dcf213b9a6cce30c17cac8ef1182ed4c"),
    "index": (22, "7e730c202bc5917d39e6577bcac44d8adfd6e6157446e801aa61312ea2da84e4"),
    "matched_retained": (20, "04d299273ce081cadd3b14cc9e070a09aaf5cfc50a5e93ee66dd2b2fb62d0ec7"),
    "governed_continuations": (6, "41b13ca4642acda5d31eccf21489d3aa1545806d8ea180e7cee33a5c8ede8f99"),
    "retained": (26, "15ec07596824fc5034feaba4735d329e74826b2849fa260b7053bbf07fe1ce8c"),
    "excluded": (88, "cf7b3013909633e3d4a5be2f61e816bed83b65089e42d72eb0e83240ebae7905"),
}


EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = (
    "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
)
EXPECTED_SPLIT_MANIFEST_DIGEST = (
    "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"
)

EXPECTED_SPLIT_QUERY_RECORDS = (
    130,
    "b334beb55254ee8908ecf5938f6dee7f4bee02581271c2f246f3fe1ab7abf140",
)
EXPECTED_SPLIT_EXACT_QUERY_RECORDS = (
    123,
    "ec30d57b483e05ad265c5815f32b00b08910c057f8f1aa984709097a065dad2c",
)
SPLIT_NONEXACT_QUERY_WITNESSES = {
    "BACK-MATTER/Colophon/Colophon.md:4909": (22352,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:225": (
        7926,
        7936,
    ),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:229": (
        7930,
    ),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:235": (
        7936,
    ),
    "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:171": (
        854,
    ),
    "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:179": (
        862,
    ),
    "CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Mechanisms-in-Programs-and-Nature.md:707": (
        4136,
    ),
}
EXPECTED_SPLIT_NONEXACT_QUERY_RECORDS_DIGEST = (
    "2a3e067f993f98f53390ca9fc3c45bbc53bc8d22f9f5bafd637eef2afdfda99d"
)
EXPECTED_SPLIT_DIRECT_NAME_PATHS = frozenset(
    {
        "BACK-MATTER/Colophon/Colophon.md",
        "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md",
    }
)
EXPECTED_EXACT_RETAINED_MIRRORS = (
    19,
    "ec75fcfed5356d02fbaac3f1fca656660e8ae3a4d8f01a6e6f9d9bfeb13e6e98",
)
SPLIT_NONEXACT_RETAINED = frozenset({854, 858, 860, 862, 922, 926, 932})
EXPECTED_SPLIT_NONEXACT_RETAINED_DIGEST = (
    "83ac5973d0172f979bb8ab6f2ea4f962aa7593daa58bd9e93dbc8ab875336f98"
)
SPLIT_NONEXACT_RETAINED_WITNESSES = {
    854: "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:171",
    858: "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:175",
    860: "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:177",
    862: "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:179",
    922: "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:239",
    926: "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:243",
    932: "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:249",
}

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
        raise SystemExit("usage: 29-T11-source-oracle.py [BOOK]")
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
        and len(DIRECT_NAME_STREAM_RX.findall(text)) == 6
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
        and len(union | GOVERNED_CONTINUATIONS) == 136
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
    split_q09: set[str] = set()
    split_q11: set[str] = set()
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
            matching = {name for name, rx in compiled.items() if rx.search(line)}
            if not matching:
                continue
            split_records.add(record)
            if "Q09" in matching:
                split_q09.add(record)
            if "Q11" in matching:
                split_q11.add(record)
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
        and not split_q09
        and not split_q11
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
        digest_records(split_exact_records),
        digest_records(split_nonexact_records),
    )
    if not split_query_ok:
        print("split_nonexact_records", sorted(split_nonexact_records))
        print("split_direct_name_stream_hits", sorted(split_direct_name_stream_hits))

    exact_retained_mirror = {n for n in RETAINED if lines[n - 1] in split_texts}
    split_nonexact_retained = set(RETAINED) - exact_retained_mirror
    retained_split_ok = (
        (len(exact_retained_mirror), digest(exact_retained_mirror))
        == EXPECTED_EXACT_RETAINED_MIRRORS
        and split_nonexact_retained == SPLIT_NONEXACT_RETAINED
        and digest(split_nonexact_retained)
        == EXPECTED_SPLIT_NONEXACT_RETAINED_DIGEST
        and set(SPLIT_NONEXACT_RETAINED_WITNESSES) == split_nonexact_retained
        and set(SPLIT_NONEXACT_RETAINED_WITNESSES.values()) <= all_split_records
    )
    ok &= retained_split_ok
    print(
        "split_retained",
        "OK" if retained_split_ok else "MISMATCH",
        len(exact_retained_mirror),
        len(split_nonexact_retained),
        digest(exact_retained_mirror),
        digest(split_nonexact_retained),
        sorted(split_nonexact_retained),
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
        and not compiled["Q09"].search("\n".join(atlas_lines))
        and not compiled["Q11"].search("\n".join(atlas_lines))
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
        and catalog_lines[11] == "Generalized Mobile Automata,"
        and len(set(catalog_lines[1:])) == 45
        and "## 11. Generalized Mobile Automata" in taxonomy_text
    )
    ok &= catalog_ok
    print("catalog", "OK" if catalog_ok else "MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
