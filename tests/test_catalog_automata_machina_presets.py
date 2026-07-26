from __future__ import annotations

from fractions import Fraction
from inspect import Parameter, signature
from itertools import product as cartesian_product

import pytest

from ca import alphabets, loci, program, rules, serialization
from ca.catalog import automata, machina


AUTOMATA_PRESETS = (
    automata.multicolor_cellular_automaton,
    automata.totalistic_cellular_automaton,
    automata.three_color_totalistic_cellular_automaton,
    automata.higher_color_totalistic_cellular_automaton,
    automata.quiescent_cellular_automaton,
    automata.symmetric_cellular_automaton,
    automata.generalized_mobile_automaton,
    automata.cellular_automaton_2d,
    automata.moore_cellular_automaton,
    automata.cellular_automaton_3d,
    automata.lattice_cellular_automaton,
    automata.arithmetic_iteration,
    automata.piecewise_integer_map,
    automata.digit_reversal_map,
    automata.continuous_cellular_automaton,
)

MACHINA_PRESETS = (
    machina.mobile_automaton,
    machina.neighbor_updating_mobile_automaton,
    machina.turing_machine,
    machina.turing_machine_2d,
    machina.extended_mobile_automaton,
)


def _source(simple: program.SimpleProgram) -> loci.FiniteConfiguration:
    source = simple.seed.source
    assert hasattr(source, "configuration")
    configuration = source.configuration
    assert type(configuration) is loci.FiniteConfiguration
    return configuration


def _successor(simple: program.SimpleProgram) -> loci.FiniteConfiguration:
    result = program.apply(simple, _source(simple))
    assert isinstance(result, program.ApplicationComplete), result
    groups = result.successor_quotient_with_derivation_fibers.atoms
    assert len(groups) == 1
    successor = groups[0].successor
    assert type(successor) is loci.FiniteConfiguration
    return successor


def _values(configuration: loci.FiniteConfiguration) -> tuple:
    return tuple(value for _, value in configuration.entries)


def _identity_table(
    colors: int,
    width: int,
    center: int,
) -> tuple[int, ...]:
    return tuple(
        values[center]
        for values in cartesian_product(range(colors), repeat=width)
    )


def _mobile_transitions(
    colors: int,
) -> tuple[tuple[tuple[int, int, int], tuple[int, int]], ...]:
    return tuple(
        (key, (key[1], 1))
        for key in cartesian_product(range(colors), repeat=3)
    )


def _neighbor_mobile_transitions(
    colors: int,
) -> tuple[
    tuple[
        tuple[int, int, int],
        tuple[tuple[int, int, int], int],
    ],
    ...,
]:
    return tuple(
        (key, (key, 1))
        for key in cartesian_product(range(colors), repeat=3)
    )


def _generalized_transitions(
    colors: int,
) -> tuple[
    tuple[
        tuple[int, int, int],
        tuple[int, tuple[int, ...]],
    ],
    ...,
]:
    return tuple(
        (key, (key[1], (1,)))
        for key in cartesian_product(range(colors), repeat=3)
    )


@pytest.mark.parametrize("constructor", AUTOMATA_PRESETS + MACHINA_PRESETS)
def test_preset_signatures_are_explicit_and_keyword_only(constructor) -> None:
    parameters = tuple(signature(constructor).parameters.values())

    assert parameters
    assert all(item.kind is Parameter.KEYWORD_ONLY for item in parameters)
    assert all(
        item.kind not in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD)
        for item in parameters
    )


def test_piecewise_fallback_is_explicitly_required() -> None:
    assert signature(automata.piecewise_integer_map).parameters[
        "otherwise"
    ].default is Parameter.empty


def test_finite_rank_one_table_presets_apply_in_declared_order() -> None:
    initial = (0, 1, 2, 1, 0)
    identity = _identity_table(3, 3, 1)
    multicolor = automata.multicolor_cellular_automaton(
        initial=initial,
        colors=3,
        rule=identity,
    )
    quiescent = automata.quiescent_cellular_automaton(
        initial=initial,
        colors=3,
        rule=identity,
        background=0,
    )
    symmetric = automata.symmetric_cellular_automaton(
        initial=initial,
        colors=3,
        rule=identity,
    )

    for simple in (multicolor, quiescent, symmetric):
        assert _values(_successor(simple)) == initial


