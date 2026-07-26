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


def test_unimplemented_selector_primitives_reject_until_their_mechanics_exist() -> None:
    implemented = {
        loci.SelectorPrimitive.LITERAL,
        loci.SelectorPrimitive.MEMBERSHIP,
        loci.SelectorPrimitive.RELATIVE,
        loci.SelectorPrimitive.AND,
        loci.SelectorPrimitive.OR,
        loci.SelectorPrimitive.NOT,
    }

    for primitive in set(loci.SelectorPrimitive) - implemented:
        with pytest.raises(ValueError, match="reserved for G7-02"):
            loci.SelectorExpr(primitive)


def test_every_g7_01_region_variant_has_one_validated_shape() -> None:
    target = loci.named("target")
    base = loci.literal((target,))
    membership = loci.SelectorExpr(loci.SelectorPrimitive.MEMBERSHIP)
    fresh_edge = loci.FreshReference("edges", "edge")
    regions = (
        base,
        loci.all_support(),
        loci.current_support(),
        loci.relative(base, (loci.coordinate("x", 1),)),
        loci.region_product((("left", base),)),
        loci.union((base, loci.literal((loci.named("other"),)))),
        loci.fresh_children(target, "children", ("child",)),
        loci.Region(
            loci.RegionKind.FRESH_EDGES,
            name="edges",
            fresh=(fresh_edge,),
        ),
        loci.intensional("x", membership),
    )
    implemented = {
        loci.RegionKind.LITERAL,
        loci.RegionKind.ALL_SUPPORT,
        loci.RegionKind.CURRENT_SUPPORT,
        loci.RegionKind.RELATIVE,
        loci.RegionKind.PRODUCT,
        loci.RegionKind.UNION,
        loci.RegionKind.FRESH_CHILDREN,
        loci.RegionKind.FRESH_EDGES,
        loci.RegionKind.INTENSIONAL,
    }

    assert {region.kind for region in regions} == implemented
    for kind in set(loci.RegionKind) - implemented:
        with pytest.raises(ValueError, match="reserved for G7-02"):
            loci.Region(kind)


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
