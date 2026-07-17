from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import unittest
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


# The environment override makes it possible to exercise this repo-ready file
# before copying it into goal-5/tests. In normal repository use, parents[2] is
# the repository root and no override is needed.
REPO_ROOT = Path(
    os.environ.get("ANKOS_REPO_ROOT", Path(__file__).resolve().parents[2])
).resolve()
GOAL_DIR = REPO_ROOT / "goal-5"
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402
import validate  # noqa: E402


EXPECTED_TARGET_BYTES = 86_868
EXPECTED_TARGET_LINES = 757
EXPECTED_TARGET_SHA256 = (
    "e1e7e6c733ee874c1d7dff7fdb86a18f36da5d7e55ac67a5a76f8f4fb1dcddaa"
)
EXPECTED_CORRECTION_ROWS_SHA256 = (
    "8c702c2f67badf3c39ce84266d4e0caf31a7001a7dff3ec7d3e0e0f4abdab2a2"
)
EXPECTED_CORRECTION_ROW_HASH_SEQUENCE = (
    "8bfce4fe58ab2ad6951f2649ad7b0fe759dea6db02bba164522d4da59c18b94e"
)
EXPECTED_REPLACEMENT_ROWS_SHA256 = (
    "759e80f6611133a7e20f5ffdc7a3781aa891c3b7ac029da5d90b7fa1cb444e89"
)
EXPECTED_REPLACEMENT_ROW_HASH_SEQUENCE = (
    "80d45ffda23c0926fe0ae5f8ffddd64f07f8538d51ce4621ced2ff7aa39ae5bc"
)
EXPECTED_ADDED_ROWS_SHA256 = (
    "96e151ad6b159903e20716035569abcee81aa391f3e5088b37b162f00f13850d"
)
EXPECTED_ADDED_ROW_HASH_SEQUENCE = (
    "6ee01a32d1468ada676a042ca2fd797baf966201da1802d7826bd2637d33e460"
)
EXPECTED_ASSET_SEQUENCE_SHA256 = (
    "01dedacd74d45a72e34a2a60c297687a3ff8ca1309f26dbbda3564bd907430c8"
)
EXPECTED_INVENTORY_HASHES = {
    "headings": "30621eb4120dd4403fb68439da962333e8a10fb2670521b859c36bfbad1f9eaa",
    "labels": "03736e98a47c0bb637a9d5919476fc113777acafe1e09fdff6b08a935adf717f",
    "code_fences": "75b75c1c4b4fd3a6d8b46f4a4651ccb8ffaf2b544dd38b3f46ff71b0c80f79ae",
    "inline_code": "763f907d4de98c607e333b311d4acd10119bef7586493f74735e3a7da889ec4d",
    "image_references": "511126a3326caa2fde8a6631a98fd8e45160882eb612c712a2a44e32353cb34b",
}
EXPECTED_COMBINED_STRUCTURE_SHA256 = (
    "d5045324145180c8c48ee6a4ca0dcf3a0652f2c5648de94185394237030c27c6"
)
EXPECTED_MATH_SPANS_SHA256 = (
    "de8de1634be899c777cb6d27d4a93ade72e1d09b1171ecbaae7336483ba9e3dd"
)

EXPECTED_HEADINGS = [
    "## Two Dimensions and Beyond",
    "### Introduction",
    "### Cellular Automata",
    "### Turing Machines",
    "### Substitution Systems and Fractals",
    "### Network Systems",
    "### Multiway Systems",
    "### Systems Based on Constraints",
]

EXPECTED_REPLACEMENT_ORDINALS = (
    989,
    990,
    991,
    992,
    993,
    995,
    996,
    997,
    998,
    999,
    1000,
    1002,
    1003,
    1004,
    1005,
    1006,
    1007,
    1008,
    1010,
    1013,
    1015,
    1020,
    1021,
    1022,
    1023,
    1024,
    1025,
    1028,
    1029,
    1030,
    1031,
    1037,
    1038,
    1040,
    1041,
    1042,
    1043,
)
EXPECTED_COMPOSITE_GROUPS = {
    "G5-A-0061": (989, 990, 991, 992, 993),
    "G5-A-0062": (996, 997, 998, 999, 1000),
    "G5-A-0063": (1002, 1003, 1004),
    "G5-A-0064": (1005, 1006, 1007, 1008),
    "G5-A-0066": (1020, 1021, 1022),
    "G5-A-0067": (1023, 1024, 1025),
    "G5-A-0068": (1028, 1029, 1030, 1031),
    "G5-A-0070": (1037, 1038),
    "G5-A-0071": (1040, 1041, 1042, 1043),
}
EXPECTED_REPAIRED_ORDINALS = (995, 1010, 1013, 1015)