def test_totalistic_specializations_apply_exact_sum_tables() -> None:
    binary = automata.totalistic_cellular_automaton(
        initial=(0, 1, 0, 1, 0),
        colors=2,
        rule=(0, 1, 0, 1),
    )
    three = automata.three_color_totalistic_cellular_automaton(
        initial=(0, 1, 2, 1, 0),
        rule=tuple(index % 3 for index in range(7)),
    )
    higher = automata.higher_color_totalistic_cellular_automaton(
        initial=(0, 1, 3, 1, 0),
        colors=4,
        rule=tuple(index % 4 for index in range(10)),
    )

    for simple in (binary, three, higher):
        assert isinstance(_successor(simple), loci.FiniteConfiguration)


def test_ranked_grid_presets_apply_identity_tables() -> None:
    ca_2d = automata.cellular_automaton_2d(
        shape=(2, 2),
        initial=(0, 1, 1, 0),
        colors=2,
        rule=_identity_table(2, 5, 2),
    )
    moore = automata.moore_cellular_automaton(
        shape=(2, 2),
        initial=(0, 1, 1, 0),
        colors=2,
        rule=_identity_table(2, 9, 4),
    )
    ca_3d = automata.cellular_automaton_3d(
        shape=(2, 1, 1),
        initial=(0, 1),
        colors=2,
        offsets=((0, 0, 0),),
        rule=(0, 1),
    )
    lattice = automata.lattice_cellular_automaton(
        shape=(1, 1, 1, 2),
        initial=(0, 1),
        colors=2,
        offsets=((0, 0, 0, 0),),
        rule=(0, 1),
        axes=("a", "b", "c", "d"),
    )

    assert _values(_successor(ca_2d)) == (0, 1, 1, 0)
    assert _values(_successor(moore)) == (0, 1, 1, 0)
    assert _values(_successor(ca_3d)) == (0, 1)
    assert _values(_successor(lattice)) == (0, 1)


def test_iterated_numeric_presets_apply_closed_rule_expressions() -> None:
    arithmetic = automata.arithmetic_iteration(
        initial=4,
        alphabet=alphabets.integers(),
        map_expression=rules.add(
            rules.observation(0),
            rules.literal_expr(3),
        ),
    )
    piecewise = automata.piecewise_integer_map(
        initial=4,
        cases=(
                (
                    2,
                    0,
                    rules.subtract(
                        rules.observation(0),
                        rules.literal_expr(2),
                    ),
            ),
        ),
        otherwise=rules.add(
            rules.observation(0),
            rules.literal_expr(1),
        ),
    )
    reverse_add = automata.digit_reversal_map(initial=6, base=2)

    assert _values(_successor(arithmetic)) == (7,)
    assert _values(_successor(piecewise)) == (2,)
    assert _values(_successor(reverse_add)) == (9,)


def test_continuous_cellular_automaton_uses_exact_rational_values() -> None:
    initial = (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4))
    simple = automata.continuous_cellular_automaton(
        initial=initial,
        local_rule=rules.project(rules.group(0), 1),
    )

    assert _values(_successor(simple)) == initial


def test_generalized_mobile_automaton_moves_tagged_active_locus() -> None:
    simple = automata.generalized_mobile_automaton(
        initial=(0, 0, 1, 0, 0),
        active=(2,),
        colors=2,
        transitions=_generalized_transitions(2),
        boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
    )

    assert _values(_successor(simple)) == (
        alphabets.tag_value("cell", 0),
        alphabets.tag_value("cell", 0),
        alphabets.tag_value("cell", 1),
        alphabets.tag_value("active", 0),
        alphabets.tag_value("cell", 0),
    )


def test_mobile_presets_apply_atomic_source_and_destination_writes() -> None:
    mobile = machina.mobile_automaton(
        initial=(0, 0, 1, 0, 0),
        head=2,
        colors=2,
        transitions=_mobile_transitions(2),
        boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
    )
    neighbor = machina.neighbor_updating_mobile_automaton(
        initial=(0, 0, 1, 0, 0),
        head=2,
        colors=2,
        transitions=_neighbor_mobile_transitions(2),
        boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
    )

    expected = (
        alphabets.tag_value("cell", 0),
        alphabets.tag_value("cell", 0),
        alphabets.tag_value("cell", 1),
        alphabets.tag_value("head", 0),
        alphabets.tag_value("cell", 0),
    )
    assert _values(_successor(mobile)) == expected
    assert _values(_successor(neighbor)) == expected


