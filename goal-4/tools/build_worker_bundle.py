#!/usr/bin/env python3
"""Build or verify a sealed, sanitized blind-discovery worker bundle."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

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
SCHEMA_NAMES = (
    "asset-ledger-row.schema.json",
    "candidate-record.schema.json",
    "cross-reference-row.schema.json",
    "reading-ledger-row.schema.json",
    "worker-output.schema.json",
)
MANIFEST_FIELDS = {
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
}
MANIFEST_INPUT_FIELDS = {"path", "bytes", "sha256"}
EXECUTION_REQUIREMENT_FIELDS = {
    "filesystem_scope",
    "input_read_only",
    "output_path",
    "network_allowed",
    "runtime_os_sandbox_required",
    "bundle_preparation_enforces_sandbox",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
CHAPTER_PATH_RE = re.compile(
    r"^(?:CHAPTERS|BACK-MATTER/NOTES)/([0-9]{2})-[^/]+\.md$"
)
STAGE_4_PATHS = {
    "FRONT-MATTER/00-Publication-and-Contents.md",
    "FRONT-MATTER/01-Preface.md",
    "BACK-MATTER/NOTES/00-General-Notes.md",
    "BACK-MATTER/Colophon.md",
}


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


def stage_for_path(relative: str) -> int | None:
    if relative in STAGE_4_PATHS:
        return 4
    if relative == "BACK-MATTER/Index.md":
        return 17
    match = CHAPTER_PATH_RE.fullmatch(relative)
    if match is None:
        return None
    chapter = int(match.group(1))
    if 1 <= chapter <= 12:
        return chapter + 4
    return None


def is_safe_relative_path(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = Path(value)
    return (
        not path.is_absolute()
        and path.as_posix() == value
        and all(part not in {"", ".", ".."} for part in path.parts)
    )


def seal_inputs(input_root: Path) -> None:
    """Make prepared inputs immutable; runtime isolation is still external."""
    for path in input_root.rglob("*"):
        if path.is_file():
            path.chmod(0o444)
    for path in sorted(
        (item for item in input_root.rglob("*") if item.is_dir()),
        key=lambda item: len(item.parts),
        reverse=True,
    ):
        path.chmod(0o555)
    input_root.chmod(0o555)


def load_csv_exact(
    path: Path,
    expected_header: list[str],
    errors: list[str],
    label: str,
) -> list[dict[str, str]]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != expected_header:
                errors.append(f"{label} header differs from the frozen schema")
                return []
            rows = list(reader)
    except (OSError, csv.Error) as exc:
        errors.append(f"cannot load {label}: {exc}")
        return []
    if any(None in row for row in rows):
        errors.append(f"{label} contains an over-wide row")
    return rows


def load_source_units(path: Path, errors: list[str]) -> list[dict[str, Any]]:
    units: list[dict[str, Any]] = []
    try:
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(),
            start=1,
        ):
            if not line:
                errors.append(
                    f"source-units.jsonl contains a blank line at {line_number}"
                )
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                errors.append(
                    f"source-units.jsonl line {line_number} is not an object"
                )
                continue
            units.append(value)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot load source-units.jsonl: {exc}")
    return units


def input_record(path: Path, bundle: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(bundle).as_posix(),
        "bytes": len(data),
        "sha256": sha256(data),
    }


def content_set_digest(records: list[dict[str, Any]]) -> str:
    return sha256(
        b"".join(
            f"{row['sha256']}  {row['path']}\n".encode()
            for row in sorted(records, key=lambda row: row["path"])
        )
    )


def schema_set_digest(schema_root: Path) -> str:
    return sha256(
        b"".join((schema_root / name).read_bytes() for name in SCHEMA_NAMES)
    )


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
    if requested_paths and len(requested_paths) != len(set(requested_paths)):
        raise ValueError("requested paths must be unique")
    paths = sorted(requested_paths or allowed_stage_paths)
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
    for schema_name in SCHEMA_NAMES:
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
        shutil.copy2(SOURCE_ROOT / relative, destination)
    for asset in assets:
        relative = asset["physical_path"]
        destination = input_root / "images" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists():
            shutil.copy2(SOURCE_ROOT / relative, destination)

    allowed: list[dict[str, Any]] = []
    for path in sorted(item for item in input_root.rglob("*") if item.is_file()):
        allowed.append(input_record(path, output))
    content_set_sha = content_set_digest(allowed)
    schema_sha = schema_set_digest(input_root / "schemas")
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
            "runtime_os_sandbox_required": True,
            "bundle_preparation_enforces_sandbox": False,
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
    seal_inputs(input_root)
    (output / "allowed-manifest.json").chmod(0o444)


def _validate_worker_output(
    bundle: Path,
    manifest: dict[str, Any],
    errors: list[str],
    require_completed_output: bool,
) -> None:
    output_path = bundle / "output" / "output.json"
    try:
        output = json.loads(output_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot load worker output: {exc}")
        return
    if not isinstance(output, dict):
        errors.append("worker output is not an object")
        return

    schema_path = bundle / "input" / "schemas" / "worker-output.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except (OSError, json.JSONDecodeError, SchemaError) as exc:
        errors.append(f"cannot load worker-output schema: {exc}")
        return

    nonuse = output.get("prohibited_input_nonuse")
    validation_value = output
    if nonuse is False and not require_completed_output:
        list_fields = (
            "reading_updates",
            "candidate_proposals",
            "asset_updates",
            "route_proposals",
            "uncertainties",
        )
        if any(output.get(field) != [] for field in list_fields):
            errors.append(
                "prohibited_input_nonuse=false is allowed only for the empty template"
            )
        validation_value = deepcopy(output)
        validation_value["prohibited_input_nonuse"] = True
    elif nonuse is not True:
        errors.append(
            "completed worker output must declare prohibited_input_nonuse=true"
        )

    validator = Draft202012Validator(schema)
    for error in sorted(
        validator.iter_errors(validation_value),
        key=lambda item: [str(part) for part in item.absolute_path],
    ):
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"worker output schema error at {location}: {error.message}")

    expected_declarations = {
        "worker_id": manifest.get("worker_id"),
        "bundle_sha256": manifest.get("content_set_sha256"),
        "prompt_sha256": manifest.get("prompt_sha256"),
        "schema_sha256": manifest.get("schema_sha256"),
        "allowed_manifest_sha256": sha256(
            (bundle / "allowed-manifest.json").read_bytes()
        ),
    }
    for field, expected in expected_declarations.items():
        if output.get(field) != expected:
            errors.append(f"worker output {field} declaration mismatch")

    assigned_units = {
        row.get("source_unit_id"): row
        for row in load_csv_exact(
            bundle / "input" / "reading-input.csv",
            READING_HEADER,
            errors,
            "reading input",
        )
        if row.get("source_unit_id")
    }
    assigned_assets = {
        row.get("asset_id"): row
        for row in load_csv_exact(
            bundle / "input" / "asset-input.csv",
            ASSET_HEADER,
            errors,
            "asset input",
        )
        if row.get("asset_id")
    }

    reading_updates = output.get("reading_updates", [])
    if isinstance(reading_updates, list):
        seen: set[str] = set()
        immutable = READING_HEADER[: READING_HEADER.index("review_status")]
        for row in reading_updates:
            if not isinstance(row, dict):
                continue
            unit_id = row.get("source_unit_id")
            if unit_id in seen:
                errors.append(f"duplicate reading update: {unit_id}")
            seen.add(unit_id)
            original = assigned_units.get(unit_id)
            if original is None:
                errors.append(f"reading update is outside assignment: {unit_id}")
                continue
            if any(row.get(field) != original.get(field) for field in immutable):
                errors.append(f"reading update changes source identity: {unit_id}")

    asset_updates = output.get("asset_updates", [])
    if isinstance(asset_updates, list):
        seen = set()
        immutable = ASSET_HEADER[: ASSET_HEADER.index("inspection_status")]
        for row in asset_updates:
            if not isinstance(row, dict):
                continue
            asset_id = row.get("asset_id")
            if asset_id in seen:
                errors.append(f"duplicate asset update: {asset_id}")
            seen.add(asset_id)
            original = assigned_assets.get(asset_id)
            if original is None:
                errors.append(f"asset update is outside assignment: {asset_id}")
                continue
            if any(row.get(field) != original.get(field) for field in immutable):
                errors.append(f"asset update changes source identity: {asset_id}")

    proposals = output.get("candidate_proposals", [])
    if isinstance(proposals, list):
        proposal_ids = {
            row.get("id")
            for row in proposals
            if isinstance(row, dict) and isinstance(row.get("id"), str)
        }
        for row in proposals:
            if not isinstance(row, dict):
                continue
            candidate_id = row.get("id", "<unknown>")
            if row.get("discovery_stage") != manifest.get("stage"):
                errors.append(
                    f"candidate {candidate_id} discovery_stage differs from bundle"
                )
            source_ids = row.get("source_unit_ids", [])
            if isinstance(source_ids, list) and not set(source_ids) <= set(
                assigned_units
            ):
                errors.append(
                    f"candidate {candidate_id} cites a source outside assignment"
                )
            image_ids = row.get("image_witnesses", [])
            if isinstance(image_ids, list) and not set(image_ids) <= set(
                assigned_assets
            ):
                errors.append(
                    f"candidate {candidate_id} cites an image outside assignment"
                )
            related_ids = row.get("related_candidate_ids", [])
            if isinstance(related_ids, list) and not set(related_ids) <= proposal_ids:
                errors.append(
                    f"candidate {candidate_id} relates to an undeclared worker candidate"
                )

    routes = output.get("route_proposals", [])
    if isinstance(routes, list):
        route_ids: set[str] = set()
        for row in routes:
            if not isinstance(row, dict):
                continue
            route_id = row.get("route_id")
            if route_id in route_ids:
                errors.append(f"duplicate route proposal: {route_id}")
            route_ids.add(route_id)
            if row.get("source_unit_id") not in assigned_units:
                errors.append(f"route {route_id} is outside the source assignment")
            if row.get("owning_stage") != str(manifest.get("stage")):
                errors.append(f"route {route_id} owning_stage differs from bundle")


def verify_bundle(
    bundle: Path,
    require_completed_output: bool = False,
) -> list[str]:
    errors: list[str] = []
    try:
        manifest_path = bundle / "allowed-manifest.json"
        manifest_bytes = manifest_path.read_bytes()
        manifest = json.loads(manifest_bytes)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot load bundle manifest: {exc}"]
    if not isinstance(manifest, dict):
        return ["bundle manifest is not an object"]
    if set(manifest) != MANIFEST_FIELDS:
        errors.append("bundle manifest fields are invalid")
    if manifest_bytes != canonical_json_bytes(manifest):
        errors.append("bundle manifest is not canonically serialized")

    if manifest.get("schema_version") != 1:
        errors.append("bundle manifest schema_version must be 1")
    worker_id = manifest.get("worker_id")
    if not isinstance(worker_id, str) or not worker_id.strip():
        errors.append("bundle worker_id must be a nonempty string")
    stage = manifest.get("stage")
    if not isinstance(stage, int) or isinstance(stage, bool) or not 4 <= stage <= 17:
        errors.append("bundle stage must be an integer from 4 through 17")
    source_paths = manifest.get("source_paths")
    if not isinstance(source_paths, list) or not source_paths or not all(
        is_safe_relative_path(path) for path in source_paths
    ):
        errors.append("bundle source_paths must be nonempty, unique, and sorted")
        source_paths = []
    elif source_paths != sorted(set(source_paths)):
        errors.append("bundle source_paths must be nonempty, unique, and sorted")
        source_paths = []
    if isinstance(stage, int):
        for source_path in source_paths:
            if stage_for_path(source_path) != stage:
                errors.append(
                    f"source path {source_path} does not belong to stage {stage}"
                )
    for count_field in ("source_unit_count", "asset_count"):
        count = manifest.get(count_field)
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            errors.append(f"bundle {count_field} must be a nonnegative integer")
    for digest_field in (
        "content_set_sha256",
        "prompt_sha256",
        "schema_sha256",
    ):
        value = manifest.get(digest_field)
        if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
            errors.append(f"bundle {digest_field} is not a SHA-256 digest")

    requirements = manifest.get("execution_requirements")
    expected_requirements = {
        "filesystem_scope": "bundle_only",
        "input_read_only": True,
        "output_path": "output/output.json",
        "network_allowed": False,
        "runtime_os_sandbox_required": True,
        "bundle_preparation_enforces_sandbox": False,
    }
    if not isinstance(requirements, dict) or set(requirements) != (
        EXECUTION_REQUIREMENT_FIELDS
    ):
        errors.append("bundle execution requirements have invalid fields")
    if requirements != expected_requirements:
        errors.append(
            "bundle must require an external OS/network sandbox and read-only input"
        )

    allowed_rows = manifest.get("allowed_inputs")
    if not isinstance(allowed_rows, list):
        errors.append("bundle allowed_inputs must be an array")
        allowed_rows = []
    expected_files: dict[str, dict[str, Any]] = {}
    declared_order: list[str] = []
    for index, row in enumerate(allowed_rows):
        if not isinstance(row, dict) or set(row) != MANIFEST_INPUT_FIELDS:
            errors.append(f"allowed_inputs[{index}] has invalid fields")
            continue
        relative = row.get("path")
        size = row.get("bytes")
        digest = row.get("sha256")
        if (
            not is_safe_relative_path(relative)
            or not str(relative).startswith("input/")
        ):
            errors.append(f"allowed_inputs[{index}] has an unsafe path")
            continue
        if relative in expected_files:
            errors.append(f"duplicate allowed input path: {relative}")
            continue
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            errors.append(f"allowed input has invalid byte count: {relative}")
        if not isinstance(digest, str) or SHA256_RE.fullmatch(digest) is None:
            errors.append(f"allowed input has invalid digest: {relative}")
        expected_files[relative] = row
        declared_order.append(relative)
    if declared_order != sorted(declared_order):
        errors.append("allowed_inputs records are not sorted by path")

    actual_files: dict[str, Path] = {}
    input_root = bundle / "input"
    if not input_root.is_dir() or input_root.is_symlink():
        errors.append("bundle input root is missing or is a symlink")
    else:
        if input_root.stat().st_mode & 0o222:
            errors.append("bundle input root is writable")
        for path in input_root.rglob("*"):
            relative = path.relative_to(bundle).as_posix()
            if path.is_symlink():
                errors.append(f"bundle input is a symlink: {relative}")
                continue
            if path.is_dir():
                if path.stat().st_mode & 0o222:
                    errors.append(f"bundle input directory is writable: {relative}")
            elif path.is_file():
                actual_files[relative] = path
                if path.stat().st_mode & 0o222:
                    errors.append(f"bundle input file is writable: {relative}")
                if path.stat().st_nlink != 1:
                    errors.append(f"bundle input file is hard-linked: {relative}")
            else:
                errors.append(f"bundle contains a special input: {relative}")

    if set(actual_files) != set(expected_files):
        errors.append("bundle input file set differs from allowlist")
    actual_records: list[dict[str, Any]] = []
    for relative, path in sorted(actual_files.items()):
        record = input_record(path, bundle)
        actual_records.append(record)
        if expected_files.get(relative) != record:
            errors.append(f"bundle input hash/size mismatch: {relative}")
    actual_content_set_sha = content_set_digest(actual_records)
    if manifest.get("content_set_sha256") != actual_content_set_sha:
        errors.append("bundle content-set digest mismatch")

    allowed_root_files = {
        "allowed-manifest.json",
        "output/output.json",
        *actual_files,
    }
    if bundle.is_symlink() or not bundle.is_dir():
        errors.append("bundle root is missing or is a symlink")
    else:
        for path in bundle.rglob("*"):
            relative = path.relative_to(bundle).as_posix()
            if path.is_symlink():
                errors.append(f"bundle contains a symlink: {relative}")
            elif path.is_file() and relative not in allowed_root_files:
                errors.append(f"bundle contains an undeclared file: {relative}")
            elif path.is_dir() and not (
                relative == "input"
                or relative == "output"
                or relative.startswith("input/")
            ):
                errors.append(f"bundle contains an undeclared directory: {relative}")
    if manifest_path.exists() and manifest_path.stat().st_mode & 0o222:
        errors.append("bundle manifest is writable")

    prompt_path = input_root / "brief.md"
    try:
        prompt_bytes = prompt_path.read_bytes()
        brief_text = prompt_bytes.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"cannot load bundle brief: {exc}")
        prompt_bytes = b""
        brief_text = ""
    if manifest.get("prompt_sha256") != sha256(prompt_bytes):
        errors.append("bundle prompt digest mismatch")
    if (
        isinstance(worker_id, str)
        and isinstance(stage, int)
        and source_paths
        and prompt_bytes != brief(worker_id, stage, source_paths).encode("utf-8")
    ):
        errors.append("bundle brief differs from its declared assignment")
    for term in FORBIDDEN_BRIEF_TERMS:
        if term.lower() in brief_text.lower():
            errors.append(f"bundle brief contains priming term: {term}")

    schema_root = input_root / "schemas"
    actual_schema_names = (
        sorted(path.name for path in schema_root.iterdir() if path.is_file())
        if schema_root.is_dir()
        else []
    )
    if actual_schema_names != list(SCHEMA_NAMES):
        errors.append("bundle schema set differs from the frozen blind schema set")
    else:
        try:
            actual_schema_sha = schema_set_digest(schema_root)
            if manifest.get("schema_sha256") != actual_schema_sha:
                errors.append("bundle schema-set digest mismatch")
            trusted_schema_root = GOAL_DIR / "schemas" / "blind"
            for name in SCHEMA_NAMES:
                if (schema_root / name).read_bytes() != (
                    trusted_schema_root / name
                ).read_bytes():
                    errors.append(f"bundle schema differs from generated schema: {name}")
        except OSError as exc:
            errors.append(f"cannot verify bundled schemas: {exc}")

    try:
        expected_guardrails = canonical_json_bytes(
            sanitized_guardrails(
                json.loads((GOAL_DIR / "guardrails.json").read_text())
            )
        )
        if (input_root / "guardrails.json").read_bytes() != expected_guardrails:
            errors.append("bundle guardrails differ from sanitized guardrails")
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        errors.append(f"cannot verify sanitized guardrails: {exc}")

    units = load_source_units(input_root / "source-units.jsonl", errors)
    unit_ids = [unit.get("source_unit_id") for unit in units]
    if not all(isinstance(unit_id, str) and unit_id for unit_id in unit_ids):
        errors.append("bundle source-unit IDs must be nonempty strings")
        valid_unit_ids: set[str] = {
            unit_id for unit_id in unit_ids if isinstance(unit_id, str)
        }
    else:
        valid_unit_ids = set(unit_ids)
    if len(unit_ids) != len(valid_unit_ids):
        errors.append("bundle source-unit IDs are not unique")
    unit_paths = [unit.get("path") for unit in units]
    if (
        any(not isinstance(path, str) for path in unit_paths)
        or sorted(set(unit_paths)) != source_paths
    ):
        errors.append("bundle source_paths differ from source-unit paths")
    if manifest.get("source_unit_count") != len(units):
        errors.append("bundle source_unit_count differs from source-units.jsonl")

    reading_rows = load_csv_exact(
        input_root / "reading-input.csv",
        READING_HEADER,
        errors,
        "reading input",
    )
    reading_ids = [row.get("source_unit_id") for row in reading_rows]
    if len(reading_ids) != len(set(reading_ids)):
        errors.append("bundle reading-input source-unit IDs are not unique")
    if set(reading_ids) != valid_unit_ids:
        errors.append("bundle reading input differs from source-unit assignment")
    if [row.get("path") for row in reading_rows] != unit_paths:
        errors.append("bundle reading input order/path differs from source units")

    source_files = {
        path.relative_to(input_root / "sources").as_posix()
        for path in (input_root / "sources").rglob("*")
        if path.is_file()
    } if (input_root / "sources").is_dir() else set()
    if source_files != set(source_paths):
        errors.append("bundled source-file paths differ from source_paths")

    asset_rows = load_csv_exact(
        input_root / "asset-input.csv",
        ASSET_HEADER,
        errors,
        "asset input",
    )
    asset_ids = [row.get("asset_id") for row in asset_rows]
    if len(asset_ids) != len(set(asset_ids)):
        errors.append("bundle asset IDs are not unique")
    if manifest.get("asset_count") != len(asset_rows):
        errors.append("bundle asset_count differs from asset-input.csv")
    for row in asset_rows:
        if row.get("assignment_path") not in source_paths:
            errors.append(
                f"asset {row.get('asset_id')} is outside the source assignment"
            )
        if row.get("assignment_stage") != str(stage):
            errors.append(
                f"asset {row.get('asset_id')} assignment_stage differs from bundle"
            )
    expected_images = {
        row.get("physical_path")
        for row in asset_rows
        if is_safe_relative_path(row.get("physical_path"))
    }
    image_files = {
        path.relative_to(input_root / "images").as_posix()
        for path in (input_root / "images").rglob("*")
        if path.is_file()
    } if (input_root / "images").is_dir() else set()
    if image_files != expected_images:
        errors.append("bundled image paths differ from the asset assignment")

    forbidden_parts = {".git", "goal-1", "goal-2", "src"}
    for relative in allowed_root_files:
        if forbidden_parts & set(Path(relative).parts):
            errors.append(f"bundle contains prohibited path: {relative}")

    _validate_worker_output(
        bundle,
        manifest,
        errors,
        require_completed_output,
    )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--output", type=Path)
    action.add_argument("--verify", type=Path)
    parser.add_argument(
        "--verify-output",
        action="store_true",
        help=(
            "with --verify, require a completed schema-valid worker output "
            "whose prohibited-input declaration is true"
        ),
    )
    parser.add_argument("--worker-id", default="blind-worker")
    parser.add_argument("--stage", type=int)
    parser.add_argument("--path", action="append", default=[])
    args = parser.parse_args()

    try:
        if args.verify is not None:
            errors = verify_bundle(
                args.verify.resolve(),
                require_completed_output=args.verify_output,
            )
            if errors:
                for error in errors:
                    print(f"ERROR: {error}", file=sys.stderr)
                return 1
            if args.verify_output:
                print("verified sealed blind-worker bundle and completed output")
            else:
                print(
                    "verified prepared blind-worker bundle; "
                    "runtime OS/network sandboxing is still required"
                )
            return 0
        if args.verify_output:
            parser.error("--verify-output requires --verify")
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
        print(
            f"prepared sealed blind-worker bundle: {args.output}; "
            "execute it only inside the required OS/network sandbox"
        )
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"bundle operation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
