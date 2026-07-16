from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path


GOAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402
import validate  # noqa: E402


EXPECTED_SHA256 = "24a49cf980ad8b5593c129fe4ed1978d79601c41099669aadbcb089d61084c9e"
EXPECTED_BYTES = 86_697
EXPECTED_LINES = 915
EXPECTED_CORRECTIONS_SHA256 = (
    "52fcb1e5dca388ebb51e1b15ecf7d974708d626db8ae2947f76715e84c50a4df"
)
EXPECTED_IMAGE_ROWS_SHA256 = (
    "510f87b2b07ded726f7385454daec5042d4fa4eff36a565bc58acf0c9ef186bc"
)
EXPECTED_ADDED_ROWS_SHA256 = (
    "4635d4cb9c570c57c05f57f72f9f792f503cac6f28acf90774348fff26ca914b"
)
EXPECTED_MAIN_LABELS_SHA256 = (
    "6c128d182e57b9312b48cad6fbaef63f1f568640fb9c315c84bc47faa6b10589"
)
EXPECTED_MAPPED_REFERENCES_SHA256 = (
    "5ae0efba370e2dfb5a8eccdf9c146d7e8d419ff32ea65f0463f84e1c104f4c21"
)

# ordinal: (basename, repaired digest, dimensions, canonical PDF page)
EXPECTED_REPAIRS = {
    842: (
        "_page_885_Picture_23.jpeg",
        "ba46e91fb91ed113e87cf3e14a900ec36c7a5428a3019c23dd2001a57a6f2b1f",
        (131, 144),
        "pdf:0886",
    ),
    851: (
        "_page_888_Picture_5.jpeg",
        "bd264b27d227693e8087ffd8a2288136984de6431c08e7ad1ba5945974e231b5",
        (103, 98),
        "pdf:0889",
    ),
    852: (
        "_page_888_Picture_6.jpeg",
        "cd06a8d4a3306d56ee610dce9b30ba911a306c045f0b9a237f6e49f5fb3db009",
        (103, 98),
        "pdf:0889",
    ),
    866: (
        "_page_889_Picture_5.jpeg",
        "430f9f249930d3f3132bdd64d5cc734219ef69d7fd88d0fba5b19c5b929bc658",
        (102, 102),
        "pdf:0890",
    ),
    867: (
        "_page_889_Picture_6.jpeg",
        "b81a750fab1412780ad01444c1da5f8001568ee05af8a975ef5aff77321e182f",
        (103, 102),
        "pdf:0890",
    ),
    872: (
        "_page_889_Picture_19.jpeg",
        "1becc30455a49adc4804802d05f90649089f41770c1561d68f2f4697bd7db8db",
        (123, 178),
        "pdf:0890",
    ),
    873: (
        "_page_889_Picture_20.jpeg",
        "393057f96db8e6848e7ec5e5d397079387da3bed6d90c71218d8f6f5b1db7e10",
        (195, 178),
        "pdf:0890",
    ),
    877: (
        "_page_897_Picture_20.jpeg",
        "5d2d9922f0c867a9a4be9809e31a1f6a8e76d7eba0b7aaf8120abc89468984d7",
        (518, 319),
        "pdf:0898",
    ),
}

# asset id: (basename, digest, dimensions)
EXPECTED_ADDED = {
    "G5-A-0042": (
        "_page_885_inline_black_cell.jpeg",
        "7e29ee2f85b3dd057f3ffe7ffed5ea8c713661d9d14188b505e0690de74b62d1",
        (15, 16),
    ),
    "G5-A-0043": (
        "_page_885_inline_black_gradient_white_block.jpeg",
        "82f3e89c67e0eb5b91b897847097cdf8d94ae7d592a8f93a71f66679f110c0b1",
        (41, 16),
    ),
}


