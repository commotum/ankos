"""Strict, dependency-free validation for the Goal 4 Stage 4 schema package.

This module implements only the closed JSON Schema 2020-12 subset used by
``goal-4/schemas``.  Semantic checks that span records or frozen contracts are
kept explicit here; attractive JSON that merely satisfies shape constraints is
not sufficient to cross an evidence, review, role, or release gate.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
from typing import Any, Iterable, Mapping, Sequence


SCHEMA_DRAFT = "https://json-schema.org/draft/2020-12/schema"
PIPELINE_CONTRACT_PATH = "goal-4/pipeline-contract.json"
PIPELINE_LOCK_PATH = "goal-4/pipeline-schema-lock.json"
REPAIRED_ROOT = "ref/A-New-Kind-of-Science-Repaired"

UPSTREAM_PATHS = {
    "baseline_lock_sha256": "goal-4/baseline-lock.json",
    "compatibility_baseline_sha256": "goal-4/compatibility-baseline.json",
    "guardrails_sha256": "goal-4/guardrails.json",
    "licensing_contract_sha256": "goal-4/licensing-contract.json",
    "review_contract_sha256": "goal-4/review-contract.md",
    "style_guide_sha256": "goal-4/style-guide.md",
    "witness_lock_sha256": "goal-4/witness-lock.json",
}

SUPPORTED_SCHEMA_KEYS = frozenset(
    {
        "$defs",
        "$id",
        "$ref",
        "$schema",
        "additionalProperties",
        "const",
        "enum",
        "items",
        "maximum",
        "maxItems",
        "minItems",
        "minimum",
        "minLength",
        "oneOf",
        "pattern",
        "properties",
        "required",
        "type",
        "uniqueItems",
    }
)

REPAIR_CLASSES = (
    "STRUCTURE_BOUNDARY",
    "MARKDOWN_STRUCTURE",
    "PROSE_OCR",
    "HEADING_OR_FURNITURE",
    "FORMULA_OR_SYMBOL",
    "WOLFRAM_CODE",
    "RULE_TABLE_OR_DATA",
    "FIGURE_OR_CAPTION",
    "INDEX_ENTRY",
    "NAVIGATION_METADATA",
    "SOURCE_ERRATUM_ANNOTATION",
    "SEARCH_NORMALIZATION",
)
WORKFLOW_STATES = (
    "CAPTURED",
    "EVIDENCE_READY",
    "PENDING_SPECIALIST_REVIEW",
    "PENDING_INDEPENDENT_REVIEW",
    "SOURCE_BLOCKED",
    "CLOSED",
)
FINAL_DISPOSITIONS = (
    "APPLIED_MECHANICALLY_PROVEN",
    "APPLIED_WITNESS_VERIFIED",
    "ANNOTATED_SOURCE_ERRATUM",
    "REJECTED_VALID_SOURCE_TEXT",
    "DUPLICATE_CANDIDATE",
    "UNRESOLVED_SOURCE_NEEDED",
)
RELEASE_ROLES = (
    "CANONICAL_AUTHOR_TEXT",
    "DERIVED_AGGREGATE",
    "GENERATED_METADATA",
    "EDITORIAL_SIDECAR",
    "SEARCH_DERIVATIVE",
    "GOVERNED_LEGACY_ASSET",
    "GOVERNED_WITNESS_ASSET",
    "RELEASE_METADATA",
)
OPERATION_TYPES = ("REPLACE", "DELETE", "MOVE", "SPLIT", "MERGE", "ANCHORED_INSERT")
HIGH_RISK_CLASSES = frozenset(
    {
        "STRUCTURE_BOUNDARY",
        "MARKDOWN_STRUCTURE",
        "HEADING_OR_FURNITURE",
        "FORMULA_OR_SYMBOL",
        "WOLFRAM_CODE",
        "RULE_TABLE_OR_DATA",
        "FIGURE_OR_CAPTION",
        "INDEX_ENTRY",
    }
)
HIGH_RISK_OPERATION_TAGS = frozenset(
    {"WITNESS_ONLY_AUTHOR_TEXT_INSERTION", "AUTHORIAL_STRUCTURE_OR_HIERARCHY_CHANGE"}
)
HIGH_RISK_AST_TAGS = frozenset(
    {"HEADING_CHANGE", "MARKDOWN_STRUCTURE_CHANGE", "BOUNDARY_CHANGE", "INDEX_ORDER_CHANGE"}
)
OPERATION_RISK_TAGS = frozenset(HIGH_RISK_OPERATION_TAGS)
AST_IMPACT_TAGS = frozenset(HIGH_RISK_AST_TAGS)
MECHANICAL_PROOF_IDS = frozenset({"IDENTITY_AUTHOR_PROJECTION_V1"})
MECHANICAL_CHECK_IDS = (
    "RAW_GUARD_JOIN",
    "FORWARD_PROJECTION_GUARD",
    "INVERSE_PROJECTION_GUARD",
    "AUTHOR_PROJECTION_IDENTITY",
)
CLASS_ROLES = {
    **{
        value: "CANONICAL_AUTHOR_TEXT"
        for value in REPAIR_CLASSES
        if value
        not in {"NAVIGATION_METADATA", "SOURCE_ERRATUM_ANNOTATION", "SEARCH_NORMALIZATION"}
    },
    "NAVIGATION_METADATA": "GENERATED_METADATA",
    "SOURCE_ERRATUM_ANNOTATION": "EDITORIAL_SIDECAR",
    "SEARCH_NORMALIZATION": "SEARCH_DERIVATIVE",
}

WORKFLOW_TRANSITIONS = frozenset(
    {
        (None, "CAPTURED"),
        ("CAPTURED", "EVIDENCE_READY"),
        ("CAPTURED", "SOURCE_BLOCKED"),
        ("SOURCE_BLOCKED", "EVIDENCE_READY"),
        ("EVIDENCE_READY", "PENDING_SPECIALIST_REVIEW"),
        ("EVIDENCE_READY", "PENDING_INDEPENDENT_REVIEW"),
        ("EVIDENCE_READY", "CLOSED"),
        ("PENDING_SPECIALIST_REVIEW", "PENDING_INDEPENDENT_REVIEW"),
        ("PENDING_SPECIALIST_REVIEW", "SOURCE_BLOCKED"),
        ("PENDING_INDEPENDENT_REVIEW", "CLOSED"),
        ("PENDING_INDEPENDENT_REVIEW", "SOURCE_BLOCKED"),
    }
)


class PipelineSchemaError(ValueError):
    """A closed schema, record, binding, or gate was violated."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    if not path.is_file() or path.is_symlink():
        raise PipelineSchemaError(f"required regular file is absent or symlinked: {path}")
    return sha256_bytes(path.read_bytes())


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise PipelineSchemaError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def _decode_json(raw: bytes, where: str) -> Any:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PipelineSchemaError(f"invalid UTF-8 JSON at {where}: {exc}") from exc
    try:
        return json.loads(text, object_pairs_hook=_strict_object)
    except PipelineSchemaError:
        raise
    except json.JSONDecodeError as exc:
        raise PipelineSchemaError(f"invalid UTF-8 JSON at {where}: {exc}") from exc


def load_json(path: Path, *, require_cj1: bool) -> Any:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise PipelineSchemaError(f"UTF-8 BOM is forbidden: {path}")
    value = _decode_json(raw, str(path))
    if require_cj1 and raw != canonical_json_bytes(value):
        raise PipelineSchemaError(f"artifact is not exact ANKOS-CJ-1: {path}")
    _reject_floats(value, str(path))
    return value


