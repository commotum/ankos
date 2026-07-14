#!/usr/bin/env python3
"""Executable semantic audit for T18 cyclic tag systems.

This is evidence/design verification, not runtime implementation.  It compares
the direct finite-word-plus-phase transition with a lossless tagged-word
lowering through one generic old-snapshot ordered-span UPDATE.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum
from itertools import product
from typing import Iterable, TypeAlias


if not __debug__:
    raise RuntimeError("T18 semantic verification requires assertions; do not run with -O")


Symbol: TypeAlias = int
Word: TypeAlias = tuple[Symbol, ...]


@dataclass(frozen=True)
class BinaryCyclicProgram:
    alphabet: tuple[Symbol, ...]
    blocks: tuple[Word, ...]
    trigger: Symbol

    def __post_init__(self) -> None:
        if not self.alphabet or len(set(self.alphabet)) != len(self.alphabet):
            raise ValueError("alphabet must be finite, nonempty, and duplicate-free")
        if not self.blocks:
            raise ValueError("a cyclic program needs at least one block")
        if self.trigger not in self.alphabet:
            raise ValueError("trigger must belong to the alphabet")
        if any(
            symbol not in self.alphabet
            for block in self.blocks
            for symbol in block
        ):
            raise ValueError("program blocks must be alphabet-closed")


@dataclass(frozen=True)
class DirectState:
    phase: int
    word: Word


class EventKind(Enum):
    ADVANCED = "advanced"
    EMPTY_STUTTER = "empty_stutter"


@dataclass(frozen=True)
class DirectEvent:
    kind: EventKind
    phase_before: int
    phase_after: int
    removed: Symbol | None
    scheduled_block: Word
    appended: Word
    successor: DirectState


def check_direct_state(
    program: BinaryCyclicProgram, state: DirectState
) -> DirectState:
    if state.phase < 0 or state.phase >= len(program.blocks):
        raise ValueError("phase is outside the program cycle")
    if any(symbol not in program.alphabet for symbol in state.word):
        raise ValueError("state word is outside the alphabet")
    return state


def direct_step(
    program: BinaryCyclicProgram, state: DirectState
) -> DirectEvent:
    """Direct model of the Chapter 3/Notes operation."""

    state = check_direct_state(program, state)
    if not state.word:
        return DirectEvent(
            EventKind.EMPTY_STUTTER,
            state.phase,
            state.phase,
            None,
            (),
            (),
            state,
        )

    scheduled = program.blocks[state.phase]
    removed = state.word[0]
    appended = scheduled if removed == program.trigger else ()
    next_state = DirectState(
        (state.phase + 1) % len(program.blocks),
        state.word[1:] + appended,
    )
    return DirectEvent(
        EventKind.ADVANCED,
        state.phase,
        next_state.phase,
        removed,
        scheduled,
        appended,
        next_state,
    )


@dataclass(frozen=True)
class PhaseTag:
    slot: int


@dataclass(frozen=True)
class DataTag:
    value: Symbol


Token: TypeAlias = PhaseTag | DataTag


@dataclass(frozen=True, eq=False)
class SnapshotToken:
    """Opaque address scope; generation is diagnostic metadata only."""

    generation: int

    def __post_init__(self) -> None:
        if self.generation < 0:
            raise ValueError("generation must be nonnegative")


@dataclass(frozen=True)
class OrderedConfiguration:
    """Semantic tagged word plus nonsemantic address/provenance data."""

    tokens: tuple[Token, ...]
    occurrence_ids: tuple[int, ...] = field(compare=False, repr=False)
    next_occurrence_id: int = field(compare=False, repr=False)
    snapshot_token: SnapshotToken = field(compare=False, repr=False)

    def __post_init__(self) -> None:
        if len(self.tokens) != len(self.occurrence_ids):
            raise ValueError("one occurrence ID is required per token")
        if any(identifier < 0 for identifier in self.occurrence_ids):
            raise ValueError("occurrence IDs must be nonnegative")
        if len(set(self.occurrence_ids)) != len(self.occurrence_ids):
            raise ValueError("occurrence IDs must be unique")
        if self.occurrence_ids and self.next_occurrence_id <= max(
            self.occurrence_ids
        ):
            raise ValueError("fresh-ID cursor overlaps existing occurrences")
        if self.next_occurrence_id < 0:
            raise ValueError("fresh-ID cursor must be nonnegative")

    @property
    def generation(self) -> int:
        return self.snapshot_token.generation


def make_configuration(
    tokens: Iterable[Token],
    *,
    generation: int = 0,
    occurrence_ids: tuple[int, ...] | None = None,
    next_occurrence_id: int | None = None,
) -> OrderedConfiguration:
    frozen = tuple(tokens)
    identifiers = (
        tuple(range(len(frozen))) if occurrence_ids is None else occurrence_ids
    )
    cursor = (
        (max(identifiers) + 1 if identifiers else 0)
        if next_occurrence_id is None
        else next_occurrence_id
    )
    return OrderedConfiguration(
        frozen,
        identifiers,
        cursor,
        SnapshotToken(generation),
    )


def validate_tagged(
    program: BinaryCyclicProgram, configuration: OrderedConfiguration
) -> None:
    if not configuration.tokens:
        raise ValueError("tagged cyclic state must retain its phase marker")
    first = configuration.tokens[0]
    if not isinstance(first, PhaseTag):
        raise ValueError("phase marker must be the unique left endpoint")
    if first.slot < 0 or first.slot >= len(program.blocks):
        raise ValueError("phase marker is outside the program cycle")
    for token in configuration.tokens[1:]:
        if not isinstance(token, DataTag):
            raise ValueError("only data tokens may follow the phase marker")
        if token.value not in program.alphabet:
            raise ValueError("data token is outside the program alphabet")


def encode_direct(
    program: BinaryCyclicProgram,
    state: DirectState,
    *,
    generation: int = 0,
) -> OrderedConfiguration:
    """Lossless map e from direct state to tagged ordered support."""

    state = check_direct_state(program, state)
    return make_configuration(
        (PhaseTag(state.phase),)
        + tuple(DataTag(value) for value in state.word),
        generation=generation,
    )


def decode_tagged(
    program: BinaryCyclicProgram, configuration: OrderedConfiguration
) -> DirectState:
    """Explicit inverse of e on the invariant-valid image."""

    validate_tagged(program, configuration)
    marker = configuration.tokens[0]
    assert isinstance(marker, PhaseTag)
    word = tuple(
        token.value
        for token in configuration.tokens[1:]
        if isinstance(token, DataTag)
    )
    return DirectState(marker.slot, word)


@dataclass(frozen=True)
class CyclicSource:
    snapshot_token: SnapshotToken = field(repr=False)
    phase_index: int
    head_index: int
    old_endpoint: int


@dataclass(frozen=True)
class CyclicRead:
    phase: int
    removed: Symbol
    phase_occurrence_id: int
    removed_occurrence_id: int


@dataclass(frozen=True)
class WriteAtom:
    token: Token
    reuse_old_index: int | None = None


@dataclass(frozen=True)
class SpanWrite:
    """One replacement over old half-open coordinates."""

    start: int
    stop: int
    replacement: tuple[WriteAtom, ...]


@dataclass(frozen=True)
class CyclicRuleResult:
    source: CyclicSource
    read: CyclicRead
    phase_after: int
    scheduled_block: Word
    appended: Word
    writes: tuple[SpanWrite, ...]


@dataclass(frozen=True)
class CyclicEvent:
    kind: EventKind
    successor: OrderedConfiguration
    source: CyclicSource | None
    read: CyclicRead | None
    scheduled_block: Word
    appended: Word
    consumed_ids: tuple[int, ...]
    persisted_ids: tuple[int, ...]
    produced_ids: tuple[int, ...]


def select_frontier(
    program: BinaryCyclicProgram, old: OrderedConfiguration
) -> tuple[CyclicSource, ...]:
    validate_tagged(program, old)
    if len(old.tokens) == 1:
        return ()
    return (
        CyclicSource(old.snapshot_token, 0, 1, len(old.tokens)),
    )


def read_neighborhood(
    program: BinaryCyclicProgram,
    old: OrderedConfiguration,
    active: tuple[CyclicSource, ...],
) -> CyclicRead:
    validate_tagged(program, old)
    if len(active) != 1:
        raise ValueError("one cyclic head source is required")
    source = active[0]
    if source.snapshot_token is not old.snapshot_token:
        raise ValueError("stale or foreign source handle")
    if (
        source.phase_index != 0
        or source.head_index != 1
        or source.old_endpoint != len(old.tokens)
        or len(old.tokens) < 2
    ):
        raise ValueError("malformed cyclic source geometry")
    marker = old.tokens[0]
    head = old.tokens[1]
    if not isinstance(marker, PhaseTag) or not isinstance(head, DataTag):
        raise ValueError("source does not address phase plus data head")
    return CyclicRead(
        marker.slot,
        head.value,
        old.occurrence_ids[0],
        old.occurrence_ids[1],
    )


def evaluate_rule(
    program: BinaryCyclicProgram,
    source: CyclicSource,
    read: CyclicRead,
) -> CyclicRuleResult:
    scheduled = program.blocks[read.phase]
    appended = scheduled if read.removed == program.trigger else ()
    phase_after = (read.phase + 1) % len(program.blocks)
    prefix = SpanWrite(
        0,
        2,
        (WriteAtom(PhaseTag(phase_after), reuse_old_index=0),),
    )
    tail = SpanWrite(
        source.old_endpoint,
        source.old_endpoint,
        tuple(WriteAtom(DataTag(value)) for value in appended),
    )
    return CyclicRuleResult(
        source,
        read,
        phase_after,
        scheduled,
        appended,
        (prefix, tail),
    )


def apply_ordered_spans(
    old: OrderedConfiguration, writes: tuple[SpanWrite, ...]
) -> OrderedConfiguration:
    """Generic atomic ordered-span UPDATE used by several constructions."""

    if tuple(sorted(writes, key=lambda write: (write.start, write.stop))) != writes:
        raise ValueError("writes must be in old-coordinate order")
    cursor = 0
    fresh = old.next_occurrence_id
    new_tokens: list[Token] = []
    new_ids: list[int] = []
    reused_indices: set[int] = set()

    for write in writes:
        if (
            write.start < cursor
            or write.stop < write.start
            or write.stop > len(old.tokens)
        ):
            raise ValueError("writes overlap or escape the old snapshot")

        new_tokens.extend(old.tokens[cursor : write.start])
        new_ids.extend(old.occurrence_ids[cursor : write.start])

        for atom in write.replacement:
            new_tokens.append(atom.token)
            if atom.reuse_old_index is None:
                new_ids.append(fresh)
                fresh += 1
            else:
                source_index = atom.reuse_old_index
                if (
                    source_index < write.start
                    or source_index >= write.stop
                    or source_index in reused_indices
                ):
                    raise ValueError("replacement reuses an invalid old occurrence")
                reused_indices.add(source_index)
                new_ids.append(old.occurrence_ids[source_index])
        cursor = write.stop

    new_tokens.extend(old.tokens[cursor:])
    new_ids.extend(old.occurrence_ids[cursor:])
    return make_configuration(
        tuple(new_tokens),
        generation=old.generation + 1,
        occurrence_ids=tuple(new_ids),
        next_occurrence_id=fresh,
    )


def apply_update(
    program: BinaryCyclicProgram,
    old: OrderedConfiguration,
    active: tuple[CyclicSource, ...],
    result: CyclicRuleResult | None,
) -> CyclicEvent:
    validate_tagged(program, old)
    if not active:
        if len(old.tokens) != 1 or result is not None:
            raise ValueError("empty-source policy applies only to empty data words")
        successor = apply_ordered_spans(old, ())
        validate_tagged(program, successor)
        return CyclicEvent(
            EventKind.EMPTY_STUTTER,
            successor,
            None,
            None,
            (),
            (),
            (),
            old.occurrence_ids,
            (),
        )

    read = read_neighborhood(program, old, active)
    expected = evaluate_rule(program, active[0], read)
    if result != expected:
        raise ValueError("rule result is stale, incomplete, or tampered")
    successor = apply_ordered_spans(old, result.writes)
    validate_tagged(program, successor)

    suffix_count = len(old.tokens) - 2
    if successor.occurrence_ids[0] != old.occurrence_ids[0]:
        raise ValueError("phase-marker occurrence identity was not preserved")
    persisted = successor.occurrence_ids[1 : 1 + suffix_count]
    if persisted != old.occurrence_ids[2:]:
        raise ValueError("old suffix occurrence order was not preserved")
    produced = successor.occurrence_ids[1 + suffix_count :]
    if len(produced) != len(result.appended):
        raise ValueError("append provenance does not match the appendant")
    if any(identifier in old.occurrence_ids for identifier in produced):
        raise ValueError("appended occurrences were not freshly allocated")

    return CyclicEvent(
        EventKind.ADVANCED,
        successor,
        active[0],
        read,
        result.scheduled_block,
        result.appended,
        (old.occurrence_ids[1],),
        old.occurrence_ids[2:],
        produced,
    )


def generic_step(
    program: BinaryCyclicProgram, old: OrderedConfiguration
) -> CyclicEvent:
    active = select_frontier(program, old)
    if not active:
        return apply_update(program, old, active, None)
    read = read_neighborhood(program, old, active)
    result = evaluate_rule(program, active[0], read)
    return apply_update(program, old, active, result)


CANONICAL_PROGRAM = BinaryCyclicProgram(
    alphabet=(0, 1),
    blocks=((1, 1), (1, 0)),
    trigger=1,
)

EXPECTED_CANONICAL_TRACE: tuple[DirectState, ...] = (
    DirectState(0, (1,)),
    DirectState(1, (1, 1)),
    DirectState(0, (1, 1, 0)),
    DirectState(1, (1, 0, 1, 1)),
    DirectState(0, (0, 1, 1, 1, 0)),
    DirectState(1, (1, 1, 1, 0)),
    DirectState(0, (1, 1, 0, 1, 0)),
    DirectState(1, (1, 0, 1, 0, 1, 1)),
    DirectState(0, (0, 1, 0, 1, 1, 1, 0)),
    DirectState(1, (1, 0, 1, 1, 1, 0)),
    DirectState(0, (0, 1, 1, 1, 0, 1, 0)),
    DirectState(1, (1, 1, 1, 0, 1, 0)),
    DirectState(0, (1, 1, 0, 1, 0, 1, 0)),
)


def direct_trace(
    program: BinaryCyclicProgram, seed: DirectState, steps: int
) -> tuple[DirectState, ...]:
    states = [check_direct_state(program, seed)]
    for _ in range(steps):
        states.append(direct_step(program, states[-1]).successor)
    return tuple(states)


def generic_trace(
    program: BinaryCyclicProgram, seed: DirectState, steps: int
) -> tuple[DirectState, ...]:
    configuration = encode_direct(program, seed)
    states = [decode_tagged(program, configuration)]
    for _ in range(steps):
        configuration = generic_step(program, configuration).successor
        states.append(decode_tagged(program, configuration))
    return tuple(states)


def words_through(
    alphabet: tuple[Symbol, ...], maximum_length: int
) -> tuple[Word, ...]:
    return tuple(
        tuple(word)
        for length in range(maximum_length + 1)
        for word in product(alphabet, repeat=length)
    )


def assert_bounded_commutation() -> dict[str, int]:
    alphabet = (0, 1)
    blocks = words_through(alphabet, 2)
    words = words_through(alphabet, 5)
    program_count = 0
    case_count = 0
    empty_cases = 0
    append_cases = 0
    no_append_cases = 0

    for cycle_length in (1, 2, 3):
        for raw_blocks in product(blocks, repeat=cycle_length):
            program = BinaryCyclicProgram(alphabet, tuple(raw_blocks), 1)
            program_count += 1
            for phase in range(cycle_length):
                for word in words:
                    state = DirectState(phase, word)
                    assert decode_tagged(program, encode_direct(program, state)) == state
                    direct = direct_step(program, state)
                    old = encode_direct(program, state)
                    generic = generic_step(program, old)
                    assert decode_tagged(program, generic.successor) == direct.successor
                    assert generic.kind is direct.kind
                    assert generic.successor.snapshot_token is not old.snapshot_token
                    assert generic.successor.generation == old.generation + 1
                    assert generic.successor.occurrence_ids[0] == old.occurrence_ids[0]

                    if not word:
                        empty_cases += 1
                        assert generic.source is None
                        assert generic.consumed_ids == ()
                        assert generic.persisted_ids == old.occurrence_ids
                        assert generic.produced_ids == ()
                    else:
                        assert generic.source is not None
                        assert generic.read is not None
                        assert generic.read.phase == phase
                        assert generic.read.removed == word[0]
                        assert generic.scheduled_block == raw_blocks[phase]
                        assert generic.appended == direct.appended
                        assert generic.consumed_ids == (old.occurrence_ids[1],)
                        assert generic.persisted_ids == old.occurrence_ids[2:]
                        if direct.appended:
                            append_cases += 1
                        else:
                            no_append_cases += 1
                    case_count += 1

    assert program_count == 399
    assert case_count == 71_442
    assert empty_cases == 1_134
    assert append_cases + no_append_cases == case_count - empty_cases
    return {
        "programs": program_count,
        "cases": case_count,
        "empty_cases": empty_cases,
        "append_cases": append_cases,
        "no_append_cases": no_append_cases,
    }


def assert_t17_shared_ordered_update() -> int:
    """T17 delete-prefix/tail-append uses the same generic span committer."""

    cases = 0
    appendants = words_through((0, 1), 2)
    for word in words_through((0, 1), 5):
        if not word:
            continue
        old = make_configuration(tuple(DataTag(value) for value in word))
        for deletion in range(1, len(word) + 1):
            for appendant in appendants:
                writes = (
                    SpanWrite(0, deletion, ()),
                    SpanWrite(
                        len(word),
                        len(word),
                        tuple(WriteAtom(DataTag(value)) for value in appendant),
                    ),
                )
                successor = apply_ordered_spans(old, writes)
                values = tuple(
                    token.value
                    for token in successor.tokens
                    if isinstance(token, DataTag)
                )
                assert values == word[deletion:] + appendant
                assert successor.occurrence_ids[: len(word) - deletion] == (
                    old.occurrence_ids[deletion:]
                )
                produced = successor.occurrence_ids[len(word) - deletion :]
                assert len(produced) == len(appendant)
                assert not set(produced).intersection(old.occurrence_ids)
                cases += 1
    assert cases == 1_806
    return cases


@dataclass(frozen=True)
class MultiplicityProgram:
    blocks: tuple[Word, ...]

    def __post_init__(self) -> None:
        if not self.blocks:
            raise ValueError("multiplicity program needs at least one block")
        if any(value < 0 for block in self.blocks for value in block):
            raise ValueError("multiplicity data must be nonnegative")


def multiplicity_step(
    program: MultiplicityProgram, state: DirectState
) -> DirectState:
    if state.phase < 0 or state.phase >= len(program.blocks):
        raise ValueError("phase is outside the program cycle")
    if any(value < 0 for value in state.word):
        raise ValueError("multiplicity state must contain natural values")
    if not state.word:
        return state
    removed = state.word[0]
    block = program.blocks[state.phase]
    return DirectState(
        (state.phase + 1) % len(program.blocks),
        state.word[1:] + block * removed,
    )


def assert_multiplicity_generalization() -> int:
    program = MultiplicityProgram(((1, 0), (2,), ()))
    fixtures = (
        (DirectState(0, (2, 3)), DirectState(1, (3, 1, 0, 1, 0))),
        (DirectState(1, (0, 2)), DirectState(2, (2,))),
        (DirectState(2, (4, 1)), DirectState(0, (1,))),
        (DirectState(1, ()), DirectState(1, ())),
    )
    for old, expected in fixtures:
        assert multiplicity_step(program, old) == expected

    cases = 0
    for phase in range(len(program.blocks)):
        for length in range(4):
            for word in product(range(4), repeat=length):
                state = DirectState(phase, tuple(word))
                direct = multiplicity_step(program, state)
                tokens = (PhaseTag(phase),) + tuple(
                    DataTag(value) for value in state.word
                )
                old = make_configuration(tokens)
                if not state.word:
                    successor = apply_ordered_spans(old, ())
                else:
                    removed = state.word[0]
                    appended = program.blocks[phase] * removed
                    writes = (
                        SpanWrite(
                            0,
                            2,
                            (
                                WriteAtom(
                                    PhaseTag((phase + 1) % len(program.blocks)),
                                    reuse_old_index=0,
                                ),
                            ),
                        ),
                        SpanWrite(
                            len(tokens),
                            len(tokens),
                            tuple(
                                WriteAtom(DataTag(value))
                                for value in appended
                            ),
                        ),
                    )
                    successor = apply_ordered_spans(old, writes)
                decoded = DirectState(
                    successor.tokens[0].slot
                    if isinstance(successor.tokens[0], PhaseTag)
                    else -1,
                    tuple(
                        token.value
                        for token in successor.tokens[1:]
                        if isinstance(token, DataTag)
                    ),
                )
                assert decoded == direct
                cases += 1
    assert cases == 255
    return cases


def expect_value_error(thunk, message: str) -> None:
    try:
        thunk()
    except ValueError:
        pass
    else:
        raise AssertionError(message)


def assert_adversaries() -> None:
    phase_program = BinaryCyclicProgram((0, 1), ((1,), (0,)), 1)
    phase_zero = direct_step(phase_program, DirectState(0, (1,))).successor
    phase_one = direct_step(phase_program, DirectState(1, (1,))).successor
    assert phase_zero.word == (1,)
    assert phase_one.word == (0,)
    assert phase_zero != phase_one

    false_trigger = direct_step(
        CANONICAL_PROGRAM, DirectState(0, (0, 1))
    )
    true_trigger = direct_step(
        CANONICAL_PROGRAM, DirectState(0, (1, 0))
    )
    assert false_trigger.appended == ()
    assert false_trigger.successor == DirectState(1, (1,))
    assert true_trigger.appended == (1, 1)
    assert true_trigger.successor == DirectState(1, (0, 1, 1))

    three = BinaryCyclicProgram((0, 1), ((0,), (1,), (1, 0)), 1)
    assert direct_trace(three, DirectState(2, (1,)), 3) == (
        DirectState(2, (1,)),
        DirectState(0, (1, 0)),
        DirectState(1, (0, 0)),
        DirectState(2, (0,)),
    )

    extinction_program = BinaryCyclicProgram((0, 1), ((), (1,)), 1)
    old = encode_direct(extinction_program, DirectState(0, (0,)), generation=4)
    extinction = generic_step(extinction_program, old)
    assert extinction.kind is EventKind.ADVANCED
    assert decode_tagged(extinction_program, extinction.successor) == DirectState(
        1, ()
    )
    assert extinction.consumed_ids == (old.occurrence_ids[1],)
    empty = generic_step(extinction_program, extinction.successor)
    assert empty.kind is EventKind.EMPTY_STUTTER
    assert decode_tagged(extinction_program, empty.successor) == DirectState(1, ())
    assert empty.successor == extinction.successor
    assert empty.successor.snapshot_token is not extinction.successor.snapshot_token

    one_block = BinaryCyclicProgram((0, 1), ((1,),), 1)
    one = generic_step(one_block, encode_direct(one_block, DirectState(0, (1,))))
    assert decode_tagged(one_block, one.successor).phase == 0

    old = encode_direct(phase_program, DirectState(0, (1, 0)), generation=7)
    active = select_frontier(phase_program, old)
    read = read_neighborhood(phase_program, old, active)
    valid = evaluate_rule(phase_program, active[0], read)

    peer = encode_direct(phase_program, DirectState(0, (1, 0)), generation=7)
    foreign = select_frontier(phase_program, peer)
    assert foreign[0].snapshot_token is not old.snapshot_token
    expect_value_error(
        lambda: read_neighborhood(phase_program, old, foreign),
        "same-generation foreign source was accepted",
    )

    prior = encode_direct(phase_program, DirectState(0, (1, 0)), generation=6)
    stale = select_frontier(phase_program, prior)
    expect_value_error(
        lambda: read_neighborhood(phase_program, old, stale),
        "stale source was accepted",
    )

    successor = apply_update(phase_program, old, active, valid).successor
    expect_value_error(
        lambda: read_neighborhood(phase_program, successor, active),
        "old handle was accepted by successor",
    )

    wrong_phase = replace(
        valid.writes[0],
        replacement=(WriteAtom(PhaseTag(0), reuse_old_index=0),),
    )
    bad_results = (
        replace(valid, writes=(valid.writes[0],)),
        replace(valid, writes=(wrong_phase, valid.writes[1])),
        replace(
            valid,
            writes=(
                valid.writes[0],
                replace(valid.writes[1], start=1, stop=1),
            ),
        ),
        replace(valid, appended=()),
    )
    for bad in bad_results:
        expect_value_error(
            lambda bad=bad: apply_update(phase_program, old, active, bad),
            "tampered cyclic rule result was accepted",
        )

    expect_value_error(
        lambda: validate_tagged(
            phase_program,
            make_configuration((DataTag(1), PhaseTag(0))),
        ),
        "phase marker outside the left endpoint was accepted",
    )
    expect_value_error(
        lambda: validate_tagged(
            phase_program,
            make_configuration((PhaseTag(0), PhaseTag(1))),
        ),
        "duplicate phase marker was accepted",
    )
    expect_value_error(
        lambda: validate_tagged(
            phase_program,
            make_configuration((PhaseTag(2), DataTag(1))),
        ),
        "out-of-range phase marker was accepted",
    )
    expect_value_error(
        lambda: BinaryCyclicProgram((0, 1), (), 1),
        "empty program cycle was accepted",
    )


def serialize_program(program: BinaryCyclicProgram) -> dict[str, object]:
    return {
        "alphabet": list(program.alphabet),
        "blocks": [list(block) for block in program.blocks],
        "trigger": program.trigger,
    }


def deserialize_program(payload: dict[str, object]) -> BinaryCyclicProgram:
    raw_alphabet = payload["alphabet"]
    raw_blocks = payload["blocks"]
    trigger = payload["trigger"]
    if not isinstance(raw_alphabet, list) or not isinstance(raw_blocks, list):
        raise ValueError("malformed program payload")
    if not isinstance(trigger, int):
        raise ValueError("malformed trigger")
    if any(not isinstance(block, list) for block in raw_blocks):
        raise ValueError("malformed block payload")
    return BinaryCyclicProgram(
        tuple(int(value) for value in raw_alphabet),
        tuple(tuple(int(value) for value in block) for block in raw_blocks),
        trigger,
    )


def serialize_state(state: DirectState) -> dict[str, object]:
    return {"phase": state.phase, "word": list(state.word)}


def deserialize_state(payload: dict[str, object]) -> DirectState:
    phase = payload["phase"]
    word = payload["word"]
    if not isinstance(phase, int) or not isinstance(word, list):
        raise ValueError("malformed state payload")
    return DirectState(phase, tuple(int(value) for value in word))


def assert_serialization() -> None:
    program = deserialize_program(serialize_program(CANONICAL_PROGRAM))
    assert program == CANONICAL_PROGRAM
    for state in EXPECTED_CANONICAL_TRACE:
        decoded = deserialize_state(serialize_state(state))
        assert decoded == state
        assert direct_step(program, decoded) == direct_step(
            CANONICAL_PROGRAM, state
        )
    assert serialize_state(DirectState(1, (1,))) != serialize_state(
        DirectState(0, (1,))
    )


@dataclass(frozen=True)
class DecisionRow:
    decision: str
    classification: int
    smallest_base: str
    action: str
    reason: str


DECISION_MATRIX = (
    DecisionRow(
        "D024",
        2,
        "typed construction-specific outcome",
        "ADD_EMPTY_STUTTER_WITNESS",
        "the explicit empty clause has one identity successor and frozen phase",
    ),
    DecisionRow(
        "D027",
        2,
        "anchored prefix-consume and old-end append schedule",
        "REUSE",
        "data-tail order and conditional appendant are unchanged",
    ),
    DecisionRow(
        "D028",
        2,
        "epsilon-capable private word and edit carriers",
        "REUSE",
        "scheduled blocks and conditional appendants may be empty",
    ),
    DecisionRow(
        "D029",
        2,
        "typed outcome envelope",
        "KEEP_T17_TERMINAL",
        "T18 empty stutter does not broaden T17 InsufficientPrefix",
    ),
    DecisionRow(
        "D032",
        3,
        "visible marker or named configuration factor",
        "REUSE_VISIBLE_CONTROL_ROLE",
        "the cyclic focus is state, not executor time",
    ),
    DecisionRow(
        "D039",
        3,
        "generic atomic ordered multi-span replacement",
        "REUSE",
        "phase/head prefix replacement and old-end insertion are disjoint spans",
    ),
    DecisionRow(
        "D126",
        3,
        "tagged Phase(slot) followed by Data(word)",
        "ADD_T18_PRESET",
        "lossless tagged state and validation add no execution algebra",
    ),
)


def assert_decision_matrix() -> None:
    assert tuple(row.decision for row in DECISION_MATRIX) == (
        "D024",
        "D027",
        "D028",
        "D029",
        "D032",
        "D039",
        "D126",
    )
    assert tuple(row.classification for row in DECISION_MATRIX) == (
        2,
        2,
        2,
        2,
        3,
        3,
        3,
    )
    assert all("executor" not in row.smallest_base.lower() for row in DECISION_MATRIX)
    assert all(row.classification != 4 for row in DECISION_MATRIX)


def main() -> None:
    assert direct_trace(CANONICAL_PROGRAM, DirectState(0, (1,)), 12) == (
        EXPECTED_CANONICAL_TRACE
    )
    assert generic_trace(CANONICAL_PROGRAM, DirectState(0, (1,)), 12) == (
        EXPECTED_CANONICAL_TRACE
    )
    bounded = assert_bounded_commutation()
    t17_cases = assert_t17_shared_ordered_update()
    multiplicity_cases = assert_multiplicity_generalization()
    assert_adversaries()
    assert_serialization()
    assert_decision_matrix()
    print(
        "T18 semantic oracle: PASS "
        f"(bounded_programs={bounded['programs']}; "
        f"commutation_cases={bounded['cases']}; "
        f"empty_stutter_cases={bounded['empty_cases']}; "
        f"append_cases={bounded['append_cases']}; "
        f"no_append_cases={bounded['no_append_cases']}; "
        f"shared_T17_update_cases={t17_cases}; "
        f"multiplicity_cases={multiplicity_cases}; "
        "canonical_t0_t12=PASS; visible_phase=PASS; "
        "tagged_inverse=PASS; opaque_snapshot_identity=PASS; "
        "phase_head_tail_atomic=PASS; extinction_then_stutter=PASS; "
        "shared_ordered_multispan_UPDATE=PASS; serialization=PASS; "
        "decision_matrix=PASS)"
    )


if __name__ == "__main__":
    main()
