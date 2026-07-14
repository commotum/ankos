#!/usr/bin/env python3
"""Frozen T23 three-dimensional cellular-automaton asset closure.

The primary plates distinguish two cubic access profiles: the six cells that
share a face with the center and all twenty-six cells in the surrounding
``3 x 3 x 3`` shell.  The center remains a separately declared read in the
compact product tables.  Depth-shaded projections, cuboid drawings, crops,
and finite display boxes are observers; none defines native coordinates,
support, boundary behavior, transition values, or rule identity.

Every raster is hash-bound to its monolith and split-corpus references.  Human
transcriptions below are entitled only by nearby source text or visible panel
labels.  No raster is treated as a serialization of a three-dimensional state,
and no stochastic plate is replayed without complete configuration, RNG,
distribution, horizon, and renderer data.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path


if not __debug__:
    raise RuntimeError("T23 asset verification requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "ref/A-New-Kind-of-Science"
BOOK = ASSET_ROOT / "A-New-Kind-of-Science.md"
SOURCE_ORACLE_PATH = ROOT / "goal-1/35-T23-source-oracle.py"

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


def digest_set(values: set[int] | frozenset[int]) -> str:
    return hashlib.sha256(",".join(map(str, sorted(values))).encode("ascii")).hexdigest()


def load_source_oracle():
    assert SOURCE_ORACLE_PATH.is_file(), "T23 source oracle is not frozen yet"
    spec = importlib.util.spec_from_file_location("t23_source_oracle", SOURCE_ORACLE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SOURCE = load_source_oracle()
S = set(SOURCE.RETAINED)

# Filled from the independent source oracle's frozen public interface.
EXPECTED_SOURCE_COUNT = 138
EXPECTED_SOURCE_DIGEST = "92ce01dbf10875f7549f3eedb180a9001c72c588494247ec13d6b9f5d7160c07"
EXPECTED_GOVERNED_IMAGE_COUNT = 10
EXPECTED_GOVERNED_IMAGE_DIGEST = "321e19bd6ddda35985b08d095c182b529076ce4eea99854230c5b512b6f115ef"

assert len(S) == EXPECTED_SOURCE_COUNT
assert SOURCE.digest(SOURCE.RETAINED) == EXPECTED_SOURCE_DIGEST
assert len(SOURCE.GOVERNED_IMAGE_LINES) == EXPECTED_GOVERNED_IMAGE_COUNT
assert SOURCE.digest(SOURCE.GOVERNED_IMAGE_LINES) == EXPECTED_GOVERNED_IMAGE_DIGEST


def near(source_lines: set[int], radius: int = 4) -> set[int]:
    assert source_lines
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


# Direct construction plates.  CFACE and CFULL are distinct access profiles;
# the tiny companion images are source-governed access/rule icons, not lookup
# tables recovered from pixels.  OPROJ is explicitly a depth-shaded top view.
CFACE = {2252, 2254}
CFULL = {2258, 2260}
OPROJ = {13634, 13636, 13638, 13640}
P_CLASS4 = {14273}
X24 = {13648}
U = CFACE | CFULL | OPROJ | P_CLASS4 | X24
STRICT_U = CFACE | CFULL | OPROJ | P_CLASS4

assert U == set(SOURCE.GOVERNED_IMAGE_LINES)
assert set(images) & S == U
assert digest_set(U) == EXPECTED_GOVERNED_IMAGE_DIGEST
classes = (CFACE, CFULL, OPROJ, P_CLASS4, X24)
assert all(not (left & right) for i, left in enumerate(classes) for right in classes[i + 1 :])
assert (len(U), len(CFACE), len(CFULL), len(OPROJ), len(P_CLASS4), len(X24)) == (
    10, 2, 2, 4, 1, 1
)


REASON = {
    2252: "direct six-face any/exact-one trace plate from a single black cell",
    2254: "six-face access/rule icon accompanying the direct trace",
    2258: "direct full-26 exact-one/exact-two trace plate with declared seeds",
    2260: "full-26 surrounding-cube access/rule icon accompanying the direct trace",
    13634: "30-update depth-shaded top projection of the exact-one-of-26 run",
    13636: "30-update depth-shaded top projection of the exact-two-of-26 run",
    13638: "30-update projection of exact-three-of-26 from a 3x1x1 block",
    13640: "30-update projection of exact-three-of-26 from a 3x3x1 block",
    13648: "T24 alternative three-dimensional nearest-neighbor lattice control",
    14273: "successive-step moving-structure observer for source-listed parameter tuple (4,5,5)",
}
assert set(REASON) == U

GOVERNING_SOURCE_LINES = {
    2252: (2256,),
    2254: (2256,),
    2258: (2262,),
    2260: (2262,),
    13634: (13632,),
    13636: (13632,),
    13638: (13632,),
    13640: (13632,),
    13648: (13644, 13646),
    14273: (14263, 14271),
}
assert set(GOVERNING_SOURCE_LINES) == U
assert all(set(source_lines) <= S for source_lines in GOVERNING_SOURCE_LINES.values())
GOVERNED_LEDGER_REASON = {
    book_line: f"{REASON[book_line]}; source={','.join(map(str, GOVERNING_SOURCE_LINES[book_line]))}"
    for book_line in U
}


# C4 is the declared one-hop radius-four source-proximity universe, not
# semantic ownership.  Only the original retained source lines are centers;
# rasters reached by this pass do not recursively become new search centers.
# All 32 ungoverned candidates remain in the physical ledger.  In particular,
# the T22 plates between the T23 introduction and its direct examples are the
# preceding row-of-eleven two-dimensional evolution, not 3D fixtures.
C4 = near(S)
ADJACENCY_ONLY = C4 - U
assert U <= C4
assert len(C4) == 42
assert len(ADJACENCY_ONLY) == 32
assert digest_set(C4) == "dcb93e36f067ee718cb7b0abf6bbd18ba42dd872b119178533e03933c014cc30"
assert digest_set(ADJACENCY_ONLY) == "be476acd01d8f280750fbc03126b41e5f4f2e3b4e941d85fee721e04f2fc3ea7"

ADJ_T22 = {
    2224, 2228, 2232, 2240, 2242, 2248, 11188, 11190, 13626, 13628, 13630,
}
ADJ_T24 = {13652}
ADJ_RANDOM_REALIZATION = {2888, 2892, 2900}
ADJ_STOCHASTIC_UPDATE = {3802, 3806, 7082, 7090}
ADJ_NONSTEP = {15487}
ADJ_ALTERNATE_UPDATE = {16450}
ADJ_RELATION = {
    2010, 2012, 2098, 2104, 2154, 3786, 13312, 14230, 14232, 14334, 17006,
}
adjacency_classes = (
    ADJ_T22,
    ADJ_T24,
    ADJ_RANDOM_REALIZATION,
    ADJ_STOCHASTIC_UPDATE,
    ADJ_NONSTEP,
    ADJ_ALTERNATE_UPDATE,
    ADJ_RELATION,
)
assert all(
    not (left & right)
    for i, left in enumerate(adjacency_classes)
    for right in adjacency_classes[i + 1 :]
)
assert set().union(*adjacency_classes) == ADJACENCY_ONLY
assert tuple(map(len, adjacency_classes)) == (11, 1, 3, 4, 1, 1, 11)

ADJACENCY_REASON = {
    2010: "continuous-cell-value CA relation reached only by source proximity",
    2012: "continuous-cell-value CA observer reached only by source proximity",
    2098: "posed PDE evolution plate; not a T23 cubic configuration",
    2104: "posed PDE evolution plate; not a T23 cubic configuration",
    2154: "one/two/three-dimensional arrangement illustration; topology relation only",
    2224: "T22 Moore access icon preceding the T23 introduction",
    2228: "T22 code-746 approximately circular run",
    2232: "T22 code-174826 odd-row seed gallery",
    2240: "T22 stacked observer of the preceding row-of-eleven run",
    2242: "T22 continuation of the preceding row-of-eleven run",
    2248: "T22 continuation of the preceding row-of-eleven run",
    2888: "continuous CA from an unserialized random initial condition",
    2892: "continuous class-4 CA from an unserialized random initial condition",
    2900: "continuous class-4 CA from an unserialized random initial condition",
    3786: "deterministic rule-30 initial-perturbation observer",
    3802: "continuous CA under unserialized external random perturbations",
    3806: "continuous CA under unserialized external random perturbations",
    7082: "probabilistic one-dimensional CA plate; sampled outcomes not serialized",
    7090: "probabilistic CA best-fit comparison; sampled outcomes not serialized",
    11188: "fourth of the T22 code-3702 last-five output panels",
    11190: "fifth of the T22 code-3702 last-five output panels",
    13312: "continuous additive-CA relation from the Notes",
    13626: "T22 code-174826 upper-right-quadrant observer",
    13628: "T22 code-174826 upper-right-quadrant observer",
    13630: "T22 code-174826 upper-right-quadrant observer",
    13652: "T24 pentagonal/alternative-lattice CA control",
    14230: "one-dimensional class-frequency statistical observer",
    14232: "one-dimensional class-frequency statistical observer",
    14334: "one-dimensional finite-period comparison observer",
    15487: "static Voronoi diagram with no canonical stepwise evolution",
    16450: "sequential-cell-update CA with a different schedule",
    17006: "continuous complex-amplitude block-CA relation",
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
        "C-FACE" if book_line in CFACE else
        "C-FULL" if book_line in CFULL else
        "O-PROJECTION" if book_line in OPROJ else
        "P-CLASS4" if book_line in P_CLASS4 else
        "X24"
    )


def adjacency_kind(book_line: int) -> str:
    return (
        "A-T22" if book_line in ADJ_T22 else
        "A-T24" if book_line in ADJ_T24 else
        "A-RANDOM-SEED" if book_line in ADJ_RANDOM_REALIZATION else
        "A-STOCHASTIC-UPDATE" if book_line in ADJ_STOCHASTIC_UPDATE else
        "A-NONSTEP" if book_line in ADJ_NONSTEP else
        "A-ALT-UPDATE" if book_line in ADJ_ALTERNATE_UPDATE else
        "A-RELATION"
    )


def ledger() -> tuple[str, int, int, int]:
    return _ledger(U, governed_kind, GOVERNED_LEDGER_REASON)


def adjacency_ledger() -> tuple[str, int, int, int]:
    return _ledger(ADJACENCY_ONLY, adjacency_kind, ADJACENCY_LEDGER_REASON)


HASH_BOUND_GOVERNED = {
    2252: (162_466, 1178, 1189, "4e5c77f3258b025ee4f8232820701900e2f4548ac2387282c15268106a780f97"),
    2254: (2_833, 173, 65, "cf54b86188b111158c4065435d661bfcaaf0e7afd782647767df6404df772eee"),
    2258: (224_987, 1179, 1192, "ec3e6be95a3104a48259389f10f1101519f985bb3565166ecd212a42f5802d1a"),
    2260: (3_582, 175, 71, "cfa1ecc95b1c19e72f0904b120107b70eb730cb26c80ef74edfbf7e6858ed3be"),
    13634: (7_498, 128, 134, "f57385f2d30bb02f6695cb1aca8ea4035a54efeaa77fb1591ae543c6456f25b1"),
    13636: (4_410, 135, 149, "d1e343bc17d478c5e9249837e5210589ed1efd3e2f7f9d72747122435524449e"),
    13638: (3_967, 132, 153, "0a556a9e6208e87f94d87b0a476f4b2f38de12967431cd4eef8ac76ed63c0927"),
    13640: (4_169, 131, 161, "1d3b216e84533b46ce242e6dd682684f914572560afe38b0b52f4534fa7b6740"),
    13648: (25_176, 548, 175, "2b17dc927842b7cefa8d1aa777b46fb2a8634f4fc62386c00e301482add40743"),
    14273: (15_018, 578, 84, "b293416f5b629568040e1608747fb496c1773579ce50d0ef87dffdcd13ef5363"),
}
assert set(HASH_BOUND_GOVERNED) == U
for book_line, (expected_bytes, expected_width, expected_height, expected_digest) in (
    HASH_BOUND_GOVERNED.items()
):
    data = physical_image(book_line).read_bytes()
    assert len(data) == expected_bytes
    assert jpeg_size(data) == (expected_width, expected_height)
    assert hashlib.sha256(data).hexdigest() == expected_digest


def face_predicate(name: str, count: int) -> int:
    assert 0 <= count <= 6
    if name == "any":
        return int(count >= 1)
    if name == "exact1":
        return int(count == 1)
    raise ValueError(name)


def full_predicate(exact: int, count: int) -> int:
    assert exact in {1, 2, 3} and 0 <= count <= 26
    return int(count == exact)


def life3d_predicate(parameters: tuple[int, int, int], self_value: int, count: int) -> int:
    """Book ``{p,q,r}``: survival interval ``p..q`` and birth count ``r``."""

    p, q, r = parameters
    assert self_value in (0, 1) and 0 <= count <= 26 and 0 <= p <= q <= 26
    return int((self_value == 1 and p <= count <= q) or (self_value == 0 and count == r))


assert tuple(face_predicate("any", count) for count in range(7)) == (0, 1, 1, 1, 1, 1, 1)
assert tuple(face_predicate("exact1", count) for count in range(7)) == (0, 1, 0, 0, 0, 0, 0)
assert all(sum(full_predicate(exact, count) for count in range(27)) == 1 for exact in (1, 2, 3))
SOURCE_LISTED_CLASS4_PARAMETERS = ((5, 7, 6), (4, 5, 5), (5, 6, 5))
assert tuple(
    count
    for count in range(27)
    if life3d_predicate((4, 5, 5), 0, count)
) == (5,)
assert tuple(
    count
    for count in range(27)
    if life3d_predicate((4, 5, 5), 1, count)
) == (4, 5)

# This B/S notation is a derived canonical spelling of the source-listed
# parameter tuple, not a label supplied by BOOK:14263--14271.
DERIVED_CANONICAL_SPELLING = {(4, 5, 5): "B5/S45"}
assert DERIVED_CANONICAL_SPELLING[(4, 5, 5)] == "B5/S45"


# Human transcriptions are hash- and source-bound metadata.  ``step 1`` is the
# displayed seed panel, not silently reinterpreted as one committed update.
DISPLAYED_STEPS = tuple(range(1, 11))
TRANSCRIPT_SPECS = (
    (
        "face6_direct",
        2252,
        (2256,),
        (("any", "single_black", DISPLAYED_STEPS, "octahedral_limit"),
         ("exact1", "single_black", DISPLAYED_STEPS, "nested")),
    ),
    ("face6_icon", 2254, (2256,), ("six_face_sharing_neighbors",)),
    (
        "full26_direct",
        2258,
        (2262,),
        (("exact1", "single_black", DISPLAYED_STEPS),
         ("exact2", "line_of_3", DISPLAYED_STEPS)),
    ),
    ("full26_icon", 2260, (2262,), ("twenty_six_surrounding_positions",)),
    (
        "projection_exact1",
        13634,
        (13632,),
        ("exact1_of_26", "single_black", 30, "top_view_nearer_darker"),
    ),
    (
        "projection_exact2",
        13636,
        (13632,),
        ("exact2_of_26", "line_of_3", 30, "top_view_nearer_darker"),
    ),
    (
        "projection_exact3_line",
        13638,
        (13632,),
        ("exact3_of_26", "3x1x1", 30, "top_view_nearer_darker"),
    ),
    (
        "projection_exact3_slab",
        13640,
        (13632,),
        ("exact3_of_26", "3x3x1", 30, "top_view_nearer_darker"),
    ),
    (
        "class4_source_tuple_4_5_5",
        14273,
        (14263, 14271),
        ((4, 5, 5), "successive_steps_of_moving_structure"),
    ),
)
assert len(TRANSCRIPT_SPECS) == 9


def transcript_payload() -> str:
    rows: list[str] = []
    names: set[str] = set()
    for name, asset_line, source_lines, values in TRANSCRIPT_SPECS:
        assert name not in names
        names.add(name)
        assert asset_line in STRICT_U
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
    assert len(rows) == 9
    return "\n".join(rows) + "\n"


TRANSCRIPT_PAYLOAD = transcript_payload()
TRANSCRIPT_SHA256 = hashlib.sha256(TRANSCRIPT_PAYLOAD.encode("utf-8")).hexdigest()
assert "B5/S45" not in TRANSCRIPT_PAYLOAD


# Printed pages 182--183 are extracted as physical JPEG pages 197--198 after
# fifteen pages of front matter.  The Notes and class-4 fixtures live on their
# own physical page numbers.  Freeze names so a display-page/printed-page mixup
# cannot silently substitute another plate.
PAGE_OFFSET_NAMES = {
    2252: "_page_197_Picture_1.jpeg",
    2254: "_page_197_Figure_2.jpeg",
    2258: "_page_198_Picture_2.jpeg",
    2260: "_page_198_Picture_3.jpeg",
}
assert {line: Path(images[line]).name for line in PAGE_OFFSET_NAMES} == PAGE_OFFSET_NAMES


guards = {
    2156: "shown is a cubic lattice",
    2256: "six neighbors with which it shares a face",
    2262: "depend on all 26 neighbors that share either a face or a corner",
    13483: "In d dimensions with k colors",
    13488: "a + k AxesTotal[a, d]",
    13497: "generalize to 3<sup>d</sup> -neighbor rules",
    13501: "a + k FullTotal[a, d]",
    13509: "positions of black cells can conveniently be displayed",
    13511: "Graphics3D[Map[Cuboid[-Reverse[#]]",
    13632: "Looking from above, with closer cells shown darker",
    13644: "in 3D (as found by Evgraf Fedorov in 1885) the cube (6)",
    14263: "3D class 4 rules",
    14266: "LifeStep3D",
    14271: "{5, 7, 6}, {4, 5, 5}, and {5, 6, 5}",
}
for line_number, fragment in guards.items():
    assert line_number in S
    assert fragment in lines[line_number - 1], (line_number, fragment)


# Notes are physically stored in split Index, while nominal split Notes is
# empty.  These representative reverse joins cover face/full mechanics,
# 3D display, projections, other-lattice control, and the named class-4 preset.
notes_split = ASSET_ROOT / "BACK-MATTER/Index/Index.md"
notes_split_lines = notes_split.read_text(encoding="utf-8").splitlines()
nominal_notes = ASSET_ROOT / "BACK-MATTER/Notes/Notes.md"
assert len(nominal_notes.read_text(encoding="utf-8").splitlines()) == 1
for book_line, split_line in {
    13483: 1384,
    13497: 1398,
    13501: 1402,
    13509: 1410,
    13632: 1533,
    13644: 1545,
    14263: 2164,
    14271: 2172,
}.items():
    assert lines[book_line - 1] == notes_split_lines[split_line - 1]


HASH_BOUND_ASSETS = set(C4)
TRANSCRIBED_ASSETS = {asset_line for _, asset_line, _, _ in TRANSCRIPT_SPECS}
PIXEL_REPLAYED_ASSETS: set[int] = set()
assert len(HASH_BOUND_ASSETS) == 42
assert len(TRANSCRIBED_ASSETS) == 9
assert TRANSCRIBED_ASSETS == STRICT_U
assert not PIXEL_REPLAYED_ASSETS

# Random-seed realizations remain deterministic programs; external
# perturbations and probability-valued rules instead alter transition-time
# semantics.  Neither group serializes the complete configuration/sample
# stream needed for exact raster replay.
UNREPLAYABLE_RANDOM_ASSETS = ADJ_RANDOM_REALIZATION | ADJ_STOCHASTIC_UPDATE
assert len(UNREPLAYABLE_RANDOM_ASSETS) == 7
assert UNREPLAYABLE_RANDOM_ASSETS <= ADJACENCY_ONLY


EXPECTED_TRANSCRIPT_SHA256 = "07d1261a07ddd0f5ecb5fcf311335b2310d148174e1a09641070a6daa492deed"
EXPECTED_STRICT_UNIVERSE_SHA256 = "8fd664af3fbc564763b551e5475494bb19661c9a352100ba840d028172ac0d97"
EXPECTED_STRICT_LEDGER_SHA256 = "ea0d1fc8e38281cdc470cf2f5eb15e132fcef0b6f3d2c444c29a933e6039826f"
EXPECTED_GOVERNED_UNIVERSE_SHA256 = EXPECTED_GOVERNED_IMAGE_DIGEST
EXPECTED_GOVERNED_LEDGER_SHA256 = "c9e97695a427f4355cd9e6edffe6ba919b55b23a195a236ae0bfceeaaca597c8"
EXPECTED_ADJACENCY_UNIVERSE_SHA256 = "be476acd01d8f280750fbc03126b41e5f4f2e3b4e941d85fee721e04f2fc3ea7"
EXPECTED_ADJACENCY_LEDGER_SHA256 = "6d68210c6b265dcbb9fcb3ab2297501cb4a32c59b74f454f8e8707ad8204f34d"
EXPECTED_CANDIDATE_UNIVERSE_SHA256 = "dcb93e36f067ee718cb7b0abf6bbd18ba42dd872b119178533e03933c014cc30"


def selected_payload(payload: str, selected: set[int]) -> str:
    rows = [
        row
        for row in payload.splitlines()
        if int(row.split("|", 1)[0]) in selected
    ]
    assert len(rows) == len(selected)
    return "\n".join(rows) + "\n"


def main() -> None:
    payload, monolith_refs, split_refs, hashes = ledger()
    adjacency_payload, adjacency_monolith_refs, adjacency_split_refs, adjacency_hashes = (
        adjacency_ledger()
    )
    strict_payload = selected_payload(payload, STRICT_U)
    assert "B5/S45" not in payload

    assert TRANSCRIPT_SHA256 == EXPECTED_TRANSCRIPT_SHA256
    assert digest_set(STRICT_U) == EXPECTED_STRICT_UNIVERSE_SHA256
    assert hashlib.sha256(strict_payload.encode("utf-8")).hexdigest() == EXPECTED_STRICT_LEDGER_SHA256
    assert digest_set(U) == EXPECTED_GOVERNED_UNIVERSE_SHA256
    assert hashlib.sha256(payload.encode("utf-8")).hexdigest() == EXPECTED_GOVERNED_LEDGER_SHA256
    assert digest_set(ADJACENCY_ONLY) == EXPECTED_ADJACENCY_UNIVERSE_SHA256
    assert hashlib.sha256(adjacency_payload.encode("utf-8")).hexdigest() == EXPECTED_ADJACENCY_LEDGER_SHA256
    assert digest_set(C4) == EXPECTED_CANDIDATE_UNIVERSE_SHA256

    assert len(payload.splitlines()) == 10
    assert len(adjacency_payload.splitlines()) == 32
    assert (monolith_refs, split_refs, hashes) == (10, 10, 10)
    assert (adjacency_monolith_refs, adjacency_split_refs, adjacency_hashes) == (32, 32, 32)
    all_rows = payload.splitlines() + adjacency_payload.splitlines()
    assert len({row.split("|")[7] for row in all_rows}) == 42

    print(
        f"T23 asset oracle: PASS source={len(S)}; C4=42; governed=10; adjacency_only=32; "
        "governed C-face/C-full/O-projection/P-class4/X24=2/2/4/1/1; "
        "adjacency T22/T24/random-seed/stochastic-update/nonstep/alternate-update/relation="
        "11/1/3/4/1/1/11; "
        "refs=84; unique_hashes=42; "
        f"transcript_records=9; transcript_sha256={TRANSCRIPT_SHA256}; "
        "HASH_BOUND=42; TRANSCRIBED=9; PIXEL_REPLAYED=0; "
        "face_any/exact1_and_full_exact1/exact2/exact3=PASS; "
        "source_class4_tuple_(4,5,5)=PASS; derived_canonical_B5/S45=PASS; "
        "projections=OBSERVER_ONLY; "
        "random/stochastic_replay=UNAVAILABLE(no_serialized_configuration/RNG/distribution/renderer); "
        "page_offset=PASS; Notes_reverse_join=PASS; unresolved=0"
    )


if __name__ == "__main__":
    main()
