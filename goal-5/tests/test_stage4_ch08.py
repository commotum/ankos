from __future__ import annotations

import copy
import re
import sys
import unittest
from pathlib import Path


GOAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402


class ChapterEightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.document = next(row for row in cls.documents if row["id"] == "CH08")
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
                4336,
                5163,
                601461,
                728322,
                828,
                126861,
                "04cac96c665697d1ac5bf4f1ac70ac3772b651c2f5c0cf6df26914ea7194a3af",
                379,
                448,
                "363",
                "432",
            ),
        )
        relevant = [row for row in self.corrections if row["document_id"] == "CH08"]
        self.assertEqual(len(relevant), 47)
        self.assertEqual(
            [row["id"] for row in relevant],
            [f"G5-C-{number:04d}" for number in range(453, 500)],
        )
        self.assertTrue(all(row["expected_count"] == 1 for row in relevant))
        self.assertTrue(
            all(row["verification_status"] == "SOURCE_VERIFIED" for row in relevant)
        )
        self.assertTrue(all(row["reviewer_type"] == "agent" for row in relevant))
        self.assertTrue(
            all(
                379
                <= int(re.match(r"pdf:(\d{4})", row["authoritative_location"])[1])
                <= 448
                for row in relevant
            )
        )
        self.assertEqual(len(self.rendered_bytes), 126417)
        self.assertEqual(len(self.rendered.splitlines()), 770)
        self.assertEqual(
            build.sha256(self.rendered_bytes),
            "5e794cedc877e539e30d9ef6102fea18f4533c56d3324f7d454326336e4a2004",
        )

    def test_opener_heading_hierarchy_and_source_literals_are_exact(self) -> None:
        self.assertTrue(
            self.rendered.startswith(
                "![](_page_378_Picture_0.jpeg)\n\n"
                "## Implications for Everyday Systems\n\n"
                "### Issues of Modelling\n\n"
            )
        )
        headings = (
            "Issues of Modelling",
            "The Growth of Crystals",
            "The Breaking of Materials",
            "Fluid Flow",
            "Fundamental Issues in Biology",
            "Growth of Plants and Animals",
            "Biological Pigmentation Patterns",
            "Financial Systems",
        )
        self.assertEqual(self.rendered.count("\n### "), len(headings))
        for heading in headings:
            self.assertEqual(self.rendered.count(f"### {heading}"), 1)
        self.assertNotIn("####", self.rendered)
        self.assertNotIn("### **", self.rendered)
        self.assertNotRegex(self.rendered, r"(?m)^## 8$")
        self.assertNotIn("STEPHEN WOLFRAM", self.rendered)
        self.assertNotIn("A NEW KIND OF SCIENCE", self.rendered)
        self.assertEqual(self.rendered.count("<sup>▶</sup>"), 1)

        # These two awkward phrases are literal source text, not residual OCR.
        self.assertEqual(self.rendered.count("case take a cell to become black"), 1)
        self.assertEqual(
            self.rendered.count(
                "The pictures below shows some typical examples of patterns found "
                "on mollusc shells."
            ),
            1,
        )

    def test_interrupted_prose_and_figure_groups_are_serialized(self) -> None:
        self.assert_order(
            "as new branches grow but then collide with each other.",
            "![](_page_386_Figure_1.jpeg)",
            "The evolution of a cellular automaton in which each cell on a "
            "hexagonal grid becomes black",
            "And if one looks at real snowflakes",
        )
        self.assert_order(
            "the paths of the cracks that emerge nevertheless appear to be quite random.",
            "![](_page_390_Figure_4.jpeg)",
            "A very simple cellular automaton model for fracture.",
            "There are certainly many aspects of real materials",
        )
        self.assert_order(
            "the behavior one gets is at first quite simple.",
            "capable of generating essentially arbitrary complexity by using short programs",
            "![](_page_406_Picture_1.jpeg)",
            "The behavior of a sequence of cellular automaton programs obtained by "
            "successive random mutations.",
            "But if complexity is this easy to get",
        )
        self.assert_order(
            "natural selection cannot reasonably be considered the source of the "
            "elaborate forms we see.",
            "![](_page_431_Picture_2.jpeg)",
            "Shell shapes generated by the simple model and found in nature.",
            "Away from mollusc shells, coiled structures",
        )
        self.assert_order(
            "simple models do not necessarily have simple behavior.",
            "![](_page_447_Picture_3.jpeg)",
            "![](_page_447_Figure_4.jpeg)",
            "![](_page_447_Figure_8.jpeg)",
            "An example of a very simple idealized model of a market.",
            "In real markets, it is usually impossible to see in detail",
        )

    def test_fluid_figures_live_captions_and_added_stages_are_complete(self) -> None:
        microscopic_caption = (
            "A simple cellular automaton system set up to emulate the microscopic "
            "behavior of molecules in a fluid. At each step the configuration of "
            "particles is updated according to the simple collision rules shown "
            "above. Particles are reflected whenever they hit the plate. A steady "
            "stream of particles is inserted in a regular way far to the left, "
            "with an average speed 3/10 of the maximum possible. Picture (a) shows "
            "the configuration of individual particles; pictures (b) and (c) show "
            "total velocities of successively larger blocks of particles. Picture "
            "(d) is obtained by transforming to a reference frame in which the "
            "fluid is on average at rest."
        )
        large_caption = (
            "A larger example of the cellular automaton system shown on the previous "
            "page. In each picture there are a total of 30 million underlying cells. "
            "The individual velocity vectors drawn correspond to averages over "
            "20 × 20 blocks of cells. Particles are inserted in a regular way at the "
            "left-hand end so as to maintain an overall flow speed equal to about "
            "0.4 of the maximum possible. To make the patterns of flow easier to "
            "see, the velocities shown are transformed so that the fluid is on "
            "average at rest, and the plate is moving. The underlying density of "
            "particles is approximately 1 per cell, or 1/6 the maximum possible—a "
            "density which more or less minimizes the viscosity of the fluid. The "
            "Reynolds number of the flow shown is then approximately 100. The "
            "agreement with experimental results on actual fluid flows is striking."
        )
        self.assertEqual(self.rendered.count(microscopic_caption), 1)
        self.assertEqual(self.rendered.count(large_caption), 1)
        self.assert_order(
            "pictures (b) and (c)—then what begins to emerge is behavior",
            "![](_page_393_Figure_2.jpeg)",
            microscopic_caption,
            "This happens for exactly the same reason as in a real fluid",
        )
        self.assert_order(
            "sensitive dependence on initial conditions, and with the chaos phenomenon",
            "![](_page_395_Figure_1.jpeg)",
            "![](_page_395_Figure_2.jpeg)",
            "![](_page_395_Step_30000.jpeg)",
            "![](_page_395_Picture_4.jpeg)",
            "![](_page_395_Step_50000.jpeg)",
            "![](_page_395_Picture_6.jpeg)",
            "![](_page_395_Picture_7.jpeg)",
            large_caption,
            "But while there are certainly mathematical equations",
        )
        self.assert_order(
            "one cannot realistically attribute the large-scale randomness",
            "![](_page_397_Picture_1.jpeg)",
            "A cellular automaton (rule 225) whose behavior is reminiscent of "
            "turbulent fluid flow.",
            "Instead, what seems to be happening is that intrinsic randomness generation",
        )

    def test_technical_math_punctuation_italics_and_residual_ocr_are_exact(self) -> None:
        expected = (
            "use one’s eyes, and to compare overall pictures",
            "differences—associated for example with texture and pigmentation patterns",
            r"about $137.5^{\circ}$ is equivalent to a rotation",
            r"golden ratio $(1+\sqrt{5})/2 \simeq 1.618$",
            r"$n^{\rm th}$ element appears at coordinates "
            r"$\sqrt{n}\,\{Cos[n\,\theta], Sin[n\,\theta]\}$",
            r"$Length[ContinuedFraction[\theta/\pi]]$.",
            r"$1/\sqrt{s}$ (involute of circle)",
            r"$e^{-s^2}$; $Sin[s]$; $s\,Sin[s]$",
            "The curvature functions $f[s]$ can be thought of as specifying",
            "(*Livonia mammilla*)",
            "previous state of its neighbors—just as in a one-dimensional cellular automaton",
            "negative weights— -0.4 per cell for the first rule, and -0.2 for the second",
            "weights of cells at distances 2 and 3",
            "certain critical level.\n\nBut as soon",
        )
        for text in expected:
            with self.subTest(text=text):
                self.assertEqual(self.rendered.count(text), 1)

        residues = (
            "one's eyes",
            "> The occurrence of these last forms",
            "differences—\n\nassociated",
            " $\\sqrt{n}$  {",
            "t (t involute of circle)",
            "(Livonia mammilla)",
            "previous state of its neighbors just as",
            "negative weights -- -0.4",
            "weights of cells at distance 2 and 3",
            "  $",
            "$  ",
            "\t",
            "\ufffd",
        )
        for residue in residues:
            with self.subTest(residue=residue):
                self.assertNotIn(residue, self.rendered)
        self.assertEqual(self.rendered.count("$"), 34)

    def test_repaired_and_added_assets_are_pinned_and_reference_order_is_exact(
        self,
    ) -> None:
        chapter_images = [row for row in self.images if row["document_id"] == "CH08"]
        self.assertEqual(len(chapter_images), 43)
        self.assertEqual([row["ordinal"] for row in chapter_images], list(range(437, 480)))
        expected_repairs = {
            444: (
                "45030dec7d6bd185fcdbb0ce3c75ec2bfa2d221226c9d87d31fcf82ec6d88be8",
                (1290, 1253),
            ),
            446: (
                "8ce5654a67e41789da1c1a8b105befc2f1b662bdfb71b9ab0366b27ff6b5652a",
                (462, 317),
            ),
            447: (
                "fe24bb6d4b2bee4fe1da04ea25a0f3b72e387cf39182a7aa1c02e6d32e568df2",
                (462, 326),
            ),
            448: (
                "a5fb015b7a038f876fe91efbef74503935e69574d492503335af21230586db7c",
                (926, 314),
            ),
            449: (
                "c64c38f5ebce894e285d134e65d6297fe6469e5e5b4a107214246416be144a02",
                (926, 313),
            ),
            450: (
                "6ba87562f18a13460fe97fe6dfbc0816d1f95d0f4726b88dcf188065bcc90f65",
                (287, 1449),
            ),
            452: (
                "8919a6aa4ec0977b4a367eccd40c06541461aeab272ab0f68d7f6338f0ef7681",
                (1254, 1019),
            ),
            453: (
                "029720c8047d287cd08afbc90992b8219d6adab3681fa64778b7a5e69eddf9f0",
                (240, 136),
            ),
            468: (
                "66ce091540c8330e1e765c8db4a4ec1d4c0c8e7079db49453506f2c35147a90f",
                (1021, 1643),
            ),
        }
        repaired = [
            row for row in chapter_images if "repaired_asset_relative_path" in row
        ]
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

        chapter_added = [
            row for row in self.added_assets if row["document_id"] == "CH08"
        ]
        expected_added = {
            "G5-A-0018": (
                "663e21e9721ae560465a89dd91d1f4aaaed2e41291e8900b16e4fb68756f9471",
                (462, 326),
            ),
            "G5-A-0019": (
                "12240c5524ea922d68b3ec647c6d45a88d47ce0dceb48d143fca665457e27f22",
                (926, 315),
            ),
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

        mapped_names = {
            row["ordinal"]: Path(row["asset_relative_path"]).name
            for row in chapter_images
        }
        expected_references = (
            [mapped_names[number] for number in range(437, 447)]
            + [added_names["G5-A-0018"]]
            + [mapped_names[447]]
            + [added_names["G5-A-0019"]]
            + [mapped_names[number] for number in range(448, 480)]
        )
        references = re.findall(r"!\[\]\(([^)]+\.jpeg)\)", self.rendered)
        self.assertEqual(len(references), 45)
        self.assertEqual(len(set(references)), 45)
        self.assertEqual(references, expected_references)

        changed_images = copy.deepcopy(self.images)
        next(row for row in changed_images if row["ordinal"] == 468)[
            "repaired_asset_sha256"
        ] = "0" * 64
        with self.assertRaises(build.BuildError):
            build.validate_images(self.raw, self.documents, changed_images)
        changed_added = copy.deepcopy(self.added_assets)
        next(row for row in changed_added if row["id"] == "G5-A-0018").pop("reason")
        with self.assertRaises(build.BuildError):
            build.validate_added_assets(self.documents, self.images, changed_added)


if __name__ == "__main__":
    unittest.main()
