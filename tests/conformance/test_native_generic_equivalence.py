"""CT12: independent retained-native and generic one-step equivalence."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

import ca
from ca import loci, program, rules

import test_oracles
from g7_fixtures import native_program, successor_values


NATIVE_CASES = (
    "ar2",
    "dyadlags",
    "lagcounts",
    "dyadrads",
    "dyadaxes-2d",
    "dyadaxes-3d",
)


def test_reference_oracles_are_statically_independent_of_runtime_semantics() -> None:
    source = Path(test_oracles.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)

    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_from = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    }
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }

    assert not any(name == "ca" or name.startswith("ca.") for name in imported)
    assert not any(
        name == "ca" or (name is not None and name.startswith("ca."))
        for name in imported_from
    )
    assert called_names.isdisjoint({"apply", "rollout", "denote", "commit"})


@pytest.mark.parametrize("case_id", NATIVE_CASES)
def test_finite_native_fixtures_match_complete_generic_results(
    case_id: str,
) -> None:
    simple_program, source, expected = native_program(case_id)

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationComplete)
    assert successor_values(result) == expected
    assert result.source_outcomes.support.presentation is rules.SupportPresentation.FINITE
    assert len(result.source_outcomes.support.atoms) == 1
    assert len(result.applied_atoms.atoms) == 1
    assert len(result.no_successor_partition.atoms) == 0
    assert rules.cardinality_size(result.outcome_atom_cardinality) == 1
    assert rules.cardinality_size(result.derivation_cardinality) == 1
    assert rules.cardinality_size(result.successor_cardinality) == 1
    assert isinstance(result.applied_atom_measure, program.MeasureAbsent)
    assert isinstance(result.successor_submeasure, program.MeasureAbsent)
    assert isinstance(result.no_successor_submeasure, program.MeasureAbsent)
    assert result.evidence.phases == tuple(program.ApplicationPhase)
    successor = result.successor_quotient_with_derivation_fibers.atoms[0].successor
    assert isinstance(successor, loci.FiniteConfiguration)
    assert source.identity != successor.identity


@pytest.mark.skip(reason="variable-structure/stochastic catalog fixtures belong to G7-02/G7-04")
def test_variable_structure_and_stochastic_fixtures_match_completely() -> None:
    pass


@pytest.mark.skip(reason="differential/intensional catalog fixtures belong to G7-02/G7-04")
def test_differential_and_intensional_fixtures_use_exact_tiny_oracles() -> None:
    pass
