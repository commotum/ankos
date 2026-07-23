from __future__ import annotations

import copy
import csv
import hashlib
import json
import shutil
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from types import MappingProxyType
from typing import Any

import pytest


TOOLS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_DIR))

import build_worker_bundle  # noqa: E402
import merge_worker_output as merge  # noqa: E402
from audit_contract import (  # noqa: E402
    ASSET_HEADER,
    CANDIDATE_FIELDS,
    FINGERPRINT_FIELDS,
    READING_HEADER,
    canonical_json_bytes,
)


ASSIGNMENT_PATH = "FRONT-MATTER/01-Preface.md"
FIRST_STAGE_4_PATH = "FRONT-MATTER/00-Publication-and-Contents.md"
INITIAL_STAGE_4_PREFIX = [FIRST_STAGE_4_PATH, ASSIGNMENT_PATH]
STAGE_5_PATH = "CHAPTERS/01-The-Foundations-for-a-New-Kind-of-Science.md"
STAGE_5_NOTES_PATH = (
    "BACK-MATTER/NOTES/01-The-Foundations-for-a-New-Kind-of-Science-Notes.md"
)


class InjectedTransactionInterrupt(BaseException):
    """Deterministic stand-in for an interruption at a transaction boundary."""


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _candidate(
    source_unit_id: str,
    image_path: str,
    epoch: int,
    stage: int = 4,
) -> dict[str, Any]:
    missing = "Further mechanics are not stated in this evidence."
    field_support = {
        field: "UNKNOWN_FROM_SOURCE" for field in FINGERPRINT_FIELDS
    }
    fingerprint = {
        field: {
            "status": "UNKNOWN_FROM_SOURCE",
            "value": None,
            "evidence_ids": [],
            "reason": missing,
        }
        for field in FINGERPRINT_FIELDS
    }
    values: dict[str, Any] = {
        "id": "W0001",
        "record_status": "ACTIVE",
        "provisional_name": "Test construction lead",
        "aliases": [],
        "discovery_stage": stage,
        "discovery_anchor": {
            "epoch": epoch,
            "kind": "SOURCE_UNIT",
            "id": source_unit_id,
            "ordinal": 1,
        },
        "source_unit_ids": [source_unit_id],
        "source_evidence": [
            {
                "evidence_id": "WE000001",
                "evidence_group_id": "WG000001",
                "discovery_anchor": {
                    "epoch": epoch,
                    "kind": "SOURCE_UNIT",
                    "id": source_unit_id,
                    "ordinal": 1,
                },
                "source_unit_id": source_unit_id,
                "image_path": None,
                "strength": "LEAD_ONLY",
                "modality": "PROSE",
                "claim": "The source unit supplies a construction lead.",
                "fingerprint_fields": [],
            },
            {
                "evidence_id": "WE000002",
                "evidence_group_id": "WG000002",
                "discovery_anchor": {
                    "epoch": epoch,
                    "kind": "IMAGE",
                    "id": image_path,
                    "ordinal": 1,
                },
                "source_unit_id": None,
                "image_path": image_path,
                "strength": "CORROBORATING",
                "modality": "IMAGE",
                "claim": "The assigned image corroborates the lead.",
                "fingerprint_fields": [],
            },
        ],
        "source_status": ["CLEAR"],
        "image_witnesses": [image_path],
        "evidence_strength": ["LEAD_ONLY", "CORROBORATING"],
        "field_support": field_support,
        "fingerprint": fingerprint,
        "parameters": [],
        "variants": [],
        "missing_mechanics": [missing],
        "uncertainties": [],
        "related_candidate_ids": [],
        "cross_reference_ids": ["WR0001"],
        "evidence_reassignments": [],
    }
    return {field: values[field] for field in CANDIDATE_FIELDS}


def _completed_bundle(
    root: Path,
    *,
    epoch: int = 1,
    worker_id: str = "merge-test-worker",
) -> Path:
    bundle = root / "bundle"
    build_worker_bundle.build_bundle(
        bundle,
        worker_id,
        4,
        INITIAL_STAGE_4_PREFIX if epoch == 1 else [ASSIGNMENT_PATH],
        epoch=epoch,
    )
    manifest = json.loads(
        (bundle / "allowed-manifest.json").read_text(encoding="utf-8")
    )
    reading = _read_csv(bundle / "input" / "reading-input.csv")
    assets = _read_csv(bundle / "input" / "asset-input.csv")
    assert reading
    assert len(assets) == 1
    source_unit_id = next(
        row["source_unit_id"]
        for row in reading
        if row["path"] == ASSIGNMENT_PATH
    )
    asset_id = assets[0]["asset_id"]
    image_path = assets[0]["physical_path"]

    reading_updates: list[dict[str, str]] = []
    for original in reading:
        row = dict(original)
        is_candidate_source = row["source_unit_id"] == source_unit_id
        retained_candidates = json.loads(original["candidate_ids"])
        retained_routes = json.loads(original["route_ids"])
        row.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": str(manifest["discovery_epoch"]),
                "review_disposition": (
                    "CANDIDATE" if is_candidate_source else "NO_CONSTRUCTION"
                ),
                "source_status": "CLEAR",
                "secondary_roles": "[]",
                "candidate_ids": json.dumps(
                    retained_candidates
                    + (["W0001"] if is_candidate_source else []),
                    separators=(",", ":"),
                ),
                "route_ids": json.dumps(
                    retained_routes,
                    separators=(",", ":"),
                ),
                "evidence_statement": "Assigned source unit reviewed.",
                "review_stage": "4",
                "reviewer": worker_id,
            }
        )
        reading_updates.append(row)

    asset_update = dict(assets[0])
    retained_asset_candidates = json.loads(asset_update["candidate_ids"])
    retained_asset_routes = json.loads(asset_update["route_ids"])
    asset_update.update(
        {
            "inspection_status": "SCREENED",
            "review_epoch": str(manifest["discovery_epoch"]),
            "visual_role": "NATIVE_EVIDENCE",
            "source_status": "CLEAR",
            "risk_flags": '["CONSTRUCTION_BEARING"]',
            "original_resolution_status": "REVIEWED",
            "transcription_status": "CHECKED",
            "candidate_ids": json.dumps(
                retained_asset_candidates + ["W0001"],
                separators=(",", ":"),
            ),
            "route_ids": json.dumps(
                retained_asset_routes + ["WR0001"],
                separators=(",", ":"),
            ),
            "evidence_statement": "Assigned image reviewed at original resolution.",
            "review_stage": "4",
            "reviewer": worker_id,
            "uncertainty": "",
        }
    )

    route = {
        "route_id": "WR0001",
        "source_unit_id": "",
        "source_asset_id": asset_id,
        "discovery_epoch": str(manifest["discovery_epoch"]),
        "discovery_kind": "IMAGE",
        "discovery_id": asset_id,
        "discovery_ordinal": "1",
        "literal_target": "the following explanatory section",
        "route_kind": "SECTION",
        "expected_topic": "additional construction detail",
        "owning_stage": "4",
        "closure_scope": "WITHIN_STAGE",
        "status": "PENDING",
        "target_unit_ids": "[]",
        "target_asset_ids": "[]",
        "attempts": "[]",
        "vocabulary_terms": "[]",
        "defect_boundary": "",
    }

    output_path = bundle / "output" / "output.json"
    output = json.loads(output_path.read_text(encoding="utf-8"))
    output.update(
        {
            "prohibited_input_nonuse": True,
            "reading_updates": reading_updates,
            "candidate_proposals": [
                _candidate(source_unit_id, image_path, manifest["discovery_epoch"])
            ],
            "asset_updates": [asset_update],
            "route_proposals": [route],
            "uncertainties": [],
        }
    )
    output_path.write_bytes(canonical_json_bytes(output))
    errors = build_worker_bundle.verify_bundle(
        bundle,
        require_completed_output=True,
    )
    assert errors == []
    return bundle


def _completed_interleaved_evidence_bundle(root: Path) -> Path:
    """Build two candidates whose frozen evidence traversal is interleaved."""
    bundle = _completed_bundle(root)
    output_path = bundle / "output" / "output.json"
    output = json.loads(output_path.read_text(encoding="utf-8"))
    manifest = json.loads(
        (bundle / "allowed-manifest.json").read_text(encoding="utf-8")
    )
    reading_input = _read_csv(bundle / "input" / "reading-input.csv")
    preface_units = [
        row["source_unit_id"]
        for row in reading_input
        if row["path"] == ASSIGNMENT_PATH
    ]
    assert len(preface_units) >= 3
    first_source, second_source, third_source = preface_units[:3]
    image_path = output["asset_updates"][0]["physical_path"]

    first_candidate = output["candidate_proposals"][0]
    assert first_candidate["source_unit_ids"] == [first_source]
    source_one_evidence = first_candidate["source_evidence"][0]
    source_three_evidence = copy.deepcopy(source_one_evidence)
    source_three_evidence.update(
        {
            "evidence_id": "WE000003",
            "evidence_group_id": "WG000003",
            "discovery_anchor": {
                "epoch": manifest["discovery_epoch"],
                "kind": "SOURCE_UNIT",
                "id": third_source,
                "ordinal": 1,
            },
            "source_unit_id": third_source,
            "claim": "A later source unit corroborates the first lead.",
            "strength": "CORROBORATING",
        }
    )
    first_candidate.update(
        {
            "source_unit_ids": [first_source, third_source],
            "source_evidence": [
                source_one_evidence,
                source_three_evidence,
            ],
            "image_witnesses": [],
            "evidence_strength": ["LEAD_ONLY", "CORROBORATING"],
            "cross_reference_ids": [],
        }
    )

    second_candidate = _candidate(
        second_source,
        image_path,
        manifest["discovery_epoch"],
    )
    second_candidate.update(
        {
            "id": "W0002",
            "provisional_name": "Second interleaved construction lead",
            "discovery_anchor": {
                "epoch": manifest["discovery_epoch"],
                "kind": "SOURCE_UNIT",
                "id": second_source,
                "ordinal": 1,
            },
        }
    )
    second_candidate["source_evidence"][0].update(
        {
            "evidence_id": "WE000002",
            "evidence_group_id": "WG000002",
        }
    )
    second_candidate["source_evidence"][1].update(
        {
            "evidence_id": "WE000004",
            "evidence_group_id": "WG000004",
        }
    )
    output["candidate_proposals"] = [first_candidate, second_candidate]

    for row in output["reading_updates"]:
        unit_id = row["source_unit_id"]
        if unit_id == second_source:
            row.update(
                {
                    "review_disposition": "CANDIDATE",
                    "candidate_ids": '["W0002"]',
                    "evidence_statement": "Assigned source unit supplies the second lead.",
                }
            )
        elif unit_id == third_source:
            row.update(
                {
                    "review_disposition": "SUPPORTS_CANDIDATE",
                    "candidate_ids": '["W0001"]',
                    "evidence_statement": "Assigned source unit supports the first lead.",
                }
            )
    output["asset_updates"][0]["candidate_ids"] = '["W0002"]'
    output_path.write_bytes(canonical_json_bytes(output))
    assert build_worker_bundle.verify_bundle(
        bundle,
        require_completed_output=True,
    ) == []
    return bundle


