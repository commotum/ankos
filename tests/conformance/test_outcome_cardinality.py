"""CT05: semantic outcomes and independent cardinalities."""

import pytest

import ca
from ca import program, rules

from g7_fixtures import (
    certificate,
    derivation,
    diamond_program,
    finite_record_program,
    no_successor,
    native_program,
)


def test_all_progress_continuation_and_no_successor_outcomes_remain_distinct() -> None:
    assert rules.Progress.ADVANCED is not rules.Progress.QUIESCENT
    assert isinstance(rules.Continue(), rules.Continue)
    assert isinstance(
        rules.Stop(
            rules.literal_expr("done"),
            certificate(rules.CertificateKind.TERMINALITY, "done"),
        ),
        rules.Stop,
    )
    atoms = tuple(
        no_successor(f"outcome-{outcome.value}", outcome)
        for outcome in rules.NoSuccessorOutcome
    )
    assert {atom.outcome for atom in atoms} == set(rules.NoSuccessorOutcome)
    assert len({atom.canonical_identity for atom in atoms}) == 4


def test_outcome_derivation_and_successor_cardinalities_are_independent() -> None:
    simple_program, source = diamond_program()

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationComplete)
    assert rules.cardinality_size(result.outcome_atom_cardinality) == 2
    assert rules.cardinality_size(result.derivation_cardinality) == 2
    assert rules.cardinality_size(result.successor_cardinality) == 1
    assert len(
        result.successor_quotient_with_derivation_fibers.atoms[0].derivations
    ) == 2

    def stopped(targets):
        return (
            derivation(
                "stopped-one-shot",
                existing=tuple(rules.preserve(target) for target in targets),
                progress=rules.Progress.QUIESCENT,
                continuation=rules.Stop(
                    rules.literal_expr("one-shot-complete"),
                    certificate(
                        rules.CertificateKind.TERMINALITY,
                        "one-shot-complete",
                    ),
                ),
            ),
        )

    stopped_program, stopped_source = finite_record_program(
        (("cell", False),),
        stopped,
    )
    stopped_result = ca.apply(stopped_program, stopped_source)
    assert isinstance(stopped_result, program.ApplicationComplete)
    assert rules.cardinality_size(stopped_result.outcome_atom_cardinality) == 1
    assert rules.cardinality_size(stopped_result.derivation_cardinality) == 1
    assert rules.cardinality_size(stopped_result.successor_cardinality) == 1


def test_exact_zero_requires_typed_atom_and_coverage_evidence() -> None:
    empty = rules.finite_support((), label="typed-empty-partition")

    assert isinstance(empty.cardinality, rules.ExactlyZero)
    assert empty.cardinality.evidence.kind is rules.CertificateKind.CARDINALITY
    assert empty.completeness_evidence.kind is rules.CertificateKind.COMPLETENESS
    assert empty.soundness_evidence.kind is rules.CertificateKind.SOUNDNESS

    simple_program, _, _ = native_program("dyadlags")
    with pytest.raises(ValueError, match="bare empty"):
        rules.literal(
            rules.OutcomeSpace(empty),
            contract=simple_program.rule.contract,
        )

    unknown = rules.Undetermined(
        rules.literal_expr("not-enumerated"),
        certificate(rules.CertificateKind.CARDINALITY, "open-obligation"),
    )
    assert rules.cardinality_size(unknown) is None

    simple_program, source, _ = native_program("dyadlags")
    exact_zero = rules.ExactlyZero(
        certificate(rules.CertificateKind.CARDINALITY, "exactly-zero")
    )
    zero_relation = rules.relation(
        rules.literal_expr("empty-relation"),
        exact_zero,
        contract=simple_program.rule.contract,
        completeness_evidence=certificate(
            rules.CertificateKind.COMPLETENESS,
            "empty-complete",
        ),
        soundness_evidence=certificate(
            rules.CertificateKind.SOUNDNESS,
            "empty-sound",
        ),
    )
    zero_program = ca.SimpleProgram(
        simple_program.seed,
        simple_program.alphabet,
        simple_program.frontier,
        simple_program.neighborhood,
        zero_relation,
    )
    rejected = ca.apply(zero_program, source)
    assert isinstance(rejected, program.ApplicationRejected)
    assert rejected.fault.phase is program.ApplicationPhase.RESULT_VALIDATION
    assert "typed NoSuccessor" in rejected.fault.reason


def test_resource_exhaustion_exists_only_in_bounded_external_results() -> None:
    simple_program, source, _ = native_program("dyadlags")

    result = ca.rollout(simple_program, steps=0, initial=source)

    assert isinstance(result, program.RolloutTruncated)
    assert result.cause is program.TruncationCause.DEPTH_BOUND
    assert "resource-exhausted" in {
        cause.value for cause in program.TruncationCause
    }
    assert not hasattr(rules, "ResourceExhausted")
