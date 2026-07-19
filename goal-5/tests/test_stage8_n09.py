#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import unittest
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REPO_ROOT = (
    Path(os.environ["ANKOS_REPO_ROOT"])
    if "ANKOS_REPO_ROOT" in os.environ
    else Path(__file__).resolve().parents[2]
).resolve()
GOAL_DIR = REPO_ROOT / "goal-5"

import sys

sys.path.insert(0, str(GOAL_DIR))
import build  # noqa: E402
import validate  # noqa: E402


FINAL_CORRECTION_COUNT = 894
FINAL_CORRECTION_LAST_NUMBER = 2805
FINAL_TARGET_BYTES = 262_097
FINAL_TARGET_LFS = 1_000
FINAL_TARGET_SHA256 = (
    "72c07a44ac1c2879c123ee0871a68cef6ba28a0de6b284169353abb85915eda1"
)
FINAL_CORRECTION_ROWS_SHA256 = (
    "2faf6c7a61f488964fb5698c339a34fef5a16bb1e010660ee4384ba3e8553bf9"
)
FINAL_CORRECTION_SEQUENCE_SHA256 = (
    "a1dd2314d964147a0763ce242804a32f82ec22d976b69bfc948ba69e86c7d59a"
)
FINAL_IMAGE_ROWS_SHA256 = (
    "eb2a63e770f3bd2562a9c1f037fdd3210cedcb779c22f352a851e9dc3ff7ed43"
)
FINAL_CHANGED_IMAGE_ROWS_SHA256 = (
    "f4b436dc6214df5e18007b123b975bbcfb375d055e637f51171dbb12d5343191"
)
FINAL_ADDITION_ROWS_SHA256 = (
    "c1c47d3e3d175cfdc656eb1ddbef48ef7fbc355a3778cd406f98671c9ad51a66"
)
EXPECTED_RAW_FIRST_256_SHA256 = (
    "8f6334091ffe983e20b94f18550302decc6dbbf61bddaa03d84a256a9a9177af"
)
EXPECTED_RAW_LAST_256_SHA256 = (
    "739aa94832176100fac67499e8829f75494e8593d84f6f1936d3b5dbba663a65"
)
EXPECTED_LEGACY_TREE = (
    "b9ff7b9b507790f1d519593baf2b2d2f24dd6cd49dc0fe10f0ac629278ea42f4",
    1463,
)
EXPECTED_PDF_SHA256 = (
    "a3cc5dd60e12d6b563aee86ea31a15b03f9cddfd4869b8f965d3a11bbc61a0d6"
)


EXPECTED_HEADINGS = [
    "## Fundamental Physics",
    "### The Notion of Reversibility",
    "### Irreversibility and the Second Law of Thermodynamics",
    "### Conserved Quantities and Continuum Phenomena",
    "### Ultimate Models for the Universe",
    "### The Nature of Space",
    "### Space as a Network",
    "### The Relationship of Space and Time",
    "### Time and Causal Networks",
    "### The Sequencing of Events in the Universe",
    "### Uniqueness and Branching in Time",
    "### Evolution of Networks",
    "### Space, Time and Relativity",
    "### Elementary Particles",
    "### The Phenomenon of Gravity",
    "### Quantum Phenomena",
]


