"""CT05 skeleton: outcome and cardinality algebra.

The implemented suite will distinguish semantic outcomes from presentation
size and keep source atoms, derivations, and distinct successors separate.
This module remains skipped until implementation; skips are not conformance
evidence.
"""

from typing import NoReturn

import pytest


pytestmark = pytest.mark.skip(
    reason="Goal 7 CT05 outcome-cardinality skeleton; implementation is pending"
)


def _pending() -> NoReturn:
    raise NotImplementedError("Goal 7 CT05 tests are not implemented")


def test_all_progress_continuation_and_no_successor_outcomes_remain_distinct() -> None:
    """Change, identity, stop, terminal, undefined, failure, and divergence differ."""

    _pending()


def test_outcome_derivation_and_successor_cardinalities_are_independent() -> None:
    """The PX04 diamond and stopped one-shot cases retain their exact counts."""

    _pending()


def test_exact_zero_requires_typed_atom_and_coverage_evidence() -> None:
    """Bare empty support is invalid and differs from an undetermined relation."""

    _pending()


def test_resource_exhaustion_exists_only_in_bounded_external_results() -> None:
    """Base Rule/Application semantics never invent completion from a bound."""

    _pending()
