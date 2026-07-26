"""Unit tests for closed exact Alphabet schemas."""

from fractions import Fraction

import pytest

from ca import alphabets, loci


def test_alphabet_descriptors_are_closed_and_versioned() -> None:
    descriptors = (
        alphabets.boolean().descriptor,
        alphabets.integers(minimum=-2, maximum=2).descriptor,
        alphabets.rationals().descriptor,
        alphabets.symbolic(("a", "b")).descriptor,
        alphabets.graph().descriptor,
    )

    assert all(descriptor.version == 1 for descriptor in descriptors)
    assert tuple(descriptor.kind for descriptor in descriptors) == (
        alphabets.AlphabetKind.ENUM,
        alphabets.AlphabetKind.INTEGERS,
        alphabets.AlphabetKind.RATIONALS,
        alphabets.AlphabetKind.SYMBOLIC,
        alphabets.AlphabetKind.GRAPH,
    )


def test_alphabet_supports_exact_scalar_and_structural_profiles() -> None:
    tagged = alphabets.tag("some", alphabets.integers())
    tagged_value = alphabets.ValueNode(
        alphabets.ValueKind.TAG,
        "some",
        items=(3,),
    )
    product = alphabets.product((alphabets.boolean(), alphabets.integers()))
    product_value = alphabets.ValueNode(
        alphabets.ValueKind.PRODUCT,
        "pair",
        items=(True, 4),
    )
    record = alphabets.record(
        (("flag", alphabets.boolean()), ("count", alphabets.integers()))
    )
    record_value = alphabets.ValueNode(
        alphabets.ValueKind.RECORD,
        "record",
        fields=(("count", 2), ("flag", False)),
    )

    assert tagged.contains(tagged_value)
    assert product.contains(product_value)
    assert record.contains(record_value)
    assert alphabets.rationals().contains(Fraction(2, 3))
    assert alphabets.graph().contains(
        alphabets.ValueNode(alphabets.ValueKind.GRAPH, "network")
    )


def test_alphabet_semantic_equality_ignores_mapping_insertion_order() -> None:
    left = alphabets.ValueNode(
        alphabets.ValueKind.RECORD,
        "state",
        fields=(("b", 2), ("a", 1)),
    )
    right = alphabets.ValueNode(
        alphabets.ValueKind.RECORD,
        "state",
        fields=(("a", 1), ("b", 2)),
    )
    schema = alphabets.record(
        (("a", alphabets.integers()), ("b", alphabets.integers()))
    )

    assert left.fields == right.fields
    assert alphabets.semantic_equal(left, right)
    assert schema.equal(left, right)


def test_enum_canonicalization_does_not_collapse_python_equal_value_types() -> None:
    left = alphabets.enum((0, False))
    right = alphabets.enum((False, 0))

    assert left.descriptor.values == (False, 0)
    assert tuple(type(item) for item in left.descriptor.values) == (bool, int)
    assert left.descriptor == right.descriptor


def test_alphabet_composition_returns_one_component() -> None:
    composed = alphabets.union(
        (
            alphabets.boolean(),
            alphabets.tag("symbol", alphabets.symbolic(("x", "y"))),
        )
    )

    assert isinstance(composed, alphabets.Alphabet)
    assert composed.descriptor.kind is alphabets.AlphabetKind.UNION
    assert len(composed.descriptor.children) == 2


def test_represented_numbers_do_not_claim_exact_real_semantics() -> None:
    represented = alphabets.represented_numeric(
        alphabets.RepresentedNumberProfile.IEEE754_BINARY64
    )
    value = alphabets.RepresentedNumber(
        alphabets.RepresentedNumberProfile.IEEE754_BINARY64,
        "0x3ff0000000000000",
    )

    assert represented.contains(value)
    assert represented.value_profile is alphabets.ValueProfile.REPRESENTED
    assert not represented.contains(1)  # type: ignore[arg-type]
    with pytest.raises((TypeError, AttributeError)):
        alphabets.enum((0.5,))  # type: ignore[arg-type]


def test_alphabet_values_reject_mutable_and_profile_incompatible_payloads() -> None:
    with pytest.raises(TypeError, match="immutable"):
        alphabets.ValueNode(
            alphabets.ValueKind.PRODUCT,
            "pair",
            items=[1],  # type: ignore[arg-type]
        )
    with pytest.raises(TypeError, match="immutable"):
        alphabets.AlphabetDescriptor(
            alphabets.AlphabetKind.ORDERED,
            values=[1, 2],  # type: ignore[arg-type]
        )
    with pytest.raises(TypeError, match="IEEE"):
        alphabets.RepresentedNumber(
            alphabets.RepresentedNumberProfile.IEEE754_BINARY64,
            (Fraction(0), Fraction(1)),
        )
    with pytest.raises(TypeError, match="interval"):
        alphabets.RepresentedNumber(
            alphabets.RepresentedNumberProfile.INTERVAL,
            1,
        )


def test_algebraic_numbers_are_exact_normalized_isolated_roots() -> None:
    square_root_two = alphabets.AlgebraicNumber(
        (1, 0, -2),
        (Fraction(1), Fraction(2)),
    )
    same_root = alphabets.AlgebraicNumber(
        (2, 0, -4),
        (Fraction(4, 3), Fraction(3, 2)),
    )

    assert square_root_two.polynomial == (1, 0, -2)
    assert square_root_two.root_index == 1
    assert alphabets.semantic_equal(square_root_two, same_root)
    assert alphabets.algebraics().contains(square_root_two)
    assert (
        alphabets.algebraics().value_profile
        is alphabets.ValueProfile.ALGEBRAIC
    )

    with pytest.raises(ValueError, match="exactly one"):
        alphabets.AlgebraicNumber(
            (1, 0, -2),
            (Fraction(-2), Fraction(2)),
        )
    with pytest.raises(ValueError, match="root_index"):
        alphabets.AlgebraicNumber(
            (1, 0, -2),
            (Fraction(1), Fraction(2)),
            root_index=0,
        )


