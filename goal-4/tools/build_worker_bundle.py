#!/usr/bin/env python3
"""Build or verify a sealed, sanitized blind-discovery worker bundle.

Preparation and output validation do not enforce the required runtime sandbox
or perform the coordinator's canonical-ID allocation and merge validation.
"""

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

from audit_contract import (
    ASSET_HEADER,
    GOAL_DIR,
    READING_HEADER,
    REPO_ROOT,
    canonical_json_bytes,
)


SOURCE_ROOT = REPO_ROOT / "ref" / "A-New-Kind-of-Science"
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
    "discovery_epoch",
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
    "coordinator_merge_validation_required",
    "worker_search_allowed",
    "worker_route_resolution_allowed",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
WORKER_CANDIDATE_RE = re.compile(r"^W[0-9]{4}$")
GLOBAL_CANDIDATE_RE = re.compile(r"^B[0-9]{4}$")
WORKER_ROUTE_RE = re.compile(r"^WR[0-9]{4}$")
GLOBAL_ROUTE_RE = re.compile(r"^R[0-9]{6}$")
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


def compile_blind_text_patterns(
    guardrails: dict[str, Any],
) -> tuple[re.Pattern[str], ...]:
    """Compile the authoritative blind free-text denylist."""
    try:
        raw_patterns = guardrails["blind_schema_policy"][
            "free_text_review_patterns"
        ]
    except KeyError as exc:
        raise ValueError(
            "guardrails lack authoritative blind free-text patterns"
        ) from exc
    if not isinstance(raw_patterns, list) or not raw_patterns:
        raise ValueError(
            "guardrail blind free-text patterns must be a nonempty array"
        )
    patterns: list[re.Pattern[str]] = []
    for index, raw in enumerate(raw_patterns):
        if not isinstance(raw, str) or not raw:
            raise ValueError(
                f"guardrail blind free-text pattern {index} is not a string"
            )
        try:
            patterns.append(re.compile(raw, re.IGNORECASE))
        except re.error as exc:
            raise ValueError(
                f"invalid guardrail blind free-text pattern {raw!r}: {exc}"
            ) from exc
    return tuple(patterns)


def blind_text_matches(
    value: Any,
    patterns: tuple[re.Pattern[str], ...],
    path: str = "$",
) -> list[str]:
    """Return locations where free text leaks frozen reconciliation language."""
    matches: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            matches.extend(
                blind_text_matches(nested, patterns, f"{path}.{key}")
            )
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            matches.extend(
                blind_text_matches(nested, patterns, f"{path}[{index}]")
            )
    elif isinstance(value, str):
        for pattern in patterns:
            if pattern.search(value):
                matches.append(f"{path} matches {pattern.pattern!r}")
    return matches


def reject_blind_text(
    value: Any,
    patterns: tuple[re.Pattern[str], ...],
    label: str,
) -> None:
    matches = blind_text_matches(value, patterns, label)
    if matches:
        raise ValueError(
            "forbidden blind priming in generated metadata: "
            + "; ".join(matches)
        )


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


def ordered_stage_paths(manifest: dict[str, Any], stage: int) -> list[str]:
    """Return one stage's documents in the corpus manifest's canonical order."""

    allowed = stage_paths(manifest, stage)
    return [
        document["path"]
        for document in manifest["documents"]
        if document["path"] in allowed
    ]


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
        "visual_roles",
        "visual_risk_flags",
        "source_uncertainty_contract",
        "review_epoch_contract",
        "lifecycle_relation_contract",
        "discovery_anchor_contract",
        "route_closure_scopes",
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


