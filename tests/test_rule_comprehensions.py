"""Focused tests for closed Rule sequence bindings and finite windows."""

from __future__ import annotations

import pytest

from ca import alphabets, loci, neighborhoods, rules


def _readable_view():
    source = loci.record_configuration((("fixture", 0),))
    return neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.INTEGER,
    ).resolve(source)


def _evaluate(expression: rules.RuleExpr):
    result, proof = rules._evaluate_proven(  # noqa: SLF001 - interpreter test
        expression,
        _readable_view(),
        anchor=None,
    )
    assert proof.steps[-1].expression == expression
    assert proof.steps[-1].result == result
    return result, proof


def _word(
    tag: str,
    *items: alphabets.SemanticValue,
) -> alphabets.ValueNode:
    return alphabets.word_value(items, tag=tag)


def _map(
    *entries: tuple[alphabets.SemanticValue, alphabets.SemanticValue],
) -> alphabets.ValueNode:
    return alphabets.map_value(
        tuple(
            alphabets.map_entry_value(key, value)
            for key, value in entries
        )
    )


def test_flat_map_items_performs_independent_substitution_with_exact_binding_proof() -> None:
    source = _word("symbols", "A", "B", "A")
    substitutions = _map(
        ("A", _word("symbols", "A", "B")),
        ("B", _word("symbols", "A")),
    )
    expression = rules.flat_map_items(
        rules.literal_expr(source),
        rules.map_lookup(
            rules.literal_expr(substitutions),
            rules.bound_value(),
            rules.literal_expr(_word("symbols")),
        ),
        "symbols",
    )

    result, proof = _evaluate(expression)

    assert result == _word("symbols", "A", "B", "A", "A", "B")
    binding_steps = tuple(
        step
        for step in proof.steps
        if step.expression.primitive is rules.ExpressionPrimitive.BOUND_VALUE
    )
    assert tuple(step.result for step in binding_steps) == ("A", "B", "A")
    assert all(len(step.read_evidence) == 1 for step in binding_steps)
    assert len(
        {step.read_evidence[0] for step in binding_steps}
    ) == len(binding_steps)


def test_windows_and_map_lookup_express_contextual_substitution() -> None:
    source = _word("cells", 0, 1, 0)
    table = _map(
        (_word("cells", 0, 0, 1), "left"),
        (_word("cells", 0, 1, 0), "center"),
        (_word("cells", 1, 0, 0), "right"),
    )
    windows = rules.sliding_windows(
        rules.literal_expr(source),
        1,
        1,
        rules.SequenceBoundary.FIXED,
        exterior=rules.literal_expr(0),
    )
    expression = rules.map_items(
        windows,
        rules.map_lookup(
            rules.literal_expr(table),
            rules.bound_value(),
            rules.literal_expr("missing"),
        ),
        "cells",
    )

    result, proof = _evaluate(expression)

    assert result == _word("cells", "left", "center", "right")
    window_step = next(
        step
        for step in proof.steps
        if step.expression.primitive
        is rules.ExpressionPrimitive.SLIDING_WINDOWS
    )
    assert window_step.result == _word(
        "cells",
        _word("cells", 0, 0, 1),
        _word("cells", 0, 1, 0),
        _word("cells", 1, 0, 0),
    )


def test_filter_items_can_select_by_exact_bound_rank_and_preserves_tag() -> None:
    expression = rules.filter_items(
        rules.literal_expr(_word("ranked", 10, 20, 30, 40)),
        rules.less_than(
            rules.bound_index(),
            rules.literal_expr(2),
        ),
    )

    result, proof = _evaluate(expression)

    assert result == _word("ranked", 10, 20)
    index_steps = tuple(
        step
        for step in proof.steps
        if step.expression.primitive is rules.ExpressionPrimitive.BOUND_INDEX
    )
    assert tuple(step.result for step in index_steps) == (0, 1, 2, 3)
    assert all(step.read_evidence for step in index_steps)


