from __future__ import annotations

import json
import os
import re
import sys
import unittest
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


# ANKOS_REPO_ROOT supports isolated packet review; in the repository, the
# parents[2] fallback resolves to the project root.
REPO_ROOT = (
    Path(os.environ["ANKOS_REPO_ROOT"])
    if "ANKOS_REPO_ROOT" in os.environ
    else Path(__file__).resolve().parents[2]
).resolve()
GOAL_DIR = REPO_ROOT / "goal-5"
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402
import validate  # noqa: E402


# Values below are derived from the canonical integrated manifests and target.
EXPECTED_TARGET_BYTES = 85_452
EXPECTED_TARGET_LINES = 666
EXPECTED_TARGET_SHA256 = (
    "23b589b5e711b93d2e4eb85f78c36e6c39f5b418f73a72bd79697fe6575f5a93"
)
EXPECTED_CORRECTION_ROWS_SHA256 = (
    "a1dec02328b53fa1f3ddacd62ab442d04e10558361296548ab9238c54087ca3b"
)
EXPECTED_CORRECTION_ROW_HASH_SEQUENCE = (
    "8641cf220bf3825065215e100c048dab582ea7683f42f13814b60bddc4f8f2c3"
)
EXPECTED_INVENTORY_HASHES = {
    "headings": "f74fc1b553f3e84a3a0a894683c7b56325406091843bc621acfcce20b1fb5ecc",
    "labels": "3b7eac5203ad6cb559dd59ba30aa9638e5eefee4fa7bbbded06883dccfdf47d3",
    "code_fences": "7caf3059216dccb0d3bcbb8f33cf7f0cc5c61ea2110e786eff313e9e15060212",
    "inline_code": "30b47173bdafdfb5bd74f036f08866579049fe3c454887ff000ec08721b00f53",
    "image_references": "387f940554c276de1af83e96d4e2ee888008f031cf8409ad0440cf62dd298f8d",
}
EXPECTED_INLINE_CODE_COUNT = 19

# These hashes pin the final post-residual N06 image-map state.
EXPECTED_IMAGE_ROWS_SHA256 = (
    "66c36e08bba712d6a91727cfabbbc18f17b051cd796a07abcf2f6eacf0c2a0f8"
)
EXPECTED_CHANGED_IMAGE_ROWS_SHA256 = (
    "0d80459b0f85ceaa12a49b1758f8ab1e45e27ce2ed63c8120fd03d7cf393533e"
)
EXPECTED_ADDED_ROWS_SHA256 = (
    "fa13028a22caf1a540af66eb59a8625c3d73fb3389a422e07e6b5621f61f82ae"
)

EXPECTED_HEADINGS = [
    "## Starting from Randomness",
    "### The Emergence of Order",
    "### Four Classes of Behavior",
    "### Sensitivity to Initial Conditions",
    "### Systems of Limited Size and Class 2 Behavior",
    "### Randomness in Class 3 Systems",
    "### Special Initial Conditions",
    "### The Notion of Attractors",
    "### Structures in Class 4 Systems",
]

EXPECTED_CHANGED_ORDINALS = (
    1049,
    1050,
    1051,
    1052,
    1057,
    1059,
    1060,
    1061,
    1062,
    1063,
    1064,
    1065,
    1066,
    1067,
    1074,
    1075,
    1076,
    1081,
    1085,
    1086,
    1087,
    1088,
    1089,
    1090,
    1098,
    1101,
    1102,
    1103,
    1104,
    1105,
    1106,
    1107,
    1108,
    1109,
    1110,
    1111,
)
EXPECTED_REPAIRED_ORDINALS = (1057, 1067, 1081, 1089, 1090, 1098)
EXPECTED_COMPOSITE_GROUPS = {
    "G5-A-0072": (1049, 1050, 1051, 1052),
    "G5-A-0073": (1059, 1060, 1061, 1062),
    "G5-A-0074": (1063, 1064, 1065, 1066),
    "G5-A-0075": (1074, 1075, 1076),
    "G5-A-0076": (1085, 1086, 1087, 1088),
    "G5-A-0077": (1101, 1102, 1103, 1104),
    "G5-A-0078": (1105, 1106, 1107),
    "G5-A-0079": (1108, 1109, 1110, 1111),
}

