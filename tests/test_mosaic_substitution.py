"""Focused tests for sealed rank-N dense-field mosaic substitution."""

from __future__ import annotations

import pytest

import ca
from ca import (
    alphabets,
    frontiers,
    loci,
    neighborhoods,
    program,
    rules,
    seeds,
)


def _readable_view():
    source = loci.record_configuration((("fixture", 0),))
    return neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.STRUCTURAL,
    ).resolve(source)


def _evaluate(expression: rules.RuleExpr) -> alphabets.SemanticValue:
    result, proof = rules._evaluate_proven(  # noqa: SLF001 - interpreter test
        expression,
        _readable_view(),
        anchor=None,
    )
    assert proof.steps[-1].expression == expression
    assert proof.steps[-1].result == result
    return result


def _grid(
    axes: tuple[str, ...],
    shape: tuple[int, ...],
    cells: tuple[alphabets.SemanticValue, ...],
    *,
    tag: str = "grid",
) -> alphabets.ValueNode:
    return alphabets.grid_field_value(axes, shape, cells, tag=tag)


def _map(
    *entries: tuple[
        alphabets.SemanticValue,
        alphabets.SemanticValue,
    ],
) -> alphabets.ValueNode:
    return alphabets.map_value(
        tuple(
            alphabets.map_entry_value(key, value)
            for key, value in entries
        ),
        tag="mosaic-productions",
    )


def _context(
    *items: alphabets.SemanticValue,
) -> alphabets.ValueNode:
    return alphabets.word_value(items, tag="mosaic-context")


def _public_apply_field(
    source_field: alphabets.ValueNode,
    expression: rules.RuleExpr,
) -> alphabets.ValueNode:
    source = loci.record_configuration((("field", source_field),))
    alphabet = alphabets.field()
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    rule = rules.expression(
        rules.ExistingPlan(
            rules.ExistingPlanKind.BY_INDEX,
            (expression,),
        ),
        contract=rules.RuleContract(
            source.contract,
            alphabet.value_profile,
            readable.result_shape,
            readable.join_shape,
            writable.effect_profile,
        ),
        witness=rules.literal_expr("mosaic-public-apply"),
        provenance=("test:mosaic-public-apply",),
    )
    simple_program = ca.SimpleProgram(
        seed=seeds.exact(
            source,
            value_profile=alphabet.value_profile,
        ),
        alphabet=alphabet,
        frontier=writable,
        neighborhood=readable,
        rule=rule,
    )

    applied = ca.apply(simple_program, source)

    assert type(applied) is program.ApplicationComplete
    for semantic_value in (simple_program, applied):
        encoded = ca.serialization.dumps(semantic_value)
        assert ca.serialization.loads(encoded) == (
            ca.serialization.Decoded(semantic_value)
        )
        assert ca.serialization.dumps(semantic_value) == encoded
    groups = applied.successor_quotient_with_derivation_fibers.atoms
    assert len(groups) == 1
    assert type(groups[0]) is program.SuccessorGroup
    successor = groups[0].successor
    assert type(successor) is loci.FiniteConfiguration
    assert len(successor.entries) == 1
    value = successor.entries[0][1]
    assert type(value) is alphabets.ValueNode
    assert value.kind is alphabets.ValueKind.FIELD
    return value


def _substitute(
    source: alphabets.SemanticValue,
    productions: alphabets.SemanticValue,
    *,
    offsets: tuple[tuple[int, ...], ...] = (),
    boundary: rules.SequenceBoundary | None = None,
    exterior: rules.RuleExpr | None = None,
) -> alphabets.ValueNode:
    result = _evaluate(
        rules.mosaic_substitute(
            rules.literal_expr(source),
            rules.literal_expr(productions),
            offsets=offsets,
            boundary=boundary,
            exterior=exterior,
        )
    )
    assert type(result) is alphabets.ValueNode
    assert result.kind is alphabets.ValueKind.FIELD
    return result


def test_two_dimensional_tiles_assemble_by_product_coordinates() -> None:
    axes = ("row", "column")
    source = _grid(
        axes,
        (2, 2),
        ("A", "B", "C", "D"),
        tag="source-grid",
    )
    productions = _map(
        (
            "A",
            _grid(axes, (2, 2), ("A00", "A01", "A10", "A11")),
        ),
        (
            "B",
            _grid(axes, (2, 2), ("B00", "B01", "B10", "B11")),
        ),
        (
            "C",
            _grid(axes, (2, 2), ("C00", "C01", "C10", "C11")),
        ),
        (
            "D",
            _grid(axes, (2, 2), ("D00", "D01", "D10", "D11")),
        ),
    )

    result = _substitute(source, productions)

    assert result.tag == "source-grid"
    assert alphabets.grid_field_parts(result) == (
        axes,
        (4, 4),
        (
            "A00",
            "A01",
            "B00",
            "B01",
            "A10",
            "A11",
            "B10",
            "B11",
            "C00",
            "C01",
            "D00",
            "D01",
            "C10",
            "C11",
            "D10",
            "D11",
        ),
    )


