#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
import unittest
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


# Final source-verified N08 integration pins. These values were derived from
# the fully integrated manifests and freshly rebuilt published target.
REPO_ROOT = (
    Path(os.environ["ANKOS_REPO_ROOT"])
    if "ANKOS_REPO_ROOT" in os.environ
    else Path(__file__).resolve().parents[2]
).resolve()
GOAL_DIR = REPO_ROOT / "goal-5"
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402
import validate  # noqa: E402


FINAL_CORRECTION_COUNT = 293
FINAL_CORRECTION_LAST_NUMBER = 1911
FINAL_TARGET_BYTES = 134_385
FINAL_TARGET_LFS = 358
FINAL_TARGET_SHA256 = (
    "3acc85433fca526eca898e6a0f116fc1017b88bb7b0048fc8f96f7d0afcead53"
)
FINAL_CORRECTION_ROWS_SHA256 = (
    "d372609e179446e6ea5b4f55d4bdd2e8eb031c5c6862f306104b476f33aa9411"
)
FINAL_CORRECTION_SEQUENCE_SHA256 = (
    "3e87300951493a07715e9f797befe63c91ee472305f52a9235f5ae4918bd6986"
)
FINAL_IMAGE_ROWS_SHA256 = (
    "ac54c92c628cc5c0042bf995884a2df4da6b98b40f66443eb5f6f412800ee219"
)
FINAL_CHANGED_IMAGE_ROWS_SHA256 = (
    "b2a3c74d62b0ec7f447c53082feaea2c2ee2283122eb226c8d0e863940b8a5c9"
)
FINAL_INLINE_CODE_COUNT = 23
FINAL_MATH_SPAN_COUNT = 128
FINAL_TRAILING_WHITESPACE_LINES = [263, 264, 265, 266, 267, 268]
FINAL_VISUAL_GUARD_IDS = [
    "G5-C-1653",
    "G5-C-1665",
    "G5-C-1720",
    "G5-C-1722",
    "G5-C-1804",
    "G5-C-1810",
    "G5-C-1817",
    "G5-C-1822",
    "G5-C-1892",
]


EXPECTED_RAW_FIRST_256_SHA256 = (
    "2f794ded978fca638b83aed2ac29f3cef2a6e42185070537a6838e414b3653b7"
)
EXPECTED_RAW_LAST_256_SHA256 = (
    "32ec631704d3a2ff7f18c45711988e61bcb2b231e679286d4a037eb54a2400a4"
)
EXPECTED_ADDED_ROWS_SHA256 = (
    "5daa5bdf8da17ea67441c26d7515d91d9a6704743972058dd3d6754a1ae07b8a"
)
EXPECTED_LEGACY_TREE = (
    "b9ff7b9b507790f1d519593baf2b2d2f24dd6cd49dc0fe10f0ac629278ea42f4",
    1463,
)
EXPECTED_PDF_SHA256 = (
    "a3cc5dd60e12d6b563aee86ea31a15b03f9cddfd4869b8f965d3a11bbc61a0d6"
)


EXPECTED_HEADINGS = [
    "## Implications for Everyday Systems",
    "### Issues of Modelling",
    "### The Growth of Crystals",
    "### The Breaking of Materials",
    "### Fluid Flow",
    "### Fundamental Issues in Biology",
    "### Growth of Plants and Animals",
    "### Biological Pigmentation Patterns",
    "### Financial Systems",
]


