"""Focused adversarial checks for complete application result records."""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction

import pytest

import ca
from ca import program, rules

from g7_fixtures import derivation, finite_record_program


def _probabilistic_diamond() -> program.ApplicationComplete:
    def atoms(targets):
        preserved = tuple(rules.preserve(target) for target in targets)
        return (
            derivation("integrity-left", existing=preserved),
            derivation("integrity-right", existing=preserved),
        )

    simple_program, source = finite_record_program(
        (("cell", False),),
        atoms,
        probability=(Fraction(1, 3), Fraction(2, 3)),
    )
    result = ca.apply(simple_program, source)
    assert isinstance(result, program.ApplicationComplete)
    return result


def test_complete_result_rejects_nonbijective_source_mapping_and_bad_lineage() -> None:
    valid = _probabilistic_diamond()
    first, second = valid.applied_atoms.atoms
    assert isinstance(first, program.AppliedDerivation)
    assert isinstance(second, program.AppliedDerivation)

    duplicate_source = replace(second, source=first.source)
    with pytest.raises(ValueError):
        replace(
            valid,
            applied_atoms=rules.finite_support(
                (first, duplicate_source),
                label="applied-atoms",
            ),
        )

    bad_lineage = replace(
        first,
        output_trace_lineage=program.TraceLineage(
            first.input_trace_lineage.root_identity,
            (*first.input_trace_lineage.path, "foreign-edge"),
        ),
    )
    with pytest.raises(ValueError):
        replace(
            valid,
            applied_atoms=rules.finite_support(
                (bad_lineage, second),
                label="applied-atoms",
            ),
        )


def test_complete_result_rejects_incomplete_fiber_and_wrong_measures() -> None:
    valid = _probabilistic_diamond()
    group = valid.successor_quotient_with_derivation_fibers.atoms[0]
    assert isinstance(group, program.SuccessorGroup)
    assert len(group.derivations) == 2

    incomplete_group = program.SuccessorGroup(
        group.successor,
        group.derivations[:1],
    )
    with pytest.raises(ValueError):
        replace(
            valid,
            successor_quotient_with_derivation_fibers=rules.finite_support(
                (incomplete_group,),
                label="successor-quotient",
            ),
        )

    first, second = valid.applied_atoms.atoms
    wrong_applied_measure = program.MeasureAvailable(
        program.ProgramMeasure(
            (
                program.MeasureMass(first.canonical_identity, Fraction(1, 2)),
                program.MeasureMass(second.canonical_identity, Fraction(1, 2)),
            ),
            Fraction(1),
        )
    )
    with pytest.raises(ValueError):
        replace(valid, applied_atom_measure=wrong_applied_measure)
    with pytest.raises(ValueError):
        replace(valid, no_successor_submeasure=program.MeasureAbsent())
    with pytest.raises(ValueError):
        replace(valid, successor_submeasure=program.MeasureAbsent())
