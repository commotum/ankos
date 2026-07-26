"""Closed Rule denotations and their complete result algebra.

``Rule`` is a frozen, versioned relation over one resolved readable view and
one resolved writable envelope.  This module owns the closed expression
interpreter and Rule-side results; it never commits configurations, realizes a
probability law, calls a solver, imports the program/catalog/RNG layers, or
dispatches on a semantic family name.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Generic, Protocol, TypeAlias, TypeVar, cast

from . import alphabets, frontiers, loci, neighborhoods, seeds


C = TypeVar("C")
R = TypeVar("R")
W = TypeVar("W")
A = TypeVar("A")
V = TypeVar("V", bound=alphabets.SemanticValue)

RuleScalar: TypeAlias = bool | int | Fraction | str
RuleRuntimeValue: TypeAlias = (
    alphabets.SemanticValue | tuple["RuleRuntimeValue", ...]
)


# ---------------------------------------------------------------------------
# Closed Rule syntax and compatibility declarations
# ---------------------------------------------------------------------------


class RulePrimitive(Enum):
    """The closed top-level Rule denotation variants."""

    LITERAL = "rule.literal"
    EXPRESSION = "rule.expression"
    RELATION = "rule.relation"
    DISTRIBUTION = "rule.distribution"
    PARALLEL = "rule.parallel"
    DIFFERENTIAL = "rule.differential"


class ExpressionPrimitive(Enum):
    """Small, reusable operations admitted by the Rule interpreter."""

    LITERAL = "expression.literal"
    OBSERVATION = "expression.observation"
    GROUP = "expression.group"
    PROJECT = "expression.project"
    TUPLE = "expression.tuple"
    ADD = "expression.add"
    MULTIPLY = "expression.multiply"
    MODULO = "expression.modulo"
    COUNT = "expression.count"
    GATE = "expression.gate"
    LOOKUP = "expression.lookup"
    EQUAL = "expression.equal"
    ALL = "expression.all"
    ANY = "expression.any"


class GateKind(Enum):
    """Closed predicates over an exact integer aggregate."""

    ANY = "any"
    ALL = "all"
    MAJORITY = "majority"
    AT_LEAST = "at-least"
    AT_MOST = "at-most"
    EXACTLY = "exactly"


@dataclass(frozen=True)
class RuleExpr:
    """One recursively closed, versioned expression AST node."""

    primitive: ExpressionPrimitive
    arguments: tuple[RuleScalar | "RuleExpr", ...] = ()
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported Rule expression version {self.version}")

    @property
    def canonical_identity(self) -> str:
        return self.identity


@dataclass(frozen=True)
class RuleContract:
    """Immutable declarations used for five-field compatibility checking."""

    configuration_contract: loci.CarrierContract
    value_profile: alphabets.ValueProfile
    required_read_shape: neighborhoods.ResultShape
    required_join_shape: neighborhoods.JoinShape
    required_effect_profile: frontiers.EffectProfile
    exactness_profile: seeds.ExactnessProfile = seeds.ExactnessProfile.EXACT
    entropy_interface: seeds.EntropyInterface = seeds.EntropyInterface.NONE
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported Rule contract version {self.version}")
        if not isinstance(self.exactness_profile, seeds.ExactnessProfile):
            raise TypeError("Rule exactness_profile must be seeds.ExactnessProfile")
        if not isinstance(self.entropy_interface, seeds.EntropyInterface):
            raise TypeError("Rule entropy_interface must be seeds.EntropyInterface")


def literal_expr(value: RuleScalar) -> RuleExpr:
    """Build one exact literal expression."""

    return RuleExpr(ExpressionPrimitive.LITERAL, (value,))


def observation(index: int) -> RuleExpr:
    """Read one value from the flat, identity-preserving old-snapshot view."""

    if isinstance(index, bool) or index < 0:
        raise ValueError("observation index must be a non-negative integer")
    return RuleExpr(ExpressionPrimitive.OBSERVATION, (index,))


def group(index: int) -> RuleExpr:
    """Read the ordered values of one group in the current join context."""

    if isinstance(index, bool) or index < 0:
        raise ValueError("group index must be a non-negative integer")
    return RuleExpr(ExpressionPrimitive.GROUP, (index,))


def project(source: RuleExpr, index: int) -> RuleExpr:
    """Project an exact position from a tuple-valued expression."""

    if isinstance(index, bool) or index < 0:
        raise ValueError("projection index must be a non-negative integer")
    return RuleExpr(ExpressionPrimitive.PROJECT, (source, index))


def add(*parts: RuleExpr) -> RuleExpr:
    if not parts:
        raise ValueError("add requires at least one expression")
    return RuleExpr(ExpressionPrimitive.ADD, tuple(parts))


def multiply(*parts: RuleExpr) -> RuleExpr:
    if not parts:
        raise ValueError("multiply requires at least one expression")
    return RuleExpr(ExpressionPrimitive.MULTIPLY, tuple(parts))


def modulo(value: RuleExpr, modulus: int) -> RuleExpr:
    if isinstance(modulus, bool) or modulus <= 0:
        raise ValueError("modulus must be a positive integer")
    return RuleExpr(ExpressionPrimitive.MODULO, (value, modulus))


def count(source: RuleExpr) -> RuleExpr:
    return RuleExpr(ExpressionPrimitive.COUNT, (source,))


def gate(
    source: RuleExpr,
    kind: GateKind,
    *,
    threshold: int = 0,
) -> RuleExpr:
    if isinstance(threshold, bool):
        raise TypeError("gate threshold must be an integer")
    return RuleExpr(
        ExpressionPrimitive.GATE,
        (source, kind.value, int(threshold)),
    )


def lookup(table_values: tuple[RuleScalar, ...], index: RuleExpr) -> RuleExpr:
    """Build an exact finite lookup; concrete table data is stored directly."""

    if not table_values:
        raise ValueError("lookup table cannot be empty")
    table_node = RuleExpr(
        ExpressionPrimitive.TUPLE,
        tuple(literal_expr(value) for value in table_values),
    )
    return RuleExpr(ExpressionPrimitive.LOOKUP, (table_node, index))


# ---------------------------------------------------------------------------
# Evidence, cardinality, total dispositions, and Rule atoms
# ---------------------------------------------------------------------------


class CertificateKind(Enum):
    """Recognized proof/evidence obligations retained by Rule results."""

    SOUNDNESS = "soundness"
    COMPLETENESS = "completeness"
    CARDINALITY = "cardinality"
    TOTALITY = "totality"
    NORMALIZATION = "normalization"
    MEASURABILITY = "measurability"
    DERIVATION = "derivation"
    TERMINALITY = "terminality"
    DIVERGENCE = "divergence"
    CONFORMANCE = "conformance"
    COMPOSITION = "composition"


@dataclass(frozen=True)
class Certificate:
    """Closed structural evidence; never an executable proof callback."""

    kind: CertificateKind
    statement: RuleExpr
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported certificate version {self.version}")

    @property
    def canonical_identity(self) -> str:
        return loci.canonical_identity(self)


def _certificate(kind: CertificateKind, label: str) -> Certificate:
    return Certificate(kind, literal_expr(label))


@dataclass(frozen=True)
class ExactlyZero:
    evidence: Certificate


@dataclass(frozen=True)
class ExactlyOne:
    evidence: Certificate


class InfiniteCardinality(Enum):
    COUNTABLY_INFINITE = "countably-infinite"
    UNCOUNTABLE = "uncountable"


@dataclass(frozen=True)
class Many:
    """An exact finite size of at least two, or one named infinite size."""

    exact_finite_size: int | None
    infinite: InfiniteCardinality | None
    evidence: Certificate

    def __post_init__(self) -> None:
        finite = self.exact_finite_size
        if (finite is None) == (self.infinite is None):
            raise ValueError("Many requires exactly one finite or infinite size")
        if finite is not None and (
            isinstance(finite, bool) or finite < 2
        ):
            raise ValueError("finite Many cardinality must be at least two")


@dataclass(frozen=True)
class Undetermined:
    """Exact relation data whose cardinality is not established."""

    reason: RuleExpr
    obligation: Certificate


Cardinality: TypeAlias = ExactlyZero | ExactlyOne | Many | Undetermined
CardinalityClaim: TypeAlias = Cardinality


def finite_cardinality(size: int) -> Cardinality:
    """Construct the exact cardinality claim for a finite support."""

    if isinstance(size, bool) or size < 0:
        raise ValueError("finite cardinality must be a non-negative integer")
    evidence = _certificate(CertificateKind.CARDINALITY, f"exactly:{size}")
    if size == 0:
        return ExactlyZero(evidence)
    if size == 1:
        return ExactlyOne(evidence)
    return Many(size, None, evidence)


def cardinality_size(cardinality: Cardinality) -> int | None:
    if isinstance(cardinality, ExactlyZero):
        return 0
    if isinstance(cardinality, ExactlyOne):
        return 1
    if isinstance(cardinality, Many):
        return cardinality.exact_finite_size
    return None


class DispositionAction(Enum):
    """The complete action vocabulary over writable capabilities."""

    PRESERVE = "preserve"
    REPLACE = "replace"
    DELETE = "delete"
    ABSENT = "absent"
    CREATE = "create"


@dataclass(frozen=True)
class NoPayload:
    """Payload marker for Preserve/Delete/Absent."""


@dataclass(frozen=True)
class ValuePayload(Generic[V]):
    value: V


DispositionPayload: TypeAlias = NoPayload | ValuePayload[V]


@dataclass(frozen=True)
class Disposition(Generic[W, V]):
    """One explicit action for one existing or fresh writable target."""

    target: W
    action: DispositionAction
    payload: DispositionPayload[V]
    evidence: Certificate
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported disposition version {self.version}")
        has_value = isinstance(self.payload, ValuePayload)
        requires_value = self.action in (
            DispositionAction.REPLACE,
            DispositionAction.CREATE,
        )
        if has_value != requires_value:
            raise ValueError(
                f"{self.action.value} disposition payload does not match its action"
            )

    @property
    def canonical_identity(self) -> str:
        return loci.canonical_identity(self)


@dataclass(frozen=True)
class TotalDisposition(Generic[V]):
    """Total existing/fresh meaning over one resolved writable envelope."""

    existing: tuple[Disposition[loci.Locus, V], ...]
    fresh: tuple[Disposition[loci.FreshReference, V], ...]
    totality_evidence: Certificate
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(
                f"unsupported total-disposition version {self.version}"
            )
        existing_targets = tuple(item.target for item in self.existing)
        fresh_targets = tuple(item.target for item in self.fresh)
        if len(existing_targets) != len(set(existing_targets)):
            raise ValueError("existing dispositions contain duplicate targets")
        if len(fresh_targets) != len(set(fresh_targets)):
            raise ValueError("fresh dispositions contain duplicate targets")
        if any(
            item.action
            not in (
                DispositionAction.PRESERVE,
                DispositionAction.REPLACE,
                DispositionAction.DELETE,
            )
            for item in self.existing
        ):
            raise ValueError("existing target has a fresh-only disposition")
        if any(
            item.action not in (DispositionAction.ABSENT, DispositionAction.CREATE)
            for item in self.fresh
        ):
            raise ValueError("fresh target has an existing-only disposition")

    @property
    def entries(
        self,
    ) -> tuple[
        Disposition[loci.Locus, V] | Disposition[loci.FreshReference, V],
        ...,
    ]:
        return (*self.existing, *self.fresh)

    @property
    def canonical_identity(self) -> str:
        return loci.canonical_identity(self)


def preserve(target: loci.Locus) -> Disposition[loci.Locus, V]:
    return Disposition(
        target,
        DispositionAction.PRESERVE,
        NoPayload(),
        _certificate(CertificateKind.TOTALITY, "existing:preserve"),
    )


def replace(
    target: loci.Locus,
    value: V,
) -> Disposition[loci.Locus, V]:
    return Disposition(
        target,
        DispositionAction.REPLACE,
        ValuePayload(value),
        _certificate(CertificateKind.TOTALITY, "existing:replace"),
    )


def delete(target: loci.Locus) -> Disposition[loci.Locus, V]:
    return Disposition(
        target,
        DispositionAction.DELETE,
        NoPayload(),
        _certificate(CertificateKind.TOTALITY, "existing:delete"),
    )


def absent(
    target: loci.FreshReference,
) -> Disposition[loci.FreshReference, V]:
    return Disposition(
        target,
        DispositionAction.ABSENT,
        NoPayload(),
        _certificate(CertificateKind.TOTALITY, "fresh:absent"),
    )


def create(
    target: loci.FreshReference,
    value: V,
) -> Disposition[loci.FreshReference, V]:
    return Disposition(
        target,
        DispositionAction.CREATE,
        ValuePayload(value),
        _certificate(CertificateKind.TOTALITY, "fresh:create"),
    )


class Progress(Enum):
    ADVANCED = "advanced"
    QUIESCENT = "quiescent"


class NoSuccessorOutcome(Enum):
    TERMINAL = "terminal"
    UNDEFINED = "undefined"
    DECLARED_FAILURE = "declared-failure"
    DIVERGENT = "divergent"


@dataclass(frozen=True)
class Continue:
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported continuation version {self.version}")


@dataclass(frozen=True)
class Stop:
    reason: RuleExpr
    certificate: Certificate
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported continuation version {self.version}")


Continuation: TypeAlias = Continue | Stop


@dataclass(frozen=True)
class Witness:
    """Stable structural identity sufficient to reproduce one atom."""

    identity: str
    descriptor: RuleExpr
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported witness version {self.version}")
        if not self.identity:
            raise ValueError("witness identity cannot be empty")

    @property
    def canonical_identity(self) -> str:
        return loci.canonical_identity(self)


Provenance: TypeAlias = tuple[str, ...]


@dataclass(frozen=True)
class Derivation(Generic[V]):
    replacement: TotalDisposition[V]
    progress: Progress
    continuation: Continuation
    witness: Witness
    provenance: Provenance
    certificate: Certificate
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported derivation version {self.version}")
        if not self.provenance:
            raise ValueError("derivation provenance cannot be empty")

    @property
    def canonical_identity(self) -> str:
        return self.witness.canonical_identity


@dataclass(frozen=True)
class NoSuccessor:
    outcome: NoSuccessorOutcome
    reason: RuleExpr
    witness: Witness
    provenance: Provenance
    certificate: Certificate
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported no-successor version {self.version}")
        if not self.provenance:
            raise ValueError("no-successor provenance cannot be empty")
        if (
            self.outcome is NoSuccessorOutcome.DIVERGENT
            and self.certificate.kind is not CertificateKind.DIVERGENCE
        ):
            raise ValueError("Divergent needs a divergence certificate")

    @property
    def canonical_identity(self) -> str:
        return self.witness.canonical_identity


RuleAtom: TypeAlias = Derivation[V] | NoSuccessor


# ---------------------------------------------------------------------------
# Complete finite/intensional supports and exact probability laws
# ---------------------------------------------------------------------------


class SupportPresentation(Enum):
    FINITE = "finite"
    INTENSIONAL = "intensional"


@dataclass(frozen=True)
class SupportSpace(Generic[A]):
    """Complete finite atoms or one complete intensional relation."""

    presentation: SupportPresentation
    atoms: tuple[A, ...]
    relation: RuleExpr | None
    cardinality: Cardinality
    completeness_evidence: Certificate
    soundness_evidence: Certificate
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported support version {self.version}")
        if self.presentation is SupportPresentation.FINITE:
            if self.relation is not None:
                raise ValueError("finite support cannot carry an intensional relation")
            expected = cardinality_size(self.cardinality)
            if expected is None or expected != len(self.atoms):
                raise ValueError("finite support cardinality must equal atom count")
        else:
            if self.atoms:
                raise ValueError("intensional support cannot carry enumerated atoms")
            if self.relation is None:
                raise ValueError("intensional support needs a closed relation AST")


def finite_support(
    atoms: tuple[A, ...],
    *,
    label: str = "finite-support",
) -> SupportSpace[A]:
    return SupportSpace(
        SupportPresentation.FINITE,
        atoms,
        None,
        finite_cardinality(len(atoms)),
        _certificate(CertificateKind.COMPLETENESS, f"{label}:complete"),
        _certificate(CertificateKind.SOUNDNESS, f"{label}:sound"),
    )


def intensional_support(
    relation: RuleExpr,
    cardinality: Cardinality,
    *,
    completeness_evidence: Certificate,
    soundness_evidence: Certificate,
) -> SupportSpace[A]:
    return SupportSpace(
        SupportPresentation.INTENSIONAL,
        (),
        relation,
        cardinality,
        completeness_evidence,
        soundness_evidence,
    )


class ProbabilityPresentation(Enum):
    FINITE = "finite"
    INTENSIONAL = "intensional"


@dataclass(frozen=True)
class AtomMass:
    atom_identity: str
    mass: Fraction

    def __post_init__(self) -> None:
        if not self.atom_identity:
            raise ValueError("probability mass needs an atom identity")
        if self.mass <= 0:
            raise ValueError("probability masses must be strictly positive")


@dataclass(frozen=True)
class ProbabilityLaw:
    """An exact normalized law over atoms; never a random draw."""

    presentation: ProbabilityPresentation
    masses: tuple[AtomMass, ...]
    measure: RuleExpr | None
    normalization_evidence: Certificate
    measurable_space_evidence: Certificate
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported probability-law version {self.version}")
        if self.presentation is ProbabilityPresentation.FINITE:
            if self.measure is not None:
                raise ValueError("finite probability law cannot carry a measure AST")
            if not self.masses:
                raise ValueError("finite probability law cannot be empty")
            identities = tuple(item.atom_identity for item in self.masses)
            if len(identities) != len(set(identities)):
                raise ValueError("finite probability law repeats an atom identity")
            if sum((item.mass for item in self.masses), Fraction(0)) != Fraction(1):
                raise ValueError("finite probability law must normalize exactly to one")
        else:
            if self.masses:
                raise ValueError("intensional probability law cannot enumerate masses")
            if self.measure is None:
                raise ValueError("intensional probability law needs a measure AST")

    def mass_for(self, atom_identity: str) -> Fraction:
        for item in self.masses:
            if item.atom_identity == atom_identity:
                return item.mass
        return Fraction(0)


@dataclass(frozen=True)
class OutcomeSpace(Generic[A]):
    support: SupportSpace[A]
    probability_law: ProbabilityLaw | None = None
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported outcome-space version {self.version}")
        law = self.probability_law
        if law is None:
            return
        if self.support.presentation is SupportPresentation.FINITE:
            identities = tuple(_atom_identity(atom) for atom in self.support.atoms)
            if set(identities) != {item.atom_identity for item in law.masses}:
                raise ValueError("probability-law support does not equal atom support")
        elif law.presentation is not ProbabilityPresentation.INTENSIONAL:
            raise ValueError("intensional support needs an intensional law")


def _atom_identity(atom: object) -> str:
    canonical = getattr(atom, "canonical_identity", None)
    if isinstance(canonical, str) and canonical:
        return canonical
    identity = getattr(atom, "identity", None)
    if isinstance(identity, str) and identity:
        return identity
    return loci.canonical_identity(atom)


def finite_probability_law(
    masses: tuple[tuple[A, Fraction], ...],
) -> ProbabilityLaw:
    return ProbabilityLaw(
        ProbabilityPresentation.FINITE,
        tuple(AtomMass(_atom_identity(atom), Fraction(mass)) for atom, mass in masses),
        None,
        _certificate(CertificateKind.NORMALIZATION, "finite-law:normalized"),
        _certificate(CertificateKind.MEASURABILITY, "finite-law:measurable"),
    )


# ---------------------------------------------------------------------------
# Rule denotation nodes and faults
# ---------------------------------------------------------------------------


class ExistingPlanKind(Enum):
    BY_INDEX = "by-index"
    BY_TARGET = "by-target"
    PRESERVE = "preserve"


@dataclass(frozen=True)
class ExistingPlan:
    """Closed construction of all existing-target dispositions."""

    kind: ExistingPlanKind
    expressions: tuple[RuleExpr, ...]
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported existing-plan version {self.version}")
        if self.kind is ExistingPlanKind.BY_TARGET and len(self.expressions) != 1:
            raise ValueError("by-target plan needs exactly one expression")
        if self.kind is ExistingPlanKind.PRESERVE and self.expressions:
            raise ValueError("preserve plan cannot carry expressions")
        if self.kind is ExistingPlanKind.BY_INDEX and not self.expressions:
            raise ValueError("by-index plan cannot be empty")


@dataclass(frozen=True)
class LiteralDenotation(Generic[V]):
    outcomes: OutcomeSpace[RuleAtom[V]]


@dataclass(frozen=True)
class ExpressionDenotation:
    existing_plan: ExistingPlan
    progress: Progress
    continuation: Continuation
    witness: RuleExpr
    provenance: Provenance
    certificate: Certificate


@dataclass(frozen=True)
class IntensionalDenotation:
    relation: RuleExpr
    cardinality: Cardinality
    completeness_evidence: Certificate
    soundness_evidence: Certificate
    probability_law: ProbabilityLaw | None = None


@dataclass(frozen=True)
class ParallelDenotation(Generic[R, W, C]):
    parts: tuple["Rule[R, W, C]", ...]

    def __post_init__(self) -> None:
        if not self.parts:
            raise ValueError("parallel Rule needs at least one part")


RuleDenotation: TypeAlias = (
    LiteralDenotation[alphabets.SemanticValue]
    | ExpressionDenotation
    | IntensionalDenotation
    | ParallelDenotation[R, W, C]
)


@dataclass(frozen=True)
class RuleDescriptor(Generic[R, W, C]):
    primitive: RulePrimitive
    denotation: RuleDenotation[R, W, C]
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported Rule descriptor version {self.version}")
        expected = {
            RulePrimitive.LITERAL: LiteralDenotation,
            RulePrimitive.EXPRESSION: ExpressionDenotation,
            RulePrimitive.RELATION: IntensionalDenotation,
            RulePrimitive.DISTRIBUTION: IntensionalDenotation,
            RulePrimitive.DIFFERENTIAL: IntensionalDenotation,
            RulePrimitive.PARALLEL: ParallelDenotation,
        }[self.primitive]
        if not isinstance(self.denotation, expected):
            raise ValueError("Rule primitive and denotation variant disagree")

    @property
    def canonical_identity(self) -> str:
        return loci.canonical_identity(self)


class RuleFaultPhase(Enum):
    DENOTATION = "rule-denotation"
    RESULT_VALIDATION = "result-validation"
    COMPOSITION = "composition"


class RuleFaultReason(Enum):
    INVALID_DESCRIPTOR = "invalid-descriptor"
    INCOMPATIBLE_READ_VIEW = "incompatible-read-view"
    INCOMPATIBLE_WRITABLE = "incompatible-writable"
    EVALUATION_FAILURE = "evaluation-failure"
    INCOMPLETE_DISPOSITION = "incomplete-disposition"
    UNAUTHORIZED_EFFECT = "unauthorized-effect"
    CONFLICTING_EFFECT = "conflicting-effect"
    INVALID_PROBABILITY_LAW = "invalid-probability-law"
    UNSUPPORTED_EXACTNESS = "unsupported-exactness"


@dataclass(frozen=True)
class RuleFault:
    phase: RuleFaultPhase
    reason: RuleFaultReason
    evidence: tuple[Certificate, ...]
    detail: str
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported Rule fault version {self.version}")
        if not self.evidence:
            raise ValueError("Rule fault needs closed evidence")
        if not self.detail:
            raise ValueError("Rule fault detail cannot be empty")


@dataclass(frozen=True)
class RuleRejected:
    fault: RuleFault


@dataclass(frozen=True)
class RuleComplete(Generic[C, V]):
    outcome_space: OutcomeSpace[RuleAtom[V]]


RuleResult: TypeAlias = RuleComplete[C, V] | RuleRejected


class _Observation(Protocol):
    target: loci.Locus
    value: alphabets.SemanticValue


class _GroupKey(Protocol):
    anchor: loci.Locus | None
    channel: int


class _ObservationGroup(Protocol):
    key: _GroupKey
    indices: tuple[int, ...]


class _ReadableView(Protocol):
    observations: tuple[_Observation, ...]
    groups: tuple[_ObservationGroup, ...]


class _ExistingCapability(Protocol):
    target: loci.Locus


class _FreshCapability(Protocol):
    target: loci.FreshReference


class _WritableCapabilities(Protocol):
    existing: tuple[_ExistingCapability, ...]
    fresh: tuple[_FreshCapability, ...]


@dataclass(frozen=True)
class Rule(Generic[R, W, C]):
    """A frozen closed denotation plus immutable compatibility declarations."""

    descriptor: RuleDescriptor[R, W, C]
    contract: RuleContract

    @property
    def canonical_identity(self) -> str:
        return loci.canonical_identity((self.descriptor, self.contract))

    def denote(self, readable: R, writable: W) -> RuleResult[C, alphabets.SemanticValue]:
        """Interpret only this module's sealed AST over the supplied ``R``/``W``."""

        try:
            view = cast(_ReadableView, readable)
            envelope = cast(_WritableCapabilities, writable)
            # Access eagerly so malformed structural records reject at this boundary.
            tuple(view.observations)
            tuple(view.groups)
            tuple(envelope.existing)
            tuple(envelope.fresh)
            return _denote_descriptor(self.descriptor, view, envelope)
        except (IndexError, KeyError, TypeError, ValueError) as exc:
            return _rejected(
                RuleFaultPhase.DENOTATION,
                RuleFaultReason.EVALUATION_FAILURE,
                f"{type(exc).__name__}: {exc}",
            )


