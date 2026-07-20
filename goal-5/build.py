#!/usr/bin/env python3
"""Build the corrected release or raw diagnostic projection from immutable inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


GOAL_DIR = Path(__file__).resolve().parent
REPO_ROOT = GOAL_DIR.parent
LEGACY_ROOT = REPO_ROOT / "ref/A-New-Kind-of-Science"
MONOLITH_PATH = LEGACY_ROOT / "A-New-Kind-of-Science.md"
OUTPUT_ROOT = REPO_ROOT / "ref/A-New-Kind-of-Science-Repaired"
RANGES_PATH = GOAL_DIR / "source-ranges.json"
IMAGES_PATH = GOAL_DIR / "image-map.jsonl"
ADDED_ASSETS_PATH = GOAL_DIR / "added-assets.jsonl"
CORRECTIONS_PATH = GOAL_DIR / "corrections.jsonl"
SOURCE_STATUS = "USER_AUTHORIZED_LOCAL_SOURCE"
BOUNDARY_STATUS = "SOURCE_CONFIRMED"
SOURCE_PAGE_IN_ASSET = re.compile(r"_page_(\d+)_")
AUTHORITATIVE_LOCATION = re.compile(r"^pdf:(\d{4})(?:$|[; ,])")
REPAIRED_IMAGE_FIELDS = {
    "repaired_asset_relative_path",
    "repaired_asset_sha256",
    "repaired_authoritative_location",
    "repaired_reason",
    "repaired_width_px",
    "repaired_height_px",
}
REFERENCE_DISPOSITION_FIELDS = {
    "reference_disposition",
    "reference_authoritative_location",
    "reference_reason",
    "reference_reviewer_type",
    "reference_verification_status",
}
OMITTED_REFERENCE_DISPOSITION = (
    "SOURCE_FALSE_POSITIVE_RASTERIZED_TEXT_OMITTED"
)
REDUNDANT_REFERENCE_DISPOSITION = (
    "SOURCE_REDUNDANT_PARTIAL_CROP_REPLACED_OMITTED"
)
OMITTED_REFERENCE_DISPOSITIONS = frozenset(
    {
        OMITTED_REFERENCE_DISPOSITION,
        REDUNDANT_REFERENCE_DISPOSITION,
    }
)
ADDED_ASSET_FIELDS = {
    "id",
    "document_id",
    "asset_relative_path",
    "asset_sha256",
    "authoritative_location",
    "reason",
    "width_px",
    "height_px",
    "reviewer_type",
    "verification_status",
}


class BuildError(ValueError):
    """An input cannot produce the promised validated corpus."""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def jpeg_dimensions(data: bytes) -> tuple[int, int]:
    """Read JPEG dimensions without adding an image-library dependency."""

    if not data.startswith(b"\xff\xd8"):
        raise BuildError("asset is not a JPEG")
    start_of_frame = {
        0xC0,
        0xC1,
        0xC2,
        0xC3,
        0xC5,
        0xC6,
        0xC7,
        0xC9,
        0xCA,
        0xCB,
        0xCD,
        0xCE,
        0xCF,
    }
    index = 2
    while index < len(data):
        while index < len(data) and data[index] != 0xFF:
            index += 1
        while index < len(data) and data[index] == 0xFF:
            index += 1
        if index >= len(data):
            break
        marker = data[index]
        index += 1
        if marker in {0x01, 0xD8, 0xD9}:
            continue
        if index + 2 > len(data):
            break
        length = int.from_bytes(data[index : index + 2], "big")
        if length < 2 or index + length > len(data):
            break
        if marker in start_of_frame:
            if length < 7:
                break
            height = int.from_bytes(data[index + 3 : index + 5], "big")
            width = int.from_bytes(data[index + 5 : index + 7], "big")
            if width <= 0 or height <= 0:
                break
            return width, height
        index += length
    raise BuildError("JPEG has no valid start-of-frame dimensions")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise BuildError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise BuildError(f"{path}:{line_number}: expected a JSON object")
        rows.append(row)
    return rows


def safe_relative_path(value: object, *, suffix: str | None = None) -> PurePosixPath:
    if not isinstance(value, str) or not value:
        raise BuildError(f"invalid relative path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise BuildError(f"unsafe relative path: {value}")
    if suffix is not None and path.suffix.lower() != suffix:
        raise BuildError(f"expected a {suffix} path: {value}")
    return path


def validate_ranges(raw: bytes, data: dict[str, Any]) -> list[dict[str, Any]]:
    documents = data.get("documents")
    if not isinstance(documents, list) or len(documents) != 29:
        raise BuildError("source-ranges.json must contain exactly 29 documents")
    expected_raw_hash = data.get("legacy_source_sha256")
    if sha256(raw) != expected_raw_hash:
        raise BuildError("raw monolith hash does not match source-ranges.json")

    source = data.get("authoritative_source")
    if not isinstance(source, dict):
        raise BuildError("source-ranges.json lacks authoritative_source")
    required_source_fields = {
        "id",
        "path",
        "sha256",
        "size_bytes",
        "pdf_page_count",
        "edition",
        "printing",
        "isbn_10",
        "location_convention",
        "authorization_date",
        "authorization_scope",
        "source_status",
    }
    missing_source_fields = required_source_fields - source.keys()
    if missing_source_fields:
        raise BuildError(
            f"authoritative_source lacks {sorted(missing_source_fields)}"
        )
    safe_relative_path(source["path"], suffix=".pdf")
    source_hash = source["sha256"]
    if (
        not isinstance(source_hash, str)
        or len(source_hash) != 64
        or any(character not in "0123456789abcdef" for character in source_hash)
    ):
        raise BuildError("authoritative_source has an invalid SHA-256")
    if not isinstance(source["size_bytes"], int) or source["size_bytes"] <= 0:
        raise BuildError("authoritative_source has an invalid byte size")
    page_count = source["pdf_page_count"]
    if not isinstance(page_count, int) or page_count <= 0:
        raise BuildError("authoritative_source has an invalid PDF page count")
    if source["source_status"] != SOURCE_STATUS:
        raise BuildError("authoritative_source is not authorized for local review")
    for field in (
        "id",
        "edition",
        "printing",
        "isbn_10",
        "location_convention",
        "authorization_date",
        "authorization_scope",
    ):
        if not isinstance(source[field], str) or not source[field].strip():
            raise BuildError(f"authoritative_source has an empty {field}")

    byte_cursor = 0
    line_cursor = 1
    authoritative_page_cursor = 1
    ids: set[str] = set()
    outputs: set[PurePosixPath] = set()
    for order, document in enumerate(documents):
        if not isinstance(document, dict) or document.get("order") != order:
            raise BuildError(f"document order is missing or non-contiguous at {order}")
        document_id = document.get("id")
        if not isinstance(document_id, str) or not document_id or document_id in ids:
            raise BuildError(f"duplicate or invalid document id: {document_id!r}")
        ids.add(document_id)
        output = safe_relative_path(document.get("output_path"), suffix=".md")
        if output in outputs:
            raise BuildError(f"duplicate output path: {output}")
        outputs.add(output)

        start = document.get("raw_start_byte")
        end = document.get("raw_end_byte_exclusive")
        start_line = document.get("raw_start_line")
        end_line = document.get("raw_end_line")
        if start != byte_cursor or not isinstance(end, int) or end <= start:
            raise BuildError(f"{document_id}: byte gap, overlap, or empty range")
        if start_line != line_cursor or not isinstance(end_line, int) or end_line < start_line:
            raise BuildError(f"{document_id}: line gap, overlap, or empty range")
        if start != 0 and raw[start - 1 : start] != b"\n":
            raise BuildError(f"{document_id}: byte range does not start after an LF")
        if end != len(raw) and raw[end - 1 : end] != b"\n":
            raise BuildError(f"{document_id}: byte range does not end at an LF")
        segment = raw[start:end]
        if len(segment) != document.get("raw_byte_count"):
            raise BuildError(f"{document_id}: byte count mismatch")
        logical_lines = segment.count(b"\n") + (0 if segment.endswith(b"\n") else 1)
        if logical_lines != document.get("raw_line_count"):
            raise BuildError(f"{document_id}: logical line count mismatch")
        if end_line - start_line + 1 != document.get("raw_line_count"):
            raise BuildError(f"{document_id}: declared line interval mismatch")
        if sha256(segment) != document.get("raw_segment_sha256"):
            raise BuildError(f"{document_id}: segment hash mismatch")
        if document.get("boundary_status") != BOUNDARY_STATUS:
            raise BuildError(f"{document_id}: boundary is not source confirmed")
        source_start = document.get("authoritative_pdf_start_page")
        source_end = document.get("authoritative_pdf_end_page")
        if (
            source_start != authoritative_page_cursor
            or not isinstance(source_end, int)
            or source_end < source_start
            or source_end > page_count
        ):
            raise BuildError(
                f"{document_id}: authoritative PDF page gap, overlap, or invalid range"
            )
        for field in ("authoritative_printed_start", "authoritative_printed_end"):
            if not isinstance(document.get(field), str) or not document[field].strip():
                raise BuildError(f"{document_id}: missing {field}")
        byte_cursor = end
        line_cursor = end_line + 1
        authoritative_page_cursor = source_end + 1

    if byte_cursor != len(raw):
        raise BuildError("document ranges do not reach the end of the monolith")
    if line_cursor - 1 != len(raw.splitlines()):
        raise BuildError("document line ranges do not cover the monolith")
    if authoritative_page_cursor != page_count + 1:
        raise BuildError("document ranges do not cover the authoritative PDF")
    return documents


CORRECTION_FIELDS = {
    "id",
    "document_id",
    "raw_start_byte",
    "before",
    "after",
    "expected_count",
    "authoritative_location",
    "reason",
    "reviewer_type",
    "verification_status",
}


def validate_corrections(
    corrections: Iterable[dict[str, Any]],
    raw: bytes,
    documents: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    documents_by_id = {document["id"]: document for document in documents}
    checked: list[dict[str, Any]] = []
    correction_ids: set[str] = set()
    for index, correction in enumerate(corrections, 1):
        missing = CORRECTION_FIELDS - correction.keys()
        if missing:
            raise BuildError(f"correction {index}: missing {sorted(missing)}")
        correction_id = correction["id"]
        if not isinstance(correction_id, str) or not correction_id or correction_id in correction_ids:
            raise BuildError(f"correction {index}: duplicate or invalid id")
        correction_ids.add(correction_id)
        document_id = correction["document_id"]
        if document_id not in documents_by_id:
            raise BuildError(f"{correction_id}: unknown document id")
        raw_start = correction["raw_start_byte"]
        if isinstance(raw_start, bool) or not isinstance(raw_start, int) or raw_start < 0:
            raise BuildError(f"{correction_id}: raw_start_byte must be a non-negative integer")
        before = correction["before"]
        after = correction["after"]
        if not isinstance(before, str) or not before or not isinstance(after, str) or before == after:
            raise BuildError(f"{correction_id}: before/after must be distinct text")
        expected_count = correction["expected_count"]
        if isinstance(expected_count, bool) or not isinstance(expected_count, int) or expected_count < 1:
            raise BuildError(f"{correction_id}: expected_count must be a positive integer")
        for field in ("authoritative_location", "reason", "reviewer_type"):
            if not isinstance(correction[field], str) or not correction[field].strip():
                raise BuildError(f"{correction_id}: {field} must be non-empty")
        if correction["verification_status"] != "SOURCE_VERIFIED":
            raise BuildError(f"{correction_id}: correction is not source verified")
        before_bytes = before.encode("utf-8")
        document = documents_by_id[document_id]
        source_match = AUTHORITATIVE_LOCATION.match(correction["authoritative_location"])
        if source_match is None:
            raise BuildError(
                f"{correction_id}: authoritative_location must begin with pdf:NNNN"
            )
        source_page = int(source_match.group(1))
        if not (
            document["authoritative_pdf_start_page"]
            <= source_page
            <= document["authoritative_pdf_end_page"]
        ):
            raise BuildError(
                f"{correction_id}: authoritative PDF page is outside its document"
            )
        raw_end = raw_start + len(before_bytes)
        if not (
            document["raw_start_byte"] <= raw_start < raw_end <= document["raw_end_byte_exclusive"]
        ):
            raise BuildError(f"{correction_id}: raw span is outside its document")
        if raw[raw_start:raw_end] != before_bytes:
            raise BuildError(f"{correction_id}: exact raw preimage does not match")
        segment = raw[document["raw_start_byte"] : document["raw_end_byte_exclusive"]]
        actual_count = segment.count(before_bytes)
        if actual_count != expected_count:
            raise BuildError(
                f"{correction_id}: expected {expected_count} raw occurrence(s), found {actual_count}"
            )
        checked.append(correction)

    for document_id in documents_by_id:
        previous_end: int | None = None
        for correction in sorted(
            (row for row in checked if row["document_id"] == document_id),
            key=lambda row: row["raw_start_byte"],
        ):
            start = correction["raw_start_byte"]
            end = start + len(correction["before"].encode("utf-8"))
            if previous_end is not None and start < previous_end:
                raise BuildError(f"{correction['id']}: correction spans overlap")
            previous_end = end
    return checked


def apply_corrections(
    document: dict[str, Any],
    segment: bytes,
    corrections: Iterable[dict[str, Any]],
) -> bytes:
    relevant = sorted(
        (row for row in corrections if row["document_id"] == document["id"]),
        key=lambda row: row["raw_start_byte"],
        reverse=True,
    )
    for correction in relevant:
        local_start = correction["raw_start_byte"] - document["raw_start_byte"]
        before = correction["before"].encode("utf-8")
        local_end = local_start + len(before)
        if segment[local_start:local_end] != before:
            raise BuildError(f"{correction['id']}: exact raw preimage no longer matches")
        after = correction["after"].encode("utf-8")
        segment = segment[:local_start] + after + segment[local_end:]
    return segment


def validate_images(
    raw: bytes,
    documents: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    *,
    legacy_root: Path = LEGACY_ROOT,
) -> list[dict[str, Any]]:
    if len(rows) != 1444:
        raise BuildError(f"image-map.jsonl must contain 1,444 rows, found {len(rows)}")
    documents_by_id = {str(document["id"]): document for document in documents}
    document_outputs = {
        document_id: safe_relative_path(document["output_path"], suffix=".md")
        for document_id, document in documents_by_id.items()
    }
    source_paths: set[PurePosixPath] = set()
    output_paths: set[PurePosixPath] = set()
    lines = raw.decode("utf-8").splitlines()
    for ordinal, row in enumerate(rows, 1):
        if row.get("ordinal") != ordinal:
            raise BuildError(f"image ordinal is missing or non-contiguous at {ordinal}")
        document_id = row.get("document_id")
        if document_id not in document_outputs:
            raise BuildError(f"image {ordinal}: unknown document id {document_id!r}")
        source_path = safe_relative_path(row.get("asset_relative_path"), suffix=".jpeg")
        if source_path in source_paths:
            raise BuildError(f"image {ordinal}: duplicate source asset {source_path}")
        source_paths.add(source_path)
        output_path = document_outputs[document_id].parent / source_path.name
        if output_path in output_paths:
            raise BuildError(f"image {ordinal}: duplicate output asset {output_path}")
        output_paths.add(output_path)
        line_number = row.get("monolith_line")
        if not isinstance(line_number, int) or not 1 <= line_number <= len(lines):
            raise BuildError(f"image {ordinal}: invalid monolith line")
        owner = documents_by_id[document_id]
        if not owner["raw_start_line"] <= line_number <= owner["raw_end_line"]:
            raise BuildError(f"image {ordinal}: monolith line is outside its owner range")
        source_page_match = SOURCE_PAGE_IN_ASSET.search(source_path.name)
        if source_page_match is None:
            raise BuildError(f"image {ordinal}: asset name lacks a source page")
        source_page = int(source_page_match.group(1)) + 1
        if not (
            owner["authoritative_pdf_start_page"]
            <= source_page
            <= owner["authoritative_pdf_end_page"]
        ):
            raise BuildError(
                f"image {ordinal}: source page is outside its owner PDF range"
            )
        if source_path.name not in lines[line_number - 1]:
            raise BuildError(f"image {ordinal}: basename absent from its monolith line")
        asset = legacy_root / Path(source_path)
        if not asset.is_file() or sha256(asset.read_bytes()) != row.get("asset_sha256"):
            raise BuildError(f"image {ordinal}: missing or changed asset {source_path}")

        repaired_fields = REPAIRED_IMAGE_FIELDS & row.keys()
        if repaired_fields and repaired_fields != REPAIRED_IMAGE_FIELDS:
            missing = sorted(REPAIRED_IMAGE_FIELDS - repaired_fields)
            raise BuildError(f"image {ordinal}: incomplete repaired asset fields {missing}")
        if repaired_fields:
            repaired_relative = safe_relative_path(
                row["repaired_asset_relative_path"], suffix=".jpeg"
            )
            if repaired_relative.parts[:2] != ("goal-5", "assets"):
                raise BuildError(
                    f"image {ordinal}: repaired asset must be under goal-5/assets"
                )
            if repaired_relative.name != source_path.name:
                raise BuildError(
                    f"image {ordinal}: repaired asset basename must match mapped asset"
                )
            repaired_location = row["repaired_authoritative_location"]
            if not isinstance(repaired_location, str):
                raise BuildError(f"image {ordinal}: invalid repaired source location")
            repaired_page_match = AUTHORITATIVE_LOCATION.match(repaired_location)
            if repaired_page_match is None or int(repaired_page_match.group(1)) != source_page:
                raise BuildError(
                    f"image {ordinal}: repaired source page does not match asset name"
                )
            if not isinstance(row["repaired_reason"], str) or not row["repaired_reason"].strip():
                raise BuildError(f"image {ordinal}: repaired asset lacks a reason")
            for field in ("repaired_width_px", "repaired_height_px"):
                if (
                    isinstance(row[field], bool)
                    or not isinstance(row[field], int)
                    or row[field] <= 0
                ):
                    raise BuildError(f"image {ordinal}: invalid {field}")
            repaired_asset = REPO_ROOT / Path(repaired_relative)
            repaired_hash = row["repaired_asset_sha256"]
            if (
                not repaired_asset.is_file()
                or not isinstance(repaired_hash, str)
                or sha256(repaired_asset.read_bytes()) != repaired_hash
            ):
                raise BuildError(
                    f"image {ordinal}: missing or changed repaired asset {repaired_relative}"
                )
            actual_dimensions = jpeg_dimensions(repaired_asset.read_bytes())
            declared_dimensions = (
                row["repaired_width_px"],
                row["repaired_height_px"],
            )
            if actual_dimensions != declared_dimensions:
                raise BuildError(
                    f"image {ordinal}: repaired asset dimensions differ from manifest"
                )

        disposition_fields = REFERENCE_DISPOSITION_FIELDS & row.keys()
        if disposition_fields and disposition_fields != REFERENCE_DISPOSITION_FIELDS:
            missing = sorted(REFERENCE_DISPOSITION_FIELDS - disposition_fields)
            raise BuildError(
                f"image {ordinal}: incomplete reference disposition fields {missing}"
            )
        if disposition_fields:
            if row["reference_disposition"] not in OMITTED_REFERENCE_DISPOSITIONS:
                raise BuildError(
                    f"image {ordinal}: unsupported reference disposition"
                )
            disposition_location = row["reference_authoritative_location"]
            location_match = (
                AUTHORITATIVE_LOCATION.match(disposition_location)
                if isinstance(disposition_location, str)
                else None
            )
            if location_match is None or int(location_match.group(1)) != source_page:
                raise BuildError(
                    f"image {ordinal}: reference disposition source page differs"
                )
            if (
                not isinstance(row["reference_reason"], str)
                or not row["reference_reason"].strip()
            ):
                raise BuildError(
                    f"image {ordinal}: reference disposition lacks a reason"
                )
            if row["reference_reviewer_type"] != "agent":
                raise BuildError(
                    f"image {ordinal}: invalid reference disposition reviewer"
                )
            if row["reference_verification_status"] != "SOURCE_VERIFIED":
                raise BuildError(
                    f"image {ordinal}: reference disposition is not source verified"
                )

    physical_assets = {
        PurePosixPath(path.relative_to(legacy_root).as_posix())
        for path in legacy_root.rglob("*.jpeg")
    }
    if physical_assets != source_paths:
        raise BuildError("image map and physical legacy JPEG inventory differ")
    return rows


def validate_added_assets(
    documents: list[dict[str, Any]],
    images: list[dict[str, Any]],
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Validate source-backed visuals absent from the legacy extraction."""

    documents_by_id = {str(document["id"]): document for document in documents}
    document_outputs = {
        document_id: safe_relative_path(document["output_path"], suffix=".md")
        for document_id, document in documents_by_id.items()
    }
    occupied_outputs = {
        document_outputs[str(row["document_id"])].parent
        / safe_relative_path(row["asset_relative_path"], suffix=".jpeg").name
        for row in images
    }
    ids: set[str] = set()
    source_paths: set[PurePosixPath] = set()
    for index, row in enumerate(rows, 1):
        missing = ADDED_ASSET_FIELDS - row.keys()
        if missing:
            raise BuildError(f"added asset {index}: missing {sorted(missing)}")
        asset_id = row["id"]
        if not isinstance(asset_id, str) or not asset_id or asset_id in ids:
            raise BuildError(f"added asset {index}: duplicate or invalid id")
        ids.add(asset_id)
        document_id = row["document_id"]
        if document_id not in documents_by_id:
            raise BuildError(f"{asset_id}: unknown document id")
        relative = safe_relative_path(row["asset_relative_path"], suffix=".jpeg")
        if relative.parts[:2] != ("goal-5", "assets"):
            raise BuildError(f"{asset_id}: added asset must be under goal-5/assets")
        if relative in source_paths:
            raise BuildError(f"{asset_id}: duplicate added asset path")
        source_paths.add(relative)
        output_path = document_outputs[document_id].parent / relative.name
        if output_path in occupied_outputs:
            raise BuildError(f"{asset_id}: duplicate output asset {output_path}")
        occupied_outputs.add(output_path)

        page_match = SOURCE_PAGE_IN_ASSET.search(relative.name)
        location = row["authoritative_location"]
        location_match = (
            AUTHORITATIVE_LOCATION.match(location)
            if isinstance(location, str)
            else None
        )
        if page_match is None or location_match is None:
            raise BuildError(f"{asset_id}: added asset lacks a canonical source page")
        filename_page = int(page_match.group(1)) + 1
        source_page = int(location_match.group(1))
        owner = documents_by_id[document_id]
        if filename_page != source_page or not (
            owner["authoritative_pdf_start_page"]
            <= source_page
            <= owner["authoritative_pdf_end_page"]
        ):
            raise BuildError(f"{asset_id}: added asset source page or owner differs")
        for field in ("reason", "reviewer_type"):
            if not isinstance(row[field], str) or not row[field].strip():
                raise BuildError(f"{asset_id}: {field} must be non-empty")
        if row["verification_status"] != "SOURCE_VERIFIED":
            raise BuildError(f"{asset_id}: added asset is not source verified")
        for field in ("width_px", "height_px"):
            if (
                isinstance(row[field], bool)
                or not isinstance(row[field], int)
                or row[field] <= 0
            ):
                raise BuildError(f"{asset_id}: invalid {field}")

        asset = REPO_ROOT / Path(relative)
        digest = row["asset_sha256"]
        if (
            not asset.is_file()
            or not isinstance(digest, str)
            or sha256(asset.read_bytes()) != digest
        ):
            raise BuildError(f"{asset_id}: missing or changed added asset {relative}")
        if jpeg_dimensions(asset.read_bytes()) != (row["width_px"], row["height_px"]):
            raise BuildError(f"{asset_id}: added asset dimensions differ from manifest")
    return rows


