#!/usr/bin/env python3
"""Bounded asset verifier for T25 two-dimensional Turing machines.

The source oracle owns the evidence boundary.  This verifier hash-binds its
exact twelve governed JPEG references: nine main-construction/path assets and
three files that together form the related Turing-machine-to-cellular-
automaton figure.  It verifies byte length, JPEG dimensions, SHA-256, the
unique physical file, and the exact monolith/split Markdown references.

This file does not transcribe a displayed rule table, recover a configuration
from pixels, or replay an evolution.  Captions, arrows, palette, layout,
coordinate orientation, rule-row order, and path geometry therefore remain
non-authoritative raster content.  The three CA-emulation files are relation
evidence, not the native identity of a T25 program.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path
from typing import NamedTuple


if not __debug__:
    raise RuntimeError("T25 asset verification requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "ref/A-New-Kind-of-Science"
BOOK = SOURCE_ROOT / "A-New-Kind-of-Science.md"
SOURCE_ORACLE_PATH = ROOT / "goal-1/37-T25-source-oracle.py"

EXPECTED_BOOK_LINES = 22_498
EXPECTED_BOOK_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_lines(values: set[int] | frozenset[int]) -> str:
    return hashlib.sha256(
        ",".join(map(str, sorted(values))).encode("ascii")
    ).hexdigest()


def load_source_oracle():
    assert SOURCE_ORACLE_PATH.is_file(), "T25 source oracle is not frozen"
    spec = importlib.util.spec_from_file_location("t25_source_oracle", SOURCE_ORACLE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


book_bytes = BOOK.read_bytes()
assert len(book_bytes.decode("utf-8").splitlines()) == EXPECTED_BOOK_LINES
assert sha256(book_bytes) == EXPECTED_BOOK_SHA256
BOOK_LINES = book_bytes.decode("utf-8").splitlines()

SOURCE = load_source_oracle()
RETAINED = set(SOURCE.RETAINED)
NATIVE = set(SOURCE.NATIVE_IMAGE_LINES)
RELATION = set(SOURCE.RELATION_IMAGE_LINES)
CONTROL = set(SOURCE.CONTROL_IMAGE_LINES)
GOVERNED = set(SOURCE.GOVERNED_IMAGE_LINES)

# Freeze the source oracle's public interface so an asset cannot silently
# enter, leave, or change evidence class underneath this dependent verifier.
EXPECTED_SOURCE_CONTRACT = {
    "retained": (63, "d65c11e7f57b120a83e9c37cd0d789ee591312f9a1316b41fae7c9ee194010b4"),
    "native_evidence": (30, "c7f09f0a15878ddf9078e96baface0169302db3ada59bc76e8f723a2ca86a848"),
    "relation_evidence": (29, "8339d80f08310f0c2b3dd75cf415730ab80e55d6735510a0438deec8852f04fe"),
    "control_evidence": (4, "8015743896a86aef3b04d12c93279f51c5f8eae5baf9fc7ed93545f6a16f268b"),
    "native_images": (6, "6cb059a1eaf065c9f6fdceff4dd39db0adab35db77584c819004ad49cfd99617"),
    "relation_images": (6, "143311c5f560e6b63d56cc7a3074518658e161c471db549f93a9a3fd4b7881d0"),
    "control_images": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "governed_images": (12, "259a790e9c6451ab832d1a2e4296ed587311377fdd9e5b9f7737dff6d2de8836"),
}

SOURCE_SETS = {
    "retained": set(SOURCE.RETAINED),
    "native_evidence": set(SOURCE.NATIVE_EVIDENCE),
    "relation_evidence": set(SOURCE.RELATION_EVIDENCE),
    "control_evidence": set(SOURCE.CONTROL_EVIDENCE),
    "native_images": NATIVE,
    "relation_images": RELATION,
    "control_images": CONTROL,
    "governed_images": GOVERNED,
}
for name, values in SOURCE_SETS.items():
    expected_count, expected_digest = EXPECTED_SOURCE_CONTRACT[name]
    assert len(values) == expected_count, (name, len(values), expected_count)
    assert digest_lines(values) == expected_digest, (name, digest_lines(values))


class AssetSpec(NamedTuple):
    role: str
    name: str
    physical: str
    split_markdown: str
    split_line: int
    byte_length: int
    width: int
    height: int
    digest: str
    boundary: str


CHAPTER5 = "CHAPTERS/5-Two-Dimensions-and-Beyond"
CHAPTER11 = "CHAPTERS/11-The-Notion-of-Computation"
SPLIT_NOTES = "BACK-MATTER/Index/Index.md"

ASSETS = {
    2268: AssetSpec(
        "N-MAIN-CONSTRUCTION",
        "_page_199_Figure_3.jpeg",
        f"{CHAPTER5}/Images/_page_199_Figure_3.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        125,
        102_643,
        1103,
        438,
        "b65dd6806bde965c1614329dcc2ae47057f8dde05a54ccbaa20305e6bd6d3977",
        "hash-bound construction plate; no arrow, row, direction, or rule transcription",
    ),
    2280: AssetSpec(
        "N-MAIN-EVOLUTION-A",
        "_page_200_Figure_2.jpeg",
        f"{CHAPTER5}/Images/_page_200_Figure_2.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        137,
        43_440,
        412,
        859,
        "f58612dc042ae05a475ea98b46188614c0ec6e1eae0e692d8859f9d34ffe6e33",
        "hash-bound evolution panel; no configuration or trace recovered from pixels",
    ),
    2284: AssetSpec(
        "N-MAIN-EVOLUTION-B",
        "_page_200_Figure_3.jpeg",
        f"{CHAPTER5}/Images/_page_200_Figure_3.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        141,
        41_398,
        395,
        559,
        "3f0504068aa39fb7b38ca21676f0d1d85ba2a8be3fec42d89be39f6b460dd99a",
        "hash-bound evolution panel; no configuration or trace recovered from pixels",
    ),
    2286: AssetSpec(
        "N-MAIN-EVOLUTION-C",
        "_page_200_Figure_4.jpeg",
        f"{CHAPTER5}/Images/_page_200_Figure_4.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        143,
        24_818,
        207,
        581,
        "a35c7b6aebb83ff9bb3e550a4bd181ae2d20c43d9f4a32222f1e4e4c18f2e760",
        "hash-bound evolution panel; no configuration or trace recovered from pixels",
    ),
    2290: AssetSpec(
        "N-MAIN-EVOLUTION-D",
        "_page_200_Figure_5.jpeg",
        f"{CHAPTER5}/Images/_page_200_Figure_5.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        147,
        39_684,
        407,
        478,
        "1adbd526c2281607fb41f52fcda1cdabba905596060717afb282c2701c438e0c",
        "hash-bound evolution panel; no configuration or trace recovered from pixels",
    ),
    2292: AssetSpec(
        "N-MAIN-RULE-PLATE",
        "_page_200_Figure_6.jpeg",
        f"{CHAPTER5}/Images/_page_200_Figure_6.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        149,
        28_717,
        520,
        240,
        "a9014f2192525ac1a2dd8903bb780bbf37bf4df8be6402b215c9789e5da98e23",
        "hash-bound displayed-rule plate; no glyph or table-row transcription",
    ),
    2298: AssetSpec(
        "R-MAIN-PATH-100K",
        "_page_201_Figure_2.jpeg",
        f"{CHAPTER5}/Images/_page_201_Figure_2.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        155,
        118_670,
        999,
        613,
        "b35ea13802354b9dc87d8040b14bab9430958ac96249ccfaeb8a486f46c89c46",
        "hash-bound path observer; path geometry is not transition state",
    ),
    2302: AssetSpec(
        "R-MAIN-PATH-500K",
        "_page_201_Figure_4.jpeg",
        f"{CHAPTER5}/Images/_page_201_Figure_4.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        159,
        36_839,
        999,
        614,
        "05facf4c932f70bfaeee9ef89d894342bba1aaa2be0027b16c7d8bba8f09770f",
        "hash-bound path observer; path geometry is not transition state",
    ),
    7942: AssetSpec(
        "R-TM-CA-ASSEMBLY-1",
        "_page_673_Figure_1.jpeg",
        f"{CHAPTER11}/Images/_page_673_Figure_1.jpeg",
        f"{CHAPTER11}/The-Notion-of-Computation.md",
        241,
        34_128,
        386,
        356,
        "eb21c4ab3390fc061d3d0903a7955a1d741857c2760b5b2fca514c28ce37332c",
        "hash-bound part of three-file TM-to-CA relation; not native T25 identity",
    ),
    7944: AssetSpec(
        "R-TM-CA-ASSEMBLY-2",
        "_page_673_Figure_2.jpeg",
        f"{CHAPTER11}/Images/_page_673_Figure_2.jpeg",
        f"{CHAPTER11}/The-Notion-of-Computation.md",
        243,
        48_054,
        453,
        420,
        "235c5cdab8a148120faf1c70d3f086f7cb3fafe55060f423095793a59eb45e43",
        "hash-bound part of three-file TM-to-CA relation; not native T25 identity",
    ),
    7946: AssetSpec(
        "R-TM-CA-ASSEMBLY-3",
        "_page_673_Figure_3.jpeg",
        f"{CHAPTER11}/Images/_page_673_Figure_3.jpeg",
        f"{CHAPTER11}/The-Notion-of-Computation.md",
        245,
        16_201,
        1065,
        70,
        "726a894fe2b74b87ccfa442d1abdec0a62a517c9c2bc0b0b323ea6dc04b0b162",
        "hash-bound part of three-file TM-to-CA relation; no CA-rule transcription",
    ),
    13674: AssetSpec(
        "R-NOTES-PATH",
        "_page_946_Picture_4.jpeg",
        "BACK-MATTER/Index/Images/_page_946_Picture_4.jpeg",
        SPLIT_NOTES,
        1575,
        27_683,
        565,
        218,
        "8448df7fc33c6c288461ce8b1e13a0fddd3f7ffe96004e98f4d2cb2e0b150f1f",
        "hash-bound Notes path observer; no path coordinates recovered from pixels",
    ),
}


MAIN_AND_PATH = {
    2268, 2280, 2284, 2286, 2290, 2292, 2298, 2302, 13674
}
TM_TO_CA_ASSEMBLY = {7942, 7944, 7946}
assert MAIN_AND_PATH.isdisjoint(TM_TO_CA_ASSEMBLY)
assert MAIN_AND_PATH | TM_TO_CA_ASSEMBLY == GOVERNED == set(ASSETS)
assert len(MAIN_AND_PATH) == 9
assert len(TM_TO_CA_ASSEMBLY) == 3
assert NATIVE == {2268, 2280, 2284, 2286, 2290, 2292}
assert RELATION == {2298, 2302, 7942, 7944, 7946, 13674}
assert not CONTROL
assert TM_TO_CA_ASSEMBLY <= RELATION


IMAGE_RE = SOURCE.IMAGE_RE
BOOK_IMAGES = {
    line_number: match.group(1)
    for line_number, line in enumerate(BOOK_LINES, 1)
    if (match := IMAGE_RE.fullmatch(line)) and match.group(1).endswith(".jpeg")
}
assert set(BOOK_IMAGES) & RETAINED == GOVERNED


def jpeg_size(data: bytes) -> tuple[int, int]:
    """Read JPEG dimensions without adding an image-library dependency."""

    assert data[:2] == b"\xff\xd8"
    start_of_frame = {
        0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
        0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
    }
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
        segment_length = int.from_bytes(data[offset : offset + 2], "big")
        assert segment_length >= 2
        if marker in start_of_frame:
            height = int.from_bytes(data[offset + 3 : offset + 5], "big")
            width = int.from_bytes(data[offset + 5 : offset + 7], "big")
            return width, height
        offset += segment_length
    raise AssertionError("JPEG SOF marker not found")


MARKDOWN_IMAGE_RE = re.compile(r"^!\[[^\]]*\]\(([^)]+\.jpeg)\)$")


def markdown_references(name: str) -> set[tuple[str, int]]:
    references: set[tuple[str, int]] = set()
    for markdown in SOURCE_ROOT.rglob("*.md"):
        relative = markdown.relative_to(SOURCE_ROOT).as_posix()
        for line_number, line in enumerate(
            markdown.read_text(encoding="utf-8").splitlines(), 1
        ):
            match = MARKDOWN_IMAGE_RE.fullmatch(line)
            if match and Path(match.group(1)).name == name:
                references.add((relative, line_number))
    return references


def asset_ledger() -> tuple[str, int, int, int]:
    rows: list[str] = []
    hashes: set[str] = set()
    total_bytes = 0
    total_references = 0
    for book_line, spec in sorted(ASSETS.items()):
        assert Path(BOOK_IMAGES[book_line]).name == spec.name
        physical = SOURCE_ROOT / spec.physical
        physical_hits = [
            path for path in SOURCE_ROOT.rglob(spec.name) if path.is_file()
        ]
        assert physical_hits == [physical], (book_line, physical_hits)

        data = physical.read_bytes()
        actual_digest = sha256(data)
        actual_width, actual_height = jpeg_size(data)
        assert len(data) == spec.byte_length, (book_line, len(data))
        assert (actual_width, actual_height) == (spec.width, spec.height), book_line
        assert actual_digest == spec.digest, (book_line, actual_digest)
        assert actual_digest not in hashes, (book_line, actual_digest)
        hashes.add(actual_digest)
        total_bytes += len(data)

        expected_references = {
            ("A-New-Kind-of-Science.md", book_line),
            (spec.split_markdown, spec.split_line),
        }
        actual_references = markdown_references(spec.name)
        assert actual_references == expected_references, (
            book_line, actual_references, expected_references
        )
        total_references += len(actual_references)

        split_line = (
            SOURCE_ROOT / spec.split_markdown
        ).read_text(encoding="utf-8").splitlines()[spec.split_line - 1]
        split_match = MARKDOWN_IMAGE_RE.fullmatch(split_line)
        assert split_match and Path(split_match.group(1)).name == spec.name

        rows.append(
            f"{book_line}|{spec.role}|{spec.name}|{spec.physical}|"
            f"{spec.byte_length}|{spec.width}|{spec.height}|{spec.digest}|"
            f"{spec.split_markdown}|{spec.split_line}|{spec.boundary}"
        )
    return "\n".join(rows) + "\n", total_bytes, total_references, len(hashes)


# These are textual source guards, not raster transcriptions.
SOURCE_TEXT_GUARDS = {
    2266: "move around on a two-dimensional grid",
    2270: "has no direct relationship to directions on the grid",
    2294: "all cells are initially white",
    2306: "The path traced out by the head",
    7938: "lighter colors in the cellular automaton represent ordinary cells",
    7948: "a Turing machine with a single step of cellular automaton evolution",
    13672: "2D position of the head at 500 successive steps",
}
for line_number, fragment in SOURCE_TEXT_GUARDS.items():
    assert line_number in RETAINED
    assert fragment in BOOK_LINES[line_number - 1], (line_number, fragment)


HASH_BOUND_ASSETS = set(ASSETS)
TRANSCRIBED_ASSETS: set[int] = set()
PIXEL_REPLAYED_ASSETS: set[int] = set()
assert HASH_BOUND_ASSETS == GOVERNED
assert not TRANSCRIBED_ASSETS
assert not PIXEL_REPLAYED_ASSETS


EXPECTED_TOTAL_BYTES = 562_275
EXPECTED_REFERENCE_COUNT = 24
EXPECTED_UNIQUE_HASHES = 12
EXPECTED_LEDGER_SHA256 = "8f5a72af45e65935b84b8fa6334b684dab88551c08dcad1565e574e9c1e08f4e"


def main() -> None:
    ledger, total_bytes, reference_count, unique_hashes = asset_ledger()
    ledger_digest = sha256(ledger.encode("utf-8"))
    assert ledger_digest == EXPECTED_LEDGER_SHA256, (
        ledger_digest, EXPECTED_LEDGER_SHA256
    )
    assert total_bytes == EXPECTED_TOTAL_BYTES
    assert reference_count == EXPECTED_REFERENCE_COUNT
    assert unique_hashes == EXPECTED_UNIQUE_HASHES

    print(
        "T25 asset oracle: PASS governed=12; main_and_path=9; "
        "TM_to_CA_relation_assembly=3; source native/relation/control=6/6/0; "
        "refs=24; unique_files=12; unique_hashes=12; bytes=562275; "
        "HASH_BOUND=12; TRANSCRIBED=0; PIXEL_REPLAYED=0; "
        "source_contract/monolith/split/hash/dimensions=PASS; unresolved=0"
    )


if __name__ == "__main__":
    main()
