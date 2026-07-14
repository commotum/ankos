#!/usr/bin/env python3
"""Frozen T18 Cyclic Tag Systems asset closure.

The direct T18 rules, phase icons, seeds, and finite-word histories are carried
by the page-95/page-96 rasters.  This oracle hash-binds those native plates,
their observer, the ordinary-tag predecessor controls, and the source-bound
emulation plates without promoting any rendering or compiler into native
cyclic-tag state.

The Notes' mechanical-implementation paragraph says "picture below", but the
repository contains no referenced or physical JPEG for that picture: the
monolith has an OCR placeholder and the split copy omits even the placeholder.
That extraction absence is frozen explicitly instead of inventing an asset.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path


if not __debug__:
    raise RuntimeError("T18 asset verification requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "ref/A-New-Kind-of-Science"
BOOK = ASSET_ROOT / "A-New-Kind-of-Science.md"
SOURCE_ORACLE_PATH = ROOT / "goal-1/32-T18-source-oracle.py"

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
    assert SOURCE_ORACLE_PATH.is_file(), "T18 source oracle is not frozen yet"
    spec = importlib.util.spec_from_file_location("t18_source_oracle", SOURCE_ORACLE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SOURCE = load_source_oracle()
S = set(SOURCE.RETAINED)
EXPECTED_SOURCE_COUNT = 160
EXPECTED_SOURCE_DIGEST = "698fb02434bd7d28565f4dd5c6e8597c079f41d94339374638e9d2a925e7630c"
assert len(S) == EXPECTED_SOURCE_COUNT
assert SOURCE.digest(S) == EXPECTED_SOURCE_DIGEST


def near(source_lines: set[int], radius: int = 4) -> set[int]:
    assert source_lines
    return {
        line_number
        for line_number in images
        if min(abs(line_number - source) for source in source_lines) <= radius
    }


# C4 is the mechanical radius-four closure over the frozen source set.  Q adds
# the complete four-raster page-93 one-deletion ordinary-tag predecessor plate;
# the immediately following page-94 predecessor plate is already in C4.  Every
# direct multi-raster caption and rule-110 relation group is otherwise closed
# by C4, so another iteration adds nothing.
C4 = near(S)
assert C4 == {
    1130,
    1140,
    1142,
    1146,
    1152,
    1156,
    8062,
    8068,
    8070,
    8074,
    8084,
    8180,
    8182,
    8184,
    8186,
    8190,
    8206,
    8228,
    8232,
    8236,
    8240,
    8260,
    18738,
}
Q = {1116, 1118, 1120, 1122}
assert C4.isdisjoint(Q)
U = C4 | Q

# C = native construction evidence, O = derived observer, R = an explicit
# predecessor/control/encoding relation, and X = a mechanically captured but
# excluded adjacency companion.  In particular, rule-110 plates remain
# relations even when they redraw an exact cyclic-tag history.
C = {1140, 1142, 1146, 1152}
O = {1156}
R = {
    1116,
    1118,
    1120,
    1122,
    1130,
    8062,
    8068,
    8070,
    8074,
    8180,
    8182,
    8184,
    8186,
    8190,
    8206,
    8228,
    8232,
    8236,
    8240,
    8260,
    18738,
}
X = {8084}
STRICT_U = C | O
assert C | O | R | X == U
classes = (C, O, R, X)
assert all(not (left & right) for i, left in enumerate(classes) for right in classes[i + 1 :])
assert (len(C4), len(Q), len(U), len(C), len(O), len(R), len(X)) == (
    23,
    4,
    27,
    4,
    1,
    21,
    1,
)

REASON = {
    1116: "ordinary one-deletion tag predecessor trace control",
    1118: "ordinary one-deletion tag predecessor trace control",
    1120: "ordinary one-deletion tag predecessor trace control",
    1122: "ordinary one-deletion tag predecessor rule control",
    1130: "ordinary two-deletion tag predecessor rule/trace control",
    1140: "native alternating-phase finite-word evolution",
    1142: "native remove-head/black-trigger/tail-append schematic",
    1146: "native two-block cyclic rule summary",
    1152: "native five rule pairs, one-black seeds, and 100-step traces",
    1156: "derived length-fluctuation observer for rules d/e",
    8062: "cyclic-tag encoding of a first-element ordinary tag system",
    8068: "multicolor-to-binary Turing-machine relation in the cyclic universality chain",
    8070: "multicolor-to-binary Turing-machine relation in the cyclic universality chain",
    8074: "ordinary-tag/Turing emulation relation in the cyclic universality chain",
    8084: "adjacent register-machine emulation plate excluded",
    8180: "rule-110 lowering relation: native cyclic view",
    8182: "rule-110 lowering relation: stationary-position view",
    8184: "rule-110 lowering relation: displayed cyclic rule",
    8186: "rule-110 lowering relation: information-line view",
    8190: "rule-110 lowering relation: explicit mechanism view",
    8206: "rule-110 localized-structure realization relation",
    8228: "rule-110 compiler schematic relation",
    8232: "rule-110 compiler collision close-up relation",
    8236: "rule-110 compiler collision close-up relation",
    8240: "rule-110 compiler collision close-up relation",
    8260: "rule-110 schematics for four cyclic rule pairs",
    18738: "compiled cyclic-rule/seed to rule-110 initial-block relation",
}
assert set(REASON) == U


# Hash-bound native transcription.  Black is 1 and white is 0.  The direct
# page-95 trace has 25 visible rows t0..t24; page 96 shows 100 rows for each of
# five two-block rules, always from the one-black seed.
HASH_BOUND_NATIVE_SHA256 = {
    1140: "b91df18a471d1e3e02e27bcf3a7b95a3f01e295223cf5ff4bd8b8fb2cc592a75",
    1142: "c8a203dc1ac1530065eb9372f5757991d22bc3c423b0c0c36041824f0acab222",
    1146: "daea1bcb06cb9715295c25a16a0bf33bb3f1ce0188d03e183596479bb1ffa3bb",
    1152: "26790ff2416466d111867c85794fd9b66aa18797cfd270f36e5631ccb7c41dee",
    1156: "b25c6520aed62856eedb5c0f1abe96d3e13ec3d9fd72306e3cb271fe1d24746a",
}
NATIVE_FILE_FACTS = {
    1140: (18_568, 248, 458),
    1142: (7_515, 508, 70),
    1146: (2_558, 226, 45),
    1152: (106_271, 1185, 547),
    1156: (99_927, 1237, 650),
}
NATIVE_IMAGE_NAMES = {
    1140: "_page_110_Picture_4.jpeg",
    1142: "_page_110_Picture_5.jpeg",
    1146: "_page_110_Picture_7.jpeg",
    1152: "_page_111_Figure_1.jpeg",
    1156: "_page_111_Figure_3.jpeg",
}
assert {line: Path(images[line]).name for line in STRICT_U} == NATIVE_IMAGE_NAMES

# Printed book pages 95--96 are PDF image pages 110--111 because the physical
# filenames count front matter.  Literal page-95/page-96 filenames at these
# monolith lines are earlier Turing-machine plates and are not T18 assets.
PAGE_NUMBER_FALSE_FRIENDS = {
    968: "_page_95_Figure_2.jpeg",
    972: "_page_96_Picture_2.jpeg",
    974: "_page_96_Picture_3.jpeg",
    976: "_page_96_Picture_4.jpeg",
}
assert {
    line: Path(images[line]).name for line in PAGE_NUMBER_FALSE_FRIENDS
} == PAGE_NUMBER_FALSE_FRIENDS
assert set(PAGE_NUMBER_FALSE_FRIENDS).isdisjoint(U)
VISUAL_FACTS = {
    "phase": "two circle states alternate on successive live steps",
    "frontier": "exactly the leftmost old symbol is removed",
    "trigger": "the current block is appended exactly when that symbol is black",
    "destination": "real emitted symbols are appended after the preserved old suffix",
    "seed": "all five page-96 examples start from one black symbol",
    "observer": "page-96 fluctuation plots derive from full finite-word histories",
}
assert set(VISUAL_FACTS) == {"phase", "frontier", "trigger", "destination", "seed", "observer"}

Bit = int
Word = tuple[Bit, ...]
Rule = tuple[Word, ...]
State = tuple[int, Word]

DIRECT_RULES: dict[str, Rule] = {
    "a": ((1, 1), (1, 0)),
    "b": ((1,), (1, 1)),
    "c": ((1, 0), (1, 1)),
    "d": ((1,), (1, 0, 1)),
    "e": ((1, 1, 1), (0,)),
}
DIRECT_SEEDS = {name: (1,) for name in DIRECT_RULES}

PAGE_95_ROWS = (
    "1",
    "11",
    "110",
    "1011",
    "01110",
    "1110",
    "11010",
    "101011",
    "0101110",
    "101110",
    "0111010",
    "111010",
    "1101010",
    "10101011",
    "010101110",
    "10101110",
    "010111010",
    "10111010",
    "011101010",
    "11101010",
    "110101010",
    "1010101011",
    "01010101110",
    "1010101110",
    "01010111010",
)

PAGE_96_PREFIX_ROWS = {
    "a": PAGE_95_ROWS[:16],
    "b": (
        "1", "1", "11", "11", "111", "111", "1111", "1111",
        "11111", "11111", "111111", "111111", "1111111", "1111111",
        "11111111", "11111111",
    ),
    "c": (
        "1", "10", "011", "11", "111", "1110", "11011", "101110",
        "0111011", "111011", "1101111", "10111110", "011111011",
        "11111011", "111101111", "1110111110",
    ),
    "d": (
        "1", "1", "101", "011", "11", "11", "1101", "1011",
        "011101", "11101", "1101101", "1011011", "011011101",
        "11011101", "1011101101", "0111011011",
    ),
    "e": (
        "1", "111", "110", "10111", "01110", "1110", "1100", "100111",
        "001110", "01110", "1110", "110111", "101110", "01110111",
        "1110111", "110111111",
    ),
}

PAGE_96_FINAL_ROWS = {
    "a": "10101010101110101010",
    "b": "11111111111111111111111111111111111111111111111111",
    "c": "11101110111110111110111011111011111011101111101110111110111110",
    "d": "110110111011011110111011011101101111011110111011011",
    "e": "001110011101110111011100111001110111011111101111110111",
}
PAGE_96_TRACE_SHA256 = {
    "a": "c9d9199aacac4298a05c9810d19654aa45ff1193067e636c3361cf4f87e21e79",
    "b": "d9a237a460cccbcd90bddc1b47a204b03f7a03941be3fc43388a0af9ae4966ef",
    "c": "adadc131e58c22729fc2651a1989d2fd5fae618cb402807f93e1b7648cbfe019",
    "d": "b7d44cb49a4fa6c6e84564e93ff29f85e12bce9eedc8ba1c6cb5324a4c29577a",
    "e": "024da84c4d9e88aa4af7c6e2ef7441b805af16708be7f2157ec4ffdfabd4cfc1",
}

# BOOK:8180/8184 independently redraws the page-96 rule (d) while lowering it
# toward rule 110.  Its first 21 displayed rows agree exactly, but the asset
# stays class R because the surrounding plate is an encoding relation.
RULE110_RELATION_ROWS = (
    "1", "1", "101", "011", "11", "11", "1101", "1011", "011101",
    "11101", "1101101", "1011011", "011011101", "11011101",
    "1011101101", "0111011011", "111011011", "110110111",
    "10110111101", "01101111011", "1101111011",
)


def live_step(rules: Rule, state: State) -> State:
    """One raster-visible event; empty-word outcome policy is out of scope."""

    phase, word = state
    if not rules or not 0 <= phase < len(rules):
        raise ValueError("invalid cyclic rule phase")
    if not word:
        raise ValueError("no live source exists in the empty word")
    if set(word) - {0, 1} or any(set(block) - {0, 1} for block in rules):
        raise ValueError("direct raster profile is binary")
    head = word[0]
    successor = word[1:] + (rules[phase] if head == 1 else ())
    return (phase + 1) % len(rules), successor


def trace(rules: Rule, seed: Word, rows: int) -> tuple[State, ...]:
    assert rows >= 1
    states: list[State] = [(0, seed)]
    while len(states) < rows:
        states.append(live_step(rules, states[-1]))
    return tuple(states)


def words(states: tuple[State, ...]) -> tuple[str, ...]:
    return tuple("".join(map(str, word)) for _, word in states)


def trace_digest(states: tuple[State, ...]) -> str:
    payload = "\n".join(words(states)) + "\n"
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


assert DIRECT_RULES["a"] == ((1, 1), (1, 0))
assert words(trace(DIRECT_RULES["a"], DIRECT_SEEDS["a"], 25)) == PAGE_95_ROWS
for name, rule in DIRECT_RULES.items():
    states = trace(rule, DIRECT_SEEDS[name], 100)
    assert words(states[:16]) == PAGE_96_PREFIX_ROWS[name]
    assert words(states)[-1] == PAGE_96_FINAL_ROWS[name]
    assert trace_digest(states) == PAGE_96_TRACE_SHA256[name]
    assert tuple(phase for phase, _ in states[:16]) == tuple(i % 2 for i in range(16))
    assert all(word for _, word in states)

# Same queue value with a different visible phase can have a different next
# word.  A white head still consumes one symbol and advances phase but appends
# no block.
assert live_step(DIRECT_RULES["a"], (0, (1,))) == (1, (1, 1))
assert live_step(DIRECT_RULES["a"], (1, (1,))) == (0, (1, 0))
assert live_step(DIRECT_RULES["a"], (0, (0, 1))) == (1, (1,))
assert words(trace(DIRECT_RULES["d"], DIRECT_SEEDS["d"], 21)) == RULE110_RELATION_ROWS


# The mechanical illustration is absent from this extraction.  Both source
# copies retain the prose; neither has a nearby image reference, and no
# physical page-895 JPEG exists anywhere in the asset tree.
assert "Mechanical implementation" in lines[12346 - 1]
assert "picture below" in lines[12346 - 1]
assert lines[12348 - 1] == "#### 000000000000000000000000000000000000000"
assert not (set(images) & set(range(12345, 12350)))
notes_split = ASSET_ROOT / "BACK-MATTER/Index/Index.md"
notes_split_lines = notes_split.read_text(encoding="utf-8").splitlines()
nominal_notes = ASSET_ROOT / "BACK-MATTER/Notes/Notes.md"
assert len(nominal_notes.read_text(encoding="utf-8").splitlines()) == 1
assert "Cyclic Tag Systems" in notes_split_lines[220 - 1]
assert "Implementation" in notes_split_lines[222 - 1]
assert "Generalizations" in notes_split_lines[242 - 1]
assert "Mechanical implementation" in notes_split_lines[251 - 1]
assert "Properties" in notes_split_lines[253 - 1]
assert "History" in notes_split_lines[261 - 1]
assert not any(image_re.fullmatch(line) for line in notes_split_lines[249 - 1 : 254])
assert not any(path.name.startswith("_page_895_") for path in ASSET_ROOT.rglob("*.jpeg"))

# The genuine flattened Index and late compiler Notes are mispartitioned into
# the split Colophon document.  Freeze those exact reverse joins, including the
# one expected image-reference spelling difference at BOOK:18738.
colophon = ASSET_ROOT / "BACK-MATTER/Colophon/Colophon.md"
colophon_lines = colophon.read_text(encoding="utf-8").splitlines()
for book_line, split_line in {
    18514: 1071,
    18674: 1231,
    18740: 1297,
    21068: 3625,
    22150: 4707,
}.items():
    assert lines[book_line - 1] == colophon_lines[split_line - 1]
assert lines[18738 - 1] == "![](_page_1131_Figure_8.jpeg)"
assert colophon_lines[1295 - 1] == "![](Images/_page_1131_Figure_8.jpeg)"


guards = {
    1136: "underlying rule already specify exactly what block can be added at each step",
    1138: "rule simply alternates on successive steps between these blocks",
    1144: "single element is removed from the beginning of the sequence",
    1154: "initial condition consists of a single black element",
    1158: "Fluctuations in the growth of sequences",
    8064: "A cyclic tag system emulating a tag system",
    8176: "rule 110 can emulate any cyclic tag system",
    8188: "Four views of a cyclic tag system",
    8192: "removing the first element from the sequence",
    8208: "Objects constructed from localized structures in rule 110",
    8230: "schematic diagram of how rule 110 can be made to emulate a cyclic tag system",
    8262: "cyclic tag systems with four different underlying rules",
    12317: "rules for the cyclic tag system on page 95 given as {{1, 1}, {1, 0}}",
    12337: "cycle through a list of more than two blocks",
    12340: "CTStep",
    12350: "Count[Flatten[rules], 1]/n-1",
    12352: "neighbor-independent substitution system",
    12354: "Thue-Morse substitution system",
    12358: "rule 110 cellular automaton",
    18514: "constructs a cyclic tag system emulating it",
    18674: "yields a specification of initial conditions in rule 110",
    18736: "blocks of lengths",
    18740: "cyclic tag system with blocks that are a multiple of 6 long",
    21068: "Cyclic tag systems, 95",
}
for line_number, fragment in guards.items():
    assert fragment in lines[line_number - 1], (line_number, fragment)
assert "emulated by rule 110, 678" in lines[21068 - 1]
assert "generalizations of, 895" in lines[21068 - 1]
assert "mechanical version of, 895" in lines[21068 - 1]


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


def ledger() -> tuple[str, int, int, int]:
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
            "C" if book_line in C else
            "O" if book_line in O else
            "R" if book_line in R else
            "X"
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
        if book_line in HASH_BOUND_NATIVE_SHA256:
            assert digest == HASH_BOUND_NATIVE_SHA256[book_line]
            assert (len(data), width, height) == NATIVE_FILE_FACTS[book_line]
        split_path, split_line = split_hits[0]
        rows.append(
            f"{book_line}|{kind}|{path.relative_to(ASSET_ROOT).as_posix()}|{len(data)}|"
            f"{width}|{height}|{digest}|"
            f"{split_path.relative_to(ASSET_ROOT).as_posix()}|{split_line}|{REASON[book_line]}"
        )

    return "\n".join(rows) + "\n", monolith_references, split_references, len(hashes)


EXPECTED_STRICT_UNIVERSE_SHA256 = "95411e9d7c6de49bdd05049d5435bf0b935a6afdcde29619b5775b2205cfe82c"
EXPECTED_STRICT_LEDGER_SHA256 = "bc91ba39ffb022ac91cdbbad2c7685523f8209de542d51a5f7d543c44f6fb488"
EXPECTED_UNIVERSE_SHA256 = "9e95aed53f7aa329a9f82567a05031e51558c0e0b978ca5eb246fb758e454838"
EXPECTED_LEDGER_SHA256 = "fa1ee814d45e3e085918627109124990635c91688655f37cbcc1ecb48e454e63"


def main() -> None:
    payload, monolith_references, split_references, hashes = ledger()
    universe_digest = hashlib.sha256(",".join(map(str, sorted(U))).encode("ascii")).hexdigest()
    ledger_digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    strict_rows = [
        row for row in payload.splitlines() if int(row.split("|", 1)[0]) in STRICT_U
    ]
    strict_payload = "\n".join(strict_rows) + "\n"
    strict_universe_digest = hashlib.sha256(
        ",".join(map(str, sorted(STRICT_U))).encode("ascii")
    ).hexdigest()
    strict_ledger_digest = hashlib.sha256(strict_payload.encode("utf-8")).hexdigest()

    assert strict_universe_digest == EXPECTED_STRICT_UNIVERSE_SHA256
    assert strict_ledger_digest == EXPECTED_STRICT_LEDGER_SHA256
    assert universe_digest == EXPECTED_UNIVERSE_SHA256
    assert ledger_digest == EXPECTED_LEDGER_SHA256
    assert len(strict_rows) == 5 and len(payload.splitlines()) == 27
    assert (monolith_references, split_references, hashes) == (27, 27, 27)
    print(
        f"T18 asset oracle: PASS source={len(S)}; C4/Q=23/4; assets=27; strict=5; "
        "classes C/O/R/X=4/1/21/1; "
        "refs=54(monolith=27,split=27); unique_hashes=27; "
        "page95_rule/seed/t0_t24=PASS; page96_rules/seeds/t0_t99=PASS; "
        "mechanical_plate_absent=PASS; page_offset=PASS; "
        "actual_Index/malformed_split_reverse=PASS"
    )


if __name__ == "__main__":
    main()
