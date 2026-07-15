"""Deterministic, byte-conserving Goal 4 zero-repair compiler.

The projection tape deliberately sits below ANKOS-AST-1.  ``SOURCE_BLOCK``
records are opaque byte slices from the frozen Stage 2 ledger; they make no
claim that the Stage 2 lexical label is semantically correct.  The sole
generated author-file byte in this build is the required terminal LF on the
Colophon.  Its projection is empty and its inverse is an exact drop.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import tempfile
import ctypes
import errno
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


class ZeroRepairError(RuntimeError):
    """A fail-closed zero-repair contract violation."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ZeroRepairError(message)


SCHEMA_VERSION = "1.0.0"
CONTRACT_ID = "ANKOS-ZERO-REPAIR-1"
TAPE_PROFILE_ID = "ANKOS-PROJECTION-TAPE-1"
SOURCE_BLOCK_SEMANTICS = "OPAQUE_BYTE_PROJECTION_OUTSIDE_ANKOS_AST_1"

EXPECTED_GUARDRAILS_SHA256 = "ba5357b6172c5740ed799bf53d65aa401c53750b0f5dc6ccc901d4149e5225cb"
EXPECTED_BASELINE_LOCK_SHA256 = "57224a1f1ba8333bbc900b23ff6127a189649feb01c279f30fac05a305658863"
EXPECTED_CORPUS_MANIFEST_SHA256 = "ba11d6ddf71aea5fb6e47be88ab54d47e33e1b8118273fa835c1b788c2321b76"
EXPECTED_STRUCTURE_LEDGER_SHA256 = "6f9891417f458ca1e40385082b4f230e780d72362a783f35e11648082a743d49"
EXPECTED_ZERO_REPAIR_CONTRACT_SHA256 = "3fd15222dfac4735640056e2ae786e36d5e96638454a4741ac1662ebfba3b964"
EXPECTED_MONOLITH_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"
EXPECTED_MONOLITH_BYTES = 3_780_628
EXPECTED_MONOLITH_LINES = 22_498
EXPECTED_SEGMENTS = 29
EXPECTED_BLOCKS = 20_430
EXPECTED_REPAIRED_RELATIVE = PurePosixPath("ref/A-New-Kind-of-Science-Repaired")
EXPECTED_LEGACY_RELATIVE = PurePosixPath("ref/A-New-Kind-of-Science")
EXPECTED_MONOLITH_RELATIVE = PurePosixPath("A-New-Kind-of-Science.md")

TAPE_RELATIVE = PurePosixPath("BUILD-METADATA/projection-tape.jsonl")
MANIFEST_RELATIVE = PurePosixPath("BUILD-METADATA/zero-repair-manifest.json")
CONTRACT_RELATIVE = PurePosixPath("zero-repair-contract.json")
TOOL_RELATIVES = (
    PurePosixPath("tools/zero_repair_lib.py"),
    PurePosixPath("tools/build_zero_repair.py"),
    PurePosixPath("tools/validate_zero_repair.py"),
    PurePosixPath("tools/zero_repair_verify.py"),
)

FILE_MODE = 0o644
DIRECTORY_MODE = 0o755
LF_SHA256 = hashlib.sha256(b"\n").hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _reject_float(value: Any) -> None:
    if isinstance(value, float):
        raise ZeroRepairError("canonical JSON forbids floating-point values")
    if isinstance(value, dict):
        for key, child in value.items():
            require(isinstance(key, str), "canonical JSON key is not a string")
            _reject_float(child)
    elif isinstance(value, list):
        for child in value:
            _reject_float(child)


def canonical_json_bytes(value: Any, *, terminal_lf: bool = True) -> bytes:
    _reject_float(value)
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return payload + (b"\n" if terminal_lf else b"")


def canonical_jsonl_bytes(rows: Iterable[dict[str, Any]]) -> bytes:
    return b"".join(canonical_json_bytes(row) for row in rows)


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ZeroRepairError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def _reject_json_float(_: str) -> Any:
    raise ZeroRepairError("JSON input contains a floating-point value")


def parse_json_bytes(payload: bytes, *, label: str, canonical: bool = False) -> Any:
    require(not payload.startswith(b"\xef\xbb\xbf"), f"{label} has a UTF-8 BOM")
    try:
        text = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise ZeroRepairError(f"{label} is not strict UTF-8") from error
    try:
        value = json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_float=_reject_json_float,
        )
    except (json.JSONDecodeError, TypeError) as error:
        raise ZeroRepairError(f"{label} is not valid JSON") from error
    _reject_float(value)
    if canonical:
        require(canonical_json_bytes(value) == payload, f"{label} is not exact ANKOS-CJ-1")
    return value


def parse_jsonl_bytes(payload: bytes, *, label: str, canonical: bool = False) -> list[dict[str, Any]]:
    require(payload.endswith(b"\n"), f"{label} lacks its terminal LF")
    rows: list[dict[str, Any]] = []
    for index, raw_line in enumerate(payload.splitlines(keepends=True), 1):
        require(raw_line.endswith(b"\n"), f"{label} line {index} lacks LF")
        require(raw_line != b"\n", f"{label} contains a blank row at {index}")
        row = parse_json_bytes(raw_line, label=f"{label} line {index}", canonical=canonical)
        require(isinstance(row, dict), f"{label} row {index} is not an object")
        rows.append(row)
    return rows


