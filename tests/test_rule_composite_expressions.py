"""Focused tests for the sealed composite/numeric Rule expression algebra."""

from fractions import Fraction

import pytest

from ca import alphabets, loci, neighborhoods, rules


def _readable_view():
    source = loci.record_configuration((("fixture", 0),))
    return neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.INTEGER,
    ).resolve(source)


def _evaluate(expression: rules.RuleExpr):
    result, proof = rules._evaluate_proven(  # noqa: SLF001 - interpreter unit test
        expression,
        _readable_view(),
        anchor=None,
    )
    assert proof.steps[-1].expression == expression
    assert proof.steps[-1].result == result
    return result, proof


def _word(tag: str, *items: alphabets.SemanticValue) -> alphabets.ValueNode:
    return alphabets.ValueNode(alphabets.ValueKind.WORD, tag, items=items)


def _product(tag: str, *items: alphabets.SemanticValue) -> alphabets.ValueNode:
    return alphabets.ValueNode(alphabets.ValueKind.PRODUCT, tag, items=items)


def _map(
    *entries: tuple[alphabets.SemanticValue, alphabets.SemanticValue],
    tag: str = "map",
) -> alphabets.ValueNode:
    return alphabets.map_value(
        tuple(
            alphabets.map_entry_value(key, value)
            for key, value in entries
        ),
        tag=tag,
    )


def test_dynamic_products_words_and_record_updates_remain_semantic_values() -> None:
    record = alphabets.ValueNode(
        alphabets.ValueKind.RECORD,
        "machine-cell",
        fields=(("state", "q0"), ("symbol", 1)),
    )
    key_expression = rules.product_value(
        "transition-key",
        rules.record_field(rules.literal_expr(record), "state"),
        rules.record_field(rules.literal_expr(record), "symbol"),
    )
    updated_expression = rules.record_update(
        rules.literal_expr(record),
        "state",
        rules.literal_expr("q1"),
    )
    word_expression = rules.word_value(
        "trace",
        key_expression,
        updated_expression,
    )

    key, key_proof = _evaluate(key_expression)
    updated, _ = _evaluate(updated_expression)
    word, word_proof = _evaluate(word_expression)

    assert key == _product("transition-key", "q0", 1)
    assert updated == alphabets.ValueNode(
        alphabets.ValueKind.RECORD,
        "machine-cell",
        fields=(("state", "q1"), ("symbol", 1)),
    )
    assert record.fields == (("state", "q0"), ("symbol", 1))
    assert word == _word("trace", key, updated)
    assert type(word) is alphabets.ValueNode
    assert (
        key_proof.steps[-1].expression.primitive
        is rules.ExpressionPrimitive.PRODUCT_VALUE
    )
    assert (
        word_proof.steps[-1].expression.primitive
        is rules.ExpressionPrimitive.WORD_VALUE
    )


def test_record_access_and_update_are_strict() -> None:
    record = alphabets.ValueNode(
        alphabets.ValueKind.RECORD,
        "pair",
        fields=(("left", 1), ("right", 2)),
    )

    with pytest.raises(KeyError, match="absent"):
        _evaluate(
            rules.record_field(rules.literal_expr(record), "missing")
        )
    with pytest.raises(KeyError, match="absent"):
        _evaluate(
            rules.record_update(
                rules.literal_expr(record),
                "missing",
                rules.literal_expr(3),
            )
        )
    with pytest.raises(TypeError, match="record"):
        _evaluate(
            rules.record_field(
                rules.literal_expr(_word("not-a-record", 1)),
                "left",
            )
        )


