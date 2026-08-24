"""Ordinary values and functions for resolving Neighborhood addresses."""

from __future__ import annotations

from collections.abc import Callable, Mapping

from . import selector
from .core import Coordinate, Seed


def current(source: Coordinate, seed: Seed) -> tuple[Coordinate, ...]:
    """Return the source coordinate as a one-address Neighborhood."""

    del seed
    return (source,)


def relation(
    name: str,
) -> Callable[[Coordinate, Seed], tuple[Coordinate, ...]]:
    """Return a Neighborhood that follows one ordered Seed relation."""

    if not isinstance(name, str) or not name:
        raise ValueError("relation name must be a nonempty string")

    def resolve_relation(source: Coordinate, seed: Seed) -> tuple[Coordinate, ...]:
        if len(source) != 2:
            raise ValueError("relation Neighborhoods require coordinates shaped as (t, address)")
        relation_data = seed.relations.get(name)
        if not isinstance(relation_data, Mapping):
            raise ValueError(f"Seed does not supply relation {name!r}")

        vertices = {coordinate[1] for coordinate in seed.values if len(coordinate) == 2}
        if set(relation_data) != vertices:
            raise ValueError(f"relation {name!r} must define every realized address exactly once")

        selected = selector.follow_relation(source, relation_data)
        missing = tuple(coordinate[1] for coordinate in selected if coordinate[1] not in vertices)
        if missing:
            raise ValueError(
                f"relation {name!r} targets {len(missing)} address(es) outside Seed support"
            )
        return selected

    resolve_relation.__name__ = f"select_{name}"
    return resolve_relation


adjacent = relation("adjacent")


def resolve(
    neighborhood: object,
    source: Coordinate,
    seed: Seed,
) -> tuple[Coordinate, ...]:
    """Resolve one definite Neighborhood into ordered read addresses."""

    if callable(neighborhood):
        addresses = tuple(neighborhood(source, seed))
    elif isinstance(neighborhood, tuple):
        addresses = selector.translate(source, neighborhood)
    else:
        raise TypeError("Neighborhood must be an offset tuple or callable")

    if any(
        not isinstance(address, tuple) or len(address) != len(source)
        for address in addresses
    ):
        raise ValueError("Neighborhood returned an address with the wrong rank")
    return addresses


__all__ = ["adjacent", "current", "relation", "resolve"]
