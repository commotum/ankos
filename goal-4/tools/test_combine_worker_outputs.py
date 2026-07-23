from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Any

import pytest


TOOLS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_DIR))

import build_worker_bundle  # noqa: E402
import combine_worker_outputs as combine  # noqa: E402
import initialize_audit  # noqa: E402
import merge_worker_output as merge  # noqa: E402
import prepare_review_output as prepare  # noqa: E402
from audit_contract import (  # noqa: E402
    ASSET_HEADER,
    CANDIDATE_FIELDS,
    FINGERPRINT_FIELDS,
    READING_HEADER,
    canonical_json_bytes,
)


FIRST_PATH = "FRONT-MATTER/00-Publication-and-Contents.md"
SECOND_PATH = "FRONT-MATTER/01-Preface.md"


def _fresh_goal(root: Path) -> Path:
    goal = root / "goal-4"
    goal.mkdir(parents=True)
    initialized = {
        path.name: payload
        for path, payload in initialize_audit.expected_artifacts().items()
        if path.parent == merge.GOAL_DIR
    }
    for name in merge.SNAPSHOT_NAMES:
        source = merge.GOAL_DIR / name
        target = goal / name
        if name in merge.WRITE_NAMES:
            target.write_bytes(initialized[name])
            shutil.copymode(source, target)
        else:
            shutil.copy2(source, target)
    shutil.copytree(merge.GOAL_DIR / "schemas", goal / "schemas")
    return goal


def _json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _scaffold(bundle: Path) -> None:
    manifest = prepare.load_manifest(bundle)
    reading = prepare.load_csv_exact(
        bundle / "input" / "reading-input.csv",
        READING_HEADER,
        "test reading input",
    )
    assets = prepare.load_csv_exact(
        bundle / "input" / "asset-input.csv",
        ASSET_HEADER,
        "test asset input",
    )
    template = prepare.expected_template(bundle, manifest)
    proposed = prepare.scaffold_output(template, reading, assets)
    output_path = bundle / "output" / "output.json"
    original = output_path.read_bytes()
    prepare.atomic_replace(
        output_path,
        canonical_json_bytes(proposed),
        original,
    )


def _candidate(
    source_unit_id: str,
    *,
    stage: int,
    epoch: int,
    name: str,
) -> dict[str, Any]:
    missing = "The test evidence does not state further native mechanics."
    field_support = {
        field: "UNKNOWN_FROM_SOURCE" for field in FINGERPRINT_FIELDS
    }
    field_support["object_kind"] = "SUPPORTED"
    fingerprint = {
        field: {
            "status": "UNKNOWN_FROM_SOURCE",
            "value": None,
            "evidence_ids": [],
            "reason": missing,
        }
        for field in FINGERPRINT_FIELDS
    }
    fingerprint["object_kind"] = {
        "status": "SUPPORTED",
        "value": "test construction",
        "evidence_ids": ["WE000001"],
        "reason": "The assigned source identifies a construction.",
    }
    values: dict[str, Any] = {
        "id": "W0001",
        "record_status": "ACTIVE",
        "provisional_name": name,
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
                "claim": "The assigned source unit supplies a construction lead.",
                "fingerprint_fields": ["object_kind"],
            }
        ],
        "source_status": ["CLEAR"],
        "image_witnesses": [],
        "evidence_strength": ["LEAD_ONLY"],
        "field_support": field_support,
        "fingerprint": fingerprint,
        "parameters": [
            {
                "name": "test parameter",
                "source_description": "The source supplies a test parameter.",
                "evidence_ids": ["WE000001"],
            }
        ],
        "variants": [
            {
                "name": "test variant",
                "source_description": "The source supplies a test variant.",
                "evidence_ids": ["WE000001"],
            }
        ],
        "missing_mechanics": [missing],
        "uncertainties": [],
        "related_candidate_ids": [
            {
                "candidate_id": "W0001",
                "relation": "SOURCE_COMPARE",
                "proof_kind": "PROVISIONAL_COMPARISON",
                "evidence_ids": ["WE000001"],
                "before_rationale": "The worker retained the source comparison.",
                "after_rationale": "The union must retain the source comparison.",
                "uncertainty": "The comparison remains provisional.",
            }
        ],
        "cross_reference_ids": ["WR0001"],
        "evidence_reassignments": [],
    }
    return {field: values[field] for field in CANDIDATE_FIELDS}


