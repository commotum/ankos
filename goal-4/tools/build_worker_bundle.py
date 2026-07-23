#!/usr/bin/env python3
"""Build or verify a sealed, sanitized blind-discovery worker bundle."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

from audit_contract import (
    ASSET_HEADER,
    GOAL_DIR,
    READING_HEADER,
    REPO_ROOT,
    canonical_json_bytes,
)


SOURCE_ROOT = REPO_ROOT / "ref" / "A-New-Kind-of-Science"
FORBIDDEN_BRIEF_TERMS = [
    "T01",
    "T45",
    "SimpleProgram",
    "api fit",
    "runtime support",
    "existing catalog",
    "semantic family action",
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_bytes(header: list[str], rows: list[dict[str, str]]) -> bytes:
    import io

    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=header, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def stage_paths(manifest: dict[str, Any], stage: int) -> set[str]:
    paths: set[str] = set()
    for document in manifest["documents"]:
        kind = document["kind"]
        if stage == 4 and kind in {
            "publication_and_printed_contents",
            "preface",
            "general_notes",
            "colophon",
        }:
            paths.add(document["path"])
        elif 5 <= stage <= 16 and kind in {"chapter", "chapter_notes"}:
            if int(document["chapter_number"]) == stage - 4:
                paths.add(document["path"])
        elif stage == 17 and kind == "index":
            paths.add(document["path"])
    return paths


def sanitized_guardrails(guardrails: dict[str, Any]) -> dict[str, Any]:
    keep = [
        "schema_version",
        "phase",
        "candidate_capture_rule",
        "candidate_id_policy",
        "eligibility_criteria",
        "reading_dispositions",
        "reading_disposition_rules",
        "disposition_precedence",
        "blind_secondary_roles",
        "evidence_strengths",
        "evidence_application",
        "field_support_statuses",
        "source_statuses",
        "evidence_modalities",
        "visual_evidence_rule",
        "blind_candidate_fields",
        "candidate_record_statuses",
        "fingerprint_fields",
        "unknown_value_policy",
    ]
    result = {key: guardrails[key] for key in keep}
    result["candidate_id_policy"] = dict(result["candidate_id_policy"])
    result["candidate_id_policy"]["pattern"] = "^W[0-9]{4}$"
    result["candidate_id_policy"]["first_id"] = "W0001"
    result["candidate_id_policy"]["allocation_order"] = (
        "Worker-local canonical evidence order; the coordinator later assigns B IDs."
    )
    return result


def brief(worker_id: str, stage: int, paths: list[str]) -> str:
    listed = "\n".join(f"- `{path}`" for path in paths)
    return f"""# Blind Source Review

Worker: `{worker_id}`
Stage: `{stage}`

Read only the files in this bundle, in the exact source-unit order provided.
Do not search before completing sequential reading. Do not use outside
knowledge to fill missing mechanics, and do not decide implementation,
equivalence, reuse, or final taxonomy.

Assigned canonical documents:

{listed}

For every source unit:

1. Read the complete byte range and enough adjacent bundled context.
2. Return exactly one primary reading disposition and a separate source status.
3. Record concise evidence, secondary roles, local candidate links, and routes.
4. Err toward a worker-local `W####` candidate when both an identity anchor and
   semantic anchor may be present.
5. Fill every fingerprint field with supported, not-applicable, unknown, or
   conflicting status. Never invent a blank.
6. Review every assigned image at least as a thumbnail; require original
   resolution for construction-bearing, text-bearing, ambiguous, or
   caption-incomplete images.
7. Queue cross-range targets; do not follow anything outside the bundle.

