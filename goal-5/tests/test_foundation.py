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
        self.assertEqual(corrections, [])
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
                "proposed_output_path", data["documents"][0]["proposed_output_path"]
            ),
            "unsafe output": lambda data: data["documents"][1].__setitem__(
                "proposed_output_path", "../escaped.md"
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
        }
        valid = {
            "id": "C-0001",
            "document_id": "CH01",
            "raw_start_byte": 2,
            "before": "bad",
            "after": "good",
            "expected_count": 1,
            "authoritative_location": "p. 1",
            "reason": "OCR substitution",
            "reviewer_type": "agent",
            "verification_status": "SOURCE_VERIFIED",
        }
        checked = build.validate_corrections([valid], raw, [document])
        self.assertEqual(
            build.apply_corrections(document, raw, checked), b"a good token"
        )

        invalid = []
        missing = valid.copy()
        del missing["authoritative_location"]
        invalid.append(missing)
        unverified = valid.copy()
        unverified["verification_status"] = "INFERRED"
        invalid.append(unverified)
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
        self.assertTrue(all(row["first_pass"] == row["second_pass"] == "NO" for row in clean))

        variants: list[list[dict[str, str]]] = []
        variants.append(copy.deepcopy(clean[:-1]))
        duplicate = copy.deepcopy(clean)
        duplicate[-1]["document_id"] = duplicate[0]["document_id"]
        variants.append(duplicate)
        changed_bound = copy.deepcopy(clean)
        changed_bound[0]["raw_end_line"] = "999"
        variants.append(changed_bound)
        reversed_passes = copy.deepcopy(clean)
        reversed_passes[0]["second_pass"] = "YES"
        variants.append(reversed_passes)
        no_evidence = copy.deepcopy(clean)
        no_evidence[0]["first_pass"] = "YES"
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
            self.assertEqual(build.build(first), (29, 1444, 0))
            self.assertEqual(build.build(second), (29, 1444, 0))
            self.assertEqual(self._tree_manifest(first), self._tree_manifest(second))

            concatenated = b"".join(
                (first / document["proposed_output_path"]).read_bytes()
                for document in self.documents
            )
            self.assertEqual(concatenated, self.raw)
            validate.validate_output(
                first, self.raw, self.documents, [], self.images
            )

            document_path = first / self.documents[0]["proposed_output_path"]
            original_document = document_path.read_bytes()
            document_path.write_bytes(original_document + b"x")
            with self.assertRaises(build.BuildError):
                validate.validate_output(
                    first, self.raw, self.documents, [], self.images
                )
            document_path.write_bytes(original_document)

            image = self.images[0]
            image_path = (
                first
                / Path(self.documents[1]["proposed_output_path"]).parent
                / Path(image["asset_relative_path"]).name
            )
            original_image = image_path.read_bytes()
            image_path.write_bytes(original_image + b"x")
            with self.assertRaises(build.BuildError):
                validate.validate_output(
                    first, self.raw, self.documents, [], self.images
                )
            image_path.write_bytes(original_image)

            extra = first / "unexpected.txt"
            extra.write_text("unexpected", encoding="utf-8")
            with self.assertRaises(build.BuildError):
                validate.validate_output(
                    first, self.raw, self.documents, [], self.images
                )


if __name__ == "__main__":
    unittest.main()
