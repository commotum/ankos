from __future__ import annotations

import copy
import re
import sys
import unittest
from pathlib import Path


GOAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402


class ChapterSixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.document = next(row for row in cls.documents if row["id"] == "CH06")
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

    def test_range_guards_and_final_document_hash_are_exact(self) -> None:
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
                2700,
                3419,
                418051,
                488397,
                720,
                70346,
                "ea43e3fa83ef57beccd9954a61272579c4efc2d3f7c80f561b418745450460da",
                239,
                312,
                "223",
                "296",
            ),
        )
        relevant = [row for row in self.corrections if row["document_id"] == "CH06"]
        self.assertEqual(len(relevant), 44)
        self.assertEqual(
            [row["id"] for row in relevant],
            [f"G5-C-{number:04d}" for number in range(356, 400)],
        )
        self.assertTrue(all(row["expected_count"] == 1 for row in relevant))
        self.assertTrue(
            all(row["verification_status"] == "SOURCE_VERIFIED" for row in relevant)
        )
        self.assertTrue(all(row["reviewer_type"] == "agent" for row in relevant))
        self.assertTrue(
            all(
                239
                <= int(re.match(r"pdf:(\d{4})", row["authoritative_location"])[1])
                <= 312
                for row in relevant
            )
        )
        self.assertEqual(len(self.rendered_bytes), 71494)
        self.assertEqual(
            build.sha256(self.rendered_bytes),
            "0eb4ebc5400c3e3ed39fb2dd8fd9c38a2977eaef1ffefb528fd4c2708a42dca5",
        )

    def test_opener_heading_hierarchy_and_directional_markers(self) -> None:
        self.assertTrue(
            self.rendered.startswith(
                "![](_page_238_Chapter_Opener.jpeg)\n\n"
                "## Starting from Randomness\n\n"
                "### The Emergence of Order\n\n"
            )
        )
        headings = (
            "The Emergence of Order",
            "Four Classes of Behavior",
            "Sensitivity to Initial Conditions",
            "Systems of Limited Size and Class 2 Behavior",
            "Randomness in Class 3 Systems",
            "Special Initial Conditions",
            "The Notion of Attractors",
            "Structures in Class 4 Systems",
        )
        self.assertEqual(self.rendered.count("\n### "), len(headings))
        for heading in headings:
            self.assertEqual(self.rendered.count(f"### {heading}"), 1)
        self.assertNotIn("####", self.rendered)
        self.assertNotIn("### **", self.rendered)
        self.assertNotRegex(self.rendered, r"(?m)^## 6$")
        self.assertNotIn("STEPHEN WOLFRAM | A NEW KIND OF SCIENCE", self.rendered)
        self.assertEqual(self.rendered.count("<sup>▶</sup>"), 2)
        self.assertIn("structures that propagates across the system. <sup>▶</sup>", self.rendered)

    def test_source_order_and_interrupted_plate_serialization(self) -> None:
        self.assert_order(
            "![](_page_242_Figure_2.jpeg)",
            "![](_page_242_Rule_30.jpeg)",
            "![](_page_242_Picture_4.jpeg)",
            "![](_page_242_Picture_5.jpeg)",
            "Other examples of cellular automata that never settle down",
        )
        self.assert_order(
            "But at the transitions it turns out that class 4 behavior is typically seen",
            "![](_page_258_Figure_1.jpeg)",
            "Examples of the evolution of continuous cellular automata",
            "![](_page_259_Picture_2.jpeg)",
            "*0.398*",
            "![](_page_259_Picture_4.jpeg)",
            "*0.4*",
            "![](_page_259_Picture_6.jpeg)",
            "*{0.5, 1.13}*",
            "Examples of continuous cellular automata that exhibit class 4 behavior.",
        )
        self.assert_order(
            "And in any such case, the pattern must repeat itself with a period of at most $2^n$ steps",
            "![](_page_274_Figure_2.jpeg)",
            "The behavior of cellular automata with a limited number of cells.",
            "![](_page_275_Figure_1.jpeg)",
            "Repetition periods for various cellular automata as a function of size.",
        )
        self.assert_order(
            "whatever pattern is produced must have exactly the same structure",
            "![](_page_285_Figure_7.jpeg)",
            "![](_page_285_Figure_8.jpeg)",
            "![](_page_285_Picture_9.jpeg)",
            "A demonstration of the fact that in rule 90 blocks of cells can behave",
        )
        self.assert_order(
            "corresponding to sequences of any number of white cells.",
            "![](_page_292_Figure_2.jpeg)",
            "Networks representing possible sequences of black and white cells that "
            "can occur at successive steps in the evolution of the two cellular "
            "automata shown on the left.",
        )

    def test_caption_only_raster_is_hidden_and_transcribed_once(self) -> None:
        comment = (
            "<!-- Editorial source-accounting reference: the legacy asset below "
            "rasterizes the author caption transcribed as live text after this figure group.\n"
            "![](_page_264_Picture_3.jpeg)\n"
            "-->"
        )
        caption = (
            "The behavior of a class 4 two-dimensional cellular automaton often "
            "known in recreational computing as the Game of Life. Localized "
            "structures that move (so-called gliders) show up as streaks in the "
            "pictures given here."
        )
        self.assertEqual(self.rendered.count(comment), 1)
        self.assertEqual(self.rendered.count(caption), 1)
        self.assert_order(
            "![](_page_264_Picture_2.jpeg)",
            comment,
            "![](_page_264_Picture_4.jpeg)",
            "![](_page_264_Picture_5.jpeg)",
            "![](_page_264_Picture_6.jpeg)",
            caption,
            "### Sensitivity to Initial Conditions",
        )
        visible_markdown = self.rendered.replace(comment, "")
        self.assertNotIn("![](_page_264_Picture_3.jpeg)", visible_markdown)
        self.assertIn("outer totalistic 9-neighbor code 224", self.rendered)

    def test_technical_math_glyphs_and_residual_ocr_are_exact(self) -> None:
        expected = (
            "*code 1815*",
            "*code 2007*",
            "*code 2043*",
            "*1 cell changed*",
            "position $Mod[2^t, n]$ in a size $n$ system",
            "for odd $n$ this period is equal to $MultiplicativeOrder[2, n]$.",
            "close to $2^n$ (for $n = 29$",
            "blocks $\\blacksquare\\blacksquare\\Box\\Box$ and "
            "$\\blacksquare\\blacksquare\\blacksquare\\Box$.",
            "$\\blacksquare \\to \\blacksquare \\Box \\blacksquare$, "
            "$\\Box \\to \\Box \\Box \\blacksquare$",
            "after $t$ steps must have at least $t$ white cells",
            "about $t^2$ nodes after $t$ steps",
            "length 12 block "
            "$\\Box\\blacksquare\\blacksquare\\blacksquare\\Box"
            "\\blacksquare\\blacksquare\\Box\\blacksquare\\blacksquare"
            "\\blacksquare\\Box$.",
            "*2 colors, next-nearest neighbors, code 20*",
            "*3 colors, nearest neighbors, code 357*",
            "*3 colors, nearest neighbors, code 1329*",
            "structures (l) and (i) from page 292",
        )
        for text in expected:
            with self.subTest(text=text):
                self.assertEqual(self.rendered.count(text), 1)
        residues = (
            "\n238\n",
            "nie 184",
            "blocks and and Rule",
            "length 12 block —————",
            "structures (I) and (i)",
            "\ninitial condition number 54,889\n",
            "  $",
            "$  ",
            "\t",
            "\ufffd",
        )
        for residue in residues:
            with self.subTest(residue=residue):
                self.assertNotIn(residue, self.rendered)
        self.assertEqual(self.rendered.count("$"), 58)

    def test_added_figures_are_placed_with_their_governing_captions(self) -> None:
        self.assert_order(
            "![](_page_281_Picture_8.jpeg)",
            "![](_page_281_Rule_30_Strip.jpeg)",
            "Examples of special initial conditions that make the rule 30 cellular automaton",
            "![](_page_284_Figure_6.jpeg)",
            "![](_page_284_Rule_126_Rule_90_Map.jpeg)",
            "Two examples of the fact that with special initial conditions rule 126 behaves exactly like rule 90.",
            "![](_page_286_Picture_9.jpeg)",
            "![](_page_286_Rule_184_Middle.jpeg)",
            "![](_page_286_Picture_11.jpeg)",
            "A rule that is not additive, but in which blocks of cells can again behave just like individual cells.",
            "![](_page_287_Picture_3.jpeg)",
            "![](_page_287_Rule_184_Strip.jpeg)",
            "The pattern produced by rule 184 (shown at left) evolving from a nested initial condition.",
        )

    def test_repaired_and_added_assets_are_pinned_and_reference_order_is_exact(self) -> None:
        chapter_images = [row for row in self.images if row["document_id"] == "CH06"]
        self.assertEqual(len(chapter_images), 99)
        self.assertEqual([row["ordinal"] for row in chapter_images], list(range(246, 345)))
        expected_repairs = {
            253: ("5d0d2305aeb15a390515c15df469a99477258031f6493e6bd9c2d9de5e5b303c", (850, 990)),
            272: ("39c0faeec91a67a957966561dfd5e4e8b28b9f4ac72bff23ddc4787925ed3f55", (410, 300)),
            283: ("794ac066a51509a37d4799acc739a6b5f4c59e751ac41c742240e6c89036cfe2", (650, 690)),
            284: ("6155bdaa297203af55f18c2ff66ae9a99e81f1abdc75713a5f03461f7cb83002", (650, 690)),
            285: ("36264bbd6814952b8bff6c4c80a7e1d19da57855e65557ccea72b10edebcd075", (650, 690)),
            317: ("a66b8790f0b4aa10ec56a609f35c5a2fbb673710f9cd4f3714927c1645ada5a1", (420, 325)),
            337: ("b01c795895a35750b33973f7a8014dc31aa01f594de8f0e7a66e5da3ac95ec55", (900, 1720)),
        }
        repaired = [row for row in chapter_images if "repaired_asset_relative_path" in row]
        self.assertEqual([row["ordinal"] for row in repaired], list(expected_repairs))
        for row in repaired:
            expected_hash, expected_dimensions = expected_repairs[row["ordinal"]]
            with self.subTest(repaired=row["ordinal"]):
                source = build.REPO_ROOT / Path(row["repaired_asset_relative_path"])
                output = build.OUTPUT_ROOT / Path(self.path).parent / source.name
                payload = source.read_bytes()
                self.assertEqual(build.sha256(payload), expected_hash)
                self.assertEqual(row["repaired_asset_sha256"], expected_hash)
                self.assertEqual(build.jpeg_dimensions(payload), expected_dimensions)
                self.assertEqual(
                    (row["repaired_width_px"], row["repaired_height_px"]),
                    expected_dimensions,
                )
                self.assertEqual(output.read_bytes(), payload)

        chapter_added = [row for row in self.added_assets if row["document_id"] == "CH06"]
        expected_added = {
            "G5-A-0012": ("1cd40b08dfadc64428ff0aaccfc065c561f72e143bc874f89ab42daa3ff6149f", (430, 565)),
            "G5-A-0013": ("0e3bcea83d4e0fcc92f08529784776f91b4c5edb80bf9795fa3828a7c0060a0d", (850, 980)),
            "G5-A-0014": ("1a8e0497be80cb24c7d741bc965c2198b467f32cb514929284732eb7df410e49", (570, 105)),
            "G5-A-0015": ("b103530d0fae6c6aa67e61b9072cc2699b1db22924c77a72bd09bdccbf427360", (420, 95)),
            "G5-A-0016": ("3738b7036adfecc29ae01bcc4f9c5472322cc1e486fccc3b8432c9291837b4ef", (420, 325)),
            "G5-A-0017": ("9b577aeb6e59caa105bf424b03ee89ffabd79c059d8a7614d39dea54ad8396cf", (630, 90)),
        }
        self.assertEqual([row["id"] for row in chapter_added], list(expected_added))
        added_names: dict[str, str] = {}
        for row in chapter_added:
            expected_hash, expected_dimensions = expected_added[row["id"]]
            with self.subTest(added=row["id"]):
                source = build.REPO_ROOT / Path(row["asset_relative_path"])
                output = build.OUTPUT_ROOT / Path(self.path).parent / source.name
                payload = source.read_bytes()
                added_names[row["id"]] = source.name
                self.assertEqual(build.sha256(payload), expected_hash)
                self.assertEqual(row["asset_sha256"], expected_hash)
                self.assertEqual(build.jpeg_dimensions(payload), expected_dimensions)
                self.assertEqual((row["width_px"], row["height_px"]), expected_dimensions)
                self.assertEqual(output.read_bytes(), payload)

        mapped_names = {row["ordinal"]: Path(row["asset_relative_path"]).name for row in chapter_images}
        expected_references = (
            [added_names["G5-A-0012"]]
            + [mapped_names[number] for number in range(246, 253)]
            + [added_names["G5-A-0013"]]
            + [mapped_names[number] for number in range(253, 307)]
            + [added_names["G5-A-0014"]]
            + [mapped_names[number] for number in range(307, 311)]
            + [added_names["G5-A-0015"]]
            + [mapped_names[number] for number in range(311, 318)]
            + [added_names["G5-A-0016"]]
            + [mapped_names[number] for number in range(318, 320)]
            + [added_names["G5-A-0017"]]
            + [mapped_names[number] for number in range(320, 345)]
        )
        references = re.findall(r"!\[\]\(([^)]+\.jpeg)\)", self.rendered)
        self.assertEqual(len(references), 105)
        self.assertEqual(len(set(references)), 105)
        self.assertEqual(references, expected_references)

        changed_images = copy.deepcopy(self.images)
        next(row for row in changed_images if row["ordinal"] == 317)[
            "repaired_asset_sha256"
        ] = "0" * 64
        with self.assertRaises(build.BuildError):
            build.validate_images(self.raw, self.documents, changed_images)
        changed_added = copy.deepcopy(self.added_assets)
        next(row for row in changed_added if row["id"] == "G5-A-0016").pop("reason")
        with self.assertRaises(build.BuildError):
            build.validate_added_assets(self.documents, self.images, changed_added)


if __name__ == "__main__":
    unittest.main()