def brief(worker_id: str, stage: int, epoch: int, paths: list[str]) -> str:
    listed = "\n".join(f"- `{path}`" for path in paths)
    reopen_instruction = (
        "\nThis is a formally reopened pass. In every reading/asset update, "
        "retain the input row's existing global B/R links exactly and in "
        "their existing order; add any new worker-local W/WR links without "
        "removing or inventing global links.\n"
        if epoch > 1
        else ""
    )
    return f"""# Blind Source Review

Worker: `{worker_id}`
Stage: `{stage}`
Discovery epoch: `{epoch}`

Read only the files in this bundle, in the exact source-unit order provided.
Do not run search in this worker bundle; the coordinator performs and records
typed local-search rounds after merging the sequential review. Do not use
outside knowledge to fill missing mechanics, and do not decide implementation,
equivalence, reuse, or final taxonomy.
{reopen_instruction}

Assigned canonical documents:

{listed}

For every source unit:

1. Read the complete byte range and enough adjacent bundled context.
2. Return exactly one primary reading disposition and a separate source status.
3. Set `review_epoch` to `{epoch}` and record concise evidence, secondary
   roles, candidate links, and routes.
4. Err toward a worker-local `W####` candidate when both an identity anchor and
   semantic anchor may be present.
5. Fill every fingerprint field with supported, not-applicable, unknown, or
   conflicting status. Never invent a blank.
6. Review every assigned image at least as a thumbnail; require original
   resolution for construction-bearing, text-bearing, ambiguous, or
   caption-incomplete images.
7. Emit routes only as `PENDING` proposals with a complete worker-local
   `WR0001`, `WR0002`, ... sequence in discovery order; do not resolve them or
   declare a final missing target. The coordinator maps WR IDs to global R IDs
   and performs global routing.
8. Allocate evidence as `WE000001`, `WE000002`, ... in first-occurrence order,
   and evidence groups as `WG000001`, `WG000002`, ... in group first-occurrence
   order. The coordinator maps these worker-local IDs to global E/G IDs.

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


def _json_equal(left: Any, right: Any) -> bool:
    return json.dumps(left, sort_keys=True, separators=(",", ":")) == json.dumps(
        right,
        sort_keys=True,
        separators=(",", ":"),
    )


def _matches_json_type(value: Any, expected: str) -> bool:
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
        "null": value is None,
    }.get(expected, False)


def json_schema_errors(
    value: Any,
    schema: dict[str, Any],
    path: str = "<root>",
) -> list[str]:
    """Validate the closed schema subset emitted by audit_contract.py."""
    errors: list[str] = []
    if "oneOf" in schema:
        branches = schema["oneOf"]
        branch_results = [
            json_schema_errors(value, branch, path) for branch in branches
        ]
        if sum(not result for result in branch_results) != 1:
            errors.append(f"{path}: value must satisfy exactly one oneOf branch")
            return errors
    expected_type = schema.get("type")
    if expected_type is not None:
        expected_types = (
            expected_type if isinstance(expected_type, list) else [expected_type]
        )
        if not all(isinstance(item, str) for item in expected_types):
            return [f"{path}: schema contains an invalid type declaration"]
        if not any(_matches_json_type(value, item) for item in expected_types):
            errors.append(
                f"{path}: expected type {' or '.join(expected_types)}, "
                f"got {type(value).__name__}"
            )
            return errors
    if "const" in schema and not _json_equal(value, schema["const"]):
        errors.append(f"{path}: value differs from required const")
    if "enum" in schema and not any(
        _json_equal(value, choice) for choice in schema["enum"]
    ):
        errors.append(f"{path}: value is not in the allowed enum")
    if isinstance(value, str):
        if "pattern" in schema:
            try:
                matched = re.search(schema["pattern"], value)
            except (re.error, TypeError):
                errors.append(f"{path}: schema contains an invalid pattern")
            else:
                if matched is None:
                    errors.append(f"{path}: string does not match required pattern")
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: string is shorter than minLength")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: value is below minimum")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: value is above maximum")
    if isinstance(value, list):
        if schema.get("uniqueItems") is True:
            serialized = [
                json.dumps(item, sort_keys=True, separators=(",", ":"))
                for item in value
            ]
            if len(serialized) != len(set(serialized)):
                errors.append(f"{path}: array items are not unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(
                    json_schema_errors(item, item_schema, f"{path}/{index}")
                )
    if isinstance(value, dict):
        required = schema.get("required", [])
        for field in required:
            if field not in value:
                errors.append(f"{path}: missing required field {field}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for field in value:
                if field not in properties:
                    errors.append(f"{path}: unexpected field {field}")
        for field, field_schema in properties.items():
            if field in value:
                errors.extend(
                    json_schema_errors(
                        value[field],
                        field_schema,
                        f"{path}/{field}",
                    )
                )
    return errors


def parse_string_array(
    value: object,
    label: str,
    errors: list[str],
) -> list[str]:
    try:
        parsed = json.loads(value) if isinstance(value, str) else None
    except json.JSONDecodeError:
        parsed = None
    if (
        not isinstance(parsed, list)
        or not all(isinstance(item, str) for item in parsed)
        or len(parsed) != len(set(parsed))
    ):
        errors.append(f"{label} must be a JSON array of unique strings")
        return []
    return parsed


def is_complete_worker_sequence(
    values: list[str],
    prefix: str,
    width: int,
) -> bool:
    return values == [
        f"{prefix}{index:0{width}d}" for index in range(1, len(values) + 1)
    ]


def reopened_local_links(
    value: object,
    original_value: object,
    *,
    epoch: object,
    local_pattern: re.Pattern[str],
    global_pattern: re.Pattern[str],
    label: str,
    errors: list[str],
) -> list[str]:
    """Validate retained global links and return this worker's local links."""

    links = parse_string_array(value, label, errors)
    original_links = parse_string_array(
        original_value,
        f"{label} authoritative input",
        errors,
    )
    local_links = [link for link in links if local_pattern.fullmatch(link)]
    retained_links = [link for link in links if global_pattern.fullmatch(link)]
    invalid_links = [
        link
        for link in links
        if not local_pattern.fullmatch(link)
        and not global_pattern.fullmatch(link)
    ]
    if invalid_links:
        errors.append(f"{label} has invalid link IDs: {invalid_links}")
    if epoch == 1:
        if retained_links:
            errors.append(
                f"{label} initial pass cannot claim pre-existing global links"
            )
    elif isinstance(epoch, int) and not isinstance(epoch, bool) and epoch > 1:
        if retained_links != original_links:
            errors.append(
                f"{label} reopened pass must retain existing global links "
                "exactly and in order"
            )
    return local_links


def discovery_anchor_orders(
    assigned_units: dict[str, dict[str, str]],
    assigned_assets: dict[str, dict[str, str]],
) -> tuple[dict[str, int], dict[str, int], dict[str, int]]:
    """Return document-first unit/image traversal orders for local anchors."""
    document_order: dict[str, int] = {}
    for row in assigned_units.values():
        path = row.get("path")
        try:
            order = int(row.get("document_order", ""))
        except ValueError:
            continue
        if path:
            document_order[path] = min(order, document_order.get(path, order))
    next_order = max(document_order.values(), default=0) + 1
    for row in assigned_assets.values():
        path = row.get("assignment_path")
        if path and path not in document_order:
            document_order[path] = next_order
            next_order += 1

    unit_order: dict[str, int] = {}
    asset_order: dict[str, int] = {}
    image_path_order: dict[str, int] = {}
    ordinal = 1
    for path in sorted(document_order, key=lambda item: document_order[item]):
        for unit_id, row in assigned_units.items():
            if row.get("path") == path:
                unit_order[unit_id] = ordinal
                ordinal += 1
        for asset_id, row in assigned_assets.items():
            if row.get("assignment_path") == path:
                asset_order[asset_id] = ordinal
                physical_path = row.get("physical_path")
                if physical_path:
                    image_path_order[physical_path] = ordinal
                ordinal += 1
    return unit_order, asset_order, image_path_order


