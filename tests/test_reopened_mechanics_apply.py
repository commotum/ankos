"""Public-boundary regressions for the reopened Goal 7 mechanics."""

from __future__ import annotations

from fractions import Fraction

import ca
import pytest
from ca import (
    alphabets,
    frontiers,
    loci,
    neighborhoods,
    program,
    rules,
    seeds,
    serialization,
)


def _rule_contract(
    source: loci.FiniteConfiguration,
    alphabet: alphabets.Alphabet,
    writable: frontiers.WritableRegion,
    readable: neighborhoods.ReadableRegion,
) -> rules.RuleContract:
    return rules.RuleContract(
        source.contract,
        alphabet.value_profile,
        readable.result_shape,
        readable.join_shape,
        writable.effect_profile,
    )


def _one_locus_expression_program(
    source: loci.FiniteConfiguration,
    alphabet: alphabets.Alphabet,
    expression: rules.RuleExpr,
    *,
    label: str,
) -> ca.SimpleProgram:
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
        contract=_rule_contract(
            source,
            alphabet,
            writable,
            readable,
        ),
        witness=rules.literal_expr(label),
        provenance=(f"test:{label}",),
    )
    return ca.SimpleProgram(
        seed=seeds.exact(
            source,
            value_profile=alphabet.value_profile,
        ),
        alphabet=alphabet,
        frontier=writable,
        neighborhood=readable,
        rule=rule,
    )


def _assert_single_deterministic_successor(
    result: program.ApplicationResult,
    expected: loci.FiniteConfiguration,
) -> loci.FiniteConfiguration:
    assert type(result) is program.ApplicationComplete
    assert (
        result.source_outcomes.support.presentation
        is rules.SupportPresentation.FINITE
    )
    assert len(result.source_outcomes.support.atoms) == 1
    assert type(result.source_outcomes.support.atoms[0]) is rules.Derivation
    assert len(result.applied_atoms.atoms) == 1
    assert type(result.applied_atoms.atoms[0]) is program.AppliedDerivation
    assert result.no_successor_partition.atoms == ()
    assert rules.cardinality_size(result.outcome_atom_cardinality) == 1
    assert rules.cardinality_size(result.derivation_cardinality) == 1
    assert rules.cardinality_size(result.successor_cardinality) == 1

    groups = result.successor_quotient_with_derivation_fibers.atoms
    assert len(groups) == 1
    assert type(groups[0]) is program.SuccessorGroup
    assert len(groups[0].derivations) == 1
    assert type(groups[0].successor) is loci.FiniteConfiguration
    assert loci.configuration_equal(groups[0].successor, expected)
    return groups[0].successor


def test_composite_machine_transition_applies_atomically_and_after_codec_roundtrip() -> None:
    tape = alphabets.word_value((0, 1, 0), tag="tape")
    machine_state = alphabets.record_value(
        (
            ("state", "q0"),
            ("head", 1),
            ("tape", tape),
        ),
        tag="machine",
    )
    source = loci.record_configuration((("machine", machine_state),))
    source_identity = loci.configuration_identity(source)

    symbol_alphabet = alphabets.enum((0, 1))
    machine_alphabet = alphabets.record(
        (
            ("state", alphabets.symbolic(("q0", "q1"))),
            ("head", alphabets.integers(minimum=0, maximum=2)),
            ("tape", alphabets.word(symbol_alphabet)),
        )
    )
    transition = alphabets.record_value(
        (
            ("next_state", "q1"),
            ("write", 0),
            ("move", 1),
        ),
        tag="transition",
    )
    default_transition = alphabets.record_value(
        (
            ("next_state", "q0"),
            ("write", 0),
            ("move", 0),
        ),
        tag="transition",
    )
    transition_table = alphabets.map_value(
        (
            alphabets.map_entry_value(
                alphabets.product_value(
                    ("q0", 1),
                    tag="transition-key",
                ),
                transition,
            ),
        ),
        tag="transitions",
    )

    old_state = rules.observation(0)
    old_head = rules.record_field(old_state, "head")
    old_tape = rules.record_field(old_state, "tape")
    scanned_symbol = rules.item_at(
        old_tape,
        old_head,
        rules.literal_expr(0),
    )
    selected_transition = rules.map_lookup(
        rules.literal_expr(transition_table),
        rules.product_value(
            "transition-key",
            rules.record_field(old_state, "state"),
            scanned_symbol,
        ),
        rules.literal_expr(default_transition),
    )
    written_state = rules.record_update(
        old_state,
        "tape",
        rules.replace_at(
            old_tape,
            old_head,
            rules.record_field(selected_transition, "write"),
        ),
    )
    moved_state = rules.record_update(
        written_state,
        "head",
        rules.add(
            old_head,
            rules.record_field(selected_transition, "move"),
        ),
    )
    next_state = rules.record_update(
        moved_state,
        "state",
        rules.record_field(selected_transition, "next_state"),
    )
    simple_program = _one_locus_expression_program(
        source,
        machine_alphabet,
        next_state,
        label="composite-machine-transition",
    )

    expected = loci.record_configuration(
        (
            (
                "machine",
                alphabets.record_value(
                    (
                        ("state", "q1"),
                        ("head", 2),
                        (
                            "tape",
                            alphabets.word_value(
                                (0, 0, 0),
                                tag="tape",
                            ),
                        ),
                    ),
                    tag="machine",
                ),
            ),
        )
    )

    first = ca.apply(simple_program, source)
    _assert_single_deterministic_successor(first, expected)

    encoded = serialization.dumps(simple_program)
    decoded = serialization.loads(encoded)
    assert type(decoded) is serialization.Decoded
    assert type(decoded.value) is ca.SimpleProgram
    assert serialization.dumps(decoded.value) == encoded
    second = ca.apply(decoded.value, source)
    _assert_single_deterministic_successor(second, expected)

    assert loci.configuration_identity(source) == source_identity
    assert source.entries == ((
        loci.named("machine", scope="record"),
        machine_state,
    ),)


