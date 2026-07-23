#!/usr/bin/env python3
"""Validate Goal 4 blind-audit ledgers, joins, queues, and phase barriers."""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import verify_corpus
from audit_contract import (
    ASSET_HEADER,
    CANDIDATE_FIELDS,
    CANDIDATE_CHANGE_ACTIONS,
    CANDIDATE_CHANGE_FIELDS,
    CROSS_REFERENCE_HEADER,
    EVIDENCE_MODALITIES,
    EVIDENCE_STRENGTHS,
    FIELD_SUPPORT_STATUSES,
    FINGERPRINT_FIELDS,
    FORBIDDEN_BLIND_FIELDS,
    GOAL_DIR,
    LIFECYCLE_PROOF_KINDS,
    MERGE_IDENTITY_PROOF_KINDS,
    READING_DISPOSITIONS,
    READING_HEADER,
    READING_REVIEW_RESULT_FIELDS,
    REVIEW_HISTORY_FIELDS,
    REVIEW_MODES,
    REPO_ROOT,
    ROUTE_CLOSURE_SCOPES,
    ROUTE_KINDS,
    ROUTE_STATUSES,
    SEARCH_HIT_DISPOSITIONS,
    SEARCH_ENRICHMENT_TRIGGER_KINDS,
    SECONDARY_ROLES,
    SOURCE_STATUSES,
    VISUAL_RISK_FLAGS,
    VISUAL_ROLES,
    ASSET_REVIEW_RESULT_FIELDS,
    canonical_sha256,
    canonical_json_bytes,
    close_review_event,
    review_event_sha256,
    review_input_projection,
    review_result_projection,
    schema_documents,
)


MANIFEST_PATH = GOAL_DIR / "corpus-manifest.json"
UNITS_PATH = GOAL_DIR / "source-units.jsonl"
READING_PATH = GOAL_DIR / "reading-ledger.csv"
CANDIDATE_PATH = GOAL_DIR / "candidate-ledger.jsonl"
CROSS_REFERENCE_PATH = GOAL_DIR / "cross-reference-ledger.csv"
ASSET_PATH = GOAL_DIR / "asset-ledger.csv"
SEARCH_PATH = GOAL_DIR / "search-rounds.json"
REVIEW_HISTORY_PATH = GOAL_DIR / "review-history.jsonl"
SCHEMA_DIR = GOAL_DIR / "schemas"

HEX64 = re.compile(r"^[0-9a-f]{64}$")
B_ID = re.compile(r"^B[0-9]{4}$")
E_ID = re.compile(r"^E[0-9]{6}$")
G_ID = re.compile(r"^G[0-9]{6}$")
Q_ID = re.compile(r"^Q[0-9]{4}$")
H_ID = re.compile(r"^H[0-9]{6}$")
V_ID = re.compile(r"^V[0-9]{6}$")
PAGE_NUMBER = re.compile(r"_page_(\d+)")
SEARCH_QUERY_FIELDS = frozenset(
    {
        "query_id",
        "family",
        "pattern",
        "mode",
        "case_sensitive",
        "whole_word",
        "scope_paths",
    }
)


def load_csv(path: Path, expected_header: list[str]) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != expected_header:
            raise ValueError(
                f"{path.name} header mismatch: {reader.fieldnames!r}"
            )
        return list(reader)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path.name}:{line_number}: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path.name}:{line_number}: row is not an object")
        rows.append(value)
    return rows


def parse_array(
    value: str,
    label: str,
    errors: list[str],
) -> list[Any]:
    try:
        result = json.loads(value)
    except json.JSONDecodeError:
        errors.append(f"{label} is not JSON")
        return []
    if not isinstance(result, list):
        errors.append(f"{label} must be a JSON array")
        return []
    return result