def _rejected(
    phase: RuleFaultPhase,
    reason: RuleFaultReason,
    detail: str,
) -> RuleRejected:
    return RuleRejected(
        RuleFault(
            phase,
            reason,
            (_certificate(CertificateKind.CONFORMANCE, detail),),
            detail,
        )
    )


def _denote_descriptor(
    descriptor: RuleDescriptor[R, W, C],
    readable: _ReadableView,
    writable: _WritableCapabilities,
) -> RuleResult[C, alphabets.SemanticValue]:
    denotation = descriptor.denotation
    if isinstance(denotation, LiteralDenotation):
        return RuleComplete(denotation.outcomes)
    if isinstance(denotation, ExpressionDenotation):
        return _denote_expression(denotation, readable, writable)
    if isinstance(denotation, IntensionalDenotation):
        support: SupportSpace[RuleAtom[alphabets.SemanticValue]] = (
            intensional_support(
                denotation.relation,
                denotation.cardinality,
                completeness_evidence=denotation.completeness_evidence,
                soundness_evidence=denotation.soundness_evidence,
            )
        )
        return RuleComplete(OutcomeSpace(support, denotation.probability_law))
    if isinstance(denotation, ParallelDenotation):
        return _denote_parallel(denotation, readable, writable)
    return _rejected(
        RuleFaultPhase.DENOTATION,
        RuleFaultReason.INVALID_DESCRIPTOR,
        "unknown closed Rule denotation variant",
    )


