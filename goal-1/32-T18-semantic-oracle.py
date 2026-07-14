#!/usr/bin/env python3
"""Executable semantic audit for T18 cyclic tag systems.

This is evidence/design verification, not runtime implementation.  It compares
the direct finite-word-plus-phase transition with a lossless tagged-word
lowering through one generic old-snapshot ordered-span UPDATE.
"""

from __future__ import annotations

import hashlib
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
        if self.alphabet != (0, 1) or self.trigger != 1:
            raise ValueError("the strict Chapter 3 preset is binary with trigger 1")
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


def rotated_rule_value(
    program: BinaryCyclicProgram, state: DirectState
) -> tuple[Word, ...]:
    """Literal Notes-style visible schedule value for the named-slot state."""

    check_direct_state(program, state)
    return program.blocks[state.phase :] + program.blocks[: state.phase]


def notes_value_projection(
    program: BinaryCyclicProgram, state: DirectState
) -> tuple[tuple[Word, ...], Word]:
    """Projection to the Notes pair {rotated rule values, finite word}."""

    return rotated_rule_value(program, state), state.word


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


def read_neighborhoods(
    program: BinaryCyclicProgram,
    old: OrderedConfiguration,
    active: tuple[CyclicSource, ...],
) -> tuple[CyclicRead, ...]:
    """Collection-shaped access used by the branch-free runner protocol."""

    validate_tagged(program, old)
    if not active:
        if len(old.tokens) != 1:
            raise ValueError("an empty frontier is valid only for an empty data word")
        return ()
    return (read_neighborhood(program, old, active),)


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


def evaluate_rules(
    program: BinaryCyclicProgram,
    active: tuple[CyclicSource, ...],
    reads: tuple[CyclicRead, ...],
) -> tuple[CyclicRuleResult, ...]:
    """Collection-shaped RULE evaluation; empty input produces empty writes."""

    if len(active) != len(reads):
        raise ValueError("one read is required for each cyclic source")
    return tuple(
        evaluate_rule(program, source, read)
        for source, read in zip(active, reads, strict=True)
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
    results: tuple[CyclicRuleResult, ...],
) -> CyclicEvent:
    validate_tagged(program, old)
    if not active:
        if len(old.tokens) != 1 or results:
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

    if len(results) != 1:
        raise ValueError("one cyclic result is required for the live source")
    result = results[0]
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
    reads = read_neighborhoods(program, old, active)
    writes = evaluate_rules(program, active, reads)
    return apply_update(program, old, active, writes)


CANONICAL_PROGRAM = BinaryCyclicProgram(
    alphabet=(0, 1),
    blocks=((1, 1), (1, 0)),
    trigger=1,
)

BOOK_PAGE_95_ROWS = (
    "1",
    "11",
    "110",
    "1011",
    "01110",
    "1110",
    "11010",
    "101011",
    "0101110",
    "101110",
    "0111010",
    "111010",
    "1101010",
    "10101011",
    "010101110",
    "10101110",
    "010111010",
    "10111010",
    "011101010",
    "11101010",
    "110101010",
    "1010101011",
    "01010101110",
    "1010101110",
    "01010111010",
)
EXPECTED_CANONICAL_TRACE: tuple[DirectState, ...] = tuple(
    DirectState(index % 2, tuple(int(bit) for bit in row))
    for index, row in enumerate(BOOK_PAGE_95_ROWS)
)

