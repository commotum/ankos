#!/usr/bin/env python3
"""Fail-closed validation for the Goal 4 Stage 3 witness state."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlsplit


class WitnessError(ValueError):
    """Raised when witness policy, provenance, or source-blocked state drifts."""


EXPECTED_BASELINE_LOCK_SHA256 = "57224a1f1ba8333bbc900b23ff6127a189649feb01c279f30fac05a305658863"
EXPECTED_STRUCTURE_SHA256 = "6f9891417f458ca1e40385082b4f230e780d72362a783f35e11648082a743d49"
EXPECTED_HELD_OUT_SHA256 = "c09f32e0eefe580eddf6d250706795c4c784532dbbe502ac1a0bf04306541fb9"
EXPECTED_LICENSING_SHA256 = "e946c7e3daf398597b42abef855432f4c304a1f3514d85e0aa0a1dde68ee03b1"
EXPECTED_RAW_BLOCK_IDS_LF_SHA256 = "46b5af25479de19aeca26f39b86c8e78c54b168d33365615ee9f3934f7a58779"
EXPECTED_SELECTED_IDS_SHA256 = "94e489a0ad2ecc85da9554478b417c771f5eeb5d901561ccf56781292f2ac9ad"

EXPECTED_SEGMENTS = [
    "PUBLICATION_AND_CONTENTS",
    "PREFACE",
    "CH01",
    "CH02",
    "CH03",
    "CH04",
    "CH05",
    "CH06",
    "CH07",
    "CH08",
    "CH09",
    "CH10",
    "CH11",
    "CH12",
    "GENERAL_NOTES",
    "N01",
    "N02",
    "N03",
    "N04",
    "N05",
    "N06",
    "N07",
    "N08",
    "N09",
    "N10",
    "N11",
    "N12",
    "INDEX",
    "COLOPHON",
]

EXPECTED_CONTENT_CLASSES = [
    "AUTHOR_TEXT",
    "AUTHOR_VISUAL",
    "SEMANTIC_LAYOUT",
    "PAGE_FURNITURE",
    "BLANK",
    "NONCONTENT_ARTIFACT",
]
EXPECTED_LEGIBILITY_AXES = [
    "PROSE_AND_PUNCTUATION",
    "FORMULA_CODE_AND_DATA",
    "FIGURE_CAPTION_AND_COLOR",
    "INDEX_ENTRY_AND_COLUMN",
]
EXPECTED_NOT_APPLICABLE = [
    "BLANK_PAGE",
    "RUNNING_HEADER",
    "PRINTED_PAGE_NUMBER",
    "SCANNER_OR_EXTRACTION_ARTIFACT",
    "NONAUTHORIAL_BINDING_OR_CROP",
]
EXPECTED_BLOCKERS = [
    "WITNESS-PERMISSION",
    "WITNESS-COMPLETE-CENSUS",
    "WITNESS-INDEX-LAYOUT",
    "WITNESS-EDITION-MATCH",
    "WITNESS-INDEPENDENT-REVIEW",
]
EXPECTED_UNRESOLVED = [
    "UNRESOLVED-WITNESS-0001",
    "UNRESOLVED-WITNESS-0002",
    "UNRESOLVED-WITNESS-0003",
    "UNRESOLVED-WITNESS-0004",
]
ALLOWED_PUBLIC_HOSTS = {
    "files.wolframcdn.com",
    "www.wolfram-media.com",
    "www.wolfram.com",
    "www.wolframscience.com",
}
FORBIDDEN_WITNESS_EXTENSIONS = {
    ".djvu",
    ".epub",
    ".gif",
    ".jpeg",
    ".jpg",
    ".pdf",
    ".png",
    ".tif",
    ".tiff",
    ".webp",
}
FORBIDDEN_MAGIC = (
    b"%PDF-",
    b"\x89PNG\r\n\x1a\n",
    b"\xff\xd8\xff",
    b"GIF87a",
    b"GIF89a",
    b"II*\x00",
    b"MM\x00*",
    b"AT&TFORM",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise WitnessError(message)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as error:
        raise WitnessError(f"cannot hash required file {path}: {error}") from error
    return digest.hexdigest()


def _reject_floats(value: Any) -> None:
    if isinstance(value, float):
        raise WitnessError("witness JSON forbids floating-point values")
    if isinstance(value, dict):
        for key, child in value.items():
            require(isinstance(key, str), "witness JSON object key is not a string")
            _reject_floats(child)
    elif isinstance(value, list):
        for child in value:
            _reject_floats(child)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise WitnessError(f"cannot load JSON {path}: {error}") from error
    require(isinstance(value, dict), f"JSON root must be an object: {path}")
    _reject_floats(value)
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        raise WitnessError(f"cannot load JSONL {path}: {error}") from error
    for number, line in enumerate(lines, 1):
        require(line != "", f"blank JSONL line at {path}:{number}")
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            raise WitnessError(f"invalid JSONL at {path}:{number}: {error}") from error
        require(isinstance(row, dict), f"JSONL row is not an object at {path}:{number}")
        _reject_floats(row)
        rows.append(row)
    return rows


def stable_json_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return sha256_bytes(payload)


def canonical_json_bytes(value: Any, *, terminal_lf: bool = True) -> bytes:
    _reject_floats(value)
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return payload + (b"\n" if terminal_lf else b"")


def canonical_jsonl_bytes(rows: list[dict[str, Any]]) -> bytes:
    return b"".join(canonical_json_bytes(row) for row in rows)


def lf_sequence_sha256(values: Iterable[str]) -> str:
    return sha256_bytes("".join(f"{value}\n" for value in values).encode("utf-8"))


def _exact_list(value: Any, expected: list[str], label: str) -> None:
    require(isinstance(value, list), f"{label} must be an array")
    require(value == expected, f"{label} drift")
    require(len(value) == len(set(value)), f"{label} contains duplicates")


def _validate_public_url(value: Any, label: str) -> str:
    require(isinstance(value, str), f"{label} must be a string")
    parsed = urlsplit(value)
    require(parsed.scheme == "https", f"{label} must use HTTPS")
    require(parsed.hostname in ALLOWED_PUBLIC_HOSTS, f"{label} uses an unapproved host")
    require(parsed.username is None and parsed.password is None, f"{label} contains credentials")
    require(parsed.port is None, f"{label} contains an unexpected port")
    require(parsed.query == "" and parsed.fragment == "", f"{label} must be a stable clean URL")
    require(parsed.path.startswith("/"), f"{label} has no absolute URL path")
    return value


def _reject_private_paths(value: Any, label: str = "root") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = key.lower()
            require(
                lowered not in {"mount_path", "credential", "credentials", "cookie", "token", "drm_key"},
                f"private mount or credential field recorded at {label}.{key}",
            )
            _reject_private_paths(child, f"{label}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_private_paths(child, f"{label}[{index}]")
    elif isinstance(value, str):
        require(not value.startswith(("/home/", "/Users/", "file://")), f"private path recorded at {label}")


def _validate_binding_files(root: Path, bindings: dict[str, Any], *, include_licensing: bool) -> None:
    require(isinstance(bindings, dict), "baseline_bindings must be an object")
    expected = {
        "baseline_lock_sha256": EXPECTED_BASELINE_LOCK_SHA256,
        "structure_ledger_sha256": EXPECTED_STRUCTURE_SHA256,
        "held_out_sample_sha256": EXPECTED_HELD_OUT_SHA256,
    }
    if include_licensing:
        expected["licensing_contract_sha256"] = EXPECTED_LICENSING_SHA256
    require(bindings == expected, "witness baseline binding values drift")
    files = {
        "baseline_lock_sha256": root / "goal-4/baseline-lock.json",
        "structure_ledger_sha256": root / "goal-4/structure-ledger.jsonl",
        "held_out_sample_sha256": root / "goal-4/held-out-sample.json",
        "licensing_contract_sha256": root / "goal-4/licensing-contract.json",
    }
    for key in expected:
        require(sha256_file(files[key]) == expected[key], f"bound file hash drift: {files[key]}")


def validate_contract(contract: dict[str, Any], root: Path) -> None:
    require(contract.get("contract_id") == "ANKOS-WITNESS-1", "witness contract ID drift")
    require(contract.get("version") == "1.0.0", "witness contract version drift")
    require(
        contract.get("status") == "FROZEN_STAGE_3_SCHEMA_SOURCE_BLOCKED",
        "witness contract status drift",
    )
    require(contract.get("frozen_on") == "2026-07-14", "witness contract date drift")
    _validate_binding_files(root, contract.get("baseline_bindings"), include_licensing=True)

    target = contract.get("target_edition")
    require(isinstance(target, dict), "target_edition must be an object")
    require(target.get("title") == "A New Kind of Science", "target title drift")
    require(target.get("author") == "Stephen Wolfram", "target author drift")
    require(target.get("edition") == "First edition", "target edition drift")
    require(target.get("printing") == "Fourth printing", "target printing drift")
    require(target.get("hardcover_isbn_10") == "1-57955-008-8", "target ISBN-10 drift")
    require(target.get("hardcover_isbn_13") == "978-1-57955-008-0", "target ISBN-13 drift")
    require(target.get("identity_state") == "OFFICIAL_ONLINE_SURFACE_IDENTIFIED_LOCAL_OCR_MATCH_UNPROVEN", "edition proof state drift")

    _exact_list(contract.get("content_classes"), EXPECTED_CONTENT_CLASSES, "content classes")
    _exact_list(contract.get("legibility_axes"), EXPECTED_LEGIBILITY_AXES, "legibility axes")
    _exact_list(contract.get("not_applicable_reasons"), EXPECTED_NOT_APPLICABLE, "not-applicable reasons")
    require(len(contract.get("required_unit_fields", [])) == 20, "required witness unit fields drift")
    require(len(contract.get("required_region_fields", [])) == 14, "required witness region fields drift")

    coverage = contract.get("coverage_policy")
    require(isinstance(coverage, dict), "coverage policy must be an object")
    for key in (
        "unit_order_must_be_total",
        "unit_ids_must_be_unique",
        "regions_must_partition_each_unit_without_gap_or_overlap",
        "authorial_regions_must_map_or_block",
        "not_applicable_requires_independent_review",
        "official_count_conflicts_must_remain_explicit",
    ):
        require(coverage.get(key) is True, f"coverage gate disabled: {key}")
    for key in (
        "missing_or_illegible_authorial_region_may_be_not_applicable",
        "one_source_census_may_force_1280_count",
    ):
        require(coverage.get(key) is False, f"coverage refusal weakened: {key}")

    held_out = contract.get("held_out_policy")
    require(isinstance(held_out, dict), "held-out policy must be an object")
    require(held_out.get("selected_count") == 1125, "held-out count drift")
    require(held_out.get("selected_raw_block_ids_sha256") == EXPECTED_SELECTED_IDS_SHA256, "held-out ID binding drift")
    require(held_out.get("proposal_fields_allowed_in_blind_packet") is False, "proposal leakage allowed")
    require(held_out.get("repair_outcomes_allowed_in_blind_packet") is False, "repair outcome leakage allowed")
    require(held_out.get("reviewer_and_proposer_must_differ") is True, "review independence disabled")

    storage = contract.get("storage_policy")
    require(isinstance(storage, dict), "storage policy must be an object")
    require(storage.get("witness_bytes_inside_repository_allowed") is False, "repository witness payload allowed")
    require(storage.get("witness_bytes_inside_repaired_release_allowed") is False, "release witness payload allowed")
    require(storage.get("credentials_or_private_mount_paths_recorded") is False, "secret recording allowed")
    require(storage.get("authorized_mount_must_be_read_only") is True, "read-only mount gate disabled")

    gates = contract.get("stage_gates")
    require(isinstance(gates, dict), "stage gates must be an object")
    require(gates.get("stage_3_complete_requires_full_authorized_census") is True, "Stage 3 completion gate weakened")
    require(gates.get("stage_3_source_blocked_allows_stage_4_schema_pipeline") is True, "Stage 4 dependency-independent gate drift")
    require(gates.get("stage_3_source_blocked_allows_author_text_correction") is False, "source-blocked text correction allowed")
    require(gates.get("stage_3_source_blocked_allows_full_repair_claim") is False, "source-blocked full claim allowed")
    _reject_private_paths(contract)


def validate_registry(registry: dict[str, Any]) -> None:
    require(registry.get("schema_version") == "1.0.0", "witness registry schema drift")
    require(registry.get("status") == "CANDIDATES_RECORDED_NO_PRIMARY_WITNESS_ACQUIRED", "witness registry status drift")
    require(registry.get("inspected_on") == "2026-07-14", "witness registry inspection date drift")
    sources = registry.get("sources")
    require(isinstance(sources, list) and len(sources) == 1, "witness source registry must contain one assessed candidate")
    source = sources[0]
    require(source.get("source_id") == "OFFICIAL_NKS_ONLINE", "official source ID drift")
    _validate_public_url(source.get("root_url"), "official source root")
    require(source.get("source_state") == "REMOTE_INTERACTIVE_ONLY", "official source access state drift")
    require(source.get("automated_or_ai_use_state") == "USE_NOT_AUTHORIZED", "official AI use state weakened")
    require(source.get("bulk_acquisition_state") == "USE_NOT_AUTHORIZED", "official bulk use state weakened")
    require(source.get("local_storage_state") == "NOT_ACQUIRED", "official source falsely acquired")
    require(source.get("redistribution_allowed") is False, "official source redistribution falsely allowed")

    identity = source.get("edition_identity")
    require(isinstance(identity, dict), "source edition identity must be an object")
    _validate_public_url(identity.get("copyright_page_url"), "copyright page")
    require(identity.get("edition") == "First edition", "source edition drift")
    require(identity.get("printing") == "Fourth printing", "source printing drift")
    require(identity.get("local_ocr_equivalence_proven") is False, "local OCR equivalence falsely claimed")

    sentinels = source.get("verified_public_sentinels")
    require(isinstance(sentinels, list) and len(sentinels) == 7, "public sentinel inventory drift")
    require(len(set(sentinels)) == len(sentinels), "duplicate public sentinel")
    for index, url in enumerate(sentinels):
        _validate_public_url(url, f"public sentinel {index}")

    permissions = source.get("permission_records")
    require(isinstance(permissions, list) and len(permissions) == 3, "permission record inventory drift")
    expected_permission_ids = [
        "NKS_BOOK_COPYRIGHT_2002",
        "WOLFRAM_SCIENCE_TERMS",
        "WOLFRAM_GENERAL_TERMS_2024",
    ]
    require([row.get("permission_record_id") for row in permissions] == expected_permission_ids, "permission record IDs drift")
    for row in permissions:
        _validate_public_url(row.get("url"), f"permission URL {row.get('permission_record_id')}")
        require(row.get("snapshot_sha256") is None, "unretained terms snapshot has a hash")
        require(row.get("snapshot_state") == "NOT_RETAINED", "terms snapshot state drift")

    claims = registry.get("official_count_claims")
    require(isinstance(claims, list) and len(claims) == 4, "official count claim inventory drift")
    expected_claims = [
        ("PRODUCT_PAGE_COUNT", 1280),
        ("COLOPHON_COUNT", 1280),
        ("CITATION_PAGE_COUNT", 1197),
        ("COLOPHON_PRINTED_LOCATION", 1264),
    ]
    require([(row.get("claim_id"), row.get("count")) for row in claims] == expected_claims, "official count conflicts were normalized or drifted")
    for row in claims:
        _validate_public_url(row.get("source_url"), f"count claim URL {row.get('claim_id')}")
    require(registry.get("count_reconciliation_state") == "UNRESOLVED_DO_NOT_FORCE", "count conflict falsely resolved")
    _reject_private_paths(registry)


def _load_structure_summary(root: Path) -> tuple[list[str], list[str]]:
    rows = load_jsonl(root / "goal-4/structure-ledger.jsonl")
    segments = [row for row in rows if row.get("record_type") == "SEGMENT"]
    blocks = [row for row in rows if row.get("record_type") == "RAW_BLOCK"]
    require(len(segments) == 29, "structure ledger segment count drift")
    require(len(blocks) == 20430, "structure ledger raw block count drift")
    segments.sort(key=lambda row: row.get("order"))
    segment_ids = [row.get("segment_id") for row in segments]
    require(segment_ids == EXPECTED_SEGMENTS, "structure ledger segment order drift")
    block_ids = [row.get("raw_block_id") for row in blocks]
    require(all(isinstance(value, str) for value in block_ids), "raw block ID is not a string")
    require(len(block_ids) == len(set(block_ids)), "duplicate raw block ID")
    require(block_ids == [f"RAW-{index:06d}" for index in range(1, 20431)], "raw block ID sequence drift")
    require(lf_sequence_sha256(block_ids) == EXPECTED_RAW_BLOCK_IDS_LF_SHA256, "raw block universe hash drift")
    require(all(row.get("segment_id") in set(EXPECTED_SEGMENTS) for row in blocks), "raw block references unknown segment")
    return segment_ids, block_ids


def _structure_rows(root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows = load_jsonl(root / "goal-4/structure-ledger.jsonl")
    segments = sorted(
        (row for row in rows if row.get("record_type") == "SEGMENT"),
        key=lambda row: row.get("order"),
    )
    blocks = [row for row in rows if row.get("record_type") == "RAW_BLOCK"]
    require([row.get("segment_id") for row in segments] == EXPECTED_SEGMENTS, "segment ledger order drift")
    require(len(blocks) == 20430, "raw block ledger count drift")
    return segments, blocks


def _expected_dimensions(blocks: list[dict[str, Any]], segment_id: str) -> list[str]:
    risks = {row.get("risk_stratum") for row in blocks}
    dimensions: list[str] = []
    if segment_id != "INDEX":
        dimensions.append("PROSE_AND_PUNCTUATION")
    if "FORMULA_CODE_RULE_OR_DATA" in risks:
        dimensions.append("FORMULA_CODE_AND_DATA")
    if "FIGURE_CAPTION_OR_VISUAL" in risks:
        dimensions.append("FIGURE_CAPTION_AND_COLOR")
    if segment_id == "INDEX" or "INDEX_COLUMN_OR_ENTRY" in risks:
        dimensions.append("INDEX_ENTRY_AND_COLUMN")
    return dimensions


def validate_region_ledger(
    root: Path,
    rows: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    path = root / "goal-4/witness-region-ledger.jsonl"
    if rows is None:
        rows = load_jsonl(path)
        require(path.read_bytes() == canonical_jsonl_bytes(rows), "witness region ledger serialization drift")
    require(len(rows) == 29, "witness region ledger row count drift")
    segments, blocks = _structure_rows(root)
    expected_fields = {
        "blocker_ids",
        "canonical_document_id",
        "canonical_path",
        "coverage_id",
        "coverage_status",
        "order",
        "raw_block_count",
        "raw_block_ids_sha256",
        "raw_segment_sha256",
        "record_type",
        "repair_authorized",
        "required_risk_dimensions",
        "schema_version",
        "segment_id",
        "unresolved_ids",
        "witness_region_ids",
        "witness_unit_ids",
    }
    all_block_ids: list[str] = []
    for order, (row, segment) in enumerate(zip(rows, segments, strict=True)):
        require(set(row) == expected_fields, f"witness gap row schema drift: {order}")
        segment_id = segment["segment_id"]
        segment_blocks = [item for item in blocks if item.get("segment_id") == segment_id]
        block_ids = [item["raw_block_id"] for item in segment_blocks]
        all_block_ids.extend(block_ids)
        require(row.get("schema_version") == "1.0.0", f"witness gap schema version drift: {segment_id}")
        require(row.get("record_type") == "SEGMENT_SOURCE_GAP", f"witness gap record type drift: {segment_id}")
        require(row.get("coverage_id") == f"WITNESS-GAP-{order + 1:04d}", f"witness coverage ID drift: {segment_id}")
        require(row.get("order") == order, f"witness gap order drift: {segment_id}")
        require(row.get("segment_id") == segment_id, f"witness gap segment drift: {segment_id}")
        require(row.get("canonical_document_id") == segment_id, f"witness canonical ID drift: {segment_id}")
        require(row.get("canonical_path") == segment["canonical_path"], f"witness canonical path drift: {segment_id}")
        require(row.get("raw_segment_sha256") == segment["raw_segment_sha256"], f"witness raw segment hash drift: {segment_id}")
        require(row.get("raw_block_count") == len(block_ids), f"witness gap block count drift: {segment_id}")
        require(row.get("raw_block_ids_sha256") == stable_json_sha256(block_ids), f"witness gap block hash drift: {segment_id}")
        require(row.get("required_risk_dimensions") == _expected_dimensions(segment_blocks, segment_id), f"witness gap risk dimensions drift: {segment_id}")
        require(row.get("witness_unit_ids") == [], f"phantom witness unit in source gap: {segment_id}")
        require(row.get("witness_region_ids") == [], f"phantom witness region in source gap: {segment_id}")
        require(row.get("coverage_status") == "SOURCE_BLOCKED", f"false witness coverage: {segment_id}")
        expected_blockers = [
            "WITNESS-PERMISSION",
            "WITNESS-COMPLETE-CENSUS",
            "WITNESS-EDITION-MATCH",
            "WITNESS-INDEPENDENT-REVIEW",
        ]
        if segment_id == "INDEX":
            expected_blockers.insert(2, "WITNESS-INDEX-LAYOUT")
        require(row.get("blocker_ids") == expected_blockers, f"witness gap blockers drift: {segment_id}")
        require(row.get("unresolved_ids") == EXPECTED_UNRESOLVED, f"witness gap unresolved links drift: {segment_id}")
        require(row.get("repair_authorized") is False, f"unauthorized witness repair enabled: {segment_id}")
    require(all_block_ids == [f"RAW-{index:06d}" for index in range(1, 20431)], "witness segment gaps do not cover raw blocks exactly once in order")
    return rows


def validate_unresolved_ledger(
    root: Path,
    rows: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    path = root / "goal-4/witness-unresolved.jsonl"
    if rows is None:
        rows = load_jsonl(path)
        require(path.read_bytes() == canonical_jsonl_bytes(rows), "witness unresolved ledger serialization drift")
    require(len(rows) == 4, "witness unresolved row count drift")
    expected_kinds = [
        "COMPLETE_PRIMARY_WITNESS_NOT_ACQUIRED",
        "AUTHORIZED_AUTOMATED_USE_NOT_ESTABLISHED",
        "RAW_EDITION_IDENTITY_NOT_ESTABLISHED",
        "PHYSICAL_UNIT_REGION_CENSUS_NOT_DERIVED",
    ]
    forbidden_leak_fields = {
        "answer",
        "candidate_text",
        "proposed_repair",
        "repair_outcome",
        "witness_transcription",
    }
    for index, row in enumerate(rows):
        require(not forbidden_leak_fields.intersection(row), f"held-out proposal or answer leakage in unresolved row {index}")
        require(row.get("schema_version") == "1.0.0", f"unresolved schema version drift: {index}")
        require(row.get("unresolved_id") == EXPECTED_UNRESOLVED[index], f"unresolved ID/order drift: {index}")
        require(row.get("kind") == expected_kinds[index], f"unresolved kind drift: {index}")
        require(row.get("workflow_state") == "SOURCE_BLOCKED", f"unresolved workflow falsely advanced: {index}")
        require(row.get("severity") == "RELEASE_BLOCKER", f"unresolved severity weakened: {index}")
        require(row.get("owner_stage") == "3-WITNESSES", f"unresolved owner drift: {index}")
        require(row.get("source_candidate_ids") == ["OFFICIAL_NKS_ONLINE"], f"unresolved source drift: {index}")
        require(row.get("affected_segment_ids") == EXPECTED_SEGMENTS, f"unresolved segment scope drift: {index}")
        require(row.get("affected_raw_block_count") == 20430, f"unresolved block count drift: {index}")
        require(row.get("affected_raw_block_ids_lf_sha256") == EXPECTED_RAW_BLOCK_IDS_LF_SHA256, f"unresolved block hash drift: {index}")
        require(row.get("affected_legacy_asset_count") == 1444, f"unresolved asset count drift: {index}")
        require(row.get("affected_held_out_sample_count") == 1125, f"unresolved held-out count drift: {index}")
        require(row.get("affected_held_out_sample_sha256") == EXPECTED_SELECTED_IDS_SHA256, f"unresolved held-out hash drift: {index}")
        require(row.get("repair_authorized") is False, f"unresolved repair falsely authorized: {index}")
        require(row.get("final_disposition") is None, f"source-blocked unresolved item has a disposition: {index}")
        for key in ("impact", "attempted_alternatives", "unblock_actions", "release_blocker_codes"):
            require(row.get(key), f"unresolved row lacks {key}: {index}")
    return rows


def validate_lock(root: Path, lock: dict[str, Any] | None = None) -> dict[str, Any]:
    path = root / "goal-4/witness-lock.json"
    if lock is None:
        lock = load_json(path)
        require(path.read_bytes() == canonical_json_bytes(lock), "witness lock serialization drift")
    require(lock.get("schema_version") == "1.0.0", "witness lock schema drift")
    require(lock.get("status") == "FROZEN_STAGE_3_SOURCE_BLOCKED", "witness lock status drift")
    expected_artifacts = [
        "goal-4/witness-contract.json",
        "goal-4/witness-mount-contract.md",
        "goal-4/witness-region-ledger.jsonl",
        "goal-4/witness-source-registry.json",
        "goal-4/witness-state.json",
        "goal-4/witness-unresolved.jsonl",
    ]
    artifacts = lock.get("artifacts")
    require(isinstance(artifacts, list), "witness lock artifacts must be an array")
    require([row.get("path") for row in artifacts] == expected_artifacts, "witness lock artifact inventory/order drift")
    for row in artifacts:
        artifact = root / row["path"]
        require(artifact.is_file() and not artifact.is_symlink(), f"locked witness artifact missing or unsafe: {artifact}")
        require(row.get("byte_size") == artifact.stat().st_size, f"locked witness artifact size drift: {artifact}")
        require(row.get("sha256") == sha256_file(artifact), f"locked witness artifact hash drift: {artifact}")
    expected_sources = [
        "goal-4/tests/test_witness.py",
        "goal-4/tools/capture_witness.py",
        "goal-4/tools/witness_lib.py",
    ]
    sources = lock.get("sources")
    require(isinstance(sources, list), "witness lock sources must be an array")
    require([row.get("path") for row in sources] == expected_sources, "witness lock source inventory/order drift")
    for row in sources:
        source = root / row["path"]
        require(source.is_file() and not source.is_symlink(), f"locked witness source missing or unsafe: {source}")
        require(row.get("byte_size") == source.stat().st_size, f"locked witness source size drift: {source}")
        require(row.get("sha256") == sha256_file(source), f"locked witness source hash drift: {source}")
    expected_bindings = {
        "baseline_lock_sha256": sha256_file(root / "goal-4/baseline-lock.json"),
        "corpus_manifest_sha256": sha256_file(root / "goal-4/corpus-manifest.json"),
        "fidelity_contract_sha256": sha256_file(root / "goal-4/fidelity-contract.md"),
        "guardrails_sha256": sha256_file(root / "goal-4/guardrails.json"),
        "held_out_sample_sha256": EXPECTED_HELD_OUT_SHA256,
        "licensing_contract_sha256": sha256_file(root / "goal-4/licensing-contract.json"),
        "review_contract_sha256": sha256_file(root / "goal-4/review-contract.md"),
        "structure_ledger_sha256": EXPECTED_STRUCTURE_SHA256,
    }
    require(lock.get("bindings") == expected_bindings, "witness lock prerequisite bindings drift")
    return lock


def validate_external_lock_root(root: Path, expected_sha256: str) -> None:
    require(re.fullmatch(r"[0-9a-f]{64}", expected_sha256) is not None, "external witness lock pin is malformed")
    require(
        sha256_file(root / "goal-4/witness-lock.json") == expected_sha256,
        "external witness lock root drift",
    )


def _validate_held_out(root: Path, block_ids: list[str]) -> None:
    held_out = load_json(root / "goal-4/held-out-sample.json")
    selected = held_out.get("selected_raw_block_ids")
    require(isinstance(selected, list), "held-out selected IDs must be an array")
    require(held_out.get("selected_count") == len(selected) == 1125, "held-out selected count drift")
    require(len(selected) == len(set(selected)), "held-out selected IDs contain duplicates")
    require(set(selected).issubset(set(block_ids)), "held-out sample references unknown raw block")
    derived = stable_json_sha256(selected)
    require(derived == EXPECTED_SELECTED_IDS_SHA256, "held-out selected ID hash drift")
    require(held_out.get("selected_raw_block_ids_sha256") == derived, "held-out declared ID hash drift")


def validate_state(state: dict[str, Any], registry: dict[str, Any], root: Path) -> None:
    require(state.get("schema_version") == "1.0.0", "witness state schema drift")
    require(state.get("contract_id") == "ANKOS-WITNESS-1", "witness state contract ID drift")
    require(state.get("status") == "SOURCE_BLOCKED", "witness state must remain SOURCE_BLOCKED")
    require(state.get("recorded_on") == "2026-07-14", "witness state date drift")
    _validate_binding_files(root, state.get("baseline_bindings"), include_licensing=False)
    require(state.get("candidate_source_ids") == ["OFFICIAL_NKS_ONLINE"], "candidate source binding drift")
    require(
        state.get("candidate_source_ids") == [row.get("source_id") for row in registry.get("sources", [])],
        "witness state and source registry disagree",
    )

    acquisition = state.get("acquisition")
    require(isinstance(acquisition, dict), "witness acquisition state must be an object")
    for key in (
        "primary_witness_acquired",
        "witness_bytes_in_repository",
        "witness_bytes_in_repaired_release",
        "authorized_read_only_mount_configured",
    ):
        require(acquisition.get(key) is False, f"source-blocked acquisition falsely enabled: {key}")
    for key in ("permission_or_license_id", "unit_manifest_path", "region_manifest_path"):
        require(acquisition.get(key) is None, f"source-blocked acquisition field must be null: {key}")

    segment_ids, block_ids = _load_structure_summary(root)
    _validate_held_out(root, block_ids)
    _exact_list(state.get("blocked_segment_ids"), segment_ids, "blocked segment IDs")

    coverage = state.get("coverage")
    require(isinstance(coverage, dict), "witness coverage must be an object")
    require(coverage.get("unit_universe_state") == "UNKNOWN_SOURCE_BLOCKED", "unit universe falsely known")
    require(coverage.get("witness_unit_count") == 0, "source-blocked state has witness units")
    require(coverage.get("witness_region_count") == 0, "source-blocked state has witness regions")
    require(coverage.get("covered_segment_count") == 0, "source-blocked state has covered segments")
    require(coverage.get("blocked_segment_count") == len(segment_ids) == 29, "blocked segment count drift")
    require(coverage.get("raw_block_count") == len(block_ids) == 20430, "blocked raw block count drift")
    require(coverage.get("raw_block_ids_lf_sha256") == lf_sequence_sha256(block_ids), "blocked raw block universe hash drift")
    require(coverage.get("held_out_selected_count") == 1125, "blocked held-out count drift")
    require(coverage.get("held_out_selected_raw_block_ids_sha256") == EXPECTED_SELECTED_IDS_SHA256, "blocked held-out hash drift")

    blockers = state.get("blockers")
    require(isinstance(blockers, list), "witness blockers must be an array")
    require([row.get("blocker_id") for row in blockers] == EXPECTED_BLOCKERS, "witness blocker inventory drift")
    require(len(EXPECTED_BLOCKERS) == len(set(row.get("blocker_id") for row in blockers)), "duplicate witness blocker")
    for row in blockers:
        require(row.get("state") == "OPEN", f"source blocker falsely closed: {row.get('blocker_id')}")
        for key in ("scope", "reason", "unblock_action", "release_impact"):
            require(isinstance(row.get(key), str) and row[key].strip(), f"incomplete blocker field: {row.get('blocker_id')}.{key}")

    gates = state.get("stage_gates")
    require(isinstance(gates, dict), "witness state gates must be an object")
    expected_gates = {
        "stage_3": "SOURCE_BLOCKED",
        "stage_4_dependency_independent_pipeline_work": "ALLOWED",
        "stage_5_zero_repair_structure_work": "ALLOWED_AFTER_STAGE_4",
        "author_text_correction": "BLOCKED",
        "full_repair_claim": "BLOCKED",
    }
    require(gates == expected_gates, "witness stage gates drift")
    _reject_private_paths(state)


def scan_for_forbidden_witness_payloads(goal_root: Path) -> None:
    require(goal_root.is_dir(), f"Goal 4 root is missing: {goal_root}")
    for path in sorted(goal_root.rglob("*"), key=lambda item: item.as_posix()):
        require(not path.is_symlink(), f"symlink under Goal 4 is forbidden: {path}")
        if not path.is_file():
            continue
        require(path.suffix.lower() not in FORBIDDEN_WITNESS_EXTENSIONS, f"forbidden witness-like payload extension: {path}")
        try:
            prefix = path.read_bytes()[:16]
        except OSError as error:
            raise WitnessError(f"cannot inspect Goal 4 payload {path}: {error}") from error
        require(not any(prefix.startswith(magic) for magic in FORBIDDEN_MAGIC), f"forbidden witness-like payload magic: {path}")


def validate_all(
    root: Path,
    *,
    contract: dict[str, Any] | None = None,
    registry: dict[str, Any] | None = None,
    state: dict[str, Any] | None = None,
    scan_payloads: bool = True,
) -> dict[str, Any]:
    root = root.resolve(strict=True)
    contract = contract or load_json(root / "goal-4/witness-contract.json")
    registry = registry or load_json(root / "goal-4/witness-source-registry.json")
    state = state or load_json(root / "goal-4/witness-state.json")
    validate_contract(contract, root)
    validate_registry(registry)
    validate_state(state, registry, root)
    validate_region_ledger(root)
    validate_unresolved_ledger(root)
    validate_lock(root)
    if scan_payloads:
        scan_for_forbidden_witness_payloads(root / "goal-4")
    return {
        "status": "SOURCE_BLOCKED",
        "candidate_sources": 1,
        "blocked_segments": 29,
        "blocked_raw_blocks": 20430,
        "blocked_held_out_items": 1125,
        "forbidden_witness_payloads": 0,
        "segment_source_gap_rows": 29,
        "unresolved_witness_rows": 4,
        "stage_4_dependency_independent_work": "ALLOWED",
    }
