from __future__ import annotations

import copy
import json
import re
import sys
import unittest
from pathlib import Path


GOAL_DIR = Path(__file__).resolve().parents[1]
if not (GOAL_DIR / "build.py").is_file():
    # Keep the /tmp review artifact executable before it is installed under goal-5/tests.
    GOAL_DIR = Path("/home/jake/Developer/ankos/goal-5")
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402
import validate  # noqa: E402


class ChapterNineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.range_data = json.loads(build.RANGES_PATH.read_text(encoding="utf-8"))
        cls.document = next(row for row in cls.documents if row["id"] == "CH09")
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

    def test_source_range_correction_packet_and_final_hash_are_exact(self) -> None:
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
                5164,
                6585,
                728322,
                932355,
                1422,
                204033,
                "59236b42ae21d1e55aaca55952d109c1371ef27e0765288b154a5772af8dae05",
                449,
                562,
                "433",
                "546",
            ),
        )
        raw_segment = self.raw[
            self.document["raw_start_byte"] : self.document["raw_end_byte_exclusive"]
        ]
        self.assertEqual(build.sha256(raw_segment), self.document["raw_segment_sha256"])

        relevant = [row for row in self.corrections if row["document_id"] == "CH09"]
        self.assertEqual(len(relevant), 77)
        self.assertEqual(
            [row["id"] for row in relevant],
            [f"G5-C-{number:04d}" for number in range(500, 577)],
        )
        self.assertTrue(all(row["expected_count"] == 1 for row in relevant))
        self.assertTrue(
            all(row["verification_status"] == "SOURCE_VERIFIED" for row in relevant)
        )
        self.assertTrue(all(row["reviewer_type"] == "agent" for row in relevant))
        for row in relevant:
            match = re.match(r"pdf:(\d{4})", row["authoritative_location"])
            self.assertIsNotNone(match, row["id"])
            self.assertTrue(449 <= int(match[1]) <= 562, row["id"])
            self.assertTrue(
                self.document["raw_start_byte"]
                <= row["raw_start_byte"]
                < self.document["raw_end_byte_exclusive"]
            )

        self.assertEqual(len(self.rendered_bytes), 204732)
        self.assertEqual(len(self.rendered.splitlines()), 1374)
        self.assertEqual(
            build.sha256(self.rendered_bytes),
            "c4786895ea852253233767f683f69ffce0f6e5576e948e4bbe3bf33c26cbc66c",
        )
        self.assertEqual(
            validate.independent_document_bytes(
                self.raw, self.documents, self.corrections
            )[self.path],
            self.rendered_bytes,
        )

    def test_authoritative_pdf_and_immutable_legacy_are_still_pinned(self) -> None:
        source = self.range_data["authoritative_source"]
        self.assertEqual(source["size_bytes"], 57_779_240)
        self.assertEqual(
            source["sha256"],
            "a3cc5dd60e12d6b563aee86ea31a15b03f9cddfd4869b8f965d3a11bbc61a0d6",
        )
        self.assertEqual(
            validate.validate_authoritative_source(self.range_data),
            build.REPO_ROOT / "A New Kind of Science/A New Kind of Science.pdf",
        )
        self.assertEqual(
            validate.legacy_tree_digest(),
            (
                "b9ff7b9b507790f1d519593baf2b2d2f24dd6cd49dc0fe10f0ac629278ea42f4",
                1463,
            ),
        )

        # The guarded source still contains the defects; only the rebuilt projection changes.
        for residue in (
            "upside-downeffectively",
            "non-planarity-nonzero",
            "How K33 is embedded",
            "(c)\n\n(b)\n\nInevitably",
        ):
            with self.subTest(raw_residue=residue):
                self.assertIn(residue, self.raw_text)
                self.assertNotIn(residue, self.rendered)

        changed = copy.deepcopy(self.corrections)
        next(row for row in changed if row["id"] == "G5-C-0576")[
            "raw_start_byte"
        ] += 1
        with self.assertRaises(build.BuildError):
            build.validate_corrections(changed, self.raw, self.documents)

    def test_opener_heading_hierarchy_and_source_literals_are_exact(self) -> None:
        self.assertTrue(
            self.rendered.startswith(
                "![](_page_448_Picture_0.jpeg)\n\n"
                "## Fundamental Physics\n\n"
                "### The Problems of Physics\n\n"
            )
        )
        headings = (
            "The Problems of Physics",
            "The Notion of Reversibility",
            "Irreversibility and the Second Law of Thermodynamics",
            "Conserved Quantities and Continuum Phenomena",
            "Ultimate Models for the Universe",
            "The Nature of Space",
            "Space as a Network",
            "The Relationship of Space and Time",
            "Time and Causal Networks",
            "The Sequencing of Events in the Universe",
            "Uniqueness and Branching in Time",
            "Evolution of Networks",
            "Space, Time and Relativity",
            "Elementary Particles",
            "The Phenomenon of Gravity",
            "Quantum Phenomena",
        )
        self.assertEqual(self.rendered.count("\n### "), len(headings))
        for heading in headings:
            self.assertEqual(self.rendered.count(f"### {heading}"), 1)
        self.assertNotIn("####", self.rendered)
        self.assertNotIn("### **", self.rendered)
        self.assertNotRegex(self.rendered, r"(?m)^## 9$")
        self.assertNotIn("STEPHEN WOLFRAM", self.rendered)
        self.assertNotIn("A NEW KIND OF SCIENCE", self.rendered)
        self.assertEqual(self.rendered.count("<sup>▶</sup>"), 1)

        # These visibly awkward constructions are literal source wording.
        for text in (
            "So even though the total of the energy of all particles remains the same",
            "there must to a good approximation be the kind of straightforward locality",
            "But the bottom row of pictures show that there are corrections to this.",
            "4,294,967,296 possible next-neighbor rules",
        ):
            with self.subTest(source_literal=text):
                self.assertEqual(self.rendered.count(text), 1)

    def test_interrupted_prose_and_source_figure_order_are_serialized(self) -> None:
        initial_condition = (
            r"with initial condition $\blacksquare\blacksquare\blacksquare"
            r"\blacksquare\blacksquare\blacksquare\Box\Box\Box\Box\Box"
            r"\blacksquare\blacksquare\blacksquare\blacksquare\blacksquare"
            r"\blacksquare$."
        )
        self.assert_order(
            "to search through these rules, trying each one in turn",
            "![](_page_482_Figure_1.jpeg)",
            initial_condition,
            "Thus, for example, cellular automata probably already have too rigid",
        )
        self.assert_order(
            "broken into a collection of nodes with exactly three connections, "
            "as in the pictures on the left.",
            "![](_page_491_Picture_1.jpeg)",
            "Examples of how nodes with more than three connections can be decomposed",
        )
        self.assert_order(
            "And any substitution system whose rules specify replacements only for "
            "blocks such as these",
            "### Uniqueness and Branching in Time",
            "![](_page_519_Picture_8.jpeg)",
            "A simple example of a multiway system in which replacements are applied",
        )
        self.assert_order(
            "traditional intuition would tend to make one think that the elaborate "
            "properties of particles",
            "![](_page_542_Picture_10.jpeg)",
            "![](_page_542_Picture_11.jpeg)",
            "The K<sub>5</sub> and K<sub>3,3</sub> forms that lead to non-planarity",
            "![](_page_542_Picture_13.jpeg)",
            "How K<sub>3,3</sub> is embedded in the network from the facing page.",
        )

    def test_high_risk_technical_text_math_and_residual_detectors_are_exact(self) -> None:
        expected = (
            "rule 154R",
            (
                r"at distance $r$ there are exactly $3r$ nodes—so that the total "
                r"number of nodes out to distance $r$ grows like $r^2$"
            ),
            r"Network (e) effectively has limiting dimension "
            r"$Log[2, 3] \simeq 1.58$.",
            (
                r"The simplest non-trivial pair of blocks that has this property is "
                r"$\blacksquare\blacksquare\Box\Box$, "
                r"$\blacksquare\blacksquare\Box\blacksquare\Box$"
            ),
            (
                r"the simplest triple is $\blacksquare\blacksquare\blacksquare"
                r"\Box\Box$, $\blacksquare\Box\blacksquare\Box\Box$, "
                r"$\blacksquare\Box\blacksquare\blacksquare\Box\Box$"
            ),
            r"$1/\sqrt{1-v^2/c^2}$, where $v/c$ is the ratio",
            r"Case (c) shows the negatively curved surface $z = x^2 - y^2$",
            "how many nodes lie within successive distances $r$ of a given node",
            "many particles—and many events—will always be involved in getting it.",
        )
        for text in expected:
            with self.subTest(text=text):
                self.assertEqual(self.rendered.count(text), 1)

        self.assertEqual(self.rendered.count(r"\simeq"), 3)
        self.assertEqual(self.rendered.count("K<sub>3,3</sub>"), 2)
        self.assertEqual(self.rendered.count(r"\blacksquare"), 36)
        self.assertEqual(self.rendered.count(r"\Box"), 28)
        self.assertEqual(self.rendered.count("$"), 144)

        residues = (
            "upside-downeffectively",
            "non-planarity-nonzero",
            "How K33 is embedded",
            "root overlap is possible",
            "simplest triple is , while the simplest triple",
            "at distance r there are exactly 3 r nodes",
            "$3 r$",
            r"$Log[2, 3] \approx 1.58$",
            "events— will",
            "  $",
            "$  ",
            "\t",
            "\ufffd",
        )
        for residue in residues:
            with self.subTest(residue=residue):
                self.assertNotIn(residue, self.rendered)

    def test_p493_and_p527_visual_groups_and_live_captions_are_exact(self) -> None:
        layout_caption = "Six different ways of laying out the same network."
        network_caption = (
            "Examples of the evolution of networks in which a single cluster of "
            "nodes is replaced at each step according to the rules shown."
        )
        self.assertEqual(self.rendered.count(layout_caption), 1)
        self.assertEqual(self.rendered.count(network_caption), 1)
        self.assert_order(
            "![](_page_492_Picture_7.jpeg)",
            "![](_page_492_Picture_8.jpeg)",
            "![](_page_492_Picture_9.jpeg)",
            "![](_page_492_Picture_10.jpeg)",
            "![](_page_492_Picture_11.jpeg)",
            "![](_page_492_Picture_12.jpeg)",
            layout_caption,
        )
        self.assert_order(
            "![](_page_526_Picture_2.jpeg)",
            "![](_page_526_Picture_3.jpeg)",
            "![](_page_526_Picture_4.jpeg)",
            network_caption,
            "Inevitably there is a certain arbitrariness in the way these pictures are drawn.",
        )
        self.assertNotRegex(self.rendered, r"(?m)^\(c\)\n\n\(b\)$")
        self.assertNotIn('(c)\n\n(b)\n\nInevitably', self.rendered)
        self.assertEqual(self.rendered.count("drawn with a “clock”"), 1)
        self.assertNotIn('drawn with a "clock"', self.rendered)

    def test_repaired_and_added_assets_are_pinned_and_reference_order_is_exact(
        self,
    ) -> None:
        chapter_images = [row for row in self.images if row["document_id"] == "CH09"]
        self.assertEqual(len(chapter_images), 110)
        self.assertEqual([row["ordinal"] for row in chapter_images], list(range(480, 590)))

        repaired = [
            row for row in chapter_images if "repaired_asset_relative_path" in row
        ]
        self.assertEqual([row["ordinal"] for row in repaired], [556])
        repaired_row = repaired[0]
        repaired_source = build.REPO_ROOT / Path(
            repaired_row["repaired_asset_relative_path"]
        )
        repaired_output = build.OUTPUT_ROOT / Path(self.path).parent / repaired_source.name
        repaired_payload = repaired_source.read_bytes()
        self.assertEqual(
            build.sha256(repaired_payload),
            "b591788d742b597cf38b5d2b22bc9244ff6f421ee95554d081d9932d0c007c55",
        )
        self.assertEqual(
            repaired_row["repaired_asset_sha256"], build.sha256(repaired_payload)
        )
        self.assertEqual(build.jpeg_dimensions(repaired_payload), (1200, 859))
        self.assertEqual(
            (repaired_row["repaired_width_px"], repaired_row["repaired_height_px"]),
            (1200, 859),
        )
        self.assertTrue(repaired_row["repaired_authoritative_location"].startswith("pdf:0527"))
        self.assertEqual(repaired_output.read_bytes(), repaired_payload)

        legacy_replaced = build.LEGACY_ROOT / Path(repaired_row["asset_relative_path"])
        legacy_replaced_payload = legacy_replaced.read_bytes()
        self.assertEqual(
            build.sha256(legacy_replaced_payload),
            "369854b0e0497c44945f93b98170d690a15c324ef8045b531fb3b1e0e400bcb7",
        )
        self.assertNotEqual(legacy_replaced_payload, repaired_payload)

        chapter_added = [
            row for row in self.added_assets if row["document_id"] == "CH09"
        ]
        expected_added = {
            "G5-A-0020": (
                "6d6e8a572b330bd82e0f1dd05e7d222ebb74635f662200c3373c916dab0ded8c",
                (205, 235),
                "pdf:0493",
            ),
            "G5-A-0021": (
                "4b5cdc6b7c8d89a678938025c29fdf452c95b30433d97a2e82dce50bbece4e11",
                (870, 920),
                "pdf:0527",
            ),
            "G5-A-0022": (
                "cc0c3d4e36c30467024b57562029e1df31363e0ab22851bec6f24be409da32a8",
                (625, 380),
                "pdf:0527",
            ),
        }
        self.assertEqual([row["id"] for row in chapter_added], list(expected_added))
        added_names: dict[str, str] = {}
        for row in chapter_added:
            expected_hash, expected_dimensions, expected_page = expected_added[row["id"]]
            with self.subTest(added=row["id"]):
                source = build.REPO_ROOT / Path(row["asset_relative_path"])
                output = build.OUTPUT_ROOT / Path(self.path).parent / source.name
                payload = source.read_bytes()
                added_names[row["id"]] = source.name
                self.assertEqual(build.sha256(payload), expected_hash)
                self.assertEqual(row["asset_sha256"], expected_hash)
                self.assertEqual(build.jpeg_dimensions(payload), expected_dimensions)
                self.assertEqual((row["width_px"], row["height_px"]), expected_dimensions)
                self.assertTrue(row["authoritative_location"].startswith(expected_page))
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                self.assertEqual(output.read_bytes(), payload)

        mapped_names = {
            row["ordinal"]: Path(row["asset_relative_path"]).name
            for row in chapter_images
        }
        expected_references = (
            [mapped_names[number] for number in range(480, 520)]
            + [added_names["G5-A-0020"]]
            + [mapped_names[number] for number in range(520, 557)]
            + [added_names["G5-A-0021"], added_names["G5-A-0022"]]
            + [mapped_names[number] for number in range(557, 590)]
        )
        references = re.findall(r"!\[\]\(([^)]+\.jpeg)\)", self.rendered)
        self.assertEqual(len(references), 113)
        self.assertEqual(len(set(references)), 113)
        self.assertEqual(references, expected_references)

        # The opener ownership quirk and unrelated ordinal 526 are visual no-ops.
        unchanged = {
            480: "0e6b4888221df3d9d6879027f8c67cd839a8b71782ebc57547b65fa019088d44",
            526: "bcacb0823dbd5f4d883ec53e87d7a61229d4c39baba4916c0fe0948c34d07c7a",
        }
        for ordinal, expected_hash in unchanged.items():
            row = next(item for item in chapter_images if item["ordinal"] == ordinal)
            with self.subTest(unchanged=ordinal):
                self.assertNotIn("repaired_asset_relative_path", row)
                legacy = build.LEGACY_ROOT / Path(row["asset_relative_path"])
                output = build.OUTPUT_ROOT / Path(self.path).parent / legacy.name
                payload = legacy.read_bytes()
                self.assertEqual(row["asset_sha256"], expected_hash)
                self.assertEqual(build.sha256(payload), expected_hash)
                self.assertEqual(output.read_bytes(), payload)

        changed_images = copy.deepcopy(self.images)
        next(row for row in changed_images if row["ordinal"] == 556)[
            "repaired_asset_sha256"
        ] = "0" * 64
        with self.assertRaises(build.BuildError):
            build.validate_images(self.raw, self.documents, changed_images)

        changed_added = copy.deepcopy(self.added_assets)
        next(row for row in changed_added if row["id"] == "G5-A-0020").pop("reason")
        with self.assertRaises(build.BuildError):
            build.validate_added_assets(self.documents, self.images, changed_added)


if __name__ == "__main__":
    unittest.main()
