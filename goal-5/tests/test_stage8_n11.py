#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import unittest
from collections import Counter
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


FINAL_CORRECTION_COUNT = 213
FINAL_CORRECTION_FIRST_NUMBER = 3361
FINAL_CORRECTION_LAST_NUMBER = 3573
FINAL_TARGET_BYTES = 87_968
FINAL_TARGET_LFS = 982
FINAL_TARGET_SHA256 = (
    "e6f30ab06b5282a0cf17b9d68603bf08d435de6bb899946365c8ed8362c80b25"
)
FINAL_CORRECTION_ROWS_SHA256 = (
    "f1a9bb22e079f058237da06e55e9d2a463a0a34b0edf8d8cc5df3a3c838dca97"
)
FINAL_CORRECTION_SEQUENCE_SHA256 = (
    "9111603c7939e72030b08c380744edd697d38fa2c7ec5c636544c176c1738c2e"
)
FINAL_IMAGE_ROWS_SHA256 = (
    "2ed7d00b10059d2ded715e2f86d049de4d1a5f1e47e204c62b37024592473a71"
)
FINAL_IMAGE_SEQUENCE_SHA256 = (
    "6dced7393995a9a481297b0a32f040db2c1277078ed7b705e7695ed5f1adf764"
)
FINAL_ADDITION_ROWS_SHA256 = (
    "baa98024dd6e2bd0c047ba81c35bb043fcdec02bb4f56121dbfac867d8fadd63"
)
FINAL_ADDITION_SEQUENCE_SHA256 = (
    "f16c807408f0b7510150303437e54a754ece23ce1683ee7a32102ea868f1033c"
)
EXPECTED_RAW_FIRST_256_SHA256 = (
    "5e154111c9dc35ef1bf58245b438febf55384e4aba2341fdb40e7f5ec493d99d"
)
EXPECTED_RAW_LAST_256_SHA256 = (
    "98d9e87b54917362334b7d2ce1b91e7eba8f7660f4fcc7eb19055d424a45c3e1"
)
EXPECTED_PDF_SHA256 = (
    "a3cc5dd60e12d6b563aee86ea31a15b03f9cddfd4869b8f965d3a11bbc61a0d6"
)


EXPECTED_HEADINGS = [
    "## The Notion of Computation",
    "### Computation as a Framework",
    "### Computations in Cellular Automata",
    "### The Phenomenon of Universality",
    "### A Universal Cellular Automaton",
    "### Emulating Other Systems with Cellular Automata",
    "### Emulating Cellular Automata with Other Systems",
    "### The Rule 110 Cellular Automaton",
    "### Class 4 Behavior and Universality",
    "### The Threshold of Universality in Cellular Automata",
    "### Universality in Turing Machines and Other Systems",
]


EXPECTED_REFERENCES = [
    "_page_1124_Picture_6.jpeg",
    "_page_1124_Picture_7.jpeg",
    "_page_1124_Picture_16.jpeg",
    "_page_1124_Picture_17.jpeg",
    "_page_1126_Universal_CA_Color_Icon_Legend.jpeg",
    "_page_1130_Figure_11.jpeg",
    "_page_1131_Figure_8.jpeg",
    "_page_1132_Picture_2.jpeg",
    "_page_1132_Picture_6.jpeg",
    "_page_1132_Figure_9.jpeg",
    "_page_1133_Rule_73_Initial_Condition.jpeg",
    "_page_1133_Rule_30_Initial_Condition.jpeg",
    "_page_1133_Rule_41_Left_Background.jpeg",
    "_page_1133_Rule_41_Single_Cell.jpeg",
    "_page_1133_Rule_41_Right_Background.jpeg",
    "_page_1133_Picture_6.jpeg",
    "_page_1133_Picture_8.jpeg",
    "_page_1134_Rogozhin_24_State_2_Color_Turing_Machine_Rule.jpeg",
    "_page_1135_Figure_14.jpeg",
    "_page_1135_Figure_16.jpeg",
    "_page_1136_Picture_5.jpeg",
]