EXPECTED_VISUAL_CORRECTION_GUARDS: dict[str, dict[str, Any]] = {
    "G5-C-1392": {
        "raw_line": 14_226,
        "raw_start_byte": 2_008_350,
        "addition_id": "G5-A-0072",
        "partial_count": 4,
        "image": "_page_963_Frequencies_of_Classes_Four_Pie_Charts.jpeg",
        "position": 2,
        "before_bytes": 124,
        "before_sha256": "8ece5634b3b358ba12b87a57ecde53fc4d50e456726c377da11c8789e83e00e2",
        "after_bytes": 58,
        "after_sha256": "a46ebb4e82ebed50a2e2862e0e22f7b34a7d98c4aaa5a64f7f92e9a28dc61c4e",
        "row_sha256": "1b2bd3a3dee4fcd6df0e002caced8535e6d9034494aa80424f9f4586bff02ac1",
    },
    "G5-C-1393": {
        "raw_line": 14_368,
        "raw_start_byte": 2_027_296,
        "addition_id": "G5-A-0073",
        "partial_count": 4,
        "image": "_page_967_Rule_90_Generalized_Additivity_Four_Panel_Row.jpeg",
        "position": 9,
        "before_bytes": 126,
        "before_sha256": "13bdae2a5e855c937e213fbf792be36f791ccf05e0d7a1f10fbea97cbdcf0f06",
        "after_bytes": 65,
        "after_sha256": "dc30063fcac78134d07a2adade7c29018689b09eae312e4a22179d570a368ebc",
        "row_sha256": "2a3aad0d883363375fdf5b2114f6edbad8bc06f53397db218096257410444def",
    },
    "G5-C-1394": {
        "raw_line": 14_378,
        "raw_start_byte": 2_027_611,
        "addition_id": "G5-A-0074",
        "partial_count": 4,
        "image": "_page_967_Rule_250_Generalized_Additivity_Four_Panel_Row.jpeg",
        "position": 10,
        "before_bytes": 126,
        "before_sha256": "07da3d2a394b4ff6c3b97845afaecd0ae950cdd717f7d509a93255ac53e10f2a",
        "after_bytes": 66,
        "after_sha256": "73582763acd641855508513ecc7fc55d1bf3bda52a614f530c6ae71d37b57897",
        "row_sha256": "a90680812744fcf43d3b72545820aff171161120fd6630b5c94a10e40e4670d0",
    },
    "G5-C-1395": {
        "raw_line": 14_544,
        "raw_start_byte": 2_049_915,
        "addition_id": "G5-A-0075",
        "partial_count": 3,
        "image": "_page_971_Nested_Initial_Conditions_Three_Panel_Row.jpeg",
        "position": 18,
        "before_bytes": 94,
        "before_sha256": "58e1860843cfbaddbcec667cf398a1eb05132cd9ce1dedd08ec5902377d0c171",
        "after_bytes": 61,
        "after_sha256": "4835ca598b5db5b47cdf313e71257b0cf5f4f7dbaee42f59943f3417b7f4b7b1",
        "row_sha256": "c3120f3650657e382ad1cb7cd75ce99252adaa0330baec5d0ece1961a0e04096",
    },
    "G5-C-1396": {
        "raw_line": 14_740,
        "raw_start_byte": 2_083_152,
        "addition_id": "G5-A-0076",
        "partial_count": 4,
        "image": "_page_978_Shift_Rule_170_Size_4_to_8_Five_Panel_Row.jpeg",
        "position": 27,
        "before_bytes": 124,
        "before_sha256": "f4e40fb4c17600cb4ce53af12495936407decb89c3b0625ec96fbf3acc99e9ac",
        "after_bytes": 61,
        "after_sha256": "40e0a73f0d600f33bfd675166688c6cea8380f5ed42856ed4514d5fdc9f5b71a",
        "row_sha256": "91b6f0a61921c2ac74329aff120e4591a6bcad5e3750cd5ff66b788c2caa3cf5",
    },
    "G5-C-1397": {
        "raw_line": 14_817,
        "raw_start_byte": 2_089_088,
        "addition_id": "G5-A-0077",
        "partial_count": 4,
        "image": "_page_980_Life_Elaborate_Structures_Four_Panel_Group.jpeg",
        "position": 40,
        "before_bytes": 125,
        "before_sha256": "6401632d97fda9c964293c72648a0de79ab45945fe06dc7adb5ca82fb6d64204",
        "after_bytes": 62,
        "after_sha256": "a65bdde3ddbe8e6bfec75162013093429ded3557419dd4141688859c9724e1b3",
        "row_sha256": "fc40b5a3700ec7e6f87d61786a0dce6c0350a3a88bd94ddc91f5f98aae155073",
    },
    "G5-C-1398": {
        "raw_line": 14_829,
        "raw_start_byte": 2_089_786,
        "addition_id": "G5-A-0078",
        "partial_count": 3,
        "image": "_page_980_Life_Spacefiller_Three_Panel_Row.jpeg",
        "position": 41,
        "before_bytes": 94,
        "before_sha256": "917315e097c1876786085c2600a963381871c0808a4ef369a9c6eade4e22f750",
        "after_bytes": 52,
        "after_sha256": "fbd5d26d9f4417c4010194c7c30511425585c64442c356ef95e8a37384606c2c",
        "row_sha256": "bb0bd2f71ca25e0dc8eeede07f05bfb701171379e1eb786f91696a78d8f986c4",
    },
    "G5-C-1399": {
        "raw_line": 14_837,
        "raw_start_byte": 2_090_131,
        "addition_id": "G5-A-0079",
        "partial_count": 4,
        "image": "_page_980_Life_Puffer_Train_Four_Panel_Group.jpeg",
        "position": 42,
        "before_bytes": 126,
        "before_sha256": "f6c4297aab5548e1c612e192939363d80c0009a8f44d3fd804c4644139ca113c",
        "after_bytes": 54,
        "after_sha256": "f7afb5f017607745488a418261e211aff2ca4c43971dbb543bca640d729e64b6",
        "row_sha256": "8b955560930c3c50acdcebe39265d12ea46aa51403bc9c415a76832cd1904c90",
    },
}

