"""CT11: catalog expansion and exact T01–T45 migration."""

from __future__ import annotations

from collections import Counter
from dataclasses import fields
from fractions import Fraction
from itertools import product

import pytest

import ca
from ca import alphabets, loci, rules
from ca.catalog import automata, criteria, entries, machina, media, substitua

from g7_catalog_manifest import (
    CANONICAL_NAME_RELATIONS,
    CANONICAL_ROWS,
    EXPECTED_COVERAGE_COUNTS,
    EXPECTED_HOME_COUNTS,
    EXPECTED_NAME_KIND_COUNTS,
    LEGACY_CALLABLE_ROWS,
    LEGACY_ROWS,
    LEGACY_TARGET_ROWS,
    METADATA_ONLY_SPELLINGS,
)


_FIVE_FIELDS = ("seed", "alphabet", "frontier", "neighborhood", "rule")
_RESERVED_CATALOG_EXPORTS = {
    "entries",
    "automata",
    "substitua",
    "machina",
    "media",
    "criteria",
    "dynamica",
}


def _program_arguments(simple_program: ca.SimpleProgram) -> dict[str, object]:
    return {
        name: getattr(simple_program, name)
        for name in _FIVE_FIELDS
    }


def _canonical_rows_by_id() -> dict[str, tuple[str, ...]]:
    return {row[0]: row for row in CANONICAL_ROWS}


def _canonical_callable(family_id: str):
    row = _canonical_rows_by_id()[family_id]
    slug, home = row[2], row[3]
    return getattr(getattr(ca.catalog, home), slug.replace("-", "_"))


def _evidence() -> rules.EvidenceTerm:
    return rules.EvidenceTerm("ct11-source", ("literal-fixture",))


def _grid(
    value: alphabets.SemanticValue,
    *,
    tag: str = "ct11-grid",
) -> alphabets.ValueNode:
    return alphabets.grid_field_value(
        ("x", "y"),
        (1, 1),
        (value,),
        tag=tag,
    )


def _map(
    *items: tuple[alphabets.SemanticValue, alphabets.SemanticValue],
    tag: str = "ct11-map",
) -> alphabets.ValueNode:
    return alphabets.map_value(
        tuple(
            alphabets.map_entry_value(key, value)
            for key, value in items
        ),
        tag=tag,
    )


def _mobile_transitions(
    *,
    neighbor_updating: bool,
) -> tuple:
    if neighbor_updating:
        return tuple(
            (key, (key, 1))
            for key in product(range(2), repeat=3)
        )
    return tuple(
        (key, (key[1], 1))
        for key in product(range(2), repeat=3)
    )


def _generalized_mobile_transitions() -> tuple:
    return tuple(
        (key, (key[1], (0,)))
        for key in product(range(2), repeat=3)
    )


def _criterion_arguments() -> dict[str, object]:
    partial_assignment = _map(("left", 0), ("right", 1), tag="assignment")
    allowed_templates = alphabets.word_value(
        (alphabets.word_value((0, 1), tag="template"),),
        tag="allowed-templates",
    )
    cardinality = rules.Undetermined(
        rules.literal_expr("ct11:not-enumerated"),
        rules.Certificate(
            rules.CertificateKind.CARDINALITY,
            rules.literal_expr("ct11:cardinality-obligation"),
        ),
    )
    return {
        "partial_assignment": partial_assignment,
        "allowed_templates": allowed_templates,
        "predicates": alphabets.word_value(
            (alphabets.symbolic_value("not-equal", items=("left", "right")),),
            tag="predicates",
        ),
        "required_occurrences": (
            alphabets.record_value(
                (
                    ("position", 0),
                    (
                        "template",
                        alphabets.word_value((0, 1), tag="template"),
                    ),
                ),
                tag="required-occurrence",
            ),
        ),
        "relation": rules.literal_expr("ct11:candidate-satisfies-constraints"),
        "cardinality": cardinality,
    }


