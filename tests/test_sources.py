"""Plural ordinary sources compose definite values without a Preset class."""

from __future__ import annotations

from collections.abc import Iterator

from ca import Seed, SimpleProgram, Space, Trajectory, rollout, seeds, spaces


def spaces_source() -> Iterator[Space]:
    yield spaces.cartesian(
        axes=("t", "x"),
        boundary=spaces.fixed(0),
    )
    yield spaces.cartesian(
        axes=("t", "x"),
        boundary=spaces.periodic(),
    )


def alphabets_source() -> Iterator[tuple[int, ...]]:
    yield (0, 1)
    yield (0, 1, 2)


def neighborhoods_source(space: Space) -> Iterator[tuple[tuple[int, ...], ...]]:
    if space.axes != ("t", "x"):
        return
    yield ((0,),)
    yield ((-1,), (0,))


def rules_source(
    alphabet: tuple[int, ...],
    neighborhood: tuple[tuple[int, ...], ...],
) -> Iterator[object]:
    del alphabet, neighborhood

    def first(observed: tuple[object, ...]) -> object:
        return observed[0]

    def largest(observed: tuple[object, ...]) -> object:
        return max(observed)

    yield first
    yield largest


def programs_source() -> Iterator[SimpleProgram]:
    for space in spaces_source():
        for alphabet in alphabets_source():
            for neighborhood in neighborhoods_source(space):
                for rule in rules_source(alphabet, neighborhood):
                    yield SimpleProgram(space, alphabet, neighborhood, rule)


def seeds_source() -> Iterator[Seed]:
    yield seeds.dense((0, 1, 0))
    yield seeds.dense((0, 0, 1, 0, 0))
    yield seeds.dense((0, 2, 0))


def test_plain_sources_yield_fully_selected_values() -> None:
    programs = tuple(programs_source())
    seeds = tuple(seeds_source())

    assert len({program.space.boundary for program in programs}) == 2
    assert len({program.rule.__name__ for program in programs}) == 2
    assert {seed.shape for seed in seeds} == {(3,), (5,)}
    assert all(callable(program.rule) for program in programs)
    assert all(program.neighborhood for program in programs)


def test_seed_compatibility_is_decided_when_trajectory_is_formed() -> None:
    programs = tuple(programs_source())
    seeds = tuple(seeds_source())
    binary_program = next(
        program for program in programs if program.alphabet == (0, 1)
    )

    compatible = Trajectory(binary_program, seeds[0])
    assert len(rollout(compatible, 1).states) == 2

    try:
        Trajectory(binary_program, seeds[2])
    except ValueError as error:
        assert "outside Alphabet" in str(error)
    else:
        raise AssertionError("an incompatible independently generated Seed was accepted")

    ternary_program = next(
        program for program in programs if program.alphabet == (0, 1, 2)
    )
    assert Trajectory(ternary_program, seeds[2]).seed is seeds[2]


def test_explicit_loops_are_enough_to_form_compatible_trajectories() -> None:
    trajectories: list[Trajectory] = []
    rejected = 0
    for program in programs_source():
        for seed in seeds_source():
            try:
                trajectories.append(Trajectory(program, seed))
            except ValueError:
                rejected += 1

    assert trajectories
    assert rejected
    assert {trajectory.seed.shape for trajectory in trajectories} == {(3,), (5,)}
