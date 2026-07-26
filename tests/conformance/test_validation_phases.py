"""CT03: fixed validation order and fail-closed application."""

from ca import program as program_api, rules

import ca

from g7_fixtures import derivation, finite_record_program, native_program
from helpers import assert_no_authoritative_commit


def test_application_runs_the_exact_generic_phase_order() -> None:
    simple_program, source, _ = native_program("dyadlags")

    result = ca.apply(simple_program, source)

    assert isinstance(result, program_api.ApplicationComplete)
    assert result.evidence.phases == tuple(program_api.ApplicationPhase)
    assert tuple(phase.value for phase in result.evidence.phases) == (
        "program",
        "input",
        "frontier",
        "neighborhood",
        "join",
        "rule-denotation",
        "result-validation",
        "fresh-binding",
        "commit",
        "successor",
        "quotient-measure",
    )


def test_first_failing_phase_prevents_every_later_phase() -> None:
    simple_program, _, _ = native_program("dyadlags")

    result = ca.apply(simple_program, object())  # type: ignore[arg-type]

    assert isinstance(result, program_api.ApplicationRejected)
    assert result.fault.phase is program_api.ApplicationPhase.INPUT
    assert result.fault.attempted_phases == (
        program_api.ApplicationPhase.PROGRAM,
        program_api.ApplicationPhase.INPUT,
    )


def test_one_invalid_atom_rejects_the_complete_finite_rule_space() -> None:
    def atoms(targets):
        valid = derivation(
            "valid",
            existing=tuple(rules.replace(target, True) for target in targets),
        )
        invalid = derivation("invalid", existing=())
        return valid, invalid

    simple_program, source = finite_record_program((("cell", False),), atoms)

    result = ca.apply(simple_program, source)

    assert isinstance(result, program_api.ApplicationRejected)
    assert result.fault.phase is program_api.ApplicationPhase.RESULT_VALIDATION
    assert result.fault.attempted_phases[-1] is program_api.ApplicationPhase.RESULT_VALIDATION


def test_rejection_preserves_input_and_publishes_no_authoritative_result() -> None:
    def atoms(_targets):
        return (derivation("missing-totality", existing=()),)

    simple_program, source = finite_record_program((("cell", False),), atoms)
    before = source.identity

    result = ca.apply(simple_program, source)

    assert isinstance(result, program_api.ApplicationRejected)
    assert source.identity == before
    assert not hasattr(result, "applied_atoms")
    assert not hasattr(result, "successor_quotient_with_derivation_fibers")
    assert_no_authoritative_commit(result, source)
