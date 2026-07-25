"""Code-shaped walkthrough of the remastered five-field architecture.

This is reference material, not package runtime code.  It shows the intended
dependency direction and public reading without introducing a second model:

    loci -> component algebras -> SimpleProgram -> catalog -> apply -> rollout

Every semantic value below is closed structural data.  There are no callbacks,
opaque solver objects, ambient randomness sources, family registries, or
configurable update policies.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Generic, TypeAlias, TypeVar


C = TypeVar("C")
V = TypeVar("V")
W = TypeVar("W")
R = TypeVar("R")
A = TypeVar("A")
P = TypeVar("P")

ExactScalar: TypeAlias = bool | int | Fraction | str


# ---------------------------------------------------------------------------
# loci.py — closed structural identity and region algebra
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Coordinate:
    axes: tuple[tuple[str, Fraction], ...]


@dataclass(frozen=True)
class NamedLocus:
    name: str


@dataclass(frozen=True)
class Occurrence:
    sequence: str
    index: int


@dataclass(frozen=True)
class GraphLocus:
    graph: str
    element: str
    port: str | None = None


@dataclass(frozen=True)
class FieldLocus:
    field: str
    component: str
    point: tuple[Fraction, ...]


@dataclass(frozen=True)
class FreshLocus:
    namespace: str
    parent_or_interface: str
    local_key: str


Locus: TypeAlias = (
    Coordinate | NamedLocus | Occurrence | GraphLocus | FieldLocus | FreshLocus
)


class RelationPrimitive(Enum):
    EQUAL = "equal"
    TAGGED = "tagged"
    ADJACENT = "adjacent"
    INCIDENT = "incident"
    REACHABLE = "reachable"
    WITHIN = "within"
    DERIVATIVE = "derivative"


@dataclass(frozen=True)
class RelationExpr:
    primitive: RelationPrimitive
    operands: tuple[ExactScalar | Locus, ...]


@dataclass(frozen=True)
class LiteralRegion:
    loci: tuple[Locus, ...]


@dataclass(frozen=True)
class AllSupport:
    carrier_name: str


@dataclass(frozen=True)
class RelativeRegion:
    anchors: "Region"
    offsets: tuple[Coordinate, ...]


@dataclass(frozen=True)
class ProductRegion:
    fields: tuple[tuple[str, "Region"], ...]


@dataclass(frozen=True)
class UnionRegion:
    parts: tuple["Region", ...]


@dataclass(frozen=True)
class FreshChildren:
    parents: "Region"
    namespace: str
    slots: tuple[str, ...]


@dataclass(frozen=True)
class IntensionalRegion:
    binder: str
    relation: RelationExpr


Region: TypeAlias = (
    LiteralRegion
    | AllSupport
    | RelativeRegion
    | ProductRegion
    | UnionRegion
    | FreshChildren
    | IntensionalRegion
)


# ---------------------------------------------------------------------------
# alphabets.py — closed value structure
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BooleanValues:
    values: tuple[bool, bool] = (False, True)


@dataclass(frozen=True)
class FiniteValues:
    values: tuple[ExactScalar, ...]


@dataclass(frozen=True)
class IntegerValues:
    minimum: int | None = None
    maximum: int | None = None


@dataclass(frozen=True)
class RationalValues:
    minimum: Fraction | None = None
    maximum: Fraction | None = None


@dataclass(frozen=True)
class TaggedValues:
    variants: tuple[tuple[str, "ValueSchema"], ...]


@dataclass(frozen=True)
class ProductValues:
    fields: tuple[tuple[str, "ValueSchema"], ...]


@dataclass(frozen=True)
class SymbolicValues:
    grammar: RelationExpr


ValueSchema: TypeAlias = (
    BooleanValues
    | FiniteValues
    | IntegerValues
    | RationalValues
    | TaggedValues
    | ProductValues
    | SymbolicValues
)


@dataclass(frozen=True)
class Alphabet(Generic[V]):
    schema: ValueSchema


class alphabets:
    """Representative primitive, compound, and general constructors."""

    @staticmethod
    def boolean() -> Alphabet[bool]:
        return Alphabet(BooleanValues())

    @staticmethod
    def finite(values: tuple[ExactScalar, ...]) -> Alphabet[ExactScalar]:
        return Alphabet(FiniteValues(values))

    @staticmethod
    def tagged(
        variants: tuple[tuple[str, ValueSchema], ...],
    ) -> Alphabet[ExactScalar]:
        return Alphabet(TaggedValues(variants))

    @staticmethod
    def product(
        fields: tuple[tuple[str, ValueSchema], ...],
    ) -> Alphabet[tuple[ExactScalar, ...]]:
        return Alphabet(ProductValues(fields))


# ---------------------------------------------------------------------------
# seeds.py — sources of invariant-bearing initial configurations
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Boundary:
    policy: str
    exterior: ExactScalar | None = None


@dataclass(frozen=True)
class BinaryLine:
    values: tuple[bool, ...]
    boundary: Boundary
    support_identity: str


@dataclass(frozen=True)
class ExactSource(Generic[C]):
    configuration: C


@dataclass(frozen=True)
class BernoulliSource:
    support: Region
    probability_true: Fraction
    boundary: Boundary


@dataclass(frozen=True)
class ProductSource(Generic[C]):
    fields: tuple[tuple[str, "Seed[C]"], ...]


@dataclass(frozen=True)
class IntensionalSource:
    binder: str
    construction: RelationExpr


@dataclass(frozen=True)
class Seed(Generic[C]):
    source: ExactSource[C] | BernoulliSource | ProductSource[C] | IntensionalSource


class seeds:
    @staticmethod
    def exact(configuration: C) -> Seed[C]:
        return Seed(ExactSource(configuration))

    @staticmethod
    def bernoulli(
        support: Region,
        probability_true: Fraction,
        boundary: Boundary,
    ) -> Seed[BinaryLine]:
        return Seed(BernoulliSource(support, probability_true, boundary))

    @staticmethod
    def product(fields: tuple[tuple[str, Seed[C]], ...]) -> Seed[C]:
        return Seed(ProductSource(fields))

    @staticmethod
    def intensional(binder: str, construction: RelationExpr) -> Seed[C]:
        return Seed(IntensionalSource(binder, construction))


# ---------------------------------------------------------------------------
# frontiers.py and neighborhoods.py — write and read capability wrappers
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WritableRegion(Generic[C, W]):
    region: Region


@dataclass(frozen=True)
class ReadableRegion(Generic[C, R]):
    region: Region
    shape: tuple[str, ...]


class frontiers:
    @staticmethod
    def literal(loci: tuple[Locus, ...]) -> WritableRegion[C, Locus]:
        return WritableRegion(LiteralRegion(loci))

    @staticmethod
    def everywhere(carrier_name: str) -> WritableRegion[C, Locus]:
        return WritableRegion(AllSupport(carrier_name))

    @staticmethod
    def union(
        regions: tuple[WritableRegion[C, W], ...],
    ) -> WritableRegion[C, W]:
        return WritableRegion(UnionRegion(tuple(item.region for item in regions)))

    @staticmethod
    def fresh_children(
        parents: WritableRegion[C, W],
        namespace: str,
        slots: tuple[str, ...],
    ) -> WritableRegion[C, Locus]:
        return WritableRegion(FreshChildren(parents.region, namespace, slots))


class neighborhoods:
    @staticmethod
    def at_self() -> ReadableRegion[C, V]:
        return ReadableRegion(LiteralRegion((NamedLocus("self"),)), ("self",))

    @staticmethod
    def product(
        fields: tuple[tuple[str, ReadableRegion[C, R]], ...],
    ) -> ReadableRegion[C, tuple[R, ...]]:
        region = ProductRegion(tuple((name, item.region) for name, item in fields))
        return ReadableRegion(region, tuple(name for name, _ in fields))

    @staticmethod
    def global_view(carrier_name: str) -> ReadableRegion[C, tuple[V, ...]]:
        return ReadableRegion(AllSupport(carrier_name), ("support",))

    @staticmethod
    def eca() -> ReadableRegion[BinaryLine, tuple[bool, bool, bool]]:
        offsets = (
            Coordinate((("x", Fraction(-1)),)),
            Coordinate((("x", Fraction(0)),)),
            Coordinate((("x", Fraction(1)),)),
        )
        return ReadableRegion(
            RelativeRegion(LiteralRegion((NamedLocus("active"),)), offsets),
            ("left", "self", "right"),
        )


# ---------------------------------------------------------------------------
# rules.py — closed relations and complete atomic replacements
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LookupRule:
    input_shape: tuple[int, ...]
    outputs: tuple[ExactScalar, ...]


@dataclass(frozen=True)
class OrderedClause:
    condition: RelationExpr
    replacement: RelationExpr


@dataclass(frozen=True)
class OrderedRule:
    clauses: tuple[OrderedClause, ...]


@dataclass(frozen=True)
class ParallelRule:
    parts: tuple["Rule[tuple[ExactScalar, ...], Locus, C]", ...]


@dataclass(frozen=True)
class RelationalRule:
    relation: RelationExpr


@dataclass(frozen=True)
class DistributionRule:
    support: RelationExpr
    exact_weights: tuple[Fraction, ...]


@dataclass(frozen=True)
class DifferentialRule:
    equation: RelationExpr


RuleDescriptor: TypeAlias = (
    LookupRule
    | OrderedRule
    | ParallelRule
    | RelationalRule
    | DistributionRule
    | DifferentialRule
)


@dataclass(frozen=True)
class Rule(Generic[R, W, C]):
    descriptor: RuleDescriptor


class rules:
    @staticmethod
    def table(
        input_shape: tuple[int, ...],
        outputs: tuple[ExactScalar, ...],
    ) -> Rule[R, W, C]:
        return Rule(LookupRule(input_shape, outputs))

    @staticmethod
    def parallel(
        parts: tuple[Rule[tuple[ExactScalar, ...], Locus, C], ...],
    ) -> Rule[tuple[ExactScalar, ...], Locus, C]:
        return Rule(ParallelRule(parts))

    @staticmethod
    def relation(relation: RelationExpr) -> Rule[R, W, C]:
        return Rule(RelationalRule(relation))

    @staticmethod
    def elementary(
        number: int,
    ) -> Rule[tuple[bool, bool, bool], Locus, BinaryLine]:
        if not 0 <= number <= 255:
            raise ValueError("elementary rule number must be in 0..255")
        outputs = tuple(bool((number >> index) & 1) for index in range(8))
        return Rule(LookupRule((2, 2, 2), outputs))


# ---------------------------------------------------------------------------
# program.py — exactly five stored fields
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SimpleProgram(Generic[C, V, W, R]):
    seed: Seed[C]
    alphabet: Alphabet[V]
    frontier: WritableRegion[C, W]
    neighborhood: ReadableRegion[C, R]
    rule: Rule[R, W, C]


# ---------------------------------------------------------------------------
# catalog/ — whole-program constructors and explicit aliases
# ---------------------------------------------------------------------------


class catalog:
    @staticmethod
    def elementary_cellular_automaton(
        rule: int = 30,
        width: int = 79,
    ) -> SimpleProgram[
        BinaryLine,
        bool,
        Locus,
        tuple[bool, bool, bool],
    ]:
        support = AllSupport(f"binary-line:{width}")
        return SimpleProgram(
            seed=seeds.bernoulli(
                support=support,
                probability_true=Fraction(1, 2),
                boundary=Boundary("fixed", False),
            ),
            alphabet=alphabets.boolean(),
            frontier=frontiers.everywhere("binary-line"),
            neighborhood=neighborhoods.eca(),
            rule=rules.elementary(rule),
        )

    @staticmethod
    def eca(
        rule: int = 30,
        width: int = 79,
    ) -> SimpleProgram[
        BinaryLine,
        bool,
        Locus,
        tuple[bool, bool, bool],
    ]:
        """Explicit alias; it returns the same ordinary five-field value."""

        return catalog.elementary_cellular_automaton(rule=rule, width=width)


# ---------------------------------------------------------------------------
# Rule/Application results used by the one universal application law
# ---------------------------------------------------------------------------


class Progress(Enum):
    ADVANCED = "advanced"
    QUIESCENT = "quiescent"


class Continuation(Enum):
    CONTINUE = "continue"
    STOP = "stop"


class NoSuccessorKind(Enum):
    TERMINAL = "terminal"
    UNDEFINED = "undefined"
    DECLARED_FAILURE = "declared-failure"
    DIVERGENT = "divergent"


class Cardinality(Enum):
    EXACTLY_ZERO = "exactly-zero"
    EXACTLY_ONE = "exactly-one"
    MANY = "many"
    UNDETERMINED = "undetermined"


@dataclass(frozen=True)
class Preserve:
    """Retain one existing writable capability."""


@dataclass(frozen=True)
class Replace(Generic[V]):
    payload: V


@dataclass(frozen=True)
class Delete:
    """Remove one existing writable capability."""


@dataclass(frozen=True)
class Absent:
    """Do not instantiate one fresh writable capability."""


@dataclass(frozen=True)
class Create(Generic[V]):
    payload: V


@dataclass(frozen=True)
class ExistingDisposition(Generic[W, V]):
    target: W
    disposition: Preserve | Replace[V] | Delete


@dataclass(frozen=True)
class FreshDisposition(Generic[W, V]):
    target: W
    disposition: Absent | Create[V]


@dataclass(frozen=True)
class TotalDisposition(Generic[W, V]):
    existing: tuple[ExistingDisposition[W, V], ...]
    fresh: tuple[FreshDisposition[W, V], ...]


@dataclass(frozen=True)
class Derivation(Generic[W, V]):
    replacement: TotalDisposition[W, V]
    progress: Progress
    continuation: Continuation
    witness: str
    provenance: tuple[str, ...]


@dataclass(frozen=True)
class NoSuccessor:
    outcome: NoSuccessorKind
    reason: str
    witness: str
    provenance: tuple[str, ...]


@dataclass(frozen=True)
class FiniteSupport(Generic[A]):
    atoms: tuple[A, ...]
    cardinality: Cardinality
    completeness_certificate: str


@dataclass(frozen=True)
class IntensionalSupport(Generic[A]):
    relation: RelationExpr
    cardinality: Cardinality
    soundness_and_coverage_certificate: str


@dataclass(frozen=True)
class OutcomeSpace(Generic[A]):
    support: FiniteSupport[A] | IntensionalSupport[A]
    probability_law: tuple[Fraction, ...] | None = None


@dataclass(frozen=True)
class Complete(Generic[P]):
    payload: P


@dataclass(frozen=True)
class Fault:
    phase: str
    reason: str
    evidence: tuple[str, ...]


@dataclass(frozen=True)
class Rejected:
    fault: Fault


@dataclass(frozen=True)
class ApplicationInput(Generic[C]):
    configuration: C
    trace_lineage: tuple[str, ...]


@dataclass(frozen=True)
class AppliedDerivation(Generic[C, W, V]):
    successor: C
    source: Derivation[W, V]
    fresh_bindings: tuple[tuple[W, Locus], ...]
    output_trace_lineage: tuple[str, ...]


@dataclass(frozen=True)
class AppliedNoSuccessor:
    source: NoSuccessor
    output_trace_lineage: tuple[str, ...]


@dataclass(frozen=True)
class SuccessorGroup(Generic[C, W, V]):
    successor: C
    derivation_fiber: tuple[AppliedDerivation[C, W, V], ...]


@dataclass(frozen=True)
class ApplicationComplete(Generic[C, W, V]):
    source_outcomes: OutcomeSpace[Derivation[W, V] | NoSuccessor]
    applied_atoms: tuple[AppliedDerivation[C, W, V] | AppliedNoSuccessor, ...]
    successor_groups: tuple[SuccessorGroup[C, W, V], ...]
    outcome_cardinality: Cardinality
    derivation_cardinality: Cardinality
    successor_cardinality: Cardinality
    evidence: tuple[str, ...]


ApplicationResult: TypeAlias = Complete[ApplicationComplete[C, W, V]] | Rejected


def apply(
    program: SimpleProgram[C, V, W, R],
    application_input: ApplicationInput[C],
) -> ApplicationResult[C, W, V]:
    """One family-blind application, shown as the five normative phases."""

    compatibility = require_valid_program(program)
    snapshot = freeze_and_validate_input(
        application_input,
        compatibility.configuration_contract,
        program.alphabet,
    )
    writable = resolve_writable(program.frontier, snapshot)
    readable = resolve_readable(program.neighborhood, snapshot)
    reconstruction = derive_closed_reconstruction(writable, compatibility)
    require_same_snapshot_and_join(snapshot, readable, writable, compatibility)

    rule_result = denote(program.rule, readable, writable)
    if isinstance(rule_result, Rejected):
        return rule_result

    # Phase 1: validate the entire sound-and-covering Rule outcome space.
    validated = validate_complete_rule_space(
        rule_result.payload,
        program.rule,
        readable,
        writable,
        compatibility,
        program.alphabet,
    )

    # Phase 2: bind every fresh identity from semantic scope and witness.
    fresh_space = bind_all_fresh(
        validated,
        snapshot.configuration_identity,
        canonical_identity(program.rule),
        writable,
    )

    # Phase 3: reconstruct every alternative from the same old snapshot.
    candidates = reconstruct_all(
        reconstruction,
        snapshot.configuration,
        validated,
        fresh_space,
    )

    # Phase 4: validate all successors before any becomes authoritative.
    applied_atoms = validate_all_successors(
        candidates,
        compatibility.configuration_contract,
        program.alphabet,
        application_input.trace_lineage,
    )

    # Phase 5: retain witnesses, then quotient and push measures forward.
    groups = group_semantically_equal_successors(applied_atoms, compatibility)
    measures = derive_unrenormalized_measure_views(validated, applied_atoms, groups)
    return build_complete_application(validated, applied_atoms, groups, measures)


# ---------------------------------------------------------------------------
# rollout.py — auxiliary traversal over apply, never a second executor
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RolloutRequest:
    steps: int
    replay_key: str | None = None


@dataclass(frozen=True)
class TraceLeaf(Generic[C]):
    configuration: C
    trace_lineage: tuple[str, ...]
    continuing: bool


@dataclass(frozen=True)
class Episode(Generic[C, W, V]):
    applications: tuple[ApplicationResult[C, W, V], ...]
    leaves: tuple[TraceLeaf[C], ...]
    truncated: bool


def rollout(
    program: SimpleProgram[C, V, W, R],
    steps: int,
    *,
    replay_key: str | None = None,
) -> Episode[C, W, V]:
    """Realize the Seed, then repeatedly traverse only through ``apply``."""

    request = RolloutRequest(steps=steps, replay_key=replay_key)
    leaves = realize_seed_with_replay(program.seed, request.replay_key)
    applications: list[ApplicationResult[C, W, V]] = []

    for _ in range(request.steps):
        next_leaves: list[TraceLeaf[C]] = []
        for leaf in leaves:
            if not leaf.continuing:
                next_leaves.append(leaf)
                continue
            result = apply(
                program,
                ApplicationInput(leaf.configuration, leaf.trace_lineage),
            )
            applications.append(result)
            next_leaves.extend(expand_continuing_derivation_fibers(result))
        leaves = tuple(next_leaves)

    return Episode(
        applications=tuple(applications),
        leaves=leaves,
        truncated=any(leaf.continuing for leaf in leaves),
    )


# ---------------------------------------------------------------------------
# serialization.py and __init__.py — canonical payload and public spelling
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ProgramPayload(Generic[C, V, W, R]):
    seed: Seed[C]
    alphabet: Alphabet[V]
    frontier: WritableRegion[C, W]
    neighborhood: ReadableRegion[C, R]
    rule: Rule[R, W, C]


class serialization:
    @staticmethod
    def encode_program(program: SimpleProgram[C, V, W, R]) -> bytes:
        payload = ProgramPayload(
            seed=program.seed,
            alphabet=program.alphabet,
            frontier=program.frontier,
            neighborhood=program.neighborhood,
            rule=program.rule,
        )
        return encode_closed_versioned_node("ca.simple-program", 1, payload)

    @staticmethod
    def decode_program(data: bytes) -> SimpleProgram[C, V, W, R] | Rejected:
        payload = decode_closed_versioned_node("ca.simple-program", 1, data)
        if isinstance(payload, Rejected):
            return payload
        return require_valid_program(
            SimpleProgram(
                seed=payload.seed,
                alphabet=payload.alphabet,
                frontier=payload.frontier,
                neighborhood=payload.neighborhood,
                rule=payload.rule,
            )
        ).program


# ``ca.__init__`` re-exports module namespaces plus only these conveniences:
# ``SimpleProgram``, ``apply``, and the auxiliary ``rollout`` boundary.
# Whole-program semantic names remain under ``ca.catalog``.


def public_surface_example() -> Episode[BinaryLine, Locus, bool]:
    program = SimpleProgram(
        seed=seeds.bernoulli(
            support=AllSupport("binary-line:79"),
            probability_true=Fraction(1, 2),
            boundary=Boundary("fixed", False),
        ),
        alphabet=alphabets.boolean(),
        frontier=frontiers.everywhere("binary-line"),
        neighborhood=neighborhoods.eca(),
        rule=rules.elementary(30),
    )

    same_program = catalog.eca(rule=30, width=79)
    assert serialization.encode_program(program) == serialization.encode_program(
        same_program
    )
    return rollout(same_program, steps=100, replay_key="example-0001")