def _denote_expression(
    denotation: ExpressionDenotation,
    readable: _ReadableView,
    writable: _WritableCapabilities,
) -> RuleResult[C, alphabets.SemanticValue]:
    existing_targets = tuple(item.target for item in writable.existing)
    fresh_targets = tuple(item.target for item in writable.fresh)
    plan = denotation.existing_plan

    if plan.kind is ExistingPlanKind.PRESERVE:
        existing = tuple(preserve(target) for target in existing_targets)
    elif plan.kind is ExistingPlanKind.BY_INDEX:
        if len(plan.expressions) != len(existing_targets):
            return _rejected(
                RuleFaultPhase.RESULT_VALIDATION,
                RuleFaultReason.INCOMPLETE_DISPOSITION,
                "by-index expression count does not equal existing capability count",
            )
        existing = tuple(
            replace(
                target,
                _require_semantic_value(
                    _evaluate(expression, readable, anchor=None)
                ),
            )
            for target, expression in zip(
                existing_targets,
                plan.expressions,
                strict=True,
            )
        )
    else:
        expression = plan.expressions[0]
        existing = tuple(
            replace(
                target,
                _require_semantic_value(
                    _evaluate(expression, readable, anchor=target)
                ),
            )
            for target in existing_targets
        )

    fresh = tuple(absent(target) for target in fresh_targets)
    total = TotalDisposition(
        existing,
        fresh,
        _certificate(CertificateKind.TOTALITY, "expression-plan:total"),
    )
    witness_descriptor = RuleExpr(
        ExpressionPrimitive.TUPLE,
        (
            denotation.witness,
            literal_expr(total.canonical_identity),
        ),
    )
    witness = Witness(
        identity=loci.canonical_identity(witness_descriptor),
        descriptor=witness_descriptor,
    )
    atom = Derivation(
        total,
        denotation.progress,
        denotation.continuation,
        witness,
        denotation.provenance,
        denotation.certificate,
    )
    return RuleComplete(OutcomeSpace(finite_support((atom,), label="expression")))


