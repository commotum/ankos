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
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
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
        self.assertEqual(len(relevant), 17)
        self.assertEqual(
            [row["id"] for row in relevant],
            [f"G5-C-{number:04d}" for number in range(107, 124)],
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
        self.assertNotIn("3.141592653...", self.rendered)
        self.assertNotIn("formula  $", self.rendered)
        self.assertNotIn("$ . In", self.rendered)
        self.assertIn(
            "cells a total of about 12 million times. <sup>▶</sup>\n\n"
            "![](_page_48_Picture_2.jpeg)",
            self.rendered,
        )
        self.assertEqual(self.rendered.count("<sup>▶</sup>"), 1)
        self.assertEqual(self.rendered.count("<sup>◀</sup>"), 1)

    def test_source_added_opener_is_pinned_and_mutation_checked(self) -> None:
        self.assertEqual(len(self.added_assets), 1)
        opener = self.added_assets[0]
        self.assertEqual(opener["id"], "G5-A-0001")
        self.assertEqual(opener["document_id"], "CH02")
        self.assertEqual(opener["authoritative_location"], "pdf:0039; chapter opener panel")
        self.assertEqual((opener["width_px"], opener["height_px"]), (154, 200))
        source = build.REPO_ROOT / Path(opener["asset_relative_path"])
        output = build.OUTPUT_ROOT / Path(self.path).parent / source.name
        payload = source.read_bytes()
        self.assertEqual(build.sha256(payload), opener["asset_sha256"])
        self.assertEqual(build.jpeg_dimensions(payload), (154, 200))
        self.assertEqual(output.read_bytes(), payload)
        self.assertEqual(self.rendered.count(f"![]({source.name})"), 1)

        mutations = []
        missing_reason = copy.deepcopy(self.added_assets)
        missing_reason[0].pop("reason")
        mutations.append(missing_reason)
        wrong_hash = copy.deepcopy(self.added_assets)
        wrong_hash[0]["asset_sha256"] = "0" * 64
        mutations.append(wrong_hash)
        wrong_dimensions = copy.deepcopy(self.added_assets)
        wrong_dimensions[0]["width_px"] = 1
        mutations.append(wrong_dimensions)
        wrong_owner = copy.deepcopy(self.added_assets)
        wrong_owner[0]["document_id"] = "CH01"
        mutations.append(wrong_owner)
        output_collision = copy.deepcopy(self.added_assets)
        output_collision[0]["asset_relative_path"] = (
            "goal-5/assets/CH02/_page_39_Figure_2.jpeg"
        )
        mutations.append(output_collision)
        unverified = copy.deepcopy(self.added_assets)
        unverified[0]["verification_status"] = "INFERRED"
        mutations.append(unverified)
        for index, rows in enumerate(mutations):
            with self.subTest(index=index):
                with self.assertRaises(build.BuildError):
                    build.validate_added_assets(self.documents, self.images, rows)

    def test_first_pass_coverage_is_recorded_without_claiming_a_second(self) -> None:
        rows = validate.validate_coverage(self.documents)
        chapter = next(row for row in rows if row["document_id"] == "CH02")
        self.assertEqual((chapter["first_pass"], chapter["second_pass"]), ("YES", "NO"))
        self.assertEqual(chapter["reviewer_type"], "agent")


if __name__ == "__main__":
    unittest.main()