def _completed_no_construction_bundle(
    root: Path,
    *,
    stage: int,
    assignment_path: str | None = None,
    assignment_paths: list[str] | None = None,
    epoch: int = 1,
    worker_id: str | None = None,
) -> Path:
    bundle = root / "bundle"
    if assignment_paths is None:
        assert assignment_path is not None
        assignment_paths = [assignment_path]
    assert assignment_path is None or assignment_paths == [assignment_path]
    worker_id = worker_id or f"stage-{stage}-order-test"
    build_worker_bundle.build_bundle(
        bundle,
        worker_id,
        stage,
        assignment_paths,
        epoch=epoch,
    )
    reading_updates: list[dict[str, str]] = []
    for original in _read_csv(bundle / "input" / "reading-input.csv"):
        row = dict(original)
        row.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": str(epoch),
                "review_disposition": "NO_CONSTRUCTION",
                "source_status": "CLEAR",
                "secondary_roles": "[]",
                "candidate_ids": original["candidate_ids"],
                "route_ids": original["route_ids"],
                "evidence_statement": "Assigned source unit reviewed.",
                "review_stage": str(stage),
                "reviewer": worker_id,
            }
        )
        reading_updates.append(row)
    asset_updates: list[dict[str, str]] = []
    for original in _read_csv(bundle / "input" / "asset-input.csv"):
        row = dict(original)
        row.update(
            {
                "inspection_status": "SCREENED",
                "review_epoch": str(epoch),
                "visual_role": "DECORATIVE",
                "source_status": "CLEAR",
                "risk_flags": "[]",
                "original_resolution_status": "NOT_REQUIRED",
                "transcription_status": "NOT_REQUIRED",
                "candidate_ids": original["candidate_ids"],
                "route_ids": original["route_ids"],
                "evidence_statement": "Assigned image screened.",
                "review_stage": str(stage),
                "reviewer": worker_id,
                "uncertainty": "",
            }
        )
        asset_updates.append(row)
    output_path = bundle / "output" / "output.json"
    output = json.loads(output_path.read_text(encoding="utf-8"))
    output.update(
        {
            "prohibited_input_nonuse": True,
            "reading_updates": reading_updates,
            "candidate_proposals": [],
            "asset_updates": asset_updates,
            "route_proposals": [],
            "uncertainties": [],
        }
    )
    output_path.write_bytes(canonical_json_bytes(output))
    assert build_worker_bundle.verify_bundle(
        bundle,
        require_completed_output=True,
    ) == []
    return bundle


def _copy_global_state(root: Path) -> Path:
    goal = root / "goal-4"
    goal.mkdir(parents=True)
    for name in merge.SNAPSHOT_NAMES:
        shutil.copy2(merge.GOAL_DIR / name, goal / name)
    shutil.copytree(merge.GOAL_DIR / "schemas", goal / "schemas")
    return goal


def _bytes(goal: Path) -> dict[str, bytes]:
    return {
        name: (goal / name).read_bytes()
        for name in merge.WRITE_NAMES
    }


def _transaction_state(
    goal: Path,
) -> tuple[dict[str, bytes], dict[str, int]]:
    return (
        _bytes(goal),
        {
            name: (goal / name).stat().st_mode & 0o777
            for name in merge.WRITE_NAMES
        },
    )


def _merge_staging_dirs(goal: Path) -> list[Path]:
    return sorted(goal.glob(".merge-worker-output-*"))


def _goal_after_initial_merge(root: Path) -> Path:
    bundle = _completed_bundle(root / "initial")
    goal = _copy_global_state(root / "state")
    merge.apply_merge(merge.prepare_merge(bundle, goal_dir=goal))
    return goal


def _search_candidate(
    source_unit_id: str,
    hit_id: str,
) -> dict[str, Any]:
    missing = "Further mechanics are not stated in this evidence."
    field_support = {
        field: "UNKNOWN_FROM_SOURCE" for field in FINGERPRINT_FIELDS
    }
    fingerprint = {
        field: {
            "status": "UNKNOWN_FROM_SOURCE",
            "value": None,
            "evidence_ids": [],
            "reason": missing,
        }
        for field in FINGERPRINT_FIELDS
    }
    values: dict[str, Any] = {
        "id": "B0001",
        "record_status": "ACTIVE",
        "provisional_name": "Search-discovered construction lead",
        "aliases": [],
        "discovery_stage": 4,
        "discovery_anchor": {
            "epoch": 1,
            "kind": "SEARCH_HIT",
            "id": hit_id,
            "ordinal": 1,
        },
        "source_unit_ids": [source_unit_id],
        "source_evidence": [
            {
                "evidence_id": "E000001",
                "evidence_group_id": "G000001",
                "discovery_anchor": {
                    "epoch": 1,
                    "kind": "SEARCH_HIT",
                    "id": hit_id,
                    "ordinal": 1,
                },
                "source_unit_id": source_unit_id,
                "image_path": None,
                "strength": "LEAD_ONLY",
                "modality": "PROSE",
                "claim": "The search hit supplies a governed construction lead.",
                "fingerprint_fields": [],
            }
        ],
        "source_status": ["CLEAR"],
        "image_witnesses": [],
        "evidence_strength": ["LEAD_ONLY"],
        "field_support": field_support,
        "fingerprint": fingerprint,
        "parameters": [],
        "variants": [],
        "missing_mechanics": [missing],
        "uncertainties": [],
        "related_candidate_ids": [],
        "cross_reference_ids": [],
        "evidence_reassignments": [],
    }
    return {field: values[field] for field in CANDIDATE_FIELDS}


def _search_enrichment_fixture(
    root: Path,
    *,
    second_candidate: bool = False,
) -> tuple[Path, Path, str, str]:
    initial_bundle = _completed_no_construction_bundle(
        root / "initial",
        stage=4,
        assignment_paths=INITIAL_STAGE_4_PREFIX,
        worker_id="search-enrichment-initial-reviewer",
    )
    goal = _copy_global_state(root / "state")
    merge.apply_merge(merge.prepare_merge(initial_bundle, goal_dir=goal))

    units = merge._read_jsonl(goal / merge.UNITS_NAME)
    target_units = [
        unit for unit in units if unit["path"] == ASSIGNMENT_PATH
    ]
    query = {
        "query_id": "Q0001",
        "family": "construction lead phrase",
        "pattern": "a first clue towards a whole new kind of science",
        "mode": "LITERAL",
        "case_sensitive": True,
        "whole_word": False,
        "scope_paths": INITIAL_STAGE_4_PREFIX,
    }
    pairs, errors = merge.validate_audit.execute_frozen_queries(
        [query],
        units,
        merge.validate_audit.REPO_ROOT
        / "ref"
        / "A-New-Kind-of-Science",
    )
    assert errors == []
    assert pairs
    target_ids = {unit["id"] for unit in target_units}
    governed_pair = next(pair for pair in pairs if pair[1] in target_ids)
    governed_unit_id = governed_pair[1]
    unit_by_id = {unit["id"]: unit for unit in units}
    governed_candidate_ids = (
        ["B0001", "B0002"] if second_candidate else ["B0001"]
    )
    hits: list[dict[str, Any]] = []
    governed_hit_id = ""
    for index, (query_id, unit_id) in enumerate(pairs, start=1):
        hit_id = f"H{index:06d}"
        governed = unit_id == governed_unit_id
        if governed:
            governed_hit_id = hit_id
        hits.append(
            {
                "hit_id": hit_id,
                "query_id": query_id,
                "source_unit_id": unit_id,
                "context_sha256": unit_by_id[unit_id]["sha256"],
                "disposition": (
                    "GOVERNED_CANDIDATE_OR_SUPPORT"
                    if governed
                    else "EXCLUSION"
                ),
                "candidate_ids": governed_candidate_ids if governed else [],
                "route_ids": [],
                "rationale": (
                    "The hit governs the newly discovered candidate."
                    if governed
                    else "The match is not a separate construction lead."
                ),
            }
        )
    assert governed_hit_id
    round_record: dict[str, Any] = {
        "round_id": "S001",
        "epoch": 1,
        "kind": "LOCAL",
        "owning_stage": 4,
        "queries": [query],
        "tool_assumptions": ["Literal UTF-8 source-unit search."],
        "result_ids": [hit["hit_id"] for hit in hits],
        "result_digest": "",
        "hits": hits,
        "new_vocabulary": [],
        "new_candidates": governed_candidate_ids,
        "new_evidence_groups": (
            ["G000001", "G000002"]
            if second_candidate
            else ["G000001"]
        ),
        "new_routes": [],
        "rerun_digest": "",
    }
    digest = merge.validate_audit.search_result_digest(round_record)
    round_record["result_digest"] = digest
    round_record["rerun_digest"] = digest
    proposed_search = {
        "schema_version": 1,
        "phase": "blind_discovery",
        "tool_assumptions": ["Literal UTF-8 source-unit search."],
        "vocabulary": [],
        "rounds": [round_record],
        "fixed_point": None,
    }

    reading = merge._read_csv(
        goal / merge.READING_NAME,
        READING_HEADER,
    )
    target = next(
        row for row in reading if row["source_unit_id"] == governed_unit_id
    )
    reading_update = dict(target)
    reading_update.update(
        {
            "review_disposition": "CANDIDATE",
            "candidate_ids": json.dumps(
                governed_candidate_ids,
                separators=(",", ":"),
            ),
            "evidence_statement": "The appended LOCAL hit supplies a construction lead.",
        }
    )
    candidate_updates = [
        _search_candidate(governed_unit_id, governed_hit_id)
    ]
    if second_candidate:
        second = copy.deepcopy(candidate_updates[0])
        second["id"] = "B0002"
        second["provisional_name"] = "Second search construction lead"
        second["discovery_anchor"]["ordinal"] = 2
        second["source_evidence"][0]["evidence_id"] = "E000002"
        second["source_evidence"][0]["evidence_group_id"] = "G000002"
        second["source_evidence"][0]["discovery_anchor"]["ordinal"] = 2
        candidate_updates.append(second)
    proposal = {
        "schema_version": 1,
        "proposal_kind": "SEARCH_APPEND",
        "coordinator_id": "search-enrichment-coordinator",
        "epoch": 1,
        "source_paths": [ASSIGNMENT_PATH],
        "base_artifact_sha256": {
            name: hashlib.sha256((goal / name).read_bytes()).hexdigest()
            for name in merge.WRITE_NAMES
        },
        "reading_updates": [reading_update],
        "asset_updates": [],
        "candidate_updates": candidate_updates,
        "route_appends": [],
        "proposed_search": proposed_search,
    }
    proposal_path = root / "search-enrichment-proposal.json"
    proposal_path.write_bytes(canonical_json_bytes(proposal))
    return goal, proposal_path, governed_unit_id, governed_hit_id


def _add_local_closure(
    goal: Path,
    *,
    epoch: int,
    stage: int,
    source_paths: list[str],
) -> None:
    search_path = goal / merge.SEARCH_NAME
    search = json.loads(search_path.read_text(encoding="utf-8"))
    assumption = "Deterministic zero-result fixture."
    if assumption not in search["tool_assumptions"]:
        search["tool_assumptions"].append(assumption)
    query_number = (
        sum(
            len(round_record["queries"])
            for round_record in search["rounds"]
        )
        + 1
    )
    round_record: dict[str, Any] = {
        "round_id": f"S{len(search['rounds']) + 1:03d}",
        "epoch": epoch,
        "kind": "LOCAL",
        "owning_stage": stage,
        "queries": [
            {
                "query_id": f"Q{query_number:04d}",
                "family": "deterministic merge-history closure fixture",
                "pattern": "__MERGE_HISTORY_IMPOSSIBLE_MATCH_71A9C2__",
                "mode": "LITERAL",
                "case_sensitive": True,
                "whole_word": False,
                "scope_paths": source_paths,
            }
        ],
        "tool_assumptions": [assumption],
        "result_ids": [],
        "result_digest": "",
        "hits": [],
        "new_vocabulary": [],
        "new_candidates": [],
        "new_evidence_groups": [],
        "new_routes": [],
        "rerun_digest": "",
    }
    digest = merge.validate_audit.search_result_digest(round_record)
    round_record["result_digest"] = digest
    round_record["rerun_digest"] = digest
    search["rounds"].append(round_record)
    proposal = {
        "schema_version": 1,
        "proposal_kind": "SEARCH_APPEND",
        "coordinator_id": "deterministic-local-closure-coordinator",
        "epoch": epoch,
        "source_paths": [],
        "base_artifact_sha256": {
            name: hashlib.sha256((goal / name).read_bytes()).hexdigest()
            for name in merge.WRITE_NAMES
        },
        "reading_updates": [],
        "asset_updates": [],
        "candidate_updates": [],
        "route_appends": [],
        "proposed_search": search,
    }
    proposal_path = (
        goal.parent
        / f"local-closure-stage-{stage}-epoch-{epoch}.json"
    )
    proposal_path.write_bytes(canonical_json_bytes(proposal))
    merge.apply_merge(
        merge.prepare_search_append(proposal_path, goal_dir=goal)
    )


