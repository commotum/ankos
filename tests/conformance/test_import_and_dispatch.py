"""CT13: import ownership, one application law, and rollout reuse."""

from __future__ import annotations

import ast
import importlib
import importlib.util
import inspect
from pathlib import Path
import re
import subprocess
import sys
import textwrap

import pytest

import ca
from ca import program

from g7_fixtures import diamond_program, native_program


SOURCE_ROOT = Path(inspect.getsourcefile(ca)).parent
PROGRAM_PATH = SOURCE_ROOT / "program.py"
CORE_MODULES = (
    "loci",
    "alphabets",
    "seeds",
    "frontiers",
    "neighborhoods",
    "rules",
    "program",
)
CORE_DEPENDENCIES = {
    "loci": set(),
    # Alphabet owns closed value structure, including typed references to
    # structural identities.  This one-way base-layer edge introduces no
    # cycle: loci remains independent of every value/component owner.
    "alphabets": {"loci"},
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
CATEGORY_MODULES = {
    "automata",
    "criteria",
    "dynamica",
    "machina",
    "media",
    "substitua",
}
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
EXPECTED_ROOT_MODULES = {
    "__init__.py",
    "alphabets.py",
    "datasets.py",
    "frontiers.py",
    "loci.py",
    "neighborhoods.py",
    "program.py",
    "rng.py",
    "rules.py",
    "seeds.py",
    "serialization.py",
}
EXPECTED_CATALOG_MODULES = {
    "__init__.py",
    "automata.py",
    "criteria.py",
    "dynamica.py",
    "entries.py",
    "machina.py",
    "media.py",
    "substitua.py",
}
EXPECTED_VIZ_MODULES = {
    "__init__.py",
    "export.py",
    "format.py",
    "server.py",
}


def _tree(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _relative_import_roots(path: Path) -> set[str]:
    imports: set[str] = set()
    for node in ast.walk(_tree(path)):
        if not isinstance(node, ast.ImportFrom) or node.level == 0:
            continue
        if node.module:
            imports.add(node.module.split(".")[0])
        else:
            imports.update(alias.name.split(".")[0] for alias in node.names)
    return imports


def _imports_absolute_root(path: Path) -> bool:
    for node in ast.walk(_tree(path)):
        if isinstance(node, ast.Import):
            if any(
                alias.name == "ca" or alias.name.startswith("ca.")
                for alias in node.names
            ):
                return True
        elif (
            isinstance(node, ast.ImportFrom)
            and node.level == 0
            and node.module is not None
            and (node.module == "ca" or node.module.startswith("ca."))
        ):
            return True
    return False


def _top_level_functions(tree: ast.Module) -> dict[str, ast.FunctionDef]:
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }


def _rooted_function_graph(
    tree: ast.Module,
    root: str,
    *,
    stop_at: frozenset[str] = frozenset(),
) -> tuple[ast.FunctionDef, ...]:
    """Return module-local functions reached through explicit name calls."""

    functions = _top_level_functions(tree)
    pending = [root]
    reached: list[ast.FunctionDef] = []
    seen: set[str] = set()
    while pending:
        name = pending.pop()
        if name in seen:
            continue
        seen.add(name)
        node = functions[name]
        reached.append(node)
        pending.extend(
            call.func.id
            for call in ast.walk(node)
            if isinstance(call, ast.Call)
            and isinstance(call.func, ast.Name)
            and call.func.id in functions
            and call.func.id not in stop_at
        )
    return tuple(reached)


def _attribute_path(node: ast.expr) -> tuple[str, ...]:
    if isinstance(node, ast.Name):
        return (node.id,)
    if isinstance(node, ast.Attribute):
        prefix = _attribute_path(node.value)
        return (*prefix, node.attr) if prefix else ()
    return ()


def _identifier_sets(
    nodes: tuple[ast.FunctionDef, ...],
) -> tuple[set[str], set[str], set[str]]:
    names: set[str] = set()
    attributes: set[str] = set()
    strings: set[str] = set()
    for root in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.Name):
                names.add(node.id)
            elif isinstance(node, ast.Attribute):
                attributes.add(node.attr)
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                strings.add(node.value)
    return names, attributes, strings


