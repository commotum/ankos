from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


GOAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402
import validate  # noqa: E402


class ChapterTwoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.all_added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.added_assets = [
            row for row in cls.all_added_assets if row["document_id"] == "CH02"
        ]
        cls.document = next(row for row in cls.documents if row["id"] == "CH02")
        cls.path = build.safe_relative_path(cls.document["output_path"], suffix=".md")
        cls.raw_text = cls.raw[
            cls.document["raw_start_byte"] : cls.document["raw_end_byte_exclusive"]
        ].decode("utf-8")
        cls.rendered = build.document_bytes(
            cls.raw, cls.documents, cls.corrections
        )[cls.path].decode("utf-8")

    def test_first_pass_corrections_are_exact_and_source_verified(self) -> None:
        relevant = [row for row in self.corrections if row["document_id"] == "CH02"]
        self.assertEqual(len(relevant), 26)
        self.assertEqual(
            [row["id"] for row in relevant],
            [f"G5-C-{number:04d}" for number in range(107, 133)],
        )
        self.assertTrue(
            all(row["verification_status"] == "SOURCE_VERIFIED" for row in relevant)
        )
        self.assertTrue(all(row["expected_count"] == 1 for row in relevant))
        self.assertTrue(
            all(
                39 <= int(str(row["authoritative_location"])[4:8]) <= 64
                for row in relevant
            )
        )

    def test_heading_furniture_caption_and_page_break_defects_are_removed(self) -> None:
        self.assertTrue(
            self.rendered.startswith(
                "![](_page_38_Chapter_Opener.jpeg)\n\n"
                "## The Crucial Experiment\n\n"
                "### How Do Simple Programs Behave?\n\n"
            )
        )
        self.assertNotIn("# 2", self.rendered)
        self.assertNotIn("#### STEPHEN WOLFRAM A NEW KIND OF SCIENCE", self.rendered)
        self.assertEqual(self.rendered.count("\n### "), 3)
        for joined in (
            "each box gives one of the possible combinations",
            "the picture shows that the overall pattern",
            "started from a single black cell. But now",
            "at least for cellular automata with rules",
            "only rather basic computer technology to make",
            "look at a program and immediately know",
            "to have arisen that there might be a general phenomenon",
        ):
            self.assertIn(joined, self.rendered)
        for split in (
            "each box\n\ngives",
            "the picture\n\nshows",
            "single\n\nblack cell",
            "at least for\n\ncellular automata",
            "rather basic\n\ncomputer technology",
            "look at a program\n\nand immediately",
            "arisen that\n\nthere might",
        ):
            self.assertNotIn(split, self.rendered)
        self.assertIn("called “fractal” or “self-similar”", self.rendered)
        self.assertNotIn('called "fractal" or "self-similar"', self.rendered)

    def test_technical_notation_and_continuation_markers_match_source(self) -> None:
        self.assertIn(
            "formula $a_i' = Mod[a_{i-1} + a_{i+1}, 2]$. In",
            self.rendered,
        )
        self.assertIn("$\\pi \\approx 3.141592653\\ldots$", self.rendered)
        self.assertIn("digits of $\\pi$ had", self.rendered)
        self.assertIn("computing $\\pi$ could", self.rendered)
        self.assertNotIn("3.141592653...", self.rendered)
        self.assertNotIn("formula  $", self.rendered)
        self.assertNotIn("$ . In", self.rendered)
        self.assertNotIn("  $", self.rendered)
        self.assertNotIn("$  ", self.rendered)
        self.assertIn(
            "![](_page_40_Picture_6.jpeg)\n\n"
            "![](_page_40_Rule_90.jpeg)\n\n"
            "A cellular automaton",
            self.rendered,
        )
        self.assertIn(
            "![](_page_42_Figure_4.jpeg)\n\n"
            "![](_page_42_Rule_30.jpeg)\n\n"
            "A cellular automaton",
            self.rendered,
        )
        self.assertIn(
            "cells a total of about 12 million times. <sup>▶</sup>\n\n"
            "![](_page_48_Picture_2.jpeg)",
            self.rendered,
        )
        self.assertEqual(self.rendered.count("<sup>▶</sup>"), 1)
        self.assertEqual(self.rendered.count("<sup>◀</sup>"), 1)

    def test_source_added_assets_are_pinned_and_mutation_checked(self) -> None:
        self.assertEqual(len(self.added_assets), 3)
        expected = {
            "G5-A-0001": (
                "pdf:0039; chapter opener panel",
                "_page_38_Chapter_Opener.jpeg",
                "0a78f582ac67a861dc64c70ea8905beebd95de3622e4e19949d7ec2002f51d79",
                (154, 200),
            ),
            "G5-A-0002": (
                "pdf:0041; rule-90 figure rule strip",
                "_page_40_Rule_90.jpeg",
                "fe3574d9b23b76d477752ab6aca234b3f9872d1f1f4f5f4eb96b973c52fe3b1e",
                (376, 39),
            ),
            "G5-A-0003": (
                "pdf:0043; rule-30 figure rule strip",
                "_page_42_Rule_30.jpeg",
                "e2b626682ac2c02fbff5eb5eb91e0ebd1f1f1e8b38eaf8b36ed572c45417f1b8",
                (376, 39),
            ),
        }
        self.assertEqual({row["id"] for row in self.added_assets}, set(expected))
        for asset in self.added_assets:
            location, name, digest, dimensions = expected[asset["id"]]
            with self.subTest(asset=asset["id"]):
                self.assertEqual(asset["document_id"], "CH02")
                self.assertEqual(asset["authoritative_location"], location)
                self.assertEqual(asset["asset_sha256"], digest)
                self.assertEqual(
                    (asset["width_px"], asset["height_px"]), dimensions
                )
                source = build.REPO_ROOT / Path(asset["asset_relative_path"])
                output = build.OUTPUT_ROOT / Path(self.path).parent / source.name
                payload = source.read_bytes()
                self.assertEqual(source.name, name)
                self.assertEqual(build.sha256(payload), digest)
                self.assertEqual(build.jpeg_dimensions(payload), dimensions)
                self.assertEqual(output.read_bytes(), payload)
                self.assertEqual(self.rendered.count(f"![]({name})"), 1)

        opener = self.added_assets[0]
        self.assertEqual(opener["id"], "G5-A-0001")

        mutations = []
        missing_reason = copy.deepcopy(self.all_added_assets)
        missing_reason[0].pop("reason")
        mutations.append(missing_reason)
        wrong_hash = copy.deepcopy(self.all_added_assets)
        wrong_hash[0]["asset_sha256"] = "0" * 64
        mutations.append(wrong_hash)
        wrong_dimensions = copy.deepcopy(self.all_added_assets)
        wrong_dimensions[0]["width_px"] = 1
        mutations.append(wrong_dimensions)
        wrong_owner = copy.deepcopy(self.all_added_assets)
        wrong_owner[0]["document_id"] = "CH01"
        mutations.append(wrong_owner)
        output_collision = copy.deepcopy(self.all_added_assets)
        output_collision[0]["asset_relative_path"] = (
            "goal-5/assets/CH02/_page_39_Figure_2.jpeg"
        )
        mutations.append(output_collision)
        unverified = copy.deepcopy(self.all_added_assets)
        unverified[0]["verification_status"] = "INFERRED"
        mutations.append(unverified)
        for index, rows in enumerate(mutations):
            with self.subTest(index=index):
                with self.assertRaises(build.BuildError):
                    build.validate_added_assets(self.documents, self.images, rows)

    def test_full_page_plates_do_not_split_prose_and_keep_source_order(self) -> None:
        rule_90_paragraph = (
            "The picture below shows the pattern produced by a cellular automaton "
            "of the same type as before, but with a slightly different rule. This "
            "time the rule specifies that a cell should be black when either its "
            "left neighbor or its right neighbor—but not both—were black on the "
            "step before. And again this rule is undeniably quite simple. But now "
            "the picture shows that the pattern it produces is not so simple."
        )
        rule_30_sentence = (
            "For even though it may be impossible to predict what color will occur "
            "at any specific step, one still knows for example that black and white "
            "will on average always occur equally often."
        )
        rule_110_sentence = (
            "The only sure way to answer these questions, it seems, is just to run "
            "the cellular automaton for as many steps as are needed, and to watch "
            "what happens."
        )
        self.assertIn(rule_90_paragraph, self.rendered)
        self.assertIn(rule_30_sentence, self.rendered)
        self.assertIn(rule_110_sentence, self.rendered)
        self.assertNotIn("different rule.\n\n![](_page_40", self.rendered)
        self.assertNotIn("not so simple.\n\nAnd if one runs", self.rendered)
        self.assertNotIn("predict what\n\n![](_page_44", self.rendered)
        self.assertNotIn("and to\n\n![](_page_47", self.rendered)

        rule_90_markers = (
            rule_90_paragraph,
            "![](_page_40_Picture_6.jpeg)",
            "![](_page_40_Rule_90.jpeg)",
            "A cellular automaton that produces an intricate nested pattern.",
            "And if one runs the cellular automaton for more steps",
        )
        rule_90_positions = [
            self.rendered.index(marker) for marker in rule_90_markers
        ]
        self.assertEqual(rule_90_positions, sorted(rule_90_positions))

        ordered_markers = (
            rule_110_sentence,
            "![](_page_47_Figure_1.jpeg)",
            "![](_page_47_Figure_2.jpeg)",
            "<sup>▶</sup>",
            "![](_page_48_Picture_2.jpeg)",
            "![](_page_49_Picture_1.jpeg)",
            "![](_page_50_Picture_1.jpeg)",
            "![](_page_51_Picture_1.jpeg)",
            "![](_page_52_Picture_1.jpeg)",
            "![](_page_53_Picture_2.jpeg)",
            "<sup>◀</sup> A single picture of the behavior from the previous five pages.",
            "However certain one might be",
        )
        positions = [self.rendered.index(marker) for marker in ordered_markers]
        self.assertEqual(positions, sorted(positions))
        for image in (
            "_page_44_Picture_1.jpeg",
            "_page_45_Picture_2.jpeg",
            "_page_47_Figure_1.jpeg",
            "_page_47_Figure_2.jpeg",
            "_page_48_Picture_2.jpeg",
            "_page_49_Picture_1.jpeg",
            "_page_50_Picture_1.jpeg",
            "_page_51_Picture_1.jpeg",
            "_page_52_Picture_1.jpeg",
            "_page_53_Picture_2.jpeg",
        ):
            self.assertEqual(self.rendered.count(f"![]({image})"), 1)

    def test_two_pass_document_coverage_is_closed(self) -> None:
        rows = validate.validate_coverage(self.documents)
        chapter = next(row for row in rows if row["document_id"] == "CH02")
        self.assertEqual(
            (chapter["first_pass"], chapter["second_pass"]), ("YES", "YES")
        )
        self.assertEqual(chapter["reviewer_type"], "agent")


if __name__ == "__main__":
    unittest.main()
