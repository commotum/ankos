from __future__ import annotations

import sys
import unittest
from pathlib import Path


GOAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402
import validate  # noqa: E402


class PublicationAndContentsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.document = next(
            row for row in cls.documents if row["id"] == "PUBLICATION_AND_CONTENTS"
        )
        cls.path = build.safe_relative_path(cls.document["output_path"], suffix=".md")
        cls.raw_text = cls.raw[
            cls.document["raw_start_byte"] : cls.document["raw_end_byte_exclusive"]
        ].decode("utf-8")
        cls.rendered = build.document_bytes(
            cls.raw, cls.documents, cls.corrections
        )[cls.path].decode("utf-8")

    def test_guarded_source_corrections_cover_real_publication_defects(self) -> None:
        relevant = [
            row
            for row in self.corrections
            if row["document_id"] == "PUBLICATION_AND_CONTENTS"
        ]
        self.assertEqual(len(relevant), 20)
        self.assertEqual(
            [row["id"] for row in relevant],
            [f"G5-C-{number:04d}" for number in range(1, 21)],
        )
        self.assertTrue(
            all(row["verification_status"] == "SOURCE_VERIFIED" for row in relevant)
        )
        self.assertTrue(
            all(str(row["authoritative_location"]).startswith("pdf:000") for row in relevant)
        )

        self.assertIn("ANEW KIND OF SCIENCE", self.raw_text)
        self.assertNotIn("ANEW KIND OF SCIENCE", self.rendered)
        self.assertEqual(
            self.rendered.count("# STEPHEN WOLFRAM A NEW KIND OF SCIENCE"), 3
        )
        self.assertIn(
            "1. Cellular automata. 2. Computational complexity. I. Title.",
            self.rendered,
        )
        self.assertNotIn("I. Cellular automata.", self.rendered)
        self.assertIn("QA267.5.C45 W67 2001", self.rendered)
        self.assertIn(
            "the holder of their copyright. Stephen Wolfram, LLC is the owner",
            self.rendered,
        )
        self.assertEqual(self.rendered.count("*Mathematica*"), 5)
        self.assertIn("“A New Kind of Science”", self.rendered)
        self.assertIn("*Mathematica*<sup>®</sup>", self.rendered)
        self.assertIn("Printed in Canada. ♾ Acid-free paper.", self.rendered)

    def test_source_structure_is_not_flattened_or_invented(self) -> None:
        self.assertIn(
            "Visit **www.wolframscience.com** for the latest information", self.rendered
        )
        self.assertNotIn("#### Visit www.wolframscience.com", self.rendered)
        for label in ("web", "email", "phone", "fax", "mail", "international"):
            self.assertIn(f"*{label}:*", self.rendered)
        self.assertIn("## Contents", self.rendered)
        self.assertNotIn("|----|", self.rendered)
        self.assertIn("<tr><td></td><td>Preface</td><td>ix</td></tr>", self.rendered)
        self.assertEqual(self.rendered.count('<th scope="row">'), 12)
        self.assertNotIn("<th>Preface", self.rendered)

    def test_published_sibling_is_the_exact_guarded_render(self) -> None:
        self.assertEqual(
            (build.OUTPUT_ROOT / Path(self.path)).read_text(encoding="utf-8"),
            self.rendered,
        )

    def test_two_pass_document_coverage_is_closed(self) -> None:
        rows = validate.validate_coverage(self.documents)
        publication = rows[0]
        self.assertEqual(publication["document_id"], "PUBLICATION_AND_CONTENTS")
        self.assertEqual(
            (publication["first_pass"], publication["second_pass"]),
            ("YES", "YES"),
        )
        self.assertEqual(publication["reviewer_type"], "agent")


if __name__ == "__main__":
    unittest.main()