# Independent semantic copies of the five page-96 native profiles.  The asset
# oracle separately hash-binds their raster transcription; this oracle proves
# that both the direct and shared tagged execution paths generate it.
BOOK_PAGE_96_PROGRAMS = {
    "a": BinaryCyclicProgram((0, 1), ((1, 1), (1, 0)), 1),
    "b": BinaryCyclicProgram((0, 1), ((1,), (1, 1)), 1),
    "c": BinaryCyclicProgram((0, 1), ((1, 0), (1, 1)), 1),
    "d": BinaryCyclicProgram((0, 1), ((1,), (1, 0, 1)), 1),
    "e": BinaryCyclicProgram((0, 1), ((1, 1, 1), (0,)), 1),
}
BOOK_PAGE_96_FINAL_ROWS = {
    "a": "10101010101110101010",
    "b": "11111111111111111111111111111111111111111111111111",
    "c": "11101110111110111110111011111011111011101111101110111110111110",
    "d": "110110111011011110111011011101101111011110111011011",
    "e": "001110011101110111011100111001110111011111101111110111",
}
BOOK_PAGE_96_TRACE_SHA256 = {
    "a": "c9d9199aacac4298a05c9810d19654aa45ff1193067e636c3361cf4f87e21e79",
    "b": "d9a237a460cccbcd90bddc1b47a204b03f7a03941be3fc43388a0af9ae4966ef",
    "c": "adadc131e58c22729fc2651a1989d2fd5fae618cb402807f93e1b7648cbfe019",
    "d": "b7d44cb49a4fa6c6e84564e93ff29f85e12bce9eedc8ba1c6cb5324a4c29577a",
    "e": "024da84c4d9e88aa4af7c6e2ef7441b805af16708be7f2157ec4ffdfabd4cfc1",
}


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


def word_rows(states: tuple[DirectState, ...]) -> tuple[str, ...]:
    return tuple("".join(map(str, state.word)) for state in states)


def word_trace_digest(states: tuple[DirectState, ...]) -> str:
    payload = "\n".join(word_rows(states)) + "\n"
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def assert_book_fixtures() -> int:
    cases = 0
    for name, program in BOOK_PAGE_96_PROGRAMS.items():
        direct = direct_trace(program, DirectState(0, (1,)), 99)
        generic = generic_trace(program, DirectState(0, (1,)), 99)
        assert direct == generic
        assert word_rows(direct)[-1] == BOOK_PAGE_96_FINAL_ROWS[name]
        assert word_trace_digest(direct) == BOOK_PAGE_96_TRACE_SHA256[name]
        assert tuple(state.phase for state in direct) == tuple(
            index % 2 for index in range(100)
        )
        assert all(state.word for state in direct)
        cases += len(direct)
    assert cases == 500
    return cases


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
        if any(
            not isinstance(value, int) or isinstance(value, bool) or value < 0
            for block in self.blocks
            for value in block
        ):
            raise ValueError("multiplicity data must be nonnegative")


