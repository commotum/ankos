#!/usr/bin/env python3
"""Materialize the immutable Goal 4 Stage 2 baseline from raw inputs."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from baseline_lib import (
    LEGACY_RELATIVE,
    REPAIRED_RELATIVE,
    build_corpus_manifest,
    build_detector_artifacts,
    build_environment_snapshot,
    build_held_out_sample,
    build_image_reference_ledger,
    build_known_defect_rows,
    build_routing_baseline,
    git_command,
    jsonl_bytes,
    structure_ledger_rows,
)
from guardrail_lib import (
    GuardrailError,
    canonical_json_bytes,
    load_json,
    require,
    sha256_bytes,
    sha256_file,
    validate_exact_goal_output,
)


JSON_OUTPUTS = {
    "corpus-manifest.json",
    "routing-baseline.json",
    "held-out-sample.json",
    "baseline-detector-report.json",
    "baseline-environment.json",
    "baseline-lock.json",
}

JSONL_OUTPUTS = {
    "structure-ledger.jsonl",
    "image-reference-ledger.jsonl",
    "known-defect-regression.jsonl",
    "baseline-detector-hits.jsonl",
}


def atomic_write(path: Path, payload: bytes) -> None:
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    try:
        temporary.write_bytes(payload)
        os.chmod(temporary, 0o644)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def git_head(root: Path) -> str:
    return git_command(root, ["rev-parse", "HEAD"]).decode("ascii").strip()


def git_status(root: Path) -> bytes:
    return git_command(root, ["status", "--short", "--untracked-files=all"])


def build_lock(root: Path, output_root: Path) -> dict:
    artifact_names = sorted((JSON_OUTPUTS | JSONL_OUTPUTS) - {"baseline-lock.json"})
    tool_paths = [
        "goal-4/tools/baseline_lib.py",
        "goal-4/tools/capture_baseline.py",
        "goal-4/tests/test_baseline.py",
    ]
    for relative in tool_paths:
        require((root / relative).is_file(), f"baseline lock source is missing: {relative}")
    return {
        "artifacts": [
            {
                "byte_size": (output_root / name).stat().st_size,
                "path": f"goal-4/{name}",
                "sha256": sha256_file(output_root / name),
            }
            for name in artifact_names
        ],
        "bindings": {
            "compatibility_baseline_sha256": sha256_file(root / "goal-4/compatibility-baseline.json"),
            "guardrails_sha256": sha256_file(root / "goal-4/guardrails.json"),
            "legacy_git_tree": "52b84494ab310afd64762bf0983106414419655e",
            "quality_protocol_sha256": sha256_file(root / "goal-4/quality-evaluation.json"),
        },
        "schema_version": "1.0.0",
        "sources": [
            {
                "byte_size": (root / relative).stat().st_size,
                "path": relative,
                "sha256": sha256_file(root / relative),
            }
            for relative in tool_paths
        ],
        "status": "FROZEN_STAGE_2_BASELINE",
    }


def capture(root: Path) -> dict[str, str | int]:
    root = root.resolve(strict=True)
    output_root = root / "goal-4"
    require(output_root.is_dir() and not output_root.is_symlink(), "goal-4 output root is missing or aliased")
    for name in JSON_OUTPUTS | JSONL_OUTPUTS:
        validate_exact_goal_output(root, output_root / name, f"goal-4/{name}")
    require((root / LEGACY_RELATIVE).is_dir(), "legacy corpus is missing")
    repaired_sibling_absent_before = not (root / REPAIRED_RELATIVE).exists()
    require(repaired_sibling_absent_before, "Stage 2 may not create or census the repaired sibling")
    contract = load_json(root / "goal-4/guardrails.json")
    quality = load_json(root / "goal-4/quality-evaluation.json")
    head_before = git_head(root)
    status_before = git_status(root)

    manifest = build_corpus_manifest(root, contract)
    structure_rows, segments, blocks = structure_ledger_rows(root, contract)
    image_rows = build_image_reference_ledger(root, manifest, segments, blocks)
    routing = build_routing_baseline(root, manifest, image_rows)
    # The held-out set is deliberately materialized before detector or defect
    # output exists in this execution path.
    sample = build_held_out_sample(root, manifest, structure_rows, blocks, contract, quality)
    defects = build_known_defect_rows(root, manifest, segments, blocks, image_rows, routing)
    detector_hits, detector_report = build_detector_artifacts(
        root, manifest, segments, blocks, image_rows, routing, defects
    )

    payloads = {
        "corpus-manifest.json": canonical_json_bytes(manifest),
        "structure-ledger.jsonl": jsonl_bytes(structure_rows),
        "image-reference-ledger.jsonl": jsonl_bytes(image_rows),
        "routing-baseline.json": canonical_json_bytes(routing),
        "held-out-sample.json": canonical_json_bytes(sample),
        "known-defect-regression.jsonl": jsonl_bytes(defects),
        "baseline-detector-hits.jsonl": jsonl_bytes(detector_hits),
        "baseline-detector-report.json": canonical_json_bytes(detector_report),
    }
    for name in sorted(payloads):
        atomic_write(output_root / name, payloads[name])

    head_after_core = git_head(root)
    status_after_core = git_status(root)
    require(head_before == head_after_core, "Git HEAD moved during Stage 2 capture; rerun from a stable snapshot")
    manifest_after = build_corpus_manifest(root, contract)
    require(manifest == manifest_after, "legacy corpus changed during Stage 2 capture")
    repaired_sibling_absent_after = not (root / REPAIRED_RELATIVE).exists()
    require(repaired_sibling_absent_after, "repaired sibling appeared during Stage 2 capture")
    environment = build_environment_snapshot(
        root,
        manifest,
        manifest_after,
        status_before,
        status_after_core,
        head_before,
        head_after_core,
        repaired_sibling_absent_before,
        repaired_sibling_absent_after,
    )
    atomic_write(output_root / "baseline-environment.json", canonical_json_bytes(environment))
    lock = build_lock(root, output_root)
    atomic_write(output_root / "baseline-lock.json", canonical_json_bytes(lock))
    require(not (root / REPAIRED_RELATIVE).exists(), "repaired sibling appeared during Stage 2 capture")
    return {
        "artifact_count": len(lock["artifacts"]),
        "block_count": len(blocks),
        "defect_count": len(defects),
        "image_reference_count": len(image_rows),
        "lock_sha256": sha256_file(output_root / "baseline-lock.json"),
        "manifest_sha256": sha256_file(output_root / "corpus-manifest.json"),
        "sample_count": sample["selected_count"],
        "segment_count": len(segments),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    try:
        summary = capture(args.repo_root)
    except GuardrailError as error:
        print(f"BASELINE CAPTURE FAIL: {error}", file=sys.stderr)
        return 1
    print(
        "BASELINE CAPTURE OK "
        + " ".join(f"{key}={value}" for key, value in sorted(summary.items()))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