def _lexical_absolute(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _path_exists(path: Path) -> bool:
    return os.path.lexists(os.fspath(path))


def _assert_no_symlink_components(path: Path, *, label: str, include_leaf: bool = True) -> None:
    absolute = _lexical_absolute(path)
    chain = list(reversed(absolute.parents))
    if include_leaf:
        chain.append(absolute)
    for component in chain:
        if not _path_exists(component):
            continue
        mode = os.lstat(component).st_mode
        require(not stat.S_ISLNK(mode), f"{label} contains a symlink component: {component}")


def _assert_regular_input(path: Path, *, label: str) -> os.stat_result:
    _assert_no_symlink_components(path, label=label)
    require(_path_exists(path), f"missing {label}: {path}")
    status = os.lstat(path)
    require(stat.S_ISREG(status.st_mode), f"{label} is not a regular file: {path}")
    mode = stat.S_IMODE(status.st_mode)
    require(mode & 0o7000 == 0, f"{label} has special mode bits: {path}")
    require(mode & 0o111 == 0, f"{label} is executable: {path}")
    return status


def _strict_relative(value: str, *, label: str) -> PurePosixPath:
    require(isinstance(value, str) and value, f"{label} is not a nonempty string")
    require("\\" not in value and "\x00" not in value, f"{label} is not a strict POSIX path")
    require("%" not in value, f"{label} contains a forbidden percent escape")
    path = PurePosixPath(value)
    require(not path.is_absolute(), f"{label} is absolute")
    require(all(part not in {"", ".", ".."} for part in path.parts), f"{label} traverses")
    require(path.as_posix() == value, f"{label} is not canonical POSIX spelling")
    return path


def _join_relative(root: Path, relative: PurePosixPath) -> Path:
    return root.joinpath(*relative.parts)


def _read_frozen(path: Path, expected_sha256: str, *, label: str) -> bytes:
    _assert_regular_input(path, label=label)
    payload = path.read_bytes()
    require(sha256_bytes(payload) == expected_sha256, f"{label} hash drift")
    return payload


def _resolve_override(repo_root: Path, override: Path | None, default: PurePosixPath) -> Path:
    if override is None:
        return _join_relative(repo_root, default)
    if override.is_absolute():
        return _lexical_absolute(override)
    return _lexical_absolute(repo_root / override)


def _sequence_sha256(blocks: list[dict[str, Any]]) -> str:
    digest = hashlib.sha256(b"ANKOS-SOURCE-BLOCK-SEQUENCE-1\0")
    for block in blocks:
        for value in (block["raw_block_id"], block["raw_sha256"]):
            encoded = value.encode("ascii")
            digest.update(len(encoded).to_bytes(8, "big"))
            digest.update(encoded)
    return digest.hexdigest()


def _tree_digest(file_records: list[dict[str, Any]]) -> str:
    digest = hashlib.sha256(b"ANKOS-ZERO-REPAIR-PAYLOAD-TREE-1\0")
    for record in sorted(file_records, key=lambda item: item["path"]):
        payload = canonical_json_bytes(record, terminal_lf=False)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest()


def load_frozen_snapshot(
    repo_root: Path,
    *,
    goal_root: Path | None = None,
    legacy_root: Path | None = None,
) -> dict[str, Any]:
    """Load and independently recheck the exact inputs needed by zero repair."""

    repo = _lexical_absolute(repo_root)
    _assert_no_symlink_components(repo, label="repository root")
    require(_path_exists(repo) and stat.S_ISDIR(os.lstat(repo).st_mode), "repository root is not a directory")
    goal = _resolve_override(repo, goal_root, PurePosixPath("goal-4"))
    legacy = _resolve_override(repo, legacy_root, EXPECTED_LEGACY_RELATIVE)
    _assert_no_symlink_components(goal, label="Goal 4 root")
    _assert_no_symlink_components(legacy, label="legacy root")
    require(_path_exists(goal) and stat.S_ISDIR(os.lstat(goal).st_mode), "Goal 4 root is not a directory")
    require(_path_exists(legacy) and stat.S_ISDIR(os.lstat(legacy).st_mode), "legacy root is not a directory")

    guardrails_path = goal / "guardrails.json"
    lock_path = goal / "baseline-lock.json"
    manifest_path = goal / "corpus-manifest.json"
    ledger_path = goal / "structure-ledger.jsonl"
    contract_path = _join_relative(goal, CONTRACT_RELATIVE)
    guardrails_raw = _read_frozen(guardrails_path, EXPECTED_GUARDRAILS_SHA256, label="guardrails")
    lock_raw = _read_frozen(lock_path, EXPECTED_BASELINE_LOCK_SHA256, label="baseline lock")
    manifest_raw = _read_frozen(manifest_path, EXPECTED_CORPUS_MANIFEST_SHA256, label="corpus manifest")
    ledger_raw = _read_frozen(ledger_path, EXPECTED_STRUCTURE_LEDGER_SHA256, label="structure ledger")
    contract_raw = _read_frozen(
        contract_path,
        EXPECTED_ZERO_REPAIR_CONTRACT_SHA256,
        label="zero-repair contract",
    )

    guardrails = parse_json_bytes(guardrails_raw, label="guardrails")
    lock = parse_json_bytes(lock_raw, label="baseline lock", canonical=True)
    corpus = parse_json_bytes(manifest_raw, label="corpus manifest", canonical=True)
    ledger_rows = parse_jsonl_bytes(ledger_raw, label="structure ledger", canonical=True)
    contract = parse_json_bytes(contract_raw, label="zero-repair contract", canonical=True)
    require(isinstance(guardrails, dict) and isinstance(lock, dict) and isinstance(corpus, dict), "frozen input root type drift")
    require(isinstance(contract, dict) and contract.get("contract_id") == CONTRACT_ID, "zero-repair contract identity drift")

    artifact_map = {
        row.get("path"): row
        for row in lock.get("artifacts", [])
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    require(
        artifact_map.get("goal-4/corpus-manifest.json", {}).get("sha256") == EXPECTED_CORPUS_MANIFEST_SHA256,
        "baseline lock corpus-manifest binding drift",
    )
    require(
        artifact_map.get("goal-4/structure-ledger.jsonl", {}).get("sha256") == EXPECTED_STRUCTURE_LEDGER_SHA256,
        "baseline lock structure-ledger binding drift",
    )

    architecture = guardrails.get("architecture")
    require(isinstance(architecture, dict), "guardrails architecture missing")
    require(architecture.get("legacy_root") == EXPECTED_LEGACY_RELATIVE.as_posix(), "legacy architecture drift")
    require(architecture.get("repaired_root") == EXPECTED_REPAIRED_RELATIVE.as_posix(), "repaired architecture drift")
    documents = guardrails.get("canonical_documents")
    require(isinstance(documents, list) and len(documents) == EXPECTED_SEGMENTS, "canonical document count drift")
    normalized_documents: list[dict[str, Any]] = []
    seen_paths: set[str] = set()
    seen_ids: set[str] = set()
    for order, document in enumerate(documents):
        require(isinstance(document, dict), f"canonical document {order} is not an object")
        path = _strict_relative(document.get("path"), label=f"canonical document {order} path")
        require(path.parts[0] == "CANONICAL" and path.suffix == ".md", f"canonical document {order} path role drift")
        require(document.get("order") == order, f"canonical document order drift: {order}")
        require(document.get("role") == "CANONICAL_AUTHOR_TEXT", f"canonical document role drift: {order}")
        document_id = document.get("id")
        require(isinstance(document_id, str) and document_id, f"canonical document ID drift: {order}")
        require(path.as_posix() not in seen_paths and document_id not in seen_ids, "canonical path or ID collision")
        seen_paths.add(path.as_posix())
        seen_ids.add(document_id)
        normalized_documents.append(
            {
                "id": document_id,
                "order": order,
                "path": path.as_posix(),
                "role": "CANONICAL_AUTHOR_TEXT",
            }
        )

    require(corpus.get("legacy_root") == EXPECTED_LEGACY_RELATIVE.as_posix(), "corpus legacy root drift")
    raw_inputs = corpus.get("raw_inputs")
    require(isinstance(raw_inputs, list), "corpus raw inputs missing")
    monolith_rows = [row for row in raw_inputs if isinstance(row, dict) and row.get("role") == "RAW_AUTHOR_TEXT_MONOLITH"]
    require(len(monolith_rows) == 1, "corpus monolith role is not unique")
    monolith_record = monolith_rows[0]
    require(monolith_record.get("relative_path") == EXPECTED_MONOLITH_RELATIVE.as_posix(), "monolith relative path drift")
    require(monolith_record.get("sha256") == EXPECTED_MONOLITH_SHA256, "monolith manifest hash drift")
    require(monolith_record.get("byte_size") == EXPECTED_MONOLITH_BYTES, "monolith manifest size drift")
    require(monolith_record.get("logical_line_count") == EXPECTED_MONOLITH_LINES, "monolith line count drift")
    monolith_path = _join_relative(legacy, EXPECTED_MONOLITH_RELATIVE)
    monolith_raw = _read_frozen(monolith_path, EXPECTED_MONOLITH_SHA256, label="legacy monolith")
    require(len(monolith_raw) == EXPECTED_MONOLITH_BYTES, "monolith byte-size drift")
    require(monolith_raw.count(b"\n") == EXPECTED_MONOLITH_LINES - 1, "monolith LF-count drift")
    require(not monolith_raw.endswith(b"\n"), "monolith terminal-LF drift")
    monolith_raw.decode("utf-8", errors="strict")

    segments = [row for row in ledger_rows if row.get("record_type") == "SEGMENT"]
    blocks = [row for row in ledger_rows if row.get("record_type") == "RAW_BLOCK"]
    require(len(ledger_rows) == EXPECTED_SEGMENTS + EXPECTED_BLOCKS, "structure-ledger row-count drift")
    require(len(segments) == EXPECTED_SEGMENTS and len(blocks) == EXPECTED_BLOCKS, "structure-ledger type-count drift")
    require(ledger_rows[:EXPECTED_SEGMENTS] == segments and ledger_rows[EXPECTED_SEGMENTS:] == blocks, "structure-ledger record ordering drift")

    for order, (segment, document) in enumerate(zip(segments, normalized_documents)):
        require(segment.get("schema_version") == SCHEMA_VERSION, f"segment schema drift: {order}")
        require(segment.get("order") == order, f"segment order drift: {order}")
        require(segment.get("segment_id") == document["id"], f"segment ID drift: {order}")
        require(segment.get("canonical_path") == document["path"], f"segment path drift: {order}")
        require(segment.get("role") == "CANONICAL_AUTHOR_TEXT", f"segment role drift: {order}")
        require(segment.get("raw_source_path") == EXPECTED_MONOLITH_RELATIVE.as_posix(), f"segment source path drift: {order}")
        require(segment.get("raw_source_sha256") == EXPECTED_MONOLITH_SHA256, f"segment source hash drift: {order}")
        start = segment.get("raw_start_byte")
        end = segment.get("raw_end_byte_exclusive")
        require(isinstance(start, int) and isinstance(end, int) and 0 <= start < end <= len(monolith_raw), f"segment byte range drift: {order}")
        require(segment.get("raw_byte_count") == end - start, f"segment byte count drift: {order}")
        require(sha256_bytes(monolith_raw[start:end]) == segment.get("raw_segment_sha256"), f"segment payload hash drift: {order}")
        if order == 0:
            require(start == 0, "first segment does not start at byte zero")
        else:
            require(segments[order - 1].get("raw_end_byte_exclusive") == start, f"segment byte gap/overlap: {order}")
    require(segments[-1].get("raw_end_byte_exclusive") == len(monolith_raw), "last segment does not reach EOF")

    segment_by_id = {segment["segment_id"]: segment for segment in segments}
    previous_end = 0
    previous_line_end = 0
    segment_block_counts = {document["id"]: 0 for document in normalized_documents}
    for index, block in enumerate(blocks, 1):
        require(block.get("schema_version") == SCHEMA_VERSION, f"raw block schema drift: {index}")
        require(block.get("order") == index, f"raw block order drift: {index}")
        require(block.get("raw_block_id") == f"RAW-{index:06d}", f"raw block ID drift: {index}")
        start = block.get("start_byte")
        end = block.get("end_byte_exclusive")
        require(isinstance(start, int) and isinstance(end, int) and start == previous_end and start < end <= len(monolith_raw), f"raw block byte gap/overlap: {index}")
        require(block.get("byte_size") == end - start, f"raw block size drift: {index}")
        require(sha256_bytes(monolith_raw[start:end]) == block.get("raw_sha256"), f"raw block hash drift: {index}")
        start_line = block.get("start_line")
        end_line = block.get("end_line")
        require(isinstance(start_line, int) and isinstance(end_line, int), f"raw block line type drift: {index}")
        require(start_line == previous_line_end + 1 and start_line <= end_line, f"raw block line gap/overlap: {index}")
        segment_id = block.get("segment_id")
        require(segment_id in segment_by_id, f"raw block segment is unknown: {index}")
        segment = segment_by_id[segment_id]
        require(block.get("canonical_document_id") == segment_id, f"raw block document ID drift: {index}")
        require(block.get("canonical_path") == segment.get("canonical_path"), f"raw block path drift: {index}")
        require(segment["raw_start_byte"] <= start < end <= segment["raw_end_byte_exclusive"], f"raw block crosses segment: {index}")
        segment_block_counts[segment_id] += 1
        previous_end = end
        previous_line_end = end_line
    require(previous_end == len(monolith_raw), "raw blocks do not reach monolith EOF")
    require(previous_line_end == EXPECTED_MONOLITH_LINES, "raw blocks do not reach final logical line")
    require(all(count > 0 for count in segment_block_counts.values()), "canonical document has no raw block")

    tool_sources: list[dict[str, Any]] = []
    tool_paths: list[Path] = []
    for relative in TOOL_RELATIVES:
        path = _join_relative(goal, relative)
        _assert_regular_input(path, label=f"tool source {relative.as_posix()}")
        tool_paths.append(path)
        tool_sources.append(
            {
                "path": f"goal-4/{relative.as_posix()}",
                "sha256": sha256_file(path),
            }
        )

    return {
        "repo_root": repo,
        "goal_root": goal,
        "legacy_root": legacy,
        "repaired_root": _join_relative(repo, EXPECTED_REPAIRED_RELATIVE),
        "input_paths": [guardrails_path, lock_path, manifest_path, ledger_path, contract_path, monolith_path, *tool_paths],
        "input_hashes": {
            "baseline_lock_sha256": EXPECTED_BASELINE_LOCK_SHA256,
            "corpus_manifest_sha256": EXPECTED_CORPUS_MANIFEST_SHA256,
            "guardrails_sha256": EXPECTED_GUARDRAILS_SHA256,
            "structure_ledger_sha256": EXPECTED_STRUCTURE_LEDGER_SHA256,
            "zero_repair_contract_sha256": EXPECTED_ZERO_REPAIR_CONTRACT_SHA256,
        },
        "monolith_path": monolith_path,
        "monolith": monolith_raw,
        "documents": normalized_documents,
        "segments": segments,
        "blocks": blocks,
        "segment_block_counts": segment_block_counts,
        "source_block_sequence_sha256": _sequence_sha256(blocks),
        "tool_sources": tool_sources,
    }


def _validate_output_location(snapshot: dict[str, Any], output_root: Path, *, must_be_absent: bool) -> Path:
    require(output_root.is_absolute(), "output root must be an absolute caller-provided path")
    output = _lexical_absolute(output_root)
    repo = snapshot["repo_root"]
    goal = snapshot["goal_root"]
    legacy = snapshot["legacy_root"]
    repaired = snapshot["repaired_root"]
    require(output != repo and output != goal and output != legacy and output != repaired, "output root aliases a governed root")
    require(not _is_within(output, legacy), "output root is inside the immutable legacy root")
    require(not _is_within(output, repaired), "output root is inside the repaired sibling")
    if _is_within(output, repo):
        require(_is_within(output, goal), "repository-local staging is allowed only below Goal 4")
    for input_path in snapshot["input_paths"]:
        require(not _is_within(input_path, output), "output root would contain a frozen input")
    parent = output.parent
    _assert_no_symlink_components(parent, label="output parent")
    require(_path_exists(parent) and stat.S_ISDIR(os.lstat(parent).st_mode), "output parent is not an existing directory")
    if must_be_absent:
        require(not _path_exists(output), "output root already exists; generated output is never an input")
    else:
        _assert_no_symlink_components(output, label="output root")
        require(_path_exists(output) and stat.S_ISDIR(os.lstat(output).st_mode), "output root is not a directory")
    return output


def _mkdir_owned(path: Path) -> None:
    if _path_exists(path):
        status = os.lstat(path)
        require(stat.S_ISDIR(status.st_mode) and not stat.S_ISLNK(status.st_mode), f"owned directory collision: {path}")
        os.chmod(path, DIRECTORY_MODE)
        return
    os.mkdir(path, DIRECTORY_MODE)
    os.chmod(path, DIRECTORY_MODE)


def _ensure_relative_parent(root: Path, relative: PurePosixPath) -> Path:
    current = root
    for part in relative.parts[:-1]:
        current = current / part
        _mkdir_owned(current)
    return current / relative.name


def _write_new_file(root: Path, relative: PurePosixPath, payload: bytes) -> Path:
    path = _ensure_relative_parent(root, relative)
    require(not _path_exists(path), f"output path already exists: {relative.as_posix()}")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o600)
    try:
        with os.fdopen(descriptor, "wb", closefd=True) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        if _path_exists(path):
            os.unlink(path)
        raise
    os.chmod(path, FILE_MODE)
    return path


def _file_record(path: str, role: str, payload: bytes) -> dict[str, Any]:
    return {
        "byte_size": len(payload),
        "mode": "0644",
        "path": path,
        "role": role,
        "sha256": sha256_bytes(payload),
        "type": "REGULAR_FILE",
    }


def _make_tape_and_documents(snapshot: dict[str, Any], output: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    monolith: bytes = snapshot["monolith"]
    blocks: list[dict[str, Any]] = snapshot["blocks"]
    documents: list[dict[str, Any]] = snapshot["documents"]
    segments: list[dict[str, Any]] = snapshot["segments"]
    blocks_by_segment: dict[str, list[dict[str, Any]]] = {document["id"]: [] for document in documents}
    for block in blocks:
        blocks_by_segment[block["segment_id"]].append(block)

    tape_rows: list[dict[str, Any]] = []
    document_records: list[dict[str, Any]] = []
    file_records: list[dict[str, Any]] = []
    tape_order = 0
    for document, segment in zip(documents, segments):
        source_payload = monolith[segment["raw_start_byte"] : segment["raw_end_byte_exclusive"]]
        output_payload = source_payload
        generated_count = 0
        if document["id"] == "COLOPHON":
            require(not source_payload.endswith(b"\n"), "Colophon unexpectedly already has a terminal LF")
            output_payload += b"\n"
            generated_count = 1
        else:
            require(source_payload.endswith(b"\n"), f"non-Colophon document lacks terminal LF: {document['id']}")
        relative = PurePosixPath(document["path"])
        _write_new_file(output, relative, output_payload)
        file_records.append(_file_record(document["path"], "CANONICAL_AUTHOR_TEXT", output_payload))

        owned_blocks = blocks_by_segment[document["id"]]
        require(owned_blocks, f"document has no source blocks: {document['id']}")
        for block in owned_blocks:
            tape_order += 1
            output_start = block["start_byte"] - segment["raw_start_byte"]
            output_end = block["end_byte_exclusive"] - segment["raw_start_byte"]
            projected = output_payload[output_start:output_end]
            require(sha256_bytes(projected) == block["raw_sha256"], f"build source projection drift: {block['raw_block_id']}")
            tape_rows.append(
                {
                    "document_id": document["id"],
                    "document_order": document["order"],
                    "output_end_byte_exclusive": output_end,
                    "output_path": document["path"],
                    "output_sha256": block["raw_sha256"],
                    "output_start_byte": output_start,
                    "projection": "IDENTITY",
                    "raw_block_id": block["raw_block_id"],
                    "raw_end_byte_exclusive": block["end_byte_exclusive"],
                    "raw_order": block["order"],
                    "raw_sha256": block["raw_sha256"],
                    "raw_start_byte": block["start_byte"],
                    "record_type": "SOURCE_BLOCK",
                    "schema_version": SCHEMA_VERSION,
                    "tape_order": tape_order,
                }
            )
        if generated_count:
            tape_order += 1
            tape_rows.append(
                {
                    "author_text_projection_byte_size": 0,
                    "document_id": document["id"],
                    "document_order": document["order"],
                    "generated_kind": "FILE_TERMINATOR_LF",
                    "inverse": "DROP_EXACT_BYTES",
                    "output_end_byte_exclusive": len(output_payload),
                    "output_path": document["path"],
                    "output_sha256": LF_SHA256,
                    "output_start_byte": len(output_payload) - 1,
                    "record_type": "GENERATED_METADATA",
                    "schema_version": SCHEMA_VERSION,
                    "tape_order": tape_order,
                }
            )
        document_records.append(
            {
                "block_count": len(owned_blocks),
                "first_raw_block_id": owned_blocks[0]["raw_block_id"],
                "generated_span_count": generated_count,
                "id": document["id"],
                "last_raw_block_id": owned_blocks[-1]["raw_block_id"],
                "order": document["order"],
                "output_byte_size": len(output_payload),
                "output_sha256": sha256_bytes(output_payload),
                "path": document["path"],
                "raw_projection_byte_size": len(source_payload),
                "raw_projection_sha256": segment["raw_segment_sha256"],
                "role": "CANONICAL_AUTHOR_TEXT",
            }
        )
    require(tape_order == EXPECTED_BLOCKS + 1, "projection tape row count drift during build")
    return tape_rows, document_records, file_records


def inverse_from_output(
    output_root: Path,
    tape_rows: list[dict[str, Any]],
    documents: list[dict[str, Any]],
) -> bytes:
    """Recover the raw stream solely from staged author-file output spans."""

    output = _lexical_absolute(output_root)
    payload_by_path: dict[str, bytes] = {}
    for document in documents:
        path = _join_relative(output, PurePosixPath(document["path"]))
        _assert_regular_input(path, label=f"canonical output {document['path']}")
        payload_by_path[document["path"]] = path.read_bytes()

    reconstructed = bytearray()
    expected_tape_order = 1
    expected_raw_order = 1
    for row in tape_rows:
        require(row.get("tape_order") == expected_tape_order, f"inverse tape order drift: {expected_tape_order}")
        expected_tape_order += 1
        path = row.get("output_path")
        require(path in payload_by_path, f"inverse tape path is undeclared: {path}")
        payload = payload_by_path[path]
        start = row.get("output_start_byte")
        end = row.get("output_end_byte_exclusive")
        require(isinstance(start, int) and isinstance(end, int) and 0 <= start < end <= len(payload), f"inverse output span drift: {expected_tape_order - 1}")
        fragment = payload[start:end]
        require(sha256_bytes(fragment) == row.get("output_sha256"), f"inverse output fragment hash drift: {expected_tape_order - 1}")
        record_type = row.get("record_type")
        if record_type == "SOURCE_BLOCK":
            require(row.get("projection") == "IDENTITY", "unknown source projection")
            require(row.get("raw_order") == expected_raw_order, f"inverse raw order drift: {expected_raw_order}")
            require(row.get("raw_block_id") == f"RAW-{expected_raw_order:06d}", f"inverse raw block ID drift: {expected_raw_order}")
            require(sha256_bytes(fragment) == row.get("raw_sha256"), f"inverse raw fragment hash drift: {expected_raw_order}")
            reconstructed.extend(fragment)
            expected_raw_order += 1
        elif record_type == "GENERATED_METADATA":
            require(row.get("generated_kind") == "FILE_TERMINATOR_LF", "unknown generated metadata kind")
            require(row.get("inverse") == "DROP_EXACT_BYTES", "unknown generated metadata inverse")
            require(row.get("author_text_projection_byte_size") == 0, "generated metadata leaked into author projection")
            require(fragment == b"\n", "generated terminal wrapper is not one LF")
        else:
            raise ZeroRepairError(f"unknown projection-tape record type: {record_type}")
    require(expected_raw_order == EXPECTED_BLOCKS + 1, "inverse did not recover every source block")
    return bytes(reconstructed)


def _build_manifest(
    snapshot: dict[str, Any],
    tape_bytes: bytes,
    tape_rows: list[dict[str, Any]],
    document_records: list[dict[str, Any]],
    file_records: list[dict[str, Any]],
    inverse_payload: bytes,
) -> dict[str, Any]:
    source_bytes = sum(document["raw_projection_byte_size"] for document in document_records)
    output_author_bytes = sum(document["output_byte_size"] for document in document_records)
    require(source_bytes == EXPECTED_MONOLITH_BYTES, "manifest source-byte arithmetic drift")
    require(output_author_bytes == EXPECTED_MONOLITH_BYTES + 1, "manifest output-byte arithmetic drift")
    require(inverse_payload == snapshot["monolith"], "inverse output does not byte-match the frozen monolith")
    tape_record = _file_record(TAPE_RELATIVE.as_posix(), "RELEASE_METADATA", tape_bytes)
    payload_records = [*file_records, tape_record]
    return {
        "certification": "UNCERTIFIED_ZERO_REPAIR",
        "contract_id": CONTRACT_ID,
        "counts": {
            "canonical_documents": EXPECTED_SEGMENTS,
            "generated_author_file_spans": 1,
            "metadata_files": 2,
            "output_author_file_bytes": output_author_bytes,
            "projection_tape_rows": len(tape_rows),
            "source_blocks": EXPECTED_BLOCKS,
            "source_projection_bytes": source_bytes,
        },
        "documents": document_records,
        "inputs": {
            **snapshot["input_hashes"],
            "legacy_monolith_relative_path": f"{EXPECTED_LEGACY_RELATIVE.as_posix()}/{EXPECTED_MONOLITH_RELATIVE.as_posix()}",
            "monolith_byte_size": EXPECTED_MONOLITH_BYTES,
            "monolith_sha256": EXPECTED_MONOLITH_SHA256,
            "tool_sources": snapshot["tool_sources"],
        },
        "inverse_proof": {
            "algorithm": "READ_OUTPUT_SPANS_IN_TAPE_ORDER_DROP_TYPED_GENERATED_METADATA",
            "recovered_byte_size": len(inverse_payload),
            "recovered_sha256": sha256_bytes(inverse_payload),
            "source_block_sequence_sha256": snapshot["source_block_sequence_sha256"],
        },
        "output_payload": {
            "file_count_excluding_manifest": len(payload_records),
            "files": sorted(payload_records, key=lambda item: item["path"]),
            "tree_sha256_excluding_manifest": _tree_digest(payload_records),
        },
        "profile": {
            "ast_profile_used": False,
            "generated_author_file_bytes": "ONE_TYPED_COLOPHON_TERMINAL_LF",
            "projection_tape_profile_id": TAPE_PROFILE_ID,
            "source_block_semantics": SOURCE_BLOCK_SEMANTICS,
        },
        "schema_version": SCHEMA_VERSION,
    }


def build_zero_repair(
    repo_root: Path,
    output_root: Path,
    *,
    goal_root: Path | None = None,
    legacy_root: Path | None = None,
) -> dict[str, Any]:
    snapshot = load_frozen_snapshot(repo_root, goal_root=goal_root, legacy_root=legacy_root)
    output = _validate_output_location(snapshot, output_root, must_be_absent=True)
    parent_status = os.lstat(output.parent)
    temporary = Path(
        tempfile.mkdtemp(
            prefix=f".{output.name}.zero-repair-private-",
            dir=os.fspath(output.parent),
        )
    )
    # mkdtemp creates 0700: keep the in-progress tree private until complete.
    require(stat.S_IMODE(os.lstat(temporary).st_mode) == 0o700, "private build root mode drift")
    promoted = False
    try:
        tape_rows, document_records, file_records = _make_tape_and_documents(snapshot, temporary)
        tape_bytes = canonical_jsonl_bytes(tape_rows)
        _write_new_file(temporary, TAPE_RELATIVE, tape_bytes)
        inverse_payload = inverse_from_output(temporary, tape_rows, snapshot["documents"])
        manifest = _build_manifest(snapshot, tape_bytes, tape_rows, document_records, file_records, inverse_payload)
        manifest_bytes = canonical_json_bytes(manifest)
        _write_new_file(temporary, MANIFEST_RELATIVE, manifest_bytes)
        os.chmod(temporary, DIRECTORY_MODE)

        # The oracle is intentionally implemented in a different module and
        # imports none of this compiler.  Compiler self-consistency is not a
        # sufficient condition for promotion.
        from zero_repair_verify import (  # pylint: disable=import-outside-toplevel
            IndependentVerificationError,
            independently_validate_zero_repair,
        )

        try:
            result = independently_validate_zero_repair(
                repo_root,
                temporary,
                goal_root=goal_root,
                legacy_root=legacy_root,
            )
        except IndependentVerificationError as error:
            raise ZeroRepairError(f"independent pre-promotion validation failed: {error}") from error

        current_parent = os.lstat(output.parent)
        require(
            (current_parent.st_dev, current_parent.st_ino)
            == (parent_status.st_dev, parent_status.st_ino),
            "output parent changed during build",
        )
        _assert_no_symlink_components(output.parent, label="output parent before promotion")
        _atomic_rename_noreplace(temporary, output)
        promoted = True
        result["manifest_sha256"] = sha256_bytes(manifest_bytes)
        return result
    finally:
        if not promoted and _path_exists(temporary):
            status = os.lstat(temporary)
            require(
                stat.S_ISDIR(status.st_mode) and not stat.S_ISLNK(status.st_mode),
                "refusing to clean an altered private build root",
            )
            shutil.rmtree(temporary)


def _atomic_rename_noreplace(source: Path, target: Path) -> None:
    """Atomically publish a complete directory without replacing a target.

    Linux ``renameat2(RENAME_NOREPLACE)`` closes the last target-creation race.
    On platforms without that primitive, the explicit absence check plus
    ``rename`` is the strongest stdlib fallback available.
    """

    require(_path_exists(source), "private build root disappeared before promotion")
    require(not _path_exists(target), "output root appeared before promotion")
    libc = ctypes.CDLL(None, use_errno=True)
    renameat2 = getattr(libc, "renameat2", None)
    if renameat2 is not None:
        renameat2.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        renameat2.restype = ctypes.c_int
        result = renameat2(
            -100,
            os.fsencode(source),
            -100,
            os.fsencode(target),
            1,
        )
        if result == 0:
            return
        error_number = ctypes.get_errno()
        if error_number not in {errno.ENOSYS, errno.EINVAL, errno.EOPNOTSUPP}:
            if error_number in {errno.EEXIST, errno.ENOTEMPTY}:
                raise ZeroRepairError("output root appeared before atomic promotion")
            raise OSError(error_number, os.strerror(error_number), os.fspath(target))
    require(not _path_exists(target), "output root appeared before fallback promotion")
    os.rename(source, target)


def _expected_output_paths(snapshot: dict[str, Any]) -> tuple[set[str], set[str]]:
    files = {document["path"] for document in snapshot["documents"]}
    files.update({TAPE_RELATIVE.as_posix(), MANIFEST_RELATIVE.as_posix()})
    directories: set[str] = set()
    for file_path in files:
        current = PurePosixPath(file_path).parent
        while current != PurePosixPath("."):
            directories.add(current.as_posix())
            current = current.parent
    return files, directories


def _inventory_output(output: Path, expected_files: set[str], expected_directories: set[str]) -> None:
    root_status = os.lstat(output)
    require(stat.S_ISDIR(root_status.st_mode) and not stat.S_ISLNK(root_status.st_mode), "output root type drift")
    require(stat.S_IMODE(root_status.st_mode) == DIRECTORY_MODE, "output root mode drift")
    actual_files: set[str] = set()
    actual_directories: set[str] = set()
    file_inodes: set[tuple[int, int]] = set()
    for directory, names, filenames in os.walk(output, topdown=True, followlinks=False):
        names.sort()
        filenames.sort()
        directory_path = Path(directory)
        for name in names:
            path = directory_path / name
            status = os.lstat(path)
            relative = path.relative_to(output).as_posix()
            require(stat.S_ISDIR(status.st_mode) and not stat.S_ISLNK(status.st_mode), f"output directory is not a real directory: {relative}")
            require(stat.S_IMODE(status.st_mode) == DIRECTORY_MODE, f"output directory mode drift: {relative}")
            actual_directories.add(relative)
        for name in filenames:
            path = directory_path / name
            status = os.lstat(path)
            relative = path.relative_to(output).as_posix()
            require(stat.S_ISREG(status.st_mode) and not stat.S_ISLNK(status.st_mode), f"output file is not a regular file: {relative}")
            require(stat.S_IMODE(status.st_mode) == FILE_MODE, f"output file mode drift: {relative}")
            require(status.st_nlink == 1, f"output file has a hardlink: {relative}")
            inode = (status.st_dev, status.st_ino)
            require(inode not in file_inodes, f"output files share an inode: {relative}")
            file_inodes.add(inode)
            actual_files.add(relative)
    require(actual_files == expected_files, "output file ownership drift")
    require(actual_directories == expected_directories, "output directory ownership drift")


def _expected_tape(snapshot: dict[str, Any], output: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Derive expected records without writing by using a private ephemeral tree."""

    # Validation should not manufacture a second tree.  Recreate the records
    # arithmetically and read the declared document bytes only for file hashes.
    monolith: bytes = snapshot["monolith"]
    blocks: list[dict[str, Any]] = snapshot["blocks"]
    documents: list[dict[str, Any]] = snapshot["documents"]
    segments: list[dict[str, Any]] = snapshot["segments"]
    blocks_by_segment: dict[str, list[dict[str, Any]]] = {document["id"]: [] for document in documents}
    for block in blocks:
        blocks_by_segment[block["segment_id"]].append(block)
    tape: list[dict[str, Any]] = []
    document_records: list[dict[str, Any]] = []
    file_records: list[dict[str, Any]] = []
    tape_order = 0
    for document, segment in zip(documents, segments):
        source_payload = monolith[segment["raw_start_byte"] : segment["raw_end_byte_exclusive"]]
        expected_payload = source_payload + (b"\n" if document["id"] == "COLOPHON" else b"")
        output_payload = _join_relative(output, PurePosixPath(document["path"])).read_bytes()
        require(output_payload == expected_payload, f"canonical zero-repair bytes drift: {document['id']}")
        file_records.append(_file_record(document["path"], "CANONICAL_AUTHOR_TEXT", output_payload))
        owned = blocks_by_segment[document["id"]]
        for block in owned:
            tape_order += 1
            output_start = block["start_byte"] - segment["raw_start_byte"]
            output_end = block["end_byte_exclusive"] - segment["raw_start_byte"]
            tape.append(
                {
                    "document_id": document["id"],
                    "document_order": document["order"],
                    "output_end_byte_exclusive": output_end,
                    "output_path": document["path"],
                    "output_sha256": block["raw_sha256"],
                    "output_start_byte": output_start,
                    "projection": "IDENTITY",
                    "raw_block_id": block["raw_block_id"],
                    "raw_end_byte_exclusive": block["end_byte_exclusive"],
                    "raw_order": block["order"],
                    "raw_sha256": block["raw_sha256"],
                    "raw_start_byte": block["start_byte"],
                    "record_type": "SOURCE_BLOCK",
                    "schema_version": SCHEMA_VERSION,
                    "tape_order": tape_order,
                }
            )
        generated_count = 0
        if document["id"] == "COLOPHON":
            generated_count = 1
            tape_order += 1
            tape.append(
                {
                    "author_text_projection_byte_size": 0,
                    "document_id": document["id"],
                    "document_order": document["order"],
                    "generated_kind": "FILE_TERMINATOR_LF",
                    "inverse": "DROP_EXACT_BYTES",
                    "output_end_byte_exclusive": len(output_payload),
                    "output_path": document["path"],
                    "output_sha256": LF_SHA256,
                    "output_start_byte": len(output_payload) - 1,
                    "record_type": "GENERATED_METADATA",
                    "schema_version": SCHEMA_VERSION,
                    "tape_order": tape_order,
                }
            )
        document_records.append(
            {
                "block_count": len(owned),
                "first_raw_block_id": owned[0]["raw_block_id"],
                "generated_span_count": generated_count,
                "id": document["id"],
                "last_raw_block_id": owned[-1]["raw_block_id"],
                "order": document["order"],
                "output_byte_size": len(output_payload),
                "output_sha256": sha256_bytes(output_payload),
                "path": document["path"],
                "raw_projection_byte_size": len(source_payload),
                "raw_projection_sha256": segment["raw_segment_sha256"],
                "role": "CANONICAL_AUTHOR_TEXT",
            }
        )
    return tape, document_records, file_records


def _validate_tape_coverage(tape_rows: list[dict[str, Any]], snapshot: dict[str, Any], output: Path) -> None:
    documents = snapshot["documents"]
    rows_by_document: dict[str, list[dict[str, Any]]] = {document["id"]: [] for document in documents}
    for row in tape_rows:
        document_id = row.get("document_id")
        require(document_id in rows_by_document, f"tape row has unknown document: {document_id}")
        rows_by_document[document_id].append(row)
    for document in documents:
        payload_size = os.lstat(_join_relative(output, PurePosixPath(document["path"]))).st_size
        cursor = 0
        for row in rows_by_document[document["id"]]:
            require(row.get("output_path") == document["path"], f"tape output path drift: {document['id']}")
            require(row.get("document_order") == document["order"], f"tape document order drift: {document['id']}")
            require(row.get("output_start_byte") == cursor, f"tape output coverage gap/overlap: {document['id']}")
            end = row.get("output_end_byte_exclusive")
            require(isinstance(end, int) and end > cursor, f"tape output span is empty: {document['id']}")
            cursor = end
        require(cursor == payload_size, f"tape output coverage does not reach EOF: {document['id']}")


def validate_zero_repair(
    repo_root: Path,
    output_root: Path,
    *,
    goal_root: Path | None = None,
    legacy_root: Path | None = None,
) -> dict[str, Any]:
    snapshot = load_frozen_snapshot(repo_root, goal_root=goal_root, legacy_root=legacy_root)
    output = _validate_output_location(snapshot, output_root, must_be_absent=False)
    expected_files, expected_directories = _expected_output_paths(snapshot)
    _inventory_output(output, expected_files, expected_directories)

    manifest_path = _join_relative(output, MANIFEST_RELATIVE)
    tape_path = _join_relative(output, TAPE_RELATIVE)
    manifest_raw = manifest_path.read_bytes()
    tape_raw = tape_path.read_bytes()
    manifest = parse_json_bytes(manifest_raw, label="zero-repair manifest", canonical=True)
    tape_rows = parse_jsonl_bytes(tape_raw, label="projection tape", canonical=True)
    require(isinstance(manifest, dict), "zero-repair manifest is not an object")
    expected_tape, document_records, file_records = _expected_tape(snapshot, output)
    require(tape_rows == expected_tape, "projection tape differs from frozen source/output mapping")
    _validate_tape_coverage(tape_rows, snapshot, output)
    inverse_payload = inverse_from_output(output, tape_rows, snapshot["documents"])
    require(len(inverse_payload) == EXPECTED_MONOLITH_BYTES, "inverse byte-size proof drift")
    require(sha256_bytes(inverse_payload) == EXPECTED_MONOLITH_SHA256, "inverse monolith hash proof drift")
    require(inverse_payload == snapshot["monolith"], "inverse byte proof differs from frozen monolith")
    expected_manifest = _build_manifest(snapshot, tape_raw, tape_rows, document_records, file_records, inverse_payload)
    require(manifest == expected_manifest, "zero-repair manifest semantic drift")
    require(canonical_json_bytes(expected_manifest) == manifest_raw, "zero-repair manifest byte drift")
    return {
        "canonical_documents": EXPECTED_SEGMENTS,
        "generated_spans": 1,
        "inverse_byte_size": len(inverse_payload),
        "inverse_sha256": sha256_bytes(inverse_payload),
        "manifest_sha256": sha256_bytes(manifest_raw),
        "payload_tree_sha256": manifest["output_payload"]["tree_sha256_excluding_manifest"],
        "projection_tape_rows": len(tape_rows),
        "projection_tape_sha256": sha256_bytes(tape_raw),
        "source_blocks": EXPECTED_BLOCKS,
    }


def _full_tree_records(root: Path) -> list[dict[str, Any]]:
    _assert_no_symlink_components(root, label="comparison root")
    require(_path_exists(root), "comparison root does not exist")
    root_status = os.lstat(root)
    require(
        stat.S_ISDIR(root_status.st_mode) and not stat.S_ISLNK(root_status.st_mode),
        "comparison root is not a real directory",
    )
    require(stat.S_IMODE(root_status.st_mode) == DIRECTORY_MODE, "comparison root mode drift")
    records: list[dict[str, Any]] = []
    for directory, names, filenames in os.walk(root, topdown=True, followlinks=False):
        names.sort()
        filenames.sort()
        directory_path = Path(directory)
        if directory_path != root:
            status = os.lstat(directory_path)
            require(stat.S_ISDIR(status.st_mode) and not stat.S_ISLNK(status.st_mode), "comparison tree contains a non-directory")
            require(stat.S_IMODE(status.st_mode) == DIRECTORY_MODE, "comparison directory mode drift")
            records.append(
                {
                    "mode": f"{stat.S_IMODE(status.st_mode):04o}",
                    "path": directory_path.relative_to(root).as_posix(),
                    "type": "DIRECTORY",
                }
            )
        for filename in filenames:
            path = directory_path / filename
            status = os.lstat(path)
            require(stat.S_ISREG(status.st_mode) and not stat.S_ISLNK(status.st_mode), "comparison tree contains an unexpected file type")
            require(stat.S_IMODE(status.st_mode) == FILE_MODE, "comparison file mode drift")
            require(status.st_nlink == 1, "comparison tree contains a hardlinked file")
            records.append(
                {
                    "byte_size": status.st_size,
                    "mode": f"{stat.S_IMODE(status.st_mode):04o}",
                    "path": path.relative_to(root).as_posix(),
                    "sha256": sha256_file(path),
                    "type": "REGULAR_FILE",
                }
            )
    require(records, "comparison root is empty")
    return sorted(records, key=lambda item: (item["path"], item["type"]))


def compare_zero_repair_trees(
    first_root: Path,
    second_root: Path,
    *,
    repo_root: Path | None = None,
    goal_root: Path | None = None,
    legacy_root: Path | None = None,
) -> dict[str, Any]:
    first = _lexical_absolute(first_root)
    second = _lexical_absolute(second_root)
    require(first != second, "clean-build comparison roots are identical")
    verification_repo = (
        _lexical_absolute(repo_root)
        if repo_root is not None
        else _lexical_absolute(Path(__file__).parents[2])
    )
    from zero_repair_verify import (  # pylint: disable=import-outside-toplevel
        IndependentVerificationError,
        independently_validate_zero_repair,
    )

    try:
        independently_validate_zero_repair(
            verification_repo,
            first,
            goal_root=goal_root,
            legacy_root=legacy_root,
        )
        independently_validate_zero_repair(
            verification_repo,
            second,
            goal_root=goal_root,
            legacy_root=legacy_root,
        )
    except IndependentVerificationError as error:
        raise ZeroRepairError(f"comparison root is not a validated zero-repair tree: {error}") from error
    first_records = _full_tree_records(first)
    second_records = _full_tree_records(second)
    require(first_records == second_records, "two clean zero-repair builds are not byte-identical")
    payload = canonical_json_bytes(first_records, terminal_lf=False)
    return {
        "file_and_directory_records": len(first_records),
        "full_tree_sha256": sha256_bytes(payload),
    }


def remove_test_tree(path: Path) -> None:
    """Test-only cleanup helper; refuses anything except a non-symlink directory."""

    absolute = _lexical_absolute(path)
    require(_path_exists(absolute), "cleanup tree does not exist")
    status = os.lstat(absolute)
    require(stat.S_ISDIR(status.st_mode) and not stat.S_ISLNK(status.st_mode), "cleanup target is not a real directory")
    shutil.rmtree(absolute)
