#!/usr/bin/env python3
"""Initialize deterministic empty/resumable Goal 4 audit ledgers."""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
from pathlib import Path
from typing import Any

import audit_transaction
from audit_contract import (
    ASSET_HEADER,
    CROSS_REFERENCE_HEADER,
    GOAL_DIR,
    READING_HEADER,
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
REVIEW_HISTORY_PATH = GOAL_DIR / "review-history.jsonl"
SCHEMA_DIR = GOAL_DIR / "schemas"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def csv_bytes(header: list[str], rows: list[dict[str, Any]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(
        buffer,
        fieldnames=header,
        lineterminator="\n",
        extrasaction="raise",
    )
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def expected_artifacts() -> dict[Path, bytes]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    units = read_jsonl(UNITS_PATH)

    reading_rows: list[dict[str, Any]] = []
    for unit in units:
        reading_rows.append(
            {
                "source_unit_id": unit["id"],
                "document_order": unit["document_order"],
                "path": unit["path"],
                "block_kind": unit["block_kind"],
                "byte_start": unit["byte_start"],
                "byte_end": unit["byte_end"],
                "line_start": unit["line_start"],
                "line_end": unit["line_end"],
                "global_line_start": unit["global_line_start"],
                "global_line_end": unit["global_line_end"],
                "unit_sha256": unit["sha256"],
                "review_status": "PENDING",
                "review_epoch": "",
                "review_disposition": "",
                "source_status": "",
                "uncertainty": "",
                "secondary_roles": "[]",
                "candidate_ids": "[]",
                "route_ids": "[]",
                "evidence_statement": "",
                "review_stage": "",
                "reviewer": "",
            }
        )

    image_links = {
        link["resolved_path"]: link
        for link in manifest["links"]
        if link["kind"] == "image"
    }
    page_pattern = re.compile(r"_page_(\d+)")
    page_ranges: dict[str, tuple[int, int]] = {}
    for document in manifest["documents"]:
        pages = [
            int(match.group(1))
            for image_path in document["image_references"]
            if (match := page_pattern.search(Path(image_path).name))
        ]
        if pages:
            page_ranges[document["path"]] = (min(pages), max(pages))

    def stage_for_path(path: str) -> int:
        document = next(item for item in manifest["documents"] if item["path"] == path)
        if document["kind"] in {
            "publication_and_printed_contents",
            "preface",
            "general_notes",
            "colophon",
        }:
            return 4
        if document["kind"] in {"chapter", "chapter_notes"}:
            return 4 + int(document["chapter_number"])
        if document["kind"] == "index":
            return 17
        raise ValueError(f"no audit stage for {path}")

    asset_rows: list[dict[str, Any]] = []
    for index, image in enumerate(manifest["images"], start=1):
        link = image_links.get(image["path"])
        if link is not None:
            assignment_path = link["source_path"]
            assignment_basis = "LIVE_MARKDOWN_REFERENCE"
        else:
            match = page_pattern.search(Path(image["path"]).name)
            page = int(match.group(1)) if match else None
            candidates = [
                path
                for path, (first, last) in page_ranges.items()
                if page is not None
                and first <= page <= last
                and Path(path).parent == Path(image["path"]).parent
            ]
            if len(candidates) != 1:
                raise ValueError(
                    f"unreferenced image has no unique owning page range: "
                    f"{image['path']} candidates={candidates}"
                )
            assignment_path = candidates[0]
            assignment_basis = "UNIQUE_DIRECTORY_PAGE_RANGE"
        asset_rows.append(
            {
                "asset_id": f"A{index:06d}",
                "link_id": link["id"] if link else "",
                "physical_path": image["path"],
                "sha256": image["sha256"],
                "bytes": image["bytes"],
                "source_path": link["source_path"] if link else "",
                "source_unit_id": link["source_unit_id"] if link else "",
                "assignment_path": assignment_path,
                "assignment_stage": stage_for_path(assignment_path),
                "assignment_basis": assignment_basis,
                "reference_status": image["inventory_status"],
                "inspection_status": "PENDING",
                "review_epoch": "",
                "visual_role": "",
                "source_status": "",
                "risk_flags": "[]",
                "original_resolution_status": "NOT_REVIEWED",
                "transcription_status": "NOT_APPLICABLE",
                "candidate_ids": "[]",
                "route_ids": "[]",
                "evidence_statement": "",
                "review_stage": "",
                "reviewer": "",
                "uncertainty": "",
            }
        )

    search = {
        "schema_version": 1,
        "phase": "blind_discovery",
        "tool_assumptions": [],
        "vocabulary": [],
        "rounds": [],
        "fixed_point": None,
    }

    artifacts: dict[Path, bytes] = {
        READING_PATH: csv_bytes(READING_HEADER, reading_rows),
        CANDIDATE_PATH: b"",
        CROSS_REFERENCE_PATH: csv_bytes(CROSS_REFERENCE_HEADER, []),
        ASSET_PATH: csv_bytes(ASSET_HEADER, asset_rows),
        REVIEW_HISTORY_PATH: b"",
        SEARCH_PATH: canonical_json_bytes(search),
    }
    for relative, schema in schema_documents().items():
        artifacts[SCHEMA_DIR / relative] = canonical_json_bytes(schema)
    return artifacts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-initial", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if args.check_initial:
        try:
            with audit_transaction.read_guard(GOAL_DIR):
                artifacts = expected_artifacts()
                stale = [
                    str(path.relative_to(GOAL_DIR))
                    for path, expected in artifacts.items()
                    if not path.exists() or path.read_bytes() != expected
                ]
        except audit_transaction.TransactionError as exc:
            print(
                "refusing initial-state comparison while transaction "
                f"is pending or busy: {exc}"
            )
            return 1
        if stale:
            print("initial audit artifacts differ: " + ", ".join(stale))
            return 1
        print("initial audit artifacts reproduce exactly")
        return 0

    try:
        audit_transaction.require_clean(GOAL_DIR)
    except audit_transaction.TransactionError as exc:
        print(f"refusing initialization while transaction is pending: {exc}")
        return 1

    artifacts = expected_artifacts()
    existing_ledgers = [
        path
        for path in (
            READING_PATH,
            CANDIDATE_PATH,
            CROSS_REFERENCE_PATH,
            ASSET_PATH,
            REVIEW_HISTORY_PATH,
            SEARCH_PATH,
        )
        if path.exists()
    ]
    if existing_ledgers and not args.force:
        print(
            "refusing to overwrite existing audit ledgers: "
            + ", ".join(str(path.relative_to(GOAL_DIR)) for path in existing_ledgers)
        )
        return 1

    for path, data in artifacts.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    print(
        "initialized audit harness: "
        "reading_rows=14311 asset_rows=1607 candidates=0 routes=0 rounds=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