def _call_paths(nodes: tuple[ast.FunctionDef, ...]) -> set[tuple[str, ...]]:
    return {
        path
        for root in nodes
        for node in ast.walk(root)
        if isinstance(node, ast.Call)
        for path in (_attribute_path(node.func),)
        if path
    }


def _attribute_paths(
    nodes: tuple[ast.FunctionDef, ...],
) -> set[tuple[str, ...]]:
    return {
        path
        for root in nodes
        for node in ast.walk(root)
        if isinstance(node, ast.Attribute)
        for path in (_attribute_path(node),)
        if path
    }


def _assert_no_dispatch_vocabulary(
    nodes: tuple[ast.FunctionDef, ...],
) -> None:
    names, attributes, strings = _identifier_sets(nodes)
    forbidden_names = {
        "SPF",
        "F",
        "T",
        "family_id",
        "catalog_id",
        "carrier_label",
        "constructor_name",
        "book_category",
        "semantic_family",
        "book_source",
        "source_ref",
        "rule_tag",
        "rule_kind",
        "LocusKind",
        "RulePrimitive",
        "apply_rule",
        "globals",
        "locals",
        "vars",
        "__import__",
        "import_module",
    }
    forbidden_attributes = {
        "family_id",
        "catalog_id",
        "carrier_label",
        "constructor_name",
        "book_category",
        "semantic_family",
        "book_source",
        "source_ref",
        "rule_tag",
        "rule_kind",
        "apply_rule",
        "__dict__",
    }
    assert names.isdisjoint(forbidden_names)
    assert attributes.isdisjoint(forbidden_attributes)
    assert not any(
        re.fullmatch(r"(?:SPF|F|T)\d{3}", value)
        for value in strings
    )
    assert not {
        "semantic-family",
        "book-source",
        "constructor-name",
        "catalog-id",
        "family-id",
        "rule-tag",
        "rule-kind",
    }.intersection(strings)
    assert not any(
        "rule" in path and path[-1] in {"kind", "primitive", "tag"}
        for path in _attribute_paths(nodes)
    )
    getattr_calls = [
        call
        for root in nodes
        for call in ast.walk(root)
        if isinstance(call, ast.Call)
        and isinstance(call.func, ast.Name)
        and call.func.id == "getattr"
    ]
    getattr_fields = {
        call.args[1].value
        for call in getattr_calls
        if len(call.args) >= 2
        if isinstance(call.args[1], ast.Constant)
        if isinstance(call.args[1].value, str)
    }
    assert len(getattr_calls) == len(getattr_fields)
    assert getattr_fields <= {"canonical_identity"}


def test_static_import_graph_matches_the_complete_one_way_package_dag() -> None:
    assert {
        path.name for path in SOURCE_ROOT.glob("*.py")
    } == EXPECTED_ROOT_MODULES
    assert {
        path.name for path in (SOURCE_ROOT / "catalog").glob("*.py")
    } == EXPECTED_CATALOG_MODULES
    assert {
        path.name for path in (SOURCE_ROOT / "viz").glob("*.py")
    } == EXPECTED_VIZ_MODULES

    for module_name, allowed in CORE_DEPENDENCIES.items():
        assert _relative_import_roots(SOURCE_ROOT / f"{module_name}.py") <= allowed

    root_allowed = {*CORE_MODULES, "catalog", "serialization"}
    assert _relative_import_roots(SOURCE_ROOT / "__init__.py") <= root_allowed
    assert _relative_import_roots(SOURCE_ROOT / "serialization.py") <= set(
        CORE_MODULES
    )

    catalog_path = SOURCE_ROOT / "catalog"
    assert not _relative_import_roots(catalog_path / "entries.py")
    for module_name in CATEGORY_MODULES:
        assert _relative_import_roots(catalog_path / f"{module_name}.py") <= set(
            CORE_MODULES
        )
    assert _relative_import_roots(catalog_path / "__init__.py") <= {
        *CATEGORY_MODULES,
        "entries",
    }
    metadata_importers = {
        path.relative_to(SOURCE_ROOT).as_posix()
        for path in SOURCE_ROOT.rglob("*.py")
        if "entries" in _relative_import_roots(path)
    }
    assert metadata_importers == {"catalog/__init__.py"}

    assert _relative_import_roots(SOURCE_ROOT / "datasets.py") <= {
        *CORE_MODULES,
        "rng",
    }
    assert not _relative_import_roots(SOURCE_ROOT / "rng.py")
    for path in (SOURCE_ROOT / "viz").glob("*.py"):
        assert _relative_import_roots(path) <= {
            "datasets",
            "export",
            "format",
            "server",
        }

    absolute_root_importers = {
        path.relative_to(SOURCE_ROOT).as_posix()
        for path in SOURCE_ROOT.rglob("*.py")
        if _imports_absolute_root(path)
    }
    assert not absolute_root_importers