# basename: (role, source key, digest, (width, height), bytes, reference position)
EXPECTED_ASSETS: dict[str, tuple[str, str | int, str, tuple[int, int], int, int]] = {
    "_page_943_Growth_Rules_Five_Panel_Row.jpeg": (
        "ADDED_ASSET",
        "G5-A-0061",
        "42a2e0c473b1e2557de66544717a196cf60638b0fbaf03ea526cc8681d4798b9",
        (1710, 420),
        108_486,
        1,
    ),
    "_page_943_Picture_21.jpeg": (
        "REPAIRED_EXISTING_ASSET",
        995,
        "0ee7e4eba4444595d291bf42af0ef18d654039e824ffd0aeba39feb17d740d1c",
        (1720, 520),
        141_065,
        3,
    ),
    "_page_944_3D_Projections_Four_Panel_Row.jpeg": (
        "ADDED_ASSET",
        "G5-A-0064",
        "2d310b84476577d4cd02e2108ab9b4ca4a0b5bd34464bdf6b58ed5085c7e2368",
        (1740, 510),
        159_857,
        7,
    ),
    "_page_944_Code_174826_Three_Step_Row.jpeg": (
        "ADDED_ASSET",
        "G5-A-0063",
        "a325aa1564e83e20eea5d029fdd1a93e792c969528308581da457656b36e787e",
        (1740, 630),
        243_798,
        6,
    ),
    "_page_944_Simple_Rules_Five_Panel_Row.jpeg": (
        "ADDED_ASSET",
        "G5-A-0062",
        "4f7eddafce93b5b08d877c6c8b632f0e776a57c19c85fefab7e021399ae37300",
        (1710, 360),
        105_173,
        4,
    ),
    "_page_945_Picture_4.jpeg": (
        "REPAIRED_EXISTING_ASSET",
        1010,
        "55097994885d3e739cb7f2e1c3059f2100ffd9581c1ce337583e35f9f28af2ff",
        (1710, 760),
        424_621,
        9,
    ),
    "_page_946_Turing_3_State_Rule_Strip.jpeg": (
        "ADDED_ASSET",
        "G5-A-0065",
        "390f7cecc49244eada15d59fca21a7c3b62019fd36cfc22111399a069e50c496",
        (900, 117),
        15_041,
        12,
    ),
    "_page_947_Figure_4.jpeg": (
        "REPAIRED_EXISTING_ASSET",
        1013,
        "f6ad4d9d5d62006e5882be9a29dd11fae0a3706df00dbbbe2e9dba394d435d90",
        (1710, 970),
        361_966,
        13,
    ),
    "_page_947_Picture_14.jpeg": (
        "REPAIRED_EXISTING_ASSET",
        1015,
        "ddd661297926a86b52f90d3285448491ca5db400936e78f20694615d989832f0",
        (1740, 1210),
        373_179,
        15,
    ),
    "_page_950_Mandelbrot_Neighbor_Systems_Three_Panel_Row.jpeg": (
        "ADDED_ASSET",
        "G5-A-0066",
        "ac149e2197c77f11241612b05024e741912a3f6b9e9cd9ea6716c3f8392947b7",
        (1710, 620),
        129_632,
        20,
    ),
    "_page_951_Sequential_Networks_Three_Panel_Row.jpeg": (
        "ADDED_ASSET",
        "G5-A-0067",
        "bdab23f6741770a35a6a548b0c9c992fd02db01b711f7f47aa1bf963e6e8e2c3",
        (1710, 1040),
        397_529,
        21,
    ),
    "_page_952_Multiway_Steps_Four_Panel_Row.jpeg": (
        "ADDED_ASSET",
        "G5-A-0068",
        "b738f6561ebe0c7c703cc5f5069d1293d10ea777bc58c52b849395208c45bc7a",
        (1680, 500),
        134_830,
        24,
    ),
    "_page_957_Constraint_Template_Icons_and_Ratios.jpeg": (
        "ADDED_ASSET",
        "G5-A-0069",
        "cfbf247bc43cfd70d28b0d5452ef08a6cc895836dab11337fb0e1082ffe872ad",
        (850, 105),
        15_903,
        28,
    ),
    "_page_958_Polyomino_Sets_Two_Panel_Row.jpeg": (
        "ADDED_ASSET",
        "G5-A-0070",
        "bb506029d1cff11bd14b5582264001fe79df69a64eac73d1b2c76172f27e5fd4",
        (1740, 420),
        51_153,
        31,
    ),
    "_page_959_Linear_Diophantine_Four_Panel_Row.jpeg": (
        "ADDED_ASSET",
        "G5-A-0071",
        "00b53946fd315a3e5291bbbc9a636e1e8c4cfea48aa81d3884b80cb50e1b557a",
        (1740, 500),
        215_193,
        33,
    ),
}

