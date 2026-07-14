#!/usr/bin/env python3
"""Dependency-free semantic checks for Goal 1 stage T14.

This is research evidence, not runtime code.  It proves that Wolfram's finite
neighbor-dependent substitution step is a restriction of the same ordered
generation-emission UPDATE used by T13 once FRONTIER and NEIGHBORHOOD select
overlapping right-context reads.  It also keeps the Notes behavior on words of
length below two separate from the source-defined native input profile.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable


if not __debug__:
    raise RuntimeError("T14 semantic verification requires assertions; do not run with -O")


Bit = int
Word = tuple[Bit, ...]
Pair = tuple[Bit, Bit]
RuleTable = dict[Pair, Word]

BITS = (0, 1)
PAIR_CONTEXTS: tuple[Pair, ...] = tuple(product(BITS, repeat=2))

# A finite adversarial audit universe, not a claimed bound on general T14:
# every nonempty binary word of length one or two is allowed as each row result.
BOUNDED_OUTPUT_WORDS: tuple[Word, ...] = tuple(
    word
    for length in (1, 2)
    for word in product(BITS, repeat=length)
)


# BOOK:12109-12113, the textual first page-85 rule.  The seed is missing after
# BOOK:12115 because of an extraction defect; BOOK:1020's direct plate visibly
# supplies 0110 and the first four rows frozen below.
PAGE_85_RULE_1: RuleTable = {
    (1, 1): (0, 1),
    (1, 0): (1, 0),
    (0, 1): (0,),
    (0, 0): (0, 1),
}
PAGE_85_SEED: Word = (0, 1, 1, 0)
EXPECTED_PAGE_85_RULE_1_TRACE: tuple[Word, ...] = (
    (0, 1, 1, 0),
    (0, 0, 1, 1, 0),
    (0, 1, 0, 0, 1, 1, 0),
    (0, 1, 0, 0, 1, 0, 0, 1, 1, 0),
)

# Raster-derived from the second rule plate at BOOK:1020.  No textual rule-2
# table was found, so this remains a visual conformance fixture, not a repair
# silently attributed to prose or Notes.
PAGE_85_RULE_2_RASTER: RuleTable = {
    (1, 1): (0, 0),
    (1, 0): (1, 1),
    (0, 1): (1,),
    (0, 0): (0,),
}
EXPECTED_PAGE_85_RULE_2_TRACE: tuple[Word, ...] = (
    (0, 1, 1, 0),
    (1, 0, 0, 1, 1),
    (1, 1, 0, 1, 0, 0),
    (0, 0, 1, 1, 1, 1, 1, 0),
)


@dataclass(frozen=True)
class OrderedConfiguration:
    """Transparent generic representation of a finite ordered word."""

    values: Word


@dataclass(frozen=True)
class OrderedEmission:
    """One source occurrence's ordered contribution to the next generation."""

    source: int
    word: Word


@dataclass(frozen=True)
class ChildInterval:
    """Inspectable parent/emission provenance; it is not future rule state."""

    source: int
    start: int
    stop: int


@dataclass(frozen=True)
class OrderedGenerationStep:
    successor: OrderedConfiguration
    child_intervals: tuple[ChildInterval, ...]
    dropped_sources: tuple[int, ...]


class SourceUndefined(ValueError):
    """The book does not establish the native short-word input profile."""


class OverlappingReplacementSpans(ValueError):
    """Raised by the deliberately wrong pair-as-splice interpretation."""


def checked_word(values: Iterable[int], *, allow_empty: bool = True) -> Word:
    word = tuple(values)
    if not allow_empty and not word:
        raise ValueError("T14 base rule results must be nonempty")
    if any(value not in BITS for value in word):
        raise ValueError("word is outside the declared binary alphabet")
    return word


def validate_rule_rows(rows: Iterable[tuple[Pair, Word]]) -> RuleTable:
    """Require exactly one closed, nonempty row for every ordered pair."""
    table: RuleTable = {}
    for raw_context, raw_output in rows:
        context = tuple(raw_context)
        if len(context) != 2 or any(value not in BITS for value in context):
            raise ValueError("invalid ordered-pair context")
        pair: Pair = (context[0], context[1])
        if pair in table:
            raise ValueError("duplicate ordered-pair row")
        table[pair] = checked_word(raw_output, allow_empty=False)
    if set(table) != set(PAIR_CONTEXTS):
        raise ValueError("table must cover every ordered pair exactly once")
    return table