def load_added_assets(
    documents: list[dict[str, Any]], images: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    return validate_added_assets(
        documents, images, read_jsonl(ADDED_ASSETS_PATH)
    )


def output_image_source(
    row: dict[str, Any], *, use_repaired_assets: bool = True
) -> Path:
    repaired = row.get("repaired_asset_relative_path") if use_repaired_assets else None
    if repaired is not None:
        return REPO_ROOT / Path(safe_relative_path(repaired, suffix=".jpeg"))
    return LEGACY_ROOT / Path(
        safe_relative_path(row["asset_relative_path"], suffix=".jpeg")
    )


def load_inputs() -> tuple[bytes, list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    range_data = json.loads(RANGES_PATH.read_text(encoding="utf-8"))
    source = safe_relative_path(range_data.get("legacy_source"), suffix=".md")
    source_path = REPO_ROOT / Path(source)
    if source_path.resolve() != MONOLITH_PATH.resolve():
        raise BuildError("build input must be the immutable legacy monolith")
    raw = source_path.read_bytes()
    documents = validate_ranges(raw, range_data)
    corrections = validate_corrections(read_jsonl(CORRECTIONS_PATH), raw, documents)
    images = validate_images(raw, documents, read_jsonl(IMAGES_PATH))
    return raw, documents, corrections, images


def document_bytes(
    raw: bytes,
    documents: list[dict[str, Any]],
    corrections: list[dict[str, Any]],
) -> dict[PurePosixPath, bytes]:
    rendered: dict[PurePosixPath, bytes] = {}
    for document in documents:
        segment = raw[document["raw_start_byte"] : document["raw_end_byte_exclusive"]]
        segment = apply_corrections(document, segment, corrections)
        output = safe_relative_path(document["output_path"], suffix=".md")
        rendered[output] = segment
    return rendered


def readme_bytes(*, zero_corrections: bool = False) -> bytes:
    if zero_corrections:
        return (
            "<!-- GENERATED FILE — DO NOT EDIT DIRECTLY. -->\n\n"
            "# A New Kind of Science — raw diagnostic projection\n\n"
            "This directory was generated with `--zero-corrections`. It is an "
            "uncorrected diagnostic projection of the immutable legacy OCR monolith, "
            "partitioned into the 29 canonical documents with the mapped legacy "
            "assets. Guarded corrections, repaired-only asset overrides, and "
            "source-added assets are deliberately excluded. This mode proves raw "
            "monolith conservation; it is not the repaired release or an "
            "OCR-corrected edition.\n\n"
            "Do not edit this generated tree. Recreate and validate it from the "
            "repository root with exactly:\n\n"
            "```bash\n"
            "python3 goal-5/build.py --zero-corrections --output /tmp/ankos-zero-corrections\n"
            "python3 goal-5/validate.py --zero-corrections --output /tmp/ankos-zero-corrections\n"
            "```\n"
        ).encode("utf-8")

    return (
        "<!-- GENERATED FILE — DO NOT EDIT DIRECTLY. -->\n\n"
        "# A New Kind of Science — source-verified repaired Markdown\n\n"
        "This generated release contains 29 canonical book documents. Sequential "
        "source comparison and the dedicated technical, figure/caption, Index, "
        "Colophon, and saturation reviews are complete. All OCR, ordering, and "
        "serialization defects discovered by those reviews have been corrected, "
        "and zero known author-text transcription ambiguity remains open.\n\n"
        "The review was performed by agents; this edition has not been human-"
        "proofread. Literal errors actually printed in the source book are "
        "intentionally preserved. Generated navigation and image alternative text "
        "are editorial material, not author text.\n\n"
        "Do not edit this generated tree. The build uses the immutable legacy OCR "
        "monolith and assets, guarded source-verified corrections, repaired-only "
        "asset overrides, and source-added assets. Neither a previous repaired tree "
        "nor the local PDF is a build input. The PDF recorded in the source manifest "
        "is a local edition-identical review and validation witness and is not "
        "redistributed with this tree.\n\n"
        "## Build and validate\n\n"
        "From the repository root, run exactly:\n\n"
        "```bash\n"
        "python3 goal-5/build.py\n"
        "python3 goal-5/validate.py\n"
        "```\n\n"
        "Validation requires the authorized local witness identified in the source "
        "manifest.\n\n"
        "## Navigation and Goal 5 records\n\n"
        "- [Book contents](Contents.md)\n"
        "- [Goal 5 plan](../../goal-5/0-plan.md)\n"
        "- [Release record](../../goal-5/12-RELEASE.md)\n"
        "- [Source ranges and witness identity](../../goal-5/source-ranges.json)\n"
        "- [Review coverage](../../goal-5/coverage.csv)\n"
        "- [Guarded corrections](../../goal-5/corrections.jsonl)\n"
        "- [Image map](../../goal-5/image-map.jsonl)\n"
        "- [Source-added assets](../../goal-5/added-assets.jsonl)\n"
        "- [Unresolved-item register](../../goal-5/unresolved.md)\n"
        "- [Technical review](../../goal-5/9-TECHNICAL.md)\n"
        "- [Figures, Index, and Colophon review](../../goal-5/10-FIGURES-INDEX.md)\n"
        "- [Saturation review](../../goal-5/11-SATURATION.md)\n"
    ).encode("utf-8")


def contents_bytes(documents: list[dict[str, Any]]) -> bytes:
    lines = [
        "<!-- GENERATED FILE — DO NOT EDIT DIRECTLY. -->",
        "",
        "# Contents",
        "",
        "*Editorial navigation generated for this Markdown edition; not author text.*",
        "",
    ]
    for document in documents:
        path = safe_relative_path(document["output_path"], suffix=".md")
        lines.append(f"- [{document['title']}]({path.as_posix()})")
    return ("\n".join(lines) + "\n").encode("utf-8")


def _safe_output_root(output_root: Path) -> Path:
    output = output_root.resolve()
    forbidden = (REPO_ROOT.resolve(), GOAL_DIR.resolve(), LEGACY_ROOT.resolve())
    if output in forbidden or output.is_relative_to(LEGACY_ROOT.resolve()):
        raise BuildError(f"refusing unsafe output path: {output}")
    default = OUTPUT_ROOT.resolve()
    temporary_root = Path(tempfile.gettempdir()).resolve()
    if output != default and (
        output == temporary_root or not output.is_relative_to(temporary_root)
    ):
        raise BuildError("output must be the repaired sibling or a directory under /tmp")
    return output


def build(
    output_root: Path = OUTPUT_ROOT, *, zero_corrections: bool = False
) -> tuple[int, int, int]:
    raw, documents, corrections, images = load_inputs()
    added_assets = load_added_assets(documents, images)
    if zero_corrections:
        corrections = []
        added_assets = []
    rendered = document_bytes(raw, documents, corrections)
    output = _safe_output_root(output_root)
    if output != OUTPUT_ROOT.resolve() and output.exists():
        raise BuildError(f"temporary output already exists: {output}")
    temporary = output.with_name(f".{output.name}.building")
    if temporary.exists():
        shutil.rmtree(temporary)
    temporary.mkdir(parents=True)
    try:
        for relative, data in rendered.items():
            destination = temporary / Path(relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        outputs = {
            document["id"]: safe_relative_path(document["output_path"], suffix=".md")
            for document in documents
        }
        for row in images:
            source = output_image_source(
                row, use_repaired_assets=not zero_corrections
            )
            mapped = safe_relative_path(row["asset_relative_path"], suffix=".jpeg")
            destination = temporary / Path(outputs[row["document_id"]].parent) / mapped.name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        for row in added_assets:
            source = REPO_ROOT / Path(
                safe_relative_path(row["asset_relative_path"], suffix=".jpeg")
            )
            destination = (
                temporary
                / Path(outputs[row["document_id"]].parent)
                / source.name
            )
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        (temporary / "README.md").write_bytes(
            readme_bytes(zero_corrections=zero_corrections)
        )
        (temporary / "Contents.md").write_bytes(contents_bytes(documents))
        if output.exists():
            shutil.rmtree(output)
        temporary.replace(output)
    except BaseException:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise
    return len(documents), len(images) + len(added_assets), len(corrections)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT_ROOT)
    parser.add_argument(
        "--zero-corrections",
        action="store_true",
        help="ignore the correction log and reproduce the raw 29-document projection",
    )
    args = parser.parse_args()
    documents, images, corrections = build(
        args.output, zero_corrections=args.zero_corrections
    )
    mode = "raw diagnostic projection" if args.zero_corrections else "corrected release"
    print(
        f"built {mode}: documents={documents} images={images} "
        f"corrections={corrections} output={args.output.resolve()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
