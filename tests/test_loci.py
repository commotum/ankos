"""Unit tests for closed structural identities and configurations."""

from fractions import Fraction

import pytest

from ca import alphabets, loci


def test_locus_constructors_cover_closed_structural_identity_forms() -> None:
    node = loci.graph_element("node", "n")
    values = (
        loci.coordinate("x", -2),
        loci.named("state"),
        loci.occurrence("word", 3),
        loci.path("root", 1),
        loci.span("word", 1, 4),
        loci.port(node, "out"),
        loci.interface(node, loci.graph_element("node", "m")),
        loci.product_locus("pair", (node, loci.named("state"))),
        node,
        loci.field_point("u", (Fraction(1, 2),)),
        loci.continuous_region("interval", (Fraction(0), Fraction(1))),
        loci.intensional_reference("x", "x > 0"),
    )

    assert {value.kind for value in values} == set(loci.LocusKind) - {
        loci.LocusKind.FRESH
    }
    assert all(value.version == 1 for value in values)


def test_canonical_order_is_numeric_not_lexicographic() -> None:
    targets = tuple(
        sorted(
            (loci.cell((2,)), loci.cell((-1,)), loci.cell((0,)), loci.cell((-2,))),
            key=loci.canonical_order_key,
        )
    )

    assert tuple(loci.grid_coordinates(target)[0] for target in targets) == (
        -2,
        -1,
        0,
        2,
    )


def test_configuration_storage_order_and_identity_are_canonical() -> None:
    carrier = loci.Carrier(
        loci.CarrierContract(loci.CarrierKind.RECORD, rank=0, shape=()),
        loci.Boundary(loci.BoundaryPolicy.NONE),
    )
    a = loci.named("a", scope="record")
    b = loci.named("b", scope="record")
    left = loci.FiniteConfiguration(carrier, ((b, 2), (a, 1)))
    right = loci.FiniteConfiguration(carrier, ((a, 1), (b, 2)))

    assert left.entries == right.entries
    assert left.identity == right.identity
    assert loci.semantic_equal(left, right)
    assert left.with_entries(((a, 3), (b, 2))).value_at(a) == 3


@pytest.mark.parametrize(
    ("boundary", "coordinate", "expected"),
    (
        (loci.Boundary(loci.BoundaryPolicy.FIXED, 9), (2,), 9),
        (loci.Boundary(loci.BoundaryPolicy.PERIODIC), (2,), 1),
        (loci.Boundary(loci.BoundaryPolicy.REFLECTIVE), (2,), 2),
    ),
)
def test_grid_boundary_data_owns_outside_reads(
    boundary: loci.Boundary[int],
    coordinate: tuple[int, ...],
    expected: int,
) -> None:
    configuration = loci.grid_configuration(
        (3,),
        (1, 2, 3),
        boundary=boundary,
    )

    assert loci.read_grid_value(configuration, coordinate) == expected


def test_regions_resolve_without_granting_capabilities() -> None:
    configuration = loci.record_configuration((("a", 1), ("b", 2)))
    a, b = tuple(target for target, _ in configuration.entries)
    region = loci.union(
        (
            loci.literal((b,)),
            loci.literal((a,)),
        )
    )

    assert loci.resolve_region(region, configuration) == (a, b)
    assert not hasattr(region, "read")
    assert not hasattr(region, "write")


def test_fresh_binding_is_deterministic_structural_data() -> None:
    parent = loci.named("parent")
    reference = loci.fresh_reference("children", "a", parent=parent)
    arguments = {
        "input_configuration_identity": "input",
        "canonical_rule_identity": "rule",
        "witness_identity": "witness",
    }

    left = loci.bind_fresh(reference, **arguments)
    right = loci.bind_fresh(reference, **arguments)

    assert left == right
    assert left.kind is loci.LocusKind.FRESH
    assert loci.bind_fresh(
        loci.fresh_reference("children", "b", parent=parent),
        **arguments,
    ) != left


