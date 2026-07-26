"""Standalone smoke checks for an installed Goal 7 wheel.

Run this file with an isolated interpreter whose environment contains the
built wheel.  Its filename intentionally does not match pytest's collection
pattern: wheel construction and installation remain an explicit release gate.
"""

from __future__ import annotations

import importlib.metadata
import importlib.util
import inspect
import json
from pathlib import Path
import sys

import ca


EXPECTED_ROOT = [
    "SimpleProgram",
    "apply",
    "rollout",
    "program",
    "catalog",
    "loci",
    "alphabets",
    "seeds",
    "frontiers",
    "neighborhoods",
    "rules",
    "serialization",
]
OBSOLETE_PUBLIC_SUBMODULES = (
    "configuration",
    "regions",
    "replacement",
    "results",
    "engine",
    "rollout",
    "run",
    "updates",
    "specs",
)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    installed_root = Path(ca.__file__).resolve().parent

    assert importlib.metadata.version("ankos") == "0.2.0"
    assert not installed_root.is_relative_to(repo_root / "src")
    assert (installed_root / "py.typed").is_file()
    assert ca.__all__ == EXPECTED_ROOT
    assert str(inspect.signature(ca.apply)) == (
        "(program: 'SimpleProgram[C, V, W, R]', "
        "input: 'C | ApplicationInput[C]') -> 'ApplicationResult[C]'"
    )
    assert str(inspect.signature(ca.rollout)) == (
        "(program: 'SimpleProgram[C, V, W, R]', *, steps: 'int', "
        "initial: 'C | None' = None, replay_key: 'ReplayKey | None' = None) "
        "-> 'RolloutResult[C]'"
    )
    assert not {"ca.datasets", "ca.rng", "ca.viz"} & set(sys.modules)

    for submodule in OBSOLETE_PUBLIC_SUBMODULES:
        assert importlib.util.find_spec(f"ca.{submodule}") is None

    simple_program = ca.catalog.eca(rule=30, width=5)
    source = ca.loci.grid_configuration(
        (5,),
        (False, False, True, False, False),
        boundary=ca.loci.Boundary(ca.loci.BoundaryPolicy.FIXED, False),
    )
    applied = ca.apply(simple_program, source)
    assert isinstance(applied, ca.program.ApplicationComplete)
    traversed = ca.rollout(simple_program, steps=2, initial=source)
    assert isinstance(traversed, ca.program.RolloutTruncated)
    assert len(traversed.raw_trace.applications.atoms) == 2

    encoded = ca.serialization.dumps(simple_program)
    envelope = json.loads(encoded)
    assert set(envelope["payload"]) == {
        "seed",
        "alphabet",
        "frontier",
        "neighborhood",
        "rule",
    }
    decoded = ca.serialization.loads(encoded)
    assert decoded == ca.serialization.Decoded(simple_program)
    assert ca.serialization.dumps(decoded.value) == encoded
    assert ca.apply(decoded.value, source) == applied

    print("installed-wheel-smoke: ok")


if __name__ == "__main__":
    main()
