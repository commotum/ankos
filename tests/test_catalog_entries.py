"""Independent checks for the callable-free canonical catalog metadata."""

from __future__ import annotations

from collections import Counter
from dataclasses import fields

from ca.catalog import entries


EXPECTED_AUDIT_IDS = tuple(
    f"F{index:03d}"
    for index in range(1, 64)
    if index not in (10, 39, 42)
)
EXPECTED_HOME_COUNTS = {
    "automata": 11,
    "substitua": 15,
    "machina": 8,
    "media": 14,
    "criteria": 9,
    "dynamica": 3,
}
EXPECTED_ROLES = (
    entries.RoleEntry(
        "F010",
        "encode-evolve-decode-interface",
        "interface",
        ("CH11:L15-37", "N11:L674-690"),
        (
            "A concrete encoder or decoder with its own invariant commit may be "
            "an ordinary media program, while composition around an unchanged "
            "target belongs to run/query tooling."
        ),
    ),
    entries.RoleEntry(
        "F042",
        "percolation-connectivity-analysis",
        "observer",
        (
            "BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes.md:"
            "L497-498",
        ),
        (
            "Occupation may be a Seed law, but spanning/connectivity over the "
            "completed sample is an observer or analysis result."
        ),
    ),
)


def test_family_entries_have_the_exact_identity_and_census() -> None:
    families = entries.FAMILY_ENTRIES

    assert type(families) is tuple
    assert len(families) == 60
    assert tuple(item.family_id for item in families) == tuple(
        f"SPF{index:03d}" for index in range(1, 61)
    )
    assert tuple(item.audit_family_id for item in families) == EXPECTED_AUDIT_IDS
    assert Counter(item.home for item in families) == EXPECTED_HOME_COUNTS
    assert Counter(item.coverage for item in families) == {
        "covered": 19,
        "addition": 41,
    }


def test_family_constructor_and_authority_fields_are_closed_and_unique() -> None:
    families = entries.FAMILY_ENTRIES
    constructor_paths = tuple(
        f"{item.constructor_module}.{item.constructor_name}" for item in families
    )

    assert len(set(constructor_paths)) == 60
    assert len({item.slug for item in families}) == 60
    for item in families:
        assert item.constructor_module == f"ca.catalog.{item.home}"
        assert item.constructor_name == item.slug.replace("-", "_")
        assert item.closed_parameters
        assert len(set(item.closed_parameters)) == len(item.closed_parameters)
        assert item.source_refs
        assert item.api_pressure_ref == (
            f"goal-5/api-pressure.md:{item.audit_family_id}"
        )

    by_id = {item.family_id: item for item in families}
    assert by_id["SPF001"].closed_parameters == (
        "seed",
        "partition",
        "block_law",
        "boundary",
        "phase",
    )
    assert by_id["SPF060"].closed_parameters == (
        "input",
        "keystream",
        "alignment",
        "generator",
    )


def test_close_roles_are_exactly_the_two_callable_free_boundaries() -> None:
    assert entries.ROLE_ENTRIES == EXPECTED_ROLES
    assert {item.audit_role_id for item in entries.ROLE_ENTRIES} == {
        "F010",
        "F042",
    }
    assert {item.role_kind for item in entries.ROLE_ENTRIES} == {
        "interface",
        "observer",
    }


def test_metadata_values_contain_no_callables_or_mutable_collections() -> None:
    for item in (*entries.FAMILY_ENTRIES, *entries.ROLE_ENTRIES):
        for field in fields(item):
            value = getattr(item, field.name)
            assert not callable(value)
            assert type(value) not in (dict, list, set)
            if type(value) is tuple:
                assert all(not callable(member) for member in value)


def test_metadata_exports_are_explicit_and_do_not_publish_pending_ledgers() -> None:
    assert "FAMILY_ENTRIES" in entries.__all__
    assert "ROLE_ENTRIES" in entries.__all__
    assert not hasattr(entries, "LEGACY_ENTRIES")
    assert not hasattr(entries, "NAME_ENTRIES")
