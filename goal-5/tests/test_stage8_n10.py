#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import unittest
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REPO_ROOT = (
    Path(os.environ["ANKOS_REPO_ROOT"])
    if "ANKOS_REPO_ROOT" in os.environ
    else Path(__file__).resolve().parents[2]
).resolve()
GOAL_DIR = REPO_ROOT / "goal-5"

import sys

sys.path.insert(0, str(GOAL_DIR))
import build  # noqa: E402
import validate  # noqa: E402


FINAL_CORRECTION_COUNT = 555
FINAL_CORRECTION_LAST_NUMBER = 3360
FINAL_TARGET_BYTES = 197_898
FINAL_TARGET_LFS = 1_098
FINAL_TARGET_SHA256 = (
    "96601763703c87874ec465245b55ed68ee5d59ecc560814ca6fbf078660b2e29"
)
FINAL_CORRECTION_ROWS_SHA256 = (
    "313d8f23a9b39e73454ba9d3d5dd4d7218530a2bb26d57c71b596571796c5031"
)
FINAL_CORRECTION_SEQUENCE_SHA256 = (
    "3173ce88f3528c079ca10b840facc94d99aca690de2d4655afbd5a8b7a5659f4"
)
FINAL_IMAGE_ROWS_SHA256 = (
    "dd98fb6f43a8dc8013652fb12c19de395ecf3e81de6dbf07974c7389064d9f13"
)
FINAL_ADDITION_ROWS_SHA256 = (
    "b5471688ec5d919c9924269bb1f36ac14baa16d449f0bbba8487605619613976"
)
EXPECTED_RAW_FIRST_256_SHA256 = (
    "ac88f926f3fbf5f358813924d33e6446823cdfc571274bb09e37ccb86cc42bf5"
)
EXPECTED_RAW_LAST_256_SHA256 = (
    "af15efc9b00c5feedb5f7c3b57fb7fba33de1fb4c64546d42c33ef7886fdc2aa"
)
EXPECTED_LEGACY_TREE = (
    "b9ff7b9b507790f1d519593baf2b2d2f24dd6cd49dc0fe10f0ac629278ea42f4",
    1463,
)
EXPECTED_PDF_SHA256 = (
    "a3cc5dd60e12d6b563aee86ea31a15b03f9cddfd4869b8f965d3a11bbc61a0d6"
)


EXPECTED_HEADINGS = [
    "## Processes of Perception and Analysis",
    "### Defining the Notion of Randomness",
    "### Defining Complexity",
    "### Data Compression",
    "### Irreversible Data Compression",
    "### Visual Perception",
    "### Auditory Perception",
    "### Statistical Analysis",
    "### Cryptography and Cryptanalysis",
    "### Traditional Mathematics and Mathematical Formulas",
    "### Human Thinking",
    "### Higher Forms of Perception and Analysis",
]


