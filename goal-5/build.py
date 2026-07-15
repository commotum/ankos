#!/usr/bin/env python3
"""Build the 29-document ANKoS baseline from the immutable OCR monolith."""

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
CORRECTIONS_PATH = GOAL_DIR / "corrections.jsonl"
SOURCE_STATUS = "USER_AUTHORIZED_LOCAL_SOURCE"
BOUNDARY_STATUS = "SOURCE_CONFIRMED"
SOURCE_PAGE_IN_ASSET = re.compile(r"_page_(\d+)_")
AUTHORITATIVE_LOCATION = re.compile(r"^pdf:(\d{4})(?:$|[; ,])")


class BuildError(ValueError):
    """An input cannot produce the promised lossless baseline."""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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

    physical_assets = {
        PurePosixPath(path.relative_to(legacy_root).as_posix())
        for path in legacy_root.rglob("*.jpeg")
    }
    if physical_assets != source_paths:
        raise BuildError("image map and physical legacy JPEG inventory differ")
    return rows


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


def readme_bytes() -> bytes:
    return (
        "# A New Kind of Science — repair worktree\n\n"
        "This directory is generated by `goal-5/build.py` from the immutable legacy "
        "OCR monolith. It is a provisional baseline projection, not yet a completely "
        "source-verified or OCR-corrected edition.\n"
    ).encode("utf-8")


def contents_bytes(documents: list[dict[str, Any]]) -> bytes:
    lines = ["# Contents", ""]
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
    if zero_corrections:
        corrections = []
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
            source = LEGACY_ROOT / Path(safe_relative_path(row["asset_relative_path"], suffix=".jpeg"))
            destination = temporary / Path(outputs[row["document_id"]].parent) / source.name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        (temporary / "README.md").write_bytes(readme_bytes())
        (temporary / "Contents.md").write_bytes(contents_bytes(documents))
        if output.exists():
            shutil.rmtree(output)
        temporary.replace(output)
    except BaseException:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise
    return len(documents), len(images), len(corrections)


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
    print(
        f"built baseline: documents={documents} images={images} "
        f"corrections={corrections} output={args.output.resolve()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
