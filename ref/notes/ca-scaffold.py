"""Compact, code-shaped walkthrough of the five-field architecture.

This is reference material, not package runtime code:

    loci -> component algebras -> SimpleProgram -> catalog -> apply -> rollout

Every semantic object is closed structural data.  There are no callbacks,
ambient random generators, family registries, update policies, or alternate
executors.
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
Exact: TypeAlias = bool | int | Fraction | str


# --- loci.py: closed identities and region variants ------------------------
class LocusKind(Enum):
    COORDINATE = "coordinate"
    NAMED = "named"
    OCCURRENCE = "occurrence"
    GRAPH_ELEMENT = "graph-element"
    FIELD_POINT = "field-point"
    FRESH = "fresh"
@dataclass(frozen=True)
class Locus:
    kind: LocusKind
    scope: str
    path: tuple[Exact, ...]
class SelectorPrimitive(Enum):
    PREDICATE = "selector.predicate"
    TRANSFORM = "selector.transform"
    MEMBERSHIP = "selector.membership"
@dataclass(frozen=True)
class SelectorExpr:
    primitive: SelectorPrimitive
    arguments: tuple[Exact | Locus | "SelectorExpr", ...]
class RegionKind(Enum):
    LITERAL = "literal"
    ALL_SUPPORT = "all-support"
    RELATIVE = "relative"
    PRODUCT = "product"
    UNION = "union"
    FRESH_CHILDREN = "fresh-children"
    INTENSIONAL = "intensional"
@dataclass(frozen=True)
class Region:
    kind: RegionKind
    name: str | None = None
    loci: tuple[Locus, ...] = ()
    parts: tuple["Region", ...] = ()
    offsets: tuple[Locus, ...] = ()
    relation: SelectorExpr | None = None

class loci:
    """A raw Region grants neither read nor write authority."""
    @staticmethod
    def named(name: str) -> Locus:
        return Locus(LocusKind.NAMED, "configuration", (name,))
    @staticmethod
    def coordinate(axis: str, value: int) -> Locus:
        return Locus(LocusKind.COORDINATE, "coordinates", (axis, value))
    @staticmethod
    def all_support(carrier: str) -> Region:
        return Region(RegionKind.ALL_SUPPORT, name=carrier)
    @staticmethod
    def relative(anchors: Region, offsets: tuple[Locus, ...]) -> Region:
        return Region(RegionKind.RELATIVE, parts=(anchors,), offsets=offsets)
    @staticmethod
    def union(parts: tuple[Region, ...]) -> Region:
        return Region(RegionKind.UNION, parts=parts)
    @staticmethod
    def intensional(binder: str, relation: SelectorExpr) -> Region:
        return Region(RegionKind.INTENSIONAL, name=binder, relation=relation)


# --- Component modules: primitives -> compounds -> useful presets ----------

# Each sealed node variant is owned by its component module.  `Expr` is only
# the compact cross-owner wire union used by this walkthrough, not a loci-owned
# god enum or an execution dispatch registry.
class AlphabetPrimitive(Enum):
    ENUM = "alphabet.enum"
    PRODUCT = "alphabet.product"
class SeedPrimitive(Enum):
    BERNOULLI = "seed.bernoulli"
class FrontierPrimitive(Enum):
    CAPABILITY_SPACE = "frontier.capability-space"
    TARGET_CONTRACT = "frontier.target-contract"
    FRESH_NAMESPACE = "frontier.fresh-namespace"
class NeighborhoodPrimitive(Enum):
    OBSERVATION_SPACE = "neighborhood.observation-space"
    JOIN_SHAPE = "neighborhood.join-shape"
class RulePrimitive(Enum):
    PRODUCT = "rule.product"
    LOOKUP = "rule.lookup"
    PARALLEL = "rule.parallel"
    RELATION = "rule.relation"
    DISTRIBUTION = "rule.distribution"
    DIFFERENTIAL = "rule.differential"
class RuleResultPrimitive(Enum):
    TOTAL_DISPOSITION = "rule-result.total-disposition"
    FINITE_SUPPORT = "rule-result.finite-support"
    INTENSIONAL_SUPPORT = "rule-result.intensional-support"
    CARDINALITY = "rule-result.cardinality"
    PROBABILITY_LAW = "rule-result.probability-law"
    WITNESS = "rule-result.witness"
    MEASURE = "rule-result.measure"
class ProgramResultPrimitive(Enum):
    TRACE_LINEAGE = "program-result.trace-lineage"
    APPLIED_DERIVATION = "program-result.applied-derivation"
    APPLIED_NO_SUCCESSOR = "program-result.applied-no-successor"
    SUCCESSOR_GROUP = "program-result.successor-group"
    APPLICATION_EVIDENCE = "program-result.application-evidence"
    RAW_TRACE = "program-result.raw-trace"
SemanticPrimitive: TypeAlias = (
    AlphabetPrimitive
    | SeedPrimitive
    | FrontierPrimitive
    | NeighborhoodPrimitive
    | RulePrimitive
    | RuleResultPrimitive
    | ProgramResultPrimitive
)
@dataclass(frozen=True)
class Expr:
    primitive: SemanticPrimitive
    arguments: tuple[Exact | Locus | SelectorExpr | "Expr", ...]
@dataclass(frozen=True)
class Alphabet(Generic[V]):
    descriptor: Expr
@dataclass(frozen=True)
class Boundary:
    policy: str
    exterior: Exact | None = None
@dataclass(frozen=True)
class BinaryLine:
    values: tuple[bool, ...]
    boundary: Boundary
    support_identity: str
@dataclass(frozen=True)
class ExactSeed(Generic[C]):
    configuration: C
@dataclass(frozen=True)
class SourceExpr:
    construction: Expr
    support: Region
    boundary: Boundary | None = None
@dataclass(frozen=True)
class Seed(Generic[C]):
    source: ExactSeed[C] | SourceExpr
@dataclass(frozen=True)
class WritableRegion(Generic[C, W]):
    descriptor: Region
@dataclass(frozen=True)
class ReadableRegion(Generic[C, R]):
    descriptor: Region
    result_shape: tuple[str, ...]
@dataclass(frozen=True)
class WritableEnvelope(Generic[A]):
    """One resolved envelope whose member capabilities are structurally keyed."""

    snapshot_binding: Expr
    capabilities: Expr
    target_contracts_and_fresh_namespaces: Expr
@dataclass(frozen=True)
class IndexedView(Generic[A]):
    """One resolved identity-indexed view whose entries have shape A."""

    snapshot_binding: Expr
    observations_and_structure: Expr
    declared_join_shape: Expr
@dataclass(frozen=True)
class Rule(Generic[R, W, C]):
    descriptor: Expr

class alphabets:
    @staticmethod
    def boolean() -> Alphabet[bool]:
        return Alphabet(Expr(AlphabetPrimitive.ENUM, (False, True)))
    @staticmethod
    def product(parts: tuple[Alphabet[Exact], ...]) -> Alphabet[tuple[Exact, ...]]:
        descriptors = tuple(part.descriptor for part in parts)
        return Alphabet(Expr(AlphabetPrimitive.PRODUCT, descriptors))

class seeds:
    @staticmethod
    def exact(configuration: C) -> Seed[C]:
        return Seed(ExactSeed(configuration))
    @staticmethod
    def bernoulli(
        support: Region,
        probability_true: Fraction,
        boundary: Boundary,
    ) -> Seed[BinaryLine]:
        construction = Expr(SeedPrimitive.BERNOULLI, (probability_true,))
        return Seed(SourceExpr(construction, support, boundary))

class frontiers:
    @staticmethod
    def everywhere() -> WritableRegion[C, WritableEnvelope[Locus]]:
        return WritableRegion(loci.all_support("current-carrier"))
    @staticmethod
    def union(
        parts: tuple[WritableRegion[C, WritableEnvelope[A]], ...],
    ) -> WritableRegion[C, WritableEnvelope[A]]:
        descriptors = tuple(part.descriptor for part in parts)
        return WritableRegion(loci.union(descriptors))

class neighborhoods:
    @staticmethod
    def product(
        fields: tuple[tuple[str, ReadableRegion[C, R]], ...],
    ) -> ReadableRegion[C, tuple[R, ...]]:
        named_parts = tuple(
            Region(RegionKind.PRODUCT, name=name, parts=(item.descriptor,))
            for name, item in fields
        )
        return ReadableRegion(
            Region(RegionKind.PRODUCT, parts=named_parts),
            tuple(name for name, _ in fields),
        )
    @staticmethod
    def eca() -> ReadableRegion[
        BinaryLine,
        IndexedView[tuple[bool, bool, bool]],
    ]:
        anchor = Region(RegionKind.LITERAL, loci=(loci.named("site"),))
        offsets = tuple(loci.coordinate("x", value) for value in (-1, 0, 1))
        return ReadableRegion(
            loci.relative(anchor, offsets),
            ("left", "self", "right"),
        )

class rules:
    @staticmethod
    def table(input_shape: tuple[int, ...], outputs: tuple[Exact, ...]) -> Rule[R, W, C]:
        shape = Expr(RulePrimitive.PRODUCT, input_shape)
        return Rule(Expr(RulePrimitive.LOOKUP, (shape, *outputs)))
    @staticmethod
    def parallel(parts: tuple[Rule[R, W, C], ...]) -> Rule[R, W, C]:
        descriptors = tuple(part.descriptor for part in parts)
        return Rule(Expr(RulePrimitive.PARALLEL, descriptors))
    @staticmethod
    def elementary(number: int) -> Rule[
        IndexedView[tuple[bool, bool, bool]],
        WritableEnvelope[Locus],
        BinaryLine,
    ]:
        if not 0 <= number <= 255:
            raise ValueError("elementary rule number must be in 0..255")
        outputs = tuple(bool((number >> index) & 1) for index in range(8))
        return rules.table((2, 2, 2), outputs)


# --- program.py: exactly five stored values --------------------------------
@dataclass(frozen=True)
class SimpleProgram(Generic[C, V, W, R]):
    seed: Seed[C]
    alphabet: Alphabet[V]
    frontier: WritableRegion[C, W]
    neighborhood: ReadableRegion[C, R]
    rule: Rule[R, W, C]

    def __post_init__(self) -> None:
        require_compatible_five_fields(self)


# --- catalog/automata.py: canonical family, preset, and explicit alias ------
class automata:
    @staticmethod
    def synchronous_local_state_transform(
        *,
        seed: Seed[C],
        alphabet: Alphabet[V],
        frontier: WritableRegion[C, W],
        neighborhood: ReadableRegion[C, R],
        rule: Rule[R, W, C],
    ) -> SimpleProgram[C, V, W, R]:
        """Canonical F053 constructor; production code validates its profile."""

        return SimpleProgram(
            seed=seed,
            alphabet=alphabet,
            frontier=frontier,
            neighborhood=neighborhood,
            rule=rule,
        )
    @staticmethod
    def eca(
        *,
        rule: int = 30,
        width: int = 79,
    ) -> SimpleProgram[
        BinaryLine,
        bool,
        WritableEnvelope[Locus],
        IndexedView[tuple[bool, bool, bool]],
    ]:
        carrier = f"binary-line:{width}"
        return automata.synchronous_local_state_transform(
            seed=seeds.bernoulli(
                loci.all_support(carrier),
                Fraction(1, 2),
                Boundary("fixed", False),
            ),
            alphabet=alphabets.boolean(),
            frontier=frontiers.everywhere(),
            neighborhood=neighborhoods.eca(),
            rule=rules.elementary(rule),
        )
    @staticmethod
    def elementary_cellular_automaton(
        *,
        rule: int = 30,
        width: int = 79,
    ) -> SimpleProgram[
        BinaryLine,
        bool,
        WritableEnvelope[Locus],
        IndexedView[tuple[bool, bool, bool]],
    ]:
        """True alternate spelling of the ``eca`` preset."""

        return automata.eca(rule=rule, width=width)


# catalog/entries.py is immutable provenance/navigation metadata only. Stage 5
# supplies exact IDs, names, and relations; it never stores callables.
class entries:
    """Stage-5-populated immutable metadata namespace."""


# `substitua.py`, `machina.py`, `media.py`, `criteria.py`, and `dynamica.py`
# own their corresponding whole-program constructors in exactly the same way.
# catalog/__init__.py re-exports unique names from all six category modules.
class catalog:
    automata = automata
    entries = entries
    synchronous_local_state_transform = staticmethod(
        automata.synchronous_local_state_transform
    )
    eca = staticmethod(automata.eca)
    elementary_cellular_automaton = staticmethod(
        automata.elementary_cellular_automaton
    )


# --- rules.py/program.py: results and one family-blind apply operation ------
class Progress(Enum):
    ADVANCED = "advanced"
    QUIESCENT = "quiescent"
class NoSuccessorOutcome(Enum):
    TERMINAL = "terminal"
    UNDEFINED = "undefined"
    DECLARED_FAILURE = "declared-failure"
    DIVERGENT = "divergent"
@dataclass(frozen=True)
class TotalDisposition(Generic[W]):
    """Closed Preserve/Replace/Delete and Absent/Create meaning over all W."""

    descriptor: Expr
    totality_evidence: Expr
CardinalityClaim: TypeAlias = Expr
Witness: TypeAlias = Expr
Provenance: TypeAlias = tuple[str, ...]
@dataclass(frozen=True)
class SupportSpace(Generic[A]):
    """Closed tagged Finite[A] | Intensional[A], with cardinality/coverage."""

    descriptor: Expr
ProbabilityLaw: TypeAlias = Expr
@dataclass(frozen=True)
class OutcomeSpace(Generic[A]):
    support: SupportSpace[A]
    probability_law: ProbabilityLaw | None
@dataclass(frozen=True)
class Continue:
    """Continue this witnessed derivation in rollout."""
@dataclass(frozen=True)
class Stop:
    reason: Expr
Continuation: TypeAlias = Continue | Stop
@dataclass(frozen=True)
class Derivation(Generic[W]):
    replacement: TotalDisposition[W]
    progress: Progress
    continuation: Continuation
    witness: Witness
    provenance: Provenance
@dataclass(frozen=True)
class NoSuccessor:
    outcome: NoSuccessorOutcome
    reason: Expr
    witness: Witness
    provenance: Provenance
RuleAtom: TypeAlias = Derivation[W] | NoSuccessor
@dataclass(frozen=True)
class RuleFault:
    phase: str
    reason: str
    evidence: tuple[str, ...]
@dataclass(frozen=True)
class RuleRejected:
    fault: RuleFault
@dataclass(frozen=True)
class RuleComplete(Generic[C, W]):
    outcome_space: OutcomeSpace[RuleAtom[W]]
RuleResult: TypeAlias = RuleComplete[C, W] | RuleRejected
@dataclass(frozen=True)
class TraceLineage:
    descriptor: Expr
@dataclass(frozen=True)
class ApplicationInput(Generic[C]):
    configuration: C
    trace_lineage: TraceLineage | None = None

# These compact shells retain the complete closed records defined in
# architecture.md rather than restating every nested field here.
@dataclass(frozen=True)
class AppliedDerivation(Generic[C, W]):
    descriptor: Expr
@dataclass(frozen=True)
class AppliedNoSuccessor:
    descriptor: Expr
AppliedAtom: TypeAlias = AppliedDerivation[C, W] | AppliedNoSuccessor
@dataclass(frozen=True)
class SuccessorGroup(Generic[C, W]):
    descriptor: Expr
@dataclass(frozen=True)
class MeasureAbsent:
    """No source probability law."""
@dataclass(frozen=True)
class MeasureAvailable:
    measure: Expr
@dataclass(frozen=True)
class MeasureUnavailable:
    reason: Expr
    retained_source_law_and_mapping_evidence: Expr
MeasureView: TypeAlias = MeasureAbsent | MeasureAvailable | MeasureUnavailable
@dataclass(frozen=True)
class ApplicationComplete(Generic[C, W]):
    source_outcomes: OutcomeSpace[RuleAtom[W]]
    applied_atoms: SupportSpace[AppliedAtom[C, W]]
    no_successor_partition: SupportSpace[AppliedNoSuccessor]
    outcome_atom_cardinality: CardinalityClaim
    derivation_cardinality: CardinalityClaim
    successor_cardinality: CardinalityClaim
    successor_quotient_with_derivation_fibers: SupportSpace[
        SuccessorGroup[C, W]
    ]
    applied_atom_measure: MeasureView
    successor_submeasure: MeasureView
    no_successor_submeasure: MeasureView
    evidence: Expr
@dataclass(frozen=True)
class ApplicationFault:
    phase: str
    reason: str
    evidence: tuple[str, ...]
@dataclass(frozen=True)
class ApplicationRejected:
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
    normalized_input = normalize_application_input(input)
    # The closed helper executes APPLICATION_PHASES in order.  Any phase fault
    # becomes ApplicationRejected and prevents every later phase.  After Rule
    # denotation its five passes are: validate the complete space, bind fresh
    # identities, reconstruct all alternatives, validate all successors, then
    # retain witnesses while forming quotient and measure views.  It never
    # switches on family, carrier, catalog entry, or Rule tag.
    return execute_closed_application_phases(
        program,
        normalized_input,
        phase_order=APPLICATION_PHASES,
    )


# --- program.py: public rollout operation and types, derived from apply -----

# Goal 7 folds the current rollout module here or into private helpers.  There
# is no target public ``ca.rollout`` submodule to shadow the root callable.
@dataclass(frozen=True)
class ContinuingLeaf(Generic[C]):
    configuration: C
    trace_lineage: TraceLineage
@dataclass(frozen=True)
class ClosedLeaf(Generic[C, W]):
    final_configuration: C | None
    source: AppliedAtom[C, W]
@dataclass(frozen=True)
class RawTrace(Generic[C, W]):
    roots: OutcomeSpace[C]
    applications: SupportSpace[ApplicationComplete[C, W]]
    derivation_edges: SupportSpace[AppliedAtom[C, W]]
    lineage_graph: Expr
    evidence: Expr
@dataclass(frozen=True)
class RolloutComplete(Generic[C, W]):
    raw_trace: RawTrace[C, W]
    closed_leaves: SupportSpace[ClosedLeaf[C, W]]
class TruncationCause(Enum):
    DEPTH_BOUND = "depth-bound"
    RESOURCE_EXHAUSTED = "resource-exhausted"
    CANCELLED = "cancelled"
    PRUNED = "pruned"
@dataclass(frozen=True)
class RolloutTruncated(Generic[C, W]):
    raw_trace: RawTrace[C, W]
    continuing_leaves: SupportSpace[ContinuingLeaf[C]]
    cause: TruncationCause
@dataclass(frozen=True)
class RolloutFault:
    reason: str
@dataclass(frozen=True)
class RolloutRejected:
    fault: RolloutFault
RolloutResult: TypeAlias = (
    RolloutComplete[C, W]
    | RolloutTruncated[C, W]
    | RolloutRejected
)
ReplayKey: TypeAlias = Exact | Expr
def rollout(
    program: SimpleProgram[C, V, W, R],
    *,
    steps: int,
    initial: C | None = None,
    replay_key: ReplayKey | None = None,
) -> RolloutResult[C, W]:
    if steps < 0:
        return RolloutRejected(RolloutFault("steps must be nonnegative"))
    initial_space = normalize_initial_or_realize_seed_closed(
        program.seed,
        initial=initial,
        replay_key=replay_key,
    )
    if isinstance(initial_space, RolloutRejected):
        return initial_space

    # This closed traversal's only transition is ``apply(program, input)``.
    # It lifts apply over finite or intensional continuing fibers without
    # enumeration, maps ApplicationRejected to RolloutRejected, preserves the
    # raw graph, and derives replay subkeys for any requested Rule-law draw.
    return traverse_closed_by_repeated_apply(
        program,
        initial_space=initial_space,
        depth_bound=steps,
        replay_key=replay_key,
    )


# --- serialization.py and ca.__init__: expanded payload, small root spelling
@dataclass(frozen=True)
class ProgramPayload(Generic[C, V, W, R]):
    seed: Seed[C]
    alphabet: Alphabet[V]
    frontier: WritableRegion[C, W]
    neighborhood: ReadableRegion[C, R]
    rule: Rule[R, W, C]
@dataclass(frozen=True)
class DecodeFault:
    phase: str
    reason: str
    evidence: tuple[str, ...]
@dataclass(frozen=True)
class DecodeRejected:
    fault: DecodeFault
@dataclass(frozen=True)
class Decoded(Generic[P]):
    value: P
DecodeResult: TypeAlias = Decoded[P] | DecodeRejected

class serialization:
    @staticmethod
    def dumps(program: SimpleProgram[C, V, W, R]) -> bytes:
        validated_program = require_valid_program_for_encoding(program)
        payload = ProgramPayload(
            validated_program.seed,
            validated_program.alphabet,
            validated_program.frontier,
            validated_program.neighborhood,
            validated_program.rule,
        )
        return encode_closed_versioned_node("ca.simple-program", 1, payload)
    @staticmethod
    def loads(
        data: bytes,
    ) -> DecodeResult[SimpleProgram[C, V, W, R]]:
        decoded_payload = decode_closed_versioned_node("ca.simple-program", 1, data)
        if isinstance(decoded_payload, DecodeRejected):
            return decoded_payload
        validated_payload = validate_decoded_program_payload(
            decoded_payload.value
        )
        if isinstance(validated_payload, DecodeRejected):
            return validated_payload
        payload = validated_payload.value
        program = SimpleProgram(
            payload.seed,
            payload.alphabet,
            payload.frontier,
            payload.neighborhood,
            payload.rule,
        )
        return Decoded(program)


# ``ca.__init__`` exposes component/catalog namespaces and only the root
# conveniences ``SimpleProgram``, ``apply``, and ``rollout``.  Detailed public
# application/rollout records remain under ``ca.program``; there is no
# competing rollout module:
#
#     ca.neighborhoods.eca()  -> ReadableRegion
#     ca.catalog.eca()        -> SimpleProgram
def public_surface_example() -> RolloutResult[
    BinaryLine,
    WritableEnvelope[Locus],
]:
    program = catalog.eca(rule=30, width=79)
    encoded = serialization.dumps(program)
    decoded = serialization.loads(encoded)
    if isinstance(decoded, DecodeRejected):
        raise ValueError(decoded.fault.reason)
    return rollout(decoded.value, steps=100, replay_key="example-0001")