def multiplicity_step(
    program: MultiplicityProgram, state: DirectState
) -> DirectState:
    if state.phase < 0 or state.phase >= len(program.blocks):
        raise ValueError("phase is outside the program cycle")
    if any(
        not isinstance(value, int) or isinstance(value, bool) or value < 0
        for value in state.word
    ):
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
    empty_active = select_frontier(extinction_program, extinction.successor)
    empty_reads = read_neighborhoods(
        extinction_program, extinction.successor, empty_active
    )
    empty_writes = evaluate_rules(extinction_program, empty_active, empty_reads)
    assert (empty_active, empty_reads, empty_writes) == ((), (), ())

    one_block = BinaryCyclicProgram((0, 1), ((1,),), 1)
    one = generic_step(one_block, encode_direct(one_block, DirectState(0, (1,))))
    assert decode_tagged(one_block, one.successor).phase == 0

    duplicate_slots = BinaryCyclicProgram(
        (0, 1), ((1,), (1,), (0,)), 1
    )
    assert deserialize_program(serialize_program(duplicate_slots)) == duplicate_slots
    duplicate_phase_zero = DirectState(0, (1,))
    duplicate_phase_one = DirectState(1, (1,))
    assert serialize_state(duplicate_phase_zero) != serialize_state(
        duplicate_phase_one
    )
    assert direct_step(duplicate_slots, duplicate_phase_zero).phase_after == 1
    assert direct_step(duplicate_slots, duplicate_phase_one).phase_after == 2
    assert notes_value_projection(
        duplicate_slots, duplicate_phase_zero
    ) != notes_value_projection(duplicate_slots, duplicate_phase_one)

    # Named phase slots form an occurrence-addressed cover of the Notes'
    # rotated value-list state.  Rotationally periodic cycles can identify
    # distinct named phases, but the quotient remains step-compatible.
    periodic = BinaryCyclicProgram(
        (0, 1), ((1,), (0,), (1,), (0,)), 1
    )
    periodic_zero = DirectState(0, (1, 0))
    periodic_two = DirectState(2, (1, 0))
    assert periodic_zero != periodic_two
    assert notes_value_projection(periodic, periodic_zero) == notes_value_projection(
        periodic, periodic_two
    )
    assert notes_value_projection(
        periodic, direct_step(periodic, periodic_zero).successor
    ) == notes_value_projection(
        periodic, direct_step(periodic, periodic_two).successor
    )

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

    successor = apply_update(phase_program, old, active, (valid,)).successor
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
            lambda bad=bad: apply_update(phase_program, old, active, (bad,)),
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
    expect_value_error(
        lambda: BinaryCyclicProgram((0, 1, 2), ((1,),), 1),
        "nonbinary data was accepted by the strict preset",
    )
    expect_value_error(
        lambda: MultiplicityProgram(((1, -1),)),
        "negative multiplicity data was accepted",
    )
    expect_value_error(
        lambda: multiplicity_step(
            MultiplicityProgram(((1,),)), DirectState(0, (1.5,))
        ),
        "nonintegral multiplicity data was accepted",
    )
    expect_value_error(
        lambda: deserialize_program(
            {"alphabet": [0, True], "blocks": [[1]], "trigger": 1}
        ),
        "coercive program deserialization was accepted",
    )
    expect_value_error(
        lambda: deserialize_state({"phase": 0, "word": [1.0]}),
        "coercive state deserialization was accepted",
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
    if type(trigger) is not int:
        raise ValueError("malformed trigger")
    if any(not isinstance(block, list) for block in raw_blocks):
        raise ValueError("malformed block payload")
    if any(type(value) is not int for value in raw_alphabet):
        raise ValueError("malformed alphabet payload")
    if any(type(value) is not int for block in raw_blocks for value in block):
        raise ValueError("malformed block payload")
    return BinaryCyclicProgram(
        tuple(raw_alphabet),
        tuple(tuple(block) for block in raw_blocks),
        trigger,
    )


def serialize_state(state: DirectState) -> dict[str, object]:
    return {"phase": state.phase, "word": list(state.word)}


def deserialize_state(payload: dict[str, object]) -> DirectState:
    phase = payload["phase"]
    word = payload["word"]
    if type(phase) is not int or not isinstance(word, list):
        raise ValueError("malformed state payload")
    if any(type(value) is not int for value in word):
        raise ValueError("malformed state payload")
    return DirectState(phase, tuple(word))


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
        "T18 composes old-end insertion with phase/head prefix replacement",
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
        "visible named phase marker or Notes rotated-value quotient",
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
        "T17 ordered support plus visible phase, anchored access, spans, and empty policy",
        "ADD_T18_PRESET",
        "the named-slot tagged cover and Notes quotient add no execution algebra",
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
    assert direct_trace(CANONICAL_PROGRAM, DirectState(0, (1,)), 24) == (
        EXPECTED_CANONICAL_TRACE
    )
    assert generic_trace(CANONICAL_PROGRAM, DirectState(0, (1,)), 24) == (
        EXPECTED_CANONICAL_TRACE
    )
    book_fixture_cases = assert_book_fixtures()
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
        f"book_fixture_states={book_fixture_cases}; "
        "canonical_t0_t24=PASS; page96_t0_t99=PASS; visible_phase=PASS; "
        "branch_free_axis_calls=PASS; tagged_inverse=PASS; "
        "notes_rotation_quotient=PASS; opaque_snapshot_identity=PASS; "
        "phase_head_tail_atomic=PASS; extinction_then_stutter=PASS; "
        "shared_ordered_multispan_UPDATE=PASS; direct_serialization=PASS; "
        "decision_matrix=PASS)"
    )


if __name__ == "__main__":
    main()
