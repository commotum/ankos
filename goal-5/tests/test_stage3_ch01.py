from __future__ import annotations

import copy
import re
import sys
import unittest
from pathlib import Path


GOAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402
import validate  # noqa: E402


def jpeg_dimensions(data: bytes) -> tuple[int, int]:
    if not data.startswith(b"\xff\xd8"):
        raise AssertionError("not a JPEG")
    index = 2
    start_of_frame = {
        0xC0,
        0xC1,
        0xC2,
        0xC3,
        0xC5,
        0xC6,
        0xC7,
        0xC9,
        0xCA,
        0xCB,
        0xCD,
        0xCE,
        0xCF,
    }
    while index < len(data):
        while index < len(data) and data[index] != 0xFF:
            index += 1
        while index < len(data) and data[index] == 0xFF:
            index += 1
        if index >= len(data):
            break
        marker = data[index]
        index += 1
        if marker in {0x01, 0xD8, 0xD9}:
            continue
        if index + 2 > len(data):
            break
        length = int.from_bytes(data[index : index + 2], "big")
        if length < 2 or index + length > len(data):
            break
        if marker in start_of_frame:
            height = int.from_bytes(data[index + 3 : index + 5], "big")
            width = int.from_bytes(data[index + 5 : index + 7], "big")
            return width, height
        index += length
    raise AssertionError("JPEG has no supported start-of-frame marker")


class ChapterOneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.document = next(row for row in cls.documents if row["id"] == "CH01")
        cls.path = build.safe_relative_path(cls.document["output_path"], suffix=".md")
        cls.raw_text = cls.raw[
            cls.document["raw_start_byte"] : cls.document["raw_end_byte_exclusive"]
        ].decode("utf-8")
        cls.rendered = build.document_bytes(
            cls.raw, cls.documents, cls.corrections
        )[cls.path].decode("utf-8")

    def test_first_pass_corrections_are_exact_and_source_verified(self) -> None:
        relevant = [row for row in self.corrections if row["document_id"] == "CH01"]
        self.assertEqual(len(relevant), 27)
        self.assertEqual(
            [row["id"] for row in relevant],
            [f"G5-C-{number:04d}" for number in range(80, 107)],
        )
        self.assertTrue(
            all(row["verification_status"] == "SOURCE_VERIFIED" for row in relevant)
        )
        self.assertTrue(all(row["expected_count"] == 1 for row in relevant))
        self.assertTrue(
            all(
                17 <= int(str(row["authoritative_location"])[4:8]) <= 37
                for row in relevant
            )
        )

    def test_heading_emphasis_and_source_punctuation_are_restored(self) -> None:
        self.assertTrue(
            self.rendered.startswith(
                "![](_page_16_Picture_0.jpeg)\n\n"
                "## The Foundations for a New Kind of Science\n\n"
                "### An Outline of Basic Ideas\n\n"
            )
        )
        headings = (
            "An Outline of Basic Ideas",
            "Relations to Other Areas",
            "Some Past Initiatives",
            "The Personal Story of the Science in This Book",
        )
        for heading in headings:
            self.assertEqual(self.rendered.count(f"### {heading}"), 1)
        self.assertNotIn("####", self.rendered)

        labels = (
            "Mathematics",
            "Physics",
            "Biology",
            "Social Sciences",
            "Computer Science",
            "Philosophy",
            "Art",
            "Technology",
            "Artificial Intelligence",
            "Artificial Life",
            "Catastrophe Theory",
            "Chaos Theory",
            "Complexity Theory",
            "Computational Complexity Theory",
            "Cybernetics",
            "Dynamical Systems Theory",
            "Evolution Theory",
            "Experimental Mathematics",
            "Fractal Geometry",
            "General Systems Theory",
            "Nanotechnology",
            "Nonlinear Dynamics",
            "Scientific Computing",
            "Self-Organization",
            "Statistical Mechanics",
        )
        for label in labels:
            self.assertEqual(self.rendered.count(f"**{label}.**"), 1)
        self.assertEqual(len(re.findall(r"\bMathematica\b", self.rendered)), 7)
        self.assertEqual(self.rendered.count("*Mathematica*"), 7)
        self.assertIn("Gödel’s Theorem", self.rendered)
        self.assertNotIn("Gödel's Theorem", self.rendered)
        self.assertIn("“cellular automata”", self.rendered)
        self.assertNotIn('"cellular automata"', self.rendered)

    def test_false_page_paragraphs_and_ocr_folio_are_removed(self) -> None:
        self.assertIn("surrounded\n\nī\n\nby computers", self.raw_text)
        self.assertNotIn("ī", self.rendered)
        correct_joins = (
            "surrounded by computers",
            "Yet despite all its development",
            "analysis can be thought of as computations",
            "systems, from simple programs to brains",
            "natural selection as a foundation—leading",
            "catastrophe theory was concerned with showing",
            "advent of computers and *Mathematica*. But almost",
            "same complex patterns of flow occur",
            "discoveries about what simple programs do",
            "avoid. Yet over and over again",
        )
        for text in correct_joins:
            self.assertIn(text, self.rendered)
        false_splits = (
            "Yet despite\n\nall",
            "can be\n\nthought",
            "systems, from\n\nsimple",
            "selection as\n\na foundation",
            "theory was\n\nconcerned",
            "computers and\n\nMathematica",
            "patterns\n\nof flow",
            "about what\n\nsimple programs",
            "Yet over\n\nand over",
        )
        for text in false_splits:
            self.assertNotIn(text, self.rendered)

    def test_figures_follow_their_referring_paragraphs_once(self) -> None:
        cover_group = (
            "computer.\n\n![](_page_32_Picture_8.jpeg)\n\n"
            "The book cover that originally sparked my interest in some of the "
            "issues discussed in this book.\n\nThe computer to which"
        )
        printout_group = (
            "complexity could emerge.\n\n![](_page_34_Figure_9.jpeg)\n\n"
            "A reproduction of the computer printout that first gave me a hint "
            "of some of the central phenomena in this book.\n\nBut how could"
        )
        self.assertIn(cover_group, self.rendered)
        self.assertIn(printout_group, self.rendered)
        self.assertEqual(self.rendered.count("![](_page_32_Picture_8.jpeg)"), 1)
        self.assertEqual(self.rendered.count("![](_page_34_Figure_9.jpeg)"), 1)
        self.assertIn("scientific community. And by the mid-1980s", self.rendered)

    def test_opener_uses_a_source_faithful_repaired_only_asset(self) -> None:
        opener = next(row for row in self.images if row["ordinal"] == 2)
        self.assertEqual(opener["document_id"], "CH01")
        self.assertEqual(
            opener["repaired_authoritative_location"],
            "pdf:0017; chapter opener composite",
        )
        self.assertEqual(
            (opener["repaired_width_px"], opener["repaired_height_px"]),
            (154, 200),
        )
        legacy = build.LEGACY_ROOT / Path(opener["asset_relative_path"])
        repaired = build.REPO_ROOT / Path(opener["repaired_asset_relative_path"])
        output = build.OUTPUT_ROOT / Path(self.path).parent / legacy.name
        legacy_bytes = legacy.read_bytes()
        repaired_bytes = repaired.read_bytes()
        self.assertEqual(
            build.sha256(legacy_bytes),
            "03a76d3233a7a24635c884c3c2f5c3216906e253bff1eacc573f428c4c183469",
        )
        self.assertEqual(build.sha256(repaired_bytes), opener["repaired_asset_sha256"])
        self.assertNotEqual(legacy_bytes, repaired_bytes)
        self.assertEqual(jpeg_dimensions(repaired_bytes), (154, 200))
        self.assertEqual(output.read_bytes(), repaired_bytes)

        missing_evidence = copy.deepcopy(self.images)
        missing_evidence[1].pop("repaired_reason")
        with self.assertRaises(build.BuildError):
            build.validate_images(self.raw, self.documents, missing_evidence)
        changed_override = copy.deepcopy(self.images)
        changed_override[1]["repaired_asset_sha256"] = "0" * 64
        with self.assertRaises(build.BuildError):
            build.validate_images(self.raw, self.documents, changed_override)

    def test_first_pass_coverage_is_recorded_without_claiming_a_second(self) -> None:
        rows = validate.validate_coverage(self.documents)
        chapter = next(row for row in rows if row["document_id"] == "CH01")
        self.assertEqual((chapter["first_pass"], chapter["second_pass"]), ("YES", "NO"))
        self.assertEqual(chapter["reviewer_type"], "agent")


if __name__ == "__main__":
    unittest.main()
