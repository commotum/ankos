from __future__ import annotations

import copy
import json
import re
import sys
import unittest
from pathlib import Path
from typing import TypeVar


GOAL_DIR = Path(__file__).resolve().parents[1]
if not (GOAL_DIR / "build.py").is_file():
    # Keep this /tmp review artifact executable before installation.
    GOAL_DIR = Path("/home/jake/Developer/ankos/goal-5")
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402
import validate  # noqa: E402


# Final integration pins from the installed packet and rebuilt CH11.
EXPECTED_CH11_CORRECTION_COUNT: int | None = 41
EXPECTED_CH11_RENDERED_BYTES: int | None = 103921
EXPECTED_CH11_RENDERED_LINES: int | None = 892
EXPECTED_CH11_RENDERED_SHA256: str | None = (
    "3dfc34e4a99364e3fa48b555ed7399a8a8c8a1acd3b977763554c89b836cfd63"
)

# ordinal: (basename, repaired hash, dimensions, source page, legacy hash)
EXPECTED_REPAIRED: dict[
    int, tuple[str, str | None, tuple[int, int] | None, str, str]
] = {
    678: (
        "_page_663_Picture_3.jpeg",
        "7332d36ff9db7abbe06ddee443cdfa7145ceb553194e5daecdbd8875e08803f0",
        (1146, 816),
        "pdf:0664",
        "46ad0f0a009327f14bd38378b580ce8a4f7ce2ea2b133b212977a872e2ab88b5",
    ),
    685: (
        "_page_668_Figure_2.jpeg",
        "7b208695f232f0b8394b8c0c6166cfc4fcf5af78d6abccdfbe99a662a27b6f93",
        (1740, 1830),
        "pdf:0669",
        "cfc68a5d0c5f74408260e31cdab43af6623b2195db06ac2722b5e5e83ce48e5e",
    ),
    687: (
        "_page_672_Picture_1.jpeg",
        "c9300f944d5146fad2d5b86909857001ff9632d58d06c4a9e8e90118c1c16fd7",
        (487, 472),
        "pdf:0673",
        "7eaddca4f7e868881728f3ca94f5c6818daaaca2f8ebc2b34d7f5886cdc59813",
    ),
    692: (
        "_page_673_Figure_3.jpeg",
        "3031ee5733642c968d4cad1194852670741c8efe3a5401e95b9481f3afde4c54",
        (1680, 225),
        "pdf:0674",
        "726a894fe2b74b87ccfa442d1abdec0a62a517c9c2bc0b0b323ea6dc04b0b162",
    ),
    693: (
        "_page_674_Picture_2.jpeg",
        "635708348afe87aad418e8baee43a36dbd4dad7bc9cb90287294621f7dc5f07d",
        (1665, 1880),
        "pdf:0675",
        "69b6bfc37b99ed6d2ed75728cadb67b37b4ddc0a0d3fb67bdc2f6c26ad0c811d",
    ),
    707: (
        "_page_683_Figure_1.jpeg",
        "d6be63efd859968863f811ecf438c02c1ef9899059a8113c1eecd76c2789e9cd",
        (1660, 975),
        "pdf:0684",
        "6ac5e1683f487efe9d2988f1c08a6f3b443c4d3fd30956d528e626bf7bacbcb1",
    ),
    711: (
        "_page_685_Figure_2.jpeg",
        "db82a1412b4083ab3881190e798ae9f40f934edf5c123242d71f3c4155367f9a",
        (1760, 1970),
        "pdf:0686",
        "ac3487347d237caa7add8f1c5988d20a6744dce392b7a49d2d312d9edbc207b6",
    ),
    712: (
        "_page_686_Picture_3.jpeg",
        "02b138de740a795f685cd70e25d8a99d3c21e3b1a45ff557afba112646c0107f",
        (1330, 1070),
        "pdf:0687",
        "702dbbb8c4c58e9ff4b146f85ed93a05b1d642f288316682902071b3c1c2f227",
    ),
    725: (
        "_page_699_Picture_1.jpeg",
        "fe48644a17dcc6c388411517822da3129d080a1397cd42785100f539a14c9502",
        (1215, 1352),
        "pdf:0700",
        "59cc77be394d7bd34b00c431ae922b2ebb019c2a4fe2ebaf028bc5fe8713d0e7",
    ),
    727: (
        "_page_701_Picture_1.jpeg",
        "c08b60c7888eb6ea9ccf82e25ee50ad003909965402d1f2596107d003590000c",
        (1202, 1335),
        "pdf:0702",
        "c2a4f628643de8b81f0a55de52e2ff18eb06b7871ee99c4e8dec72f2a4d864ad",
    ),
    729: (
        "_page_707_Figure_1.jpeg",
        "0d4d66ff1de567571c444bd22eeaeb7f97bb7797bd618828cd13ed9796b231e2",
        (1130, 1104),
        "pdf:0708",
        "974e12d28e8acc6fb4af26f7b1dd09eae1f30d802666a61f41abed8ec2d42e19",
    ),
    747: (
        "_page_717_Figure_1.jpeg",
        "fcef153b9c49813d03d3789858625332f5dbdef14facd9b213976d8a2b2aceae",
        (1765, 2210),
        "pdf:0718",
        "626cc565266d0ecbcfac47cb3e88ad7fbd4dc426dc2a40ffa371f9cea93aa752",
    ),
    756: (
        "_page_723_Figure_6.jpeg",
        "1d660229e6daca3bec276b36a68bce31fdbdb0e3f2bbdb8d708d34650f0918d5",
        (1585, 1340),
        "pdf:0724",
        "17d82f5f6cab7e8676ac69824320c364a8cbe58426b5af38073b3c5592e11f13",
    ),
    762: (
        "_page_727_Figure_1.jpeg",
        "c82c8d3499c0bec245a8ee70e33766ce9a210bc5afbb4b8077a346f905735907",
        (1021, 1336),
        "pdf:0728",
        "e8c4436894b724030d64fb7bf3c4a4382daa08a8e5c55a2242a83c4128bf96d3",
    ),
}