# addition id: (basename, SHA, dimensions, bytes, PDF, printed, ordinals,
#               final reference position)
EXPECTED_ADDITIONS: dict[str, tuple[str, str, tuple[int, int], int, int, int, tuple[int, ...], int]] = {
    "G5-A-0094": (
        "_page_1008_Hopper_Crystals_Four_Panel_Row.jpeg",
        "45e8795fdf982f5f7fba67661d1d44aad9a9a0c38ac24da9cf9ab6c09e2a3213",
        (1720, 410),
        313_190,
        1009,
        993,
        (1200, 1201, 1202, 1203),
        1,
    ),
    "G5-A-0095": (
        "_page_1009_Boiling_Heating_Rates_Two_Panel_Row.jpeg",
        "2f88db99fccef22422781eebae9e68cb449cf91cf518130374012450d3a08589",
        (1645, 420),
        183_484,
        1010,
        994,
        (1204, 1205),
        2,
    ),
    "G5-A-0096": (
        "_page_1015_Sound_Waves_Four_Step_Row.jpeg",
        "a33b2b6d625b9b5cd54039b2393b16437bed0ddac477ae84b15192b5cc97cd2a",
        (1725, 420),
        357_345,
        1016,
        1000,
        (1206, 1207, 1208, 1209),
        3,
    ),
    "G5-A-0097": (
        "_page_1015_Shocks_Three_Step_Row.jpeg",
        "f7342a6167c1563c1434ce4990518995ab651e7dfc691cdd78edf3ff186561cf",
        (1725, 590),
        794_218,
        1016,
        1000,
        (1210, 1211, 1212),
        4,
    ),
    "G5-A-0098": (
        "_page_1021_Mathematical_Leaf_Shapes_Five_Panel_Row.jpeg",
        "447f03843a24a76049a14f8dbe1b386382bff463463a59be6211a25c57dbfd7d",
        (1725, 340),
        94_715,
        1022,
        1006,
        (1214, 1215, 1216, 1217, 1218),
        6,
    ),
    "G5-A-0099": (
        "_page_1021_Parameter_Space_Connectedness_Two_Panel_Row.jpeg",
        "d358642211be38443b01bf46e6056908365d75eaf5011b38f551774b2cee00c0",
        (1190, 490),
        253_178,
        1022,
        1006,
        (1219, 1220),
        7,
    ),
    "G5-A-0100": (
        "_page_1022_Phyllotaxis_Projections_Two_Panel_Row.jpeg",
        "537381d0e5e0953a551c83ac43a157e940584d1b1cdf4718499b23db5eb04a7f",
        (1710, 825),
        588_220,
        1023,
        1007,
        (1221, 1222),
        8,
    ),
    "G5-A-0101": (
        "_page_1023_Locally_Isotropic_Growth_Four_Panel_Row.jpeg",
        "b4b218145bba73fb8055a0b7c84f6136fb1b922e5d5c56226c6f4746963ad103",
        (1715, 440),
        379_253,
        1024,
        1008,
        (1223, 1224, 1225, 1226),
        9,
    ),
    "G5-A-0102": (
        "_page_1029_Zipf_Frequency_Three_Plot_Row.jpeg",
        "092ad63cfc64de7c5f72d38817c6ea0b22fb10d77e141da4af17b6260cd9f4e9",
        (1695, 290),
        83_296,
        1030,
        1014,
        (1229, 1230, 1231),
        12,
    ),
}


EXPECTED_RETAINED = {
    1213: "_page_1020_Figure_8.jpeg",
    1227: "_page_1024_Picture_3.jpeg",
    1228: "_page_1028_Picture_8.jpeg",
}


EXPECTED_REFERENCES = [
    "_page_1008_Hopper_Crystals_Four_Panel_Row.jpeg",
    "_page_1009_Boiling_Heating_Rates_Two_Panel_Row.jpeg",
    "_page_1015_Sound_Waves_Four_Step_Row.jpeg",
    "_page_1015_Shocks_Three_Step_Row.jpeg",
    "_page_1020_Figure_8.jpeg",
    "_page_1021_Mathematical_Leaf_Shapes_Five_Panel_Row.jpeg",
    "_page_1021_Parameter_Space_Connectedness_Two_Panel_Row.jpeg",
    "_page_1022_Phyllotaxis_Projections_Two_Panel_Row.jpeg",
    "_page_1023_Locally_Isotropic_Growth_Four_Panel_Row.jpeg",
    "_page_1024_Picture_3.jpeg",
    "_page_1028_Picture_8.jpeg",
    "_page_1029_Zipf_Frequency_Three_Plot_Row.jpeg",
]


