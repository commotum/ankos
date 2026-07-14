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
EXPECTED_SOURCE_COUNT = 264
EXPECTED_SOURCE_DIGEST = "e54447c5ecdd87f896d65e5f05bbcd809de6908a357f35762a44aedb194c39e6"
EXPECTED_GOVERNED_IMAGE_COUNT = 68
EXPECTED_GOVERNED_IMAGE_DIGEST = "d596854fe15fafe293038296ec2e5872612edda3033c08d6d2d314134ac3dd43"
assert len(S) == EXPECTED_SOURCE_COUNT
assert SOURCE.digest(S) == EXPECTED_SOURCE_DIGEST
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


def code_224_life_predicate(self_value: int, count: int) -> bool:
    """Life B3/S23 in the same 18-case code convention."""

    return count == 3 or (self_value == 1 and count == 2)


NAMED_CODE_PREDICATES = {
    175_850: code_175850_predicate,
    746: code_746_predicate,
    174_826: code_174826_predicate,
    224: code_224_life_predicate,
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
# applications/observers outside the strict Chapter 5 fixture.  P keeps Game
# of Life visible as the ordinary named B3/S23 preset (outer-count code 224)
# over this same T22 algebra.  The X classes mark actual construction controls:
# T21 cardinal access, T23 3D access, T24 other lattices, and a pure constraint
# model set.  S separately records stochastic aggregation: it has canonical
# evolution, but its RNG/distribution semantics belong to its owning stage and
# are not silently imported into strict deterministic T22.
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
P = {
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
S_STOCHASTIC = {15223, 15225, 15227, 15229, 15231}
XCONSTRAINT = {2682}
U = STRICT_U | R | P | S_STOCHASTIC | X21 | X23 | X24 | XCONSTRAINT
assert set(SOURCE.GOVERNED_IMAGE_LINES) == U
assert set(images) & S == U

classes = (C18, C512, O, R, P, S_STOCHASTIC, X21, X23, X24, XCONSTRAINT)
assert all(not (left & right) for i, left in enumerate(classes) for right in classes[i + 1 :])
assert (len(U), len(C18), len(C512), len(O), len(R), len(P), len(S_STOCHASTIC), len(X21), len(X23), len(X24), len(XCONSTRAINT)) == (
    68,
    4,
    0,
    8,
    17,
    19,
    5,
    1,
    9,
    4,
    1,
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
for line_number in P:
    REASON[line_number] = "Game of Life named B3/S23 outer-count-code-224 preset/relation"
for line_number in S_STOCHASTIC:
    REASON[line_number] = "stochastic eight-neighbor aggregation relation; RNG semantics deferred"
for line_number in XCONSTRAINT:
    REASON[line_number] = "pure 3x3-template constraint/model-set nonstep control"
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
        15223: "stochastic eight-neighbor aggregation relation; RNG semantics deferred",
        15225: "stochastic eight-neighbor aggregation relation; RNG semantics deferred",
        15227: "stochastic eight-neighbor aggregation relation; RNG semantics deferred",
        15229: "stochastic eight-neighbor aggregation relation; RNG semantics deferred",
        15231: "stochastic eight-neighbor aggregation relation; RNG semantics deferred",
    }
)
assert set(REASON) == U


# Radius four is an independent proximity candidate audit, not semantic
# ownership.  The 27 unentitled rasters remain fully ledgered rather than being
# discarded because their captions, neighboring examples, or physical pages
# happen to lie near retained T22 evidence.
C4 = near(S)
ADJACENCY_ONLY = C4 - U
assert U <= C4
assert len(C4) == 95
assert len(ADJACENCY_ONLY) == 27
assert hashlib.sha256(
    ",".join(map(str, sorted(C4))).encode("ascii")
).hexdigest() == "fd5999e41e82738f1c6fe3ef16713d0e6c7534c21f3714a9c059cc530e6df175"
assert hashlib.sha256(
    ",".join(map(str, sorted(ADJACENCY_ONLY))).encode("ascii")
).hexdigest() == "7b95fd5481303cc5ebcb3f5e942f8c10a160562ed83bff429fa0028dcc868602"

ADJ_RELATED = {
    2172,
    2176,
    2598,
    2686,
    2924,
    4074,
    4076,
    13565,
    13567,
    13577,
    13615,
    14111,
    14117,
    15217,
    15219,
    15235,
    15263,
}
ADJ_OTHER = ADJACENCY_ONLY - ADJ_RELATED
assert not (ADJ_RELATED & ADJ_OTHER)
assert ADJ_RELATED | ADJ_OTHER == ADJACENCY_ONLY
assert (len(ADJ_RELATED), len(ADJ_OTHER)) == (17, 10)

ADJACENCY_REASON = {
    line_number: "typed relation/control reached only by radius-four proximity"
    for line_number in ADJ_RELATED
}
ADJACENCY_REASON.update(
    {
        line_number: "other-construction or false-proximity raster"
        for line_number in ADJ_OTHER
    }
)
ADJACENCY_REASON.update(
    {
        2172: "T21 four-cardinal access diagram reached by proximity",
        2176: "T21 four-cardinal code-1022 trace reached by proximity",
        2598: "static four-neighbor constraint plate",
        2686: "continuation of a pure 3x3-template constraint model set",
        2924: "T21 four-cardinal equal-sum random-gallery continuation",
        4074: "constraint/invariant-state relation",
        4076: "constraint/invariant-state relation",
        4418: "hexagonal snowflake image before the retained lattice model",
        11134: "one-dimensional rule-30 output",
        11176: "preceding function-rule output, not one of code 3702's five panels",
        13565: "T21 five-position growth-count panel",
        13567: "T21 five-position growth-count panel",
        13577: "T21 code-942 slice observer",
        13615: "T21 historical outer-count-code-12 plate",
        14111: "constraint/model-set relation",
        14117: "constraint relation to a one-dimensional CA history",
        15217: "preceding stochastic four-neighbor aggregation plate",
        15219: "preceding stochastic four-neighbor aggregation plate",
        15235: "later stochastic eight-neighbor aggregation continuation",
        15263: "diffusion-limited aggregation plate before code-746 evidence",
        16450: "sequential-update cellular-automaton control",
        16456: "one-dimensional sequential additive-rule plate",
        16458: "one-dimensional sequential additive-rule plate",
        16462: "one-dimensional sequential additive-rule plate",
        16464: "one-dimensional sequential additive-rule plate",
        17433: "single-step image-processing relation",
        18746: "preceding two-neighbor rule plate",
    }
)
assert set(ADJACENCY_REASON) == ADJACENCY_ONLY


def governed_kind(book_line: int) -> str:
    return (
        "C18" if book_line in C18 else
        "C512" if book_line in C512 else
        "O" if book_line in O else
        "R" if book_line in R else
        "P-LIFE" if book_line in P else
        "S-STOCHASTIC" if book_line in S_STOCHASTIC else
        "X21" if book_line in X21 else
        "X23" if book_line in X23 else
        "X24" if book_line in X24 else
        "X-CONSTRAINT"
    )


def adjacency_kind(book_line: int) -> str:
    return "A-RELATED" if book_line in ADJ_RELATED else "A-OTHER"


def ledger() -> tuple[str, int, int, int]:
    """Exact governed-universe manifest (68 rows)."""

    return _ledger(U, governed_kind, REASON)


def adjacency_ledger() -> tuple[str, int, int, int]:
    """Exact radius-four-only exclusion manifest (27 rows)."""

    return _ledger(ADJACENCY_ONLY, adjacency_kind, ADJACENCY_REASON)


CODE_746_REPRISE_LABELS = tuple(range(1, 17)) + (50, 100, 200, 300, 400)
CODE_976_RANDOM_LABELS = (
    1,
    2,
    3,
    4,
    5,
    10,
    20,
    30,
    40,
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500,
    550,
    600,
    700,
    800,
)
CODE_3702_ASSETS = (11182, 11184, 11186, 11188, 11190)
OTHER_MOORE_RULE_ASSETS_AND_SEEDS = (
    (15275, 7),
    (15277, 6),
    (15279, 7),
    (15281, 11),
)

RELATION_TRANSCRIPT_SPECS = (
    (
        "code746_reprise",
        3900,
        (3902,),
        (746, CODE_746_REPRISE_LABELS, "intrinsic_randomness", "roughly_circular"),
    ),
    (
        "domain_boundary_observer",
        3908,
        (3910,),
        ("initial_black_rectangle", 39, 29, "shrinks_to_nothing"),
    ),
    (
        "code976_random_periodic",
        3912,
        (3914,),
        (976, CODE_976_RANDOM_LABELS, "random_initial", "periodic_width_80"),
    ),
    (
        "code746_orientation",
        5636,
        (5638,),
        (746, (10, 40, 110), "rule_c_100_updates", "orientation_observer"),
    ),
    *(
        (
            f"code3702_last_five_{asset_line}",
            asset_line,
            (11178, 11180),
            (3702, "one_of_last_five_outputs_after_25_updates"),
        )
        for asset_line in CODE_3702_ASSETS
    ),
    (
        "code746_anisotropy_15269",
        15269,
        (15267,),
        (746, "anisotropy_about_4_percent_after_a_few_thousand_updates"),
    ),
    (
        "code746_anisotropy_15271",
        15271,
        (15267,),
        (746, "anisotropy_about_4_percent_after_a_few_thousand_updates"),
    ),
    *(
        (
            f"other_moore_rule_{asset_line}",
            asset_line,
            (15273,),
            ("finite_row", seed_length, "10,000_updates"),
        )
        for asset_line, seed_length in OTHER_MOORE_RULE_ASSETS_AND_SEEDS
    ),
    (
        "wireworld_relation",
        18759,
        (18755, 18757),
        ("four_colors", "eight_neighbors_counting_value_1", "1D_CA_emulation"),
    ),
)
assert len(RELATION_TRANSCRIPT_SPECS) == 16


# Printed pages 177--181 are extracted as physical JPEG pages 192--196 after
# fifteen pages of front matter.  Literal physical page-178/180/181 assets are
# unrelated Chapter 4 number-system plates.
PAGE_OFFSET_NAMES = {
    2220: "_page_192_Figure_2.jpeg",
    2224: "_page_192_Picture_4.jpeg",
    2228: "_page_193_Picture_2.jpeg",
    2232: "_page_194_Picture_1.jpeg",
    2240: "_page_195_Picture_2.jpeg",
    2242: "_page_196_Picture_2.jpeg",
    2244: "_page_196_Picture_3.jpeg",
    2246: "_page_196_Picture_4.jpeg",
    2248: "_page_196_Picture_5.jpeg",
}
assert {line: Path(images[line]).name for line in PAGE_OFFSET_NAMES} == PAGE_OFFSET_NAMES
PAGE_NUMBER_FALSE_FRIENDS = {
    2048: "_page_178_Picture_2.jpeg",
    2084: "_page_180_Picture_2.jpeg",
    2104: "_page_181_Picture_2.jpeg",
}
assert {line: Path(images[line]).name for line in PAGE_NUMBER_FALSE_FRIENDS} == PAGE_NUMBER_FALSE_FRIENDS
assert set(PAGE_NUMBER_FALSE_FRIENDS).isdisjoint(C4)


guards = {
    2212: "exactly three of its eight neighbors—including diagonals",
    2226: "code number 175850",
    2230: "code number 746",
    2234: "code number 174826",
    2250: "row of 11 black cells",
    13475: "For the 9-neighbor rules introduced on page 177",
    13479: "ListConvolve[{{2, 2, 2}, {2, 1, 2}, {2, 2, 2}}",
    13481: "IntegerDigits[code, 2, 18]",
    13544: "$2^{512}",
    13547: "$2^{18}",
    13548: "$2^{10}",
    13549: "$2^9",
    14241: "outer totalistic rules there are examples with codes 224 (Game of Life)",
    14243: "Life 2D cellular automaton",
    14247: "#1 == 1 && #2 == 4 || #2 == 3",
    15221: "with 8 neighbors",
    18755: "4-color WireWorld cellular automaton",
}
for line_number, fragment in guards.items():
    assert line_number in S
    assert fragment in lines[line_number - 1], (line_number, fragment)


# T22 Notes are physically stored in split Index, while nominal split Notes is
# empty.  Freeze representative reverse joins across mechanics, schema counts,
# the named Life preset, and long-run code-746 evidence.
notes_split = ASSET_ROOT / "BACK-MATTER/Index/Index.md"
notes_split_lines = notes_split.read_text(encoding="utf-8").splitlines()
nominal_notes = ASSET_ROOT / "BACK-MATTER/Notes/Notes.md"
assert len(nominal_notes.read_text(encoding="utf-8").splitlines()) == 1
for book_line, split_line in {
    13475: 1376,
    13544: 1445,
    13620: 1521,
    14239: 2140,
    14243: 2144,
    15267: 3168,
}.items():
    assert lines[book_line - 1] == notes_split_lines[split_line - 1]


TRANSCRIPT_SPECS = STRICT_TRANSCRIPT_SPECS + RELATION_TRANSCRIPT_SPECS
HASH_BOUND_ASSETS = set(C4)
TRANSCRIBED_ASSETS = {asset_line for _, asset_line, _, _ in TRANSCRIPT_SPECS}
PIXEL_REPLAYED_ASSETS: set[int] = set()
assert len(HASH_BOUND_ASSETS) == 95
assert len(TRANSCRIBED_ASSETS) == 28
assert TRANSCRIBED_ASSETS <= U
assert not PIXEL_REPLAYED_ASSETS


def transcript_payload() -> str:
    rows: list[str] = []
    names: set[str] = set()
    for name, asset_line, source_lines, values in TRANSCRIPT_SPECS:
        assert name not in names
        names.add(name)
        assert asset_line in U
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
    assert len(rows) == 28
    return "\n".join(rows) + "\n"


TRANSCRIPT_PAYLOAD = transcript_payload()
TRANSCRIPT_SHA256 = hashlib.sha256(TRANSCRIPT_PAYLOAD.encode("utf-8")).hexdigest()

# These plates disclose no executable random stream.  Their labels and images
# are retained, but replay requires an RNG/distribution/seed or explicit finite
# configuration that the Book does not serialize here.
UNREPLAYABLE_RANDOM_ASSETS = {3912} | S_STOCHASTIC
assert UNREPLAYABLE_RANDOM_ASSETS <= U


EXPECTED_TRANSCRIPT_SHA256 = "981e0e0391310b9f3b86cd0f8863589bbf7423ddd1da87525da10d2ae704c4e3"
EXPECTED_STRICT_UNIVERSE_SHA256 = "9be14d56b98ad3cf701533768d12c5b98cb05a85c599d73cb029f213bcc6efa4"
EXPECTED_STRICT_LEDGER_SHA256 = "a8dfd2a91350fefe29f1e7f205182daa932335f555fb44be05fc256d1dbfa730"
EXPECTED_GOVERNED_UNIVERSE_SHA256 = "d596854fe15fafe293038296ec2e5872612edda3033c08d6d2d314134ac3dd43"
EXPECTED_GOVERNED_LEDGER_SHA256 = "0e88ca4aa91ea5599f71dbee0347ac7ea8bfa16d865a9bb4a6ac34f5cb317c13"
EXPECTED_ADJACENCY_UNIVERSE_SHA256 = "7b95fd5481303cc5ebcb3f5e942f8c10a160562ed83bff429fa0028dcc868602"
EXPECTED_ADJACENCY_LEDGER_SHA256 = "55e369f47d4108febd80b8e6b09f2ab5a7b50ff09bb5da8644a63909c079191d"
EXPECTED_LIFE_UNIVERSE_SHA256 = "d43e2ef92df4c54ee10d3e491907851dc544389ad3a69ec38506a1c1726cbced"
EXPECTED_LIFE_LEDGER_SHA256 = "ababa435e3e54af24ce60c8e9e32455087fb0bdae5865884a419cd4123878a76"
assert TRANSCRIPT_SHA256 == EXPECTED_TRANSCRIPT_SHA256


def universe_digest(values: set[int]) -> str:
    return hashlib.sha256(",".join(map(str, sorted(values))).encode("ascii")).hexdigest()


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
    life_payload = selected_payload(payload, P)

    assert universe_digest(STRICT_U) == EXPECTED_STRICT_UNIVERSE_SHA256
    assert hashlib.sha256(strict_payload.encode("utf-8")).hexdigest() == EXPECTED_STRICT_LEDGER_SHA256
    assert universe_digest(U) == EXPECTED_GOVERNED_UNIVERSE_SHA256
    assert hashlib.sha256(payload.encode("utf-8")).hexdigest() == EXPECTED_GOVERNED_LEDGER_SHA256
    assert universe_digest(ADJACENCY_ONLY) == EXPECTED_ADJACENCY_UNIVERSE_SHA256
    assert hashlib.sha256(adjacency_payload.encode("utf-8")).hexdigest() == EXPECTED_ADJACENCY_LEDGER_SHA256
    assert universe_digest(P) == EXPECTED_LIFE_UNIVERSE_SHA256
    assert hashlib.sha256(life_payload.encode("utf-8")).hexdigest() == EXPECTED_LIFE_LEDGER_SHA256

    assert len(payload.splitlines()) == 68
    assert len(adjacency_payload.splitlines()) == 27
    assert (monolith_refs, split_refs, hashes) == (68, 68, 68)
    assert (adjacency_monolith_refs, adjacency_split_refs, adjacency_hashes) == (27, 27, 27)
    all_rows = payload.splitlines() + adjacency_payload.splitlines()
    assert len({row.split("|")[7] for row in all_rows}) == 95

    print(
        f"T22 asset oracle: PASS source={len(S)}; C4=95; governed=68; adjacency_only=27; "
        "governed C18/C512/O/R/P-Life/S-stochastic/X21/X23/X24/X-constraint="
        "4/0/8/17/19/5/1/9/4/1; adjacency related/other=17/10; "
        "refs=190; unique_hashes=95; "
        f"transcript_records={len(TRANSCRIPT_SPECS)}; transcript_sha256={TRANSCRIPT_SHA256}; "
        "HASH_BOUND=95; TRANSCRIBED=28; PIXEL_REPLAYED=0; "
        "named_outer_codes_175850/746/174826/224_all_18_cases=PASS; "
        "Life=B3/S23_same_T22_algebra; C512_rasters=0(source_text_only); "
        "random/stochastic_replay=UNAVAILABLE(no_serialized_RNG/distribution/seed); "
        "page_offset=PASS; Notes_reverse_join=PASS"
    )


if __name__ == "__main__":
    main()