def build_bundle(
    output: Path,
    worker_id: str,
    stage: int,
    requested_paths: list[str],
    epoch: int = 1,
) -> None:
    if output.exists():
        raise ValueError(f"output already exists: {output}")
    if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 1:
        raise ValueError("discovery epoch must be a positive integer")
    manifest = json.loads((GOAL_DIR / "corpus-manifest.json").read_text())
    guardrails = json.loads((GOAL_DIR / "guardrails.json").read_text())
    text_patterns = compile_blind_text_patterns(guardrails)
    if not isinstance(worker_id, str) or not worker_id.strip():
        raise ValueError("worker_id must be a nonempty string")
    reject_blind_text(
        {"worker_id": worker_id},
        text_patterns,
        "worker_metadata",
    )
    allowed_stage_path_order = ordered_stage_paths(manifest, stage)
    allowed_stage_paths = set(allowed_stage_path_order)
    if requested_paths and len(requested_paths) != len(set(requested_paths)):
        raise ValueError("requested paths must be unique")
    requested_set = set(requested_paths) if requested_paths else allowed_stage_paths
    paths = [
        path for path in allowed_stage_path_order if path in requested_set
    ]
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

    prompt_bytes = brief(worker_id, stage, epoch, paths).encode("utf-8")
    reject_blind_text(
        prompt_bytes.decode("utf-8"),
        text_patterns,
        "brief",
    )
    blind_guardrails = sanitized_guardrails(guardrails)
    reject_blind_text(
        blind_guardrails,
        text_patterns,
        "sanitized_guardrails",
    )

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
        canonical_json_bytes(blind_guardrails),
    )
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
        "discovery_epoch": epoch,
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
            "coordinator_merge_validation_required": True,
            "worker_search_allowed": False,
            "worker_route_resolution_allowed": False,
        },
        "allowed_inputs": allowed,
    }
    reject_blind_text(
        bundle_manifest,
        text_patterns,
        "allowed_manifest",
    )
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
    reject_blind_text(
        template,
        text_patterns,
        "worker_output_template",
    )
    write(output / "output" / "output.json", canonical_json_bytes(template))
    seal_inputs(input_root)
    (output / "allowed-manifest.json").chmod(0o444)


