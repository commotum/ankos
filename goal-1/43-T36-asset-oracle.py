#!/usr/bin/env python3
"""Fail-closed raster/provenance audit for T36 digit-reversal arithmetic.

The governed T36 image record is intentionally narrow: the three native main
plates, the native Notes regular-region-length plot, and the three related
fixed-width digit-reversal permutation plates.  Immediate T35/T37 boundaries,
the separate digit-count plate, and the following iterated-bitwise gallery are
an exact, physically bound adjacency-exclusion universe.

Every governed JPEG is bound to one monolith reference, one split-Markdown
reference, one physical file, exact bytes, dimensions, SHA-256, evidence role,
and assembly.  The same physical checks bind every excluded neighbor.  Pixels
do not supply a formula, seed, event count, digit convention, width policy,
trace value, palette, crop, regularity measurement, FFT permutation, or CA
lowering.  All governed assets are therefore HASH_BOUND; none is transcribed
or replayed at pixel level.
"""

from __future__ import annotations

import hashlib
import re
import runpy
import sys
from pathlib import Path
from typing import NamedTuple


if not __debug__:
    raise RuntimeError("T36 asset verification requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "ref/A-New-Kind-of-Science"
BOOK = SOURCE_ROOT / "A-New-Kind-of-Science.md"
SOURCE_ORACLE_PATH = ROOT / "goal-1/43-T36-source-oracle.py"

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
IMAGE_RE = re.compile(r"^!\[[^]]*\]\(([^)]*?\.jpeg)\)$")
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


def parse_assets(rows: str) -> dict[int, AssetSpec]:
    assets: dict[int, AssetSpec] = {}
    for row in rows.splitlines():
        fields = row.split("|", 11)
        assert len(fields) == 12, row
        line = int(fields[0])
        assert line not in assets
        assets[line] = AssetSpec(
            fields[1], fields[2], fields[3], fields[4], int(fields[5]),
            int(fields[6]), int(fields[7]), int(fields[8]), fields[9],
            fields[10], fields[11],
        )
    return assets


# Frozen governed manifest.  These are the only T36 images that contribute to
# the governed asset metrics.  Their formulas and interpretations remain text
# evidence even though the referenced files are cryptographically bound here.
ASSET_ROWS = r"""
1543|N-T36-SEED-16|_page_140_Picture_5.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_140_Picture_5.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|147|140714|607|922|4adb983dd8fa5ec5a8904cca51dec2d6fef50b3f28924784ee832e4f2d8b5d6c|-|native printed-page-125 seed-16 digit presentation; source text, not pixels, states the rule, seed, and 180-step claim
1547|N-T36-SEED-512|_page_141_Picture_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_141_Picture_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|151|359405|950|1461|2523481bae71468864a41f08ae0e0dcc1a823bfd49c5efdcc788625b00cd0fba|t36_seed_512_continuation|native printed-page-126 seed-512 presentation; source text supplies the thousand-step scope
1551|N-T36-MILLIONTH-CONTINUATION|_page_142_Picture_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_142_Picture_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|155|516673|962|1476|d304e0089d5be1c9662e1645812b78f2d900f009e7805978a142b4f1b741700e|t36_seed_512_continuation|native printed-page-127 continuation at the millionth step; crop and complete-width statement remain prose evidence
12641|N-T36-REGULAR-REGION-LENGTHS|_page_920_Figure_12.jpeg|BACK-MATTER/Index/Images/_page_920_Figure_12.jpeg|BACK-MATTER/Index/Index.md|544|13166|559|107|806545c68cad4830840650728e14b07bbab6a6de84eca6c95e83e1422f0d768a|-|native Notes plot of regular-region lengths; no values or measurement algorithm are transcribed from pixels
12654|R-T36-FIXED-WIDTH-REVERSAL-A|_page_920_Picture_20.jpeg|BACK-MATTER/Index/Images/_page_920_Picture_20.jpeg|BACK-MATTER/Index/Index.md|557|6689|184|155|2029134c9db04ce2aff0d1659a3c8a349080c727e32232e8d678111a62de4de9|t36_digit_reversal_relation_trilogy|related fixed-width digit-reversal permutation plate A; the generic k,m formula is source text
12656|R-T36-FIXED-WIDTH-REVERSAL-B|_page_920_Picture_21.jpeg|BACK-MATTER/Index/Images/_page_920_Picture_21.jpeg|BACK-MATTER/Index/Index.md|559|13053|181|153|f13f46847832eb97ca2665867c4dda09101f8f7f7448348961d702fe7fe14305|t36_digit_reversal_relation_trilogy|related fixed-width digit-reversal permutation plate B; FFT and quasi-Monte-Carlo uses remain prose relations
12658|R-T36-FIXED-WIDTH-REVERSAL-C|_page_920_Picture_22.jpeg|BACK-MATTER/Index/Images/_page_920_Picture_22.jpeg|BACK-MATTER/Index/Index.md|561|12353|184|153|5d85f1c33422576a95048a3e57e4ed1d97fb5466cd174916921fbb0b153164b1|t36_digit_reversal_relation_trilogy|related fixed-width digit-reversal permutation plate C; no iterative reversal-add semantics are inferred from the raster
""".strip()
ASSETS = parse_assets(ASSET_ROWS)

NATIVE_IMAGE_LINES = frozenset({1543, 1547, 1551, 12641})
RELATION_IMAGE_LINES = frozenset({12654, 12656, 12658})
CONTROL_IMAGE_LINES: frozenset[int] = frozenset()
GOVERNED_IMAGE_LINES = (
    NATIVE_IMAGE_LINES | RELATION_IMAGE_LINES | CONTROL_IMAGE_LINES
)
assert GOVERNED_IMAGE_LINES == frozenset(ASSETS)
assert not (
    NATIVE_IMAGE_LINES & RELATION_IMAGE_LINES
    or NATIVE_IMAGE_LINES & CONTROL_IMAGE_LINES
    or RELATION_IMAGE_LINES & CONTROL_IMAGE_LINES
)
assert (
    len(NATIVE_IMAGE_LINES), len(RELATION_IMAGE_LINES),
    len(CONTROL_IMAGE_LINES), len(GOVERNED_IMAGE_LINES),
) == (4, 3, 0, 7)
assert digest_lines(NATIVE_IMAGE_LINES) == (
    "03d88e9c3761fdc27d9d2c0890650bacd7f5184d62020c04cad2563354b081f4"
)
assert digest_lines(RELATION_IMAGE_LINES) == (
    "a988c242ab8946f7a30e9aafdb304b4557702ad8c1193bd6222f07ee5b19f734"
)
assert digest_lines(CONTROL_IMAGE_LINES) == (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)
assert digest_lines(GOVERNED_IMAGE_LINES) == (
    "cc95a793f6b1137436119dd78e15f68598326d85c0aff16e9870ec4ac2c67a5e"
)


ASSEMBLIES = {
    assembly: frozenset(
        line for line, asset in ASSETS.items() if asset.assembly == assembly
    )
    for assembly in {asset.assembly for asset in ASSETS.values()} - {"-"}
}
assert ASSEMBLIES == {
    "t36_seed_512_continuation": frozenset({1547, 1551}),
    "t36_digit_reversal_relation_trilogy": frozenset(
        {12654, 12656, 12658}
    ),
}
assert sum(map(len, ASSEMBLIES.values())) == 5


# Exact adjacency fixed point: the last T35 and first T37 main plates, the
# immediately preceding T35 Notes plate, the separate later digit-count plate,
# and the following five-image bitwise/CA gallery.  They are verified as
# physical exclusions, never silently ignored or promoted into T36 evidence.
ADJACENCY_EXCLUSIONS = {
    1523: ("_page_139_Figure_1.jpeg", "last T35 main plate before T36"),
    1565: ("_page_143_Figure_6.jpeg", "first T37 main plate after T36"),
    12633: ("_page_920_Figure_8.jpeg", "immediately preceding T35 Notes plate"),
    12674: ("_page_920_Figure_30.jpeg", "separate iterated digit-count system"),
    12678: ("_page_921_Picture_3.jpeg", "iterated bitwise/CA gallery A"),
    12680: ("_page_921_Picture_4.jpeg", "iterated bitwise/CA gallery B"),
    12682: ("_page_921_Picture_5.jpeg", "iterated bitwise/CA gallery C"),
    12684: ("_page_921_Picture_6.jpeg", "iterated bitwise/CA gallery D"),
    12686: ("_page_921_Picture_7.jpeg", "iterated bitwise/CA gallery E"),
}
EXCLUDED_IMAGE_LINES = frozenset(ADJACENCY_EXCLUSIONS)
assert GOVERNED_IMAGE_LINES.isdisjoint(EXCLUDED_IMAGE_LINES)
for excluded_line, (excluded_name, _reason) in ADJACENCY_EXCLUSIONS.items():
    assert BOOK_LINES[excluded_line - 1] == f"![]({excluded_name})"


EXCLUDED_ASSET_ROWS = r"""
1523|X-T35-SEED-SIX-LONG-RUN|_page_139_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_139_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|127|50875|1065|561|994a1ab97bc3de5aee725d3a7ad222e9c970e8b8f7c454b89b46805159795f2c|-|last T35 main plate; its piecewise integer rule is not T36 reversal-addition
1565|X-T37-RECURSIVE-BOUNDARY|_page_143_Figure_6.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_143_Figure_6.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|169|86025|1231|382|731de2a621d5b227026c1b1ac4ed488ce96afc26be0fd5fcb0495297f5ed650b|-|first T37 recursive-sequence plate after the T36 main section
12633|X-T35-REVERSIBLE-VARIANT|_page_920_Figure_8.jpeg|BACK-MATTER/Index/Images/_page_920_Figure_8.jpeg|BACK-MATTER/Index/Index.md|536|8897|593|100|99b72bc69f8a8badf8665097268dc8e021fbb53f8ae9c94de7eaeb4071179e71|-|immediately preceding T35 reversible-map Notes plate
12674|X-ITERATED-DIGIT-COUNT|_page_920_Figure_30.jpeg|BACK-MATTER/Index/Images/_page_920_Figure_30.jpeg|BACK-MATTER/Index/Index.md|577|10024|575|98|8e8c22a2c52e54c3d5ab4ae00b12f84e862a1264a532e2f35266b29b5a6d3ba0|-|separate list-growing digit-count system after the T36 relation plates
12678|X-ITERATED-BITWISE-A|_page_921_Picture_3.jpeg|BACK-MATTER/Index/Images/_page_921_Picture_3.jpeg|BACK-MATTER/Index/Index.md|581|2657|96|83|985e5d74ae6c0bbf6f3beb1554345c0af51c848889f0305de416ef093bd70481|iterated_bitwise_gallery|separate bitwise/arithmetic iteration gallery A; first example relates to CA rule 60
12680|X-ITERATED-BITWISE-B|_page_921_Picture_4.jpeg|BACK-MATTER/Index/Images/_page_921_Picture_4.jpeg|BACK-MATTER/Index/Index.md|583|2980|81|83|d9da05f6d43e78e6cb16a0ea451d8204e2f4320aaccdfe6ef2b9b157daa6749e|iterated_bitwise_gallery|separate bitwise/arithmetic iteration gallery B
12682|X-ITERATED-BITWISE-C|_page_921_Picture_5.jpeg|BACK-MATTER/Index/Images/_page_921_Picture_5.jpeg|BACK-MATTER/Index/Index.md|585|3791|133|93|5e308a461a3d1852a69750c906d5a46a0b94e264696fff6209ca414e43c58068|iterated_bitwise_gallery|separate bitwise/arithmetic iteration gallery C
12684|X-ITERATED-BITWISE-D|_page_921_Picture_6.jpeg|BACK-MATTER/Index/Images/_page_921_Picture_6.jpeg|BACK-MATTER/Index/Index.md|587|3249|114|89|b0eca5ac7ce927db9edb42807573b5a63ee9c9420a733782609612234cc565eb|iterated_bitwise_gallery|separate bitwise/arithmetic iteration gallery D
12686|X-ITERATED-BITWISE-E|_page_921_Picture_7.jpeg|BACK-MATTER/Index/Images/_page_921_Picture_7.jpeg|BACK-MATTER/Index/Index.md|589|2324|92|93|5ed00f75d880eb9a2d3aa47132e1d560a5f2997f7f7292d309b7146532adca15|iterated_bitwise_gallery|separate bitwise/arithmetic iteration gallery E before the T37 Notes heading
""".strip()
EXCLUDED_ASSETS = parse_assets(EXCLUDED_ASSET_ROWS)
assert frozenset(EXCLUDED_ASSETS) == EXCLUDED_IMAGE_LINES
for line, asset in EXCLUDED_ASSETS.items():
    assert asset.name == ADJACENCY_EXCLUSIONS[line][0]

EXCLUDED_ASSEMBLIES = {
    assembly: frozenset(
        line for line, asset in EXCLUDED_ASSETS.items()
        if asset.assembly == assembly
    )
    for assembly in {asset.assembly for asset in EXCLUDED_ASSETS.values()} - {"-"}
}
assert EXCLUDED_ASSEMBLIES == {
    "iterated_bitwise_gallery": frozenset(
        {12678, 12680, 12682, 12684, 12686}
    ),
}


SOURCE_DERIVED_CANDIDATE_GROUPS = {
    "main_T35_T36_T37_boundary": frozenset(
        {1523, 1543, 1547, 1551, 1565}
    ),
    "notes_reversal_and_immediate_boundaries": frozenset(
        {12633, 12641, 12654, 12656, 12658, 12674}
    ),
    "following_iterated_bitwise_gallery": frozenset(
        {12678, 12680, 12682, 12684, 12686}
    ),
}
CANDIDATE_IMAGE_LINES = frozenset().union(
    *SOURCE_DERIVED_CANDIDATE_GROUPS.values()
)
assert sum(map(len, SOURCE_DERIVED_CANDIDATE_GROUPS.values())) == len(
    CANDIDATE_IMAGE_LINES
)
assert all(line in BOOK_IMAGES for line in CANDIDATE_IMAGE_LINES)
UNRESOLVED_IMAGE_LINES: frozenset[int] = frozenset()
assert CANDIDATE_IMAGE_LINES == GOVERNED_IMAGE_LINES | EXCLUDED_IMAGE_LINES
assert len(CANDIDATE_IMAGE_LINES) == 16
assert digest_lines(EXCLUDED_IMAGE_LINES) == (
    "72aa6b7545f1896ba5ee090fcb050c5d378e2c90898d49c6b3373811ded93689"
)
assert digest_lines(CANDIDATE_IMAGE_LINES) == (
    "908f2831353adf6c52b599bd62f8de7971b2f99637c66a041a232a2ca1faa7c0"
)


CLASSIFICATION = {
    **{line: "N" for line in NATIVE_IMAGE_LINES},
    **{line: "R" for line in RELATION_IMAGE_LINES},
    **{line: "C" for line in CONTROL_IMAGE_LINES},
    **{line: "X" for line in EXCLUDED_IMAGE_LINES},
}
assert frozenset(CLASSIFICATION) == CANDIDATE_IMAGE_LINES
assert tuple(CLASSIFICATION.values()).count("N") == 4
assert tuple(CLASSIFICATION.values()).count("R") == 3
assert tuple(CLASSIFICATION.values()).count("C") == 0
assert tuple(CLASSIFICATION.values()).count("X") == 9


HASH_BOUND = GOVERNED_IMAGE_LINES
LIMITED_TRANSCRIBED: frozenset[int] = frozenset()
PIXEL_REPLAYED: frozenset[int] = frozenset()
assert LIMITED_TRANSCRIBED <= HASH_BOUND
assert PIXEL_REPLAYED <= LIMITED_TRANSCRIBED
assert (len(HASH_BOUND), len(LIMITED_TRANSCRIBED), len(PIXEL_REPLAYED)) == (
    7, 0, 0,
)


UNRECOVERED_RASTER_SEMANTICS = frozenset(
    {
        "exact cell rows, complete scalar traces, and unprinted intermediate values",
        "digit order, leading-zero policy, alignment, padding, crop, and complete width",
        "palette, JPEG threshold, resampling, grid geometry, and display orientation",
        "regular-region segmentation, lengths, effective-period equivalence, and fit method",
        "fixed-width and grow-left update mechanics beyond the explicit Notes prose",
        "FFT, Halton, van-der-Corput, and quasi-Monte-Carlo algorithms beyond stated relations",
        "a digit-local CA rule, carry propagation schedule, compiler, or stroboscopic timing",
        "any callback, family dispatch, hidden width, observer feedback, or T36 executor",
    }
)
assert len(UNRECOVERED_RASTER_SEMANTICS) == 8


SOURCE_DERIVED_NOT_PIXEL_TRANSCRIBED = frozenset(
    {
        "base-2 reverse-then-add formula and positive seeds 16 and 512",
        "180-step, thousand-step, millionth-step, and 568418-bit source claims",
        "fixed-width drop-carry and grow-one-left-digit Notes variants",
        "generic fixed-width base-k digit-reversal permutation formula",
        "FFT and quasi-Monte-Carlo relations and historical attribution",
    }
)
assert len(SOURCE_DERIVED_NOT_PIXEL_TRANSCRIBED) == 5


SOURCE_GUARDS = {
    1525: "starting from the value 6",
    1545: "write its base 2 digits in reverse order",
    1549: "starting with the number 512",
    1553: "starting at the millionth step",
    1567: "Examples of some simple recursive sequences",
    12631: "backward and forward evolution from n = 8",
    12635: "Reversal-addition systems",
    12637: "Reverse[Integer Digits[n, 2]]",
    12639: "568418 base 2 digits",
    12643: "digit sequence of fixed length",
    12646: "Digit reversal",
    12650: "IntegerDigits[n, k, m]",
    12652: "fast Fourier transform",
    12668: "Digit count sequences",
    12676: "Iterated bitwise operations",
    12688: "Recursive Sequences",
}
for source_line, fragment in SOURCE_GUARDS.items():
    assert fragment in BOOK_LINES[source_line - 1], (source_line, fragment)


def jpeg_size(data: bytes) -> tuple[int, int]:
    """Read a JPEG SOF marker without an image-library dependency."""

    assert data[:2] == b"\xff\xd8"
    sof = {
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
        segment_size = int.from_bytes(data[offset : offset + 2], "big")
        assert segment_size >= 2
        if marker in sof:
            width = int.from_bytes(data[offset + 5 : offset + 7], "big")
            height = int.from_bytes(data[offset + 3 : offset + 5], "big")
            return width, height
        offset += segment_size
    raise AssertionError("JPEG SOF marker not found")


def verify_asset_bytes(book_line: int, asset: AssetSpec, data: bytes) -> str:
    """Verify one frozen file record; exposed for hostile mutation checks."""

    assert len(data) == asset.byte_length, (book_line, len(data), asset.byte_length)
    assert jpeg_size(data) == (asset.width, asset.height), book_line
    digest = sha256(data)
    assert digest == asset.digest, (book_line, digest, asset.digest)
    return digest


def load_source_oracle() -> dict[str, object]:
    """Load the independent source audit without depending on caller cwd."""

    assert SOURCE_ORACLE_PATH.is_file(), "T36 source oracle is not frozen"
    return runpy.run_path(
        str(SOURCE_ORACLE_PATH), run_name="t36_source_oracle_asset_interface"
    )


def verify_source_interface() -> None:
    """Bind the source audit's final source-owned image partition exactly."""

    source = load_source_oracle()
    required = {
        "NATIVE_IMAGE_LINES": NATIVE_IMAGE_LINES,
        "RELATION_IMAGE_LINES": RELATION_IMAGE_LINES,
        "CONTROL_IMAGE_LINES": CONTROL_IMAGE_LINES,
        "GOVERNED_IMAGE_LINES": GOVERNED_IMAGE_LINES,
        "EXCLUDED_IMAGE_LINES": EXCLUDED_IMAGE_LINES,
        "CANDIDATE_IMAGE_LINES": CANDIDATE_IMAGE_LINES,
        "UNRESOLVED_IMAGE_LINES": UNRESOLVED_IMAGE_LINES,
    }
    for attribute, expected in required.items():
        actual = frozenset(source[attribute])
        assert actual == expected, (attribute, sorted(actual), sorted(expected))

    expected_partition = {
        "native": (len(NATIVE_IMAGE_LINES), digest_lines(NATIVE_IMAGE_LINES)),
        "relation": (
            len(RELATION_IMAGE_LINES), digest_lines(RELATION_IMAGE_LINES)
        ),
        "control": (len(CONTROL_IMAGE_LINES), digest_lines(CONTROL_IMAGE_LINES)),
    }
    assert source["EXPECTED_IMAGE_PARTITION"] == expected_partition
    expected_ledger = {
        "candidate_images": (
            len(CANDIDATE_IMAGE_LINES), digest_lines(CANDIDATE_IMAGE_LINES)
        ),
        "governed_images": (
            len(GOVERNED_IMAGE_LINES), digest_lines(GOVERNED_IMAGE_LINES)
        ),
        "excluded_images": (
            len(EXCLUDED_IMAGE_LINES), digest_lines(EXCLUDED_IMAGE_LINES)
        ),
    }
    assert source["EXPECTED_IMAGE_LEDGER"] == expected_ledger


def ledger() -> tuple[str, str, int, int, int, int, int, int, int, int]:
    """Verify governed and excluded assets and return canonical ledgers."""

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
        kind = CLASSIFICATION[book_line]
        assert kind in {"N", "R", "C"}
        assert asset.role.startswith(f"{kind}-")
        assert BOOK_LINES[book_line - 1] == f"![]({asset.name})"
        assert monolith_by_name.get(asset.name) == [book_line]

        expected_split = SOURCE_ROOT / asset.split_markdown
        split_hits = split_by_name.get(asset.name, [])
        assert split_hits == [(expected_split, asset.split_line)], (
            book_line, split_hits,
        )
        expected_physical = SOURCE_ROOT / asset.physical
        physical_hits = physical_by_name.get(asset.name, [])
        assert physical_hits == [expected_physical], (book_line, physical_hits)

        digest = verify_asset_bytes(book_line, asset, expected_physical.read_bytes())
        assert digest not in hashes, (book_line, digest)
        hashes.add(digest)
        total_bytes += asset.byte_length
        monolith_references += 1
        split_references += 1
        rows.append(
            "|".join(
                (
                    str(book_line), kind, asset.role, asset.physical,
                    str(asset.byte_length), str(asset.width), str(asset.height),
                    asset.digest, asset.split_markdown, str(asset.split_line),
                    asset.assembly, asset.boundary,
                )
            )
        )

    excluded_rows: list[str] = []
    excluded_hashes: set[str] = set()
    excluded_bytes = 0
    excluded_monolith_references = 0
    excluded_split_references = 0
    for book_line, asset in sorted(EXCLUDED_ASSETS.items()):
        assert CLASSIFICATION[book_line] == "X"
        assert asset.role.startswith("X-")
        assert BOOK_LINES[book_line - 1] == f"![]({asset.name})"
        assert monolith_by_name.get(asset.name) == [book_line]

        expected_split = SOURCE_ROOT / asset.split_markdown
        split_hits = split_by_name.get(asset.name, [])
        assert split_hits == [(expected_split, asset.split_line)]
        expected_physical = SOURCE_ROOT / asset.physical
        physical_hits = physical_by_name.get(asset.name, [])
        assert physical_hits == [expected_physical]

        digest = verify_asset_bytes(book_line, asset, expected_physical.read_bytes())
        assert digest not in hashes and digest not in excluded_hashes
        excluded_hashes.add(digest)
        excluded_bytes += asset.byte_length
        excluded_monolith_references += 1
        excluded_split_references += 1
        excluded_rows.append(
            "|".join(
                (
                    str(book_line), "X", asset.role, asset.physical,
                    str(asset.byte_length), str(asset.width), str(asset.height),
                    asset.digest, asset.split_markdown, str(asset.split_line),
                    asset.assembly, asset.boundary,
                )
            )
        )

    return (
        "\n".join(rows) + "\n", "\n".join(excluded_rows) + "\n",
        monolith_references, split_references, len(hashes), total_bytes,
        excluded_monolith_references, excluded_split_references,
        len(excluded_hashes), excluded_bytes,
    )


# Frozen after the canonical ledger was independently regenerated from the
# exact manifests above.  No bypass sentinel is accepted.
EXPECTED_LEDGER_SHA256 = (
    "bace783750e95440b030b76110c86191e73bdac053bd0404a269d9f6ddebe9f1"
)
EXPECTED_EXCLUDED_LEDGER_SHA256 = (
    "7da1a0cc0bb03e39c6cfa18bca8e4fc12ab151e6b0d6c05ac6f3ee32c5d2efe6"
)


def main() -> None:
    if len(sys.argv) != 1:
        raise SystemExit("usage: 43-T36-asset-oracle.py")
    verify_source_interface()
    (
        payload, excluded_payload,
        monolith_refs, split_refs, hashes, total_bytes,
        excluded_monolith_refs, excluded_split_refs,
        excluded_hashes, excluded_bytes,
    ) = ledger()
    ledger_digest = sha256(payload.encode("utf-8"))
    excluded_ledger_digest = sha256(excluded_payload.encode("utf-8"))
    assert ledger_digest == EXPECTED_LEDGER_SHA256, (
        "ledger", ledger_digest, EXPECTED_LEDGER_SHA256,
    )
    assert excluded_ledger_digest == EXPECTED_EXCLUDED_LEDGER_SHA256, (
        "excluded ledger", excluded_ledger_digest,
        EXPECTED_EXCLUDED_LEDGER_SHA256,
    )
    assert (monolith_refs, split_refs, hashes, total_bytes) == (
        7, 7, 7, 1_062_053,
    )
    assert (
        excluded_monolith_refs, excluded_split_refs,
        excluded_hashes, excluded_bytes,
    ) == (9, 9, 9, 170_822)
    print(
        "T36 asset oracle: PASS governed=7; classes N/R/C=4/3/0; "
        "candidates=16; excluded=9; refs=14(monolith=7,split=7); "
        "unique_hashes=7; bytes=1062053; assemblies=2/5_files; "
        "excluded_bound=9/18_refs/9_hashes/170822_bytes/1_assembly/5_files; "
        "boundary=7_HASH_BOUND/0_LIMITED_TRANSCRIBED/0_PIXEL_REPLAYED; "
        "formulas/seeds/traces/palettes/crops=source_text_only_or_unrecovered; "
        "unresolved_image_dispositions=0"
    )


if __name__ == "__main__":
    main()
