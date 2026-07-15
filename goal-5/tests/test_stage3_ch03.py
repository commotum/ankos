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


class ChapterThreeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.document = next(row for row in cls.documents if row["id"] == "CH03")
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

    def test_range_and_first_pass_corrections_are_exact(self) -> None:
        self.assertEqual(
            (
                self.document["raw_start_line"],
                self.document["raw_end_line"],
                self.document["raw_start_byte"],
                self.document["raw_end_byte_exclusive"],
                self.document["authoritative_pdf_start_page"],
                self.document["authoritative_pdf_end_page"],
            ),
            (680, 1367, 119521, 199880, 67, 130),
        )
        relevant = [
            row for row in self.corrections if row["document_id"] == "CH03"
        ]
        self.assertEqual(len(relevant), 61)
        self.assertEqual(
            [row["id"] for row in relevant],
            [f"G5-C-{number:04d}" for number in range(133, 194)],
        )
        self.assertTrue(all(row["expected_count"] == 1 for row in relevant))
        self.assertTrue(
            all(row["verification_status"] == "SOURCE_VERIFIED" for row in relevant)
        )
        self.assertTrue(all(row["reviewer_type"] == "agent" for row in relevant))
        self.assertTrue(
            all(
                67 <= int(str(row["authoritative_location"])[4:8]) <= 129
                for row in relevant
            )
        )

    def test_heading_furniture_and_source_typography_are_restored(self) -> None:
        self.assertTrue(
            self.rendered.startswith(
                "![](_page_66_Picture_0.jpeg)\n\n"
                "## The World of Simple Programs\n\n"
                "### The Search for General Features\n\n"
            )
        )
        headings = (
            "The Search for General Features",
            "More Cellular Automata",
            "Mobile Automata",
            "Turing Machines",
            "Substitution Systems",
            "Sequential Substitution Systems",
            "Tag Systems",
            "Cyclic Tag Systems",
            "Register Machines",
            "Symbolic Systems",
            "Some Conclusions",
            "How the Discoveries in This Chapter Were Made",
        )
        self.assertEqual(self.rendered.count("\n### "), len(headings))
        for heading in headings:
            self.assertEqual(self.rendered.count(f"### {heading}"), 1)
        self.assertNotIn("####", self.rendered)
        self.assertNotIn("### **", self.rendered)
        self.assertNotIn("STEPHEN WOLFRAM | A NEW KIND OF SCIENCE", self.rendered)

        self.assertNotIn('"', self.rendered)
        self.assertNotIn("'", self.rendered)
        self.assertEqual(self.rendered.count("“"), 10)
        self.assertEqual(self.rendered.count("”"), 10)
        self.assertEqual(self.rendered.count("’"), 5)
        self.assertEqual(self.rendered.count("—"), 45)
        for text in (
            "0’s and 1’s",
            "where the A’s correspond to white elements and the B’s to black ones.",
            "single “active cell” that gets updated at each step—and then",
            "systems one studies—and to the procedures",
            "just with one’s eyes",
        ):
            self.assertIn(text, self.rendered)
        self.assertIn("string ABBBABA, where", self.rendered)
        self.assertNotIn("$ABBBABA$", self.rendered)
        self.assertNotIn("*ABBBABA*", self.rendered)
        caption = (
            "corresponding to the element *A*, and the dark squares to the element "
            "*B*. At each step, the rule then specifies that the string which exists "
            "at that step should be scanned from left to right, and the first sequence "
            "*BA* that is found should be replaced by *ABA*."
        )
        self.assertIn(caption, self.rendered)
        self.assertIn("the initial string is *BABA*", self.rendered)
        self.assertIn("adding an *A* inside the string", self.rendered)

    def test_technical_notation_matches_the_source(self) -> None:
        expected = (
            r"$Log[2, 3] \approx 1.59$",
            r"$Log[2, 1 + \sqrt{5}] \approx 1.69$",
            r"after $t$ steps grows roughly like $\sqrt{2t}$.",
            r"$(1 + \sqrt{5})/2 \approx 1.618$",
            r"$\{ABA \rightarrow AAB, A \rightarrow ABA\}$",
            (
                "If one value is $n$, then the next value is $3n/2$ if $n$ is even, "
                "and $(3n + 1)/2$ if $n$ is odd. The initial condition is $n = 1$."
            ),
            r"$e[x\_][y\_] \rightarrow x[x[y]]$",
            r"$x\_$",
            r"$y\_$",
            r"$2^{2^{2^{\cdots}}}$",
        )
        for text in expected:
            self.assertIn(text, self.rendered)
        self.assertEqual(self.rendered.count("$e[e[e][e]][e][e]$"), 2)
        self.assertNotIn(r"\vdots", self.rendered)
        self.assertNotIn(r"2^{2^{2^{-}}}", self.rendered)
        self.assertNotIn("formula  $", self.rendered)
        self.assertNotIn("$ .", self.rendered)

    def test_page_turns_and_plate_sequences_do_not_split_prose(self) -> None:
        joined_fragments = (
            "And in a sense my approach is to work like a naturalist",
            "Thus, for example, in rules 0 and 128",
            "more complicated behavior. But in fact the behavior",
            "Cases (c) through (f) are similar, except that",
            "two possible elements—then it seems",
            "the first register again alternates between 0 and 1",
            "compressed to include only those steps at which",
            "what implies that there are general principles",
            "fundamentally imprecise. For when one deals",
            "And if it turns out that there is behavior",
            "reduce their number as much as possible",
        )
        for text in joined_fragments:
            self.assertIn(text, self.rendered)
        false_splits = (
            "sense my\n\napproach",
            "for example, in\n\nrules 0",
            "more complicated behavior.\n\nBut in fact",
            "are similar,\n\nexcept that",
            "possible elements—\n\nthen it seems",
            "register again\n\nalternates",
            "include only\n\nthose steps",
            "implies that\n\nthere are general",
            "imprecise.\n\nFor when",
            "if it turns\n\nout that",
            "number as\n\nmuch as possible",
        )
        for text in false_splits:
            self.assertNotIn(text, self.rendered)

        self.assert_order(
            "And in a sense my approach is to work like a naturalist",
            "![](_page_67_Picture_1.jpeg)",
            "Four basic examples from the previous chapter",
            "I start by considering more general cellular automata",
        )
        self.assert_order(
            "Thus, for example, in rules 0 and 128",
            "![](_page_69_Rules_100_139.jpeg)",
            "Evolution of cellular automata with a sequence of different possible rules",
            "![](_page_70_Picture_2.jpeg)",
            "![](_page_71_Picture_2.jpeg)",
            "<sup>◀</sup> The behavior of all 256 possible cellular automata",
            "But among the rules shown on the last few pages",
        )
        self.assert_order(
            "more complicated behavior. But in fact the behavior",
            "![](_page_76_Figure_2.jpeg)",
            "A sequence of totalistic cellular automata with three possible colors",
            "And indeed, this is a first indication",
        )
        self.assert_order(
            "Cases (c) through (f) are similar, except that",
            "![](_page_87_Figure_2.jpeg)",
            "Examples of mobile automata with various rules.",
            "But with a total of 218 out of the 65,536 possible rules",
        )
        self.assert_order(
            "two possible elements—then it seems",
            "![](_page_105_Picture_2.jpeg)",
            "![](_page_105_Figure_4.jpeg)",
            "A sequential substitution system whose rule involves two possible replacements.",
            "And from this one might be led to conclude",
        )
        self.assert_order(
            "what implies that there are general principles",
            "![](_page_122_Figure_2.jpeg)",
            "Examples of cellular automata with rules of varying complexity.",
            "And it is this that means",
        )

    def test_every_compound_figure_places_its_shared_caption_last(self) -> None:
        groups = (
            (
                "![](_page_88_Picture_5.jpeg)",
                "![](_page_88_Picture_6.jpeg)",
                "![](_page_88_Picture_8.jpeg)",
                "A mobile automaton with slightly more complicated rules",
            ),
            (
                "![](_page_89_Picture_3.jpeg)",
                "![](_page_89_Picture_5.jpeg)",
                "![](_page_89_Picture_6.jpeg)",
                "A mobile automaton that yields a pattern with seemingly random features.",
            ),
            (
                "![](_page_91_Figure_6.jpeg)",
                "![](_page_91_Figure_8.jpeg)",
                "A generalized mobile automaton in which any number of cells can be active",
            ),
            (
                "![](_page_101_Picture_4.jpeg)",
                "![](_page_101_Picture_5.jpeg)",
                "Two views of a substitution system whose rules allow both creation and destruction",
            ),
            (
                "![](_page_102_Figure_2.jpeg)",
                "![](_page_102_Figure_4.jpeg)",
                "Examples of substitution systems that have three and four possible colors",
            ),
            (
                "![](_page_106_Figure_2.jpeg)",
                "![](_page_106_Figure_4.jpeg)",
                "Examples of sequential substitution systems whose rules involve three possible replacements.",
            ),
            (
                "![](_page_110_Picture_4.jpeg)",
                "![](_page_110_Picture_5.jpeg)",
                "![](_page_110_Picture_7.jpeg)",
                "An example of a cyclic tag system.",
            ),
        )
        for group in groups:
            with self.subTest(group=group[0]):
                self.assert_order(*group)

    def test_source_added_and_repaired_assets_are_pinned(self) -> None:
        chapter_images = [row for row in self.images if row["document_id"] == "CH03"]
        self.assertEqual(len(chapter_images), 86)
        self.assertEqual(
            [row["ordinal"] for row in chapter_images], list(range(24, 110))
        )
        chapter_added = [
            row for row in self.added_assets if row["document_id"] == "CH03"
        ]
        self.assertEqual(len(chapter_added), 1)
        added = chapter_added[0]
        self.assertEqual(
            (
                added["id"],
                added["asset_sha256"],
                added["width_px"],
                added["height_px"],
            ),
            (
                "G5-A-0004",
                "bd3e7c463e043e2bd5d578d48bbbaa9739b70a0da6af99d45469b531a3528abf",
                930,
                1275,
            ),
        )
        added_source = build.REPO_ROOT / Path(added["asset_relative_path"])
        added_output = build.OUTPUT_ROOT / Path(self.path).parent / added_source.name
        self.assertEqual(added_output.read_bytes(), added_source.read_bytes())
        self.assertEqual(build.jpeg_dimensions(added_source.read_bytes()), (930, 1275))

        expected_repairs = {
            53: (
                "4026c3f35504a7b16700a4a767b255896f1c16700991a10c22352d5e41a54c74",
                (411, 491),
            ),
            63: (
                "a13bfef810fd5987564b8ff4a7c5573201c3d29ab27e0829dcf820665a8e70b7",
                (1179, 1310),
            ),
            103: (
                "ac463215e59a02711f142e56e421a72d7f3c3c764ee04451beea6bea22119b4e",
                (1232, 579),
            ),
        }
        repaired_rows = [
            row for row in chapter_images if "repaired_asset_relative_path" in row
        ]
        self.assertEqual({row["ordinal"] for row in repaired_rows}, set(expected_repairs))
        for row in repaired_rows:
            digest, dimensions = expected_repairs[row["ordinal"]]
            with self.subTest(ordinal=row["ordinal"]):
                legacy = build.LEGACY_ROOT / Path(row["asset_relative_path"])
                repaired = build.REPO_ROOT / Path(row["repaired_asset_relative_path"])
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

        references = re.findall(r"!\[\]\(([^)]+\.jpeg)\)", self.rendered)
        expected_names = {
            Path(row["asset_relative_path"]).name for row in chapter_images
        } | {added_source.name}
        self.assertEqual(len(references), 87)
        self.assertEqual(len(set(references)), 87)
        self.assertEqual(set(references), expected_names)
        self.assertIn(
            "![](_page_117_Figure_5.jpeg)\n\n"
            "A sequence of steps in the evolution of a simple symbolic system. "
            "At each step each boxed region is transformed according to the rule shown. "
            "This transformation corresponds to applying the basic *Mathematica* "
            "operation *expression /. rule*.",
            self.rendered,
        )

        changed_hash = copy.deepcopy(self.images)
        target = next(row for row in changed_hash if row["ordinal"] == 103)
        target["repaired_asset_sha256"] = "0" * 64
        with self.assertRaises(build.BuildError):
            build.validate_images(self.raw, self.documents, changed_hash)
        missing_reason = copy.deepcopy(self.added_assets)
        target_added = next(row for row in missing_reason if row["id"] == "G5-A-0004")
        target_added.pop("reason")
        with self.assertRaises(build.BuildError):
            build.validate_added_assets(self.documents, self.images, missing_reason)

    def test_first_pass_coverage_is_recorded_and_second_pass_remains_open(self) -> None:
        rows = validate.validate_coverage(self.documents)
        chapter = next(row for row in rows if row["document_id"] == "CH03")
        self.assertEqual(
            (chapter["first_pass"], chapter["second_pass"]), ("YES", "NO")
        )
        self.assertEqual(chapter["reviewer_type"], "agent")


if __name__ == "__main__":
    unittest.main()
