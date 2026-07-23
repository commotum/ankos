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
    CROSS_REFERENCE_HEADER,
    EVIDENCE_MODALITIES,
    EVIDENCE_STRENGTHS,
    FIELD_SUPPORT_STATUSES,
    FINGERPRINT_FIELDS,
    FORBIDDEN_BLIND_FIELDS,
    GOAL_DIR,
    READING_DISPOSITIONS,
    READING_HEADER,
    REPO_ROOT,
    ROUTE_CLOSURE_SCOPES,
    ROUTE_KINDS,
    ROUTE_STATUSES,
    SEARCH_HIT_DISPOSITIONS,
    SECONDARY_ROLES,
    SOURCE_STATUSES,
    VISUAL_RISK_FLAGS,
    VISUAL_ROLES,
    canonical_json_bytes,
    schema_documents,
)


MANIFEST_PATH = GOAL_DIR / "corpus-manifest.json"
UNITS_PATH = GOAL_DIR / "source-units.jsonl"
READING_PATH = GOAL_DIR / "reading-ledger.csv"
CANDIDATE_PATH = GOAL_DIR / "candidate-ledger.jsonl"
CROSS_REFERENCE_PATH = GOAL_DIR / "cross-reference-ledger.csv"
ASSET_PATH = GOAL_DIR / "asset-ledger.csv"
SEARCH_PATH = GOAL_DIR / "search-rounds.json"
SCHEMA_DIR = GOAL_DIR / "schemas"

HEX64 = re.compile(r"^[0-9a-f]{64}$")
B_ID = re.compile(r"^B[0-9]{4}$")
E_ID = re.compile(r"^E[0-9]{6}$")
G_ID = re.compile(r"^G[0-9]{6}$")
Q_ID = re.compile(r"^Q[0-9]{4}$")
H_ID = re.compile(r"^H[0-9]{6}$")
PAGE_NUMBER = re.compile(r"_page_(\d+)")


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
            "evidence_ids",
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
        elif not isinstance(relation["uncertainty"], str) or not relation[
            "uncertainty"
        ].strip():
            errors.append(f"{prefix} provisional relation lacks uncertainty")

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


