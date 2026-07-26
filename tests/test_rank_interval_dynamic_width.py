"""Focused hostile coverage for the bounded Goal 7 generic gaps."""

from fractions import Fraction

import pytest

import ca
from ca import (
    alphabets,
    frontiers,
    loci,
    neighborhoods,
    program,
    rules,
    seeds,
    serialization,
)


def _evaluate(expression: rules.RuleExpr):
    source = loci.record_configuration((("fixture", 0),))
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.INTEGER,
    ).resolve(source)
    return rules._evaluate_proven(  # noqa: SLF001 - interpreter unit test
        expression,
        readable,
        anchor=None,
    )


def _rank_four_program(seed: seeds.Seed) -> ca.SimpleProgram:
    contract = seed.configuration_contract
    alphabet = alphabets.boolean()
    writable = frontiers.everywhere(
        configuration_contract=contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.grid_relative(
        ((0, 0, 0, 0),),
        configuration_contract=contract,
        value_profile=alphabet.value_profile,
    )
    rule = rules.expression(
        rules.ExistingPlan(
            rules.ExistingPlanKind.BY_TARGET,
            (rules.project(rules.group(0), 0),),
        ),
        contract=rules.RuleContract(
            contract,
            alphabet.value_profile,
            readable.result_shape,
            readable.join_shape,
            writable.effect_profile,
        ),
        witness=rules.literal_expr("rank-four-identity"),
        provenance=("test:rank-four-seed",),
    )
    return ca.SimpleProgram(seed, alphabet, writable, readable, rule)


def test_finite_grid_is_rank_generic_and_preserves_explicit_axes() -> None:
    axes = ("row", "column", "layer", "phase")
    seed = seeds.finite_grid(
        (1, 1, 1, 2),
        (False, True),
        boundary=loci.Boundary(loci.BoundaryPolicy.FIXED, False),
        axes=axes,
    )
    configuration = seed.denote().exact_configuration

    assert configuration is not None
    assert configuration.contract.rank == 4
    assert configuration.contract.shape == (1, 1, 1, 2)
    assert configuration.contract.axes == axes
    assert all(
        target.path[0] == axes
        for target, _ in configuration.entries
    )


def test_rank_four_grid_fill_and_uniform_seeds_realize_end_to_end() -> None:
    shape = (1, 1, 1, 1)
    contract = loci.CarrierContract(
        loci.CarrierKind.GRID,
        rank=4,
        shape=shape,
    )
    candidates = (
        seeds.constructive(
            seeds.Construction(
                seeds.ConstructionOp.GRID,
                (
                    shape,
                    (True,),
                    (("policy", "fixed"), ("exterior", False)),
                ),
            ),
            configuration_contract=contract,
            value_profile=alphabets.ValueProfile.BOOLEAN,
        ),
        seeds.constructive(
            seeds.Construction(seeds.ConstructionOp.FILL, (True,)),
            configuration_contract=contract,
            value_profile=alphabets.ValueProfile.BOOLEAN,
        ),
        seeds.law(
            seeds.UniformTupleLaw(1, 2),
            configuration_contract=contract,
            value_profile=alphabets.ValueProfile.BOOLEAN,
            construction=seeds.Construction(seeds.ConstructionOp.GRID),
        ),
    )

    for candidate in candidates:
        result = ca.rollout(_rank_four_program(candidate), steps=0)
        assert isinstance(result, program.RolloutTruncated)
        roots = result.raw_trace.roots.support.atoms
        assert roots
        assert all(
            root.contract.axes == ("x", "y", "z", "axis4")
            for root in roots
        )


@pytest.mark.parametrize(
    ("shape", "values", "axes", "error"),
    (
        ((), (), None, seeds.SeedValidationError),
        ((1, 1, 1, 1), (False,), ("x", "y", "z"), seeds.SeedValidationError),
        ((1, 1, 1, 1), (False,), ("x", "y", "z", "z"), seeds.SeedValidationError),
        ((1, 1, 1, 1), (False,), ("x", "y", "z", 4), TypeError),
    ),
)
def test_finite_grid_rejects_malformed_generic_rank_declarations(
    shape,
    values,
    axes,
    error,
) -> None:
    with pytest.raises(error):
        seeds.finite_grid(
            shape,
            values,
            boundary=loci.Boundary(loci.BoundaryPolicy.FIXED, False),
            axes=axes,
        )


def test_exact_rational_intervals_respect_endpoint_topology() -> None:
    closed = alphabets.rational_interval(Fraction(0), Fraction(1))
    open_interval = alphabets.rational_interval(
        Fraction(0),
        Fraction(1),
        lower_closed=False,
        upper_closed=False,
    )
    singleton = alphabets.rational_interval(Fraction(1, 3), Fraction(1, 3))

    assert closed.value_profile is alphabets.ValueProfile.RATIONAL
    assert closed.contains(0)
    assert closed.contains(Fraction(1, 2))
    assert closed.contains(1)
    assert not closed.contains(False)
    assert not closed.contains(Fraction(-1, 10))
    assert not closed.contains(Fraction(11, 10))
    assert not open_interval.contains(0)
    assert open_interval.contains(Fraction(1, 2))
    assert not open_interval.contains(1)
    assert singleton.contains(Fraction(1, 3))
    assert not singleton.contains(Fraction(333, 1000))
    assert closed.descriptor.scalars == (
        ("lower", Fraction(0)),
        ("upper", Fraction(1)),
        ("lower_closed", True),
        ("upper_closed", True),
    )


@pytest.mark.parametrize(
    ("arguments", "keywords", "error"),
    (
        ((0, Fraction(1)), {}, TypeError),
        ((Fraction(0), 1), {}, TypeError),
        ((Fraction(1), Fraction(0)), {}, ValueError),
        (
            (Fraction(0), Fraction(0)),
            {"lower_closed": False},
            ValueError,
        ),
        (
            (Fraction(0), Fraction(1)),
            {"upper_closed": 1},
            TypeError,
        ),
        (
            (lambda: Fraction(0), Fraction(1)),
            {},
            TypeError,
        ),
    ),
)
def test_rational_interval_rejects_inexact_opaque_or_empty_bounds(
    arguments,
    keywords,
    error,
) -> None:
    with pytest.raises(error):
        alphabets.rational_interval(*arguments, **keywords)


def test_rational_interval_descriptor_and_codec_fail_closed() -> None:
    interval = alphabets.rational_interval(
        Fraction(-2, 3),
        Fraction(5, 7),
        upper_closed=False,
    )
    encoded = serialization.dumps(interval)

    assert serialization.loads(encoded) == serialization.Decoded(interval)
    assert serialization.dumps(interval.descriptor.kind)
    with pytest.raises(TypeError, match="exact Fractions"):
        alphabets.AlphabetDescriptor(
            alphabets.AlphabetKind.RATIONAL_INTERVAL,
            scalars=(
                ("lower", 0),
                ("upper", Fraction(1)),
                ("lower_closed", True),
                ("upper_closed", True),
            ),
        )
    with pytest.raises(ValueError, match="descriptor shape"):
        alphabets.AlphabetDescriptor(
            alphabets.AlphabetKind.RATIONAL_INTERVAL,
            scalars=(
                ("upper", Fraction(1)),
                ("lower", Fraction(0)),
                ("lower_closed", True),
                ("upper_closed", True),
            ),
        )


def test_integer_digits_accepts_a_dynamic_positive_width() -> None:
    state = alphabets.record_value(
        (
            ("value", 2),
            ("width", 4),
        ),
        tag="digit-state",
    )
    state_expression = rules.literal_expr(state)
    expression = rules.integer_digits(
        rules.record_field(state_expression, "value"),
        2,
        width=rules.record_field(state_expression, "width"),
    )
    value, proof = _evaluate(expression)

    assert value == alphabets.word_value((0, 0, 1, 0), tag="digits")
    assert proof.steps[-1].result == value
    assert serialization.loads(serialization.dumps(expression)) == (
        serialization.Decoded(expression)
    )


@pytest.mark.parametrize(
    ("width", "error"),
    (
        (rules.literal_expr(0), ValueError),
        (rules.literal_expr(-1), ValueError),
        (rules.literal_expr(True), TypeError),
        (rules.literal_expr(Fraction(3, 2)), TypeError),
        (rules.add(rules.literal_expr(1), rules.literal_expr(2)), OverflowError),
    ),
)
def test_integer_digits_dynamic_width_fails_closed(
    width: rules.RuleExpr,
    error: type[Exception],
) -> None:
    expression = rules.integer_digits(
        rules.literal_expr(8),
        2,
        width=width,
    )
    with pytest.raises(error):
        _evaluate(expression)


def test_integer_digits_rejects_an_opaque_width_at_construction() -> None:
    with pytest.raises(ValueError, match="RuleExpr"):
        rules.integer_digits(
            rules.literal_expr(1),
            2,
            width="4",  # type: ignore[arg-type]
        )
