"""CT01 skeleton: exact five-field program boundary.

The implemented suite will reject every stored semantic sidecar and confirm
that catalog values are ordinary programs. This module remains skipped until
its Goal 7 implementation; skips are not conformance evidence.
"""

from typing import NoReturn

import pytest


pytestmark = pytest.mark.skip(
    reason="Goal 7 CT01 program-boundary skeleton; implementation is pending"
)


def _pending() -> NoReturn:
    raise NotImplementedError("Goal 7 CT01 tests are not implemented")


def test_simple_program_has_exactly_the_five_settled_fields() -> None:
    """Stored fields are seed, alphabet, frontier, neighborhood, and rule."""

    _pending()


def test_program_rejects_semantic_sidecars_and_constructor_receipts() -> None:
    """Domain, policy, scheduler, RNG, observer, and catalog identity stay outside."""

    _pending()


def test_every_catalog_constructor_returns_exact_simple_program_type() -> None:
    """Whole-program navigation creates no subclass or alternate runtime type."""

    _pending()
