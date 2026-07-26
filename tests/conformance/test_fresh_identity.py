"""CT07: deterministic fresh structural identities."""

import pytest

import ca
from ca import alphabets, frontiers, loci, neighborhoods, program, rules, seeds

from g7_fixtures import derivation, rule_contract


def _binding(reference: loci.FreshReference) -> loci.Locus:
    return loci.bind_fresh(
        reference,
        input_configuration_identity="configuration",
        canonical_rule_identity="rule",
        witness_identity="witness",
    )


def _fresh_program():
    source = loci.record_configuration((("parent", False),))
    parent = source.entries[0][0]
    references = (
        loci.fresh_reference("children", "left", parent=parent),
        loci.fresh_reference("children", "right", parent=parent),
    )
    writable = frontiers.fresh(
        loci.literal(fresh=references),
        namespace=frontiers.FreshNamespace("children", parent),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    atom = derivation(
        "two-births",
        existing=(),
        fresh=tuple(rules.create(reference, True) for reference in references),
    )
    alphabet = alphabets.boolean()
    rule = rules.finite_rule(
        (atom,),
        contract=rule_contract(source, alphabet, writable, readable),
    )
    return (
        ca.SimpleProgram(
            seeds.exact(source),
            alphabet,
            writable,
            readable,
            rule,
        ),
        source,
        references,
    )


def test_same_scope_and_local_key_bind_the_same_identity() -> None:
    reference = loci.fresh_reference("children", "same")

    assert _binding(reference) == _binding(reference)
    assert _binding(reference).kind is loci.LocusKind.FRESH


def test_distinct_authorized_local_keys_bind_distinct_identities() -> None:
    left = loci.fresh_reference("children", "left")
    right = loci.fresh_reference("children", "right")

    assert _binding(left) != _binding(right)
    assert len({_binding(left), _binding(right)}) == 2


def test_binding_is_independent_of_traversal_workers_and_unrelated_allocations() -> None:
    reference = loci.fresh_reference("children", 7)
    expected = _binding(reference)

    unrelated = tuple(
        _binding(loci.fresh_reference("other", index))
        for index in range(50)
    )

    assert len(set(unrelated)) == 50
    assert _binding(reference) == expected


def test_unauthorized_namespace_parent_or_collision_rejects_without_commit() -> None:
    source = loci.record_configuration((("parent", False),))
    absent_parent = loci.named("absent", scope="record")
    reference = loci.fresh_reference(
        "children",
        "child",
        parent=absent_parent,
    )
    writable = frontiers.fresh(
        loci.literal(fresh=(reference,)),
        namespace=frontiers.FreshNamespace("children"),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    with pytest.raises(frontiers.WritableResolutionError, match="parent"):
        writable.resolve(source)

    duplicate = loci.fresh_reference(
        "children",
        "same",
        parent=source.entries[0][0],
    )
    with pytest.raises(ValueError, match="duplicate fresh"):
        loci.literal(fresh=(duplicate, duplicate))
    assert len(source.entries) == 1


def test_raw_bindings_remain_available_before_alpha_equivalence() -> None:
    simple_program, source, references = _fresh_program()

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationComplete)
    applied = result.applied_atoms.atoms[0]
    assert isinstance(applied, program.AppliedDerivation)
    assert tuple(binding.reference for binding in applied.fresh_bindings) == references
    assert len({binding.identity for binding in applied.fresh_bindings}) == 2
    fiber = result.successor_quotient_with_derivation_fibers.atoms[0]
    assert fiber.derivations[0].fresh_bindings == applied.fresh_bindings


def test_created_values_bind_same_derivation_structural_references() -> None:
    source_value = alphabets.ValueNode(
        alphabets.ValueKind.GRAPH,
        "root-node",
    )
    source = loci.record_configuration((("root", source_value),))
    parent = source.entries[0][0]
    references = (
        loci.fresh_reference("graph-patch", "left", parent=parent),
        loci.fresh_reference("graph-patch", "right", parent=parent),
        loci.FreshReference(
            "graph-patch",
            "edge",
            parent=parent,
            interface=(parent,),
        ),
    )
    writable = frontiers.fresh(
        loci.literal(fresh=references),
        namespace=frontiers.FreshNamespace("graph-patch", parent),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.STRUCTURAL,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.STRUCTURAL,
    )
    node = alphabets.ValueNode(alphabets.ValueKind.GRAPH, "node")
    edge = alphabets.ValueNode(
        alphabets.ValueKind.GRAPH,
        "edge",
        items=(
            alphabets.StructuralReference(references[0]),
            alphabets.StructuralReference(references[1]),
        ),
    )
    atom = derivation(
        "graph-patch",
        existing=(),
        fresh=(
            rules.create(references[0], node),
            rules.create(references[1], node),
            rules.create(references[2], edge),
        ),
    )
    alphabet = alphabets.graph()
    rule = rules.finite_rule(
        (atom,),
        contract=rule_contract(source, alphabet, writable, readable),
    )
    simple_program = ca.SimpleProgram(
        seeds.exact(
            source,
            value_profile=alphabets.ValueProfile.STRUCTURAL,
        ),
        alphabet,
        writable,
        readable,
        rule,
    )

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationComplete)
    applied = result.applied_atoms.atoms[0]
    assert isinstance(applied, program.AppliedDerivation)
    bound = {
        binding.reference: binding.identity for binding in applied.fresh_bindings
    }
    edge_identity = bound[references[2]]
    edge_value = applied.successor.value_at(edge_identity)
    assert isinstance(edge_value, alphabets.ValueNode)
    assert edge_value.items == (
        alphabets.StructuralReference(bound[references[0]]),
        alphabets.StructuralReference(bound[references[1]]),
    )
    assert all(
        isinstance(item, alphabets.StructuralReference) and item.is_bound
        for item in edge_value.items
    )
