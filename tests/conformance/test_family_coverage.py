"""Goal 7 exact sixty-family coverage join.

G7-02 owns the mechanics partition, direct ordinary-program fixtures,
secondary pressure joins, and exclusions.  G7-04 will add the canonical
constructor and metadata joins without changing this mechanics ledger.
"""

from collections import Counter

import pytest

from g7_mechanics import (
    MECHANICS_ROWS,
    PRIMARY_PRESSURES,
    SECONDARY_JOINS,
    WORKSTREAM_COUNTS,
)



def test_primary_pressure_partition_contains_each_spf001_through_spf060_once() -> None:
    """The twelve primary partitions have no duplicate, omission, or extra row."""

    expected = tuple(f"SPF{index:03d}" for index in range(1, 61))
    actual = tuple(sorted(row.spf for row in MECHANICS_ROWS))

    assert actual == expected
    assert len({row.family for row in MECHANICS_ROWS}) == 60
    assert set(row.primary for row in MECHANICS_ROWS) == set(PRIMARY_PRESSURES)
    assert Counter(row.workstream for row in MECHANICS_ROWS) == dict(
        WORKSTREAM_COUNTS
    )


@pytest.mark.skip(reason="G7-04 owns canonical catalog constructor expansion")
def test_every_family_constructor_returns_a_closed_compatible_simple_program() -> None:
    """One representative closed argument set expands each canonical constructor."""

    raise AssertionError("G7-04 catalog constructor join is not active")


@pytest.mark.skip(reason="G7-04 owns callable-free catalog provenance metadata")
def test_every_family_joins_exact_spf_f_home_source_and_pressure_metadata() -> None:
    """Callable expansion and callable-free provenance agree row by row."""

    raise AssertionError("G7-04 catalog metadata join is not active")


@pytest.mark.skip(reason="G7-02 direct mechanics fixtures are being implemented")
def test_every_family_runs_its_named_fixture_through_generic_application() -> None:
    """Finite and intensional cases use the same denotational boundary."""

    raise AssertionError("G7-02 mechanics fixture join is not active")


def test_all_eight_secondary_pressure_joins_are_present_exactly() -> None:
    """The deliberate PX03, PX04, and six PX08 cross-cuts remain covered."""

    actual = tuple(
        sorted(
            (row.spf, pressure)
            for row in MECHANICS_ROWS
            for pressure in row.secondary
        )
    )
    assert actual == tuple(sorted(SECONDARY_JOINS))


def test_close_roles_and_retired_seed_role_are_excluded_from_sixty_rows() -> None:
    """F010, F042, and T08 are never smuggled into executable family coverage."""

    family_ids = {row.family for row in MECHANICS_ROWS}
    spf_ids = {row.spf for row in MECHANICS_ROWS}

    assert {"F010", "F042"}.isdisjoint(family_ids)
    assert "T08" not in family_ids
    assert all(value.startswith("SPF") for value in spf_ids)
