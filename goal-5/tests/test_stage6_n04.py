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


EXPECTED_SHA256 = "f882f0d87558eb4cdfdb21e67d49c06e0052c8456e52aa09cfdddc3a1eb859da"
EXPECTED_BYTES = 115_681
EXPECTED_LINES = 1_026
EXPECTED_CORRECTIONS_SHA256 = (
    "7c13c61d7678bc2ecec7416e3bce4e91ace394219868df439d2bd0c5d5092968"
)
EXPECTED_IMAGE_ROWS_SHA256 = (
    "c00359a797473057a847aef362c8ee6e9072010d946dfa07828593094843bb17"
)
EXPECTED_ADDED_ROWS_SHA256 = (
    "3381cb267b972e772b0bafaf7496a6b6762eff75bc9e01e467bfaa75b9c895d6"
)
EXPECTED_MAIN_LABELS_SHA256 = (
    "c5dfdd31ef58354101048c061ca4776667f96cfb5da9ca321a127e93986feca3"
)
EXPECTED_HEADINGS_SHA256 = (
    "1c0d092fa0c96aa19d14fff63ec369ef4118ffab8d1c919422c194d40dac18a2"
)
EXPECTED_MAPPED_NAMES_SHA256 = (
    "cb4deff02d891ea263566a8e88f96dd58c32108a44350b0cff8dcbadd0546b6b"
)
EXPECTED_RETAINED_REFERENCES_SHA256 = (
    "0b8c8788a03f83f3535ead27136587bc73333d607b4f4875f3ea3f796ad21cfd"
)
EXPECTED_ALL_REFERENCES_SHA256 = (
    "78d28e7ce11bdeb6fb2197de601b940f8ddc755fd36b3721d8ad5a36cbd1b14c"
)
EXPECTED_EMPHASIS_COUNTS = {
    "BOLD": 110,
    "BOLD_ITALIC": 0,
    "ITALIC_NESTED_IN_BOLD": 0,
    "ITALIC": 190,
}

EXPECTED_DISPOSITION_ORDINALS = [
    927,
    928,
    929,
    931,
    932,
    933,
    934,
    935,
    942,
    943,
    952,
    953,
    954,
    955,
    956,
    957,
    962,
    963,
    964,
    965,
    966,
    970,
    971,
    979,
    981,
    982,
    983,
    985,
    986,
    987,
]

EXPECTED_REPLACEMENT_GROUPS = {
    (927, 928, 929): ("G5-A-0053", 921),
    (931, 932, 933, 934, 935): ("G5-A-0050", 922),
    (942, 943): ("G5-A-0054", 925),
    (952, 953, 954, 955, 956, 957): ("G5-A-0055", 930),
    (962, 963, 964, 965, 966): ("G5-A-0056", 932),
    (970, 971): ("G5-A-0057", 933),
    (979,): ("G5-A-0058", 938),
    (981, 982, 983): ("G5-A-0059", 939),
    (985, 986, 987): ("G5-A-0060", 940),
}

