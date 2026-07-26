"""Focused tests for the Substitua and Media five-field constructors."""

from __future__ import annotations

from inspect import Parameter, signature

import pytest

from ca import SimpleProgram, alphabets, frontiers, loci, neighborhoods, rules, seeds
from ca.catalog import media, substitua


SUBSTITUA_CANONICAL = (
    substitua.append_only_sequence_generation,
    substitua.context_dependent_substitution,
    substitua.first_passage_aggregation,
    substitua.front_delete_rear_append_system,
    substitua.global_score_sequential_placement,
    substitua.history_dependent_growth_rewrite,
    substitua.indexed_history_recurrence,
    substitua.iterated_erasure_process,
    substitua.local_graph_rewrite,
    substitua.moving_frontier_shell_accretion,
    substitua.multiway_rewrite,
    substitua.parallel_independent_substitution,
    substitua.parallel_network_rewrite,
    substitua.random_functional_graph_construction,
    substitua.structural_pattern_rewrite,
)

MEDIA_CANONICAL = (
    media.event_provenance_causal_network,
    media.digit_emitting_register_transduction,
    media.error_diffusion_transform,
    media.maximal_run_record_transduction,
    media.hash_index_transform,
    media.probabilistic_transition_model_fitting,
    media.sampled_causal_order_network,
    media.weighted_prefix_block_transduction,
    media.nested_interval_symbol_transduction,
    media.history_reference_record_transduction,
    media.recursive_uniform_region_decomposition,
    media.orthogonal_basis_coefficient_transform,
    media.predictive_residual_transduction,
    media.aligned_xor_stream_transduction,
)

CANONICAL = (*SUBSTITUA_CANONICAL, *MEDIA_CANONICAL)


def _components():
    source = loci.history_configuration((True, False, False))
    alphabet = alphabets.boolean()
    return (
        seeds.exact(source),
        alphabet,
        frontiers.everywhere(
            configuration_contract=source.contract,
            value_profile=alphabet.value_profile,
        ),
        neighborhoods.dyadlags_0d(
            configuration_contract=source.contract,
        ),
        rules.dyadlags_0d(rule=150),
    )


@pytest.mark.parametrize("constructor", CANONICAL)
def test_canonical_constructor_is_an_exact_five_field_expansion(
    constructor,
) -> None:
    seed, alphabet, frontier, neighborhood, rule = _components()

    result = constructor(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )

    assert type(result) is SimpleProgram
    assert result.seed is seed
    assert result.alphabet is alphabet
    assert result.frontier is frontier
    assert result.neighborhood is neighborhood
    assert result.rule is rule


@pytest.mark.parametrize("constructor", (*CANONICAL, substitua.multiway_system, substitua.network_rewrite))
def test_constructor_signature_is_keyword_only_and_uniform(constructor) -> None:
    parameters = tuple(signature(constructor).parameters.values())

    assert tuple(parameter.name for parameter in parameters) == (
        "seed",
        "alphabet",
        "frontier",
        "neighborhood",
        "rule",
    )
    assert all(parameter.kind is Parameter.KEYWORD_ONLY for parameter in parameters)


@pytest.mark.parametrize(
    ("alias_name", "delegate_name"),
    (
        ("multiway_system", "multiway_rewrite"),
        ("network_rewrite", "parallel_network_rewrite"),
    ),
)
def test_true_alias_delegates_with_the_exact_five_fields(
    monkeypatch,
    alias_name,
    delegate_name,
) -> None:
    seed, alphabet, frontier, neighborhood, rule = _components()
    expected = object()
    received = []

    def delegate(
        *,
        seed,
        alphabet,
        frontier,
        neighborhood,
        rule,
    ):
        received.append((seed, alphabet, frontier, neighborhood, rule))
        return expected

    monkeypatch.setattr(substitua, delegate_name, delegate)

    result = getattr(substitua, alias_name)(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )

    assert result is expected
    assert received == [(seed, alphabet, frontier, neighborhood, rule)]