def test_apply_works_and_whole_program_decodes_while_catalog_is_blocked() -> None:
    script = textwrap.dedent(
        """
        import importlib.abc
        import sys
        import ca
        from ca import alphabets, frontiers, loci, neighborhoods, rules, seeds

        source = loci.history_configuration((True, False, False))
        simple_program = ca.SimpleProgram(
            seeds.exact(source),
            alphabets.boolean(),
            frontiers.everywhere(
                configuration_contract=source.contract,
                value_profile=alphabets.ValueProfile.BOOLEAN,
            ),
            neighborhoods.dyadlags_0d(configuration_contract=source.contract),
            rules.dyadlags_0d(rule=150),
        )

        class BlockCatalog(importlib.abc.MetaPathFinder):
            def find_spec(self, fullname, path=None, target=None):
                if fullname == "ca.catalog" or fullname.startswith("ca.catalog."):
                    raise ImportError("catalog blocked")
                return None

        sys.meta_path.insert(0, BlockCatalog())
        for name in tuple(sys.modules):
            if name == "ca.catalog" or name.startswith("ca.catalog."):
                del sys.modules[name]

        applied = ca.apply(simple_program, source)
        assert isinstance(applied, ca.program.ApplicationComplete)
        encoded = ca.serialization.dumps(simple_program)
        decoded = ca.serialization.loads(encoded)
        assert decoded == ca.serialization.Decoded(simple_program)
        assert ca.serialization.dumps(decoded.value) == encoded
        assert ca.apply(decoded.value, source) == applied
        assert not any(
            name == "ca.catalog" or name.startswith("ca.catalog.")
            for name in sys.modules
        )
        """
    )
    completed = subprocess.run(
        [sys.executable, "-c", script],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr


def test_apply_is_the_only_production_step_and_its_call_graph_has_no_dispatch() -> None:
    apply_definitions = [
        (path.relative_to(SOURCE_ROOT).as_posix(), node.lineno)
        for path in SOURCE_ROOT.rglob("*.py")
        for node in ast.walk(_tree(path))
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "apply"
    ]
    assert apply_definitions == [("program.py", program.apply.__code__.co_firstlineno)]

    tree = _tree(PROGRAM_PATH)
    apply_graph = _rooted_function_graph(tree, "apply")
    _assert_no_dispatch_vocabulary(apply_graph)
    functions = _top_level_functions(tree)
    rule_denotation_owners = {
        name
        for name, node in functions.items()
        for call in ast.walk(node)
        if isinstance(call, ast.Call)
        and _attribute_path(call.func)[-2:] == ("rule", "denote")
    }
    commit_owners = {
        name
        for name, node in functions.items()
        for call in ast.walk(node)
        if isinstance(call, ast.Call)
        and isinstance(call.func, ast.Name)
        and call.func.id == "_commit"
    }
    assert rule_denotation_owners == {"apply"}
    assert commit_owners == {"apply"}


def test_rollout_statically_reuses_apply_without_a_second_step_path() -> None:
    tree = _tree(PROGRAM_PATH)
    rollout_node = _top_level_functions(tree)["rollout"]
    direct_apply_calls = [
        call
        for call in ast.walk(rollout_node)
        if isinstance(call, ast.Call)
        and isinstance(call.func, ast.Name)
        and call.func.id == "apply"
    ]
    assert len(direct_apply_calls) == 1

    # The apply call itself is the authorized step boundary; inspect all
    # rollout-owned helpers without traversing through that boundary.
    rollout_graph = _rooted_function_graph(
        tree,
        "rollout",
        stop_at=frozenset({"apply"}),
    )
    _assert_no_dispatch_vocabulary(rollout_graph)
    names, attributes, _ = _identifier_sets(rollout_graph)
    assert names.isdisjoint({"tensor", "family", "apply_rule"})
    assert attributes.isdisjoint({"tensor", "family", "apply_rule"})

    # Seed binding may inspect the program's Seed, but traversal must not
    # resolve transition regions, denote a Rule, or commit a replacement.
    call_paths = _call_paths(rollout_graph)
    assert not any(
        path[-2:] in {
            ("frontier", "resolve"),
            ("neighborhood", "resolve"),
            ("rule", "denote"),
        }
        for path in call_paths
    )


def test_public_surface_submodules_and_signatures_are_exact() -> None:
    assert ca.__all__ == [
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
    catalog_callable_names = {
        name
        for name in ca.catalog.__all__
        if callable(getattr(ca.catalog, name))
    }
    assert not {
        name for name in catalog_callable_names if hasattr(ca, name)
    }
    for submodule in OBSOLETE_PUBLIC_SUBMODULES:
        qualified = f"ca.{submodule}"
        assert importlib.util.find_spec(qualified) is None
        with pytest.raises(ModuleNotFoundError):
            importlib.import_module(qualified)


def _manual_rollout(simple_program, source, *, steps, step):
    root_lineage = program.TraceLineage(
        ca.loci.canonical_identity(
            ("seed-root", ca.loci.configuration_identity(source))
        )
    )
    continuing = [program.ContinuingLeaf(source, root_lineage)]
    applications = []
    edges = []
    lineage_edges = []
    inputs = []

    for _ in range(steps):
        next_continuing = []
        for leaf in continuing:
            application_input = program.ApplicationInput(
                leaf.configuration,
                leaf.trace_lineage,
            )
            inputs.append(application_input)
            result = step(simple_program, application_input)
            assert isinstance(result, program.ApplicationComplete)
            assert (
                result.applied_atoms.presentation
                is ca.rules.SupportPresentation.FINITE
            )
            applications.append(result)
            for atom in result.applied_atoms.atoms:
                assert isinstance(atom, program.AppliedDerivation)
                assert isinstance(atom.source.continuation, ca.rules.Continue)
                edges.append(atom)
                lineage_edges.append(
                    program.TraceEdge(
                        leaf.trace_lineage,
                        atom.output_trace_lineage,
                        atom.canonical_identity,
                    )
                )
                next_continuing.append(
                    program.ContinuingLeaf(
                        atom.successor,
                        atom.output_trace_lineage,
                    )
                )
        continuing = next_continuing

    roots = ca.rules.OutcomeSpace(
        ca.rules.finite_support((source,), label="seed-roots"),
        None,
    )
    seed_evidence = program.SeedRealizationEvidence(
        "explicit-initial",
        None,
        None,
        None,
        (),
    )
    raw_trace = program.RawTrace(
        roots,
        ca.rules.finite_support(
            tuple(applications),
            label="rollout-applications",
        ),
        ca.rules.finite_support(tuple(edges), label="rollout-edges"),
        tuple(lineage_edges),
        seed_evidence,
        (),
    )
    return (
        program.RolloutTruncated(
            raw_trace,
            ca.rules.finite_support(
                tuple(continuing),
                label="continuing-leaves",
            ),
            program.TruncationCause.DEPTH_BOUND,
        ),
        tuple(inputs),
    )


def test_rollout_exactly_matches_manual_apply_for_full_deterministic_and_branching_results(
    monkeypatch,
) -> None:
    real_apply = program.apply
    cases = []

    deterministic_program, deterministic_source, _ = native_program("dyadlags")
    cases.append((deterministic_program, deterministic_source, 2))
    branching_program, branching_source = diamond_program()
    cases.append((branching_program, branching_source, 1))

    for simple_program, source, steps in cases:
        expected, expected_inputs = _manual_rollout(
            simple_program,
            source,
            steps=steps,
            step=real_apply,
        )
        calls = []

        def spy(subject, application_input):
            calls.append(application_input)
            return real_apply(subject, application_input)

        monkeypatch.setattr(program, "apply", spy)
        actual = ca.rollout(simple_program, steps=steps, initial=source)

        assert calls == list(expected_inputs)
        assert actual == expected
