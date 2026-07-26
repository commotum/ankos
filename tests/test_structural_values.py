"""Focused structural Alphabet values that future generic Rules can consume."""

from __future__ import annotations

from fractions import Fraction

import pytest

from ca import alphabets


def test_symbolic_expression_schema_is_structural_not_a_finite_symbol_enum() -> None:
    expression = alphabets.symbolic_value(
        "add",
        items=(
            alphabets.symbolic_value("x"),
            0,
        ),
    )
    expression_schema = alphabets.symbolic_expression()
    finite_symbols = alphabets.symbolic(("x", "y"))

    assert (
        alphabets.AlphabetKind.SYMBOLIC_EXPRESSION.value
        == "symbolic-expression"
    )
    assert expression_schema.value_profile is alphabets.ValueProfile.STRUCTURAL
    assert expression_schema.contains(expression)
    assert not expression_schema.contains("x")
    assert not expression_schema.contains(alphabets.pattern_value("x"))

    assert finite_symbols.value_profile is alphabets.ValueProfile.SYMBOLIC
    assert finite_symbols.contains("x")
    assert not finite_symbols.contains(expression)


@pytest.mark.parametrize(
    ("axes", "shape", "cells", "tag"),
    (
        (("x",), (3,), (0, 1, 2), "line"),
        (
            ("row", "column"),
            (2, 3),
            ("00", "01", "02", "10", "11", "12"),
            "grid",
        ),
        (
            ("a", "b", "c", "d"),
            (1, 2, 1, 2),
            (
                False,
                Fraction(1, 3),
                alphabets.symbolic_value("leaf"),
                "tail",
            ),
            "rank-four",
        ),
    ),
)
def test_grid_field_roundtrips_rank_n_last_axis_fastest(
    axes: tuple[str, ...],
    shape: tuple[int, ...],
    cells: tuple[alphabets.SemanticValue, ...],
    tag: str,
) -> None:
    value = alphabets.grid_field_value(
        axes,
        shape,
        cells,
        tag=tag,
    )

    assert value.kind is alphabets.ValueKind.FIELD
    assert value.tag == tag
    assert value.items == ()
    assert tuple(name for name, _ in value.fields) == (
        "axes",
        "cells",
        "shape",
    )
    fields = dict(value.fields)
    assert fields["axes"].tag == "grid-axes"
    assert fields["cells"].tag == "grid-cells"
    assert fields["shape"].tag == "grid-shape"
    assert alphabets.grid_field_parts(value) == (axes, shape, cells)
    assert alphabets.field().contains(value)
    assert not alphabets.symbolic_expression().contains(value)


def test_grid_field_semantic_equality_uses_axes_shape_cell_order_and_tag() -> None:
    cells = ("00", "01", "10", "11")
    canonical = alphabets.grid_field_value(
        ("row", "column"),
        (2, 2),
        cells,
    )
    independently_built = alphabets.field_value(
        "grid",
        fields=(
            (
                "shape",
                alphabets.word_value((2, 2), tag="grid-shape"),
            ),
            (
                "cells",
                alphabets.word_value(cells, tag="grid-cells"),
            ),
            (
                "axes",
                alphabets.word_value(
                    ("row", "column"),
                    tag="grid-axes",
                ),
            ),
        ),
    )

    assert alphabets.semantic_equal(canonical, independently_built)
    assert alphabets.grid_field_parts(independently_built) == (
        ("row", "column"),
        (2, 2),
        cells,
    )
    assert not alphabets.semantic_equal(
        canonical,
        alphabets.grid_field_value(
            ("column", "row"),
            (2, 2),
            cells,
        ),
    )
    assert not alphabets.semantic_equal(
        canonical,
        alphabets.grid_field_value(
            ("row", "column"),
            (2, 2),
            ("00", "10", "01", "11"),
        ),
    )
    assert not alphabets.semantic_equal(
        canonical,
        alphabets.grid_field_value(
            ("row", "column"),
            (2, 2),
            cells,
            tag="tile",
        ),
    )


