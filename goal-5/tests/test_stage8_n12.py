#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from typing import Any


_default_root = Path.cwd()
if not (_default_root / "goal-5").is_dir():
    _default_root = Path(__file__).resolve().parents[2]
REPO_ROOT = Path(os.environ.get("ANKOS_REPO_ROOT", _default_root)).resolve()
GOAL_DIR = REPO_ROOT / "goal-5"

import sys

sys.path.insert(0, str(GOAL_DIR))
import build  # noqa: E402
import validate  # noqa: E402


FINAL_CORRECTION_COUNT = 1222
FINAL_BASE_CORRECTION_FIRST_NUMBER = 3577
FINAL_BASE_CORRECTION_LAST_NUMBER = 4445
FINAL_REPAIR_CORRECTION_FIRST_NUMBER = 4475
FINAL_REPAIR_CORRECTION_LAST_NUMBER = 4534
FINAL_TECHNICAL_CORRECTION_FIRST_NUMBER = 4536
FINAL_TECHNICAL_CORRECTION_LAST_NUMBER = 4828
FINAL_TARGET_BYTES = 398_152
FINAL_TARGET_LFS = 1_857
FINAL_TARGET_SHA256 = (
    "90d4ddcb566aae8515b0515221a10b4d7c2d96f353b429e52010cc93222bbdfa"
)
FINAL_CORRECTION_ROWS_SHA256 = (
    "43c9f2668c8f951848779e4ead4e762d317cedb007e8135442d090e409e95b38"
)
FINAL_CORRECTION_SEQUENCE_SHA256 = (
    "e1fa1c367f28f6db3e5bf71fc6d62f871e36e3b6d9a08ce8466bfc6da420f548"
)
FINAL_IMAGE_ROWS_SHA256 = (
    "0b30632d2ca01fe1aba50d7d9fcec926704eae3a1b945a5b741c3768bcafc693"
)
FINAL_IMAGE_SEQUENCE_SHA256 = (
    "f3540d2c585bf4b7eb605cb831da381f9eb1e654c3a2d73246f7f4be856c3c69"
)
FINAL_ADDITION_ROWS_SHA256 = (
    "d039d972314fe3785d00fcd405a3570a35aeccc925a7fee761bc0be0f3757f9b"
)
FINAL_ADDITION_SEQUENCE_SHA256 = (
    "c6d9709f099973e3a67b054ee3c973f324cbdbc6db6b3b61c02fe83f52ddcdb1"
)
EXPECTED_RAW_FIRST_256_SHA256 = (
    "7efd78367ce9c1dc9e8ab62351205d717d6cddc3000bfb98b467ad92654b7b81"
)
EXPECTED_RAW_LAST_256_SHA256 = (
    "88388af26b2f7b449897c5146ec311dadea7d98677547b5d030446ff3cbe8fbd"
)
EXPECTED_PDF_SHA256 = (
    "a3cc5dd60e12d6b563aee86ea31a15b03f9cddfd4869b8f965d3a11bbc61a0d6"
)
EXPECTED_NORMAL_TREE_SHA256 = (
    "904bab4188661c228690b8fb6fe9ff95c1765512c7fad78b9eb467e53ccbf8ac"
)
EXPECTED_ZERO_TREE_SHA256 = (
    "1971cbef0d2c588ee94eb0d268e535c1e9fd2eb6bcc8864bd671ab40ca98729b"
)


EXPECTED_HEADINGS = [
    "## The Principle of Computational Equivalence",
    "### Basic Framework",
    "### Outline of the Principle",
    "### The Content of the Principle",
    "### The Validity of the Principle",
    "### Explaining the Phenomenon of Complexity",
    "### Computational Irreducibility",
    "### The Phenomenon of Free Will",
    "### Undecidability and Intractability",
    "### Implications for Mathematics and Its Foundations",
    "### Intelligence in the Universe",
    "### Implications for Technology",
    "### Historical Perspectives",
]


