"""Behavioral tests for the first concrete simple-program preset."""

from __future__ import annotations

import pickle
from collections.abc import Mapping

from ca import Trajectory, rollout, seeds, spaces
from ca.catalog.automata import elementary_ca as eca


def _row(
    state: Mapping[tuple[object, ...], object],
    time: int,
    width: int,
) -> tuple[object, ...]:
    return tuple(state[(time, x)] for x in range(width))


def test_rule_30_uses_wolfram_left_self_right_numbering() -> None:
    rule_30 = eca.rule(30)
    expected = {
        (1, 1, 1): 0,
        (1, 1, 0): 0,
        (1, 0, 1): 0,
        (1, 0, 0): 1,
        (0, 1, 1): 1,
        (0, 1, 0): 1,
        (0, 0, 1): 1,
        (0, 0, 0): 0,
    }

    assert {
        pattern: rule_30(pattern)
        for pattern in expected
    } == expected
    assert eca.ALPHABET == (0, 1)
    assert eca.NEIGHBORHOOD == ((-1,), (0,), (1,))
    assert eca.rule(30) == rule_30
    assert pickle.loads(pickle.dumps(rule_30)) == rule_30
    assert pickle.loads(pickle.dumps(eca.program(30))) == eca.program(30)


def test_rule_30_rollout_and_seed_width_remain_independent() -> None:
    program = eca.program(30)
    episode = rollout(Trajectory(program, eca.centered_seed(7)), limit=2)

    assert _row(episode.states[0], 0, 7) == (0, 0, 0, 1, 0, 0, 0)
    assert _row(episode.states[1], 1, 7) == (0, 0, 1, 1, 1, 0, 0)
    assert _row(episode.states[2], 2, 7) == (0, 1, 1, 0, 0, 1, 0)

    wider = Trajectory(program, eca.centered_seed(9))
    assert wider.seed.shape == (9,)


def test_boundary_choice_changes_edge_reads_without_changing_seed() -> None:
    seed = seeds.dense((1, 0, 0, 0, 0))
    fixed_zero = spaces.cartesian(
        axes=("t", "x"),
        boundary=spaces.fixed(0),
    )
    fixed_one = spaces.cartesian(
        axes=("t", "x"),
        boundary=spaces.fixed(1),
    )
    wrapped = spaces.cartesian(
        axes=("t", "x"),
        boundary=spaces.periodic(),
    )
    fixed = rollout(Trajectory(eca.program(90), seed), limit=1)
    periodic = rollout(
        Trajectory(eca.program(90, space=wrapped), seed),
        limit=1,
    )
    one = rollout(
        Trajectory(eca.program(90, space=fixed_one), seeds.dense((0,) * 5)),
        limit=1,
    )

    assert eca.DEFAULT_SPACE == fixed_zero
    assert tuple(
        eca.programs(numbers=(90,), spaces=(fixed_zero, fixed_one, wrapped))
    ) == (
        eca.program(90, space=fixed_zero),
        eca.program(90, space=fixed_one),
        eca.program(90, space=wrapped),
    )
    assert _row(fixed.states[1], 1, 5) == (0, 1, 0, 0, 0)
    assert _row(periodic.states[1], 1, 5) == (0, 1, 0, 0, 1)
    assert _row(one.states[1], 1, 5) == (1, 0, 0, 0, 1)
