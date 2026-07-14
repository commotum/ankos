from __future__ import annotations

import copy
import base64
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
    canonical_json_bytes,
    legacy_recursive_signature,
    load_json,
    sha256_bytes,
    sha256_file,
    validate_contract,
    validate_exact_goal_output,
    validate_publication_target,
    validate_root_relationship,
)
from capture_compatibility import probe_empty_sibling_lifecycle  # noqa: E402


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

    def test_contract_hash_registry_cannot_be_removed(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["contracts"] = []
        with self.assertRaisesRegex(GuardrailError, "contract hash registry"):
            self.validate_mutation(contract=contract)

    def test_duplicate_declared_output_is_rejected(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["declared_outputs"].append(copy.deepcopy(contract["declared_outputs"][0]))
        with self.assertRaisesRegex(GuardrailError, "output count"):
            self.validate_mutation(contract=contract)

    def test_asset_identity_and_publication_atomicity_are_frozen(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["asset_policy"]["preserve_distinct_asset_ids"] = False
        with self.assertRaisesRegex(GuardrailError, "asset identities"):
            self.validate_mutation(contract=contract)
        contract = copy.deepcopy(self.contract)
        contract["publication"]["atomic_same_filesystem_rename_required"] = False
        with self.assertRaisesRegex(GuardrailError, "publication safety gate"):
            self.validate_mutation(contract=contract)

    def test_serialization_and_scope_profiles_are_frozen(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["serialization"]["canonical_json_profile_id"] = "LOOSE-JSON"
        with self.assertRaisesRegex(GuardrailError, "generated JSON profile"):
            self.validate_mutation(contract=contract)
        contract = copy.deepcopy(self.contract)
        contract["architecture"]["forbidden_write_roots"].remove("goal-3")
        with self.assertRaisesRegex(GuardrailError, "forbidden write scope"):
            self.validate_mutation(contract=contract)

    def test_anchor_and_operation_risk_grammars_are_frozen(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["canonical_documents"][0]["anchor_slug"] = "has_underscore"
        with self.assertRaisesRegex(GuardrailError, "anchor-slug grammar"):
            self.validate_mutation(contract=contract)
        contract = copy.deepcopy(self.contract)
        contract["repair_policy"]["mandatory_high_risk_operations"] = []
        with self.assertRaisesRegex(GuardrailError, "high-risk operation"):
            self.validate_mutation(contract=contract)

    def test_whole_contract_digest_freezes_canonical_paths_and_role_meanings(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["canonical_documents"][0]["path"] = (
            "CANONICAL/FRONT-MATTER/00-Different.md"
        )
        with self.assertRaisesRegex(GuardrailError, "whole guardrail contract digest"):
            self.validate_mutation(contract=contract)
        contract = copy.deepcopy(self.contract)
        contract["role_definitions"]["CANONICAL_AUTHOR_TEXT"] = "weakened"
        with self.assertRaisesRegex(GuardrailError, "whole guardrail contract digest"):
            self.validate_mutation(contract=contract)

    def test_holdout_membership_cannot_become_outcome_aware(self) -> None:
        quality = copy.deepcopy(self.quality)
        quality["sample_size"]["changed_unchanged_rule"] = "select after repairs"
        with self.assertRaisesRegex(GuardrailError, "outcome-aware"):
            self.validate_mutation(quality=quality)


class PathAndPublicationTests(unittest.TestCase):
    def make_publication_layout(self, temporary: str) -> tuple[Path, Path, Path]:
        root = Path(temporary)
        legacy = root / "ref/A-New-Kind-of-Science"
        target = root / "ref/A-New-Kind-of-Science-Repaired"
        releases = root / "goal-4/releases"
        legacy.mkdir(parents=True)
        releases.mkdir(parents=True)
        return legacy, target, releases

    def write_trusted_manifest(
        self,
        releases: Path,
        rows: list[dict],
        *,
        name: str = "release.json",
    ) -> Path:
        path = releases / name
        path.write_text(
            json.dumps(
                {
                    "schema_version": "1.0.0",
                    "target": "ref/A-New-Kind-of-Science-Repaired",
                    "files": rows,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        return path

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
            Path("goal-4/../goal-4/compatibility-baseline.json"),
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
            legacy, target, releases = self.make_publication_layout(temporary)
            self.assertEqual(validate_publication_target(target, legacy), "ABSENT")
            target.mkdir()
            self.assertEqual(validate_publication_target(target, legacy), "EMPTY")
            payload = target / "README.md"
            payload.write_bytes(b"owned\n")
            with self.assertRaisesRegex(GuardrailError, "trusted external manifest"):
                validate_publication_target(target, legacy)
            rows = [
                {
                    "path": "README.md",
                    "entry_type": "FILE",
                    "sha256": sha256_file(payload),
                    "byte_size": payload.stat().st_size,
                    "mode": format(payload.stat().st_mode & 0o7777, "04o"),
                }
            ]
            trusted = self.write_trusted_manifest(releases, rows)
            self.assertEqual(validate_publication_target(target, legacy, trusted), "MANIFEST_OWNED")
            (target / "unowned-empty-directory").mkdir()
            with self.assertRaisesRegex(GuardrailError, "unowned"):
                validate_publication_target(target, legacy, trusted)

    def test_owned_target_hash_drift_and_symlink_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            legacy, target, releases = self.make_publication_layout(temporary)
            target.mkdir()
            payload = target / "release.txt"
            payload.write_bytes(b"v1")
            trusted = self.write_trusted_manifest(
                releases,
                [
                    {
                        "path": "release.txt",
                        "entry_type": "FILE",
                        "sha256": sha256_file(payload),
                        "byte_size": 2,
                        "mode": format(payload.stat().st_mode & 0o7777, "04o"),
                    }
                ],
            )
            payload.write_bytes(b"v2")
            with self.assertRaisesRegex(GuardrailError, "hash drift"):
                validate_publication_target(target, legacy, trusted)
            payload.unlink()
            payload.symlink_to(legacy, target_is_directory=True)
            with self.assertRaisesRegex(GuardrailError, "symlink"):
                validate_publication_target(target, legacy, trusted)

    def test_hardlinked_publication_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            legacy, target, releases = self.make_publication_layout(temporary)
            target.mkdir()
            source = legacy / "asset.jpeg"
            source.write_bytes(b"asset")
            linked = target / "asset.jpeg"
            os.link(source, linked)
            trusted = self.write_trusted_manifest(
                releases,
                [
                    {
                        "path": "asset.jpeg",
                        "entry_type": "FILE",
                        "sha256": sha256_file(linked),
                        "byte_size": linked.stat().st_size,
                        "mode": format(linked.stat().st_mode & 0o7777, "04o"),
                    }
                ],
            )
            with self.assertRaisesRegex(GuardrailError, "hardlinked"):
                validate_publication_target(target, legacy, trusted)

    def test_wrong_named_traversal_and_symlink_parent_targets_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            legacy, target, _ = self.make_publication_layout(temporary)
            with self.assertRaisesRegex(GuardrailError, "exact repaired sibling"):
                validate_publication_target(target.with_name("Different-Repaired"), legacy)
            alias_parent = target.parent / "alias-step"
            alias_parent.mkdir()
            traversal = alias_parent / ".." / target.name
            with self.assertRaisesRegex(GuardrailError, "contains '\\.\\.'"):
                validate_publication_target(traversal, legacy)
            symlink_parent = Path(temporary) / "ref-alias"
            symlink_parent.symlink_to(target.parent, target_is_directory=True)
            with self.assertRaisesRegex(GuardrailError, "symlink component"):
                validate_publication_target(symlink_parent / target.name, legacy)

    def test_target_local_or_outside_registry_manifest_is_not_trusted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            legacy, target, releases = self.make_publication_layout(temporary)
            target.mkdir()
            payload = target / "release.txt"
            payload.write_bytes(b"v1")
            rows = [
                {
                    "path": "release.txt",
                    "entry_type": "FILE",
                    "sha256": sha256_file(payload),
                    "byte_size": 2,
                    "mode": format(payload.stat().st_mode & 0o7777, "04o"),
                }
            ]
            trusted = self.write_trusted_manifest(releases, rows)
            target_local = target / "release.json"
            target_local.write_bytes(trusted.read_bytes())
            with self.assertRaisesRegex(GuardrailError, "outside the exact"):
                validate_publication_target(target, legacy, target_local)
            outside = Path(temporary) / "release.json"
            outside.write_bytes(trusted.read_bytes())
            with self.assertRaisesRegex(GuardrailError, "outside the exact"):
                validate_publication_target(target, legacy, outside)


class EmptySiblingLifecycleTests(unittest.TestCase):
    @staticmethod
    def baseline_rows() -> list[dict]:
        return [
            {
                "path": "goal-1/example.py",
                "status_kind": "EXITED",
                "exit_code": 0,
                "stdout_bytes": b"same",
                "stderr_bytes": b"",
                "framed_behavior_sha256": "fixture",
            }
        ]

    def test_probe_restores_absence_after_success(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "A-New-Kind-of-Science-Repaired"
            calls = 0

            def run_round() -> list[dict]:
                nonlocal calls
                calls += 1
                return copy.deepcopy(self.baseline_rows())

            sibling, post = probe_empty_sibling_lifecycle(
                target, self.baseline_rows(), run_round
            )
            self.assertEqual(sibling, post)
            self.assertEqual(calls, 2)
            self.assertFalse(target.exists())

    def test_probe_refuses_a_preexisting_empty_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "A-New-Kind-of-Science-Repaired"
            target.mkdir()
            with self.assertRaisesRegex(GuardrailError, "must be absent"):
                probe_empty_sibling_lifecycle(target, self.baseline_rows(), self.baseline_rows)
            self.assertTrue(target.is_dir())

    def test_probe_cleans_up_when_execution_raises(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "A-New-Kind-of-Science-Repaired"

            def fail() -> list[dict]:
                raise RuntimeError("synthetic oracle failure")

            with self.assertRaisesRegex(RuntimeError, "synthetic"):
                probe_empty_sibling_lifecycle(target, self.baseline_rows(), fail)
            self.assertFalse(target.exists())


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
    def validate_baseline(self, baseline: dict) -> None:
        validate_contract(
            load_json(ROOT / "goal-4/guardrails.json"),
            load_json(ROOT / "goal-4/quality-evaluation.json"),
            load_json(ROOT / "goal-4/licensing-contract.json"),
            ROOT,
            baseline=baseline,
            check_files=True,
            check_current_scripts=True,
        )

    def test_materialized_baseline_validates_when_present(self) -> None:
        baseline_path = ROOT / "goal-4/compatibility-baseline.json"
        if not baseline_path.exists():
            self.skipTest("compatibility baseline is materialized after the contract tests")
        self.validate_baseline(load_json(baseline_path))

    def test_output_byte_mutation_invalidates_baseline(self) -> None:
        baseline_path = ROOT / "goal-4/compatibility-baseline.json"
        if not baseline_path.exists():
            self.skipTest("compatibility baseline is materialized after the contract tests")
        baseline = load_json(baseline_path)
        baseline["oracles"][0]["stdout"]["base64"] = base64.b64encode(b"valid mutation").decode("ascii")
        with self.assertRaises(GuardrailError):
            self.validate_baseline(baseline)

    def test_fabricated_equal_closure_is_rejected_against_current_files(self) -> None:
        baseline_path = ROOT / "goal-4/compatibility-baseline.json"
        if not baseline_path.exists():
            self.skipTest("compatibility baseline is materialized after the contract tests")
        baseline = load_json(baseline_path)
        rows = baseline["closure"]["dependency_rows"]
        row = next(item for item in rows if not item["path"].startswith("ref/A-New-Kind-of-Science/"))
        row["sha256"] = "0" * 64 if row["sha256"] != "0" * 64 else "1" * 64
        forged = sha256_bytes(canonical_json_bytes(rows))
        baseline["closure"]["dependency_fingerprint_before"] = forged
        baseline["closure"]["dependency_fingerprint_after"] = forged
        for oracle in baseline["oracles"]:
            oracle["transitive_dependency_fingerprint"] = forged
        with self.assertRaisesRegex(GuardrailError, "current dependency closure"):
            self.validate_baseline(baseline)

    def test_classification_summary_and_probe_lifecycle_are_bound(self) -> None:
        baseline_path = ROOT / "goal-4/compatibility-baseline.json"
        if not baseline_path.exists():
            self.skipTest("compatibility baseline is materialized after the contract tests")
        baseline = load_json(baseline_path)
        baseline["classification_summary"]["all_count"] += 1
        with self.assertRaisesRegex(GuardrailError, "classification summary"):
            self.validate_baseline(baseline)
        baseline = load_json(baseline_path)
        baseline["empty_sibling_probe"]["final_state"] = "EMPTY"
        with self.assertRaisesRegex(GuardrailError, "restore absence"):
            self.validate_baseline(baseline)


if __name__ == "__main__":
    unittest.main()
