#!/usr/bin/env python3
"""Normal and mutation tests for the Stage 4 schema package."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "goal-4" / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import pipeline_schema_lib as lib  # noqa: E402
import overlay_lib  # noqa: E402
import validate_pipeline_schemas as schema_cli  # noqa: E402


ZERO = "0" * 64
EMPTY_SHA = hashlib.sha256(b"").hexdigest()
VIEW_SHA = hashlib.sha256(b"independent-evidence-view").hexdigest()
MONOLITH_PATH = ROOT / "ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md"
MONOLITH_BYTES = MONOLITH_PATH.read_bytes()
GUARD_BYTES = MONOLITH_BYTES[:39]
GUARD_TEXT = GUARD_BYTES.decode("utf-8")
GUARD_SHA = hashlib.sha256(GUARD_BYTES).hexdigest()


def projection(text: str) -> dict[str, str]:
    return {"sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "text": text}


def payload_hash(payload: object) -> str:
    return hashlib.sha256(lib.canonical_json_bytes(payload)[:-1]).hexdigest()


def closed_workflow(disposition: str = "APPLIED_MECHANICALLY_PROVEN") -> dict[str, object]:
    return {
        "events": [
            {"evidence_ids": [], "from_state": None, "principal_id": "creator", "reason_code": "CAPTURE", "sequence": 0, "session_id": "session", "to_state": "CAPTURED"},
            {"evidence_ids": ["EVIDENCE-1"], "from_state": "CAPTURED", "principal_id": "creator", "reason_code": "PROOF", "sequence": 1, "session_id": "session", "to_state": "EVIDENCE_READY"},
            {"evidence_ids": ["EVIDENCE-1"], "from_state": "EVIDENCE_READY", "principal_id": "creator", "reason_code": "CLOSE", "sequence": 2, "session_id": "session", "to_state": "CLOSED"},
        ],
        "final_disposition": disposition,
        "owner_stage": "4-PIPELINE",
        "required_review_roles": [],
        "state": "CLOSED",
        "unresolved_ids": [],
    }


def blocked_workflow(unresolved: str = "UNRESOLVED-WITNESS-0001") -> dict[str, object]:
    return {
        "events": [
            {"evidence_ids": [], "from_state": None, "principal_id": "creator", "reason_code": "CAPTURE", "sequence": 0, "session_id": "session", "to_state": "CAPTURED"},
            {"evidence_ids": [], "from_state": "CAPTURED", "principal_id": "creator", "reason_code": "SOURCE-GAP", "sequence": 1, "session_id": "session", "to_state": "SOURCE_BLOCKED"},
        ],
        "final_disposition": None,
        "owner_stage": "4-PIPELINE",
        "required_review_roles": [],
        "state": "SOURCE_BLOCKED",
        "unresolved_ids": [unresolved],
    }


def operation(kind: str, before: str, after: str, *, inverse: bool = False) -> dict[str, object]:
    if kind != "MOVE":
        raise ValueError("test fixture currently uses MOVE operations")
    fields = {
        "block_id": "RAW-000001",
        "destination_left_id": None,
        "destination_right_id": "RAW-000002" if inverse else "RAW-000003",
        "expected_block_sha256": GUARD_SHA,
        "expected_destination_adjacency_count": 1,
        "expected_source_adjacency_count": 1,
        "operation_type": "MOVE",
        "source_left_id": None,
        "source_right_id": "RAW-000003" if inverse else "RAW-000002",
    }
    payload = {
        "operation_fields": fields,
        "source_node_ids": ["NODE-1"],
        "target_node_ids": ["NODE-1"],
    }
    return {
        "expected_input_projection_sha256": projection(before)["sha256"],
        "expected_output_projection_sha256": projection(after)["sha256"],
        "operation_type": kind,
        "payload": payload,
        "payload_sha256": payload_hash(payload),
    }


def valid_repair() -> dict[str, object]:
    row: dict[str, object] = {
        "after_projection": projection("x"),
        "application_order": 0,
        "baseline_lock_sha256": lib.sha256_file(ROOT / "goal-4/baseline-lock.json"),
        "before_projection": projection("x"),
        "confidence": "HIGH",
        "creator": {"principal_id": "creator", "principal_type": "AGENT", "session_id": "session"},
        "dependencies": [],
        "evidence": {
            "after_view_sha256": None,
            "authoritative": [],
            "before_view_sha256": None,
            "diagnostic": [],
            "mechanical": [
                {
                    "evidence_id": "EVIDENCE-1",
                    "evidence_kind": "MECHANICAL_PROOF",
                    "evidence_sha256": EMPTY_SHA,
                    "mechanical_proof_id": "IDENTITY_AUTHOR_PROJECTION_V1",
                    "permission_record_id": None,
                    "witness_region_ids": [],
                }
            ],
            "witness_view_sha256": None,
        },
        "forward_operation": operation("MOVE", "x", "x"),
        "guard": {
            "expected_occurrence_count": 1,
            "guard_kind": "PREIMAGE",
            "preimage": GUARD_TEXT,
            "preimage_sha256": GUARD_SHA,
            "raw_block_ids": ["RAW-000001"],
            "raw_source_path": "ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md",
            "raw_source_sha256": hashlib.sha256(MONOLITH_BYTES).hexdigest(),
            "span": {"end_byte_exclusive": len(GUARD_BYTES), "sha256": GUARD_SHA, "start_byte": 0},
        },
        "inverse_operation": operation("MOVE", "x", "x", inverse=True),
        "operation_projection_sha256": VIEW_SHA,
        "rationale": "Synthetic byte-preserving metadata operation.",
        "repair_class": "NAVIGATION_METADATA",
        "repair_id": "REPAIR-TEST-0001",
        "review_ids": [],
        "risk": {"ast_impact_tags": [], "class_tags": ["NAVIGATION_METADATA"], "high_risk": False, "operation_tags": [], "severity_id": "S3_REQUIRED_RELEASE_MECHANICS_ERROR"},
        "schema_version": "1.0.0",
        "target": {"canonical_document_id": None, "node_ids": ["NODE-1"], "path": "DERIVED/Contents.md", "role": "GENERATED_METADATA"},
        "target_state_guards": {"after_sha256": VIEW_SHA, "before_sha256": VIEW_SHA},
        "unresolved_ids": [],
        "verification_results": [],
        "witness_projection": None,
        "workflow": closed_workflow(),
    }
    row["guard"]["expected_occurrence_count"] = MONOLITH_BYTES.count(GUARD_BYTES)
    row["evidence"]["mechanical"][0]["evidence_sha256"] = lib.mechanical_proof_sha256(row)
    row["verification_results"] = [
        {
            "check_id": check_id,
            "details_sha256": lib.mechanical_check_sha256(row, check_id),
            "passed": True,
        }
        for check_id in lib.MECHANICAL_CHECK_IDS
    ]
    return row


def valid_overlay_binding(registry):
    row = valid_repair()
    row["repair_class"] = "PROSE_OCR"
    row["risk"]["class_tags"] = ["PROSE_OCR"]
    row["target"] = {
        "canonical_document_id": "PUBLICATION_AND_CONTENTS",
        "node_ids": ["NODE-1"],
        "path": "CANONICAL/FRONT-MATTER/00-Publication-and-Contents.md",
        "role": "CANONICAL_AUTHOR_TEXT",
    }
    raw_row = lib._frozen_indexes(registry)["blocks_by_id"]["RAW-000001"]
    meta = overlay_lib.OperationMeta(
        repair_id=row["repair_id"],
        target_id="PUBLICATION_AND_CONTENTS",
        target_path=row["target"]["path"],
        raw_source_id="RAW-000001",
        raw_source_span_sha256=GUARD_SHA,
        raw_source_row_sha256=hashlib.sha256(lib.canonical_json_bytes(raw_row)).hexdigest(),
        target_role="CANONICAL_AUTHOR_TEXT",
        repair_class="PROSE_OCR",
        expected_target_sha256=row["target_state_guards"]["before_sha256"],
        expected_result_sha256=row["target_state_guards"]["after_sha256"],
        creator_principal_id="creator",
        workflow_state="CLOSED",
        final_disposition="APPLIED_MECHANICALLY_PROVEN",
    )
    operation_row = overlay_lib.Move(
        meta=meta,
        block_id="RAW-000001",
        expected_block_sha256=raw_row["raw_sha256"],
        source_left_id=None,
        source_right_id="RAW-000002",
        destination_left_id=None,
        destination_right_id="RAW-000003",
        expected_source_adjacency_count=1,
        expected_destination_adjacency_count=1,
    )
    row["operation_projection_sha256"] = overlay_lib.operation_projection_sha256(operation_row)
    return row, operation_row


def endpoint(kind: str, projection_sha: str, *, role: str | None, path: str | None) -> dict[str, object]:
    span = None if kind in {"GENERATED_NONE", "TYPED_EXCLUSION"} else {"end_byte_exclusive": 1, "sha256": ZERO, "start_byte": 0}
    return {
        "author_text_projection_sha256": projection_sha,
        "canonical_document_id": None,
        "endpoint_kind": kind,
        "path": path,
        "raw_block_ids": [],
        "role": role,
        "span": span,
        "witness_region_ids": [],
    }


def valid_generated_provenance() -> dict[str, object]:
    return {
        "author_text_projection_sha256": EMPTY_SHA,
        "inverse": {"inverse_kind": "REMOVE_GENERATED", "repair_ids": []},
        "mapping_kind": "GENERATED_METADATA",
        "node_ids": ["NODE-1"],
        "provenance_id": "PROVENANCE-1",
        "repair_ids": [],
        "schema_version": "1.0.0",
        "sequence": 0,
        "source": endpoint("GENERATED_NONE", EMPTY_SHA, role=None, path=None),
        "target": endpoint("GENERATED_SPAN", EMPTY_SHA, role="GENERATED_METADATA", path="DERIVED/Contents.md"),
    }


def valid_ast_node(
    node_id: str,
    *,
    document_id: str = "PUBLICATION_AND_CONTENTS",
    output_path: str = "CANONICAL/FRONT-MATTER/00-Publication-and-Contents.md",
    data: bytes = GUARD_BYTES,
    raw_block_ids: list[str] | None = None,
    anchor_id: str | None = None,
    node_type: str | None = None,
    destination: str | None = None,
    link_kind: str | None = None,
) -> dict[str, object]:
    text = data.decode("utf-8")
    fields = {"text": text}
    if anchor_id is not None:
        fields["anchor_id"] = anchor_id
    if destination is not None:
        fields["destination"] = destination
    if link_kind is not None:
        fields["link_kind"] = link_kind
    return {
        "author_text_projection": text,
        "author_text_projection_sha256": hashlib.sha256(data).hexdigest(),
        "canonical_document_id": document_id,
        "content_role": "CANONICAL_AUTHOR_TEXT",
        "fields": fields,
        "node_id": node_id,
        "node_type": node_type or ("GENERATED_ANCHOR" if anchor_id is not None else "TEXT"),
        "ordinal": 0,
        "output_path": output_path,
        "output_span": {"end_byte_exclusive": len(data), "sha256": hashlib.sha256(data).hexdigest(), "start_byte": 0},
        "parent_node_id": None,
        "raw_span_ids": ["RAW-000001"] if raw_block_ids is None else raw_block_ids,
        "schema_version": "1.0.0",
        "witness_region_ids": [],
    }


def valid_raw_provenance() -> dict[str, object]:
    source = {
        "author_text_projection_sha256": GUARD_SHA,
        "canonical_document_id": "PUBLICATION_AND_CONTENTS",
        "endpoint_kind": "RAW_SPAN",
        "path": "ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md",
        "raw_block_ids": ["RAW-000001"],
        "role": "CANONICAL_AUTHOR_TEXT",
        "span": {"end_byte_exclusive": len(GUARD_BYTES), "sha256": GUARD_SHA, "start_byte": 0},
        "witness_region_ids": [],
    }
    target = {
        "author_text_projection_sha256": GUARD_SHA,
        "canonical_document_id": "PUBLICATION_AND_CONTENTS",
        "endpoint_kind": "CANONICAL_SPAN",
        "path": "CANONICAL/FRONT-MATTER/00-Publication-and-Contents.md",
        "raw_block_ids": ["RAW-000001"],
        "role": "CANONICAL_AUTHOR_TEXT",
        "span": {"end_byte_exclusive": len(GUARD_BYTES), "sha256": GUARD_SHA, "start_byte": 0},
        "witness_region_ids": [],
    }
    return {
        "author_text_projection_sha256": GUARD_SHA,
        "inverse": {"inverse_kind": "IDENTITY", "repair_ids": []},
        "mapping_kind": "RAW_PRESERVED",
        "node_ids": ["NODE-RAW-1"],
        "provenance_id": "PROVENANCE-RAW-1",
        "repair_ids": [],
        "schema_version": "1.0.0",
        "sequence": 0,
        "source": source,
        "target": target,
    }


def closed_review(
    review_id: str,
    *,
    role: str = "SOURCE_REVIEWER",
    principal: str = "reviewer",
    subject_id: str = "REPAIR-TEST-0001",
) -> dict[str, object]:
    row = valid_review()
    row.update(
        {
            "closure_state": "CLOSED",
            "principal_id": principal,
            "repair_id": subject_id,
            "review_id": review_id,
            "reviewer_role": role,
            "subject_id": subject_id,
            "subject_type": "REPAIR",
        }
    )
    return row


def valid_navigation() -> dict[str, object]:
    return {
        "anchor_id": "ankos-ch01-raw-h-000001",
        "author_text_projection_sha256": EMPTY_SHA,
        "destination_anchor_id": None,
        "destination_asset_id": None,
        "destination_path": None,
        "generated": True,
        "link_kind": "NONE",
        "navigation_id": "NAVIGATION-1",
        "printed_page_label": None,
        "raw_block_id": "RAW-000001",
        "raw_line_span": {"end_line": 1, "start_line": 1},
        "record_type": "ANCHOR",
        "resolution_state": "RESOLVED",
        "schema_version": "1.0.0",
        "sequence": 0,
        "source_document_id": "PUBLICATION_AND_CONTENTS",
        "source_node_id": "NODE-NAV-1",
        "source_path": "CANONICAL/FRONT-MATTER/00-Publication-and-Contents.md",
        "unresolved_ids": [],
        "witness_unit_id": None,
        "workflow": closed_workflow("APPLIED_MECHANICALLY_PROVEN"),
    }


def valid_figure() -> dict[str, object]:
    baseline = lib.load_json(ROOT / "goal-4/corpus-manifest.json", require_cj1=True)
    asset = next(row for row in baseline["raw_inputs"] if row["kind"] == "JPEG")
    return {
        "alt_text_sidecar_id": None,
        "asset_id": "ASSET-1",
        "asset_role": "GOVERNED_LEGACY_ASSET",
        "asset_sha256": asset["sha256"],
        "association_state": "SOURCE_BLOCKED",
        "byte_size": asset["byte_size"],
        "canonical_document_id": "COLOPHON",
        "caption_ownership_evidence_sha256": None,
        "caption_projection_sha256": None,
        "caption_span": None,
        "completeness_state": "UNKNOWN_SOURCE_BLOCKED",
        "component_order_evidence_sha256": None,
        "dimensions": {"height": asset["image"]["height"], "width": asset["image"]["width"]},
        "figure_group_id": None,
        "grouping_evidence_sha256": None,
        "legacy_reference_ordinals": [1],
        "license_record_id": None,
        "manifest_file_id": asset["file_id"],
        "ordered_component_asset_ids": [],
        "printed_group_ids": [],
        "raw_block_ids": ["RAW-000001"],
        "record_id": "FIGURE-1",
        "record_type": "ASSET_CANDIDATE",
        "redistribution_allowed": None,
        "release_path": f"ASSETS/LEGACY/{asset['relative_path']}",
        "repair_ids": [],
        "review_ids": [],
        "scale_orientation_color_significance": None,
        "schema_version": "1.0.0",
        "unresolved_ids": ["UNRESOLVED-WITNESS-0001"],
        "witness_region_ids": [],
        "witness_unit_id": None,
        "workflow": blocked_workflow(),
    }


def valid_review() -> dict[str, object]:
    return {
        "adjudicator_review_id": None,
        "agreement_state": "AGREES",
        "blind_preproposal": False,
        "candidate_visible": True,
        "closure_state": "OPEN",
        "decision_kind": "STRUCTURE",
        "decision_payload": "synthetic",
        "decision_sha256": projection("synthetic")["sha256"],
        "disagrees_with_review_ids": [],
        "evidence_view_id": "EVIDENCE-1",
        "evidence_view_sha256": VIEW_SHA,
        "follow_up": None,
        "principal_id": "agent",
        "proposal_visible": False,
        "raw_block_ids": ["RAW-000001"],
        "raw_visible": True,
        "repair_id": None,
        "review_id": "REVIEW-1",
        "reviewed_at": None,
        "reviewer_role": "SPECIALIST_REVIEWER",
        "reviewer_type": "AGENT",
        "schema_version": "1.0.0",
        "session_id": "session",
        "specialty": "STRUCTURE",
        "subject_id": "RAW-000001",
        "subject_type": "RAW_BLOCK",
        "view_locator": {"geometry": None, "witness_region_id": None, "witness_unit_id": None},
        "witness_region_ids": [],
    }


def valid_unresolved() -> dict[str, object]:
    return {
        "affected": {"asset_ids": [], "figure_group_ids": [], "navigation_ids": [], "node_ids": [], "raw_block_ids": [], "repair_ids": [], "review_ids": [], "segment_ids": ["CH01"], "technical_span_ids": [], "witness_region_ids": []},
        "attempted_alternatives": [],
        "category": "SOURCE",
        "dependency_ids": [],
        "evidence_ids": [],
        "final_disposition": None,
        "impact": "Synthetic source gap.",
        "kind": "SOURCE-GAP",
        "owner_stage": "3-WITNESSES",
        "release_blocker_codes": ["WITNESS-IDENTITY-GAP"],
        "repair_authorized": False,
        "resolution": None,
        "schema_version": "1.0.0",
        "severity_id": "S0_SOURCE_OR_COVERAGE_BLOCKER",
        "source_candidate_ids": [],
        "unblock_actions": ["Acquire an authorized witness."],
        "unresolved_id": "UNRESOLVED-TEST-1",
        "workflow_state": "SOURCE_BLOCKED",
    }


def valid_compatibility() -> dict[str, object]:
    baseline = lib.load_json(ROOT / "goal-4/compatibility-baseline.json", require_cj1=True)
    results = [
        {
            "argv": row["argv"],
            "baseline_framed_behavior_sha256": row["framed_behavior_sha256"],
            "current_framed_behavior_sha256": row["framed_behavior_sha256"],
            "exit_code": row["exit_code"],
            "identical": True,
            "path": row["path"],
            "status_kind": row["status_kind"],
            "stderr_sha256": row["stderr"]["sha256"],
            "stdout_sha256": row["stdout"]["sha256"],
        }
        for row in baseline["oracles"]
    ]
    return {
        "aggregate_behavior_digest": baseline["behavior_digest"],
        "all_identical": True,
        "baseline_behavior_digest": baseline["behavior_digest"],
        "baseline_path": "goal-4/compatibility-baseline.json",
        "baseline_sha256": lib.sha256_file(ROOT / "goal-4/compatibility-baseline.json"),
        "contract_id": "ANKOS-COMPATIBILITY-VERIFY-1",
        "dependency_fingerprint": baseline["closure"]["dependency_fingerprint_after"],
        "legacy_tree_digest": baseline["closure"]["legacy_tree_digest_after"],
        "oracle_results": results,
        "phase": "ZERO_REPAIR_STAGING",
        "schema_version": "1.0.0",
        "sentinel_fixture_results": {"duplicate_basename_detected": True, "nested_markdown_detected": True},
        "sibling_state": "EMPTY",
    }


def receipt_hash(row: dict[str, object]) -> str:
    payload = {key: value for key, value in row.items() if key != "receipt_sha256"}
    return hashlib.sha256(lib.canonical_json_bytes(payload)[:-1]).hexdigest()


def valid_compatibility_observation(record: dict[str, object]) -> dict[str, object]:
    oracle_receipts = []
    for evidence in record["oracle_results"]:
        execution = valid_execution_receipt(
            receipt_id=f"EXEC-{len(oracle_receipts):04d}",
            command=[sys.executable, "goal-4/tools/capture_compatibility.py"],
            tool_path="goal-4/tools/capture_compatibility.py",
            status_kind=evidence["status_kind"],
            exit_code=evidence["exit_code"],
            stdout_sha256=evidence["stdout_sha256"],
            stderr_sha256=evidence["stderr_sha256"],
        )
        row = {
            "argv": evidence["argv"],
            "execution_receipt": execution,
            "framed_behavior_sha256": evidence["current_framed_behavior_sha256"],
            "oracle_result_sha256": hashlib.sha256(lib.canonical_json_bytes(evidence)).hexdigest(),
            "path": evidence["path"],
            "receipt_sha256": ZERO,
        }
        row["receipt_sha256"] = receipt_hash(row)
        oracle_receipts.append(row)
    receipt = {
        "aggregate_behavior_digest": record["aggregate_behavior_digest"],
        "compatibility_record_sha256": hashlib.sha256(lib.canonical_json_bytes(record)).hexdigest(),
        "contract_id": "ANKOS-COMPATIBILITY-OBSERVATION-1",
        "dependency_fingerprint": record["dependency_fingerprint"],
        "execution_environment_sha256": VIEW_SHA,
        "legacy_tree_digest": record["legacy_tree_digest"],
        "observation_id": "COMPATIBILITY-OBSERVATION-1",
        "observed_at": "2026-07-14T12:00:02Z",
        "oracle_receipts": oracle_receipts,
        "receipt_sha256": ZERO,
        "runner_principal_id": "runner",
        "runner_session_id": "runner-session",
        "schema_version": "1.0.0",
        "sentinel_fixture_results_sha256": hashlib.sha256(
            lib.canonical_json_bytes(record["sentinel_fixture_results"])[:-1]
        ).hexdigest(),
    }
    receipt["receipt_sha256"] = receipt_hash(receipt)
    return receipt


def valid_execution_receipt(
    *,
    receipt_id: str = "EXECUTION-1",
    command: list[str] | None = None,
    tool_path: str = "goal-4/tools/capture_compatibility.py",
    status_kind: str = "EXITED",
    exit_code: int | None = 0,
    stdout_sha256: str = EMPTY_SHA,
    stderr_sha256: str = EMPTY_SHA,
) -> dict[str, object]:
    command = [sys.executable, tool_path] if command is None else command
    row = {
        "command": command,
        "command_sha256": hashlib.sha256(lib.canonical_json_bytes(command)[:-1]).hexdigest(),
        "contract_id": "ANKOS-EXECUTION-RECEIPT-1",
        "executed_tool_path": tool_path,
        "executed_tool_sha256": lib.sha256_file(ROOT / tool_path),
        "execution_kind": "EXECUTED",
        "exit_code": exit_code,
        "finished_at": "2026-07-14T12:00:01Z",
        "not_executed_reason": None,
        "receipt_id": receipt_id,
        "receipt_sha256": ZERO,
        "runner_path": "goal-4/tools/execution_receipt_runner.py",
        "runner_sha256": lib.sha256_file(ROOT / "goal-4/tools/execution_receipt_runner.py"),
        "schema_version": "1.0.0",
        "started_at": "2026-07-14T12:00:00Z",
        "status_kind": status_kind,
        "stderr_byte_size": 0,
        "stderr_sha256": stderr_sha256,
        "stdout_byte_size": 0,
        "stdout_sha256": stdout_sha256,
    }
    row["receipt_sha256"] = receipt_hash(row)
    return row


def valid_corpus_manifest() -> dict[str, object]:
    guardrails = lib.load_json(ROOT / "goal-4/guardrails.json", require_cj1=False)
    files = []
    for document in guardrails["canonical_documents"]:
        files.append({"author_text_projection_sha256": ZERO, "byte_size": 0, "canonical_document_id": document["id"], "canonical_order": document["order"], "media_type": "text/markdown", "mode": "0644", "path": document["path"], "role": "CANONICAL_AUTHOR_TEXT", "sha256": ZERO, "source_identity": document["id"]})
    return {
        "asset_counts": {"governed_legacy": 0, "governed_witness": 0},
        "author_text_projection_sha256": ZERO,
        "canonical_document_order": [item["id"] for item in guardrails["canonical_documents"]],
        "certification_state": "UNCERTIFIED",
        "contract_id": "ANKOS-CORPUS-MANIFEST-1",
        "files": files,
        "release_id": "RELEASE-TEST-1",
        "role_counts": {"CANONICAL_AUTHOR_TEXT": 29},
        "schema_version": "1.0.0",
    }


def valid_release_manifest() -> dict[str, object]:
    return {
        "audit_certificate": None,
        "certification_state": "UNCERTIFIED",
        "claim_scope": "ZERO_REPAIR_STRUCTURAL_BUILD",
        "commands": [["python3", "build.py"]],
        "compatibility_observation_receipt_sha256": ZERO,
        "compatibility_verification_sha256": ZERO,
        "contract_bindings": {"pipeline": ZERO},
        "contract_id": "ANKOS-RELEASE-1",
        "input_bindings": {"baseline": ZERO},
        "inverse_replay": {"raw_projection_sha256": ZERO, "receipt_sha256": ZERO},
        "ledger_hashes": {},
        "open_blocker_ids": ["UNRESOLVED-WITNESS-0001"],
        "output_manifest_sha256": ZERO,
        "overlay_hashes": {},
        "prior_release": None,
        "publication": {"atomic_same_filesystem_rename": False, "target_state": "NOT_PUBLISHED"},
        "release_id": "RELEASE-TEST-1",
        "reproducibility_receipt_sha256": ZERO,
        "role_counts": {"CANONICAL_AUTHOR_TEXT": 29},
        "rollback": {"command": [], "receipt_sha256": ZERO},
        "schema_lock_sha256": ZERO,
        "schema_version": "1.0.0",
        "tool_hashes": {},
        "two_clean_build_digests": [ZERO, ZERO],
    }


def valid_technical() -> dict[str, object]:
    return {
        "canonical_document_id": "PUBLICATION_AND_CONTENTS",
        "changed_token_ids": [],
        "node_id": "NODE-TECHNICAL-1",
        "output_span": {
            "end_byte_exclusive": len(GUARD_BYTES),
            "sha256": GUARD_SHA,
            "start_byte": 0,
        },
        "output_path": "CANONICAL/FRONT-MATTER/00-Publication-and-Contents.md",
        "parse_check": "SOURCE_BLOCKED",
        "program_count_classification": "NOT_APPLICABLE",
        "raw_block_ids": ["RAW-000001"],
        "raw_span": {
            "end_byte_exclusive": len(GUARD_BYTES),
            "sha256": GUARD_SHA,
            "start_byte": 0,
        },
        "render_check": "SOURCE_BLOCKED",
        "repair_ids": [],
        "schema_version": "1.0.0",
        "source_projection": GUARD_TEXT,
        "source_projection_sha256": GUARD_SHA,
        "specialist_review_ids": [],
        "technical_kind": "FORMULA",
        "technical_span_id": "TECHNICAL-SPAN-1",
        "tokens": [
            {
                "changed": False,
                "evidence_ids": [],
                "ordinal": 0,
                "raw_sha256": GUARD_SHA,
                "raw_text": GUARD_TEXT,
                "repaired_text": None,
                "review_ids": [],
                "token_id": "TOKEN-1",
                "token_kind": "RAW-TEXT",
                "witness_text": None,
            }
        ],
        "unresolved_ids": ["UNRESOLVED-WITNESS-0001"],
        "witness_check": "SOURCE_BLOCKED",
        "witness_region_ids": [],
        "workflow": blocked_workflow(),
    }


class PipelineSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract, cls.registry = lib.validate_pipeline_contract(ROOT)

    def expect_failure(self, function, *args, **kwargs) -> None:
        with self.assertRaises(lib.PipelineSchemaError):
            function(*args, **kwargs)

    def test_01_package_contract_and_schemas_pass(self) -> None:
        self.assertEqual(len(self.registry.schemas), 14)
        self.assertEqual(len(self.contract["ledgers"]), 8)

    def test_02_valid_mechanical_repair_passes(self) -> None:
        lib.validate_repair(valid_repair(), self.registry)

    def test_03_unknown_repair_field_fails(self) -> None:
        row = valid_repair()
        row["unknown"] = True
        self.expect_failure(lib.validate_repair, row, self.registry)

    def test_04_missing_required_repair_field_fails(self) -> None:
        row = valid_repair()
        del row["baseline_lock_sha256"]
        self.expect_failure(lib.validate_repair, row, self.registry)

    def test_05_baseline_lock_drift_fails(self) -> None:
        row = valid_repair()
        row["baseline_lock_sha256"] = ZERO
        self.expect_failure(lib.validate_repair, row, self.registry)

    def test_06_preimage_hash_drift_fails(self) -> None:
        row = valid_repair()
        row["guard"]["preimage_sha256"] = ZERO
        self.expect_failure(lib.validate_repair, row, self.registry)

    def test_07_operation_payload_drift_fails(self) -> None:
        row = valid_repair()
        row["forward_operation"]["payload"]["text"] = "changed"
        self.expect_failure(lib.validate_repair, row, self.registry)

    def test_08_inverse_hash_direction_fails(self) -> None:
        row = valid_repair()
        row["inverse_operation"]["expected_output_projection_sha256"] = ZERO
        self.expect_failure(lib.validate_repair, row, self.registry)

    def test_09_nonclosed_final_disposition_fails(self) -> None:
        workflow = blocked_workflow()
        workflow["final_disposition"] = "UNRESOLVED_SOURCE_NEEDED"
        self.expect_failure(lib.validate_workflow, workflow)

    def test_10_closed_without_disposition_fails(self) -> None:
        workflow = closed_workflow()
        workflow["final_disposition"] = None
        self.expect_failure(lib.validate_workflow, workflow)

    def test_11_workflow_event_gap_fails(self) -> None:
        workflow = closed_workflow()
        workflow["events"][1]["sequence"] = 4
        self.expect_failure(lib.validate_workflow, workflow)

    def test_12_source_blocked_without_unresolved_fails(self) -> None:
        workflow = blocked_workflow()
        workflow["unresolved_ids"] = []
        self.expect_failure(lib.validate_workflow, workflow)

    def test_13_high_risk_union_cannot_be_underdeclared(self) -> None:
        row = valid_repair()
        row["risk"]["operation_tags"] = ["AUTHORIAL_STRUCTURE_OR_HIERARCHY_CHANGE"]
        self.expect_failure(lib.validate_repair, row, self.registry)

    def test_14_author_text_change_is_source_blocked(self) -> None:
        row = valid_repair()
        row["repair_class"] = "PROSE_OCR"
        row["risk"]["class_tags"] = ["PROSE_OCR"]
        row["target"] = {"canonical_document_id": "CH01", "node_ids": ["NODE-1"], "path": "CANONICAL/CHAPTERS/01-The-Foundations-for-a-New-Kind-of-Science.md", "role": "CANONICAL_AUTHOR_TEXT"}
        row["after_projection"] = projection("y")
        row["forward_operation"]["expected_output_projection_sha256"] = projection("y")["sha256"]
        row["inverse_operation"]["expected_input_projection_sha256"] = projection("y")["sha256"]
        row["workflow"] = closed_workflow("APPLIED_WITNESS_VERIFIED")
        self.expect_failure(lib.validate_repair, row, self.registry)

    def test_15_authorial_structure_cannot_be_mechanical(self) -> None:
        row = valid_repair()
        row["repair_class"] = "MARKDOWN_STRUCTURE"
        row["risk"]["class_tags"] = ["MARKDOWN_STRUCTURE"]
        row["risk"]["high_risk"] = True
        row["target"] = {"canonical_document_id": "CH01", "node_ids": ["NODE-1"], "path": "CANONICAL/CHAPTERS/01-The-Foundations-for-a-New-Kind-of-Science.md", "role": "CANONICAL_AUTHOR_TEXT"}
        row["review_ids"] = ["REVIEW-1"]
        self.expect_failure(lib.validate_repair, row, self.registry)

    def test_16_annotation_disposition_is_sidecar_only(self) -> None:
        row = valid_repair()
        row["workflow"] = closed_workflow("ANNOTATED_SOURCE_ERRATUM")
        self.expect_failure(lib.validate_repair, row, self.registry)

    def test_17_nonapplied_candidate_cannot_have_application_order(self) -> None:
        row = valid_repair()
        row["workflow"] = closed_workflow("REJECTED_VALID_SOURCE_TEXT")
        self.expect_failure(lib.validate_repair, row, self.registry)

    def test_18_missing_review_foreign_key_fails(self) -> None:
        row = valid_repair()
        row["review_ids"] = ["REVIEW-1"]
        self.expect_failure(lib.validate_repair_set, [row], self.registry)

    def test_19_missing_dependency_foreign_key_fails(self) -> None:
        row = valid_repair()
        row["dependencies"] = ["REPAIR-MISSING"]
        self.expect_failure(lib.validate_repair_set, [row], self.registry)

    def test_20_valid_generated_provenance_passes(self) -> None:
        lib.validate_provenance(valid_generated_provenance(), self.registry)

    def test_21_generated_nonempty_projection_fails(self) -> None:
        row = valid_generated_provenance()
        row["author_text_projection_sha256"] = projection("x")["sha256"]
        self.expect_failure(lib.validate_provenance, row, self.registry)

    def test_22_witness_insert_provenance_is_blocked(self) -> None:
        row = valid_generated_provenance()
        row["mapping_kind"] = "WITNESS_INSERTED"
        self.expect_failure(lib.validate_provenance, row, self.registry)

    def test_23_valid_generated_navigation_passes(self) -> None:
        row = valid_navigation()
        lib.validate_navigation(
            row,
            self.registry,
            ast_nodes=[valid_ast_node("NODE-NAV-1", anchor_id=row["anchor_id"])],
        )

    def test_24_navigation_escape_fails(self) -> None:
        row = valid_navigation()
        row["destination_path"] = "../escape.md"
        self.expect_failure(
            lib.validate_navigation,
            row,
            self.registry,
            ast_nodes=[valid_ast_node("NODE-NAV-1", anchor_id=row["anchor_id"])],
        )

    def test_25_generated_navigation_projection_fails(self) -> None:
        row = valid_navigation()
        row["author_text_projection_sha256"] = projection("x")["sha256"]
        self.expect_failure(
            lib.validate_navigation,
            row,
            self.registry,
            ast_nodes=[valid_ast_node("NODE-NAV-1", anchor_id=row["anchor_id"])],
        )

    def test_26_valid_source_blocked_legacy_figure_passes(self) -> None:
        lib.validate_figure(valid_figure(), self.registry)

    def test_27_witness_asset_release_is_blocked(self) -> None:
        row = valid_figure()
        row["asset_role"] = "GOVERNED_WITNESS_ASSET"
        self.expect_failure(lib.validate_figure, row, self.registry)

    def test_28_verified_figure_without_witness_fails(self) -> None:
        row = valid_figure()
        row["association_state"] = "VERIFIED"
        self.expect_failure(lib.validate_figure, row, self.registry)

    def test_29_valid_agent_review_passes(self) -> None:
        lib.validate_review(valid_review(), self.registry)

    def test_30_blind_reviewer_cannot_see_proposal(self) -> None:
        row = valid_review()
        row["blind_preproposal"] = True
        row["proposal_visible"] = True
        self.expect_failure(lib.validate_review, row, self.registry)

    def test_31_unresolved_disagreement_cannot_close(self) -> None:
        row = valid_review()
        row["agreement_state"] = "DISAGREES"
        row["closure_state"] = "CLOSED"
        self.expect_failure(lib.validate_review, row, self.registry)

    def test_32_human_review_needs_timestamp(self) -> None:
        row = valid_review()
        row["reviewer_type"] = "HUMAN"
        self.expect_failure(lib.validate_review, row, self.registry)

    def test_33_external_lock_pin_rejects_wrong_digest(self) -> None:
        self.expect_failure(lib.validate_lock, ROOT, ZERO)

    def test_34_cj1_rejects_pretty_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pretty.json"
            path.write_text(json.dumps({"b": 1, "a": 2}, indent=2) + "\n", encoding="utf-8")
            with self.assertRaises(lib.PipelineSchemaError):
                lib.load_json(path, require_cj1=True)

    def test_35_schema_unknown_keyword_fails(self) -> None:
        schema = deepcopy(self.registry.schemas["goal-4/schemas/common.schema.json"])
        schema["unsupportedKeyword"] = True
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "common.schema.json"
            target.write_bytes(lib.canonical_json_bytes(schema))
            self.expect_failure(lib.SchemaRegistry, root, ["common.schema.json"])

    def test_36_valid_unresolved_passes(self) -> None:
        lib.validate_unresolved(valid_unresolved(), self.registry)

    def test_37_source_blocked_unresolved_cannot_authorize_repair(self) -> None:
        row = valid_unresolved()
        row["repair_authorized"] = True
        self.expect_failure(lib.validate_unresolved, row, self.registry)

    def test_38_compatibility_baseline_drift_fails(self) -> None:
        row = valid_compatibility()
        row["baseline_sha256"] = ZERO
        self.expect_failure(lib.validate_compatibility, row, self.registry)

    def test_39_corpus_role_count_drift_fails(self) -> None:
        row = valid_corpus_manifest()
        row["role_counts"]["CANONICAL_AUTHOR_TEXT"] = 28
        guardrails = lib.load_json(ROOT / "goal-4/guardrails.json", require_cj1=False)
        self.expect_failure(lib.validate_corpus_manifest, row, self.registry, guardrails)

    def test_40_certified_release_is_source_blocked(self) -> None:
        row = valid_release_manifest()
        row["compatibility_verification_sha256"] = VIEW_SHA
        row["output_manifest_sha256"] = VIEW_SHA
        row["schema_lock_sha256"] = VIEW_SHA
        row["inverse_replay"]["raw_projection_sha256"] = VIEW_SHA
        row["two_clean_build_digests"] = [VIEW_SHA, VIEW_SHA]
        row["certification_state"] = "AUDIT_CERTIFIED"
        row["audit_certificate"] = {"certificate_id": "CERTIFICATE-1", "witness_lock_sha256": VIEW_SHA}
        self.expect_failure(lib.validate_release_manifest, row, self.registry)

    def test_41_externally_pinned_package_lock_passes(self) -> None:
        result = lib.validate_package(ROOT, schema_cli.EXPECTED_PIPELINE_SCHEMA_LOCK_SHA256)
        self.assertEqual(result["schema_count"], 14)

    def test_42_duplicate_key_json_fails_before_canonicalization(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.json"
            path.write_bytes(b'{"a":1,"a":2}\n')
            with self.assertRaisesRegex(lib.PipelineSchemaError, "duplicate JSON object key"):
                lib.load_json(path, require_cj1=False)

    def test_43_duplicate_key_jsonl_fails_before_canonicalization(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.jsonl"
            path.write_bytes(b'{"outer":{"a":1,"a":2}}\n')
            with self.assertRaisesRegex(lib.PipelineSchemaError, "duplicate JSON object key"):
                lib.load_jsonl(path, require_cj1=False)

    def test_44_raw_guard_path_must_join_stage2_manifest(self) -> None:
        row = valid_repair()
        row["guard"]["raw_source_path"] = "ref/A-New-Kind-of-Science/not-the-monolith.md"
        self.expect_failure(lib.validate_repair, row, self.registry)

    def test_45_raw_guard_span_and_blocks_must_join_stage2(self) -> None:
        row = valid_repair()
        row["guard"]["raw_block_ids"] = ["RAW-000002"]
        self.expect_failure(lib.validate_repair, row, self.registry)
        row = valid_repair()
        row["guard"]["span"]["sha256"] = EMPTY_SHA
        self.expect_failure(lib.validate_repair, row, self.registry)

    def test_46_mechanical_disposition_needs_real_typed_proof_and_checks(self) -> None:
        row = valid_repair()
        row["evidence"]["mechanical"] = []
        self.expect_failure(lib.validate_repair, row, self.registry)
        row = valid_repair()
        row["verification_results"] = []
        self.expect_failure(lib.validate_repair, row, self.registry)
        row = valid_repair()
        row["verification_results"][0]["details_sha256"] = VIEW_SHA
        self.expect_failure(lib.validate_repair, row, self.registry)

    def test_47_risk_class_tag_union_cannot_omit_or_understate(self) -> None:
        row = valid_repair()
        row["risk"]["class_tags"] = []
        self.expect_failure(lib.validate_repair, row, self.registry)
        row = valid_repair()
        row["repair_class"] = "PROSE_OCR"
        row["risk"]["class_tags"] = ["PROSE_OCR", "FORMULA_OR_SYMBOL"]
        row["target"] = {
            "canonical_document_id": "PUBLICATION_AND_CONTENTS",
            "node_ids": ["NODE-1"],
            "path": "CANONICAL/FRONT-MATTER/00-Publication-and-Contents.md",
            "role": "CANONICAL_AUTHOR_TEXT",
        }
        self.expect_failure(lib.validate_repair, row, self.registry)

    def test_48_joined_review_rows_are_validated_and_independent(self) -> None:
        repair = valid_repair()
        repair["review_ids"] = ["REVIEW-1"]
        review = closed_review("REVIEW-1", principal="creator")
        review["evidence_view_sha256"] = repair["evidence"]["mechanical"][0]["evidence_sha256"]
        self.expect_failure(lib.validate_repair_set, [repair], self.registry, [review])
        review["principal_id"] = "independent"
        review["decision_sha256"] = VIEW_SHA
        self.expect_failure(lib.validate_repair_set, [repair], self.registry, [review])

    def test_49_disagreement_needs_independent_joined_adjudication(self) -> None:
        first = valid_review()
        first.update(
            {
                "adjudicator_review_id": "REVIEW-ADJUDICATOR",
                "agreement_state": "DISAGREES",
                "closure_state": "CLOSED",
                "disagrees_with_review_ids": ["REVIEW-2"],
                "follow_up": "Independent adjudication completed.",
                "review_id": "REVIEW-1",
            }
        )
        second = valid_review()
        second.update({"closure_state": "CLOSED", "principal_id": "second", "review_id": "REVIEW-2"})
        adjudicator = valid_review()
        adjudicator.update(
            {
                "agreement_state": "NOT_APPLICABLE",
                "closure_state": "CLOSED",
                "principal_id": "third",
                "review_id": "REVIEW-ADJUDICATOR",
                "reviewer_role": "ADJUDICATOR",
                "specialty": "NOT_APPLICABLE",
            }
        )
        result = lib.validate_review_set([first, second, adjudicator], self.registry)
        self.assertEqual(set(result), {"REVIEW-1", "REVIEW-2", "REVIEW-ADJUDICATOR"})
        adjudicator["principal_id"] = first["principal_id"]
        self.expect_failure(lib.validate_review_set, [first, second, adjudicator], self.registry)

    def test_50_fabricated_review_witness_region_fails_join(self) -> None:
        row = valid_review()
        row["witness_region_ids"] = ["WITNESS-FAKE"]
        self.expect_failure(lib.validate_review, row, self.registry)

    def test_51_raw_preserved_provenance_joins_frozen_span(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            path = output / "CANONICAL/FRONT-MATTER/00-Publication-and-Contents.md"
            path.parent.mkdir(parents=True)
            path.write_bytes(GUARD_BYTES)
            ast = [valid_ast_node("NODE-RAW-1")]
            lib.validate_provenance(
                valid_raw_provenance(), self.registry, output_root=output, ast_nodes=ast
            )
            row = valid_raw_provenance()
            row["source"]["raw_block_ids"] = ["RAW-000002"]
            self.expect_failure(
                lib.validate_provenance,
                row,
                self.registry,
                output_root=output,
                ast_nodes=ast,
            )

    def test_52_raw_exclusion_is_typed_but_source_blocked(self) -> None:
        row = valid_raw_provenance()
        row["author_text_projection_sha256"] = EMPTY_SHA
        row["mapping_kind"] = "RAW_EXCLUDED"
        row["target"] = endpoint("TYPED_EXCLUSION", EMPTY_SHA, role=None, path=None)
        self.expect_failure(lib.validate_provenance, row, self.registry)

    def test_53_valid_source_blocked_technical_span_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            path = output / valid_technical()["output_path"]
            path.parent.mkdir(parents=True)
            path.write_bytes(GUARD_BYTES)
            lib.validate_technical(
                valid_technical(),
                self.registry,
                output_root=output,
                ast_nodes=[valid_ast_node("NODE-TECHNICAL-1")],
            )

    def test_54_technical_token_semantics_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            path = output / valid_technical()["output_path"]
            path.parent.mkdir(parents=True)
            path.write_bytes(GUARD_BYTES)
            kwargs = {"output_root": output, "ast_nodes": [valid_ast_node("NODE-TECHNICAL-1")]}
            row = valid_technical()
            row["tokens"][0]["raw_sha256"] = VIEW_SHA
            self.expect_failure(lib.validate_technical, row, self.registry, **kwargs)
            row = valid_technical()
            row["tokens"][0]["changed"] = True
            row["tokens"][0]["repaired_text"] = "changed"
            row["changed_token_ids"] = ["TOKEN-1"]
            self.expect_failure(lib.validate_technical, row, self.registry, **kwargs)

    def test_55_figure_fake_witness_id_fails_join(self) -> None:
        row = valid_figure()
        row["witness_region_ids"] = ["WITNESS-FAKE"]
        self.expect_failure(lib.validate_figure, row, self.registry)

    def test_56_complete_compatibility_behavior_passes(self) -> None:
        lib.validate_compatibility(valid_compatibility(), self.registry)

    def test_57_empty_or_incomplete_compatibility_scope_fails(self) -> None:
        row = valid_compatibility()
        row["oracle_results"] = []
        self.expect_failure(lib.validate_compatibility, row, self.registry)
        row = valid_compatibility()
        row["oracle_results"].pop()
        self.expect_failure(lib.validate_compatibility, row, self.registry)

    def test_58_compatibility_identical_flag_cannot_lie(self) -> None:
        row = valid_compatibility()
        row["oracle_results"][0]["current_framed_behavior_sha256"] = VIEW_SHA
        self.expect_failure(lib.validate_compatibility, row, self.registry)

    def test_59_corpus_canonical_path_role_mapping_is_exact(self) -> None:
        row = valid_corpus_manifest()
        row["files"][0]["path"] = "CANONICAL/fake.md"
        guardrails = lib.load_json(ROOT / "goal-4/guardrails.json", require_cj1=False)
        self.expect_failure(lib.validate_corpus_manifest, row, self.registry, guardrails)

    def test_60_certified_corpus_checks_real_files_and_projections_first(self) -> None:
        row = valid_corpus_manifest()
        row["certification_state"] = "AUDIT_CERTIFIED"
        row["author_text_projection_sha256"] = EMPTY_SHA
        guardrails = lib.load_json(ROOT / "goal-4/guardrails.json", require_cj1=False)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            projections: dict[str, bytes] = {}
            for item in row["files"]:
                path = output / item["path"]
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"")
                os.chmod(path, 0o644)
                item["author_text_projection_sha256"] = EMPTY_SHA
                item["byte_size"] = 0
                item["mode"] = "0644"
                item["sha256"] = EMPTY_SHA
                projections[item["path"]] = b""
            with self.assertRaisesRegex(lib.PipelineSchemaError, "current SOURCE_BLOCKED"):
                lib.validate_corpus_manifest(
                    row,
                    self.registry,
                    guardrails,
                    output_root=output,
                    author_text_projections=projections,
                )
            row["files"][0]["byte_size"] = 1
            with self.assertRaisesRegex(lib.PipelineSchemaError, "file/hash/size/mode drift"):
                lib.validate_corpus_manifest(
                    row,
                    self.registry,
                    guardrails,
                    output_root=output,
                    author_text_projections=projections,
                )

    def test_61_release_refuses_self_asserted_zero_digests(self) -> None:
        with self.assertRaisesRegex(lib.PipelineSchemaError, "all-zero placeholder"):
            lib.validate_release_manifest(valid_release_manifest(), self.registry)

    def test_62_not_published_release_must_enumerate_all_blockers(self) -> None:
        dynamic = valid_unresolved()
        expected = set(lib._frozen_indexes(self.registry)["open_unresolved_ids"]) | {
            dynamic["unresolved_id"]
        }
        self.assertEqual(
            lib.expected_release_blocker_ids(self.registry, [dynamic]), expected
        )

    def test_63_not_published_state_cannot_claim_atomic_publication(self) -> None:
        row = valid_release_manifest()
        for field in (
            "compatibility_observation_receipt_sha256",
            "compatibility_verification_sha256",
            "output_manifest_sha256",
            "reproducibility_receipt_sha256",
            "schema_lock_sha256",
        ):
            row[field] = VIEW_SHA
        row["inverse_replay"]["raw_projection_sha256"] = VIEW_SHA
        row["inverse_replay"]["receipt_sha256"] = VIEW_SHA
        row["rollback"]["receipt_sha256"] = VIEW_SHA
        row["two_clean_build_digests"] = [VIEW_SHA, VIEW_SHA]
        row["open_blocker_ids"] = sorted(lib._frozen_indexes(self.registry)["open_unresolved_ids"])
        row["publication"]["atomic_same_filesystem_rename"] = True
        with self.assertRaisesRegex(lib.PipelineSchemaError, "NOT_PUBLISHED"):
            lib.validate_release_manifest(row, self.registry)

    def test_64_package_validation_is_relocation_safe(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            relocated = Path(directory) / "relocated"
            shutil.copytree(ROOT / "goal-4", relocated / "goal-4")
            (relocated / "ref/A-New-Kind-of-Science-Repaired").mkdir(parents=True)
            result = lib.validate_package(
                relocated, schema_cli.EXPECTED_PIPELINE_SCHEMA_LOCK_SHA256
            )
            self.assertEqual(result["schema_count"], 14)
            completed = subprocess.run(
                [
                    sys.executable,
                    "-O",
                    str(relocated / "goal-4/tools/validate_pipeline_schemas.py"),
                    "--repo-root",
                    str(relocated),
                ],
                cwd=Path(directory),
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("Stage 4 pipeline schema validation: PASS", completed.stdout)

    def test_65_repair_row_hash_and_overlay_projection_bridge_are_exact(self) -> None:
        row, operation_row = valid_overlay_binding(self.registry)
        binding = lib.validate_overlay_operation_binding(
            row, self.registry, operation_row
        )
        self.assertTrue(binding.overlay_operation_bound)
        self.assertEqual(binding.repair_row_sha256, lib.canonical_repair_row_sha256(row))
        self.assertEqual(binding.expected_target_sha256, row["target_state_guards"]["before_sha256"])
        self.assertEqual(binding.expected_result_sha256, row["target_state_guards"]["after_sha256"])
        self.assertEqual(binding.forward_payload_sha256, row["forward_operation"]["payload_sha256"])
        self.assertEqual(binding.inverse_payload_sha256, row["inverse_operation"]["payload_sha256"])
        row["operation_projection_sha256"] = EMPTY_SHA
        self.expect_failure(
            lib.validate_overlay_operation_binding, row, self.registry, operation_row
        )

    def test_66_raw_preserved_requires_concrete_output_and_ast_join(self) -> None:
        row = valid_raw_provenance()
        self.expect_failure(lib.validate_provenance, row, self.registry)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            path = output / row["target"]["path"]
            path.parent.mkdir(parents=True)
            path.write_bytes(b"X" + GUARD_BYTES)
            self.expect_failure(
                lib.validate_provenance,
                row,
                self.registry,
                output_root=output,
                ast_nodes=[valid_ast_node("NODE-RAW-1")],
            )

    def test_67_complete_provenance_is_bidirectional_not_source_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            row = valid_raw_provenance()
            path = output / row["target"]["path"]
            path.parent.mkdir(parents=True)
            path.write_bytes(GUARD_BYTES)
            with self.assertRaisesRegex(lib.PipelineSchemaError, "exact ordered raw-block coverage"):
                lib.validate_provenance_set(
                    [row],
                    self.registry,
                    require_complete_raw_coverage=True,
                    output_root=output,
                    ast_nodes=[valid_ast_node("NODE-RAW-1")],
                )

    def test_68_overlay_bridge_binds_target_guards_and_typed_fields(self) -> None:
        row, operation_row = valid_overlay_binding(self.registry)
        row["target_state_guards"]["before_sha256"] = EMPTY_SHA
        row["evidence"]["mechanical"][0]["evidence_sha256"] = lib.mechanical_proof_sha256(row)
        row["verification_results"] = [
            {"check_id": check, "details_sha256": lib.mechanical_check_sha256(row, check), "passed": True}
            for check in lib.MECHANICAL_CHECK_IDS
        ]
        self.expect_failure(
            lib.validate_overlay_operation_binding, row, self.registry, operation_row
        )
        row, operation_row = valid_overlay_binding(self.registry)
        row["forward_operation"]["payload"]["operation_fields"]["destination_right_id"] = "RAW-000004"
        row["inverse_operation"]["payload"]["operation_fields"]["source_right_id"] = "RAW-000004"
        for key in ("forward_operation", "inverse_operation"):
            row[key]["payload_sha256"] = payload_hash(row[key]["payload"])
        row["evidence"]["mechanical"][0]["evidence_sha256"] = lib.mechanical_proof_sha256(row)
        row["verification_results"] = [
            {"check_id": check, "details_sha256": lib.mechanical_check_sha256(row, check), "passed": True}
            for check in lib.MECHANICAL_CHECK_IDS
        ]
        self.expect_failure(
            lib.validate_overlay_operation_binding, row, self.registry, operation_row
        )

    def test_69_technical_output_span_cannot_be_absent_or_arbitrary(self) -> None:
        row = valid_technical()
        self.expect_failure(lib.validate_technical, row, self.registry)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            path = output / row["output_path"]
            path.parent.mkdir(parents=True)
            path.write_bytes(GUARD_BYTES)
            row["output_span"]["start_byte"] = 1_000_000_000
            row["output_span"]["end_byte_exclusive"] = 1_000_000_000 + len(GUARD_BYTES)
            self.expect_failure(
                lib.validate_technical,
                row,
                self.registry,
                output_root=output,
                ast_nodes=[valid_ast_node("NODE-TECHNICAL-1")],
            )

    def test_70_navigation_enforces_workflow_sequence_and_destination(self) -> None:
        anchor = valid_navigation()
        ast = [valid_ast_node("NODE-NAV-1", anchor_id=anchor["anchor_id"])]
        anchor["workflow"]["events"][1]["sequence"] = 9
        self.expect_failure(lib.validate_navigation, anchor, self.registry, ast_nodes=ast)
        anchor = valid_navigation()
        anchor["sequence"] = 2
        self.expect_failure(lib.validate_navigation_set, [anchor], self.registry, ast_nodes=ast)
        link = valid_navigation()
        link.update({"anchor_id": None, "link_kind": "NEXT", "record_type": "LINK"})
        self.expect_failure(lib.validate_navigation, link, self.registry, ast_nodes=ast)

    def test_71_compatibility_needs_separate_observation_for_release_evidence(self) -> None:
        record = valid_compatibility()
        lib.validate_compatibility(record, self.registry)
        receipt = valid_compatibility_observation(record)
        lib.validate_compatibility_observation(record, receipt, self.registry)
        receipt["oracle_receipts"][0]["execution_receipt"]["stdout_sha256"] = VIEW_SHA
        receipt["oracle_receipts"][0]["execution_receipt"]["receipt_sha256"] = receipt_hash(
            receipt["oracle_receipts"][0]["execution_receipt"]
        )
        receipt["oracle_receipts"][0]["receipt_sha256"] = receipt_hash(receipt["oracle_receipts"][0])
        receipt["receipt_sha256"] = receipt_hash(receipt)
        self.expect_failure(
            lib.validate_compatibility_observation, record, receipt, self.registry
        )

    def test_72_release_ledger_validation_fails_closed_on_absent_registry_files(self) -> None:
        self.expect_failure(
            lib._validate_release_ledgers,
            self.registry,
            self.contract,
            output_root=None,
            ast_nodes=[],
        )

    def test_73_release_schema_rejects_boolean_only_execution_claims(self) -> None:
        row = valid_release_manifest()
        row["inverse_replay"]["passed"] = True
        row["rollback"]["verified"] = True
        self.expect_failure(lib.validate_release_manifest, row, self.registry)

    def test_74_overlay_review_metadata_joins_every_exact_registry_field(self) -> None:
        row, operation_row = valid_overlay_binding(self.registry)
        review = closed_review("REVIEW-1", principal="independent")
        review["evidence_view_sha256"] = row["evidence"]["mechanical"][0]["evidence_sha256"]
        review["decision_kind"] = "APPROVAL"
        review["decision_payload"] = "APPROVED"
        review["decision_sha256"] = projection("APPROVED")["sha256"]
        row["review_ids"] = [review["review_id"]]
        exact_review = overlay_lib.IndependentReview(
            review_id=review["review_id"],
            creator_principal_id=row["creator"]["principal_id"],
            source_reviewer_principal_id=review["principal_id"],
            source_reviewer_type=review["reviewer_type"],
            source_reviewer_session_id=review["session_id"],
            source_reviewer_role=review["reviewer_role"],
            source_decision="APPROVED",
            evidence_view_sha256=review["evidence_view_sha256"],
            review_row_sha256=hashlib.sha256(lib.canonical_json_bytes(review)).hexdigest(),
            blind_preproposal=review["blind_preproposal"],
        )
        operation_row = replace(operation_row, meta=replace(operation_row.meta, review=exact_review))
        row["operation_projection_sha256"] = overlay_lib.operation_projection_sha256(operation_row)
        lib.validate_overlay_operation_binding(
            row, self.registry, operation_row, [review]
        )
        altered = replace(exact_review, source_reviewer_session_id="different-session")
        operation_row = replace(operation_row, meta=replace(operation_row.meta, review=altered))
        row["operation_projection_sha256"] = overlay_lib.operation_projection_sha256(operation_row)
        self.expect_failure(
            lib.validate_overlay_operation_binding,
            row,
            self.registry,
            operation_row,
            [review],
        )

    def test_75_ast_raw_ids_bind_each_node_to_exact_bytes_not_only_partition(self) -> None:
        indexes = lib._frozen_indexes(self.registry)
        first = indexes["blocks_by_id"]["RAW-000001"]
        second = indexes["blocks_by_id"]["RAW-000002"]
        exact = MONOLITH_BYTES[first["start_byte"] : second["end_byte_exclusive"]]
        node = valid_ast_node(
            "NODE-TWO-BLOCKS",
            data=exact,
            raw_block_ids=["RAW-000001", "RAW-000002"],
        )
        lib._validated_ast_nodes(self.registry, [node])
        skewed = exact[len(GUARD_BYTES) :] + exact[: len(GUARD_BYTES)]
        node = valid_ast_node(
            "NODE-TWO-BLOCKS",
            data=skewed,
            raw_block_ids=["RAW-000001", "RAW-000002"],
        )
        self.expect_failure(lib._validated_ast_nodes, self.registry, [node])

    def test_76_overlay_bridge_rejects_unrelated_or_negative_review_directly(self) -> None:
        row, operation_row = valid_overlay_binding(self.registry)
        review = closed_review("REVIEW-NEGATIVE", principal="independent")
        review.update({"decision_kind": "REJECTION", "decision_payload": "REJECTED", "subject_id": "REPAIR-OTHER", "repair_id": "REPAIR-OTHER"})
        review["decision_sha256"] = projection("REJECTED")["sha256"]
        review["evidence_view_sha256"] = row["evidence"]["mechanical"][0]["evidence_sha256"]
        row["review_ids"] = [review["review_id"]]
        meta_review = overlay_lib.IndependentReview(
            review_id=review["review_id"], creator_principal_id="creator",
            source_reviewer_principal_id=review["principal_id"], source_reviewer_type=review["reviewer_type"],
            source_reviewer_session_id=review["session_id"], source_reviewer_role=review["reviewer_role"],
            source_decision="APPROVED", evidence_view_sha256=review["evidence_view_sha256"],
            review_row_sha256=hashlib.sha256(lib.canonical_json_bytes(review)).hexdigest(),
            blind_preproposal=review["blind_preproposal"],
        )
        operation_row = replace(operation_row, meta=replace(operation_row.meta, review=meta_review))
        row["operation_projection_sha256"] = overlay_lib.operation_projection_sha256(operation_row)
        self.expect_failure(lib.validate_overlay_operation_binding, row, self.registry, operation_row, [review])

    def test_77_resolved_navigation_link_joins_resolved_anchor_and_link_ast(self) -> None:
        anchor = valid_navigation()
        anchor["sequence"] = 0
        link = valid_navigation()
        link.update({
            "anchor_id": None,
            "destination_anchor_id": anchor["anchor_id"],
            "destination_path": anchor["source_path"],
            "link_kind": "NEXT",
            "navigation_id": "NAVIGATION-2",
            "record_type": "LINK",
            "sequence": 1,
            "source_node_id": "NODE-LINK-1",
        })
        ast = [
            valid_ast_node("NODE-NAV-1", anchor_id=anchor["anchor_id"]),
            valid_ast_node("NODE-LINK-1", node_type="GENERATED_LINK", destination=anchor["anchor_id"], link_kind="NEXT"),
        ]
        lib.validate_navigation_set([anchor, link], self.registry, ast_nodes=ast)
        anchor["resolution_state"] = "BROKEN"
        anchor["workflow"] = blocked_workflow()
        anchor["unresolved_ids"] = anchor["workflow"]["unresolved_ids"]
        self.expect_failure(lib.validate_navigation_set, [anchor, link], self.registry, ast_nodes=ast)

    def test_78_navigation_dynamic_blocker_requires_exact_unresolved_fk(self) -> None:
        row = valid_navigation()
        row["resolution_state"] = "SOURCE_BLOCKED"
        row["workflow"] = blocked_workflow("UNRESOLVED-TEST-1")
        row["unresolved_ids"] = ["UNRESOLVED-TEST-1"]
        ast = [valid_ast_node("NODE-NAV-1", anchor_id=row["anchor_id"])]
        self.expect_failure(lib.validate_navigation, row, self.registry, ast_nodes=ast)
        lib.validate_navigation(row, self.registry, ast_nodes=ast, unresolved_records=[valid_unresolved()])

    def test_79_figure_set_rejects_duplicate_ids_and_wrong_review_subject(self) -> None:
        first = valid_figure()
        second = valid_figure()
        second["record_id"] = "FIGURE-2"
        self.expect_failure(lib.validate_figure_set, [first, second], self.registry)
        review = closed_review("REVIEW-FIGURE", role="SPECIALIST_REVIEWER", subject_id="WRONG-FIGURE")
        review.update({"repair_id": None, "specialty": "FIGURE_CAPTION", "subject_type": "FIGURE_GROUP"})
        first["review_ids"] = [review["review_id"]]
        self.expect_failure(lib.validate_figure_set, [first], self.registry, review_records=[review])

    def test_80_registered_ast_ledger_rejects_different_caller_rows(self) -> None:
        ledger = [valid_ast_node("NODE-LEDGER-1")]
        self.assertEqual(lib.validate_registered_ast_rows(self.registry, ledger), ledger)
        caller = deepcopy(ledger)
        caller[0]["node_id"] = "NODE-CALLER-DIFFERENT"
        self.expect_failure(lib.validate_registered_ast_rows, self.registry, ledger, caller)

    def test_81_release_blocker_union_includes_dynamic_open_rows_only(self) -> None:
        dynamic = valid_unresolved()
        expected = set(lib._frozen_indexes(self.registry)["open_unresolved_ids"]) | {dynamic["unresolved_id"]}
        self.assertEqual(lib.expected_release_blocker_ids(self.registry, [dynamic]), expected)
        dynamic["workflow_state"] = "CLOSED"
        dynamic["final_disposition"] = "UNRESOLVED_SOURCE_NEEDED"
        dynamic["resolution"] = {"evidence_ids": [], "resolution_sha256": VIEW_SHA, "summary": "closed"}
        self.assertEqual(
            lib.expected_release_blocker_ids(self.registry, [dynamic]),
            set(lib._frozen_indexes(self.registry)["open_unresolved_ids"]),
        )


if __name__ == "__main__":
    unittest.main()