# asset id: (basename, digest, dimensions, bytes, canonical PDF page)
EXPECTED_ADDED = {
    "G5-A-0050": (
        "_page_921_iterated_bitwise_operations_six_panel_row.jpeg",
        "916b5e32245602e09f6bd8a1a5f1619e7475066c9e37052641c3a2b424edd7d1",
        (1697, 331),
        139_212,
        922,
    ),
    "G5-A-0051": (
        "_page_938_wave_equation_1d_2d_3d_time_slices.jpeg",
        "ecad084efa2d6f7faffefc2edfe25c60c1271410a6ddc757ae639e339efb414b",
        (1710, 412),
        120_607,
        939,
    ),
    "G5-A-0052": (
        "_page_932_three_sine_functions_lower_contour.jpeg",
        "5b3e50512f0fb99832d992f99aea88f3465101ee0c8a8a813b9f709d8f913424",
        (1709, 404),
        280_246,
        933,
    ),
    "G5-A-0053": (
        "_page_920_digit_reversal_three_panel_row.jpeg",
        "ddca9aa140a931d288af0e1a608f966d2237cd22ad6cbd8633e49421e19a394c",
        (1687, 468),
        303_144,
        921,
    ),
    "G5-A-0054": (
        "_page_924_divisors_two_panel_row.jpeg",
        "23f79c952ced337631dd2ec6f1a89d728657990b6d995cf7c919e320ddd4177b",
        (1709, 355),
        159_234,
        925,
    ),
    "G5-A-0055": (
        "_page_929_continued_fraction_iterates_six_panel_row.jpeg",
        "4dcaa9580be68835447b36758c80e72bc05031349ad98e8bd802de71b321ff68",
        (1688, 469),
        342_981,
        930,
    ),
    "G5-A-0056": (
        "_page_931_digital_slope_five_panel_row.jpeg",
        "4c59262db498f8279d18d2c0e38c27d38a26d89684bed07b1c05c4d3e8ad9894",
        (1704, 533),
        172_220,
        932,
    ),
    "G5-A-0057": (
        "_page_932_zero_spacing_two_panel_row.jpeg",
        "30c07f2c1b5570b3925cdebeb91f819274f07d1863c65b72673935ed36ac8fd4",
        (1710, 304),
        76_753,
        933,
    ),
    "G5-A-0058": (
        "_page_937_continuous_ca_successive_colors_clean.jpeg",
        "56b13c5850925119fc9478cf59cb1ea293a1573d1e89a4216794fed3d16c349d",
        (1705, 955),
        695_357,
        938,
    ),
    "G5-A-0059": (
        "_page_938_pde_nonlinearity_three_panel_row.jpeg",
        "a2d52180dff2afc40b52f089af5b96278ed3e4634f9b9c55d4673d4e2460af03",
        (1698, 583),
        178_203,
        939,
    ),
    "G5-A-0060": (
        "_page_939_pde_convergence_three_panel_row.jpeg",
        "6054d0bf73934126a4948fb72c73384ae3437ec5be2d6f9444f81e75bf5d2550",
        (1708, 338),
        101_797,
        940,
    ),
}