def test_independent_substitution_applies_ordered_variable_length_output() -> None:
    source_word = alphabets.word_value(
        ("A", "B", "A"),
        tag="symbols",
    )
    source = loci.record_configuration((("word", source_word),))
    source_identity = loci.configuration_identity(source)
    alphabet = alphabets.word(alphabets.symbolic(("A", "B")))
    productions = alphabets.map_value(
        (
            alphabets.map_entry_value(
                "A",
                alphabets.word_value(("A", "B"), tag="symbols"),
            ),
            alphabets.map_entry_value(
                "B",
                alphabets.word_value((), tag="symbols"),
            ),
        ),
        tag="productions",
    )
    simple_program = _one_locus_expression_program(
        source,
        alphabet,
        rules.flat_map_lookup(
            rules.observation(0),
            rules.literal_expr(productions),
        ),
        label="ordered-independent-substitution",
    )
    expected = loci.record_configuration(
        (
            (
                "word",
                alphabets.word_value(
                    ("A", "B", "A", "B"),
                    tag="symbols",
                ),
            ),
        )
    )

    result = ca.apply(simple_program, source)
    _assert_single_deterministic_successor(result, expected)

    assert loci.configuration_identity(source) == source_identity
    assert source.entries[0][1] == source_word


def test_rank_four_relative_neighbor_applies_along_axis_four() -> None:
    shape = (1, 1, 1, 2)
    boundary = loci.Boundary(loci.BoundaryPolicy.PERIODIC)
    source = loci.grid_configuration(
        shape,
        (False, True),
        boundary=boundary,
    )
    source_identity = loci.configuration_identity(source)
    alphabet = alphabets.boolean()
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.grid_relative(
        ((0, 0, 0, 1),),
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
        key="axis4-successor",
    )
    rule = rules.expression(
        rules.ExistingPlan(
            rules.ExistingPlanKind.BY_TARGET,
            (rules.project(rules.group(0), 0),),
        ),
        contract=_rule_contract(
            source,
            alphabet,
            writable,
            readable,
        ),
        witness=rules.literal_expr("rank-four-axis4-copy"),
        provenance=("test:rank-four-axis4-copy",),
    )
    simple_program = ca.SimpleProgram(
        seed=seeds.exact(source),
        alphabet=alphabet,
        frontier=writable,
        neighborhood=readable,
        rule=rule,
    )
    expected = loci.grid_configuration(
        shape,
        (True, False),
        boundary=boundary,
    )

    result = ca.apply(simple_program, source)
    successor = _assert_single_deterministic_successor(result, expected)

    assert successor.contract.axes == ("x", "y", "z", "axis4")
    assert loci.configuration_identity(source) == source_identity
    assert tuple(value for _, value in source.entries) == (False, True)


