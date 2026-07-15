#!/usr/bin/env python3
"""Hostile integration tests for the production overlay registry boundary."""

from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "goal-4" / "tools"
sys.path.insert(0, str(TOOLS))

import overlay_lib  # noqa: E402
import overlay_registry  # noqa: E402
import pipeline_schema_lib as pipeline  # noqa: E402


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def copy_file(source_root: Path, destination_root: Path, relative: str) -> None:
    source = source_root / relative
    destination = destination_root / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def clone_registry_root() -> tempfile.TemporaryDirectory[str]:
    temporary = tempfile.TemporaryDirectory(prefix="ankos-overlay-registry-")
    destination = Path(temporary.name) / "repo"
    destination.mkdir()
    paths = {
        "goal-4/baseline-lock.json",
        "goal-4/witness-lock.json",
        "goal-4/pipeline-schema-lock.json",
        "goal-4/guardrails.json",
        "goal-4/compatibility-baseline.json",
        "goal-4/licensing-contract.json",
        "goal-4/review-contract.md",
        "goal-4/style-guide.md",
        overlay_registry.MONOLITH_PATH,
    }
    for lock_path in (
        "goal-4/baseline-lock.json",
        "goal-4/witness-lock.json",
        "goal-4/pipeline-schema-lock.json",
    ):
        lock = json.loads((ROOT / lock_path).read_text(encoding="utf-8"))
        for bucket in ("artifacts", "sources"):
            for row in lock.get(bucket, []):
                paths.add(row["path"])
    for relative in sorted(paths):
        copy_file(ROOT, destination, relative)
    (destination / "ref" / "A-New-Kind-of-Science-Repaired").mkdir(parents=True)
    temporary.repo_root = destination  # type: ignore[attr-defined]
    return temporary


class RealCorpusRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.snapshot = overlay_registry._load_snapshot(ROOT)  # type: ignore[attr-defined]
        cls.state = cls.snapshot.state
        cls.guardrails = json.loads((ROOT / "goal-4/guardrails.json").read_text(encoding="utf-8"))

    def test_real_state_is_exactly_29_targets_and_20430_blocks(self) -> None:
        self.assertEqual(len(self.state.target_keys), 29)
        self.assertEqual(set(self.state.roles), {overlay_lib.CANONICAL_AUTHOR_TEXT})
        self.assertEqual(
            sum(
                len(self.state.blocks(role, target_id))
                for target_id, role in self.state.target_keys
            ),
            20430,
        )
        expected_keys = tuple(
            sorted(
                (row["id"], overlay_lib.CANONICAL_AUTHOR_TEXT)
                for row in self.guardrails["canonical_documents"]
            )
        )
        self.assertEqual(self.state.target_keys, expected_keys)

    def test_real_state_concatenation_and_empty_inverse_are_identities(self) -> None:
        recovered = b"".join(
            block.data
            for document in self.guardrails["canonical_documents"]
            for block in self.state.blocks(
                overlay_lib.CANONICAL_AUTHOR_TEXT, document["id"]
            )
        )
        monolith = (ROOT / overlay_registry.MONOLITH_PATH).read_bytes()
        self.assertEqual(recovered, monolith)
        self.assertEqual(sha256(recovered), overlay_registry.MONOLITH_SHA256)
        replay = overlay_lib.apply_overlays(self.state, ())
        self.assertEqual(replay.state, self.state)
        self.assertEqual(overlay_lib.inverse_replay(replay), self.state)

    def mint(self, state: overlay_lib.OverlayState, operations: object) -> object:
        # The real loader is exercised once for this class and afresh by every
        # filesystem mutation test.  Reusing that immutable result here keeps
        # caller-input mutation tests focused and avoids repeated 20,430-row
        # schema-package scans.
        with mock.patch.object(
            overlay_registry, "_load_snapshot", return_value=self.snapshot
        ):
            return overlay_registry.mint_production_authority(
                ROOT, state, operations  # type: ignore[arg-type]
            )

    def canonical_operation(self) -> overlay_lib.Replace:
        document = self.guardrails["canonical_documents"][0]
        target_id = document["id"]
        blocks = self.state.blocks(overlay_lib.CANONICAL_AUTHOR_TEXT, target_id)
        source = blocks[0]
        replacement_data = source.data + b"X"
        after = (overlay_lib.Block(source.block_id, replacement_data),) + blocks[1:]
        meta = overlay_lib.OperationMeta(
            repair_id="REPAIR-REGISTRY-TEST-0001",
            target_id=target_id,
            target_path=document["path"],
            raw_source_id=source.block_id,
            raw_source_span_sha256=source.sha256,
            raw_source_row_sha256=self.snapshot.block_row_sha256s[source.block_id],
            target_role=overlay_lib.CANONICAL_AUTHOR_TEXT,
            repair_class=overlay_lib.PROSE_OCR,
            expected_target_sha256=self.state.target_sha256(
                overlay_lib.CANONICAL_AUTHOR_TEXT, target_id
            ),
            expected_result_sha256=overlay_lib.target_sha256(
                target_id, overlay_lib.CANONICAL_AUTHOR_TEXT, after
            ),
            creator_principal_id="registry-test-creator",
            workflow_state="CLOSED",
            final_disposition="APPLIED_WITNESS_VERIFIED",
        )
        return overlay_lib.Replace(
            meta,
            source.block_id,
            source.sha256,
            source.data,
            replacement_data,
            1,
        )

    def test_current_real_gate_categorically_refuses_canonical_authority(self) -> None:
        operation = self.canonical_operation()
        with self.assertRaisesRegex(
            overlay_registry.RegistryGateError,
            "SOURCE_BLOCKED.*zero authorized witness regions",
        ):
            self.mint(self.state, (operation,))

    def test_arbitrary_target_state_drift_is_rejected_before_gate(self) -> None:
        operation = self.canonical_operation()
        targets = {
            (target_id, role): self.state.blocks(role, target_id)
            for target_id, role in self.state.target_keys
        }
        key = self.state.target_keys[0]
        targets[key] = targets[key][1:]
        drifted = overlay_lib.OverlayState.from_mapping(targets)
        with self.assertRaisesRegex(
            overlay_registry.RegistryError, "initial overlay state differs"
        ):
            self.mint(drifted, (operation,))

    def test_raw_row_substitution_is_rejected_before_gate(self) -> None:
        operation = self.canonical_operation()
        forged = replace(
            operation,
            meta=replace(operation.meta, raw_source_row_sha256="0" * 64),
        )
        with self.assertRaisesRegex(
            overlay_registry.RegistryError, "raw source row hash drift"
        ):
            self.mint(self.state, (forged,))

    def test_target_hash_substitution_is_rejected_before_gate(self) -> None:
        operation = self.canonical_operation()
        forged = replace(
            operation,
            meta=replace(operation.meta, expected_target_sha256="0" * 64),
        )
        with self.assertRaisesRegex(
            overlay_registry.RegistryError, "exact target pre-state guard drift"
        ):
            self.mint(self.state, (forged,))

    def test_noncanonical_operation_cannot_enter_canonical_authority(self) -> None:
        operation = self.canonical_operation()
        noncanonical = replace(
            operation,
            meta=replace(
                operation.meta,
                target_role=overlay_lib.EDITORIAL_SIDECAR,
                repair_class=overlay_lib.SOURCE_ERRATUM_ANNOTATION,
                final_disposition="ANNOTATED_SOURCE_ERRATUM",
            ),
        )
        with self.assertRaisesRegex(
            overlay_registry.RegistryError, "cannot include noncanonical roles"
        ):
            self.mint(self.state, (noncanonical,))

    def test_public_executor_rejects_test_only_authority_for_real_state(self) -> None:
        operation = self.canonical_operation()
        synthetic = overlay_lib._test_only_application_authority(  # type: ignore[attr-defined]
            self.state, (operation,)
        )
        self.assertTrue(synthetic.synthetic_test_only)
        with self.assertRaisesRegex(
            overlay_lib.EvidenceError, "rejects synthetic test-only authority"
        ):
            overlay_lib.apply_overlays(
                self.state, (operation,), authority=synthetic
            )

    def test_registry_digest_binds_every_validated_repair_vector(self) -> None:
        operation = self.canonical_operation()
        binding = pipeline.ValidatedRepairBinding(
            repair_id=operation.meta.repair_id,
            repair_row_sha256=sha256(b"repair row"),
            operation_projection_sha256=overlay_lib.operation_projection_sha256(
                operation
            ),
            expected_target_sha256=operation.meta.expected_target_sha256,
            expected_result_sha256=operation.meta.expected_result_sha256,
            forward_payload_sha256=sha256(b"forward payload"),
            inverse_payload_sha256=sha256(b"inverse payload"),
            overlay_operation_bound=True,
        )
        expected = overlay_registry._registry_digest(  # type: ignore[attr-defined]
            self.snapshot, (binding,)
        )
        for field in (
            "repair_row_sha256",
            "operation_projection_sha256",
            "expected_target_sha256",
            "expected_result_sha256",
            "forward_payload_sha256",
            "inverse_payload_sha256",
        ):
            with self.subTest(field=field):
                forged = replace(
                    binding, **{field: sha256(f"forged {field}".encode())}
                )
                self.assertNotEqual(
                    overlay_registry._registry_digest(  # type: ignore[attr-defined]
                        self.snapshot, (forged,)
                    ),
                    expected,
                )

    def test_production_factory_receives_literal_validated_binding_fields(self) -> None:
        operation = self.canonical_operation()
        binding = pipeline.ValidatedRepairBinding(
            repair_id=operation.meta.repair_id,
            repair_row_sha256=sha256(b"exact repair ledger row"),
            operation_projection_sha256=overlay_lib.operation_projection_sha256(
                operation
            ),
            expected_target_sha256=operation.meta.expected_target_sha256,
            expected_result_sha256=operation.meta.expected_result_sha256,
            forward_payload_sha256=sha256(b"exact forward payload"),
            inverse_payload_sha256=sha256(b"exact inverse payload"),
            overlay_operation_bound=True,
        )
        present_repairs = overlay_registry._Ledger(  # type: ignore[attr-defined]
            overlay_registry.REPAIR_LEDGER_PATH,
            True,
            sha256(b"repair ledger"),
            ({"repair_id": operation.meta.repair_id},),
            (binding.repair_row_sha256,),
        )
        present_reviews = overlay_registry._Ledger(  # type: ignore[attr-defined]
            overlay_registry.REVIEW_LEDGER_PATH,
            True,
            sha256(b"review ledger"),
            (),
            (),
        )
        opened = replace(
            self.snapshot,
            witness_status="OPEN",
            witness_region_ids=frozenset({"WITNESS-REGION-0001"}),
            repair_ledger=present_repairs,
            review_ledger=present_reviews,
        )
        sentinel = object()
        with (
            mock.patch.object(
                overlay_registry, "_load_snapshot", return_value=opened
            ),
            mock.patch.object(
                pipeline,
                "validate_overlay_operation_binding",
                return_value=binding,
            ),
            mock.patch.object(
                pipeline,
                "validate_overlay_witness_binding",
                return_value=None,
                create=True,
            ),
            mock.patch.object(
                overlay_lib,
                "_application_authority_from_validated_registry",
                return_value=sentinel,
            ) as factory,
        ):
            result = overlay_registry.mint_production_authority(
                ROOT, self.state, (operation,)
            )
        self.assertIs(result, sentinel)
        grant = factory.call_args.kwargs["grants"][0]
        self.assertEqual(grant.repair_row_sha256, binding.repair_row_sha256)
        self.assertEqual(grant.expected_target_sha256, binding.expected_target_sha256)
        self.assertEqual(grant.expected_result_sha256, binding.expected_result_sha256)
        self.assertEqual(grant.forward_payload_sha256, binding.forward_payload_sha256)
        self.assertEqual(grant.inverse_payload_sha256, binding.inverse_payload_sha256)


