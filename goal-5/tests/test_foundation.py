from __future__ import annotations

import copy
import csv
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


GOAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402
import validate  # noqa: E402


class FoundationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.range_data = json.loads(build.RANGES_PATH.read_text(encoding="utf-8"))
        cls.raw = build.LEGACY_ROOT.joinpath("A-New-Kind-of-Science.md").read_bytes()
        cls.documents = build.validate_ranges(cls.raw, cls.range_data)
        cls.images = build.validate_images(
            cls.raw, cls.documents, build.read_jsonl(build.IMAGES_PATH)
        )

    def test_clean_compact_inputs(self) -> None:
        raw, documents, corrections, images = build.load_inputs()
        self.assertEqual(raw, self.raw)
        self.assertEqual(len(documents), 29)
        self.assertEqual(
            corrections,
            build.validate_corrections(corrections, raw, documents),
        )
        self.assertEqual(len(images), 1444)
        self.assertEqual(len(raw), 3_780_628)
        self.assertEqual(len(raw.splitlines()), 22_498)
        self.assertFalse(raw.endswith(b"\n"))
        self.assertEqual(
            build.sha256(raw),
            "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20",
        )

    def test_raw_drift_is_rejected_before_building(self) -> None:
        changed = bytearray(self.raw)
        changed[100] ^= 1
        with self.assertRaisesRegex(build.BuildError, "raw monolith hash"):
            build.validate_ranges(bytes(changed), self.range_data)

    def test_authoritative_source_and_page_partition_are_pinned(self) -> None:
        source = self.range_data["authoritative_source"]
        self.assertEqual(source["edition"], "First edition")
        self.assertEqual(source["printing"], "First printing")
        self.assertEqual(source["pdf_page_count"], 1_280)
        self.assertEqual(
            source["sha256"],
            "a3cc5dd60e12d6b563aee86ea31a15b03f9cddfd4869b8f965d3a11bbc61a0d6",
        )
        self.assertEqual(
            validate.validate_authoritative_source(self.range_data),
            build.REPO_ROOT / "A New Kind of Science/A New Kind of Science.pdf",
        )
        self.assertEqual(
            [
                (
                    document["authoritative_pdf_start_page"],
                    document["authoritative_pdf_end_page"],
                )
                for document in self.documents[:3]
            ],
            [(1, 8), (9, 16), (17, 38)],
        )
        self.assertEqual(
            (
                self.documents[-2]["authoritative_pdf_start_page"],
                self.documents[-2]["authoritative_pdf_end_page"],
                self.documents[-1]["authoritative_pdf_start_page"],
                self.documents[-1]["authoritative_pdf_end_page"],
            ),
            (1217, 1279, 1280, 1280),
        )

        invalid_hash = copy.deepcopy(self.range_data)
        invalid_hash["authoritative_source"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(build.BuildError, "source hash"):
            validate.validate_authoritative_source(invalid_hash)

        for name, mutate in {
            "source page gap": lambda data: data["documents"][1].__setitem__(
                "authoritative_pdf_start_page", 10
            ),
            "unconfirmed boundary": lambda data: data["documents"][1].__setitem__(
                "boundary_status", "PROVISIONAL"
            ),
            "incomplete source partition": lambda data: data["documents"][-1].__setitem__(
                "authoritative_pdf_end_page", 1279
            ),
        }.items():
            with self.subTest(name=name):
                data = copy.deepcopy(self.range_data)
                mutate(data)
                with self.assertRaises(build.BuildError):
                    build.validate_ranges(self.raw, data)

    def test_range_and_output_mutations_are_rejected(self) -> None:
        mutations = {
            "byte gap": lambda data: data["documents"][1].__setitem__(
                "raw_start_byte", data["documents"][1]["raw_start_byte"] + 1
            ),
            "byte overlap": lambda data: data["documents"][1].__setitem__(
                "raw_start_byte", data["documents"][1]["raw_start_byte"] - 1
            ),
            "duplicate order": lambda data: data["documents"][1].__setitem__("order", 0),
            "duplicate id": lambda data: data["documents"][1].__setitem__(
                "id", data["documents"][0]["id"]
            ),
            "duplicate output": lambda data: data["documents"][1].__setitem__(
                "output_path", data["documents"][0]["output_path"]
            ),
            "unsafe output": lambda data: data["documents"][1].__setitem__(
                "output_path", "../escaped.md"
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                data = copy.deepcopy(self.range_data)
                mutate(data)
                with self.assertRaises(build.BuildError):
                    build.validate_ranges(self.raw, data)

    def test_corrections_require_evidence_and_exact_preimages(self) -> None:
        raw = b"a bad token"
        document = {
            "id": "CH01",
            "raw_start_byte": 0,
            "raw_end_byte_exclusive": len(raw),
            "output_path": "CHAPTERS/01-Test.md",
            "authoritative_pdf_start_page": 1,
            "authoritative_pdf_end_page": 1,
        }
        valid = {
            "id": "C-0001",
            "document_id": "CH01",
            "raw_start_byte": 2,
            "before": "bad",
            "after": "good",
            "expected_count": 1,
            "authoritative_location": "pdf:0001",
            "reason": "OCR substitution",
            "reviewer_type": "agent",
            "verification_status": "SOURCE_VERIFIED",
        }
        checked = build.validate_corrections([valid], raw, [document])
        self.assertEqual(
            build.apply_corrections(document, raw, checked), b"a good token"
        )
        independently_rendered = validate.independent_document_bytes(
            raw, [document], checked
        )
        self.assertEqual(
            independently_rendered[build.safe_relative_path("CHAPTERS/01-Test.md")],
            b"a good token",
        )

        invalid = []
        missing = valid.copy()
        del missing["authoritative_location"]
        invalid.append(missing)
        unverified = valid.copy()
        unverified["verification_status"] = "INFERRED"
        invalid.append(unverified)
        unbound_source = valid.copy()
        unbound_source["authoritative_location"] = "p. 1"
        invalid.append(unbound_source)
        wrong_source_page = valid.copy()
        wrong_source_page["authoritative_location"] = "pdf:0002"
        invalid.append(wrong_source_page)
        duplicate = valid.copy()
        invalid.append([valid, duplicate])
        for case in invalid:
            records = case if isinstance(case, list) else [case]
            with self.subTest(case=case):
                with self.assertRaises(build.BuildError):
                    build.validate_corrections(records, raw, [document])

        for offset, count in ((0, 1), (2, 2)):
            correction = valid.copy()
            correction["raw_start_byte"] = offset
            correction["expected_count"] = count
            with self.subTest(offset=offset, count=count):
                with self.assertRaises(build.BuildError):
                    build.validate_corrections([correction], raw, [document])

        overlap = valid.copy()
        overlap["id"] = "C-0002"
        overlap["raw_start_byte"] = 3
        overlap["before"] = "ad"
        with self.assertRaisesRegex(build.BuildError, "overlap"):
            build.validate_corrections([overlap, valid], raw, [document])

    def _write_coverage(self, path: Path, rows: list[dict[str, str]]) -> None:
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=validate.COVERAGE_FIELDS)
            writer.writeheader()
            writer.writerows(rows)

    def test_coverage_is_a_complete_one_row_join(self) -> None:
        clean = validate.validate_coverage(self.documents)
        self.assertEqual(len(clean), 29)
        self.assertTrue(
            all(
                row["first_pass"] in {"NO", "YES"}
                and row["second_pass"] in {"NO", "YES"}
                and not (row["second_pass"] == "YES" and row["first_pass"] != "YES")
                for row in clean
            )
        )

        variants: list[list[dict[str, str]]] = []
        variants.append(copy.deepcopy(clean[:-1]))
        reordered = copy.deepcopy(clean)
        reordered[0], reordered[1] = reordered[1], reordered[0]
        variants.append(reordered)
        duplicate = copy.deepcopy(clean)
        duplicate[-1]["document_id"] = duplicate[0]["document_id"]
        variants.append(duplicate)
        changed_bound = copy.deepcopy(clean)
        changed_bound[0]["raw_end_line"] = "999"
        variants.append(changed_bound)
        changed_source_bound = copy.deepcopy(clean)
        changed_source_bound[0]["authoritative_end"] = "pdf:9999"
        variants.append(changed_source_bound)
        reversed_passes = copy.deepcopy(clean)
        reversed_passes[3]["second_pass"] = "YES"
        variants.append(reversed_passes)
        no_evidence = copy.deepcopy(clean)
        no_evidence[3]["first_pass"] = "YES"
        variants.append(no_evidence)

        with tempfile.TemporaryDirectory() as directory:
            for index, rows in enumerate(variants):
                with self.subTest(index=index):
                    path = Path(directory) / f"coverage-{index}.csv"
                    self._write_coverage(path, rows)
                    with self.assertRaises(build.BuildError):
                        validate.validate_coverage(self.documents, path)

    def test_image_sequence_assets_and_known_edge_cases(self) -> None:
        actual: list[tuple[str, str]] = []
        for document in self.documents:
            segment = self.raw[
                document["raw_start_byte"] : document["raw_end_byte_exclusive"]
            ].decode("utf-8")
            actual.extend(
                (document["id"], Path(target).name)
                for target in validate.IMAGE_REFERENCE.findall(segment)
            )
        expected = [
            (row["document_id"], Path(row["asset_relative_path"]).name)
            for row in self.images
        ]
        self.assertEqual(actual, expected)
        self.assertEqual(len({name for _, name in expected}), 1444)
        self.assertEqual(len({row["asset_sha256"] for row in self.images}), 1442)
        self.assertEqual(
            [row["ordinal"] for row in self.images if row["split_status"] == "OMITTED"],
            [24, 134, 135],
        )
        self.assertEqual(self.images[-1]["document_id"], "N12")
        self.assertTrue(self.images[-1]["asset_relative_path"].startswith("BACK-MATTER/Colophon/"))
        moved_openers = {
            row["ordinal"]: row["document_id"]
            for row in self.images
            if row["ordinal"] in {2, 24, 169, 345, 437, 480, 657, 764}
        }
        self.assertEqual(
            moved_openers,
            {
                2: "CH01",
                24: "CH03",
                169: "CH05",
                345: "CH07",
                437: "CH08",
                480: "CH09",
                657: "CH11",
                764: "CH12",
            },
        )

    def test_complete_legacy_tree_matches_the_frozen_snapshot(self) -> None:
        self.assertEqual(
            validate.legacy_tree_digest(),
            (
                "b9ff7b9b507790f1d519593baf2b2d2f24dd6cd49dc0fe10f0ac629278ea42f4",
                1463,
            ),
        )

    def test_image_map_mutations_are_rejected(self) -> None:
        mutations = {
            "ordinal": lambda rows: rows[0].__setitem__("ordinal", 2),
            "owner": lambda rows: rows[0].__setitem__("document_id", "CH01"),
            "hash": lambda rows: rows[0].__setitem__("asset_sha256", "0" * 64),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                rows = copy.deepcopy(self.images)
                mutate(rows)
                with self.assertRaises(build.BuildError):
                    build.validate_images(self.raw, self.documents, rows)

        wrong_source_span = copy.deepcopy(self.documents)
        wrong_source_span[1]["authoritative_pdf_end_page"] = 14
        with self.assertRaisesRegex(build.BuildError, "owner PDF range"):
            build.validate_images(self.raw, wrong_source_span, self.images)

    @staticmethod
    def _tree_manifest(root: Path) -> list[tuple[str, str]]:
        manifest = []
        for path in sorted(item for item in root.rglob("*") if item.is_file()):
            manifest.append(
                (
                    path.relative_to(root).as_posix(),
                    hashlib.sha256(path.read_bytes()).hexdigest(),
                )
            )
        return manifest

    def test_zero_build_is_conservative_deterministic_and_strict(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first"
            second = Path(directory) / "second"
            self.assertEqual(
                build.build(first, zero_corrections=True), (29, 1444, 0)
            )
            self.assertEqual(
                build.build(second, zero_corrections=True), (29, 1444, 0)
            )
            self.assertEqual(self._tree_manifest(first), self._tree_manifest(second))

            concatenated = b"".join(
                (first / document["output_path"]).read_bytes()
                for document in self.documents
            )
            self.assertEqual(concatenated, self.raw)
            validate.validate_output(
                first,
                self.raw,
                self.documents,
                [],
                self.images,
                zero_corrections=True,
            )

            document_paths = {
                document["id"]: Path(document["output_path"])
                for document in self.documents
            }
            for row in self.images:
                image_path = (
                    first
                    / document_paths[row["document_id"]].parent
                    / Path(row["asset_relative_path"]).name
                )
                self.assertEqual(build.sha256(image_path.read_bytes()), row["asset_sha256"])
            opener = self.images[1]
            self.assertIn("repaired_asset_sha256", opener)
            self.assertNotEqual(opener["asset_sha256"], opener["repaired_asset_sha256"])

            document_path = first / self.documents[0]["output_path"]
            original_document = document_path.read_bytes()
            document_path.write_bytes(original_document + b"x")
            with self.assertRaises(build.BuildError):
                validate.validate_output(
                    first,
                    self.raw,
                    self.documents,
                    [],
                    self.images,
                    zero_corrections=True,
                )
            document_path.write_bytes(original_document)

            image = self.images[0]
            image_path = (
                first
                / Path(self.documents[1]["output_path"]).parent
                / Path(image["asset_relative_path"]).name
            )
            original_image = image_path.read_bytes()
            image_path.write_bytes(original_image + b"x")
            with self.assertRaises(build.BuildError):
                validate.validate_output(
                    first,
                    self.raw,
                    self.documents,
                    [],
                    self.images,
                    zero_corrections=True,
                )
            image_path.write_bytes(original_image)

            extra = first / "unexpected.txt"
            extra.write_text("unexpected", encoding="utf-8")
            with self.assertRaises(build.BuildError):
                validate.validate_output(
                    first,
                    self.raw,
                    self.documents,
                    [],
                    self.images,
                    zero_corrections=True,
                )

            occupied = Path(directory) / "occupied"
            occupied.mkdir()
            with self.assertRaisesRegex(build.BuildError, "already exists"):
                build.build(occupied)


if __name__ == "__main__":
    unittest.main()