def test_word_and_tuple_sequence_operations_are_exact_and_tag_preserving() -> None:
    tape = _word("tape", "a", "b", "c", "d")
    source = rules.literal_expr(tape)

    assert _evaluate(rules.length(source))[0] == 4
    assert _evaluate(
        rules.item_at(source, rules.literal_expr(2), rules.literal_expr("x"))
    )[0] == "c"
    assert _evaluate(
        rules.item_at(source, rules.literal_expr(9), rules.literal_expr("x"))
    )[0] == "x"
    assert _evaluate(
        rules.item_at(source, rules.literal_expr(-1), rules.literal_expr("x"))
    )[0] == "x"
    assert _evaluate(
        rules.slice_items(
            source,
            rules.literal_expr(1),
            rules.literal_expr(3),
        )
    )[0] == _word("tape", "b", "c")
    assert _evaluate(rules.reverse(source))[0] == _word(
        "tape", "d", "c", "b", "a"
    )
    assert _evaluate(
        rules.replace_at(
            source,
            rules.literal_expr(1),
            rules.literal_expr("B"),
        )
    )[0] == _word("tape", "a", "B", "c", "d")

    joined = rules.concatenate(
        rules.slice_items(
            source,
            rules.literal_expr(0),
            rules.literal_expr(2),
        ),
        rules.slice_items(
            source,
            rules.literal_expr(2),
            rules.literal_expr(4),
        ),
    )
    assert _evaluate(joined)[0] == tape

    runtime_tuple = rules.RuleExpr(
        rules.ExpressionPrimitive.TUPLE,
        (rules.literal_expr(1), rules.literal_expr(2)),
    )
    tuple_slice = rules.slice_items(
        runtime_tuple,
        rules.literal_expr(0),
        rules.literal_expr(2),
    )
    assert _evaluate(tuple_slice)[0] == _word("word", 1, 2)


@pytest.mark.parametrize(
    "expression",
    (
        rules.item_at(
            rules.literal_expr(_word("w", 1)),
            rules.literal_expr(True),
            rules.literal_expr(0),
        ),
        rules.slice_items(
            rules.literal_expr(_word("w", 1)),
            rules.literal_expr(-1),
            rules.literal_expr(1),
        ),
        rules.slice_items(
            rules.literal_expr(_word("w", 1)),
            rules.literal_expr(0),
            rules.literal_expr(2),
        ),
        rules.replace_at(
            rules.literal_expr(_word("w", 1)),
            rules.literal_expr(1),
            rules.literal_expr(2),
        ),
        rules.concatenate(
            rules.literal_expr(_word("left", 1)),
            rules.literal_expr(_word("right", 2)),
        ),
    ),
)
def test_sequence_operations_reject_implicit_coercion_or_bounds(
    expression: rules.RuleExpr,
) -> None:
    with pytest.raises((TypeError, ValueError, IndexError)):
        _evaluate(expression)


def test_semantic_key_maps_support_products_lookup_update_and_defaults() -> None:
    key_q0 = _product("transition-key", "q0", 1)
    key_q1 = _product("transition-key", "q1", 1)
    table = _map(
        (key_q1, _word("tape", "R")),
        (key_q0, _word("tape", "L")),
        tag="transitions",
    )
    dynamic_key = rules.product_value(
        "transition-key",
        rules.literal_expr("q0"),
        rules.literal_expr(1),
    )

    assert _evaluate(
        rules.map_lookup(
            rules.literal_expr(table),
            dynamic_key,
            rules.literal_expr(_word("tape", "?")),
        )
    )[0] == _word("tape", "L")
    assert _evaluate(
        rules.map_lookup(
            rules.literal_expr(table),
            rules.literal_expr(_product("transition-key", "missing", 0)),
            rules.literal_expr(_word("tape", "?")),
        )
    )[0] == _word("tape", "?")

    changed, _ = _evaluate(
        rules.map_update(
            rules.literal_expr(table),
            rules.literal_expr(key_q0),
            rules.literal_expr(_word("tape", "S")),
        )
    )
    assert type(changed) is alphabets.ValueNode
    assert changed.tag == "transitions"
    assert _evaluate(
        rules.map_lookup(
            rules.literal_expr(changed),
            rules.literal_expr(key_q0),
            rules.literal_expr(_word("tape", "?")),
        )
    )[0] == _word("tape", "S")

    inserted, _ = _evaluate(
        rules.map_update(
            rules.literal_expr(changed),
            rules.literal_expr(7),
            rules.literal_expr("seven"),
        )
    )
    assert _evaluate(
        rules.map_lookup(
            rules.literal_expr(inserted),
            rules.literal_expr(7),
            rules.literal_expr("missing"),
        )
    )[0] == "seven"
    assert inserted.tag == "transitions"


