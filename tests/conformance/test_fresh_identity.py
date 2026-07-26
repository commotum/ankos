"""CT07: deterministic fresh structural identities."""

from concurrent.futures import ThreadPoolExecutor

import pytest

import ca
from ca import alphabets, frontiers, loci, neighborhoods, program, rules, seeds

from g7_fixtures import certificate, derivation, rule_contract


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
    references = tuple(
        loci.fresh_reference("children", index)
        for index in range(12)
    )
    expected = tuple(_binding(reference) for reference in references)

    unrelated = tuple(
        _binding(loci.fresh_reference("other", index))
        for index in range(50)
    )
    reverse = tuple(
        reversed(
            tuple(_binding(reference) for reference in reversed(references))
        )
    )
    lazy = tuple(map(_binding, references))
    with ThreadPoolExecutor(max_workers=1) as one_worker:
        serial_worker = tuple(one_worker.map(_binding, references))
    with ThreadPoolExecutor(max_workers=4) as four_workers:
        parallel_worker = tuple(four_workers.map(_binding, references))

    assert len(set(unrelated)) == 50
    assert reverse == expected
    assert lazy == expected
    assert serial_worker == expected
    assert parallel_worker == expected


def test_every_fresh_scope_input_contributes_to_the_bound_identity() -> None:
    parent_a = loci.named("a", scope="record")
    parent_b = loci.named("b", scope="record")
    base = loci.fresh_reference(
        "children",
        "local",
        parent=parent_a,
        interface_loci=(parent_a,),
    )

    def bind(
        reference: loci.FreshReference = base,
        *,
        input_identity: str = "configuration",
        rule_identity: str = "rule",
        witness_identity: str = "witness",
    ) -> loci.Locus:
        return loci.bind_fresh(
            reference,
            input_configuration_identity=input_identity,
            canonical_rule_identity=rule_identity,
            witness_identity=witness_identity,
        )

    variants = (
        bind(),
        bind(input_identity="other-configuration"),
        bind(rule_identity="other-rule"),
        bind(witness_identity="other-witness"),
        bind(
            loci.fresh_reference(
                "other-namespace",
                "local",
                parent=parent_a,
                interface_loci=(parent_a,),
            )
        ),
        bind(
            loci.fresh_reference(
                "children",
                "other-local",
                parent=parent_a,
                interface_loci=(parent_a,),
            )
        ),
        bind(
            loci.fresh_reference(
                "children",
                "local",
                parent=parent_b,
                interface_loci=(parent_a,),
            )
        ),
        bind(
            loci.fresh_reference(
                "children",
                "local",
                parent=parent_a,
                interface_loci=(parent_b,),
            )
        ),
    )

    assert len(set(variants)) == len(variants)


@pytest.mark.parametrize(
    ("reference", "namespace", "reason"),
    (
        (
            loci.fresh_reference("wrong", "child"),
            frontiers.FreshNamespace("children"),
            "namespace",
        ),
        (
            loci.fresh_reference(
                "children",
                "child",
                parent=loci.named("absent", scope="record"),
            ),
            frontiers.FreshNamespace("children"),
            "parent",
        ),
    ),
)
def test_unauthorized_namespace_or_parent_rejects_application_without_commit(
    reference: loci.FreshReference,
    namespace: frontiers.FreshNamespace,
    reason: str,
) -> None:
    source = loci.record_configuration((("parent", False),))
    writable = frontiers.fresh(
        loci.literal(fresh=(reference,)),
        namespace=namespace,
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    alphabet = alphabets.boolean()
    atom = derivation(
        f"invalid-{reason}",
        existing=(),
        fresh=(rules.create(reference, True),),
    )
    simple_program = ca.SimpleProgram(
        seeds.exact(source),
        alphabet,
        writable,
        readable,
        rules.finite_rule(
            (atom,),
            contract=rule_contract(
                source,
                alphabet,
                writable,
                readable,
            ),
        ),
    )
    before = source.identity

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationRejected)
    assert result.fault.phase is program.ApplicationPhase.FRONTIER
    assert reason in result.fault.reason
    assert source.identity == before
    assert not hasattr(result, "applied_atoms")


def test_duplicate_reference_is_rejected_before_application() -> None:
    source = loci.record_configuration((("parent", False),))
    duplicate = loci.fresh_reference(
        "children",
        "same",
        parent=source.entries[0][0],
    )
    with pytest.raises(ValueError, match="duplicate fresh"):
        loci.literal(fresh=(duplicate, duplicate))
    assert len(source.entries) == 1


def test_fresh_collision_rejects_application_without_commit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    simple_program, source, _ = _fresh_program()
    collided = loci.Locus(loci.LocusKind.FRESH, "collision", ("same",))
    before = source.identity
    monkeypatch.setattr(loci, "bind_fresh", lambda *args, **kwargs: collided)

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationRejected)
    assert result.fault.phase is program.ApplicationPhase.FRESH_BINDING
    assert "fresh bindings collide" in result.fault.reason
    assert source.identity == before
    assert not hasattr(result, "applied_atoms")


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


