"""Production registry boundary for the Stage 4 overlay engine.

The byte-block engine in :mod:`overlay_lib` intentionally knows nothing about
the repository.  This module supplies the missing trust boundary: it rebuilds
the only permitted initial state from the externally pinned Stage 1--3
artifacts, validates dynamic repair/review ledgers through the independent
pipeline-schema validator, and refuses canonical authority while the real
witness registry is ``SOURCE_BLOCKED``.

No test authority helper is imported or used here.  The private production
factory is reached only after every frozen identity and every dynamic registry
join has passed.  The current frozen package has zero authorized witness
regions, so that final branch is deliberately unreachable today.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
from typing import Any, Iterable, Mapping, Sequence

import overlay_lib
import pipeline_schema_lib as pipeline


BASELINE_LOCK_SHA256 = "57224a1f1ba8333bbc900b23ff6127a189649feb01c279f30fac05a305658863"
WITNESS_LOCK_SHA256 = "f348e4dd0ebf328c48066696eb70359d954e07cbdfd7b7fd827286e3268ba449"
GUARDRAILS_SHA256 = "ba5357b6172c5740ed799bf53d65aa401c53750b0f5dc6ccc901d4149e5225cb"
STRUCTURE_LEDGER_SHA256 = "6f9891417f458ca1e40385082b4f230e780d72362a783f35e11648082a743d49"
MONOLITH_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"
PIPELINE_SCHEMA_LOCK_SHA256 = "31e9ae9b20e643bb9e6ad9b6f1d1efdf4a936cc6a3519360a21619be4e9a45cd"

LEGACY_ROOT = "ref/A-New-Kind-of-Science"
MONOLITH_PATH = f"{LEGACY_ROOT}/A-New-Kind-of-Science.md"
REPAIR_LEDGER_PATH = "goal-4/repair-ledger.jsonl"
REVIEW_LEDGER_PATH = "goal-4/review-ledger.jsonl"


class RegistryError(ValueError):
    """A frozen artifact, registry row, or cross-file join is invalid."""


class RegistryGateError(RegistryError):
    """The production authority gate is not open."""


class RegistryIntegrationError(RegistryError):
    """A required independently validated production bridge is unavailable."""


@dataclass(frozen=True, slots=True)
class _Ledger:
    path: str
    present: bool
    file_sha256: str | None
    rows: tuple[Mapping[str, Any], ...]
    row_sha256s: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class _Snapshot:
    repo_root: Path
    state: overlay_lib.OverlayState
    target_paths: Mapping[str, str]
    block_rows: Mapping[str, Mapping[str, Any]]
    block_row_sha256s: Mapping[str, str]
    baseline_lock_sha256: str
    witness_lock_sha256: str
    guardrails_sha256: str
    structure_ledger_sha256: str
    monolith_sha256: str
    witness_state_sha256: str
    witness_region_ledger_sha256: str
    pipeline_schema_lock_sha256: str
    witness_status: str
    witness_region_ids: frozenset[str]
    repair_ledger: _Ledger
    review_ledger: _Ledger
    schema_registry: pipeline.SchemaRegistry


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise RegistryError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _reject_float(value: str) -> None:
    raise RegistryError(f"floating-point JSON value is forbidden: {value}")


def _decode_json(raw: bytes, where: str) -> Any:
    try:
        text = raw.decode("utf-8")
        return json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_float=_reject_float,
            parse_constant=_reject_float,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RegistryError(f"invalid UTF-8 JSON in {where}: {exc}") from exc


def _canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def _safe_relative(value: str, where: str) -> PurePosixPath:
    if not isinstance(value, str) or not value:
        raise RegistryError(f"{where} path must be nonempty text")
    path = PurePosixPath(value)
    if path.is_absolute() or value != path.as_posix():
        raise RegistryError(f"{where} path is not canonical relative POSIX: {value!r}")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise RegistryError(f"{where} path escapes its root: {value!r}")
    return path


def _read_file(repo_root: Path, relative: str) -> bytes:
    rel = _safe_relative(relative, "registry artifact")
    candidate = repo_root.joinpath(*rel.parts)
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(repo_root)
    except (OSError, ValueError) as exc:
        raise RegistryError(f"artifact is absent or escapes repository: {relative}") from exc
    if resolved != candidate:
        raise RegistryError(f"artifact path contains a symlink: {relative}")
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(candidate, flags)
    except OSError as exc:
        raise RegistryError(f"cannot open registry artifact: {relative}: {exc}") from exc
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise RegistryError(f"registry artifact is not a regular file: {relative}")
        with os.fdopen(descriptor, "rb", closefd=False) as handle:
            raw = handle.read()
        after = os.fstat(descriptor)
        if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
        ):
            raise RegistryError(f"registry artifact changed while read: {relative}")
        if len(raw) != before.st_size:
            raise RegistryError(f"short registry artifact read: {relative}")
        return raw
    finally:
        os.close(descriptor)


def _load_json(repo_root: Path, relative: str, *, canonical: bool) -> tuple[Any, bytes]:
    raw = _read_file(repo_root, relative)
    value = _decode_json(raw, relative)
    if canonical and raw != _canonical_json_bytes(value):
        raise RegistryError(f"non-canonical ANKOS-CJ-1 JSON: {relative}")
    return value, raw


def _decode_jsonl(raw: bytes, where: str) -> tuple[tuple[Mapping[str, Any], ...], tuple[str, ...]]:
    if not raw:
        return (), ()
    rows: list[Mapping[str, Any]] = []
    hashes: list[str] = []
    for number, line in enumerate(raw.splitlines(keepends=True), 1):
        if not line.endswith(b"\n") or line == b"\n":
            raise RegistryError(f"malformed canonical JSONL row {number}: {where}")
        value = _decode_json(line, f"{where}:{number}")
        if not isinstance(value, dict) or line != _canonical_json_bytes(value):
            raise RegistryError(f"non-canonical JSONL row {number}: {where}")
        rows.append(value)
        hashes.append(_sha256(line))
    return tuple(rows), tuple(hashes)


def _exact_keys(value: Mapping[str, Any], keys: set[str], where: str) -> None:
    if set(value) != keys:
        raise RegistryError(f"{where} keys differ from the closed contract")


def _strict_int(value: Any, where: str, *, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise RegistryError(f"{where} must be an integer >= {minimum}")
    return value


def _verify_lock(
    repo_root: Path,
    relative: str,
    expected_sha256: str,
    expected_status: str,
) -> tuple[Mapping[str, Any], Mapping[str, bytes], bytes]:
    lock, raw = _load_json(repo_root, relative, canonical=True)
    if not isinstance(lock, dict):
        raise RegistryError(f"lock root is not an object: {relative}")
    if _sha256(raw) != expected_sha256:
        raise RegistryError(f"externally pinned lock replacement: {relative}")
    _exact_keys(lock, {"artifacts", "bindings", "schema_version", "sources", "status"}, relative)
    if lock["schema_version"] != "1.0.0" or lock["status"] != expected_status:
        raise RegistryError(f"lock identity/status drift: {relative}")
    payloads: dict[str, bytes] = {}
    seen: set[str] = set()
    for bucket in ("artifacts", "sources"):
        rows = lock[bucket]
        if not isinstance(rows, list):
            raise RegistryError(f"lock {bucket} is not an array: {relative}")
        for row in rows:
            if not isinstance(row, dict):
                raise RegistryError(f"malformed lock row: {relative}")
            _exact_keys(row, {"byte_size", "path", "sha256"}, f"{relative} row")
            path = row["path"]
            if path in seen:
                raise RegistryError(f"duplicate locked path: {path}")
            seen.add(path)
            data = _read_file(repo_root, path)
            if len(data) != _strict_int(row["byte_size"], "locked byte size"):
                raise RegistryError(f"locked byte-size drift: {path}")
            if _sha256(data) != row["sha256"]:
                raise RegistryError(f"locked artifact drift: {path}")
            payloads[path] = data
    return lock, payloads, raw


def _load_ledger(repo_root: Path, path: str) -> _Ledger:
    candidate = repo_root.joinpath(*_safe_relative(path, "ledger").parts)
    if not candidate.exists():
        return _Ledger(path, False, None, (), ())
    raw = _read_file(repo_root, path)
    rows, row_hashes = _decode_jsonl(raw, path)
    return _Ledger(path, True, _sha256(raw), rows, row_hashes)


def _line_identity(raw: bytes, start: int, end: int) -> tuple[int, int, int]:
    selected = raw[start:end]
    start_line = raw.count(b"\n", 0, start) + 1
    line_count = selected.count(b"\n") + (0 if selected.endswith(b"\n") else 1)
    return start_line, start_line + line_count - 1, line_count


def _validate_guardrails(repo_root: Path) -> tuple[Mapping[str, Any], bytes]:
    guardrails, raw = _load_json(repo_root, "goal-4/guardrails.json", canonical=False)
    if not isinstance(guardrails, dict) or _sha256(raw) != GUARDRAILS_SHA256:
        raise RegistryError("frozen guardrails digest drift")
    if guardrails.get("status") != "FROZEN_STAGE_1":
        raise RegistryError("guardrail status drift")
    architecture = guardrails.get("architecture")
    legacy = guardrails.get("legacy_input")
    if not isinstance(architecture, dict) or not isinstance(legacy, dict):
        raise RegistryError("guardrail architecture/input contract is malformed")
    if architecture.get("legacy_root") != LEGACY_ROOT or architecture.get("repaired_root") != "ref/A-New-Kind-of-Science-Repaired":
        raise RegistryError("guardrail root identity drift")
    if legacy.get("canonical_monolith") != MONOLITH_PATH or legacy.get("generated_output_may_be_build_input") is not False:
        raise RegistryError("guardrail monolith/input direction drift")
    documents = guardrails.get("canonical_documents")
    if not isinstance(documents, list) or len(documents) != 29:
        raise RegistryError("canonical document universe must contain exactly 29 rows")
    expected = {"order", "id", "anchor_slug", "kind", "title", "path", "role"}
    for index, row in enumerate(documents):
        if not isinstance(row, dict):
            raise RegistryError("malformed canonical document row")
        _exact_keys(row, expected, "canonical document")
        if row["order"] != index or row["role"] != overlay_lib.CANONICAL_AUTHOR_TEXT:
            raise RegistryError("canonical document order/role drift")
        path = _safe_relative(row["path"], "canonical document")
        if not path.parts or path.parts[0] != "CANONICAL":
            raise RegistryError("canonical document path escaped CANONICAL")
    ids = [row["id"] for row in documents]
    paths = [row["path"] for row in documents]
    if len(set(ids)) != 29 or len(set(paths)) != 29:
        raise RegistryError("duplicate canonical document ID/path")
    return guardrails, raw


def _build_state(
    guardrails: Mapping[str, Any],
    corpus: Mapping[str, Any],
    structure_raw: bytes,
    monolith: bytes,
) -> tuple[
    overlay_lib.OverlayState,
    dict[str, str],
    dict[str, Mapping[str, Any]],
    dict[str, str],
]:
    rows, row_hashes = _decode_jsonl(structure_raw, "goal-4/structure-ledger.jsonl")
    if len(rows) != 29 + 20430:
        raise RegistryError("structure ledger cardinality drift")
    segment_rows = rows[:29]
    block_rows = rows[29:]
    if any(row.get("record_type") != "SEGMENT" for row in segment_rows) or any(
        row.get("record_type") != "RAW_BLOCK" for row in block_rows
    ):
        raise RegistryError("structure ledger record ordering/type drift")

    documents = guardrails["canonical_documents"]
    by_document = {row["id"]: row for row in documents}
    target_paths = {row["id"]: row["path"] for row in documents}
    segment_by_id: dict[str, Mapping[str, Any]] = {}
    cursor = 0
    for order, (row, document) in enumerate(zip(segment_rows, documents, strict=True)):
        if row.get("order") != order or row.get("segment_id") != document["id"]:
            raise RegistryError("segment/document identity join drift")
        if row.get("canonical_path") != document["path"] or row.get("role") != document["role"]:
            raise RegistryError("segment canonical path/role join drift")
        start = _strict_int(row.get("raw_start_byte"), "segment start")
        end = _strict_int(row.get("raw_end_byte_exclusive"), "segment end")
        if start != cursor or end <= start or end > len(monolith):
            raise RegistryError("segment spans are not a contiguous monolith partition")
        selected = monolith[start:end]
        if row.get("raw_byte_count") != len(selected) or row.get("raw_segment_sha256") != _sha256(selected):
            raise RegistryError("segment byte/hash join drift")
        if row.get("raw_source_path") != "A-New-Kind-of-Science.md" or row.get("raw_source_sha256") != MONOLITH_SHA256:
            raise RegistryError("segment raw-source identity drift")
        start_line, end_line, line_count = _line_identity(monolith, start, end)
        if (row.get("raw_start_line"), row.get("raw_end_line"), row.get("raw_line_count")) != (start_line, end_line, line_count):
            raise RegistryError("segment line/span join drift")
        segment_by_id[document["id"]] = row
        cursor = end
    if cursor != len(monolith):
        raise RegistryError("segment partition does not cover the monolith")

    targets: dict[tuple[str, str], list[overlay_lib.Block]] = {
        (row["id"], overlay_lib.CANONICAL_AUTHOR_TEXT): [] for row in documents
    }
    block_by_id: dict[str, Mapping[str, Any]] = {}
    block_hash_by_id: dict[str, str] = {}
    cursor = 0
    for index, (row, row_hash) in enumerate(zip(block_rows, row_hashes[29:], strict=True), 1):
        block_id = f"RAW-{index:06d}"
        if row.get("order") != index or row.get("raw_block_id") != block_id:
            raise RegistryError("raw block order/ID drift")
        start = _strict_int(row.get("start_byte"), "raw block start")
        end = _strict_int(row.get("end_byte_exclusive"), "raw block end")
        if start != cursor or end <= start or end > len(monolith):
            raise RegistryError("raw blocks are not a contiguous monolith partition")
        data = monolith[start:end]
        if row.get("byte_size") != len(data) or row.get("raw_sha256") != _sha256(data):
            raise RegistryError("raw block byte/hash join drift")
        if row.get("terminal_lf") is not data.endswith(b"\n"):
            raise RegistryError("raw block terminal-LF drift")
        start_line, end_line, line_count = _line_identity(monolith, start, end)
        if (row.get("start_line"), row.get("end_line"), row.get("line_count")) != (start_line, end_line, line_count):
            raise RegistryError("raw block line/span join drift")
        document_id = row.get("canonical_document_id")
        document = by_document.get(document_id)
        segment = segment_by_id.get(row.get("segment_id"))
        if document is None or segment is None or document_id != row.get("segment_id"):
            raise RegistryError("raw block segment/document join drift")
        if row.get("canonical_path") != document["path"]:
            raise RegistryError("raw block canonical path join drift")
        if start < segment["raw_start_byte"] or end > segment["raw_end_byte_exclusive"]:
            raise RegistryError("raw block span crosses its segment")
        targets[(document_id, overlay_lib.CANONICAL_AUTHOR_TEXT)].append(
            overlay_lib.Block(block_id, data)
        )
        block_by_id[block_id] = row
        block_hash_by_id[block_id] = row_hash
        cursor = end
    if cursor != len(monolith) or len(block_by_id) != 20430:
        raise RegistryError("raw block partition is incomplete")
    if any(not blocks for blocks in targets.values()):
        raise RegistryError("a canonical target has no raw blocks")
    state = overlay_lib.OverlayState.from_mapping(targets)
    recovered = b"".join(
        block.data
        for document in documents
        for block in state.blocks(overlay_lib.CANONICAL_AUTHOR_TEXT, document["id"])
    )
    if recovered != monolith:
        raise RegistryError("overlay-state construction is not an exact monolith identity")
    return state, target_paths, block_by_id, block_hash_by_id


def _load_snapshot(repo_root: Path | str) -> _Snapshot:
    root = Path(repo_root).resolve(strict=True)
    if not root.is_dir():
        raise RegistryError("repository root is not a directory")

    guardrails, guardrails_raw = _validate_guardrails(root)
    baseline, baseline_files, baseline_raw = _verify_lock(
        root,
        "goal-4/baseline-lock.json",
        BASELINE_LOCK_SHA256,
        "FROZEN_STAGE_2_BASELINE",
    )
    if baseline["bindings"].get("guardrails_sha256") != _sha256(guardrails_raw):
        raise RegistryError("baseline lock does not bind actual guardrails")
    corpus_raw = baseline_files.get("goal-4/corpus-manifest.json")
    structure_raw = baseline_files.get("goal-4/structure-ledger.jsonl")
    if corpus_raw is None or structure_raw is None or _sha256(structure_raw) != STRUCTURE_LEDGER_SHA256:
        raise RegistryError("baseline lock lacks the frozen corpus/structure artifacts")
    corpus = _decode_json(corpus_raw, "goal-4/corpus-manifest.json")
    if corpus_raw != _canonical_json_bytes(corpus) or not isinstance(corpus, dict):
        raise RegistryError("corpus manifest is not canonical")
    if corpus.get("legacy_root") != LEGACY_ROOT or corpus.get("counts") != {"all_regular_files": 1463, "jpeg": 1444, "markdown": 19}:
        raise RegistryError("corpus manifest identity/count drift")
    monolith_rows = [
        row
        for row in corpus.get("raw_inputs", [])
        if row.get("role") == "RAW_AUTHOR_TEXT_MONOLITH"
    ]
    if len(monolith_rows) != 1:
        raise RegistryError("corpus manifest lacks exactly one raw monolith")
    monolith_row = monolith_rows[0]
    if monolith_row.get("relative_path") != "A-New-Kind-of-Science.md" or monolith_row.get("sha256") != MONOLITH_SHA256:
        raise RegistryError("monolith manifest row identity drift")
    monolith = _read_file(root, MONOLITH_PATH)
    if len(monolith) != monolith_row.get("byte_size") or _sha256(monolith) != MONOLITH_SHA256:
        raise RegistryError("raw monolith byte/hash drift")
    state, target_paths, block_rows, block_row_hashes = _build_state(
        guardrails, corpus, structure_raw, monolith
    )

    witness, witness_files, witness_raw = _verify_lock(
        root,
        "goal-4/witness-lock.json",
        WITNESS_LOCK_SHA256,
        "FROZEN_STAGE_3_SOURCE_BLOCKED",
    )
    bindings = witness["bindings"]
    if (
        bindings.get("baseline_lock_sha256") != _sha256(baseline_raw)
        or bindings.get("guardrails_sha256") != _sha256(guardrails_raw)
        or bindings.get("structure_ledger_sha256") != _sha256(structure_raw)
        or bindings.get("corpus_manifest_sha256") != _sha256(corpus_raw)
    ):
        raise RegistryError("witness lock upstream bindings drift")
    witness_state_raw = witness_files.get("goal-4/witness-state.json")
    witness_regions_raw = witness_files.get("goal-4/witness-region-ledger.jsonl")
    if witness_state_raw is None or witness_regions_raw is None:
        raise RegistryError("witness lock lacks state/region ledger")
    witness_state = _decode_json(witness_state_raw, "goal-4/witness-state.json")
    witness_rows, _ = _decode_jsonl(
        witness_regions_raw, "goal-4/witness-region-ledger.jsonl"
    )
    if not isinstance(witness_state, dict) or witness_state.get("status") != "SOURCE_BLOCKED":
        raise RegistryError("current witness state is not SOURCE_BLOCKED")
    if len(witness_rows) != 29:
        raise RegistryError("source-blocked witness ledger must contain 29 segment gaps")
    documents = guardrails["canonical_documents"]
    for index, (row, document) in enumerate(zip(witness_rows, documents, strict=True)):
        if (
            row.get("record_type") != "SEGMENT_SOURCE_GAP"
            or row.get("order") != index
            or row.get("segment_id") != document["id"]
            or row.get("canonical_document_id") != document["id"]
            or row.get("canonical_path") != document["path"]
            or row.get("coverage_status") != "SOURCE_BLOCKED"
            or row.get("repair_authorized") is not False
            or row.get("witness_region_ids") != []
        ):
            raise RegistryError("witness gap/document/authority join drift")
        ids = [
            block_id
            for block_id, block_row in block_rows.items()
            if block_row["canonical_document_id"] == document["id"]
        ]
        ids_digest = _sha256(
            json.dumps(ids, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
                "utf-8"
            )
        )
        if row.get("raw_block_count") != len(ids) or row.get("raw_block_ids_sha256") != ids_digest:
            raise RegistryError("witness gap/raw-block join drift")
    coverage = witness_state.get("coverage")
    if not isinstance(coverage, dict) or coverage.get("witness_region_count") != 0 or coverage.get("blocked_segment_count") != 29:
        raise RegistryError("witness state coverage contradicts the region ledger")

    try:
        contract, schema_registry = pipeline.validate_pipeline_contract(root)
        pipeline.validate_lock(root, PIPELINE_SCHEMA_LOCK_SHA256)
    except (OSError, pipeline.PipelineSchemaError) as exc:
        raise RegistryError(f"pipeline schema package is not independently valid: {exc}") from exc
    ledger_registry = {row["path"]: row for row in contract["ledgers"]}
    if REPAIR_LEDGER_PATH not in ledger_registry or REVIEW_LEDGER_PATH not in ledger_registry:
        raise RegistryError("pipeline contract lacks repair/review ledger registrations")
    repairs = _load_ledger(root, REPAIR_LEDGER_PATH)
    reviews = _load_ledger(root, REVIEW_LEDGER_PATH)
    try:
        pipeline.validate_review_set(reviews.rows, schema_registry)
        pipeline.validate_repair_set(repairs.rows, schema_registry, reviews.rows)
    except (KeyError, TypeError, pipeline.PipelineSchemaError) as exc:
        raise RegistryError(f"dynamic repair/review registry is invalid: {exc}") from exc

    return _Snapshot(
        repo_root=root,
        state=state,
        target_paths=target_paths,
        block_rows=block_rows,
        block_row_sha256s=block_row_hashes,
        baseline_lock_sha256=_sha256(baseline_raw),
        witness_lock_sha256=_sha256(witness_raw),
        guardrails_sha256=_sha256(guardrails_raw),
        structure_ledger_sha256=_sha256(structure_raw),
        monolith_sha256=_sha256(monolith),
        witness_state_sha256=_sha256(witness_state_raw),
        witness_region_ledger_sha256=_sha256(witness_regions_raw),
        pipeline_schema_lock_sha256=PIPELINE_SCHEMA_LOCK_SHA256,
        witness_status=witness_state["status"],
        witness_region_ids=frozenset(),
        repair_ledger=repairs,
        review_ledger=reviews,
        schema_registry=schema_registry,
    )


def load_frozen_overlay_state(repo_root: Path | str) -> overlay_lib.OverlayState:
    """Rebuild the exact 29-target/20,430-block canonical raw state."""

    return _load_snapshot(repo_root).state


def _registry_digest(snapshot: _Snapshot, bindings: Sequence[pipeline.ValidatedRepairBinding]) -> str:
    repair_bindings = [
        {
            "expected_result_sha256": binding.expected_result_sha256,
            "expected_target_sha256": binding.expected_target_sha256,
            "forward_payload_sha256": binding.forward_payload_sha256,
            "inverse_payload_sha256": binding.inverse_payload_sha256,
            "operation_projection_sha256": binding.operation_projection_sha256,
            "overlay_operation_bound": binding.overlay_operation_bound,
            "repair_id": binding.repair_id,
            "repair_row_sha256": binding.repair_row_sha256,
        }
        for binding in bindings
    ]
    payload = {
        "baseline_lock_sha256": snapshot.baseline_lock_sha256,
        "guardrails_sha256": snapshot.guardrails_sha256,
        "monolith_sha256": snapshot.monolith_sha256,
        "pipeline_schema_lock_sha256": snapshot.pipeline_schema_lock_sha256,
        "repair_ledger_sha256": snapshot.repair_ledger.file_sha256,
        "repair_bindings": repair_bindings,
        "review_ledger_sha256": snapshot.review_ledger.file_sha256,
        "review_rows": list(snapshot.review_ledger.row_sha256s),
        "structure_ledger_sha256": snapshot.structure_ledger_sha256,
        "witness_lock_sha256": snapshot.witness_lock_sha256,
        "witness_region_ledger_sha256": snapshot.witness_region_ledger_sha256,
        "witness_state_sha256": snapshot.witness_state_sha256,
    }
    return _sha256(b"ANKOS-OVERLAY-PRODUCTION-REGISTRY-1\0" + _canonical_json_bytes(payload))


def mint_production_authority(
    repo_root: Path | str,
    initial: overlay_lib.OverlayState,
    records: Iterable[overlay_lib.Operation],
) -> overlay_lib.ApplicationAuthority:
    """Validate the live registry and mint canonical authority, or fail closed.

    The current Stage 3 registry is intentionally incapable of succeeding:
    it has no authorized witness regions and no repair/review ledgers.  State
    and operation inputs are still checked before returning the categorical
    gate error so target/block substitutions cannot hide behind that status.
    """

    snapshot = _load_snapshot(repo_root)
    if not isinstance(initial, overlay_lib.OverlayState) or initial != snapshot.state:
        raise RegistryError("initial overlay state differs from the frozen 29-document registry")
    closed = tuple(records)
    known = (
        overlay_lib.Replace,
        overlay_lib.Delete,
        overlay_lib.AnchoredInsert,
        overlay_lib.Move,
        overlay_lib.Split,
        overlay_lib.Merge,
    )
    if not closed or any(not isinstance(record, known) for record in closed):
        raise RegistryError("authority requires a nonempty batch of typed overlay operations")
    if any(record.meta.target_role != overlay_lib.CANONICAL_AUTHOR_TEXT for record in closed):
        raise RegistryError("production canonical authority cannot include noncanonical roles")
    validated_state = snapshot.state
    for record in closed:
        expected_path = snapshot.target_paths.get(record.meta.target_id)
        if expected_path is None or record.meta.target_path != expected_path:
            raise RegistryError(f"{record.meta.repair_id}: target ID/path is outside the frozen 29-document registry")
        if record.meta.raw_source_id not in snapshot.block_rows:
            raise RegistryError(f"{record.meta.repair_id}: raw source block is outside the frozen 20,430-block registry")
        if record.meta.raw_source_row_sha256 != snapshot.block_row_sha256s[record.meta.raw_source_id]:
            raise RegistryError(f"{record.meta.repair_id}: raw source row hash drift")
        before = validated_state.blocks(record.meta.target_role, record.meta.target_id)
        before_sha256 = overlay_lib.target_sha256(
            record.meta.target_id, record.meta.target_role, before
        )
        if record.meta.expected_target_sha256 != before_sha256:
            raise RegistryError(f"{record.meta.repair_id}: exact target pre-state guard drift")
        apply_one = getattr(overlay_lib, "_apply_operation", None)
        if apply_one is None:
            raise RegistryIntegrationError("overlay exact-operation validator is unavailable")
        try:
            after = apply_one(record, before)
        except overlay_lib.OverlayError as exc:
            raise RegistryError(
                f"{record.meta.repair_id}: typed operation does not join the frozen target: {exc}"
            ) from exc
        after_sha256 = overlay_lib.target_sha256(
            record.meta.target_id, record.meta.target_role, after
        )
        if record.meta.expected_result_sha256 != after_sha256:
            raise RegistryError(f"{record.meta.repair_id}: exact target post-state guard drift")
        validated_state = validated_state.with_blocks(
            record.meta.target_role, after, record.meta.target_id
        )

    # This is a categorical repository fact, checked only after all immutable
    # inputs and caller-controlled state/operation identities were validated.
    if (
        snapshot.witness_status != "OPEN"
        or not snapshot.witness_region_ids
        or not snapshot.repair_ledger.present
        or not snapshot.review_ledger.present
    ):
        raise RegistryGateError(
            "canonical application gate is SOURCE_BLOCKED: zero authorized witness regions and no governed repair/review authority registry"
        )

    repair_by_id = {row["repair_id"]: row for row in snapshot.repair_ledger.rows}
    bindings: list[pipeline.ValidatedRepairBinding] = []
    grants: list[overlay_lib.AuthorityGrant] = []
    for record in closed:
        row = repair_by_id.get(record.meta.repair_id)
        if row is None:
            raise RegistryError(f"{record.meta.repair_id}: operation has no exact repair-ledger row")
        try:
            binding = pipeline.validate_overlay_operation_binding(
                row,
                snapshot.schema_registry,
                record,
                snapshot.review_ledger.rows,
            )
        except pipeline.PipelineSchemaError as exc:
            raise RegistryError(f"{record.meta.repair_id}: typed operation registry join failed: {exc}") from exc
        if binding.overlay_operation_bound is not True:
            raise RegistryIntegrationError("schema validator returned an unbound repair operation")
        # The current Stage 3 schema exposes no independently validated
        # witness-row binding object.  Never reconstruct a weaker substitute.
        witness_bridge = getattr(pipeline, "validate_overlay_witness_binding", None)
        if witness_bridge is None:
            raise RegistryIntegrationError(
                "OPEN authority requires a public validated witness-row binding API; the current Stage 3/4 schema only exposes operation/raw/review bindings"
            )
        witness_bridge(row, snapshot.schema_registry, record)
        meta = record.meta
        witness = meta.witness
        review = meta.review
        grants.append(
            overlay_lib.AuthorityGrant(
                repair_id=meta.repair_id,
                target_id=meta.target_id,
                target_path=meta.target_path,
                raw_source_id=meta.raw_source_id,
                raw_source_span_sha256=meta.raw_source_span_sha256,
                raw_source_row_sha256=meta.raw_source_row_sha256,
                target_role=meta.target_role,
                operation_projection_sha256=binding.operation_projection_sha256,
                validated_risk_tags=meta.validated_risk_tags,
                validated_ast_impact=meta.validated_ast_impact,
                witness_id=None if witness is None else witness.witness_id,
                witness_region_id=None if witness is None else witness.region_id,
                witness_region_sha256=None if witness is None else witness.region_sha256,
                review_id=None if review is None else review.review_id,
                review_row_sha256=None if review is None else review.review_row_sha256,
                specialist_review_id=None if review is None else review.specialist_review_id,
                specialist_review_row_sha256=None if review is None else review.specialist_review_row_sha256,
            )
        )
        bindings.append(binding)

    registry_sha256 = _registry_digest(snapshot, bindings)
    proof_payload = {
        "expected_result_sha256s": [
            binding.expected_result_sha256 for binding in bindings
        ],
        "expected_target_sha256s": [
            binding.expected_target_sha256 for binding in bindings
        ],
        "forward_payload_sha256s": [
            binding.forward_payload_sha256 for binding in bindings
        ],
        "initial_state_sha256": initial.sha256,
        "inverse_payload_sha256s": [
            binding.inverse_payload_sha256 for binding in bindings
        ],
        "operation_projections": [binding.operation_projection_sha256 for binding in bindings],
        "registry_sha256": registry_sha256,
        "repair_row_sha256s": [binding.repair_row_sha256 for binding in bindings],
    }
    validator_proof_sha256 = _sha256(
        b"ANKOS-OVERLAY-PRODUCTION-VALIDATOR-PROOF-1\0"
        + _canonical_json_bytes(proof_payload)
    )
    factory = getattr(overlay_lib, "_application_authority_from_validated_registry", None)
    if factory is None:
        raise RegistryIntegrationError("overlay production authority factory is unavailable")
    return factory(
        gate_state="OPEN",
        baseline_lock_sha256=snapshot.baseline_lock_sha256,
        witness_lock_sha256=snapshot.witness_lock_sha256,
        registry_sha256=registry_sha256,
        validator_proof_sha256=validator_proof_sha256,
        initial_state_sha256=initial.sha256,
        ordered_batch_sha256=overlay_lib.ordered_operations_sha256(closed),
        grants=tuple(grants),
    )


__all__ = [
    "RegistryError",
    "RegistryGateError",
    "RegistryIntegrationError",
    "load_frozen_overlay_state",
    "mint_production_authority",
]
