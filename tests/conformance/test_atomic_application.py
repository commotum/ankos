"""CT04: atomic reconstruction and preserve-outside semantics."""

import pytest

import ca
from ca import alphabets, frontiers, loci, neighborhoods, program, rules, seeds

from g7_fixtures import certificate, derivation, rule_contract


def _literal_program(
    configuration,
    writable,
    readable,
    atom,
    *,
    alphabet=None,
):
    if alphabet is None:
        alphabet = alphabets.boolean()
    rule = rules.finite_rule(
        (atom,),
        contract=rule_contract(
            configuration,
            alphabet,
            writable,
            readable,
        ),
    )
    return ca.SimpleProgram(
        seeds.exact(configuration, value_profile=alphabet.value_profile),
        alphabet,
        writable,
        readable,
        rule,
    )


def test_coupled_effects_commit_from_one_old_snapshot() -> None:
    source = loci.record_configuration((("left", False), ("right", True)))
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    rule = rules.expression(
        rules.ExistingPlan(
            rules.ExistingPlanKind.BY_INDEX,
            (rules.observation(1), rules.observation(0)),
        ),
        contract=rule_contract(source, alphabets.boolean(), writable, readable),
        witness=rules.literal_expr("swap-one-old-snapshot"),
        provenance=("test:atomic-swap",),
    )
    simple_program = ca.SimpleProgram(
        seeds.exact(source),
        alphabets.boolean(),
        writable,
        readable,
        rule,
    )

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationComplete)
    successor = result.successor_quotient_with_derivation_fibers.atoms[0].successor
    assert tuple(successor.entries) == (
        (loci.named("left", scope="record"), True),
        (loci.named("right", scope="record"), False),
    )
    assert tuple(value for _, value in source.entries) == (False, True)


def test_birth_deletion_and_interface_effects_are_explicit() -> None:
    source = loci.record_configuration((("keep", True), ("parent", False)))
    parent = loci.named("parent", scope="record")
    fresh_reference = loci.fresh_reference(
        "children",
        "child-a",
        parent=parent,
        interface_loci=(parent,),
    )
    existing = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
        effects=(frontiers.Effect.REPLACE, frontiers.Effect.DELETE),
    )
    fresh = frontiers.fresh(
        loci.literal(fresh=(fresh_reference,)),
        namespace=frontiers.FreshNamespace("children", parent),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    writable = frontiers.union((existing, fresh))
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    existing_actions = tuple(
        rules.preserve(target)
        if target.path[-1] == "keep"
        else rules.delete(target)
        for target, _ in source.entries
    )
    atom = derivation(
        "delete-parent-create-child",
        existing=existing_actions,
        fresh=(rules.create(fresh_reference, True),),
    )
    simple_program = _literal_program(source, writable, readable, atom)

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationComplete)
    applied = result.applied_atoms.atoms[0]
    assert isinstance(applied, program.AppliedDerivation)
    assert len(applied.fresh_bindings) == 1
    successor = applied.successor
    assert not successor.contains(parent)
    assert successor.contains(loci.named("keep", scope="record"))
    assert successor.contains(applied.fresh_bindings[0].identity)
    assert successor.structure == source.structure


def test_every_successor_preserves_outside_and_reconstructs_inside_w() -> None:
    source = loci.record_configuration(
        (("outside-a", False), ("target", False), ("outside-b", True))
    )
    target = loci.named("target", scope="record")
    writable = frontiers.literal(
        (target,),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    readable = neighborhoods.literal(
        (target,),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    atom = derivation(
        "replace-target",
        existing=(rules.replace(target, True),),
    )
    simple_program = _literal_program(source, writable, readable, atom)

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationComplete)
    successor = result.applied_atoms.atoms[0].successor
    assert successor.value_at(loci.named("outside-a", scope="record")) is False
    assert successor.value_at(loci.named("outside-b", scope="record")) is True
    assert successor.value_at(target) is True


def test_missing_unauthorized_conflicting_or_invalid_effect_rejects_all() -> None:
    source = loci.record_configuration((("cell", False),))
    target = source.entries[0][0]
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
        )


def test_overlapping_incompatible_write_capabilities_reject_before_commit() -> None:
    source = loci.record_configuration((("cell", False),))
    target = source.entries[0][0]
    current = frontiers.literal(
        (target,),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
        frame=frontiers.WriteFrame.CURRENT,
    )
    successor = frontiers.literal(
        (target,),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
        frame=frontiers.WriteFrame.SUCCESSOR,
    )
    writable = frontiers.union((current, successor))
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    simple_program = _literal_program(
        source,
        writable,
        readable,
        derivation(
            "overlapping-write-contracts",
            existing=(rules.replace(target, True),),
        ),
    )
    before = source.identity

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationRejected)
    assert result.fault.phase is program.ApplicationPhase.FRONTIER
    assert "overlapping writable parts" in result.fault.reason
    assert source.identity == before
    assert not hasattr(result, "applied_atoms")


def test_changed_quiescent_successor_rejects_after_atomic_reconstruction() -> None:
    source = loci.record_configuration((("cell", False),))
    target = source.entries[0][0]
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    atom = derivation(
        "invalid-quiescent-change",
        existing=(rules.replace(target, True),),
        progress=rules.Progress.QUIESCENT,
        continuation=rules.Continue(),
    )
    simple_program = _literal_program(source, writable, readable, atom)
    before = source.identity

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationRejected)
    assert result.fault.phase is program.ApplicationPhase.SUCCESSOR
    assert "Quiescent derivation changed" in result.fault.reason
    assert source.identity == before
    assert not hasattr(result, "applied_atoms")

    unauthorized = derivation(
        "unauthorized-delete",
        existing=(rules.delete(target),),
    )
    result = ca.apply(
        _literal_program(source, writable, readable, unauthorized),
        source,
    )
    assert isinstance(result, program.ApplicationRejected)
    assert result.fault.phase is program.ApplicationPhase.RESULT_VALIDATION

    missing = derivation("missing", existing=())
    result = ca.apply(_literal_program(source, writable, readable, missing), source)
    assert isinstance(result, program.ApplicationRejected)

    invalid = derivation(
        "invalid-alphabet-value",
        existing=(rules.replace(target, 2),),
    )
    result = ca.apply(_literal_program(source, writable, readable, invalid), source)
    assert isinstance(result, program.ApplicationRejected)

    with pytest.raises(ValueError, match="duplicate"):
        rules.TotalDisposition(
            (rules.preserve(target), rules.replace(target, True)),
            (),
            certificate(rules.CertificateKind.TOTALITY, "conflicting"),
        )
