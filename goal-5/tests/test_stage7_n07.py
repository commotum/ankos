from __future__ import annotations

import hashlib
import json
import os
import re
import sys
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
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402
import validate  # noqa: E402


EXPECTED_TARGET_BYTES = 115_684
EXPECTED_TARGET_LINES = 692
EXPECTED_TARGET_SHA256 = (
    "fd8696100529789964578841267bbd841411691d05248840ede6e0b4b7bd69f3"
)
EXPECTED_CORRECTION_ROWS_SHA256 = (
    "9f2268a0836440ec47763f4084f796583801fae8f4d0a51f526d660037778329"
)
EXPECTED_CORRECTION_SEQUENCE_SHA256 = (
    "ccbed8f6141b7a58696bae7c60bd6aef5e426e3c10225b62ca1b40a29e4b8c81"
)
EXPECTED_IMAGE_ROWS_SHA256 = (
    "87d6f62179556612e854563466e3200541ed96f8ce80f1d07a5400aedcc64b41"
)
EXPECTED_CHANGED_IMAGE_ROWS_SHA256 = (
    "d94dca287537a8dbaf5f4d3d237eab00cdb216b5d1fbecd449b44da6992a90d0"
)
EXPECTED_ADDED_ROWS_SHA256 = (
    "2fa71cde066fbcc75a1563963afeb5717f14653e9e8313ce1c5034e1b8329d55"
)

EXPECTED_HEADINGS = [
    "## Mechanisms in Programs and Nature",
    "### Universality of Behavior",
    "### Three Mechanisms for Randomness",
    "### Randomness from the Environment",
    "### Chaos Theory and Randomness from Initial Conditions",
    "### The Intrinsic Generation of Randomness",
    "### The Phenomenon of Continuity",
    "### Origins of Discreteness",
    "### The Problem of Satisfying Constraints",
    "### Origins of Simple Behavior",
]

EXPECTED_COMPOSITE_GROUPS = {
    "G5-A-0080": (1112, 1113, 1114, 1115, 1116),
    "G5-A-0081": (1117, 1118, 1119, 1120, 1121),
    "G5-A-0082": (1122, 1123, 1124, 1125, 1126),
    "G5-A-0083": (1133, 1134, 1135, 1136, 1137),
    "G5-A-0084": (1138, 1139, 1140),
    "G5-A-0085": (1141, 1142, 1143, 1144),
    "G5-A-0086": (1145, 1146, 1147, 1148, 1149),
    "G5-A-0087": (1150, 1151, 1152, 1153, 1154),
    "G5-A-0088": (1155, 1156, 1157, 1158, 1159),
    "G5-A-0089": (1160, 1161, 1162, 1163),
    "G5-A-0090": (1166, 1167),
    "G5-A-0091": (1168, 1169, 1170, 1171),
    "G5-A-0092": (1172, 1173, 1174, 1175),
    "G5-A-0093": (1195, 1196, 1197),
}

