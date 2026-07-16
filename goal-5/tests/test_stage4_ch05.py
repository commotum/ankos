from __future__ import annotations

import copy
import re
import sys
import unittest
from pathlib import Path


GOAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402


class ChapterFiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.document = next(row for row in cls.documents if row["id"] == "CH05")
        cls.path = build.safe_relative_path(cls.document["output_path"], suffix=".md")
        cls.raw_text = cls.raw[
            cls.document["raw_start_byte"] : cls.document["raw_end_byte_exclusive"]
        ].decode("utf-8")
        cls.rendered = build.document_bytes(
            cls.raw, cls.documents, cls.corrections
        )[cls.path].decode("utf-8")

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

    def test_range_and_guarded_corrections_are_exact(self) -> None:
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
                2142,
                2699,
                355646,
                418051,
                558,
                62405,
                "d06e5b3e21899aba420e8e33a85c608f0e02745e6e390149590538f4460cede7",
                185,
                238,
                "169",
                "222",
            ),
        )
        relevant = [
            row for row in self.corrections if row["document_id"] == "CH05"
        ]
        self.assertEqual(len(relevant), 52)
        self.assertEqual(
            [row["id"] for row in relevant],
            [f"G5-C-{number:04d}" for number in range(304, 356)],
        )
        self.assertTrue(all(row["expected_count"] == 1 for row in relevant))
        self.assertTrue(
            all(row["verification_status"] == "SOURCE_VERIFIED" for row in relevant)
        )
        self.assertTrue(all(row["reviewer_type"] == "agent" for row in relevant))
        self.assertTrue(
            all(
                185
                <= int(re.match(r"pdf:(\d{4})", row["authoritative_location"])[1])
                <= 237
                for row in relevant
            )
        )
        self.assertTrue(
            all(
                self.document["raw_start_byte"]
                <= row["raw_start_byte"]
                < self.document["raw_end_byte_exclusive"]
                for row in relevant
            )
        )

    def test_heading_hierarchy_and_restored_captions(self) -> None:
        self.assertTrue(
            self.rendered.startswith(
                "![](_page_184_Picture_0.jpeg)\n\n"
                "## Two Dimensions and Beyond\n\n"
                "### Introduction\n\n"
            )
        )
        headings = (
            "Introduction",
            "Cellular Automata",
            "Turing Machines",
            "Substitution Systems and Fractals",
            "Network Systems",
            "Multiway Systems",
            "Systems Based on Constraints",
        )
        self.assertEqual(self.rendered.count("\n### "), len(headings))
        for heading in headings:
            self.assertEqual(self.rendered.count(f"### {heading}"), 1)
        self.assertNotIn("####", self.rendered)
        self.assertNotIn("### **", self.rendered)
        self.assertNotRegex(self.rendered, r"(?m)^# 5$")
        self.assertNotIn("\nO F\n", self.rendered)
        self.assertNotIn("\nSCIENCE\n", self.rendered)

        image_caption_blocks = (
            (
                "![](_page_187_Picture_2.jpeg)",
                "A three-dimensional object formed by stacking the two-dimensional "
                "patterns from the bottom of the previous page.",
            ),
            (
                "![](_page_195_Picture_2.jpeg)",
                "Three-dimensional objects formed by stacking successive "
                "two-dimensional patterns produced in the evolution of the "
                "cellular automaton from the previous page.",
            ),
            (
                "![](_page_199_Figure_3.jpeg)",
                "An example of a two-dimensional Turing machine whose head has "
                "three possible states.",
            ),
            (
                "![](_page_202_Rule_Strip.jpeg)",
                "A two-dimensional substitution system in which each square is "
                "replaced by four smaller squares at every step according to the "
                "rule shown on the left.",
            ),
            (
                "![](_page_206_Picture_1.jpeg)",
                "Examples of fractal patterns produced by repeatedly applying the "
                "geometrical rules shown for a total of 12 steps.",
            ),
            (
                "![](_page_207_Figure_1.jpeg)",
                "A two-dimensional neighbor-dependent substitution system. The "
                "grid of cells is assumed to wrap around in both its dimensions.\n\n"
                "Patterns generated by 8 steps of evolution in various "
                "two-dimensional neighbor-dependent substitution systems.",
            ),
            (
                "![](_page_212_Picture_2.jpeg)",
                "An example of a network that forms a nested geometrical structure.",
            ),
            (
                "![](_page_223_Figure_1.jpeg)",
                "Collections of states generated at particular steps in the "
                "evolution of various multiway systems.",
            ),
            (
                "![](_page_234_Template_Strip.jpeg)",
                "The simplest system based on constraints that is forced to "
                "exhibit a non-repetitive pattern.",
            ),
        )
        for image, caption in image_caption_blocks:
            with self.subTest(image=image):
                self.assertEqual(self.rendered.count(f"{image}\n\n{caption}"), 1)

    def test_turing_panels_rules_and_labels_follow_source_order(self) -> None:
        # Panels (b) and (d) retain their printed labels in their pinned images;
        # the source labels for (a), (c), and (e) remain live Markdown.
        self.assert_order(
            "![](_page_199_Figure_3.jpeg)",
            "An example of a two-dimensional Turing machine whose head has three possible states.",
            "![](_page_200_Figure_2.jpeg)",
            "*(a) (step 1000)*",
            "![](_page_200_Figure_3.jpeg)",
            "![](_page_200_Figure_4.jpeg)",
            "*(c) (step 3000)*",
            "![](_page_200_Figure_5.jpeg)",
            "![](_page_200_Panel_E.jpeg)",
            "*(e) (step 10000)*",
            "![](_page_200_Figure_6.jpeg)",
            "Examples of patterns produced by two-dimensional Turing machines "
            "whose heads have four possible states.",
            "![](_page_201_Figure_2.jpeg)",
            "*100,000 steps*",
            "![](_page_201_Figure_4.jpeg)",
            "*500,000 steps*",
            "The path traced out by the head of the two-dimensional Turing machine "
            "with rule (e) from the previous page.",
        )
        turing_plate = self.rendered[
            self.rendered.index("![](_page_200_Figure_2.jpeg)") : self.rendered.index(
                "![](_page_201_Figure_2.jpeg)"
            )
        ]
        self.assertEqual(
            re.findall(r"(?m)^\*\([ace]\) \(step \d+\)\*$", turing_plate),
            ["*(a) (step 1000)*", "*(c) (step 3000)*", "*(e) (step 10000)*"],
        )

    def test_pdf219_rules_are_exact_live_code_without_corrupt_duplicate(self) -> None:
        rule_d = (
            "{{1, 1} → {{{1, 2}, {1, 2}}, {}}, {1, 2} → {{2, 2}, {{1}, {1}}}, "
            "{2, 1} → {{1}, {{}, {2}}}, {2, 2} → {{1, 2}, {2, 1}}, {2, 3} → "
            "{{{2, 1}, {2}}, {1}}, {2, 4} → {{1}, {1, 1}}}"
        )
        rule_e = (
            "{{1, 1} → {{}, {{1, 1}, {1, 2}}}, {1, 2} → {{{}, {1}}, {{1, 1}, "
            "{1, 2}}}, {2, 1} → {{2}, {}}, {2, 2} → {{{2, 1}, {1}}, {{1, 1}, "
            "{2}}}, {2, 3} → {{2, 2}, {2}}, {2, 4} → {{2, 1}, {2}}}"
        )
        block_d = f"```text\n{rule_d}\n```"
        block_e = f"```text\n{rule_e}\n```"
        self.assertEqual(
            re.findall(r"```text\n.*?\n```", self.rendered, re.DOTALL),
            [block_d, block_e],
        )
        self.assert_order(
            "![](_page_218_Figure_2.jpeg)",
            "*(d)*",
            block_d,
            "*(e)*",
            block_e,
            "Network systems in which the total number of nodes obtained on "
            "successive steps appears to vary in a largely random way forever.",
        )
        self.assertEqual(self.rendered.count(rule_d), 1)
        self.assertEqual(self.rendered.count(rule_e), 1)
        self.assertNotIn(r"\begin{array}", self.rendered)
        self.assertNotIn("((2,1),((2,1)", self.rendered)

    def test_multiplication_notation_is_normalized_and_tab_free(self) -> None:
        expected = (
            "tessellation of $5 \\times 5$ blocks of cells.",
            "tessellation of $5 \\times 10$ blocks of cells; pattern (b) from a "
            "tessellation of $24 \\times 24$ blocks.",
            "templates that involve complete $3 \\times 3$ blocks of cells",
            "constraint involving $3 \\times 3$ templates of cells.",
            "only the 56 $3 \\times 3$ templates shown at left",
        )
        for text in expected:
            with self.subTest(text=text):
                self.assertEqual(self.rendered.count(text), 1)
        self.assertEqual(self.rendered.count(r"\times"), 6)
        self.assertNotIn("\t", self.rendered)
        self.assertNotIn(r"$3\times3$", self.rendered)
        self.assertNotIn(r"$56.3 \times 3$", self.rendered)

    def test_pdf228_figure_follows_both_explanatory_paragraphs(self) -> None:
        self.assert_order(
            "What about other constraints? The pictures on the facing page show "
            "schematically what happens with constraints that require each cell",
            "Several kinds of results are seen. In the two cases shown as blank "
            "rectangles on the upper right",
            "![](_page_227_Figure_3.jpeg)",
            "Patterns satisfying constraints which specify that every black cell "
            "and every white cell must have a certain fixed number of black and "
            "white neighbors.",
            "So what about more complicated constraints? The pictures below show "
            "examples based on constraints",
            "![](_page_228_Figure_5.jpeg)",
            "Systems specified by the constraint that the local arrangement of "
            "colors around every cell must match the fixed set of possible templates shown.",
        )

    def test_pdf235_and_pdf236_compound_figures_precede_their_captions(self) -> None:
        self.assert_order(
            "![](_page_234_Figure_2.jpeg)",
            "![](_page_234_Template_Strip.jpeg)",
            "The simplest system based on constraints that is forced to exhibit "
            "a non-repetitive pattern.",
            "The idea is to set up templates that involve complete $3 \\times 3$ "
            "blocks of cells",
            "![](_page_235_Picture_4.jpeg)",
            "![](_page_235_Picture_6.jpeg)",
            "An example of a system based on a constraint involving $3 \\times 3$ "
            "templates of cells.",
            "What about more complex patterns? Searches have not succeeded in "
            "finding anything.",
            "![](_page_236_Picture_1.jpeg)",
            "![](_page_236_Picture_2.jpeg)",
            "A system based on a constraint, in which a complex and largely random "
            "pattern is forced to occur.",
        )

    def test_repaired_and_added_assets_are_pinned_mapped_and_ordered(self) -> None:
        chapter_images = [row for row in self.images if row["document_id"] == "CH05"]
        self.assertEqual(len(chapter_images), 77)
        self.assertEqual(
            [row["ordinal"] for row in chapter_images], list(range(169, 246))
        )
        self.assertTrue(all(row["split_status"] == "PRESENT" for row in chapter_images))

        expected_repairs = {
            174: (
                "05110d831a2704d60c2443a204932e52dab30450ec241d00cc5d156c650edad3",
                (3484, 2368),
            ),
            182: (
                "261f34529b5464b80b8fea0194f7fe86bca089e5eb3e755213a4476d63bd2254",
                (1178, 1242),
            ),
            191: (
                "718e289f093548b0f38f0a628859b4aeef2ec5d11419647bb813f4c10f769fde",
                (1103, 438),
            ),
            192: (
                "b9b06f73d68024fb38f7fd238b1e08cd24e6e78a9e752295fe74494861328e14",
                (260, 1004),
            ),
            194: (
                "79b8bf7927c0f3297ead40e9a9c3496949d652501e42352d4270a998fe2bce01",
                (486, 472),
            ),
            200: (
                "75e29e39338d4a88ea105781fd42b9bf6cd97b3ede4b49f0ff43c2d4440a61fc",
                (1141, 1349),
            ),
            205: (
                "3e71a719ad6b0727b58406dae98fcc21de1d6ad4bc04ed01ceacad827da1ebc5",
                (1094, 981),
            ),
            206: (
                "4f8728cb5a5bc587e6c06a8e931b2c0721ba6ae58f7ab3835a69144bbb7fc458",
                (1184, 1005),
            ),
            210: (
                "92ff6d41056943bce46467bb15093ae11cdf847df8d25af8c74b273456749a7f",
                (1128, 767),
            ),
            217: (
                "365d660b70fd0e75635383613e51781628f70be14a7ccc1f9653f2086526a8eb",
                (1052, 1023),
            ),
            228: (
                "1b0bc5181f40eee841675b8ee0d2fef929ec1122e3e75595a5945eb8edb99a0f",
                (1059, 1089),
            ),
        }
        repaired_rows = [
            row for row in chapter_images if "repaired_asset_relative_path" in row
        ]
        self.assertEqual(
            [row["ordinal"] for row in repaired_rows], list(expected_repairs)
        )
        for row in repaired_rows:
            digest, dimensions = expected_repairs[row["ordinal"]]
            with self.subTest(repaired_ordinal=row["ordinal"]):
                legacy = build.LEGACY_ROOT / Path(row["asset_relative_path"])
                repaired = build.REPO_ROOT / Path(
                    row["repaired_asset_relative_path"]
                )
                output = build.OUTPUT_ROOT / Path(self.path).parent / legacy.name
                payload = repaired.read_bytes()
                self.assertEqual(row["repaired_asset_sha256"], digest)
                self.assertEqual(build.sha256(payload), digest)
                self.assertEqual(build.jpeg_dimensions(payload), dimensions)
                self.assertEqual(
                    (row["repaired_width_px"], row["repaired_height_px"]),
                    dimensions,
                )
                self.assertNotEqual(payload, legacy.read_bytes())
                self.assertEqual(output.read_bytes(), payload)

        chapter_added = [
            row for row in self.added_assets if row["document_id"] == "CH05"
        ]
        expected_added = {
            "G5-A-0009": (
                "8b9903aebdcc8c47b1d8b97c060398dd5f884dd1ecadae91085edb3219a84648",
                (486, 649),
            ),
            "G5-A-0010": (
                "b29c3ffcb6beb5d49e8af80f7ae17dde9504c14cc2822941173287f0f2fc9b19",
                (308, 76),
            ),
            "G5-A-0011": (
                "4c3b264f02ddbc8b656402401f90e6f27f8b1105ef197a2655f37b120ee93e51",
                (632, 58),
            ),
        }
        self.assertEqual([row["id"] for row in chapter_added], list(expected_added))
        added_names: dict[str, str] = {}
        for row in chapter_added:
            digest, dimensions = expected_added[row["id"]]
            with self.subTest(added=row["id"]):
                source = build.REPO_ROOT / Path(row["asset_relative_path"])
                output = build.OUTPUT_ROOT / Path(self.path).parent / source.name
                payload = source.read_bytes()
                added_names[row["id"]] = source.name
                self.assertEqual(row["asset_sha256"], digest)
                self.assertEqual(build.sha256(payload), digest)
                self.assertEqual(build.jpeg_dimensions(payload), dimensions)
                self.assertEqual((row["width_px"], row["height_px"]), dimensions)
                self.assertEqual(output.read_bytes(), payload)

        mapped_names = {
            row["ordinal"]: Path(row["asset_relative_path"]).name
            for row in chapter_images
        }
        expected_references = (
            [mapped_names[number] for number in range(169, 196)]
            + [added_names["G5-A-0009"]]
            + [mapped_names[number] for number in range(196, 200)]
            + [added_names["G5-A-0010"]]
            + [mapped_names[number] for number in range(200, 242)]
            + [added_names["G5-A-0011"]]
            + [mapped_names[number] for number in range(242, 246)]
        )
        references = re.findall(r"!\[\]\(([^)]+\.jpeg)\)", self.rendered)
        self.assertEqual(len(references), 80)
        self.assertEqual(len(set(references)), 80)
        self.assertEqual(references, expected_references)

        changed_hash = copy.deepcopy(self.images)
        changed = next(row for row in changed_hash if row["ordinal"] == 217)
        changed["repaired_asset_sha256"] = "0" * 64
        with self.assertRaises(build.BuildError):
            build.validate_images(self.raw, self.documents, changed_hash)
        missing_reason = copy.deepcopy(self.added_assets)
        changed_added = next(
            row for row in missing_reason if row["id"] == "G5-A-0010"
        )
        changed_added.pop("reason")
        with self.assertRaises(build.BuildError):
            build.validate_added_assets(self.documents, self.images, missing_reason)


if __name__ == "__main__":
    unittest.main()
