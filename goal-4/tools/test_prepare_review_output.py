from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


TOOLS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_DIR))

import build_worker_bundle  # noqa: E402
import prepare_review_output as prepare  # noqa: E402
from audit_contract import ASSET_HEADER, READING_HEADER, canonical_json_bytes  # noqa: E402


PREFACE_PATH = "FRONT-MATTER/01-Preface.md"


def _build_bundle(
    root: Path,
    *,
    paths: list[str] | None = None,
    worker_id: str = "review-output-test-worker",
) -> Path:
    bundle = root / "bundle"
    build_worker_bundle.build_bundle(
        bundle,
        worker_id,
        4,
        paths or [],
        epoch=1,
    )
    assert build_worker_bundle.verify_bundle(bundle) == []
    return bundle


def _output(bundle: Path) -> dict:
    return json.loads(
        (bundle / "output" / "output.json").read_text(encoding="utf-8")
    )


def _write_output(bundle: Path, output: dict) -> None:
    (bundle / "output" / "output.json").write_bytes(
        canonical_json_bytes(output)
    )


def _complete_test_fixture(bundle: Path) -> None:
    output = _output(bundle)
    manifest = json.loads(
        (bundle / "allowed-manifest.json").read_text(encoding="utf-8")
    )
    worker_id = manifest["worker_id"]
    stage = str(manifest["stage"])
    epoch = str(manifest["discovery_epoch"])
    for row in output["reading_updates"]:
        row.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": epoch,
                "review_disposition": "NO_CONSTRUCTION",
                "source_status": "CLEAR",
                "uncertainty": "",
                "secondary_roles": "[]",
                "evidence_statement": "Test fixture row was explicitly reviewed.",
                "review_stage": stage,
                "reviewer": worker_id,
            }
        )
    for row in output["asset_updates"]:
        row.update(
            {
                "inspection_status": "SCREENED",
                "review_epoch": epoch,
                "visual_role": "DECORATIVE",
                "source_status": "CLEAR",
                "risk_flags": "[]",
                "original_resolution_status": "NOT_REQUIRED",
                "transcription_status": "NOT_REQUIRED",
                "evidence_statement": "Test fixture asset was explicitly screened.",
                "review_stage": stage,
                "reviewer": worker_id,
                "uncertainty": "",
            }
        )
    _write_output(bundle, output)


def test_stage4_scaffold_has_exact_assignment_and_no_semantic_defaults(
    tmp_path: Path,
) -> None:
    bundle = _build_bundle(tmp_path)
    original_reading = build_worker_bundle.read_csv(
        bundle / "input" / "reading-input.csv"
    )
    original_assets = build_worker_bundle.read_csv(
        bundle / "input" / "asset-input.csv"
    )

    changed, reading_count, asset_count = prepare.prepare(bundle)
    assert changed is True
    assert (reading_count, asset_count) == (157, 2)

    output = _output(bundle)
    assert output["prohibited_input_nonuse"] is False
    assert output["candidate_proposals"] == []
    assert output["route_proposals"] == []
    assert output["uncertainties"] == []
    assert len(output["reading_updates"]) == len(original_reading) == 157
    assert len(output["asset_updates"]) == len(original_assets) == 2

    reading_immutable = READING_HEADER[: READING_HEADER.index("review_status")]
    for scaffolded, original in zip(
        output["reading_updates"],
        original_reading,
        strict=True,
    ):
        assert set(scaffolded) == set(READING_HEADER)
        assert all(
            scaffolded[field] == original[field]
            for field in reading_immutable
        )
        assert scaffolded["review_status"] == "PENDING"
        assert scaffolded["review_epoch"] == ""
        assert scaffolded["review_disposition"] == ""
        assert scaffolded["source_status"] == ""
        assert scaffolded["secondary_roles"] == ""
        assert scaffolded["candidate_ids"] == original["candidate_ids"]
        assert scaffolded["route_ids"] == original["route_ids"]
        assert scaffolded["evidence_statement"] == ""
        assert scaffolded["review_stage"] == ""
        assert scaffolded["reviewer"] == ""
        assert scaffolded["uncertainty"] == ""

    asset_immutable = ASSET_HEADER[: ASSET_HEADER.index("inspection_status")]
    for scaffolded, original in zip(
        output["asset_updates"],
        original_assets,
        strict=True,
    ):
        assert set(scaffolded) == set(ASSET_HEADER)
        assert all(
            scaffolded[field] == original[field] for field in asset_immutable
        )
        assert scaffolded["inspection_status"] == "PENDING"
        assert scaffolded["review_epoch"] == ""
        assert scaffolded["visual_role"] == ""
        assert scaffolded["source_status"] == ""
        assert scaffolded["risk_flags"] == ""
        assert scaffolded["original_resolution_status"] == ""
        assert scaffolded["transcription_status"] == ""
        assert scaffolded["candidate_ids"] == original["candidate_ids"]
        assert scaffolded["route_ids"] == original["route_ids"]
        assert scaffolded["evidence_statement"] == ""
        assert scaffolded["review_stage"] == ""
        assert scaffolded["reviewer"] == ""
        assert scaffolded["uncertainty"] == ""

    errors, incomplete, finalized = prepare.check(bundle)
    assert errors == []
    assert len(incomplete) == 159
    assert finalized is False


