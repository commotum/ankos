"""Unit contract for the explicit whole-program catalog assembly."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
import inspect
from itertools import product as cartesian_product
from types import ModuleType

import pytest

import ca
from ca import loci
from ca.catalog import automata, criteria, dynamica, entries, machina, substitua


NAVIGATION_NAMES = (
    "entries",
    "automata",
    "substitua",
    "machina",
    "media",
    "criteria",
    "dynamica",
)


def _assert_inert(value: object) -> None:
    assert not callable(value)
    assert type(value) not in (dict, list, set)
    if is_dataclass(value) and not isinstance(value, type):
        for field in fields(value):
            _assert_inert(getattr(value, field.name))
    elif type(value) is tuple:
        for member in value:
            _assert_inert(member)


def _neighbor_mobile_transitions() -> tuple[
    tuple[
        tuple[int, int, int],
        tuple[tuple[int, int, int], int],
    ],
    ...,
]:
    return tuple(
        (context, (context, 1))
        for context in cartesian_product(range(2), repeat=3)
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


def test_catalog_metadata_is_immutable_and_callable_free() -> None:
    _assert_inert(entries.FAMILY_ENTRIES)
    _assert_inert(entries.ROLE_ENTRIES)
    _assert_inert(entries.LEGACY_ENTRIES)
    _assert_inert(entries.NAME_ENTRIES)

    for owner in (
        automata,
        substitua,
        machina,
        ca.catalog.media,
        criteria,
        dynamica,
    ):
        source = inspect.getsource(owner)
        assert "catalog.entries" not in source
        assert "from . import entries" not in source
        assert "from .entries import" not in source


def test_alias_and_compatibility_relations_preserve_their_public_contracts() -> None:
    for alias, delegate in (
        (substitua.multiway_system, substitua.multiway_rewrite),
        (substitua.network_rewrite, substitua.parallel_network_rewrite),
        (dynamica.pde, dynamica.partial_differential_relation),
    ):
        assert inspect.signature(alias) == inspect.signature(delegate)

    assert inspect.signature(automata.elementary_cellular_automaton) == (
        inspect.signature(automata.eca)
    )
    assert automata.elementary_cellular_automaton(rule=110, width=7) == (
        automata.eca(rule=110, width=7)
    )

    legacy_arguments = {
        "initial": (0, 1, 0),
        "head": 1,
        "colors": 2,
        "transitions": _neighbor_mobile_transitions(),
        "boundary": loci.Boundary(loci.BoundaryPolicy.PERIODIC),
    }
    assert inspect.signature(machina.extended_mobile_automaton) == (
        inspect.signature(machina.neighbor_updating_mobile_automaton)
    )
    with pytest.warns(DeprecationWarning):
        legacy = machina.extended_mobile_automaton(**legacy_arguments)
    assert legacy == machina.neighbor_updating_mobile_automaton(
        **legacy_arguments
    )
