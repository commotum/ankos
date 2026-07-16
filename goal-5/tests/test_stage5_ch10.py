from __future__ import annotations

import copy
import json
import re
import sys
import unittest
from pathlib import Path


GOAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402
import validate  # noqa: E402


class ChapterTenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.range_data = json.loads(build.RANGES_PATH.read_text(encoding="utf-8"))
        cls.document = next(row for row in cls.documents if row["id"] == "CH10")
        cls.path = build.safe_relative_path(cls.document["output_path"], suffix=".md")
        cls.raw_text = cls.raw[
            cls.document["raw_start_byte"] : cls.document["raw_end_byte_exclusive"]
        ].decode("utf-8")
        cls.rendered_bytes = build.document_bytes(
            cls.raw, cls.documents, cls.corrections
        )[cls.path]
        cls.rendered = cls.rendered_bytes.decode("utf-8")

    def assert_order(self, *markers: str) -> None:
        positions: list[int] = []
        for marker in markers:
            self.assertEqual(
                self.rendered.count(marker),
                1,
                f"marker must occur exactly once: {marker[:100]!r}",
            )
            positions.append(self.rendered.index(marker))
        self.assertEqual(positions, sorted(positions))

    def table_rows(self) -> list[list[str]]:
        return [
            [cell.strip() for cell in line.strip("|").split("|")]
            for line in self.rendered.splitlines()
            if line.startswith("|")
        ]

    def test_source_range_correction_packet_and_final_hash_are_exact(self) -> None:
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
                6586,
                7691,
                932355,
                1103253,
                1106,
                170898,
                "a4598197bfb9eb7bc64f54692c7cf75212768a47e89f449454ad35efdae0a041",
                563,
                652,
                "547",
                "636",
            ),
        )
        raw_segment = self.raw[
            self.document["raw_start_byte"] : self.document["raw_end_byte_exclusive"]
        ]
        self.assertEqual(build.sha256(raw_segment), self.document["raw_segment_sha256"])

        relevant = [row for row in self.corrections if row["document_id"] == "CH10"]
        self.assertEqual(len(relevant), 90)
        self.assertEqual(
            [row["id"] for row in relevant],
            [f"G5-C-{number:04d}" for number in range(577, 667)],
        )
        self.assertTrue(all(row["expected_count"] == 1 for row in relevant))
        self.assertTrue(
            all(row["verification_status"] == "SOURCE_VERIFIED" for row in relevant)
        )
        self.assertTrue(all(row["reviewer_type"] == "agent" for row in relevant))
        for row in relevant:
            match = re.match(r"pdf:(\d{4})", row["authoritative_location"])
            self.assertIsNotNone(match, row["id"])
            self.assertTrue(563 <= int(match[1]) <= 652, row["id"])
            self.assertTrue(
                self.document["raw_start_byte"]
                <= row["raw_start_byte"]
                < self.document["raw_end_byte_exclusive"]
            )

        self.assertEqual(len(self.rendered_bytes), 164487)
        self.assertEqual(len(self.rendered.splitlines()), 1014)
        self.assertEqual(
            build.sha256(self.rendered_bytes),
            "82217582690509ef97acd14ca12f0f9680e380ce6a1d8f8a0373e569114b2bc3",
        )
        self.assertEqual(
            validate.independent_document_bytes(
                self.raw, self.documents, self.corrections
            )[self.path],
            self.rendered_bytes,
        )

    def test_authoritative_source_legacy_and_ch10_guards_are_pinned(self) -> None:
        source = self.range_data["authoritative_source"]
        self.assertEqual(source["size_bytes"], 57_779_240)
        self.assertEqual(
            source["sha256"],
            "a3cc5dd60e12d6b563aee86ea31a15b03f9cddfd4869b8f965d3a11bbc61a0d6",
        )
        self.assertEqual(
            validate.validate_authoritative_source(self.range_data),
            build.REPO_ROOT / "A New Kind of Science/A New Kind of Science.pdf",
        )
        self.assertEqual(
            validate.legacy_tree_digest(),
            (
                "b9ff7b9b507790f1d519593baf2b2d2f24dd6cd49dc0fe10f0ac629278ea42f4",
                1463,
            ),
        )

        parity = next(
            row
            for row in self.corrections
            if row["document_id"] == "CH10"
            and "Binomial [y, x]/2" in row["before"]
        )
        mutations = (
            ("raw_start_byte", parity["raw_start_byte"] + 1),
            ("expected_count", 2),
            ("verification_status", "PROPOSED"),
            ("authoritative_location", "pdf:0562"),
        )
        for field, value in mutations:
            changed = copy.deepcopy(self.corrections)
            target = next(row for row in changed if row["id"] == parity["id"])
            target[field] = value
            with self.subTest(mutation=field), self.assertRaises(build.BuildError):
                build.validate_corrections(changed, self.raw, self.documents)

    def test_opener_heading_hierarchy_and_source_literals_are_exact(self) -> None:
        self.assertTrue(
            self.rendered.startswith(
                "![](_page_562_Chapter_Opener.jpeg)\n\n"
                "## Processes of Perception and Analysis\n\n"
                "### Introduction\n\n"
            )
        )
        headings = (
            "Introduction",
            "What Perception and Analysis Do",
            "Defining the Notion of Randomness",
            "Defining Complexity",
            "Data Compression",
            "Irreversible Data Compression",
            "Visual Perception",
            "Auditory Perception",
            "Statistical Analysis",
            "Cryptography and Cryptanalysis",
            "Traditional Mathematics and Mathematical Formulas",
            "Human Thinking",
            "Higher Forms of Perception and Analysis",
        )
        self.assertEqual(self.rendered.count("\n### "), len(headings))
        self.assert_order(*(f"### {heading}" for heading in headings))
        self.assertNotIn("####", self.rendered)
        self.assertNotIn("### **", self.rendered)
        self.assertNotRegex(self.rendered, r"(?m)^# 10$")

        self.assertEqual(self.rendered.count("sequences (d) and (e) are random"), 1)
        self.assertNotIn("sequences (e) and (f) are random", self.rendered)
        self.assertEqual(
            self.rendered.count(
                r"$e_i e_j$ is analogous to $e_i \wedge e_j$, "
                r"$e_i + e_j$ to $e_i \vee e_j$"
            ),
            1,
        )
        self.assertEqual(self.rendered.count("<sup>◀</sup>"), 1)
        self.assertNotIn("<sup>♠</sup>", self.rendered)
        self.assertEqual(self.rendered.count(r"basic $2 \times 2$ patterns."), 1)
        self.assertEqual(self.rendered.count("*Mathematica*"), 8)

    def test_interrupted_prose_and_figure_caption_order_are_exact(self) -> None:
        self.assert_order(
            "overwhelmingly easier to generate highly complex behavior than to "
            "recognize the origins of this behavior.",
            "![](_page_566_Figure_2.jpeg)",
            "Patterns produced by taking a single black cell",
        )
        self.assert_order(
            "![](_page_587_Figure_6.jpeg)",
            "![](_page_587_Figure_7.jpeg)",
            "The effect of including progressively smaller features in the "
            "representation of images by nested squares.",
            "![](_page_588_Figure_1.jpeg)",
        )
        self.assert_order(
            "![](_page_614_Vigenere_Example.jpeg)",
            "A simple example of an encryption system in which the encrypting "
            "sequence is obtained by repetitively cycling",
        )
        self.assert_order(
            "![](_page_609_Block_Frequency_Panels.jpeg)",
            "![](_page_609_Picture_2.jpeg)",
            "Statistics of block frequencies for various sequences.",
        )
        self.assert_order(
            "![](_page_617_Figure_3.jpeg)",
            "![](_page_617_Figure_5.jpeg)",
            "Another consequence of additivity: the correspondence between colors",
        )
        self.assert_order(
            "![](_page_619_Figure_3.jpeg)",
            "![](_page_619_Figure_4.jpeg)",
            "Sideways evolution in rule 30.",
            "So if the encrypting sequence corresponds to a single column",
        )
        self.assert_order(
            "![](_page_622_Repetitive_Lookup.jpeg)",
            "<sup>◀</sup> An example of how the color of any square in a repetitive "
            "pattern",
            "![](_page_623_Picture_1.jpeg)",
            "![](_page_623_Coordinate_Grid.jpeg)",
            "![](_page_623_Substitution_Rules.jpeg)",
            "![](_page_623_Picture_3.jpeg)",
            "An example of how the color of any square in a nested pattern",
        )
        self.assert_order(
            "![](_page_629_Figure_1.jpeg)",
            "![](_page_629_Multiplication_Rules.jpeg)",
            "Cellular automaton rules equivalent to multiplication of digit sequences",
        )
        self.assert_order(
            "![](_page_631_Picture_4.jpeg)",
            "![](_page_631_Picture_5.jpeg)",
            "![](_page_631_Picture_7.jpeg)",
            "Boolean expression representations of the rules for three elementary "
            "cellular automata.",
        )
        two_step_caption = (
            "Boolean expression representations of the results from two steps in "
            "the evolution of three elementary cellular automata. At the top in "
            "each case is shown the explicit array of outcomes for each of the 32 "
            "possible initial configurations of cells. In the middle are shown "
            "those configurations that yield black cells. And at the bottom are "
            "the minimal representations of these collections of possibilities."
        )
        self.assert_order(
            "the individual terms end up not depending on most of these variables.",
            "![](_page_632_Two_Step_Boolean_Top.jpeg)",
            "![](_page_632_Two_Step_Boolean_Rule_30.jpeg)",
            two_step_caption,
            "So what happens if one considers more steps?",
        )

    def test_high_risk_technical_text_formulas_and_tables_are_exact(self) -> None:
        expected_counts = {
            "picture (c) in fact allows a very short description.": 1,
            r"$2^6 = 64$ possible $3 \times 2$ blocks": 1,
            r"numerical values $-1$ and $+1$": 1,
            r"$GCD[x,y] = 1$": 2,
            r"$Mod[Quotient[m^t,k^n],k]$": 1,
            r"$(1 - (-1)^{Binomial[y,x]})/2$": 1,
            r"$Binomial[t,n]$": 1,
            r"$GegenbauerC[n,-t,-1/2]$": 1,
            (
                r"$e_i e_j$ is analogous to $e_i \wedge e_j$, "
                r"$e_i + e_j$ to $e_i \vee e_j$"
            ): 1,
            (
                "the network and formula shown are the ones that involve the "
                "absolute minimum number of operations"
            ): 1,
        }
        for text, expected_count in expected_counts.items():
            with self.subTest(text=text):
                self.assertEqual(self.rendered.count(text), expected_count)

        substitution_rules = (
            r"(b) $\blacksquare \to \blacksquare \square$, "
            r"$\square \to \square \blacksquare$, "
            r"(c) $\blacksquare \to \blacksquare \blacksquare \square$, "
            r"$\square \to \square$ and "
            r"(d) $\blacksquare \to \blacksquare \blacksquare \blacksquare "
            r"\square \square \square$, $\square \to \blacksquare \square$"
        )
        self.assertEqual(self.rendered.count(substitution_rules), 1)

        table_rows = self.table_rows()
        self.assertIn(
            [
                "$(1+x)^5$",
                "$1 + 5x + 10x^2 + 10x^3 + 5x^4 + x^5$",
            ],
            table_rows,
        )
        self.assertIn(
            [
                "$(1+x+x^2)^5$",
                "$1 + 5x + 15x^2 + 30x^3 + 45x^4 + 51x^5 + 45x^6 + "
                "30x^7 + 15x^8 + 5x^9 + x^{10}$",
            ],
            table_rows,
        )

        expected_power_rows = [
            ["$m^1$", "$m$", "$m$"],
            ["$m^2$", r"$m \times m$", "$m^2$"],
            ["$m^3$", r"$m \times m \times m$", r"$m^2 \times m$"],
            ["$m^4$", r"$m \times m \times m \times m$", "$(m^2)^2$"],
            [
                "$m^5$",
                r"$m \times m \times m \times m \times m$",
                r"$(m^2)^2 \times m$",
            ],
            [
                "$m^6$",
                r"$m \times m \times m \times m \times m \times m$",
                "$(m^2 \\times m)^2$",
            ],
            [
                "$m^7$",
                r"$m \times m \times m \times m \times m \times m \times m$",
                r"$(m^2 \times m)^2 \times m$",
            ],
            [
                "$m^8$",
                r"$m \times m \times m \times m \times m \times m \times m "
                r"\times m$",
                "$((m^2)^2)^2$",
            ],
            [
                "$m^9$",
                r"$m \times m \times m \times m \times m \times m \times m "
                r"\times m \times m$",
                r"$((m^2)^2)^2 \times m$",
            ],
            [
                "$m^{10}$",
                r"$m \times m \times m \times m \times m \times m \times m "
                r"\times m \times m \times m$",
                "$((m^2)^2 \\times m)^2$",
            ],
        ]
        actual_power_rows = [
            row
            for row in table_rows
            if row and re.fullmatch(r"\$m\^(?:[1-9]|\{10\})\$", row[0])
        ]
        self.assertEqual(actual_power_rows, expected_power_rows)

    def test_repaired_and_added_assets_and_reference_order_are_exact(self) -> None:
        chapter_images = [row for row in self.images if row["document_id"] == "CH10"]
        self.assertEqual(len(chapter_images), 67)
        self.assertEqual([row["ordinal"] for row in chapter_images], list(range(590, 657)))

        expected_repaired = {
            610: (
                "4593068b703d9bd4e1360ca935ae3c0667159f706cee025c5505221a0c788345",
                (1200, 450),
                "pdf:0588",
                "1f04b96b819d010b0733b5b54a5472c4b2e01afc705f123ca5d995ce5f726abe",
            ),
            613: (
                "6e8922b56593d17d139120f86251c4d19755c5ded6d90c08d918fe0147562ff4",
                (987, 1280),
                "pdf:0592",
                "b7925aad250dac1de6d00d35946642fc952a2c084286fc2a6950dc92a2e08924",
            ),
            641: (
                "f4ea4b4ebf2f6372f0357e7050f16e5a956eb01e1749e658ae77c55cdce075f0",
                (1200, 411),
                "pdf:0620",
                "28e76e04fc4c770acf5127d3285495a922d784c7496f43acb596a22d6dd27ba2",
            ),
            651: (
                "a6af8c6071e287d15f7257daa089ffa9321cd09e27ae4661c7f8554c20abfe7f",
                (500, 314),
                "pdf:0632",
                "65db6af5782c94809fbb107fb95baadfb5b56f70a2436b028a1d739e8beaa12b",
            ),
            652: (
                "d24ce5cc45a9a4e5693af17dda0a19eb8e03a2fd5dcf372c8a79a94e157a9024",
                (500, 312),
                "pdf:0632",
                "88a349a5e7ef6afcf39c84337bd40cc6e00844b4758ce394c7a40a6b19ce19f7",
            ),
        }
        repaired = [
            row for row in chapter_images if "repaired_asset_relative_path" in row
        ]
        self.assertEqual([row["ordinal"] for row in repaired], list(expected_repaired))
        for row in repaired:
            expected_hash, dimensions, page, legacy_hash = expected_repaired[
                row["ordinal"]
            ]
            with self.subTest(repaired=row["ordinal"]):
                source = build.REPO_ROOT / Path(row["repaired_asset_relative_path"])
                output = build.OUTPUT_ROOT / Path(self.path).parent / source.name
                payload = source.read_bytes()
                legacy = build.LEGACY_ROOT / Path(row["asset_relative_path"])
                legacy_payload = legacy.read_bytes()
                self.assertEqual(build.sha256(payload), expected_hash)
                self.assertEqual(row["repaired_asset_sha256"], expected_hash)
                self.assertEqual(build.jpeg_dimensions(payload), dimensions)
                self.assertEqual(
                    (row["repaired_width_px"], row["repaired_height_px"]), dimensions
                )
                self.assertTrue(row["repaired_authoritative_location"].startswith(page))
                self.assertEqual(row["asset_sha256"], legacy_hash)
                self.assertEqual(build.sha256(legacy_payload), legacy_hash)
                self.assertNotEqual(payload, legacy_payload)
                self.assertEqual(output.read_bytes(), payload)

        expected_added = {
            "G5-A-0023": (
                "_page_562_Chapter_Opener.jpeg",
                "0688a1a13f5d8facb7f54e86a014952db8f40fe31f85d5bfce55b8f5608e4dea",
                (440, 560),
                "pdf:0563",
            ),
            "G5-A-0024": (
                "_page_587_Figure_7.jpeg",
                "52dc7bec727a7af83d2d5634e1bd1fc71dd588c9d2163637f06ecde220fb682b",
                (680, 340),
                "pdf:0588",
            ),
            "G5-A-0025": (
                "_page_614_Vigenere_Example.jpeg",
                "d70b0800e74e8b3e0fad54fce53882b01c503d542d4bf0421098c19779d883e5",
                (800, 690),
                "pdf:0615",
            ),
            "G5-A-0026": (
                "_page_619_Figure_4.jpeg",
                "9302fa6e81fa797ad5614dc4b3cbd16c4a3a0416240ace6ca7182a44fedc8cde",
                (820, 320),
                "pdf:0620",
            ),
            "G5-A-0027": (
                "_page_622_Repetitive_Lookup.jpeg",
                "eafe84c58f407037018b40e793df5a4e91c63a3cbb05450c9eaef8205e8e24a3",
                (175, 140),
                "pdf:0623",
            ),
            "G5-A-0028": (
                "_page_623_Coordinate_Grid.jpeg",
                "2e0cc562508e2ba3848d57594a7df8da163c8558592c8dcfc3890edfa0ec52b6",
                (1110, 1080),
                "pdf:0624",
            ),
            "G5-A-0029": (
                "_page_623_Substitution_Rules.jpeg",
                "4a73df48897bf2c1fc18b705a567efa6b2f15d444fe61a1c53891888a8445eeb",
                (370, 160),
                "pdf:0624",
            ),
            "G5-A-0030": (
                "_page_629_Multiplication_Rules.jpeg",
                "f5ae6b30c235ba7d3f50e2efe06e289ecab08ce5030c3f8d2d19a216332ba671",
                (1200, 385),
                "pdf:0630",
            ),
            "G5-A-0031": (
                "_page_632_Two_Step_Boolean_Top.jpeg",
                "61a9830e53f03b24364ff5a181489a0047f9d5e932d0ca415b5d65b105ff3f70",
                (1200, 466),
                "pdf:0633",
            ),
            "G5-A-0032": (
                "_page_632_Two_Step_Boolean_Rule_30.jpeg",
                "107b5d8c30d67b0fb1703e92ca568f65bd7dc0879da19d62c0f71cbb79deb076",
                (660, 510),
                "pdf:0633",
            ),
            "G5-A-0033": (
                "_page_609_Block_Frequency_Panels.jpeg",
                "2eae3f22577a012d78ff23500d0909dbda9f9bb1f7488794c57fa9450ccfd5f4",
                (1200, 576),
                "pdf:0610",
            ),
        }
        chapter_added = [
            row for row in self.added_assets if row["document_id"] == "CH10"
        ]
        self.assertEqual([row["id"] for row in chapter_added], list(expected_added))
        added_names: dict[str, str] = {}
        for row in chapter_added:
            expected_name, expected_hash, dimensions, page = expected_added[row["id"]]
            with self.subTest(added=row["id"]):
                source = build.REPO_ROOT / Path(row["asset_relative_path"])
                output = build.OUTPUT_ROOT / Path(self.path).parent / source.name
                payload = source.read_bytes()
                added_names[row["id"]] = source.name
                self.assertEqual(source.name, expected_name)
                self.assertEqual(build.sha256(payload), expected_hash)
                self.assertEqual(row["asset_sha256"], expected_hash)
                self.assertEqual(build.jpeg_dimensions(payload), dimensions)
                self.assertEqual((row["width_px"], row["height_px"]), dimensions)
                self.assertTrue(row["authoritative_location"].startswith(page))
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                self.assertEqual(output.read_bytes(), payload)

        mapped_names = {
            row["ordinal"]: Path(row["asset_relative_path"]).name
            for row in chapter_images
        }
        expected_references = (
            [added_names["G5-A-0023"]]
            + [mapped_names[number] for number in range(590, 611)]
            + [added_names["G5-A-0024"]]
            + [mapped_names[number] for number in range(611, 631)]
            + [added_names["G5-A-0033"]]
            + [mapped_names[number] for number in range(631, 634)]
            + [added_names["G5-A-0025"]]
            + [mapped_names[number] for number in range(634, 642)]
            + [added_names["G5-A-0026"]]
            + [mapped_names[number] for number in range(642, 644)]
            + [added_names["G5-A-0027"]]
            + [
                mapped_names[644],
                added_names["G5-A-0028"],
                added_names["G5-A-0029"],
                mapped_names[645],
            ]
            + [mapped_names[number] for number in range(646, 651)]
            + [added_names["G5-A-0030"]]
            + [mapped_names[number] for number in range(651, 654)]
            + [added_names["G5-A-0031"], added_names["G5-A-0032"]]
            + [mapped_names[number] for number in range(654, 657)]
        )
        references = re.findall(r"!\[\]\(([^)]+\.jpeg)\)", self.rendered)
        self.assertEqual(len(references), 78)
        self.assertEqual(len(set(references)), 78)
        self.assertEqual(references, expected_references)

        unchanged = {
            638: "0a909cfa5b0be0e02e51e630bf1f1e938051ffd7db6c24e01ca37ccf610a89e3",
            639: "0950f2f74e265aef2f5839b18fb54a08e3077800e3abe89c6c5fa80224fff66b",
            644: "6b32debc0a3ae9ce898ac103f882137cce41c2ad91330e6dc92a6cc21849c618",
            645: "46077b731213938dc4838ff79baf87410e6ef521e586b77f99596300f7b61a1b",
            650: "9f0c1bf2f9af5226d6d4170e5a03f31301c1119061f659fe7944f2d83abd7278",
            653: "66252aab9bcbced1f65ed65a7625858f5e6ad71d4fa1548bf648f57988ba0ea9",
        }
        for ordinal, expected_hash in unchanged.items():
            row = next(item for item in chapter_images if item["ordinal"] == ordinal)
            with self.subTest(unchanged=ordinal):
                self.assertNotIn("repaired_asset_relative_path", row)
                legacy = build.LEGACY_ROOT / Path(row["asset_relative_path"])
                output = build.OUTPUT_ROOT / Path(self.path).parent / legacy.name
                payload = legacy.read_bytes()
                self.assertEqual(row["asset_sha256"], expected_hash)
                self.assertEqual(build.sha256(payload), expected_hash)
                self.assertEqual(output.read_bytes(), payload)

        changed_images = copy.deepcopy(self.images)
        next(row for row in changed_images if row["ordinal"] == 610)[
            "repaired_asset_sha256"
        ] = "0" * 64
        with self.assertRaises(build.BuildError):
            build.validate_images(self.raw, self.documents, changed_images)

        changed_added = copy.deepcopy(self.added_assets)
        next(row for row in changed_added if row["id"] == "G5-A-0023").pop("reason")
        with self.assertRaises(build.BuildError):
            build.validate_added_assets(self.documents, self.images, changed_added)

    def test_high_risk_residual_ocr_and_layout_detectors_are_clean(self) -> None:
        raw_only = (
            "#### **Data Compression**",
            r"picture  $\langle c \rangle$",
            "pattern recognition\n\nand system identification",
            "> Neurophysiological experiments",
            "must-almost by definition-be",
            "many fewer than toperations",
            r"$e_j \wedge e_j$",
            "<sup>♠</sup>",
            "| 0  | 0000 | 0000<br>0000",
            "| 0 0 | 0 1 | 0 2 |",
            "818283 + 818485",
            "black cells. And at the bottom are the\n\nof\n\nthese",
            r"basic  $2 \times 2$  patterns.",
            "in designing Mathematica",
            "single Mathematica pattern",
            "success of Mathematica",
            "language—like Mathematica—that",
        )
        for residue in raw_only:
            with self.subTest(raw_residue=residue):
                self.assertEqual(self.raw_text.count(residue), 1)
                self.assertNotIn(residue, self.rendered)

        residues = (
            "2 x 2 template",
            "8 x 8 basic forms",
            "32 x 32.",
            "$Log[n]^2$ .",
            "818283",
            "\t",
            "\ufffd",
        )
        for residue in residues:
            with self.subTest(residue=residue):
                self.assertNotIn(residue, self.rendered)

        self.assertNotRegex(self.rendered, r"(?m)^\|\s*0\s*\|\s*0000\s*\|")
        self.assertNotRegex(self.rendered, r"(?m)^\|\s*0 0\s*\|\s*0 1\s*\|")
        self.assertNotRegex(
            self.rendered,
            r"(?m)^(?:of|these|minimal representations|collections of possibilities\.)$",
        )


if __name__ == "__main__":
    unittest.main()
