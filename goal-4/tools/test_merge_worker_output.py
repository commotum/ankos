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
    search_path.write_bytes(canonical_json_bytes(search))


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
    assert preview["review_ids"] == ["V000001", "V000002"]
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
    assert [event["review_id"] for event in history] == ["V000001", "V000002"]
    assert [event["source_paths"] for event in history] == [
        [FIRST_STAGE_4_PATH],
        [ASSIGNMENT_PATH],
    ]
    assert history[0]["previous_event_sha256"] is None
    assert history[1]["previous_event_sha256"] == history[0]["event_sha256"]
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


@pytest.mark.parametrize("failure_call", [2, 3, len(merge.WRITE_NAMES)])
def test_apply_pre_replace_failure_restores_bytes_modes_and_cleans_staging(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure_call: int,
) -> None:
    bundle = _completed_bundle(tmp_path)
    goal = _copy_global_state(tmp_path)
    plan = merge.prepare_merge(bundle, goal_dir=goal)
    before = _transaction_state(goal)
    real_replace = merge.os.replace
    calls = 0
    injected = OSError(f"failure before replace call {failure_call}")

    def fail_before_replace(source: Path, target: Path) -> None:
        nonlocal calls
        calls += 1
        if calls == failure_call:
            raise injected
        real_replace(source, target)

    monkeypatch.setattr(merge.os, "replace", fail_before_replace)
    with pytest.raises(OSError) as caught:
        merge.apply_merge(plan)

    assert caught.value is injected
    assert _transaction_state(goal) == before
    assert _merge_staging_dirs(goal) == []


@pytest.mark.parametrize("interrupt_call", [2, len(merge.WRITE_NAMES)])
def test_apply_replace_then_interrupt_restores_every_target_and_cleans_staging(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    interrupt_call: int,
) -> None:
    bundle = _completed_bundle(tmp_path)
    goal = _copy_global_state(tmp_path)
    plan = merge.prepare_merge(bundle, goal_dir=goal)
    before = _transaction_state(goal)
    real_replace = merge.os.replace
    calls = 0
    injected = InjectedTransactionInterrupt(
        "replacement committed before bookkeeping"
    )

    def replace_then_interrupt(source: Path, target: Path) -> None:
        nonlocal calls
        calls += 1
        real_replace(source, target)
        if calls == interrupt_call:
            raise injected

    monkeypatch.setattr(merge.os, "replace", replace_then_interrupt)
    with pytest.raises(InjectedTransactionInterrupt) as caught:
        merge.apply_merge(plan)

    assert caught.value is injected
    assert _transaction_state(goal) == before
    assert _merge_staging_dirs(goal) == []


def test_apply_final_verification_failure_rolls_back_bytes_and_modes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bundle = _completed_bundle(tmp_path)
    goal = _copy_global_state(tmp_path)
    plan = merge.prepare_merge(bundle, goal_dir=goal)
    before = _transaction_state(goal)
    real_replace = merge.os.replace
    calls = 0
    corrupt_target = goal / merge.CANDIDATE_NAME

    def corrupt_after_final_replace(source: Path, target: Path) -> None:
        nonlocal calls
        calls += 1
        real_replace(source, target)
        if calls == len(merge.WRITE_NAMES):
            corrupt_target.write_bytes(b"concurrent mutation\n")
            corrupt_target.chmod(0o600)

    monkeypatch.setattr(merge.os, "replace", corrupt_after_final_replace)
    with pytest.raises(
        merge.MergeError,
        match="applied ledger differs from staged bytes",
    ):
        merge.apply_merge(plan)

    assert _transaction_state(goal) == before
    assert _merge_staging_dirs(goal) == []


def test_apply_rollback_failure_retains_recovery_staging(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bundle = _completed_bundle(tmp_path)
    goal = _copy_global_state(tmp_path)
    plan = merge.prepare_merge(bundle, goal_dir=goal)
    real_replace = merge.os.replace
    calls = 0

    def fail_commit_then_rollback(source: Path, target: Path) -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("injected commit failure")
        if calls == 4:
            raise InjectedTransactionInterrupt("injected rollback failure")
        real_replace(source, target)

    monkeypatch.setattr(merge.os, "replace", fail_commit_then_rollback)
    with pytest.raises(
        merge.MergeError,
        match="rollback also failed",
    ) as caught:
        merge.apply_merge(plan)

    recovery_dirs = _merge_staging_dirs(goal)
    assert len(recovery_dirs) == 1
    assert str(recovery_dirs[0]) in str(caught.value)
    recovery_copy = recovery_dirs[0] / "old" / merge.CANDIDATE_NAME
    assert recovery_copy.read_bytes() == plan.original_bytes[merge.CANDIDATE_NAME]
    assert (
        recovery_copy.stat().st_mode & 0o777
    ) == plan.original_modes[merge.CANDIDATE_NAME]


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
    assert plan.review_ids == ("V000004",)
    merge.apply_merge(plan)

    history = merge._read_jsonl(goal / merge.REVIEW_HISTORY_NAME)
    assert [event["epoch"] for event in history] == [1, 1, 2, 3]
    assert [event["source_paths"] for event in history] == [
        [FIRST_STAGE_4_PATH],
        [ASSIGNMENT_PATH],
        [ASSIGNMENT_PATH],
        [ASSIGNMENT_PATH],
    ]
    assert history[3]["previous_event_sha256"] == history[2]["event_sha256"]


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
    assert plan.review_ids == ("V000006",)
    merge.apply_merge(plan)

    history = merge._read_jsonl(goal / merge.REVIEW_HISTORY_NAME)
    assert [event["review_id"] for event in history] == [
        "V000001",
        "V000002",
        "V000003",
        "V000004",
        "V000005",
        "V000006",
    ]
    assert [event["epoch"] for event in history] == [1, 1, 1, 1, 2, 2]
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
