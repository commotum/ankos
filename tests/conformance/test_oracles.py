"""Frozen implementation-independent one-step oracles for Goal 7 CT12.

This module is deliberately both fixture data and its Stage 1 consistency
suite.  It imports only the Python standard library and contains no transition
evaluator.  Future CT12 tests map real ``ApplicationResult`` records onto these
closed test-only terms; the runtime must never import this module.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, fields, is_dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Literal, TypeAlias


OracleScalar: TypeAlias = bool | int | Fraction | str | None
Action: TypeAlias = Literal["preserve", "replace", "delete", "absent", "create"]
AtomKind: TypeAlias = Literal["derivation", "no-successor"]
Progress: TypeAlias = Literal["advanced", "quiescent"]
SupportKind: TypeAlias = Literal["finite", "intensional"]
CardinalityKind: TypeAlias = Literal["exact", "uncountable"]
MeasureKind: TypeAlias = Literal["absent", "available", "unavailable"]


@dataclass(frozen=True)
class OracleTerm:
    """One exact symbolic test term with no evaluation behavior."""

    tag: str
    arguments: tuple[OracleScalar | OracleTerm, ...] = ()


OracleValue: TypeAlias = OracleScalar | OracleTerm


@dataclass(frozen=True)
class OracleCardinality:
    """An exact finite or named intensional cardinality."""

    kind: CardinalityKind
    value: int | None


@dataclass(frozen=True)
class OracleDisposition:
    """One explicit total-disposition entry over a writable capability."""

    target: OracleTerm
    action: Action
    value: OracleValue = None


@dataclass(frozen=True)
class OracleSourceAtom:
    """One complete expected Rule atom before reconstruction and commit."""

    atom_id: str
    kind: AtomKind
    witness: OracleTerm
    provenance: tuple[str, ...]
    progress: Progress | None
    continuation: OracleTerm | None
    dispositions: tuple[OracleDisposition, ...]
    reason: OracleTerm | None
    certificate: OracleTerm
    mass: Fraction | None = None


@dataclass(frozen=True)
class OracleFiber:
    """One expected semantic successor and its complete derivation fiber."""

    successor: OracleTerm
    atom_ids: tuple[str, ...]


@dataclass(frozen=True)
class OracleFreshBinding:
    """One structural fresh-identity recipe and its exact bound identity."""

    local_key: OracleTerm
    identity: OracleTerm
    evidence: OracleTerm


@dataclass(frozen=True)
class OracleAppliedAtom:
    """One source atom after generic binding, reconstruction, and validation."""

    atom_id: str
    source_atom_id: str
    successor: OracleTerm | None
    fresh_bindings: tuple[OracleFreshBinding, ...]
    output_trace_lineage: OracleTerm
    evidence: OracleTerm


@dataclass(frozen=True)
class OracleMeasureView:
    """One explicitly absent, available, or unavailable measure view."""

    kind: MeasureKind
    masses: tuple[tuple[OracleValue, Fraction], ...]
    total_mass: Fraction | None
    evidence: OracleTerm | None


@dataclass(frozen=True)
class OracleMeasures:
    """The three non-renormalized measure views owned by application."""

    applied_atoms: OracleMeasureView
    successors: OracleMeasureView
    no_successors: OracleMeasureView


@dataclass(frozen=True)
class OracleExpected:
    """Complete normalized expectation for one generic application."""

    support_kind: SupportKind
    source_outcomes: tuple[OracleSourceAtom, ...]
    applied_atoms: tuple[OracleAppliedAtom, ...]
    no_successor_partition: tuple[OracleAppliedAtom, ...]
    outcome_cardinality: OracleCardinality
    derivation_cardinality: OracleCardinality
    successor_cardinality: OracleCardinality
    successor_fibers: tuple[OracleFiber, ...]
    measures: OracleMeasures
    source_intensional_relation: OracleTerm | None
    applied_intensional_relation: OracleTerm | None
    successor_intensional_relation: OracleTerm | None
    evidence: OracleTerm


@dataclass(frozen=True)
class OracleCase:
    """One named CT12 input/read/write/result fixture."""

    case_id: str
    mechanics: tuple[str, ...]
    conformance_refs: tuple[str, ...]
    current_native: bool
    source: OracleTerm
    writable: tuple[OracleTerm, ...]
    readable: OracleTerm
    expected: OracleExpected


@dataclass(frozen=True)
class PreCutoverSnapshot:
    """Exact historical facts needed by later cutover-negative tests."""

    goal6_close_commit: str
    preimplementation_shell_commit: str
    execution_start_commit: str
    goal6_runtime_src_tree: str
    goal6_runtime_tests_tree: str
    execution_start_src_tree: str
    execution_start_tests_tree: str
    goal2_tree: str
    goal5_tree: str
    goal6_tree: str
    python_version: str
    numpy_version: str
    package_version: str
    package_description: str
    runtime_dependencies: tuple[str, ...]
    active_test_baseline: str
    public_manifest_sha256: str
    public_manifest_algorithm: str
    root_exports: tuple[str, ...]
    target_root_exports: tuple[str, ...]
    eager_imports: tuple[str, ...]
    physical_modules_to_remove: tuple[str, ...]
    obsolete_execution_sites: tuple[str, ...]
    frozen_git_blobs: tuple[tuple[str, str], ...]
    frozen_sha256: tuple[tuple[str, str], ...]


def _term(tag: str, *arguments: OracleValue) -> OracleTerm:
    """Construct inert fixture syntax; this function performs no evaluation."""

    return OracleTerm(tag=tag, arguments=arguments)


def _disposition(
    target: OracleTerm,
    action: Action,
    value: OracleValue = None,
) -> OracleDisposition:
    """Construct one inert expected disposition."""

    return OracleDisposition(target=target, action=action, value=value)


def _applied(
    source: OracleSourceAtom,
    successor: OracleTerm | None,
    case_id: str,
    fresh_bindings: tuple[OracleFreshBinding, ...] = (),
) -> OracleAppliedAtom:
    """Construct inert applied-atom data without reconstructing a successor."""

    return OracleAppliedAtom(
        atom_id=source.atom_id,
        source_atom_id=source.atom_id,
        successor=successor,
        fresh_bindings=fresh_bindings,
        output_trace_lineage=_term("lineage", case_id, source.atom_id),
        evidence=_term("applied-atom-evidence", case_id, source.atom_id),
    )


EXACT_ZERO = OracleCardinality("exact", 0)
EXACT_ONE = OracleCardinality("exact", 1)
EXACT_TWO = OracleCardinality("exact", 2)
EXACT_THREE = OracleCardinality("exact", 3)
UNCOUNTABLE = OracleCardinality("uncountable", None)
ABSENT_MEASURE = OracleMeasureView(
    kind="absent",
    masses=(),
    total_mass=None,
    evidence=None,
)
ABSENT_MEASURES = OracleMeasures(
    applied_atoms=ABSENT_MEASURE,
    successors=ABSENT_MEASURE,
    no_successors=ABSENT_MEASURE,
)


PRE_CUTOVER = PreCutoverSnapshot(
    goal6_close_commit="60bde6da318f415e43e14fc98b5faa28f14cd945",
    preimplementation_shell_commit="1562041e4dab0a6d9e51d730222de0a4f1b52038",
    execution_start_commit="95ba134ee8f9671181c237cd2975004f3442efbe",
    goal6_runtime_src_tree="6e6b34769d60508c03d0a69fad1ede4fef75e217",
    goal6_runtime_tests_tree="02ad081e039a46efbf61855fdeae60abb7bb70ad",
    execution_start_src_tree="af9ae63c9b3683fd9b7ba1292d9127f647dc48f5",
    execution_start_tests_tree="a77a8f6092c9b3f907a1bd6aee7c6b09c1055fa7",
    goal2_tree="48b6309655ec7c1d3aaa1a0ec5dfb700385e16d1",
    goal5_tree="ba62f20b8c620094a0ad683906a803c5404be5f2",
    goal6_tree="dfeaa1d302acceb274a6dec815ae587dada7ac78",
    python_version="3.10.13",
    numpy_version="2.2.6",
    package_version="0.1.0",
    package_description="A New Kind of Science cellular automata library",
    runtime_dependencies=("numpy>=2.2", "pytest>=9.0.3"),
    active_test_baseline="102 passed, 96 skipped",
    public_manifest_sha256=(
        "fe4f136f50cf1471268278b5f62a33492bad090808605a9a3f7c048aed81a4f2"
    ),
    public_manifest_algorithm=(
        "iterate ordered ca.__all__; obj=getattr(ca,name); "
        "module=getattr(obj,'__module__',None); kind=type(obj).__name__; "
        "signature=str(inspect.signature(obj)) with TypeError/ValueError -> None; "
        "rows contain exactly name,module,kind,signature; "
        "json.dumps(rows,sort_keys=True,separators=(',',':')).encode('utf-8'); "
        "sha256 bytes with no trailing newline"
    ),
    root_exports=(
        "Alphabet",
        "Dynamics",
        "Frontier",
        "Neighborhood",
        "RawBatch",
        "RawEpisode",
        "Rule",
        "RuleChannel",
        "Seed",
        "alphabets",
        "apply_rule",
        "ar2_0d",
        "ar2_modular_0d",
        "axis_shell",
        "bernoulli",
        "boolean",
        "canonical_coords",
        "change_count_shell",
        "constant",
        "derive_episode_rng",
        "directional_fov",
        "directional_line",
        "dyadlags_0d_neighborhood",
        "dyadlags_0d_rule",
        "lagcounts_0d_neighborhood",
        "lagcounts_0d_rule",
        "dyadrads_1d_neighborhood",
        "dyadrads_1d_rule",
        "dyadaxes_2d_neighborhood",
        "dyadaxes_2d_rule",
        "dyadaxes_3d_neighborhood",
        "dyadaxes_3d_rule",
        "datasets",
        "dynamics_from_spec",
        "eca",
        "float_range_alphabet",
        "frontiers",
        "history",
        "instantiate",
        "int_range_alphabet",
        "l1_shell",
        "literal_offsets",
        "loci",
        "metric_radius",
        "moore",
        "neighborhoods",
        "numpy_rng",
        "pair",
        "point",
        "render",
        "rng",
        "rollout",
        "rollout_batch",
        "rule_count",
        "rules",
        "selector_seed",
        "seeds",
        "self_at",
        "shell",
        "splitmix64",
        "symbolic",
        "time_slice",
        "uniform_bits",
        "uniform_pair",
        "valid_rule_ids",
        "viz",
        "von_neumann",
    ),
    target_root_exports=(
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
        "serialization",
        "catalog",
    ),
    eager_imports=(
        "ca.specs",
        "ca.rollout",
        "ca.datasets",
        "ca.rng",
        "ca.viz",
    ),
    physical_modules_to_remove=("ca.rollout", "ca.specs"),
    obsolete_execution_sites=(
        "src/ca/__init__.py imports ca.specs and ca.rollout",
        "src/ca/datasets.py imports ca.specs and ca.rollout",
        "src/ca/datasets.py branches on _rule and _neighborhood",
        "src/ca/viz/export.py imports ca.specs",
        "src/ca/rules.py instantiate branches on rule.family",
    ),
    frozen_git_blobs=(
        ("src/ca/__init__.py", "1f4868f38ba209b862bd2a0855bcd638f40497e1"),
        ("src/ca/specs.py", "a6f92d421b5af773a68301ae7c7b542a915c2416"),
        ("src/ca/rollout.py", "1191137be02192a86c775da3a91b3dbe2eabc33d"),
        (
            "tests/test_specs.py",
            "88eceb78a7b33168ea97e7e5885419dc415f021f",
        ),
        (
            "tests/test_rollout.py",
            "2f34d1a78dd599e381ed31a5e3d4adbf2123d320",
        ),
        ("pyproject.toml", "16b8eecc60521130e742fb6c3eb64e02b41c3861"),
        ("uv.lock", "5eacafdd1c819f6c50080268156b58e8a10fdf25"),
    ),
    frozen_sha256=(
        (
            "src/ca/__init__.py",
            "34729bcbde8109ea46e52fc1912f06c50e58737d5d936ea7958d2369e433401d",
        ),
        (
            "src/ca/specs.py",
            "8593ca05fb6be723513802a5019428d84c7bf36d9a8e2a7122afbb076ed523a4",
        ),
        (
            "src/ca/rollout.py",
            "ba14aa66c6494cd35f3601f0fed25d0d590e64aede014314ac72d3177018f44b",
        ),
        (
            "pyproject.toml",
            "3f278bba4c64719fe76546e3470a0954bb506c25daa3a9d4b79a9e02f7cb2345",
        ),
        (
            "uv.lock",
            "7ec09380d160d9f1299793091c0ed02579aa1db7cb6e83f5df41093bc00b7600",
        ),
    ),
)


# N01: retained native scalar AR2, rule 17 means a=2, b=1, constant=1.
AR2_PREVIOUS = _term("field", "previous")
AR2_CURRENT = _term("field", "current")
AR2_SOURCE = _term(
    "configuration.record",
    _term("field-value", "previous", 3),
    _term("field-value", "current", 5),
)
AR2_SUCCESSOR = _term(
    "configuration.record",
    _term("field-value", "previous", 5),
    _term("field-value", "current", 14),
)
AR2_ATOM = OracleSourceAtom(
    atom_id="ar2-step",
    kind="derivation",
    witness=_term("witness.rule", "ar2-modular", "rule-id", 17),
    provenance=("native:ar2_modular_0d", "rule-17:a=2,b=1,c=1,mod=97"),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(AR2_PREVIOUS, "replace", 5),
        _disposition(AR2_CURRENT, "replace", 14),
    ),
    reason=None,
    certificate=_term(
        "arithmetic-certificate",
        _term("equals", _term("mod", _term("sum", 10, 3, 1), 97), 14),
    ),
)
AR2_CASE = OracleCase(
    case_id="native.scalar.ar2-modular",
    mechanics=("current-scalar",),
    conformance_refs=("G7-00:current-scalar", "CT12"),
    current_native=True,
    source=AR2_SOURCE,
    writable=(AR2_PREVIOUS, AR2_CURRENT),
    readable=_term(
        "read.record",
        _term("field-value", "previous", 3),
        _term("field-value", "current", 5),
    ),
    expected=OracleExpected(
        support_kind="finite",
        source_outcomes=(AR2_ATOM,),
        applied_atoms=(
            _applied(
                AR2_ATOM,
                AR2_SUCCESSOR,
                "native.scalar.ar2-modular",
            ),
        ),
        no_successor_partition=(),
        outcome_cardinality=EXACT_ONE,
        derivation_cardinality=EXACT_ONE,
        successor_cardinality=EXACT_ONE,
        successor_fibers=(OracleFiber(AR2_SUCCESSOR, ("ar2-step",)),),
        measures=ABSENT_MEASURES,
        source_intensional_relation=None,
        applied_intensional_relation=None,
        successor_intensional_relation=None,
        evidence=_term("application-evidence", "native.scalar.ar2-modular"),
    ),
)


# N02: retained native temporal 3-lag lookup.
DYAD_OLDER = _term("history-slot", "older")
DYAD_PREVIOUS = _term("history-slot", "previous")
DYAD_CURRENT = _term("history-slot", "current")
DYADLAGS_SOURCE = _term("history", _term("values", 1, 0, 0))
DYADLAGS_SUCCESSOR = _term("history", _term("values", 0, 0, 1))
DYADLAGS_ATOM = OracleSourceAtom(
    atom_id="dyadlags-rule-150",
    kind="derivation",
    witness=_term(
        "lookup-witness",
        "dyadlags-0d",
        _term("context", 1, 0, 0),
        _term("index", 4),
        _term("rule-id", 150),
    ),
    provenance=("native:dyadlags_0d", "rule-150:bit-4=1"),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(DYAD_OLDER, "replace", 0),
        _disposition(DYAD_PREVIOUS, "replace", 0),
        _disposition(DYAD_CURRENT, "replace", 1),
    ),
    reason=None,
    certificate=_term("lookup-certificate", 150, 4, 1),
)
DYADLAGS_CASE = OracleCase(
    case_id="native.temporal.dyadlags-rule-150",
    mechanics=("current-temporal",),
    conformance_refs=("G7-00:current-temporal", "CT12"),
    current_native=True,
    source=DYADLAGS_SOURCE,
    writable=(DYAD_OLDER, DYAD_PREVIOUS, DYAD_CURRENT),
    readable=_term("temporal-lag-view", _term("values", 1, 0, 0)),
    expected=OracleExpected(
        support_kind="finite",
        source_outcomes=(DYADLAGS_ATOM,),
        applied_atoms=(
            _applied(
                DYADLAGS_ATOM,
                DYADLAGS_SUCCESSOR,
                "native.temporal.dyadlags-rule-150",
            ),
        ),
        no_successor_partition=(),
        outcome_cardinality=EXACT_ONE,
        derivation_cardinality=EXACT_ONE,
        successor_cardinality=EXACT_ONE,
        successor_fibers=(
            OracleFiber(DYADLAGS_SUCCESSOR, ("dyadlags-rule-150",)),
        ),
        measures=ABSENT_MEASURES,
        source_intensional_relation=None,
        applied_intensional_relation=None,
        successor_intensional_relation=None,
        evidence=_term(
            "application-evidence",
            "native.temporal.dyadlags-rule-150",
        ),
    ),
)


# N03: retained native count-banded temporal lookup.
LAG_0 = _term("history-index", 0)
LAG_1 = _term("history-index", 1)
LAG_2 = _term("history-index", 2)
LAG_3 = _term("history-index", 3)
LAG_4 = _term("history-index", 4)
LAG_5 = _term("history-index", 5)
LAG_6 = _term("history-index", 6)
LAG_7 = _term("history-index", 7)
LAG_8 = _term("history-index", 8)
LAG_9 = _term("history-index", 9)
LAGCOUNTS_SOURCE = _term(
    "history",
    _term("values", 1, 0, 1, 1, 0, 0, 1, 0, 1, 1),
)
LAGCOUNTS_SUCCESSOR = _term(
    "history",
    _term("values", 0, 1, 1, 0, 0, 1, 0, 1, 1, 1),
)
LAGCOUNTS_ATOM = OracleSourceAtom(
    atom_id="lagcounts-rule-91",
    kind="derivation",
    witness=_term(
        "count-band-witness",
        _term("current", 1),
        _term("band-counts", 2, 1, 2),
        _term("context", 77),
        _term("rule-id", 91),
    ),
    provenance=(
        "native:lagcounts_0d",
        "hash-word:0x3238ad129bb6db1d",
        "output-bit:1",
    ),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(LAG_0, "replace", 0),
        _disposition(LAG_1, "replace", 1),
        _disposition(LAG_2, "replace", 1),
        _disposition(LAG_3, "replace", 0),
        _disposition(LAG_4, "replace", 0),
        _disposition(LAG_5, "replace", 1),
        _disposition(LAG_6, "replace", 0),
        _disposition(LAG_7, "replace", 1),
        _disposition(LAG_8, "replace", 1),
        _disposition(LAG_9, "replace", 1),
    ),
    reason=None,
    certificate=_term(
        "deterministic-table-certificate",
        91,
        77,
        "0x3238ad129bb6db1d",
        1,
    ),
)
LAGCOUNTS_WRITABLE = (
    LAG_0,
    LAG_1,
    LAG_2,
    LAG_3,
    LAG_4,
    LAG_5,
    LAG_6,
    LAG_7,
    LAG_8,
    LAG_9,
)
LAGCOUNTS_CASE = OracleCase(
    case_id="native.temporal.lagcounts-rule-91",
    mechanics=("current-temporal",),
    conformance_refs=("G7-00:current-temporal", "CT12"),
    current_native=True,
    source=LAGCOUNTS_SOURCE,
    writable=LAGCOUNTS_WRITABLE,
    readable=_term(
        "count-banded-history-view",
        _term("current", 1),
        _term("recent", 1, 0, 1),
        _term("middle", 1, 0, 0),
        _term("oldest", 1, 0, 1),
    ),
    expected=OracleExpected(
        support_kind="finite",
        source_outcomes=(LAGCOUNTS_ATOM,),
        applied_atoms=(
            _applied(
                LAGCOUNTS_ATOM,
                LAGCOUNTS_SUCCESSOR,
                "native.temporal.lagcounts-rule-91",
            ),
        ),
        no_successor_partition=(),
        outcome_cardinality=EXACT_ONE,
        derivation_cardinality=EXACT_ONE,
        successor_cardinality=EXACT_ONE,
        successor_fibers=(
            OracleFiber(LAGCOUNTS_SUCCESSOR, ("lagcounts-rule-91",)),
        ),
        measures=ABSENT_MEASURES,
        source_intensional_relation=None,
        applied_intensional_relation=None,
        successor_intensional_relation=None,
        evidence=_term(
            "application-evidence",
            "native.temporal.lagcounts-rule-91",
        ),
    ),
)


# N04: retained native 1-D Dyadrads lookup with fixed-zero topology.
LINE_0 = _term("cell1d", 0)
LINE_1 = _term("cell1d", 1)
LINE_2 = _term("cell1d", 2)
LINE_3 = _term("cell1d", 3)
LINE_4 = _term("cell1d", 4)
LINE_SOURCE = _term(
    "line1d",
    _term("topology", "finite-line", 5),
    _term("default", 0),
    _term("values", 1, 0, 1, 0, 0),
)
LINE_SUCCESSOR = _term(
    "line1d",
    _term("topology", "finite-line", 5),
    _term("default", 0),
    _term("values", 0, 1, 0, 1, 1),
)
LINE_ATOM = OracleSourceAtom(
    atom_id="dyadrads-rule-30",
    kind="derivation",
    witness=_term(
        "lookup-witness",
        "dyadrads-1d",
        _term("indices", 5, 2, 5, 2, 4),
        _term("rule-id", 30),
    ),
    provenance=("native:dyadrads_1d", "configuration-topology:fixed-zero", "rule-30"),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(LINE_0, "replace", 0),
        _disposition(LINE_1, "replace", 1),
        _disposition(LINE_2, "replace", 0),
        _disposition(LINE_3, "replace", 1),
        _disposition(LINE_4, "replace", 1),
    ),
    reason=None,
    certificate=_term("lookup-certificate", 30, _term("indices", 5, 2, 5, 2, 4)),
)
LINE_CASE = OracleCase(
    case_id="native.cellular.dyadrads-rule-30",
    mechanics=("current-cellular", "cellular"),
    conformance_refs=("G7-00:current-cellular", "CT12"),
    current_native=True,
    source=LINE_SOURCE,
    writable=(LINE_0, LINE_1, LINE_2, LINE_3, LINE_4),
    readable=_term("old-snapshot-stencils", LINE_SOURCE),
    expected=OracleExpected(
        support_kind="finite",
        source_outcomes=(LINE_ATOM,),
        applied_atoms=(
            _applied(
                LINE_ATOM,
                LINE_SUCCESSOR,
                "native.cellular.dyadrads-rule-30",
            ),
        ),
        no_successor_partition=(),
        outcome_cardinality=EXACT_ONE,
        derivation_cardinality=EXACT_ONE,
        successor_cardinality=EXACT_ONE,
        successor_fibers=(OracleFiber(LINE_SUCCESSOR, ("dyadrads-rule-30",)),),
        measures=ABSENT_MEASURES,
        source_intensional_relation=None,
        applied_intensional_relation=None,
        successor_intensional_relation=None,
        evidence=_term("application-evidence", "native.cellular.dyadrads-rule-30"),
    ),
)


# N05: retained native 2-D Dyadaxes lookup with fixed-zero topology.
GRID_NW = _term("cell2d", -1, -1)
GRID_N = _term("cell2d", -1, 0)
GRID_NE = _term("cell2d", -1, 1)
GRID_W = _term("cell2d", 0, -1)
GRID_C = _term("cell2d", 0, 0)
GRID_E = _term("cell2d", 0, 1)
GRID_SW = _term("cell2d", 1, -1)
GRID_S = _term("cell2d", 1, 0)
GRID_SE = _term("cell2d", 1, 1)
GRID_SOURCE = _term(
    "grid2d",
    _term("topology", "finite-grid", 3, 3),
    _term("default", 0),
    _term("row", 1, 1, 1),
    _term("row", 1, 1, 1),
    _term("row", 1, 1, 1),
)
GRID_SUCCESSOR = _term(
    "grid2d",
    _term("topology", "finite-grid", 3, 3),
    _term("default", 0),
    _term("row", 0, 0, 0),
    _term("row", 0, 1, 0),
    _term("row", 0, 0, 0),
)
GRID_WRITABLE = (
    GRID_NW,
    GRID_N,
    GRID_NE,
    GRID_W,
    GRID_C,
    GRID_E,
    GRID_SW,
    GRID_S,
    GRID_SE,
)
GRID_ATOM = OracleSourceAtom(
    atom_id="dyadaxes-2d-rule-128",
    kind="derivation",
    witness=_term(
        "lookup-witness",
        "dyadaxes-2d",
        _term(
            "index-grid",
            _term("row", 1, 3, 1),
            _term("row", 3, 7, 3),
            _term("row", 1, 3, 1),
        ),
        _term("rule-id", 128),
    ),
    provenance=(
        "native:dyadaxes_2d",
        "configuration-topology:fixed-zero",
        "rule-128",
    ),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(GRID_NW, "replace", 0),
        _disposition(GRID_N, "replace", 0),
        _disposition(GRID_NE, "replace", 0),
        _disposition(GRID_W, "replace", 0),
        _disposition(GRID_C, "replace", 1),
        _disposition(GRID_E, "replace", 0),
        _disposition(GRID_SW, "replace", 0),
        _disposition(GRID_S, "replace", 0),
        _disposition(GRID_SE, "replace", 0),
    ),
    reason=None,
    certificate=_term("lookup-certificate", 128, "bit-7-only"),
)
GRID_CASE = OracleCase(
    case_id="native.multidimensional.dyadaxes-2d-rule-128",
    mechanics=("current-multidimensional", "cellular"),
    conformance_refs=("G7-00:current-multidimensional", "CT12"),
    current_native=True,
    source=GRID_SOURCE,
    writable=GRID_WRITABLE,
    readable=_term("old-snapshot-2d-stencils", GRID_SOURCE),
    expected=OracleExpected(
        support_kind="finite",
        source_outcomes=(GRID_ATOM,),
        applied_atoms=(
            _applied(
                GRID_ATOM,
                GRID_SUCCESSOR,
                "native.multidimensional.dyadaxes-2d-rule-128",
            ),
        ),
        no_successor_partition=(),
        outcome_cardinality=EXACT_ONE,
        derivation_cardinality=EXACT_ONE,
        successor_cardinality=EXACT_ONE,
        successor_fibers=(
            OracleFiber(GRID_SUCCESSOR, ("dyadaxes-2d-rule-128",)),
        ),
        measures=ABSENT_MEASURES,
        source_intensional_relation=None,
        applied_intensional_relation=None,
        successor_intensional_relation=None,
        evidence=_term(
            "application-evidence",
            "native.multidimensional.dyadaxes-2d-rule-128",
        ),
    ),
)


# N06: retained native 3-D Dyadaxes lookup with fixed-zero topology.
C_MMM = _term("cell3d", -1, -1, -1)
C_MMZ = _term("cell3d", -1, -1, 0)
C_MMP = _term("cell3d", -1, -1, 1)
C_MZM = _term("cell3d", -1, 0, -1)
C_MZZ = _term("cell3d", -1, 0, 0)
C_MZP = _term("cell3d", -1, 0, 1)
C_MPM = _term("cell3d", -1, 1, -1)
C_MPZ = _term("cell3d", -1, 1, 0)
C_MPP = _term("cell3d", -1, 1, 1)
C_ZMM = _term("cell3d", 0, -1, -1)
C_ZMZ = _term("cell3d", 0, -1, 0)
C_ZMP = _term("cell3d", 0, -1, 1)
C_ZZM = _term("cell3d", 0, 0, -1)
C_ZZZ = _term("cell3d", 0, 0, 0)
C_ZZP = _term("cell3d", 0, 0, 1)
C_ZPM = _term("cell3d", 0, 1, -1)
C_ZPZ = _term("cell3d", 0, 1, 0)
C_ZPP = _term("cell3d", 0, 1, 1)
C_PMM = _term("cell3d", 1, -1, -1)
C_PMZ = _term("cell3d", 1, -1, 0)
C_PMP = _term("cell3d", 1, -1, 1)
C_PZM = _term("cell3d", 1, 0, -1)
C_PZZ = _term("cell3d", 1, 0, 0)
C_PZP = _term("cell3d", 1, 0, 1)
C_PPM = _term("cell3d", 1, 1, -1)
C_PPZ = _term("cell3d", 1, 1, 0)
C_PPP = _term("cell3d", 1, 1, 1)
CUBE_WRITABLE = (
    C_MMM,
    C_MMZ,
    C_MMP,
    C_MZM,
    C_MZZ,
    C_MZP,
    C_MPM,
    C_MPZ,
    C_MPP,
    C_ZMM,
    C_ZMZ,
    C_ZMP,
    C_ZZM,
    C_ZZZ,
    C_ZZP,
    C_ZPM,
    C_ZPZ,
    C_ZPP,
    C_PMM,
    C_PMZ,
    C_PMP,
    C_PZM,
    C_PZZ,
    C_PZP,
    C_PPM,
    C_PPZ,
    C_PPP,
)
CUBE_SOURCE = _term(
    "grid3d",
    _term("topology", "finite-grid", 3, 3, 3),
    _term("default", 0),
    _term(
        "layer",
        _term("row", 1, 1, 1),
        _term("row", 1, 1, 1),
        _term("row", 1, 1, 1),
    ),
    _term(
        "layer",
        _term("row", 1, 1, 1),
        _term("row", 1, 1, 1),
        _term("row", 1, 1, 1),
    ),
    _term(
        "layer",
        _term("row", 1, 1, 1),
        _term("row", 1, 1, 1),
        _term("row", 1, 1, 1),
    ),
)
CUBE_SUCCESSOR = _term(
    "grid3d",
    _term("topology", "finite-grid", 3, 3, 3),
    _term("default", 0),
    _term(
        "layer",
        _term("row", 0, 0, 0),
        _term("row", 0, 1, 0),
        _term("row", 0, 0, 0),
    ),
    _term(
        "layer",
        _term("row", 0, 1, 0),
        _term("row", 1, 1, 1),
        _term("row", 0, 1, 0),
    ),
    _term(
        "layer",
        _term("row", 0, 0, 0),
        _term("row", 0, 1, 0),
        _term("row", 0, 0, 0),
    ),
)
CUBE_ATOM = OracleSourceAtom(
    atom_id="dyadaxes-3d-rule-128",
    kind="derivation",
    witness=_term(
        "lookup-witness",
        "dyadaxes-3d",
        _term("index-multiplicity", _term("index", 7, 7), _term("index", 3, 12), _term("index", 1, 8)),
        _term("rule-id", 128),
    ),
    provenance=(
        "native:dyadaxes_3d",
        "configuration-topology:fixed-zero",
        "rule-128",
    ),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(C_MMM, "replace", 0),
        _disposition(C_MMZ, "replace", 0),
        _disposition(C_MMP, "replace", 0),
        _disposition(C_MZM, "replace", 0),
        _disposition(C_MZZ, "replace", 1),
        _disposition(C_MZP, "replace", 0),
        _disposition(C_MPM, "replace", 0),
        _disposition(C_MPZ, "replace", 0),
        _disposition(C_MPP, "replace", 0),
        _disposition(C_ZMM, "replace", 0),
        _disposition(C_ZMZ, "replace", 1),
        _disposition(C_ZMP, "replace", 0),
        _disposition(C_ZZM, "replace", 1),
        _disposition(C_ZZZ, "replace", 1),
        _disposition(C_ZZP, "replace", 1),
        _disposition(C_ZPM, "replace", 0),
        _disposition(C_ZPZ, "replace", 1),
        _disposition(C_ZPP, "replace", 0),
        _disposition(C_PMM, "replace", 0),
        _disposition(C_PMZ, "replace", 0),
        _disposition(C_PMP, "replace", 0),
        _disposition(C_PZM, "replace", 0),
        _disposition(C_PZZ, "replace", 1),
        _disposition(C_PZP, "replace", 0),
        _disposition(C_PPM, "replace", 0),
        _disposition(C_PPZ, "replace", 0),
        _disposition(C_PPP, "replace", 0),
    ),
    reason=None,
    certificate=_term(
        "lookup-certificate",
        128,
        _term("bit-7-sites", "center-and-six-face-centers"),
    ),
)
CUBE_CASE = OracleCase(
    case_id="native.multidimensional.dyadaxes-3d-rule-128",
    mechanics=("current-multidimensional", "cellular"),
    conformance_refs=("G7-00:current-multidimensional", "CT12"),
    current_native=True,
    source=CUBE_SOURCE,
    writable=CUBE_WRITABLE,
    readable=_term("old-snapshot-3d-stencils", CUBE_SOURCE),
    expected=OracleExpected(
        support_kind="finite",
        source_outcomes=(CUBE_ATOM,),
        applied_atoms=(
            _applied(
                CUBE_ATOM,
                CUBE_SUCCESSOR,
                "native.multidimensional.dyadaxes-3d-rule-128",
            ),
        ),
        no_successor_partition=(),
        outcome_cardinality=EXACT_ONE,
        derivation_cardinality=EXACT_ONE,
        successor_cardinality=EXACT_ONE,
        successor_fibers=(
            OracleFiber(CUBE_SUCCESSOR, ("dyadaxes-3d-rule-128",)),
        ),
        measures=ABSENT_MEASURES,
        source_intensional_relation=None,
        applied_intensional_relation=None,
        successor_intensional_relation=None,
        evidence=_term(
            "application-evidence",
            "native.multidimensional.dyadaxes-3d-rule-128",
        ),
    ),
)


# PX01 mobile automaton: both possible destinations are writable.
TAPE_LEFT = _term("tape-cell", -1)
TAPE_SOURCE = _term("tape-cell", 0)
TAPE_RIGHT = _term("tape-cell", 1)
HEAD_Q1 = _term("head", "q", 1)
HEAD_P0 = _term("head", "p", 0)
MOBILE_SOURCE = _term(
    "tape",
    _term("at", -1, 0),
    _term("at", 0, HEAD_Q1),
    _term("at", 1, 0),
)
MOBILE_LEFT_SUCCESSOR = _term(
    "tape",
    _term("at", -1, HEAD_P0),
    _term("at", 0, 0),
    _term("at", 1, 0),
)
MOBILE_RIGHT_SUCCESSOR = _term(
    "tape",
    _term("at", -1, 0),
    _term("at", 0, 0),
    _term("at", 1, HEAD_P0),
)
MOBILE_LEFT_ATOM = OracleSourceAtom(
    atom_id="mobile-left",
    kind="derivation",
    witness=_term("transition-witness", "q", 1, "p", 0, "left"),
    provenance=("PX01:F031", "transition:left"),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(TAPE_LEFT, "replace", HEAD_P0),
        _disposition(TAPE_SOURCE, "replace", 0),
        _disposition(TAPE_RIGHT, "preserve"),
    ),
    reason=None,
    certificate=_term("single-head-certificate", -1),
)
MOBILE_RIGHT_ATOM = OracleSourceAtom(
    atom_id="mobile-right",
    kind="derivation",
    witness=_term("transition-witness", "q", 1, "p", 0, "right"),
    provenance=("PX01:F031", "transition:right"),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(TAPE_LEFT, "preserve"),
        _disposition(TAPE_SOURCE, "replace", 0),
        _disposition(TAPE_RIGHT, "replace", HEAD_P0),
    ),
    reason=None,
    certificate=_term("single-head-certificate", 1),
)
MOBILE_CASE = OracleCase(
    case_id="px01.mobile-head-branching",
    mechanics=("mobile",),
    conformance_refs=("PX01:F031", "CT12:mobile"),
    current_native=False,
    source=MOBILE_SOURCE,
    writable=(TAPE_LEFT, TAPE_SOURCE, TAPE_RIGHT),
    readable=_term("keyed-old-tape", MOBILE_SOURCE),
    expected=OracleExpected(
        support_kind="finite",
        source_outcomes=(MOBILE_LEFT_ATOM, MOBILE_RIGHT_ATOM),
        applied_atoms=(
            _applied(
                MOBILE_LEFT_ATOM,
                MOBILE_LEFT_SUCCESSOR,
                "px01.mobile-head-branching",
            ),
            _applied(
                MOBILE_RIGHT_ATOM,
                MOBILE_RIGHT_SUCCESSOR,
                "px01.mobile-head-branching",
            ),
        ),
        no_successor_partition=(),
        outcome_cardinality=EXACT_TWO,
        derivation_cardinality=EXACT_TWO,
        successor_cardinality=EXACT_TWO,
        successor_fibers=(
            OracleFiber(MOBILE_LEFT_SUCCESSOR, ("mobile-left",)),
            OracleFiber(MOBILE_RIGHT_SUCCESSOR, ("mobile-right",)),
        ),
        measures=ABSENT_MEASURES,
        source_intensional_relation=None,
        applied_intensional_relation=None,
        successor_intensional_relation=None,
        evidence=_term("application-evidence", "px01.mobile-head-branching"),
    ),
)


# CT12 Turing machine: a deterministic stateful write-and-move transition.
#
# This is deliberately not another label on the mobile fixture above.  Its
# expected record describes a conventional transition keyed by machine state
# and scanned symbol; the runtime test reaches it through the public catalog
# constructor rather than through a test-owned finite Rule.
TURING_HEAD_Q0 = _term("head", "q", 0)
TURING_HEAD_P1 = _term("head", "p", 1)
TURING_SOURCE = _term(
    "tape",
    _term("at", -1, 1),
    _term("at", 0, TURING_HEAD_Q0),
    _term("at", 1, 1),
)
TURING_SUCCESSOR = _term(
    "tape",
    _term("at", -1, TURING_HEAD_P1),
    _term("at", 0, 1),
    _term("at", 1, 1),
)
TURING_ATOM = OracleSourceAtom(
    atom_id="turing-q0-write1-left",
    kind="derivation",
    witness=_term(
        "turing-transition-witness",
        _term("state", "q"),
        _term("scanned", 0),
        _term("next-state", "p"),
        _term("write", 1),
        _term("move", -1),
    ),
    provenance=("mechanics:indexed-replacement",),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(TAPE_LEFT, "replace", TURING_HEAD_P1),
        _disposition(TAPE_SOURCE, "replace", 1),
        _disposition(TAPE_RIGHT, "preserve"),
    ),
    reason=None,
    certificate=_term(
        "turing-transition-certificate",
        "q",
        0,
        "p",
        1,
        -1,
    ),
)
TURING_CASE = OracleCase(
    case_id="px01.turing-stateful-step",
    mechanics=("turing",),
    conformance_refs=("PX01:F031", "CT12:Turing"),
    current_native=False,
    source=TURING_SOURCE,
    writable=(TAPE_LEFT, TAPE_SOURCE, TAPE_RIGHT),
    readable=_term("global-turing-tape", TURING_SOURCE),
    expected=OracleExpected(
        support_kind="finite",
        source_outcomes=(TURING_ATOM,),
        applied_atoms=(
            _applied(
                TURING_ATOM,
                TURING_SUCCESSOR,
                "px01.turing-stateful-step",
            ),
        ),
        no_successor_partition=(),
        outcome_cardinality=EXACT_ONE,
        derivation_cardinality=EXACT_ONE,
        successor_cardinality=EXACT_ONE,
        successor_fibers=(
            OracleFiber(
                TURING_SUCCESSOR,
                ("turing-q0-write1-left",),
            ),
        ),
        measures=ABSENT_MEASURES,
        source_intensional_relation=None,
        applied_intensional_relation=None,
        successor_intensional_relation=None,
        evidence=_term(
            "application-evidence",
            "px01.turing-stateful-step",
        ),
    ),
)


# PX02 parallel substitution: A -> AB and B -> epsilon in one old-snapshot pass.
SUB_OLD_A = _term("occurrence", "old", 0)
SUB_OLD_B = _term("occurrence", "old", 1)
SUB_NEW_A_SLOT = _term("fresh-slot", "offspring", SUB_OLD_A, 0)
SUB_NEW_B_SLOT = _term("fresh-slot", "offspring", SUB_OLD_A, 1)
SUB_NEW_A = _term("fresh-id", "px02.parallel-substitution", "old:0", 0)
SUB_NEW_B = _term("fresh-id", "px02.parallel-substitution", "old:0", 1)
SUB_SOURCE = _term(
    "word",
    _term("symbol", SUB_OLD_A, "A"),
    _term("symbol", SUB_OLD_B, "B"),
)
SUB_SUCCESSOR = _term(
    "word",
    _term("symbol", SUB_NEW_A, "A"),
    _term("symbol", SUB_NEW_B, "B"),
)
SUB_ATOM = OracleSourceAtom(
    atom_id="parallel-substitution",
    kind="derivation",
    witness=_term("generation-witness", "A->AB", "B->epsilon"),
    provenance=("PX02:F038",),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(SUB_OLD_A, "delete"),
        _disposition(SUB_OLD_B, "delete"),
        _disposition(SUB_NEW_A_SLOT, "create", _term("symbol-value", "A")),
        _disposition(SUB_NEW_B_SLOT, "create", _term("symbol-value", "B")),
    ),
    reason=None,
    certificate=_term(
        "ordered-offspring-certificate",
        SUB_NEW_A_SLOT,
        SUB_NEW_B_SLOT,
    ),
)
SUB_FRESH_BINDINGS = (
    OracleFreshBinding(
        local_key=SUB_NEW_A_SLOT,
        identity=SUB_NEW_A,
        evidence=_term(
            "fresh-recipe",
            _term("input-identity", "word:old-generation"),
            _term("rule-identity", "A->AB"),
            _term("witness", "generation-witness"),
            _term("namespace", "px02.parallel-substitution"),
            _term("parent-and-ordinal", SUB_OLD_A, 0),
        ),
    ),
    OracleFreshBinding(
        local_key=SUB_NEW_B_SLOT,
        identity=SUB_NEW_B,
        evidence=_term(
            "fresh-recipe",
            _term("input-identity", "word:old-generation"),
            _term("rule-identity", "A->AB"),
            _term("witness", "generation-witness"),
            _term("namespace", "px02.parallel-substitution"),
            _term("parent-and-ordinal", SUB_OLD_A, 1),
        ),
    ),
)
SUBSTITUTION_CASE = OracleCase(
    case_id="px02.parallel-substitution",
    mechanics=("substitution", "variable-support"),
    conformance_refs=("PX02:F038", "CT12"),
    current_native=False,
    source=SUB_SOURCE,
    writable=(SUB_OLD_A, SUB_OLD_B, SUB_NEW_A_SLOT, SUB_NEW_B_SLOT),
    readable=_term("old-generation-items", SUB_SOURCE),
    expected=OracleExpected(
        support_kind="finite",
        source_outcomes=(SUB_ATOM,),
        applied_atoms=(
            _applied(
                SUB_ATOM,
                SUB_SUCCESSOR,
                "px02.parallel-substitution",
                fresh_bindings=SUB_FRESH_BINDINGS,
            ),
        ),
        no_successor_partition=(),
        outcome_cardinality=EXACT_ONE,
        derivation_cardinality=EXACT_ONE,
        successor_cardinality=EXACT_ONE,
        successor_fibers=(OracleFiber(SUB_SUCCESSOR, ("parallel-substitution",)),),
        measures=ABSENT_MEASURES,
        source_intensional_relation=None,
        applied_intensional_relation=None,
        successor_intensional_relation=None,
        evidence=_term("application-evidence", "px02.parallel-substitution"),
    ),
)


# PX04 multiway diamond: two witnessed rewrites quotient to one successor.
MW_TARGET = _term("word-occurrence", 0)
MW_SOURCE = _term("word", _term("symbol", MW_TARGET, "a"))
MW_SUCCESSOR = _term("word", _term("symbol", MW_TARGET, "b"))
MW_ATOM_LEFT = OracleSourceAtom(
    atom_id="diamond-rule-left",
    kind="derivation",
    witness=_term("rewrite-witness", "rule-left", "match:0", "parent:a"),
    provenance=("PX04:F034", "rule:left"),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(_disposition(MW_TARGET, "replace", _term("symbol-value", "b")),),
    reason=None,
    certificate=_term("rewrite-certificate", "a->b", "left"),
)
MW_ATOM_RIGHT = OracleSourceAtom(
    atom_id="diamond-rule-right",
    kind="derivation",
    witness=_term("rewrite-witness", "rule-right", "match:0", "parent:a"),
    provenance=("PX04:F034", "rule:right"),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(_disposition(MW_TARGET, "replace", _term("symbol-value", "b")),),
    reason=None,
    certificate=_term("rewrite-certificate", "a->b", "right"),
)
MULTIWAY_CASE = OracleCase(
    case_id="px04.multiway-diamond",
    mechanics=("multiway",),
    conformance_refs=("PX04:F034", "CT08", "CT12"),
    current_native=False,
    source=MW_SOURCE,
    writable=(MW_TARGET,),
    readable=_term("all-matches", MW_SOURCE),
    expected=OracleExpected(
        support_kind="finite",
        source_outcomes=(MW_ATOM_LEFT, MW_ATOM_RIGHT),
        applied_atoms=(
            _applied(
                MW_ATOM_LEFT,
                MW_SUCCESSOR,
                "px04.multiway-diamond",
            ),
            _applied(
                MW_ATOM_RIGHT,
                MW_SUCCESSOR,
                "px04.multiway-diamond",
            ),
        ),
        no_successor_partition=(),
        outcome_cardinality=EXACT_TWO,
        derivation_cardinality=EXACT_TWO,
        successor_cardinality=EXACT_ONE,
        successor_fibers=(
            OracleFiber(
                MW_SUCCESSOR,
                ("diamond-rule-left", "diamond-rule-right"),
            ),
        ),
        measures=ABSENT_MEASURES,
        source_intensional_relation=None,
        applied_intensional_relation=None,
        successor_intensional_relation=None,
        evidence=_term("application-evidence", "px04.multiway-diamond"),
    ),
)


# PX04 constraint family: x^2 = rhs over Z/3Z gives exact zero, one, or two.
CONSTRAINT_X = _term("unknown", "x")


def _constraint_source(rhs: int) -> OracleTerm:
    return _term(
        "constraint-state",
        _term("domain", "Z/3Z"),
        _term("equation", "x^2=rhs"),
        _term("rhs", rhs),
        _term("slot", "x", "unset"),
    )


CONSTRAINT_ZERO_ATOM = OracleSourceAtom(
    atom_id="constraint-no-solution",
    kind="no-successor",
    witness=_term("relation-witness", "x^2=2", "Z/3Z"),
    provenance=("PX04:F019", "rhs=2"),
    progress=None,
    continuation=None,
    dispositions=(),
    reason=_term("terminal", "no-solution"),
    certificate=_term(
        "truth-table",
        _term("row", 0, _term("square-residue", 0), False),
        _term("row", 1, _term("square-residue", 1), False),
        _term("row", 2, _term("square-residue", 1), False),
    ),
)
CONSTRAINT_ZERO_APPLIED = _applied(
    CONSTRAINT_ZERO_ATOM,
    None,
    "px04.constraint-mod3-zero",
)
CONSTRAINT_ZERO_CASE = OracleCase(
    case_id="px04.constraint-mod3-zero",
    mechanics=("constraint",),
    conformance_refs=("PX04:F019", "CT05", "CT12"),
    current_native=False,
    source=_constraint_source(2),
    writable=(CONSTRAINT_X,),
    readable=_term("constraint-view", "x^2=2", "Z/3Z"),
    expected=OracleExpected(
        support_kind="finite",
        source_outcomes=(CONSTRAINT_ZERO_ATOM,),
        applied_atoms=(CONSTRAINT_ZERO_APPLIED,),
        no_successor_partition=(CONSTRAINT_ZERO_APPLIED,),
        outcome_cardinality=EXACT_ONE,
        derivation_cardinality=EXACT_ZERO,
        successor_cardinality=EXACT_ZERO,
        successor_fibers=(),
        measures=ABSENT_MEASURES,
        source_intensional_relation=None,
        applied_intensional_relation=None,
        successor_intensional_relation=None,
        evidence=_term("application-evidence", "px04.constraint-mod3-zero"),
    ),
)

CONSTRAINT_ONE_SUCCESSOR = _term("assignment", _term("value", "x", 0))
CONSTRAINT_ONE_ATOM = OracleSourceAtom(
    atom_id="constraint-x-0",
    kind="derivation",
    witness=_term("solution-witness", "x", 0),
    provenance=("PX04:F019", "rhs=0"),
    progress="advanced",
    continuation=_term("stop", "completed"),
    dispositions=(_disposition(CONSTRAINT_X, "replace", 0),),
    reason=None,
    certificate=_term("equation-certificate", "0^2=0 mod 3"),
)
CONSTRAINT_ONE_CASE = OracleCase(
    case_id="px04.constraint-mod3-one",
    mechanics=("constraint",),
    conformance_refs=("PX04:F019", "CT05", "CT12"),
    current_native=False,
    source=_constraint_source(0),
    writable=(CONSTRAINT_X,),
    readable=_term("constraint-view", "x^2=0", "Z/3Z"),
    expected=OracleExpected(
        support_kind="finite",
        source_outcomes=(CONSTRAINT_ONE_ATOM,),
        applied_atoms=(
            _applied(
                CONSTRAINT_ONE_ATOM,
                CONSTRAINT_ONE_SUCCESSOR,
                "px04.constraint-mod3-one",
            ),
        ),
        no_successor_partition=(),
        outcome_cardinality=EXACT_ONE,
        derivation_cardinality=EXACT_ONE,
        successor_cardinality=EXACT_ONE,
        successor_fibers=(
            OracleFiber(CONSTRAINT_ONE_SUCCESSOR, ("constraint-x-0",)),
        ),
        measures=ABSENT_MEASURES,
        source_intensional_relation=None,
        applied_intensional_relation=None,
        successor_intensional_relation=None,
        evidence=_term("application-evidence", "px04.constraint-mod3-one"),
    ),
)

CONSTRAINT_X1_SUCCESSOR = _term("assignment", _term("value", "x", 1))
CONSTRAINT_X2_SUCCESSOR = _term("assignment", _term("value", "x", 2))
CONSTRAINT_X1_ATOM = OracleSourceAtom(
    atom_id="constraint-x-1",
    kind="derivation",
    witness=_term("solution-witness", "x", 1),
    provenance=("PX04:F019", "rhs=1"),
    progress="advanced",
    continuation=_term("stop", "completed"),
    dispositions=(_disposition(CONSTRAINT_X, "replace", 1),),
    reason=None,
    certificate=_term("equation-certificate", "1^2=1 mod 3"),
)
CONSTRAINT_X2_ATOM = OracleSourceAtom(
    atom_id="constraint-x-2",
    kind="derivation",
    witness=_term("solution-witness", "x", 2),
    provenance=("PX04:F019", "rhs=1"),
    progress="advanced",
    continuation=_term("stop", "completed"),
    dispositions=(_disposition(CONSTRAINT_X, "replace", 2),),
    reason=None,
    certificate=_term("equation-certificate", "2^2=1 mod 3"),
)
CONSTRAINT_MANY_CASE = OracleCase(
    case_id="px04.constraint-mod3-many",
    mechanics=("constraint",),
    conformance_refs=("PX04:F019", "CT05", "CT12"),
    current_native=False,
    source=_constraint_source(1),
    writable=(CONSTRAINT_X,),
    readable=_term("constraint-view", "x^2=1", "Z/3Z"),
    expected=OracleExpected(
        support_kind="finite",
        source_outcomes=(CONSTRAINT_X1_ATOM, CONSTRAINT_X2_ATOM),
        applied_atoms=(
            _applied(
                CONSTRAINT_X1_ATOM,
                CONSTRAINT_X1_SUCCESSOR,
                "px04.constraint-mod3-many",
            ),
            _applied(
                CONSTRAINT_X2_ATOM,
                CONSTRAINT_X2_SUCCESSOR,
                "px04.constraint-mod3-many",
            ),
        ),
        no_successor_partition=(),
        outcome_cardinality=EXACT_TWO,
        derivation_cardinality=EXACT_TWO,
        successor_cardinality=EXACT_TWO,
        successor_fibers=(
            OracleFiber(CONSTRAINT_X1_SUCCESSOR, ("constraint-x-1",)),
            OracleFiber(CONSTRAINT_X2_SUCCESSOR, ("constraint-x-2",)),
        ),
        measures=ABSENT_MEASURES,
        source_intensional_relation=None,
        applied_intensional_relation=None,
        successor_intensional_relation=None,
        evidence=_term("application-evidence", "px04.constraint-mod3-many"),
    ),
)


# PX02 graph replacement freezes deletion, interfaces, and fresh identities.
GRAPH_B = _term("node", "b")
GRAPH_AB = _term("edge", "a", "b")
GRAPH_BC = _term("edge", "b", "c")
GRAPH_X_SLOT = _term("fresh-slot", "node", "x")
GRAPH_Y_SLOT = _term("fresh-slot", "node", "y")
GRAPH_AX_SLOT = _term("fresh-slot", "edge", "a-x")
GRAPH_XY_SLOT = _term("fresh-slot", "edge", "x-y")
GRAPH_YC_SLOT = _term("fresh-slot", "edge", "y-c")
GRAPH_X = _term("fresh-id", "px02.graph-interface-replacement", "b", "x")
GRAPH_Y = _term("fresh-id", "px02.graph-interface-replacement", "b", "y")
GRAPH_AX = _term("fresh-id", "px02.graph-interface-replacement", "b", "a-x")
GRAPH_XY = _term("fresh-id", "px02.graph-interface-replacement", "b", "x-y")
GRAPH_YC = _term("fresh-id", "px02.graph-interface-replacement", "b", "y-c")
GRAPH_SOURCE = _term(
    "graph",
    _term("nodes", "a", "b", "c"),
    _term("edges", _term("edge", "a", "b"), _term("edge", "b", "c")),
)
GRAPH_SUCCESSOR = _term(
    "graph",
    _term("nodes", "a", GRAPH_X, GRAPH_Y, "c"),
    _term(
        "edges",
        _term("edge-record", GRAPH_AX, "a", GRAPH_X),
        _term("edge-record", GRAPH_XY, GRAPH_X, GRAPH_Y),
        _term("edge-record", GRAPH_YC, GRAPH_Y, "c"),
    ),
)
GRAPH_ATOM = OracleSourceAtom(
    atom_id="graph-replacement",
    kind="derivation",
    witness=_term("match", _term("node", "b"), _term("ports", "a", "c")),
    provenance=("PX02:F029",),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(GRAPH_B, "delete"),
        _disposition(GRAPH_AB, "delete"),
        _disposition(GRAPH_BC, "delete"),
        _disposition(GRAPH_X_SLOT, "create", _term("node-value", "x")),
        _disposition(GRAPH_Y_SLOT, "create", _term("node-value", "y")),
        _disposition(
            GRAPH_AX_SLOT,
            "create",
            _term(
                "edge-value",
                _term("existing-ref", "a"),
                _term("fresh-ref", GRAPH_X_SLOT),
            ),
        ),
        _disposition(
            GRAPH_XY_SLOT,
            "create",
            _term(
                "edge-value",
                _term("fresh-ref", GRAPH_X_SLOT),
                _term("fresh-ref", GRAPH_Y_SLOT),
            ),
        ),
        _disposition(
            GRAPH_YC_SLOT,
            "create",
            _term(
                "edge-value",
                _term("fresh-ref", GRAPH_Y_SLOT),
                _term("existing-ref", "c"),
            ),
        ),
    ),
    reason=None,
    certificate=_term(
        "interface-certificate",
        _term("external", "a", "c"),
        _term(
            "authorized-fresh-slots",
            GRAPH_X_SLOT,
            GRAPH_Y_SLOT,
            GRAPH_AX_SLOT,
            GRAPH_XY_SLOT,
            GRAPH_YC_SLOT,
        ),
    ),
)
GRAPH_FRESH_BINDINGS = (
    OracleFreshBinding(
        GRAPH_X_SLOT,
        GRAPH_X,
        _term(
            "fresh-recipe",
            _term("input-identity", "graph:a-b-c"),
            _term("rule-identity", "F029"),
            _term("match-witness", "node:b"),
            _term("interface", "a", "c"),
            _term("namespace", "px02.graph-interface-replacement"),
            _term("local-key", "x"),
        ),
    ),
    OracleFreshBinding(
        GRAPH_Y_SLOT,
        GRAPH_Y,
        _term(
            "fresh-recipe",
            _term("input-identity", "graph:a-b-c"),
            _term("rule-identity", "F029"),
            _term("match-witness", "node:b"),
            _term("interface", "a", "c"),
            _term("namespace", "px02.graph-interface-replacement"),
            _term("local-key", "y"),
        ),
    ),
    OracleFreshBinding(
        GRAPH_AX_SLOT,
        GRAPH_AX,
        _term(
            "fresh-recipe",
            _term("input-identity", "graph:a-b-c"),
            _term("rule-identity", "F029"),
            _term("match-witness", "node:b"),
            _term("interface", "a", "c"),
            _term("namespace", "px02.graph-interface-replacement"),
            _term("local-key", "a-x"),
        ),
    ),
    OracleFreshBinding(
        GRAPH_XY_SLOT,
        GRAPH_XY,
        _term(
            "fresh-recipe",
            _term("input-identity", "graph:a-b-c"),
            _term("rule-identity", "F029"),
            _term("match-witness", "node:b"),
            _term("interface", "a", "c"),
            _term("namespace", "px02.graph-interface-replacement"),
            _term("local-key", "x-y"),
        ),
    ),
    OracleFreshBinding(
        GRAPH_YC_SLOT,
        GRAPH_YC,
        _term(
            "fresh-recipe",
            _term("input-identity", "graph:a-b-c"),
            _term("rule-identity", "F029"),
            _term("match-witness", "node:b"),
            _term("interface", "a", "c"),
            _term("namespace", "px02.graph-interface-replacement"),
            _term("local-key", "y-c"),
        ),
    ),
)
GRAPH_CASE = OracleCase(
    case_id="px02.graph-interface-replacement",
    mechanics=("variable-support",),
    conformance_refs=("PX02:F029", "CT07", "CT12"),
    current_native=False,
    source=GRAPH_SOURCE,
    writable=(
        GRAPH_B,
        GRAPH_AB,
        GRAPH_BC,
        GRAPH_X_SLOT,
        GRAPH_Y_SLOT,
        GRAPH_AX_SLOT,
        GRAPH_XY_SLOT,
        GRAPH_YC_SLOT,
    ),
    readable=_term(
        "matched-interface-view",
        GRAPH_SOURCE,
        _term("external-ports", "a", "c"),
    ),
    expected=OracleExpected(
        support_kind="finite",
        source_outcomes=(GRAPH_ATOM,),
        applied_atoms=(
            _applied(
                GRAPH_ATOM,
                GRAPH_SUCCESSOR,
                "px02.graph-interface-replacement",
                fresh_bindings=GRAPH_FRESH_BINDINGS,
            ),
        ),
        no_successor_partition=(),
        outcome_cardinality=EXACT_ONE,
        derivation_cardinality=EXACT_ONE,
        successor_cardinality=EXACT_ONE,
        successor_fibers=(OracleFiber(GRAPH_SUCCESSOR, ("graph-replacement",)),),
        measures=ABSENT_MEASURES,
        source_intensional_relation=None,
        applied_intensional_relation=None,
        successor_intensional_relation=None,
        evidence=_term(
            "application-evidence",
            "px02.graph-interface-replacement",
        ),
    ),
)


# PX06 stochastic law: two successors and one no-successor atom.
SEARCH_X = _term("field", "x")
SEARCH_K = _term("field", "k")
SEARCH_SOURCE = _term(
    "configuration.record",
    _term("field-value", "x", 0),
    _term("field-value", "k", 0),
)
SEARCH_ACCEPT_SUCCESSOR = _term(
    "configuration.record",
    _term("field-value", "x", 1),
    _term("field-value", "k", 1),
)
SEARCH_REJECT_SUCCESSOR = _term(
    "configuration.record",
    _term("field-value", "x", 0),
    _term("field-value", "k", 1),
)
SEARCH_ACCEPT_ATOM = OracleSourceAtom(
    atom_id="search-accept",
    kind="derivation",
    witness=_term("proposal-witness", 1, "accepted"),
    provenance=("PX06:F050",),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(SEARCH_X, "replace", 1),
        _disposition(SEARCH_K, "replace", 1),
    ),
    reason=None,
    certificate=_term("law-atom-certificate", "accept", Fraction(1, 2)),
    mass=Fraction(1, 2),
)
SEARCH_REJECT_ATOM = OracleSourceAtom(
    atom_id="search-reject",
    kind="derivation",
    witness=_term("proposal-witness", 0, "rejected"),
    provenance=("PX06:F050",),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(SEARCH_X, "preserve"),
        _disposition(SEARCH_K, "replace", 1),
    ),
    reason=None,
    certificate=_term("law-atom-certificate", "reject", Fraction(1, 4)),
    mass=Fraction(1, 4),
)
SEARCH_NONE_ATOM = OracleSourceAtom(
    atom_id="search-no-proposal",
    kind="no-successor",
    witness=_term("proposal-witness", "none"),
    provenance=("PX06:F050",),
    progress=None,
    continuation=None,
    dispositions=(),
    reason=_term("terminal", "no-proposal"),
    certificate=_term("law-atom-certificate", "no-proposal", Fraction(1, 4)),
    mass=Fraction(1, 4),
)
SEARCH_ACCEPT_APPLIED = _applied(
    SEARCH_ACCEPT_ATOM,
    SEARCH_ACCEPT_SUCCESSOR,
    "px06.stochastic-search-law",
)
SEARCH_REJECT_APPLIED = _applied(
    SEARCH_REJECT_ATOM,
    SEARCH_REJECT_SUCCESSOR,
    "px06.stochastic-search-law",
)
SEARCH_NONE_APPLIED = _applied(
    SEARCH_NONE_ATOM,
    None,
    "px06.stochastic-search-law",
)
STOCHASTIC_CASE = OracleCase(
    case_id="px06.stochastic-search-law",
    mechanics=("stochastic",),
    conformance_refs=("PX06:F050", "CT06", "CT12"),
    current_native=False,
    source=SEARCH_SOURCE,
    writable=(SEARCH_X, SEARCH_K),
    readable=_term(
        "search-view",
        SEARCH_SOURCE,
        _term("objective", "(x-1)^2"),
        _term("proposal-law", "closed"),
    ),
    expected=OracleExpected(
        support_kind="finite",
        source_outcomes=(
            SEARCH_ACCEPT_ATOM,
            SEARCH_REJECT_ATOM,
            SEARCH_NONE_ATOM,
        ),
        applied_atoms=(
            SEARCH_ACCEPT_APPLIED,
            SEARCH_REJECT_APPLIED,
            SEARCH_NONE_APPLIED,
        ),
        no_successor_partition=(SEARCH_NONE_APPLIED,),
        outcome_cardinality=EXACT_THREE,
        derivation_cardinality=EXACT_TWO,
        successor_cardinality=EXACT_TWO,
        successor_fibers=(
            OracleFiber(SEARCH_ACCEPT_SUCCESSOR, ("search-accept",)),
            OracleFiber(SEARCH_REJECT_SUCCESSOR, ("search-reject",)),
        ),
        measures=OracleMeasures(
            applied_atoms=OracleMeasureView(
                kind="available",
                masses=(
                    ("search-accept", Fraction(1, 2)),
                    ("search-reject", Fraction(1, 4)),
                    ("search-no-proposal", Fraction(1, 4)),
                ),
                total_mass=Fraction(1, 1),
                evidence=_term("law-evidence", "closed-three-atom-law"),
            ),
            successors=OracleMeasureView(
                kind="available",
                masses=(
                    (SEARCH_ACCEPT_SUCCESSOR, Fraction(1, 2)),
                    (SEARCH_REJECT_SUCCESSOR, Fraction(1, 4)),
                ),
                total_mass=Fraction(3, 4),
                evidence=_term("pushforward-evidence", "derivation-atoms-only"),
            ),
            no_successors=OracleMeasureView(
                kind="available",
                masses=(("search-no-proposal", Fraction(1, 4)),),
                total_mass=Fraction(1, 4),
                evidence=_term("restriction-evidence", "no-successor-atoms-only"),
            ),
        ),
        source_intensional_relation=None,
        applied_intensional_relation=None,
        successor_intensional_relation=None,
        evidence=_term("application-evidence", "px06.stochastic-search-law"),
    ),
)


# PX05 exact differential flow: the closed maximal solution of dx/dt=1.
FLOW_SOLUTION_SLOT = _term("solution-slot", "x")
FLOW_SOURCE = _term(
    "differential-state",
    _term("equation", _term("derivative", "x", "t"), 1),
    _term("initial-condition", _term("x-at", 0), 0),
    _term("solution", "unset"),
)
FLOW_SUCCESSOR = _term(
    "differential-state",
    _term("equation", _term("derivative", "x", "t"), 1),
    _term("initial-condition", _term("x-at", 0), 0),
    _term(
        "solution",
        _term(
            "maximal-solution",
            _term("binder", "t", "exact-real"),
            _term("equals", _term("x-of", "t"), "t"),
        ),
    ),
)
FLOW_ATOM = OracleSourceAtom(
    atom_id="exact-flow-x-equals-t",
    kind="derivation",
    witness=_term(
        "differential-proof",
        _term("derivative-of", "t", "t", 1),
        _term("initial-value", 0, 0),
        _term("coverage", "maximal-exact-real-solution"),
    ),
    provenance=("PX05:F037",),
    progress="advanced",
    continuation=_term("stop", "completed"),
    dispositions=(
        _disposition(
            FLOW_SOLUTION_SLOT,
            "replace",
            _term(
                "maximal-solution",
                _term("binder", "t", "exact-real"),
                _term("equals", _term("x-of", "t"), "t"),
            ),
        ),
    ),
    reason=None,
    certificate=_term("equation-and-initial-condition-certificate", "exact"),
)
FLOW_CASE = OracleCase(
    case_id="px05.exact-differential-flow",
    mechanics=("differential",),
    conformance_refs=("PX05:F037", "CT12"),
    current_native=False,
    source=FLOW_SOURCE,
    writable=(FLOW_SOLUTION_SLOT,),
    readable=_term(
        "differential-view",
        _term("equation", _term("derivative", "x", "t"), 1),
        _term("initial-condition", _term("x-at", 0), 0),
        _term("duration-or-event-selector", "none"),
    ),
    expected=OracleExpected(
        support_kind="finite",
        source_outcomes=(FLOW_ATOM,),
        applied_atoms=(
            _applied(
                FLOW_ATOM,
                FLOW_SUCCESSOR,
                "px05.exact-differential-flow",
            ),
        ),
        no_successor_partition=(),
        outcome_cardinality=EXACT_ONE,
        derivation_cardinality=EXACT_ONE,
        successor_cardinality=EXACT_ONE,
        successor_fibers=(
            OracleFiber(FLOW_SUCCESSOR, ("exact-flow-x-equals-t",)),
        ),
        measures=ABSENT_MEASURES,
        source_intensional_relation=None,
        applied_intensional_relation=None,
        successor_intensional_relation=None,
        evidence=_term("application-evidence", "px05.exact-differential-flow"),
    ),
)


# PX04/PX05 intensional differential relation: every exact constant field.
FIELD_U = _term("field-capability", "u")
DIFFERENTIAL_SOURCE_RELATION = _term(
    "intensional-source-outcome-relation",
    _term("binder", "c"),
    _term("domain", "exact-real"),
    _term(
        "source-derivation-template",
        _term("atom-id", _term("parameterized", "constant-field", "c")),
        _term(
            "total-disposition",
            _term("replace", FIELD_U, _term("constant-field", "c")),
        ),
        _term("witness", _term("derivative", "u", "x"), 0),
        _term("stop", "completed"),
    ),
)
DIFFERENTIAL_APPLIED_RELATION = _term(
    "intensional-applied-atom-relation",
    _term("binder", "c"),
    _term("domain", "exact-real"),
    _term(
        "applied-derivation-template",
        _term("source-atom-id", _term("parameterized", "constant-field", "c")),
        _term(
            "successor",
            _term(
                "field-state",
                _term("domain", _term("closed-interval", 0, 1)),
                _term("field", "u", _term("constant-field", "c")),
            ),
        ),
        _term("fresh-bindings", "empty"),
        _term("output-lineage", "px05.constant-field-intensional", "c"),
        _term("application-evidence", "exact-differential-proof", "c"),
    ),
)
DIFFERENTIAL_SUCCESSOR_RELATION = _term(
    "intensional-successor-quotient-relation",
    _term("binder", "c"),
    _term("domain", "exact-real"),
    _term(
        "successor-group-template",
        _term(
            "field-state",
            _term("domain", _term("closed-interval", 0, 1)),
            _term("field", "u", _term("constant-field", "c")),
        ),
        _term(
            "derivation-fiber",
            _term("applied-atom-id", _term("parameterized", "constant-field", "c")),
        ),
    ),
)
DIFFERENTIAL_CASE = OracleCase(
    case_id="px05.constant-field-intensional",
    mechanics=("intensional",),
    conformance_refs=("PX04:F041", "PX05:F041", "CT12"),
    current_native=False,
    source=_term(
        "field-state",
        _term("domain", _term("closed-interval", 0, 1)),
        _term("field", "u", "unknown"),
    ),
    writable=(FIELD_U,),
    readable=_term(
        "differential-view",
        _term("domain", _term("closed-interval", 0, 1)),
        _term("germ", _term("derivative", "u", "x")),
        _term("side-data", "none"),
    ),
    expected=OracleExpected(
        support_kind="intensional",
        source_outcomes=(),
        applied_atoms=(),
        no_successor_partition=(),
        outcome_cardinality=UNCOUNTABLE,
        derivation_cardinality=UNCOUNTABLE,
        successor_cardinality=UNCOUNTABLE,
        successor_fibers=(),
        measures=ABSENT_MEASURES,
        source_intensional_relation=DIFFERENTIAL_SOURCE_RELATION,
        applied_intensional_relation=DIFFERENTIAL_APPLIED_RELATION,
        successor_intensional_relation=DIFFERENTIAL_SUCCESSOR_RELATION,
        evidence=_term(
            "application-evidence",
            "px05.constant-field-intensional",
            _term("coverage", "all-exact-real-c"),
        ),
    ),
)


CT12_CASES = (
    AR2_CASE,
    DYADLAGS_CASE,
    LAGCOUNTS_CASE,
    LINE_CASE,
    GRID_CASE,
    CUBE_CASE,
    MOBILE_CASE,
    SUBSTITUTION_CASE,
    MULTIWAY_CASE,
    CONSTRAINT_ZERO_CASE,
    CONSTRAINT_ONE_CASE,
    CONSTRAINT_MANY_CASE,
    GRAPH_CASE,
    STOCHASTIC_CASE,
    FLOW_CASE,
    DIFFERENTIAL_CASE,
    TURING_CASE,
)

EXPECTED_CT12_CASE_IDS = (
    "native.scalar.ar2-modular",
    "native.temporal.dyadlags-rule-150",
    "native.temporal.lagcounts-rule-91",
    "native.cellular.dyadrads-rule-30",
    "native.multidimensional.dyadaxes-2d-rule-128",
    "native.multidimensional.dyadaxes-3d-rule-128",
    "px01.mobile-head-branching",
    "px02.parallel-substitution",
    "px04.multiway-diamond",
    "px04.constraint-mod3-zero",
    "px04.constraint-mod3-one",
    "px04.constraint-mod3-many",
    "px02.graph-interface-replacement",
    "px06.stochastic-search-law",
    "px05.exact-differential-flow",
    "px05.constant-field-intensional",
    "px01.turing-stateful-step",
)

REQUIRED_CT12_MECHANICS = (
    "current-scalar",
    "current-temporal",
    "current-cellular",
    "current-multidimensional",
    "cellular",
    "mobile",
    "turing",
    "substitution",
    "multiway",
    "constraint",
    "variable-support",
    "stochastic",
    "differential",
    "intensional",
)


def _assert_term_is_closed(term: OracleTerm) -> None:
    assert term.tag
    for argument in term.arguments:
        if isinstance(argument, OracleTerm):
            _assert_term_is_closed(argument)
        else:
            assert isinstance(argument, (bool, int, Fraction, str)) or argument is None
            assert not isinstance(argument, float)


def _term_contains_tag(term: OracleTerm, tag: str) -> bool:
    return term.tag == tag or any(
        _term_contains_tag(argument, tag)
        for argument in term.arguments
        if isinstance(argument, OracleTerm)
    )


def test_pre_cutover_snapshot_is_exact_and_complete() -> None:
    assert PRE_CUTOVER.goal6_close_commit == (
        "60bde6da318f415e43e14fc98b5faa28f14cd945"
    )
    assert PRE_CUTOVER.preimplementation_shell_commit == (
        "1562041e4dab0a6d9e51d730222de0a4f1b52038"
    )
    assert PRE_CUTOVER.execution_start_commit == (
        "95ba134ee8f9671181c237cd2975004f3442efbe"
    )
    assert len(PRE_CUTOVER.root_exports) == 67
    assert len(set(PRE_CUTOVER.root_exports)) == 67
    assert PRE_CUTOVER.public_manifest_sha256 == (
        "fe4f136f50cf1471268278b5f62a33492bad090808605a9a3f7c048aed81a4f2"
    )
    assert PRE_CUTOVER.eager_imports == (
        "ca.specs",
        "ca.rollout",
        "ca.datasets",
        "ca.rng",
        "ca.viz",
    )
    assert PRE_CUTOVER.physical_modules_to_remove == ("ca.rollout", "ca.specs")
    assert len(PRE_CUTOVER.obsolete_execution_sites) == 5
    assert len(PRE_CUTOVER.frozen_git_blobs) == 7
    assert len(PRE_CUTOVER.frozen_sha256) == 5
    assert set(PRE_CUTOVER.target_root_exports) == {
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
        "serialization",
        "catalog",
    }
    assert set(PRE_CUTOVER.target_root_exports) - set(PRE_CUTOVER.root_exports) == {
        "SimpleProgram",
        "apply",
        "program",
        "serialization",
        "catalog",
    }
    assert PRE_CUTOVER.active_test_baseline == "102 passed, 96 skipped"


def test_oracle_source_has_no_runtime_semantic_dependency() -> None:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    allowed_import_roots = {
        "__future__",
        "ast",
        "dataclasses",
        "fractions",
        "pathlib",
        "typing",
    }
    forbidden_call_names = {
        "__import__",
        "apply",
        "apply_rule",
        "compile",
        "commit",
        "denote",
        "eval",
        "evaluate",
        "exec",
        "getattr",
        "globals",
        "import_module",
        "instantiate",
        "locals",
        "reference_step",
        "rollout",
        "solve",
        "solver",
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] in allowed_import_roots
        elif isinstance(node, ast.ImportFrom):
            assert node.level == 0
            assert node.module is not None
            assert node.module.split(".", 1)[0] in allowed_import_roots
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                assert node.func.id not in forbidden_call_names
            elif isinstance(node.func, ast.Attribute):
                assert node.func.attr not in forbidden_call_names


def test_runtime_source_has_no_dependency_on_test_oracles() -> None:
    repository = Path(__file__).resolve().parents[2]
    for path in (repository / "src" / "ca").rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "test_oracles" not in source
        assert "tests.conformance" not in source
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                assert all(
                    alias.name.split(".", 1)[0] != "tests" for alias in node.names
                )
            elif isinstance(node, ast.ImportFrom):
                assert node.module is None or node.module.split(".", 1)[0] != "tests"


def _assert_fixture_data_contains_no_callables(value: Any) -> None:
    if is_dataclass(value) and not isinstance(value, type):
        for item in fields(value):
            _assert_fixture_data_contains_no_callables(value.__dict__[item.name])
        return
    if isinstance(value, tuple):
        for item in value:
            _assert_fixture_data_contains_no_callables(item)
        return
    assert not callable(value)


def test_frozen_fixture_values_contain_no_callbacks_or_evaluators() -> None:
    _assert_fixture_data_contains_no_callables(PRE_CUTOVER)
    _assert_fixture_data_contains_no_callables(CT12_CASES)


def test_oracle_inventory_covers_every_minimum_ct12_mechanic() -> None:
    covered = {mechanic for case in CT12_CASES for mechanic in case.mechanics}
    assert covered >= set(REQUIRED_CT12_MECHANICS)
    assert tuple(case.case_id for case in CT12_CASES) == EXPECTED_CT12_CASE_IDS
    assert len(CT12_CASES) == 17
    assert all(case.current_native for case in CT12_CASES[:6])
    assert not any(case.current_native for case in CT12_CASES[6:])


def test_oracle_case_ids_and_closed_terms_are_exact() -> None:
    case_ids = [case.case_id for case in CT12_CASES]
    assert len(case_ids) == len(set(case_ids))

    for case in CT12_CASES:
        assert case.conformance_refs
        assert case.writable
        assert len(case.writable) == len(set(case.writable))
        _assert_term_is_closed(case.source)
        _assert_term_is_closed(case.readable)
        _assert_term_is_closed(case.expected.evidence)
        for target in case.writable:
            _assert_term_is_closed(target)


def test_finite_oracles_have_total_dispositions_cardinalities_and_fibers() -> None:
    for case in CT12_CASES:
        expected = case.expected
        if expected.support_kind != "finite":
            continue

        assert expected.source_intensional_relation is None
        assert expected.applied_intensional_relation is None
        assert expected.successor_intensional_relation is None
        assert expected.outcome_cardinality == OracleCardinality(
            "exact",
            len(expected.source_outcomes),
        )

        source_by_id = {
            atom.atom_id: atom for atom in expected.source_outcomes
        }
        assert len(source_by_id) == len(expected.source_outcomes)
        applied_by_id = {
            atom.atom_id: atom for atom in expected.applied_atoms
        }
        assert len(applied_by_id) == len(expected.applied_atoms)
        assert set(applied_by_id) == set(source_by_id)
        assert all(
            atom.source_atom_id in source_by_id
            for atom in expected.applied_atoms
        )

        source_derivations = [
            atom
            for atom in expected.source_outcomes
            if atom.kind == "derivation"
        ]
        source_no_successors = [
            atom
            for atom in expected.source_outcomes
            if atom.kind == "no-successor"
        ]
        applied_derivations = [
            atom
            for atom in expected.applied_atoms
            if source_by_id[atom.source_atom_id].kind == "derivation"
        ]
        applied_no_successors = [
            atom
            for atom in expected.applied_atoms
            if source_by_id[atom.source_atom_id].kind == "no-successor"
        ]
        assert expected.no_successor_partition == tuple(
            applied_no_successors
        )
        successors = {atom.successor for atom in applied_derivations}
        assert None not in successors
        assert expected.derivation_cardinality == OracleCardinality(
            "exact",
            len(applied_derivations),
        )
        assert expected.successor_cardinality == OracleCardinality(
            "exact",
            len(successors),
        )

        fiber_atom_ids: list[str] = []
        for fiber in expected.successor_fibers:
            assert fiber.successor in successors
            fiber_atom_ids.extend(fiber.atom_ids)
        assert sorted(fiber_atom_ids) == sorted(
            atom.atom_id for atom in applied_derivations
        )

        for atom in source_derivations:
            assert atom.progress is not None
            assert atom.continuation is not None
            assert atom.reason is None
            assert set(disposition.target for disposition in atom.dispositions) == set(
                case.writable
            )
            assert len(atom.dispositions) == len(case.writable)
            assert len({item.target for item in atom.dispositions}) == len(
                atom.dispositions
            )
            for item in atom.dispositions:
                if item.action in {"replace", "create"}:
                    assert item.value is not None
                else:
                    assert item.value is None

        for atom in source_no_successors:
            assert atom.progress is None
            assert atom.continuation is None
            assert atom.dispositions == ()
            assert atom.reason is not None

        for atom in expected.source_outcomes:
            assert atom.provenance
            _assert_term_is_closed(atom.witness)
            _assert_term_is_closed(atom.certificate)
            assert not _term_contains_tag(atom.certificate, "fresh-id")
            for disposition in atom.dispositions:
                if isinstance(disposition.value, OracleTerm):
                    assert not _term_contains_tag(disposition.value, "fresh-id")

        all_fresh_identities: list[OracleTerm] = []
        for atom in expected.applied_atoms:
            source_atom = source_by_id[atom.source_atom_id]
            assert atom.atom_id == atom.source_atom_id
            assert atom.output_trace_lineage.tag == "lineage"
            _assert_term_is_closed(atom.output_trace_lineage)
            _assert_term_is_closed(atom.evidence)
            if source_atom.kind == "derivation":
                assert atom.successor is not None
            else:
                assert atom.successor is None
                assert atom.fresh_bindings == ()

            fresh_local_keys = [
                binding.local_key for binding in atom.fresh_bindings
            ]
            fresh_identities = [
                binding.identity for binding in atom.fresh_bindings
            ]
            assert len(fresh_local_keys) == len(set(fresh_local_keys))
            assert len(fresh_identities) == len(set(fresh_identities))
            assert set(fresh_local_keys) == {
                disposition.target
                for disposition in source_atom.dispositions
                if disposition.action == "create"
            }
            all_fresh_identities.extend(fresh_identities)
            for binding in atom.fresh_bindings:
                assert binding.local_key in case.writable
                _assert_term_is_closed(binding.local_key)
                _assert_term_is_closed(binding.identity)
                _assert_term_is_closed(binding.evidence)
        assert len(all_fresh_identities) == len(set(all_fresh_identities))

        for measure in (
            expected.measures.applied_atoms,
            expected.measures.successors,
            expected.measures.no_successors,
        ):
            if measure.kind == "absent":
                assert measure.masses == ()
                assert measure.total_mass is None
                assert measure.evidence is None
            elif measure.kind == "available":
                assert measure.masses
                assert measure.total_mass == sum(
                    (mass for _, mass in measure.masses),
                    Fraction(0, 1),
                )
                assert measure.evidence is not None
                _assert_term_is_closed(measure.evidence)
            else:
                assert measure.kind == "unavailable"
                assert measure.masses == ()
                assert measure.total_mass is None
                assert measure.evidence is not None
                _assert_term_is_closed(measure.evidence)


def test_multiway_oracle_retains_both_witnesses_in_one_successor_fiber() -> None:
    expected = MULTIWAY_CASE.expected
    assert expected.outcome_cardinality == EXACT_TWO
    assert expected.derivation_cardinality == EXACT_TWO
    assert expected.successor_cardinality == EXACT_ONE
    assert expected.successor_fibers == (
        OracleFiber(
            MW_SUCCESSOR,
            ("diamond-rule-left", "diamond-rule-right"),
        ),
    )


def test_constraint_oracles_distinguish_zero_one_and_many() -> None:
    assert (
        CONSTRAINT_ZERO_CASE.expected.outcome_cardinality,
        CONSTRAINT_ZERO_CASE.expected.derivation_cardinality,
        CONSTRAINT_ZERO_CASE.expected.successor_cardinality,
    ) == (EXACT_ONE, EXACT_ZERO, EXACT_ZERO)
    assert (
        CONSTRAINT_ONE_CASE.expected.outcome_cardinality,
        CONSTRAINT_ONE_CASE.expected.derivation_cardinality,
        CONSTRAINT_ONE_CASE.expected.successor_cardinality,
    ) == (EXACT_ONE, EXACT_ONE, EXACT_ONE)
    assert (
        CONSTRAINT_MANY_CASE.expected.outcome_cardinality,
        CONSTRAINT_MANY_CASE.expected.derivation_cardinality,
        CONSTRAINT_MANY_CASE.expected.successor_cardinality,
    ) == (EXACT_TWO, EXACT_TWO, EXACT_TWO)
    assert CONSTRAINT_ZERO_ATOM.reason == _term("terminal", "no-solution")


def test_stochastic_oracle_uses_exact_unrenormalized_submeasures() -> None:
    expected = STOCHASTIC_CASE.expected
    masses = tuple(atom.mass for atom in expected.source_outcomes)
    assert masses == (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4))
    assert sum(mass for mass in masses if mass is not None) == Fraction(1, 1)
    assert expected.measures.applied_atoms.total_mass == Fraction(1, 1)
    assert expected.measures.successors.total_mass == Fraction(3, 4)
    assert expected.measures.no_successors.total_mass == Fraction(1, 4)
    assert (
        expected.measures.successors.total_mass
        + expected.measures.no_successors.total_mass
        == Fraction(1, 1)
    )


def test_exact_differential_oracle_stops_with_the_maximal_solution_ast() -> None:
    expected = FLOW_CASE.expected
    assert expected.support_kind == "finite"
    assert expected.outcome_cardinality == EXACT_ONE
    assert FLOW_ATOM.continuation == _term("stop", "completed")
    assert expected.applied_atoms[0].successor == FLOW_SUCCESSOR
    assert FLOW_CASE.readable.arguments[-1] == _term(
        "duration-or-event-selector",
        "none",
    )


def test_intensional_oracle_is_closed_relation_data_without_a_solver() -> None:
    expected = DIFFERENTIAL_CASE.expected
    assert expected.support_kind == "intensional"
    assert expected.source_outcomes == ()
    assert expected.applied_atoms == ()
    assert expected.no_successor_partition == ()
    assert expected.outcome_cardinality == UNCOUNTABLE
    assert expected.derivation_cardinality == UNCOUNTABLE
    assert expected.successor_cardinality == UNCOUNTABLE
    assert expected.measures == ABSENT_MEASURES
    assert expected.source_intensional_relation == DIFFERENTIAL_SOURCE_RELATION
    assert expected.applied_intensional_relation == DIFFERENTIAL_APPLIED_RELATION
    assert (
        expected.successor_intensional_relation
        == DIFFERENTIAL_SUCCESSOR_RELATION
    )
    for relation in (
        expected.source_intensional_relation,
        expected.applied_intensional_relation,
        expected.successor_intensional_relation,
    ):
        assert relation is not None
        _assert_term_is_closed(relation)