EXPECTED_RETAINED_REFERENCES = [
    "_page_1124_Picture_6.jpeg",
    "_page_1124_Picture_7.jpeg",
    "_page_1124_Picture_16.jpeg",
    "_page_1124_Picture_17.jpeg",
    "_page_1130_Figure_11.jpeg",
    "_page_1131_Figure_8.jpeg",
    "_page_1132_Picture_2.jpeg",
    "_page_1132_Picture_6.jpeg",
    "_page_1132_Figure_9.jpeg",
    "_page_1133_Picture_6.jpeg",
    "_page_1133_Picture_8.jpeg",
    "_page_1135_Figure_14.jpeg",
    "_page_1135_Figure_16.jpeg",
    "_page_1136_Picture_5.jpeg",
]


EXPECTED_ADDED_ASSETS = {
    "G5-A-0142": (
        "_page_1126_Universal_CA_Color_Icon_Legend.jpeg",
        "ff1b09b93cf6702ab015722f9f9cbc28cd96b0abb7288453a336f9bc525c53a5",
        (852, 68),
    ),
    "G5-A-0143": (
        "_page_1133_Rule_73_Initial_Condition.jpeg",
        "960ef63de3154db48f81a6820e25511a1e41687cc41b17025e4501ddcffb22d3",
        (71, 20),
    ),
    "G5-A-0144": (
        "_page_1133_Rule_30_Initial_Condition.jpeg",
        "e35c8aaae3339432ddbc90e96a3654b901359ed4d267179199cef744e92759bd",
        (186, 20),
    ),
    "G5-A-0145": (
        "_page_1133_Rule_41_Left_Background.jpeg",
        "34aa09c4cb59f57566203983974241a05c4cc745c419870742bb76a8d28241b2",
        (212, 20),
    ),
    "G5-A-0146": (
        "_page_1133_Rule_41_Single_Cell.jpeg",
        "3360233ab37e5f0e0ae5926d2419f38307ba35c95781ac071c1db7bf5940baed",
        (16, 20),
    ),
    "G5-A-0147": (
        "_page_1133_Rule_41_Right_Background.jpeg",
        "57760f40bd6bac938557d852569f03bbcdc92286225f397c09539a6c59873fd8",
        (109, 20),
    ),
    "G5-A-0148": (
        "_page_1134_Rogozhin_24_State_2_Color_Turing_Machine_Rule.jpeg",
        "c6c0b1418dddb6093c0d21d0f527ede3344815bb5991362c7745fb1a05d3b022",
        (850, 47),
    ),
}


NEWLY_FENCED_DISPLAYS = {
    "G5-C-3527": """```
NestList[Join[{0}, Mod[1 + Rest[FoldList[Plus, 0, #]], 2],
  {{0}, {1, 1, 0}}[[Mod[Apply[Plus, #], 2] + 1]]] &, init, t]
```""",
    "G5-C-3536": """```
Mod[x, Prime[Rest[NestList[NestWhile[# + 1 &, # + 1,
  Mod[x, Prime[#]] == 0 &] &, 0, n]]]]
```""",
    "G5-C-3538": """```
{d[4, 40], i[5], d[3, 9], i[3], d[7, 4], d[5, 14], i[6],
 d[3, 3], i[7], d[6, 2], i[6], d[5, 11], d[6, 3], d[4, 35],
 d[6, 15], i[4], d[8, 16], d[5, 21], i[1], d[3, 1], d[5, 25],
 i[2], d[3, 1], i[6], d[5, 32], d[1, 28], d[3, 1], d[4, 28],
 i[4], d[6, 29], d[3, 1], d[5, 24], d[2, 28], d[3, 1],
 i[8], i[6], d[5, 36], i[6], d[3, 3], d[6, 40], d[4, 3]}
```""",
    "G5-C-3542": """```
2^FromDigits[Reverse[Take[list, n - 1]]]
  3^FromDigits[Take[list, {n + 1, -1}]] 5^list[[n]] 7^s
```""",
}


