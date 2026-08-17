"""Small end-to-end checks for the retained native program fixtures."""

from __future__ import annotations

import pytest

import ca
from ca import program

from g7_fixtures import native_program, successor_values


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
def test_native_program_applies_to_its_expected_successors(case_id: str) -> None:
    simple_program, source, expected = native_program(case_id)

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationComplete)
    assert successor_values(result) == expected
