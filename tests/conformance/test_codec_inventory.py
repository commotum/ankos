"""G7-02 sealed semantic-variant inventory boundary.

This suite freezes the records and enum variants that G7-03 must encode.  It
does not import or exercise serialization: inventory must precede codecs.
"""

from __future__ import annotations

import csv
from dataclasses import fields, is_dataclass
from enum import Enum
import importlib
from pathlib import Path
import re
from types import ModuleType


OWNER_NAMES = (
    "loci",
    "alphabets",
    "seeds",
    "frontiers",
    "neighborhoods",
    "rules",
    "program",
)
INVENTORY_PATH = (
    Path(__file__).resolve().parents[2] / "goal-7" / "codec-inventory.csv"
)
INVENTORY_COLUMNS = (
    "owner",
    "type",
    "kind",
    "variant",
    "tag",
    "version",
    "exact_fields",
    "wire_value",
    "local_validator",
    "equality_law",
)

_CONTEXT_VALIDATORS = {
    ("rules", "NoPayload"): "Disposition.__post_init__",
    ("rules", "ValuePayload"): "Disposition.__post_init__",
    (
        "program",
        "CompatibilityEvidence",
    ): "_require_compatible_five_fields",
    ("program", "MeasureAbsent"): "fieldless-sum-variant",
}
_CANONICAL_IDENTITY_TYPES = {
    ("loci", "Locus"),
    ("loci", "FreshReference"),
}
_CONFIGURATION_EQUALITY_TYPES = {
    ("loci", "FiniteConfiguration"),
    ("loci", "IntensionalConfiguration"),
}
_SEMANTIC_VALUE_TYPES = {
    ("alphabets", "AlgebraicNumber"),
    ("alphabets", "ExactComplex"),
    ("alphabets", "StructuralReference"),
    ("alphabets", "ValueNode"),
    ("alphabets", "RepresentedNumber"),
}


def _owner_modules() -> tuple[ModuleType, ...]:
    return tuple(importlib.import_module(f"ca.{name}") for name in OWNER_NAMES)


def _public_sealed_types(
    module: ModuleType,
) -> tuple[tuple[str, type[object]], ...]:
    sealed: list[tuple[str, type[object]]] = []
    for name, value in vars(module).items():
        if (
            name.startswith("_")
            or not isinstance(value, type)
            or value.__module__ != module.__name__
        ):
            continue
        if issubclass(value, Enum):
            sealed.append((name, value))
            continue
        parameters = getattr(value, "__dataclass_params__", None)
        if is_dataclass(value) and parameters is not None and parameters.frozen:
            sealed.append((name, value))
    return tuple(sealed)


def _tag(owner_name: str, type_name: str) -> str:
    if owner_name == "program" and type_name == "SimpleProgram":
        return "ca.simple-program"
    kebab = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", type_name).lower()
    return f"ca.{owner_name}.{kebab}"


def _local_validator(owner_name: str, value: type[object]) -> str:
    if "__post_init__" in value.__dict__:
        return f"{value.__name__}.__post_init__"
    return _CONTEXT_VALIDATORS[(owner_name, value.__name__)]


def _equality_law(owner_name: str, type_name: str, *, enum: bool) -> str:
    key = (owner_name, type_name)
    if enum:
        return "enum-member"
    if key in _CANONICAL_IDENTITY_TYPES:
        return "loci.canonical_identity"
    if key in _CONFIGURATION_EQUALITY_TYPES:
        return "loci.configuration_equal"
    if key in _SEMANTIC_VALUE_TYPES:
        return "alphabets.semantic_equal"
    return "structural-fields"


def _inventory_rows() -> tuple[dict[str, str], ...]:
    with INVENTORY_PATH.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        assert tuple(reader.fieldnames or ()) == INVENTORY_COLUMNS
        rows = tuple(reader)
    assert all(
        key is not None and value is not None
        for row in rows
        for key, value in row.items()
    )
    assert all(
        row[column]
        for row in rows
        for column in INVENTORY_COLUMNS
        if column not in {"exact_fields", "wire_value"}
    )
    return rows