EXPECTED_REFERENCES = [
    "_page_1032_Inverse_Rules_Four_Panel_Row.jpeg",
    "_page_1033_Picture_14.jpeg",
    "_page_1037_Picture_13.jpeg",
    "_page_1038_Block_Rules_Five_Panel_Row.jpeg",
    "_page_1044_Diameter_Six_Network_Row.jpeg",
    "_page_1044_Girth_Six_Network_Row.jpeg",
    "_page_1047_Picture_11.jpeg",
    "_page_1049_Picture_5.jpeg",
    "_page_1049_Size_Dependent_Rule_60_Three_Panel_Row.jpeg",
    "_page_1049_Additive_Rules_Three_Column_Group.jpeg",
    "_page_1049_Figure_14.jpeg",
    "_page_1050_Intrinsic_Synchronization_Rule_and_Spacetime.jpeg",
    "_page_1050_Firing_Squad_Five_Width_Group.jpeg",
    "_page_1051_Spacetime_Networks_Three_Panel_Row.jpeg",
    "_page_1052_Confluence_Four_Case_Row.jpeg",
    "_page_1052_Flat_Functions_Three_Case_Row.jpeg",
    "_page_1053_Neighbor_Independent_Update_Rule.jpeg",
    "_page_1053_Picture_14.jpeg",
    "_page_1053_Picture_16.jpeg",
    "_page_1054_Figure_3.jpeg",
    "_page_1054_Overlapping_Clusters_Three_Example_Group.jpeg",
    "_page_1055_Picture_8.jpeg",
    "_page_1055_Picture_12.jpeg",
    "_page_1056_Picture_5.jpeg",
    "_page_1057_Figure_6.jpeg",
    "_page_1061_Picture_3.jpeg",
    "_page_1064_Spherical_Networks_Five_Panel_Row.jpeg",
    "_page_1065_Hyperbolic_Networks_Four_Panel_Row.jpeg",
    "_page_1067_Random_Event_Causal_Networks_Three_Panel_Row.jpeg",
    "_page_1070_Figure_3.jpeg",
    "_page_1075_Picture_3.jpeg",
    "_page_1075_Picture_7.jpeg",
]


EXPECTED_RETAINED = {
    1236: "_page_1033_Picture_14.jpeg",
    1237: "_page_1037_Picture_13.jpeg",
    1254: "_page_1047_Picture_11.jpeg",
    1255: "_page_1049_Picture_5.jpeg",
    1276: "_page_1053_Picture_14.jpeg",
    1282: "_page_1055_Picture_8.jpeg",
    1283: "_page_1055_Picture_12.jpeg",
    1284: "_page_1056_Picture_5.jpeg",
    1285: "_page_1057_Figure_6.jpeg",
    1286: "_page_1061_Picture_3.jpeg",
    1299: "_page_1070_Figure_3.jpeg",
    1300: "_page_1075_Picture_3.jpeg",
    1301: "_page_1075_Picture_7.jpeg",
}


