"""Focused contracts for the Media and Criteria catalog presets."""

from __future__ import annotations

import inspect

import pytest

import ca
from ca import alphabets, loci, program, rules, serialization
from ca.catalog import criteria, media


PRESET_SIGNATURES = (
    (
        media.constant_digit_register,
        ("register", "register_law", "digit_projection", "base"),
    ),
    (media.look_and_say, ("digits",)),
    (
        criteria.local_constraint_system,
        ("partial_assignment", "predicates", "relation", "cardinality"),
    ),
    (
        criteria.template_constraint_system,
        (
            "partial_assignment",
            "allowed_templates",
            "relation",
            "cardinality",
        ),
    ),
    (
        criteria.seeded_template_constraint_system,
        (
            "partial_assignment",
            "allowed_templates",
            "required_occurrences",
            "relation",
            "cardinality",
        ),
    ),
)


def _exact_source(
    simple_program: ca.SimpleProgram,
) -> loci.FiniteConfiguration[alphabets.SemanticValue]:
    source = simple_program.seed.denote().exact_configuration
    assert type(source) is loci.FiniteConfiguration
    return source


def _single_successor(
    result: program.ApplicationResult[
        loci.FiniteConfiguration[alphabets.SemanticValue]
    ],
) -> loci.FiniteConfiguration[alphabets.SemanticValue]:
    assert type(result) is program.ApplicationComplete
    groups = result.successor_quotient_with_derivation_fibers.atoms
    assert len(groups) == 1
    return groups[0].successor


def _single_state(
    configuration: loci.FiniteConfiguration[alphabets.SemanticValue],
) -> alphabets.SemanticValue:
    assert len(configuration.entries) == 1
    return configuration.entries[0][1]


def _register_program() -> ca.SimpleProgram:
    next_register = rules.add(
        rules.record_field(rules.observation(0), "register"),
        rules.literal_expr(1),
    )
    return media.constant_digit_register(
        register=9,
        register_law=next_register,
        digit_projection=rules.modulo(next_register, 10),
        base=10,
    )


def _constraint_inputs() -> tuple[
    alphabets.ValueNode,
    alphabets.ValueNode,
    alphabets.ValueNode,
    alphabets.ValueNode,
    rules.RuleExpr,
    rules.Cardinality,
]:
    partial_assignment = alphabets.map_value(
        (
            alphabets.map_entry_value("left", 0),
            alphabets.map_entry_value("right", 1),
        ),
        tag="partial-assignment",
    )
    predicates = alphabets.word_value(
        (
            alphabets.symbolic_value(
                "not-equal",
                items=("left", "right"),
            ),
        ),
        tag="local-predicates",
    )
    template = alphabets.word_value((0, 1), tag="template")
    allowed_templates = alphabets.word_value(
        (template,),
        tag="allowed-templates",
    )
    required_occurrence = alphabets.record_value(
        (
            ("position", 0),
            ("template", template),
        ),
        tag="required-occurrence",
    )
    relation = rules.literal_expr("candidate satisfies declared constraints")
    cardinality = rules.Undetermined(
        rules.literal_expr("solution count is not enumerated"),
        rules.Certificate(
            rules.CertificateKind.CARDINALITY,
            rules.literal_expr("external solution-count obligation"),
        ),
    )
    return (
        partial_assignment,
        predicates,
        allowed_templates,
        required_occurrence,
        relation,
        cardinality,
    )


def _criterion_programs() -> dict[str, ca.SimpleProgram]:
    (
        partial_assignment,
        predicates,
        allowed_templates,
        required_occurrence,
        relation,
        cardinality,
    ) = _constraint_inputs()
    return {
        "local": criteria.local_constraint_system(
            partial_assignment=partial_assignment,
            predicates=predicates,
            relation=relation,
            cardinality=cardinality,
        ),
        "template": criteria.template_constraint_system(
            partial_assignment=partial_assignment,
            allowed_templates=allowed_templates,
            relation=relation,
            cardinality=cardinality,
        ),
        "seeded-template": criteria.seeded_template_constraint_system(
            partial_assignment=partial_assignment,
            allowed_templates=allowed_templates,
            required_occurrences=(required_occurrence,),
            relation=relation,
            cardinality=cardinality,
        ),
    }


def _all_preset_programs() -> dict[str, ca.SimpleProgram]:
    return {
        "constant-digit-register": _register_program(),
        "look-and-say": media.look_and_say(digits=(1, 1, 2)),
        **_criterion_programs(),
    }


