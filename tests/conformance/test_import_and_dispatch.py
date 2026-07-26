"""CT13 skeleton: import ownership and absence of semantic dispatch.

The implemented suite will combine static dependency inspection with blocked
catalog execution and rollout/apply call-path proofs. This module remains
skipped until implementation; skips are not conformance evidence.
"""

from typing import NoReturn

import pytest


pytestmark = pytest.mark.skip(
    reason="Goal 7 CT13 import/dispatch skeleton; implementation is pending"
)


def _pending() -> NoReturn:
    raise NotImplementedError("Goal 7 CT13 tests are not implemented")


def test_static_import_graph_matches_the_one_way_semantic_dag() -> None:
    """Core, serialization, catalog, façade, and auxiliaries import only downward."""

    _pending()


def test_apply_and_decode_work_while_catalog_imports_are_blocked() -> None:
    """Expanded values never require constructor or metadata lookup."""

    _pending()


def test_generic_application_contains_no_family_or_descriptor_dispatch() -> None:
    """SPF/F/T IDs, carrier labels, locus kinds, and Rule tags select no engine."""

    _pending()


def test_public_surface_submodules_and_signatures_are_exact() -> None:
    """Callable rollout, absent obsolete modules, and forbidden keywords are checked."""

    _pending()


def test_rollout_matches_manual_repeated_apply_for_deterministic_and_branching_cases() -> None:
    """A spy and static call graph prove that traversal owns no second step law."""

    _pending()
