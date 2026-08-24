"""Behavioral checks for the shared coordinate-selection helpers."""

from __future__ import annotations

from ca import selector


def test_selection_composes_named_axis_predicates_without_reordering() -> None:
    coordinates = (
        (0, -2),
        (0, -1),
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 1),
    )
    axes = ("t", "x")
    interior_odd_at_t0 = selector.all_of(
        selector.axis_equal("t", 0, axes=axes),
        selector.axis_between("x", -1, 1, axes=axes),
        selector.negate(selector.mod_equal("x", 2, axes=axes)),
    )

    assert selector.select(coordinates, interior_odd_at_t0) == (
        (0, -1),
        (0, 1),
    )


def test_translation_and_relation_following_preserve_declared_order() -> None:
    assert selector.translate(
        (5, 10, 20),
        ((0, -1, 0), (0, 0, 0), (-1, 0, 2)),
    ) == (
        (5, 9, 20),
        (5, 10, 20),
        (4, 10, 22),
    )
    assert selector.follow_relation(
        (5, "b"),
        {"a": ("b",), "b": ("c", "a"), "c": ("b",)},
    ) == ((5, "c"), (5, "a"))


def test_metrics_construct_reusable_ball_and_shell_predicates() -> None:
    candidates = ((-1, -1), (-1, 0), (0, 0), (0, 1), (1, 0), (1, 1))

    assert selector.taxicab((3, -4)) == 7
    assert selector.euclidean((3, -4)) == 5
    assert selector.chebyshev((3, -4)) == 4
    assert selector.select(
        candidates,
        selector.within_radius(1, metric=selector.taxicab),
    ) == ((-1, 0), (0, 0), (0, 1), (1, 0))
    assert selector.select(
        candidates,
        selector.on_shell(1, metric=selector.chebyshev),
    ) == ((-1, -1), (-1, 0), (0, 1), (1, 0), (1, 1))


def test_predicate_alternatives_and_lexicographic_order_are_plain_functions() -> None:
    endpoint = selector.any_of(
        selector.axis_equal(1, -1),
        selector.axis_equal(1, 1),
    )

    assert selector.select(((0, 0), (0, 1), (0, -1)), endpoint) == (
        (0, 1),
        (0, -1),
    )
    assert selector.lexicographic_order(((0, 1), (0, -1), (0, 0))) == (
        (0, -1),
        (0, 0),
        (0, 1),
    )