EXPECTED_REFERENCES = [
    "_page_1083_Figure_4.jpeg",
    "_page_1085_Figure_16.jpeg",
    "_page_1085_Picture_18.jpeg",
    "_page_1087_Repeat_Probability_Six_Panel_Row.jpeg",
    "_page_1087_2D_Run_Length_Two_Panel_Row.jpeg",
    "_page_1087_Figure_27.jpeg",
    "_page_1088_Walsh_Ordering_Three_Matrix_Row.jpeg",
    "_page_1088_Hadamard_Construction_Five_Stage_Row.jpeg",
    "_page_1088_Picture_26.jpeg",
    "_page_1088_Picture_31.jpeg",
    "_page_1089_Picture_3.jpeg",
    "_page_1089_Figure_11.jpeg",
    "_page_1089_Figure_13.jpeg",
    "_page_1090_Picture_7.jpeg",
    "_page_1091_Visual_History_Four_Panel_Row.jpeg",
    "_page_1091_Picture_11.jpeg",
    "_page_1091_Image_Processing_Four_Panel_Row.jpeg",
    "_page_1092_Picture_6.jpeg",
    "_page_1092_Ordered_Dither_Progression.jpeg",
    "_page_1093_Picture_2.jpeg",
    "_page_1093_Picture_4.jpeg",
    "_page_1093_Picture_6.jpeg",
    "_page_1093_Picture_8.jpeg",
    "_page_1093_Picture_11.jpeg",
    "_page_1093_Picture_13.jpeg",
    "_page_1093_Picture_15.jpeg",
    "_page_1094_Perception_Presentation_Two_Panel_Row.jpeg",
    "_page_1094_Figure_15.jpeg",
    "_page_1097_Figure_7.jpeg",
    "_page_1097_Figure_9.jpeg",
    "_page_1099_Figure_1.jpeg",
    "_page_1101_English_Text_Redundancy_Strip.jpeg",
    "_page_1102_Rule_30_Predecessor_Five_Column_Row.jpeg",
    "_page_1103_Picture_4.jpeg",
    "_page_1103_Figure_7.jpeg",
    "_page_1103_Nonlinear_Feedback_Shift_Register_Two_Panel_Row.jpeg",
    "_page_1104_Backtracking_Four_Component_Group.jpeg",
    "_page_1104_Target_Column_Swatch.jpeg",
    "_page_1104_Picture_9.jpeg",
    "_page_1104_Figure_12.jpeg",
    "_page_1105_Figure_7.jpeg",
    "_page_1105_Quadratic_Residue_Two_Panel_Row.jpeg",
    "_page_1106_Picture_4.jpeg",
    "_page_1106_Arbitrary_Digit_Operations_Three_Panel_Row.jpeg",
    "_page_1107_2D_Rule_90_Eight_Case_Group.jpeg",
    "_page_1107_2D_Rule_150_Eight_Case_Group.jpeg",
    "_page_1108_Continuous_Generalizations_Three_Part_Group.jpeg",
    "_page_1108_Nested_Continuous_Functions_Two_Panel_Row.jpeg",
    "_page_1108_Figure_13.jpeg",
    "_page_1109_Power_Computation_Two_Panel_Row.jpeg",
    "_page_1109_Complex_Powers_Four_Panel_Row.jpeg",
    "_page_1111_Figure_4.jpeg",
    "_page_1111_NAND_Distributions_Three_Panel_Row.jpeg",
    "_page_1112_Picture_5.jpeg",
    "_page_1116_Picture_4.jpeg",
    "_page_1116_Picture_6.jpeg",
    "_page_1120_Games_Between_Programs_Full_Group.jpeg",
]


EXPECTED_RETAINED_REFERENCES = [
    "_page_1083_Figure_4.jpeg", "_page_1085_Figure_16.jpeg",
    "_page_1085_Picture_18.jpeg", "_page_1087_Figure_27.jpeg",
    "_page_1088_Picture_26.jpeg", "_page_1088_Picture_31.jpeg",
    "_page_1089_Picture_3.jpeg", "_page_1089_Figure_11.jpeg",
    "_page_1089_Figure_13.jpeg", "_page_1090_Picture_7.jpeg",
    "_page_1091_Picture_11.jpeg", "_page_1092_Picture_6.jpeg",
    "_page_1093_Picture_2.jpeg", "_page_1093_Picture_4.jpeg",
    "_page_1093_Picture_6.jpeg", "_page_1093_Picture_8.jpeg",
    "_page_1093_Picture_11.jpeg", "_page_1093_Picture_13.jpeg",
    "_page_1093_Picture_15.jpeg", "_page_1094_Figure_15.jpeg",
    "_page_1097_Figure_7.jpeg", "_page_1097_Figure_9.jpeg",
    "_page_1099_Figure_1.jpeg", "_page_1103_Picture_4.jpeg",
    "_page_1103_Figure_7.jpeg", "_page_1104_Picture_9.jpeg",
    "_page_1104_Figure_12.jpeg", "_page_1105_Figure_7.jpeg",
    "_page_1106_Picture_4.jpeg", "_page_1108_Figure_13.jpeg",
    "_page_1111_Figure_4.jpeg", "_page_1112_Picture_5.jpeg",
    "_page_1116_Picture_4.jpeg", "_page_1116_Picture_6.jpeg",
]


EXPECTED_REPAIRS = {
    1390: (
        "_page_1116_Picture_4.jpeg",
        "787056603e15a8246f7206359129dc5f21028c7e87fb693797585e7ab0c9d057",
        (1660, 600),
        55,
    ),
}


EXPECTED_ADDED_REFERENCES = [
    name for name in EXPECTED_REFERENCES if name not in EXPECTED_RETAINED_REFERENCES
]
WHOLLY_MISSING_ADDITIONS = {
    "G5-A-0125", "G5-A-0127", "G5-A-0131", "G5-A-0134", "G5-A-0135"
}