def _complete_review_and_local_closure(goal: Path) -> None:
    manifest = json.loads(
        (goal / merge.MANIFEST_NAME).read_text(encoding="utf-8")
    )
    units = merge._read_jsonl(goal / merge.UNITS_NAME)
    reading = merge._read_csv(
        goal / merge.READING_NAME,
        READING_HEADER,
    )
    candidates = merge._read_jsonl(goal / merge.CANDIDATE_NAME)
    routes = merge._read_csv(
        goal / merge.ROUTE_NAME,
        merge.CROSS_REFERENCE_HEADER,
    )
    assets = merge._read_csv(goal / merge.ASSET_NAME, ASSET_HEADER)
    search = json.loads(
        (goal / merge.SEARCH_NAME).read_text(encoding="utf-8")
    )
    history = merge._read_jsonl(goal / merge.REVIEW_HISTORY_NAME)
    document_by_path = {
        document["path"]: document for document in manifest["documents"]
    }
    ordered_documents = sorted(
        manifest["documents"],
        key=lambda document: (
            merge.validate_audit.stage_for_document(document),
            int(document["order"]),
        ),
    )
    unit_by_id = {unit["id"]: unit for unit in units}

    for document in ordered_documents:
        path = document["path"]
        path_reading = [row for row in reading if row["path"] == path]
        if path_reading and all(
            row["review_status"] == "REVIEWED" for row in path_reading
        ):
            continue
        stage = merge.validate_audit.stage_for_document(document)
        reviewer = f"complete-review-stage-{stage}"
        for row in path_reading:
            row.update(
                {
                    "review_status": "REVIEWED",
                    "review_epoch": "1",
                    "review_disposition": "NO_CONSTRUCTION",
                    "source_status": "CLEAR",
                    "uncertainty": "",
                    "secondary_roles": "[]",
                    "candidate_ids": "[]",
                    "route_ids": "[]",
                    "evidence_statement": (
                        "No qualifying construction in this closure fixture unit."
                    ),
                    "review_stage": str(stage),
                    "reviewer": reviewer,
                }
            )
        for row in assets:
            if row["assignment_path"] != path:
                continue
            row.update(
                {
                    "inspection_status": "SCREENED",
                    "review_epoch": "1",
                    "visual_role": "DECORATIVE",
                    "source_status": "CLEAR",
                    "risk_flags": "[]",
                    "original_resolution_status": "NOT_REQUIRED",
                    "transcription_status": "NOT_REQUIRED",
                    "candidate_ids": "[]",
                    "route_ids": "[]",
                    "evidence_statement": (
                        "No construction-bearing visual content in this fixture."
                    ),
                    "review_stage": str(stage),
                    "reviewer": reviewer,
                    "uncertainty": "",
                }
            )
        event_core: dict[str, Any] = {
            "review_id": f"V{len(history) + 1:06d}",
            "epoch": 1,
            "stage": stage,
            "mode": "INITIAL",
            "reviewer": reviewer,
            "source_paths": [path],
        }
        path_change = merge.close_path_change(
            event_core,
            {
                "source_path": path,
                "source_unit_ids": [
                    unit["id"] for unit in units if unit["path"] == path
                ],
                "asset_ids": [
                    asset["asset_id"]
                    for asset in assets
                    if asset["assignment_path"] == path
                ],
                "previous_path_result_sha256": None,
            },
            unit_by_id,
            {row["source_unit_id"]: row for row in reading},
            {row["asset_id"]: row for row in assets},
        )
        event_core.update(
            {
                "path_changes": [path_change],
                "candidate_changes": [],
                "route_changes": [],
                "search_change": None,
            }
        )
        history.append(
            merge.close_review_event(
                event_core,
                history[-1]["event_sha256"],
            )
        )

    assumption = "Deterministic zero-result completion fixture."
    for stage in range(4, 18):
        scope_paths = [
            document["path"]
            for document in ordered_documents
            if merge.validate_audit.stage_for_document(document) == stage
        ]
        before_search = copy.deepcopy(search)
        round_record: dict[str, Any] = {
            "round_id": f"S{len(search['rounds']) + 1:03d}",
            "epoch": 1,
            "kind": "LOCAL",
            "owning_stage": stage,
            "queries": [
                {
                    "query_id": (
                        f"Q{sum(len(item['queries']) for item in search['rounds']) + 1:04d}"
                    ),
                    "family": "zero-result completion fixture",
                    "pattern": "__MERGE_COMPLETION_IMPOSSIBLE_MATCH_71A9C2__",
                    "mode": "LITERAL",
                    "case_sensitive": True,
                    "whole_word": False,
                    "scope_paths": scope_paths,
                }
            ],
            "tool_assumptions": [assumption],
            "result_ids": [],
            "result_digest": "",
            "hits": [],
            "new_vocabulary": [],
            "new_candidates": [],
            "new_evidence_groups": [],
            "new_routes": [],
            "rerun_digest": "",
        }
        digest = merge.validate_audit.search_result_digest(round_record)
        round_record["result_digest"] = digest
        round_record["rerun_digest"] = digest
        if assumption not in search["tool_assumptions"]:
            search["tool_assumptions"].append(assumption)
        search["rounds"].append(round_record)
        event_core = {
            "review_id": f"V{len(history) + 1:06d}",
            "epoch": 1,
            "stage": stage,
            "mode": "SEARCH_APPEND",
            "reviewer": "completion-search-coordinator",
            "source_paths": [],
            "path_changes": [],
            "candidate_changes": [],
            "route_changes": [],
            "search_change": merge.close_search_change(
                before_search,
                search,
            ),
        }
        history.append(
            merge.close_review_event(
                event_core,
                history[-1]["event_sha256"],
            )
        )

    (goal / merge.READING_NAME).write_bytes(
        build_worker_bundle.csv_bytes(READING_HEADER, reading)
    )
    (goal / merge.ASSET_NAME).write_bytes(
        build_worker_bundle.csv_bytes(ASSET_HEADER, assets)
    )
    (goal / merge.SEARCH_NAME).write_bytes(canonical_json_bytes(search))
    (goal / merge.REVIEW_HISTORY_NAME).write_bytes(
        merge._jsonl_bytes(history)
    )
    assert merge.validate_audit.validate_objects(
        manifest,
        units,
        reading,
        candidates,
        routes,
        assets,
        search,
        history,
    ) == []


@pytest.fixture(scope="module")
def closed_review_goal_template(
    tmp_path_factory: pytest.TempPathFactory,
) -> Path:
    root = tmp_path_factory.mktemp("closed-review-goal")
    goal = _goal_after_initial_merge(root)
    _complete_review_and_local_closure(goal)
    return goal


def _copy_goal_template(template: Path, root: Path) -> Path:
    goal = root / "goal-4"
    shutil.copytree(template, goal)
    return goal


def _resolved_route_proposal(goal: Path, root: Path) -> Path:
    routes = merge._read_csv(
        goal / merge.ROUTE_NAME,
        merge.CROSS_REFERENCE_HEADER,
    )
    assert len(routes) == 1
    update = dict(routes[0])
    target_unit_id = next(
        unit["id"]
        for unit in merge._read_jsonl(goal / merge.UNITS_NAME)
        if unit["path"] == ASSIGNMENT_PATH
    )
    update.update(
        {
            "status": "RESOLVED",
            "target_unit_ids": json.dumps(
                [target_unit_id],
                separators=(",", ":"),
            ),
            "attempts": '["Resolved against the reviewed Preface units."]',
        }
    )
    proposal = {
        "schema_version": 1,
        "proposal_kind": "ROUTE_RESOLUTION",
        "coordinator_id": "route-resolution-coordinator",
        "epoch": 1,
        "base_artifact_sha256": {
            name: hashlib.sha256((goal / name).read_bytes()).hexdigest()
            for name in merge.WRITE_NAMES
        },
        "route_updates": [update],
    }
    proposal_path = root / "route-resolution-proposal.json"
    proposal_path.write_bytes(canonical_json_bytes(proposal))
    return proposal_path


def _missing_route_proposal(
    goal: Path,
    root: Path,
    *,
    filename: str,
) -> tuple[Path, dict[str, str]]:
    routes = merge._read_csv(
        goal / merge.ROUTE_NAME,
        merge.CROSS_REFERENCE_HEADER,
    )
    assert len(routes) == 1
    update = dict(routes[0])
    update.update(
        {
            "status": "MISSING_TARGET_FINAL",
            "attempts": (
                '["Reviewed the complete canonical corpus and route context."]'
            ),
            "vocabulary_terms": (
                '["following explanatory section","additional construction detail"]'
            ),
            "defect_boundary": (
                "The canonical source contains no uniquely resolvable target "
                "after complete review and exact local-search closure."
            ),
        }
    )
    proposal = {
        "schema_version": 1,
        "proposal_kind": "ROUTE_RESOLUTION",
        "coordinator_id": "missing-route-resolution-coordinator",
        "epoch": 1,
        "base_artifact_sha256": {
            name: hashlib.sha256((goal / name).read_bytes()).hexdigest()
            for name in merge.WRITE_NAMES
        },
        "route_updates": [update],
    }
    proposal_path = root / filename
    proposal_path.parent.mkdir(parents=True, exist_ok=True)
    proposal_path.write_bytes(canonical_json_bytes(proposal))
    return proposal_path, update


def _stage18_saturation_proposal(
    goal: Path,
    root: Path,
    *,
    filename: str,
    establish_fixed_point: bool,
) -> tuple[Path, dict[str, Any]]:
    manifest = json.loads(
        (goal / merge.MANIFEST_NAME).read_text(encoding="utf-8")
    )
    ordered_documents = sorted(
        manifest["documents"],
        key=lambda document: (
            merge.validate_audit.stage_for_document(document),
            int(document["order"]),
        ),
    )
    search = json.loads(
        (goal / merge.SEARCH_NAME).read_text(encoding="utf-8")
    )
    round_record: dict[str, Any] = {
        "round_id": f"S{len(search['rounds']) + 1:03d}",
        "epoch": max(
            event["epoch"]
            for event in merge._read_jsonl(
                goal / merge.REVIEW_HISTORY_NAME
            )
        ),
        "kind": "SATURATION",
        "owning_stage": 18,
        "queries": [
            {
                "query_id": (
                    f"Q{sum(len(item['queries']) for item in search['rounds']) + 1:04d}"
                ),
                "family": "zero-result Stage 18 saturation fixture",
                "pattern": "__MERGE_COMPLETION_IMPOSSIBLE_MATCH_71A9C2__",
                "mode": "LITERAL",
                "case_sensitive": True,
                "whole_word": False,
                "scope_paths": [
                    document["path"] for document in ordered_documents
                ],
            }
        ],
        "tool_assumptions": [
            "Deterministic zero-result completion fixture."
        ],
        "result_ids": [],
        "result_digest": "",
        "hits": [],
        "new_vocabulary": [],
        "new_candidates": [],
        "new_evidence_groups": [],
        "new_routes": [],
        "rerun_digest": "",
    }
    digest = merge.validate_audit.search_result_digest(round_record)
    round_record["result_digest"] = digest
    round_record["rerun_digest"] = digest
    proposed_search = copy.deepcopy(search)
    proposed_search["rounds"].append(round_record)
    proposed_search["fixed_point"] = (
        {
            "round_id": round_record["round_id"],
            "zero_delta": True,
            "rerun_reproduced": True,
            "result_digest": digest,
        }
        if establish_fixed_point
        else None
    )
    proposal = {
        "schema_version": 1,
        "proposal_kind": "SEARCH_APPEND",
        "coordinator_id": "stage18-saturation-coordinator",
        "epoch": round_record["epoch"],
        "source_paths": [],
        "base_artifact_sha256": {
            name: hashlib.sha256((goal / name).read_bytes()).hexdigest()
            for name in merge.WRITE_NAMES
        },
        "reading_updates": [],
        "asset_updates": [],
        "candidate_updates": [],
        "route_appends": [],
        "proposed_search": proposed_search,
    }
    proposal_path = root / filename
    proposal_path.parent.mkdir(parents=True, exist_ok=True)
    proposal_path.write_bytes(canonical_json_bytes(proposal))
    return proposal_path, proposed_search


