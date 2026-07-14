#!/usr/bin/env python3
"""Dependency-free semantic checks for Goal 1 stage T10.

This is research evidence, not runtime code.  It proves that the factored
``(bit field, active position)`` view and the transparent tagged-cell view
commute for every strict T10 local input/result and several outside contexts.
"""

from __future__ import annotations

from itertools import product


if not __debug__:
    raise RuntimeError("T10 semantic verification requires assertions; do not run with -O")


PLAIN = "plain"
ACTIVE = "active"
CONTEXTS = tuple(product((0, 1), repeat=3))
OUTPUTS = tuple(product((0, 1), repeat=3))
MOVES = (-1, 1)


# BOOK:11982-11993, the page-73 extended-mobile rule.
PAGE_73_RULE = {
    (1, 1, 1): ((0, 0, 0), -1),
    (1, 1, 0): ((1, 0, 1), -1),
    (1, 0, 1): ((1, 1, 1), 1),
    (1, 0, 0): ((1, 0, 0), 1),
    (0, 1, 1): ((0, 0, 0), 1),
    (0, 1, 0): ((0, 1, 1), -1),
    (0, 0, 1): ((1, 0, 1), 1),
    (0, 0, 0): ((1, 1, 1), 1),
}

EXPECTED_PAGE_73_TRACE = (
    ((), 0),
    ((-1, 0, 1), 1),
    ((-1, 0, 2), 0),
    ((-1, 1, 2), -1),
    ((-1, 0, 1, 2), -2),
    ((-3, -1, 0, 1, 2), -1),
    ((-3, 1, 2), 0),
    ((-3, -1, 1, 2), 1),
    ((-3, -1), 2),
    ((-3, -1, 1, 2, 3), 3),
    ((-3, -1, 1, 2, 4), 2),
    ((-3, -1, 1, 3, 4), 1),
    ((-3, -1, 1, 2, 3, 4), 0),
)


def normalize_bits(bits: dict[int, int]) -> dict[int, int]:
    """Canonical sparse binary field with implicit zero default."""
    assert all(value in (0, 1) for value in bits.values())
    return {position: value for position, value in bits.items() if value}


def normalize_tagged(cells: dict[int, tuple[str, int]]) -> dict[int, tuple[str, int]]:
    """Canonical sparse tagged field; Plain(0) is the implicit default."""
    assert all(tag in (PLAIN, ACTIVE) and value in (0, 1) for tag, value in cells.values())
    active = [position for position, (tag, _value) in cells.items() if tag == ACTIVE]
    assert len(active) == 1
    return {
        position: cell
        for position, cell in cells.items()
        if cell != (PLAIN, 0)
    }


def encode(bits: dict[int, int], active: int) -> dict[int, tuple[str, int]]:
    """Losslessly tag the active cell while retaining its underlying bit."""
    normalized = normalize_bits(bits)
    cells = {position: (PLAIN, value) for position, value in normalized.items()}
    cells[active] = (ACTIVE, normalized.get(active, 0))
    return normalize_tagged(cells)


def decode(cells: dict[int, tuple[str, int]]) -> tuple[dict[int, int], int]:
    cells = normalize_tagged(cells)
    active_positions = [
        position for position, (tag, _value) in cells.items() if tag == ACTIVE
    ]
    assert len(active_positions) == 1
    bits = normalize_bits({position: value for position, (_tag, value) in cells.items()})
    return bits, active_positions[0]


def factored_step(
    rule: dict[tuple[int, int, int], tuple[tuple[int, int, int], int]],
    state: tuple[dict[int, int], int],
) -> tuple[dict[int, int], int]:
    bits, active = state
    bits = normalize_bits(bits)
    read = tuple(bits.get(active + offset, 0) for offset in (-1, 0, 1))
    replacement, move = rule[read]
    assert replacement in OUTPUTS and move in MOVES

    successor = dict(bits)
    for offset, value in zip((-1, 0, 1), replacement):
        successor[active + offset] = value
    return normalize_bits(successor), active + move


def lower_result(
    active: int,
    result: tuple[tuple[int, int, int], int],
) -> dict[int, tuple[str, int]]:
    """Losslessly lower one native block/direction result to three label writes."""
    replacement, move = result
    assert replacement in OUTPUTS and move in MOVES
    writes = {
        active + offset: (PLAIN, value)
        for offset, value in zip((-1, 0, 1), replacement)
    }
    writes[active + move] = (ACTIVE, replacement[move + 1])
    return writes


def unlower_result(
    active: int,
    writes: dict[int, tuple[str, int]],
) -> tuple[tuple[int, int, int], int]:
    """Recover the native result from a valid strict-T10 three-write bundle."""
    assert set(writes) == {active - 1, active, active + 1}
    assert all(tag in (PLAIN, ACTIVE) and value in (0, 1) for tag, value in writes.values())
    tagged_offsets = tuple(
        offset for offset in (-1, 0, 1) if writes[active + offset][0] == ACTIVE
    )
    assert len(tagged_offsets) == 1 and tagged_offsets[0] in MOVES
    move = tagged_offsets[0]
    assert writes[active][0] == PLAIN
    assert all(
        writes[active + offset][0] == (ACTIVE if offset == move else PLAIN)
        for offset in (-1, 0, 1)
    )
    replacement = tuple(writes[active + offset][1] for offset in (-1, 0, 1))
    return replacement, move  # type: ignore[return-value]


