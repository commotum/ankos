"""Behavioral checks for definite Neighborhood address resolution."""

from __future__ import annotations

from ca import Seed, neighborhoods, selector


def _relational_seed(adjacency: dict[str, list[str]]) -> Seed:
    return Seed(
        shape=("a", "b", "c"),
        values={(0, "a"): 0, (0, "b"): 1, (0, "c"): 0},
        relations={"edge": adjacency},
    )


def test_resolve_accepts_offsets_and_address_functions() -> None:
    seed = _relational_seed({"a": ["b"], "b": ["a", "c"], "c": ["b"]})

    assert neighborhoods.resolve(((0, -1), (0, 0), (0, 1)), (4, 10), seed) == (
        (4, 9),
        (4, 10),
        (4, 11),
    )
    assert neighborhoods.resolve(neighborhoods.current, (4, 10), seed) == ((4, 10),)


def test_ball_is_a_definite_ordered_neighborhood_with_explicit_time() -> None:
    assert neighborhoods.ball(
        spatial_rank=2,
        radius=1,
        metric=selector.taxicab,
    ) == (
        (0, -1, 0),
        (0, 0, -1),
        (0, 0, 0),
        (0, 0, 1),
        (0, 1, 0),
    )


def test_relation_neighborhood_uses_seed_data_and_preserves_order() -> None:
    seed = _relational_seed({"a": ["b"], "b": ["c", "a"], "c": ["b"]})
    edge = neighborhoods.relation("edge")

    assert neighborhoods.resolve(edge, (7, "b"), seed) == (
        (7, "c"),
        (7, "a"),
    )


def test_relation_neighborhood_rejects_targets_outside_realized_support() -> None:
    seed = _relational_seed(
        {"a": ["b"], "b": ["c", "missing"], "c": ["b"]}
    )
    edge = neighborhoods.relation("edge")

    try:
        neighborhoods.resolve(edge, (0, "b"), seed)
    except ValueError as error:
        assert "outside Seed support" in str(error)
    else:
        raise AssertionError("relation target outside support was accepted")
