"""Small, dependency-free helpers for selecting ordinary coordinates."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from math import isclose, sqrt


Coordinate = tuple[object, ...]
Predicate = Callable[[Coordinate], bool]
Metric = Callable[[tuple[float, ...]], float]


def select(
    candidates: Iterable[Coordinate],
    predicate: Predicate,
) -> tuple[Coordinate, ...]:
    """Return matching candidates in their original order."""

    return tuple(candidate for candidate in candidates if predicate(candidate))


def translate(
    source: Coordinate,
    offsets: Iterable[Coordinate],
) -> tuple[Coordinate, ...]:
    """Translate ordered numeric offsets relative to one coordinate."""

    selected: list[Coordinate] = []
    for offset in offsets:
        if not isinstance(offset, tuple) or len(offset) != len(source):
            raise ValueError("each offset must match the source coordinate rank")
        try:
            selected.append(tuple(value + delta for value, delta in zip(source, offset)))
        except TypeError as error:
            raise TypeError("translation requires additive coordinate components") from error
    return tuple(selected)


def follow_relation(
    source: Coordinate,
    relation: Mapping[object, Sequence[object]],
    axis: int = -1,
) -> tuple[Coordinate, ...]:
    """Replace one source component with each ordered target in a relation."""

    if not source:
        raise ValueError("a relation source cannot be empty")
    try:
        origin = source[axis]
    except IndexError as error:
        raise ValueError("relation axis is outside the source coordinate") from error
    if origin not in relation:
        raise ValueError("relation does not define the source address")
    targets = tuple(relation[origin])

    resolved: list[Coordinate] = []
    for target in targets:
        coordinate = list(source)
        coordinate[axis] = target
        resolved.append(tuple(coordinate))
    return tuple(resolved)


def all_of(*predicates: Predicate) -> Predicate:
    """Require every predicate; an empty conjunction accepts everything."""

    return lambda coordinate: all(predicate(coordinate) for predicate in predicates)


def any_of(*predicates: Predicate) -> Predicate:
    """Require any predicate; an empty disjunction accepts nothing."""

    return lambda coordinate: any(predicate(coordinate) for predicate in predicates)


def negate(predicate: Predicate) -> Predicate:
    """Return the Boolean complement of a predicate."""

    return lambda coordinate: not predicate(coordinate)


def _axis_index(axis: int | str, axes: Sequence[str] | None) -> int:
    if isinstance(axis, int):
        return axis
    if axes is None:
        raise ValueError("named-axis predicates require an axes sequence")
    try:
        return tuple(axes).index(axis)
    except ValueError as error:
        raise ValueError(f"unknown axis {axis!r}") from error


def axis_equal(
    axis: int | str,
    value: object,
    *,
    axes: Sequence[str] | None = None,
) -> Predicate:
    """Select coordinates whose named or indexed component equals a value."""

    index = _axis_index(axis, axes)
    return lambda coordinate: coordinate[index] == value


def axis_between(
    axis: int | str,
    low: object,
    high: object,
    *,
    axes: Sequence[str] | None = None,
) -> Predicate:
    """Select coordinates whose component lies in one inclusive interval."""

    index = _axis_index(axis, axes)
    return lambda coordinate: low <= coordinate[index] <= high  # type: ignore[operator]


def mod_equal(
    axis: int | str,
    modulus: int,
    phase: int = 0,
    *,
    axes: Sequence[str] | None = None,
) -> Predicate:
    """Select integer coordinate components with one modular phase."""

    if modulus <= 0:
        raise ValueError("modulus must be positive")
    index = _axis_index(axis, axes)

    def matches_phase(coordinate: Coordinate) -> bool:
        return coordinate[index] % modulus == phase % modulus  # type: ignore[operator]

    return matches_phase


def taxicab(delta: tuple[float, ...]) -> float:
    """Return the L1 norm of a coordinate displacement."""

    return sum(abs(value) for value in delta)


def euclidean(delta: tuple[float, ...]) -> float:
    """Return the L2 norm of a coordinate displacement."""

    return sqrt(sum(value * value for value in delta))


def chebyshev(delta: tuple[float, ...]) -> float:
    """Return the L-infinity norm of a coordinate displacement."""

    return max((abs(value) for value in delta), default=0.0)


def _displacement(
    coordinate: Coordinate,
    center: Coordinate | None,
) -> tuple[float, ...]:
    if center is None:
        return coordinate  # type: ignore[return-value]
    if len(coordinate) != len(center):
        raise ValueError("coordinate and center must have the same rank")
    try:
        return tuple(  # type: ignore[return-value]
            value - origin  # type: ignore[operator]
            for value, origin in zip(coordinate, center)
        )
    except TypeError as error:
        raise TypeError("metric predicates require subtractable coordinates") from error


def within_radius(
    radius: float,
    *,
    metric: Metric = taxicab,
    center: Coordinate | None = None,
) -> Predicate:
    """Select coordinates at most ``radius`` from an optional center."""

    if radius < 0:
        raise ValueError("radius must be nonnegative")
    return lambda coordinate: metric(_displacement(coordinate, center)) <= radius


def on_shell(
    radius: float,
    *,
    metric: Metric = taxicab,
    center: Coordinate | None = None,
) -> Predicate:
    """Select coordinates exactly one metric radius from an optional center."""

    if radius < 0:
        raise ValueError("radius must be nonnegative")
    return lambda coordinate: isclose(
        metric(_displacement(coordinate, center)),
        radius,
    )


def lexicographic_order(
    coordinates: Iterable[Coordinate],
    components: Sequence[int] | None = None,
) -> tuple[Coordinate, ...]:
    """Return coordinates in deterministic lexicographic order."""

    realized = tuple(coordinates)
    if components is None:
        return tuple(sorted(realized))
    indices = tuple(components)
    return tuple(
        sorted(
            realized,
            key=lambda coordinate: tuple(coordinate[index] for index in indices),
        )
    )


__all__ = [
    "all_of",
    "any_of",
    "axis_between",
    "axis_equal",
    "chebyshev",
    "euclidean",
    "follow_relation",
    "lexicographic_order",
    "mod_equal",
    "negate",
    "on_shell",
    "select",
    "taxicab",
    "translate",
    "within_radius",
]