def tagged_step(
    rule: dict[tuple[int, int, int], tuple[tuple[int, int, int], int]],
    cells: dict[int, tuple[str, int]],
) -> dict[int, tuple[str, int]]:
    cells = normalize_tagged(cells)
    active = next(
        position for position, (tag, _value) in cells.items() if tag == ACTIVE
    )

    def old_bit(position: int) -> int:
        return cells.get(position, (PLAIN, 0))[1]

    read = tuple(old_bit(active + offset) for offset in (-1, 0, 1))
    replacement, move = rule[read]
    assert replacement in OUTPUTS and move in MOVES

    # All complete label writes are derived from the same old snapshot.  The
    # destination tag is attached to its NEW replacement value, not its old bit.
    writes = lower_result(active, (replacement, move))
    successor = dict(cells)
    successor.update(writes)
    return normalize_tagged(successor)


def assert_rule_space() -> None:
    assert len(CONTEXTS) == 8
    assert len(OUTPUTS) * len(MOVES) == 16
    assert 16**8 == 4_294_967_296
    assert set(PAGE_73_RULE) == set(CONTEXTS)


def derived_plane_codes(
    rule: dict[tuple[int, int, int], tuple[tuple[int, int, int], int]],
) -> tuple[int, int, int, int]:
    """Optional inferred codec: i=4L+2C+R and direction bit 1 means left."""
    codes = [0, 0, 0, 0]
    for context, (replacement, move) in rule.items():
        index = 4 * context[0] + 2 * context[1] + context[2]
        for output_offset, value in enumerate(replacement):
            codes[output_offset] |= value << index
        codes[3] |= (move == -1) << index
    return tuple(codes)  # type: ignore[return-value]


def assert_exhaustive_commutation() -> int:
    cases = 0
    for context in CONTEXTS:
        for replacement in OUTPUTS:
            for move in MOVES:
                for outside in product((0, 1), repeat=4):
                    bits = {
                        position: value
                        for position, value in zip(
                            (-3, -2, -1, 0, 1, 2, 3),
                            outside[:2] + context + outside[2:],
                        )
                    }
                    # Only the selected row matters, but a total table is part
                    # of strict T10 identity.
                    rule = {candidate: ((0, 0, 0), -1) for candidate in CONTEXTS}
                    rule[context] = (replacement, move)

                    lowered = lower_result(0, (replacement, move))
                    assert unlower_result(0, lowered) == (replacement, move)
                    encoded = encode(bits, 0)
                    assert decode(encoded) == (normalize_bits(bits), 0)
                    assert encode(*decode(encoded)) == encoded

                    factored_next = factored_step(rule, (bits, 0))
                    tagged_next = tagged_step(rule, encoded)
                    assert tagged_next == encode(*factored_next)

                    next_bits, next_active = factored_next
                    assert next_active == move
                    assert tuple(next_bits.get(offset, 0) for offset in (-1, 0, 1)) == replacement
                    assert next_bits.get(-3, 0) == outside[0]
                    assert next_bits.get(-2, 0) == outside[1]
                    assert next_bits.get(2, 0) == outside[2]
                    assert next_bits.get(3, 0) == outside[3]
                    assert sum(tag == ACTIVE for tag, _value in tagged_next.values()) == 1
                    cases += 1
    return cases


def assert_destination_uses_new_value() -> None:
    # The all-zero page-73 row writes 111 and moves right.  T09-style movement
    # would preserve the old destination bit (0); strict T10 must yield Active(1).
    cells = encode({}, 0)
    successor = tagged_step(PAGE_73_RULE, cells)
    assert successor[1] == (ACTIVE, 1)
    assert successor[-1] == (PLAIN, 1)
    assert successor[0] == (PLAIN, 1)


def assert_target_local_ca_needs_radius_two() -> None:
    # Target 0 is immediately left of the active source at 1.  These states
    # agree on the target's complete radius-one tagged neighborhood (-1,0,1)
    # but differ at 2, the active source's opposite neighbor.  The page-73 rows
    # 110 -> 101 and 111 -> 000 therefore give different next bits at target 0.
    low = encode({0: 1, 1: 1}, 1)
    high = encode({0: 1, 1: 1, 2: 1}, 1)
    assert tuple(low.get(x, (PLAIN, 0)) for x in (-1, 0, 1)) == tuple(
        high.get(x, (PLAIN, 0)) for x in (-1, 0, 1)
    )
    assert tagged_step(PAGE_73_RULE, low).get(0, (PLAIN, 0))[1] == 1
    assert tagged_step(PAGE_73_RULE, high).get(0, (PLAIN, 0))[1] == 0


def page_73_trace(steps: int) -> tuple[tuple[tuple[int, ...], int], ...]:
    state: tuple[dict[int, int], int] = ({}, 0)
    trace = []
    for _ in range(steps + 1):
        bits, active = state
        trace.append((tuple(sorted(bits)), active))
        state = factored_step(PAGE_73_RULE, state)
    return tuple(trace)


def main() -> None:
    assert_rule_space()
    assert derived_plane_codes(PAGE_73_RULE) == (115, 37, 103, 196)
    cases = assert_exhaustive_commutation()
    assert_destination_uses_new_value()
    assert_target_local_ca_needs_radius_two()
    trace = page_73_trace(12)
    # A complete replayable t0..t12 fixture rather than an image-derived assertion.
    assert trace == EXPECTED_PAGE_73_TRACE
    print(
        "T10 semantic oracle: PASS "
        f"({cases} exhaustive commutation cases; rule_space={16**8}; "
        f"derived_planes={derived_plane_codes(PAGE_73_RULE)}; "
        f"page73_t0_t12=PASS(last={trace[-1]}); lowering_inverse=PASS; "
        f"radius2_CA_witness=PASS)"
    )


if __name__ == "__main__":
    main()