# basename: (role, addition ID or repaired map ordinal, digest,
#            (width, height), byte count, 1-based Markdown reference position)
EXPECTED_ASSETS: dict[
    str, tuple[str, str | int, str, tuple[int, int], int, int]
] = {
    "_page_963_Frequencies_of_Classes_Four_Pie_Charts.jpeg": (
        "ADDED_ASSET",
        "G5-A-0072",
        "04509aa5adc7085f181c56a623023a7fcd15085f983ea36e5fc3767ca6b0e449",
        (1860, 490),
        89_735,
        2,
    ),
    "_page_966_Figure_19.jpeg": (
        "REPAIRED_EXISTING_ASSET",
        1057,
        "fa2575de32a65da1f1d9a1fb4cef4a57f095136f551f9bef65304631a7edaf90",
        (1800, 890),
        263_732,
        7,
    ),
    "_page_967_Picture_22.jpeg": (
        "REPAIRED_EXISTING_ASSET",
        1067,
        "7031dde8b41161115352948f9a77c2a6a8cadd0bf2bafd5b8189bc1aeca60aed",
        (1820, 440),
        113_436,
        11,
    ),
    "_page_967_Rule_250_Generalized_Additivity_Four_Panel_Row.jpeg": (
        "ADDED_ASSET",
        "G5-A-0074",
        "3e13dea59cfe70198743d29e7710f522de531f9e519ee7c080f51387f168bb6e",
        (1860, 340),
        117_613,
        10,
    ),
    "_page_967_Rule_90_Generalized_Additivity_Four_Panel_Row.jpeg": (
        "ADDED_ASSET",
        "G5-A-0073",
        "174774b58b270fdbfd2d3ce50a1612ff07f3e419050366da2a39414409dfc724",
        (1860, 360),
        93_907,
        9,
    ),
    "_page_971_Nested_Initial_Conditions_Three_Panel_Row.jpeg": (
        "ADDED_ASSET",
        "G5-A-0075",
        "bb5b5b5c2a1e547e59d3882380531ab6960739bd3633462bb7c7c0807809d2ef",
        (1800, 460),
        282_694,
        18,
    ),
    "_page_977_Picture_6.jpeg": (
        "REPAIRED_EXISTING_ASSET",
        1081,
        "7a9e1134d9e9eb69f991814c6c530bd5340508e63f5e24d0bf0e1c5c3583d742",
        (1860, 510),
        137_752,
        23,
    ),
    "_page_978_Figure_14.jpeg": (
        "REPAIRED_EXISTING_ASSET",
        1089,
        "4a63d0a1b6e1cb884bdc095e0104adcfe89f57bcc5f163983f39a536121d7be0",
        (1800, 960),
        344_319,
        28,
    ),
    "_page_978_Picture_15.jpeg": (
        "REPAIRED_EXISTING_ASSET",
        1090,
        "1d6c8da946b6f8033a737b88fc52e4766d066d1be2f3192446565fdf9c69d401",
        (1800, 980),
        612_723,
        29,
    ),
    "_page_978_Shift_Rule_170_Size_4_to_8_Five_Panel_Row.jpeg": (
        "ADDED_ASSET",
        "G5-A-0076",
        "1957a65d26376106d0a68a12d28a35000d3be7941a350f7bfd7a462c73672008",
        (1860, 440),
        152_661,
        27,
    ),
    "_page_980_Figure_3.jpeg": (
        "REPAIRED_EXISTING_ASSET",
        1098,
        "819837fecdb7f91c5e142c3efd64fa876e2537fc6ae947b261e6fa2265e9db9d",
        (1700, 590),
        335_157,
        37,
    ),
    "_page_980_Life_Elaborate_Structures_Four_Panel_Group.jpeg": (
        "ADDED_ASSET",
        "G5-A-0077",
        "06a272b83b3eefb5740d6f328db2f03ff1527db625231f388d31a32a71f1cd80",
        (1700, 900),
        263_017,
        40,
    ),
    "_page_980_Life_Puffer_Train_Four_Panel_Group.jpeg": (
        "ADDED_ASSET",
        "G5-A-0079",
        "d63b7a94b59c570c8b6b692a0b372156e94b5fdfc7f4b2b01ec52d215cb41a04",
        (1700, 1550),
        276_061,
        42,
    ),
    "_page_980_Life_Spacefiller_Three_Panel_Row.jpeg": (
        "ADDED_ASSET",
        "G5-A-0078",
        "ebd0ba594b0b663e325ecf62007ee84cbc7ecd6f52f994d162c7659da2559c3f",
        (1700, 590),
        152_794,
        41,
    ),
}

