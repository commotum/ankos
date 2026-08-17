"""Focused public-boundary tests for the bounded Substitua presets."""

from __future__ import annotations

from fractions import Fraction
from inspect import Parameter, signature

import pytest

import ca
from ca import alphabets, loci, program, rules, seeds, serialization
from ca.catalog import substitua


def _evidence(label: str = "book-source") -> rules.EvidenceTerm:
    return rules.EvidenceTerm(label, ("closed-citation",))


def _grid(
    cells: tuple[alphabets.SemanticValue, ...],
    *,
    shape: tuple[int, int] = (1, 1),
    axes: tuple[str, str] = ("row", "column"),
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


def _initial(simple_program: ca.SimpleProgram) -> loci.FiniteConfiguration:
    assert type(simple_program.seed.source) is seeds.ExactSource
    source = simple_program.seed.source.configuration
    assert type(source) is loci.FiniteConfiguration
    return source


def _roundtrip(value):
    encoded = serialization.dumps(value)
    assert serialization.loads(encoded) == serialization.Decoded(value)
    assert serialization.dumps(value) == encoded
    assert b"catalog:" not in encoded
    assert b"catalog-source-evidence" not in encoded


def _apply_value(
    simple_program: ca.SimpleProgram,
    source: loci.FiniteConfiguration | None = None,
) -> tuple[alphabets.SemanticValue, loci.FiniteConfiguration]:
    if source is None:
        source = _initial(simple_program)
    source_identity = loci.configuration_identity(source)
    result = ca.apply(simple_program, source)

    assert type(result) is program.ApplicationComplete
    _roundtrip(simple_program)
    _roundtrip(result)
    groups = result.successor_quotient_with_derivation_fibers.atoms
    assert len(groups) == 1
    assert type(groups[0]) is program.SuccessorGroup
    successor = groups[0].successor
    assert type(successor) is loci.FiniteConfiguration
    assert len(successor.entries) == 1
    assert loci.configuration_identity(source) == source_identity
    return successor.entries[0][1], successor


def _assert_terminal(
    simple_program: ca.SimpleProgram,
    source: loci.FiniteConfiguration | None = None,
) -> None:
    if source is None:
        source = _initial(simple_program)
    result = ca.apply(simple_program, source)

    assert type(result) is program.ApplicationComplete
    assert result.successor_quotient_with_derivation_fibers.atoms == ()
    assert len(result.no_successor_partition.atoms) == 1
    no_successor = result.no_successor_partition.atoms[0].source
    assert type(no_successor) is rules.NoSuccessor
    assert no_successor.outcome is rules.NoSuccessorOutcome.TERMINAL
    _roundtrip(result)


def _fields(
    value: alphabets.SemanticValue,
) -> dict[str, alphabets.SemanticValue]:
    assert type(value) is alphabets.ValueNode
    assert value.kind is alphabets.ValueKind.RECORD
    return dict(value.fields)


def _independent_tiles() -> alphabets.ValueNode:
    return _map(
        ("A", _grid(("A", "B"), shape=(1, 2), tag="tile")),
        ("B", _grid(("B", "A"), shape=(1, 2), tag="tile")),
    )


def _single_context_tiles() -> alphabets.ValueNode:
    return _map(
        (_context("A", "A", "A", "A"), _grid(("A",), tag="tile")),
    )


def _symbolic_fixture() -> tuple[alphabets.ValueNode, alphabets.ValueNode]:
    x = alphabets.symbolic_value("x")
    expression = alphabets.symbolic_value("add", items=(x, 0))
    rewrites = alphabets.rewrite_rules_value(
        (
            alphabets.rewrite_rule_value(
                alphabets.pattern_node(
                    "add",
                    (
                        alphabets.pattern_bind("value"),
                        alphabets.pattern_literal(0),
                    ),
                ),
                alphabets.template_binding("value"),
            ),
        )
    )
    return expression, rewrites


SIGNATURES = {
    "constant_digit_sequence": (
        "base",
        "prefix",
        "next_digit",
        "source_evidence",
    ),
    "neighbor_dependent_substitution": (
        "symbols",
        "initial",
        "productions",
    ),
    "context_dependent_substitution_2d": (
        "symbols",
        "initial",
        "productions",
    ),
    "tag_system": ("symbols", "initial", "n", "appendants"),
    "cyclic_tag_system": (
        "initial",
        "blocks",
        "initial_phase",
        "trigger",
    ),
    "recursive_sequence": ("prefix", "coefficients", "bias"),
    "variable_index_recursive_sequence": ("prefix", "recurrence"),
    "number_theoretic_filtering": (
        "upper",
        "lower",
        "first_divisor",
    ),
    "neighbor_independent_substitution": (
        "symbols",
        "initial",
        "productions",
    ),
    "creation_destruction_substitution": (
        "symbols",
        "initial",
        "productions",
    ),
    "substitution_system_2d": ("symbols", "initial", "productions"),
    "geometric_substitution": ("seed", "productions"),
    "continued_fraction_substitution": (
        "continued_fraction",
        "source_evidence",
    ),
    "sequential_substitution": ("symbols", "initial", "clauses"),
    "symbolic_system": ("expression", "rewrites", "scan"),
}


@pytest.mark.parametrize(("name", "parameters"), SIGNATURES.items())
def test_preset_signatures_are_explicit_and_keyword_only(
    name: str,
    parameters: tuple[str, ...],
) -> None:
    actual = tuple(signature(getattr(substitua, name)).parameters.values())

    assert name in substitua.__all__
    assert tuple(parameter.name for parameter in actual) == parameters
    assert all(parameter.kind is Parameter.KEYWORD_ONLY for parameter in actual)


def test_constant_digit_and_fixed_recursive_sequences_apply_and_roundtrip() -> None:
    digit_program = substitua.constant_digit_sequence(
        base=10,
        prefix=(1, 2),
        next_digit=rules.modulo(
            rules.add(
                rules.length(rules.observation(0)),
                rules.literal_expr(1),
            ),
            10,
        ),
        source_evidence=_evidence("constant-digits"),
    )
    digit_value, _ = _apply_value(digit_program)
    assert alphabets.word_items(digit_value) == (1, 2, 3)

    recurrence_program = substitua.recursive_sequence(
        prefix=(1, 1),
        coefficients=(1, 1),
    )
    recurrence_value, _ = _apply_value(recurrence_program)
    assert alphabets.word_items(recurrence_value) == (1, 1, 2)

    rational_program = substitua.recursive_sequence(
        prefix=(Fraction(1, 2),),
        coefficients=(Fraction(2),),
    )
    rational_value, _ = _apply_value(rational_program)
    assert alphabets.word_items(rational_value) == (
        Fraction(1, 2),
        Fraction(1),
    )


def test_variable_index_sequence_exposes_prefix_and_one_origin_next_index() -> None:
    state = rules.observation(0)
    recurrence = rules.add(
        rules.length(rules.record_field(state, "prefix")),
        rules.literal_expr(1),
    )
    simple_program = substitua.variable_index_recursive_sequence(
        prefix=(1, 2),
        recurrence=recurrence,
    )

    value, _ = _apply_value(simple_program)
    fields = _fields(value)
    assert fields["next_index"] == 4
    assert alphabets.word_items(fields["prefix"]) == (1, 2, 3)

    zero_program = substitua.variable_index_recursive_sequence(
        prefix=(1,),
        recurrence=rules.literal_expr(0),
    )
    zero_value, _ = _apply_value(zero_program)
    assert alphabets.word_items(_fields(zero_value)["prefix"]) == (1, 0)


def test_word_substitutions_preserve_their_distinguishing_mechanics() -> None:
    neighbor = substitua.neighbor_dependent_substitution(
        symbols=("A", "B"),
        initial=("A", "B", "A"),
        productions=(
            (("A", "A"), ("A",)),
            (("A", "B"), ("B", "B")),
            (("B", "A"), ("A",)),
            (("B", "B"), ("B",)),
        ),
    )
    value, _ = _apply_value(neighbor)
    assert alphabets.word_items(value) == ("B", "B", "A")

    independent = substitua.neighbor_independent_substitution(
        symbols=("A", "B"),
        initial=("A", "B"),
        productions=(("A", ("A", "B")), ("B", ("A",))),
    )
    value, _ = _apply_value(independent)
    assert alphabets.word_items(value) == ("A", "B", "A")

    creation = substitua.creation_destruction_substitution(
        symbols=("A", "B"),
        initial=("A", "B"),
        productions=(("A", ()), ("B", ("B", "A"))),
    )
    value, _ = _apply_value(creation)
    assert alphabets.word_items(value) == ("B", "A")


def test_tag_and_cyclic_tag_systems_delete_and_append_atomically() -> None:
    tag = substitua.tag_system(
        symbols=(0, 1),
        initial=(1, 0),
        n=1,
        appendants=(((0,), (1,)), ((1,), (1, 0))),
    )
    value, _ = _apply_value(tag)
    assert alphabets.word_items(value) == (0, 1, 0)

    cyclic = substitua.cyclic_tag_system(
        initial=(True, False),
        blocks=((True, True), ()),
    )
    value, _ = _apply_value(cyclic)
    fields = _fields(value)
    assert fields["phase"] == 1
    assert alphabets.word_items(fields["word"]) == (False, True, True)


def test_number_filter_advances_through_composite_zero_removal_stages() -> None:
    simple_program = substitua.number_theoretic_filtering(upper=6)

    value, successor = _apply_value(simple_program)
    fields = _fields(value)
    assert fields["divisor"] == 3
    assert alphabets.word_items(fields["candidates"]) == (2, 3, 5)

    value, successor = _apply_value(simple_program, successor)
    fields = _fields(value)
    assert fields["divisor"] == 4
    assert alphabets.word_items(fields["candidates"]) == (2, 3, 5)

    value, _ = _apply_value(simple_program, successor)
    fields = _fields(value)
    assert fields["divisor"] == 5
    assert alphabets.word_items(fields["candidates"]) == (2, 3, 5)


def test_rank_two_independent_contextual_and_geometric_mosaics_apply() -> None:
    source = _grid(("A", "B"), shape=(1, 2), tag="source")
    productions = _independent_tiles()

    substitution = substitua.substitution_system_2d(
        symbols=("A", "B"),
        initial=source,
        productions=productions,
    )
    value, _ = _apply_value(substitution)
    assert alphabets.grid_field_parts(value) == (
        ("row", "column"),
        (1, 4),
        ("A", "B", "B", "A"),
    )

    geometric = substitua.geometric_substitution(
        seed=source,
        productions=productions,
    )
    value, _ = _apply_value(geometric)
    assert alphabets.grid_field_parts(value) == (
        ("row", "column"),
        (1, 4),
        ("A", "B", "B", "A"),
    )
    assert geometric == substitution
    assert serialization.dumps(geometric) == serialization.dumps(
        substitution
    )

    contextual = substitua.context_dependent_substitution_2d(
        symbols=("A",),
        initial=_grid(("A",), tag="context-source"),
        productions=_single_context_tiles(),
    )
    value, _ = _apply_value(contextual)
    assert alphabets.grid_field_parts(value) == (
        ("row", "column"),
        (1, 1),
        ("A",),
    )


def test_continued_fraction_uses_visible_reverse_tail_schedule() -> None:
    simple_program = substitua.continued_fraction_substitution(
        continued_fraction=(3, 2, 1),
        source_evidence=_evidence("continued-fraction"),
    )

    value, successor = _apply_value(simple_program)
    fields = _fields(value)
    assert fields["cursor"] == 1
    assert alphabets.word_items(fields["schedule"]) == (1, 2)
    assert alphabets.word_items(fields["word"]) == (1,)

    value, successor = _apply_value(simple_program, successor)
    fields = _fields(value)
    assert fields["cursor"] == 2
    assert alphabets.word_items(fields["word"]) == (0, 1, 0)
    _assert_terminal(simple_program, successor)


def test_sequential_and_symbolic_rewrites_apply_one_selected_match() -> None:
    sequential = substitua.sequential_substitution(
        symbols=("A", "B", "X"),
        initial=("A", "B", "A", "B", "A"),
        clauses=(
            (("B", "A"), ("X",)),
            (("A", "B"), ("B", "B")),
        ),
    )
    value, _ = _apply_value(sequential)
    assert alphabets.word_items(value) == ("A", "X", "B", "A")

    expression, rewrites = _symbolic_fixture()
    symbolic = substitua.symbolic_system(
        expression=expression,
        rewrites=rewrites,
    )
    value, _ = _apply_value(symbolic)
    assert value == alphabets.symbolic_value("x")


def test_terminal_presets_return_typed_no_successor_outcomes() -> None:
    programs = (
        substitua.neighbor_dependent_substitution(
            symbols=("A",),
            initial=("A",),
            productions=((("A", "A"), ("A",)),),
        ),
        substitua.tag_system(
            symbols=(0,),
            initial=(0,),
            n=2,
            appendants=(((0, 0), (0,)),),
        ),
        substitua.cyclic_tag_system(initial=(), blocks=((True,),)),
        substitua.continued_fraction_substitution(
            continued_fraction=(3,),
            source_evidence=_evidence(),
        ),
        substitua.sequential_substitution(
            symbols=("A", "B"),
            initial=("A",),
            clauses=((("B",), ("A",)),),
        ),
    )

    for simple_program in programs:
        _assert_terminal(simple_program)


def test_closed_rule_expressions_are_range_checked_before_commit() -> None:
    scalar_rewrite = alphabets.rewrite_rules_value(
        (
            alphabets.rewrite_rule_value(
                alphabets.pattern_node("root", ()),
                alphabets.template_literal(0),
            ),
        )
    )
    programs = (
        substitua.constant_digit_sequence(
            base=2,
            prefix=(0,),
            next_digit=rules.literal_expr(2),
            source_evidence=_evidence("out-of-range-digit"),
        ),
        substitua.variable_index_recursive_sequence(
            prefix=(1,),
            recurrence=rules.literal_expr(-1),
        ),
        substitua.symbolic_system(
            expression=alphabets.symbolic_value("root"),
            rewrites=scalar_rewrite,
        ),
    )

    for simple_program in programs:
        source = _initial(simple_program)
        source_identity = loci.configuration_identity(source)

        rejected = ca.apply(simple_program, source)

        assert type(rejected) is program.ApplicationRejected
        assert (
            rejected.fault.phase
            is program.ApplicationPhase.RESULT_VALIDATION
        )
        assert loci.configuration_identity(source) == source_identity
        assert not hasattr(rejected, "applied_atoms")
        assert not hasattr(
            rejected,
            "successor_quotient_with_derivation_fibers",
        )
        _roundtrip(simple_program)
        _roundtrip(rejected)


@pytest.mark.parametrize(
    ("call", "match"),
    (
        (
            lambda: substitua.constant_digit_sequence(
                base=True,
                prefix=(0,),
                next_digit=rules.literal_expr(0),
                source_evidence=_evidence(),
            ),
            "base",
        ),
        (
            lambda: substitua.neighbor_dependent_substitution(
                symbols=("A", "B"),
                initial=("A", "B"),
                productions=((("A", "A"), ("A",)),),
            ),
            "cover",
        ),
        (
            lambda: substitua.context_dependent_substitution_2d(
                symbols=("A",),
                initial=alphabets.grid_field_value(
                    ("x",),
                    (1,),
                    ("A",),
                ),
                productions=_single_context_tiles(),
            ),
            "rank-2",
        ),
        (
            lambda: substitua.tag_system(
                symbols=(0, 1),
                initial=(0,),
                n=1,
                appendants=(((0,), (0,)),),
            ),
            "cover",
        ),
        (
            lambda: substitua.cyclic_tag_system(
                initial=(True,),
                blocks=((True,),),
                initial_phase=1,
            ),
            "initial_phase",
        ),
        (
            lambda: substitua.recursive_sequence(
                prefix=(1,),
                coefficients=(Fraction(1),),
            ),
            "match",
        ),
        (
            lambda: substitua.recursive_sequence(
                prefix=(Fraction(1),),
                coefficients=(Fraction(1),),
                bias=0,
            ),
            "bias",
        ),
        (
            lambda: substitua.variable_index_recursive_sequence(
                prefix=(True,),
                recurrence=rules.literal_expr(1),
            ),
            "positive-int",
        ),
        (
            lambda: substitua.number_theoretic_filtering(
                upper=5,
                first_divisor=6,
            ),
            "first_divisor",
        ),
        (
            lambda: substitua.neighbor_independent_substitution(
                symbols=("A",),
                initial=("A",),
                productions=(("A", ()),),
            ),
            "cannot be empty",
        ),
        (
            lambda: substitua.creation_destruction_substitution(
                symbols=("A", "B"),
                initial=("A",),
                productions=(("A", ("A",)), ("B", ("A", "B"))),
            ),
            "empty production",
        ),
        (
            lambda: substitua.substitution_system_2d(
                symbols=("A", "B"),
                initial=_grid(("A", "B"), shape=(1, 2)),
                productions=_map(
                    ("A", _grid(("A",), axes=("row", "other"))),
                    ("B", _grid(("B",), axes=("row", "other"))),
                ),
            ),
            "axes",
        ),
        (
            lambda: substitua.geometric_substitution(
                seed=_grid(("A",)),
                productions=_map(("B", _grid(("B",)))),
            ),
            "production keys",
        ),
        (
            lambda: substitua.continued_fraction_substitution(
                continued_fraction=(2, 0),
                source_evidence=_evidence(),
            ),
            "positive",
        ),
        (
            lambda: substitua.sequential_substitution(
                symbols=("A",),
                initial=("A",),
                clauses=(((), ("A",)),),
            ),
            "cannot be empty",
        ),
        (
            lambda: substitua.symbolic_system(
                expression=alphabets.symbolic_value("x"),
                rewrites=alphabets.word_value(("opaque",), tag="rewrite-rules"),
            ),
            "rewrite",
        ),
    ),
)
def test_hostile_preset_inputs_fail_closed(call, match: str) -> None:
    with pytest.raises((TypeError, ValueError), match=match):
        call()
