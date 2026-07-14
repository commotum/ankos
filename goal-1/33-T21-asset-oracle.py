#!/usr/bin/env python3
"""Frozen T21 two-dimensional cellular-automaton asset closure.

T21's native plates use the square lattice with four cardinal neighbors.  The
plates deliberately carry two different compact rule profiles: a ten-case
``Self x CardinalCount`` code and a six-case ``CenterPlusFourSum`` code.  This
oracle keeps those profiles separate, hash-binds the direct rule/seed/view
transcriptions, and classifies Moore, 3D, and other-lattice plates as typed
relations or controls rather than silently importing their geometry.

Raster orientation, crop, palette, grid lines, and one-dimensional slice views
are observer data.  Textual captions and Notes are the semantic authority;
pixels are used only for explicitly labelled codes, checkpoints, and panels.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path


if not __debug__:
    raise RuntimeError("T21 asset verification requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "ref/A-New-Kind-of-Science"
BOOK = ASSET_ROOT / "A-New-Kind-of-Science.md"
SOURCE_ORACLE_PATH = ROOT / "goal-1/33-T21-source-oracle.py"

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
    assert SOURCE_ORACLE_PATH.is_file(), "T21 source oracle is not frozen yet"
    spec = importlib.util.spec_from_file_location("t21_source_oracle", SOURCE_ORACLE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SOURCE = load_source_oracle()
S = set(SOURCE.RETAINED)
EXPECTED_SOURCE_COUNT = 312
EXPECTED_SOURCE_DIGEST = "50caf57ebaa912d54ca50df2ec22ebcd418d2b898fbe03414de0af282e9fa60d"
assert len(S) == EXPECTED_SOURCE_COUNT
assert SOURCE.digest(S) == EXPECTED_SOURCE_DIGEST


def near(source_lines: set[int], radius: int = 4) -> set[int]:
    assert source_lines
    return {
        line_number
        for line_number in images
        if min(abs(line_number - source) for source in source_lines) <= radius
    }


# Frozen, caption-governed direct T21 asset roles.  C10 is the center-
# conditioned cardinal-count profile; C6 is the equal-sum profile.  O contains
# only derived stack/slice views of those same native evolutions.
C10 = {
    2172,
    2176,
    2182,
    2192,
    2196,
    13565,
    13567,
    13569,
    13571,
    13573,
}
C6 = {2920, 2924}
O = {2188, 2200, 2928, 13577}
C = C10 | C6

# These source-bound plates are useful relations but do not supply a new
# native T21 profile.  They cover exhaustive five-site rules selected through
# invariant constraints, weighted reads, mixed 4/8-neighbor comparisons,
# application/property views, additivity, and the Ulam/history decompositions.
R = {
    4080,
    5086,
    5636,
    6642,
    10259,
    13599,
    13603,
    13605,
    13607,
    13609,
    13611,
    13615,
}

# Explicit nearby construction controls.  X22 is Moore/eight-neighbor or a
# nine-site/periodic-boundary view, X23 is three-dimensional, and X24 is the
# cross-dimensional/alternative-lattice boundary.  Keeping these sets literal
# prevents a nearby plate from being promoted merely because it shares a
# caption or physical page.
X22 = {
    2220,
    2224,
    2228,
    2232,
    2240,
    2242,
    2244,
    2246,
    2248,
    3900,
    3912,
    13626,
    13628,
    13630,
}
X23 = {2252, 2254, 2258, 2260, 13634, 13636, 13638, 13640}
X24 = {13648, 13652, 13656}
X = X22 | X23 | X24
U = C | O | R | X
STRICT_U = C | O

EXPECTED_SOURCE_ASSETS = {
    2172, 2176, 2182, 2188, 2192, 2196, 2200,
    2220, 2224, 2228, 2232, 2240, 2242, 2244, 2246, 2248,
    2252, 2254, 2258, 2260,
    2920, 2924, 2928,
    3900, 3912, 4080, 5086, 5636, 6642, 10259,
    13565, 13567, 13569, 13571, 13573, 13577, 13599,
    13603, 13605, 13607, 13609, 13611, 13615,
    13626, 13628, 13630, 13634, 13636, 13638, 13640,
    13648, 13652, 13656,
}
assert set(images) & S == EXPECTED_SOURCE_ASSETS
assert U == EXPECTED_SOURCE_ASSETS
classes = (C10, C6, O, R, X22, X23, X24)
assert all(not (left & right) for i, left in enumerate(classes) for right in classes[i + 1 :])
assert (len(U), len(C10), len(C6), len(O), len(R), len(X22), len(X23), len(X24)) == (
    53, 10, 2, 4, 12, 14, 8, 3
)

REASON: dict[int, str] = {}
for line_number in C10:
    REASON[line_number] = "native square-grid Self x CardinalCount rule/trace plate"
for line_number in C6:
    REASON[line_number] = "native square-grid CenterPlusFourSum rule/trace plate"
REASON.update({
    2188: "stacked-space observer of the native code-942 evolution",
    2200: "one-dimensional slice observer for the native cardinal gallery",
    2928: "one-dimensional slice observer for the native equal-sum gallery",
    13577: "offset-slice observer for native code 942",
    4080: "general five-site rules selected through an invariant-constraint relation",
    5086: "weighted radius-three neighborhood relation",
    5636: "mixed four/eight-neighbor orientation comparison",
    6642: "outer-totalistic perception/application relation with neighborhood unstated here",
    10259: "additive self-reproduction relation",
    13599: "history-bearing Ulam-system predecessor relation",
    13603: "Ulam component relation whose s-only case is outer-totalistic code 686",
    13605: "Ulam component/decomposition relation",
    13607: "Ulam component/decomposition relation",
    13609: "Ulam component/decomposition relation",
    13611: "Ulam component/decomposition relation",
    13615: "historical outer-totalistic code-12 relation from block seeds",
})
for line_number in X22:
    REASON[line_number] = "T22 Moore/eight-neighbor or nine-site control"
for line_number in X23:
    REASON[line_number] = "T23 three-dimensional cellular-automaton control"
for line_number in X24:
    REASON[line_number] = "T24 alternative-lattice/higher-dimensional control"
assert set(REASON) == U


# Hash-bound direct plates.  Bytes and dimensions are checked again in the
# complete source-derived ledger; these individual facts make the native
# transcription independently fail closed.
HASH_BOUND_NATIVE = {
    2172: (3_425, 213, 114, "abfbc90a8bdab839ac452194adf8f7e30258e877967a79ac71db59b1a716df75"),
    2176: (55_226, 1133, 159, "27c53f797a1cc47a0a3fc36985fe35108a708c4897ccbd5417b71303e4ccef56"),
    2182: (215_987, 1154, 565, "a3116f543fc7325ecd3a47d4594416e8441dfc056f5bc5586ccc43576a2ed530"),
    2188: (237_507, 1234, 855, "471580bdfc83549ebd84368ddbae3927126392e6b8048fb30ab063cea89b00c7"),
    2192: (163_251, 1126, 1235, "22c5a519118645ad7dbcd7642bb4e655ffe15152e8125104fdb265faa43e2133"),
    2196: (233_241, 1118, 1402, "c82c50a646122b9265813553a85043cc162f5ed63dc5063bc8b5280d463643e2"),
    2200: (261_068, 1153, 1341, "97e2f28e497096fd83d4c051ff15a93dc732515fabe1f7db4c8816d609804e8c"),
    2920: (309_273, 1109, 1297, "49f35fe65202ef7fbfee2da92b7460d36fc329b66a553782ebf8991f237944dd"),
    2924: (240_733, 1013, 1291, "23df7e86bf96a148a17c13847eb53c773a24f86cc5a24f2e1a550f79b94439e3"),
    2928: (295_433, 1195, 1355, "71f5ac8784f493b664a93aff52e157e1ac7bf94a6b2e910f98de9fef663736ec"),
    13565: (3_315, 102, 122, "282db35c7be44488bd5cd6b67b258ba3ed29672b9a4885e6643c34089c3bedde"),
    13567: (2_651, 119, 114, "3ae6019c97e520386b240af13717284431f43dbb9785e4dc4e31bf6cee00d1be"),
    13569: (3_889, 110, 120, "e7c6082e6cfc90444dc42eb52800e8f7a70a675e8a8e76281beaff35bd28b640"),
    13571: (3_067, 108, 126, "4aedb5c05e6a92981e626f362bec72d58e07d738ef565987a78c9acffc9fa8c2"),
    13573: (3_675, 90, 120, "3da001aec8b59909e106dcba350d68f866cc7559b05f784ff88040d96263f296"),
    13577: (16_819, 597, 231, "8227893d712fabbc2713f800a48cf00dd4bd810e4394ecdd17cb764a170512df"),
}
assert set(HASH_BOUND_NATIVE) == C | O


# Direct raster transcriptions, governed by BOOK:2174--2198 and
# BOOK:2922--2930.  The first gallery uses every integer code 450..498 after
# 22 updates from one black cell; its second plate shows this exact labelled
# subset after twice as many updates.  The slice plate is an observer.
CARDINAL_GALLERY_22_CODES = tuple(range(450, 499))
CARDINAL_GALLERY_44_CODES = (
    451,
    452,
    453,
    454,
    457,
    459,
    461,
    462,
    465,
    467,
    468,
    470,
    473,
    475,
    478,
    481,
    483,
    489,
    491,
    493,
)
CARDINAL_SLICE_CODES = tuple(range(450, 482))
assert len(CARDINAL_GALLERY_22_CODES) == 49
assert len(CARDINAL_GALLERY_44_CODES) == 20
assert len(CARDINAL_SLICE_CODES) == 32
assert set(CARDINAL_GALLERY_44_CODES) <= set(CARDINAL_GALLERY_22_CODES)

# The equal-sum random gallery carries one common, visually displayed but not
# serialized random sample.  Checkpoint labels are exact plate data; they do
# not define a PRNG, seed law, crop, or boundary.  The continuation contains
# every nonzero even code below 62 (all-white preserving), excluding 0 and 62.
SUM_GALLERY_CODES = (4, 12, 24, 30, 38, 52)
SUM_GALLERY_CHECKPOINT_LABELS = (1, 2, 5, 100, 500)
SUM_500_CODES = tuple(range(2, 62, 2))
SUM_SLICE_CODES = (4, 12, 24, 38, 30, 52)
assert len(SUM_500_CODES) == 30
assert set(SUM_GALLERY_CODES) <= set(SUM_500_CODES)

# Notes growth-rule labels transcribed from the five hash-bound panels.  The
# source formula, not the plotted shapes, defines the center-conditioned rule.
GROWTH_CARDINAL_COUNTS = (
    (1,),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 3, 4),
)
CODE_942_SLICE_OFFSETS = tuple(range(6))


Point = tuple[int, int]
FiniteDifference = tuple[int, frozenset[Point]]
CARDINAL_OFFSETS: tuple[Point, ...] = ((-1, 0), (0, -1), (0, 1), (1, 0))


def center_conditioned_output(code: int, self_value: int, cardinal_count: int) -> int:
    """Ten-row code: low-to-high bits are (count, self) pairs."""

    if not 0 <= code < 2**10:
        raise ValueError("center-conditioned cardinal code must have ten bits")
    if self_value not in (0, 1) or not 0 <= cardinal_count <= 4:
        raise ValueError("invalid binary center/cardinal-count case")
    return (code >> (2 * cardinal_count + self_value)) & 1


def equal_sum_output(code: int, center_plus_cardinals: int) -> int:
    """Six-row code: bit s is the result for total binary sum s."""

    if not 0 <= code < 2**6 or not 0 <= center_plus_cardinals <= 5:
        raise ValueError("invalid six-row equal-sum case")
    return (code >> center_plus_cardinals) & 1


def center_conditioned_step(state: FiniteDifference, code: int) -> FiniteDifference:
    """Evolve a uniform background plus a finite set of differing sites."""

    background, differences = state
    if background not in (0, 1):
        raise ValueError("background must be binary")
    next_background = center_conditioned_output(code, background, 4 * background)
    candidates = {
        (x + dx, y + dy)
        for x, y in differences
        for dx, dy in ((0, 0),) + CARDINAL_OFFSETS
    }
    next_differences: set[Point] = set()
    for x, y in candidates:
        self_value = background ^ ((x, y) in differences)
        count = sum(
            background ^ ((x + dx, y + dy) in differences)
            for dx, dy in CARDINAL_OFFSETS
        )
        value = center_conditioned_output(code, self_value, count)
        if value != next_background:
            next_differences.add((x, y))
    return next_background, frozenset(next_differences)


def center_conditioned_trace(code: int, updates: int) -> tuple[FiniteDifference, ...]:
    if updates < 0:
        raise ValueError("updates must be nonnegative")
    states: list[FiniteDifference] = [(0, frozenset({(0, 0)}))]
    for _ in range(updates):
        states.append(center_conditioned_step(states[-1], code))
    return tuple(states)


# Textual rule descriptions pin both code convention and one-cell seed.  The
# panel labels are one-origin (step 1 is the seed), so their last visible
# labels correspond to generations 7 and 29 respectively.
assert all(center_conditioned_output(1022, self_value, count) == (self_value == 1 or count > 0)
           for count in range(5) for self_value in (0, 1))
assert all(
    center_conditioned_output(942, self_value, count)
    == (count in {1, 4} or (self_value == 1 and count not in {1, 4}))
    for count in range(5)
    for self_value in (0, 1)
)
CODE_1022_PANEL_LABELS = tuple(range(1, 9))
CODE_942_PANEL_LABELS = tuple(range(1, 9)) + (10, 20, 30)
CODE_1022_LIVE_COUNTS = (1, 5, 13, 25, 41, 61, 85, 113)
CODE_942_LIVE_COUNTS = (1, 5, 9, 21, 29, 41, 53, 89, 129, 545, 1217)
assert tuple(len(center_conditioned_trace(1022, 7)[label - 1][1])
             for label in CODE_1022_PANEL_LABELS) == CODE_1022_LIVE_COUNTS
trace_942 = center_conditioned_trace(942, 29)
assert tuple(len(trace_942[label - 1][1]) for label in CODE_942_PANEL_LABELS) == CODE_942_LIVE_COUNTS

# Odd gallery codes invert the otherwise uniform background on odd events;
# the even 22/44-event plates return it to white.  This complete-state fact is
# why a white raster crop must not be mistaken for a permanently white native
# background or an in-place finite-array boundary.
assert center_conditioned_trace(451, 1)[1][0] == 1
assert center_conditioned_trace(451, 2)[2][0] == 0
assert all(center_conditioned_trace(code, 22)[-1][0] == 0 for code in CARDINAL_GALLERY_22_CODES)
assert all(center_conditioned_trace(code, 44)[-1][0] == 0 for code in CARDINAL_GALLERY_44_CODES)

# Six-case convention and white-background filter.
assert tuple(equal_sum_output(52, total) for total in range(6)) == (0, 0, 1, 0, 1, 1)
assert all(equal_sum_output(code, 0) == 0 for code in SUM_500_CODES)


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


for book_line, (expected_bytes, expected_width, expected_height, expected_digest) in HASH_BOUND_NATIVE.items():
    path = physical_image(book_line)
    data = path.read_bytes()
    assert len(data) == expected_bytes
    assert jpeg_size(data) == (expected_width, expected_height)
    assert hashlib.sha256(data).hexdigest() == expected_digest


def ledger() -> tuple[str, int, int, int]:
    """Return the exact monolith/split/physical manifest for all 53 assets."""

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
            "C10" if book_line in C10 else
            "C6" if book_line in C6 else
            "O" if book_line in O else
            "R" if book_line in R else
            "X22" if book_line in X22 else
            "X23" if book_line in X23 else
            "X24"
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
            f"{split_path.relative_to(ASSET_ROOT).as_posix()}|{split_line}|{REASON[book_line]}"
        )

    return "\n".join(rows) + "\n", monolith_references, split_references, len(hashes)


# The chapter's printed pages 170--175 are physical JPEG pages 185--190: the
# extraction filenames count fifteen pages of front matter.  Literal physical
# page-170 files are Chapter 4 continuous-system plates, not T21 assets.
PAGE_OFFSET_NAMES = {
    2172: "_page_185_Picture_9.jpeg",
    2176: "_page_186_Picture_2.jpeg",
    2182: "_page_186_Picture_5.jpeg",
    2188: "_page_187_Picture_2.jpeg",
    2192: "_page_188_Figure_1.jpeg",
    2196: "_page_189_Figure_1.jpeg",
    2200: "_page_190_Figure_1.jpeg",
}
assert {line: Path(images[line]).name for line in PAGE_OFFSET_NAMES} == PAGE_OFFSET_NAMES
assert all(not Path(images[line]).name.startswith("_page_17") for line in PAGE_OFFSET_NAMES)


# Guard the semantic captions and Notes that entitle the visual transcription.
guards = {
    2168: "neighbors in all four directions on the grid",
    2170: "average of the previous colors of its four neighbors",
    2178: "code 1022",
    2184: "code 942",
    2194: "starting from a single black square and then running for 22 steps",
    2198: "now after twice as many steps",
    2202: "one-dimensional slices",
    2922: "cell and its four immediate neighbors",
    2926: "include most of the 64 possibilities that leave a state that contains only white cells unchanged",
    2930: "One-dimensional slices",
    13471: "For the 5-neighbor rules introduced on page 170",
    13473: "IntegerDigits[code, 2, 10]",
    13563: "minimal number of black cells for growth",
    13575: "Code 942 slices",
}
for line_number, fragment in guards.items():
    assert fragment in lines[line_number - 1], (line_number, fragment)


def main() -> None:
    # Source-bound universe, class partition, complete ledger, and frozen
    # digests are added once the independent source oracle publishes RETAINED.
    print(
        "T21 asset oracle: PROVISIONAL direct=16; "
        "classes native C10/C6/O=10/2/4; "
        "codes 1022/942 + cardinal galleries=PASS; "
        "six-case sum galleries=PASS; native hashes/page offset=PASS"
    )


if __name__ == "__main__":
    main()
