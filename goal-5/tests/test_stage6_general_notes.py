from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path


GOAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402
import validate  # noqa: E402


EXPECTED_SHA256 = "1a5b294ecc1be93f0ed1f565646eaedaab10775f87ca314e0225c76bad76a10c"
EXPECTED_BYTES = 44_301
EXPECTED_LINES = 191


class GeneralNotesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.document = next(
            row for row in cls.documents if row["id"] == "GENERAL_NOTES"
        )
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
                10623,
                10817,
                1540232,
                1584683,
                195,
                44451,
                "06ee1851338bb2e9475c45acd0c4fba02cb42933209f86076be4bbf5d70ae5c2",
                865,
                874,
                "849",
                "858",
            ),
        )
        segment = self.raw[1540232:1584683]
        self.assertEqual(build.sha256(segment), self.document["raw_segment_sha256"])

        relevant = [
            row for row in self.corrections if row["document_id"] == "GENERAL_NOTES"
        ]
        self.assertGreaterEqual(len(self.corrections), 882)
        self.assertEqual(len(relevant), 21)
        self.assertEqual(
            [row["id"] for row in relevant],
            [f"G5-C-{number:04d}" for number in range(862, 883)],
        )
        for row in relevant:
            with self.subTest(correction=row["id"]):
                self.assertEqual(row["expected_count"], 1)
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                page = re.match(r"pdf:(\d{4})", row["authoritative_location"])
                self.assertIsNotNone(page)
                self.assertTrue(865 <= int(page.group(1)) <= 873)
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
        row = next(item for item in rows if item["document_id"] == "GENERAL_NOTES")
        self.assertEqual(
            (row["first_pass"], row["second_pass"], row["reviewer_type"]),
            ("YES", "YES", "agent"),
        )
        self.assertIn("21 guarded corrections", row["notes"])
        self.assertIn("one mapped reference", row["notes"])
        self.assertIn("closing passes restarted", row["notes"])

    def test_note_structure_styles_and_residuals_are_exact(self) -> None:
        self.assertTrue(self.rendered.startswith("## General Notes\n\n"))
        self.assertEqual(len(re.findall(r"(?m)^■ \*\*", self.rendered)), 32)
        self.assertEqual(
            len(
                re.findall(
                    r"(?m)^■ (?:Iteration|Functional operations|List manipulation|"
                    r"Transformation rules|Numerical functions)$",
                    self.rendered,
                )
            ),
            5,
        )
        self.assertIsNone(re.search(r"(?m)(?<!\n)\n(?=■ \*\*)", self.rendered))
        self.assertIn("■ ***Mathematica*.** I created *Mathematica*", self.rendered)
        self.assertIn("the *Mathematica* programs for generating", self.rendered)
        self.assertIn("the new Mathematica-Sans font", self.rendered)
        self.assertNotIn("*Mathematica*-Sans", self.rendered)
        self.assertNotIn("#### General Notes", self.rendered)
        for residue in (
            "shortterm",
            "honorifies",
            "not vet been addressed",
            "computingwhich",
            "Windows NTwith",
            "Ouotient",
            "Ceilinal",
            "From Digits",
        ):
            with self.subTest(residue=residue):
                self.assertNotIn(residue, self.rendered)

    def test_cover_patterns_figure_association_and_asset_are_exact(self) -> None:
        self.assertEqual(self.rendered.count("□□□■■■■■"), 1)
        self.assertEqual(self.rendered.count("■■■■■□□□"), 1)
        self.assert_order(
            "■ **Cover image.**",
            "□□□■■■■■",
            "■■■■■□□□",
            "The picture on the right shows 3000 steps",
            "![](_page_866_Picture_8.jpeg)",
            "■ **Endpapers.**",
            "■ **Using color.**",
            "■ **Pictures in the book.**",
        )
        mapped = [row for row in self.images if row["document_id"] == "GENERAL_NOTES"]
        self.assertEqual(len(mapped), 1)
        self.assertEqual(
            (
                mapped[0]["ordinal"],
                mapped[0]["asset_sha256"],
                Path(mapped[0]["asset_relative_path"]).name,
            ),
            (
                823,
                "0cd42df471f7440aa4722b5bffff7265263b6c7f19980307677a375ab46fa8eb",
                "_page_866_Picture_8.jpeg",
            ),
        )
        output_asset = build.OUTPUT_ROOT / self.path.parent / "_page_866_Picture_8.jpeg"
        self.assertEqual(build.sha256(output_asset.read_bytes()), mapped[0]["asset_sha256"])
        self.assertEqual(build.jpeg_dimensions(output_asset.read_bytes()), (589, 1436))

    def test_program_inventory_arrows_and_table_are_exact(self) -> None:
        self.assertEqual(self.rendered.count("⟶"), 45)
        self.assertEqual(self.rendered.count("→"), 6)
        self.assertEqual(self.rendered.count("```"), 10)
        self.assertNotIn("```wl", self.rendered)
        exact_programs = (
            "NestList[f, x, 3] ⟶ {x, f[x], f[f[x]], f[f[f[x]]]}",
            "MapIndexed[f, {a, b, c}] ⟶ {f[a, {1}], f[b, {2}], f[c, {3}]}",
            "Table[f[i, j], {i, 2}, {j, 3}] ⟶",
            "ListConvolve[{a, b}, {1, 2, 3, 4, 5}] ⟶",
            "{f[1], g[2], f[2], g[3]} /. f[1] | g[_] → p ⟶ {p, p, f[2], p}",
            "IntegerDigits[13, 2, 6] ⟶ {0, 0, 1, 1, 0, 1}",
            "`Block[{k = 2}, program]`",
        )
        for specimen in exact_programs:
            with self.subTest(specimen=specimen):
                self.assertEqual(self.rendered.count(specimen), 1)

        table = """| π     | Pi       | ∞              | Infinity | ⅇ              | E         | ⅈ                 | I          |
|-------|----------|----------------|----------|----------------|-----------|-------------------|------------|
| x°    | x Degree | $x^y$          | x^y      | $\\sqrt{x}$     | Sqrt[x]   | $x \\rightarrow y$ | x -> y     |
| x ≠ y | x != y   | x ≤ y          | x <= y   | $\\partial_x y$ | D[y, x]   | ¬x                | !x         |
| x ∧ y | x && y   | x ∨ y          | x \\|\\| y | x ⊻ y         | Xor[x, y] | x ⊼ y             | Nand[x, y] |"""
        self.assertEqual(self.rendered.count(table), 1)


if __name__ == "__main__":
    unittest.main()