def _denote_parallel(
    denotation: ParallelDenotation[R, W, C],
    readable: _ReadableView,
    writable: _WritableCapabilities,
) -> RuleResult[C, alphabets.SemanticValue]:
    parts: list[Derivation[alphabets.SemanticValue]] = []
    for rule in denotation.parts:
        result = rule.denote(cast(R, readable), cast(W, writable))
        if isinstance(result, RuleRejected):
            return result
        support = result.outcome_space.support
        if (
            support.presentation is not SupportPresentation.FINITE
            or len(support.atoms) != 1
            or not isinstance(support.atoms[0], Derivation)
            or result.outcome_space.probability_law is not None
        ):
            return _rejected(
                RuleFaultPhase.COMPOSITION,
                RuleFaultReason.UNSUPPORTED_EXACTNESS,
                "parallel currently requires deterministic finite derivation parts",
            )
        parts.append(support.atoms[0])

    merged = _merge_dispositions(tuple(parts))
    if isinstance(merged, RuleRejected):
        return merged
    progress = (
        Progress.ADVANCED
        if any(part.progress is Progress.ADVANCED for part in parts)
        else Progress.QUIESCENT
    )
    continuation: Continuation = Continue()
    stops = tuple(
        part.continuation
        for part in parts
        if isinstance(part.continuation, Stop)
    )
    if stops:
        if len(set(stops)) != 1:
            return _rejected(
                RuleFaultPhase.COMPOSITION,
                RuleFaultReason.CONFLICTING_EFFECT,
                "parallel parts declare incompatible stopping reasons",
            )
        continuation = stops[0]
    witness_expr = RuleExpr(
        ExpressionPrimitive.TUPLE,
        tuple(part.witness.descriptor for part in parts),
    )
    atom = Derivation(
        merged,
        progress,
        continuation,
        Witness(loci.canonical_identity(witness_expr), witness_expr),
        tuple(item for part in parts for item in part.provenance),
        _certificate(CertificateKind.COMPOSITION, "parallel:closed-product"),
    )
    return RuleComplete(OutcomeSpace(finite_support((atom,), label="parallel")))


