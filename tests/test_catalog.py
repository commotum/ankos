"""Goal 7 unit-contract skeleton for whole-program catalog assembly.

These tests will cover navigation modules, explicit constructor exports, and
callable-free metadata after reusable mechanics and codecs are complete. The
module is skipped until G7-04 implementation; no skipped assertion is evidence
of conformance.
"""

from typing import NoReturn

import pytest


pytestmark = pytest.mark.skip(
    reason="G7-04 owns the whole-program catalog unit contract"
)


def _pending() -> NoReturn:
    raise NotImplementedError("G7-04 catalog tests are not implemented")


def test_catalog_has_six_explicit_navigation_namespaces() -> None:
    """Automata, substitua, machina, media, criteria, and dynamica are present."""

    _pending()


def test_catalog_flat_exports_are_explicit_and_collision_free() -> None:
    """Preferred spellings are deny-by-default and have one canonical owner."""

    _pending()


def test_catalog_constructors_return_ordinary_expanded_simple_programs() -> None:
    """No constructor creates a subclass, receipt, registry entry, or executor."""

    _pending()


def test_catalog_metadata_is_immutable_and_callable_free() -> None:
    """Entries describe SPF/F/T/name/source relations without semantic objects."""

    _pending()


def test_alias_preset_and_compatibility_relations_preserve_exact_expansion() -> None:
    """A/P/K spellings obey their declared argument and payload relations."""

    _pending()
