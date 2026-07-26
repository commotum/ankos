"""Unit tests for closed exact Alphabet schemas."""

from fractions import Fraction

import pytest

from ca import alphabets


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
