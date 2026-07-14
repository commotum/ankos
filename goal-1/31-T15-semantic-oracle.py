#!/usr/bin/env python3
"""Independent semantic and architecture checks for Goal 1 stage T15.

This is dependency-free research evidence, not runtime code.  It reconstructs
the hash-bound page-101 creation/destruction example as the same contextual
ordered-generation schedule proved for T14, except that a selected old source
may emit the empty word.  It tests the smallest reusable factorization:

* the private ``OrderedGenerationConcat`` result carrier accepts ``Sigma*``;
* strict public T13 and T14 validators continue to require ``Sigma+``;
* every selected source has one explicit source-bound emission record, even
  when that record has a zero-length word and no child records; and
* zero selected sources, an explicit empty emission, an empty successor, and
  a zero-successor terminal outcome remain observably different.

The direct source has no textual T15 table.  Raster fixtures below are included
only after the separate asset audit has fixed their table, seed, and trace.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from itertools import product
from typing import Iterable, TypeAlias


if not __debug__:
    raise RuntimeError("T15 semantic verification requires assertions; do not run with -O")


Symbol: TypeAlias = int
Word: TypeAlias = tuple[Symbol, ...]
Pair: TypeAlias = tuple[Symbol, Symbol]
PairTable: TypeAlias = dict[Pair, Word]
Morphism: TypeAlias = dict[Symbol, Word]


@dataclass(frozen=True)
class Alphabet:
    """Finite ordered alphabet; ordering is explicit program data."""

    symbols: tuple[Symbol, ...]

    def __post_init__(self) -> None:
        if not self.symbols:
            raise ValueError("alphabet must be nonempty")
        if len(set(self.symbols)) != len(self.symbols):
            raise ValueError("alphabet symbols must be unique")


BINARY = Alphabet((0, 1))
TERNARY = Alphabet((0, 1, 2))
QUATERNARY = Alphabet((0, 1, 2, 3))


def checked_word(values: Iterable[Symbol], alphabet: Alphabet) -> Word:
    word = tuple(values)
    if any(value not in alphabet.symbols for value in word):
        raise ValueError("word is outside the declared alphabet")
    return word


def checked_nonempty_word(values: Iterable[Symbol], alphabet: Alphabet) -> Word:
    word = checked_word(values, alphabet)
    if not word:
        raise ValueError("strict rule result must be in Sigma+")
    return word


def digit_words(rows: tuple[str, ...]) -> tuple[Word, ...]:
    return tuple(tuple(int(character) for character in row) for row in rows)


def pair_contexts(alphabet: Alphabet) -> tuple[Pair, ...]:
    return tuple(product(alphabet.symbols, repeat=2))


def _validate_pair_rows(
    rows: Iterable[tuple[Pair, Word]], alphabet: Alphabet
) -> PairTable:
    """Private Sigma* table validator shared before preset refinements."""

    table: PairTable = {}
    for raw_context, raw_output in rows:
        context = tuple(raw_context)
        if len(context) != 2 or any(value not in alphabet.symbols for value in context):
            raise ValueError("invalid ordered-pair context")
        pair: Pair = (context[0], context[1])
        if pair in table:
            raise ValueError("duplicate ordered-pair row")
        table[pair] = checked_word(raw_output, alphabet)
    if set(table) != set(pair_contexts(alphabet)):
        raise ValueError("table must cover every ordered pair exactly once")
    return table


def validate_t15_pair_rows(
    rows: Iterable[tuple[Pair, Word]], alphabet: Alphabet
) -> PairTable:
    """T15 contextual profile: total, closed, and epsilon-capable."""

    return _validate_pair_rows(rows, alphabet)


def validate_t14_pair_rows(
    rows: Iterable[tuple[Pair, Word]], alphabet: Alphabet
) -> PairTable:
    """Strict T14 preset remains total, closed, and nonempty."""

    table = _validate_pair_rows(rows, alphabet)
    if any(not output for output in table.values()):
        raise ValueError("T14 table results must be in Sigma+")
    return table


def validate_t13_morphism(
    rows: Iterable[tuple[Symbol, Word]], alphabet: Alphabet
) -> Morphism:
    """Strict T13 preset remains a total Sigma -> Sigma+ morphism."""

    table: Morphism = {}
    for symbol, raw_output in rows:
        if symbol not in alphabet.symbols:
            raise ValueError("invalid T13 source symbol")
        if symbol in table:
            raise ValueError("duplicate T13 row")
        table[symbol] = checked_nonempty_word(raw_output, alphabet)
    if set(table) != set(alphabet.symbols):
        raise ValueError("T13 morphism must cover the alphabet exactly once")
    return table


@dataclass(frozen=True, eq=False)
class SnapshotToken:
    """Opaque configuration identity; generation is diagnostic metadata only."""

    generation: int

    def __post_init__(self) -> None:
        if self.generation < 0:
            raise ValueError("generation must be nonnegative")


@dataclass(frozen=True)
class OrderedConfiguration:
    """Semantic finite word plus a nonsemantic identity-scoped token."""

    alphabet: Alphabet
    values: Word
    snapshot_token: SnapshotToken = field(
        default_factory=lambda: SnapshotToken(0), compare=False, repr=False
    )

    def __post_init__(self) -> None:
        checked_word(self.values, self.alphabet)

    @property
    def generation(self) -> int:
        return self.snapshot_token.generation


@dataclass(frozen=True)
class SourceHandle:
    snapshot_token: SnapshotToken = field(repr=False)
    index: int

    @property
    def generation(self) -> int:
        return self.snapshot_token.generation


@dataclass(frozen=True)
class OrderedEmission:
    """RULE write bound to exactly one selected old occurrence."""

    source: SourceHandle
    word: Word


@dataclass(frozen=True)
class ChildRecord:
    """One real child; epsilon emissions deliberately have none."""

    parent: SourceHandle
    child_ordinal: int
    successor_index: int
    value: Symbol


@dataclass(frozen=True)
class EmissionRecord:
    """Inspectable source/result/span witness retained even for epsilon."""

    source: SourceHandle
    word: Word
    start: int
    stop: int
    children: tuple[ChildRecord, ...]


@dataclass(frozen=True)
class OrderedGenerationStep:
    successor: OrderedConfiguration
    emission_records: tuple[EmissionRecord, ...]
    dropped_sources: tuple[SourceHandle, ...]


@dataclass(frozen=True)
class Transition:
    """A successful event has exactly one successor, possibly the empty word."""

    event: OrderedGenerationStep

    @property
    def successors(self) -> tuple[OrderedConfiguration, ...]:
        return (self.event.successor,)


@dataclass(frozen=True)
class Terminal:
    """Typed zero-successor outcome used to guard the T16 boundary."""

    final: OrderedConfiguration
    reason: str

    @property
    def successors(self) -> tuple[OrderedConfiguration, ...]:
        return ()


StepOutcome: TypeAlias = Transition | Terminal


def make_configuration(
    word: Word, alphabet: Alphabet, *, generation: int
) -> OrderedConfiguration:
    """Allocate a fresh opaque snapshot identity for one semantic word."""

    return OrderedConfiguration(
        alphabet, checked_word(word, alphabet), SnapshotToken(generation)
    )


def encode_native(
    word: Word, alphabet: Alphabet, *, generation: int = 0
) -> OrderedConfiguration:
    """Lossless map e; every call allocates a distinct address scope."""

    return make_configuration(word, alphabet, generation=generation)


def decode_generic(configuration: OrderedConfiguration) -> Word:
    return checked_word(configuration.values, configuration.alphabet)


def all_occurrences(
    configuration: OrderedConfiguration,
) -> tuple[SourceHandle, ...]:
    """T13 FRONTIER: every old occurrence is selected."""

    return tuple(
        SourceHandle(configuration.snapshot_token, index)
        for index in range(len(configuration.values))
    )


def all_right_context_anchors(
    configuration: OrderedConfiguration,
) -> tuple[SourceHandle, ...]:
    """T14/T15 FRONTIER: each old occurrence having a right neighbor."""

    return tuple(
        SourceHandle(configuration.snapshot_token, index)
        for index in range(max(0, len(configuration.values) - 1))
    )


def _check_active(
    old: OrderedConfiguration,
    active: tuple[SourceHandle, ...],
    *, require_right_neighbor: bool = False,
) -> None:
    if tuple(sorted(set(active), key=lambda handle: handle.index)) != active:
        raise ValueError("active handles must be unique and in source order")
    upper = len(old.values) - (1 if require_right_neighbor else 0)
    if any(source.snapshot_token is not old.snapshot_token for source in active):
        raise ValueError("stale or foreign source handle")
    if any(source.index < 0 or source.index >= upper for source in active):
        raise ValueError("source handle is outside its old-snapshot role")


def read_self(
    old: OrderedConfiguration, active: tuple[SourceHandle, ...]
) -> tuple[Symbol, ...]:
    _check_active(old, active)
    return tuple(old.values[source.index] for source in active)


def read_self_right(
    old: OrderedConfiguration, active: tuple[SourceHandle, ...]
) -> tuple[Pair, ...]:
    """Overlapping pair reads are all taken from one immutable old word."""

    _check_active(old, active, require_right_neighbor=True)
    return tuple(
        (old.values[source.index], old.values[source.index + 1])
        for source in active
    )


def self_emissions(
    morphism: Morphism,
    active: tuple[SourceHandle, ...],
    reads: tuple[Symbol, ...],
) -> tuple[OrderedEmission, ...]:
    if len(active) != len(reads):
        raise ValueError("one read is required per selected source")
    return tuple(
        OrderedEmission(source, morphism[symbol])
        for source, symbol in zip(active, reads, strict=True)
    )


def pair_emissions(
    table: PairTable,
    active: tuple[SourceHandle, ...],
    reads: tuple[Pair, ...],
) -> tuple[OrderedEmission, ...]:
    if len(active) != len(reads):
        raise ValueError("one read is required per selected source")
    return tuple(
        OrderedEmission(source, table[context])
        for source, context in zip(active, reads, strict=True)
    )


def validate_generation_witness(
    old: OrderedConfiguration,
    active: tuple[SourceHandle, ...],
    event: OrderedGenerationStep,
) -> None:
    """Reject fake epsilon children or any tampered provenance/result data."""

    _check_active(old, active)
    if event.successor.alphabet != old.alphabet:
        raise ValueError("UPDATE changed the alphabet")
    if event.successor.snapshot_token is old.snapshot_token:
        raise ValueError("successor reused the old snapshot identity")
    if event.successor.generation != old.generation + 1:
        raise ValueError("successor generation diagnostic is not old + 1")
    if tuple(record.source for record in event.emission_records) != active:
        raise ValueError("records must cover the selected frontier exactly in order")

    rebuilt: list[Symbol] = []
    for record in event.emission_records:
        word = checked_word(record.word, old.alphabet)
        if record.start != len(rebuilt) or record.stop != record.start + len(word):
            raise ValueError("emission span is not the exact ordered concatenation span")
        expected_children = tuple(
            ChildRecord(record.source, ordinal, record.start + ordinal, value)
            for ordinal, value in enumerate(word)
        )
        if record.children != expected_children:
            raise ValueError("emission child records are incomplete, fake, or reordered")
        rebuilt.extend(word)
    if tuple(rebuilt) != event.successor.values:
        raise ValueError("successor does not equal source-ordered emission concatenation")

    active_indices = {source.index for source in active}
    expected_dropped = tuple(
        SourceHandle(old.snapshot_token, index)
        for index in range(len(old.values))
        if index not in active_indices
    )
    if event.dropped_sources != expected_dropped:
        raise ValueError("unselected old-source disposition is incomplete or copied")


def apply_ordered_generation(
    old: OrderedConfiguration,
    active: tuple[SourceHandle, ...],
    emissions: tuple[OrderedEmission, ...],
) -> Transition:
    """Private Sigma*-capable ordered generation UPDATE.

    Every selected old source must return one emission record.  Empty words are
    not dropped records, fake symbols, or terminal signals.  All old sources
    are consumed, unselected sources are reported rather than copied, and only
    real output symbols become child records in the successor generation.
    """

    _check_active(old, active)
    if tuple(emission.source for emission in emissions) != active:
        raise ValueError("emissions must cover selected handles exactly in order")

    next_values: list[Symbol] = []
    records: list[EmissionRecord] = []
    for emission in emissions:
        word = checked_word(emission.word, old.alphabet)
        start = len(next_values)
        children = tuple(
            ChildRecord(emission.source, ordinal, start + ordinal, value)
            for ordinal, value in enumerate(word)
        )
        next_values.extend(word)
        records.append(
            EmissionRecord(emission.source, word, start, len(next_values), children)
        )

    active_indices = {source.index for source in active}
    dropped = tuple(
        SourceHandle(old.snapshot_token, index)
        for index in range(len(old.values))
        if index not in active_indices
    )
    event = OrderedGenerationStep(
        successor=make_configuration(
            tuple(next_values), old.alphabet, generation=old.generation + 1
        ),
        emission_records=tuple(records),
        dropped_sources=dropped,
    )
    validate_generation_witness(old, active, event)
    return Transition(event)


def _shared_self_step(
    morphism: Morphism, configuration: OrderedConfiguration
) -> Transition:
    active = all_occurrences(configuration)
    reads = read_self(configuration, active)
    writes = self_emissions(morphism, active, reads)
    return apply_ordered_generation(configuration, active, writes)


def t13_step(morphism: Morphism, configuration: OrderedConfiguration) -> Transition:
    strict = validate_t13_morphism(morphism.items(), configuration.alphabet)
    return _shared_self_step(strict, configuration)


def _shared_pair_step(
    table: PairTable, configuration: OrderedConfiguration
) -> Transition:
    active = all_right_context_anchors(configuration)
    reads = read_self_right(configuration, active)
    writes = pair_emissions(table, active, reads)
    return apply_ordered_generation(configuration, active, writes)


def t14_step(table: PairTable, configuration: OrderedConfiguration) -> Transition:
    strict = validate_t14_pair_rows(table.items(), configuration.alphabet)
    return _shared_pair_step(strict, configuration)


def t15_step(table: PairTable, configuration: OrderedConfiguration) -> Transition:
    """Reconstructed pair operator, including its derived zero-source case."""

    epsilon_capable = validate_t15_pair_rows(table.items(), configuration.alphabet)
    return _shared_pair_step(epsilon_capable, configuration)


def t16_no_match(configuration: OrderedConfiguration) -> Terminal:
    """Outcome guard only: T16 NoMatch is not an empty T15 transition."""

    return Terminal(configuration, "NoMatch")


def t17_insufficient_prefix(configuration: OrderedConfiguration) -> Terminal:
    """Outcome guard only: a disabled tag residue has zero successors."""

    return Terminal(configuration, "InsufficientPrefix")


def native_pair_step(table: PairTable, word: Word, alphabet: Alphabet) -> Word:
    checked_word(word, alphabet)
    return tuple(
        value
        for index in range(max(0, len(word) - 1))
        for value in table[(word[index], word[index + 1])]
    )


def native_self_step(morphism: Morphism, word: Word, alphabet: Alphabet) -> Word:
    checked_word(word, alphabet)
    return tuple(value for symbol in word for value in morphism[symbol])


def native_pair_trace(
    table: PairTable, seed: Word, steps: int, alphabet: Alphabet
) -> tuple[Word, ...]:
    word = checked_word(seed, alphabet)
    rows = [word]
    for _ in range(steps):
        word = native_pair_step(table, word, alphabet)
        rows.append(word)
    return tuple(rows)


# Hash-bound page-101 rule/seed independently decoded by the asset audit
# (SHA-256 9390efdb915dfdf78e870f85b0f2964791a00714f8619525e256098b98919c4e).
# Color mapping is light=0, dark=1; glyph order is 11,10,01,00.  This is the
# direct evidence that permits this oracle to model the contextual pair
# schedule rather than merely hypothesize it from the preceding T14 section.
PAGE_101_RULE: PairTable = {
    (1, 1): (1, 1),
    (1, 0): (0,),
    (0, 1): (1, 0),
    (0, 0): (),
}
PAGE_101_SEED: Word = (0, 1, 1, 0)
PAGE_101_EXPECTED_TRACE: tuple[Word, ...] = digit_words(
    (
        "0110",
        "10110",
        "010110",
        "10010110",
        "010010110",
        "10010010110",
        "010010010110",
        "10010010010110",
        "010010010010110",
        "10010010010010110",
        "010010010010010110",
        "10010010010010010110",
    )
)


# Independently decoded page-102 plates.  The separate asset oracle owns the
# raster identity/provenance (rule strip SHA-256
# 77c261cf4c9b83d08aead4601916dbc6ac96f371b00a30549c96586295d18585;
# evolution SHA-256
# cc6b3fdffceecf66543d9f6dbfc1628913eec7356e11e5716473a112b5b728a4).
# These hardcoded expected strings were sampled directly from the plate and
# are not generated from the tables below.
PAGE_102_RULE_A: PairTable = {
    (2, 2): (0,),
    (2, 1): (0,),
    (2, 0): (2,),
    (1, 2): (0, 0),
    (1, 1): (0, 1),
    (1, 0): (1, 1),
    (0, 2): (2,),
    (0, 1): (2,),
    (0, 0): (0,),
}
PAGE_102_RULE_B: PairTable = {
    (2, 2): (2,),
    (2, 1): (0, 1),
    (2, 0): (0,),
    (1, 2): (),
    (1, 1): (),
    (1, 0): (2,),
    (0, 2): (0,),
    (0, 1): (0, 1),
    (0, 0): (2,),
}
PAGE_102_RULE_C: PairTable = {
    (2, 2): (1,),
    (2, 1): (),
    (2, 0): (0, 1),
    (1, 2): (2, 1),
    (1, 1): (0, 2),
    (1, 0): (2, 2),
    (0, 2): (),
    (0, 1): (1, 2),
    (0, 0): (0,),
}
PAGE_102_RULE_D: PairTable = {
    (2, 2): (2, 0),
    (2, 1): (1, 1),
    (2, 0): (2, 0),
    (1, 2): (2,),
    (1, 1): (1,),
    (1, 0): (),
    (0, 2): (0,),
    (0, 1): (0,),
    (0, 0): (2, 1),
}
PAGE_102_RULE_E: PairTable = {
    (3, 3): (1, 2),
    (3, 2): (2, 3),
    (3, 1): (0,),
    (3, 0): (1, 0),
    (2, 3): (),
    (2, 2): (2,),
    (2, 1): (1, 3),
    (2, 0): (),
    (1, 3): (2, 0),
    (1, 2): (),
    (1, 1): (1,),
    (1, 0): (3, 0),
    (0, 3): (),
    (0, 2): (2, 0),
    (0, 1): (3, 3),
    (0, 0): (2, 2),
}
PAGE_102_RULE_F: PairTable = {
    (3, 3): (1, 3),
    (3, 2): (0, 3),
    (3, 1): (2,),
    (3, 0): (),
    (2, 3): (0, 2),
    (2, 2): (),
    (2, 1): (0, 1),
    (2, 0): (3,),
    (1, 3): (0, 3),
    (1, 2): (0,),
    (1, 1): (2, 1),
    (1, 0): (2, 2),
    (0, 3): (),
    (0, 2): (3,),
    (0, 1): (1, 0),
    (0, 0): (1, 3),
}


PAGE_102_FIXTURES: tuple[
    tuple[str, Alphabet, PairTable, Word, tuple[Word, ...]], ...
] = (
    (
        "a",
        TERNARY,
        PAGE_102_RULE_A,
        (0, 1, 1, 0),
        digit_words(
            (
                "0110",
                "20111",
                "220101",
                "022112",
                "2000100",
                "2002110",
                "20200111",
                "222020101",
                "002222112",
                "0200000100",
                "2200002110",
                "02000200111",
            )
        ),
    ),
    (
        "b",
        TERNARY,
        PAGE_102_RULE_B,
        (0, 1, 2, 1),
        digit_words(
            (
                "0121",
                "0101",
                "01201",
                "01001",
                "012201",
                "012001",
                "010201",
                "0120001",
                "0102201",
                "01202001",
                "01000201",
                "012220001",
            )
        ),
    ),
    (
        "c",
        TERNARY,
        PAGE_102_RULE_C,
        (0, 1, 1, 0),
        digit_words(
            (
                "0110",
                "120222",
                "210111",
                "22120202",
                "1210101",
                "2122122212",
                "211211121",
                "0221020221",
                "122011",
                "211011202",
                "022212022101",
                "11210112212",
            )
        ),
    ),
    (
        "d",
        TERNARY,
        PAGE_102_RULE_D,
        (0, 1, 2, 0),
        digit_words(
            (
                "0120",
                "0220",
                "02020",
                "020020",
                "02021020",
                "020011020",
                "0202101020",
                "0200110020",
                "020210121020",
                "0200110211020",
                "02021010111020",
                "0200110011020",
            )
        ),
    ),
    (
        "e",
        QUATERNARY,
        PAGE_102_RULE_E,
        (0, 1, 0, 0),
        digit_words(
            (
                "0100",
                "333022",
                "121210202",
                "1313302020",
                "2002012102020",
                "22203313302020",
                "221202012102020",
                "213203313302020",
                "1320231202012102020",
                "2023200203313302020",
                "202322201202012102020",
                "20232233203313302020",
            )
        ),
    ),
    (
        "f",
        QUATERNARY,
        PAGE_102_RULE_F,
        (0, 1, 0, 0),
        digit_words(
            (
                "0100",
                "102213",
                "2230103",
                "021022",
                "301223",
                "10002",
                "2213133",
                "010320313",
                "1022033203",
                "223313033",
                "021320313",
                "30103033203",
            )
        ),
    ),
)


@dataclass(frozen=True)
class DecisionDisposition:
    decision: str
    action: str
    reason: str


DECISION_MATRIX = (
    DecisionDisposition(
        "D019",
        "CLARIFY_PRIVATE_BASE",
        "OrderedGenerationConcat accepts Sigma* and retains a zero-length source record; T13 full coverage remains a preset.",
    ),
    DecisionDisposition(
        "D020",
        "KEEP_T13_SIGMA_PLUS",
        "T15 contextual epsilon evidence does not weaken T13's public total Sigma->Sigma+ morphism validator.",
    ),
    DecisionDisposition(
        "D024",
        "EXTEND_OUTCOME_CASES",
        "T15 epsilon, zero-source, and post-extinction events are distinct one-successor transitions under the reconstructed Notes operator, not T16/T17 terminal outcomes.",
    ),
    DecisionDisposition(
        "D028",
        "CONFIRM_SIGMA_STAR_CARRIER",
        "Direct T15 epsilon rows independently confirm a private Sigma* word/emission carrier while public T13/T14/T16 validators retain their construction-specific nonempty restrictions.",
    ),
    DecisionDisposition(
        "D124",
        "KEEP_T14_SIGMA_PLUS",
        "T14 remains HasRightNeighbor plus pair read plus Sigma+; T15 reuses its schedule with a different result refinement.",
    ),
    DecisionDisposition(
        "D125",
        "ADD_T15_PRESET",
        "T15 adds the total Sigma^2 -> Sigma* preset over the same OrderedGenerationConcat UPDATE; no new execution algebra is required.",
    ),
    DecisionDisposition(
        "T16/D025",
        "KEEP_T16_RHS_NONEMPTY",
        "No direct T16 deletion evidence exists; T15 epsilon does not broaden the exactly-one splice preset.",
    ),
)


def expect_value_error(action, message: str) -> None:
    try:
        action()
    except ValueError:
        return
    raise AssertionError(message)


def assert_raster_fixtures() -> None:
    assert validate_t15_pair_rows(PAGE_101_RULE.items(), BINARY) == PAGE_101_RULE
    assert native_pair_trace(
        PAGE_101_RULE, PAGE_101_SEED, len(PAGE_101_EXPECTED_TRACE) - 1, BINARY
    ) == PAGE_101_EXPECTED_TRACE
    generic_rows = [encode_native(PAGE_101_SEED, BINARY)]
    for _ in range(len(PAGE_101_EXPECTED_TRACE) - 1):
        generic_rows.append(t15_step(PAGE_101_RULE, generic_rows[-1]).event.successor)
    assert tuple(row.values for row in generic_rows) == PAGE_101_EXPECTED_TRACE

    assert tuple(fixture[0] for fixture in PAGE_102_FIXTURES) == (
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
    )
    assert tuple(
        sum(not output for output in fixture[2].values())
        for fixture in PAGE_102_FIXTURES
    ) == (0, 2, 2, 1, 4, 3)
    for name, alphabet, table, seed, expected_trace in PAGE_102_FIXTURES:
        assert name in {"a", "b", "c", "d", "e", "f"}
        assert validate_t15_pair_rows(table.items(), alphabet) == table
        assert len(table) == len(alphabet.symbols) ** 2
        assert len(expected_trace) == 12
        assert expected_trace[0] == seed
        assert native_pair_trace(
            table, seed, len(expected_trace) - 1, alphabet
        ) == expected_trace
        configuration = encode_native(seed, alphabet)
        reconstructed = [configuration.values]
        for _ in range(len(expected_trace) - 1):
            configuration = t15_step(table, configuration).event.successor
            reconstructed.append(configuration.values)
        assert tuple(reconstructed) == expected_trace


def assert_empty_role_distinctions() -> None:
    # One selected source explicitly returns epsilon.  The event exists, its
    # result record exists, it creates no child, and the empty word is the one
    # valid successor rather than a terminal signal.
    old_pair = encode_native((0, 0), BINARY, generation=7)
    pair_h0, pair_h1 = all_occurrences(old_pair)
    explicit = t15_step(PAGE_101_RULE, old_pair)
    assert len(explicit.successors) == 1
    assert explicit.event.successor.values == ()
    assert explicit.event.emission_records == (
        EmissionRecord(pair_h0, (), 0, 0, ()),
    )
    assert explicit.event.dropped_sources == (pair_h1,)

    # A singleton has zero eligible right-context sources.  It reaches the
    # same empty value, but has no RULE result record at all.
    singleton_old = encode_native((0,), BINARY, generation=7)
    singleton = t15_step(PAGE_101_RULE, singleton_old)
    assert len(singleton.successors) == 1
    assert singleton.event.successor.values == ()
    assert singleton.event.emission_records == ()
    assert singleton.event.dropped_sources == all_occurrences(singleton_old)

    # Applying the source Notes' generic Partition/Flatten operator to the
    # epsilon-capable table derives a vacuous empty successor after extinction.
    # This is not a displayed trace claim and not an invented halt/stutter
    # policy; it is a mathematical consequence of the reconstructed operator.
    empty = t15_step(PAGE_101_RULE, explicit.event.successor)
    assert len(empty.successors) == 1
    assert empty.event.successor.values == ()
    assert empty.event.emission_records == ()
    assert empty.event.dropped_sources == ()

    # T16 NoMatch retains its final state and has zero successors.  Equality
    # of a final word value can never erase this outcome distinction.
    no_match = t16_no_match(encode_native((), BINARY))
    assert len(no_match.successors) == 0
    assert no_match.final.values == () and no_match.reason == "NoMatch"
    tag_terminal = t17_insufficient_prefix(encode_native((0,), BINARY))
    assert len(tag_terminal.successors) == 0
    assert tag_terminal.reason == "InsufficientPrefix"
    assert explicit != no_match and empty != no_match
    assert singleton != tag_terminal


def assert_order_newborn_and_right_edge() -> None:
    # Empty and nonempty emissions coexist in source order.  The zero-length
    # witness occupies [0,0); the following real children begin at 0.  No
    # epsilon symbol or zero-width child is manufactured.
    mixed_old = encode_native((0, 0, 1), BINARY, generation=3)
    mixed_h0, mixed_h1, mixed_h2 = all_occurrences(mixed_old)
    mixed = t15_step(PAGE_101_RULE, mixed_old)
    assert mixed.event.successor.values == (1, 0)
    assert mixed.event.emission_records == (
        EmissionRecord(mixed_h0, (), 0, 0, ()),
        EmissionRecord(
            mixed_h1,
            (1, 0),
            0,
            2,
            (
                ChildRecord(mixed_h1, 0, 0, 1),
                ChildRecord(mixed_h1, 1, 1, 0),
            ),
        ),
    )
    assert mixed.event.dropped_sources == (mixed_h2,)

    # The rightmost old occurrence participates in the preceding read but has
    # no emission of its own and is not copied forward.
    right_old = encode_native((0, 1), BINARY)
    right = t15_step(PAGE_101_RULE, right_old)
    assert read_self_right(right_old, all_right_context_anchors(right_old)) == ((0, 1),)
    assert right.event.successor.values == (1, 0)
    assert right.event.dropped_sources == (all_occurrences(right_old)[1],)

    # All reads are old-snapshot reads and newborns wait until the next event.
    newborn_table = dict(PAGE_101_RULE)
    newborn_table[(0, 0)] = (0, 1)
    first = t15_step(newborn_table, encode_native((0, 0), BINARY))
    assert first.event.successor.values == (0, 1)
    assert len(first.event.emission_records) == 1
    second = t15_step(newborn_table, first.event.successor)
    assert second.event.successor.values == (1, 0)

    # Reversing ordered source-bound writes changes a deliberately asymmetric
    # result, so UPDATE cannot sort by output value or ignore source order.
    asym_old = encode_native((0, 1, 1), BINARY)
    active = all_right_context_anchors(asym_old)
    writes = pair_emissions(
        PAGE_101_RULE, active, read_self_right(asym_old, active)
    )
    assert tuple(value for write in writes for value in write.word) == (1, 0, 1, 1)
    expect_value_error(
        lambda: apply_ordered_generation(asym_old, active, tuple(reversed(writes))),
        "reordered source-bound writes were accepted",
    )


def assert_hostile_validation() -> None:
    assert validate_t15_pair_rows(PAGE_101_RULE.items(), BINARY) == PAGE_101_RULE
    expect_value_error(
        lambda: validate_t14_pair_rows(PAGE_101_RULE.items(), BINARY),
        "strict T14 accepted a T15 epsilon row",
    )
    expect_value_error(
        lambda: validate_t13_morphism(((0, ()), (1, (0,))), BINARY),
        "strict T13 accepted an epsilon row",
    )

    invalid_pair_rows = (
        tuple(PAGE_101_RULE.items())[:-1],
        tuple(PAGE_101_RULE.items()) + (((0, 0), (1,)),),
        tuple(
            ((0, 2), word) if context == (0, 0) else (context, word)
            for context, word in PAGE_101_RULE.items()
        ),
        tuple(
            (context, (2,)) if context == (0, 0) else (context, word)
            for context, word in PAGE_101_RULE.items()
        ),
    )
    for rows in invalid_pair_rows:
        expect_value_error(
            lambda rows=rows: validate_t15_pair_rows(rows, BINARY),
            "malformed T15 pair table was accepted",
        )

    old = encode_native((0, 0, 1), BINARY, generation=9)
    h0, h1 = all_right_context_anchors(old)
    valid_writes = (
        OrderedEmission(h0, ()),
        OrderedEmission(h1, (1, 0)),
    )
    # Same generation and index do not imply identity.  Each independently
    # encoded configuration owns a fresh token.
    same_generation_peer = encode_native((1, 1, 0), BINARY, generation=9)
    foreign_same_generation = all_occurrences(same_generation_peer)[0]
    assert foreign_same_generation.generation == h0.generation == 9
    assert foreign_same_generation.snapshot_token is not old.snapshot_token

    prior = encode_native((0, 0, 1), BINARY, generation=8)
    stale_prior_generation = all_occurrences(prior)[0]
    out_of_range = SourceHandle(old.snapshot_token, 3)
    invalid_results = (
        ((h0, h0), (valid_writes[0], valid_writes[0])),
        ((h1, h0), tuple(reversed(valid_writes))),
        (
            (foreign_same_generation,),
            (OrderedEmission(foreign_same_generation, ()),),
        ),
        (
            (stale_prior_generation,),
            (OrderedEmission(stale_prior_generation, ()),),
        ),
        ((out_of_range,), (OrderedEmission(out_of_range, ()),)),
        ((h0, h1), (valid_writes[0],)),
        ((h0, h1), tuple(reversed(valid_writes))),
        ((h0,), (OrderedEmission(h0, (2,)),)),
    )
    for active, writes in invalid_results:
        expect_value_error(
            lambda active=active, writes=writes: apply_ordered_generation(
                old, active, writes
            ),
            "malformed ordered-generation write set was accepted",
        )

    valid = apply_ordered_generation(old, (h0, h1), valid_writes).event
    epsilon_record = valid.emission_records[0]
    fake_child = ChildRecord(h0, 0, 0, 0)
    fake_epsilon_record = replace(epsilon_record, children=(fake_child,))
    tampered = replace(
        valid,
        emission_records=(fake_epsilon_record, valid.emission_records[1]),
    )
    expect_value_error(
        lambda: validate_generation_witness(old, (h0, h1), tampered),
        "fake child attached to epsilon emission was accepted",
    )

    # A handle selected from the old generation cannot be reused against the
    # successor merely because its integer index still exists.
    successor = valid.successor
    assert successor.snapshot_token is not old.snapshot_token
    assert successor.generation == old.generation + 1
    expect_value_error(
        lambda: read_self_right(successor, (h0,)),
        "old-snapshot handle was accepted in a newborn generation",
    )
    expect_value_error(
        lambda: read_self(old, (foreign_same_generation,)),
        "same-generation foreign handle was accepted for a read",
    )

    # Opaque address identity is not semantic configuration state.
    semantic_peer = encode_native(old.values, old.alphabet, generation=old.generation)
    assert semantic_peer == old
    assert semantic_peer.snapshot_token is not old.snapshot_token


def bounded_words(alphabet: Alphabet, lengths: Iterable[int]) -> tuple[Word, ...]:
    return tuple(
        tuple(word)
        for length in lengths
        for word in product(alphabet.symbols, repeat=length)
    )


def assert_exhaustive_pair_commutation(
    max_input_length: int = 6,
) -> dict[str, int]:
    """Exhaust all binary pair tables with output lengths zero through two."""

    output_words = bounded_words(BINARY, (0, 1, 2))
    input_words = bounded_words(BINARY, range(max_input_length + 1))
    contexts = pair_contexts(BINARY)
    assert len(output_words) == 7
    assert len(contexts) == 4
    assert len(output_words) ** len(contexts) == 2_401
    assert len(input_words) == 127

    counters = {
        "tables": 0,
        "epsilon_tables": 0,
        "commutation_cases": 0,
        "strict_t14_tables": 0,
        "strict_t14_cases": 0,
        "zero_source_cases": 0,
        "explicit_epsilon_cases": 0,
        "explicit_epsilon_records": 0,
        "empty_successor_cases": 0,
        "active_extinction_cases": 0,
    }
    for outputs in product(output_words, repeat=len(contexts)):
        table = dict(zip(contexts, outputs, strict=True))
        assert validate_t15_pair_rows(table.items(), BINARY) == table
        counters["tables"] += 1
        has_epsilon_row = any(not output for output in outputs)
        if has_epsilon_row:
            counters["epsilon_tables"] += 1
            expect_value_error(
                lambda table=table: validate_t14_pair_rows(table.items(), BINARY),
                "strict T14 accepted a bounded epsilon table",
            )
        else:
            assert validate_t14_pair_rows(table.items(), BINARY) == table
            counters["strict_t14_tables"] += 1

        for word in input_words:
            encoded = encode_native(word, BINARY)
            assert decode_generic(encoded) == word
            assert encode_native(decode_generic(encoded), BINARY) == encoded

            native_next = native_pair_step(table, word, BINARY)
            generic = _shared_pair_step(table, encoded)
            assert len(generic.successors) == 1
            assert encode_native(native_next, BINARY) == generic.event.successor
            assert decode_generic(generic.event.successor) == native_next
            assert tuple(record.word for record in generic.event.emission_records) == tuple(
                table[pair] for pair in zip(word, word[1:])
            )
            assert tuple(
                child.value
                for record in generic.event.emission_records
                for child in record.children
            ) == native_next
            counters["commutation_cases"] += 1

            if len(word) < 2:
                assert generic.event.emission_records == ()
                counters["zero_source_cases"] += 1
            epsilon_records = sum(
                not record.word for record in generic.event.emission_records
            )
            if epsilon_records:
                counters["explicit_epsilon_cases"] += 1
                counters["explicit_epsilon_records"] += epsilon_records
            if not native_next:
                counters["empty_successor_cases"] += 1
                if len(word) >= 2:
                    counters["active_extinction_cases"] += 1

            if not has_epsilon_row:
                # ``table`` has already passed the strict public validator;
                # the same private UPDATE must commute on every input.
                counters["strict_t14_cases"] += 1

    assert counters["tables"] == 2_401
    assert counters["epsilon_tables"] == 1_105
    assert counters["commutation_cases"] == 304_927
    assert counters["strict_t14_tables"] == 1_296
    assert counters["strict_t14_cases"] == 164_592
    assert counters["zero_source_cases"] == 7_203
    assert counters["explicit_epsilon_cases"] == 102_388
    assert counters["explicit_epsilon_records"] == 176_988
    assert counters["empty_successor_cases"] == 12_979
    assert counters["active_extinction_cases"] == 5_776
    return counters


def assert_exhaustive_t13_regression(max_input_length: int = 6) -> int:
    """Strict T13 remains Sigma+ while invoking the same private UPDATE."""

    outputs = bounded_words(BINARY, (1, 2))
    inputs = bounded_words(BINARY, range(max_input_length + 1))
    assert len(outputs) == 6 and len(inputs) == 127
    cases = 0
    for raw_outputs in product(outputs, repeat=len(BINARY.symbols)):
        morphism = dict(zip(BINARY.symbols, raw_outputs, strict=True))
        assert validate_t13_morphism(morphism.items(), BINARY) == morphism
        for word in inputs:
            native_next = native_self_step(morphism, word, BINARY)
            generic = _shared_self_step(morphism, encode_native(word, BINARY))
            assert encode_native(native_next, BINARY) == generic.event.successor
            assert len(generic.event.emission_records) == len(word)
            assert all(record.word for record in generic.event.emission_records)
            cases += 1
    assert cases == 4_572
    return cases


def assert_architecture_decisions() -> None:
    assert tuple(row.decision for row in DECISION_MATRIX) == (
        "D019",
        "D020",
        "D024",
        "D028",
        "D124",
        "D125",
        "T16/D025",
    )
    assert tuple(row.action for row in DECISION_MATRIX) == (
        "CLARIFY_PRIVATE_BASE",
        "KEEP_T13_SIGMA_PLUS",
        "EXTEND_OUTCOME_CASES",
        "CONFIRM_SIGMA_STAR_CARRIER",
        "KEEP_T14_SIGMA_PLUS",
        "ADD_T15_PRESET",
        "KEEP_T16_RHS_NONEMPTY",
    )
    assert all("executor" not in row.reason.lower() for row in DECISION_MATRIX)


def main() -> None:
    assert_raster_fixtures()
    assert_empty_role_distinctions()
    assert_order_newborn_and_right_edge()
    assert_hostile_validation()
    pair_counts = assert_exhaustive_pair_commutation()
    t13_cases = assert_exhaustive_t13_regression()
    assert_architecture_decisions()
    print(
        "T15 semantic oracle: PASS "
        f"(bounded_tables={pair_counts['tables']}; "
        f"epsilon_tables={pair_counts['epsilon_tables']}; "
        f"commutation_cases={pair_counts['commutation_cases']}; "
        f"strict_t14_cases={pair_counts['strict_t14_cases']}; "
        f"strict_t13_cases={t13_cases}; "
        f"zero_source_cases={pair_counts['zero_source_cases']}; "
        f"explicit_epsilon_cases={pair_counts['explicit_epsilon_cases']}; "
        f"explicit_epsilon_records={pair_counts['explicit_epsilon_records']}; "
        f"empty_successor_cases={pair_counts['empty_successor_cases']}; "
        f"active_extinction_cases={pair_counts['active_extinction_cases']}; "
        "page101_t0_t11=PASS; page102_fixtures="
        f"{len(PAGE_102_FIXTURES)}; shared_ordered_UPDATE=PASS; "
        "epsilon_record_no_fake_children=PASS; newborn_deferral=PASS; "
        "rightmost_drop=PASS; opaque_snapshot_identity=PASS; "
        "extinction_is_transition=PASS; no_match_is_zero_successor=PASS; "
        "hostile_validation=PASS; decision_matrix=PASS)"
    )


if __name__ == "__main__":
    main()
