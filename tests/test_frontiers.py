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
    assert product.resolve(source).targets == tuple(
        target for target, _ in source.entries
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
