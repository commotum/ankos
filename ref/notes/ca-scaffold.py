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

class Primitive(Enum):
    ENUM = "enum"
    PRODUCT = "product"
    BERNOULLI = "bernoulli"
    LOOKUP = "lookup"
    PARALLEL = "parallel"
    RELATION = "relation"
    DISTRIBUTION = "distribution"
    DIFFERENTIAL = "differential"

@dataclass(frozen=True)
class Expr:
    """One recognized, versioned node in a closed semantic AST."""

    primitive: Primitive
    arguments: tuple[Exact | Locus | "Expr", ...]

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
    relation: Expr | None = None


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


# --- Component modules: primitives -> compounds -> useful presets ----------

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
class Rule(Generic[R, W, C]):
    descriptor: Expr


class alphabets:
    @staticmethod
    def boolean() -> Alphabet[bool]:
        return Alphabet(Expr(Primitive.ENUM, (False, True)))

    @staticmethod
    def product(parts: tuple[Alphabet[Exact], ...]) -> Alphabet[tuple[Exact, ...]]:
        descriptors = tuple(part.descriptor for part in parts)
        return Alphabet(Expr(Primitive.PRODUCT, descriptors))


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
        construction = Expr(Primitive.BERNOULLI, (probability_true,))
        return Seed(SourceExpr(construction, support, boundary))


class frontiers:
    @staticmethod
    def everywhere(carrier: str) -> WritableRegion[C, Locus]:
        return WritableRegion(loci.all_support(carrier))

    @staticmethod
    def union(parts: tuple[WritableRegion[C, W], ...]) -> WritableRegion[C, W]:
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
    def eca() -> ReadableRegion[BinaryLine, tuple[bool, bool, bool]]:
        anchor = Region(RegionKind.LITERAL, loci=(loci.named("site"),))
        offsets = tuple(loci.coordinate("x", value) for value in (-1, 0, 1))
        return ReadableRegion(
            loci.relative(anchor, offsets),
            ("left", "self", "right"),
        )


class rules:
    @staticmethod
    def table(input_shape: tuple[int, ...], outputs: tuple[Exact, ...]) -> Rule[R, W, C]:
        shape = Expr(Primitive.PRODUCT, input_shape)
        return Rule(Expr(Primitive.LOOKUP, (shape, *outputs)))

    @staticmethod
    def parallel(parts: tuple[Rule[R, W, C], ...]) -> Rule[R, W, C]:
        descriptors = tuple(part.descriptor for part in parts)
        return Rule(Expr(Primitive.PARALLEL, descriptors))

    @staticmethod
    def elementary(number: int) -> Rule[tuple[bool, bool, bool], Locus, BinaryLine]:
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


# --- catalog/automata.py: whole-program constructor and explicit alias -----