def test_codec_inventory_is_exhaustive_and_matches_owner_shapes() -> None:
    rows = _inventory_rows()
    expected_keys: list[tuple[str, str, str]] = []
    expected_fields: dict[tuple[str, str, str], tuple[str, ...]] = {}
    expected_wire_values: dict[tuple[str, str, str], str] = {}

    for module in _owner_modules():
        owner_name = module.__name__.removeprefix("ca.")
        owner = f"ca.{owner_name}"
        for type_name, value in _public_sealed_types(module):
            if issubclass(value, Enum):
                for variant, member in value.__members__.items():
                    key = (owner, type_name, variant)
                    expected_keys.append(key)
                    expected_fields[key] = ("value",)
                    assert type(member.value) is str
                    expected_wire_values[key] = member.value
            else:
                key = (owner, type_name, "record")
                expected_keys.append(key)
                expected_fields[key] = tuple(field.name for field in fields(value))
                expected_wire_values[key] = ""

    actual_keys = [
        (row["owner"], row["type"], row["variant"]) for row in rows
    ]
    assert actual_keys == expected_keys
    assert len(actual_keys) == len(set(actual_keys))

    for row in rows:
        key = (row["owner"], row["type"], row["variant"])
        exact_fields = tuple(
            field for field in row["exact_fields"].split("|") if field
        )
        assert exact_fields == expected_fields[key]
        assert row["wire_value"] == expected_wire_values[key]


def test_codec_inventory_freezes_tags_versions_validators_and_equality() -> None:
    rows = _inventory_rows()
    types_by_owner = {
        module.__name__: dict(_public_sealed_types(module))
        for module in _owner_modules()
    }

    for row in rows:
        owner_name = row["owner"].removeprefix("ca.")
        value = types_by_owner[row["owner"]][row["type"]]
        is_enum = issubclass(value, Enum)

        assert row["kind"] == ("enum-member" if is_enum else "frozen-dataclass")
        assert row["tag"] == _tag(owner_name, row["type"])
        assert row["version"] == "1"
        if not is_enum:
            version_fields = tuple(
                field for field in fields(value) if field.name == "version"
            )
            if version_fields:
                assert len(version_fields) == 1
                assert version_fields[0].default == 1
        assert row["local_validator"] == (
            "Enum.__call__"
            if is_enum
            else _local_validator(owner_name, value)
        )
        assert row["equality_law"] == _equality_law(
            owner_name,
            row["type"],
            enum=is_enum,
        )

    owner_types = {(row["owner"], row["type"]) for row in rows}
    assert len({row["tag"] for row in rows}) == len(owner_types)


def test_inventory_joins_the_closed_production_schema_exactly() -> None:
    """Every CSV obligation has one and only one production schema owner."""

    serialization = importlib.import_module("ca.serialization")
    schema_rows = serialization._schema_rows()
    inventory = _inventory_rows()

    assert len(schema_rows) == len(
        {(row["owner"], row["type"]) for row in inventory}
    )
    assert len(schema_rows) == 178
    by_owner_type = {
        (row.owner, row.type_name): row for row in schema_rows
    }
    assert len(by_owner_type) == len(schema_rows)

    inventory_keys = {
        (row["owner"], row["type"]) for row in inventory
    }
    assert set(by_owner_type) == inventory_keys

    for (owner, type_name), schema in by_owner_type.items():
        rows = tuple(
            row
            for row in inventory
            if row["owner"] == owner and row["type"] == type_name
        )
        assert rows
        assert schema.owner == owner
        assert schema.type_name == type_name
        assert schema.tag == rows[0]["tag"]
        assert schema.version == int(rows[0]["version"])
        assert schema.value_type.__module__ == owner
        assert schema.value_type.__name__ == type_name
        if rows[0]["kind"] == "enum-member":
            assert schema.fields == ("value",)
            assert schema.enum_values == tuple(
                row["wire_value"] for row in rows
            )
            assert tuple(schema.value_type) == tuple(
                schema.value_type(value) for value in schema.enum_values
            )
        else:
            assert len(rows) == 1
            assert schema.enum_values == ()
            assert schema.fields == tuple(
                field
                for field in rows[0]["exact_fields"].split("|")
                if field
            )

    assert set(serialization._SCHEMA_BY_TYPE) == {
        row.value_type for row in schema_rows
    }
    assert set(serialization._SCHEMA_BY_TAG) == {
        row.tag for row in schema_rows
    }