@pytest.mark.parametrize(
    ("axes", "shape", "cells", "error"),
    (
        ((), (), (), ValueError),
        (["x"], (1,), (0,), TypeError),
        (("x",), [1], (0,), TypeError),
        (("x",), (1,), [0], TypeError),
        (("",), (1,), (0,), TypeError),
        (("x", "x"), (1, 1), (0,), ValueError),
        (("x",), (1, 1), (0,), ValueError),
        (("x",), (True,), (0,), TypeError),
        (("x",), (0,), (), ValueError),
        (("x",), (-1,), (), ValueError),
        (("x",), (2,), (), ValueError),
        (("x",), (1,), (object(),), TypeError),
    ),
)
def test_grid_field_builder_rejects_empty_or_malformed_parts(
    axes: object,
    shape: object,
    cells: object,
    error: type[Exception],
) -> None:
    with pytest.raises(error):
        alphabets.grid_field_value(axes, shape, cells)  # type: ignore[arg-type]


def _raw_grid_field(
    *,
    axes: alphabets.SemanticValue,
    shape: alphabets.SemanticValue,
    cells: alphabets.SemanticValue,
    items: tuple[alphabets.SemanticValue, ...] = (),
    extra: tuple[tuple[str, alphabets.SemanticValue], ...] = (),
) -> alphabets.ValueNode:
    return alphabets.field_value(
        "grid",
        items=items,
        fields=(
            ("axes", axes),
            ("cells", cells),
            ("shape", shape),
            *extra,
        ),
    )


@pytest.mark.parametrize(
    ("value", "error"),
    (
        (0, TypeError),
        (alphabets.symbolic_value("grid"), TypeError),
        (alphabets.field_value("arbitrary"), ValueError),
        (
            _raw_grid_field(
                axes=alphabets.word_value(("x",), tag="grid-axes"),
                shape=alphabets.word_value((1,), tag="grid-shape"),
                cells=alphabets.word_value((0,), tag="grid-cells"),
                items=(0,),
            ),
            ValueError,
        ),
        (
            alphabets.field_value(
                "grid",
                fields=(
                    (
                        "axes",
                        alphabets.word_value(("x",), tag="grid-axes"),
                    ),
                    (
                        "cells",
                        alphabets.word_value((0,), tag="grid-cells"),
                    ),
                ),
            ),
            ValueError,
        ),
        (
            _raw_grid_field(
                axes=alphabets.word_value(("x",), tag="wrong"),
                shape=alphabets.word_value((1,), tag="grid-shape"),
                cells=alphabets.word_value((0,), tag="grid-cells"),
            ),
            ValueError,
        ),
        (
            _raw_grid_field(
                axes="x",
                shape=alphabets.word_value((1,), tag="grid-shape"),
                cells=alphabets.word_value((0,), tag="grid-cells"),
            ),
            TypeError,
        ),
        (
            _raw_grid_field(
                axes=alphabets.word_value((0,), tag="grid-axes"),
                shape=alphabets.word_value((1,), tag="grid-shape"),
                cells=alphabets.word_value((0,), tag="grid-cells"),
            ),
            TypeError,
        ),
        (
            _raw_grid_field(
                axes=alphabets.word_value(("x",), tag="grid-axes"),
                shape=alphabets.word_value((True,), tag="grid-shape"),
                cells=alphabets.word_value((0,), tag="grid-cells"),
            ),
            TypeError,
        ),
        (
            _raw_grid_field(
                axes=alphabets.word_value(("x",), tag="grid-axes"),
                shape=alphabets.word_value((2,), tag="grid-shape"),
                cells=alphabets.word_value((0,), tag="grid-cells"),
            ),
            ValueError,
        ),
        (
            _raw_grid_field(
                axes=alphabets.word_value(("x",), tag="grid-axes"),
                shape=alphabets.word_value((1,), tag="grid-shape"),
                cells=alphabets.word_value((0,), tag="grid-cells"),
                extra=(("metadata", 0),),
            ),
            ValueError,
        ),
    ),
)
def test_grid_field_parser_rejects_arbitrary_or_malformed_fields(
    value: object,
    error: type[Exception],
) -> None:
    with pytest.raises(error):
        alphabets.grid_field_parts(value)  # type: ignore[arg-type]


def test_generic_field_schema_does_not_claim_every_field_is_a_dense_grid() -> None:
    arbitrary = alphabets.field_value(
        "continuous-field",
        fields=(("equation", "u_t = u_xx"),),
    )

    assert alphabets.field().contains(arbitrary)
    with pytest.raises(ValueError):
        alphabets.grid_field_parts(arbitrary)
