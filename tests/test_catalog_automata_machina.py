from __future__ import annotations

import pytest

from ca import program
from ca.catalog import automata


def test_eca_binds_one_concrete_ordinary_program() -> None:
    constructed = automata.eca(rule=110, width=7)

    assert type(constructed) is program.SimpleProgram
    assert constructed.seed.configuration_contract.shape == (7,)
    assert constructed.alphabet.value_profile.value == "boolean"
    assert constructed.rule.descriptor.denotation.provenance == (
        "preset:elementary",
        "rule-110",
    )


def test_elementary_cellular_automaton_is_an_exact_alias() -> None:
    assert automata.elementary_cellular_automaton(rule=90, width=9) == (
        automata.eca(rule=90, width=9)
    )


@pytest.mark.parametrize("width", (0, -1))
def test_eca_rejects_nonpositive_width(width: int) -> None:
    with pytest.raises(ValueError, match="positive"):
        automata.eca(width=width)


def test_eca_rejects_boolean_width() -> None:
    with pytest.raises(TypeError, match="integer"):
        automata.eca(width=True)