REQUIRED_LITERAL_PINS: tuple[tuple[str, str, int], ...] = (
    (
        "langton-ant-rule",
        "{s_, c_} :> With[{sp = s (2 c - 1) I},\n  {sp, 1 - c, {Re[sp], Im[sp]}}]",
        1,
    ),
    ("sierpinski-imaginary-offset", "Nest[{2 #, 2 # + 1, 2 # + I} &, {0}, n]", 1),
    (
        "dragon-rule-imaginary-list",
        "(0.296 - 0.57 I) z - 0.067 I - I {1.04, 0.237}",
        1,
    ),
    ("complex-map-rule-189", "f[z_] = 1/2 (1 - I) {z + 1/2, z - 1/2}", 1),
    ("complex-map-transformed-rule", "f[z_] = (1 - I) {z + 1, z}", 1),
    ("complex-map-rule-190", "f[z_] = 1/2 (1 - I) {I z + 1/2, z - 1/2}", 1),
    ("network-pattern-double-blank", "d[{__, 1, p : ((0) ..), 0}]", 1),
    ("network-pattern-zero-or-more", "q : ((0) ...), 1, 0", 1),
    ("nonlinear-threshold-source", "$r > 6$", 1),
    ("source-ocr-fidelity-wh", "shows wh different strings", 1),
    ("fermat-identity", "`x^n + y^n == z^n`", 1),
    ("cubes-3456-identity", "`3^3 + 4^3 + 5^3 == 6^3`", 1),
    ("cubes-1689-identity", "`1^3 + 6^3 + 8^3 == 9^3`", 1),
    (
        "fourth-powers-identity",
        "`95800^4 + 217519^4 + 414560^4 == 422481^4`",
        1,
    ),
    ("mobile-rule-count", "$(4k)^{k^5}$", 1),
    (
        "sierpinski-binomial-square-array",
        "`Mod[Array[Binomial, {2, 2}^n, 0], 2]`",
        1,
    ),
    (
        "sierpinski-bitand-square-array",
        "`1 - Sign[Array[BitAnd, {2, 2}^n, 0]]`",
        1,
    ),
    (
        "flat-four-rule-list",
        "`{3 -> {{1, 0}, {3, 2}}, 2 -> {{1}, {3}}, 1 -> {{3, 2}}, 0 -> {{3}}}`",
        1,
    ),
    ("icosahedral-wolfram-relation", "`x^2 == y^3 == (x y)^5 == 1`", 1),
    ("linear-wolfram-equation", "`u == m . v`", 1),
    ("nonlinear-wolfram-equation", "`u == m1 . v + m2 . v^2`", 1),
    ("diophantine-wolfram-equation", "`x^3 + x + 1 == 0`", 1),
)
FORBIDDEN_LITERAL_PINS: tuple[tuple[str, str], ...] = (
    ("fenced-language-tag", "```wl"),
    ("legacy-corrupt-rule-index", "rule|| 18 - #]|"),
    ("legacy-complex-pattern-markup", "z_{-}"),
    ("lowercase-imaginary-unit", "(1-i)"),
    (
        "dragon-rule-lost-imaginary-factor",
        "(0.296 - 0.57 I) z - 0.067 I - {1.04, 0.237}",
    ),
    ("sierpinski-real-offset-regression", "Nest[{2 #, 2 # + 1, 2 # + 1} &"),
    ("editorialized-wh", "shows how different strings"),
    ("wrong-threshold-inequality", r"r \ge 6"),
    ("temporary-png-reference", ".png)"),
    ("n06-title-leak", "Starting from Randomness"),
    ("mobile-rule-lost-superscript", "$(4k)^k$"),
    (
        "sierpinski-binomial-rectangular-array",
        "`Mod[Array[Binomial, {2, 2^n}, 0], 2]`",
    ),
    (
        "sierpinski-bitand-rectangular-array",
        "`1 - Sign[Array[BitAnd, {2, 2^n}, 0]]`",
    ),
    ("nested-singleton-rule-lists", "`{{3 ->"),
    ("mathematical-group-relation", "$x^2 = y^3 = (xy)^5 = 1$"),
    ("mathematical-linear-equation", r"$u = m \cdot v$"),
    (
        "mathematical-nonlinear-equation",
        r"$u = m_1 \cdot v + m_2 \cdot v^2$",
    ),
    ("mathematical-diophantine-equation", "$x^3 + x + 1 = 0$"),
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def jsonl_bytes(rows: Iterable[dict[str, Any]]) -> bytes:
    materialized = list(rows)
    if not materialized:
        return b""
    return b"\n".join(canonical_bytes(row) for row in materialized) + b"\n"


def sequence_sha256(rows: Iterable[dict[str, Any]]) -> str:
    return build.sha256(jsonl_bytes(rows))


def rows_sha256(rows: list[dict[str, Any]]) -> str:
    return sequence_sha256(rows)


def row_hash_sequence_sha256(rows: list[dict[str, Any]]) -> str:
    hashes = [build.sha256(canonical_bytes(row)) for row in rows]
    return build.sha256(("\n".join(hashes) + "\n").encode("ascii"))


def code_fence_inventory(
    lines: list[str],
) -> tuple[list[dict[str, Any]], set[int]]:
    rows: list[dict[str, Any]] = []
    fenced_lines: set[int] = set()
    active: dict[str, Any] | None = None
    for line_number, line in enumerate(lines, 1):
        match = re.match(r"^(`{3,})(.*)$", line)
        if active is None:
            if match is None:
                continue
            active = {
                "start_line": line_number,
                "delimiter": match.group(1),
                "info": match.group(2).strip(),
                "content": [],
                "literal": [line],
            }
            fenced_lines.add(line_number)
            continue
        fenced_lines.add(line_number)
        if match is not None and match.group(1) == active["delimiter"] and not match.group(2).strip():
            active["literal"].append(line)
            content = "\n".join(active["content"])
            literal = "\n".join(active["literal"])
            rows.append(
                {
                    "ordinal": len(rows) + 1,
                    "start_line": active["start_line"],
                    "end_line": line_number,
                    "delimiter": active["delimiter"],
                    "info": active["info"],
                    "content_lines": len(active["content"]),
                    "content_sha256": build.sha256(content.encode("utf-8")),
                    "literal_sha256": build.sha256(literal.encode("utf-8")),
                }
            )
            active = None
        else:
            active["content"].append(line)
            active["literal"].append(line)
    if active is not None:
        raise AssertionError(f"unclosed code fence at line {active['start_line']}")
    return rows, fenced_lines


def inline_code_for_line(line: str, line_number: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    cursor = 0
    while cursor < len(line):
        start = line.find("`", cursor)
        if start < 0:
            break
        run_end = start
        while run_end < len(line) and line[run_end] == "`":
            run_end += 1
        delimiter = line[start:run_end]
        close = line.find(delimiter, run_end)
        if close < 0:
            raise AssertionError(f"unmatched inline code at line {line_number}")
        text = line[run_end:close]
        rows.append(
            {
                "line": line_number,
                "column": start + 1,
                "delimiter_length": len(delimiter),
                "text": text,
                "text_sha256": build.sha256(text.encode("utf-8")),
            }
        )
        cursor = close + len(delimiter)
    return rows


def markdown_inventories(
    markdown: str,
) -> tuple[dict[str, list[dict[str, Any]]], set[int]]:
    lines = markdown.splitlines()
    fences, fenced_lines = code_fence_inventory(lines)
    inventories: dict[str, list[dict[str, Any]]] = {
        "headings": [],
        "labels": [],
        "code_fences": fences,
        "inline_code": [],
        "image_references": [],
    }
    heading_re = re.compile(r"^(#{1,6}) (.+)$")
    label_re = re.compile(r"^■\s+\*\*(.+?)\*\*(?:\s|$)")
    image_re = re.compile(r"!\[([^\]]*)\]\(([^)\n]+)\)")
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
                    "exact_prefix": line[: label.end()].rstrip(),
                }
            )
        for row in inline_code_for_line(line, line_number):
            row["ordinal"] = len(inventories["inline_code"]) + 1
            inventories["inline_code"].append(row)
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
    return inventories, fenced_lines


