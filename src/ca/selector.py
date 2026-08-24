"""Coordinate selection with ordinary tuples and plain relation mappings."""

from __future__ import annotations

from collections.abc import Callable, Mapping

from .core import Coordinate, Seed


def relative(
    source: Coordinate,
    offsets: tuple[Coordinate, ...],
) -> tuple[Coordinate, ...]:
    """Translate ordered numeric offsets relative to one full source address."""

    selected: list[Coordinate] = []
    for offset in offsets:
        if not isinstance(offset, tuple) or len(offset) != len(source):
            raise ValueError("each offset must match the source coordinate rank")
        try:
            selected.append(tuple(value + delta for value, delta in zip(source, offset)))
        except TypeError as error:
            raise TypeError("relative offsets require additive coordinate components") from error
    return tuple(selected)


def current(source: Coordinate, seed: Seed) -> tuple[Coordinate, ...]:
    """Select only the current source address."""

    del seed
    return (source,)


def relation(
    name: str,
) -> Callable[[Coordinate, Seed], tuple[Coordinate, ...]]:
    """Return a selector that follows one ordered Seed relation."""

    if not isinstance(name, str) or not name:
        raise ValueError("relation name must be a nonempty string")

    def select_relation(source: Coordinate, seed: Seed) -> tuple[Coordinate, ...]:
        if len(source) != 2:
            raise ValueError("relation selectors require coordinates shaped as (t, address)")
        relation_data = seed.relations.get(name)
        if not isinstance(relation_data, Mapping):
            raise ValueError(f"Seed does not supply relation {name!r}")

        vertices = {
            coordinate[1]
            for coordinate in seed.values
            if len(coordinate) == 2
        }
        if set(relation_data) != vertices:
            raise ValueError(
                f"relation {name!r} must define every realized address exactly once"
            )

        vertex = source[1]
        if vertex not in vertices:
            raise ValueError("relation source is outside Seed support")
        neighbors = relation_data[vertex]
        if not isinstance(neighbors, tuple):
            raise TypeError("ordered relation targets must be a tuple")
        missing = tuple(neighbor for neighbor in neighbors if neighbor not in vertices)
        if missing:
            raise ValueError(
                f"relation {name!r} targets {len(missing)} address(es) outside Seed support"
            )
        return tuple((source[0], neighbor) for neighbor in neighbors)

    select_relation.__name__ = f"select_{name}"
    return select_relation


adjacent = relation("adjacent")


def select(
    neighborhood: object,
    source: Coordinate,
    seed: Seed,
) -> tuple[Coordinate, ...]:
    """Resolve an offset tuple or address function into ordered addresses."""

    if callable(neighborhood):
        addresses = tuple(neighborhood(source, seed))
    elif isinstance(neighborhood, tuple):
        addresses = relative(source, neighborhood)
    else:
        raise TypeError("Neighborhood must be an offset tuple or callable")

    if any(
        not isinstance(address, tuple) or len(address) != len(source)
        for address in addresses
    ):
        raise ValueError("Neighborhood returned an address with the wrong rank")
    return addresses


__all__ = ["adjacent", "current", "relation", "relative", "select"]
