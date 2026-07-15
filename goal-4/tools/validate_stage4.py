#!/usr/bin/env python3
"""Validate the frozen Goal 4 implementation/proof package.

This is the outer trust anchor for Stage 4.  The implementation lock binds this
validator, every other accepted Stage 4 contract, schema, implementation, and
test, plus the exact Stage 1--3 validators it executes.  Only the lock itself
is absent from its artifact list.  A caller must supply the independently
recorded lock digest, which avoids a content-hash cycle without leaving this
validator mutable or unbound.

The default mode proves package/upstream/raw-input integrity and the current
SOURCE_BLOCKED gate.  It intentionally reports a quick result, not Stage 4
closure.  ``--mode full`` additionally runs the normal/optimized/external-CWD
test matrix and two clean zero-repair builds through the separately locked
conservation verifier.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping, Sequence


class Stage4ValidationError(RuntimeError):
    """The Stage 4 outer proof failed closed."""


LOCK_RELATIVE = PurePosixPath("goal-4/stage4-implementation-lock.json")

LOCK_ID = "ANKOS-STAGE4-IMPLEMENTATION-LOCK-1"
SCHEMA_VERSION = "1.0.0"
LOCK_STATUS = "FROZEN_STAGE_4_IMPLEMENTATION_SOURCE_BLOCKED"
REGULAR_FILE = "REGULAR_FILE"
LEGACY_RELATIVE = PurePosixPath("ref/A-New-Kind-of-Science")
REPAIRED_RELATIVE = PurePosixPath("ref/A-New-Kind-of-Science-Repaired")
EXPECTED_LEGACY_COUNTS = {"all_regular_files": 1463, "jpeg": 1444, "markdown": 19}
EXPECTED_DOCUMENTS = 29
EXPECTED_SOURCE_BLOCKS = 20_430
EXPECTED_TAPE_ROWS = 20_431
EXPECTED_MONOLITH_BYTES = 3_780_628
EXPECTED_MONOLITH_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"


def _artifact_rows() -> tuple[tuple[str, str], ...]:
    """Return the exact accepted artifact surface in canonical path order."""

    rows = {
        # Direct upstream trust and raw-state bindings.
        "goal-4/baseline-lock.json": "UPSTREAM_LOCK",
        "goal-4/compatibility-baseline.json": "UPSTREAM_STATE",
        "goal-4/corpus-manifest.json": "UPSTREAM_STATE",
        "goal-4/fidelity-contract.md": "UPSTREAM_CONTRACT",
        "goal-4/guardrails.json": "UPSTREAM_CONTRACT",
        "goal-4/licensing-contract.json": "UPSTREAM_CONTRACT",
        "goal-4/promotion-contract.md": "UPSTREAM_CONTRACT",
        "goal-4/review-contract.md": "UPSTREAM_CONTRACT",
        "goal-4/structure-ledger.jsonl": "UPSTREAM_STATE",
        "goal-4/style-guide.md": "UPSTREAM_CONTRACT",
        "goal-4/witness-contract.json": "UPSTREAM_CONTRACT",
        "goal-4/witness-lock.json": "UPSTREAM_LOCK",
        "goal-4/witness-mount-contract.md": "UPSTREAM_CONTRACT",
        "goal-4/witness-state.json": "UPSTREAM_STATE",
        # Stage 4 contracts and nested implementation locks.
        "goal-4/pipeline-contract.json": "CONTRACT",
        "goal-4/pipeline-schema-lock.json": "IMPLEMENTATION_LOCK",
        "goal-4/zero-repair-contract.json": "CONTRACT",
        "goal-4/zero-repair-implementation-lock.json": "IMPLEMENTATION_LOCK",
        # Closed Stage 4 schemas.
        "goal-4/schemas/ast-node.schema.json": "SCHEMA",
        "goal-4/schemas/common.schema.json": "SCHEMA",
        "goal-4/schemas/compatibility-verification.schema.json": "SCHEMA",
        "goal-4/schemas/corpus-manifest.schema.json": "SCHEMA",
        "goal-4/schemas/figure-record.schema.json": "SCHEMA",
        "goal-4/schemas/navigation-record.schema.json": "SCHEMA",
        "goal-4/schemas/provenance-record.schema.json": "SCHEMA",
        "goal-4/schemas/release-manifest.schema.json": "SCHEMA",
        "goal-4/schemas/repair-record.schema.json": "SCHEMA",
        "goal-4/schemas/review-record.schema.json": "SCHEMA",
        "goal-4/schemas/technical-record.schema.json": "SCHEMA",
        "goal-4/schemas/unresolved-record.schema.json": "SCHEMA",
        "goal-4/schemas/workflow.schema.json": "SCHEMA",
        # Stage 4 implementations and exact nested entry points.
        "goal-4/tools/build_zero_repair.py": "TOOL",
        "goal-4/tools/overlay_lib.py": "TOOL",
        "goal-4/tools/overlay_registry.py": "TOOL",
        "goal-4/tools/pipeline_schema_lib.py": "TOOL",
        "goal-4/tools/validate_pipeline_schemas.py": "TOOL",
        "goal-4/tools/validate_stage4.py": "TOOL",
        "goal-4/tools/validate_zero_repair.py": "TOOL",
        "goal-4/tools/zero_repair_lib.py": "TOOL",
        "goal-4/tools/zero_repair_verify.py": "TOOL",
        # Stage 1--3 entry points are pinned here because their own one-way
        # locks intentionally exclude the entry-point validator.
        "goal-4/tools/validate_baseline.py": "UPSTREAM_VALIDATOR",
        "goal-4/tools/validate_guardrails.py": "UPSTREAM_VALIDATOR",
        "goal-4/tools/validate_witness.py": "UPSTREAM_VALIDATOR",
        # The complete accepted Stage 4 test surface.
        "goal-4/tests/test_overlay.py": "TEST",
        "goal-4/tests/test_overlay_registry.py": "TEST",
        "goal-4/tests/test_pipeline_schemas.py": "TEST",
        "goal-4/tests/test_stage4.py": "TEST",
        "goal-4/tests/test_zero_repair.py": "TEST",
    }
    return tuple(sorted(rows.items()))


EXPECTED_ARTIFACT_ROWS = _artifact_rows()
EXPECTED_ARTIFACT_PATHS = tuple(path for path, _ in EXPECTED_ARTIFACT_ROWS)
EXPECTED_CATEGORY_BY_PATH = dict(EXPECTED_ARTIFACT_ROWS)

EXPECTED_VALIDATORS = (
    ("goal-4/tools/validate_guardrails.py", "GUARDRAILS OK"),
    ("goal-4/tools/validate_baseline.py", "BASELINE OK "),
    ("goal-4/tools/validate_witness.py", "WITNESS OK "),
    (
        "goal-4/tools/validate_pipeline_schemas.py",
        "Stage 4 pipeline schema validation: PASS ",
    ),
)
EXPECTED_TESTS = (
    "goal-4/tests/test_overlay.py",
    "goal-4/tests/test_overlay_registry.py",
    "goal-4/tests/test_pipeline_schemas.py",
    "goal-4/tests/test_stage4.py",
    "goal-4/tests/test_zero_repair.py",
)
EXPECTED_MATRIX_MODES = ("NORMAL", "OPTIMIZED")
EXPECTED_MATRIX_CWDS = ("REPOSITORY_ROOT", "EXTERNAL_TMP")

EXPECTED_LOCK_KEYS = {
    "artifacts",
    "bindings",
    "lock_id",
    "matrix",
    "schema_version",
    "stable_zero_repair_proof",
    "status",
    "trust_chain",
}
EXPECTED_BINDING_KEYS = {
    "baseline_lock_sha256",
    "compatibility_baseline_sha256",
    "corpus_manifest_sha256",
    "guardrails_sha256",
    "legacy_allowlist_sha256",
    "pipeline_schema_lock_sha256",
    "structure_ledger_sha256",
    "witness_lock_sha256",
    "witness_state_sha256",
    "zero_repair_contract_sha256",
    "zero_repair_implementation_lock_sha256",
}
EXPECTED_PROOF_KEYS = {
    "canonical_documents",
    "full_tree_sha256",
    "inverse_byte_size",
    "inverse_sha256",
    "manifest_sha256",
    "payload_tree_sha256",
    "projection_tape_rows",
    "projection_tape_sha256",
    "proof_sha256",
    "source_blocks",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Stage4ValidationError(message)


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _require_sha256(value: Any, label: str) -> str:
    _require(
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value),
        f"{label} is not a lowercase SHA-256",
    )
    return value


def _reject_float(value: Any) -> None:
    if isinstance(value, float):
        raise Stage4ValidationError("canonical JSON contains a floating-point value")
    if isinstance(value, dict):
        for key, child in value.items():
            _require(isinstance(key, str), "canonical JSON contains a non-string key")
            _reject_float(child)
    elif isinstance(value, list):
        for child in value:
            _reject_float(child)


def canonical_json_bytes(value: Any, *, terminal_lf: bool = True) -> bytes:
    _reject_float(value)
    try:
        payload = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise Stage4ValidationError("value is not canonical-JSON serializable") from error
    return payload + (b"\n" if terminal_lf else b"")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise Stage4ValidationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_json_float(_: str) -> Any:
    raise Stage4ValidationError("JSON contains a floating-point value")


def parse_json_bytes(raw: bytes, label: str, *, canonical: bool) -> Any:
    _require(not raw.startswith(b"\xef\xbb\xbf"), f"{label} has a UTF-8 BOM")
    try:
        decoded = raw.decode("utf-8", errors="strict")
        value = json.loads(
            decoded,
            object_pairs_hook=_unique_object,
            parse_float=_reject_json_float,
            parse_constant=_reject_json_float,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError) as error:
        raise Stage4ValidationError(f"{label} is not strict JSON") from error
    _reject_float(value)
    if canonical:
        _require(canonical_json_bytes(value) == raw, f"{label} is not canonical ANKOS-CJ-1")
    return value


def safe_relative(value: Any, label: str) -> PurePosixPath:
    _require(isinstance(value, str) and bool(value), f"{label} is not a nonempty string")
    _require(
        "\\" not in value and "\x00" not in value and "%" not in value,
        f"{label} uses unsafe path spelling",
    )
    _require(
        all(ord(character) >= 32 and ord(character) != 127 for character in value),
        f"{label} contains a control character",
    )
    relative = PurePosixPath(value)
    _require(not relative.is_absolute(), f"{label} is absolute")
    _require(
        relative.as_posix() == value
        and all(part not in {"", ".", ".."} for part in relative.parts),
        f"{label} is not a normalized relative path",
    )
    return relative


def _absolute(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))


def _join(root: Path, relative: PurePosixPath) -> Path:
    return root.joinpath(*relative.parts)


def _lexists(path: Path) -> bool:
    return os.path.lexists(os.fspath(path))


def _assert_no_symlink_chain(path: Path, label: str) -> None:
    absolute = _absolute(path)
    for component in [*reversed(absolute.parents), absolute]:
        if _lexists(component):
            _require(
                not stat.S_ISLNK(os.lstat(component).st_mode),
                f"{label} has a symlink path component",
            )


def _plain_directory(path: Path, label: str) -> os.stat_result:
    _assert_no_symlink_chain(path, label)
    _require(_lexists(path), f"{label} does not exist")
    status = os.lstat(path)
    _require(
        stat.S_ISDIR(status.st_mode) and not stat.S_ISLNK(status.st_mode),
        f"{label} is not a real directory",
    )
    return status


def read_plain_file(path: Path, label: str) -> tuple[bytes, os.stat_result]:
    """Read a direct, single-linked regular file with before/after identity checks."""

    _assert_no_symlink_chain(path, label)
    _require(_lexists(path), f"{label} is missing")
    before = os.lstat(path)
    _require(
        stat.S_ISREG(before.st_mode) and not stat.S_ISLNK(before.st_mode),
        f"{label} is not a regular file",
    )
    _require(before.st_nlink == 1, f"{label} is hardlinked")
    _require(stat.S_IMODE(before.st_mode) & 0o7111 == 0, f"{label} has executable or special mode bits")
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags)
    try:
        opened = os.fstat(descriptor)
        _require(
            stat.S_ISREG(opened.st_mode)
            and (opened.st_dev, opened.st_ino) == (before.st_dev, before.st_ino),
            f"{label} changed while opening",
        )
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after_fd = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    after_path = os.lstat(path)
    identity = lambda item: (
        item.st_dev,
        item.st_ino,
        item.st_mode,
        item.st_nlink,
        item.st_size,
        item.st_mtime_ns,
        item.st_ctime_ns,
    )
    _require(
        identity(before) == identity(opened) == identity(after_fd) == identity(after_path),
        f"{label} mutated while reading",
    )
    payload = b"".join(chunks)
    _require(len(payload) == before.st_size, f"{label} byte-size changed while reading")
    return payload, before


def _exact_keys(value: Any, expected: set[str], label: str) -> Mapping[str, Any]:
    _require(isinstance(value, dict), f"{label} is not an object")
    _require(set(value) == expected, f"{label} field set drift")
    return value


def _artifact_map(lock: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    rows = lock["artifacts"]
    _require(isinstance(rows, list), "outer-lock artifacts is not an array")
    paths: list[str] = []
    result: dict[str, Mapping[str, Any]] = {}
    for index, candidate in enumerate(rows):
        row = _exact_keys(
            candidate,
            {"byte_size", "category", "path", "sha256", "type"},
            f"outer-lock artifact {index}",
        )
        relative = safe_relative(row["path"], f"outer-lock artifact {index} path")
        path = relative.as_posix()
        _require(path.startswith("goal-4/"), f"outer-lock artifact escapes Goal 4: {path}")
        _require(path not in result, f"duplicate outer-lock artifact path: {path}")
        _require(row["type"] == REGULAR_FILE, f"outer-lock artifact type drift: {path}")
        _require(
            type(row["byte_size"]) is int and row["byte_size"] >= 0,
            f"outer-lock artifact byte-size drift: {path}",
        )
        _require_sha256(row["sha256"], f"outer-lock artifact digest: {path}")
        _require(
            row["category"] == EXPECTED_CATEGORY_BY_PATH.get(path),
            f"outer-lock artifact category/path drift: {path}",
        )
        result[path] = row
        paths.append(path)
    _require(tuple(paths) == EXPECTED_ARTIFACT_PATHS, "outer-lock artifact path set/order drift")
    return result


def _load_outer_lock(
    repo: Path, expected_lock_sha256: str
) -> tuple[Mapping[str, Any], dict[str, Mapping[str, Any]], bytes]:
    _require_sha256(expected_lock_sha256, "caller-supplied Stage 4 outer-lock digest")
    lock_path = _join(repo, LOCK_RELATIVE)
    raw, _ = read_plain_file(lock_path, "Stage 4 outer implementation lock")
    _require(
        _sha256(raw) == expected_lock_sha256,
        "Stage 4 outer implementation lock digest drift",
    )
    lock = parse_json_bytes(raw, "Stage 4 outer implementation lock", canonical=True)
    lock = _exact_keys(lock, EXPECTED_LOCK_KEYS, "Stage 4 outer implementation lock")
    _require(lock["lock_id"] == LOCK_ID, "Stage 4 outer lock identity drift")
    _require(lock["schema_version"] == SCHEMA_VERSION, "Stage 4 outer lock schema drift")
    _require(lock["status"] == LOCK_STATUS, "Stage 4 outer lock status drift")
    artifacts = _artifact_map(lock)
    _validate_lock_metadata(lock)
    return lock, artifacts, raw


def _validate_lock_metadata(lock: Mapping[str, Any]) -> None:
    bindings = _exact_keys(lock["bindings"], EXPECTED_BINDING_KEYS, "outer-lock bindings")
    for key, value in bindings.items():
        _require_sha256(value, f"outer-lock binding {key}")

    matrix = _exact_keys(
        lock["matrix"],
        {
            "cwd_profiles",
            "modes",
            "test_paths",
            "validator_paths",
            "zero_build_cli",
            "zero_validate_cli",
        },
        "outer-lock matrix",
    )
    _require(tuple(matrix["modes"]) == EXPECTED_MATRIX_MODES, "outer-lock matrix modes drift")
    _require(tuple(matrix["cwd_profiles"]) == EXPECTED_MATRIX_CWDS, "outer-lock matrix CWD profiles drift")
    _require(tuple(matrix["test_paths"]) == EXPECTED_TESTS, "outer-lock matrix tests drift")
    _require(
        tuple(matrix["validator_paths"]) == tuple(path for path, _ in EXPECTED_VALIDATORS),
        "outer-lock matrix validators drift",
    )
    _require(matrix["zero_build_cli"] == "goal-4/tools/build_zero_repair.py", "outer-lock build CLI drift")
    _require(matrix["zero_validate_cli"] == "goal-4/tools/validate_zero_repair.py", "outer-lock zero validator drift")

    proof = _exact_keys(
        lock["stable_zero_repair_proof"],
        EXPECTED_PROOF_KEYS,
        "outer-lock stable zero-repair proof",
    )
    _validate_zero_proof(proof)

    trust = _exact_keys(
        lock["trust_chain"],
        {
            "lock_digest_external_argument_required",
            "lock_excluded_from_artifacts",
            "validator_relative_path",
        },
        "outer-lock trust chain",
    )
    _require(trust["lock_digest_external_argument_required"] is True, "outer-lock external pin requirement drift")
    _require(trust["lock_excluded_from_artifacts"] is True, "outer-lock self-hash exclusion drift")
    _require(trust["validator_relative_path"] == "goal-4/tools/validate_stage4.py", "outer-lock validator path drift")
    _require(
        trust["validator_relative_path"] in EXPECTED_ARTIFACT_PATHS,
        "outer lock does not bind its validator",
    )
    _require(LOCK_RELATIVE.as_posix() not in EXPECTED_ARTIFACT_PATHS, "outer lock contains a circular self-hash")


def _verify_artifact(repo: Path, row: Mapping[str, Any]) -> tuple[int, int, int, int, int, int, str]:
    relative = safe_relative(row["path"], "locked artifact path")
    payload, status = read_plain_file(_join(repo, relative), f"locked artifact {relative.as_posix()}")
    _require(len(payload) == row["byte_size"], f"locked artifact byte-size drift: {relative.as_posix()}")
    digest = _sha256(payload)
    _require(digest == row["sha256"], f"locked artifact digest drift: {relative.as_posix()}")
    return (
        status.st_dev,
        status.st_ino,
        status.st_mode,
        status.st_nlink,
        status.st_size,
        status.st_mtime_ns,
        digest,
    )


def validate_locked_artifacts(
    repo: Path, artifacts: Mapping[str, Mapping[str, Any]]
) -> dict[str, tuple[int, int, int, int, int, int, str]]:
    return {path: _verify_artifact(repo, artifacts[path]) for path in EXPECTED_ARTIFACT_PATHS}


def _locked_digest(artifacts: Mapping[str, Mapping[str, Any]], path: str) -> str:
    _require(path in artifacts, f"outer lock omits binding target: {path}")
    return str(artifacts[path]["sha256"])


def _validate_direct_bindings(
    repo: Path, lock: Mapping[str, Any], artifacts: Mapping[str, Mapping[str, Any]]
) -> None:
    bindings = lock["bindings"]
    targets = {
        "baseline_lock_sha256": "goal-4/baseline-lock.json",
        "compatibility_baseline_sha256": "goal-4/compatibility-baseline.json",
        "corpus_manifest_sha256": "goal-4/corpus-manifest.json",
        "guardrails_sha256": "goal-4/guardrails.json",
        "pipeline_schema_lock_sha256": "goal-4/pipeline-schema-lock.json",
        "structure_ledger_sha256": "goal-4/structure-ledger.jsonl",
        "witness_lock_sha256": "goal-4/witness-lock.json",
        "witness_state_sha256": "goal-4/witness-state.json",
        "zero_repair_contract_sha256": "goal-4/zero-repair-contract.json",
        "zero_repair_implementation_lock_sha256": "goal-4/zero-repair-implementation-lock.json",
    }
    for binding, path in targets.items():
        _require(bindings[binding] == _locked_digest(artifacts, path), f"outer-lock binding drift: {binding}")
    _validate_nested_locks(repo, lock)


def _load_canonical_object(repo: Path, relative: str, label: str) -> Mapping[str, Any]:
    raw, _ = read_plain_file(_join(repo, safe_relative(relative, label)), label)
    return _exact_keys_or_object(parse_json_bytes(raw, label, canonical=True), label)


def _exact_keys_or_object(value: Any, label: str) -> Mapping[str, Any]:
    _require(isinstance(value, dict), f"{label} is not an object")
    return value


def _validate_nested_locks(repo: Path, lock: Mapping[str, Any]) -> None:
    bindings = lock["bindings"]
    baseline = _load_canonical_object(repo, "goal-4/baseline-lock.json", "baseline lock")
    witness = _load_canonical_object(repo, "goal-4/witness-lock.json", "witness lock")
    pipeline = _load_canonical_object(repo, "goal-4/pipeline-schema-lock.json", "pipeline schema lock")
    zero = _load_canonical_object(repo, "goal-4/zero-repair-implementation-lock.json", "zero-repair implementation lock")
    _require(baseline.get("status") == "FROZEN_STAGE_2_BASELINE", "baseline lock status drift")
    _require(witness.get("status") == "FROZEN_STAGE_3_SOURCE_BLOCKED", "witness lock status drift")
    _require(pipeline.get("status") == "FROZEN_STAGE_4_SCHEMA_SOURCE_BLOCKED", "pipeline schema lock status drift")
    _require(zero.get("lock_id") == "ANKOS-ZERO-REPAIR-IMPLEMENTATION-LOCK-1", "zero-repair lock identity drift")
    _require(zero.get("schema_version") == SCHEMA_VERSION, "zero-repair lock schema drift")
    _require(
        witness.get("bindings", {}).get("baseline_lock_sha256") == bindings["baseline_lock_sha256"],
        "witness/baseline lock join drift",
    )
    _require(
        pipeline.get("bindings", {}).get("baseline_lock_sha256") == bindings["baseline_lock_sha256"]
        and pipeline.get("bindings", {}).get("witness_lock_sha256") == bindings["witness_lock_sha256"]
        and pipeline.get("bindings", {}).get("guardrails_sha256") == bindings["guardrails_sha256"],
        "pipeline/upstream lock join drift",
    )


def legacy_allowlist_digest(rows: Sequence[Mapping[str, Any]]) -> str:
    projected: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        _require(isinstance(row, dict), f"corpus raw-input row {index} is not an object")
        relative = safe_relative(row.get("relative_path"), f"corpus raw-input row {index} path")
        kind = row.get("kind")
        _require(kind in {"MARKDOWN", "JPEG"}, f"corpus raw-input row {index} kind drift")
        _require(type(row.get("byte_size")) is int and row["byte_size"] >= 0, f"corpus raw-input row {index} size drift")
        digest = _require_sha256(row.get("sha256"), f"corpus raw-input row {index} digest")
        projected.append(
            {
                "byte_size": row["byte_size"],
                "kind": kind,
                "path": relative.as_posix(),
                "sha256": digest,
            }
        )
    payload = b"ANKOS-STAGE4-LEGACY-ALLOWLIST-1\0" + canonical_json_bytes(projected, terminal_lf=False)
    return _sha256(payload)


def validate_legacy_allowlist(repo: Path, expected_digest: str) -> Mapping[str, Any]:
    legacy = _join(repo, LEGACY_RELATIVE)
    _plain_directory(legacy, "legacy root")
    manifest = _load_canonical_object(repo, "goal-4/corpus-manifest.json", "corpus manifest")
    rows = manifest.get("raw_inputs")
    _require(isinstance(rows, list), "corpus manifest raw_inputs is not an array")
    _require(manifest.get("counts") == EXPECTED_LEGACY_COUNTS, "corpus manifest legacy counts drift")
    allowlist_digest = legacy_allowlist_digest(rows)
    _require(allowlist_digest == expected_digest, "legacy allowlist digest drift")

    expected: dict[str, Mapping[str, Any]] = {}
    kind_counts = {"MARKDOWN": 0, "JPEG": 0}
    for row in rows:
        path = safe_relative(row["relative_path"], "legacy allowlist path").as_posix()
        _require(path not in expected, f"duplicate legacy allowlist path: {path}")
        expected[path] = row
        kind_counts[row["kind"]] += 1
    _require(len(expected) == EXPECTED_LEGACY_COUNTS["all_regular_files"], "legacy allowlist count drift")
    _require(kind_counts == {"MARKDOWN": 19, "JPEG": 1444}, "legacy allowlist kind counts drift")

    actual: set[str] = set()
    directory_count = 0
    for current, directory_names, file_names in os.walk(legacy, topdown=True, followlinks=False):
        current_path = Path(current)
        _plain_directory(current_path, "legacy directory")
        directory_count += 1
        for name in list(directory_names):
            child = current_path / name
            status = os.lstat(child)
            _require(
                stat.S_ISDIR(status.st_mode) and not stat.S_ISLNK(status.st_mode),
                f"legacy tree contains a non-directory or symlink directory: {child}",
            )
        for name in file_names:
            child = current_path / name
            relative = child.relative_to(legacy).as_posix()
            status = os.lstat(child)
            _require(stat.S_ISREG(status.st_mode) and not stat.S_ISLNK(status.st_mode), f"legacy tree contains a non-regular file: {relative}")
            _require(status.st_nlink == 1, f"legacy file is hardlinked: {relative}")
            actual.add(relative)
    expected_directories = manifest.get("totals", {}).get("directory_count_including_root")
    _require(type(expected_directories) is int and directory_count == expected_directories, "legacy directory-count drift")
    _require(actual == set(expected), "legacy filesystem path set differs from explicit allowlist")

    sequence = hashlib.sha256(b"ANKOS-STAGE4-LEGACY-CONTENT-1\0")
    for path in sorted(expected):
        row = expected[path]
        payload, _ = read_plain_file(_join(legacy, safe_relative(path, "legacy file path")), f"legacy file {path}")
        _require(len(payload) == row["byte_size"], f"legacy byte-size drift: {path}")
        digest = _sha256(payload)
        _require(digest == row["sha256"], f"legacy content digest drift: {path}")
        encoded_path = path.encode("utf-8")
        sequence.update(len(encoded_path).to_bytes(8, "big"))
        sequence.update(encoded_path)
        sequence.update(bytes.fromhex(digest))
    return {
        "allowlist_sha256": allowlist_digest,
        "content_sequence_sha256": sequence.hexdigest(),
        "directory_count": directory_count,
        "regular_files": len(actual),
    }


def validate_empty_sibling(repo: Path) -> Mapping[str, Any]:
    sibling = _join(repo, REPAIRED_RELATIVE)
    status = _plain_directory(sibling, "repaired sibling")
    with os.scandir(sibling) as entries:
        names = [entry.name for entry in entries]
    _require(not names, "repaired sibling is not empty")
    return {
        "device": status.st_dev,
        "inode": status.st_ino,
        "mode": stat.S_IMODE(status.st_mode),
        "mtime_ns": status.st_mtime_ns,
        "entries": (),
    }


def _validate_source_blocked(repo: Path, lock: Mapping[str, Any]) -> Mapping[str, Any]:
    state = _load_canonical_object(repo, "goal-4/witness-state.json", "witness state")
    _require(state.get("contract_id") == "ANKOS-WITNESS-1", "witness state contract drift")
    _require(state.get("schema_version") == SCHEMA_VERSION, "witness state schema drift")
    _require(state.get("status") == "SOURCE_BLOCKED", "witness is no longer in the frozen SOURCE_BLOCKED state")
    coverage = state.get("coverage")
    acquisition = state.get("acquisition")
    gates = state.get("stage_gates")
    _require(isinstance(coverage, dict) and isinstance(acquisition, dict) and isinstance(gates, dict), "witness gate sections missing")
    _require(
        coverage.get("covered_segment_count") == 0
        and coverage.get("blocked_segment_count") == EXPECTED_DOCUMENTS
        and coverage.get("raw_block_count") == EXPECTED_SOURCE_BLOCKS,
        "SOURCE_BLOCKED coverage arithmetic drift",
    )
    _require(
        acquisition.get("primary_witness_acquired") is False
        and acquisition.get("authorized_read_only_mount_configured") is False
        and acquisition.get("permission_or_license_id") is None,
        "SOURCE_BLOCKED acquisition state drift",
    )
    _require(
        gates.get("stage_4_dependency_independent_pipeline_work") == "ALLOWED"
        and gates.get("author_text_correction") == "BLOCKED"
        and gates.get("full_repair_claim") == "BLOCKED",
        "SOURCE_BLOCKED stage gates drift",
    )
    pipeline = _load_canonical_object(repo, "goal-4/pipeline-contract.json", "pipeline contract")
    current = pipeline.get("current_gates")
    _require(isinstance(current, dict), "pipeline current gates missing")
    _require(
        current.get("witness_status") == "SOURCE_BLOCKED"
        and current.get("author_text_token_changes_allowed") is False
        and current.get("witness_only_text_insertions_allowed") is False
        and current.get("witness_asset_insertions_allowed") is False
        and current.get("audit_certification_allowed") is False,
        "pipeline SOURCE_BLOCKED gate drift",
    )
    _require(
        lock["bindings"]["witness_state_sha256"]
        == _sha256(read_plain_file(_join(repo, PurePosixPath("goal-4/witness-state.json")), "witness state")[0]),
        "outer lock/witness state join drift",
    )
    return {"blocked_segments": EXPECTED_DOCUMENTS, "raw_blocks": EXPECTED_SOURCE_BLOCKS, "status": "SOURCE_BLOCKED"}


def stable_zero_proof_digest(proof_without_digest: Mapping[str, Any]) -> str:
    payload = b"ANKOS-STAGE4-ZERO-PROOF-1\0" + canonical_json_bytes(
        dict(proof_without_digest), terminal_lf=False
    )
    return _sha256(payload)


def _validate_zero_proof(proof: Mapping[str, Any]) -> None:
    for key in (
        "full_tree_sha256",
        "inverse_sha256",
        "manifest_sha256",
        "payload_tree_sha256",
        "projection_tape_sha256",
        "proof_sha256",
    ):
        _require_sha256(proof[key], f"stable zero-repair proof {key}")
    for key in ("canonical_documents", "source_blocks", "projection_tape_rows", "inverse_byte_size"):
        _require(type(proof[key]) is int, f"stable zero-repair proof {key} is not an integer")
    _require(proof["canonical_documents"] == EXPECTED_DOCUMENTS, "stable zero-repair document count drift")
    _require(proof["source_blocks"] == EXPECTED_SOURCE_BLOCKS, "stable zero-repair source-block count drift")
    _require(proof["projection_tape_rows"] == EXPECTED_TAPE_ROWS, "stable zero-repair tape-row count drift")
    _require(proof["inverse_byte_size"] == EXPECTED_MONOLITH_BYTES, "stable zero-repair inverse size drift")
    _require(proof["inverse_sha256"] == EXPECTED_MONOLITH_SHA256, "stable zero-repair inverse digest drift")
    core = {key: value for key, value in proof.items() if key != "proof_sha256"}
    _require(proof["proof_sha256"] == stable_zero_proof_digest(core), "stable zero-repair proof digest drift")


def _validate_zero_contract(repo: Path, lock: Mapping[str, Any]) -> None:
    contract = _load_canonical_object(repo, "goal-4/zero-repair-contract.json", "zero-repair contract")
    proof = lock["stable_zero_repair_proof"]
    _require(contract.get("contract_id") == "ANKOS-ZERO-REPAIR-1", "zero-repair contract identity drift")
    _require(contract.get("schema_version") == SCHEMA_VERSION, "zero-repair contract schema drift")
    counts = contract.get("counts")
    contract_proof = contract.get("proof")
    _require(isinstance(counts, dict) and isinstance(contract_proof, dict), "zero-repair contract sections missing")
    _require(
        counts.get("canonical_documents") == proof["canonical_documents"]
        and counts.get("source_blocks") == proof["source_blocks"]
        and counts.get("projection_tape_rows") == proof["projection_tape_rows"],
        "zero-repair contract/outer proof count join drift",
    )
    _require(
        contract_proof.get("inverse_sha256") == proof["inverse_sha256"]
        and contract_proof.get("projection_tape_sha256") == proof["projection_tape_sha256"]
        and contract_proof.get("payload_tree_sha256_excluding_manifest") == proof["payload_tree_sha256"],
        "zero-repair contract/outer proof digest join drift",
    )


def _runtime_path(repo: Path) -> None:
    declared = _join(repo, PurePosixPath("goal-4/tools/validate_stage4.py"))
    actual = _absolute(Path(__file__))
    _require(actual == declared, "executed Stage 4 validator path differs from declared path")
    read_plain_file(declared, "declared Stage 4 validator")


def _subprocess_environment() -> dict[str, str]:
    environment = dict(os.environ)
    for key in list(environment):
        if key.upper() in {"PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP", "PYTHONINSPECT"}:
            environment.pop(key, None)
    environment.update(
        {
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONHASHSEED": "0",
            "PYTHONNOUSERSITE": "1",
            "TZ": "UTC",
        }
    )
    return environment


def _run_command(
    command: Sequence[str],
    *,
    cwd: Path,
    label: str,
    timeout: int = 900,
) -> tuple[bytes, bytes]:
    try:
        result = subprocess.run(
            list(command),
            cwd=cwd,
            env=_subprocess_environment(),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise Stage4ValidationError(f"{label} could not complete: {error}") from error
    if result.returncode != 0:
        stdout = result.stdout[-8000:].decode("utf-8", errors="replace")
        stderr = result.stderr[-8000:].decode("utf-8", errors="replace")
        raise Stage4ValidationError(
            f"{label} failed with exit {result.returncode}; stdout={stdout!r}; stderr={stderr!r}"
        )
    return result.stdout, result.stderr


def _python_command(script: Path, *, optimized: bool, arguments: Iterable[str] = ()) -> list[str]:
    interpreter = _absolute(Path(sys.executable))
    command = [os.fspath(interpreter)]
    if optimized:
        command.append("-O")
    command.extend(["-B", os.fspath(script), *arguments])
    return command


def _require_validator_output(stdout: bytes, stderr: bytes, prefix: str, label: str) -> None:
    _require(not stderr, f"{label} wrote to stderr on success")
    _require(stdout.endswith(b"\n") and stdout.count(b"\n") == 1, f"{label} success output shape drift")
    try:
        decoded = stdout.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise Stage4ValidationError(f"{label} emitted non-UTF-8 output") from error
    _require(decoded.startswith(prefix), f"{label} success prefix drift")


def _run_validator(
    repo: Path,
    artifacts: Mapping[str, Mapping[str, Any]],
    path: str,
    prefix: str,
    *,
    optimized: bool,
    cwd: Path,
) -> None:
    _verify_artifact(repo, artifacts[path])
    script = _join(repo, safe_relative(path, "validator path"))
    stdout, stderr = _run_command(
        _python_command(script, optimized=optimized, arguments=("--repo-root", os.fspath(repo))),
        cwd=cwd,
        label=f"validator {path} ({'optimized' if optimized else 'normal'}, cwd={cwd})",
    )
    _require_validator_output(stdout, stderr, prefix, f"validator {path}")
    _verify_artifact(repo, artifacts[path])


def _run_test(
    repo: Path,
    artifacts: Mapping[str, Mapping[str, Any]],
    path: str,
    *,
    optimized: bool,
    cwd: Path,
) -> None:
    _verify_artifact(repo, artifacts[path])
    script = _join(repo, safe_relative(path, "test path"))
    _run_command(
        _python_command(script, optimized=optimized),
        cwd=cwd,
        label=f"test {path} ({'optimized' if optimized else 'normal'}, cwd={cwd})",
    )
    _verify_artifact(repo, artifacts[path])


def _parse_prefixed_json(stdout: bytes, stderr: bytes, prefix: str, label: str) -> Mapping[str, Any]:
    _require(not stderr, f"{label} wrote to stderr on success")
    prefix_bytes = prefix.encode("utf-8")
    _require(stdout.startswith(prefix_bytes) and stdout.endswith(b"\n"), f"{label} output envelope drift")
    raw = stdout[len(prefix_bytes) :]
    value = parse_json_bytes(raw, f"{label} result", canonical=True)
    _require(isinstance(value, dict), f"{label} result is not an object")
    return value


def _zero_result_core(result: Mapping[str, Any], full_tree_sha256: str) -> dict[str, Any]:
    core = {
        "canonical_documents": result.get("canonical_documents"),
        "full_tree_sha256": full_tree_sha256,
        "inverse_byte_size": result.get("inverse_byte_size"),
        "inverse_sha256": result.get("inverse_sha256"),
        "manifest_sha256": result.get("manifest_sha256"),
        "payload_tree_sha256": result.get("payload_tree_sha256"),
        "projection_tape_rows": result.get("projection_tape_rows"),
        "projection_tape_sha256": result.get("projection_tape_sha256"),
        "source_blocks": result.get("source_blocks"),
    }
    for key in ("full_tree_sha256", "inverse_sha256", "manifest_sha256", "payload_tree_sha256", "projection_tape_sha256"):
        _require_sha256(core[key], f"runtime zero-repair result {key}")
    return core


def _run_zero_builds(
    repo: Path,
    artifacts: Mapping[str, Mapping[str, Any]],
    expected_proof: Mapping[str, Any],
    work: Path,
) -> Mapping[str, Any]:
    first = work / "zero-a"
    second = work / "zero-b"
    build_path = "goal-4/tools/build_zero_repair.py"
    validate_path = "goal-4/tools/validate_zero_repair.py"
    _verify_artifact(repo, artifacts[build_path])
    stdout, stderr = _run_command(
        _python_command(
            _join(repo, safe_relative(build_path, "zero build CLI")),
            optimized=False,
            arguments=(
                "--repo-root",
                os.fspath(repo),
                "--output-root",
                os.fspath(first),
                "--comparison-output-root",
                os.fspath(second),
            ),
        ),
        cwd=work,
        label="two fresh zero-repair builds",
        timeout=1200,
    )
    built = _parse_prefixed_json(stdout, stderr, "ZERO-REPAIR BUILD OK ", "zero-repair build")
    comparison = built.get("clean_build_equality")
    second_result = built.get("comparison_build")
    _require(isinstance(comparison, dict) and isinstance(second_result, dict), "zero build comparison evidence missing")
    tree_digest = _require_sha256(comparison.get("full_tree_sha256"), "zero build full-tree digest")
    first_core = _zero_result_core(built, tree_digest)
    second_core = _zero_result_core(second_result, tree_digest)
    _require(first_core == second_core, "two zero-repair build proof results differ")

    _verify_artifact(repo, artifacts[validate_path])
    stdout, stderr = _run_command(
        _python_command(
            _join(repo, safe_relative(validate_path, "zero validation CLI")),
            optimized=False,
            arguments=(
                "--repo-root",
                os.fspath(repo),
                "--output-root",
                os.fspath(first),
                "--compare-root",
                os.fspath(second),
            ),
        ),
        cwd=work,
        label="independent zero-repair validation/comparison",
        timeout=1200,
    )
    validated = _parse_prefixed_json(
        stdout, stderr, "ZERO-REPAIR VALIDATION OK ", "zero-repair validation"
    )
    validation_comparison = validated.get("clean_build_equality")
    validation_second = validated.get("comparison_build")
    _require(
        isinstance(validation_comparison, dict) and isinstance(validation_second, dict),
        "independent zero validation comparison evidence missing",
    )
    validation_tree = _require_sha256(
        validation_comparison.get("full_tree_sha256"), "independent zero full-tree digest"
    )
    validated_core = _zero_result_core(validated, validation_tree)
    validated_second_core = _zero_result_core(validation_second, validation_tree)
    _require(
        first_core == validated_core == validated_second_core,
        "builder and independent validator proof results differ",
    )
    expected_core = {key: value for key, value in expected_proof.items() if key != "proof_sha256"}
    _require(first_core == expected_core, "fresh zero-repair proof differs from frozen outer proof")
    _require(
        stable_zero_proof_digest(first_core) == expected_proof["proof_sha256"],
        "fresh zero-repair stable proof digest drift",
    )
    _verify_artifact(repo, artifacts[build_path])
    _verify_artifact(repo, artifacts[validate_path])
    return {"first": first_core, "second": second_core, "independent": validated_core}


def _git_command(repo: Path, arguments: Sequence[str], label: str) -> bytes:
    git = Path("/usr/bin/git")
    _require(git.is_file(), "Git executable is unavailable for repository scope audit")
    stdout, _ = _run_command(
        [os.fspath(git), "-C", os.fspath(repo), *arguments],
        cwd=repo,
        label=label,
    )
    return stdout


def _git_scope_audit(repo: Path) -> Mapping[str, Any]:
    dot_git = repo / ".git"
    if not _lexists(dot_git):
        return {"state": "NO_GIT_RELOCATED", "changed_paths": ()}
    _require(
        stat.S_ISDIR(os.lstat(dot_git).st_mode) or stat.S_ISREG(os.lstat(dot_git).st_mode),
        ".git is neither a directory nor a worktree file",
    )
    _require(_git_command(repo, ["diff", "--check"], "Git unstaged whitespace audit") == b"", "git diff --check reported findings")
    _require(
        _git_command(repo, ["diff", "--cached", "--check"], "Git staged whitespace audit") == b"",
        "git diff --cached --check reported findings",
    )
    commands = (
        ["diff", "--name-only", "-z"],
        ["diff", "--cached", "--name-only", "-z"],
        ["ls-files", "--others", "--exclude-standard", "-z"],
    )
    paths: set[str] = set()
    for index, arguments in enumerate(commands):
        raw = _git_command(repo, arguments, f"Git scope inventory {index}")
        _require(not raw or raw.endswith(b"\0"), "Git scope inventory framing drift")
        for encoded in raw.split(b"\0"):
            if not encoded:
                continue
            try:
                path = encoded.decode("utf-8", errors="strict")
            except UnicodeDecodeError as error:
                raise Stage4ValidationError("Git scope path is not UTF-8") from error
            normalized = safe_relative(path, "Git scope path").as_posix()
            _require(
                normalized.startswith("goal-4/")
                or normalized == REPAIRED_RELATIVE.as_posix()
                or normalized.startswith(REPAIRED_RELATIVE.as_posix() + "/"),
                f"worktree change escapes Goal 4 authorized roots: {normalized}",
            )
            paths.add(normalized)
    return {"state": "PASS", "changed_paths": tuple(sorted(paths))}


def _static_validation(
    repo: Path, expected_lock_sha256: str,
) -> tuple[
    Mapping[str, Any],
    dict[str, Mapping[str, Any]],
    Mapping[str, Any],
    Mapping[str, Any],
    Mapping[str, Any],
    dict[str, tuple[int, int, int, int, int, int, str]],
]:
    _plain_directory(repo, "repository root")
    _runtime_path(repo)
    lock, artifacts, _ = _load_outer_lock(repo, expected_lock_sha256)
    artifact_snapshot = validate_locked_artifacts(repo, artifacts)
    _validate_direct_bindings(repo, lock, artifacts)
    legacy = validate_legacy_allowlist(repo, lock["bindings"]["legacy_allowlist_sha256"])
    sibling = validate_empty_sibling(repo)
    blocked = _validate_source_blocked(repo, lock)
    _validate_zero_contract(repo, lock)
    return lock, artifacts, legacy, sibling, blocked, artifact_snapshot


def _assert_static_unchanged(
    before_artifacts: Mapping[str, Any],
    after_artifacts: Mapping[str, Any],
    before_legacy: Mapping[str, Any],
    after_legacy: Mapping[str, Any],
    before_sibling: Mapping[str, Any],
    after_sibling: Mapping[str, Any],
) -> None:
    _require(before_artifacts == after_artifacts, "an accepted Stage 4 artifact mutated during validation")
    _require(before_legacy == after_legacy, "legacy inputs mutated during validation")
    _require(before_sibling == after_sibling, "repaired sibling mutated during validation")


def run_lock_only(repo: Path, expected_lock_sha256: str) -> Mapping[str, Any]:
    _plain_directory(repo, "repository root")
    _runtime_path(repo)
    lock, artifacts, _ = _load_outer_lock(repo, expected_lock_sha256)
    validate_locked_artifacts(repo, artifacts)
    _validate_direct_bindings(repo, lock, artifacts)
    _validate_zero_contract(repo, lock)
    return {
        "artifacts": len(artifacts),
        "closure_claim": False,
        "lock_sha256": expected_lock_sha256,
        "mode": "LOCK_ONLY",
    }


def run_quick(repo: Path, expected_lock_sha256: str) -> Mapping[str, Any]:
    lock, artifacts, legacy, sibling, blocked, before_artifacts = _static_validation(
        repo, expected_lock_sha256
    )
    for path, prefix in EXPECTED_VALIDATORS:
        _run_validator(repo, artifacts, path, prefix, optimized=False, cwd=repo)
    after_artifacts = validate_locked_artifacts(repo, artifacts)
    after_legacy = validate_legacy_allowlist(repo, lock["bindings"]["legacy_allowlist_sha256"])
    after_sibling = validate_empty_sibling(repo)
    _assert_static_unchanged(before_artifacts, after_artifacts, legacy, after_legacy, sibling, after_sibling)
    return {
        "artifacts": len(artifacts),
        "closure_claim": False,
        "legacy_files": legacy["regular_files"],
        "lock_sha256": expected_lock_sha256,
        "mode": "QUICK",
        "source_state": blocked["status"],
        "validators": len(EXPECTED_VALIDATORS),
    }


def run_full(repo: Path, expected_lock_sha256: str) -> Mapping[str, Any]:
    lock, artifacts, legacy, sibling, blocked, before_artifacts = _static_validation(
        repo, expected_lock_sha256
    )
    git_before = _git_scope_audit(repo)
    with tempfile.TemporaryDirectory(prefix="ankos-stage4-full-", dir="/tmp") as temporary:
        work = Path(temporary)
        external_cwd = work / "external-cwd"
        external_cwd.mkdir(mode=0o700)
        matrix_runs = 0
        for mode in EXPECTED_MATRIX_MODES:
            optimized = mode == "OPTIMIZED"
            for cwd_profile in EXPECTED_MATRIX_CWDS:
                cwd = repo if cwd_profile == "REPOSITORY_ROOT" else external_cwd
                for path, prefix in EXPECTED_VALIDATORS:
                    _run_validator(repo, artifacts, path, prefix, optimized=optimized, cwd=cwd)
                    matrix_runs += 1
                for path in EXPECTED_TESTS:
                    _run_test(repo, artifacts, path, optimized=optimized, cwd=cwd)
                    matrix_runs += 1
        zero = _run_zero_builds(repo, artifacts, lock["stable_zero_repair_proof"], work)
    after_artifacts = validate_locked_artifacts(repo, artifacts)
    after_legacy = validate_legacy_allowlist(repo, lock["bindings"]["legacy_allowlist_sha256"])
    after_sibling = validate_empty_sibling(repo)
    _assert_static_unchanged(before_artifacts, after_artifacts, legacy, after_legacy, sibling, after_sibling)
    git_after = _git_scope_audit(repo)
    _require(git_before == git_after, "repository scope changed during full Stage 4 validation")
    return {
        "artifacts": len(artifacts),
        "closure_claim": "FULL_MATRIX_ONLY",
        "git_scope": git_after["state"],
        "legacy_files": legacy["regular_files"],
        "lock_sha256": expected_lock_sha256,
        "matrix_runs": matrix_runs,
        "mode": "FULL",
        "source_state": blocked["status"],
        "zero_proof_sha256": stable_zero_proof_digest(zero["first"]),
    }


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=repository_root())
    parser.add_argument("--mode", choices=("lock-only", "quick", "full"), default="quick")
    parser.add_argument("--expected-lock-sha256", required=True)
    args = parser.parse_args(argv)
    repo = _absolute(args.repo_root)
    try:
        if args.mode == "lock-only":
            result = run_lock_only(repo, args.expected_lock_sha256)
        elif args.mode == "quick":
            result = run_quick(repo, args.expected_lock_sha256)
        else:
            result = run_full(repo, args.expected_lock_sha256)
    except (OSError, Stage4ValidationError, ValueError, KeyError, TypeError) as error:
        print(f"STAGE4 FAIL: {error}", file=sys.stderr)
        return 1
    prefix = {
        "lock-only": "STAGE4 LOCK-ONLY OK ",
        "quick": "STAGE4 QUICK OK ",
        "full": "STAGE4 FULL OK ",
    }[args.mode]
    print(prefix + json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