def math_inventory(markdown: str, fenced_lines: set[int]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(markdown.splitlines(), 1):
        if line_number in fenced_lines:
            continue
        visible = list(line)
        cursor = 0
        while cursor < len(line):
            start = line.find("`", cursor)
            if start < 0:
                break
            run_end = start
            while run_end < len(line) and line[run_end] == "`":
                run_end += 1
            delimiter = line[start:run_end]
            close = line.find(delimiter, run_end)
            if close < 0:
                raise AssertionError(f"unmatched inline code at line {line_number}")
            for index in range(start, close + len(delimiter)):
                visible[index] = " "
            cursor = close + len(delimiter)
        masked = "".join(visible)
        positions = [
            index
            for index, character in enumerate(masked)
            if character == "$" and (index == 0 or masked[index - 1] != "\\")
        ]
        if len(positions) % 2:
            raise AssertionError(f"unbalanced math delimiter at line {line_number}")
        for start, end in zip(positions[::2], positions[1::2]):
            if end == start + 1:
                raise AssertionError(f"empty math span at line {line_number}")
            text = line[start + 1 : end]
            if text != text.strip():
                raise AssertionError(f"math delimiter absorbs edge space at line {line_number}")
            rows.append(
                {
                    "ordinal": len(rows) + 1,
                    "line": line_number,
                    "column": start + 1,
                    "text": text,
                    "text_sha256": build.sha256(text.encode("utf-8")),
                }
            )
    return rows


class NotesForChapter5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.document = next(row for row in cls.documents if row["id"] == "N05")
        cls.n06_document = next(row for row in cls.documents if row["id"] == "N06")
        cls.path = build.safe_relative_path(cls.document["output_path"], suffix=".md")
        cls.rendered_bytes = build.document_bytes(
            cls.raw, cls.documents, cls.corrections
        )[cls.path]
        cls.rendered = cls.rendered_bytes.decode("utf-8")
        cls.output_path = build.OUTPUT_ROOT / Path(cls.path)
        cls.n05_corrections = [
            row for row in cls.corrections if row["document_id"] == "N05"
        ]
        cls.n05_images = [row for row in cls.images if row["document_id"] == "N05"]
        cls.n05_added = [
            row for row in cls.added_assets if row["document_id"] == "N05"
        ]
        cls.inventories, cls.fenced_lines = markdown_inventories(cls.rendered)
        cls.references = [
            row["path"] for row in cls.inventories["image_references"]
        ]

    def test_exact_range_guards_built_target_and_n06_boundary(self) -> None:
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
                13_460,
                14_198,
                1_908_092,
                2_002_646,
                739,
                94_554,
                "2e852a2c414c01f47fad21115dc497f5cb7f51d4651f9d942a61419b38eb641a",
                943,
                962,
                "927",
                "946",
            ),
        )
        segment = self.raw[1_908_092:2_002_646]
        self.assertEqual(build.sha256(segment), self.document["raw_segment_sha256"])

        self.assertEqual(len(self.corrections), 1_213)
        self.assertEqual(len(self.n05_corrections), 164)
        self.assertEqual(
            [row["id"] for row in self.n05_corrections],
            [f"G5-C-{number:04d}" for number in range(1050, 1214)],
        )
        self.assertEqual(rows_sha256(self.n05_corrections), EXPECTED_CORRECTION_ROWS_SHA256)
        self.assertEqual(
            row_hash_sequence_sha256(self.n05_corrections),
            EXPECTED_CORRECTION_ROW_HASH_SEQUENCE,
        )
        previous_end = self.document["raw_start_byte"]
        # Manifest IDs remain append-only, so the final closing guard (C1213)
        # intentionally appears after C1212 even though its raw span is earlier.
        # Sort only for the interval-overlap proof; retain manifest order for the
        # exact row and row-hash-sequence assertions above.
        for row in sorted(
            self.n05_corrections, key=lambda correction: correction["raw_start_byte"]
        ):
            with self.subTest(correction=row["id"]):
                self.assertEqual(set(row), build.CORRECTION_FIELDS | {"raw_line"})
                self.assertEqual(row["document_id"], "N05")
                self.assertEqual(row["expected_count"], 1)
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                self.assertTrue(row["reason"].strip())
                self.assertNotIn("/tmp", row["reason"])
                self.assertNotIn("TMP-N05", json.dumps(row, ensure_ascii=False))
                start = row["raw_start_byte"]
                before = row["before"].encode("utf-8")
                end = start + len(before)
                local = start - self.document["raw_start_byte"]
                self.assertGreaterEqual(start, previous_end)
                self.assertLessEqual(end, self.document["raw_end_byte_exclusive"])
                self.assertEqual(self.raw[start:end], before)
                self.assertEqual(segment.count(before), 1)
                self.assertEqual(
                    row["raw_line"],
                    self.document["raw_start_line"] + segment[:local].count(b"\n"),
                )
                pages = [
                    int(value)
                    for value in re.findall(
                        r"pdf:(\d{4})", row["authoritative_location"]
                    )
                ]
                printed = [
                    int(value)
                    for value in re.findall(
                        r"printed:(\d{3})", row["authoritative_location"]
                    )
                ]
                self.assertTrue(pages)
                self.assertEqual(printed, [page - 16 for page in pages])
                self.assertTrue(all(943 <= page <= 961 for page in pages))
                previous_end = end

        closing_guard = self.n05_corrections[-1]
        self.assertEqual(
            {
                key: closing_guard[key]
                for key in (
                    "id",
                    "document_id",
                    "raw_start_byte",
                    "raw_line",
                    "before",
                    "after",
                    "expected_count",
                    "authoritative_location",
                    "reviewer_type",
                    "verification_status",
                )
            },
            {
                "id": "G5-C-1213",
                "document_id": "N05",
                "raw_start_byte": 1_962_472,
                "raw_line": 13_996,
                "before": "$x^2 = y^3 = (xy)^5 = 1$",
                "after": "`x^2 == y^3 == (x y)^5 == 1`",
                "expected_count": 1,
                "authoritative_location": (
                    "pdf:0954; printed:938; right column, "
                    "icosahedral-group relation"
                ),
                "reviewer_type": "agent",
                "verification_status": "SOURCE_VERIFIED",
            },
        )
        self.assertEqual(len(closing_guard["before"].encode()), 24)
        self.assertEqual(
            build.sha256(closing_guard["before"].encode()),
            "b8295c9f9df648fb2c9d4c29f3b1ebb92ad2359d87476174e0cbd1b7605f3322",
        )
        self.assertEqual(len(closing_guard["after"].encode()), 28)
        self.assertEqual(
            build.sha256(closing_guard["after"].encode()),
            "c06f3e92ffcc4c60db764e8f90e6670dd5d4a2ddaed1f51064d574481225cbcd",
        )
        self.assertEqual(
            build.sha256(closing_guard["reason"].encode()),
            "5150274e32eddac1f0d64c19a42a14a35e245a5a62cef5932f507e25feee4bb7",
        )
        self.assertEqual(
            build.sha256(canonical_bytes(closing_guard)),
            "fb49f69dbec7afb8e199617a43979f0663e40fef9df3e8a6498b7ae8c9c46265",
        )

        self.assertEqual(len(self.rendered_bytes), EXPECTED_TARGET_BYTES)
        self.assertEqual(self.rendered_bytes.count(b"\n"), EXPECTED_TARGET_LINES)
        self.assertEqual(len(self.rendered.splitlines()), EXPECTED_TARGET_LINES)
        self.assertTrue(self.rendered_bytes.endswith(b"\n"))
        self.assertEqual(build.sha256(self.rendered_bytes), EXPECTED_TARGET_SHA256)
        self.assertEqual(self.output_path.read_bytes(), self.rendered_bytes)
        self.assertEqual(
            validate.independent_document_bytes(
                self.raw, self.documents, self.corrections
            )[self.path],
            self.rendered_bytes,
        )

        n06 = self.n06_document
        self.assertEqual(
            (
                n06["raw_start_byte"],
                n06["raw_end_byte_exclusive"],
                n06["raw_start_line"],
                n06["raw_end_line"],
                n06["raw_segment_sha256"],
                n06["heading_text"],
            ),
            (
                2_002_646,
                2_090_568,
                14_199,
                14_847,
                "6dafcf5b8e8e94fff0ccc7962f3a794b1eaef33338860a50a7aa00b0bdae4a8e",
                "#### Starting from Randomness",
            ),
        )
        self.assertEqual(self.document["raw_end_byte_exclusive"], n06["raw_start_byte"])
        self.assertEqual(self.document["raw_end_line"] + 1, n06["raw_start_line"])
        n06_segment = self.raw[n06["raw_start_byte"] : n06["raw_end_byte_exclusive"]]
        self.assertEqual(build.sha256(n06_segment), n06["raw_segment_sha256"])
        self.assertEqual(
            build.sha256(n06_segment[:256]),
            "d7be311d059597c30a465a5b23806deacc6b6cdae7f74cc330f42c7d2d0390d8",
        )
        self.assertEqual(n06_segment.splitlines()[0].decode(), n06["heading_text"])
        self.assertNotIn(n06["heading_text"], self.rendered)
        self.assertNotIn(n06["title"], self.rendered)

    def test_exact_markdown_inventories_and_math_delimiters(self) -> None:
        expected_counts = {
            "headings": 8,
            "labels": 99,
            "code_fences": 49,
            "inline_code": 78,
            "image_references": 37,
        }
        for name, expected_count in expected_counts.items():
            with self.subTest(inventory=name):
                rows = self.inventories[name]
                self.assertEqual(len(rows), expected_count)
                self.assertEqual(
                    sequence_sha256(rows), EXPECTED_INVENTORY_HASHES[name]
                )
        self.assertEqual(
            [row["exact"] for row in self.inventories["headings"]],
            EXPECTED_HEADINGS,
        )
        self.assertEqual(
            [row["level"] for row in self.inventories["headings"]],
            [2] + [3] * 7,
        )
        self.assertTrue(
            all(
                row["delimiter"] == "```" and not row["info"]
                for row in self.inventories["code_fences"]
            )
        )
        self.assertEqual(len(set(self.references)), 37)
        self.assertTrue(all(name.endswith(".jpeg") and "/" not in name for name in self.references))

        events: list[dict[str, Any]] = []
        for name in ("headings", "labels", "inline_code", "image_references"):
            for row in self.inventories[name]:
                events.append(
                    {
                        "kind": name,
                        "line": row["line"],
                        "column": row.get("column", 1),
                        "ordinal": row["ordinal"],
                        "row_sha256": build.sha256(canonical_bytes(row)),
                    }
                )
        for row in self.inventories["code_fences"]:
            events.append(
                {
                    "kind": "code_fences",
                    "line": row["start_line"],
                    "column": 1,
                    "ordinal": row["ordinal"],
                    "row_sha256": build.sha256(canonical_bytes(row)),
                }
            )
        events.sort(key=lambda row: (row["line"], row["column"], row["kind"]))
        self.assertEqual(len(events), 271)
        self.assertEqual(sequence_sha256(events), EXPECTED_COMBINED_STRUCTURE_SHA256)

        math = math_inventory(self.rendered, self.fenced_lines)
        self.assertEqual(self.rendered.count("$"), 148)
        self.assertNotIn("$$", self.rendered)
        self.assertEqual(len(math), 74)
        self.assertEqual(sequence_sha256(math), EXPECTED_MATH_SPANS_SHA256)
        self.assertTrue(all(row["text"] for row in math))

    def test_replacement_rows_dispositions_and_reference_set_are_exact(self) -> None:
        self.assertEqual(len(self.n05_images), 59)
        self.assertEqual(
            [row["ordinal"] for row in self.n05_images], list(range(989, 1048))
        )
        replacements = [
            row
            for row in self.n05_images
            if "reference_disposition" in row
            or "repaired_asset_relative_path" in row
        ]
        self.assertEqual(
            [row["ordinal"] for row in replacements],
            list(EXPECTED_REPLACEMENT_ORDINALS),
        )
        self.assertEqual(rows_sha256(replacements), EXPECTED_REPLACEMENT_ROWS_SHA256)
        self.assertEqual(
            row_hash_sequence_sha256(replacements),
            EXPECTED_REPLACEMENT_ROW_HASH_SEQUENCE,
        )
        redundant = [row for row in replacements if "reference_disposition" in row]
        repaired = [row for row in replacements if "repaired_asset_relative_path" in row]
        self.assertEqual((len(redundant), len(repaired)), (33, 4))
        self.assertEqual(
            [row["ordinal"] for row in repaired], list(EXPECTED_REPAIRED_ORDINALS)
        )
        groups: dict[str, list[int]] = defaultdict(list)
        for row in redundant:
            with self.subTest(redundant_ordinal=row["ordinal"]):
                self.assertEqual(
                    row["reference_disposition"],
                    build.REDUNDANT_REFERENCE_DISPOSITION,
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
            with self.subTest(repaired_ordinal=row["ordinal"]):
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
            for row in self.n05_images
            if "reference_disposition" not in row
        ]
        added_names = {Path(row["asset_relative_path"]).name for row in self.n05_added}
        self.assertEqual((len(retained), len(added_names)), (26, 11))
        self.assertEqual(set(self.references), set(retained) | added_names)
        self.assertEqual(Counter(self.references), Counter(set(self.references)))

        for row in self.n05_images:
            basename = Path(row["asset_relative_path"]).name
            output = build.OUTPUT_ROOT / Path(self.path).parent / basename
            expected_sha = row.get("repaired_asset_sha256", row["asset_sha256"])
            with self.subTest(mapped_output=basename):
                self.assertTrue(output.is_file())
                self.assertEqual(build.sha256(output.read_bytes()), expected_sha)

    def test_eleven_additions_and_fifteen_special_assets_are_exact(self) -> None:
        self.assertEqual(
            [row["id"] for row in self.n05_added],
            [f"G5-A-{number:04d}" for number in range(61, 72)],
        )
        self.assertEqual(rows_sha256(self.n05_added), EXPECTED_ADDED_ROWS_SHA256)
        self.assertEqual(
            row_hash_sequence_sha256(self.n05_added), EXPECTED_ADDED_ROW_HASH_SEQUENCE
        )
        added_by_path = {row["asset_relative_path"]: row for row in self.n05_added}
        repaired_rows = {
            row["repaired_asset_relative_path"]: row
            for row in self.n05_images
            if "repaired_asset_relative_path" in row
        }
        self.assertEqual((len(added_by_path), len(repaired_rows)), (11, 4))
        self.assertFalse(set(added_by_path) & set(repaired_rows))
        expected_paths = {f"goal-5/assets/N05/{name}" for name in EXPECTED_ASSETS}
        self.assertEqual(set(added_by_path) | set(repaired_rows), expected_paths)

        asset_inventory: list[dict[str, Any]] = []
        for ordinal, relative in enumerate(sorted(expected_paths), 1):
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
                    self.assertEqual(row["reviewer_type"], "agent")
                    self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                    self.assertEqual(row["asset_sha256"], digest)
                    self.assertEqual(
                        (row["width_px"], row["height_px"]), dimensions
                    )
                else:
                    row = repaired_rows[relative]
                    self.assertEqual(row["ordinal"], source_key)
                    self.assertEqual(row["repaired_asset_sha256"], digest)
                    self.assertEqual(
                        (row["repaired_width_px"], row["repaired_height_px"]),
                        dimensions,
                    )
            asset_inventory.append(
                {
                    "ordinal": ordinal,
                    "path": relative,
                    "role": role,
                    "source_key": source_key,
                    "bytes": byte_count,
                    "width_px": dimensions[0],
                    "height_px": dimensions[1],
                    "sha256": digest,
                }
            )
        self.assertEqual(sequence_sha256(asset_inventory), EXPECTED_ASSET_SEQUENCE_SHA256)
        self.assertEqual(
            Counter(row["role"] for row in asset_inventory),
            Counter({"ADDED_ASSET": 11, "REPAIRED_EXISTING_ASSET": 4}),
        )

    def test_forty_high_risk_source_technical_and_visual_pins(self) -> None:
        self.assertEqual(
            len(REQUIRED_LITERAL_PINS) + len(FORBIDDEN_LITERAL_PINS), 40
        )
        for pin_id, literal, expected_count in REQUIRED_LITERAL_PINS:
            with self.subTest(required_pin=pin_id):
                self.assertEqual(self.rendered.count(literal), expected_count)
        for pin_id, literal in FORBIDDEN_LITERAL_PINS:
            with self.subTest(forbidden_pin=pin_id):
                self.assertNotIn(literal, self.rendered)

        # Tie the sixteen closing literals above to the six guards that own
        # them, so an identical string elsewhere cannot mask a guard rollback.
        repair_pins = {
            "G5-C-1088": (
                ("$(4k)^{k^5}$",),
                ("$(4k)^k$",),
            ),
            "G5-C-1095": (
                (
                    "`Mod[Array[Binomial, {2, 2}^n, 0], 2]`",
                    "`1 - Sign[Array[BitAnd, {2, 2}^n, 0]]`",
                ),
                (
                    "`Mod[Array[Binomial, {2, 2^n}, 0], 2]`",
                    "`1 - Sign[Array[BitAnd, {2, 2^n}, 0]]`",
                ),
            ),
            "G5-C-1103": (
                (
                    "`{3 -> {{1, 0}, {3, 2}}, 2 -> {{1}, {3}}, "
                    "1 -> {{3, 2}}, 0 -> {{3}}}`",
                ),
                ("`{{3 ->",),
            ),
            "G5-C-1172": (
                ("`u == m . v`", "`u == m1 . v + m2 . v^2`"),
                (
                    r"$u = m \cdot v$",
                    r"$u = m_1 \cdot v + m_2 \cdot v^2$",
                ),
            ),
            "G5-C-1202": (
                ("`x^3 + x + 1 == 0`",),
                ("$x^3 + x + 1 = 0$",),
            ),
            "G5-C-1213": (
                ("`x^2 == y^3 == (x y)^5 == 1`",),
                ("$x^2 = y^3 = (xy)^5 = 1$",),
            ),
        }
        self.assertEqual(
            tuple(repair_pins),
            (
                "G5-C-1088",
                "G5-C-1095",
                "G5-C-1103",
                "G5-C-1172",
                "G5-C-1202",
                "G5-C-1213",
            ),
        )
        guards = {row["id"]: row for row in self.n05_corrections}
        for guard_id, (required, forbidden) in repair_pins.items():
            guard = guards[guard_id]
            with self.subTest(closing_repair_guard=guard_id):
                for literal in required:
                    self.assertIn(literal, guard["after"])
                for literal in forbidden:
                    self.assertNotIn(literal, guard["after"])
                if guard_id == "G5-C-1213":
                    self.assertTrue(guard["reason"].startswith("Technical repair:"))
                else:
                    self.assertIn("Closing technical repair:", guard["reason"])

    def test_v010_v011_merged_labels_images_and_positions(self) -> None:
        guards = {row["id"]: row for row in self.n05_corrections}
        expected = {
            "G5-C-1087": {
                "raw_line": 13_676,
                "raw_start_byte": 1_925_612,
                "before_sha256": "6398d8c5296bdce5950a34774d2471100711cee2b6e068ca17128f38e60bbe61",
                "after_sha256": "b29ad8a6f6bebcd99ca36696ef69b12116cf0ab4af3f9edf849ccd9d7b16e2ab",
                "after_bytes": 604,
                "label": "■ **Rules based on turning.**",
                "image": "_page_946_Turing_3_State_Rule_Strip.jpeg",
                "position": 12,
            },
            "G5-C-1187": {
                "raw_line": 14_097,
                "raw_start_byte": 1_981_251,
                "before_sha256": "18e7bcd6350afc8b4c0e2057c4171bfbfde47c6a9747ddfceb59ac0cec0fbf84",
                "after_sha256": "510795f57d4ebf484de97cb27417d7fd98208ea9fe64aeddbbf8972e7219a54c",
                "after_bytes": 799,
                "label": "■ **Other types of constraints.**",
                "image": "_page_957_Constraint_Template_Icons_and_Ratios.jpeg",
                "position": 28,
            },
        }
        for guard_id, pin in expected.items():
            row = guards[guard_id]
            with self.subTest(visual_guard=guard_id):
                self.assertEqual(row["raw_line"], pin["raw_line"])
                self.assertEqual(row["raw_start_byte"], pin["raw_start_byte"])
                self.assertEqual(
                    hashlib.sha256(row["before"].encode()).hexdigest(),
                    pin["before_sha256"],
                )
                self.assertEqual(
                    hashlib.sha256(row["after"].encode()).hexdigest(),
                    pin["after_sha256"],
                )
                self.assertEqual(len(row["after"].encode()), pin["after_bytes"])
                self.assertIn(pin["label"], row["after"])
                self.assertIn(f"![]({pin['image']})", row["after"])
                self.assertEqual(self.rendered.count(pin["label"]), 1)
                self.assertEqual(self.rendered.count(f"![]({pin['image']})"), 1)
                self.assertEqual(self.references[pin["position"] - 1], pin["image"])


if __name__ == "__main__":
    unittest.main()
