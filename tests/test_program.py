"""Unit tests for five-field programs, application, and rollout."""

from dataclasses import fields, replace

import pytest

import ca
from ca import alphabets, frontiers, loci, neighborhoods, program, rules, seeds


def _program():
    source = loci.history_configuration((True, False, False))
    alphabet = alphabets.boolean()
    return (
        ca.SimpleProgram(
            seeds.exact(source),
            alphabet,
            frontiers.everywhere(
                configuration_contract=source.contract,
                value_profile=alphabet.value_profile,
            ),
            neighborhoods.dyadlags_0d(
                configuration_contract=source.contract
            ),
            rules.dyadlags_0d(rule=150),
        ),
        source,
    )


def test_simple_program_has_exactly_five_stored_fields() -> None:
    simple_program, _ = _program()

    assert tuple(field.name for field in fields(simple_program)) == (
        "seed",
        "alphabet",
        "frontier",
        "neighborhood",
        "rule",
    )
    assert len(simple_program.__dict__) == 5


def test_program_construction_validates_cross_field_contracts() -> None:
    simple_program, _ = _program()
    incompatible = replace(
        simple_program.neighborhood,
        value_profile=alphabets.ValueProfile.INTEGER,
    )

    with pytest.raises(program.ProgramCompatibilityError):
        ca.SimpleProgram(
            simple_program.seed,
            simple_program.alphabet,
            simple_program.frontier,
            incompatible,
            simple_program.rule,
        )


def test_apply_owns_application_results_and_preserves_the_input() -> None:
    simple_program, source = _program()
    identity = source.identity

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationComplete)
    assert source.identity == identity
    assert result.evidence.phases == tuple(program.ApplicationPhase)
    assert len(result.applied_atoms.atoms) == 1
    assert len(result.successor_quotient_with_derivation_fibers.atoms) == 1


def test_rollout_uses_the_owned_apply_operation_and_preserves_fibers(
    monkeypatch,
) -> None:
    simple_program, source = _program()
    calls = []
    owned_apply = program.apply

    def spy(*args, **kwargs):
        calls.append(args[1])
        return owned_apply(*args, **kwargs)

    monkeypatch.setattr(program, "apply", spy)
    result = ca.rollout(simple_program, steps=2, initial=source)

    assert isinstance(result, program.RolloutTruncated)
    assert len(calls) == 2
    assert len(result.raw_trace.applications.atoms) == 2
    assert len(result.raw_trace.derivation_edges.atoms) == 2
    assert len(result.raw_trace.lineage_graph) == 2


def test_rollout_binds_seed_or_validates_explicit_initial_state() -> None:
    simple_program, source = _program()

    seeded = ca.rollout(simple_program, steps=0)
    explicit = ca.rollout(simple_program, steps=0, initial=source)
    invalid = ca.rollout(
        simple_program,
        steps=0,
        initial=loci.history_configuration((1, 2, 3)),
    )

    assert isinstance(seeded, program.RolloutTruncated)
    assert seeded.raw_trace.seed_evidence.source_identity != "explicit-initial"
    assert isinstance(explicit, program.RolloutTruncated)
    assert explicit.raw_trace.seed_evidence.source_identity == "explicit-initial"
    assert isinstance(invalid, program.RolloutRejected)


def test_program_result_records_remain_owner_qualified() -> None:
    assert program.ApplicationComplete.__module__ == "ca.program"
    assert program.RolloutComplete.__module__ == "ca.program"
    assert program.RolloutTruncated.__module__ == "ca.program"
    assert not hasattr(ca, "ApplicationComplete")
    assert not hasattr(ca, "RolloutComplete")
