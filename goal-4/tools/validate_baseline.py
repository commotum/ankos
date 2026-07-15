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
) -> None:
    raw_overrides = raw_overrides or {}
    manifest_paths = [row["relative_path"] for row in manifest["raw_inputs"]]
    require(len(manifest_paths) == len(set(manifest_paths)) == 1463, "manifest path count/uniqueness drift")
    require(manifest_paths == sorted(manifest_paths, key=lambda item: item.encode("utf-8")), "manifest path order drift")
    require(not any(path.startswith("../") or "A-New-Kind-of-Science-Repaired" in path for path in manifest_paths), "manifest includes an unsafe/repaired path")
    actual_paths = []
    legacy = root / LEGACY_RELATIVE
    for path in sorted(legacy.rglob("*"), key=lambda item: item.relative_to(legacy).as_posix().encode("utf-8")):
        require(not path.is_symlink(), f"legacy input symlink: {path}")
        if path.is_dir():
            continue
        require(path.is_file(), f"legacy special file: {path}")
        actual_paths.append(path.relative_to(legacy).as_posix())
    require(actual_paths == manifest_paths, "legacy exact-root path set differs from explicit manifest")
    for row in manifest["raw_inputs"]:
        relative = row["relative_path"]
        safe_relative_posix(relative)
        path = raw_overrides.get(relative, legacy / Path(*PurePosixPath(relative).parts))
        require(path.is_file() and not path.is_symlink(), f"raw input is missing/aliased: {relative}")
        mode = path.stat(follow_symlinks=False).st_mode
        require(stat.S_ISREG(mode), f"raw input is not regular: {relative}")
        payload = path.read_bytes()
        require(len(payload) == row["byte_size"], f"raw byte-size drift: {relative}")
        require(sha256_bytes(payload) == row["sha256"], f"raw SHA-256 drift: {relative}")
        if row["kind"] == "MARKDOWN":
            payload.decode("utf-8", errors="strict")
            require(b"\r" not in payload and not payload.startswith(b"\xef\xbb\xbf"), f"raw text profile drift: {relative}")
            require(len(split_raw_lines(payload)) == row["logical_line_count"], f"raw logical-line drift: {relative}")
            require(payload.count(b"\n") == row["text"]["lf_count"], f"raw LF count drift: {relative}")
            require(payload.endswith(b"\n") is row["text"]["terminal_lf"], f"raw final-LF drift: {relative}")
        else:
            require(payload.startswith(b"\xff\xd8") and payload.endswith(b"\xff\xd9"), f"raw JPEG framing drift: {relative}")


def _independent_structure_checks(
    root: Path,
    structure_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    segments = [row for row in structure_rows if row.get("record_type") == "SEGMENT"]
    blocks = [row for row in structure_rows if row.get("record_type") == "RAW_BLOCK"]
    require(len(segments) == 29 and len(blocks) == 20430, "structure record counts drift")
    require([row["segment_id"] for row in segments] == [row[0] for row in SEGMENT_STARTS], "segment ID/order drift")
    monolith = (root / LEGACY_RELATIVE / MONOLITH_RELATIVE).read_bytes()
    require(len(monolith) == 3780628 and sha256_bytes(monolith) == MONOLITH_SHA256, "independent monolith identity drift")
    lines = split_raw_lines(monolith)
    require(len(lines) == 22498 and monolith.count(b"\n") == 22497 and not monolith.endswith(b"\n"), "independent monolith line profile drift")
    expected_signatures = {row[0]: row[1:] for row in EXPECTED_SEGMENT_SIGNATURES}
    all_window_counts = Counter(line_window_signature(lines, number) for number in range(1, len(lines) + 1))
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
        require(row["boundary_status"] == "PROPOSED_RAW_BOUNDARY_PENDING_STAGE_3_5_WITNESS_VALIDATION", "Stage 2 boundary falsely claims witness authority")
        previous_line = end_line
        previous_byte = end_byte
    require(previous_line == 22498 and previous_byte == len(monolith), "segment final edge drift")
    previous_line = 0
    previous_byte = 0
    for ordinal, row in enumerate(blocks, 1):
        require(row["raw_block_id"] == f"RAW-{ordinal:06d}" and row["order"] == ordinal, "raw block ID/order drift")
        require(row["block_kind"] in BLOCK_KIND_ENUM, "raw block kind is outside frozen enum")
        require(row["risk_stratum"] in RISK_PRIORITY, "raw block risk is outside frozen enum")
        require(row["start_line"] == previous_line + 1 and row["start_byte"] == previous_byte, "raw block gap/overlap")
        require(row["end_line"] >= row["start_line"] and row["end_byte_exclusive"] > row["start_byte"], "raw block has invalid extent")
        payload = monolith[row["start_byte"] : row["end_byte_exclusive"]]
        require(len(payload) == row["byte_size"] and sha256_bytes(payload) == row["raw_sha256"], "raw block bytes/hash drift")
        require(row["terminal_lf"] is payload.endswith(b"\n"), "raw block LF flag drift")
        owner = next(segment for segment in segments if segment["segment_id"] == row["segment_id"])
        require(owner["raw_start_line"] <= row["start_line"] <= row["end_line"] <= owner["raw_end_line"], "raw block crosses segment")
        previous_line = row["end_line"]
        previous_byte = row["end_byte_exclusive"]
    require(previous_line == 22498 and previous_byte == len(monolith), "raw block final edge drift")
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