def test_closed_nodes_reject_opaque_or_malformed_payloads() -> None:
    with pytest.raises(TypeError):
        loci.Locus(
            loci.LocusKind.PATH,
            "path",
            (object(),),  # type: ignore[arg-type]
        )
    with pytest.raises(TypeError):
        loci.SelectorExpr(
            loci.SelectorPrimitive.LITERAL,
            arguments=(lambda: None,),  # type: ignore[arg-type]
        )
    with pytest.raises(ValueError):
        loci.CarrierContract(loci.CarrierKind.GRID, rank=2, shape=(3,))


@pytest.mark.parametrize("coordinate", (0.5, True, "1/2"))
def test_field_points_reject_implicit_exactification(coordinate: object) -> None:
    with pytest.raises(TypeError, match="exact integers or Fractions"):
        loci.field_point(
            "u",
            (coordinate,),  # type: ignore[arg-type]
        )


def test_field_points_require_closed_names_and_immutable_coordinates() -> None:
    assert loci.field_point("u", (1, Fraction(1, 2))).path == (
        "u",
        Fraction(1),
        Fraction(1, 2),
    )
    with pytest.raises(TypeError, match="immutable tuple"):
        loci.field_point("u", [Fraction(0)])  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="field name"):
        loci.field_point("", (Fraction(0),))
    with pytest.raises(ValueError, match="component"):
        loci.field_point("u", (Fraction(0),), component="")


@pytest.mark.parametrize(
    "exterior",
    (
        object(),
        lambda: None,
        0.5,
        [1],
        {"value": 1},
    ),
)
def test_fixed_boundaries_reject_opaque_mutable_or_inexact_data(
    exterior: object,
) -> None:
    with pytest.raises(TypeError, match="closed immutable semantic data"):
        loci.Boundary(loci.BoundaryPolicy.FIXED, exterior)


def test_fixed_boundaries_accept_closed_structural_semantic_data() -> None:
    structural = alphabets.ValueNode(
        alphabets.ValueKind.WORD,
        "binary-word",
        items=(False, True),
    )

    boundary = loci.Boundary(loci.BoundaryPolicy.FIXED, structural)

    assert boundary.exterior == structural


def test_exact_structural_records_reject_boolean_versions_and_subclass_scalars() -> None:
    with pytest.raises(TypeError, match="version"):
        loci.Locus(loci.LocusKind.NAMED, "scope", ("name",), True)
    with pytest.raises(TypeError, match="version"):
        loci.Boundary(loci.BoundaryPolicy.NONE, version=True)


@pytest.mark.parametrize("index", (True, 1.5, "1"))
def test_occurrences_reject_implicit_integer_coercion(index: object) -> None:
    with pytest.raises(TypeError, match="index must be an integer"):
        loci.occurrence("word", index)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("start", "stop"),
    (
        (True, 1),
        (0, False),
        (0.5, 1),
        (0, 1.5),
    ),
)
def test_spans_reject_implicit_integer_coercion(
    start: object,
    stop: object,
) -> None:
    with pytest.raises(TypeError, match="bounds must be integers"):
        loci.span("word", start, stop)  # type: ignore[arg-type]


def test_cells_and_intensional_references_require_nonempty_exact_identity() -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        loci.cell(())
    with pytest.raises(TypeError, match="coordinates must be integers"):
        loci.cell((True,))
    with pytest.raises(ValueError, match="binder"):
        loci.intensional_reference("", "relation")
    with pytest.raises(ValueError, match="relation identity"):
        loci.intensional_reference("x", "")


def test_g7_01_selector_shapes_are_closed_and_explicit() -> None:
    target = loci.named("target")
    literal = loci.SelectorExpr(
        loci.SelectorPrimitive.LITERAL,
        arguments=(target,),
    )
    membership = loci.SelectorExpr(loci.SelectorPrimitive.MEMBERSHIP)
    relative = loci.SelectorExpr(
        loci.SelectorPrimitive.RELATIVE,
        arguments=(target,),
    )

    assert loci.SelectorExpr(
        loci.SelectorPrimitive.AND,
        children=(literal, membership),
    ).children == (literal, membership)
    assert loci.SelectorExpr(
        loci.SelectorPrimitive.OR,
        children=(membership, relative),
    ).children == (membership, relative)
    assert loci.SelectorExpr(
        loci.SelectorPrimitive.NOT,
        children=(membership,),
    ).children == (membership,)

    with pytest.raises(ValueError, match="literal selector"):
        loci.SelectorExpr(loci.SelectorPrimitive.LITERAL)
    with pytest.raises(ValueError, match="one Locus"):
        loci.SelectorExpr(
            loci.SelectorPrimitive.RELATIVE,
            arguments=("target",),
        )
    with pytest.raises(ValueError, match="two child"):
        loci.SelectorExpr(
            loci.SelectorPrimitive.AND,
            children=(membership,),
        )


