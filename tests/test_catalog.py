"""Unit contract for the explicit whole-program catalog assembly."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from fractions import Fraction
import inspect
from itertools import product as cartesian_product
from types import ModuleType

import pytest

import ca
from ca import alphabets, loci, rules, serialization
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


def _components(simple_program: ca.SimpleProgram) -> dict[str, object]:
    return {
        "seed": simple_program.seed,
        "alphabet": simple_program.alphabet,
        "frontier": simple_program.frontier,
        "neighborhood": simple_program.neighborhood,
        "rule": simple_program.rule,
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
    assert len(ca.__all__) == 12


def test_catalog_flat_exports_are_explicit_and_collision_free() -> None:
    expected = {
        item.spelling for item in entries.NAME_ENTRIES if item.flat_export
    }
    actual = set(ca.catalog.__all__) - set(NAVIGATION_NAMES)

    assert len(ca.catalog.__all__) == 111
    assert len(set(ca.catalog.__all__)) == 111
    assert actual == expected
    assert len(actual) == 104
    assert all(callable(getattr(ca.catalog, name)) for name in actual)
    assert not hasattr(ca.catalog, "extended_mobile_automaton")
    assert callable(machina.extended_mobile_automaton)
    assert {
        "fractal_system",
        "network_system",
        "function_combination_system",
    }.isdisjoint(actual)
    assert actual.isdisjoint(set(ca.__all__))


def test_catalog_constructors_return_ordinary_expanded_simple_programs() -> None:
    reference = automata.eca(rule=30, width=5)

    for entry in entries.FAMILY_ENTRIES:
        owner = getattr(ca.catalog, entry.home)
        constructor = getattr(owner, entry.constructor_name)
        constructed = constructor(**_components(reference))

        assert type(constructed) is ca.SimpleProgram
        assert constructed == reference
        assert getattr(ca.catalog, entry.constructor_name) is constructor
        encoded = serialization.dumps(constructed)
        assert serialization.loads(encoded) == serialization.Decoded(
            constructed
        )
        assert b"SPF" not in encoded
        assert b"catalog" not in encoded


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


def test_alias_preset_and_compatibility_relations_preserve_exact_expansion() -> None:
    reference = automata.eca(rule=90, width=5)
    components = _components(reference)

    for alias, delegate in (
        (substitua.multiway_system, substitua.multiway_rewrite),
        (substitua.network_rewrite, substitua.parallel_network_rewrite),
        (dynamica.pde, dynamica.partial_differential_relation),
    ):
        assert inspect.signature(alias) == inspect.signature(delegate)
        assert alias(**components) == delegate(**components)

    assert inspect.signature(automata.elementary_cellular_automaton) == (
        inspect.signature(automata.eca)
    )
    assert automata.elementary_cellular_automaton(rule=110, width=7) == (
        automata.eca(rule=110, width=7)
    )

    eca = automata.eca(rule=30, width=5)
    assert automata.synchronous_local_state_transform(
        **_components(eca)
    ) == eca

    partial = alphabets.word_value((0,), tag="partial")
    templates = alphabets.word_value((0,), tag="templates")
    cardinality = rules.Undetermined(
        rules.literal_expr("not-enumerated"),
        rules.Certificate(
            rules.CertificateKind.CARDINALITY,
            rules.literal_expr("cardinality-obligation"),
        ),
    )
    template = criteria.template_constraint_system(
        partial_assignment=partial,
        allowed_templates=templates,
        relation=rules.literal_expr("satisfies"),
        cardinality=cardinality,
    )
    assert criteria.local_satisfaction_relation(
        **_components(template)
    ) == template
    assert inspect.signature(criteria.template_constraint_system) != (
        inspect.signature(criteria.local_satisfaction_relation)
    )

    continuous = automata.continuous_cellular_automaton(
        initial=(Fraction(1, 2),),
        local_rule=rules.project(rules.group(0), 1),
        boundary=loci.Boundary(
            loci.BoundaryPolicy.FIXED,
            Fraction(0),
        ),
    )
    assert automata.synchronous_local_state_transform(
        **_components(continuous)
    ) == continuous
    assert inspect.signature(automata.continuous_cellular_automaton) != (
        inspect.signature(automata.synchronous_local_state_transform)
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
