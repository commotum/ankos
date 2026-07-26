"""CT01: the exact five-field program boundary."""

from dataclasses import fields

import pytest

import ca

from g7_fixtures import native_program


def test_simple_program_has_exactly_the_five_settled_fields() -> None:
    program, _, _ = native_program("dyadlags")

    expected = ("seed", "alphabet", "frontier", "neighborhood", "rule")
    assert tuple(field.name for field in fields(ca.SimpleProgram)) == expected
    assert tuple(program.__dict__) == expected
    assert len(program.__dict__) == 5


def test_program_rejects_semantic_sidecars_and_constructor_receipts() -> None:
    program, _, _ = native_program("dyadlags")

    values = dict(program.__dict__)
    for forbidden in (
        "domain",
        "policy",
        "scheduler",
        "rng",
        "observer",
        "catalog_id",
        "compatibility_certificate",
    ):
        with pytest.raises(TypeError):
            ca.SimpleProgram(**values, **{forbidden: object()})


@pytest.mark.parametrize(
    "case_id",
    (
        "ar2",
        "dyadlags",
        "lagcounts",
        "dyadrads",
        "dyadaxes-2d",
        "dyadaxes-3d",
    ),
)
def test_every_retained_native_construction_is_an_exact_simple_program(
    case_id: str,
) -> None:
    program, _, _ = native_program(case_id)

    assert type(program) is ca.SimpleProgram