def test_prepare_is_idempotent_and_resume_preserves_proved_row_work(
    tmp_path: Path,
) -> None:
    bundle = _build_bundle(tmp_path, paths=[PREFACE_PATH])
    changed, _, _ = prepare.prepare(bundle)
    assert changed is True
    output_path = bundle / "output" / "output.json"
    prepared_bytes = output_path.read_bytes()

    changed, _, _ = prepare.prepare(bundle)
    assert changed is False
    assert output_path.read_bytes() == prepared_bytes

    output = _output(bundle)
    first_id = output["reading_updates"][0]["source_unit_id"]
    output["reading_updates"][0]["evidence_statement"] = (
        "Explicit partial human work."
    )
    output["reading_updates"].pop()
    _write_output(bundle, output)
    partial_bytes = output_path.read_bytes()

    with pytest.raises(prepare.PreparationError, match="use --resume"):
        prepare.prepare(bundle)
    assert output_path.read_bytes() == partial_bytes

    changed, reading_count, asset_count = prepare.prepare(bundle, resume=True)
    assert changed is True
    resumed = _output(bundle)
    assert len(resumed["reading_updates"]) == reading_count
    assert len(resumed["asset_updates"]) == asset_count
    assert resumed["reading_updates"][0]["source_unit_id"] == first_id
    assert (
        resumed["reading_updates"][0]["evidence_statement"]
        == "Explicit partial human work."
    )
    assert resumed["reading_updates"][-1]["review_status"] == "PENDING"
    assert resumed["reading_updates"][-1]["evidence_statement"] == ""

    resumed_bytes = output_path.read_bytes()
    changed, _, _ = prepare.prepare(bundle, resume=True)
    assert changed is False
    assert output_path.read_bytes() == resumed_bytes
    assert not list(
        (bundle / "output").glob(".prepare-review-output-*.tmp")
    )


def test_resume_rejects_identity_changes_and_nonrow_semantic_work(
    tmp_path: Path,
) -> None:
    bundle = _build_bundle(tmp_path, paths=[PREFACE_PATH])
    prepare.prepare(bundle)
    output_path = bundle / "output" / "output.json"

    output = _output(bundle)
    output["reading_updates"][0]["unit_sha256"] = "0" * 64
    _write_output(bundle, output)
    tampered_bytes = output_path.read_bytes()
    with pytest.raises(prepare.PreparationError, match="immutable identity"):
        prepare.prepare(bundle, resume=True)
    assert output_path.read_bytes() == tampered_bytes

    prepare.atomic_replace(
        output_path,
        canonical_json_bytes(prepare.scaffold_output(
            prepare.expected_template(bundle, prepare.load_manifest(bundle)),
            build_worker_bundle.read_csv(bundle / "input" / "reading-input.csv"),
            build_worker_bundle.read_csv(bundle / "input" / "asset-input.csv"),
        )),
        tampered_bytes,
    )
    output = _output(bundle)
    output["candidate_proposals"] = [{}]
    _write_output(bundle, output)
    candidate_bytes = output_path.read_bytes()
    with pytest.raises(prepare.PreparationError, match="candidate_proposals"):
        prepare.prepare(bundle, resume=True)
    assert output_path.read_bytes() == candidate_bytes


def test_finalize_is_failure_safe_and_completed_verifier_compatible(
    tmp_path: Path,
) -> None:
    bundle = _build_bundle(tmp_path, paths=[PREFACE_PATH])
    prepare.prepare(bundle)
    output_path = bundle / "output" / "output.json"
    draft_bytes = output_path.read_bytes()

    with pytest.raises(prepare.PreparationError, match="remain incomplete"):
        prepare.finalize_declaration(bundle)
    assert output_path.read_bytes() == draft_bytes
    assert _output(bundle)["prohibited_input_nonuse"] is False

    _complete_test_fixture(bundle)
    errors, incomplete, finalized = prepare.check(bundle)
    assert errors == []
    assert incomplete == []
    assert finalized is False

    changed = prepare.finalize_declaration(bundle)
    assert changed is True
    assert _output(bundle)["prohibited_input_nonuse"] is True
    assert build_worker_bundle.verify_bundle(
        bundle,
        require_completed_output=True,
    ) == []

    finalized_bytes = output_path.read_bytes()
    changed = prepare.finalize_declaration(bundle)
    assert changed is False
    assert output_path.read_bytes() == finalized_bytes
    errors, incomplete, finalized = prepare.check(bundle)
    assert errors == []
    assert incomplete == []
    assert finalized is True


def test_check_cli_reports_incomplete_rows_without_writing(tmp_path: Path) -> None:
    bundle = _build_bundle(tmp_path, paths=[PREFACE_PATH])
    prepare.prepare(bundle)
    before = (bundle / "output" / "output.json").read_bytes()
    completed = subprocess.run(
        [
            sys.executable,
            str(TOOLS_DIR / "prepare_review_output.py"),
            str(bundle),
            "--check",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 1
    assert "INCOMPLETE: reading " in completed.stdout
    assert "assigned rows require human completion" in completed.stdout
    assert (bundle / "output" / "output.json").read_bytes() == before
