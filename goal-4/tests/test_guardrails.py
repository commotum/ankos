from __future__ import annotations

import copy
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "goal-4/tools"
sys.path.insert(0, str(TOOLS))

from guardrail_lib import (  # noqa: E402
    GuardrailError,
    legacy_recursive_signature,
    load_json,
    sha256_file,
    validate_contract,
    validate_exact_goal_output,
    validate_publication_target,
    validate_root_relationship,
)


class GuardrailContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = load_json(ROOT / "goal-4/guardrails.json")
        cls.quality = load_json(ROOT / "goal-4/quality-evaluation.json")
        cls.licensing = load_json(ROOT / "goal-4/licensing-contract.json")

    def validate_mutation(
        self,
        contract: dict | None = None,
        quality: dict | None = None,
        licensing: dict | None = None,
    ) -> None:
        validate_contract(
            contract or copy.deepcopy(self.contract),
            quality or copy.deepcopy(self.quality),
            licensing or copy.deepcopy(self.licensing),
            ROOT,
            baseline=None,
            check_files=False,
        )

    def test_current_contract_and_frozen_files_validate(self) -> None:
        validate_contract(
            self.contract,
            self.quality,
            self.licensing,
            ROOT,
            baseline=None,
            check_files=True,
        )

    def test_exact_29_document_count_is_enforced(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["canonical_documents"].pop()
        with self.assertRaisesRegex(GuardrailError, "count must be 29"):
            self.validate_mutation(contract=contract)

    def test_aggregate_cannot_be_retyped_as_canonical(self) -> None:
        contract = copy.deepcopy(self.contract)
        for row in contract["declared_outputs"]:
            if row["path"] == "DERIVED/A-New-Kind-of-Science.md":
                row["role"] = "CANONICAL_AUTHOR_TEXT"
        with self.assertRaisesRegex(GuardrailError, "output paths/roles drift"):
            self.validate_mutation(contract=contract)

    def test_review_independence_cannot_be_disabled(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["review_policy"]["creator_and_reviewer_must_differ"] = False
        with self.assertRaisesRegex(GuardrailError, "review gate disabled"):
            self.validate_mutation(contract=contract)

    def test_every_author_text_change_requires_independent_review(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["review_policy"]["every_author_text_change_independent_source_review"] = False
        with self.assertRaisesRegex(GuardrailError, "review gate disabled"):
            self.validate_mutation(contract=contract)

    def test_illegible_author_text_cannot_be_not_applicable(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["evidence_policy"]["not_applicable_for_authorial_or_illegible_content"] = True
        with self.assertRaisesRegex(GuardrailError, "hide authorial content"):
            self.validate_mutation(contract=contract)

    def test_author_text_quality_threshold_cannot_be_weakened(self) -> None:
        quality = copy.deepcopy(self.quality)
        quality["metrics"]["author_text_character_projection_exactness"]["minimum_ratio"] = {
            "numerator": 999,
            "denominator": 1000,
        }
        with self.assertRaisesRegex(GuardrailError, "threshold weakened"):
            self.validate_mutation(quality=quality)

    def test_sample_quota_formula_cannot_drift(self) -> None:
        quality = copy.deepcopy(self.quality)
        quality["sample_size"]["document_quota"] = "5 percent"
        with self.assertRaisesRegex(GuardrailError, "quota is not exact"):
            self.validate_mutation(quality=quality)

    def test_external_redistribution_is_not_implicitly_authorized(self) -> None:
        licensing = copy.deepcopy(self.licensing)
        for row in licensing["current_records"]:
            if row["artifact_class"] == "EXTERNAL_REPAIRED_EDITION_REDISTRIBUTION":
                row["state"] = "COMMIT_ALLOWED"
        with self.assertRaisesRegex(GuardrailError, "implicitly authorized"):
            self.validate_mutation(licensing=licensing)

    def test_mechanical_author_text_changes_remain_forbidden(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["repair_policy"]["mechanically_proven_author_text_token_changes_allowed"] = True
        with self.assertRaisesRegex(GuardrailError, "Mechanical|mechanical"):
            self.validate_mutation(contract=contract)


class PathAndPublicationTests(unittest.TestCase):
    def test_compatibility_output_is_exactly_goal_owned(self) -> None:
        expected = validate_exact_goal_output(
            ROOT,
            Path("goal-4/compatibility-baseline.json"),
            "goal-4/compatibility-baseline.json",
        )
        self.assertEqual(expected, ROOT / "goal-4/compatibility-baseline.json")
        for unsafe in (
            Path("ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md"),
            Path("goal-1/compatibility-baseline.json"),
            Path("goal-4/../goal-1/compatibility-baseline.json"),
        ):
            with self.assertRaises(GuardrailError):
                validate_exact_goal_output(
                    ROOT,
                    unsafe,
                    "goal-4/compatibility-baseline.json",
                )

    def test_prefix_named_sibling_is_component_wise_valid(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "ref/A-New-Kind-of-Science").mkdir(parents=True)
            legacy, repaired = validate_root_relationship(
                root,
                "ref/A-New-Kind-of-Science",
                "ref/A-New-Kind-of-Science-Repaired",
            )
            self.assertEqual(legacy.parent, repaired.parent)
            self.assertTrue(str(repaired).startswith(str(legacy)))
            self.assertFalse(repaired.is_relative_to(legacy))

    def test_equal_descendant_and_traversal_output_roots_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "ref/A-New-Kind-of-Science").mkdir(parents=True)
            with self.assertRaises(GuardrailError):
                validate_root_relationship(root, "ref/A-New-Kind-of-Science", "ref/A-New-Kind-of-Science")
            with self.assertRaises(GuardrailError):
                validate_root_relationship(
                    root,
                    "ref/A-New-Kind-of-Science",
                    "ref/A-New-Kind-of-Science/REPAIRED",
                )
            with self.assertRaises(GuardrailError):
                validate_root_relationship(
                    root,
                    "ref/A-New-Kind-of-Science",
                    "ref/../ref/A-New-Kind-of-Science-Repaired",
                )

    def test_symlink_alias_output_root_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            legacy = root / "ref/A-New-Kind-of-Science"
            legacy.mkdir(parents=True)
            (root / "ref/A-New-Kind-of-Science-Repaired").symlink_to(legacy, target_is_directory=True)
            with self.assertRaisesRegex(GuardrailError, "symlink"):
                validate_root_relationship(
                    root,
                    "ref/A-New-Kind-of-Science",
                    "ref/A-New-Kind-of-Science-Repaired",
                )

    def test_publication_target_absent_empty_owned_and_unowned(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            legacy = root / "A-New-Kind-of-Science"
            target = root / "A-New-Kind-of-Science-Repaired"
            legacy.mkdir()
            self.assertEqual(validate_publication_target(target, legacy), "ABSENT")
            target.mkdir()
            self.assertEqual(validate_publication_target(target, legacy), "EMPTY")
            payload = target / "README.md"
            payload.write_bytes(b"owned\n")
            with self.assertRaisesRegex(GuardrailError, "trusted external manifest"):
                validate_publication_target(target, legacy)
            trusted = {
                "files": [
                    {
                        "path": "README.md",
                        "entry_type": "FILE",
                        "sha256": sha256_file(payload),
                        "byte_size": payload.stat().st_size,
                        "mode": format(payload.stat().st_mode & 0o7777, "04o"),
                    }
                ]
            }
            self.assertEqual(validate_publication_target(target, legacy, trusted), "MANIFEST_OWNED")
            (target / "unowned-empty-directory").mkdir()
            with self.assertRaisesRegex(GuardrailError, "unowned"):
                validate_publication_target(target, legacy, trusted)

    def test_owned_target_hash_drift_and_symlink_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            legacy = root / "A-New-Kind-of-Science"
            target = root / "A-New-Kind-of-Science-Repaired"
            legacy.mkdir()
            target.mkdir()
            payload = target / "release.txt"
            payload.write_bytes(b"v1")
            trusted = {
                "files": [
                    {
                        "path": "release.txt",
                        "entry_type": "FILE",
                        "sha256": sha256_file(payload),
                        "byte_size": 2,
                        "mode": format(payload.stat().st_mode & 0o7777, "04o"),
                    }
                ]
            }
            payload.write_bytes(b"v2")
            with self.assertRaisesRegex(GuardrailError, "hash drift"):
                validate_publication_target(target, legacy, trusted)
            payload.unlink()
            payload.symlink_to(legacy, target_is_directory=True)
            with self.assertRaisesRegex(GuardrailError, "symlink"):
                validate_publication_target(target, legacy, trusted)

    def test_hardlinked_publication_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            legacy = root / "A-New-Kind-of-Science"
            target = root / "A-New-Kind-of-Science-Repaired"
            legacy.mkdir()
            target.mkdir()
            source = legacy / "asset.jpeg"
            source.write_bytes(b"asset")
            linked = target / "asset.jpeg"
            os.link(source, linked)
            trusted = {
                "files": [
                    {
                        "path": "asset.jpeg",
                        "entry_type": "FILE",
                        "sha256": sha256_file(linked),
                        "byte_size": linked.stat().st_size,
                        "mode": format(linked.stat().st_mode & 0o7777, "04o"),
                    }
                ]
            }
            with self.assertRaisesRegex(GuardrailError, "hardlinked"):
                validate_publication_target(target, legacy, trusted)


class ConsumerContaminationTests(unittest.TestCase):
    def test_sibling_is_invisible_but_nested_output_contaminates_signature(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            legacy = root / "A-New-Kind-of-Science"
            sibling = root / "A-New-Kind-of-Science-Repaired"
            legacy.mkdir()
            sibling.mkdir()
            (legacy / "book.md").write_bytes(b"raw")
            (legacy / "asset.jpeg").write_bytes(b"jpeg")
            baseline = legacy_recursive_signature(legacy)
            (sibling / "book.md").write_bytes(b"repaired")
            (sibling / "asset.jpeg").write_bytes(b"copy")
            self.assertEqual(legacy_recursive_signature(legacy), baseline)
            nested = legacy / "REPAIRED"
            nested.mkdir()
            (nested / "book.md").write_bytes(b"repaired")
            (nested / "asset.jpeg").write_bytes(b"copy")
            contaminated = legacy_recursive_signature(legacy)
            self.assertNotEqual(contaminated["signature_sha256"], baseline["signature_sha256"])
            self.assertIn("asset.jpeg", contaminated["duplicate_jpeg_basenames"])


class BaselineTests(unittest.TestCase):
    def test_materialized_baseline_validates_when_present(self) -> None:
        baseline_path = ROOT / "goal-4/compatibility-baseline.json"
        if not baseline_path.exists():
            self.skipTest("compatibility baseline is materialized after the contract tests")
        validate_contract(
            load_json(ROOT / "goal-4/guardrails.json"),
            load_json(ROOT / "goal-4/quality-evaluation.json"),
            load_json(ROOT / "goal-4/licensing-contract.json"),
            ROOT,
            baseline=load_json(baseline_path),
            check_files=True,
            check_current_scripts=True,
        )

    def test_output_byte_mutation_invalidates_baseline(self) -> None:
        baseline_path = ROOT / "goal-4/compatibility-baseline.json"
        if not baseline_path.exists():
            self.skipTest("compatibility baseline is materialized after the contract tests")
        baseline = load_json(baseline_path)
        baseline["oracles"][0]["stdout"]["base64"] += "AA=="
        with self.assertRaises(GuardrailError):
            validate_contract(
                load_json(ROOT / "goal-4/guardrails.json"),
                load_json(ROOT / "goal-4/quality-evaluation.json"),
                load_json(ROOT / "goal-4/licensing-contract.json"),
                ROOT,
                baseline=baseline,
                check_files=True,
                check_current_scripts=True,
            )


if __name__ == "__main__":
    unittest.main()
