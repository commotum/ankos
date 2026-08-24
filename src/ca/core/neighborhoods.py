"""Ordinary values and functions for resolving Neighborhood addresses."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from itertools import product
from math import ceil

from ..utils import selector
from .seeds import Coordinate, Seed


def current(source: Coordinate, seed: Seed) -> tuple[Coordinate, ...]:
    """Return the spatial source as a one-address Neighborhood."""

    del seed
    return (source,)


def relation(
    name: str,
) -> Callable[[Coordinate, Seed], tuple[Coordinate, ...]]:
    """Return a Neighborhood that follows one ordered Seed relation."""

    if not isinstance(name, str) or not name:
        raise ValueError("relation name must be a nonempty string")

    def resolve_relation(source: Coordinate, seed: Seed) -> tuple[Coordinate, ...]:
        if len(source) != 1:
            raise ValueError(
                "relation Neighborhoods require spatial coordinates shaped as (address,)"
            )
        relation_data = seed.relations.get(name)
        if not isinstance(relation_data, Mapping):
            raise ValueError(f"Seed does not supply relation {name!r}")

        vertices = {
            coordinate[1] for coordinate in seed.values if len(coordinate) == 2
        }
        if set(relation_data) != vertices:
            raise ValueError(
                f"relation {name!r} must define every realized address exactly once"
            )

        selected = selector.follow_relation(source, relation_data)
        missing = tuple(
            coordinate[0]
            for coordinate in selected
            if coordinate[0] not in vertices
        )
        if missing:
            raise ValueError(
                f"relation {name!r} targets {len(missing)} address(es) outside Seed support"
            )
        return selected

    resolve_relation.__name__ = f"select_{name}"
    return resolve_relation


adjacent = relation("adjacent")


def ball(
    spatial_rank: int,
    radius: float,
    *,
    metric: Callable[[tuple[float, ...]], float] = selector.taxicab,
) -> tuple[Coordinate, ...]:
    """Return a lattice ball of spatial offsets."""

    if spatial_rank < 0:
        raise ValueError("spatial rank must be nonnegative")
    bound = ceil(radius)
    candidates = product(range(-bound, bound + 1), repeat=spatial_rank)
    selected = selector.select(
        candidates,
        selector.within_radius(radius, metric=metric),
    )
    return tuple(selected)


def shell(
    spatial_rank: int,
    radius: float,
    *,
    metric: Callable[[tuple[float, ...]], float] = selector.taxicab,
) -> tuple[Coordinate, ...]:
    """Return a lattice shell of spatial offsets."""

    if spatial_rank < 0:
        raise ValueError("spatial rank must be nonnegative")
    bound = ceil(radius)
    candidates = product(range(-bound, bound + 1), repeat=spatial_rank)
    selected = selector.select(
        candidates,
        selector.on_shell(radius, metric=metric),
    )
    return tuple(selected)


def resolve(
    neighborhood: object,
    source: Coordinate,
    seed: Seed,
) -> tuple[Coordinate, ...]:
    """Resolve one definite Neighborhood into ordered read addresses."""

    spatial_source = source[1:]
    if callable(neighborhood):
        spatial = tuple(neighborhood(spatial_source, seed))
    elif isinstance(neighborhood, tuple):
        spatial = selector.translate(spatial_source, neighborhood)
    else:
        raise TypeError("Neighborhood must be an offset tuple or callable")

    if any(
        not isinstance(address, tuple) or len(address) != len(spatial_source)
        for address in spatial
    ):
        raise ValueError("Neighborhood returned a spatial address with the wrong rank")
    return tuple((source[0], *address) for address in spatial)


__all__ = ["adjacent", "ball", "current", "relation", "resolve", "shell"]
