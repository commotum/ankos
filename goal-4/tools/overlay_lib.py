"""Deterministic, fail-closed repair overlays for Goal 4.

This module deliberately operates on a small byte-block model.  It is the
executable core used to prove operation guards, role separation, dependency
ordering, and reversibility before any corpus repair is attempted.  It does
not read the legacy tree, a witness mount, or a generated output tree.

The public operations are immutable records.  Every record binds both the
complete target pre-state and post-state hashes, plus operation-specific
preimages/counts/hashes.  Canonical author-text changes are accepted only
with edition-identical witness-region evidence and an independent approved
source review.  Byte-conserving split/merge operations are the sole canonical
operations that may be mechanically proven without source evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
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


def target_sha256(role: str, blocks: Sequence[Block]) -> str:
    """Hash a complete role target with unambiguous IDs, order, and bytes."""

    if role not in TARGET_ROLES:
        raise SchemaError(f"unknown target role: {role!r}")
    digest = hashlib.sha256()
    _feed_length_prefixed(digest, b"ANKOS-OVERLAY-TARGET-1")
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
    """Immutable target-role state with deterministic ordering and hashing."""

    _targets: tuple[tuple[str, tuple[Block, ...]], ...]

    def __post_init__(self) -> None:
        roles = [role for role, _ in self._targets]
        if roles != sorted(roles):
            raise SchemaError("state targets must be sorted by role")
        if len(roles) != len(set(roles)):
            raise SchemaError("state contains duplicate target roles")
        for role, blocks in self._targets:
            target_sha256(role, blocks)

    @classmethod
    def from_mapping(cls, targets: Mapping[str, Iterable[Block]]) -> "OverlayState":
        if not isinstance(targets, Mapping):
            raise SchemaError("targets must be a mapping")
        closed = tuple(sorted((role, tuple(blocks)) for role, blocks in targets.items()))
        return cls(closed)

    @property
    def roles(self) -> tuple[str, ...]:
        return tuple(role for role, _ in self._targets)

    def blocks(self, role: str) -> tuple[Block, ...]:
        for candidate, blocks in self._targets:
            if candidate == role:
                return blocks
        raise RoleError(f"target role is absent from state: {role}")

    def target_sha256(self, role: str) -> str:
        return target_sha256(role, self.blocks(role))

    def with_blocks(self, role: str, blocks: Iterable[Block]) -> "OverlayState":
        if role not in self.roles:
            raise RoleError(f"target role is absent from state: {role}")
        replacement = tuple(blocks)
        target_sha256(role, replacement)
        return OverlayState.from_mapping(
            {
                candidate: replacement if candidate == role else existing
                for candidate, existing in self._targets
            }
        )

    @property
    def sha256(self) -> str:
        digest = hashlib.sha256()
        _feed_length_prefixed(digest, b"ANKOS-OVERLAY-STATE-1")
        digest.update(len(self._targets).to_bytes(8, "big"))
        for role, blocks in self._targets:
            _feed_length_prefixed(digest, role.encode("ascii"))
            _feed_length_prefixed(digest, target_sha256(role, blocks).encode("ascii"))
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

    creator_principal_id: str
    source_reviewer_principal_id: str
    source_reviewer_type: str
    source_reviewer_session_id: str
    source_reviewer_role: str
    source_decision: str
    evidence_view_sha256: str
    blind_preproposal: bool
    specialist_principal_id: str | None = None
    specialist_type: str | None = None
    specialist_session_id: str | None = None
    specialist_decision: str | None = None
    specialist_evidence_view_sha256: str | None = None


@dataclass(frozen=True, slots=True)
class OperationMeta:
    """Closed common metadata and complete target hash guards."""

    repair_id: str
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
        for dependency in self.dependencies:
            _require_id(dependency, "dependency repair ID")
        if len(self.dependencies) != len(set(self.dependencies)):
            raise SchemaError(f"duplicate dependencies in {self.repair_id}")
        if self.repair_id in self.dependencies:
            raise SchemaError(f"repair depends on itself: {self.repair_id}")


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
        if not isinstance(self.expected_count, int) or isinstance(self.expected_count, bool) or self.expected_count < 1:
            raise SchemaError("replace expected_count must be a positive integer")


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
        if not isinstance(self.expected_count, int) or isinstance(self.expected_count, bool) or self.expected_count < 1:
            raise SchemaError("delete expected_count must be a positive integer")


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
        if self.expected_adjacency_count != 1:
            raise SchemaError("anchored insert requires exactly one adjacent anchor pair")


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
        if self.expected_source_adjacency_count != 1:
            raise SchemaError("move requires exactly one guarded source adjacency")
        if self.expected_destination_adjacency_count != 1:
            raise SchemaError("move requires exactly one guarded destination adjacency")


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
        object.__setattr__(self, "parts", tuple(self.parts))
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
        if self.expected_block_count != 1:
            raise SchemaError("split requires exact source block count 1")


@dataclass(frozen=True, slots=True)
class Merge:
    meta: OperationMeta
    block_ids: tuple[str, ...]
    expected_block_sha256s: tuple[str, ...]
    merged_block: Block
    expected_adjacency_count: int

    operation = "MERGE"

    def __post_init__(self) -> None:
        object.__setattr__(self, "block_ids", tuple(self.block_ids))
        object.__setattr__(self, "expected_block_sha256s", tuple(self.expected_block_sha256s))
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
        if self.expected_adjacency_count != 1:
            raise SchemaError("merge requires exactly one guarded adjacency")


Operation: TypeAlias = Replace | Delete | AnchoredInsert | Move | Split | Merge


@dataclass(frozen=True, slots=True)
class OperationReceipt:
    """Exact postimage guard plus the declared reverse operation payload."""

    repair_id: str
    operation: str
    inverse_operation: str
    target_role: str
    before_target_sha256: str
    after_target_sha256: str
    before_blocks: tuple[Block, ...]
    after_blocks: tuple[Block, ...]


@dataclass(frozen=True, slots=True)
class ReplayResult:
    """Immutable forward result and receipts required for inverse replay."""

    state: OverlayState
    receipts: tuple[OperationReceipt, ...]
    initial_state_sha256: str
    final_state_sha256: str


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


def _canonical_change_requires_evidence(
    record: Operation, before: Sequence[Block], after: Sequence[Block]
) -> bool:
    if record.meta.target_role != CANONICAL_AUTHOR_TEXT:
        return False
    before_projection = b"".join(block.data for block in before)
    after_projection = b"".join(block.data for block in after)
    # A move is source-significant even in a degenerate equal-byte case.
    return isinstance(record, Move) or before_projection != after_projection


def _validate_evidence(
    record: Operation, before: Sequence[Block], after: Sequence[Block]
) -> None:
    meta = record.meta
    requires_evidence = _canonical_change_requires_evidence(record, before, after)
    if requires_evidence:
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
        high_risk = (
            meta.repair_class in HIGH_RISK_CLASSES
            or isinstance(record, (AnchoredInsert, Move))
        )
        _validate_review(meta, meta.review, high_risk=high_risk)
        return

    if meta.target_role == CANONICAL_AUTHOR_TEXT:
        if not isinstance(record, (Split, Merge)):
            raise EvidenceError(
                f"{meta.repair_id}: only byte-conserving split/merge may be mechanical in canonical text"
            )
        if meta.repair_class not in {STRUCTURE_BOUNDARY, MARKDOWN_STRUCTURE}:
            raise EvidenceError(
                f"{meta.repair_id}: mechanical canonical split/merge needs a structure class"
            )
        if meta.workflow_state != "CLOSED" or meta.final_disposition != "APPLIED_MECHANICALLY_PROVEN":
            raise EvidenceError(
                f"{meta.repair_id}: mechanical canonical split/merge must be CLOSED and proven"
            )


INVERSE_NAMES = {
    "REPLACE": "REPLACE_EXACT_POSTIMAGE",
    "DELETE": "RESTORE_DELETED_SPAN",
    "ANCHORED_INSERT": "DELETE_ANCHORED_INSERTION",
    "MOVE": "MOVE_TO_SOURCE_ADJACENCY",
    "SPLIT": "MERGE_SPLIT_PARTS",
    "MERGE": "SPLIT_MERGED_BLOCK",
}


def apply_overlays(initial: OverlayState, records: Iterable[Operation]) -> ReplayResult:
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
    repair_ids = [record.meta.repair_id for record in closed_records]
    if len(repair_ids) != len(set(repair_ids)):
        raise DependencyError("overlay batch contains duplicate repair IDs")
    batch_ids = set(repair_ids)
    for record in closed_records:
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
        before = state.blocks(meta.target_role)
        actual_before_sha256 = target_sha256(meta.target_role, before)
        if actual_before_sha256 != meta.expected_target_sha256:
            raise GuardError(f"{meta.repair_id}: complete target pre-state hash guard failed")

        after = _apply_operation(record, before)
        actual_after_sha256 = target_sha256(meta.target_role, after)
        if actual_after_sha256 != meta.expected_result_sha256:
            raise GuardError(f"{meta.repair_id}: complete target post-state hash guard failed")
        _validate_evidence(record, before, after)

        state = state.with_blocks(meta.target_role, after)
        receipts.append(
            OperationReceipt(
                repair_id=meta.repair_id,
                operation=record.operation,
                inverse_operation=INVERSE_NAMES[record.operation],
                target_role=meta.target_role,
                before_target_sha256=actual_before_sha256,
                after_target_sha256=actual_after_sha256,
                before_blocks=before,
                after_blocks=after,
            )
        )
        applied.add(meta.repair_id)

    return ReplayResult(
        state=state,
        receipts=tuple(receipts),
        initial_state_sha256=initial.sha256,
        final_state_sha256=state.sha256,
    )


def inverse_replay(result: ReplayResult, state: OverlayState | None = None) -> OverlayState:
    """Reverse a successful batch, refusing any changed postimage exactly."""

    if not isinstance(result, ReplayResult):
        raise SchemaError("inverse replay requires a ReplayResult")
    current = result.state if state is None else state
    if not isinstance(current, OverlayState):
        raise SchemaError("inverse state must be an OverlayState")
    if current.sha256 != result.final_state_sha256:
        raise InverseError("inverse replay final-state hash guard failed")

    for receipt in reversed(result.receipts):
        actual = current.blocks(receipt.target_role)
        if actual != receipt.after_blocks:
            raise InverseError(f"{receipt.repair_id}: inverse exact postimage guard failed")
        if target_sha256(receipt.target_role, actual) != receipt.after_target_sha256:
            raise InverseError(f"{receipt.repair_id}: inverse postimage hash guard failed")
        if target_sha256(receipt.target_role, receipt.before_blocks) != receipt.before_target_sha256:
            raise InverseError(f"{receipt.repair_id}: stored inverse preimage hash guard failed")
        current = current.with_blocks(receipt.target_role, receipt.before_blocks)

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
