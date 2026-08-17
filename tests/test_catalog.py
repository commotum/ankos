"""Unit contract for the explicit whole-program catalog assembly."""

from __future__ import annotations

import inspect
from types import ModuleType

import ca
from ca.catalog import entries


NAVIGATION_NAMES = (
    "entries",
    "automata",
    "substitua",
    "machina",
    "media",
    "criteria",
    "dynamica",
)


def test_catalog_has_six_explicit_navigation_namespaces() -> None:
    assert tuple(ca.catalog.__all__[:7]) == NAVIGATION_NAMES
    for name in NAVIGATION_NAMES:
        namespace = getattr(ca.catalog, name)
        assert type(namespace) is ModuleType
        assert namespace.__name__ == f"ca.catalog.{name}"

    assert ca.catalog is __import__("ca.catalog", fromlist=["catalog"])
    assert "catalog" in ca.__all__


def test_catalog_flat_exports_are_explicit_and_collision_free() -> None:
    expected = {
        item.spelling for item in entries.NAME_ENTRIES if item.flat_export
    }
    actual = set(ca.catalog.__all__) - set(NAVIGATION_NAMES)

    assert len(ca.catalog.__all__) == len(set(ca.catalog.__all__))
    assert actual == expected
    assert all(callable(getattr(ca.catalog, name)) for name in actual)
    assert not hasattr(ca.catalog, "extended_mobile_automaton")
    assert callable(machina.extended_mobile_automaton)
    assert {
        "fractal_system",
        "network_system",
        "function_combination_system",
    }.isdisjoint(actual)
    assert actual.isdisjoint(set(ca.__all__))


def test_canonical_builder_signatures_match_their_semantic_metadata() -> None:
    for entry in entries.FAMILY_ENTRIES:
        owner = getattr(ca.catalog, entry.home)
        builder = getattr(owner, entry.constructor_name)
        parameters = tuple(inspect.signature(builder).parameters.values())

        assert tuple(parameter.name for parameter in parameters) == (
            entry.closed_parameters
        )
        assert all(
            parameter.kind is inspect.Parameter.KEYWORD_ONLY
            for parameter in parameters
        )
        assert all(
            parameter.default is inspect.Parameter.empty
            for parameter in parameters
        )
        assert getattr(ca.catalog, entry.constructor_name) is builder