# These pins deliberately target the source omissions and the highest-risk
# technical objects. Counts should be adjudicated if the same literal appears
# elsewhere in N08, but the literal itself is source-sealed.
REQUIRED_LITERAL_PINS = [
    (
        "ordinary-differential-omission",
        "some simplified ordinary differential equations",
        1,
    ),
    (
        "cellular-fluid-history-article",
        "Following the development of the molecular model",
        1,
    ),
    (
        "ginger-terminal-period",
        r"ginger  $\{0.65, \, 0.6, \, 15^{\circ}\}$ .",
        1,
    ),
    (
        "fibonacci-prose-ellipsis",
        "(i.e. 1, 2, 3, 5, 8, 13, …)",
        1,
    ),
    (
        "reaction-diffusion-equality",
        r"$\partial_t c == d \cdot \partial_{xx} c + m \cdot c$",
        1,
    ),
    ("man-made-snow", "man-made snow", 1),
    ("crushing-parenthesis-omission", "are sometimes used.)", 1),
    (
        "computer-graphics-omission",
        "typical parametrizations used in computer graphics is not clear.",
        1,
    ),
    (
        "navier-stokes-omission",
        "next order corrections to the Navier-Stokes equations.",
        1,
    ),
    ("jet-stream-omission", "such as the jet stream.", 1),
    ("genetic-programs-omission", "Genetic programs are encoded", 1),
    ("cas-pattern", "CAStep[rule_List, a_] := Map[rule[[14 - #]] &,", 1),
    (
        "hex-table",
        "Table[{i Sqrt[3], j}, {i, 1, m}, {j, Mod[i, 2], n, 2}]",
        1,
    ),
    ("reynolds-nu", r"$Re = U L/\nu$", 1),
    ("reynolds-range", r"$50 \lesssim R \lesssim 150$", 1),
    (
        "depth-mathematica",
        "equal to `Depth` for trees given as *Mathematica* expressions",
        1,
    ),
    (
        "tree-nest",
        "Nest[Flatten[Outer[Times, 1 + #, b]] &, {0}, n]",
        1,
    ),
    ("tree-total-length", "`Apply[Plus, Abs[b]]^n`", 1),
    ("parameter-axis", "`Im[c] == 0`", 1),
    (
        "parameter-with",
        "With[{d = Conjugate[c], r = 1 - Abs[c]^2},",
        1,
    ),
    (
        "parameter-power",
        "Im[c (1 - d^n)/(1 - d)] + Im[c d^n (1 + d)]/r",
        1,
    ),
    (
        "boundary-sequence",
        r"$\{0, 1, 1, 1, 0, 1, 0, 1, 0, 1, ...\}$",
        1,
    ),
    (
        "golden-ratio-identity",
        r"$GoldenRatio == (1 + \sqrt{5})/2$",
        1,
    ),
    (
        "golden-ratio-second-identity",
        r"$2 - GoldenRatio == GoldenRatio^{-2} \simeq 0.38$",
        1,
    ),
    ("golden-ratio-identifier", r"2 \pi n GoldenRatio", 1),
    ("laplacian-pattern", "`Laplacian[f_] :=`", 1),
    ("shell-close-brace", "\\right\\}", 1),
    (
        "ndsolve-equalities",
        "NDSolve[{x'[s] == Cos[θ[s]], y'[s] == Sin[θ[s]], θ'[s] ==",
        1,
    ),
    ("ndsolve-final-delimiter", "{s, 0, Subscript[s, max]}]", 1),
    ("weighted-pattern", "WeightedStep[w_List, a_] :=", 1),
    ("layer-pattern", "Layer[n_] := Layer[n] = Select", 1),
    ("zipf-nth", r"$n^{\text{th}}$ most common word", 1),
    ("zipf-frequency", r"frequency $1/n$", 1),
    ("zipf-normalization", r"$p = 1/(2k)$", 1),
]


FORBIDDEN_LITERAL_PINS = [
    (
        "missing-ordinary-differential",
        "some simplified differential equations",
    ),
    (
        "missing-cellular-fluid-history-article",
        "Following development of the molecular model",
    ),
    (
        "missing-ginger-terminal-period",
        "ginger  $\\{0.65, \\, 0.6, \\, 15^{\\circ}\\}$ \n\n",
    ),
    (
        "ascii-fibonacci-prose-ellipsis",
        "(i.e. 1, 2, 3, 5, 8, 13, ...)",
    ),
    (
        "reaction-diffusion-single-equality",
        r"$\partial_t c = d \cdot \partial_{xx} c + m \cdot c$",
    ),
    ("missing-computer-graphics-end", "computer graphics is\n\n"),
    ("missing-navier-stokes-end", "Navier-Stokes\n\nAbove the speed"),
    ("missing-genetic-are", "Genetic programs encoded"),
    ("escaped-cas-pattern", r"CAStep[rule\_List, a\_]"),
    ("tight-rule-index", "rule[[14-#]]"),
    ("latin-viscosity", "Re = U L/v"),
    ("wrong-reynolds-operators", r"50 \le R \le 150"),
    ("parameter-single-equality", "Im[c] = 0"),
    ("broken-parameter-power", "Im[c(1-d^))/(1-d)]"),
    (
        "extra-boundary-one",
        r"$\{0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, ...\}$",
    ),
    (
        "double-zero-boundary-sequence",
        r"$\{0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, ...\}$",
    ),
    ("golden-ratio-single-equality", r"GoldenRatio = (1 + \sqrt{5})/2"),
    ("split-golden-ratio", r"2 \pi n Golden Ratio"),
    ("broken-laplacian-pattern", "Laplacian[f_{-}]"),
    ("ndsolve-single-equality", "NDSolve[{x'[s] = Cos"),
    ("escaped-weighted-pattern", r"WeightedStep[w\_List, a\_]"),
    ("spurious-end-cases", r"\end{cases}"),
    ("html-superscript", "<sup>"),
    ("html-code", "<code>"),
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
        (
            path.relative_to(root).as_posix(),
            hashlib.sha256(path.read_bytes()).hexdigest(),
        )
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    ]