def test_exact_complex_never_accepts_represented_components() -> None:
    square_root_two = alphabets.AlgebraicNumber(
        (1, 0, -2),
        (Fraction(1), Fraction(2)),
    )
    value = alphabets.ExactComplex(square_root_two, Fraction(-1, 3))
    schema = alphabets.exact_complexes()

    assert schema.contains(value)
    assert schema.value_profile is alphabets.ValueProfile.COMPLEX
    with pytest.raises(TypeError, match="exact-complex"):
        alphabets.ExactComplex(  # type: ignore[arg-type]
            alphabets.RepresentedNumber(
                alphabets.RepresentedNumberProfile.DECIMAL,
                "1.0",
            ),
            0,
        )


def test_structural_references_bind_recursively_and_fail_closed() -> None:
    fresh = loci.fresh_reference("child", "left")
    existing = loci.named("root")
    bound = loci.named("left", scope="bound")
    value = alphabets.ValueNode(
        alphabets.ValueKind.RECORD,
        "references",
        fields=(
            ("existing", alphabets.StructuralReference(existing)),
            (
                "nested",
                alphabets.ValueNode(
                    alphabets.ValueKind.PRODUCT,
                    "pair",
                    items=(alphabets.StructuralReference(fresh), 1),
                ),
            ),
        ),
    )

    resolved = alphabets.bind_structural_references(
        value,
        ((fresh, bound),),
    )

    assert isinstance(resolved, alphabets.ValueNode)
    fields = dict(resolved.fields)
    assert fields["existing"] == alphabets.StructuralReference(existing)
    nested = fields["nested"]
    assert isinstance(nested, alphabets.ValueNode)
    assert nested.items[0] == alphabets.StructuralReference(bound)
    assert alphabets.structural_references().contains(nested.items[0])
    with pytest.raises(ValueError, match="unbound"):
        alphabets.bind_structural_references(value, ())


def test_representation_relation_distinguishes_exact_lossy_and_approximate() -> None:
    source = alphabets.enum(("a", "b"))
    binary = alphabets.enum((0, 1))
    exact = alphabets.RepresentationRelation(
        source.descriptor,
        binary.descriptor,
        alphabets.RepresentationProfile.EXACT,
        (
            alphabets.RepresentationPair("b", 1),
            alphabets.RepresentationPair("a", 0),
        ),
        (1, 0),
        (
            alphabets.RepresentationPair(1, "b"),
            alphabets.RepresentationPair(0, "a"),
        ),
    )

    assert exact.forward("a") == 0
    assert exact.inverse(1) == "b"
    assert exact.image_evidence == (0, 1)

    lossy = alphabets.RepresentationRelation(
        source.descriptor,
        alphabets.enum((0,)).descriptor,
        alphabets.RepresentationProfile.LOSSY,
        (
            alphabets.RepresentationPair("a", 0),
            alphabets.RepresentationPair("b", 0),
        ),
        (0,),
        qualification=(("information-loss", "many-to-one"),),
    )
    assert lossy.forward("b") == 0
    with pytest.raises(ValueError, match="only exact"):
        lossy.inverse(0)

    third = Fraction(1, 3)
    represented_third = alphabets.RepresentedNumber(
        alphabets.RepresentedNumberProfile.IEEE754_BINARY32,
        0x3EAAAAAB,
    )
    approximate = alphabets.RepresentationRelation(
        alphabets.enum((third,)).descriptor,
        alphabets.represented_numeric(
            alphabets.RepresentedNumberProfile.IEEE754_BINARY32
        ).descriptor,
        alphabets.RepresentationProfile.APPROXIMATE,
        (alphabets.RepresentationPair(third, represented_third),),
        (represented_third,),
        qualification=(("error-model", "nearest-binary32"),),
    )
    assert approximate.forward(third) == represented_third


def test_representation_relation_validates_coverage_image_and_inverse() -> None:
    source = alphabets.enum(("a", "b"))
    target = alphabets.enum((0, 1))

    with pytest.raises(ValueError, match="cover"):
        alphabets.RepresentationRelation(
            source.descriptor,
            target.descriptor,
            alphabets.RepresentationProfile.EXACT,
            (alphabets.RepresentationPair("a", 0),),
            (0,),
            (alphabets.RepresentationPair(0, "a"),),
        )
    with pytest.raises(ValueError, match="inverse-on-image"):
        alphabets.RepresentationRelation(
            source.descriptor,
            target.descriptor,
            alphabets.RepresentationProfile.EXACT,
            (
                alphabets.RepresentationPair("a", 0),
                alphabets.RepresentationPair("b", 1),
            ),
            (0, 1),
        )
    with pytest.raises(ValueError, match="error-bound or error-model"):
        alphabets.RepresentationRelation(
            alphabets.enum(("a",)).descriptor,
            target.descriptor,
            alphabets.RepresentationProfile.APPROXIMATE,
            (alphabets.RepresentationPair("a", 0),),
            (0,),
            qualification=(("method", "rounded"),),
        )


def test_refinement_is_closed_schema_intersection() -> None:
    nonnegative_small_integer = alphabets.refine(
        alphabets.integers(),
        alphabets.integers(minimum=0, maximum=3),
    )

    assert nonnegative_small_integer.contains(0)
    assert nonnegative_small_integer.contains(3)
    assert not nonnegative_small_integer.contains(-1)
    assert not nonnegative_small_integer.contains(4)
    assert (
        nonnegative_small_integer.value_profile
        is alphabets.ValueProfile.INTEGER
    )
