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

    source_units = exact_string_list(
        row["source_unit_ids"],
        f"{prefix}.source_unit_ids",
        errors,
        nonempty=True,
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
        if image_path is not None and image_path not in image_paths:
            errors.append(f"{prefix} evidence references unknown image")
        if image_path is not None and image_path not in image_witnesses:
            errors.append(
                f"{prefix} evidence image is absent from image_witnesses"
            )
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
            if value["value"] is not None or field_evidence_ids:
                errors.append(
                    f"{prefix}.{field} not-applicable value carries value/evidence"
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
        if row["status"] not in ROUTE_STATUSES:
            errors.append(f"{prefix} has invalid status")
        targets = parsed_string_list(
            row["target_unit_ids"], f"{prefix}.target_unit_ids", errors
        )
        attempts = parsed_string_list(
            row["attempts"], f"{prefix}.attempts", errors
        )
        parsed_string_list(
            row["vocabulary_terms"], f"{prefix}.vocabulary_terms", errors
        )
        if any(value not in unit_ids for value in targets):
            errors.append(f"{prefix} targets unknown source unit")
        if not row["literal_target"].strip() or not row["expected_topic"].strip():
            errors.append(f"{prefix} lacks target/topic")
        try:
            owning_stage = int(row["owning_stage"])
        except ValueError:
            owning_stage = -1
        if source_unit is not None:
            expected_stage = stage_by_path[source_unit["path"]]
            if owning_stage != expected_stage:
                errors.append(
                    f"{prefix} owning stage differs from source-unit stage"
                )
            source_reading = reading_by_unit.get(row["source_unit_id"])
            if (
                source_reading is None
                or source_reading["review_status"] != "REVIEWED"
            ):
                errors.append(f"{prefix} source unit is not reviewed")
        defect = row["defect_boundary"].strip()
        if row["status"] == "PENDING":
            if targets or defect:
                errors.append(f"{prefix} pending route has final disposition data")
        elif row["status"] == "RESOLVED":
            if not targets or defect:
                errors.append(
                    f"{prefix} resolved route lacks targets or claims a defect"
                )
        elif row["status"] == "MISSING_TARGET_FINAL":
            if targets or not attempts or not defect:
                errors.append(
                    f"{prefix} final missing route needs attempts/defect and no target"
                )

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

    candidate_source_links: dict[str, set[str]] = {
        unit_id: set() for unit_id in unit_ids
    }
    for candidate in candidates:
        candidate_id = candidate["id"]
        for source_unit_id in candidate["source_unit_ids"]:
            if source_unit_id in candidate_source_links:
                candidate_source_links[source_unit_id].add(candidate_id)
        linked_rows = [
            reading_by_unit[source_unit_id]
            for source_unit_id in candidate["source_unit_ids"]
            if source_unit_id in reading_by_unit
        ]
        if not linked_rows:
            errors.append(f"candidate {candidate_id} has no reading-ledger join")
            continue
        if any(row["review_status"] != "REVIEWED" for row in linked_rows):
            errors.append(f"candidate {candidate_id} links an unreviewed source unit")
        expected_statuses = {row["source_status"] for row in linked_rows}
        if set(candidate["source_status"]) != expected_statuses:
            errors.append(
                f"candidate {candidate_id} source_status is not the exact "
                "reading-ledger aggregate"
            )
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
            if linked_candidates and row.get("visual_role") != "NATIVE_EVIDENCE":
                errors.append(
                    f"{prefix} candidate witness is not classified NATIVE_EVIDENCE"
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
    for row in assets:
        for candidate_id in parse_array(
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
        if asset_candidate_links.get(candidate_id, set()) != witnesses:
            errors.append(
                f"candidate {candidate_id} image witnesses lack exact asset reverse joins"
            )

    if require_all_reviewed and screened_count != len(assets):
        errors.append("not every physical image is screened")

    if set(search) != {
        "schema_version",
        "phase",
        "tool_assumptions",
        "vocabulary",
        "rounds",
        "fixed_point",
    }:
        errors.append("search-rounds fields do not match blind allowlist")
    if forbidden_keys(search):
        errors.append("search-rounds contains forbidden blind field")
    if search.get("schema_version") != 1 or search.get("phase") != "blind_discovery":
        errors.append("search-rounds schema/phase is invalid")
    if not isinstance(search.get("tool_assumptions"), list) or not isinstance(
        search.get("vocabulary"), list
    ) or not isinstance(search.get("rounds"), list):
        errors.append("search-rounds list fields are invalid")
    seen_hits: set[str] = set()
    for round_index, round_record in enumerate(search.get("rounds", []), start=1):
        required = {
            "round_id",
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
        if not HEX64.fullmatch(str(round_record["result_digest"])) or not HEX64.fullmatch(
            str(round_record["rerun_digest"])
        ):
            errors.append(f"search round {round_index} digest is invalid")
        hit_ids: list[str] = []
        for hit in round_record["hits"]:
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
            if hit_id in seen_hits:
                errors.append(f"duplicate search hit ID: {hit_id}")
            seen_hits.add(hit_id)
            hit_ids.append(hit_id)
            if hit["source_unit_id"] not in unit_ids:
                errors.append(f"search hit {hit_id} has unknown source unit")
            if hit["disposition"] not in SEARCH_HIT_DISPOSITIONS:
                errors.append(f"search hit {hit_id} lacks final blind disposition")
            if any(value not in candidate_ids for value in hit["candidate_ids"]):
                errors.append(f"search hit {hit_id} links unknown candidate")
            if any(value not in route_ids for value in hit["route_ids"]):
                errors.append(f"search hit {hit_id} links unknown route")
            if not hit["rationale"].strip():
                errors.append(f"search hit {hit_id} lacks rationale")
        if round_record["result_ids"] != hit_ids:
            errors.append(f"search round {round_index} result IDs differ from hits")

    for required_stage in require_stages:
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
