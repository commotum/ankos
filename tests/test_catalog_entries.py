"""Independent checks for the callable-free canonical catalog metadata."""

from __future__ import annotations

from collections import Counter
from dataclasses import fields, is_dataclass

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
            "BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes/07-Mechanisms-in-Programs-and-Nature-Notes.md:"
            "L497-498",
        ),
        (
            "Occupation may be a Seed law, but spanning/connectivity over the "
            "completed sample is an observer or analysis result."
        ),
    ),
)
EXPECTED_LEGACY_DISPOSITIONS = {
    "retain-family": 15,
    "retain-preset": 21,
    "merge": 2,
    "repair": 3,
    "alias": 2,
    "retire-role": 1,
    "split": 1,
}
EXPECTED_NAME_KINDS = {"C": 60, "P": 40, "A": 4, "K": 1}


def _assert_inert(value: object) -> None:
    assert not callable(value)
    assert type(value) not in (dict, list, set)
    if is_dataclass(value) and not isinstance(value, type):
        for field in fields(value):
            _assert_inert(getattr(value, field.name))
    elif type(value) is tuple:
        for member in value:
            _assert_inert(member)


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
    _assert_inert(entries.FAMILY_ENTRIES)
    _assert_inert(entries.ROLE_ENTRIES)
    _assert_inert(entries.LEGACY_ENTRIES)
    _assert_inert(entries.NAME_ENTRIES)


def test_legacy_entries_have_the_exact_identity_census_and_target_shapes() -> None:
    legacy = entries.LEGACY_ENTRIES

    assert type(legacy) is tuple
    assert tuple(item.legacy_id for item in legacy) == tuple(
        f"T{index:02d}" for index in range(1, 46)
    )
    assert Counter(item.disposition for item in legacy) == (
        EXPECTED_LEGACY_DISPOSITIONS
    )
    assert {item.legacy_id: len(item.targets) for item in legacy} == {
        **{f"T{index:02d}": 1 for index in range(1, 46)},
        "T08": 0,
        "T40": 2,
    }

    by_id = {item.legacy_id: item for item in legacy}
    assert by_id["T01"] == entries.LegacyEntry(
        "T01",
        "Elementary Cellular Automata",
        "retain-family",
        ("C090",),
        ("CH03:L29-56",),
        (
            entries.LegacyTarget(
                None, "SPF050", "eca", "P", ("CH03:L29-56",)
            ),
        ),
    )
    assert by_id["T10"].targets == (
        entries.LegacyTarget(
            None,
            "SPF030",
            "neighbor_updating_mobile_automaton",
            "P",
            ("CH03:L197-207",),
        ),
    )
    assert by_id["T29"].targets == (
        entries.LegacyTarget(
            None,
            "SPF038",
            "parallel_network_rewrite",
            "C",
            ("CH05:L239-248,L287-331",),
        ),
    )
    assert by_id["T40"].candidate_ids == ("C003", "C017")
    assert by_id["T40"].targets == (
        entries.LegacyTarget(
            "sequence",
            "SPF002",
            "constant_digit_sequence",
            "P",
            ("N04:L203-210,L569-599",),
        ),
        entries.LegacyTarget(
            "register",
            "SPF008",
            "constant_digit_register",
            "P",
            ("CH04:L303-308,L343-350", "N04:L561-562"),
        ),
    )
    assert by_id["T45"].targets == (
        entries.LegacyTarget(
            None,
            "SPF039",
            "partial_differential_relation",
            "C",
            ("CH04:L625-674", "N04:L933-940"),
        ),
    )
    assert by_id["T14"].candidate_ids == ("C011", "C055")
    assert by_id["T33"].candidate_ids == ("C042", "C043")


def test_name_entries_have_the_exact_public_census_and_closed_joins() -> None:
    names = entries.NAME_ENTRIES
    family_ids = {item.family_id for item in entries.FAMILY_ENTRIES}

    assert type(names) is tuple
    assert len(names) == 105
    assert len({item.spelling for item in names}) == 105
    assert Counter(item.kind for item in names) == EXPECTED_NAME_KINDS
    assert sum(item.flat_export for item in names) == 104
    assert {item.spelling for item in names if not item.flat_export} == {
        "extended_mobile_automaton"
    }
    assert {item.target_family_id for item in names} <= family_ids
    assert all(item.delegate_import_name.startswith("ca.catalog.") for item in names)
    assert {
        item.spelling for item in names if item.kind == "C"
    } == {
        item.constructor_name for item in entries.FAMILY_ENTRIES
    }
    assert {item.spelling for item in names if item.kind == "A"} == {
        "elementary_cellular_automaton",
        "multiway_system",
        "network_rewrite",
        "pde",
    }
    assert {item.spelling for item in names if item.kind == "K"} == {
        "extended_mobile_automaton"
    }

    legacy_relation_kinds = Counter(
        item.kind for item in names if item.legacy_entry_ids
    )
    assert legacy_relation_kinds == {"C": 5, "P": 39, "A": 4, "K": 1}
    legacy_ids = {item.legacy_id for item in entries.LEGACY_ENTRIES}
    assert {
        legacy_id
        for item in names
        for legacy_id in item.legacy_entry_ids
    } <= legacy_ids


def test_name_entries_preserve_special_alias_adapter_split_and_preset_rows() -> None:
    by_name = {item.spelling: item for item in entries.NAME_ENTRIES}

    assert by_name["elementary_cellular_automaton"] == entries.NameEntry(
        "elementary_cellular_automaton",
        "automata",
        "A",
        "SPF050",
        "ca.catalog.automata.eca",
        True,
        (
            "Bind binary 1-D radius-one synchronous feedback; family constructor "
            "remains synchronous_local_state_transform."
        ),
        ("T01",),
        ("CH03:L29-56",),
    )
    assert by_name["extended_mobile_automaton"] == entries.NameEntry(
        "extended_mobile_automaton",
        "machina",
        "K",
        "SPF030",
        "ca.catalog.machina.neighbor_updating_mobile_automaton",
        False,
        (
            "Correctly bind the neighbor-updating fixed-block result; deprecated "
            "old name delegates losslessly."
        ),
        ("T10",),
        ("CH03:L197-207",),
    )
    assert (
        by_name["network_rewrite"].delegate_import_name
        == "ca.catalog.substitua.parallel_network_rewrite"
    )
    assert (
        by_name["multiway_system"].delegate_import_name
        == "ca.catalog.substitua.multiway_rewrite"
    )
    assert (
        by_name["pde"].delegate_import_name
        == "ca.catalog.dynamica.partial_differential_relation"
    )
    assert (
        by_name["constant_digit_sequence"].target_family_id,
        by_name["constant_digit_register"].target_family_id,
    ) == ("SPF002", "SPF008")
    assert by_name["look_and_say"].legacy_entry_ids == ()
    assert by_name["look_and_say"].source_refs == ("N04:L193-202",)


def test_metadata_exports_are_explicit_and_publish_all_frozen_ledgers() -> None:
    assert {
        "FAMILY_ENTRIES",
        "ROLE_ENTRIES",
        "LEGACY_ENTRIES",
        "NAME_ENTRIES",
    } <= set(entries.__all__)
