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


EXPECTED_SHA256 = "897cae5d2988c0e4d746aad431cffc411a81d2766e057d184f2c47f718755007"
EXPECTED_BYTES = 82_769
EXPECTED_LINES = 867
EXPECTED_CORRECTIONS_SHA256 = (
    "c23edfcdc7d11d1ca4cf25a1166bcd10d3e5c4aadf45b5f6a60638755aae2bdd"
)
EXPECTED_IMAGE_ROWS_SHA256 = (
    "79505d4c9f3befe5b96441a5e010d05fcb75ebcb5f99631ed470646845eabdfe"
)
EXPECTED_ADDED_ROWS_SHA256 = (
    "086c1a1c1787b6ef1638620b6ab5367242eb73dda7e4033b0fe5b70a31bab9b7"
)
EXPECTED_MAIN_LABELS_SHA256 = (
    "887aaed659ba6b1156452680663fc15ea33b1939b06bba2bd7c2906ee4bc509c"
)
EXPECTED_HEADINGS_SHA256 = (
    "fa40d0d874acdbc7b593fb71adb38ffd7db6a9ba5847391912cd04183e6ab414"
)
EXPECTED_MAPPED_NAMES_SHA256 = (
    "7c2ed6cca81deb3f9c7d9366dd81fd8579f9ee40d6bcb803abcdb29687afde7a"
)
EXPECTED_RETAINED_REFERENCES_SHA256 = (
    "d189803161cda7aea73566d4ea88ef708c0676183359f37328eeafb0d5af5af7"
)
EXPECTED_ALL_REFERENCES_SHA256 = (
    "ecf550c89305e511bb38fe4d34c64eb044af19bcbf84d045c1f8b31e1865cc03"
)
EXPECTED_EMPHASIS_COUNTS = {
    "BOLD": 96,
    "BOLD_ITALIC": 0,
    "ITALIC_NESTED_IN_BOLD": 0,
    "ITALIC": 162,
}

# ordinal: (basename, repaired digest, dimensions)
EXPECTED_REPAIRS = {
    914: (
        "_page_913_Picture_8.jpeg",
        "628575ed404f9e6946fc004b0c5d99960977b52365094465337fd8bed3cf8ab0",
        (408, 222),
    ),
    915: (
        "_page_913_Picture_9.jpeg",
        "e330316cb9781c070f3da53aa1a4146f232dd6d79eebb5755838b26ea3898277",
        (408, 222),
    ),
    916: (
        "_page_913_Picture_10.jpeg",
        "52b68a37ba15c0b2a797ec1dc7a28bb05ceeec76275f172b116b9e8b3cc4e574",
        (408, 222),
    ),
    917: (
        "_page_913_Picture_11.jpeg",
        "df33c9f0d00ee279585b8a708770beaaec7a90cea60eeda35ef4a29f4a411a5c",
        (408, 222),
    ),
}

# asset id: (basename, digest, dimensions, bytes, canonical PDF page)
EXPECTED_ADDED = {
    "G5-A-0044": (
        "_page_904_busy_beaver_2_3_4_state_rules.jpeg",
        "0d68816552ccc8411015066f174b2c949ac3235d8f3c8d654023ba0063a9df10",
        (520, 48),
        9_590,
        905,
    ),
    "G5-A-0045": (
        "_page_904_busy_beaver_5_state_rule.jpeg",
        "c5056019f2e46743c213c169115fb23ebd31820e809d77b404a0e5d770a1a532",
        (425, 52),
        5_663,
        905,
    ),
    "G5-A-0046": (
        "_page_906_golden_ratio_rectangle.jpeg",
        "df3fbefb0c73072e67d51128740c17f6e8d961428733d85cb2945f210c37a1eb",
        (22, 22),
        284,
        907,
    ),
    "G5-A-0047": (
        "_page_907_rule_b_path_evolution.jpeg",
        "9a241506acce41bd966cf6decec3cadb114055e6bb2c95095b59f4f4612b8ecf",
        (408, 145),
        14_100,
        908,
    ),
    "G5-A-0048": (
        "_page_910_cyclic_tag_trough.jpeg",
        "6033f545fd714b37508ae0b58ace40575efaed71c3c83485acc2121b524d9473",
        (385, 34),
        6_194,
        911,
    ),
    "G5-A-0049": (
        "_page_911_symbolic_representation_table.jpeg",
        "7918291950df26d248d8eafe42caadd7e50e2bc478ab7b7ba81bfe1c4da3e8df",
        (525, 199),
        29_919,
        912,
    ),
}