def test_default_cli_is_dry_run_and_rewrites_all_id_families(
    tmp_path: Path,
) -> None:
    bundle = _completed_bundle(tmp_path)
    goal = _copy_global_state(tmp_path)
    before = _bytes(goal)

    completed = subprocess.run(
        [
            sys.executable,
            str(TOOLS_DIR / "merge_worker_output.py"),
            str(bundle),
            "--goal-dir",
            str(goal),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    preview = json.loads(completed.stdout)
    assert preview["mode"] == "dry-run"
    assert preview["review_ids"] == ["V000001"]
    assert preview["review_mode"] == "INITIAL"
    assert preview["mappings"] == {
        "candidates": {"W0001": "B0001"},
        "routes": {"WR0001": "R000001"},
        "evidence": {
            "WE000001": "E000001",
            "WE000002": "E000002",
        },
        "evidence_groups": {
            "WG000001": "G000001",
            "WG000002": "G000002",
        },
    }
    assert preview["search_ledger_preserved"] is True
    assert _bytes(goal) == before


def test_interleaved_candidate_evidence_verifies_previews_and_validates(
    tmp_path: Path,
) -> None:
    bundle = _completed_interleaved_evidence_bundle(tmp_path)
    assert build_worker_bundle.verify_bundle(
        bundle,
        require_completed_output=True,
    ) == []
    goal = _copy_global_state(tmp_path)

    plan = merge.prepare_merge(bundle, goal_dir=goal)
    preview = plan.preview()
    assert preview["mappings"]["evidence"] == {
        "WE000001": "E000001",
        "WE000002": "E000002",
        "WE000003": "E000003",
        "WE000004": "E000004",
    }
    assert preview["mappings"]["evidence_groups"] == {
        "WG000001": "G000001",
        "WG000002": "G000002",
        "WG000003": "G000003",
        "WG000004": "G000004",
    }

    merge.apply_merge(plan)
    completed = subprocess.run(
        [
            sys.executable,
            str(TOOLS_DIR / "validate_audit.py"),
            "--repo-root",
            str(merge.validate_audit.REPO_ROOT),
            "--goal-dir",
            str(goal),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr


def test_interleaved_worker_evidence_rejects_invalid_local_allocations(
    tmp_path: Path,
) -> None:
    bundle = _completed_interleaved_evidence_bundle(tmp_path)
    output = json.loads(
        (bundle / "output" / "output.json").read_text(encoding="utf-8")
    )

    gap = copy.deepcopy(output)
    gap["candidate_proposals"][1]["source_evidence"][1][
        "evidence_id"
    ] = "WE000005"
    gap_errors = build_worker_bundle.verify_bundle(
        bundle,
        require_completed_output=True,
        worker_output_override=gap,
    )
    assert any(
        "complete unique WE000001 sequence" in error
        for error in gap_errors
    )

    duplicate = copy.deepcopy(output)
    duplicate["candidate_proposals"][1]["source_evidence"][0][
        "evidence_id"
    ] = "WE000001"
    duplicate_errors = build_worker_bundle.verify_bundle(
        bundle,
        require_completed_output=True,
        worker_output_override=duplicate,
    )
    assert any(
        "complete unique WE000001 sequence" in error
        for error in duplicate_errors
    )

    out_of_traversal = copy.deepcopy(output)
    first_late = out_of_traversal["candidate_proposals"][0][
        "source_evidence"
    ][1]
    second_early = out_of_traversal["candidate_proposals"][1][
        "source_evidence"
    ][0]
    first_late["evidence_id"], second_early["evidence_id"] = (
        second_early["evidence_id"],
        first_late["evidence_id"],
    )
    first_late["evidence_group_id"], second_early["evidence_group_id"] = (
        second_early["evidence_group_id"],
        first_late["evidence_group_id"],
    )
    traversal_errors = build_worker_bundle.verify_bundle(
        bundle,
        require_completed_output=True,
        worker_output_override=out_of_traversal,
    )
    assert any(
        "evidence ID order differs from frozen discovery-anchor traversal"
        in error
        for error in traversal_errors
    )


def test_apply_uses_validated_staged_ledgers_and_preserves_search(
    tmp_path: Path,
) -> None:
    bundle = _completed_bundle(tmp_path)
    goal = _copy_global_state(tmp_path)
    search_before = (goal / merge.SEARCH_NAME).read_bytes()

    plan = merge.prepare_merge(bundle, goal_dir=goal)
    merge.apply_merge(plan)

    assert (goal / merge.SEARCH_NAME).read_bytes() == search_before
    history = merge._read_jsonl(goal / merge.REVIEW_HISTORY_NAME)
    assert [event["review_id"] for event in history] == ["V000001"]
    assert history[0]["source_paths"] == INITIAL_STAGE_4_PREFIX
    assert history[0]["previous_event_sha256"] is None
    candidates = merge._read_jsonl(goal / merge.CANDIDATE_NAME)
    routes = merge._read_csv(
        goal / merge.ROUTE_NAME,
        merge.CROSS_REFERENCE_HEADER,
    )
    reading = merge._read_csv(goal / merge.READING_NAME, READING_HEADER)
    assets = merge._read_csv(goal / merge.ASSET_NAME, ASSET_HEADER)
    assert [row["id"] for row in candidates] == ["B0001"]
    assert len(history[0]["candidate_changes"]) == 1
    create = history[0]["candidate_changes"][0]
    assert create["action"] == "CREATE"
    assert create["candidate_id"] == "B0001"
    assert create["previous_candidate_result_sha256"] is None
    assert create["before_candidate"] is None
    assert create["before_candidate_sha256"] is None
    assert create["after_candidate"] == candidates[0]
    assert len(history[0]["route_changes"]) == 1
    assert history[0]["route_changes"][0]["after_route"] == routes[0]
    assert [row["route_id"] for row in routes] == ["R000001"]
    assert [
        item["evidence_id"] for item in candidates[0]["source_evidence"]
    ] == ["E000001", "E000002"]
    assert json.loads(
        next(
            row["candidate_ids"]
            for row in reading
            if row["source_unit_id"] == candidates[0]["source_unit_ids"][0]
        )
    ) == ["B0001"]
    assert json.loads(
        next(
            row["route_ids"]
            for row in assets
            if row["physical_path"] == candidates[0]["image_witnesses"][0]
        )
    ) == ["R000001"]


def test_prepared_plan_state_maps_are_frozen_and_token_bound(
    tmp_path: Path,
) -> None:
    bundle = _completed_bundle(tmp_path)
    goal = _copy_global_state(tmp_path)
    plan = merge.prepare_merge(bundle, goal_dir=goal)
    before = _transaction_state(goal)
    assert len(plan.validation_token) == 64

    replacements: dict[str, bytes | int] = {
        "proposed_bytes": plan.proposed_bytes[merge.READING_NAME] + b"\n",
        "original_bytes": plan.original_bytes[merge.READING_NAME] + b"\n",
        "original_modes": plan.original_modes[merge.READING_NAME] ^ 0o001,
    }
    for field, replacement_value in replacements.items():
        frozen = getattr(plan, field)
        assert isinstance(frozen, MappingProxyType)
        with pytest.raises(TypeError):
            frozen[merge.READING_NAME] = replacement_value

        replaced = dict(frozen)
        replaced[merge.READING_NAME] = replacement_value
        tampered = replace(
            plan,
            **{field: MappingProxyType(replaced)},
        )
        with pytest.raises(
            merge.MergeError,
            match="prepared plan validation token mismatch",
        ):
            merge.apply_merge(tampered)
        assert _transaction_state(goal) == before

    mutable_replacement = replace(
        plan,
        proposed_bytes=dict(plan.proposed_bytes),
    )
    with pytest.raises(
        merge.MergeError,
        match="prepared plan proposed_bytes map is not frozen",
    ):
        merge.apply_merge(mutable_replacement)
    assert _transaction_state(goal) == before


def test_apply_fault_rolls_back_through_durable_transaction(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bundle = _completed_bundle(tmp_path)
    goal = _copy_global_state(tmp_path)
    plan = merge.prepare_merge(bundle, goal_dir=goal)
    before = _transaction_state(goal)
    real_apply = merge.audit_transaction.apply_transaction

    def faulted_apply(
        goal_dir: Path,
        base_bytes: dict[str, bytes],
        proposed_bytes: dict[str, bytes],
        artifact_modes: dict[str, int],
    ) -> object:
        def inject(event: str) -> None:
            if event == (
                "apply:after_replace:"
                + merge.audit_transaction.ARTIFACT_NAMES[0]
            ):
                raise OSError("injected durable apply failure")

        return real_apply(
            goal_dir,
            base_bytes,
            proposed_bytes,
            artifact_modes,
            fault_injector=inject,
        )

    monkeypatch.setattr(
        merge.audit_transaction,
        "apply_transaction",
        faulted_apply,
    )
    with pytest.raises(
        merge.MergeError,
        match="recovery action=ROLLED_BACK_MIXED",
    ):
        merge.apply_merge(plan)

    assert _transaction_state(goal) == before
    assert not (goal / merge.audit_transaction.PENDING_NAME).exists()


def test_bad_completed_bundle_is_rejected(tmp_path: Path) -> None:
    bundle = _completed_bundle(tmp_path)
    goal = _copy_global_state(tmp_path)
    output_path = bundle / "output" / "output.json"
    output = json.loads(output_path.read_text(encoding="utf-8"))
    output["prohibited_input_nonuse"] = False
    output_path.write_bytes(canonical_json_bytes(output))

    with pytest.raises(merge.MergeError, match="bundle verification failed"):
        merge.prepare_merge(bundle, goal_dir=goal)


def test_worker_review_epoch_must_match_bundle_epoch(tmp_path: Path) -> None:
    bundle = _completed_bundle(tmp_path)
    goal = _copy_global_state(tmp_path)
    output_path = bundle / "output" / "output.json"
    output = json.loads(output_path.read_text(encoding="utf-8"))
    output["reading_updates"][0]["review_epoch"] = "2"
    output_path.write_bytes(canonical_json_bytes(output))

    with pytest.raises(
        merge.MergeError,
        match="review_epoch differs from bundle",
    ):
        merge.prepare_merge(bundle, goal_dir=goal)


def test_stale_input_projection_is_rejected(tmp_path: Path) -> None:
    bundle = _completed_bundle(tmp_path)
    goal = _copy_global_state(tmp_path)
    rows = _read_csv(goal / merge.READING_NAME)
    target = next(row for row in rows if row["path"] == ASSIGNMENT_PATH)
    target["evidence_statement"] = "Concurrent global change."
    (goal / merge.READING_NAME).write_bytes(
        build_worker_bundle.csv_bytes(READING_HEADER, rows)
    )

    with pytest.raises(merge.MergeError, match="stale reading-input projection"):
        merge.prepare_merge(bundle, goal_dir=goal)


def test_existing_global_id_collision_is_rejected(tmp_path: Path) -> None:
    bundle = _completed_bundle(tmp_path)
    goal = _copy_global_state(tmp_path)
    (goal / merge.CANDIDATE_NAME).write_text(
        '{"id":"B0001"}\n{"id":"B0001"}\n',
        encoding="utf-8",
    )

    with pytest.raises(merge.MergeError, match="candidate ID collision"):
        merge.prepare_merge(bundle, goal_dir=goal)


def test_later_initial_stage_requires_all_prior_stage_gates(
    tmp_path: Path,
) -> None:
    bundle = _completed_no_construction_bundle(
        tmp_path,
        stage=5,
        assignment_path=STAGE_5_PATH,
    )
    goal = _copy_global_state(tmp_path)

    with pytest.raises(
        merge.MergeError,
        match="stage 5 merge prerequisites failed",
    ):
        merge.prepare_merge(bundle, goal_dir=goal)


def test_stage_five_notes_cannot_merge_before_main_chapter(
    tmp_path: Path,
) -> None:
    bundle = _completed_no_construction_bundle(
        tmp_path,
        stage=5,
        assignment_path=STAGE_5_NOTES_PATH,
    )
    goal = _copy_global_state(tmp_path)

    with pytest.raises(
        merge.MergeError,
        match="earlier canonical document .* remains pending",
    ):
        merge.prepare_merge(bundle, goal_dir=goal)


def test_bundle_rejects_mixed_pending_and_reviewed_projection(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    goal = _goal_after_initial_merge(tmp_path)
    monkeypatch.setattr(build_worker_bundle, "GOAL_DIR", goal)
    with pytest.raises(
        ValueError,
        match="uniformly PENDING or uniformly REVIEWED/SCREENED",
    ):
        build_worker_bundle.build_bundle(
            tmp_path / "mixed-bundle",
            "mixed-projection-worker",
            4,
            [
                ASSIGNMENT_PATH,
                "BACK-MATTER/NOTES/00-General-Notes.md",
            ],
            epoch=1,
        )


def test_bundle_rejects_invalid_path_mixed_with_valid_assignment(
    tmp_path: Path,
) -> None:
    with pytest.raises(ValueError, match="OUTSIDE.md"):
        build_worker_bundle.build_bundle(
            tmp_path / "invalid-path-bundle",
            "invalid-path-worker",
            4,
            [FIRST_STAGE_4_PATH, "OUTSIDE.md"],
            epoch=1,
        )


def test_epoch_two_reopen_retains_provenance_and_appends_ids(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    goal = _goal_after_initial_merge(tmp_path)
    _add_local_closure(
        goal,
        epoch=1,
        stage=4,
        source_paths=INITIAL_STAGE_4_PREFIX,
    )
    monkeypatch.setattr(build_worker_bundle, "GOAL_DIR", goal)
    bundle = _completed_bundle(
        tmp_path / "reopened",
        epoch=2,
        worker_id="merge-reopen-worker",
    )
    search_before = json.loads(
        (goal / merge.SEARCH_NAME).read_text(encoding="utf-8")
    )

    plan = merge.prepare_merge(bundle, goal_dir=goal)
    preview = plan.preview()
    assert preview["discovery_epoch"] == 2
    assert preview["review_ids"] == ["V000003"]
    assert preview["review_mode"] == "REOPEN"
    assert preview["search_ledger_preserved"] is True
    assert preview["search_fixed_point_cleared"] is True
    assert plan.candidate_ids == {"W0001": "B0002"}
    assert plan.route_ids == {"WR0001": "R000002"}
    assert plan.evidence_ids == {
        "WE000001": "E000003",
        "WE000002": "E000004",
    }
    merge.apply_merge(plan)

    candidates = merge._read_jsonl(goal / merge.CANDIDATE_NAME)
    routes = merge._read_csv(
        goal / merge.ROUTE_NAME,
        merge.CROSS_REFERENCE_HEADER,
    )
    reading = merge._read_csv(goal / merge.READING_NAME, READING_HEADER)
    assets = merge._read_csv(goal / merge.ASSET_NAME, ASSET_HEADER)
    assert [row["id"] for row in candidates] == ["B0001", "B0002"]
    assert [row["route_id"] for row in routes] == ["R000001", "R000002"]
    source_unit_id = candidates[0]["source_unit_ids"][0]
    image_path = candidates[0]["image_witnesses"][0]
    assert json.loads(
        next(
            row["candidate_ids"]
            for row in reading
            if row["source_unit_id"] == source_unit_id
        )
    ) == ["B0001", "B0002"]
    reopened_asset = next(
        row for row in assets if row["physical_path"] == image_path
    )
    assert json.loads(reopened_asset["candidate_ids"]) == ["B0001", "B0002"]
    assert json.loads(reopened_asset["route_ids"]) == ["R000001", "R000002"]
    search_after = json.loads(
        (goal / merge.SEARCH_NAME).read_text(encoding="utf-8")
    )
    assert search_after["fixed_point"] is None
    assert search_after["rounds"] == search_before["rounds"]
    assert search_after["vocabulary"] == search_before["vocabulary"]
    history = merge._read_jsonl(goal / merge.REVIEW_HISTORY_NAME)
    assert [event["review_id"] for event in history] == [
        "V000001",
        "V000002",
        "V000003",
    ]
    assert [event["epoch"] for event in history] == [1, 1, 2]
    assert history[2]["previous_event_sha256"] == history[1]["event_sha256"]


def test_epoch_two_reopen_requires_current_epoch_local_search_closure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    goal = _goal_after_initial_merge(tmp_path)
    monkeypatch.setattr(build_worker_bundle, "GOAL_DIR", goal)
    bundle = _completed_bundle(
        tmp_path / "reopened",
        epoch=2,
        worker_id="merge-unclosed-reopen-worker",
    )

    with pytest.raises(
        merge.MergeError,
        match="LOCAL search scopes are not closed",
    ):
        merge.prepare_merge(bundle, goal_dir=goal)


def test_same_path_can_reopen_again_at_epoch_three_after_epoch_two_closure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    goal = _goal_after_initial_merge(tmp_path)
    _add_local_closure(
        goal,
        epoch=1,
        stage=4,
        source_paths=INITIAL_STAGE_4_PREFIX,
    )
    monkeypatch.setattr(build_worker_bundle, "GOAL_DIR", goal)
    epoch_two = _completed_bundle(
        tmp_path / "epoch-two",
        epoch=2,
        worker_id="repeat-reopen-epoch-two",
    )
    merge.apply_merge(merge.prepare_merge(epoch_two, goal_dir=goal))
    _add_local_closure(
        goal,
        epoch=2,
        stage=4,
        source_paths=[ASSIGNMENT_PATH],
    )

    epoch_three = _completed_bundle(
        tmp_path / "epoch-three",
        epoch=3,
        worker_id="repeat-reopen-epoch-three",
    )
    plan = merge.prepare_merge(epoch_three, goal_dir=goal)
    assert plan.discovery_epoch == 3
    assert plan.review_ids == ("V000005",)
    merge.apply_merge(plan)

    history = merge._read_jsonl(goal / merge.REVIEW_HISTORY_NAME)
    assert [event["epoch"] for event in history] == [1, 1, 2, 2, 3]
    assert [event["source_paths"] for event in history] == [
        INITIAL_STAGE_4_PREFIX,
        [],
        [ASSIGNMENT_PATH],
        [],
        [ASSIGNMENT_PATH],
    ]
    assert history[4]["previous_event_sha256"] == history[3]["event_sha256"]


def test_pending_stage_five_forward_merge_uses_active_epoch_two(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest = json.loads(
        (merge.GOAL_DIR / merge.MANIFEST_NAME).read_text(encoding="utf-8")
    )
    stage_four_paths = build_worker_bundle.ordered_stage_paths(manifest, 4)
    initial_bundle = _completed_no_construction_bundle(
        tmp_path / "initial-stage-four",
        stage=4,
        assignment_paths=stage_four_paths,
        worker_id="complete-stage-four",
    )
    goal = _copy_global_state(tmp_path / "state")
    merge.apply_merge(merge.prepare_merge(initial_bundle, goal_dir=goal))
    _add_local_closure(
        goal,
        epoch=1,
        stage=4,
        source_paths=stage_four_paths,
    )

    monkeypatch.setattr(build_worker_bundle, "GOAL_DIR", goal)
    reopened_bundle = _completed_no_construction_bundle(
        tmp_path / "reopen-stage-four",
        stage=4,
        assignment_path=ASSIGNMENT_PATH,
        epoch=2,
        worker_id="reopen-stage-four",
    )
    merge.apply_merge(merge.prepare_merge(reopened_bundle, goal_dir=goal))
    _add_local_closure(
        goal,
        epoch=2,
        stage=4,
        source_paths=[ASSIGNMENT_PATH],
    )

    stage_five_bundle = _completed_no_construction_bundle(
        tmp_path / "forward-stage-five",
        stage=5,
        assignment_path=STAGE_5_PATH,
        epoch=2,
        worker_id="forward-stage-five-at-active-epoch",
    )
    plan = merge.prepare_merge(stage_five_bundle, goal_dir=goal)
    assert plan.review_mode == "INITIAL"
    assert plan.discovery_epoch == 2
    assert plan.review_ids == ("V000005",)
    merge.apply_merge(plan)

    history = merge._read_jsonl(goal / merge.REVIEW_HISTORY_NAME)
    assert [event["review_id"] for event in history] == [
        "V000001",
        "V000002",
        "V000003",
        "V000004",
        "V000005",
    ]
    assert [event["epoch"] for event in history] == [1, 1, 2, 2, 2]
    assert history[-1]["mode"] == "INITIAL"
    assert history[-1]["source_paths"] == [STAGE_5_PATH]


def test_reopen_epoch_must_be_next_global_epoch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    goal = _goal_after_initial_merge(tmp_path)
    monkeypatch.setattr(build_worker_bundle, "GOAL_DIR", goal)
    bundle = _completed_bundle(
        tmp_path / "reopened",
        epoch=3,
        worker_id="merge-skipped-epoch-worker",
    )

    with pytest.raises(
        merge.MergeError,
        match="epoch 3 is not the next review epoch 2",
    ):
        merge.prepare_merge(bundle, goal_dir=goal)


def test_initial_forward_merge_cannot_skip_active_epoch_one(
    tmp_path: Path,
) -> None:
    bundle = _completed_no_construction_bundle(
        tmp_path / "reopened",
        stage=4,
        assignment_path=FIRST_STAGE_4_PATH,
        epoch=2,
        worker_id="merge-premature-reopen-worker",
    )
    goal = _copy_global_state(tmp_path)

    with pytest.raises(
        merge.MergeError,
        match="differs from the active review epoch 1",
    ):
        merge.prepare_merge(bundle, goal_dir=goal)


def test_epoch_two_reopen_rejects_loss_of_existing_links(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    goal = _goal_after_initial_merge(tmp_path)
    monkeypatch.setattr(build_worker_bundle, "GOAL_DIR", goal)
    bundle = _completed_bundle(
        tmp_path / "reopened",
        epoch=2,
        worker_id="merge-lossy-reopen-worker",
    )
    output_path = bundle / "output" / "output.json"
    output = json.loads(output_path.read_text(encoding="utf-8"))
    source_unit_id = output["candidate_proposals"][0]["source_unit_ids"][0]
    update = next(
        row
        for row in output["reading_updates"]
        if row["source_unit_id"] == source_unit_id
    )
    update["candidate_ids"] = '["W0001"]'
    output_path.write_bytes(canonical_json_bytes(output))

    with pytest.raises(
        merge.MergeError,
        match="reopened pass must retain existing global links",
    ):
        merge.prepare_merge(bundle, goal_dir=goal)


def test_reopen_rejects_loss_of_prior_review_history(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    goal = _goal_after_initial_merge(tmp_path)
    monkeypatch.setattr(build_worker_bundle, "GOAL_DIR", goal)
    bundle = _completed_bundle(
        tmp_path / "reopened",
        epoch=2,
        worker_id="merge-history-loss-worker",
    )
    (goal / merge.REVIEW_HISTORY_NAME).write_bytes(b"")

    with pytest.raises(
        merge.MergeError,
        match="no authoritative prior review-history event",
    ):
        merge.prepare_merge(bundle, goal_dir=goal)


def test_epoch_two_reopen_rejects_stale_projection(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    authoritative_goal = _goal_after_initial_merge(tmp_path / "authoritative")
    monkeypatch.setattr(build_worker_bundle, "GOAL_DIR", authoritative_goal)
    bundle = _completed_bundle(
        tmp_path / "reopened",
        epoch=2,
        worker_id="merge-stale-reopen-worker",
    )
    target_goal = tmp_path / "target" / "goal-4"
    target_goal.parent.mkdir()
    shutil.copytree(authoritative_goal, target_goal)
    rows = _read_csv(target_goal / merge.READING_NAME)
    target = next(row for row in rows if row["path"] == ASSIGNMENT_PATH)
    target["evidence_statement"] = "Concurrent reopened-pass change."
    (target_goal / merge.READING_NAME).write_bytes(
        build_worker_bundle.csv_bytes(READING_HEADER, rows)
    )

    with pytest.raises(
        merge.MergeError,
        match="stale reading-input projection",
    ):
        merge.prepare_merge(bundle, goal_dir=target_goal)


def test_search_enrichment_default_dry_run_then_transactional_apply(
    tmp_path: Path,
) -> None:
    goal, proposal_path, unit_id, governed_hit_id = (
        _search_enrichment_fixture(tmp_path)
    )
    before = _transaction_state(goal)

    completed = subprocess.run(
        [
            sys.executable,
            str(TOOLS_DIR / "merge_worker_output.py"),
            "--search-append",
            str(proposal_path),
            "--goal-dir",
            str(goal),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    preview = json.loads(completed.stdout)
    assert preview["mode"] == "dry-run"
    assert preview["proposal_kind"] == "SEARCH_APPEND"
    assert preview["review_ids"] == ["V000002"]
    assert preview["trigger_hit_ids"] == [governed_hit_id]
    assert _transaction_state(goal) == before

    plan = merge.prepare_search_append(proposal_path, goal_dir=goal)
    merge.apply_merge(plan)
    reading = merge._read_csv(goal / merge.READING_NAME, READING_HEADER)
    row = next(item for item in reading if item["source_unit_id"] == unit_id)
    assert row["review_disposition"] == "CANDIDATE"
    assert json.loads(row["candidate_ids"]) == ["B0001"]
    candidates = merge._read_jsonl(goal / merge.CANDIDATE_NAME)
    assert [candidate["id"] for candidate in candidates] == ["B0001"]
    search = json.loads((goal / merge.SEARCH_NAME).read_text(encoding="utf-8"))
    assert [round_record["round_id"] for round_record in search["rounds"]] == [
        "S001"
    ]
    history = merge._read_jsonl(goal / merge.REVIEW_HISTORY_NAME)
    assert [event["mode"] for event in history] == [
        "INITIAL",
        "SEARCH_APPEND",
    ]
    enrichment = history[-1]
    assert len(enrichment["candidate_changes"]) == 1
    create = enrichment["candidate_changes"][0]
    assert create["action"] == "CREATE"
    assert create["candidate_id"] == "B0001"
    assert create["after_candidate"] == candidates[0]
    prior_path = next(
        change
        for change in history[0]["path_changes"]
        if change["source_path"] == ASSIGNMENT_PATH
    )
    assert enrichment["path_changes"][0][
        "previous_path_result_sha256"
    ] == prior_path["result_projection_sha256"]
    assert enrichment["path_changes"][0]["result_snapshot"][
        "source_path"
    ] == ASSIGNMENT_PATH


def test_route_resolution_default_dry_run_then_transactional_apply(
    tmp_path: Path,
) -> None:
    goal = _goal_after_initial_merge(tmp_path)
    routes = merge._read_csv(
        goal / merge.ROUTE_NAME,
        merge.CROSS_REFERENCE_HEADER,
    )
    assert len(routes) == 1
    update = dict(routes[0])
    target_unit_id = next(
        unit["id"]
        for unit in merge._read_jsonl(goal / merge.UNITS_NAME)
        if unit["path"] == ASSIGNMENT_PATH
    )
    update.update(
        {
            "status": "RESOLVED",
            "target_unit_ids": json.dumps(
                [target_unit_id],
                separators=(",", ":"),
            ),
            "attempts": '["Resolved against the reviewed Preface units."]',
        }
    )
    proposal = {
        "schema_version": 1,
        "proposal_kind": "ROUTE_RESOLUTION",
        "coordinator_id": "route-resolution-coordinator",
        "epoch": 1,
        "base_artifact_sha256": {
            name: hashlib.sha256((goal / name).read_bytes()).hexdigest()
            for name in merge.WRITE_NAMES
        },
        "route_updates": [update],
    }
    proposal_path = tmp_path / "route-resolution-proposal.json"
    proposal_path.write_bytes(canonical_json_bytes(proposal))
    before = _transaction_state(goal)

    completed = subprocess.run(
        [
            sys.executable,
            str(TOOLS_DIR / "merge_worker_output.py"),
            "--route-resolution",
            str(proposal_path),
            "--goal-dir",
            str(goal),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    preview = json.loads(completed.stdout)
    assert preview == {
        "changes": {
            "review_event_appends": 1,
            "route_updates": 1,
        },
        "coordinator_id": "route-resolution-coordinator",
        "epoch": 1,
        "goal_dir": str(goal.resolve()),
        "mode": "dry-run",
        "proposal": str(proposal_path.resolve()),
        "proposal_kind": "ROUTE_RESOLUTION",
        "review_ids": ["V000002"],
        "source_paths": [ASSIGNMENT_PATH],
        "stage": 4,
    }
    assert _transaction_state(goal) == before

    plan = merge.prepare_route_resolution(proposal_path, goal_dir=goal)
    merge.apply_merge(plan)
    resolved = merge._read_csv(
        goal / merge.ROUTE_NAME,
        merge.CROSS_REFERENCE_HEADER,
    )
    assert resolved == [update]
    history = merge._read_jsonl(goal / merge.REVIEW_HISTORY_NAME)
    assert [event["mode"] for event in history] == [
        "INITIAL",
        "ROUTE_RESOLUTION",
    ]
    event = history[-1]
    assert event["source_paths"] == [ASSIGNMENT_PATH]
    assert event["candidate_changes"] == []
    assert event["search_change"] is None
    assert event["route_changes"][0]["action"] == "UPDATE"
    assert event["route_changes"][0]["before_route"] == routes[0]
    assert event["route_changes"][0]["after_route"] == update


def test_missing_target_final_rejects_premature_review_and_search_state(
    closed_review_goal_template: Path,
    tmp_path: Path,
) -> None:
    partial_goal = _goal_after_initial_merge(tmp_path / "partial")
    partial_proposal, _ = _missing_route_proposal(
        partial_goal,
        tmp_path,
        filename="partial-missing-route.json",
    )
    with pytest.raises(
        merge.MergeError,
        match="requires complete sequential source review and asset screening",
    ):
        merge.prepare_route_resolution(
            partial_proposal,
            goal_dir=partial_goal,
        )

    no_local_goal = _copy_goal_template(
        closed_review_goal_template,
        tmp_path / "no-local",
    )
    history = merge._read_jsonl(
        no_local_goal / merge.REVIEW_HISTORY_NAME
    )
    history = [
        event for event in history if event["mode"] != "SEARCH_APPEND"
    ]
    search = json.loads(
        (no_local_goal / merge.SEARCH_NAME).read_text(encoding="utf-8")
    )
    search.update(
        {
            "tool_assumptions": [],
            "vocabulary": [],
            "rounds": [],
            "fixed_point": None,
        }
    )
    (no_local_goal / merge.REVIEW_HISTORY_NAME).write_bytes(
        merge._jsonl_bytes(history)
    )
    (no_local_goal / merge.SEARCH_NAME).write_bytes(
        canonical_json_bytes(search)
    )
    current_values = (
        json.loads(
            (no_local_goal / merge.MANIFEST_NAME).read_text(
                encoding="utf-8"
            )
        ),
        merge._read_jsonl(no_local_goal / merge.UNITS_NAME),
        merge._read_csv(
            no_local_goal / merge.READING_NAME,
            READING_HEADER,
        ),
        merge._read_jsonl(no_local_goal / merge.CANDIDATE_NAME),
        merge._read_csv(
            no_local_goal / merge.ROUTE_NAME,
            merge.CROSS_REFERENCE_HEADER,
        ),
        merge._read_csv(
            no_local_goal / merge.ASSET_NAME,
            ASSET_HEADER,
        ),
        search,
        history,
    )
    assert merge.validate_audit.validate_objects(*current_values) == []
    no_local_proposal, _ = _missing_route_proposal(
        no_local_goal,
        tmp_path,
        filename="no-local-missing-route.json",
    )
    with pytest.raises(
        merge.MergeError,
        match="requires exact LOCAL search closure",
    ):
        merge.prepare_route_resolution(
            no_local_proposal,
            goal_dir=no_local_goal,
        )

    no_saturation_goal = _copy_goal_template(
        closed_review_goal_template,
        tmp_path / "no-saturation",
    )
    no_saturation_proposal, _ = _missing_route_proposal(
        no_saturation_goal,
        tmp_path,
        filename="no-saturation-missing-route.json",
    )
    with pytest.raises(
        merge.MergeError,
        match="requires a Stage 18 SATURATION search round.*epoch 1",
    ):
        merge.prepare_route_resolution(
            no_saturation_proposal,
            goal_dir=no_saturation_goal,
        )

    partial_scope_goal = _copy_goal_template(
        closed_review_goal_template,
        tmp_path / "partial-saturation-scope",
    )
    partial_search_proposal, _ = _stage18_saturation_proposal(
        partial_scope_goal,
        tmp_path,
        filename="partial-scope-saturation.json",
        establish_fixed_point=False,
    )
    partial_payload = json.loads(
        partial_search_proposal.read_text(encoding="utf-8")
    )
    partial_round = partial_payload["proposed_search"]["rounds"][-1]
    partial_round["queries"][0]["scope_paths"].pop()
    partial_digest = merge.validate_audit.search_result_digest(
        partial_round
    )
    partial_round["result_digest"] = partial_digest
    partial_round["rerun_digest"] = partial_digest
    partial_search_proposal.write_bytes(
        canonical_json_bytes(partial_payload)
    )
    merge.apply_merge(
        merge.prepare_search_append(
            partial_search_proposal,
            goal_dir=partial_scope_goal,
        )
    )
    partial_route_proposal, _ = _missing_route_proposal(
        partial_scope_goal,
        tmp_path,
        filename="partial-scope-missing-route.json",
    )
    with pytest.raises(
        merge.MergeError,
        match="requires a Stage 18 SATURATION search round.*exact full-corpus scope",
    ):
        merge.prepare_route_resolution(
            partial_route_proposal,
            goal_dir=partial_scope_goal,
        )

    with pytest.raises(
        merge.MergeError,
        match="requires a Stage 18 SATURATION search round.*epoch 2",
    ):
        merge._validate_stage18_context_ready(
            label="MISSING_TARGET_FINAL",
            manifest={"documents": [{"path": "fixture.md"}]},
            history=[
                {
                    "mode": "INITIAL",
                    "stage": 4,
                    "epoch": 1,
                    "source_paths": ["fixture.md"],
                },
                {
                    "mode": "REOPEN",
                    "stage": 4,
                    "epoch": 2,
                    "source_paths": ["fixture.md"],
                },
            ],
            reading=[{"review_status": "REVIEWED"}],
            assets=[{"inspection_status": "SCREENED"}],
            search={
                "rounds": [
                    {
                        "kind": "LOCAL",
                        "owning_stage": 4,
                        "epoch": 1,
                        "queries": [{"scope_paths": ["fixture.md"]}],
                    },
                    {
                        "kind": "SATURATION",
                        "owning_stage": 18,
                        "epoch": 1,
                        "queries": [{"scope_paths": ["fixture.md"]}],
                    },
                    {
                        "kind": "LOCAL",
                        "owning_stage": 4,
                        "epoch": 2,
                        "queries": [{"scope_paths": ["fixture.md"]}],
                    },
                ]
            },
        )


def test_missing_target_final_reachable_after_review_and_local_closure(
    closed_review_goal_template: Path,
    tmp_path: Path,
) -> None:
    goal = _copy_goal_template(closed_review_goal_template, tmp_path)
    saturation_proposal, _ = _stage18_saturation_proposal(
        goal,
        tmp_path,
        filename="pre-route-saturation.json",
        establish_fixed_point=False,
    )
    merge.apply_merge(
        merge.prepare_search_append(
            saturation_proposal,
            goal_dir=goal,
        )
    )
    proposal_path, expected_update = _missing_route_proposal(
        goal,
        tmp_path,
        filename="completed-missing-route.json",
    )
    search_before = (goal / merge.SEARCH_NAME).read_bytes()
    assert json.loads(search_before)["fixed_point"] is None
    before = _transaction_state(goal)

    completed = subprocess.run(
        [
            sys.executable,
            str(TOOLS_DIR / "merge_worker_output.py"),
            "--route-resolution",
            str(proposal_path),
            "--goal-dir",
            str(goal),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    preview = json.loads(completed.stdout)
    assert preview["mode"] == "dry-run"
    assert preview["proposal_kind"] == "ROUTE_RESOLUTION"
    assert preview["stage"] == 18
    assert preview["source_paths"] == [ASSIGNMENT_PATH]
    assert _transaction_state(goal) == before

    plan = merge.prepare_route_resolution(proposal_path, goal_dir=goal)
    merge.apply_merge(plan)
    assert (goal / merge.SEARCH_NAME).read_bytes() == search_before
    routes = merge._read_csv(
        goal / merge.ROUTE_NAME,
        merge.CROSS_REFERENCE_HEADER,
    )
    assert routes == [expected_update]
    history = merge._read_jsonl(goal / merge.REVIEW_HISTORY_NAME)
    event = history[-1]
    assert event["mode"] == "ROUTE_RESOLUTION"
    assert event["stage"] == 18
    assert event["source_paths"] == [ASSIGNMENT_PATH]
    assert event["route_changes"][0]["after_route"] == expected_update


def test_candidate_revision_default_dry_run_then_transactional_apply(
    closed_review_goal_template: Path,
    tmp_path: Path,
) -> None:
    goal = _copy_goal_template(closed_review_goal_template, tmp_path)
    candidates = merge._read_jsonl(goal / merge.CANDIDATE_NAME)
    assert len(candidates) == 1
    before_candidate = candidates[0]
    updated_candidate = copy.deepcopy(before_candidate)
    image_path = updated_candidate["image_witnesses"][0]
    updated_candidate["source_evidence"].append(
        {
            "evidence_id": "E000003",
            "evidence_group_id": "G000003",
            "discovery_anchor": {
                "epoch": 1,
                "kind": "IMAGE",
                "id": image_path,
                "ordinal": 2,
            },
            "source_unit_id": None,
            "image_path": image_path,
            "strength": "CONTEXTUAL",
            "modality": "IMAGE",
            "claim": "Stage 18 inspection adds a second governed image observation.",
            "fingerprint_fields": [],
        }
    )
    updated_candidate["evidence_strength"].append("CONTEXTUAL")
    proposal = {
        "schema_version": 1,
        "proposal_kind": "CANDIDATE_REVISION",
        "coordinator_id": "candidate-revision-coordinator",
        "epoch": 1,
        "base_artifact_sha256": {
            name: hashlib.sha256((goal / name).read_bytes()).hexdigest()
            for name in merge.WRITE_NAMES
        },
        "candidate_updates": [updated_candidate],
        "reading_updates": [],
        "asset_updates": [],
    }
    proposal_path = tmp_path / "candidate-revision-proposal.json"
    proposal_path.write_bytes(canonical_json_bytes(proposal))

    rewritten = copy.deepcopy(proposal)
    rewritten_candidate = rewritten["candidate_updates"][0]
    rewritten_candidate["source_evidence"] = [
        rewritten_candidate["source_evidence"][-1],
        *rewritten_candidate["source_evidence"][:-1],
    ]
    rewritten_path = tmp_path / "rewritten-candidate-provenance.json"
    rewritten_path.write_bytes(canonical_json_bytes(rewritten))
    with pytest.raises(
        merge.MergeError,
        match="source_evidence rewrites prior provenance",
    ):
        merge.prepare_candidate_revision(rewritten_path, goal_dir=goal)

    before = _transaction_state(goal)
    completed = subprocess.run(
        [
            sys.executable,
            str(TOOLS_DIR / "merge_worker_output.py"),
            "--candidate-revision",
            str(proposal_path),
            "--goal-dir",
            str(goal),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    preview = json.loads(completed.stdout)
    assert preview["mode"] == "dry-run"
    assert preview["proposal_kind"] == "CANDIDATE_REVISION"
    assert preview["stage"] == 18
    assert preview["source_paths"] == [ASSIGNMENT_PATH]
    assert preview["changes"] == {
        "asset_updates": 0,
        "candidate_appends": 0,
        "candidate_updates": 1,
        "reading_updates": 0,
        "review_event_appends": 1,
    }
    assert _transaction_state(goal) == before

    plan = merge.prepare_candidate_revision(proposal_path, goal_dir=goal)
    merge.apply_merge(plan)
    revised = merge._read_jsonl(goal / merge.CANDIDATE_NAME)
    assert revised == [updated_candidate]
    history = merge._read_jsonl(goal / merge.REVIEW_HISTORY_NAME)
    event = history[-1]
    assert event["mode"] == "CANDIDATE_REVISION"
    assert event["stage"] == 18
    assert event["source_paths"] == [ASSIGNMENT_PATH]
    assert event["path_changes"][0]["result_snapshot"] == history[0][
        "path_changes"
    ][1]["result_snapshot"]
    change = event["candidate_changes"][0]
    assert change["action"] == "UPDATE"
    assert change["before_candidate"] == before_candidate
    assert change["after_candidate"] == updated_candidate


def test_final_fixed_point_rejects_open_local_scope(
    closed_review_goal_template: Path,
    tmp_path: Path,
) -> None:
    goal = _copy_goal_template(closed_review_goal_template, tmp_path)
    history = [
        event
        for event in merge._read_jsonl(
            goal / merge.REVIEW_HISTORY_NAME
        )
        if event["mode"] != "SEARCH_APPEND"
    ]
    search = json.loads(
        (goal / merge.SEARCH_NAME).read_text(encoding="utf-8")
    )
    search.update(
        {
            "tool_assumptions": [],
            "vocabulary": [],
            "rounds": [],
            "fixed_point": None,
        }
    )
    (goal / merge.REVIEW_HISTORY_NAME).write_bytes(
        merge._jsonl_bytes(history)
    )
    (goal / merge.SEARCH_NAME).write_bytes(canonical_json_bytes(search))
    proposal_path, _ = _stage18_saturation_proposal(
        goal,
        tmp_path,
        filename="fixed-point-with-open-local-scope.json",
        establish_fixed_point=True,
    )

    with pytest.raises(
        merge.MergeError,
        match="fixed-point establishment requires exact LOCAL search closure",
    ):
        merge.prepare_search_append(proposal_path, goal_dir=goal)


def test_final_fixed_point_rejects_pending_routes_and_unreported_vocabulary(
    closed_review_goal_template: Path,
    tmp_path: Path,
) -> None:
    pending_goal = _copy_goal_template(
        closed_review_goal_template,
        tmp_path / "pending-route",
    )
    pending_proposal, _ = _stage18_saturation_proposal(
        pending_goal,
        tmp_path,
        filename="fixed-point-with-pending-route.json",
        establish_fixed_point=True,
    )
    with pytest.raises(
        merge.MergeError,
        match="requires all cross-reference routes to be terminal.*R000001",
    ):
        merge.prepare_search_append(
            pending_proposal,
            goal_dir=pending_goal,
        )

    vocabulary_goal = _copy_goal_template(
        closed_review_goal_template,
        tmp_path / "unreported-vocabulary",
    )
    route_proposal = _resolved_route_proposal(vocabulary_goal, tmp_path)
    merge.apply_merge(
        merge.prepare_route_resolution(
            route_proposal,
            goal_dir=vocabulary_goal,
        )
    )
    vocabulary_proposal, _ = _stage18_saturation_proposal(
        vocabulary_goal,
        tmp_path,
        filename="fixed-point-with-unreported-vocabulary.json",
        establish_fixed_point=True,
    )
    payload = json.loads(
        vocabulary_proposal.read_text(encoding="utf-8")
    )
    payload["proposed_search"]["vocabulary"].append(
        "unreported zero-delta alias"
    )
    vocabulary_proposal.write_bytes(canonical_json_bytes(payload))
    with pytest.raises(
        merge.MergeError,
        match="top-level vocabulary differs from exact ordered.*replay",
    ):
        merge.prepare_search_append(
            vocabulary_proposal,
            goal_dir=vocabulary_goal,
        )


def test_final_zero_hit_saturation_default_dry_run_then_apply(
    closed_review_goal_template: Path,
    tmp_path: Path,
) -> None:
    goal = _copy_goal_template(closed_review_goal_template, tmp_path)
    route_proposal = _resolved_route_proposal(goal, tmp_path)
    merge.apply_merge(
        merge.prepare_route_resolution(route_proposal, goal_dir=goal)
    )

    manifest = json.loads(
        (goal / merge.MANIFEST_NAME).read_text(encoding="utf-8")
    )
    ordered_documents = sorted(
        manifest["documents"],
        key=lambda document: (
            merge.validate_audit.stage_for_document(document),
            int(document["order"]),
        ),
    )
    search = json.loads(
        (goal / merge.SEARCH_NAME).read_text(encoding="utf-8")
    )
    round_record: dict[str, Any] = {
        "round_id": f"S{len(search['rounds']) + 1:03d}",
        "epoch": 1,
        "kind": "SATURATION",
        "owning_stage": 18,
        "queries": [
            {
                "query_id": (
                    f"Q{sum(len(item['queries']) for item in search['rounds']) + 1:04d}"
                ),
                "family": "zero-result final saturation fixture",
                "pattern": "__MERGE_COMPLETION_IMPOSSIBLE_MATCH_71A9C2__",
                "mode": "LITERAL",
                "case_sensitive": True,
                "whole_word": False,
                "scope_paths": [
                    document["path"] for document in ordered_documents
                ],
            }
        ],
        "tool_assumptions": [
            "Deterministic zero-result completion fixture."
        ],
        "result_ids": [],
        "result_digest": "",
        "hits": [],
        "new_vocabulary": [],
        "new_candidates": [],
        "new_evidence_groups": [],
        "new_routes": [],
        "rerun_digest": "",
    }
    digest = merge.validate_audit.search_result_digest(round_record)
    round_record["result_digest"] = digest
    round_record["rerun_digest"] = digest
    proposed_search = copy.deepcopy(search)
    proposed_search["rounds"].append(round_record)
    proposed_search["fixed_point"] = {
        "round_id": round_record["round_id"],
        "zero_delta": True,
        "rerun_reproduced": True,
        "result_digest": digest,
    }
    proposal = {
        "schema_version": 1,
        "proposal_kind": "SEARCH_APPEND",
        "coordinator_id": "final-saturation-coordinator",
        "epoch": 1,
        "source_paths": [],
        "base_artifact_sha256": {
            name: hashlib.sha256((goal / name).read_bytes()).hexdigest()
            for name in merge.WRITE_NAMES
        },
        "reading_updates": [],
        "asset_updates": [],
        "candidate_updates": [],
        "route_appends": [],
        "proposed_search": proposed_search,
    }
    proposal_path = tmp_path / "final-saturation-proposal.json"
    proposal_path.write_bytes(canonical_json_bytes(proposal))

    invalid = copy.deepcopy(proposal)
    invalid["proposed_search"]["fixed_point"]["zero_delta"] = False
    invalid_path = tmp_path / "invalid-final-saturation.json"
    invalid_path.write_bytes(canonical_json_bytes(invalid))
    with pytest.raises(
        merge.MergeError,
        match="fixed_point.*oneOf branch",
    ):
        merge.prepare_search_append(invalid_path, goal_dir=goal)

    before = _transaction_state(goal)
    completed = subprocess.run(
        [
            sys.executable,
            str(TOOLS_DIR / "merge_worker_output.py"),
            "--search-append",
            str(proposal_path),
            "--goal-dir",
            str(goal),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    preview = json.loads(completed.stdout)
    assert preview["mode"] == "dry-run"
    assert preview["proposal_kind"] == "SEARCH_APPEND"
    assert preview["source_paths"] == []
    assert preview["trigger_hit_ids"] == []
    assert preview["search_fixed_point_cleared"] is False
    assert preview["search_fixed_point_established"] is True
    assert _transaction_state(goal) == before

    plan = merge.prepare_search_append(proposal_path, goal_dir=goal)
    merge.apply_merge(plan)
    closed_search = json.loads(
        (goal / merge.SEARCH_NAME).read_text(encoding="utf-8")
    )
    assert closed_search["fixed_point"] == proposed_search["fixed_point"]
    values = (
        manifest,
        merge._read_jsonl(goal / merge.UNITS_NAME),
        merge._read_csv(goal / merge.READING_NAME, READING_HEADER),
        merge._read_jsonl(goal / merge.CANDIDATE_NAME),
        merge._read_csv(
            goal / merge.ROUTE_NAME,
            merge.CROSS_REFERENCE_HEADER,
        ),
        merge._read_csv(goal / merge.ASSET_NAME, ASSET_HEADER),
        closed_search,
        merge._read_jsonl(goal / merge.REVIEW_HISTORY_NAME),
    )
    assert merge.validate_audit.validate_objects(
        *values,
        require_stages={18},
        require_all_reviewed=True,
    ) == []


def test_search_enrichment_rejects_unauthorized_and_immutable_deltas(
    tmp_path: Path,
) -> None:
    goal, proposal_path, governed_unit_id, _ = _search_enrichment_fixture(
        tmp_path
    )
    base = json.loads(proposal_path.read_text(encoding="utf-8"))
    reading = merge._read_csv(goal / merge.READING_NAME, READING_HEADER)
    unrelated = next(
        row
        for row in reading
        if row["path"] == ASSIGNMENT_PATH
        and row["source_unit_id"] != governed_unit_id
    )
    assets = merge._read_csv(goal / merge.ASSET_NAME, ASSET_HEADER)
    prefaced_asset = next(
        row for row in assets if row["assignment_path"] == ASSIGNMENT_PATH
    )

    mutations: list[tuple[str, dict[str, Any], str]] = []
    no_hit = copy.deepcopy(base)
    unrelated_update = dict(unrelated)
    unrelated_update["evidence_statement"] = (
        "Changed without an authorizing search hit."
    )
    no_hit["reading_updates"].append(unrelated_update)
    mutations.append(("no-hit", no_hit, "without a new search hit"))

    completion = copy.deepcopy(base)
    completion["reading_updates"][0]["review_epoch"] = "2"
    mutations.append(("completion", completion, "completion/identity field"))

    visual = copy.deepcopy(base)
    asset_update = dict(prefaced_asset)
    asset_update["visual_role"] = "CONTROL"
    visual["asset_updates"] = [asset_update]
    mutations.append(("visual", visual, "visual/completion field"))

    unrelated_link = copy.deepcopy(base)
    unrelated_link["reading_updates"][0]["candidate_ids"] = (
        '["B0001","B9999"]'
    )
    mutations.append(
        ("unrelated-link", unrelated_link, "absent from its hit")
    )

    nonappend_search = copy.deepcopy(base)
    nonappend_search["proposed_search"]["rounds"].append(
        copy.deepcopy(nonappend_search["proposed_search"]["rounds"][0])
    )
    mutations.append(
        ("nonappend-search", nonappend_search, "append one")
    )

    stale = copy.deepcopy(base)
    stale["base_artifact_sha256"][merge.SEARCH_NAME] = "0" * 64
    mutations.append(("stale-prefix", stale, "digests are stale"))

    for name, mutation, message in mutations:
        path = tmp_path / f"{name}.json"
        path.write_bytes(canonical_json_bytes(mutation))
        with pytest.raises(merge.MergeError, match=message):
            merge.prepare_search_append(path, goal_dir=goal)


def test_search_enrichment_rejects_forbidden_coordinator_identity(
    tmp_path: Path,
) -> None:
    goal, proposal_path, _, _ = _search_enrichment_fixture(tmp_path)
    proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
    proposal["coordinator_id"] = "T03 reconciliation coordinator"
    forbidden = tmp_path / "forbidden-coordinator.json"
    forbidden.write_bytes(canonical_json_bytes(proposal))

    with pytest.raises(merge.MergeError, match="prohibited"):
        merge.prepare_search_append(forbidden, goal_dir=goal)


def test_search_append_rejects_declared_unchanged_snapshot_path(
    tmp_path: Path,
) -> None:
    goal, proposal_path, _, _ = _search_enrichment_fixture(tmp_path)
    proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
    proposal["source_paths"] = INITIAL_STAGE_4_PREFIX
    multi_path = tmp_path / "multi-path-enrichment.json"
    multi_path.write_bytes(canonical_json_bytes(proposal))

    with pytest.raises(
        merge.MergeError,
        match="source_paths must equal changed row/asset snapshots",
    ):
        merge.prepare_search_append(multi_path, goal_dir=goal)


def test_search_enrichment_rollback_restores_history_and_all_ledgers(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    goal, proposal_path, _, _ = _search_enrichment_fixture(tmp_path)
    plan = merge.prepare_search_append(proposal_path, goal_dir=goal)
    before = _transaction_state(goal)
    real_replace = merge.os.replace
    calls = 0

    def fail_before_history_replace(source: Path, target: Path) -> None:
        nonlocal calls
        calls += 1
        if calls == len(merge.WRITE_NAMES):
            raise OSError("injected enrichment history replacement failure")
        real_replace(source, target)

    monkeypatch.setattr(merge.os, "replace", fail_before_history_replace)
    with pytest.raises(
        merge.MergeError,
        match="recovery action=ROLLED_BACK_MIXED",
    ):
        merge.apply_merge(plan)

    assert _transaction_state(goal) == before
    assert _merge_staging_dirs(goal) == []


def test_search_enrichment_appends_evidence_to_existing_active_candidate(
    tmp_path: Path,
) -> None:
    goal, first_proposal, first_unit_id, _ = _search_enrichment_fixture(
        tmp_path
    )
    merge.apply_merge(
        merge.prepare_search_append(first_proposal, goal_dir=goal)
    )
    units = merge._read_jsonl(goal / merge.UNITS_NAME)
    query = {
        "query_id": "Q0002",
        "family": "second construction lead phrase",
        "pattern": "This book is the culmination of nearly twenty years of work",
        "mode": "LITERAL",
        "case_sensitive": True,
        "whole_word": False,
        "scope_paths": INITIAL_STAGE_4_PREFIX,
    }
    pairs, errors = merge.validate_audit.execute_frozen_queries(
        [query],
        units,
        merge.validate_audit.REPO_ROOT
        / "ref"
        / "A-New-Kind-of-Science",
    )
    assert errors == []
    target_ids = {
        unit["id"] for unit in units if unit["path"] == ASSIGNMENT_PATH
    }
    unit_id = next(
        found_unit_id
        for _, found_unit_id in pairs
        if found_unit_id in target_ids and found_unit_id != first_unit_id
    )
    search = json.loads((goal / merge.SEARCH_NAME).read_text(encoding="utf-8"))
    prior_hit_count = sum(
        len(round_record["hits"]) for round_record in search["rounds"]
    )
    hit_id = f"H{prior_hit_count + 1:06d}"
    unit_by_id = {unit["id"]: unit for unit in units}
    hit = {
        "hit_id": hit_id,
        "query_id": "Q0002",
        "source_unit_id": unit_id,
        "context_sha256": unit_by_id[unit_id]["sha256"],
        "disposition": "GOVERNED_CANDIDATE_OR_SUPPORT",
        "candidate_ids": ["B0001"],
        "route_ids": [],
        "rationale": "The hit adds evidence to the existing candidate.",
    }
    round_record = {
        "round_id": "S002",
        "epoch": 1,
        "kind": "LOCAL",
        "owning_stage": 4,
        "queries": [query],
        "tool_assumptions": ["Literal UTF-8 source-unit search."],
        "result_ids": [hit_id],
        "result_digest": "",
        "hits": [hit],
        "new_vocabulary": [],
        "new_candidates": [],
        "new_evidence_groups": ["G000002"],
        "new_routes": [],
        "rerun_digest": "",
    }
    digest = merge.validate_audit.search_result_digest(round_record)
    round_record["result_digest"] = digest
    round_record["rerun_digest"] = digest
    proposed_search = copy.deepcopy(search)
    proposed_search["rounds"].append(round_record)
    proposed_search["fixed_point"] = None

    reading = merge._read_csv(goal / merge.READING_NAME, READING_HEADER)
    row = next(item for item in reading if item["source_unit_id"] == unit_id)
    reading_update = dict(row)
    reading_update.update(
        {
            "review_disposition": "SUPPORTS_CANDIDATE",
            "candidate_ids": '["B0001"]',
            "evidence_statement": "The second LOCAL hit supports B0001.",
        }
    )
    candidate = copy.deepcopy(
        merge._read_jsonl(goal / merge.CANDIDATE_NAME)[0]
    )
    candidate["source_unit_ids"].append(unit_id)
    candidate["source_evidence"].append(
        {
            "evidence_id": "E000002",
            "evidence_group_id": "G000002",
            "discovery_anchor": {
                "epoch": 1,
                "kind": "SEARCH_HIT",
                "id": hit_id,
                "ordinal": 1,
            },
            "source_unit_id": unit_id,
            "image_path": None,
            "strength": "CORROBORATING",
            "modality": "PROSE",
            "claim": "The second hit corroborates the existing candidate.",
            "fingerprint_fields": [],
        }
    )
    candidate["evidence_strength"].append("CORROBORATING")
    proposal = {
        "schema_version": 1,
        "proposal_kind": "SEARCH_APPEND",
        "coordinator_id": "second-search-enrichment-coordinator",
        "epoch": 1,
        "source_paths": [ASSIGNMENT_PATH],
        "base_artifact_sha256": {
            name: hashlib.sha256((goal / name).read_bytes()).hexdigest()
            for name in merge.WRITE_NAMES
        },
        "reading_updates": [reading_update],
        "asset_updates": [],
        "candidate_updates": [candidate],
        "route_appends": [],
        "proposed_search": proposed_search,
    }
    proposal_path = tmp_path / "existing-candidate-enrichment.json"
    proposal_path.write_bytes(canonical_json_bytes(proposal))

    inserted = copy.deepcopy(proposal)
    inserted["candidate_updates"][0]["source_unit_ids"] = [
        unit_id,
        first_unit_id,
    ]
    inserted_path = tmp_path / "inserted-provenance-enrichment.json"
    inserted_path.write_bytes(canonical_json_bytes(inserted))
    with pytest.raises(
        merge.MergeError,
        match="deletes or rewrites prior provenance",
    ):
        merge.prepare_search_append(inserted_path, goal_dir=goal)

    plan = merge.prepare_search_append(proposal_path, goal_dir=goal)
    assert plan.candidate_update_count == 1
    assert plan.candidate_append_count == 0
    merge.apply_merge(plan)
    updated = merge._read_jsonl(goal / merge.CANDIDATE_NAME)[0]
    assert [
        item["evidence_id"] for item in updated["source_evidence"]
    ] == ["E000001", "E000002"]
    assert merge._existing_evidence_sequences([updated]) == (
        ["E000001", "E000002"],
        ["G000001", "G000002"],
    )
    history = merge._read_jsonl(goal / merge.REVIEW_HISTORY_NAME)
    prior_create = history[-2]["candidate_changes"][0]
    update = history[-1]["candidate_changes"][0]
    assert update["action"] == "UPDATE"
    assert update["candidate_id"] == "B0001"
    assert update["previous_candidate_result_sha256"] == prior_create[
        "after_candidate_sha256"
    ]
    assert update["before_candidate"] == prior_create["after_candidate"]
    assert update["before_candidate_sha256"] == prior_create[
        "after_candidate_sha256"
    ]
    assert update["after_candidate"] == updated