def _merge_dispositions(
    parts: tuple[Derivation[alphabets.SemanticValue], ...],
) -> TotalDisposition[alphabets.SemanticValue] | RuleRejected:
    if not parts:
        return _rejected(
            RuleFaultPhase.COMPOSITION,
            RuleFaultReason.INVALID_DESCRIPTOR,
            "parallel derivation product cannot be empty",
        )
    first = parts[0].replacement
    existing: list[Disposition[loci.Locus, alphabets.SemanticValue]] = []
    fresh: list[
        Disposition[loci.FreshReference, alphabets.SemanticValue]
    ] = []
    for index in range(len(first.existing)):
        candidates = tuple(part.replacement.existing[index] for part in parts)
        if len({item.target for item in candidates}) != 1:
            return _rejected(
                RuleFaultPhase.COMPOSITION,
                RuleFaultReason.INCOMPATIBLE_WRITABLE,
                "parallel existing-target order disagrees",
            )
        active = tuple(
            item
            for item in candidates
            if item.action is not DispositionAction.PRESERVE
        )
        if not active:
            existing.append(candidates[0])
        elif len(set(active)) == 1:
            existing.append(active[0])
        else:
            return _rejected(
                RuleFaultPhase.COMPOSITION,
                RuleFaultReason.CONFLICTING_EFFECT,
                "parallel existing-target effects conflict",
            )
    for index in range(len(first.fresh)):
        candidates = tuple(part.replacement.fresh[index] for part in parts)
        if len({item.target for item in candidates}) != 1:
            return _rejected(
                RuleFaultPhase.COMPOSITION,
                RuleFaultReason.INCOMPATIBLE_WRITABLE,
                "parallel fresh-target order disagrees",
            )
        active = tuple(
            item
            for item in candidates
            if item.action is not DispositionAction.ABSENT
        )
        if not active:
            fresh.append(candidates[0])
        elif len(set(active)) == 1:
            fresh.append(active[0])
        else:
            return _rejected(
                RuleFaultPhase.COMPOSITION,
                RuleFaultReason.CONFLICTING_EFFECT,
                "parallel fresh-target effects conflict",
            )
    return TotalDisposition(
        tuple(existing),
        tuple(fresh),
        _certificate(CertificateKind.TOTALITY, "parallel:merged-total"),
    )


