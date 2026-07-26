"""Frozen implementation-independent one-step oracles for Goal 7 CT12.

This module is deliberately both fixture data and its Stage 1 consistency
suite.  It imports only the Python standard library and contains no transition
evaluator.  Future CT12 tests map real ``ApplicationResult`` records onto these
closed test-only terms; the runtime must never import this module.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Literal, TypeAlias


OracleScalar: TypeAlias = bool | int | Fraction | str | None
Action: TypeAlias = Literal["preserve", "replace", "delete", "absent", "create"]
AtomKind: TypeAlias = Literal["derivation", "no-successor"]
Progress: TypeAlias = Literal["advanced", "quiescent"]
SupportKind: TypeAlias = Literal["finite", "intensional"]
CardinalityKind: TypeAlias = Literal["exact", "uncountable"]


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
class OracleAtom:
    """One complete expected Rule/application atom."""

    atom_id: str
    kind: AtomKind
    witness: OracleTerm
    provenance: tuple[str, ...]
    lineage: OracleTerm
    progress: Progress | None
    continuation: OracleTerm | None
    dispositions: tuple[OracleDisposition, ...]
    successor: OracleTerm | None
    reason: OracleTerm | None
    certificate: OracleTerm
    mass: Fraction | None = None


@dataclass(frozen=True)
class OracleFiber:
    """One expected semantic successor and its complete derivation fiber."""

    successor: OracleTerm
    atom_ids: tuple[str, ...]


@dataclass(frozen=True)
class OracleExpected:
    """Complete normalized expectation for one generic application."""

    support_kind: SupportKind
    atoms: tuple[OracleAtom, ...]
    outcome_cardinality: OracleCardinality
    derivation_cardinality: OracleCardinality
    successor_cardinality: OracleCardinality
    successor_fibers: tuple[OracleFiber, ...]
    applied_atom_mass: Fraction | None
    successor_mass: Fraction | None
    no_successor_mass: Fraction | None
    intensional_relation: OracleTerm | None
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
    execution_start_commit: str
    goal6_runtime_src_tree: str
    goal6_runtime_tests_tree: str
    execution_start_src_tree: str
    execution_start_tests_tree: str
    goal2_tree: str
    goal5_tree: str
    python_version: str
    numpy_version: str
    package_version: str
    package_description: str
    runtime_dependencies: tuple[str, ...]
    active_test_baseline: str
    root_exports: tuple[str, ...]
    target_root_exports: tuple[str, ...]
    physical_modules_to_remove: tuple[str, ...]


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


EXACT_ZERO = OracleCardinality("exact", 0)
EXACT_ONE = OracleCardinality("exact", 1)
EXACT_TWO = OracleCardinality("exact", 2)
EXACT_THREE = OracleCardinality("exact", 3)
UNCOUNTABLE = OracleCardinality("uncountable", None)


PRE_CUTOVER = PreCutoverSnapshot(
    goal6_close_commit="60bde6da318f415e43e14fc98b5faa28f14cd945",
    execution_start_commit="95ba134ee8f9671181c237cd2975004f3442efbe",
    goal6_runtime_src_tree="6e6b34769d60508c03d0a69fad1ede4fef75e217",
    goal6_runtime_tests_tree="02ad081e039a46efbf61855fdeae60abb7bb70ad",
    execution_start_src_tree="af9ae63c9b3683fd9b7ba1292d9127f647dc48f5",
    execution_start_tests_tree="a77a8f6092c9b3f907a1bd6aee7c6b09c1055fa7",
    goal2_tree="48b6309655ec7c1d3aaa1a0ec5dfb700385e16d1",
    goal5_tree="ba62f20b8c620094a0ad683906a803c5404be5f2",
    python_version="3.10.13",
    numpy_version="2.2.6",
    package_version="0.1.0",
    package_description="A New Kind of Science cellular automata library",
    runtime_dependencies=("numpy>=2.2", "pytest>=9.0.3"),
    active_test_baseline="102 passed, 96 skipped",
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
    physical_modules_to_remove=("ca.rollout", "ca.specs"),
)


# Current native scalar: AR2 rule 0 means a=1, b=0, constant=1.
AR2_PREVIOUS = _term("field", "previous")
AR2_CURRENT = _term("field", "current")
AR2_SOURCE = _term(
    "configuration.record",
    _term("field-value", "previous", 1),
    _term("field-value", "current", 2),
)
AR2_SUCCESSOR = _term(
    "configuration.record",
    _term("field-value", "previous", 2),
    _term("field-value", "current", 3),
)
AR2_ATOM = OracleAtom(
    atom_id="ar2-step",
    kind="derivation",
    witness=_term("witness.rule", "ar2-modular", "rule-id", 0),
    provenance=("native:ar2_modular_0d", "rule-0:a=1,b=0,c=1,mod=97"),
    lineage=_term("lineage", "native.scalar.ar2-modular", "ar2-step"),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(AR2_PREVIOUS, "replace", 2),
        _disposition(AR2_CURRENT, "replace", 3),
    ),
    successor=AR2_SUCCESSOR,
    reason=None,
    certificate=_term("arithmetic-certificate", _term("equals", 3, 3)),
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
        _term("field-value", "previous", 1),
        _term("field-value", "current", 2),
    ),
    expected=OracleExpected(
        support_kind="finite",
        atoms=(AR2_ATOM,),
        outcome_cardinality=EXACT_ONE,
        derivation_cardinality=EXACT_ONE,
        successor_cardinality=EXACT_ONE,
        successor_fibers=(OracleFiber(AR2_SUCCESSOR, ("ar2-step",)),),
        applied_atom_mass=None,
        successor_mass=None,
        no_successor_mass=None,
        intensional_relation=None,
        evidence=_term("application-evidence", "native.scalar.ar2-modular"),
    ),
)


# Current native cellular: the finite rule-0 table writes zero at every site.
LINE_LEFT = _term("cell1d", -1)
LINE_CENTER = _term("cell1d", 0)
LINE_RIGHT = _term("cell1d", 1)
LINE_SOURCE = _term("line1d", _term("values", 1, 0, 1))
LINE_SUCCESSOR = _term("line1d", _term("values", 0, 0, 0))
LINE_ATOM = OracleAtom(
    atom_id="dyadrads-rule-0",
    kind="derivation",
    witness=_term("witness.rule", "dyadrads-1d", "rule-id", 0),
    provenance=("native:dyadrads_1d", "fixed-boundary:0"),
    lineage=_term("lineage", "native.cellular.dyadrads-rule-0", "dyadrads-rule-0"),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(LINE_LEFT, "replace", 0),
        _disposition(LINE_CENTER, "replace", 0),
        _disposition(LINE_RIGHT, "replace", 0),
    ),
    successor=LINE_SUCCESSOR,
    reason=None,
    certificate=_term("lookup-certificate", "rule-0", "all-contexts-to-zero"),
)
LINE_CASE = OracleCase(
    case_id="native.cellular.dyadrads-rule-0",
    mechanics=("current-cellular", "cellular"),
    conformance_refs=("G7-00:current-cellular", "CT12"),
    current_native=True,
    source=LINE_SOURCE,
    writable=(LINE_LEFT, LINE_CENTER, LINE_RIGHT),
    readable=_term(
        "old-snapshot-stencils",
        _term("values", 1, 0, 1),
        _term("boundary", "fixed", 0),
    ),
    expected=OracleExpected(
        support_kind="finite",
        atoms=(LINE_ATOM,),
        outcome_cardinality=EXACT_ONE,
        derivation_cardinality=EXACT_ONE,
        successor_cardinality=EXACT_ONE,
        successor_fibers=(OracleFiber(LINE_SUCCESSOR, ("dyadrads-rule-0",)),),
        applied_atom_mass=None,
        successor_mass=None,
        no_successor_mass=None,
        intensional_relation=None,
        evidence=_term("application-evidence", "native.cellular.dyadrads-rule-0"),
    ),
)


# Current native multidimensional case: the 2-D finite rule-0 table is zero.
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
    _term("row", 0, 1, 0),
    _term("row", 1, 1, 1),
    _term("row", 0, 1, 0),
)
GRID_SUCCESSOR = _term(
    "grid2d",
    _term("row", 0, 0, 0),
    _term("row", 0, 0, 0),
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
GRID_ATOM = OracleAtom(
    atom_id="dyadaxes-2d-rule-0",
    kind="derivation",
    witness=_term("witness.rule", "dyadaxes-2d", "rule-id", 0),
    provenance=("native:dyadaxes_2d", "fixed-boundary:0"),
    lineage=_term(
        "lineage",
        "native.multidimensional.dyadaxes-2d-rule-0",
        "dyadaxes-2d-rule-0",
    ),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=tuple(_disposition(target, "replace", 0) for target in GRID_WRITABLE),
    successor=GRID_SUCCESSOR,
    reason=None,
    certificate=_term("lookup-certificate", "rule-0", "all-contexts-to-zero"),
)
GRID_CASE = OracleCase(
    case_id="native.multidimensional.dyadaxes-2d-rule-0",
    mechanics=("current-multidimensional", "cellular"),
    conformance_refs=("G7-00:current-multidimensional", "CT12"),
    current_native=True,
    source=GRID_SOURCE,
    writable=GRID_WRITABLE,
    readable=_term(
        "old-snapshot-2d-stencils",
        GRID_SOURCE,
        _term("boundary", "fixed", 0),
    ),
    expected=OracleExpected(
        support_kind="finite",
        atoms=(GRID_ATOM,),
        outcome_cardinality=EXACT_ONE,
        derivation_cardinality=EXACT_ONE,
        successor_cardinality=EXACT_ONE,
        successor_fibers=(
            OracleFiber(GRID_SUCCESSOR, ("dyadaxes-2d-rule-0",)),
        ),
        applied_atom_mass=None,
        successor_mass=None,
        no_successor_mass=None,
        intensional_relation=None,
        evidence=_term(
            "application-evidence",
            "native.multidimensional.dyadaxes-2d-rule-0",
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
MOBILE_LEFT_ATOM = OracleAtom(
    atom_id="mobile-left",
    kind="derivation",
    witness=_term("transition-witness", "q", 1, "p", 0, "left"),
    provenance=("PX01:F031", "transition:left"),
    lineage=_term("lineage", "px01.mobile-head-branching", "mobile-left"),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(TAPE_LEFT, "replace", HEAD_P0),
        _disposition(TAPE_SOURCE, "replace", 0),
        _disposition(TAPE_RIGHT, "preserve"),
    ),
    successor=MOBILE_LEFT_SUCCESSOR,
    reason=None,
    certificate=_term("single-head-certificate", -1),
)
MOBILE_RIGHT_ATOM = OracleAtom(
    atom_id="mobile-right",
    kind="derivation",
    witness=_term("transition-witness", "q", 1, "p", 0, "right"),
    provenance=("PX01:F031", "transition:right"),
    lineage=_term("lineage", "px01.mobile-head-branching", "mobile-right"),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(TAPE_LEFT, "preserve"),
        _disposition(TAPE_SOURCE, "replace", 0),
        _disposition(TAPE_RIGHT, "replace", HEAD_P0),
    ),
    successor=MOBILE_RIGHT_SUCCESSOR,
    reason=None,
    certificate=_term("single-head-certificate", 1),
)
MOBILE_CASE = OracleCase(
    case_id="px01.mobile-head-branching",
    mechanics=("mobile",),
    conformance_refs=("PX01:F031", "CT12"),
    current_native=False,
    source=MOBILE_SOURCE,
    writable=(TAPE_LEFT, TAPE_SOURCE, TAPE_RIGHT),
    readable=_term("keyed-old-tape", MOBILE_SOURCE),
    expected=OracleExpected(
        support_kind="finite",
        atoms=(MOBILE_LEFT_ATOM, MOBILE_RIGHT_ATOM),
        outcome_cardinality=EXACT_TWO,
        derivation_cardinality=EXACT_TWO,
        successor_cardinality=EXACT_TWO,
        successor_fibers=(
            OracleFiber(MOBILE_LEFT_SUCCESSOR, ("mobile-left",)),
            OracleFiber(MOBILE_RIGHT_SUCCESSOR, ("mobile-right",)),
        ),
        applied_atom_mass=None,
        successor_mass=None,
        no_successor_mass=None,
        intensional_relation=None,
        evidence=_term("application-evidence", "px01.mobile-head-branching"),
    ),
)


# A deterministic Turing profile is the same generic mechanic with one atom.
TURING_SUCCESSOR = _term(
    "tape",
    _term("at", -1, 0),
    _term("at", 0, 0),
    _term("at", 1, _term("head", "scan", 0)),
)
TURING_ATOM = OracleAtom(
    atom_id="turing-write-right",
    kind="derivation",
    witness=_term("transition-witness", "q", 1, "scan", 0, "right"),
    provenance=("CT12:turing", "PX01:F031"),
    lineage=_term("lineage", "ct12.turing-write-move", "turing-write-right"),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(TAPE_LEFT, "preserve"),
        _disposition(TAPE_SOURCE, "replace", 0),
        _disposition(TAPE_RIGHT, "replace", _term("head", "scan", 0)),
    ),
    successor=TURING_SUCCESSOR,
    reason=None,
    certificate=_term("single-head-certificate", 1),
)
TURING_CASE = OracleCase(
    case_id="ct12.turing-write-move",
    mechanics=("turing",),
    conformance_refs=("CT12:mobile/Turing", "PX01:F031"),
    current_native=False,
    source=MOBILE_SOURCE,
    writable=(TAPE_LEFT, TAPE_SOURCE, TAPE_RIGHT),
    readable=_term("keyed-old-tape", MOBILE_SOURCE),
    expected=OracleExpected(
        support_kind="finite",
        atoms=(TURING_ATOM,),
        outcome_cardinality=EXACT_ONE,
        derivation_cardinality=EXACT_ONE,
        successor_cardinality=EXACT_ONE,
        successor_fibers=(
            OracleFiber(TURING_SUCCESSOR, ("turing-write-right",)),
        ),
        applied_atom_mass=None,
        successor_mass=None,
        no_successor_mass=None,
        intensional_relation=None,
        evidence=_term("application-evidence", "ct12.turing-write-move"),
    ),
)


# PX02 parallel substitution: A -> AB and B -> epsilon in one old-snapshot pass.
SUB_OLD_A = _term("occurrence", "old", 0)
SUB_OLD_B = _term("occurrence", "old", 1)
SUB_NEW_A = _term("fresh-child", "old:0", 0)
SUB_NEW_B = _term("fresh-child", "old:0", 1)
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
SUB_ATOM = OracleAtom(
    atom_id="parallel-substitution",
    kind="derivation",
    witness=_term("generation-witness", "A->AB", "B->epsilon"),
    provenance=("PX02:F038",),
    lineage=_term("lineage", "px02.parallel-substitution", "parallel-substitution"),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(SUB_OLD_A, "delete"),
        _disposition(SUB_OLD_B, "delete"),
        _disposition(SUB_NEW_A, "create", _term("symbol-value", "A")),
        _disposition(SUB_NEW_B, "create", _term("symbol-value", "B")),
    ),
    successor=SUB_SUCCESSOR,
    reason=None,
    certificate=_term("ordered-offspring-certificate", SUB_NEW_A, SUB_NEW_B),
)
SUBSTITUTION_CASE = OracleCase(
    case_id="px02.parallel-substitution",
    mechanics=("substitution", "variable-support"),
    conformance_refs=("PX02:F038", "CT12"),
    current_native=False,
    source=SUB_SOURCE,
    writable=(SUB_OLD_A, SUB_OLD_B, SUB_NEW_A, SUB_NEW_B),
    readable=_term("old-generation-items", SUB_SOURCE),
    expected=OracleExpected(
        support_kind="finite",
        atoms=(SUB_ATOM,),
        outcome_cardinality=EXACT_ONE,
        derivation_cardinality=EXACT_ONE,
        successor_cardinality=EXACT_ONE,
        successor_fibers=(OracleFiber(SUB_SUCCESSOR, ("parallel-substitution",)),),
        applied_atom_mass=None,
        successor_mass=None,
        no_successor_mass=None,
        intensional_relation=None,
        evidence=_term("application-evidence", "px02.parallel-substitution"),
    ),
)


# PX04 multiway diamond: two witnessed rewrites quotient to one successor.
MW_TARGET = _term("word-occurrence", 0)
MW_SOURCE = _term("word", _term("symbol", MW_TARGET, "a"))
MW_SUCCESSOR = _term("word", _term("symbol", MW_TARGET, "b"))
MW_ATOM_LEFT = OracleAtom(
    atom_id="diamond-rule-left",
    kind="derivation",
    witness=_term("rewrite-witness", "rule-left", "match:0", "parent:a"),
    provenance=("PX04:F034", "rule:left"),
    lineage=_term("lineage", "px04.multiway-diamond", "diamond-rule-left"),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(_disposition(MW_TARGET, "replace", _term("symbol-value", "b")),),
    successor=MW_SUCCESSOR,
    reason=None,
    certificate=_term("rewrite-certificate", "a->b", "left"),
)
MW_ATOM_RIGHT = OracleAtom(
    atom_id="diamond-rule-right",
    kind="derivation",
    witness=_term("rewrite-witness", "rule-right", "match:0", "parent:a"),
    provenance=("PX04:F034", "rule:right"),
    lineage=_term("lineage", "px04.multiway-diamond", "diamond-rule-right"),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(_disposition(MW_TARGET, "replace", _term("symbol-value", "b")),),
    successor=MW_SUCCESSOR,
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
        atoms=(MW_ATOM_LEFT, MW_ATOM_RIGHT),
        outcome_cardinality=EXACT_TWO,
        derivation_cardinality=EXACT_TWO,
        successor_cardinality=EXACT_ONE,
        successor_fibers=(
            OracleFiber(
                MW_SUCCESSOR,
                ("diamond-rule-left", "diamond-rule-right"),
            ),
        ),
        applied_atom_mass=None,
        successor_mass=None,
        no_successor_mass=None,
        intensional_relation=None,
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


CONSTRAINT_ZERO_ATOM = OracleAtom(
    atom_id="constraint-no-solution",
    kind="no-successor",
    witness=_term("relation-witness", "x^2=2", "Z/3Z"),
    provenance=("PX04:F019", "rhs=2"),
    lineage=_term("lineage", "px04.constraint-mod3-zero", "constraint-no-solution"),
    progress=None,
    continuation=None,
    dispositions=(),
    successor=None,
    reason=_term("terminal", "no-solution"),
    certificate=_term(
        "truth-table",
        _term("row", 0, False),
        _term("row", 1, False),
        _term("row", 2, False),
    ),
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
        atoms=(CONSTRAINT_ZERO_ATOM,),
        outcome_cardinality=EXACT_ONE,
        derivation_cardinality=EXACT_ZERO,
        successor_cardinality=EXACT_ZERO,
        successor_fibers=(),
        applied_atom_mass=None,
        successor_mass=None,
        no_successor_mass=None,
        intensional_relation=None,
        evidence=_term("application-evidence", "px04.constraint-mod3-zero"),
    ),
)

CONSTRAINT_ONE_SUCCESSOR = _term("assignment", _term("value", "x", 0))
CONSTRAINT_ONE_ATOM = OracleAtom(
    atom_id="constraint-x-0",
    kind="derivation",
    witness=_term("solution-witness", "x", 0),
    provenance=("PX04:F019", "rhs=0"),
    lineage=_term("lineage", "px04.constraint-mod3-one", "constraint-x-0"),
    progress="advanced",
    continuation=_term("stop", "completed"),
    dispositions=(_disposition(CONSTRAINT_X, "replace", 0),),
    successor=CONSTRAINT_ONE_SUCCESSOR,
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
        atoms=(CONSTRAINT_ONE_ATOM,),
        outcome_cardinality=EXACT_ONE,
        derivation_cardinality=EXACT_ONE,
        successor_cardinality=EXACT_ONE,
        successor_fibers=(
            OracleFiber(CONSTRAINT_ONE_SUCCESSOR, ("constraint-x-0",)),
        ),
        applied_atom_mass=None,
        successor_mass=None,
        no_successor_mass=None,
        intensional_relation=None,
        evidence=_term("application-evidence", "px04.constraint-mod3-one"),
    ),
)

CONSTRAINT_X1_SUCCESSOR = _term("assignment", _term("value", "x", 1))
CONSTRAINT_X2_SUCCESSOR = _term("assignment", _term("value", "x", 2))
CONSTRAINT_X1_ATOM = OracleAtom(
    atom_id="constraint-x-1",
    kind="derivation",
    witness=_term("solution-witness", "x", 1),
    provenance=("PX04:F019", "rhs=1"),
    lineage=_term("lineage", "px04.constraint-mod3-many", "constraint-x-1"),
    progress="advanced",
    continuation=_term("stop", "completed"),
    dispositions=(_disposition(CONSTRAINT_X, "replace", 1),),
    successor=CONSTRAINT_X1_SUCCESSOR,
    reason=None,
    certificate=_term("equation-certificate", "1^2=1 mod 3"),
)
CONSTRAINT_X2_ATOM = OracleAtom(
    atom_id="constraint-x-2",
    kind="derivation",
    witness=_term("solution-witness", "x", 2),
    provenance=("PX04:F019", "rhs=1"),
    lineage=_term("lineage", "px04.constraint-mod3-many", "constraint-x-2"),
    progress="advanced",
    continuation=_term("stop", "completed"),
    dispositions=(_disposition(CONSTRAINT_X, "replace", 2),),
    successor=CONSTRAINT_X2_SUCCESSOR,
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
        atoms=(CONSTRAINT_X1_ATOM, CONSTRAINT_X2_ATOM),
        outcome_cardinality=EXACT_TWO,
        derivation_cardinality=EXACT_TWO,
        successor_cardinality=EXACT_TWO,
        successor_fibers=(
            OracleFiber(CONSTRAINT_X1_SUCCESSOR, ("constraint-x-1",)),
            OracleFiber(CONSTRAINT_X2_SUCCESSOR, ("constraint-x-2",)),
        ),
        applied_atom_mass=None,
        successor_mass=None,
        no_successor_mass=None,
        intensional_relation=None,
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
        _term("edge", "a", GRAPH_X),
        _term("edge", GRAPH_X, GRAPH_Y),
        _term("edge", GRAPH_Y, "c"),
    ),
)
GRAPH_ATOM = OracleAtom(
    atom_id="graph-replacement",
    kind="derivation",
    witness=_term("match", _term("node", "b"), _term("ports", "a", "c")),
    provenance=("PX02:F029",),
    lineage=_term(
        "lineage",
        "px02.graph-interface-replacement",
        "graph-replacement",
    ),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(GRAPH_B, "delete"),
        _disposition(GRAPH_AB, "delete"),
        _disposition(GRAPH_BC, "delete"),
        _disposition(GRAPH_X_SLOT, "create", GRAPH_X),
        _disposition(GRAPH_Y_SLOT, "create", GRAPH_Y),
        _disposition(GRAPH_AX_SLOT, "create", _term("edge", "a", GRAPH_X)),
        _disposition(GRAPH_XY_SLOT, "create", _term("edge", GRAPH_X, GRAPH_Y)),
        _disposition(GRAPH_YC_SLOT, "create", _term("edge", GRAPH_Y, "c")),
    ),
    successor=GRAPH_SUCCESSOR,
    reason=None,
    certificate=_term(
        "interface-certificate",
        _term("external", "a", "c"),
        _term("fresh", GRAPH_X, GRAPH_Y),
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
        atoms=(GRAPH_ATOM,),
        outcome_cardinality=EXACT_ONE,
        derivation_cardinality=EXACT_ONE,
        successor_cardinality=EXACT_ONE,
        successor_fibers=(OracleFiber(GRAPH_SUCCESSOR, ("graph-replacement",)),),
        applied_atom_mass=None,
        successor_mass=None,
        no_successor_mass=None,
        intensional_relation=None,
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
SEARCH_ACCEPT_ATOM = OracleAtom(
    atom_id="search-accept",
    kind="derivation",
    witness=_term("proposal-witness", 1, "accepted"),
    provenance=("PX06:F050",),
    lineage=_term("lineage", "px06.stochastic-search-law", "search-accept"),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(SEARCH_X, "replace", 1),
        _disposition(SEARCH_K, "replace", 1),
    ),
    successor=SEARCH_ACCEPT_SUCCESSOR,
    reason=None,
    certificate=_term("law-atom-certificate", "accept", Fraction(1, 2)),
    mass=Fraction(1, 2),
)
SEARCH_REJECT_ATOM = OracleAtom(
    atom_id="search-reject",
    kind="derivation",
    witness=_term("proposal-witness", 0, "rejected"),
    provenance=("PX06:F050",),
    lineage=_term("lineage", "px06.stochastic-search-law", "search-reject"),
    progress="advanced",
    continuation=_term("continue"),
    dispositions=(
        _disposition(SEARCH_X, "preserve"),
        _disposition(SEARCH_K, "replace", 1),
    ),
    successor=SEARCH_REJECT_SUCCESSOR,
    reason=None,
    certificate=_term("law-atom-certificate", "reject", Fraction(1, 4)),
    mass=Fraction(1, 4),
)
SEARCH_NONE_ATOM = OracleAtom(
    atom_id="search-no-proposal",
    kind="no-successor",
    witness=_term("proposal-witness", "none"),
    provenance=("PX06:F050",),
    lineage=_term("lineage", "px06.stochastic-search-law", "search-no-proposal"),
    progress=None,
    continuation=None,
    dispositions=(),
    successor=None,
    reason=_term("terminal", "no-proposal"),
    certificate=_term("law-atom-certificate", "no-proposal", Fraction(1, 4)),
    mass=Fraction(1, 4),
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
        atoms=(SEARCH_ACCEPT_ATOM, SEARCH_REJECT_ATOM, SEARCH_NONE_ATOM),
        outcome_cardinality=EXACT_THREE,
        derivation_cardinality=EXACT_TWO,
        successor_cardinality=EXACT_TWO,
        successor_fibers=(
            OracleFiber(SEARCH_ACCEPT_SUCCESSOR, ("search-accept",)),
            OracleFiber(SEARCH_REJECT_SUCCESSOR, ("search-reject",)),
        ),
        applied_atom_mass=Fraction(1, 1),
        successor_mass=Fraction(3, 4),
        no_successor_mass=Fraction(1, 4),
        intensional_relation=None,
        evidence=_term("application-evidence", "px06.stochastic-search-law"),
    ),
)


# PX05 differential/intensional relation: every exact constant field is valid.
FIELD_U = _term("field-capability", "u")
DIFFERENTIAL_RELATION = _term(
    "intensional-relation",
    _term("binder", "c"),
    _term("domain", "exact-real"),
    _term(
        "derivation-template",
        _term("replace", FIELD_U, _term("constant-field", "c")),
        _term("witness", _term("derivative", "u", "x"), 0),
        _term("stop", "completed"),
    ),
)
DIFFERENTIAL_CASE = OracleCase(
    case_id="px05.constant-field-intensional",
    mechanics=("differential-intensional",),
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
        atoms=(),
        outcome_cardinality=UNCOUNTABLE,
        derivation_cardinality=UNCOUNTABLE,
        successor_cardinality=UNCOUNTABLE,
        successor_fibers=(),
        applied_atom_mass=None,
        successor_mass=None,
        no_successor_mass=None,
        intensional_relation=DIFFERENTIAL_RELATION,
        evidence=_term(
            "application-evidence",
            "px05.constant-field-intensional",
            _term("coverage", "all-exact-real-c"),
        ),
    ),
)


CT12_CASES = (
    AR2_CASE,
    LINE_CASE,
    GRID_CASE,
    MOBILE_CASE,
    TURING_CASE,
    SUBSTITUTION_CASE,
    MULTIWAY_CASE,
    CONSTRAINT_ZERO_CASE,
    CONSTRAINT_ONE_CASE,
    CONSTRAINT_MANY_CASE,
    GRAPH_CASE,
    STOCHASTIC_CASE,
    DIFFERENTIAL_CASE,
)

REQUIRED_CT12_MECHANICS = (
    "current-scalar",
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
    "differential-intensional",
)


def _assert_term_is_closed(term: OracleTerm) -> None:
    assert term.tag
    for argument in term.arguments:
        if isinstance(argument, OracleTerm):
            _assert_term_is_closed(argument)
        else:
            assert isinstance(argument, (bool, int, Fraction, str)) or argument is None
            assert not isinstance(argument, float)


def test_pre_cutover_snapshot_is_exact_and_complete() -> None:
    assert len(PRE_CUTOVER.root_exports) == 67
    assert len(set(PRE_CUTOVER.root_exports)) == 67
    assert PRE_CUTOVER.physical_modules_to_remove == ("ca.rollout", "ca.specs")
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
    tree = ast.parse(Path(__file__).read_text())
    allowed_import_roots = {
        "__future__",
        "ast",
        "dataclasses",
        "fractions",
        "pathlib",
        "typing",
    }
    forbidden_call_names = {
        "apply",
        "apply_rule",
        "commit",
        "denote",
        "eval",
        "evaluate",
        "exec",
        "instantiate",
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


def test_oracle_inventory_covers_every_minimum_ct12_mechanic() -> None:
    covered = {mechanic for case in CT12_CASES for mechanic in case.mechanics}
    assert covered >= set(REQUIRED_CT12_MECHANICS)
    assert tuple(case.case_id for case in CT12_CASES[:3]) == (
        "native.scalar.ar2-modular",
        "native.cellular.dyadrads-rule-0",
        "native.multidimensional.dyadaxes-2d-rule-0",
    )
    assert all(case.current_native for case in CT12_CASES[:3])
    assert not any(case.current_native for case in CT12_CASES[3:])


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

        assert expected.intensional_relation is None
        assert expected.outcome_cardinality == OracleCardinality(
            "exact",
            len(expected.atoms),
        )

        atom_ids = [atom.atom_id for atom in expected.atoms]
        assert len(atom_ids) == len(set(atom_ids))
        derivations = [atom for atom in expected.atoms if atom.kind == "derivation"]
        no_successors = [
            atom for atom in expected.atoms if atom.kind == "no-successor"
        ]
        successors = {atom.successor for atom in derivations}
        assert None not in successors
        assert expected.derivation_cardinality == OracleCardinality(
            "exact",
            len(derivations),
        )
        assert expected.successor_cardinality == OracleCardinality(
            "exact",
            len(successors),
        )

        fiber_atom_ids: list[str] = []
        for fiber in expected.successor_fibers:
            assert fiber.successor in successors
            fiber_atom_ids.extend(fiber.atom_ids)
        assert sorted(fiber_atom_ids) == sorted(atom.atom_id for atom in derivations)

        for atom in derivations:
            assert atom.progress is not None
            assert atom.continuation is not None
            assert atom.successor is not None
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

        for atom in no_successors:
            assert atom.progress is None
            assert atom.continuation is None
            assert atom.dispositions == ()
            assert atom.successor is None
            assert atom.reason is not None

        for atom in expected.atoms:
            assert atom.provenance
            assert atom.lineage.tag == "lineage"
            _assert_term_is_closed(atom.witness)
            _assert_term_is_closed(atom.lineage)
            _assert_term_is_closed(atom.certificate)


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
    masses = tuple(atom.mass for atom in expected.atoms)
    assert masses == (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4))
    assert sum(mass for mass in masses if mass is not None) == Fraction(1, 1)
    assert expected.applied_atom_mass == Fraction(1, 1)
    assert expected.successor_mass == Fraction(3, 4)
    assert expected.no_successor_mass == Fraction(1, 4)
    assert expected.successor_mass + expected.no_successor_mass == Fraction(1, 1)


def test_intensional_oracle_is_closed_relation_data_without_a_solver() -> None:
    expected = DIFFERENTIAL_CASE.expected
    assert expected.support_kind == "intensional"
    assert expected.atoms == ()
    assert expected.outcome_cardinality == UNCOUNTABLE
    assert expected.derivation_cardinality == UNCOUNTABLE
    assert expected.successor_cardinality == UNCOUNTABLE
    assert expected.intensional_relation == DIFFERENTIAL_RELATION
    assert expected.intensional_relation.tag == "intensional-relation"
    _assert_term_is_closed(expected.intensional_relation)
