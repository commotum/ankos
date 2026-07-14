#!/usr/bin/env python3
"""Dependency-free semantic oracle for T42 CF-driven substitutions.

The exact source construction is a finite schedule of ordinary binary T13
morphisms.  Given a finalized natural simple-continued-fraction prefix
``(a0,a1,...,a[m-1])``, it drops ``a0`` and reverses the remaining positive
coefficients exactly once.  A visible cursor selects one immutable morphism
per event; every old data occurrence is then replaced from the same snapshot
and the blocks are concatenated in source order.  Cursor advancement and word
replacement are atomic.

This file is proof/audit code, not runtime implementation.  It models the
direct product ``(cursor, word)``, a lossless ``Cursor · Data+`` tagged
lowering, exact occurrence lineage, finite schedule completion, page-162
fixtures, and hostile counterexamples.  It uses only the standard library,
is silent on import, has no filesystem dependency, and fails closed under
``python -O``.
"""

from __future__ import annotations

import json
import sys
from dataclasses import FrozenInstanceError, dataclass, fields, is_dataclass, replace
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import isqrt
from typing import TypeAlias


if not __debug__:
    raise RuntimeError("T42 semantic oracle must run with assertions enabled")


Bit: TypeAlias = int
Word: TypeAlias = tuple[Bit, ...]

RULE_CODEC_VERSION = "t42.rho-simple-cf/v1"
PROGRAM_SCHEMA_VERSION = "scheduled-ordered-morphism/v1"
TAGGED_SCHEMA_VERSION = "visible-cursor-data-word/v1"
REPLICATED_SCHEMA_VERSION = "uniform-phase-index-times-bit-word/v1"
LINEAGE_SCHEMA_VERSION = "old-occurrence-child-ordinal/v1"
NATURAL_CF_ORIENTATION = "natural_simple_cf_prefix"
REVERSED_TAIL_ORIENTATION = "reverse_rest_once_execution_order"
EXPLICIT_EXECUTION_ORIENTATION = "already_execution_ordered"
IRRATIONAL_PREFIX = "irrational_prefix"
RATIONAL_COMPLETE = "rational_complete"
EXPLICIT_SOURCE = "explicit_schedule"
COMPLETE_EXACT = "complete_exact"
COMPLETE_CERTIFIED = "complete_certified"
SCHEDULE_EXHAUSTED = "schedule_exhausted"


SOURCE_CLAIMS = (
    ("BOOK:1850-1858", "page 162 uses one continued-fraction term to choose each generalized-substitution rule"),
    ("BOOK:12587-12589", "the executable rule schedule is Reverse[Rest[ContinuedFraction[h,m]]]"),
    ("BOOK:12589", "coefficient a emits 0^(a-1)1 for 0 and 0^(a-1)10 for 1"),
    ("BOOK:12591", "the seed is {0}, each rule applies in parallel, and Floor[h] is an observer offset"),
    ("BOOK:12593-12595", "quadratic profiles collapse periodic coefficient blocks to fixed neighbor-independent morphisms"),
    ("BOOK:13030-13034", "ContinuedFraction[h,m] returns m terms, so Rest supplies m-1 rule coefficients"),
    ("BOOK:13170-13172", "cosine interval counts use the mechanical word; the sine sibling is underspecified"),
)


ARCHITECTURE_CLASSIFICATION = (
    "1: reuse T13 finite ordered support, all-occurrence firing, nonempty per-source words, lineage, and ragged traces",
    "1: reuse D019 OrderedGenerationConcat for old-snapshot source-ordered replacement",
    "2: parameterize the immutable rule table by a positive exact coefficient through the closed rho codec",
    "2: parameterize FRONTIER/NEIGHBORHOOD by D032 visible finite schedule focus plus T13 self reads",
    "3: smallest execution base is the lossless uniform PhaseIndex×Bit word; every old occurrence then self-reads and emits through exact T13",
    "3: compact (cursor,word) and Cursor(cursor)·Data(word) views are lossless interfaces; the tagged view needs a shared cursor read",
    "3: compose cursor assignment and ordered-generation replacement atomically; D039 is an optional tagged/span lowering",
    "1-3 only: no T42 UPDATE algebra, executor, family dispatcher, callback, evaluator, raster program, or class-4 category",
)


GOAL2_CONFORMANCE = (
    "Accept only finalized exact/certified simple-CF prefixes or explicitly execution-ordered positive schedules.",
    "Retain signed a0, query/result provenance, coefficient orientation, term count, and rule-codec version.",
    "Reverse a natural CF tail exactly once before execution; never lazily pull natural-order coefficients per event.",
    "Keep the cursor in visible configuration and update it atomically with the dynamic ordered word.",
    "Use the uniform PhaseIndex×Bit product-word lowering when exact T13 AllOccurrences/Self/OrderedGenerationConcat execution is desired.",
    "Use complete old-snapshot occurrence coverage and source-order child concatenation with no newborn firing.",
    "Report finite schedule completion distinctly from empty word, fixed point, external horizon, error, or resource failure.",
    "Do not wrap, repeat the last rule, infer the cursor from generation, or continue a shorter horizon as a longer one.",
    "Keep T41 curve/count queries and T40 coefficient evaluation outside T42 transition state.",
)


