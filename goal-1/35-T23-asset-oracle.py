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
    14273: "successive-step moving-structure observer for named B5/S45 preset",
}
assert set(REASON) == U


# Radius four is a mechanical source-proximity audit, not semantic ownership.
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
ADJ_STOCHASTIC = {2888, 2892, 2900, 3802, 3806, 7082, 7090}
ADJ_NONSTEP = {15487}
ADJ_ALTERNATE_UPDATE = {16450}
ADJ_RELATION = {
    2010, 2012, 2098, 2104, 2154, 3786, 13312, 14230, 14232, 14334, 17006,
}
adjacency_classes = (
    ADJ_T22,
    ADJ_T24,
    ADJ_STOCHASTIC,
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
assert tuple(map(len, adjacency_classes)) == (11, 1, 7, 1, 1, 11)

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
        "A-STOCHASTIC" if book_line in ADJ_STOCHASTIC else
        "A-NONSTEP" if book_line in ADJ_NONSTEP else
        "A-ALT-UPDATE" if book_line in ADJ_ALTERNATE_UPDATE else
        "A-RELATION"
    )


def ledger() -> tuple[str, int, int, int]:
    return _ledger(U, governed_kind, REASON)


def adjacency_ledger() -> tuple[str, int, int, int]:
    return _ledger(ADJACENCY_ONLY, adjacency_kind, ADJACENCY_REASON)


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
NAMED_CLASS4 = ((5, 7, 6), (4, 5, 5), (5, 6, 5))
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
    ("full26_icon", 2260, (2262,), ("twenty_six_face_edge_corner_neighbors",)),
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
        "class4_b5_s45",
        14273,
        (14263, 14271),
        ((4, 5, 5), "B5/S45", "successive_steps_of_moving_structure"),
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
