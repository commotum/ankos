"""CT11 skeleton: catalog expansion and exact T01–T45 migration.

The implemented suite will transcribe the authoritative migration ledger as
test data while keeping runtime metadata callable-free and non-semantic. This
module remains skipped until implementation; skips are not conformance
evidence.
"""

from typing import NoReturn

import pytest


pytestmark = pytest.mark.skip(
    reason="G7-04 owns the CT11 catalog-expansion contract"
)


def _pending() -> NoReturn:
    raise NotImplementedError("G7-04 CT11 tests are not implemented")


def test_sixty_canonical_constructors_have_exact_metadata_and_one_home() -> None:
    """Every SPF row expands once through its locked category owner."""

    _pending()


def test_t01_through_t45_match_the_exact_expected_migration_manifest() -> None:
    """Targets, kinds, spellings, bindings, owners, and exports match row by row."""

    _pending()


def test_canonical_preset_alias_and_compatibility_relations_are_exact() -> None:
    """C/P/A/K callables obey their expansion or total translation contracts."""

    _pending()


def test_flat_qualified_and_metadata_only_names_obey_the_export_contract() -> None:
    """All C/P/A are flat, the sole K is qualified, and M is never callable."""

    _pending()


def test_t08_t40_t32_and_t44_keep_their_special_dispositions() -> None:
    """Zero/two targets and the two preset-not-alias decisions remain explicit."""

    _pending()