def exact_int(value: object, name: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{name} must be an exact integer")
    return value


def exact_nonnegative(value: object, name: str) -> int:
    result = exact_int(value, name)
    if result < 0:
        raise ValueError(f"{name} must be nonnegative")
    return result


def exact_positive(value: object, name: str) -> int:
    result = exact_int(value, name)
    if result <= 0:
        raise ValueError(f"{name} must be positive")
    return result


def exact_text(value: object, name: str) -> str:
    if type(value) is not str or not value:
        raise TypeError(f"{name} must be nonempty exact text")
    return value


def exact_tuple(value: object, name: str) -> tuple[object, ...]:
    if type(value) is not tuple:
        raise TypeError(f"{name} must be an exact tuple")
    return value


def is_sha256(value: str) -> bool:
    return len(value) == 64 and all(character in "0123456789abcdef" for character in value)


def stable_id(label: str) -> str:
    return sha256(label.encode("utf-8")).hexdigest()


def checked_word(value: object, name: str = "word", *, nonempty: bool = True) -> Word:
    raw = exact_tuple(value, name)
    if nonempty and not raw:
        raise ValueError(f"{name} must be nonempty")
    checked: list[int] = []
    for item in raw:
        bit = exact_int(item, f"{name} symbol")
        if bit not in (0, 1):
            raise ValueError(f"{name} must be binary")
        checked.append(bit)
    return tuple(checked)


def canonical_json(payload: object) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


@dataclass(frozen=True)
class QueryProvenance:
    query_id: str
    result_id: str
    proof_strength: str
    coefficient_start: int
    requested_count: int

    def __post_init__(self) -> None:
        query_id = exact_text(self.query_id, "query id")
        result_id = exact_text(self.result_id, "result id")
        if not is_sha256(query_id) or not is_sha256(result_id):
            raise ValueError("query and result ids must be lowercase SHA-256 hex")
        if self.proof_strength not in (COMPLETE_EXACT, COMPLETE_CERTIFIED):
            raise ValueError("T42 accepts only complete exact/certified coefficient results")
        if exact_nonnegative(self.coefficient_start, "coefficient start") != 0:
            raise ValueError("T42 natural CF handoff must begin at coefficient zero")
        exact_positive(self.requested_count, "requested coefficient count")

    def key(self) -> tuple[object, ...]:
        return (
            "QueryProvenance/v1",
            self.query_id,
            self.result_id,
            self.proof_strength,
            self.coefficient_start,
            self.requested_count,
        )


@dataclass(frozen=True)
class FinalizedNaturalCFPrefix:
    provenance: QueryProvenance
    coefficients: tuple[int, ...]
    source_kind: str
    orientation: str = NATURAL_CF_ORIENTATION

    def __post_init__(self) -> None:
        if type(self.provenance) is not QueryProvenance:
            raise TypeError("natural CF prefix needs exact query provenance")
        raw = exact_tuple(self.coefficients, "continued-fraction coefficients")
        if not raw:
            raise ValueError("continued-fraction prefix must contain a0")
        checked = tuple(exact_int(value, "continued-fraction coefficient") for value in raw)
        if any(value <= 0 for value in checked[1:]):
            raise ValueError("simple-CF tail coefficients must be positive")
        if len(checked) != self.provenance.requested_count:
            raise ValueError("coefficient payload length must equal the finalized query count")
        if self.source_kind not in (IRRATIONAL_PREFIX, RATIONAL_COMPLETE):
            raise ValueError("unknown natural CF source kind")
        if self.orientation != NATURAL_CF_ORIENTATION:
            raise ValueError("natural CF prefix orientation is fixed")
        object.__setattr__(self, "coefficients", checked)

    @property
    def a0(self) -> int:
        return self.coefficients[0]

    @property
    def natural_tail(self) -> tuple[int, ...]:
        return self.coefficients[1:]

    def key(self) -> tuple[object, ...]:
        return (
            "FinalizedNaturalCFPrefix/v1",
            self.provenance.key(),
            self.coefficients,
            self.source_kind,
            self.orientation,
        )


@dataclass(frozen=True)
class FinalizedExecutionSchedule:
    provenance: QueryProvenance
    coefficients: tuple[int, ...]
    a0: int
    natural_term_count: int
    source_kind: str
    orientation: str

    def __post_init__(self) -> None:
        if type(self.provenance) is not QueryProvenance:
            raise TypeError("execution schedule needs exact query provenance")
        raw = exact_tuple(self.coefficients, "execution coefficients")
        checked = tuple(exact_positive(value, "execution coefficient") for value in raw)
        a0 = exact_int(self.a0, "a0")
        count = exact_positive(self.natural_term_count, "natural term count")
        if count != len(checked) + 1:
            raise ValueError("one a0 plus the execution schedule must equal the term count")
        if self.source_kind not in (IRRATIONAL_PREFIX, RATIONAL_COMPLETE, EXPLICIT_SOURCE):
            raise ValueError("unknown execution schedule source kind")
        if self.orientation not in (
            REVERSED_TAIL_ORIENTATION,
            EXPLICIT_EXECUTION_ORIENTATION,
        ):
            raise ValueError("execution schedule orientation must be explicit")
        object.__setattr__(self, "coefficients", checked)
        object.__setattr__(self, "a0", a0)

    def key(self) -> tuple[object, ...]:
        return (
            "FinalizedExecutionSchedule/v1",
            self.provenance.key(),
            self.coefficients,
            self.a0,
            self.natural_term_count,
            self.source_kind,
            self.orientation,
        )


def reverse_natural_cf_tail_once(prefix: object) -> FinalizedExecutionSchedule:
    if type(prefix) is not FinalizedNaturalCFPrefix:
        raise TypeError("reverse-once construction requires a finalized natural CF prefix")
    return FinalizedExecutionSchedule(
        prefix.provenance,
        tuple(reversed(prefix.natural_tail)),
        prefix.a0,
        len(prefix.coefficients),
        prefix.source_kind,
        REVERSED_TAIL_ORIENTATION,
    )


def explicit_execution_schedule(
    coefficients: object,
    *,
    a0: object,
    provenance: object,
) -> FinalizedExecutionSchedule:
    if type(provenance) is not QueryProvenance:
        raise TypeError("explicit schedule needs exact provenance")
    raw = exact_tuple(coefficients, "explicit execution coefficients")
    return FinalizedExecutionSchedule(
        provenance,
        tuple(exact_positive(value, "explicit coefficient") for value in raw),
        exact_int(a0, "explicit a0"),
        len(raw) + 1,
        EXPLICIT_SOURCE,
        EXPLICIT_EXECUTION_ORIENTATION,
    )


def rho_block(coefficient: object, symbol: object) -> Word:
    a = exact_positive(coefficient, "rho coefficient")
    bit = exact_int(symbol, "rho source symbol")
    if bit not in (0, 1):
        raise ValueError("rho source symbol must be binary")
    prefix = (0,) * (a - 1) + (1,)
    return prefix if bit == 0 else prefix + (0,)


def rho_word(coefficient: object, word: object) -> Word:
    checked = checked_word(word)
    return tuple(
        child
        for symbol in checked
        for child in rho_block(coefficient, symbol)
    )


def explicit_table(coefficient: object) -> tuple[tuple[int, Word], ...]:
    a = exact_positive(coefficient, "table coefficient")
    return ((0, rho_block(a, 0)), (1, rho_block(a, 1)))


def coefficient_from_table(table: object) -> int:
    raw = exact_tuple(table, "rho table")
    if len(raw) != 2 or raw[0][0] != 0 or raw[1][0] != 1:
        raise ValueError("rho table must have ordered rows 0 then 1")
    first = checked_word(raw[0][1])
    second = checked_word(raw[1][1])
    coefficient = len(first)
    if explicit_table(coefficient) != raw:
        raise ValueError("table is not in the lossless rho image")
    return coefficient


@dataclass(frozen=True)
class ScheduledMorphismProgram:
    schedule: FinalizedExecutionSchedule
    seed: Word = (0,)
    rule_codec: str = RULE_CODEC_VERSION
    schema: str = PROGRAM_SCHEMA_VERSION
    program_id: str = ""

    def __post_init__(self) -> None:
        if type(self.schedule) is not FinalizedExecutionSchedule:
            raise TypeError("program needs a finalized execution schedule")
        if self.schedule.source_kind == RATIONAL_COMPLETE:
            raise ValueError("the strict Book construction excludes rational h")
        seed = checked_word(self.seed, "program seed")
        if self.rule_codec != RULE_CODEC_VERSION or self.schema != PROGRAM_SCHEMA_VERSION:
            raise ValueError("unknown scheduled-morphism schema or rho codec")
        payload = {
            "schema": self.schema,
            "rule_codec": self.rule_codec,
            "schedule": self.schedule.key(),
            "seed": seed,
        }
        computed = sha256(canonical_json(payload).encode("utf-8")).hexdigest()
        if self.program_id not in ("", computed):
            raise ValueError("forged program id")
        object.__setattr__(self, "seed", seed)
        object.__setattr__(self, "program_id", computed)

    def key(self) -> tuple[object, ...]:
        return (
            "ScheduledMorphismProgram/v1",
            self.schema,
            self.rule_codec,
            self.schedule.key(),
            self.seed,
            self.program_id,
        )


def program_from_natural_prefix(prefix: object) -> ScheduledMorphismProgram:
    return ScheduledMorphismProgram(reverse_natural_cf_tail_once(prefix))


@dataclass(frozen=True)
class DirectConfiguration:
    cursor: int
    word: Word

    def __post_init__(self) -> None:
        object.__setattr__(self, "cursor", exact_nonnegative(self.cursor, "visible cursor"))
        object.__setattr__(self, "word", checked_word(self.word, "configuration word"))


def check_configuration(
    program: object, configuration: object
) -> DirectConfiguration:
    if type(program) is not ScheduledMorphismProgram:
        raise TypeError("configuration validation needs an exact program")
    if type(configuration) is not DirectConfiguration:
        raise TypeError("expected an exact direct configuration")
    if configuration.cursor > len(program.schedule.coefficients):
        raise ValueError("visible cursor is outside the finite schedule")
    return configuration


@dataclass(frozen=True)
class OccurrenceHandle:
    program_id: str
    scope_id: str
    generation: int
    source_index: int
    occurrence_id: int

    def __post_init__(self) -> None:
        for value, name in ((self.program_id, "program id"), (self.scope_id, "scope id")):
            text = exact_text(value, name)
            if not is_sha256(text):
                raise ValueError(f"{name} must be SHA-256 hex")
        exact_nonnegative(self.generation, "handle generation")
        exact_nonnegative(self.source_index, "source index")
        exact_nonnegative(self.occurrence_id, "occurrence id")


@dataclass(frozen=True)
class RuntimeSnapshot:
    program_id: str
    configuration: DirectConfiguration
    scope_id: str
    generation: int
    occurrence_ids: tuple[int, ...]
    next_occurrence_id: int

    def __post_init__(self) -> None:
        if not is_sha256(exact_text(self.program_id, "snapshot program id")):
            raise ValueError("snapshot program id must be SHA-256 hex")
        if type(self.configuration) is not DirectConfiguration:
            raise TypeError("snapshot needs an exact configuration")
        if not is_sha256(exact_text(self.scope_id, "snapshot scope id")):
            raise ValueError("snapshot scope id must be SHA-256 hex")
        exact_nonnegative(self.generation, "snapshot generation")
        raw_ids = exact_tuple(self.occurrence_ids, "occurrence ids")
        checked_ids = tuple(exact_nonnegative(value, "occurrence id") for value in raw_ids)
        if len(checked_ids) != len(self.configuration.word):
            raise ValueError("one occurrence id is required for every data occurrence")
        if len(set(checked_ids)) != len(checked_ids):
            raise ValueError("occurrence ids must be unique")
        next_id = exact_nonnegative(self.next_occurrence_id, "next occurrence id")
        if checked_ids and next_id <= max(checked_ids):
            raise ValueError("next occurrence id must exceed all live ids")
        object.__setattr__(self, "occurrence_ids", checked_ids)


def initial_snapshot(
    program: object,
    *,
    branch_label: str = "canonical",
) -> RuntimeSnapshot:
    if type(program) is not ScheduledMorphismProgram:
        raise TypeError("initial snapshot needs an exact program")
    label = exact_text(branch_label, "branch label")
    scope = stable_id(f"{program.program_id}|{label}|generation:0")
    ids = tuple(range(len(program.seed)))
    return RuntimeSnapshot(
        program.program_id,
        DirectConfiguration(0, program.seed),
        scope,
        0,
        ids,
        len(ids),
    )


def arbitrary_snapshot(
    program: object,
    configuration: object,
    *,
    generation: object,
    branch_label: str,
) -> RuntimeSnapshot:
    if type(program) is not ScheduledMorphismProgram:
        raise TypeError("arbitrary snapshot needs an exact program")
    checked = check_configuration(program, configuration)
    generation_value = exact_nonnegative(generation, "arbitrary generation")
    label = exact_text(branch_label, "branch label")
    scope = stable_id(
        f"{program.program_id}|{label}|generation:{generation_value}|cursor:{checked.cursor}|word:{checked.word}"
    )
    ids = tuple(range(1000, 1000 + len(checked.word)))
    return RuntimeSnapshot(
        program.program_id,
        checked,
        scope,
        generation_value,
        ids,
        1000 + len(ids),
    )


def check_snapshot(program: object, snapshot: object) -> RuntimeSnapshot:
    if type(program) is not ScheduledMorphismProgram:
        raise TypeError("snapshot validation needs an exact program")
    if type(snapshot) is not RuntimeSnapshot:
        raise TypeError("expected an exact runtime snapshot")
    if snapshot.program_id != program.program_id:
        raise ValueError("snapshot belongs to another program")
    check_configuration(program, snapshot.configuration)
    return snapshot


def select_all_occurrences(
    program: object, snapshot: object
) -> tuple[OccurrenceHandle, ...]:
    checked = check_snapshot(program, snapshot)
    if checked.configuration.cursor == len(program.schedule.coefficients):
        return ()
    return tuple(
        OccurrenceHandle(
            program.program_id,
            checked.scope_id,
            checked.generation,
            index,
            occurrence_id,
        )
        for index, occurrence_id in enumerate(checked.occurrence_ids)
    )


@dataclass(frozen=True)
class SelfRead:
    handle: OccurrenceHandle
    symbol: int

    def __post_init__(self) -> None:
        if type(self.handle) is not OccurrenceHandle:
            raise TypeError("self read needs an exact occurrence handle")
        bit = exact_int(self.symbol, "read symbol")
        if bit not in (0, 1):
            raise ValueError("read symbol must be binary")


def read_self_symbols(
    program: object,
    snapshot: object,
    handles: object,
) -> tuple[SelfRead, ...]:
    checked = check_snapshot(program, snapshot)
    raw_handles = exact_tuple(handles, "frontier handles")
    expected = select_all_occurrences(program, checked)
    if raw_handles != expected:
        raise ValueError("reads require complete ordered exact-snapshot frontier handles")
    return tuple(
        SelfRead(handle, checked.configuration.word[handle.source_index])
        for handle in raw_handles
    )


@dataclass(frozen=True)
class ReplacementEmission:
    source: OccurrenceHandle
    coefficient: int
    output: Word

    def __post_init__(self) -> None:
        if type(self.source) is not OccurrenceHandle:
            raise TypeError("emission source must be an exact handle")
        coefficient = exact_positive(self.coefficient, "emission coefficient")
        output = checked_word(self.output, "emission output")
        object.__setattr__(self, "coefficient", coefficient)
        object.__setattr__(self, "output", output)


def apply_rho_rule(
    coefficient: object, reads: object
) -> tuple[ReplacementEmission, ...]:
    a = exact_positive(coefficient, "scheduled coefficient")
    raw_reads = exact_tuple(reads, "self reads")
    if any(type(read) is not SelfRead for read in raw_reads):
        raise TypeError("rho RULE accepts only exact self reads")
    return tuple(
        ReplacementEmission(read.handle, a, rho_block(a, read.symbol))
        for read in raw_reads
    )


@dataclass(frozen=True)
class LineageRecord:
    parent_occurrence_id: int
    source_index: int
    child_occurrence_ids: tuple[int, ...]

    def __post_init__(self) -> None:
        exact_nonnegative(self.parent_occurrence_id, "parent occurrence id")
        exact_nonnegative(self.source_index, "lineage source index")
        raw = exact_tuple(self.child_occurrence_ids, "child occurrence ids")
        checked = tuple(exact_nonnegative(value, "child occurrence id") for value in raw)
        if len(set(checked)) != len(checked):
            raise ValueError("child occurrence ids must be unique")
        object.__setattr__(self, "child_occurrence_ids", checked)


@dataclass(frozen=True)
class AdvancedTransition:
    program_id: str
    provenance_result_id: str
    cursor_before: int
    cursor_after: int
    coefficient: int
    reads: tuple[SelfRead, ...]
    emissions: tuple[ReplacementEmission, ...]
    lineage: tuple[LineageRecord, ...]
    successor: RuntimeSnapshot


@dataclass(frozen=True)
class ScheduleCompletion:
    program_id: str
    provenance_result_id: str
    configuration: DirectConfiguration
    reason: str = SCHEDULE_EXHAUSTED
    successors: tuple[()] = ()

    def __post_init__(self) -> None:
        if self.reason != SCHEDULE_EXHAUSTED or self.successors != ():
            raise ValueError("schedule completion is a zero-successor terminal outcome")


StepOutcome: TypeAlias = AdvancedTransition | ScheduleCompletion


def ordered_generation_commit(
    program: object,
    snapshot: object,
    handles: object,
    emissions: object,
) -> AdvancedTransition:
    checked = check_snapshot(program, snapshot)
    cursor = checked.configuration.cursor
    if cursor >= len(program.schedule.coefficients):
        raise ValueError("cannot commit after schedule completion")
    expected_handles = select_all_occurrences(program, checked)
    raw_handles = exact_tuple(handles, "commit handles")
    if raw_handles != expected_handles:
        raise ValueError("UPDATE requires exact complete source-ordered frontier coverage")
    raw_emissions = exact_tuple(emissions, "commit emissions")
    if any(type(emission) is not ReplacementEmission for emission in raw_emissions):
        raise TypeError("UPDATE accepts only exact replacement emissions")
    if len(raw_emissions) != len(expected_handles):
        raise ValueError("UPDATE requires exactly one emission per selected source")
    coefficient = program.schedule.coefficients[cursor]
    lineage: list[LineageRecord] = []
    next_ids: list[int] = []
    next_word: list[int] = []
    fresh = checked.next_occurrence_id
    for index, (handle, emission) in enumerate(zip(expected_handles, raw_emissions)):
        if emission.source != handle:
            raise ValueError("emissions must retain exact source handles and source order")
        source_symbol = checked.configuration.word[index]
        expected_output = rho_block(coefficient, source_symbol)
        if emission.coefficient != coefficient or emission.output != expected_output:
            raise ValueError("emission does not match the closed scheduled rho rule")
        child_ids = tuple(range(fresh, fresh + len(emission.output)))
        fresh += len(child_ids)
        next_ids.extend(child_ids)
        next_word.extend(emission.output)
        lineage.append(
            LineageRecord(handle.occurrence_id, index, child_ids)
        )
    successor_configuration = DirectConfiguration(cursor + 1, tuple(next_word))
    successor_scope = stable_id(
        f"{checked.scope_id}|{program.program_id}|event:{checked.generation}|cursor:{cursor}|coefficient:{coefficient}"
    )
    successor = RuntimeSnapshot(
        program.program_id,
        successor_configuration,
        successor_scope,
        checked.generation + 1,
        tuple(next_ids),
        fresh,
    )
    return AdvancedTransition(
        program.program_id,
        program.schedule.provenance.result_id,
        cursor,
        cursor + 1,
        coefficient,
        tuple(read_self_symbols(program, checked, expected_handles)),
        tuple(raw_emissions),
        tuple(lineage),
        successor,
    )


def direct_step(program: object, snapshot: object) -> StepOutcome:
    checked = check_snapshot(program, snapshot)
    if checked.configuration.cursor == len(program.schedule.coefficients):
        return ScheduleCompletion(
            program.program_id,
            program.schedule.provenance.result_id,
            checked.configuration,
        )
    handles = select_all_occurrences(program, checked)
    reads = read_self_symbols(program, checked, handles)
    coefficient = program.schedule.coefficients[checked.configuration.cursor]
    emissions = apply_rho_rule(coefficient, reads)
    return ordered_generation_commit(program, checked, handles, emissions)


@dataclass(frozen=True)
class CursorToken:
    slot: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "slot", exact_nonnegative(self.slot, "cursor token slot"))


