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


EXPECTED_SHA256 = "a1384ad5ada245f65d5ba8c5ff2af275ec1101252775a33ad69a7279216688d7"
EXPECTED_BYTES = 252_955
EXPECTED_LINES = 1_686

# basename: (hash, dimensions, canonical PDF page)
EXPECTED_ADDED = {
    "_page_789_Further_Axiom_Systems.jpeg": (
        "2faa5666ec052f5d2a93dd9b9a417fa5f3f1e27f7cddf1ab9225d5bece60b8e5",
        (2101, 2790),
        "pdf:0790",
    ),
    "_page_801_Arithmetic_Universality.jpeg": (
        "59f9e51f16ee92f5c4aab8119ac5bdfb5358abce7faab457f213a03e7c391638",
        (2315, 1989),
        "pdf:0802",
    ),
    "_page_805_Diophantine_Equation_Table.jpeg": (
        "5e4e219e85018464917e6074568383cb77c8640e8bf732aa4141ec688b40a347",
        (2450, 3005),
        "pdf:0806",
    ),
    "_page_822_Logic_Primitive_Functions.jpeg": (
        "5929e2daa8f623d9c695579e81347caa4d546264a7d02b4d534a14d9026e1751",
        (2357, 1772),
        "pdf:0823",
    ),
    "_page_832_Basic_Logic_Theorems.jpeg": (
        "08983a421e1235234626dc9175c6a973056393f0f92d9fc68626cb8e6f1c7975",
        (2473, 2525),
        "pdf:0833",
    ),
    "_page_833_NAND_Theorems.jpeg": (
        "2a42adbd6d54c3bd2740b49214c26f7984ec852f5821dc6760ec4f52bddeaae6",
        (2316, 1270),
        "pdf:0834",
    ),
    "_page_846_Picture_13.jpeg": (
        "1cf33d03b5588db23d8492d39135326e63e2acfc46931b3d4add582e91c0f336",
        (468, 253),
        "pdf:0847",
    ),
}

EXPECTED_REFERENCES = [
    "_page_730_Picture_0.jpeg",
    "_page_740_Figure_2.jpeg",
    "_page_746_Figure_2.jpeg",
    "_page_747_Picture_5.jpeg",
    "_page_753_Picture_3.jpeg",
    "_page_755_Picture_2.jpeg",
    "_page_759_Figure_1.jpeg",
    "_page_760_Picture_11.jpeg",
    "_page_762_Figure_2.jpeg",
    "_page_764_Figure_1.jpeg",
    "_page_765_Picture_1.jpeg",
    "_page_769_Figure_1.jpeg",
    "_page_772_Figure_1.jpeg",
    "_page_774_Figure_1.jpeg",
    "_page_775_Figure_1.jpeg",
    "_page_776_Figure_2.jpeg",
    "_page_778_Figure_2.jpeg",
    "_page_780_Picture_10.jpeg",
    "_page_780_Picture_12.jpeg",
    "_page_782_Figure_2.jpeg",
    "_page_783_Figure_2.jpeg",
    "_page_785_Figure_2.jpeg",
    "_page_788_Figure_2.jpeg",
    "_page_789_Further_Axiom_Systems.jpeg",
    "_page_790_Figure_7.jpeg",
    "_page_791_Picture_4.jpeg",
    "_page_792_Picture_3.jpeg",
    "_page_792_Picture_4.jpeg",
    "_page_793_Picture_2.jpeg",
    "_page_793_Picture_3.jpeg",
    "_page_793_Picture_5.jpeg",
    "_page_793_Picture_6.jpeg",
    "_page_793_Picture_7.jpeg",
    "_page_793_Picture_8.jpeg",
    "_page_795_Picture_7.jpeg",
    "_page_796_Figure_2.jpeg",
    "_page_798_Picture_2.jpeg",
    "_page_801_Arithmetic_Universality.jpeg",
    "_page_805_Diophantine_Equation_Table.jpeg",
    "_page_809_Figure_1.jpeg",
    "_page_811_Figure_2.jpeg",
    "_page_813_Figure_2.jpeg",
    "_page_817_Figure_1.jpeg",
    "_page_818_Figure_2.jpeg",
    "_page_819_Figure_2.jpeg",
    "_page_820_Figure_1.jpeg",
    "_page_821_Picture_8.jpeg",
    "_page_822_Logic_Primitive_Functions.jpeg",
    "_page_823_Figure_2.jpeg",
    "_page_824_Figure_9.jpeg",
    "_page_825_Figure_1.jpeg",
    "_page_826_Figure_1.jpeg",
    "_page_827_Figure_3.jpeg",
    "_page_828_Figure_3.jpeg",
    "_page_829_Picture_2.jpeg",
    "_page_829_Figure_4.jpeg",
    "_page_832_Basic_Logic_Theorems.jpeg",
    "_page_833_NAND_Theorems.jpeg",
    "_page_839_Figure_4.jpeg",
    "_page_845_Picture_10.jpeg",
    "_page_845_Picture_12.jpeg",
    "_page_846_Picture_11.jpeg",
    "_page_846_Picture_13.jpeg",
    "_page_847_Figure_1.jpeg",
    "_page_848_Figure_2.jpeg",
    "_page_862_Picture_0.jpeg",
]


class ChapterTwelveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.document = next(row for row in cls.documents if row["id"] == "CH12")
        cls.path = build.safe_relative_path(cls.document["output_path"], suffix=".md")
        cls.rendered_bytes = build.document_bytes(
            cls.raw, cls.documents, cls.corrections
        )[cls.path]
        cls.rendered = cls.rendered_bytes.decode("utf-8")

    def assert_order(self, *markers: str) -> None:
        positions = []
        for marker in markers:
            self.assertEqual(self.rendered.count(marker), 1, marker[:100])
            positions.append(self.rendered.index(marker))
        self.assertEqual(positions, sorted(positions))

    def test_source_range_packet_and_render_are_exact(self) -> None:
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
                8608,
                10622,
                1208768,
                1540232,
                2015,
                331464,
                "a78f141c50eaf495c51d5a426d3057c9b6acffcbc5d7bb6b3a6b213cfd18bc25",
                731,
                864,
                "715",
                "848",
            ),
        )
        segment = self.raw[1208768:1540232]
        self.assertEqual(build.sha256(segment), self.document["raw_segment_sha256"])

        relevant = [row for row in self.corrections if row["document_id"] == "CH12"]
        self.assertEqual(len(self.corrections), 861)
        self.assertEqual(len(relevant), 131)
        self.assertEqual(
            [row["id"] for row in relevant],
            [f"G5-C-{number:04d}" for number in range(731, 862)],
        )
        for row in relevant:
            with self.subTest(correction=row["id"]):
                self.assertEqual(row["expected_count"], 1)
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                page = re.match(r"pdf:(\d{4})", row["authoritative_location"])
                self.assertIsNotNone(page)
                self.assertTrue(731 <= int(page.group(1)) <= 864)
                start = row["raw_start_byte"]
                before = row["before"].encode("utf-8")
                self.assertEqual(self.raw[start : start + len(before)], before)

        self.assertEqual(len(self.rendered_bytes), EXPECTED_BYTES)
        self.assertEqual(len(self.rendered.splitlines()), EXPECTED_LINES)
        self.assertEqual(build.sha256(self.rendered_bytes), EXPECTED_SHA256)
        self.assertEqual(
            validate.independent_document_bytes(
                self.raw, self.documents, self.corrections
            )[self.path],
            self.rendered_bytes,
        )

    def test_heading_hierarchy_and_high_risk_source_text_are_exact(self) -> None:
        self.assertTrue(
            self.rendered.startswith(
                "![](_page_730_Picture_0.jpeg)\n\n"
                "## The Principle of Computational Equivalence\n\n"
                "### Basic Framework\n\n"
            )
        )
        headings = (
            "Basic Framework",
            "Outline of the Principle",
            "The Content of the Principle",
            "The Validity of the Principle",
            "Explaining the Phenomenon of Complexity",
            "Computational Irreducibility",
            "The Phenomenon of Free Will",
            "Undecidability and Intractability",
            "Implications for Mathematics and Its Foundations",
            "Intelligence in the Universe",
            "Implications for Technology",
            "Historical Perspectives",
        )
        self.assertEqual(self.rendered.count("\n### "), len(headings))
        self.assert_order(*(f"### {heading}" for heading in headings))
        self.assertNotIn("####", self.rendered)

        exact_once = (
            "function like $1/x$ almost any digit in $x$",
            "the celebrated P=NP question",
            "infinite sets of integers just by a symbol like $s$.",
            "quantities like $1/0$ or the total number",
            r"symbols like $\infty$ and $\aleph_0$—the same",
            "as in a *Mathematica* pattern",
            r"Statements like $p = \neg \neg p$ do not hold",
            r"digit sequence of $\pi$ to an extraterrestrial",
            r"Explicit $\bar{\wedge}$ operators have been omitted",
            r"lemmas $\boxed{L_n}$, from which it is eventually possible to prove",
            "the lemmas ■ → ■■ and ■ → □",
            "the fifth theorem □■□ → ■□■",
        )
        for text in exact_once:
            with self.subTest(text=text):
                self.assertEqual(self.rendered.count(text), 1)
        self.assertNotIn("$P = NP$", self.rendered)
        self.assertNotIn("Explicit $\\circ$ operators have been omitted", self.rendered)

    def test_plate_order_and_caption_contracts_are_exact(self) -> None:
        self.assert_order(
            "![](_page_789_Further_Axiom_Systems.jpeg)",
            "Further axiom systems for traditional mathematics.",
            "![](_page_790_Figure_7.jpeg)",
        )
        self.assert_order(
            "![](_page_801_Arithmetic_Universality.jpeg)",
            "Universality in arithmetic, illustrated by an integer equation",
            "![](_page_805_Diophantine_Equation_Table.jpeg)",
            "Smallest solutions for various sequences of integer",
        )
        self.assert_order(
            "![](_page_822_Logic_Primitive_Functions.jpeg)",
            "Functions that can be used to formulate logic.",
            "![](_page_823_Figure_2.jpeg)",
        )
        self.assert_order(
            "![](_page_832_Basic_Logic_Theorems.jpeg)",
            "The theorems of basic logic written out",
            "![](_page_833_NAND_Theorems.jpeg)",
            "The theorems of logic formulated in terms of NAND.",
        )
        self.assert_order(
            "![](_page_846_Picture_11.jpeg)",
            "![](_page_846_Picture_13.jpeg)",
            "If the purpose is to generate a uniformly expanding pattern",
            "![](_page_847_Figure_1.jpeg)",
        )

    def test_mapped_and_added_assets_and_reference_order_are_exact(self) -> None:
        chapter_images = [row for row in self.images if row["document_id"] == "CH12"]
        chapter_added = [
            row for row in self.added_assets if row["document_id"] == "CH12"
        ]
        self.assertEqual(len(self.images), 1444)
        self.assertEqual(len(self.added_assets), 41)
        self.assertEqual(len(self.images) + len(self.added_assets), 1485)
        self.assertEqual(
            sum("repaired_asset_relative_path" in row for row in self.images), 64
        )
        self.assertEqual([row["ordinal"] for row in chapter_images], list(range(764, 823)))
        self.assertTrue(
            all("repaired_asset_relative_path" not in row for row in chapter_images)
        )
        self.assertEqual(
            [row["id"] for row in chapter_added],
            [f"G5-A-{number:04d}" for number in range(35, 42)],
        )

        for row in chapter_added:
            source = build.REPO_ROOT / Path(row["asset_relative_path"])
            output = build.OUTPUT_ROOT / Path(self.path).parent / source.name
            payload = source.read_bytes()
            expected_hash, dimensions, page = EXPECTED_ADDED[source.name]
            with self.subTest(asset=source.name):
                self.assertEqual(build.sha256(payload), expected_hash)
                self.assertEqual(row["asset_sha256"], expected_hash)
                self.assertEqual(build.jpeg_dimensions(payload), dimensions)
                self.assertEqual((row["width_px"], row["height_px"]), dimensions)
                self.assertTrue(row["authoritative_location"].startswith(page))
                self.assertEqual(output.read_bytes(), payload)

        references = re.findall(r"!\[\]\(([^)]+\.jpeg)\)", self.rendered)
        self.assertEqual(references, EXPECTED_REFERENCES)
        self.assertEqual(len(references), 66)
        self.assertEqual(len(set(references)), 66)

        changed = copy.deepcopy(self.added_assets)
        next(row for row in changed if row["id"] == "G5-A-0037")["width_px"] += 1
        with self.assertRaises(build.BuildError):
            build.validate_added_assets(self.documents, self.images, changed)

    def test_high_risk_residual_detectors_are_clean(self) -> None:
        forbidden = (
            "function like 1/x almost any digit in x",
            "symbol like s.",
            "quantities like 1/0",
            r"like  $\infty$",
            r"$\aleph_0$ —",
            r"$p=\neg\neg p$",
            r"sequence of  $\pi$",
            "as in a Mathematica pattern",
            "generatedbut",
            "generatedmany",
            "vield",
            "guite",
            "\ufffd",
        )
        for text in forbidden:
            with self.subTest(forbidden=text):
                self.assertNotIn(text, self.rendered)
        self.assertNotRegex(self.rendered, r"(?m)^\|")
        self.assertNotRegex(self.rendered, r"(?m)^>")
        self.assertNotRegex(self.rendered, r"  \$|\$  ")


if __name__ == "__main__":
    unittest.main()
