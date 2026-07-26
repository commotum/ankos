"""CT13: import ownership and absence of semantic dispatch."""

from __future__ import annotations

import ast
import importlib.util
import inspect
from pathlib import Path
import subprocess
import sys

import ca
from ca import program

from g7_fixtures import diamond_program, native_program


CORE_DEPENDENCIES = {
    "loci": set(),
    "alphabets": set(),
    "seeds": {"alphabets", "loci"},
    "frontiers": {"alphabets", "loci", "seeds"},
    "neighborhoods": {"alphabets", "loci", "seeds"},
    "rules": {"alphabets", "frontiers", "loci", "neighborhoods", "seeds"},
    "program": {
        "alphabets",
        "frontiers",
        "loci",
        "neighborhoods",
        "rules",
        "seeds",
    },
}


def _local_imports(module_name: str) -> set[str]:
    module = getattr(ca, module_name)
    path = Path(inspect.getsourcefile(module))
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom) or node.level != 1:
            continue
        if node.module:
            imports.add(node.module.split(".")[0])
        else:
            imports.update(alias.name.split(".")[0] for alias in node.names)
    return imports


def test_static_import_graph_matches_the_one_way_semantic_dag() -> None:
    for module_name, allowed in CORE_DEPENDENCIES.items():
        assert _local_imports(module_name) <= allowed


def test_apply_works_while_catalog_imports_are_blocked() -> None:
    script = """
import importlib.abc
import sys

class BlockCatalog(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "ca.catalog" or fullname.startswith("ca.catalog."):
            raise ImportError("catalog blocked")
        return None

sys.meta_path.insert(0, BlockCatalog())
import ca
from ca import alphabets, frontiers, loci, neighborhoods, rules, seeds
source = loci.history_configuration((True, False, False))
program = ca.SimpleProgram(
    seeds.exact(source),
    alphabets.boolean(),
    frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    ),
    neighborhoods.dyadlags_0d(configuration_contract=source.contract),
    rules.dyadlags_0d(rule=150),
)
assert isinstance(ca.apply(program, source), ca.program.ApplicationComplete)
assert "ca.catalog" not in sys.modules
"""
    completed = subprocess.run(
        [sys.executable, "-c", script],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr


def test_generic_application_contains_no_family_or_descriptor_dispatch() -> None:
    source = inspect.getsource(program.apply)
    tree = ast.parse(source)
    names = {
        node.id for node in ast.walk(tree) if isinstance(node, ast.Name)
    }
    attributes = {
        node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
    }

    assert names.isdisjoint({"SPF", "F", "T"})
    assert attributes.isdisjoint({"family_id", "catalog_id", "carrier_label"})
    assert "RulePrimitive" not in source
    assert "LocusKind" not in source


def test_public_surface_submodules_and_signatures_are_exact() -> None:
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
    assert str(inspect.signature(ca.apply)) == (
        "(program: 'SimpleProgram[C, V, W, R]', "
        "input: 'C | ApplicationInput[C]') -> 'ApplicationResult[C]'"
    )
    assert str(inspect.signature(ca.rollout)) == (
        "(program: 'SimpleProgram[C, V, W, R]', *, steps: 'int', "
        "initial: 'C | None' = None, replay_key: 'ReplayKey | None' = None) "
        "-> 'RolloutResult[C]'"
    )
    assert callable(ca.rollout)
    assert importlib.util.find_spec("ca.rollout") is None
    assert importlib.util.find_spec("ca.specs") is None


def test_rollout_matches_manual_repeated_apply_for_deterministic_and_branching_cases(
    monkeypatch,
) -> None:
    simple_program, source, _ = native_program("dyadlags")
    first = ca.apply(simple_program, source)
    assert isinstance(first, program.ApplicationComplete)
    first_successor = first.successor_quotient_with_derivation_fibers.atoms[0].successor
    second = ca.apply(simple_program, first_successor)
    assert isinstance(second, program.ApplicationComplete)
    manual_successor = second.successor_quotient_with_derivation_fibers.atoms[0].successor

    calls = []
    real_apply = program.apply

    def spy(*args, **kwargs):
        calls.append(args[1])
        return real_apply(*args, **kwargs)

    monkeypatch.setattr(program, "apply", spy)
    traversed = ca.rollout(simple_program, steps=2, initial=source)

    assert isinstance(traversed, program.RolloutTruncated)
    assert len(calls) == 2
    assert traversed.continuing_leaves.atoms[0].configuration == manual_successor

    branching_program, branching_source = diamond_program()
    branching = ca.rollout(
        branching_program,
        steps=1,
        initial=branching_source,
    )
    assert isinstance(branching, program.RolloutTruncated)
    assert len(branching.raw_trace.derivation_edges.atoms) == 2
    assert len(branching.continuing_leaves.atoms) == 2
