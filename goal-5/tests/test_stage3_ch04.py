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


class ChapterFourTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.document = next(row for row in cls.documents if row["id"] == "CH04")
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

    @staticmethod
    def matrix_html(rows: tuple[tuple[str, ...], ...]) -> str:
        body = "\n".join(
            "    <tr>" + "".join(f"<td>{value}</td>" for value in row) + "</tr>"
            for row in rows
        )
        return f"<table>\n  <tbody>\n{body}\n  </tbody>\n</table>"

    def test_range_and_first_pass_corrections_are_exact(self) -> None:
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
                1368,
                2141,
                199880,
                355646,
                774,
                155766,
                "3e556da45a36b8c8792f8ae1f790baec5220d79e25802a05b73b465c5fd0ffb1",
                131,
                184,
                "115",
                "168",
            ),
        )
        relevant = [
            row for row in self.corrections if row["document_id"] == "CH04"
        ]
        self.assertEqual(len(relevant), 110)
        self.assertEqual(
            [row["id"] for row in relevant],
            [f"G5-C-{number:04d}" for number in range(194, 304)],
        )
        self.assertEqual(sum(row["expected_count"] for row in relevant), 112)
        self.assertEqual(
            {
                row["id"]: row["expected_count"]
                for row in relevant
                if row["expected_count"] != 1
            },
            {"G5-C-0295": 2, "G5-C-0298": 2},
        )
        self.assertTrue(
            all(row["verification_status"] == "SOURCE_VERIFIED" for row in relevant)
        )
        self.assertTrue(all(row["reviewer_type"] == "agent" for row in relevant))
        self.assertTrue(
            all(
                131
                <= int(re.match(r"pdf:(\d{4})", row["authoritative_location"])[1])
                <= 184
                for row in relevant
            )
        )
        self.assertEqual(
            {
                row["id"]: row["authoritative_location"]
                for row in relevant
                if row["id"] in {"G5-C-0195", "G5-C-0274", "G5-C-0293", "G5-C-0302"}
            },
            {
                "G5-C-0195": "pdf:0132",
                "G5-C-0274": "pdf:0169",
                "G5-C-0293": "pdf:0180",
                "G5-C-0302": "pdf:0183",
            },
        )
        self.assertTrue(
            all(
                self.document["raw_start_byte"]
                <= row["raw_start_byte"]
                < self.document["raw_end_byte_exclusive"]
                for row in relevant
            )
        )

    def test_heading_hierarchy_and_page_furniture_are_restored(self) -> None:
        self.assertTrue(
            self.rendered.startswith(
                "![](_page_130_Chapter_Opener.jpeg)\n\n"
                "## Systems Based on Numbers\n\n"
                "### The Notion of Numbers\n\n"
            )
        )
        headings = (
            "The Notion of Numbers",
            "Elementary Arithmetic",
            "Recursive Sequences",
            "The Sequence of Primes",
            "Mathematical Constants",
            "Mathematical Functions",
            "Iterated Maps and the Chaos Phenomenon",
            "Continuous Cellular Automata",
            "Partial Differential Equations",
            "Continuous Versus Discrete Systems",
        )
        self.assertEqual(self.rendered.count("\n### "), len(headings))
        for heading in headings:
            self.assertEqual(self.rendered.count(f"### {heading}"), 1)
        self.assertNotIn("####", self.rendered)
        self.assertNotIn("### **", self.rendered)
        self.assertNotRegex(self.rendered, r"(?m)^# 4$")
        self.assertNotIn("STEPHEN WOLFRAM A NEW KIND OF SCIENCE", self.rendered)
        self.assertNotIn("\nSCIENCE\n", self.rendered)

    def test_all_live_tables_are_balanced_headerless_and_complete(self) -> None:
        tables = re.findall(r"<table>\n(.*?)\n</table>", self.rendered, re.DOTALL)
        self.assertEqual(len(tables), 11)
        self.assertEqual(self.rendered.count("<table>"), 11)
        self.assertEqual(self.rendered.count("</table>"), 11)
        self.assertEqual(self.rendered.count("<tbody>"), 11)
        self.assertEqual(self.rendered.count("</tbody>"), 11)
        self.assertEqual(self.rendered.count("<tr>"), 91)
        self.assertEqual(self.rendered.count("</tr>"), 91)
        self.assertEqual(self.rendered.count("<td>"), 289)
        self.assertEqual(self.rendered.count("</td>"), 289)
        self.assertEqual(
            [table.count("<tr>") for table in tables],
            [9, 5, 5, 8, 8, 8, 8, 22, 6, 6, 6],
        )
        for table in tables:
            self.assertEqual(table.count("<tbody>"), 1)
            self.assertEqual(table.count("</tbody>"), 1)
            self.assertEqual(table.count("<tr>"), table.count("</tr>"))
            self.assertEqual(table.count("<td>"), table.count("</td>"))
            self.assertNotIn("<thead", table)
            self.assertNotIn("<th", table)
        self.assertNotRegex(self.rendered, r"(?m)^\|")
        self.assertNotIn("```", self.rendered)

    def test_high_risk_table_and_formula_tokens_match_the_source(self) -> None:
        expected = (
            (
                r"<tr><td>\(3829 = 1 \times 3125 + 1 \times 625 + 0 \times "
                r"125 + 3 \times 25 + 0 \times 5 + 4 \times 1\)</td><td>110304"
                r"</td><td>(base 5)</td></tr>"
            ),
            (
                r"<tr><td>\(3829 = 1 \times 2048 + 1 \times 1024 + 1 \times "
                r"512 + 0 \times 256 + 1 \times 128 + 1 \times 64 + 1 \times "
                r"32 + 1 \times 16 + 0 \times 8 + 1 \times 4 + 0 \times 2 + "
                r"1 \times 1\)</td><td>111011110101</td><td>(base 2)</td></tr>"
            ),
            (
                r"\(1/81 = 0.000000110010100100010110000111111001101011011101001111"
                r"000000110010100100010110000\ldots\)"
            ),
            (
                r"\(\sqrt{11} = 11.010100010000111001010010011111111010110111100110"
                r"10000010110100011101111001001001\ldots\)"
            ),
            (
                r"\(\operatorname{Log}[2] = 0.101100010111001000010111111101111101000111"
                r"00111101111001101010111100100111100011101100111001100000000011111100"
                r"\ldots\)"
            ),
            (
                r"\(\sqrt[3]{2} = \{1, 3, 1, 5, 1, 1, 4, 1, 1, 8, 1, 14, 1, "
                r"10, 2, 1, 4, 12, 2, 3, 2, 1, 3, 4, 1, 1, 2, 14, 3, 12, 1, 15, "
                r"3, 1, 4, 534, 1, 1, 5, 1, 1, 121, 1, 2, 2, 4, 10, 3, 2, 2, "
                r"\ldots\}\)"
            ),
            (
                r"\(\pi = \{3, 7, 15, 1, 292, 1, 1, 1, 2, 1, 3, 1, 14, 2, 1, "
                r"1, 2, 2, 2, 2, 1, 84, 2, 1, 1, 15, 3, 13, 1, 4, 2, 6, 6, 99, "
                r"1, 2, 2, 6, 3, 5, 1, 1, 6, 8, 1, 7, 1, 2, 3, 7, 1, 2, "
                r"\ldots\}\)"
            ),
            (
                r"\(\operatorname{Sinh}[1] = \{1, 5, 1, 2, 2, 2, 1, 2, 7, 5, "
                r"1, 1, 1, 2, 2, 19, 1, 2, 1, 7, 1, 1, 9, 1, 3, 1, 1, 2, 1, "
                r"1, 1, 1, 1, 3, 1, 2, 4, 5, 3, 5, 1, 3, 1, 1, 1, 2, 7, 1, 9, "
                r"1, 1, 2, 1, 21, 1, \ldots\}\)"
            ),
            (
                r"\(\operatorname{Tanh}[1] = \{0, 1, 3, 5, 7, 9, 11, 13, 15, "
                r"17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, "
                r"47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, "
                r"\ldots\}\)"
            ),
            (
                r"$$3.141592653\ldots = 3 + \frac{1}{10}\left(1 + \frac{1}{10}"
                r"\left(4 + \frac{1}{10}\left(1 + \frac{1}{10}\left(5 + "
                r"\frac{1}{10}\left(9 + \frac{1}{10}\left(2 + \frac{1}{10}"
                r"\left(6 + \frac{1}{10}\left(5 + \frac{1}{10}\left(3 + "
                r"\ldots\right)\right)\right)\right)\right)\right)\right)\right)"
                r"\right)$$"
            ),
            (
                r"$$11.001001000\ldots = 2 + 1 + \frac{1}{2}\left(0 + "
                r"\frac{1}{2}\left(0 + \frac{1}{2}\left(1 + \frac{1}{2}"
                r"\left(0 + \frac{1}{2}\left(0 + \frac{1}{2}\left(1 + "
                r"\frac{1}{2}\left(0 + \frac{1}{2}\left(0 + \frac{1}{2}"
                r"\left(0 + \ldots\right)\right)\right)\right)\right)\right)"
                r"\right)\right)\right)$$"
            ),
            (
                r"$$3 + \frac{1}{7 + \frac{1}{15 + \frac{1}{1 + \frac{1}{292 + "
                r"\frac{1}{1 + \frac{1}{1 + \frac{1}{1 + \frac{1}{2 + "
                r"\frac{1}{1 + \frac{1}{3 + \frac{1}{1 + \frac{1}{14 + "
                r"\ldots}}}}}}}}}}}}$$"
            ),
            (
                r"$$\{3, 7, 15, 1, 292, 1, 1, 1, 2, 1, 3, 1, 14, 2, 1, 1, "
                r"2, 2, 2, 2, 1, 84, 2, 1, 1, 15, 3, 13, 1, 4, 2, 6, 6, 99, "
                r"1, 2, 2, 6, 3, 5, 1, \ldots\}$$"
            ),
            r"$n \rightarrow If[EvenQ[n], 3\,n/2, 3\,(n+1)/2]$",
            r"$FractionalPart[x+1/4]$",
            (
                "determine the overall form of behavior produced in each case. "
                "<sup>▶</sup>"
            ),
        )
        for token in expected:
            with self.subTest(token=token[:80]):
                self.assertIn(token, self.rendered)

        equations = (
            r"*diffusion equation:* $\partial_t u[t,x] = 1/4\,\partial_{xx}u[t,x]$",
            r"*wave equation:* $\partial_{tt}u[t,x] = \partial_{xx}u[t,x]$",
            (
                r"*sine-Gordon soliton equation:* $\partial_{tt}u[t,x] = "
                r"\partial_{xx}u[t,x] + Sin[u[t,x]]$"
            ),
            (
                r"$\partial_{tt}u[t,x] = \partial_{xx}u[t,x] + "
                r"(1-u[t,x]^2)(1+u[t,x])$"
            ),
            (
                r"$\partial_{tt}u[t,x] = \partial_{xx}u[t,x] + "
                r"(1-u[t,x]^2)(1+2u[t,x])$"
            ),
            (
                r"$\partial_{tt}u[t,x] = \partial_{xx}u[t,x] + "
                r"(1-u[t,x]^2)(1+4u[t,x])$"
            ),
        )
        for equation in equations[:3]:
            self.assertEqual(self.rendered.count(equation), 1)
        for equation in equations[3:]:
            self.assertEqual(self.rendered.count(equation), 2)
        self.assertIn(
            r"the initial conditions used are $u=e^{-x^2}$, $\partial_t u=0$.",
            self.rendered,
        )
        self.assertNotIn(r"\partial_r", self.rendered)

    def test_all_three_continuous_cellular_automaton_matrices_are_exact(self) -> None:
        matrices = (
            (
                ("0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "0"),
                ("0", "0", "0", "0", "0.333", "0.333", "0.333", "0", "0", "0", "0"),
                ("0", "0", "0", "0.111", "0.222", "0.333", "0.222", "0.111", "0", "0", "0"),
                ("0", "0", "0.037", "0.111", "0.222", "0.259", "0.222", "0.111", "0.037", "0", "0"),
                ("0", "0.012", "0.049", "0.123", "0.198", "0.235", "0.198", "0.123", "0.049", "0.012", "0"),
                ("0.004", "0.021", "0.062", "0.123", "0.185", "0.21", "0.185", "0.123", "0.062", "0.021", "0.004"),
            ),
            (
                ("0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "0"),
                ("0", "0", "0", "0", "0.5", "0.5", "0.5", "0", "0", "0", "0"),
                ("0", "0", "0", "0.25", "0.5", "0.75", "0.5", "0.25", "0", "0", "0"),
                ("0", "0", "0.125", "0.375", "0.75", "0.875", "0.75", "0.375", "0.125", "0", "0"),
                ("0", "0.063", "0.25", "0.625", "0", "0.188", "0", "0.625", "0.25", "0.063", "0"),
                ("0.031", "0.156", "0.469", "0.438", "0.406", "0.094", "0.406", "0.438", "0.469", "0.156", "0.031"),
            ),
            (
                ("0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "0"),
                ("0.25", "0.25", "0.25", "0.25", "0.583", "0.583", "0.583", "0.25", "0.25", "0.25", "0.25"),
                ("0.5", "0.5", "0.5", "0.611", "0.722", "0.833", "0.722", "0.611", "0.5", "0.5", "0.5"),
                ("0.75", "0.75", "0.787", "0.861", "0.972", "0.009", "0.972", "0.861", "0.787", "0.75", "0.75"),
                ("0", "0.012", "0.049", "0.123", "0.864", "0.901", "0.864", "0.123", "0.049", "0.012", "0"),
                ("0.254", "0.271", "0.312", "0.596", "0.88", "0.127", "0.88", "0.596", "0.312", "0.271", "0.254"),
            ),
        )
        for number, matrix in enumerate(matrices, start=1):
            with self.subTest(matrix=number):
                self.assertEqual(len(matrix), 6)
                self.assertTrue(all(len(row) == 11 for row in matrix))
                self.assertEqual(self.rendered.count(self.matrix_html(matrix)), 1)

    def test_page_turns_and_compound_figure_captions_are_serialized(self) -> None:
        joined_fragments = (
            "there are 10 possible choices: 0 through 9. But as the picture",
            "no nested digit sequences ever occur",
            "essentially the same for all numbers. If one does this",
            "purely repetitive, making the generated pattern nested",
            "for a while these digits are what is important",
            "But traditional mathematical methods give very little guidance",
            "there was no possibility of dismissing what I saw",
        )
        for fragment in joined_fragments:
            self.assertIn(fragment, self.rendered)
        false_splits = (
            "choices:\n\n0 through 9",
            "nested digit sequences\n\never occur",
            "same for\n\nall numbers",
            "purely repetitive,\n\nmaking",
            "these digits are\n\nwhat is important",
            "But traditional\n\nmathematical methods",
            "there was no\n\npossibility",
        )
        for fragment in false_splits:
            self.assertNotIn(fragment, self.rendered)

        self.assert_order(
            "there are 10 possible choices: 0 through 9. But as the picture",
            r"\(3829 = 3 \times 1000 + 8 \times 100 + 2 \times 10 + 9 \times 1\)",
            "Representations of the number 3829 in various bases.",
            "So what this means is that in a computer numbers are represented",
        )
        self.assert_order(
            "The result of this process is to generate the successive numbers",
            "![](_page_132_Figure_10_Overview.jpeg)",
            "![](_page_132_Figure_10.jpeg)",
            "Digit sequences of successive numbers written in base 2.",
            "The pictures below show what happens if one adds a number other than 1",
        )
        self.assert_order(
            "As a first example, consider a slight variation on the operation",
            "![](_page_137_Digit_Matrix.jpeg)",
            "![](_page_137_Picture_7.jpeg)",
            "Results of starting with the number 1, then applying the following rule:",
            "This procedure is always guaranteed to give a whole number.",
        )
        self.assert_order(
            "![](_page_151_Figure_7.jpeg)",
            r"A pictorial representation of the first 20,000 digits of $\pi$ in base 2.",
            "![](_page_152_Pi_Digits.jpeg)",
            r"The first 4000 digits of $\pi$ in bases 10 and 2.",
            "In no case are there any obvious regularities.",
        )
        self.assert_order(
            "![](_page_165_Figure_1.jpeg)",
            "Examples of iterated maps starting from simple initial conditions.",
            "![](_page_166_Figure_2.jpeg)",
            "The same iterated maps as on the facing page, but now started",
            "This is very different from what happens in cases (a) and (b).",
        )
        self.assert_order(
            "![](_page_178_Picture_2.jpeg)",
            "![](_page_178_Picture_3.jpeg)",
            "*diffusion equation:*",
            "![](_page_178_Picture_5.jpeg)",
            "![](_page_178_Picture_6.jpeg)",
            "*wave equation:*",
            "![](_page_178_Picture_8.jpeg)",
            "![](_page_178_Picture_9.jpeg)",
            "*sine-Gordon soliton equation:*",
            "Three partial differential equations that have historically been studied",
            "But an immediate difficulty is that there is no obvious way to sample",
        )
        self.assert_order(
            "![](_page_180_Picture_2.jpeg)",
            "![](_page_180_Picture_3.jpeg)",
            "![](_page_180_Picture_5.jpeg)",
            "![](_page_180_Picture_6.jpeg)",
            "![](_page_180_Picture_8.jpeg)",
            "![](_page_180_Picture_9.jpeg)",
            "Examples of partial differential equations I have found",
            "![](_page_181_Picture_2.jpeg)",
            "![](_page_181_Picture_4.jpeg)",
            "![](_page_181_Picture_6.jpeg)",
            "<sup>◀</sup> Solutions to the same equations",
            "### Continuous Versus Discrete Systems",
        )

    def test_known_ocr_and_layout_debris_is_absent(self) -> None:
        debris = (
            "| c | т | F | Р | н |",
            "B29 =<br>",
            "\n.38\n",
            "base s digits of s digits of s",
            "#### STEPHEN WOLFRAM A NEW KIND OF SCIENCE",
            "\n> all numbers.",
            "\n> And from this it seems",
            "<sup>◆</sup>",
            r"\partial_r u",
            "￥",
        )
        for fragment in debris:
            self.assertNotIn(fragment, self.rendered)
        self.assertNotIn(
            "3.141592653589793238462643383279502884197169399375105820974944592",
            self.rendered,
        )
        self.assertNotIn(
            "11.0010010000111111011010101000100010000.101101011110100011001101",
            self.rendered,
        )

    def test_source_added_and_repaired_assets_are_pinned_and_ordered(self) -> None:
        chapter_images = [row for row in self.images if row["document_id"] == "CH04"]
        self.assertEqual(len(chapter_images), 59)
        self.assertEqual(
            [row["ordinal"] for row in chapter_images], list(range(110, 169))
        )
        self.assertEqual(
            {row["ordinal"] for row in chapter_images if row["split_status"] == "OMITTED"},
            {134, 135},
        )

        chapter_added = [
            row for row in self.added_assets if row["document_id"] == "CH04"
        ]
        expected_added = {
            "G5-A-0005": (
                "fbc194fef8dd8094f771f49cc3ba99b7b42b6a2803180aa88f35772477c56303",
                (266, 342),
            ),
            "G5-A-0006": (
                "eb7f88f8a20b329ce262df9c6d7cd29addea6b946fac7154762a634692593513",
                (61, 1273),
            ),
            "G5-A-0007": (
                "0fa01ed522477dd5eca36845e9077b3fbc9d1c7c43bf65a2a33846e9f56bece7",
                (584, 296),
            ),
            "G5-A-0008": (
                "199075592a9392a796724234bab78703dacb2412f42a528fbb7d8ffd782136c3",
                (1059, 1212),
            ),
        }
        self.assertEqual([row["id"] for row in chapter_added], list(expected_added))
        added_names: dict[str, str] = {}
        for row in chapter_added:
            digest, dimensions = expected_added[row["id"]]
            with self.subTest(added=row["id"]):
                source = build.REPO_ROOT / Path(row["asset_relative_path"])
                output = build.OUTPUT_ROOT / Path(self.path).parent / source.name
                payload = source.read_bytes()
                added_names[row["id"]] = source.name
                self.assertEqual(row["asset_sha256"], digest)
                self.assertEqual(build.sha256(payload), digest)
                self.assertEqual(build.jpeg_dimensions(payload), dimensions)
                self.assertEqual((row["width_px"], row["height_px"]), dimensions)
                self.assertEqual(output.read_bytes(), payload)

        repaired_rows = [
            row for row in chapter_images if "repaired_asset_relative_path" in row
        ]
        self.assertEqual([row["ordinal"] for row in repaired_rows], [141])
        repaired = repaired_rows[0]
        self.assertEqual(
            (
                repaired["repaired_asset_sha256"],
                repaired["repaired_width_px"],
                repaired["repaired_height_px"],
            ),
            (
                "c64ffe6bfbc61fc16b44f04affd6ab7695e285d0b22990a62e1c27e44c5dd10b",
                1040,
                992,
            ),
        )
        legacy = build.LEGACY_ROOT / Path(repaired["asset_relative_path"])
        repaired_source = build.REPO_ROOT / Path(
            repaired["repaired_asset_relative_path"]
        )
        output = build.OUTPUT_ROOT / Path(self.path).parent / legacy.name
        repaired_payload = repaired_source.read_bytes()
        self.assertEqual(
            build.sha256(repaired_payload), repaired["repaired_asset_sha256"]
        )
        self.assertEqual(build.jpeg_dimensions(repaired_payload), (1040, 992))
        self.assertNotEqual(repaired_payload, legacy.read_bytes())
        self.assertEqual(output.read_bytes(), repaired_payload)

        mapped_names = {
            row["ordinal"]: Path(row["asset_relative_path"]).name
            for row in chapter_images
        }
        expected_references = (
            [added_names["G5-A-0005"], added_names["G5-A-0006"]]
            + [mapped_names[number] for number in range(110, 117)]
            + [added_names["G5-A-0007"]]
            + [mapped_names[number] for number in range(117, 134)]
            + [added_names["G5-A-0008"]]
            + [mapped_names[number] for number in range(134, 169)]
        )
        references = re.findall(r"!\[\]\(([^)]+\.jpeg)\)", self.rendered)
        self.assertEqual(len(references), 63)
        self.assertEqual(len(set(references)), 63)
        self.assertEqual(references, expected_references)

        changed_hash = copy.deepcopy(self.images)
        changed = next(row for row in changed_hash if row["ordinal"] == 141)
        changed["repaired_asset_sha256"] = "0" * 64
        with self.assertRaises(build.BuildError):
            build.validate_images(self.raw, self.documents, changed_hash)
        missing_reason = copy.deepcopy(self.added_assets)
        changed_added = next(row for row in missing_reason if row["id"] == "G5-A-0008")
        changed_added.pop("reason")
        with self.assertRaises(build.BuildError):
            build.validate_added_assets(self.documents, self.images, missing_reason)

    def test_coverage_remains_open_for_independent_review(self) -> None:
        rows = validate.validate_coverage(self.documents)
        chapter = next(row for row in rows if row["document_id"] == "CH04")
        self.assertEqual(
            (chapter["first_pass"], chapter["second_pass"]), ("YES", "NO")
        )


if __name__ == "__main__":
    unittest.main()