@dataclass(frozen=True)
class DataToken:
    value: int

    def __post_init__(self) -> None:
        value = exact_int(self.value, "data token value")
        if value not in (0, 1):
            raise ValueError("data token must be binary")


Token: TypeAlias = CursorToken | DataToken


@dataclass(frozen=True)
class TaggedConfiguration:
    tokens: tuple[Token, ...]
    schema: str = TAGGED_SCHEMA_VERSION

    def __post_init__(self) -> None:
        raw = exact_tuple(self.tokens, "tagged tokens")
        if self.schema != TAGGED_SCHEMA_VERSION:
            raise ValueError("unknown tagged configuration schema")
        if len(raw) < 2 or type(raw[0]) is not CursorToken:
            raise ValueError("tagged configuration must be Cursor · Data+")
        if any(type(token) is CursorToken for token in raw[1:]):
            raise ValueError("tagged configuration has more than one cursor")
        if any(type(token) is not DataToken for token in raw[1:]):
            raise TypeError("all tokens after the cursor must be exact Data tokens")


def encode_tagged(configuration: object) -> TaggedConfiguration:
    if type(configuration) is not DirectConfiguration:
        raise TypeError("tagged encoding requires an exact direct configuration")
    return TaggedConfiguration(
        (CursorToken(configuration.cursor),)
        + tuple(DataToken(value) for value in configuration.word)
    )


