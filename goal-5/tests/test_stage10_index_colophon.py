from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from collections import Counter
from pathlib import Path
from typing import Any


GOAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402
import validate  # noqa: E402


EXPECTED = {
    "INDEX": {
        "id": "G5-C-4829",
        "raw_start_byte": 3_327_771,
        "raw_end_byte_exclusive": 3_777_655,
        "raw_start_line": 20_826,
        "raw_end_line": 22_457,
        "raw_byte_count": 449_884,
        "raw_line_count": 1_632,
        "raw_sha256": "c7158d6e6e431686e3eac7627ce5b6eafd73e7f133a4dca8a8d28f37915b93c9",
        "pdf_start": 1_217,
        "pdf_end": 1_279,
        "location": "pdf:1217; through pdf:1279; Stage 10 fixed-layout Index reconstruction",
        "row_sha256": "2d830244cc5cf4bb1b15f69f790335e1888f131c68809be46cab1676fc022d92",
        "target_bytes": 503_396,
        "target_lfs": 17_740,
        "target_sha256": "9aa140977bdd7e94ef352d91efe57ff2fb0a1dbb375a6c673da146f2e745a9af",
    },
    "COLOPHON": {
        "id": "G5-C-4830",
        "raw_start_byte": 3_777_655,
        "raw_end_byte_exclusive": 3_780_628,
        "raw_start_line": 22_458,
        "raw_end_line": 22_498,
        "raw_byte_count": 2_973,
        "raw_line_count": 41,
        "raw_sha256": "e2980ae72d81a28a08c07250eb4abcc90a1b3ac7d0b42a0713fca6d96d8d6156",
        "pdf_start": 1_280,
        "pdf_end": 1_280,
        "location": "pdf:1280; complete final-page Colophon fixed-layout reconstruction",
        "row_sha256": "840f38752035b919ef221376d225ad38521c9628617bc388c42dba24ed42ce60",
        "target_bytes": 2_992,
        "target_lfs": 39,
        "target_sha256": "44641db1c2ceabc1baf7856aa9b6a67ff0ef360181beb9041ec84d28b20493e9",
    },
}


