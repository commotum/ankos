"""CT03: fixed validation order and fail-closed application."""

import pytest

import ca
from ca import frontiers, neighborhoods, program as program_api, rules

from g7_fixtures import derivation, finite_record_program, native_program
from helpers import assert_no_authoritative_commit


class SentinelPhaseFault(ValueError):
    """Private injected fault used to prove the generic phase boundary."""


_PHASE_HOOKS = (
    (
        program_api.ApplicationPhase.PROGRAM,
        program_api,
        "_require_compatible_five_fields",
    ),
    (
        program_api.ApplicationPhase.INPUT,
        program_api,
        "_normalize_input",
    ),
    (
        program_api.ApplicationPhase.FRONTIER,
        frontiers.WritableRegion,
        "resolve",
    ),
    (
        program_api.ApplicationPhase.NEIGHBORHOOD,
        neighborhoods.ReadableRegion,
        "resolve",
    ),
    (
        program_api.ApplicationPhase.JOIN,
        program_api,
        "_validate_join",
    ),
    (
        program_api.ApplicationPhase.RULE_DENOTATION,
        rules.Rule,
        "denote",
    ),
    (
        program_api.ApplicationPhase.RESULT_VALIDATION,
        program_api,
        "_validate_rule_space",
    ),
    (
        program_api.ApplicationPhase.FRESH_BINDING,
        program_api,
        "_bind_fresh_for_atom",
    ),
    (
        program_api.ApplicationPhase.COMMIT,
        program_api,
        "_commit",
    ),
    (
        program_api.ApplicationPhase.SUCCESSOR,
        program_api,
        "_lineage_after",
    ),
    (
        program_api.ApplicationPhase.QUOTIENT_MEASURE,
        program_api,
        "_quotient",
    ),
)


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


@pytest.mark.parametrize(
    "fault_phase",
    tuple(program_api.ApplicationPhase),
    ids=lambda phase: phase.value,
)
def test_first_fault_at_each_phase_is_fail_closed(
    fault_phase: program_api.ApplicationPhase,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    simple_program, source, _ = native_program("dyadlags")
    input_identity = source.identity
    observed: list[program_api.ApplicationPhase] = []

    for phase, owner, attribute in _PHASE_HOOKS:
        original = getattr(owner, attribute)

        def phase_spy(
            *args,
            _phase=phase,
            _original=original,
            **kwargs,
        ):
            observed.append(_phase)
            if _phase is fault_phase:
                raise SentinelPhaseFault(f"sentinel:{_phase.value}")
            return _original(*args, **kwargs)

        monkeypatch.setattr(owner, attribute, phase_spy)

    result = ca.apply(simple_program, source)
    all_phases = tuple(program_api.ApplicationPhase)
    expected_attempts = all_phases[: all_phases.index(fault_phase) + 1]

    assert isinstance(result, program_api.ApplicationRejected)
    assert result.fault.phase is fault_phase
    assert result.fault.reason == f"sentinel:{fault_phase.value}"
    assert result.fault.evidence == ("SentinelPhaseFault",)
    assert result.fault.attempted_phases == expected_attempts
    assert tuple(observed) == expected_attempts
    assert_no_authoritative_commit(result, source, input_identity)


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
    assert_no_authoritative_commit(result, source, before)