def forbidden_keys(value: Any, path: str = "$") -> list[str]:
    failures: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in FORBIDDEN_BLIND_FIELDS:
                failures.append(f"{path}.{key}")
            failures.extend(forbidden_keys(nested, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            failures.extend(forbidden_keys(nested, f"{path}[{index}]"))
    return failures


def blind_text_leaks(value: Any, patterns: list[re.Pattern[str]], path: str) -> list[str]:
    failures: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            failures.extend(blind_text_leaks(nested, patterns, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            failures.extend(
                blind_text_leaks(nested, patterns, f"{path}[{index}]")
            )
    elif isinstance(value, str):
        for pattern in patterns:
            if pattern.search(value):
                failures.append(f"{path} matches {pattern.pattern!r}")
    return failures


def load_blind_text_patterns() -> tuple[list[re.Pattern[str]], list[str]]:
    errors: list[str] = []
    try:
        guardrails = json.loads(
            (GOAL_DIR / "guardrails.json").read_text(encoding="utf-8")
        )
        raw_patterns = guardrails["blind_schema_policy"][
            "free_text_review_patterns"
        ]
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        return [], [f"cannot load blind free-text patterns: {exc}"]
    if not isinstance(raw_patterns, list):
        return [], ["blind free-text patterns are not an array"]
    compiled: list[re.Pattern[str]] = []
    for raw in raw_patterns:
        try:
            compiled.append(re.compile(raw, re.IGNORECASE))
        except (TypeError, re.error) as exc:
            errors.append(f"invalid blind free-text pattern {raw!r}: {exc}")
    return compiled, errors


def stage_for_document(document: dict[str, Any]) -> int:
    kind = document["kind"]
    if kind in {
        "publication_and_printed_contents",
        "preface",
        "general_notes",
        "colophon",
    }:
        return 4
    if kind in {"chapter", "chapter_notes"}:
        return 4 + int(document["chapter_number"])
    if kind == "index":
        return 17
    raise ValueError(f"no audit stage for document kind {kind}")


def exact_string_list(
    value: Any,
    label: str,
    errors: list[str],
    *,
    nonempty: bool = False,
) -> list[str]:
    if not isinstance(value, list):
        errors.append(f"{label} must be an array")
        return []
    if any(not isinstance(item, str) or not item.strip() for item in value):
        errors.append(f"{label} must contain nonempty strings")
    if len(value) != len(set(value)):
        errors.append(f"{label} contains duplicates")
    if nonempty and not value:
        errors.append(f"{label} must not be empty")
    return [item for item in value if isinstance(item, str)]


def parsed_string_list(
    value: str,
    label: str,
    errors: list[str],
) -> list[str]:
    parsed = parse_array(value, label, errors)
    return exact_string_list(parsed, label, errors)


def expected_asset_assignments(
    manifest: dict[str, Any],
) -> tuple[dict[str, dict[str, str]], list[str]]:
    """Recompute each physical image's exact owner from canonical manifest data."""
    errors: list[str] = []
    documents = {document["path"]: document for document in manifest["documents"]}
    image_links = {
        link["resolved_path"]: link
        for link in manifest["links"]
        if link["kind"] == "image"
    }
    page_ranges: dict[str, tuple[int, int]] = {}
    for document in manifest["documents"]:
        pages = [
            int(match.group(1))
            for image_path in document["image_references"]
            if (match := PAGE_NUMBER.search(Path(image_path).name))
        ]
        if pages:
            page_ranges[document["path"]] = (min(pages), max(pages))

    expected: dict[str, dict[str, str]] = {}
    for image in manifest["images"]:
        path = image["path"]
        link = image_links.get(path)
        if link is not None:
            assignment_path = link["source_path"]
            expected[path] = {
                "link_id": link["id"],
                "source_path": link["source_path"],
                "source_unit_id": link["source_unit_id"] or "",
                "assignment_path": assignment_path,
                "assignment_stage": str(
                    stage_for_document(documents[assignment_path])
                ),
                "assignment_basis": "LIVE_MARKDOWN_REFERENCE",
                "reference_status": "REFERENCED",
            }
            continue

        match = PAGE_NUMBER.search(Path(path).name)
        page = int(match.group(1)) if match else None
        owners = [
            document_path
            for document_path, (first_page, last_page) in page_ranges.items()
            if page is not None
            and first_page <= page <= last_page
            and Path(document_path).parent == Path(path).parent
        ]
        if len(owners) != 1:
            errors.append(
                f"manifest image {path} has non-unique inferred owner: {owners}"
            )
            continue
        assignment_path = owners[0]
        expected[path] = {
            "link_id": "",
            "source_path": "",
            "source_unit_id": "",
            "assignment_path": assignment_path,
            "assignment_stage": str(
                stage_for_document(documents[assignment_path])
            ),
            "assignment_basis": "UNIQUE_DIRECTORY_PAGE_RANGE",
            "reference_status": "UNREFERENCED_PHYSICAL",
        }
    return expected, errors


def search_result_digest(round_record: dict[str, Any]) -> str:
    """Hash frozen queries and the ordered canonical result identity/context."""
    payload = {
        "epoch": round_record["epoch"],
        "kind": round_record["kind"],
        "owning_stage": round_record["owning_stage"],
        "queries": round_record["queries"],
        "results": [
            {
                "hit_id": hit["hit_id"],
                "query_id": hit["query_id"],
                "source_unit_id": hit["source_unit_id"],
                "context_sha256": hit["context_sha256"],
            }
            for hit in round_record["hits"]
        ],
    }
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def search_query_id_sequence_errors(rounds: object) -> list[str]:
    """Validate Q IDs in their global encounter order across all rounds."""
    if not isinstance(rounds, list):
        return []
    encountered: list[object] = []
    for round_record in rounds:
        if not isinstance(round_record, dict):
            continue
        queries = round_record.get("queries")
        if not isinstance(queries, list):
            continue
        for query in queries:
            if isinstance(query, dict) and set(query) == SEARCH_QUERY_FIELDS:
                encountered.append(query.get("query_id"))
    expected = [
        f"Q{index:04d}" for index in range(1, len(encountered) + 1)
    ]
    if encountered != expected:
        return ["search query IDs are not a complete append-only Q sequence"]
    return []


def execute_frozen_queries(
    queries: list[dict[str, Any]],
    units: list[dict[str, Any]],
    source_root: Path,
) -> tuple[list[tuple[str, str]], list[str]]:
    """Execute the frozen, tool-independent search language over source units."""
    errors: list[str] = []
    bytes_by_path: dict[str, bytes] = {}
    results: list[tuple[str, str]] = []
    for query in queries:
        if not isinstance(query, dict):
            continue
        query_id = query.get("query_id")
        pattern = query.get("pattern")
        mode = query.get("mode")
        case_sensitive = query.get("case_sensitive")
        whole_word = query.get("whole_word")
        scope_paths = query.get("scope_paths")
        if (
            not isinstance(query_id, str)
            or not isinstance(pattern, str)
            or not pattern
            or mode not in {"LITERAL", "REGEX"}
            or not isinstance(case_sensitive, bool)
            or not isinstance(whole_word, bool)
            or not isinstance(scope_paths, list)
        ):
            continue
        expression = re.escape(pattern) if mode == "LITERAL" else pattern
        if whole_word:
            expression = rf"(?<!\w)(?:{expression})(?!\w)"
        flags = re.MULTILINE
        if not case_sensitive:
            flags |= re.IGNORECASE
        try:
            compiled = re.compile(expression, flags)
        except re.error as exc:
            errors.append(f"search query {query_id} has invalid regex: {exc}")
            continue
        scope = set(scope_paths)
        for unit in units:
            if unit["path"] not in scope:
                continue
            if unit["path"] not in bytes_by_path:
                try:
                    bytes_by_path[unit["path"]] = (
                        source_root / unit["path"]
                    ).read_bytes()
                except OSError as exc:
                    errors.append(
                        f"cannot execute search in {unit['path']}: {exc}"
                    )
                    bytes_by_path[unit["path"]] = b""
            block = bytes_by_path[unit["path"]][
                unit["byte_start"] : unit["byte_end"]
            ]
            try:
                text = block.decode("utf-8")
            except UnicodeDecodeError as exc:
                errors.append(
                    f"cannot decode source unit {unit['id']} for search: {exc}"
                )
                continue
            if compiled.search(text):
                results.append((query_id, unit["id"]))
    return results, errors


def validate_candidate(
    row: dict[str, Any],
    candidate_ids: set[str],
    unit_ids: set[str],
    image_paths: set[str],
    route_ids: set[str],
    evidence_ids_global: set[str],
    errors: list[str],
) -> None:
    candidate_id = row.get("id", "<missing>")
    prefix = f"candidate {candidate_id}"
    if list(row) != CANDIDATE_FIELDS or set(row) != set(CANDIDATE_FIELDS):
        errors.append(f"{prefix} fields do not match blind allowlist/order")
        return
    leaks = forbidden_keys(row)
    if leaks:
        errors.append(f"{prefix} contains forbidden blind fields: {leaks}")
    if not B_ID.fullmatch(str(candidate_id)):
        errors.append(f"{prefix} has invalid B ID")
    if row["record_status"] not in {
        "ACTIVE",
        "MERGED_REDIRECT",
        "SPLIT_SUPERSEDED",
    }:
        errors.append(f"{prefix} has invalid record_status")
    if not isinstance(row["provisional_name"], str) or not row[
        "provisional_name"
    ].strip():
        errors.append(f"{prefix} lacks provisional_name")
    if not isinstance(row["discovery_stage"], int) or not (
        4 <= row["discovery_stage"] <= 18
    ):
        errors.append(f"{prefix} has invalid discovery_stage")
    anchor = row["discovery_anchor"]
    if (
        not isinstance(anchor, dict)
        or set(anchor) != {"epoch", "kind", "id", "ordinal"}
        or not isinstance(anchor.get("epoch"), int)
        or anchor["epoch"] < 1
        or anchor.get("kind") not in {"SOURCE_UNIT", "IMAGE", "SEARCH_HIT"}
        or not isinstance(anchor.get("id"), str)
        or not anchor["id"]
        or not isinstance(anchor.get("ordinal"), int)
        or anchor["ordinal"] < 1
    ):
        errors.append(f"{prefix} has invalid discovery_anchor")

    source_units = exact_string_list(
        row["source_unit_ids"],
        f"{prefix}.source_unit_ids",
        errors,
    )
    if any(unit not in unit_ids for unit in source_units):
        errors.append(f"{prefix} references unknown source unit")
    aliases = exact_string_list(row["aliases"], f"{prefix}.aliases", errors)
    source_statuses = exact_string_list(
        row["source_status"],
        f"{prefix}.source_status",
        errors,
        nonempty=True,
    )
    image_witnesses = exact_string_list(
        row["image_witnesses"], f"{prefix}.image_witnesses", errors
    )
    if not source_units and not image_witnesses:
        errors.append(f"{prefix} requires a source unit or image witness")
    aggregate_strengths = exact_string_list(
        row["evidence_strength"],
        f"{prefix}.evidence_strength",
        errors,
        nonempty=True,
    )
    missing_mechanics = exact_string_list(
        row["missing_mechanics"], f"{prefix}.missing_mechanics", errors
    )
    uncertainties = exact_string_list(
        row["uncertainties"], f"{prefix}.uncertainties", errors
    )
    cross_reference_ids = exact_string_list(
        row["cross_reference_ids"],
        f"{prefix}.cross_reference_ids",
        errors,
    )
    if any(value not in SOURCE_STATUSES for value in source_statuses):
        errors.append(f"{prefix} has invalid source_status")
    if any(value not in image_paths for value in image_witnesses):
        errors.append(f"{prefix} references unknown image")
    if any(value not in EVIDENCE_STRENGTHS for value in aggregate_strengths):
        errors.append(f"{prefix} has invalid evidence strength")
    if any(value not in route_ids for value in cross_reference_ids):
        errors.append(f"{prefix} references unknown route")
    if any(alias == row["provisional_name"] for alias in aliases):
        errors.append(f"{prefix} repeats provisional_name as an alias")

    evidence = row["source_evidence"]
    if not isinstance(evidence, list) or not evidence:
        errors.append(f"{prefix} requires source_evidence")
        evidence = []
    local_evidence_ids: set[str] = set()
    evidence_fields: dict[str, set[str]] = {}
    evidence_strength_by_id: dict[str, str] = {}
    evidence_strengths: set[str] = set()
    evidence_units: set[str] = set()
    evidence_images: set[str] = set()
    for item in evidence:
        if not isinstance(item, dict):
            errors.append(f"{prefix} evidence item must be object")
            continue
        expected = {
            "evidence_id",
            "evidence_group_id",
            "discovery_anchor",
            "source_unit_id",
            "image_path",
            "strength",
            "modality",
            "claim",
            "fingerprint_fields",
        }
        if set(item) != expected:
            errors.append(f"{prefix} evidence fields do not match allowlist")
            continue
        evidence_id = item["evidence_id"]
        if not isinstance(evidence_id, str) or not E_ID.fullmatch(evidence_id):
            errors.append(f"{prefix} evidence ID is invalid")
        elif evidence_id in local_evidence_ids or evidence_id in evidence_ids_global:
            errors.append(f"{prefix} evidence ID is not unique: {evidence_id}")
        else:
            local_evidence_ids.add(evidence_id)
            evidence_ids_global.add(evidence_id)
        if not isinstance(item["evidence_group_id"], str) or not G_ID.fullmatch(
            item["evidence_group_id"]
        ):
            errors.append(f"{prefix} evidence group ID is invalid")
        evidence_anchor = item["discovery_anchor"]
        if (
            not isinstance(evidence_anchor, dict)
            or set(evidence_anchor) != {"epoch", "kind", "id", "ordinal"}
            or not isinstance(evidence_anchor.get("epoch"), int)
            or evidence_anchor["epoch"] < 1
            or evidence_anchor.get("kind")
            not in {"SOURCE_UNIT", "IMAGE", "SEARCH_HIT"}
            or not isinstance(evidence_anchor.get("id"), str)
            or not evidence_anchor["id"]
            or not isinstance(evidence_anchor.get("ordinal"), int)
            or evidence_anchor["ordinal"] < 1
        ):
            errors.append(f"{prefix} evidence discovery anchor is invalid")
        source_unit_id = item["source_unit_id"]
        image_path = item["image_path"]
        if source_unit_id is not None and source_unit_id not in unit_ids:
            errors.append(f"{prefix} evidence references unknown unit")
        if source_unit_id is not None and source_unit_id not in source_units:
            errors.append(
                f"{prefix} evidence unit is absent from source_unit_ids"
            )
        if isinstance(source_unit_id, str):
            evidence_units.add(source_unit_id)
        if image_path is not None and image_path not in image_paths:
            errors.append(f"{prefix} evidence references unknown image")
        if image_path is not None and image_path not in image_witnesses:
            errors.append(
                f"{prefix} evidence image is absent from image_witnesses"
            )
        if isinstance(image_path, str):
            evidence_images.add(image_path)
        if isinstance(evidence_anchor, dict):
            if (
                evidence_anchor.get("kind") == "SOURCE_UNIT"
                and evidence_anchor.get("id") != source_unit_id
            ):
                errors.append(
                    f"{prefix} evidence source-unit anchor is inconsistent"
                )
            if (
                evidence_anchor.get("kind") == "IMAGE"
                and evidence_anchor.get("id") != image_path
            ):
                errors.append(f"{prefix} evidence image anchor is inconsistent")
        if item["source_unit_id"] is None and item["image_path"] is None:
            errors.append(f"{prefix} evidence has no canonical witness")
        if item["strength"] not in EVIDENCE_STRENGTHS:
            errors.append(f"{prefix} evidence strength is invalid")
        else:
            evidence_strengths.add(item["strength"])
            if isinstance(evidence_id, str):
                evidence_strength_by_id[evidence_id] = item["strength"]
        if item["modality"] not in EVIDENCE_MODALITIES:
            errors.append(f"{prefix} evidence modality is invalid")
        if item["modality"] == "IMAGE" and image_path is None:
            errors.append(f"{prefix} IMAGE evidence lacks image_path")
        if not isinstance(item["claim"], str) or not item["claim"].strip():
            errors.append(f"{prefix} evidence claim is empty")
        fields = exact_string_list(
            item["fingerprint_fields"],
            f"{prefix} evidence {evidence_id}.fingerprint_fields",
            errors,
        )
        if any(field not in FINGERPRINT_FIELDS for field in fields):
            errors.append(f"{prefix} evidence fingerprint fields are invalid")
        if isinstance(evidence_id, str):
            evidence_fields[evidence_id] = set(fields)

    if set(aggregate_strengths) != evidence_strengths:
        errors.append(
            f"{prefix} aggregate evidence_strength differs from source evidence"
        )
    if set(source_units) != evidence_units:
        errors.append(
            f"{prefix} source_unit_ids are not the exact evidence-unit join"
        )
    if set(image_witnesses) != evidence_images:
        errors.append(
            f"{prefix} image_witnesses are not the exact evidence-image join"
        )

    if not isinstance(row["field_support"], dict) or set(
        row["field_support"]
    ) != set(FINGERPRINT_FIELDS):
        errors.append(f"{prefix} field_support does not cover fingerprint")
    if not isinstance(row["fingerprint"], dict) or list(
        row["fingerprint"]
    ) != FINGERPRINT_FIELDS:
        errors.append(f"{prefix} fingerprint fields/order are invalid")
        return
    for field in FINGERPRINT_FIELDS:
        support = row["field_support"].get(field)
        value = row["fingerprint"].get(field)
        if support not in FIELD_SUPPORT_STATUSES:
            errors.append(f"{prefix}.{field} has invalid field support")
        if not isinstance(value, dict) or set(value) != {
            "status",
            "value",
            "evidence_ids",
            "reason",
        }:
            errors.append(f"{prefix}.{field} has invalid value object")
            continue
        if value["status"] != support:
            errors.append(f"{prefix}.{field} support/status disagree")
        field_evidence_ids = exact_string_list(
            value["evidence_ids"],
            f"{prefix}.{field}.evidence_ids",
            errors,
        )
        if any(
            evidence_id not in local_evidence_ids
            for evidence_id in field_evidence_ids
        ):
            errors.append(f"{prefix}.{field} has invalid evidence IDs")
        declared_ids = {
            evidence_id
            for evidence_id, declared_fields in evidence_fields.items()
            if field in declared_fields
        }
        if set(field_evidence_ids) != declared_ids:
            errors.append(
                f"{prefix}.{field} evidence IDs/declarations are not exact"
            )
        reason = value["reason"]
        if support == "SUPPORTED":
            if (
                not isinstance(value["value"], str)
                or not value["value"].strip()
                or not field_evidence_ids
            ):
                errors.append(f"{prefix}.{field} supported value lacks evidence")
            if reason not in ("", None):
                errors.append(f"{prefix}.{field} supported value has a reason")
        elif support == "NOT_APPLICABLE":
            if value["value"] is not None or not field_evidence_ids:
                errors.append(
                    f"{prefix}.{field} not-applicable value must be null and "
                    "evidence-justified"
                )
            if not isinstance(reason, str) or not reason.strip():
                errors.append(f"{prefix}.{field} not-applicable value lacks reason")
        elif support == "UNKNOWN_FROM_SOURCE":
            if value["value"] is not None:
                errors.append(f"{prefix}.{field} unknown value is not null")
            if not isinstance(reason, str) or not reason.strip():
                errors.append(f"{prefix}.{field} unknown value lacks reason")
            elif reason not in missing_mechanics:
                errors.append(
                    f"{prefix}.{field} unknown reason is absent from "
                    "missing_mechanics"
                )
        elif support == "CONFLICTING_SOURCE":
            if value["value"] is not None or len(field_evidence_ids) < 2:
                errors.append(
                    f"{prefix}.{field} conflict requires null value and "
                    "at least two evidence IDs"
                )
            if not isinstance(reason, str) or not reason.strip():
                errors.append(f"{prefix}.{field} conflict lacks reason")
            elif reason not in uncertainties:
                errors.append(
                    f"{prefix}.{field} conflict reason is absent from uncertainties"
                )

    for collection_name in ("parameters", "variants"):
        collection = row[collection_name]
        if not isinstance(collection, list):
            errors.append(f"{prefix}.{collection_name} must be an array")
            continue
        seen_names: set[str] = set()
        for item in collection:
            if not isinstance(item, dict) or set(item) != {
                "name",
                "source_description",
                "evidence_ids",
            }:
                errors.append(f"{prefix} has malformed {collection_name} item")
                continue
            if not isinstance(item["name"], str) or not item["name"].strip():
                errors.append(f"{prefix} has unnamed {collection_name} item")
            elif item["name"] in seen_names:
                errors.append(f"{prefix} repeats {collection_name} name")
            else:
                seen_names.add(item["name"])
            if (
                not isinstance(item["source_description"], str)
                or not item["source_description"].strip()
            ):
                errors.append(
                    f"{prefix} {collection_name} item lacks source description"
                )
            item_evidence = exact_string_list(
                item["evidence_ids"],
                f"{prefix}.{collection_name}.evidence_ids",
                errors,
                nonempty=True,
            )
            if any(value not in local_evidence_ids for value in item_evidence):
                errors.append(
                    f"{prefix} {collection_name} item has invalid evidence ID"
                )

    relations = row["related_candidate_ids"]
    if not isinstance(relations, list):
        errors.append(f"{prefix}.related_candidate_ids must be an array")
        relations = []
    definitive_relations: list[str] = []
    seen_relations: set[tuple[str, str]] = set()
    for relation in relations:
        if not isinstance(relation, dict) or set(relation) != {
            "candidate_id",
            "relation",
            "proof_kind",
            "evidence_ids",
            "before_rationale",
            "after_rationale",
            "uncertainty",
        }:
            errors.append(f"{prefix} has malformed related candidate")
            continue
        if relation["candidate_id"] not in candidate_ids:
            errors.append(f"{prefix} relates to unknown candidate")
        if relation["candidate_id"] == candidate_id:
            errors.append(f"{prefix} has a self relation")
        if relation["relation"] not in {
            "POSSIBLY_SAME_AS",
            "POSSIBLE_VARIANT_OF",
            "SOURCE_COMPARE",
            "MERGED_INTO",
            "SPLIT_INTO",
        }:
            errors.append(f"{prefix} has invalid blind candidate relation")
        proof_kind = relation["proof_kind"]
        if (
            not isinstance(proof_kind, str)
            or proof_kind not in LIFECYCLE_PROOF_KINDS
        ):
            errors.append(f"{prefix} has invalid lifecycle proof kind")
        relation_key = (relation["candidate_id"], relation["relation"])
        if relation_key in seen_relations:
            errors.append(f"{prefix} repeats a candidate relation")
        seen_relations.add(relation_key)
        relation_evidence = exact_string_list(
            relation["evidence_ids"],
            f"{prefix}.related_candidate_ids.evidence_ids",
            errors,
            nonempty=True,
        )
        if any(item not in local_evidence_ids for item in relation_evidence):
            errors.append(f"{prefix} relation has invalid evidence ID")
        if relation["relation"] in {"MERGED_INTO", "SPLIT_INTO"}:
            definitive_relations.append(relation["relation"])
            if relation["uncertainty"]:
                errors.append(
                    f"{prefix} definitive supersession relation is uncertain"
                )
            if relation["relation"] == "MERGED_INTO":
                if (
                    not isinstance(proof_kind, str)
                    or proof_kind not in MERGE_IDENTITY_PROOF_KINDS
                ):
                    errors.append(
                        f"{prefix} merge lacks a typed identity proof"
                    )
                if any(
                    evidence_strength_by_id.get(evidence_id)
                    != "DIRECT_IDENTITY"
                    for evidence_id in relation_evidence
                ):
                    errors.append(
                        f"{prefix} merge identity proof uses non-identity evidence"
                    )
                if relation["before_rationale"] or relation["after_rationale"]:
                    errors.append(
                        f"{prefix} merge relation carries split rationale fields"
                    )
            else:
                if proof_kind != "SPLIT_DISTINCTION":
                    errors.append(
                        f"{prefix} split lacks a typed distinction proof"
                    )
                if (
                    not isinstance(relation["before_rationale"], str)
                    or not relation["before_rationale"].strip()
                    or not isinstance(relation["after_rationale"], str)
                    or not relation["after_rationale"].strip()
                ):
                    errors.append(
                        f"{prefix} split lacks explicit before/after rationale"
                    )
        elif not isinstance(relation["uncertainty"], str) or not relation[
            "uncertainty"
        ].strip():
            errors.append(f"{prefix} provisional relation lacks uncertainty")
        else:
            if proof_kind != "PROVISIONAL_COMPARISON":
                errors.append(
                    f"{prefix} provisional relation has a definitive proof kind"
                )
            if relation["before_rationale"] or relation["after_rationale"]:
                errors.append(
                    f"{prefix} provisional relation carries split rationale fields"
                )

    if row["record_status"] == "ACTIVE" and definitive_relations:
        errors.append(f"{prefix} active record has supersession relation")
    if row["record_status"] == "MERGED_REDIRECT" and definitive_relations != [
        "MERGED_INTO"
    ]:
        errors.append(f"{prefix} merged redirect needs exactly one MERGED_INTO")
    if row["record_status"] == "SPLIT_SUPERSEDED" and (
        len(definitive_relations) < 2
        or set(definitive_relations) != {"SPLIT_INTO"}
    ):
        errors.append(f"{prefix} split tombstone needs at least two SPLIT_INTO")

    reassignments = row["evidence_reassignments"]
    if not isinstance(reassignments, list):
        errors.append(f"{prefix}.evidence_reassignments must be an array")
        reassignments = []
    reassigned_from: list[str] = []
    for reassignment in reassignments:
        if not isinstance(reassignment, dict) or set(reassignment) != {
            "from_evidence_id",
            "targets",
        }:
            errors.append(f"{prefix} has malformed evidence reassignment")
            continue
        from_evidence_id = reassignment["from_evidence_id"]
        if from_evidence_id not in local_evidence_ids:
            errors.append(f"{prefix} reassigns unknown local evidence")
        reassigned_from.append(from_evidence_id)
        targets = reassignment["targets"]
        if not isinstance(targets, list) or not targets:
            errors.append(f"{prefix} evidence reassignment has no targets")
            continue
        seen_targets: set[tuple[str, str]] = set()
        for target in targets:
            if not isinstance(target, dict) or set(target) != {
                "candidate_id",
                "evidence_id",
            }:
                errors.append(f"{prefix} has malformed reassignment target")
                continue
            target_key = (target["candidate_id"], target["evidence_id"])
            if target_key in seen_targets:
                errors.append(f"{prefix} repeats evidence reassignment target")
            seen_targets.add(target_key)
            if target["candidate_id"] not in candidate_ids:
                errors.append(f"{prefix} reassigns evidence to unknown candidate")
            if not isinstance(target["evidence_id"], str) or not E_ID.fullmatch(
                target["evidence_id"]
            ):
                errors.append(f"{prefix} has invalid target evidence ID")
    if len(reassigned_from) != len(set(reassigned_from)):
        errors.append(f"{prefix} reassigns one evidence item more than once")
    if row["record_status"] == "ACTIVE" and reassignments:
        errors.append(f"{prefix} active record has evidence reassignments")
    if row["record_status"] != "ACTIVE" and set(reassigned_from) != local_evidence_ids:
        errors.append(
            f"{prefix} tombstone does not reassign every evidence item"
        )

    if isinstance(row["field_support"], dict) and (
        "CONFLICTING_SOURCE" in row["field_support"].values()
    ) and (
        "CONFLICTING" not in source_statuses
    ):
        errors.append(f"{prefix} conflicting field lacks CONFLICTING source status")


READING_ENRICHMENT_SCALAR_FIELDS = {
    "review_disposition",
    "source_status",
    "uncertainty",
    "evidence_statement",
}
READING_ENRICHMENT_ADDITIVE_FIELDS = {
    "secondary_roles",
    "candidate_ids",
    "route_ids",
}
ASSET_ENRICHMENT_ADDITIVE_FIELDS = {"candidate_ids", "route_ids"}


def _validate_history_snapshot(
    event: dict[str, Any],
    source_unit_ids: list[str],
    asset_ids: list[str],
    errors: list[str],
    prefix: str,
) -> dict[str, Any] | None:
    snapshot = event.get("result_snapshot")
    if not isinstance(snapshot, dict) or set(snapshot) != {
        "schema_version",
        "source_path",
        "reading_results",
        "asset_results",
    }:
        errors.append(f"{prefix} has malformed full result snapshot")
        return None
    source_paths = event.get("source_paths")
    source_path = source_paths[0] if isinstance(source_paths, list) and len(source_paths) == 1 else None
    if snapshot.get("schema_version") != 1 or snapshot.get("source_path") != source_path:
        errors.append(f"{prefix} result snapshot identity is inconsistent")
    reading_results = snapshot.get("reading_results")
    asset_results = snapshot.get("asset_results")
    if not isinstance(reading_results, list):
        errors.append(f"{prefix} result snapshot reading_results is not an array")
        reading_results = []
    if not isinstance(asset_results, list):
        errors.append(f"{prefix} result snapshot asset_results is not an array")
        asset_results = []
    if [
        row.get("source_unit_id") if isinstance(row, dict) else None
        for row in reading_results
    ] != source_unit_ids:
        errors.append(f"{prefix} result snapshot source-unit order/scope differs")
    if [
        row.get("asset_id") if isinstance(row, dict) else None
        for row in asset_results
    ] != asset_ids:
        errors.append(f"{prefix} result snapshot asset order/scope differs")

    for row_index, row in enumerate(reading_results, start=1):
        row_prefix = f"{prefix} reading snapshot row {row_index}"
        if not isinstance(row, dict) or set(row) != set(
            READING_REVIEW_RESULT_FIELDS
        ):
            errors.append(f"{row_prefix} fields differ from full projection")
            continue
        if row.get("review_status") != "REVIEWED":
            errors.append(f"{row_prefix} is not REVIEWED")
        try:
            if int(row.get("review_epoch", "")) < 1:
                raise ValueError
            if not 4 <= int(row.get("review_stage", "")) <= 17:
                raise ValueError
        except (TypeError, ValueError):
            errors.append(f"{row_prefix} has invalid completion metadata")
        if not isinstance(row.get("reviewer"), str) or not row["reviewer"].strip():
            errors.append(f"{row_prefix} lacks reviewer")
        disposition = row.get("review_disposition")
        source_status = row.get("source_status")
        if disposition not in READING_DISPOSITIONS:
            errors.append(f"{row_prefix} has invalid disposition")
        if source_status not in SOURCE_STATUSES:
            errors.append(f"{row_prefix} has invalid source status")
        secondary = parsed_string_list(
            row.get("secondary_roles", ""),
            f"{row_prefix}.secondary_roles",
            errors,
        )
        candidates = parsed_string_list(
            row.get("candidate_ids", ""),
            f"{row_prefix}.candidate_ids",
            errors,
        )
        routes = parsed_string_list(
            row.get("route_ids", ""),
            f"{row_prefix}.route_ids",
            errors,
        )
        if any(value not in SECONDARY_ROLES for value in secondary):
            errors.append(f"{row_prefix} has invalid secondary role")
        uncertainty = row.get("uncertainty", "")
        if source_status == "CLEAR" and uncertainty:
            errors.append(f"{row_prefix} CLEAR source has uncertainty")
        if source_status in {"AMBIGUOUS", "DEFECTIVE", "CONFLICTING"} and not str(
            uncertainty
        ).strip():
            errors.append(f"{row_prefix} non-clear source lacks uncertainty")
        if not isinstance(row.get("evidence_statement"), str) or not row[
            "evidence_statement"
        ].strip():
            errors.append(f"{row_prefix} lacks evidence statement")
        if disposition in {"CANDIDATE", "SUPPORTS_CANDIDATE"} and not candidates:
            errors.append(f"{row_prefix} candidate disposition lacks B link")
        if disposition == "CROSS_REFERENCE" and not routes:
            errors.append(f"{row_prefix} cross-reference lacks route")
        if disposition == "NO_CONSTRUCTION" and (candidates or routes):
            errors.append(f"{row_prefix} NO_CONSTRUCTION carries links")
        if disposition == "SOURCE_DEFECT_OR_AMBIGUITY" and source_status == "CLEAR":
            errors.append(f"{row_prefix} source defect is CLEAR")

    for row_index, row in enumerate(asset_results, start=1):
        row_prefix = f"{prefix} asset snapshot row {row_index}"
        if not isinstance(row, dict) or set(row) != set(
            ASSET_REVIEW_RESULT_FIELDS
        ):
            errors.append(f"{row_prefix} fields differ from full projection")
            continue
        if row.get("inspection_status") != "SCREENED":
            errors.append(f"{row_prefix} is not SCREENED")
        try:
            if int(row.get("review_epoch", "")) < 1:
                raise ValueError
            if not 4 <= int(row.get("review_stage", "")) <= 17:
                raise ValueError
        except (TypeError, ValueError):
            errors.append(f"{row_prefix} has invalid completion metadata")
        if not isinstance(row.get("reviewer"), str) or not row["reviewer"].strip():
            errors.append(f"{row_prefix} lacks reviewer")
        if row.get("visual_role") not in VISUAL_ROLES:
            errors.append(f"{row_prefix} has invalid visual role")
        source_status = row.get("source_status")
        if source_status not in SOURCE_STATUSES:
            errors.append(f"{row_prefix} has invalid source status")
        risk_flags = parsed_string_list(
            row.get("risk_flags", ""),
            f"{row_prefix}.risk_flags",
            errors,
        )
        parsed_string_list(
            row.get("candidate_ids", ""),
            f"{row_prefix}.candidate_ids",
            errors,
        )
        parsed_string_list(
            row.get("route_ids", ""),
            f"{row_prefix}.route_ids",
            errors,
        )
        if any(value not in VISUAL_RISK_FLAGS for value in risk_flags):
            errors.append(f"{row_prefix} has invalid risk flag")
        if row.get("original_resolution_status") not in {
            "NOT_REQUIRED",
            "REVIEWED",
        }:
            errors.append(f"{row_prefix} has invalid resolution status")
        if row.get("transcription_status") not in {
            "NOT_APPLICABLE",
            "NOT_REQUIRED",
            "CHECKED",
        }:
            errors.append(f"{row_prefix} has invalid transcription status")
        uncertainty = row.get("uncertainty", "")
        if source_status == "CLEAR" and uncertainty:
            errors.append(f"{row_prefix} CLEAR source has uncertainty")
        if source_status in {"AMBIGUOUS", "DEFECTIVE", "CONFLICTING"} and not str(
            uncertainty
        ).strip():
            errors.append(f"{row_prefix} non-clear source lacks uncertainty")

    return snapshot


def _validate_search_enrichment_diff(
    previous_snapshot: dict[str, Any],
    snapshot: dict[str, Any],
    trigger_unit_ids: set[str],
    trigger_candidate_ids_by_unit: dict[str, set[str]],
    trigger_route_ids_by_unit: dict[str, set[str]],
    trigger_candidate_ids: set[str],
    trigger_route_ids: set[str],
    errors: list[str],
    prefix: str,
) -> None:
    previous_reading = {
        row["source_unit_id"]: row
        for row in previous_snapshot["reading_results"]
        if isinstance(row, dict) and "source_unit_id" in row
    }
    previous_assets = {
        row["asset_id"]: row
        for row in previous_snapshot["asset_results"]
        if isinstance(row, dict) and "asset_id" in row
    }
    changed = False
    allowed_reading = (
        READING_ENRICHMENT_SCALAR_FIELDS
        | READING_ENRICHMENT_ADDITIVE_FIELDS
    )
    for row in snapshot["reading_results"]:
        if not isinstance(row, dict) or "source_unit_id" not in row:
            continue
        unit_id = row["source_unit_id"]
        before = previous_reading.get(unit_id)
        if before is None:
            errors.append(f"{prefix} enrichment adds an unknown reading row")
            continue
        changed_fields = {
            field for field in READING_REVIEW_RESULT_FIELDS if row.get(field) != before.get(field)
        }
        if not changed_fields:
            continue
        changed = True
        if unit_id not in trigger_unit_ids:
            errors.append(
                f"{prefix} changes reading {unit_id} without an exact trigger hit"
            )
        illegal = changed_fields - allowed_reading
        if illegal:
            errors.append(
                f"{prefix} changes immutable reading fields: {sorted(illegal)}"
            )
        for field in changed_fields & READING_ENRICHMENT_ADDITIVE_FIELDS:
            old_values = set(
                parsed_string_list(
                    before[field], f"{prefix}.previous.{unit_id}.{field}", errors
                )
            )
            new_values = set(
                parsed_string_list(
                    row[field], f"{prefix}.current.{unit_id}.{field}", errors
                )
            )
            if not old_values.issubset(new_values):
                errors.append(
                    f"{prefix} removes prior reading enrichment from "
                    f"{unit_id}.{field}"
                )
            added = new_values - old_values
            if field == "candidate_ids" and not added.issubset(
                trigger_candidate_ids_by_unit.get(unit_id, set())
            ):
                errors.append(
                    f"{prefix} adds unrelated candidate links to {unit_id}"
                )
            if field == "route_ids" and not added.issubset(
                trigger_route_ids_by_unit.get(unit_id, set())
            ):
                errors.append(f"{prefix} adds unrelated route links to {unit_id}")
        current_candidate_ids = set(
            parsed_string_list(
                row["candidate_ids"],
                f"{prefix}.current.{unit_id}.candidate_ids",
                errors,
            )
        )
        current_route_ids = set(
            parsed_string_list(
                row["route_ids"],
                f"{prefix}.current.{unit_id}.route_ids",
                errors,
            )
        )
        if row.get("review_disposition") in {
            "CANDIDATE",
            "SUPPORTS_CANDIDATE",
        } and not (
            current_candidate_ids
            & trigger_candidate_ids_by_unit.get(unit_id, set())
        ):
            errors.append(
                f"{prefix} candidate disposition lacks a triggered candidate link"
            )
        if row.get("review_disposition") == "CROSS_REFERENCE" and not (
            current_route_ids & trigger_route_ids_by_unit.get(unit_id, set())
        ):
            errors.append(
                f"{prefix} cross-reference disposition lacks a triggered route link"
            )

    for row in snapshot["asset_results"]:
        if not isinstance(row, dict) or "asset_id" not in row:
            continue
        asset_id = row["asset_id"]
        before = previous_assets.get(asset_id)
        if before is None:
            errors.append(f"{prefix} enrichment adds an unknown asset row")
            continue
        changed_fields = {
            field for field in ASSET_REVIEW_RESULT_FIELDS if row.get(field) != before.get(field)
        }
        if not changed_fields:
            continue
        changed = True
        illegal = changed_fields - ASSET_ENRICHMENT_ADDITIVE_FIELDS
        if illegal:
            errors.append(
                f"{prefix} changes immutable asset fields: {sorted(illegal)}"
            )
        for field in changed_fields & ASSET_ENRICHMENT_ADDITIVE_FIELDS:
            old_values = set(
                parsed_string_list(
                    before[field], f"{prefix}.previous.{asset_id}.{field}", errors
                )
            )
            new_values = set(
                parsed_string_list(
                    row[field], f"{prefix}.current.{asset_id}.{field}", errors
                )
            )
            if not old_values.issubset(new_values):
                errors.append(
                    f"{prefix} removes prior asset enrichment from "
                    f"{asset_id}.{field}"
                )
            added = new_values - old_values
            if field == "candidate_ids" and not added.issubset(
                trigger_candidate_ids
            ):
                errors.append(
                    f"{prefix} adds unrelated candidate links to asset {asset_id}"
                )
            if field == "route_ids" and not added.issubset(trigger_route_ids):
                errors.append(
                    f"{prefix} adds unrelated route links to asset {asset_id}"
                )
    if not changed:
        errors.append(f"{prefix} SEARCH_ENRICHMENT has no semantic delta")


def validate_review_history(
    manifest: dict[str, Any],
    units: list[dict[str, Any]],
    reading: list[dict[str, str]],
    assets: list[dict[str, str]],
    candidates: list[dict[str, Any]],
    review_history: list[dict[str, Any]],
    search: dict[str, Any],
    stage_by_path: dict[str, int],
) -> tuple[
    list[str],
    set[int],
    dict[str, set[int]],
    dict[str, set[int]],
    dict[tuple[int, int], set[str]],
]:
    """Validate immutable review snapshots and typed search enrichments."""
    errors: list[str] = []
    unit_by_id = {unit["id"]: unit for unit in units}
    reading_by_id = {row.get("source_unit_id", ""): row for row in reading}
    asset_by_id = {row.get("asset_id", ""): row for row in assets}
    audit_paths = [
        document["path"]
        for document in sorted(
            manifest["documents"],
            key=lambda document: (
                stage_by_path[document["path"]],
                int(document["order"]),
            ),
        )
    ]
    document_position = {
        path: index for index, path in enumerate(audit_paths, start=1)
    }
    unit_position = {
        unit["id"]: index for index, unit in enumerate(units, start=1)
    }
    asset_position = {
        row.get("asset_id", ""): index
        for index, row in enumerate(assets, start=1)
    }
    search_rounds = search.get("rounds", []) if isinstance(search, dict) else []
    if not isinstance(search_rounds, list):
        search_rounds = []
    hit_meta: dict[
        str,
        tuple[int, int, str, str, str, set[str], set[str]],
    ] = {}
    for round_position, round_record in enumerate(search_rounds, start=1):
        if not isinstance(round_record, dict):
            continue
        epoch = round_record.get("epoch")
        kind = round_record.get("kind")
        for hit in round_record.get("hits", []):
            if (
                isinstance(hit, dict)
                and isinstance(hit.get("hit_id"), str)
                and isinstance(epoch, int)
                and kind in {"LOCAL", "SATURATION"}
                and isinstance(hit.get("source_unit_id"), str)
            ):
                hit_meta[hit["hit_id"]] = (
                    round_position,
                    epoch,
                    kind,
                    hit["source_unit_id"],
                    str(hit.get("disposition", "")),
                    {
                        value
                        for value in hit.get("candidate_ids", [])
                        if isinstance(value, str)
                    },
                    {
                        value
                        for value in hit.get("route_ids", [])
                        if isinstance(value, str)
                    },
                )

    history_epochs: set[int] = set()
    unit_history_epochs: dict[str, set[int]] = {}
    asset_path_history_epochs: dict[str, set[int]] = {}
    expected_local_scopes: dict[tuple[int, int], set[str]] = {}
    latest_review_unit_event: dict[str, dict[str, Any]] = {}
    latest_review_asset_event: dict[str, dict[str, Any]] = {}
    latest_path_event: dict[str, dict[str, Any]] = {}
    seen_paths: set[str] = set()
    seen_review_path_epochs: set[tuple[int, str]] = set()
    next_initial_path_index = 0
    prior_event_hash: str | None = None
    prior_event_epoch: int | None = None
    prior_search_round_count = 0
    last_review_position_by_epoch: dict[int, int] = {}

    if not isinstance(review_history, list):
        return (
            ["review-history root must be an ordered JSONL record list"],
            set(),
            {},
            {},
            {},
        )

    for index, event in enumerate(review_history, start=1):
        prefix = f"review-history event {index}"
        if not isinstance(event, dict):
            errors.append(f"{prefix} is not an object")
            continue
        if set(event) != set(REVIEW_HISTORY_FIELDS):
            errors.append(f"{prefix} fields differ from the closed contract")
            continue
        if event.get("review_id") != f"V{index:06d}":
            errors.append(f"{prefix} violates the append-only V sequence")
        epoch = event.get("epoch")
        stage = event.get("stage")
        mode = event.get("mode")
        reviewer = event.get("reviewer")
        if not isinstance(epoch, int) or epoch < 1:
            errors.append(f"{prefix} has invalid epoch")
            continue
        history_epochs.add(epoch)
        if not isinstance(stage, int) or not 4 <= stage <= 17:
            errors.append(f"{prefix} has invalid stage")
            continue
        if mode not in REVIEW_MODES:
            errors.append(f"{prefix} has invalid mode")
        if not isinstance(reviewer, str) or not reviewer.strip():
            errors.append(f"{prefix} lacks reviewer")
        is_review_event = mode in {"INITIAL", "REOPEN"}
        is_enrichment = mode == "SEARCH_ENRICHMENT"

        source_paths = exact_string_list(
            event.get("source_paths"),
            f"{prefix}.source_paths",
            errors,
            nonempty=True,
        )
        if len(source_paths) != 1:
            errors.append(f"{prefix} must cover exactly one canonical source path")
        event_path = source_paths[0] if len(source_paths) == 1 else None
        source_unit_ids = exact_string_list(
            event.get("source_unit_ids"),
            f"{prefix}.source_unit_ids",
            errors,
            nonempty=True,
        )
        asset_ids = exact_string_list(
            event.get("asset_ids"),
            f"{prefix}.asset_ids",
            errors,
        )
        if event_path not in stage_by_path:
            errors.append(f"{prefix} contains an unknown source path")
        elif stage_by_path[event_path] != stage:
            errors.append(f"{prefix} source path lies outside its stage")
        expected_units = [
            unit["id"] for unit in units if unit["path"] == event_path
        ]
        expected_assets = [
            row.get("asset_id", "")
            for row in assets
            if row.get("assignment_path") == event_path
        ]
        if source_unit_ids != expected_units:
            errors.append(
                f"{prefix} source-unit scope is not the exact ordered path scope"
            )
        if asset_ids != expected_assets:
            errors.append(
                f"{prefix} asset scope is not the exact ordered path scope"
            )
        if source_unit_ids != sorted(
            source_unit_ids, key=lambda value: unit_position.get(value, 10**9)
        ):
            errors.append(f"{prefix} source units are not in canonical order")
        if asset_ids != sorted(
            asset_ids, key=lambda value: asset_position.get(value, 10**9)
        ):
            errors.append(f"{prefix} assets are not in canonical order")

        opens_epoch = prior_event_epoch is None or epoch > prior_event_epoch
        if prior_event_epoch is None:
            if epoch != 1 or mode != "INITIAL":
                errors.append(f"{prefix} must begin history with INITIAL epoch 1")
        else:
            if epoch < prior_event_epoch:
                errors.append(f"{prefix} moves backward to an earlier epoch")
            elif epoch > prior_event_epoch + 1:
                errors.append(f"{prefix} skips a global review epoch")
            if epoch > prior_event_epoch and mode != "REOPEN":
                errors.append(f"{prefix} opens a new epoch without REOPEN")
        if is_enrichment and prior_event_epoch != epoch:
            errors.append(
                f"{prefix} SEARCH_ENRICHMENT is not in the active epoch"
            )

        prefix_count = event.get("prior_search_round_count")
        prefix_digest = event.get("prior_search_rounds_sha256")
        if not isinstance(prefix_count, int) or prefix_count < 0:
            errors.append(f"{prefix} has invalid prior search round count")
            prefix_count = 0
        if prefix_count < prior_search_round_count:
            errors.append(f"{prefix} moves backward to an earlier search prefix")
        if prefix_count > len(search_rounds):
            errors.append(f"{prefix} search prefix exceeds recorded rounds")
            search_prefix = search_rounds
        else:
            search_prefix = search_rounds[:prefix_count]
        if prefix_digest != canonical_sha256(search_prefix):
            errors.append(f"{prefix} prior search-round prefix hash is stale")
        if any(
            isinstance(round_record, dict)
            and isinstance(round_record.get("epoch"), int)
            and round_record["epoch"] > epoch
            for round_record in search_prefix
        ):
            errors.append(f"{prefix} search prefix contains a future epoch")
        if opens_epoch and epoch > 1:
            for (prior_stage, prior_epoch), prior_paths in (
                expected_local_scopes.items()
            ):
                if prior_epoch >= epoch:
                    continue
                local_rounds = [
                    round_record
                    for round_record in search_prefix
                    if isinstance(round_record, dict)
                    and round_record.get("kind") == "LOCAL"
                    and round_record.get("owning_stage") == prior_stage
                    and round_record.get("epoch") == prior_epoch
                ]
                local_scope = {
                    path
                    for round_record in local_rounds
                    for query in round_record.get("queries", [])
                    if isinstance(query, dict)
                    for path in query.get("scope_paths", [])
                }
                if not local_rounds or local_scope != prior_paths:
                    errors.append(
                        f"{prefix} advances epoch before Stage {prior_stage} "
                        f"epoch {prior_epoch} LOCAL closure"
                    )
        prior_search_round_count = prefix_count

        prior_path_event = latest_path_event.get(event_path or "")
        expected_previous_path_digest = (
            prior_path_event.get("result_projection_sha256")
            if prior_path_event is not None
            else None
        )
        if event.get("previous_path_result_sha256") != expected_previous_path_digest:
            errors.append(f"{prefix} breaks its per-path result chain")
        if mode == "INITIAL" and prior_path_event is not None:
            errors.append(f"{prefix} INITIAL path was already reviewed")
        if mode in {"REOPEN", "SEARCH_ENRICHMENT"} and prior_path_event is None:
            errors.append(f"{prefix} {mode} path has no prior snapshot")

        trigger_kind = event.get("trigger_search_kind")
        trigger_hit_ids = exact_string_list(
            event.get("trigger_hit_ids"),
            f"{prefix}.trigger_hit_ids",
            errors,
        )
        trigger_unit_ids: set[str] = set()
        trigger_candidate_ids_by_unit: dict[str, set[str]] = {}
        trigger_route_ids_by_unit: dict[str, set[str]] = {}
        trigger_candidate_ids: set[str] = set()
        trigger_route_ids: set[str] = set()
        if is_review_event:
            if trigger_kind is not None or trigger_hit_ids:
                errors.append(f"{prefix} review event carries search triggers")
        elif is_enrichment:
            if trigger_kind not in SEARCH_ENRICHMENT_TRIGGER_KINDS:
                errors.append(f"{prefix} has invalid enrichment trigger kind")
            if not trigger_hit_ids:
                errors.append(f"{prefix} enrichment lacks trigger hit IDs")
            prior_path_prefix_count = (
                prior_path_event.get("prior_search_round_count", 0)
                if prior_path_event is not None
                else 0
            )
            if prefix_count <= prior_path_prefix_count:
                errors.append(
                    f"{prefix} enrichment does not advance its path search prefix"
                )
            for hit_id in trigger_hit_ids:
                meta = hit_meta.get(hit_id)
                if meta is None:
                    errors.append(f"{prefix} trigger hit {hit_id} is unknown")
                    continue
                (
                    round_position,
                    hit_epoch,
                    hit_kind,
                    unit_id,
                    disposition,
                    hit_candidate_ids,
                    hit_route_ids,
                ) = meta
                if not prior_path_prefix_count < round_position <= prefix_count:
                    errors.append(
                        f"{prefix} trigger hit {hit_id} is not newly visible"
                    )
                if hit_epoch != epoch or hit_kind != trigger_kind:
                    errors.append(
                        f"{prefix} trigger hit {hit_id} has wrong epoch/kind"
                    )
                if disposition == "EXCLUSION":
                    errors.append(
                        f"{prefix} EXCLUSION hit {hit_id} cannot authorize enrichment"
                    )
                source_unit = unit_by_id.get(unit_id)
                if source_unit is None or source_unit["path"] != event_path:
                    errors.append(
                        f"{prefix} trigger hit {hit_id} lies outside its path"
                    )
                else:
                    trigger_unit_ids.add(unit_id)
                    trigger_candidate_ids_by_unit.setdefault(
                        unit_id, set()
                    ).update(hit_candidate_ids)
                    trigger_route_ids_by_unit.setdefault(
                        unit_id, set()
                    ).update(hit_route_ids)
                    trigger_candidate_ids.update(hit_candidate_ids)
                    trigger_route_ids.update(hit_route_ids)

        snapshot = _validate_history_snapshot(
            event,
            source_unit_ids,
            asset_ids,
            errors,
            prefix,
        )
        if isinstance(snapshot, dict):
            if event.get("result_projection_sha256") != canonical_sha256(snapshot):
                errors.append(f"{prefix} full result snapshot hash is stale")
            if is_review_event:
                for row in snapshot["reading_results"]:
                    if isinstance(row, dict) and (
                        row.get("review_epoch") != str(epoch)
                        or row.get("review_stage") != str(stage)
                        or row.get("reviewer") != reviewer
                    ):
                        errors.append(
                            f"{prefix} reading snapshot completion metadata "
                            "differs from review event"
                        )
                for row in snapshot["asset_results"]:
                    if isinstance(row, dict) and (
                        row.get("review_epoch") != str(epoch)
                        or row.get("review_stage") != str(stage)
                        or row.get("reviewer") != reviewer
                    ):
                        errors.append(
                            f"{prefix} asset snapshot completion metadata "
                            "differs from review event"
                        )
            elif is_enrichment and prior_path_event is not None:
                previous_snapshot = prior_path_event.get("result_snapshot")
                if isinstance(previous_snapshot, dict):
                    _validate_search_enrichment_diff(
                        previous_snapshot,
                        snapshot,
                        trigger_unit_ids,
                        trigger_candidate_ids_by_unit,
                        trigger_route_ids_by_unit,
                        trigger_candidate_ids,
                        trigger_route_ids,
                        errors,
                        prefix,
                    )

        if is_review_event and event_path is not None:
            event_position = document_position.get(event_path, 10**9)
            prior_position = last_review_position_by_epoch.get(epoch)
            if prior_position is not None and event_position <= prior_position:
                errors.append(
                    f"{prefix} violates strict frozen document traversal "
                    "within its epoch"
                )
            last_review_position_by_epoch[epoch] = event_position
            if (epoch, event_path) in seen_review_path_epochs:
                errors.append(f"{prefix} repeats a reviewed path in one epoch")
            seen_review_path_epochs.add((epoch, event_path))
            if mode == "INITIAL":
                expected_initial_path = (
                    audit_paths[next_initial_path_index]
                    if next_initial_path_index < len(audit_paths)
                    else None
                )
                if event_path != expected_initial_path:
                    errors.append(
                        f"{prefix} INITIAL path is not the first unread audit path"
                    )
                else:
                    next_initial_path_index += 1
            elif mode == "REOPEN" and event_path not in seen_paths:
                errors.append(f"{prefix} REOPEN path was not previously reviewed")
            seen_paths.add(event_path)
            expected_local_scopes.setdefault((stage, epoch), set()).add(event_path)
            for unit_id in source_unit_ids:
                latest_review_unit_event[unit_id] = event
                unit_history_epochs.setdefault(unit_id, set()).add(epoch)
            for asset_id in asset_ids:
                latest_review_asset_event[asset_id] = event
                physical_path = asset_by_id.get(asset_id, {}).get("physical_path")
                if physical_path:
                    asset_path_history_epochs.setdefault(
                        physical_path, set()
                    ).add(epoch)
        elif is_enrichment and event_path not in seen_paths:
            errors.append(f"{prefix} enrichment path was never reviewed")

        previous_hash = event.get("previous_event_sha256")
        if previous_hash != prior_event_hash:
            errors.append(f"{prefix} previous-event hash breaks append chain")
        for field in (
            "input_projection_sha256",
            "result_projection_sha256",
            "event_sha256",
        ):
            if not isinstance(event.get(field), str) or not HEX64.fullmatch(
                event[field]
            ):
                errors.append(f"{prefix} has invalid {field}")
        try:
            expected_input_digest = canonical_sha256(
                review_input_projection(event, unit_by_id, asset_by_id)
            )
        except (KeyError, TypeError):
            expected_input_digest = None
        if (
            expected_input_digest is not None
            and event.get("input_projection_sha256") != expected_input_digest
        ):
            errors.append(f"{prefix} immutable input projection hash is stale")
        try:
            expected_event_digest = review_event_sha256(event)
        except (KeyError, TypeError):
            expected_event_digest = None
        if (
            expected_event_digest is not None
            and event.get("event_sha256") != expected_event_digest
        ):
            errors.append(f"{prefix} closed event hash is stale")
        prior_event_hash = event.get("event_sha256")
        prior_event_epoch = epoch
        if event_path is not None:
            latest_path_event[event_path] = event

    for row in reading:
        unit_id = row.get("source_unit_id", "")
        event = latest_review_unit_event.get(unit_id)
        if row.get("review_status") == "PENDING":
            if event is not None:
                errors.append(f"reading {unit_id} is pending but has review history")
            continue
        if row.get("review_status") != "REVIEWED":
            continue
        if event is None:
            errors.append(f"reading {unit_id} is reviewed without review history")
            continue
        if row.get("review_epoch") != str(event["epoch"]):
            errors.append(
                f"reading {unit_id} review epoch is not its latest review event"
            )
        if row.get("review_stage") != str(event["stage"]):
            errors.append(
                f"reading {unit_id} review stage differs from latest review event"
            )
        if row.get("reviewer") != event["reviewer"]:
            errors.append(
                f"reading {unit_id} reviewer differs from latest review event"
            )
    for row in assets:
        asset_id = row.get("asset_id", "")
        event = latest_review_asset_event.get(asset_id)
        if row.get("inspection_status") == "PENDING":
            if event is not None:
                errors.append(f"asset {asset_id} is pending but has review history")
            continue
        if row.get("inspection_status") != "SCREENED":
            continue
        if event is None:
            errors.append(f"asset {asset_id} is screened without review history")
            continue
        if row.get("review_epoch") != str(event["epoch"]):
            errors.append(
                f"asset {asset_id} review epoch is not its latest review event"
            )
        if row.get("review_stage") != str(event["stage"]):
            errors.append(
                f"asset {asset_id} review stage differs from latest review event"
            )
        if row.get("reviewer") != event["reviewer"]:
            errors.append(
                f"asset {asset_id} reviewer differs from latest review event"
            )

    for path, event in latest_path_event.items():
        try:
            current_snapshot = review_result_projection(
                event, reading_by_id, asset_by_id
            )
        except (KeyError, TypeError, IndexError):
            continue
        if event.get("result_snapshot") != current_snapshot:
            errors.append(
                f"review-history latest snapshot for {path} differs from "
                "current full row projection"
            )

    return (
        errors,
        history_epochs,
        unit_history_epochs,
        asset_path_history_epochs,
        expected_local_scopes,
    )


def validate_objects(
    manifest: dict[str, Any],
    units: list[dict[str, Any]],
    reading: list[dict[str, str]],
    candidates: list[dict[str, Any]],
    routes: list[dict[str, str]],
    assets: list[dict[str, str]],
    search: dict[str, Any],
    review_history: list[dict[str, Any]],
    require_stages: set[int] | None = None,
    require_all_reviewed: bool = False,
    repo_root: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    require_stages = require_stages or set()
    source_root = (repo_root or REPO_ROOT) / "ref" / "A-New-Kind-of-Science"
    unit_by_id = {unit["id"]: unit for unit in units}
    unit_ids = set(unit_by_id)
    document_by_path = {doc["path"]: doc for doc in manifest["documents"]}
    image_by_path = {image["path"]: image for image in manifest["images"]}
    image_paths = set(image_by_path)
    unit_position = {
        unit["id"]: position for position, unit in enumerate(units, start=1)
    }
    image_position = {
        image["path"]: position
        for position, image in enumerate(manifest["images"], start=1)
    }
    stage_by_path = {
        path: stage_for_document(document)
        for path, document in document_by_path.items()
    }
    expected_assets, assignment_errors = expected_asset_assignments(manifest)
    errors.extend(assignment_errors)
    asset_record_by_id = {row.get("asset_id", ""): row for row in assets}
    asset_ids = set(asset_record_by_id)
    discovery_epochs: set[int] = set()
    non_review_epochs: set[int] = set()
    (
        history_errors,
        history_epochs,
        unit_history_epochs,
        asset_path_history_epochs,
        history_local_scopes,
    ) = validate_review_history(
        manifest,
        units,
        reading,
        assets,
        candidates,
        review_history,
        search,
        stage_by_path,
    )
    errors.extend(history_errors)
    discovery_epochs.update(history_epochs)

    route_by_id = {row.get("route_id", ""): row for row in routes}
    route_ids = set(route_by_id)
    candidate_ids = {str(row.get("id", "")) for row in candidates}

    if len(reading) != len(units):
        errors.append("reading ledger row count differs from source units")
    if [row.get("source_unit_id") for row in reading] != [
        unit["id"] for unit in units
    ]:
        errors.append("reading ledger unit order/set differs from source units")

    reading_candidate_links: dict[str, set[str]] = {}
    reading_route_links: dict[str, set[str]] = {}
    reading_review_epochs: dict[str, int] = {}
    reviewed_count = 0
    for row in reading:
        unit_id = row.get("source_unit_id", "")
        unit = unit_by_id.get(unit_id)
        if unit is None:
            continue
        prefix = f"reading {unit_id}"
        static_fields = {
            "document_order": str(unit["document_order"]),
            "path": unit["path"],
            "block_kind": unit["block_kind"],
            "byte_start": str(unit["byte_start"]),
            "byte_end": str(unit["byte_end"]),
            "line_start": str(unit["line_start"]),
            "line_end": str(unit["line_end"]),
            "global_line_start": str(unit["global_line_start"]),
            "global_line_end": str(unit["global_line_end"]),
            "unit_sha256": unit["sha256"],
        }
        for key, expected in static_fields.items():
            if row.get(key) != expected:
                errors.append(f"{prefix} static field mismatch: {key}")
        secondary = parsed_string_list(
            row.get("secondary_roles", ""),
            f"{prefix}.secondary_roles",
            errors,
        )
        linked_candidates = parsed_string_list(
            row.get("candidate_ids", ""),
            f"{prefix}.candidate_ids",
            errors,
        )
        linked_routes = parsed_string_list(
            row.get("route_ids", ""),
            f"{prefix}.route_ids",
            errors,
        )
        reading_candidate_links[unit_id] = set(linked_candidates)
        reading_route_links[unit_id] = set(linked_routes)
        if any(value not in SECONDARY_ROLES for value in secondary):
            errors.append(f"{prefix} has invalid secondary role")
        if any(value not in candidate_ids for value in linked_candidates):
            errors.append(f"{prefix} links unknown candidate")
        if any(value not in route_ids for value in linked_routes):
            errors.append(f"{prefix} links unknown route")

        status = row.get("review_status")
        if status == "PENDING":
            if any(
                row.get(key)
                for key in (
                    "review_epoch",
                    "review_disposition",
                    "source_status",
                    "uncertainty",
                    "evidence_statement",
                    "review_stage",
                    "reviewer",
                )
            ) or secondary or linked_candidates or linked_routes:
                errors.append(f"{prefix} pending row contains review result")
        elif status == "REVIEWED":
            reviewed_count += 1
            try:
                review_epoch = int(row.get("review_epoch", ""))
            except ValueError:
                review_epoch = -1
            if review_epoch < 1:
                errors.append(f"{prefix} has invalid review epoch")
            else:
                reading_review_epochs[unit_id] = review_epoch
                discovery_epochs.add(review_epoch)
            if row.get("review_disposition") not in READING_DISPOSITIONS:
                errors.append(f"{prefix} has invalid review disposition")
            if row.get("source_status") not in SOURCE_STATUSES:
                errors.append(f"{prefix} has invalid source status")
            uncertainty = row.get("uncertainty", "").strip()
            if row.get("source_status") == "CLEAR" and uncertainty:
                errors.append(f"{prefix} CLEAR source has an uncertainty boundary")
            if (
                row.get("source_status") in {
                    "AMBIGUOUS",
                    "DEFECTIVE",
                    "CONFLICTING",
                }
                and not uncertainty
            ):
                errors.append(f"{prefix} non-clear source lacks uncertainty boundary")
            if (
                "SOURCE_DEFECT" in secondary
                and row.get("source_status") == "CLEAR"
            ):
                errors.append(f"{prefix} source-defect role has CLEAR source status")
            if not row.get("evidence_statement", "").strip():
                errors.append(f"{prefix} lacks evidence statement")
            if not row.get("reviewer", "").strip():
                errors.append(f"{prefix} lacks reviewer")
            try:
                stage = int(row.get("review_stage", ""))
            except ValueError:
                stage = -1
            expected_stage = stage_by_path[unit["path"]]
            if stage != expected_stage:
                errors.append(
                    f"{prefix} review stage {stage} differs from assigned "
                    f"stage {expected_stage}"
                )
            if (
                row.get("review_disposition")
                in {"CANDIDATE", "SUPPORTS_CANDIDATE"}
                and not linked_candidates
            ):
                errors.append(
                    f"{prefix} candidate/support disposition has no B link"
                )
            if (
                row.get("review_disposition") == "CROSS_REFERENCE"
                and not linked_routes
            ):
                errors.append(f"{prefix} cross-reference disposition has no route")
            if row.get("review_disposition") == "NO_CONSTRUCTION" and (
                linked_candidates or linked_routes
            ):
                errors.append(
                    f"{prefix} NO_CONSTRUCTION row carries candidate/route links"
                )
            if (
                row.get("review_disposition") == "SOURCE_DEFECT_OR_AMBIGUITY"
                and row.get("source_status") == "CLEAR"
            ):
                errors.append(
                    f"{prefix} source-defect disposition has CLEAR source status"
                )
        else:
            errors.append(f"{prefix} has invalid review_status")

    reading_by_unit = {row["source_unit_id"]: row for row in reading}

    if require_all_reviewed and reviewed_count != len(units):
        errors.append("not every source unit is reviewed")

    if [row.get("route_id") for row in routes] != [
        f"R{index:06d}" for index in range(1, len(routes) + 1)
    ]:
        errors.append("route IDs are not a total canonical sequence")
    for row in routes:
        route_id = row["route_id"]
        prefix = f"route {route_id}"
        source_unit = unit_by_id.get(row["source_unit_id"])
        source_asset = asset_record_by_id.get(row["source_asset_id"])
        if row["route_kind"] not in ROUTE_KINDS:
            errors.append(f"{prefix} has invalid kind")
        try:
            discovery_epoch = int(row["discovery_epoch"])
        except ValueError:
            discovery_epoch = -1
        if discovery_epoch < 1:
            errors.append(f"{prefix} has invalid discovery epoch")
        else:
            discovery_epochs.add(discovery_epoch)
            non_review_epochs.add(discovery_epoch)
        try:
            discovery_ordinal = int(row["discovery_ordinal"])
        except ValueError:
            discovery_ordinal = -1
        if discovery_ordinal < 1:
            errors.append(f"{prefix} has invalid discovery ordinal")
        if row["discovery_kind"] not in {
            "SOURCE_UNIT",
            "IMAGE",
            "SEARCH_HIT",
        }:
            errors.append(f"{prefix} has invalid discovery kind")
        if row["discovery_kind"] == "SOURCE_UNIT":
            if (
                source_unit is None
                or row["source_asset_id"]
                or row["discovery_id"] != row["source_unit_id"]
            ):
                errors.append(f"{prefix} source discovery anchor is inconsistent")
        if row["discovery_kind"] == "IMAGE":
            if (
                source_asset is None
                or row["source_unit_id"]
                or row["discovery_id"] != row["source_asset_id"]
            ):
                errors.append(f"{prefix} image discovery anchor is inconsistent")
        if row["discovery_kind"] == "SEARCH_HIT" and not H_ID.fullmatch(
            row["discovery_id"]
        ):
            errors.append(f"{prefix} has invalid search-hit discovery anchor")
        if row["discovery_kind"] == "SEARCH_HIT" and (
            source_unit is None or row["source_asset_id"]
        ):
            errors.append(f"{prefix} search discovery source is inconsistent")
        if row["closure_scope"] not in ROUTE_CLOSURE_SCOPES:
            errors.append(f"{prefix} has invalid closure scope")
        if row["status"] not in ROUTE_STATUSES:
            errors.append(f"{prefix} has invalid status")
        targets = parsed_string_list(
            row["target_unit_ids"], f"{prefix}.target_unit_ids", errors
        )
        target_assets = parsed_string_list(
            row["target_asset_ids"], f"{prefix}.target_asset_ids", errors
        )
        attempts = parsed_string_list(
            row["attempts"], f"{prefix}.attempts", errors
        )
        parsed_string_list(
            row["vocabulary_terms"], f"{prefix}.vocabulary_terms", errors
        )
        if any(value not in unit_ids for value in targets):
            errors.append(f"{prefix} targets unknown source unit")
        if any(value not in asset_ids for value in target_assets):
            errors.append(f"{prefix} targets unknown asset")
        if not row["literal_target"].strip() or not row["expected_topic"].strip():
            errors.append(f"{prefix} lacks target/topic")
        try:
            owning_stage = int(row["owning_stage"])
        except ValueError:
            owning_stage = -1
        if source_unit is not None:
            expected_stage = stage_by_path[source_unit["path"]]
            if (
                row["discovery_kind"] == "SOURCE_UNIT"
                and owning_stage != expected_stage
            ):
                errors.append(
                    f"{prefix} source-anchored owning stage differs from source stage"
                )
            if (
                row["discovery_kind"] == "SOURCE_UNIT"
                and reading_review_epochs.get(row["source_unit_id"], -1)
                < discovery_epoch
            ):
                errors.append(
                    f"{prefix} source anchor postdates its source review epoch"
                )
            if (
                row["discovery_kind"] == "SOURCE_UNIT"
                and discovery_epoch
                not in unit_history_epochs.get(row["source_unit_id"], set())
            ):
                errors.append(
                    f"{prefix} source anchor lacks matching review-history epoch"
                )
            source_reading = reading_by_unit.get(row["source_unit_id"])
            if (
                source_reading is None
                or source_reading["review_status"] != "REVIEWED"
            ):
                errors.append(f"{prefix} source unit is not reviewed")
        if source_asset is not None:
            source_path = source_asset["physical_path"]
            if (
                row["discovery_kind"] == "IMAGE"
                and discovery_epoch
                not in asset_path_history_epochs.get(source_path, set())
            ):
                errors.append(
                    f"{prefix} image anchor lacks matching review-history epoch"
                )
            assignment = expected_assets.get(source_path)
            if assignment is None:
                errors.append(f"{prefix} source asset assignment is unknown")
            else:
                expected_stage = int(assignment["assignment_stage"])
                if (
                    row["discovery_kind"] == "IMAGE"
                    and owning_stage != expected_stage
                ):
                    errors.append(
                        f"{prefix} image-anchored owning stage differs from "
                        "asset stage"
                    )
            if source_asset["inspection_status"] != "SCREENED":
                errors.append(f"{prefix} source asset is not screened")
        defect = row["defect_boundary"].strip()
        if row["status"] == "PENDING":
            if targets or target_assets or defect:
                errors.append(f"{prefix} pending route has final disposition data")
        elif row["status"] == "RESOLVED":
            if (not targets and not target_assets) or defect:
                errors.append(
                    f"{prefix} resolved route lacks targets or claims a defect"
                )
            if any(
                reading_by_unit[target]["review_status"] != "REVIEWED"
                for target in targets
                if target in reading_by_unit
            ):
                errors.append(f"{prefix} resolves to an unreviewed source unit")
            if any(
                asset_record_by_id[target]["inspection_status"] != "SCREENED"
                for target in target_assets
                if target in asset_record_by_id
            ):
                errors.append(f"{prefix} resolves to an unscreened asset")
        elif row["status"] == "MISSING_TARGET_FINAL":
            if targets or target_assets or not attempts or not defect:
                errors.append(
                    f"{prefix} final missing route needs attempts/defect and no target"
                )
        if row["status"] == "RESOLVED":
            target_stages = {
                stage_by_path[unit_by_id[target]["path"]]
                for target in targets
                if target in unit_by_id
            }
            target_stages.update(
                int(
                    expected_assets[
                        asset_record_by_id[target]["physical_path"]
                    ]["assignment_stage"]
                )
                for target in target_assets
                if target in asset_record_by_id
                and asset_record_by_id[target]["physical_path"] in expected_assets
            )
            if (
                row["closure_scope"] == "WITHIN_STAGE"
                and any(stage != owning_stage for stage in target_stages)
            ):
                errors.append(f"{prefix} within-stage route crosses stage boundary")
            if (
                row["closure_scope"] == "CROSS_RANGE"
                and target_stages
                and all(stage == owning_stage for stage in target_stages)
            ):
                errors.append(f"{prefix} cross-range route resolves only within stage")

    evidence_ids_global: set[str] = set()
    if [row.get("id") for row in candidates] != [
        f"B{index:04d}" for index in range(1, len(candidates) + 1)
    ]:
        errors.append("candidate IDs are not append-only B sequence")
    for candidate in candidates:
        validate_candidate(
            candidate,
            candidate_ids,
            unit_ids,
            image_paths,
            route_ids,
            evidence_ids_global,
            errors,
        )
    evidence_id_order = [
        evidence.get("evidence_id")
        for candidate in candidates
        for evidence in candidate.get("source_evidence", [])
        if isinstance(evidence, dict)
    ]
    expected_evidence_ids = {
        f"E{index:06d}" for index in range(1, len(evidence_id_order) + 1)
    }
    if (
        len(evidence_id_order) != len(set(evidence_id_order))
        or set(evidence_id_order) != expected_evidence_ids
    ):
        errors.append(
            "global evidence IDs are not a unique contiguous E allocation"
        )
    for candidate in candidates:
        local_ids = [
            evidence.get("evidence_id")
            for evidence in candidate.get("source_evidence", [])
            if isinstance(evidence, dict)
        ]
        if local_ids != sorted(
            local_ids,
            key=lambda value: (
                int(value[1:])
                if isinstance(value, str) and E_ID.fullmatch(value)
                else 10**9
            ),
        ):
            errors.append(
                f"candidate {candidate.get('id')} evidence IDs are not "
                "strictly increasing"
            )

    candidate_by_id = {candidate["id"]: candidate for candidate in candidates}
    evidence_by_group: dict[str, list[tuple[str, dict[str, Any]]]] = {}
    evidence_group_minimum_e: dict[str, int] = {}
    for candidate in candidates:
        for evidence in candidate.get("source_evidence", []):
            if isinstance(evidence, dict):
                group_id = str(evidence.get("evidence_group_id", ""))
                evidence_by_group.setdefault(group_id, []).append(
                    (candidate["id"], evidence)
                )
                evidence_id = evidence.get("evidence_id")
                if isinstance(evidence_id, str) and E_ID.fullmatch(evidence_id):
                    evidence_group_minimum_e[group_id] = min(
                        evidence_group_minimum_e.get(group_id, 10**9),
                        int(evidence_id[1:]),
                    )
    expected_group_ids = [
        f"G{index:06d}" for index in range(1, len(evidence_by_group) + 1)
    ]
    if set(evidence_by_group) != set(expected_group_ids):
        errors.append("global evidence-group IDs are not contiguous")
    groups_by_first_evidence = sorted(
        evidence_by_group,
        key=lambda group_id: evidence_group_minimum_e.get(group_id, 10**9),
    )
    if groups_by_first_evidence != expected_group_ids:
        errors.append(
            "evidence-group numeric order differs from minimum-E allocation order"
        )
    split_children: set[str] = set()
    supersession_targets: dict[str, list[str]] = {
        candidate_id: [] for candidate_id in candidate_ids
    }
    for candidate in candidates:
        source_number = (
            int(candidate["id"][1:])
            if B_ID.fullmatch(candidate["id"])
            else -1
        )
        for relation in candidate.get("related_candidate_ids", []):
            if not isinstance(relation, dict):
                continue
            relation_kind = relation.get("relation")
            if relation_kind not in {"MERGED_INTO", "SPLIT_INTO"}:
                continue
            target_id = relation.get("candidate_id")
            target = candidate_by_id.get(target_id)
            if target is None:
                continue
            supersession_targets[candidate["id"]].append(target_id)
            target_number = (
                int(target_id[1:])
                if isinstance(target_id, str) and B_ID.fullmatch(target_id)
                else -1
            )
            if relation_kind == "MERGED_INTO" and target_number >= source_number:
                errors.append(
                    f"candidate {candidate['id']} does not merge into an earlier ID"
                )
            if relation_kind == "SPLIT_INTO":
                if target_number <= source_number:
                    errors.append(
                        f"candidate {candidate['id']} split child is not a new ID"
                    )
                if target_id in split_children:
                    errors.append(f"candidate {target_id} has multiple split parents")
                split_children.add(target_id)

        direct_targets = [
            candidate_by_id[target_id]
            for target_id in supersession_targets[candidate["id"]]
            if target_id in candidate_by_id
        ]
        if candidate["record_status"] == "MERGED_REDIRECT" and direct_targets:
            target = direct_targets[0]
            for field in (
                "source_unit_ids",
                "image_witnesses",
                "cross_reference_ids",
            ):
                if not set(candidate[field]).issubset(set(target[field])):
                    errors.append(
                        f"candidate {candidate['id']} merge drops {field}"
                    )
        if candidate["record_status"] == "SPLIT_SUPERSEDED" and direct_targets:
            for field in (
                "source_unit_ids",
                "image_witnesses",
                "cross_reference_ids",
            ):
                target_union = set().union(
                    *(set(target[field]) for target in direct_targets)
                )
                if not set(candidate[field]).issubset(target_union):
                    errors.append(
                        f"candidate {candidate['id']} split drops {field}"
                    )

        source_evidence = {
            item["evidence_id"]: item
            for item in candidate.get("source_evidence", [])
            if isinstance(item, dict) and "evidence_id" in item
        }
        direct_target_ids = set(supersession_targets[candidate["id"]])
        for reassignment in candidate.get("evidence_reassignments", []):
            if not isinstance(reassignment, dict):
                continue
            source_item = source_evidence.get(reassignment.get("from_evidence_id"))
            for mapped in reassignment.get("targets", []):
                if not isinstance(mapped, dict):
                    continue
                target_id = mapped.get("candidate_id")
                if target_id not in direct_target_ids:
                    errors.append(
                        f"candidate {candidate['id']} reassigns evidence outside "
                        "its direct supersession targets"
                    )
                    continue
                target_candidate = candidate_by_id.get(target_id)
                if target_candidate is None:
                    continue
                target_item = next(
                    (
                        item
                        for item in target_candidate["source_evidence"]
                        if item["evidence_id"] == mapped.get("evidence_id")
                    ),
                    None,
                )
                if target_item is None:
                    errors.append(
                        f"candidate {candidate['id']} maps to missing target evidence"
                    )
                elif source_item is not None and (
                    source_item["source_unit_id"] != target_item["source_unit_id"]
                    or source_item["image_path"] != target_item["image_path"]
                ):
                    errors.append(
                        f"candidate {candidate['id']} evidence reassignment "
                        "changes its canonical witness"
                    )

    lineage_state: dict[str, int] = {}
    lineage_terminals: dict[str, set[str]] = {}

    def terminal_descendants(candidate_id: str) -> set[str]:
        state = lineage_state.get(candidate_id, 0)
        if state == 1:
            errors.append(f"candidate lineage cycle reaches {candidate_id}")
            return set()
        if state == 2:
            return lineage_terminals[candidate_id]
        lineage_state[candidate_id] = 1
        candidate = candidate_by_id[candidate_id]
        if candidate["record_status"] == "ACTIVE":
            terminals = {candidate_id}
        else:
            terminals: set[str] = set()
            for target_id in supersession_targets.get(candidate_id, []):
                if target_id in candidate_by_id:
                    terminals.update(terminal_descendants(target_id))
            if not terminals:
                errors.append(
                    f"candidate {candidate_id} lineage has no active descendant"
                )
        lineage_state[candidate_id] = 2
        lineage_terminals[candidate_id] = terminals
        return terminals

    for candidate_id in candidate_ids:
        terminal_descendants(candidate_id)

    candidate_source_links: dict[str, set[str]] = {
        unit_id: set() for unit_id in unit_ids
    }
    for candidate in candidates:
        candidate_id = candidate["id"]
        if candidate["record_status"] == "ACTIVE":
            for source_unit_id in candidate["source_unit_ids"]:
                if source_unit_id in candidate_source_links:
                    candidate_source_links[source_unit_id].add(candidate_id)
        linked_rows = [
            reading_by_unit[source_unit_id]
            for source_unit_id in candidate["source_unit_ids"]
            if source_unit_id in reading_by_unit
        ]
        actual_linked_units = {
            unit_id
            for unit_id, links in reading_candidate_links.items()
            if candidate_id in links
        }
        if candidate["record_status"] != "ACTIVE" and actual_linked_units:
            errors.append(
                f"candidate {candidate_id} tombstone retains reading-ledger links"
            )
        if any(row["review_status"] != "REVIEWED" for row in linked_rows):
            errors.append(f"candidate {candidate_id} links an unreviewed source unit")
        for route_id in candidate["cross_reference_ids"]:
            route = route_by_id.get(route_id)
            if route is not None:
                route_unit_is_owned = (
                    route["source_unit_id"] in candidate["source_unit_ids"]
                )
                route_asset = asset_record_by_id.get(route["source_asset_id"])
                route_asset_is_owned = (
                    route_asset is not None
                    and route_asset["physical_path"]
                    in candidate["image_witnesses"]
                )
                if not route_unit_is_owned and not route_asset_is_owned:
                    errors.append(
                        f"candidate {candidate_id} cross-reference source is "
                        "absent from candidate provenance"
                    )

    for unit_id in unit_ids:
        if reading_candidate_links.get(unit_id, set()) != candidate_source_links[
            unit_id
        ]:
            errors.append(
                f"reading {unit_id} candidate links are not the exact reverse join"
            )

    route_source_links: dict[str, set[str]] = {
        unit_id: set() for unit_id in unit_ids
    }
    for route in routes:
        if route["source_unit_id"] in route_source_links:
            route_source_links[route["source_unit_id"]].add(route["route_id"])
    for unit_id in unit_ids:
        if reading_route_links.get(unit_id, set()) != route_source_links[unit_id]:
            errors.append(
                f"reading {unit_id} route links are not the exact reverse join"
            )

    if len(assets) != len(manifest["images"]):
        errors.append("asset ledger row count differs from physical images")
    if [row.get("asset_id") for row in assets] != [
        f"A{index:06d}" for index in range(1, len(assets) + 1)
    ]:
        errors.append("asset IDs are not a total canonical sequence")
    if [row.get("physical_path") for row in assets] != [
        image["path"] for image in manifest["images"]
    ]:
        errors.append("asset ledger order/set differs from physical images")
    screened_count = 0
    asset_route_links: dict[str, set[str]] = {}
    asset_review_epochs: dict[str, int] = {}
    for row in assets:
        path = row.get("physical_path", "")
        image = image_by_path.get(path)
        if image is None:
            continue
        prefix = f"asset {row.get('asset_id')}"
        if row.get("sha256") != image["sha256"] or row.get("bytes") != str(
            image["bytes"]
        ):
            errors.append(f"{prefix} static physical record mismatch")
        expected_assignment = expected_assets.get(path)
        if expected_assignment is None:
            errors.append(f"{prefix} lacks recomputable assignment")
        else:
            for key, expected in expected_assignment.items():
                if row.get(key) != expected:
                    errors.append(f"{prefix} exact assignment mismatch: {key}")
        assignment_path = row.get("assignment_path", "")
        document = document_by_path.get(assignment_path)
        if document is None:
            errors.append(f"{prefix} has unknown assignment path")
            assignment_stage = -1
        else:
            try:
                assignment_stage = int(row.get("assignment_stage", ""))
            except ValueError:
                assignment_stage = -1
            if assignment_stage != stage_for_document(document):
                errors.append(f"{prefix} assignment stage mismatch")
        linked_candidates = parsed_string_list(
            row.get("candidate_ids", ""), f"{prefix}.candidate_ids", errors
        )
        linked_routes = parsed_string_list(
            row.get("route_ids", ""), f"{prefix}.route_ids", errors
        )
        asset_route_links[row.get("asset_id", "")] = set(linked_routes)
        risk_flags = parsed_string_list(
            row.get("risk_flags", ""), f"{prefix}.risk_flags", errors
        )
        if any(value not in candidate_ids for value in linked_candidates):
            errors.append(f"{prefix} links unknown candidate")
        if any(value not in route_ids for value in linked_routes):
            errors.append(f"{prefix} links unknown route")
        if any(value not in VISUAL_RISK_FLAGS for value in risk_flags):
            errors.append(f"{prefix} has invalid visual risk flag")
        status = row.get("inspection_status")
        if status == "PENDING":
            if (
                row.get("visual_role")
                or row.get("review_epoch")
                or row.get("source_status")
                or risk_flags
                or row.get("evidence_statement")
                or row.get("review_stage")
                or row.get("reviewer")
                or row.get("uncertainty")
                or linked_candidates
                or linked_routes
                or row.get("original_resolution_status") != "NOT_REVIEWED"
                or row.get("transcription_status") != "NOT_APPLICABLE"
            ):
                errors.append(f"{prefix} pending row contains inspection result")
        elif status == "SCREENED":
            screened_count += 1
            try:
                review_epoch = int(row.get("review_epoch", ""))
            except ValueError:
                review_epoch = -1
            if review_epoch < 1:
                errors.append(f"{prefix} has invalid review epoch")
            else:
                asset_review_epochs[path] = review_epoch
                discovery_epochs.add(review_epoch)
            if row.get("visual_role") not in VISUAL_ROLES:
                errors.append(f"{prefix} has invalid visual role")
            if row.get("source_status") not in SOURCE_STATUSES:
                errors.append(f"{prefix} has invalid source status")
            uncertainty = row.get("uncertainty", "").strip()
            if row.get("source_status") == "CLEAR" and uncertainty:
                errors.append(f"{prefix} CLEAR source has an uncertainty boundary")
            if (
                row.get("source_status") in {
                    "AMBIGUOUS",
                    "DEFECTIVE",
                    "CONFLICTING",
                }
                and not uncertainty
            ):
                errors.append(f"{prefix} non-clear source lacks uncertainty boundary")
            if (
                row.get("visual_role") == "SOURCE_DEFECT"
                and row.get("source_status") == "CLEAR"
            ):
                errors.append(f"{prefix} source-defect role has CLEAR source status")
            high_risk = bool(risk_flags)
            resolution = row.get("original_resolution_status")
            if high_risk and resolution != "REVIEWED":
                errors.append(f"{prefix} risky image lacks original-resolution review")
            if not high_risk and resolution not in {"NOT_REQUIRED", "REVIEWED"}:
                errors.append(f"{prefix} lacks resolution disposition")
            transcription = row.get("transcription_status")
            if transcription not in {"NOT_REQUIRED", "CHECKED"}:
                errors.append(f"{prefix} has invalid transcription status")
            if "TEXT_BEARING" in risk_flags and transcription != "CHECKED":
                errors.append(f"{prefix} text-bearing image lacks checked transcription")
            if row.get("visual_role") == "NATIVE_EVIDENCE":
                if "CONSTRUCTION_BEARING" not in risk_flags:
                    errors.append(
                        f"{prefix} native evidence lacks construction-bearing flag"
                    )
                if resolution != "REVIEWED" or transcription != "CHECKED":
                    errors.append(
                        f"{prefix} native evidence lacks resolution/transcription check"
                    )
            if not row.get("evidence_statement", "").strip():
                errors.append(f"{prefix} lacks evidence statement")
            if not row.get("reviewer", "").strip():
                errors.append(f"{prefix} lacks reviewer")
            try:
                review_stage = int(row.get("review_stage", ""))
            except ValueError:
                review_stage = -1
            if review_stage != assignment_stage:
                errors.append(f"{prefix} reviewed outside assigned stage")
        else:
            errors.append(f"{prefix} has invalid inspection_status")

    for route in routes:
        if route.get("discovery_kind") != "IMAGE":
            continue
        source_asset = asset_record_by_id.get(route.get("source_asset_id", ""))
        if source_asset is None:
            continue
        try:
            route_epoch = int(route.get("discovery_epoch", ""))
        except ValueError:
            continue
        source_path = source_asset.get("physical_path", "")
        if asset_review_epochs.get(source_path, -1) < route_epoch:
            errors.append(
                f"route {route.get('route_id')} image anchor postdates "
                "its asset review epoch"
            )

    expected_asset_route_links: dict[str, set[str]] = {
        asset_id: set() for asset_id in asset_ids
    }
    for route in routes:
        if route["source_asset_id"] in expected_asset_route_links:
            expected_asset_route_links[route["source_asset_id"]].add(
                route["route_id"]
            )
    for asset_id in asset_ids:
        if asset_route_links.get(asset_id, set()) != expected_asset_route_links[
            asset_id
        ]:
            errors.append(
                f"asset {asset_id} route links are not the exact reverse join"
            )

    asset_candidate_links: dict[str, set[str]] = {
        candidate_id: set() for candidate_id in candidate_ids
    }
    asset_by_path = {row["physical_path"]: row for row in assets}
    for row in assets:
        for candidate_id in parsed_string_list(
            row["candidate_ids"],
            f"asset {row['asset_id']}.candidate_ids",
            errors,
        ):
            asset_candidate_links.setdefault(candidate_id, set()).add(
                row["physical_path"]
            )
    for candidate in candidates:
        candidate_id = candidate["id"]
        witnesses = set(candidate["image_witnesses"])
        expected_witness_links = (
            witnesses if candidate["record_status"] == "ACTIVE" else set()
        )
        if asset_candidate_links.get(candidate_id, set()) != expected_witness_links:
            errors.append(
                f"candidate {candidate_id} image witnesses lack exact asset reverse joins"
            )
        provenance_statuses = {
            reading_by_unit[source_unit_id]["source_status"]
            for source_unit_id in candidate["source_unit_ids"]
            if source_unit_id in reading_by_unit
        }
        provenance_statuses.update(
            asset_by_path[image_path]["source_status"]
            for image_path in candidate["image_witnesses"]
            if image_path in asset_by_path
            and asset_by_path[image_path]["inspection_status"] == "SCREENED"
        )
        if set(candidate["source_status"]) != provenance_statuses:
            errors.append(
                f"candidate {candidate_id} source_status is not the exact "
                "unit/asset provenance aggregate"
            )
        for evidence in candidate["source_evidence"]:
            image_path = evidence.get("image_path")
            if image_path is None:
                continue
            asset = asset_by_path.get(image_path)
            if asset is None or asset["inspection_status"] != "SCREENED":
                errors.append(
                    f"candidate {candidate_id} image evidence is not screened"
                )
                continue
            if evidence.get("strength") in {
                "DIRECT_IDENTITY",
                "DIRECT_PARTIAL_MECHANICS",
                "DIRECT_COMPLETE_MECHANICS",
            } and (
                asset["visual_role"] != "NATIVE_EVIDENCE"
                or asset["original_resolution_status"] != "REVIEWED"
                or asset["transcription_status"] != "CHECKED"
            ):
                errors.append(
                    f"candidate {candidate_id} direct image evidence lacks "
                    "resolution/transcription verification"
                )

    if require_all_reviewed and screened_count != len(assets):
        errors.append("not every physical image is screened")

    search_fields = {
        "schema_version",
        "phase",
        "tool_assumptions",
        "vocabulary",
        "rounds",
        "fixed_point",
    }
    if not isinstance(search, dict):
        errors.append("search-rounds root is not an object")
        search = {}
    if set(search) != search_fields:
        errors.append("search-rounds fields do not match blind allowlist")
    if forbidden_keys(search):
        errors.append("search-rounds contains forbidden blind field")
    if search.get("schema_version") != 1 or search.get("phase") != "blind_discovery":
        errors.append("search-rounds schema/phase is invalid")
    search_assumptions = exact_string_list(
        search.get("tool_assumptions"),
        "search-rounds.tool_assumptions",
        errors,
    )
    vocabulary = exact_string_list(
        search.get("vocabulary"),
        "search-rounds.vocabulary",
        errors,
    )
    rounds = search.get("rounds")
    if not isinstance(rounds, list):
        errors.append("search-rounds.rounds must be an array")
        rounds = []
    errors.extend(search_query_id_sequence_errors(rounds))
    seen_queries: set[str] = set()
    seen_hits: set[str] = set()
    hit_by_id: dict[str, dict[str, Any]] = {}
    hit_round_meta: dict[str, tuple[int, int, str]] = {}
    seen_new_vocabulary: set[str] = set()
    seen_new_candidates: set[str] = set()
    seen_new_evidence_groups: set[str] = set()
    seen_new_routes: set[str] = set()
    ordered_stage18_candidates: list[str] = []
    ordered_stage18_routes: list[str] = []
    expected_next_hit = 1
    prior_round_key: tuple[int, int, int] | None = None
    for round_index, round_record in enumerate(rounds, start=1):
        required = {
            "round_id",
            "epoch",
            "kind",
            "owning_stage",
            "queries",
            "tool_assumptions",
            "result_ids",
            "result_digest",
            "hits",
            "new_vocabulary",
            "new_candidates",
            "new_evidence_groups",
            "new_routes",
            "rerun_digest",
        }
        if not isinstance(round_record, dict) or set(round_record) != required:
            errors.append(f"search round {round_index} fields are invalid")
            continue
        if round_record["round_id"] != f"S{round_index:03d}":
            errors.append(f"search round {round_index} ID is invalid")
        epoch = round_record["epoch"]
        kind = round_record["kind"]
        owning_stage = round_record["owning_stage"]
        if not isinstance(epoch, int) or epoch < 1:
            errors.append(f"search round {round_index} has invalid epoch")
            epoch = -1
        else:
            discovery_epochs.add(epoch)
            non_review_epochs.add(epoch)
        if kind not in {"LOCAL", "SATURATION"}:
            errors.append(f"search round {round_index} has invalid kind")
        if not isinstance(owning_stage, int) or not 4 <= owning_stage <= 18:
            errors.append(f"search round {round_index} has invalid owning stage")
            owning_stage = -1
        if kind == "LOCAL" and not 4 <= owning_stage <= 17:
            errors.append(f"search round {round_index} LOCAL stage is invalid")
        if kind == "SATURATION" and owning_stage != 18:
            errors.append(f"search round {round_index} SATURATION stage is not 18")
        round_key = (
            epoch,
            owning_stage,
            0 if kind == "LOCAL" else 1,
        )
        if prior_round_key is not None and round_key < prior_round_key:
            errors.append(f"search round {round_index} violates audit event order")
        prior_round_key = round_key

        queries = round_record["queries"]
        if not isinstance(queries, list) or not queries:
            errors.append(f"search round {round_index} requires queries")
            queries = []
        current_query_ids: set[str] = set()
        current_query_scopes: dict[str, set[str]] = {}
        for query_index, query in enumerate(queries, start=1):
            if not isinstance(query, dict) or set(query) != SEARCH_QUERY_FIELDS:
                errors.append(
                    f"search round {round_index} query {query_index} fields are invalid"
                )
                continue
            query_id = query["query_id"]
            if not isinstance(query_id, str) or not Q_ID.fullmatch(query_id):
                errors.append(f"search query {query_id!r} has invalid ID")
            if query_id in seen_queries:
                errors.append(f"duplicate search query ID: {query_id}")
            seen_queries.add(query_id)
            current_query_ids.add(query_id)
            if not isinstance(query["family"], str) or not query["family"].strip():
                errors.append(f"search query {query_id} lacks family")
            if not isinstance(query["pattern"], str) or not query["pattern"]:
                errors.append(f"search query {query_id} lacks pattern")
            if query["mode"] not in {"LITERAL", "REGEX"}:
                errors.append(f"search query {query_id} has invalid mode")
            if not isinstance(query["case_sensitive"], bool):
                errors.append(
                    f"search query {query_id} case_sensitive is not boolean"
                )
            if not isinstance(query["whole_word"], bool):
                errors.append(
                    f"search query {query_id} whole_word is not boolean"
                )
            scope_paths = exact_string_list(
                query["scope_paths"],
                f"search query {query_id}.scope_paths",
                errors,
                nonempty=True,
            )
            if any(path not in document_by_path for path in scope_paths):
                errors.append(f"search query {query_id} has unknown scope path")
            if kind == "LOCAL" and any(
                stage_by_path.get(path) != owning_stage for path in scope_paths
            ):
                errors.append(
                    f"search query {query_id} leaves its local owning stage"
                )
            if any(
                reading_row["review_status"] != "REVIEWED"
                for reading_row in reading
                if reading_row["path"] in scope_paths
            ):
                errors.append(
                    f"search query {query_id} scopes an unreviewed document"
                )
            if any(
                asset["inspection_status"] != "SCREENED"
                for asset in assets
                if asset["assignment_path"] in scope_paths
            ):
                errors.append(
                    f"search query {query_id} scopes an unscreened asset"
                )
            current_query_scopes[query_id] = set(scope_paths)

        if kind == "SATURATION":
            if reviewed_count != len(units):
                errors.append(
                    f"search round {round_index} saturation precedes full reading"
                )
            if screened_count != len(assets):
                errors.append(
                    f"search round {round_index} saturation precedes asset screening"
                )

        round_assumptions = exact_string_list(
            round_record["tool_assumptions"],
            f"search round {round_index}.tool_assumptions",
            errors,
        )
        if any(item not in search_assumptions for item in round_assumptions):
            errors.append(
                f"search round {round_index} has undeclared tool assumption"
            )

        hit_ids: list[str] = []
        result_pairs: set[tuple[str, str]] = set()
        ordered_result_pairs: list[tuple[str, str]] = []
        hits = round_record["hits"]
        if not isinstance(hits, list):
            errors.append(f"search round {round_index}.hits must be an array")
            hits = []
        for hit in hits:
            expected = {
                "hit_id",
                "query_id",
                "source_unit_id",
                "context_sha256",
                "disposition",
                "candidate_ids",
                "route_ids",
                "rationale",
            }
            if not isinstance(hit, dict) or set(hit) != expected:
                errors.append(f"search round {round_index} hit fields are invalid")
                continue
            hit_id = hit["hit_id"]
            expected_hit_id = f"H{expected_next_hit:06d}"
            expected_next_hit += 1
            if not isinstance(hit_id, str) or not H_ID.fullmatch(hit_id):
                errors.append(f"search hit {hit_id!r} has invalid ID")
            if hit_id != expected_hit_id:
                errors.append(
                    f"search hit {hit_id} violates canonical append-only sequence"
                )
            if hit_id in seen_hits:
                errors.append(f"duplicate search hit ID: {hit_id}")
            seen_hits.add(hit_id)
            if isinstance(hit_id, str):
                hit_by_id[hit_id] = hit
                hit_round_meta[hit_id] = (epoch, owning_stage, kind)
            hit_ids.append(hit_id)
            if hit["query_id"] not in current_query_ids:
                errors.append(
                    f"search hit {hit_id} references a query outside its round"
                )
            pair = (hit["query_id"], hit["source_unit_id"])
            if pair in result_pairs:
                errors.append(f"search hit {hit_id} duplicates query/unit result")
            result_pairs.add(pair)
            ordered_result_pairs.append(pair)
            source_unit = unit_by_id.get(hit["source_unit_id"])
            if source_unit is None:
                errors.append(f"search hit {hit_id} has unknown source unit")
            else:
                if hit["context_sha256"] != source_unit["sha256"]:
                    errors.append(f"search hit {hit_id} has stale context hash")
                if source_unit["path"] not in current_query_scopes.get(
                    hit["query_id"], set()
                ):
                    errors.append(f"search hit {hit_id} lies outside query scope")
                source_reading = reading_by_unit.get(hit["source_unit_id"])
                if (
                    source_reading is None
                    or source_reading["review_status"] != "REVIEWED"
                ):
                    errors.append(
                        f"search hit {hit_id} points to an unreviewed unit"
                    )
            if hit["disposition"] not in SEARCH_HIT_DISPOSITIONS:
                errors.append(f"search hit {hit_id} lacks final blind disposition")
            hit_candidates = exact_string_list(
                hit["candidate_ids"],
                f"search hit {hit_id}.candidate_ids",
                errors,
            )
            hit_routes = exact_string_list(
                hit["route_ids"],
                f"search hit {hit_id}.route_ids",
                errors,
            )
            if any(value not in candidate_ids for value in hit_candidates):
                errors.append(f"search hit {hit_id} links unknown candidate")
            if any(value not in route_ids for value in hit_routes):
                errors.append(f"search hit {hit_id} links unknown route")
            if hit["disposition"] in {
                "GOVERNED_CANDIDATE_OR_SUPPORT",
                "DUPLICATE",
            } and not hit_candidates:
                errors.append(
                    f"search hit {hit_id} governed/duplicate disposition "
                    "lacks candidate link"
                )
            if hit["disposition"] == "CROSS_REFERENCE" and not hit_routes:
                errors.append(
                    f"search hit {hit_id} cross-reference disposition lacks route"
                )
            if hit["disposition"] == "EXCLUSION" and (
                hit_candidates or hit_routes
            ):
                errors.append(
                    f"search hit {hit_id} exclusion carries candidate/route links"
                )
            if not isinstance(hit["rationale"], str) or not hit[
                "rationale"
            ].strip():
                errors.append(f"search hit {hit_id} lacks rationale")

        rerun_pairs, rerun_errors = execute_frozen_queries(
            queries, units, source_root
        )
        errors.extend(rerun_errors)
        if ordered_result_pairs != rerun_pairs:
            errors.append(
                f"search round {round_index} recorded results differ from "
                "independent query execution"
            )

        result_ids = exact_string_list(
            round_record["result_ids"],
            f"search round {round_index}.result_ids",
            errors,
        )
        if result_ids != hit_ids:
            errors.append(f"search round {round_index} result IDs differ from hits")
        try:
            computed_digest = search_result_digest(round_record)
        except (KeyError, TypeError):
            computed_digest = None
            errors.append(f"search round {round_index} digest payload is invalid")
        if round_record["result_digest"] != computed_digest:
            errors.append(f"search round {round_index} result digest is stale")
        if round_record["rerun_digest"] != computed_digest:
            errors.append(f"search round {round_index} rerun did not reproduce")

        delta_values: dict[str, list[str]] = {}
        for key in (
            "new_vocabulary",
            "new_candidates",
            "new_evidence_groups",
            "new_routes",
        ):
            delta_values[key] = exact_string_list(
                round_record[key],
                f"search round {round_index}.{key}",
                errors,
            )
        if any(
            item not in vocabulary for item in delta_values["new_vocabulary"]
        ):
            errors.append(
                f"search round {round_index} new vocabulary absent from final set"
            )
        if any(
            item not in candidate_ids for item in delta_values["new_candidates"]
        ):
            errors.append(
                f"search round {round_index} names unknown new candidate"
            )
        if any(item not in route_ids for item in delta_values["new_routes"]):
            errors.append(f"search round {round_index} names unknown new route")
        for group_id in delta_values["new_evidence_groups"]:
            if not G_ID.fullmatch(group_id):
                errors.append(
                    f"search round {round_index} has invalid evidence group ID"
                )
            group_records = evidence_by_group.get(group_id, [])
            if not group_records:
                errors.append(
                    f"search round {round_index} names unknown evidence group "
                    f"{group_id}"
                )
            for candidate_id, evidence in group_records:
                anchor = evidence.get("discovery_anchor", {})
                if (
                    anchor.get("epoch") != epoch
                    or anchor.get("kind") != "SEARCH_HIT"
                    or anchor.get("id") not in hit_ids
                ):
                    errors.append(
                        f"search round {round_index} evidence group {group_id} "
                        f"has inconsistent anchor on {candidate_id}"
                    )
        for candidate_id in delta_values["new_candidates"]:
            candidate = candidate_by_id.get(candidate_id)
            anchor = candidate.get("discovery_anchor", {}) if candidate else {}
            if (
                candidate is not None
                and (
                    candidate["discovery_stage"] != owning_stage
                    or anchor.get("epoch") != epoch
                    or anchor.get("kind") != "SEARCH_HIT"
                    or anchor.get("id") not in hit_ids
                )
            ):
                errors.append(
                    f"search round {round_index} new candidate {candidate_id} "
                    "has inconsistent discovery anchor"
                )
        for route_id in delta_values["new_routes"]:
            route = route_by_id.get(route_id)
            if (
                route is not None
                and (
                    route["owning_stage"] != str(owning_stage)
                    or route["discovery_epoch"] != str(epoch)
                    or route["discovery_kind"] != "SEARCH_HIT"
                    or route["discovery_id"] not in hit_ids
                )
            ):
                errors.append(
                    f"search round {round_index} new route {route_id} "
                    "has inconsistent discovery anchor"
                )
        for key, seen in (
            ("new_vocabulary", seen_new_vocabulary),
            ("new_candidates", seen_new_candidates),
            ("new_evidence_groups", seen_new_evidence_groups),
            ("new_routes", seen_new_routes),
        ):
            duplicates = set(delta_values[key]) & seen
            if duplicates:
                errors.append(
                    f"search round {round_index} repeats prior {key}: "
                    f"{sorted(duplicates)}"
                )
            seen.update(delta_values[key])
        ordered_stage18_candidates.extend(delta_values["new_candidates"])
        ordered_stage18_routes.extend(delta_values["new_routes"])

    search_discovered_candidates = [
        candidate["id"]
        for candidate in candidates
        if candidate.get("discovery_anchor", {}).get("kind") == "SEARCH_HIT"
    ]
    if search_discovered_candidates != ordered_stage18_candidates:
        errors.append(
            "search-discovered candidate sequence differs from round discovery order"
        )
    search_discovered_routes = [
        route["route_id"]
        for route in routes
        if route["discovery_kind"] == "SEARCH_HIT"
    ]
    if search_discovered_routes != ordered_stage18_routes:
        errors.append(
            "search-discovered route sequence differs from round discovery order"
        )

    route_anchor_ordinals: dict[tuple[int, str, str], list[int]] = {}
    prior_route_key: tuple[int, int, int, int, int, int] | None = None
    for route in routes:
        route_id = route["route_id"]
        try:
            epoch = int(route["discovery_epoch"])
            ordinal = int(route["discovery_ordinal"])
        except ValueError:
            continue
        kind = route["discovery_kind"]
        anchor_id = route["discovery_id"]
        route_key: tuple[int, int, int, int, int, int] | None = None
        if kind == "SOURCE_UNIT":
            unit = unit_by_id.get(anchor_id)
            if unit is not None:
                stage = stage_by_path[unit["path"]]
                route_key = (
                    epoch,
                    stage,
                    int(unit["document_order"]),
                    0,
                    unit_position[anchor_id],
                    ordinal,
                )
        elif kind == "IMAGE":
            asset = asset_record_by_id.get(anchor_id)
            if asset is not None:
                assignment = expected_assets.get(asset["physical_path"])
                if assignment is not None:
                    assignment_path = assignment["assignment_path"]
                    stage = int(assignment["assignment_stage"])
                    route_key = (
                        epoch,
                        stage,
                        int(document_by_path[assignment_path]["order"]),
                        1,
                        image_position[asset["physical_path"]],
                        ordinal,
                    )
        elif kind == "SEARCH_HIT":
            hit = hit_by_id.get(anchor_id)
            meta = hit_round_meta.get(anchor_id)
            if hit is None or meta is None:
                errors.append(f"route {route_id} anchor hit is unknown")
            else:
                hit_epoch, stage, _ = meta
                route_key = (
                    epoch,
                    stage,
                    len(document_by_path) + 1,
                    2,
                    int(anchor_id[1:]),
                    ordinal,
                )
                if hit_epoch != epoch or route["owning_stage"] != str(stage):
                    errors.append(
                        f"route {route_id} anchor epoch/stage differs from round"
                    )
                if route_id not in hit["route_ids"]:
                    errors.append(f"route {route_id} anchor hit lacks route link")
                if route["source_unit_id"] != hit["source_unit_id"]:
                    errors.append(
                        f"route {route_id} source differs from anchor hit"
                    )
        route_anchor_ordinals.setdefault((epoch, kind, anchor_id), []).append(
            ordinal
        )
        if route_key is not None:
            if prior_route_key is not None and route_key < prior_route_key:
                errors.append(
                    f"route {route_id} violates frozen allocation traversal"
                )
            prior_route_key = route_key
    for anchor_identity, ordinals in route_anchor_ordinals.items():
        if sorted(ordinals) != list(range(1, len(ordinals) + 1)):
            errors.append(
                f"route anchor {anchor_identity} ordinals are not contiguous"
            )

    fixed_point = search.get("fixed_point")
    if fixed_point is not None:
        required_fixed = {
            "round_id",
            "zero_delta",
            "rerun_reproduced",
            "result_digest",
        }
        if not isinstance(fixed_point, dict) or set(fixed_point) != required_fixed:
            errors.append("search fixed_point fields are invalid")
        elif not rounds:
            errors.append("search fixed_point exists without rounds")
        else:
            last = rounds[-1]
            if last.get("kind") != "SATURATION" or last.get("owning_stage") != 18:
                errors.append("search fixed_point final round is not saturation")
            if fixed_point["round_id"] != last.get("round_id"):
                errors.append("search fixed_point does not name the final round")
            if fixed_point["zero_delta"] is not True:
                errors.append("search fixed_point does not certify zero delta")
            if fixed_point["rerun_reproduced"] is not True:
                errors.append("search fixed_point does not certify rerun")
            if fixed_point["result_digest"] != last.get("result_digest"):
                errors.append("search fixed_point digest differs from final round")
            if any(
                last.get(key)
                for key in (
                    "new_vocabulary",
                    "new_candidates",
                    "new_evidence_groups",
                    "new_routes",
                )
            ):
                errors.append("search fixed_point final round is not zero-delta")
            if last.get("result_digest") != last.get("rerun_digest"):
                errors.append("search fixed_point final rerun differs")
            final_scope = {
                path
                for query in last.get("queries", [])
                if isinstance(query, dict)
                for path in query.get("scope_paths", [])
            }
            if final_scope != set(document_by_path):
                errors.append(
                    "search fixed_point final round does not scope every document"
                )

    anchor_ordinals: dict[tuple[int, str, str], list[int]] = {}
    prior_anchor_key: tuple[int, int, int, int, int, int] | None = None
    for candidate in candidates:
        candidate_id = candidate["id"]
        anchor = candidate["discovery_anchor"]
        if not isinstance(anchor, dict) or not {
            "epoch",
            "kind",
            "id",
            "ordinal",
        }.issubset(anchor):
            continue
        epoch = anchor["epoch"]
        kind = anchor["kind"]
        anchor_id = anchor["id"]
        ordinal = anchor["ordinal"]
        if (
            not isinstance(epoch, int)
            or epoch < 1
            or kind not in {"SOURCE_UNIT", "IMAGE", "SEARCH_HIT"}
            or not isinstance(anchor_id, str)
            or not isinstance(ordinal, int)
            or ordinal < 1
        ):
            continue
        discovery_epochs.add(epoch)
        non_review_epochs.add(epoch)
        anchor_stage = -1
        anchor_key: tuple[int, int, int, int, int, int] | None = None
        if kind == "SOURCE_UNIT":
            source_unit = unit_by_id.get(anchor_id)
            if source_unit is None:
                errors.append(f"candidate {candidate_id} anchor unit is unknown")
            else:
                anchor_stage = stage_by_path[source_unit["path"]]
                anchor_key = (
                    epoch,
                    anchor_stage,
                    int(source_unit["document_order"]),
                    0,
                    unit_position[anchor_id],
                    ordinal,
                )
                if anchor_id not in candidate["source_unit_ids"]:
                    errors.append(
                        f"candidate {candidate_id} anchor unit lacks provenance"
                    )
                if reading_review_epochs.get(anchor_id, -1) < epoch:
                    errors.append(
                        f"candidate {candidate_id} source anchor postdates "
                        "its source review epoch"
                    )
                if epoch not in unit_history_epochs.get(anchor_id, set()):
                    errors.append(
                        f"candidate {candidate_id} source anchor lacks matching "
                        "review-history epoch"
                    )
        elif kind == "IMAGE":
            assignment = expected_assets.get(anchor_id)
            if assignment is None:
                errors.append(f"candidate {candidate_id} anchor image is unknown")
            else:
                assignment_path = assignment["assignment_path"]
                anchor_stage = int(assignment["assignment_stage"])
                anchor_key = (
                    epoch,
                    anchor_stage,
                    int(document_by_path[assignment_path]["order"]),
                    1,
                    image_position[anchor_id],
                    ordinal,
                )
                if anchor_id not in candidate["image_witnesses"]:
                    errors.append(
                        f"candidate {candidate_id} anchor image lacks provenance"
                    )
                if asset_review_epochs.get(anchor_id, -1) < epoch:
                    errors.append(
                        f"candidate {candidate_id} image anchor postdates "
                        "its asset review epoch"
                    )
                if epoch not in asset_path_history_epochs.get(anchor_id, set()):
                    errors.append(
                        f"candidate {candidate_id} image anchor lacks matching "
                        "review-history epoch"
                    )
        elif kind == "SEARCH_HIT":
            hit = hit_by_id.get(anchor_id)
            meta = hit_round_meta.get(anchor_id)
            if hit is None or meta is None:
                errors.append(f"candidate {candidate_id} anchor hit is unknown")
            else:
                hit_epoch, anchor_stage, _ = meta
                anchor_key = (
                    epoch,
                    anchor_stage,
                    len(document_by_path) + 1,
                    2,
                    int(anchor_id[1:]),
                    ordinal,
                )
                if epoch != hit_epoch:
                    errors.append(
                        f"candidate {candidate_id} anchor epoch differs from "
                        "search round"
                    )
                if candidate_id not in hit["candidate_ids"]:
                    errors.append(
                        f"candidate {candidate_id} anchor hit lacks candidate link"
                    )
        if anchor_stage != candidate["discovery_stage"]:
            errors.append(
                f"candidate {candidate_id} discovery stage differs from anchor stage"
            )
        anchor_ordinals.setdefault((epoch, kind, anchor_id), []).append(ordinal)
        if anchor_key is not None:
            if prior_anchor_key is not None and anchor_key < prior_anchor_key:
                errors.append(
                    f"candidate {candidate_id} violates frozen B-ID traversal order"
                )
            prior_anchor_key = anchor_key
    for anchor_identity, ordinals in anchor_ordinals.items():
        if sorted(ordinals) != list(range(1, len(ordinals) + 1)):
            errors.append(
                f"candidate anchor {anchor_identity} ordinals are not contiguous"
            )

    evidence_anchor_ordinals: dict[tuple[int, str, str], list[int]] = {}
    search_evidence_groups: set[str] = set()
    ordered_evidence: list[tuple[int, dict[str, Any], dict[str, Any]]] = []
    for candidate in candidates:
        for evidence in candidate["source_evidence"]:
            evidence_id = evidence.get("evidence_id", "")
            if isinstance(evidence_id, str) and E_ID.fullmatch(evidence_id):
                ordered_evidence.append((int(evidence_id[1:]), candidate, evidence))
    ordered_evidence.sort(key=lambda item: item[0])
    prior_evidence_key: tuple[int, int, int, int, int, int] | None = None
    for _, candidate, evidence in ordered_evidence:
        candidate_id = candidate["id"]
        anchor = evidence.get("discovery_anchor", {})
        if not isinstance(anchor, dict) or not {
            "epoch",
            "kind",
            "id",
            "ordinal",
        }.issubset(anchor):
            continue
        epoch = anchor["epoch"]
        kind = anchor["kind"]
        anchor_id = anchor["id"]
        ordinal = anchor["ordinal"]
        if (
            not isinstance(epoch, int)
            or epoch < 1
            or kind not in {"SOURCE_UNIT", "IMAGE", "SEARCH_HIT"}
            or not isinstance(anchor_id, str)
            or not isinstance(ordinal, int)
            or ordinal < 1
        ):
            continue
        discovery_epochs.add(epoch)
        non_review_epochs.add(epoch)
        candidate_epoch = candidate.get("discovery_anchor", {}).get("epoch")
        if isinstance(candidate_epoch, int) and epoch < candidate_epoch:
            errors.append(
                f"candidate {candidate_id} evidence predates candidate discovery epoch"
            )
        evidence_anchor_ordinals.setdefault(
            (epoch, kind, anchor_id), []
        ).append(ordinal)
        evidence_key: tuple[int, int, int, int, int, int] | None = None
        if kind == "SEARCH_HIT":
            search_evidence_groups.add(evidence["evidence_group_id"])
            hit = hit_by_id.get(anchor_id)
            meta = hit_round_meta.get(anchor_id)
            if hit is None or meta is None:
                errors.append(
                    f"candidate {candidate_id} evidence anchor hit is unknown"
                )
            else:
                hit_epoch, anchor_stage, _ = meta
                evidence_key = (
                    epoch,
                    anchor_stage,
                    len(document_by_path) + 1,
                    2,
                    int(anchor_id[1:]),
                    ordinal,
                )
                if hit_epoch != epoch:
                    errors.append(
                        f"candidate {candidate_id} evidence epoch differs "
                        "from search round"
                    )
                if candidate_id not in hit["candidate_ids"]:
                    errors.append(
                        f"candidate {candidate_id} evidence anchor hit lacks "
                        "candidate link"
                    )
        elif kind == "SOURCE_UNIT":
            source_unit = unit_by_id.get(anchor_id)
            if source_unit is None:
                errors.append(
                    f"candidate {candidate_id} evidence anchor unit is unknown"
                )
            else:
                anchor_stage = stage_by_path[source_unit["path"]]
                evidence_key = (
                    epoch,
                    anchor_stage,
                    int(source_unit["document_order"]),
                    0,
                    unit_position[anchor_id],
                    ordinal,
                )
                if reading_review_epochs.get(anchor_id, -1) < epoch:
                    errors.append(
                        f"candidate {candidate_id} evidence source anchor "
                        "postdates its source review epoch"
                    )
                if epoch not in unit_history_epochs.get(anchor_id, set()):
                    errors.append(
                        f"candidate {candidate_id} evidence source anchor lacks "
                        "matching review-history epoch"
                    )
        elif kind == "IMAGE":
            assignment = expected_assets.get(anchor_id)
            if assignment is None:
                errors.append(
                    f"candidate {candidate_id} evidence anchor image is unknown"
                )
            else:
                assignment_path = assignment["assignment_path"]
                evidence_key = (
                    epoch,
                    int(assignment["assignment_stage"]),
                    int(document_by_path[assignment_path]["order"]),
                    1,
                    image_position[anchor_id],
                    ordinal,
                )
                if asset_review_epochs.get(anchor_id, -1) < epoch:
                    errors.append(
                        f"candidate {candidate_id} evidence image anchor "
                        "postdates its asset review epoch"
                    )
                if epoch not in asset_path_history_epochs.get(anchor_id, set()):
                    errors.append(
                        f"candidate {candidate_id} evidence image anchor lacks "
                        "matching review-history epoch"
                    )
        if evidence_key is not None:
            if prior_evidence_key is not None and evidence_key < prior_evidence_key:
                errors.append(
                    f"candidate {candidate_id} evidence violates frozen "
                    "allocation traversal"
                )
            prior_evidence_key = evidence_key
    for anchor_identity, ordinals in evidence_anchor_ordinals.items():
        if sorted(ordinals) != list(range(1, len(ordinals) + 1)):
            errors.append(
                f"evidence anchor {anchor_identity} ordinals are not contiguous"
            )
    if search_evidence_groups != seen_new_evidence_groups:
        errors.append(
            "search-discovered evidence groups differ from search-round deltas"
        )
    if discovery_epochs and discovery_epochs != set(
        range(1, max(discovery_epochs) + 1)
    ):
        errors.append(
            "global discovery epochs are not contiguous from 1 across "
            "review history, candidates, evidence, routes, and search"
        )
    if non_review_epochs and (
        not history_epochs or max(non_review_epochs) > max(history_epochs)
    ):
        errors.append(
            "search/non-review discovery opens an epoch not established by "
            "append-only review history"
        )

    def validate_local_epoch_coverage(
        stage_number: int,
        round_limit: int,
        closure_label: str,
        *,
        required_epochs: set[int] | None = None,
    ) -> None:
        expected_scopes = {
            epoch: set(paths)
            for (stage, epoch), paths in history_local_scopes.items()
            if stage == stage_number
        }
        actual_rounds: dict[int, list[dict[str, Any]]] = {}
        for index, round_record in enumerate(rounds):
            if index >= round_limit or not isinstance(round_record, dict):
                continue
            if (
                round_record.get("kind") != "LOCAL"
                or round_record.get("owning_stage") != stage_number
            ):
                continue
            epoch = round_record.get("epoch")
            if isinstance(epoch, int) and epoch >= 1:
                actual_rounds.setdefault(epoch, []).append(round_record)
        epochs_to_check = set(actual_rounds)
        if required_epochs is None:
            epochs_to_check.update(expected_scopes)
        else:
            epochs_to_check.update(required_epochs)
        for epoch in sorted(epochs_to_check):
            local_rounds = actual_rounds.get(epoch, [])
            local_scope = {
                path
                for round_record in local_rounds
                for query in round_record.get("queries", [])
                if isinstance(query, dict)
                for path in query.get("scope_paths", [])
            }
            if not local_rounds or local_scope != expected_scopes.get(
                epoch, set()
            ):
                errors.append(
                    f"{closure_label} lacks exact Stage {stage_number} "
                    f"review-epoch {epoch} LOCAL-round coverage"
                )

    max_discovery_epoch = max(discovery_epochs, default=0)
    for stage_number in range(4, 18):
        stage_history_epochs = {
            epoch
            for stage, epoch in history_local_scopes
            if stage == stage_number
        }
        closed_prior_epochs = {
            epoch for epoch in stage_history_epochs if epoch < max_discovery_epoch
        }
        actual_local_epochs = {
            round_record.get("epoch")
            for round_record in rounds
            if isinstance(round_record, dict)
            and round_record.get("kind") == "LOCAL"
            and round_record.get("owning_stage") == stage_number
            and isinstance(round_record.get("epoch"), int)
        }
        epochs_to_require = closed_prior_epochs | actual_local_epochs
        if epochs_to_require:
            validate_local_epoch_coverage(
                stage_number,
                len(rounds),
                "global epoch closure",
                required_epochs=epochs_to_require,
            )

    for required_stage in require_stages:
        if required_stage == 18:
            if reviewed_count != len(units):
                errors.append("stage 18 began before every source unit was reviewed")
            if screened_count != len(assets):
                errors.append("stage 18 began before every asset was screened")
            if any(route["status"] == "PENDING" for route in routes):
                errors.append("stage 18 has pending cross-reference routes")
            if fixed_point is None:
                errors.append("stage 18 lacks a validated search fixed point")
            continue
        assigned_paths = {
            path
            for path, document in document_by_path.items()
            if stage_for_document(document) == required_stage
        }
        assigned_reading = [row for row in reading if row["path"] in assigned_paths]
        if not assigned_reading or any(
            row["review_status"] != "REVIEWED" for row in assigned_reading
        ):
            errors.append(f"stage {required_stage} source units are not fully reviewed")
        assigned_assets = [
            row for row in assets if row["assignment_path"] in assigned_paths
        ]
        if any(row["inspection_status"] != "SCREENED" for row in assigned_assets):
            errors.append(f"stage {required_stage} assets are not fully screened")
        validate_local_epoch_coverage(
            required_stage,
            len(rounds),
            f"stage {required_stage}",
            required_epochs={
                epoch
                for stage, epoch in history_local_scopes
                if stage == required_stage
            },
        )
        if any(
            route["status"] == "PENDING"
            for route in routes
            if route["owning_stage"] == str(required_stage)
            and route["closure_scope"] == "WITHIN_STAGE"
        ):
            errors.append(
                f"stage {required_stage} has pending within-stage routes"
            )

    if 18 in require_stages or require_all_reviewed:
        if isinstance(fixed_point, dict):
            fixed_round_id = fixed_point.get("round_id")
            fixed_round_index = next(
                (
                    index
                    for index, round_record in enumerate(rounds)
                    if isinstance(round_record, dict)
                    and round_record.get("round_id") == fixed_round_id
                ),
                len(rounds),
            )
        else:
            fixed_round_index = len(rounds)
        for stage_number in range(4, 18):
            validate_local_epoch_coverage(
                stage_number,
                fixed_round_index,
                "stage 18/all-reviewed closure before saturation",
                required_epochs={
                    epoch
                    for stage, epoch in history_local_scopes
                    if stage == stage_number
                },
            )

    if require_all_reviewed:
        if any(route["status"] == "PENDING" for route in routes):
            errors.append("all-reviewed closure has pending routes")
        if fixed_point is None:
            errors.append("all-reviewed closure lacks search fixed point")

    text_patterns, pattern_errors = load_blind_text_patterns()
    errors.extend(pattern_errors)
    for artifact_name, artifact in (
        ("reading-ledger", reading),
        ("candidate-ledger", candidates),
        ("cross-reference-ledger", routes),
        ("asset-ledger", assets),
        ("review-history", review_history),
        ("search-rounds", search),
    ):
        leaks = blind_text_leaks(artifact, text_patterns, artifact_name)
        if leaks:
            errors.append(
                f"{artifact_name} contains prohibited reconciliation text: "
                + "; ".join(leaks[:10])
            )

    return errors


def mutation_checks(
    manifest: dict[str, Any],
    units: list[dict[str, Any]],
    reading: list[dict[str, str]],
    candidates: list[dict[str, Any]],
    routes: list[dict[str, str]],
    assets: list[dict[str, str]],
    search: dict[str, Any],
    review_history: list[dict[str, Any]],
) -> list[str]:
    failures: list[str] = []
    base_reading = copy.deepcopy(reading)
    base_assets = copy.deepcopy(assets)
    base_search = copy.deepcopy(search)
    unit = units[0]
    unit_id = unit["id"]
    path = unit["path"]
    stage = stage_for_document(
        next(document for document in manifest["documents"] if document["path"] == path)
    )

    base_reading[0].update(
        {
            "review_status": "REVIEWED",
            "review_epoch": "1",
            "review_disposition": "CANDIDATE",
            "source_status": "CLEAR",
            "secondary_roles": "[]",
            "candidate_ids": '["B0001"]',
            "route_ids": '["R000001"]',
            "evidence_statement": "Introduces a bounded fixture construction.",
            "review_stage": str(stage),
            "reviewer": "fixture-reviewer",
        }
    )
    for row in base_reading[1:]:
        if row["path"] != path:
            continue
        row.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": "1",
                "review_disposition": "NO_CONSTRUCTION",
                "source_status": "CLEAR",
                "uncertainty": "",
                "secondary_roles": "[]",
                "candidate_ids": "[]",
                "route_ids": "[]",
                "evidence_statement": "No construction in this fixture unit.",
                "review_stage": str(stage),
                "reviewer": "fixture-reviewer",
            }
        )
    for row in base_assets:
        if row["assignment_path"] != path:
            continue
        row.update(
            {
                "inspection_status": "SCREENED",
                "review_epoch": "1",
                "visual_role": "DECORATIVE",
                "source_status": "CLEAR",
                "risk_flags": "[]",
                "original_resolution_status": "NOT_REQUIRED",
                "transcription_status": "NOT_REQUIRED",
                "candidate_ids": "[]",
                "route_ids": "[]",
                "evidence_statement": "No construction-bearing visual content.",
                "review_stage": str(stage),
                "reviewer": "fixture-reviewer",
                "uncertainty": "",
            }
        )

    unit_by_fixture_id = {item["id"]: item for item in units}

    def append_history_event(
        prior: list[dict[str, Any]],
        reading_state: list[dict[str, str]],
        asset_state: list[dict[str, str]],
        source_path: str,
        epoch: int,
        mode: str,
        reviewer: str,
        prior_rounds: list[dict[str, Any]],
        trigger_search_kind: str | None = None,
        trigger_hit_ids: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        result = copy.deepcopy(prior)
        prior_path_event = next(
            (
                item
                for item in reversed(result)
                if item.get("source_paths") == [source_path]
            ),
            None,
        )
        event = close_review_event(
            {
                "review_id": f"V{len(result) + 1:06d}",
                "epoch": epoch,
                "stage": stage_for_document(
                    next(
                        document
                        for document in manifest["documents"]
                        if document["path"] == source_path
                    )
                ),
                "mode": mode,
                "reviewer": reviewer,
                "source_paths": [source_path],
                "source_unit_ids": [
                    item["id"] for item in units if item["path"] == source_path
                ],
                "asset_ids": [
                    item["asset_id"]
                    for item in asset_state
                    if item["assignment_path"] == source_path
                ],
                "previous_path_result_sha256": (
                    prior_path_event["result_projection_sha256"]
                    if prior_path_event is not None
                    else None
                ),
                "trigger_search_kind": trigger_search_kind,
                "trigger_hit_ids": trigger_hit_ids or [],
            },
            unit_by_fixture_id,
            {
                item["source_unit_id"]: item for item in reading_state
            },
            {item["asset_id"]: item for item in asset_state},
            result[-1]["event_sha256"] if result else None,
            prior_rounds,
        )
        result.append(event)
        return result

    base_history = append_history_event(
        [],
        base_reading,
        base_assets,
        path,
        1,
        "INITIAL",
        "fixture-reviewer",
        [],
    )
    evidence = {
        "evidence_id": "E000001",
        "evidence_group_id": "G000001",
        "discovery_anchor": {
            "epoch": 1,
            "kind": "SOURCE_UNIT",
            "id": unit_id,
            "ordinal": 1,
        },
        "source_unit_id": unit_id,
        "image_path": None,
        "strength": "DIRECT_COMPLETE_MECHANICS",
        "modality": "PROSE",
        "claim": "The fixture supplies every test fingerprint field.",
        "fingerprint_fields": list(FINGERPRINT_FIELDS),
    }
    candidate = {key: [] for key in CANDIDATE_FIELDS}
    candidate.update(
        {
            "id": "B0001",
            "record_status": "ACTIVE",
            "provisional_name": "bounded fixture construction",
            "aliases": [],
            "discovery_stage": stage,
            "discovery_anchor": {
                "epoch": 1,
                "kind": "SOURCE_UNIT",
                "id": unit_id,
                "ordinal": 1,
            },
            "source_unit_ids": [unit_id],
            "source_evidence": [evidence],
            "source_status": ["CLEAR"],
            "image_witnesses": [],
            "evidence_strength": ["DIRECT_COMPLETE_MECHANICS"],
            "field_support": {
                field: "SUPPORTED" for field in FINGERPRINT_FIELDS
            },
            "fingerprint": {
                field: {
                    "status": "SUPPORTED",
                    "value": f"fixture {field}",
                    "evidence_ids": ["E000001"],
                    "reason": "",
                }
                for field in FINGERPRINT_FIELDS
            },
            "parameters": [],
            "variants": [],
            "missing_mechanics": [],
            "uncertainties": [],
            "related_candidate_ids": [],
            "cross_reference_ids": ["R000001"],
            "evidence_reassignments": [],
        }
    )
    route = {key: "" for key in CROSS_REFERENCE_HEADER}
    route.update(
        {
            "route_id": "R000001",
            "source_unit_id": unit_id,
            "source_asset_id": "",
            "discovery_epoch": "1",
            "discovery_kind": "SOURCE_UNIT",
            "discovery_id": unit_id,
            "discovery_ordinal": "1",
            "literal_target": "later fixture page",
            "route_kind": "PAGE",
            "expected_topic": "fixture mechanics",
            "owning_stage": str(stage),
            "closure_scope": "CROSS_RANGE",
            "status": "PENDING",
            "target_unit_ids": "[]",
            "target_asset_ids": "[]",
            "attempts": "[]",
            "vocabulary_terms": '["fixture mechanics"]',
            "defect_boundary": "",
        }
    )
    base_candidates = [candidate]
    base_routes = [route]

    base_errors = validate_objects(
        manifest,
        units,
        base_reading,
        base_candidates,
        base_routes,
        base_assets,
        base_search,
        base_history,
    )
    if base_errors:
        return ["valid candidate/route mutation fixture failed: " + "; ".join(base_errors)]

    defect_reading = copy.deepcopy(base_reading)
    defect_unit = units[1]
    defect_document = next(
        document
        for document in manifest["documents"]
        if document["path"] == defect_unit["path"]
    )
    defect_reading[1].update(
        {
            "review_status": "REVIEWED",
            "review_epoch": "1",
            "review_disposition": "SOURCE_DEFECT_OR_AMBIGUITY",
            "source_status": "DEFECTIVE",
            "uncertainty": (
                "The source unit ends mid-expression, so its construction "
                "boundary cannot be recovered locally."
            ),
            "secondary_roles": '["SOURCE_DEFECT"]',
            "candidate_ids": "[]",
            "route_ids": "[]",
            "evidence_statement": (
                "The visible source boundary is incomplete and is retained "
                "as an explicit defect."
            ),
            "review_stage": str(stage_for_document(defect_document)),
            "reviewer": "fixture-reviewer",
        }
    )
    defect_reading_history = append_history_event(
        [],
        defect_reading,
        base_assets,
        path,
        1,
        "INITIAL",
        "fixture-reviewer",
        [],
    )
    defect_reading_errors = validate_objects(
        manifest,
        units,
        defect_reading,
        base_candidates,
        base_routes,
        base_assets,
        base_search,
        defect_reading_history,
    )
    if defect_reading_errors:
        failures.append(
            "valid source-defect reading fixture failed: "
            + "; ".join(defect_reading_errors)
        )

    ordered_fixture_paths = [
        document["path"]
        for document in sorted(
            manifest["documents"],
            key=lambda document: (
                stage_for_document(document),
                int(document["order"]),
            ),
        )
    ]
    defect_asset_path = next(
        candidate_path
        for candidate_path in ordered_fixture_paths
        if any(
            item["assignment_path"] == candidate_path for item in base_assets
        )
    )
    defect_asset_reading = copy.deepcopy(base_reading)
    defect_asset = copy.deepcopy(base_assets)
    defect_stage = stage_for_document(
        next(
            document
            for document in manifest["documents"]
            if document["path"] == defect_asset_path
        )
    )
    for row in defect_asset_reading:
        if row["path"] != defect_asset_path:
            continue
        row.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": "1",
                "review_disposition": "NO_CONSTRUCTION",
                "source_status": "CLEAR",
                "uncertainty": "",
                "secondary_roles": "[]",
                "candidate_ids": "[]",
                "route_ids": "[]",
                "evidence_statement": "No construction in this fixture unit.",
                "review_stage": str(defect_stage),
                "reviewer": "fixture-reviewer",
            }
        )
    for row in defect_asset:
        if row["assignment_path"] != defect_asset_path:
            continue
        row.update(
            {
                "inspection_status": "SCREENED",
                "review_epoch": "1",
                "visual_role": "DECORATIVE",
                "source_status": "CLEAR",
                "risk_flags": "[]",
                "original_resolution_status": "NOT_REQUIRED",
                "transcription_status": "NOT_REQUIRED",
                "candidate_ids": "[]",
                "route_ids": "[]",
                "evidence_statement": "No construction-bearing visual content.",
                "review_stage": str(defect_stage),
                "reviewer": "fixture-reviewer",
                "uncertainty": "",
            }
        )
    defect_asset_index = next(
        index
        for index, item in enumerate(defect_asset)
        if item["assignment_path"] == defect_asset_path
    )
    defect_asset[defect_asset_index].update(
        {
            "inspection_status": "SCREENED",
            "review_epoch": "1",
            "visual_role": "SOURCE_DEFECT",
            "source_status": "DEFECTIVE",
            "risk_flags": '["AMBIGUOUS"]',
            "original_resolution_status": "REVIEWED",
            "transcription_status": "NOT_REQUIRED",
            "candidate_ids": "[]",
            "route_ids": "[]",
            "evidence_statement": (
                "The original-resolution image is visibly clipped at the "
                "construction boundary."
            ),
            "review_stage": defect_asset[defect_asset_index]["assignment_stage"],
            "reviewer": "fixture-reviewer",
            "uncertainty": (
                "The clipped edge prevents a complete reading of the depicted "
                "construction."
            ),
        }
    )
    defect_asset_history = append_history_event(
        base_history,
        defect_asset_reading,
        defect_asset,
        defect_asset_path,
        1,
        "INITIAL",
        "fixture-reviewer",
        [],
    )
    defect_asset_errors = validate_objects(
        manifest,
        units,
        defect_asset_reading,
        base_candidates,
        base_routes,
        defect_asset,
        base_search,
        defect_asset_history,
    )
    if defect_asset_errors:
        failures.append(
            "valid source-defect asset fixture failed: "
            + "; ".join(defect_asset_errors)
        )

    def zero_local_round(
        round_number: int,
        query_number: int,
        epoch: int,
        owning_stage: int,
        scope_paths: list[str],
    ) -> dict[str, Any]:
        round_record = {
            "round_id": f"S{round_number:03d}",
            "epoch": epoch,
            "kind": "LOCAL",
            "owning_stage": owning_stage,
            "queries": [
                {
                    "query_id": f"Q{query_number:04d}",
                    "family": "zero-result history fixture",
                    "pattern": "__AUDIT_HISTORY_IMPOSSIBLE_MATCH_83F2D1__",
                    "mode": "LITERAL",
                    "case_sensitive": True,
                    "whole_word": False,
                    "scope_paths": scope_paths,
                }
            ],
            "tool_assumptions": ["Deterministic zero-result history fixture."],
            "result_ids": [],
            "result_digest": "",
            "hits": [],
            "new_vocabulary": [],
            "new_candidates": [],
            "new_evidence_groups": [],
            "new_routes": [],
            "rerun_digest": "",
        }
        digest = search_result_digest(round_record)
        round_record["result_digest"] = digest
        round_record["rerun_digest"] = digest
        return round_record

    epoch1_round = zero_local_round(1, 1, 1, stage, [path])
    reopened_search = {
        "schema_version": 1,
        "phase": "blind_discovery",
        "tool_assumptions": ["Deterministic zero-result history fixture."],
        "vocabulary": [],
        "rounds": [epoch1_round],
        "fixed_point": None,
    }
    reopened_reading = copy.deepcopy(base_reading)
    reopened_assets = copy.deepcopy(base_assets)
    reopened_route = copy.deepcopy(route)
    reopened_route.update(
        {
            "route_id": "R000002",
            "discovery_epoch": "2",
            "discovery_ordinal": "1",
            "literal_target": "reopened-pass fixture target",
            "expected_topic": "reopened-pass fixture mechanics",
            "vocabulary_terms": '["reopened-pass fixture mechanics"]',
        }
    )
    reopened_routes = [copy.deepcopy(route), reopened_route]
    for row in reopened_reading:
        if row["path"] == path:
            row["review_epoch"] = "2"
    for row in reopened_assets:
        if row["assignment_path"] == path:
            row["review_epoch"] = "2"
    reopened_reading[0]["route_ids"] = '["R000001","R000002"]'
    reopened_history = append_history_event(
        base_history,
        reopened_reading,
        reopened_assets,
        path,
        2,
        "REOPEN",
        "fixture-reviewer",
        reopened_search["rounds"],
    )
    reopened_errors = validate_objects(
        manifest,
        units,
        reopened_reading,
        base_candidates,
        reopened_routes,
        reopened_assets,
        reopened_search,
        reopened_history,
    )
    if reopened_errors:
        failures.append(
            "valid reopened discovery-epoch fixture failed: "
            + "; ".join(reopened_errors)
        )

    audit_paths = [
        document["path"]
        for document in sorted(
            manifest["documents"],
            key=lambda document: (
                stage_for_document(document),
                int(document["order"]),
            ),
        )
    ]
    next_path = audit_paths[1]
    next_stage = stage_for_document(
        next(
            document
            for document in manifest["documents"]
            if document["path"] == next_path
        )
    )
    forward_reading = copy.deepcopy(reopened_reading)
    forward_assets = copy.deepcopy(reopened_assets)
    for row in forward_reading:
        if row["path"] != next_path:
            continue
        row.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": "2",
                "review_disposition": "NO_CONSTRUCTION",
                "source_status": "CLEAR",
                "uncertainty": "",
                "secondary_roles": "[]",
                "candidate_ids": "[]",
                "route_ids": "[]",
                "evidence_statement": "No construction in this fixture unit.",
                "review_stage": str(next_stage),
                "reviewer": "fixture-reviewer",
            }
        )
    for row in forward_assets:
        if row["assignment_path"] != next_path:
            continue
        row.update(
            {
                "inspection_status": "SCREENED",
                "review_epoch": "2",
                "visual_role": "DECORATIVE",
                "source_status": "CLEAR",
                "risk_flags": "[]",
                "original_resolution_status": "NOT_REQUIRED",
                "transcription_status": "NOT_REQUIRED",
                "candidate_ids": "[]",
                "route_ids": "[]",
                "evidence_statement": "No construction-bearing visual content.",
                "review_stage": str(next_stage),
                "reviewer": "fixture-reviewer",
                "uncertainty": "",
            }
        )
    forward_history = append_history_event(
        reopened_history,
        forward_reading,
        forward_assets,
        next_path,
        2,
        "INITIAL",
        "fixture-reviewer",
        reopened_search["rounds"],
    )
    epoch2_round = zero_local_round(
        2,
        2,
        2,
        stage,
        [path, next_path],
    )
    epoch3_search = copy.deepcopy(reopened_search)
    epoch3_search["rounds"].append(epoch2_round)
    repeated_reading = copy.deepcopy(forward_reading)
    repeated_assets = copy.deepcopy(forward_assets)
    for row in repeated_reading:
        if row["path"] == path:
            row["review_epoch"] = "3"
    for row in repeated_assets:
        if row["assignment_path"] == path:
            row["review_epoch"] = "3"
    repeated_history = append_history_event(
        forward_history,
        repeated_reading,
        repeated_assets,
        path,
        3,
        "REOPEN",
        "fixture-reviewer",
        epoch3_search["rounds"],
    )
    repeated_errors = validate_objects(
        manifest,
        units,
        repeated_reading,
        base_candidates,
        reopened_routes,
        repeated_assets,
        epoch3_search,
        repeated_history,
    )
    if repeated_errors:
        failures.append(
            "valid partial epoch1/reopen epoch2/forward epoch2/repeated epoch3 "
            "fixture failed: " + "; ".join(repeated_errors)
        )

    def expect_history_failure(
        name: str,
        reading_state: list[dict[str, str]],
        candidate_state: list[dict[str, Any]],
        route_state: list[dict[str, str]],
        asset_state: list[dict[str, str]],
        search_state: dict[str, Any],
        history_state: list[dict[str, Any]],
    ) -> None:
        if not validate_objects(
            manifest,
            units,
            reading_state,
            candidate_state,
            route_state,
            asset_state,
            search_state,
            history_state,
        ):
            failures.append(f"history mutation unexpectedly passed: {name}")

    expect_history_failure(
        "reviewed rows without history",
        base_reading,
        base_candidates,
        base_routes,
        base_assets,
        base_search,
        [],
    )
    forged_history = copy.deepcopy(base_history)
    forged_history[0]["input_projection_sha256"] = "0" * 64
    expect_history_failure(
        "forged history projection",
        base_reading,
        base_candidates,
        base_routes,
        base_assets,
        base_search,
        forged_history,
    )
    expect_history_failure(
        "stale latest review epoch",
        reopened_reading,
        base_candidates,
        reopened_routes,
        reopened_assets,
        reopened_search,
        base_history,
    )
    backfilled_reopen_history = append_history_event(
        base_history,
        reopened_reading,
        reopened_assets,
        path,
        2,
        "REOPEN",
        "fixture-reviewer",
        [],
    )
    expect_history_failure(
        "epoch advancement before prior local closure",
        reopened_reading,
        base_candidates,
        reopened_routes,
        reopened_assets,
        reopened_search,
        backfilled_reopen_history,
    )
    backward_epoch_history = append_history_event(
        reopened_history,
        forward_reading,
        forward_assets,
        next_path,
        1,
        "INITIAL",
        "fixture-reviewer",
        reopened_search["rounds"],
    )
    expect_history_failure(
        "review history moves backward in epoch",
        forward_reading,
        base_candidates,
        reopened_routes,
        forward_assets,
        reopened_search,
        backward_epoch_history,
    )

    skipped_reading = copy.deepcopy(reading)
    skipped_assets = copy.deepcopy(assets)
    for row in skipped_reading:
        if row["path"] != next_path:
            continue
        row.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": "1",
                "review_disposition": "NO_CONSTRUCTION",
                "source_status": "CLEAR",
                "uncertainty": "",
                "secondary_roles": "[]",
                "candidate_ids": "[]",
                "route_ids": "[]",
                "evidence_statement": "No construction in this fixture unit.",
                "review_stage": str(next_stage),
                "reviewer": "fixture-reviewer",
            }
        )
    for row in skipped_assets:
        if row["assignment_path"] != next_path:
            continue
        row.update(
            {
                "inspection_status": "SCREENED",
                "review_epoch": "1",
                "visual_role": "DECORATIVE",
                "source_status": "CLEAR",
                "risk_flags": "[]",
                "original_resolution_status": "NOT_REQUIRED",
                "transcription_status": "NOT_REQUIRED",
                "candidate_ids": "[]",
                "route_ids": "[]",
                "evidence_statement": "No construction-bearing visual content.",
                "review_stage": str(next_stage),
                "reviewer": "fixture-reviewer",
                "uncertainty": "",
            }
        )
    skipped_history = append_history_event(
        [],
        skipped_reading,
        skipped_assets,
        next_path,
        1,
        "INITIAL",
        "fixture-reviewer",
        [],
    )
    expect_history_failure(
        "INITIAL event skips an unread canonical path",
        skipped_reading,
        [],
        [],
        skipped_assets,
        base_search,
        skipped_history,
    )

    multipath_history = [
        close_review_event(
            {
                "review_id": "V000001",
                "epoch": 1,
                "stage": stage,
                "mode": "INITIAL",
                "reviewer": "fixture-reviewer",
                "source_paths": [path, next_path],
                "source_unit_ids": [
                    item["id"]
                    for item in units
                    if item["path"] in {path, next_path}
                ],
                "asset_ids": [
                    item["asset_id"]
                    for item in forward_assets
                    if item["assignment_path"] in {path, next_path}
                ],
            },
            unit_by_fixture_id,
            {
                item["source_unit_id"]: item for item in forward_reading
            },
            {item["asset_id"]: item for item in forward_assets},
            None,
            [],
        )
    ]
    expect_history_failure(
        "one event covers multiple or noncontiguous paths",
        forward_reading,
        base_candidates,
        base_routes,
        forward_assets,
        base_search,
        multipath_history,
    )

    allocation_candidate = copy.deepcopy(candidate)
    second_evidence = copy.deepcopy(evidence)
    second_evidence.update(
        {
            "evidence_id": "E000002",
            "evidence_group_id": "G000002",
            "discovery_anchor": {
                "epoch": 1,
                "kind": "SOURCE_UNIT",
                "id": unit_id,
                "ordinal": 2,
            },
            "strength": "CORROBORATING",
            "claim": "The same canonical unit independently corroborates the fixture.",
            "fingerprint_fields": [],
        }
    )
    allocation_candidate["source_evidence"].append(second_evidence)
    allocation_candidate["evidence_strength"] = [
        "DIRECT_COMPLETE_MECHANICS",
        "CORROBORATING",
    ]
    allocation_errors = validate_objects(
        manifest,
        units,
        base_reading,
        [allocation_candidate],
        base_routes,
        base_assets,
        base_search,
        base_history,
    )
    if allocation_errors:
        failures.append(
            "valid exact evidence-allocation fixture failed: "
            + "; ".join(allocation_errors)
        )

    def lineage_candidate(
        candidate_id: str,
        evidence_number: int,
        epoch: int,
        ordinal: int,
    ) -> dict[str, Any]:
        result = copy.deepcopy(candidate)
        evidence_id = f"E{evidence_number:06d}"
        group_id = f"G{evidence_number:06d}"
        result["id"] = candidate_id
        result["provisional_name"] = f"lineage fixture {candidate_id}"
        result["discovery_anchor"] = {
            "epoch": epoch,
            "kind": "SOURCE_UNIT",
            "id": unit_id,
            "ordinal": ordinal,
        }
        result["source_evidence"][0]["evidence_id"] = evidence_id
        result["source_evidence"][0]["evidence_group_id"] = group_id
        result["source_evidence"][0]["discovery_anchor"] = {
            "epoch": epoch,
            "kind": "SOURCE_UNIT",
            "id": unit_id,
            "ordinal": ordinal,
        }
        for field in FINGERPRINT_FIELDS:
            result["fingerprint"][field]["evidence_ids"] = [evidence_id]
        result["related_candidate_ids"] = []
        result["evidence_reassignments"] = []
        return result

    tail_candidate_one = lineage_candidate("B0001", 1, 1, 1)
    tail_candidate_two = lineage_candidate("B0002", 2, 1, 2)
    tail_candidate_two["cross_reference_ids"] = []
    tail_evidence = copy.deepcopy(tail_candidate_one["source_evidence"][0])
    tail_evidence.update(
        {
            "evidence_id": "E000003",
            "evidence_group_id": "G000003",
            "discovery_anchor": {
                "epoch": 1,
                "kind": "SOURCE_UNIT",
                "id": unit_id,
                "ordinal": 3,
            },
            "strength": "CORROBORATING",
            "claim": (
                "A later append-only evidence item corroborates the earlier "
                "candidate after another candidate already exists."
            ),
            "fingerprint_fields": [],
        }
    )
    tail_candidate_one["source_evidence"].append(tail_evidence)
    tail_candidate_one["evidence_strength"] = [
        "DIRECT_COMPLETE_MECHANICS",
        "CORROBORATING",
    ]
    tail_reading = copy.deepcopy(base_reading)
    tail_reading[0]["candidate_ids"] = '["B0001","B0002"]'
    tail_history = append_history_event(
        [],
        tail_reading,
        base_assets,
        path,
        1,
        "INITIAL",
        "fixture-reviewer",
        [],
    )
    tail_errors = validate_objects(
        manifest,
        units,
        tail_reading,
        [tail_candidate_one, tail_candidate_two],
        base_routes,
        base_assets,
        base_search,
        tail_history,
    )
    if tail_errors:
        failures.append(
            "valid E-tail appended to an earlier candidate failed: "
            + "; ".join(tail_errors)
        )

    lineage_candidates = [
        lineage_candidate("B0001", 1, 1, 1),
        lineage_candidate("B0002", 2, 1, 2),
        lineage_candidate("B0003", 3, 2, 1),
        lineage_candidate("B0004", 4, 2, 2),
    ]
    lineage_candidates[0].update(
        {
            "record_status": "SPLIT_SUPERSEDED",
            "related_candidate_ids": [
                {
                    "candidate_id": "B0003",
                    "relation": "SPLIT_INTO",
                    "proof_kind": "SPLIT_DISTINCTION",
                    "evidence_ids": ["E000001"],
                    "before_rationale": (
                        "The parent record combined two distinguishable "
                        "construction boundaries."
                    ),
                    "after_rationale": (
                        "This child retains the first construction boundary."
                    ),
                    "uncertainty": "",
                },
                {
                    "candidate_id": "B0004",
                    "relation": "SPLIT_INTO",
                    "proof_kind": "SPLIT_DISTINCTION",
                    "evidence_ids": ["E000001"],
                    "before_rationale": (
                        "The parent record combined two distinguishable "
                        "construction boundaries."
                    ),
                    "after_rationale": (
                        "This child retains the second construction boundary."
                    ),
                    "uncertainty": "",
                },
            ],
            "evidence_reassignments": [
                {
                    "from_evidence_id": "E000001",
                    "targets": [
                        {
                            "candidate_id": "B0003",
                            "evidence_id": "E000003",
                        },
                        {
                            "candidate_id": "B0004",
                            "evidence_id": "E000004",
                        },
                    ],
                }
            ],
        }
    )
    lineage_candidates[1]["source_evidence"][0][
        "strength"
    ] = "DIRECT_IDENTITY"
    lineage_candidates[1]["evidence_strength"] = ["DIRECT_IDENTITY"]
    lineage_candidates[1].update(
        {
            "record_status": "MERGED_REDIRECT",
            "related_candidate_ids": [
                {
                    "candidate_id": "B0001",
                    "relation": "MERGED_INTO",
                    "proof_kind": "PROVED_DUPLICATE_IDENTITY",
                    "evidence_ids": ["E000002"],
                    "before_rationale": "",
                    "after_rationale": "",
                    "uncertainty": "",
                }
            ],
            "evidence_reassignments": [
                {
                    "from_evidence_id": "E000002",
                    "targets": [
                        {
                            "candidate_id": "B0001",
                            "evidence_id": "E000001",
                        }
                    ],
                }
            ],
        }
    )
    lineage_candidates[3]["cross_reference_ids"] = []
    lineage_reading = copy.deepcopy(base_reading)
    lineage_assets = copy.deepcopy(base_assets)
    for row in lineage_reading:
        if row["path"] == path:
            row["review_epoch"] = "2"
    for row in lineage_assets:
        if row["assignment_path"] == path:
            row["review_epoch"] = "2"
    lineage_reading[0]["candidate_ids"] = '["B0003","B0004"]'
    lineage_history = append_history_event(
        base_history,
        lineage_reading,
        lineage_assets,
        path,
        2,
        "REOPEN",
        "fixture-reviewer",
        reopened_search["rounds"],
    )
    lineage_errors = validate_objects(
        manifest,
        units,
        lineage_reading,
        lineage_candidates,
        base_routes,
        lineage_assets,
        reopened_search,
        lineage_history,
    )
    if lineage_errors:
        failures.append(
            "valid multi-layer lineage fixture failed: "
            + "; ".join(lineage_errors)
        )
    broken_lineage = copy.deepcopy(lineage_candidates)
    broken_lineage[1]["evidence_reassignments"][0]["targets"][0][
        "evidence_id"
    ] = "E999999"

    mutations: list[
        tuple[
            str,
            list[dict[str, str]],
            list[dict[str, Any]],
            list[dict[str, str]],
            list[dict[str, str]],
            dict[str, Any],
        ]
    ] = []
    mutations.append(
        (
            "broken multi-layer evidence reassignment",
            lineage_reading,
            broken_lineage,
            base_routes,
            base_assets,
            base_search,
        )
    )
    reversed_evidence_order = copy.deepcopy(allocation_candidate)
    reversed_evidence_order["source_evidence"].reverse()
    mutations.append(
        (
            "reversed global E allocation order",
            base_reading,
            [reversed_evidence_order],
            base_routes,
            base_assets,
            base_search,
        )
    )
    reversed_group_order = copy.deepcopy(allocation_candidate)
    reversed_group_order["source_evidence"][0][
        "evidence_group_id"
    ] = "G000002"
    reversed_group_order["source_evidence"][1][
        "evidence_group_id"
    ] = "G000001"
    mutations.append(
        (
            "reversed first-occurrence G allocation order",
            base_reading,
            [reversed_group_order],
            base_routes,
            base_assets,
            base_search,
        )
    )
    generic_merge_evidence = copy.deepcopy(lineage_candidates)
    generic_merge_evidence[1]["source_evidence"][0][
        "strength"
    ] = "DIRECT_COMPLETE_MECHANICS"
    generic_merge_evidence[1]["evidence_strength"] = [
        "DIRECT_COMPLETE_MECHANICS"
    ]
    mutations.append(
        (
            "merge justified only by generic mechanics evidence",
            lineage_reading,
            generic_merge_evidence,
            base_routes,
            base_assets,
            base_search,
        )
    )
    missing_split_rationale = copy.deepcopy(lineage_candidates)
    missing_split_rationale[0]["related_candidate_ids"][0][
        "after_rationale"
    ] = ""
    mutations.append(
        (
            "split tombstone without explicit after rationale",
            lineage_reading,
            missing_split_rationale,
            base_routes,
            base_assets,
            base_search,
        )
    )
    missing_reading_uncertainty = copy.deepcopy(defect_reading)
    missing_reading_uncertainty[1]["uncertainty"] = ""
    mutations.append(
        (
            "non-clear reading without uncertainty boundary",
            missing_reading_uncertainty,
            base_candidates,
            base_routes,
            base_assets,
            base_search,
        )
    )
    clear_reading_uncertainty = copy.deepcopy(base_reading)
    clear_reading_uncertainty[0]["uncertainty"] = (
        "A CLEAR reading must not retain an uncertainty boundary."
    )
    mutations.append(
        (
            "CLEAR reading with uncertainty boundary",
            clear_reading_uncertainty,
            base_candidates,
            base_routes,
            base_assets,
            base_search,
        )
    )
    clear_defect_reading = copy.deepcopy(defect_reading)
    clear_defect_reading[1]["source_status"] = "CLEAR"
    clear_defect_reading[1]["uncertainty"] = ""
    mutations.append(
        (
            "source-defect reading marked CLEAR",
            clear_defect_reading,
            base_candidates,
            base_routes,
            base_assets,
            base_search,
        )
    )
    missing_asset_uncertainty = copy.deepcopy(defect_asset)
    missing_asset_uncertainty[defect_asset_index]["uncertainty"] = ""
    mutations.append(
        (
            "non-clear asset without uncertainty boundary",
            base_reading,
            base_candidates,
            base_routes,
            missing_asset_uncertainty,
            base_search,
        )
    )
    clear_asset_uncertainty = copy.deepcopy(defect_asset)
    clear_asset_uncertainty[defect_asset_index].update(
        {
            "visual_role": "CONTROL",
            "source_status": "CLEAR",
        }
    )
    mutations.append(
        (
            "CLEAR asset with uncertainty boundary",
            base_reading,
            base_candidates,
            base_routes,
            clear_asset_uncertainty,
            base_search,
        )
    )
    clear_defect_asset = copy.deepcopy(defect_asset)
    clear_defect_asset[defect_asset_index].update(
        {
            "source_status": "CLEAR",
            "uncertainty": "",
        }
    )
    mutations.append(
        (
            "source-defect asset marked CLEAR",
            base_reading,
            base_candidates,
            base_routes,
            clear_defect_asset,
            base_search,
        )
    )
    reviewed_without_epoch = copy.deepcopy(base_reading)
    reviewed_without_epoch[0]["review_epoch"] = ""
    mutations.append(
        (
            "reviewed reading without review epoch",
            reviewed_without_epoch,
            base_candidates,
            base_routes,
            base_assets,
            base_search,
        )
    )
    pending_with_epoch = copy.deepcopy(base_reading)
    pending_with_epoch[-1]["review_epoch"] = "1"
    mutations.append(
        (
            "pending reading with review epoch",
            pending_with_epoch,
            base_candidates,
            base_routes,
            base_assets,
            base_search,
        )
    )
    screened_without_epoch = copy.deepcopy(defect_asset)
    screened_without_epoch[defect_asset_index]["review_epoch"] = ""
    mutations.append(
        (
            "screened asset without review epoch",
            base_reading,
            base_candidates,
            base_routes,
            screened_without_epoch,
            base_search,
        )
    )
    pending_asset_with_epoch = copy.deepcopy(base_assets)
    pending_asset_with_epoch[-1]["review_epoch"] = "1"
    mutations.append(
        (
            "pending asset with review epoch",
            base_reading,
            base_candidates,
            base_routes,
            pending_asset_with_epoch,
            base_search,
        )
    )
    anchor_after_review = copy.deepcopy(base_routes)
    anchor_after_review[0]["discovery_epoch"] = "2"
    mutations.append(
        (
            "source anchor postdates source review epoch",
            base_reading,
            base_candidates,
            anchor_after_review,
            base_assets,
            base_search,
        )
    )
    gap_route_epoch = copy.deepcopy(base_routes)
    gap_route_epoch[0]["discovery_epoch"] = "7"
    mutations.append(
        (
            "route opens a gapped global discovery epoch",
            base_reading,
            base_candidates,
            gap_route_epoch,
            base_assets,
            base_search,
        )
    )
    evidence_predates_candidate = copy.deepcopy(base_candidates)
    evidence_predates_candidate[0]["discovery_anchor"]["epoch"] = 2
    evidence_predates_reading = copy.deepcopy(base_reading)
    evidence_predates_reading[0]["review_epoch"] = "2"
    mutations.append(
        (
            "evidence predates candidate discovery epoch",
            evidence_predates_reading,
            evidence_predates_candidate,
            base_routes,
            base_assets,
            base_search,
        )
    )

    missing_reading = copy.deepcopy(base_reading)
    missing_reading.pop()
    mutations.append(
        (
            "missing reading row",
            missing_reading,
            base_candidates,
            base_routes,
            base_assets,
            base_search,
        )
    )
    corrupt_hash = copy.deepcopy(base_reading)
    corrupt_hash[0]["unit_sha256"] = "0" * 64
    mutations.append(
        (
            "stale reading hash",
            corrupt_hash,
            base_candidates,
            base_routes,
            base_assets,
            base_search,
        )
    )
    missing_asset = copy.deepcopy(base_assets)
    missing_asset.pop()
    mutations.append(
        (
            "missing asset row",
            base_reading,
            base_candidates,
            base_routes,
            missing_asset,
            base_search,
        )
    )

    missing_provenance = copy.deepcopy(base_candidates)
    missing_provenance[0]["source_unit_ids"] = []
    mutations.append(
        (
            "candidate provenance reverse join",
            base_reading,
            missing_provenance,
            base_routes,
            base_assets,
            base_search,
        )
    )
    undeclared_field = copy.deepcopy(base_candidates)
    undeclared_field[0]["source_evidence"][0]["fingerprint_fields"].pop()
    mutations.append(
        (
            "fingerprint evidence declaration",
            base_reading,
            undeclared_field,
            base_routes,
            base_assets,
            base_search,
        )
    )
    missing_field_evidence = copy.deepcopy(base_candidates)
    missing_field_evidence[0]["fingerprint"][FINGERPRINT_FIELDS[0]][
        "evidence_ids"
    ] = []
    mutations.append(
        (
            "supported field without evidence",
            base_reading,
            missing_field_evidence,
            base_routes,
            base_assets,
            base_search,
        )
    )
    forbidden_field = copy.deepcopy(base_candidates)
    forbidden_field[0]["catalog_action"] = "ADD_CATALOG_ENTRY"
    mutations.append(
        (
            "forbidden candidate field",
            base_reading,
            forbidden_field,
            base_routes,
            base_assets,
            base_search,
        )
    )
    forbidden_text = copy.deepcopy(base_candidates)
    forbidden_text[0]["source_evidence"][0]["claim"] = "Matches T01."
    mutations.append(
        (
            "forbidden reconciliation free text",
            base_reading,
            forbidden_text,
            base_routes,
            base_assets,
            base_search,
        )
    )
    missing_candidate_backlink = copy.deepcopy(base_reading)
    missing_candidate_backlink[0]["candidate_ids"] = "[]"
    mutations.append(
        (
            "missing reading candidate backlink",
            missing_candidate_backlink,
            base_candidates,
            base_routes,
            base_assets,
            base_search,
        )
    )
    unknown_route_source = copy.deepcopy(base_routes)
    unknown_route_source[0]["source_unit_id"] = "U999999"
    unknown_route_source[0]["discovery_id"] = "U999999"
    mutations.append(
        (
            "route with unknown source",
            base_reading,
            base_candidates,
            unknown_route_source,
            base_assets,
            base_search,
        )
    )
    unresolved_resolved_route = copy.deepcopy(base_routes)
    unresolved_resolved_route[0]["status"] = "RESOLVED"
    mutations.append(
        (
            "resolved route without typed target",
            base_reading,
            base_candidates,
            unresolved_resolved_route,
            base_assets,
            base_search,
        )
    )
    wrong_assignment = copy.deepcopy(base_assets)
    wrong_assignment[0]["assignment_path"] = manifest["documents"][-1]["path"]
    mutations.append(
        (
            "wrong known asset assignment",
            base_reading,
            base_candidates,
            base_routes,
            wrong_assignment,
            base_search,
        )
    )
    risky_asset = copy.deepcopy(base_assets)
    risky_asset[0].update(
        {
            "inspection_status": "SCREENED",
            "review_epoch": "1",
            "visual_role": "CONTROL",
            "source_status": "CLEAR",
            "risk_flags": '["TEXT_BEARING"]',
            "original_resolution_status": "NOT_REQUIRED",
            "transcription_status": "CHECKED",
            "evidence_statement": "Fixture text was screened.",
            "review_stage": risky_asset[0]["assignment_stage"],
            "reviewer": "fixture-reviewer",
        }
    )
    mutations.append(
        (
            "risky asset without original resolution",
            base_reading,
            base_candidates,
            base_routes,
            risky_asset,
            base_search,
        )
    )

    search_reading = copy.deepcopy(base_reading)
    for row in search_reading:
        if row["path"] == path:
            row["review_epoch"] = "2"
    search_assets = copy.deepcopy(base_assets)
    for row in search_assets:
        if row["assignment_path"] == path:
            row["review_epoch"] = "2"
    source_bytes = (
        REPO_ROOT / "ref" / "A-New-Kind-of-Science" / path
    ).read_bytes()
    fixture_pattern = source_bytes[
        unit["byte_start"] : unit["byte_end"]
    ].decode("utf-8")
    search_fixture = {
        "schema_version": 1,
        "phase": "blind_discovery",
        "tool_assumptions": [
            "Deterministic zero-result history fixture.",
            "Literal UTF-8 line search.",
        ],
        "vocabulary": ["fixture"],
        "rounds": [
            copy.deepcopy(epoch1_round),
            {
                "round_id": "S002",
                "epoch": 2,
                "kind": "LOCAL",
                "owning_stage": stage,
                "queries": [
                    {
                        "query_id": "Q0002",
                        "family": "fixture noun",
                        "pattern": fixture_pattern,
                        "mode": "LITERAL",
                        "case_sensitive": True,
                        "whole_word": False,
                        "scope_paths": [path],
                    }
                ],
                "tool_assumptions": ["Literal UTF-8 line search."],
                "result_ids": [],
                "result_digest": "",
                "hits": [],
                "new_vocabulary": [],
                "new_candidates": [],
                "new_evidence_groups": [],
                "new_routes": [],
                "rerun_digest": "",
            }
        ],
        "fixed_point": None,
    }
    active_search_round = search_fixture["rounds"][1]
    fixture_pairs, fixture_query_errors = execute_frozen_queries(
        active_search_round["queries"],
        units,
        REPO_ROOT / "ref" / "A-New-Kind-of-Science",
    )
    failures.extend(fixture_query_errors)
    unit_by_fixture_id = {item["id"]: item for item in units}
    for hit_index, (query_id, hit_unit_id) in enumerate(
        fixture_pairs, start=1
    ):
        hit_id = f"H{hit_index:06d}"
        governed = hit_unit_id == unit_id
        active_search_round["result_ids"].append(hit_id)
        active_search_round["hits"].append(
            {
                "hit_id": hit_id,
                "query_id": query_id,
                "source_unit_id": hit_unit_id,
                "context_sha256": unit_by_fixture_id[hit_unit_id]["sha256"],
                "disposition": (
                    "GOVERNED_CANDIDATE_OR_SUPPORT"
                    if governed
                    else "EXCLUSION"
                ),
                "candidate_ids": ["B0001"] if governed else [],
                "route_ids": [],
                "rationale": (
                    "Already governed by the fixture candidate."
                    if governed
                    else "Duplicate literal outside the fixture anchor."
                ),
            }
        )
    digest = search_result_digest(active_search_round)
    active_search_round["result_digest"] = digest
    active_search_round["rerun_digest"] = digest
    search_history = append_history_event(
        base_history,
        search_reading,
        search_assets,
        path,
        2,
        "REOPEN",
        "fixture-reviewer",
        search_fixture["rounds"][:1],
    )
    search_errors = validate_objects(
        manifest,
        units,
        search_reading,
        base_candidates,
        base_routes,
        search_assets,
        search_fixture,
        search_history,
    )
    if search_errors:
        failures.append(
            "valid local-search mutation fixture failed: " + "; ".join(search_errors)
        )
    else:
        def refresh_round_digest(round_record: dict[str, Any]) -> None:
            round_digest = search_result_digest(round_record)
            round_record["result_digest"] = round_digest
            round_record["rerun_digest"] = round_digest

        def replace_active_query_id(
            search_state: dict[str, Any],
            query_id: str,
        ) -> None:
            active_round = search_state["rounds"][1]
            active_round["queries"][-1]["query_id"] = query_id
            for hit in active_round["hits"]:
                hit["query_id"] = query_id
            refresh_round_digest(active_round)

        impossible_query = copy.deepcopy(epoch1_round["queries"][0])
        impossible_query["family"] = "query-order mutation fixture"

        reversed_query_order = copy.deepcopy(search_fixture)
        reversed_extra = copy.deepcopy(impossible_query)
        reversed_extra["query_id"] = "Q0003"
        reversed_query_order["rounds"][1]["queries"].insert(
            0, reversed_extra
        )
        refresh_round_digest(reversed_query_order["rounds"][1])

        duplicate_query_id = copy.deepcopy(search_fixture)
        replace_active_query_id(duplicate_query_id, "Q0001")

        skipped_query_id = copy.deepcopy(search_fixture)
        replace_active_query_id(skipped_query_id, "Q0003")

        cross_round_query_order = copy.deepcopy(search_fixture)
        cross_round_extra = copy.deepcopy(impossible_query)
        cross_round_extra["query_id"] = "Q0003"
        cross_round_query_order["rounds"][0]["queries"].append(
            cross_round_extra
        )
        refresh_round_digest(cross_round_query_order["rounds"][0])
        cross_round_history = append_history_event(
            base_history,
            search_reading,
            search_assets,
            path,
            2,
            "REOPEN",
            "fixture-reviewer",
            cross_round_query_order["rounds"][:1],
        )

        query_order_mutations = (
            ("reversed query IDs", reversed_query_order, search_history),
            ("duplicate query ID", duplicate_query_id, search_history),
            ("skipped query ID", skipped_query_id, search_history),
            (
                "cross-round query order",
                cross_round_query_order,
                cross_round_history,
            ),
        )
        for mutation_name, search_state, history_state in query_order_mutations:
            order_errors = validate_objects(
                manifest,
                units,
                search_reading,
                base_candidates,
                base_routes,
                search_assets,
                search_state,
                history_state,
            )
            if (
                "search query IDs are not a complete append-only Q sequence"
                not in order_errors
            ):
                failures.append(
                    f"{mutation_name} unexpectedly passed Q-sequence validation"
                )
            replay_or_digest_errors = [
                error
                for error in order_errors
                if (
                    "recorded results differ from independent query execution"
                    in error
                    or "result digest is stale" in error
                    or "rerun did not reproduce" in error
                )
            ]
            if replay_or_digest_errors:
                failures.append(
                    f"{mutation_name} did not preserve replay/digest validity: "
                    + "; ".join(replay_or_digest_errors)
                )

        governed_hit = next(
            hit
            for hit in active_search_round["hits"]
            if hit["source_unit_id"] == unit_id
        )
        local_enriched_reading = copy.deepcopy(search_reading)
        local_enriched_reading[0]["evidence_statement"] = (
            "The original review plus the later LOCAL hit supports this "
            "fixture construction."
        )
        local_enrichment_history = append_history_event(
            search_history,
            local_enriched_reading,
            search_assets,
            path,
            2,
            "SEARCH_ENRICHMENT",
            "fixture-search-enricher",
            search_fixture["rounds"],
            "LOCAL",
            [governed_hit["hit_id"]],
        )
        local_enrichment_errors = validate_objects(
            manifest,
            units,
            local_enriched_reading,
            base_candidates,
            base_routes,
            search_assets,
            search_fixture,
            local_enrichment_history,
        )
        if local_enrichment_errors:
            failures.append(
                "valid post-review LOCAL enrichment fixture failed: "
                + "; ".join(local_enrichment_errors)
            )

        expect_history_failure(
            "silent evidence amendment without enrichment event",
            local_enriched_reading,
            base_candidates,
            base_routes,
            search_assets,
            search_fixture,
            search_history,
        )
        silent_disposition = copy.deepcopy(search_reading)
        silent_disposition[0]["review_disposition"] = "SUPPORTS_CANDIDATE"
        expect_history_failure(
            "silent disposition amendment without enrichment event",
            silent_disposition,
            base_candidates,
            base_routes,
            search_assets,
            search_fixture,
            search_history,
        )
        untriggered_history = append_history_event(
            search_history,
            local_enriched_reading,
            search_assets,
            path,
            2,
            "SEARCH_ENRICHMENT",
            "fixture-search-enricher",
            search_fixture["rounds"],
        )
        expect_history_failure(
            "untriggered search enrichment",
            local_enriched_reading,
            base_candidates,
            base_routes,
            search_assets,
            search_fixture,
            untriggered_history,
        )

        exclusion_hit = next(
            (
                hit
                for hit in active_search_round["hits"]
                if hit["disposition"] == "EXCLUSION"
            ),
            None,
        )
        if exclusion_hit is not None:
            exclusion_reading = copy.deepcopy(search_reading)
            exclusion_index = next(
                index
                for index, row in enumerate(exclusion_reading)
                if row["source_unit_id"] == exclusion_hit["source_unit_id"]
            )
            exclusion_reading[exclusion_index]["evidence_statement"] = (
                "An EXCLUSION result must not authorize this amendment."
            )
            exclusion_history = append_history_event(
                search_history,
                exclusion_reading,
                search_assets,
                path,
                2,
                "SEARCH_ENRICHMENT",
                "fixture-search-enricher",
                search_fixture["rounds"],
                "LOCAL",
                [exclusion_hit["hit_id"]],
            )
            expect_history_failure(
                "EXCLUSION hit authorizes an amendment",
                exclusion_reading,
                base_candidates,
                base_routes,
                search_assets,
                search_fixture,
                exclusion_history,
            )

        previous_snapshot = search_history[-1]["result_snapshot"]
        unrelated_snapshot = copy.deepcopy(
            local_enrichment_history[-1]["result_snapshot"]
        )
        unrelated_snapshot["reading_results"][0][
            "candidate_ids"
        ] = '["B0001","B9999"]'
        unrelated_errors: list[str] = []
        _validate_search_enrichment_diff(
            previous_snapshot,
            unrelated_snapshot,
            {unit_id},
            {unit_id: {"B0001"}},
            {unit_id: set()},
            {"B0001"},
            set(),
            unrelated_errors,
            "unrelated-link fixture",
        )
        if not any("unrelated candidate links" in error for error in unrelated_errors):
            failures.append(
                "unrelated candidate-link enrichment mutation unexpectedly passed"
            )
        unrelated_route_snapshot = copy.deepcopy(
            local_enrichment_history[-1]["result_snapshot"]
        )
        unrelated_route_snapshot["reading_results"][0][
            "route_ids"
        ] = '["R000001","R999999"]'
        unrelated_route_errors: list[str] = []
        _validate_search_enrichment_diff(
            previous_snapshot,
            unrelated_route_snapshot,
            {unit_id},
            {unit_id: {"B0001"}},
            {unit_id: set()},
            {"B0001"},
            set(),
            unrelated_route_errors,
            "unrelated-route fixture",
        )
        if not any(
            "unrelated route links" in error for error in unrelated_route_errors
        ):
            failures.append(
                "unrelated route-link enrichment mutation unexpectedly passed"
            )

        asset_snapshot = defect_asset_history[-1]["result_snapshot"]
        illegal_asset_snapshot = copy.deepcopy(asset_snapshot)
        illegal_asset_snapshot["asset_results"][0]["visual_role"] = "CONTROL"
        illegal_asset_errors: list[str] = []
        _validate_search_enrichment_diff(
            asset_snapshot,
            illegal_asset_snapshot,
            set(),
            {},
            {},
            set(),
            set(),
            illegal_asset_errors,
            "illegal-asset fixture",
        )
        if not any(
            "immutable asset fields" in error for error in illegal_asset_errors
        ):
            failures.append(
                "illegal image-role enrichment mutation unexpectedly passed"
            )
        silent_image_role = copy.deepcopy(defect_asset)
        silent_image_role[defect_asset_index]["visual_role"] = "CONTROL"
        expect_history_failure(
            "silent image-role amendment without enrichment event",
            defect_asset_reading,
            base_candidates,
            base_routes,
            silent_image_role,
            base_search,
            defect_asset_history,
        )

        stale_digest = copy.deepcopy(search_fixture)
        stale_digest["rounds"][1]["result_digest"] = "0" * 64
        mutations.append(
            (
                "stale search digest",
                search_reading,
                base_candidates,
                base_routes,
                base_assets,
                stale_digest,
            )
        )
        stale_context = copy.deepcopy(search_fixture)
        stale_context["rounds"][1]["hits"][0]["context_sha256"] = "0" * 64
        mutations.append(
            (
                "stale search context",
                search_reading,
                base_candidates,
                base_routes,
                base_assets,
                stale_context,
            )
        )
        ungoverned_hit = copy.deepcopy(search_fixture)
        ungoverned_hit["rounds"][1]["hits"][0]["candidate_ids"] = []
        updated_digest = search_result_digest(ungoverned_hit["rounds"][1])
        ungoverned_hit["rounds"][1]["result_digest"] = updated_digest
        ungoverned_hit["rounds"][1]["rerun_digest"] = updated_digest
        mutations.append(
            (
                "governed hit without candidate",
                search_reading,
                base_candidates,
                base_routes,
                base_assets,
                ungoverned_hit,
            )
        )
        fake_group = copy.deepcopy(search_fixture)
        fake_group["rounds"][1]["new_evidence_groups"] = ["G999999"]
        mutations.append(
            (
                "search delta with fake evidence group",
                search_reading,
                base_candidates,
                base_routes,
                base_assets,
                fake_group,
            )
        )
        gap_search_epoch = copy.deepcopy(search_fixture)
        gap_search_epoch["rounds"][1]["epoch"] = 7
        gap_digest = search_result_digest(gap_search_epoch["rounds"][1])
        gap_search_epoch["rounds"][1]["result_digest"] = gap_digest
        gap_search_epoch["rounds"][1]["rerun_digest"] = gap_digest
        mutations.append(
            (
                "search round opens a gapped global discovery epoch",
                search_reading,
                base_candidates,
                base_routes,
                base_assets,
                gap_search_epoch,
            )
        )

    cross_stage_errors = validate_objects(
        manifest,
        units,
        base_reading,
        base_candidates,
        base_routes,
        base_assets,
        base_search,
        base_history,
        {stage},
    )
    if any("pending within-stage routes" in error for error in cross_stage_errors):
        failures.append("cross-range pending route incorrectly blocks stage closure")
    within_routes = copy.deepcopy(base_routes)
    within_routes[0]["closure_scope"] = "WITHIN_STAGE"
    within_stage_errors = validate_objects(
        manifest,
        units,
        base_reading,
        base_candidates,
        within_routes,
        base_assets,
        base_search,
        base_history,
        {stage},
    )
    if not any("pending within-stage routes" in error for error in within_stage_errors):
        failures.append("pending within-stage route did not block stage closure")

    for (
        name,
        changed_reading,
        changed_candidates,
        changed_routes,
        changed_assets,
        changed_search,
    ) in mutations:
        if not validate_objects(
            manifest,
            units,
            changed_reading,
            changed_candidates,
            changed_routes,
            changed_assets,
            changed_search,
            base_history,
        ):
            failures.append(f"mutation unexpectedly passed: {name}")
    return failures


