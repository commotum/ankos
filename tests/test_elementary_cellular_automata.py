"""Behavioral tests for the first concrete simple-program preset."""

from __future__ import annotations

from collections.abc import Mapping

from ca import Seed, Trajectory, rollout
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
        pattern: rule_30(pattern, (0, 0))
        for pattern in expected
    } == expected


def test_rule_30_rollout_and_seed_width_remain_independent() -> None:
    program = eca.program(30)
    episode = rollout(Trajectory(program, eca.centered_seed(7)), limit=2)

    assert _row(episode.states[0], 0, 7) == (0, 0, 0, 1, 0, 0, 0)
    assert _row(episode.states[1], 1, 7) == (0, 0, 1, 1, 1, 0, 0)
    assert _row(episode.states[2], 2, 7) == (0, 1, 1, 0, 0, 1, 0)

    wider = Trajectory(program, eca.centered_seed(9))
    assert wider.seed.shape == (9,)


def test_boundary_choice_changes_edge_reads_without_changing_seed() -> None:
    seed = Seed(
        shape=(5,),
        values={(0, x): int(x == 0) for x in range(5)},
    )
    fixed = rollout(Trajectory(eca.program(90), seed), limit=1)
    periodic = rollout(
        Trajectory(eca.program(90, boundary=eca.PERIODIC), seed),
        limit=1,
    )

    assert _row(fixed.states[1], 1, 5) == (0, 1, 0, 0, 0)
    assert _row(periodic.states[1], 1, 5) == (0, 1, 0, 0, 1)
