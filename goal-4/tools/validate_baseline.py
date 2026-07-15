#!/usr/bin/env python3
"""Validate the frozen Goal 4 Stage 2 baseline and its raw inputs."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import stat
import subprocess
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path, PurePosixPath
from typing import Any

from PIL import Image

from baseline_lib import (
    BLOCK_KIND_ENUM,
    EXPECTED_SEGMENT_SIGNATURES,
    LEGACY_GIT_TREE,
    LEGACY_RELATIVE,
    MONOLITH_RELATIVE,
    MONOLITH_SHA256,
    REPAIRED_RELATIVE,
    RISK_PRIORITY,
    SEGMENT_STARTS,
    build_corpus_manifest,
    build_detector_artifacts,
    build_held_out_sample,
    build_image_reference_ledger,
    build_known_defect_rows,
    build_routing_baseline,
    jsonl_bytes,
    line_window_signature,
    quality_manifest_material,
    split_raw_lines,
    stable_json_bytes,
    structure_ledger_rows,
)
from guardrail_lib import (
    GuardrailError,
    canonical_json_bytes,
    git_tree_identity,
    load_canonical_json,
    load_json,
    require,
    safe_relative_posix,
    sha256_bytes,
    sha256_file,
)


EXPECTED_ARTIFACTS = (
    "baseline-detector-hits.jsonl",
    "baseline-detector-report.json",
    "baseline-environment.json",
    "corpus-manifest.json",
    "held-out-sample.json",
    "image-reference-ledger.jsonl",
    "known-defect-regression.jsonl",
    "routing-baseline.json",
    "structure-ledger.jsonl",
)

# Set only after the Stage 2 source/test surface is closed. The lock excludes
# this validator itself, avoiding a circular self-hash.
EXPECTED_BASELINE_LOCK_SHA256: str | None = None
EXPECTED_ROUTING_PROJECTION_SHA256: str | None = None

MANIFEST_KEYS = {
    "contract_id",
    "counts",
    "discovery_policy",
    "duplicate_jpeg_payload_groups",
    "git",
    "legacy_root",
    "ordering",
    "path_digests",
    "path_profile",
    "quality_seed_material",
    "raw_inputs",
    "role_counts",
    "schema_version",
    "totals",
}
RAW_COMMON_KEYS = {
    "allocated_byte_size_at_capture",
    "basename",
    "byte_size",
    "file_id",
    "filesystem_mode_at_capture",
    "git_head_blob_oid",
    "git_object_format",
    "git_storage",
    "git_tree_mode",
    "image",
    "kind",
    "link_count_at_capture",
    "logical_line_count",
    "media_type",
    "relative_path",
    "role",
    "sha256",
    "text",
}
RAW_JPEG_EXTRA_KEYS = {"git_lfs_oid_sha256", "git_lfs_size"}
JPEG_IMAGE_KEYS = {
    "component_count",
    "decoded_color_mode",
    "height",
    "sample_precision",
    "sof_marker",
    "width",
}
TEXT_PROFILE_KEYS = {
    "cr_count",
    "encoding",
    "lf_count",
    "mojibake_signature_count",
    "replacement_character_count",
    "terminal_lf",
    "utf8_bom",
}

I_BLANK = lambda text: not text.strip()
I_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
I_HEADING = re.compile(r"^ {0,3}#{1,6}(?:\s|$)")
I_IMAGE = re.compile(r"^\s*!\[[^\]]*\]\([^)]*\)\s*$")
I_TABLE = re.compile(r"^\s*\|.*\|\s*$")
I_LIST = re.compile(r"^\s{0,3}(?:[-+*]|[•■])\s+")
I_QUOTE = re.compile(r"^\s{0,3}>")
I_MATH = re.compile(r"^\s*\${1,2}.*\${1,2}\s*$")
I_CAPTION = re.compile(
    r"^\s*(?:<sup>[^<]*(?:◆|■)[^<]*</sup>|(?:Figure|Figures|Picture|Pictures)\b)",
    re.IGNORECASE,
)
I_INLINE = re.compile(r"(?<!\\)\$(?!\$).*?(?<!\\)\$")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    try:
        payload = path.read_bytes()
    except OSError as error:
        raise GuardrailError(f"cannot read JSONL {path}: {error}") from error
    require(payload.endswith(b"\n"), f"JSONL lacks terminal LF: {path}")
    rows: list[dict[str, Any]] = []
    for number, raw in enumerate(payload.splitlines(keepends=True), 1):
        require(raw.endswith(b"\n"), f"JSONL row lacks LF: {path}:{number}")
        try:
            row = json.loads(raw[:-1].decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as error:
            raise GuardrailError(f"invalid JSONL row {path}:{number}: {error}") from error
        require(isinstance(row, dict), f"JSONL row is not an object: {path}:{number}")
        require(raw == stable_json_bytes(row), f"JSONL row is not canonical: {path}:{number}")
        rows.append(row)
    return rows


def _artifact_paths(artifact_root: Path) -> dict[str, Path]:
    return {name: artifact_root / name for name in EXPECTED_ARTIFACTS}


def _strict_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    require(set(value) == expected, f"{label} field set drift")


def _independent_jpeg_metadata(payload: bytes) -> dict[str, Any]:
    """Parse the JPEG marker stream and require an independently decodable image."""

    require(payload[:2] == b"\xff\xd8", "JPEG is missing SOI")
    index = 2
    frame: dict[str, Any] | None = None
    saw_scan = False
    saw_eoi = False
    sof_markers = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    while index < len(payload):
        require(payload[index] == 0xFF, "invalid JPEG marker prefix")
        marker_start = index
        while index < len(payload) and payload[index] == 0xFF:
            index += 1
        require(index < len(payload), "truncated JPEG marker")
        marker = payload[index]
        index += 1
        require(marker != 0x00, "stuffed JPEG byte outside entropy data")
        if marker == 0xD9:
            require(index == len(payload), "JPEG has bytes after EOI")
            saw_eoi = True
            break
        require(marker != 0xD8, "nested JPEG SOI marker")
        if marker in {0x01, *range(0xD0, 0xD8)}:
            continue
        require(index + 2 <= len(payload), "truncated JPEG segment length")
        length = int.from_bytes(payload[index : index + 2], "big")
        require(length >= 2 and index + length <= len(payload), "invalid JPEG segment length")
        if marker in sof_markers:
            require(frame is None, "JPEG has multiple SOF frames")
            require(length >= 8, "truncated JPEG SOF")
            precision = payload[index + 2]
            height = int.from_bytes(payload[index + 3 : index + 5], "big")
            width = int.from_bytes(payload[index + 5 : index + 7], "big")
            components = payload[index + 7]
            require(components > 0 and length == 8 + 3 * components, "invalid JPEG SOF component table")
            require(width > 0 and height > 0, "invalid JPEG dimensions")
            frame = {
                "component_count": components,
                "height": height,
                "sample_precision": precision,
                "sof_marker": f"SOF{marker - 0xC0}",
                "width": width,
            }
        if marker == 0xDA:
            components = payload[index + 2] if length >= 3 else 0
            require(components > 0 and length == 6 + 2 * components, "invalid JPEG SOS component table")
            saw_scan = True
            index += length
            while index < len(payload):
                if payload[index] != 0xFF:
                    index += 1
                    continue
                prefix = index
                while index < len(payload) and payload[index] == 0xFF:
                    index += 1
                require(index < len(payload), "truncated JPEG entropy marker")
                entropy_marker = payload[index]
                if entropy_marker == 0x00 or 0xD0 <= entropy_marker <= 0xD7:
                    index += 1
                    continue
                index = prefix
                break
            continue
        index += length
        require(index > marker_start, "JPEG parser made no progress")
    require(frame is not None and saw_scan and saw_eoi, "JPEG lacks a complete SOF/SOS/EOI stream")
    require(frame == {
        "component_count": 3,
        "height": frame["height"],
        "sample_precision": 8,
        "sof_marker": "SOF0",
        "width": frame["width"],
    }, "JPEG is not frozen 8-bit three-component SOF0")
    try:
        with Image.open(io.BytesIO(payload)) as opened:
            require(opened.format == "JPEG", "decoder did not identify JPEG")
            decoded_size = opened.size
            decoded_mode = opened.mode
            opened.verify()
        with Image.open(io.BytesIO(payload)) as decoded:
            decoded.load()
            require(decoded.size == decoded_size and decoded.mode == decoded_mode, "JPEG decode metadata changed after load")
    except (OSError, SyntaxError, ValueError) as error:
        raise GuardrailError(f"JPEG decoder rejected payload: {error}") from error
    require(decoded_size == (frame["width"], frame["height"]), "JPEG parser/decoder dimension mismatch")
    require(decoded_mode == "RGB", "JPEG decoded color-mode drift")
    return {**frame, "decoded_color_mode": decoded_mode}


def _git_blob_sha1(payload: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(payload)).encode("ascii") + b"\0" + payload).hexdigest()


def _git_output(root: Path, arguments: list[str]) -> bytes:
    result = subprocess.run(
        ["/usr/bin/git", *arguments],
        cwd=root,
        env={"PATH": "/usr/bin:/bin", "LC_ALL": "C", "LANG": "C"},
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, f"Git audit failed: {' '.join(arguments)}")
    return result.stdout


def _independent_git_lfs_checks(root: Path, manifest: dict[str, Any]) -> None:
    prefix = LEGACY_RELATIVE + "/"
    entries: dict[str, tuple[str, str]] = {}
    fields = _git_output(root, ["ls-tree", "-rz", "HEAD", "--", LEGACY_RELATIVE]).split(b"\0")
    for field in fields:
        if not field:
            continue
        metadata, encoded_path = field.split(b"\t", 1)
        mode, kind, oid = metadata.decode("ascii").split()
        path = encoded_path.decode("utf-8")
        require(kind == "blob" and path.startswith(prefix), "unexpected Git tree entry")
        entries[path[len(prefix) :]] = (mode, oid)
    require(set(entries) == {row["relative_path"] for row in manifest["raw_inputs"]}, "independent Git path-set drift")
    pointer_pattern = re.compile(
        rb"version https://git-lfs\.github\.com/spec/v1\n"
        rb"oid sha256:([0-9a-f]{64})\n"
        rb"size ([0-9]+)\n"
    )
    for row in manifest["raw_inputs"]:
        mode, oid = entries[row["relative_path"]]
        require((mode, oid) == (row["git_tree_mode"], row["git_head_blob_oid"]), f"Git entry drift: {row['relative_path']}")
        stored = _git_output(root, ["cat-file", "blob", oid])
        require(_git_blob_sha1(stored) == oid, f"Git blob identity drift: {row['relative_path']}")
        if row["kind"] == "MARKDOWN":
            require(row["git_storage"] == "DIRECT_BLOB" and sha256_bytes(stored) == row["sha256"], f"direct Git blob drift: {row['relative_path']}")
        else:
            match = pointer_pattern.fullmatch(stored)
            require(match is not None and row["git_storage"] == "LFS_POINTER_V1", f"LFS pointer drift: {row['relative_path']}")
            require(match.group(1).decode("ascii") == row["sha256"] == row["git_lfs_oid_sha256"], f"LFS OID drift: {row['relative_path']}")
            require(int(match.group(2)) == row["byte_size"] == row["git_lfs_size"], f"LFS size drift: {row['relative_path']}")


def _independent_lexical_spans(lines: list[dict[str, Any]]) -> list[tuple[int, int, str, str | None]]:
    texts = [row["content"].decode("utf-8", errors="strict") for row in lines]

    def indented(text: str) -> bool:
        return text.startswith("    ") or text.startswith("\t")

    def any_match(text: str, patterns: tuple[re.Pattern[str], ...]) -> bool:
        return any(pattern.match(text) is not None for pattern in patterns)

    spans: list[tuple[int, int, str, str | None]] = []
    position = 0
    while position < len(texts):
        begin = position
        current = texts[position]
        if I_BLANK(current):
            position += 1
            while position < len(texts) and I_BLANK(texts[position]):
                position += 1
            base = "STRUCTURE_BOUNDARY"
        elif (opened := I_FENCE.match(current)) is not None:
            token = opened.group(1)
            closing = re.compile(r"^ {0,3}" + re.escape(token[0]) + "{" + str(len(token)) + r",}\s*$")
            position += 1
            while position < len(texts) and closing.match(texts[position]) is None:
                position += 1
            require(position < len(texts), f"independent lexer found an open fence at {begin + 1}")
            position += 1
            base = "CODE_BLOCK"
        elif I_HEADING.match(current):
            position += 1
            base = "HEADING"
        elif I_IMAGE.match(current):
            position += 1
            base = "IMAGE_REFERENCE"
        elif I_TABLE.match(current):
            position += 1
            while position < len(texts) and I_TABLE.match(texts[position]):
                position += 1
            base = "DATA_TABLE"
        elif I_LIST.match(current):
            position += 1
            terminators = (I_LIST, I_HEADING, I_IMAGE, I_FENCE, I_TABLE, I_QUOTE)
            while position < len(texts) and not I_BLANK(texts[position]) and not any_match(texts[position], terminators):
                position += 1
            base = "LIST_ITEM"
        elif I_QUOTE.match(current):
            position += 1
            while position < len(texts) and I_QUOTE.match(texts[position]):
                position += 1
            base = "BLOCKQUOTE"
        elif I_MATH.match(current):
            position += 1
            base = "MATH_BLOCK"
        elif I_CAPTION.match(current):
            position += 1
            terminators = (I_HEADING, I_IMAGE, I_FENCE, I_TABLE, I_LIST, I_QUOTE)
            while position < len(texts) and not I_BLANK(texts[position]) and not any_match(texts[position], terminators):
                position += 1
            base = "CAPTION"
        elif indented(current):
            position += 1
            while position < len(texts) and indented(texts[position]):
                position += 1
            base = "CODE_BLOCK"
        else:
            position += 1
            terminators = (I_HEADING, I_IMAGE, I_FENCE, I_TABLE, I_LIST, I_QUOTE, I_MATH, I_CAPTION)
            while (
                position < len(texts)
                and not I_BLANK(texts[position])
                and not any_match(texts[position], terminators)
                and not indented(texts[position])
            ):
                position += 1
            base = "PROSE"
        kind = base
        container: str | None = None
        if base in {"PROSE", "LIST_ITEM", "BLOCKQUOTE", "CAPTION"} and any(
            I_INLINE.search(texts[number]) is not None for number in range(begin, position)
        ):
            kind = "MATH_INLINE"
            container = base
        spans.append((begin + 1, position, kind, container))
    return spans


def _independent_risk(document_id: str, kind: str) -> str:
    if document_id == "INDEX":
        return "INDEX_COLUMN_OR_ENTRY"
    if kind in {"MATH_INLINE", "MATH_BLOCK", "CODE_BLOCK", "DATA_TABLE"}:
        return "FORMULA_CODE_RULE_OR_DATA"
    if kind in {"IMAGE_REFERENCE", "CAPTION"}:
        return "FIGURE_CAPTION_OR_VISUAL"
    if kind in {"HEADING", "LIST_ITEM", "BLOCKQUOTE", "STRUCTURE_BOUNDARY"}:
        return "HEADING_LIST_OR_LAYOUT"
    require(kind == "PROSE", f"independent classifier rejects unknown kind: {kind}")
    return "PROSE"


def _validate_raw_rows(
    root: Path,
    manifest: dict[str, Any],
    raw_overrides: dict[str, Path] | None,
    *,
    legacy_root: Path | None = None,
    audit_capture_metadata: bool = False,
) -> None:
    raw_overrides = raw_overrides or {}
    _strict_keys(manifest, MANIFEST_KEYS, "manifest")
    require(manifest["schema_version"] == "1.0.0" and manifest["legacy_root"] == LEGACY_RELATIVE, "manifest identity drift")
    manifest_paths = [row["relative_path"] for row in manifest["raw_inputs"]]
    require(len(manifest_paths) == len(set(manifest_paths)) == 1463, "manifest path count/uniqueness drift")
    require(manifest_paths == sorted(manifest_paths, key=lambda item: item.encode("utf-8")), "manifest path order drift")
    require(not any(path.startswith("../") or "A-New-Kind-of-Science-Repaired" in path for path in manifest_paths), "manifest includes an unsafe/repaired path")
    actual_paths = []
    candidate = legacy_root or root / LEGACY_RELATIVE
    require(candidate.is_dir() and not candidate.is_symlink(), "legacy content root is missing or aliased")
    legacy = candidate.resolve(strict=True)
    for path in sorted(legacy.rglob("*"), key=lambda item: item.relative_to(legacy).as_posix().encode("utf-8")):
        require(not path.is_symlink(), f"legacy input symlink: {path}")
        if path.is_dir():
            continue
        require(path.is_file(), f"legacy special file: {path}")
        actual_paths.append(path.relative_to(legacy).as_posix())
    require(actual_paths == manifest_paths, "legacy exact-root path set differs from explicit manifest")
    roles: Counter[str] = Counter()
    kinds: Counter[str] = Counter()
    duplicate_payloads: dict[str, list[str]] = defaultdict(list)
    for ordinal, row in enumerate(manifest["raw_inputs"], 1):
        relative = row["relative_path"]
        expected_keys = RAW_COMMON_KEYS | (RAW_JPEG_EXTRA_KEYS if row.get("kind") == "JPEG" else set())
        _strict_keys(row, expected_keys, f"manifest raw row {ordinal}")
        safe_relative_posix(relative)
        path = raw_overrides.get(relative, legacy / Path(*PurePosixPath(relative).parts))
        require(path.is_file() and not path.is_symlink(), f"raw input is missing/aliased: {relative}")
        mode = path.stat(follow_symlinks=False).st_mode
        require(stat.S_ISREG(mode), f"raw input is not regular: {relative}")
        require(row["file_id"] == f"RAW-FILE-{ordinal:04d}" and row["basename"] == PurePosixPath(relative).name, f"raw identity drift: {relative}")
        require(row["git_object_format"] == "sha1" and re.fullmatch(r"[0-9a-f]{40}", row["git_head_blob_oid"]) is not None, f"raw Git identity format drift: {relative}")
        require(row["git_tree_mode"] == "100644", f"raw Git mode claim drift: {relative}")
        require(row["link_count_at_capture"] == 1, f"raw capture link-count claim drift: {relative}")
        if audit_capture_metadata:
            stat_result = path.stat(follow_symlinks=False)
            require(format(stat.S_IMODE(mode), "04o") == row["filesystem_mode_at_capture"], f"raw filesystem-mode drift: {relative}")
            require(stat_result.st_nlink == row["link_count_at_capture"], f"raw link-count drift: {relative}")
            require(stat_result.st_blocks * 512 == row["allocated_byte_size_at_capture"], f"raw allocation drift: {relative}")
        payload = path.read_bytes()
        require(len(payload) == row["byte_size"], f"raw byte-size drift: {relative}")
        require(sha256_bytes(payload) == row["sha256"], f"raw SHA-256 drift: {relative}")
        roles[row["role"]] += 1
        kinds[row["kind"]] += 1
        if row["kind"] == "MARKDOWN":
            text = payload.decode("utf-8", errors="strict")
            _strict_keys(row["text"], TEXT_PROFILE_KEYS, f"text profile {relative}")
            require(row["image"] is None and row["logical_line_count"] is not None and row["media_type"] == "text/markdown", f"Markdown manifest typing drift: {relative}")
            require(row["git_storage"] == "DIRECT_BLOB", f"Markdown Git-storage drift: {relative}")
            require(b"\r" not in payload and not payload.startswith(b"\xef\xbb\xbf"), f"raw text profile drift: {relative}")
            require(len(split_raw_lines(payload)) == row["logical_line_count"], f"raw logical-line drift: {relative}")
            require(payload.count(b"\n") == row["text"]["lf_count"], f"raw LF count drift: {relative}")
            require(payload.endswith(b"\n") is row["text"]["terminal_lf"], f"raw final-LF drift: {relative}")
            require(row["text"] == {
                "cr_count": 0,
                "encoding": "UTF-8",
                "lf_count": payload.count(b"\n"),
                "mojibake_signature_count": sum(text.count(marker) for marker in ("Ã", "Â", "â€", "ðŸ")),
                "replacement_character_count": text.count("\ufffd"),
                "terminal_lf": payload.endswith(b"\n"),
                "utf8_bom": False,
            }, f"raw Markdown text-profile values drift: {relative}")
        else:
            require(row["kind"] == "JPEG" and row["role"] == "LEGACY_ASSET", f"raw non-Markdown typing drift: {relative}")
            require(row["text"] is None and row["logical_line_count"] is None and row["media_type"] == "image/jpeg", f"JPEG manifest typing drift: {relative}")
            require(row["git_storage"] == "LFS_POINTER_V1", f"JPEG Git-storage drift: {relative}")
            _strict_keys(row["image"], JPEG_IMAGE_KEYS, f"JPEG profile {relative}")
            parsed = _independent_jpeg_metadata(payload)
            require(row["image"] == parsed, f"raw JPEG metadata drift: {relative}")
            require(row["git_lfs_oid_sha256"] == row["sha256"] and row["git_lfs_size"] == row["byte_size"], f"JPEG LFS claim drift: {relative}")
            duplicate_payloads[row["sha256"]].append(relative)
    require(dict(sorted(kinds.items())) == {"JPEG": 1444, "MARKDOWN": 19}, "manifest kind census drift")
    require(dict(sorted(roles.items())) == manifest["role_counts"] == {
        "INTERPRETIVE_METADATA": 1,
        "LEGACY_ASSET": 1444,
        "LEGACY_ROUTING_MARKDOWN": 17,
        "RAW_AUTHOR_TEXT_MONOLITH": 1,
    }, "manifest role census drift")
    require(manifest["counts"] == {"all_regular_files": 1463, "jpeg": 1444, "markdown": 19}, "manifest count summary drift")
    expected_duplicates = [
        {"paths": paths, "sha256": digest}
        for digest, paths in sorted(duplicate_payloads.items())
        if len(paths) > 1
    ]
    require(manifest["duplicate_jpeg_payload_groups"] == expected_duplicates, "duplicate JPEG group drift")
    markdown_paths = [row["relative_path"] for row in manifest["raw_inputs"] if row["kind"] == "MARKDOWN"]
    jpeg_paths = [row["relative_path"] for row in manifest["raw_inputs"] if row["kind"] == "JPEG"]
    def path_digest(paths: list[str]) -> str:
        return sha256_bytes(b"".join(path.encode("utf-8") + b"\n" for path in paths))
    require(manifest["path_digests"] == {
        "all_terminal_lf_sha256": path_digest(manifest_paths),
        "jpeg_terminal_lf_sha256": path_digest(jpeg_paths),
        "markdown_terminal_lf_sha256": path_digest(markdown_paths),
    }, "manifest path digest drift")
    material = json.dumps(
        [
            {key: row[key] for key in ("relative_path", "role", "byte_size", "logical_line_count", "sha256")}
            for row in manifest["raw_inputs"]
        ],
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    require(manifest["quality_seed_material"] == {
        "byte_size": len(material),
        "serialization": "UTF-8 sorted-key compact JSON array without terminal LF",
        "sha256": sha256_bytes(material),
    }, "quality seed material drift")
    require(manifest["totals"]["logical_bytes"] == sum(row["byte_size"] for row in manifest["raw_inputs"]), "manifest logical-byte total drift")
    require(manifest["totals"]["markdown_logical_lines"] == sum(row["logical_line_count"] or 0 for row in manifest["raw_inputs"]), "manifest logical-line total drift")


def _independent_structure_checks(
    root: Path,
    structure_rows: list[dict[str, Any]],
    *,
    legacy_root: Path | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    segments = [row for row in structure_rows if row.get("record_type") == "SEGMENT"]
    blocks = [row for row in structure_rows if row.get("record_type") == "RAW_BLOCK"]
    require(len(segments) == 29 and len(blocks) == 20430, "structure record counts drift")
    require([row["segment_id"] for row in segments] == [row[0] for row in SEGMENT_STARTS], "segment ID/order drift")
    legacy = legacy_root or root / LEGACY_RELATIVE
    monolith = (legacy / MONOLITH_RELATIVE).read_bytes()
    require(len(monolith) == 3780628 and sha256_bytes(monolith) == MONOLITH_SHA256, "independent monolith identity drift")
    lines = split_raw_lines(monolith)
    require(len(lines) == 22498 and monolith.count(b"\n") == 22497 and not monolith.endswith(b"\n"), "independent monolith line profile drift")
    expected_signatures = {row[0]: row[1:] for row in EXPECTED_SEGMENT_SIGNATURES}
    all_windows = [line_window_signature(lines, number) for number in range(1, len(lines) + 1)]
    all_window_counts = Counter(all_windows)
    unique_window_line = {digest: number for number, digest in enumerate(all_windows, 1) if all_window_counts[digest] == 1}
    previous_line = 0
    previous_byte = 0
    for index, (row, spec) in enumerate(zip(segments, SEGMENT_STARTS, strict=True)):
        segment_id, start_line, marker = spec
        end_line = SEGMENT_STARTS[index + 1][1] - 1 if index + 1 < len(SEGMENT_STARTS) else 22498
        require(row["raw_start_line"] == start_line and row["raw_end_line"] == end_line, f"segment range drift: {segment_id}")
        require(lines[start_line - 1]["content"].decode("utf-8") == marker, f"segment marker drift: {segment_id}")
        start_byte = lines[start_line - 1]["byte_start"]
        end_byte = lines[end_line - 1]["byte_end"]
        require(start_line == previous_line + 1 and start_byte == previous_byte, f"segment gap/overlap: {segment_id}")
        require(row["raw_start_byte"] == start_byte and row["raw_end_byte_exclusive"] == end_byte, f"segment byte range drift: {segment_id}")
        require(row["raw_segment_sha256"] == sha256_bytes(monolith[start_byte:end_byte]), f"segment hash drift: {segment_id}")
        observed = (row["signature"]["start_sha256"], row["signature"]["end_sha256"])
        require(observed == expected_signatures[segment_id], f"segment frozen signature drift: {segment_id}")
        require(all_window_counts[observed[0]] == all_window_counts[observed[1]] == 1, f"segment signature is not globally unique: {segment_id}")
        require((unique_window_line[observed[0]], unique_window_line[observed[1]]) == (start_line, end_line), f"segment signatures map to different focal lines: {segment_id}")
        require(row["boundary_status"] == "PROPOSED_RAW_BOUNDARY_PENDING_STAGE_3_5_WITNESS_VALIDATION", "Stage 2 boundary falsely claims witness authority")
        previous_line = end_line
        previous_byte = end_byte
    require(previous_line == 22498 and previous_byte == len(monolith), "segment final edge drift")
    lexical_spans = _independent_lexical_spans(lines)
    require(len(lexical_spans) == len(blocks), "independent raw lexer block-count drift")
    segment_by_id = {row["segment_id"]: row for row in segments}
    previous_line = 0
    previous_byte = 0
    kind_census: Counter[str] = Counter()
    risk_census: Counter[str] = Counter()
    for ordinal, (row, lexical) in enumerate(zip(blocks, lexical_spans, strict=True), 1):
        lexical_start, lexical_end, lexical_kind, lexical_container = lexical
        require(row["raw_block_id"] == f"RAW-{ordinal:06d}" and row["order"] == ordinal, "raw block ID/order drift")
        require(row["block_kind"] in BLOCK_KIND_ENUM, "raw block kind is outside frozen enum")
        require(row["risk_stratum"] in RISK_PRIORITY, "raw block risk is outside frozen enum")
        require(
            (row["start_line"], row["end_line"], row["block_kind"], row["container_kind"])
            == (lexical_start, lexical_end, lexical_kind, lexical_container),
            f"raw block independent lexical classification drift: {row['raw_block_id']}",
        )
        require(row["start_line"] == previous_line + 1 and row["start_byte"] == previous_byte, "raw block gap/overlap")
        require(row["end_line"] >= row["start_line"] and row["end_byte_exclusive"] > row["start_byte"], "raw block has invalid extent")
        require(row["start_byte"] == lines[row["start_line"] - 1]["byte_start"], f"raw block start line/byte mismatch: {row['raw_block_id']}")
        require(row["end_byte_exclusive"] == lines[row["end_line"] - 1]["byte_end"], f"raw block end line/byte mismatch: {row['raw_block_id']}")
        require(row["line_count"] == row["end_line"] - row["start_line"] + 1, f"raw block line-count drift: {row['raw_block_id']}")
        payload = monolith[row["start_byte"] : row["end_byte_exclusive"]]
        require(len(payload) == row["byte_size"] and sha256_bytes(payload) == row["raw_sha256"], "raw block bytes/hash drift")
        require(row["terminal_lf"] is payload.endswith(b"\n"), "raw block LF flag drift")
        owner = segment_by_id[row["segment_id"]]
        require(owner["raw_start_line"] <= row["start_line"] <= row["end_line"] <= owner["raw_end_line"], "raw block crosses segment")
        require(row["canonical_document_id"] == owner["segment_id"] and row["canonical_path"] == owner["canonical_path"], f"raw block canonical owner drift: {row['raw_block_id']}")
        require(row["risk_stratum"] == _independent_risk(owner["segment_id"], row["block_kind"]), f"raw block risk classification drift: {row['raw_block_id']}")
        kind_census[row["block_kind"]] += 1
        risk_census[row["risk_stratum"]] += 1
        previous_line = row["end_line"]
        previous_byte = row["end_byte_exclusive"]
    require(previous_line == 22498 and previous_byte == len(monolith), "raw block final edge drift")
    require(dict(sorted(kind_census.items())) == {
        "BLOCKQUOTE": 8,
        "CAPTION": 11,
        "CODE_BLOCK": 254,
        "DATA_TABLE": 45,
        "HEADING": 286,
        "IMAGE_REFERENCE": 1444,
        "LIST_ITEM": 1279,
        "MATH_BLOCK": 135,
        "MATH_INLINE": 1075,
        "PROSE": 6050,
        "STRUCTURE_BOUNDARY": 9843,
    }, "raw block kind census drift")
    require(dict(sorted(risk_census.items())) == {
        "FIGURE_CAPTION_OR_VISUAL": 1455,
        "FORMULA_CODE_RULE_OR_DATA": 1474,
        "HEADING_LIST_OR_LAYOUT": 10681,
        "INDEX_COLUMN_OR_ENTRY": 1468,
        "PROSE": 5352,
    }, "raw block risk census drift")
    return segments, blocks


def _independent_sample_ids(
    manifest: dict[str, Any],
    blocks: list[dict[str, Any]],
    contract: dict[str, Any],
    quality: dict[str, Any],
) -> tuple[str, list[str], list[dict[str, Any]]]:
    projection = [
        {key: row[key] for key in ("relative_path", "role", "byte_size", "logical_line_count", "sha256")}
        for row in manifest["raw_inputs"]
    ]
    material = json.dumps(projection, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    seed_bytes = hashlib.sha256(bytes.fromhex(quality["seed"]["domain_separator_hex"]) + material).digest()
    seed = seed_bytes.hex()
    ranked: dict[tuple[str, str], list[tuple[int, str, str]]] = defaultdict(list)
    for block in blocks:
        framed = (
            seed_bytes
            + b"\0"
            + block["canonical_document_id"].encode()
            + b"\0"
            + block["risk_stratum"].encode()
            + b"\0"
            + block["raw_block_id"].encode()
        )
        digest = hashlib.sha256(framed).hexdigest()
        ranked[(block["canonical_document_id"], block["risk_stratum"])].append((int(digest, 16), block["raw_block_id"], digest))
    chosen: list[str] = []
    allocations: list[dict[str, Any]] = []
    for document in contract["canonical_documents"]:
        document_id = document["id"]
        populations = {stratum: len(ranked[(document_id, stratum)]) for stratum in RISK_PRIORITY}
        population = sum(populations.values())
        quota = min(population, max((population + 19) // 20, 20))
        allocation = {stratum: 0 for stratum in RISK_PRIORITY}
        available = quota
        for stratum in RISK_PRIORITY:
            if stratum != "PROSE" and populations[stratum] and available:
                allocation[stratum] = 1
                available -= 1
        capacities = {stratum: populations[stratum] - allocation[stratum] for stratum in RISK_PRIORITY}
        capacity_total = sum(capacities.values())
        if available:
            ideals = {stratum: Fraction(available * capacities[stratum], capacity_total) for stratum in RISK_PRIORITY}
            for stratum in RISK_PRIORITY:
                allocation[stratum] += ideals[stratum].numerator // ideals[stratum].denominator
            residual = quota - sum(allocation.values())
            remainder_order = sorted(
                RISK_PRIORITY,
                key=lambda stratum: (-(ideals[stratum] - int(ideals[stratum])), RISK_PRIORITY.index(stratum), stratum),
            )
            for stratum in remainder_order[:residual]:
                allocation[stratum] += 1
        require(sum(allocation.values()) == quota, "independent Hamilton allocation drift")
        for stratum in RISK_PRIORITY:
            items = sorted(ranked[(document_id, stratum)])
            chosen.extend(item[1] for item in items[: allocation[stratum]])
        allocations.append({"canonical_document_id": document_id, "population": population, "populations": populations, "quota": quota, "allocations": allocation})
    return seed, chosen, allocations


def _independent_rankings(
    seed_hex: str,
    blocks: list[dict[str, Any]],
    contract: dict[str, Any],
    selected_ids: list[str],
) -> list[dict[str, Any]]:
    seed = bytes.fromhex(seed_hex)
    grouped: dict[tuple[str, str], list[tuple[int, str, str]]] = defaultdict(list)
    for block in blocks:
        framed = (
            seed
            + b"\0"
            + block["canonical_document_id"].encode("utf-8")
            + b"\0"
            + block["risk_stratum"].encode("utf-8")
            + b"\0"
            + block["raw_block_id"].encode("utf-8")
        )
        digest = hashlib.sha256(framed).hexdigest()
        grouped[(block["canonical_document_id"], block["risk_stratum"])].append(
            (int(digest, 16), block["raw_block_id"], digest)
        )
    selected = set(selected_ids)
    require(len(selected) == len(selected_ids), "independent sample contains duplicate selected IDs")
    rankings: list[dict[str, Any]] = []
    for document in contract["canonical_documents"]:
        document_id = document["id"]
        for stratum in RISK_PRIORITY:
            for position, (_, raw_block_id, digest) in enumerate(sorted(grouped[(document_id, stratum)]), 1):
                rankings.append(
                    {
                        "canonical_document_id": document_id,
                        "position_in_stratum": position,
                        "rank_sha256": digest,
                        "raw_block_id": raw_block_id,
                        "risk_stratum": stratum,
                        "selected": raw_block_id in selected,
                    }
                )
    return rankings


I_IMAGE_REFERENCE = re.compile(r"!\[[^\]\n]*\]\((?:<)?([^)>\n]+?\.jpeg)(?:>)?(?:\s+[^)\n]+)?\)")
I_CONTENT_LINK = re.compile(r"(?<!!)\[([^\]\n]+)\]\(([^)\n]+\.md)\)")


def _independent_image_references(payload: bytes) -> list[dict[str, Any]]:
    references: list[dict[str, Any]] = []
    for line in split_raw_lines(payload):
        text = line["content"].decode("utf-8", errors="strict")
        for match in I_IMAGE_REFERENCE.finditer(text):
            target = match.group(1).strip()
            references.append(
                {
                    "basename": PurePosixPath(target).name,
                    "line": line["line"],
                    "line_sha256": sha256_bytes(payload[line["byte_start"] : line["byte_end"]]),
                    "target": target,
                }
            )
    return references


def _owner_for_line(segments: list[dict[str, Any]], line: int) -> dict[str, Any]:
    owners = [row for row in segments if row["raw_start_line"] <= line <= row["raw_end_line"]]
    require(len(owners) == 1, f"line has no unique segment owner: {line}")
    return owners[0]


def _block_id_for_line(blocks: list[dict[str, Any]], line: int) -> str:
    owners = [row for row in blocks if row["start_line"] <= line <= row["end_line"]]
    require(len(owners) == 1, f"line has no unique block owner: {line}")
    return owners[0]["raw_block_id"]


def _independent_image_checks(
    legacy: Path,
    manifest: dict[str, Any],
    segments: list[dict[str, Any]],
    blocks: list[dict[str, Any]],
    image_rows: list[dict[str, Any]],
) -> None:
    assets = [row for row in manifest["raw_inputs"] if row["kind"] == "JPEG"]
    asset_by_basename = {row["basename"]: row for row in assets}
    require(len(asset_by_basename) == len(assets) == 1444, "independent asset basename census drift")
    split_by_basename: dict[str, list[dict[str, Any]]] = defaultdict(list)
    routing_sources = [row for row in manifest["raw_inputs"] if row["role"] == "LEGACY_ROUTING_MARKDOWN"]
    for source in routing_sources:
        source_path = legacy / Path(*PurePosixPath(source["relative_path"]).parts)
        for reference in _independent_image_references(source_path.read_bytes()):
            candidate = (source_path.parent / Path(*PurePosixPath(reference["target"]).parts)).resolve(strict=True)
            require(candidate.is_relative_to(legacy) and candidate.is_file() and not candidate.is_symlink(), f"split image target escapes/is missing: {source['relative_path']}:{reference['line']}")
            resolved = candidate.relative_to(legacy).as_posix()
            require(reference["basename"] in asset_by_basename, f"split reference has no asset: {reference['basename']}")
            require(resolved == asset_by_basename[reference["basename"]]["relative_path"], f"split target/asset join drift: {reference['basename']}")
            split_by_basename[reference["basename"]].append(
                {
                    "line": reference["line"],
                    "line_sha256": reference["line_sha256"],
                    "path": source["relative_path"],
                    "resolved_asset_path": resolved,
                    "target": reference["target"],
                }
            )
    monolith_path = legacy / MONOLITH_RELATIVE
    monolith_refs = _independent_image_references(monolith_path.read_bytes())
    require(len(monolith_refs) == 1444 and sum(map(len, split_by_basename.values())) == 1441, "independent image-reference census drift")
    require(len(image_rows) == len(monolith_refs), "image ledger row count drift")
    expected_keys = {
        "asset_byte_size", "asset_file_id", "asset_height", "asset_relative_path", "asset_sha256", "asset_width",
        "basename", "canonical_document_id", "monolith_direct_target_resolves", "monolith_line", "monolith_line_sha256",
        "monolith_target", "raw_block_id", "raw_reference_ordinal", "record_type", "schema_version", "split_references", "split_status",
    }
    for ordinal, (row, reference) in enumerate(zip(image_rows, monolith_refs, strict=True), 1):
        _strict_keys(row, expected_keys, f"image ledger row {ordinal}")
        asset = asset_by_basename[reference["basename"]]
        owner = _owner_for_line(segments, reference["line"])
        split_references = sorted(split_by_basename.get(reference["basename"], []), key=lambda item: (item["path"], item["line"]))
        require(len(split_references) <= 1, f"duplicate split reference: {reference['basename']}")
        direct = monolith_path.parent / Path(*PurePosixPath(reference["target"]).parts)
        expected = {
            "asset_byte_size": asset["byte_size"],
            "asset_file_id": asset["file_id"],
            "asset_height": asset["image"]["height"],
            "asset_relative_path": asset["relative_path"],
            "asset_sha256": asset["sha256"],
            "asset_width": asset["image"]["width"],
            "basename": reference["basename"],
            "canonical_document_id": owner["segment_id"],
            "monolith_direct_target_resolves": direct.is_file(),
            "monolith_line": reference["line"],
            "monolith_line_sha256": reference["line_sha256"],
            "monolith_target": reference["target"],
            "raw_block_id": _block_id_for_line(blocks, reference["line"]),
            "raw_reference_ordinal": ordinal,
            "record_type": "IMAGE_REFERENCE",
            "schema_version": "1.0.0",
            "split_references": split_references,
            "split_status": "PRESENT" if split_references else "OMITTED",
        }
        require(row == expected, f"independent image ledger drift at ordinal {ordinal}")
    require(not any(row["monolith_direct_target_resolves"] for row in image_rows), "a monolith image target unexpectedly resolves")
    require(
        [(row["raw_reference_ordinal"], row["monolith_line"], row["basename"]) for row in image_rows if row["split_status"] == "OMITTED"]
        == [
            (24, 680, "_page_66_Picture_0.jpeg"),
            (134, 1711, "_page_154_Figure_2.jpeg"),
            (135, 1744, "_page_156_Figure_1.jpeg"),
        ],
        "independent split-image omission drift",
    )


def _span_bytes(payload: bytes, start_line: int, end_line: int) -> bytes:
    lines = split_raw_lines(payload)
    require(1 <= start_line <= end_line <= len(lines), "line span is outside source")
    return payload[lines[start_line - 1]["byte_start"] : lines[end_line - 1]["byte_end"]]


def _independent_routing_checks(
    legacy: Path,
    manifest: dict[str, Any],
    segments: list[dict[str, Any]],
    image_rows: list[dict[str, Any]],
    routing: dict[str, Any],
) -> None:
    expected_top = {
        "atlas", "consumer_compatibility_baseline", "contents_links", "fence_delimiters", "image_references",
        "nonrouting_link_shapes", "omitted_transition_or_malformed_raw_lines", "routing_files", "routing_spans",
        "schema_version", "textual_evidence_limit",
    }
    _strict_keys(routing, expected_top, "routing baseline")
    require(routing["schema_version"] == "1.0.0", "routing schema drift")
    inputs = {row["relative_path"]: row for row in manifest["raw_inputs"]}
    route_sources = [row for row in manifest["raw_inputs"] if row["role"] == "LEGACY_ROUTING_MARKDOWN"]
    require(len(route_sources) == 17, "routing source count drift")
    expected_files = []
    for source in route_sources:
        payload = (legacy / Path(*PurePosixPath(source["relative_path"]).parts)).read_bytes()
        expected_files.append(
            {
                "byte_size": len(payload),
                "image_reference_count": len(_independent_image_references(payload)),
                "logical_line_count": len(split_raw_lines(payload)),
                "path": source["relative_path"],
                "sha256": sha256_bytes(payload),
                "terminal_lf": payload.endswith(b"\n"),
            }
        )
    require(routing["routing_files"] == expected_files, "independent routing-file ledger drift")
    atlas = inputs["ANKoS-Atlas.md"]
    require(routing["atlas"] == {
        "byte_size": atlas["byte_size"],
        "image_reference_count": 0,
        "logical_line_count": atlas["logical_line_count"],
        "path": "ANKoS-Atlas.md",
        "role": "INTERPRETIVE_METADATA",
        "sha256": atlas["sha256"],
        "terminal_lf": atlas["text"]["terminal_lf"],
        "textual_witness_allowed": False,
    }, "Atlas role/identity drift")
    monolith = (legacy / MONOLITH_RELATIVE).read_bytes()
    route_spans = routing["routing_spans"]
    require(len(route_spans) == 32 and [row["route_id"] for row in route_spans] == [f"ROUTE-{number:03d}" for number in range(1, 33)], "routing span identity drift")
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in route_spans:
        grouped[row["source_path"]].append(row)
        source = inputs[row["source_path"]]
        payload = (legacy / Path(*PurePosixPath(row["source_path"]).parts)).read_bytes()
        split_span = _span_bytes(payload, row["split_start_line"], row["split_end_line"])
        require(row["source_sha256"] == source["sha256"], f"routing source hash drift: {row['route_id']}")
        require(row["split_span_byte_size"] == len(split_span) and row["split_span_sha256"] == sha256_bytes(split_span), f"routing split span drift: {row['route_id']}")
        if row["raw_start_line"] is None:
            require(row["raw_end_line"] is None and row["raw_span_byte_size"] is None and row["raw_span_sha256"] is None, f"generated route has a raw projection: {row['route_id']}")
            require(row["target_document_id"] == "GENERATED_METADATA" and row["disposition"] == "GENERATED_NAVIGATION_NO_AUTHOR_TEXT_PROJECTION", "generated Contents route drift")
        else:
            raw_span = _span_bytes(monolith, row["raw_start_line"], row["raw_end_line"])
            require(row["raw_span_byte_size"] == len(raw_span) and row["raw_span_sha256"] == sha256_bytes(raw_span), f"routing raw span drift: {row['route_id']}")
            start_owner = _owner_for_line(segments, row["raw_start_line"])["segment_id"]
            end_owner = _owner_for_line(segments, row["raw_end_line"])["segment_id"]
            require(start_owner == end_owner == row["target_document_id"], f"routing raw owner drift: {row['route_id']}")
    for source in route_sources:
        spans = grouped[source["relative_path"]]
        require(spans and spans[0]["split_start_line"] == 1 and spans[-1]["split_end_line"] == source["logical_line_count"], f"routing split edge drift: {source['relative_path']}")
        require(all(left["split_end_line"] + 1 == right["split_start_line"] for left, right in zip(spans, spans[1:])), f"routing split gap/overlap: {source['relative_path']}")
    require(sum(row["raw_start_line"] is not None for row in route_spans) == 31, "raw routing span count drift")
    contents_relative = "FRONT-MATTER/Contents/Contents.md"
    contents_path = legacy / contents_relative
    expected_links: list[dict[str, Any]] = []
    semantic_by_label = {
        "The Principle of Computational Equivalence": "TARGET_CONTAINS_GENERAL_AND_CHAPTER_NOTES",
        "Notes": "TARGET_IS_ONE_STRAY_N03_SENTENCE",
        "Index": "TARGET_CONTAINS_NOTES_AND_NO_ACTUAL_INDEX",
        "Colophon": "TARGET_BEGINS_IN_N10_AND_ACTUAL_COLOPHON_IS_AT_LINE_5015",
    }
    for line in split_raw_lines(contents_path.read_bytes()):
        for match in I_CONTENT_LINK.finditer(line["content"].decode("utf-8")):
            label, target = match.groups()
            resolved = (contents_path.parent / Path(*PurePosixPath(target).parts)).resolve(strict=True)
            require(resolved.is_relative_to(legacy) and resolved.is_file() and not resolved.is_symlink(), f"Contents link fails lexical resolution: {line['line']}")
            relative = resolved.relative_to(legacy).as_posix()
            expected_links.append({
                "label": label,
                "lexically_resolves": True,
                "line": line["line"],
                "resolved_path": relative,
                "semantic_route_status": semantic_by_label.get(label, "NOMINAL_TARGET_MATCHES_DOCUMENT"),
                "target": target,
                "target_sha256": inputs[relative]["sha256"],
            })
    require(routing["contents_links"] == expected_links and len(expected_links) == 16, "Contents link ledger drift")
    require(sum(row["semantic_route_status"] != "NOMINAL_TARGET_MATCHES_DOCUMENT" for row in expected_links) == 4, "Contents semantic anomaly count drift")
    fence_counts = {
        row["relative_path"]: sum(
            re.match(rb"^ {0,3}(`{3,}|~{3,})", line["content"]) is not None
            for line in split_raw_lines((legacy / Path(*PurePosixPath(row["relative_path"]).parts)).read_bytes())
        )
        for row in manifest["raw_inputs"]
        if row["kind"] == "MARKDOWN"
    }
    require(routing["fence_delimiters"] == {
        "all_markdown_count": sum(fence_counts.values()),
        "by_path": dict(sorted(fence_counts.items())),
        "monolith_count": fence_counts[MONOLITH_RELATIVE],
    }, "fence delimiter census drift")
    omissions = [
        {
            "asset_sha256": row["asset_sha256"],
            "basename": row["basename"],
            "canonical_document_id": row["canonical_document_id"],
            "monolith_line": row["monolith_line"],
            "raw_reference_ordinal": row["raw_reference_ordinal"],
        }
        for row in image_rows
        if row["split_status"] == "OMITTED"
    ]
    image_summary = routing["image_references"]
    require(image_summary["split_omissions"] == omissions and image_summary["monolith_count"] == 1444 and image_summary["split_count"] == 1441, "routing image summary drift")
    require(image_summary["all_monolith_targets_broken_relative_to_monolith"] is True and image_summary["monolith_source_sha256"] == sha256_bytes(monolith), "routing monolith image claim drift")
    for row in routing["nonrouting_link_shapes"]["rows"]:
        require(row["line_sha256"] == sha256_bytes(_span_bytes(monolith, row["line"], row["line"])), "nonrouting link-shape hash drift")
    require([row["line"] for row in routing["nonrouting_link_shapes"]["rows"]] == [15347, 16774, 17356, 18922, 20385], "nonrouting link-shape line drift")
    expected_omitted = [(398, 399), (1368, 1369), (2700, 2701), (6586, 6587), (12083, 12084), (12086, 12088), (17443, 17443)]
    require([tuple(row["lines"]) for row in routing["omitted_transition_or_malformed_raw_lines"]] == expected_omitted, "omitted transition range drift")
    for row in routing["omitted_transition_or_malformed_raw_lines"]:
        require(row["raw_span_sha256"] == sha256_bytes(_span_bytes(monolith, *row["lines"])), "omitted transition hash drift")


def _independent_defect_checks(
    legacy: Path,
    artifact_root: Path,
    manifest: dict[str, Any],
    segments: list[dict[str, Any]],
    blocks: list[dict[str, Any]],
    image_rows: list[dict[str, Any]],
    routing: dict[str, Any],
    defect_rows: list[dict[str, Any]],
    detector_hits: list[dict[str, Any]],
    detector_report: dict[str, Any],
) -> None:
    require(len(defect_rows) == 55 and [row["sentinel_id"] for row in defect_rows] == [f"DEFECT-{number:04d}" for number in range(1, 56)], "known-defect identity drift")
    inputs = {row["relative_path"]: row for row in manifest["raw_inputs"]}
    image_by_line = {row["monolith_line"]: row for row in image_rows}
    for row in defect_rows:
        require(row["schema_version"] == "1.0.0" and row["repair_authorized"] is False, f"known defect authorizes repair: {row['sentinel_id']}")
        require(row["exact_regression_detector"] == "D13_EXACT_SENTINEL" and row["candidate_detector_routes"], f"known defect detector route drift: {row['sentinel_id']}")
        require(row["closure_stages"] == ["40-SATURATION", "42-RELEASE"], f"known defect closure route drift: {row['sentinel_id']}")
        require(set(row["primary_content_stages"]) <= set(row["workflow_stages"]) and set(row["specialist_stages"]) <= set(row["workflow_stages"]), f"known defect workflow route drift: {row['sentinel_id']}")
        if row["sentinel_kind"] == "EXACT_RAW_SPAN":
            source = inputs[row["source_path"]]
            payload = (legacy / Path(*PurePosixPath(row["source_path"]).parts)).read_bytes()
            lines = split_raw_lines(payload)
            span = _span_bytes(payload, row["raw_start_line"], row["raw_end_line"])
            start_text = lines[row["raw_start_line"] - 1]["content"].decode("utf-8")
            end_text = lines[row["raw_end_line"] - 1]["content"].decode("utf-8")
            require(row["raw_source_sha256"] == source["sha256"] and row["raw_source_role"] == source["role"], f"known defect source drift: {row['sentinel_id']}")
            require(row["raw_span_byte_size"] == len(span) and row["raw_span_sha256"] == sha256_bytes(span) and row["raw_span_occurrence_count"] == payload.count(span), f"known defect span drift: {row['sentinel_id']}")
            require(row["start_line_prefix"] == start_text[:160] and row["start_line_suffix"] == start_text[-160:] and row["end_line_prefix"] == end_text[:160] and row["end_line_suffix"] == end_text[-160:], f"known defect text sentinel drift: {row['sentinel_id']}")
            if row["source_path"] == MONOLITH_RELATIVE:
                owner = _owner_for_line(segments, row["raw_start_line"])["segment_id"]
                require(_owner_for_line(segments, row["raw_end_line"])["segment_id"] == owner == row["owner_document_id"], f"known defect monolith owner drift: {row['sentinel_id']}")
                expected_blocks = [block["raw_block_id"] for block in blocks if block["start_line"] <= row["raw_end_line"] and block["end_line"] >= row["raw_start_line"]]
                require(row["raw_block_ids"] == expected_blocks, f"known defect raw-block route drift: {row['sentinel_id']}")
            else:
                matching_routes = [route for route in routing["routing_spans"] if route["source_path"] == row["source_path"] and route["split_start_line"] <= row["raw_start_line"] <= route["split_end_line"]]
                require(len(matching_routes) == 1 and matching_routes[0]["target_document_id"] == row["owner_document_id"], f"known defect split owner drift: {row['sentinel_id']}")
            if "image_reference" in row:
                image = image_by_line[row["raw_start_line"]]
                require(row["image_reference"] == {"basename": image["basename"], "raw_reference_ordinal": image["raw_reference_ordinal"], "split_status": image["split_status"]}, f"known defect image route drift: {row['sentinel_id']}")
        else:
            require(row["sentinel_kind"] == "AGGREGATE_GUARDRAIL", f"unknown known-defect kind: {row['sentinel_id']}")
            artifact_path = row["artifact_path"]
            if artifact_path == "ANKoS-Atlas.md":
                expected_hash = inputs[artifact_path]["sha256"]
            else:
                expected_hash = sha256_file(artifact_root / PurePosixPath(artifact_path).name)
            require(row["artifact_sha256"] == expected_hash, f"aggregate defect artifact binding drift: {row['sentinel_id']}")
    exact_hits = [row for row in detector_hits if row["detector_id"] == "D13_EXACT_SENTINEL"]
    require(len(exact_hits) == len(defect_rows), "exact sentinel detector coverage drift")
    by_route = {row["route"]: row for row in exact_hits}
    require(set(by_route) == {row["sentinel_id"] for row in defect_rows}, "exact sentinel detector route drift")
    for defect in defect_rows:
        hit = by_route[defect["sentinel_id"]]
        require(hit["source_path"] == defect.get("source_path", defect.get("artifact_path")) and hit["start_line"] == defect.get("raw_start_line") and hit["end_line"] == defect.get("raw_end_line"), f"exact sentinel hit location drift: {defect['sentinel_id']}")
        require(hit["fingerprint_sha256"] == defect.get("raw_span_sha256", defect.get("artifact_sha256")) and hit["raw_block_ids"] == defect["raw_block_ids"], f"exact sentinel hit fingerprint drift: {defect['sentinel_id']}")
    require([row["hit_id"] for row in detector_hits] == [f"HIT-{number:06d}" for number in range(1, len(detector_hits) + 1)], "detector hit ID/order drift")
    require(all(row["repair_authorized"] is False for row in detector_hits), "baseline detector hit authorizes repair")
    registry = detector_report["known_defect_registry"]
    require(detector_report["repairs_applied"] == 0 and detector_report["baseline_only"] is True and registry["unrouted_count"] == 0, "detector report repair/routing claim drift")
    require(registry["exact_presence_count"] == registry["exact_presence_denominator"] == 55 and registry["registry_sha256"] == sha256_bytes(jsonl_bytes(defect_rows)), "detector report exact-registry binding drift")
    generic_locations: dict[tuple[str, int | None], set[str]] = defaultdict(set)
    for hit in detector_hits:
        if hit["detector_id"] != "D13_EXACT_SENTINEL":
            generic_locations[(hit["source_path"], hit["start_line"])].add(hit["detector_id"])
    expected_routes = []
    for defect in defect_rows:
        generic = sorted(generic_locations[(defect.get("source_path", defect.get("artifact_path", "")), defect.get("raw_start_line"))])
        expected_routes.append({
            "generic_detector_ids": generic,
            "route_kind": "GENERIC_DETECTOR_PLUS_EXACT_REGRESSION" if generic else "EXACT_REGRESSION_MANUAL_ROUTE",
            "sentinel_id": defect["sentinel_id"],
        })
    require(registry["routes"] == expected_routes, "detector report known-defect routes drift")
    generic_count = sum(bool(row["generic_detector_ids"]) for row in expected_routes)
    require(registry["generic_candidate_recall_numerator"] == generic_count and registry["generic_candidate_recall_denominator"] == 55 and registry["manual_exact_route_count"] == 55 - generic_count, "detector generic-recall accounting drift")


def _validate_lock(root: Path, artifact_root: Path, lock: dict[str, Any]) -> None:
    require(lock.get("schema_version") == "1.0.0" and lock.get("status") == "FROZEN_STAGE_2_BASELINE", "baseline lock state drift")
    expected_paths = [f"goal-4/{name}" for name in EXPECTED_ARTIFACTS]
    require([row["path"] for row in lock["artifacts"]] == expected_paths, "baseline lock artifact scope drift")
    for row in lock["artifacts"]:
        path = artifact_root / Path(row["path"]).name
        require(path.is_file(), f"locked artifact missing: {row['path']}")
        require(path.stat().st_size == row["byte_size"] and sha256_file(path) == row["sha256"], f"locked artifact drift: {row['path']}")
    for row in lock["sources"]:
        path = root / row["path"]
        require(path.is_file(), f"locked source missing: {row['path']}")
        require(path.stat().st_size == row["byte_size"] and sha256_file(path) == row["sha256"], f"locked source drift: {row['path']}")
    require(lock["bindings"] == {
        "compatibility_baseline_sha256": sha256_file(root / "goal-4/compatibility-baseline.json"),
        "guardrails_sha256": sha256_file(root / "goal-4/guardrails.json"),
        "legacy_git_tree": LEGACY_GIT_TREE,
        "quality_protocol_sha256": sha256_file(root / "goal-4/quality-evaluation.json"),
    }, "baseline lock binding drift")


def validate_baseline(
    root: Path,
    *,
    artifact_root: Path | None = None,
    raw_overrides: dict[str, Path] | None = None,
    check_lock: bool = True,
    require_sibling_absent: bool = False,
) -> dict[str, Any]:
    root = root.resolve(strict=True)
    artifact_root = (artifact_root or root / "goal-4").resolve(strict=True)
    if require_sibling_absent:
        require(not (root / REPAIRED_RELATIVE).exists(), "Stage 2 repaired sibling must remain absent")
    paths = _artifact_paths(artifact_root)
    manifest = load_canonical_json(paths["corpus-manifest.json"])
    routing = load_canonical_json(paths["routing-baseline.json"])
    sample = load_canonical_json(paths["held-out-sample.json"])
    detector_report = load_canonical_json(paths["baseline-detector-report.json"])
    environment = load_canonical_json(paths["baseline-environment.json"])
    structure_rows = load_jsonl(paths["structure-ledger.jsonl"])
    image_rows = load_jsonl(paths["image-reference-ledger.jsonl"])
    defect_rows = load_jsonl(paths["known-defect-regression.jsonl"])
    detector_hits = load_jsonl(paths["baseline-detector-hits.jsonl"])
    contract = load_json(root / "goal-4/guardrails.json")
    quality = load_json(root / "goal-4/quality-evaluation.json")
    _validate_raw_rows(root, manifest, raw_overrides)
    require(git_tree_identity(root, "HEAD", LEGACY_RELATIVE) == LEGACY_GIT_TREE, "legacy Git tree drift")
    segments, blocks = _independent_structure_checks(root, structure_rows)
    independent_seed, independent_ids, independent_allocations = _independent_sample_ids(manifest, blocks, contract, quality)
    require(independent_seed == sample["seed_sha256"], "independent held-out seed drift")
    require(independent_ids == sample["selected_raw_block_ids"], "independent held-out membership/order drift")
    require(independent_allocations == sample["document_allocations"], "independent held-out allocation drift")
    require(len(sample["rankings"]) == len(blocks) and sum(row["selected"] for row in sample["rankings"]) == 1125, "held-out rank coverage drift")
    require(len(image_rows) == 1444 and [row["raw_reference_ordinal"] for row in image_rows] == list(range(1, 1445)), "image reference ordinal drift")
    require([(row["raw_reference_ordinal"], row["monolith_line"]) for row in image_rows if row["split_status"] == "OMITTED"] == [(24, 680), (134, 1711), (135, 1744)], "image omission drift")
    require(len(defect_rows) == 55 and all(row["repair_authorized"] is False for row in defect_rows), "known-defect registry drift/authorization")
    require([row["sentinel_id"] for row in defect_rows] == [f"DEFECT-{number:04d}" for number in range(1, 56)], "known-defect IDs drift")
    require(detector_report["repairs_applied"] == 0 and detector_report["known_defect_registry"]["unrouted_count"] == 0, "baseline detector report claims repairs or leaves an unrouted sentinel")
    require(sum(row["detector_id"] == "D13_EXACT_SENTINEL" for row in detector_hits) == 55, "exact sentinel detector coverage drift")

    expected_manifest = build_corpus_manifest(root, contract)
    expected_structure, expected_segments, expected_blocks = structure_ledger_rows(root, contract)
    expected_images = build_image_reference_ledger(root, expected_manifest, expected_segments, expected_blocks)
    expected_routing = build_routing_baseline(root, expected_manifest, expected_images)
    expected_sample = build_held_out_sample(root, expected_manifest, expected_structure, expected_blocks, contract, quality)
    expected_defects = build_known_defect_rows(root, expected_manifest, expected_segments, expected_blocks, expected_images, expected_routing)
    expected_hits, expected_report = build_detector_artifacts(root, expected_manifest, expected_segments, expected_blocks, expected_images, expected_routing, expected_defects)
    require(manifest == expected_manifest, "corpus manifest does not reproduce")
    require(structure_rows == expected_structure, "structure ledger does not reproduce")
    require(image_rows == expected_images, "image reference ledger does not reproduce")
    require(routing == expected_routing, "routing baseline does not reproduce")
    require(sample == expected_sample, "held-out sample does not reproduce")
    require(defect_rows == expected_defects, "known-defect registry does not reproduce")
    require(detector_hits == expected_hits and detector_report == expected_report, "detector baseline does not reproduce")
    require(environment.get("schema_version") == "1.0.0", "baseline environment schema drift")
    scope = environment.get("capture_scope", {})
    require(scope.get("git_head_stable_during_capture") is True, "Git HEAD moved during baseline capture")
    require(
        scope.get("legacy_git_tree_before") == scope.get("legacy_git_tree_after") == LEGACY_GIT_TREE,
        "environment legacy Git-tree binding drift",
    )
    require(scope.get("legacy_manifest_stable_during_capture") is True, "legacy manifest moved during baseline capture")
    require(
        scope.get("legacy_manifest_rows_sha256_before")
        == scope.get("legacy_manifest_rows_sha256_after")
        == sha256_bytes(canonical_json_bytes(manifest["raw_inputs"])),
        "environment legacy manifest binding drift",
    )
    require(scope.get("repaired_sibling_absent_before") is True and scope.get("repaired_sibling_absent_after") is True, "environment captured a repaired sibling")
    if check_lock:
        lock_path = artifact_root / "baseline-lock.json"
        lock = load_canonical_json(lock_path)
        _validate_lock(root, artifact_root, lock)
        if EXPECTED_BASELINE_LOCK_SHA256 is not None:
            require(sha256_file(lock_path) == EXPECTED_BASELINE_LOCK_SHA256, "frozen baseline lock digest drift")
    return {
        "blocks": len(blocks),
        "defects": len(defect_rows),
        "images": len(image_rows),
        "sample": len(independent_ids),
        "segments": len(segments),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--artifact-root", type=Path)
    parser.add_argument("--skip-lock", action="store_true")
    parser.add_argument("--require-sibling-absent", action="store_true")
    args = parser.parse_args()
    try:
        summary = validate_baseline(
            args.repo_root,
            artifact_root=args.artifact_root,
            check_lock=not args.skip_lock,
            require_sibling_absent=args.require_sibling_absent,
        )
    except (GuardrailError, UnicodeError, OSError, KeyError, TypeError, ValueError) as error:
        print(f"BASELINE FAIL: {error}", file=sys.stderr)
        return 1
    print("BASELINE OK " + " ".join(f"{key}={value}" for key, value in sorted(summary.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
