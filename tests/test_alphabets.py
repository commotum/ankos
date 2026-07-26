"""Goal 7 unit-contract skeleton for closed Alphabet values.

These tests will cover the component-owned value universe independently of
carrier topology, execution, and catalog naming. The module is skipped until
the G7-01 Alphabet contract is implemented; no skipped assertion is evidence
of conformance.
"""

from typing import NoReturn

import pytest


pytestmark = pytest.mark.skip(
    reason="Goal 7 Alphabet contract skeleton; implementation is pending"
)


def _pending() -> NoReturn:
    raise NotImplementedError("Goal 7 Alphabet tests are not implemented")


def test_alphabet_descriptors_are_closed_and_versioned() -> None:
    """Recognized nodes have stable tags, versions, and exact fields."""

    _pending()


def test_alphabet_supports_exact_scalar_and_structural_profiles() -> None:
    """Scalar, tagged, product, record, word, graph, and field values remain exact."""

    _pending()


def test_alphabet_semantic_equality_ignores_representation_accidents() -> None:
    """Object identity, hash order, storage order, and display form are irrelevant."""

    _pending()


def test_alphabet_composition_returns_one_component() -> None:
    """Products, tags, unions, and refinements remain one Alphabet value."""

    _pending()


def test_represented_numbers_do_not_claim_exact_real_semantics() -> None:
    """Machine floats require an explicit represented-number profile."""

    _pending()
