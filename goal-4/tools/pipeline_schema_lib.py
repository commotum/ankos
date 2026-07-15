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
from pathlib import Path, PurePosixPath
import re
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


def load_json(path: Path, *, require_cj1: bool) -> Any:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise PipelineSchemaError(f"UTF-8 BOM is forbidden: {path}")
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PipelineSchemaError(f"invalid UTF-8 JSON at {path}: {exc}") from exc
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
        try:
            row = json.loads(line.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise PipelineSchemaError(f"invalid JSONL row {index} at {path}: {exc}") from exc
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
            choices = schema.get(key, [])
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
    if CLASS_ROLES[record["repair_class"]] != record["target"]["role"]:
        raise PipelineSchemaError("repair class crossed its frozen target role")
    derived_high_risk = (
        record["repair_class"] in HIGH_RISK_CLASSES
        or bool(set(record["risk"]["operation_tags"]) & HIGH_RISK_OPERATION_TAGS)
        or bool(set(record["risk"]["ast_impact_tags"]) & HIGH_RISK_AST_TAGS)
    )
    if record["risk"]["high_risk"] != derived_high_risk:
        raise PipelineSchemaError("high-risk union is misclassified")
    guard = record["guard"]
    if guard["guard_kind"] == "PREIMAGE":
        if sha256_bytes(guard["preimage"].encode("utf-8")) != guard["preimage_sha256"]:
            raise PipelineSchemaError("preimage hash mismatch")
    else:
        for side in ("left_anchor", "right_anchor"):
            anchor = guard[side]
            if sha256_bytes(anchor["text"].encode("utf-8")) != anchor["sha256"]:
                raise PipelineSchemaError(f"{side} hash mismatch")
            if anchor["end_byte_exclusive"] <= anchor["start_byte"]:
                raise PipelineSchemaError(f"{side} has an empty/reversed span")
        if guard["left_anchor"]["end_byte_exclusive"] != guard["right_anchor"]["start_byte"]:
            raise PipelineSchemaError("two-sided anchors are not adjacent")
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
    actual_witness_regions: set[str] = set()
    for row in load_jsonl(registry.repo_root / "goal-4/witness-region-ledger.jsonl", require_cj1=True):
        actual_witness_regions.update(row.get("witness_region_ids", []))
    for evidence in record["evidence"]["authoritative"]:
        if evidence["evidence_kind"] != "AUTHORITATIVE_WITNESS_REGION":
            raise PipelineSchemaError("authoritative evidence array contains a non-authoritative kind")
        if not evidence["witness_region_ids"] or not set(evidence["witness_region_ids"]).issubset(actual_witness_regions):
            raise PipelineSchemaError("authoritative evidence does not join to Stage 3 witness regions")
        if evidence["permission_record_id"] is None:
            raise PipelineSchemaError("authoritative evidence lacks a permission record")


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
    review_ids = {record["review_id"] for record in review_records}
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
    if len(applied_orders) != len(set(applied_orders)):
        raise PipelineSchemaError("duplicate repair application order")


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
    if record["reviewer_type"] == "HUMAN" and record["reviewed_at"] is None:
        raise PipelineSchemaError("human review lacks audit timestamp")
    if record["agreement_state"] in {"DISAGREES", "PENDING_ADJUDICATION"} and record["closure_state"] == "CLOSED":
        raise PipelineSchemaError("unresolved disagreement is closed")
    if record["blind_preproposal"] and record["proposal_visible"]:
        raise PipelineSchemaError("blind pre-proposal reviewer saw proposal")


def validate_unresolved(record: Mapping[str, Any], registry: SchemaRegistry) -> None:
    registry.validate("goal-4/schemas/unresolved-record.schema.json", record)
    if record["workflow_state"] == "SOURCE_BLOCKED" and record["repair_authorized"]:
        raise PipelineSchemaError("source-blocked item authorizes repair")
    if record["resolution"] is None and not record["release_blocker_codes"] and record["severity_id"] != "S4_OPTIONAL_EDITORIAL_ENHANCEMENT":
        raise PipelineSchemaError("open nonoptional item lacks release blocker code")


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
