"""Unit tests for identity-preserving readable regions."""

import pytest

from ca import alphabets, loci, neighborhoods


def test_literal_view_preserves_target_identity_and_order() -> None:
    source = loci.record_configuration((("a", 1), ("b", 2)))
    targets = tuple(target for target, _ in source.entries)
    region = neighborhoods.literal(
        targets,
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.INTEGER,
    )

    view = region.resolve(source)

    assert view.snapshot_identity == source.identity
    assert tuple(item.target for item in view.observations) == targets
    assert tuple(item.value for item in view.observations) == (1, 2)
    assert all(
        isinstance(item.state, neighborhoods.Present)
        for item in view.observations
    )
    assert view.groups[0].indices == (0, 1)


def test_relative_view_distinguishes_present_boundary_default_and_absent() -> None:
    fixed = loci.grid_configuration(
        (3,),
        (False, True, False),
        boundary=loci.Boundary(loci.BoundaryPolicy.FIXED, False),
    )
    no_boundary = loci.grid_configuration(
        (3,),
        (False, True, False),
        boundary=loci.Boundary(loci.BoundaryPolicy.NONE),
    )
    region = neighborhoods.eca(configuration_contract=fixed.contract)

    fixed_view = region.resolve(fixed)
    absent_view = region.resolve(no_boundary)

    assert any(
        isinstance(item.state, neighborhoods.Present)
        for item in fixed_view.observations
    )
    assert any(
        isinstance(item.state, neighborhoods.BoundaryDefault)
        for item in fixed_view.observations
    )
    assert any(
        isinstance(item.state, neighborhoods.Absent)
        for item in absent_view.observations
    )
    with pytest.raises(neighborhoods.ReadableResolutionError):
        next(
            item
            for item in absent_view.observations
            if isinstance(item.state, neighborhoods.Absent)
        ).value


def test_relative_groups_join_by_anchor_identity() -> None:
    source = loci.grid_configuration(
        (3,),
        (False, True, False),
        boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
    )
    view = neighborhoods.eca(configuration_contract=source.contract).resolve(
        source
    )

    assert len(view.groups) == 3
    assert all(len(group.indices) == 3 for group in view.groups)
    assert tuple(group.anchor for group in view.groups) == loci.grid_loci((3,))
    assert view.join_shape.mode is neighborhoods.JoinMode.ANCHOR_IDENTITY


def test_product_preserves_field_group_boundaries_and_channels() -> None:
    source = loci.grid_configuration(
        (3,),
        (False, True, False),
        boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
    )
    contract = source.contract
    product = neighborhoods.product(
        (
            (
                "self",
                neighborhoods.grid_relative(
                    ((0,),),
                    configuration_contract=contract,
                    value_profile=alphabets.ValueProfile.BOOLEAN,
                ),
            ),
            (
                "sides",
                neighborhoods.grid_relative(
                    ((-1,), (1,)),
                    configuration_contract=contract,
                    value_profile=alphabets.ValueProfile.BOOLEAN,
                ),
            ),
        )
    )

    view = product.resolve(source)

    assert product.join_shape.mode is neighborhoods.JoinMode.PRODUCT
    assert len(view.groups) == 6
    for anchor in loci.grid_loci((3,)):
        assert {
            group.key.channel for group in view.groups if group.anchor == anchor
        } == {0, 1}


@pytest.mark.parametrize(
    ("factory", "fields"),
    (
        (neighborhoods.ar2_0d, ("ar2",)),
        (
            neighborhoods.dyadlags_0d,
            ("older", "previous", "current"),
        ),
        (
            neighborhoods.lagcounts_0d,
            ("history", "recent", "middle", "oldest"),
        ),
        (
            neighborhoods.dyadrads_1d,
            ("self", "primary", "secondary"),
        ),
        (
            neighborhoods.dyadaxes_2d,
            ("self", "primary", "secondary"),
        ),
        (
            neighborhoods.dyadaxes_3d,
            ("self", "primary", "secondary"),
        ),
    ),
)
def test_retained_native_presets_publish_exact_rule_facing_shapes(
    factory,
    fields: tuple[str, ...],
) -> None:
    region = factory()

    assert tuple(field.key for field in region.result_shape.fields) == fields
    assert isinstance(region, neighborhoods.ReadableRegion)


def test_neighborhood_grants_no_write_authority() -> None:
    region = neighborhoods.global_view(
        value_profile=alphabets.ValueProfile.BOOLEAN
    )

    assert not hasattr(region, "effects")
    assert not hasattr(region, "commit")
    assert not hasattr(region, "write")