EXPECTED_REFERENCES = [
    "_page_1142_Figure_7.jpeg",
    "_page_1146_Figure_2.jpeg",
    "_page_1152_Figure_5.jpeg",
    "_page_1152_Figure_6.jpeg",
    "_page_1154_Figure_8.jpeg",
    "_page_1155_Figure_12.jpeg",
    "_page_1157_Figure_7.jpeg",
    "_page_1159_Figure_6.jpeg",
    "_page_1159_Figure_21.jpeg",
    "_page_1169_Picture_4.jpeg",
    "_page_1170_Figure_15.jpeg",
    "_page_1172_Figure_6.jpeg",
    "_page_1172_Figure_7.jpeg",
    "_page_1172_Figure_8.jpeg",
    "_page_1172_Figure_9.jpeg",
    "_page_1174_Page_783_End_White_Black.jpeg",
    "_page_1174_Page_783_End_Black.jpeg",
    "_page_1177_Figure_9.jpeg",
    "_page_1178_Figure_7.jpeg",
    "_page_1178_Figure_8.jpeg",
    "_page_1178_Figure_9.jpeg",
    "_page_1178_Figure_10.jpeg",
    "_page_1180_Figure_11.jpeg",
    "_page_1181_Figure_8.jpeg",
    "_page_1183_Rule_110_Forbidden_Sequence.jpeg",
    "_page_1183_Rule_110_Single_Black_Cell.jpeg",
    "_page_1183_Rule_110_Allowed_Initial_Sequence.jpeg",
    "_page_1184_Page_799_Last_Length_4_String.jpeg",
    "_page_1184_Page_799_Last_Length_6_String.jpeg",
    "_page_1184_Page_799_Item_n_Ending.jpeg",
    "_page_1184_Page_799_Item_o_Ending.jpeg",
    "_page_1184_Page_799_Item_p_State.jpeg",
    "_page_1184_Page_799_First_Lemma_Input.jpeg",
    "_page_1184_Page_799_First_Lemma_Output.jpeg",
    "_page_1184_Page_799_Second_Lemma_Input.jpeg",
    "_page_1184_Page_799_Second_Lemma_Output.jpeg",
    "_page_1188_Picture_3.jpeg",
    "_page_1188_Figure_5.jpeg",
    "_page_1188_Figure_14.jpeg",
    "_page_1190_Figure_6.jpeg",
    "_page_1190_Figure_13.jpeg",
    "_page_1191_Picture_20.jpeg",
    "_page_1201_Picture_4.jpeg",
    "_page_1201_Picture_6.jpeg",
    "_page_1201_Picture_9.jpeg",
    "_page_1201_Picture_10.jpeg",
    "_page_1201_Picture_11.jpeg",
    "_page_1201_Page_834_First_Ungeneratable_Sequence.jpeg",
    "_page_1201_Picture_13.jpeg",
    "_page_1201_Picture_14.jpeg",
    "_page_1205_Figure_3.jpeg",
    "_page_1210_Figure_2.jpeg",
    "_page_1214_Picture_0.jpeg",
]


EXPECTED_REPAIRS = {
    1410: ("_page_1152_Figure_6.jpeg", "dd51a449bc6219f812402f24bf6397c2c6f3d45ec0fd4aad9fd211ad7b888fbb", (465, 153)),
    1415: ("_page_1159_Figure_21.jpeg", "320b69d78508e31b72343931f5a9d9215f595220e5b140efd1d87addade03d9e", (875, 155)),
    1417: ("_page_1170_Figure_15.jpeg", "f954853ddabaf365e8f23b8d36dbaa7f3f8d9c0caf2d2fff3440f721d1c33cf4", (880, 780)),
    1418: ("_page_1172_Figure_6.jpeg", "baab2a52f2dcae6e58d89cdf7a8ba8053082f482929f7299cf31d25801d16af3", (195, 175)),
    1423: ("_page_1178_Figure_7.jpeg", "8bdd1bafc5f07f214389fec3f1b55d7637159cb2b0488760bb438f03379a1870", (155, 168)),
    1424: ("_page_1178_Figure_8.jpeg", "559e8ddef5dc5ed5ac632f89b773a5890514d771d9573150d0f82551fc757ccf", (175, 168)),
    1436: ("_page_1201_Picture_6.jpeg", "56e3be5e88d033cfdf9ca09df4a13bc68c305a3184c550d8687e447562beba00", (870, 865)),
    1437: ("_page_1201_Picture_9.jpeg", "b1af0d55b1b44132f6430bd6a517b1b9f1ff2a9e39682b2be9bc443751b0fbe3", (198, 248)),
    1441: ("_page_1201_Picture_14.jpeg", "f48e5fc1e75564503334ead407657ef8b73c69ed2b84a1b7c8285bbb58f2f52d", (510, 205)),
}


