"""CT08: witnesses, derivation fibers, and semantic quotienting."""

from fractions import Fraction

import pytest

import ca
from ca import alphabets, frontiers, loci, neighborhoods, program, rules, seeds

from g7_fixtures import (
    derivation,
    diamond_program,
    finite_record_program,
    rule_contract,
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
    assert left == right
    assert (
        left.successor_quotient_with_derivation_fibers
        == right.successor_quotient_with_derivation_fibers
    )
    assert left.applied_atoms == right.applied_atoms


def test_semantic_equality_is_not_hash_storage_rendering_or_catalog_name(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
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

    monkeypatch.setattr(loci.Locus, "__hash__", lambda _self: 1)
    false_value = loci.FiniteConfiguration(
        carrier,
        ((a, False), (b, False)),
    )
    assert hash(a) == hash(b)
    assert not loci.semantic_equal(left, false_value)

    exact_fraction = loci.record_configuration(
        (("value", Fraction(1, 10)),)
    )
    nearby_fraction = loci.record_configuration(
        (("value", Fraction(10000000000000001, 100000000000000000)),)
    )
    rendered_fraction = loci.record_configuration((("value", "1/10"),))
    assert not loci.semantic_equal(exact_fraction, nearby_fraction)
    assert not loci.semantic_equal(exact_fraction, rendered_fraction)


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
    assert sorted(
        item.mass for item in result.applied_atom_measure.measure.masses
    ) == [Fraction(1, 3), Fraction(2, 3)]


def test_fresh_witness_scope_is_quotiented_by_declared_alpha_identity() -> None:
    contract = loci.CarrierContract(
        loci.CarrierKind.RECORD,
        rank=0,
        shape=(),
        identity_law=loci.ConfigurationIdentityLaw.BOUND_FRESH_ALPHA,
    )
    carrier = loci.Carrier(
        contract,
        loci.Boundary(loci.BoundaryPolicy.NONE),
    )
    parent = loci.named("parent", scope="record")
    source = loci.FiniteConfiguration(carrier, ((parent, False),))
    reference = loci.fresh_reference(
        "children",
        "child",
        parent=parent,
    )
    writable = frontiers.fresh(
        loci.literal(fresh=(reference,)),
        namespace=frontiers.FreshNamespace("children", parent),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    atoms = tuple(
        derivation(
            witness,
            existing=(),
            fresh=(rules.create(reference, True),),
        )
        for witness in ("alpha-left", "alpha-right")
    )
    alphabet = alphabets.boolean()
    simple_program = ca.SimpleProgram(
        seeds.exact(source),
        alphabet,
        writable,
        readable,
        rules.finite_rule(
            atoms,
            contract=rule_contract(
                source,
                alphabet,
                writable,
                readable,
            ),
        ),
    )

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationComplete)
    applied = result.applied_atoms.atoms
    assert len(applied) == 2
    assert all(isinstance(item, program.AppliedDerivation) for item in applied)
    left, right = applied
    assert isinstance(left, program.AppliedDerivation)
    assert isinstance(right, program.AppliedDerivation)
    assert left.fresh_bindings[0].identity != right.fresh_bindings[0].identity
    assert loci.configuration_equal(left.successor, right.successor)
    quotient = result.successor_quotient_with_derivation_fibers.atoms
    assert len(quotient) == 1
    assert {
        item.source.witness.identity for item in quotient[0].derivations
    } == {"alpha-left", "alpha-right"}
