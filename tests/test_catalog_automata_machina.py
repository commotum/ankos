from __future__ import annotations

import inspect

import pytest

from ca import program
from ca.catalog import automata, machina


CANONICAL_CONSTRUCTORS = (
    automata.alternating_partition_local_evolution,
    automata.asynchronous_local_state_automaton,
    automata.coupled_field_mobile_locus_evolution,
    automata.driven_relaxation,
    automata.history_dependent_agent_game,
    automata.iterated_map,
    automata.multi_active_local_rewrite,
    automata.mutable_rule_local_automaton,
    automata.population_evolutionary_search,
    automata.synchronous_local_state_transform,
    automata.weighted_network_state_update,
    machina.enumerative_semidecision,
    machina.finite_gate_circuit,
    machina.mobile_head_grid_rewrite,
    machina.nearest_neighbor_retrieval,
    machina.recursive_function_evaluator,
    machina.register_machine,
    machina.stored_program_random_access_machine,
    machina.priority_dovetailed_oracle_construction,
)


@pytest.mark.parametrize("constructor", CANONICAL_CONSTRUCTORS)
def test_canonical_constructor_is_exact_five_component_assembly(constructor) -> None:
    reference = automata.eca(rule=30, width=5)

    assert tuple(inspect.signature(constructor).parameters) == (
        "seed",
        "alphabet",
        "frontier",
        "neighborhood",
        "rule",
    )
    assert all(
        parameter.kind is inspect.Parameter.KEYWORD_ONLY
        for parameter in inspect.signature(constructor).parameters.values()
    )

    constructed = constructor(
        seed=reference.seed,
        alphabet=reference.alphabet,
        frontier=reference.frontier,
        neighborhood=reference.neighborhood,
        rule=reference.rule,
    )

    assert type(constructed) is program.SimpleProgram
    assert constructed == reference


def test_eca_binds_one_concrete_ordinary_program() -> None:
    constructed = automata.eca(rule=110, width=7)

    assert type(constructed) is program.SimpleProgram
    assert constructed.seed.configuration_contract.shape == (7,)
    assert constructed.alphabet.value_profile.value == "boolean"
    assert constructed.rule.descriptor.denotation.provenance == (
        "preset:elementary",
        "rule-110",
    )


def test_elementary_cellular_automaton_is_an_exact_alias() -> None:
    assert automata.elementary_cellular_automaton(rule=90, width=9) == (
        automata.eca(rule=90, width=9)
    )


@pytest.mark.parametrize("width", (0, -1))
def test_eca_rejects_nonpositive_width(width: int) -> None:
    with pytest.raises(ValueError, match="positive"):
        automata.eca(width=width)


def test_eca_rejects_boolean_width() -> None:
    with pytest.raises(TypeError, match="integer"):
        automata.eca(width=True)