def _route(source_unit_id: str, *, stage: int, epoch: int) -> dict[str, str]:
    return {
        "route_id": "WR0001",
        "source_unit_id": source_unit_id,
        "source_asset_id": "",
        "discovery_epoch": str(epoch),
        "discovery_kind": "SOURCE_UNIT",
        "discovery_id": source_unit_id,
        "discovery_ordinal": "1",
        "literal_target": "test target",
        "route_kind": "OTHER",
        "expected_topic": "test construction target",
        "owning_stage": str(stage),
        "closure_scope": "CROSS_RANGE",
        "status": "PENDING",
        "target_unit_ids": "[]",
        "target_asset_ids": "[]",
        "attempts": "[]",
        "vocabulary_terms": '["test construction"]',
        "defect_boundary": "",
    }


def _complete_sub_bundle(
    bundle: Path,
    *,
    goal: Path,
    candidate_name: str,
) -> str:
    manifest = prepare.load_manifest(bundle)
    stage = int(manifest["stage"])
    epoch = int(manifest["discovery_epoch"])
    worker = str(manifest["worker_id"])
    reading = prepare.load_csv_exact(
        bundle / "input" / "reading-input.csv",
        READING_HEADER,
        "test reading input",
    )
    assets = prepare.load_csv_exact(
        bundle / "input" / "asset-input.csv",
        ASSET_HEADER,
        "test asset input",
    )
    source_unit_id = reading[0]["source_unit_id"]
    output = _json(bundle / "output" / "output.json")
    reading_updates: list[dict[str, str]] = []
    for original in reading:
        is_anchor = original["source_unit_id"] == source_unit_id
        row = dict(original)
        row.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": str(epoch),
                "review_disposition": (
                    "CANDIDATE" if is_anchor else "NO_CONSTRUCTION"
                ),
                "source_status": "CLEAR",
                "uncertainty": "",
                "secondary_roles": "[]",
                "candidate_ids": '["W0001"]' if is_anchor else "[]",
                "route_ids": '["WR0001"]' if is_anchor else "[]",
                "evidence_statement": "Test source unit was explicitly reviewed.",
                "review_stage": str(stage),
                "reviewer": worker,
            }
        )
        reading_updates.append(
            {field: row[field] for field in READING_HEADER}
        )
    asset_updates: list[dict[str, str]] = []
    for original in assets:
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
                "candidate_ids": "[]",
                "route_ids": "[]",
                "evidence_statement": "Test asset was explicitly screened.",
                "review_stage": str(stage),
                "reviewer": worker,
                "uncertainty": "",
            }
        )
        asset_updates.append(
            {field: row[field] for field in ASSET_HEADER}
        )
    output.update(
        {
            "prohibited_input_nonuse": True,
            "reading_updates": reading_updates,
            "candidate_proposals": [
                _candidate(
                    source_unit_id,
                    stage=stage,
                    epoch=epoch,
                    name=candidate_name,
                )
            ],
            "asset_updates": asset_updates,
            "route_proposals": [
                _route(source_unit_id, stage=stage, epoch=epoch)
            ],
            "uncertainties": [f"{candidate_name} test uncertainty."],
        }
    )
    (bundle / "output" / "output.json").write_bytes(
        canonical_json_bytes(output)
    )
    assert build_worker_bundle.verify_bundle(
        bundle,
        require_completed_output=True,
        goal_dir=goal,
    ) == []
    return source_unit_id


