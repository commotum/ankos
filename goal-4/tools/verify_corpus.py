#!/usr/bin/env python3
"""Independently verify Goal 4 corpus and source-unit artifacts."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import urllib.parse
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


GOAL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = GOAL_DIR.parent
SOURCE_REL = Path("ref/A-New-Kind-of-Science")
MANIFEST_PATH = GOAL_DIR / "corpus-manifest.json"
UNITS_PATH = GOAL_DIR / "source-units.jsonl"
CONTENTS_ENTRY = re.compile(r"^- \[[^\]]+\]\(([^)]+)\)$")
LINK_PATTERN = re.compile(
    r"(?P<image>!)?\[[^\]]*\]\("
    r"(?P<target><[^>]+>|[^)\s]+)"
    r"(?:\s+[\"'][^)]*[\"'])?\)"
)
FENCE_PATTERN = re.compile(rb"^[ \t]{0,3}(`{3,}|~{3,})")
STRUCTURAL_BOUNDARY_PATTERN = re.compile(
    rb"^(?:#{1,6}(?:\s|$)|[-+*]\s|\d+[.)]\s)"
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_units(path: Path) -> list[dict[str, Any]]:
    units: list[dict[str, Any]] = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL line {line_number}: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"source unit line {line_number} is not an object")
        units.append(value)
    return units


def expected_unit_ranges(data: bytes) -> list[tuple[int, int, int, int]]:
    """Independent block parser returning byte and line ranges."""
    lines = data.splitlines(keepends=True)
    if not lines:
        return []
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))

    result: list[tuple[int, int, int, int]] = []
    block_start = 0
    cursor = 0
    fence_char: bytes | None = None
    while cursor < len(lines):
        raw = lines[cursor].rstrip(b"\r\n")
        if (
            fence_char is None
            and cursor > block_start
            and STRUCTURAL_BOUNDARY_PATTERN.match(raw)
        ):
            result.append(
                (offsets[block_start], offsets[cursor], block_start + 1, cursor)
            )
            block_start = cursor
        marker_match = FENCE_PATTERN.match(raw)
        if marker_match:
            marker = marker_match.group(1)
            marker_char = marker[:1]
            if fence_char is None:
                fence_char = marker_char
            elif marker_char == fence_char:
                fence_char = None
        cursor += 1
        if fence_char is None and raw.strip() == b"":
            while cursor < len(lines) and lines[cursor].strip() == b"":
                cursor += 1
            result.append(
                (offsets[block_start], offsets[cursor], block_start + 1, cursor)
            )
            block_start = cursor
    if block_start < len(lines):
        result.append(
            (offsets[block_start], offsets[len(lines)], block_start + 1, len(lines))
        )
    return result


def parse_contents_independently(path: Path) -> list[str]:
    targets: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = CONTENTS_ENTRY.fullmatch(line)
        if match:
            targets.append(urllib.parse.unquote(match.group(1)))
    return targets


def normalize_link(
    source_path: Path,
    raw_target: str,
    source_root: Path,
) -> tuple[str, str | None, bool]:
    target = raw_target.strip("<>")
    if target.startswith("#"):
        return "anchor", None, True
    parsed = urllib.parse.urlsplit(target)
    if parsed.scheme or parsed.netloc or target.startswith(("mailto:", "tel:")):
        return "external", None, True
    decoded = urllib.parse.unquote(parsed.path)
    if not decoded:
        return "anchor", None, True
    resolved = (source_path.parent / decoded).resolve()
    try:
        relative = resolved.relative_to(source_root.resolve()).as_posix()
    except ValueError:
        return "outside_source", resolved.as_posix(), resolved.exists()
    suffix = resolved.suffix.lower()
    kind = (
        "image"
        if suffix == ".jpeg"
        else "document"
        if suffix == ".md"
        else "other_local"
    )
    return kind, relative, resolved.exists()


def independent_links(source_root: Path) -> list[tuple[Any, ...]]:
    records: list[tuple[Any, ...]] = []
    for path in sorted(source_root.rglob("*.md")):
        relative = path.relative_to(source_root).as_posix()
        text = path.read_text(encoding="utf-8")
        for match in LINK_PATTERN.finditer(text):
            raw = match.group("target").strip("<>")
            kind, resolved, exists = normalize_link(path, raw, source_root)
            records.append(
                (
                    relative,
                    raw,
                    bool(match.group("image")),
                    kind,
                    resolved,
                    exists,
                )
            )
    return records


def independent_tree_digest(source_root: Path) -> str:
    value = hashlib.sha256()
    for path in sorted(item for item in source_root.rglob("*") if item.is_file()):
        relative = "./" + path.relative_to(source_root).as_posix()
        value.update(f"{digest(path.read_bytes())}  {relative}\n".encode())
    return value.hexdigest()


def verify_loaded(
    manifest: dict[str, Any],
    units: list[dict[str, Any]],
    repo_root: Path,
    units_bytes: bytes | None = None,
) -> list[str]:
    errors: list[str] = []
    source_root = repo_root / SOURCE_REL

    if manifest.get("schema_version") != 1:
        errors.append("manifest schema_version must equal 1")
    counts = manifest.get("counts")
    if not isinstance(counts, dict):
        return ["manifest counts must be an object"]

    all_files = sorted(path for path in source_root.rglob("*") if path.is_file())
    markdown = [path for path in all_files if path.suffix.lower() == ".md"]
    images = [path for path in all_files if path.suffix.lower() == ".jpeg"]
    other = [
        path
        for path in all_files
        if path.suffix.lower() not in {".md", ".jpeg"}
    ]
    expected_counts = {
        "total_files": 1638,
        "markdown_files": 31,
        "navigation_documents": 2,
        "book_documents": 29,
        "images": 1607,
        "other_files": 0,
    }
    actual_independent = {
        "total_files": len(all_files),
        "markdown_files": len(markdown),
        "navigation_documents": 2,
        "book_documents": len(markdown) - 2,
        "images": len(images),
        "other_files": len(other),
    }
    if actual_independent != expected_counts:
        errors.append(
            f"physical inventory differs from frozen expected counts: {actual_independent}"
        )
    for key, value in actual_independent.items():
        if counts.get(key) != value:
            errors.append(f"manifest count {key} is stale")
    if manifest.get("source_tree_sha256") != independent_tree_digest(source_root):
        errors.append("manifest source-tree digest mismatch")

    contents_targets = parse_contents_independently(source_root / "Contents.md")
    if len(contents_targets) != 29 or len(set(contents_targets)) != 29:
        errors.append("Contents.md must contain 29 unique ordered document targets")
    physical_book_docs = {
        path.relative_to(source_root).as_posix()
        for path in markdown
        if path.name not in {"README.md", "Contents.md"}
    }
    if set(contents_targets) != physical_book_docs:
        errors.append("Contents targets do not equal the physical book-document set")

    documents = manifest.get("documents")
    if not isinstance(documents, list):
        return errors + ["manifest documents must be a list"]
    manifest_paths = [doc.get("path") for doc in documents]
    if manifest_paths != contents_targets:
        errors.append("manifest document order differs from Contents.md")
    if [doc.get("order") for doc in documents] != list(range(1, 30)):
        errors.append("manifest document order fields are not 1..29")

    kind_counts = Counter(doc.get("kind") for doc in documents)
    expected_kind_counts = {
        "publication_and_printed_contents": 1,
        "preface": 1,
        "chapter": 12,
        "general_notes": 1,
        "chapter_notes": 12,
        "index": 1,
        "colophon": 1,
    }
    if kind_counts != expected_kind_counts:
        errors.append(f"document kind counts are invalid: {dict(kind_counts)}")
    concatenated = b"".join((source_root / path).read_bytes() for path in contents_targets)
    if manifest.get("book_text_concatenated_sha256") != digest(concatenated):
        errors.append("manifest concatenated book-text digest mismatch")

    units_by_path: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for index, unit in enumerate(units, start=1):
        if unit.get("id") != f"U{index:06d}":
            errors.append(f"source unit ID/order mismatch at row {index}")
        path = unit.get("path")
        if isinstance(path, str):
            units_by_path[path].append(unit)
        else:
            errors.append(f"source unit {index} has no path")

    expected_global_line = 1
    for document in documents:
        relative = document.get("path")
        if not isinstance(relative, str):
            errors.append("document path must be a string")
            continue
        path = source_root / relative
        if not path.is_file():
            errors.append(f"document does not exist: {relative}")
            continue
        data = path.read_bytes()
        lines = data.splitlines(keepends=True)
        if document.get("sha256") != digest(data):
            errors.append(f"document hash mismatch: {relative}")
        if document.get("bytes") != len(data):
            errors.append(f"document byte count mismatch: {relative}")
        if document.get("line_count") != len(lines):
            errors.append(f"document line count mismatch: {relative}")
        if document.get("global_line_start") != expected_global_line:
            errors.append(f"document global line start mismatch: {relative}")
        expected_global_end = expected_global_line + len(lines) - 1
        if document.get("global_line_end") != expected_global_end:
            errors.append(f"document global line end mismatch: {relative}")

        expected_ranges = expected_unit_ranges(data)
        doc_units = units_by_path.get(relative, [])
        actual_ranges = [
            (
                unit.get("byte_start"),
                unit.get("byte_end"),
                unit.get("line_start"),
                unit.get("line_end"),
            )
            for unit in doc_units
        ]
        if actual_ranges != expected_ranges:
            errors.append(f"source-unit segmentation mismatch: {relative}")

        for unit in doc_units:
            byte_start = unit.get("byte_start")
            byte_end = unit.get("byte_end")
            line_start = unit.get("line_start")
            line_end = unit.get("line_end")
            if not all(
                isinstance(value, int)
                for value in (byte_start, byte_end, line_start, line_end)
            ):
                errors.append(f"source unit has non-integer range: {unit.get('id')}")
                continue
            block = data[byte_start:byte_end]
            if unit.get("sha256") != digest(block):
                errors.append(f"source unit hash mismatch: {unit.get('id')}")
            expected_global_start = expected_global_line + line_start - 1
            expected_global_end_for_unit = expected_global_line + line_end - 1
            if unit.get("global_line_start") != expected_global_start:
                errors.append(f"unit global start mismatch: {unit.get('id')}")
            if unit.get("global_line_end") != expected_global_end_for_unit:
                errors.append(f"unit global end mismatch: {unit.get('id')}")

        if document.get("unit_count") != len(doc_units):
            errors.append(f"document unit count mismatch: {relative}")
        if document.get("unit_ids") != [unit.get("id") for unit in doc_units]:
            errors.append(f"document unit ID list mismatch: {relative}")
        expected_global_line = expected_global_end + 1

    if set(units_by_path) != set(contents_targets):
        errors.append("source-unit document set is not exactly the 29 book documents")
    if counts.get("source_units") != len(units):
        errors.append("manifest source-unit count mismatch")
    if counts.get("logical_lines") != expected_global_line - 1:
        errors.append("manifest logical-line count mismatch")

    if units_bytes is not None and manifest.get("source_units_sha256") != digest(
        units_bytes
    ):
        errors.append("source-units file hash mismatch")

    image_rows = manifest.get("images")
    if not isinstance(image_rows, list):
        errors.append("manifest images must be a list")
        image_rows = []
    physical_image_paths = {
        path.relative_to(source_root).as_posix() for path in images
    }
    manifest_image_paths = {row.get("path") for row in image_rows}
    if manifest_image_paths != physical_image_paths:
        errors.append("manifest image set differs from physical image set")
    for row in image_rows:
        relative = row.get("path")
        if not isinstance(relative, str):
            errors.append("image row lacks path")
            continue
        path = source_root / relative
        if not path.is_file():
            errors.append(f"image does not exist: {relative}")
            continue
        data = path.read_bytes()
        if row.get("sha256") != digest(data):
            errors.append(f"image hash mismatch: {relative}")
        if row.get("bytes") != len(data):
            errors.append(f"image byte count mismatch: {relative}")

    manifest_links = manifest.get("links")
    if not isinstance(manifest_links, list):
        errors.append("manifest links must be a list")
        manifest_links = []
    manifest_link_tuples = [
        (
            row.get("source_path"),
            row.get("raw_target"),
            row.get("markdown_image_syntax"),
            row.get("kind"),
            row.get("resolved_path"),
            row.get("exists"),
        )
        for row in manifest_links
    ]
    independent = independent_links(source_root)
    if Counter(manifest_link_tuples) != Counter(independent):
        errors.append("manifest links differ from independent Markdown parse")
    if any(not row.get("exists") for row in manifest_links):
        errors.append("manifest contains a broken local or declared-existing link")
    if [row.get("id") for row in manifest_links] != [
        f"L{index:06d}" for index in range(1, len(manifest_links) + 1)
    ]:
        errors.append("manifest link IDs are not total canonical sequence")
    valid_units = {unit.get("id"): unit for unit in units}
    for row in manifest_links:
        source_path = row.get("source_path")
        source_unit_id = row.get("source_unit_id")
        if source_path in {"README.md", "Contents.md"}:
            if source_unit_id is not None:
                errors.append("navigation link must not claim a book source unit")
            continue
        if source_unit_id not in valid_units:
            errors.append(f"book link lacks valid source unit: {row.get('id')}")
            continue
        unit = valid_units[source_unit_id]
        if unit.get("path") != source_path:
            errors.append(f"book link source-unit path mismatch: {row.get('id')}")
            continue
        data = (source_root / source_path).read_bytes()
        block = data[unit["byte_start"] : unit["byte_end"]].decode("utf-8")
        if row.get("raw_target") not in block:
            errors.append(f"book link target is not inside claimed unit: {row.get('id')}")
    image_link_count = sum(1 for row in manifest_links if row.get("kind") == "image")
    if counts.get("image_references") != image_link_count:
        errors.append("manifest image-reference count mismatch")

    links_by_id = {row.get("id"): row for row in manifest_links}
    expected_references: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in manifest_links:
        if row.get("kind") == "image" and isinstance(row.get("resolved_path"), str):
            expected_references[row["resolved_path"]].append(
                {
                    "link_id": row.get("id"),
                    "source_path": row.get("source_path"),
                    "source_unit_id": row.get("source_unit_id"),
                }
            )
    for row in image_rows:
        expected = expected_references.get(row.get("path"), [])
        if row.get("referenced_by") != expected:
            errors.append(f"image reverse-reference mismatch: {row.get('path')}")
        if row.get("reference_count") != len(expected):
            errors.append(f"image reference count mismatch: {row.get('path')}")
        expected_status = "REFERENCED" if expected else "UNREFERENCED_PHYSICAL"
        if row.get("inventory_status") != expected_status:
            errors.append(f"image inventory status mismatch: {row.get('path')}")
        for reference in row.get("referenced_by", []):
            if reference.get("link_id") not in links_by_id:
                errors.append(f"image references unknown link: {row.get('path')}")

    doc_by_path = {doc.get("path"): doc for doc in documents}
    for relative, document in doc_by_path.items():
        expected_link_ids = [
            row.get("id")
            for row in manifest_links
            if row.get("source_path") == relative
        ]
        if document.get("link_ids") != expected_link_ids:
            errors.append(f"document link join mismatch: {relative}")
        expected_images = [
            row.get("resolved_path")
            for row in manifest_links
            if row.get("source_path") == relative and row.get("kind") == "image"
        ]
        if document.get("image_references") != expected_images:
            errors.append(f"document image-reference join mismatch: {relative}")

    navigation = manifest.get("navigation_documents")
    if not isinstance(navigation, list) or len(navigation) != 2:
        errors.append("navigation manifest must contain two documents")
    else:
        if {row.get("path") for row in navigation} != {"README.md", "Contents.md"}:
            errors.append("navigation manifest paths are invalid")
        for row in navigation:
            path = source_root / row["path"]
            data = path.read_bytes()
            if row.get("sha256") != digest(data) or row.get("bytes") != len(data):
                errors.append(f"navigation file record mismatch: {row.get('path')}")

    pairs = manifest.get("chapter_notes_pairs")
    if not isinstance(pairs, list) or len(pairs) != 12:
        errors.append("chapter/Notes pairing must contain 12 rows")
    else:
        if [row.get("chapter_number") for row in pairs] != list(range(1, 13)):
            errors.append("chapter/Notes pairing numbers are invalid")
        for row in pairs:
            if row.get("chapter_path") not in contents_targets:
                errors.append("chapter pair points outside canonical documents")
            if row.get("notes_path") not in contents_targets:
                errors.append("Notes pair points outside canonical documents")

    return errors


def mutation_checks(
    manifest: dict[str, Any],
    units: list[dict[str, Any]],
    repo_root: Path,
    units_bytes: bytes,
) -> list[str]:
    failures: list[str] = []
    mutations: list[tuple[str, dict[str, Any], list[dict[str, Any]], bytes | None]] = []

    missing_document = copy.deepcopy(manifest)
    missing_document["documents"].pop()
    mutations.append(("missing document", missing_document, units, units_bytes))

    corrupt_unit = copy.deepcopy(units)
    corrupt_unit[0]["byte_end"] += 1
    mutations.append(("corrupt source-unit range", manifest, corrupt_unit, units_bytes))

    missing_unit = copy.deepcopy(units)
    missing_unit.pop(0)
    mutations.append(("missing source-unit row", manifest, missing_unit, units_bytes))

    missing_image = copy.deepcopy(manifest)
    missing_image["images"].pop()
    mutations.append(("missing physical image row", missing_image, units, units_bytes))

    stale_link = copy.deepcopy(manifest)
    stale_link["links"][0]["exists"] = False
    mutations.append(("stale link record", stale_link, units, units_bytes))

    stale_unit_hash = copy.deepcopy(manifest)
    stale_unit_hash["source_units_sha256"] = "0" * 64
    mutations.append(("stale source-unit digest", stale_unit_hash, units, units_bytes))

    for name, changed_manifest, changed_units, changed_bytes in mutations:
        if not verify_loaded(
            changed_manifest,
            changed_units,
            repo_root,
            changed_bytes,
        ):
            failures.append(f"mutation unexpectedly passed: {name}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--units", type=Path, default=UNITS_PATH)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        units_bytes = args.units.read_bytes()
        units = load_units(args.units)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"corpus artifact load failed: {exc}", file=sys.stderr)
        return 1
    if not isinstance(manifest, dict):
        print("corpus manifest root must be an object", file=sys.stderr)
        return 1

    errors = verify_loaded(manifest, units, args.repo_root.resolve(), units_bytes)
    if args.self_test:
        errors.extend(
            mutation_checks(manifest, units, args.repo_root.resolve(), units_bytes)
        )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "verified corpus map"
        + (" and mutation checks" if args.self_test else "")
        + f": documents={len(manifest['documents'])} "
        + f"images={len(manifest['images'])} units={len(units)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
