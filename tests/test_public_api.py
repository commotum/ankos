"""Goal 7 unit-contract skeleton for the curated package façade.

These tests will assert the final root spelling after the atomic cutover while
keeping component records and catalog constructors owner-qualified. The module
is skipped until that cutover; no skipped assertion is evidence of
conformance.
"""

from typing import NoReturn

import pytest


pytestmark = pytest.mark.skip(
    reason="Goal 7 public API contract skeleton; atomic cutover is pending"
)


def _pending() -> NoReturn:
    raise NotImplementedError("Goal 7 public API tests are not implemented")


def test_root_exports_only_the_settled_namespaces_and_three_conveniences() -> None:
    """Root exposes module namespaces plus SimpleProgram, apply, and rollout."""

    _pending()


def test_component_and_catalog_constructors_are_module_qualified() -> None:
    """Reusable components and whole-program names occupy distinct namespaces."""

    _pending()


def test_apply_and_rollout_have_the_exact_public_signatures() -> None:
    """Base operations accept no solver, observer, policy, or renderer keywords."""

    _pending()


def test_rollout_is_callable_and_has_no_shadowing_public_submodule() -> None:
    """The final package physically lacks ca.rollout as a module."""

    _pending()


def test_obsolete_modules_exports_and_eager_auxiliaries_are_absent() -> None:
    """Legacy façades and downstream datasets/RNG/viz do not enter root import."""

    _pending()
