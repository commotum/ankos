#!/usr/bin/env python3
"""Frozen T10 Extended Mobile Automata raster-asset closure oracle."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


if not __debug__:
    raise RuntimeError("T10 asset verification requires assertions; do not run with -O")

ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "ref/A-New-Kind-of-Science"
BOOK = ASSET_ROOT / "A-New-Kind-of-Science.md"

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

# Core construction/caption/Notes/variant anchors. This is deliberately not
# every generic occurrence of "mobile automaton": T10 requires the evidenced
# three-cell replacement result, its governed Chapter 3 run, or a typed
# relation/control boundary. BOOK:12002 is retained because its mixed motion
# plate explicitly maps cases (a)-(c) to pages 73-75.
SOURCE_ANCHORS = {882, 890, 898, 11982, 11993, 12002, 16066, 16068}
for line_number in SOURCE_ANCHORS:
    assert lines[line_number - 1].strip(), line_number

# Mechanical bounded candidates. The three page-75 rasters are outside this
# set and enter only because BOOK:904 explicitly says "shown on the facing
# page"; the caption at BOOK:912 governs the complete three-file plate.
C4 = {
    line_number
    for line_number in images
    if min(abs(line_number - source) for source in SOURCE_ANCHORS) <= 4
}
Q = {906, 908, 910}
assert C4 == {886, 888, 892, 896, 900, 902, 11998, 12000, 12004, 12006, 16070}
assert Q.isdisjoint(C4)
U = C4 | Q

# C: direct construction evidence: a strict T10 rule table or the independently
# evidenced reversible three-cell-write variant. O: direct observer evidence:
# an evolution or compressed run. R: a later mixed rule/motion relation plate
# whose caption maps panels (a)-(c) to pages 73-75. X: inspected adjacency
# controls that belong to T09 or T11. C/O classify evidence role only; raster
# layout is never native configuration, RULE, UPDATE, or trace representation.
C = {888, 896, 910, 16070}
O = {886, 892, 900, 902, 906, 908}
R = {12004}
X = {11998, 12000, 12006}
groups = (C, O, R, X)
assert all(groups[a].isdisjoint(groups[b]) for a in range(4) for b in range(a))
assert C | O | R | X == U
assert (len(C4), len(Q), len(U), len(C), len(O), len(R), len(X)) == (11, 3, 14, 4, 6, 1, 3)


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


def ledger() -> tuple[str, int, int, int]:
    """Return the exact LF-terminated ledger and reference/hash totals."""

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
        kind = (
            "C"
            if book_line in C
            else "O"
            if book_line in O
            else "R"
            if book_line in R
            else "X"
        )
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
            f"{book_line}|{kind}|{path.relative_to(ASSET_ROOT).as_posix()}|{len(data)}|"
            f"{width}|{height}|{digest}|"
            f"{split_path.relative_to(ASSET_ROOT).as_posix()}|{split_line}"
        )

    payload = "\n".join(rows) + "\n"
    return payload, monolith_references, split_references, len(hashes)


EXPECTED_UNIVERSE_SHA256 = "8914fda71f91933f3de2785ed01470291443a3fe75ee709e0d0621f306353354"
EXPECTED_LEDGER_SHA256 = "25bda40f87de92226bbe1ed6b6461987429814aec3e7574efc637fdd3590304a"


def main() -> None:
    universe_payload = ",".join(map(str, sorted(U))).encode("ascii")
    assert hashlib.sha256(universe_payload).hexdigest() == EXPECTED_UNIVERSE_SHA256
    payload, monolith_references, split_references, hashes = ledger()
    assert len(payload.splitlines()) == 14
    assert hashlib.sha256(payload.encode("utf-8")).hexdigest() == EXPECTED_LEDGER_SHA256
    assert (monolith_references, split_references, hashes) == (14, 14, 14)
    print(
        "T10 asset oracle: PASS C4/Q=11/3; assets=14; "
        "classes C/O/R/X=4/6/1/3(direct=10); refs=28(monolith=14,split=14); "
        "unique_hashes=14"
    )


if __name__ == "__main__":
    main()
