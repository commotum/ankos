"""Tests for the narrow G7-01 package façade."""

import importlib.util
import inspect
from pathlib import Path
import subprocess
import sys

import ca


def test_root_exports_only_the_settled_namespaces_and_three_conveniences() -> None:
    assert ca.__all__ == [
        "SimpleProgram",
        "apply",
        "rollout",
        "program",
        "loci",
        "alphabets",
        "seeds",
        "frontiers",
        "neighborhoods",
        "rules",
    ]
    assert set(vars(ca)) >= set(ca.__all__)


def test_component_constructors_are_module_qualified() -> None:
    assert callable(ca.alphabets.boolean)
    assert callable(ca.seeds.exact)
    assert callable(ca.frontiers.everywhere)
    assert callable(ca.neighborhoods.eca)
    assert callable(ca.rules.elementary)
    for broad_export in (
        "boolean",
        "exact",
        "everywhere",
        "eca",
        "elementary",
        "catalog",
        "serialization",
    ):
        assert broad_export not in ca.__all__
        assert not hasattr(ca, broad_export)


def test_apply_and_rollout_have_the_exact_public_signatures() -> None:
    assert str(inspect.signature(ca.apply)) == (
        "(program: 'SimpleProgram[C, V, W, R]', "
        "input: 'C | ApplicationInput[C]') -> 'ApplicationResult[C]'"
    )
    assert str(inspect.signature(ca.rollout)) == (
        "(program: 'SimpleProgram[C, V, W, R]', *, steps: 'int', "
        "initial: 'C | None' = None, replay_key: 'ReplayKey | None' = None) "
        "-> 'RolloutResult[C]'"
    )


def test_rollout_is_callable_and_has_no_shadowing_public_submodule() -> None:
    assert callable(ca.rollout)
    assert importlib.util.find_spec("ca.rollout") is None
    assert not (Path(ca.__file__).parent / "rollout.py").exists()


def test_obsolete_modules_exports_and_eager_auxiliaries_are_absent() -> None:
    script = """
import sys
import ca
assert "ca.specs" not in sys.modules
assert "ca.rollout" not in sys.modules
assert "ca.datasets" not in sys.modules
assert "ca.rng" not in sys.modules
assert "ca.viz" not in sys.modules
assert not hasattr(ca, "Dynamics")
assert not hasattr(ca, "RawEpisode")
assert not hasattr(ca, "rollout_batch")
"""
    completed = subprocess.run(
        [sys.executable, "-c", script],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