def _preset_programs() -> dict[str, ca.SimpleProgram]:
    binary_table = (0,) * 8
    two_symbols = (0, 1)
    initial_word = (0, 1, 0)
    independent_productions = ((0, (0, 1)), (1, (1,)))
    contextual_productions = tuple(
        (context, (context[0],))
        for context in product(two_symbols, repeat=2)
    )
    tag_appendants = (((0,), (1,)), ((1,), (0,)))

    field_zero = _grid(0)
    tile_zero = _grid(0, tag="ct11-tile")
    mosaic_productions = _map((0, tile_zero), tag="mosaic-productions")
    contextual_mosaic_productions = _map(
        (
            alphabets.word_value(
                (0, 0, 0, 0),
                tag="mosaic-context",
            ),
            tile_zero,
        ),
        tag="contextual-mosaic-productions",
    )

    rewrite = alphabets.rewrite_rule_value(
        alphabets.pattern_node(
            "identity",
            (alphabets.pattern_bind("value"),),
        ),
        alphabets.template_node(
            "identity",
            (alphabets.template_binding("value"),),
        ),
    )
    rewrites = alphabets.rewrite_rules_value((rewrite,))

    criterion = _criterion_arguments()
    register_law = rules.add(
        rules.record_field(rules.observation(0), "register"),
        rules.literal_expr(1),
    )
    observed_integer = rules.observation(0)

    programs = {
        "eca": automata.eca(rule=30, width=5),
        "multicolor_cellular_automaton": (
            automata.multicolor_cellular_automaton(
                initial=initial_word,
                colors=2,
                rule=binary_table,
            )
        ),
        "totalistic_cellular_automaton": (
            automata.totalistic_cellular_automaton(
                initial=initial_word,
                colors=2,
                rule=(0,) * 4,
            )
        ),
        "three_color_totalistic_cellular_automaton": (
            automata.three_color_totalistic_cellular_automaton(
                initial=(0, 1, 2),
                rule=(0,) * 7,
            )
        ),
        "higher_color_totalistic_cellular_automaton": (
            automata.higher_color_totalistic_cellular_automaton(
                initial=(0, 1, 2, 3),
                colors=4,
                rule=(0,) * 10,
            )
        ),
        "quiescent_cellular_automaton": (
            automata.quiescent_cellular_automaton(
                initial=initial_word,
                colors=2,
                rule=binary_table,
            )
        ),
        "symmetric_cellular_automaton": (
            automata.symmetric_cellular_automaton(
                initial=initial_word,
                colors=2,
                rule=binary_table,
            )
        ),
        "mobile_automaton": machina.mobile_automaton(
            initial=initial_word,
            head=1,
            colors=2,
            transitions=_mobile_transitions(neighbor_updating=False),
        ),
        "neighbor_updating_mobile_automaton": (
            machina.neighbor_updating_mobile_automaton(
                initial=initial_word,
                head=1,
                colors=2,
                transitions=_mobile_transitions(neighbor_updating=True),
            )
        ),
        "generalized_mobile_automaton": (
            automata.generalized_mobile_automaton(
                initial=initial_word,
                active=(1,),
                colors=2,
                transitions=_generalized_mobile_transitions(),
            )
        ),
        "turing_machine": machina.turing_machine(
            tape=initial_word,
            head=1,
            initial_state="q",
            states=("q",),
            symbols=2,
            transitions=(),
        ),
        "neighbor_independent_substitution": (
            substitua.neighbor_independent_substitution(
                symbols=two_symbols,
                initial=initial_word,
                productions=independent_productions,
            )
        ),
        "neighbor_dependent_substitution": (
            substitua.neighbor_dependent_substitution(
                symbols=two_symbols,
                initial=initial_word,
                productions=contextual_productions,
            )
        ),
        "creation_destruction_substitution": (
            substitua.creation_destruction_substitution(
                symbols=two_symbols,
                initial=initial_word,
                productions=((0, ()), (1, (0, 1))),
            )
        ),
        "sequential_substitution": substitua.sequential_substitution(
            symbols=two_symbols,
            initial=initial_word,
            clauses=(((0, 1), (1, 0)),),
        ),
        "tag_system": substitua.tag_system(
            symbols=two_symbols,
            initial=initial_word,
            n=1,
            appendants=tag_appendants,
        ),
        "cyclic_tag_system": substitua.cyclic_tag_system(
            initial=(True, False),
            blocks=((True,), (False,)),
        ),
        "symbolic_system": substitua.symbolic_system(
            expression=alphabets.symbolic_value(
                "identity",
                items=("x",),
            ),
            rewrites=rewrites,
        ),
        "cellular_automaton_2d": automata.cellular_automaton_2d(
            shape=(1, 1),
            initial=(0,),
            colors=2,
            rule=(0,) * 32,
        ),
        "moore_cellular_automaton": automata.moore_cellular_automaton(
            shape=(1, 1),
            initial=(0,),
            colors=2,
            rule=(0,) * 512,
        ),
        "cellular_automaton_3d": automata.cellular_automaton_3d(
            shape=(1, 1, 1),
            initial=(0,),
            colors=2,
            offsets=((0, 0, 0),),
            rule=(0, 1),
        ),
        "lattice_cellular_automaton": automata.lattice_cellular_automaton(
            shape=(1, 1, 1, 1),
            initial=(0,),
            colors=2,
            offsets=((0, 0, 0, 0),),
            rule=(0, 1),
            axes=("a", "b", "c", "d"),
        ),
        "turing_machine_2d": machina.turing_machine_2d(
            shape=(1, 1),
            tape=(0,),
            head=(0, 0),
            initial_state="q",
            states=("q",),
            symbols=2,
            transitions=(),
        ),
        "substitution_system_2d": substitua.substitution_system_2d(
            symbols=(0,),
            initial=field_zero,
            productions=mosaic_productions,
        ),
        "geometric_substitution": substitua.geometric_substitution(
            seed=field_zero,
            productions=mosaic_productions,
        ),
        "context_dependent_substitution_2d": (
            substitua.context_dependent_substitution_2d(
                symbols=(0,),
                initial=field_zero,
                productions=contextual_mosaic_productions,
            )
        ),
        "local_constraint_system": criteria.local_constraint_system(
            partial_assignment=criterion["partial_assignment"],
            predicates=criterion["predicates"],
            relation=criterion["relation"],
            cardinality=criterion["cardinality"],
        ),
        "template_constraint_system": criteria.template_constraint_system(
            partial_assignment=criterion["partial_assignment"],
            allowed_templates=criterion["allowed_templates"],
            relation=criterion["relation"],
            cardinality=criterion["cardinality"],
        ),
        "seeded_template_constraint_system": (
            criteria.seeded_template_constraint_system(
                partial_assignment=criterion["partial_assignment"],
                allowed_templates=criterion["allowed_templates"],
                required_occurrences=criterion["required_occurrences"],
                relation=criterion["relation"],
                cardinality=criterion["cardinality"],
            )
        ),
        "arithmetic_iteration": automata.arithmetic_iteration(
            initial=1,
            alphabet=alphabets.integers(),
            map_expression=rules.add(
                observed_integer,
                rules.literal_expr(1),
            ),
        ),
        "piecewise_integer_map": automata.piecewise_integer_map(
            initial=1,
            cases=(
                (
                    2,
                    0,
                    rules.add(observed_integer, rules.literal_expr(2)),
                ),
            ),
            otherwise=rules.add(
                observed_integer,
                rules.literal_expr(1),
            ),
        ),
        "digit_reversal_map": automata.digit_reversal_map(
            initial=6,
            base=2,
        ),
        "recursive_sequence": substitua.recursive_sequence(
            prefix=(1, 1),
            coefficients=(1, 1),
        ),
        "variable_index_recursive_sequence": (
            substitua.variable_index_recursive_sequence(
                prefix=(1,),
                recurrence=rules.literal_expr(1),
            )
        ),
        "number_theoretic_filtering": (
            substitua.number_theoretic_filtering(upper=5)
        ),
        "constant_digit_sequence": substitua.constant_digit_sequence(
            base=10,
            prefix=(3,),
            next_digit=rules.literal_expr(1),
            source_evidence=_evidence(),
        ),
        "constant_digit_register": media.constant_digit_register(
            register=9,
            register_law=register_law,
            digit_projection=rules.modulo(register_law, 10),
        ),
        "continued_fraction_substitution": (
            substitua.continued_fraction_substitution(
                continued_fraction=(1, 2),
                source_evidence=_evidence(),
            )
        ),
        "continuous_cellular_automaton": (
            automata.continuous_cellular_automaton(
                initial=(Fraction(0), Fraction(1, 2)),
                local_rule=rules.project(rules.group(0), 1),
            )
        ),
        "look_and_say": media.look_and_say(digits=(1, 1, 2)),
    }
    assert all(type(item) is ca.SimpleProgram for item in programs.values())
    return programs


