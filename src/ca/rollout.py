"""Pair mechanics with a Seed and produce immutable Episode data."""

from __future__ import annotations

from dataclasses import dataclass

from .core import alphabets, neighborhoods, spaces
from .core.seeds import Seed, State, freeze_state, state_time
from .simpleprograms import SimpleProgram


@dataclass(frozen=True)
class Trajectory:
    """One SimpleProgram paired with one compatible Seed realization."""

    program: SimpleProgram
    seed: Seed

    def __post_init__(self) -> None:
        if not isinstance(self.program, SimpleProgram):
            raise TypeError("Trajectory.program must be a SimpleProgram")
        if not isinstance(self.seed, Seed):
            raise TypeError("Trajectory.seed must be a Seed")

        spatial = tuple(self.program.space.coordinates(self.seed))
        if len(set(spatial)) != len(spatial):
            raise ValueError("Space produced duplicate realized coordinates")
        spatial_rank = len(self.program.space.axes) - 1
        if any(
            not isinstance(item, tuple) or len(item) != spatial_rank
            for item in spatial
        ):
            raise ValueError("realized coordinates do not match Space axes")

        expected = {(self.seed.time, *item) for item in spatial}
        actual = set(self.seed.values)
        if actual != expected:
            missing = len(expected - actual)
            extra = len(actual - expected)
            raise ValueError(
                "Seed must assign the complete realized Space support "
                f"(missing={missing}, extra={extra})"
            )
        invalid = [
            coordinate
            for coordinate, value in self.seed.values.items()
            if not alphabets.accepts(self.program.alphabet, value)
        ]
        if invalid:
            raise ValueError(
                f"Seed values outside Alphabet at {len(invalid)} coordinate(s)"
            )


@dataclass(frozen=True)
class Episode:
    """The complete immutable States produced by one rollout."""

    states: tuple[State, ...]

    def __post_init__(self) -> None:
        frozen_states = tuple(freeze_state(state) for state in self.states)
        if not frozen_states:
            raise ValueError("Episode must contain at least its Seed State")
        times = tuple(state_time(state) for state in frozen_states)
        if any(later != earlier + 1 for earlier, later in zip(times, times[1:])):
            raise ValueError("Episode States must have consecutive explicit times")
        object.__setattr__(self, "states", frozen_states)


def _require_complete_state(trajectory: Trajectory, state: State) -> int:
    time = state_time(state)
    spatial = tuple(trajectory.program.space.coordinates(trajectory.seed))
    expected = {(time, *address) for address in spatial}
    actual = set(state)
    if actual != expected:
        missing = len(expected - actual)
        extra = len(actual - expected)
        raise ValueError(
            "State must cover the complete realized Space support "
            f"(missing={missing}, extra={extra})"
        )
    return time


def step(trajectory: Trajectory, state: State) -> State:
    """Construct one complete new State without altering the source State."""

    if not isinstance(trajectory, Trajectory):
        raise TypeError("step requires a Trajectory")
    current = freeze_state(state)
    time = _require_complete_state(trajectory, current)
    program = trajectory.program
    seed = trajectory.seed
    successor: dict[tuple[object, ...], object] = {}

    for spatial in program.space.coordinates(seed):
        source = (time, *spatial)
        addresses = neighborhoods.resolve(program.neighborhood, source, seed)
        observed = tuple(
            spaces.read(program.space, current, address, seed)
            for address in addresses
        )
        value = program.rule(observed, source)
        if not alphabets.accepts(program.alphabet, value):
            raise ValueError(f"Rule output at {source!r} is outside Alphabet")
        successor[(time + 1, *spatial)] = value

    return freeze_state(successor)


def rollout(trajectory: Trajectory, limit: int) -> Episode:
    """Return the Seed State followed by exactly ``limit`` complete successors."""

    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ValueError("rollout limit must be a nonnegative integer")
    if not isinstance(trajectory, Trajectory):
        raise TypeError("rollout requires a Trajectory")

    states: list[State] = [trajectory.seed.values]
    for _ in range(limit):
        states.append(step(trajectory, states[-1]))
    return Episode(tuple(states))


__all__ = ["Episode", "Trajectory", "rollout", "step"]