def test_rule_comparisons_use_alphabet_semantics_for_exact_values() -> None:
    first = alphabets.AlgebraicNumber(
        (1, 0, -2),
        (Fraction(1), Fraction(2)),
    )
    equivalent = alphabets.AlgebraicNumber(
        (2, 0, -4),
        (Fraction(4, 3), Fraction(3, 2)),
    )
    assert first != equivalent
    assert alphabets.semantic_equal(first, equivalent)

    assert _evaluate(
        rules.equal(
            rules.literal_expr(first),
            rules.literal_expr(equivalent),
        )
    )[0] is True
    left_tuple = rules.RuleExpr(
        rules.ExpressionPrimitive.TUPLE,
        (rules.literal_expr(first), rules.literal_expr("tail")),
    )
    right_tuple = rules.RuleExpr(
        rules.ExpressionPrimitive.TUPLE,
        (rules.literal_expr(equivalent), rules.literal_expr("tail")),
    )
    assert _evaluate(rules.equal(left_tuple, right_tuple))[0] is True

    source = _word("values", first, "separator")
    assert _evaluate(
        rules.index_of(
            rules.literal_expr(source),
            rules.literal_expr(equivalent),
            rules.literal_expr(-1),
        )
    )[0] == 0

    runs, _ = _evaluate(
        rules.maximal_runs(
            rules.literal_expr(_word("values", first, equivalent))
        )
    )
    run_items = alphabets.word_items(runs)
    assert len(run_items) == 1
    assert alphabets.record_get(run_items[0], "length") == 2

    table = _map((first, "old"), tag="algebraic-keys")
    assert _evaluate(
        rules.map_lookup(
            rules.literal_expr(table),
            rules.literal_expr(equivalent),
            rules.literal_expr("missing"),
        )
    )[0] == "old"
    updated, _ = _evaluate(
        rules.map_update(
            rules.literal_expr(table),
            rules.literal_expr(equivalent),
            rules.literal_expr("new"),
        )
    )
    assert updated.tag == "algebraic-keys"
    assert len(alphabets.map_entries(updated)) == 1
    assert alphabets.map_get(updated, first) == "new"


def test_semantic_key_maps_reject_duplicate_or_malformed_entries() -> None:
    with pytest.raises(ValueError, match="unique"):
        _map((1, "a"), (1, "b"))

    with pytest.raises(ValueError, match="entry"):
        alphabets.ValueNode(
            alphabets.ValueKind.MAP,
            "map",
            items=(_product("wrong-entry-tag", 1, "a"),),
        )

    with pytest.raises(TypeError, match="map"):
        _evaluate(
            rules.map_lookup(
                rules.literal_expr(_word("not-a-map")),
                rules.literal_expr(1),
                rules.literal_expr("missing"),
            )
        )


def test_flat_map_lookup_is_ordered_total_and_word_valued() -> None:
    source = _word("symbols", "A", "B", "A")
    table = _map(
        ("A", _word("symbols", "A", "B")),
        ("B", _word("symbols")),
    )

    result, proof = _evaluate(
        rules.flat_map_lookup(
            rules.literal_expr(source),
            rules.literal_expr(table),
        )
    )

    assert result == _word("symbols", "A", "B", "A", "B")
    assert (
        proof.steps[-1].expression.primitive
        is rules.ExpressionPrimitive.FLAT_MAP_LOOKUP
    )

    with pytest.raises(KeyError, match="not total"):
        _evaluate(
            rules.flat_map_lookup(
                rules.literal_expr(_word("symbols", "C")),
                rules.literal_expr(table),
            )
        )
    with pytest.raises(TypeError, match="word"):
        _evaluate(
            rules.flat_map_lookup(
                rules.literal_expr(_word("symbols", "A")),
                rules.literal_expr(_map(("A", 1))),
            )
        )
    with pytest.raises(ValueError, match="tag"):
        _evaluate(
            rules.flat_map_lookup(
                rules.literal_expr(_word("symbols", "A")),
                rules.literal_expr(
                    _map(("A", _word("other", "A")))
                ),
            )
        )