REQUIRED_LITERAL_PINS = [
    "- (a) *Unary.* `Table[0, {n}]`. (Not self-delimited.)",
    "- (b) *Ordinary base 2.* `IntegerDigits[n, 2]`.",
    "- (c) *Length prefixed.* Starting with an ordinary base 2 digit sequence",
    "- (d) *Binary-coded base 3.*",
    "- (e) *Fibonacci encoding.*",
    "- (a) *(Thue-Morse sequence)*",
    "- (b) *(Fibonacci-related sequence)*",
    "- (c) *(Cantor set)*",
    "- (d) *(Period-doubling sequence)*",
    r"$\phi[j][t-1, \omega]$",
    r"$(1-\lambda^2)/(\lambda^2-2\lambda Cos[2\pi\omega]+1)-1$",
    "such as {{1, 1}, {0}} each element",
    "position `{x, y}` in the pattern shown",
    r"computation of $3^{20}$ (a)",
    "■ **Page 627 · Structure of *Mathematica*.**",
    "$x + y z$ comes to be interpreted in *Mathematica* as "
    "`Plus[x, Times[y, z]]`",
    "avoid this effect.",
    "found for sufficiently large n from",
    "rather than t applications of h.",
    "■ **Page 621 · Pointer encoding.** The pointer encoding compression method",
    "many kinds of data.",
    "Most standard continuous mathematical functions never show any kind of nested behavior.",
    "and can so cannot",
    "appear to be associated changes",
    "`Flatten[Table[{1, Table[0, {n - 1}]}, {n}]]`",
    "`h[a_, b_] := FromDigits[g[ListConvolve[IntegerDigits[a, k], IntegerDigits[b, k], {1, -1}, 0]], k]`",
    "{{}, {{1}}}, n - 3]]]",
    "Complement[Flatten[Table[Outer[1 - Times[##] &",
    "($\\{r^2, rs, s^2, -rs\\}$  works for any r and s",
    "$m = \\{\\{0, -1, 1\\}, \\{1, 0, -1\\}, \\{-1, 1, 0\\}\\}$).",
    "probabilities 1/2, 1/4, 1/8, … will yield codewords of lengths 1, 2, 3, …",
    "within the bin—after trailing zeros",
    r"*(Period-doubling sequence)* The spectrum is  $(2^{\#}-",
    "the ordinary squares 1, 4, 9, 16, … show up",
    "in the pattern shown is given by  `Extract",
    "`u = h[r, r]; h[h[u, u], s]`—which requires only 3 applications",
    "functions which require 0, 1, 2, … terms",
    "BDDs of sizes 1, 2, … is",
    "$m = \\{\\{1, -1\\}, \\{-1, 1\\}\\}$.)",
]


FORBIDDEN_LITERAL_PINS = [
    "- (a) Unary. `Table[0, {n}]`.",
    "- (d) *Binary-coded base 3*.",
    "- (e) *Fibonacci encoding*.",
    "- (d) (Period-doubling sequence)",
    r"\phi[i][t-1, \omega]",
    r"\cos[2\pi\omega]",
    "such as\n\n{{1, 1}, {0}} each",
    "position in the pattern shown",
    "computation of 320 (a)",
    "■ **Page 627 · Structure of Mathematica.**",
    "x + yz comes to be interpreted in Mathematica",
    "$(\\{r^2, rs, s^2, -rs\\})$",
    "$m = \\{\\{0, -1, 1\\}, \\{1, 0, -1\\}, \\{-1, 1, 0\\}\\}\\)$ .",
    "■ **Nested continuous functions.** Elliptic theta",
    "The pointer compression method",
    "patternsexpressions",
    "featuresbeyond",
    "probabilities 1/2, 1/4, 1/8, ... will yield codewords of lengths 1, 2, 3, ...",
    "within the bin after trailing zeros",
    r"*(Period-doubling sequence)* The spectrum  $(2^{\#}-",
    "the ordinary squares 1, 4, 9, 16, ... show up",
    "in the pattern shown is given  `Extract",
    "`u = h[r, r]; h[h[u, u], s]` which requires only 3 applications",
    "functions which require 0, 1, 2, ... terms",
    "BDDs of sizes 1, 2, ... is",
    "$m = \\{\\{1, -1\\}, \\{-1, 1\\}\\}\\}$ .)",
    "N10-SRC-",
    "N10-TFP-",
    "G5-N10-VIS-",
    "FIRST_PASS",
    "<<<<<<<",
    ">>>>>>>",
]


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def rows_sha256(rows: list[dict[str, Any]]) -> str:
    return hashlib.sha256(
        b"".join(canonical_bytes(row) + b"\n" for row in rows)
    ).hexdigest()


