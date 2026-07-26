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


def _assert_terminal(
    simple: program.SimpleProgram,
    source: loci.FiniteConfiguration | None = None,
    *,
    reason: str = "no-applicable-transition",
) -> program.ApplicationComplete:
    result = program.apply(simple, _source(simple) if source is None else source)
    assert isinstance(result, program.ApplicationComplete)
    assert result.successor_quotient_with_derivation_fibers.atoms == ()
    assert len(result.no_successor_partition.atoms) == 1
    terminal = result.no_successor_partition.atoms[0].source
    assert terminal.outcome is rules.NoSuccessorOutcome.TERMINAL
    assert terminal.reason == rules.literal_expr(reason)
    assert terminal.provenance == (f"mechanics:{reason}",)
    return result


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
    movement: int = 1,
) -> tuple[tuple[tuple[int, int, int], tuple[int, int]], ...]:
    return tuple(
        (key, (key[1], movement))
        for key in cartesian_product(range(colors), repeat=3)
    )


def _neighbor_mobile_transitions(
    colors: int,
    movement: int = 1,
) -> tuple[
    tuple[
        tuple[int, int, int],
        tuple[tuple[int, int, int], int],
    ],
    ...,
]:
    return tuple(
        (key, (key, movement))
        for key in cartesian_product(range(colors), repeat=3)
    )