REQUIRED_LITERAL_PINS: tuple[tuple[str, str, int], ...] = (
    (
        "rule22-side-block",
        "changing the color of a single cell has no effect after even one step "
        "if the cell has a ■■ block on either side",
        1,
    ),
    ("rule225-initial-strip", "with the initial condition ■■□■", 1),
    ("rule225-background-strip", "repetitions of the block ■□", 1),
    ("rule225-boolean", "Rule 225 can be expressed as ¬ p ⊻ (q ∨ r).", 1),
    (
        "period-blocks",
        "For period 1 the possible blocks are □ and ■■□; for period 2 "
        "■□■□□□ and ■■■■□□.",
        1,
    ),
    ("rule45-background", "background of repeated ■■□ blocks", 1),
    (
        "rule90-density",
        "1/2 (1 - (1 - 2 p))^(2^DigitCount[t, 2, 1])",
        1,
    ),
    (
        "period-ratio-table",
        "| n     | 11 | 13 | 19 | 25 | 27 | 29  | 37    | 41 | 43 | 53      |\n"
        "|-------|----|----|----|----|----|-----|-------|----|----|---------|\n"
        "| ratio | 3  | 5  | 27 | 41 | 19 | 565 | 21255 | 25 | 3  | 1266205 |",
        1,
    ),
    ("source-printed-plain-spacetime-entropy", r"$h \le 2r h_t$", 1),
    ("cyclic-mod-equality", "`Mod[k^t, n] == 1`", 1),
    ("cyclic-gcd-equality", "`GCD[k, n] == 1`", 1),
    ("cyclic-power-equality", "`n == k^s`", 1),
    ("cyclic-spatial-period", "*RotateLeft[list, m] == list*", 1),
    ("cyclic-definition-single-equals", "`m = k^IntegerExponent[n, k]`", 1),
    ("class4-terminal-period", "and 4320.\n", 1),
    (
        "cyclic-terminal-period",
        "`MultiplicativeOrder[k, n/m]` steps.\n",
        1,
    ),
    ("density-terminal-period", "very different behavior.\n", 1),
    (
        "excluded-blocks-column-join",
        "additional excluded blocks with lengths between n and 2n.",
        1,
    ),
    ("rule22-four-to-m", "4^m", 1),
    (
        "endomorphism-square-brackets",
        r"\sigma[a \oplus b] == \sigma[a] \oplus \sigma[b]",
        1,
    ),
    ("regex-alternatives", "`{(0 | 1) ...}`", 1),
    (
        "rule126-list-braces",
        r"\{\{1, 2\}, \{3, 5\}, \{13, 23\}, \{106, 196\}, "
        r"\{2866, 5474\}\}",
        1,
    ),
    ("factor-expression", "Factor[x^(k^n - 1) - 1, Modulus -> k]", 1),
    ("temporal-entropy-label", "dimension $h_t$ for temporal sequences", 1),
)