def test_maximal_runs_and_flat_map_items_express_look_and_say() -> None:
    runs = rules.maximal_runs(
        rules.literal_expr(_word("digits", 1, 1, 1, 2, 2, 1))
    )
    body = rules.word_value(
        "digits",
        rules.record_field(rules.bound_value(), "length"),
        rules.record_field(rules.bound_value(), "value"),
    )
    expression = rules.flat_map_items(runs, body, "digits")

    result, proof = _evaluate(expression)

    assert result == _word("digits", 3, 1, 2, 2, 1, 1)
    assert (
        proof.steps[-1].expression.primitive
        is rules.ExpressionPrimitive.FLAT_MAP_ITEMS
    )
    assert sum(
        step.expression.primitive is rules.ExpressionPrimitive.BOUND_VALUE
        for step in proof.steps
    ) == 6


def test_nested_bindings_expand_geometric_occurrences_by_de_bruijn_depth() -> None:
    factors = rules.literal_expr(_word("factors", 1, 10, 100))
    occurrence = rules.product_value(
        "occurrence",
        rules.bound_index(1),
        rules.bound_index(0),
        rules.multiply(
            rules.bound_value(1),
            rules.bound_value(0),
        ),
    )
    per_base = rules.map_items(factors, occurrence, "occurrences")
    expression = rules.flat_map_items(
        rules.literal_expr(_word("bases", 2, 3)),
        per_base,
        "occurrences",
    )

    result, proof = _evaluate(expression)

    assert result == _word(
        "occurrences",
        alphabets.product_value((0, 0, 2), tag="occurrence"),
        alphabets.product_value((0, 1, 20), tag="occurrence"),
        alphabets.product_value((0, 2, 200), tag="occurrence"),
        alphabets.product_value((1, 0, 3), tag="occurrence"),
        alphabets.product_value((1, 1, 30), tag="occurrence"),
        alphabets.product_value((1, 2, 300), tag="occurrence"),
    )
    outer_values = tuple(
        step.result
        for step in proof.steps
        if (
            step.expression.primitive
            is rules.ExpressionPrimitive.BOUND_VALUE
            and step.expression.arguments == (1,)
        )
    )
    assert outer_values == (2, 2, 2, 3, 3, 3)


def test_sequence_boundaries_are_fixed_periodic_or_endpoint_reflective() -> None:
    source = rules.literal_expr(_word("letters", "a", "b", "c"))

    fixed, _ = _evaluate(
        rules.sliding_windows(
            source,
            1,
            1,
            rules.SequenceBoundary.FIXED,
            exterior=rules.literal_expr("x"),
        )
    )
    periodic, _ = _evaluate(
        rules.sliding_windows(
            source,
            1,
            1,
            rules.SequenceBoundary.PERIODIC,
        )
    )
    reflective, _ = _evaluate(
        rules.sliding_windows(
            source,
            1,
            1,
            rules.SequenceBoundary.REFLECTIVE,
        )
    )

    assert fixed == _word(
        "letters",
        _word("letters", "x", "a", "b"),
        _word("letters", "a", "b", "c"),
        _word("letters", "b", "c", "x"),
    )
    assert periodic == _word(
        "letters",
        _word("letters", "c", "a", "b"),
        _word("letters", "a", "b", "c"),
        _word("letters", "b", "c", "a"),
    )
    assert reflective == _word(
        "letters",
        _word("letters", "b", "a", "b"),
        _word("letters", "a", "b", "c"),
        _word("letters", "b", "c", "b"),
    )


def test_empty_comprehensions_and_windows_keep_closed_word_tags() -> None:
    empty = rules.literal_expr(_word("empty"))

    assert _evaluate(
        rules.map_items(empty, rules.bound_value(9), "mapped")
    )[0] == _word("mapped")
    assert _evaluate(
        rules.filter_items(empty, rules.bound_value(9))
    )[0] == _word("empty")
    assert _evaluate(
        rules.flat_map_items(empty, rules.bound_value(9), "flattened")
    )[0] == _word("flattened")
    assert _evaluate(
        rules.sliding_windows(
            empty,
            2,
            2,
            rules.SequenceBoundary.FIXED,
            exterior=rules.bound_value(9),
        )
    )[0] == _word("empty")