# (basename, hash, dimensions, source page)
EXPECTED_ADDED_RULE: tuple[str, str | None, tuple[int, int] | None, str] = (
    "_page_722_Turing_Rule.jpeg",
    "d0ca97ecfe190b85dbb5273f8b7feece40b0ed208e504e33e714b32c0bc3a033",
    (1290, 150),
    "pdf:0723",
)


T = TypeVar("T")


class ChapterElevenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.range_data = json.loads(build.RANGES_PATH.read_text(encoding="utf-8"))
        cls.document = next(row for row in cls.documents if row["id"] == "CH11")
        cls.path = build.safe_relative_path(cls.document["output_path"], suffix=".md")
        cls.raw_text = cls.raw[
            cls.document["raw_start_byte"] : cls.document["raw_end_byte_exclusive"]
        ].decode("utf-8")
        cls.rendered_bytes = build.document_bytes(
            cls.raw, cls.documents, cls.corrections
        )[cls.path]
        cls.rendered = cls.rendered_bytes.decode("utf-8")

    def pinned(self, value: T | None, name: str) -> T:
        self.assertIsNotNone(value, f"patch integration-dependent pin: {name}")
        return value  # type: ignore[return-value]

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

    def table_rows(self) -> list[list[str]]:
        return [
            [cell.strip() for cell in line.strip("|").split("|")]
            for line in self.rendered.splitlines()
            if line.startswith("|")
        ]

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
                7692,
                8607,
                1103253,
                1208768,
                916,
                105515,
                "1ae6fc36cabfccc28bf04f383613c239de178ff371798a6eb954c722bc67a599",
                653,
                730,
                "637",
                "714",
            ),
        )
        raw_segment = self.raw[
            self.document["raw_start_byte"] : self.document["raw_end_byte_exclusive"]
        ]
        self.assertEqual(build.sha256(raw_segment), self.document["raw_segment_sha256"])

        relevant = [row for row in self.corrections if row["document_id"] == "CH11"]
        self.assertEqual(len(self.corrections), 707)
        expected_count = self.pinned(
            EXPECTED_CH11_CORRECTION_COUNT, "EXPECTED_CH11_CORRECTION_COUNT"
        )
        self.assertEqual(len(relevant), expected_count)
        self.assertEqual(
            [row["id"] for row in relevant],
            [f"G5-C-{number:04d}" for number in range(667, 667 + expected_count)],
        )
        self.assertTrue(all(row["expected_count"] == 1 for row in relevant))
        self.assertTrue(
            all(row["verification_status"] == "SOURCE_VERIFIED" for row in relevant)
        )
        self.assertTrue(all(row["reviewer_type"] == "agent" for row in relevant))
        for row in relevant:
            with self.subTest(correction=row["id"]):
                match = re.match(r"pdf:(\d{4})", row["authoritative_location"])
                self.assertIsNotNone(match)
                self.assertTrue(653 <= int(match.group(1)) <= 730)
                start = row["raw_start_byte"]
                end = start + len(row["before"].encode("utf-8"))
                self.assertTrue(1103253 <= start < end <= 1208768)
                self.assertEqual(self.raw[start:end], row["before"].encode("utf-8"))

        self.assertEqual(
            len(self.rendered_bytes),
            self.pinned(EXPECTED_CH11_RENDERED_BYTES, "EXPECTED_CH11_RENDERED_BYTES"),
        )
        self.assertEqual(
            len(self.rendered.splitlines()),
            self.pinned(EXPECTED_CH11_RENDERED_LINES, "EXPECTED_CH11_RENDERED_LINES"),
        )
        self.assertEqual(
            build.sha256(self.rendered_bytes),
            self.pinned(EXPECTED_CH11_RENDERED_SHA256, "EXPECTED_CH11_RENDERED_SHA256"),
        )
        self.assertEqual(
            validate.independent_document_bytes(
                self.raw, self.documents, self.corrections
            )[self.path],
            self.rendered_bytes,
        )

    def test_authoritative_source_legacy_and_guards_are_pinned(self) -> None:
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

        arithmetic = next(
            row
            for row in self.corrections
            if row["document_id"] == "CH11"
            and "$i + 5$, $2^a$, $3^b$" in row["after"]
        )
        mutations = (
            ("raw_start_byte", arithmetic["raw_start_byte"] + 1),
            ("expected_count", 2),
            ("verification_status", "PROPOSED"),
            ("authoritative_location", "pdf:0652"),
        )
        for field, value in mutations:
            changed = copy.deepcopy(self.corrections)
            next(row for row in changed if row["id"] == arithmetic["id"])[field] = value
            with self.subTest(mutation=field), self.assertRaises(build.BuildError):
                build.validate_corrections(changed, self.raw, self.documents)

    def test_opener_heading_hierarchy_and_source_literals_are_exact(self) -> None:
        self.assertTrue(
            self.rendered.startswith(
                "![](_page_652_Picture_0.jpeg)\n\n"
                "## The Notion of Computation\n\n"
                "### Computation as a Framework\n\n"
            )
        )
        headings = (
            "Computation as a Framework",
            "Computations in Cellular Automata",
            "The Phenomenon of Universality",
            "A Universal Cellular Automaton",
            "Emulating Other Systems with Cellular Automata",
            "Emulating Cellular Automata with Other Systems",
            "Implications of Universality",
            "The Rule 110 Cellular Automaton",
            "The Significance of Universality in Rule 110",
            "Class 4 Behavior and Universality",
            "The Threshold of Universality in Cellular Automata",
            "Universality in Turing Machines and Other Systems",
        )
        self.assertEqual(self.rendered.count("\n### "), len(headings))
        self.assert_order(*(f"### {heading}" for heading in headings))
        self.assertNotIn("####", self.rendered)
        self.assertNotIn("### **", self.rendered)
        self.assertNotRegex(self.rendered, r"(?m)^# 11$")

        expected = {
            "elementary rule 132, as shown on the left": 1,
            r"But by using $\boxminus$ to stand for a cell with any possible color": 1,
            "corresponding quite directly to cellular automata": 1,
            "Gödel’s Theorem": 1,
            "rule 110—a cellular automaton": 1,
            r"$i + 5$, $2^a$, $3^b$": 1,
            r"computes $Mod[n, 30]$": 1,
            "taking the first 100,000 steps, and keeping only those": 1,
            "So this means that after going through": 1,
        }
        for text, count in expected.items():
            with self.subTest(source_text=text):
                self.assertEqual(self.rendered.count(text), count)
        self.assertNotIn(r"$i + 5 \cdot 2^a \cdot 3^b$", self.rendered)

    def test_high_risk_formulas_table_and_combinator_are_exact(self) -> None:
        expected_formulas = {
            r"If the values of the cells in each block are labelled $p$, $q$ and "
            r"$r$, then rule 110 can be written as $Mod[(1 + p) q r + q + r, 2]$ "
            r"or $\neg (p \land q \land r) \land (q \lor r)$.": 1,
            r"\{6, 5, -4, 3\}[[Mod[n, 4] + 1]]/2": 1,
            "*Mathematica* */.* order.": 1,
        }
        for text, count in expected_formulas.items():
            with self.subTest(formula=text):
                self.assertEqual(self.rendered.count(text), count)

        expected_table = [
            [
                "$2 n + 1$",
                "$(n - 1)/3$",
                "$3 (n - 1)$",
                "$(n + 1)/2$",
                "$(n - 4)/3$",
                "$2 n + 1$",
                "$n + 1$",
                "$3 (n - 1)$",
                "$n + 1$",
                "$n + 1$",
            ],
            ["---"] * 10,
            [f"${number}$" for number in range(10)],
            [
                "$2 n + 1$",
                "$n + 1$",
                "$3 (n - 1)$",
                "$(n + 1)/2$",
                "$n + 1$",
                "$2 n + 1$",
                "$(n - 1)/3$",
                "$3 (n - 1)$",
                "$n + 1$",
                "$(n - 4)/3$",
            ],
            [f"${number}$" for number in range(10, 20)],
            [
                "$2 n + 1$",
                "$n + 1$",
                "$3 (n - 1)$",
                "$(n + 1)/2$",
                "$n + 1$",
                "$2 n + 1$",
                "$n + 1$",
                "$3 (n - 1)$",
                "$n + 1$",
                "$n + 1$",
            ],
            [f"${number}$" for number in range(20, 30)],
        ]
        self.assertEqual(self.table_rows(), expected_table)

        display_expressions = re.findall(r"(?m)^\$\$(.+)\$\$$", self.rendered)
        self.assertEqual(len(display_expressions), 1)
        combinator = display_expressions[0]
        self.assertEqual(len(combinator.encode("utf-8")), 886)
        self.assertEqual(
            build.sha256(combinator.encode("utf-8")),
            "277f0c69734c2de7780b9ac792e2af4a5cca34d30a3263c68ab4f3b04d11f792",
        )
        self.assertEqual(combinator.count("["), 295)
        self.assertEqual(combinator.count("]"), 295)
        expression = f"$${combinator}$$"
        caption = (
            "A combinator expression that corresponds to the operation of doing one "
            "step of rule 110 evolution."
        )
        self.assertLess(self.rendered.index(expression), self.rendered.index(caption))

    def test_repaired_captions_and_image_order_are_exact(self) -> None:
        substitution_caption = (
            "Examples of cellular automata that emulate substitution systems. The "
            "successive steps in the evolution of each substitution system are "
            "obtained at the points indicated by arrows. Note that the sequences of "
            "elements generated by the cellular automata are aligned at the right, "
            "while in the pictures of the substitution systems shown they are aligned "
            "at the left. The rules for the three cellular automata involve only "
            "nearest neighbors, and allow 12 possible colors for each cell."
        )
        self.assert_order(
            "![](_page_674_Picture_2.jpeg)",
            substitution_caption,
            "![](_page_675_Figure_1.jpeg)",
        )
        self.assert_order(
            "![](_page_685_Figure_2.jpeg)",
            "Emulating a Turing machine with a tag system that depends only on the "
            "first element at each step.",
            "![](_page_686_Picture_3.jpeg)",
        )
        self.assertIn(
            "![](_page_700_Picture_1.jpeg)\n\n"
            "Close-ups (continued).\n\n"
            "![](_page_701_Picture_1.jpeg)\n\n"
            "Close-ups (continued).\n\n"
            "additional localized structures are produced",
            self.rendered,
        )
        self.assertEqual(self.rendered.count("Close-ups (continued)."), 2)

        emulation_caption = (
            "Examples of using various specific elementary cellular automata to "
            "emulate other elementary cellular automata. In each case single cells "
            "are encoded as blocks of cells, and all distinct such encodings with "
            "blocks up to length 20 are shown."
        )
        self.assert_order(
            "![](_page_717_Figure_1.jpeg)",
            emulation_caption,
            "So given a particular elementary cellular automaton one can then ask",
        )
        self.assert_order(
            "![](_page_722_Turing_Rule.jpeg)",
            "The rule for the simplest Turing machine currently known to be universal",
            "![](_page_722_Figure_6.jpeg)",
        )

        turing_caption = (
            "Examples of Turing machines with 2 states and 4 colors that show complex "
            "behavior. The compressed pictures above are based on 50,000 steps of "
            "evolution. In all cases, all cells are initially white."
        )
        self.assert_order(
            "![](_page_723_Figure_6.jpeg)",
            turing_caption,
            "The pictures at the bottom of the facing page give examples",
        )
        self.assert_order(
            "![](_page_727_Figure_1.jpeg)",
            "*Mathematica* */.* order.",
            "that no fixed point is reached",
        )

    def test_repaired_and_added_assets_are_pinned_and_references_are_exact(
        self,
    ) -> None:
        chapter_images = [row for row in self.images if row["document_id"] == "CH11"]
        self.assertEqual(len(self.images), 1444)
        self.assertEqual(len(self.added_assets), 34)
        self.assertEqual(len(self.images) + len(self.added_assets), 1478)
        self.assertEqual(
            sum("repaired_asset_relative_path" in row for row in self.images), 64
        )
        self.assertEqual(len(chapter_images), 107)
        self.assertEqual([row["ordinal"] for row in chapter_images], list(range(657, 764)))

        repaired = [
            row for row in chapter_images if "repaired_asset_relative_path" in row
        ]
        self.assertEqual([row["ordinal"] for row in repaired], list(EXPECTED_REPAIRED))
        for row in repaired:
            name, expected_hash_value, expected_dimensions_value, page, legacy_hash = (
                EXPECTED_REPAIRED[row["ordinal"]]
            )
            expected_hash = self.pinned(
                expected_hash_value, f"EXPECTED_REPAIRED[{row['ordinal']}].hash"
            )
            expected_dimensions = self.pinned(
                expected_dimensions_value,
                f"EXPECTED_REPAIRED[{row['ordinal']}].dimensions",
            )
            with self.subTest(repaired=row["ordinal"]):
                source = build.REPO_ROOT / Path(row["repaired_asset_relative_path"])
                output = build.OUTPUT_ROOT / Path(self.path).parent / name
                payload = source.read_bytes()
                legacy = build.LEGACY_ROOT / Path(row["asset_relative_path"])
                legacy_payload = legacy.read_bytes()
                self.assertEqual(source.name, name)
                self.assertEqual(build.sha256(payload), expected_hash)
                self.assertEqual(row["repaired_asset_sha256"], expected_hash)
                self.assertEqual(build.jpeg_dimensions(payload), expected_dimensions)
                self.assertEqual(
                    (row["repaired_width_px"], row["repaired_height_px"]),
                    expected_dimensions,
                )
                self.assertTrue(row["repaired_authoritative_location"].startswith(page))
                self.assertEqual(row["asset_sha256"], legacy_hash)
                self.assertEqual(build.sha256(legacy_payload), legacy_hash)
                self.assertNotEqual(payload, legacy_payload)
                self.assertEqual(output.read_bytes(), payload)

        chapter_added = [
            row for row in self.added_assets if row["document_id"] == "CH11"
        ]
        self.assertEqual([row["id"] for row in chapter_added], ["G5-A-0034"])
        added = chapter_added[0]
        added_name, added_hash_value, added_dimensions_value, added_page = (
            EXPECTED_ADDED_RULE
        )
        added_hash = self.pinned(added_hash_value, "EXPECTED_ADDED_RULE.hash")
        added_dimensions = self.pinned(
            added_dimensions_value, "EXPECTED_ADDED_RULE.dimensions"
        )
        added_source = build.REPO_ROOT / Path(added["asset_relative_path"])
        added_output = build.OUTPUT_ROOT / Path(self.path).parent / added_name
        added_payload = added_source.read_bytes()
        self.assertEqual(added_source.name, added_name)
        self.assertEqual(build.sha256(added_payload), added_hash)
        self.assertEqual(added["asset_sha256"], added_hash)
        self.assertEqual(build.jpeg_dimensions(added_payload), added_dimensions)
        self.assertEqual((added["width_px"], added["height_px"]), added_dimensions)
        self.assertTrue(added["authoritative_location"].startswith(added_page))
        self.assertEqual(added["reviewer_type"], "agent")
        self.assertEqual(added["verification_status"], "SOURCE_VERIFIED")
        self.assertEqual(added_output.read_bytes(), added_payload)

        mapped_names = {
            row["ordinal"]: Path(row["asset_relative_path"]).name
            for row in chapter_images
        }
        expected_references = (
            [mapped_names[number] for number in range(657, 754)]
            + [added_name]
            + [mapped_names[number] for number in range(754, 764)]
        )
        references = re.findall(r"!\[\]\(([^)]+\.jpeg)\)", self.rendered)
        self.assertEqual(len(references), 108)
        self.assertEqual(len(set(references)), 108)
        self.assertEqual(references, expected_references)

        # The opener's historical storage path and ref104 are intentional no-ops.
        unchanged = {
            657: "2c8e8786086d845c76b22be879139d0a2513d81337c203b4abce733e86e33aa6",
            760: "9cca4b3d3e5aeb589032d706b40ceaa18d08c1018648ad09102c43c1593e78b7",
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
        next(row for row in changed_images if row["ordinal"] == 678)[
            "repaired_asset_sha256"
        ] = "0" * 64
        with self.assertRaises(build.BuildError):
            build.validate_images(self.raw, self.documents, changed_images)

        changed_added = copy.deepcopy(self.added_assets)
        next(row for row in changed_added if row["id"] == "G5-A-0034").pop("reason")
        with self.assertRaises(build.BuildError):
            build.validate_added_assets(self.documents, self.images, changed_added)

    def test_high_risk_residual_ocr_and_layout_detectors_are_clean(self) -> None:
        raw_only = (
            "think in purely\n\nabstract terms",
            "elementary rule 132. as shown on the left",
            "corresponding guite directly",
            "nthat it obtains",
            "successive stens correspond",
            "Gödel's Theorem",
            "rule 110-a cellular automaton",
            "Mod[(1+p) gr + g + r, 2]",
            r"\{6, 5, -4, 3\} [Mod[n, 4] + 1]]/2",
            "tag system compressed evolution (1500 steps)",
            "rulo 11",
            "STEPHEN WOLFRAM",
            "*Mathematica 1*. order.",
            "| ,   | ٨  | ٨  | ٨  | ٨        |",
        )
        for residue in raw_only:
            with self.subTest(raw_residue=residue):
                self.assertEqual(self.raw_text.count(residue), 1)
                self.assertNotIn(residue, self.rendered)

        residues = (
            "<sup>(</sup>a)  $p[x_{-}]",
            r"$p[x_{-}|[p][p][p]",
            "interprets this command\n\nby executing",
            "But from\n\nexperience with computer languages",
            "always yielding\n\nfor example purely repetitive patterns",
            "reduce the number\n\nof colors from 19 to 17",
            "emulate more than a\n\nfew of the 256 possible elementary rules",
            "taking the first 100,000 steps, and\n\nkeeping only those",
            "So this means\n\nthat after going through",
            "####",
            "\t",
            "\ufffd",
        )
        for residue in residues:
            with self.subTest(residue=residue):
                self.assertNotIn(residue, self.rendered)
        self.assertNotRegex(self.rendered, r"(?m)^\|\s*,\s*\|.*[٨•]")


if __name__ == "__main__":
    unittest.main()