class NotesForChapter4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.document = next(row for row in cls.documents if row["id"] == "N04")
        cls.path = build.safe_relative_path(cls.document["output_path"], suffix=".md")
        cls.rendered_bytes = build.document_bytes(
            cls.raw, cls.documents, cls.corrections
        )[cls.path]
        cls.rendered = cls.rendered_bytes.decode("utf-8")
        cls.output_path = build.OUTPUT_ROOT / Path(cls.path)
        cls.n04_corrections = [
            row for row in cls.corrections if row["document_id"] == "N04"
        ]
        cls.n04_images = [
            row for row in cls.images if row["document_id"] == "N04"
        ]
        cls.n04_added = [
            row for row in cls.added_assets if row["document_id"] == "N04"
        ]
        cls.n05_document = next(row for row in cls.documents if row["id"] == "N05")
        cls.n05_images = [
            row for row in cls.images if row["document_id"] == "N05"
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
                12499,
                13459,
                1792864,
                1908092,
                961,
                115228,
                "d72cde3ea798f8e47fb9d58973168adf89faa6996353fea62e72e5abb8d3a292",
                917,
                942,
                "901",
                "926",
            ),
        )
        segment = self.raw[1792864:1908092]
        self.assertEqual(len(segment), 115228)
        self.assertEqual(build.sha256(segment), self.document["raw_segment_sha256"])

        self.assertEqual(len(self.n04_corrections), 74)
        self.assertEqual(
            [row["id"] for row in self.n04_corrections],
            [f"G5-C-{number:04d}" for number in range(974, 1048)],
        )
        self.assertEqual(
            self.rows_sha256(self.n04_corrections), EXPECTED_CORRECTIONS_SHA256
        )
        self.assertEqual(len({row["before"] for row in self.n04_corrections}), 74)

        previous_end = self.document["raw_start_byte"]
        for row in sorted(
            self.n04_corrections, key=lambda item: item["raw_start_byte"]
        ):
            with self.subTest(correction=row["id"]):
                self.assertEqual(set(row), build.CORRECTION_FIELDS | {"raw_line"})
                self.assertEqual(row["document_id"], "N04")
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
                    self.document["raw_start_line"] + segment[:local].count(b"\n"),
                )
                pages = [
                    int(value)
                    for value in re.findall(
                        r"pdf:(\d{4})", row["authoritative_location"]
                    )
                ]
                self.assertTrue(pages)
                self.assertTrue(all(917 <= page <= 942 for page in pages))
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
                "## Systems Based on Numbers",
                "### The Notion of Numbers",
                "### Elementary Arithmetic",
                "### Recursive Sequences",
                "### The Sequence of Primes",
                "### Mathematical Constants",
                "### Mathematical Functions",
                "### Iterated Maps and the Chaos Phenomenon",
                "### Continuous Cellular Automata",
                "### Partial Differential Equations",
                "### Continuous Versus Discrete Systems",
            ],
        )
        self.assertEqual(self.sequence_sha256(headings), EXPECTED_HEADINGS_SHA256)
        labels = re.findall(r"(?m)^■ \*\*(.+?)\*\*", self.rendered)
        self.assertEqual(len(labels), 110)
        self.assertEqual(self.sequence_sha256(labels), EXPECTED_MAIN_LABELS_SHA256)
        self.assertEqual(len(re.findall(r"(?m)^▪ ", self.rendered)), 8)
        self.assertEqual(self.rendered.count("```"), 94)
        self.assertEqual(
            len(re.findall(r"(?<!`)`[^`\n]+`(?!`)", self.rendered)), 318
        )
        self.assertEqual(
            len(re.findall(r"(?<!\\)\$[^$\n]+(?<!\\)\$", self.rendered)),
            135,
        )
        self.assertEqual(self.rendered.count("$$"), 12)
        self.assertEqual(
            len(re.findall(r"(?i)\bpages? \d+(?:[-–]\d+)?", self.rendered)),
            140,
        )
        emphasis = self.emphasis_counts(self.rendered)
        self.assertEqual(emphasis, EXPECTED_EMPHASIS_COUNTS)
        self.assertEqual(sum(emphasis.values()), 300)
        self.assertEqual(self.rendered.count("’"), 28)
        self.assertEqual(self.rendered.count("“"), 12)
        self.assertEqual(self.rendered.count("”"), 12)
        self.assertEqual(self.rendered.count("*Mathematica*"), 10)
        self.assertNotIn("####", self.rendered)

    def test_mapped_inventory_dispositions_and_order_are_exact(self) -> None:
        self.assertEqual(len(self.n04_images), 71)
        self.assertEqual(
            [row["ordinal"] for row in self.n04_images], list(range(918, 989))
        )
        self.assertEqual(self.rows_sha256(self.n04_images), EXPECTED_IMAGE_ROWS_SHA256)
        mapped_names = [
            Path(row["asset_relative_path"]).name for row in self.n04_images
        ]
        self.assertEqual(
            self.sequence_sha256(mapped_names), EXPECTED_MAPPED_NAMES_SHA256
        )

        disposition_rows = [
            row for row in self.n04_images if "reference_disposition" in row
        ]
        self.assertEqual(
            [row["ordinal"] for row in disposition_rows],
            EXPECTED_DISPOSITION_ORDINALS,
        )
        for row in disposition_rows:
            with self.subTest(ordinal=row["ordinal"]):
                self.assertEqual(
                    row["reference_disposition"],
                    build.REDUNDANT_REFERENCE_DISPOSITION,
                )
                self.assertEqual(
                    build.REFERENCE_DISPOSITION_FIELDS & set(row),
                    build.REFERENCE_DISPOSITION_FIELDS,
                )
                self.assertTrue(
                    row["reference_authoritative_location"].startswith("pdf:09")
                )
                self.assertTrue(row["reference_reason"].strip())
                self.assertEqual(row["reference_reviewer_type"], "agent")
                self.assertEqual(
                    row["reference_verification_status"], "SOURCE_VERIFIED"
                )
        for ordinals, (replacement_id, pdf_page) in EXPECTED_REPLACEMENT_GROUPS.items():
            group = [row for row in disposition_rows if row["ordinal"] in ordinals]
            self.assertEqual([row["ordinal"] for row in group], list(ordinals))
            for row in group:
                self.assertIn(replacement_id, row["reference_reason"])
                self.assertTrue(
                    row["reference_authoritative_location"].startswith(
                        f"pdf:{pdf_page:04d}"
                    )
                )

        references = re.findall(
            r"!\[([^\]]*)\]\(([^)\s]+\.jpeg)\)", self.rendered
        )
        self.assertEqual(len(references), 52)
        self.assertEqual(len({target for _, target in references}), 52)
        self.assertEqual(
            self.sequence_sha256([f"{alt}\t{target}" for alt, target in references]),
            EXPECTED_ALL_REFERENCES_SHA256,
        )
        added_names = {
            Path(row["asset_relative_path"]).name for row in self.n04_added
        }
        actual_mapped = [
            target for _, target in references if target not in added_names
        ]
        disposed_ordinals = set(EXPECTED_DISPOSITION_ORDINALS)
        expected_retained = [
            name
            for row, name in zip(self.n04_images, mapped_names)
            if row["ordinal"] not in disposed_ordinals
        ]
        self.assertEqual(actual_mapped, expected_retained)
        self.assertEqual(len(actual_mapped), 41)
        self.assertEqual(
            self.sequence_sha256(actual_mapped),
            EXPECTED_RETAINED_REFERENCES_SHA256,
        )
        for row in disposition_rows:
            self.assertNotIn(Path(row["asset_relative_path"]).name, self.rendered)

        # Legacy mapped bytes remain available and verified even when a complete
        # source composite supersedes their Markdown references.
        for row in self.n04_images:
            basename = Path(row["asset_relative_path"]).name
            output = build.OUTPUT_ROOT / Path(self.path).parent / basename
            self.assertTrue(output.is_file(), basename)
            self.assertEqual(build.sha256(output.read_bytes()), row["asset_sha256"])

    def test_eleven_source_added_assets_and_placement_are_exact(self) -> None:
        self.assertEqual(
            [row["id"] for row in self.n04_added],
            [f"G5-A-{number:04d}" for number in range(50, 61)],
        )
        self.assertEqual(self.rows_sha256(self.n04_added), EXPECTED_ADDED_ROWS_SHA256)
        for row in self.n04_added:
            basename, digest, dimensions, byte_count, pdf_page = EXPECTED_ADDED[
                row["id"]
            ]
            with self.subTest(asset=row["id"]):
                self.assertEqual(set(row), build.ADDED_ASSET_FIELDS)
                self.assertEqual(row["document_id"], "N04")
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
            Path(row["asset_relative_path"]).name for row in self.n04_added
        ]
        added_set = set(added_names)
        positions = [
            index + 1
            for index, (_, target) in enumerate(references)
            if target in added_set
        ]
        self.assertEqual(positions, [10, 12, 19, 28, 33, 37, 38, 46, 48, 49, 51])
        self.assertEqual(
            [target for _, target in references if target in added_set],
            [
                EXPECTED_ADDED["G5-A-0053"][0],
                EXPECTED_ADDED["G5-A-0050"][0],
                EXPECTED_ADDED["G5-A-0054"][0],
                EXPECTED_ADDED["G5-A-0055"][0],
                EXPECTED_ADDED["G5-A-0056"][0],
                EXPECTED_ADDED["G5-A-0052"][0],
                EXPECTED_ADDED["G5-A-0057"][0],
                EXPECTED_ADDED["G5-A-0058"][0],
                EXPECTED_ADDED["G5-A-0059"][0],
                EXPECTED_ADDED["G5-A-0051"][0],
                EXPECTED_ADDED["G5-A-0060"][0],
            ],
        )

    def test_high_risk_technical_forms_are_exact(self) -> None:
        required = (
            "# >= k",
            "Fold[k #1 + #2 &, 0, list]",
            "1 <= DigitCount[n, 2, 1] <= Log[2, n]",
            "Root[#^3 - # - 1 &, 1]",
            "t = 10^Range[6]",
            "If[b == 6",
            "Last[#1]],\n    2 Last[#1]}",
            "f[n] == m",
            "f[0, y___Integer]",
            "c[g_, h___]",
            "2^(# + 1) - # - 2",
            "2^Ceiling[Log[2, # + 2]] - # - 2",
            "2^31 - 1",
            "2^13466917 - 1",
            "DivisorSigma[1, n] - 2 n",
            "#[[2]]^2/#[[3]]",
            "#[[1]] != #[[2]]",
            "$2^t$ digits",
            "k^((k^s - 1) (1 + s - s k)/(k - 1))",
            "one part in $10^{30}$",
            "Prime[n]^-s",
            "LogIntegral[n] - Sum",
            "PrimePi[n] - LogIntegral[n]",
            "Apply[LCM, Range[n]]] - n",
            "2 Cos[RiemannSiegelTheta[t]]",
            "Zeta[z + (3/4 + I t)]",
            "Re[r[i]] == 1/2",
            "With[{r = FromContinuedFraction[ContinuedFraction[x, n]]}, -Log[Denominator[r], Abs[x - r]]]",
            "CCAEvolveList[f_, init_List, t_Integer]",
            "((∂_t u)^2 + (∂_x u)^2)/2",
            "Sqrt[1/8 a c (b - d)]",
            r"2\,3^{1/4}\,\mathrm{EllipticK}[1/2]",
            r"$u[t, x] \partial_x u[t, x]$.)",
            "s^2 + 4 r == 4^t n",
            "{a_, b_} -> If[a > b, {a - b, b}, {a, b - a}]",
            "$n 2^n$",
            "*n n*!",
            "Nest[Sqrt[# + 2] &, 0, n] == 2 Cos[Pi/2^(n + 1)]",
            "Fold[#1^2 - #2 &, x, b] == x",
            "Ceiling[NestList[(2 - Mod[-#, 1])^2 &, x^2, n - 1] - 2]",
            "n - (# - 2) 2^(# - 1) - 2",
            "(# - 1) 2^# + 1 < n",
            "IntegerDigits[Mod[2^n Floor[2^53 x], 2^53], 2, 53]",
            "Flatten[IntegerDigits[IntegerDigits[Mod[2^n Floor[10^12 x], 10^12], 10, 12], 2, 4]]",
            r"$Sin[\pi u]^2$ makes the mapping become just  $u \rightarrow FractionalPart[2u]$",
            "a'[t] = f[a[t], b[t], …]",
            r"$$\partial_t u[t, x] = -\partial_{xx} u[t, x]$$",
            r"$$\partial_{tt} u[t, x] = \partial_{xx} u[t, x] + f[u[t, x]]$$",
            r"$$\partial_{tt} u[t, x] == \partial_{xx} u[t, x] + f[u[t, x]]$$",
            r"$$\partial_{tt} u[t, x] = \partial_{xx} u[t, x] + (1 - u[t, x]^n) (1 + a u[t, x])$$",
        )
        for specimen in required:
            with self.subTest(specimen=specimen[:80]):
                self.assertEqual(self.rendered.count(specimen), 1)

        source_fidelity_pins = (
            "requiring for example IntegerQ[DivisorSigma[1, n]/n]",
            "*m* itself contains rational numbers",
            "a combination of neighboring cell value",
            "using the `NDSolve` function built into *Mathematica*",
            "For rational functions `f[x]`, `Integrate[f[x], {x, 0, 1}]` must always be a linear function of `Log` and `ArcTan` applied to algebraic numbers (`f[x] = 1/(1 + x^2)` for example yields $\\pi/4$).",
            "the sequence `FractionalPart[a^n x]` associated with the map",
        )
        for specimen in source_fidelity_pins:
            with self.subTest(source_fidelity=specimen):
                self.assertEqual(self.rendered.count(specimen), 1)

        standalone_expressions = (
            "Floor[h] + Fold[Flatten[#1 /. #2] &, {0}, rules]",
            "n -> If[Mod[n, 3] == 0, 2 n/3, Round[4 n/3]]",
            "Flatten[Table[Table[n, {IntegerExponent[n, 2] + 1}], {n, m}]]",
            "Nest[Replace[#, {x___} -> {x, 1, x, 0}] &, {}, k]",
            "39448887705043893375102470161238803295318090278129552",
            "Ceiling[1 + ProductLog[(n - 1) Log[2]/2]/Log[2]]",
        )
        for expression in standalone_expressions:
            with self.subTest(standalone=expression[:80]):
                self.assertEqual(self.rendered.count(f"\n\n`{expression}`\n\n"), 1)
                self.assertNotIn(f"`{expression}`.", self.rendered)

        shallit = self.rendered[
            self.rendered.index("{0, k - 1, k + 2") : self.rendered.index(
                "```", self.rendered.index("{0, k - 1, k + 2")
            )
        ]
        self.assertIn(
            "{9, 10}, {7, 8}, {9, 10}, {3, 4}}[[#]]] &, 1, n]]]", shallit
        )
        self.assertNotIn("n]]]]", shallit)

        forbidden = (
            "f[n] <= m",
            "vield",
            "xeventually",
            "163is",
            "swill",
            "wrong-with",
            "machineprecision",
            "lowlevel",
            "repeats-but",
            "digit-bydigit",
            "Bessell",
            "2or at most",
            "Integer Digits",
            "<sup>",
            "</sup>",
            r"\blacksquare",
            r"\_",
            r"\#",
            "socalled",
            "PrimePi[n] LogIntegral[n]",
            "Integrate  $[f[x],",
            "FractionalPart[anx]",
        )
        for remnant in forbidden:
            with self.subTest(remnant=remnant):
                self.assertNotIn(remnant, self.rendered)
        self.assertNotRegex(self.rendered, r"(?m)^924$")

    def test_closure_inventory_and_n05_handoff_are_exact(self) -> None:
        references = re.findall(
            r"!\[([^\]]*)\]\(([^)\s]+\.jpeg)\)", self.rendered
        )
        dispositions = [
            row for row in self.n04_images if "reference_disposition" in row
        ]
        repaired = [
            row for row in self.n04_images if "repaired_asset_relative_path" in row
        ]
        self.assertEqual(repaired, [])
        self.assertEqual(
            (
                len(self.n04_corrections),
                len(self.n04_images),
                len(dispositions),
                len(self.n04_added),
                len(references),
            ),
            (74, 71, 30, 11, 52),
        )
        self.assertEqual(
            (
                self.document["raw_end_line"] + 1,
                self.document["raw_end_byte_exclusive"],
                self.document["authoritative_pdf_end_page"] + 1,
            ),
            (
                self.n05_document["raw_start_line"],
                self.n05_document["raw_start_byte"],
                self.n05_document["authoritative_pdf_start_page"],
            ),
        )
        self.assertEqual(
            (
                self.n05_document["raw_start_line"],
                self.n05_document["raw_start_byte"],
                self.n05_document["authoritative_pdf_start_page"],
            ),
            (13460, 1908092, 943),
        )
        self.assertEqual(self.n05_images[0]["ordinal"], 989)
        self.assertEqual(
            [row["ordinal"] for row in self.n05_images], list(range(989, 1048))
        )
        self.assertEqual(
            Path(self.n05_images[0]["asset_relative_path"]).name,
            "_page_943_Picture_11.jpeg",
        )
        self.assertEqual(
            int(self.n04_corrections[-1]["id"].rsplit("-", 1)[1]) + 1, 1048
        )
        self.assertEqual(
            int(self.n04_added[-1]["id"].rsplit("-", 1)[1]) + 1, 61
        )
        self.assertTrue(self.rendered.endswith("calcium”).\n"))


if __name__ == "__main__":
    unittest.main()