def test_maximal_runs_and_exact_numeric_transduction_apply_together() -> None:
    symbols = alphabets.symbolic(("A", "B"))
    run_alphabet = alphabets.record(
        (
            ("value", symbols),
            ("start", alphabets.integers(minimum=0)),
            ("length", alphabets.integers(minimum=1)),
        )
    )
    state_alphabet = alphabets.record(
        (
            ("input", alphabets.word(symbols)),
            ("runs", alphabets.word(run_alphabet)),
            ("number", alphabets.integers(minimum=0)),
            ("width", alphabets.integers(minimum=1)),
            ("reverse_add", alphabets.integers(minimum=0)),
            ("rational", alphabets.rationals()),
            ("fraction", alphabets.rationals()),
            ("quotient", alphabets.integers()),
        )
    )
    input_word = alphabets.word_value(
        ("A", "A", "B", "B", "B", "A"),
        tag="symbols",
    )
    initial_state = alphabets.record_value(
        (
            ("input", input_word),
            ("runs", alphabets.word_value((), tag="runs")),
            ("number", 16),
            ("width", 5),
            ("reverse_add", 0),
            ("rational", Fraction(-7, 3)),
            ("fraction", Fraction(0)),
            ("quotient", 0),
        ),
        tag="transduction",
    )
    source = loci.record_configuration((("state", initial_state),))
    source_identity = loci.configuration_identity(source)

    old_state = rules.observation(0)
    number = rules.record_field(old_state, "number")
    reversed_number = rules.from_digits(
        rules.reverse(
            rules.integer_digits(
                number,
                2,
                width=rules.record_field(old_state, "width"),
            )
        ),
        2,
    )
    with_runs = rules.record_update(
        old_state,
        "runs",
        rules.maximal_runs(rules.record_field(old_state, "input")),
    )
    with_reverse_add = rules.record_update(
        with_runs,
        "reverse_add",
        rules.add(number, reversed_number),
    )
    with_fraction = rules.record_update(
        with_reverse_add,
        "fraction",
        rules.fractional_part(
            rules.record_field(old_state, "rational")
        ),
    )
    completed_state = rules.record_update(
        with_fraction,
        "quotient",
        rules.floor_divide(
            rules.record_field(old_state, "rational"),
            rules.literal_expr(Fraction(2, 3)),
        ),
    )
    simple_program = _one_locus_expression_program(
        source,
        state_alphabet,
        completed_state,
        label="maximal-runs-numeric-transduction",
    )

    expected_runs = alphabets.word_value(
        (
            alphabets.record_value(
                (
                    ("value", "A"),
                    ("start", 0),
                    ("length", 2),
                ),
                tag="run",
            ),
            alphabets.record_value(
                (
                    ("value", "B"),
                    ("start", 2),
                    ("length", 3),
                ),
                tag="run",
            ),
            alphabets.record_value(
                (
                    ("value", "A"),
                    ("start", 5),
                    ("length", 1),
                ),
                tag="run",
            ),
        ),
        tag="runs",
    )
    expected_state = alphabets.record_value(
        (
            ("input", input_word),
            ("runs", expected_runs),
            ("number", 16),
            ("width", 5),
            ("reverse_add", 17),
            ("rational", Fraction(-7, 3)),
            ("fraction", Fraction(-1, 3)),
            ("quotient", -4),
        ),
        tag="transduction",
    )
    expected = loci.record_configuration((("state", expected_state),))

    result = ca.apply(simple_program, source)
    _assert_single_deterministic_successor(result, expected)

    assert loci.configuration_identity(source) == source_identity
    assert source.entries[0][1] == initial_state


@pytest.mark.parametrize(
    ("expression", "exception_name"),
    (
        (
            rules.divide(
                rules.literal_expr(1),
                rules.literal_expr(0),
            ),
            "ZeroDivisionError",
        ),
        (
            rules.integer_digits(
                rules.literal_expr(4),
                2,
                width=2,
            ),
            "OverflowError",
        ),
    ),
)
def test_arithmetic_evaluation_faults_reject_at_both_public_boundaries(
    expression: rules.RuleExpr,
    exception_name: str,
) -> None:
    source = loci.record_configuration((("value", 1),))
    simple_program = _one_locus_expression_program(
        source,
        alphabets.integers(),
        expression,
        label="arithmetic-fault",
    )

    denotation = simple_program.rule.denote(
        simple_program.neighborhood.resolve(source),
        simple_program.frontier.resolve(source),
    )

    assert isinstance(denotation, rules.RuleRejected)
    assert denotation.fault.phase is rules.RuleFaultPhase.DENOTATION
    assert denotation.fault.reason is rules.RuleFaultReason.EVALUATION_FAILURE
    assert exception_name in denotation.fault.detail

    application = ca.apply(simple_program, source)

    assert isinstance(application, program.ApplicationRejected)
    assert application.fault.phase is program.ApplicationPhase.RULE_DENOTATION
    assert exception_name in application.fault.reason