def load_jsonl(path: Path, *, require_cj1: bool) -> list[Any]:
    raw = path.read_bytes()
    if raw and not raw.endswith(b"\n"):
        raise PipelineSchemaError(f"JSONL lacks terminal LF: {path}")
    rows: list[Any] = []
    for index, line in enumerate(raw.splitlines(keepends=True), 1):
        if line in {b"\n", b"\r\n"}:
            raise PipelineSchemaError(f"blank JSONL row {index}: {path}")
        row = _decode_json(line, f"{path}:{index}")
        if require_cj1 and line != canonical_json_bytes(row):
            raise PipelineSchemaError(f"JSONL row {index} is not ANKOS-CJ-1: {path}")
        _reject_floats(row, f"{path}:{index}")
        rows.append(row)
    return rows


def _reject_floats(value: Any, where: str) -> None:
    if isinstance(value, float):
        raise PipelineSchemaError(f"floating-point value forbidden at {where}")
    if isinstance(value, list):
        for index, item in enumerate(value):
            _reject_floats(item, f"{where}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            _reject_floats(item, f"{where}.{key}")


def _type_matches(value: Any, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "string":
        return isinstance(value, str)
    if expected == "array":
        return isinstance(value, list)
    if expected == "object":
        return isinstance(value, dict)
    raise PipelineSchemaError(f"unsupported JSON Schema type: {expected}")


class SchemaRegistry:
    """Load, lint, resolve, and apply the closed schema subset."""

    def __init__(self, repo_root: Path, schema_paths: Sequence[str]) -> None:
        self.repo_root = repo_root
        self.schemas: dict[str, Mapping[str, Any]] = {}
        for relative in schema_paths:
            path = repo_root / relative
            schema = load_json(path, require_cj1=True)
            if not isinstance(schema, dict):
                raise PipelineSchemaError(f"schema root is not an object: {relative}")
            self.schemas[relative] = schema
        self._by_name = {Path(path).name: path for path in self.schemas}
        if len(self._by_name) != len(self.schemas):
            raise PipelineSchemaError("schema basenames are not unique")
        for relative, schema in self.schemas.items():
            self._lint_schema(schema, relative, "$")

    def _lint_schema(self, schema: Any, current: str, at: str) -> None:
        if isinstance(schema, bool):
            return
        if not isinstance(schema, dict):
            raise PipelineSchemaError(f"schema node is not object/bool at {current}:{at}")
        unknown = set(schema) - SUPPORTED_SCHEMA_KEYS
        if unknown:
            raise PipelineSchemaError(f"unsupported schema keyword(s) {sorted(unknown)} at {current}:{at}")
        if "$schema" in schema and schema["$schema"] != SCHEMA_DRAFT:
            raise PipelineSchemaError(f"wrong JSON Schema draft at {current}:{at}")
        if "$ref" in schema:
            self._resolve_ref(current, schema["$ref"])
        for key in ("properties", "$defs"):
            entries = schema.get(key, {})
            if not isinstance(entries, dict):
                raise PipelineSchemaError(f"{key} is not an object at {current}:{at}")
            for name, subschema in entries.items():
                self._lint_schema(subschema, current, f"{at}/{key}/{name}")
        if "items" in schema:
            self._lint_schema(schema["items"], current, f"{at}/items")
        if isinstance(schema.get("additionalProperties"), dict):
            self._lint_schema(schema["additionalProperties"], current, f"{at}/additionalProperties")
        for key in ("oneOf",):
            if key not in schema:
                continue
            choices = schema[key]
            if not isinstance(choices, list) or not choices:
                raise PipelineSchemaError(f"{key} must be a nonempty array at {current}:{at}")
            for index, subschema in enumerate(choices):
                self._lint_schema(subschema, current, f"{at}/{key}/{index}")

    def _resolve_ref(self, current: str, ref: str) -> tuple[str, Any]:
        if not isinstance(ref, str):
            raise PipelineSchemaError(f"non-string $ref in {current}")
        document, marker, fragment = ref.partition("#")
        target_path = current if not document else self._by_name.get(Path(document).name)
        if target_path is None or target_path not in self.schemas:
            raise PipelineSchemaError(f"unresolved schema document reference {ref!r} in {current}")
        target: Any = self.schemas[target_path]
        if marker:
            if fragment and not fragment.startswith("/"):
                raise PipelineSchemaError(f"unsupported non-pointer fragment {ref!r}")
            for encoded in fragment.split("/")[1:] if fragment else []:
                key = encoded.replace("~1", "/").replace("~0", "~")
                if not isinstance(target, dict) or key not in target:
                    raise PipelineSchemaError(f"unresolved JSON pointer {ref!r} in {current}")
                target = target[key]
        return target_path, target

    def validate(self, schema_path: str, value: Any) -> None:
        if schema_path not in self.schemas:
            raise PipelineSchemaError(f"schema is not registered: {schema_path}")
        self._validate(value, self.schemas[schema_path], schema_path, "$")

    def _validate(self, value: Any, schema: Any, current: str, at: str) -> None:
        if schema is False:
            raise PipelineSchemaError(f"false schema rejected {at}")
        if schema is True:
            return
        if "$ref" in schema:
            target_path, target = self._resolve_ref(current, schema["$ref"])
            self._validate(value, target, target_path, at)
            return
        if "oneOf" in schema:
            matches = 0
            for candidate in schema["oneOf"]:
                try:
                    self._validate(value, candidate, current, at)
                except PipelineSchemaError:
                    continue
                matches += 1
            if matches != 1:
                raise PipelineSchemaError(f"oneOf matched {matches} alternatives at {at}")
            return
        expected = schema.get("type")
        if expected is not None:
            choices = expected if isinstance(expected, list) else [expected]
            if not any(_type_matches(value, choice) for choice in choices):
                raise PipelineSchemaError(f"wrong type at {at}: expected {choices}")
        if "const" in schema and value != schema["const"]:
            raise PipelineSchemaError(f"const mismatch at {at}")
        if "enum" in schema and value not in schema["enum"]:
            raise PipelineSchemaError(f"unknown closed value at {at}: {value!r}")
        if isinstance(value, str):
            if len(value) < schema.get("minLength", 0):
                raise PipelineSchemaError(f"string too short at {at}")
            if "pattern" in schema and re.search(schema["pattern"], value) is None:
                raise PipelineSchemaError(f"pattern mismatch at {at}")
        if isinstance(value, int) and not isinstance(value, bool):
            if "minimum" in schema and value < schema["minimum"]:
                raise PipelineSchemaError(f"integer below minimum at {at}")
            if "maximum" in schema and value > schema["maximum"]:
                raise PipelineSchemaError(f"integer above maximum at {at}")
        if isinstance(value, list):
            if len(value) < schema.get("minItems", 0):
                raise PipelineSchemaError(f"array too short at {at}")
            if "maxItems" in schema and len(value) > schema["maxItems"]:
                raise PipelineSchemaError(f"array too long at {at}")
            if schema.get("uniqueItems"):
                encoded = [canonical_json_bytes(item) for item in value]
                if len(encoded) != len(set(encoded)):
                    raise PipelineSchemaError(f"array items are not unique at {at}")
            if "items" in schema:
                for index, item in enumerate(value):
                    self._validate(item, schema["items"], current, f"{at}[{index}]")
        if isinstance(value, dict):
            required = schema.get("required", [])
            missing = [key for key in required if key not in value]
            if missing:
                raise PipelineSchemaError(f"missing required field(s) {missing} at {at}")
            properties = schema.get("properties", {})
            extras = set(value) - set(properties)
            additional = schema.get("additionalProperties", True)
            if extras and additional is False:
                raise PipelineSchemaError(f"unknown field(s) {sorted(extras)} at {at}")
            for key, item in value.items():
                if key in properties:
                    self._validate(item, properties[key], current, f"{at}.{key}")
                elif isinstance(additional, dict):
                    self._validate(item, additional, current, f"{at}.{key}")


def _safe_repo_path(value: str, field: str) -> None:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise PipelineSchemaError(f"unsafe repository path in {field}")
    pure = PurePosixPath(value)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        raise PipelineSchemaError(f"unsafe repository path in {field}: {value!r}")


def _locked_artifact(repo_root: Path, lock: Mapping[str, Any], relative: str) -> Path:
    rows = [row for row in lock.get("artifacts", []) if row.get("path") == relative]
    if len(rows) != 1:
        raise PipelineSchemaError(f"frozen lock lacks exactly one artifact row: {relative}")
    row = rows[0]
    path = repo_root / relative
    if (
        not isinstance(row.get("byte_size"), int)
        or isinstance(row.get("byte_size"), bool)
        or path.stat().st_size != row["byte_size"]
        or sha256_file(path) != row.get("sha256")
    ):
        raise PipelineSchemaError(f"frozen artifact differs from its lock: {relative}")
    return path


def _frozen_indexes(registry: SchemaRegistry) -> Mapping[str, Any]:
    """Load only externally bound Stage 2/3 identities used by semantic joins.

    The large structure ledger is cached on the registry, but every call first
    rechecks its byte size and digest against the externally pinned baseline
    lock.  A caller therefore cannot mutate a frozen artifact after registry
    construction and continue on stale trusted data.
    """

    root = registry.repo_root
    baseline_lock_path = root / "goal-4/baseline-lock.json"
    baseline_lock = load_json(baseline_lock_path, require_cj1=True)
    corpus_path = _locked_artifact(root, baseline_lock, "goal-4/corpus-manifest.json")
    structure_path = _locked_artifact(root, baseline_lock, "goal-4/structure-ledger.jsonl")
    witness_lock = load_json(root / "goal-4/witness-lock.json", require_cj1=True)
    witness_region_path = _locked_artifact(
        root, witness_lock, "goal-4/witness-region-ledger.jsonl"
    )
    witness_unresolved_path = _locked_artifact(
        root, witness_lock, "goal-4/witness-unresolved.jsonl"
    )
    fingerprint = (
        sha256_file(baseline_lock_path),
        sha256_file(corpus_path),
        sha256_file(structure_path),
        sha256_file(root / "goal-4/witness-lock.json"),
        sha256_file(witness_region_path),
        sha256_file(witness_unresolved_path),
    )
    cached = getattr(registry, "_frozen_index_cache", None)
    if cached is not None and cached[0] == fingerprint:
        return cached[1]

    corpus = load_json(corpus_path, require_cj1=True)
    legacy_root = corpus.get("legacy_root")
    if legacy_root != "ref/A-New-Kind-of-Science":
        raise PipelineSchemaError("Stage 2 legacy-root identity drift")
    input_by_path: dict[str, Mapping[str, Any]] = {}
    input_by_id: dict[str, Mapping[str, Any]] = {}
    for row in corpus.get("raw_inputs", []):
        relative = row.get("relative_path")
        file_id = row.get("file_id")
        if not isinstance(relative, str) or not isinstance(file_id, str):
            raise PipelineSchemaError("malformed Stage 2 raw-input identity")
        repo_path = f"{legacy_root}/{relative}"
        if repo_path in input_by_path or file_id in input_by_id:
            raise PipelineSchemaError("duplicate Stage 2 raw-input path or ID")
        input_by_path[repo_path] = row
        input_by_id[file_id] = row

    structure = load_jsonl(structure_path, require_cj1=True)
    blocks: list[Mapping[str, Any]] = []
    blocks_by_id: dict[str, Mapping[str, Any]] = {}
    segments_by_id: dict[str, Mapping[str, Any]] = {}
    for row in structure:
        if row.get("record_type") == "RAW_BLOCK":
            block_id = row.get("raw_block_id")
            if not isinstance(block_id, str) or block_id in blocks_by_id:
                raise PipelineSchemaError("duplicate/malformed Stage 2 raw-block identity")
            blocks.append(row)
            blocks_by_id[block_id] = row
        elif row.get("record_type") == "SEGMENT":
            segment_id = row.get("segment_id")
            if not isinstance(segment_id, str) or segment_id in segments_by_id:
                raise PipelineSchemaError("duplicate/malformed Stage 2 segment identity")
            segments_by_id[segment_id] = row
        else:
            raise PipelineSchemaError("unknown Stage 2 structure-ledger record type")
    if len(blocks) != 20430 or len(segments_by_id) != 29:
        raise PipelineSchemaError("Stage 2 structure universe cardinality drift")
    blocks.sort(key=lambda row: row["order"])

    guardrails = load_json(root / "goal-4/guardrails.json", require_cj1=False)
    documents = guardrails.get("canonical_documents", [])
    if len(documents) != 29:
        raise PipelineSchemaError("guardrail canonical-document universe drift")
    documents_by_id = {row["id"]: row for row in documents}
    documents_by_path = {row["path"]: row for row in documents}
    if len(documents_by_id) != 29 or len(documents_by_path) != 29:
        raise PipelineSchemaError("duplicate guardrail document ID/path")

    witness_rows = load_jsonl(witness_region_path, require_cj1=True)
    witness_region_ids: set[str] = set()
    for row in witness_rows:
        for region_id in row.get("witness_region_ids", []):
            if region_id in witness_region_ids:
                raise PipelineSchemaError("duplicate Stage 3 witness-region identity")
            witness_region_ids.add(region_id)
    witness_unresolved = load_jsonl(witness_unresolved_path, require_cj1=True)
    open_unresolved_ids = {
        row["unresolved_id"]
        for row in witness_unresolved
        if row.get("workflow_state") != "CLOSED"
    }
    indexes: Mapping[str, Any] = {
        "blocks": blocks,
        "blocks_by_id": blocks_by_id,
        "documents": documents,
        "documents_by_id": documents_by_id,
        "documents_by_path": documents_by_path,
        "input_by_id": input_by_id,
        "input_by_path": input_by_path,
        "legacy_root": legacy_root,
        "open_unresolved_ids": open_unresolved_ids,
        "segments_by_id": segments_by_id,
        "witness_region_ids": witness_region_ids,
    }
    setattr(registry, "_frozen_index_cache", (fingerprint, indexes))
    return indexes


def _read_frozen_input(
    registry: SchemaRegistry, source_path: str, source_sha256: str
) -> tuple[bytes, Mapping[str, Any]]:
    _safe_repo_path(source_path, "frozen raw source")
    indexes = _frozen_indexes(registry)
    manifest_row = indexes["input_by_path"].get(source_path)
    if manifest_row is None:
        raise PipelineSchemaError("raw source path does not join Stage 2 input manifest")
    if manifest_row.get("sha256") != source_sha256:
        raise PipelineSchemaError("raw source hash does not join Stage 2 input manifest")
    path = registry.repo_root / source_path
    if path.stat().st_size != manifest_row.get("byte_size") or sha256_file(path) != source_sha256:
        raise PipelineSchemaError("raw source file differs from frozen Stage 2 identity")
    return path.read_bytes(), manifest_row


def _expected_blocks_for_span(
    registry: SchemaRegistry, start: int, end: int
) -> list[Mapping[str, Any]]:
    if start < 0 or end <= start:
        raise PipelineSchemaError("raw span is empty, reversed, or negative")
    indexes = _frozen_indexes(registry)
    return [
        row
        for row in indexes["blocks"]
        if row["start_byte"] < end and start < row["end_byte_exclusive"]
    ]


def _validate_raw_span(
    registry: SchemaRegistry,
    *,
    source_path: str,
    source_sha256: str,
    span: Mapping[str, Any],
    raw_block_ids: Sequence[str],
    expected_text: str | None = None,
) -> bytes:
    payload, manifest_row = _read_frozen_input(registry, source_path, source_sha256)
    if manifest_row.get("role") != "RAW_AUTHOR_TEXT_MONOLITH":
        raise PipelineSchemaError("raw text span is not anchored in the Stage 2 monolith")
    start = span["start_byte"]
    end = span["end_byte_exclusive"]
    if end > len(payload):
        raise PipelineSchemaError("raw span exceeds the frozen source")
    selected = payload[start:end]
    selected_sha = sha256_bytes(selected)
    if span["sha256"] != selected_sha:
        raise PipelineSchemaError("raw span hash does not match frozen source bytes")
    expected_blocks = _expected_blocks_for_span(registry, start, end)
    expected_ids = [row["raw_block_id"] for row in expected_blocks]
    if list(raw_block_ids) != expected_ids:
        raise PipelineSchemaError("raw block IDs do not exactly cover the frozen span")
    canonical_ids = {row["canonical_document_id"] for row in expected_blocks}
    if len(canonical_ids) != 1:
        raise PipelineSchemaError("raw span crosses a frozen canonical-document boundary")
    if expected_text is not None:
        try:
            decoded = selected.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise PipelineSchemaError("raw text guard is not valid UTF-8") from exc
        if decoded != expected_text:
            raise PipelineSchemaError("guard text does not equal frozen source bytes")
    return selected


def _validate_raw_block_ids(registry: SchemaRegistry, raw_block_ids: Sequence[str]) -> None:
    known = _frozen_indexes(registry)["blocks_by_id"]
    if any(block_id not in known for block_id in raw_block_ids):
        raise PipelineSchemaError("raw block ID does not join Stage 2 structure ledger")


def _projection_hash(projection: Mapping[str, Any], field: str) -> None:
    expected = sha256_bytes(projection["text"].encode("utf-8"))
    if projection["sha256"] != expected:
        raise PipelineSchemaError(f"projection hash mismatch: {field}")


def validate_workflow(workflow: Mapping[str, Any]) -> None:
    events = workflow["events"]
    previous: str | None = None
    for index, event in enumerate(events):
        if event["sequence"] != index:
            raise PipelineSchemaError("workflow event sequence is not contiguous")
        if event["from_state"] != previous:
            raise PipelineSchemaError("workflow event from_state does not join")
        transition = (event["from_state"], event["to_state"])
        if transition not in WORKFLOW_TRANSITIONS:
            raise PipelineSchemaError(f"forbidden workflow transition: {transition}")
        previous = event["to_state"]
    if previous != workflow["state"]:
        raise PipelineSchemaError("workflow final event does not equal current state")
    disposition = workflow["final_disposition"]
    if workflow["state"] == "CLOSED":
        if disposition not in FINAL_DISPOSITIONS:
            raise PipelineSchemaError("CLOSED workflow lacks a final disposition")
    elif disposition is not None:
        raise PipelineSchemaError("non-CLOSED workflow has a final disposition")
    if workflow["state"] == "SOURCE_BLOCKED" and not workflow["unresolved_ids"]:
        raise PipelineSchemaError("SOURCE_BLOCKED workflow lacks an unresolved ID")


def _mechanical_basis(record: Mapping[str, Any]) -> Mapping[str, Any]:
    return {
        "after_projection_sha256": record["after_projection"]["sha256"],
        "before_projection_sha256": record["before_projection"]["sha256"],
        "forward_payload_sha256": record["forward_operation"]["payload_sha256"],
        "guard_kind": record["guard"]["guard_kind"],
        "inverse_payload_sha256": record["inverse_operation"]["payload_sha256"],
        "proof_id": "IDENTITY_AUTHOR_PROJECTION_V1",
        "raw_source_sha256": record["guard"]["raw_source_sha256"],
        "repair_id": record["repair_id"],
    }


def mechanical_proof_sha256(record: Mapping[str, Any]) -> str:
    """Digest of the independently recomputable mechanical proof basis."""

    return sha256_bytes(canonical_json_bytes(_mechanical_basis(record))[:-1])


def mechanical_check_sha256(record: Mapping[str, Any], check_id: str) -> str:
    if check_id not in MECHANICAL_CHECK_IDS:
        raise PipelineSchemaError(f"unknown mechanical check ID: {check_id}")
    projection = {"basis": _mechanical_basis(record), "check_id": check_id}
    return sha256_bytes(canonical_json_bytes(projection)[:-1])


def _validate_evidence(record: Mapping[str, Any], registry: SchemaRegistry) -> None:
    evidence = record["evidence"]
    all_ids: list[str] = []
    expected_kind = {
        "authoritative": "AUTHORITATIVE_WITNESS_REGION",
        "mechanical": "MECHANICAL_PROOF",
        "diagnostic": "DIAGNOSTIC_ONLY",
    }
    actual_witness_regions = _frozen_indexes(registry)["witness_region_ids"]
    for bucket, kind in expected_kind.items():
        for row in evidence[bucket]:
            all_ids.append(row["evidence_id"])
            if row["evidence_kind"] != kind:
                raise PipelineSchemaError(f"{bucket} evidence has the wrong evidence kind")
            if row["evidence_sha256"] == "0" * 64:
                raise PipelineSchemaError("evidence uses the all-zero placeholder digest")
            if kind == "AUTHORITATIVE_WITNESS_REGION":
                regions = row["witness_region_ids"]
                if not regions or not set(regions).issubset(actual_witness_regions):
                    raise PipelineSchemaError("authoritative evidence does not join Stage 3 witness regions")
                if not row["permission_record_id"] or row["mechanical_proof_id"] is not None:
                    raise PipelineSchemaError("authoritative evidence lacks permission or claims a mechanical proof")
            elif kind == "MECHANICAL_PROOF":
                if row["mechanical_proof_id"] not in MECHANICAL_PROOF_IDS:
                    raise PipelineSchemaError("mechanical evidence uses an unknown proof type")
                if row["permission_record_id"] is not None or row["witness_region_ids"]:
                    raise PipelineSchemaError("mechanical evidence improperly claims witness/permission evidence")
                if row["evidence_sha256"] != mechanical_proof_sha256(record):
                    raise PipelineSchemaError("mechanical evidence digest is not the recomputed proof digest")
            elif (
                row["mechanical_proof_id"] is not None
                or row["permission_record_id"] is not None
                or row["witness_region_ids"]
            ):
                raise PipelineSchemaError("diagnostic-only evidence claims proof or authority")
    if len(all_ids) != len(set(all_ids)):
        raise PipelineSchemaError("duplicate evidence ID across repair evidence buckets")
    for field in ("before_view_sha256", "witness_view_sha256", "after_view_sha256"):
        value = evidence[field]
        if value is not None and (not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None or value == "0" * 64):
            raise PipelineSchemaError(f"invalid/placeholder repair evidence-view digest: {field}")


def validate_repair(record: Mapping[str, Any], registry: SchemaRegistry) -> None:
    schema_path = "goal-4/schemas/repair-record.schema.json"
    registry.validate(schema_path, record)
    validate_workflow(record["workflow"])
    if record["baseline_lock_sha256"] != sha256_file(registry.repo_root / "goal-4/baseline-lock.json"):
        raise PipelineSchemaError("repair does not bind the frozen baseline lock")
    _safe_repo_path(record["target"]["path"], "repair target")
    _safe_repo_path(record["guard"]["raw_source_path"], "repair source")
    _projection_hash(record["before_projection"], "before")
    _projection_hash(record["after_projection"], "after")
    if record["witness_projection"] is not None:
        _projection_hash(record["witness_projection"], "witness")
    if record["repair_id"] in record["dependencies"]:
        raise PipelineSchemaError("repair depends on itself")
    _validate_evidence(record, registry)
    if CLASS_ROLES[record["repair_class"]] != record["target"]["role"]:
        raise PipelineSchemaError("repair class crossed its frozen target role")
    class_tags = record["risk"]["class_tags"]
    if not class_tags or record["repair_class"] not in class_tags:
        raise PipelineSchemaError("risk class-tag union omits the primary repair class")
    if any(CLASS_ROLES[tag] != record["target"]["role"] for tag in class_tags):
        raise PipelineSchemaError("risk class tag crosses the frozen target role")
    operation_tags = set(record["risk"]["operation_tags"])
    ast_tags = set(record["risk"]["ast_impact_tags"])
    if not operation_tags.issubset(OPERATION_RISK_TAGS):
        raise PipelineSchemaError("unknown operation risk tag")
    if not ast_tags.issubset(AST_IMPACT_TAGS):
        raise PipelineSchemaError("unknown AST-impact risk tag")
    derived_high_risk = (
        bool(set(class_tags) & HIGH_RISK_CLASSES)
        or bool(operation_tags & HIGH_RISK_OPERATION_TAGS)
        or bool(ast_tags & HIGH_RISK_AST_TAGS)
    )
    if record["risk"]["high_risk"] != derived_high_risk:
        raise PipelineSchemaError("high-risk union is misclassified")
    guard = record["guard"]
    if guard["guard_kind"] == "PREIMAGE":
        if sha256_bytes(guard["preimage"].encode("utf-8")) != guard["preimage_sha256"]:
            raise PipelineSchemaError("preimage hash mismatch")
        selected = _validate_raw_span(
            registry,
            source_path=guard["raw_source_path"],
            source_sha256=guard["raw_source_sha256"],
            span=guard["span"],
            raw_block_ids=guard["raw_block_ids"],
            expected_text=guard["preimage"],
        )
        if guard["preimage_sha256"] != sha256_bytes(selected):
            raise PipelineSchemaError("preimage digest does not join its raw span")
        raw_source, _ = _read_frozen_input(
            registry, guard["raw_source_path"], guard["raw_source_sha256"]
        )
        if raw_source.count(selected) != guard["expected_occurrence_count"]:
            raise PipelineSchemaError("preimage expected-occurrence count differs from frozen source")
    else:
        raw_source, _ = _read_frozen_input(
            registry, guard["raw_source_path"], guard["raw_source_sha256"]
        )
        for side in ("left_anchor", "right_anchor"):
            anchor = guard[side]
            if sha256_bytes(anchor["text"].encode("utf-8")) != anchor["sha256"]:
                raise PipelineSchemaError(f"{side} hash mismatch")
            if anchor["end_byte_exclusive"] <= anchor["start_byte"]:
                raise PipelineSchemaError(f"{side} has an empty/reversed span")
            if anchor["end_byte_exclusive"] > len(raw_source):
                raise PipelineSchemaError(f"{side} exceeds frozen source")
            selected = raw_source[anchor["start_byte"] : anchor["end_byte_exclusive"]]
            if selected != anchor["text"].encode("utf-8") or sha256_bytes(selected) != anchor["sha256"]:
                raise PipelineSchemaError(f"{side} does not join frozen source bytes")
            expected_blocks = _expected_blocks_for_span(
                registry, anchor["start_byte"], anchor["end_byte_exclusive"]
            )
            if len(expected_blocks) != 1 or expected_blocks[0]["raw_block_id"] != anchor["raw_block_id"]:
                raise PipelineSchemaError(f"{side} does not join exactly one Stage 2 raw block")
        if guard["left_anchor"]["end_byte_exclusive"] != guard["right_anchor"]["start_byte"]:
            raise PipelineSchemaError("two-sided anchors are not adjacent")
        joined = guard["left_anchor"]["text"].encode("utf-8") + guard["right_anchor"]["text"].encode("utf-8")
        if raw_source.count(joined) != guard["expected_adjacency_count"]:
            raise PipelineSchemaError("two-sided expected-adjacency count differs from frozen source")
    forward = record["forward_operation"]
    inverse = record["inverse_operation"]
    for label, operation in (("forward", forward), ("inverse", inverse)):
        if sha256_bytes(canonical_json_bytes(operation["payload"])[:-1]) != operation["payload_sha256"]:
            raise PipelineSchemaError(f"{label} operation payload hash mismatch")
    if forward["expected_input_projection_sha256"] != record["before_projection"]["sha256"]:
        raise PipelineSchemaError("forward input does not bind before projection")
    if forward["expected_output_projection_sha256"] != record["after_projection"]["sha256"]:
        raise PipelineSchemaError("forward output does not bind after projection")
    if inverse["expected_input_projection_sha256"] != record["after_projection"]["sha256"] or inverse["expected_output_projection_sha256"] != record["before_projection"]["sha256"]:
        raise PipelineSchemaError("inverse projection guards are not exact reverses")
    disposition = record["workflow"]["final_disposition"]
    if disposition in {"APPLIED_MECHANICALLY_PROVEN", "APPLIED_WITNESS_VERIFIED", "ANNOTATED_SOURCE_ERRATUM"}:
        if record["application_order"] is None or record["application_order"] < 0:
            raise PipelineSchemaError("applied record lacks application order")
        if record["risk"]["high_risk"] and not record["review_ids"]:
            raise PipelineSchemaError("applied high-risk repair lacks joined review IDs")
    elif record["application_order"] is not None:
        raise PipelineSchemaError("non-applied record has application order")
    if disposition == "ANNOTATED_SOURCE_ERRATUM" and (
        record["repair_class"] != "SOURCE_ERRATUM_ANNOTATION"
        or record["target"]["role"] != "EDITORIAL_SIDECAR"
    ):
        raise PipelineSchemaError("source-erratum annotation disposition escaped its sidecar")
    if disposition == "APPLIED_MECHANICALLY_PROVEN" and record["before_projection"]["sha256"] != record["after_projection"]["sha256"]:
        raise PipelineSchemaError("mechanical operation changed author projection")
    if disposition == "APPLIED_MECHANICALLY_PROVEN" and record["repair_class"] in {"STRUCTURE_BOUNDARY", "MARKDOWN_STRUCTURE"}:
        raise PipelineSchemaError("authorial structure/Markdown repair cannot be excused as tape partitioning")
    canonical_change = record["target"]["role"] == "CANONICAL_AUTHOR_TEXT" and record["before_projection"]["sha256"] != record["after_projection"]["sha256"]
    if canonical_change and _markdown_structure_signature(record["before_projection"]["text"]) != _markdown_structure_signature(record["after_projection"]["text"]):
        tags = set(record["risk"]["operation_tags"]) | set(record["risk"]["ast_impact_tags"])
        if not tags & {"AUTHORIAL_STRUCTURE_OR_HIERARCHY_CHANGE", "HEADING_CHANGE", "MARKDOWN_STRUCTURE_CHANGE"}:
            raise PipelineSchemaError("authorial Markdown/hierarchy change lacks a high-risk impact tag")
    if canonical_change or forward["operation_type"] == "ANCHORED_INSERT":
        raise PipelineSchemaError("current SOURCE_BLOCKED gate forbids author-text change/insertion")
    if disposition == "APPLIED_WITNESS_VERIFIED":
        raise PipelineSchemaError("current SOURCE_BLOCKED gate forbids witness-applied disposition")
    if disposition == "APPLIED_MECHANICALLY_PROVEN":
        if len(record["evidence"]["mechanical"]) != 1:
            raise PipelineSchemaError("mechanically applied repair lacks exactly one typed proof")
        checks = record["verification_results"]
        if [row["check_id"] for row in checks] != list(MECHANICAL_CHECK_IDS):
            raise PipelineSchemaError("mechanical repair lacks the exact ordered check suite")
        for check in checks:
            if check["passed"] is not True:
                raise PipelineSchemaError("mechanical verification check did not pass")
            if check["details_sha256"] != mechanical_check_sha256(record, check["check_id"]):
                raise PipelineSchemaError("mechanical verification details digest is not recomputable")
    elif record["evidence"]["mechanical"]:
        raise PipelineSchemaError("non-mechanical disposition carries mechanical-proof evidence")


def _markdown_structure_signature(text: str) -> tuple[str, ...]:
    markers: list[str] = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if re.match(r"^#{1,6} ", stripped):
            markers.append("HEADING")
        elif stripped.startswith(("- ", "* ", "+ ")) or re.match(r"^[0-9]+[.)] ", stripped):
            markers.append("LIST")
        elif stripped.startswith("```"):
            markers.append("FENCE")
        elif stripped.startswith("> "):
            markers.append("BLOCKQUOTE")
    return tuple(markers)


def validate_repair_set(
    records: Sequence[Mapping[str, Any]],
    registry: SchemaRegistry,
    review_records: Sequence[Mapping[str, Any]] = (),
    unresolved_records: Sequence[Mapping[str, Any]] = (),
) -> None:
    repair_ids = [record["repair_id"] for record in records]
    if len(repair_ids) != len(set(repair_ids)):
        raise PipelineSchemaError("duplicate repair ID")
    review_by_id = validate_review_set(review_records, registry)
    review_ids = set(review_by_id)
    unresolved_ids = {record["unresolved_id"] for record in unresolved_records}
    unresolved_ids.update(
        row["unresolved_id"]
        for row in load_jsonl(registry.repo_root / "goal-4/witness-unresolved.jsonl", require_cj1=True)
    )
    applied_orders: list[int] = []
    by_id = {record["repair_id"]: record for record in records}
    for record in records:
        validate_repair(record, registry)
        if not set(record["dependencies"]).issubset(by_id):
            raise PipelineSchemaError("repair dependency does not join")
        if not set(record["review_ids"]).issubset(review_ids):
            raise PipelineSchemaError("repair review ID does not join review ledger")
        combined_unresolved = set(record["unresolved_ids"]) | set(record["workflow"]["unresolved_ids"])
        if not combined_unresolved.issubset(unresolved_ids):
            raise PipelineSchemaError("repair unresolved ID does not join federated ledger")
        order = record["application_order"]
        if order is not None:
            applied_orders.append(order)
            for dependency in record["dependencies"]:
                dependency_order = by_id[dependency]["application_order"]
                if dependency_order is None or dependency_order >= order:
                    raise PipelineSchemaError("repair dependency is not applied earlier")
        joined_reviews = [review_by_id[review_id] for review_id in record["review_ids"]]
        for review in joined_reviews:
            if (
                review["subject_type"] != "REPAIR"
                or review["subject_id"] != record["repair_id"]
                or review["repair_id"] != record["repair_id"]
            ):
                raise PipelineSchemaError("review row does not join its repair subject")
            if review["principal_id"] == record["creator"]["principal_id"]:
                raise PipelineSchemaError("repair creator cannot independently review the repair")
            if review["closure_state"] != "CLOSED":
                raise PipelineSchemaError("applied repair references an open review")
        disposition = record["workflow"]["final_disposition"]
        applied = disposition in {
            "APPLIED_MECHANICALLY_PROVEN",
            "APPLIED_WITNESS_VERIFIED",
            "ANNOTATED_SOURCE_ERRATUM",
        }
        required_roles: set[str] = set()
        if applied and record["risk"]["high_risk"]:
            required_roles = {"SOURCE_REVIEWER", "SPECIALIST_REVIEWER"}
        declared_roles = set(record["workflow"]["required_review_roles"])
        if declared_roles != required_roles:
            raise PipelineSchemaError("workflow required-review roles differ from derived risk")
        actual_roles = {review["reviewer_role"] for review in joined_reviews}
        if not required_roles.issubset(actual_roles):
            raise PipelineSchemaError("applied high-risk repair lacks required joined review roles")
        if required_roles:
            source_rows = [row for row in joined_reviews if row["reviewer_role"] == "SOURCE_REVIEWER"]
            specialist_rows = [row for row in joined_reviews if row["reviewer_role"] == "SPECIALIST_REVIEWER"]
            if len(source_rows) != 1 or len(specialist_rows) != 1:
                raise PipelineSchemaError("high-risk repair requires exactly one source and specialist review")
            source = source_rows[0]
            specialist = specialist_rows[0]
            if source["principal_id"] == specialist["principal_id"]:
                raise PipelineSchemaError("source and specialist review principals are not independent")
            for review in (source, specialist):
                if (
                    review["blind_preproposal"] is not True
                    or review["candidate_visible"] is not False
                    or review["proposal_visible"] is not False
                ):
                    raise PipelineSchemaError("high-risk review is not sealed blind pre-proposal")
                if review["agreement_state"] != "AGREES":
                    raise PipelineSchemaError("required high-risk review did not agree")
            if not source["witness_region_ids"]:
                raise PipelineSchemaError("source review lacks an authoritative witness-region join")
            expected_specialty = _required_specialty(record)
            if specialist["specialty"] != expected_specialty:
                raise PipelineSchemaError("specialist review has the wrong declared specialty")
        allowed_view_hashes = {
            value
            for value in (
                record["evidence"]["before_view_sha256"],
                record["evidence"]["witness_view_sha256"],
                record["evidence"]["after_view_sha256"],
            )
            if value is not None
        }
        allowed_view_hashes.update(
            row["evidence_sha256"]
            for bucket in record["evidence"].values()
            if isinstance(bucket, list)
            for row in bucket
        )
        for review in joined_reviews:
            if review["evidence_view_sha256"] not in allowed_view_hashes:
                raise PipelineSchemaError("review evidence-view hash does not bind repair evidence")
    if len(applied_orders) != len(set(applied_orders)):
        raise PipelineSchemaError("duplicate repair application order")


def _required_specialty(record: Mapping[str, Any]) -> str:
    classes = set(record["risk"]["class_tags"])
    if classes & {"FORMULA_OR_SYMBOL", "WOLFRAM_CODE", "RULE_TABLE_OR_DATA"}:
        return "FORMULA_CODE_DATA"
    if "INDEX_ENTRY" in classes:
        return "INDEX"
    if "FIGURE_OR_CAPTION" in classes:
        return "FIGURE_CAPTION"
    if classes & {"STRUCTURE_BOUNDARY", "MARKDOWN_STRUCTURE", "HEADING_OR_FURNITURE"}:
        return "STRUCTURE"
    return "GENERAL"


def validate_provenance(record: Mapping[str, Any], registry: SchemaRegistry) -> None:
    registry.validate("goal-4/schemas/provenance-record.schema.json", record)
    kind = record["mapping_kind"]
    if kind == "WITNESS_INSERTED":
        raise PipelineSchemaError("current SOURCE_BLOCKED gate forbids witness insertion provenance")
    if kind == "GENERATED_METADATA":
        empty = sha256_bytes(b"")
        if record["author_text_projection_sha256"] != empty or record["inverse"]["inverse_kind"] != "REMOVE_GENERATED":
            raise PipelineSchemaError("generated metadata has nonempty projection or wrong inverse")
    if kind == "RAW_PRESERVED":
        if record["source"]["author_text_projection_sha256"] != record["target"]["author_text_projection_sha256"]:
            raise PipelineSchemaError("RAW_PRESERVED projection changed")


def validate_navigation(record: Mapping[str, Any], registry: SchemaRegistry) -> None:
    registry.validate("goal-4/schemas/navigation-record.schema.json", record)
    _safe_repo_path(record["source_path"], "navigation source")
    if record["destination_path"] is not None:
        _safe_repo_path(record["destination_path"], "navigation destination")
    if record["generated"] and record["author_text_projection_sha256"] != sha256_bytes(b""):
        raise PipelineSchemaError("generated navigation has nonempty author projection")


def validate_figure(record: Mapping[str, Any], registry: SchemaRegistry) -> None:
    registry.validate("goal-4/schemas/figure-record.schema.json", record)
    validate_workflow(record["workflow"])
    if record["asset_role"] == "GOVERNED_WITNESS_ASSET" or record["redistribution_allowed"] is True:
        raise PipelineSchemaError("current SOURCE_BLOCKED gate forbids witness asset release")
    if record["association_state"] == "VERIFIED" and not record["witness_region_ids"]:
        raise PipelineSchemaError("verified figure association lacks witness regions")


def validate_review(record: Mapping[str, Any], registry: SchemaRegistry) -> None:
    registry.validate("goal-4/schemas/review-record.schema.json", record)
    _validate_raw_block_ids(registry, record["raw_block_ids"])
    witness_ids = _frozen_indexes(registry)["witness_region_ids"]
    if not set(record["witness_region_ids"]).issubset(witness_ids):
        raise PipelineSchemaError("review witness-region ID does not join Stage 3")
    if record["decision_sha256"] != sha256_bytes(record["decision_payload"].encode("utf-8")):
        raise PipelineSchemaError("review decision hash does not bind the decision payload")
    if record["evidence_view_sha256"] == "0" * 64:
        raise PipelineSchemaError("review evidence-view digest is an all-zero placeholder")
    if record["reviewer_type"] == "HUMAN" and record["reviewed_at"] is None:
        raise PipelineSchemaError("human review lacks audit timestamp")
    if record["reviewed_at"] is not None and re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", record["reviewed_at"]
    ) is None:
        raise PipelineSchemaError("review timestamp is not canonical UTC seconds")
    if record["blind_preproposal"] and (
        record["proposal_visible"] or record["candidate_visible"]
    ):
        raise PipelineSchemaError("blind pre-proposal reviewer saw candidate/proposal")
    locator = record["view_locator"]
    locator_region = locator["witness_region_id"]
    if locator_region is not None:
        if locator_region not in record["witness_region_ids"] or locator_region not in witness_ids:
            raise PipelineSchemaError("review view locator does not join its witness-region set")
        if locator["witness_unit_id"] is None or locator["geometry"] is None:
            raise PipelineSchemaError("witness-region view lacks unit/geometry locator")
    elif locator["witness_unit_id"] is not None or locator["geometry"] is not None:
        raise PipelineSchemaError("partial witness view locator is forbidden")
    if record["raw_visible"] and not record["raw_block_ids"]:
        raise PipelineSchemaError("raw-visible review lacks raw-block identities")
    disagreement = record["agreement_state"] in {"DISAGREES", "PENDING_ADJUDICATION"}
    if disagreement:
        if not record["disagrees_with_review_ids"] or not record["follow_up"]:
            raise PipelineSchemaError("disagreement lacks joined opponent/follow-up")
    elif record["disagrees_with_review_ids"] or record["adjudicator_review_id"] is not None:
        raise PipelineSchemaError("non-disagreement carries disagreement/adjudicator fields")
    if record["agreement_state"] == "PENDING_ADJUDICATION" and record["closure_state"] == "CLOSED":
        raise PipelineSchemaError("pending adjudication is closed")


def validate_review_set(
    records: Sequence[Mapping[str, Any]], registry: SchemaRegistry
) -> dict[str, Mapping[str, Any]]:
    by_id: dict[str, Mapping[str, Any]] = {}
    for record in records:
        validate_review(record, registry)
        review_id = record["review_id"]
        if review_id in by_id:
            raise PipelineSchemaError("duplicate review ID")
        by_id[review_id] = record
    for record in records:
        opponents: list[Mapping[str, Any]] = []
        for review_id in record["disagrees_with_review_ids"]:
            opponent = by_id.get(review_id)
            if opponent is None:
                raise PipelineSchemaError("disagreement reference does not join review ledger")
            if opponent["subject_type"] != record["subject_type"] or opponent["subject_id"] != record["subject_id"]:
                raise PipelineSchemaError("disagreement crosses review subjects")
            if opponent["principal_id"] == record["principal_id"]:
                raise PipelineSchemaError("review principal disagrees with itself")
            opponents.append(opponent)
        adjudicator_id = record["adjudicator_review_id"]
        if record["agreement_state"] == "DISAGREES" and record["closure_state"] == "CLOSED":
            if adjudicator_id is None:
                raise PipelineSchemaError("closed disagreement lacks adjudication")
            adjudicator = by_id.get(adjudicator_id)
            if adjudicator is None:
                raise PipelineSchemaError("adjudicator ID does not join review ledger")
            if (
                adjudicator["reviewer_role"] != "ADJUDICATOR"
                or adjudicator["closure_state"] != "CLOSED"
                or adjudicator["subject_type"] != record["subject_type"]
                or adjudicator["subject_id"] != record["subject_id"]
            ):
                raise PipelineSchemaError("adjudicator row does not close the same subject")
            dispute_principals = {record["principal_id"]} | {
                opponent["principal_id"] for opponent in opponents
            }
            if adjudicator["principal_id"] in dispute_principals:
                raise PipelineSchemaError("disagreeing principal self-adjudicated")
        elif adjudicator_id is not None:
            raise PipelineSchemaError("open/non-disagreeing review claims an adjudicator")
    return by_id


def validate_unresolved(record: Mapping[str, Any], registry: SchemaRegistry) -> None:
    registry.validate("goal-4/schemas/unresolved-record.schema.json", record)
    if record["workflow_state"] == "SOURCE_BLOCKED" and record["repair_authorized"]:
        raise PipelineSchemaError("source-blocked item authorizes repair")
    if record["workflow_state"] != "CLOSED" and record["final_disposition"] is not None:
        raise PipelineSchemaError("open unresolved item has a final disposition")
    if record["workflow_state"] == "CLOSED" and record["resolution"] is None:
        raise PipelineSchemaError("closed unresolved item lacks a resolution")
    if record["resolution"] is None and not record["release_blocker_codes"] and record["severity_id"] != "S4_OPTIONAL_EDITORIAL_ENHANCEMENT":
        raise PipelineSchemaError("open nonoptional item lacks release blocker code")


def validate_compatibility(record: Mapping[str, Any], registry: SchemaRegistry) -> None:
    registry.validate("goal-4/schemas/compatibility-verification.schema.json", record)
    baseline_path = registry.repo_root / "goal-4/compatibility-baseline.json"
    if record["baseline_sha256"] != sha256_file(baseline_path):
        raise PipelineSchemaError("compatibility verification does not bind frozen baseline")
    baseline = load_json(baseline_path, require_cj1=True)
    if record["baseline_behavior_digest"] != baseline["behavior_digest"]:
        raise PipelineSchemaError("compatibility behavior baseline drift")
    expected_all = all(row["identical"] for row in record["oracle_results"])
    if record["all_identical"] != expected_all:
        raise PipelineSchemaError("compatibility all_identical summary is dishonest")


def validate_corpus_manifest(record: Mapping[str, Any], registry: SchemaRegistry, guardrails: Mapping[str, Any]) -> None:
    registry.validate("goal-4/schemas/corpus-manifest.schema.json", record)
    paths: set[str] = set()
    counts: dict[str, int] = {}
    canonical: list[tuple[int, str]] = []
    for item in record["files"]:
        _safe_repo_path(item["path"], "corpus output")
        if item["path"] in paths:
            raise PipelineSchemaError("duplicate corpus output path")
        paths.add(item["path"])
        counts[item["role"]] = counts.get(item["role"], 0) + 1
        if item["role"] == "CANONICAL_AUTHOR_TEXT":
            if item["canonical_order"] is None or item["canonical_document_id"] is None:
                raise PipelineSchemaError("canonical file lacks order/document ID")
            canonical.append((item["canonical_order"], item["canonical_document_id"]))
    if counts != record["role_counts"]:
        raise PipelineSchemaError("manifest role counts do not match files")
    expected = [(item["order"], item["id"]) for item in guardrails["canonical_documents"]]
    if sorted(canonical) != expected or record["canonical_document_order"] != [item[1] for item in expected]:
        raise PipelineSchemaError("canonical document count/path order drift")
    if record["certification_state"] != "UNCERTIFIED":
        raise PipelineSchemaError("current SOURCE_BLOCKED gate forbids certified corpus")


def validate_release_manifest(record: Mapping[str, Any], registry: SchemaRegistry) -> None:
    registry.validate("goal-4/schemas/release-manifest.schema.json", record)
    if record["certification_state"] != "UNCERTIFIED" or record["audit_certificate"] is not None:
        raise PipelineSchemaError("current SOURCE_BLOCKED gate forbids audit certification")
    if record["claim_scope"] == "FULL_REPAIR_CERTIFIED":
        raise PipelineSchemaError("current SOURCE_BLOCKED gate forbids full-repair claim")
    if not record["open_blocker_ids"]:
        raise PipelineSchemaError("uncertified source-blocked release omits blockers")
    if len(set(record["two_clean_build_digests"])) != 1:
        raise PipelineSchemaError("two clean builds are not byte-identical")


def _require_exact_keys(value: Mapping[str, Any], expected: Iterable[str], where: str) -> None:
    expected_set = set(expected)
    if set(value) != expected_set:
        raise PipelineSchemaError(
            f"{where} keys differ: missing={sorted(expected_set - set(value))}, extra={sorted(set(value) - expected_set)}"
        )


def validate_pipeline_contract(repo_root: Path) -> tuple[Mapping[str, Any], SchemaRegistry]:
    contract_path = repo_root / PIPELINE_CONTRACT_PATH
    contract = load_json(contract_path, require_cj1=True)
    if not isinstance(contract, dict):
        raise PipelineSchemaError("pipeline contract root is not an object")
    _require_exact_keys(
        contract,
        {
            "contract_id",
            "current_gates",
            "final_dispositions",
            "json_schema_draft",
            "ledgers",
            "operation_types",
            "release_roles",
            "schema_files",
            "schema_version",
            "serialization_profile",
            "status",
            "upstream_bindings",
            "workflow_states",
        },
        "pipeline contract",
    )
    if contract["contract_id"] != "ANKOS-PIPELINE-1" or contract["schema_version"] != "1.0.0":
        raise PipelineSchemaError("wrong pipeline contract identity/version")
    if contract["json_schema_draft"] != SCHEMA_DRAFT or contract["serialization_profile"] != "ANKOS-CJ-1":
        raise PipelineSchemaError("wrong schema draft or serialization profile")
    if tuple(contract["operation_types"]) != OPERATION_TYPES:
        raise PipelineSchemaError("operation type contract drift")
    if tuple(contract["workflow_states"]) != WORKFLOW_STATES:
        raise PipelineSchemaError("workflow state contract drift")
    if tuple(contract["final_dispositions"]) != FINAL_DISPOSITIONS:
        raise PipelineSchemaError("final disposition contract drift")
    if tuple(contract["release_roles"]) != RELEASE_ROLES:
        raise PipelineSchemaError("release role contract drift")
    expected_gates = {
        "audit_certification_allowed": False,
        "author_text_token_changes_allowed": False,
        "offline_zero_repair_build_allowed": True,
        "witness_asset_insertions_allowed": False,
        "witness_only_text_insertions_allowed": False,
        "witness_status": "SOURCE_BLOCKED",
    }
    if contract["current_gates"] != expected_gates:
        raise PipelineSchemaError("current Stage 3 source-blocked gates were weakened")
    if contract["upstream_bindings"].keys() != UPSTREAM_PATHS.keys():
        raise PipelineSchemaError("upstream binding key set drift")
    for key, relative in UPSTREAM_PATHS.items():
        if contract["upstream_bindings"][key] != sha256_file(repo_root / relative):
            raise PipelineSchemaError(f"upstream hash binding drift: {key}")
    schema_paths = contract["schema_files"]
    if len(schema_paths) != len(set(schema_paths)) or len(schema_paths) != 13:
        raise PipelineSchemaError("schema registry must contain 13 unique schemas")
    for relative in schema_paths:
        _safe_repo_path(relative, "schema registry")
        if not relative.startswith("goal-4/schemas/") or not relative.endswith(".schema.json"):
            raise PipelineSchemaError(f"schema path escapes closed package: {relative}")
    registry = SchemaRegistry(repo_root, schema_paths)
    ledger_paths: set[str] = set()
    for ledger in contract["ledgers"]:
        _require_exact_keys(ledger, {"empty_allowed", "path", "schema"}, "ledger registry row")
        _safe_repo_path(ledger["path"], "ledger registry")
        if ledger["path"] in ledger_paths:
            raise PipelineSchemaError("duplicate ledger path")
        ledger_paths.add(ledger["path"])
        if ledger["schema"] not in registry.schemas:
            raise PipelineSchemaError("ledger references unregistered schema")
    witness_state = load_json(repo_root / "goal-4/witness-state.json", require_cj1=False)
    if witness_state.get("status") != "SOURCE_BLOCKED":
        raise PipelineSchemaError("current witness state is not SOURCE_BLOCKED")
    coverage = load_jsonl(repo_root / "goal-4/witness-region-ledger.jsonl", require_cj1=True)
    if len(coverage) != 29:
        raise PipelineSchemaError("source-blocked witness coverage must have 29 segment rows")
    if any(row.get("repair_authorized") or row.get("witness_region_ids") for row in coverage):
        raise PipelineSchemaError("source-blocked coverage unexpectedly authorizes repair")
    repaired = repo_root / REPAIRED_ROOT
    if repaired.exists() and any(repaired.iterdir()):
        raise PipelineSchemaError("Stage 4 schema validation found nonempty repaired sibling")
    return contract, registry


def validate_lock(repo_root: Path, expected_lock_sha256: str) -> Mapping[str, Any]:
    path = repo_root / PIPELINE_LOCK_PATH
    actual_lock_sha256 = sha256_file(path)
    if actual_lock_sha256 != expected_lock_sha256:
        raise PipelineSchemaError("pipeline schema lock differs from validator-pinned digest")
    lock = load_json(path, require_cj1=True)
    _require_exact_keys(lock, {"artifacts", "bindings", "schema_version", "status"}, "pipeline schema lock")
    if lock["schema_version"] != "1.0.0" or lock["status"] != "FROZEN_STAGE_4_SCHEMA_SOURCE_BLOCKED":
        raise PipelineSchemaError("pipeline schema lock identity/status drift")
    if lock["bindings"] != {
        "baseline_lock_sha256": sha256_file(repo_root / "goal-4/baseline-lock.json"),
        "guardrails_sha256": sha256_file(repo_root / "goal-4/guardrails.json"),
        "witness_lock_sha256": sha256_file(repo_root / "goal-4/witness-lock.json"),
    }:
        raise PipelineSchemaError("pipeline schema lock upstream bindings drift")
    seen: set[str] = set()
    for row in lock["artifacts"]:
        _require_exact_keys(row, {"byte_size", "path", "sha256"}, "pipeline lock artifact")
        relative = row["path"]
        _safe_repo_path(relative, "pipeline lock artifact")
        if relative == "goal-4/tools/validate_pipeline_schemas.py":
            raise PipelineSchemaError("validator must be excluded from its externally pinned lock")
        if relative in seen:
            raise PipelineSchemaError("duplicate pipeline lock artifact")
        seen.add(relative)
        artifact = repo_root / relative
        if artifact.stat().st_size != row["byte_size"] or sha256_file(artifact) != row["sha256"]:
            raise PipelineSchemaError(f"pipeline lock artifact drift: {relative}")
    required = {
        PIPELINE_CONTRACT_PATH,
        "goal-4/tools/pipeline_schema_lib.py",
        "goal-4/tests/test_pipeline_schemas.py",
    }
    contract = load_json(repo_root / PIPELINE_CONTRACT_PATH, require_cj1=True)
    required.update(contract["schema_files"])
    if seen != required:
        raise PipelineSchemaError(
            f"pipeline lock artifact set drift: missing={sorted(required - seen)}, extra={sorted(seen - required)}"
        )
    return lock


def validate_package(repo_root: Path, expected_lock_sha256: str) -> dict[str, int | str]:
    contract, registry = validate_pipeline_contract(repo_root)
    lock = validate_lock(repo_root, expected_lock_sha256)
    return {
        "artifact_count": len(lock["artifacts"]),
        "ledger_schema_count": len(contract["ledgers"]),
        "lock_sha256": expected_lock_sha256,
        "schema_count": len(registry.schemas),
    }


def clone(value: Any) -> Any:
    """Deep-copy helper used by mutation tests without relying on assertions."""

    return deepcopy(value)
