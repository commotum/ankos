#!/usr/bin/env python3
"""Fail-closed raster/provenance audit for T42 CF-driven substitutions.

The closed T42 raster universe contains one native page-162 plate and eleven
text-backed relation plates: the page-903 fractional-orbit observer, five
page-916 digital-slope panels, and five page-971 billiards panels.  Every
asset is bound to its monolith and split-Markdown references, unique physical
file, byte length, baseline-JFIF/RGB profile, dimensions, and SHA-256 digest.

All twelve assets are HASH_BOUND.  The native page-162 plate is additionally
LIMITED_TRANSCRIBED: its four displayed function labels, visible execution-
order coefficient rows, rule-icon labels, and black/gray convention are manual
fixture evidence.  The page-903 text independently supplies the executable
rho formula, so no geometry, window, coefficient evaluator, or hidden program
is inferred from pixels.  The exact trace replay combines that formula with
the frozen transcription manifest.  Relation images remain observers, not
transition state or rule tables.
"""

from __future__ import annotations

import hashlib
import json
import re
import runpy
import sys
from pathlib import Path
from typing import NamedTuple


if not __debug__:
    raise RuntimeError("T42 asset verification requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "ref/A-New-Kind-of-Science"
BOOK = SOURCE_ROOT / "A-New-Kind-of-Science.md"
SOURCE_ORACLE_PATH = ROOT / "goal-1/46-T42-source-oracle.py"
SEMANTIC_ORACLE_PATH = ROOT / "goal-1/46-T42-semantic-oracle.py"

EXPECTED_BOOK_LINES = 22_498
EXPECTED_BOOK_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"
EXPECTED_SEMANTIC_ORACLE_SHA256 = (
    "cd7daf5c293fa55a3a4972c1ebcaae4b9eccbc0ff704a1e4f45fe2ca2936ffcb"
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_lines(values: set[int] | frozenset[int]) -> str:
    return sha256(",".join(map(str, sorted(values))).encode("ascii"))


def digest_records(values: set[str] | frozenset[str]) -> str:
    """Hash an unordered record set with length-delimited UTF-8 framing."""

    payload = bytearray()
    for value in sorted(values):
        encoded = value.encode("utf-8")
        payload.extend(len(encoded).to_bytes(8, "big"))
        payload.extend(encoded)
    return sha256(bytes(payload))


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
    decoded_mode: str
    components: int
    digest: str
    assembly: str
    boundary: str
    reason: str


def parse_assets(rows: str) -> dict[int, AssetSpec]:
    assets: dict[int, AssetSpec] = {}
    for row in rows.strip().splitlines():
        fields = row.split("|", 14)
        assert len(fields) == 15, row
        line = int(fields[0])
        assert line not in assets
        assets[line] = AssetSpec(
            fields[1], fields[2], fields[3], fields[4], int(fields[5]),
            int(fields[6]), int(fields[7]), int(fields[8]), fields[9],
            int(fields[10]), fields[11], fields[12], fields[13], fields[14],
        )
    return assets


ASSET_ROWS = r"""
1854|N-page162-cf-driven-substitution|_page_162_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_162_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|313|206693|1050|1155|RGB|3|ab5e7bbab2a14b3d4fb832dad43842ceb4f206653810d7dfcd23238095741cfe|-|LIMITED_TRANSCRIBED|native four-profile substitution and axis-crossing plate; displayed functions, coefficient rows, icon labels, and black/gray convention are manual fixture transcription, while executable rho mechanics come from text
12583|R-page903-fractional-orbit-observer|_page_918_Figure_16.jpeg|BACK-MATTER/Index/Images/_page_918_Figure_16.jpeg|BACK-MATTER/Index/Index.md|486|29780|565|165|RGB|3|063be8f26ae1d13f7c97292b30d845cc67552027aef4964c99f4e44d9254fae6|-|HASH_BOUND|related Mod[h n,1] observer immediately preceding the exact mechanical-word substitution construction
13119|R-page916-digital-slope-a|_page_931_Figure_9.jpeg|BACK-MATTER/Index/Images/_page_931_Figure_9.jpeg|BACK-MATTER/Index/Index.md|1022|6165|120|158|RGB|3|bb11803238dda52fd8f63a292f7f2d96a4d7a75cfdbfe159cb190ff64916d0ca|page916-digital-slope-five|HASH_BOUND|digital-slope relation A; source text supplies the mechanical differences and CF relation
13121|R-page916-digital-slope-b|_page_931_Figure_10.jpeg|BACK-MATTER/Index/Images/_page_931_Figure_10.jpeg|BACK-MATTER/Index/Index.md|1024|6840|122|147|RGB|3|2282818d058f61cf1e511c3a87d944bdabdd49c95a76a82e158f5dcc9007338c|page916-digital-slope-five|HASH_BOUND|digital-slope relation B; source text supplies the mechanical differences and CF relation
13123|R-page916-digital-slope-c|_page_931_Figure_11.jpeg|BACK-MATTER/Index/Images/_page_931_Figure_11.jpeg|BACK-MATTER/Index/Index.md|1026|5429|103|161|RGB|3|e80bdf6b9e562f086ce6efb205dce5dd6a3200d383971e3883cda4dc74eabbb2|page916-digital-slope-five|HASH_BOUND|digital-slope relation C; source text supplies the mechanical differences and CF relation
13125|R-page916-digital-slope-d|_page_931_Figure_12.jpeg|BACK-MATTER/Index/Images/_page_931_Figure_12.jpeg|BACK-MATTER/Index/Index.md|1028|6192|110|155|RGB|3|d4cd35ac79902f539674d4114bba8bd7a12a1674ef334903028ebcd9f1a260e8|page916-digital-slope-five|HASH_BOUND|digital-slope relation D; source text supplies the mechanical differences and CF relation
13127|R-page916-digital-slope-e|_page_931_Figure_13.jpeg|BACK-MATTER/Index/Images/_page_931_Figure_13.jpeg|BACK-MATTER/Index/Index.md|1030|3562|75|155|RGB|3|66c9d76cf184c965d21af617adbf5c87b8a6d88632494eb5be39b46386dc5b95|page916-digital-slope-five|HASH_BOUND|digital-slope relation E; source text supplies the mechanical differences and CF relation
14925|R-page971-billiards-a|_page_986_Picture_4.jpeg|BACK-MATTER/Index/Images/_page_986_Picture_4.jpeg|BACK-MATTER/Index/Index.md|2826|2185|118|99|RGB|3|dce3420f6ab4b0cda93c35df05fc0f1af1477889fcf988251894fd4c53e94a2f|page971-billiards-five|HASH_BOUND|billiard relation A; prose relates the side itinerary to slope continued fractions and page-903 substitutions
14927|R-page971-billiards-b|_page_986_Picture_5.jpeg|BACK-MATTER/Index/Images/_page_986_Picture_5.jpeg|BACK-MATTER/Index/Index.md|2828|2449|93|92|RGB|3|0cf2cee6cf4e44d42f09a4116cfd09a5e622fc9799901fcf05cc4a744a17cfe6|page971-billiards-five|HASH_BOUND|billiard relation B; no itinerary or slope is transcribed from pixels
14929|R-page971-billiards-c|_page_986_Picture_6.jpeg|BACK-MATTER/Index/Images/_page_986_Picture_6.jpeg|BACK-MATTER/Index/Index.md|2830|4105|99|103|RGB|3|91ccba8bb1c4a855376d1573507072af4ae310e06aaeb751e4a4de912f518234|page971-billiards-five|HASH_BOUND|billiard relation C; no itinerary or slope is transcribed from pixels
14931|R-page971-billiards-d|_page_986_Picture_7.jpeg|BACK-MATTER/Index/Images/_page_986_Picture_7.jpeg|BACK-MATTER/Index/Index.md|2832|5402|92|96|RGB|3|5d4ced55b1fed2900320f0f2d61df6dc43e63339726c33bb1bcef528e0497608|page971-billiards-five|HASH_BOUND|billiard relation D; no itinerary or slope is transcribed from pixels
14933|R-page971-billiards-e|_page_986_Picture_8.jpeg|BACK-MATTER/Index/Images/_page_986_Picture_8.jpeg|BACK-MATTER/Index/Index.md|2834|6253|102|111|RGB|3|a1983299e03d94a78d251a7116ede9184b32a24bf8e9f9a0402cd18420749b7f|page971-billiards-five|HASH_BOUND|billiard relation E; no itinerary or slope is transcribed from pixels
"""

ASSETS = parse_assets(ASSET_ROWS)

NATIVE_IMAGE_LINES = frozenset({1854})
RELATION_IMAGE_LINES = frozenset({
    12583,
    13119, 13121, 13123, 13125, 13127,
    14925, 14927, 14929, 14931, 14933,
})
CONTROL_IMAGE_LINES: frozenset[int] = frozenset()
GOVERNED_IMAGE_LINES = (
    NATIVE_IMAGE_LINES | RELATION_IMAGE_LINES | CONTROL_IMAGE_LINES
)
EXCLUDED_IMAGE_LINES: frozenset[int] = frozenset()
CANDIDATE_IMAGE_LINES = GOVERNED_IMAGE_LINES
UNRESOLVED_IMAGE_LINES: frozenset[int] = frozenset()

assert GOVERNED_IMAGE_LINES == frozenset(ASSETS)
assert not (
    NATIVE_IMAGE_LINES & RELATION_IMAGE_LINES
    or NATIVE_IMAGE_LINES & CONTROL_IMAGE_LINES
    or RELATION_IMAGE_LINES & CONTROL_IMAGE_LINES
)
assert (
    len(NATIVE_IMAGE_LINES), len(RELATION_IMAGE_LINES),
    len(CONTROL_IMAGE_LINES), len(GOVERNED_IMAGE_LINES),
) == (1, 11, 0, 12)


EXPECTED_IMAGE_ROLE_PARTITION = {
    "native": (len(NATIVE_IMAGE_LINES), digest_lines(NATIVE_IMAGE_LINES)),
    "relation": (len(RELATION_IMAGE_LINES), digest_lines(RELATION_IMAGE_LINES)),
    "control": (len(CONTROL_IMAGE_LINES), digest_lines(CONTROL_IMAGE_LINES)),
}
EXPECTED_IMAGE_LEDGER = {
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


SOURCE_DERIVED_CANDIDATE_SCOPES = {
    "strict-page162-T42-clauses": (1850, 1858, frozenset({1854})),
    "page903-mechanical-sequence-and-rules": (
        12581, 12595, frozenset({12583})
    ),
    "page916-digital-slope-assembly": (
        13111, 13129, frozenset({13119, 13121, 13123, 13125, 13127})
    ),
    "page971-billiards-assembly": (
        14923, 14935, frozenset({14925, 14927, 14929, 14931, 14933})
    ),
}
assert frozenset().union(
    *(scope[2] for scope in SOURCE_DERIVED_CANDIDATE_SCOPES.values())
) == CANDIDATE_IMAGE_LINES


CLASSIFICATION = {
    **{line: "N" for line in NATIVE_IMAGE_LINES},
    **{line: "R" for line in RELATION_IMAGE_LINES},
    **{line: "C" for line in CONTROL_IMAGE_LINES},
    **{line: "X" for line in EXCLUDED_IMAGE_LINES},
}
assert frozenset(CLASSIFICATION) == CANDIDATE_IMAGE_LINES


ASSEMBLIES = {
    "page916-digital-slope-five": frozenset(
        {13119, 13121, 13123, 13125, 13127}
    ),
    "page971-billiards-five": frozenset(
        {14925, 14927, 14929, 14931, 14933}
    ),
}
assert all(
    frozenset(line for line, asset in ASSETS.items() if asset.assembly == name)
    == lines
    for name, lines in ASSEMBLIES.items()
)
assert sum(map(len, ASSEMBLIES.values())) == 10


HASH_BOUND_IMAGE_LINES = GOVERNED_IMAGE_LINES
LIMITED_TRANSCRIBED_IMAGE_LINES = frozenset(
    line for line, asset in ASSETS.items()
    if asset.boundary == "LIMITED_TRANSCRIBED"
)
PIXEL_REPLAYED_IMAGE_LINES: frozenset[int] = frozenset()
assert {asset.boundary for asset in ASSETS.values()} == {
    "HASH_BOUND", "LIMITED_TRANSCRIBED",
}
assert LIMITED_TRANSCRIBED_IMAGE_LINES == frozenset({1854})
assert PIXEL_REPLAYED_IMAGE_LINES <= LIMITED_TRANSCRIBED_IMAGE_LINES
assert LIMITED_TRANSCRIBED_IMAGE_LINES <= HASH_BOUND_IMAGE_LINES
assert (
    len(HASH_BOUND_IMAGE_LINES), len(LIMITED_TRANSCRIBED_IMAGE_LINES),
    len(PIXEL_REPLAYED_IMAGE_LINES),
) == (12, 1, 0)


SOURCE_GUARDS = frozenset({
    "1850|rule at each step|term in the continued fraction representation",
    "1856|pattern of axis crossings|generalized substitution system|successive terms in each continued fraction",
    "1858|more than two sine functions|no longer seems to be any particular connection",
    "12581|successive multiples *Mod[h n, 1]*|positions of a particle bouncing",
    "12587|Relation to substitution systems|Floor[(n+1)h] - Floor[nh]|first m rules",
    "12589|Reverse|Rest|ContinuedFraction",
    "12591|Floor[h] + Fold|{0}|rules",
    "12595|neighbor-independent substitution system|GoldenRatio|sqrt{2}|sqrt{3}",
    "13111|Digital slope representation|Floor[nh] - Floor[(n-1)h]|substitution rules derived",
    "13170|Cos[ax] - Cos[bx]|number of zeros|Floor[(n+1)#] - Floor[n#]",
    "13172|sequence of substitution rules|-1/2 is inserted",
    "14923|Billiards|continued fraction form|related to substitution systems",
})


ROLE_RECORDS = frozenset(
    f"{line}|{asset.role}|{asset.assembly}|{asset.reason}"
    for line, asset in ASSETS.items()
)


CANDIDATE_SCOPE_RECORDS = frozenset(
    f"{name}|{start}|{end}|{','.join(map(str, sorted(lines)))}"
    for name, (start, end, lines) in SOURCE_DERIVED_CANDIDATE_SCOPES.items()
)


RASTER_BOUNDARY_RECORDS = frozenset({
    "boundary|12-HASH_BOUND|1-LIMITED_TRANSCRIBED|0-PIXEL_REPLAYED",
    "raster-limited-transcription|BOOK1854 supplies four displayed function labels execution-order coefficient rows rule-icon labels and black-gray convention only",
    "raster-nonauthority|no executable rho formula geometry window coefficient evaluator hidden program curve sample line slope or billiard itinerary comes from pixels",
    "native-replay-authority|BOOK12587-12591 rho rule text plus frozen limited-transcription semantic manifest",
    "page918|fractional-orbit observer relation not T42 configuration",
    "page916|digital-slope renderings are observer relations not rule tables",
    "page971|billiard trajectories are relation renderings not substitution state",
    "image-profile|baseline JFIF 1.01 density 1x1 8-bit 3-component decoded RGB",
    "architecture|no raster program callback executor family dispatch hidden state or new UPDATE",
})


REFERENCE_RECORDS = frozenset({
    "monolith|12|one-reference-per-file",
    "split|12|one-reference-per-file",
    "total-source-references|24",
    "physical-files|12|unique-names-paths-and-hashes",
    "total-bytes|285055",
    "assemblies|2|10-files",
    "roles|N=1|R=11|C=0|X=0",
    "candidates|12|governed=12|excluded=0|unresolved=0",
})


TRACE_MECHANICS_RECORDS = frozenset({
    "orientation|natural CF prefix (a0,a1,...)->Reverse(Rest(...)) exactly once",
    "rule-zero|rho_a(0)=0^(a-1)1",
    "rule-one|rho_a(1)=0^(a-1)10",
    "seed|one zero symbol",
    "event|all old occurrences fire from one snapshot and child blocks concatenate in source order",
    "completion|m-term irrational prefix yields m-1 coefficient events",
    "offset|Floor[h] is observer output and not substitution state",
    "fixture-authority|frozen limited transcription of BOOK1854 labels and schedules combined with independent BOOK12587-12591 rho mechanics",
})


EXPECTED_MANIFEST_DIGESTS = {
    "source_guards": "3af61ce1ed64445420d669e1e6c0b64d974ff3e68efc1ece419e653dfefdd95b",
    "roles": "f92ff60ec74cb037d48e95382b95297d875b3073461a1460f3de25eacef872dc",
    "candidate_scopes": "c49cb99f7d8ccd9f620c8e8dcaa08692ac488222f8a2ca4d6e42222f89cb2253",
    "raster_boundary": "76ab1731b97b0869281b1f04c48a002de1044d20f36c1efd33d094e16ae44ca6",
    "references": "9c6e64eee50e68fe0e6b4cab8951a3ac682a48b9872958c74ddc79e851f186dc",
    "trace_mechanics": "65e392445d70f18836da277e9e12017aa90b93255de34286d51e48b818ff39ab",
}


EXPECTED_ASSET_SEMANTIC_MANIFEST = (
    ("schema", "T42-page162-semantic-interface/v1"),
    (
        "asset",
        (
            "_page_162_Figure_1.jpeg",
            206693,
            1050,
            1155,
            "ab5e7bbab2a14b3d4fb832dad43842ceb4f206653810d7dfcd23238095741cfe",
        ),
    ),
    ("gray_value", 0),
    ("black_value", 1),
    ("rule_icon_coefficients", (1, 2, 3, 4, 5)),
    ("smallest_execution_lowering", "uniform_PhaseIndex_times_Bit_word"),
    (
        "fixtures",
        (
            (
                "page162-alpha-1-plus-sqrt2",
                (0, 2, 2, 2, 2, 2),
                (2, 2, 2, 2, 2),
                (1, 2, 5, 12, 29, 70),
                "8ba86691662b9853053af6dd5b5e3dfc17caf43a640b2bbb45c01e323c30bff7",
                "LIMITED_TRANSCRIBED",
            ),
            (
                "page162-alpha-2-plus-sqrt5",
                (0, 1, 1, 1, 1, 1, 1, 1, 1, 1),
                (1, 1, 1, 1, 1, 1, 1, 1, 1),
                (1, 1, 2, 3, 5, 8, 13, 21, 34, 55),
                "fa947b9859783d29be2ba4015183fa85b52cb6181e04eab41658ab55f6761e36",
                "LIMITED_TRANSCRIBED",
            ),
            (
                "page162-alpha-2-plus-cuberoot5",
                (0, 1, 1, 2, 1, 4, 2),
                (2, 4, 1, 2, 1, 1),
                (1, 2, 9, 11, 31, 42, 73),
                "f851acd68816def8a87c81de3358a129a1a735b2a42399485966261962eb6aa5",
                "LIMITED_TRANSCRIBED",
            ),
            (
                "page162-alpha-1-plus-sqrt-e",
                (0, 2, 4, 1, 2, 3),
                (3, 2, 1, 4, 2),
                (1, 3, 7, 10, 47, 104),
                "961704a7ac5de6ac75aff0bee33c2a0d8406c9db80ed91043595d453cb4f76b6",
                "LIMITED_TRANSCRIBED",
            ),
        ),
    ),
    ("fixture_coefficient_evidence", "LIMITED_TRANSCRIBED"),
    ("pixel_replayed", False),
    ("pixel_program_forbidden", True),
)


EXPECTED_ASSET_SEMANTIC_MANIFEST_SHA256 = (
    "a29095461ff79de0d08ebd5d2347a5c0edd8ff3151363264ff2fe61892a88556"
)


def verify_semantic_manifests() -> None:
    manifests = {
        "source_guards": SOURCE_GUARDS,
        "roles": ROLE_RECORDS,
        "candidate_scopes": CANDIDATE_SCOPE_RECORDS,
        "raster_boundary": RASTER_BOUNDARY_RECORDS,
        "references": REFERENCE_RECORDS,
        "trace_mechanics": TRACE_MECHANICS_RECORDS,
    }
    for name, records in manifests.items():
        assert records and len(records) == len(set(records))
        actual = digest_records(records)
        expected = EXPECTED_MANIFEST_DIGESTS[name]
        assert actual == expected, (name, actual, expected)

    payload = json.dumps(
        EXPECTED_ASSET_SEMANTIC_MANIFEST,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    actual = sha256(payload)
    assert actual == EXPECTED_ASSET_SEMANTIC_MANIFEST_SHA256, (
        actual, EXPECTED_ASSET_SEMANTIC_MANIFEST_SHA256,
    )


def verify_source_guards_and_candidate_closure() -> None:
    for record in SOURCE_GUARDS:
        fields = record.split("|")
        line = int(fields[0])
        text = BOOK_LINES[line - 1]
        for needle in fields[1:]:
            assert needle in text, (line, needle)

    actual_union: set[int] = set()
    for name, (start, end, expected) in SOURCE_DERIVED_CANDIDATE_SCOPES.items():
        actual = frozenset(
            line for line in BOOK_IMAGES if start <= line <= end
        )
        assert actual == expected, (name, sorted(actual), sorted(expected))
        assert actual_union.isdisjoint(actual), name
        actual_union.update(actual)
    assert frozenset(actual_union) == CANDIDATE_IMAGE_LINES
    assert CANDIDATE_IMAGE_LINES == (
        GOVERNED_IMAGE_LINES | EXCLUDED_IMAGE_LINES | UNRESOLVED_IMAGE_LINES
    )


def jpeg_profile(data: bytes) -> tuple[int, int, str, int]:
    """Verify baseline JFIF metadata and return dimensions/mode/components."""

    assert data[:2] == b"\xff\xd8" and data[-2:] == b"\xff\xd9"
    assert data[2:4] == b"\xff\xe0"
    assert int.from_bytes(data[4:6], "big") == 16
    assert data[6:11] == b"JFIF\x00"
    assert data[11:13] == b"\x01\x01"
    assert data[13] == 0
    assert int.from_bytes(data[14:16], "big") == 1
    assert int.from_bytes(data[16:18], "big") == 1
    assert data[18:20] == b"\x00\x00"

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
        if marker == 0xDA:
            break
        segment_size = int.from_bytes(data[offset:offset + 2], "big")
        assert segment_size >= 2 and offset + segment_size <= len(data)
        if marker == 0xC0:
            assert data[offset + 2] == 8
            height = int.from_bytes(data[offset + 3:offset + 5], "big")
            width = int.from_bytes(data[offset + 5:offset + 7], "big")
            components = data[offset + 7]
            assert components == 3
            component_ids = tuple(
                data[offset + 8 + 3 * index] for index in range(components)
            )
            assert component_ids == (1, 2, 3)
            return width, height, "RGB", components
        assert marker not in {
            0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
            0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
        }
        offset += segment_size
    raise AssertionError("baseline JPEG SOF marker not found")


def verify_asset_bytes(book_line: int, asset: AssetSpec, data: bytes) -> str:
    """Verify a frozen asset record; exposed for hostile mutation tests."""

    assert len(data) == asset.byte_length, (book_line, len(data), asset.byte_length)
    assert jpeg_profile(data) == (
        asset.width, asset.height, asset.decoded_mode, asset.components
    ), book_line
    digest = sha256(data)
    assert digest == asset.digest, (book_line, digest, asset.digest)
    return digest


def load_source_oracle() -> dict[str, object]:
    assert SOURCE_ORACLE_PATH.is_file(), "T42 source oracle is not frozen"
    return runpy.run_path(
        str(SOURCE_ORACLE_PATH), run_name="t42_source_for_asset_interface"
    )


def verify_source_interface() -> None:
    """Bind the independent source audit's exact image partition."""

    source = load_source_oracle()
    required = {
        "NATIVE_IMAGE_LINES": NATIVE_IMAGE_LINES,
        "RELATION_IMAGE_LINES": RELATION_IMAGE_LINES,
        "CONTROL_IMAGE_LINES": CONTROL_IMAGE_LINES,
        "GOVERNED_IMAGE_LINES": GOVERNED_IMAGE_LINES,
        "EXCLUDED_IMAGE_LINES": EXCLUDED_IMAGE_LINES,
        "CANDIDATE_IMAGE_LINES": CANDIDATE_IMAGE_LINES,
        "UNRESOLVED_IMAGE_LINES": UNRESOLVED_IMAGE_LINES,
        "HASH_BOUND_IMAGE_LINES": HASH_BOUND_IMAGE_LINES,
        "LIMITED_TRANSCRIBED_IMAGE_LINES": LIMITED_TRANSCRIBED_IMAGE_LINES,
        "PIXEL_REPLAYED_IMAGE_LINES": PIXEL_REPLAYED_IMAGE_LINES,
    }
    for name, expected in required.items():
        actual = frozenset(source[name])
        assert actual == expected, (name, sorted(actual), sorted(expected))

    assert source["EXPECTED_IMAGE_ROLE_PARTITION"] == (
        EXPECTED_IMAGE_ROLE_PARTITION
    )
    assert source["EXPECTED_IMAGE_LEDGER"] == EXPECTED_IMAGE_LEDGER
    assert tuple(source["EXPECTED_IMAGE_ASSET_MANIFEST"]) == (
        EXPECTED_IMAGE_ASSET_MANIFEST
    )


def load_semantic_manifest() -> tuple[tuple[str, object], ...]:
    assert SEMANTIC_ORACLE_PATH.is_file(), "T42 semantic oracle is not frozen"
    semantic_bytes = SEMANTIC_ORACLE_PATH.read_bytes()
    assert sha256(semantic_bytes) == EXPECTED_SEMANTIC_ORACLE_SHA256
    semantic = runpy.run_path(
        str(SEMANTIC_ORACLE_PATH), run_name="t42_semantic_for_asset_interface"
    )
    manifest = tuple(semantic["ASSET_SEMANTIC_MANIFEST"])
    assert manifest == EXPECTED_ASSET_SEMANTIC_MANIFEST
    return manifest


def rho_block(coefficient: int, bit: int) -> tuple[int, ...]:
    assert type(coefficient) is int and coefficient > 0
    assert type(bit) is int and bit in (0, 1)
    return (0,) * (coefficient - 1) + (1,) + ((0,) if bit else ())


def rho_word(coefficient: int, word: tuple[int, ...]) -> tuple[int, ...]:
    assert type(word) is tuple and word
    assert all(type(bit) is int and bit in (0, 1) for bit in word)
    return tuple(
        child
        for bit in word
        for child in rho_block(coefficient, bit)
    )


def replay_native_traces(
    manifest: tuple[tuple[str, object], ...],
) -> tuple[str, tuple[int, int, int, int, int]]:
    """Replay exact source/semantic fixtures without decoding JPEG pixels."""

    fields = dict(manifest)
    assert fields["schema"] == "T42-page162-semantic-interface/v1"
    native = ASSETS[1854]
    assert fields["asset"] == (
        native.name, native.byte_length, native.width, native.height,
        native.digest,
    )
    assert fields["gray_value"] == 0 and fields["black_value"] == 1
    assert fields["fixture_coefficient_evidence"] == "LIMITED_TRANSCRIBED"
    assert fields["pixel_replayed"] is False
    assert fields["pixel_program_forbidden"] is True
    assert fields["smallest_execution_lowering"] == (
        "uniform_PhaseIndex_times_Bit_word"
    )

    icon_coefficients = tuple(fields["rule_icon_coefficients"])
    assert icon_coefficients == (1, 2, 3, 4, 5)
    icon_entries = 0
    icon_children = 0
    for coefficient in icon_coefficients:
        for bit in (0, 1):
            block = rho_block(coefficient, bit)
            assert block == (
                (0,) * (coefficient - 1) + (1,) + ((0,) if bit else ())
            )
            icon_entries += 1
            icon_children += len(block)

    trace_rows: list[str] = []
    fixtures = tuple(fields["fixtures"])
    fixture_count = 0
    event_count = 0
    source_firings = 0
    emitted_children = 0
    for fixture in fixtures:
        (
            name, coefficients, expected_schedule, expected_lengths,
            final_digest, evidence_mode,
        ) = fixture
        assert evidence_mode == "LIMITED_TRANSCRIBED"
        coefficients = tuple(coefficients)
        schedule = tuple(expected_schedule)
        lengths = tuple(expected_lengths)
        assert coefficients and type(coefficients[0]) is int
        assert all(type(value) is int and value > 0 for value in coefficients[1:])
        assert schedule == tuple(reversed(coefficients[1:]))
        assert len(lengths) == len(schedule) + 1 and lengths[0] == 1

        word = (0,)
        actual_lengths = [1]
        for event, coefficient in enumerate(schedule):
            old = word
            old_digest = sha256("".join(map(str, old)).encode("ascii"))
            word = rho_word(coefficient, old)
            new_digest = sha256("".join(map(str, word)).encode("ascii"))
            actual_lengths.append(len(word))
            trace_rows.append(
                f"{name}|{evidence_mode}|{event}|{coefficient}|{len(old)}|{old_digest}|"
                f"{len(word)}|{new_digest}"
            )
            event_count += 1
            source_firings += len(old)
            emitted_children += len(word)
        assert tuple(actual_lengths) == lengths
        assert sha256("".join(map(str, word)).encode("ascii")) == final_digest
        fixture_count += 1

    assert (icon_entries, icon_children) == (10, 35)
    payload = "\n".join(trace_rows) + "\n"
    return sha256(payload.encode("utf-8")), (
        fixture_count, event_count, source_firings, emitted_children,
        icon_entries,
    )


def split_and_physical_indices() -> tuple[
    dict[str, list[tuple[Path, int, str]]], dict[str, list[Path]]
]:
    split_markdown = sorted(
        path for path in SOURCE_ROOT.rglob("*.md")
        if path.resolve() != BOOK.resolve() and path.name != "ANKoS-Atlas.md"
    )
    assert len(split_markdown) == 17
    split_re = re.compile(r"^!\[\]\((?:Images/)?([^/()]+\.jpeg)\)$")
    split_by_name: dict[str, list[tuple[Path, int, str]]] = {}
    for markdown in split_markdown:
        for line_number, text in enumerate(
            markdown.read_text(encoding="utf-8").splitlines(), 1
        ):
            if match := split_re.fullmatch(text):
                split_by_name.setdefault(match.group(1), []).append(
                    (markdown, line_number, text)
                )

    physical_by_name: dict[str, list[Path]] = {}
    for path in SOURCE_ROOT.rglob("*.jpeg"):
        if path.is_file():
            physical_by_name.setdefault(path.name, []).append(path)
    return split_by_name, physical_by_name


def ledger() -> tuple[
    str, tuple[int, int, int, int], str, str, tuple[int, int]
]:
    """Verify the closed asset universe and return canonical manifests."""

    split_by_name, physical_by_name = split_and_physical_indices()
    rows: list[str] = []
    structural_records: set[str] = set()
    ordered_sha256sum_rows: list[str] = []
    hashes: set[str] = set()
    names: set[str] = set()
    physical_paths: set[Path] = set()
    total_bytes = 0
    monolith_references = 0
    split_references = 0
    rgb_profiles = 0
    baseline_jfif_profiles = 0

    monolith_by_name: dict[str, list[int]] = {}
    for line, reference in BOOK_IMAGES.items():
        monolith_by_name.setdefault(Path(reference).name, []).append(line)

    for book_line, asset in sorted(ASSETS.items()):
        kind = CLASSIFICATION[book_line]
        assert kind in {"N", "R", "C"}
        assert asset.role.startswith(f"{kind}-")
        assert BOOK_IMAGES[book_line] == asset.name
        assert monolith_by_name.get(asset.name) == [book_line]
        monolith_references += 1

        expected_split = SOURCE_ROOT / asset.split_markdown
        split_hits = split_by_name.get(asset.name, [])
        assert split_hits == [(
            expected_split,
            asset.split_line,
            f"![](Images/{asset.name})",
        )], (book_line, split_hits)
        split_references += 1

        physical_path = SOURCE_ROOT / asset.physical
        assert physical_by_name.get(asset.name) == [physical_path]
        data = physical_path.read_bytes()
        digest = verify_asset_bytes(book_line, asset, data)
        assert asset.name not in names
        assert physical_path not in physical_paths
        assert digest not in hashes
        names.add(asset.name)
        physical_paths.add(physical_path)
        hashes.add(digest)
        total_bytes += len(data)
        rgb_profiles += int(asset.decoded_mode == "RGB")
        baseline_jfif_profiles += 1

        rows.append("|".join((str(book_line),) + tuple(map(str, asset))))
        structural_records.add(
            f"{book_line}->{asset.physical}\0{asset.byte_length}\0{digest}"
        )
        root_relative = physical_path.relative_to(ROOT).as_posix()
        ordered_sha256sum_rows.append(f"{digest}  {root_relative}\n")

    assert len(names) == len(physical_paths) == len(hashes) == 12
    payload = "\n".join(rows) + "\n"
    ordered_payload = "".join(ordered_sha256sum_rows)
    return (
        payload,
        (monolith_references, split_references, len(hashes), total_bytes),
        digest_records(structural_records),
        sha256(ordered_payload.encode("utf-8")),
        (rgb_profiles, baseline_jfif_profiles),
    )


def expect_assertion(operation: object) -> None:
    assert callable(operation)
    try:
        operation()
    except AssertionError:
        return
    raise AssertionError("hostile mutation was accepted")


def verify_hostile_mutation_gates() -> tuple[int, int]:
    """Prove byte and same-cardinality manifest mutations fail closed."""

    asset_rejections = 0
    for line, asset in ASSETS.items():
        data = bytearray((SOURCE_ROOT / asset.physical).read_bytes())
        mutation_index = len(data) // 2
        data[mutation_index] ^= 0x01
        expect_assertion(
            lambda line=line, asset=asset, data=bytes(data):
            verify_asset_bytes(line, asset, data)
        )
        asset_rejections += 1

    manifest_rejections = 0
    manifests = {
        "source_guards": SOURCE_GUARDS,
        "roles": ROLE_RECORDS,
        "candidate_scopes": CANDIDATE_SCOPE_RECORDS,
        "raster_boundary": RASTER_BOUNDARY_RECORDS,
        "references": REFERENCE_RECORDS,
        "trace_mechanics": TRACE_MECHANICS_RECORDS,
    }
    for name, records in manifests.items():
        original = min(records)
        mutated = (records - {original}) | {original + "\0mutated"}
        assert len(mutated) == len(records)
        assert digest_records(mutated) != EXPECTED_MANIFEST_DIGESTS[name]
        manifest_rejections += 1

    semantic_mutant = list(EXPECTED_ASSET_SEMANTIC_MANIFEST)
    semantic_mutant[-1] = ("pixel_program_forbidden", False)
    mutant_payload = json.dumps(
        semantic_mutant, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    assert sha256(mutant_payload) != EXPECTED_ASSET_SEMANTIC_MANIFEST_SHA256
    manifest_rejections += 1

    native = ASSETS[1854]
    digest_mutant = native._replace(digest="0" * 64)
    native_data = (SOURCE_ROOT / native.physical).read_bytes()
    expect_assertion(
        lambda: verify_asset_bytes(1854, digest_mutant, native_data)
    )
    manifest_rejections += 1

    trace_mutant = list(EXPECTED_ASSET_SEMANTIC_MANIFEST)
    fixture_field = next(
        index for index, field in enumerate(trace_mutant)
        if field[0] == "fixtures"
    )
    fixtures = list(trace_mutant[fixture_field][1])
    first = list(fixtures[0])
    first[2] = (3,) + tuple(first[2][1:])
    fixtures[0] = tuple(first)
    trace_mutant[fixture_field] = ("fixtures", tuple(fixtures))
    expect_assertion(lambda: replay_native_traces(tuple(trace_mutant)))
    manifest_rejections += 1

    partition_mutant = NATIVE_IMAGE_LINES | frozenset({12583})
    assert partition_mutant != NATIVE_IMAGE_LINES
    assert digest_lines(partition_mutant) != (
        EXPECTED_IMAGE_ROLE_PARTITION["native"][1]
    )
    manifest_rejections += 1

    return asset_rejections, manifest_rejections


EXPECTED_IMAGE_ASSET_MANIFEST = (
    12,
    "881c5c67fbf2aa6eb6bc6b8b0417b77df0057e24d657e72a08aac4f58d8cd2f5",
)
EXPECTED_ORDERED_SHA256SUM_MANIFEST = (
    12,
    "95a30c1661e88bcca18c33dbe9e841e04ae568785144ab16767c5ab803bdb3ef",
)
EXPECTED_LEDGER_SHA256 = (
    "42e6fcc06ad821257a3fdaa81a1ca2cb8c71a1449a44dd4250f7644bc0d16b29"
)
EXPECTED_TRACE_LEDGER_SHA256 = (
    "df358b3c335e09333a1110b7d25f38bb4745dc6598b8095c7c4fa766d925ef12"
)
EXPECTED_TRACE_METRICS = (4, 25, 301, 599, 10)
EXPECTED_REFERENCE_METRICS = (12, 12, 24)
EXPECTED_PHYSICAL_METRICS = (12, 12, 285_055)
EXPECTED_PROFILE_METRICS = (12, 12)
EXPECTED_DISPOSITION_METRICS = (1, 11, 0, 12, 0, 0)
EXPECTED_HOSTILE_MUTATION_METRICS = (12, 10)


IMAGE_ASSET_INTERFACE = (
    ("schema", "T42-image-asset-interface/v1"),
    ("role_partition", EXPECTED_IMAGE_ROLE_PARTITION),
    ("ledger", EXPECTED_IMAGE_LEDGER),
    ("asset_manifest", EXPECTED_IMAGE_ASSET_MANIFEST),
    ("boundary", (12, 1, 0)),
    ("pixel_inference", 0),
)


def main() -> None:
    if len(sys.argv) != 1:
        raise SystemExit("usage: 46-T42-asset-oracle.py")

    verify_semantic_manifests()
    verify_source_guards_and_candidate_closure()
    verify_source_interface()
    semantic_manifest = load_semantic_manifest()
    trace_digest, trace_metrics = replay_native_traces(semantic_manifest)
    payload, metrics, structural_digest, ordered_digest, profiles = ledger()
    hostile_mutations = verify_hostile_mutation_gates()
    ledger_digest = sha256(payload.encode("utf-8"))

    assert ledger_digest == EXPECTED_LEDGER_SHA256, (
        "ledger", ledger_digest, EXPECTED_LEDGER_SHA256,
    )
    assert (12, structural_digest) == EXPECTED_IMAGE_ASSET_MANIFEST
    assert (12, ordered_digest) == EXPECTED_ORDERED_SHA256SUM_MANIFEST
    assert trace_digest == EXPECTED_TRACE_LEDGER_SHA256, (
        trace_digest, EXPECTED_TRACE_LEDGER_SHA256,
    )
    assert trace_metrics == EXPECTED_TRACE_METRICS
    assert (metrics[0], metrics[1], metrics[0] + metrics[1]) == (
        EXPECTED_REFERENCE_METRICS
    )
    assert (metrics[2], metrics[2], metrics[3]) == EXPECTED_PHYSICAL_METRICS
    assert profiles == EXPECTED_PROFILE_METRICS
    assert hostile_mutations == EXPECTED_HOSTILE_MUTATION_METRICS
    assert (
        len(NATIVE_IMAGE_LINES), len(RELATION_IMAGE_LINES),
        len(CONTROL_IMAGE_LINES), len(GOVERNED_IMAGE_LINES),
        len(EXCLUDED_IMAGE_LINES), len(UNRESOLVED_IMAGE_LINES),
    ) == EXPECTED_DISPOSITION_METRICS
    assert (len(ASSEMBLIES), sum(map(len, ASSEMBLIES.values()))) == (2, 10)
    assert (
        len(HASH_BOUND_IMAGE_LINES), len(LIMITED_TRANSCRIBED_IMAGE_LINES),
        len(PIXEL_REPLAYED_IMAGE_LINES),
    ) == (12, 1, 0)

    print(
        "T42 asset oracle: PASS governed=12; classes N/R/C=1/11/0; "
        "candidates=12; excluded=0; refs=24(monolith=12,split=12); "
        "unique_hashes=12; physical_files=12; bytes=285055; "
        "assemblies=2/10_files; profiles=12_RGB/12_baseline_JFIF_1.01; "
        "boundary=12_HASH_BOUND/1_LIMITED_TRANSCRIBED/0_PIXEL_REPLAYED; "
        f"native_trace=fixtures_{trace_metrics[0]}/events_{trace_metrics[1]}/"
        f"source_firings_{trace_metrics[2]}/children_{trace_metrics[3]}/"
        f"rule_icon_entries_{trace_metrics[4]}; "
        f"mutation_gates=assets_{hostile_mutations[0]}/"
        f"manifests_{hostile_mutations[1]}; "
        "pixel_inference=0; source_and_semantic_interfaces=PASS; "
        "unresolved_image_dispositions=0"
    )
    print(f"asset_manifest={structural_digest}")
    print(f"trace_manifest={trace_digest}")


if __name__ == "__main__":
    main()
