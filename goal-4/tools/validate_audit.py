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
        if not isinstance(evidence_id, str) or not evidence_id:
            errors.append(f"{prefix} evidence ID is invalid")
        elif evidence_id in local_evidence_ids or evidence_id in evidence_ids_global:
            errors.append(f"{prefix} evidence ID is not unique: {evidence_id}")
        else:
            local_evidence_ids.add(evidence_id)
            evidence_ids_global.add(evidence_id)
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
) -> list[str]:
    errors: list[str] = []
    require_stages = require_stages or set()
    unit_by_id = {unit["id"]: unit for unit in units}
    unit_ids = set(unit_by_id)
    document_by_path = {doc["path"]: doc for doc in manifest["documents"]}
    image_by_path = {image["path"]: image for image in manifest["images"]}
    image_paths = set(image_by_path)
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
        if source_unit is None:
            errors.append(f"{prefix} has unknown source unit")
        if row["route_kind"] not in ROUTE_KINDS:
            errors.append(f"{prefix} has invalid kind")
        try:
            discovery_epoch = int(row["discovery_epoch"])
        except ValueError:
            discovery_epoch = -1
        if discovery_epoch < 1:
            errors.append(f"{prefix} has invalid discovery epoch")
        if row["discovery_kind"] not in {"SOURCE_UNIT", "SEARCH_HIT"}:
            errors.append(f"{prefix} has invalid discovery kind")
        if (
            row["discovery_kind"] == "SOURCE_UNIT"
            and row["discovery_id"] != row["source_unit_id"]
        ):
            errors.append(f"{prefix} source discovery anchor is inconsistent")
        if row["discovery_kind"] == "SEARCH_HIT" and not H_ID.fullmatch(
            row["discovery_id"]
        ):
            errors.append(f"{prefix} has invalid search-hit discovery anchor")
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

    candidate_by_id = {candidate["id"]: candidate for candidate in candidates}
    split_children: set[str] = set()
    for candidate in candidates:
        source_number = int(candidate["id"][1:]) if B_ID.fullmatch(candidate["id"]) else -1
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
            if target["record_status"] != "ACTIVE":
                errors.append(
                    f"candidate {candidate['id']} supersession target "
                    f"{target_id} is not ACTIVE"
                )
            target_number = (
                int(target_id[1:]) if isinstance(target_id, str) and B_ID.fullmatch(target_id) else -1
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
            if (
                route is not None
                and route["source_unit_id"] not in candidate["source_unit_ids"]
            ):
                errors.append(
                    f"candidate {candidate_id} cross-reference source is absent "
                    "from candidate provenance"
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
        risk_flags = parsed_string_list(
            row.get("risk_flags", ""), f"{prefix}.risk_flags", errors
        )
        if any(value not in candidate_ids for value in linked_candidates):
            errors.append(f"{prefix} links unknown candidate")
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
                "flags",
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
            exact_string_list(
                query["flags"], f"search query {query_id}.flags", errors
            )
            scope_paths = exact_string_list(
                query["scope_paths"],
                f"search query {query_id}.scope_paths",
                errors,
                nonempty=True,
            )
            if any(path not in document_by_path for path in scope_paths):
                errors.append(f"search query {query_id} has unknown scope path")
            if any(
                reading_row["review_status"] != "REVIEWED"
                for reading_row in reading
                if reading_row["path"] in scope_paths
            ):
                errors.append(
                    f"search query {query_id} scopes an unreviewed document"
                )
            current_query_scopes[query_id] = set(scope_paths)

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
            hit_ids.append(hit_id)
            if hit["query_id"] not in current_query_ids:
                errors.append(
                    f"search hit {hit_id} references a query outside its round"
                )
            pair = (hit["query_id"], hit["source_unit_id"])
            if pair in result_pairs:
                errors.append(f"search hit {hit_id} duplicates query/unit result")
            result_pairs.add(pair)
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
            if not isinstance(hit["rationale"], str) or not hit[
                "rationale"
            ].strip():
                errors.append(f"search hit {hit_id} lacks rationale")

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

    stage18_candidates = [
        candidate["id"]
        for candidate in candidates
        if candidate["discovery_stage"] == 18
    ]
    if stage18_candidates != ordered_stage18_candidates:
        errors.append(
            "Stage 18 candidate sequence differs from search-round discovery order"
        )
    stage18_routes = [
        route["route_id"] for route in routes if route["owning_stage"] == "18"
    ]
    if stage18_routes != ordered_stage18_routes:
        errors.append("Stage 18 route sequence differs from search-round discovery order")

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

    unit_position = {
        unit["id"]: position for position, unit in enumerate(units, start=1)
    }
    image_position = {
        image["path"]: position
        for position, image in enumerate(manifest["images"], start=1)
    }
    anchor_ordinals: dict[tuple[str, str], list[int]] = {}
    prior_anchor_key: tuple[int, int, int, int, int] | None = None
    for candidate in candidates:
        candidate_id = candidate["id"]
        anchor = candidate["discovery_anchor"]
        if not isinstance(anchor, dict) or not {
            "kind",
            "id",
            "ordinal",
        }.issubset(anchor):
            continue
        kind = anchor["kind"]
        anchor_id = anchor["id"]
        ordinal = anchor["ordinal"]
        if (
            kind not in {"SOURCE_UNIT", "IMAGE", "SEARCH_HIT"}
            or not isinstance(anchor_id, str)
            or not isinstance(ordinal, int)
            or ordinal < 1
        ):
            continue
        anchor_stage = -1
        anchor_key: tuple[int, int, int, int, int] | None = None
        if kind == "SOURCE_UNIT":
            source_unit = unit_by_id.get(anchor_id)
            if source_unit is None:
                errors.append(f"candidate {candidate_id} anchor unit is unknown")
            else:
                anchor_stage = stage_by_path[source_unit["path"]]
                anchor_key = (
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
            anchor_stage = 18
            hit = hit_by_id.get(anchor_id)
            if hit is None:
                errors.append(f"candidate {candidate_id} anchor hit is unknown")
            else:
                anchor_key = (
                    18,
                    0,
                    0,
                    int(anchor_id[1:]),
                    ordinal,
                )
                if candidate_id not in hit["candidate_ids"]:
                    errors.append(
                        f"candidate {candidate_id} anchor hit lacks candidate link"
                    )
        if anchor_stage != candidate["discovery_stage"]:
            errors.append(
                f"candidate {candidate_id} discovery stage differs from anchor stage"
            )
        if candidate["discovery_stage"] == 18 and kind != "SEARCH_HIT":
            errors.append(
                f"candidate {candidate_id} Stage 18 discovery lacks search-hit anchor"
            )
        if candidate["discovery_stage"] < 18 and kind == "SEARCH_HIT":
            errors.append(
                f"candidate {candidate_id} pre-saturation discovery uses search hit"
            )
        anchor_ordinals.setdefault((kind, anchor_id), []).append(ordinal)
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
        if any(
            route["status"] == "PENDING"
            for route in routes
            if route["owning_stage"] == str(required_stage)
        ):
            errors.append(f"stage {required_stage} has pending owned routes")

    if require_all_reviewed:
        if any(route["status"] == "PENDING" for route in routes):
            errors.append("all-reviewed closure has pending routes")
        if fixed_point is None:
            errors.append("all-reviewed closure lacks search fixed point")

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

    missing_reading = copy.deepcopy(reading)
    missing_reading.pop()
    mutations.append(
        ("missing reading row", missing_reading, candidates, routes, assets, search)
    )

    corrupt_hash = copy.deepcopy(reading)
    corrupt_hash[0]["unit_sha256"] = "0" * 64
    mutations.append(
        ("stale reading hash", corrupt_hash, candidates, routes, assets, search)
    )

    missing_asset = copy.deepcopy(assets)
    missing_asset.pop()
    mutations.append(
        ("missing asset row", reading, candidates, routes, missing_asset, search)
    )

    bad_route = copy.deepcopy(routes)
    bad_route.append(
        {
            key: value
            for key, value in zip(
                CROSS_REFERENCE_HEADER,
                [
                    "R000001",
                    "U999999",
                    "page 1",
                    "PAGE",
                    "unknown",
                    "4",
                    "PENDING",
                    "[]",
                    "[]",
                    "[]",
                    "",
                ],
            )
        }
    )
    mutations.append(
        ("route with unknown source", reading, candidates, bad_route, assets, search)
    )

    leaked_candidate = {
        key: [] for key in CANDIDATE_FIELDS
    }
    leaked_candidate.update(
        {
            "id": "B0001",
            "record_status": "ACTIVE",
            "provisional_name": "mutation",
            "discovery_stage": 4,
            "source_unit_ids": ["U000001"],
            "source_evidence": [],
            "source_status": ["CLEAR"],
            "evidence_strength": ["DIRECT_IDENTITY"],
            "field_support": {
                field: "UNKNOWN_FROM_SOURCE" for field in FINGERPRINT_FIELDS
            },
            "fingerprint": {
                field: {
                    "status": "UNKNOWN_FROM_SOURCE",
                    "value": None,
                    "evidence_ids": [],
                    "reason": "mutation",
                }
                for field in FINGERPRINT_FIELDS
            },
            "catalog_action": "ADD_CATALOG_ENTRY",
        }
    )
    mutations.append(
        (
            "forbidden candidate field",
            reading,
            [leaked_candidate],
            routes,
            assets,
            search,
        )
    )

    bad_search = copy.deepcopy(search)
    bad_search["rounds"] = [
        {
            "round_id": "S001",
            "queries": [],
            "tool_assumptions": [],
            "result_ids": ["H000001"],
            "result_digest": "0" * 64,
            "hits": [
                {
                    "hit_id": "H000001",
                    "query_id": "Q001",
                    "source_unit_id": "U000001",
                    "context_sha256": "0" * 64,
                    "disposition": "",
                    "candidate_ids": [],
                    "route_ids": [],
                    "rationale": "",
                }
            ],
            "new_vocabulary": [],
            "new_candidates": [],
            "new_evidence_groups": [],
            "new_routes": [],
            "rerun_digest": "0" * 64,
        }
    ]
    mutations.append(
        (
            "undispositioned search hit",
            reading,
            candidates,
            routes,
            assets,
            bad_search,
        )
    )

    for name, changed_reading, changed_candidates, changed_routes, changed_assets, changed_search in mutations:
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