def validate_schema_files(goal_dir: Path) -> list[str]:
    errors: list[str] = []
    expected = schema_documents()
    for relative, schema in expected.items():
        path = goal_dir / "schemas" / relative
        if not path.is_file():
            errors.append(f"missing schema: {relative}")
        elif path.read_bytes() != canonical_json_bytes(schema):
            errors.append(f"stale schema: {relative}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--goal-dir", type=Path, default=GOAL_DIR)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--require-stage", type=int, action="append", default=[])
    parser.add_argument("--require-all-reviewed", action="store_true")
    args = parser.parse_args()

    goal_dir = args.goal_dir.resolve()
    repo_root = args.repo_root.resolve()
    try:
        manifest = json.loads(
            (goal_dir / "corpus-manifest.json").read_text(encoding="utf-8")
        )
        units_bytes = (goal_dir / "source-units.jsonl").read_bytes()
        units = verify_corpus.load_units(goal_dir / "source-units.jsonl")
        reading = load_csv(goal_dir / "reading-ledger.csv", READING_HEADER)
        candidates = load_jsonl(goal_dir / "candidate-ledger.jsonl")
        routes = load_csv(
            goal_dir / "cross-reference-ledger.csv",
            CROSS_REFERENCE_HEADER,
        )
        assets = load_csv(goal_dir / "asset-ledger.csv", ASSET_HEADER)
        review_history = load_jsonl(goal_dir / "review-history.jsonl")
        search = json.loads(
            (goal_dir / "search-rounds.json").read_text(encoding="utf-8")
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"audit artifact load failed: {exc}", file=sys.stderr)
        return 1

    errors = verify_corpus.verify_loaded(manifest, units, repo_root, units_bytes)
    errors.extend(validate_schema_files(goal_dir))
    errors.extend(
        validate_objects(
            manifest,
            units,
            reading,
            candidates,
            routes,
            assets,
            search,
            review_history,
            set(args.require_stage),
            args.require_all_reviewed,
            repo_root,
        )
    )
    if (goal_dir / "classification-ledger.csv").exists() or (
        goal_dir / "coverage-matrix.csv"
    ).exists():
        errors.append("reconciliation data files exist before Stage 19")
    if args.self_test:
        errors.extend(
            mutation_checks(
                manifest,
                units,
                reading,
                candidates,
                routes,
                assets,
                search,
                review_history,
            )
        )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    reviewed = sum(row["review_status"] == "REVIEWED" for row in reading)
    screened = sum(row["inspection_status"] == "SCREENED" for row in assets)
    print(
        "validated blind audit harness"
        + (" and mutation checks" if args.self_test else "")
        + f": units={len(units)} reviewed={reviewed} "
        + f"candidates={len(candidates)} routes={len(routes)} "
        + f"assets={len(assets)} screened={screened} "
        + f"rounds={len(search['rounds'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
