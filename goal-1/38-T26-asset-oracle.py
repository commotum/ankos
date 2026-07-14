#!/usr/bin/env python3
"""Fail-closed asset audit for T26 two-dimensional substitution systems.

The source oracle owns the semantic evidence boundary.  This dependent audit
freezes its exact 26-image interface, including three split figures that the
initial interface omitted: the full page-568 comparison, the page-207
neighbor-dependent control, and both halves of the page-623 coordinate/
finite-automaton figure.  Every governed JPEG is bound to its unique physical
file, exact monolith and split references, byte length, dimensions, SHA-256,
evidence class, and assembly membership.

No displayed rule glyph, seed array, intermediate configuration, palette, or
trace is transcribed from pixels, and no raster is replayed.  The exact page-
187 rule, seed, and patch assembly are text-owned source facts.  Page-188
displayed rules and all other raster-only details remain unrecovered.  Thus
all 26 assets are HASH_BOUND, while TRANSCRIBED and PIXEL_REPLAYED are empty.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path
from typing import NamedTuple


if not __debug__:
    raise RuntimeError("T26 asset verification requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "ref/A-New-Kind-of-Science"
BOOK = SOURCE_ROOT / "A-New-Kind-of-Science.md"
SOURCE_ORACLE_PATH = ROOT / "goal-1/38-T26-source-oracle.py"

EXPECTED_BOOK_LINES = 22_498
EXPECTED_BOOK_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_lines(values: set[int] | frozenset[int]) -> str:
    return hashlib.sha256(
        ",".join(map(str, sorted(values))).encode("ascii")
    ).hexdigest()


def load_source_oracle():
    assert SOURCE_ORACLE_PATH.is_file(), "T26 source oracle is not frozen"
    spec = importlib.util.spec_from_file_location("t26_source_oracle", SOURCE_ORACLE_PATH)
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

# A source-oracle edit that preserves a filename but changes its evidence
# class or governing context must stop this dependent audit.
EXPECTED_SOURCE_CONTRACT = {
    "retained": (115, "962eef0254ab18a40c72b64e8127f6356977fc3ff4dd15e29cf9094f502e7413"),
    "native_evidence": (23, "ef70c2761fd15a9c63d9a7c597e18bee94ceeb3cda7c41078f31b2dc44921f74"),
    "relation_evidence": (67, "99cd6cfc9fbf549c65694fcedf58421f0a1f7e14dbf8e1f39a82dda50a219c49"),
    "control_evidence": (25, "34ce5350d22b028c7dbd345bd4655eb971b8be7c0a89581ed95981fe1f9177f7"),
    "native_images": (3, "88c77dedfd94731adae1c3913a93edfea3ad631c7afc976b012c7024d169e83a"),
    "relation_images": (16, "33b72d4db3c3e99d04583d7a7e716ac8d2de973ae8786198a79958812453adf6"),
    "control_images": (7, "25d33c19678ec52a86b371190a08ac42abf01a63ae9831182ba8b006bf108bcd"),
    "governed_images": (26, "9018acedd5ff638608aa2a79feb5059de5b8a671792ab0c8ec501437eea85ee7"),
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
for contract_name, contract_values in SOURCE_SETS.items():
    expected_count, expected_digest = EXPECTED_SOURCE_CONTRACT[contract_name]
    assert len(contract_values) == expected_count, (
        contract_name, len(contract_values), expected_count
    )
    assert digest_lines(contract_values) == expected_digest, (
        contract_name, digest_lines(contract_values), expected_digest
    )


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


CHAPTER5 = "CHAPTERS/5-Two-Dimensions-and-Beyond"
CHAPTER10 = "CHAPTERS/10-Processes-of-Perception-and-Analysis"
SPLIT_NOTES = "BACK-MATTER/Index/Index.md"

ASSETS = {
    2314: AssetSpec(
        "N-STRICT-2X2",
        "_page_202_Picture_4.jpeg",
        f"{CHAPTER5}/Images/_page_202_Picture_4.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        171, 108_556, 1064, 578,
        "ec903a3a52824f3a1e97766dca0eebea857e37e42e6ebc1f0525f19e29f2ca5e",
        "-",
        "strict square-grid plate; exact rule and seed are text-owned; raster trace unrecovered",
    ),
    2322: AssetSpec(
        "N-STRICT-K3-GALLERY",
        "_page_203_Figure_2.jpeg",
        f"{CHAPTER5}/Images/_page_203_Figure_2.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        179, 295_361, 1141, 1349,
        "e898fd8f8039ae055dbcbfba6d7128e91e7b1f857f6bd0e994a67d0f454dd2ff",
        "-",
        "strict square-grid gallery; displayed rule glyphs, seed, and traces not transcribed",
    ),
    2328: AssetSpec(
        "C-GEOMETRIC-ORIENTATION-EVOLUTION",
        "_page_204_Picture_4.jpeg",
        f"{CHAPTER5}/Images/_page_204_Picture_4.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        183, 87_284, 1140, 532,
        "dcf7ff457a600fb1d0f1bcf98a427e4eb54ca8cab5ed9aaf2c3fcdc35220a471",
        "geometric_orientation",
        "off-grid oriented geometric replacement control; not strict T26 orientation semantics",
    ),
    2330: AssetSpec(
        "C-GEOMETRIC-ORIENTATION-RULE",
        "_page_204_Picture_5.jpeg",
        f"{CHAPTER5}/Images/_page_204_Picture_5.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        185, 3_127, 221, 80,
        "7e04c2b7277c015f960e2d42176562a4d6f79ce0643a360a37cc8cc6ac24d29d",
        "geometric_orientation",
        "rule half of oriented geometric control; glyphs not transcribed",
    ),
    2340: AssetSpec(
        "C-GEOMETRIC-OVERLAP-EVOLUTION",
        "_page_205_Picture_1.jpeg",
        f"{CHAPTER5}/Images/_page_205_Picture_1.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        193, 71_322, 1094, 472,
        "2913f51a292f9aa24307696ae4b08817031a292526032bf1b663954437552dbf",
        "geometric_overlap",
        "off-grid overlapping geometric replacement control; not strict patch assembly",
    ),
    2344: AssetSpec(
        "C-GEOMETRIC-OVERLAP-RULE",
        "_page_205_Picture_3.jpeg",
        f"{CHAPTER5}/Images/_page_205_Picture_3.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        197, 3_263, 217, 82,
        "5dd9aacee0337c34a929925d189d2558186a6f3728b16828127df61633fc5213",
        "geometric_overlap",
        "rule half of overlap control; glyphs not transcribed",
    ),
    2354: AssetSpec(
        "C-GEOMETRIC-GALLERY",
        "_page_206_Picture_1.jpeg",
        f"{CHAPTER5}/Images/_page_206_Picture_1.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        207, 133_892, 1094, 981,
        "c492333aff2709dfd5be91fb551cb6a112cfff0982e351a09ce03f4db86c0759",
        "-",
        "off-grid fractal/geometric gallery; not a strict square-patch program",
    ),
    2362: AssetSpec(
        "C-CONTEXTUAL-GRID",
        "_page_207_Figure_1.jpeg",
        f"{CHAPTER5}/Images/_page_207_Figure_1.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md",
        213, 185_670, 1184, 1023,
        "e7f0112ebc4a6b4276bffeaccc043855335527d38e638c2ed37c428451d57b1c",
        "-",
        "neighbor-dependent T28 control; contextual choice and wrap policy are not strict T26",
    ),
    6666: AssetSpec(
        "R-PERCEPTION-COMPARISON-A",
        "_page_568_Picture_2.jpeg",
        f"{CHAPTER10}/Images/_page_568_Picture_2.jpeg",
        f"{CHAPTER10}/Processes-of-Perception-and-Analysis.md",
        79, 36_404, 272, 291,
        "294844205dc6647865ccf7c9e17ffb03564456ed95d8582c46282cfcfab4f315",
        "perception_comparison",
        "repetitive comparison panel in a shared observer figure; not T26 native state",
    ),
    6668: AssetSpec(
        "R-PERCEPTION-COMPARISON-B",
        "_page_568_Picture_3.jpeg",
        f"{CHAPTER10}/Images/_page_568_Picture_3.jpeg",
        f"{CHAPTER10}/Processes-of-Perception-and-Analysis.md",
        81, 25_044, 279, 290,
        "725fe614093c0cdfbfbb3eb5fd0ee61139c823fb14a46f5284b5ed612a951ec8",
        "perception_comparison",
        "nested T26 comparison panel used as an observer, not construction identity",
    ),
    6670: AssetSpec(
        "R-PERCEPTION-COMPARISON-C",
        "_page_568_Picture_4.jpeg",
        f"{CHAPTER10}/Images/_page_568_Picture_4.jpeg",
        f"{CHAPTER10}/Processes-of-Perception-and-Analysis.md",
        83, 36_370, 275, 298,
        "394ad070bda95f50d42e1a530158245c0d1c1ca58ab3c9f80fa7876012d5829d",
        "perception_comparison",
        "random-looking comparison panel in a shared observer figure; not stochastic T26",
    ),
    6840: AssetSpec(
        "R-RECURSIVE-SUBDIVISION",
        "_page_583_Figure_2.jpeg",
        f"{CHAPTER10}/Images/_page_583_Figure_2.jpeg",
        f"{CHAPTER10}/Processes-of-Perception-and-Analysis.md",
        253, 194_507, 1110, 894,
        "e5f2a52133f632cf93a188df668d7148999c8b664a698607dd6e9f8b1df4ebf5",
        "-",
        "adaptive recursive-subdivision encoding relation; not uniform strict replacement",
    ),
    6982: AssetSpec(
        "R-NESTING-PERCEPTION-GALLERY",
        "_page_598_Figure_2.jpeg",
        f"{CHAPTER10}/Images/_page_598_Figure_2.jpeg",
        f"{CHAPTER10}/Processes-of-Perception-and-Analysis.md",
        395, 251_707, 1169, 694,
        "f5bc4bb286bf303dfd249053941a86aa4c6e6c08403b5f67cfa4f29db587c380",
        "-",
        "nested-pattern perception/encoding gallery; displayed rules remain raster-only",
    ),
    7284: AssetSpec(
        "R-COORDINATE-AUTOMATON-PATTERN",
        "_page_623_Picture_1.jpeg",
        f"{CHAPTER10}/Images/_page_623_Picture_1.jpeg",
        f"{CHAPTER10}/Processes-of-Perception-and-Analysis.md",
        693, 37_741, 289, 858,
        "6b32debc0a3ae9ce898ac103f882137cce41c2ad91330e6dc92a6cc21849c618",
        "coordinate_automaton",
        "coordinate-digit pattern half; evaluator relation, not UPDATE state",
    ),
    7306: AssetSpec(
        "R-COORDINATE-AUTOMATON-MACHINE",
        "_page_623_Picture_3.jpeg",
        f"{CHAPTER10}/Images/_page_623_Picture_3.jpeg",
        f"{CHAPTER10}/Processes-of-Perception-and-Analysis.md",
        695, 7_901, 314, 169,
        "46077b731213938dc4838ff79baf87410e6ef521e586b77f99596300f7b61a1b",
        "coordinate_automaton",
        "finite-automaton half; coordinate evaluator relation, not transition machinery",
    ),
    7320: AssetSpec(
        "R-COORDINATE-AUTOMATON-GALLERY",
        "_page_624_Figure_3.jpeg",
        f"{CHAPTER10}/Images/_page_624_Figure_3.jpeg",
        f"{CHAPTER10}/Processes-of-Perception-and-Analysis.md",
        703, 208_974, 1186, 1029,
        "ac4c0b912be1c737915abc8497a3c8a2a5878bfd5140cf1066df4b1efdccbef7",
        "-",
        "coordinate-evaluator gallery; automata are analyzers, not hidden T26 control",
    ),
    13724: AssetSpec(
        "N-NONWHITE-BACKGROUND",
        "_page_947_Figure_4.jpeg",
        "BACK-MATTER/Index/Images/_page_947_Figure_4.jpeg",
        SPLIT_NOTES,
        1625, 38_464, 570, 313,
        "e9087bc89be51f34a192a2a0431c87ee3d8f73665274a14502d3da2e56f6d0ae",
        "-",
        "native background variant; displayed rules and traces not transcribed",
    ),
    13742: AssetSpec(
        "R-OTHER-SHAPES",
        "_page_947_Picture_10.jpeg",
        "BACK-MATTER/Index/Images/_page_947_Picture_10.jpeg",
        SPLIT_NOTES,
        1643, 18_968, 574, 243,
        "e584cf7dc88c04282641904275cf4c977f712dfd8840b1c0f9116e2ee99560a5",
        "-",
        "other-shape subdivision/equal-square encoding relation; not strict geometry",
    ),
    13748: AssetSpec(
        "R-PENROSE",
        "_page_947_Picture_14.jpeg",
        "BACK-MATTER/Index/Images/_page_947_Picture_14.jpeg",
        SPLIT_NOTES,
        1649, 36_386, 568, 398,
        "05d21731abacb2cd5dec383baa0f87af165b7b638ccb2aa32a1645e27702ddf5",
        "-",
        "Penrose triangle-subdivision relation; not strict square-grid support",
    ),
    13772: AssetSpec(
        "C-GEOMETRIC-3D-VIEW",
        "_page_948_Picture_8.jpeg",
        "BACK-MATTER/Index/Images/_page_948_Picture_8.jpeg",
        SPLIT_NOTES,
        1673, 28_225, 578, 202,
        "c6bd6e27e13a7c638f38d493fe4172ad030c845731937881cd5b58bac70b8696",
        "-",
        "3D visualization of geometric T27 evolutions; observer is not T26 state",
    ),
    14111: AssetSpec(
        "R-CONSTRAINT-FORCED-NESTING",
        "_page_957_Picture_14.jpeg",
        "BACK-MATTER/Index/Images/_page_957_Picture_14.jpeg",
        SPLIT_NOTES,
        2012, 11_244, 560, 84,
        "957c224462a36129efb03f2413788e4bc4a4f0606372f27dc67ca1df05b87b35",
        "-",
        "nested-pattern input to a constraint construction; not T26 constraint semantics",
    ),
    17303: AssetSpec(
        "R-WALSH-KRONECKER-1",
        "_page_1088_Picture_11.jpeg",
        "BACK-MATTER/Index/Images/_page_1088_Picture_11.jpeg",
        SPLIT_NOTES,
        5204, 1_939, 119, 123,
        "017cf1f693abcafb18613cc6ba9bb407222be911860115b2af25514094ec5031",
        "walsh_kronecker",
        "first Walsh/Kronecker relation panel; not native program identity",
    ),
    17305: AssetSpec(
        "R-WALSH-KRONECKER-2",
        "_page_1088_Picture_12.jpeg",
        "BACK-MATTER/Index/Images/_page_1088_Picture_12.jpeg",
        SPLIT_NOTES,
        5206, 2_716, 101, 116,
        "b8f0b29932b58cb1b6d71d89beae90ffefc67ed6da065aee5d280ac8776a45a7",
        "walsh_kronecker",
        "second Walsh/Kronecker relation panel; not native program identity",
    ),
    17307: AssetSpec(
        "R-WALSH-KRONECKER-3",
        "_page_1088_Picture_13.jpeg",
        "BACK-MATTER/Index/Images/_page_1088_Picture_13.jpeg",
        SPLIT_NOTES,
        5208, 3_244, 107, 123,
        "27a4888b42f1f3dbfe5bc5db7156da4e37ea931e30407aab6fe5eee333e60dd0",
        "walsh_kronecker",
        "third Walsh/Kronecker relation panel; not native program identity",
    ),
    17309: AssetSpec(
        "R-WALSH-KRONECKER-4",
        "_page_1088_Picture_14.jpeg",
        "BACK-MATTER/Index/Images/_page_1088_Picture_14.jpeg",
        SPLIT_NOTES,
        5210, 4_859, 103, 109,
        "06f0d2770eda8de96ffa840246255508ab8f3c42190f7cc8302c5e13a1c68f7d",
        "walsh_kronecker",
        "fourth Walsh/Kronecker relation panel; not native program identity",
    ),
    17311: AssetSpec(
        "R-WALSH-KRONECKER-5",
        "_page_1088_Picture_15.jpeg",
        "BACK-MATTER/Index/Images/_page_1088_Picture_15.jpeg",
        SPLIT_NOTES,
        5212, 5_313, 101, 106,
        "43b14aa76ce606f36bd331f3087fcee23d450d8043a0b293feb7c0b7eed11b5b",
        "walsh_kronecker",
        "fifth Walsh/Kronecker relation panel; not native program identity",
    ),
}


STRICT_GRID_NATIVE = {2314, 2322}
NONWHITE_NATIVE = {13724}
PERCEPTION_ASSEMBLY = {6666, 6668, 6670}
RECURSIVE_SUBDIVISION = {6840}
NESTING_OBSERVER = {6982}
COORDINATE_ASSEMBLY = {7284, 7306}
COORDINATE_GALLERY = {7320}
OTHER_SHAPE = {13742}
PENROSE = {13748}
CONSTRAINT_RELATION = {14111}
WALSH_ASSEMBLY = {17303, 17305, 17307, 17309, 17311}
GEOMETRIC_ORIENTATION_ASSEMBLY = {2328, 2330}
GEOMETRIC_OVERLAP_ASSEMBLY = {2340, 2344}
GEOMETRIC_GALLERY = {2354}
CONTEXTUAL_GRID = {2362}
GEOMETRIC_3D_OBSERVER = {13772}

assert NATIVE == STRICT_GRID_NATIVE | NONWHITE_NATIVE
assert RELATION == (
    PERCEPTION_ASSEMBLY | RECURSIVE_SUBDIVISION | NESTING_OBSERVER
    | COORDINATE_ASSEMBLY | COORDINATE_GALLERY | OTHER_SHAPE | PENROSE
    | CONSTRAINT_RELATION | WALSH_ASSEMBLY
)
assert CONTROL == (
    GEOMETRIC_ORIENTATION_ASSEMBLY | GEOMETRIC_OVERLAP_ASSEMBLY
    | GEOMETRIC_GALLERY | CONTEXTUAL_GRID | GEOMETRIC_3D_OBSERVER
)
assert NATIVE.isdisjoint(RELATION | CONTROL)
assert RELATION.isdisjoint(CONTROL)
assert NATIVE | RELATION | CONTROL == GOVERNED == set(ASSETS)


ASSEMBLIES = {
    "geometric_orientation": GEOMETRIC_ORIENTATION_ASSEMBLY,
    "geometric_overlap": GEOMETRIC_OVERLAP_ASSEMBLY,
    "perception_comparison": PERCEPTION_ASSEMBLY,
    "coordinate_automaton": COORDINATE_ASSEMBLY,
    "walsh_kronecker": WALSH_ASSEMBLY,
}
assert sum(map(len, ASSEMBLIES.values())) == len(set().union(*ASSEMBLIES.values()))
assert all(len(lines) >= 2 for lines in ASSEMBLIES.values())
assert all(
    ASSETS[line].assembly == assembly
    for assembly, assembly_lines in ASSEMBLIES.items()
    for line in assembly_lines
)
assert all(
    spec.assembly == "-" or book_line in ASSEMBLIES[spec.assembly]
    for book_line, spec in ASSETS.items()
)


IMAGE_RE = SOURCE.IMAGE_RE
BOOK_IMAGES = {
    line_number: match.group(1)
    for line_number, line in enumerate(BOOK_LINES, 1)
    if (match := IMAGE_RE.fullmatch(line)) and match.group(1).endswith(".jpeg")
}
assert set(BOOK_IMAGES) & RETAINED == GOVERNED

# Fixed-radius saturation catches split assemblies without re-governing every
# inherited or merely adjacent picture.  The three inherited Chapter 3
# substitution plates are deliberately left to T13, just as preceding Turing
# plates remain outside T26.  Every non-governed image within ten physical
# lines of retained T26 evidence is named exactly once here.
NEARBY_EXCLUDED_CLASS = {
    "preceding_turing": {972, 974, 976},
    "inherited_1d_substitution": {988, 990, 998},
    "preceding_t25": {2298, 2302, 13674},
    "unrelated_encoding": {6830, 6846, 6852},
    "other_perception_observers": {6974, 6994},
    "fractal_dimension_observer": {13780},
    "julia_mandelbrot_observers": {13790, 13794, 13800, 13802, 13804},
    "constraint_ca_control": {14117},
    "walsh_basis_controls": {17287, 17289, 17291},
}
NEARBY_EXCLUDED = set().union(*NEARBY_EXCLUDED_CLASS.values())
assert sum(map(len, NEARBY_EXCLUDED_CLASS.values())) == len(NEARBY_EXCLUDED) == 24
assert not NEARBY_EXCLUDED & GOVERNED
NEARBY_CANDIDATES = {
    image_line
    for image_line in BOOK_IMAGES
    if min(abs(image_line - source_line) for source_line in RETAINED) <= 10
}
assert NEARBY_CANDIDATES == GOVERNED | NEARBY_EXCLUDED
assert len(NEARBY_CANDIDATES) == 50
assert digest_lines(NEARBY_CANDIDATES) == (
    "3a53ccedfffc5567db32e08b22727f9a11f97a1bc257d9eb62f11d674d39b74b"
)
assert digest_lines(NEARBY_EXCLUDED) == (
    "e1473927d57185611743238182c78fcb9ad89f2eb2eda1c5329505fe71fb53bc"
)


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


def markdown_reference_index() -> dict[str, set[tuple[str, int]]]:
    index: dict[str, set[tuple[str, int]]] = {}
    for markdown in SOURCE_ROOT.rglob("*.md"):
        relative = markdown.relative_to(SOURCE_ROOT).as_posix()
        for line_number, line in enumerate(
            markdown.read_text(encoding="utf-8").splitlines(), 1
        ):
            match = MARKDOWN_IMAGE_RE.fullmatch(line)
            if match:
                index.setdefault(Path(match.group(1)).name, set()).add(
                    (relative, line_number)
                )
    return index


def asset_ledger() -> tuple[str, int, int, int]:
    rows: list[str] = []
    hashes: set[str] = set()
    total_bytes = 0
    total_references = 0
    reference_index = markdown_reference_index()
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
        assert actual_digest not in hashes, ("exact duplicate", book_line, actual_digest)
        hashes.add(actual_digest)
        total_bytes += len(data)

        expected_references = {
            ("A-New-Kind-of-Science.md", book_line),
            (spec.split_markdown, spec.split_line),
        }
        actual_references = reference_index.get(spec.name, set())
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
            f"{spec.split_markdown}|{spec.split_line}|{spec.assembly}|{spec.boundary}"
        )
    return "\n".join(rows) + "\n", total_bytes, total_references, len(hashes)


# These guards classify source-owned facts and multi-file boundaries.  They
# are not transcriptions from the JPEGs.
SOURCE_TEXT_GUARDS = {
    2316: "each square is replaced by four smaller squares at every step",
    2332: "take account of the orientation of that square",
    2334: "possible for the squares produced to overlap",
    2342: "simple geometrical rule shown on the right",
    2356: "sets up elements on a grid it is straightforward to allow the replacements",
    2364: "this in effect reduces one to dealing with a one-dimensional system",
    6672: "Pictures exhibiting different degrees of apparent randomness",
    6676: "nested structure of picture (b)",
    6842: "generalization of a two-dimensional substitution system",
    6984: "two-dimensional pointer-based encoding scheme",
    7312: "finite automaton at the bottom right",
    7322: "feeding the digit sequences of its y and x coordinates",
    13683: "initial condition such as {{1}}",
    13692: "finite automaton from the digit sequences",
    13722: "Non-white backgrounds",
    13740: "subdividing other geometrical figures",
    13744: "starting from initial condition {{3}}",
    13746: "Penrose tilings",
    13770: "3D pictures below show successive steps",
    14109: "only 51 of the 65,536 possible 2×2 blocks",
    17297: "evolution of a 2D substitution system, or equivalently from a Kronecker product",
}
for source_line, fragment in SOURCE_TEXT_GUARDS.items():
    assert fragment in BOOK_LINES[source_line - 1], (source_line, fragment)

MIXED_PATCH_RULE_FRAGMENTS = (
    "3 \\rightarrow \\{\\{1, 0\\}, \\{3, 2\\}\\}",
    "2 \\rightarrow \\{\\{1\\}, \\{3\\}\\}",
    "1 \\rightarrow \\{\\{3, 2\\}\\}",
    "0 \\rightarrow \\{\\{3\\}\\}",
    "starting from initial condition {{3}}",
)
assert all(
    fragment in BOOK_LINES[13744 - 1]
    for fragment in MIXED_PATCH_RULE_FRAGMENTS
)
assert {13683, 13744} <= set(SOURCE.NATIVE_EVIDENCE)
assert {13692, 13695, 13696, 13699} <= set(SOURCE.RELATION_EVIDENCE)
assert not ({13692, 13695, 13696, 13699} & set(SOURCE.NATIVE_EVIDENCE))
assert {2332, 2334, 2342, 2356, 2364, 13770} <= set(SOURCE.CONTROL_EVIDENCE)
assert {
    6676, 6842, 6984, 7312, 7322, 13740, 13746, 14109, 17297
} <= set(SOURCE.RELATION_EVIDENCE)
assert SOURCE.OTHER_SHAPES_ENCODED_ROWS == (
    (0, ((3,),)),
    (1, ((3, 2),)),
    (2, ((1,), (3,))),
    (3, ((1, 0), (3, 2))),
)
assert SOURCE.OTHER_SHAPES_ENCODED_SEED == ((3,),)
mixed_trace = [SOURCE.OTHER_SHAPES_ENCODED_SEED]
for _ in range(len(SOURCE.OTHER_SHAPES_EXPECTED_SHAPES) - 1):
    mixed_trace.append(
        SOURCE.expand_compatible_mosaic(
            mixed_trace[-1],
            dict(SOURCE.OTHER_SHAPES_ENCODED_ROWS),
        )
    )
assert tuple((len(grid), len(grid[0])) for grid in mixed_trace) == (
    SOURCE.OTHER_SHAPES_EXPECTED_SHAPES
)
assert 13742 in SOURCE.RELATION_IMAGE_LINES
assert 13742 in SOURCE.RELATION_EVIDENCE
assert 13742 not in SOURCE.NATIVE_IMAGE_LINES


HASH_BOUND_ASSETS = set(ASSETS)
TRANSCRIBED_ASSETS: set[int] = set()
PIXEL_REPLAYED_ASSETS: set[int] = set()
assert HASH_BOUND_ASSETS == GOVERNED
assert not TRANSCRIBED_ASSETS
assert not PIXEL_REPLAYED_ASSETS

# These raster facts are deliberately not claimed by this audit.
UNRECOVERED_NATIVE_RASTER_FACTS = {
    2314: ("displayed_intermediate_arrays", "renderer", "pixel_trace"),
    2322: ("displayed_rule_tables", "seed_pixels", "panel_traces", "renderer"),
    13724: ("displayed_rule_tables", "seed_pixels", "panel_traces", "renderer"),
}
assert set(UNRECOVERED_NATIVE_RASTER_FACTS) == NATIVE


EXPECTED_TOTAL_BYTES = 1_838_481
EXPECTED_REFERENCE_COUNT = 52
EXPECTED_UNIQUE_HASHES = 26
EXPECTED_LEDGER_SHA256 = "6efdf22fdacd0bc9c9b5f59ef61e56c29cdbb9d76624dad5c088c8aed0e17beb"


def main() -> None:
    ledger, total_bytes, reference_count, unique_hashes = asset_ledger()
    ledger_digest = sha256(ledger.encode("utf-8"))
    assert ledger_digest == EXPECTED_LEDGER_SHA256, (
        ledger_digest, EXPECTED_LEDGER_SHA256
    )
    assert total_bytes == EXPECTED_TOTAL_BYTES, total_bytes
    assert reference_count == EXPECTED_REFERENCE_COUNT, reference_count
    assert unique_hashes == EXPECTED_UNIQUE_HASHES, unique_hashes

    print(
        "T26 asset oracle: PASS governed=26; source native/relation/control=3/16/7; "
        "strict_native=2; nonwhite_native=1; assemblies=5/14_files; "
        "fixed_radius_candidates=50; nearby_excluded=24; "
        "refs=52; unique_files=26; unique_hashes=26; "
        f"bytes={total_bytes}; HASH_BOUND=26; TRANSCRIBED=0; PIXEL_REPLAYED=0; "
        "source_contract/monolith/split/hash/dimensions/classification=PASS; "
        "displayed_rules/seeds/traces=NOT_RECOVERED; exact_duplicates=0; unresolved=0"
    )


if __name__ == "__main__":
    main()
