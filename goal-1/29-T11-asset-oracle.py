#!/usr/bin/env python3
"""Frozen native physical-asset fixed point for T11 Generalized Mobile Automata.

This oracle starts from the native Chapter 3 construction and its malformed
Notes implementation fragment, then binds the exhaustive source-neighborhood
ledger through ``29-T11-source-oracle.py``.  Nothing is inferred from the
catalog summary.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path


if not __debug__:
    raise RuntimeError("T11 asset verification requires assertions; do not run with -O")

ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "ref/A-New-Kind-of-Science"
BOOK = ASSET_ROOT / "A-New-Kind-of-Science.md"
SOURCE_ORACLE_PATH = ROOT / "goal-1/29-T11-source-oracle.py"

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


def near(source_lines: set[int], radius: int = 4) -> set[int]:
    """Return the mechanical raster neighborhood of a frozen source set."""

    assert source_lines
    return {
        line_number
        for line_number in images
        if min(abs(line_number - source) for source in source_lines) <= radius
    }


# Complete native main-text passage.  These are semantic text/caption roots,
# not search hits and not the local catalog paraphrase.  At radius four the
# three governed rasters are already a fixed point: the line-928 facing-page
# pointer lands on 932, and no additional same-caption/panel companion exists.
CHAPTER_ROOTS = {916, 918, 920, 924, 928, 930, 934}
CHAPTER_C4 = near(CHAPTER_ROOTS)
assert CHAPTER_C4 == {922, 926, 932}
assert set(images) & set(range(916, 935)) == CHAPTER_C4
direct_page_files = {
    path.name
    for path in ASSET_ROOT.rglob("*.jpeg")
    if re.fullmatch(r"_page_9[12]_.+\.jpeg", path.name)
}
assert direct_page_files == {
    "_page_91_Figure_6.jpeg",
    "_page_91_Figure_8.jpeg",
    "_page_92_Figure_1.jpeg",
}

# The extracted Notes lost the Generalized Mobile Automata heading and the
# opening of its implementation paragraph.  Lines 12008/12010 are nevertheless
# the direct prose/code fragment.  Their radius-four images are both *before*
# the fragment and governed by the preceding page-75 active-motion note, so
# they are frozen as adjacency controls rather than T11 evidence.
NOTES_ROOTS = {12008, 12010}
NOTES_C4 = near(NOTES_ROOTS)
assert NOTES_C4 == {12004, 12006}
assert not (set(images) & set(range(12008, 12012)))

# Relation siblings close the native section boundaries.  The predecessor
# paragraph explicitly points both upward and to its facing page; the successor
# is the first Turing construction/caption.  Radius four closes both plates and
# stops before unrelated earlier T10 and later Turing examples.
PREDECESSOR_ROOTS = {904, 912, 914}
PREDECESSOR_C4 = near(PREDECESSOR_ROOTS)
assert PREDECESSOR_C4 == {900, 902, 906, 908, 910}

SUCCESSOR_ROOTS = {940, 942, 948}
SUCCESSOR_C4 = near(SUCCESSOR_ROOTS)
assert SUCCESSOR_C4 == {944, 946}

assert not (
    CHAPTER_C4 & NOTES_C4
    or CHAPTER_C4 & PREDECESSOR_C4
    or CHAPTER_C4 & SUCCESSOR_C4
    or NOTES_C4 & PREDECESSOR_C4
    or NOTES_C4 & SUCCESSOR_C4
    or PREDECESSOR_C4 & SUCCESSOR_C4
)

# C: direct construction/rule evidence.  O: direct evolution observer.  The
# final R/X classes are completed after binding the exhaustive source closure.
# Figure 932 contains both eight rules and their evolutions, so construction is
# its stronger role; C/O never imply that raster layout is native state.
C = {922, 932}
O = {926}
STRICT_U = C | O
assert STRICT_U == CHAPTER_C4 and len(STRICT_U) == 3

# Hash-bound visual transcription.  This is deliberately more precise than
# the prose shorthand "move", "split in two", and "disappear": black activity
# dots in the result glyphs occupy relative offsets in {-1, 0, +1}.  In
# particular, the native plates visibly contain empty, stationary-only,
# stationary-plus-right, and all-three output sets.  Thus the raster evidence
# rules out any result schema restricted to one moving destination or exactly
# two children.  It does not by itself define behavior outside this strict
# radius-one binary construction.
DIRECT_VISUAL_SHA256 = {
    922: "841e52174bee649faa4f32c351235609b41f08d875351f4e04e328fe1d0dc3db",
    926: "2c1a760d55d31820631bfee265514a276033fe3c6c720a43c2e27da9306e50fe",
    932: "5bb405f6fa8114431bc2d83d4005d8154d026a5337fda5277defa11c41989f1c",
}
VISUAL_FACTS = {
    922: "rule strip returns a new source color plus a set of relative activity dots",
    926: "uniform-white visible initial row has one central active dot; evolution proliferates dots",
    932: "all eight panels start from one dot on white; rules include {}, {0}, {0,+1}, {-1,0,+1}",
}
assert set(DIRECT_VISUAL_SHA256) == set(VISUAL_FACTS) == C | O
# Panel frames/crops expose no boundary symbol, edge rule, wrapping, reflection,
# finite capacity, or other semantic boundary behavior.
VISUAL_BOUNDARY_FINDING = "display crop only; no native finite-edge semantics"

guards = {
    846: "three-color totalistic cellular automaton with code number 1599",
    862: "An example of a mobile automaton",
    868: "Examples of mobile automata with various rules",
    898: "A mobile automaton that yields a pattern with seemingly random features",
    904: "example shown on the facing page",
    912: "Each column above shows 400 steps",
    916: "a class of generalized mobile automata",
    918: "an active cell can split in two, or can disappear entirely",
    920: "new active cells end up being created every few steps",
    924: "any number of cells can be active at a time",
    928: "first few pictures on the facing page",
    930: "large numbers of cells are active at the same time",
    934: "active cells proliferate forever",
    940: "single active cell, known as the \"head\"",
    948: "one active cell or \"head\"",
    12002: "positions of the active cell for 20,000 steps",
    12008: "a list of the positions of active cells",
    12010: "GMAStep[rules\\_, {list\\_, nlist\\_}]",
}
for line_number, fragment in guards.items():
    assert fragment in lines[line_number - 1], (line_number, fragment)


def load_source_oracle():
    """Load the exhaustive source closure when its frozen oracle is present."""

    assert SOURCE_ORACLE_PATH.is_file(), "T11 source oracle is not frozen yet"
    spec = importlib.util.spec_from_file_location("t11_source_oracle", SOURCE_ORACLE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SOURCE = load_source_oracle()
S = set(SOURCE.RETAINED)
assert len(S) == 26
assert SOURCE.digest(S) == "15ec07596824fc5034feaba4735d329e74826b2849fa260b7053bbf07fe1ce8c"

# Mechanical zero-remainder ledger from all 26 retained source lines.  The
# only incidental raster is 844, the preceding cellular-automaton plate.  Q
# adds six explicitly governed predecessor/successor companions that are not
# within radius four of a retained source line.  No caption, facing-page,
# Notes, or section-boundary pointer remains outside U.
C4 = near(S)
assert C4 == {844, 858, 860, 866, 910, 922, 926, 932, 12004, 12006}
Q = (PREDECESSOR_C4 | SUCCESSOR_C4) - C4
assert Q == {900, 902, 906, 908, 944, 946}
assert C4.isdisjoint(Q)
U = C4 | Q

R_SOURCE = {858, 860, 866, 910}
R = R_SOURCE | PREDECESSOR_C4 | SUCCESSOR_C4
X = {844} | NOTES_C4
assert C | O | R | X == U
assert not (C & O or C & R or C & X or O & R or O & X or R & X)
assert (len(C4), len(Q), len(U), len(C), len(O), len(R), len(X)) == (
    10,
    6,
    16,
    2,
    1,
    10,
    3,
)

REASON: dict[int, str] = {}
for line_number in C:
    REASON[line_number] = "native generalized-mobile rule/construction plate"
for line_number in O:
    REASON[line_number] = "native generalized-mobile evolution observer"
for line_number in R_SOURCE:
    REASON[line_number] = "ordinary/extended single-active inherited-shape relation"
for line_number in PREDECESSOR_C4 - R_SOURCE:
    REASON[line_number] = "single-active extended-mobile predecessor relation"
for line_number in SUCCESSOR_C4:
    REASON[line_number] = "single-head Turing successor relation"
REASON[844] = "mechanical previous-section cellular-automaton adjacency control"
for line_number in NOTES_C4:
    REASON[line_number] = "preceding page-75 motion-note adjacency control"
assert set(REASON) == U


def jpeg_size(data: bytes) -> tuple[int, int]:
    """Read JPEG dimensions without adding a library dependency."""

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


def ledger(universe: set[int], classes: dict[int, str]) -> tuple[str, int, int, int]:
    """Return exact LF-terminated physical/reference ledger and totals."""

    assert set(classes) == universe
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
    for book_line in sorted(universe):
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
        if book_line in DIRECT_VISUAL_SHA256:
            assert digest == DIRECT_VISUAL_SHA256[book_line], (book_line, digest)
        hashes.add(digest)
        width, height = jpeg_size(data)
        split_path, split_line = split_hits[0]
        rows.append(
            f"{book_line}|{classes[book_line]}|{path.relative_to(ASSET_ROOT).as_posix()}|"
            f"{len(data)}|{width}|{height}|{digest}|"
            f"{split_path.relative_to(ASSET_ROOT).as_posix()}|{split_line}"
        )

    payload = "\n".join(rows) + "\n"
    return payload, monolith_references, split_references, len(hashes)


EXPECTED_STRICT_UNIVERSE_SHA256 = "daa4b34781edb487e6dc388cbe60f94a261c27d2fcc9c00a23a0d5bca2d2d7f1"
EXPECTED_STRICT_LEDGER_SHA256 = "0c713a3c4775fac478c8b75907cd35fc0ec9518131c4790b116e92dac8ccd346"
EXPECTED_UNIVERSE_SHA256 = "48158fc4a89e8dcfdc2611799b0152309478a5c7d5f3aea439597f946b12fc8b"
EXPECTED_LEDGER_SHA256 = "bc00a4fac328069714ba8cd20713a6bb47774c1d0f2e8d06b491526f5a127c89"


def main() -> None:
    universe_payload = ",".join(map(str, sorted(U))).encode("ascii")
    universe_digest = hashlib.sha256(universe_payload).hexdigest()
    classes = {
        line_number: (
            "C" if line_number in C else "O" if line_number in O else "R" if line_number in R else "X"
        )
        for line_number in U
    }
    payload, monolith_references, split_references, hashes = ledger(U, classes)
    ledger_digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    strict_universe_payload = ",".join(map(str, sorted(STRICT_U))).encode("ascii")
    strict_universe_digest = hashlib.sha256(strict_universe_payload).hexdigest()
    strict_rows = [
        row for row in payload.splitlines() if int(row.split("|", 1)[0]) in STRICT_U
    ]
    strict_payload = "\n".join(strict_rows) + "\n"
    strict_ledger_digest = hashlib.sha256(strict_payload.encode("utf-8")).hexdigest()
    assert strict_universe_digest == EXPECTED_STRICT_UNIVERSE_SHA256
    assert strict_ledger_digest == EXPECTED_STRICT_LEDGER_SHA256
    assert universe_digest == EXPECTED_UNIVERSE_SHA256
    assert ledger_digest == EXPECTED_LEDGER_SHA256
    assert len(strict_rows) == 3 and len(payload.splitlines()) == 16
    assert (monolith_references, split_references, hashes) == (16, 16, 16)
    print(
        "T11 asset oracle: PASS source=26; C4/Q=10/6; assets=16; strict=3; "
        "classes C/O/R/X=2/1/10/3(direct=3); "
        "refs=32(monolith=16,split=16); unique_hashes=16"
    )


if __name__ == "__main__":
    main()