def _generalized_transitions(
    colors: int,
    movement: int = 1,
) -> tuple[
    tuple[
        tuple[int, int, int],
        tuple[int, tuple[int, ...]],
    ],
    ...,
]:
    return tuple(
        (key, (key[1], (movement,)))
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


def test_periodic_movement_presets_normalize_edge_destinations() -> None:
    generalized = automata.generalized_mobile_automaton(
        initial=(1, 0, 0),
        active=(0,),
        colors=2,
        transitions=_generalized_transitions(2, -1),
    )
    mobile = machina.mobile_automaton(
        initial=(1, 0, 0),
        head=0,
        colors=2,
        transitions=_mobile_transitions(2, -1),
    )
    neighbor = machina.neighbor_updating_mobile_automaton(
        initial=(1, 0, 0),
        head=0,
        colors=2,
        transitions=_neighbor_mobile_transitions(2, -1),
    )
    legacy_arguments = dict(
        initial=(1, 0, 0),
        head=0,
        colors=2,
        transitions=_neighbor_mobile_transitions(2, -1),
    )
    with pytest.warns(DeprecationWarning):
        legacy = machina.extended_mobile_automaton(**legacy_arguments)

    assert _values(_successor(generalized))[-1] == alphabets.tag_value(
        "active",
        0,
    )
    for simple in (mobile, neighbor, legacy):
        assert _values(_successor(simple))[-1] == alphabets.tag_value(
            "head",
            0,
        )


def test_generalized_mobile_zero_active_state_is_explicitly_terminal() -> None:
    initially_empty = automata.generalized_mobile_automaton(
        initial=(0, 0, 0),
        active=(),
        colors=2,
        transitions=_generalized_transitions(2),
    )
    deletes_active = automata.generalized_mobile_automaton(
        initial=(0, 0, 0),
        active=(1,),
        colors=2,
        transitions=tuple(
            (key, (key[1], ()))
            for key in cartesian_product(range(2), repeat=3)
        ),
    )

    _assert_terminal(initially_empty, reason="no-active-loci")
    successor = _successor(deletes_active)
    assert all(
        value.tag == "cell"
        for value in _values(successor)
        if isinstance(value, alphabets.ValueNode)
    )
    _assert_terminal(
        deletes_active,
        successor,
        reason="no-active-loci",
    )


@pytest.mark.parametrize(
    "constructor",
    (
        lambda boundary: automata.generalized_mobile_automaton(
            initial=(0, 0, 0),
            active=(0,),
            colors=2,
            transitions=_generalized_transitions(2, -1),
            boundary=boundary,
        ),
        lambda boundary: machina.mobile_automaton(
            initial=(0, 0, 0),
            head=0,
            colors=2,
            transitions=_mobile_transitions(2, -1),
            boundary=boundary,
        ),
        lambda boundary: machina.neighbor_updating_mobile_automaton(
            initial=(0, 0, 0),
            head=0,
            colors=2,
            transitions=_neighbor_mobile_transitions(2, -1),
            boundary=boundary,
        ),
    ),
)
@pytest.mark.parametrize(
    "boundary",
    (
        loci.Boundary(loci.BoundaryPolicy.FIXED, 0),
        loci.Boundary(loci.BoundaryPolicy.NONE),
        loci.Boundary(loci.BoundaryPolicy.REFLECTIVE),
    ),
)
def test_anchored_movement_presets_reject_nonperiodic_carriers(
    constructor,
    boundary: loci.Boundary,
) -> None:
    with pytest.raises(ValueError, match="periodic boundary"):
        constructor(boundary)


def test_extended_mobile_rejects_nonperiodic_carrier_after_warning() -> None:
    with pytest.warns(DeprecationWarning):
        with pytest.raises(ValueError, match="periodic boundary"):
            machina.extended_mobile_automaton(
                initial=(0, 0, 0),
                head=0,
                colors=2,
                transitions=_neighbor_mobile_transitions(2, -1),
                boundary=loci.Boundary(loci.BoundaryPolicy.REFLECTIVE),
            )


def test_turing_edges_are_rule_owned_under_finite_and_wrapping_boundaries() -> None:
    terminal_1d = machina.turing_machine(
        tape=(0, 0, 0),
        head=0,
        initial_state="q0",
        states=("q0",),
        symbols=2,
        transitions=((("q0", 0), ("q0", 1, -1)),),
    )
    terminal_2d = machina.turing_machine_2d(
        shape=(2, 2),
        tape=(0,) * 4,
        head=(0, 0),
        initial_state="q0",
        states=("q0",),
        symbols=2,
        transitions=((("q0", 0), ("q0", 1, (-1, 0))),),
    )
    periodic_1d = machina.turing_machine(
        tape=(0, 0, 0),
        head=0,
        initial_state="q0",
        states=("q0", "q1"),
        symbols=2,
        transitions=((("q0", 0), ("q1", 1, -1)),),
        boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
    )
    periodic_2d = machina.turing_machine_2d(
        shape=(3, 3),
        tape=(0,) * 9,
        head=(0, 0),
        initial_state="q0",
        states=("q0", "q1"),
        symbols=2,
        transitions=((("q0", 0), ("q1", 1, (0, -1))),),
        boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
    )

    _assert_terminal(terminal_1d)
    _assert_terminal(terminal_2d)
    assert _values(_successor(periodic_1d))[-1] == alphabets.tag_value(
        "head:q1",
        0,
    )
    assert _values(_successor(periodic_2d))[2] == alphabets.tag_value(
        "head:q1",
        0,
    )


def test_turing_reflective_aliases_commit_one_normalized_destination() -> None:
    reflected_1d = machina.turing_machine(
        tape=(0, 0, 0),
        head=0,
        initial_state="q0",
        states=("q0", "q1"),
        symbols=2,
        transitions=((("q0", 0), ("q1", 1, -1)),),
        boundary=loci.Boundary(loci.BoundaryPolicy.REFLECTIVE),
    )
    aliased_2d = machina.turing_machine_2d(
        shape=(1, 1),
        tape=(0,),
        head=(0, 0),
        initial_state="q0",
        states=("q0", "q1"),
        symbols=2,
        transitions=((("q0", 0), ("q1", 1, (0, 1))),),
        boundary=loci.Boundary(loci.BoundaryPolicy.REFLECTIVE),
    )

    assert _values(_successor(reflected_1d))[1] == alphabets.tag_value(
        "head:q1",
        0,
    )
    assert _values(_successor(aliased_2d)) == (
        alphabets.tag_value("head:q1", 1),
    )


def test_one_cell_turing_carriers_preserve_global_boundary_semantics() -> None:
    arguments = dict(
        tape=(0,),
        head=0,
        initial_state="q0",
        states=("q0", "q1"),
        symbols=1,
        transitions=((("q0", 0), ("q1", 0, 1)),),
    )
    periodic = machina.turing_machine(
        **arguments,
        boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
    )
    reflective = machina.turing_machine(
        **arguments,
        boundary=loci.Boundary(loci.BoundaryPolicy.REFLECTIVE),
    )
    finite = machina.turing_machine(**arguments)

    expected = (alphabets.tag_value("head:q1", 0),)
    assert _values(_successor(periodic)) == expected
    assert _values(_successor(reflective)) == expected
    _assert_terminal(finite)

    with pytest.raises(ValueError, match="cannot be empty"):
        machina.turing_machine(
            tape=(),
            head=0,
            initial_state="q0",
            states=("q0",),
            symbols=1,
            transitions=(),
        )


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

    canonical = machina.neighbor_updating_mobile_automaton(**arguments)
    assert legacy == canonical
    assert serialization.dumps(legacy) == serialization.dumps(canonical)


def test_equivalent_rank_one_preset_paths_have_no_invocation_identity() -> None:
    initial = (0, 1, 2, 1, 0)
    identity = _identity_table(3, 3, 1)
    programs = (
        automata.multicolor_cellular_automaton(
            initial=initial,
            colors=3,
            rule=identity,
        ),
        automata.quiescent_cellular_automaton(
            initial=initial,
            colors=3,
            rule=identity,
            background=0,
        ),
        automata.quiescent_cellular_automaton(
            initial=initial,
            colors=3,
            rule=identity,
            background=1,
        ),
        automata.symmetric_cellular_automaton(
            initial=initial,
            colors=3,
            rule=identity,
        ),
    )

    assert all(simple == programs[0] for simple in programs[1:])
    encoded = serialization.dumps(programs[0])
    assert all(serialization.dumps(simple) == encoded for simple in programs[1:])


def test_totalistic_specializations_are_exact_expansion_paths() -> None:
    three_arguments = dict(
        initial=(0, 1, 2, 1, 0),
        rule=tuple(index % 3 for index in range(7)),
    )
    four_arguments = dict(
        initial=(0, 1, 3, 1, 0),
        rule=tuple(index % 4 for index in range(10)),
    )
    three_general = automata.totalistic_cellular_automaton(
        colors=3,
        radius=1,
        **three_arguments,
    )
    three_specialized = automata.three_color_totalistic_cellular_automaton(
        **three_arguments,
    )
    four_general = automata.totalistic_cellular_automaton(
        colors=4,
        radius=1,
        **four_arguments,
    )
    four_specialized = automata.higher_color_totalistic_cellular_automaton(
        colors=4,
        radius=1,
        **four_arguments,
    )

    assert three_general == three_specialized
    assert serialization.dumps(three_general) == serialization.dumps(
        three_specialized
    )
    assert four_general == four_specialized
    assert serialization.dumps(four_general) == serialization.dumps(
        four_specialized
    )


def test_ranked_named_presets_equal_the_same_lattice_expansion() -> None:
    initial_2d = (0, 1, 1, 0)
    von_neumann = (
        (-1, 0),
        (0, -1),
        (0, 0),
        (0, 1),
        (1, 0),
    )
    named_2d = automata.cellular_automaton_2d(
        shape=(2, 2),
        initial=initial_2d,
        colors=2,
        rule=_identity_table(2, 5, 2),
    )
    lattice_2d = automata.lattice_cellular_automaton(
        shape=(2, 2),
        initial=initial_2d,
        colors=2,
        offsets=von_neumann,
        rule=_identity_table(2, 5, 2),
        axes=("x", "y"),
    )
    named_3d = automata.cellular_automaton_3d(
        shape=(2, 1, 1),
        initial=(0, 1),
        colors=2,
        offsets=((0, 0, 0),),
        rule=(0, 1),
    )
    lattice_3d = automata.lattice_cellular_automaton(
        shape=(2, 1, 1),
        initial=(0, 1),
        colors=2,
        offsets=((0, 0, 0),),
        rule=(0, 1),
        axes=("x", "y", "z"),
    )

    assert named_2d == lattice_2d
    assert serialization.dumps(named_2d) == serialization.dumps(lattice_2d)
    assert named_3d == lattice_3d
    assert serialization.dumps(named_3d) == serialization.dumps(lattice_3d)


def test_digit_reversal_equals_its_generic_arithmetic_expansion() -> None:
    source = rules.observation(0)
    expression = rules.add(
        source,
        rules.from_digits(
            rules.reverse(rules.integer_digits(source, 2)),
            2,
        ),
    )
    generic = automata.arithmetic_iteration(
        initial=6,
        alphabet=alphabets.naturals(),
        map_expression=expression,
    )
    named = automata.digit_reversal_map(initial=6, base=2)

    assert generic == named
    assert serialization.dumps(generic) == serialization.dumps(named)


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
    one_dimensional = machina.turing_machine(
        tape=(0, 0, 1, 0, 0),
        head=2,
        initial_state="q0",
        states=("q0",),
        symbols=2,
        transitions=((("q0", 0), ("q0", 1, 1)),),
        boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
    )
    two_dimensional = machina.turing_machine_2d(
        shape=(3, 3),
        tape=(0, 0, 0, 0, 1, 0, 0, 0, 0),
        head=(1, 1),
        initial_state="q0",
        states=("q0",),
        symbols=2,
        transitions=((("q0", 0), ("q0", 1, (0, 1))),),
        boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
    )

    _assert_terminal(one_dimensional)
    _assert_terminal(two_dimensional)


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
        encoded = serialization.dumps(simple)
        assert serialization.loads(encoded) == serialization.Decoded(simple)
        assert b"catalog:" not in encoded


@pytest.mark.parametrize(
    "constructor",
    (
        lambda: automata.multicolor_cellular_automaton(
            initial=(0, 1, 0),
            colors=2,
            rule=(0,) * 8,
            boundary=loci.Boundary(loci.BoundaryPolicy.NONE),
        ),
        lambda: automata.totalistic_cellular_automaton(
            initial=(0, 1, 0),
            colors=2,
            rule=(0,) * 4,
            boundary=loci.Boundary(loci.BoundaryPolicy.NONE),
        ),
        lambda: automata.cellular_automaton_2d(
            shape=(1, 1),
            initial=(0,),
            colors=2,
            rule=(0,) * 32,
            boundary=loci.Boundary(loci.BoundaryPolicy.NONE),
        ),
        lambda: automata.moore_cellular_automaton(
            shape=(1, 1),
            initial=(0,),
            colors=2,
            rule=(0,) * 512,
            boundary=loci.Boundary(loci.BoundaryPolicy.NONE),
        ),
        lambda: automata.cellular_automaton_3d(
            shape=(2, 1, 1),
            initial=(0, 0),
            colors=2,
            offsets=((0, 0, 0), (1, 0, 0)),
            rule=(0,) * 4,
            boundary=loci.Boundary(loci.BoundaryPolicy.NONE),
        ),
        lambda: automata.lattice_cellular_automaton(
            shape=(2, 1),
            initial=(0, 0),
            colors=2,
            offsets=((0, 0), (1, 0)),
            rule=(0,) * 4,
            boundary=loci.Boundary(loci.BoundaryPolicy.NONE),
        ),
        lambda: automata.continuous_cellular_automaton(
            initial=(Fraction(0), Fraction(1)),
            local_rule=rules.project(rules.group(0), 1),
            boundary=loci.Boundary(loci.BoundaryPolicy.NONE),
        ),
    ),
)
def test_nonzero_finite_stencils_reject_absent_boundaries(
    constructor,
) -> None:
    with pytest.raises(ValueError, match="BoundaryPolicy.NONE"):
        constructor()


def test_zero_only_lattice_stencil_accepts_absent_boundary() -> None:
    simple = automata.lattice_cellular_automaton(
        shape=(1, 1),
        initial=(1,),
        colors=2,
        offsets=((0, 0),),
        rule=(0, 1),
        boundary=loci.Boundary(loci.BoundaryPolicy.NONE),
    )

    assert _values(_successor(simple)) == (1,)


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
