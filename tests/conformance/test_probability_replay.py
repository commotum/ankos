"""CT06 skeleton: probability laws, Seed realization, and replay.

The implemented suite will keep denotational laws separate from externally
authorized draws and retain exact unrenormalized measure views. This module
remains skipped until implementation; skips are not conformance evidence.
"""

from typing import NoReturn

import pytest


pytestmark = pytest.mark.skip(
    reason="Goal 7 CT06 probability/replay skeleton; implementation is pending"
)


def _pending() -> NoReturn:
    raise NotImplementedError("Goal 7 CT06 tests are not implemented")


def test_rule_law_contains_no_draw_and_applied_mass_is_preserved() -> None:
    """Applied, successor, and no-successor measures retain tagged total mass."""

    _pending()


def test_replay_is_deterministic_and_traversal_order_independent() -> None:
    """Law, lineage, key, and profile determine evidence without ambient RNG."""

    _pending()


def test_seed_law_handles_no_key_keyed_realization_and_explicit_initial() -> None:
    """Complete law, authorized draw, and validation bypass remain distinct."""

    _pending()


def test_unavailable_is_narrowly_limited_to_successor_quotient_measure() -> None:
    """Malformed source or applied mappings reject instead of becoming unavailable."""

    _pending()
