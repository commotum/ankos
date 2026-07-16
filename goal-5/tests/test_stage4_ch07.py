from __future__ import annotations

import copy
import re
import sys
import unittest
from pathlib import Path


GOAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402


class ChapterSevenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.document = next(row for row in cls.documents if row["id"] == "CH07")
        cls.path = build.safe_relative_path(cls.document["output_path"], suffix=".md")
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

    def test_range_guards_correction_packet_and_final_hash_are_exact(self) -> None:
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
                3420,
                4335,
                488397,
                601461,
                916,
                113064,
                "4ef8b442496e6851807f595fee914abcda7d095d67575edd4f7781140e443627",
                313,
                378,
                "297",
                "362",
            ),
        )
        relevant = [row for row in self.corrections if row["document_id"] == "CH07"]
        self.assertEqual(len(relevant), 53)
        self.assertEqual(
            [row["id"] for row in relevant],
            [f"G5-C-{number:04d}" for number in range(400, 453)],
        )
        self.assertEqual(
            [row["expected_count"] for row in relevant if row["expected_count"] != 1],
            [3, 3, 3],
        )
        self.assertTrue(
            all(row["verification_status"] == "SOURCE_VERIFIED" for row in relevant)
        )
        self.assertTrue(all(row["reviewer_type"] == "agent" for row in relevant))
        self.assertTrue(
            all(
                313
                <= int(re.match(r"pdf:(\d{4})", row["authoritative_location"])[1])
                <= 378
                for row in relevant
            )
        )
        self.assertEqual(len(self.rendered_bytes), 113785)
        self.assertEqual(
            build.sha256(self.rendered_bytes),
            "e052f275ea7519f2e8c270f1dd68eac01d123aa3b73355eff5803f02708e542d",
        )

    def test_opener_heading_hierarchy_and_source_furniture_are_exact(self) -> None:
        self.assertTrue(
            self.rendered.startswith(
                "![](_page_312_Picture_0.jpeg)\n\n"
                "## Mechanisms in Programs and Nature\n\n"
                "### Universality of Behavior\n\n"
            )
        )
        headings = (
            "Universality of Behavior",
            "Three Mechanisms for Randomness",
            "Randomness from the Environment",
            "Chaos Theory and Randomness from Initial Conditions",
            "The Intrinsic Generation of Randomness",
            "The Phenomenon of Continuity",
            "Origins of Discreteness",
            "The Problem of Satisfying Constraints",
            "Origins of Simple Behavior",
        )
        self.assertEqual(self.rendered.count("\n### "), len(headings))
        for heading in headings:
            self.assertEqual(self.rendered.count(f"### {heading}"), 1)
        self.assertNotIn("####", self.rendered)
        self.assertNotIn("### **", self.rendered)
        self.assertNotIn("\nSTEPHEN WOLFRAM\n", self.rendered)
        self.assertNotIn("A NEW KIND OF SCIENCE", self.rendered)
        self.assertIn("intrinsic randomness generations can be widespread", self.rendered)
        self.assertIn("Homogenous growth from a single point", self.rendered)

    def test_interrupted_prose_and_shared_figure_groups_are_serialized(self) -> None:
        self.assert_order(
            "cannot diverge any further. And then in the first case",
            "![](_page_322_Picture_2.jpeg)",
            "A kneading process similar to ones used to make noodles or taffy",
            "![](_page_322_Picture_4.jpeg)",
            "Two examples of what can happen when the kneading process above",
        )
        self.assert_order(
            "before being affected by microscopic perturbations in the mirrors",
            "![](_page_326_Picture_2.jpeg)",
            "![](_page_326_Picture_3.jpeg)",
            "An arrangement of mirrors set up to exhibit randomness",
        )
        self.assert_order(
            "randomness in this initial digit sequence.",
            "![](_page_327_Picture_6.jpeg)",
            "Paths followed by four idealized balls dropped from initial positions",
        )
        self.assert_order(
            "simple laws of nature could exist.",
            "![](_page_329_Figure_1.jpeg)",
            "differing by $10^{-8}$—are shown",
        )
        self.assert_order(
            "![](_page_340_Figure_2.jpeg)",
            "![](_page_340_Figure_4.jpeg)",
            "The effects of various levels of external randomness",
        )
        self.assert_order(
            "the overall shapes of the clusters produced remain very much the same.",
            "![](_page_347_Picture_5.jpeg)",
            "![](_page_347_Picture_7.jpeg)",
            "![](_page_347_Figure_8.jpeg)",
            "![](_page_347_Figure_9.jpeg)",
            "Patterns produced by generalized aggregation models",
        )

    def test_invariant_state_nesting_and_live_captions_are_complete(self) -> None:
        full_caption = (
            "Behavior of a two-dimensional cellular automaton starting from a "
            "random initial condition. At each step, each cell looks at the total "
            "number of black cells in the 9-cell neighborhood"
        )
        substitution_caption = (
            "Nesting in one- and two-dimensional neighbor-independent substitution "
            "systems in which each element breaks into a block of smaller elements "
            "at each step."
        )
        self.assertEqual(self.rendered.count(full_caption), 1)
        self.assertEqual(self.rendered.count(substitution_caption), 1)
        self.assert_order(
            "the constraint associated with the invariant state.",
            "![](_page_363_Picture_7.jpeg)",
            "![](_page_363_Picture_9.jpeg)",
            "Two of the 28 elementary cellular automata",
            "![](_page_364_Figure_2.jpeg)",
            "Typical behavior of two-dimensional cellular automata",
        )
        self.assert_order(
            "![](_page_372_Figure_4.jpeg)",
            substitution_caption,
            "An essentially equivalent process involves every element branching",
            "![](_page_372_Figure_6.jpeg)",
            "Nested patterns generated by simple branching processes.",
        )
        self.assert_order(
            "The picture samples just the first cell in every $14 \\times 7$ block",
            "![](_page_374_Picture_10.jpeg)",
            "A highly compressed representation of the evolution of rule 110",
        )

    def test_text_only_label_raster_is_hidden_and_both_labels_are_live(self) -> None:
        comment = (
            "<!-- Editorial source-accounting reference: the legacy asset below "
            "rasterizes the author label transcribed as live text above.\n"
            "![](_page_375_Picture_5.jpeg)\n"
            "-->"
        )
        self.assertEqual(self.rendered.count(comment), 1)
        self.assertEqual(self.rendered.count("*k=3 totalistic code 1893*"), 1)
        self.assertEqual(self.rendered.count("*elementary rule 18 (compressed)*"), 1)
        self.assert_order(
            "![](_page_375_Picture_4.jpeg)",
            "*k=3 totalistic code 1893*",
            comment,
            "![](_page_375_Picture_6.jpeg)",
            "*elementary rule 18 (compressed)*",
            "Examples involving domains containing apparent randomness.",
        )
        visible_markdown = self.rendered.replace(comment, "")
        self.assertNotIn("![](_page_375_Picture_5.jpeg)", visible_markdown)

    def test_technical_math_punctuation_and_residual_ocr_are_exact(self) -> None:
        expected = (
            "say $x$, which runs from 0 to 1",
            "sizes of the numbers $x$, but rather",
            "position $FractionalPart[2 x]$ on the next step",
            "differing by $10^{-8}$—are shown",
            "reduced modulo $2^n$, where $n$ is the width",
            "$39 \\times 29$ cells in size",
            "$100^{\\circ}\\mathrm{C}$, a discrete transition",
            "a $20 \\times 20$ array",
            "a $30 \\times 30$ array",
            "a $2 \\times 2$ block",
            "explicit evolution rules—mostly those governing",
            "three-dimensional space",
        )
        for text in expected:
            with self.subTest(text=text):
                self.assertEqual(self.rendered.count(text), 1)
        self.assertEqual(self.rendered.count("a $10 \\times 10$ array"), 3)
        residues = (
            "guite",
            "threedimensional",
            "rulesmostly",
            "<sup>",
            "FractionalPart(2x)",
            "30 x 30",
            "39 x 29",
            "\nI\n",
            "  $",
            "$  ",
            "\t",
            "\ufffd",
        )
        for residue in residues:
            with self.subTest(residue=residue):
                self.assertNotIn(residue, self.rendered)
        self.assertEqual(self.rendered.count("$"), 34)

    def test_repaired_assets_are_pinned_and_reference_order_is_exact(self) -> None:
        chapter_images = [row for row in self.images if row["document_id"] == "CH07"]
        self.assertEqual(len(chapter_images), 92)
        self.assertEqual([row["ordinal"] for row in chapter_images], list(range(345, 437)))
        expected_repairs = {
            354: ("ed137122a85fe2b431a4e92e04e62b0896346565354f86c31cd9a7c8b9fa64b9", (861, 459)),
            356: ("664040e7606bf46b5dbace8e4f5d345c9906468fb812631b5dfedef8d16058bc", (1188, 707)),
            367: ("145c22860c8748b03906c65e83a9f109d2902c94ecc44e231f221fd044a2b1a7", (1170, 1154)),
            370: ("bb5b9ec85c595f56774b60c050068fbbfec8bf73f0ac617c07920f6c952b2edf", (275, 242)),
            374: ("f680b7be36592fbb7be42bddf13a7ca5bd7ba682369808e216d54de159f242bc", (1143, 1255)),
            391: ("ca511874fffcd5276cca44c7856bdedcf7f56426d2d52664b4faa63ba3244dc1", (380, 300)),
            392: ("afc8bbe14ebcf42402b29f865898fc1937d3768e55161540e5cccf2dec582855", (380, 310)),
            400: ("afd8f4864039c9859310fecab9dce0144e8891f2ed3cd7df93d56f70aa690602", (198, 143)),
            401: ("e587ca740623f157686c0162097904afe30126517d2eac1afc2448d277148bf5", (200, 143)),
            422: ("7369f22f93d6072ee7ff690fbf4ca807a778d1128583ce40854618dd084ea90d", (919, 195)),
            423: ("c947a0ef73de7a74bb0c282e8c7f4084cbe1b82e6a578733591288c224baa4b6", (1700, 352)),
            430: ("287c3aac228b01edf6dc96aa595eb924e5aa0b798e19a013d4195782db3e28ae", (376, 213)),
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

        self.assertEqual(
            [row for row in self.added_assets if row["document_id"] == "CH07"], []
        )
        expected_references = [
            Path(row["asset_relative_path"]).name for row in chapter_images
        ]
        references = re.findall(r"!\[\]\(([^)]+\.jpeg)\)", self.rendered)
        self.assertEqual(len(references), 92)
        self.assertEqual(len(set(references)), 92)
        self.assertEqual(references, expected_references)

        changed_images = copy.deepcopy(self.images)
        next(row for row in changed_images if row["ordinal"] == 423)[
            "repaired_asset_sha256"
        ] = "0" * 64
        with self.assertRaises(build.BuildError):
            build.validate_images(self.raw, self.documents, changed_images)


if __name__ == "__main__":
    unittest.main()
