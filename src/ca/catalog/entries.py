"""Callable-free metadata shells for the audited simple-program catalog.

This module owns immutable records for canonical family identity, close roles,
legacy migration, and public-name relations.  It does not own constructors,
component values, program values, registries, lookup dispatch, or execution.
The six category modules build programs without importing this module;
``ca.catalog`` is the sole eventual join between metadata and callables.

Goal 7 will populate these records from ``goal-6/catalog-migration.md`` after
the component mechanics exist.  This skeleton intentionally defines no
metadata values or lookup behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias


CatalogHome: TypeAlias = Literal[
    "automata",
    "substitua",
    "machina",
    "media",
    "criteria",
    "dynamica",
]
Coverage: TypeAlias = Literal["covered", "addition"]
RoleKind: TypeAlias = Literal["interface", "observer"]
LegacyDisposition: TypeAlias = Literal[
    "retain-family",
    "retain-preset",
    "merge",
    "repair",
    "alias",
    "retire-role",
    "split",
]
CallableTreatment: TypeAlias = Literal["C", "P", "A", "K", "M"]
CallableNameKind: TypeAlias = Literal["C", "P", "A", "K"]


@dataclass(frozen=True)
class FamilyEntry:
    """Metadata for exactly one canonical SPF family constructor."""

    family_id: str
    audit_family_id: str
    slug: str
    home: CatalogHome
    constructor_module: str
    constructor_name: str
    coverage: Coverage
    closed_parameters: tuple[str, ...]
    source_refs: tuple[str, ...]
    api_pressure_ref: str
    name_relations: tuple[str, ...]


@dataclass(frozen=True)
class RoleEntry:
    """Metadata for one audited close role with no family constructor."""

    audit_role_id: str
    slug: str
    role_kind: RoleKind
    source_refs: tuple[str, ...]
    boundary: str


@dataclass(frozen=True)
class LegacyEntry:
    """Metadata for one stable T01--T45 migration identity."""

    legacy_id: str
    label: str
    disposition: LegacyDisposition
    candidate_ids: tuple[str, ...]
    source_refs: tuple[str, ...]
    targets: tuple["LegacyTarget", ...]


@dataclass(frozen=True)
class LegacyTarget:
    """One normalized target branch retained by a legacy entry."""

    branch_name: str | None
    target_family_id: str
    callable_spelling: str | None
    treatment: CallableTreatment
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class NameEntry:
    """Callable-free metadata for one canonical or delegating spelling."""

    spelling: str
    owner_module: CatalogHome
    kind: CallableNameKind
    target_family_id: str
    delegate_import_name: str
    flat_export: bool
    closed_binding_summary: str
    legacy_entry_ids: tuple[str, ...]
    source_refs: tuple[str, ...]


__all__ = (
    "CallableNameKind",
    "CallableTreatment",
    "CatalogHome",
    "Coverage",
    "FamilyEntry",
    "LegacyDisposition",
    "LegacyEntry",
    "LegacyTarget",
    "NameEntry",
    "RoleEntry",
    "RoleKind",
)