def _evaluate(
    expression: RuleExpr,
    readable: _ReadableView,
    *,
    anchor: loci.Locus | None,
) -> RuleRuntimeValue:
    primitive = expression.primitive
    arguments = expression.arguments
    if primitive is ExpressionPrimitive.LITERAL:
        if len(arguments) != 1 or isinstance(arguments[0], RuleExpr):
            raise ValueError("literal expression is malformed")
        return arguments[0]
    if primitive is ExpressionPrimitive.OBSERVATION:
        index = _literal_int(arguments, 0)
        return readable.observations[index].value
    if primitive is ExpressionPrimitive.GROUP:
        channel = _literal_int(arguments, 0)
        return tuple(
            readable.observations[index].value
            for index in _group_indices(readable, anchor, channel)
        )
    if primitive is ExpressionPrimitive.PROJECT:
        source = _evaluate(_child(arguments, 0), readable, anchor=anchor)
        if not isinstance(source, tuple):
            raise TypeError("project source is not tuple-valued")
        return source[_literal_int(arguments, 1)]
    if primitive is ExpressionPrimitive.TUPLE:
        return tuple(
            _evaluate(_as_expression(argument), readable, anchor=anchor)
            for argument in arguments
        )
    if primitive in (ExpressionPrimitive.ADD, ExpressionPrimitive.MULTIPLY):
        values = tuple(
            _require_int(
                _evaluate(_as_expression(argument), readable, anchor=anchor)
            )
            for argument in arguments
        )
        if primitive is ExpressionPrimitive.ADD:
            return sum(values)
        product = 1
        for value in values:
            product *= value
        return product
    if primitive is ExpressionPrimitive.MODULO:
        value = _require_int(_evaluate(_child(arguments, 0), readable, anchor=anchor))
        modulus_value = _literal_int(arguments, 1)
        if modulus_value <= 0:
            raise ValueError("modulo expression needs positive modulus")
        return value % modulus_value
    if primitive is ExpressionPrimitive.COUNT:
        values = _require_tuple(
            _evaluate(_child(arguments, 0), readable, anchor=anchor)
        )
        return sum(1 for value in values if _require_bit(value) == 1)
    if primitive is ExpressionPrimitive.GATE:
        source = _evaluate(_child(arguments, 0), readable, anchor=anchor)
        threshold = _literal_int(arguments, 2)
        gate_name = _literal_str(arguments, 1)
        values = source if isinstance(source, tuple) else (source,)
        total = sum(_require_bit(value) for value in values)
        kind = GateKind(gate_name)
        if kind is GateKind.ANY:
            return int(total > 0)
        if kind is GateKind.ALL:
            return int(total == len(values))
        if kind is GateKind.MAJORITY:
            return int(total * 2 > len(values))
        if kind is GateKind.AT_LEAST:
            return int(total >= threshold)
        if kind is GateKind.AT_MOST:
            return int(total <= threshold)
        return int(total == threshold)
    if primitive is ExpressionPrimitive.LOOKUP:
        table = _require_tuple(
            _evaluate(_child(arguments, 0), readable, anchor=anchor)
        )
        index = _require_int(
            _evaluate(_child(arguments, 1), readable, anchor=anchor)
        )
        return table[index]
    if primitive is ExpressionPrimitive.EQUAL:
        left = _evaluate(_child(arguments, 0), readable, anchor=anchor)
        right = _evaluate(_child(arguments, 1), readable, anchor=anchor)
        return loci.semantic_equal(left, right)
    if primitive in (ExpressionPrimitive.ALL, ExpressionPrimitive.ANY):
        values = _require_tuple(
            _evaluate(_child(arguments, 0), readable, anchor=anchor)
        )
        bits = tuple(_require_bit(value) for value in values)
        return (
            int(all(bits))
            if primitive is ExpressionPrimitive.ALL
            else int(any(bits))
        )
    raise ValueError(f"unsupported expression primitive {primitive.value}")


def _group_indices(
    readable: _ReadableView,
    anchor: loci.Locus | None,
    channel: int,
) -> tuple[int, ...]:
    matches = tuple(
        item.indices
        for item in readable.groups
        if item.key.channel == channel
        and (anchor is None or item.key.anchor == anchor)
    )
    if len(matches) != 1:
        raise ValueError(
            f"read group {(anchor, channel)!r} resolved {len(matches)} times"
        )
    return matches[0]


def _as_expression(value: RuleScalar | RuleExpr) -> RuleExpr:
    return value if isinstance(value, RuleExpr) else literal_expr(value)


def _child(
    arguments: tuple[RuleScalar | RuleExpr, ...],
    index: int,
) -> RuleExpr:
    value = arguments[index]
    if not isinstance(value, RuleExpr):
        raise TypeError("expected a child Rule expression")
    return value


def _literal_int(
    arguments: tuple[RuleScalar | RuleExpr, ...],
    index: int,
) -> int:
    value = arguments[index]
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("expected an integer Rule literal")
    return value


def _literal_str(
    arguments: tuple[RuleScalar | RuleExpr, ...],
    index: int,
) -> str:
    value = arguments[index]
    if not isinstance(value, str):
        raise TypeError("expected a string Rule literal")
    return value


def _require_tuple(value: RuleRuntimeValue) -> tuple[RuleRuntimeValue, ...]:
    if not isinstance(value, tuple):
        raise TypeError("expected tuple-valued Rule expression")
    return value


def _require_int(value: RuleRuntimeValue) -> int:
    if isinstance(value, bool):
        return int(value)
    if not isinstance(value, int):
        raise TypeError("expected integer Rule expression")
    return value


def _require_bit(value: RuleRuntimeValue) -> int:
    integer = _require_int(value)
    if integer not in (0, 1):
        raise ValueError("expected a binary Rule value")
    return integer


def _require_semantic_value(
    value: RuleRuntimeValue,
) -> alphabets.SemanticValue:
    if isinstance(
        value,
        (bool, int, Fraction, str, alphabets.RepresentedNumber, alphabets.ValueNode),
    ):
        return value
    raise TypeError("Rule expression did not produce one semantic value")


# ---------------------------------------------------------------------------
# General constructors and closed composition
# ---------------------------------------------------------------------------


def literal(
    outcomes: OutcomeSpace[RuleAtom[alphabets.SemanticValue]],
    *,
    contract: RuleContract,
) -> Rule[R, W, C]:
    """Build a Rule whose complete closed atom space is already supplied."""

    if (
        outcomes.support.presentation is SupportPresentation.FINITE
        and not outcomes.support.atoms
    ):
        raise ValueError(
            "a complete finite Rule result cannot be a bare empty support"
        )
    descriptor: RuleDescriptor[R, W, C] = RuleDescriptor(
        RulePrimitive.LITERAL,
        LiteralDenotation(outcomes),
    )
    return Rule(descriptor, contract)


def expression(
    existing_plan: ExistingPlan,
    *,
    contract: RuleContract,
    witness: RuleExpr,
    provenance: Provenance,
    progress: Progress = Progress.ADVANCED,
    continuation: Continuation = Continue(),
    certificate: Certificate | None = None,
) -> Rule[R, W, C]:
    """Build one deterministic closed expression-to-disposition Rule."""

    if not provenance:
        raise ValueError("expression Rule provenance cannot be empty")
    descriptor: RuleDescriptor[R, W, C] = RuleDescriptor(
        RulePrimitive.EXPRESSION,
        ExpressionDenotation(
            existing_plan,
            progress,
            continuation,
            witness,
            provenance,
            certificate
            or _certificate(CertificateKind.DERIVATION, "expression:verified"),
        ),
    )
    return Rule(descriptor, contract)


def relation(
    relation_ast: RuleExpr,
    cardinality: Cardinality,
    *,
    contract: RuleContract,
    completeness_evidence: Certificate,
    soundness_evidence: Certificate,
) -> Rule[R, W, C]:
    """Build a complete intensional atom relation without running a solver."""

    descriptor: RuleDescriptor[R, W, C] = RuleDescriptor(
        RulePrimitive.RELATION,
        IntensionalDenotation(
            relation_ast,
            cardinality,
            completeness_evidence,
            soundness_evidence,
        ),
    )
    return Rule(descriptor, contract)


def distribution(
    relation_ast: RuleExpr,
    cardinality: Cardinality,
    law: ProbabilityLaw,
    *,
    contract: RuleContract,
    completeness_evidence: Certificate,
    soundness_evidence: Certificate,
) -> Rule[R, W, C]:
    """Build an intensional law-valued Rule without drawing from the law."""

    if law.presentation is not ProbabilityPresentation.INTENSIONAL:
        raise ValueError("intensional distribution requires an intensional law")
    descriptor: RuleDescriptor[R, W, C] = RuleDescriptor(
        RulePrimitive.DISTRIBUTION,
        IntensionalDenotation(
            relation_ast,
            cardinality,
            completeness_evidence,
            soundness_evidence,
            law,
        ),
    )
    return Rule(descriptor, contract)


