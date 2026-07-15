from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path


GOAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402
import validate  # noqa: E402


class PrefaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.document = next(row for row in cls.documents if row["id"] == "PREFACE")
        cls.path = build.safe_relative_path(cls.document["output_path"], suffix=".md")
        cls.raw_text = cls.raw[
            cls.document["raw_start_byte"] : cls.document["raw_end_byte_exclusive"]
        ].decode("utf-8")
        cls.rendered = build.document_bytes(
            cls.raw, cls.documents, cls.corrections
        )[cls.path].decode("utf-8")

    def test_all_first_pass_corrections_are_guarded_and_source_verified(self) -> None:
        relevant = [
            row for row in self.corrections if row["document_id"] == "PREFACE"
        ]
        self.assertEqual(len(relevant), 59)
        self.assertEqual(
            [row["id"] for row in relevant],
            [f"G5-C-{number:04d}" for number in range(21, 80)],
        )
        self.assertTrue(
            all(row["verification_status"] == "SOURCE_VERIFIED" for row in relevant)
        )
        self.assertTrue(
            all(
                9 <= int(str(row["authoritative_location"])[4:8]) <= 14
                for row in relevant
            )
        )

    def test_heading_signature_and_real_paragraph_structure_are_restored(self) -> None:
        self.assertTrue(self.rendered.startswith("## Preface\n\n"))
        self.assertNotIn("#### **Preface**", self.rendered)
        self.assertIn(
            "Stephen Wolfram<br>\nJanuary 15, 2002\n\nThe creation",
            self.rendered,
        )
        self.assertIn("experiences—particularly", self.rendered)
        self.assertIn("what is now in this book.\n\nIn my early years", self.rendered)
        self.assertIn("the form and content of this book", self.rendered)
        self.assertIn("complete this project.\n\nIn developing", self.rendered)
        self.assertIn("mathematics of cellular automata", self.rendered)
        self.assertIn("Norman Packard", self.rendered)
        self.assertIn("decision to focus my work towards", self.rendered)
        self.assertIn("D’Angour, Richard Feynman", self.rendered)
        for false_split in (
            "form\n\nand content",
            "mathematics of\n\ncellular",
            "Norman\n\nPackard",
            "focus\n\nmy work",
            "D'Angour,\n\nRichard",
        ):
            self.assertNotIn(false_split, self.rendered)
        self.assertNotIn("Acknowledgments", self.rendered)

    def test_source_typography_names_and_date_ranges_are_restored(self) -> None:
        self.assertEqual(self.rendered.count("Mathematica"), 11)
        self.assertEqual(self.rendered.count("*Mathematica*"), 11)
        self.assertNotRegex(
            self.rendered, r"\b(?:19|20)\d{2}-(?:19|20)\d{2}\b"
        )
        self.assertEqual(
            len(re.findall(r"\b(?:19|20)\d{2}–(?:19|20)\d{2}\b", self.rendered)),
            37,
        )
        self.assertNotIn("2001– 2002", self.rendered)
        self.assertIn("Tom Wickham-Jones", self.rendered)
        self.assertNotIn("Wickham-Iones", self.rendered)
        self.assertIn("Cvitanovič", self.rendered)
        self.assertNotIn("Cvitanović", self.rendered)
        self.assertIn("Erdős", self.rendered)
        self.assertIn("d’Humières", self.rendered)
        for defect in (
            "history-or",
            "people-especially",
            "institutions-especially",
            "Illinois-have",
            "academia-there",
            "education-in",
            "done-and",
            "far-I",
        ):
            self.assertNotIn(defect, self.rendered)

    def test_divider_asset_and_published_sibling_are_preserved(self) -> None:
        self.assertEqual(self.rendered.count("![](_page_14_Picture_0.jpeg)"), 1)
        image = next(
            row
            for row in self.images
            if row["asset_relative_path"].endswith("_page_14_Picture_0.jpeg")
        )
        self.assertEqual(image["document_id"], "PREFACE")
        self.assertEqual(image["monolith_line"], 164)
        self.assertEqual(
            (build.OUTPUT_ROOT / Path(self.path)).read_text(encoding="utf-8"),
            self.rendered,
        )

    def test_two_pass_document_coverage_is_closed(self) -> None:
        rows = validate.validate_coverage(self.documents)
        preface = next(row for row in rows if row["document_id"] == "PREFACE")
        self.assertEqual((preface["first_pass"], preface["second_pass"]), ("YES", "YES"))
        self.assertEqual(preface["reviewer_type"], "agent")


if __name__ == "__main__":
    unittest.main()