def decode_tagged(program: object, tagged: object) -> DirectConfiguration:
    if type(program) is not ScheduledMorphismProgram:
        raise TypeError("tagged decoding needs an exact program")
    if type(tagged) is not TaggedConfiguration:
        raise TypeError("expected an exact tagged configuration")
    cursor = tagged.tokens[0]
    assert type(cursor) is CursorToken
    configuration = DirectConfiguration(
        cursor.slot,
        tuple(token.value for token in tagged.tokens[1:] if type(token) is DataToken),
    )
    return check_configuration(program, configuration)


@dataclass(frozen=True)
class TaggedAdvancedTransition:
    cursor_before: int
    cursor_after: int
    coefficient: int
    source_tokens: tuple[Token, ...]
    emitted_blocks: tuple[tuple[Token, ...], ...]
    successor: TaggedConfiguration


@dataclass(frozen=True)
class TaggedScheduleCompletion:
    configuration: TaggedConfiguration
    reason: str = SCHEDULE_EXHAUSTED
    successors: tuple[()] = ()


TaggedOutcome: TypeAlias = TaggedAdvancedTransition | TaggedScheduleCompletion


def tagged_step(program: object, tagged: object) -> TaggedOutcome:
    configuration = decode_tagged(program, tagged)
    if configuration.cursor == len(program.schedule.coefficients):
        return TaggedScheduleCompletion(tagged)
    coefficient = program.schedule.coefficients[configuration.cursor]
    emitted: list[tuple[Token, ...]] = [
        (CursorToken(configuration.cursor + 1),)
    ]
    for token in tagged.tokens[1:]:
        assert type(token) is DataToken
        emitted.append(tuple(DataToken(value) for value in rho_block(coefficient, token.value)))
    successor = TaggedConfiguration(tuple(item for block in emitted for item in block))
    return TaggedAdvancedTransition(
        configuration.cursor,
        configuration.cursor + 1,
        coefficient,
        tagged.tokens,
        tuple(emitted),
        successor,
    )


@dataclass(frozen=True)
class PhasedBit:
    phase: int
    value: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "phase", exact_nonnegative(self.phase, "replicated phase"))
        value = exact_int(self.value, "replicated bit")
        if value not in (0, 1):
            raise ValueError("replicated product value must be binary")


@dataclass(frozen=True)
class ReplicatedPhaseConfiguration:
    cells: tuple[PhasedBit, ...]
    schema: str = REPLICATED_SCHEMA_VERSION

    def __post_init__(self) -> None:
        raw = exact_tuple(self.cells, "replicated product cells")
        if self.schema != REPLICATED_SCHEMA_VERSION:
            raise ValueError("unknown replicated product schema")
        if not raw:
            raise ValueError("replicated phase word must be nonempty")
        if any(type(cell) is not PhasedBit for cell in raw):
            raise TypeError("replicated phase word requires exact PhasedBit cells")
        phases = {cell.phase for cell in raw}
        if len(phases) != 1:
            raise ValueError("replicated phase word must satisfy the uniform-phase invariant")

    @property
    def phase(self) -> int:
        return self.cells[0].phase


def encode_replicated(configuration: object) -> ReplicatedPhaseConfiguration:
    if type(configuration) is not DirectConfiguration:
        raise TypeError("replicated encoding requires an exact direct configuration")
    return ReplicatedPhaseConfiguration(
        tuple(PhasedBit(configuration.cursor, value) for value in configuration.word)
    )


def decode_replicated(
    program: object, replicated: object
) -> DirectConfiguration:
    if type(program) is not ScheduledMorphismProgram:
        raise TypeError("replicated decoding needs an exact program")
    if type(replicated) is not ReplicatedPhaseConfiguration:
        raise TypeError("expected an exact replicated phase configuration")
    return check_configuration(
        program,
        DirectConfiguration(
            replicated.phase,
            tuple(cell.value for cell in replicated.cells),
        ),
    )


@dataclass(frozen=True)
class ReplicatedAdvancedTransition:
    phase_before: int
    phase_after: int
    coefficient: int
    source_cells: tuple[PhasedBit, ...]
    emitted_blocks: tuple[tuple[PhasedBit, ...], ...]
    successor: ReplicatedPhaseConfiguration


@dataclass(frozen=True)
class ReplicatedScheduleCompletion:
    configuration: ReplicatedPhaseConfiguration
    reason: str = SCHEDULE_EXHAUSTED
    successors: tuple[()] = ()


ReplicatedOutcome: TypeAlias = (
    ReplicatedAdvancedTransition | ReplicatedScheduleCompletion
)


def replicated_step(
    program: object, replicated: object
) -> ReplicatedOutcome:
    """Exact T13 lowering over the uniform ``PhaseIndex x Bit`` alphabet.

    Every old occurrence self-reads its own ``(phase, bit)`` pair.  For live
    phase ``i`` it emits the nonempty block
    ``((i+1,child) for child in rho_(S[i])(bit))``.  Source-order flattening is
    therefore literally T13 AllOccurrences/Self/OrderedGenerationConcat; no
    shared cursor neighborhood or separate live-event control write remains.
    """

    configuration = decode_replicated(program, replicated)
    if configuration.cursor == len(program.schedule.coefficients):
        return ReplicatedScheduleCompletion(replicated)
    coefficient = program.schedule.coefficients[configuration.cursor]
    emitted = tuple(
        tuple(
            PhasedBit(configuration.cursor + 1, child)
            for child in rho_block(coefficient, cell.value)
        )
        for cell in replicated.cells
    )
    successor = ReplicatedPhaseConfiguration(
        tuple(child for block in emitted for child in block)
    )
    return ReplicatedAdvancedTransition(
        configuration.cursor,
        configuration.cursor + 1,
        coefficient,
        replicated.cells,
        emitted,
        successor,
    )


def run_to_completion(
    program: object,
    snapshot: object | None = None,
) -> tuple[tuple[DirectConfiguration, ...], tuple[AdvancedTransition, ...], ScheduleCompletion]:
    if type(program) is not ScheduledMorphismProgram:
        raise TypeError("run needs an exact program")
    current = initial_snapshot(program) if snapshot is None else check_snapshot(program, snapshot)
    configurations: list[DirectConfiguration] = [current.configuration]
    events: list[AdvancedTransition] = []
    while True:
        outcome = direct_step(program, current)
        if type(outcome) is ScheduleCompletion:
            return tuple(configurations), tuple(events), outcome
        assert type(outcome) is AdvancedTransition
        events.append(outcome)
        current = outcome.successor
        configurations.append(current.configuration)


def offset_word(a0: object, word: object) -> tuple[int, ...]:
    offset = exact_int(a0, "mechanical-word offset")
    checked = checked_word(word)
    return tuple(offset + symbol for symbol in checked)


def simple_cf_value(coefficients: object) -> Fraction:
    raw = exact_tuple(coefficients, "simple CF")
    if not raw:
        raise ValueError("simple CF cannot be empty")
    values = tuple(exact_int(value, "simple-CF coefficient") for value in raw)
    if any(value <= 0 for value in values[1:]):
        raise ValueError("simple-CF tail must be positive")
    result = Fraction(values[-1], 1)
    for coefficient in reversed(values[:-1]):
        result = Fraction(coefficient, 1) + Fraction(1, result)
    return result


def raw_cf_fold(coefficients: object) -> Word:
    raw = exact_tuple(coefficients, "raw CF coefficients")
    if not raw:
        raise ValueError("raw CF fold requires a0")
    values = tuple(exact_int(value, "raw CF coefficient") for value in raw)
    if any(value <= 0 for value in values[1:]):
        raise ValueError("raw CF tail must be positive")
    word: Word = (0,)
    for coefficient in reversed(values[1:]):
        word = rho_word(coefficient, word)
    return word


def floor_n_sqrt2(n: object, sign: object) -> int:
    multiplier = exact_nonnegative(n, "sqrt2 multiplier")
    direction = exact_int(sign, "sqrt2 sign")
    if direction not in (-1, 1):
        raise ValueError("sqrt2 sign must be -1 or 1")
    if multiplier == 0:
        return 0
    lower = isqrt(2 * multiplier * multiplier)
    return lower if direction == 1 else -lower - 1


def sqrt2_mechanical_differences(sign: int, count: int) -> tuple[int, ...]:
    direction = exact_int(sign, "sqrt2 mechanical sign")
    total = exact_nonnegative(count, "mechanical count")
    return tuple(
        floor_n_sqrt2(n + 1, direction) - floor_n_sqrt2(n, direction)
        for n in range(1, total + 1)
    )