def _validate_worker_output(
    bundle: Path,
    manifest: dict[str, Any],
    errors: list[str],
    require_completed_output: bool,
    text_patterns: tuple[re.Pattern[str], ...],
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
    for match in blind_text_matches(output, text_patterns, "worker_output"):
        errors.append(f"worker output contains forbidden blind priming: {match}")

    schema_path = bundle / "input" / "schemas" / "worker-output.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot load worker-output schema: {exc}")
        return
    if not isinstance(schema, dict):
        errors.append("worker-output schema is not an object")
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

    for error in json_schema_errors(validation_value, schema):
        errors.append(f"worker output schema error at {error}")

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
    assigned_image_paths = {
        row.get("physical_path")
        for row in assigned_assets.values()
        if row.get("physical_path")
    }
    (
        assigned_unit_anchor_order,
        assigned_asset_anchor_order,
        assigned_image_anchor_order,
    ) = discovery_anchor_orders(assigned_units, assigned_assets)
    if nonuse is not True:
        return
    bundle_epoch = manifest.get("discovery_epoch")
    valid_bundle_epoch = (
        isinstance(bundle_epoch, int)
        and not isinstance(bundle_epoch, bool)
        and bundle_epoch >= 1
    )

    reading_updates = output.get("reading_updates", [])
    candidate_sources_from_reading: dict[str, set[str]] = {}
    route_sources_from_reading: dict[str, set[str]] = {}
    if isinstance(reading_updates, list):
        seen: set[str] = set()
        immutable = READING_HEADER[: READING_HEADER.index("review_status")]
        for row in reading_updates:
            if not isinstance(row, dict):
                continue
            unit_id = row.get("source_unit_id")
            if not isinstance(unit_id, str):
                errors.append("reading update has a non-string source_unit_id")
                continue
            if unit_id in seen:
                errors.append(f"duplicate reading update: {unit_id}")
            seen.add(unit_id)
            original = assigned_units.get(unit_id)
            if original is None:
                errors.append(f"reading update is outside assignment: {unit_id}")
                continue
            if any(row.get(field) != original.get(field) for field in immutable):
                errors.append(f"reading update changes source identity: {unit_id}")
            if row.get("review_status") != "REVIEWED":
                errors.append(f"reading update is not REVIEWED: {unit_id}")
            if row.get("review_epoch") != str(bundle_epoch):
                errors.append(
                    f"reading update review_epoch differs from bundle: {unit_id}"
                )
            if not row.get("review_disposition") or not row.get("source_status"):
                errors.append(f"reading update lacks a disposition/status: {unit_id}")
            if row.get("review_stage") != str(manifest.get("stage")):
                errors.append(f"reading update stage differs from bundle: {unit_id}")
            if row.get("reviewer") != manifest.get("worker_id"):
                errors.append(f"reading update reviewer differs from worker: {unit_id}")
            if not row.get("evidence_statement"):
                errors.append(f"reading update lacks evidence: {unit_id}")
            parse_string_array(
                row.get("secondary_roles"),
                f"reading update {unit_id} secondary_roles",
                errors,
            )
            for candidate_id in reopened_local_links(
                row.get("candidate_ids"),
                original.get("candidate_ids"),
                epoch=bundle_epoch,
                local_pattern=WORKER_CANDIDATE_RE,
                global_pattern=GLOBAL_CANDIDATE_RE,
                label=f"reading update {unit_id} candidate_ids",
                errors=errors,
            ):
                candidate_sources_from_reading.setdefault(candidate_id, set()).add(
                    unit_id
                )
            for route_id in reopened_local_links(
                row.get("route_ids"),
                original.get("route_ids"),
                epoch=bundle_epoch,
                local_pattern=WORKER_ROUTE_RE,
                global_pattern=GLOBAL_ROUTE_RE,
                label=f"reading update {unit_id} route_ids",
                errors=errors,
            ):
                route_sources_from_reading.setdefault(route_id, set()).add(unit_id)
        if seen != set(assigned_units):
            errors.append(
                "completed worker output must update every assigned source unit exactly once"
            )

    asset_updates = output.get("asset_updates", [])
    candidate_images_from_assets: dict[str, set[str]] = {}
    route_sources_from_assets: dict[str, set[str]] = {}
    if isinstance(asset_updates, list):
        seen = set()
        immutable = ASSET_HEADER[: ASSET_HEADER.index("inspection_status")]
        for row in asset_updates:
            if not isinstance(row, dict):
                continue
            asset_id = row.get("asset_id")
            if not isinstance(asset_id, str):
                errors.append("asset update has a non-string asset_id")
                continue
            if asset_id in seen:
                errors.append(f"duplicate asset update: {asset_id}")
            seen.add(asset_id)
            original = assigned_assets.get(asset_id)
            if original is None:
                errors.append(f"asset update is outside assignment: {asset_id}")
                continue
            if any(row.get(field) != original.get(field) for field in immutable):
                errors.append(f"asset update changes source identity: {asset_id}")
            if row.get("inspection_status") != "SCREENED":
                errors.append(f"asset update is not SCREENED: {asset_id}")
            if row.get("review_epoch") != str(bundle_epoch):
                errors.append(
                    f"asset update review_epoch differs from bundle: {asset_id}"
                )
            if row.get("review_stage") != str(manifest.get("stage")):
                errors.append(f"asset update stage differs from bundle: {asset_id}")
            if row.get("reviewer") != manifest.get("worker_id"):
                errors.append(f"asset update reviewer differs from worker: {asset_id}")
            if not row.get("visual_role") or not row.get("evidence_statement"):
                errors.append(f"asset update lacks visual evidence fields: {asset_id}")
            for candidate_id in reopened_local_links(
                row.get("candidate_ids"),
                original.get("candidate_ids"),
                epoch=bundle_epoch,
                local_pattern=WORKER_CANDIDATE_RE,
                global_pattern=GLOBAL_CANDIDATE_RE,
                label=f"asset update {asset_id} candidate_ids",
                errors=errors,
            ):
                candidate_images_from_assets.setdefault(candidate_id, set()).add(
                    row.get("physical_path", "")
                )
            for route_id in reopened_local_links(
                row.get("route_ids"),
                original.get("route_ids"),
                epoch=bundle_epoch,
                local_pattern=WORKER_ROUTE_RE,
                global_pattern=GLOBAL_ROUTE_RE,
                label=f"asset update {asset_id} route_ids",
                errors=errors,
            ):
                route_sources_from_assets.setdefault(route_id, set()).add(asset_id)
        if seen != set(assigned_assets):
            errors.append(
                "completed worker output must update every assigned asset exactly once"
            )

    proposals = output.get("candidate_proposals", [])
    proposal_by_id: dict[str, dict[str, Any]] = {}
    proposal_anchor_keys: list[tuple[int, int, int]] = []
    worker_evidence_ids: list[str] = []
    worker_group_ids: list[str] = []
    seen_worker_group_ids: set[str] = set()
    reading_status_by_unit = {
        row.get("source_unit_id"): row.get("source_status")
        for row in reading_updates
        if isinstance(row, dict) and isinstance(row.get("source_unit_id"), str)
    }
    asset_status_by_image = {
        row.get("physical_path"): row.get("source_status")
        for row in asset_updates
        if isinstance(row, dict) and isinstance(row.get("physical_path"), str)
    }
    if isinstance(proposals, list):
        proposal_ids = [
            row.get("id")
            for row in proposals
            if isinstance(row, dict) and isinstance(row.get("id"), str)
        ]
        if not is_complete_worker_sequence(
            proposal_ids,
            "W",
            4,
        ) or len(proposal_ids) != len(proposals):
            errors.append(
                "worker candidate IDs must be a complete ordered W0001 sequence"
            )
        proposal_id_set = set(proposal_ids)
        for row in proposals:
            if not isinstance(row, dict):
                continue
            candidate_id = row.get("id", "<unknown>")
            if not isinstance(candidate_id, str):
                errors.append("candidate proposal has a non-string id")
                continue
            proposal_by_id[candidate_id] = row
            if row.get("record_status") != "ACTIVE":
                errors.append(f"worker candidate {candidate_id} must be ACTIVE")
            if row.get("evidence_reassignments") != []:
                errors.append(
                    f"worker candidate {candidate_id} cannot reassign evidence; "
                    "the coordinator owns split/merge allocation"
                )
            if row.get("discovery_stage") != manifest.get("stage"):
                errors.append(
                    f"candidate {candidate_id} discovery_stage differs from bundle"
                )
            anchor = row.get("discovery_anchor")
            if not isinstance(anchor, dict):
                errors.append(f"candidate {candidate_id} lacks a discovery anchor")
            else:
                anchor_kind = anchor.get("kind")
                anchor_id = anchor.get("id")
                anchor_ordinal = anchor.get("ordinal")
                if anchor.get("epoch") != bundle_epoch:
                    errors.append(
                        f"candidate {candidate_id} discovery epoch differs "
                        "from bundle"
                    )
                anchor_order: int | None = None
                if not isinstance(anchor_id, str):
                    errors.append(
                        f"candidate {candidate_id} anchor ID must be a string"
                    )
                elif anchor_kind == "SOURCE_UNIT":
                    anchor_order = assigned_unit_anchor_order.get(anchor_id)
                    if anchor_order is None:
                        errors.append(
                            f"candidate {candidate_id} anchor is outside assignment"
                        )
                    elif anchor_id not in row.get("source_unit_ids", []):
                        errors.append(
                            f"candidate {candidate_id} source anchor is not evidence"
                        )
                elif anchor_kind == "IMAGE":
                    anchor_order = assigned_image_anchor_order.get(anchor_id)
                    if anchor_order is None:
                        errors.append(
                            f"candidate {candidate_id} anchor is outside assignment"
                        )
                    elif anchor_id not in row.get("image_witnesses", []):
                        errors.append(
                            f"candidate {candidate_id} image anchor is not evidence"
                        )
                else:
                    errors.append(
                        f"candidate {candidate_id} SEARCH_HIT/unknown anchor "
                        "is invalid for a Stage 4–17 reading bundle"
                    )
                if (
                    anchor_order is not None
                    and isinstance(anchor_ordinal, int)
                    and not isinstance(anchor_ordinal, bool)
                    and anchor_ordinal >= 1
                    and valid_bundle_epoch
                ):
                    proposal_anchor_keys.append(
                        (
                            bundle_epoch,
                            anchor_order,
                            anchor_ordinal,
                        )
                    )
            source_ids = row.get("source_unit_ids", [])
            if isinstance(source_ids, list) and (
                not all(isinstance(item, str) for item in source_ids)
                or not set(source_ids) <= set(assigned_units)
            ):
                errors.append(
                    f"candidate {candidate_id} cites a source outside assignment"
                )
            image_ids = row.get("image_witnesses", [])
            if isinstance(image_ids, list) and (
                not all(isinstance(item, str) for item in image_ids)
                or not set(image_ids) <= assigned_image_paths
            ):
                errors.append(
                    f"candidate {candidate_id} cites an image outside assignment"
                )
            if isinstance(source_ids, list) and all(
                isinstance(item, str) for item in source_ids
            ):
                source_set = set(source_ids)
                if candidate_sources_from_reading.get(candidate_id, set()) != (
                    source_set
                ):
                    errors.append(
                        f"candidate {candidate_id} source-unit/read-ledger join differs"
                    )
            if isinstance(image_ids, list) and all(
                isinstance(item, str) for item in image_ids
            ) and candidate_images_from_assets.get(candidate_id, set()) != set(
                image_ids
            ):
                errors.append(
                    f"candidate {candidate_id} image/asset-ledger join differs"
                )
            if (
                isinstance(source_ids, list)
                and all(isinstance(item, str) for item in source_ids)
                and isinstance(image_ids, list)
                and all(isinstance(item, str) for item in image_ids)
            ):
                provenance_statuses = {
                    reading_status_by_unit.get(source_id)
                    for source_id in source_ids
                } | {
                    asset_status_by_image.get(image_path)
                    for image_path in image_ids
                }
                declared_statuses = row.get("source_status", [])
                if (
                    not isinstance(declared_statuses, list)
                    or not all(
                        isinstance(item, str) for item in declared_statuses
                    )
                    or set(declared_statuses) != provenance_statuses
                ):
                    errors.append(
                        f"candidate {candidate_id} source-status join differs"
                    )

            evidence_rows = row.get("source_evidence", [])
            evidence_by_id: dict[str, dict[str, Any]] = {}
            evidence_source_ids: set[str] = set()
            evidence_image_paths: set[str] = set()
            if isinstance(evidence_rows, list):
                for evidence in evidence_rows:
                    if not isinstance(evidence, dict):
                        continue
                    evidence_id = evidence.get("evidence_id")
                    if not isinstance(evidence_id, str) or evidence_id in evidence_by_id:
                        errors.append(
                            f"candidate {candidate_id} has invalid/duplicate evidence IDs"
                        )
                        continue
                    evidence_by_id[evidence_id] = evidence
                    worker_evidence_ids.append(evidence_id)
                    evidence_group_id = evidence.get("evidence_group_id")
                    if (
                        isinstance(evidence_group_id, str)
                        and evidence_group_id not in seen_worker_group_ids
                    ):
                        seen_worker_group_ids.add(evidence_group_id)
                        worker_group_ids.append(evidence_group_id)
                    source_id = evidence.get("source_unit_id")
                    image_path = evidence.get("image_path")
                    if source_id is None and image_path is None:
                        errors.append(
                            f"candidate {candidate_id} evidence {evidence_id} "
                            "has no source or image"
                        )
                    if isinstance(source_id, str):
                        evidence_source_ids.add(source_id)
                    if isinstance(image_path, str):
                        evidence_image_paths.add(image_path)
            if isinstance(source_ids, list) and all(
                isinstance(item, str) for item in source_ids
            ) and evidence_source_ids != set(source_ids):
                errors.append(
                    f"candidate {candidate_id} source-evidence/source-unit join differs"
                )
            if isinstance(image_ids, list) and all(
                isinstance(item, str) for item in image_ids
            ) and evidence_image_paths != set(image_ids):
                errors.append(
                    f"candidate {candidate_id} source-evidence/image join differs"
                )
            evidence_strengths = {
                evidence.get("strength")
                for evidence in evidence_by_id.values()
                if isinstance(evidence.get("strength"), str)
            }
            declared_strengths = row.get("evidence_strength", [])
            if (
                not isinstance(declared_strengths, list)
                or not all(isinstance(item, str) for item in declared_strengths)
                or set(declared_strengths) != evidence_strengths
            ):
                errors.append(
                    f"candidate {candidate_id} evidence-strength join differs"
                )

            fingerprint_references: dict[str, set[str]] = {}
            fingerprint = row.get("fingerprint", {})
            if isinstance(fingerprint, dict):
                for field, field_value in fingerprint.items():
                    if not isinstance(field_value, dict):
                        continue
                    for evidence_id in field_value.get("evidence_ids", []):
                        if isinstance(evidence_id, str):
                            fingerprint_references.setdefault(
                                evidence_id, set()
                            ).add(field)
            referenced_evidence: set[str] = set(fingerprint_references)
            for record_field in ("parameters", "variants", "related_candidate_ids"):
                records = row.get(record_field, [])
                if isinstance(records, list):
                    for record in records:
                        if isinstance(record, dict):
                            referenced_evidence.update(
                                evidence_id
                                for evidence_id in record.get("evidence_ids", [])
                                if isinstance(evidence_id, str)
                            )
            if not referenced_evidence <= set(evidence_by_id):
                errors.append(
                    f"candidate {candidate_id} references undeclared evidence"
                )
            for evidence_id, evidence in evidence_by_id.items():
                declared_fields = evidence.get("fingerprint_fields", [])
                if (
                    not isinstance(declared_fields, list)
                    or not all(isinstance(item, str) for item in declared_fields)
                    or set(declared_fields)
                    != fingerprint_references.get(evidence_id, set())
                ):
                    errors.append(
                        f"candidate {candidate_id} evidence {evidence_id} "
                        "fingerprint-field join differs"
                    )
            related_ids = row.get("related_candidate_ids", [])
            if isinstance(related_ids, list):
                relation_targets = [
                    relation.get("candidate_id")
                    for relation in related_ids
                    if isinstance(relation, dict)
                    and isinstance(relation.get("candidate_id"), str)
                ]
                if len(relation_targets) != len(related_ids) or not (
                    set(relation_targets) <= proposal_id_set
                ):
                    errors.append(
                        f"candidate {candidate_id} relates to an undeclared "
                        "worker candidate"
                    )
        if len(proposal_anchor_keys) == len(proposals):
            if proposal_anchor_keys != sorted(proposal_anchor_keys):
                errors.append(
                    "worker candidate order differs from discovery-anchor traversal"
                )
            ordinals_by_anchor: dict[tuple[int, int], list[int]] = {}
            for epoch, anchor_order, ordinal in proposal_anchor_keys:
                ordinals_by_anchor.setdefault((epoch, anchor_order), []).append(
                    ordinal
                )
            for anchor_key, ordinals in ordinals_by_anchor.items():
                if ordinals != list(range(1, len(ordinals) + 1)):
                    errors.append(
                        "worker discovery-anchor ordinals are not complete for "
                        f"anchor {anchor_key}"
                    )
        if not is_complete_worker_sequence(worker_evidence_ids, "WE", 6):
            errors.append(
                "worker evidence IDs must be a complete ordered WE000001 sequence"
            )
        if not is_complete_worker_sequence(worker_group_ids, "WG", 6):
            errors.append(
                "worker evidence-group first occurrences must be a complete "
                "ordered WG000001 sequence"
            )

    routes = output.get("route_proposals", [])
    route_ids: set[str] = set()
    route_anchor_keys: list[tuple[int, int, int]] = []
    if isinstance(routes, list):
        proposed_route_ids = [
            row.get("route_id")
            for row in routes
            if isinstance(row, dict) and isinstance(row.get("route_id"), str)
        ]
        if (
            not is_complete_worker_sequence(proposed_route_ids, "WR", 4)
            or len(proposed_route_ids) != len(routes)
        ):
            errors.append(
                "worker route IDs must be a complete ordered WR0001 sequence"
            )
        for row in routes:
            if not isinstance(row, dict):
                continue
            route_id = row.get("route_id")
            if not isinstance(route_id, str):
                errors.append("route proposal has a non-string route_id")
                continue
            if route_id in route_ids:
                errors.append(f"duplicate route proposal: {route_id}")
            route_ids.add(route_id)
            if row.get("source_unit_id") not in assigned_units:
                if row.get("discovery_kind") == "SOURCE_UNIT":
                    errors.append(
                        f"route {route_id} is outside the source assignment"
                    )
            if row.get("source_asset_id") not in assigned_assets:
                if row.get("discovery_kind") == "IMAGE":
                    errors.append(
                        f"route {route_id} is outside the asset assignment"
                    )
            if row.get("owning_stage") != str(manifest.get("stage")):
                errors.append(f"route {route_id} owning_stage differs from bundle")
            if row.get("status") != "PENDING":
                errors.append(
                    f"route {route_id} must remain PENDING for coordinator routing"
                )
            target_unit_ids = parse_string_array(
                row.get("target_unit_ids"),
                f"route {route_id} target_unit_ids",
                errors,
            )
            target_asset_ids = parse_string_array(
                row.get("target_asset_ids"),
                f"route {route_id} target_asset_ids",
                errors,
            )
            parse_string_array(
                row.get("attempts"),
                f"route {route_id} attempts",
                errors,
            )
            parse_string_array(
                row.get("vocabulary_terms"),
                f"route {route_id} vocabulary_terms",
                errors,
            )
            if target_unit_ids or target_asset_ids or row.get("defect_boundary"):
                errors.append(
                    f"route {route_id} PENDING proposal cannot claim a target "
                    "or final defect boundary"
                )
            if not row.get("literal_target") or not row.get("expected_topic"):
                errors.append(
                    f"route {route_id} lacks its literal target or expected topic"
                )
            if row.get("discovery_epoch") != str(
                bundle_epoch
            ):
                errors.append(
                    f"route {route_id} discovery_epoch differs from bundle"
                )
            ordinal_text = row.get("discovery_ordinal")
            ordinal = (
                int(ordinal_text)
                if isinstance(ordinal_text, str)
                and re.fullmatch(r"[1-9][0-9]*", ordinal_text)
                else None
            )
            if ordinal is None:
                errors.append(
                    f"route {route_id} discovery_ordinal must be a canonical "
                    "positive integer string"
                )
            anchor_order: int | None = None
            if row.get("discovery_kind") == "SOURCE_UNIT":
                if row.get("source_asset_id") or row.get("discovery_id") != row.get(
                    "source_unit_id"
                ):
                    errors.append(f"route {route_id} source-unit anchor differs")
                else:
                    anchor_order = assigned_unit_anchor_order.get(
                        row.get("source_unit_id")
                    )
                if route_sources_from_reading.get(route_id, set()) != {
                    row.get("source_unit_id")
                } or route_sources_from_assets.get(route_id, set()):
                    errors.append(f"route {route_id} reading-ledger join differs")
            elif row.get("discovery_kind") == "IMAGE":
                if row.get("source_unit_id") or row.get("discovery_id") != row.get(
                    "source_asset_id"
                ):
                    errors.append(f"route {route_id} image anchor differs")
                else:
                    anchor_order = assigned_asset_anchor_order.get(
                        row.get("source_asset_id")
                    )
                if route_sources_from_assets.get(route_id, set()) != {
                    row.get("source_asset_id")
                } or route_sources_from_reading.get(route_id, set()):
                    errors.append(f"route {route_id} asset-ledger join differs")
            else:
                errors.append(
                    f"route {route_id} SEARCH_HIT/unknown discovery is invalid "
                    "for a Stage 4–17 reading bundle"
                )
            if (
                anchor_order is not None
                and ordinal is not None
                and valid_bundle_epoch
            ):
                route_anchor_keys.append(
                    (
                        bundle_epoch,
                        anchor_order,
                        ordinal,
                    )
                )
        if set(route_sources_from_reading) | set(
            route_sources_from_assets
        ) != route_ids:
            errors.append(
                "reading/asset route IDs differ from worker route proposals"
            )
        if len(route_anchor_keys) == len(routes):
            if route_anchor_keys != sorted(route_anchor_keys):
                errors.append(
                    "worker route order differs from discovery-anchor traversal"
                )
            ordinals_by_anchor: dict[tuple[int, int], list[int]] = {}
            for epoch, anchor_order, ordinal in route_anchor_keys:
                ordinals_by_anchor.setdefault((epoch, anchor_order), []).append(
                    ordinal
                )
            for anchor_key, ordinals in ordinals_by_anchor.items():
                if ordinals != list(range(1, len(ordinals) + 1)):
                    errors.append(
                        "worker route discovery ordinals are not complete for "
                        f"anchor {anchor_key}"
                    )

    for candidate_id, row in proposal_by_id.items():
        cross_reference_ids = row.get("cross_reference_ids", [])
        if isinstance(cross_reference_ids, list) and (
            not all(isinstance(item, str) for item in cross_reference_ids)
            or not set(cross_reference_ids) <= route_ids
        ):
            errors.append(
                f"candidate {candidate_id} references an undeclared worker route"
            )
    linked_candidate_ids = set(candidate_sources_from_reading) | set(
        candidate_images_from_assets
    )
    if linked_candidate_ids != set(proposal_by_id):
        errors.append(
            "reading/asset candidate IDs differ from worker candidate proposals"
        )


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
    try:
        trusted_guardrails = json.loads(
            (GOAL_DIR / "guardrails.json").read_text(encoding="utf-8")
        )
        text_patterns = compile_blind_text_patterns(trusted_guardrails)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"cannot load blind free-text patterns: {exc}")
        text_patterns = ()
    for match in blind_text_matches(
        manifest,
        text_patterns,
        "allowed_manifest",
    ):
        errors.append(f"bundle manifest contains forbidden blind priming: {match}")
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
    discovery_epoch = manifest.get("discovery_epoch")
    if (
        not isinstance(discovery_epoch, int)
        or isinstance(discovery_epoch, bool)
        or discovery_epoch < 1
    ):
        errors.append("bundle discovery_epoch must be a positive integer")
    source_paths = manifest.get("source_paths")
    if not isinstance(source_paths, list) or not source_paths or not all(
        is_safe_relative_path(path) for path in source_paths
    ):
        errors.append(
            "bundle source_paths must be nonempty, unique, and canonically ordered"
        )
        source_paths = []
    elif len(source_paths) != len(set(source_paths)):
        errors.append(
            "bundle source_paths must be nonempty, unique, and canonically ordered"
        )
        source_paths = []
    else:
        try:
            corpus_manifest = json.loads(
                (GOAL_DIR / "corpus-manifest.json").read_text(encoding="utf-8")
            )
            canonical_paths = [
                path
                for path in ordered_stage_paths(corpus_manifest, stage)
                if path in set(source_paths)
            ]
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            canonical_paths = []
        if source_paths != canonical_paths:
            errors.append(
                "bundle source_paths must follow canonical manifest order"
            )
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
        "coordinator_merge_validation_required": True,
        "worker_search_allowed": False,
        "worker_route_resolution_allowed": False,
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
            elif not path.is_file() and not path.is_dir():
                errors.append(f"bundle contains a special filesystem entry: {relative}")
    if manifest_path.exists() and manifest_path.stat().st_mode & 0o222:
        errors.append("bundle manifest is writable")
    if manifest_path.exists() and manifest_path.stat().st_nlink != 1:
        errors.append("bundle manifest is hard-linked")
    output_root = bundle / "output"
    if (
        not output_root.is_dir()
        or output_root.is_symlink()
        or not output_root.stat().st_mode & 0o200
    ):
        errors.append("bundle output directory must be a writable real directory")
    worker_output_path = output_root / "output.json"
    if (
        worker_output_path.exists()
        and not worker_output_path.is_symlink()
        and worker_output_path.stat().st_nlink != 1
    ):
        errors.append("worker output file is hard-linked")

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
        and isinstance(discovery_epoch, int)
        and source_paths
        and prompt_bytes
        != brief(worker_id, stage, discovery_epoch, source_paths).encode("utf-8")
    ):
        errors.append("bundle brief differs from its declared assignment")
    for match in blind_text_matches(brief_text, text_patterns, "brief"):
        errors.append(f"bundle brief contains forbidden blind priming: {match}")

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
    unit_ids = [unit.get("id") for unit in units]
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
        or list(dict.fromkeys(unit_paths)) != source_paths
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

    source_files = (
        {
            path.relative_to(input_root / "sources").as_posix()
            for path in (input_root / "sources").rglob("*")
            if path.is_file()
        }
        if (input_root / "sources").is_dir()
        else set()
    )
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
    image_files = (
        {
            path.relative_to(input_root / "images").as_posix()
            for path in (input_root / "images").rglob("*")
            if path.is_file()
        }
        if (input_root / "images").is_dir()
        else set()
    )
    if image_files != expected_images:
        errors.append("bundled image paths differ from the asset assignment")

    derived_input_files = {
        "input/brief.md",
        "input/guardrails.json",
        "input/source-units.jsonl",
        "input/reading-input.csv",
        "input/asset-input.csv",
        *(f"input/schemas/{name}" for name in SCHEMA_NAMES),
        *(f"input/sources/{path}" for path in source_paths),
        *(f"input/images/{path}" for path in expected_images),
    }
    if set(actual_files) != derived_input_files:
        errors.append(
            "bundle input files differ from the exact derived assignment projection"
        )

    try:
        authoritative_units = [
            json.loads(line)
            for line in (GOAL_DIR / "source-units.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line
        ]
        expected_units = [
            unit for unit in authoritative_units if unit["path"] in source_paths
        ]
        expected_unit_bytes = b"".join(
            (
                json.dumps(unit, sort_keys=True, separators=(",", ":")) + "\n"
            ).encode()
            for unit in expected_units
        )
        if (input_root / "source-units.jsonl").read_bytes() != expected_unit_bytes:
            errors.append("bundled source units differ from the authoritative projection")

        expected_reading = [
            row
            for row in read_csv(GOAL_DIR / "reading-ledger.csv")
            if row["path"] in source_paths
        ]
        if (input_root / "reading-input.csv").read_bytes() != csv_bytes(
            READING_HEADER,
            expected_reading,
        ):
            errors.append("reading input differs from the authoritative projection")

        expected_assets = [
            row
            for row in read_csv(GOAL_DIR / "asset-ledger.csv")
            if row["assignment_path"] in source_paths
        ]
        if (input_root / "asset-input.csv").read_bytes() != csv_bytes(
            ASSET_HEADER,
            expected_assets,
        ):
            errors.append("asset input differs from the authoritative projection")

        for source_path in source_paths:
            if (input_root / "sources" / source_path).read_bytes() != (
                SOURCE_ROOT / source_path
            ).read_bytes():
                errors.append(
                    f"bundled source differs from authoritative source: {source_path}"
                )
        for image_path in expected_images:
            if (input_root / "images" / image_path).read_bytes() != (
                SOURCE_ROOT / image_path
            ).read_bytes():
                errors.append(
                    f"bundled image differs from authoritative image: {image_path}"
                )
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        errors.append(f"cannot verify authoritative bundle projection: {exc}")

    forbidden_parts = {
        ".git",
        "goal-1",
        "goal-2",
        "src",
        "api.md",
        "simple_programs.md",
    }
    for relative in allowed_root_files:
        if forbidden_parts & set(Path(relative).parts):
            errors.append(f"bundle contains prohibited path: {relative}")

    _validate_worker_output(
        bundle,
        manifest,
        errors,
        require_completed_output,
        text_patterns,
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
    parser.add_argument(
        "--epoch",
        type=int,
        default=1,
        help="positive blind-discovery epoch (1 for the initial pass)",
    )
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
                print(
                    "verified sealed blind-worker bundle and completed output; "
                    "coordinator canonical-ID allocation and merge validation "
                    "remain required"
                )
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
            args.epoch,
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
