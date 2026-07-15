"""Deterministic, fail-closed repair overlays for Goal 4.

This module deliberately operates on a small byte-block model.  It is the
executable core used to prove operation guards, role separation, dependency
ordering, and reversibility before any corpus repair is attempted.  It does
not read the legacy tree, a witness mount, or a generated output tree.

The public operations are immutable records.  Every record binds a specific
document target, the complete target pre-state and post-state hashes, and
operation-specific preimages/counts/hashes.  Canonical author-text changes
are accepted only with edition-identical witness-region evidence, independent
approved source and specialist reviews, and an application authority sealed
by the higher-level registry validator.  With no authority the canonical gate
is SOURCE_BLOCKED.  Raw byte partitioning belongs to the projection-tape
compiler, not to this semantic overlay engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass, replace
import hashlib
import re
from typing import Iterable, Mapping, Sequence, TypeAlias


CANONICAL_AUTHOR_TEXT = "CANONICAL_AUTHOR_TEXT"
DERIVED_AGGREGATE = "DERIVED_AGGREGATE"
GENERATED_METADATA = "GENERATED_METADATA"
EDITORIAL_SIDECAR = "EDITORIAL_SIDECAR"
SEARCH_DERIVATIVE = "SEARCH_DERIVATIVE"

TARGET_ROLES = frozenset(
    {
        CANONICAL_AUTHOR_TEXT,
        DERIVED_AGGREGATE,
        GENERATED_METADATA,
        EDITORIAL_SIDECAR,
        SEARCH_DERIVATIVE,
    }
)

STRUCTURE_BOUNDARY = "STRUCTURE_BOUNDARY"
MARKDOWN_STRUCTURE = "MARKDOWN_STRUCTURE"
PROSE_OCR = "PROSE_OCR"
HEADING_OR_FURNITURE = "HEADING_OR_FURNITURE"
FORMULA_OR_SYMBOL = "FORMULA_OR_SYMBOL"
WOLFRAM_CODE = "WOLFRAM_CODE"
RULE_TABLE_OR_DATA = "RULE_TABLE_OR_DATA"
FIGURE_OR_CAPTION = "FIGURE_OR_CAPTION"
INDEX_ENTRY = "INDEX_ENTRY"
NAVIGATION_METADATA = "NAVIGATION_METADATA"
SOURCE_ERRATUM_ANNOTATION = "SOURCE_ERRATUM_ANNOTATION"
SEARCH_NORMALIZATION = "SEARCH_NORMALIZATION"

CANONICAL_CLASSES = frozenset(
    {
        STRUCTURE_BOUNDARY,
        MARKDOWN_STRUCTURE,
        PROSE_OCR,
        HEADING_OR_FURNITURE,
        FORMULA_OR_SYMBOL,
        WOLFRAM_CODE,
        RULE_TABLE_OR_DATA,
        FIGURE_OR_CAPTION,
        INDEX_ENTRY,
    }
)

CLASS_ALLOWED_ROLES = {
    **{repair_class: frozenset({CANONICAL_AUTHOR_TEXT}) for repair_class in CANONICAL_CLASSES},
    NAVIGATION_METADATA: frozenset({GENERATED_METADATA}),
    SOURCE_ERRATUM_ANNOTATION: frozenset({EDITORIAL_SIDECAR}),
    SEARCH_NORMALIZATION: frozenset({SEARCH_DERIVATIVE}),
}

HIGH_RISK_CLASSES = frozenset(
    {
        STRUCTURE_BOUNDARY,
        MARKDOWN_STRUCTURE,
        HEADING_OR_FURNITURE,
        FORMULA_OR_SYMBOL,
        WOLFRAM_CODE,
        RULE_TABLE_OR_DATA,
        FIGURE_OR_CAPTION,
        INDEX_ENTRY,
    }
)

WORKFLOW_STATES = frozenset(
    {
        "CAPTURED",
        "EVIDENCE_READY",
        "PENDING_SPECIALIST_REVIEW",
        "PENDING_INDEPENDENT_REVIEW",
        "SOURCE_BLOCKED",
        "CLOSED",
    }
)

FINAL_DISPOSITIONS = frozenset(
    {
        "APPLIED_MECHANICALLY_PROVEN",
        "APPLIED_WITNESS_VERIFIED",
        "ANNOTATED_SOURCE_ERRATUM",
        "REJECTED_VALID_SOURCE_TEXT",
        "DUPLICATE_CANDIDATE",
        "UNRESOLVED_SOURCE_NEEDED",
    }
)

PRINCIPAL_TYPES = frozenset({"HUMAN", "AGENT", "AUTOMATED"})
ID_RE = re.compile(r"[A-Z0-9]+(?:[_-][A-Z0-9]+)*\Z")
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
AUTHORITY_GATE_STATES = frozenset({"SOURCE_BLOCKED", "OPEN"})

# These seals prevent accidental/direct construction and dataclasses.replace
# fabrication at the API boundary.  They are process-local object identities,
# not cryptographic secrets; the accompanying digests provide deterministic
# integrity, not external authenticity.  The trust root remains the validator
# which creates an ApplicationAuthority from its pinned registry.
_AUTHORITY_SEAL = object()
_REPLAY_SEAL = object()


class OverlayError(ValueError):
    """Base class for a refused overlay or inverse replay."""


class SchemaError(OverlayError):
    """An operation record or state has an invalid closed-schema value."""


class GuardError(OverlayError):
    """An exact preimage, count, adjacency, or hash guard failed."""


class RoleError(OverlayError):
    """An operation class attempted to cross target-role boundaries."""


class EvidenceError(OverlayError):
    """A canonical author-text change lacks sufficient source review."""


class DependencyError(OverlayError):
    """Overlay dependencies are missing, duplicated, or out of order."""


class InverseError(OverlayError):
    """The forward result no longer matches the guarded inverse preimage."""


ByteLike: TypeAlias = bytes | str


def _bytes(value: ByteLike, field: str) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    raise SchemaError(f"{field} must be bytes or UTF-8 text")


def sha256_bytes(value: ByteLike) -> str:
    """Return the lowercase SHA-256 digest of bytes or UTF-8 text."""

    return hashlib.sha256(_bytes(value, "value")).hexdigest()


def _require_id(value: str, field: str) -> None:
    if not isinstance(value, str) or ID_RE.fullmatch(value) is None:
        raise SchemaError(f"{field} is not a closed-profile ID: {value!r}")


def _require_sha256(value: str, field: str) -> None:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        raise SchemaError(f"{field} is not a lowercase SHA-256 digest")


def _require_nonempty_text(value: str, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise SchemaError(f"{field} must be nonempty text")


def _require_positive_int(value: int, field: str) -> None:
    if type(value) is not int or value < 1:
        raise SchemaError(f"{field} must be a positive integer")


def _require_exact_one(value: int, field: str) -> None:
    if type(value) is not int or value != 1:
        raise SchemaError(f"{field} must be the integer 1")


def _feed_length_prefixed(digest: "hashlib._Hash", value: bytes) -> None:
    digest.update(len(value).to_bytes(8, "big"))
    digest.update(value)


@dataclass(frozen=True, slots=True)
class Block:
    """One uniquely identified synthetic byte/text block."""

    block_id: str
    data: ByteLike

    def __post_init__(self) -> None:
        _require_id(self.block_id, "block_id")
        object.__setattr__(self, "data", _bytes(self.data, "block data"))

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.data).hexdigest()

    def text(self) -> str:
        return self.data.decode("utf-8")


def target_sha256(target_id: str, role: str, blocks: Sequence[Block]) -> str:
    """Hash one complete document/role target with IDs, order, and bytes."""

    _require_id(target_id, "target_id")
    if role not in TARGET_ROLES:
        raise SchemaError(f"unknown target role: {role!r}")
    digest = hashlib.sha256()
    _feed_length_prefixed(digest, b"ANKOS-OVERLAY-TARGET-2")
    _feed_length_prefixed(digest, target_id.encode("ascii"))
    _feed_length_prefixed(digest, role.encode("ascii"))
    digest.update(len(blocks).to_bytes(8, "big"))
    seen: set[str] = set()
    for block in blocks:
        if not isinstance(block, Block):
            raise SchemaError("target contains a non-Block value")
        if block.block_id in seen:
            raise SchemaError(f"duplicate block ID in {role}: {block.block_id}")
        seen.add(block.block_id)
        _feed_length_prefixed(digest, block.block_id.encode("ascii"))
        _feed_length_prefixed(digest, block.data)
    return digest.hexdigest()


@dataclass(frozen=True, slots=True)
class OverlayState:
    """Immutable document/role state with deterministic ordering and hashing.

    Direct construction defensively tuple-normalizes every container, so a
    caller retaining a mutable input list cannot mutate the frozen state.
    """

    _targets: tuple[tuple[str, str, tuple[Block, ...]], ...]

    def __post_init__(self) -> None:
        try:
            raw_targets = tuple(self._targets)
        except TypeError as error:
            raise SchemaError("state targets must be iterable") from error
        closed: list[tuple[str, str, tuple[Block, ...]]] = []
        for raw in raw_targets:
            if not isinstance(raw, (tuple, list)) or len(raw) != 3:
                raise SchemaError("each state target must be (target_id, role, blocks)")
            target_id, role, raw_blocks = raw
            try:
                blocks = tuple(raw_blocks)
            except TypeError as error:
                raise SchemaError("state target blocks must be iterable") from error
            _require_id(target_id, "target_id")
            target_sha256(target_id, role, blocks)
            closed.append((target_id, role, blocks))
        keys = [(target_id, role) for target_id, role, _ in closed]
        if keys != sorted(keys):
            raise SchemaError("state targets must be sorted by target ID and role")
        if len(keys) != len(set(keys)):
            raise SchemaError("state contains duplicate document/role targets")
        object.__setattr__(self, "_targets", tuple(closed))

    @classmethod
    def from_mapping(
        cls, targets: Mapping[tuple[str, str], Iterable[Block]]
    ) -> "OverlayState":
        if not isinstance(targets, Mapping):
            raise SchemaError("targets must be a mapping")
        closed_rows: list[tuple[str, str, tuple[Block, ...]]] = []
        for key, blocks in targets.items():
            if type(key) is not tuple or len(key) != 2:
                raise SchemaError("state mapping keys must be (target_id, role) tuples")
            target_id, role = key
            closed_rows.append((target_id, role, tuple(blocks)))
        closed = tuple(sorted(closed_rows))
        return cls(closed)

    @property
    def roles(self) -> tuple[str, ...]:
        return tuple(sorted({role for _, role, _ in self._targets}))

    @property
    def target_keys(self) -> tuple[tuple[str, str], ...]:
        return tuple((target_id, role) for target_id, role, _ in self._targets)

    def _resolve_target_id(self, role: str, target_id: str | None) -> str:
        if target_id is not None:
            _require_id(target_id, "target_id")
            return target_id
        candidates = [candidate for candidate, candidate_role, _ in self._targets if candidate_role == role]
        if len(candidates) != 1:
            raise RoleError(
                f"target_id is required for role {role}; found {len(candidates)} document targets"
            )
        return candidates[0]

    def blocks(self, role: str, target_id: str | None = None) -> tuple[Block, ...]:
        resolved = self._resolve_target_id(role, target_id)
        for candidate, candidate_role, blocks in self._targets:
            if candidate == resolved and candidate_role == role:
                return blocks
        raise RoleError(f"document/role target is absent from state: {resolved}/{role}")

    def target_sha256(self, role: str, target_id: str | None = None) -> str:
        resolved = self._resolve_target_id(role, target_id)
        return target_sha256(resolved, role, self.blocks(role, resolved))

    def with_blocks(
        self, role: str, blocks: Iterable[Block], target_id: str | None = None
    ) -> "OverlayState":
        resolved = self._resolve_target_id(role, target_id)
        if (resolved, role) not in self.target_keys:
            raise RoleError(f"document/role target is absent from state: {resolved}/{role}")
        replacement = tuple(blocks)
        target_sha256(resolved, role, replacement)
        return OverlayState.from_mapping(
            {
                (candidate, candidate_role): (
                    replacement
                    if candidate == resolved and candidate_role == role
                    else existing
                )
                for candidate, candidate_role, existing in self._targets
            }
        )

    @property
    def sha256(self) -> str:
        digest = hashlib.sha256()
        _feed_length_prefixed(digest, b"ANKOS-OVERLAY-STATE-2")
        digest.update(len(self._targets).to_bytes(8, "big"))
        for target_id, role, blocks in self._targets:
            _feed_length_prefixed(digest, target_id.encode("ascii"))
            _feed_length_prefixed(digest, role.encode("ascii"))
            _feed_length_prefixed(
                digest, target_sha256(target_id, role, blocks).encode("ascii")
            )
        return digest.hexdigest()


@dataclass(frozen=True, slots=True)
class WitnessEvidence:
    """Pinned identity for one authorized edition-identical witness region."""

    witness_id: str
    edition_id: str
    region_id: str
    region_sha256: str
    evidence_view_sha256: str
    authorized: bool
    edition_identical: bool
    legible_for_change: bool


@dataclass(frozen=True, slots=True)
class IndependentReview:
    """Independent source review, with optional high-risk specialist review."""

    review_id: str
    creator_principal_id: str
    source_reviewer_principal_id: str
    source_reviewer_type: str
    source_reviewer_session_id: str
    source_reviewer_role: str
    source_decision: str
    evidence_view_sha256: str
    blind_preproposal: bool
    specialist_review_id: str | None = None
    specialist_principal_id: str | None = None
    specialist_type: str | None = None
    specialist_session_id: str | None = None
    specialist_decision: str | None = None
    specialist_evidence_view_sha256: str | None = None


@dataclass(frozen=True, slots=True)
class OperationMeta:
    """Closed common metadata and complete target hash guards."""

    repair_id: str
    target_id: str
    target_role: str
    repair_class: str
    expected_target_sha256: str
    expected_result_sha256: str
    creator_principal_id: str
    workflow_state: str
    final_disposition: str
    dependencies: tuple[str, ...] = ()
    witness: WitnessEvidence | None = None
    review: IndependentReview | None = None

    def __post_init__(self) -> None:
        _require_id(self.repair_id, "repair_id")
        _require_id(self.target_id, "target_id")
        if self.target_role not in TARGET_ROLES:
            raise SchemaError(f"unknown target role: {self.target_role!r}")
        if self.repair_class not in CLASS_ALLOWED_ROLES:
            raise SchemaError(f"unknown repair class: {self.repair_class!r}")
        _require_sha256(self.expected_target_sha256, "expected_target_sha256")
        _require_sha256(self.expected_result_sha256, "expected_result_sha256")
        _require_nonempty_text(self.creator_principal_id, "creator_principal_id")
        if self.workflow_state not in WORKFLOW_STATES:
            raise SchemaError(f"unknown workflow state: {self.workflow_state!r}")
        if self.final_disposition not in FINAL_DISPOSITIONS:
            raise SchemaError(f"unknown final disposition: {self.final_disposition!r}")
        if type(self.dependencies) is not tuple:
            raise SchemaError("dependencies must be an immutable tuple")
        for dependency in self.dependencies:
            _require_id(dependency, "dependency repair ID")
        if len(self.dependencies) != len(set(self.dependencies)):
            raise SchemaError(f"duplicate dependencies in {self.repair_id}")
        if self.repair_id in self.dependencies:
            raise SchemaError(f"repair depends on itself: {self.repair_id}")
        if self.witness is not None and not isinstance(self.witness, WitnessEvidence):
            raise SchemaError("witness must be WitnessEvidence or None")
        if self.review is not None and not isinstance(self.review, IndependentReview):
            raise SchemaError("review must be IndependentReview or None")


@dataclass(frozen=True, slots=True)
class Replace:
    meta: OperationMeta
    block_id: str
    expected_block_sha256: str
    preimage: ByteLike
    replacement: ByteLike
    expected_count: int

    operation = "REPLACE"

    def __post_init__(self) -> None:
        _require_id(self.block_id, "block_id")
        _require_sha256(self.expected_block_sha256, "expected_block_sha256")
        object.__setattr__(self, "preimage", _bytes(self.preimage, "replace preimage"))
        object.__setattr__(self, "replacement", _bytes(self.replacement, "replacement"))
        if not self.preimage:
            raise SchemaError("replace preimage must be nonempty")
        if not self.replacement:
            raise SchemaError("replace replacement must be nonempty; use Delete")
        if self.preimage == self.replacement:
            raise SchemaError("replace operation is a no-op")
        _require_positive_int(self.expected_count, "replace expected_count")


@dataclass(frozen=True, slots=True)
class Delete:
    meta: OperationMeta
    block_id: str
    expected_block_sha256: str
    preimage: ByteLike
    expected_count: int

    operation = "DELETE"

    def __post_init__(self) -> None:
        _require_id(self.block_id, "block_id")
        _require_sha256(self.expected_block_sha256, "expected_block_sha256")
        object.__setattr__(self, "preimage", _bytes(self.preimage, "delete preimage"))
        if not self.preimage:
            raise SchemaError("delete preimage must be nonempty")
        _require_positive_int(self.expected_count, "delete expected_count")


@dataclass(frozen=True, slots=True)
class AnchoredInsert:
    meta: OperationMeta
    block_id: str
    expected_block_sha256: str
    left_anchor: ByteLike
    right_anchor: ByteLike
    insertion: ByteLike
    expected_adjacency_count: int

    operation = "ANCHORED_INSERT"

    def __post_init__(self) -> None:
        _require_id(self.block_id, "block_id")
        _require_sha256(self.expected_block_sha256, "expected_block_sha256")
        object.__setattr__(self, "left_anchor", _bytes(self.left_anchor, "left anchor"))
        object.__setattr__(self, "right_anchor", _bytes(self.right_anchor, "right anchor"))
        object.__setattr__(self, "insertion", _bytes(self.insertion, "insertion"))
        if not self.left_anchor or not self.right_anchor:
            raise SchemaError("anchored insert requires two nonempty anchors")
        if not self.insertion:
            raise SchemaError("anchored insert payload must be nonempty")
        _require_exact_one(
            self.expected_adjacency_count,
            "anchored insert expected_adjacency_count",
        )


@dataclass(frozen=True, slots=True)
class Move:
    meta: OperationMeta
    block_id: str
    expected_block_sha256: str
    source_left_id: str | None
    source_right_id: str | None
    destination_left_id: str | None
    destination_right_id: str | None
    expected_source_adjacency_count: int
    expected_destination_adjacency_count: int

    operation = "MOVE"

    def __post_init__(self) -> None:
        _require_id(self.block_id, "block_id")
        _require_sha256(self.expected_block_sha256, "expected_block_sha256")
        for field, value in (
            ("source_left_id", self.source_left_id),
            ("source_right_id", self.source_right_id),
            ("destination_left_id", self.destination_left_id),
            ("destination_right_id", self.destination_right_id),
        ):
            if value is not None:
                _require_id(value, field)
            if value == self.block_id:
                raise SchemaError(f"{field} cannot be the moved block")
        if self.source_left_id is None and self.source_right_id is None:
            raise SchemaError("move requires at least one source neighbor")
        if self.destination_left_id is None and self.destination_right_id is None:
            raise SchemaError("move requires at least one destination neighbor")
        _require_exact_one(
            self.expected_source_adjacency_count,
            "move expected_source_adjacency_count",
        )
        _require_exact_one(
            self.expected_destination_adjacency_count,
            "move expected_destination_adjacency_count",
        )


@dataclass(frozen=True, slots=True)
class Split:
    meta: OperationMeta
    block_id: str
    expected_block_sha256: str
    parts: tuple[Block, ...]
    expected_block_count: int

    operation = "SPLIT"

    def __post_init__(self) -> None:
        _require_id(self.block_id, "block_id")
        _require_sha256(self.expected_block_sha256, "expected_block_sha256")
        if type(self.parts) is not tuple:
            raise SchemaError("split parts must be an immutable tuple")
        if len(self.parts) < 2:
            raise SchemaError("split requires at least two parts")
        if any(not isinstance(part, Block) for part in self.parts):
            raise SchemaError("split parts must be Blocks")
        if any(not part.data for part in self.parts):
            raise SchemaError("split parts must be nonempty")
        ids = [part.block_id for part in self.parts]
        if len(ids) != len(set(ids)):
            raise SchemaError("split part IDs must be unique")
        if self.block_id in ids:
            raise SchemaError("split part IDs must not reuse the source block ID")
        _require_exact_one(self.expected_block_count, "split expected_block_count")


@dataclass(frozen=True, slots=True)
class Merge:
    meta: OperationMeta
    block_ids: tuple[str, ...]
    expected_block_sha256s: tuple[str, ...]
    merged_block: Block
    expected_adjacency_count: int

    operation = "MERGE"

    def __post_init__(self) -> None:
        if type(self.block_ids) is not tuple:
            raise SchemaError("merge block_ids must be an immutable tuple")
        if type(self.expected_block_sha256s) is not tuple:
            raise SchemaError("merge expected_block_sha256s must be an immutable tuple")
        if len(self.block_ids) < 2:
            raise SchemaError("merge requires at least two source blocks")
        for block_id in self.block_ids:
            _require_id(block_id, "merge block ID")
        if len(self.block_ids) != len(set(self.block_ids)):
            raise SchemaError("merge block IDs must be unique")
        if len(self.expected_block_sha256s) != len(self.block_ids):
            raise SchemaError("merge block hash count differs from block ID count")
        for expected in self.expected_block_sha256s:
            _require_sha256(expected, "merge expected block SHA-256")
        if not isinstance(self.merged_block, Block):
            raise SchemaError("merged_block must be a Block")
        if self.merged_block.block_id in self.block_ids:
            raise SchemaError("merged block ID must not reuse a source block ID")
        _require_exact_one(self.expected_adjacency_count, "merge expected_adjacency_count")


Operation: TypeAlias = Replace | Delete | AnchoredInsert | Move | Split | Merge


def _feed_projection_value(digest: "hashlib._Hash", value: object) -> None:
    """Feed a closed Python value into a deterministic, typed hash stream."""

    if value is None:
        _feed_length_prefixed(digest, b"NONE")
        return
    if type(value) is bool:
        _feed_length_prefixed(digest, b"BOOL")
        _feed_length_prefixed(digest, b"1" if value else b"0")
        return
    if type(value) is int:
        _feed_length_prefixed(digest, b"INT")
        _feed_length_prefixed(digest, str(value).encode("ascii"))
        return
    if isinstance(value, str):
        _feed_length_prefixed(digest, b"STR")
        _feed_length_prefixed(digest, value.encode("utf-8"))
        return
    if isinstance(value, bytes):
        _feed_length_prefixed(digest, b"BYTES")
        _feed_length_prefixed(digest, value)
        return
    if type(value) is tuple:
        _feed_length_prefixed(digest, b"TUPLE")
        digest.update(len(value).to_bytes(8, "big"))
        for item in value:
            _feed_projection_value(digest, item)
        return
    if is_dataclass(value):
        _feed_length_prefixed(digest, b"DATACLASS")
        _feed_length_prefixed(digest, type(value).__name__.encode("ascii"))
        projected_fields = tuple(item for item in fields(value) if not item.name.startswith("_"))
        digest.update(len(projected_fields).to_bytes(8, "big"))
        for item in projected_fields:
            _feed_length_prefixed(digest, item.name.encode("ascii"))
            _feed_projection_value(digest, getattr(value, item.name))
        return
    raise SchemaError(f"value has no closed projection encoding: {type(value).__name__}")


def _projection_sha256(domain: bytes, value: object) -> str:
    digest = hashlib.sha256()
    _feed_length_prefixed(digest, domain)
    _feed_projection_value(digest, value)
    return digest.hexdigest()


def operation_projection_sha256(record: Operation) -> str:
    """Bind every declared field of one exact typed operation."""

    if not isinstance(record, (Replace, Delete, AnchoredInsert, Move, Split, Merge)):
        raise SchemaError("operation projection requires a known operation record")
    return _projection_sha256(b"ANKOS-OVERLAY-OPERATION-2", record)


def ordered_operations_sha256(records: Sequence[Operation]) -> str:
    projections = tuple(operation_projection_sha256(record) for record in records)
    return _projection_sha256(b"ANKOS-OVERLAY-ORDERED-BATCH-2", projections)


@dataclass(frozen=True, slots=True)
class AuthorityGrant:
    """One validator-approved exact canonical operation/evidence join."""

    repair_id: str
    target_id: str
    target_role: str
    operation_projection_sha256: str
    witness_id: str | None
    witness_region_id: str | None
    witness_region_sha256: str | None
    review_id: str | None
    specialist_review_id: str | None

    def __post_init__(self) -> None:
        _require_id(self.repair_id, "authority repair_id")
        _require_id(self.target_id, "authority target_id")
        if self.target_role != CANONICAL_AUTHOR_TEXT:
            raise SchemaError("authority grants are only for canonical author text")
        _require_sha256(
            self.operation_projection_sha256,
            "authority operation projection SHA-256",
        )
        for value, field_name in (
            (self.witness_id, "authority witness_id"),
            (self.witness_region_id, "authority witness_region_id"),
            (self.review_id, "authority review_id"),
            (self.specialist_review_id, "authority specialist_review_id"),
        ):
            if value is not None:
                _require_id(value, field_name)
        if self.witness_region_sha256 is not None:
            _require_sha256(
                self.witness_region_sha256,
                "authority witness region SHA-256",
            )


def _authority_integrity_sha256(
    *,
    gate_state: str,
    baseline_lock_sha256: str,
    witness_lock_sha256: str,
    registry_sha256: str,
    validator_proof_sha256: str,
    initial_state_sha256: str,
    ordered_batch_sha256: str,
    grants: tuple[AuthorityGrant, ...],
    synthetic_test_only: bool,
) -> str:
    payload = (
        gate_state,
        baseline_lock_sha256,
        witness_lock_sha256,
        registry_sha256,
        validator_proof_sha256,
        initial_state_sha256,
        ordered_batch_sha256,
        grants,
        synthetic_test_only,
    )
    return _projection_sha256(b"ANKOS-OVERLAY-AUTHORITY-2", payload)


@dataclass(frozen=True, slots=True)
class ApplicationAuthority:
    """Sealed result of higher-level registry/gate validation.

    The overlay primitive never reads the registry or filesystem.  Production
    code must call ``_application_authority_from_validated_registry`` only
    after its independent validator has authenticated the supplied lock,
    registry, target identities, and grants.  The public default is blocked;
    the sole public OPEN constructor is explicitly test-only.
    """

    gate_state: str
    baseline_lock_sha256: str
    witness_lock_sha256: str
    registry_sha256: str
    validator_proof_sha256: str
    initial_state_sha256: str
    ordered_batch_sha256: str
    grants: tuple[AuthorityGrant, ...]
    synthetic_test_only: bool
    integrity_sha256: str
    _seal: object = field(repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._seal is not _AUTHORITY_SEAL:
            raise SchemaError("ApplicationAuthority must be sealed by the registry validator")
        if self.gate_state not in AUTHORITY_GATE_STATES:
            raise SchemaError(f"unknown application authority gate: {self.gate_state!r}")
        for value, field_name in (
            (self.baseline_lock_sha256, "authority baseline lock SHA-256"),
            (self.witness_lock_sha256, "authority witness lock SHA-256"),
            (self.registry_sha256, "authority registry SHA-256"),
            (self.validator_proof_sha256, "authority validator proof SHA-256"),
            (self.initial_state_sha256, "authority initial-state SHA-256"),
            (self.ordered_batch_sha256, "authority ordered-batch SHA-256"),
            (self.integrity_sha256, "authority integrity SHA-256"),
        ):
            _require_sha256(value, field_name)
        if type(self.grants) is not tuple:
            raise SchemaError("authority grants must be an immutable tuple")
        if any(not isinstance(grant, AuthorityGrant) for grant in self.grants):
            raise SchemaError("authority grants contain a non-AuthorityGrant value")
        repair_ids = [grant.repair_id for grant in self.grants]
        if len(repair_ids) != len(set(repair_ids)):
            raise SchemaError("authority contains duplicate repair grants")
        if type(self.synthetic_test_only) is not bool:
            raise SchemaError("synthetic_test_only must be a strict boolean")
        expected = _authority_integrity_sha256(
            gate_state=self.gate_state,
            baseline_lock_sha256=self.baseline_lock_sha256,
            witness_lock_sha256=self.witness_lock_sha256,
            registry_sha256=self.registry_sha256,
            validator_proof_sha256=self.validator_proof_sha256,
            initial_state_sha256=self.initial_state_sha256,
            ordered_batch_sha256=self.ordered_batch_sha256,
            grants=self.grants,
            synthetic_test_only=self.synthetic_test_only,
        )
        if self.integrity_sha256 != expected:
            raise SchemaError("application authority integrity guard failed")


def _application_authority_from_validated_registry(
    *,
    gate_state: str,
    baseline_lock_sha256: str,
    witness_lock_sha256: str,
    registry_sha256: str,
    validator_proof_sha256: str,
    initial_state_sha256: str,
    ordered_batch_sha256: str,
    grants: tuple[AuthorityGrant, ...],
    synthetic_test_only: bool = False,
) -> ApplicationAuthority:
    """Validator boundary: seal an already validated authoritative registry.

    This leading-underscore factory is deliberately not a general public
    authority mint.  Its caller is the higher-level validator responsible for
    establishing the external trust root; this primitive verifies all joins.
    """

    if type(grants) is not tuple:
        raise SchemaError("validated authority grants must be an immutable tuple")
    integrity = _authority_integrity_sha256(
        gate_state=gate_state,
        baseline_lock_sha256=baseline_lock_sha256,
        witness_lock_sha256=witness_lock_sha256,
        registry_sha256=registry_sha256,
        validator_proof_sha256=validator_proof_sha256,
        initial_state_sha256=initial_state_sha256,
        ordered_batch_sha256=ordered_batch_sha256,
        grants=grants,
        synthetic_test_only=synthetic_test_only,
    )
    return ApplicationAuthority(
        gate_state=gate_state,
        baseline_lock_sha256=baseline_lock_sha256,
        witness_lock_sha256=witness_lock_sha256,
        registry_sha256=registry_sha256,
        validator_proof_sha256=validator_proof_sha256,
        initial_state_sha256=initial_state_sha256,
        ordered_batch_sha256=ordered_batch_sha256,
        grants=grants,
        synthetic_test_only=synthetic_test_only,
        integrity_sha256=integrity,
        _seal=_AUTHORITY_SEAL,
    )


def _authority_grant_for(record: Operation) -> AuthorityGrant:
    meta = record.meta
    witness = meta.witness
    review = meta.review
    return AuthorityGrant(
        repair_id=meta.repair_id,
        target_id=meta.target_id,
        target_role=meta.target_role,
        operation_projection_sha256=operation_projection_sha256(record),
        witness_id=None if witness is None else witness.witness_id,
        witness_region_id=None if witness is None else witness.region_id,
        witness_region_sha256=None if witness is None else witness.region_sha256,
        review_id=None if review is None else review.review_id,
        specialist_review_id=None if review is None else review.specialist_review_id,
    )


def test_only_application_authority(
    initial: OverlayState, records: Iterable[Operation]
) -> ApplicationAuthority:
    """Seal a synthetic OPEN authority for unit tests only.

    Production validators must never call this function.  Its conspicuous name
    and ``synthetic_test_only`` bit make accidental release use observable.
    """

    if not isinstance(initial, OverlayState):
        raise SchemaError("test authority initial state must be OverlayState")
    closed_records = tuple(records)
    batch_sha256 = ordered_operations_sha256(closed_records)
    grants = tuple(
        _authority_grant_for(record)
        for record in closed_records
        if record.meta.target_role == CANONICAL_AUTHOR_TEXT
    )
    registry_sha256 = _projection_sha256(
        b"ANKOS-OVERLAY-SYNTHETIC-REGISTRY-2", grants
    )
    return _application_authority_from_validated_registry(
        gate_state="OPEN",
        baseline_lock_sha256=sha256_bytes(b"TEST-ONLY-BASELINE-LOCK"),
        witness_lock_sha256=sha256_bytes(b"TEST-ONLY-WITNESS-LOCK"),
        registry_sha256=registry_sha256,
        validator_proof_sha256=sha256_bytes(b"TEST-ONLY-VALIDATOR-PROOF"),
        initial_state_sha256=initial.sha256,
        ordered_batch_sha256=batch_sha256,
        grants=grants,
        synthetic_test_only=True,
    )


@dataclass(frozen=True, slots=True)
class OperationReceipt:
    """Context-bound exact postimage and declared reverse payload."""

    sequence_index: int
    repair_id: str
    operation: str
    inverse_operation: str
    target_id: str
    target_role: str
    operation_projection_sha256: str
    authority_context_sha256: str
    before_target_sha256: str
    after_target_sha256: str
    before_blocks: tuple[Block, ...]
    after_blocks: tuple[Block, ...]
    previous_receipt_sha256: str
    receipt_sha256: str

    def __post_init__(self) -> None:
        if type(self.sequence_index) is not int or self.sequence_index < 0:
            raise SchemaError("receipt sequence_index must be a nonnegative integer")
        _require_id(self.repair_id, "receipt repair_id")
        _require_id(self.target_id, "receipt target_id")
        if self.target_role not in TARGET_ROLES:
            raise SchemaError("receipt has an unknown target role")
        if type(self.before_blocks) is not tuple or type(self.after_blocks) is not tuple:
            raise SchemaError("receipt block snapshots must be immutable tuples")
        for value, field_name in (
            (self.operation_projection_sha256, "receipt operation projection SHA-256"),
            (self.authority_context_sha256, "receipt authority context SHA-256"),
            (self.before_target_sha256, "receipt before-target SHA-256"),
            (self.after_target_sha256, "receipt after-target SHA-256"),
            (self.previous_receipt_sha256, "receipt previous-link SHA-256"),
            (self.receipt_sha256, "receipt SHA-256"),
        ):
            _require_sha256(value, field_name)


def _receipt_integrity_sha256(receipt: OperationReceipt) -> str:
    payload = tuple(
        getattr(receipt, item.name)
        for item in fields(receipt)
        if item.name != "receipt_sha256"
    )
    return _projection_sha256(b"ANKOS-OVERLAY-RECEIPT-2", payload)


@dataclass(frozen=True, slots=True)
class ReplayResult:
    """Sealed forward result and integrity-linked receipts for inverse replay."""

    state: OverlayState
    receipts: tuple[OperationReceipt, ...]
    initial_state_sha256: str
    final_state_sha256: str
    authority_context_sha256: str
    ordered_batch_sha256: str
    receipt_chain_sha256: str
    integrity_sha256: str
    _seal: object = field(repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._seal is not _REPLAY_SEAL:
            raise SchemaError("ReplayResult must be created by apply_overlays")
        if not isinstance(self.state, OverlayState):
            raise SchemaError("replay state must be OverlayState")
        if type(self.receipts) is not tuple:
            raise SchemaError("replay receipts must be an immutable tuple")
        if any(not isinstance(receipt, OperationReceipt) for receipt in self.receipts):
            raise SchemaError("replay contains a non-OperationReceipt value")
        for value, field_name in (
            (self.initial_state_sha256, "replay initial-state SHA-256"),
            (self.final_state_sha256, "replay final-state SHA-256"),
            (self.authority_context_sha256, "replay authority-context SHA-256"),
            (self.ordered_batch_sha256, "replay ordered-batch SHA-256"),
            (self.receipt_chain_sha256, "replay receipt-chain SHA-256"),
            (self.integrity_sha256, "replay integrity SHA-256"),
        ):
            _require_sha256(value, field_name)


def _replay_integrity_sha256(
    *,
    state_sha256: str,
    initial_state_sha256: str,
    final_state_sha256: str,
    authority_context_sha256: str,
    ordered_batch_sha256: str,
    receipt_chain_sha256: str,
) -> str:
    return _projection_sha256(
        b"ANKOS-OVERLAY-REPLAY-2",
        (
            state_sha256,
            initial_state_sha256,
            final_state_sha256,
            authority_context_sha256,
            ordered_batch_sha256,
            receipt_chain_sha256,
        ),
    )


def _block_index(blocks: Sequence[Block], block_id: str) -> int:
    positions = [index for index, block in enumerate(blocks) if block.block_id == block_id]
    if len(positions) != 1:
        raise GuardError(f"expected exactly one block {block_id}, found {len(positions)}")
    return positions[0]


def _adjacency_count(ids: Sequence[str], left: str | None, right: str | None) -> int:
    if left is None:
        return int(bool(ids) and ids[0] == right)
    if right is None:
        return int(bool(ids) and ids[-1] == left)
    return sum(1 for index in range(len(ids) - 1) if ids[index] == left and ids[index + 1] == right)


def _source_adjacency_count(
    ids: Sequence[str], left: str | None, block_id: str, right: str | None
) -> int:
    count = 0
    for index, candidate in enumerate(ids):
        if candidate != block_id:
            continue
        actual_left = ids[index - 1] if index else None
        actual_right = ids[index + 1] if index + 1 < len(ids) else None
        if actual_left == left and actual_right == right:
            count += 1
    return count


def _replace_block(blocks: Sequence[Block], index: int, block: Block) -> tuple[Block, ...]:
    changed = list(blocks)
    changed[index] = block
    return tuple(changed)


def _validate_block_hash(block: Block, expected: str, repair_id: str) -> None:
    if block.sha256 != expected:
        raise GuardError(f"{repair_id}: block hash guard failed for {block.block_id}")


def _apply_operation(record: Operation, blocks: tuple[Block, ...]) -> tuple[Block, ...]:
    repair_id = record.meta.repair_id
    if isinstance(record, Replace):
        index = _block_index(blocks, record.block_id)
        block = blocks[index]
        _validate_block_hash(block, record.expected_block_sha256, repair_id)
        count = block.data.count(record.preimage)
        if count != record.expected_count:
            raise GuardError(
                f"{repair_id}: replace preimage count guard failed; expected "
                f"{record.expected_count}, found {count}"
            )
        return _replace_block(
            blocks,
            index,
            Block(block.block_id, block.data.replace(record.preimage, record.replacement)),
        )

    if isinstance(record, Delete):
        index = _block_index(blocks, record.block_id)
        block = blocks[index]
        _validate_block_hash(block, record.expected_block_sha256, repair_id)
        count = block.data.count(record.preimage)
        if count != record.expected_count:
            raise GuardError(
                f"{repair_id}: delete preimage count guard failed; expected "
                f"{record.expected_count}, found {count}"
            )
        return _replace_block(
            blocks,
            index,
            Block(block.block_id, block.data.replace(record.preimage, b"")),
        )

    if isinstance(record, AnchoredInsert):
        index = _block_index(blocks, record.block_id)
        block = blocks[index]
        _validate_block_hash(block, record.expected_block_sha256, repair_id)
        adjacent = record.left_anchor + record.right_anchor
        count = block.data.count(adjacent)
        if count != record.expected_adjacency_count:
            raise GuardError(
                f"{repair_id}: adjacent anchor count guard failed; expected "
                f"{record.expected_adjacency_count}, found {count}"
            )
        inserted = record.left_anchor + record.insertion + record.right_anchor
        return _replace_block(blocks, index, Block(block.block_id, block.data.replace(adjacent, inserted)))

    if isinstance(record, Move):
        index = _block_index(blocks, record.block_id)
        block = blocks[index]
        _validate_block_hash(block, record.expected_block_sha256, repair_id)
        ids = [candidate.block_id for candidate in blocks]
        source_count = _source_adjacency_count(
            ids, record.source_left_id, record.block_id, record.source_right_id
        )
        if source_count != record.expected_source_adjacency_count:
            raise GuardError(
                f"{repair_id}: source adjacency guard failed; expected "
                f"{record.expected_source_adjacency_count}, found {source_count}"
            )
        remaining = list(blocks)
        remaining.pop(index)
        remaining_ids = [candidate.block_id for candidate in remaining]
        destination_count = _adjacency_count(
            remaining_ids, record.destination_left_id, record.destination_right_id
        )
        if destination_count != record.expected_destination_adjacency_count:
            raise GuardError(
                f"{repair_id}: destination adjacency guard failed; expected "
                f"{record.expected_destination_adjacency_count}, found {destination_count}"
            )
        if record.destination_left_id is None:
            destination = 0
        elif record.destination_right_id is None:
            destination = len(remaining)
        else:
            destination = remaining_ids.index(record.destination_right_id)
        remaining.insert(destination, block)
        result = tuple(remaining)
        if result == blocks:
            raise GuardError(f"{repair_id}: move operation is a no-op")
        return result

    if isinstance(record, Split):
        index = _block_index(blocks, record.block_id)
        block = blocks[index]
        _validate_block_hash(block, record.expected_block_sha256, repair_id)
        if sum(candidate.block_id == record.block_id for candidate in blocks) != record.expected_block_count:
            raise GuardError(f"{repair_id}: split block count guard failed")
        if b"".join(part.data for part in record.parts) != block.data:
            raise GuardError(f"{repair_id}: split parts do not exactly reconstruct the preimage")
        existing = {candidate.block_id for candidate in blocks}
        collisions = existing.intersection(part.block_id for part in record.parts)
        if collisions:
            raise GuardError(f"{repair_id}: split part ID collides with target: {sorted(collisions)!r}")
        return tuple(blocks[:index]) + record.parts + tuple(blocks[index + 1 :])

    if isinstance(record, Merge):
        ids = [candidate.block_id for candidate in blocks]
        pattern = list(record.block_ids)
        starts = [
            index
            for index in range(len(ids) - len(pattern) + 1)
            if ids[index : index + len(pattern)] == pattern
        ]
        if len(starts) != record.expected_adjacency_count:
            raise GuardError(
                f"{repair_id}: merge adjacency guard failed; expected "
                f"{record.expected_adjacency_count}, found {len(starts)}"
            )
        start = starts[0]
        sources = tuple(blocks[start : start + len(pattern)])
        for block, expected in zip(sources, record.expected_block_sha256s, strict=True):
            _validate_block_hash(block, expected, repair_id)
        if record.merged_block.data != b"".join(block.data for block in sources):
            raise GuardError(f"{repair_id}: merged block does not exactly reconstruct source bytes")
        existing = set(ids).difference(record.block_ids)
        if record.merged_block.block_id in existing:
            raise GuardError(f"{repair_id}: merged block ID collides with target")
        return (
            tuple(blocks[:start])
            + (record.merged_block,)
            + tuple(blocks[start + len(pattern) :])
        )

    raise SchemaError(f"unknown operation type: {type(record).__name__}")


def _validate_role(record: Operation) -> None:
    meta = record.meta
    allowed = CLASS_ALLOWED_ROLES[meta.repair_class]
    if meta.target_role not in allowed:
        raise RoleError(
            f"{meta.repair_id}: class {meta.repair_class} cannot target {meta.target_role}"
        )
    if meta.target_role == DERIVED_AGGREGATE:
        raise RoleError(f"{meta.repair_id}: derived aggregate refuses repair overlays")


def _validate_application_workflow(record: Operation) -> None:
    """Refuse pending, rejected, duplicate, or unresolved records before mutation."""

    meta = record.meta
    if meta.workflow_state != "CLOSED":
        raise EvidenceError(f"{meta.repair_id}: applied overlay is not CLOSED; it must be CLOSED")
    if meta.target_role == CANONICAL_AUTHOR_TEXT:
        allowed = {"APPLIED_WITNESS_VERIFIED"}
    elif meta.target_role == GENERATED_METADATA:
        allowed = {"APPLIED_MECHANICALLY_PROVEN"}
    elif meta.target_role == EDITORIAL_SIDECAR:
        allowed = {"ANNOTATED_SOURCE_ERRATUM"}
    elif meta.target_role == SEARCH_DERIVATIVE:
        allowed = {"APPLIED_MECHANICALLY_PROVEN"}
    else:
        allowed = set()
    if meta.final_disposition not in allowed:
        raise EvidenceError(
            f"{meta.repair_id}: disposition {meta.final_disposition} is not applicable "
            f"to {meta.target_role}"
        )


def _validate_witness(witness: WitnessEvidence, repair_id: str) -> None:
    _require_nonempty_text(witness.witness_id, "witness_id")
    _require_nonempty_text(witness.edition_id, "edition_id")
    _require_nonempty_text(witness.region_id, "region_id")
    _require_sha256(witness.region_sha256, "witness region SHA-256")
    _require_sha256(witness.evidence_view_sha256, "evidence view SHA-256")
    if witness.authorized is not True:
        raise EvidenceError(f"{repair_id}: witness is not authorized")
    if witness.edition_identical is not True:
        raise EvidenceError(f"{repair_id}: witness is not edition-identical")
    if witness.legible_for_change is not True:
        raise EvidenceError(f"{repair_id}: witness region is not legible for the change")


def _validate_review(
    meta: OperationMeta, review: IndependentReview, *, high_risk: bool
) -> None:
    repair_id = meta.repair_id
    _require_id(review.review_id, "source review_id")
    if review.creator_principal_id != meta.creator_principal_id:
        raise EvidenceError(f"{repair_id}: review creator does not match repair creator")
    _require_nonempty_text(review.source_reviewer_principal_id, "source reviewer principal ID")
    if review.source_reviewer_principal_id == meta.creator_principal_id:
        raise EvidenceError(f"{repair_id}: creator cannot independently source-review the repair")
    if review.source_reviewer_type not in PRINCIPAL_TYPES:
        raise EvidenceError(f"{repair_id}: unknown source reviewer type")
    _require_nonempty_text(review.source_reviewer_session_id, "source reviewer session ID")
    if review.source_reviewer_role != "SOURCE_REVIEWER":
        raise EvidenceError(f"{repair_id}: independent decision is not a SOURCE_REVIEWER decision")
    if review.source_decision != "APPROVED":
        raise EvidenceError(f"{repair_id}: source review is not approved")
    _require_sha256(review.evidence_view_sha256, "review evidence view SHA-256")
    witness = meta.witness
    if witness is None:
        raise EvidenceError(f"{repair_id}: review cannot bind an absent witness")
    if review.evidence_view_sha256 != witness.evidence_view_sha256:
        raise EvidenceError(f"{repair_id}: source review evidence-view hash mismatch")

    if high_risk:
        if review.blind_preproposal is not True:
            raise EvidenceError(f"{repair_id}: high-risk repair lacks blind preproposal review")
        if review.specialist_review_id is None:
            raise EvidenceError(f"{repair_id}: high-risk repair lacks specialist review ID")
        _require_id(review.specialist_review_id, "specialist review_id")
        if not review.specialist_principal_id:
            raise EvidenceError(f"{repair_id}: high-risk repair lacks specialist review")
        if review.specialist_principal_id == meta.creator_principal_id:
            raise EvidenceError(f"{repair_id}: creator cannot specialist-review the repair")
        if review.specialist_type not in PRINCIPAL_TYPES:
            raise EvidenceError(f"{repair_id}: unknown specialist reviewer type")
        _require_nonempty_text(review.specialist_session_id or "", "specialist session ID")
        if review.specialist_decision != "APPROVED":
            raise EvidenceError(f"{repair_id}: specialist review is not approved")
        if review.specialist_evidence_view_sha256 != witness.evidence_view_sha256:
            raise EvidenceError(f"{repair_id}: specialist evidence-view hash mismatch")


def _markdown_structure_signature(blocks: Sequence[Block]) -> tuple[tuple[str, int], ...]:
    """Return byte-level Markdown marker locations without trusting repair class."""

    markers: list[tuple[str, int]] = []
    line_number = 0
    for block in blocks:
        for line in block.data.splitlines():
            line_number += 1
            stripped = line.lstrip()
            if re.match(rb"#{1,6}(?:[ \t]|$)", stripped):
                markers.append(("ATX_HEADING", line_number))
            if stripped.startswith((b"```", b"~~~")):
                markers.append(("FENCE", line_number))
            if re.match(rb"(?:[-+*]|[0-9]+[.)])[ \t]+", stripped):
                markers.append(("LIST", line_number))
            if stripped.startswith(b">"):
                markers.append(("QUOTE", line_number))
            if b"|" in line:
                markers.append(("TABLE_CANDIDATE", line_number))
    return tuple(markers)


def _validate_evidence(
    record: Operation, before: Sequence[Block], after: Sequence[Block]
) -> None:
    meta = record.meta
    if meta.target_role == CANONICAL_AUTHOR_TEXT:
        if isinstance(record, (Replace, Delete)) and record.expected_count != 1:
            raise EvidenceError(f"{meta.repair_id}: canonical author-text repairs are per occurrence")
        if meta.workflow_state != "CLOSED":
            raise EvidenceError(f"{meta.repair_id}: author-text repair is not CLOSED")
        if meta.final_disposition != "APPLIED_WITNESS_VERIFIED":
            raise EvidenceError(
                f"{meta.repair_id}: author-text repair is not APPLIED_WITNESS_VERIFIED"
            )
        if meta.witness is None:
            raise EvidenceError(f"{meta.repair_id}: author-text repair lacks witness evidence")
        if meta.review is None:
            raise EvidenceError(f"{meta.repair_id}: author-text repair lacks independent review")
        _validate_witness(meta.witness, meta.repair_id)
        # Classification is caller-controlled, so it cannot lower risk.  A
        # Markdown marker change such as ``Title`` -> ``# Title`` is detected
        # independently, and every canonical semantic overlay is conservatively
        # specialist-reviewed even when its declared class is merely PROSE_OCR.
        structure_changed = (
            _markdown_structure_signature(before)
            != _markdown_structure_signature(after)
        )
        high_risk = structure_changed or meta.target_role == CANONICAL_AUTHOR_TEXT
        _validate_review(meta, meta.review, high_risk=high_risk)
        return


def _validate_application_authority(
    initial: OverlayState,
    records: tuple[Operation, ...],
    authority: ApplicationAuthority | None,
) -> str:
    """Verify the sealed gate and every exact canonical registry join."""

    canonical = tuple(
        record for record in records if record.meta.target_role == CANONICAL_AUTHOR_TEXT
    )
    if not canonical:
        return _projection_sha256(b"ANKOS-OVERLAY-NO-CANONICAL-AUTHORITY-2", ())
    if authority is None:
        raise EvidenceError("canonical application gate is SOURCE_BLOCKED; authority is required")
    if not isinstance(authority, ApplicationAuthority) or authority._seal is not _AUTHORITY_SEAL:
        raise EvidenceError("canonical application authority is not validator-sealed")
    expected_integrity = _authority_integrity_sha256(
        gate_state=authority.gate_state,
        baseline_lock_sha256=authority.baseline_lock_sha256,
        witness_lock_sha256=authority.witness_lock_sha256,
        registry_sha256=authority.registry_sha256,
        validator_proof_sha256=authority.validator_proof_sha256,
        initial_state_sha256=authority.initial_state_sha256,
        ordered_batch_sha256=authority.ordered_batch_sha256,
        grants=authority.grants,
        synthetic_test_only=authority.synthetic_test_only,
    )
    if authority.integrity_sha256 != expected_integrity:
        raise EvidenceError("canonical application authority integrity guard failed")
    if authority.gate_state != "OPEN":
        raise EvidenceError(f"canonical application gate is {authority.gate_state}")
    if authority.initial_state_sha256 != initial.sha256:
        raise EvidenceError("canonical authority initial-state binding mismatch")
    actual_batch = ordered_operations_sha256(records)
    if authority.ordered_batch_sha256 != actual_batch:
        raise EvidenceError("canonical authority ordered-operation binding mismatch")

    by_repair = {grant.repair_id: grant for grant in authority.grants}
    if set(by_repair) != {record.meta.repair_id for record in canonical}:
        raise EvidenceError("canonical authority grant set does not match the batch")
    for record in canonical:
        meta = record.meta
        grant = by_repair[meta.repair_id]
        witness = meta.witness
        review = meta.review
        expected_join = (
            meta.target_id,
            meta.target_role,
            operation_projection_sha256(record),
            None if witness is None else witness.witness_id,
            None if witness is None else witness.region_id,
            None if witness is None else witness.region_sha256,
            None if review is None else review.review_id,
            None if review is None else review.specialist_review_id,
        )
        actual_join = (
            grant.target_id,
            grant.target_role,
            grant.operation_projection_sha256,
            grant.witness_id,
            grant.witness_region_id,
            grant.witness_region_sha256,
            grant.review_id,
            grant.specialist_review_id,
        )
        if actual_join != expected_join:
            raise EvidenceError(f"{meta.repair_id}: authoritative registry join mismatch")
    return authority.integrity_sha256


INVERSE_NAMES = {
    "REPLACE": "REPLACE_EXACT_POSTIMAGE",
    "DELETE": "RESTORE_DELETED_SPAN",
    "ANCHORED_INSERT": "DELETE_ANCHORED_INSERTION",
    "MOVE": "MOVE_TO_SOURCE_ADJACENCY",
    "SPLIT": "MERGE_SPLIT_PARTS",
    "MERGE": "SPLIT_MERGED_BLOCK",
}


def apply_overlays(
    initial: OverlayState,
    records: Iterable[Operation],
    *,
    authority: ApplicationAuthority | None = None,
) -> ReplayResult:
    """Apply ordered overlays atomically to immutable state.

    Dependencies must name records in this exact batch and must already have
    succeeded.  This preserves the declared overlay order instead of silently
    choosing a topological order for the caller.
    """

    if not isinstance(initial, OverlayState):
        raise SchemaError("initial state must be an OverlayState")
    closed_records = tuple(records)
    if any(not isinstance(record, (Replace, Delete, AnchoredInsert, Move, Split, Merge)) for record in closed_records):
        raise SchemaError("overlay batch contains an unknown operation record")
    batch_sha256 = ordered_operations_sha256(closed_records)
    authority_context_sha256 = _validate_application_authority(
        initial, closed_records, authority
    )
    repair_ids = [record.meta.repair_id for record in closed_records]
    if len(repair_ids) != len(set(repair_ids)):
        raise DependencyError("overlay batch contains duplicate repair IDs")
    batch_ids = set(repair_ids)
    previous_receipt_sha256 = sha256_bytes(b"ANKOS-OVERLAY-RECEIPT-CHAIN-START-2")
    for sequence_index, record in enumerate(closed_records):
        missing = set(record.meta.dependencies).difference(batch_ids)
        if missing:
            raise DependencyError(
                f"{record.meta.repair_id}: unresolved dependencies: {sorted(missing)!r}"
            )

    state = initial
    receipts: list[OperationReceipt] = []
    applied: set[str] = set()
    for record in closed_records:
        meta = record.meta
        pending = set(meta.dependencies).difference(applied)
        if pending:
            raise DependencyError(
                f"{meta.repair_id}: dependencies are not ordered before repair: {sorted(pending)!r}"
            )
        _validate_role(record)
        _validate_application_workflow(record)
        before = state.blocks(meta.target_role, meta.target_id)
        actual_before_sha256 = target_sha256(meta.target_id, meta.target_role, before)
        if actual_before_sha256 != meta.expected_target_sha256:
            raise GuardError(f"{meta.repair_id}: complete target pre-state hash guard failed")

        after = _apply_operation(record, before)
        actual_after_sha256 = target_sha256(meta.target_id, meta.target_role, after)
        if actual_after_sha256 != meta.expected_result_sha256:
            raise GuardError(f"{meta.repair_id}: complete target post-state hash guard failed")
        _validate_evidence(record, before, after)

        state = state.with_blocks(meta.target_role, after, meta.target_id)
        unsigned_receipt = OperationReceipt(
            sequence_index=sequence_index,
            repair_id=meta.repair_id,
            operation=record.operation,
            inverse_operation=INVERSE_NAMES[record.operation],
            target_id=meta.target_id,
            target_role=meta.target_role,
            operation_projection_sha256=operation_projection_sha256(record),
            authority_context_sha256=authority_context_sha256,
            before_target_sha256=actual_before_sha256,
            after_target_sha256=actual_after_sha256,
            before_blocks=before,
            after_blocks=after,
            previous_receipt_sha256=previous_receipt_sha256,
            receipt_sha256="0" * 64,
        )
        receipt = replace(
            unsigned_receipt,
            receipt_sha256=_receipt_integrity_sha256(unsigned_receipt),
        )
        receipts.append(receipt)
        previous_receipt_sha256 = receipt.receipt_sha256
        applied.add(meta.repair_id)

    final_sha256 = state.sha256
    replay_integrity = _replay_integrity_sha256(
        state_sha256=final_sha256,
        initial_state_sha256=initial.sha256,
        final_state_sha256=final_sha256,
        authority_context_sha256=authority_context_sha256,
        ordered_batch_sha256=batch_sha256,
        receipt_chain_sha256=previous_receipt_sha256,
    )
    return ReplayResult(
        state=state,
        receipts=tuple(receipts),
        initial_state_sha256=initial.sha256,
        final_state_sha256=final_sha256,
        authority_context_sha256=authority_context_sha256,
        ordered_batch_sha256=batch_sha256,
        receipt_chain_sha256=previous_receipt_sha256,
        integrity_sha256=replay_integrity,
        _seal=_REPLAY_SEAL,
    )


def inverse_replay(result: ReplayResult, state: OverlayState | None = None) -> OverlayState:
    """Reverse a successful batch, refusing any changed postimage exactly."""

    if not isinstance(result, ReplayResult):
        raise SchemaError("inverse replay requires a ReplayResult")
    if result._seal is not _REPLAY_SEAL:
        raise InverseError("inverse replay result is not application-sealed")
    expected_replay_integrity = _replay_integrity_sha256(
        state_sha256=result.state.sha256,
        initial_state_sha256=result.initial_state_sha256,
        final_state_sha256=result.final_state_sha256,
        authority_context_sha256=result.authority_context_sha256,
        ordered_batch_sha256=result.ordered_batch_sha256,
        receipt_chain_sha256=result.receipt_chain_sha256,
    )
    if result.integrity_sha256 != expected_replay_integrity:
        raise InverseError("inverse replay authenticity/integrity digest failed")
    previous_receipt_sha256 = sha256_bytes(b"ANKOS-OVERLAY-RECEIPT-CHAIN-START-2")
    for expected_index, receipt in enumerate(result.receipts):
        if receipt.sequence_index != expected_index:
            raise InverseError("inverse replay receipt sequence is not contiguous")
        if receipt.authority_context_sha256 != result.authority_context_sha256:
            raise InverseError(f"{receipt.repair_id}: receipt authority context mismatch")
        if receipt.previous_receipt_sha256 != previous_receipt_sha256:
            raise InverseError(f"{receipt.repair_id}: receipt chain link mismatch")
        if receipt.receipt_sha256 != _receipt_integrity_sha256(receipt):
            raise InverseError(f"{receipt.repair_id}: receipt integrity digest failed")
        previous_receipt_sha256 = receipt.receipt_sha256
    if previous_receipt_sha256 != result.receipt_chain_sha256:
        raise InverseError("inverse replay receipt-chain terminal digest failed")
    current = result.state if state is None else state
    if not isinstance(current, OverlayState):
        raise SchemaError("inverse state must be an OverlayState")
    if current.sha256 != result.final_state_sha256:
        raise InverseError("inverse replay final-state hash guard failed")

    for receipt in reversed(result.receipts):
        actual = current.blocks(receipt.target_role, receipt.target_id)
        if actual != receipt.after_blocks:
            raise InverseError(f"{receipt.repair_id}: inverse exact postimage guard failed")
        if target_sha256(receipt.target_id, receipt.target_role, actual) != receipt.after_target_sha256:
            raise InverseError(f"{receipt.repair_id}: inverse postimage hash guard failed")
        if target_sha256(
            receipt.target_id, receipt.target_role, receipt.before_blocks
        ) != receipt.before_target_sha256:
            raise InverseError(f"{receipt.repair_id}: stored inverse preimage hash guard failed")
        current = current.with_blocks(
            receipt.target_role, receipt.before_blocks, receipt.target_id
        )

    if current.sha256 != result.initial_state_sha256:
        raise InverseError("inverse replay did not recover the exact initial state")
    return current


__all__ = [
    "AnchoredInsert",
    "Block",
    "CANONICAL_AUTHOR_TEXT",
    "DERIVED_AGGREGATE",
    "Delete",
    "DependencyError",
    "EDITORIAL_SIDECAR",
    "EvidenceError",
    "FIGURE_OR_CAPTION",
    "FORMULA_OR_SYMBOL",
    "GENERATED_METADATA",
    "GuardError",
    "HEADING_OR_FURNITURE",
    "INDEX_ENTRY",
    "IndependentReview",
    "InverseError",
    "MARKDOWN_STRUCTURE",
    "Merge",
    "Move",
    "NAVIGATION_METADATA",
    "OperationMeta",
    "OverlayError",
    "OverlayState",
    "PROSE_OCR",
    "ReplayResult",
    "Replace",
    "RoleError",
    "RULE_TABLE_OR_DATA",
    "SEARCH_DERIVATIVE",
    "SEARCH_NORMALIZATION",
    "SOURCE_ERRATUM_ANNOTATION",
    "STRUCTURE_BOUNDARY",
    "SchemaError",
    "Split",
    "WOLFRAM_CODE",
    "WitnessEvidence",
    "apply_overlays",
    "inverse_replay",
    "sha256_bytes",
    "target_sha256",
]
