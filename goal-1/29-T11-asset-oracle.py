#!/usr/bin/env python3
"""Frozen native physical-asset fixed point for T11 Generalized Mobile Automata.

This oracle deliberately starts from the native Chapter 3 construction and
its malformed Notes implementation fragment.  The broader source-neighborhood
ledger is bound below through ``29-T11-source-oracle.py`` once that source
closure is frozen; it must never be inferred from the catalog summary.
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

# The extracted Notes lost the Generalized Mobile Automata heading and the
# opening of its implementation paragraph.  Lines 12008/12010 are nevertheless
# the direct prose/code fragment.  Their radius-four images are both *before*
# the fragment and governed by the preceding page-75 active-motion note, so
# they are frozen as adjacency controls rather than T11 evidence.
NOTES_ROOTS = {12008, 12010}
NOTES_C4 = near(NOTES_ROOTS)
assert NOTES_C4 == {12004, 12006}

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

# C: direct construction/rule evidence.  O: direct evolution observer.  R:
# typed predecessor/successor relation.  X: mechanical Notes adjacency control.
# Figure 932 contains both eight rules and their evolutions, so construction is
# its stronger role; C/O never imply that raster layout is native state.
C = {922, 932}
O = {926}
R = PREDECESSOR_C4 | SUCCESSOR_C4
X = NOTES_C4
U_NATIVE = C | O | R | X
assert U_NATIVE == CHAPTER_C4 | NOTES_C4 | PREDECESSOR_C4 | SUCCESSOR_C4
assert (len(C), len(O), len(R), len(X), len(U_NATIVE)) == (2, 1, 7, 2, 12)

REASON_NATIVE: dict[int, str] = {}
for line_number in C:
    REASON_NATIVE[line_number] = "native generalized-mobile rule/construction plate"
for line_number in O:
    REASON_NATIVE[line_number] = "native generalized-mobile evolution observer"
for line_number in PREDECESSOR_C4:
    REASON_NATIVE[line_number] = "single-active extended-mobile predecessor relation"
for line_number in SUCCESSOR_C4:
    REASON_NATIVE[line_number] = "single-head Turing successor relation"
for line_number in X:
    REASON_NATIVE[line_number] = "preceding page-75 motion-note adjacency control"
assert set(REASON_NATIVE) == U_NATIVE

guards = {
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


EXPECTED_NATIVE_UNIVERSE_SHA256 = "03213cdcaadd65139dd945acb5feb30c5b1d8a8a177a29f58f67234289fe87af"
EXPECTED_NATIVE_LEDGER_SHA256 = "4cba5c5a9871543eb977b9aeb3facd368daad6be7400ed656048d2c04b11cd73"


def main() -> None:
    universe_payload = ",".join(map(str, sorted(U_NATIVE))).encode("ascii")
    universe_digest = hashlib.sha256(universe_payload).hexdigest()
    classes = {
        line_number: (
            "C" if line_number in C else "O" if line_number in O else "R" if line_number in R else "X"
        )
        for line_number in U_NATIVE
    }
    payload, monolith_references, split_references, hashes = ledger(U_NATIVE, classes)
    ledger_digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    assert universe_digest == EXPECTED_NATIVE_UNIVERSE_SHA256
    assert ledger_digest == EXPECTED_NATIVE_LEDGER_SHA256
    assert len(payload.splitlines()) == 12
    assert (monolith_references, split_references, hashes) == (12, 12, 12)
    print(
        "T11 native asset oracle: PASS assets=12; classes C/O/R/X=2/1/7/2(direct=3); "
        "refs=24(monolith=12,split=12); unique_hashes=12; source_binding=pending"
    )


if __name__ == "__main__":
    main()