REQUIRED_LITERAL_PINS = [
    "Flatten[{Transpose[{Join[{4, 18 (1 - a), 6}, Table[9,\n"
    "  {2^(2 r + 1) - 3}]], 10 - 3 rtab}], Table[{9, 1}, {r}], 9, 13}]",
    "Select[rules, Mod[Length[#], 6] != 0 &] == {}, init_] :=",
    "MapThread[If[#1 === #2 === {d[22, 11], s[3]}, {d[",
    r"$f_j[a_j] == InverseFunction[\phi][f_i[\phi[a_j]]]$",
    "yields a number x such that Mod[x, p] == list. Based on this",
    "TSToPR[{n_, rule_}] := Fold[Apply[c, Flatten[{#1, Array[p, #2],",
    "IntegerDigits[216 (# + 432 10^49), 2] &",
    r"$n + Table[Prime[i]^reg[[i]], \{i, nr\}]p - 1$",
    "the rule he gave in this case is:\n\n"
    "![](_page_1134_Rogozhin_24_State_2_Color_Turing_Machine_Rule.jpeg)",
    "*s[s[s][k]][k[k[s[s]]]]* serves as a doubling function.",
]


FORBIDDEN_LITERAL_PINS = [
    r"$f_i[a_i] = InverseFunction[\phi][f_i[\phi[a_i]]]$",
    "Mod[x, p] = list.",
    "Table[{9, 1}, {r}], {9, 13}",
    "Select[rules, Mod[Length[#], 6] + 0 &]",
    "10<sup>49</sup>",
    "N11-SRC-",
    "N11-TFP-",
    "G5-N11-VIS-",
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


class NotesForChapter11Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.document = next(row for row in cls.documents if row["id"] == "N11")
        cls.n10 = next(row for row in cls.documents if row["id"] == "N10")
        cls.n12 = next(row for row in cls.documents if row["id"] == "N12")
        cls.path = build.safe_relative_path(cls.document["output_path"], suffix=".md")
        cls.rendered_bytes = build.document_bytes(
            cls.raw, cls.documents, cls.corrections
        )[cls.path]
        cls.rendered = cls.rendered_bytes.decode("utf-8")
        cls.output_path = build.OUTPUT_ROOT / Path(cls.path)
        cls.rows = [row for row in cls.corrections if row["document_id"] == "N11"]
        cls.rows_by_id = {row["id"]: row for row in cls.rows}
        cls.image_rows = [row for row in cls.images if row["document_id"] == "N11"]
        cls.added = [
            row for row in cls.added_assets if row["document_id"] == "N11"
        ]
        cls.references = re.findall(r"!\[[^]]*\]\(([^)\n]+)\)", cls.rendered)
        cls.segment = cls.raw[
            cls.document["raw_start_byte"] : cls.document["raw_end_byte_exclusive"]
        ]

    def test_exact_source_range_correction_registry_and_boundaries(self) -> None:
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
                18_195,
                19_027,
                2_810_072,
                2_926_907,
                833,
                116_835,
                "fadca1514dc3621dec6c0587ec8bb33fe2b18c32846b16bb22ea80872f8fec9b",
                1123,
                1140,
                "1107",
                "1124",
            ),
        )
        self.assertEqual(build.sha256(self.segment[:256]), EXPECTED_RAW_FIRST_256_SHA256)
        self.assertEqual(build.sha256(self.segment[-256:]), EXPECTED_RAW_LAST_256_SHA256)
        self.assertEqual(self.n10["raw_end_byte_exclusive"], 2_810_072)
        self.assertEqual(self.n10["raw_end_line"] + 1, 18_195)
        self.assertEqual(self.n12["raw_start_byte"], 2_926_907)
        self.assertEqual(self.n12["raw_start_line"], 19_028)

        self.assertEqual(len(self.rows), FINAL_CORRECTION_COUNT)
        self.assertEqual(
            [row["id"] for row in self.rows],
            [
                f"G5-C-{number:04d}"
                for number in range(
                    FINAL_CORRECTION_FIRST_NUMBER, FINAL_CORRECTION_LAST_NUMBER + 1
                )
            ],
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
                self.assertTrue(all(1123 <= page <= 1140 for page in pages))
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
            (
                len(headings),
                len(labels),
                len(fence_lines),
                len(inline_code),
                len(math_spans),
                len(display_math),
                len(self.references),
            ),
            (11, 70, 132, 3, 61, 0, 21),
        )
        self.assertTrue(all(line == "```" for line in fence_lines))
        self.assertEqual(self.references, EXPECTED_REFERENCES)
        self.assertEqual(len(set(self.references)), 21)
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
            (38, 0, 3),
        )
        self.assertEqual(
            [
                ord(character)
                for character in self.rendered
                if ord(character) < 32 and character not in "\n\t"
            ],
            [],
        )
        self.assertNotIn("\\)$", self.rendered)
        self.assertNotIn("<<<<<<<", self.rendered)
        self.assertNotIn(">>>>>>>", self.rendered)

    def test_high_risk_source_and_technical_literals(self) -> None:
        for literal in REQUIRED_LITERAL_PINS:
            with self.subTest(required=literal[:72]):
                self.assertIn(literal, self.rendered)
        for literal in FORBIDDEN_LITERAL_PINS:
            with self.subTest(forbidden=literal[:72]):
                self.assertNotIn(literal, self.rendered)

        equality_rewrites = {
            "G5-C-3494": (
                r"$f_i[a_i] = InverseFunction[\phi][f_i[\phi[a_i]]]$",
                r"$f_j[a_j] == InverseFunction[\phi][f_i[\phi[a_j]]]$",
            ),
            "G5-C-3535": (
                "Mod[x, p] = list.",
                "Mod[x, p] == list.",
            ),
        }
        for correction_id, (before, after) in equality_rewrites.items():
            row = self.rows_by_id[correction_id]
            with self.subTest(equality_fix=correction_id):
                self.assertIn(before, row["before"])
                self.assertIn(after, row["after"])
                self.assertNotIn(before, row["after"])
                self.assertEqual(self.rendered.count(after), 1)

        for correction_id, display in NEWLY_FENCED_DISPLAYS.items():
            with self.subTest(fenced_display=correction_id):
                self.assertIn(display, self.rows_by_id[correction_id]["after"])
                self.assertEqual(self.rendered.count(display), 1)

        manifest = "\n".join(
            canonical_bytes(row).decode("utf-8")
            for row in self.rows + self.image_rows + self.added
        )
        for literal in ("N11-SRC-", "N11-TFP-", "G5-N11-VIS-", "FIRST_PASS"):
            self.assertNotIn(literal, manifest)

    def test_exact_image_map_reference_and_asset_accounting(self) -> None:
        self.assertEqual(len(self.image_rows), 14)
        self.assertEqual(
            [row["ordinal"] for row in self.image_rows], list(range(1393, 1407))
        )
        self.assertEqual(rows_sha256(self.image_rows), FINAL_IMAGE_ROWS_SHA256)
        self.assertEqual(
            row_hash_sequence_sha256(self.image_rows), FINAL_IMAGE_SEQUENCE_SHA256
        )
        self.assertEqual(
            Counter(
                "omitted"
                if "reference_disposition" in row
                else "repaired"
                if "repaired_asset_relative_path" in row
                else "retained"
                for row in self.image_rows
            ),
            Counter({"retained": 14}),
        )

        base_fields = {
            "asset_relative_path",
            "asset_sha256",
            "document_id",
            "monolith_line",
            "ordinal",
            "split_status",
        }
        retained: list[str] = []
        for row in self.image_rows:
            basename = Path(row["asset_relative_path"]).name
            legacy = build.LEGACY_ROOT / Path(row["asset_relative_path"])
            output = build.OUTPUT_ROOT / Path(self.path).parent / basename
            with self.subTest(retained=basename):
                self.assertEqual(set(row), base_fields)
                self.assertEqual(build.sha256(legacy.read_bytes()), row["asset_sha256"])
                self.assertEqual(output.read_bytes(), legacy.read_bytes())
                self.assertEqual(self.references.count(basename), 1)
            retained.append(basename)
        self.assertEqual(retained, EXPECTED_RETAINED_REFERENCES)

        self.assertEqual(
            [row["id"] for row in self.added],
            [f"G5-A-{number:04d}" for number in range(142, 149)],
        )
        self.assertEqual(rows_sha256(self.added), FINAL_ADDITION_ROWS_SHA256)
        self.assertEqual(
            row_hash_sequence_sha256(self.added), FINAL_ADDITION_SEQUENCE_SHA256
        )
        self.assertEqual(
            [Path(row["asset_relative_path"]).name for row in self.added],
            [EXPECTED_ADDED_ASSETS[row["id"]][0] for row in self.added],
        )
        self.assertEqual(
            {path.name for path in (GOAL_DIR / "assets/N11").glob("*.jpeg")},
            {value[0] for value in EXPECTED_ADDED_ASSETS.values()},
        )

        guards: dict[str, str] = {}
        for row in self.rows:
            for asset_id in re.findall(r"G5-A-01(?:4[2-8])", row["reason"]):
                self.assertNotIn(asset_id, guards)
                guards[asset_id] = row["id"]
        self.assertEqual(set(guards), set(EXPECTED_ADDED_ASSETS))

        for row in self.added:
            name, digest, dimensions = EXPECTED_ADDED_ASSETS[row["id"]]
            payload = (REPO_ROOT / row["asset_relative_path"]).read_bytes()
            output = build.OUTPUT_ROOT / Path(self.path).parent / name
            source_page = int(
                re.search(r"pdf:(\d{4})", row["authoritative_location"]).group(1)
            )
            filename_page = int(re.search(r"_page_(\d+)_", name).group(1))
            with self.subTest(addition=row["id"]):
                self.assertEqual(set(row), build.ADDED_ASSET_FIELDS)
                self.assertEqual(row["asset_sha256"], digest)
                self.assertEqual(build.sha256(payload), digest)
                self.assertEqual(build.jpeg_dimensions(payload), dimensions)
                self.assertEqual((row["width_px"], row["height_px"]), dimensions)
                self.assertEqual(filename_page + 1, source_page)
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                self.assertEqual(output.read_bytes(), payload)
                self.assertEqual(self.references.count(name), 1)
                self.assertIn(
                    f"![]({name})", self.rows_by_id[guards[row["id"]]]["after"]
                )

        added_names = {value[0] for value in EXPECTED_ADDED_ASSETS.values()}
        self.assertEqual(
            [name for name in self.references if name not in added_names],
            EXPECTED_RETAINED_REFERENCES,
        )
        self.assertEqual(
            [name for name in self.references if name in added_names],
            [name for name in EXPECTED_REFERENCES if name in added_names],
        )

    def test_authoritative_source_and_first_pass_coverage_state(self) -> None:
        range_data = json.loads(build.RANGES_PATH.read_text(encoding="utf-8"))
        source = range_data["authoritative_source"]
        self.assertEqual(
            (source["sha256"], source["size_bytes"], source["pdf_page_count"]),
            (EXPECTED_PDF_SHA256, 57_779_240, 1280),
        )
        pdf = validate.validate_authoritative_source(range_data)
        self.assertEqual(build.sha256(pdf.read_bytes()), EXPECTED_PDF_SHA256)
        coverage = validate.validate_coverage(self.documents)
        n11 = next(row for row in coverage if row["document_id"] == "N11")
        self.assertEqual(
            (n11["first_pass"], n11["second_pass"], n11["reviewer_type"]),
            ("NO", "NO", ""),
        )
        self.assertEqual(sum(row["second_pass"] == "YES" for row in coverage), 25)

    def test_normal_and_zero_builds_remain_deterministic(self) -> None:
        with tempfile.TemporaryDirectory(prefix="n11-build-") as directory:
            first = Path(directory) / "first"
            second = Path(directory) / "second"
            self.assertEqual(build.build(first), (29, 1592, 3573))
            self.assertEqual(build.build(second), (29, 1592, 3573))
            first_manifest = tree_manifest(first)
            self.assertEqual(first_manifest, tree_manifest(second))
            self.assertEqual(first_manifest, tree_manifest(build.OUTPUT_ROOT))
            self.assertEqual(len(first_manifest), 1623)
            self.assertEqual(validate.validate(first), (29, 1592, 3573, 25))

            zero = Path(directory) / "zero"
            self.assertEqual(build.build(zero, zero_corrections=True), (29, 1444, 0))
            self.assertEqual(len(tree_manifest(zero)), 1475)
            self.assertEqual(
                validate.validate(zero, zero_corrections=True), (29, 1444, 0, 25)
            )
            concatenated = b"".join(
                (zero / document["output_path"]).read_bytes()
                for document in self.documents
            )
            self.assertEqual(concatenated, self.raw)
            validate.validate_output(
                zero,
                self.raw,
                self.documents,
                [],
                self.images,
                zero_corrections=True,
            )


if __name__ == "__main__":
    unittest.main()
