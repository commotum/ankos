"""CT03 skeleton: validation phase order and no-commit failure.

The implemented suite will use private test instrumentation around ordinary
closed descriptors, never public observers or stateful semantic callbacks.
This module remains skipped until implementation; skips are not conformance
evidence.
"""

from typing import NoReturn

import pytest


pytestmark = pytest.mark.skip(
    reason="Goal 7 CT03 validation-phase skeleton; implementation is pending"
)


def _pending() -> NoReturn:
    raise NotImplementedError("Goal 7 CT03 tests are not implemented")


def test_application_runs_the_exact_generic_phase_order() -> None:
    """Program through quotient/measure phases execute in the settled sequence."""

    _pending()


def test_first_failing_phase_prevents_every_later_phase() -> None:
    """Each phase fault is canonical and later semantic work is absent."""

    _pending()


def test_one_invalid_atom_rejects_the_complete_finite_rule_space() -> None:
    """A valid-looking subset never becomes authoritative."""

    _pending()


def test_rejection_preserves_input_and_publishes_no_authoritative_result() -> None:
    """No candidate, successor, or cardinality leaks across a failed boundary."""

    _pending()
