#!/usr/bin/env python3
"""Prepare and safely finalize a nonsemantic blind-review output worksheet.

This tool never assigns a reading disposition, source status, visual role,
risk flag, evidence statement, candidate, route, or uncertainty.  It copies
the immutable bundle projections into ``output/output.json`` and leaves every
human judgment visibly incomplete.  The existing bundle verifier remains the
authority for a completed output.

Mutating commands serialize with other invocations of this helper through an
advisory lock on the bundle's output directory.  Editors and other
non-cooperating writers must be quiescent while a mutating command runs.
"""

from __future__ import annotations

import argparse
import csv
import fcntl
import hashlib
import json
import os
import stat
import sys
import tempfile
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterator

import build_worker_bundle
from audit_contract import (
    ASSET_HEADER,
    READING_DISPOSITIONS,
    READING_HEADER,
    SECONDARY_ROLES,
    SOURCE_STATUSES,
    VISUAL_RISK_FLAGS,
    VISUAL_ROLES,
    canonical_json_bytes,
)


OUTPUT_FIELDS = (
    "worker_id",
    "bundle_sha256",
    "prompt_sha256",
    "schema_sha256",
    "allowed_manifest_sha256",
    "prohibited_input_nonuse",
    "reading_updates",
    "candidate_proposals",
    "asset_updates",
    "route_proposals",
    "uncertainties",
)
DECLARATION_FIELDS = OUTPUT_FIELDS[:5]
READING_IMMUTABLE_FIELDS = READING_HEADER[
    : READING_HEADER.index("review_status")
]
ASSET_IMMUTABLE_FIELDS = ASSET_HEADER[
    : ASSET_HEADER.index("inspection_status")
]
FINAL_ORIGINAL_RESOLUTION_STATUSES = {"NOT_REQUIRED", "REVIEWED"}
FINAL_TRANSCRIPTION_STATUSES = {
    "NOT_APPLICABLE",
    "NOT_REQUIRED",
    "CHECKED",
}


class PreparationError(ValueError):
    """The worksheet cannot be prepared or finalized safely."""


@contextmanager
def output_lock(bundle: Path) -> Iterator[None]:
    """Serialize cooperating worksheet operations without adding bundle files."""

    output_dir = bundle / "output"
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    try:
        descriptor = os.open(output_dir, flags)
    except OSError as exc:
        raise PreparationError(f"cannot open bundle output directory: {exc}") from exc
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)


def load_csv_exact(path: Path, header: list[str], label: str) -> list[dict[str, str]]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != header:
                raise PreparationError(
                    f"{label} header differs from the frozen contract"
                )
            rows = list(reader)
    except (OSError, csv.Error) as exc:
        raise PreparationError(f"cannot load {label}: {exc}") from exc
    if any(None in row for row in rows):
        raise PreparationError(f"{label} contains an over-wide row")
    return rows


