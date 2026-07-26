"""Focused tests for closed composite values and rank-generic finite grids."""

from __future__ import annotations

import pytest

from ca import alphabets, loci


def test_public_composite_constructors_match_their_schemas_and_accessors() -> None:
    tagged = alphabets.tag_value("some", 3)
    product = alphabets.product_value((True, 4), tag="flag-count")
    record = alphabets.record_value(
        (("flag", False), ("count", 2)),
        tag="state",
    )
    word = alphabets.word_value(("a", "b"), tag="symbols")
    pattern = alphabets.pattern_value(
        "capture",
        items=(alphabets.symbolic_value("variable", items=("x",)),),
        fields=(("name", "x"),),
    )
    field = alphabets.field_value(
        "sample",
        fields=(("value", 7), ("component", "u")),
    )

    assert alphabets.tag("some", alphabets.integers()).contains(tagged)
    assert alphabets.product(
        (alphabets.boolean(), alphabets.integers())
    ).contains(product)
    assert alphabets.record(
        (("count", alphabets.integers()), ("flag", alphabets.boolean()))
    ).contains(record)
    assert alphabets.word(alphabets.symbolic(("a", "b"))).contains(word)
    assert alphabets.pattern().contains(pattern)
    assert alphabets.field().contains(field)
    assert alphabets.enum((pattern,)).contains(pattern)

    assert alphabets.tag_payload(tagged) == 3
    assert alphabets.product_items(product) == (True, 4)
    assert alphabets.record_fields(record) == (
        ("count", 2),
        ("flag", False),
    )
    assert alphabets.record_get(record, "flag") is False
    assert alphabets.word_items(word) == ("a", "b")
    assert alphabets.node_items(pattern) == pattern.items
    assert alphabets.node_fields(field) == (
        ("component", "u"),
        ("value", 7),
    )
    assert alphabets.node_get(field, "component") == "u"


@pytest.mark.parametrize(
    "kind",
    (
        alphabets.ValueKind.RECORD,
        alphabets.ValueKind.GRAPH,
        alphabets.ValueKind.FIELD,
        alphabets.ValueKind.INSTRUCTION,
        alphabets.ValueKind.PATTERN,
        alphabets.ValueKind.EQUATION,
        alphabets.ValueKind.DISTRIBUTION,
        alphabets.ValueKind.SYMBOLIC,
    ),
)
def test_named_value_node_fields_have_one_canonical_order(
    kind: alphabets.ValueKind,
) -> None:
    left = alphabets.ValueNode(
        kind,
        "fixture",
        fields=(("zeta", 2), ("alpha", 1)),
    )
    right = alphabets.ValueNode(
        kind,
        "fixture",
        fields=(("alpha", 1), ("zeta", 2)),
    )

    assert left.fields == (("alpha", 1), ("zeta", 2))
    assert left == right
    assert alphabets.semantic_equal(left, right)


def test_map_values_use_explicit_canonical_semantic_key_entries() -> None:
    coordinate_key = alphabets.product_value(
        (2, -1),
        tag="coordinate",
    )
    tagged_key = alphabets.tag_value("slot", "tail")
    coordinate_entry = alphabets.map_entry_value(coordinate_key, "occupied")
    tagged_entry = alphabets.map_entry_value(tagged_key, "open")

    left = alphabets.map_value(
        (tagged_entry, coordinate_entry),
        tag="support",
    )
    right = alphabets.map_value(
        (coordinate_entry, tagged_entry),
        tag="support",
    )
    schema = alphabets.map_values(
        alphabets.enum((coordinate_key, tagged_key)),
        alphabets.symbolic(("occupied", "open")),
    )

    assert left == right
    assert alphabets.semantic_equal(left, right)
    assert not left.fields
    assert all(
        entry.kind is alphabets.ValueKind.PRODUCT
        and entry.tag == "entry"
        and len(entry.items) == 2
        for entry in left.items
    )
    assert schema.contains(left)
    assert alphabets.map_get(left, coordinate_key) == "occupied"
    assert alphabets.map_get(left, tagged_key) == "open"
    assert alphabets.map_entries(left) == tuple(
        (entry.items[0], entry.items[1]) for entry in left.items
    )