EXPECTED_ADDED_ASSETS = {
    "G5-A-0149": ("_page_1174_Page_783_End_White_Black.jpeg", "b5daa58720c14e5f2ebf00034bc34e561c6f7d2402077fc452985dd6e62f55ff", (28, 21)),
    "G5-A-0150": ("_page_1174_Page_783_End_Black.jpeg", "9d01fcc40b1118e23f090a2f79c499884e3b6f20f91f8467d5929262f6532ddd", (14, 21)),
    "G5-A-0151": ("_page_1183_Rule_110_Forbidden_Sequence.jpeg", "66e80e33becced428c737147cf3c90815f693c01e869d178915efadc2039306f", (66, 21)),
    "G5-A-0152": ("_page_1183_Rule_110_Single_Black_Cell.jpeg", "89d7e9327ec092eb05b90ea9eaacbc45e97381a38d1bc904ffd17bc7ffc79d69", (14, 21)),
    "G5-A-0153": ("_page_1183_Rule_110_Allowed_Initial_Sequence.jpeg", "08ba7546d8df81891e0db4fc5adde88921347261837d64123b36c2b2ab18d29d", (66, 21)),
    "G5-A-0154": ("_page_1184_Page_799_Last_Length_4_String.jpeg", "20f90f45a8d114489e40633718625760961a9d19e66b39acc8df535622fb43fe", (53, 21)),
    "G5-A-0155": ("_page_1184_Page_799_Last_Length_6_String.jpeg", "3c1d97ded6b2d81432128ffe2c6c5ae8f1d4a7fb936cb501fea730d310c40c8a", (81, 21)),
    "G5-A-0156": ("_page_1184_Page_799_Item_n_Ending.jpeg", "31c4a17e5c7eb9c511a55298b138202283a026d850842b8f15a96d25ddb4f716", (28, 21)),
    "G5-A-0157": ("_page_1184_Page_799_Item_o_Ending.jpeg", "cdc68bbe1495bfa7c0de04568d97144342015b5d68a226d54267cd4b723ae91d", (28, 21)),
    "G5-A-0158": ("_page_1184_Page_799_Item_p_State.jpeg", "da96ad147d864d3d12302faeebbe72d893252cafc6d1e23c811513cb67da9cbb", (53, 21)),
    "G5-A-0159": ("_page_1184_Page_799_First_Lemma_Input.jpeg", "b07234262b625ab816b11d1988606a2dc72519dbafc11049eab47e5d8c47e85f", (16, 21)),
    "G5-A-0160": ("_page_1184_Page_799_First_Lemma_Output.jpeg", "b8c349c34f56a0257fcac929076d4875a4bfa59edaa6643422e499daf2f1fe79", (31, 21)),
    "G5-A-0161": ("_page_1184_Page_799_Second_Lemma_Input.jpeg", "d5ff42a0d1a8d3116317dfe3e6f09b6d101c67939320e8ff3250ad58c3ebcdee", (16, 21)),
    "G5-A-0162": ("_page_1184_Page_799_Second_Lemma_Output.jpeg", "07eb0e1bcf34cf7ff68ba6e1cacf4f7b05215f78fc7ec414efa9c180e00ec660", (16, 21)),
    "G5-A-0163": ("_page_1201_Page_834_First_Ungeneratable_Sequence.jpeg", "55589c9b41198368c321e54528b95994b75d9d0d9bdfaf6f2f84b95b5cfa6636", (67, 21)),
}


EXPECTED_FULL_LEDGER_SHA256 = {
    "corrections.jsonl": "e47d2d5396c0149d99a4220560b54be0f29a58de32761e26d7b337c47b671f20",
    "image-map.jsonl": "e2fac1db19000e4bd4e634ac7dd1ea0920d3c7c9f105e2503904cc024bfe0681",
    "added-assets.jsonl": "d647fa8d948b155720ca3f8c909429654f30398fbf566e0b0fb6cca779e621ae",
    "source-ranges.json": "36dacbddcbb0157f604aafeca93e6e189bd16c6b52ac6409d6d83681a41de498",
    "coverage.csv": "fb592a7019feb5cd1f8f19fe13e91c365ce13c578cf4e61ee79ea87a97491d34",
}