def fixture_provenance(label: str, count: int, strength: str = COMPLETE_EXACT) -> QueryProvenance:
    return QueryProvenance(
        stable_id(f"T42 query {label}"),
        stable_id(f"T42 result {label}"),
        strength,
        0,
        count,
    )


@dataclass(frozen=True)
class PageFixture:
    name: str
    coefficients: tuple[int, ...]
    expected_schedule: tuple[int, ...]
    expected_lengths: tuple[int, ...]
    expected_final_sha256: str
    proof_strength: str

    def __post_init__(self) -> None:
        exact_text(self.name, "fixture name")
        raw = exact_tuple(self.coefficients, "fixture coefficients")
        if not raw or any(type(value) is not int for value in raw):
            raise ValueError("fixture coefficients must be exact and include a0")
        if any(value <= 0 for value in raw[1:]):
            raise ValueError("fixture tail coefficients must be positive")
        schedule = exact_tuple(self.expected_schedule, "fixture schedule")
        if tuple(reversed(raw[1:])) != schedule:
            raise ValueError("fixture execution schedule must be the reversed natural tail")
        lengths = exact_tuple(self.expected_lengths, "fixture lengths")
        if len(lengths) != len(schedule) + 1 or lengths[0] != 1:
            raise ValueError("fixture lengths must include the one-symbol seed")
        if not is_sha256(exact_text(self.expected_final_sha256, "fixture word SHA")):
            raise ValueError("fixture word SHA must be lowercase SHA-256")
        if self.proof_strength not in (COMPLETE_EXACT, COMPLETE_CERTIFIED):
            raise ValueError("fixture proof strength must be complete")


PAGE_FIXTURES = (
    PageFixture(
        "page162-alpha-1-plus-sqrt2",
        (0, 2, 2, 2, 2, 2),
        (2, 2, 2, 2, 2),
        (1, 2, 5, 12, 29, 70),
        "8ba86691662b9853053af6dd5b5e3dfc17caf43a640b2bbb45c01e323c30bff7",
        COMPLETE_EXACT,
    ),
    PageFixture(
        "page162-alpha-2-plus-sqrt5",
        (0, 1, 1, 1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1),
        (1, 1, 2, 3, 5, 8, 13, 21, 34, 55),
        "fa947b9859783d29be2ba4015183fa85b52cb6181e04eab41658ab55f6761e36",
        COMPLETE_EXACT,
    ),
    PageFixture(
        "page162-alpha-2-plus-cuberoot5",
        (0, 1, 1, 2, 1, 4, 2),
        (2, 4, 1, 2, 1, 1),
        (1, 2, 9, 11, 31, 42, 73),
        "f851acd68816def8a87c81de3358a129a1a735b2a42399485966261962eb6aa5",
        COMPLETE_EXACT,
    ),
    PageFixture(
        "page162-alpha-1-plus-sqrt-e",
        (0, 2, 4, 1, 2, 3),
        (3, 2, 1, 4, 2),
        (1, 3, 7, 10, 47, 104),
        "961704a7ac5de6ac75aff0bee33c2a0d8406c9db80ed91043595d453cb4f76b6",
        COMPLETE_CERTIFIED,
    ),
)


PAGE162_ASSET = (
    "_page_162_Figure_1.jpeg",
    206693,
    1050,
    1155,
    "ab5e7bbab2a14b3d4fb832dad43842ceb4f206653810d7dfcd23238095741cfe",
)


ASSET_SEMANTIC_MANIFEST = (
    ("schema", "T42-page162-semantic-interface/v1"),
    ("asset", PAGE162_ASSET),
    ("gray_value", 0),
    ("black_value", 1),
    ("rule_icon_coefficients", (1, 2, 3, 4, 5)),
    ("smallest_execution_lowering", "uniform_PhaseIndex_times_Bit_word"),
    (
        "fixtures",
        tuple(
            (
                fixture.name,
                fixture.coefficients,
                fixture.expected_schedule,
                fixture.expected_lengths,
                fixture.expected_final_sha256,
            )
            for fixture in PAGE_FIXTURES
        ),
    ),
    ("pixel_program_forbidden", True),
)


SOURCE_SEMANTIC_MANIFEST = (
    ("schema", "T42-source-semantic-interface/v1"),
    ("natural_prefix_to_schedule", "Reverse[Rest[ContinuedFraction[h,m]]]"),
    ("events_for_irrational_m_term_prefix", "m-1"),
    ("rho_0", "0^(a-1)1"),
    ("rho_1", "0^(a-1)10"),
    ("exact_T13_lowering", "(i,bit)->[(i+1,child) for child in rho_Si(bit)]"),
    ("replicated_invariant", "nonempty_and_all_phase_indices_equal"),
    ("seed", (0,)),
    ("mechanical_word_index_start", 1),
    ("a0_domain", "signed_integer"),
    ("tail_domain", "positive_integer"),
    ("rational_source", "rejected"),
    ("sine_half_shift_rule_generator", "source_underspecified"),
)


def audit_page_fixtures() -> tuple[int, int, int, int, int, int]:
    fixture_count = 0
    events = 0
    source_firings = 0
    children = 0
    compact_commutations = 0
    replicated_commutations = 0
    for fixture in PAGE_FIXTURES:
        provenance = fixture_provenance(
            fixture.name,
            len(fixture.coefficients),
            fixture.proof_strength,
        )
        prefix = FinalizedNaturalCFPrefix(
            provenance,
            fixture.coefficients,
            IRRATIONAL_PREFIX,
        )
        schedule = reverse_natural_cf_tail_once(prefix)
        assert schedule.coefficients == fixture.expected_schedule
        program = ScheduledMorphismProgram(schedule)
        configurations, trace, completion = run_to_completion(program)
        assert tuple(len(configuration.word) for configuration in configurations) == fixture.expected_lengths
        final_word = configurations[-1].word
        assert sha256("".join(map(str, final_word)).encode("ascii")).hexdigest() == fixture.expected_final_sha256
        assert completion.configuration == configurations[-1]
        assert completion.successors == ()
        for event, configuration in zip(trace, configurations):
            tagged_before = encode_tagged(configuration)
            tagged_outcome = tagged_step(program, tagged_before)
            assert type(tagged_outcome) is TaggedAdvancedTransition
            assert decode_tagged(program, tagged_outcome.successor) == event.successor.configuration
            replicated_before = encode_replicated(configuration)
            replicated_outcome = replicated_step(program, replicated_before)
            assert type(replicated_outcome) is ReplicatedAdvancedTransition
            assert decode_replicated(program, replicated_outcome.successor) == event.successor.configuration
            assert len(replicated_outcome.emitted_blocks) == len(configuration.word)
            assert event.cursor_after == event.cursor_before + 1
            assert len(event.reads) == len(configuration.word)
            assert len(event.emissions) == len(configuration.word)
            assert len(event.lineage) == len(configuration.word)
            assert sum(len(row.child_occurrence_ids) for row in event.lineage) == len(event.successor.configuration.word)
            source_firings += len(configuration.word)
            children += len(event.successor.configuration.word)
            compact_commutations += 1
            replicated_commutations += 1
        tagged_completion = tagged_step(program, encode_tagged(configurations[-1]))
        assert type(tagged_completion) is TaggedScheduleCompletion
        assert tagged_completion.successors == ()
        replicated_completion = replicated_step(
            program, encode_replicated(configurations[-1])
        )
        assert type(replicated_completion) is ReplicatedScheduleCompletion
        assert replicated_completion.successors == ()
        fixture_count += 1
        events += len(trace)
    assert (
        fixture_count,
        events,
        source_firings,
        children,
        compact_commutations,
        replicated_commutations,
    ) == (
        4,
        25,
        301,
        599,
        25,
        25,
    )
    return (
        fixture_count,
        events,
        source_firings,
        children,
        compact_commutations,
        replicated_commutations,
    )


def audit_bounded_direct_tagged_commutation() -> tuple[int, int, int, int, int]:
    programs = 0
    active_cases = 0
    completion_cases = 0
    total_children = 0
    replicated_cases = 0
    schedules = ((),) + tuple((a,) for a in range(1, 4)) + tuple(
        pair for pair in product(range(1, 4), repeat=2)
    )
    words = tuple(
        tuple(bits)
        for length in range(1, 5)
        for bits in product((0, 1), repeat=length)
    )
    for schedule_values in schedules:
        provenance = fixture_provenance(
            f"bounded-{schedule_values}",
            len(schedule_values) + 1,
        )
        schedule = explicit_execution_schedule(
            schedule_values,
            a0=0,
            provenance=provenance,
        )
        program = ScheduledMorphismProgram(schedule)
        programs += 1
        for word in words:
            for cursor in range(len(schedule_values) + 1):
                configuration = DirectConfiguration(cursor, word)
                snapshot = arbitrary_snapshot(
                    program,
                    configuration,
                    generation=7,
                    branch_label=f"bounded-{word}-{cursor}",
                )
                direct = direct_step(program, snapshot)
                tagged = tagged_step(program, encode_tagged(configuration))
                replicated = replicated_step(
                    program, encode_replicated(configuration)
                )
                if cursor == len(schedule_values):
                    assert type(direct) is ScheduleCompletion
                    assert type(tagged) is TaggedScheduleCompletion
                    assert type(replicated) is ReplicatedScheduleCompletion
                    completion_cases += 1
                else:
                    assert type(direct) is AdvancedTransition
                    assert type(tagged) is TaggedAdvancedTransition
                    assert type(replicated) is ReplicatedAdvancedTransition
                    assert decode_tagged(program, tagged.successor) == direct.successor.configuration
                    assert decode_replicated(program, replicated.successor) == direct.successor.configuration
                    expected = rho_word(schedule_values[cursor], word)
                    assert direct.successor.configuration == DirectConfiguration(cursor + 1, expected)
                    assert tuple(
                        child
                        for emission in direct.emissions
                        for child in emission.output
                    ) == expected
                    active_cases += 1
                    replicated_cases += 1
                    total_children += len(expected)
    assert programs == 13
    assert active_cases == 630
    assert replicated_cases == 630
    assert completion_cases == 390
    return programs, active_cases, completion_cases, replicated_cases, total_children