def test_extended_mobile_adapter_warns_and_delegates_losslessly() -> None:
    arguments = dict(
        initial=(0, 0, 1, 0, 0),
        head=2,
        colors=2,
        transitions=_neighbor_mobile_transitions(2),
        boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
    )

    with pytest.warns(DeprecationWarning, match="neighbor_updating"):
        legacy = machina.extended_mobile_automaton(**arguments)

    assert legacy == machina.neighbor_updating_mobile_automaton(**arguments)


def test_turing_presets_apply_tagged_control_transitions() -> None:
    one_dimensional = machina.turing_machine(
        tape=(0, 0, 0, 0, 0),
        head=2,
        initial_state="q0",
        states=("q0", "q1"),
        symbols=2,
        transitions=((("q0", 0), ("q1", 1, 1)),),
        boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
    )
    two_dimensional = machina.turing_machine_2d(
        shape=(3, 3),
        tape=(0,) * 9,
        head=(1, 1),
        initial_state="q0",
        states=("q0", "q1"),
        symbols=2,
        transitions=((("q0", 0), ("q1", 1, (0, 1))),),
        boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
    )

    one_values = _values(_successor(one_dimensional))
    assert one_values[2] == alphabets.tag_value("cell", 1)
    assert one_values[3] == alphabets.tag_value("head:q1", 0)
    two_values = _values(_successor(two_dimensional))
    assert two_values[4] == alphabets.tag_value("cell", 1)
    assert two_values[5] == alphabets.tag_value("head:q1", 0)


def test_missing_turing_transition_is_an_explicit_terminal_continuation() -> None:
    simple = machina.turing_machine(
        tape=(0, 0, 1, 0, 0),
        head=2,
        initial_state="q0",
        states=("q0",),
        symbols=2,
        transitions=((("q0", 0), ("q0", 1, 1)),),
        boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
    )

    result = program.apply(simple, _source(simple))

    assert isinstance(result, program.ApplicationComplete)
    atom = result.source_outcomes.support.atoms[0]
    assert isinstance(atom, rules.Derivation)
    assert isinstance(atom.continuation, rules.Stop)
    assert atom.progress is rules.Progress.QUIESCENT
    assert loci.configuration_equal(_successor(simple), _source(simple))


def _all_program_samples() -> tuple[program.SimpleProgram, ...]:
    identity_3 = _identity_table(3, 3, 1)
    return (
        automata.multicolor_cellular_automaton(
            initial=(0, 1, 0),
            colors=2,
            rule=_identity_table(2, 3, 1),
        ),
        automata.totalistic_cellular_automaton(
            initial=(0, 1, 0),
            colors=2,
            rule=(0, 1, 0, 1),
        ),
        automata.three_color_totalistic_cellular_automaton(
            initial=(0, 1, 0),
            rule=tuple(index % 3 for index in range(7)),
        ),
        automata.higher_color_totalistic_cellular_automaton(
            initial=(0, 1, 0),
            colors=4,
            rule=tuple(index % 4 for index in range(10)),
        ),
        automata.quiescent_cellular_automaton(
            initial=(0, 1, 0),
            colors=3,
            rule=identity_3,
        ),
        automata.symmetric_cellular_automaton(
            initial=(0, 1, 0),
            colors=3,
            rule=identity_3,
        ),
        automata.generalized_mobile_automaton(
            initial=(0, 1, 0),
            active=(1,),
            colors=2,
            transitions=_generalized_transitions(2),
            boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
        ),
        automata.cellular_automaton_2d(
            shape=(1, 1),
            initial=(1,),
            colors=2,
            rule=_identity_table(2, 5, 2),
        ),
        automata.moore_cellular_automaton(
            shape=(1, 1),
            initial=(1,),
            colors=2,
            rule=_identity_table(2, 9, 4),
        ),
        automata.cellular_automaton_3d(
            shape=(1, 1, 1),
            initial=(1,),
            colors=2,
            offsets=((0, 0, 0),),
            rule=(0, 1),
        ),
        automata.lattice_cellular_automaton(
            shape=(1, 1, 1, 1),
            initial=(1,),
            colors=2,
            offsets=((0, 0, 0, 0),),
            rule=(0, 1),
        ),
        automata.arithmetic_iteration(
            initial=1,
            alphabet=alphabets.integers(),
            map_expression=rules.add(
                rules.observation(0),
                rules.literal_expr(1),
            ),
        ),
        automata.piecewise_integer_map(
            initial=2,
            cases=((2, 0, rules.literal_expr(1)),),
            otherwise=rules.literal_expr(0),
        ),
        automata.digit_reversal_map(initial=6),
        automata.continuous_cellular_automaton(
            initial=(Fraction(1, 2),),
            local_rule=rules.project(rules.group(0), 1),
        ),
        machina.mobile_automaton(
            initial=(0, 1, 0),
            head=1,
            colors=2,
            transitions=_mobile_transitions(2),
            boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
        ),
        machina.neighbor_updating_mobile_automaton(
            initial=(0, 1, 0),
            head=1,
            colors=2,
            transitions=_neighbor_mobile_transitions(2),
            boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
        ),
        machina.turing_machine(
            tape=(0, 0, 0),
            head=1,
            initial_state="q0",
            states=("q0",),
            symbols=2,
            transitions=((("q0", 0), ("q0", 1, 1)),),
            boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
        ),
        machina.turing_machine_2d(
            shape=(3, 3),
            tape=(0,) * 9,
            head=(1, 1),
            initial_state="q0",
            states=("q0",),
            symbols=2,
            transitions=((("q0", 0), ("q0", 1, (0, 1))),),
            boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
        ),
    )