def test_sixty_canonical_constructors_have_exact_metadata_and_one_home() -> None:
    """Every SPF row expands once through its locked category owner."""

    actual_rows = tuple(
        (
            item.family_id,
            item.audit_family_id,
            item.slug,
            item.home,
            item.coverage,
            ";".join(item.closed_parameters),
            ";".join(item.source_refs),
        )
        for item in entries.FAMILY_ENTRIES
    )

    assert actual_rows == CANONICAL_ROWS
    assert Counter(item.home for item in entries.FAMILY_ENTRIES) == (
        EXPECTED_HOME_COUNTS
    )
    assert Counter(item.coverage for item in entries.FAMILY_ENTRIES) == (
        EXPECTED_COVERAGE_COUNTS
    )
    assert tuple(
        (
            item.constructor_module,
            item.constructor_name,
            item.api_pressure_ref,
            item.name_relations,
        )
        for item in entries.FAMILY_ENTRIES
    ) == tuple(
        (
            f"ca.catalog.{row[3]}",
            row[2].replace("-", "_"),
            f"goal-5/api-pressure.md:{row[1]}",
            CANONICAL_NAME_RELATIONS.get(row[0], ()),
        )
        for row in CANONICAL_ROWS
    )

    reference = automata.eca(rule=30, width=5)
    for row in CANONICAL_ROWS:
        constructor = _canonical_callable(row[0])
        constructed = constructor(**_program_arguments(reference))
        reexpanded = constructor(**_program_arguments(constructed))

        assert type(constructed) is ca.SimpleProgram
        assert reexpanded == constructed
        assert tuple(field.name for field in fields(constructed)) == _FIVE_FIELDS
        assert set(constructed.__dict__) == set(_FIVE_FIELDS)


