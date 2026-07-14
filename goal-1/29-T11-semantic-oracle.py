#!/usr/bin/env python3
"""Dependency-free semantic checks for Goal 1 stage T11.

This is research evidence, not runtime code.  It models the construction shown
at BOOK:916-934 and the executable ``GMAStep`` at BOOK:12008-12010:

* every cell active in the old state reads the old left/self/right bit triple;
* its row result contains a new value for that old source and relative next-
  active positions;
* old active sources therefore own distinct value writes;
* all proposed next-active positions are combined by exact set union; and
* a factored ``(bit field, active set)`` state commutes with a transparent
  ``Plain(bit) | Active(bit)`` representation.

The page-76 rule glyphs supply relative activity positions ``-1, 0, +1``,
including empty, singleton, pair, and triple subsets.  They therefore give 16
strict row results (two source bits times eight activity subsets).  The oracle
does not invent a finite boundary or decide whether an already-empty frontier
stutters or terminates; ``NoActiveSources`` keeps that source-level outcome
obligation explicit.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from itertools import combinations, permutations, product
from pathlib import Path
from typing import Iterable, Mapping, Sequence


if not __debug__:
    raise RuntimeError("T11 semantic verification requires assertions; do not run with -O")


PLAIN = "plain"
ACTIVE = "active"
BITS = (0, 1)
READ_OFFSETS = (-1, 0, 1)
ACTIVITY_OFFSETS = (-1, 0, 1)
CONTEXTS = tuple(product(BITS, repeat=3))
ACTIVITY_SUBSETS = tuple(
    frozenset(subset)
    for size in range(4)
    for subset in combinations(ACTIVITY_OFFSETS, size)
)
ROW_RESULTS = tuple(product(BITS, ACTIVITY_SUBSETS))


REPO_ROOT = Path(__file__).resolve().parents[1]
PAGE_91_RULE_ASSET = (
    REPO_ROOT
    / "ref/A-New-Kind-of-Science/CHAPTERS/3-The-World-of-Simple-Programs/Images"
    / "_page_91_Figure_6.jpeg"
)
PAGE_91_RULE_ASSET_SHA256 = (
    "841e52174bee649faa4f32c351235609b41f08d875351f4e04e328fe1d0dc3db"
)


# BOOK:922.  This is a derived visual transcription of the hash-bound native
# rule strip, not a source-defined integer code.  Rows are physical L/C/R.
PAGE_91_RULE: Rule = {
    (1, 1, 1): (0, frozenset({1})),
    (1, 1, 0): (0, frozenset({1})),
    (1, 0, 1): (1, frozenset({1})),
    (1, 0, 0): (1, frozenset({0, 1})),
    (0, 1, 1): (1, frozenset({-1})),
    (0, 1, 0): (1, frozenset({-1, 1})),
    (0, 0, 1): (1, frozenset({-1})),
    (0, 0, 0): (1, frozenset({-1, 1})),
}


# Independently recomputed from PAGE_91_RULE, an all-zero field, and A_0={0}.
# Each row is (positions whose underlying bit is 1, active positions).
EXPECTED_PAGE_91_TRACE = (
    ((), (0,)),
    ((0,), (-1, 1)),
    ((-1, 0, 1), (-2, 1, 2)),
    ((-2, -1, 0, 2), (-3, 2, 3)),
    ((-3, -2, -1, 0, 2, 3), (-4, 1, 3, 4)),
    ((-4, -3, -2, -1, 0, 1, 2, 4), (-5, 2, 4, 5)),
    ((-5, -4, -3, -2, -1, 0, 1, 4, 5), (-6, 3, 5, 6)),
    ((-6, -5, -4, -3, -2, -1, 0, 1, 3, 4, 6), (-7, 2, 6, 7)),
    ((-7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 6, 7), (-8, 3, 5, 7, 8)),
    ((-8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 4, 5, 6, 8), (-9, 4, 6, 8, 9)),
    ((-9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 4, 5, 8, 9), (-10, 3, 7, 9, 10)),
    ((-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 7, 8, 10), (-11, 4, 6, 10, 11)),
    ((-11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 5, 6, 7, 8, 10, 11), (-12, 5, 7, 9, 11, 12)),
)


class NoActiveSources(RuntimeError):
    """The book does not specify rollout behavior from an empty active set."""


@dataclass(frozen=True)
class Event:
    source: int
    read: tuple[int, int, int]
    new_source_bit: int
    relative_activity: frozenset[int]
    proposed_activity: frozenset[int]


Rule = dict[tuple[int, int, int], tuple[int, frozenset[int]]]
Bits = dict[int, int]
ActiveSet = frozenset[int]
Cell = tuple[str, int]
Tagged = dict[int, Cell]


def normalize_bits(bits: Mapping[int, int]) -> Bits:
    """Canonical sparse binary field with implicit zero default."""
    assert all(isinstance(position, int) for position in bits)
    assert all(value in BITS for value in bits.values())
    return {int(position): int(value) for position, value in bits.items() if value}


def normalize_active(active: Iterable[int]) -> ActiveSet:
    assert all(isinstance(position, int) for position in active)
    return frozenset(int(position) for position in active)


def normalize_offsets(offsets: Iterable[int]) -> frozenset[int]:
    """Operational normalization induced by Union[Flatten[...]]."""
    assert all(isinstance(offset, int) for offset in offsets)
    return frozenset(int(offset) for offset in offsets)


def normalize_tagged(cells: Mapping[int, Cell]) -> Tagged:
    assert all(isinstance(position, int) for position in cells)
    assert all(tag in (PLAIN, ACTIVE) and value in BITS for tag, value in cells.values())
    return {
        int(position): (tag, int(value))
        for position, (tag, value) in cells.items()
        if (tag, value) != (PLAIN, 0)
    }


def encode(bits: Mapping[int, int], active: Iterable[int]) -> Tagged:
    """Tag every active position while retaining its underlying bit."""
    normalized_bits = normalize_bits(bits)
    normalized_active = normalize_active(active)
    cells: Tagged = {
        position: (PLAIN, value) for position, value in normalized_bits.items()
    }
    for position in normalized_active:
        cells[position] = (ACTIVE, normalized_bits.get(position, 0))
    return normalize_tagged(cells)


def decode(cells: Mapping[int, Cell]) -> tuple[Bits, ActiveSet]:
    normalized = normalize_tagged(cells)
    bits = normalize_bits(
        {position: value for position, (_tag, value) in normalized.items()}
    )
    active = frozenset(
        position for position, (tag, _value) in normalized.items() if tag == ACTIVE
    )
    return bits, active


def read_context(bits: Mapping[int, int], source: int) -> tuple[int, int, int]:
    normalized = normalize_bits(bits)
    return tuple(normalized.get(source + offset, 0) for offset in READ_OFFSETS)  # type: ignore[return-value]


def table_from_rows(
    rows: Sequence[
        tuple[tuple[int, int, int], tuple[int, Iterable[int]]]
    ],
) -> Rule:
    """Build a closed table while rejecting duplicate or missing contexts."""
    table: Rule = {}
    for context, (new_bit, offsets) in rows:
        assert context in CONTEXTS
        assert context not in table
        assert new_bit in BITS
        table[context] = (int(new_bit), normalize_offsets(offsets))
    assert set(table) == set(CONTEXTS)
    return table


def constant_rule(new_bit: int, offsets: Iterable[int]) -> Rule:
    normalized_offsets = normalize_offsets(offsets)
    return table_from_rows(
        tuple((context, (new_bit, normalized_offsets)) for context in CONTEXTS)
    )


def evaluate_old_snapshot(
    rule: Rule,
    bits: Mapping[int, int],
    active: Iterable[int],
    source_order: Sequence[int] | None = None,
) -> tuple[Event, ...]:
    """Evaluate every old active source before applying any value write."""
    normalized_bits = normalize_bits(bits)
    normalized_active = normalize_active(active)
    if not normalized_active:
        raise NoActiveSources("T11 source semantics from an empty frontier are unspecified")

    order = tuple(sorted(normalized_active)) if source_order is None else tuple(source_order)
    assert len(order) == len(normalized_active) and set(order) == set(normalized_active)
    assert set(rule) == set(CONTEXTS)

    events = []
    for source in order:
        context = read_context(normalized_bits, source)
        new_bit, relative = rule[context]
        assert new_bit in BITS
        relative = normalize_offsets(relative)
        events.append(
            Event(
                source=source,
                read=context,
                new_source_bit=new_bit,
                relative_activity=relative,
                proposed_activity=frozenset(source + offset for offset in relative),
            )
        )
    return tuple(events)


def apply_events_factored(
    state: tuple[Mapping[int, int], Iterable[int]],
    events: Sequence[Event],
) -> tuple[Bits, ActiveSet]:
    """Apply distinct source-value assignments plus activity-set union."""
    bits, active = state
    bits = normalize_bits(bits)
    active = normalize_active(active)
    assert {event.source for event in events} == set(active)
    assert len({event.source for event in events}) == len(events)

    successor_bits = dict(bits)
    for event in events:
        successor_bits[event.source] = event.new_source_bit

    successor_active = frozenset(
        position
        for event in events
        for position in event.proposed_activity
    )
    return normalize_bits(successor_bits), successor_active


def factored_step(
    rule: Rule,
    state: tuple[Mapping[int, int], Iterable[int]],
    source_order: Sequence[int] | None = None,
) -> tuple[tuple[Bits, ActiveSet], tuple[Event, ...]]:
    bits, active = state
    events = evaluate_old_snapshot(rule, bits, active, source_order)
    return apply_events_factored((bits, active), events), events


def commit_complete_tagged_writes(cells: Mapping[int, Cell], events: Sequence[Event]) -> Tagged:
    """Lower the factored result to one conflict-free atomic cell-write map.

    Activity proposals may collide, but they are first combined as a set.  Each
    old source owns its value write.  Complete writes are needed only on the
    union of old active sources and next-active positions.
    """
    normalized_cells = normalize_tagged(cells)
    old_bits, old_active = decode(normalized_cells)
    assert {event.source for event in events} == set(old_active)
    assert len({event.source for event in events}) == len(events)

    value_writes = {event.source: event.new_source_bit for event in events}
    next_active = frozenset(
        position
        for event in events
        for position in event.proposed_activity
    )
    targets = old_active | next_active

    writes: Tagged = {}
    for target in targets:
        next_bit = value_writes.get(target, old_bits.get(target, 0))
        writes[target] = (ACTIVE if target in next_active else PLAIN, next_bit)

    successor = dict(normalized_cells)
    successor.update(writes)
    return normalize_tagged(successor)


def tagged_step(rule: Rule, cells: Mapping[int, Cell]) -> tuple[Tagged, tuple[Event, ...]]:
    bits, active = decode(cells)
    (next_bits, next_active), events = factored_step(rule, (bits, active))
    committed = commit_complete_tagged_writes(cells, events)
    assert committed == encode(next_bits, next_active)
    return committed, events


def events_from_results(
    bits: Mapping[int, int],
    results: Mapping[int, tuple[int, Iterable[int]]],
) -> tuple[Event, ...]:
    """Build old-snapshot events directly for exhaustive composition testing."""
    normalized_bits = normalize_bits(bits)
    events = []
    for source in sorted(results):
        new_bit, offsets = results[source]
        assert new_bit in BITS
        relative = normalize_offsets(offsets)
        events.append(
            Event(
                source=source,
                read=read_context(normalized_bits, source),
                new_source_bit=int(new_bit),
                relative_activity=relative,
                proposed_activity=frozenset(source + offset for offset in relative),
            )
        )
    return tuple(events)


def assert_rule_schema() -> None:
    assert len(CONTEXTS) == 8
    assert len(ACTIVITY_SUBSETS) == 8
    assert set(ACTIVITY_SUBSETS) == {
        frozenset(subset) for mask in range(8)
        for subset in [
            tuple(offset for index, offset in enumerate(ACTIVITY_OFFSETS) if mask & (1 << index))
        ]
    }
    assert len(ROW_RESULTS) == 16
    assert 16**8 == 4_294_967_296

    # Final Union makes ordering and duplicate activity proposals operationally
    # irrelevant even if a source rule was written using a list.
    assert normalize_offsets((1, -1, 0, 1)) == frozenset((-1, 0, 1))


def assert_page_91_asset_and_rule() -> None:
    assert PAGE_91_RULE_ASSET.is_file()
    digest = hashlib.sha256(PAGE_91_RULE_ASSET.read_bytes()).hexdigest()
    assert digest == PAGE_91_RULE_ASSET_SHA256
    assert set(PAGE_91_RULE) == set(CONTEXTS)
    assert all(result in ROW_RESULTS for result in PAGE_91_RULE.values())

    # The visually easy-to-misread 000 result has left/right activity only;
    # the center output cell is not active.
    assert PAGE_91_RULE[(0, 0, 0)] == (1, frozenset({-1, 1}))

    # Optional derived bit planes under i = 4L + 2C + R.  These are a guarded
    # transcription aid, not a source-defined generalized-mobile codec.
    planes = [0, 0, 0, 0]
    for index in range(8):
        context = ((index >> 2) & 1, (index >> 1) & 1, index & 1)
        new_bit, activity = PAGE_91_RULE[context]
        flags = (new_bit, -1 in activity, 0 in activity, 1 in activity)
        for plane, flag in enumerate(flags):
            planes[plane] |= int(flag) << index
    assert tuple(planes) == (63, 15, 16, 245)


def assert_table_validation() -> None:
    rule = constant_rule(0, ())
    assert set(rule) == set(CONTEXTS)

    missing = tuple((context, (0, ())) for context in CONTEXTS[:-1])
    try:
        table_from_rows(missing)
    except AssertionError:
        pass
    else:
        raise AssertionError("missing table row was accepted")

    duplicate = tuple((context, (0, ())) for context in CONTEXTS) + (
        (CONTEXTS[0], (1, (0,))),
    )
    try:
        table_from_rows(duplicate)
    except AssertionError:
        pass
    else:
        raise AssertionError("duplicate table row was accepted")


def assert_exhaustive_composition_commutation() -> int:
    """Cover every strict result combination for up to three nearby sources."""
    cases = 0
    source_universe = (-1, 0, 1)
    bit_positions = (-2, -1, 0, 1, 2)

    for bit_values in product(BITS, repeat=len(bit_positions)):
        bits = {
            position: value
            for position, value in zip(bit_positions, bit_values)
            if value
        }
        for source_count in range(1, len(source_universe) + 1):
            for sources in combinations(source_universe, source_count):
                active = frozenset(sources)
                for row_results in product(ROW_RESULTS, repeat=source_count):
                    results = dict(zip(sources, row_results))
                    events = events_from_results(bits, results)
                    next_bits, next_active = apply_events_factored((bits, active), events)

                    encoded = encode(bits, active)
                    assert decode(encoded) == (normalize_bits(bits), active)
                    assert encode(*decode(encoded)) == encoded

                    committed = commit_complete_tagged_writes(encoded, events)
                    assert committed == encode(next_bits, next_active)
                    assert decode(committed) == (next_bits, next_active)
                    cases += 1
    return cases


def assert_notes_split_and_newborn_schedule() -> None:
    # BOOK:12008's displayed result 000 -> {1,{1,-1}}.  The source changes;
    # the two newborn active destinations retain their old underlying bits and
    # do not themselves fire during this event.
    rule = constant_rule(1, (1, -1))
    successor, events = tagged_step(rule, encode({}, {0}))
    assert len(events) == 1
    assert events[0].read == (0, 0, 0)
    assert successor == {
        -1: (ACTIVE, 0),
        0: (PLAIN, 1),
        1: (ACTIVE, 0),
    }


def assert_notes_wider_finite_offsets() -> None:
    # BOOK:12008 types the result as relative positions without stating a
    # radius-one limit.  The page-76 glyph profile is stricter than this
    # executable carrier, so a wider finite literal set must still commute.
    rule = constant_rule(1, (-7, 0, 9))
    successor, events = tagged_step(rule, encode({}, {4}))
    assert len(events) == 1
    assert events[0].relative_activity == frozenset({-7, 0, 9})
    assert decode(successor) == ({4: 1}, frozenset({-3, 4, 13}))


def assert_activity_collision_is_union() -> None:
    bits = {1: 1}
    active = {-1, 1}
    results = {
        -1: (1, (1,)),
        1: (0, (-1,)),
    }
    events = events_from_results(bits, results)
    next_bits, next_active = apply_events_factored((bits, active), events)
    assert next_active == frozenset({0})
    assert sum(0 in event.proposed_activity for event in events) == 2

    committed = commit_complete_tagged_writes(encode(bits, active), events)
    assert committed == encode(next_bits, {0})
    assert committed[0] == (ACTIVE, 0)  # destination color is preserved


def assert_source_destination_overlap() -> None:
    # Source 0 activates old source 1 while source 1 writes its own new bit and
    # emits no children.  The complete result at 1 is Active(new_source_bit).
    bits: Bits = {}
    active = {0, 1}
    events = events_from_results(bits, {0: (0, (1,)), 1: (1, ())})
    next_bits, next_active = apply_events_factored((bits, active), events)
    assert next_active == frozenset({1})
    committed = commit_complete_tagged_writes(encode(bits, active), events)
    assert committed == encode(next_bits, next_active)
    assert committed[1] == (ACTIVE, 1)


def assert_disappearance_and_empty_outcome_obligation() -> None:
    bits: Bits = {}
    active = {-1, 1}
    events = events_from_results(bits, {-1: (1, ()), 1: (1, ())})
    next_bits, next_active = apply_events_factored((bits, active), events)
    assert next_active == frozenset()
    committed = commit_complete_tagged_writes(encode(bits, active), events)
    assert committed == encode(next_bits, ())
    assert all(tag == PLAIN for tag, _value in committed.values())

    try:
        factored_step(constant_rule(0, ()), (next_bits, next_active))
    except NoActiveSources:
        pass
    else:
        raise AssertionError("oracle silently invented empty-frontier continuation")


def assert_old_snapshot_not_sequential() -> None:
    # Both adjacent sources initially read 000.  Source 0 writes 1.  A wrong
    # in-place schedule would then let source 1 read 100 and choose another row.
    rows = []
    for context in CONTEXTS:
        if context == (0, 0, 0):
            rows.append((context, (1, (1,))))
        elif context == (1, 0, 0):
            rows.append((context, (0, (-1,))))
        else:
            rows.append((context, (0, ())))
    rule = table_from_rows(tuple(rows))

    (next_bits, next_active), events = factored_step(rule, ({}, {0, 1}))
    assert tuple(event.read for event in events) == ((0, 0, 0), (0, 0, 0))
    assert next_bits == {0: 1, 1: 1}
    assert next_active == frozenset({1, 2})

    sequential_bits: Bits = {}
    sequential_active: set[int] = set()
    for source in (0, 1):
        context = read_context(sequential_bits, source)
        new_bit, offsets = rule[context]
        sequential_bits[source] = new_bit
        sequential_active.update(source + offset for offset in offsets)
    sequential_bits = normalize_bits(sequential_bits)
    assert sequential_bits == {0: 1}
    assert sequential_active == {0, 1}
    assert (sequential_bits, frozenset(sequential_active)) != (next_bits, next_active)


def assert_source_order_is_nonsemantic() -> None:
    bits = {-2: 1, 0: 1, 2: 1}
    active = {-1, 0, 1}
    rule = {}
    for index, context in enumerate(CONTEXTS):
        subset = ACTIVITY_SUBSETS[index]
        rule[context] = (index % 2, subset)

    expected = factored_step(rule, (bits, active))[0]
    for order in permutations(active):
        assert factored_step(rule, (bits, active), order)[0] == expected


def assert_target_local_ca_needs_radius_two() -> None:
    # Target 0 receives activity from source 1 at offset -1.  Two states agree
    # on the target's complete tagged radius-one neighborhood (-1,0,1) but
    # differ at 2, which changes source 1's row and therefore target activity.
    rows = []
    for context in CONTEXTS:
        offsets = (-1,) if context == (0, 0, 0) else ()
        rows.append((context, (0, offsets)))
    rule = table_from_rows(tuple(rows))

    low = encode({}, {1})
    high = encode({2: 1}, {1})
    assert tuple(low.get(x, (PLAIN, 0)) for x in (-1, 0, 1)) == tuple(
        high.get(x, (PLAIN, 0)) for x in (-1, 0, 1)
    )
    low_next, _events = tagged_step(rule, low)
    high_next, _events = tagged_step(rule, high)
    assert low_next.get(0, (PLAIN, 0))[0] == ACTIVE
    assert high_next.get(0, (PLAIN, 0))[0] == PLAIN


def page_91_trace(steps: int) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    state: tuple[Bits, ActiveSet] = ({}, frozenset({0}))
    trace = []
    for _ in range(steps + 1):
        bits, active = state
        trace.append((tuple(sorted(bits)), tuple(sorted(active))))
        state, _events = factored_step(PAGE_91_RULE, state)
    return tuple(trace)


def main() -> None:
    assert_rule_schema()
    assert_page_91_asset_and_rule()
    assert_table_validation()
    cases = assert_exhaustive_composition_commutation()
    assert_notes_split_and_newborn_schedule()
    assert_notes_wider_finite_offsets()
    assert_activity_collision_is_union()
    assert_source_destination_overlap()
    assert_disappearance_and_empty_outcome_obligation()
    assert_old_snapshot_not_sequential()
    assert_source_order_is_nonsemantic()
    assert_target_local_ca_needs_radius_two()
    trace = page_91_trace(12)
    assert trace == EXPECTED_PAGE_91_TRACE
    print(
        "T11 semantic oracle: PASS "
        f"({cases} exhaustive composition/representation cases; "
        f"contexts={len(CONTEXTS)}; row_results={len(ROW_RESULTS)}; "
        f"derived_rule_space={len(ROW_RESULTS) ** len(CONTEXTS)}; "
        "old_snapshot=PASS; activity_union=PASS; split/disappear/offset0=PASS; "
        "wider_finite_offsets=PASS; derived_planes=PASS; "
        "collision/source-overlap=PASS; source_order=PASS; "
        "radius2_CA_witness=PASS; page91_hash/rule/t0_t12=PASS; "
        "empty_frontier_outcome=UNSPECIFIED)"
    )


if __name__ == "__main__":
    main()