@pytest.mark.parametrize(
    ("constructor", "parameter_names"),
    PRESET_SIGNATURES,
)
def test_preset_signatures_are_explicit_keyword_only_and_nonvariadic(
    constructor,
    parameter_names: tuple[str, ...],
) -> None:
    parameters = tuple(inspect.signature(constructor).parameters.values())

    assert tuple(parameter.name for parameter in parameters) == parameter_names
    assert all(
        parameter.kind is inspect.Parameter.KEYWORD_ONLY
        for parameter in parameters
    )
    assert all(
        parameter.kind
        not in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        )
        for parameter in parameters
    )


def test_constant_digit_register_commits_one_atomic_record_update() -> None:
    simple_program = _register_program()
    source = _exact_source(simple_program)
    source_identity = loci.configuration_identity(source)

    initial_state = _single_state(source)
    assert alphabets.record_get(initial_state, "register") == 9
    assert alphabets.record_get(initial_state, "digit") == 9

    result = ca.apply(simple_program, source)
    successor = _single_successor(result)
    successor_state = _single_state(successor)

    assert alphabets.record_get(successor_state, "register") == 10
    assert alphabets.record_get(successor_state, "digit") == 0
    assert type(result) is program.ApplicationComplete
    (atom,) = result.source_outcomes.support.atoms
    assert type(atom) is rules.Derivation
    assert len(atom.replacement.existing) == 1
    assert (
        atom.replacement.existing[0].action
        is rules.DispositionAction.REPLACE
    )
    assert atom.replacement.existing[0].target == source.entries[0][0]

    assert loci.configuration_identity(source) == source_identity
    assert _single_state(source) == initial_state


def test_look_and_say_executes_the_representative_step_and_rollout() -> None:
    simple_program = media.look_and_say(digits=(1, 1, 2))
    source = _exact_source(simple_program)
    expected_state = alphabets.word_value((2, 1, 1, 2), tag="digits")

    successor = _single_successor(ca.apply(simple_program, source))

    assert _single_state(successor) == expected_state
    assert _single_state(source) == alphabets.word_value(
        (1, 1, 2),
        tag="digits",
    )

    rolled = ca.rollout(simple_program, steps=1)

    assert type(rolled) is program.RolloutTruncated
    assert rolled.cause is program.TruncationCause.DEPTH_BOUND
    assert len(rolled.raw_trace.applications.atoms) == 1
    assert len(rolled.continuing_leaves.atoms) == 1
    assert (
        _single_state(rolled.continuing_leaves.atoms[0].configuration)
        == expected_state
    )


def test_constraint_presets_retain_three_distinct_source_presentations() -> None:
    (
        partial_assignment,
        predicates,
        allowed_templates,
        required_occurrence,
        relation,
        cardinality,
    ) = _constraint_inputs()
    simple_programs = _criterion_programs()
    states = {
        name: _single_state(_exact_source(simple_program))
        for name, simple_program in simple_programs.items()
    }

    local_state = states["local"]
    template_state = states["template"]
    seeded_state = states["seeded-template"]

    assert local_state.tag == "local-constraint-system"
    assert alphabets.record_get(
        local_state,
        "partial_assignment",
    ) == partial_assignment
    assert alphabets.record_get(local_state, "predicates") == predicates

    assert template_state.tag == "template-constraint-system"
    assert alphabets.record_get(
        template_state,
        "partial_assignment",
    ) == partial_assignment
    assert alphabets.record_get(
        template_state,
        "allowed_templates",
    ) == allowed_templates

    assert seeded_state.tag == "seeded-template-constraint-system"
    assert alphabets.record_get(
        seeded_state,
        "partial_assignment",
    ) == partial_assignment
    assert alphabets.record_get(
        seeded_state,
        "allowed_templates",
    ) == allowed_templates
    occurrences = alphabets.record_get(
        seeded_state,
        "required_occurrences",
    )
    assert type(occurrences) is alphabets.ValueNode
    assert occurrences.tag == "required-occurrences"
    assert alphabets.word_items(occurrences) == (required_occurrence,)

    assert len(
        {loci.canonical_identity(state) for state in states.values()}
    ) == 3
    for simple_program in simple_programs.values():
        denotation = simple_program.rule.descriptor.denotation
        assert type(denotation) is rules.IntensionalDenotation
        assert denotation.relation == relation
        assert denotation.cardinality == cardinality


