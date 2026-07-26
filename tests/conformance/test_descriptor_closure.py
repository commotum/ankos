"""CT02: descriptor closure and five-way compatibility."""

from dataclasses import replace
from fractions import Fraction

import pytest

import ca
from ca import alphabets, frontiers, loci, neighborhoods, rules, seeds

from g7_fixtures import native_program
from helpers import assert_closed_descriptor


def _walk(value: object) -> None:
    """Recursively reject executable or mutable recipe payloads."""

    assert not callable(value)
    assert not isinstance(value, (dict, list, set, bytearray))
    fields = getattr(value, "__dataclass_fields__", None)
    if fields is not None:
        for name in fields:
            _walk(getattr(value, name))
    elif isinstance(value, tuple):
        for item in value:
            _walk(item)


def test_every_descriptor_is_recursively_closed_versioned_and_exact() -> None:
    program, _, _ = native_program("dyadaxes-2d")
    values = (
        program.seed,
        program.alphabet,
        program.frontier,
        program.neighborhood,
        program.rule,
        loci.path("root", 3, Fraction(1, 2)),
        alphabets.represented_numeric(
            alphabets.RepresentedNumberProfile.IEEE754_BINARY64
        ),
    )

    for value in values:
        _walk(value)
        assert_closed_descriptor(value)


def test_top_level_components_have_one_exact_supported_version() -> None:
    program, _, _ = native_program("dyadlags")

    assert (
        program.seed.version,
        program.frontier.version,
        program.neighborhood.version,
    ) == (1, 1, 1)
    with pytest.raises(seeds.SeedValidationError, match="version"):
        replace(program.seed, version=2)
    with pytest.raises(frontiers.WritableResolutionError, match="version"):
        replace(program.frontier, version=True)
    with pytest.raises(neighborhoods.ReadableResolutionError, match="version"):
        replace(program.neighborhood, version="1")  # type: ignore[arg-type]


def test_program_construction_proves_all_cross_field_compatibility_clauses() -> None:
    program, _, _ = native_program("dyadlags")

    assert program.seed.configuration_contract == program.rule.contract.configuration_contract
    assert program.alphabet.value_profile is program.seed.value_profile
    assert set(program.rule.contract.required_effect_profile.existing).issubset(
        program.frontier.effect_profile.existing
    )
    assert set(program.rule.contract.required_effect_profile.fresh).issubset(
        program.frontier.effect_profile.fresh
    )
    assert program.neighborhood.result_shape == program.rule.contract.required_read_shape
    assert program.neighborhood.join_shape == program.rule.contract.required_join_shape
    assert program.seed.exactness_profile is program.rule.contract.exactness_profile


def test_frontier_may_grant_a_strict_superset_of_rule_effects() -> None:
    program, _, _ = native_program("dyadlags")
    broader_frontier = replace(
        program.frontier,
        effect_profile=frontiers.EffectProfile(
            existing=(frontiers.Effect.REPLACE, frontiers.Effect.DELETE),
        ),
    )

    broader = ca.SimpleProgram(
        program.seed,
        program.alphabet,
        broader_frontier,
        program.neighborhood,
        program.rule,
    )

    assert broader.rule.contract.required_effect_profile.existing == (
        frontiers.Effect.REPLACE,
    )
    assert broader.frontier.effect_profile.existing == (
        frontiers.Effect.REPLACE,
        frontiers.Effect.DELETE,
    )


def test_rule_carrier_must_accept_seed_output() -> None:
    program, _, _ = native_program("dyadlags")
    wrong_carrier = loci.CarrierContract(
        loci.CarrierKind.RECORD,
        rank=0,
        shape=(),
    )
    wrong_rule = replace(
        program.rule,
        contract=replace(
            program.rule.contract,
            configuration_contract=wrong_carrier,
        ),
    )

    with pytest.raises(
        ca.program.ProgramCompatibilityError,
        match="Rule configuration contract",
    ):
        ca.SimpleProgram(
            program.seed,
            program.alphabet,
            program.frontier,
            program.neighborhood,
            wrong_rule,
        )


def test_frontier_carrier_must_accept_seed_output() -> None:
    program, _, _ = native_program("dyadlags")
    wrong_frontier = replace(
        program.frontier,
        configuration_contract=loci.CarrierContract(
            loci.CarrierKind.RECORD,
            rank=0,
            shape=(),
        ),
    )

    with pytest.raises(
        ca.program.ProgramCompatibilityError,
        match="WritableRegion configuration contract",
    ):
        ca.SimpleProgram(
            program.seed,
            program.alphabet,
            wrong_frontier,
            program.neighborhood,
            program.rule,
        )


def test_neighborhood_carrier_must_accept_seed_output() -> None:
    program, _, _ = native_program("dyadlags")
    wrong_neighborhood = replace(
        program.neighborhood,
        configuration_contract=loci.CarrierContract(
            loci.CarrierKind.RECORD,
            rank=0,
            shape=(),
        ),
    )

    with pytest.raises(
        ca.program.ProgramCompatibilityError,
        match="ReadableRegion configuration contract",
    ):
        ca.SimpleProgram(
            program.seed,
            program.alphabet,
            program.frontier,
            wrong_neighborhood,
            program.rule,
        )


