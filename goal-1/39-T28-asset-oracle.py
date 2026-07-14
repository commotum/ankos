#!/usr/bin/env python3
"""Fail-closed asset/provenance audit for T28 contextual 2D substitution.

The governed asset universe is intentionally small.  It contains the native
page-207 T28 plate, the exact one-dimensional contextual predecessor and
singleton-output CA-emulation relation plates, and the seven Chapter 5 plates
that establish the T26/T27 dimensional controls immediately preceding T28.

Every governed JPEG is bound to one unique physical file, its exact monolith
and split-Markdown references, byte length, dimensions, SHA-256, and evidence
class.  The native plate is also a *limited manual transcription*: only its
three visible caption statements and three panel counts are recorded.  No
rule glyph, seed, cell array, intermediate configuration, palette, or trace is
transcribed, and no raster-derived transition is replayed.  Thus all ten
assets are HASH_BOUND, only BOOK:2362 is LIMITED_TRANSCRIBED, and none is
PIXEL_REPLAYED.

The source oracle owns the semantic evidence boundary.  This verifier binds
that public image-line interface once it is frozen; it does not use images as
a substitute for the Book's machine-readable Notes expression.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from pathlib import Path
from typing import NamedTuple


if not __debug__:
    raise RuntimeError("T28 asset verification requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "ref/A-New-Kind-of-Science"
BOOK = SOURCE_ROOT / "A-New-Kind-of-Science.md"
SOURCE_ORACLE_PATH = ROOT / "goal-1/39-T28-source-oracle.py"

EXPECTED_BOOK_LINES = 22_498
EXPECTED_BOOK_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_lines(values: set[int] | frozenset[int]) -> str:
    return sha256(",".join(map(str, sorted(values))).encode("ascii"))


book_bytes = BOOK.read_bytes()
assert len(book_bytes.decode("utf-8").splitlines()) == EXPECTED_BOOK_LINES
assert sha256(book_bytes) == EXPECTED_BOOK_SHA256
BOOK_LINES = book_bytes.decode("utf-8").splitlines()
IMAGE_RE = re.compile(r"^!\[\]\(([^)]*?\.jpeg)\)$")
BOOK_IMAGES = {
    line_number: match.group(1)
    for line_number, line in enumerate(BOOK_LINES, 1)
    if (match := IMAGE_RE.fullmatch(line))
}


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
    assembly: str
    boundary: str


CHAPTER3 = "CHAPTERS/3-The-World-of-Simple-Programs"
CHAPTER5 = "CHAPTERS/5-Two-Dimensions-and-Beyond"
CHAPTER11 = "CHAPTERS/11-The-Notion-of-Computation"

ASSETS = {
    1020: AssetSpec(
        "R-1D-CONTEXTUAL-ANALOG",
        "_page_100_Picture_3.jpeg",
        f"{CHAPTER3}/Images/_page_100_Picture_3.jpeg",
        f"{CHAPTER3}/The-World-of-Simple-Programs.md",
        337,
        106_884,
        912,
        614,
        "25df45fbfcb5f0f57d18779b2b8af7cb31c9a9400d81b69779663c448882d183",
        "-",
        "one-dimensional contextual analog only; no 2D patch or boundary semantics",
    ),
    2314: AssetSpec(
        "C-T26-UNIFORM-2D",
        "_page_202_Picture_4.jpeg",
        f"{CHAPTER5}/Images/_page_202_Picture_4.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        171,
        108_556,
        1064,
        578,
        "ec903a3a52824f3a1e97766dca0eebea857e37e42e6ebc1f0525f19e29f2ca5e",
        "-",
        "neighbor-independent aligned T26 predecessor; no contextual choice",
    ),
    2322: AssetSpec(
        "C-T26-GALLERY",
        "_page_203_Figure_2.jpeg",
        f"{CHAPTER5}/Images/_page_203_Figure_2.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        179,
        295_361,
        1141,
        1349,
        "e898fd8f8039ae055dbcbfba6d7128e91e7b1f857f6bd0e994a67d0f454dd2ff",
        "-",
        "neighbor-independent aligned T26 gallery; no contextual choice",
    ),
    2328: AssetSpec(
        "C-T27-ORIENTATION-EVOLUTION",
        "_page_204_Picture_4.jpeg",
        f"{CHAPTER5}/Images/_page_204_Picture_4.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        183,
        87_284,
        1140,
        532,
        "dcf7ff457a600fb1d0f1bcf98a427e4eb54ca8cab5ed9aaf2c3fcdc35220a471",
        "geometric_orientation",
        "off-grid T27 evolution; absence of stable grid neighbors is the control",
    ),
    2330: AssetSpec(
        "C-T27-ORIENTATION-RULE",
        "_page_204_Picture_5.jpeg",
        f"{CHAPTER5}/Images/_page_204_Picture_5.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        185,
        3_127,
        221,
        80,
        "7e04c2b7277c015f960e2d42176562a4d6f79ce0643a360a37cc8cc6ac24d29d",
        "geometric_orientation",
        "rule companion for the off-grid T27 orientation control; glyph unrecovered",
    ),
    2340: AssetSpec(
        "C-T27-OVERLAP-EVOLUTION",
        "_page_205_Picture_1.jpeg",
        f"{CHAPTER5}/Images/_page_205_Picture_1.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        193,
        71_322,
        1094,
        472,
        "2913f51a292f9aa24307696ae4b08817031a292526032bf1b663954437552dbf",
        "geometric_overlap",
        "off-grid T27 overlap evolution; not aligned contextual patch assembly",
    ),
    2344: AssetSpec(
        "C-T27-OVERLAP-RULE",
        "_page_205_Picture_3.jpeg",
        f"{CHAPTER5}/Images/_page_205_Picture_3.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        197,
        3_263,
        217,
        82,
        "5dd9aacee0337c34a929925d189d2558186a6f3728b16828127df61633fc5213",
        "geometric_overlap",
        "rule companion for the off-grid T27 overlap control; glyph unrecovered",
    ),
    2354: AssetSpec(
        "C-T27-GEOMETRIC-GALLERY",
        "_page_206_Picture_1.jpeg",
        f"{CHAPTER5}/Images/_page_206_Picture_1.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        207,
        133_892,
        1094,
        981,
        "c492333aff2709dfd5be91fb551cb6a112cfff0982e351a09ce03f4db86c0759",
        "-",
        "off-grid T27 gallery immediately preceding the gridded-neighbor contrast",
    ),
    2362: AssetSpec(
        "N-T28-CONTEXTUAL-GRID",
        "_page_207_Figure_1.jpeg",
        f"{CHAPTER5}/Images/_page_207_Figure_1.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        213,
        185_670,
        1184,
        1023,
        "e7f0112ebc4a6b4276bffeaccc043855335527d38e638c2ed37c428451d57b1c",
        "-",
        "native T28 plate; limited caption/count transcription only",
    ),
    8026: AssetSpec(
        "R-CA-SINGLETON-OUTPUT",
        "_page_681_Figure_3.jpeg",
        f"{CHAPTER11}/Images/_page_681_Figure_3.jpeg",
        f"{CHAPTER11}/The-Notion-of-Computation.md",
        325,
        116_784,
        880,
        367,
        "66295968a40bcb9140d67e3fba6ec15420849d298afac6ddf6583b5108f9c51a",
        "-",
        "one-dimensional singleton-output CA-emulation relation; not native T28",
    ),
}

NATIVE = frozenset({2362})
RELATION = frozenset({1020, 8026})
CONTROL = frozenset({2314, 2322, 2328, 2330, 2340, 2344, 2354})
GOVERNED = NATIVE | RELATION | CONTROL
assert GOVERNED == frozenset(ASSETS)
assert not (NATIVE & RELATION or NATIVE & CONTROL or RELATION & CONTROL)
assert (len(NATIVE), len(RELATION), len(CONTROL), len(GOVERNED)) == (1, 2, 7, 10)
assert digest_lines(NATIVE) == "9bf42f4b66fe462d800a8b659ec866dca7f23597393f9cb25456d41f5458b590"
assert digest_lines(RELATION) == "ac31f08d2eaed3c8cfd457f9d4922b7fab79508739676c57158d156356528eb2"
assert digest_lines(CONTROL) == "6159ae09901c63d9c720102232de4bbc096433209203024d3750c10068f2f0e9"
assert digest_lines(GOVERNED) == "06e50ad4cf8480aed23443fd40147ac0fb35e0776e1883d025467943c4889411"
ASSEMBLIES = {
    assembly: frozenset(
        line for line, asset in ASSETS.items() if asset.assembly == assembly
    )
    for assembly in {asset.assembly for asset in ASSETS.values()} - {"-"}
}
assert ASSEMBLIES == {
    "geometric_orientation": frozenset({2328, 2330}),
    "geometric_overlap": frozenset({2340, 2344}),
}
assert sum(map(len, ASSEMBLIES.values())) == 4


# These source-adjacent images are deliberately not governed.  Freezing the
# exclusions prevents a radius-based collector from silently pulling a T25
# path, Turing/sequential CA emulations, or three Mandelbrot rasters into T28.
ADJACENCY_EXCLUSIONS = {
    2302: ("_page_201_Figure_4.jpeg", "preceding T25 path observer"),
    8018: ("_page_680_Figure_5.jpeg", "preceding Turing-machine CA emulation"),
    8036: ("_page_682_Figure_2.jpeg", "following sequential-substitution CA emulation"),
    8038: ("_page_682_Figure_3.jpeg", "following sequential-substitution CA emulation"),
    13800: ("_page_950_Picture_3.jpeg", "Mandelbrot raster before the Notes heading"),
    13802: ("_page_950_Picture_4.jpeg", "Mandelbrot raster before the Notes heading"),
    13804: ("_page_950_Figure_5.jpeg", "Mandelbrot raster before the Notes heading"),
}
EXCLUDED = frozenset(ADJACENCY_EXCLUSIONS)
assert GOVERNED.isdisjoint(EXCLUDED)
for excluded_line, (excluded_name, _reason) in ADJACENCY_EXCLUSIONS.items():
    assert BOOK_LINES[excluded_line - 1] == f"![]({excluded_name})"

# The candidate closure is explicit and reproducible: the exact 1D analog;
# every image from the immediately preceding T25 plate through the native T28
# plate; the CA-emulation paragraph with its preceding/following sibling
# plates; and the three images mechanically adjacent to the Notes heading.
# N/R/C plus the seven dispositions above exhaust it with no unresolved line.
CANDIDATE_IMAGE_LINES = frozenset(
    {1020}
    | {line for line in BOOK_IMAGES if 2302 <= line <= 2362}
    | {line for line in BOOK_IMAGES if 8018 <= line <= 8038}
    | {line for line in BOOK_IMAGES if 13800 <= line <= 13806}
)
assert CANDIDATE_IMAGE_LINES == GOVERNED | EXCLUDED
assert len(CANDIDATE_IMAGE_LINES) == 17
assert digest_lines(EXCLUDED) == "8b6cbf265e37d7759d88fad5b1fa99c9814dc40293ea8a350f3a40b21bbd26f7"
assert digest_lines(CANDIDATE_IMAGE_LINES) == (
    "a2767e2fc3594f3aeabe748a5b584a31dc69bad4ca2b6eedcc7d8bec8ac3ea45"
)
CLASSIFICATION = {
    **{line: "N" for line in NATIVE},
    **{line: "R" for line in RELATION},
    **{line: "C" for line in CONTROL},
    **{line: "X" for line in EXCLUDED},
}
assert frozenset(CLASSIFICATION) == CANDIDATE_IMAGE_LINES
assert tuple(CLASSIFICATION.values()).count("N") == 1
assert tuple(CLASSIFICATION.values()).count("R") == 2
assert tuple(CLASSIFICATION.values()).count("C") == 7
assert tuple(CLASSIFICATION.values()).count("X") == 7


# This is a manual reading of text and counts visibly printed inside the exact
# hash-bound raster.  It is intentionally not presented as machine-verified
# OCR.  The executable glyph contents and configurations remain unrecovered.
LIMITED_TRANSCRIPTION = {
    2362: {
        "caption_name": "A two-dimensional neighbor-dependent substitution system.",
        "caption_boundary": "The grid of cells is assumed to wrap around in both its dimensions.",
        "gallery_caption": (
            "Patterns generated by 8 steps of evolution in various "
            "two-dimensional neighbor-dependent substitution systems."
        ),
        "top_steps": "step 1 through step 7 (seven displayed stages)",
        "top_rule_panels": 5,
        "gallery_panels": "(a) through (h) (eight displayed examples)",
    }
}
HASH_BOUND = GOVERNED
TRANSCRIBED = frozenset(LIMITED_TRANSCRIPTION)
PIXEL_REPLAYED: frozenset[int] = frozenset()
assert TRANSCRIBED <= HASH_BOUND
assert not PIXEL_REPLAYED
assert (len(HASH_BOUND), len(TRANSCRIBED), len(PIXEL_REPLAYED)) == (10, 1, 0)

UNRECOVERED_NATIVE_RASTER_CONTENT = frozenset(
    {
        "exact five-glyph rule contents",
        "complete native rule table",
        "native seed array",
        "intermediate cell configurations",
        "exact native trace",
        "gallery rule glyph contents",
        "gallery result cell arrays",
        "palette-to-label mapping",
    }
)
assert len(UNRECOVERED_NATIVE_RASTER_CONTENT) == 8


SOURCE_GUARDS = {
    1018: "rules depend not only on the color of a single element",
    1022: "rightmost element is always dropped",
    2312: "construct two-dimensional substitution systems",
    2316: "each square is replaced by four smaller squares",
    2326: "nothing about this basic process that depends on the squares being arranged",
    2332: "take account of the orientation of that square",
    2342: "squares that overlap",
    2350: "characteristics of other neighboring elements",
    2352: "difficult to define an obvious notion of neighbors",
    2356: "sets up elements on a grid",
    8024: "generalizes to neighbor-dependent substitution systems",
    8028: "highly uniform rules always yielding just one cell",
    13806: "Page 192 · Neighbor-dependent substitution systems",
    13808: "Flatten2D[Partition[list, {2, 2}, 1, -1] /. rule]",
    13810: "arbitrarily large set of different possible neighborhood configurations",
}
for source_line, fragment in SOURCE_GUARDS.items():
    assert fragment in BOOK_LINES[source_line - 1], (source_line, fragment)


def load_source_oracle():
    """Load the source oracle without relying on the caller's cwd."""

    assert SOURCE_ORACLE_PATH.is_file(), "T28 source oracle is not frozen"
    spec = importlib.util.spec_from_file_location("t28_source_oracle", SOURCE_ORACLE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def jpeg_size(data: bytes) -> tuple[int, int]:
    """Read a JPEG SOF marker without depending on an image library."""

    assert data[:2] == b"\xff\xd8"
    sof = {
        0xC0,
        0xC1,
        0xC2,
        0xC3,
        0xC5,
        0xC6,
        0xC7,
        0xC9,
        0xCA,
        0xCB,
        0xCD,
        0xCE,
        0xCF,
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
        segment_size = int.from_bytes(data[offset : offset + 2], "big")
        if marker in sof:
            width = int.from_bytes(data[offset + 5 : offset + 7], "big")
            height = int.from_bytes(data[offset + 3 : offset + 5], "big")
            return width, height
        offset += segment_size
    raise AssertionError("JPEG SOF marker not found")


def verify_source_interface() -> None:
    """Bind the exact image classes exported by the frozen source audit."""

    source = load_source_oracle()
    required = {
        "NATIVE_IMAGE_LINES": NATIVE,
        "RELATION_IMAGE_LINES": RELATION,
        "CONTROL_IMAGE_LINES": CONTROL,
        "GOVERNED_IMAGE_LINES": GOVERNED,
        "EXCLUDED_IMAGE_LINES": EXCLUDED,
        "CANDIDATE_IMAGE_LINES": CANDIDATE_IMAGE_LINES,
        "UNRESOLVED_IMAGE_LINES": frozenset(),
    }
    for attribute, expected in required.items():
        actual = frozenset(getattr(source, attribute))
        assert actual == expected, (attribute, sorted(actual), sorted(expected))


def ledger() -> tuple[str, int, int, int, int]:
    """Verify every asset and return the canonical provenance ledger."""

    split_markdown = sorted(
        path
        for path in SOURCE_ROOT.rglob("*.md")
        if path.resolve() != BOOK.resolve() and path.name != "ANKoS-Atlas.md"
    )
    assert len(split_markdown) == 17

    monolith_by_name: dict[str, list[int]] = {}
    for line_number, reference in BOOK_IMAGES.items():
        monolith_by_name.setdefault(Path(reference).name, []).append(line_number)

    split_by_name: dict[str, list[tuple[Path, int]]] = {}
    split_re = re.compile(r"^!\[\]\((?:Images/)?([^/()]+\.jpeg)\)$")
    for markdown in split_markdown:
        for line_number, line in enumerate(
            markdown.read_text(encoding="utf-8").splitlines(), 1
        ):
            if match := split_re.fullmatch(line):
                split_by_name.setdefault(match.group(1), []).append(
                    (markdown, line_number)
                )

    physical_by_name: dict[str, list[Path]] = {}
    for path in SOURCE_ROOT.rglob("*.jpeg"):
        if path.is_file():
            physical_by_name.setdefault(path.name, []).append(path)

    rows: list[str] = []
    hashes: set[str] = set()
    total_bytes = 0
    monolith_references = 0
    split_references = 0
    for book_line, asset in sorted(ASSETS.items()):
        kind = "N" if book_line in NATIVE else "R" if book_line in RELATION else "C"
        assert BOOK_LINES[book_line - 1] == f"![]({asset.name})"
        assert monolith_by_name.get(asset.name) == [book_line]

        expected_split = SOURCE_ROOT / asset.split_markdown
        split_hits = split_by_name.get(asset.name, [])
        assert split_hits == [(expected_split, asset.split_line)], (book_line, split_hits)

        expected_physical = SOURCE_ROOT / asset.physical
        physical_hits = physical_by_name.get(asset.name, [])
        assert physical_hits == [expected_physical], (book_line, physical_hits)

        data = expected_physical.read_bytes()
        digest = sha256(data)
        assert len(data) == asset.byte_length, (book_line, len(data), asset.byte_length)
        assert jpeg_size(data) == (asset.width, asset.height)
        assert digest == asset.digest, (book_line, digest, asset.digest)
        assert digest not in hashes, (book_line, digest)

        hashes.add(digest)
        total_bytes += len(data)
        monolith_references += 1
        split_references += 1
        rows.append(
            "|".join(
                (
                    str(book_line),
                    kind,
                    asset.role,
                    asset.physical,
                    str(asset.byte_length),
                    str(asset.width),
                    str(asset.height),
                    asset.digest,
                    asset.split_markdown,
                    str(asset.split_line),
                    asset.assembly,
                    asset.boundary,
                )
            )
        )

    payload = "\n".join(rows) + "\n"
    return payload, monolith_references, split_references, len(hashes), total_bytes


EXPECTED_LEDGER_SHA256 = "f68d3637a5f601c2e7b84f3ec4bbaa0630622dc20a3159fcbd6c4602c931044f"
EXPECTED_TRANSCRIPTION_SHA256 = (
    "ff9874f033d1b4bbbaa39bd64a2f4cd39f0e96bddff222d09565e6ff19aeb36c"
)


def main() -> None:
    verify_source_interface()
    payload, monolith_refs, split_refs, hashes, total_bytes = ledger()
    ledger_digest = sha256(payload.encode("utf-8"))
    transcription_payload = json.dumps(
        LIMITED_TRANSCRIPTION, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    transcription_digest = sha256(transcription_payload)
    assert ledger_digest == EXPECTED_LEDGER_SHA256, (
        "ledger",
        ledger_digest,
        EXPECTED_LEDGER_SHA256,
    )
    assert transcription_digest == EXPECTED_TRANSCRIPTION_SHA256, (
        "transcription",
        transcription_digest,
        EXPECTED_TRANSCRIPTION_SHA256,
    )
    assert (monolith_refs, split_refs, hashes, total_bytes) == (10, 10, 10, 1_112_143)
    print(
        "T28 asset oracle: PASS assets=10; classes N/R/C/X=1/2/7/7; "
        "adjacency_exclusions=7; refs=20(monolith=10,split=10); "
        "unique_hashes=10; bytes=1112143; assemblies=2/4_files; "
        "boundary=10_HASH_BOUND/1_LIMITED_TRANSCRIBED/0_PIXEL_REPLAYED; "
        "native_caption/wrap/counts=bound; glyphs/seed/trace=unrecovered; "
        "unresolved=0"
    )


if __name__ == "__main__":
    main()