def test_all_new_presets_round_trip_through_the_closed_codec() -> None:
    for simple in _all_program_samples():
        assert serialization.loads(serialization.dumps(simple)) == (
            serialization.Decoded(simple)
        )


@pytest.mark.parametrize(
    ("constructor", "match"),
    (
        (
            lambda: automata.multicolor_cellular_automaton(
                initial=(0,),
                colors=True,
                rule=(0,),
            ),
            "integer",
        ),
        (
            lambda: automata.multicolor_cellular_automaton(
                initial=(0,),
                colors=2,
                rule=(0, 1),
            ),
            "exactly 8",
        ),
        (
            lambda: automata.quiescent_cellular_automaton(
                initial=(0,),
                colors=2,
                rule=(1,) + (0,) * 7,
            ),
            "uniform background",
        ),
        (
            lambda: automata.symmetric_cellular_automaton(
                initial=(0,),
                colors=2,
                rule=(0, 1, 0, 0, 0, 0, 0, 0),
            ),
            "reflection symmetric",
        ),
        (
            lambda: automata.generalized_mobile_automaton(
                initial=(0, 0, 0),
                active=(1,),
                colors=2,
                transitions=(),
            ),
            "total",
        ),
        (
            lambda: automata.cellular_automaton_2d(
                shape=(2, 2),
                initial=(0,),
                colors=2,
                rule=(0,) * 32,
            ),
            "exactly 4",
        ),
        (
            lambda: automata.piecewise_integer_map(
                initial=1,
                cases=((0, 0, rules.literal_expr(1)),),
                otherwise=rules.literal_expr(0),
            ),
            "positive",
        ),
        (
            lambda: automata.continuous_cellular_automaton(
                initial=(0.5,),
                local_rule=rules.literal_expr(Fraction(1, 2)),
            ),
            "Fractions",
        ),
        (
            lambda: machina.mobile_automaton(
                initial=(0, 0, 0),
                head=1,
                colors=2,
                transitions=(),
            ),
            "total",
        ),
        (
            lambda: machina.turing_machine(
                tape=(0, 0, 0),
                head=1,
                initial_state="q1",
                states=("q0",),
                symbols=2,
                transitions=(),
            ),
            "declared",
        ),
        (
            lambda: machina.turing_machine_2d(
                shape=(3, 3),
                tape=(0,) * 9,
                head=(1, 1),
                initial_state="q0",
                states=("q0",),
                symbols=2,
                transitions=((("q0", 0), ("q0", 0, (1, 1))),),
            ),
            "cardinal",
        ),
    ),
)
def test_presets_reject_malformed_or_semantically_open_inputs(
    constructor,
    match: str,
) -> None:
    with pytest.raises((TypeError, ValueError), match=match):
        constructor()