def load_manifest(bundle: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            (bundle / "allowed-manifest.json").read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise PreparationError(f"cannot load bundle manifest: {exc}") from exc
    if not isinstance(value, dict):
        raise PreparationError("bundle manifest is not an object")
    return value


def expected_template(bundle: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    try:
        manifest_digest = hashlib.sha256(
            (bundle / "allowed-manifest.json").read_bytes()
        ).hexdigest()
        return {
            "worker_id": manifest["worker_id"],
            "bundle_sha256": manifest["content_set_sha256"],
            "prompt_sha256": manifest["prompt_sha256"],
            "schema_sha256": manifest["schema_sha256"],
            "allowed_manifest_sha256": manifest_digest,
            "prohibited_input_nonuse": False,
            "reading_updates": [],
            "candidate_proposals": [],
            "asset_updates": [],
            "route_proposals": [],
            "uncertainties": [],
        }
    except (KeyError, OSError) as exc:
        raise PreparationError(f"bundle manifest is incomplete: {exc}") from exc


def load_output(bundle: Path) -> tuple[bytes, dict[str, Any]]:
    path = bundle / "output" / "output.json"
    try:
        payload = path.read_bytes()
        value = json.loads(payload)
    except (OSError, json.JSONDecodeError) as exc:
        raise PreparationError(f"cannot load worker output: {exc}") from exc
    if not isinstance(value, dict):
        raise PreparationError("worker output is not an object")
    return payload, value


def verify_static_bundle(
    bundle: Path,
    template: dict[str, Any],
) -> None:
    """Verify every bundle input while substituting the pristine output value."""

    errors = build_worker_bundle.verify_bundle(
        bundle,
        worker_output_override=template,
    )
    if errors:
        raise PreparationError(
            "bundle verification failed:\n- " + "\n- ".join(errors)
        )


def scaffold_reading(row: dict[str, str]) -> dict[str, str]:
    result = {field: row[field] for field in READING_IMMUTABLE_FIELDS}
    result.update(
        {
            "review_status": "PENDING",
            "review_epoch": "",
            "review_disposition": "",
            "source_status": "",
            "uncertainty": "",
            "secondary_roles": "",
            # Existing global links are immutable across a reopened pass.
            "candidate_ids": row["candidate_ids"],
            "route_ids": row["route_ids"],
            "evidence_statement": "",
            "review_stage": "",
            "reviewer": "",
        }
    )
    return {field: result[field] for field in READING_HEADER}


def scaffold_asset(row: dict[str, str]) -> dict[str, str]:
    result = {field: row[field] for field in ASSET_IMMUTABLE_FIELDS}
    result.update(
        {
            "inspection_status": "PENDING",
            "review_epoch": "",
            "visual_role": "",
            "source_status": "",
            "risk_flags": "",
            "original_resolution_status": "",
            "transcription_status": "",
            # Existing global links are immutable across a reopened pass.
            "candidate_ids": row["candidate_ids"],
            "route_ids": row["route_ids"],
            "evidence_statement": "",
            "review_stage": "",
            "reviewer": "",
            "uncertainty": "",
        }
    )
    return {field: result[field] for field in ASSET_HEADER}


def scaffold_output(
    template: dict[str, Any],
    reading: list[dict[str, str]],
    assets: list[dict[str, str]],
) -> dict[str, Any]:
    output = deepcopy(template)
    output["reading_updates"] = [scaffold_reading(row) for row in reading]
    output["asset_updates"] = [scaffold_asset(row) for row in assets]
    return output


def validate_top_level_identity(
    output: dict[str, Any],
    template: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    if set(output) != set(OUTPUT_FIELDS):
        errors.append("worker output fields differ from the frozen contract")
        return errors
    for field in DECLARATION_FIELDS:
        if output.get(field) != template[field]:
            errors.append(f"worker output declaration differs: {field}")
    if not isinstance(output.get("prohibited_input_nonuse"), bool):
        errors.append("prohibited_input_nonuse must be boolean")
    for field in (
        "reading_updates",
        "candidate_proposals",
        "asset_updates",
        "route_proposals",
        "uncertainties",
    ):
        if not isinstance(output.get(field), list):
            errors.append(f"worker output {field} must be an array")
    return errors


def validate_row_identity(
    updates: object,
    assigned: list[dict[str, str]],
    *,
    header: list[str],
    immutable_fields: list[str],
    id_field: str,
    label: str,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(updates, list):
        return [f"{label} updates must be an array"]
    assigned_by_id = {row[id_field]: row for row in assigned}
    expected_ids = [row[id_field] for row in assigned]
    actual_ids: list[str] = []
    seen: set[str] = set()
    for index, update in enumerate(updates):
        if not isinstance(update, dict):
            errors.append(f"{label} update {index} is not an object")
            continue
        if set(update) != set(header):
            errors.append(f"{label} update {index} fields differ from the contract")
            continue
        non_string_fields = [
            field for field in header if not isinstance(update.get(field), str)
        ]
        if non_string_fields:
            errors.append(
                f"{label} update {index} has non-string fields: "
                + ",".join(non_string_fields)
            )
            continue
        identifier = update.get(id_field)
        if not isinstance(identifier, str):
            errors.append(f"{label} update {index} has a non-string identity")
            continue
        actual_ids.append(identifier)
        if identifier in seen:
            errors.append(f"duplicate {label} update: {identifier}")
            continue
        seen.add(identifier)
        original = assigned_by_id.get(identifier)
        if original is None:
            errors.append(f"{label} update lies outside the assignment: {identifier}")
            continue
        changed = [
            field
            for field in immutable_fields
            if update.get(field) != original.get(field)
        ]
        if changed:
            errors.append(
                f"{label} update changes immutable identity {identifier}: "
                + ",".join(changed)
            )
    if actual_ids != expected_ids:
        missing = [identifier for identifier in expected_ids if identifier not in seen]
        extra = [
            identifier
            for identifier in actual_ids
            if identifier not in assigned_by_id
        ]
        if missing:
            errors.append(f"{label} assignment rows are missing: {','.join(missing)}")
        if extra:
            errors.append(f"{label} assignment rows are unknown: {','.join(extra)}")
        if not missing and not extra:
            errors.append(f"{label} updates are not in assignment order")
    return errors


def resume_rows(
    updates: object,
    assigned: list[dict[str, str]],
    *,
    header: list[str],
    immutable_fields: list[str],
    id_field: str,
    label: str,
    scaffold,
) -> list[dict[str, str]]:
    if not isinstance(updates, list):
        raise PreparationError(f"{label} updates must be an array")
    assigned_by_id = {row[id_field]: row for row in assigned}
    existing_by_id: dict[str, dict[str, str]] = {}
    for index, update in enumerate(updates):
        if not isinstance(update, dict) or set(update) != set(header):
            raise PreparationError(
                f"{label} update {index} fields differ from the contract"
            )
        non_string_fields = [
            field for field in header if not isinstance(update.get(field), str)
        ]
        if non_string_fields:
            raise PreparationError(
                f"{label} update {index} has non-string fields: "
                + ",".join(non_string_fields)
            )
        identifier = update.get(id_field)
        if not isinstance(identifier, str):
            raise PreparationError(
                f"{label} update {index} has a non-string identity"
            )
        if identifier not in assigned_by_id:
            raise PreparationError(
                f"{label} update {index} has an unknown assignment identity"
            )
        if identifier in existing_by_id:
            raise PreparationError(f"duplicate {label} update: {identifier}")
        original = assigned_by_id[identifier]
        changed = [
            field
            for field in immutable_fields
            if update.get(field) != original.get(field)
        ]
        if changed:
            raise PreparationError(
                f"{label} update changes immutable identity {identifier}: "
                + ",".join(changed)
            )
        existing_by_id[identifier] = update
    return [
        deepcopy(existing_by_id.get(row[id_field], scaffold(row)))
        for row in assigned
    ]


def parse_string_array(
    value: object,
    *,
    allowed: set[str] | None = None,
) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return False
    if (
        not isinstance(parsed, list)
        or not all(isinstance(item, str) for item in parsed)
        or len(parsed) != len(set(parsed))
    ):
        return False
    return allowed is None or all(item in allowed for item in parsed)


def reading_incomplete(
    row: dict[str, str],
    *,
    epoch: int,
    stage: int,
    worker_id: str,
) -> list[str]:
    fields: list[str] = []
    if row["review_status"] != "REVIEWED":
        fields.append("review_status")
    if row["review_epoch"] != str(epoch):
        fields.append("review_epoch")
    if row["review_disposition"] not in READING_DISPOSITIONS:
        fields.append("review_disposition")
    if row["source_status"] not in SOURCE_STATUSES:
        fields.append("source_status")
    if not parse_string_array(
        row["secondary_roles"],
        allowed=set(SECONDARY_ROLES),
    ):
        fields.append("secondary_roles")
    if not parse_string_array(row["candidate_ids"]):
        fields.append("candidate_ids")
    if not parse_string_array(row["route_ids"]):
        fields.append("route_ids")
    if not row["evidence_statement"].strip():
        fields.append("evidence_statement")
    if row["review_stage"] != str(stage):
        fields.append("review_stage")
    if row["reviewer"] != worker_id:
        fields.append("reviewer")
    if row["source_status"] == "CLEAR" and row["uncertainty"]:
        fields.append("uncertainty(clear_requires_empty)")
    if row["source_status"] in {"AMBIGUOUS", "DEFECTIVE", "CONFLICTING"} and not row[
        "uncertainty"
    ].strip():
        fields.append("uncertainty(nonclear_requires_text)")
    return fields


def asset_incomplete(
    row: dict[str, str],
    *,
    epoch: int,
    stage: int,
    worker_id: str,
) -> list[str]:
    fields: list[str] = []
    if row["inspection_status"] != "SCREENED":
        fields.append("inspection_status")
    if row["review_epoch"] != str(epoch):
        fields.append("review_epoch")
    if row["visual_role"] not in VISUAL_ROLES:
        fields.append("visual_role")
    if row["source_status"] not in SOURCE_STATUSES:
        fields.append("source_status")
    if not parse_string_array(
        row["risk_flags"],
        allowed=set(VISUAL_RISK_FLAGS),
    ):
        fields.append("risk_flags")
    if row["original_resolution_status"] not in FINAL_ORIGINAL_RESOLUTION_STATUSES:
        fields.append("original_resolution_status")
    if row["transcription_status"] not in FINAL_TRANSCRIPTION_STATUSES:
        fields.append("transcription_status")
    if not parse_string_array(row["candidate_ids"]):
        fields.append("candidate_ids")
    if not parse_string_array(row["route_ids"]):
        fields.append("route_ids")
    if not row["evidence_statement"].strip():
        fields.append("evidence_statement")
    if row["review_stage"] != str(stage):
        fields.append("review_stage")
    if row["reviewer"] != worker_id:
        fields.append("reviewer")
    if row["source_status"] == "CLEAR" and row["uncertainty"]:
        fields.append("uncertainty(clear_requires_empty)")
    if row["source_status"] in {"AMBIGUOUS", "DEFECTIVE", "CONFLICTING"} and not row[
        "uncertainty"
    ].strip():
        fields.append("uncertainty(nonclear_requires_text)")
    return fields


def incomplete_human_fields(
    output: dict[str, Any],
    manifest: dict[str, Any],
) -> list[str]:
    findings: list[str] = []
    epoch = manifest.get("discovery_epoch")
    stage = manifest.get("stage")
    worker_id = manifest.get("worker_id")
    if (
        not isinstance(epoch, int)
        or isinstance(epoch, bool)
        or not isinstance(stage, int)
        or isinstance(stage, bool)
        or not isinstance(worker_id, str)
    ):
        return ["bundle manifest lacks valid worker/stage/epoch metadata"]
    for row in output["reading_updates"]:
        missing = reading_incomplete(
            row,
            epoch=epoch,
            stage=stage,
            worker_id=worker_id,
        )
        if missing:
            findings.append(
                f"reading {row['source_unit_id']}: " + ",".join(missing)
            )
    for row in output["asset_updates"]:
        missing = asset_incomplete(
            row,
            epoch=epoch,
            stage=stage,
            worker_id=worker_id,
        )
        if missing:
            findings.append(f"asset {row['asset_id']}: " + ",".join(missing))
    return findings


def atomic_replace(path: Path, payload: bytes, expected: bytes) -> None:
    """Replace one regular output file atomically if its snapshot is unchanged."""

    try:
        before = path.lstat()
    except OSError as exc:
        raise PreparationError(f"cannot stat worker output: {exc}") from exc
    if (
        not stat.S_ISREG(before.st_mode)
        or path.is_symlink()
        or before.st_nlink != 1
    ):
        raise PreparationError("worker output must be one regular non-linked file")
    if path.read_bytes() != expected:
        raise PreparationError("worker output changed during preparation")

    descriptor = -1
    temporary_name = ""
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=".prepare-review-output-",
            suffix=".tmp",
            dir=path.parent,
        )
        os.fchmod(descriptor, stat.S_IMODE(before.st_mode))
        with os.fdopen(descriptor, "wb") as handle:
            descriptor = -1
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        if path.read_bytes() != expected:
            raise PreparationError("worker output changed before atomic replacement")
        os.replace(temporary_name, path)
        temporary_name = ""
    except OSError as exc:
        raise PreparationError(
            f"cannot atomically replace worker output: {exc}"
        ) from exc
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if temporary_name:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass


def bundle_state(
    bundle: Path,
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    list[dict[str, str]],
    list[dict[str, str]],
    bytes,
    dict[str, Any],
]:
    manifest = load_manifest(bundle)
    template = expected_template(bundle, manifest)
    verify_static_bundle(bundle, template)
    reading = load_csv_exact(
        bundle / "input" / "reading-input.csv",
        READING_HEADER,
        "reading input",
    )
    assets = load_csv_exact(
        bundle / "input" / "asset-input.csv",
        ASSET_HEADER,
        "asset input",
    )
    original_bytes, output = load_output(bundle)
    return manifest, template, reading, assets, original_bytes, output


def prepare(bundle: Path, *, resume: bool = False) -> tuple[bool, int, int]:
    bundle = bundle.resolve()
    with output_lock(bundle):
        (
            _manifest,
            template,
            reading,
            assets,
            original_bytes,
            output,
        ) = bundle_state(bundle)
        expected = scaffold_output(template, reading, assets)
        if not resume:
            if output == expected:
                return False, len(reading), len(assets)
            if output != template:
                raise PreparationError(
                    "worker output contains non-template work; use --resume "
                    "to preserve row work after identity checks"
                )
            proposed = expected
        else:
            errors = validate_top_level_identity(output, template)
            if errors:
                raise PreparationError("\n- ".join(errors))
            if output["prohibited_input_nonuse"] is not False:
                raise PreparationError(
                    "--resume requires an unfinalized false declaration"
                )
            for field in (
                "candidate_proposals",
                "route_proposals",
                "uncertainties",
            ):
                if output[field] != []:
                    raise PreparationError(
                        f"--resume refuses nonempty {field}; it only proves "
                        "row-assignment identity"
                    )
            proposed = deepcopy(output)
            proposed["reading_updates"] = resume_rows(
                output["reading_updates"],
                reading,
                header=READING_HEADER,
                immutable_fields=READING_IMMUTABLE_FIELDS,
                id_field="source_unit_id",
                label="reading",
                scaffold=scaffold_reading,
            )
            proposed["asset_updates"] = resume_rows(
                output["asset_updates"],
                assets,
                header=ASSET_HEADER,
                immutable_fields=ASSET_IMMUTABLE_FIELDS,
                id_field="asset_id",
                label="asset",
                scaffold=scaffold_asset,
            )
        if proposed == output:
            return False, len(reading), len(assets)
        atomic_replace(
            bundle / "output" / "output.json",
            canonical_json_bytes(proposed),
            original_bytes,
        )
        return True, len(reading), len(assets)


def check(
    bundle: Path,
) -> tuple[list[str], list[str], bool]:
    bundle = bundle.resolve()
    with output_lock(bundle):
        (
            manifest,
            template,
            reading,
            assets,
            _original_bytes,
            output,
        ) = bundle_state(bundle)
        identity_errors = validate_top_level_identity(output, template)
        if not identity_errors:
            identity_errors.extend(
                validate_row_identity(
                    output["reading_updates"],
                    reading,
                    header=READING_HEADER,
                    immutable_fields=READING_IMMUTABLE_FIELDS,
                    id_field="source_unit_id",
                    label="reading",
                )
            )
            identity_errors.extend(
                validate_row_identity(
                    output["asset_updates"],
                    assets,
                    header=ASSET_HEADER,
                    immutable_fields=ASSET_IMMUTABLE_FIELDS,
                    id_field="asset_id",
                    label="asset",
                )
            )
        if identity_errors:
            return identity_errors, [], bool(
                output.get("prohibited_input_nonuse")
            )
        incomplete = incomplete_human_fields(output, manifest)
        if incomplete:
            return [], incomplete, output["prohibited_input_nonuse"]
        validation_value = deepcopy(output)
        validation_value["prohibited_input_nonuse"] = True
        verifier_errors = build_worker_bundle.verify_bundle(
            bundle,
            require_completed_output=True,
            worker_output_override=validation_value,
        )
        return verifier_errors, [], output["prohibited_input_nonuse"]


def finalize_declaration(bundle: Path) -> bool:
    bundle = bundle.resolve()
    with output_lock(bundle):
        (
            manifest,
            template,
            reading,
            assets,
            original_bytes,
            output,
        ) = bundle_state(bundle)
        identity_errors = validate_top_level_identity(output, template)
        if not identity_errors:
            identity_errors.extend(
                validate_row_identity(
                    output["reading_updates"],
                    reading,
                    header=READING_HEADER,
                    immutable_fields=READING_IMMUTABLE_FIELDS,
                    id_field="source_unit_id",
                    label="reading",
                )
            )
            identity_errors.extend(
                validate_row_identity(
                    output["asset_updates"],
                    assets,
                    header=ASSET_HEADER,
                    immutable_fields=ASSET_IMMUTABLE_FIELDS,
                    id_field="asset_id",
                    label="asset",
                )
            )
        if identity_errors:
            raise PreparationError(
                "worker output identity validation failed:\n- "
                + "\n- ".join(identity_errors)
            )
        incomplete = incomplete_human_fields(output, manifest)
        if incomplete:
            raise PreparationError(
                "human review fields remain incomplete:\n- "
                + "\n- ".join(incomplete)
            )
        proposed = deepcopy(output)
        proposed["prohibited_input_nonuse"] = True
        verifier_errors = build_worker_bundle.verify_bundle(
            bundle,
            require_completed_output=True,
            worker_output_override=proposed,
        )
        if verifier_errors:
            raise PreparationError(
                "completed worker output verification failed:\n- "
                + "\n- ".join(verifier_errors)
            )
        if output["prohibited_input_nonuse"] is True:
            return False
        atomic_replace(
            bundle / "output" / "output.json",
            canonical_json_bytes(proposed),
            original_bytes,
        )
        return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    action = parser.add_mutually_exclusive_group()
    action.add_argument(
        "--resume",
        action="store_true",
        help=(
            "preserve existing row judgments after proving exact assignment "
            "identity; candidate/route/uncertainty proposals must still be empty"
        ),
    )
    action.add_argument(
        "--check",
        action="store_true",
        help="report incomplete human fields without writing",
    )
    action.add_argument(
        "--finalize-declaration",
        action="store_true",
        help=(
            "set prohibited_input_nonuse=true only after the complete output "
            "passes the existing verifier"
        ),
    )
    args = parser.parse_args()

    try:
        if args.check:
            errors, incomplete, finalized = check(args.bundle)
            if errors:
                for error in errors:
                    print(f"ERROR: {error}", file=sys.stderr)
                return 1
            if incomplete:
                for finding in incomplete:
                    print(f"INCOMPLETE: {finding}")
                print(
                    f"review output incomplete: {len(incomplete)} assigned "
                    "rows require human completion"
                )
                return 1
            state = "true" if finalized else "false (ready to finalize)"
            print(
                "review output human fields are complete and verifier-compatible; "
                f"prohibited_input_nonuse={state}"
            )
            return 0
        if args.finalize_declaration:
            changed = finalize_declaration(args.bundle)
            verb = "finalized" if changed else "already finalized"
            print(f"{verb} verified worker output declaration: {args.bundle}")
            return 0
        changed, reading_count, asset_count = prepare(
            args.bundle,
            resume=args.resume,
        )
        verb = "prepared" if changed else "already prepared"
        print(
            f"{verb} nonsemantic review worksheet: {args.bundle}; "
            f"reading_updates={reading_count} asset_updates={asset_count}; "
            "prohibited_input_nonuse=false"
        )
        return 0
    except (OSError, PreparationError, ValueError, json.JSONDecodeError) as exc:
        print(f"review-output preparation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
