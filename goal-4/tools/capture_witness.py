#!/usr/bin/env python3
"""Generate deterministic Stage 3 source-gap ledgers and their internal lock."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from witness_lib import (
    EXPECTED_BLOCKERS,
    EXPECTED_HELD_OUT_SHA256,
    EXPECTED_RAW_BLOCK_IDS_LF_SHA256,
    EXPECTED_SEGMENTS,
    EXPECTED_SELECTED_IDS_SHA256,
    EXPECTED_STRUCTURE_SHA256,
    WitnessError,
    load_json,
    load_jsonl,
    require,
    sha256_bytes,
    sha256_file,
    stable_json_sha256,
    validate_contract,
    validate_registry,
    validate_state,
)


SCHEMA_VERSION = "1.0.0"
GOAL_RELATIVE = Path("goal-4")
LEDGER_RELATIVE = GOAL_RELATIVE / "witness-region-ledger.jsonl"
UNRESOLVED_RELATIVE = GOAL_RELATIVE / "witness-unresolved.jsonl"
LOCK_RELATIVE = GOAL_RELATIVE / "witness-lock.json"


def canonical_json_bytes(value: Any, *, terminal_lf: bool = True) -> bytes:
    def reject_float(item: Any) -> None:
        if isinstance(item, float):
            raise WitnessError("Stage 3 canonical JSON forbids floating-point values")
        if isinstance(item, dict):
            for key, child in item.items():
                require(isinstance(key, str), "Stage 3 canonical JSON key is not a string")
                reject_float(child)
        elif isinstance(item, list):
            for child in item:
                reject_float(child)

    reject_float(value)
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return payload + (b"\n" if terminal_lf else b"")


def canonical_jsonl_bytes(rows: list[dict[str, Any]]) -> bytes:
    return b"".join(canonical_json_bytes(row) for row in rows)


def _exact_output(root: Path, relative: Path) -> Path:
    require(not relative.is_absolute() and ".." not in relative.parts, "unsafe generated output path")
    require(relative.parts[0] == "goal-4", "Stage 3 generated output escaped Goal 4")
    output = root / relative
    require(output.parent.resolve(strict=True) == (root / "goal-4").resolve(strict=True), "generated output parent drift")
    require(not output.is_symlink(), f"generated output is a symlink: {output}")
    return output


def _atomic_write(path: Path, payload: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _risk_dimensions(rows: list[dict[str, Any]], segment_id: str) -> list[str]:
    risks = {row.get("risk_stratum") for row in rows}
    dimensions: list[str] = []
    if segment_id != "INDEX":
        dimensions.append("PROSE_AND_PUNCTUATION")
    if "FORMULA_CODE_RULE_OR_DATA" in risks:
        dimensions.append("FORMULA_CODE_AND_DATA")
    if "FIGURE_CAPTION_OR_VISUAL" in risks:
        dimensions.append("FIGURE_CAPTION_AND_COLOR")
    if segment_id == "INDEX" or "INDEX_COLUMN_OR_ENTRY" in risks:
        dimensions.append("INDEX_ENTRY_AND_COLUMN")
    require(dimensions, f"segment has no witness risk dimension: {segment_id}")
    return dimensions


def build_region_ledger(root: Path) -> list[dict[str, Any]]:
    rows = load_jsonl(root / "goal-4/structure-ledger.jsonl")
    segments = sorted(
        (row for row in rows if row.get("record_type") == "SEGMENT"),
        key=lambda row: row.get("order"),
    )
    blocks = [row for row in rows if row.get("record_type") == "RAW_BLOCK"]
    require([row.get("segment_id") for row in segments] == EXPECTED_SEGMENTS, "segment universe drift")
    result: list[dict[str, Any]] = []
    for order, segment in enumerate(segments):
        segment_id = segment["segment_id"]
        segment_blocks = [row for row in blocks if row.get("segment_id") == segment_id]
        block_ids = [row["raw_block_id"] for row in segment_blocks]
        blocker_ids = [
            "WITNESS-PERMISSION",
            "WITNESS-COMPLETE-CENSUS",
            "WITNESS-EDITION-MATCH",
            "WITNESS-INDEPENDENT-REVIEW",
        ]
        if segment_id == "INDEX":
            blocker_ids.insert(2, "WITNESS-INDEX-LAYOUT")
        result.append(
            {
                "schema_version": SCHEMA_VERSION,
                "record_type": "SEGMENT_SOURCE_GAP",
                "coverage_id": f"WITNESS-GAP-{order + 1:04d}",
                "order": order,
                "segment_id": segment_id,
                "canonical_document_id": segment_id,
                "canonical_path": segment["canonical_path"],
                "raw_segment_sha256": segment["raw_segment_sha256"],
                "raw_block_count": len(block_ids),
                "raw_block_ids_sha256": stable_json_sha256(block_ids),
                "required_risk_dimensions": _risk_dimensions(segment_blocks, segment_id),
                "witness_unit_ids": [],
                "witness_region_ids": [],
                "coverage_status": "SOURCE_BLOCKED",
                "blocker_ids": blocker_ids,
                "unresolved_ids": [
                    "UNRESOLVED-WITNESS-0001",
                    "UNRESOLVED-WITNESS-0002",
                    "UNRESOLVED-WITNESS-0003",
                    "UNRESOLVED-WITNESS-0004",
                ],
                "repair_authorized": False,
            }
        )
    require(sum(row["raw_block_count"] for row in result) == 20430, "source-gap block coverage drift")
    return result


def build_unresolved_rows() -> list[dict[str, Any]]:
    definitions = [
        (
            "UNRESOLVED-WITNESS-0001",
            "COMPLETE_PRIMARY_WITNESS_NOT_ACQUIRED",
            [],
            "No complete edition-identical primary witness has been lawfully acquired and pinned.",
            ["Acquire a complete official or separately licensed edition-identical witness."],
        ),
        (
            "UNRESOLVED-WITNESS-0002",
            "AUTHORIZED_AUTOMATED_USE_NOT_ESTABLISHED",
            ["UNRESOLVED-WITNESS-0001"],
            "Posted terms do not establish permission for bulk or AI-assisted acquisition, storage, and review.",
            ["Obtain written permission covering automated or AI-assisted audit, storage, retention, and derivatives."],
        ),
        (
            "UNRESOLVED-WITNESS-0003",
            "RAW_EDITION_IDENTITY_NOT_ESTABLISHED",
            ["UNRESOLVED-WITNESS-0001"],
            "The local OCR lineage has not been proven edition-identical to the official First Edition, Fourth Printing surface.",
            ["Match copyright, publication, pagination, and sequential content fingerprints against an authorized witness."],
        ),
        (
            "UNRESOLVED-WITNESS-0004",
            "PHYSICAL_UNIT_REGION_CENSUS_NOT_DERIVED",
            ["UNRESOLVED-WITNESS-0001", "UNRESOLVED-WITNESS-0002"],
            "Covers, endpapers, leaves, blanks, pages, plates, inserts, foldouts, regions, and Index columns have not been censused.",
            ["Derive and independently review a complete physical/digital unit census and nonoverlapping region partition."],
        ),
    ]
    blocker_codes = [
        "WITNESS_IDENTITY_OR_REGION_GAP",
        "ILLEGIBLE_OR_UNTRANSCRIBED_AUTHORIAL_REGION",
        "UNRESOLVED_SOURCE_NEEDED_AUTHORIAL_ITEM",
        "RAW_WITNESS_CANONICAL_PROVENANCE_GAP_OR_OVERLAP",
        "MISSING_OR_UNLICENSED_AUTHORIAL_VISUAL_COMPONENT",
    ]
    rows: list[dict[str, Any]] = []
    for unresolved_id, kind, dependencies, impact, actions in definitions:
        rows.append(
            {
                "schema_version": SCHEMA_VERSION,
                "unresolved_id": unresolved_id,
                "kind": kind,
                "workflow_state": "SOURCE_BLOCKED",
                "severity": "RELEASE_BLOCKER",
                "owner_stage": "3-WITNESSES",
                "dependency_ids": dependencies,
                "source_candidate_ids": ["OFFICIAL_NKS_ONLINE"],
                "affected_segment_ids": EXPECTED_SEGMENTS,
                "affected_raw_block_count": 20430,
                "affected_raw_block_ids_lf_sha256": EXPECTED_RAW_BLOCK_IDS_LF_SHA256,
                "affected_legacy_asset_count": 1444,
                "affected_held_out_sample_count": 1125,
                "affected_held_out_sample_sha256": EXPECTED_SELECTED_IDS_SHA256,
                "release_blocker_codes": blocker_codes,
                "impact": impact,
                "attempted_alternatives": [
                    "Official page-numbered HTML and public chapter/section PDF surfaces were assessed without bulk retention.",
                    "The reflowed public Index was rejected as proof of printed column order.",
                    "Correlated local OCR derivatives and cropped JPEGs were rejected as independent witnesses.",
                ],
                "unblock_actions": actions,
                "repair_authorized": False,
                "final_disposition": None,
            }
        )
    return rows


def build_lock(
    root: Path,
    ledger_bytes: bytes,
    unresolved_bytes: bytes,
) -> dict[str, Any]:
    artifact_paths = [
        "goal-4/witness-contract.json",
        "goal-4/witness-mount-contract.md",
        "goal-4/witness-source-registry.json",
        "goal-4/witness-state.json",
    ]
    artifact_material = {
        path: ((root / path).stat().st_size, sha256_file(root / path))
        for path in artifact_paths
    }
    artifact_material[LEDGER_RELATIVE.as_posix()] = (
        len(ledger_bytes),
        sha256_bytes(ledger_bytes),
    )
    artifact_material[UNRESOLVED_RELATIVE.as_posix()] = (
        len(unresolved_bytes),
        sha256_bytes(unresolved_bytes),
    )
    artifacts = [
        {"path": path, "byte_size": artifact_material[path][0], "sha256": artifact_material[path][1]}
        for path in sorted(artifact_material)
    ]
    source_paths = [
        "goal-4/tests/test_witness.py",
        "goal-4/tools/capture_witness.py",
        "goal-4/tools/witness_lib.py",
    ]
    sources = [
        {
            "path": path,
            "byte_size": (root / path).stat().st_size,
            "sha256": sha256_file(root / path),
        }
        for path in source_paths
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "FROZEN_STAGE_3_SOURCE_BLOCKED",
        "artifacts": artifacts,
        "bindings": {
            "baseline_lock_sha256": sha256_file(root / "goal-4/baseline-lock.json"),
            "corpus_manifest_sha256": sha256_file(root / "goal-4/corpus-manifest.json"),
            "fidelity_contract_sha256": sha256_file(root / "goal-4/fidelity-contract.md"),
            "guardrails_sha256": sha256_file(root / "goal-4/guardrails.json"),
            "held_out_sample_sha256": EXPECTED_HELD_OUT_SHA256,
            "licensing_contract_sha256": sha256_file(root / "goal-4/licensing-contract.json"),
            "review_contract_sha256": sha256_file(root / "goal-4/review-contract.md"),
            "structure_ledger_sha256": EXPECTED_STRUCTURE_SHA256,
        },
        "sources": sources,
    }


def capture(root: Path, *, check: bool) -> None:
    root = root.resolve(strict=True)
    contract = load_json(root / "goal-4/witness-contract.json")
    registry = load_json(root / "goal-4/witness-source-registry.json")
    state = load_json(root / "goal-4/witness-state.json")
    validate_contract(contract, root)
    validate_registry(registry)
    validate_state(state, registry, root)
    ledger_bytes = canonical_jsonl_bytes(build_region_ledger(root))
    unresolved_bytes = canonical_jsonl_bytes(build_unresolved_rows())
    lock_bytes = canonical_json_bytes(build_lock(root, ledger_bytes, unresolved_bytes))
    outputs = {
        _exact_output(root, LEDGER_RELATIVE): ledger_bytes,
        _exact_output(root, UNRESOLVED_RELATIVE): unresolved_bytes,
        _exact_output(root, LOCK_RELATIVE): lock_bytes,
    }
    for path, payload in outputs.items():
        if check:
            require(path.is_file(), f"generated Stage 3 artifact is missing: {path}")
            require(path.read_bytes() == payload, f"generated Stage 3 artifact drift: {path}")
        else:
            _atomic_write(path, payload)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        capture(args.repo_root, check=args.check)
    except WitnessError as error:
        print(f"WITNESS CAPTURE FAIL: {error}")
        return 1
    print("WITNESS CAPTURE OK" if not args.check else "WITNESS REPRODUCIBILITY OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