@pytest.mark.parametrize(
    "expression",
    (
        rules.bound_value(),
        rules.bound_index(0),
        rules.map_items(
            rules.literal_expr(_word("items", 1)),
            rules.RuleExpr(
                rules.ExpressionPrimitive.TUPLE,
                (rules.literal_expr(1), rules.literal_expr(2)),
            ),
            "items",
        ),
        rules.filter_items(
            rules.literal_expr(_word("items", 1)),
            rules.literal_expr(2),
        ),
        rules.filter_items(
            rules.RuleExpr(
                rules.ExpressionPrimitive.TUPLE,
                (
                    rules.RuleExpr(
                        rules.ExpressionPrimitive.TUPLE,
                        (rules.literal_expr(1),),
                    ),
                ),
            ),
            rules.literal_expr(0),
        ),
        rules.flat_map_items(
            rules.literal_expr(_word("items", 1)),
            rules.literal_expr(1),
            "items",
        ),
        rules.flat_map_items(
            rules.literal_expr(_word("items", 1)),
            rules.word_value("wrong", rules.bound_value()),
            "items",
        ),
        rules.map_items(
            rules.literal_expr(_word("items", 1)),
            rules.bound_value(1),
            "items",
        ),
    ),
)
def test_binding_evaluation_fails_closed_on_scope_type_or_tag_errors(
    expression: rules.RuleExpr,
) -> None:
    with pytest.raises((IndexError, TypeError, ValueError)):
        _evaluate(expression)


@pytest.mark.parametrize(
    ("primitive", "arguments"),
    (
        (rules.ExpressionPrimitive.BOUND_VALUE, ()),
        (rules.ExpressionPrimitive.BOUND_INDEX, (True,)),
        (
            rules.ExpressionPrimitive.MAP_ITEMS,
            (rules.literal_expr(1), rules.literal_expr(1), ""),
        ),
        (
            rules.ExpressionPrimitive.FILTER_ITEMS,
            (rules.literal_expr(1),),
        ),
        (
            rules.ExpressionPrimitive.FLAT_MAP_ITEMS,
            (rules.literal_expr(1), rules.literal_expr(1), 3),
        ),
        (
            rules.ExpressionPrimitive.SLIDING_WINDOWS,
            (
                rules.literal_expr(_word("items")),
                1,
                1,
                rules.SequenceBoundary.FIXED.value,
            ),
        ),
        (
            rules.ExpressionPrimitive.SLIDING_WINDOWS,
            (
                rules.literal_expr(_word("items")),
                1,
                1,
                rules.SequenceBoundary.PERIODIC.value,
                rules.literal_expr(0),
            ),
        ),
        (
            rules.ExpressionPrimitive.SLIDING_WINDOWS,
            (rules.literal_expr(_word("items")), -1, 1, "unknown"),
        ),
    ),
)
def test_comprehension_expression_shapes_fail_at_construction(
    primitive: rules.ExpressionPrimitive,
    arguments: tuple[object, ...],
) -> None:
    with pytest.raises((TypeError, ValueError)):
        rules.RuleExpr(primitive, arguments)  # type: ignore[arg-type]


def test_public_comprehension_helpers_reject_invalid_literal_parameters() -> None:
    with pytest.raises(ValueError):
        rules.bound_value(True)
    with pytest.raises(ValueError):
        rules.bound_index(-1)
    with pytest.raises(ValueError):
        rules.map_items(
            rules.literal_expr(_word("items")),
            rules.literal_expr(1),
            "",
        )
    with pytest.raises(ValueError):
        rules.flat_map_items(
            rules.literal_expr(_word("items")),
            rules.literal_expr(1),
            "",
        )
    with pytest.raises(ValueError):
        rules.sliding_windows(
            rules.literal_expr(_word("items")),
            -1,
            0,
            rules.SequenceBoundary.PERIODIC,
        )
    with pytest.raises(ValueError):
        rules.sliding_windows(
            rules.literal_expr(_word("items")),
            0,
            True,
            rules.SequenceBoundary.PERIODIC,
        )
    with pytest.raises(TypeError):
        rules.sliding_windows(
            rules.literal_expr(_word("items")),
            0,
            0,
            "periodic",  # type: ignore[arg-type]
        )
    with pytest.raises(ValueError):
        rules.sliding_windows(
            rules.literal_expr(_word("items")),
            0,
            0,
            rules.SequenceBoundary.FIXED,
        )
    with pytest.raises(ValueError):
        rules.sliding_windows(
            rules.literal_expr(_word("items")),
            0,
            0,
            rules.SequenceBoundary.REFLECTIVE,
            exterior=rules.literal_expr(0),
        )