def encode_native(word: Word) -> OrderedConfiguration:
    """Lossless native-word to generic-configuration map e."""
    return OrderedConfiguration(checked_word(word))


def decode_generic(configuration: OrderedConfiguration) -> Word:
    """Explicit inverse of e on its invariant-valid image."""
    return checked_word(configuration.values)


def all_occurrences(configuration: OrderedConfiguration) -> tuple[int, ...]:
    """T13 FRONTIER: every old occurrence emits once."""
    return tuple(range(len(configuration.values)))


def all_right_context_anchors(
    configuration: OrderedConfiguration,
) -> tuple[int, ...]:
    """T14 FRONTIER: every old occurrence having an immediate right neighbor."""
    return tuple(range(max(0, len(configuration.values) - 1)))


def read_self(
    configuration: OrderedConfiguration, active: tuple[int, ...]
) -> tuple[Bit, ...]:
    values = configuration.values
    assert all(0 <= source < len(values) for source in active)
    return tuple(values[source] for source in active)


def read_self_right(
    configuration: OrderedConfiguration, active: tuple[int, ...]
) -> tuple[Pair, ...]:
    """Ordered, overlapping reads from one immutable old snapshot."""
    values = configuration.values
    assert all(0 <= source < len(values) - 1 for source in active)
    return tuple((values[source], values[source + 1]) for source in active)


def pair_rule_emissions(
    table: RuleTable,
    active: tuple[int, ...],
    reads: tuple[Pair, ...],
) -> tuple[OrderedEmission, ...]:
    assert len(active) == len(reads)
    assert set(table) == set(PAIR_CONTEXTS)
    return tuple(
        OrderedEmission(source, checked_word(table[context], allow_empty=False))
        for source, context in zip(active, reads, strict=True)
    )


def self_rule_emissions(
    morphism: dict[Bit, Word],
    active: tuple[int, ...],
    reads: tuple[Bit, ...],
) -> tuple[OrderedEmission, ...]:
    """T13 uses the same result and UPDATE with a self-only table."""
    assert len(active) == len(reads)
    assert set(morphism) == set(BITS)
    return tuple(
        OrderedEmission(source, checked_word(morphism[value], allow_empty=False))
        for source, value in zip(active, reads, strict=True)
    )


def apply_ordered_generation(
    old: OrderedConfiguration,
    active: tuple[int, ...],
    emissions: tuple[OrderedEmission, ...],
) -> OrderedGenerationStep:
    """Shared T13/T14 UPDATE: rebuild one generation from ordered emissions.

    It never interprets a read neighborhood as a replacement span.  The old
    generation is consumed atomically, emissions are concatenated in source
    order, and any old occurrences outside the selected emission frontier are
    reported as dropped rather than silently copied forward.
    """
    if tuple(sorted(set(active))) != active:
        raise ValueError("active source handles must be unique and ordered")
    if any(source < 0 or source >= len(old.values) for source in active):
        raise ValueError("stale or foreign source handle")
    if tuple(emission.source for emission in emissions) != active:
        raise ValueError("emissions must cover the selected frontier exactly in order")

    next_values: list[Bit] = []
    intervals: list[ChildInterval] = []
    for emission in emissions:
        word = checked_word(emission.word, allow_empty=False)
        start = len(next_values)
        next_values.extend(word)
        intervals.append(ChildInterval(emission.source, start, len(next_values)))

    active_set = set(active)
    dropped = tuple(source for source in range(len(old.values)) if source not in active_set)
    return OrderedGenerationStep(
        successor=OrderedConfiguration(tuple(next_values)),
        child_intervals=tuple(intervals),
        dropped_sources=dropped,
    )


def shared_t13_step(
    morphism: dict[Bit, Word], configuration: OrderedConfiguration
) -> OrderedGenerationStep:
    active = all_occurrences(configuration)
    reads = read_self(configuration, active)
    emissions = self_rule_emissions(morphism, active, reads)
    return apply_ordered_generation(configuration, active, emissions)


