#!/usr/bin/env python3
"""Validate Goal 4 blind-audit ledgers, joins, queues, and phase barriers."""

from __future__ import annotations

import argparse
import copy
import csv
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

    source_units = row["source_unit_ids"]
    if not isinstance(source_units, list) or not source_units:
        errors.append(f"{prefix} requires source_unit_ids")
        source_units = []
    if any(unit not in unit_ids for unit in source_units):
        errors.append(f"{prefix} references unknown source unit")
    if len(source_units) != len(set(source_units)):
        errors.append(f"{prefix} repeats source units")

    for key in (
        "aliases",
        "source_status",
        "image_witnesses",
        "evidence_strength",
        "parameters",
        "variants",
        "missing_mechanics",
        "uncertainties",
        "related_candidate_ids",
        "cross_reference_ids",
    ):
        if not isinstance(row[key], list):
            errors.append(f"{prefix}.{key} must be an array")

    if any(value not in SOURCE_STATUSES for value in row["source_status"]):
        errors.append(f"{prefix} has invalid source_status")
    if any(value not in image_paths for value in row["image_witnesses"]):
        errors.append(f"{prefix} references unknown image")
    if any(value not in EVIDENCE_STRENGTHS for value in row["evidence_strength"]):
        errors.append(f"{prefix} has invalid evidence strength")
    if any(value not in route_ids for value in row["cross_reference_ids"]):
        errors.append(f"{prefix} references unknown route")

    evidence = row["source_evidence"]
    if not isinstance(evidence, list) or not evidence:
        errors.append(f"{prefix} requires source_evidence")
        evidence = []
    local_evidence_ids: set[str] = set()
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
        if item["source_unit_id"] is not None and item["source_unit_id"] not in unit_ids:
            errors.append(f"{prefix} evidence references unknown unit")
        if item["image_path"] is not None and item["image_path"] not in image_paths:
            errors.append(f"{prefix} evidence references unknown image")
        if item["source_unit_id"] is None and item["image_path"] is None:
            errors.append(f"{prefix} evidence has no canonical witness")
        if item["strength"] not in EVIDENCE_STRENGTHS:
            errors.append(f"{prefix} evidence strength is invalid")
        if item["modality"] not in EVIDENCE_MODALITIES:
            errors.append(f"{prefix} evidence modality is invalid")
        if not isinstance(item["claim"], str) or not item["claim"].strip():
            errors.append(f"{prefix} evidence claim is empty")
        fields = item["fingerprint_fields"]
        if not isinstance(fields, list) or any(
            field not in FINGERPRINT_FIELDS for field in fields
        ):
            errors.append(f"{prefix} evidence fingerprint fields are invalid")

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
        if not isinstance(value["evidence_ids"], list) or any(
            evidence_id not in local_evidence_ids
            for evidence_id in value["evidence_ids"]
        ):
            errors.append(f"{prefix}.{field} has invalid evidence IDs")
        if support == "SUPPORTED":
            if value["value"] in (None, "") or not value["evidence_ids"]:
                errors.append(f"{prefix}.{field} supported value lacks evidence")
        elif not isinstance(value["reason"], str) or not value["reason"].strip():
            errors.append(f"{prefix}.{field} non-supported value lacks reason")

    for relation in row["related_candidate_ids"]:
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
        if relation["relation"] not in {
            "POSSIBLY_SAME_AS",
            "POSSIBLE_VARIANT_OF",
            "SOURCE_COMPARE",
        }:
            errors.append(f"{prefix} has invalid blind candidate relation")
        if any(item not in local_evidence_ids for item in relation["evidence_ids"]):
            errors.append(f"{prefix} relation has invalid evidence ID")


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
    link_by_id = {link["id"]: link for link in manifest["links"]}

    route_ids = {row.get("route_id", "") for row in routes}
    candidate_ids = {str(row.get("id", "")) for row in candidates}

    if len(reading) != len(units):
        errors.append("reading ledger row count differs from source units")
    if [row.get("source_unit_id") for row in reading] != [
        unit["id"] for unit in units
    ]:
        errors.append("reading ledger unit order/set differs from source units")

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
        secondary = parse_array(row.get("secondary_roles", ""), f"{prefix}.secondary_roles", errors)
        linked_candidates = parse_array(row.get("candidate_ids", ""), f"{prefix}.candidate_ids", errors)
        linked_routes = parse_array(row.get("route_ids", ""), f"{prefix}.route_ids", errors)
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
            if not 4 <= stage <= 18:
                errors.append(f"{prefix} has invalid blind review stage")
            if (
                row.get("review_disposition") == "CANDIDATE"
                and not linked_candidates
            ):
                errors.append(f"{prefix} candidate disposition has no B link")
            if (
                row.get("review_disposition") == "CROSS_REFERENCE"
                and not linked_routes
            ):
                errors.append(f"{prefix} cross-reference disposition has no route")
        else:
            errors.append(f"{prefix} has invalid review_status")

    if require_all_reviewed and reviewed_count != len(units):
        errors.append("not every source unit is reviewed")

    if [row.get("route_id") for row in routes] != [
        f"R{index:06d}" for index in range(1, len(routes) + 1)
    ]:
        errors.append("route IDs are not a total canonical sequence")
    for row in routes:
        route_id = row["route_id"]
        prefix = f"route {route_id}"
        if row["source_unit_id"] not in unit_ids:
            errors.append(f"{prefix} has unknown source unit")
        if row["route_kind"] not in ROUTE_KINDS:
            errors.append(f"{prefix} has invalid kind")
        if row["status"] not in ROUTE_STATUSES:
            errors.append(f"{prefix} has invalid status")
        for key in ("target_unit_ids", "attempts", "vocabulary_terms"):
            values = parse_array(row[key], f"{prefix}.{key}", errors)
            if key == "target_unit_ids" and any(
                value not in unit_ids for value in values
            ):
                errors.append(f"{prefix} targets unknown source unit")
        if not row["literal_target"].strip() or not row["expected_topic"].strip():
            errors.append(f"{prefix} lacks target/topic")
        try:
            owning_stage = int(row["owning_stage"])
        except ValueError:
            owning_stage = -1
        if not 4 <= owning_stage <= 18:
            errors.append(f"{prefix} has invalid owning stage")
        targets = parse_array(row["target_unit_ids"], f"{prefix}.target_unit_ids", errors)
        if row["status"] == "RESOLVED" and not targets:
            errors.append(f"{prefix} resolved without target")
        if row["status"] == "MISSING_TARGET_FINAL" and not row[
            "defect_boundary"
        ].strip():
            errors.append(f"{prefix} final missing target lacks boundary")

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

    reading_by_unit = {row["source_unit_id"]: row for row in reading}
    for candidate in candidates:
        candidate_id = candidate["id"]
        linked_rows = [
            row
            for row in reading
            if candidate_id
            in parse_array(
                row["candidate_ids"],
                f"reading {row['source_unit_id']}.candidate_ids",
                errors,
            )
        ]
        if not linked_rows:
            errors.append(f"candidate {candidate_id} has no reading-ledger join")
        for source_unit_id in candidate["source_unit_ids"]:
            row = reading_by_unit.get(source_unit_id)
            if row is None or candidate_id not in parse_array(
                row["candidate_ids"],
                f"reading {source_unit_id}.candidate_ids",
                errors,
            ):
                errors.append(
                    f"candidate {candidate_id} provenance unit lacks reverse join: "
                    f"{source_unit_id}"
                )
    for route in routes:
        row = reading_by_unit.get(route["source_unit_id"])
        if row is None or route["route_id"] not in parse_array(
            row["route_ids"],
            f"reading {route['source_unit_id']}.route_ids",
            errors,
        ):
            errors.append(f"route {route['route_id']} lacks reading-ledger reverse join")

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
        expected_reference = image["inventory_status"]
        if row.get("reference_status") != expected_reference:
            errors.append(f"{prefix} reference status mismatch")
        link_id = row.get("link_id", "")
        if expected_reference == "REFERENCED":
            link = link_by_id.get(link_id)
            if link is None or link.get("resolved_path") != path:
                errors.append(f"{prefix} has invalid image link")
            else:
                if row.get("source_path") != link["source_path"]:
                    errors.append(f"{prefix} source path mismatch")
                if row.get("source_unit_id") != (link["source_unit_id"] or ""):
                    errors.append(f"{prefix} source unit mismatch")
                if row.get("assignment_basis") != "LIVE_MARKDOWN_REFERENCE":
                    errors.append(f"{prefix} has invalid reference assignment basis")
        else:
            if link_id or row.get("source_path") or row.get("source_unit_id"):
                errors.append(f"{prefix} unreferenced row claims live owner")
            if row.get("assignment_basis") != "UNIQUE_DIRECTORY_PAGE_RANGE":
                errors.append(f"{prefix} lacks explicit physical assignment basis")
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
        linked_candidates = parse_array(
            row.get("candidate_ids", ""), f"{prefix}.candidate_ids", errors
        )
        if any(value not in candidate_ids for value in linked_candidates):
            errors.append(f"{prefix} links unknown candidate")
        status = row.get("inspection_status")
        if status == "PENDING":
            if (
                row.get("visual_role")
                or row.get("evidence_statement")
                or row.get("review_stage")
                or row.get("reviewer")
                or linked_candidates
                or row.get("original_resolution_status") != "NOT_REVIEWED"
            ):
                errors.append(f"{prefix} pending row contains inspection result")
        elif status == "SCREENED":
            screened_count += 1
            if row.get("visual_role") not in VISUAL_ROLES:
                errors.append(f"{prefix} has invalid visual role")
            if row.get("original_resolution_status") not in {
                "NOT_REQUIRED",
                "REVIEWED",
            }:
                errors.append(f"{prefix} lacks resolution disposition")
            if row.get("transcription_status") not in {
                "NOT_APPLICABLE",
                "NOT_REQUIRED",
                "CHECKED",
            }:
                errors.append(f"{prefix} has invalid transcription status")
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