def test_t01_through_t45_match_the_exact_expected_migration_manifest() -> None:
    """Targets, kinds, spellings, bindings, owners, and exports match row by row."""

    actual_rows = tuple(
        (
            item.legacy_id,
            item.label,
            item.disposition,
            ",".join(item.candidate_ids),
            ";".join(item.source_refs),
        )
        for item in entries.LEGACY_ENTRIES
    )
    actual_targets = tuple(
        (
            item.legacy_id,
            target.branch_name or "-",
            target.target_family_id,
            target.callable_spelling or "-",
            target.treatment,
            ";".join(target.source_refs),
        )
        for item in entries.LEGACY_ENTRIES
        for target in item.targets
    )

    assert actual_rows == LEGACY_ROWS
    assert actual_targets == LEGACY_TARGET_ROWS

    actual_callable_relations = tuple(
        (
            item.spelling,
            item.owner_module,
            item.kind,
            item.target_family_id,
            (
                item.closed_binding_summary
                if item.kind == "P"
                else item.delegate_import_name
            ),
            "1" if item.flat_export else "0",
            ",".join(item.legacy_entry_ids),
            ";".join(item.source_refs),
        )
        for item in entries.NAME_ENTRIES
        if item.legacy_entry_ids
    )

    assert actual_callable_relations == LEGACY_CALLABLE_ROWS
    assert len(actual_callable_relations) == 49
    assert Counter(row[2] for row in actual_callable_relations) == {
        "C": 5,
        "P": 39,
        "A": 4,
        "K": 1,
    }


def test_canonical_preset_alias_and_compatibility_relations_are_exact() -> None:
    """C/P/A/K callables obey their expansion or total translation contracts."""

    programs = _preset_programs()
    expected_presets = {
        row[0]
        for row in LEGACY_CALLABLE_ROWS
        if row[2] == "P"
    } | {"look_and_say"}

    assert set(programs) == expected_presets
    assert len(programs) == 40

    target_by_spelling = {
        row[0]: row[3]
        for row in LEGACY_CALLABLE_ROWS
        if row[2] == "P"
    }
    target_by_spelling["look_and_say"] = "SPF012"
    for spelling, simple_program in programs.items():
        canonical = _canonical_callable(target_by_spelling[spelling])
        expanded = canonical(**_program_arguments(simple_program))

        assert expanded == simple_program
        assert tuple(field.name for field in fields(expanded)) == _FIVE_FIELDS
        assert not hasattr(expanded, "family_id")
        assert not hasattr(expanded, "catalog_spelling")

    reference = automata.eca(rule=90, width=5)
    assert automata.elementary_cellular_automaton(
        rule=90,
        width=5,
    ) == reference
    assert substitua.multiway_system(**_program_arguments(reference)) == (
        substitua.multiway_rewrite(**_program_arguments(reference))
    )
    assert substitua.network_rewrite(**_program_arguments(reference)) == (
        substitua.parallel_network_rewrite(**_program_arguments(reference))
    )
    assert ca.catalog.dynamica.pde(**_program_arguments(reference)) == (
        ca.catalog.dynamica.partial_differential_relation(
            **_program_arguments(reference)
        )
    )

    neighbor_arguments = {
        "initial": (0, 1, 0),
        "head": 1,
        "colors": 2,
        "transitions": _mobile_transitions(neighbor_updating=True),
    }
    with pytest.warns(DeprecationWarning):
        legacy = machina.extended_mobile_automaton(**neighbor_arguments)
    current = machina.neighbor_updating_mobile_automaton(
        **neighbor_arguments
    )
    assert legacy == current