def canonical_row_sha256(row: dict[str, Any]) -> str:
    payload = (
        json.dumps(
            row,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


class Stage10IndexColophonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.range_data = json.loads(build.RANGES_PATH.read_text(encoding="utf-8"))
        cls.raw = build.LEGACY_ROOT.joinpath("A-New-Kind-of-Science.md").read_bytes()
        cls.documents = build.validate_ranges(cls.raw, cls.range_data)
        cls.corrections = build.validate_corrections(
            build.read_jsonl(build.CORRECTIONS_PATH), cls.raw, cls.documents
        )
        cls.document_by_id = {
            document["id"]: document for document in cls.documents
        }
        cls.rows_by_document = {
            document_id: [
                row
                for row in cls.corrections
                if row["document_id"] == document_id
            ]
            for document_id in EXPECTED
        }
        cls.independent = validate.independent_document_bytes(
            cls.raw, cls.documents, cls.corrections
        )

    def test_whole_document_source_ranges_and_correction_rows_are_pinned(self) -> None:
        selected = [
            (position, row["id"], row["document_id"])
            for position, row in enumerate(self.corrections)
            if row["id"] in {"G5-C-4829", "G5-C-4830"}
        ]
        self.assertEqual(
            [(correction_id, document_id) for _, correction_id, document_id in selected],
            [("G5-C-4829", "INDEX"), ("G5-C-4830", "COLOPHON")],
        )
        self.assertLess(selected[0][0], selected[1][0])

        for document_id, expected in EXPECTED.items():
            with self.subTest(document_id=document_id):
                document = self.document_by_id[document_id]
                self.assertEqual(
                    (
                        document["raw_start_byte"],
                        document["raw_end_byte_exclusive"],
                        document["raw_start_line"],
                        document["raw_end_line"],
                        document["raw_byte_count"],
                        document["raw_line_count"],
                        document["raw_segment_sha256"],
                        document["authoritative_pdf_start_page"],
                        document["authoritative_pdf_end_page"],
                    ),
                    (
                        expected["raw_start_byte"],
                        expected["raw_end_byte_exclusive"],
                        expected["raw_start_line"],
                        expected["raw_end_line"],
                        expected["raw_byte_count"],
                        expected["raw_line_count"],
                        expected["raw_sha256"],
                        expected["pdf_start"],
                        expected["pdf_end"],
                    ),
                )

                segment = self.raw[
                    expected["raw_start_byte"] : expected["raw_end_byte_exclusive"]
                ]
                self.assertEqual(len(segment), expected["raw_byte_count"])
                self.assertEqual(build.sha256(segment), expected["raw_sha256"])

                self.assertEqual(len(self.rows_by_document[document_id]), 1)
                row = self.rows_by_document[document_id][0]
                self.assertEqual(set(row), build.CORRECTION_FIELDS)
                self.assertEqual(row["id"], expected["id"])
                self.assertEqual(row["raw_start_byte"], expected["raw_start_byte"])
                self.assertEqual(row["before"].encode("utf-8"), segment)
                self.assertEqual(row["expected_count"], 1)
                self.assertEqual(row["authoritative_location"], expected["location"])
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                self.assertEqual(canonical_row_sha256(row), expected["row_sha256"])

                output = build.safe_relative_path(document["output_path"], suffix=".md")
                rendered = row["after"].encode("utf-8")
                self.assertEqual(self.independent[output], rendered)
                self.assertEqual(
                    build.apply_corrections(document, segment, self.corrections),
                    rendered,
                )
                self.assertEqual((build.OUTPUT_ROOT / Path(output)).read_bytes(), rendered)
                self.assertEqual(len(rendered), expected["target_bytes"])
                self.assertEqual(rendered.count(b"\n"), expected["target_lfs"])
                self.assertEqual(build.sha256(rendered), expected["target_sha256"])

    def test_index_markdown_structure_is_exact(self) -> None:
        row = self.rows_by_document["INDEX"][0]
        rendered = row["after"]
        lines = rendered.splitlines()

        self.assertEqual(
            lines[:8],
            [
                "#### Index",
                "",
                "*See page 852 for notes about this index*",
                "*and about entries for personal names.*",
                "",
                "*Note that names mentioned only in the*",
                "*Preface are not included in this index.*",
                "",
            ],
        )
        self.assertEqual(len(lines), 17_740)
        self.assertEqual(sum(line.startswith("- ") for line in lines), 5_484)
        self.assertEqual(sum(line.startswith("  - ") for line in lines), 12_214)
        self.assertEqual(sum(line.startswith("    ") for line in lines), 34)
        self.assertEqual(
            Counter(len(line) - len(line.lstrip(" ")) for line in lines),
            {0: 5_492, 2: 12_214, 4: 34},
        )
        self.assertEqual(5_484 + 12_214 + 34, 17_732)
        self.assertEqual(sum(line.startswith("#") for line in lines), 1)
        self.assertEqual(rendered.count("`"), 818)
        self.assertNotIn("**", rendered)
        self.assertEqual(rendered.count("*") // 2, 704)
        self.assertEqual(rendered.count("<sub>"), 12)
        self.assertEqual(rendered.count("</sub>"), 12)
        self.assertEqual(rendered.count("<sup>"), 7)
        self.assertEqual(rendered.count("</sup>"), 7)
        self.assertNotIn("<!--", rendered)
        self.assertFalse(any(line.strip() in {"---", "***", "___"} for line in lines))
        self.assertTrue(rendered.endswith("- Zygmund series, 918\n"))

    def test_colophon_markdown_structure_and_high_risk_repairs_are_exact(self) -> None:
        row = self.rows_by_document["COLOPHON"][0]
        rendered = row["after"]

        self.assertTrue(rendered.startswith("#### *Colophon*\n\n"))
        self.assertEqual(rendered.count("*"), 36)
        self.assertNotIn("**", rendered)
        self.assertEqual(rendered.count("*") // 2, 18)
        self.assertIn("round dots angled at 45°", rendered)
        self.assertNotIn("$45^{\\circ}$", rendered)
        self.assertIn("796 *Mathematica* programs", rendered)
        self.assertIn("For other credits see pages xii–xiv.", rendered)
        self.assertIn("P. E. Dimotakis", rendered)
        self.assertIn("H. Honji/S. Taneda", rendered)
        self.assertIn("MIT Press", rendered)
        self.assertIn("Chip Clark/The Smithsonian Institution", rendered)
        self.assertNotIn("P.E. Dimotakis", rendered)
        self.assertNotIn("H. Honjilő. Taneda", rendered)
        self.assertNotIn("MT Fress", rendered)
        self.assertNotIn("Chip Clarlv", rendered)
        self.assertTrue(
            rendered.endswith("Printed by Kromar Printing Ltd, Winnipeg, Canada.\n")
        )
        self.assertFalse(rendered.endswith("\n\n"))

    def test_stage10_correction_metadata_mutations_are_rejected(self) -> None:
        base = self.rows_by_document["COLOPHON"][0]
        mutations = {
            "blank id": lambda row: row.__setitem__("id", ""),
            "unknown document": lambda row: row.__setitem__("document_id", "UNKNOWN"),
            "wrong start": lambda row: row.__setitem__(
                "raw_start_byte", row["raw_start_byte"] + 1
            ),
            "wrong preimage": lambda row: row.__setitem__(
                "before", "X" + row["before"][1:]
            ),
            "outside source page": lambda row: row.__setitem__(
                "authoritative_location", "pdf:1279; wrong document"
            ),
            "missing reason": lambda row: row.pop("reason"),
            "nonpositive occurrence count": lambda row: row.__setitem__(
                "expected_count", 0
            ),
            "unverified": lambda row: row.__setitem__(
                "verification_status", "INFERRED"
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                changed = copy.deepcopy(base)
                mutate(changed)
                with self.assertRaises(build.BuildError):
                    build.validate_corrections([changed], self.raw, self.documents)


if __name__ == "__main__":
    unittest.main()
