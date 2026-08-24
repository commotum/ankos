"""Coordinate and relation selection without semantic locus classes."""

from __future__ import annotations

from ca import Seed, selector


def test_relative_offsets_preserve_order_and_explicit_time() -> None:
    assert selector.relative(
        (5, 10, 20),
        ((0, -1, 0), (0, 0, 0), (-1, 0, 2)),
    ) == (
        (5, 9, 20),
        (5, 10, 20),
        (4, 10, 22),
    )


def _relational_seed(adjacency: dict[str, list[str]]) -> Seed:
    return Seed(
        shape=("a", "b", "c"),
        values={(0, "a"): 0, (0, "b"): 1, (0, "c"): 0},
        relations={"edge": adjacency},
    )


def test_relation_selector_preserves_seed_order() -> None:
    seed = _relational_seed(
        {"a": ["b"], "b": ["c", "a"], "c": ["b"]}
    )
    edge_neighbors = selector.relation("edge")

    assert edge_neighbors((0, "b"), seed) == ((0, "c"), (0, "a"))
    assert selector.select(edge_neighbors, (0, "b"), seed) == (
        (0, "c"),
        (0, "a"),
    )


def test_relation_selector_rejects_targets_outside_support() -> None:
    seed = _relational_seed(
        {"a": ["b"], "b": ["c", "missing"], "c": ["b"]}
    )
    edge_neighbors = selector.relation("edge")

    try:
        edge_neighbors((0, "b"), seed)
    except ValueError as error:
        assert "outside Seed support" in str(error)
    else:
        raise AssertionError("relation target outside support was accepted")


def test_current_selects_the_plain_source_coordinate() -> None:
    seed = _relational_seed(
        {"a": ["b"], "b": ["a", "c"], "c": ["b"]}
    )

    assert selector.current((0, "a"), seed) == ((0, "a"),)
