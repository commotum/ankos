"""Behavioral checks for the minimal composition values."""

from __future__ import annotations

from ca import Seed, SimpleProgram, Space, Trajectory, rollout


def _line_coordinates(seed: object) -> tuple[tuple[int], ...]:
    size = seed.shape[0]
    return tuple((x,) for x in range(size))


def _identity_rule(observed: tuple[object, ...], coordinate: tuple[object, ...]) -> object:
    del coordinate
    return observed[0]


def _program() -> SimpleProgram:
    return SimpleProgram(
        space=Space(
            axes=("t", "x"),
            extent="finite-from-seed",
            boundary=("fixed", 0),
            coordinates=_line_coordinates,
        ),
        alphabet=frozenset({0, 1}),
        neighborhood=((0, 0),),
        rule=_identity_rule,
    )


def _seed(values: list[int]) -> Seed:
    return Seed(
        shape=(len(values),),
        values={(0, x): value for x, value in enumerate(values)},
    )


def test_one_program_accepts_two_realized_seed_shapes() -> None:
    program = _program()

    short = Trajectory(program, _seed([0, 1, 0]))
    long = Trajectory(program, _seed([0, 0, 1, 0, 0]))

    assert short.program is program
    assert long.program is program
    assert short.seed.shape == (3,)
    assert long.seed.shape == (5,)
    assert dict(rollout(short, 1).states[1]) == {
        (1, 0): 0,
        (1, 1): 1,
        (1, 2): 0,
    }
    assert dict(rollout(long, 1).states[1]) == {
        (1, 0): 0,
        (1, 1): 0,
        (1, 2): 1,
        (1, 3): 0,
        (1, 4): 0,
    }


def test_seed_detaches_mutable_input_state_and_relations() -> None:
    values = {(0, "a"): [1, 0], (0, "b"): [0, 1]}
    adjacency = {"a": ["b"], "b": ["a"]}
    seed = Seed(
        shape=("a", "b"),
        values=values,
        relations={"adjacent": adjacency},
    )

    values[(0, "a")][0] = 9
    adjacency["a"].append("a")

    assert seed.values[(0, "a")] == (1, 0)
    assert seed.relations["adjacent"]["a"] == ("b",)


def test_trajectory_rejects_incomplete_support() -> None:
    program = _program()
    incomplete = Seed(shape=(3,), values={(0, 0): 0, (0, 1): 1})

    try:
        Trajectory(program, incomplete)
    except ValueError as error:
        assert "complete realized Space support" in str(error)
    else:
        raise AssertionError("incomplete Seed support was accepted")


def test_trajectory_rejects_values_outside_alphabet() -> None:
    program = _program()
    invalid = Seed(
        shape=(3,),
        values={(0, 0): 0, (0, 1): 2, (0, 2): 0},
    )

    try:
        Trajectory(program, invalid)
    except ValueError as error:
        assert "outside Alphabet" in str(error)
    else:
        raise AssertionError("Alphabet-invalid Seed was accepted")


def test_program_rejects_neighborhood_offsets_with_wrong_rank() -> None:
    try:
        SimpleProgram(
            space=Space(
                axes=("t", "x"),
                extent="finite-from-seed",
                boundary=("fixed", 0),
                coordinates=_line_coordinates,
            ),
            alphabet=frozenset({0, 1}),
            neighborhood=((0, 0, 1),),
            rule=_identity_rule,
        )
    except ValueError as error:
        assert "match Space coordinate rank" in str(error)
    else:
        raise AssertionError("a wrong-rank Neighborhood was accepted")