def test_index_and_tag_search_use_exact_semantic_equality() -> None:
    needle = _product("key", 1, "x")
    word = _word(
        "values",
        0,
        needle,
        alphabets.ValueNode(
            alphabets.ValueKind.TAG,
            "head",
            items=("q0",),
        ),
    )

    assert _evaluate(
        rules.index_of(
            rules.literal_expr(word),
            rules.literal_expr(needle),
            rules.literal_expr(-1),
        )
    )[0] == 1
    assert _evaluate(
        rules.index_of_tag(
            rules.literal_expr(word),
            "head",
            rules.literal_expr(-1),
        )
    )[0] == 2
    assert _evaluate(
        rules.index_of_tag(
            rules.literal_expr(word),
            "absent",
            rules.literal_expr(-1),
        )
    )[0] == -1


def test_exact_numeric_and_positional_operations_compose() -> None:
    assert _evaluate(
        rules.floor_divide(
            rules.literal_expr(Fraction(-7, 3)),
            rules.literal_expr(Fraction(2, 3)),
        )
    )[0] == -4
    assert _evaluate(
        rules.absolute(rules.literal_expr(Fraction(-7, 3)))
    )[0] == Fraction(7, 3)
    assert _evaluate(
        rules.fractional_part(rules.literal_expr(Fraction(-7, 3)))
    )[0] == Fraction(-1, 3)
    assert _evaluate(
        rules.fractional_part(rules.literal_expr(4))
    )[0] == 0

    digits, _ = _evaluate(rules.integer_digits(rules.literal_expr(16), 2))
    assert digits == _word("digits", 1, 0, 0, 0, 0)
    fixed, _ = _evaluate(
        rules.integer_digits(rules.literal_expr(2), 2, width=4)
    )
    assert fixed == _word("digits", 0, 0, 1, 0)
    assert _evaluate(
        rules.from_digits(rules.literal_expr(fixed), 2)
    )[0] == 2

    reversal_add = rules.add(
        rules.literal_expr(16),
        rules.from_digits(
            rules.reverse(rules.integer_digits(rules.literal_expr(16), 2)),
            2,
        ),
    )
    result, proof = _evaluate(reversal_add)
    assert result == 17
    assert {
        step.expression.primitive for step in proof.steps
    }.issuperset(
        {
            rules.ExpressionPrimitive.INTEGER_DIGITS,
            rules.ExpressionPrimitive.REVERSE,
            rules.ExpressionPrimitive.FROM_DIGITS,
            rules.ExpressionPrimitive.ADD,
        }
    )


@pytest.mark.parametrize(
    ("expression", "error"),
    (
        (
            rules.floor_divide(
                rules.literal_expr(1),
                rules.literal_expr(0),
            ),
            ZeroDivisionError,
        ),
        (
            rules.floor_divide(
                rules.literal_expr(True),
                rules.literal_expr(1),
            ),
            TypeError,
        ),
        (
            rules.fractional_part(rules.literal_expr(False)),
            TypeError,
        ),
        (
            rules.integer_digits(rules.literal_expr(-1), 2),
            ValueError,
        ),
        (
            rules.integer_digits(rules.literal_expr(True), 2),
            TypeError,
        ),
        (
            rules.integer_digits(rules.literal_expr(8), 2, width=3),
            OverflowError,
        ),
        (
            rules.from_digits(
                rules.literal_expr(_word("digits", 0, 2)),
                2,
            ),
            ValueError,
        ),
        (
            rules.from_digits(
                rules.literal_expr(_word("digits")),
                2,
            ),
            ValueError,
        ),
    ),
)
def test_numeric_operations_fail_closed(
    expression: rules.RuleExpr,
    error: type[Exception],
) -> None:
    with pytest.raises(error):
        _evaluate(expression)


