"""Behavioral tests for complete immutable successor construction."""

from __future__ import annotations

from ca import Seed, SimpleProgram, Space, Trajectory, rollout, selector, spaces, step


def _binary_line(
    values: tuple[int, ...],
    *,
    boundary: object,
    normalize: object = None,
    neighborhood: object = ((0, -1), (0, 0), (0, 1)),
    rule: object,
) -> Trajectory:
    program = SimpleProgram(
        space=Space(
            axes=("t", "x"),
            extent="finite-from-seed",
            boundary=boundary,
            coordinates=spaces.box_coordinates,
            normalize=normalize,
        ),
        alphabet=frozenset({0, 1}),
        neighborhood=neighborhood,
        rule=rule,
    )
    seed = Seed(
        shape=(len(values),),
        values={(0, x): value for x, value in enumerate(values)},
    )
    return Trajectory(program, seed)


def _any_observed(
    observed: tuple[object, ...],
    coordinate: tuple[object, ...],
) -> int:
    del coordinate
    return int(any(observed))


def _left_value(
    observed: tuple[object, ...],
    coordinate: tuple[object, ...],
) -> object:
    del coordinate
    return observed[0]


def test_cartesian_rollout_constructs_complete_immutable_slices() -> None:
    trajectory = _binary_line(
        (1, 0, 0),
        boundary=spaces.fixed(0),
        rule=_any_observed,
    )

    episode = rollout(trajectory, 2)

    assert tuple(episode.states[0].items()) == (
        ((0, 0), 1),
        ((0, 1), 0),
        ((0, 2), 0),
    )
    assert dict(episode.states[1]) == {(1, 0): 1, (1, 1): 1, (1, 2): 0}
    assert dict(episode.states[2]) == {(2, 0): 1, (2, 1): 1, (2, 2): 1}

    try:
        episode.states[0][(0, 0)] = 0
    except TypeError:
        pass
    else:
        raise AssertionError("Episode State was mutable")
    assert episode.states[0][(0, 0)] == 1


def test_periodic_and_fixed_boundaries_differ_at_edge() -> None:
    fixed = _binary_line(
        (0, 0, 1),
        boundary=spaces.fixed(0),
        neighborhood=((0, -1),),
        rule=_left_value,
    )
    periodic = _binary_line(
        (0, 0, 1),
        boundary="periodic",
        normalize=spaces.box_wrap,
        neighborhood=((0, -1),),
        rule=_left_value,
    )

    assert step(fixed, fixed.seed.values)[(1, 0)] == 0
    assert step(periodic, periodic.seed.values)[(1, 0)] == 1


def test_relational_rollout_uses_seed_adjacency() -> None:
    program = SimpleProgram(
        space=Space(
            axes=("t", "v"),
            extent="finite-from-seed",
            boundary=None,
            coordinates=spaces.relation_coordinates,
        ),
        alphabet=frozenset({0, 1}),
        neighborhood=selector.adjacent,
        rule=_any_observed,
    )
    seed = Seed(
        shape=("a", "b", "c"),
        values={(0, "a"): 1, (0, "b"): 0, (0, "c"): 0},
        relations={
            "adjacent": {
                "a": ("b",),
                "b": ("a", "c"),
                "c": ("b",),
            }
        },
    )

    episode = rollout(Trajectory(program, seed), 1)

    assert dict(episode.states[1]) == {
        (1, "a"): 0,
        (1, "b"): 1,
        (1, "c"): 0,
    }


def test_unavailable_historical_read_is_rejected() -> None:
    trajectory = _binary_line(
        (0, 1, 0),
        boundary=spaces.fixed(0),
        neighborhood=((-1, 0),),
        rule=_left_value,
    )

    try:
        step(trajectory, trajectory.seed.values)
    except ValueError as error:
        assert "source time" in str(error) and "unavailable" in str(error)
    else:
        raise AssertionError("unavailable historical read was accepted")


def test_rule_output_outside_alphabet_is_rejected() -> None:
    def invalid_rule(
        observed: tuple[object, ...],
        coordinate: tuple[object, ...],
    ) -> int:
        del observed, coordinate
        return 2

    trajectory = _binary_line(
        (0, 1, 0),
        boundary=spaces.fixed(0),
        rule=invalid_rule,
    )

    try:
        step(trajectory, trajectory.seed.values)
    except ValueError as error:
        assert "outside Alphabet" in str(error)
    else:
        raise AssertionError("Alphabet-invalid Rule output was accepted")


def test_zero_limit_returns_only_seed_state() -> None:
    trajectory = _binary_line(
        (1, 0, 1),
        boundary=spaces.fixed(0),
        rule=_any_observed,
    )

    episode = rollout(trajectory, 0)

    assert len(episode.states) == 1
    assert episode.states[0] == trajectory.seed.values
