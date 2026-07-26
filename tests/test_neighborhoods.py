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
        (neighborhoods.ar2_0d, (("ar2", 2),)),
        (
            neighborhoods.dyadlags_0d,
            (("older", 1), ("previous", 1), ("current", 1)),
        ),
        (
            neighborhoods.lagcounts_0d,
            (("history", 1), ("recent", 3), ("middle", 3), ("oldest", 3)),
        ),
        (
            neighborhoods.dyadrads_1d,
            (("self", 1), ("primary", 2), ("secondary", 2)),
        ),
        (
            neighborhoods.dyadaxes_2d,
            (("self", 1), ("primary", 4), ("secondary", 4)),
        ),
        (
            neighborhoods.dyadaxes_3d,
            (("self", 1), ("primary", 6), ("secondary", 20)),
        ),
    ),
)
def test_retained_native_presets_publish_exact_rule_facing_shapes(
    factory,
    fields: tuple[tuple[str, int], ...],
) -> None:
    region = factory()

    assert tuple(
        (
            field.key,
            1 if field.arity is neighborhoods.ReadArity.ONE else field.size,
        )
        for field in region.result_shape.fields
    ) == fields
    assert all(
        field.arity is not neighborhoods.ReadArity.VARIABLE
        for field in region.result_shape.fields
    )
    assert isinstance(region, neighborhoods.ReadableRegion)


@pytest.mark.parametrize(
    ("region", "source", "sizes"),
    (
        (
            neighborhoods.dyadlags_0d(),
            loci.history_configuration((True, False, True)),
            (1, 1, 1),
        ),
        (
            neighborhoods.lagcounts_0d(),
            loci.history_configuration(
                (True, False, True, False, True, False, True, False, True, False)
            ),
            (1, 3, 3, 3),
        ),
        (
            neighborhoods.dyadrads_1d(),
            loci.grid_configuration(
                (5,),
                (False,) * 5,
                boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
            ),
            (1, 2, 2),
        ),
        (
            neighborhoods.dyadaxes_2d(),
            loci.grid_configuration(
                (3, 3),
                (False,) * 9,
                boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
            ),
            (1, 4, 4),
        ),
        (
            neighborhoods.dyadaxes_3d(),
            loci.grid_configuration(
                (3, 3, 3),
                (False,) * 27,
                boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
            ),
            (1, 6, 20),
        ),
    ),
)
def test_native_resolved_groups_match_declared_field_arities(
    region,
    source,
    sizes: tuple[int, ...],
) -> None:
    view = region.resolve(source)
    groups_by_anchor = {}
    for group in view.groups:
        groups_by_anchor.setdefault(group.anchor, []).append(group)

    assert all(
        tuple(len(group.indices) for group in groups) == sizes
        for groups in groups_by_anchor.values()
    )


def test_lagcount_shape_tracks_the_requested_band_size() -> None:
    region = neighborhoods.lagcounts_0d(band_size=2)
    source = loci.history_configuration(
        (True, False, True, False, True, False, True)
    )

    assert tuple(
        1 if field.arity is neighborhoods.ReadArity.ONE else field.size
        for field in region.result_shape.fields
    ) == (1, 2, 2, 2)
    assert tuple(len(group.indices) for group in region.resolve(source).groups) == (
        1,
        2,
        2,
        2,
    )
    with pytest.raises(neighborhoods.ReadableResolutionError):
        neighborhoods.lagcounts_0d(band_count=2)


def test_neighborhood_grants_no_write_authority() -> None:
    region = neighborhoods.global_view(
        value_profile=alphabets.ValueProfile.BOOLEAN
    )

    assert not hasattr(region, "effects")
    assert not hasattr(region, "commit")
    assert not hasattr(region, "write")
