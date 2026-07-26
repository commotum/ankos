"""CT02: descriptor closure and five-way compatibility."""

from dataclasses import replace
from fractions import Fraction

import pytest

import ca
from ca import alphabets, frontiers, loci, neighborhoods, rules, seeds

from g7_fixtures import native_program


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


def test_program_construction_proves_all_cross_field_compatibility_clauses() -> None:
    program, _, _ = native_program("dyadlags")

    assert program.seed.configuration_contract == program.rule.contract.configuration_contract
    assert program.alphabet.value_profile is program.seed.value_profile
    assert program.frontier.effect_profile == program.rule.contract.required_effect_profile
    assert program.neighborhood.result_shape == program.rule.contract.required_read_shape
    assert program.neighborhood.join_shape == program.rule.contract.required_join_shape
    assert program.seed.exactness_profile is program.rule.contract.exactness_profile


def test_each_cross_field_clause_has_an_independent_negative_case() -> None:
    program, _, _ = native_program("dyadlags")

    wrong_profile_frontier = replace(
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
            wrong_profile_frontier,
            program.neighborhood,
            program.rule,
        )

    wrong_carrier = replace(
        program.neighborhood,
        configuration_contract=loci.CarrierContract(
            loci.CarrierKind.GRID,
            rank=1,
            axes=("x",),
        ),
    )
    with pytest.raises(ca.program.ProgramCompatibilityError, match="ReadableRegion"):
        ca.SimpleProgram(
            program.seed,
            program.alphabet,
            program.frontier,
            wrong_carrier,
            program.rule,
        )

    wrong_shape = replace(
        program.neighborhood,
        result_shape=neighborhoods.ResultShape(
            (neighborhoods.ReadField("wrong", neighborhoods.ReadArity.ONE),)
        ),
    )
    with pytest.raises(ca.program.ProgramCompatibilityError, match="read shape"):
        ca.SimpleProgram(
            program.seed,
            program.alphabet,
            program.frontier,
            wrong_shape,
            program.rule,
        )

    wrong_effect = replace(
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
            wrong_effect,
        )

    wrong_exactness = replace(
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
            wrong_exactness,
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