def require_finalized() -> None:
    pins = {
        "FINAL_CORRECTION_COUNT": FINAL_CORRECTION_COUNT,
        "FINAL_CORRECTION_LAST_NUMBER": FINAL_CORRECTION_LAST_NUMBER,
        "FINAL_TARGET_BYTES": FINAL_TARGET_BYTES,
        "FINAL_TARGET_LFS": FINAL_TARGET_LFS,
        "FINAL_TARGET_SHA256": FINAL_TARGET_SHA256,
        "FINAL_CORRECTION_ROWS_SHA256": FINAL_CORRECTION_ROWS_SHA256,
        "FINAL_CORRECTION_SEQUENCE_SHA256": FINAL_CORRECTION_SEQUENCE_SHA256,
        "FINAL_IMAGE_ROWS_SHA256": FINAL_IMAGE_ROWS_SHA256,
        "FINAL_CHANGED_IMAGE_ROWS_SHA256": FINAL_CHANGED_IMAGE_ROWS_SHA256,
        "FINAL_INLINE_CODE_COUNT": FINAL_INLINE_CODE_COUNT,
        "FINAL_MATH_SPAN_COUNT": FINAL_MATH_SPAN_COUNT,
        "FINAL_TRAILING_WHITESPACE_LINES": FINAL_TRAILING_WHITESPACE_LINES,
        "FINAL_VISUAL_GUARD_IDS": FINAL_VISUAL_GUARD_IDS,
    }
    missing = [name for name, value in pins.items() if value is None]
    if missing:
        raise AssertionError(
            "N08 draft was installed before final pins were derived: "
            + ", ".join(missing)
        )


