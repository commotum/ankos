"""Unit tests for writable capability envelopes."""

import pytest

from ca import alphabets, frontiers, loci


def _source():
    return loci.record_configuration((("a", False), ("b", True)))


def test_writable_region_resolves_the_complete_possible_write_envelope() -> None:
    source = _source()
    region = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
        effects=(frontiers.Effect.REPLACE, frontiers.Effect.DELETE),
    )

    resolved = region.resolve(source)

    assert resolved.snapshot_identity == source.identity
    assert tuple(item.target for item in resolved.existing) == tuple(
        target for target, _ in source.entries
    )
    assert all(
        item.effects
        == (frontiers.Effect.REPLACE, frontiers.Effect.DELETE)
        for item in resolved.existing
    )
    assert resolved.reconstruction.preserves_outside
    assert resolved.reconstruction.complete


def test_effect_profile_has_one_canonical_permission_order() -> None:
    profile = frontiers.EffectProfile(
        existing=(frontiers.Effect.DELETE, frontiers.Effect.REPLACE),
    )

    assert profile.existing == (
        frontiers.Effect.REPLACE,
        frontiers.Effect.DELETE,
    )
    assert profile == frontiers.EffectProfile(
        existing=(frontiers.Effect.REPLACE, frontiers.Effect.DELETE),
    )