def test_every_selector_primitive_has_one_closed_validated_shape() -> None:
    target = loci.path("root")
    literal = loci.selector_literal(target)
    selectors = (
        literal,
        loci.selector_equal(target, target),
        loci.selector_tagged("path"),
        loci.SelectorExpr(
            loci.SelectorPrimitive.RELATIVE,
            arguments=(target,),
        ),
        loci.selector_metric(loci.cell((0,)), 1),
        loci.selector_path(target),
        loci.selector_incidence(target),
        loci.selector_reachable(target, 2),
        loci.selector_field_restriction(
            "u",
            (Fraction(0), Fraction(1)),
        ),
        loci.selector_differential_germ("u", 1),
        loci.selector_history(),
        loci.SelectorExpr(loci.SelectorPrimitive.MEMBERSHIP),
        loci.SelectorExpr(
            loci.SelectorPrimitive.AND,
            children=(literal, literal),
        ),
        loci.SelectorExpr(
            loci.SelectorPrimitive.OR,
            children=(literal, literal),
        ),
        loci.SelectorExpr(
            loci.SelectorPrimitive.NOT,
            children=(literal,),
        ),
    )

    assert {selector.primitive for selector in selectors} == set(
        loci.SelectorPrimitive
    )
    with pytest.raises(ValueError, match="nonnegative exact radius"):
        loci.selector_metric(loci.cell((0,)), -1)
    with pytest.raises(ValueError, match="ordered integer range"):
        loci.selector_history(2, 1)
    with pytest.raises(ValueError, match="lower/upper"):
        loci.selector_field_restriction(
            "u",
            (Fraction(1), Fraction(0)),
        )


def test_every_region_variant_has_one_validated_shape() -> None:
    target = loci.named("target")
    other = loci.named("other")
    base = loci.literal((target,))
    membership = loci.SelectorExpr(loci.SelectorPrimitive.MEMBERSHIP)
    regions = (
        base,
        loci.all_support(),
        loci.current_support(),
        loci.relative(base, (loci.coordinate("x", 1),)),
        loci.region_product((("left", base),)),
        loci.union((base, loci.literal((other,)))),
        loci.intersection((base, loci.all_support())),
        loci.difference(loci.all_support(), base),
        loci.span_region("word", 0, 1),
        loci.path_region(loci.path("root")),
        loci.matched_interface(base, loci.literal((other,))),
        loci.dynamic_address(base),
        loci.fresh_children(target, "children", ("child",)),
        loci.fresh_edges(
            (target, other),
            "edges",
            ("edge",),
        ),
        loci.continuous(
            "interval",
            (Fraction(0), Fraction(1)),
        ),
        loci.differential(
            "u",
            loci.selector_differential_germ("u", 1),
        ),
        loci.intensional("x", membership),
    )

    assert {region.kind for region in regions} == set(loci.RegionKind)


def test_region_variants_reject_irrelevant_or_ambiguous_fields_locally() -> None:
    target = loci.named("target")
    base = loci.literal((target,))
    with pytest.raises(ValueError, match="all-support"):
        loci.Region(loci.RegionKind.ALL_SUPPORT)
    with pytest.raises(ValueError, match="duplicate loci"):
        loci.literal((target, target))
    with pytest.raises(ValueError, match="relative"):
        loci.Region(
            loci.RegionKind.RELATIVE,
            name="unexpected",
            parts=(base,),
            offsets=(loci.coordinate("x", 1),),
        )
    with pytest.raises(ValueError, match="product"):
        loci.Region(
            loci.RegionKind.PRODUCT,
            name="field",
            parts=(base, base),
        )