def test_map_keys_are_semantically_unique_and_bind_structural_references() -> None:
    first_key = alphabets.record_value(
        (("x", 1), ("y", 2)),
        tag="coordinate",
    )
    equal_key = alphabets.record_value(
        (("y", 2), ("x", 1)),
        tag="coordinate",
    )
    with pytest.raises(ValueError, match="semantically unique"):
        alphabets.map_value(
            (
                alphabets.map_entry_value(first_key, "first"),
                alphabets.map_entry_value(equal_key, "second"),
            )
        )

    fresh = loci.fresh_reference("children", "left")
    bound = loci.named("left", scope="bound")
    unresolved = alphabets.map_value(
        (
            alphabets.map_entry_value(
                alphabets.StructuralReference(fresh),
                alphabets.word_value((1, 2)),
            ),
        )
    )
    resolved = alphabets.bind_structural_references(
        unresolved,
        ((fresh, bound),),
    )

    assert alphabets.map_get(
        resolved,
        alphabets.StructuralReference(bound),
    ) == alphabets.word_value((1, 2))


def test_composite_values_fail_closed_on_opaque_or_malformed_payloads() -> None:
    with pytest.raises(TypeError, match="opaque"):
        alphabets.tag_value("opaque", object())  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="immutable"):
        alphabets.product_value([1, 2])  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="at least one"):
        alphabets.product_value(())
    with pytest.raises(TypeError, match="immutable"):
        alphabets.record_value([("x", 1)])  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="unique"):
        alphabets.record_value((("x", 1), ("x", 2)))
    with pytest.raises(TypeError, match="immutable"):
        alphabets.word_value([1, 2])  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="immutable"):
        alphabets.map_value([])  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="explicit entry products"):
        alphabets.ValueNode(
            alphabets.ValueKind.MAP,
            "map",
            items=(alphabets.product_value(("key", "value")),),
        )
    with pytest.raises(ValueError, match="not fields"):
        alphabets.ValueNode(
            alphabets.ValueKind.MAP,
            "map",
            fields=(("key", "value"),),
        )
    with pytest.raises(TypeError, match="closed semantic"):
        alphabets.map_get(alphabets.map_value(()), object())  # type: ignore[arg-type]


def test_composite_accessors_reject_wrong_shapes_and_missing_members() -> None:
    record = alphabets.record_value((("x", 1),))
    word = alphabets.word_value((1,))
    mapping = alphabets.map_value(
        (alphabets.map_entry_value("x", 1),)
    )

    with pytest.raises(TypeError, match="tag"):
        alphabets.tag_payload(word)
    with pytest.raises(TypeError, match="product"):
        alphabets.product_items(record)
    with pytest.raises(TypeError, match="record"):
        alphabets.record_fields(word)
    with pytest.raises(KeyError):
        alphabets.record_get(record, "missing")
    with pytest.raises(TypeError, match="word"):
        alphabets.word_items(record)
    with pytest.raises(KeyError):
        alphabets.map_get(mapping, "missing")
    with pytest.raises(TypeError, match="ValueNode"):
        alphabets.node_items(1)
    with pytest.raises(ValueError, match="field name"):
        alphabets.node_get(record, "")


def test_default_grid_axes_preserve_familiar_ranks_and_extend_deterministically() -> None:
    assert loci.default_grid_axes(1) == ("x",)
    assert loci.default_grid_axes(2) == ("x", "y")
    assert loci.default_grid_axes(3) == ("x", "y", "z")
    assert loci.default_grid_axes(6) == (
        "x",
        "y",
        "z",
        "axis4",
        "axis5",
        "axis6",
    )

    target = loci.cell((0, 1, 2, 3, 4))
    assert target.scope == "grid:x,y,z,axis4,axis5"
    assert loci.grid_coordinates(target) == (0, 1, 2, 3, 4)
    assert loci.coordinate("axis5", -1).path == ("axis5", -1)


