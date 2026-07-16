from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path


GOAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402
import validate  # noqa: E402


EXPECTED_SHA256 = "8d1cf6cbfdd1de864838781d8c16610630890c0269d3c1b510fb4eea479b5b40"
EXPECTED_BYTES = 29_769
EXPECTED_LINES = 75


class NotesForChapter1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.document = next(row for row in cls.documents if row["id"] == "N01")
        cls.path = build.safe_relative_path(cls.document["output_path"], suffix=".md")
        cls.rendered_bytes = build.document_bytes(
            cls.raw, cls.documents, cls.corrections
        )[cls.path]
        cls.rendered = cls.rendered_bytes.decode("utf-8")

    def test_source_range_corrections_and_render_are_exact(self) -> None:
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
                10818,
                10894,
                1584683,
                1614202,
                77,
                29519,
                "0b6c35adb40cc66f790a7593e4faec2a0837192097a86bb1b28742ef7ab021ad",
                875,
                880,
                "859",
                "864",
            ),
        )
        segment = self.raw[1584683:1614202]
        self.assertEqual(build.sha256(segment), self.document["raw_segment_sha256"])

        relevant = [row for row in self.corrections if row["document_id"] == "N01"]
        self.assertGreaterEqual(len(self.corrections), 905)
        self.assertEqual(len(relevant), 23)
        self.assertEqual(
            [row["id"] for row in relevant],
            [f"G5-C-{number:04d}" for number in range(883, 906)],
        )
        for row in relevant:
            with self.subTest(correction=row["id"]):
                self.assertEqual(row["expected_count"], 1)
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                pages = [int(value) for value in re.findall(r"pdf:(\d{4})", row["authoritative_location"])]
                self.assertTrue(pages)
                self.assertTrue(all(875 <= page <= 880 for page in pages))
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

    def test_two_pass_coverage_is_closed(self) -> None:
        rows = validate.validate_coverage(self.documents)
        row = next(item for item in rows if item["document_id"] == "N01")
        self.assertEqual(
            (row["first_pass"], row["second_pass"], row["reviewer_type"]),
            ("YES", "YES", "agent"),
        )
        self.assertIn("23 guarded corrections", row["notes"])
        self.assertIn("zero mapped images", row["notes"])
        self.assertIn("closing passes restarted", row["notes"])

    def test_heading_note_and_timeline_structure_is_exact(self) -> None:
        self.assertTrue(
            self.rendered.startswith(
                "## The Foundations for a New Kind of Science\n\n"
                "### An Outline of Basic Ideas\n\n"
            )
        )
        self.assertEqual(
            re.findall(r"(?m)^### (.+)$", self.rendered),
            [
                "An Outline of Basic Ideas",
                "Relations to Other Areas",
                "The Personal Story of the Science in This Book",
            ],
        )
        labels = re.findall(r"(?m)^■ \*\*(.+?)\*\*", self.rendered)
        self.assertEqual(
            labels,
            [
                "Mathematics in science.",
                "Definition of mathematics.",
                "Reasons for mathematics in science.",
                "History of programs and nature.",
                "Extensions of mathematics.",
                "The role of logic.",
                "Complexity and theology.",
                "Artifacts and natural systems.",
                "Complexity and science.",
                "Page 7 · Mathematics.",
                "Page 8 · Physics.",
                "Page 8 · Biology.",
                "Page 9 · Social and related sciences.",
                "Page 10 · Computer science.",
                "Page 10 · Philosophy.",
                "Page 11 · Technology.",
                "Scope of existing sciences.",
                "Page 17 · Statistical physics cover.",
                "Page 17 · My 1973 computer experiments.",
                "Page 19 · Computer printouts.",
                "Timeline.",
                "Detailed history.",
            ],
        )
        self.assertEqual(
            re.findall(r"(?m)^▪ (.+)$", self.rendered),
            [
                "1974–1980: particle physics and cosmology",
                "1979–1981: developing SMP computer algebra system",
                "1981–1986: cellular automata etc.",
                "1986–1991: intensive *Mathematica* development",
                "1991–2001: writing this book",
            ],
        )
        self.assertNotRegex(self.rendered, r"(?m)^- ")
        self.assertNotIn("####", self.rendered)
        self.assertNotIn("■1979", self.rendered)

    def test_technical_punctuation_emphasis_and_source_forms_are_exact(self) -> None:
        self.assertEqual(self.rendered.count("–"), 21)
        self.assertEqual(self.rendered.count("—"), 32)
        self.assertEqual(
            re.findall(r"(?<!\*)\*([^*\n]+)\*(?!\*)", self.rendered),
            [
                "Mathematical Principles of Natural Philosophy",
                "Principia",
                "Mathematica",
                "The Wisdom of God Manifested in the Works of the Creation",
                "Origin of Species",
                "Mathematica",
                "Mathematica",
                "Mathematica",
                "Mathematica",
            ],
        )
        self.assertNotIn('"', self.rendered)
        self.assertIn("Newton’s", self.rendered)
        self.assertIn("Euclid’s", self.rendered)
        self.assertIn("Ray’s", self.rendered)
        self.assertIn("Darwin’s", self.rendered)
        self.assertIn("I actually consider in this book.", self.rendered)
        self.assertIn("protein folding and structure on pages 1003 and 1184.", self.rendered)
        for exact_source_form in (
            "(I had avoided this name to prevent confusion with the largely unrelated field of computational complexity theory).",
            "a random sequence of digits were used",
            "There have however been occasional discussions",
            "the much quoted argument",
            "issues of modelling",
            "cellular automata etc.",
        ):
            with self.subTest(source_form=exact_source_form):
                self.assertIn(exact_source_form, self.rendered)

        for residue in (
            "mathematicalexamples",
            "selection-but",
            "logic-an",
            "popular-with",
            "organizations-especially",
            "hierarchy-and",
            "rules-though",
            "accounts-and",
            "scientistswith",
            "retreat-though",
            "middlesquare",
            "times-after",
        ):
            with self.subTest(residue=residue):
                self.assertNotIn(residue, self.rendered)

    def test_document_is_text_only_and_has_no_image_ownership(self) -> None:
        self.assertNotIn("![](", self.rendered)
        self.assertNotIn("```", self.rendered)
        self.assertNotRegex(self.rendered, r"(?m)^\|")
        mapped = [row for row in self.images if row["document_id"] == "N01"]
        self.assertEqual(mapped, [])


if __name__ == "__main__":
    unittest.main()
