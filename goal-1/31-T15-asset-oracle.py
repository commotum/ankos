#!/usr/bin/env python3
"""Frozen T15 Creation/Destruction Substitution Systems asset closure.

The prose establishes disappearance, balance, and possible die-out, but the
actual T15 tables and seeds occur only in the page-101/page-102 rasters.  This
oracle therefore hash-binds the source-derived asset fixed point, records the
direct visual transcription, and checks the transcribed rows against the one
old-snapshot adjacent-pair/ordered-concatenation operator from the T14 Notes.

An empty selected-source emission, a zero-source event on a word shorter than
two symbols, and a terminal/no-successor outcome are deliberately distinct.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path


if not __debug__:
    raise RuntimeError("T15 asset verification requires assertions; do not use -O")

ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "ref/A-New-Kind-of-Science"
BOOK = ASSET_ROOT / "A-New-Kind-of-Science.md"
SOURCE_ORACLE_PATH = ROOT / "goal-1/31-T15-source-oracle.py"

EXPECTED_BOOK_LINES = 22_498
EXPECTED_BOOK_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"

book_bytes = BOOK.read_bytes()
assert hashlib.sha256(book_bytes).hexdigest() == EXPECTED_BOOK_SHA256
lines = book_bytes.decode("utf-8").splitlines()
assert len(lines) == EXPECTED_BOOK_LINES

image_re = re.compile(r"^!\[\]\(([^)]*?\.jpeg)\)$")
images = {
    line_number: match.group(1)
    for line_number, line in enumerate(lines, 1)
    if (match := image_re.fullmatch(line))
}


def load_source_oracle():
    assert SOURCE_ORACLE_PATH.is_file(), "T15 source oracle is not frozen"
    spec = importlib.util.spec_from_file_location("t15_source_oracle", SOURCE_ORACLE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SOURCE = load_source_oracle()
S = set(SOURCE.RETAINED)
assert len(S) == 40
assert SOURCE.digest(S) == "03fc9177af658074d7a276757fcc742a1afb3e5fe976ec6b08d438c1a57f7e73"


def near(source_lines: set[int], radius: int = 4) -> set[int]:
    assert source_lines
    return {
        line_number
        for line_number in images
        if min(abs(line_number - source) for source in source_lines) <= radius
    }


# C4 is a mechanical radius-four closure over the frozen source set.  Q closes
# multi-raster captions and the direct predecessor relation: all three page-96
# Turing-machine panels, both views of the page-99 T13 systems, and all three
# page-904 Busy-Beaver panels are either included together or excluded
# together.  Iterating those caption/companion rules adds no further asset.
C4 = near(S)
assert C4 == {
    976,
    988,
    990,
    1014,
    1020,
    1034,
    1036,
    1044,
    1048,
    1066,
    1130,
    2354,
    2362,
    7942,
    7944,
    7946,
    12093,
    12095,
    12134,
}
Q = {972, 974, 1008, 12091}
assert C4.isdisjoint(Q)
U = C4 | Q

# C is construction/rule/trace evidence, O is an observer-only second view, R
# is a typed predecessor/schedule/emulation relation, and X is a mechanical
# adjacency control.  Page 102's evolution plate is C: its insets directly
# expose the ordered word trace even though row placement and connector lines
# are observers.
C = {1036, 1044, 1048}
O = {1034}
R = {
    988,
    990,
    1008,
    1014,
    1020,
    1066,
    1130,
    2354,
    2362,
    7942,
    7944,
    7946,
    12134,
}
X = {972, 974, 976, 12091, 12093, 12095}
STRICT_U = C | O
assert C | O | R | X == U
assert not (C & O or C & R or C & X or O & R or O & X or R & X)
assert (len(C4), len(Q), len(U), len(C), len(O), len(R), len(X)) == (
    19,
    4,
    23,
    3,
    1,
    13,
    6,
)

REASON: dict[int, str] = {
    1034: "observer-only equal-total-width view of the native binary trace",
    1036: "native binary pair table, seed, and fixed-size evolution",
    1044: "native three/four-color fixed-size evolutions and lineage insets",
    1048: "native three/four-color pair tables including epsilon outputs",
}
for line_number in {988, 990, 1008, 1014}:
    REASON[line_number] = "neighbor-independent non-erasing predecessor relation"
REASON[1020] = "neighbor-dependent non-epsilon predecessor relation"
REASON[1066] = "sequential-substitution schedule contrast"
REASON[1130] = "tag-system extinction/outcome contrast"
for line_number in {2354, 2362}:
    REASON[line_number] = "geometric/two-dimensional substitution relation"
for line_number in {7942, 7944, 7946}:
    REASON[line_number] = "cellular-automaton emulation relation"
REASON[12134] = "neighbor-independent growth observer relation"
for line_number in {972, 974, 976}:
    REASON[line_number] = "mechanical preceding Turing-machine same-caption control"
for line_number in {12091, 12093, 12095}:
    REASON[line_number] = "mechanical preceding Busy-Beaver same-caption control"
assert set(REASON) == U


HASH_BOUND_VISUAL_SHA256 = {
    1034: "669c209eabf0a35d9095bf553b1c959946f72da0b0584de566a3a9032240a50e",
    1036: "9390efdb915dfdf78e870f85b0f2964791a00714f8619525e256098b98919c4e",
    1044: "cc6b3fdffceecf66543d9f6dbfc1628913eec7356e11e5716473a112b5b728a4",
    1048: "77c261cf4c9b83d08aead4601916dbc6ac96f371b00a30549c96586295d18585",
}
NATIVE_FILE_FACTS = {
    1034: (33_265, 366, 370),
    1036: (26_355, 348, 360),
    1044: (300_371, 1120, 1263),
    1048: (22_030, 458, 175),
}
VISUAL_FACTS = {
    "page_101_views": (
        "the same binary evolution appears once rescaled to equal total width "
        "and once with fixed-size cells"
    ),
    "page_101_rule": "ordered binary inputs 11,10,01,00 include the native row 00->epsilon",
    "page_102_rules": (
        "four complete three-color pair tables and two complete four-color pair "
        "tables contain 0-, 1-, and 2-symbol emissions"
    ),
    "page_102_traces": "six fixed-size word traces display twelve rows t0..t11",
    "order": "connector insets show row-relative movement; sequence order, not plotted x, is state",
    "boundary": "the plates show no pad, wrap, sentinel, capacity, or copy-forward behavior",
}

Word = tuple[int, ...]
Rule = dict[tuple[int, int], Word]

# Direct raster transcriptions.  Colors are numbered lightest to darkest.
PAGE_101_RULE: Rule = {
    (1, 1): (1, 1),
    (1, 0): (0,),
    (0, 1): (1, 0),
    (0, 0): (),
}
PAGE_101_SEED: Word = (0, 1, 1, 0)
PAGE_101_DIRECT_ROWS = (
    "0110",
    "10110",
    "010110",
    "10010110",
    "010010110",
    "10010010110",
    "010010010110",
    "10010010010110",
    "010010010010110",
    "10010010010010110",
    "010010010010010110",
    "10010010010010010110",
)

PAGE_102_RULES: dict[str, Rule] = {
    "a": {
        (2, 2): (0,), (2, 1): (0,), (2, 0): (2,),
        (1, 2): (0, 0), (1, 1): (0, 1), (1, 0): (1, 1),
        (0, 2): (2,), (0, 1): (2,), (0, 0): (0,),
    },
    "b": {
        (2, 2): (2,), (2, 1): (0, 1), (2, 0): (0,),
        (1, 2): (), (1, 1): (), (1, 0): (2,),
        (0, 2): (0,), (0, 1): (0, 1), (0, 0): (2,),
    },
    "c": {
        (2, 2): (1,), (2, 1): (), (2, 0): (0, 1),
        (1, 2): (2, 1), (1, 1): (0, 2), (1, 0): (2, 2),
        (0, 2): (), (0, 1): (1, 2), (0, 0): (0,),
    },
    "d": {
        (2, 2): (2, 0), (2, 1): (1, 1), (2, 0): (2, 0),
        (1, 2): (2,), (1, 1): (1,), (1, 0): (),
        (0, 2): (0,), (0, 1): (0,), (0, 0): (2, 1),
    },
    "e": {
        (3, 3): (1, 2), (3, 2): (2, 3), (3, 1): (0,), (3, 0): (1, 0),
        (2, 3): (), (2, 2): (2,), (2, 1): (1, 3), (2, 0): (),
        (1, 3): (2, 0), (1, 2): (), (1, 1): (1,), (1, 0): (3, 0),
        (0, 3): (), (0, 2): (2, 0), (0, 1): (3, 3), (0, 0): (2, 2),
    },
    "f": {
        (3, 3): (1, 3), (3, 2): (0, 3), (3, 1): (2,), (3, 0): (),
        (2, 3): (0, 2), (2, 2): (), (2, 1): (0, 1), (2, 0): (3,),
        (1, 3): (0, 3), (1, 2): (0,), (1, 1): (2, 1), (1, 0): (2, 2),
        (0, 3): (), (0, 2): (3,), (0, 1): (1, 0), (0, 0): (1, 3),
    },
}
PAGE_102_SEEDS: dict[str, Word] = {
    "a": (0, 1, 1, 0),
    "b": (0, 1, 2, 1),
    "c": (0, 1, 1, 0),
    "d": (0, 1, 2, 0),
    "e": (0, 1, 0, 0),
    "f": (0, 1, 0, 0),
}
PAGE_102_DIRECT_ROWS = {
    "a": ("0110", "20111", "220101", "022112", "2000100", "2002110", "20200111", "222020101", "002222112", "0200000100", "2200002110", "02000200111"),
    "b": ("0121", "0101", "01201", "01001", "012201", "012001", "010201", "0120001", "0102201", "01202001", "01000201", "012220001"),
    "c": ("0110", "120222", "210111", "22120202", "1210101", "2122122212", "211211121", "0221020221", "122011", "211011202", "022212022101", "11210112212"),
    "d": ("0120", "0220", "02020", "020020", "02021020", "020011020", "0202101020", "0200110020", "020210121020", "0200110211020", "02021010111020", "0200110011020"),
    "e": ("0100", "333022", "121210202", "1313302020", "2002012102020", "22203313302020", "221202012102020", "213203313302020", "1320231202012102020", "2023200203313302020", "202322201202012102020", "20232233203313302020"),
    "f": ("0100", "102213", "2230103", "021022", "301223", "10002", "2213133", "010320313", "1022033203", "223313033", "021320313", "30103033203"),
}


def step(rule: Rule, word: Word) -> Word:
    """One snapshot-parallel event; always returns one complete word."""
    return tuple(
        value
        for source in range(max(0, len(word) - 1))
        for value in rule[(word[source], word[source + 1])]
    )


def trace(rule: Rule, seed: Word, steps: int) -> tuple[Word, ...]:
    rows = [seed]
    for _ in range(steps):
        rows.append(step(rule, rows[-1]))
    return tuple(rows)


def strings(rows: tuple[Word, ...]) -> tuple[str, ...]:
    return tuple("".join(str(value) for value in row) for row in rows)


assert set(PAGE_101_RULE) == {(1, 1), (1, 0), (0, 1), (0, 0)}
assert strings(trace(PAGE_101_RULE, PAGE_101_SEED, 11)) == PAGE_101_DIRECT_ROWS
assert {pair for pair, emitted in PAGE_101_RULE.items() if not emitted} == {(0, 0)}

for name, rule in PAGE_102_RULES.items():
    colors = 3 if name in "abcd" else 4
    assert set(rule) == {(left, right) for left in range(colors) for right in range(colors)}
    assert all(len(emitted) <= 2 and set(emitted) <= set(range(colors)) for emitted in rule.values())
    assert strings(trace(rule, PAGE_102_SEEDS[name], 11)) == PAGE_102_DIRECT_ROWS[name]

EPSILON_ROWS = {
    name: frozenset(pair for pair, emitted in rule.items() if not emitted)
    for name, rule in PAGE_102_RULES.items()
}
assert {name: len(rows) for name, rows in EPSILON_ROWS.items()} == {
    "a": 0,
    "b": 2,
    "c": 2,
    "d": 1,
    "e": 4,
    "f": 3,
}

# Direct-table consequences.  A two-symbol word has one selected source, so an
# epsilon row produces the empty *successor configuration*.  This is genuine
# extinction by an applied row, not the zero-eligible-source case represented
# by [] or [x], and never a zero-successor terminal outcome.
assert step(PAGE_101_RULE, (0, 0)) == ()
assert step(PAGE_101_RULE, ()) == ()
assert step(PAGE_101_RULE, (1,)) == ()
for name, epsilon_rows in EPSILON_ROWS.items():
    rule = PAGE_102_RULES[name]
    for pair in epsilon_rows:
        assert step(rule, pair) == ()
assert all(PAGE_102_DIRECT_ROWS[name][-1] for name in PAGE_102_DIRECT_ROWS)


guards = {
    1026: "every single element should be replaced by at least one new element",
    1028: "elements can simply disappear",
    1030: "creation and destruction of elements is almost perfectly balanced",
    1032: "Two views of a substitution system whose rules allow both creation and destruction",
    1038: "only by a fixed amount at each step",
    1046: "addition or subtraction of elements to its left",
    1050: "away from the right-hand edge",
    1052: "elements are created and destroyed throughout",
    1060: "operate in parallel on all the elements",
    1132: "all the elements are eventually removed from the sequence",
    12113: "Partition[#, 2, 1]",
}
for line_number, fragment in guards.items():
    assert fragment in lines[line_number - 1], (line_number, fragment)


def jpeg_size(data: bytes) -> tuple[int, int]:
    assert data[:2] == b"\xff\xd8"
    sof = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    offset = 2
    while offset < len(data):
        while offset < len(data) and data[offset] != 0xFF:
            offset += 1
        while offset < len(data) and data[offset] == 0xFF:
            offset += 1
        assert offset < len(data)
        marker = data[offset]
        offset += 1
        if marker in {0x00, 0x01} or 0xD0 <= marker <= 0xD9:
            continue
        segment_size = int.from_bytes(data[offset : offset + 2], "big")
        if marker in sof:
            width = int.from_bytes(data[offset + 5 : offset + 7], "big")
            height = int.from_bytes(data[offset + 3 : offset + 5], "big")
            return width, height
        offset += segment_size
    raise AssertionError("JPEG SOF marker not found")


def ledger() -> tuple[str, int, int, int]:
    split_markdown = sorted(
        path
        for path in ASSET_ROOT.rglob("*.md")
        if path.resolve() != BOOK.resolve() and path.name != "ANKoS-Atlas.md"
    )
    assert len(split_markdown) == 17

    monolith_by_name: dict[str, list[int]] = {}
    for line_number, reference in images.items():
        monolith_by_name.setdefault(Path(reference).name, []).append(line_number)

    split_by_name: dict[str, list[tuple[Path, int]]] = {}
    split_re = re.compile(r"^!\[\]\((?:Images/)?([^/()]+\.jpeg)\)$")
    for markdown in split_markdown:
        for line_number, line in enumerate(markdown.read_text(encoding="utf-8").splitlines(), 1):
            if match := split_re.fullmatch(line):
                split_by_name.setdefault(match.group(1), []).append((markdown, line_number))

    physical_by_name: dict[str, list[Path]] = {}
    for path in ASSET_ROOT.rglob("*.jpeg"):
        if path.is_file():
            physical_by_name.setdefault(path.name, []).append(path)

    rows: list[str] = []
    hashes: set[str] = set()
    monolith_references = 0
    split_references = 0
    for book_line in sorted(U):
        kind = "C" if book_line in C else "O" if book_line in O else "R" if book_line in R else "X"
        name = Path(images[book_line]).name
        monolith_hits = monolith_by_name.get(name, [])
        split_hits = split_by_name.get(name, [])
        physical_hits = physical_by_name.get(name, [])
        assert monolith_hits == [book_line], (book_line, monolith_hits)
        assert len(split_hits) == 1, (book_line, split_hits)
        assert len(physical_hits) == 1, (book_line, physical_hits)
        monolith_references += len(monolith_hits)
        split_references += len(split_hits)

        path = physical_hits[0]
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        assert digest not in hashes, (book_line, digest)
        if book_line in HASH_BOUND_VISUAL_SHA256:
            assert digest == HASH_BOUND_VISUAL_SHA256[book_line]
        hashes.add(digest)
        width, height = jpeg_size(data)
        if book_line in NATIVE_FILE_FACTS:
            assert (len(data), width, height) == NATIVE_FILE_FACTS[book_line]
        split_path, split_line = split_hits[0]
        rows.append(
            f"{book_line}|{kind}|{path.relative_to(ASSET_ROOT).as_posix()}|{len(data)}|"
            f"{width}|{height}|{digest}|"
            f"{split_path.relative_to(ASSET_ROOT).as_posix()}|{split_line}|{REASON[book_line]}"
        )

    return "\n".join(rows) + "\n", monolith_references, split_references, len(hashes)


payload, monolith_references, split_references, unique_hashes = ledger()
PAYLOAD_SHA256 = hashlib.sha256(payload.encode("utf-8")).hexdigest()
EXPECTED_PAYLOAD_SHA256 = "5ecf88946cd1a840d0a2444a562ee83592306b1693ddb3d31bbb057a31c3b38a"
assert PAYLOAD_SHA256 == EXPECTED_PAYLOAD_SHA256
assert (monolith_references, split_references, unique_hashes) == (23, 23, 23)

print(payload, end="")
print("closure", len(C4), len(Q), len(U))
print("classes", len(C), len(O), len(R), len(X))
print("references", monolith_references, split_references, unique_hashes)
print("payload_sha256", PAYLOAD_SHA256)
print("native_hashes", HASH_BOUND_VISUAL_SHA256)
print("epsilon_rows", {name: sorted(rows) for name, rows in EPSILON_ROWS.items()})
print("direct_rows", 12, 1 + len(PAGE_102_DIRECT_ROWS))
print("asset OK")