def test_independent_lookup_keeps_false_and_zero_semantically_distinct() -> None:
    axes = ("x",)
    source = _grid(axes, (2,), (False, 0))
    productions = _map(
        (False, _grid(axes, (1,), ("false",))),
        (0, _grid(axes, (1,), ("zero",))),
    )

    result = _substitute(source, productions)

    assert alphabets.grid_field_parts(result) == (
        axes,
        (2,),
        ("false", "zero"),
    )


def test_rank_four_periodic_context_uses_declared_offset_order() -> None:
    axes = ("a", "b", "c", "d")
    source = _grid(
        axes,
        (1, 1, 2, 2),
        ("A", "B", "C", "D"),
        tag="rank-four",
    )
    tile_shape = (1, 1, 1, 1)
    productions = _map(
        (
            _context("A", "B", "C"),
            _grid(axes, tile_shape, ("a",)),
        ),
        (
            _context("B", "A", "D"),
            _grid(axes, tile_shape, ("b",)),
        ),
        (
            _context("C", "D", "A"),
            _grid(axes, tile_shape, ("c",)),
        ),
        (
            _context("D", "C", "B"),
            _grid(axes, tile_shape, ("d",)),
        ),
    )

    result = _substitute(
        source,
        productions,
        offsets=(
            (0, 0, 0, 0),
            (0, 0, 0, 1),
            (0, 0, 1, 0),
        ),
        boundary=rules.SequenceBoundary.PERIODIC,
    )

    assert alphabets.grid_field_parts(result) == (
        axes,
        (1, 1, 2, 2),
        ("a", "b", "c", "d"),
    )
    assert result.tag == source.tag


def test_rank_four_fixed_exterior_context_expands_last_axis() -> None:
    axes = ("a", "b", "c", "d")
    source = _grid(axes, (1, 1, 1, 2), ("A", "B"))
    tile_shape = (1, 1, 1, 2)
    productions = _map(
        (
            _context("E", "A", "B"),
            _grid(axes, tile_shape, ("A0", "A1")),
        ),
        (
            _context("A", "B", "E"),
            _grid(axes, tile_shape, ("B0", "B1")),
        ),
    )

    result = _substitute(
        source,
        productions,
        offsets=(
            (0, 0, 0, -1),
            (0, 0, 0, 0),
            (0, 0, 0, 1),
        ),
        boundary=rules.SequenceBoundary.FIXED,
        exterior=rules.literal_expr("E"),
    )

    assert alphabets.grid_field_parts(result) == (
        axes,
        (1, 1, 1, 4),
        ("A0", "A1", "B0", "B1"),
    )


def test_two_dimensional_and_rank_four_mosaics_execute_through_public_apply() -> None:
    axes_2d = ("row", "column")
    source_2d = _grid(
        axes_2d,
        (2, 2),
        ("A", "B", "C", "D"),
        tag="public-grid",
    )
    productions_2d = _map(
        ("A", _grid(axes_2d, (2, 2), ("A0", "A1", "A2", "A3"))),
        ("B", _grid(axes_2d, (2, 2), ("B0", "B1", "B2", "B3"))),
        ("C", _grid(axes_2d, (2, 2), ("C0", "C1", "C2", "C3"))),
        ("D", _grid(axes_2d, (2, 2), ("D0", "D1", "D2", "D3"))),
    )
    result_2d = _public_apply_field(
        source_2d,
        rules.mosaic_substitute(
            rules.observation(0),
            rules.literal_expr(productions_2d),
        ),
    )
    assert alphabets.grid_field_parts(result_2d) == (
        axes_2d,
        (4, 4),
        (
            "A0",
            "A1",
            "B0",
            "B1",
            "A2",
            "A3",
            "B2",
            "B3",
            "C0",
            "C1",
            "D0",
            "D1",
            "C2",
            "C3",
            "D2",
            "D3",
        ),
    )

    axes_4d = ("a", "b", "c", "d")
    periodic_source = _grid(
        axes_4d,
        (1, 1, 2, 2),
        ("A", "B", "C", "D"),
    )
    periodic_productions = _map(
        (_context("A", "B"), _grid(axes_4d, (1, 1, 1, 1), ("a",))),
        (_context("B", "A"), _grid(axes_4d, (1, 1, 1, 1), ("b",))),
        (_context("C", "D"), _grid(axes_4d, (1, 1, 1, 1), ("c",))),
        (_context("D", "C"), _grid(axes_4d, (1, 1, 1, 1), ("d",))),
    )
    periodic_result = _public_apply_field(
        periodic_source,
        rules.mosaic_substitute(
            rules.observation(0),
            rules.literal_expr(periodic_productions),
            offsets=((0, 0, 0, 0), (0, 0, 0, 1)),
            boundary=rules.SequenceBoundary.PERIODIC,
        ),
    )
    assert alphabets.grid_field_parts(periodic_result)[2] == (
        "a",
        "b",
        "c",
        "d",
    )

    fixed_source = _grid(
        axes_4d,
        (1, 1, 1, 2),
        ("A", "B"),
    )
    fixed_productions = _map(
        (
            _context("E", "A"),
            _grid(axes_4d, (1, 1, 1, 1), ("left",)),
        ),
        (
            _context("A", "B"),
            _grid(axes_4d, (1, 1, 1, 1), ("right",)),
        ),
    )
    fixed_result = _public_apply_field(
        fixed_source,
        rules.mosaic_substitute(
            rules.observation(0),
            rules.literal_expr(fixed_productions),
            offsets=((0, 0, 0, -1), (0, 0, 0, 0)),
            boundary=rules.SequenceBoundary.FIXED,
            exterior=rules.literal_expr("E"),
        ),
    )
    assert alphabets.grid_field_parts(fixed_result)[2] == (
        "left",
        "right",
    )