def validate_objects(
    manifest: dict[str, Any],
    units: list[dict[str, Any]],
    reading: list[dict[str, str]],
    candidates: list[dict[str, Any]],
    routes: list[dict[str, str]],
    assets: list[dict[str, str]],
    search: dict[str, Any],
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
                    "review_disposition",
                    "source_status",
                    "evidence_statement",
                    "review_stage",
                    "reviewer",
                )
            ) or secondary or linked_candidates or linked_routes:
                errors.append(f"{prefix} pending row contains review result")
        elif status == "REVIEWED":
            reviewed_count += 1
            if row.get("review_disposition") not in READING_DISPOSITIONS:
                errors.append(f"{prefix} has invalid review disposition")
            if row.get("source_status") not in SOURCE_STATUSES:
                errors.append(f"{prefix} has invalid source status")
            if row.get("source_status") in {
                "AMBIGUOUS",
                "DEFECTIVE",
                "CONFLICTING",
            } and not row.get("uncertainty", "").strip():
                errors.append(f"{prefix} non-clear source lacks uncertainty boundary")
            if (
                row.get("visual_role") == "SOURCE_DEFECT"
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
            source_reading = reading_by_unit.get(row["source_unit_id"])
            if (
                source_reading is None
                or source_reading["review_status"] != "REVIEWED"
            ):
                errors.append(f"{prefix} source unit is not reviewed")
        if source_asset is not None:
            source_path = source_asset["physical_path"]
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
    expected_evidence_ids = {
        f"E{index:06d}"
        for index in range(1, len(evidence_ids_global) + 1)
    }
    if evidence_ids_global != expected_evidence_ids:
        errors.append("evidence IDs are not a complete append-only E sequence")

    candidate_by_id = {candidate["id"]: candidate for candidate in candidates}
    evidence_by_group: dict[str, list[tuple[str, dict[str, Any]]]] = {}
    for candidate in candidates:
        for evidence in candidate.get("source_evidence", []):
            if isinstance(evidence, dict):
                evidence_by_group.setdefault(
                    str(evidence.get("evidence_group_id", "")), []
                ).append((candidate["id"], evidence))
    evidence_group_ids = set(evidence_by_group)
    expected_group_ids = {
        f"G{index:06d}"
        for index in range(1, len(evidence_group_ids) + 1)
    }
    if evidence_group_ids != expected_group_ids:
        errors.append(
            "evidence-group IDs are not a complete append-only G sequence"
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
                or row.get("source_status")
                or risk_flags
                or row.get("evidence_statement")
                or row.get("review_stage")
                or row.get("reviewer")
                or linked_candidates
                or linked_routes
                or row.get("original_resolution_status") != "NOT_REVIEWED"
                or row.get("transcription_status") != "NOT_APPLICABLE"
            ):
                errors.append(f"{prefix} pending row contains inspection result")
        elif status == "SCREENED":
            screened_count += 1
            if row.get("visual_role") not in VISUAL_ROLES:
                errors.append(f"{prefix} has invalid visual role")
            if row.get("source_status") not in SOURCE_STATUSES:
                errors.append(f"{prefix} has invalid source status")
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
            expected_query_fields = {
                "query_id",
                "family",
                "pattern",
                "mode",
                "case_sensitive",
                "whole_word",
                "scope_paths",
            }
            if not isinstance(query, dict) or set(query) != expected_query_fields:
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

    if seen_queries != {
        f"Q{index:04d}" for index in range(1, len(seen_queries) + 1)
    }:
        errors.append("search query IDs are not a complete append-only Q sequence")

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
    candidate_epochs: set[int] = set()
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
        candidate_epochs.add(epoch)
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
    if candidate_epochs and candidate_epochs != set(
        range(1, max(candidate_epochs) + 1)
    ):
        errors.append("candidate discovery epochs are not contiguous from 1")
    for anchor_identity, ordinals in anchor_ordinals.items():
        if sorted(ordinals) != list(range(1, len(ordinals) + 1)):
            errors.append(
                f"candidate anchor {anchor_identity} ordinals are not contiguous"
            )

    evidence_anchor_ordinals: dict[tuple[int, str, str], list[int]] = {}
    search_evidence_groups: set[str] = set()
    for candidate in candidates:
        candidate_id = candidate["id"]
        for evidence in candidate["source_evidence"]:
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
                or not isinstance(ordinal, int)
                or ordinal < 1
            ):
                continue
            evidence_anchor_ordinals.setdefault(
                (epoch, kind, anchor_id), []
            ).append(ordinal)
            if kind == "SEARCH_HIT":
                search_evidence_groups.add(evidence["evidence_group_id"])
                hit = hit_by_id.get(anchor_id)
                meta = hit_round_meta.get(anchor_id)
                if hit is None or meta is None:
                    errors.append(
                        f"candidate {candidate_id} evidence anchor hit is unknown"
                    )
                else:
                    hit_epoch, _, _ = meta
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
            elif kind == "SOURCE_UNIT" and anchor_id not in unit_by_id:
                errors.append(
                    f"candidate {candidate_id} evidence anchor unit is unknown"
                )
            elif kind == "IMAGE" and anchor_id not in image_by_path:
                errors.append(
                    f"candidate {candidate_id} evidence anchor image is unknown"
                )
    for anchor_identity, ordinals in evidence_anchor_ordinals.items():
        if sorted(ordinals) != list(range(1, len(ordinals) + 1)):
            errors.append(
                f"evidence anchor {anchor_identity} ordinals are not contiguous"
            )
    if search_evidence_groups != seen_new_evidence_groups:
        errors.append(
            "search-discovered evidence groups differ from search-round deltas"
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
        local_rounds = [
            round_record
            for round_record in rounds
            if isinstance(round_record, dict)
            and round_record.get("kind") == "LOCAL"
            and round_record.get("owning_stage") == required_stage
        ]
        local_scope = {
            path
            for round_record in local_rounds
            for query in round_record.get("queries", [])
            if isinstance(query, dict)
            for path in query.get("scope_paths", [])
        }
        if not local_rounds or local_scope != assigned_paths:
            errors.append(
                f"stage {required_stage} lacks full-scope local-search evidence"
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
    )
    if base_errors:
        return ["valid candidate/route mutation fixture failed: " + "; ".join(base_errors)]

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
                    "evidence_ids": ["E000001"],
                    "uncertainty": "",
                },
                {
                    "candidate_id": "B0004",
                    "relation": "SPLIT_INTO",
                    "evidence_ids": ["E000001"],
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
    lineage_candidates[1].update(
        {
            "record_status": "MERGED_REDIRECT",
            "related_candidate_ids": [
                {
                    "candidate_id": "B0001",
                    "relation": "MERGED_INTO",
                    "evidence_ids": ["E000002"],
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
    lineage_reading[0]["candidate_ids"] = '["B0003","B0004"]'
    lineage_errors = validate_objects(
        manifest,
        units,
        lineage_reading,
        lineage_candidates,
        base_routes,
        base_assets,
        base_search,
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
        if row["path"] != path or row["review_status"] == "REVIEWED":
            continue
        row.update(
            {
                "review_status": "REVIEWED",
                "review_disposition": "NO_CONSTRUCTION",
                "source_status": "CLEAR",
                "secondary_roles": "[]",
                "candidate_ids": "[]",
                "route_ids": "[]",
                "evidence_statement": "No construction in this fixture unit.",
                "review_stage": str(stage),
                "reviewer": "fixture-reviewer",
            }
        )
    source_bytes = (
        REPO_ROOT / "ref" / "A-New-Kind-of-Science" / path
    ).read_bytes()
    fixture_pattern = source_bytes[
        unit["byte_start"] : unit["byte_end"]
    ].decode("utf-8")
    search_fixture = {
        "schema_version": 1,
        "phase": "blind_discovery",
        "tool_assumptions": ["Literal UTF-8 line search."],
        "vocabulary": ["fixture"],
        "rounds": [
            {
                "round_id": "S001",
                "epoch": 1,
                "kind": "LOCAL",
                "owning_stage": stage,
                "queries": [
                    {
                        "query_id": "Q0001",
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
    fixture_pairs, fixture_query_errors = execute_frozen_queries(
        search_fixture["rounds"][0]["queries"],
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
        search_fixture["rounds"][0]["result_ids"].append(hit_id)
        search_fixture["rounds"][0]["hits"].append(
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
    digest = search_result_digest(search_fixture["rounds"][0])
    search_fixture["rounds"][0]["result_digest"] = digest
    search_fixture["rounds"][0]["rerun_digest"] = digest
    search_errors = validate_objects(
        manifest,
        units,
        search_reading,
        base_candidates,
        base_routes,
        base_assets,
        search_fixture,
    )
    if search_errors:
        failures.append(
            "valid local-search mutation fixture failed: " + "; ".join(search_errors)
        )
    else:
        stale_digest = copy.deepcopy(search_fixture)
        stale_digest["rounds"][0]["result_digest"] = "0" * 64
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
        stale_context["rounds"][0]["hits"][0]["context_sha256"] = "0" * 64
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
        ungoverned_hit["rounds"][0]["hits"][0]["candidate_ids"] = []
        updated_digest = search_result_digest(ungoverned_hit["rounds"][0])
        ungoverned_hit["rounds"][0]["result_digest"] = updated_digest
        ungoverned_hit["rounds"][0]["rerun_digest"] = updated_digest
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
        fake_group["rounds"][0]["new_evidence_groups"] = ["G999999"]
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

    cross_stage_errors = validate_objects(
        manifest,
        units,
        base_reading,
        base_candidates,
        base_routes,
        base_assets,
        base_search,
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