def test_finite_set_span_path_interface_and_dynamic_address_resolution() -> None:
    left = loci.graph_element("node", "left")
    right = loci.graph_element("node", "right")
    edge = loci.graph_element("edge", "edge")
    address = loci.named("cursor", scope="graph")
    word_0 = loci.occurrence("word", 0)
    word_1 = loci.occurrence("word", 1)
    root = loci.path("root")
    child = loci.path("root", "child")
    carrier = loci.Carrier(
        loci.CarrierContract(loci.CarrierKind.GRAPH),
        loci.Boundary(loci.BoundaryPolicy.NONE),
    )
    configuration = loci.FiniteConfiguration(
        carrier,
        tuple(
            (target, 0)
            for target in (
                left,
                right,
                edge,
                address,
                word_0,
                word_1,
                root,
                child,
            )
        ),
        (
            loci.StructuralRelation(
                "interface",
                (left, right, edge),
            ),
            loci.StructuralRelation("address", (address, right)),
            loci.StructuralRelation("incidence", (left, edge, right)),
        ),
    )

    selected = loci.union(
        (
            loci.literal((left, right)),
            loci.literal((edge,)),
        )
    )
    assert loci.resolve_region(
        loci.intersection((selected, loci.literal((right, edge)))),
        configuration,
    ) == tuple(sorted((right, edge), key=loci.canonical_order_key))
    assert loci.resolve_region(
        loci.difference(selected, loci.literal((right,))),
        configuration,
    ) == tuple(sorted((left, edge), key=loci.canonical_order_key))
    assert loci.resolve_region(
        loci.span_region("word", 1, 2),
        configuration,
    ) == (word_1,)
    assert loci.resolve_region(
        loci.path_region(root),
        configuration,
    ) == tuple(sorted((root, child), key=loci.canonical_order_key))
    assert loci.resolve_region(
        loci.matched_interface(
            loci.literal((left,)),
            loci.literal((right,)),
        ),
        configuration,
    ) == (edge,)
    assert loci.resolve_region(
        loci.dynamic_address(loci.literal((address,))),
        configuration,
    ) == (right,)
    assert loci.resolve_selector(
        loci.selector_incidence(left),
        configuration,
    ) == tuple(
        target
        for target, _ in configuration.entries
        if target in (edge, right)
    )
    assert set(
        loci.resolve_selector(
            loci.selector_reachable(left, 1),
            configuration,
        )
    ) == {left, edge, right}


def test_closed_non_enumerated_regions_and_selectors_fail_without_approximation() -> None:
    configuration = loci.record_configuration((("u", 0),))
    regions = (
        loci.continuous(
            "interval",
            (Fraction(0), Fraction(1)),
        ),
        loci.differential(
            "u",
            loci.selector_differential_germ("u", 1),
        ),
        loci.intensional(
            "solution",
            loci.SelectorExpr(loci.SelectorPrimitive.MEMBERSHIP),
        ),
    )

    for region in regions:
        with pytest.raises(loci.LociResolutionError, match="non-enumerated"):
            loci.resolve_region(region, configuration)
    for selector in (
        loci.selector_differential_germ("u", 1),
        loci.SelectorExpr(loci.SelectorPrimitive.MEMBERSHIP),
    ):
        with pytest.raises(loci.LociResolutionError, match="non-enumerated"):
            loci.resolve_selector(selector, configuration)


def test_dynamic_fresh_templates_resolve_from_each_current_configuration() -> None:
    first = loci.record_configuration((("a", 0), ("b", 0)))
    second = loci.record_configuration((("c", 0),))
    children = loci.fresh_children_dynamic(
        loci.all_support(),
        "children",
        ("left", "right"),
    )

    first_references = loci.resolve_fresh_references(children, first)
    second_references = loci.resolve_fresh_references(children, second)

    assert {reference.parent for reference in first_references} == {
        target for target, _ in first.entries
    }
    assert {reference.local_key for reference in first_references} == {
        "left",
        "right",
    }
    assert {reference.parent for reference in second_references} == {
        target for target, _ in second.entries
    }
    assert not {
        reference.parent for reference in first_references
    }.intersection(reference.parent for reference in second_references)

    a, b = tuple(target for target, _ in first.entries)
    edges = loci.fresh_edges_dynamic(
        (loci.literal((a,)), loci.literal((b,))),
        "edges",
        ("edge",),
    )
    assert loci.resolve_fresh_references(edges, first) == (
        loci.FreshReference("edges", "edge", interface=(a, b)),
    )
    with pytest.raises(loci.LociResolutionError, match="needs a configuration"):
        loci.resolve_fresh_references(children)