Write only `output/output.json` and preserve every required hash/declaration.
Network use and access outside this bundle are prohibited. If the bundle lacks
needed evidence, record the missing target rather than guessing.
"""


def write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def build_bundle(
    output: Path,
    worker_id: str,
    stage: int,
    requested_paths: list[str],
) -> None:
    if output.exists():
        raise ValueError(f"output already exists: {output}")
    manifest = json.loads((GOAL_DIR / "corpus-manifest.json").read_text())
    guardrails = json.loads((GOAL_DIR / "guardrails.json").read_text())
    allowed_stage_paths = stage_paths(manifest, stage)
    paths = requested_paths or sorted(allowed_stage_paths)
    if not paths or set(paths) - allowed_stage_paths:
        raise ValueError(
            f"paths are not exactly within stage {stage}: "
            f"{sorted(set(paths) - allowed_stage_paths)}"
        )

    units = [
        json.loads(line)
        for line in (GOAL_DIR / "source-units.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line
    ]
    selected_units = [unit for unit in units if unit["path"] in paths]
    reading = [
        row
        for row in read_csv(GOAL_DIR / "reading-ledger.csv")
        if row["path"] in paths
    ]
    assets = [
        row
        for row in read_csv(GOAL_DIR / "asset-ledger.csv")
        if row["assignment_path"] in paths
    ]

    output.mkdir(parents=True)
    input_root = output / "input"
    schema_source = GOAL_DIR / "schemas" / "blind"
    for schema_name in (
        "reading-ledger-row.schema.json",
        "candidate-record.schema.json",
        "asset-ledger-row.schema.json",
        "cross-reference-row.schema.json",
        "worker-output.schema.json",
    ):
        write(
            input_root / "schemas" / schema_name,
            (schema_source / schema_name).read_bytes(),
        )
    write(
        input_root / "guardrails.json",
        canonical_json_bytes(sanitized_guardrails(guardrails)),
    )
    prompt_bytes = brief(worker_id, stage, paths).encode("utf-8")
    write(input_root / "brief.md", prompt_bytes)
    write(
        input_root / "source-units.jsonl",
        b"".join(
            (
                json.dumps(unit, sort_keys=True, separators=(",", ":")) + "\n"
            ).encode()
            for unit in selected_units
        ),
    )
    write(input_root / "reading-input.csv", csv_bytes(READING_HEADER, reading))
    write(input_root / "asset-input.csv", csv_bytes(ASSET_HEADER, assets))
    for relative in paths:
        destination = input_root / "sources" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        os.link(SOURCE_ROOT / relative, destination)
    for asset in assets:
        relative = asset["physical_path"]
        destination = input_root / "images" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        os.link(SOURCE_ROOT / relative, destination)

    allowed: list[dict[str, Any]] = []
    for path in sorted(item for item in input_root.rglob("*") if item.is_file()):
        data = path.read_bytes()
        allowed.append(
            {
                "path": path.relative_to(output).as_posix(),
                "bytes": len(data),
                "sha256": sha256(data),
            }
        )
    content_set_sha = sha256(
        b"".join(
            f"{row['sha256']}  {row['path']}\n".encode() for row in allowed
        )
    )
    schema_sha = sha256(
        b"".join(
            (input_root / "schemas" / name).read_bytes()
            for name in sorted(
                path.name for path in (input_root / "schemas").iterdir()
            )
        )
    )
    bundle_manifest = {
        "schema_version": 1,
        "worker_id": worker_id,
        "stage": stage,
        "source_paths": paths,
        "source_unit_count": len(selected_units),
        "asset_count": len(assets),
        "content_set_sha256": content_set_sha,
        "prompt_sha256": sha256(prompt_bytes),
        "schema_sha256": schema_sha,
        "execution_requirements": {
            "filesystem_scope": "bundle_only",
            "input_read_only": True,
            "output_path": "output/output.json",
            "network_allowed": False,
        },
        "allowed_inputs": allowed,
    }
    manifest_bytes = canonical_json_bytes(bundle_manifest)
    write(output / "allowed-manifest.json", manifest_bytes)
    template = {
        "worker_id": worker_id,
        "bundle_sha256": content_set_sha,
        "prompt_sha256": bundle_manifest["prompt_sha256"],
        "schema_sha256": schema_sha,
        "allowed_manifest_sha256": sha256(manifest_bytes),
        "prohibited_input_nonuse": False,
        "reading_updates": [],
        "candidate_proposals": [],
        "asset_updates": [],
        "route_proposals": [],
        "uncertainties": [],
    }
    write(output / "output" / "output.json", canonical_json_bytes(template))


def verify_bundle(bundle: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest_path = bundle / "allowed-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot load bundle manifest: {exc}"]
    if set(manifest) != {
        "schema_version",
        "worker_id",
        "stage",
        "source_paths",
        "source_unit_count",
        "asset_count",
        "content_set_sha256",
        "prompt_sha256",
        "schema_sha256",
        "execution_requirements",
        "allowed_inputs",
    }:
        errors.append("bundle manifest fields are invalid")
    actual_files = {
        path.relative_to(bundle).as_posix(): path
        for path in (bundle / "input").rglob("*")
        if path.is_file()
    }
    expected_files = {row["path"]: row for row in manifest.get("allowed_inputs", [])}
    if set(actual_files) != set(expected_files):
        errors.append("bundle input file set differs from allowlist")
    for relative, path in actual_files.items():
        if path.is_symlink():
            errors.append(f"bundle input is a symlink: {relative}")
        data = path.read_bytes()
        record = expected_files.get(relative, {})
        if record.get("bytes") != len(data) or record.get("sha256") != sha256(data):
            errors.append(f"bundle input hash/size mismatch: {relative}")
    content_set_sha = sha256(
        b"".join(
            f"{expected_files[path]['sha256']}  {path}\n".encode()
            for path in sorted(expected_files)
        )
    )
    if manifest.get("content_set_sha256") != content_set_sha:
        errors.append("bundle content-set digest mismatch")
    brief_text = (bundle / "input" / "brief.md").read_text(encoding="utf-8")
    for term in FORBIDDEN_BRIEF_TERMS:
        if term.lower() in brief_text.lower():
            errors.append(f"bundle brief contains priming term: {term}")
    forbidden_parts = {".git", "goal-1", "goal-2", "src"}
    for relative in actual_files:
        if forbidden_parts & set(Path(relative).parts):
            errors.append(f"bundle contains prohibited path: {relative}")
    requirements = manifest.get("execution_requirements", {})
    if requirements.get("network_allowed") is not False:
        errors.append("bundle does not prohibit network")
    if requirements.get("input_read_only") is not True:
        errors.append("bundle does not require read-only input")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--output", type=Path)
    action.add_argument("--verify", type=Path)
    parser.add_argument("--worker-id", default="blind-worker")
    parser.add_argument("--stage", type=int)
    parser.add_argument("--path", action="append", default=[])
    args = parser.parse_args()

    try:
        if args.verify is not None:
            errors = verify_bundle(args.verify.resolve())
            if errors:
                for error in errors:
                    print(f"ERROR: {error}", file=sys.stderr)
                return 1
            print("verified sealed blind-worker bundle")
            return 0
        if args.stage is None:
            parser.error("--stage is required with --output")
        build_bundle(
            args.output.resolve(),
            args.worker_id,
            args.stage,
            args.path,
        )
        errors = verify_bundle(args.output.resolve())
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        print(f"built sealed blind-worker bundle: {args.output}")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"bundle operation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
