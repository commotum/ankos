#!/usr/bin/env python3
"""Build deterministic Goal 4 corpus and source-unit manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.parse
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


TOOL_VERSION = 1
GOAL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = GOAL_DIR.parent
SOURCE_REL = Path("ref/A-New-Kind-of-Science")
CONTENTS_REL = SOURCE_REL / "Contents.md"
README_REL = SOURCE_REL / "README.md"
MANIFEST_PATH = GOAL_DIR / "corpus-manifest.json"
UNITS_PATH = GOAL_DIR / "source-units.jsonl"

CONTENTS_LINK_RE = re.compile(r"^- \[([^\]]+)\]\(([^)]+)\)$")
MARKDOWN_LINK_RE = re.compile(
    r"(?P<image>!)?\[[^\]]*\]\("
    r"(?P<target><[^>]+>|[^)\s]+)"
    r"(?:\s+[\"'][^)]*[\"'])?\)"
)
FENCE_RE = re.compile(rb"^[ \t]{0,3}(`{3,}|~{3,})")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_record(path: Path, source_root: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(source_root).as_posix(),
        "bytes": len(data),
        "sha256": sha256_bytes(data),
    }


def parse_contents(contents_path: Path) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for line in contents_path.read_text(encoding="utf-8").splitlines():
        match = CONTENTS_LINK_RE.fullmatch(line)
        if match:
            title, target = match.groups()
            entries.append(
                {
                    "title": title,
                    "path": urllib.parse.unquote(target),
                }
            )
    return entries


def line_offsets(data: bytes) -> tuple[list[bytes], list[int]]:
    lines = data.splitlines(keepends=True)
    if data and not lines:
        lines = [data]
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    return lines, offsets


def source_unit_line_ranges(data: bytes) -> list[tuple[int, int]]:
    """Return zero-based half-open line ranges covering data exactly."""
    lines, _ = line_offsets(data)
    if not lines:
        return []

    ranges: list[tuple[int, int]] = []
    start = 0
    index = 0
    fence_marker: bytes | None = None

    while index < len(lines):
        stripped = lines[index].rstrip(b"\r\n")
        fence = FENCE_RE.match(stripped)
        if fence:
            marker = fence.group(1)
            if fence_marker is None:
                fence_marker = marker[:1]
            elif marker.startswith(fence_marker * 3):
                fence_marker = None

        index += 1
        if fence_marker is None and stripped.strip() == b"":
            while index < len(lines) and lines[index].strip() == b"":
                index += 1
            ranges.append((start, index))
            start = index

    if start < len(lines):
        ranges.append((start, len(lines)))
    return ranges


def classify_block(block: bytes) -> str:
    nonblank = next(
        (line.strip() for line in block.splitlines() if line.strip()),
        b"",
    )
    if not nonblank:
        return "blank"
    if nonblank.startswith((b"```", b"~~~")):
        return "fenced_code"
    if re.match(rb"^#{1,6}(?:\s|$)", nonblank):
        return "heading"
    if nonblank.startswith(b"!["):
        return "image"
    if re.match(rb"^(?:[-+*]|\d+[.)])\s", nonblank):
        return "list"
    if nonblank.startswith(b">"):
        return "blockquote"
    if nonblank.startswith(b"|"):
        return "table"
    return "paragraph"


def normalize_target(
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

    decoded_path = urllib.parse.unquote(parsed.path)
    if not decoded_path:
        return "anchor", None, True

    resolved = (source_path.parent / decoded_path).resolve()
    try:
        relative = resolved.relative_to(source_root.resolve()).as_posix()
    except ValueError:
        return "outside_source", resolved.as_posix(), resolved.exists()

    suffix = resolved.suffix.lower()
    if suffix == ".jpeg":
        kind = "image"
    elif suffix == ".md":
        kind = "document"
    else:
        kind = "other_local"
    return kind, relative, resolved.exists()


def markdown_links(text: str) -> Iterable[tuple[bool, str]]:
    for match in MARKDOWN_LINK_RE.finditer(text):
        yield bool(match.group("image")), match.group("target").strip("<>")


def document_kind(relative_path: str) -> str:
    if relative_path == "FRONT-MATTER/00-Publication-and-Contents.md":
        return "publication_and_printed_contents"
    if relative_path == "FRONT-MATTER/01-Preface.md":
        return "preface"
    if relative_path.startswith("CHAPTERS/"):
        return "chapter"
    if relative_path == "BACK-MATTER/NOTES/00-General-Notes.md":
        return "general_notes"
    if relative_path.startswith("BACK-MATTER/NOTES/"):
        return "chapter_notes"
    if relative_path == "BACK-MATTER/Index.md":
        return "index"
    if relative_path == "BACK-MATTER/Colophon.md":
        return "colophon"
    return "unknown"


def chapter_number(relative_path: str) -> int | None:
    name = Path(relative_path).name
    match = re.match(r"^(\d{2})-", name)
    if not match:
        return None
    value = int(match.group(1))
    return value if 1 <= value <= 12 else None


def aggregate_tree_sha(source_root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in source_root.rglob("*") if item.is_file()):
        relative = "./" + path.relative_to(source_root).as_posix()
        digest.update(f"{sha256_bytes(path.read_bytes())}  {relative}\n".encode())
    return digest.hexdigest()


def build(repo_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    source_root = repo_root / SOURCE_REL
    contents_path = repo_root / CONTENTS_REL
    entries = parse_contents(contents_path)

    all_files = sorted(path for path in source_root.rglob("*") if path.is_file())
    markdown_files = [path for path in all_files if path.suffix.lower() == ".md"]
    image_files = [path for path in all_files if path.suffix.lower() == ".jpeg"]
    other_files = [
        path
        for path in all_files
        if path.suffix.lower() not in {".md", ".jpeg"}
    ]

    units: list[dict[str, Any]] = []
    documents: list[dict[str, Any]] = []
    links: list[dict[str, Any]] = []
    global_line = 1
    next_unit = 1
    next_link = 1

    unit_by_byte: dict[str, list[tuple[int, int, str]]] = defaultdict(list)

    for order, entry in enumerate(entries, start=1):
        relative_path = entry["path"]
        path = source_root / relative_path
        data = path.read_bytes()
        lines, offsets = line_offsets(data)
        document_unit_ids: list[str] = []

        for start_line, end_line in source_unit_line_ranges(data):
            unit_id = f"U{next_unit:06d}"
            next_unit += 1
            byte_start = offsets[start_line]
            byte_end = offsets[end_line]
            block = data[byte_start:byte_end]
            unit = {
                "id": unit_id,
                "document_order": order,
                "path": relative_path,
                "block_kind": classify_block(block),
                "byte_start": byte_start,
                "byte_end": byte_end,
                "line_start": start_line + 1,
                "line_end": end_line,
                "global_line_start": global_line + start_line,
                "global_line_end": global_line + end_line - 1,
                "sha256": sha256_bytes(block),
            }
            units.append(unit)
            document_unit_ids.append(unit_id)
            unit_by_byte[relative_path].append((byte_start, byte_end, unit_id))

        document_links: list[str] = []
        document_images: list[str] = []
        text = data.decode("utf-8")
        for is_image, raw_target in markdown_links(text):
            kind, resolved, exists = normalize_target(path, raw_target, source_root)
            match = MARKDOWN_LINK_RE.search(text)
            del match
            link_id = f"L{next_link:06d}"
            next_link += 1
            link_record = {
                "id": link_id,
                "source_path": relative_path,
                "source_unit_id": None,
                "raw_target": raw_target,
                "markdown_image_syntax": is_image,
                "kind": kind,
                "resolved_path": resolved,
                "exists": exists,
            }
            links.append(link_record)
            document_links.append(link_id)
            if kind == "image" and resolved is not None:
                document_images.append(resolved)

        # Bind each document link to its containing source unit by matching the
        # target token's first byte occurrence after the previous match.
        link_cursor = 0
        link_index = len(links) - len(document_links)
        for match in MARKDOWN_LINK_RE.finditer(text):
            prefix_bytes = text[: match.start()].encode("utf-8")
            byte_position = len(prefix_bytes)
            while link_cursor < len(unit_by_byte[relative_path]):
                start, end, unit_id = unit_by_byte[relative_path][link_cursor]
                if start <= byte_position < end:
                    links[link_index]["source_unit_id"] = unit_id
                    break
                link_cursor += 1
            link_index += 1

        line_count = len(lines)
        record = file_record(path, source_root)
        record.update(
            {
                "order": order,
                "title": entry["title"],
                "kind": document_kind(relative_path),
                "chapter_number": chapter_number(relative_path),
                "line_count": line_count,
                "global_line_start": global_line,
                "global_line_end": global_line + line_count - 1,
                "unit_count": len(document_unit_ids),
                "unit_ids": document_unit_ids,
                "link_ids": document_links,
                "image_references": document_images,
            }
        )
        documents.append(record)
        global_line += line_count

    # Navigation links are manifest evidence but are not Book source units.
    for nav_relative in ("README.md", "Contents.md"):
        nav_path = source_root / nav_relative
        text = nav_path.read_text(encoding="utf-8")
        for is_image, raw_target in markdown_links(text):
            kind, resolved, exists = normalize_target(
                nav_path, raw_target, source_root
            )
            links.append(
                {
                    "id": f"L{next_link:06d}",
                    "source_path": nav_relative,
                    "source_unit_id": None,
                    "raw_target": raw_target,
                    "markdown_image_syntax": is_image,
                    "kind": kind,
                    "resolved_path": resolved,
                    "exists": exists,
                }
            )
            next_link += 1

    referenced_by: dict[str, list[dict[str, str]]] = defaultdict(list)
    for link in links:
        if link["kind"] == "image" and link["resolved_path"] is not None:
            referenced_by[link["resolved_path"]].append(
                {
                    "link_id": link["id"],
                    "source_path": link["source_path"],
                    "source_unit_id": link["source_unit_id"],
                }
            )

    images: list[dict[str, Any]] = []
    for image_path in image_files:
        record = file_record(image_path, source_root)
        references = referenced_by.get(record["path"], [])
        record.update(
            {
                "reference_count": len(references),
                "referenced_by": references,
                "inventory_status": (
                    "REFERENCED" if references else "UNREFERENCED_PHYSICAL"
                ),
            }
        )
        images.append(record)

    navigation = [
        {
            **file_record(source_root / "README.md", source_root),
            "role": "source_overview",
        },
        {
            **file_record(source_root / "Contents.md", source_root),
            "role": "canonical_navigation",
        },
    ]

    pairs: list[dict[str, Any]] = []
    for number in range(1, 13):
        chapter = next(
            doc
            for doc in documents
            if doc["kind"] == "chapter" and doc["chapter_number"] == number
        )
        notes = next(
            doc
            for doc in documents
            if doc["kind"] == "chapter_notes"
            and doc["chapter_number"] == number
        )
        pairs.append(
            {
                "chapter_number": number,
                "chapter_path": chapter["path"],
                "notes_path": notes["path"],
            }
        )

    units_bytes = b"".join(
        (
            json.dumps(unit, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        for unit in units
    )

    manifest: dict[str, Any] = {
        "schema_version": 1,
        "tool_version": TOOL_VERSION,
        "source_root": SOURCE_REL.as_posix(),
        "contents_path": CONTENTS_REL.as_posix(),
        "source_tree_sha256": aggregate_tree_sha(source_root),
        "book_text_concatenated_sha256": sha256_bytes(
            b"".join((source_root / entry["path"]).read_bytes() for entry in entries)
        ),
        "source_units_sha256": sha256_bytes(units_bytes),
        "counts": {
            "total_files": len(all_files),
            "markdown_files": len(markdown_files),
            "navigation_documents": len(navigation),
            "book_documents": len(documents),
            "images": len(images),
            "other_files": len(other_files),
            "source_units": len(units),
            "logical_lines": global_line - 1,
            "links": len(links),
            "image_references": sum(
                1 for link in links if link["kind"] == "image"
            ),
            "referenced_physical_images": sum(
                1 for image in images if image["reference_count"] > 0
            ),
            "unreferenced_physical_images": sum(
                1 for image in images if image["reference_count"] == 0
            ),
        },
        "navigation_documents": navigation,
        "documents": documents,
        "chapter_notes_pairs": pairs,
        "links": links,
        "images": images,
        "other_files": [
            file_record(path, source_root) for path in other_files
        ],
        "split_anomalies": [],
    }
    return manifest, units


def serialize_units(units: list[dict[str, Any]]) -> bytes:
    return b"".join(
        (
            json.dumps(unit, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        for unit in units
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--units", type=Path, default=UNITS_PATH)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    manifest, units = build(args.repo_root.resolve())
    manifest_bytes = (
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    units_bytes = serialize_units(units)

    if args.check:
        failures: list[str] = []
        if not args.manifest.exists() or args.manifest.read_bytes() != manifest_bytes:
            failures.append(str(args.manifest))
        if not args.units.exists() or args.units.read_bytes() != units_bytes:
            failures.append(str(args.units))
        if failures:
            print("generated corpus artifacts are stale: " + ", ".join(failures))
            return 1
        print("corpus artifacts reproduce exactly")
        return 0

    args.manifest.write_bytes(manifest_bytes)
    args.units.write_bytes(units_bytes)
    print(
        "built corpus artifacts: "
        f"documents={manifest['counts']['book_documents']} "
        f"images={manifest['counts']['images']} "
        f"units={manifest['counts']['source_units']} "
        f"lines={manifest['counts']['logical_lines']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
