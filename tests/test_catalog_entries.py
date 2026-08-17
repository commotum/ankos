"""Focused integrity checks for the callable-free catalog taxonomy."""

from __future__ import annotations

from dataclasses import fields, is_dataclass

from ca.catalog import entries


HOMES = {
    "automata",
    "substitua",
    "machina",
    "media",
    "criteria",
    "dynamica",
}


def _assert_inert(value: object) -> None:
    assert not callable(value)
    assert type(value) not in (dict, list, set)
    if is_dataclass(value) and not isinstance(value, type):
        for field in fields(value):
            _assert_inert(getattr(value, field.name))
    elif type(value) is tuple:
        for member in value:
            _assert_inert(member)


def test_family_index_is_complete_closed_and_unique() -> None:
    families = entries.FAMILY_ENTRIES

    assert type(families) is tuple
    assert tuple(item.family_id for item in families) == tuple(
        f"SPF{index:03d}" for index in range(1, 61)
    )
    assert len({item.audit_family_id for item in families}) == len(families)
    assert len({(item.home, item.slug) for item in families}) == len(families)
    assert len(
        {(item.constructor_module, item.constructor_name) for item in families}
    ) == len(families)

    for item in families:
        assert item.home in HOMES
        assert item.constructor_module == f"ca.catalog.{item.home}"
        assert item.constructor_name == item.slug.replace("-", "_")
        assert item.closed_parameters
        assert len(set(item.closed_parameters)) == len(item.closed_parameters)
        assert item.source_refs
        assert item.api_pressure_ref == (
            f"goal-5/api-pressure.md:{item.audit_family_id}"
        )


def test_metadata_is_immutable_and_callable_free() -> None:
    _assert_inert(entries.FAMILY_ENTRIES)
    _assert_inert(entries.ROLE_ENTRIES)
    _assert_inert(entries.LEGACY_ENTRIES)
    _assert_inert(entries.NAME_ENTRIES)


def test_close_roles_remain_provenanced_non_family_boundaries() -> None:
    roles = entries.ROLE_ENTRIES
    family_audit_ids = {
        item.audit_family_id for item in entries.FAMILY_ENTRIES
    }

    assert {(item.audit_role_id, item.role_kind) for item in roles} == {
        ("F010", "interface"),
        ("F042", "observer"),
    }
    assert all(item.source_refs and item.boundary for item in roles)
    assert {item.audit_role_id for item in roles}.isdisjoint(family_audit_ids)


def test_legacy_and_public_name_relations_are_referentially_closed() -> None:
    families = {item.family_id: item for item in entries.FAMILY_ENTRIES}
    legacy = {item.legacy_id: item for item in entries.LEGACY_ENTRIES}
    names = {item.spelling: item for item in entries.NAME_ENTRIES}

    assert len(legacy) == len(entries.LEGACY_ENTRIES)
    assert len(names) == len(entries.NAME_ENTRIES)
    assert all(item.disposition in {
        "retain-family",
        "retain-preset",
        "merge",
        "repair",
        "alias",
        "retire-role",
        "split",
    } for item in legacy.values())

    for item in legacy.values():
        assert item.source_refs
        for target in item.targets:
            assert target.target_family_id in families
            assert target.treatment in {"C", "P", "A", "K", "M"}
            assert target.source_refs

    for item in names.values():
        assert item.owner_module in HOMES
        assert item.kind in {"C", "P", "A", "K"}
        assert item.target_family_id in families
        assert item.delegate_import_name.startswith("ca.catalog.")
        assert set(item.legacy_entry_ids) <= set(legacy)
        assert item.source_refs or not item.legacy_entry_ids

    assert {
        item.spelling for item in names.values() if item.kind == "C"
    } == {
        item.constructor_name for item in families.values()
    }


def test_risky_retirement_split_and_preset_migrations_stay_explicit() -> None:
    legacy = {item.legacy_id: item for item in entries.LEGACY_ENTRIES}
    names = {item.spelling: item for item in entries.NAME_ENTRIES}

    assert legacy["T08"].disposition == "retire-role"
    assert legacy["T08"].candidate_ids == ()
    assert legacy["T08"].targets == ()
    assert not any("T08" in item.legacy_entry_ids for item in names.values())

    split = legacy["T40"]
    assert split.disposition == "split"
    assert tuple(
        (
            target.branch_name,
            target.target_family_id,
            target.callable_spelling,
            target.treatment,
        )
        for target in split.targets
    ) == (
        ("sequence", "SPF002", "constant_digit_sequence", "P"),
        ("register", "SPF008", "constant_digit_register", "P"),
    )

    for legacy_id, spelling in (
        ("T32", "template_constraint_system"),
        ("T44", "continuous_cellular_automaton"),
    ):
        assert legacy[legacy_id].disposition == "alias"
        assert legacy[legacy_id].targets[0].treatment == "P"
        assert names[spelling].kind == "P"


def test_alias_adapter_and_split_name_rows_keep_their_family_links() -> None:
    names = {item.spelling: item for item in entries.NAME_ENTRIES}

    assert {
        item.spelling for item in names.values() if item.kind == "A"
    } == {
        "elementary_cellular_automaton",
        "multiway_system",
        "network_rewrite",
        "pde",
    }
    assert names["extended_mobile_automaton"].kind == "K"
    assert not names["extended_mobile_automaton"].flat_export
    assert (
        names["constant_digit_sequence"].target_family_id,
        names["constant_digit_register"].target_family_id,
    ) == ("SPF002", "SPF008")
    assert names["look_and_say"].legacy_entry_ids == ()
    assert names["look_and_say"].source_refs == ("N04:L193-202",)


def test_metadata_exports_publish_the_four_frozen_ledgers() -> None:
    assert {
        "FAMILY_ENTRIES",
        "ROLE_ENTRIES",
        "LEGACY_ENTRIES",
        "NAME_ENTRIES",
    } <= set(entries.__all__)