class BooleanParser:
    def __init__(self, source: str, values: dict[str, bool]) -> None:
        self.tokens = re.findall(r"[pqr01]|[()¬∧∨⊻]", source)
        self.index = 0
        self.values = values

    def take(self, token: str) -> bool:
        if self.index < len(self.tokens) and self.tokens[self.index] == token:
            self.index += 1
            return True
        return False

    def unary(self) -> bool:
        if self.take("¬"):
            return not self.unary()
        if self.take("("):
            value = self.or_()
            if not self.take(")"):
                raise AssertionError("unclosed Boolean group")
            return value
        token = self.tokens[self.index]
        self.index += 1
        if token in "01":
            return token == "1"
        return self.values[token]

    def and_(self) -> bool:
        value = self.unary()
        while self.take("∧"):
            right = self.unary()
            value = value and right
        return value

    def xor(self) -> bool:
        value = self.and_()
        while self.take("⊻"):
            value = value != self.and_()
        return value

    def or_(self) -> bool:
        value = self.xor()
        while self.take("∨"):
            right = self.xor()
            value = value or right
        return value

    def parse(self) -> bool:
        value = self.or_()
        if self.index != len(self.tokens):
            raise AssertionError("unconsumed Boolean tokens")
        return value


class NotesForChapter3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.document = next(row for row in cls.documents if row["id"] == "N03")
        cls.path = build.safe_relative_path(cls.document["output_path"], suffix=".md")
        cls.rendered_bytes = build.document_bytes(
            cls.raw, cls.documents, cls.corrections
        )[cls.path]
        cls.rendered = cls.rendered_bytes.decode("utf-8")
        cls.output_path = build.OUTPUT_ROOT / Path(cls.path)
        cls.n03_corrections = [
            row for row in cls.corrections if row["document_id"] == "N03"
        ]
        cls.n03_images = [
            row for row in cls.images if row["document_id"] == "N03"
        ]
        cls.n03_added = [
            row for row in cls.added_assets if row["document_id"] == "N03"
        ]
        cls.n04_document = next(
            row for row in cls.documents if row["id"] == "N04"
        )
        cls.n04_images = [
            row for row in cls.images if row["document_id"] == "N04"
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

    @staticmethod
    def sequence_sha256(items: list[str]) -> str:
        return build.sha256(("\n".join(items) + "\n").encode("utf-8"))

    @staticmethod
    def emphasis_counts(markdown: str) -> dict[str, int]:
        visible = re.sub(r"(?ms)^```[^\n]*\n.*?^```$", " ", markdown)
        visible = re.sub(r"(?<!`)`[^`\n]+`(?!`)", " ", visible)
        visible = re.sub(r"(?<!\\)\$[^$\n]+(?<!\\)\$", " ", visible)
        visible = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", visible)
        if "_" in visible:
            raise AssertionError("unexpected underscore-form emphasis")

        triples = list(re.finditer(r"\*\*\*(.+?)\*\*\*", visible))
        without_triples = re.sub(r"\*\*\*(.+?)\*\*\*", " ", visible)
        bold = list(re.finditer(r"\*\*(.+?)\*\*", without_triples))
        nested = sum(
            len(re.findall(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", match.group(1)))
            for match in bold
        )
        without_bold = re.sub(r"\*\*(.+?)\*\*", " ", without_triples)
        italic = list(
            re.finditer(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", without_bold)
        )
        return {
            "BOLD": len(bold),
            "BOLD_ITALIC": len(triples),
            "ITALIC_NESTED_IN_BOLD": nested,
            "ITALIC": len(italic),
        }

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
                11631,
                12498,
                1703015,
                1792864,
                868,
                89849,
                "b412e36c234f3def3237475d70a0336cf89d09f6f71d3ef66656a51082333484",
                899,
                916,
                "883",
                "900",
            ),
        )
        segment = self.raw[1703015:1792864]
        self.assertEqual(len(segment), 89849)
        self.assertEqual(build.sha256(segment), self.document["raw_segment_sha256"])

        self.assertEqual(len(self.n03_corrections), 25)
        self.assertEqual(
            [row["id"] for row in self.n03_corrections],
            [f"G5-C-{number:04d}" for number in range(949, 974)],
        )
        self.assertEqual(
            self.rows_sha256(self.n03_corrections),
            EXPECTED_CORRECTIONS_SHA256,
        )
        self.assertEqual(len({row["before"] for row in self.n03_corrections}), 25)

        previous_end = self.document["raw_start_byte"]
        for row in sorted(
            self.n03_corrections, key=lambda item: item["raw_start_byte"]
        ):
            with self.subTest(correction=row["id"]):
                self.assertEqual(set(row), build.CORRECTION_FIELDS | {"raw_line"})
                self.assertEqual(row["document_id"], "N03")
                self.assertEqual(row["expected_count"], 1)
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                self.assertTrue(row["reason"].strip())

                start = row["raw_start_byte"]
                before = row["before"].encode("utf-8")
                end = start + len(before)
                local = start - self.document["raw_start_byte"]
                self.assertGreaterEqual(start, previous_end)
                self.assertLessEqual(end, self.document["raw_end_byte_exclusive"])
                self.assertEqual(self.raw[start:end], before)
                self.assertEqual(segment.count(before), 1)
                self.assertEqual(
                    row["raw_line"],
                    self.document["raw_start_line"]
                    + segment[:local].count(b"\n"),
                )
                pages = [
                    int(value)
                    for value in re.findall(
                        r"pdf:(\d{4})", row["authoritative_location"]
                    )
                ]
                self.assertTrue(pages)
                self.assertTrue(all(899 <= page <= 916 for page in pages))
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

    def test_heading_note_and_markup_inventory_is_exact(self) -> None:
        headings = re.findall(r"(?m)^#{2,3} .+$", self.rendered)
        self.assertEqual(
            headings,
            [
                "## The World of Simple Programs",
                "### More Cellular Automata",
                "### Mobile Automata",
                "### Turing Machines",
                "### Substitution Systems",
                "### Sequential Substitution Systems",
                "### Tag Systems",
                "### Cyclic Tag Systems",
                "### Register Machines",
                "### Symbolic Systems",
                "### How the Discoveries in This Chapter Were Made",
            ],
        )
        self.assertEqual(self.sequence_sha256(headings), EXPECTED_HEADINGS_SHA256)
        labels = re.findall(r"(?m)^■ \*\*(.+?)\*\*", self.rendered)
        self.assertEqual(len(labels), 83)
        self.assertEqual(
            self.sequence_sha256(labels), EXPECTED_MAIN_LABELS_SHA256
        )
        self.assertEqual(len(re.findall(r"(?m)^▪ ", self.rendered)), 39)
        self.assertEqual(self.rendered.count("```"), 104)
        self.assertEqual(
            len(re.findall(r"(?<!`)`[^`\n]+`(?!`)", self.rendered)), 298
        )
        self.assertEqual(
            len(re.findall(r"(?<!\\)\$[^$\n]+(?<!\\)\$", self.rendered)),
            1,
        )
        emphasis = self.emphasis_counts(self.rendered)
        self.assertEqual(emphasis, EXPECTED_EMPHASIS_COUNTS)
        self.assertEqual(sum(emphasis.values()), 258)
        self.assertNotIn("####", self.rendered)

    def test_mapped_inventory_false_positive_and_order_are_exact(self) -> None:
        self.assertEqual(len(self.n03_images), 40)
        self.assertEqual(
            [row["ordinal"] for row in self.n03_images], list(range(878, 918))
        )
        self.assertEqual(
            self.rows_sha256(self.n03_images), EXPECTED_IMAGE_ROWS_SHA256
        )
        mapped_names = [
            Path(row["asset_relative_path"]).name for row in self.n03_images
        ]
        self.assertEqual(
            self.sequence_sha256(mapped_names), EXPECTED_MAPPED_NAMES_SHA256
        )

        disposition_rows = [
            row for row in self.n03_images if "reference_disposition" in row
        ]
        self.assertEqual(len(disposition_rows), 1)
        disposition = disposition_rows[0]
        self.assertEqual(disposition["ordinal"], 894)
        self.assertEqual(
            disposition["reference_disposition"],
            build.OMITTED_REFERENCE_DISPOSITION,
        )
        self.assertEqual(
            build.REFERENCE_DISPOSITION_FIELDS & set(disposition),
            build.REFERENCE_DISPOSITION_FIELDS,
        )
        self.assertTrue(
            disposition["reference_authoritative_location"].startswith("pdf:0903")
        )
        self.assertEqual(disposition["reference_reviewer_type"], "agent")
        self.assertEqual(
            disposition["reference_verification_status"], "SOURCE_VERIFIED"
        )

        references = re.findall(
            r"!\[([^\]]*)\]\(([^)\s]+\.jpeg)\)", self.rendered
        )
        self.assertEqual(len(references), 45)
        self.assertEqual(len({target for _, target in references}), 45)
        self.assertEqual(
            self.sequence_sha256([f"{alt}\t{target}" for alt, target in references]),
            EXPECTED_ALL_REFERENCES_SHA256,
        )
        added_names = {
            Path(row["asset_relative_path"]).name for row in self.n03_added
        }
        actual_mapped = [
            target for _, target in references if target not in added_names
        ]
        expected_retained = [
            name
            for row, name in zip(self.n03_images, mapped_names)
            if row["ordinal"] != 894
        ]
        self.assertEqual(actual_mapped, expected_retained)
        self.assertEqual(
            self.sequence_sha256(actual_mapped),
            EXPECTED_RETAINED_REFERENCES_SHA256,
        )
        self.assertNotIn("_page_902_Figure_24.jpeg", self.rendered)

        # Every mapped asset remains present and verified, including the
        # source-false-positive raster that repaired Markdown does not render.
        for row in self.n03_images:
            basename = Path(row["asset_relative_path"]).name
            output = build.OUTPUT_ROOT / Path(self.path).parent / basename
            self.assertTrue(output.is_file(), basename)
        false_positive_output = (
            build.OUTPUT_ROOT
            / Path(self.path).parent
            / "_page_902_Figure_24.jpeg"
        )
        self.assertEqual(
            build.sha256(false_positive_output.read_bytes()),
            disposition["asset_sha256"],
        )

    def test_four_operator_panel_overrides_are_exact(self) -> None:
        repaired_rows = [
            row
            for row in self.n03_images
            if "repaired_asset_relative_path" in row
        ]
        self.assertEqual(
            [row["ordinal"] for row in repaired_rows], list(EXPECTED_REPAIRS)
        )
        for row in repaired_rows:
            basename, digest, dimensions = EXPECTED_REPAIRS[row["ordinal"]]
            with self.subTest(ordinal=row["ordinal"], asset=basename):
                self.assertEqual(
                    build.REPAIRED_IMAGE_FIELDS & set(row),
                    build.REPAIRED_IMAGE_FIELDS,
                )
                self.assertEqual(Path(row["asset_relative_path"]).name, basename)
                repaired = build.REPO_ROOT / Path(
                    row["repaired_asset_relative_path"]
                )
                output = build.OUTPUT_ROOT / Path(self.path).parent / basename
                payload = repaired.read_bytes()
                self.assertEqual(row["repaired_asset_sha256"], digest)
                self.assertEqual(build.sha256(payload), digest)
                self.assertEqual(build.jpeg_dimensions(payload), dimensions)
                self.assertEqual(
                    (row["repaired_width_px"], row["repaired_height_px"]),
                    dimensions,
                )
                self.assertTrue(
                    row["repaired_authoritative_location"].startswith("pdf:0914")
                )
                self.assertIn("excluding", row["repaired_authoritative_location"])
                self.assertEqual(output.read_bytes(), payload)

        operator_sequence = (
            "`x_ -> x ∘ x`\n\n"
            "![](_page_913_Picture_8.jpeg)\n\n"
            "`x_ ∘ y_ -> (y ∘ x) ∘ y`\n\n"
            "![](_page_913_Picture_9.jpeg)\n\n"
            "`x_ ∘ y_ -> (y ∘ y) ∘ (x ∘ x)`\n\n"
            "![](_page_913_Picture_10.jpeg)\n\n"
            "`x_ ∘ y_ -> y ∘ (x ∘ x)`\n\n"
            "![](_page_913_Picture_11.jpeg)"
        )
        self.assertEqual(self.rendered.count(operator_sequence), 1)

    def test_six_source_added_assets_and_placement_are_exact(self) -> None:
        self.assertEqual(
            [row["id"] for row in self.n03_added],
            [f"G5-A-{number:04d}" for number in range(44, 50)],
        )
        self.assertEqual(
            self.rows_sha256(self.n03_added), EXPECTED_ADDED_ROWS_SHA256
        )
        for row in self.n03_added:
            basename, digest, dimensions, byte_count, pdf_page = EXPECTED_ADDED[
                row["id"]
            ]
            with self.subTest(asset=row["id"]):
                self.assertEqual(set(row), build.ADDED_ASSET_FIELDS)
                self.assertEqual(row["document_id"], "N03")
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                self.assertTrue(
                    row["authoritative_location"].startswith(f"pdf:{pdf_page:04d}")
                )
                source = build.REPO_ROOT / Path(row["asset_relative_path"])
                output = build.OUTPUT_ROOT / Path(self.path).parent / basename
                payload = source.read_bytes()
                self.assertEqual(source.name, basename)
                self.assertEqual(len(payload), byte_count)
                self.assertEqual(row["asset_sha256"], digest)
                self.assertEqual(build.sha256(payload), digest)
                self.assertEqual(build.jpeg_dimensions(payload), dimensions)
                self.assertEqual(
                    (row["width_px"], row["height_px"]), dimensions
                )
                self.assertEqual(output.read_bytes(), payload)

        references = re.findall(
            r"!\[([^\]]*)\]\(([^)\s]+\.jpeg)\)", self.rendered
        )
        added_names = [
            Path(row["asset_relative_path"]).name for row in self.n03_added
        ]
        positions = [
            index + 1
            for index, (_, target) in enumerate(references)
            if target in set(added_names)
        ]
        self.assertEqual(positions, [24, 25, 31, 32, 37, 38])
        self.assertEqual(
            [target for _, target in references if target in set(added_names)],
            added_names,
        )

    def test_boolean_table_is_complete_and_semantically_exact(self) -> None:
        table = self.rendered.split("```text\n", 1)[1].split("\n```", 1)[0]
        entries = [
            (int(number), expression.strip())
            for number, expression in re.findall(
                r"rule (\d+): (.*?)(?= \| rule \d+:|\n|$)", table
            )
        ]
        self.assertEqual(len(entries), 256)
        self.assertEqual(sorted(number for number, _ in entries), list(range(256)))
        self.assertEqual(len({number for number, _ in entries}), 256)

        for number, expression in entries:
            actual = 0
            for p in (False, True):
                for q in (False, True):
                    for r in (False, True):
                        value = BooleanParser(
                            expression, {"p": p, "q": q, "r": r}
                        ).parse()
                        actual |= int(value) << (
                            4 * int(p) + 2 * int(q) + int(r)
                        )
            with self.subTest(rule=number, expression=expression):
                self.assertEqual(actual, number)

    def test_high_risk_technical_forms_and_order_are_exact(self) -> None:
        required_once = (
            "TMStep[rule_List, {s_, a_List, n_}] /; 1 <= n <= Length[a] :=",
            "For all `m <= Fibonacci[t - 1]`",
            "For *m* > 1, the value of *n* for which `m == Fibonacci[n]`",
            "the maximum period is 6 *k*, achieved when `k = 10 5^m`",
            "typically grows like `λ^t`, where `λ` is the largest eigenvalue",
            "a[t] == 2 a[t - 1] + a[t - 2]",
            "For large *t* the number of elements increases like `λ^t` with "
            "`λ = (Sqrt[13] + 1)/2`",
            "`a[r], ..., a[1], a[0]`",
            "`{1, 2, 2, 1, 1, 2, ...}`",
            "CTStep[{{r_, s___}, {1, a___}}] := {{s, r}, Join[{a}, r]}",
            "{1, 3, 5, 10, 16, 37, 215, 1280}",
            "Module[{i = 1}, expr /. lhs :> rhs /; i++ == 1]",
            "($\\partial_{xx} f[x]$ for example gives `f''[x]` which is "
            "`Derivative[2][f][x]`.)",
            "Raymond Smullyan",
            "which—like combinators—has no built-in notion of types",
            "u = expr //. {e -> 2, x_[y_] -> y^x} = 2^(2^m)",
        )
        for specimen in required_once:
            with self.subTest(specimen=specimen[:80]):
                self.assertEqual(self.rendered.count(specimen), 1)
        self.assertEqual(
            self.rendered.count(
                "MAStep[rule_, {list_List, n_Integer}] /; "
                "1 < n < Length[list] :="
            ),
            2,
        )

        forbidden = (
            "_page_902_Figure_24.jpeg",
            "Subscript[∂, xx]",
            "10^(5 m)",
            "m < Fibonacci[t - 1]",
            "m = Fibonacci[n]",
            "TMStep[rule_List, {s_, a_List, n_}] /; "
            "1 < n < Length[a] :=",
            "…",
            "#### 000000",
            "| ist",
            "||ist",
            "OddO",
            "105^",
            "Smullvan",
            "mfor",
            "neighborindependent",
            "Perioddoubling",
            "righthand side",
            "lefthand side",
            "<sup>",
            "</sub>",
            "$$",
            "\\_",
        )
        for remnant in forbidden:
            with self.subTest(remnant=remnant):
                self.assertNotIn(remnant, self.rendered)

        sequential_positions = [
            self.rendered.index(
                "Sequential substitution systems can be implemented quite directly"
            ),
            self.rendered.index("Having made the definition"),
            self.rendered.index("Attributes[s] = Flat"),
            self.rendered.index("the state of a sequential substitution system"),
        ]
        self.assertEqual(sequential_positions, sorted(sequential_positions))

    def test_two_pass_coverage_is_closed(self) -> None:
        rows = validate.validate_coverage(self.documents)
        row = next(item for item in rows if item["document_id"] == "N03")
        self.assertEqual(
            (row["first_pass"], row["second_pass"], row["reviewer_type"]),
            ("YES", "YES", "agent"),
        )
        self.assertIn("25 guarded corrections", row["notes"])
        self.assertIn("one source-false-positive", row["notes"])
        self.assertIn("4 repaired-only overrides", row["notes"])
        self.assertIn(
            "zero discrepancy ambiguity or source omission", row["notes"]
        )

    def test_closure_inventory_and_n04_handoff_are_exact(self) -> None:
        references = re.findall(
            r"!\[([^\]]*)\]\(([^)\s]+\.jpeg)\)", self.rendered
        )
        repaired = [
            row
            for row in self.n03_images
            if "repaired_asset_relative_path" in row
        ]
        dispositions = [
            row for row in self.n03_images if "reference_disposition" in row
        ]
        self.assertEqual(
            (
                len(self.n03_corrections),
                len(self.n03_images),
                len(repaired),
                len(dispositions),
                len(self.n03_added),
                len(references),
            ),
            (25, 40, 4, 1, 6, 45),
        )
        self.assertEqual(
            (
                self.document["raw_end_line"] + 1,
                self.document["raw_end_byte_exclusive"],
                self.document["authoritative_pdf_end_page"] + 1,
            ),
            (
                self.n04_document["raw_start_line"],
                self.n04_document["raw_start_byte"],
                self.n04_document["authoritative_pdf_start_page"],
            ),
        )
        self.assertEqual(
            (
                self.n04_document["raw_start_line"],
                self.n04_document["raw_start_byte"],
                self.n04_document["authoritative_pdf_start_page"],
            ),
            (12499, 1792864, 917),
        )
        self.assertEqual(
            [row["ordinal"] for row in self.n04_images], list(range(918, 989))
        )
        self.assertEqual(
            Path(self.n04_images[0]["asset_relative_path"]).name,
            "_page_916_Figure_12.jpeg",
        )
        self.assertEqual(
            int(self.n03_corrections[-1]["id"].rsplit("-", 1)[1]) + 1,
            974,
        )
        self.assertEqual(
            int(self.n03_added[-1]["id"].rsplit("-", 1)[1]) + 1,
            50,
        )


if __name__ == "__main__":
    unittest.main()
