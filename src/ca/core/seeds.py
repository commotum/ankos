"""Concrete Seed realizations and immutable State helpers."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType


Coordinate = tuple[object, ...]
State = Mapping[Coordinate, object]


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
    """Return a detached immutable complete State with one explicit time."""

    copied: dict[Coordinate, object] = {}
    times: set[int] = set()
    for coordinate, value in values.items():
        if not isinstance(coordinate, tuple) or not coordinate:
            raise ValueError("State coordinates must be nonempty tuples")
        time = coordinate[0]
        if isinstance(time, bool) or not isinstance(time, int):
            raise ValueError("the first coordinate component must be an integer time")
        times.add(time)
        copied[coordinate] = _freeze(value)
    if not copied:
        raise ValueError("a State must contain at least one coordinate")
    if len(times) != 1:
        raise ValueError("one State must contain exactly one explicit time")
    return MappingProxyType(copied)


def state_time(state: State) -> int:
    """Return the single explicit time shared by every coordinate in a State."""

    times = {coordinate[0] for coordinate in state}
    if not state or len(times) != 1:
        raise ValueError("one State must contain exactly one explicit time")
    time = next(iter(times))
    if isinstance(time, bool) or not isinstance(time, int):
        raise ValueError("State time must be an integer")
    return time


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


def dense(values: object, *, time: int = 0) -> Seed:
    """Build a rectangular Seed from ordinary nested lists or tuples."""

    realized: dict[tuple[int, ...], object] = {}

    def visit(value: object, address: tuple[int, ...]) -> tuple[int, ...]:
        if isinstance(value, (list, tuple)):
            if not value:
                raise ValueError("dense Seed axes must be nonempty")
            child_shapes = tuple(
                visit(child, (*address, index))
                for index, child in enumerate(value)
            )
            if len(set(child_shapes)) != 1:
                raise ValueError("dense Seed values must form a rectangular shape")
            return (len(value), *child_shapes[0])
        realized[address] = value
        return ()

    shape = visit(values, ())
    state = {(time, *address): value for address, value in realized.items()}
    return Seed(shape=shape, values=state)


__all__ = ["Coordinate", "Seed", "State", "dense", "freeze_state", "state_time"]