def row_hash_sequence_sha256(rows: list[dict[str, Any]]) -> str:
    payload = "".join(
        hashlib.sha256(canonical_bytes(row)).hexdigest() + "\n" for row in rows
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def tree_manifest(root: Path) -> list[tuple[str, str]]:
    return [
        (path.relative_to(root).as_posix(), build.sha256(path.read_bytes()))
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    ]


def plain_pair_problems(text: str) -> list[tuple[int, int, int]]:
    text = re.sub(r"```[^\n]*\n.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]*`", "", text)
    text = re.sub(r"\$\$.*?\$\$", "", text, flags=re.DOTALL)
    text = re.sub(
        r"(?<!\$)\$(?!\$)(?:\\.|[^$\n])*?\$(?!\$)", "", text
    )
    problems: list[tuple[int, int, int]] = []
    line = 1
    for paragraph in text.split("\n\n"):
        depth = 0
        minimum = 0
        for character in paragraph:
            if character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                minimum = min(minimum, depth)
        if depth or minimum:
            problems.append((line, depth, minimum))
        line += paragraph.count("\n") + 2
    return problems


class NotesForChapter10Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.document = next(row for row in cls.documents if row["id"] == "N10")
        cls.n09 = next(row for row in cls.documents if row["id"] == "N09")
        cls.n11 = next(row for row in cls.documents if row["id"] == "N11")
        cls.path = build.safe_relative_path(cls.document["output_path"], suffix=".md")
        cls.rendered_bytes = build.document_bytes(
            cls.raw, cls.documents, cls.corrections
        )[cls.path]
        cls.rendered = cls.rendered_bytes.decode("utf-8")
        cls.output_path = build.OUTPUT_ROOT / Path(cls.path)
        cls.rows = [row for row in cls.corrections if row["document_id"] == "N10"]
        cls.image_rows = [row for row in cls.images if row["document_id"] == "N10"]
        cls.added = [row for row in cls.added_assets if row["document_id"] == "N10"]
        cls.references = re.findall(r"!\[[^]]*\]\(([^)\n]+)\)", cls.rendered)
        cls.segment = cls.raw[
            cls.document["raw_start_byte"] : cls.document["raw_end_byte_exclusive"]
        ]

    def test_exact_source_range_correction_registry_and_boundaries(self) -> None:
        self.assertEqual(
            (
                self.document["raw_start_line"], self.document["raw_end_line"],
                self.document["raw_start_byte"], self.document["raw_end_byte_exclusive"],
                self.document["raw_line_count"], self.document["raw_byte_count"],
                self.document["raw_segment_sha256"],
                self.document["authoritative_pdf_start_page"],
                self.document["authoritative_pdf_end_page"],
                self.document["authoritative_printed_start"],
                self.document["authoritative_printed_end"],
            ),
            (17_087, 18_194, 2_603_694, 2_810_072, 1_108, 206_378,
             "e274a9a35a8864dffd9abc46adf59e8284ad8daf5d162341d95614cba42ebb3d",
             1083, 1122, "1067", "1106"),
        )
        self.assertEqual(build.sha256(self.segment[:256]), EXPECTED_RAW_FIRST_256_SHA256)
        self.assertEqual(build.sha256(self.segment[-256:]), EXPECTED_RAW_LAST_256_SHA256)
        self.assertEqual(self.n09["raw_end_byte_exclusive"], 2_603_694)
        self.assertEqual(self.n09["raw_end_line"] + 1, 17_087)
        self.assertEqual(self.n11["raw_start_byte"], 2_810_072)
        self.assertEqual(self.n11["raw_start_line"], 18_195)

        self.assertEqual(len(self.rows), FINAL_CORRECTION_COUNT)
        self.assertEqual(
            [row["id"] for row in self.rows],
            [f"G5-C-{number:04d}"
             for number in range(2806, FINAL_CORRECTION_LAST_NUMBER + 1)],
        )
        self.assertEqual(rows_sha256(self.rows), FINAL_CORRECTION_ROWS_SHA256)
        self.assertEqual(
            row_hash_sequence_sha256(self.rows), FINAL_CORRECTION_SEQUENCE_SHA256
        )
        previous_end = self.document["raw_start_byte"]
        for row in sorted(
            self.rows, key=lambda value: (value["raw_start_byte"], value["id"])
        ):
            with self.subTest(correction=row["id"]):
                self.assertEqual(set(row), build.CORRECTION_FIELDS | {"raw_line"})
                start = row["raw_start_byte"]
                before = row["before"].encode("utf-8")
                end = start + len(before)
                local = start - self.document["raw_start_byte"]
                self.assertGreaterEqual(start, previous_end)
                self.assertEqual(self.raw[start:end], before)
                self.assertEqual(self.segment.count(before), row["expected_count"])
                self.assertEqual(
                    row["raw_line"],
                    self.document["raw_start_line"] + self.segment[:local].count(b"\n"),
                )
                pages = [
                    int(page)
                    for page in re.findall(r"pdf:(\d{4})", row["authoritative_location"])
                ]
                printed = [
                    int(page)
                    for page in re.findall(
                        r"printed(?::|\s)+(\d{3,4})", row["authoritative_location"]
                    )
                ]
                self.assertTrue(pages)
                self.assertTrue(all(1083 <= page <= 1122 for page in pages))
                self.assertTrue(printed)
                self.assertEqual(printed[0], pages[0] - 16)
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                previous_end = end

    def test_exact_final_render_and_markdown_structure(self) -> None:
        self.assertEqual(len(self.rendered_bytes), FINAL_TARGET_BYTES)
        self.assertEqual(self.rendered_bytes.count(b"\n"), FINAL_TARGET_LFS)
        self.assertEqual(build.sha256(self.rendered_bytes), FINAL_TARGET_SHA256)
        self.assertTrue(self.rendered_bytes.endswith(b"\n\n"))
        self.assertFalse(self.rendered_bytes.endswith(b"\n\n\n"))
        self.assertEqual(self.output_path.read_bytes(), self.rendered_bytes)
        self.assertEqual(
            validate.independent_document_bytes(
                self.raw, self.documents, self.corrections
            )[self.path],
            self.rendered_bytes,
        )

        lines = self.rendered.splitlines()
        headings = [line for line in lines if line.startswith("#")]
        labels = [line for line in lines if line.startswith("■ **")]
        fence_lines = re.findall(r"(?m)^ {0,3}```[^\n]*$", self.rendered)
        without_fences = re.sub(
            r"```[^\n]*\n.*?```", "", self.rendered, flags=re.DOTALL
        )
        inline_code = re.findall(r"(?<!`)`([^`]+)`(?!`)", without_fences)
        math_spans = re.findall(
            r"(?<!\$)\$(?!\$)(?:\\.|[^$\n])+?(?<!\$)\$(?!\$)", self.rendered
        )
        display_math = re.findall(r"(?m)^ {0,3}\$\$\s*$", self.rendered)
        self.assertEqual(headings, EXPECTED_HEADINGS)
        self.assertEqual(
            (len(headings), len(labels), len(fence_lines), len(inline_code),
             len(math_spans), len(display_math), len(self.references)),
            (12, 160, 98, 93, 209, 10, 57),
        )
        self.assertTrue(all(line == "```" for line in fence_lines))
        self.assertEqual(self.references, EXPECTED_REFERENCES)
        self.assertEqual(len(set(self.references)), 57)
        self.assertEqual(
            [
                (number, span)
                for number, span in enumerate(math_spans, 1)
                if span.count("{") != span.count("}")
            ],
            [],
        )
        self.assertEqual(
            (
                self.rendered.count("—"),
                self.rendered.count("…"),
                self.rendered.count("..."),
            ),
            (105, 5, 7),
        )
        self.assertEqual(
            [number for number, line in enumerate(lines, 1) if line.endswith((" ", "\t"))],
            [],
        )
        self.assertEqual(
            [ord(character) for character in self.rendered
             if ord(character) < 32 and character not in "\n\t"],
            [],
        )
        self.assertEqual(plain_pair_problems(self.rendered), [])
        self.assertNotIn("\\)$", self.rendered)

    def test_high_risk_source_and_technical_literals(self) -> None:
        for literal in REQUIRED_LITERAL_PINS:
            with self.subTest(required=literal[:60]):
                self.assertIn(literal, self.rendered)
        for literal in FORBIDDEN_LITERAL_PINS:
            with self.subTest(forbidden=literal[:60]):
                self.assertNotIn(literal, self.rendered)
        self.assertEqual(self.rendered.count("*Mathematica*"), 23)
        manifest = "\n".join(
            canonical_bytes(row).decode("utf-8")
            for row in self.rows + self.image_rows + self.added
        )
        for literal in ("N10-SRC-", "N10-TFP-", "G5-N10-VIS-", "FIRST_PASS"):
            self.assertNotIn(literal, manifest)

    def test_image_map_dispositions_and_reference_accounting(self) -> None:
        self.assertEqual(len(self.image_rows), 91)
        self.assertEqual(
            [row["ordinal"] for row in self.image_rows], list(range(1302, 1393))
        )
        self.assertEqual(rows_sha256(self.image_rows), FINAL_IMAGE_ROWS_SHA256)
        counts = Counter(
            "omitted" if "reference_disposition" in row
            else "repaired" if "repaired_asset_relative_path" in row
            else "retained"
            for row in self.image_rows
        )
        self.assertEqual(
            counts, Counter({"omitted": 57, "retained": 33, "repaired": 1})
        )
        retained = [
            Path(row["asset_relative_path"]).name for row in self.image_rows
            if "reference_disposition" not in row
        ]
        self.assertEqual(retained, EXPECTED_RETAINED_REFERENCES)
        added_names = {Path(row["asset_relative_path"]).name for row in self.added}
        self.assertEqual(
            [name for name in self.references if name not in added_names], retained
        )

        grouped: defaultdict[str, list[int]] = defaultdict(list)
        base_fields = {
            "asset_relative_path", "asset_sha256", "document_id",
            "monolith_line", "ordinal", "split_status",
        }
        disposition_fields = {
            "reference_disposition", "reference_authoritative_location",
            "reference_reason", "reference_reviewer_type",
            "reference_verification_status",
        }
        for row in self.image_rows:
            basename = Path(row["asset_relative_path"]).name
            legacy = build.LEGACY_ROOT / Path(row["asset_relative_path"])
            output = build.OUTPUT_ROOT / Path(self.path).parent / basename
            self.assertEqual(build.sha256(legacy.read_bytes()), row["asset_sha256"])
            if "reference_disposition" in row:
                self.assertEqual(set(row), base_fields | disposition_fields)
                self.assertEqual(
                    row["reference_disposition"], build.REDUNDANT_REFERENCE_DISPOSITION
                )
                self.assertEqual(row["reference_reviewer_type"], "agent")
                self.assertEqual(
                    row["reference_verification_status"], "SOURCE_VERIFIED"
                )
                matches = re.findall(r"G5-A-\d{4}", row["reference_reason"])
                self.assertEqual(len(matches), 1)
                grouped[matches[0]].append(row["ordinal"])
                self.assertNotIn(basename, self.references)
                self.assertEqual(output.read_bytes(), legacy.read_bytes())
            elif "repaired_asset_relative_path" in row:
                self.assertEqual(set(row), base_fields | build.REPAIRED_IMAGE_FIELDS)
                name, digest, dimensions, position = EXPECTED_REPAIRS[row["ordinal"]]
                repaired = REPO_ROOT / row["repaired_asset_relative_path"]
                payload = repaired.read_bytes()
                self.assertEqual(name, basename)
                self.assertEqual(row["repaired_asset_sha256"], digest)
                self.assertEqual(build.sha256(payload), digest)
                self.assertEqual(build.jpeg_dimensions(payload), dimensions)
                self.assertEqual(
                    (row["repaired_width_px"], row["repaired_height_px"]),
                    dimensions,
                )
                self.assertEqual(output.read_bytes(), payload)
                self.assertEqual(self.references[position - 1], name)
            else:
                self.assertEqual(set(row), base_fields)
                self.assertIn(basename, self.references)
                self.assertEqual(output.read_bytes(), legacy.read_bytes())
        self.assertEqual(len(grouped), 18)
        self.assertEqual(sum(map(len, grouped.values())), 57)
        self.assertEqual(set(grouped), {
            row["id"] for row in self.added if row["id"] not in WHOLLY_MISSING_ADDITIONS
        })

    def test_added_assets_and_visual_guards_are_exact(self) -> None:
        self.assertEqual(
            [row["id"] for row in self.added],
            [f"G5-A-{number:04d}" for number in range(119, 142)],
        )
        self.assertEqual(rows_sha256(self.added), FINAL_ADDITION_ROWS_SHA256)
        self.assertEqual(
            [Path(row["asset_relative_path"]).name for row in self.added],
            EXPECTED_ADDED_REFERENCES,
        )
        self.assertEqual(
            {path.name for path in (GOAL_DIR / "assets/N10").glob("*.jpeg")},
            set(EXPECTED_ADDED_REFERENCES)
            | {value[0] for value in EXPECTED_REPAIRS.values()},
        )

        visual_guards: dict[str, dict[str, Any]] = {}
        for row in self.rows:
            matches = re.findall(r"G5-A-01(?:[12]\d|3\d|4[01])", row["reason"])
            if matches:
                self.assertEqual(len(matches), 1)
                visual_guards[matches[0]] = row
        self.assertEqual(set(visual_guards), {row["id"] for row in self.added})

        for row in self.added:
            basename = Path(row["asset_relative_path"]).name
            payload = (REPO_ROOT / row["asset_relative_path"]).read_bytes()
            output = build.OUTPUT_ROOT / Path(self.path).parent / basename
            page = int(re.search(r"pdf:(\d{4})", row["authoritative_location"]).group(1))
            filename_page = int(re.search(r"_page_(\d+)_", basename).group(1))
            with self.subTest(addition=row["id"]):
                self.assertEqual(set(row), build.ADDED_ASSET_FIELDS)
                self.assertEqual(build.sha256(payload), row["asset_sha256"])
                self.assertEqual(
                    build.jpeg_dimensions(payload), (row["width_px"], row["height_px"])
                )
                self.assertEqual(filename_page + 1, page)
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                self.assertEqual(output.read_bytes(), payload)
                self.assertEqual(self.references.count(basename), 1)
                guard = visual_guards[row["id"]]
                self.assertIn(f"![]({basename})", guard["after"])
        replacement_ids = {row["id"] for row in self.added} - WHOLLY_MISSING_ADDITIONS
        self.assertEqual(len(replacement_ids), 18)
        self.assertEqual(len(WHOLLY_MISSING_ADDITIONS), 5)

    def test_authoritative_source_legacy_and_completed_coverage(self) -> None:
        range_data = json.loads(build.RANGES_PATH.read_text(encoding="utf-8"))
        source = range_data["authoritative_source"]
        self.assertEqual(
            (source["sha256"], source["size_bytes"], source["pdf_page_count"]),
            (EXPECTED_PDF_SHA256, 57_779_240, 1280),
        )
        pdf = validate.validate_authoritative_source(range_data)
        self.assertEqual(build.sha256(pdf.read_bytes()), EXPECTED_PDF_SHA256)
        self.assertEqual(validate.legacy_tree_digest(), EXPECTED_LEGACY_TREE)
        coverage = validate.validate_coverage(self.documents)
        n10 = next(row for row in coverage if row["document_id"] == "N10")
        self.assertEqual(
            (n10["first_pass"], n10["second_pass"], n10["reviewer_type"]),
            ("YES", "YES", "agent"),
        )
        self.assertEqual(sum(row["second_pass"] == "YES" for row in coverage), 26)

    def test_normal_and_zero_builds_remain_deterministic(self) -> None:
        with tempfile.TemporaryDirectory(prefix="n10-build-") as directory:
            first = Path(directory) / "first"
            second = Path(directory) / "second"
            self.assertEqual(build.build(first), (29, 1607, 4370))
            self.assertEqual(build.build(second), (29, 1607, 4370))
            first_manifest = tree_manifest(first)
            self.assertEqual(first_manifest, tree_manifest(second))
            self.assertEqual(first_manifest, tree_manifest(build.OUTPUT_ROOT))
            self.assertEqual(len(first_manifest), 1638)
            self.assertEqual(validate.validate(first), (29, 1607, 4370, 26))

            zero = Path(directory) / "zero"
            self.assertEqual(build.build(zero, zero_corrections=True), (29, 1444, 0))
            self.assertEqual(len(tree_manifest(zero)), 1475)
            concatenated = b"".join(
                (zero / document["output_path"]).read_bytes()
                for document in self.documents
            )
            self.assertEqual(concatenated, self.raw)
            validate.validate_output(
                zero, self.raw, self.documents, [], self.images,
                zero_corrections=True,
            )


if __name__ == "__main__":
    unittest.main()