def test_trace_lineage_does_not_change_denotation_or_fresh_identity() -> None:
    simple_program, source, _ = _fresh_program()
    left_lineage = program.TraceLineage("left-root")
    right_lineage = program.TraceLineage("right-root")

    left = ca.apply(
        simple_program,
        program.ApplicationInput(source, left_lineage),
    )
    right = ca.apply(
        simple_program,
        program.ApplicationInput(source, right_lineage),
    )

    assert isinstance(left, program.ApplicationComplete)
    assert isinstance(right, program.ApplicationComplete)
    assert left.source_outcomes == right.source_outcomes
    left_atom = left.applied_atoms.atoms[0]
    right_atom = right.applied_atoms.atoms[0]
    assert isinstance(left_atom, program.AppliedDerivation)
    assert isinstance(right_atom, program.AppliedDerivation)
    assert left_atom.fresh_bindings == right_atom.fresh_bindings
    assert left_atom.successor == right_atom.successor
    assert left_atom.input_trace_lineage != right_atom.input_trace_lineage
    assert left_atom.output_trace_lineage != right_atom.output_trace_lineage


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


def test_unbound_structural_reference_rejects_at_commit() -> None:
    target = loci.named("root", scope="record")
    carrier = loci.Carrier(
        loci.CarrierContract(loci.CarrierKind.RECORD, rank=0, shape=()),
        loci.Boundary(loci.BoundaryPolicy.NONE),
    )
    source = loci.FiniteConfiguration(
        carrier,
        ((target, alphabets.StructuralReference(target)),),
    )
    unbound = loci.fresh_reference("missing", "child")
    alphabet = alphabets.structural_references()
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.STRUCTURAL,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.STRUCTURAL,
    )
    atom = derivation(
        "unbound-value-reference",
        existing=(
            rules.replace(
                target,
                alphabets.StructuralReference(unbound),
            ),
        ),
    )
    simple_program = ca.SimpleProgram(
        seeds.exact(
            source,
            value_profile=alphabets.ValueProfile.STRUCTURAL,
        ),
        alphabet,
        writable,
        readable,
        rules.finite_rule(
            (atom,),
            contract=rule_contract(
                source,
                alphabet,
                writable,
                readable,
            ),
        ),
    )

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationRejected)
    assert result.fault.phase is program.ApplicationPhase.COMMIT
    assert result.fault.attempted_phases[-1] is program.ApplicationPhase.COMMIT
    assert "unbound fresh reference" in result.fault.reason
    assert source.entries == (
        (target, alphabets.StructuralReference(target)),
    )


def test_dynamic_fresh_frontier_is_resolved_for_each_application_input() -> None:
    carrier = loci.Carrier(
        loci.CarrierContract(loci.CarrierKind.RECORD, rank=0, shape=()),
        loci.Boundary(loci.BoundaryPolicy.NONE),
    )

    def configuration(*names: str) -> loci.FiniteConfiguration[bool]:
        return loci.FiniteConfiguration(
            carrier,
            tuple(
                (loci.named(name, scope="record"), False)
                for name in names
            ),
        )

    first_source = configuration("a")
    second_source = configuration("a", "b")
    alphabet = alphabets.boolean()
    writable = frontiers.dynamic_fresh(
        loci.fresh_children_dynamic(
            loci.all_support(),
            "children",
            ("child",),
        ),
        namespace=frontiers.FreshNamespace("children"),
        configuration_contract=first_source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    readable = neighborhoods.global_view(
        configuration_contract=first_source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    clause_result = rules.DerivationClauseResult(
        existing_plans=(),
        fresh_plans=(
            rules.FreshDispositionPlan(
                rules.every_capability(),
                rules.DispositionAction.CREATE,
                rules.literal_expr(True),
            ),
        ),
        progress=rules.Progress.ADVANCED,
        continuation=rules.Continue(),
        witness=rules.literal_expr("dynamic-fresh"),
        provenance=("test:dynamic-fresh",),
        certificate=certificate(
            rules.CertificateKind.DERIVATION,
            "dynamic-fresh",
        ),
    )
    rule = rules.clause_kernel(
        (
            rules.RuleClause(
                rules.literal_expr(1),
                clause_result,
            ),
        ),
        contract=rule_contract(
            first_source,
            alphabet,
            writable,
            readable,
        ),
        completeness_evidence=certificate(
            rules.CertificateKind.COMPLETENESS,
            "dynamic-fresh",
        ),
    )
    simple_program = ca.SimpleProgram(
        seeds.exact(first_source),
        alphabet,
        writable,
        readable,
        rule,
    )

    first = ca.apply(simple_program, first_source)
    second = ca.apply(simple_program, second_source)

    assert isinstance(first, program.ApplicationComplete)
    assert isinstance(second, program.ApplicationComplete)
    first_applied = first.applied_atoms.atoms[0]
    second_applied = second.applied_atoms.atoms[0]
    assert isinstance(first_applied, program.AppliedDerivation)
    assert isinstance(second_applied, program.AppliedDerivation)
    assert len(first_applied.fresh_bindings) == 1
    assert len(second_applied.fresh_bindings) == 2
    assert {
        binding.reference.parent for binding in first_applied.fresh_bindings
    } == {first_source.entries[0][0]}
    assert {
        binding.reference.parent for binding in second_applied.fresh_bindings
    } == {target for target, _ in second_source.entries}
    assert len(first_applied.successor.entries) == 2
    assert len(second_applied.successor.entries) == 4