class NotesForChapter8Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        require_finalized()
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.document = next(row for row in cls.documents if row["id"] == "N08")
        cls.n07 = next(row for row in cls.documents if row["id"] == "N07")
        cls.n09 = next(row for row in cls.documents if row["id"] == "N09")
        cls.path = build.safe_relative_path(cls.document["output_path"], suffix=".md")
        cls.rendered_bytes = build.document_bytes(
            cls.raw, cls.documents, cls.corrections
        )[cls.path]
        cls.rendered = cls.rendered_bytes.decode("utf-8")
        cls.output_path = build.OUTPUT_ROOT / Path(cls.path)
        cls.rows = [row for row in cls.corrections if row["document_id"] == "N08"]
        cls.image_rows = [row for row in cls.images if row["document_id"] == "N08"]
        cls.added = [row for row in cls.added_assets if row["document_id"] == "N08"]
        cls.references = re.findall(r"!\[[^]]*\]\(([^)\n]+)\)", cls.rendered)
        cls.segment = cls.raw[
            cls.document["raw_start_byte"] : cls.document["raw_end_byte_exclusive"]
        ]

    def test_exact_source_range_corrections_and_ownership_joins(self) -> None:
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
                15_583,
                16_011,
                2_206_052,
                2_339_807,
                429,
                133_755,
                "c0540e327e3eaf20cb6aea65dfa0cea44a23c8e98c736702eae5331d735d2718",
                1007,
                1032,
                "991",
                "1016",
            ),
        )
        self.assertEqual(build.sha256(self.segment[:256]), EXPECTED_RAW_FIRST_256_SHA256)
        self.assertEqual(build.sha256(self.segment[-256:]), EXPECTED_RAW_LAST_256_SHA256)
        self.assertEqual(len(self.rows), FINAL_CORRECTION_COUNT)
        self.assertEqual(
            [row["id"] for row in self.rows],
            [
                f"G5-C-{number:04d}"
                for number in range(1619, int(FINAL_CORRECTION_LAST_NUMBER) + 1)
            ],
        )
        self.assertEqual(
            int(FINAL_CORRECTION_LAST_NUMBER) - 1619 + 1,
            FINAL_CORRECTION_COUNT,
        )
        self.assertEqual(rows_sha256(self.rows), FINAL_CORRECTION_ROWS_SHA256)
        self.assertEqual(
            row_hash_sequence_sha256(self.rows), FINAL_CORRECTION_SEQUENCE_SHA256
        )

        previous_end = self.document["raw_start_byte"]
        for row in sorted(self.rows, key=lambda value: value["raw_start_byte"]):
            with self.subTest(correction=row["id"]):
                self.assertEqual(set(row), build.CORRECTION_FIELDS | {"raw_line"})
                start = row["raw_start_byte"]
                before = row["before"].encode("utf-8")
                end = start + len(before)
                local = start - self.document["raw_start_byte"]
                self.assertGreaterEqual(start, previous_end)
                self.assertLessEqual(end, self.document["raw_end_byte_exclusive"])
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
                self.assertTrue(all(1007 <= page <= 1032 for page in pages))
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                previous_end = end

        self.assertEqual(self.n07["raw_end_byte_exclusive"], 2_206_052)
        self.assertEqual(self.n07["raw_end_line"] + 1, 15_583)
        self.assertEqual(self.n09["raw_start_byte"], 2_339_807)
        self.assertEqual(self.n09["raw_start_line"], 16_012)
        self.assertNotIn("## Fundamental Physics", self.rendered)

    def test_exact_final_render_and_two_terminal_lfs(self) -> None:
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

    def test_markdown_structure_is_balanced_exact_and_clean(self) -> None:
        lines = self.rendered.splitlines()
        headings = [line for line in lines if line.startswith("#")]
        labels = [line for line in lines if line.startswith("■ **")]
        fences = [line for line in lines if line.startswith("```")]
        inline_code = re.findall(r"(?<!`)`[^`\n]+`(?!`)", self.rendered)
        math_spans = re.findall(
            r"(?<!\$)\$(?!\$)(?:\\.|[^$\n])+?(?<!\$)\$(?!\$)",
            self.rendered,
        )
        self.assertEqual(headings, EXPECTED_HEADINGS)
        self.assertEqual([len(headings), len(labels), len(fences), len(self.references)], [9, 128, 12, 12])
        self.assertEqual(len(inline_code), FINAL_INLINE_CODE_COUNT)
        self.assertEqual(len(math_spans), FINAL_MATH_SPAN_COUNT)
        self.assertTrue(all(line == "```" for line in fences))
        self.assertEqual(len(fences) % 2, 0)
        self.assertEqual(self.references, EXPECTED_REFERENCES)
        self.assertEqual(len(set(self.references)), 12)
        self.assertTrue(
            all(path.endswith(".jpeg") and "/" not in path for path in self.references)
        )
        self.assertEqual(
            [
                (index, ord(character))
                for index, character in enumerate(self.rendered)
                if ord(character) < 32 and character not in "\n\t"
            ],
            [],
        )
        self.assertEqual(
            [
                number
                for number, line in enumerate(self.rendered.splitlines(), 1)
                if line.endswith((" ", "\t"))
            ],
            FINAL_TRAILING_WHITESPACE_LINES,
        )

    def test_all_thirty_two_image_rows_and_dispositions_are_exact(self) -> None:
        self.assertEqual(len(self.image_rows), 32)
        self.assertEqual(
            [row["ordinal"] for row in self.image_rows], list(range(1200, 1232))
        )
        self.assertEqual(rows_sha256(self.image_rows), FINAL_IMAGE_ROWS_SHA256)
        changed = [
            row
            for row in self.image_rows
            if "reference_disposition" in row
            or "repaired_asset_relative_path" in row
        ]
        self.assertEqual(len(changed), 29)
        self.assertEqual(rows_sha256(changed), FINAL_CHANGED_IMAGE_ROWS_SHA256)
        self.assertEqual(
            [row["ordinal"] for row in changed],
            [number for number in range(1200, 1232) if number not in EXPECTED_RETAINED],
        )
        self.assertFalse(
            [row for row in self.image_rows if "repaired_asset_relative_path" in row]
        )

        grouped: dict[str, list[int]] = defaultdict(list)
        for row in changed:
            self.assertEqual(
                row["reference_disposition"], build.REDUNDANT_REFERENCE_DISPOSITION
            )
            self.assertEqual(
                build.REFERENCE_DISPOSITION_FIELDS & set(row),
                build.REFERENCE_DISPOSITION_FIELDS,
            )
            self.assertEqual(row["reference_reviewer_type"], "agent")
            self.assertEqual(row["reference_verification_status"], "SOURCE_VERIFIED")
            matches = re.findall(r"G5-A-\d{4}", row["reference_reason"])
            self.assertEqual(len(matches), 1)
            grouped[matches[0]].append(row["ordinal"])
            self.assertNotIn(Path(row["asset_relative_path"]).name, self.references)
        self.assertEqual(
            {key: tuple(value) for key, value in grouped.items()},
            {key: value[6] for key, value in EXPECTED_ADDITIONS.items()},
        )

        retained = {
            row["ordinal"]: Path(row["asset_relative_path"]).name
            for row in self.image_rows
            if "reference_disposition" not in row
        }
        self.assertEqual(retained, EXPECTED_RETAINED)
        self.assertEqual(self.references, EXPECTED_REFERENCES)
        self.assertEqual(Counter(self.references), Counter(set(self.references)))

        for row in self.image_rows:
            basename = Path(row["asset_relative_path"]).name
            legacy = build.LEGACY_ROOT / Path(row["asset_relative_path"])
            output = build.OUTPUT_ROOT / Path(self.path).parent / basename
            with self.subTest(mapped_output=basename):
                self.assertTrue(legacy.is_file())
                self.assertTrue(output.is_file())
                self.assertEqual(build.sha256(legacy.read_bytes()), row["asset_sha256"])
                self.assertEqual(output.read_bytes(), legacy.read_bytes())

    def test_nine_additions_are_byte_exact_and_in_source_order(self) -> None:
        self.assertEqual(
            [row["id"] for row in self.added],
            [f"G5-A-{number:04d}" for number in range(94, 103)],
        )
        self.assertEqual(rows_sha256(self.added), EXPECTED_ADDED_ROWS_SHA256)
        self.assertEqual(set(EXPECTED_ADDITIONS), {row["id"] for row in self.added})
        expected_paths = {
            f"goal-5/assets/N08/{value[0]}" for value in EXPECTED_ADDITIONS.values()
        }
        actual_paths = {
            path.relative_to(REPO_ROOT).as_posix()
            for path in (GOAL_DIR / "assets/N08").glob("*.jpeg")
        }
        self.assertEqual(actual_paths, expected_paths)

        for row in self.added:
            (
                basename,
                digest,
                dimensions,
                byte_count,
                pdf_page,
                printed_page,
                _ordinals,
                position,
            ) = EXPECTED_ADDITIONS[row["id"]]
            source = REPO_ROOT / row["asset_relative_path"]
            output = build.OUTPUT_ROOT / Path(self.path).parent / basename
            payload = source.read_bytes()
            with self.subTest(added=row["id"]):
                self.assertEqual(set(row), build.ADDED_ASSET_FIELDS)
                self.assertEqual(Path(row["asset_relative_path"]).name, basename)
                self.assertEqual(len(payload), byte_count)
                self.assertEqual(build.sha256(payload), digest)
                self.assertEqual(row["asset_sha256"], digest)
                self.assertEqual(build.jpeg_dimensions(payload), dimensions)
                self.assertEqual((row["width_px"], row["height_px"]), dimensions)
                self.assertIn(f"pdf:{pdf_page:04d}", row["authoritative_location"])
                self.assertIn(f"printed:{printed_page}", row["authoritative_location"])
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                self.assertEqual(output.read_bytes(), payload)
                self.assertEqual(self.references[position - 1], basename)

    def test_nine_visual_reference_guards_are_exact_and_final(self) -> None:
        guards = []
        for row in self.rows:
            matches = re.findall(r"G5-A-(?:009[4-9]|010[0-2])", row["reason"])
            if matches:
                self.assertEqual(len(matches), 1)
                guards.append((matches[0], row))
        self.assertEqual([row["id"] for _, row in guards], FINAL_VISUAL_GUARD_IDS)
        self.assertEqual({addition for addition, _ in guards}, set(EXPECTED_ADDITIONS))

        by_id = dict(guards)
        image_by_ordinal = {
            row["ordinal"]: Path(row["asset_relative_path"]).name
            for row in self.image_rows
        }
        for addition_id, expected in EXPECTED_ADDITIONS.items():
            row = by_id[addition_id]
            basename, _digest, _dims, _bytes, _pdf, _printed, ordinals, position = expected
            partials = re.findall(r"!\[\]\(([^)\n]+)\)", row["before"])
            final = re.fullmatch(r"!\[\]\(([^)\n]+)\)", row["after"])
            with self.subTest(visual_guard=addition_id):
                self.assertEqual(partials, [image_by_ordinal[number] for number in ordinals])
                self.assertIsNotNone(final)
                self.assertEqual(final.group(1), basename)  # type: ignore[union-attr]
                self.assertIn(addition_id, row["authoritative_location"])
                self.assertIn(addition_id, row["reason"])
                self.assertNotIn("proposed", row["reason"].lower())
                self.assertEqual(self.rendered.count(row["after"]), 1)
                self.assertEqual(self.references[position - 1], basename)
                for partial in partials:
                    self.assertNotIn(f"![]({partial})", self.rendered)

    def test_high_risk_source_and_technical_literals(self) -> None:
        for pin_id, literal, expected_count in REQUIRED_LITERAL_PINS:
            with self.subTest(required_pin=pin_id):
                self.assertEqual(self.rendered.count(literal), expected_count)
        for pin_id, literal in FORBIDDEN_LITERAL_PINS:
            with self.subTest(forbidden_pin=pin_id):
                self.assertNotIn(literal, self.rendered)

        parameter_explanations = [
            paragraph
            for paragraph in self.rendered.split("\n\n")
            if paragraph.startswith(
                "In the pictures in the main text, the black region is connected"
            )
        ]
        self.assertEqual(len(parameter_explanations), 1)
        parameter_explanation = parameter_explanations[0]
        self.assertEqual(parameter_explanation.count("$c$"), 4)
        for literal in (
            "near any particular value of $c$",
            "for that value of $c$",
            "if $c$ changes only slightly",
            "in a small region of $c$ values",
        ):
            with self.subTest(parameter_explanation=literal):
                self.assertEqual(parameter_explanation.count(literal), 1)

        manifest = "\n".join(
            canonical_bytes(row).decode("utf-8")
            for row in self.rows + self.image_rows + self.added
        )
        self.assertNotRegex(
            manifest,
            r"N08-(?:SRC-PROP|TFP|PROP|VP|A-PROV|C-PROV)",
        )
        self.assertNotIn("FIRST_PASS", manifest)
        self.assertNotIn("proposed canonical", manifest)

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

    def test_normal_build_is_deterministic_and_matches_published_tree(self) -> None:
        _, documents, corrections, images = build.load_inputs()
        added_assets = build.load_added_assets(documents, images)
        expected_build = (
            len(documents),
            len(images) + len(added_assets),
            len(corrections),
        )
        coverage = validate.validate_coverage(documents)
        expected_validation = expected_build + (
            sum(row["second_pass"] == "YES" for row in coverage),
        )
        with tempfile.TemporaryDirectory(prefix="n08-normal-build-") as directory:
            first = Path(directory) / "first"
            second = Path(directory) / "second"
            self.assertEqual(build.build(first), expected_build)
            self.assertEqual(build.build(second), expected_build)
            first_manifest = tree_manifest(first)
            self.assertEqual(first_manifest, tree_manifest(second))
            self.assertEqual(first_manifest, tree_manifest(build.OUTPUT_ROOT))
            self.assertEqual(len(first_manifest), sum(expected_build[:2]) + 2)
            self.assertEqual(validate.validate(first), expected_validation)

    def test_zero_build_still_reassembles_the_immutable_monolith(self) -> None:
        with tempfile.TemporaryDirectory(prefix="n08-zero-build-") as directory:
            output = Path(directory) / "zero"
            self.assertEqual(build.build(output, zero_corrections=True), (29, 1444, 0))
            manifest = tree_manifest(output)
            self.assertEqual(len(manifest), 1475)
            concatenated = b"".join(
                (output / document["output_path"]).read_bytes()
                for document in self.documents
            )
            self.assertEqual(concatenated, self.raw)
            validate.validate_output(
                output,
                self.raw,
                self.documents,
                [],
                self.images,
                zero_corrections=True,
            )


if __name__ == "__main__":
    unittest.main()