def test_configuration_identity_law_supports_exact_or_bound_fresh_alpha() -> None:
    alpha_contract = loci.CarrierContract(
        loci.CarrierKind.GRAPH,
        identity_law=loci.ConfigurationIdentityLaw.BOUND_FRESH_ALPHA,
    )
    alpha_carrier = loci.Carrier(
        alpha_contract,
        loci.Boundary(loci.BoundaryPolicy.NONE),
    )
    left_a = loci.Locus(loci.LocusKind.FRESH, "nodes", ("a", "left"))
    left_b = loci.Locus(loci.LocusKind.FRESH, "nodes", ("z", "right"))
    right_a = loci.Locus(loci.LocusKind.FRESH, "nodes", ("z", "left"))
    right_b = loci.Locus(loci.LocusKind.FRESH, "nodes", ("a", "right"))
    left = loci.FiniteConfiguration(
        alpha_carrier,
        ((left_a, 1), (left_b, 2)),
        (loci.StructuralRelation("edge", (left_a, left_b)),),
    )
    right = loci.FiniteConfiguration(
        alpha_carrier,
        ((right_a, 1), (right_b, 2)),
        (loci.StructuralRelation("edge", (right_a, right_b)),),
    )

    assert left.identity == right.identity
    assert loci.configuration_equal(left, right)
    assert loci.semantic_equal(left, right)

    different_key = loci.FiniteConfiguration(
        alpha_carrier,
        (
            (loci.Locus(loci.LocusKind.FRESH, "nodes", ("a", "other")), 1),
            (right_b, 2),
        ),
    )
    assert not loci.configuration_equal(left, different_key)

    exact_carrier = loci.Carrier(
        loci.CarrierContract(loci.CarrierKind.GRAPH),
        loci.Boundary(loci.BoundaryPolicy.NONE),
    )
    exact_left = loci.FiniteConfiguration(exact_carrier, ((left_a, 1),))
    exact_right = loci.FiniteConfiguration(exact_carrier, ((right_a, 1),))
    assert not loci.configuration_equal(exact_left, exact_right)

    parent_a = loci.named("a", scope="graph")
    parent_b = loci.named("b", scope="graph")
    binding_arguments = {
        "input_configuration_identity": "source",
        "canonical_rule_identity": "rule",
    }
    children_left = tuple(
        loci.bind_fresh(
            loci.fresh_reference("children", "child", parent=parent),
            witness_identity="left-witness",
            **binding_arguments,
        )
        for parent in (parent_a, parent_b)
    )
    children_right = tuple(
        loci.bind_fresh(
            loci.fresh_reference("children", "child", parent=parent),
            witness_identity="right-witness",
            **binding_arguments,
        )
        for parent in (parent_a, parent_b)
    )
    anchored_left = loci.FiniteConfiguration(
        alpha_carrier,
        (
            (parent_a, 0),
            (parent_b, 0),
            (children_left[0], 1),
            (children_left[1], 1),
        ),
    )
    anchored_right = loci.FiniteConfiguration(
        alpha_carrier,
        (
            (parent_a, 0),
            (parent_b, 0),
            (children_right[0], 1),
            (children_right[1], 1),
        ),
    )
    assert loci.configuration_equal(anchored_left, anchored_right)

    with pytest.raises(ValueError, match="unique namespace/local-key/anchor"):
        loci.FiniteConfiguration(
            alpha_carrier,
            (
                (
                    loci.Locus(
                        loci.LocusKind.FRESH,
                        "nodes",
                        ("scope-a", "same"),
                    ),
                    1,
                ),
                (
                    loci.Locus(
                        loci.LocusKind.FRESH,
                        "nodes",
                        ("scope-b", "same"),
                    ),
                    2,
                ),
            ),
        )