def _fixture(root: Path) -> dict[str, Any]:
    goal = _fresh_goal(root / "state")
    first = root / "first"
    second = root / "second"
    union = root / "union"
    build_worker_bundle.build_bundle(
        first,
        "first-worker",
        4,
        [FIRST_PATH],
        epoch=1,
        goal_dir=goal,
    )
    build_worker_bundle.build_bundle(
        second,
        "second-worker",
        4,
        [SECOND_PATH],
        epoch=1,
        goal_dir=goal,
    )
    build_worker_bundle.build_bundle(
        union,
        "union-worker",
        4,
        [FIRST_PATH, SECOND_PATH],
        epoch=1,
        goal_dir=goal,
    )
    for bundle in (first, second, union):
        assert build_worker_bundle.verify_bundle(
            bundle,
            goal_dir=goal,
        ) == []
        _scaffold(bundle)
    first_source = _complete_sub_bundle(
        first,
        goal=goal,
        candidate_name="First test construction",
    )
    second_source = _complete_sub_bundle(
        second,
        goal=goal,
        candidate_name="Second test construction",
    )
    return {
        "goal": goal,
        "first": first,
        "second": second,
        "union": union,
        "first_source": first_source,
        "second_source": second_source,
    }


def test_combines_completed_disjoint_outputs_and_rewrites_every_join(
    tmp_path: Path,
) -> None:
    fixture = _fixture(tmp_path)
    summary = combine.combine_worker_outputs(
        [fixture["first"], fixture["second"]],
        fixture["union"],
        goal_dir=fixture["goal"],
    )

    assert summary.sub_bundle_count == 2
    assert summary.candidate_count == 2
    assert summary.evidence_count == 2
    assert summary.evidence_group_count == 2
    assert summary.route_count == 2

    output = _json(fixture["union"] / "output" / "output.json")
    assert output["prohibited_input_nonuse"] is False
    assert [row["id"] for row in output["candidate_proposals"]] == [
        "W0001",
        "W0002",
    ]
    assert [
        row["source_evidence"][0]["evidence_id"]
        for row in output["candidate_proposals"]
    ] == ["WE000001", "WE000002"]
    assert [
        row["source_evidence"][0]["evidence_group_id"]
        for row in output["candidate_proposals"]
    ] == ["WG000001", "WG000002"]
    assert [row["route_id"] for row in output["route_proposals"]] == [
        "WR0001",
        "WR0002",
    ]
    assert [
        row["cross_reference_ids"]
        for row in output["candidate_proposals"]
    ] == [["WR0001"], ["WR0002"]]
    assert [
        row["fingerprint"]["object_kind"]["evidence_ids"]
        for row in output["candidate_proposals"]
    ] == [["WE000001"], ["WE000002"]]
    assert [
        row["parameters"][0]["evidence_ids"]
        for row in output["candidate_proposals"]
    ] == [["WE000001"], ["WE000002"]]
    assert [
        row["variants"][0]["evidence_ids"]
        for row in output["candidate_proposals"]
    ] == [["WE000001"], ["WE000002"]]
    assert [
        row["related_candidate_ids"][0]["candidate_id"]
        for row in output["candidate_proposals"]
    ] == ["W0001", "W0002"]
    assert [
        row["related_candidate_ids"][0]["evidence_ids"]
        for row in output["candidate_proposals"]
    ] == [["WE000001"], ["WE000002"]]

    reading_by_id = {
        row["source_unit_id"]: row for row in output["reading_updates"]
    }
    assert reading_by_id[fixture["first_source"]]["candidate_ids"] == '["W0001"]'
    assert reading_by_id[fixture["first_source"]]["route_ids"] == '["WR0001"]'
    assert reading_by_id[fixture["second_source"]]["candidate_ids"] == '["W0002"]'
    assert reading_by_id[fixture["second_source"]]["route_ids"] == '["WR0002"]'
    assert {
        row["reviewer"] for row in output["reading_updates"]
    } == {"union-worker"}
    assert {
        row["review_stage"] for row in output["reading_updates"]
    } == {"4"}
    assert {
        row["reviewer"] for row in output["asset_updates"]
    } <= {"union-worker"}

    completed = json.loads(json.dumps(output))
    completed["prohibited_input_nonuse"] = True
    assert build_worker_bundle.verify_bundle(
        fixture["union"],
        require_completed_output=True,
        worker_output_override=completed,
        goal_dir=fixture["goal"],
    ) == []


