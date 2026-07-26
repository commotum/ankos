"""Five-field programs and their family-blind application boundary.

This module owns the immutable ``SimpleProgram`` value, application inputs
and results, generic reconstruction evidence, raw rollout traces, and the two
public operations that Goal 7 will implement. It consumes the five component
contracts and Rule-side result algebra without owning component factories,
semantic-family constructors, serialization, datasets, random helpers, or
visualization.

The declarations below are an inert Goal 7 scaffold. Frozen records establish
the settled ownership and public shapes, while construction validation,
application, Seed realization, replay derivation, reconstruction, quotienting,
and traversal remain uniformly unimplemented. No placeholder result is
authoritative.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Generic, NoReturn, TypeAlias, TypeVar

from . import alphabets, frontiers, loci, neighborhoods, rules, seeds


C = TypeVar("C")
V = TypeVar("V")
W = TypeVar("W")
R = TypeVar("R")


def _not_implemented() -> NoReturn:
    """Raise the standard error for unfinished Goal 7 program behavior."""

    raise NotImplementedError("Goal 7 program scaffold is not implemented")


# ---------------------------------------------------------------------------
# Phase 1.1: One Program Value
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SimpleProgram(Generic[C, V, W, R]):
    """One immutable program with exactly the five settled components."""

    seed: seeds.Seed[C]
    alphabet: alphabets.Alphabet[V]
    frontier: frontiers.WritableRegion[C, W]
    neighborhood: neighborhoods.ReadableRegion[C, R]
    rule: rules.Rule[R, W, C]

    def __post_init__(self) -> None:
        """Validate all five local descriptors and their compatibility."""

        _not_implemented()


# ---------------------------------------------------------------------------
# Phase 1.2: Application Evidence and Result Shells
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ProgramEvidence:
    """Generic closed, versioned program-owned evidence.

    This is a structural scaffold for application and trace evidence whose
    exact sealed variants land with G7-01. It deliberately admits only exact
    scalar values and already closed loci structures; it is not an opaque
    extension point or a cross-owner semantic enum.
    """

    tag: str
    version: int
    fields: tuple[
        tuple[
            str,
            bool
            | int
            | Fraction
            | str
            | loci.Locus
            | loci.SelectorExpr
            | loci.Region
            | "ProgramEvidence",
        ],
        ...,
    ] = ()


@dataclass(frozen=True)
class TraceLineage:
    """Closed invocation lineage that cannot change Rule denotation."""

    descriptor: ProgramEvidence


@dataclass(frozen=True)
class ApplicationInput(Generic[C]):
    """One immutable configuration with optional validated trace lineage."""

    configuration: C
    trace_lineage: TraceLineage | None = None


@dataclass(frozen=True)
class AppliedDerivation(Generic[C, W]):
    """Compact shell for one validated, reconstructed derivation."""

    descriptor: ProgramEvidence


@dataclass(frozen=True)
class AppliedNoSuccessor:
    """Compact shell for one validated no-successor Rule atom."""

    descriptor: ProgramEvidence


AppliedAtom: TypeAlias = AppliedDerivation[C, W] | AppliedNoSuccessor


@dataclass(frozen=True)
class SuccessorGroup(Generic[C, W]):
    """One semantic successor and its complete derivation fiber."""

    descriptor: ProgramEvidence


@dataclass(frozen=True)
class MeasureAbsent:
    """No source probability law exists."""


@dataclass(frozen=True)
class MeasureAvailable:
    """A validated measure view is available."""

    measure: ProgramEvidence


@dataclass(frozen=True)
class MeasureUnavailable:
    """Only a derived successor quotient lacks established measurability."""

    reason: ProgramEvidence
    retained_source_law_and_mapping_evidence: ProgramEvidence


MeasureView: TypeAlias = MeasureAbsent | MeasureAvailable | MeasureUnavailable


@dataclass(frozen=True)
class ApplicationComplete(Generic[C, W]):
    """Authoritative application result after every generic phase succeeds."""

    source_outcomes: rules.OutcomeSpace[rules.RuleAtom[W]]
    applied_atoms: rules.SupportSpace[AppliedAtom[C, W]]
    no_successor_partition: rules.SupportSpace[AppliedNoSuccessor]
    outcome_atom_cardinality: rules.CardinalityClaim
    derivation_cardinality: rules.CardinalityClaim
    successor_cardinality: rules.CardinalityClaim
    successor_quotient_with_derivation_fibers: rules.SupportSpace[
        SuccessorGroup[C, W]
    ]
    applied_atom_measure: MeasureView
    successor_submeasure: MeasureView
    no_successor_submeasure: MeasureView
    evidence: ProgramEvidence


@dataclass(frozen=True)
class ApplicationFault:
    """First failing generic application phase and its closed evidence."""

    phase: str
    reason: str
    evidence: tuple[str, ...]


@dataclass(frozen=True)
class ApplicationRejected:
    """Rejected application with no authoritative successor space."""

    fault: ApplicationFault


ApplicationResult: TypeAlias = ApplicationComplete[C, W] | ApplicationRejected


APPLICATION_PHASES = (
    "program",
    "input",
    "frontier",
    "neighborhood",
    "join",
    "rule-denotation",
    "result-validation",
    "fresh-binding",
    "commit",
    "successor",
    "quotient-measure",
)


def apply(
    program: SimpleProgram[C, V, W, R],
    input: C | ApplicationInput[C],
) -> ApplicationResult[C, W]:
    """Apply one program through the single family-blind atomic boundary."""

    _not_implemented()


# ---------------------------------------------------------------------------
# Phase 1.3: Rollout Records and Traversal Surface
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ContinuingLeaf(Generic[C]):
    """One configuration/lineage fiber eligible for another application."""

    configuration: C
    trace_lineage: TraceLineage


@dataclass(frozen=True)
class ClosedLeaf(Generic[C, W]):
    """One branch closed by its own continuation or no-successor semantics."""

    final_configuration: C | None
    source: AppliedAtom[C, W]


@dataclass(frozen=True)
class RawTrace(Generic[C, W]):
    """Raw structural application graph retained before downstream views."""

    roots: rules.OutcomeSpace[C]
    applications: rules.SupportSpace[ApplicationComplete[C, W]]
    derivation_edges: rules.SupportSpace[AppliedAtom[C, W]]
    lineage_graph: ProgramEvidence
    evidence: ProgramEvidence


@dataclass(frozen=True)
class RolloutComplete(Generic[C, W]):
    """A traversal whose represented branches all closed semantically."""

    raw_trace: RawTrace[C, W]
    closed_leaves: rules.SupportSpace[ClosedLeaf[C, W]]


class TruncationCause(Enum):
    """Typed external causes that do not imply semantic terminality."""

    DEPTH_BOUND = "depth-bound"
    RESOURCE_EXHAUSTED = "resource-exhausted"
    CANCELLED = "cancelled"
    PRUNED = "pruned"


@dataclass(frozen=True)
class RolloutTruncated(Generic[C, W]):
    """A raw partial trace retaining every still-continuing fiber."""

    raw_trace: RawTrace[C, W]
    continuing_leaves: rules.SupportSpace[ContinuingLeaf[C]]
    cause: TruncationCause


@dataclass(frozen=True)
class RolloutFault:
    """Invalid rollout request or traversal boundary."""

    reason: str


@dataclass(frozen=True)
class RolloutRejected:
    """Rejected rollout with no authoritative traversal result."""

    fault: RolloutFault


RolloutResult: TypeAlias = (
    RolloutComplete[C, W] | RolloutTruncated[C, W] | RolloutRejected
)
ReplayKey: TypeAlias = bool | int | Fraction | str | ProgramEvidence


def rollout(
    program: SimpleProgram[C, V, W, R],
    *,
    steps: int,
    initial: C | None = None,
    replay_key: ReplayKey | None = None,
) -> RolloutResult[C, W]:
    """Traverse only by repeatedly invoking the owned ``apply`` operation."""

    _not_implemented()


# ---------------------------------------------------------------------------
# Phase 2: Generic Application Mechanics
# ---------------------------------------------------------------------------

# Cross-field unification, snapshot resolution, closed reconstruction,
# phase-wide validation, deterministic fresh binding, semantic quotienting,
# exact measure projection, and Seed realization land here in G7-01.


# ---------------------------------------------------------------------------
# Phase 3: Traversal and Replay Mechanics
# ---------------------------------------------------------------------------

# Raw branching/intensional traversal, replay-coordinate derivation, and
# continuing-fiber expansion land here in G7-01 without a second one-step path.


__all__ = [
    "ApplicationComplete",
    "ApplicationFault",
    "ApplicationInput",
    "ApplicationRejected",
    "ApplicationResult",
    "AppliedAtom",
    "AppliedDerivation",
    "AppliedNoSuccessor",
    "ClosedLeaf",
    "ContinuingLeaf",
    "MeasureAbsent",
    "MeasureAvailable",
    "MeasureUnavailable",
    "MeasureView",
    "RawTrace",
    "ReplayKey",
    "RolloutComplete",
    "RolloutFault",
    "RolloutRejected",
    "RolloutResult",
    "RolloutTruncated",
    "SimpleProgram",
    "SuccessorGroup",
    "TraceLineage",
    "TruncationCause",
    "apply",
    "rollout",
]
