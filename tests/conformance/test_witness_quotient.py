"""CT08: witnesses, derivation fibers, and semantic quotienting."""

from fractions import Fraction

import ca
from ca import alphabets, loci, program, rules

from g7_fixtures import (
    derivation,
    diamond_program,
    finite_record_program,
)


def test_diamond_has_two_atoms_two_derivations_and_one_successor() -> None:
    simple_program, source = diamond_program()

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationComplete)
    assert len(result.source_outcomes.support.atoms) == 2
    assert len(result.applied_atoms.atoms) == 2
    assert len(result.successor_quotient_with_derivation_fibers.atoms) == 1
    fiber = result.successor_quotient_with_derivation_fibers.atoms[0]
    assert {item.source.witness.identity for item in fiber.derivations} == {
        "diamond-left",
        "diamond-right",
    }


def test_rule_enumeration_permutation_preserves_quotient_and_fibers() -> None:
    def atoms(targets):
        replacement = tuple(rules.replace(target, True) for target in targets)
        return (
            derivation("left", existing=replacement),
            derivation("right", existing=replacement),
        )

    def reversed_atoms(targets):
        return tuple(reversed(atoms(targets)))

    left_program, source = finite_record_program((("cell", False),), atoms)
    right_program, _ = finite_record_program(
        (("cell", False),),
        reversed_atoms,
    )

    left = ca.apply(left_program, source)
    right = ca.apply(right_program, source)

    assert isinstance(left, program.ApplicationComplete)
    assert isinstance(right, program.ApplicationComplete)
    left_fiber = left.successor_quotient_with_derivation_fibers.atoms[0]
    right_fiber = right.successor_quotient_with_derivation_fibers.atoms[0]
    assert loci.semantic_equal(left_fiber.successor, right_fiber.successor)
    assert {
        item.source.witness.identity for item in left_fiber.derivations
    } == {
        item.source.witness.identity for item in right_fiber.derivations
    }


def test_semantic_equality_is_not_hash_storage_rendering_or_catalog_name() -> None:
    carrier = loci.Carrier(
        loci.CarrierContract(loci.CarrierKind.RECORD, rank=0, shape=()),
        loci.Boundary(loci.BoundaryPolicy.NONE),
    )
    a = loci.named("a", scope="record")
    b = loci.named("b", scope="record")
    left = loci.FiniteConfiguration(carrier, ((a, False), (b, True)))
    differently_ordered = loci.FiniteConfiguration(
        carrier,
        ((b, True), (a, False)),
    )
    different_boundary = loci.FiniteConfiguration(
        loci.Carrier(
            carrier.contract,
            loci.Boundary(loci.BoundaryPolicy.FIXED, False),
        ),
        ((a, False), (b, True)),
    )

    assert loci.semantic_equal(left, differently_ordered)
    assert left.identity == differently_ordered.identity
    assert not loci.semantic_equal(left, different_boundary)
    assert not hasattr(left, "catalog_name")


def test_equal_successor_mass_aggregates_without_erasing_source_atoms() -> None:
    simple_program, source = diamond_program()

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationComplete)
    assert isinstance(result.successor_submeasure, program.MeasureAvailable)
    assert result.successor_submeasure.measure.masses == (
        program.MeasureMass(
            result.successor_quotient_with_derivation_fibers.atoms[
                0
            ].canonical_identity,
            Fraction(1),
        ),
    )
    assert tuple(
        item.mass for item in result.applied_atom_measure.measure.masses
    ) == (Fraction(1, 3), Fraction(2, 3))