REQUIRED_LITERALS = [
    "Beginning in the 1950s, however, it became increasingly common",
    "`Abs[Fourier[data]]^2`",
    "`Abs[Fourier[list]]^2`",
    "n[i + 2] == Mod[65539^2 n[i], 2^31] ==",
    "LFSRStep[list_] :=",
    "LFSRStep[taps_List, list_] :=",
    "PolynomialMod[x^t, {1 + x + x^n, 2}]",
    "`f[n_] := f[n - 1] + f[n - 2]`",
    "λ[x_] := Exp[-10 (x - 1)^2] + Exp[-10 (x - 3)^2]",
    "With[{σ = 1}, (d/(2 π σ t))^(d/2) Exp[-d r^2/(2 σ t)]]",
    "AEvolve[t_] := Nest[AStep, {{0, 0}}, t]",
    "AStep[a_] := ReplacePart[a, 1, (#[[Random[",
    "■ **Isotropy.** Any pattern grown from a single cell",
    "{a1_, a2_, a3_, a4_, a5_, a6_, a7_}",
    "e[s_] := -1/2 Apply[Plus, s ListConvolve[",
    "m[s_] := Apply[Plus, s, {0, 1}]",
    "Abs[m[s]] == (1 - Sinh[2 β]^-4)^(1/8)",
    "Mask[list_] := Array[Mod[#1 + #2, 2] &, Dimensions[list]]",
    "$p == p^2 (3-2p)$",
    "Cost[list_] := Apply[Plus, Abs[list - RotateLeft[list]]]",
    "Move[list_] := (If[Cost[#] < Cost[list], #, list] &)[",
    "NP-complete problem",
    "self-gravitating regions",
    r"$1/18(17\sqrt{13}-24)\pi \approx 0.95$",
    "nested *Mathematica* list such as `{{{}, {{}}}, {}}`",
    "c[{m_, n_}, d_] :=",
    "SandStep[s_] := s + ListConvolve[",
    "![](_page_1005_Sandpile_Fixed_Configurations_Four_Cycle_Row.jpeg)",
    "“1/f noise”",
    "“taps”",
    "“droplets”",
    "“percolating”",
    "James Gleick’s 1987 popular book *Chaos*",
    "`SeedRandom[n]`",
    "`n -> Mod[a n, m]`",
    "FixedPoint[# - a f'[#] &, Subscript[x, 0]]",
    "$2^n$ steps",
    "$E_8$",
    "$t^{1/3}$",
    "`Binomial[2 n, n]/(n + 1)`",
    "a digit $k$ positions from the right will typically repeat",
    "period $m - 1$ for many values of $a$",
    "In the case $a = 65539$, the points lie on planes in 3D",
    "nonlinear functions of $n$ are used",
    "where $n$ is the number of cells",
    "Given a sequence $a$ of $n$ equally probable 0’s and 1’s",
    "to $n$ digits:",
    "if one takes $n$ numbers that follow Gaussian distributions",
    "a random walk with $t$ steps of length 1 starting at position 0 can be generated from",
    "A generalization to $d$ dimensions is then",
    "a lattice with $k$ directions in two dimensions",
    "root mean square displacement after $t$ steps",
    "value $3/(2+d)$; for $d > 4$",
    "perfectly isotropic in $d$ dimensions",
    r"where $\beta$ can be deduced from",
    "same for every $k$, but some complexity in shape is seen, though for large $k$",
    "wavenumber $k$ by a so-called dispersion relation",
    "For some $k$ this yields a value",
    "for some range of $k$—implying an instability",
    "`m[s_] := Apply[Plus, s, {0, 1}]`.",
]