def test_reflective_context_does_not_repeat_finite_endpoints() -> None:
    axes = ("x",)
    source = _grid(axes, (3,), ("A", "B", "C"))
    productions = _map(
        (_context("B", "A"), _grid(axes, (1,), ("left",))),
        (_context("A", "B"), _grid(axes, (1,), ("middle",))),
        (_context("B", "C"), _grid(axes, (1,), ("right",))),
    )

    result = _substitute(
        source,
        productions,
        offsets=((-1,), (0,)),
        boundary=rules.SequenceBoundary.REFLECTIVE,
    )

    assert alphabets.grid_field_parts(result)[2] == (
        "left",
        "middle",
        "right",
    )


@pytest.mark.parametrize(
    ("source", "productions", "error"),
    (
        (
            _grid(("x",), (2,), ("A", "B")),
            _map(("A", _grid(("x",), (1,), ("a",)))),
            KeyError,
        ),
        (
            _grid(("x",), (1,), ("A",)),
            alphabets.word_value((), tag="not-a-map"),
            TypeError,
        ),
        (
            _grid(("x",), (1,), ("A",)),
            alphabets.map_value((), tag="empty"),
            ValueError,
        ),
        (
            _grid(("x",), (1,), ("A",)),
            _map(
                (
                    "A",
                    alphabets.field_value(
                        "arbitrary",
                        fields=(("payload", 0),),
                    ),
                )
            ),
            ValueError,
        ),
        (
            _grid(("x",), (1,), ("A",)),
            _map(
                ("A", _grid(("x",), (1,), ("a",))),
                (
                    "unused",
                    alphabets.field_value(
                        "arbitrary",
                        fields=(("payload", 0),),
                    ),
                ),
            ),
            ValueError,
        ),
    ),
)
def test_missing_or_malformed_productions_fail_closed(
    source: alphabets.SemanticValue,
    productions: alphabets.SemanticValue,
    error: type[Exception],
) -> None:
    with pytest.raises(error):
        _substitute(source, productions)


@pytest.mark.parametrize(
    "productions",
    (
        _map(
            ("A", _grid(("x",), (1,), ("a",))),
            ("B", _grid(("other",), (1,), ("b",))),
        ),
        _map(
            ("A", _grid(("x",), (1,), ("a",))),
            ("B", _grid(("x",), (2,), ("b0", "b1"))),
        ),
        _map(
            ("A", _grid(("x",), (1,), ("a",))),
            (
                "B",
                _grid(
                    ("x", "y"),
                    (1, 1),
                    ("b",),
                ),
            ),
        ),
    ),
)
def test_mixed_tile_axes_rank_or_shape_are_rejected(
    productions: alphabets.ValueNode,
) -> None:
    source = _grid(("x",), (2,), ("A", "B"))

    with pytest.raises(ValueError):
        _substitute(source, productions)


@pytest.mark.parametrize(
    "productions",
    (
        _map(
            (
                "not-context",
                _grid(("x",), (1,), ("value",)),
            )
        ),
        _map(
            (
                alphabets.word_value(
                    ("A",),
                    tag="wrong-context-tag",
                ),
                _grid(("x",), (1,), ("value",)),
            )
        ),
        _map(
            (
                _context("A", "B"),
                _grid(("x",), (1,), ("value",)),
            )
        ),
    ),
)
def test_contextual_keys_require_exact_tag_and_offset_arity(
    productions: alphabets.ValueNode,
) -> None:
    source = _grid(("x",), (1,), ("A",))

    with pytest.raises(ValueError):
        _substitute(
            source,
            productions,
            offsets=((0,),),
            boundary=rules.SequenceBoundary.PERIODIC,
        )