def test_writable_region_distinguishes_existing_and_fresh_capabilities() -> None:
    source = _source()
    parent = source.entries[0][0]
    reference = loci.fresh_reference("children", "child", parent=parent)
    existing = frontiers.literal(
        (parent,),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    fresh = frontiers.fresh(
        loci.literal(fresh=(reference,)),
        namespace=frontiers.FreshNamespace("children", parent),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    combined = frontiers.union((existing, fresh)).resolve(source)

    assert tuple(item.target for item in combined.existing) == (parent,)
    assert tuple(item.target for item in combined.fresh) == (reference,)
    assert combined.existing[0].effects == (frontiers.Effect.REPLACE,)
    assert combined.fresh[0].namespace.namespace == "children"


def test_writable_region_composition_returns_one_component() -> None:
    source = _source()
    parts = tuple(
        (
            target.path[-1],
            frontiers.literal(
                (target,),
                configuration_contract=source.contract,
                value_profile=alphabets.ValueProfile.BOOLEAN,
            ),
        )
        for target, _ in source.entries
    )

    product = frontiers.product(parts)

    assert isinstance(product, frontiers.WritableRegion)
    assert product.descriptor.kind is loci.RegionKind.PRODUCT
    assert tuple(part.name for part in product.descriptor.parts) == ("a", "b")
    assert product.resolve(source).targets == tuple(
        target for target, _ in source.entries
    )


def test_target_kind_and_fresh_namespace_are_checked_without_barring_bound_births() -> None:
    bound_birth = loci.Locus(loci.LocusKind.FRESH, "children", ("child",))
    capability = frontiers.ExistingCapability(
        bound_birth,
        frontiers.TargetContract(
            loci.LocusKind.FRESH,
            alphabets.ValueProfile.BOOLEAN,
        ),
        (frontiers.Effect.REPLACE,),
    )

    assert capability.target is bound_birth
    with pytest.raises(frontiers.WritableResolutionError, match="target kind"):
        frontiers.ExistingCapability(
            loci.named("cell"),
            frontiers.TargetContract(
                loci.LocusKind.COORDINATE,
                alphabets.ValueProfile.BOOLEAN,
            ),
            (frontiers.Effect.REPLACE,),
        )
    with pytest.raises(frontiers.WritableResolutionError, match="namespace"):
        frontiers.FreshCapability(
            loci.fresh_reference("other", "child"),
            frontiers.TargetContract(
                loci.LocusKind.FRESH,
                alphabets.ValueProfile.BOOLEAN,
            ),
            frontiers.FreshNamespace("children"),
        )


def test_frontier_grants_no_implicit_read_authority() -> None:
    source = _source()
    resolved = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    ).resolve(source)

    assert all(not hasattr(item, "value") for item in resolved.existing)
    assert not hasattr(resolved, "observations")
    assert not hasattr(resolved, "read")


def test_frontier_does_not_select_firing_sites_or_conflict_winners() -> None:
    region = frontiers.everywhere(
        value_profile=alphabets.ValueProfile.BOOLEAN
    )

    assert not hasattr(region, "schedule")
    assert not hasattr(region, "applicability")
    assert not hasattr(region, "winner")
    with pytest.raises(frontiers.WritableResolutionError):
        region.resolve(object())


def test_heterogeneous_union_preserves_each_target_contract_and_effect() -> None:
    source = _source()
    a, b = tuple(target for target, _ in source.entries)
    current_delete = frontiers.literal(
        (a,),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
        effects=(frontiers.Effect.DELETE,),
        frame=frontiers.WriteFrame.CURRENT,
    )
    successor_replace = frontiers.literal(
        (b,),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
        effects=(frontiers.Effect.REPLACE,),
        frame=frontiers.WriteFrame.SUCCESSOR,
    )

    combined = frontiers.union((successor_replace, current_delete))
    resolved = combined.resolve(source)
    by_target = {capability.target: capability for capability in resolved.existing}

    assert combined.parts
    assert by_target[a].effects == (frontiers.Effect.DELETE,)
    assert by_target[a].contract.frame is frontiers.WriteFrame.CURRENT
    assert by_target[b].effects == (frontiers.Effect.REPLACE,)
    assert by_target[b].contract.frame is frontiers.WriteFrame.SUCCESSOR
    assert combined.effect_profile.existing == (
        frontiers.Effect.REPLACE,
        frontiers.Effect.DELETE,
    )


def test_dynamic_fresh_union_supports_multiple_namespaces() -> None:
    source = _source()
    a, b = tuple(target for target, _ in source.entries)
    children = frontiers.dynamic_fresh(
        loci.fresh_children_dynamic(
            loci.literal((a, b)),
            "children",
            ("child",),
        ),
        namespace=frontiers.FreshNamespace("children"),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    edges = frontiers.dynamic_fresh(
        loci.fresh_edges_dynamic(
            (loci.literal((a,)), loci.literal((b,))),
            "edges",
            ("edge",),
        ),
        namespace=frontiers.FreshNamespace("edges"),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )

    combined = frontiers.union((children, edges))
    resolved = combined.resolve(source)

    assert combined.fresh_namespace is None
    assert tuple(
        namespace.namespace for namespace in combined.fresh_namespaces
    ) == ("children", "edges")
    assert {
        capability.namespace.namespace for capability in resolved.fresh
    } == {"children", "edges"}
    assert {
        capability.target.parent
        for capability in resolved.fresh
        if capability.namespace.namespace == "children"
    } == {a, b}
    assert {
        capability.target.interface
        for capability in resolved.fresh
        if capability.namespace.namespace == "edges"
    } == {(a, b)}


def test_union_merges_overlapping_permissions_without_losing_part_data() -> None:
    source = _source()
    target = source.entries[0][0]
    replace = frontiers.literal(
        (target,),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    delete = frontiers.literal(
        (target,),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
        effects=(frontiers.Effect.DELETE,),
    )

    combined = frontiers.union((delete, replace))
    resolved = combined.resolve(source)

    assert len(combined.descriptor.parts) == 1
    assert len(combined.parts) == 2
    assert resolved.existing[0].effects == (
        frontiers.Effect.REPLACE,
        frontiers.Effect.DELETE,
    )


def test_dynamic_fresh_template_may_resolve_no_current_capabilities() -> None:
    source = _source()
    dynamic = frontiers.dynamic_fresh(
        loci.fresh_children_dynamic(
            loci.literal((loci.named("absent", scope="record"),)),
            "children",
            ("child",),
        ),
        namespace=frontiers.FreshNamespace("children"),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )

    resolved = dynamic.resolve(source)

    assert resolved.fresh == ()
    assert resolved.targets == ()
