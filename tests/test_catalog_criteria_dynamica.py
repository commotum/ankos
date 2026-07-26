from __future__ import annotations

import inspect

import pytest

from ca import program
from ca.catalog import automata, criteria, dynamica


CANONICAL_CONSTRUCTORS = (
    criteria.finite_model_satisfaction,
    criteria.geometric_embedding_relation,
    criteria.global_equation_relation,
    criteria.inverse_local_system_reconstruction,
    criteria.local_factor_weighted_relation,
    criteria.local_satisfaction_relation,
    criteria.program_randomization_test,
    criteria.stochastic_local_search,
    criteria.weighted_history_sum_relation,
    dynamica.continuous_event_dynamics,
    dynamica.ordinary_differential_flow,
    dynamica.partial_differential_relation,
)


@pytest.mark.parametrize("constructor", CANONICAL_CONSTRUCTORS)
def test_canonical_constructor_is_exact_five_component_assembly(constructor) -> None:
    reference = automata.eca(rule=30, width=5)
    signature = inspect.signature(constructor)

    assert tuple(signature.parameters) == (
        "seed",
        "alphabet",
        "frontier",
        "neighborhood",
        "rule",
    )
    assert all(
        parameter.kind is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
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


def test_pde_is_an_exact_same_signature_alias() -> None:
    reference = automata.eca(rule=90, width=7)
    arguments = {
        "seed": reference.seed,
        "alphabet": reference.alphabet,
        "frontier": reference.frontier,
        "neighborhood": reference.neighborhood,
        "rule": reference.rule,
    }

    assert inspect.signature(dynamica.pde) == inspect.signature(
        dynamica.partial_differential_relation
    )
    assert dynamica.pde(**arguments) == (
        dynamica.partial_differential_relation(**arguments)
    )
