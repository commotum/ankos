#!/usr/bin/env python3
"""Fail-closed raster/provenance audit for T38 variable-index recurrences.

Four images are governed: the main eight-rule/term-row plate, its fluctuation
plate, the related digit-count plate, and the Notes address-plot plate.  Eleven
neighbor images are bound as exclusions.  Only the two main plates have a
limited manual transcription; no pixels are regenerated or treated as a
hidden executable program.
"""

from __future__ import annotations

import hashlib
import re
import runpy
import sys
from pathlib import Path
from typing import NamedTuple


if not __debug__:
    raise RuntimeError("T38 asset verification requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "ref/A-New-Kind-of-Science"
BOOK = SOURCE_ROOT / "A-New-Kind-of-Science.md"
SOURCE_ORACLE_PATH = ROOT / "goal-1/44-T38-source-oracle.py"

EXPECTED_BOOK_LINES = 22_498
EXPECTED_BOOK_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_records(values: set[str] | frozenset[str]) -> str:
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
    digest: str
    assembly: str
    boundary: str
    reason: str


def parse_assets(rows: str) -> dict[int, AssetSpec]:
    assets: dict[int, AssetSpec] = {}
    for row in rows.strip().splitlines():
        fields = row.split("|", 12)
        assert len(fields) == 13, row
        line = int(fields[0])
        assert line not in assets
        assets[line] = AssetSpec(
            fields[1], fields[2], fields[3], fields[4], int(fields[5]),
            int(fields[6]), int(fields[7]), int(fields[8]), fields[9],
            fields[10], fields[11], fields[12],
        )
    return assets


GOVERNED_ROWS = r"""
1573|N-strict-rules-and-visible-prefixes|_page_144_Figure_3.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_144_Figure_3.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|177|151577|1237|773|1d42ad7a00174dc8fb589b7d98dcde344264e86dd396a9fce3e88dd737959b77|main-variable-recurrence|LIMITED_TRANSCRIBED|eight formulas, seeds, and finite term rows; lower e-h mini-plots are physically cropped
1599|N-fluctuation-observer-plate|_page_145_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_145_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|181|224485|1234|1370|4ecc73da26bd1382d27190f5cc56b687566358d99ae0e92d5dfb2098c0bda6c4|main-variable-recurrence|LIMITED_TRANSCRIBED|six source-labeled observer formulas and qualitative plots; no curve samples transcribed
12674|R-digit-count-nesting-relation|_page_920_Figure_30.jpeg|BACK-MATTER/Index/Images/_page_920_Figure_30.jpeg|BACK-MATTER/Index/Index.md|577|10024|575|98|8e8c22a2c52e54c3d5ab4ae00b12f84e862a1264a532e2f35266b29b5a6d3ba0|notes-digit-relation|HASH_BOUND|digit-count sequence resembles case-c nesting but is not T38 evolution
12763|N-computed-address-observer|_page_922_Figure_2.jpeg|BACK-MATTER/Index/Images/_page_922_Figure_2.jpeg|BACK-MATTER/Index/Index.md|666|21890|582|220|8d1179a70a1aad8edf0ead0c676b8b02409257a086490f0dfb3901c6090c4b01|notes-address-observer|HASH_BOUND|p and q address plots only; exact addresses derive from the recurrence
"""


EXCLUDED_ROWS = r"""
1565|X-T37-fixed-lag|_page_143_Figure_6.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_143_Figure_6.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|169|86025|1231|382|731de2a621d5b227026c1b1ac4ed488ce96afc26be0fd5fcb0495297f5ed650b|T37-main|HASH_BOUND|fixed-distance recurrence plate belongs to T37
1625|X-T39-prime-sieve|_page_147_Figure_4.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_147_Figure_4.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|207|101730|1166|396|d802dac2946c5c80ef031170ab4667a0ef39f1e690fd50a47e1633974440d8f8|T39-main|HASH_BOUND|prime-sieve plate begins the next construction
12678|X-bitwise-neighbor|_page_921_Picture_3.jpeg|BACK-MATTER/Index/Images/_page_921_Picture_3.jpeg|BACK-MATTER/Index/Index.md|581|2657|96|83|985e5d74ae6c0bbf6f3beb1554345c0af51c848889f0305de416ef093bd70481|bitwise-gallery|HASH_BOUND|iterated bitwise gallery is a T36-neighbor exclusion
12680|X-bitwise-neighbor|_page_921_Picture_4.jpeg|BACK-MATTER/Index/Images/_page_921_Picture_4.jpeg|BACK-MATTER/Index/Index.md|583|2980|81|83|d9da05f6d43e78e6cb16a0ea451d8204e2f4320aaccdfe6ef2b9b157daa6749e|bitwise-gallery|HASH_BOUND|iterated bitwise gallery is a T36-neighbor exclusion
12682|X-bitwise-neighbor|_page_921_Picture_5.jpeg|BACK-MATTER/Index/Images/_page_921_Picture_5.jpeg|BACK-MATTER/Index/Index.md|585|3791|133|93|5e308a461a3d1852a69750c906d5a46a0b94e264696fff6209ca414e43c58068|bitwise-gallery|HASH_BOUND|iterated bitwise gallery is a T36-neighbor exclusion
12684|X-bitwise-neighbor|_page_921_Picture_6.jpeg|BACK-MATTER/Index/Images/_page_921_Picture_6.jpeg|BACK-MATTER/Index/Index.md|587|3249|114|89|b0eca5ac7ce927db9edb42807573b5a63ee9c9420a733782609612234cc565eb|bitwise-gallery|HASH_BOUND|iterated bitwise gallery is a T36-neighbor exclusion
12686|X-bitwise-neighbor|_page_921_Picture_7.jpeg|BACK-MATTER/Index/Images/_page_921_Picture_7.jpeg|BACK-MATTER/Index/Index.md|589|2324|92|93|5ed00f75d880eb9a2d3aa47132e1d560a5f2997f7f7292d309b7146532adca15|bitwise-gallery|HASH_BOUND|iterated bitwise gallery is a T36-neighbor exclusion
12822|X-primitive-recursive-function|_page_923_Figure_10.jpeg|BACK-MATTER/Index/Images/_page_923_Figure_10.jpeg|BACK-MATTER/Index/Index.md|725|9981|576|116|133dccf7a75edfb851d03a4d00222c947cc4933aabc1cf7ea8f7ecb5cc463e53|primitive-recursive-functions|HASH_BOUND|multiargument primitive-function relation is not native T38 prefix evolution
12826|X-primitive-recursive-function|_page_923_Figure_12.jpeg|BACK-MATTER/Index/Images/_page_923_Figure_12.jpeg|BACK-MATTER/Index/Index.md|729|13234|557|125|63ffe598605bc10b8c82e4412033e9f04cece4be0073a4319600348206dfe6e1|primitive-recursive-functions|HASH_BOUND|multiargument primitive-function relation is not native T38 prefix evolution
12836|X-diagonal-function|_page_923_Figure_17.jpeg|BACK-MATTER/Index/Images/_page_923_Figure_17.jpeg|BACK-MATTER/Index/Index.md|739|9684|547|120|b9556755f0a0a47c70699e18f5fc1e880ecd5a29c78014d010142b6ba248e05f|diagonal-functions|HASH_BOUND|diagonal computability relation is not native T38 prefix evolution
12844|X-Ulam-T39-composition|_page_923_Figure_21.jpeg|BACK-MATTER/Index/Images/_page_923_Figure_21.jpeg|BACK-MATTER/Index/Index.md|747|9807|576|79|d5f1729767f4379de49c08cb2508f5ce08e35fee6f28028e39e82a249f6fd160|Ulam-T39|HASH_BOUND|Ulam is the separately resolved T37/T39 composition
"""


ASSETS = parse_assets(GOVERNED_ROWS)
EXCLUDED_ASSETS = parse_assets(EXCLUDED_ROWS)
NATIVE_IMAGE_LINES = frozenset({1573, 1599, 12763})
RELATION_IMAGE_LINES = frozenset({12674})
CONTROL_IMAGE_LINES = frozenset()
GOVERNED_IMAGE_LINES = frozenset(ASSETS)
EXCLUDED_IMAGE_LINES = frozenset(EXCLUDED_ASSETS)
CANDIDATE_IMAGE_LINES = GOVERNED_IMAGE_LINES | EXCLUDED_IMAGE_LINES
assert set(ASSETS) == set(NATIVE_IMAGE_LINES | RELATION_IMAGE_LINES)
assert not (GOVERNED_IMAGE_LINES & EXCLUDED_IMAGE_LINES)
assert len(CANDIDATE_IMAGE_LINES) == 15


PROGRAM_TRANSCRIPT = frozenset({
    "a|f[n]=1+f[n-f[n-1]]|seed=1|visible=48",
    "b|f[n]=2+f[n-f[n-1]]|seed=1,1|visible=44",
    "c|f[n]=f[f[n-1]]+f[n-f[n-1]]|seed=1,1|visible=40",
    "d|f[n]=f[n-f[n-1]]+f[n-f[n-2]-1]|seed=1,1|visible=40",
    "e|f[n]=f[n-f[n-1]]+f[n-f[n-2]]|seed=1,1|visible=40",
    "f|f[n]=f[n-f[n-1]-1]+f[n-f[n-2]-1]|seed=1,1|visible=42",
    "g|f[n]=f[f[n-1]]+f[n-f[n-2]-1]|seed=1,1|visible=41",
    "h|f[n]=f[f[n-1]]+f[n-2*f[n-1]+1]|seed=1,1|visible=45",
})


VISIBLE_TERM_ROWS = {
    "a": (1,2,2,3,3,3,4,4,4,4,5,5,5,5,5,6,6,6,6,6,6,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8,9,9,9,9,9,9,9,9,9,10,10,10),
    "b": (1,1,3,3,3,5,3,5,5,5,7,5,7,5,7,7,7,9,7,9,7,9,7,9,9,9,11,9,11,9,11,9,11,9,11,11,11,13,11,13,11,13,11,13),
    "c": (1,1,2,2,3,4,4,4,5,6,7,7,8,8,8,8,9,10,11,12,12,13,14,14,15,15,15,16,16,16,16,16,17,18,19,20,21,21,22,23),
    "d": (1,1,2,2,3,4,4,4,5,6,6,7,8,8,8,8,9,10,10,11,12,12,12,13,14,14,15,16,16,16,16,16,17,18,18,19,20,20,20,21),
    "e": (1,1,2,3,3,4,5,5,6,6,6,8,8,8,10,9,10,11,11,12,12,12,12,16,14,14,16,16,16,16,20,17,17,20,21,19,20,22,21,22),
    "f": (1,1,2,2,2,4,3,4,4,4,8,5,5,8,8,6,8,12,8,11,9,9,10,13,16,9,12,20,10,12,23,12,15,21,13,17,18,19,19,22,21,19),
    "g": (1,1,2,2,2,3,4,4,4,4,5,6,7,8,8,8,8,8,8,9,10,10,10,11,13,15,15,14,15,16,16,16,16,16,16,16,17,18,18,18,18),
    "h": (1,1,2,2,2,3,3,4,3,4,4,4,5,4,6,5,6,6,7,6,7,6,7,7,7,8,8,9,7,9,7,10,8,11,8,11,9,10,10,11,10,11,10,11,11),
}
VISIBLE_ROW_RECORDS = frozenset(
    f"{name}|{','.join(map(str, values))}"
    for name, values in VISIBLE_TERM_ROWS.items()
)


SOURCE_GUARDS = frozenset({
    "1569|not just a fixed distance back|f[n - f[n - 1]]",
    "1571|meaningless quantities such as f[0], f[-1] and f[-2]",
    "1575|particular rules shown here all avoid this problem",
    "1601|Fluctuations in the overall increase|base 2 digit sequence",
    "1607|case (f)|even after a million steps",
    "1613|number of 1's|digit sequences of all numbers less than n",
    "12720|essential to store all the values of f[n]",
    "12722|f[n-f[n-1]] + f[n-f[n-2]]",
    "12726|leftmost innermost|f[-1]-f[-1]",
    "12731|(n + g[IntegerDigits[n, 2]])/2",
    "12738|Flatten[Table[n, {IntegerExponent[n, 2] + 1}]",
    "12742|2m+1-DigitCount[m, 2, 1]",
    "12759|positive and negative fluctuations|not completely random",
    "12761|form f[p[n]] + f[q[n]]",
    "12765|distinct nodes reached starting from f[12]",
    "12767|John Conway around 1988|Douglas Hofstadter in 1979",
})


LIMIT_AND_ROLE_RECORDS = frozenset({
    "BOOK1573|LIMITED_TRANSCRIBED|rules,seeds,visible-rows|no-pixel-replay",
    "BOOK1573|crop|a-d-mini-plots-complete|e-h-mini-plots-cut-by-jpeg-bottom",
    "BOOK1599|LIMITED_TRANSCRIBED|c-g:f[n]-n/2|h:f[n]-0.42*n^0.818",
    "BOOK1599|plots|qualitative-only|no-curve-samples-or-pixel-replay",
    "BOOK12674|RELATION|digit-count-nesting|not-native-feedback",
    "BOOK12763|NATIVE_OBSERVER|p-q-address-plots|addresses-derived-from-rule",
    "BOOK12738|source-defect|missing-extra-initial-1|repair-must-be-guarded",
    "boundary|4-governed|11-excluded|15-total",
})


EXCLUSION_REASON_RECORDS = frozenset(
    f"{line}|{asset.role}|{asset.reason}|{asset.assembly}"
    for line, asset in EXCLUDED_ASSETS.items()
)


EXPECTED_MANIFEST_DIGESTS = {
    "source_guards": "3ac1585e704e68a190516f88def59e91e9852124239795e1835695e1a01d4dd0",
    "program_transcript": "80503af310381125333643ed629d70d77853b89d8b66016bc92875d9ebd7145c",
    "visible_rows": "253d43c6204d2ad5a77da8b3b5a98f38d87e40c657c8596252c8208c47b43301",
    "limits_roles": "1c20fd43315194e279654e4e91d31fea6c1d297210f7a2bdee79f3a6ee052608",
    "exclusion_reasons": "df31ce479153e6e458b3c37b8fd23fb828fd086916c53f628a762ff71b9bb3fe",
}
EXPECTED_GOVERNED_LEDGER_SHA256 = "3c452b9744ee59b3fcc73c51696a918afce5058b68ce2da3e297cbacf5402f29"
EXPECTED_EXCLUDED_LEDGER_SHA256 = "d38473a634eb17c3af67427517ba5020d3b5cf5dd1e76139f1c4e8eadb204686"


def verify_semantic_manifests() -> None:
    manifests = {
        "source_guards": SOURCE_GUARDS,
        "program_transcript": PROGRAM_TRANSCRIPT,
        "visible_rows": VISIBLE_ROW_RECORDS,
        "limits_roles": LIMIT_AND_ROLE_RECORDS,
        "exclusion_reasons": EXCLUSION_REASON_RECORDS,
    }
    for name, records in manifests.items():
        assert records and len(records) == len(set(records))
        actual = digest_records(records)
        expected = EXPECTED_MANIFEST_DIGESTS[name]
        assert actual == expected, (name, actual, expected)


def jpeg_size(data: bytes) -> tuple[int, int]:
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
        size = int.from_bytes(data[offset:offset + 2], "big")
        assert size >= 2
        if marker in sof:
            height = int.from_bytes(data[offset + 3:offset + 5], "big")
            width = int.from_bytes(data[offset + 5:offset + 7], "big")
            return width, height
        offset += size
    raise AssertionError("JPEG SOF marker not found")


def verify_source_guards() -> None:
    for record in SOURCE_GUARDS:
        fields = record.split("|")
        line = int(fields[0])
        text = BOOK_LINES[line - 1]
        for needle in fields[1:]:
            assert needle in text, (line, needle)


def verify_source_interface() -> None:
    source = runpy.run_path(str(SOURCE_ORACLE_PATH), run_name="t38_source_for_asset")
    expected = {
        "GOVERNED_IMAGE_LINES": GOVERNED_IMAGE_LINES,
        "EXCLUDED_IMAGE_LINES": EXCLUDED_IMAGE_LINES,
        "NATIVE_IMAGE_LINES": NATIVE_IMAGE_LINES,
        "RELATION_IMAGE_LINES": RELATION_IMAGE_LINES,
        "CONTROL_IMAGE_LINES": CONTROL_IMAGE_LINES,
    }
    for name, values in expected.items():
        assert frozenset(source[name]) == values, (name, source[name], values)
    assert frozenset(source["SOURCE_SEMANTIC_GUARDS"])


def split_and_physical_indices() -> tuple[
    dict[str, list[tuple[Path, int]]], dict[str, list[Path]]
]:
    split_markdown = sorted(
        path for path in SOURCE_ROOT.rglob("*.md")
        if path.resolve() != BOOK.resolve() and path.name != "ANKoS-Atlas.md"
    )
    assert len(split_markdown) == 17
    split_re = re.compile(r"^!\[\]\((?:Images/)?([^/()]+\.jpeg)\)$")
    split_by_name: dict[str, list[tuple[Path, int]]] = {}
    for markdown in split_markdown:
        for line, text in enumerate(markdown.read_text(encoding="utf-8").splitlines(), 1):
            if match := split_re.fullmatch(text):
                split_by_name.setdefault(match.group(1), []).append((markdown, line))
    physical_by_name: dict[str, list[Path]] = {}
    for path in SOURCE_ROOT.rglob("*.jpeg"):
        if path.is_file():
            physical_by_name.setdefault(path.name, []).append(path)
    return split_by_name, physical_by_name


def verify_group(
    assets: dict[int, AssetSpec],
    split_by_name: dict[str, list[tuple[Path, int]]],
    physical_by_name: dict[str, list[Path]],
) -> tuple[str, int, int, int, int, int]:
    rows: list[str] = []
    hashes: set[str] = set()
    assemblies: set[str] = set()
    total_bytes = 0
    for book_line, asset in sorted(assets.items()):
        assert BOOK_IMAGES[book_line] == asset.name
        assert [line for line, name in BOOK_IMAGES.items() if name == asset.name] == [book_line]
        split_path = SOURCE_ROOT / asset.split_markdown
        assert split_by_name.get(asset.name) == [(split_path, asset.split_line)]
        physical_path = SOURCE_ROOT / asset.physical
        assert physical_by_name.get(asset.name) == [physical_path]
        data = physical_path.read_bytes()
        assert len(data) == asset.byte_length
        assert jpeg_size(data) == (asset.width, asset.height)
        digest = sha256(data)
        assert digest == asset.digest
        hashes.add(digest)
        assemblies.add(asset.assembly)
        total_bytes += len(data)
        rows.append("|".join((str(book_line),) + tuple(map(str, asset))))
    payload = "\n".join(rows) + "\n"
    count = len(assets)
    return payload, count, count, len(hashes), total_bytes, len(assemblies)


def ledger() -> tuple[str, str, tuple[int, ...], tuple[int, ...]]:
    split_by_name, physical_by_name = split_and_physical_indices()
    governed_payload, *governed_metrics = verify_group(
        ASSETS, split_by_name, physical_by_name
    )
    excluded_payload, *excluded_metrics = verify_group(
        EXCLUDED_ASSETS, split_by_name, physical_by_name
    )
    return (
        governed_payload,
        excluded_payload,
        tuple(governed_metrics),
        tuple(excluded_metrics),
    )


def main() -> None:
    if len(sys.argv) != 1:
        raise SystemExit("usage: 44-T38-asset-oracle.py")
    verify_semantic_manifests()
    verify_source_guards()
    verify_source_interface()
    governed, excluded, gm, xm = ledger()
    assert sha256(governed.encode("utf-8")) == EXPECTED_GOVERNED_LEDGER_SHA256
    assert sha256(excluded.encode("utf-8")) == EXPECTED_EXCLUDED_LEDGER_SHA256
    assert gm == (4, 4, 4, 407_976, 3), gm
    assert xm == (11, 11, 11, 245_462, 6), xm
    assert {a.boundary for a in ASSETS.values()} == {"LIMITED_TRANSCRIBED", "HASH_BOUND"}
    assert sum(a.boundary == "LIMITED_TRANSCRIBED" for a in ASSETS.values()) == 2
    assert len(PROGRAM_TRANSCRIPT) == 8
    assert tuple(map(len, VISIBLE_TERM_ROWS.values())) == (48,44,40,40,40,42,41,45)
    print(
        "T38 asset oracle: PASS governed=4; classes N/R/C=3/1/0; "
        "candidates=15; excluded=11; refs=8; hashes=4; bytes=407976; "
        "assemblies=3/4_files; excluded_refs=22; excluded_hashes=11; "
        "excluded_bytes=245462; excluded_assemblies=6/11_files; "
        "boundary=4_HASH_BOUND/2_LIMITED_TRANSCRIBED/0_PIXEL_REPLAYED; "
        "visible_horizons=48/44/40/40/40/42/41/45; "
        "page144_lower_e-h_plots=CROPPED; unresolved_image_dispositions=0"
    )


if __name__ == "__main__":
    main()
