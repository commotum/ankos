#!/usr/bin/env python3
"""Frozen T24 higher-dimensional/fixed-incidence CA asset closure.

The governed plates show dimensional arrangements, hexagonal-lattice growth,
alternative nearest-neighbor lattices, congruent pentagonal cells, and a
nonrepetitive Penrose support.  Related Penrose/Voronoi plates explain how a
support can be obtained; sequential-network plates are controls for a
different schedule and structural update.  None of these rasters is a native
serialization of coordinates, incidence, a seed, a rule table, or a trace.

Every candidate raster is hash-bound through its monolith reference, its split
corpus reference, and its unique physical JPEG.  Human transcriptions are
limited to metadata stated by nearby retained source text.  In particular, a
visible tiling or graph never authorizes reconstruction of complete topology,
and no displayed evolution is replayed from pixels.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path


if not __debug__:
    raise RuntimeError("T24 asset verification requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "ref/A-New-Kind-of-Science"
BOOK = ASSET_ROOT / "A-New-Kind-of-Science.md"
SOURCE_ORACLE_PATH = ROOT / "goal-1/36-T24-source-oracle.py"

EXPECTED_BOOK_LINES = 22_498
EXPECTED_BOOK_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"

book_bytes = BOOK.read_bytes()
assert hashlib.sha256(book_bytes).hexdigest() == EXPECTED_BOOK_SHA256
lines = book_bytes.decode("utf-8").splitlines()
assert len(lines) == EXPECTED_BOOK_LINES


def digest_set(values: set[int] | frozenset[int]) -> str:
    return hashlib.sha256(",".join(map(str, sorted(values))).encode("ascii")).hexdigest()


def load_source_oracle():
    assert SOURCE_ORACLE_PATH.is_file(), "T24 source oracle is not frozen yet"
    spec = importlib.util.spec_from_file_location("t24_source_oracle", SOURCE_ORACLE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SOURCE = load_source_oracle()
S = set(SOURCE.RETAINED)
NATIVE = set(SOURCE.NATIVE_IMAGE_LINES)
RELATION = set(SOURCE.RELATION_IMAGE_LINES)
CONTROL = set(SOURCE.CONTROL_IMAGE_LINES)
GOVERNED = set(SOURCE.GOVERNED_IMAGE_LINES)

# Filled from the source oracle's final public contract.  These values make a
# changed evidence partition fail before the asset universe can silently move.
EXPECTED_SOURCE_COUNT = 145
EXPECTED_SOURCE_DIGEST = "52c5ea5e4964df3ec11e3c2994691a4fb9eda6b0ee9ce61a5ea91f87d7df37fa"
EXPECTED_NATIVE_SOURCE_COUNT = 80
EXPECTED_NATIVE_SOURCE_DIGEST = "1c7fa838bfa3e42073f8f8b7f8dfe2647a16a188f515063421892fb7255df2c3"
EXPECTED_RELATION_SOURCE_COUNT = 16
EXPECTED_RELATION_SOURCE_DIGEST = "d74e8224571c62fff7eb6ed75171a60a0be1a19c299dc9fe8a83bd9f4942585b"
EXPECTED_CONTROL_SOURCE_COUNT = 49
EXPECTED_CONTROL_SOURCE_DIGEST = "eaaa54ac9aa56764b6b86260be2c0d978067d24db4c17884fad1632b784bff99"
EXPECTED_GOVERNED_COUNT = 11
EXPECTED_GOVERNED_DIGEST = "07b740cf80d9e0caef2500ebb6882c4322a6969b9fc284e3e77af4b9a611b62d"
EXPECTED_NATIVE_IMAGE_DIGEST = "e6b89d89fdb76ba4bb76560fcbcd6dd0f22169301ab98bc8017e8bf0571b085f"
EXPECTED_RELATION_IMAGE_DIGEST = "97cdd4f0b5c022cd17993d343b86304469fd691b53f5e5d6d3d8dad5b003b5c8"
EXPECTED_CONTROL_IMAGE_DIGEST = "5748688fa018e741a32f21c25a0b5935985b6c17f924575daf80fcfe2ce258c1"

assert len(S) == EXPECTED_SOURCE_COUNT
assert SOURCE.digest(SOURCE.RETAINED) == EXPECTED_SOURCE_DIGEST
assert len(SOURCE.NATIVE_EVIDENCE) == EXPECTED_NATIVE_SOURCE_COUNT
assert SOURCE.digest(SOURCE.NATIVE_EVIDENCE) == EXPECTED_NATIVE_SOURCE_DIGEST
assert len(SOURCE.RELATION_EVIDENCE) == EXPECTED_RELATION_SOURCE_COUNT
assert SOURCE.digest(SOURCE.RELATION_EVIDENCE) == EXPECTED_RELATION_SOURCE_DIGEST
assert len(SOURCE.CONTROL_EVIDENCE) == EXPECTED_CONTROL_SOURCE_COUNT
assert SOURCE.digest(SOURCE.CONTROL_EVIDENCE) == EXPECTED_CONTROL_SOURCE_DIGEST
assert len(GOVERNED) == EXPECTED_GOVERNED_COUNT
assert SOURCE.digest(SOURCE.GOVERNED_IMAGE_LINES) == EXPECTED_GOVERNED_DIGEST
assert SOURCE.digest(SOURCE.NATIVE_IMAGE_LINES) == EXPECTED_NATIVE_IMAGE_DIGEST
assert SOURCE.digest(SOURCE.RELATION_IMAGE_LINES) == EXPECTED_RELATION_IMAGE_DIGEST
assert SOURCE.digest(SOURCE.CONTROL_IMAGE_LINES) == EXPECTED_CONTROL_IMAGE_DIGEST


image_re = SOURCE.IMAGE_RE
images = {
    line_number: match.group(1)
    for line_number, line in enumerate(lines, 1)
    if (match := image_re.fullmatch(line)) and match.group(1).endswith(".jpeg")
}


def near(source_lines: set[int], radius: int = 4) -> set[int]:
    """One nonrecursive source-proximity pass over monolith image lines."""

    assert source_lines and radius >= 0
    return {
        line_number
        for line_number in images
        if min(abs(line_number - source) for source in source_lines) <= radius
    }


def jpeg_size(data: bytes) -> tuple[int, int]:
    """Read JPEG dimensions without adding an image-library dependency."""

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


def physical_image(book_line: int) -> Path:
    name = Path(images[book_line]).name
    hits = [path for path in ASSET_ROOT.rglob(name) if path.is_file()]
    assert len(hits) == 1, (book_line, name, hits)
    return hits[0]


def _ledger(
    asset_lines: set[int],
    kind_for,
    reasons: dict[int, str],
) -> tuple[str, int, int, int]:
    """Return exact monolith/split/physical metadata for ``asset_lines``."""

    assert asset_lines and set(reasons) == asset_lines
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
    for book_line in sorted(asset_lines):
        kind = kind_for(book_line)
        name = Path(images[book_line]).name
        monolith_hits = monolith_by_name.get(name, [])
        split_hits = split_by_name.get(name, [])
        physical_hits = physical_by_name.get(name, [])
        assert monolith_hits == [book_line], (book_line, monolith_hits)
        assert len(split_hits) == 1, (book_line, split_hits)
        assert len(physical_hits) == 1, (book_line, physical_hits)
        monolith_references += 1
        split_references += 1

        path = physical_hits[0]
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        assert digest not in hashes, (book_line, digest)
        hashes.add(digest)
        width, height = jpeg_size(data)
        split_path, split_line = split_hits[0]
        rows.append(
            f"{book_line}|{kind}|{images[book_line]}|"
            f"{path.relative_to(ASSET_ROOT).as_posix()}|{len(data)}|"
            f"{width}|{height}|{digest}|"
            f"{split_path.relative_to(ASSET_ROOT).as_posix()}|{split_line}|{reasons[book_line]}"
        )

    return "\n".join(rows) + "\n", monolith_references, split_references, len(hashes)


# The governed sets are supplied by the independent source audit.  They are
# semantic ownership, unlike the radius-four candidate collection below.
N_DIMENSION = {2154}
N_HEX_ANY = {4412}
N_HEX_EXACT1 = {4428}
N_LATTICES = {13648}
N_PENTAGON = {13652}
N_PENROSE = {13656}
R_PENROSE_GENERATOR = {13748}
R_VORONOI = {15487}
C_SEQUENTIAL_NETWORK = {13891, 13893, 13895}

native_classes = (
    N_DIMENSION,
    N_HEX_ANY,
    N_HEX_EXACT1,
    N_LATTICES,
    N_PENTAGON,
    N_PENROSE,
)
relation_classes = (R_PENROSE_GENERATOR, R_VORONOI)
control_classes = (C_SEQUENTIAL_NETWORK,)
all_governed_classes = native_classes + relation_classes + control_classes
assert all(
    not (left & right)
    for i, left in enumerate(all_governed_classes)
    for right in all_governed_classes[i + 1 :]
)
assert set().union(*native_classes) == NATIVE
assert set().union(*relation_classes) == RELATION
assert set().union(*control_classes) == CONTROL
assert NATIVE | RELATION | CONTROL == GOVERNED
assert (len(NATIVE), len(RELATION), len(CONTROL), len(GOVERNED)) == (6, 2, 3, 11)
assert set(images) & S == GOVERNED


# C4 is one declared, nonrecursive radius-four pass around the complete retained
# source partition.  An image reached by the pass never becomes a new center.
C4 = near(S)
ADJACENCY_ONLY = C4 - GOVERNED
assert GOVERNED <= C4
assert len(C4) == 22
assert len(ADJACENCY_ONLY) == 11

ADJ_STRUCTURAL_NETWORK = {2422, 2430}
ADJ_NATURAL_OBSERVER = {4418}
ADJ_OTHER_CA = {10259, 13312, 13638, 13640}
ADJ_SUBSTITUTION = {13742}
ADJ_NETWORK_OBSERVER = {13907}
ADJ_STATIC_GEOMETRY = {15479}
ADJ_SEQUENTIAL_CA = {16450}
adjacency_classes = (
    ADJ_STRUCTURAL_NETWORK,
    ADJ_NATURAL_OBSERVER,
    ADJ_OTHER_CA,
    ADJ_SUBSTITUTION,
    ADJ_NETWORK_OBSERVER,
    ADJ_STATIC_GEOMETRY,
    ADJ_SEQUENTIAL_CA,
)
assert all(
    not (left & right)
    for i, left in enumerate(adjacency_classes)
    for right in adjacency_classes[i + 1 :]
)
assert set().union(*adjacency_classes) == ADJACENCY_ONLY
assert tuple(map(len, adjacency_classes)) == (2, 1, 4, 1, 1, 1, 1)


GOVERNING_SOURCE_LINES = {
    2154: (2156,),
    4412: (4410, 4414, 15608, 15610, 15612),
    4428: (4422, 4424, 4430, 15608, 15610, 15612),
    13648: (13642, 13644, 13646),
    13652: (13650,),
    13656: (13654,),
    13748: (13746, 13748, 13754),
    13891: (13889, 13891),
    13893: (13889, 13893),
    13895: (13889, 13895),
    15487: (15485, 15487),
}
assert set(GOVERNING_SOURCE_LINES) == GOVERNED
assert all(set(source_lines) <= S for source_lines in GOVERNING_SOURCE_LINES.values())

GOVERNED_REASON = {
    2154: "one/two/three-dimensional arrangement plate; examples, not a support serialization",
    4412: "page-369 hex-grid crystal-growth plate; source rule code 16382",
    4428: "page-371 hex-grid inhibited-growth plate; source rule code 10926",
    13648: "alternative nearest-neighbor lattice/Voronoi-cell shape plate",
    13652: "congruent pentagonal-cell CA plate; first source rule code 4094",
    13656: "nested nonrepetitive Penrose-support CA plate; first source rule code 254",
    13748: "Penrose tiling construction relation; not the T24 CA transition",
    13891: "single-active-node sequential network control, first governed plate",
    13893: "single-active-node sequential network control, second governed plate",
    13895: "single-active-node sequential network control, third governed plate",
    15487: "Voronoi geometry relation; not a T24 configuration or evolution",
}
assert set(GOVERNED_REASON) == GOVERNED
GOVERNED_LEDGER_REASON = {
    book_line: (
        f"{GOVERNED_REASON[book_line]}; "
        f"source={','.join(map(str, GOVERNING_SOURCE_LINES[book_line]))}"
    )
    for book_line in GOVERNED
}


ADJACENCY_REASON = {
    2422: "structural-network snapshot preceding topology-rerouting mechanics",
    2430: "network-layout observer; drawing position is not native dimensional support",
    4418: "photographs of natural snowflakes, not CA configuration data",
    10259: "unrelated two-dimensional additive self-reproduction CA plate",
    13312: "continuous-value additive CA relation from the Notes",
    13638: "T23 exact-three-of-26 depth-shaded projection",
    13640: "T23 exact-three-of-26 depth-shaded projection",
    13742: "other-shape substitution-system plate, not fixed-incidence CA evolution",
    13907: "dimensionality plot for structural network systems, not a fixed-network CA trace",
    15479: "static discrete circle-packing constraint plate with no CA step",
    16450: "sequential-cell-update CA control with new-value reads",
}
assert set(ADJACENCY_REASON) == ADJACENCY_ONLY


def nearest_retained(book_line: int) -> tuple[int, ...]:
    distance = min(abs(book_line - source_line) for source_line in S)
    assert distance <= 4
    return tuple(sorted(source_line for source_line in S if abs(book_line - source_line) == distance))


ADJACENCY_LEDGER_REASON = {
    book_line: (
        f"{ADJACENCY_REASON[book_line]}; "
        f"nearest_retained={','.join(map(str, nearest_retained(book_line)))}"
    )
    for book_line in ADJACENCY_ONLY
}


def governed_kind(book_line: int) -> str:
    return (
        "N-DIMENSION" if book_line in N_DIMENSION else
        "N-HEX-ANY" if book_line in N_HEX_ANY else
        "N-HEX-EXACT1" if book_line in N_HEX_EXACT1 else
        "N-LATTICES" if book_line in N_LATTICES else
        "N-PENTAGON" if book_line in N_PENTAGON else
        "N-PENROSE" if book_line in N_PENROSE else
        "R-PENROSE-GENERATOR" if book_line in R_PENROSE_GENERATOR else
        "R-VORONOI" if book_line in R_VORONOI else
        "C-SEQUENTIAL-NETWORK"
    )


def adjacency_kind(book_line: int) -> str:
    return (
        "A-STRUCTURAL-NETWORK" if book_line in ADJ_STRUCTURAL_NETWORK else
        "A-NATURAL-OBSERVER" if book_line in ADJ_NATURAL_OBSERVER else
        "A-OTHER-CA" if book_line in ADJ_OTHER_CA else
        "A-SUBSTITUTION" if book_line in ADJ_SUBSTITUTION else
        "A-NETWORK-OBSERVER" if book_line in ADJ_NETWORK_OBSERVER else
        "A-STATIC-GEOMETRY" if book_line in ADJ_STATIC_GEOMETRY else
        "A-SEQUENTIAL-CA"
    )


def governed_ledger() -> tuple[str, int, int, int]:
    return _ledger(GOVERNED, governed_kind, GOVERNED_LEDGER_REASON)


def adjacency_ledger() -> tuple[str, int, int, int]:
    return _ledger(ADJACENCY_ONLY, adjacency_kind, ADJACENCY_LEDGER_REASON)


HASH_BOUND_CANDIDATES = {
    2154: (41_417, 933, 307, "fc490b29b4e9bccca63211d15a343bb12f54073324aa3f679694506ce705a151"),
    2422: (92_766, 1128, 767, "af0f9a518be6e813de266014ea84ef65acd7ab3c0bce6dc4b77304086bb0404c"),
    2430: (45_490, 905, 412, "f6dda658647f60f79be0157922ce5fa5279e96141566e761f8e02258629f48a1"),
    4412: (59_518, 853, 294, "b3abd7c2f4f658cb3e405eb31dfba25f7b4ddde8de513f3f9cf8788e8d36f7b1"),
    4418: (87_360, 904, 453, "1fb4c22a34260fdfd050a7cacee9d9b4efa3bd8af60c35c4110a082881fcf739"),
    4428: (203_762, 1117, 900, "8c110e0b3fd53ff59a60dc9f2522a6bbdeef920ea46494d1a4dd18004fb94060"),
    10259: (36_753, 1154, 277, "851cf63cb497d076054d9b3cedf0db108f0cb439a7876726075eb82b5cfe0f6c"),
    13312: (23_933, 592, 238, "e1443f6b4aee358dad09728c67919c6ead43d3a8c583e8ff63c78b458e647ec7"),
    13638: (3_967, 132, 153, "0a556a9e6208e87f94d87b0a476f4b2f38de12967431cd4eef8ac76ed63c0927"),
    13640: (4_169, 131, 161, "1d3b216e84533b46ce242e6dd682684f914572560afe38b0b52f4534fa7b6740"),
    13648: (25_176, 548, 175, "2b17dc927842b7cefa8d1aa777b46fb2a8634f4fc62386c00e301482add40743"),
    13652: (38_810, 545, 247, "6d138c039f5d319f8f8635d19b33cabbd6dbff7a68249de6810c7adfa79d5a71"),
    13656: (40_329, 573, 225, "350a3c7090182a8c74d8890e4a92bc38cd51da2c72b648aca0084f44cc529a8b"),
    13742: (18_968, 574, 243, "e584cf7dc88c04282641904275cf4c977f712dfd8840b1c0f9116e2ee99560a5"),
    13748: (36_386, 568, 398, "05d21731abacb2cd5dec383baa0f87af165b7b638ccb2aa32a1645e27702ddf5"),
    13891: (14_489, 220, 318, "f368c0cdbd7eb83edda9e97dfeaa3f489e5b69a608fd8a87402cd949abd9a042"),
    13893: (12_957, 150, 296, "8a38223e5c7459e70b7d54fd25582fb5c54b56083e2d487cf3b155dd60d893cf"),
    13895: (13_701, 175, 316, "5266f380501e301506c0908c9ea965e28ec3b80b2c2872d46b461cfc824fdeb6"),
    13907: (12_706, 570, 93, "12c5b95ea2bbbfb2998e4d52820584b67dc2a357d991af3321ea256953c5b038"),
    15479: (48_777, 573, 284, "bc0eb1da6c34a828981031939e0ac0e1b7a3136581655c5a27771ddc32d19193"),
    15487: (42_208, 536, 195, "fddb41a6fd05e1afa24d654b44bf516dc240ec5ae36bec4f726d1937d11c7413"),
    16450: (104_351, 552, 503, "f109e4b50674bff8f054e83d8c70da6cfdbd767511eb4de2b8eafeb02af63ce1"),
}
assert set(HASH_BOUND_CANDIDATES) == C4
for book_line, (expected_bytes, expected_width, expected_height, expected_digest) in (
    HASH_BOUND_CANDIDATES.items()
):
    data = physical_image(book_line).read_bytes()
    assert len(data) == expected_bytes
    assert jpeg_size(data) == (expected_width, expected_height)
    assert hashlib.sha256(data).hexdigest() == expected_digest


# Page 369 and page 371 use the same 14-entry implementation over a distorted
# square array.  These predicates come from the retained implementation text,
# not from reading pixels in the two plates.
def hex_output(code: int, self_value: int, black_neighbor_count: int) -> int:
    assert 0 <= code < 2**14
    assert self_value in (0, 1) and 0 <= black_neighbor_count <= 6
    aggregate = self_value + 2 * black_neighbor_count
    digits = tuple(map(int, f"{code:014b}"))
    return digits[13 - aggregate]


assert all(
    hex_output(16382, self_value, count) == int(self_value == 1 or count >= 1)
    for self_value in (0, 1)
    for count in range(7)
)
assert all(
    hex_output(10926, self_value, count) == int(self_value == 1 or count == 1)
    for self_value in (0, 1)
    for count in range(7)
)


def outer_totalistic_growth_any_code(degree: int) -> int:
    """Derived all-cases-but-empty code for a binary degree-m growth rule."""

    assert degree >= 1
    return 2 ** (2 * (degree + 1)) - 2


assert outer_totalistic_growth_any_code(5) == 4094
assert outer_totalistic_growth_any_code(3) == 254


# Human transcriptions contain only source-stated metadata for the six native
# plates.  They neither recover arrays from pictures nor promote observers to
# construction data.
TRANSCRIPT_SPECS = (
    (
        "dimensional_arrangements",
        2154,
        (2156,),
        ("1D_line", "2D_square_with_triangular_and_hexagonal_alternatives", "3D_cubic_with_other_and_nonrepetitive_alternatives"),
    ),
    (
        "hex_growth_page_369",
        4412,
        (4410, 4414, 15608, 15610, 15612),
        ("distorted_square_representation_of_hexagonal_lattice", 6, "persistent_or_any_neighbor", 16382),
    ),
    (
        "hex_growth_page_371",
        4428,
        (4422, 4424, 4430, 15608, 15610, 15612),
        ("distorted_square_representation_of_hexagonal_lattice", 6, "persistent_or_exactly_one_neighbor", 10926),
    ),
    (
        "nearest_neighbor_lattice_shapes",
        13648,
        (13642, 13644, 13646),
        (
            ("2D_square", 4),
            ("2D_hexagon", 6),
            ("3D_cube", 6),
            ("3D_hexagonal_prism", 8),
            ("3D_rhombic_dodecahedron_fcc", 12),
            ("3D_elongated_dodecahedron", 12),
            ("3D_truncated_octahedron_bcc", 14),
            ("4D_possible_counts", (8, 16, 24)),
        ),
    ),
    (
        "pentagonal_growth",
        13652,
        (13650,),
        ("congruent_pentagonal_tiling", 5, "outer_totalistic", 4094, "persistent_or_any_neighbor"),
    ),
    (
        "penrose_growth",
        13656,
        (13654,),
        ("nested_nonrepetitive_Penrose_tiling", "two_tile_shapes_treated_same", 3, "outer_totalistic", 254, "persistent_or_any_neighbor"),
    ),
)
assert len(TRANSCRIPT_SPECS) == 6


def transcript_payload() -> str:
    rows: list[str] = []
    names: set[str] = set()
    for name, asset_line, source_lines, values in TRANSCRIPT_SPECS:
        assert name not in names
        names.add(name)
        assert asset_line in NATIVE
        assert source_lines and set(source_lines) <= S
        asset_data = physical_image(asset_line).read_bytes()
        asset_digest = hashlib.sha256(asset_data).hexdigest()
        source_record = "\x1e".join(
            f"{line_number}:{lines[line_number - 1]}" for line_number in source_lines
        )
        source_digest = hashlib.sha256(source_record.encode("utf-8")).hexdigest()
        rows.append(
            f"{name}|asset={asset_line}|asset_sha256={asset_digest}|"
            f"source={','.join(map(str, source_lines))}|source_sha256={source_digest}|"
            f"values={values!r}"
        )
    assert len(rows) == 6
    return "\n".join(rows) + "\n"


TRANSCRIPT_PAYLOAD = transcript_payload()
TRANSCRIPT_SHA256 = hashlib.sha256(TRANSCRIPT_PAYLOAD.encode("utf-8")).hexdigest()


# Guard both source text and exact monolith image references.  Printed pages
# 169, 369, 371, 929, 930, 932, 943, 930/936, and 987 use extracted JPEG page
# numbers shifted by front matter; names prevent a printed/extracted-page swap.
EXPECTED_IMAGE_NAMES = {
    2154: "_page_184_Picture_6.jpeg",
    4412: "_page_384_Picture_8.jpeg",
    4428: "_page_386_Figure_1.jpeg",
    13648: "_page_945_Picture_2.jpeg",
    13652: "_page_945_Picture_4.jpeg",
    13656: "_page_945_Picture_6.jpeg",
    13748: "_page_947_Picture_14.jpeg",
    13891: "_page_951_Picture_6.jpeg",
    13893: "_page_951_Picture_7.jpeg",
    13895: "_page_951_Picture_8.jpeg",
    15487: "_page_1002_Picture_9.jpeg",
}
assert {line: Path(images[line]).name for line in EXPECTED_IMAGE_NAMES} == EXPECTED_IMAGE_NAMES

guards = {
    2156: "Examples of simple arrangements of elements in one, two and three dimensions",
    4410: "any cell which is adjacent to a black cell will itself become black on the next step",
    4414: "reflects directly the structure of the underlying lattice of cells",
    4422: "simple hexagonal grid",
    4424: "cells become black if they have exactly one black neighbor",
    4430: "each cell on a hexagonal grid becomes black whenever exactly one",
    13642: "limited number of types of cells can be identified",
    13644: "what matters is not detailed geometry, but merely what cells are adjacent",
    13646: "In 4D, 8, 16 and 24 nearest neighbors are possible",
    13650: "has code 4094",
    13654: "first example is code 254",
    13658: "each cell corresponds to a node in a network",
    13746: "Penrose tilings",
    13889: "only a single active node",
    13909: "assign a color to each node, and then update this color at each step",
    13913: "NetCAStep",
    15485: "For a simple cubic lattice the regions are cubes with 6 faces",
    15608: "treat hexagonal lattices as distorted square lattices",
    15610: "CAStep",
    15612: "code 16382; on page 371 it is code 10926",
}
for line_number, fragment in guards.items():
    assert line_number in S
    assert fragment in lines[line_number - 1], (line_number, fragment)


# Fixed-network label evolution is source-complete text, not an omitted raster.
# The nearby picture is a dimensionality observer for structurally evolving
# network systems and remains adjacency-only.
FIXED_NETWORK_TEXT_EVIDENCE = {13658, 13909, 13910, 13913, 13914, 13915}
assert FIXED_NETWORK_TEXT_EVIDENCE <= set(SOURCE.NATIVE_EVIDENCE)
assert ADJ_NETWORK_OBSERVER == {13907}
assert not ({13907} & GOVERNED)


# Notes are physically stored in split Index, while nominal split Notes is
# empty.  Representative reverse joins cover arbitrary dimensions, other
# geometries, fixed networks, and the two hexagonal-array rule codes.
notes_split = ASSET_ROOT / "BACK-MATTER/Index/Index.md"
notes_split_lines = notes_split.read_text(encoding="utf-8").splitlines()
nominal_notes = ASSET_ROOT / "BACK-MATTER/Notes/Notes.md"
assert len(nominal_notes.read_text(encoding="utf-8").splitlines()) == 1
for book_line, split_line in {
    13483: 1384,
    13513: 1414,
    13642: 1543,
    13650: 1551,
    13654: 1555,
    13658: 1559,
    13909: 1810,
    15608: 3509,
    15612: 3513,
}.items():
    assert lines[book_line - 1] == notes_split_lines[split_line - 1]


HASH_BOUND_ASSETS = set(C4)
TRANSCRIBED_ASSETS = {asset_line for _, asset_line, _, _ in TRANSCRIPT_SPECS}
PIXEL_REPLAYED_ASSETS: set[int] = set()
assert len(HASH_BOUND_ASSETS) == 22
assert TRANSCRIBED_ASSETS == NATIVE
assert len(TRANSCRIBED_ASSETS) == 6
assert not PIXEL_REPLAYED_ASSETS

# Plates may show visible cells or frames, but complete native topology,
# initial configuration, update horizon, and renderer are not serialized.
TOPOLOGY_NOT_SERIALIZED = set(NATIVE)
SEED_NOT_SERIALIZED = N_HEX_ANY | N_HEX_EXACT1 | N_PENTAGON | N_PENROSE
TRACE_NOT_REPLAYABLE = set(SEED_NOT_SERIALIZED)
assert TOPOLOGY_NOT_SERIALIZED == TRANSCRIBED_ASSETS
assert TRACE_NOT_REPLAYABLE <= TRANSCRIBED_ASSETS


EXPECTED_TRANSCRIPT_SHA256 = "c8dea3a540c8bf6dca319bc1d8387daf33b45a7d830cba1a7facc3150f7e3ba3"
EXPECTED_GOVERNED_UNIVERSE_SHA256 = EXPECTED_GOVERNED_DIGEST
EXPECTED_GOVERNED_LEDGER_SHA256 = "36a902946f4c447733483b49e05ecae7ba29e3ed0d05fb76606c87491d6869ff"
EXPECTED_ADJACENCY_UNIVERSE_SHA256 = "2b47127033ba2b7d5b363e36fc20188a906da8ef0b3b3c86a4a3e6c272fc3cfa"
EXPECTED_ADJACENCY_LEDGER_SHA256 = "3091c88d840e3283bdf349ad43355ad4590af8d368ca7b82426829dbec423200"
EXPECTED_CANDIDATE_UNIVERSE_SHA256 = "d2d1265a973f27484c6fc8bc797c3a903c46b4f734e11d854a66af562a271fa8"


def main() -> None:
    governed_payload, governed_monolith_refs, governed_split_refs, governed_hashes = (
        governed_ledger()
    )
    adjacency_payload, adjacency_monolith_refs, adjacency_split_refs, adjacency_hashes = (
        adjacency_ledger()
    )

    assert TRANSCRIPT_SHA256 == EXPECTED_TRANSCRIPT_SHA256
    assert digest_set(GOVERNED) == EXPECTED_GOVERNED_UNIVERSE_SHA256
    assert hashlib.sha256(governed_payload.encode("utf-8")).hexdigest() == EXPECTED_GOVERNED_LEDGER_SHA256
    assert digest_set(ADJACENCY_ONLY) == EXPECTED_ADJACENCY_UNIVERSE_SHA256
    assert hashlib.sha256(adjacency_payload.encode("utf-8")).hexdigest() == EXPECTED_ADJACENCY_LEDGER_SHA256
    assert digest_set(C4) == EXPECTED_CANDIDATE_UNIVERSE_SHA256

    assert len(governed_payload.splitlines()) == 11
    assert len(adjacency_payload.splitlines()) == 11
    assert (governed_monolith_refs, governed_split_refs, governed_hashes) == (11, 11, 11)
    assert (adjacency_monolith_refs, adjacency_split_refs, adjacency_hashes) == (11, 11, 11)
    all_rows = governed_payload.splitlines() + adjacency_payload.splitlines()
    assert len({row.split("|")[7] for row in all_rows}) == 22

    print(
        f"T24 asset oracle: PASS source={len(S)}; C4=22; governed=11; adjacency_only=11; "
        "governed native/relation/control=6/2/3; "
        "native dimension/hex-any/hex-exact1/lattices/pentagon/Penrose=1/1/1/1/1/1; "
        "adjacency structural-network/natural-observer/other-CA/substitution/"
        "network-observer/static-geometry/sequential-CA=2/1/4/1/1/1/1; "
        "refs=44; unique_hashes=22; "
        f"transcript_records=6; transcript_sha256={TRANSCRIPT_SHA256}; "
        "HASH_BOUND=22; TRANSCRIBED=6; PIXEL_REPLAYED=0; "
        "hex_codes_16382/10926=PASS; pentagonal_4094/Penrose_254=PASS; "
        "fixed_network=TEXT_ONLY; topology/seed/trace=NOT_SERIALIZED; "
        "monolith/split/image_guards=PASS; Notes_reverse_join=PASS; unresolved=0"
    )


if __name__ == "__main__":
    main()