@pytest.mark.parametrize(
    ("kwargs", "error"),
    (
        ({"offsets": []}, TypeError),
        ({"offsets": ([0],)}, TypeError),
        ({"offsets": ((),)}, ValueError),
        ({"offsets": ((True,),)}, TypeError),
        ({"offsets": ((0,), (0, 0))}, ValueError),
        (
            {
                "boundary": rules.SequenceBoundary.PERIODIC,
            },
            ValueError,
        ),
        ({"offsets": ((0,),)}, TypeError),
        (
            {
                "offsets": ((0,),),
                "boundary": rules.SequenceBoundary.FIXED,
            },
            ValueError,
        ),
        (
            {
                "offsets": ((0,),),
                "boundary": rules.SequenceBoundary.PERIODIC,
                "exterior": rules.literal_expr("E"),
            },
            ValueError,
        ),
    ),
)
def test_constructor_rejects_invalid_offsets_boundary_or_exterior(
    kwargs: dict[str, object],
    error: type[Exception],
) -> None:
    source = rules.literal_expr(_grid(("x",), (1,), ("A",)))
    productions = rules.literal_expr(
        _map(("A", _grid(("x",), (1,), ("a",))))
    )

    with pytest.raises(error):
        rules.mosaic_substitute(  # type: ignore[arg-type]
            source,
            productions,
            **kwargs,
        )


def test_runtime_rejects_offset_rank_mismatch_and_nonsemantic_exterior() -> None:
    source = _grid(("x", "y"), (1, 1), ("A",))
    productions = _map(
        (
            _context("A"),
            _grid(("x", "y"), (1, 1), ("a",)),
        )
    )

    with pytest.raises(ValueError, match="source rank"):
        _substitute(
            source,
            productions,
            offsets=((0,),),
            boundary=rules.SequenceBoundary.PERIODIC,
        )

    tuple_exterior = rules.RuleExpr(
        rules.ExpressionPrimitive.TUPLE,
        (rules.literal_expr("E"),),
    )
    with pytest.raises(TypeError, match="semantic value"):
        _substitute(
            _grid(("x",), (1,), ("A",)),
            _map(
                (
                    _context("A"),
                    _grid(("x",), (1,), ("a",)),
                )
            ),
            offsets=((0,),),
            boundary=rules.SequenceBoundary.FIXED,
            exterior=tuple_exterior,
        )


def test_direct_ast_rejects_unknown_boundary_and_malformed_offsets() -> None:
    source = rules.literal_expr(_grid(("x",), (1,), ("A",)))
    productions = rules.literal_expr(
        _map(
            (
                _context("A"),
                _grid(("x",), (1,), ("a",)),
            )
        )
    )
    valid = rules.mosaic_substitute(
        source,
        productions,
        offsets=((0,),),
        boundary=rules.SequenceBoundary.PERIODIC,
    )
    offsets = valid.arguments[2]

    with pytest.raises(ValueError, match="not recognized"):
        rules.RuleExpr(
            rules.ExpressionPrimitive.MOSAIC_SUBSTITUTE,
            (source, productions, offsets, "unknown-boundary"),
        )
    malformed_offsets = alphabets.word_value(
        (alphabets.word_value((), tag="mosaic-offset"),),
        tag="mosaic-offsets",
    )
    with pytest.raises(ValueError, match="malformed offset"):
        rules.RuleExpr(
            rules.ExpressionPrimitive.MOSAIC_SUBSTITUTE,
            (
                source,
                productions,
                malformed_offsets,
                rules.SequenceBoundary.PERIODIC.value,
            ),
        )


def test_substitution_is_repeatable_and_never_mutates_inputs() -> None:
    axes = ("row", "column")
    source = _grid(axes, (1, 2), ("A", "B"), tag="immutable")
    productions = _map(
        ("A", _grid(axes, (1, 1), ("a",))),
        ("B", _grid(axes, (1, 1), ("b",))),
    )
    source_identity = source
    production_entries = alphabets.map_entries(productions)
    expression = rules.mosaic_substitute(
        rules.literal_expr(source),
        rules.literal_expr(productions),
    )

    first = _evaluate(expression)
    second = _evaluate(expression)

    assert first == second
    assert source is source_identity
    assert alphabets.grid_field_parts(source) == (
        axes,
        (1, 2),
        ("A", "B"),
    )
    assert alphabets.map_entries(productions) == production_entries
