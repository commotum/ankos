"""Unit tests for identity-preserving readable regions."""

from fractions import Fraction

import pytest

from ca import alphabets, frontiers, loci, neighborhoods, rules, seeds


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


def test_readable_view_rejects_duplicate_group_keys() -> None:
    source = loci.record_configuration((("a", 1), ("b", 2)))
    targets = tuple(target for target, _ in source.entries)
    dependency = neighborhoods.ReadDependency(
        "record",
        loci.all_support(),
        None,
        seeds.ExactnessProfile.EXACT,
    )
    observations = tuple(
        neighborhoods.Observation(
            target,
            neighborhoods.Present(source.value_at(target)),
        )
        for target in targets
    )
    duplicate = neighborhoods.GroupKey(None, 0)

    with pytest.raises(
        neighborhoods.ReadableResolutionError,
        match="group keys must be unique",
    ):
        neighborhoods.ReadableView(
            source.identity,
            observations,
            (
                neighborhoods.ObservationGroup(duplicate, (0,)),
                neighborhoods.ObservationGroup(duplicate, (1,)),
            ),
            neighborhoods.JoinShape(neighborhoods.JoinMode.NONE, ()),
            (dependency,),
        )


def test_readable_view_checks_none_group_anchor_against_every_observation() -> None:
    source = loci.record_configuration((("a", 1), ("b", 2)))
    targets = tuple(target for target, _ in source.entries)
    dependency = neighborhoods.ReadDependency(
        "record",
        loci.all_support(),
        None,
        seeds.ExactnessProfile.EXACT,
    )
    observations = (
        neighborhoods.Observation(
            targets[0],
            neighborhoods.Present(1),
        ),
        neighborhoods.Observation(
            targets[1],
            neighborhoods.Present(2),
            anchor=targets[0],
        ),
    )

    with pytest.raises(
        neighborhoods.ReadableResolutionError,
        match="group and observation anchors disagree",
    ):
        neighborhoods.ReadableView(
            source.identity,
            observations,
            (
                neighborhoods.ObservationGroup(
                    neighborhoods.GroupKey(None, 0),
                    (0, 1),
                ),
            ),
            neighborhoods.JoinShape(neighborhoods.JoinMode.NONE, ()),
            (dependency,),
        )


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
        (False, True, True, False, False, True, True)
    )
    view = region.resolve(source)

    assert tuple(
        1 if field.arity is neighborhoods.ReadArity.ONE else field.size
        for field in region.result_shape.fields
    ) == (1, 2, 2, 2)
    assert tuple(len(group.indices) for group in view.groups) == (
        1,
        2,
        2,
        2,
    )
    assert tuple(
        tuple(view.observations[index].value for index in group.indices)
        for group in view.groups
    ) == (
        (True,),
        (False, True),
        (True, False),
        (False, True),
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


def test_metric_and_history_dependencies_materialize_only_selected_values() -> None:
    grid = loci.grid_configuration(
        (5,),
        (0, 1, 2, 3, 4),
        boundary=loci.Boundary(loci.BoundaryPolicy.NONE),
    )
    metric = neighborhoods.metric(
        loci.cell((0,)),
        1,
        configuration_contract=grid.contract,
        value_profile=alphabets.ValueProfile.INTEGER,
    )
    metric_view = metric.resolve(grid)

    assert isinstance(metric_view, neighborhoods.ReadableView)
    assert tuple(
        loci.grid_coordinates(item.target) for item in metric_view.observations
    ) == ((-1,), (0,), (1,))
    assert tuple(item.value for item in metric_view.observations) == (1, 2, 3)
    assert (
        metric_view.dependencies[0].selector.primitive
        is loci.SelectorPrimitive.METRIC
    )

    history = loci.history_configuration((0, 1, 2, 3, 4))
    history_view = neighborhoods.history_dependency(
        1,
        4,
        configuration_contract=history.contract,
        value_profile=alphabets.ValueProfile.INTEGER,
    ).resolve(history)

    assert isinstance(history_view, neighborhoods.ReadableView)
    assert tuple(item.value for item in history_view.observations) == (1, 2, 3)
    assert (
        history_view.dependencies[0].selector.primitive
        is loci.SelectorPrimitive.HISTORY
    )


def test_path_and_matched_interface_dependencies_preserve_structure() -> None:
    tree_contract = loci.CarrierContract(loci.CarrierKind.TREE)
    tree = loci.FiniteConfiguration(
        loci.Carrier(
            tree_contract,
            loci.Boundary(loci.BoundaryPolicy.NONE),
        ),
        (
            (loci.path("other"), 0),
            (loci.path("root"), 1),
            (loci.path("root", "left"), 2),
        ),
    )
    path_view = neighborhoods.path(
        loci.path("root"),
        configuration_contract=tree_contract,
        value_profile=alphabets.ValueProfile.INTEGER,
    ).resolve(tree)

    assert isinstance(path_view, neighborhoods.ReadableView)
    assert tuple(item.value for item in path_view.observations) == (1, 2)
    assert path_view.dependencies[0].region.kind is loci.RegionKind.PATH

    left = loci.graph_element("node", "left")
    right = loci.graph_element("node", "right")
    edge = loci.graph_element("edge", "edge")
    graph_contract = loci.CarrierContract(loci.CarrierKind.GRAPH)
    graph = loci.FiniteConfiguration(
        loci.Carrier(
            graph_contract,
            loci.Boundary(loci.BoundaryPolicy.NONE),
        ),
        ((left, 1), (right, 2), (edge, 3)),
        (loci.StructuralRelation("interface", (left, edge, right)),),
    )
    interface_view = neighborhoods.matched_interface(
        loci.literal((left,)),
        loci.literal((right,)),
        configuration_contract=graph_contract,
        value_profile=alphabets.ValueProfile.INTEGER,
    ).resolve(graph)

    assert isinstance(interface_view, neighborhoods.ReadableView)
    assert tuple(item.target for item in interface_view.observations) == (edge,)
    assert interface_view.observations[0].value == 3
    assert (
        interface_view.dependencies[0].region.kind
        is loci.RegionKind.MATCHED_INTERFACE
    )


def test_field_restriction_and_differential_germ_do_not_hide_reads() -> None:
    field_contract = loci.CarrierContract(loci.CarrierKind.FIELD, rank=1)
    points = tuple(
        loci.field_point("u", (Fraction(coordinate),))
        for coordinate in (-1, 0, 1)
    )
    source = loci.FiniteConfiguration(
        loci.Carrier(
            field_contract,
            loci.Boundary(loci.BoundaryPolicy.NONE),
        ),
        tuple(zip(points, (10, 20, 30))),
    )
    restriction = neighborhoods.field_restriction(
        "u",
        (0, 1),
        configuration_contract=field_contract,
        value_profile=alphabets.ValueProfile.INTEGER,
    )
    finite_view = restriction.resolve(source)

    assert isinstance(finite_view, neighborhoods.ReadableView)
    assert tuple(item.target for item in finite_view.observations) == points[1:]
    assert tuple(item.value for item in finite_view.observations) == (20, 30)

    differential = neighborhoods.differential_germ(
        "u",
        2,
        configuration_contract=field_contract,
        value_profile=alphabets.ValueProfile.INTEGER,
    )
    dependency_view = differential.resolve(source)

    assert isinstance(
        dependency_view,
        neighborhoods.IntensionalReadableView,
    )
    assert dependency_view.observations == ()
    assert dependency_view.groups == ()
    assert (
        dependency_view.dependencies[0].region.kind
        is loci.RegionKind.DIFFERENTIAL
    )
    assert (
        dependency_view.dependencies[0].region.relation.primitive
        is loci.SelectorPrimitive.DIFFERENTIAL_GERM
    )


def test_intensional_read_view_retains_source_and_dependency_relations() -> None:
    source_relation = loci.SelectorExpr(loci.SelectorPrimitive.MEMBERSHIP)
    contract = loci.CarrierContract(loci.CarrierKind.INTENSIONAL)
    source = loci.IntensionalConfiguration(
        contract,
        source_relation,
        "all-real-field-configurations",
    )
    dependency_relation = loci.SelectorExpr(
        loci.SelectorPrimitive.AND,
        children=(
            source_relation,
            loci.SelectorExpr(
                loci.SelectorPrimitive.NOT,
                children=(
                    loci.SelectorExpr(loci.SelectorPrimitive.MEMBERSHIP),
                ),
            ),
        ),
    )
    region = neighborhoods.intensional(
        "field",
        dependency_relation,
        configuration_contract=contract,
        value_profile=alphabets.ValueProfile.EXACT,
    )

    view = region.resolve(source)

    assert isinstance(view, neighborhoods.IntensionalReadableView)
    assert view.snapshot_identity == source.identity
    assert view.configuration_relation == source_relation
    assert view.dependencies[0].region.relation == dependency_relation
    assert view.observations == ()
    assert view.groups == ()


def test_intensional_dependencies_fail_in_materialized_identity_products() -> None:
    field_contract = loci.CarrierContract(loci.CarrierKind.FIELD, rank=1)
    point = loci.field_point("u", (Fraction(0),))
    source = loci.FiniteConfiguration(
        loci.Carrier(
            field_contract,
            loci.Boundary(loci.BoundaryPolicy.NONE),
        ),
        ((point, 1),),
    )
    mixed = neighborhoods.product(
        (
            (
                "value",
                neighborhoods.field_restriction(
                    "u",
                    (0, 0),
                    configuration_contract=field_contract,
                    value_profile=alphabets.ValueProfile.INTEGER,
                ),
            ),
            (
                "germ",
                neighborhoods.differential_germ(
                    "u",
                    1,
                    configuration_contract=field_contract,
                    value_profile=alphabets.ValueProfile.INTEGER,
                ),
            ),
        )
    )

    with pytest.raises(
        neighborhoods.ReadableResolutionError,
        match="cannot silently discard",
    ):
        mixed.resolve(source)


def test_intensional_read_view_is_usable_by_closed_relation_rules() -> None:
    field_contract = loci.CarrierContract(loci.CarrierKind.FIELD, rank=1)
    point = loci.field_point("u", (Fraction(0),))
    field_value = alphabets.ValueNode(
        alphabets.ValueKind.FIELD,
        "partial-field",
        fields=(("value", 1),),
    )
    source = loci.FiniteConfiguration(
        loci.Carrier(
            field_contract,
            loci.Boundary(loci.BoundaryPolicy.NONE),
        ),
        ((point, field_value),),
    )
    alphabet = alphabets.field()
    neighborhood = neighborhoods.differential_germ(
        "u",
        1,
        configuration_contract=field_contract,
        value_profile=alphabet.value_profile,
    )
    frontier = frontiers.everywhere(
        configuration_contract=field_contract,
        value_profile=alphabet.value_profile,
    )
    view = neighborhood.resolve(source)
    writable = frontier.resolve(source)

    def certificate(
        kind: rules.CertificateKind,
        label: str,
    ) -> rules.Certificate:
        return rules.Certificate(kind, rules.literal_expr(label))

    rule = rules.differential(
        rules.literal_expr("du/dx=0"),
        rules.ExactlyOne(
            certificate(rules.CertificateKind.CARDINALITY, "one-family")
        ),
        contract=rules.RuleContract(
            field_contract,
            alphabet.value_profile,
            neighborhood.result_shape,
            neighborhood.join_shape,
            frontier.effect_profile,
        ),
        completeness_evidence=certificate(
            rules.CertificateKind.COMPLETENESS,
            "complete",
        ),
        soundness_evidence=certificate(
            rules.CertificateKind.SOUNDNESS,
            "sound",
        ),
    )

    result = rule.denote(view, writable)

    assert isinstance(view, neighborhoods.IntensionalReadableView)
    assert isinstance(result, rules.RuleComplete)
    assert (
        result.outcome_space.support.presentation
        is rules.SupportPresentation.INTENSIONAL
    )