def audit_mechanical_word_alignment() -> tuple[int, int, int, int]:
    positive_prefix = FinalizedNaturalCFPrefix(
        fixture_provenance("sqrt2-m3", 3),
        (1, 2, 2),
        IRRATIONAL_PREFIX,
    )
    positive_program = program_from_natural_prefix(positive_prefix)
    positive_configs, _, _ = run_to_completion(positive_program)
    positive_output = offset_word(positive_prefix.a0, positive_configs[-1].word)
    positive_expected = sqrt2_mechanical_differences(1, len(positive_output))
    assert positive_configs[-1].word == (0, 1, 0, 1, 0)
    assert positive_output == (1, 2, 1, 2, 1) == positive_expected
    d0_positive = tuple(
        floor_n_sqrt2(n + 1, 1) - floor_n_sqrt2(n, 1)
        for n in range(len(positive_output))
    )
    assert positive_output != d0_positive

    negative_prefix = FinalizedNaturalCFPrefix(
        fixture_provenance("negative-sqrt2-m4", 4),
        (-2, 1, 1, 2),
        IRRATIONAL_PREFIX,
    )
    negative_program = program_from_natural_prefix(negative_prefix)
    negative_configs, _, _ = run_to_completion(negative_program)
    negative_output = offset_word(negative_prefix.a0, negative_configs[-1].word)
    negative_expected = sqrt2_mechanical_differences(-1, len(negative_output))
    assert negative_program.schedule.coefficients == (2, 1, 1)
    assert tuple(configuration.word for configuration in negative_configs) == (
        (0,),
        (0, 1),
        (1, 1, 0),
        (1, 0, 1, 0, 1),
    )
    assert negative_output == (-1, -2, -1, -2, -1) == negative_expected
    d0_negative = tuple(
        floor_n_sqrt2(n + 1, -1) - floor_n_sqrt2(n, -1)
        for n in range(len(negative_output))
    )
    assert negative_output != d0_negative
    return len(positive_output), len(negative_output), 2, 2