def shared_t14_notes_step(
    table: RuleTable, configuration: OrderedConfiguration
) -> OrderedGenerationStep:
    """Branch-free pipeline matching the finite Notes expression.

    For words of length zero or one this is an implementation-derived
    totalization only; ``native_defined_step`` deliberately leaves that source
    profile undefined.
    """
    active = all_right_context_anchors(configuration)
    reads = read_self_right(configuration, active)
    emissions = pair_rule_emissions(table, active, reads)
    return apply_ordered_generation(configuration, active, emissions)


def notes_partition_step(table: RuleTable, word: Word) -> Word:
    """Direct model of Flatten[Partition[word,2,1] /. table]."""
    word = checked_word(word)
    pairs = tuple(zip(word, word[1:]))
    return tuple(value for pair in pairs for value in table[pair])


def native_defined_step(table: RuleTable, word: Word) -> Word:
    """Source-defined profile: defer validity/outcome for words below length 2."""
    word = checked_word(word)
    if len(word) < 2:
        raise SourceUndefined(
            "T14 source does not establish whether short words are native states, "
            "terminal outcomes, or continued Notes-extension states"
        )
    return notes_partition_step(table, word)


def trace(table: RuleTable, seed: Word, steps: int) -> tuple[Word, ...]:
    word = checked_word(seed)
    rows = [word]
    for _ in range(steps):
        word = notes_partition_step(table, word)
        rows.append(word)
    return tuple(rows)


def wrong_disjoint_pair_splice(word: Word) -> Word:
    """Hostile model: treating overlapping reads as simultaneous edit spans."""
    spans = tuple((source, source + 2) for source in range(max(0, len(word) - 1)))
    for left, right in zip(spans, spans[1:]):
        if left[1] > right[0]:
            raise OverlappingReplacementSpans((left, right))
    return word


def assert_table_validation() -> None:
    assert validate_rule_rows(PAGE_85_RULE_1.items()) == PAGE_85_RULE_1
    assert validate_rule_rows(PAGE_85_RULE_2_RASTER.items()) == PAGE_85_RULE_2_RASTER

    invalid_rows = (
        tuple(PAGE_85_RULE_1.items())[:-1],
        tuple(PAGE_85_RULE_1.items()) + (((1, 1), (1,)),),
        tuple((context, () if context == (0, 0) else word) for context, word in PAGE_85_RULE_1.items()),
        tuple((context, (2,) if context == (0, 0) else word) for context, word in PAGE_85_RULE_1.items()),
    )
    for rows in invalid_rows:
        try:
            validate_rule_rows(rows)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid T14 table was accepted")


def assert_page_85_fixtures() -> None:
    assert trace(PAGE_85_RULE_1, PAGE_85_SEED, 3) == EXPECTED_PAGE_85_RULE_1_TRACE
    assert trace(PAGE_85_RULE_2_RASTER, PAGE_85_SEED, 3) == EXPECTED_PAGE_85_RULE_2_TRACE


def assert_update_reuse_and_counterexamples() -> None:
    # T13 and T14 invoke the exact same ordered-generation UPDATE.  Only their
    # frontier/read/table shapes differ.
    old = encode_native((0, 1, 0))
    t13 = shared_t13_step({0: (1,), 1: (1, 0)}, old)
    assert t13.successor.values == (1, 1, 0, 1)
    assert t13.dropped_sources == ()

    t14 = shared_t14_notes_step(PAGE_85_RULE_1, old)
    assert t14.successor.values == (0, 1, 0)
    assert t14.dropped_sources == (2,)
    assert t14.child_intervals == (
        ChildInterval(0, 0, 1),
        ChildInterval(1, 1, 3),
    )

    # A self-only T13 morphism cannot express T14: the same source symbol 0
    # must emit 01 in context 00 but 0 in context 01.
    assert PAGE_85_RULE_1[(0, 0)] != PAGE_85_RULE_1[(0, 1)]
    assert native_defined_step(PAGE_85_RULE_1, (0, 0)) == (0, 1)
    assert native_defined_step(PAGE_85_RULE_1, (0, 1)) == (0,)

    # Overlap belongs only to reads.  Treating [0,2) and [1,3) as replacement
    # spans creates a false collision that the native ordered emissions lack.
    try:
        wrong_disjoint_pair_splice((0, 1, 0))
    except OverlappingReplacementSpans:
        pass
    else:
        raise AssertionError("overlapping pair reads were accepted as disjoint splices")

    # A CA-style copy-forward for the inactive rightmost source is incorrect.
    assert native_defined_step(PAGE_85_RULE_1, (0, 1)) == (0,)
    assert native_defined_step(PAGE_85_RULE_1, (0, 1)) + (1,) == (0, 1)

    # Source order is semantic; reversing the two ordered emissions changes 010.
    forward = PAGE_85_RULE_1[(0, 1)] + PAGE_85_RULE_1[(1, 0)]
    reverse = PAGE_85_RULE_1[(1, 0)] + PAGE_85_RULE_1[(0, 1)]
    assert forward == (0, 1, 0) and reverse == (1, 0, 0)

    # BOOK:1026 describes the displayed trajectories, not all seeds of the
    # table: even with nonempty row outputs the open-right drop can shrink 01.
    assert len(native_defined_step(PAGE_85_RULE_1, (0, 1))) < 2