# id: basename, digest, dimensions, replaced ordinals, final reference position
EXPECTED_ADDITIONS = {
    "G5-A-0103": ("_page_1032_Inverse_Rules_Four_Panel_Row.jpeg", "b17fb98d737d71e8add545168d38717d24f342f39ceeb7f68f69502c224ee3be", (2110, 520), (1232, 1233, 1234, 1235), 1),
    "G5-A-0104": ("_page_1038_Block_Rules_Five_Panel_Row.jpeg", "6240560b555f369d5c0bb7869a8796b84c002d10e5c380fd8f5c1efcaa755f78", (1995, 385), (1238, 1239, 1240, 1241, 1242), 4),
    "G5-A-0105": ("_page_1044_Diameter_Six_Network_Row.jpeg", "c53fa89aa270829a5d990b56cef4be42f45dffe1daef2efd4fdb0c5a40156419", (1720, 290), (1243, 1244, 1245, 1246, 1247), 5),
    "G5-A-0106": ("_page_1044_Girth_Six_Network_Row.jpeg", "0e5fedee979bc65b676da5b2de4ec1eadaea2c0f66ed98f4e4ae1b87e9f930a0", (1785, 280), (1248, 1249, 1250, 1251, 1252, 1253), 6),
    "G5-A-0107": ("_page_1049_Size_Dependent_Rule_60_Three_Panel_Row.jpeg", "b52e81f32ca8a0e6e59b65727be15fabf8dbd7d8336905221b9e623b914d906f", (1760, 360), (1256, 1257, 1258), 9),
    "G5-A-0108": ("_page_1049_Additive_Rules_Three_Column_Group.jpeg", "adfe24ec7c77a8eae3633e3c94e31e2847ec6d3bdbadfe4e4e6a337a9d91fb70", (1940, 620), (1259, 1260), 10),
    "G5-A-0109": ("_page_1050_Intrinsic_Synchronization_Rule_and_Spacetime.jpeg", "e6fda40a6ee7f78ffe0431bf9c1510cbe8499adf1c86d4271b8424336e59aeaa", (1710, 515), (1262, 1263), 12),
    "G5-A-0110": ("_page_1050_Firing_Squad_Five_Width_Group.jpeg", "8c29187f72a99158d383e8bb7ff1e0947d1ab48c9bdb874998a9a407c2e54718", (1910, 790), (1264, 1265, 1266, 1267), 13),
    "G5-A-0111": ("_page_1051_Spacetime_Networks_Three_Panel_Row.jpeg", "012ab5e2b7b6392919f924368ef2d46afe5e62b83f573790535478419af6db41", (1710, 430), (1268, 1269), 14),
    "G5-A-0112": ("_page_1052_Confluence_Four_Case_Row.jpeg", "763233fbcd08b7285d01228778f42d7b77e798e5f7978b8e7d9582a33b2b4f9c", (1730, 675), (1270, 1271, 1272), 15),
    "G5-A-0113": ("_page_1052_Flat_Functions_Three_Case_Row.jpeg", "78fb901d6d85fd7b2fad51c63d24d44f4b65a266687ee819ad0f64970f370f58", (1730, 570), (1273, 1274, 1275), 16),
    "G5-A-0114": ("_page_1053_Neighbor_Independent_Update_Rule.jpeg", "6b1a22b7ec267cbd50d15270492a5fa0f3ed15d9c084292bf8f3c22147ea600f", (1180, 380), (), 17),
    "G5-A-0115": ("_page_1054_Overlapping_Clusters_Three_Example_Group.jpeg", "880e1e3f22525cf332a659fae1d45ab94dd8541269d4ad94440a86b1f4e5edc3", (1990, 390), (1279, 1280, 1281), 21),
    "G5-A-0116": ("_page_1064_Spherical_Networks_Five_Panel_Row.jpeg", "184a4d948c495ee258dcb74dfc993a9827f6607655fbb9a79a4007d2b1551b3f", (2010, 340), (1287, 1288, 1289, 1290, 1291), 27),
    "G5-A-0117": ("_page_1065_Hyperbolic_Networks_Four_Panel_Row.jpeg", "48026580f07e08478f65540d5c1e1b740708c746941c644749ae3f5ad7f7d493", (1770, 430), (1292, 1293, 1294, 1295), 28),
    "G5-A-0118": ("_page_1067_Random_Event_Causal_Networks_Three_Panel_Row.jpeg", "f7e5fbe9c292374cb20c99acec8bf4020f399232004dfe002b426f9a8d2e33f3", (1770, 560), (1296, 1297, 1298), 29),
}


# ordinal: basename, digest, dimensions, final reference position
EXPECTED_REPAIRS = {
    1261: ("_page_1049_Figure_14.jpeg", "5aa9dde5f6abba47cfebda473d1b93e8d2d9bacc0e0439096ec356c402f0f016", (2050, 2200), 11),
    1277: ("_page_1053_Picture_16.jpeg", "7f6861e955d5837a0fafd4b3588b1d1654cc06771ab77f19ecba083a86d04be6", (1120, 600), 19),
    1278: ("_page_1054_Figure_3.jpeg", "4146c4233c1722c347d9c16e5de2bd1d368ffd8a456b6e7b8a32dae7f550148b", (1750, 960), 20),
}


EXPECTED_VISUAL_GUARD_IDS = [
    "G5-C-1920", "G5-C-2007", "G5-C-2089", "G5-C-2092",
    "G5-C-2165", "G5-C-2167", "G5-C-2174", "G5-C-2178",
    "G5-C-2191", "G5-C-2200", "G5-C-2203", "G5-C-2215",
    "G5-C-2239", "G5-C-2378", "G5-C-2383", "G5-C-2408",
]