class FrozenArtifactMutationTests(unittest.TestCase):
    def test_target_path_drift_in_guardrails_is_rejected(self) -> None:
        temporary = clone_registry_root()
        self.addCleanup(temporary.cleanup)
        root = temporary.repo_root  # type: ignore[attr-defined]
        path = root / "goal-4/guardrails.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        value["canonical_documents"][0]["path"] = "CANONICAL/FORGED.md"
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(
            overlay_registry.RegistryError, "guardrails digest drift"
        ):
            overlay_registry.load_frozen_overlay_state(root)

    def test_raw_block_ledger_drift_is_rejected(self) -> None:
        temporary = clone_registry_root()
        self.addCleanup(temporary.cleanup)
        root = temporary.repo_root  # type: ignore[attr-defined]
        path = root / "goal-4/structure-ledger.jsonl"
        lines = path.read_bytes().splitlines(keepends=True)
        row = json.loads(lines[29])
        row["raw_sha256"] = "0" * 64
        lines[29] = pipeline.canonical_json_bytes(row)
        path.write_bytes(b"".join(lines))
        with self.assertRaisesRegex(
            overlay_registry.RegistryError, "locked (?:byte-size|artifact) drift"
        ):
            overlay_registry.load_frozen_overlay_state(root)

    def test_monolith_raw_byte_drift_is_rejected(self) -> None:
        temporary = clone_registry_root()
        self.addCleanup(temporary.cleanup)
        root = temporary.repo_root  # type: ignore[attr-defined]
        path = root / overlay_registry.MONOLITH_PATH
        raw = bytearray(path.read_bytes())
        raw[0] ^= 1
        path.write_bytes(raw)
        with self.assertRaisesRegex(
            overlay_registry.RegistryError, "raw monolith byte/hash drift"
        ):
            overlay_registry.load_frozen_overlay_state(root)

    def test_self_consistent_baseline_lock_replacement_is_rejected(self) -> None:
        temporary = clone_registry_root()
        self.addCleanup(temporary.cleanup)
        root = temporary.repo_root  # type: ignore[attr-defined]
        structure = root / "goal-4/structure-ledger.jsonl"
        structure.write_bytes(structure.read_bytes() + b"{}\n")
        lock_path = root / "goal-4/baseline-lock.json"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        row = next(
            item
            for item in lock["artifacts"]
            if item["path"] == "goal-4/structure-ledger.jsonl"
        )
        row["byte_size"] = structure.stat().st_size
        row["sha256"] = sha256(structure.read_bytes())
        lock_path.write_bytes(pipeline.canonical_json_bytes(lock))
        with self.assertRaisesRegex(
            overlay_registry.RegistryError, "externally pinned lock replacement"
        ):
            overlay_registry.load_frozen_overlay_state(root)

    def test_fake_witness_region_is_rejected_by_actual_witness_lock(self) -> None:
        temporary = clone_registry_root()
        self.addCleanup(temporary.cleanup)
        root = temporary.repo_root  # type: ignore[attr-defined]
        path = root / "goal-4/witness-region-ledger.jsonl"
        rows = path.read_bytes().splitlines(keepends=True)
        row = json.loads(rows[0])
        row["repair_authorized"] = True
        row["witness_region_ids"] = ["FAKE-WITNESS-REGION-0001"]
        rows[0] = pipeline.canonical_json_bytes(row)
        path.write_bytes(b"".join(rows))
        with self.assertRaisesRegex(
            overlay_registry.RegistryError, "locked (?:byte-size|artifact) drift"
        ):
            overlay_registry.load_frozen_overlay_state(root)

    def test_fake_review_ledger_is_loaded_and_rejected(self) -> None:
        temporary = clone_registry_root()
        self.addCleanup(temporary.cleanup)
        root = temporary.repo_root  # type: ignore[attr-defined]
        path = root / overlay_registry.REVIEW_LEDGER_PATH
        path.write_bytes(pipeline.canonical_json_bytes({"review_id": "FAKE-REVIEW"}))
        with self.assertRaisesRegex(
            overlay_registry.RegistryError, "dynamic repair/review registry is invalid"
        ):
            overlay_registry.load_frozen_overlay_state(root)

    def test_fake_repair_ledger_is_loaded_and_rejected(self) -> None:
        temporary = clone_registry_root()
        self.addCleanup(temporary.cleanup)
        root = temporary.repo_root  # type: ignore[attr-defined]
        path = root / overlay_registry.REPAIR_LEDGER_PATH
        path.write_bytes(pipeline.canonical_json_bytes({"repair_id": "FAKE-REPAIR"}))
        with self.assertRaisesRegex(
            overlay_registry.RegistryError, "dynamic repair/review registry is invalid"
        ):
            overlay_registry.load_frozen_overlay_state(root)


if __name__ == "__main__":
    unittest.main()