def differential(
    relation_ast: RuleExpr,
    cardinality: Cardinality,
    *,
    contract: RuleContract,
    completeness_evidence: Certificate,
    soundness_evidence: Certificate,
) -> Rule[R, W, C]:
    """Build an exact/intensional differential solution relation."""

    descriptor: RuleDescriptor[R, W, C] = RuleDescriptor(
        RulePrimitive.DIFFERENTIAL,
        IntensionalDenotation(
            relation_ast,
            cardinality,
            completeness_evidence,
            soundness_evidence,
        ),
    )
    return Rule(descriptor, contract)


def parallel(parts: tuple[Rule[R, W, C], ...]) -> Rule[R, W, C]:
    """Compose deterministic effects over one immutable ``(R, W)`` binding."""

    if not parts:
        raise ValueError("parallel requires at least one Rule")
    contract = parts[0].contract
    if any(part.contract != contract for part in parts[1:]):
        raise ValueError("parallel Rule contracts must be identical")
    descriptor: RuleDescriptor[R, W, C] = RuleDescriptor(
        RulePrimitive.PARALLEL,
        ParallelDenotation(parts),
    )
    return Rule(descriptor, contract)


def finite_rule(
    atoms: tuple[RuleAtom[alphabets.SemanticValue], ...],
    *,
    contract: RuleContract,
    probability_law: ProbabilityLaw | None = None,
    label: str = "finite-rule",
) -> Rule[R, W, C]:
    """Convenience constructor for closed finite zero/one/many fixtures."""

    if not atoms:
        raise ValueError("finite Rule needs a typed atom; bare empty is invalid")
    return literal(
        OutcomeSpace(finite_support(atoms, label=label), probability_law),
        contract=contract,
    )


# ---------------------------------------------------------------------------
# Retained native component presets, compiled from concrete construction data
# ---------------------------------------------------------------------------


def _native_contract(
    carrier: loci.CarrierContract,
    *,
    readable: neighborhoods.ReadableRegion[object, object],
    value_profile: alphabets.ValueProfile = alphabets.ValueProfile.BOOLEAN,
) -> RuleContract:
    return RuleContract(
        configuration_contract=carrier,
        value_profile=value_profile,
        required_read_shape=readable.result_shape,
        required_join_shape=readable.join_shape,
        required_effect_profile=frontiers.EffectProfile(
            existing=(frontiers.Effect.REPLACE,),
        ),
    )


def _rule_number(number: int) -> int:
    if isinstance(number, bool) or not isinstance(number, int):
        raise TypeError("rule construction data must be an integer")
    if not 0 <= number < 256:
        raise ValueError("rule construction data must be in range 0..255")
    return number


def _binary_table(number: int, width: int = 8) -> tuple[bool, ...]:
    return tuple(bool((number >> index) & 1) for index in range(width))


def ar2_modular_0d(
    *,
    rule: int,
    modulus: int = 97,
    coefficient_grid: tuple[int, int] = (16, 16),
    constant: int = 1,
) -> Rule[R, W, C]:
    """Compile one concrete second-order modular recurrence."""

    if isinstance(rule, bool) or not isinstance(rule, int):
        raise TypeError("rule construction data must be an integer")
    rows, columns = coefficient_grid
    if rows <= 0 or columns <= 0 or not 0 <= rule < rows * columns:
        raise ValueError("rule construction data is outside coefficient grid")
    if modulus <= 0:
        raise ValueError("modulus must be positive")
    a = rule // columns + 1
    b = rule % columns
    next_value = modulo(
        add(
            multiply(literal_expr(a), observation(1)),
            multiply(literal_expr(b), observation(0)),
            literal_expr(constant),
        ),
        modulus,
    )
    carrier = loci.CarrierContract(loci.CarrierKind.RECORD, rank=0, shape=())
    readable = neighborhoods.ar2_0d(
        configuration_contract=carrier,
        value_profile=alphabets.ValueProfile.INTEGER,
    )
    return expression(
        ExistingPlan(
            ExistingPlanKind.BY_INDEX,
            (observation(1), next_value),
        ),
        contract=_native_contract(
            carrier,
            readable=readable,
            value_profile=alphabets.ValueProfile.INTEGER,
        ),
        witness=RuleExpr(
            ExpressionPrimitive.TUPLE,
            (
                literal_expr("ar2-modular"),
                literal_expr(rule),
                literal_expr(a),
                literal_expr(b),
                literal_expr(constant),
                literal_expr(modulus),
            ),
        ),
        provenance=(
            "native:ar2_modular_0d",
            f"rule-{rule}:a={a},b={b},c={constant},mod={modulus}",
        ),
    )