def test_finite_grid_helpers_support_arbitrary_positive_rank_and_custom_axes() -> None:
    shape = (1, 1, 1, 1, 1)
    configuration = loci.grid_configuration(
        shape,
        (7,),
        boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
    )

    assert configuration.contract.rank == 5
    assert configuration.contract.axes == (
        "x",
        "y",
        "z",
        "axis4",
        "axis5",
    )
    assert tuple(target for target, _ in configuration.entries) == loci.grid_loci(
        shape
    )
    assert loci.read_grid_value(configuration, (9, -4, 2, 11, -8)) == 7

    custom_axes = ("row", "column", "layer", "phase")
    custom = loci.grid_configuration(
        (1, 1, 1, 1),
        ("origin",),
        boundary=loci.Boundary(loci.BoundaryPolicy.NONE),
        axes=custom_axes,
    )
    assert custom.contract.axes == custom_axes
    assert custom.entries[0][0] == loci.cell(
        (0, 0, 0, 0),
        axes=custom_axes,
    )


def test_realized_finite_grids_materialize_default_axes_without_mutating_wildcards() -> None:
    wildcard = loci.CarrierContract(
        loci.CarrierKind.GRID,
        rank=2,
        shape=(1, 1),
    )
    configuration = loci.FiniteConfiguration(
        loci.Carrier(
            wildcard,
            loci.Boundary(loci.BoundaryPolicy.NONE),
        ),
        ((loci.cell((0, 0)), 7),),
    )

    assert wildcard.axes == ()
    assert wildcard.accepts(configuration.contract)
    assert configuration.contract.axes == ("x", "y")
    assert loci.read_grid_value(configuration, (0, 0)) == 7


@pytest.mark.parametrize("rank", (0, -1, True, 1.5, "4"))
def test_default_grid_axes_reject_nonpositive_or_inexact_rank(rank: object) -> None:
    with pytest.raises((TypeError, ValueError), match="grid rank"):
        loci.default_grid_axes(rank)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "shape",
    (
        [],
        (),
        (1, True),
        (1, 1.5),
        (1, 0),
        (1, -1),
    ),
)
def test_grid_loci_reject_malformed_shapes(shape: object) -> None:
    with pytest.raises((TypeError, ValueError), match="grid (shape|rank)"):
        loci.grid_loci(shape)  # type: ignore[arg-type]


def test_grid_helpers_reject_malformed_axes_values_and_read_coordinates() -> None:
    with pytest.raises(TypeError, match="immutable tuple"):
        loci.grid_loci((1, 1), axes=["x", "y"])  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="equal rank"):
        loci.grid_loci((1, 1), axes=("x",))
    with pytest.raises(ValueError, match="unique"):
        loci.grid_loci((1, 1), axes=("x", "x"))
    with pytest.raises(TypeError, match="nonempty strings"):
        loci.grid_loci((1, 1), axes=("x", ""))
    with pytest.raises(TypeError, match="immutable tuple"):
        loci.grid_configuration(
            (1,),
            [1],  # type: ignore[arg-type]
            boundary=loci.Boundary(loci.BoundaryPolicy.NONE),
        )

    configuration = loci.grid_configuration(
        (1, 1, 1, 1),
        (1,),
        boundary=loci.Boundary(loci.BoundaryPolicy.NONE),
    )
    with pytest.raises(ValueError, match="equal rank"):
        loci.read_grid_value(configuration, (0, 0, 0))
    with pytest.raises(TypeError, match="integers"):
        loci.read_grid_value(
            configuration,
            (0, 0, 0, True),
        )
    with pytest.raises(TypeError, match="immutable tuple"):
        loci.read_grid_value(
            configuration,
            [0, 0, 0, 0],  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    ("scope", "path", "error"),
    (
        ("grid:x", ("other", 0), ValueError),
        ("grid:x", ("x", "0"), TypeError),
        ("grid:x", ("x", True), TypeError),
        ("grid:x,y", ("x", 0), ValueError),
        ("grid:x,x", ("x", 0, "x", 1), ValueError),
        ("grid:x", (), ValueError),
    ),
)
def test_grid_coordinates_reject_forged_or_inexact_loci(
    scope: str,
    path: tuple[loci.ClosedScalar, ...],
    error: type[Exception],
) -> None:
    forged = loci.Locus(loci.LocusKind.COORDINATE, scope, path)

    with pytest.raises(error):
        loci.grid_coordinates(forged)