def test_seed_values_must_conform_to_same_profile_alphabet() -> None:
    program, _, _ = native_program("ar2")
    excluding_alphabet = alphabets.modular(2)

    assert excluding_alphabet.value_profile is program.alphabet.value_profile
    with pytest.raises(
        ca.program.ProgramCompatibilityError,
        match="Seed value does not conform to Alphabet",
    ):
        ca.SimpleProgram(
            program.seed,
            excluding_alphabet,
            program.frontier,
            program.neighborhood,
            program.rule,
        )


def test_component_value_profiles_must_agree() -> None:
    program, _, _ = native_program("dyadlags")
    wrong_frontier = replace(
        program.frontier,
        value_profile=alphabets.ValueProfile.INTEGER,
        target_contract=replace(
            program.frontier.target_contract,
            value_profile=alphabets.ValueProfile.INTEGER,
        ),
    )

    with pytest.raises(ca.program.ProgramCompatibilityError, match="profiles"):
        ca.SimpleProgram(
            program.seed,
            program.alphabet,
            wrong_frontier,
            program.neighborhood,
            program.rule,
        )


def test_rule_read_shape_must_match_neighborhood() -> None:
    program, _, _ = native_program("dyadlags")
    wrong_neighborhood = replace(
        program.neighborhood,
        result_shape=neighborhoods.ResultShape(
            (
                neighborhoods.ReadField(
                    "wrong",
                    neighborhoods.ReadArity.ONE,
                    1,
                ),
                *program.neighborhood.result_shape.fields[1:],
            )
        ),
    )

    with pytest.raises(ca.program.ProgramCompatibilityError, match="read shape"):
        ca.SimpleProgram(
            program.seed,
            program.alphabet,
            program.frontier,
            wrong_neighborhood,
            program.rule,
        )


def test_rule_join_shape_must_match_neighborhood() -> None:
    program, _, _ = native_program("dyadlags")
    wrong_rule = replace(
        program.rule,
        contract=replace(
            program.rule.contract,
            required_join_shape=neighborhoods.JoinShape(
                neighborhoods.JoinMode.GLOBAL,
                ("wrong",),
            ),
        ),
    )

    with pytest.raises(ca.program.ProgramCompatibilityError, match="join shape"):
        ca.SimpleProgram(
            program.seed,
            program.alphabet,
            program.frontier,
            program.neighborhood,
            wrong_rule,
        )


def test_rule_effects_must_fit_frontier_capabilities() -> None:
    program, _, _ = native_program("dyadlags")
    wrong_rule = replace(
        program.rule,
        contract=replace(
            program.rule.contract,
            required_effect_profile=frontiers.EffectProfile(
                existing=(frontiers.Effect.DELETE,)
            ),
        ),
    )
    with pytest.raises(ca.program.ProgramCompatibilityError, match="effects"):
        ca.SimpleProgram(
            program.seed,
            program.alphabet,
            program.frontier,
            program.neighborhood,
            wrong_rule,
        )


def test_component_exactness_and_representation_profiles_must_agree() -> None:
    program, _, _ = native_program("dyadlags")
    represented_rule = replace(
        program.rule,
        contract=replace(
            program.rule.contract,
            exactness_profile=seeds.ExactnessProfile.REPRESENTED,
        ),
    )
    with pytest.raises(ca.program.ProgramCompatibilityError, match="exactness"):
        ca.SimpleProgram(
            program.seed,
            program.alphabet,
            program.frontier,
            program.neighborhood,
            represented_rule,
        )


def test_descriptors_reject_callbacks_opaque_escape_and_ambient_entropy() -> None:
    with pytest.raises(TypeError):
        loci.SelectorExpr(
            loci.SelectorPrimitive.LITERAL,
            arguments=(lambda: None,),  # type: ignore[arg-type]
        )
    with pytest.raises(TypeError):
        rules.RuleExpr(
            rules.ExpressionPrimitive.LITERAL,
            arguments=(lambda: None,),  # type: ignore[arg-type]
        )
    with pytest.raises((TypeError, ValueError)):
        seeds.Construction(
            seeds.ConstructionOp.SEQUENCE,
            arguments=({"mutable": True},),  # type: ignore[arg-type]
        )
    with pytest.raises(TypeError):
        seeds.bernoulli(
            loci.literal((loci.named("x"),)),
            0.5,  # type: ignore[arg-type]
            configuration_contract=loci.CarrierContract(
                loci.CarrierKind.RECORD,
                rank=0,
                shape=(),
            ),
        )
    with pytest.raises(TypeError):
        frontiers.EffectProfile(
            existing=("opaque",),  # type: ignore[arg-type]
        )
    with pytest.raises(TypeError):
        frontiers.TargetContract(
            "opaque",  # type: ignore[arg-type]
            alphabets.ValueProfile.BOOLEAN,
        )
    with pytest.raises(TypeError):
        neighborhoods.JoinShape(
            "opaque",  # type: ignore[arg-type]
            (),
        )
    with pytest.raises(TypeError):
        neighborhoods.ResultShape(
            ("opaque",),  # type: ignore[arg-type]
        )

    program, _, _ = native_program("dyadlags")
    with pytest.raises(TypeError):
        seeds.OverlaySource(
            (program.seed,),
            "opaque",  # type: ignore[arg-type]
        )
    with pytest.raises(TypeError):
        seeds.SeedOutputContract(
            program.seed.configuration_contract,
            program.seed.value_profile,
            "opaque",  # type: ignore[arg-type]
        )