FORBIDDEN_LITERAL_PINS: tuple[tuple[str, str], ...] = (
    ("fenced-language-tag", "```wl"),
    ("cyclic-mod-single-equals", "$Mod[k^t, n] = 1$"),
    ("cyclic-gcd-single-equals", "GCD[k, n] = 1"),
    ("cyclic-power-single-equals", "$n = k^s$"),
    ("class4-missing-period", "and 4320\n"),
    (
        "cyclic-missing-period-and-trailing-space",
        "`MultiplicativeOrder[k, n/m]` steps \n",
    ),
    ("density-missing-period", "very different behavior\n"),
    (
        "rule90-density-misgrouped",
        "1/2 (1 - (1 - 2 p)^(2^DigitCount[t, 2, 1]))",
    ),
    ("invented-period-ratio-entry", "| 31 |"),
    ("invented-spatial-entropy-subscript", r"$h_x \le 2r h_t$"),
    (
        "excluded-blocks-false-paragraph",
        "additional excluded blocks with lengths\n\nbetween n and 2n.",
    ),
    ("rule22-lost-exponent", "two black squares 4 m positions apart"),
    (
        "endomorphism-parentheses",
        r"\sigma(a \oplus b) = \sigma(a) \oplus \sigma(b)",
    ),
    ("regex-division", "{(0/1)...}"),
    ("rule126-parenthesized-pairs", r"\{(1, 2), (3, 5), (13, 23)"),
    ("factor-split-markup", "Factor [ $x^{k^n-1}$"),
    ("temporal-entropy-plain", "dimension h_t for temporal sequences"),
    ("temporary-png-reference", ".png)"),
    ("n07-title-leak", "Mechanisms in Programs and Nature"),
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def rows_sha256(rows: Iterable[dict[str, Any]]) -> str:
    materialized = list(rows)
    payload = b""
    if materialized:
        payload = b"\n".join(canonical_bytes(row) for row in materialized) + b"\n"
    return build.sha256(payload)


def row_hash_sequence_sha256(rows: Iterable[dict[str, Any]]) -> str:
    hashes = [build.sha256(canonical_bytes(row)) for row in rows]
    return build.sha256(("\n".join(hashes) + "\n").encode("ascii"))


def markdown_inventories(markdown: str) -> dict[str, list[dict[str, Any]]]:
    lines = markdown.splitlines()
    inventories: dict[str, list[dict[str, Any]]] = {
        "headings": [],
        "labels": [],
        "code_fences": [],
        "inline_code": [],
        "image_references": [],
    }
    fenced_lines: set[int] = set()
    active: dict[str, Any] | None = None
    for line_number, line in enumerate(lines, 1):
        match = re.match(r"^(`{3,})(.*)$", line)
        if active is None and match is not None:
            active = {
                "start_line": line_number,
                "delimiter": match.group(1),
                "info": match.group(2).strip(),
                "content": [],
            }
            fenced_lines.add(line_number)
            continue
        if active is not None:
            fenced_lines.add(line_number)
            if match is not None and match.group(1) == active["delimiter"] and not match.group(2).strip():
                content = "\n".join(active["content"])
                inventories["code_fences"].append(
                    {
                        "ordinal": len(inventories["code_fences"]) + 1,
                        "start_line": active["start_line"],
                        "end_line": line_number,
                        "delimiter": active["delimiter"],
                        "info": active["info"],
                        "content_lines": len(active["content"]),
                        "content_sha256": build.sha256(content.encode("utf-8")),
                    }
                )
                active = None
            else:
                active["content"].append(line)
    if active is not None:
        raise AssertionError(f"unclosed code fence at line {active['start_line']}")

    heading_re = re.compile(r"^(#{1,6}) (.+)$")
    label_re = re.compile(r"^■\s+\*\*(.+?)\*\*(?:\s|$)")
    image_re = re.compile(r"!\[([^\]]*)\]\(([^)\n]+)\)")
    inline_re = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")
    for line_number, line in enumerate(lines, 1):
        if line_number in fenced_lines:
            continue
        heading = heading_re.match(line)
        if heading is not None:
            inventories["headings"].append(
                {
                    "ordinal": len(inventories["headings"]) + 1,
                    "line": line_number,
                    "level": len(heading.group(1)),
                    "text": heading.group(2),
                    "exact": line,
                }
            )
        if line.startswith("■"):
            label = label_re.match(line)
            if label is None:
                raise AssertionError(f"square note lacks bold label at line {line_number}")
            inventories["labels"].append(
                {
                    "ordinal": len(inventories["labels"]) + 1,
                    "line": line_number,
                    "label": label.group(1),
                }
            )
        for match in inline_re.finditer(line):
            inventories["inline_code"].append(
                {
                    "ordinal": len(inventories["inline_code"]) + 1,
                    "line": line_number,
                    "column": match.start() + 1,
                    "text": match.group(1),
                }
            )
        for match in image_re.finditer(line):
            inventories["image_references"].append(
                {
                    "ordinal": len(inventories["image_references"]) + 1,
                    "line": line_number,
                    "column": match.start() + 1,
                    "alt": match.group(1),
                    "path": match.group(2),
                    "exact": match.group(0),
                }
            )
    return inventories


class NotesForChapter6Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.document = next(row for row in cls.documents if row["id"] == "N06")
        cls.n05_document = next(row for row in cls.documents if row["id"] == "N05")
        cls.n07_document = next(row for row in cls.documents if row["id"] == "N07")
        cls.path = build.safe_relative_path(cls.document["output_path"], suffix=".md")
        cls.rendered_bytes = build.document_bytes(
            cls.raw, cls.documents, cls.corrections
        )[cls.path]
        cls.rendered = cls.rendered_bytes.decode("utf-8")
        cls.output_path = build.OUTPUT_ROOT / Path(cls.path)
        cls.n06_corrections = [
            row for row in cls.corrections if row["document_id"] == "N06"
        ]
        cls.n06_images = [row for row in cls.images if row["document_id"] == "N06"]
        cls.n06_added = [
            row for row in cls.added_assets if row["document_id"] == "N06"
        ]
        cls.inventories = markdown_inventories(cls.rendered)
        cls.references = [
            row["path"] for row in cls.inventories["image_references"]
        ]

    def test_exact_range_corrections_target_and_adjacent_boundaries(self) -> None:
        self.assertEqual(
            (
                self.document["raw_start_line"],
                self.document["raw_end_line"],
                self.document["raw_start_byte"],
                self.document["raw_end_byte_exclusive"],
                self.document["raw_line_count"],
                self.document["raw_byte_count"],
                self.document["raw_segment_sha256"],
                self.document["authoritative_pdf_start_page"],
                self.document["authoritative_pdf_end_page"],
                self.document["authoritative_printed_start"],
                self.document["authoritative_printed_end"],
            ),
            (
                14_199,
                14_847,
                2_002_646,
                2_090_568,
                649,
                87_922,
                "6dafcf5b8e8e94fff0ccc7962f3a794b1eaef33338860a50a7aa00b0bdae4a8e",
                963,
                982,
                "947",
                "966",
            ),
        )
        segment = self.raw[2_002_646:2_090_568]
        self.assertEqual(build.sha256(segment), self.document["raw_segment_sha256"])
        self.assertEqual(
            build.sha256(segment[:256]),
            "d7be311d059597c30a465a5b23806deacc6b6cdae7f74cc330f42c7d2d0390d8",
        )
        self.assertEqual(
            build.sha256(segment[-256:]),
            "8304b693e586f85c66065bdf16dc2a550e0849234277efc8129a4dbac79c3861",
        )
        self.assertEqual(segment.splitlines()[0].decode(), self.document["heading_text"])

        # Later note chapters append corrections globally; N06's owned slice is
        # immutable and remains the exact guard here.
        self.assertGreaterEqual(len(self.corrections), 1_401)
        self.assertEqual(len(self.n06_corrections), 188)
        self.assertEqual(
            [row["id"] for row in self.n06_corrections],
            [f"G5-C-{number:04d}" for number in range(1214, 1402)],
        )
        self.assertEqual(
            rows_sha256(self.n06_corrections), EXPECTED_CORRECTION_ROWS_SHA256
        )
        self.assertEqual(
            row_hash_sequence_sha256(self.n06_corrections),
            EXPECTED_CORRECTION_ROW_HASH_SEQUENCE,
        )
        previous_end = self.document["raw_start_byte"]
        by_id = {row["id"]: row for row in self.n06_corrections}
        self.assertEqual(
            (
                by_id["G5-C-1262"]["raw_start_byte"],
                by_id["G5-C-1262"]["after"],
            ),
            (
                2_022_065,
                "| n     | 11 | 13 | 19 | 25 | 27 | 29  | 37    | 41 | 43 | 53      |\n"
                "|-------|----|----|----|----|----|-----|-------|----|----|---------|\n"
                "| ratio | 3  | 5  | 27 | 41 | 19 | 565 | 21255 | 25 | 3  | 1266205 |\n",
            ),
        )
        self.assertEqual(
            (
                by_id["G5-C-1292"]["raw_start_byte"],
                by_id["G5-C-1292"]["before"],
                by_id["G5-C-1292"]["after"],
            ),
            (
                2_035_208,
                "$$1/2(1-(1-2p))^{2}$$\n",
                "```\n1/2 (1 - (1 - 2 p))^(2^DigitCount[t, 2, 1])\n```\n",
            ),
        )
        self.assertIn(r"$h \le 2r h_t$", self.rendered)
        self.assertNotIn(r"$h_x \le 2r h_t$", self.rendered)

        # C1392-C1399 are append-only visual guards and C1400-C1401 are fresh
        # source-residual guards. Their raw spans occur between earlier text
        # guards. Sort only for the non-overlap proof; manifest order remains
        # pinned above.
        for row in sorted(
            self.n06_corrections, key=lambda correction: correction["raw_start_byte"]
        ):
            with self.subTest(correction=row["id"]):
                self.assertEqual(set(row), build.CORRECTION_FIELDS | {"raw_line"})
                self.assertEqual(row["document_id"], "N06")
                self.assertIsInstance(row["expected_count"], int)
                self.assertGreaterEqual(row["expected_count"], 1)
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                self.assertTrue(row["reason"].strip())
                self.assertNotIn("/tmp", row["reason"])
                start = row["raw_start_byte"]
                before = row["before"].encode("utf-8")
                end = start + len(before)
                local = start - self.document["raw_start_byte"]
                self.assertGreaterEqual(start, previous_end)
                self.assertLessEqual(end, self.document["raw_end_byte_exclusive"])
                self.assertEqual(self.raw[start:end], before)
                self.assertEqual(segment.count(before), row["expected_count"])
                self.assertEqual(
                    row["raw_line"],
                    self.document["raw_start_line"] + segment[:local].count(b"\n"),
                )
                pages = [
                    int(value)
                    for value in re.findall(r"pdf:(\d{4})", row["authoritative_location"])
                ]
                printed = [
                    int(value)
                    for value in re.findall(
                        r"printed:(\d{3})", row["authoritative_location"]
                    )
                ]
                self.assertTrue(pages)
                self.assertEqual(printed, [page - 16 for page in pages])
                self.assertTrue(all(963 <= page <= 981 for page in pages))
                previous_end = end

        self.assertEqual(len(self.rendered_bytes), EXPECTED_TARGET_BYTES)
        self.assertEqual(self.rendered_bytes.count(b"\n"), EXPECTED_TARGET_LINES)
        self.assertTrue(self.rendered_bytes.endswith(b"\n"))
        self.assertEqual(build.sha256(self.rendered_bytes), EXPECTED_TARGET_SHA256)
        self.assertEqual(self.output_path.read_bytes(), self.rendered_bytes)
        self.assertEqual(
            validate.independent_document_bytes(
                self.raw, self.documents, self.corrections
            )[self.path],
            self.rendered_bytes,
        )

        self.assertEqual(
            self.n05_document["raw_end_byte_exclusive"],
            self.document["raw_start_byte"],
        )
        self.assertEqual(
            self.n05_document["raw_end_line"] + 1, self.document["raw_start_line"]
        )
        self.assertEqual(
            self.document["raw_end_byte_exclusive"],
            self.n07_document["raw_start_byte"],
        )
        self.assertEqual(
            self.document["raw_end_line"] + 1, self.n07_document["raw_start_line"]
        )
        n07 = self.raw[2_090_568 : self.n07_document["raw_end_byte_exclusive"]]
        self.assertEqual(
            build.sha256(n07[:256]),
            "6fb51ed7e49f81225291de3c248e5c113f70ca605b32642727e13f04d2494102",
        )
        self.assertNotIn(self.n05_document["title"], self.rendered)
        self.assertNotIn(self.n07_document["title"], self.rendered)

    def test_markdown_structure_plain_fences_and_controls(self) -> None:
        expected_counts = {
            "headings": 9,
            "labels": 86,
            "code_fences": 35,
            "inline_code": EXPECTED_INLINE_CODE_COUNT,
            "image_references": 42,
        }
        for name, expected_count in expected_counts.items():
            with self.subTest(inventory=name):
                rows = self.inventories[name]
                self.assertEqual(len(rows), expected_count)
                self.assertEqual(rows_sha256(rows), EXPECTED_INVENTORY_HASHES[name])
        self.assertEqual(
            [row["exact"] for row in self.inventories["headings"]],
            EXPECTED_HEADINGS,
        )
        self.assertEqual(
            [row["level"] for row in self.inventories["headings"]],
            [2] + [3] * 8,
        )
        self.assertTrue(
            all(
                row["delimiter"] == "```" and not row["info"]
                for row in self.inventories["code_fences"]
            )
        )
        self.assertEqual(len(set(self.references)), 42)
        self.assertTrue(
            all(name.endswith(".jpeg") and "/" not in name for name in self.references)
        )
        controls = [
            (index, ord(character))
            for index, character in enumerate(self.rendered)
            if ord(character) < 32 and character not in "\n\t"
        ]
        self.assertEqual(controls, [])
        self.assertEqual(
            [
                line_number
                for line_number, line in enumerate(self.rendered.splitlines(), 1)
                if line.endswith((" ", "\t"))
            ],
            [164, 522],
        )

    def test_sixty_four_image_rows_and_thirty_six_changes_are_exact(self) -> None:
        self.assertEqual(len(self.n06_images), 64)
        self.assertEqual(
            [row["ordinal"] for row in self.n06_images], list(range(1048, 1112))
        )
        self.assertEqual(rows_sha256(self.n06_images), EXPECTED_IMAGE_ROWS_SHA256)
        changed = [
            row
            for row in self.n06_images
            if "reference_disposition" in row
            or "repaired_asset_relative_path" in row
        ]
        self.assertEqual(
            [row["ordinal"] for row in changed], list(EXPECTED_CHANGED_ORDINALS)
        )
        self.assertEqual(len(changed), 36)
        self.assertEqual(
            rows_sha256(changed), EXPECTED_CHANGED_IMAGE_ROWS_SHA256
        )
        redundant = [row for row in changed if "reference_disposition" in row]
        repaired = [row for row in changed if "repaired_asset_relative_path" in row]
        self.assertEqual((len(redundant), len(repaired)), (30, 6))
        self.assertEqual(
            [row["ordinal"] for row in repaired], list(EXPECTED_REPAIRED_ORDINALS)
        )
        groups: dict[str, list[int]] = defaultdict(list)
        for row in redundant:
            self.assertEqual(
                row["reference_disposition"], build.REDUNDANT_REFERENCE_DISPOSITION
            )
            self.assertEqual(
                build.REFERENCE_DISPOSITION_FIELDS & set(row),
                build.REFERENCE_DISPOSITION_FIELDS,
            )
            self.assertEqual(row["reference_reviewer_type"], "agent")
            self.assertEqual(
                row["reference_verification_status"], "SOURCE_VERIFIED"
            )
            matches = re.findall(r"G5-A-\d{4}", row["reference_reason"])
            self.assertEqual(len(matches), 1)
            groups[matches[0]].append(row["ordinal"])
            self.assertNotIn(Path(row["asset_relative_path"]).name, self.references)
        self.assertEqual(
            {key: tuple(values) for key, values in groups.items()},
            EXPECTED_COMPOSITE_GROUPS,
        )
        for row in repaired:
            self.assertEqual(
                build.REPAIRED_IMAGE_FIELDS & set(row), build.REPAIRED_IMAGE_FIELDS
            )
            self.assertNotIn("reference_disposition", row)
            self.assertEqual(
                Path(row["repaired_asset_relative_path"]).name,
                Path(row["asset_relative_path"]).name,
            )

        retained = [
            Path(row["asset_relative_path"]).name
            for row in self.n06_images
            if "reference_disposition" not in row
        ]
        added_names = {Path(row["asset_relative_path"]).name for row in self.n06_added}
        self.assertEqual((len(retained), len(added_names)), (34, 8))
        self.assertEqual(set(self.references), set(retained) | added_names)
        self.assertEqual(Counter(self.references), Counter(set(self.references)))
        for row in self.n06_images:
            basename = Path(row["asset_relative_path"]).name
            output = build.OUTPUT_ROOT / Path(self.path).parent / basename
            expected_sha = row.get("repaired_asset_sha256", row["asset_sha256"])
            with self.subTest(mapped_output=basename):
                self.assertTrue(output.is_file())
                self.assertEqual(build.sha256(output.read_bytes()), expected_sha)

    def test_eight_additions_and_fourteen_special_assets_are_exact(self) -> None:
        self.assertEqual(
            [row["id"] for row in self.n06_added],
            [f"G5-A-{number:04d}" for number in range(72, 80)],
        )
        self.assertEqual(rows_sha256(self.n06_added), EXPECTED_ADDED_ROWS_SHA256)
        added_by_path = {row["asset_relative_path"]: row for row in self.n06_added}
        repaired_by_path = {
            row["repaired_asset_relative_path"]: row
            for row in self.n06_images
            if "repaired_asset_relative_path" in row
        }
        self.assertEqual((len(added_by_path), len(repaired_by_path)), (8, 6))
        self.assertFalse(set(added_by_path) & set(repaired_by_path))
        expected_paths = {f"goal-5/assets/N06/{name}" for name in EXPECTED_ASSETS}
        self.assertEqual(set(added_by_path) | set(repaired_by_path), expected_paths)

        for relative in sorted(expected_paths):
            basename = Path(relative).name
            role, source_key, digest, dimensions, byte_count, position = EXPECTED_ASSETS[
                basename
            ]
            source = REPO_ROOT / relative
            output = build.OUTPUT_ROOT / Path(self.path).parent / basename
            payload = source.read_bytes()
            with self.subTest(asset=basename):
                self.assertEqual(len(payload), byte_count)
                self.assertEqual(build.sha256(payload), digest)
                self.assertEqual(build.jpeg_dimensions(payload), dimensions)
                self.assertEqual(output.read_bytes(), payload)
                self.assertEqual(self.references[position - 1], basename)
                if role == "ADDED_ASSET":
                    row = added_by_path[relative]
                    self.assertEqual(row["id"], source_key)
                    self.assertEqual(set(row), build.ADDED_ASSET_FIELDS)
                    self.assertEqual(row["asset_sha256"], digest)
                    self.assertEqual(
                        (row["width_px"], row["height_px"]), dimensions
                    )
                else:
                    row = repaired_by_path[relative]
                    self.assertEqual(row["ordinal"], source_key)
                    self.assertEqual(row["repaired_asset_sha256"], digest)
                    self.assertEqual(
                        (row["repaired_width_px"], row["repaired_height_px"]),
                        dimensions,
                    )
                self.assertEqual(row.get("reviewer_type", "agent"), "agent")
                self.assertEqual(
                    row.get("verification_status", "SOURCE_VERIFIED"),
                    "SOURCE_VERIFIED",
                )

    def test_eight_guarded_visual_reference_substitutions_are_exact(self) -> None:
        guards = {row["id"]: row for row in self.n06_corrections}
        self.assertEqual(
            list(EXPECTED_VISUAL_CORRECTION_GUARDS),
            [f"G5-C-{number:04d}" for number in range(1392, 1400)],
        )
        for guard_id, expected in EXPECTED_VISUAL_CORRECTION_GUARDS.items():
            row = guards[guard_id]
            image = expected["image"]
            addition_id = expected["addition_id"]
            before_payload = row["before"].encode("utf-8")
            after_payload = row["after"].encode("utf-8")
            partials = re.findall(r"!\[\]\(([^)\n]+)\)", row["before"])
            with self.subTest(visual_correction_guard=guard_id):
                self.assertEqual(row["raw_line"], expected["raw_line"])
                self.assertEqual(row["raw_start_byte"], expected["raw_start_byte"])
                self.assertEqual(len(before_payload), expected["before_bytes"])
                self.assertEqual(
                    build.sha256(before_payload), expected["before_sha256"]
                )
                self.assertEqual(len(after_payload), expected["after_bytes"])
                self.assertEqual(build.sha256(after_payload), expected["after_sha256"])
                self.assertEqual(
                    build.sha256(canonical_bytes(row)), expected["row_sha256"]
                )
                self.assertEqual(len(partials), expected["partial_count"])
                self.assertEqual(len(set(partials)), expected["partial_count"])
                self.assertEqual(row["after"], f"![]({image})")
                self.assertIn(addition_id, row["authoritative_location"])
                self.assertIn(addition_id, row["reason"])
                self.assertTrue(row["reason"].startswith("Visual source repair:"))
                self.assertEqual(self.rendered.count(row["after"]), 1)
                self.assertEqual(self.references[expected["position"] - 1], image)
                for partial in partials:
                    self.assertNotIn(f"![]({partial})", self.rendered)

    def test_high_risk_source_and_technical_literals(self) -> None:
        self.assertEqual(
            len(REQUIRED_LITERAL_PINS) + len(FORBIDDEN_LITERAL_PINS), 43
        )
        for pin_id, literal, expected_count in REQUIRED_LITERAL_PINS:
            with self.subTest(required_pin=pin_id):
                self.assertEqual(self.rendered.count(literal), expected_count)
        for pin_id, literal in FORBIDDEN_LITERAL_PINS:
            with self.subTest(forbidden_pin=pin_id):
                self.assertNotIn(literal, self.rendered)


if __name__ == "__main__":
    unittest.main()