def test_flat_qualified_and_metadata_only_names_obey_the_export_contract() -> None:
    """All C/P/A are flat, the sole K is qualified, and M is never callable."""

    canonical_names = {
        row[2].replace("-", "_")
        for row in CANONICAL_ROWS
    }
    legacy_names = {row[0] for row in LEGACY_CALLABLE_ROWS}
    expected_names = canonical_names | legacy_names | {"look_and_say"}
    expected_flat = expected_names - {"extended_mobile_automaton"}

    assert len(expected_names) == 105
    assert len(expected_flat) == 104
    assert {item.spelling for item in entries.NAME_ENTRIES} == expected_names
    assert Counter(item.kind for item in entries.NAME_ENTRIES) == (
        EXPECTED_NAME_KIND_COUNTS
    )
    assert {
        item.spelling
        for item in entries.NAME_ENTRIES
        if item.flat_export
    } == expected_flat
    assert {
        item.spelling
        for item in entries.NAME_ENTRIES
        if not item.flat_export
    } == {"extended_mobile_automaton"}

    assert set(ca.catalog.__all__) == (
        expected_flat | _RESERVED_CATALOG_EXPORTS
    )
    assert all(callable(getattr(ca.catalog, name)) for name in expected_flat)
    assert not hasattr(ca.catalog, "extended_mobile_automaton")
    assert (
        machina.extended_mobile_automaton
        is getattr(machina, "extended_mobile_automaton")
    )
    assert "extended_mobile_automaton" in machina.__all__

    assert expected_names.isdisjoint(ca.__all__)
    assert all(not hasattr(ca, name) for name in expected_names)
    for spelling in METADATA_ONLY_SPELLINGS:
        assert all(
            not hasattr(module, spelling)
            for module in (
                ca.catalog,
                automata,
                substitua,
                machina,
                media,
                criteria,
                ca.catalog.dynamica,
            )
        )


def test_t08_t40_t32_and_t44_keep_their_special_dispositions() -> None:
    """Zero/two targets and the two preset-not-alias decisions remain explicit."""

    legacy = {item.legacy_id: item for item in entries.LEGACY_ENTRIES}
    names = {item.spelling: item for item in entries.NAME_ENTRIES}

    assert legacy["T08"].disposition == "retire-role"
    assert legacy["T08"].candidate_ids == ()
    assert legacy["T08"].targets == ()
    assert not any("T08" in item.legacy_entry_ids for item in names.values())

    assert legacy["T40"].disposition == "split"
    assert tuple(target.branch_name for target in legacy["T40"].targets) == (
        "sequence",
        "register",
    )
    assert tuple(
        (
            target.target_family_id,
            target.callable_spelling,
            target.treatment,
        )
        for target in legacy["T40"].targets
    ) == (
        ("SPF002", "constant_digit_sequence", "P"),
        ("SPF008", "constant_digit_register", "P"),
    )
    assert {
        name
        for name, item in names.items()
        if item.legacy_entry_ids == ("T40",)
    } == {"constant_digit_sequence", "constant_digit_register"}

    for legacy_id, spelling in (
        ("T32", "template_constraint_system"),
        ("T44", "continuous_cellular_automaton"),
    ):
        assert legacy[legacy_id].disposition == "alias"
        assert legacy[legacy_id].targets[0].treatment == "P"
        assert names[spelling].kind == "P"
        assert names[spelling].delegate_import_name == (
            f"ca.catalog."
            f"{names[spelling].owner_module}."
            f"{_canonical_rows_by_id()[names[spelling].target_family_id][2].replace('-', '_')}"
        )