class NotesForChapter2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.document = next(row for row in cls.documents if row["id"] == "N02")
        cls.path = build.safe_relative_path(
            cls.document["output_path"], suffix=".md"
        )
        cls.rendered_bytes = build.document_bytes(
            cls.raw, cls.documents, cls.corrections
        )[cls.path]
        cls.rendered = cls.rendered_bytes.decode("utf-8")
        cls.output_path = build.OUTPUT_ROOT / Path(cls.path)
        cls.n02_corrections = [
            row for row in cls.corrections if row["document_id"] == "N02"
        ]
        cls.n02_images = [
            row for row in cls.images if row["document_id"] == "N02"
        ]
        cls.n02_added = [
            row for row in cls.added_assets if row["document_id"] == "N02"
        ]

    @staticmethod
    def rows_sha256(rows: list[dict[str, object]]) -> str:
        payload = (
            "\n".join(
                json.dumps(
                    row,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                )
                for row in rows
            )
            + "\n"
        ).encode("utf-8")
        return build.sha256(payload)

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
                10895,
                11630,
                1614202,
                1703015,
                736,
                88813,
                "a61d99e196259648128812cf904149a077cec866d18cc8b841abb6bb679e3d24",
                881,
                898,
                "865",
                "882",
            ),
        )
        segment = self.raw[1614202:1703015]
        self.assertEqual(len(segment), 88813)
        self.assertEqual(
            build.sha256(segment), self.document["raw_segment_sha256"]
        )

        self.assertEqual(len(self.n02_corrections), 43)
        self.assertEqual(
            [row["id"] for row in self.n02_corrections],
            [f"G5-C-{number:04d}" for number in range(906, 949)],
        )
        self.assertEqual(
            self.rows_sha256(self.n02_corrections),
            EXPECTED_CORRECTIONS_SHA256,
        )
        self.assertEqual(
            len({row["before"] for row in self.n02_corrections}), 43
        )

        previous_end = self.document["raw_start_byte"]
        ordered_corrections = sorted(
            self.n02_corrections, key=lambda row: row["raw_start_byte"]
        )
        for row in ordered_corrections:
            with self.subTest(correction=row["id"]):
                self.assertEqual(
                    set(row), build.CORRECTION_FIELDS | {"raw_line"}
                )
                self.assertEqual(row["document_id"], "N02")
                self.assertEqual(row["expected_count"], 1)
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(
                    row["verification_status"], "SOURCE_VERIFIED"
                )
                self.assertTrue(row["reason"].strip())
                pages = [
                    int(value)
                    for value in re.findall(
                        r"pdf:(\d{4})", row["authoritative_location"]
                    )
                ]
                self.assertTrue(pages)
                self.assertTrue(all(881 <= page <= 898 for page in pages))
                self.assertTrue(10895 <= row["raw_line"] <= 11630)

                start = row["raw_start_byte"]
                before = row["before"].encode("utf-8")
                end = start + len(before)
                self.assertGreaterEqual(start, previous_end)
                self.assertLessEqual(end, 1703015)
                self.assertEqual(self.raw[start:end], before)
                self.assertEqual(segment.count(before), 1)
                previous_end = end

        self.assertEqual(len(self.rendered_bytes), EXPECTED_BYTES)
        self.assertEqual(len(self.rendered.splitlines()), EXPECTED_LINES)
        self.assertEqual(build.sha256(self.rendered_bytes), EXPECTED_SHA256)
        self.assertEqual(self.output_path.read_bytes(), self.rendered_bytes)
        self.assertEqual(
            validate.independent_document_bytes(
                self.raw, self.documents, self.corrections
            )[self.path],
            self.rendered_bytes,
        )

    def test_heading_and_structural_counts_are_exact(self) -> None:
        self.assertEqual(
            re.findall(r"(?m)^#{2,3} .+$", self.rendered),
            [
                "## The Crucial Experiment",
                "### How Do Simple Programs Behave?",
                "### The Need for a New Intuition",
                "### Why These Discoveries Were Not Made Before",
            ],
        )
        labels = re.findall(r"(?m)^■ \*\*(.+?)\*\*", self.rendered)
        self.assertEqual(len(labels), 33)
        self.assertEqual(
            build.sha256(("\n".join(labels) + "\n").encode("utf-8")),
            EXPECTED_MAIN_LABELS_SHA256,
        )
        self.assertEqual(len(re.findall(r"(?m)^▪ ", self.rendered)), 101)
        self.assertEqual(self.rendered.count("```"), 94)
        self.assertEqual(
            len(re.findall(r"(?<!`)`[^`\n]+`(?!`)", self.rendered)), 105
        )
        self.assertEqual(
            len(re.findall(r"(?m)^In\[\d+\]", self.rendered)), 13
        )
        self.assertNotIn("####", self.rendered)

    def test_mapped_reference_inventory_and_order_are_exact(self) -> None:
        self.assertEqual(len(self.n02_images), 54)
        self.assertEqual(
            [row["ordinal"] for row in self.n02_images],
            list(range(824, 878)),
        )
        self.assertEqual(
            self.rows_sha256(self.n02_images), EXPECTED_IMAGE_ROWS_SHA256
        )
        mapped_names = [
            Path(row["asset_relative_path"]).name for row in self.n02_images
        ]
        self.assertEqual(
            build.sha256(
                ("\n".join(mapped_names) + "\n").encode("utf-8")
            ),
            EXPECTED_MAPPED_REFERENCES_SHA256,
        )

        references = re.findall(
            r"!\[([^\]]*)\]\(([^)\s]+\.jpeg)\)", self.rendered
        )
        self.assertEqual(len(references), 56)
        self.assertEqual(len({target for _, target in references}), 56)
        added_names = {
            Path(row["asset_relative_path"]).name for row in self.n02_added
        }
        actual_mapped = [
            target for _, target in references if target not in added_names
        ]
        self.assertEqual(actual_mapped, mapped_names)
        self.assertEqual(
            references[14:18],
            [
                ("", "_page_884_Figure_30.jpeg"),
                ("black cell", "_page_885_inline_black_cell.jpeg"),
                (
                    "striped black-to-white block",
                    "_page_885_inline_black_gradient_white_block.jpeg",
                ),
                ("", "_page_885_Picture_12.jpeg"),
            ],
        )

    def test_eight_repaired_rows_and_output_assets_are_exact(self) -> None:
        repaired_rows = [
            row
            for row in self.n02_images
            if "repaired_asset_relative_path" in row
        ]
        self.assertEqual(
            [row["ordinal"] for row in repaired_rows],
            list(EXPECTED_REPAIRS),
        )
        for row in repaired_rows:
            basename, digest, dimensions, page = EXPECTED_REPAIRS[
                row["ordinal"]
            ]
            with self.subTest(ordinal=row["ordinal"], asset=basename):
                repaired_fields = (
                    build.REPAIRED_IMAGE_FIELDS & set(row)
                )
                self.assertEqual(
                    repaired_fields, build.REPAIRED_IMAGE_FIELDS
                )
                legacy = build.LEGACY_ROOT / Path(
                    row["asset_relative_path"]
                )
                repaired = build.REPO_ROOT / Path(
                    row["repaired_asset_relative_path"]
                )
                output = (
                    build.OUTPUT_ROOT / Path(self.path).parent / basename
                )
                payload = repaired.read_bytes()

                self.assertEqual(legacy.name, basename)
                self.assertEqual(repaired.name, basename)
                self.assertEqual(
                    build.sha256(legacy.read_bytes()),
                    row["asset_sha256"],
                )
                self.assertEqual(row["repaired_asset_sha256"], digest)
                self.assertEqual(build.sha256(payload), digest)
                self.assertEqual(build.jpeg_dimensions(payload), dimensions)
                self.assertEqual(
                    (
                        row["repaired_width_px"],
                        row["repaired_height_px"],
                    ),
                    dimensions,
                )
                self.assertTrue(
                    row["repaired_authoritative_location"].startswith(page)
                )
                page_match = re.search(r"_page_(\d+)_", basename)
                self.assertIsNotNone(page_match)
                self.assertEqual(
                    int(page_match.group(1)) + 1, int(page[-4:])
                )
                self.assertEqual(output.read_bytes(), payload)

    def test_added_inline_rows_assets_and_placement_are_exact(self) -> None:
        self.assertEqual(
            [row["id"] for row in self.n02_added],
            ["G5-A-0042", "G5-A-0043"],
        )
        self.assertEqual(
            self.rows_sha256(self.n02_added), EXPECTED_ADDED_ROWS_SHA256
        )
        for row in self.n02_added:
            basename, digest, dimensions = EXPECTED_ADDED[row["id"]]
            with self.subTest(asset=row["id"]):
                self.assertEqual(set(row), build.ADDED_ASSET_FIELDS)
                self.assertEqual(row["document_id"], "N02")
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(
                    row["verification_status"], "SOURCE_VERIFIED"
                )
                self.assertTrue(
                    row["authoritative_location"].startswith("pdf:0886")
                )
                source = build.REPO_ROOT / Path(
                    row["asset_relative_path"]
                )
                output = (
                    build.OUTPUT_ROOT / Path(self.path).parent / basename
                )
                payload = source.read_bytes()
                self.assertEqual(source.name, basename)
                self.assertEqual(row["asset_sha256"], digest)
                self.assertEqual(build.sha256(payload), digest)
                self.assertEqual(build.jpeg_dimensions(payload), dimensions)
                self.assertEqual(
                    (row["width_px"], row["height_px"]), dimensions
                )
                self.assertEqual(output.read_bytes(), payload)

        inline_sentence = (
            "■ **Another initial condition.** Inserting a single "
            "![black cell](_page_885_inline_black_cell.jpeg) in a background "
            "of ![striped black-to-white block]"
            "(_page_885_inline_black_gradient_white_block.jpeg) blocks in "
            "rule 90 yields the pattern below"
        )
        self.assertEqual(self.rendered.count(inline_sentence), 1)
        self.assertNotIn("single ■ in a background of ▥ blocks", self.rendered)

    def test_source_emphasis_and_math_variable_styles_are_exact(self) -> None:
        bold_italic_leads = (
            "Complete pattern.",
            "Center column.",
            "Architecture.",
            "Textile making.",
            "Rope.",
            "Knots and string figures.",
            "Paperfolding.",
            "Mathematics.",
            "Logic.",
            "Grammar.",
            "Poetry.",
            "Music.",
            "Military drill.",
            "Games.",
            "Puzzles.",
            "Cryptography.",
            "Maze designs.",
            "Rule-based pictures.",
        )
        self.assertEqual(
            re.findall(r"(?m)^\*\*\*(.+?\.)\*\*\*", self.rendered),
            list(bold_italic_leads),
        )
        self.assertEqual(self.rendered.count("Some examples include:\n"), 1)
        self.assertNotIn("**Some examples include:**", self.rendered)

        for source_style in (
            "into *n* - 2 of the *n* array elements",
            "popularization in *Scientific American* by Martin Gardner",
            "code 20 *k* = 2, *r* = 2 totalistic rule",
            "The 3 *n* + 1 problem",
            "all the *k* = 2, *r* = 1 cellular automata",
            "rule 110 and *k* = 2, *r* = 2 totalistic code 10",
            "occur in *k* = 2, *r* = 2 totalistic rules",
        ):
            with self.subTest(source_style=source_style):
                self.assertEqual(self.rendered.count(source_style), 1)

    def test_technical_repairs_and_visible_source_forms_are_exact(self) -> None:
        exact_once = (
            "Show[CAGraphics[CAEvolveList[\n"
            " ElementaryRule[30], CenterList[103], 50]]]",
            "tp = ap[0];\n"
            "            ap[0] = revrule[ap[1]+2*(tp + 2*t)];\n"
            "            t = tp;\n"
            "        }\n"
            "    }\n"
            "    MLPutIntegerList(stdlink, a, n);\n"
            "}",
            ":Arguments: {Reverse[rule], a, steps}\n"
            ":ArgumentTypes: {IntegerList, IntegerList, Integer}\n"
            ":ReturnType: Manual\n"
            ":End:",
            "{{1, 1, 1} -> 0, {1, 1, 0} -> 0, "
            "{1, 0, 1} -> 0, {1, 0, 0} -> 1,\n"
            " {0, 1, 1} -> 1, {0, 1, 0} -> 1, "
            "{0, 0, 1} -> 1, {0, 0, 0} -> 0}",
            "Mod[Binomial[t, (n + t)/2], 2] /; EvenQ[n + t]",
            "a block of *n* adjacent white cells "
            "(corresponding to a row in a white triangle) seems quite "
            "accurately to approach `2^-n`",
            "three levels of nesting as shown here are rare.",
            "combining ◣, ◥, ◤, ◢ in various possible ways.",
        )
        for specimen in exact_once:
            with self.subTest(specimen=specimen[:80]):
                self.assertEqual(self.rendered.count(specimen), 1)

        self.assertNotIn(
            "ElementaryRule[30], CenterList[103], 50]]]]", self.rendered
        )
        self.assertNotIn("AII", self.rendered)
        for source_form in (
            "tries to updates",
            "there functions",
            "The runs",
            "I would amazed",
            "architectural ornamental",
            "laserprinter",
            "(See page 1021).",
        ):
            with self.subTest(source_form=source_form):
                self.assertIn(source_form, self.rendered)

    def test_intentionally_malformed_source_braces_are_preserved(self) -> None:
        malformed = (
            "{{{{a11, a12, ...}, off1}, {a21, ...}, off2}, ...}, bspec}"
        )
        silently_repaired = (
            "{{{{a11, a12, ...}, off1}, "
            "{{a21, ...}, off2}, ...}, bspec}"
        )
        self.assertEqual(self.rendered.count(malformed), 1)
        self.assertEqual(malformed.count("{"), 5)
        self.assertEqual(malformed.count("}"), 6)
        self.assertNotIn(silently_repaired, self.rendered)

        # These three visibly printed groupings likewise must not be
        # normalized according to presumed modern CellularAutomaton syntax.
        for source_row in (
            "{n, {k, {{0, 1, 0}, {1, 1, 1}, {0, 1, 0}}, {1, 1}}}",
            "{n, {k, {{0, k, 0}, {k, 1, k}, {0, k, 0}}, {1, 1}}}",
            "{n + k^5 (k - 1), {k, {{0, 1, 0}, "
            "{1, 4 k + 1, 1}, {0, 1, 0}}, {1, 1}}}",
        ):
            with self.subTest(source_row=source_row[:60]):
                self.assertEqual(self.rendered.count(source_row), 1)


if __name__ == "__main__":
    unittest.main()
