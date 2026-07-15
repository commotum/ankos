"""Strict, dependency-free validation for the Goal 4 Stage 4 schema package.

This module implements only the closed JSON Schema 2020-12 subset used by
``goal-4/schemas``.  Semantic checks that span records or frozen contracts are
kept explicit here; attractive JSON that merely satisfies shape constraints is
not sufficient to cross an evidence, review, role, or release gate.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import hashlib
import json
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
GUARDRAIL_OPERATION_TAGS = frozenset(
    {"WITNESS_ONLY_AUTHOR_TEXT_INSERTION", "AUTHORIAL_STRUCTURE_OR_HIERARCHY_CHANGE"}
)
OVERLAY_OPERATION_TAGS = frozenset(
    {
        "LEXICAL_ONLY",
        "STRUCTURAL",
        "FORMULA_SYMBOL",
        "CODE_SEMANTICS",
        "DATA_SEMANTICS",
        "FIGURE_SEMANTICS",
        "INDEX_SEMANTICS",
    }
)
HIGH_RISK_OPERATION_TAGS = frozenset(
    GUARDRAIL_OPERATION_TAGS | (OVERLAY_OPERATION_TAGS - {"LEXICAL_ONLY"})
)
GUARDRAIL_AST_TAGS = frozenset(
    {"HEADING_CHANGE", "MARKDOWN_STRUCTURE_CHANGE", "BOUNDARY_CHANGE", "INDEX_ORDER_CHANGE"}
)
OVERLAY_AST_TAGS = frozenset(
    {
        "HEADING_DEPTH",
        "PARAGRAPH_BOUNDARY",
        "LIST_STRUCTURE",
        "FENCE_STRUCTURE",
        "TABLE_STRUCTURE",
        "MATH_STRUCTURE",
        "CODE_STRUCTURE",
        "BLOCK_BOUNDARY",
    }
)
HIGH_RISK_AST_TAGS = frozenset(GUARDRAIL_AST_TAGS | OVERLAY_AST_TAGS)
OPERATION_RISK_TAGS = frozenset(GUARDRAIL_OPERATION_TAGS | OVERLAY_OPERATION_TAGS)
AST_IMPACT_TAGS = frozenset(GUARDRAIL_AST_TAGS | OVERLAY_AST_TAGS)
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


@dataclass(frozen=True, slots=True)
class ValidatedRepairBinding:
    """Hash bridge from one validated registry row to one overlay operation."""

    repair_id: str
    repair_row_sha256: str
    operation_projection_sha256: str
    expected_target_sha256: str
    expected_result_sha256: str
    forward_payload_sha256: str
    inverse_payload_sha256: str
    overlay_operation_bound: bool


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


def _read_output_file(output_root: Path | None, relative: str, field: str) -> bytes:
    """Read one declared output while rejecting absence, links, and root escape."""

    _safe_repo_path(relative, field)
    if output_root is None:
        raise PipelineSchemaError(f"{field} lacks a concrete output root")
    root = output_root.resolve()
    if not output_root.is_dir() or output_root.is_symlink():
        raise PipelineSchemaError(f"{field} output root is absent, non-directory, or symlinked")
    candidate = output_root / relative
    try:
        candidate.resolve().relative_to(root)
    except ValueError as exc:
        raise PipelineSchemaError(f"{field} escapes its concrete output root") from exc
    current = output_root
    for part in PurePosixPath(relative).parts:
        current = current / part
        if current.is_symlink():
            raise PipelineSchemaError(f"{field} traverses a symlinked output component")
    if not candidate.is_file() or candidate.is_symlink():
        raise PipelineSchemaError(f"{field} does not identify a concrete regular output file")
    return candidate.read_bytes()


def _validate_output_span(
    *,
    output_root: Path | None,
    path: str,
    span: Mapping[str, Any],
    field: str,
    expected_bytes: bytes | None = None,
) -> bytes:
    payload = _read_output_file(output_root, path, field)
    start = span["start_byte"]
    end = span["end_byte_exclusive"]
    if start < 0 or end <= start or end > len(payload):
        raise PipelineSchemaError(f"{field} span is empty, reversed, or outside the output file")
    selected = payload[start:end]
    if sha256_bytes(selected) != span["sha256"]:
        raise PipelineSchemaError(f"{field} span hash does not join concrete output bytes")
    if expected_bytes is not None and selected != expected_bytes:
        raise PipelineSchemaError(f"{field} span bytes differ from the declared projection")
    return selected


def _validated_ast_nodes(
    registry: SchemaRegistry, ast_nodes: Sequence[Mapping[str, Any]]
) -> dict[str, Mapping[str, Any]]:
    by_id: dict[str, Mapping[str, Any]] = {}
    indexes = _frozen_indexes(registry)
    for node in ast_nodes:
        registry.validate("goal-4/schemas/ast-node.schema.json", node)
        node_id = node["node_id"]
        if node_id in by_id:
            raise PipelineSchemaError("duplicate AST node ID")
        by_id[node_id] = node
        _safe_repo_path(node["output_path"], "AST node output path")
        projected = node["author_text_projection"].encode("utf-8")
        if sha256_bytes(projected) != node["author_text_projection_sha256"]:
            raise PipelineSchemaError("AST node author projection hash mismatch")
        span = node["output_span"]
        if span["end_byte_exclusive"] - span["start_byte"] != len(projected):
            raise PipelineSchemaError("AST node output span length differs from its projection")
        if span["sha256"] != node["author_text_projection_sha256"]:
            raise PipelineSchemaError("AST node output span hash differs from its projection")
        _validate_raw_block_ids(registry, node["raw_span_ids"])
        if node["content_role"] == "CANONICAL_AUTHOR_TEXT":
            document = indexes["documents_by_id"].get(node["canonical_document_id"])
            if document is None or node["output_path"] != document["path"]:
                raise PipelineSchemaError("canonical AST node does not join guardrail document/path")
            if any(
                indexes["blocks_by_id"][block_id]["canonical_document_id"]
                != node["canonical_document_id"]
                for block_id in node["raw_span_ids"]
            ):
                raise PipelineSchemaError("AST node raw spans cross its canonical document")
        elif node["canonical_document_id"] is not None:
            raise PipelineSchemaError("noncanonical AST node claims a canonical document")
    return by_id


def _join_output_node_partition(
    *,
    node_ids: Sequence[str],
    ast_by_id: Mapping[str, Mapping[str, Any]],
    output_root: Path | None,
    output_path: str,
    canonical_document_id: str,
    target_span: Mapping[str, Any],
    raw_block_ids: Sequence[str],
) -> None:
    if not node_ids:
        raise PipelineSchemaError("canonical output span lacks owning AST nodes")
    try:
        nodes = [ast_by_id[node_id] for node_id in node_ids]
    except KeyError as exc:
        raise PipelineSchemaError("canonical output span references an absent AST node") from exc
    if len(node_ids) != len(set(node_ids)):
        raise PipelineSchemaError("canonical output span repeats an AST node")
    nodes = sorted(nodes, key=lambda row: row["output_span"]["start_byte"])
    cursor = target_span["start_byte"]
    joined_raw: list[str] = []
    for node in nodes:
        if (
            node["content_role"] != "CANONICAL_AUTHOR_TEXT"
            or node["canonical_document_id"] != canonical_document_id
            or node["output_path"] != output_path
            or node["output_span"]["start_byte"] != cursor
        ):
            raise PipelineSchemaError("AST node does not exactly partition its canonical output span")
        node_bytes = node["author_text_projection"].encode("utf-8")
        _validate_output_span(
            output_root=output_root,
            path=output_path,
            span=node["output_span"],
            field="AST node output",
            expected_bytes=node_bytes,
        )
        cursor = node["output_span"]["end_byte_exclusive"]
        joined_raw.extend(node["raw_span_ids"])
    if cursor != target_span["end_byte_exclusive"]:
        raise PipelineSchemaError("AST nodes do not reach the canonical output-span end")
    if joined_raw != list(raw_block_ids):
        raise PipelineSchemaError("AST-node raw spans do not exactly join provenance raw blocks")


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


_INVERSE_OPERATION_TYPES = {
    "REPLACE": "REPLACE",
    "DELETE": "ANCHORED_INSERT",
    "ANCHORED_INSERT": "DELETE",
    "MOVE": "MOVE",
    "SPLIT": "MERGE",
    "MERGE": "SPLIT",
}


def _hex_bytes(value: str, field: str, *, nonempty: bool = True) -> bytes:
    if not isinstance(value, str) or re.fullmatch(r"(?:[0-9a-f]{2})*", value) is None:
        raise PipelineSchemaError(f"{field} is not canonical lowercase byte hex")
    data = bytes.fromhex(value)
    if nonempty and not data:
        raise PipelineSchemaError(f"{field} is empty")
    return data


def _operation_fields(operation: Mapping[str, Any], label: str) -> Mapping[str, Any]:
    fields = operation["payload"]["operation_fields"]
    if fields["operation_type"] != operation["operation_type"]:
        raise PipelineSchemaError(f"{label} typed payload operation type differs from its envelope")
    expected = {
        "REPLACE": {"operation_type", "block_id", "expected_block_sha256", "preimage_hex", "replacement_hex", "expected_count"},
        "DELETE": {"operation_type", "block_id", "expected_block_sha256", "preimage_hex", "expected_count"},
        "ANCHORED_INSERT": {"operation_type", "block_id", "expected_block_sha256", "left_anchor_hex", "right_anchor_hex", "insertion_hex", "expected_adjacency_count"},
        "MOVE": {"operation_type", "block_id", "expected_block_sha256", "source_left_id", "source_right_id", "destination_left_id", "destination_right_id", "expected_source_adjacency_count", "expected_destination_adjacency_count"},
        "SPLIT": {"operation_type", "block_id", "expected_block_sha256", "parts", "expected_block_count"},
        "MERGE": {"operation_type", "block_ids", "expected_block_sha256s", "merged_block", "expected_adjacency_count"},
    }[operation["operation_type"]]
    _require_exact_keys(fields, expected, f"{label} typed operation payload")
    for field in ("preimage_hex", "replacement_hex", "left_anchor_hex", "right_anchor_hex", "insertion_hex"):
        if field in fields:
            _hex_bytes(fields[field], f"{label} {field}")
    return fields


def _validate_operation_inverse_pair(
    forward: Mapping[str, Any], inverse: Mapping[str, Any]
) -> None:
    """Validate the declared exact inverse descriptor, not only its operation name."""

    forward_type = forward["operation_type"]
    inverse_type = inverse["operation_type"]
    if _INVERSE_OPERATION_TYPES[forward_type] != inverse_type:
        raise PipelineSchemaError("inverse operation type is not the exact forward inverse")
    forward_payload = forward["payload"]
    inverse_payload = inverse["payload"]
    if inverse_payload["source_node_ids"] != forward_payload["target_node_ids"]:
        raise PipelineSchemaError("inverse source-node set does not reverse forward targets")
    if inverse_payload["target_node_ids"] != forward_payload["source_node_ids"]:
        raise PipelineSchemaError("inverse target-node set does not reverse forward sources")
    before = _operation_fields(forward, "forward")
    after = _operation_fields(inverse, "inverse")

    if forward_type == "MOVE":
        pairs = (
            ("block_id", "block_id"),
            ("expected_block_sha256", "expected_block_sha256"),
            ("source_left_id", "destination_left_id"),
            ("source_right_id", "destination_right_id"),
            ("destination_left_id", "source_left_id"),
            ("destination_right_id", "source_right_id"),
            ("expected_source_adjacency_count", "expected_destination_adjacency_count"),
            ("expected_destination_adjacency_count", "expected_source_adjacency_count"),
        )
        if any(before[left] != after[right] for left, right in pairs):
            raise PipelineSchemaError("MOVE inverse payload does not swap exact adjacencies")
    elif forward_type == "REPLACE":
        if (
            before["block_id"] != after["block_id"]
            or before["preimage_hex"] != after["replacement_hex"]
            or before["replacement_hex"] != after["preimage_hex"]
            or before["expected_count"] != after["expected_count"]
        ):
            raise PipelineSchemaError("REPLACE inverse payload does not swap exact byte strings")
    elif forward_type == "DELETE":
        if (
            before["block_id"] != after["block_id"]
            or before["preimage_hex"] != after["insertion_hex"]
            or before["expected_count"] != after["expected_adjacency_count"]
        ):
            raise PipelineSchemaError("DELETE inverse payload does not restore the deleted bytes")
    elif forward_type == "ANCHORED_INSERT":
        if (
            before["block_id"] != after["block_id"]
            or before["insertion_hex"] != after["preimage_hex"]
            or before["expected_adjacency_count"] != after["expected_count"]
        ):
            raise PipelineSchemaError("ANCHORED_INSERT inverse payload does not delete the insertion")
    elif forward_type == "SPLIT":
        parts = before["parts"]
        part_ids = [part["block_id"] for part in parts]
        part_bytes = [_hex_bytes(part["data_hex"], "split part data") for part in parts]
        if (
            after["block_ids"] != part_ids
            or after["expected_block_sha256s"]
            != [sha256_bytes(data) for data in part_bytes]
            or after["merged_block"]["block_id"] != before["block_id"]
            or _hex_bytes(after["merged_block"]["data_hex"], "inverse merged block data")
            != b"".join(part_bytes)
            or after["expected_adjacency_count"] != 1
        ):
            raise PipelineSchemaError("SPLIT inverse payload is not the exact part merge")
    elif forward_type == "MERGE":
        merged = _hex_bytes(before["merged_block"]["data_hex"], "merged block data")
        parts = after["parts"]
        part_ids = [part["block_id"] for part in parts]
        part_bytes = [_hex_bytes(part["data_hex"], "inverse split part data") for part in parts]
        if (
            after["block_id"] != before["merged_block"]["block_id"]
            or after["expected_block_sha256"] != sha256_bytes(merged)
            or part_ids != before["block_ids"]
            or [sha256_bytes(data) for data in part_bytes]
            != before["expected_block_sha256s"]
            or b"".join(part_bytes) != merged
            or after["expected_block_count"] != 1
        ):
            raise PipelineSchemaError("MERGE inverse payload is not the exact source split")


def _typed_overlay_operation_fields(operation: Any, overlay_lib: Any) -> Mapping[str, Any]:
    """Project every operation-specific dataclass field to canonical JSON values."""

    if isinstance(operation, overlay_lib.Replace):
        return {
            "block_id": operation.block_id,
            "expected_block_sha256": operation.expected_block_sha256,
            "expected_count": operation.expected_count,
            "operation_type": "REPLACE",
            "preimage_hex": operation.preimage.hex(),
            "replacement_hex": operation.replacement.hex(),
        }
    if isinstance(operation, overlay_lib.Delete):
        return {
            "block_id": operation.block_id,
            "expected_block_sha256": operation.expected_block_sha256,
            "expected_count": operation.expected_count,
            "operation_type": "DELETE",
            "preimage_hex": operation.preimage.hex(),
        }
    if isinstance(operation, overlay_lib.AnchoredInsert):
        return {
            "block_id": operation.block_id,
            "expected_adjacency_count": operation.expected_adjacency_count,
            "expected_block_sha256": operation.expected_block_sha256,
            "insertion_hex": operation.insertion.hex(),
            "left_anchor_hex": operation.left_anchor.hex(),
            "operation_type": "ANCHORED_INSERT",
            "right_anchor_hex": operation.right_anchor.hex(),
        }
    if isinstance(operation, overlay_lib.Move):
        return {
            "block_id": operation.block_id,
            "destination_left_id": operation.destination_left_id,
            "destination_right_id": operation.destination_right_id,
            "expected_block_sha256": operation.expected_block_sha256,
            "expected_destination_adjacency_count": operation.expected_destination_adjacency_count,
            "expected_source_adjacency_count": operation.expected_source_adjacency_count,
            "operation_type": "MOVE",
            "source_left_id": operation.source_left_id,
            "source_right_id": operation.source_right_id,
        }
    if isinstance(operation, overlay_lib.Split):
        return {
            "block_id": operation.block_id,
            "expected_block_count": operation.expected_block_count,
            "expected_block_sha256": operation.expected_block_sha256,
            "operation_type": "SPLIT",
            "parts": [
                {"block_id": part.block_id, "data_hex": part.data.hex()}
                for part in operation.parts
            ],
        }
    if isinstance(operation, overlay_lib.Merge):
        return {
            "block_ids": list(operation.block_ids),
            "expected_adjacency_count": operation.expected_adjacency_count,
            "expected_block_sha256s": list(operation.expected_block_sha256s),
            "merged_block": {
                "block_id": operation.merged_block.block_id,
                "data_hex": operation.merged_block.data.hex(),
            },
            "operation_type": "MERGE",
        }
    raise PipelineSchemaError("overlay operation is not one of the six closed typed operations")


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
        "after_target_sha256": record["target_state_guards"]["after_sha256"],
        "before_projection_sha256": record["before_projection"]["sha256"],
        "before_target_sha256": record["target_state_guards"]["before_sha256"],
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


def canonical_repair_row_sha256(record: Mapping[str, Any]) -> str:
    """Hash exact ANKOS-CJ-1 bytes for authority/ledger row binding."""

    _reject_floats(record, "repair row")
    return sha256_bytes(canonical_json_bytes(record))


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


def validate_repair(
    record: Mapping[str, Any], registry: SchemaRegistry
) -> ValidatedRepairBinding:
    schema_path = "goal-4/schemas/repair-record.schema.json"
    registry.validate(schema_path, record)
    validate_workflow(record["workflow"])
    if record["baseline_lock_sha256"] != sha256_file(registry.repo_root / "goal-4/baseline-lock.json"):
        raise PipelineSchemaError("repair does not bind the frozen baseline lock")
    if record["operation_projection_sha256"] == "0" * 64:
        raise PipelineSchemaError("repair operation projection uses an all-zero placeholder")
    if any(
        record["target_state_guards"][field] == "0" * 64
        for field in ("before_sha256", "after_sha256")
    ):
        raise PipelineSchemaError("repair target-state guard uses an all-zero placeholder")
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
    target = record["target"]
    indexes = _frozen_indexes(registry)
    if target["role"] == "CANONICAL_AUTHOR_TEXT":
        document = indexes["documents_by_id"].get(target["canonical_document_id"])
        if document is None or target["path"] != document["path"]:
            raise PipelineSchemaError("canonical repair target does not join guardrail document/path")
    elif target["canonical_document_id"] is not None:
        raise PipelineSchemaError("noncanonical repair target claims a canonical document ID")
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
    if target["role"] == "CANONICAL_AUTHOR_TEXT":
        guard_block_ids = (
            guard["raw_block_ids"]
            if guard["guard_kind"] == "PREIMAGE"
            else [guard["left_anchor"]["raw_block_id"], guard["right_anchor"]["raw_block_id"]]
        )
        if any(
            indexes["blocks_by_id"][block_id]["canonical_document_id"]
            != target["canonical_document_id"]
            for block_id in guard_block_ids
        ):
            raise PipelineSchemaError("canonical repair target does not match guarded raw document")
    forward = record["forward_operation"]
    inverse = record["inverse_operation"]
    for label, operation in (("forward", forward), ("inverse", inverse)):
        if sha256_bytes(canonical_json_bytes(operation["payload"])[:-1]) != operation["payload_sha256"]:
            raise PipelineSchemaError(f"{label} operation payload hash mismatch")
        _operation_fields(operation, label)
    _validate_operation_inverse_pair(forward, inverse)
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
    return ValidatedRepairBinding(
        repair_id=record["repair_id"],
        repair_row_sha256=canonical_repair_row_sha256(record),
        operation_projection_sha256=record["operation_projection_sha256"],
        expected_target_sha256=record["target_state_guards"]["before_sha256"],
        expected_result_sha256=record["target_state_guards"]["after_sha256"],
        forward_payload_sha256=record["forward_operation"]["payload_sha256"],
        inverse_payload_sha256=record["inverse_operation"]["payload_sha256"],
        overlay_operation_bound=False,
    )


def validate_overlay_operation_binding(
    record: Mapping[str, Any],
    registry: SchemaRegistry,
    overlay_operation: Any,
    review_records: Sequence[Mapping[str, Any]] = (),
) -> ValidatedRepairBinding:
    """Authenticate one JSON repair row against overlay_lib's exact operation hash.

    This is the only schema/overlay bridge intended for authority minting.  A
    bare row binding returned by :func:`validate_repair` is explicitly marked
    unbound and must not be used as an authority grant.
    """

    binding = validate_repair(record, registry)
    try:
        import overlay_lib

        operation_sha = overlay_lib.operation_projection_sha256(overlay_operation)
    except (AttributeError, TypeError, ValueError) as exc:
        raise PipelineSchemaError(f"invalid typed overlay operation: {exc}") from exc
    if operation_sha != record["operation_projection_sha256"]:
        raise PipelineSchemaError("repair row does not bind exact overlay operation projection")
    meta = overlay_operation.meta
    target = record["target"]
    if target["role"] != "CANONICAL_AUTHOR_TEXT" or target["canonical_document_id"] is None:
        raise PipelineSchemaError("authority bridge is restricted to canonical author-text operations")
    expected_meta = {
        "creator_principal_id": record["creator"]["principal_id"],
        "dependencies": tuple(record["dependencies"]),
        "expected_result_sha256": record["target_state_guards"]["after_sha256"],
        "expected_target_sha256": record["target_state_guards"]["before_sha256"],
        "final_disposition": record["workflow"]["final_disposition"],
        "repair_class": record["repair_class"],
        "repair_id": record["repair_id"],
        "target_id": target["canonical_document_id"],
        "target_path": target["path"],
        "target_role": target["role"],
        "validated_ast_impact": tuple(
            sorted(set(record["risk"]["ast_impact_tags"]) & OVERLAY_AST_TAGS)
        ),
        "validated_risk_tags": tuple(
            sorted(set(record["risk"]["operation_tags"]) & OVERLAY_OPERATION_TAGS)
        ),
        "workflow_state": record["workflow"]["state"],
    }
    for field, expected in expected_meta.items():
        if getattr(meta, field) != expected:
            raise PipelineSchemaError(f"overlay operation metadata differs from repair row: {field}")
    if overlay_operation.operation != record["forward_operation"]["operation_type"]:
        raise PipelineSchemaError("overlay operation type differs from repair forward operation")
    expected_operation_fields = _typed_overlay_operation_fields(overlay_operation, overlay_lib)
    if record["forward_operation"]["payload"]["operation_fields"] != expected_operation_fields:
        raise PipelineSchemaError("overlay typed operation fields differ from repair forward payload")
    guard = record["guard"]
    raw_block_ids = (
        guard["raw_block_ids"]
        if guard["guard_kind"] == "PREIMAGE"
        else [guard["left_anchor"]["raw_block_id"], guard["right_anchor"]["raw_block_id"]]
    )
    if meta.raw_source_id not in raw_block_ids:
        raise PipelineSchemaError("overlay raw-source ID does not join repair guard blocks")
    raw_row = _frozen_indexes(registry)["blocks_by_id"][meta.raw_source_id]
    if meta.raw_source_row_sha256 != sha256_bytes(canonical_json_bytes(raw_row)):
        raise PipelineSchemaError("overlay raw-source row hash does not bind Stage 2 ledger row")
    expected_span_sha = (
        guard["span"]["sha256"]
        if guard["guard_kind"] == "PREIMAGE"
        else sha256_bytes(
            (
                guard["left_anchor"]["text"] + guard["right_anchor"]["text"]
            ).encode("utf-8")
        )
    )
    if meta.raw_source_span_sha256 != expected_span_sha:
        raise PipelineSchemaError("overlay raw-source span hash does not bind repair guard")
    if meta.witness is not None or record["evidence"]["authoritative"]:
        raise PipelineSchemaError("current SOURCE_BLOCKED authority cannot carry witness metadata")
    review_by_id = validate_review_set(review_records, registry)
    if set(record["review_ids"]) != set(review_by_id).intersection(record["review_ids"]):
        raise PipelineSchemaError("overlay authority review IDs do not join validated review rows")
    if record["review_ids"]:
        source_rows = [
            review_by_id[review_id]
            for review_id in record["review_ids"]
            if review_by_id[review_id]["reviewer_role"] == "SOURCE_REVIEWER"
        ]
        specialist_rows = [
            review_by_id[review_id]
            for review_id in record["review_ids"]
            if review_by_id[review_id]["reviewer_role"] == "SPECIALIST_REVIEWER"
        ]
        if len(source_rows) != 1:
            raise PipelineSchemaError("overlay authority lacks exactly one source-review row")
        source = source_rows[0]
        if source["agreement_state"] != "AGREES" or source["closure_state"] != "CLOSED":
            raise PipelineSchemaError("overlay source review is not closed and approving")
        if meta.review is None:
            raise PipelineSchemaError("overlay metadata omits the registry source review")
        expected_source_fields = {
            "blind_preproposal": source["blind_preproposal"],
            "creator_principal_id": record["creator"]["principal_id"],
            "evidence_view_sha256": source["evidence_view_sha256"],
            "review_id": source["review_id"],
            "review_row_sha256": sha256_bytes(canonical_json_bytes(source)),
            "source_decision": "APPROVED",
            "source_reviewer_principal_id": source["principal_id"],
            "source_reviewer_role": source["reviewer_role"],
            "source_reviewer_session_id": source["session_id"],
            "source_reviewer_type": source["reviewer_type"],
        }
        for field, expected in expected_source_fields.items():
            if getattr(meta.review, field) != expected:
                raise PipelineSchemaError(
                    f"overlay source-review metadata differs from exact registry row: {field}"
                )
        if specialist_rows:
            if len(specialist_rows) != 1:
                raise PipelineSchemaError("overlay authority has ambiguous specialist-review rows")
            specialist = specialist_rows[0]
            if specialist["agreement_state"] != "AGREES" or specialist["closure_state"] != "CLOSED":
                raise PipelineSchemaError("overlay specialist review is not closed and approving")
            expected_specialist_fields = {
                "specialist_decision": "APPROVED",
                "specialist_evidence_view_sha256": specialist["evidence_view_sha256"],
                "specialist_principal_id": specialist["principal_id"],
                "specialist_review_id": specialist["review_id"],
                "specialist_review_row_sha256": sha256_bytes(canonical_json_bytes(specialist)),
                "specialist_role": specialist["reviewer_role"],
                "specialist_session_id": specialist["session_id"],
                "specialist_specialty": specialist["specialty"],
                "specialist_type": specialist["reviewer_type"],
            }
            for field, expected in expected_specialist_fields.items():
                if getattr(meta.review, field) != expected:
                    raise PipelineSchemaError(
                        f"overlay specialist-review metadata differs from exact registry row: {field}"
                    )
        else:
            for field in (
                "specialist_decision",
                "specialist_evidence_view_sha256",
                "specialist_principal_id",
                "specialist_review_id",
                "specialist_review_row_sha256",
                "specialist_role",
                "specialist_session_id",
                "specialist_specialty",
                "specialist_type",
            ):
                if getattr(meta.review, field) is not None:
                    raise PipelineSchemaError(
                        f"overlay carries unjoined specialist-review metadata: {field}"
                    )
    elif meta.review is not None:
        raise PipelineSchemaError("overlay operation carries a review absent from repair row")
    return ValidatedRepairBinding(
        repair_id=binding.repair_id,
        repair_row_sha256=binding.repair_row_sha256,
        operation_projection_sha256=operation_sha,
        expected_target_sha256=binding.expected_target_sha256,
        expected_result_sha256=binding.expected_result_sha256,
        forward_payload_sha256=binding.forward_payload_sha256,
        inverse_payload_sha256=binding.inverse_payload_sha256,
        overlay_operation_bound=True,
    )


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
) -> dict[str, ValidatedRepairBinding]:
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
    bindings: dict[str, ValidatedRepairBinding] = {}
    by_id = {record["repair_id"]: record for record in records}
    for record in records:
        bindings[record["repair_id"]] = validate_repair(record, registry)
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
    return bindings


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


def validate_provenance(
    record: Mapping[str, Any],
    registry: SchemaRegistry,
    *,
    output_root: Path | None = None,
    ast_nodes: Sequence[Mapping[str, Any]] = (),
    _ast_by_id: Mapping[str, Mapping[str, Any]] | None = None,
) -> None:
    registry.validate("goal-4/schemas/provenance-record.schema.json", record)
    kind = record["mapping_kind"]
    source = record["source"]
    target = record["target"]
    for label, endpoint in (("source", source), ("target", target)):
        path = endpoint["path"]
        if path is not None:
            _safe_repo_path(path, f"provenance {label} path")
        if endpoint["role"] is not None and endpoint["role"] not in RELEASE_ROLES:
            raise PipelineSchemaError(f"provenance {label} has an unknown release role")
        if not set(endpoint["witness_region_ids"]).issubset(
            _frozen_indexes(registry)["witness_region_ids"]
        ):
            raise PipelineSchemaError(f"provenance {label} witness region does not join Stage 3")
    if kind in {"RAW_PRESERVED", "RAW_REPAIRED", "RAW_EXCLUDED"}:
        if source["endpoint_kind"] != "RAW_SPAN" or source["span"] is None or source["path"] is None:
            raise PipelineSchemaError("raw provenance lacks a typed raw-span source")
        raw_bytes = _validate_raw_span(
            registry,
            source_path=source["path"],
            source_sha256=_frozen_indexes(registry)["input_by_path"].get(source["path"], {}).get("sha256", ""),
            span=source["span"],
            raw_block_ids=source["raw_block_ids"],
        )
        if source["author_text_projection_sha256"] != sha256_bytes(raw_bytes):
            raise PipelineSchemaError("raw provenance source projection does not equal raw bytes")
        block_rows = [
            _frozen_indexes(registry)["blocks_by_id"][block_id]
            for block_id in source["raw_block_ids"]
        ]
        document_id = block_rows[0]["canonical_document_id"]
        if source["canonical_document_id"] != document_id:
            raise PipelineSchemaError("raw provenance source document does not join Stage 2 blocks")
    if kind == "WITNESS_INSERTED":
        if source["endpoint_kind"] != "WITNESS_REGION" or not source["witness_region_ids"]:
            raise PipelineSchemaError("witness insertion lacks a typed witness-region source")
        raise PipelineSchemaError("current SOURCE_BLOCKED gate forbids witness insertion provenance")
    if kind == "GENERATED_METADATA":
        empty = sha256_bytes(b"")
        if (
            record["author_text_projection_sha256"] != empty
            or source["endpoint_kind"] != "GENERATED_NONE"
            or source["path"] is not None
            or source["role"] is not None
            or source["span"] is not None
            or source["raw_block_ids"]
            or source["witness_region_ids"]
            or source["author_text_projection_sha256"] != empty
            or target["endpoint_kind"] != "GENERATED_SPAN"
            or target["role"] != "GENERATED_METADATA"
            or target["path"] is None
            or target["author_text_projection_sha256"] != empty
            or record["inverse"]["inverse_kind"] != "REMOVE_GENERATED"
            or record["repair_ids"]
            or record["inverse"]["repair_ids"]
        ):
            raise PipelineSchemaError("generated metadata has nonempty projection or wrong inverse")
    if kind == "RAW_PRESERVED":
        indexes = _frozen_indexes(registry)
        document_id = source["canonical_document_id"]
        document = indexes["documents_by_id"].get(document_id)
        if (
            target["endpoint_kind"] != "CANONICAL_SPAN"
            or target["role"] != "CANONICAL_AUTHOR_TEXT"
            or document is None
            or target["canonical_document_id"] != document_id
            or target["path"] != document["path"]
            or target["span"] is None
            or target["raw_block_ids"] != source["raw_block_ids"]
            or target["witness_region_ids"]
            or source["author_text_projection_sha256"] != target["author_text_projection_sha256"]
            or record["author_text_projection_sha256"] != source["author_text_projection_sha256"]
            or record["repair_ids"]
            or record["inverse"] != {"inverse_kind": "IDENTITY", "repair_ids": []}
        ):
            raise PipelineSchemaError("RAW_PRESERVED projection changed")
        output_bytes = _validate_output_span(
            output_root=output_root,
            path=target["path"],
            span=target["span"],
            field="RAW_PRESERVED target",
            expected_bytes=raw_bytes,
        )
        if target["author_text_projection_sha256"] != sha256_bytes(output_bytes):
            raise PipelineSchemaError("RAW_PRESERVED target projection does not equal output bytes")
        ast_by_id = (
            _validated_ast_nodes(registry, ast_nodes)
            if _ast_by_id is None
            else _ast_by_id
        )
        _join_output_node_partition(
            node_ids=record["node_ids"],
            ast_by_id=ast_by_id,
            output_root=output_root,
            output_path=target["path"],
            canonical_document_id=document_id,
            target_span=target["span"],
            raw_block_ids=target["raw_block_ids"],
        )
    elif kind == "RAW_REPAIRED":
        if target["endpoint_kind"] != "CANONICAL_SPAN" or not record["repair_ids"]:
            raise PipelineSchemaError("RAW_REPAIRED lacks canonical target/joined repair")
        raise PipelineSchemaError("current SOURCE_BLOCKED gate forbids repaired raw provenance")
    elif kind == "RAW_EXCLUDED":
        if (
            target["endpoint_kind"] != "TYPED_EXCLUSION"
            or target["path"] is not None
            or target["span"] is not None
            or target["role"] is not None
            or target["author_text_projection_sha256"] != sha256_bytes(b"")
        ):
            raise PipelineSchemaError("RAW_EXCLUDED lacks a typed empty exclusion target")
        raise PipelineSchemaError("current SOURCE_BLOCKED gate forbids raw author-text exclusion")
    elif kind in {
        "CANONICAL_DERIVED",
        "CANONICAL_EDITORIAL_REFERENCE",
        "CANONICAL_SEARCH_DERIVATIVE",
    }:
        expected = {
            "CANONICAL_DERIVED": ("DERIVED_SPAN", "DERIVED_AGGREGATE", "DROP_DERIVED_VIEW"),
            "CANONICAL_EDITORIAL_REFERENCE": ("SIDECAR_SPAN", "EDITORIAL_SIDECAR", "DROP_DERIVED_VIEW"),
            "CANONICAL_SEARCH_DERIVATIVE": ("SEARCH_SPAN", "SEARCH_DERIVATIVE", "DROP_DERIVED_VIEW"),
        }[kind]
        if (
            source["endpoint_kind"] != "CANONICAL_SPAN"
            or source["role"] != "CANONICAL_AUTHOR_TEXT"
            or target["endpoint_kind"] != expected[0]
            or target["role"] != expected[1]
            or target["path"] is None
            or source["author_text_projection_sha256"] != target["author_text_projection_sha256"]
            or record["author_text_projection_sha256"] != source["author_text_projection_sha256"]
            or record["inverse"]["inverse_kind"] != expected[2]
        ):
            raise PipelineSchemaError("derived provenance role/projection/inverse mismatch")


def validate_provenance_set(
    records: Sequence[Mapping[str, Any]],
    registry: SchemaRegistry,
    repair_records: Sequence[Mapping[str, Any]] = (),
    *,
    require_complete_raw_coverage: bool = False,
    output_root: Path | None = None,
    ast_nodes: Sequence[Mapping[str, Any]] = (),
) -> None:
    ids: set[str] = set()
    sequences: list[int] = []
    repair_ids = {row["repair_id"] for row in repair_records}
    covered_raw_blocks: list[str] = []
    covered_raw_spans: list[tuple[int, int]] = []
    covered_target_blocks: list[str] = []
    target_spans_by_path: dict[str, list[tuple[int, int]]] = {}
    used_node_ids: list[str] = []
    ast_by_id = _validated_ast_nodes(registry, ast_nodes)
    for record in records:
        validate_provenance(
            record,
            registry,
            output_root=output_root,
            ast_nodes=ast_nodes,
            _ast_by_id=ast_by_id,
        )
        if record["provenance_id"] in ids:
            raise PipelineSchemaError("duplicate provenance ID")
        ids.add(record["provenance_id"])
        sequences.append(record["sequence"])
        if not set(record["repair_ids"]).issubset(repair_ids):
            raise PipelineSchemaError("provenance repair ID does not join repair ledger")
        if set(record["inverse"]["repair_ids"]) != set(record["repair_ids"]):
            raise PipelineSchemaError("provenance inverse repair set does not match forward repair set")
        if record["mapping_kind"].startswith("RAW_"):
            covered_raw_blocks.extend(record["source"]["raw_block_ids"])
            span = record["source"]["span"]
            covered_raw_spans.append((span["start_byte"], span["end_byte_exclusive"]))
        if record["mapping_kind"] in {"RAW_PRESERVED", "RAW_REPAIRED"}:
            target = record["target"]
            covered_target_blocks.extend(target["raw_block_ids"])
            used_node_ids.extend(record["node_ids"])
            target_span = target["span"]
            target_spans_by_path.setdefault(target["path"], []).append(
                (target_span["start_byte"], target_span["end_byte_exclusive"])
            )
    if sequences != list(range(len(records))):
        raise PipelineSchemaError("provenance sequence is not exact ledger order")
    if len(covered_raw_blocks) != len(set(covered_raw_blocks)):
        raise PipelineSchemaError("raw block is mapped by multiple provenance rows")
    if require_complete_raw_coverage:
        expected = [row["raw_block_id"] for row in _frozen_indexes(registry)["blocks"]]
        if covered_raw_blocks != expected:
            raise PipelineSchemaError("provenance does not provide exact ordered raw-block coverage")
        monolith = _frozen_indexes(registry)["input_by_path"][
            "ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md"
        ]
        if not covered_raw_spans or covered_raw_spans[0][0] != 0:
            raise PipelineSchemaError("complete provenance does not begin at raw byte zero")
        for left, right in zip(covered_raw_spans, covered_raw_spans[1:]):
            if left[1] != right[0]:
                raise PipelineSchemaError("complete provenance raw spans have a gap/overlap")
        if covered_raw_spans[-1][1] != monolith["byte_size"]:
            raise PipelineSchemaError("complete provenance does not reach the raw monolith end")
        if covered_target_blocks != expected:
            raise PipelineSchemaError(
                "complete provenance does not provide exact ordered canonical-output block coverage"
            )
        if len(used_node_ids) != len(set(used_node_ids)):
            raise PipelineSchemaError("canonical AST node is owned by multiple provenance rows")
        expected_ast_ids = {
            node_id
            for node_id, node in ast_by_id.items()
            if node["content_role"] == "CANONICAL_AUTHOR_TEXT"
        }
        if set(used_node_ids) != expected_ast_ids:
            raise PipelineSchemaError(
                "complete provenance is not bidirectional over every canonical AST node"
            )
        documents = _frozen_indexes(registry)["documents"]
        expected_paths = {document["path"] for document in documents}
        if set(target_spans_by_path) != expected_paths:
            raise PipelineSchemaError(
                "complete provenance does not cover the exact canonical-output path universe"
            )
        for document in documents:
            path = document["path"]
            output = _read_output_file(output_root, path, "complete provenance output")
            spans = sorted(target_spans_by_path[path])
            if not spans or spans[0][0] != 0:
                raise PipelineSchemaError("canonical output provenance does not begin at byte zero")
            for left, right in zip(spans, spans[1:]):
                if left[1] != right[0]:
                    raise PipelineSchemaError(
                        "canonical output provenance has a target gap or overlap"
                    )
            if spans[-1][1] != len(output):
                raise PipelineSchemaError(
                    "canonical output provenance does not reach the concrete file end"
                )


def validate_navigation(
    record: Mapping[str, Any],
    registry: SchemaRegistry,
    *,
    ast_nodes: Sequence[Mapping[str, Any]] = (),
    navigation_by_anchor: Mapping[str, Mapping[str, Any]] | None = None,
    figure_records: Sequence[Mapping[str, Any]] = (),
    _ast_by_id: Mapping[str, Mapping[str, Any]] | None = None,
) -> None:
    registry.validate("goal-4/schemas/navigation-record.schema.json", record)
    validate_workflow(record["workflow"])
    indexes = _frozen_indexes(registry)
    _safe_repo_path(record["source_path"], "navigation source")
    document = indexes["documents_by_id"].get(record["source_document_id"])
    if document is None or document["path"] != record["source_path"]:
        raise PipelineSchemaError("navigation source document/path does not join guardrails")
    if record["destination_path"] is not None:
        _safe_repo_path(record["destination_path"], "navigation destination")
    if record["generated"] and record["author_text_projection_sha256"] != sha256_bytes(b""):
        raise PipelineSchemaError("generated navigation has nonempty author projection")
    if set(record["unresolved_ids"]) != set(record["workflow"]["unresolved_ids"]):
        raise PipelineSchemaError("navigation unresolved IDs differ from workflow blockers")
    state = record["resolution_state"]
    if state == "RESOLVED":
        if record["workflow"]["state"] != "CLOSED" or record["unresolved_ids"]:
            raise PipelineSchemaError("resolved navigation lacks a closed unblocked workflow")
    elif state == "SOURCE_BLOCKED":
        if record["workflow"]["state"] != "SOURCE_BLOCKED" or not record["unresolved_ids"]:
            raise PipelineSchemaError("source-blocked navigation lacks an exact blocked workflow")
    elif record["workflow"]["state"] == "CLOSED":
        raise PipelineSchemaError("pending/broken navigation cannot have a closed workflow")

    raw_block_id = record["raw_block_id"]
    if raw_block_id is None:
        if record["raw_line_span"] is not None:
            raise PipelineSchemaError("navigation line span lacks a Stage 2 raw block")
    else:
        raw = indexes["blocks_by_id"].get(raw_block_id)
        if raw is None or raw["canonical_document_id"] != record["source_document_id"]:
            raise PipelineSchemaError("navigation raw block does not join its source document")
        line_span = record["raw_line_span"]
        if line_span is None or line_span != {
            "start_line": raw["start_line"],
            "end_line": raw["end_line"],
        }:
            raise PipelineSchemaError("navigation line span does not exactly join its raw block")

    ast_by_id = _validated_ast_nodes(registry, ast_nodes) if _ast_by_id is None else _ast_by_id
    source_node_id = record["source_node_id"]
    if source_node_id is None or source_node_id not in ast_by_id:
        raise PipelineSchemaError("navigation source node does not join the AST ledger")
    node = ast_by_id[source_node_id]
    if (
        node["canonical_document_id"] != record["source_document_id"]
        or node["output_path"] != record["source_path"]
        or (raw_block_id is not None and raw_block_id not in node["raw_span_ids"])
    ):
        raise PipelineSchemaError("navigation source node/document/block join is inconsistent")

    record_type = record["record_type"]
    destinations = (
        record["destination_path"],
        record["destination_anchor_id"],
        record["destination_asset_id"],
    )
    if record_type == "ANCHOR":
        if (
            record["anchor_id"] is None
            or record["link_kind"] != "NONE"
            or any(value is not None for value in destinations)
            or node["fields"].get("anchor_id") != record["anchor_id"]
        ):
            raise PipelineSchemaError("ANCHOR navigation has inconsistent anchor/link fields")
    elif record_type == "LINK":
        if record["anchor_id"] is not None or record["link_kind"] == "NONE":
            raise PipelineSchemaError("LINK navigation has inconsistent link fields")
        if state == "RESOLVED" and all(value is None for value in destinations):
            raise PipelineSchemaError("resolved LINK lacks a concrete destination")
    elif record_type == "PAGE_ROUTE":
        if record["printed_page_label"] is None or record["link_kind"] != "PAGE":
            raise PipelineSchemaError("PAGE_ROUTE lacks exact page semantics")
    elif record_type == "LEGACY_COMPATIBILITY_ROUTE":
        if record["link_kind"] != "LEGACY_COMPATIBILITY" or record["destination_path"] is None:
            raise PipelineSchemaError("legacy compatibility route lacks a concrete destination")

    if state == "RESOLVED" and record["destination_anchor_id"] is not None:
        destination = (navigation_by_anchor or {}).get(record["destination_anchor_id"])
        if destination is None or (
            record["destination_path"] is not None
            and destination["source_path"] != record["destination_path"]
        ):
            raise PipelineSchemaError("resolved destination anchor does not join an exact ANCHOR row")
    if state == "RESOLVED" and record["destination_asset_id"] is not None:
        assets = {row["asset_id"]: row for row in figure_records if row["record_type"] == "ASSET_CANDIDATE"}
        asset = assets.get(record["destination_asset_id"])
        if asset is None or (
            record["destination_path"] is not None
            and asset["release_path"] != record["destination_path"]
        ):
            raise PipelineSchemaError("resolved destination asset does not join a figure asset row")


def validate_navigation_set(
    records: Sequence[Mapping[str, Any]],
    registry: SchemaRegistry,
    *,
    ast_nodes: Sequence[Mapping[str, Any]] = (),
    figure_records: Sequence[Mapping[str, Any]] = (),
) -> None:
    if [row["sequence"] for row in records] != list(range(len(records))):
        raise PipelineSchemaError("navigation ledger sequence is not exact ledger order")
    ids = [row["navigation_id"] for row in records]
    if len(ids) != len(set(ids)):
        raise PipelineSchemaError("duplicate navigation ID")
    anchors = [row for row in records if row["record_type"] == "ANCHOR"]
    anchor_ids = [row["anchor_id"] for row in anchors]
    if len(anchor_ids) != len(set(anchor_ids)):
        raise PipelineSchemaError("duplicate navigation anchor ID")
    by_anchor = {row["anchor_id"]: row for row in anchors}
    ast_by_id = _validated_ast_nodes(registry, ast_nodes)
    for row in records:
        validate_navigation(
            row,
            registry,
            ast_nodes=ast_nodes,
            navigation_by_anchor=by_anchor,
            figure_records=figure_records,
            _ast_by_id=ast_by_id,
        )


def validate_technical(
    record: Mapping[str, Any],
    registry: SchemaRegistry,
    repair_records: Sequence[Mapping[str, Any]] = (),
    review_records: Sequence[Mapping[str, Any]] = (),
    unresolved_records: Sequence[Mapping[str, Any]] = (),
    *,
    output_root: Path | None = None,
    ast_nodes: Sequence[Mapping[str, Any]] = (),
) -> None:
    registry.validate("goal-4/schemas/technical-record.schema.json", record)
    validate_workflow(record["workflow"])
    indexes = _frozen_indexes(registry)
    if record["canonical_document_id"] not in indexes["documents_by_id"]:
        raise PipelineSchemaError("technical span document does not join guardrails")
    document = indexes["documents_by_id"][record["canonical_document_id"]]
    if record["output_path"] != document["path"]:
        raise PipelineSchemaError("technical output path does not join its canonical document")
    _validate_raw_block_ids(registry, record["raw_block_ids"])
    block_rows = [indexes["blocks_by_id"][block_id] for block_id in record["raw_block_ids"]]
    if any(row["canonical_document_id"] != record["canonical_document_id"] for row in block_rows):
        raise PipelineSchemaError("technical span raw blocks cross its canonical document")
    if [row["order"] for row in block_rows] != sorted(row["order"] for row in block_rows):
        raise PipelineSchemaError("technical span raw blocks are not in frozen source order")
    monolith_path = f"{indexes['legacy_root']}/A-New-Kind-of-Science.md"
    monolith_sha = indexes["input_by_path"][monolith_path]["sha256"]
    source_bytes = record["source_projection"].encode("utf-8")
    if sha256_bytes(source_bytes) != record["source_projection_sha256"]:
        raise PipelineSchemaError("technical source-projection hash mismatch")
    joined_source = _validate_raw_span(
        registry,
        source_path=monolith_path,
        source_sha256=monolith_sha,
        span=record["raw_span"],
        raw_block_ids=record["raw_block_ids"],
        expected_text=record["source_projection"],
    )
    if joined_source != source_bytes:
        raise PipelineSchemaError("technical source projection differs from exact raw span")
    output_span = record["output_span"]
    output_bytes = _validate_output_span(
        output_root=output_root,
        path=record["output_path"],
        span=output_span,
        field="technical output",
        expected_bytes=source_bytes,
    )
    if sha256_bytes(output_bytes) != record["source_projection_sha256"]:
        raise PipelineSchemaError("unchanged technical output bytes differ from source projection")
    ast_by_id = _validated_ast_nodes(registry, ast_nodes)
    _join_output_node_partition(
        node_ids=[record["node_id"]],
        ast_by_id=ast_by_id,
        output_root=output_root,
        output_path=record["output_path"],
        canonical_document_id=record["canonical_document_id"],
        target_span=output_span,
        raw_block_ids=record["raw_block_ids"],
    )
    tokens = record["tokens"]
    if not tokens:
        raise PipelineSchemaError("technical span lacks enumerated tokens")
    if [token["ordinal"] for token in tokens] != list(range(len(tokens))):
        raise PipelineSchemaError("technical token ordinals are not contiguous")
    token_ids = [token["token_id"] for token in tokens]
    if len(token_ids) != len(set(token_ids)):
        raise PipelineSchemaError("duplicate technical token ID")
    if "".join(token["raw_text"] for token in tokens) != record["source_projection"]:
        raise PipelineSchemaError("technical token stream does not exactly reconstruct source projection")
    derived_changed: list[str] = []
    for token in tokens:
        if token["raw_sha256"] != sha256_bytes(token["raw_text"].encode("utf-8")):
            raise PipelineSchemaError("technical token raw hash mismatch")
        if token["changed"]:
            derived_changed.append(token["token_id"])
            if token["repaired_text"] is None or token["repaired_text"] == token["raw_text"]:
                raise PipelineSchemaError("changed technical token lacks a distinct repaired value")
            if not token["evidence_ids"] or not token["review_ids"]:
                raise PipelineSchemaError("changed technical token lacks evidence/review joins")
        else:
            if token["repaired_text"] not in {None, token["raw_text"]}:
                raise PipelineSchemaError("unchanged technical token carries a changed repaired value")
            if token["evidence_ids"] or token["review_ids"]:
                raise PipelineSchemaError("unchanged technical token claims change evidence/reviews")
        if token["witness_text"] is not None:
            raise PipelineSchemaError("current SOURCE_BLOCKED gate forbids technical witness text")
    if record["changed_token_ids"] != derived_changed:
        raise PipelineSchemaError("changed-token summary differs from token rows")
    if derived_changed or record["repair_ids"]:
        raise PipelineSchemaError("current SOURCE_BLOCKED gate forbids repaired technical tokens")
    if not set(record["witness_region_ids"]).issubset(indexes["witness_region_ids"]):
        raise PipelineSchemaError("technical witness-region ID does not join Stage 3")
    if record["witness_region_ids"]:
        raise PipelineSchemaError("current SOURCE_BLOCKED technical span unexpectedly has witness regions")
    if record["witness_check"] not in {"SOURCE_BLOCKED", "NOT_APPLICABLE"}:
        raise PipelineSchemaError("technical witness check exceeds current Stage 3 evidence")
    unresolved_ids = set(indexes["open_unresolved_ids"])
    unresolved_ids.update(row["unresolved_id"] for row in unresolved_records)
    joined_unresolved = set(record["unresolved_ids"]) | set(record["workflow"]["unresolved_ids"])
    if not joined_unresolved.issubset(unresolved_ids):
        raise PipelineSchemaError("technical unresolved ID does not join federated ledger")
    if record["workflow"]["state"] == "SOURCE_BLOCKED" and not joined_unresolved:
        raise PipelineSchemaError("source-blocked technical span lacks a joined blocker")
    if record["parse_check"] == "FAIL_DIAGNOSTIC" or record["render_check"] == "FAIL_DIAGNOSTIC":
        if not joined_unresolved:
            raise PipelineSchemaError("failed technical diagnostic lacks unresolved disposition")
    if record["technical_kind"] == "WOLFRAM_PROGRAM" and record["program_count_classification"] == "NOT_APPLICABLE":
        raise PipelineSchemaError("Wolfram program lacks a program-count classification")
    if record["technical_kind"] != "WOLFRAM_PROGRAM" and record["program_count_classification"] == "COUNTED_PROGRAM":
        raise PipelineSchemaError("non-program technical span is counted as a Wolfram program")
    repair_ids = {row["repair_id"] for row in repair_records}
    if not set(record["repair_ids"]).issubset(repair_ids):
        raise PipelineSchemaError("technical repair ID does not join repair ledger")
    review_by_id = validate_review_set(review_records, registry)
    if not set(record["specialist_review_ids"]).issubset(review_by_id):
        raise PipelineSchemaError("technical specialist review ID does not join review ledger")
    for review_id in record["specialist_review_ids"]:
        review = review_by_id[review_id]
        if (
            review["reviewer_role"] != "SPECIALIST_REVIEWER"
            or review["specialty"] != "FORMULA_CODE_DATA"
            or review["subject_type"] != "TECHNICAL_SPAN"
            or review["subject_id"] != record["technical_span_id"]
            or review["closure_state"] != "CLOSED"
        ):
            raise PipelineSchemaError("technical specialist review row has wrong role/subject/state")
    if record["workflow"]["state"] == "CLOSED" and not record["specialist_review_ids"]:
        raise PipelineSchemaError("closed technical span lacks owning specialist review")


def validate_figure(record: Mapping[str, Any], registry: SchemaRegistry) -> None:
    registry.validate("goal-4/schemas/figure-record.schema.json", record)
    validate_workflow(record["workflow"])
    indexes = _frozen_indexes(registry)
    _validate_raw_block_ids(registry, record["raw_block_ids"])
    if record["canonical_document_id"] is not None and record["canonical_document_id"] not in indexes["documents_by_id"]:
        raise PipelineSchemaError("figure canonical document does not join guardrails")
    if not set(record["witness_region_ids"]).issubset(indexes["witness_region_ids"]):
        raise PipelineSchemaError("figure witness-region ID does not join Stage 3")
    if not (
        set(record["unresolved_ids"]) | set(record["workflow"]["unresolved_ids"])
    ).issubset(indexes["open_unresolved_ids"]):
        raise PipelineSchemaError("figure unresolved ID does not join Stage 3 blocker ledger")
    if record["asset_role"] == "GOVERNED_WITNESS_ASSET" or record["redistribution_allowed"] is True:
        raise PipelineSchemaError("current SOURCE_BLOCKED gate forbids witness asset release")
    if record["association_state"] == "VERIFIED" and not record["witness_region_ids"]:
        raise PipelineSchemaError("verified figure association lacks witness regions")
    if record["association_state"] == "VERIFIED":
        raise PipelineSchemaError("current SOURCE_BLOCKED gate forbids verified figure association")
    if record["record_type"] == "ASSET_CANDIDATE":
        required = (
            "asset_id",
            "manifest_file_id",
            "asset_role",
            "asset_sha256",
            "byte_size",
            "dimensions",
            "release_path",
        )
        if any(record[field] is None for field in required):
            raise PipelineSchemaError("asset candidate lacks concrete Stage 2 asset identity")
        manifest_row = indexes["input_by_id"].get(record["manifest_file_id"])
        if manifest_row is None or manifest_row.get("role") != "LEGACY_ASSET":
            raise PipelineSchemaError("figure asset does not join a Stage 2 legacy asset")
        expected_path = f"ASSETS/LEGACY/{manifest_row['relative_path']}"
        if (
            record["asset_role"] != "GOVERNED_LEGACY_ASSET"
            or record["asset_sha256"] != manifest_row["sha256"]
            or record["byte_size"] != manifest_row["byte_size"]
            or record["dimensions"]
            != {
                "height": manifest_row["image"]["height"],
                "width": manifest_row["image"]["width"],
            }
            or record["release_path"] != expected_path
        ):
            raise PipelineSchemaError("figure asset metadata differs from Stage 2 manifest")
        legacy_path = registry.repo_root / indexes["legacy_root"] / manifest_row["relative_path"]
        if legacy_path.stat().st_size != record["byte_size"] or sha256_file(legacy_path) != record["asset_sha256"]:
            raise PipelineSchemaError("figure asset file differs from frozen Stage 2 bytes")
        if record["ordered_component_asset_ids"]:
            raise PipelineSchemaError("asset candidate improperly owns ordered group components")
    else:
        for field in (
            "asset_id",
            "manifest_file_id",
            "asset_role",
            "asset_sha256",
            "byte_size",
            "dimensions",
            "release_path",
        ):
            if record[field] is not None:
                raise PipelineSchemaError("printed figure group carries single-asset fields")
        if record["figure_group_id"] is None:
            raise PipelineSchemaError("printed figure-group record lacks group ID")
    if record["workflow"]["state"] == "SOURCE_BLOCKED" and not (
        set(record["unresolved_ids"]) | set(record["workflow"]["unresolved_ids"])
    ):
        raise PipelineSchemaError("source-blocked figure record lacks a joined blocker")


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
    """Validate a compatibility evidence record without claiming oracle execution."""
    registry.validate("goal-4/schemas/compatibility-verification.schema.json", record)
    baseline_path = registry.repo_root / "goal-4/compatibility-baseline.json"
    if record["baseline_sha256"] != sha256_file(baseline_path):
        raise PipelineSchemaError("compatibility verification does not bind frozen baseline")
    baseline = load_json(baseline_path, require_cj1=True)
    if record["baseline_behavior_digest"] != baseline["behavior_digest"]:
        raise PipelineSchemaError("compatibility behavior baseline drift")
    expected_oracles = baseline["oracles"]
    rows = record["oracle_results"]
    if not rows or len(rows) != len(expected_oracles):
        raise PipelineSchemaError("compatibility result set is empty or incomplete")
    if [row["path"] for row in rows] != [row["path"] for row in expected_oracles]:
        raise PipelineSchemaError("compatibility result paths/order differ from frozen oracle scope")
    aggregate_rows: list[Mapping[str, Any]] = []
    for row, expected in zip(rows, expected_oracles):
        if row["argv"] != expected["argv"]:
            raise PipelineSchemaError("compatibility oracle argv differs from frozen invocation")
        if row["baseline_framed_behavior_sha256"] != expected["framed_behavior_sha256"]:
            raise PipelineSchemaError("compatibility row does not bind frozen oracle behavior")
        derived_identical = (
            row["current_framed_behavior_sha256"] == expected["framed_behavior_sha256"]
            and row["exit_code"] == expected["exit_code"]
            and row["stdout_sha256"] == expected["stdout"]["sha256"]
            and row["stderr_sha256"] == expected["stderr"]["sha256"]
            and row["status_kind"] == expected["status_kind"]
        )
        if row["identical"] != derived_identical:
            raise PipelineSchemaError("compatibility per-oracle identical flag is dishonest")
        aggregate_rows.append(
            {
                "exit_code": row["exit_code"],
                "framed_behavior_sha256": row["current_framed_behavior_sha256"],
                "path": row["path"],
                "status_kind": row["status_kind"],
                "stderr_sha256": row["stderr_sha256"],
                "stdout_sha256": row["stdout_sha256"],
            }
        )
    aggregate_projection = sorted(aggregate_rows, key=lambda row: row["path"])
    expected_aggregate = sha256_bytes(canonical_json_bytes(aggregate_projection))
    if record["aggregate_behavior_digest"] != expected_aggregate:
        raise PipelineSchemaError("compatibility aggregate behavior digest is not recomputable")
    if record["dependency_fingerprint"] != baseline["closure"]["dependency_fingerprint_after"]:
        raise PipelineSchemaError("compatibility dependency fingerprint drift")
    if record["legacy_tree_digest"] != baseline["closure"]["legacy_tree_digest_after"]:
        raise PipelineSchemaError("compatibility legacy-tree digest drift")
    if record["sentinel_fixture_results"] != {
        "duplicate_basename_detected": True,
        "nested_markdown_detected": True,
    }:
        raise PipelineSchemaError("compatibility sentinel fixtures did not prove recursive behavior")
    expected_all = all(row["identical"] for row in rows)
    if record["all_identical"] != expected_all:
        raise PipelineSchemaError("compatibility all_identical summary is dishonest")


def _require_canonical_utc(value: Any, field: str) -> None:
    if not isinstance(value, str) or re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", value
    ) is None:
        raise PipelineSchemaError(f"{field} is not canonical UTC seconds")


def _receipt_payload_sha256(receipt: Mapping[str, Any]) -> str:
    payload = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    return sha256_bytes(canonical_json_bytes(payload)[:-1])


def _validate_self_hashing_receipt(receipt: Mapping[str, Any], field: str) -> None:
    value = receipt.get("receipt_sha256")
    if not isinstance(value, str) or value == "0" * 64 or value != _receipt_payload_sha256(receipt):
        raise PipelineSchemaError(f"{field} receipt hash is absent, placeholder, or not recomputable")


def validate_compatibility_observation(
    record: Mapping[str, Any],
    receipt: Mapping[str, Any],
    registry: SchemaRegistry,
) -> None:
    """Join evidence to a separately supplied current oracle-execution receipt."""

    validate_compatibility(record, registry)
    _require_exact_keys(
        receipt,
        {
            "aggregate_behavior_digest",
            "compatibility_record_sha256",
            "contract_id",
            "dependency_fingerprint",
            "execution_environment_sha256",
            "legacy_tree_digest",
            "observation_id",
            "observed_at",
            "oracle_receipts",
            "receipt_sha256",
            "runner_principal_id",
            "runner_session_id",
            "schema_version",
            "sentinel_fixture_results_sha256",
        },
        "compatibility observation receipt",
    )
    if receipt["schema_version"] != "1.0.0" or receipt["contract_id"] != "ANKOS-COMPATIBILITY-OBSERVATION-1":
        raise PipelineSchemaError("wrong compatibility observation receipt identity")
    for field in ("observation_id", "runner_principal_id", "runner_session_id"):
        if not isinstance(receipt[field], str) or not receipt[field]:
            raise PipelineSchemaError(f"compatibility observation lacks {field}")
    _require_canonical_utc(receipt["observed_at"], "compatibility observation timestamp")
    if receipt["execution_environment_sha256"] == "0" * 64:
        raise PipelineSchemaError("compatibility observation uses a placeholder environment digest")
    if receipt["compatibility_record_sha256"] != sha256_bytes(canonical_json_bytes(record)):
        raise PipelineSchemaError("compatibility observation does not bind the exact evidence row")
    for field in ("aggregate_behavior_digest", "dependency_fingerprint", "legacy_tree_digest"):
        if receipt[field] != record[field]:
            raise PipelineSchemaError(f"compatibility observation differs from evidence: {field}")
    sentinel_sha = sha256_bytes(canonical_json_bytes(record["sentinel_fixture_results"])[:-1])
    if receipt["sentinel_fixture_results_sha256"] != sentinel_sha:
        raise PipelineSchemaError("compatibility observation sentinel receipt does not join evidence")
    rows = receipt["oracle_receipts"]
    if not isinstance(rows, list) or len(rows) != len(record["oracle_results"]):
        raise PipelineSchemaError("compatibility observation receipt scope is incomplete")
    expected_keys = {
        "argv",
        "exit_code",
        "finished_at",
        "framed_behavior_sha256",
        "oracle_result_sha256",
        "path",
        "receipt_sha256",
        "runner_command",
        "started_at",
        "status_kind",
        "stderr_sha256",
        "stdout_sha256",
    }
    for observed, evidence in zip(rows, record["oracle_results"]):
        _require_exact_keys(observed, expected_keys, "compatibility oracle execution receipt")
        _require_canonical_utc(observed["started_at"], "oracle start timestamp")
        _require_canonical_utc(observed["finished_at"], "oracle finish timestamp")
        if not isinstance(observed["runner_command"], list) or not observed["runner_command"] or any(
            not isinstance(part, str) or not part for part in observed["runner_command"]
        ):
            raise PipelineSchemaError("compatibility oracle receipt has no concrete runner command")
        expected = {
            "argv": evidence["argv"],
            "exit_code": evidence["exit_code"],
            "framed_behavior_sha256": evidence["current_framed_behavior_sha256"],
            "oracle_result_sha256": sha256_bytes(canonical_json_bytes(evidence)),
            "path": evidence["path"],
            "status_kind": evidence["status_kind"],
            "stderr_sha256": evidence["stderr_sha256"],
            "stdout_sha256": evidence["stdout_sha256"],
        }
        if any(observed[field] != value for field, value in expected.items()):
            raise PipelineSchemaError("compatibility oracle receipt differs from exact evidence row")
        _validate_self_hashing_receipt(observed, "compatibility oracle execution")
    _validate_self_hashing_receipt(receipt, "compatibility observation")


def validate_corpus_manifest(
    record: Mapping[str, Any],
    registry: SchemaRegistry,
    guardrails: Mapping[str, Any],
    *,
    output_root: Path | None = None,
    author_text_projections: Mapping[str, bytes] | None = None,
) -> None:
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
        elif item["canonical_order"] is not None or item["canonical_document_id"] is not None:
            raise PipelineSchemaError("noncanonical file claims canonical order/document identity")
        if item["author_text_projection_sha256"] is not None and re.fullmatch(
            r"[0-9a-f]{64}", item["author_text_projection_sha256"]
        ) is None:
            raise PipelineSchemaError("manifest file has malformed author projection digest")
    if counts != record["role_counts"]:
        raise PipelineSchemaError("manifest role counts do not match files")
    documents = guardrails["canonical_documents"]
    expected = [(item["order"], item["id"]) for item in documents]
    expected_by_id = {item["id"]: item for item in documents}
    if sorted(canonical) != expected or record["canonical_document_order"] != [item[1] for item in expected]:
        raise PipelineSchemaError("canonical document count/path order drift")
    canonical_files = [item for item in record["files"] if item["role"] == "CANONICAL_AUTHOR_TEXT"]
    for item in canonical_files:
        expected_document = expected_by_id[item["canonical_document_id"]]
        if (
            item["canonical_order"] != expected_document["order"]
            or item["path"] != expected_document["path"]
            or item["source_identity"] != expected_document["id"]
            or item["media_type"] != "text/markdown"
        ):
            raise PipelineSchemaError("canonical manifest path/role/identity differs from guardrails")
    expected_asset_counts = {
        "governed_legacy": counts.get("GOVERNED_LEGACY_ASSET", 0),
        "governed_witness": counts.get("GOVERNED_WITNESS_ASSET", 0),
    }
    if record["asset_counts"] != expected_asset_counts:
        raise PipelineSchemaError("manifest asset counts differ from file roles")
    if record["certification_state"] != "UNCERTIFIED":
        if output_root is None or author_text_projections is None:
            raise PipelineSchemaError("certified corpus validation lacks output root/projection evidence")
        output_root = output_root.resolve()
        if not output_root.is_dir() or output_root.is_symlink():
            raise PipelineSchemaError("certified corpus output root is absent, non-directory, or symlinked")
        observed: set[str] = set()
        for path in output_root.rglob("*"):
            relative = path.relative_to(output_root).as_posix()
            if path.is_symlink() or not path.is_file():
                if path.is_dir() and not path.is_symlink():
                    continue
                raise PipelineSchemaError(f"certified output has non-regular entry: {relative}")
            observed.add(relative)
        if observed != paths:
            raise PipelineSchemaError("certified output file set differs from its manifest")
        for item in record["files"]:
            path = output_root / item["path"]
            mode = f"{stat.S_IMODE(path.stat().st_mode):04o}"
            if (
                path.stat().st_size != item["byte_size"]
                or sha256_file(path) != item["sha256"]
                or mode != item["mode"]
            ):
                raise PipelineSchemaError(f"certified output file/hash/size/mode drift: {item['path']}")
        canonical_paths = [item["path"] for item in sorted(canonical_files, key=lambda row: row["canonical_order"])]
        if set(author_text_projections) != set(canonical_paths):
            raise PipelineSchemaError("certified projection evidence does not exactly cover canonical files")
        aggregate = bytearray()
        file_by_path = {item["path"]: item for item in canonical_files}
        for path in canonical_paths:
            projection = author_text_projections[path]
            if not isinstance(projection, bytes):
                raise PipelineSchemaError("certified author projection is not bytes")
            if sha256_bytes(projection) != file_by_path[path]["author_text_projection_sha256"]:
                raise PipelineSchemaError("certified per-file author projection digest mismatch")
            aggregate.extend(projection)
        if sha256_bytes(bytes(aggregate)) != record["author_text_projection_sha256"]:
            raise PipelineSchemaError("certified aggregate author projection digest mismatch")
        raise PipelineSchemaError("current SOURCE_BLOCKED gate forbids certified corpus")


def _validate_artifact_map(
    values: Mapping[str, str],
    registry: SchemaRegistry,
    label: str,
    *,
    empty_allowed: bool,
) -> None:
    if not values and not empty_allowed:
        raise PipelineSchemaError(f"release {label} artifact map is empty")
    for relative, expected_sha in values.items():
        _safe_repo_path(relative, f"release {label} artifact")
        if expected_sha == "0" * 64:
            raise PipelineSchemaError(f"release {label} uses an all-zero placeholder digest")
        if sha256_file(registry.repo_root / relative) != expected_sha:
            raise PipelineSchemaError(f"release {label} does not join a concrete artifact: {relative}")


def _artifact_with_digest(
    maps: Sequence[Mapping[str, str]], digest: str, registry: SchemaRegistry, label: str
) -> Path:
    matches = [relative for values in maps for relative, value in values.items() if value == digest]
    if len(matches) != 1:
        raise PipelineSchemaError(f"release {label} digest does not identify exactly one concrete artifact")
    path = registry.repo_root / matches[0]
    if sha256_file(path) != digest:
        raise PipelineSchemaError(f"release {label} concrete artifact hash drift")
    return path


def _validate_release_ledgers(
    registry: SchemaRegistry,
    contract: Mapping[str, Any],
    *,
    output_root: Path | None,
    ast_nodes: Sequence[Mapping[str, Any]],
) -> None:
    """Parse every registered ledger and run its semantic/cross-ledger validator."""

    by_path: dict[str, list[Mapping[str, Any]]] = {}
    for registration in contract["ledgers"]:
        rows = load_jsonl(registry.repo_root / registration["path"], require_cj1=True)
        if not rows and not registration["empty_allowed"]:
            raise PipelineSchemaError(f"registered ledger is empty but empty_allowed is false: {registration['path']}")
        for row in rows:
            if not isinstance(row, dict):
                raise PipelineSchemaError(f"registered ledger contains a non-object row: {registration['path']}")
            registry.validate(registration["schema"], row)
        by_path[registration["path"]] = rows

    reviews = by_path["goal-4/review-ledger.jsonl"]
    unresolved = by_path["goal-4/unresolved-ledger.jsonl"]
    repairs = by_path["goal-4/repair-ledger.jsonl"]
    provenance = by_path["goal-4/provenance-map.jsonl"]
    technical = by_path["goal-4/formula-code-ledger.jsonl"]
    figures = by_path["goal-4/figure-caption-asset-ledger.jsonl"]
    navigation = by_path["goal-4/navigation-ledger.jsonl"]
    validate_review_set(reviews, registry)
    unresolved_ids: set[str] = set()
    for row in unresolved:
        validate_unresolved(row, registry)
        if row["unresolved_id"] in unresolved_ids:
            raise PipelineSchemaError("duplicate unresolved-ledger ID")
        unresolved_ids.add(row["unresolved_id"])
    validate_repair_set(repairs, registry, reviews, unresolved)
    for row in figures:
        validate_figure(row, registry)
    validate_provenance_set(
        provenance,
        registry,
        repairs,
        require_complete_raw_coverage=True,
        output_root=output_root,
        ast_nodes=ast_nodes,
    )
    for row in technical:
        validate_technical(
            row,
            registry,
            repairs,
            reviews,
            unresolved,
            output_root=output_root,
            ast_nodes=ast_nodes,
        )
    validate_navigation_set(
        navigation,
        registry,
        ast_nodes=ast_nodes,
        figure_records=figures,
    )


def _load_receipt(
    maps: Sequence[Mapping[str, str]], digest: str, registry: SchemaRegistry, label: str
) -> Mapping[str, Any]:
    path = _artifact_with_digest(maps, digest, registry, label)
    receipt = load_json(path, require_cj1=True)
    if not isinstance(receipt, dict):
        raise PipelineSchemaError(f"release {label} artifact is not an object receipt")
    return receipt


def _validate_inverse_replay_receipt(
    receipt: Mapping[str, Any], release: Mapping[str, Any], monolith_sha256: str
) -> None:
    keys = {
        "command", "contract_id", "execution_environment_sha256", "exit_code",
        "finished_at", "input_state_sha256", "operation_batch_sha256", "receipt_chain_sha256",
        "receipt_id", "receipt_sha256", "release_id", "schema_version", "started_at",
        "status_kind", "stderr_sha256", "stdout_sha256", "output_raw_projection_sha256",
    }
    _require_exact_keys(receipt, keys, "inverse replay receipt")
    if receipt["schema_version"] != "1.0.0" or receipt["contract_id"] != "ANKOS-INVERSE-REPLAY-RECEIPT-1":
        raise PipelineSchemaError("wrong inverse replay receipt identity")
    if receipt["release_id"] != release["release_id"] or receipt["output_raw_projection_sha256"] != monolith_sha256:
        raise PipelineSchemaError("inverse replay receipt does not recover the release's frozen monolith")
    if receipt["status_kind"] != "EXITED" or receipt["exit_code"] != 0:
        raise PipelineSchemaError("inverse replay receipt is not a successful observed execution")
    if not receipt["command"] or any(not isinstance(part, str) or not part for part in receipt["command"]):
        raise PipelineSchemaError("inverse replay receipt lacks a concrete command")
    for field in ("started_at", "finished_at"):
        _require_canonical_utc(receipt[field], f"inverse replay {field}")
    for field in ("execution_environment_sha256", "input_state_sha256", "operation_batch_sha256", "receipt_chain_sha256"):
        if receipt[field] == "0" * 64:
            raise PipelineSchemaError(f"inverse replay receipt has placeholder {field}")
    _validate_self_hashing_receipt(receipt, "inverse replay")


def _validate_reproducibility_receipt(
    receipt: Mapping[str, Any], release: Mapping[str, Any]
) -> None:
    _require_exact_keys(
        receipt,
        {"build_receipts", "contract_id", "receipt_id", "receipt_sha256", "release_id", "schema_version"},
        "reproducibility receipt",
    )
    if receipt["schema_version"] != "1.0.0" or receipt["contract_id"] != "ANKOS-REPRODUCIBILITY-RECEIPT-1" or receipt["release_id"] != release["release_id"]:
        raise PipelineSchemaError("wrong reproducibility receipt identity")
    builds = receipt["build_receipts"]
    if not isinstance(builds, list) or len(builds) != 2:
        raise PipelineSchemaError("reproducibility receipt does not contain exactly two builds")
    build_keys = {
        "build_id", "command", "execution_environment_sha256", "exit_code", "finished_at",
        "output_manifest_sha256", "output_tree_sha256", "receipt_sha256", "started_at",
        "status_kind", "stderr_sha256", "stdout_sha256",
    }
    for index, build in enumerate(builds):
        _require_exact_keys(build, build_keys, "clean-build execution receipt")
        if build["status_kind"] != "EXITED" or build["exit_code"] != 0:
            raise PipelineSchemaError("clean-build receipt is not a successful observed execution")
        if build["command"] not in release["commands"]:
            raise PipelineSchemaError("clean-build receipt command is absent from release commands")
        if build["output_manifest_sha256"] != release["output_manifest_sha256"] or build["output_tree_sha256"] != release["two_clean_build_digests"][index]:
            raise PipelineSchemaError("clean-build receipt does not join release output digests")
        if build["execution_environment_sha256"] == "0" * 64:
            raise PipelineSchemaError("clean-build receipt has a placeholder environment digest")
        _require_canonical_utc(build["started_at"], "clean-build start timestamp")
        _require_canonical_utc(build["finished_at"], "clean-build finish timestamp")
        _validate_self_hashing_receipt(build, "clean-build execution")
    if builds[0]["output_tree_sha256"] != builds[1]["output_tree_sha256"]:
        raise PipelineSchemaError("two independently receipted clean builds differ")
    _validate_self_hashing_receipt(receipt, "reproducibility")


def _validate_rollback_receipt(
    receipt: Mapping[str, Any], release: Mapping[str, Any]
) -> None:
    keys = {
        "command", "contract_id", "exit_code", "finished_at", "receipt_id", "receipt_sha256",
        "release_id", "schema_version", "started_at", "status", "stderr_sha256", "stdout_sha256",
    }
    _require_exact_keys(receipt, keys, "rollback receipt")
    if receipt["schema_version"] != "1.0.0" or receipt["contract_id"] != "ANKOS-ROLLBACK-RECEIPT-1" or receipt["release_id"] != release["release_id"]:
        raise PipelineSchemaError("wrong rollback receipt identity")
    not_published = release["publication"]["target_state"] == "NOT_PUBLISHED"
    if not_published:
        if receipt["status"] != "NOT_APPLICABLE_NOT_PUBLISHED" or receipt["command"] or any(
            receipt[field] is not None for field in ("exit_code", "started_at", "finished_at", "stdout_sha256", "stderr_sha256")
        ):
            raise PipelineSchemaError("not-published rollback receipt is contradictory")
    else:
        if receipt["status"] != "VERIFIED" or receipt["command"] != release["rollback"]["command"] or receipt["exit_code"] != 0:
            raise PipelineSchemaError("published rollback lacks a successful exact command receipt")
        _require_canonical_utc(receipt["started_at"], "rollback start timestamp")
        _require_canonical_utc(receipt["finished_at"], "rollback finish timestamp")
    _validate_self_hashing_receipt(receipt, "rollback")


def validate_release_manifest(
    record: Mapping[str, Any],
    registry: SchemaRegistry,
    *,
    output_root: Path | None = None,
    author_text_projections: Mapping[str, bytes] | None = None,
    ast_nodes: Sequence[Mapping[str, Any]] = (),
) -> None:
    registry.validate("goal-4/schemas/release-manifest.schema.json", record)
    scalar_digests = (
        record["compatibility_observation_receipt_sha256"],
        record["compatibility_verification_sha256"],
        record["reproducibility_receipt_sha256"],
        record["output_manifest_sha256"],
        record["schema_lock_sha256"],
        record["inverse_replay"]["receipt_sha256"],
        record["inverse_replay"]["raw_projection_sha256"],
        record["rollback"]["receipt_sha256"],
        *record["two_clean_build_digests"],
    )
    if any(value == "0" * 64 for value in scalar_digests):
        raise PipelineSchemaError("release manifest uses an all-zero placeholder digest")
    if record["certification_state"] != "UNCERTIFIED" or record["audit_certificate"] is not None:
        raise PipelineSchemaError("current SOURCE_BLOCKED gate forbids audit certification")
    if record["claim_scope"] == "FULL_REPAIR_CERTIFIED":
        raise PipelineSchemaError("current SOURCE_BLOCKED gate forbids full-repair claim")
    if set(record["open_blocker_ids"]) != _frozen_indexes(registry)["open_unresolved_ids"]:
        raise PipelineSchemaError("uncertified release does not enumerate every Stage 3 blocker")
    publication = record["publication"]
    rollback = record["rollback"]
    if publication["target_state"] == "NOT_PUBLISHED":
        if (
            publication["atomic_same_filesystem_rename"] is not False
            or rollback["command"] != []
            or record["prior_release"] is not None
        ):
            raise PipelineSchemaError("NOT_PUBLISHED release has incomplete/contradictory publication state")
    elif (
        publication["atomic_same_filesystem_rename"] is not True
        or not rollback["command"]
    ):
        raise PipelineSchemaError("published release lacks atomic promotion and verified rollback")
    contract_paths = {
        "goal-4/baseline-lock.json",
        "goal-4/guardrails.json",
        "goal-4/licensing-contract.json",
        "goal-4/pipeline-contract.json",
        "goal-4/promotion-contract.md",
        "goal-4/review-contract.md",
        "goal-4/style-guide.md",
        "goal-4/witness-lock.json",
        "goal-4/zero-repair-contract.json",
    }
    if set(record["contract_bindings"]) != contract_paths:
        raise PipelineSchemaError("release contract bindings are not the exact frozen contract set")
    required_inputs = {
        "goal-4/corpus-manifest.json",
        "goal-4/structure-ledger.jsonl",
        "ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md",
    }
    if not required_inputs.issubset(record["input_bindings"]):
        raise PipelineSchemaError("release input bindings omit frozen Stage 2 source identities")
    required_tools = {
        "goal-4/tools/build_zero_repair.py",
        "goal-4/tools/overlay_lib.py",
        "goal-4/tools/zero_repair_lib.py",
    }
    if not required_tools.issubset(record["tool_hashes"]):
        raise PipelineSchemaError("release tool hashes omit required build/overlay implementations")
    contract = load_json(registry.repo_root / PIPELINE_CONTRACT_PATH, require_cj1=True)
    expected_ledgers = {row["path"] for row in contract["ledgers"]}
    if set(record["ledger_hashes"]) != expected_ledgers:
        raise PipelineSchemaError("release ledger hashes do not cover the exact registered ledger set")
    for label, values, empty_allowed in (
        ("contract", record["contract_bindings"], False),
        ("input", record["input_bindings"], False),
        ("overlay", record["overlay_hashes"], record["claim_scope"] == "ZERO_REPAIR_STRUCTURAL_BUILD"),
        ("tool", record["tool_hashes"], False),
        ("ledger", record["ledger_hashes"], False),
    ):
        _validate_artifact_map(values, registry, label, empty_allowed=empty_allowed)
    if record["schema_lock_sha256"] != sha256_file(registry.repo_root / PIPELINE_LOCK_PATH):
        raise PipelineSchemaError("release schema-lock digest does not join the package lock")
    artifact_maps = (
        record["contract_bindings"],
        record["input_bindings"],
        record["overlay_hashes"],
        record["tool_hashes"],
        record["ledger_hashes"],
    )
    compatibility_path = _artifact_with_digest(
        artifact_maps,
        record["compatibility_verification_sha256"],
        registry,
        "compatibility verification",
    )
    compatibility = load_json(compatibility_path, require_cj1=True)
    validate_compatibility(compatibility, registry)
    if compatibility["all_identical"] is not True:
        raise PipelineSchemaError("release compatibility verification is not fully identical")
    observation = _load_receipt(
        artifact_maps,
        record["compatibility_observation_receipt_sha256"],
        registry,
        "compatibility observation",
    )
    validate_compatibility_observation(compatibility, observation, registry)
    _validate_release_ledgers(
        registry,
        contract,
        output_root=output_root,
        ast_nodes=ast_nodes,
    )
    corpus_path = _artifact_with_digest(
        artifact_maps, record["output_manifest_sha256"], registry, "output manifest"
    )
    corpus_manifest = load_json(corpus_path, require_cj1=True)
    guardrails = load_json(registry.repo_root / "goal-4/guardrails.json", require_cj1=False)
    validate_corpus_manifest(
        corpus_manifest,
        registry,
        guardrails,
        output_root=output_root,
        author_text_projections=author_text_projections,
    )
    if corpus_manifest["release_id"] != record["release_id"]:
        raise PipelineSchemaError("release/output-manifest release IDs do not join")
    if corpus_manifest["role_counts"] != record["role_counts"]:
        raise PipelineSchemaError("release role counts do not join output manifest")
    monolith = _frozen_indexes(registry)["input_by_path"][
        "ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md"
    ]
    if record["inverse_replay"]["raw_projection_sha256"] != monolith["sha256"]:
        raise PipelineSchemaError("release inverse replay does not recover the frozen monolith")
    if not record["commands"] or any(
        not command or any(not isinstance(part, str) or not part for part in command)
        for command in record["commands"]
    ):
        raise PipelineSchemaError("release reproduction command list is empty/malformed")
    if len(set(record["two_clean_build_digests"])) != 1:
        raise PipelineSchemaError("two clean builds are not byte-identical")
    inverse_receipt = _load_receipt(
        artifact_maps, record["inverse_replay"]["receipt_sha256"], registry, "inverse replay"
    )
    _validate_inverse_replay_receipt(inverse_receipt, record, monolith["sha256"])
    reproducibility_receipt = _load_receipt(
        artifact_maps,
        record["reproducibility_receipt_sha256"],
        registry,
        "reproducibility",
    )
    _validate_reproducibility_receipt(reproducibility_receipt, record)
    rollback_receipt = _load_receipt(
        artifact_maps, record["rollback"]["receipt_sha256"], registry, "rollback"
    )
    _validate_rollback_receipt(rollback_receipt, record)


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