REQUIRED_LITERAL_PINS = [
    ("inverse-bound", r"$\overline{s} \le r + 1/2 k^{2r+1} (k^{2r} - 1)$", 1),
    ("rule-184-cells", "rule 184, it can be taken to be 1 for each ■□ block", 1),
    ("rule-170-cells", "For rule 170, it is 1 for both □□ and ■□.", 1),
    ("rule-150-cells", "For rule 150, it is 1 for □□ and ■■, with", 1),
    ("cycle-label", "■ **Page 479 · Cycle lengths.** The lengths", 1),
    ("polytope-parentheses", "the simplex ($d + 1$ vertices) and hypercube ($2^d$ vertices)", 1),
    ("phi-cubed", r"a $\phi^3$ field theory", 1),
    ("geodesic-space", "`z = f[x, y]` this is equivalent", 1),
    ("quantum-group", r"quantum group $SU(2)_q$—and", 1),
    ("gauge-quotes", "“gauge” in space", 1),
    ("torsion-quotes", "word “torsion”. Here", 1),
    ("hidden-variable-quotes", "“hidden variable”", 1),
    ("entangled-quotes", "“entangled” state", 1),
    ("firing-five-width", "_page_1050_Firing_Squad_Five_Width_Group.jpeg", 1),
    ("source-native-probe", "will then to probe", 1),
    ("source-native-devices", "the actually devices", 1),
    ("source-native-flux", "fact that every point in the system the total flux", 1),
    ("planar-source-punctuation", "networks to be planar the numbers are", 1),
    ("integer-digits-code", "`IntegerDigits[n, 2, 8]`", 1),
    ("network-variable", "network *g* so that", 1),
    ("coordinate-expression", "$x[i, k]$ which minimize", 1),
    ("string-triple-code", '`{"AAABB", "ABABB", "ABAABB"}`', 1),
    ("sphere-volume-assignment", "Integrate[Sin[θ]^(d - 1), {θ, 0, r/a}] =", 1),
    ("small-ball-equation", r"$$\partial_{tt} v[t]/v[t] == -1/2(\rho + 3p)$$", 1),
    ("source-roman-s-matrices", "as S matrices for elementary evolution events", 1),
]


FORBIDDEN_LITERAL_PINS = [
    "Cycle lengths.** · Cycle lengths.",
    "the simplex (d+1) vertices)",
    r"$\phi$   $^3$",
    "10-3 level",
    "f[x, y]this",
    "SU(2),and",
    "string theory-there",
    "■■ , with",
    "“gauge\"",
    "“torsion\"",
    "“hidden variable\"",
    "“entangled\"",
    "<sup>",
    "</sup>",
    "<sub>",
    "</sub>",
    "\n• ",
    "\n  - ",
    "network q so that",
    "networks to be planar, the numbers are",
    "as *S* matrices for elementary evolution events",
    r"$$\partial_{tt} v[t]/v[t] = -1/2(\rho + 3p)$$",
]


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


def tree_manifest(root: Path) -> list[tuple[str, str]]:
    return [
        (path.relative_to(root).as_posix(), build.sha256(path.read_bytes()))
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    ]


