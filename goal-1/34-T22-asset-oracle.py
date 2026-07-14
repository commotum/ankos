#!/usr/bin/env python3
"""Frozen T22 Moore-neighborhood cellular-automaton asset closure.

The strict Chapter 5 examples use a square lattice, the eight surrounding
cells (including diagonals), and a separately visible center value.  Their
compact rule numbers therefore describe an 18-case ``SelfValue x MooreCount``
table.  General 512-context positional rules and ten-case equal-sum rules use
the same nine declared reads but are distinct RULE schemas.

Raster labels are hash-bound human transcriptions, not executable semantics.
Only facts fixed by Book prose, a complete rule, and an exact seed are derived
here.  No random initial state, PRNG, crop, boundary, palette, or renderer is
invented to make a plate appear replayable.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path


if not __debug__:
    raise RuntimeError("T22 asset verification requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "ref/A-New-Kind-of-Science"
BOOK = ASSET_ROOT / "A-New-Kind-of-Science.md"
SOURCE_ORACLE_PATH = ROOT / "goal-1/34-T22-source-oracle.py"

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
    assert SOURCE_ORACLE_PATH.is_file(), "T22 source oracle is not frozen yet"
    spec = importlib.util.spec_from_file_location("t22_source_oracle", SOURCE_ORACLE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SOURCE = load_source_oracle()
S = set(SOURCE.RETAINED)


def near(source_lines: set[int], radius: int = 4) -> set[int]:
    assert source_lines
    return {
        line_number
        for line_number in images
        if min(abs(line_number - source) for source in source_lines) <= radius
    }


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


def outer_count_output(code: int, self_value: int, moore_count: int) -> int:
    """18-case code: low-to-high bit index is ``2*count + self``."""

    if not 0 <= code < 2**18:
        raise ValueError("Moore outer-count code must have at most 18 bits")
    if self_value not in (0, 1) or not 0 <= moore_count <= 8:
        raise ValueError("invalid binary self/Moore-count case")
    return (code >> (2 * moore_count + self_value)) & 1


def encode_outer_count(predicate) -> int:
    return sum(
        1 << (2 * count + self_value)
        for count in range(9)
        for self_value in (0, 1)
        if predicate(self_value, count)
    )


def code_175850_predicate(self_value: int, count: int) -> bool:
    return count in {3, 5} or (self_value == 1 and count not in {3, 5})


def code_746_predicate(self_value: int, count: int) -> bool:
    return count == 3 or (self_value == 1 and count in {0, 1, 2, 4})


def code_174826_predicate(self_value: int, count: int) -> bool:
    return count == 3 or (self_value == 1 and count != 3)


NAMED_CODE_PREDICATES = {
    175_850: code_175850_predicate,
    746: code_746_predicate,
    174_826: code_174826_predicate,
}
for named_code, predicate in NAMED_CODE_PREDICATES.items():
    assert encode_outer_count(predicate) == named_code
    assert all(
        outer_count_output(named_code, self_value, count) == predicate(self_value, count)
        for count in range(9)
        for self_value in (0, 1)
    )
    assert outer_count_output(named_code, 0, 0) == 0


# Direct native plates.  C18 contains the Chapter 5 count-rule traces and its
# nine-position access icon.  The Book establishes the 512-context positional
# schema in prose, but supplies no direct C512 raster plate.  O contains views
# of the same code-174826 run rather than another rule or executor.
C18 = {2220, 2224, 2228, 2232}
C512: set[int] = set()
O = {2240, 2242, 2244, 2246, 2248, 13626, 13628, 13630}
STRICT_U = C18 | C512 | O


HASH_BOUND_STRICT = {
    2220: (245_146, 1163, 1221, "bfc32030860d4b0e9d3f836f4a7f9aac65d76780842edb4329dac344a2bfb979"),
    2224: (2_866, 174, 96, "92a1ec8298e4d5e6b673db24d65549f8f197725b1eb5d634ccd489c21596cdf7"),
    2228: (349_419, 1186, 1188, "619632d2e70821bb87d0e374e15313765e00c20195466e377195d333cfcf64db"),
    2232: (85_008, 1134, 699, "a1732422a9a954e5ec89988138fe23dd4b5a1929107298b5664b20a842edaea2"),
    2240: (146_561, 1178, 1242, "36f05cdf712339707e89040a929b38991ed1bf2bfaa1371ebf33cd24d472bdd9"),
    2242: (29_724, 593, 456, "3ccec68b36203e94bd506d0b57408cb412b21b59bff908ccf273a50495f44996"),
    2244: (50_316, 541, 557, "75653dc6c95dde22448e892c7bb0a97907361717e02369da8dd5e9a253cbbc90"),
    2246: (50_329, 528, 565, "6d9dcbea90ba98b05cd152450b41ebbb4b9554732b119590692a0b614dccd499"),
    2248: (70_665, 601, 615, "f3b81cfffda71eb9626e4c1a1cc5b9027b135000bd49fd01791c2178afe7d191"),
    13626: (8_259, 173, 211, "afc3073eb966064ef5794b255ce1fd402b85fbce8f7f94484281d1363650765b"),
    13628: (7_227, 184, 212, "af69e803aaf53e31122794eef45fe76f6c99d19099eacbf752dbabfd2bf055c5"),
    13630: (6_998, 199, 222, "5719e73c7e2c41e95a50bd35c9f3f264dcf4e33ee5cfc8aef5c96ad583361872"),
}
assert set(HASH_BOUND_STRICT) == STRICT_U
for book_line, (expected_bytes, expected_width, expected_height, expected_digest) in (
    HASH_BOUND_STRICT.items()
):
    data = physical_image(book_line).read_bytes()
    assert len(data) == expected_bytes
    assert jpeg_size(data) == (expected_width, expected_height)
    assert hashlib.sha256(data).hexdigest() == expected_digest


# Hash-bound human transcription.  A displayed ``step 1`` is the seed panel;
# this is deliberately not silently converted to an event count.  Text saying
# "after N steps" is separately recorded as N updates.
CODE_175850_DISPLAYED_STEPS = tuple(range(1, 25)) + (100, 200)
CODE_175850_SEED = ("finite_row", 7)
CODE_746_UPDATES = 400
CODE_746_SEED = ("finite_row", 7)
CODE_174826_SEED_LENGTHS = tuple(range(3, 32, 2))
CODE_174826_UPDATES = 60
CODE_174826_STACK_SEEDS = (13, 15, 17, 11)
CODE_174826_CONTINUATION_LABELS = {
    2242: (100, 200),
    2244: (300,),
    2246: (400,),
    2248: (500,),
}
CODE_174826_NOTES_LABELS = {
    13626: (1000,),
    13628: (2000,),
    13630: (3000,),
}

STRICT_TRANSCRIPT_SPECS = (
    (
        "code175850_direct",
        2220,
        (2226,),
        (175_850, CODE_175850_SEED, CODE_175850_DISPLAYED_STEPS, "rough_surface"),
    ),
    ("moore_access_icon", 2224, (2226,), ("eight_surrounding_plus_self",)),
    (
        "code746_direct",
        2228,
        (2230,),
        (746, CODE_746_SEED, CODE_746_UPDATES, "approximately_circular", "radius_about_0.37*t"),
    ),
    (
        "code174826_seed_gallery",
        2232,
        (2234,),
        (174_826, CODE_174826_SEED_LENGTHS, CODE_174826_UPDATES, "some_fixed_some_growing"),
    ),
    (
        "code174826_stacked_observer",
        2240,
        (2250,),
        (CODE_174826_STACK_SEEDS, "largest_display_200_steps"),
    ),
    *(
        (f"code174826_continuation_{asset_line}", asset_line, (2250,), labels)
        for asset_line, labels in sorted(CODE_174826_CONTINUATION_LABELS.items())
    ),
    *(
        (
            f"code174826_notes_{asset_line}",
            asset_line,
            (13622, 13624),
            ("upperright_quadrant", labels),
        )
        for asset_line, labels in sorted(CODE_174826_NOTES_LABELS.items())
    ),
)
assert len(STRICT_TRANSCRIPT_SPECS) == 12


# Source-entitled relations and controls.  R keeps deterministic Moore-family
# applications/observers outside the strict Chapter 5 fixture.  The X classes
# make close but semantically distinct constructions visible: T21 cardinal
# access, T23 3D access, T24 other lattices, Life as a named preset, and pure
# constraints/stochastic aggregation, which do not share T22's deterministic
# one-successor rule despite using 3x3 templates or eight-neighbor geometry.
R = {
    3900,
    3908,
    3912,
    4450,
    5636,
    11182,
    11184,
    11186,
    11188,
    11190,
    15269,
    15271,
    15275,
    15277,
    15279,
    15281,
    18759,
}
X21 = {2920}
X23 = {2252, 2254, 2258, 2260, 13634, 13636, 13638, 13640, 14273}
X24 = {4428, 13648, 13652, 13656}
XLIFE = {
    14789,
    14793,
    14797,
    14801,
    14805,
    14809,
    14813,
    14817,
    14819,
    14821,
    14823,
    14829,
    14831,
    14833,
    14837,
    14839,
    14841,
    14843,
    18753,
}
XNONFIT = {2682, 15223, 15225, 15227, 15229, 15231}
U = STRICT_U | R | X21 | X23 | X24 | XLIFE | XNONFIT

classes = (C18, C512, O, R, X21, X23, X24, XLIFE, XNONFIT)
assert all(not (left & right) for i, left in enumerate(classes) for right in classes[i + 1 :])
assert (len(U), len(C18), len(C512), len(O), len(R), len(X21), len(X23), len(X24), len(XLIFE), len(XNONFIT)) == (
    68,
    4,
    0,
    8,
    17,
    1,
    9,
    4,
    19,
    6,
)


REASON: dict[int, str] = {}
for line_number in C18:
    REASON[line_number] = "strict 18-case SelfValue x MooreCount rule/access/trace plate"
for line_number in O:
    REASON[line_number] = "observer of the strict code-174826 evolution"
for line_number in R:
    REASON[line_number] = "deterministic Moore-family relation, application, or observer"
for line_number in X21:
    REASON[line_number] = "T21 four-cardinal-neighbor control"
for line_number in X23:
    REASON[line_number] = "T23 three-dimensional cellular-automaton control"
for line_number in X24:
    REASON[line_number] = "T24 alternative-lattice control"
for line_number in XLIFE:
    REASON[line_number] = "Game of Life named-preset relation/control"
for line_number in XNONFIT:
    REASON[line_number] = "constraint or stochastic-aggregation nonfit/control"
REASON.update(
    {
        2220: "code-175850 row-7 trace and rough-growth plate",
        2224: "nine-position Moore access icon for the strict count rule",
        2228: "code-746 row-7 400-update approximately circular plate",
        2232: "code-174826 60-update odd-row-seed gallery",
        3900: "code-746 intrinsic-randomness and circular-growth observer",
        3908: "domain-boundary observer with fixed rectangular seed",
        3912: "totalistic code-976 random periodic realization relation",
        4450: "eight-neighbor growth/crystal-shape relation",
        5636: "code-746 orientation/isotropy observer",
        11182: "first of five code-3702 totalistic output panels",
        11184: "second of five code-3702 totalistic output panels",
        11186: "third of five code-3702 totalistic output panels",
        11188: "fourth of five code-3702 totalistic output panels",
        11190: "fifth of five code-3702 totalistic output panels",
        15269: "code-746 long-run anisotropy observer",
        15271: "code-746 long-run anisotropy observer",
        15275: "other Moore rule 10,000-update relation",
        15277: "other Moore rule 10,000-update relation",
        15279: "other Moore rule 10,000-update relation",
        15281: "other Moore rule 10,000-update relation",
        18759: "four-color WireWorld eight-neighbor relation",
        2682: "pure 3x3-template constraint with no stepwise evolution",
        15223: "stochastic eight-neighbor aggregation control",
        15225: "stochastic eight-neighbor aggregation control",
        15227: "stochastic eight-neighbor aggregation control",
        15229: "stochastic eight-neighbor aggregation control",
        15231: "stochastic eight-neighbor aggregation control",
    }
)
assert set(REASON) == U