FORBIDDEN_PROVENANCE = re.compile(
    r"/tmp/|\bprovisional\b|first[-_ ]pass|FIRST_PASS|"
    r"N12-(?:SRC|TECH|TFP|LONG|VIS)|\bAMB\d{3}\b|integration[-_ ]candidate",
    re.IGNORECASE,
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def rows_sha256(rows: list[dict[str, Any]]) -> str:
    return hashlib.sha256(
        b"".join(canonical_bytes(row) + b"\n" for row in rows)
    ).hexdigest()


def row_hash_sequence_sha256(rows: list[dict[str, Any]]) -> str:
    payload = "".join(
        hashlib.sha256(canonical_bytes(row)).hexdigest() + "\n" for row in rows
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def length_prefixed_tree(root: Path) -> tuple[str, list[tuple[str, str, int]]]:
    digest = hashlib.sha256()
    manifest: list[tuple[str, str, int]] = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative_text = path.relative_to(root).as_posix()
        relative = relative_text.encode("utf-8")
        payload = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
        manifest.append((relative_text, build.sha256(payload), len(payload)))
    return digest.hexdigest(), manifest


class NotesForChapter12FirstPassTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.document = next(row for row in cls.documents if row["id"] == "N12")
        cls.n11 = next(row for row in cls.documents if row["id"] == "N11")
        cls.index = next(row for row in cls.documents if row["id"] == "INDEX")
        cls.path = build.safe_relative_path(cls.document["output_path"], suffix=".md")
        cls.rendered_bytes = build.document_bytes(
            cls.raw, cls.documents, cls.corrections
        )[cls.path]
        cls.rendered = cls.rendered_bytes.decode("utf-8")
        cls.output_path = build.OUTPUT_ROOT / Path(cls.path)
        cls.rows = [row for row in cls.corrections if row["document_id"] == "N12"]
        cls.image_rows = [row for row in cls.images if row["document_id"] == "N12"]
        cls.added = [row for row in cls.added_assets if row["document_id"] == "N12"]
        cls.references = re.findall(r"!\[[^]]*\]\(([^)\n]+)\)", cls.rendered)
        cls.segment = cls.raw[
            cls.document["raw_start_byte"] : cls.document["raw_end_byte_exclusive"]
        ]

    def test_exact_source_range_correction_registry_and_boundaries(self) -> None:
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
                19_028,
                20_825,
                2_926_907,
                3_327_771,
                1_798,
                400_864,
                "4e48b0ff741eed035fdd63d5d1264b73cb8dea3ec87a73d7571e33995f23b513",
                1141,
                1216,
                "1125",
                "1197 followed by an unfoliated blank, divider, and blank",
            ),
        )
        self.assertEqual(build.sha256(self.segment[:256]), EXPECTED_RAW_FIRST_256_SHA256)
        self.assertEqual(build.sha256(self.segment[-256:]), EXPECTED_RAW_LAST_256_SHA256)
        self.assertEqual(self.n11["raw_end_byte_exclusive"], 2_926_907)
        self.assertEqual(self.n11["raw_end_line"] + 1, 19_028)
        self.assertEqual(self.index["raw_start_byte"], 3_327_771)
        self.assertEqual(self.index["raw_start_line"], 20_826)

        self.assertEqual(len(self.rows), FINAL_CORRECTION_COUNT)
        self.assertEqual(
            [row["id"] for row in self.rows],
            [
                *(
                    f"G5-C-{number:04d}"
                    for number in range(
                        FINAL_BASE_CORRECTION_FIRST_NUMBER,
                        FINAL_BASE_CORRECTION_LAST_NUMBER + 1,
                    )
                ),
                *(
                    f"G5-C-{number:04d}"
                    for number in range(
                        FINAL_REPAIR_CORRECTION_FIRST_NUMBER,
                        FINAL_REPAIR_CORRECTION_LAST_NUMBER + 1,
                    )
                ),
                *(
                    f"G5-C-{number:04d}"
                    for number in range(
                        FINAL_TECHNICAL_CORRECTION_FIRST_NUMBER,
                        FINAL_TECHNICAL_CORRECTION_LAST_NUMBER + 1,
                    )
                ),
            ],
        )
        self.assertEqual(rows_sha256(self.rows), FINAL_CORRECTION_ROWS_SHA256)
        self.assertEqual(
            row_hash_sequence_sha256(self.rows), FINAL_CORRECTION_SEQUENCE_SHA256
        )

        previous_end = self.document["raw_start_byte"]
        for row in sorted(self.rows, key=lambda value: value["raw_start_byte"]):
            with self.subTest(correction=row["id"]):
                self.assertEqual(set(row), build.CORRECTION_FIELDS)
                start = row["raw_start_byte"]
                before = row["before"].encode("utf-8")
                end = start + len(before)
                self.assertGreaterEqual(start, previous_end)
                self.assertEqual(self.raw[start:end], before)
                self.assertEqual(self.segment.count(before), row["expected_count"])
                self.assertGreaterEqual(row["expected_count"], 1)
                pages = [
                    int(page)
                    for page in re.findall(
                        r"pdf:(\d{4})", row["authoritative_location"]
                    )
                ]
                printed = [
                    int(page)
                    for page in re.findall(
                        r"printed(?::|\s)+(\d{3,4})",
                        row["authoritative_location"],
                    )
                ]
                self.assertTrue(pages)
                self.assertTrue(all(1141 <= page <= 1216 for page in pages))
                self.assertTrue(printed)
                self.assertEqual(printed[0], pages[0] - 16)
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                previous_end = end
        manifest_text = "\n".join(
            canonical_bytes(row).decode("utf-8")
            for row in self.rows + self.image_rows + self.added
        )
        self.assertIsNone(FORBIDDEN_PROVENANCE.search(manifest_text))

    def test_exact_final_render_and_markdown_structure(self) -> None:
        self.assertEqual(len(self.rendered_bytes), FINAL_TARGET_BYTES)
        self.assertEqual(self.rendered_bytes.count(b"\n"), FINAL_TARGET_LFS)
        self.assertEqual(build.sha256(self.rendered_bytes), FINAL_TARGET_SHA256)
        self.assertTrue(self.rendered_bytes.endswith(b"\n\n"))
        self.assertFalse(self.rendered_bytes.endswith(b"\n\n\n"))
        self.assertEqual(self.output_path.read_bytes(), self.rendered_bytes)
        self.assertEqual(
            validate.independent_document_bytes(
                self.raw, self.documents, self.corrections
            )[self.path],
            self.rendered_bytes,
        )

        lines = self.rendered.splitlines()
        headings = [line for line in lines if line.startswith("#")]
        labels = [line for line in lines if line.startswith("■ **")]
        fence_lines = re.findall(r"(?m)^ {0,3}```[^\n]*$", self.rendered)
        without_fences = re.sub(
            r"```[^\n]*\n.*?```", "", self.rendered, flags=re.DOTALL
        )
        inline_code = re.findall(r"(?<!`)`([^`]+)`(?!`)", without_fences)
        math_spans = re.findall(
            r"(?<!\$)\$(?!\$)(?:\\.|[^$\n])+?(?<!\$)\$(?!\$)", self.rendered
        )
        display_math = re.findall(r"(?m)^ {0,3}\$\$\s*$", self.rendered)
        self.assertEqual(headings, EXPECTED_HEADINGS)
        self.assertEqual(
            (
                len(headings),
                len(labels),
                len(fence_lines),
                len(inline_code),
                len(math_spans),
                len(display_math),
                len(self.references),
            ),
            (13, 257, 104, 327, 510, 12, 53),
        )
        self.assertTrue(all(line == "```" for line in fence_lines))
        self.assertEqual(self.references, EXPECTED_REFERENCES)
        self.assertEqual(len(set(self.references)), 53)
        self.assertEqual(
            [
                (number, span)
                for number, span in enumerate(math_spans, 1)
                if span.count("{") != span.count("}")
            ],
            [],
        )
        self.assertEqual(
            (
                self.rendered.count("—"),
                self.rendered.count("…"),
                self.rendered.count("..."),
            ),
            (477, 0, 20),
        )
        self.assertEqual(
            [number for number, line in enumerate(lines, 1) if line.endswith((" ", "\t"))],
            [],
        )
        self.assertEqual(
            [
                ord(character)
                for character in self.rendered
                if ord(character) < 32 and character not in "\n\t"
            ],
            [],
        )
        self.assertNotIn("\\)$", self.rendered)
        self.assertNotIn("<<<<<<<", self.rendered)
        self.assertNotIn(">>>>>>>", self.rendered)

    def test_late_close_source_and_technical_repairs_are_exact(self) -> None:
        by_id = {row["id"]: row for row in self.corrections}
        self.assertEqual(
            by_id["G5-C-3797"]["after"],
            "`NestList`[#2 &, 2, n], or  $2^{2^n}$ , although for  "
            "$x = (20\\,4^s - 2)/3$  a better fit for  $n \\le 200$  is just  "
            "$2^{2.6 n}$ , with outputs increasing like  $2^{2^{1.3 n}}$ .\n",
        )
        self.assertEqual(
            [row["id"] for row in self.corrections[4370:4385]],
            [f"G5-C-{number:04d}" for number in range(4371, 4386)],
        )
        self.assertEqual(
            [row["id"] for row in self.corrections[4385:4445]],
            [f"G5-C-{number:04d}" for number in range(4386, 4446)],
        )
        self.assertEqual(
            (by_id["G5-C-4371"]["before"], by_id["G5-C-4371"]["after"]),
            ('"BBBBBBBA"', '`"BBBBBBA"`'),
        )
        self.assertNotIn("BBBBBBBA", self.rendered)
        self.assertEqual(self.rendered.count("BBBBBBA"), 1)
        self.assertNotIn("_-", self.rendered)
        self.assertNotIn("_{-}", self.rendered)
        self.assertNotIn("204^s", self.rendered)
        self.assertEqual(self.rendered.count(r"20\,4^s"), 2)
        self.assertIn("$s\\,k + 4$ generators and $5\\,s\\,k + 2$", self.rendered)
        self.assertIn("`LeafCount` grows like $3^t$.", self.rendered)
        self.assertEqual(self.rendered.count("10<sup>45</sup>"), 2)
        self.assertNotIn(r", \\ (a \circ a)", self.rendered)
        self.assertIn(r", (a \circ a)", self.rendered)

        self.assertEqual(
            (
                len(re.findall(r"(?<![=])==(?!=)", self.rendered)),
                len(re.findall(r"(?<![=])===(?!=)", self.rendered)),
            ),
            (216, 3),
        )
        self.assertIn("such as equations u == v", self.rendered)
        self.assertNotIn("such as equations u = v", self.rendered)
        polyadic = (
            "f[f[a, b, c], d, e] = f[a, f[b, c, d], e] = "
            "f[a, b, f[c, d, e]]"
        )
        self.assertIn(f"\n\n{polyadic}\n\nAnother example", self.rendered)
        self.assertNotIn(f"{polyadic}. Another example", self.rendered)
        self.assertNotIn(
            "f[f[a, b, c], d, e] == f[a, f[b, c, d], e] == ",
            self.rendered,
        )
        self.assertEqual(
            self.rendered.count(
                "additive cellular automata (1984) (`MultiplicativeOrder`)"
            ),
            1,
        )
        self.assertNotIn(
            "additive cellular automata (MultiplicativeOrder)", self.rendered
        )
        self.assertEqual(self.rendered.count(r"Apply[And, axioms]}];"), 1)
        self.assertNotIn(r"Apply[And, axioms]\}];", self.rendered)
        self.assertNotIn(r"Apply[And, axioms]\}\};", self.rendered)
        for row in self.corrections[4385:4445]:
            with self.subTest(late_guard=row["id"]):
                self.assertNotIn(row["before"], self.rendered)
                self.assertEqual(self.rendered.count(row["after"]), 1)

    def test_reopened_spacing_syntax_and_nand_repairs_are_exact(self) -> None:
        by_id = {row["id"]: row for row in self.rows}
        self.assertEqual(
            (
                by_id["G5-C-4600"]["raw_start_byte"],
                by_id["G5-C-4600"]["before"],
                by_id["G5-C-4600"]["after"],
            ),
            (3000685, r"\$IterationLimit", "`$IterationLimit`"),
        )
        self.assertIn(
            "constructs such as `$IterationLimit` and `TimeConstraint`",
            self.rendered,
        )
        self.assertNotIn(r"\`$IterationLimit`", self.rendered)

        repaired_rows = [
            row
            for row in self.rows
            if FINAL_REPAIR_CORRECTION_FIRST_NUMBER
            <= int(row["id"].rsplit("-", 1)[1])
            <= FINAL_REPAIR_CORRECTION_LAST_NUMBER
        ]
        self.assertEqual(
            [row["id"] for row in repaired_rows],
            [
                f"G5-C-{number:04d}"
                for number in range(
                    FINAL_REPAIR_CORRECTION_FIRST_NUMBER,
                    FINAL_REPAIR_CORRECTION_LAST_NUMBER + 1,
                )
            ],
        )
        for row in repaired_rows:
            with self.subTest(reopened_guard=row["id"]):
                self.assertNotIn(row["before"], self.rendered)
                self.assertEqual(self.rendered.count(row["after"]), 1)

        technical_rows = [
            row
            for row in self.rows
            if FINAL_TECHNICAL_CORRECTION_FIRST_NUMBER
            <= int(row["id"].rsplit("-", 1)[1])
            <= FINAL_TECHNICAL_CORRECTION_LAST_NUMBER
        ]
        self.assertEqual(
            [row["id"] for row in technical_rows],
            [
                f"G5-C-{number:04d}"
                for number in range(
                    FINAL_TECHNICAL_CORRECTION_FIRST_NUMBER,
                    FINAL_TECHNICAL_CORRECTION_LAST_NUMBER + 1,
                )
            ],
        )
        self.assertEqual(len(technical_rows), 293)

        self.assertNotIn(r"\bar{\pi}", self.rendered)
        self.assertEqual(self.rendered.count(r"\bar{\land}"), 143)
        self.assertIn("$a x^2 + b y == c$", self.rendered)
        self.assertNotIn("b y^2 == c", self.rendered)
        self.assertIn("`Zeta`[1/2 + i x]", self.rendered)
        self.assertNotIn("Zeta[1/2 + i x]", self.rendered)
        self.assertIn(
            "`StringJoin`[u[[s]]] == `StringJoin`[v[[s]]]", self.rendered
        )
        self.assertIn("- (l) See page 613.", self.rendered)
        self.assertIn("`Ceiling`[2 a/3] - (a + 1) solutions", self.rendered)
        self.assertIn("Module[{c, v}, c = Apply[Function,", self.rendered)
        self.assertIn("Apply[And, axioms]}];", self.rendered)

    def test_exact_image_map_repairs_and_reference_accounting(self) -> None:
        self.assertEqual(len(self.image_rows), 38)
        self.assertEqual(
            [row["ordinal"] for row in self.image_rows], list(range(1407, 1445))
        )
        self.assertEqual(rows_sha256(self.image_rows), FINAL_IMAGE_ROWS_SHA256)
        self.assertEqual(
            row_hash_sequence_sha256(self.image_rows), FINAL_IMAGE_SEQUENCE_SHA256
        )
        self.assertEqual(
            Counter(
                "omitted"
                if "reference_disposition" in row
                else "repaired"
                if "repaired_asset_relative_path" in row
                else "retained"
                for row in self.image_rows
            ),
            Counter({"retained": 29, "repaired": 9}),
        )

        base_fields = {
            "asset_relative_path",
            "asset_sha256",
            "document_id",
            "monolith_line",
            "ordinal",
            "split_status",
        }
        mapped_names: list[str] = []
        for row in self.image_rows:
            basename = Path(row["asset_relative_path"]).name
            legacy = build.LEGACY_ROOT / Path(row["asset_relative_path"])
            output = build.OUTPUT_ROOT / Path(self.path).parent / basename
            with self.subTest(mapped_asset=row["ordinal"]):
                self.assertEqual(build.sha256(legacy.read_bytes()), row["asset_sha256"])
                self.assertEqual(self.references.count(basename), 1)
                if "repaired_asset_relative_path" in row:
                    self.assertEqual(set(row), base_fields | build.REPAIRED_IMAGE_FIELDS)
                    name, digest, dimensions = EXPECTED_REPAIRS[row["ordinal"]]
                    repaired = REPO_ROOT / row["repaired_asset_relative_path"]
                    payload = repaired.read_bytes()
                    self.assertEqual(basename, name)
                    self.assertEqual(row["repaired_asset_sha256"], digest)
                    self.assertEqual(build.sha256(payload), digest)
                    self.assertEqual(build.jpeg_dimensions(payload), dimensions)
                    self.assertEqual(
                        (row["repaired_width_px"], row["repaired_height_px"]),
                        dimensions,
                    )
                    self.assertEqual(output.read_bytes(), payload)
                else:
                    self.assertEqual(set(row), base_fields)
                    self.assertEqual(output.read_bytes(), legacy.read_bytes())
            mapped_names.append(basename)

        added_names = {value[0] for value in EXPECTED_ADDED_ASSETS.values()}
        self.assertEqual(
            [name for name in self.references if name not in added_names], mapped_names
        )

    def test_exact_added_assets_hashes_dimensions_and_order(self) -> None:
        self.assertEqual(
            [row["id"] for row in self.added],
            [f"G5-A-{number:04d}" for number in range(149, 164)],
        )
        self.assertEqual(rows_sha256(self.added), FINAL_ADDITION_ROWS_SHA256)
        self.assertEqual(
            row_hash_sequence_sha256(self.added), FINAL_ADDITION_SEQUENCE_SHA256
        )
        self.assertEqual(
            [Path(row["asset_relative_path"]).name for row in self.added],
            [EXPECTED_ADDED_ASSETS[row["id"]][0] for row in self.added],
        )

        for row in self.added:
            name, digest, dimensions = EXPECTED_ADDED_ASSETS[row["id"]]
            payload = (REPO_ROOT / row["asset_relative_path"]).read_bytes()
            output = build.OUTPUT_ROOT / Path(self.path).parent / name
            source_page = int(
                re.search(r"pdf:(\d{4})", row["authoritative_location"]).group(1)
            )
            filename_page = int(re.search(r"_page_(\d+)_", name).group(1))
            with self.subTest(addition=row["id"]):
                self.assertEqual(set(row), build.ADDED_ASSET_FIELDS)
                self.assertEqual(row["asset_sha256"], digest)
                self.assertEqual(build.sha256(payload), digest)
                self.assertEqual(build.jpeg_dimensions(payload), dimensions)
                self.assertEqual((row["width_px"], row["height_px"]), dimensions)
                self.assertEqual(filename_page + 1, source_page)
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                self.assertEqual(output.read_bytes(), payload)
                self.assertEqual(self.references.count(name), 1)

        asset_names = {
            path.name for path in (GOAL_DIR / "assets/N12").glob("*.jpeg")
        }
        expected_names = {value[0] for value in EXPECTED_ADDED_ASSETS.values()} | {
            value[0] for value in EXPECTED_REPAIRS.values()
        }
        self.assertEqual(asset_names, expected_names)
        added_names = {value[0] for value in EXPECTED_ADDED_ASSETS.values()}
        self.assertEqual(
            [name for name in self.references if name in added_names],
            [value[0] for value in EXPECTED_ADDED_ASSETS.values()],
        )

    def test_exact_integrated_input_ledgers_and_no_temp_provenance(self) -> None:
        for relative, expected in EXPECTED_FULL_LEDGER_SHA256.items():
            with self.subTest(input_ledger=relative):
                payload = (GOAL_DIR / relative).read_bytes()
                self.assertEqual(build.sha256(payload), expected)

        self.assertEqual(len(self.corrections), 4_830)
        self.assertEqual(
            [row["id"] for row in self.corrections],
            [f"G5-C-{number:04d}" for number in range(1, 4_831)],
        )
        self.assertEqual(len(self.images), 1_444)
        self.assertEqual(len(self.added_assets), 163)
        self.assertEqual(
            [row["id"] for row in self.added_assets],
            [f"G5-A-{number:04d}" for number in range(1, 164)],
        )

        n12_payload = "\n".join(
            canonical_bytes(row).decode("utf-8")
            for row in self.rows + self.image_rows + self.added
        )
        self.assertIsNone(FORBIDDEN_PROVENANCE.search(n12_payload))
        self.assertNotIn("<<<<<<<", n12_payload)
        self.assertNotIn(">>>>>>>", n12_payload)

    def test_authoritative_source_and_pending_first_pass_coverage_state(self) -> None:
        range_data = json.loads(build.RANGES_PATH.read_text(encoding="utf-8"))
        source = range_data["authoritative_source"]
        self.assertEqual(
            (source["sha256"], source["size_bytes"], source["pdf_page_count"]),
            (EXPECTED_PDF_SHA256, 57_779_240, 1280),
        )
        pdf = validate.validate_authoritative_source(range_data)
        self.assertEqual(build.sha256(pdf.read_bytes()), EXPECTED_PDF_SHA256)
        coverage = validate.validate_coverage(self.documents)
        n12 = next(row for row in coverage if row["document_id"] == "N12")
        self.assertEqual(
            (n12["first_pass"], n12["second_pass"], n12["reviewer_type"]),
            ("YES", "YES", "agent"),
        )
        self.assertEqual(sum(row["second_pass"] == "YES" for row in coverage), 29)

    def test_normal_and_zero_builds_have_frozen_length_prefixed_trees(self) -> None:
        with tempfile.TemporaryDirectory(prefix="n12-firstpass-build-") as directory:
            first = Path(directory) / "first"
            second = Path(directory) / "second"
            self.assertEqual(build.build(first), (29, 1607, 4830))
            self.assertEqual(build.build(second), (29, 1607, 4830))
            first_tree, first_manifest = length_prefixed_tree(first)
            second_tree, second_manifest = length_prefixed_tree(second)
            output_tree, output_manifest = length_prefixed_tree(build.OUTPUT_ROOT)
            self.assertEqual(first_manifest, second_manifest)
            self.assertEqual(first_manifest, output_manifest)
            self.assertEqual(len(first_manifest), 1638)
            self.assertEqual(first_tree, EXPECTED_NORMAL_TREE_SHA256)
            self.assertEqual(second_tree, EXPECTED_NORMAL_TREE_SHA256)
            self.assertEqual(output_tree, EXPECTED_NORMAL_TREE_SHA256)
            self.assertEqual(validate.validate(first), (29, 1607, 4830, 29))

            zero = Path(directory) / "zero"
            self.assertEqual(build.build(zero, zero_corrections=True), (29, 1444, 0))
            zero_tree, zero_manifest = length_prefixed_tree(zero)
            self.assertEqual(len(zero_manifest), 1475)
            self.assertEqual(zero_tree, EXPECTED_ZERO_TREE_SHA256)
            self.assertEqual(
                validate.validate(zero, zero_corrections=True), (29, 1444, 0, 29)
            )
            concatenated = b"".join(
                (zero / document["output_path"]).read_bytes()
                for document in self.documents
            )
            self.assertEqual(concatenated, self.raw)
            validate.validate_output(
                zero,
                self.raw,
                self.documents,
                [],
                self.images,
                zero_corrections=True,
            )


if __name__ == "__main__":
    unittest.main()