class NotesForChapter9Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.document = next(row for row in cls.documents if row["id"] == "N09")
        cls.n08 = next(row for row in cls.documents if row["id"] == "N08")
        cls.n10 = next(row for row in cls.documents if row["id"] == "N10")
        cls.path = build.safe_relative_path(cls.document["output_path"], suffix=".md")
        cls.rendered_bytes = build.document_bytes(
            cls.raw, cls.documents, cls.corrections
        )[cls.path]
        cls.rendered = cls.rendered_bytes.decode("utf-8")
        cls.output_path = build.OUTPUT_ROOT / Path(cls.path)
        cls.rows = [row for row in cls.corrections if row["document_id"] == "N09"]
        cls.image_rows = [row for row in cls.images if row["document_id"] == "N09"]
        cls.added = [row for row in cls.added_assets if row["document_id"] == "N09"]
        cls.references = re.findall(r"!\[[^]]*\]\(([^)\n]+)\)", cls.rendered)
        cls.segment = cls.raw[
            cls.document["raw_start_byte"] : cls.document["raw_end_byte_exclusive"]
        ]

    def test_exact_source_range_correction_registry_and_boundaries(self) -> None:
        self.assertEqual(
            (
                self.document["raw_start_line"], self.document["raw_end_line"],
                self.document["raw_start_byte"], self.document["raw_end_byte_exclusive"],
                self.document["raw_line_count"], self.document["raw_byte_count"],
                self.document["raw_segment_sha256"],
                self.document["authoritative_pdf_start_page"],
                self.document["authoritative_pdf_end_page"],
                self.document["authoritative_printed_start"],
                self.document["authoritative_printed_end"],
            ),
            (16_012, 17_086, 2_339_807, 2_603_694, 1_075, 263_887,
             "a0e5b5ec39fa0d8c607d5d2505dc518552b500334f05f35bb30152c1ca4cf786",
             1033, 1082, "1017", "1066"),
        )
        self.assertEqual(build.sha256(self.segment[:256]), EXPECTED_RAW_FIRST_256_SHA256)
        self.assertEqual(build.sha256(self.segment[-256:]), EXPECTED_RAW_LAST_256_SHA256)
        self.assertEqual(self.n08["raw_end_byte_exclusive"], 2_339_807)
        self.assertEqual(self.n08["raw_end_line"] + 1, 16_012)
        self.assertEqual(self.n10["raw_start_byte"], 2_603_694)
        self.assertEqual(self.n10["raw_start_line"], 17_087)

        self.assertEqual(len(self.rows), FINAL_CORRECTION_COUNT)
        self.assertEqual(
            [row["id"] for row in self.rows],
            [f"G5-C-{number:04d}" for number in range(1912, 2806)],
        )
        self.assertEqual(rows_sha256(self.rows), FINAL_CORRECTION_ROWS_SHA256)
        self.assertEqual(
            row_hash_sequence_sha256(self.rows), FINAL_CORRECTION_SEQUENCE_SHA256
        )
        reserved = self.rows[0]
        self.assertEqual(
            (reserved["id"], reserved["raw_start_byte"], reserved["raw_line"]),
            ("G5-C-1912", 2_342_783, 16_027),
        )
        self.assertIn("OCR runaway", reserved["reason"])
        self.assertEqual(self.rows[1]["id"], "G5-C-1913")
        self.assertEqual(self.rows[1]["after"], "## Fundamental Physics")

        previous_end = self.document["raw_start_byte"]
        for row in sorted(self.rows, key=lambda value: value["raw_start_byte"]):
            with self.subTest(correction=row["id"]):
                self.assertEqual(set(row), build.CORRECTION_FIELDS | {"raw_line"})
                start = row["raw_start_byte"]
                before = row["before"].encode("utf-8")
                end = start + len(before)
                local = start - self.document["raw_start_byte"]
                self.assertGreaterEqual(start, previous_end)
                self.assertEqual(self.raw[start:end], before)
                self.assertEqual(self.segment.count(before), row["expected_count"])
                self.assertEqual(
                    row["raw_line"],
                    self.document["raw_start_line"] + self.segment[:local].count(b"\n"),
                )
                pages = [
                    int(page)
                    for page in re.findall(r"pdf:(\d{4})", row["authoritative_location"])
                ]
                printed = [
                    int(page)
                    for page in re.findall(
                        r"printed:(\d{3,4})", row["authoritative_location"]
                    )
                ]
                self.assertTrue(pages)
                self.assertEqual(printed, [page - 16 for page in pages])
                self.assertTrue(all(1033 <= page <= 1082 for page in pages))
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                previous_end = end

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
        fences = [line for line in lines if line.startswith("```")]
        inline_code = re.findall(r"(?<!`)`[^`\n]+`(?!`)", self.rendered)
        math_spans = re.findall(
            r"(?<!\$)\$(?!\$)(?:\\.|[^$\n])+?(?<!\$)\$(?!\$)", self.rendered
        )
        self.assertEqual(headings, EXPECTED_HEADINGS)
        self.assertEqual(
            (len(headings), len(labels), len(fences), len(inline_code),
             len(math_spans), len(self.references)),
            (16, 174, 76, 82, 403, 32),
        )
        self.assertTrue(all(line == "```" for line in fences))
        self.assertEqual(self.references, EXPECTED_REFERENCES)
        self.assertEqual(len(set(self.references)), 32)
        self.assertEqual(
            [
                number for number, line in enumerate(lines, 1)
                if line.endswith((" ", "\t"))
            ],
            [],
        )
        self.assertEqual(
            [
                (index, ord(character))
                for index, character in enumerate(self.rendered)
                if ord(character) < 32 and character not in "\n\t"
            ],
            [],
        )
        self.assertNotRegex(self.rendered, r"\$\s*\^[^$]*\$")

        quantum = self.rendered.split("■ **Quantum effects.**", 1)[1].split(
            "All of these effects", 1
        )[0]
        self.assertEqual(len(re.findall(r"^- ", quantum, flags=re.MULTILINE)), 26)
        self.assertNotIn("\n\n- Exclusion principle", quantum)

    def test_high_risk_source_and_technical_literals(self) -> None:
        for pin_id, literal, expected_count in REQUIRED_LITERAL_PINS:
            with self.subTest(required=pin_id):
                self.assertEqual(self.rendered.count(literal), expected_count)
        for literal in FORBIDDEN_LITERAL_PINS:
            with self.subTest(forbidden=literal):
                self.assertNotIn(literal, self.rendered)
        self.assertEqual(self.rendered.count("$10^{-3}$ level"), 2)
        diffusion_equations = (
            r"$\partial_t f[x, t] == c \, \partial_{xx} f[x, t]$",
            r"$f[x + dx, t] == f[x, t] + \partial_x f[x, t] dx + 1/2 \partial_{xx} f[x, t] dx^2 + ...$",
            r"$f[x, t+dt] == p_1 f[x-dx, t] + p_2 f[x, t] + p_3 f[x+dx, t]$",
            r"$p_1 + p_2 + p_3 == 1$",
            r"$p_1 == p_3$",
            r"$f[x, t + dt] == c (f[x - dx, t] + f[x + dx, t]) + (1 - 2c) f[x, t]$",
            r"$f[x, t] + dt \partial_t f[x, t] == f[x, t] + c dx^2 \partial_{xx} f[x, t]$",
            r"$\partial_t f[x, t] == \xi \, \partial_{xx} f[x, t]$",
        )
        for literal in diffusion_equations:
            with self.subTest(diffusion_equation=literal):
                self.assertEqual(self.rendered.count(literal), 1)
        for literal in (
            "*Size dependence.*", "*Additive rules.*", "*Updating orders.*",
            "*History.* Sequential cellular automata",
            "*Implementation.* The following will update triples",
            "any string of *A*’s and *B*’s",
        ):
            self.assertIn(literal, self.rendered)

        manifest = "\n".join(
            canonical_bytes(row).decode("utf-8")
            for row in self.rows + self.image_rows + self.added
        )
        self.assertNotRegex(manifest, r"N09-(?:SRC-PROP|TFP|VIS-C)")
        self.assertNotIn("FIRST_PASS", manifest)

    def test_all_image_rows_dispositions_repairs_and_output_hashes(self) -> None:
        self.assertEqual(len(self.image_rows), 70)
        self.assertEqual(
            [row["ordinal"] for row in self.image_rows], list(range(1232, 1302))
        )
        self.assertEqual(rows_sha256(self.image_rows), FINAL_IMAGE_ROWS_SHA256)
        changed = [
            row for row in self.image_rows
            if "reference_disposition" in row or "repaired_asset_relative_path" in row
        ]
        self.assertEqual(len(changed), 57)
        self.assertEqual(rows_sha256(changed), FINAL_CHANGED_IMAGE_ROWS_SHA256)
        counts = Counter(
            "omitted" if "reference_disposition" in row
            else "repaired" if "repaired_asset_relative_path" in row
            else "retained"
            for row in self.image_rows
        )
        self.assertEqual(counts, Counter({"omitted": 54, "retained": 13, "repaired": 3}))

        retained = {
            row["ordinal"]: Path(row["asset_relative_path"]).name
            for row in self.image_rows
            if "reference_disposition" not in row
            and "repaired_asset_relative_path" not in row
        }
        self.assertEqual(retained, EXPECTED_RETAINED)
        grouped: defaultdict[str, list[int]] = defaultdict(list)
        for row in self.image_rows:
            basename = Path(row["asset_relative_path"]).name
            legacy = build.LEGACY_ROOT / Path(row["asset_relative_path"])
            output = build.OUTPUT_ROOT / Path(self.path).parent / basename
            self.assertEqual(build.sha256(legacy.read_bytes()), row["asset_sha256"])
            if "reference_disposition" in row:
                self.assertEqual(
                    row["reference_disposition"], build.REDUNDANT_REFERENCE_DISPOSITION
                )
                self.assertNotIn(basename, self.references)
                matches = re.findall(r"G5-A-\d{4}", row["reference_reason"])
                self.assertEqual(len(matches), 1)
                grouped[matches[0]].append(row["ordinal"])
                self.assertEqual(output.read_bytes(), legacy.read_bytes())
            elif "repaired_asset_relative_path" in row:
                name, digest, dimensions, position = EXPECTED_REPAIRS[row["ordinal"]]
                repaired = REPO_ROOT / row["repaired_asset_relative_path"]
                payload = repaired.read_bytes()
                self.assertEqual(name, basename)
                self.assertEqual(build.sha256(payload), digest)
                self.assertEqual(build.jpeg_dimensions(payload), dimensions)
                self.assertEqual(output.read_bytes(), payload)
                self.assertEqual(self.references[position - 1], name)
            else:
                self.assertEqual(output.read_bytes(), legacy.read_bytes())
        self.assertEqual(
            {key: tuple(value) for key, value in grouped.items()},
            {key: value[3] for key, value in EXPECTED_ADDITIONS.items() if value[3]},
        )

    def test_additions_assets_and_visual_guards_are_exact(self) -> None:
        self.assertEqual(
            [row["id"] for row in self.added],
            [f"G5-A-{number:04d}" for number in range(103, 119)],
        )
        self.assertEqual(rows_sha256(self.added), FINAL_ADDITION_ROWS_SHA256)
        expected_asset_names = {
            value[0] for value in EXPECTED_ADDITIONS.values()
        } | {value[0] for value in EXPECTED_REPAIRS.values()}
        self.assertEqual(
            {path.name for path in (GOAL_DIR / "assets/N09").glob("*.jpeg")},
            expected_asset_names,
        )
        self.assertEqual(len(expected_asset_names), 19)

        for row in self.added:
            basename, digest, dimensions, _ordinals, position = EXPECTED_ADDITIONS[row["id"]]
            payload = (REPO_ROOT / row["asset_relative_path"]).read_bytes()
            output = build.OUTPUT_ROOT / Path(self.path).parent / basename
            with self.subTest(addition=row["id"]):
                self.assertEqual(set(row), build.ADDED_ASSET_FIELDS)
                self.assertEqual(Path(row["asset_relative_path"]).name, basename)
                self.assertEqual(build.sha256(payload), digest)
                self.assertEqual(row["asset_sha256"], digest)
                self.assertEqual(build.jpeg_dimensions(payload), dimensions)
                self.assertEqual((row["width_px"], row["height_px"]), dimensions)
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                self.assertEqual(output.read_bytes(), payload)
                self.assertEqual(self.references[position - 1], basename)

        guards: list[tuple[str, dict[str, Any]]] = []
        for row in self.rows:
            matches = re.findall(r"G5-A-01(?:0[3-9]|1[0-8])", row["reason"])
            if matches:
                self.assertEqual(len(matches), 1)
                guards.append((matches[0], row))
        self.assertEqual([row["id"] for _, row in guards], EXPECTED_VISUAL_GUARD_IDS)
        self.assertEqual({addition for addition, _ in guards}, set(EXPECTED_ADDITIONS))
        for addition_id, row in guards:
            basename, _digest, _dimensions, ordinals, position = EXPECTED_ADDITIONS[addition_id]
            self.assertIn(f"![]({basename})", row["after"])
            self.assertIn(addition_id, row["authoritative_location"])
            self.assertEqual(self.references[position - 1], basename)
            self.assertEqual(self.rendered.count(f"![]({basename})"), 1)
            if ordinals:
                partials = re.findall(r"!\[\]\(([^)\n]+)\)", row["before"])
                image_names = {
                    image["ordinal"]: Path(image["asset_relative_path"]).name
                    for image in self.image_rows
                }
                self.assertEqual(partials, [image_names[number] for number in ordinals])

    def test_authoritative_pdf_and_legacy_tree_are_immutable(self) -> None:
        range_data = json.loads(build.RANGES_PATH.read_text(encoding="utf-8"))
        source = range_data["authoritative_source"]
        self.assertEqual(
            (source["sha256"], source["size_bytes"], source["pdf_page_count"]),
            (EXPECTED_PDF_SHA256, 57_779_240, 1280),
        )
        pdf = validate.validate_authoritative_source(range_data)
        self.assertEqual(build.sha256(pdf.read_bytes()), EXPECTED_PDF_SHA256)
        self.assertEqual(validate.legacy_tree_digest(), EXPECTED_LEGACY_TREE)

    def test_normal_and_zero_builds_remain_deterministic(self) -> None:
        coverage = validate.validate_coverage(self.documents)
        n09_coverage = next(
            row for row in coverage if row["document_id"] == "N09"
        )
        self.assertEqual(
            (
                n09_coverage["first_pass"],
                n09_coverage["second_pass"],
                n09_coverage["reviewer_type"],
            ),
            ("YES", "YES", "agent"),
        )
        self.assertIn("894 guarded corrections", n09_coverage["notes"])
        self.assertIn("G5-C-1912 through G5-C-2805", n09_coverage["notes"])
        self.assertEqual(
            sum(row["second_pass"] == "YES" for row in coverage), 27
        )
        with tempfile.TemporaryDirectory(prefix="n09-build-") as directory:
            first = Path(directory) / "first"
            second = Path(directory) / "second"
            self.assertEqual(build.build(first), (29, 1607, 4830))
            self.assertEqual(build.build(second), (29, 1607, 4830))
            first_manifest = tree_manifest(first)
            self.assertEqual(first_manifest, tree_manifest(second))
            self.assertEqual(first_manifest, tree_manifest(build.OUTPUT_ROOT))
            self.assertEqual(len(first_manifest), 1638)
            self.assertEqual(validate.validate(first), (29, 1607, 4830, 27))

            zero = Path(directory) / "zero"
            self.assertEqual(build.build(zero, zero_corrections=True), (29, 1444, 0))
            self.assertEqual(len(tree_manifest(zero)), 1475)
            concatenated = b"".join(
                (zero / document["output_path"]).read_bytes()
                for document in self.documents
            )
            self.assertEqual(concatenated, self.raw)
            validate.validate_output(
                zero, self.raw, self.documents, [], self.images,
                zero_corrections=True,
            )


if __name__ == "__main__":
    unittest.main()