def test_maximal_runs_encode_complete_named_records() -> None:
    source = _word("symbols", "A", "A", "B", "B", "B", "A")

    encoded, proof = _evaluate(
        rules.maximal_runs(rules.literal_expr(source))
    )

    assert encoded == _word(
        "runs",
        alphabets.ValueNode(
            alphabets.ValueKind.RECORD,
            "run",
            fields=(("value", "A"), ("start", 0), ("length", 2)),
        ),
        alphabets.ValueNode(
            alphabets.ValueKind.RECORD,
            "run",
            fields=(("value", "B"), ("start", 2), ("length", 3)),
        ),
        alphabets.ValueNode(
            alphabets.ValueKind.RECORD,
            "run",
            fields=(("value", "A"), ("start", 5), ("length", 1)),
        ),
    )
    assert type(encoded) is alphabets.ValueNode
    assert (
        proof.steps[-1].expression.primitive
        is rules.ExpressionPrimitive.MAXIMAL_RUNS
    )
    assert _evaluate(
        rules.maximal_runs(rules.literal_expr(_word("symbols")))
    )[0] == _word("runs")


@pytest.mark.parametrize(
    ("primitive", "arguments"),
    (
        (rules.ExpressionPrimitive.RECORD_FIELD, (rules.literal_expr(1), "")),
        (
            rules.ExpressionPrimitive.RECORD_UPDATE,
            (rules.literal_expr(1), "field", 2),
        ),
        (rules.ExpressionPrimitive.LENGTH, ()),
        (
            rules.ExpressionPrimitive.ITEM_AT,
            (rules.literal_expr(1), rules.literal_expr(0)),
        ),
        (rules.ExpressionPrimitive.SLICE, (rules.literal_expr(1),)),
        (rules.ExpressionPrimitive.CONCATENATE, ()),
        (rules.ExpressionPrimitive.CONCATENATE, (1,)),
        (
            rules.ExpressionPrimitive.INDEX_OF_TAG,
            (rules.literal_expr(1), "", rules.literal_expr(-1)),
        ),
        (
            rules.ExpressionPrimitive.INTEGER_DIGITS,
            (rules.literal_expr(1), 1),
        ),
        (
            rules.ExpressionPrimitive.FROM_DIGITS,
            (rules.literal_expr(1), True),
        ),
        (rules.ExpressionPrimitive.PRODUCT_VALUE, ("key",)),
        (rules.ExpressionPrimitive.WORD_VALUE, ("",)),
        (
            rules.ExpressionPrimitive.FLAT_MAP_LOOKUP,
            (rules.literal_expr(1),),
        ),
    ),
)
def test_composite_expression_shapes_fail_at_construction(
    primitive: rules.ExpressionPrimitive,
    arguments: tuple[object, ...],
) -> None:
    with pytest.raises((TypeError, ValueError)):
        rules.RuleExpr(primitive, arguments)  # type: ignore[arg-type]


def test_public_helpers_reject_invalid_literal_schema_parameters() -> None:
    with pytest.raises(ValueError):
        rules.record_field(rules.literal_expr(1), "")
    with pytest.raises(ValueError):
        rules.index_of_tag(rules.literal_expr(_word("w")), "", rules.literal_expr(-1))
    with pytest.raises(ValueError):
        rules.integer_digits(rules.literal_expr(1), 1)
    with pytest.raises(ValueError):
        rules.integer_digits(rules.literal_expr(1), 2, width=0)
    with pytest.raises(ValueError):
        rules.from_digits(rules.literal_expr(_word("digits", 1)), 1)
    with pytest.raises(ValueError):
        rules.product_value("key")
    with pytest.raises(ValueError):
        rules.word_value("")
