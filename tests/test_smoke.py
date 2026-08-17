"""Smoke checks for the one explicitly supported catalog example."""

from __future__ import annotations

import ca
from ca import program, serialization


def test_eca_rolls_out_and_round_trips() -> None:
    simple_program = ca.catalog.eca(rule=30, width=9)

    episode = ca.rollout(
        simple_program,
        steps=1,
        replay_key="eca-smoke",
    )
    encoded = serialization.dumps(simple_program)

    assert isinstance(episode, program.RolloutTruncated)
    assert serialization.loads(encoded) == serialization.Decoded(simple_program)


def test_elementary_cellular_automaton_is_the_eca_alias() -> None:
    assert ca.catalog.elementary_cellular_automaton(rule=90, width=7) == (
        ca.catalog.eca(rule=90, width=7)
    )
