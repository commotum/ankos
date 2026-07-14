#!/usr/bin/env python3
"""Dependency-free semantic checks for Goal 1 stage T10.

This is research evidence, not runtime code.  It proves that the factored
``(bit field, active position)`` view and the transparent tagged-cell view
commute for every strict T10 local input/result and several outside contexts.
"""

from __future__ import annotations

from itertools import product


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
    writes = {
        active + offset: (PLAIN, value)
        for offset, value in zip((-1, 0, 1), replacement)
    }
    destination = active + move
    writes[destination] = (ACTIVE, replacement[move + 1])
    successor = dict(cells)
    successor.update(writes)
    return normalize_tagged(successor)


def assert_rule_space() -> None:
    assert len(CONTEXTS) == 8
    assert len(OUTPUTS) * len(MOVES) == 16
    assert 16**8 == 4_294_967_296
    assert set(PAGE_73_RULE) == set(CONTEXTS)


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

                    factored_next = factored_step(rule, (bits, 0))
                    tagged_next = tagged_step(rule, encode(bits, 0))
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
    cases = assert_exhaustive_commutation()
    assert_destination_uses_new_value()
    trace = page_73_trace(12)
    # A replayable checkpoint rather than an image-derived assertion.
    assert trace[:5] == (
        ((), 0),
        ((-1, 0, 1), 1),
        ((-1, 0, 2), 0),
        ((-1, 1, 2), -1),
        ((-1, 0, 1, 2), -2),
    )
    print(
        "T10 semantic oracle: PASS "
        f"({cases} exhaustive commutation cases; rule_space={16**8}; "
        f"page73_checkpoint={trace[:5]})"
    )


if __name__ == "__main__":
    main()