def assert_short_word_uncertainty() -> None:
    for word in ((), (0,), (1,)):
        # Mathematica's Partition/Flatten expression has this natural result.
        assert notes_partition_step(PAGE_85_RULE_1, word) == ()
        notes_shared = shared_t14_notes_step(PAGE_85_RULE_1, encode_native(word))
        assert notes_shared.successor == OrderedConfiguration(())
        assert notes_shared.dropped_sources == tuple(range(len(word)))

        # But native validity and terminal-vs-successor interpretation are not
        # promoted from host behavior into source semantics.
        try:
            native_defined_step(PAGE_85_RULE_1, word)
        except SourceUndefined:
            pass
        else:
            raise AssertionError("short-word source uncertainty was erased")


def assert_exhaustive_bounded_commutation(max_input_length: int = 6) -> tuple[int, int]:
    """Exhaust all 6^4 bounded tables and binary words through length six."""
    assert len(PAIR_CONTEXTS) == 4
    assert len(BOUNDED_OUTPUT_WORDS) == 6
    assert len(BOUNDED_OUTPUT_WORDS) ** len(PAIR_CONTEXTS) == 1_296

    defined_cases = 0
    short_extension_cases = 0
    for outputs in product(BOUNDED_OUTPUT_WORDS, repeat=len(PAIR_CONTEXTS)):
        table = dict(zip(PAIR_CONTEXTS, outputs, strict=True))
        assert validate_rule_rows(table.items()) == table
        for length in range(max_input_length + 1):
            for raw_word in product(BITS, repeat=length):
                word: Word = tuple(raw_word)
                encoded = encode_native(word)
                assert decode_generic(encoded) == word
                assert encode_native(decode_generic(encoded)) == encoded

                notes_next = notes_partition_step(table, word)
                generic_step = shared_t14_notes_step(table, encoded)
                generic_next = generic_step.successor

                # The explicit one-step commuting square on the supported
                # profile, plus the separately-labelled Notes totalization.
                assert encode_native(notes_next) == generic_next
                assert decode_generic(generic_next) == notes_next
                assert tuple(
                    notes_next[interval.start : interval.stop]
                    for interval in generic_step.child_intervals
                ) == tuple(table[pair] for pair in zip(word, word[1:]))
                assert sum(
                    interval.stop - interval.start
                    for interval in generic_step.child_intervals
                ) == len(notes_next)

                if length >= 2:
                    assert encode_native(native_defined_step(table, word)) == generic_next
                    assert generic_step.dropped_sources == (length - 1,)
                    defined_cases += 1
                else:
                    assert notes_next == ()
                    short_extension_cases += 1

    return defined_cases, short_extension_cases


def main() -> None:
    assert_table_validation()
    assert_page_85_fixtures()
    assert_update_reuse_and_counterexamples()
    assert_short_word_uncertainty()
    defined_cases, short_cases = assert_exhaustive_bounded_commutation()
    assert defined_cases == 160_704
    assert short_cases == 3_888
    print(
        "T14 semantic oracle: PASS "
        f"(bounded_tables={len(BOUNDED_OUTPUT_WORDS) ** len(PAIR_CONTEXTS)}; "
        f"defined_commutation_cases={defined_cases}; "
        f"short_notes_extension_cases={short_cases}; "
        "page85_rule1_t0_t3=PASS; page85_rule2_raster_t0_t4=PASS; "
        "shared_ordered_UPDATE=PASS; overlap_is_read_only=PASS; "
        "rightmost_drop=PASS; short_native_profile=UNSPECIFIED)"
    )


if __name__ == "__main__":
    main()