def test_rejects_noncanonical_partition_without_mutating_union(
    tmp_path: Path,
) -> None:
    fixture = _fixture(tmp_path)
    output_path = fixture["union"] / "output" / "output.json"
    before = output_path.read_bytes()

    with pytest.raises(combine.CombineError, match="exact ordered partition"):
        combine.combine_worker_outputs(
            [fixture["second"], fixture["first"]],
            fixture["union"],
            goal_dir=fixture["goal"],
        )
    assert output_path.read_bytes() == before


def test_rejects_incomplete_input_and_nonpristine_union(
    tmp_path: Path,
) -> None:
    incomplete_fixture = _fixture(tmp_path / "incomplete")
    first_output_path = (
        incomplete_fixture["first"] / "output" / "output.json"
    )
    first_output = _json(first_output_path)
    first_output["prohibited_input_nonuse"] = False
    first_output_path.write_bytes(canonical_json_bytes(first_output))
    union_output_path = (
        incomplete_fixture["union"] / "output" / "output.json"
    )
    before = union_output_path.read_bytes()
    with pytest.raises(combine.CombineError, match="bundle verification failed"):
        combine.combine_worker_outputs(
            [
                incomplete_fixture["first"],
                incomplete_fixture["second"],
            ],
            incomplete_fixture["union"],
            goal_dir=incomplete_fixture["goal"],
        )
    assert union_output_path.read_bytes() == before

    dirty_fixture = _fixture(tmp_path / "dirty")
    dirty_output_path = dirty_fixture["union"] / "output" / "output.json"
    dirty = _json(dirty_output_path)
    dirty["reading_updates"][0]["evidence_statement"] = "Pre-existing work."
    dirty_output_path.write_bytes(canonical_json_bytes(dirty))
    dirty_bytes = dirty_output_path.read_bytes()
    with pytest.raises(combine.CombineError, match="pristine nonsemantic scaffold"):
        combine.combine_worker_outputs(
            [dirty_fixture["first"], dirty_fixture["second"]],
            dirty_fixture["union"],
            goal_dir=dirty_fixture["goal"],
        )
    assert dirty_output_path.read_bytes() == dirty_bytes


def test_requires_two_distinct_inputs_and_refuses_second_write(
    tmp_path: Path,
) -> None:
    fixture = _fixture(tmp_path)
    with pytest.raises(combine.CombineError, match="at least two"):
        combine.combine_worker_outputs(
            [fixture["first"]],
            fixture["union"],
            goal_dir=fixture["goal"],
        )
    with pytest.raises(combine.CombineError, match="must be distinct"):
        combine.combine_worker_outputs(
            [fixture["first"], fixture["first"]],
            fixture["union"],
            goal_dir=fixture["goal"],
        )

    combine.combine_worker_outputs(
        [fixture["first"], fixture["second"]],
        fixture["union"],
        goal_dir=fixture["goal"],
    )
    output_path = fixture["union"] / "output" / "output.json"
    authored = output_path.read_bytes()
    with pytest.raises(combine.CombineError, match="pristine nonsemantic scaffold"):
        combine.combine_worker_outputs(
            [fixture["first"], fixture["second"]],
            fixture["union"],
            goal_dir=fixture["goal"],
        )
    assert output_path.read_bytes() == authored
