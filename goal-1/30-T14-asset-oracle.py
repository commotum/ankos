#!/usr/bin/env python3
"""Frozen T14 Neighbor-Dependent Substitution Systems asset closure."""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path


if not __debug__:
    raise RuntimeError("T14 asset verification requires assertions; do not run with -O")

ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "ref/A-New-Kind-of-Science"
BOOK = ASSET_ROOT / "A-New-Kind-of-Science.md"
SOURCE_ORACLE_PATH = ROOT / "goal-1/30-T14-source-oracle.py"

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
    assert SOURCE_ORACLE_PATH.is_file(), "T14 source oracle is not frozen yet"
    spec = importlib.util.spec_from_file_location("t14_source_oracle", SOURCE_ORACLE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SOURCE = load_source_oracle()
S = set(SOURCE.RETAINED)
assert len(S) == 40
assert SOURCE.digest(S) == "24213ee950c26341f210496994a3b91202ccb5c560c1b078192ee85a8b33410a"


def near(source_lines: set[int], radius: int = 4) -> set[int]:
    assert source_lines
    return {
        line_number
        for line_number in images
        if min(abs(line_number - source) for source in source_lines) <= radius
    }


# Mechanical source closure.  Q is the semantic fixed-point delta: immediate
# predecessor, same-caption/two-view, explicit next-page, and same-plate
# companions not reached by C4.  The 13800 addition is an adjacency control:
# all three Mandelbrot rasters share one preceding caption and must be frozen
# together even though none is T14 evidence.
C4 = near(S)
assert C4 == {
    988,
    990,
    1014,
    1020,
    1034,
    1044,
    1048,
    1066,
    2354,
    5932,
    5950,
    5958,
    8018,
    8026,
    12134,
    13802,
    13804,
}
Q = {1008, 1036, 2362, 5934, 13800}
assert C4.isdisjoint(Q)
U = C4 | Q

# The page-100 composite is the only native T14 raster.  It contains both
# construction tables and their evolution observers, so C is its stronger
# role.  R records typed construction/schedule/emulation relations; X records
# genuinely mechanical adjacency controls.
C = {1020}
O: set[int] = set()
R = {
    988,
    990,
    1008,
    1014,
    1034,
    1036,
    1044,
    1048,
    1066,
    2354,
    2362,
    5932,
    5934,
    5950,
    5958,
    8026,
}
X = {8018, 12134, 13800, 13802, 13804}
STRICT_U = C | O
assert C | O | R | X == U
assert not (C & O or C & R or C & X or O & R or O & X or R & X)
assert (len(C4), len(Q), len(U), len(C), len(O), len(R), len(X)) == (
    17,
    5,
    22,
    1,
    0,
    16,
    5,
)

REASON: dict[int, str] = {}
REASON[1020] = "native pair-context rule tables and rescaled evolutions"
for line_number in {988, 990, 1008, 1014}:
    REASON[line_number] = "neighbor-independent substitution predecessor relation"
for line_number in {1034, 1036, 1044, 1048}:
    REASON[line_number] = "creation/destruction or multicolor contextual successor relation"
REASON[1066] = "sequential substitution schedule contrast"
for line_number in {2354, 2362}:
    REASON[line_number] = "geometric/2D contextual-substitution relation"
for line_number in {5932, 5934, 5950, 5958}:
    REASON[line_number] = "general/sequential substitution schedule and causal relation"
REASON[8026] = "one-output neighbor-dependent CA-emulation relation"
REASON[8018] = "mechanical preceding Turing-emulation adjacency control"
REASON[12134] = "mechanical neighbor-independent growth-note adjacency control"
for line_number in {13800, 13802, 13804}:
    REASON[line_number] = "mechanical preceding Mandelbrot same-caption control"
assert set(REASON) == U


# Complete page inventory and hash-bound visual transcription.  There is only
# one physical page-100 raster and one monolith/split reference to it.
assert set(images) & set(range(1018, 1027)) == {1020}
page_100_files = {
    path.name
    for path in ASSET_ROOT.rglob("*.jpeg")
    if re.fullmatch(r"_page_100_.+\.jpeg", path.name)
}
assert page_100_files == {"_page_100_Picture_3.jpeg"}

HASH_BOUND_VISUAL_SHA256 = {
    1020: "25df45fbfcb5f0f57d18779b2b8af7cb31c9a9400d81b69779663c448882d183",
    8026: "66295968a40bcb9140d67e3fba6ec15420849d298afac6ddf6583b5108f9c51a",
}
VISUAL_FACTS = {
    "seed": "both displayed evolutions begin 0110 (light,dark,dark,light)",
    "rule_1": "11->01, 10->10, 01->0, 00->01",
    "rule_2": "11->00, 10->11, 01->1, 00->0 (raster-only transcription)",
    "observer": "each generation is horizontally rescaled to one equal display width",
    "boundary": "rightmost old element has no source result; no pad/wrap/sentinel is shown",
}
assert set(VISUAL_FACTS) == {"seed", "rule_1", "rule_2", "observer", "boundary"}

# Page 681 is classified R because the displayed cellular automata are target
# systems in an emulation comparison.  Its hash-bound native substitution
# tables nevertheless establish useful restrictions: the left table exhausts
# the four ordered binary pairs, the right table exhausts the nine ordered
# three-color pairs, and every rule emits exactly one cell.  They are pair-read
# substitution tables, not the usual eight-row width-three elementary-CA table.
PAGE_681_VISUAL_FACTS = {
    "binary": "four ordered binary pair-input glyphs",
    "three_color": "nine ordered three-color pair-input glyphs",
    "output": "every glyph emits exactly one cell",
    "scope": "target cellular automata are an emulation relation, not the native rule-table shape",
}
assert set(PAGE_681_VISUAL_FACTS) == {"binary", "three_color", "output", "scope"}

Rule = dict[tuple[int, int], tuple[int, ...]]
Word = tuple[int, ...]
RULE_1: Rule = {
    (1, 1): (0, 1),
    (1, 0): (1, 0),
    (0, 1): (0,),
    (0, 0): (0, 1),
}
RULE_2_RASTER: Rule = {
    (1, 1): (0, 0),
    (1, 0): (1, 1),
    (0, 1): (1,),
    (0, 0): (0,),
}
SEED: Word = (0, 1, 1, 0)


def step(rule: Rule, word: Word) -> Word:
    assert set(rule) == {(0, 0), (0, 1), (1, 0), (1, 1)}
    return tuple(
        value
        for source in range(max(0, len(word) - 1))
        for value in rule[(word[source], word[source + 1])]
    )


def trace(rule: Rule, word: Word, steps: int) -> tuple[Word, ...]:
    rows = [word]
    for _ in range(steps):
        word = step(rule, word)
        rows.append(word)
    return tuple(rows)


assert trace(RULE_1, SEED, 3) == (
    (0, 1, 1, 0),
    (0, 0, 1, 1, 0),
    (0, 1, 0, 0, 1, 1, 0),
    (0, 1, 0, 0, 1, 0, 0, 1, 1, 0),
)
assert trace(RULE_2_RASTER, SEED, 3) == (
    (0, 1, 1, 0),
    (1, 0, 0, 1, 1),
    (1, 1, 0, 1, 0, 0),
    (0, 0, 1, 1, 1, 1, 1, 0),
)

guards = {
    984: "each one of these elements is replaced by a new block of elements",
    1016: "The evolution of the same substitution systems as on the previous page",
    1018: "color of the element immediately to its right",
    1022: "the rightmost element is always dropped",
    1024: "In the first example",
    1026: "every single element should be replaced by at least one new element",
    1032: "Two views of a substitution system whose rules allow both creation and destruction",
    1046: "only the order of elements is ever significant",
    1050: "works almost exactly like a cellular automaton",
    1068: "first sequence BA that is found should be replaced by ABA",
    2356: "picture at the top of the next page",
    5930: "relations between updating events can be represented by a causal network",
    5936: "Examples of sequential substitution systems",
    5944: "pictures on the next page",
    5952: "Examples of general substitution systems and the causal networks",
    5960: "when replacements are performed at random",
    5962: "three different ways that replacements can be made",
    8024: "neighbor-dependent substitution systems",
    8028: "highly uniform rules always yielding just one cell",
    12109: "first one on page 85",
    12111: "\\{1, 1\\}",
    12113: "Partition[#, 2, 1]",
    12115: "initial condition for the first example on page 85 is",
    13806: "Page 192 · Neighbor-dependent substitution systems",
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
            assert digest == HASH_BOUND_VISUAL_SHA256[book_line], (book_line, digest)
        hashes.add(digest)
        width, height = jpeg_size(data)
        split_path, split_line = split_hits[0]
        rows.append(
            f"{book_line}|{kind}|{path.relative_to(ASSET_ROOT).as_posix()}|{len(data)}|"
            f"{width}|{height}|{digest}|"
            f"{split_path.relative_to(ASSET_ROOT).as_posix()}|{split_line}"
        )

    payload = "\n".join(rows) + "\n"
    return payload, monolith_references, split_references, len(hashes)


EXPECTED_STRICT_UNIVERSE_SHA256 = "f296867839c8befafed32b55a7c11ab4ad14387d2434b970a55237d537bc9353"
EXPECTED_STRICT_LEDGER_SHA256 = "40c2178d7353f36f16ff37d5c2f70b74cbbe6707dd0ca01cb3fc3b0ba7b9f54c"
EXPECTED_UNIVERSE_SHA256 = "1811099e5169b328d8ea60789acc84104069a71fd5ecee9278628d46bd90f8ab"
EXPECTED_LEDGER_SHA256 = "723881f59dd4b41da523b825c3c777c0532804ee5cc75b15576820070bec9ae4"


def main() -> None:
    payload, monolith_references, split_references, hashes = ledger()
    universe_digest = hashlib.sha256(",".join(map(str, sorted(U))).encode("ascii")).hexdigest()
    ledger_digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    strict_rows = [
        row for row in payload.splitlines() if int(row.split("|", 1)[0]) in STRICT_U
    ]
    strict_payload = "\n".join(strict_rows) + "\n"
    strict_universe_digest = hashlib.sha256(
        ",".join(map(str, sorted(STRICT_U))).encode("ascii")
    ).hexdigest()
    strict_ledger_digest = hashlib.sha256(strict_payload.encode("utf-8")).hexdigest()
    assert strict_universe_digest == EXPECTED_STRICT_UNIVERSE_SHA256
    assert strict_ledger_digest == EXPECTED_STRICT_LEDGER_SHA256
    assert universe_digest == EXPECTED_UNIVERSE_SHA256
    assert ledger_digest == EXPECTED_LEDGER_SHA256
    assert len(strict_rows) == 1 and len(payload.splitlines()) == 22
    assert (monolith_references, split_references, hashes) == (22, 22, 22)
    print(
        "T14 asset oracle: PASS source=40; C4/Q=17/5; assets=22; strict=1; "
        "classes C/O/R/X=1/0/16/5(direct=1); "
        "refs=44(monolith=22,split=22); unique_hashes=22; "
        "page100_rules/seeds/rows/rescaling/right_edge=PASS"
    )


if __name__ == "__main__":
    main()