class automata:
    @staticmethod
    def elementary_cellular_automaton(
        rule: int = 30,
        width: int = 79,
    ) -> SimpleProgram[BinaryLine, bool, Locus, tuple[bool, bool, bool]]:
        return SimpleProgram(
            seed=seeds.bernoulli(
                loci.all_support(f"binary-line:{width}"),
                Fraction(1, 2),
                Boundary("fixed", False),
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
    ) -> SimpleProgram[BinaryLine, bool, Locus, tuple[bool, bool, bool]]:
        return automata.elementary_cellular_automaton(rule=rule, width=width)


# catalog/entries.py is descriptive provenance/navigation, never dispatch.
@dataclass(frozen=True)
class CatalogEntry:
    stable_id: str
    module: str
    canonical_name: str
    aliases: tuple[str, ...]

class entries:
    elementary_cellular_automaton = CatalogEntry(
        stable_id="automata.elementary-cellular-automaton",
        module="automata",
        canonical_name="elementary_cellular_automaton",
        aliases=("eca",),
    )


# `substitua.py`, `machina.py`, `media.py`, `criteria.py`, and `dynamica.py`
# own their corresponding whole-program constructors in exactly the same way.
# catalog/__init__.py re-exports unique names from all six category modules.
class catalog:
    elementary_cellular_automaton = staticmethod(
        automata.elementary_cellular_automaton
    )
    eca = staticmethod(automata.eca)


# --- rules.py/program.py: results and one family-blind apply operation ------

class Disposition(Enum):
    PRESERVE = "preserve"
    REPLACE = "replace"
    DELETE = "delete"
    ABSENT = "absent"
    CREATE = "create"

class Progress(Enum):
    ADVANCED = "advanced"
    QUIESCENT = "quiescent"

class NoSuccessorOutcome(Enum):
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
class Write(Generic[W, V]):
    target: W
    disposition: Disposition
    payload: V | Expr | None

@dataclass(frozen=True)
class Continue:
    """Continue this derivation in rollout."""

@dataclass(frozen=True)
class Stop:
    reason: str

Continuation: TypeAlias = Continue | Stop

@dataclass(frozen=True)
class Derivation(Generic[W, V]):
    replacement: tuple[Write[W, V], ...]
    progress: Progress
    continuation: Continuation
    witness: str

@dataclass(frozen=True)
class NoSuccessor:
    outcome: NoSuccessorOutcome
    reason: str
    witness: str

RuleAtom: TypeAlias = Derivation[W, V] | NoSuccessor

@dataclass(frozen=True)
class OutcomeSpace(Generic[A]):
    finite: tuple[A, ...] | None
    intensional: Expr | None
    cardinality: Cardinality
    soundness_and_coverage: str
    probability_law: tuple[Fraction, ...] | None = None

@dataclass(frozen=True)
class RuleFault:
    phase: str
    reason: str
    evidence: tuple[str, ...]

@dataclass(frozen=True)
class RuleRejected:
    fault: RuleFault

@dataclass(frozen=True)
class RuleComplete(Generic[W, V]):
    outcomes: OutcomeSpace[RuleAtom[W, V]]

RuleResult: TypeAlias = RuleComplete[W, V] | RuleRejected

@dataclass(frozen=True)
class ApplicationInput(Generic[C]):
    configuration: C
    trace_lineage: tuple[str, ...]

@dataclass(frozen=True)
class ApplicationComplete(Generic[C, W, V]):
    source: OutcomeSpace[RuleAtom[W, V]]
    applied_atoms: tuple[tuple[C | None, RuleAtom[W, V], tuple[str, ...]], ...]
    successor_fibers: tuple[tuple[C, tuple[str, ...]], ...]
    cardinalities: tuple[Cardinality, Cardinality, Cardinality]

@dataclass(frozen=True)
class ApplicationFault:
    phase: str
    reason: str
    evidence: tuple[str, ...]

@dataclass(frozen=True)
class ApplicationRejected:
    fault: ApplicationFault

ApplicationResult: TypeAlias = ApplicationComplete[C, W, V] | ApplicationRejected


def apply(
    program: SimpleProgram[C, V, W, R],
    application_input: C | ApplicationInput[C],
) -> ApplicationResult[C, W, V]:
    normalized_input = normalize_application_input(application_input)
    compatibility = require_valid_program(program)
    snapshot = freeze_and_validate_input(normalized_input, compatibility)
    writable = resolve_writable(program.frontier, snapshot)
    readable = resolve_readable(program.neighborhood, snapshot)
    reconstruction = derive_closed_reconstruction(writable, compatibility)
    require_same_snapshot_and_join(snapshot, readable, writable, compatibility)
    rule_result = denote(program.rule, readable, writable)
    if isinstance(rule_result, RuleRejected):
        return ApplicationRejected(
            ApplicationFault(
                phase=f"rule:{rule_result.fault.phase}",
                reason=rule_result.fault.reason,
                evidence=rule_result.fault.evidence,
            )
        )

    # 1. Validate the whole sound-and-covering Rule outcome space.
    validated = validate_complete_rule_space(rule_result.outcomes, program, readable, writable)
    # 2. Bind all fresh identities from semantic input, Rule, and witnesses.
    fresh = bind_all_fresh(validated, snapshot, program.rule, writable)
    # 3. Reconstruct every alternative from the same immutable snapshot.
    candidates = reconstruct_all(reconstruction, snapshot, validated, fresh)
    # 4. Validate all successors before any becomes authoritative.
    applied = validate_all_successors(candidates, program.alphabet, compatibility)
    # 5. Retain witnesses, then quotient and push measures forward.
    groups = group_semantically_equal_successors(applied, compatibility)
    measures = derive_unrenormalized_measure_views(validated, applied, groups)
    return build_complete_application(validated, applied, groups, measures)


# --- program.py: public rollout operation and types, derived from apply -----

# Goal 7 folds the current rollout module here or into private helpers.  There
# is no target public ``ca.rollout`` submodule to shadow the root callable.

@dataclass(frozen=True)
class TraceLeaf(Generic[C]):
    configuration: C
    trace_lineage: tuple[str, ...]
    continuing: bool

@dataclass(frozen=True)
class RolloutResult(Generic[C, W, V]):
    applications: tuple[ApplicationResult[C, W, V], ...]
    leaves: tuple[TraceLeaf[C], ...]
    truncated: bool


def rollout(
    program: SimpleProgram[C, V, W, R],
    *,
    steps: int,
    initial: C | None = None,
    replay_key: str | None = None,
) -> RolloutResult[C, W, V]:
    leaves = normalize_initial_or_realize_seed(
        program.seed,
        initial=initial,
        replay_key=replay_key,
    )
    applications: list[ApplicationResult[C, W, V]] = []
    for _ in range(steps):
        next_leaves: list[TraceLeaf[C]] = []
        for leaf in leaves:
            if leaf.continuing:
                result = apply(program, ApplicationInput(leaf.configuration, leaf.trace_lineage))
                applications.append(result)
                next_leaves.extend(expand_continuing_derivation_fibers(result))
            else:
                next_leaves.append(leaf)
        leaves = tuple(next_leaves)
    return RolloutResult(
        tuple(applications),
        leaves,
        any(leaf.continuing for leaf in leaves),
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
    def encode_program(program: SimpleProgram[C, V, W, R]) -> bytes:
        payload = ProgramPayload(
            program.seed,
            program.alphabet,
            program.frontier,
            program.neighborhood,
            program.rule,
        )
        return encode_closed_versioned_node("ca.simple-program", 1, payload)

    @staticmethod
    def decode_program(
        data: bytes,
    ) -> DecodeResult[SimpleProgram[C, V, W, R]]:
        decoded_payload = decode_closed_versioned_node("ca.simple-program", 1, data)
        if isinstance(decoded_payload, DecodeRejected):
            return decoded_payload
        payload = decoded_payload.value
        program = SimpleProgram(
            payload.seed,
            payload.alphabet,
            payload.frontier,
            payload.neighborhood,
            payload.rule,
        )
        return Decoded(require_valid_program(program).program)


# ``ca.__init__`` exposes component/catalog namespaces and re-exports
# ``SimpleProgram``, ``apply``, ``rollout``, and their public types from
# ``program.py``.  It does not expose a competing rollout module:
#
#     ca.neighborhoods.eca()  -> ReadableRegion
#     ca.catalog.eca()        -> SimpleProgram

def public_surface_example() -> RolloutResult[BinaryLine, Locus, bool]:
    program = catalog.eca(rule=30, width=79)
    encoded = serialization.encode_program(program)
    decoded = serialization.decode_program(encoded)
    if isinstance(decoded, DecodeRejected):
        raise ValueError(decoded.fault.reason)
    return rollout(decoded.value, steps=100, replay_key="example-0001")
