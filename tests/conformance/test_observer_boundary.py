"""CT14: executable constructions versus observer roles.

G7-02 proves the mechanics boundary with ordinary five-field programs and
pure external views. G7-04 owns the callable-free role metadata; G7-03 owns
the corresponding serialization exclusion.
"""

from dataclasses import dataclass, fields

import pytest

import ca
from ca import program

from g7_mechanics import (
    MECHANICS_ROWS,
    assert_mechanics_run,
    run_mechanics_fixture,
)


@dataclass(frozen=True)
class RenderedObservation:
    """Pure test-side projection with no semantic authority."""

    label: str
    source_identity: str


def test_f004_and_f045_are_executable_ordinary_programs() -> None:
    """Both families own explicit readable/writable state and invariant commits."""

    rows = {row.spf: row for row in MECHANICS_ROWS}
    for spf in ("SPF004", "SPF042"):
        execution = run_mechanics_fixture(rows[spf])
        assert_mechanics_run(execution)
        assert type(execution.simple_program) is ca.SimpleProgram
        assert isinstance(execution.result, program.ApplicationComplete)


@pytest.mark.skip(reason="G7-04 owns callable-free F010/F042 role metadata")
def test_f010_and_f042_are_callable_free_role_entries() -> None:
    """Interfaces and observations gain no constructor merely from naming."""

    raise AssertionError("G7-04 role metadata is not active")


def test_observers_cannot_change_identity_or_application() -> None:
    """Pure tooling occupies no field and cannot influence semantic results."""

    row = next(row for row in MECHANICS_ROWS if row.spf == "SPF004")
    execution = run_mechanics_fixture(row)
    before_identity = execution.simple_program.canonical_identity
    before_result = execution.result
    observation = RenderedObservation(
        "causal-network-view",
        execution.source.identity,
    )

    assert observation.source_identity == execution.source.identity
    assert tuple(field.name for field in fields(ca.SimpleProgram)) == (
        "seed",
        "alphabet",
        "frontier",
        "neighborhood",
        "rule",
    )
    assert execution.simple_program.canonical_identity == before_identity
    assert ca.apply(execution.simple_program, execution.source) == before_result


@pytest.mark.skip(reason="G7-03 owns canonical serialization exclusion checks")
def test_observers_cannot_change_serialization() -> None:
    """No pure observer is admitted into a canonical five-field payload."""

    raise AssertionError("G7-03 serialization boundary is not active")


def test_stateful_transform_with_its_own_commit_remains_an_ordinary_program() -> None:
    """The role boundary does not forbid separately specified media mechanics."""

    row = next(row for row in MECHANICS_ROWS if row.spf == "SPF042")
    execution = run_mechanics_fixture(row)
    assert_mechanics_run(execution)
    assert isinstance(execution.result, program.ApplicationComplete)
    derivation = execution.result.applied_atoms.atoms[0]
    assert isinstance(derivation, program.AppliedDerivation)
    assert derivation.source.provenance == (
        "mechanics:visible-surrogate-evaluator-state",
    )