@pytest.mark.parametrize(
    "name",
    ("local", "template", "seeded-template"),
)
def test_constraint_presets_apply_as_closed_intensional_relations(
    name: str,
) -> None:
    simple_program = _criterion_programs()[name]
    source = _exact_source(simple_program)

    applied = ca.apply(simple_program, source)

    assert type(applied) is program.ApplicationComplete
    assert (
        applied.source_outcomes.support.presentation
        is rules.SupportPresentation.INTENSIONAL
    )
    assert (
        applied.applied_atoms.presentation
        is rules.SupportPresentation.INTENSIONAL
    )
    assert (
        applied.successor_quotient_with_derivation_fibers.presentation
        is rules.SupportPresentation.INTENSIONAL
    )
    assert type(applied.outcome_atom_cardinality) is rules.Undetermined
    assert type(applied.derivation_cardinality) is rules.Undetermined
    assert type(applied.successor_cardinality) is rules.Undetermined

    rolled = ca.rollout(simple_program, steps=1)

    assert type(rolled) is program.RolloutTruncated
    assert rolled.cause is program.TruncationCause.INTENSIONAL_SUPPORT
    assert len(rolled.raw_trace.applications.atoms) == 1


@pytest.mark.parametrize(
    "name",
    (
        "constant-digit-register",
        "look-and-say",
        "local",
        "template",
        "seeded-template",
    ),
)
def test_preset_programs_round_trip_and_reencode_canonically(
    name: str,
) -> None:
    simple_program = _all_preset_programs()[name]
    encoded = serialization.dumps(simple_program)

    decoded = serialization.loads(encoded)

    assert type(decoded) is serialization.Decoded
    assert type(decoded.value) is ca.SimpleProgram
    assert decoded.value == simple_program
    assert serialization.dumps(decoded.value) == encoded


def test_media_presets_reject_hostile_inputs() -> None:
    valid_law = rules.literal_expr(0)

    with pytest.raises(ValueError):
        media.constant_digit_register(
            register=-1,
            register_law=valid_law,
            digit_projection=valid_law,
        )
    with pytest.raises(ValueError):
        media.constant_digit_register(
            register=0,
            register_law=valid_law,
            digit_projection=valid_law,
            base=1,
        )
    with pytest.raises(TypeError):
        media.constant_digit_register(
            register=0,
            register_law=0,  # type: ignore[arg-type]
            digit_projection=valid_law,
        )
    with pytest.raises(TypeError):
        media.constant_digit_register(
            register=0,
            register_law=valid_law,
            digit_projection=0,  # type: ignore[arg-type]
        )

    for digits in ((), (1, -1), (1, True), [1, 1, 2]):
        with pytest.raises(ValueError):
            media.look_and_say(digits=digits)  # type: ignore[arg-type]


def test_constraint_presets_reject_hostile_inputs_and_empty_occurrences() -> None:
    (
        partial_assignment,
        predicates,
        allowed_templates,
        required_occurrence,
        relation,
        cardinality,
    ) = _constraint_inputs()

    with pytest.raises(TypeError):
        criteria.local_constraint_system(
            partial_assignment="partial",  # type: ignore[arg-type]
            predicates=predicates,
            relation=relation,
            cardinality=cardinality,
        )
    with pytest.raises(TypeError):
        criteria.local_constraint_system(
            partial_assignment=partial_assignment,
            predicates="predicates",  # type: ignore[arg-type]
            relation=relation,
            cardinality=cardinality,
        )
    with pytest.raises(TypeError):
        criteria.template_constraint_system(
            partial_assignment=partial_assignment,
            allowed_templates=allowed_templates,
            relation="relation",  # type: ignore[arg-type]
            cardinality=cardinality,
        )
    with pytest.raises(TypeError):
        criteria.template_constraint_system(
            partial_assignment=partial_assignment,
            allowed_templates=allowed_templates,
            relation=relation,
            cardinality=object(),  # type: ignore[arg-type]
        )
    with pytest.raises(ValueError, match="nonempty"):
        criteria.seeded_template_constraint_system(
            partial_assignment=partial_assignment,
            allowed_templates=allowed_templates,
            required_occurrences=(),
            relation=relation,
            cardinality=cardinality,
        )
    with pytest.raises(ValueError):
        criteria.seeded_template_constraint_system(
            partial_assignment=partial_assignment,
            allowed_templates=allowed_templates,
            required_occurrences=[required_occurrence],  # type: ignore[arg-type]
            relation=relation,
            cardinality=cardinality,
        )
    with pytest.raises(ValueError):
        criteria.seeded_template_constraint_system(
            partial_assignment=partial_assignment,
            allowed_templates=allowed_templates,
            required_occurrences=("occurrence",),  # type: ignore[arg-type]
            relation=relation,
            cardinality=cardinality,
        )
