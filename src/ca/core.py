"""Small immutable values for the coordinate-first ANKoS kernel."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from types import MappingProxyType


Coordinate = tuple[object, ...]
State = Mapping[Coordinate, object]

_MISSING = object()


def _freeze(value: object) -> object:
    """Detach ordinary mutable containers without inventing semantic nodes."""

    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, (tuple, list)):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, (set, frozenset)):
        return frozenset(_freeze(item) for item in value)
    return value


def freeze_state(values: Mapping[Coordinate, object]) -> State:
    """Return a detached immutable complete state with one explicit time."""

    copied: dict[Coordinate, object] = {}
    times: set[int] = set()
    for coordinate, value in values.items():
        if not isinstance(coordinate, tuple) or not coordinate:
            raise ValueError("state coordinates must be nonempty tuples")
        time = coordinate[0]
        if isinstance(time, bool) or not isinstance(time, int):
            raise ValueError("the first coordinate component must be an integer time")
        times.add(time)
        copied[coordinate] = _freeze(value)
    if not copied:
        raise ValueError("a state must contain at least one coordinate")
    if len(times) != 1:
        raise ValueError("one state must contain exactly one explicit time")
    return MappingProxyType(copied)


def state_time(state: State) -> int:
    """Return the single explicit time shared by every coordinate in a State."""

    times = {coordinate[0] for coordinate in state}
    if not state or len(times) != 1:
        raise ValueError("one state must contain exactly one explicit time")
    time = next(iter(times))
    if isinstance(time, bool) or not isinstance(time, int):
        raise ValueError("state time must be an integer")
    return time


def alphabet_accepts(alphabet: object, value: object) -> bool:
    """Use an ordinary membership container or predicate as an Alphabet."""

    if callable(alphabet):
        return bool(alphabet(value))
    try:
        return value in alphabet  # type: ignore[operator]
    except TypeError as error:
        raise TypeError("alphabet must be a membership container or callable") from error


def _fixed_boundary_value(boundary: object) -> object:
    if (
        isinstance(boundary, tuple)
        and len(boundary) == 2
        and boundary[0] == "fixed"
    ):
        return boundary[1]
    return _MISSING


@dataclass(frozen=True)
class Space:
    """One definite coordinate, extent, and boundary law."""

    axes: tuple[str, ...]
    extent: str
    boundary: object
    coordinates: Callable[[object], tuple[tuple[object, ...], ...]]
    normalize: Callable[[tuple[object, ...], object], tuple[object, ...]] | None = None

    def __post_init__(self) -> None:
        axes = tuple(self.axes)
        object.__setattr__(self, "axes", axes)
        if not axes or axes[0] != "t":
            raise ValueError("Space axes must begin with explicit time axis 't'")
        if len(set(axes)) != len(axes):
            raise ValueError("Space axes must be unique")
        if not isinstance(self.extent, str) or not self.extent:
            raise ValueError("Space extent law must be a nonempty string")
        if not callable(self.coordinates):
            raise TypeError("Space coordinates must be callable")
        if self.normalize is not None and not callable(self.normalize):
            raise TypeError("Space normalize must be callable when supplied")


@dataclass(frozen=True)
class SimpleProgram:
    """One definite reusable dynamics, independent of Seed."""

    space: Space
    alphabet: object
    neighborhood: object
    rule: Callable[[tuple[object, ...], Coordinate], object]

    def __post_init__(self) -> None:
        if not isinstance(self.space, Space):
            raise TypeError("SimpleProgram.space must be a Space")
        if not callable(self.neighborhood) and not isinstance(
            self.neighborhood, tuple
        ):
            raise TypeError("Neighborhood must be an offset tuple or callable")
        if isinstance(self.neighborhood, tuple) and any(
            not isinstance(offset, tuple) or len(offset) != len(self.space.axes)
            for offset in self.neighborhood
        ):
            raise ValueError("Neighborhood offsets must match Space coordinate rank")
        if not callable(self.rule):
            raise TypeError("Rule must be callable")
        boundary_value = _fixed_boundary_value(self.space.boundary)
        if boundary_value is not _MISSING and not alphabet_accepts(
            self.alphabet, boundary_value
        ):
            raise ValueError("fixed boundary value is not admitted by Alphabet")


@dataclass(frozen=True)
class Seed:
    """One complete initial State plus realized shape and relation data."""

    shape: object
    values: State
    relations: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "shape", _freeze(self.shape))
        object.__setattr__(self, "values", freeze_state(self.values))
        frozen_relations = _freeze(self.relations)
        if not isinstance(frozen_relations, Mapping):
            raise TypeError("Seed relations must be a mapping")
        object.__setattr__(self, "relations", frozen_relations)

    @property
    def time(self) -> int:
        return state_time(self.values)


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
        if any(not isinstance(item, tuple) or len(item) != spatial_rank for item in spatial):
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
            if not alphabet_accepts(self.program.alphabet, value)
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
            raise ValueError("Episode must contain at least its Seed state")
        times = tuple(state_time(state) for state in frozen_states)
        if any(later != earlier + 1 for earlier, later in zip(times, times[1:])):
            raise ValueError("Episode States must have consecutive explicit times")
        object.__setattr__(self, "states", frozen_states)


__all__ = [
    "Coordinate",
    "Episode",
    "Seed",
    "SimpleProgram",
    "Space",
    "State",
    "Trajectory",
    "alphabet_accepts",
    "freeze_state",
    "state_time",
]
