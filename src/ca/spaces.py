"""Plain coordinate enumeration and boundary resolution for Space values."""

from __future__ import annotations

from collections.abc import Mapping
from itertools import product

from .core import Coordinate, Seed, Space, State, state_time


def fixed(value: object) -> tuple[str, object]:
    """Return the ordinary value used for a fixed exterior boundary."""

    return ("fixed", value)


def box_coordinates(seed: object) -> tuple[tuple[int, ...], ...]:
    """Enumerate a finite zero-based Cartesian box supplied by Seed shape."""

    if not isinstance(seed, Seed) or not isinstance(seed.shape, tuple):
        raise ValueError("box Space requires Seed shape to be a tuple of sizes")
    shape = seed.shape
    if not shape or any(
        isinstance(size, bool) or not isinstance(size, int) or size <= 0
        for size in shape
    ):
        raise ValueError("box Seed shape must contain positive integer sizes")
    return tuple(product(*(range(size) for size in shape)))


def box_wrap(
    address: tuple[object, ...],
    seed: object,
) -> tuple[object, ...]:
    """Wrap one Cartesian spatial address through Seed dimensions."""

    if not isinstance(seed, Seed) or not isinstance(seed.shape, tuple):
        raise ValueError("periodic box resolution requires tuple Seed shape")
    if len(address) != len(seed.shape):
        raise ValueError("address rank does not match box Seed shape")
    if any(not isinstance(value, int) for value in address):
        raise TypeError("box addresses must contain integers")
    return tuple(value % size for value, size in zip(address, seed.shape))


def relation_coordinates(seed: object) -> tuple[tuple[object], ...]:
    """Enumerate stable addresses from an ordered Seed support."""

    if not isinstance(seed, Seed):
        raise TypeError("relational coordinates require a Seed")
    if isinstance(seed.shape, Mapping):
        support = tuple(seed.shape)
    elif isinstance(seed.shape, tuple):
        support = seed.shape
    else:
        raise ValueError("relational Seed shape must be a tuple or mapping")
    if not support or len(set(support)) != len(support):
        raise ValueError("relational Seed support must be nonempty and unique")
    return tuple((address,) for address in support)


def read(
    space: Space,
    state: State,
    coordinate: Coordinate,
    seed: Seed,
) -> object:
    """Read one address through a Space's exact boundary law."""

    if not isinstance(coordinate, tuple) or len(coordinate) != len(space.axes):
        raise ValueError("read coordinate does not match Space axes")
    current_time = state_time(state)
    if coordinate[0] != current_time:
        raise ValueError(
            f"source time {coordinate[0]!r} is unavailable in State at t={current_time}"
        )
    if coordinate in state:
        return state[coordinate]

    spatial = coordinate[1:]
    realized = set(space.coordinates(seed))
    if spatial in realized:
        raise ValueError("current State is incomplete at a realized coordinate")

    boundary = space.boundary
    if (
        isinstance(boundary, tuple)
        and len(boundary) == 2
        and boundary[0] == "fixed"
    ):
        return boundary[1]

    if boundary == "periodic":
        if space.normalize is None:
            raise ValueError(f"{boundary} Space requires a normalization function")
        normalized = space.normalize(spatial, seed)
        target = (coordinate[0], *normalized)
        if target not in state:
            raise ValueError("Space normalization did not resolve to realized support")
        return state[target]

    if boundary is None:
        raise KeyError(f"coordinate {coordinate!r} is outside realized support")
    raise ValueError(f"unknown Space boundary law {boundary!r}")


__all__ = [
    "box_coordinates",
    "box_wrap",
    "fixed",
    "read",
    "relation_coordinates",
]
