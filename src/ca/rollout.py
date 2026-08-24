"""Reference immutable execution for one resolved Trajectory."""

from __future__ import annotations

from . import selector, spaces
from .core import (
    Episode,
    State,
    Trajectory,
    alphabet_accepts,
    freeze_state,
    state_time,
)


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
        addresses = selector.select(program.neighborhood, source, seed)
        observed = tuple(
            spaces.read(program.space, current, address, seed)
            for address in addresses
        )
        value = program.rule(observed, source)
        if not alphabet_accepts(program.alphabet, value):
            raise ValueError(f"Rule output at {source!r} is outside Alphabet")
        successor[(time + 1, *spatial)] = value

    return freeze_state(successor)


def rollout(trajectory: Trajectory, limit: int) -> Episode:
    """Return the Seed State followed by exactly `limit` complete successors."""

    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ValueError("rollout limit must be a nonnegative integer")
    if not isinstance(trajectory, Trajectory):
        raise TypeError("rollout requires a Trajectory")

    states: list[State] = [trajectory.seed.values]
    for _ in range(limit):
        states.append(step(trajectory, states[-1]))
    return Episode(tuple(states))


__all__ = ["rollout", "step"]
