from __future__ import annotations

import json
import os
import shutil
import stat
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "goal-4/tools"
sys.path.insert(0, str(TOOLS))

from zero_repair_lib import (  # noqa: E402
    EXPECTED_BLOCKS,
    EXPECTED_MONOLITH_BYTES,
    EXPECTED_MONOLITH_SHA256,
    MANIFEST_RELATIVE,
    TAPE_RELATIVE,
    ZeroRepairError,
    build_zero_repair,
    canonical_json_bytes,
    compare_zero_repair_trees,
    parse_jsonl_bytes,
    validate_zero_repair,
)


class ZeroRepairBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory(prefix="ankos-zero-repair-tests-")
        cls.temp_root = Path(cls.temporary.name)
        cls.first = cls.temp_root / "clean-a"
        cls.second = cls.temp_root / "clean-b"
        cls.first_result = build_zero_repair(ROOT, cls.first)
        cls.second_result = build_zero_repair(ROOT, cls.second)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def clone(self, name: str) -> Path:
        destination = self.temp_root / name
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(self.first, destination)
        return destination

    def test_real_build_has_29_documents_and_true_inverse(self) -> None:
        result = validate_zero_repair(ROOT, self.first)
        self.assertEqual(result["canonical_documents"], 29)
        self.assertEqual(result["source_blocks"], EXPECTED_BLOCKS)
        self.assertEqual(result["projection_tape_rows"], EXPECTED_BLOCKS + 1)
        self.assertEqual(result["generated_spans"], 1)
        self.assertEqual(result["inverse_byte_size"], EXPECTED_MONOLITH_BYTES)
        self.assertEqual(result["inverse_sha256"], EXPECTED_MONOLITH_SHA256)
        self.assertEqual(len(list((self.first / "CANONICAL").rglob("*.md"))), 29)
        self.assertEqual(len(list(self.first.rglob("*.jpeg"))), 0)

    def test_two_clean_builds_are_byte_identical(self) -> None:
        comparison = compare_zero_repair_trees(self.first, self.second)
        self.assertEqual(comparison["file_and_directory_records"], 37)
        self.assertRegex(comparison["full_tree_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(self.first_result["manifest_sha256"], self.second_result["manifest_sha256"])
        self.assertEqual(self.first_result["projection_tape_sha256"], self.second_result["projection_tape_sha256"])

    def test_tape_is_opaque_and_has_one_typed_colophon_wrapper(self) -> None:
        tape = parse_jsonl_bytes(
            (self.first / TAPE_RELATIVE).read_bytes(),
            label="test projection tape",
            canonical=True,
        )
        source_rows = [row for row in tape if row["record_type"] == "SOURCE_BLOCK"]
        generated = [row for row in tape if row["record_type"] == "GENERATED_METADATA"]
        self.assertEqual(len(source_rows), EXPECTED_BLOCKS)
        self.assertTrue(all("block_kind" not in row and "node_type" not in row for row in source_rows))
        self.assertEqual(
            generated,
            [
                {
                    "author_text_projection_byte_size": 0,
                    "document_id": "COLOPHON",
                    "document_order": 28,
                    "generated_kind": "FILE_TERMINATOR_LF",
                    "inverse": "DROP_EXACT_BYTES",
                    "output_end_byte_exclusive": 2974,
                    "output_path": "CANONICAL/BACK-MATTER/Colophon.md",
                    "output_sha256": "01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b",
                    "output_start_byte": 2973,
                    "record_type": "GENERATED_METADATA",
                    "schema_version": "1.0.0",
                    "tape_order": EXPECTED_BLOCKS + 1,
                }
            ],
        )

    def test_author_file_byte_mutation_fails(self) -> None:
        tree = self.clone("mutated-author-byte")
        path = tree / "CANONICAL/CHAPTERS/01-The-Foundations-for-a-New-Kind-of-Science.md"
        payload = bytearray(path.read_bytes())
        payload[10] ^= 1
        path.write_bytes(payload)
        os.chmod(path, 0o644)
        with self.assertRaisesRegex(ZeroRepairError, "canonical zero-repair bytes drift"):
            validate_zero_repair(ROOT, tree)

    def test_missing_colophon_wrapper_lf_fails(self) -> None:
        tree = self.clone("missing-wrapper-lf")
        path = tree / "CANONICAL/BACK-MATTER/Colophon.md"
        payload = path.read_bytes()
        self.assertTrue(payload.endswith(b"\n"))
        path.write_bytes(payload[:-1])
        os.chmod(path, 0o644)
        with self.assertRaisesRegex(ZeroRepairError, "canonical zero-repair bytes drift"):
            validate_zero_repair(ROOT, tree)

    def test_projection_span_gap_fails(self) -> None:
        tree = self.clone("projection-gap")
        path = tree / TAPE_RELATIVE
        rows = parse_jsonl_bytes(path.read_bytes(), label="mutable tape", canonical=True)
        rows[1]["output_start_byte"] += 1
        path.write_bytes(b"".join(canonical_json_bytes(row) for row in rows))
        os.chmod(path, 0o644)
        with self.assertRaisesRegex(ZeroRepairError, "projection tape differs"):
            validate_zero_repair(ROOT, tree)

    def test_extra_file_and_wrong_mode_fail_ownership(self) -> None:
        extra_tree = self.clone("extra-file")
        extra = extra_tree / "CANONICAL/unowned.md"
        extra.write_bytes(b"unowned\n")
        os.chmod(extra, 0o644)
        with self.assertRaisesRegex(ZeroRepairError, "output file ownership drift"):
            validate_zero_repair(ROOT, extra_tree)

        mode_tree = self.clone("wrong-mode")
        path = mode_tree / "CANONICAL/BACK-MATTER/Index.md"
        os.chmod(path, 0o600)
        with self.assertRaisesRegex(ZeroRepairError, "output file mode drift"):
            validate_zero_repair(ROOT, mode_tree)

    def test_output_symlink_fails(self) -> None:
        tree = self.clone("output-symlink")
        path = tree / "CANONICAL/BACK-MATTER/Colophon.md"
        path.unlink()
        os.symlink("Index.md", path)
        with self.assertRaisesRegex(ZeroRepairError, "not a regular file"):
            validate_zero_repair(ROOT, tree)

    def test_preexisting_output_is_not_an_input(self) -> None:
        with self.assertRaisesRegex(ZeroRepairError, "already exists"):
            build_zero_repair(ROOT, self.first)

    def test_repaired_sibling_and_legacy_descendant_are_never_outputs(self) -> None:
        repaired = ROOT / "ref/A-New-Kind-of-Science-Repaired"
        with self.assertRaisesRegex(ZeroRepairError, "aliases a governed root"):
            build_zero_repair(ROOT, repaired)
        legacy_child = ROOT / "ref/A-New-Kind-of-Science/zero-repair-forbidden"
        with self.assertRaisesRegex(ZeroRepairError, "immutable legacy root"):
            build_zero_repair(ROOT, legacy_child)
        self.assertFalse(legacy_child.exists())

    def test_comparison_detects_a_different_tree(self) -> None:
        tree = self.clone("comparison-drift")
        path = tree / MANIFEST_RELATIVE
        payload = bytearray(path.read_bytes())
        payload[-2] ^= 1
        path.write_bytes(payload)
        os.chmod(path, 0o644)
        with self.assertRaisesRegex(ZeroRepairError, "not byte-identical"):
            compare_zero_repair_trees(self.first, tree)

    def test_relocated_no_git_read_only_inputs_build(self) -> None:
        portable_parent = self.temp_root / "portable-fixture"
        portable = portable_parent / "repo"
        goal = portable / "policy"
        legacy = portable / "corpus"
        tools = goal / "tools"
        tools.mkdir(parents=True)
        legacy.mkdir(parents=True)
        for name in (
            "guardrails.json",
            "baseline-lock.json",
            "corpus-manifest.json",
            "structure-ledger.jsonl",
        ):
            shutil.copyfile(ROOT / "goal-4" / name, goal / name)
        for name in (
            "zero_repair_lib.py",
            "build_zero_repair.py",
            "validate_zero_repair.py",
        ):
            shutil.copyfile(ROOT / "goal-4/tools" / name, tools / name)
        shutil.copyfile(
            ROOT / "ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md",
            legacy / "A-New-Kind-of-Science.md",
        )
        for path in portable.rglob("*"):
            if path.is_file():
                os.chmod(path, 0o444)
        directories = sorted(
            (path for path in portable.rglob("*") if path.is_dir()),
            key=lambda item: len(item.parts),
            reverse=True,
        )
        for directory in directories:
            os.chmod(directory, 0o555)
        os.chmod(portable, 0o555)
        output = portable_parent / "relocated-output"
        try:
            result = build_zero_repair(
                portable,
                output,
                goal_root=Path("policy"),
                legacy_root=Path("corpus"),
            )
            self.assertEqual(result["inverse_sha256"], EXPECTED_MONOLITH_SHA256)
            self.assertFalse((portable / ".git").exists())
        finally:
            for directory in [portable, *reversed(directories)]:
                if directory.exists() and stat.S_ISDIR(os.lstat(directory).st_mode):
                    os.chmod(directory, 0o755)


if __name__ == "__main__":
    unittest.main()