FORBIDDEN_LITERALS = [
    "Abs[Fourier[data]]<sup>2</sup>",
    "Abs[Fourier[list]]<sup>2</sup>",
    "LFSRStep[list ]",
    "s_{-}",
    "n_{-}",
    "<math>",
    "5neighbor",
    "5neig",
    "NPcomplete",
    "selfgravitating",
    r"\pi \simeq 0.95",
    "{{{}}, {{}}}, {{}}}",
    "$f[n_] := f[n-1] + f[n-2]$",
    "2<sup>n</sup>",
    "E<sub>8</sub>",
    "t <sup>1/3</sup>",
    '"1/f noise"',
    '"taps"',
    '"droplets"',
    '"percolating"',
    "![](_page_1005_Picture_2.jpeg)",
    "![](_page_1005_Picture_3.jpeg)",
    "![](_page_1005_Picture_4.jpeg)",
    "a digit k positions from the right will typically repeat",
    "period m-1 for many values of a",
    "In the case a = 65539, the points lie on planes in 3D",
    "nonlinear functions of n are used",
    "where n is the number of cells",
    "Given a sequence a of n equally probable 0’s and 1’s",
    "if one takes n numbers that follow Gaussian distributions",
    "a random walk with t steps of length 1 starting at position 0 can be generated\n",
    "A generalization to d dimensions is then",
    "a lattice with k directions in two dimensions",
    "root mean square displacement after t steps",
    "value 3/(2+d); for d>4",
    "perfectly isotropic in d dimensions",
    "where β can be deduced from",
    "same for every k, but some complexity in shape is seen, though for large k",
    "wavenumber k by a so-called dispersion relation",
    "for some range of k—implying an instability",
    "```\nm[s_] := Apply[Plus, s, {0, 1}]\n```",
    "\n\n.\n",
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


class NotesForChapter7Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.document = next(row for row in cls.documents if row["id"] == "N07")
        cls.n06 = next(row for row in cls.documents if row["id"] == "N06")
        cls.n08 = next(row for row in cls.documents if row["id"] == "N08")
        cls.path = build.safe_relative_path(cls.document["output_path"], suffix=".md")
        cls.rendered_bytes = build.document_bytes(
            cls.raw, cls.documents, cls.corrections
        )[cls.path]
        cls.rendered = cls.rendered_bytes.decode("utf-8")
        cls.output_path = build.OUTPUT_ROOT / Path(cls.path)
        cls.rows = [row for row in cls.corrections if row["document_id"] == "N07"]
        cls.image_rows = [row for row in cls.images if row["document_id"] == "N07"]
        cls.added = [
            row for row in cls.added_assets if row["document_id"] == "N07"
        ]
        cls.references = re.findall(r"!\[[^]]*\]\(([^)\n]+)\)", cls.rendered)

    def test_exact_range_guarded_corrections_and_boundaries(self) -> None:
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
                14_848,
                15_582,
                2_090_568,
                2_206_052,
                735,
                115_484,
                "b2e1c570e36dd0d9ab5600c7f90de53733fd10ce55f53bdb7975e1bf42b513c7",
                983,
                1006,
                "967",
                "990",
            ),
        )
        segment = self.raw[2_090_568:2_206_052]
        self.assertEqual(build.sha256(segment[:256]), "6fb51ed7e49f81225291de3c248e5c113f70ca605b32642727e13f04d2494102")
        self.assertEqual(build.sha256(segment[-256:]), "125e0ebbf4a285e04df5781c930adb627b7514d361a95b5a43bd06a0a799581c")
        self.assertEqual(len(self.rows), 217)
        self.assertEqual(
            [row["id"] for row in self.rows],
            [f"G5-C-{number:04d}" for number in range(1402, 1619)],
        )
        self.assertEqual(rows_sha256(self.rows), EXPECTED_CORRECTION_ROWS_SHA256)
        self.assertEqual(
            row_hash_sequence_sha256(self.rows), EXPECTED_CORRECTION_SEQUENCE_SHA256
        )

        previous_end = self.document["raw_start_byte"]
        for row in sorted(self.rows, key=lambda value: value["raw_start_byte"]):
            with self.subTest(correction=row["id"]):
                self.assertEqual(set(row), build.CORRECTION_FIELDS | {"raw_line"})
                start = row["raw_start_byte"]
                before = row["before"].encode()
                end = start + len(before)
                local = start - self.document["raw_start_byte"]
                self.assertGreaterEqual(start, previous_end)
                self.assertLessEqual(end, self.document["raw_end_byte_exclusive"])
                self.assertEqual(self.raw[start:end], before)
                self.assertEqual(segment.count(before), row["expected_count"])
                self.assertEqual(
                    row["raw_line"],
                    self.document["raw_start_line"] + segment[:local].count(b"\n"),
                )
                pages = [
                    int(page)
                    for page in re.findall(r"pdf:(\d{4})", row["authoritative_location"])
                ]
                printed = [
                    int(page)
                    for page in re.findall(
                        r"printed:(\d{3})", row["authoritative_location"]
                    )
                ]
                self.assertTrue(pages)
                self.assertEqual(printed, [page - 16 for page in pages])
                self.assertTrue(all(983 <= page <= 1006 for page in pages))
                self.assertEqual(row["reviewer_type"], "agent")
                self.assertEqual(row["verification_status"], "SOURCE_VERIFIED")
                previous_end = end

        self.assertEqual(self.n06["raw_end_byte_exclusive"], 2_090_568)
        self.assertEqual(self.n06["raw_end_line"] + 1, 14_848)
        self.assertEqual(self.n08["raw_start_byte"], 2_206_052)
        self.assertEqual(self.n08["raw_start_line"], 15_583)
        self.assertEqual(len(self.rendered_bytes), EXPECTED_TARGET_BYTES)
        self.assertEqual(self.rendered_bytes.count(b"\n"), EXPECTED_TARGET_LINES)
        self.assertEqual(build.sha256(self.rendered_bytes), EXPECTED_TARGET_SHA256)
        self.assertEqual(self.output_path.read_bytes(), self.rendered_bytes)
        self.assertEqual(
            validate.independent_document_bytes(
                self.raw, self.documents, self.corrections
            )[self.path],
            self.rendered_bytes,
        )

    def test_markdown_structure_is_balanced_and_exact(self) -> None:
        lines = self.rendered.splitlines()
        headings = [line for line in lines if line.startswith("#")]
        labels = [line for line in lines if line.startswith("■ **")]
        fences = [line for line in lines if line.startswith("```")]
        self.assertEqual(headings, EXPECTED_HEADINGS)
        self.assertEqual((len(labels), len(fences), len(self.references)), (92, 74, 43))
        self.assertTrue(all(line == "```" for line in fences))
        self.assertEqual(len(fences) % 2, 0)
        self.assertEqual(len(set(self.references)), 43)
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

    def test_eighty_eight_image_rows_and_sixty_eight_changes(self) -> None:
        self.assertEqual(len(self.image_rows), 88)
        self.assertEqual(
            [row["ordinal"] for row in self.image_rows], list(range(1112, 1200))
        )
        self.assertEqual(rows_sha256(self.image_rows), EXPECTED_IMAGE_ROWS_SHA256)
        changed = [
            row
            for row in self.image_rows
            if "reference_disposition" in row
            or "repaired_asset_relative_path" in row
        ]
        self.assertEqual(len(changed), 68)
        self.assertEqual(rows_sha256(changed), EXPECTED_CHANGED_IMAGE_ROWS_SHA256)
        redundant = [row for row in changed if "reference_disposition" in row]
        repaired = [row for row in changed if "repaired_asset_relative_path" in row]
        self.assertEqual((len(redundant), len(repaired)), (59, 9))
        self.assertEqual(
            [row["ordinal"] for row in repaired],
            [1127, 1165, 1176, 1179, 1180, 1183, 1188, 1190, 1194],
        )

        groups: dict[str, list[int]] = defaultdict(list)
        for row in redundant:
            self.assertEqual(
                row["reference_disposition"], build.REDUNDANT_REFERENCE_DISPOSITION
            )
            self.assertEqual(
                row["reference_verification_status"], "SOURCE_VERIFIED"
            )
            matches = re.findall(r"G5-A-\d{4}", row["reference_reason"])
            self.assertEqual(len(matches), 1)
            groups[matches[0]].append(row["ordinal"])
            self.assertNotIn(Path(row["asset_relative_path"]).name, self.references)
        self.assertEqual(
            {key: tuple(values) for key, values in groups.items()},
            EXPECTED_COMPOSITE_GROUPS,
        )

        retained = [
            Path(row["asset_relative_path"]).name
            for row in self.image_rows
            if "reference_disposition" not in row
        ]
        added = {Path(row["asset_relative_path"]).name for row in self.added}
        self.assertEqual((len(retained), len(added)), (29, 14))
        self.assertEqual(set(self.references), set(retained) | added)
        self.assertEqual(Counter(self.references), Counter(set(self.references)))
        for row in self.image_rows:
            basename = Path(row["asset_relative_path"]).name
            output = build.OUTPUT_ROOT / Path(self.path).parent / basename
            digest = row.get("repaired_asset_sha256", row["asset_sha256"])
            with self.subTest(mapped_output=basename):
                self.assertTrue(output.is_file())
                self.assertEqual(build.sha256(output.read_bytes()), digest)

    def test_fourteen_additions_nine_repairs_and_twenty_three_assets(self) -> None:
        self.assertEqual(
            [row["id"] for row in self.added],
            [f"G5-A-{number:04d}" for number in range(80, 94)],
        )
        self.assertEqual(rows_sha256(self.added), EXPECTED_ADDED_ROWS_SHA256)
        repaired = [
            row for row in self.image_rows if "repaired_asset_relative_path" in row
        ]
        expected_paths = {
            row["asset_relative_path"] for row in self.added
        } | {row["repaired_asset_relative_path"] for row in repaired}
        actual_paths = {
            path.relative_to(REPO_ROOT).as_posix()
            for path in (GOAL_DIR / "assets/N07").glob("*.jpeg")
        }
        self.assertEqual(actual_paths, expected_paths)
        self.assertEqual(len(actual_paths), 23)
        for row in self.added:
            source = REPO_ROOT / row["asset_relative_path"]
            payload = source.read_bytes()
            with self.subTest(added=row["id"]):
                self.assertEqual(build.sha256(payload), row["asset_sha256"])
                self.assertEqual(
                    build.jpeg_dimensions(payload), (row["width_px"], row["height_px"])
                )
        for row in repaired:
            source = REPO_ROOT / row["repaired_asset_relative_path"]
            payload = source.read_bytes()
            with self.subTest(repaired=row["ordinal"]):
                self.assertEqual(build.sha256(payload), row["repaired_asset_sha256"])
                self.assertEqual(
                    build.jpeg_dimensions(payload),
                    (row["repaired_width_px"], row["repaired_height_px"]),
                )

    def test_fourteen_visual_guards_are_final_not_provisional(self) -> None:
        guards = [
            row
            for row in self.rows
            if 1567 <= int(row["id"].removeprefix("G5-C-")) <= 1580
        ]
        self.assertEqual(
            [row["id"] for row in guards],
            [f"G5-C-{number:04d}" for number in range(1567, 1581)],
        )
        for row in guards:
            partials = re.findall(r"!\[\]\(([^)\n]+)\)", row["before"])
            final = re.fullmatch(r"!\[\]\(([^)\n]+)\)", row["after"])
            with self.subTest(guard=row["id"]):
                self.assertIsNotNone(final)
                self.assertGreaterEqual(len(partials), 2)
                self.assertIn("recorded by G5-A-", row["reason"])
                self.assertNotIn("proposed", row["reason"].lower())
                self.assertEqual(self.rendered.count(row["after"]), 1)
                for partial in partials:
                    self.assertNotIn(f"![]({partial})", self.rendered)

    def test_high_risk_literals_and_provisional_tokens(self) -> None:
        for literal in REQUIRED_LITERALS:
            with self.subTest(required=literal):
                self.assertIn(literal, self.rendered)
        for literal in FORBIDDEN_LITERALS:
            with self.subTest(forbidden=literal):
                self.assertNotIn(literal, self.rendered)
        n07_manifest = "\n".join(canonical_bytes(row).decode() for row in self.rows)
        n07_manifest += "\n" + "\n".join(
            canonical_bytes(row).decode() for row in self.image_rows + self.added
        )
        self.assertNotRegex(n07_manifest, r"N07-(?:PROP|TFP|VP|A-PROV|C-PROV)")
        self.assertNotIn("FIRST_PASS", n07_manifest)
        self.assertNotIn("proposed canonical", n07_manifest)


if __name__ == "__main__":
    unittest.main()