def dyadlags_0d(*, rule: int) -> Rule[R, W, C]:
    """Compile one concrete binary temporal three-lag lookup."""

    number = _rule_number(rule)
    index = add(
        observation(2),
        multiply(literal_expr(2), observation(1)),
        multiply(literal_expr(4), observation(0)),
    )
    output = lookup(_binary_table(number), index)
    carrier = loci.CarrierContract(
        loci.CarrierKind.HISTORY,
        rank=1,
        shape=(3,),
        axes=("history",),
    )
    readable = neighborhoods.dyadlags_0d(
        configuration_contract=carrier,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    return expression(
        ExistingPlan(
            ExistingPlanKind.BY_INDEX,
            (observation(1), observation(2), output),
        ),
        contract=_native_contract(
            carrier,
            readable=readable,
        ),
        witness=RuleExpr(
            ExpressionPrimitive.TUPLE,
            (literal_expr("dyadlags-0d"), literal_expr(number), index),
        ),
        provenance=("native:dyadlags_0d", f"rule-{number}"),
    )


_UINT64_MASK = (1 << 64) - 1
_LAGCOUNTS_HASH_KEY = 0xD1B54A32D192ED03


def _splitmix64(seed: int, stream: int) -> int:
    value = (seed + stream + 0x9E3779B97F4A7C15) & _UINT64_MASK
    value = (value ^ (value >> 30)) * 0xBF58476D1CE4E5B9 & _UINT64_MASK
    value = (value ^ (value >> 27)) * 0x94D049BB133111EB & _UINT64_MASK
    return (value ^ (value >> 31)) & _UINT64_MASK


def _sampled_lag_table(number: int) -> tuple[bool, ...]:
    base = (number ^ _LAGCOUNTS_HASH_KEY) & _UINT64_MASK
    return tuple(bool(_splitmix64(base, context) & 1) for context in range(128))


def lagcounts_0d(
    *,
    rule: int,
    band_size: int = 3,
    band_count: int = 3,
) -> Rule[R, W, C]:
    """Compile one concrete count-banded temporal lookup."""

    number = _rule_number(rule)
    if band_size != 3 or band_count != 3:
        raise ValueError("G7-01 native lagcounts uses exactly three bands of three")
    context = add(
        observation(0),
        multiply(literal_expr(2), count(group(1))),
        multiply(literal_expr(8), count(group(2))),
        multiply(literal_expr(32), count(group(3))),
    )
    output = lookup(_sampled_lag_table(number), context)
    prior = tuple(observation(index) for index in range(8, -1, -1))
    carrier = loci.CarrierContract(
        loci.CarrierKind.HISTORY,
        rank=1,
        shape=(10,),
        axes=("history",),
    )
    readable = neighborhoods.lagcounts_0d(
        band_size,
        band_count,
        configuration_contract=carrier,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    return expression(
        ExistingPlan(ExistingPlanKind.BY_INDEX, (*prior, output)),
        contract=_native_contract(
            carrier,
            readable=readable,
        ),
        witness=RuleExpr(
            ExpressionPrimitive.TUPLE,
            (literal_expr("lagcounts-0d"), literal_expr(number), context),
        ),
        provenance=("native:lagcounts_0d", f"rule-{number}"),
    )


def _spatial_lookup(
    *,
    rule: int,
    rank: int,
    secondary_gate: GateKind,
    secondary_threshold: int,
    label: str,
    readable: neighborhoods.ReadableRegion[object, object],
) -> Rule[R, W, C]:
    number = _rule_number(rule)
    primary = gate(group(1), GateKind.MAJORITY)
    secondary = gate(
        group(2),
        secondary_gate,
        threshold=secondary_threshold,
    )
    index = add(
        project(group(0), 0),
        multiply(literal_expr(2), primary),
        multiply(literal_expr(4), secondary),
    )
    output = lookup(_binary_table(number), index)
    carrier = loci.CarrierContract(
        loci.CarrierKind.GRID,
        rank=rank,
        axes=("x", "y", "z")[:rank],
    )
    return expression(
        ExistingPlan(ExistingPlanKind.BY_TARGET, (output,)),
        contract=_native_contract(
            carrier,
            readable=readable,
        ),
        witness=RuleExpr(
            ExpressionPrimitive.TUPLE,
            (literal_expr(label), literal_expr(number), index),
        ),
        provenance=(f"native:{label.replace('-', '_')}", f"rule-{number}"),
    )


def dyadrads_1d(*, rule: int) -> Rule[R, W, C]:
    """Compile one concrete 1-D Dyadrads lookup."""

    number = _rule_number(rule)
    index = add(
        project(group(0), 0),
        multiply(literal_expr(2), gate(group(1), GateKind.ANY)),
        multiply(literal_expr(4), gate(group(2), GateKind.ANY)),
    )
    output = lookup(_binary_table(number), index)
    carrier = loci.CarrierContract(
        loci.CarrierKind.GRID,
        rank=1,
        axes=("x",),
    )
    readable = neighborhoods.dyadrads_1d(
        configuration_contract=carrier,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    return expression(
        ExistingPlan(ExistingPlanKind.BY_TARGET, (output,)),
        contract=_native_contract(
            carrier,
            readable=readable,
        ),
        witness=RuleExpr(
            ExpressionPrimitive.TUPLE,
            (literal_expr("dyadrads-1d"), literal_expr(number), index),
        ),
        provenance=("native:dyadrads_1d", f"rule-{number}"),
    )


def dyadaxes_2d(*, rule: int) -> Rule[R, W, C]:
    """Compile one concrete 2-D Dyadaxes lookup."""

    carrier = loci.CarrierContract(
        loci.CarrierKind.GRID,
        rank=2,
        axes=("x", "y"),
    )
    return _spatial_lookup(
        rule=rule,
        rank=2,
        secondary_gate=GateKind.MAJORITY,
        secondary_threshold=0,
        label="dyadaxes-2d",
        readable=neighborhoods.dyadaxes_2d(
            configuration_contract=carrier,
            value_profile=alphabets.ValueProfile.BOOLEAN,
        ),
    )


def dyadaxes_3d(*, rule: int) -> Rule[R, W, C]:
    """Compile one concrete 3-D Dyadaxes lookup."""

    carrier = loci.CarrierContract(
        loci.CarrierKind.GRID,
        rank=3,
        axes=("x", "y", "z"),
    )
    return _spatial_lookup(
        rule=rule,
        rank=3,
        secondary_gate=GateKind.AT_LEAST,
        secondary_threshold=10,
        label="dyadaxes-3d",
        readable=neighborhoods.dyadaxes_3d(
            configuration_contract=carrier,
            value_profile=alphabets.ValueProfile.BOOLEAN,
        ),
    )


def elementary(number: int) -> Rule[R, W, C]:
    """Compile an elementary binary local lookup from concrete rule data."""

    number = _rule_number(number)
    index = add(
        multiply(literal_expr(4), project(group(0), 0)),
        multiply(literal_expr(2), project(group(0), 1)),
        project(group(0), 2),
    )
    carrier = loci.CarrierContract(
        loci.CarrierKind.GRID,
        rank=1,
        axes=("x",),
    )
    readable = neighborhoods.eca(
        configuration_contract=carrier,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    return expression(
        ExistingPlan(
            ExistingPlanKind.BY_TARGET,
            (lookup(_binary_table(number), index),),
        ),
        contract=_native_contract(
            carrier,
            readable=readable,
        ),
        witness=RuleExpr(
            ExpressionPrimitive.TUPLE,
            (literal_expr("elementary"), literal_expr(number), index),
        ),
        provenance=("preset:elementary", f"rule-{number}"),
    )


__all__ = [
    "AtomMass",
    "Cardinality",
    "CardinalityClaim",
    "Certificate",
    "CertificateKind",
    "Continue",
    "Derivation",
    "Disposition",
    "DispositionAction",
    "ExactlyOne",
    "ExactlyZero",
    "ExistingPlan",
    "ExistingPlanKind",
    "GateKind",
    "InfiniteCardinality",
    "Many",
    "NoPayload",
    "NoSuccessor",
    "NoSuccessorOutcome",
    "OutcomeSpace",
    "ProbabilityLaw",
    "ProbabilityPresentation",
    "Progress",
    "Provenance",
    "Rule",
    "RuleAtom",
    "RuleComplete",
    "RuleContract",
    "RuleDescriptor",
    "RuleExpr",
    "RuleFault",
    "RuleFaultPhase",
    "RuleFaultReason",
    "RulePrimitive",
    "RuleRejected",
    "RuleResult",
    "Stop",
    "SupportPresentation",
    "SupportSpace",
    "TotalDisposition",
    "Undetermined",
    "ValuePayload",
    "Witness",
    "absent",
    "add",
    "ar2_modular_0d",
    "cardinality_size",
    "count",
    "create",
    "delete",
    "differential",
    "distribution",
    "dyadlags_0d",
    "dyadrads_1d",
    "dyadaxes_2d",
    "dyadaxes_3d",
    "elementary",
    "expression",
    "finite_cardinality",
    "finite_probability_law",
    "finite_rule",
    "finite_support",
    "gate",
    "group",
    "intensional_support",
    "lagcounts_0d",
    "literal",
    "literal_expr",
    "lookup",
    "modulo",
    "multiply",
    "observation",
    "parallel",
    "preserve",
    "project",
    "relation",
    "replace",
]
