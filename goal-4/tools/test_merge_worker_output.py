from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path
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
STAGE_5_PATH = "CHAPTERS/01-The-Foundations-for-a-New-Kind-of-Science.md"


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
        [ASSIGNMENT_PATH],
        epoch=epoch,
    )
    manifest = json.loads(
        (bundle / "allowed-manifest.json").read_text(encoding="utf-8")
    )
    reading = _read_csv(bundle / "input" / "reading-input.csv")
    assets = _read_csv(bundle / "input" / "asset-input.csv")
    assert reading
    assert len(assets) == 1
    source_unit_id = reading[0]["source_unit_id"]
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


def _completed_no_construction_bundle(
    root: Path,
    *,
    stage: int,
    assignment_path: str,
) -> Path:
    bundle = root / "bundle"
    worker_id = f"stage-{stage}-order-test"
    build_worker_bundle.build_bundle(
        bundle,
        worker_id,
        stage,
        [assignment_path],
        epoch=1,
    )
    reading_updates: list[dict[str, str]] = []
    for original in _read_csv(bundle / "input" / "reading-input.csv"):
        row = dict(original)
        row.update(
            {
                "review_status": "REVIEWED",
                "review_disposition": "NO_CONSTRUCTION",
                "source_status": "CLEAR",
                "secondary_roles": "[]",
                "candidate_ids": "[]",
                "route_ids": "[]",
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
                "visual_role": "DECORATIVE",
                "source_status": "CLEAR",
                "risk_flags": "[]",
                "original_resolution_status": "NOT_REQUIRED",
                "transcription_status": "NOT_REQUIRED",
                "candidate_ids": "[]",
                "route_ids": "[]",
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
        for name in (*merge.WRITE_NAMES, merge.SEARCH_NAME)
    }


def _goal_after_initial_merge(root: Path) -> Path:
    bundle = _completed_bundle(root / "initial")
    goal = _copy_global_state(root / "state")
    merge.apply_merge(merge.prepare_merge(bundle, goal_dir=goal))
    return goal


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


def test_apply_uses_validated_staged_ledgers_and_preserves_search(
    tmp_path: Path,
) -> None:
    bundle = _completed_bundle(tmp_path)
    goal = _copy_global_state(tmp_path)
    search_before = (goal / merge.SEARCH_NAME).read_bytes()

    plan = merge.prepare_merge(bundle, goal_dir=goal)
    merge.apply_merge(plan)

    assert (goal / merge.SEARCH_NAME).read_bytes() == search_before
    candidates = merge._read_jsonl(goal / merge.CANDIDATE_NAME)
    routes = merge._read_csv(
        goal / merge.ROUTE_NAME,
        merge.CROSS_REFERENCE_HEADER,
    )
    reading = merge._read_csv(goal / merge.READING_NAME, READING_HEADER)
    assets = merge._read_csv(goal / merge.ASSET_NAME, ASSET_HEADER)
    assert [row["id"] for row in candidates] == ["B0001"]
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


def test_bad_completed_bundle_is_rejected(tmp_path: Path) -> None:
    bundle = _completed_bundle(tmp_path)
    goal = _copy_global_state(tmp_path)
    output_path = bundle / "output" / "output.json"
    output = json.loads(output_path.read_text(encoding="utf-8"))
    output["prohibited_input_nonuse"] = False
    output_path.write_bytes(canonical_json_bytes(output))

    with pytest.raises(merge.MergeError, match="bundle verification failed"):
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


def test_epoch_two_reopen_retains_provenance_and_appends_ids(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    goal = _goal_after_initial_merge(tmp_path)
    monkeypatch.setattr(build_worker_bundle, "GOAL_DIR", goal)
    bundle = _completed_bundle(
        tmp_path / "reopened",
        epoch=2,
        worker_id="merge-reopen-worker",
    )

    plan = merge.prepare_merge(bundle, goal_dir=goal)
    assert plan.preview()["discovery_epoch"] == 2
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
