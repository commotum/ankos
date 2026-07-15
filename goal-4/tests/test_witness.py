from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "goal-4/tools"
sys.path.insert(0, str(TOOLS))

from witness_lib import (  # noqa: E402
    WitnessError,
    load_json,
    load_jsonl,
    scan_for_forbidden_witness_payloads,
    validate_all,
    validate_contract,
    validate_external_lock_root,
    validate_lock,
    validate_registry,
    validate_region_ledger,
    validate_state,
    validate_unresolved_ledger,
)


class WitnessContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = load_json(ROOT / "goal-4/witness-contract.json")
        cls.registry = load_json(ROOT / "goal-4/witness-source-registry.json")
        cls.state = load_json(ROOT / "goal-4/witness-state.json")
        cls.region_rows = load_jsonl(ROOT / "goal-4/witness-region-ledger.jsonl")
        cls.unresolved_rows = load_jsonl(ROOT / "goal-4/witness-unresolved.jsonl")
        cls.lock = load_json(ROOT / "goal-4/witness-lock.json")

    def test_current_source_blocked_state_validates(self) -> None:
        result = validate_all(ROOT)
        self.assertEqual(result["status"], "SOURCE_BLOCKED")
        self.assertEqual(result["blocked_raw_blocks"], 20430)

    def test_contract_cannot_claim_a_completed_witness(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["status"] = "COMPLETE"
        with self.assertRaisesRegex(WitnessError, "contract status"):
            validate_contract(contract, ROOT)

    def test_stage_gate_cannot_allow_source_blocked_text_changes(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["stage_gates"]["stage_3_source_blocked_allows_author_text_correction"] = True
        with self.assertRaisesRegex(WitnessError, "text correction"):
            validate_contract(contract, ROOT)

    def test_not_applicable_reasons_cannot_expand_to_illegibility(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["not_applicable_reasons"].append("ILLEGIBLE_AUTHOR_TEXT")
        with self.assertRaisesRegex(WitnessError, "not-applicable"):
            validate_contract(contract, ROOT)

    def test_legibility_axis_cannot_be_removed(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["legibility_axes"].remove("INDEX_ENTRY_AND_COLUMN")
        with self.assertRaisesRegex(WitnessError, "legibility axes"):
            validate_contract(contract, ROOT)

    def test_baseline_binding_cannot_drift(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["baseline_bindings"]["structure_ledger_sha256"] = "0" * 64
        with self.assertRaisesRegex(WitnessError, "binding values"):
            validate_contract(contract, ROOT)

    def test_official_source_must_remain_remote_only(self) -> None:
        registry = copy.deepcopy(self.registry)
        registry["sources"][0]["source_state"] = "LOCAL_READ_ONLY_MOUNT"
        with self.assertRaisesRegex(WitnessError, "access state"):
            validate_registry(registry)

    def test_bulk_and_ai_use_cannot_be_implicitly_authorized(self) -> None:
        registry = copy.deepcopy(self.registry)
        registry["sources"][0]["automated_or_ai_use_state"] = "AUTHORIZED"
        with self.assertRaisesRegex(WitnessError, "AI use"):
            validate_registry(registry)
        registry = copy.deepcopy(self.registry)
        registry["sources"][0]["bulk_acquisition_state"] = "AUTHORIZED"
        with self.assertRaisesRegex(WitnessError, "bulk use"):
            validate_registry(registry)

    def test_public_url_cannot_redirect_policy_to_an_unapproved_host(self) -> None:
        registry = copy.deepcopy(self.registry)
        registry["sources"][0]["permission_records"][2]["url"] = "https://example.com/terms"
        with self.assertRaisesRegex(WitnessError, "unapproved host"):
            validate_registry(registry)

    def test_count_conflict_cannot_be_normalized_away(self) -> None:
        registry = copy.deepcopy(self.registry)
        registry["official_count_claims"][2]["count"] = 1280
        with self.assertRaisesRegex(WitnessError, "normalized"):
            validate_registry(registry)
        registry = copy.deepcopy(self.registry)
        registry["count_reconciliation_state"] = "RESOLVED_1280"
        with self.assertRaisesRegex(WitnessError, "falsely resolved"):
            validate_registry(registry)

    def test_unretained_terms_cannot_claim_a_snapshot_hash(self) -> None:
        registry = copy.deepcopy(self.registry)
        registry["sources"][0]["permission_records"][0]["snapshot_sha256"] = "a" * 64
        with self.assertRaisesRegex(WitnessError, "unretained"):
            validate_registry(registry)

    def test_source_blocked_state_cannot_claim_acquisition(self) -> None:
        state = copy.deepcopy(self.state)
        state["acquisition"]["primary_witness_acquired"] = True
        with self.assertRaisesRegex(WitnessError, "falsely enabled"):
            validate_state(state, self.registry, ROOT)

    def test_source_blocked_state_cannot_record_a_mount_path(self) -> None:
        state = copy.deepcopy(self.state)
        state["acquisition"]["unit_manifest_path"] = "/home/user/private/witness.json"
        with self.assertRaisesRegex(WitnessError, "must be null"):
            validate_state(state, self.registry, ROOT)

    def test_every_segment_must_remain_explicitly_blocked(self) -> None:
        state = copy.deepcopy(self.state)
        state["blocked_segment_ids"].remove("INDEX")
        state["coverage"]["blocked_segment_count"] = 28
        with self.assertRaisesRegex(WitnessError, "blocked segment IDs"):
            validate_state(state, self.registry, ROOT)

    def test_blocked_raw_universe_is_bound(self) -> None:
        state = copy.deepcopy(self.state)
        state["coverage"]["raw_block_count"] -= 1
        with self.assertRaisesRegex(WitnessError, "raw block count"):
            validate_state(state, self.registry, ROOT)
        state = copy.deepcopy(self.state)
        state["coverage"]["raw_block_ids_lf_sha256"] = "f" * 64
        with self.assertRaisesRegex(WitnessError, "raw block universe hash"):
            validate_state(state, self.registry, ROOT)

    def test_held_out_universe_is_bound(self) -> None:
        state = copy.deepcopy(self.state)
        state["coverage"]["held_out_selected_count"] = 1124
        with self.assertRaisesRegex(WitnessError, "held-out count"):
            validate_state(state, self.registry, ROOT)
        state = copy.deepcopy(self.state)
        state["coverage"]["held_out_selected_raw_block_ids_sha256"] = "e" * 64
        with self.assertRaisesRegex(WitnessError, "held-out hash"):
            validate_state(state, self.registry, ROOT)

    def test_no_source_blocker_can_be_silently_closed(self) -> None:
        state = copy.deepcopy(self.state)
        state["blockers"][0]["state"] = "CLOSED"
        with self.assertRaisesRegex(WitnessError, "falsely closed"):
            validate_state(state, self.registry, ROOT)

    def test_segment_gap_ledger_covers_exactly_29_documents(self) -> None:
        rows = copy.deepcopy(self.region_rows)
        rows.pop()
        with self.assertRaisesRegex(WitnessError, "row count"):
            validate_region_ledger(ROOT, rows)

    def test_index_layout_blocker_cannot_be_removed(self) -> None:
        rows = copy.deepcopy(self.region_rows)
        index = next(row for row in rows if row["segment_id"] == "INDEX")
        index["blocker_ids"].remove("WITNESS-INDEX-LAYOUT")
        with self.assertRaisesRegex(WitnessError, "blockers drift"):
            validate_region_ledger(ROOT, rows)

    def test_visual_gap_dimension_cannot_be_removed(self) -> None:
        rows = copy.deepcopy(self.region_rows)
        visual = next(row for row in rows if "FIGURE_CAPTION_AND_COLOR" in row["required_risk_dimensions"])
        visual["required_risk_dimensions"].remove("FIGURE_CAPTION_AND_COLOR")
        with self.assertRaisesRegex(WitnessError, "risk dimensions"):
            validate_region_ledger(ROOT, rows)

    def test_gap_cannot_claim_a_phantom_region_or_authorized_repair(self) -> None:
        rows = copy.deepcopy(self.region_rows)
        rows[0]["witness_region_ids"] = ["PHANTOM-REGION"]
        with self.assertRaisesRegex(WitnessError, "phantom witness region"):
            validate_region_ledger(ROOT, rows)
        rows = copy.deepcopy(self.region_rows)
        rows[0]["repair_authorized"] = True
        with self.assertRaisesRegex(WitnessError, "unauthorized witness repair"):
            validate_region_ledger(ROOT, rows)

    def test_gap_row_cannot_leak_a_proposed_answer(self) -> None:
        rows = copy.deepcopy(self.region_rows)
        rows[0]["proposed_repair"] = "guess"
        with self.assertRaisesRegex(WitnessError, "schema drift"):
            validate_region_ledger(ROOT, rows)

    def test_unresolved_source_item_cannot_receive_a_final_disposition(self) -> None:
        rows = copy.deepcopy(self.unresolved_rows)
        rows[0]["final_disposition"] = "APPLIED_WITNESS_VERIFIED"
        with self.assertRaisesRegex(WitnessError, "has a disposition"):
            validate_unresolved_ledger(ROOT, rows)

    def test_unresolved_ledger_cannot_leak_held_out_answers(self) -> None:
        rows = copy.deepcopy(self.unresolved_rows)
        rows[0]["witness_transcription"] = "answer"
        with self.assertRaisesRegex(WitnessError, "leakage"):
            validate_unresolved_ledger(ROOT, rows)

    def test_internal_lock_inventory_and_hashes_are_enforced(self) -> None:
        lock = copy.deepcopy(self.lock)
        lock["artifacts"].pop()
        with self.assertRaisesRegex(WitnessError, "inventory"):
            validate_lock(ROOT, lock)
        lock = copy.deepcopy(self.lock)
        lock["artifacts"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(WitnessError, "artifact hash drift"):
            validate_lock(ROOT, lock)

    def test_external_lock_root_rejects_a_self_consistent_repin(self) -> None:
        with self.assertRaisesRegex(WitnessError, "external witness lock root"):
            validate_external_lock_root(ROOT, "0" * 64)

    def test_stage_4_can_proceed_but_full_claim_stays_blocked(self) -> None:
        state = copy.deepcopy(self.state)
        state["stage_gates"]["full_repair_claim"] = "ALLOWED"
        with self.assertRaisesRegex(WitnessError, "stage gates"):
            validate_state(state, self.registry, ROOT)
        state = copy.deepcopy(self.state)
        state["stage_gates"]["stage_4_dependency_independent_pipeline_work"] = "BLOCKED"
        with self.assertRaisesRegex(WitnessError, "stage gates"):
            validate_state(state, self.registry, ROOT)

    def test_private_paths_cannot_enter_registry(self) -> None:
        registry = copy.deepcopy(self.registry)
        registry["sources"][0]["mount_path"] = "/home/user/witness"
        with self.assertRaisesRegex(WitnessError, "private mount"):
            validate_registry(registry)

    def test_witness_like_binary_payloads_are_rejected_by_extension_and_magic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            goal = Path(temporary)
            (goal / "page.pdf").write_text("metadata only", encoding="utf-8")
            with self.assertRaisesRegex(WitnessError, "extension"):
                scan_for_forbidden_witness_payloads(goal)
        with tempfile.TemporaryDirectory() as temporary:
            goal = Path(temporary)
            (goal / "disguised.bin").write_bytes(b"%PDF-1.7\n")
            with self.assertRaisesRegex(WitnessError, "magic"):
                scan_for_forbidden_witness_payloads(goal)

    def test_symlinked_payloads_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            goal = Path(temporary)
            target = goal / "metadata.txt"
            target.write_text("safe", encoding="utf-8")
            (goal / "alias.txt").symlink_to(target)
            with self.assertRaisesRegex(WitnessError, "symlink"):
                scan_for_forbidden_witness_payloads(goal)


if __name__ == "__main__":
    unittest.main()
