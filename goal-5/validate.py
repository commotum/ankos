#!/usr/bin/env python3
"""Validate the compact Goal 5 inputs and a generated 29-document baseline."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path, PurePosixPath

import build


COVERAGE_PATH = build.GOAL_DIR / "coverage.csv"
COVERAGE_FIELDS = [
    "document_id",
    "raw_start_line",
    "raw_end_line",
    "first_pass",
    "second_pass",
    "authoritative_start",
    "authoritative_end",
    "reviewer_type",
    "notes",
]
IMAGE_REFERENCE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")


def validate_authoritative_source(data: dict[str, object]) -> Path:
    """Pin the local fixed-layout witness without making it a build input."""

    source = data.get("authoritative_source")
    if not isinstance(source, dict):
        raise build.BuildError("source-ranges.json lacks authoritative_source")
    relative = build.safe_relative_path(source.get("path"), suffix=".pdf")
    path = (build.REPO_ROOT / Path(relative)).resolve()
    repository = build.REPO_ROOT.resolve()
    if not path.is_relative_to(repository):
        raise build.BuildError("authoritative source resolves outside the repository")
    if path.is_relative_to(build.LEGACY_ROOT.resolve()) or path.is_relative_to(
        build.OUTPUT_ROOT.resolve()
    ):
        raise build.BuildError("authoritative source overlaps a protected corpus tree")
    if not path.is_file():
        raise build.BuildError(f"authoritative source is missing: {relative}")
    payload = path.read_bytes()
    if len(payload) != source.get("size_bytes"):
        raise build.BuildError("authoritative source byte size differs from its manifest")
    if build.sha256(payload) != source.get("sha256"):
        raise build.BuildError("authoritative source hash differs from its manifest")
    if not payload.startswith(b"%PDF-") or b"%%EOF" not in payload[-1024:]:
        raise build.BuildError("authoritative source is not a complete PDF payload")
    return path


def legacy_tree_digest() -> tuple[str, int]:
    lines: list[bytes] = []
    paths = sorted(
        (path for path in build.LEGACY_ROOT.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(build.REPO_ROOT).as_posix().encode(),
    )
    for path in paths:
        digest = build.sha256(path.read_bytes())
        label = path.relative_to(build.REPO_ROOT).as_posix()
        lines.append(f"{digest}  {label}\n".encode())
    return hashlib.sha256(b"".join(lines)).hexdigest(), len(paths)


def independent_document_bytes(
    raw: bytes,
    documents: list[dict[str, object]],
    corrections: list[dict[str, object]],
) -> dict[PurePosixPath, bytes]:
    rendered: dict[PurePosixPath, bytes] = {}
    for document in documents:
        start = int(document["raw_start_byte"])
        end = int(document["raw_end_byte_exclusive"])
        cursor = start
        pieces: list[bytes] = []
        relevant = sorted(
            (
                correction
                for correction in corrections
                if correction["document_id"] == document["id"]
            ),
            key=lambda correction: int(correction["raw_start_byte"]),
        )
        for correction in relevant:
            correction_start = int(correction["raw_start_byte"])
            before = str(correction["before"]).encode("utf-8")
            pieces.append(raw[cursor:correction_start])
            pieces.append(str(correction["after"]).encode("utf-8"))
            cursor = correction_start + len(before)
        pieces.append(raw[cursor:end])
        output = build.safe_relative_path(document["output_path"], suffix=".md")
        rendered[output] = b"".join(pieces)
    return rendered


def validate_coverage(
    documents: list[dict[str, object]], path: Path = COVERAGE_PATH
) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != COVERAGE_FIELDS:
            raise build.BuildError(
                f"{path}: expected columns {COVERAGE_FIELDS}, found {reader.fieldnames}"
            )
        rows = list(reader)
    if len(rows) != len(documents):
        raise build.BuildError(
            f"{path}: expected one row per document ({len(documents)}), found {len(rows)}"
        )
    expected_order = [str(document["id"]) for document in documents]
    actual_order = [row["document_id"] for row in rows]
    if actual_order != expected_order:
        raise build.BuildError(f"{path}: coverage rows are not in canonical order")
    by_id: dict[str, dict[str, str]] = {}
    for row in rows:
        document_id = row["document_id"]
        if not document_id or document_id in by_id:
            raise build.BuildError(f"{path}: duplicate or empty document_id {document_id!r}")
        by_id[document_id] = row

    for document in documents:
        document_id = str(document["id"])
        row = by_id.get(document_id)
        if row is None:
            raise build.BuildError(f"{path}: missing coverage row for {document_id}")
        if row["raw_start_line"] != str(document["raw_start_line"]):
            raise build.BuildError(f"{path}: {document_id} start line drift")
        if row["raw_end_line"] != str(document["raw_end_line"]):
            raise build.BuildError(f"{path}: {document_id} end line drift")
        expected_source_start = f"pdf:{int(document['authoritative_pdf_start_page']):04d}"
        expected_source_end = f"pdf:{int(document['authoritative_pdf_end_page']):04d}"
        if row["authoritative_start"] != expected_source_start:
            raise build.BuildError(f"{path}: {document_id} authoritative start drift")
        if row["authoritative_end"] != expected_source_end:
            raise build.BuildError(f"{path}: {document_id} authoritative end drift")
        if row["first_pass"] not in {"NO", "YES"} or row["second_pass"] not in {"NO", "YES"}:
            raise build.BuildError(f"{path}: {document_id} pass values must be NO or YES")
        if row["second_pass"] == "YES" and row["first_pass"] != "YES":
            raise build.BuildError(f"{path}: {document_id} second pass precedes first pass")
        if row["first_pass"] == "YES" and not row["reviewer_type"].strip():
            raise build.BuildError(
                f"{path}: {document_id} reviewed row lacks reviewer_type"
            )
    return rows


def expected_output_files(
    documents: list[dict[str, object]],
    images: list[dict[str, object]],
    added_assets: list[dict[str, object]] | None = None,
) -> set[PurePosixPath]:
    if added_assets is None:
        added_assets = []
    document_paths = {
        str(document["id"]): build.safe_relative_path(
            document["output_path"], suffix=".md"
        )
        for document in documents
    }
    expected = set(document_paths.values())
    expected.update({PurePosixPath("README.md"), PurePosixPath("Contents.md")})
    for row in images:
        source = build.safe_relative_path(row["asset_relative_path"], suffix=".jpeg")
        expected.add(document_paths[str(row["document_id"])].parent / source.name)
    for row in added_assets:
        source = build.safe_relative_path(row["asset_relative_path"], suffix=".jpeg")
        expected.add(document_paths[str(row["document_id"])].parent / source.name)
    return expected


def validate_output(
    output_root: Path,
    raw: bytes,
    documents: list[dict[str, object]],
    corrections: list[dict[str, object]],
    images: list[dict[str, object]],
    *,
    zero_corrections: bool = False,
    added_assets: list[dict[str, object]] | None = None,
) -> None:
    if added_assets is None:
        added_assets = []
    output = output_root.resolve()
    build._safe_output_root(output)
    if not output.is_dir():
        raise build.BuildError(f"output directory does not exist: {output}")

    rendered = independent_document_bytes(raw, documents, corrections)
    for relative, expected in rendered.items():
        path = output / Path(relative)
        if not path.is_file() or path.read_bytes() != expected:
            raise build.BuildError(f"missing or changed output document: {relative}")
    if zero_corrections and b"".join(rendered.values()) != raw:
        raise build.BuildError("zero-correction documents do not reassemble to the monolith")

    document_paths = {
        str(document["id"]): build.safe_relative_path(
            document["output_path"], suffix=".md"
        )
        for document in documents
    }
    expected_references: list[tuple[str, str]] = []
    for row in images:
        source = build.safe_relative_path(row["asset_relative_path"], suffix=".jpeg")
        relative = document_paths[str(row["document_id"])].parent / source.name
        path = output / Path(relative)
        expected_hash = (
            row["asset_sha256"]
            if zero_corrections
            else row.get("repaired_asset_sha256", row["asset_sha256"])
        )
        if not path.is_file() or build.sha256(path.read_bytes()) != expected_hash:
            raise build.BuildError(f"missing or changed output image: {relative}")
        if zero_corrections or row.get("reference_disposition") not in (
            build.OMITTED_REFERENCE_DISPOSITIONS
        ):
            expected_references.append((str(row["document_id"]), source.name))

    expected_added_references: list[tuple[str, str]] = []
    for row in added_assets:
        source = build.safe_relative_path(row["asset_relative_path"], suffix=".jpeg")
        relative = document_paths[str(row["document_id"])].parent / source.name
        path = output / Path(relative)
        if not path.is_file() or build.sha256(path.read_bytes()) != row["asset_sha256"]:
            raise build.BuildError(f"missing or changed source-added image: {relative}")
        expected_added_references.append((str(row["document_id"]), source.name))

    actual_references: list[tuple[str, str]] = []
    for document in documents:
        document_id = str(document["id"])
        relative = document_paths[document_id]
        text = (output / Path(relative)).read_text(encoding="utf-8")
        for target in IMAGE_REFERENCE.findall(text):
            target_path = build.safe_relative_path(target)
            resolved = relative.parent / target_path
            if not (output / Path(resolved)).is_file():
                raise build.BuildError(f"{relative}: unresolved image target {target}")
            actual_references.append((document_id, target_path.name))
    added_reference_set = set(expected_added_references)
    actual_added = [row for row in actual_references if row in added_reference_set]
    actual_legacy = [row for row in actual_references if row not in added_reference_set]
    if actual_legacy != expected_references:
        raise build.BuildError("output image references differ from image-map.jsonl")
    if sorted(actual_added) != sorted(expected_added_references):
        raise build.BuildError("output source-added image references differ from manifest")

    if (output / "README.md").read_bytes() != build.readme_bytes():
        raise build.BuildError("README.md is missing or changed")
    if (output / "Contents.md").read_bytes() != build.contents_bytes(documents):
        raise build.BuildError("Contents.md is missing or changed")
    for document in documents:
        relative = document_paths[str(document["id"])]
        if not (output / Path(relative)).is_file():
            raise build.BuildError(f"Contents target is missing: {relative}")

    actual_files = {
        PurePosixPath(path.relative_to(output).as_posix())
        for path in output.rglob("*")
        if path.is_file()
    }
    expected_files = expected_output_files(documents, images, added_assets)
    if actual_files != expected_files:
        missing = sorted(str(path) for path in expected_files - actual_files)
        extra = sorted(str(path) for path in actual_files - expected_files)
        raise build.BuildError(f"output file set differs; missing={missing} extra={extra}")


def validate(
    output_root: Path = build.OUTPUT_ROOT, *, zero_corrections: bool = False
) -> tuple[int, int, int, int]:
    raw, documents, corrections, images = build.load_inputs()
    added_assets = build.load_added_assets(documents, images)
    if zero_corrections:
        corrections = []
        added_assets = []
    facts = json.loads((build.GOAL_DIR / "legacy-facts.json").read_text(encoding="utf-8"))
    range_data = json.loads(build.RANGES_PATH.read_text(encoding="utf-8"))
    validate_authoritative_source(range_data)
    expected_digest = facts["legacy_tree"]["snapshot_sha256"]
    expected_files = facts["legacy_tree"]["file_counts"]["regular_files"]
    actual_digest, actual_files = legacy_tree_digest()
    if (actual_digest, actual_files) != (expected_digest, expected_files):
        raise build.BuildError(
            "complete legacy tree differs from the frozen path-and-file snapshot"
        )
    coverage = validate_coverage(documents)
    validate_output(
        output_root,
        raw,
        documents,
        corrections,
        images,
        zero_corrections=zero_corrections,
        added_assets=added_assets,
    )
    reviewed = sum(row["second_pass"] == "YES" for row in coverage)
    return len(documents), len(images) + len(added_assets), len(corrections), reviewed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=build.OUTPUT_ROOT)
    parser.add_argument(
        "--zero-corrections",
        action="store_true",
        help="validate the target as the raw 29-document projection",
    )
    args = parser.parse_args()
    documents, images, corrections, reviewed = validate(
        args.output, zero_corrections=args.zero_corrections
    )
    print(
        f"validated baseline: documents={documents} images={images} "
        f"corrections={corrections} second_pass_documents={reviewed}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