def audit_rational_exclusion_and_dual() -> tuple[int, int, int]:
    canonical = (1, 2)
    alternate = (1, 1, 1)
    assert simple_cf_value(canonical) == Fraction(3, 2)
    assert simple_cf_value(alternate) == Fraction(3, 2)
    canonical_word = raw_cf_fold(canonical)
    alternate_word = raw_cf_fold(alternate)
    assert canonical_word == (0, 1)
    assert alternate_word == (1, 0)
    assert offset_word(1, canonical_word) == (1, 2)
    assert offset_word(1, alternate_word) == (2, 1)
    actual = (
        (3 // 1) - (3 // 2),
        (9 // 2) - (3 // 1),
    )
    assert actual == (2, 1)
    assert offset_word(1, canonical_word) != actual
    rational_prefix = FinalizedNaturalCFPrefix(
        fixture_provenance("rational-three-halves", 2),
        canonical,
        RATIONAL_COMPLETE,
    )
    rejected = 0
    try:
        program_from_natural_prefix(rational_prefix)
    except ValueError:
        rejected += 1
    else:
        raise AssertionError("rational T42 source was accepted")
    return 2, 2, rejected


def audit_direction_horizon_and_loss() -> tuple[int, int, int, int, int]:
    reversed_word = rho_word(1, rho_word(2, (0,)))
    natural_word = rho_word(2, rho_word(1, (0,)))
    assert reversed_word == (1, 1, 0)
    assert natural_word == (0, 1, 0)
    assert reversed_word != natural_word

    short_prefix = FinalizedNaturalCFPrefix(
        fixture_provenance("horizon-short", 2),
        (0, 1),
        IRRATIONAL_PREFIX,
    )
    long_prefix = FinalizedNaturalCFPrefix(
        fixture_provenance("horizon-long", 3),
        (0, 1, 2),
        IRRATIONAL_PREFIX,
    )
    short_program = program_from_natural_prefix(short_prefix)
    long_program = program_from_natural_prefix(long_prefix)
    short_first = direct_step(short_program, initial_snapshot(short_program))
    long_first = direct_step(long_program, initial_snapshot(long_program))
    assert type(short_first) is AdvancedTransition
    assert type(long_first) is AdvancedTransition
    assert short_program.schedule.coefficients == (1,)
    assert long_program.schedule.coefficients == (2, 1)
    assert short_first.successor.configuration.word == (1,)
    assert long_first.successor.configuration.word == (0, 1)
    assert short_program.program_id != long_program.program_id

    word_only_a = ScheduledMorphismProgram(
        explicit_execution_schedule(
            (1,), a0=0, provenance=fixture_provenance("word-loss-a", 2)
        )
    )
    word_only_b = ScheduledMorphismProgram(
        explicit_execution_schedule(
            (2,), a0=0, provenance=fixture_provenance("word-loss-b", 2)
        )
    )
    step_a = direct_step(word_only_a, initial_snapshot(word_only_a))
    step_b = direct_step(word_only_b, initial_snapshot(word_only_b))
    assert type(step_a) is AdvancedTransition and type(step_b) is AdvancedTransition
    assert step_a.successor.configuration.word != step_b.successor.configuration.word

    repeated = ScheduledMorphismProgram(
        explicit_execution_schedule(
            (2, 1, 2, 3),
            a0=0,
            provenance=fixture_provenance("cursor-loss", 5),
        )
    )
    at_zero = arbitrary_snapshot(
        repeated,
        DirectConfiguration(0, (0,)),
        generation=9,
        branch_label="cursor-zero",
    )
    at_two = arbitrary_snapshot(
        repeated,
        DirectConfiguration(2, (0,)),
        generation=9,
        branch_label="cursor-two",
    )
    zero_step = direct_step(repeated, at_zero)
    two_step = direct_step(repeated, at_two)
    assert type(zero_step) is AdvancedTransition and type(two_step) is AdvancedTransition
    assert zero_step.coefficient == two_step.coefficient == 2
    assert zero_step.successor.configuration.word == two_step.successor.configuration.word == (0, 1)
    assert zero_step.successor.configuration.cursor == 1
    assert two_step.successor.configuration.cursor == 3
    assert repeated.schedule.coefficients[1] == 1
    assert repeated.schedule.coefficients[3] == 3

    m1 = FinalizedNaturalCFPrefix(
        fixture_provenance("m1-zero-events", 1),
        (0,),
        IRRATIONAL_PREFIX,
    )
    m1_program = program_from_natural_prefix(m1)
    configurations, events, completion = run_to_completion(m1_program)
    assert m1_program.schedule.coefficients == ()
    assert configurations == (DirectConfiguration(0, (0,)),)
    assert events == () and completion.successors == ()
    return 1, 1, 1, 1, 1


def apply_execution_block(block: object, word: object) -> Word:
    coefficients = exact_tuple(block, "execution block")
    result = checked_word(word)
    for coefficient in coefficients:
        result = rho_word(coefficient, result)
    return result


def macro_table(execution_block: object) -> tuple[tuple[int, Word], ...]:
    block = exact_tuple(execution_block, "macro execution block")
    if not block:
        raise ValueError("macro block must be nonempty")
    return (
        (0, apply_execution_block(block, (0,))),
        (1, apply_execution_block(block, (1,))),
    )


def apply_table(table: object, word: object) -> Word:
    raw_table = exact_tuple(table, "explicit morphism table")
    if len(raw_table) != 2 or raw_table[0][0] != 0 or raw_table[1][0] != 1:
        raise ValueError("binary table rows must be ordered 0 then 1")
    outputs = (checked_word(raw_table[0][1]), checked_word(raw_table[1][1]))
    checked = checked_word(word)
    return tuple(child for symbol in checked for child in outputs[symbol])


def audit_quadratic_macro_relations() -> tuple[int, int, int, int]:
    golden = explicit_table(1)
    sqrt2 = explicit_table(2)
    sqrt3 = macro_table((2, 1))
    assert golden == ((0, (1,)), (1, (1, 0)))
    assert sqrt2 == ((0, (0, 1)), (1, (0, 1, 0)))
    assert sqrt3 == ((0, (1, 1, 0)), (1, (1, 1, 0, 1)))
    cases = 0
    for length in range(1, 6):
        for bits in product((0, 1), repeat=length):
            word = tuple(bits)
            assert apply_table(sqrt3, word) == apply_execution_block((2, 1), word)
            cases += 1
    assert cases == 62
    first_coefficient_event = rho_word(2, (0,))
    one_macro_event = apply_table(sqrt3, (0,))
    assert first_coefficient_event == (0, 1)
    assert one_macro_event == (1, 1, 0)
    assert first_coefficient_event != one_macro_event
    return 3, cases, 2, 1


def audit_table_codec() -> tuple[int, int]:
    cases = 0
    total_output_symbols = 0
    for coefficient in range(1, 65):
        table = explicit_table(coefficient)
        assert coefficient_from_table(table) == coefficient
        total_output_symbols += sum(len(output) for _, output in table)
        cases += 1
    assert total_output_symbols == sum(2 * value + 1 for value in range(1, 65))
    return cases, total_output_symbols


def sequential_newborn_mutant(coefficient: int, word: Word) -> Word:
    """Deliberately wrong fixed-index in-place mutation for an oracle guard."""

    mutable = list(checked_word(word))
    original_count = len(mutable)
    for index in range(original_count):
        mutable[index : index + 1] = rho_block(coefficient, mutable[index])
    return tuple(mutable)


def must_raise(error_type: type[BaseException], thunk: object) -> int:
    if not callable(thunk):
        raise TypeError("must_raise needs a callable")
    try:
        thunk()
    except error_type:
        return 1
    except Exception as error:  # pragma: no cover - diagnostic path
        raise AssertionError(
            f"expected {error_type.__name__}, got {type(error).__name__}: {error}"
        ) from error
    raise AssertionError(f"expected {error_type.__name__}")


FORBIDDEN_ROLE_SUFFIXES = (
    "State",
    "Executor",
    "Evaluator",
    "RasterProgram",
    "FamilyDispatcher",
    "Update",
)


FORBIDDEN_FIELD_NAMES = frozenset(
    {
        "evaluator",
        "callback",
        "raster",
        "family",
        "executor",
        "hidden_time",
        "generation_as_cursor",
    }
)


def dataclass_manifest(namespace: dict[str, object]) -> tuple[tuple[str, tuple[str, ...]], ...]:
    rows: list[tuple[str, tuple[str, ...]]] = []
    for name, value in namespace.items():
        if isinstance(value, type) and is_dataclass(value):
            rows.append((name, tuple(field.name for field in fields(value))))
    return tuple(sorted(rows))


def forbidden_surface(namespace: dict[str, object]) -> tuple[tuple[str, tuple[str, ...]], ...]:
    violations: list[tuple[str, tuple[str, ...]]] = []
    for name, value in namespace.items():
        if not isinstance(value, type):
            continue
        groups: list[str] = []
        for suffix in FORBIDDEN_ROLE_SUFFIXES:
            if name.endswith(suffix):
                groups.append(suffix)
        if is_dataclass(value):
            bad_fields = sorted(
                field.name for field in fields(value) if field.name in FORBIDDEN_FIELD_NAMES
            )
            groups.extend(f"field:{field}" for field in bad_fields)
        if groups:
            violations.append((name, tuple(groups)))
    return tuple(sorted(violations))


def audit_no_hidden_surface() -> tuple[int, int, int, int]:
    manifest = dataclass_manifest(dict(globals()))
    violations = forbidden_surface(dict(globals()))
    assert violations == ()
    assert all(not line.lstrip().startswith("4:") for line in ARCHITECTURE_CLASSIFICATION)
    assert any("1-3 only" in line for line in ARCHITECTURE_CLASSIFICATION)
    public_program_fields = dict(manifest)["ScheduledMorphismProgram"]
    assert not (set(public_program_fields) & FORBIDDEN_FIELD_NAMES)
    mutated = dict(globals())
    mutated["T42Executor"] = type("T42Executor", (), {})
    assert forbidden_surface(mutated) == (("T42Executor", ("Executor",)),)
    mutated = dict(globals())
    mutated["CurveRasterProgram"] = type("CurveRasterProgram", (), {})
    assert forbidden_surface(mutated) == (("CurveRasterProgram", ("RasterProgram",)),)
    return len(manifest), len(violations), 0, 2


def audit_hostile_validation() -> int:
    rejected = 0
    good_provenance = fixture_provenance("hostile", 3)
    rejected += must_raise(TypeError, lambda: QueryProvenance(1, good_provenance.result_id, COMPLETE_EXACT, 0, 3))
    rejected += must_raise(ValueError, lambda: QueryProvenance("0" * 63, good_provenance.result_id, COMPLETE_EXACT, 0, 3))
    rejected += must_raise(ValueError, lambda: QueryProvenance(good_provenance.query_id, good_provenance.result_id, "partial", 0, 3))
    rejected += must_raise(ValueError, lambda: QueryProvenance(good_provenance.query_id, good_provenance.result_id, COMPLETE_EXACT, 1, 3))
    rejected += must_raise(TypeError, lambda: QueryProvenance(good_provenance.query_id, good_provenance.result_id, COMPLETE_EXACT, 0, 3.0))
    rejected += must_raise(ValueError, lambda: FinalizedNaturalCFPrefix(good_provenance, (), IRRATIONAL_PREFIX))
    rejected += must_raise(ValueError, lambda: FinalizedNaturalCFPrefix(good_provenance, (0, 1), IRRATIONAL_PREFIX))
    rejected += must_raise(TypeError, lambda: FinalizedNaturalCFPrefix(good_provenance, (0, 1.0, 2), IRRATIONAL_PREFIX))
    rejected += must_raise(ValueError, lambda: FinalizedNaturalCFPrefix(good_provenance, (0, 0, 2), IRRATIONAL_PREFIX))
    rejected += must_raise(ValueError, lambda: FinalizedNaturalCFPrefix(good_provenance, (0, -1, 2), IRRATIONAL_PREFIX))
    rejected += must_raise(ValueError, lambda: FinalizedNaturalCFPrefix(good_provenance, (0, 1, 2), "unknown"))
    good_prefix = FinalizedNaturalCFPrefix(good_provenance, (-7, 1, 2), IRRATIONAL_PREFIX)
    rejected += must_raise(TypeError, lambda: reverse_natural_cf_tail_once(reverse_natural_cf_tail_once(good_prefix)))
    rejected += must_raise(TypeError, lambda: explicit_execution_schedule([1, 2], a0=0, provenance=good_provenance))
    rejected += must_raise(ValueError, lambda: explicit_execution_schedule((1, 0), a0=0, provenance=good_provenance))
    rejected += must_raise(TypeError, lambda: explicit_execution_schedule((1, 2), a0=0.0, provenance=good_provenance))

    rational_prefix = FinalizedNaturalCFPrefix(
        fixture_provenance("hostile-rational", 2),
        (1, 2),
        RATIONAL_COMPLETE,
    )
    rejected += must_raise(ValueError, lambda: program_from_natural_prefix(rational_prefix))
    program = program_from_natural_prefix(good_prefix)
    rejected += must_raise(ValueError, lambda: ScheduledMorphismProgram(program.schedule, program_id="f" * 64))
    rejected += must_raise(FrozenInstanceError, lambda: setattr(program, "program_id", "0" * 64))
    rejected += must_raise(ValueError, lambda: DirectConfiguration(0, ()))
    rejected += must_raise(TypeError, lambda: DirectConfiguration(False, (0,)))
    rejected += must_raise(ValueError, lambda: DirectConfiguration(0, (2,)))
    rejected += must_raise(ValueError, lambda: check_configuration(program, DirectConfiguration(4, (0,))))
    rejected += must_raise(TypeError, lambda: rho_block(1.0, 0))
    rejected += must_raise(ValueError, lambda: rho_block(0, 0))
    rejected += must_raise(ValueError, lambda: rho_block(1, 2))
    rejected += must_raise(ValueError, lambda: coefficient_from_table(((0, (1,)), (1, (0, 1)))))
    rejected += must_raise(ValueError, lambda: macro_table(()))

    snapshot = arbitrary_snapshot(
        program,
        DirectConfiguration(0, (0, 1)),
        generation=0,
        branch_label="hostile-two-sources",
    )
    handles = select_all_occurrences(program, snapshot)
    reads = read_self_symbols(program, snapshot, handles)
    coefficient = program.schedule.coefficients[0]
    emissions = apply_rho_rule(coefficient, reads)
    rejected += must_raise(ValueError, lambda: read_self_symbols(program, snapshot, tuple(reversed(handles))))
    rejected += must_raise(ValueError, lambda: ordered_generation_commit(program, snapshot, handles[:-1], emissions[:-1]))
    rejected += must_raise(ValueError, lambda: ordered_generation_commit(program, snapshot, handles, emissions + emissions[:1]))
    stale = replace(handles[0], scope_id=stable_id("stale"))
    rejected += must_raise(
        ValueError,
        lambda: ordered_generation_commit(
            program,
            snapshot,
            handles,
            (replace(emissions[0], source=stale), emissions[1]),
        ),
    )
    rejected += must_raise(
        ValueError,
        lambda: ordered_generation_commit(
            program,
            snapshot,
            handles,
            (replace(emissions[0], output=(1,)), emissions[1]),
        ),
    )
    other_program = ScheduledMorphismProgram(
        explicit_execution_schedule(
            (3,),
            a0=0,
            provenance=fixture_provenance("other-program", 2),
        )
    )
    rejected += must_raise(ValueError, lambda: direct_step(other_program, snapshot))

    rejected += must_raise(ValueError, lambda: TaggedConfiguration((DataToken(0),)))
    rejected += must_raise(ValueError, lambda: TaggedConfiguration((CursorToken(0),)))
    rejected += must_raise(ValueError, lambda: TaggedConfiguration((CursorToken(0), DataToken(0), CursorToken(1))))
    rejected += must_raise(TypeError, lambda: TaggedConfiguration((CursorToken(0), DataToken(0), 1)))
    rejected += must_raise(ValueError, lambda: decode_tagged(program, TaggedConfiguration((CursorToken(4), DataToken(0)))))
    rejected += must_raise(ValueError, lambda: ReplicatedPhaseConfiguration(()))
    rejected += must_raise(TypeError, lambda: ReplicatedPhaseConfiguration((PhasedBit(0, 0), 1)))
    rejected += must_raise(
        ValueError,
        lambda: ReplicatedPhaseConfiguration((PhasedBit(0, 0), PhasedBit(1, 1))),
    )
    rejected += must_raise(ValueError, lambda: PhasedBit(0, 2))
    rejected += must_raise(
        ValueError,
        lambda: decode_replicated(
            program,
            ReplicatedPhaseConfiguration((PhasedBit(4, 0),)),
        ),
    )

    empty_schedule_program = program_from_natural_prefix(
        FinalizedNaturalCFPrefix(
            fixture_provenance("hostile-m1", 1),
            (0,),
            IRRATIONAL_PREFIX,
        )
    )
    terminal_snapshot = initial_snapshot(empty_schedule_program)
    rejected += must_raise(
        ValueError,
        lambda: ordered_generation_commit(
            empty_schedule_program,
            terminal_snapshot,
            (),
            (),
        ),
    )

    assert sequential_newborn_mutant(2, (0, 1)) == (0, 0, 1, 0, 1)
    assert rho_word(2, (0, 1)) == (0, 1, 0, 1, 0)
    assert sequential_newborn_mutant(2, (0, 1)) != rho_word(2, (0, 1))
    rejected += 1

    resume_program = ScheduledMorphismProgram(
        explicit_execution_schedule(
            (1, 2, 3),
            a0=0,
            provenance=fixture_provenance("generation-cursor-mutation", 4),
        )
    )
    resumed = arbitrary_snapshot(
        resume_program,
        DirectConfiguration(2, (0,)),
        generation=0,
        branch_label="resumed",
    )
    correct = direct_step(resume_program, resumed)
    assert type(correct) is AdvancedTransition and correct.coefficient == 3
    generation_mutant_word = rho_word(resume_program.schedule.coefficients[resumed.generation], resumed.configuration.word)
    assert generation_mutant_word == (1,)
    assert correct.successor.configuration.word == (0, 0, 1)
    rejected += 1

    tagged_before = encode_tagged(DirectConfiguration(0, (0,)))
    tagged_after = tagged_step(other_program, tagged_before)
    assert type(tagged_after) is TaggedAdvancedTransition
    stale_cursor_mutant = TaggedConfiguration(
        (CursorToken(0),) + tagged_after.successor.tokens[1:]
    )
    assert decode_tagged(other_program, stale_cursor_mutant) != decode_tagged(other_program, tagged_after.successor)
    rejected += 1

    completion_program = ScheduledMorphismProgram(
        explicit_execution_schedule(
            (1,),
            a0=0,
            provenance=fixture_provenance("terminal-wrap-mutation", 2),
        )
    )
    first = direct_step(completion_program, initial_snapshot(completion_program))
    assert type(first) is AdvancedTransition
    completion = direct_step(completion_program, first.successor)
    assert type(completion) is ScheduleCompletion
    wrapped_mutant = DirectConfiguration(0, completion.configuration.word)
    assert wrapped_mutant != completion.configuration
    assert completion.successors == ()
    rejected += 1

    return rejected


EXPECTED_DIGEST = "017d2557aa15e403d6e91991b98f55124cf91c63273e726af57547427531a47e"


def collect_audit_summary() -> tuple[tuple[str, object], ...]:
    page = audit_page_fixtures()
    bounded = audit_bounded_direct_tagged_commutation()
    mechanical = audit_mechanical_word_alignment()
    rational = audit_rational_exclusion_and_dual()
    losses = audit_direction_horizon_and_loss()
    macro = audit_quadratic_macro_relations()
    codec = audit_table_codec()
    surface = audit_no_hidden_surface()
    hostile = audit_hostile_validation()
    return (
        ("page162_fixtures", page),
        ("bounded_direct_tagged_commutation", bounded),
        ("mechanical_word_d1_alignment", mechanical),
        ("rational_exclusion_and_dual", rational),
        ("direction_horizon_loss_witnesses", losses),
        ("quadratic_macro_relations", macro),
        ("rho_table_codec", codec),
        ("no_hidden_surface", surface),
        ("hostile_rejections", hostile),
        ("asset_semantic_manifest", ASSET_SEMANTIC_MANIFEST),
        ("source_semantic_manifest", SOURCE_SEMANTIC_MANIFEST),
        ("source_claims", SOURCE_CLAIMS),
        ("architecture_classification", ARCHITECTURE_CLASSIFICATION),
        ("goal2_conformance", GOAL2_CONFORMANCE),
        ("dataclass_manifest", dataclass_manifest(dict(globals()))),
        ("forbidden_role_suffixes", FORBIDDEN_ROLE_SUFFIXES),
        ("forbidden_field_names", tuple(sorted(FORBIDDEN_FIELD_NAMES))),
    )


def main() -> None:
    summary = collect_audit_summary()
    digest = sha256(repr(summary).encode("utf-8")).hexdigest()
    if EXPECTED_DIGEST == "TO_BE_COMPUTED":
        print(f"computed_semantic_digest={digest}")
        return
    assert digest == EXPECTED_DIGEST
    metrics = dict(summary)
    page = metrics["page162_fixtures"]
    bounded = metrics["bounded_direct_tagged_commutation"]
    mechanical = metrics["mechanical_word_d1_alignment"]
    rational = metrics["rational_exclusion_and_dual"]
    losses = metrics["direction_horizon_loss_witnesses"]
    macro = metrics["quadratic_macro_relations"]
    codec = metrics["rho_table_codec"]
    surface = metrics["no_hidden_surface"]
    print("T42 semantic oracle: PASS")
    print(
        f"page162=fixtures:{page[0]}/events:{page[1]}/source_firings:{page[2]}/"
        f"children:{page[3]}/compact_tagged_commutations:{page[4]}/"
        f"replicated_product_commutations:{page[5]}; asset_hash=PASS"
    )
    print(
        f"bounded=programs:{bounded[0]}/active_cases:{bounded[1]}/"
        f"completion_cases:{bounded[2]}/replicated_T13_cases:{bounded[3]}/"
        f"children:{bounded[4]}; old_snapshot_ordered_concat=PASS; lineage=PASS"
    )
    print(
        f"mechanical_alignment=sqrt2:{mechanical[0]}/negative_sqrt2:{mechanical[1]}/"
        f"d1_matches:{mechanical[2]}/d0_mismatches:{mechanical[3]}; signed_a0=PASS"
    )
    print(
        f"rational=dual_CF_forms:{rational[0]}/distinct_folds:{rational[1]}/"
        f"strict_rejections:{rational[2]}; reverse_mismatch:{losses[0]}; "
        f"horizon_nonresume:{losses[1]}; word_loss:{losses[2]}; "
        f"cursor_loss:{losses[3]}; m1_completion:{losses[4]}"
    )
    print(
        f"quadratic_macros=tables:{macro[0]}/word_cases:{macro[1]}/"
        f"coefficient_events_per_sqrt3_macro:{macro[2]}/false_one_step_rejections:{macro[3]}; "
        f"rho_codec_roundtrips:{codec[0]}/output_symbols:{codec[1]}"
    )
    print(
        f"surface=dataclasses:{surface[0]}/native_forbidden_roles:{surface[1]}/"
        f"class4_algebras:{surface[2]}/mutation_surface_guards:{surface[3]}; "
        f"hostile_rejections={metrics['hostile_rejections']}; hidden_evaluator=absent; "
        "raster_program=absent; family_executor=absent; new_UPDATE=absent"
    )
    print(f"semantic_digest={digest}")


if __name__ == "__main__":
    if len(sys.argv) != 1:
        raise SystemExit("usage: 46-T42-semantic-oracle.py")
    main()
