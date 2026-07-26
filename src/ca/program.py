"""Exactly-five-field programs, one atomic application law, and rollout.

Rule denotation ends in :mod:`ca.rules`; this module validates and maps that
complete result through deterministic fresh binding, generic structural
reconstruction, successor validation, semantic quotienting, and exact measure
projection.  ``apply`` is the package's only one-step execution primitive.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, fields
from enum import Enum
from fractions import Fraction
from itertools import product as cartesian_product
from math import lcm
from typing import Generic, TypeAlias, TypeVar, cast

from . import alphabets, frontiers, loci, neighborhoods, rules, seeds


C = TypeVar("C")
V = TypeVar("V")
W = TypeVar("W")
R = TypeVar("R")


class ProgramCompatibilityError(ValueError):
    """The five independently built components cannot form one program."""


_COMPATIBILITY_CLAUSES = (
    "seed-output-unifies",
    "seed-values-conform",
    "frontier-accepts-carrier",
    "neighborhood-accepts-carrier",
    "read-shape-matches",
    "join-shape-matches",
    "effects-fit-frontier",
    "exactness-and-entropy-explicit",
)


@dataclass(frozen=True)
class CompatibilityEvidence:
    """Ephemeral proof summary; it is never stored on ``SimpleProgram``."""

    configuration_contract: loci.CarrierContract
    value_profile: alphabets.ValueProfile
    clauses: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.configuration_contract) is not loci.CarrierContract:
            raise TypeError(
                "compatibility evidence needs a CarrierContract"
            )
        if type(self.value_profile) is not alphabets.ValueProfile:
            raise TypeError(
                "compatibility evidence needs a ValueProfile"
            )
        if self.clauses != _COMPATIBILITY_CLAUSES:
            raise ValueError(
                "compatibility evidence clauses are not the canonical proof"
            )


@dataclass(frozen=True)
class SimpleProgram(Generic[C, V, W, R]):
    """One immutable simple program with exactly the five settled fields."""

    seed: seeds.Seed[C]
    alphabet: alphabets.Alphabet[V]
    frontier: frontiers.WritableRegion[C, W]
    neighborhood: neighborhoods.ReadableRegion[C, R]
    rule: rules.Rule[R, W, C]

    def __post_init__(self) -> None:
        _require_compatible_five_fields(self)

    @property
    def canonical_identity(self) -> str:
        return loci.canonical_identity(self)


def _require_compatible_five_fields(
    program: SimpleProgram[C, V, W, R],
) -> CompatibilityEvidence:
    if type(program) is not SimpleProgram:
        raise ProgramCompatibilityError(
            "SimpleProgram is sealed; semantic sidecar subclasses are invalid"
        )
    if tuple(field.name for field in fields(SimpleProgram)) != (
        "seed",
        "alphabet",
        "frontier",
        "neighborhood",
        "rule",
    ):
        raise ProgramCompatibilityError("SimpleProgram field contract is corrupted")
    if type(program.seed) is not seeds.Seed:
        raise ProgramCompatibilityError("seed is not a recognized Seed")
    if type(program.alphabet) is not alphabets.Alphabet:
        raise ProgramCompatibilityError("alphabet is not a recognized Alphabet")
    if type(program.frontier) is not frontiers.WritableRegion:
        raise ProgramCompatibilityError("frontier is not a recognized WritableRegion")
    if type(program.neighborhood) is not neighborhoods.ReadableRegion:
        raise ProgramCompatibilityError(
            "neighborhood is not a recognized ReadableRegion"
        )
    if type(program.rule) is not rules.Rule:
        raise ProgramCompatibilityError("rule is not a recognized Rule")

    seed_contract = program.seed.output_contract
    rule_contract = program.rule.contract
    carrier = seed_contract.configuration_contract
    if not rule_contract.configuration_contract.accepts(carrier):
        raise ProgramCompatibilityError(
            "Rule configuration contract does not accept Seed output"
        )
    frontier_contract = program.frontier.configuration_contract
    if frontier_contract is not None and not frontier_contract.accepts(carrier):
        raise ProgramCompatibilityError(
            "WritableRegion configuration contract does not accept Seed output"
        )
    readable_contract = program.neighborhood.configuration_contract
    if readable_contract is not None and not readable_contract.accepts(carrier):
        raise ProgramCompatibilityError(
            "ReadableRegion configuration contract does not accept Seed output"
        )

    value_profile = program.alphabet.value_profile
    profiles = (
        seed_contract.value_profile,
        program.frontier.value_profile,
        program.neighborhood.value_profile,
        rule_contract.value_profile,
    )
    if any(profile is not None and profile is not value_profile for profile in profiles):
        raise ProgramCompatibilityError(
            "Seed/Alphabet/region/Rule value profiles disagree"
        )
    if program.neighborhood.result_shape != rule_contract.required_read_shape:
        raise ProgramCompatibilityError("Rule read shape does not match Neighborhood")
    if program.neighborhood.join_shape != rule_contract.required_join_shape:
        raise ProgramCompatibilityError("Rule join shape does not match Neighborhood")
    required_effects = rule_contract.required_effect_profile
    available_effects = program.frontier.effect_profile
    if not (
        set(required_effects.existing).issubset(available_effects.existing)
        and set(required_effects.fresh).issubset(available_effects.fresh)
    ):
        raise ProgramCompatibilityError(
            "Rule effects are not included in Frontier capabilities"
        )
    if (
        seed_contract.exactness_profile is not program.frontier.exactness_profile
        or seed_contract.exactness_profile is not program.neighborhood.exactness_profile
        or seed_contract.exactness_profile is not rule_contract.exactness_profile
    ):
        raise ProgramCompatibilityError("component exactness profiles disagree")
    if (
        rule_contract.entropy_interface is seeds.EntropyInterface.REPLAY_KEY
        and seed_contract.entropy_interface is seeds.EntropyInterface.NONE
    ):
        # A stochastic transition does not require a stochastic Seed, but it
        # does require the program-owned replay interface.  That interface is
        # always available to rollout, so this is not a mismatch.
        pass

    _require_seed_values_conform(program)

    return CompatibilityEvidence(
        carrier,
        value_profile,
        _COMPATIBILITY_CLAUSES,
    )


def _integer_intervals(
    descriptor: alphabets.AlphabetDescriptor,
    upper: int,
) -> tuple[tuple[int, int], ...]:
    """Describe accepted integer intervals within ``[0, upper]`` structurally."""

    kind = descriptor.kind
    intervals: list[tuple[int, int]] = []
    if kind in (
        alphabets.AlphabetKind.ENUM,
        alphabets.AlphabetKind.ORDERED,
        alphabets.AlphabetKind.SYMBOLIC,
    ):
        points = sorted(
            {
                value
                for value in descriptor.values
                if type(value) is int and 0 <= value <= upper
            }
        )
        for point in points:
            if intervals and point == intervals[-1][1] + 1:
                intervals[-1] = (intervals[-1][0], point)
            else:
                intervals.append((point, point))
    elif kind in (
        alphabets.AlphabetKind.NATURALS,
        alphabets.AlphabetKind.RATIONALS,
    ):
        intervals.append((0, upper))
    elif kind is alphabets.AlphabetKind.INTEGERS:
        parameters = dict(descriptor.scalars)
        minimum = cast(int | None, parameters.get("minimum"))
        maximum = cast(int | None, parameters.get("maximum"))
        low = max(0, minimum if minimum is not None else 0)
        high = min(upper, maximum if maximum is not None else upper)
        if low <= high:
            intervals.append((low, high))
    elif kind is alphabets.AlphabetKind.MODULAR:
        modulus = cast(int, dict(descriptor.scalars)["modulus"])
        high = min(upper, modulus - 1)
        if high >= 0:
            intervals.append((0, high))
    elif kind is alphabets.AlphabetKind.UNION:
        for child in descriptor.children:
            intervals.extend(_integer_intervals(child, upper))
    return tuple(intervals)


def _alphabet_accepts_uniform_values(
    alphabet: alphabets.Alphabet[object],
    law: seeds.UniformTupleLaw,
) -> bool:
    """Prove the law's full value range without enumerating ``range(n)``."""

    if alphabet.value_profile is alphabets.ValueProfile.BOOLEAN:
        return (
            law.value_count == 2
            and alphabet.contains(False)
            and alphabet.contains(True)
        )
    upper = law.value_count - 1
    intervals = sorted(
        _integer_intervals(alphabet.descriptor, upper),
        key=lambda interval: (interval[0], interval[1]),
    )
    covered_through = -1
    for low, high in intervals:
        if low > covered_through + 1:
            break
        covered_through = max(covered_through, high)
        if covered_through >= upper:
            return True
    return False


def _require_seed_values_conform(
    program: SimpleProgram[C, V, W, R],
) -> None:
    """Prove every explicit Seed value admitted at construction time."""

    def require_configuration(configuration: object) -> None:
        if not isinstance(
            configuration,
            (loci.FiniteConfiguration, loci.IntensionalConfiguration),
        ):
            raise ProgramCompatibilityError(
                "Seed contains an unrecognized configuration"
            )
        if not program.seed.configuration_contract.accepts(
            configuration.contract
        ):
            raise ProgramCompatibilityError(
                "Seed configuration violates its output contract"
            )
        if isinstance(configuration, loci.FiniteConfiguration):
            for _, value in configuration.entries:
                try:
                    program.alphabet.require(
                        cast(alphabets.SemanticValue, value)
                    )
                except ValueError as error:
                    raise ProgramCompatibilityError(
                        "Seed value does not conform to Alphabet"
                    ) from error
            boundary = configuration.carrier.boundary
            if boundary.policy is loci.BoundaryPolicy.FIXED:
                try:
                    program.alphabet.require(
                        cast(alphabets.SemanticValue, boundary.exterior)
                    )
                except ValueError as error:
                    raise ProgramCompatibilityError(
                        "Seed boundary value does not conform to Alphabet"
                    ) from error

    def require_construction(construction: seeds.Construction) -> None:
        arguments = construction.arguments
        values: tuple[alphabets.SemanticValue, ...] = ()
        if construction.operation is seeds.ConstructionOp.FILL and arguments:
            values = (cast(alphabets.SemanticValue, arguments[0]),)
        elif construction.operation is seeds.ConstructionOp.POINT and arguments:
            values = (cast(alphabets.SemanticValue, arguments[-1]),)
        elif construction.operation is seeds.ConstructionOp.SEQUENCE and arguments:
            values = cast(tuple[alphabets.SemanticValue, ...], arguments[0])
        elif construction.operation is seeds.ConstructionOp.RECORD and arguments:
            fields_value = cast(
                tuple[tuple[str, alphabets.SemanticValue], ...],
                arguments[0],
            )
            values = tuple(value for _, value in fields_value)
        elif construction.operation is seeds.ConstructionOp.GRID and len(arguments) >= 2:
            values = cast(tuple[alphabets.SemanticValue, ...], arguments[1])
            boundary_fields = dict(
                cast(
                    tuple[tuple[str, alphabets.SemanticValue], ...],
                    arguments[2],
                )
            )
            if "exterior" in boundary_fields:
                values = (
                    *values,
                    cast(
                        alphabets.SemanticValue,
                        boundary_fields["exterior"],
                    ),
                )
        for value in values:
            try:
                program.alphabet.require(value)
            except ValueError as error:
                raise ProgramCompatibilityError(
                    "constructive Seed value does not conform to Alphabet"
                ) from error

    def require_source(source: seeds.SeedSource[object]) -> None:
        if isinstance(source, (seeds.ExactSource, seeds.PartialSource)):
            require_configuration(source.configuration)
        elif isinstance(source, seeds.ConstructiveSource):
            require_construction(source.construction)
        elif isinstance(source, seeds.LawSource):
            if isinstance(source.law, seeds.BernoulliLaw):
                for value in (source.law.false_value, source.law.true_value):
                    try:
                        program.alphabet.require(value)
                    except ValueError as error:
                        raise ProgramCompatibilityError(
                            "Bernoulli Seed value does not conform to Alphabet"
                        ) from error
                if source.law.boundary.policy is loci.BoundaryPolicy.FIXED:
                    try:
                        program.alphabet.require(
                            cast(
                                alphabets.SemanticValue,
                                source.law.boundary.exterior,
                            )
                        )
                    except ValueError as error:
                        raise ProgramCompatibilityError(
                            "Bernoulli boundary does not conform to Alphabet"
                        ) from error
            elif isinstance(source.law, seeds.UniformTupleLaw):
                if not _alphabet_accepts_uniform_values(
                    cast(alphabets.Alphabet[object], program.alphabet),
                    source.law,
                ):
                    raise ProgramCompatibilityError(
                        "uniform Seed value range does not conform to Alphabet"
                    )
            if source.construction is not None:
                require_construction(source.construction)
        elif isinstance(
            source,
            (
                seeds.ProductSource,
                seeds.MixtureSource,
                seeds.ProductLawSource,
            ),
        ):
            for part in source.parts:
                require_source(cast(seeds.SeedSource[object], part.seed.source))
        elif isinstance(source, seeds.OverlaySource):
            for part in source.parts:
                require_source(cast(seeds.SeedSource[object], part.source))
        elif isinstance(source, seeds.RefinedSource):
            require_source(cast(seeds.SeedSource[object], source.source.source))

    require_source(cast(seeds.SeedSource[object], program.seed.source))


class ApplicationPhase(Enum):
    PROGRAM = "program"
    INPUT = "input"
    FRONTIER = "frontier"
    NEIGHBORHOOD = "neighborhood"
    JOIN = "join"
    RULE_DENOTATION = "rule-denotation"
    RESULT_VALIDATION = "result-validation"
    FRESH_BINDING = "fresh-binding"
    COMMIT = "commit"
    SUCCESSOR = "successor"
    QUOTIENT_MEASURE = "quotient-measure"


APPLICATION_PHASES = tuple(phase.value for phase in ApplicationPhase)


@dataclass(frozen=True)
class TraceLineage:
    """Invocation lineage used for replay/evidence, never state semantics."""

    root_identity: str
    path: tuple[str, ...] = ()
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported trace-lineage version {self.version}")
        if not isinstance(self.root_identity, str) or not self.root_identity:
            raise ValueError("trace lineage requires a root identity")
        if type(self.path) is not tuple:
            raise TypeError("trace lineage path must be an immutable tuple")
        if any(not isinstance(edge, str) or not edge for edge in self.path):
            raise ValueError("trace lineage path must contain nonempty identities")

    @property
    def canonical_identity(self) -> str:
        return loci.canonical_identity(self)


@dataclass(frozen=True)
class ApplicationInput(Generic[C]):
    configuration: C
    trace_lineage: TraceLineage | None = None

    def __post_init__(self) -> None:
        if type(self.configuration) not in (
            loci.FiniteConfiguration,
            loci.IntensionalConfiguration,
        ):
            raise TypeError("application input configuration is not recognized")
        if self.trace_lineage is not None and type(self.trace_lineage) is not TraceLineage:
            raise TypeError("trace_lineage must be a recognized TraceLineage")


@dataclass(frozen=True)
class FreshBinding:
    reference: loci.FreshReference
    identity: loci.Locus

    def __post_init__(self) -> None:
        if type(self.reference) is not loci.FreshReference:
            raise TypeError("fresh binding reference is not recognized")
        if type(self.identity) is not loci.Locus:
            raise TypeError("fresh binding identity is not recognized")
        if self.identity.kind is not loci.LocusKind.FRESH:
            raise ValueError("fresh binding must bind a fresh Locus identity")


@dataclass(frozen=True)
class AppliedEvidence:
    application_identity: str
    disposition_identity: str
    version: int = 1

    def __post_init__(self) -> None:
        if type(self.version) is not int or self.version != 1:
            raise ValueError(f"unsupported applied-evidence version {self.version}")
        if any(
            not isinstance(value, str) or not value
            for value in (
                self.application_identity,
                self.disposition_identity,
            )
        ):
            raise ValueError("applied evidence identities cannot be empty")


@dataclass(frozen=True)
class AppliedDerivation(Generic[C]):
    successor: C
    source: rules.Derivation[alphabets.SemanticValue]
    fresh_bindings: tuple[FreshBinding, ...]
    input_trace_lineage: TraceLineage
    output_trace_lineage: TraceLineage
    evidence: AppliedEvidence

    def __post_init__(self) -> None:
        if type(self.successor) not in (
            loci.FiniteConfiguration,
            loci.IntensionalConfiguration,
        ):
            raise TypeError("applied successor configuration is not recognized")
        if type(self.source) is not rules.Derivation:
            raise TypeError("applied derivation source is not recognized")
        if type(self.fresh_bindings) is not tuple or any(
            type(item) is not FreshBinding for item in self.fresh_bindings
        ):
            raise TypeError("fresh bindings must be an immutable tuple")
        if type(self.input_trace_lineage) is not TraceLineage or type(
            self.output_trace_lineage
        ) is not TraceLineage:
            raise TypeError("applied derivation lineage is not recognized")
        if type(self.evidence) is not AppliedEvidence:
            raise TypeError("applied derivation evidence is not recognized")
        if (
            self.input_trace_lineage.root_identity
            != self.output_trace_lineage.root_identity
            or len(self.output_trace_lineage.path)
            != len(self.input_trace_lineage.path) + 1
            or self.output_trace_lineage.path[:-1]
            != self.input_trace_lineage.path
        ):
            raise ValueError("output lineage must extend input lineage once")

    @property
    def canonical_identity(self) -> str:
        return loci.canonical_identity(
            (
                self.source.canonical_identity,
                loci.configuration_identity(self.successor),
                self.fresh_bindings,
                self.input_trace_lineage,
                self.output_trace_lineage,
            )
        )


@dataclass(frozen=True)
class AppliedNoSuccessor:
    source: rules.NoSuccessor
    input_trace_lineage: TraceLineage
    output_trace_lineage: TraceLineage
    evidence: AppliedEvidence

    def __post_init__(self) -> None:
        if type(self.source) is not rules.NoSuccessor:
            raise TypeError("applied no-successor source is not recognized")
        if type(self.input_trace_lineage) is not TraceLineage or type(
            self.output_trace_lineage
        ) is not TraceLineage:
            raise TypeError("applied no-successor lineage is not recognized")
        if type(self.evidence) is not AppliedEvidence:
            raise TypeError("applied no-successor evidence is not recognized")
        if (
            self.input_trace_lineage.root_identity
            != self.output_trace_lineage.root_identity
            or len(self.output_trace_lineage.path)
            != len(self.input_trace_lineage.path) + 1
            or self.output_trace_lineage.path[:-1]
            != self.input_trace_lineage.path
        ):
            raise ValueError("output lineage must extend input lineage once")

    @property
    def canonical_identity(self) -> str:
        return loci.canonical_identity(
            (
                self.source.canonical_identity,
                self.input_trace_lineage,
                self.output_trace_lineage,
            )
        )


AppliedAtom: TypeAlias = AppliedDerivation[C] | AppliedNoSuccessor


@dataclass(frozen=True)
class SuccessorGroup(Generic[C]):
    successor: C
    derivations: tuple[AppliedDerivation[C], ...]

    def __post_init__(self) -> None:
        if type(self.successor) not in (
            loci.FiniteConfiguration,
            loci.IntensionalConfiguration,
        ):
            raise TypeError("successor-group configuration is not recognized")
        if type(self.derivations) is not tuple or any(
            type(item) is not AppliedDerivation for item in self.derivations
        ):
            raise TypeError("successor fiber must be an immutable derivation tuple")
        if not self.derivations:
            raise ValueError("successor group needs a derivation fiber")
        if any(
            not loci.configuration_equal(item.successor, self.successor)
            for item in self.derivations
        ):
            raise ValueError("successor fiber contains a different successor")
        identities = tuple(
            item.canonical_identity for item in self.derivations
        )
        if len(identities) != len(set(identities)):
            raise ValueError("successor fiber repeats a derivation")
        ordered = tuple(
            item
            for _, item in sorted(
                zip(identities, self.derivations, strict=True),
                key=lambda pair: pair[0],
            )
        )
        if tuple(item.canonical_identity for item in ordered) != identities:
            object.__setattr__(self, "derivations", ordered)

    @property
    def canonical_identity(self) -> str:
        return loci.configuration_identity(self.successor)


@dataclass(frozen=True)
class MeasureMass:
    point_identity: str
    mass: Fraction

    def __post_init__(self) -> None:
        if not isinstance(self.point_identity, str) or not self.point_identity:
            raise ValueError("measure point identity cannot be empty")
        if isinstance(self.mass, bool) or not isinstance(self.mass, Fraction):
            raise TypeError("measure mass must be an exact Fraction")
        if self.mass <= 0:
            raise ValueError("measure mass must be positive")


@dataclass(frozen=True)
class ProgramMeasure:
    masses: tuple[MeasureMass, ...]
    total_mass: Fraction | None
    intensional_descriptor: rules.RuleExpr | None = None

    def __post_init__(self) -> None:
        if type(self.masses) is not tuple or any(
            type(item) is not MeasureMass for item in self.masses
        ):
            raise TypeError("measure masses must be a tuple of MeasureMass values")
        point_identities = tuple(item.point_identity for item in self.masses)
        if len(point_identities) != len(set(point_identities)):
            raise ValueError("measure repeats a point identity")
        ordered = tuple(sorted(self.masses, key=lambda item: item.point_identity))
        if tuple(item.point_identity for item in ordered) != point_identities:
            object.__setattr__(self, "masses", ordered)
        if self.total_mass is not None and (
            isinstance(self.total_mass, bool)
            or not isinstance(self.total_mass, Fraction)
        ):
            raise TypeError("measure total must be an exact Fraction or unknown")
        if self.total_mass is not None and (
            self.total_mass < 0 or self.total_mass > 1
        ):
            raise ValueError("submeasure mass must lie in [0, 1]")
        if self.masses and self.intensional_descriptor is not None:
            raise ValueError("measure cannot be finite and intensional together")
        if self.intensional_descriptor is not None:
            if type(self.intensional_descriptor) is not rules.RuleExpr:
                raise TypeError("intensional measure needs a closed RuleExpr")
            if self.total_mass is not None:
                raise ValueError(
                    "an unenumerated submeasure cannot claim a known total"
                )
        if self.masses and sum(
            (item.mass for item in self.masses), Fraction(0)
        ) != self.total_mass:
            raise ValueError("finite measure masses do not match total")
        if not self.masses and self.intensional_descriptor is None:
            if self.total_mass != Fraction(0):
                raise ValueError("an empty finite measure has total mass zero")


@dataclass(frozen=True)
class MeasureAbsent:
    """No source probability law exists."""


@dataclass(frozen=True)
class MeasureAvailable:
    measure: ProgramMeasure

    def __post_init__(self) -> None:
        if type(self.measure) is not ProgramMeasure:
            raise TypeError("available measure payload is not recognized")


@dataclass(frozen=True)
class MeasureUnavailable:
    reason: str
    retained_source_law_and_mapping_evidence: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.reason, str) or not self.reason:
            raise ValueError("unavailable measure needs a reason")
        if type(self.retained_source_law_and_mapping_evidence) is not tuple or any(
            not isinstance(item, str) or not item
            for item in self.retained_source_law_and_mapping_evidence
        ):
            raise TypeError("unavailable measure evidence is not recognized")
        if not self.retained_source_law_and_mapping_evidence:
            raise ValueError("unavailable measure needs reason and retained evidence")


MeasureView: TypeAlias = MeasureAbsent | MeasureAvailable | MeasureUnavailable


@dataclass(frozen=True)
class ApplicationEvidence:
    phases: tuple[ApplicationPhase, ...]
    program_identity: str
    input_configuration_identity: str
    readable_binding_identity: str
    writable_binding_identity: str
    application_identity: str
    canonical_rule_identity: str
    input_trace_lineage_identity: str

    def __post_init__(self) -> None:
        if type(self.phases) is not tuple or any(
            type(phase) is not ApplicationPhase for phase in self.phases
        ):
            raise TypeError("application phases are not recognized")
        if self.phases != tuple(ApplicationPhase):
            raise ValueError("complete application evidence needs every phase")
        identities = (
            self.program_identity,
            self.input_configuration_identity,
            self.readable_binding_identity,
            self.writable_binding_identity,
            self.application_identity,
            self.canonical_rule_identity,
            self.input_trace_lineage_identity,
        )
        if any(not isinstance(item, str) or not item for item in identities):
            raise ValueError("application evidence identities cannot be empty")
        expected_application_identity = loci.canonical_identity(
            (
                self.program_identity,
                self.input_configuration_identity,
                self.readable_binding_identity,
                self.writable_binding_identity,
            )
        )
        if self.application_identity != expected_application_identity:
            raise ValueError(
                "application identity disagrees with its program/input/R/W bindings"
            )


@dataclass(frozen=True)
class ApplicationComplete(Generic[C]):
    source_outcomes: rules.OutcomeSpace[
        rules.Derivation[alphabets.SemanticValue] | rules.NoSuccessor
    ]
    applied_atoms: rules.SupportSpace[AppliedAtom[C]]
    no_successor_partition: rules.SupportSpace[AppliedNoSuccessor]
    outcome_atom_cardinality: rules.Cardinality
    derivation_cardinality: rules.Cardinality
    successor_cardinality: rules.Cardinality
    successor_quotient_with_derivation_fibers: rules.SupportSpace[
        SuccessorGroup[C]
    ]
    applied_atom_measure: MeasureView
    successor_submeasure: MeasureView
    no_successor_submeasure: MeasureView
    evidence: ApplicationEvidence

    def __post_init__(self) -> None:
        if type(self.source_outcomes) is not rules.OutcomeSpace:
            raise TypeError("application source outcomes are not recognized")
        if type(self.applied_atoms) is not rules.SupportSpace:
            raise TypeError("application applied-atom space is not recognized")
        if type(self.no_successor_partition) is not rules.SupportSpace:
            raise TypeError("application no-successor space is not recognized")
        cardinality_types = (
            rules.ExactlyZero,
            rules.ExactlyOne,
            rules.Many,
            rules.Undetermined,
        )
        if any(
            type(value) not in cardinality_types
            for value in (
                self.outcome_atom_cardinality,
                self.derivation_cardinality,
                self.successor_cardinality,
            )
        ):
            raise TypeError("application cardinality variant is not recognized")
        if (
            self.outcome_atom_cardinality
            != self.source_outcomes.support.cardinality
        ):
            raise ValueError("outcome cardinality disagrees with source support")
        if type(
            self.successor_quotient_with_derivation_fibers
        ) is not rules.SupportSpace:
            raise TypeError("successor quotient space is not recognized")
        if (
            self.successor_cardinality
            != self.successor_quotient_with_derivation_fibers.cardinality
        ):
            raise ValueError("successor cardinality disagrees with quotient support")
        measure_types = (MeasureAbsent, MeasureAvailable, MeasureUnavailable)
        if any(
            type(value) not in measure_types
            for value in (
                self.applied_atom_measure,
                self.successor_submeasure,
                self.no_successor_submeasure,
            )
        ):
            raise TypeError("application measure view is not recognized")
        if type(self.evidence) is not ApplicationEvidence:
            raise TypeError("application evidence is not recognized")
        _validate_complete_application(self)


@dataclass(frozen=True)
class ApplicationFault:
    phase: ApplicationPhase
    reason: str
    evidence: tuple[str, ...]
    attempted_phases: tuple[ApplicationPhase, ...]

    def __post_init__(self) -> None:
        if type(self.phase) is not ApplicationPhase:
            raise TypeError("application fault phase is not recognized")
        if not isinstance(self.reason, str) or not self.reason:
            raise ValueError("application fault needs a reason")
        if type(self.evidence) is not tuple or any(
            not isinstance(item, str) or not item for item in self.evidence
        ):
            raise TypeError("application fault evidence is not recognized")
        if type(self.attempted_phases) is not tuple or any(
            type(item) is not ApplicationPhase for item in self.attempted_phases
        ):
            raise TypeError("attempted application phases are not recognized")
        if not self.evidence:
            raise ValueError("application fault needs reason and evidence")
        if not self.attempted_phases or self.attempted_phases[-1] is not self.phase:
            raise ValueError("fault phase must be the final attempted phase")


@dataclass(frozen=True)
class ApplicationRejected:
    fault: ApplicationFault

    def __post_init__(self) -> None:
        if type(self.fault) is not ApplicationFault:
            raise TypeError("application rejection fault is not recognized")


ApplicationResult: TypeAlias = ApplicationComplete[C] | ApplicationRejected


def _rejection(
    phase: ApplicationPhase,
    reason: str,
    attempted: list[ApplicationPhase],
    *evidence: str,
) -> ApplicationRejected:
    return ApplicationRejected(
        ApplicationFault(
            phase,
            reason,
            tuple(evidence) or (reason,),
            tuple(attempted),
        )
    )


def _normalize_input(
    value: C | ApplicationInput[C],
) -> tuple[C, TraceLineage]:
    if isinstance(value, ApplicationInput):
        configuration = value.configuration
        lineage = value.trace_lineage
    else:
        configuration = value
        lineage = None
    identity = loci.configuration_identity(configuration)
    if lineage is None:
        lineage = TraceLineage(
            loci.canonical_identity(("direct-application-root", identity))
        )
    return configuration, lineage


def _validate_configuration(
    configuration: C,
    program: SimpleProgram[C, V, W, R],
) -> None:
    if not isinstance(
        configuration,
        (loci.FiniteConfiguration, loci.IntensionalConfiguration),
    ):
        raise TypeError(
            f"unrecognized configuration variant {type(configuration).__name__}"
        )
    if not program.seed.configuration_contract.accepts(configuration.contract):
        raise ValueError("configuration contract does not match the program")
    if isinstance(configuration, loci.FiniteConfiguration):
        for _, value in configuration.entries:
            program.alphabet.require(cast(alphabets.SemanticValue, value))
        boundary = configuration.carrier.boundary
        if boundary.policy is loci.BoundaryPolicy.FIXED:
            program.alphabet.require(
                cast(alphabets.SemanticValue, boundary.exterior)
            )
    loci.configuration_identity(configuration)


def _validate_join(
    readable: neighborhoods.ResolvedReadableView[alphabets.SemanticValue],
    writable: frontiers.ResolvedWritableCapabilities,
    configuration_identity: str,
    program: SimpleProgram[C, V, W, R],
) -> None:
    if readable.snapshot_identity != configuration_identity:
        raise ValueError("ReadableRegion resolved against a different snapshot")
    if writable.snapshot_identity != configuration_identity:
        raise ValueError("WritableRegion resolved against a different snapshot")
    if readable.snapshot_identity != writable.snapshot_identity:
        raise ValueError("readable and writable bindings disagree")
    if readable.join_shape != program.rule.contract.required_join_shape:
        raise ValueError("resolved readable join shape disagrees with Rule")
    existing_targets = tuple(item.target for item in writable.existing)
    anchors = {
        group.anchor
        for group in readable.groups
        if group.anchor is not None
    }
    if readable.join_shape.mode is neighborhoods.JoinMode.TARGET_IDENTITY:
        if type(writable) is frontiers.IntensionalWritableCapabilities:
            raise ValueError(
                "target-identity joins require enumerable writable targets"
            )
        if anchors != set(existing_targets):
            raise ValueError("target-identity join does not cover writable targets")
    elif readable.join_shape.mode in (
        neighborhoods.JoinMode.ANCHOR_IDENTITY,
        neighborhoods.JoinMode.PRODUCT,
    ):
        if type(writable) is frontiers.IntensionalWritableCapabilities:
            raise ValueError(
                "anchor/product joins require enumerable writable targets"
            )
        # An anchor identifies the read context used by the Rule; it is not
        # necessarily every member of the complete writable envelope.  A
        # temporal macro-rule, for example, reads one current-anchored history
        # group and returns a total disposition over the whole history.
        # Requiring equality here would incorrectly turn Frontier into the
        # firing/read set.  Every realized anchor must still be writable when
        # this join mode claims an R-to-W identity relation.
        if not anchors or not anchors.issubset(set(existing_targets)):
            raise ValueError("read anchors do not belong to the writable envelope")


def _validate_rule_space(
    result: rules.RuleComplete[C, alphabets.SemanticValue],
    writable: frontiers.ResolvedWritableCapabilities,
    alphabet: alphabets.Alphabet[V],
    contract: rules.RuleContract,
) -> rules.OutcomeSpace[
    rules.Derivation[alphabets.SemanticValue] | rules.NoSuccessor
]:
    outcome_space = result.outcome_space
    has_law = outcome_space.probability_law is not None
    declares_law = (
        contract.entropy_interface is seeds.EntropyInterface.REPLAY_KEY
    )
    if has_law != declares_law:
        raise ValueError(
            "Rule probability law disagrees with its entropy interface"
        )
    support = outcome_space.support
    if support.presentation is rules.SupportPresentation.INTENSIONAL:
        if support.relation is None:
            raise ValueError("intensional Rule result has no relation")
        if isinstance(support.cardinality, rules.ExactlyZero):
            raise ValueError(
                "exact-zero Rule denotation requires a typed NoSuccessor atom"
            )
        return outcome_space
    if type(writable) is frontiers.IntensionalWritableCapabilities:
        raise ValueError(
            "an intensional writable envelope requires an intensional Rule result"
        )
    if not support.atoms:
        raise ValueError("bare empty finite Rule result is invalid")
    if any(
        type(atom) not in (rules.Derivation, rules.NoSuccessor)
        for atom in support.atoms
    ):
        raise TypeError("Rule support contains an unknown atom variant")
    atom_ids = tuple(atom.canonical_identity for atom in support.atoms)
    if len(atom_ids) != len(set(atom_ids)):
        raise ValueError("Rule result repeats a witness identity")

    expected_existing = tuple(item.target for item in writable.existing)
    expected_fresh = tuple(item.target for item in writable.fresh)
    for atom in support.atoms:
        if isinstance(atom, rules.NoSuccessor):
            continue
        replacement = atom.replacement
        if tuple(item.target for item in replacement.existing) != expected_existing:
            raise ValueError("disposition is not total over existing capabilities")
        if tuple(item.target for item in replacement.fresh) != expected_fresh:
            raise ValueError("disposition is not total over fresh capabilities")
        for disposition, capability in zip(
            replacement.existing,
            writable.existing,
            strict=True,
        ):
            if (
                disposition.action is rules.DispositionAction.REPLACE
                and (
                    frontiers.Effect.REPLACE not in capability.effects
                    or frontiers.Effect.REPLACE
                    not in contract.required_effect_profile.existing
                )
            ):
                raise ValueError("replacement is not authorized")
            if (
                disposition.action is rules.DispositionAction.DELETE
                and (
                    frontiers.Effect.DELETE not in capability.effects
                    or frontiers.Effect.DELETE
                    not in contract.required_effect_profile.existing
                )
            ):
                raise ValueError("deletion is not authorized")
            if isinstance(disposition.payload, rules.ValuePayload):
                alphabet.require(disposition.payload.value)
        for disposition in replacement.fresh:
            # Presence in ``writable.fresh`` is itself the resolved CREATE
            # capability.  FreshCapability deliberately has no second effect
            # list: its closed sum admits only Absent or Create.
            if disposition.action not in (
                rules.DispositionAction.ABSENT,
                rules.DispositionAction.CREATE,
            ):
                raise ValueError("fresh disposition uses an unauthorized action")
            if (
                disposition.action is rules.DispositionAction.CREATE
                and frontiers.Effect.CREATE
                not in contract.required_effect_profile.fresh
            ):
                raise ValueError("creation is not declared by the Rule")
            if isinstance(disposition.payload, rules.ValuePayload):
                alphabet.require(disposition.payload.value)
    return outcome_space


def _bind_fresh_for_atom(
    atom: rules.Derivation[alphabets.SemanticValue],
    writable: frontiers.WritableCapabilities,
    *,
    input_identity: str,
    rule_identity: str,
    occupied_identities: tuple[loci.Locus, ...],
) -> tuple[FreshBinding, ...]:
    bindings: list[FreshBinding] = []
    for capability in writable.fresh:
        reference = capability.target
        identity = loci.bind_fresh(
            reference,
            input_configuration_identity=input_identity,
            canonical_rule_identity=rule_identity,
            witness_identity=atom.witness.canonical_identity,
        )
        bindings.append(FreshBinding(reference, identity))
    identities = tuple(binding.identity for binding in bindings)
    if len(identities) != len(set(identities)):
        raise ValueError("fresh bindings collide")
    if set(identities).intersection(occupied_identities):
        raise ValueError("fresh binding collides with an existing identity")
    return tuple(bindings)


def _commit(
    configuration: C,
    atom: rules.Derivation[alphabets.SemanticValue],
    bindings: tuple[FreshBinding, ...],
    writable: frontiers.WritableCapabilities,
) -> C:
    if not isinstance(configuration, loci.FiniteConfiguration):
        raise TypeError("finite derivation commit requires FiniteConfiguration")
    if writable.snapshot_identity != configuration.identity:
        raise ValueError("reconstruction plan belongs to a different snapshot")
    disposition_targets = tuple(
        item.target for item in atom.replacement.entries
    )
    lens_targets = tuple(
        lens.target for lens in writable.reconstruction.lenses
    )
    if disposition_targets != lens_targets:
        raise ValueError(
            "reconstruction lenses do not cover the total disposition in order"
        )
    replacement_by_target = {
        disposition.target: disposition
        for disposition in atom.replacement.existing
    }
    structural_bindings = tuple(
        (binding.reference, binding.identity) for binding in bindings
    )

    def bind_value(
        value: alphabets.SemanticValue,
    ) -> alphabets.SemanticValue:
        return alphabets.bind_structural_references(
            value,
            structural_bindings,
        )

    entries: list[tuple[loci.Locus, alphabets.SemanticValue]] = []
    for target, old_value in configuration.entries:
        disposition = replacement_by_target.get(target)
        if disposition is None:
            entries.append((target, cast(alphabets.SemanticValue, old_value)))
            continue
        if disposition.action is rules.DispositionAction.PRESERVE:
            entries.append((target, cast(alphabets.SemanticValue, old_value)))
        elif disposition.action is rules.DispositionAction.REPLACE:
            payload = cast(rules.ValuePayload[alphabets.SemanticValue], disposition.payload)
            entries.append((target, bind_value(payload.value)))
        elif disposition.action is rules.DispositionAction.DELETE:
            continue
        else:
            raise ValueError("existing disposition uses a fresh-only action")

    binding_by_reference = {
        binding.reference: binding.identity for binding in bindings
    }
    for disposition in atom.replacement.fresh:
        if disposition.action is rules.DispositionAction.ABSENT:
            continue
        if disposition.action is not rules.DispositionAction.CREATE:
            raise ValueError("fresh disposition uses an existing-only action")
        bound = binding_by_reference.get(disposition.target)
        if bound is None:
            raise ValueError("fresh creation has no deterministic binding")
        payload = cast(rules.ValuePayload[alphabets.SemanticValue], disposition.payload)
        entries.append((bound, bind_value(payload.value)))

    successor = configuration.with_entries(
        tuple(entries),
        structure=configuration.structure,
    )
    return cast(C, successor)


def _lineage_after(
    input_lineage: TraceLineage,
    application_identity: str,
    atom_identity: str,
    outcome: str,
) -> TraceLineage:
    edge = loci.canonical_identity(
        (
            input_lineage.canonical_identity,
            application_identity,
            atom_identity,
            outcome,
        )
    )
    return TraceLineage(input_lineage.root_identity, (*input_lineage.path, edge))


def _finite_measures(
    law: rules.ProbabilityLaw | None,
    applied: tuple[AppliedAtom[C], ...],
    groups: tuple[SuccessorGroup[C], ...],
) -> tuple[MeasureView, MeasureView, MeasureView]:
    if law is None:
        absent = MeasureAbsent()
        return absent, absent, absent
    if law.presentation is not rules.ProbabilityPresentation.FINITE:
        raise ValueError("finite measure projection needs a finite probability law")

    applied_masses = tuple(
        MeasureMass(
            atom.canonical_identity,
            law.mass_for(atom.source.canonical_identity),
        )
        for atom in applied
        if law.mass_for(atom.source.canonical_identity) > 0
    )
    no_successor_atoms = tuple(
        atom for atom in applied if isinstance(atom, AppliedNoSuccessor)
    )
    no_successor_masses = tuple(
        MeasureMass(
            atom.canonical_identity,
            law.mass_for(atom.source.canonical_identity),
        )
        for atom in no_successor_atoms
        if law.mass_for(atom.source.canonical_identity) > 0
    )
    successor_masses: list[MeasureMass] = []
    for group in groups:
        mass = sum(
            (
                law.mass_for(item.source.canonical_identity)
                for item in group.derivations
            ),
            Fraction(0),
        )
        if mass > 0:
            successor_masses.append(
                MeasureMass(group.canonical_identity, mass)
            )
    successor_total = sum(
        (item.mass for item in successor_masses),
        Fraction(0),
    )
    no_successor_total = sum(
        (item.mass for item in no_successor_masses),
        Fraction(0),
    )
    return (
        MeasureAvailable(ProgramMeasure(applied_masses, Fraction(1))),
        MeasureAvailable(
            ProgramMeasure(tuple(successor_masses), successor_total)
        ),
        MeasureAvailable(
            ProgramMeasure(no_successor_masses, no_successor_total)
        ),
    )


def _quotient(
    derivations: tuple[AppliedDerivation[C], ...],
) -> tuple[SuccessorGroup[C], ...]:
    groups: list[SuccessorGroup[C]] = []
    for derivation in sorted(
        derivations,
        key=lambda item: item.canonical_identity,
    ):
        for index, group in enumerate(groups):
            if loci.configuration_equal(group.successor, derivation.successor):
                groups[index] = SuccessorGroup(
                    group.successor,
                    (*group.derivations, derivation),
                )
                break
        else:
            groups.append(SuccessorGroup(derivation.successor, (derivation,)))
    normalized = tuple(
        SuccessorGroup(
            group.successor,
            tuple(
                sorted(
                    group.derivations,
                    key=lambda item: item.canonical_identity,
                )
            ),
        )
        for group in groups
    )
    return tuple(
        sorted(normalized, key=lambda group: group.canonical_identity)
    )


def _phase_certificate(
    kind: rules.CertificateKind,
    phase: str,
    relation: rules.RuleExpr,
) -> rules.Certificate:
    return rules.Certificate(
        kind,
        rules.RuleExpr(
            rules.ExpressionPrimitive.TUPLE,
            (
                rules.literal_expr(f"application-phase:{phase}"),
                relation,
            ),
        ),
    )


def _tagged_relation(
    label: str,
    *arguments: rules.RuleExpr,
) -> rules.RuleExpr:
    return rules.RuleExpr(
        rules.ExpressionPrimitive.TUPLE,
        (rules.literal_expr(label), *arguments),
    )


def _application_context(
    evidence: ApplicationEvidence,
) -> rules.RuleExpr:
    """Closed invocation data needed to interpret every mapped relation."""

    return _tagged_relation(
        "application-context:v1",
        rules.literal_expr(evidence.program_identity),
        rules.literal_expr(evidence.canonical_rule_identity),
        rules.literal_expr(evidence.input_configuration_identity),
        rules.literal_expr(evidence.readable_binding_identity),
        rules.literal_expr(evidence.writable_binding_identity),
        rules.literal_expr(evidence.input_trace_lineage_identity),
        rules.literal_expr(evidence.application_identity),
    )


def _intensional_projection_relation(
    *,
    phase: str,
    source_relation: rules.RuleExpr,
    evidence: ApplicationEvidence,
) -> rules.RuleExpr:
    """Describe one application-bound projection of a Rule relation.

    The three projections deliberately do not share a generic wrapper.  A
    no-successor partition filters only terminal/failure atoms, while the
    successor quotient filters only derivations before fresh binding, commit,
    validation, lineage extension, and semantic quotienting.
    """

    context = _application_context(evidence)
    source = _tagged_relation("source-rule-relation", source_relation)
    source_conformance = _tagged_relation(
        "map:source-conformance",
        rules.literal_expr(evidence.input_configuration_identity),
        rules.literal_expr(evidence.readable_binding_identity),
        rules.literal_expr(evidence.writable_binding_identity),
    )
    fresh_binding = _tagged_relation(
        "map:fresh-bindings-by-source-witness",
        rules.literal_expr(evidence.input_configuration_identity),
        rules.literal_expr(evidence.canonical_rule_identity),
        rules.literal_expr(evidence.writable_binding_identity),
    )
    commit = _tagged_relation(
        "map:atomic-commit-and-successor-validation",
        rules.literal_expr(evidence.input_configuration_identity),
        rules.literal_expr(evidence.writable_binding_identity),
    )
    lineage = _tagged_relation(
        "map:extend-trace-lineage",
        rules.literal_expr(evidence.input_trace_lineage_identity),
        rules.literal_expr(evidence.application_identity),
    )

    if phase == "applied-atoms":
        pipeline = (
            _tagged_relation("filter:all-rule-atoms", source),
            _tagged_relation(
                "union:typed-applied-atom-branches",
                _tagged_relation(
                    "branch:derivation-to-applied",
                    _tagged_relation("filter:derivation", source),
                    source_conformance,
                    fresh_binding,
                    commit,
                    lineage,
                    _tagged_relation("map:typed-applied-derivation"),
                ),
                _tagged_relation(
                    "branch:no-successor-to-applied",
                    _tagged_relation("filter:no-successor", source),
                    source_conformance,
                    lineage,
                    _tagged_relation("map:typed-applied-no-successor"),
                ),
            ),
        )
    elif phase == "no-successor-partition":
        pipeline = (
            _tagged_relation("filter:no-successor", source),
            source_conformance,
            lineage,
            _tagged_relation("map:typed-applied-no-successor"),
        )
    elif phase == "successor-quotient":
        pipeline = (
            _tagged_relation("filter:derivation", source),
            source_conformance,
            fresh_binding,
            commit,
            lineage,
            _tagged_relation(
                "quotient:semantic-successor-with-derivation-fibers"
            ),
        )
    else:
        raise ValueError(f"unknown intensional application projection {phase!r}")

    return _tagged_relation(
        f"application-projection:{phase}:v1",
        context,
        *pipeline,
    )


def _mapped_intensional_support(
    *,
    phase: str,
    source_relation: rules.RuleExpr,
    cardinality: rules.Cardinality,
    evidence: ApplicationEvidence,
) -> rules.SupportSpace[object]:
    mapped_relation = _intensional_projection_relation(
        phase=phase,
        source_relation=source_relation,
        evidence=evidence,
    )
    return rules.intensional_support(
        mapped_relation,
        cardinality,
        completeness_evidence=_phase_certificate(
            rules.CertificateKind.COMPLETENESS,
            phase,
            mapped_relation,
        ),
        soundness_evidence=_phase_certificate(
            rules.CertificateKind.SOUNDNESS,
            phase,
            mapped_relation,
        ),
    )


def _projection_cardinality(
    *,
    phase: str,
    source_relation: rules.RuleExpr,
    evidence: ApplicationEvidence,
) -> rules.Undetermined:
    obligation = _tagged_relation(
        f"application-cardinality:{phase}:v1",
        _application_context(evidence),
        _tagged_relation("source-rule-relation", source_relation),
    )
    return rules.Undetermined(
        obligation,
        rules.Certificate(
            rules.CertificateKind.CARDINALITY,
            obligation,
        ),
    )


def _expected_intensional_spaces(
    source_support: rules.SupportSpace[object],
    evidence: ApplicationEvidence,
    projection_cardinalities: rules.ProjectionCardinalities | None = None,
) -> tuple[
    rules.SupportSpace[object],
    rules.SupportSpace[object],
    rules.Cardinality,
    rules.Cardinality,
    rules.SupportSpace[object],
]:
    if source_support.presentation is not rules.SupportPresentation.INTENSIONAL:
        raise ValueError("intensional application needs intensional source support")
    source_relation = cast(rules.RuleExpr, source_support.relation)
    if projection_cardinalities is None:
        derivation_cardinality = _projection_cardinality(
            phase="derivation",
            source_relation=source_relation,
            evidence=evidence,
        )
        no_successor_cardinality = _projection_cardinality(
            phase="no-successor",
            source_relation=source_relation,
            evidence=evidence,
        )
        successor_cardinality = _projection_cardinality(
            phase="successor-quotient",
            source_relation=source_relation,
            evidence=evidence,
        )
    else:
        derivation_cardinality = projection_cardinalities.derivations
        no_successor_cardinality = projection_cardinalities.no_successors
        successor_cardinality = projection_cardinalities.successors
    applied = _mapped_intensional_support(
        phase="applied-atoms",
        source_relation=source_relation,
        cardinality=source_support.cardinality,
        evidence=evidence,
    )
    no_successor = _mapped_intensional_support(
        phase="no-successor-partition",
        source_relation=source_relation,
        cardinality=no_successor_cardinality,
        evidence=evidence,
    )
    successors = _mapped_intensional_support(
        phase="successor-quotient",
        source_relation=source_relation,
        cardinality=successor_cardinality,
        evidence=evidence,
    )
    return (
        applied,
        no_successor,
        derivation_cardinality,
        successor_cardinality,
        successors,
    )


def _intensional_measures(
    law: rules.ProbabilityLaw | None,
    applied: rules.SupportSpace[object],
    no_successor: rules.SupportSpace[object],
    successors: rules.SupportSpace[object],
    evidence: ApplicationEvidence,
) -> tuple[MeasureView, MeasureView, MeasureView]:
    if law is None:
        absent = MeasureAbsent()
        return absent, absent, absent
    if law.presentation is not rules.ProbabilityPresentation.INTENSIONAL:
        raise ValueError("intensional support needs an intensional probability law")
    descriptor = cast(rules.RuleExpr, law.measure)
    context = _application_context(evidence)
    applied_relation = cast(rules.RuleExpr, applied.relation)
    no_successor_relation = cast(rules.RuleExpr, no_successor.relation)
    successor_relation = cast(rules.RuleExpr, successors.relation)
    applied_measure = MeasureAvailable(
        ProgramMeasure(
            (),
            None,
            _tagged_relation(
                "applied-measure-pushforward:v1",
                context,
                descriptor,
                applied_relation,
            ),
        )
    )
    no_successor_measure = MeasureAvailable(
        ProgramMeasure(
            (),
            None,
            _tagged_relation(
                "no-successor-measure-restriction:v1",
                context,
                descriptor,
                no_successor_relation,
            ),
        )
    )
    successor_measure = MeasureUnavailable(
        "semantic successor quotient measurability is not established",
        (
            law.normalization_evidence.canonical_identity,
            law.measurable_space_evidence.canonical_identity,
            evidence.application_identity,
            successor_relation.canonical_identity,
        ),
    )
    return applied_measure, successor_measure, no_successor_measure


def _validate_finite_application(
    result: ApplicationComplete[object],
) -> None:
    source_support = result.source_outcomes.support
    finite_spaces = (
        result.applied_atoms,
        result.no_successor_partition,
        result.successor_quotient_with_derivation_fibers,
    )
    if any(
        space.presentation is not rules.SupportPresentation.FINITE
        for space in finite_spaces
    ):
        raise ValueError(
            "finite source outcomes require finite application projections"
        )
    if rules.cardinality_size(result.applied_atoms.cardinality) != len(
        source_support.atoms
    ):
        raise ValueError(
            "applied-atom cardinality disagrees with source outcomes"
        )

    source_by_identity: dict[
        str,
        rules.Derivation[alphabets.SemanticValue] | rules.NoSuccessor,
    ] = {}
    for source in source_support.atoms:
        if type(source) not in (rules.Derivation, rules.NoSuccessor):
            raise TypeError("source outcome support contains an unknown atom")
        source_by_identity[source.canonical_identity] = source

    applied = result.applied_atoms.atoms
    if any(
        type(item) not in (AppliedDerivation, AppliedNoSuccessor)
        for item in applied
    ):
        raise TypeError("application support contains an unknown atom")
    applied_source_identities = tuple(
        item.source.canonical_identity for item in applied
    )
    if (
        len(applied_source_identities) != len(set(applied_source_identities))
        or set(applied_source_identities) != set(source_by_identity)
    ):
        raise ValueError(
            "applied atoms are not a one-to-one image of source outcomes"
        )

    for item in applied:
        expected_source = source_by_identity.get(item.source.canonical_identity)
        if expected_source is None or item.source != expected_source:
            raise ValueError(
                "applied atom source does not equal its source-outcome atom"
            )
        if item.evidence.application_identity != result.evidence.application_identity:
            raise ValueError(
                "applied evidence belongs to a different application"
            )
        if (
            item.input_trace_lineage.canonical_identity
            != result.evidence.input_trace_lineage_identity
        ):
            raise ValueError(
                "applied atom input lineage disagrees with application evidence"
            )
        if type(item) is AppliedDerivation:
            if type(expected_source) is not rules.Derivation:
                raise ValueError(
                    "a source no-successor atom mapped to an applied derivation"
                )
            expected_output_lineage = _lineage_after(
                item.input_trace_lineage,
                result.evidence.application_identity,
                item.source.canonical_identity,
                item.source.progress.value,
            )
            if item.output_trace_lineage != expected_output_lineage:
                raise ValueError(
                    "applied derivation output lineage has the wrong edge"
                )
            if (
                item.evidence.disposition_identity
                != item.source.replacement.canonical_identity
            ):
                raise ValueError(
                    "applied derivation evidence names the wrong disposition"
                )
            expected_references = tuple(
                disposition.target
                for disposition in item.source.replacement.fresh
            )
            if tuple(
                binding.reference for binding in item.fresh_bindings
            ) != expected_references:
                raise ValueError(
                    "applied derivation bindings do not cover fresh dispositions"
                )
            expected_binding_identities = tuple(
                loci.bind_fresh(
                    reference,
                    input_configuration_identity=(
                        result.evidence.input_configuration_identity
                    ),
                    canonical_rule_identity=(
                        result.evidence.canonical_rule_identity
                    ),
                    witness_identity=item.source.witness.canonical_identity,
                )
                for reference in expected_references
            )
            if tuple(
                binding.identity for binding in item.fresh_bindings
            ) != expected_binding_identities:
                raise ValueError(
                    "fresh bindings disagree with application/rule/witness identities"
                )
        else:
            if type(expected_source) is not rules.NoSuccessor:
                raise ValueError(
                    "a source derivation mapped to applied no-successor"
                )
            expected_output_lineage = _lineage_after(
                item.input_trace_lineage,
                result.evidence.application_identity,
                item.source.canonical_identity,
                item.source.outcome.value,
            )
            if item.output_trace_lineage != expected_output_lineage:
                raise ValueError(
                    "applied no-successor output lineage has the wrong edge"
                )
            if item.evidence.disposition_identity != "no-disposition":
                raise ValueError(
                    "applied no-successor evidence names a disposition"
                )

    derivations = tuple(
        cast(AppliedDerivation[object], item)
        for item in applied
        if type(item) is AppliedDerivation
    )
    no_successors = tuple(
        cast(AppliedNoSuccessor, item)
        for item in applied
        if type(item) is AppliedNoSuccessor
    )
    if rules.cardinality_size(result.derivation_cardinality) != len(
        derivations
    ):
        raise ValueError(
            "derivation cardinality disagrees with applied derivations"
        )

    expected_applied = rules.finite_support(
        applied,
        label="applied-atoms",
    )
    if result.applied_atoms != expected_applied:
        raise ValueError("applied-atom support evidence is not canonical")
    expected_no_successor = rules.finite_support(
        no_successors,
        label="no-successor-partition",
    )
    if result.no_successor_partition != expected_no_successor:
        raise ValueError(
            "no-successor partition is not the exact filtered projection"
        )

    expected_groups = _quotient(derivations)
    expected_successors = rules.finite_support(
        expected_groups,
        label="successor-quotient",
    )
    if (
        result.successor_quotient_with_derivation_fibers
        != expected_successors
    ):
        raise ValueError(
            "successor quotient does not exactly cover derivation fibers"
        )
    if rules.cardinality_size(result.successor_cardinality) != len(
        expected_groups
    ):
        raise ValueError(
            "successor cardinality disagrees with semantic quotient"
        )

    expected_measures = _finite_measures(
        result.source_outcomes.probability_law,
        cast(tuple[AppliedAtom[object], ...], applied),
        expected_groups,
    )
    actual_measures = (
        result.applied_atom_measure,
        result.successor_submeasure,
        result.no_successor_submeasure,
    )
    if actual_measures != expected_measures:
        raise ValueError(
            "finite application measures disagree with source law and projections"
        )


def _validate_intensional_application(
    result: ApplicationComplete[object],
) -> None:
    source_support = result.source_outcomes.support
    if source_support.presentation is not rules.SupportPresentation.INTENSIONAL:
        raise ValueError("intensional validation received finite source support")
    (
        expected_applied,
        expected_no_successor,
        expected_derivation_cardinality,
        expected_successor_cardinality,
        expected_successors,
    ) = _expected_intensional_spaces(
        cast(rules.SupportSpace[object], source_support),
        result.evidence,
        result.source_outcomes.projection_cardinalities,
    )
    if result.applied_atoms != expected_applied:
        raise ValueError(
            "intensional applied relation is not bound to this application"
        )
    if result.no_successor_partition != expected_no_successor:
        raise ValueError(
            "intensional no-successor relation is not its filtered projection"
        )
    if (
        result.successor_quotient_with_derivation_fibers
        != expected_successors
    ):
        raise ValueError(
            "intensional successor relation is not its derivation quotient"
        )
    if result.outcome_atom_cardinality != source_support.cardinality:
        raise ValueError(
            "intensional outcome cardinality disagrees with source support"
        )
    if result.applied_atoms.cardinality != source_support.cardinality:
        raise ValueError(
            "intensional applied mapping is not cardinality-preserving"
        )
    if result.derivation_cardinality != expected_derivation_cardinality:
        raise ValueError(
            "intensional derivation cardinality is not source-filter bound"
        )
    if result.successor_cardinality != expected_successor_cardinality:
        raise ValueError(
            "intensional successor cardinality is not quotient bound"
        )

    expected_measures = _intensional_measures(
        result.source_outcomes.probability_law,
        expected_applied,
        expected_no_successor,
        expected_successors,
        result.evidence,
    )
    actual_measures = (
        result.applied_atom_measure,
        result.successor_submeasure,
        result.no_successor_submeasure,
    )
    if actual_measures != expected_measures:
        raise ValueError(
            "intensional measures are not bound to application projections"
        )


def _validate_complete_application(
    result: ApplicationComplete[object],
) -> None:
    source_support = result.source_outcomes.support
    if result.outcome_atom_cardinality != source_support.cardinality:
        raise ValueError("outcome cardinality disagrees with source support")
    if source_support.presentation is rules.SupportPresentation.FINITE:
        _validate_finite_application(result)
    else:
        _validate_intensional_application(result)


def _intensional_application(
    outcome_space: rules.OutcomeSpace[
        rules.Derivation[alphabets.SemanticValue] | rules.NoSuccessor
    ],
    evidence: ApplicationEvidence,
) -> ApplicationComplete[C]:
    support = outcome_space.support
    (
        untyped_applied,
        untyped_no_successor,
        derivation_cardinality,
        successor_cardinality,
        untyped_successors,
    ) = _expected_intensional_spaces(
        cast(rules.SupportSpace[object], support),
        evidence,
        outcome_space.projection_cardinalities,
    )
    applied_support = cast(
        rules.SupportSpace[AppliedAtom[C]], untyped_applied
    )
    no_successor = cast(
        rules.SupportSpace[AppliedNoSuccessor], untyped_no_successor
    )
    successors = cast(
        rules.SupportSpace[SuccessorGroup[C]], untyped_successors
    )
    applied_measure, successor_measure, no_successor_measure = _intensional_measures(
        outcome_space.probability_law,
        untyped_applied,
        untyped_no_successor,
        untyped_successors,
        evidence,
    )
    return ApplicationComplete(
        outcome_space,
        applied_support,
        no_successor,
        support.cardinality,
        derivation_cardinality,
        successor_cardinality,
        successors,
        applied_measure,
        successor_measure,
        no_successor_measure,
        evidence,
    )


def apply(
    program: SimpleProgram[C, V, W, R],
    input: C | ApplicationInput[C],
) -> ApplicationResult[C]:
    """Apply one program through the fixed family-blind atomic phase order."""

    attempted: list[ApplicationPhase] = []
    attempted.append(ApplicationPhase.PROGRAM)
    try:
        compatibility = _require_compatible_five_fields(program)
    except (TypeError, ValueError) as error:
        return _rejection(
            ApplicationPhase.PROGRAM,
            str(error),
            attempted,
            type(error).__name__,
        )

    attempted.append(ApplicationPhase.INPUT)
    try:
        configuration, input_lineage = _normalize_input(input)
        _validate_configuration(configuration, program)
        input_identity = loci.configuration_identity(configuration)
    except (TypeError, ValueError) as error:
        return _rejection(
            ApplicationPhase.INPUT,
            str(error),
            attempted,
            type(error).__name__,
        )

    attempted.append(ApplicationPhase.FRONTIER)
    try:
        writable = program.frontier.resolve(configuration)
    except (TypeError, ValueError) as error:
        return _rejection(
            ApplicationPhase.FRONTIER,
            str(error),
            attempted,
            type(error).__name__,
        )

    attempted.append(ApplicationPhase.NEIGHBORHOOD)
    try:
        readable = program.neighborhood.resolve(configuration)
    except (TypeError, ValueError) as error:
        return _rejection(
            ApplicationPhase.NEIGHBORHOOD,
            str(error),
            attempted,
            type(error).__name__,
        )

    attempted.append(ApplicationPhase.JOIN)
    try:
        _validate_join(
            cast(neighborhoods.ReadableView[alphabets.SemanticValue], readable),
            writable,
            input_identity,
            program,
        )
        readable_identity = loci.canonical_identity(readable)
        writable_identity = loci.canonical_identity(writable)
        application_identity = loci.canonical_identity(
            (
                program.canonical_identity,
                input_identity,
                readable_identity,
                writable_identity,
            )
        )
    except (TypeError, ValueError) as error:
        return _rejection(
            ApplicationPhase.JOIN,
            str(error),
            attempted,
            type(error).__name__,
        )

    attempted.append(ApplicationPhase.RULE_DENOTATION)
    rule_result = program.rule.denote(readable, cast(W, writable))
    if isinstance(rule_result, rules.RuleRejected):
        fault_phase = (
            ApplicationPhase.RESULT_VALIDATION
            if rule_result.fault.phase
            in (
                rules.RuleFaultPhase.RESULT_VALIDATION,
                rules.RuleFaultPhase.COMPOSITION,
            )
            else ApplicationPhase.RULE_DENOTATION
        )
        if fault_phase is ApplicationPhase.RESULT_VALIDATION:
            attempted.append(ApplicationPhase.RESULT_VALIDATION)
        return _rejection(
            fault_phase,
            rule_result.fault.detail,
            attempted,
            rule_result.fault.reason.value,
        )

    attempted.append(ApplicationPhase.RESULT_VALIDATION)
    try:
        outcome_space = _validate_rule_space(
            rule_result,
            writable,
            program.alphabet,
            program.rule.contract,
        )
    except (TypeError, ValueError) as error:
        return _rejection(
            ApplicationPhase.RESULT_VALIDATION,
            str(error),
            attempted,
            type(error).__name__,
        )

    attempted.append(ApplicationPhase.FRESH_BINDING)
    support = outcome_space.support
    if support.presentation is rules.SupportPresentation.INTENSIONAL:
        # Binding/reconstruction/validation are retained as closed relation
        # composition rather than forced enumeration.
        attempted.extend(
            (
                ApplicationPhase.COMMIT,
                ApplicationPhase.SUCCESSOR,
                ApplicationPhase.QUOTIENT_MEASURE,
            )
        )
        evidence = ApplicationEvidence(
            tuple(attempted),
            program.canonical_identity,
            input_identity,
            readable_identity,
            writable_identity,
            application_identity,
            program.rule.canonical_identity,
            input_lineage.canonical_identity,
        )
        return _intensional_application(outcome_space, evidence)
    if type(writable) is not frontiers.WritableCapabilities:
        return _rejection(
            ApplicationPhase.RESULT_VALIDATION,
            "a finite Rule result requires enumerable writable capabilities",
            attempted,
            "WritableResolutionError",
        )

    bindings_by_atom: list[
        tuple[
            rules.Derivation[alphabets.SemanticValue] | rules.NoSuccessor,
            tuple[FreshBinding, ...],
        ]
    ] = []
    try:
        for atom in support.atoms:
            bindings = (
                _bind_fresh_for_atom(
                    atom,
                    writable,
                    input_identity=input_identity,
                    rule_identity=program.rule.canonical_identity,
                    occupied_identities=(
                        tuple(target for target, _ in configuration.entries)
                        if isinstance(configuration, loci.FiniteConfiguration)
                        else ()
                    ),
                )
                if isinstance(atom, rules.Derivation)
                else ()
            )
            bindings_by_atom.append((atom, bindings))
    except (TypeError, ValueError) as error:
        return _rejection(
            ApplicationPhase.FRESH_BINDING,
            str(error),
            attempted,
            type(error).__name__,
        )

    attempted.append(ApplicationPhase.COMMIT)
    candidates: list[
        tuple[
            rules.Derivation[alphabets.SemanticValue] | rules.NoSuccessor,
            C | None,
            tuple[FreshBinding, ...],
        ]
    ] = []
    try:
        for atom, bindings in bindings_by_atom:
            successor = (
                _commit(configuration, atom, bindings, writable)
                if isinstance(atom, rules.Derivation)
                else None
            )
            candidates.append((atom, successor, bindings))
    except (TypeError, ValueError) as error:
        return _rejection(
            ApplicationPhase.COMMIT,
            str(error),
            attempted,
            type(error).__name__,
        )

    attempted.append(ApplicationPhase.SUCCESSOR)
    applied: list[AppliedAtom[C]] = []
    try:
        for atom, successor, bindings in candidates:
            if isinstance(atom, rules.NoSuccessor):
                output_lineage = _lineage_after(
                    input_lineage,
                    application_identity,
                    atom.canonical_identity,
                    atom.outcome.value,
                )
                applied.append(
                    AppliedNoSuccessor(
                        atom,
                        input_lineage,
                        output_lineage,
                        AppliedEvidence(
                            application_identity,
                            "no-disposition",
                        ),
                    )
                )
                continue
            assert successor is not None
            _validate_configuration(successor, program)
            if (
                atom.progress is rules.Progress.QUIESCENT
                and not loci.configuration_equal(configuration, successor)
            ):
                raise ValueError("Quiescent derivation changed the configuration")
            output_lineage = _lineage_after(
                input_lineage,
                application_identity,
                atom.canonical_identity,
                atom.progress.value,
            )
            applied.append(
                AppliedDerivation(
                    successor,
                    atom,
                    bindings,
                    input_lineage,
                    output_lineage,
                    AppliedEvidence(
                        application_identity,
                        atom.replacement.canonical_identity,
                    ),
                )
            )
    except (TypeError, ValueError) as error:
        return _rejection(
            ApplicationPhase.SUCCESSOR,
            str(error),
            attempted,
            type(error).__name__,
        )

    attempted.append(ApplicationPhase.QUOTIENT_MEASURE)
    try:
        derivations = tuple(
            atom for atom in applied if isinstance(atom, AppliedDerivation)
        )
        no_successors = tuple(
            atom for atom in applied if isinstance(atom, AppliedNoSuccessor)
        )
        groups = _quotient(derivations)
        applied_measure, successor_measure, no_successor_measure = _finite_measures(
            outcome_space.probability_law,
            tuple(applied),
            groups,
        )
        applied_support = rules.finite_support(
            tuple(applied),
            label="applied-atoms",
        )
        no_successor_support = rules.finite_support(
            no_successors,
            label="no-successor-partition",
        )
        successor_support = rules.finite_support(
            groups,
            label="successor-quotient",
        )
        evidence = ApplicationEvidence(
            tuple(attempted),
            program.canonical_identity,
            input_identity,
            readable_identity,
            writable_identity,
            application_identity,
            program.rule.canonical_identity,
            input_lineage.canonical_identity,
        )
    except (TypeError, ValueError) as error:
        return _rejection(
            ApplicationPhase.QUOTIENT_MEASURE,
            str(error),
            attempted,
            type(error).__name__,
        )

    return ApplicationComplete(
        outcome_space,
        applied_support,
        no_successor_support,
        support.cardinality,
        rules.finite_cardinality(len(derivations)),
        rules.finite_cardinality(len(groups)),
        successor_support,
        applied_measure,
        successor_measure,
        no_successor_measure,
        evidence,
    )


# ---------------------------------------------------------------------------
# Seed realization and traversal derived only from apply
# ---------------------------------------------------------------------------


class SamplerProfile(Enum):
    """Closed deterministic sampler used only after an explicit replay key."""

    SHA256_REJECTION_V1 = "sha256-rejection-v1"


class NumericProfile(Enum):
    """Closed exact arithmetic profile for probability-law realization."""

    FRACTION_TICKETS_V1 = "fraction-tickets-v1"


@dataclass(frozen=True)
class DrawEvidence:
    """Complete replay coordinates for one law realization."""

    law_identity: str
    application_identity: str
    replay_key_identity: str
    subkey_identity: str
    coordinate: tuple[str, ...]
    sampler_profile: SamplerProfile
    numeric_profile: NumericProfile
    selected_witness_identity: str
    rejection_rounds: int
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported draw-evidence version {self.version}")
        strings = (
            self.law_identity,
            self.application_identity,
            self.replay_key_identity,
            self.subkey_identity,
            self.selected_witness_identity,
        )
        if any(not isinstance(item, str) or not item for item in strings):
            raise ValueError("draw evidence identities must be nonempty strings")
        if type(self.coordinate) is not tuple or any(
            not isinstance(item, str) or not item for item in self.coordinate
        ):
            raise TypeError("draw coordinates must be immutable nonempty strings")
        if not isinstance(self.sampler_profile, SamplerProfile):
            raise TypeError("draw sampler profile is not recognized")
        if not isinstance(self.numeric_profile, NumericProfile):
            raise TypeError("draw numeric profile is not recognized")
        if (
            isinstance(self.rejection_rounds, bool)
            or not isinstance(self.rejection_rounds, int)
            or self.rejection_rounds < 0
        ):
            raise ValueError("draw rejection count must be a nonnegative integer")


@dataclass(frozen=True)
class SeedRealizationEvidence(Generic[C]):
    source_identity: str
    replay_key_identity: str | None
    selected_identity: str | None
    denotation: seeds.SeedDenotation[C] | None = None
    draws: tuple[DrawEvidence, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.source_identity, str) or not self.source_identity:
            raise ValueError("Seed evidence needs a source identity")
        if self.replay_key_identity is not None and (
            not isinstance(self.replay_key_identity, str)
            or not self.replay_key_identity
        ):
            raise ValueError("Seed replay-key identity cannot be empty")
        if self.selected_identity is not None and (
            not isinstance(self.selected_identity, str)
            or not self.selected_identity
        ):
            raise ValueError("selected Seed identity cannot be empty")
        if self.denotation is not None and type(
            self.denotation
        ) is not seeds.SeedDenotation:
            raise TypeError("Seed evidence denotation is not recognized")
        if type(self.draws) is not tuple or any(
            type(item) is not DrawEvidence for item in self.draws
        ):
            raise TypeError("Seed draw evidence must be an immutable tuple")
        if self.selected_identity is None and self.draws:
            raise ValueError("Seed draws require a selected realization")


@dataclass(frozen=True)
class ContinuingLeaf(Generic[C]):
    configuration: C
    trace_lineage: TraceLineage

    def __post_init__(self) -> None:
        if type(self.configuration) not in (
            loci.FiniteConfiguration,
            loci.IntensionalConfiguration,
        ):
            raise TypeError("continuing-leaf configuration is not recognized")
        if type(self.trace_lineage) is not TraceLineage:
            raise TypeError("continuing-leaf lineage is not recognized")

    @property
    def canonical_identity(self) -> str:
        return loci.canonical_identity(
            (loci.configuration_identity(self.configuration), self.trace_lineage)
        )


@dataclass(frozen=True)
class ClosedLeaf(Generic[C]):
    final_configuration: C | None
    source: AppliedAtom[C]

    def __post_init__(self) -> None:
        if self.final_configuration is not None and type(
            self.final_configuration
        ) not in (
            loci.FiniteConfiguration,
            loci.IntensionalConfiguration,
        ):
            raise TypeError("closed-leaf configuration is not recognized")
        if type(self.source) not in (AppliedDerivation, AppliedNoSuccessor):
            raise TypeError("closed-leaf source atom is not recognized")
        if (
            type(self.source) is AppliedDerivation
            and self.final_configuration is None
        ):
            raise ValueError("a stopped derivation retains its final configuration")
        if (
            type(self.source) is AppliedNoSuccessor
            and self.final_configuration is not None
        ):
            raise ValueError("a no-successor leaf has no final configuration")

    @property
    def canonical_identity(self) -> str:
        return loci.canonical_identity(
            (
                None
                if self.final_configuration is None
                else loci.configuration_identity(self.final_configuration),
                self.source.canonical_identity,
            )
        )


@dataclass(frozen=True)
class TraceEdge:
    parent_lineage: TraceLineage
    child_lineage: TraceLineage
    applied_atom_identity: str

    def __post_init__(self) -> None:
        if type(self.parent_lineage) is not TraceLineage or type(
            self.child_lineage
        ) is not TraceLineage:
            raise TypeError("trace-edge lineage is not recognized")
        if (
            self.parent_lineage.root_identity
            != self.child_lineage.root_identity
            or len(self.child_lineage.path)
            != len(self.parent_lineage.path) + 1
            or self.child_lineage.path[:-1] != self.parent_lineage.path
        ):
            raise ValueError("trace edge child must extend its parent once")
        if (
            not isinstance(self.applied_atom_identity, str)
            or not self.applied_atom_identity
        ):
            raise ValueError("trace edge needs an applied-atom identity")


@dataclass(frozen=True)
class RawTrace(Generic[C]):
    roots: rules.OutcomeSpace[C]
    applications: rules.SupportSpace[ApplicationComplete[C]]
    derivation_edges: rules.SupportSpace[AppliedAtom[C]]
    lineage_graph: tuple[TraceEdge, ...]
    seed_evidence: SeedRealizationEvidence[C]
    draw_evidence: tuple[DrawEvidence, ...] = ()

    def __post_init__(self) -> None:
        if type(self.roots) is not rules.OutcomeSpace:
            raise TypeError("raw trace roots are not recognized")
        if type(self.applications) is not rules.SupportSpace:
            raise TypeError("raw trace application space is not recognized")
        if type(self.derivation_edges) is not rules.SupportSpace:
            raise TypeError("raw trace edge space is not recognized")
        if (
            self.roots.support.presentation
            is rules.SupportPresentation.FINITE
            and any(
                type(item)
                not in (
                    loci.FiniteConfiguration,
                    loci.IntensionalConfiguration,
                )
                for item in self.roots.support.atoms
            )
        ):
            raise TypeError("raw trace root support contains an unknown value")
        if (
            self.applications.presentation
            is rules.SupportPresentation.FINITE
            and any(
                type(item) is not ApplicationComplete
                for item in self.applications.atoms
            )
        ):
            raise TypeError("raw trace application support contains an unknown value")
        if (
            self.derivation_edges.presentation
            is rules.SupportPresentation.FINITE
            and any(
                type(item) not in (AppliedDerivation, AppliedNoSuccessor)
                for item in self.derivation_edges.atoms
            )
        ):
            raise TypeError("raw trace derivation support contains an unknown value")
        if type(self.lineage_graph) is not tuple or any(
            type(item) is not TraceEdge for item in self.lineage_graph
        ):
            raise TypeError("raw lineage graph is not recognized")
        if (
            self.derivation_edges.presentation
            is rules.SupportPresentation.FINITE
        ):
            edge_identities = {
                item.canonical_identity for item in self.derivation_edges.atoms
            }
            if len(self.lineage_graph) != len(self.derivation_edges.atoms) or any(
                edge.applied_atom_identity not in edge_identities
                for edge in self.lineage_graph
            ):
                raise ValueError(
                    "raw lineage graph must cover every retained derivation edge"
                )
        if type(self.seed_evidence) is not SeedRealizationEvidence:
            raise TypeError("raw trace Seed evidence is not recognized")
        if type(self.draw_evidence) is not tuple or any(
            type(item) is not DrawEvidence for item in self.draw_evidence
        ):
            raise TypeError("raw trace draw evidence is not recognized")


@dataclass(frozen=True)
class RolloutComplete(Generic[C]):
    raw_trace: RawTrace[C]
    closed_leaves: rules.SupportSpace[ClosedLeaf[C]]

    def __post_init__(self) -> None:
        if type(self.raw_trace) is not RawTrace:
            raise TypeError("complete rollout trace is not recognized")
        if type(self.closed_leaves) is not rules.SupportSpace:
            raise TypeError("closed-leaf support is not recognized")
        if (
            self.closed_leaves.presentation
            is not rules.SupportPresentation.FINITE
            or any(
                type(item) is not ClosedLeaf
                for item in self.closed_leaves.atoms
            )
        ):
            raise TypeError("complete rollout needs finite closed leaves")


class TruncationCause(Enum):
    DEPTH_BOUND = "depth-bound"
    INTENSIONAL_SUPPORT = "intensional-support"
    RESOURCE_EXHAUSTED = "resource-exhausted"
    CANCELLED = "cancelled"
    PRUNED = "pruned"


@dataclass(frozen=True)
class RolloutTruncated(Generic[C]):
    raw_trace: RawTrace[C]
    continuing_leaves: rules.SupportSpace[ContinuingLeaf[C]]
    cause: TruncationCause

    def __post_init__(self) -> None:
        if type(self.raw_trace) is not RawTrace:
            raise TypeError("truncated rollout trace is not recognized")
        if type(self.continuing_leaves) is not rules.SupportSpace:
            raise TypeError("continuing-leaf support is not recognized")
        if (
            self.continuing_leaves.presentation
            is rules.SupportPresentation.FINITE
            and any(
                type(item) is not ContinuingLeaf
                for item in self.continuing_leaves.atoms
            )
        ):
            raise TypeError("continuing-leaf support contains an unknown value")
        if type(self.cause) is not TruncationCause:
            raise TypeError("truncation cause is not recognized")


@dataclass(frozen=True)
class RolloutFault:
    reason: str
    evidence: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.reason, str) or not self.reason:
            raise ValueError("rollout fault needs a reason")
        if type(self.evidence) is not tuple or any(
            not isinstance(item, str) or not item for item in self.evidence
        ):
            raise TypeError("rollout fault evidence is not recognized")


@dataclass(frozen=True)
class RolloutRejected:
    fault: RolloutFault

    def __post_init__(self) -> None:
        if type(self.fault) is not RolloutFault:
            raise TypeError("rollout rejection fault is not recognized")


RolloutResult: TypeAlias = (
    RolloutComplete[C] | RolloutTruncated[C] | RolloutRejected
)
ReplayKey: TypeAlias = bool | int | Fraction | str


def _configuration_from_values(
    contract: loci.CarrierContract,
    values: tuple[alphabets.SemanticValue, ...],
    *,
    boundary: loci.Boundary[alphabets.SemanticValue] | None = None,
) -> loci.FiniteConfiguration[alphabets.SemanticValue]:
    if contract.kind is loci.CarrierKind.HISTORY:
        if contract.shape is not None and contract.shape != (len(values),):
            raise ValueError("realized history length disagrees with Seed contract")
        return loci.history_configuration(values)
    if contract.kind is loci.CarrierKind.RECORD:
        if len(values) == 2:
            return loci.record_configuration(
                (("previous", values[0]), ("current", values[1]))
            )
        return loci.record_configuration(
            tuple((f"field-{index}", value) for index, value in enumerate(values))
        )
    if contract.kind is loci.CarrierKind.GRID:
        if contract.shape is None:
            raise ValueError("tuple grid realization requires a concrete shape")
        targets = loci.grid_loci(
            contract.shape,
            axes=contract.axes or None,
        )
        if len(values) != len(targets):
            raise ValueError(
                "realized tuple length disagrees with its grid carrier"
            )
        axes = contract.axes or ("x", "y", "z")[: len(contract.shape)]
        concrete_contract = loci.CarrierContract(
            loci.CarrierKind.GRID,
            rank=len(contract.shape),
            shape=contract.shape,
            axes=axes,
        )
        return loci.FiniteConfiguration(
            loci.Carrier(
                concrete_contract,
                boundary
                if boundary is not None
                else loci.Boundary(loci.BoundaryPolicy.NONE),
            ),
            tuple(zip(targets, values, strict=True)),
        )
    raise ValueError(
        f"tuple realization is unsupported for {contract.kind.value}"
    )


def _construction_targets(
    contract: loci.CarrierContract,
) -> tuple[loci.Locus, ...]:
    if contract.kind is loci.CarrierKind.HISTORY:
        if contract.shape is None or len(contract.shape) != 1:
            raise ValueError("history construction requires a concrete length")
        return tuple(
            loci.occurrence("history", index)
            for index in range(contract.shape[0])
        )
    if contract.kind is loci.CarrierKind.GRID:
        if contract.shape is None:
            raise ValueError("grid construction requires a concrete shape")
        return loci.grid_loci(
            contract.shape,
            axes=contract.axes or None,
        )
    raise ValueError(
        f"carrier {contract.kind.value} has no closed fill target set"
    )


def _realize_construction(
    construction: seeds.Construction,
    contract: loci.CarrierContract,
) -> loci.FiniteConfiguration[alphabets.SemanticValue]:
    operation = construction.operation
    arguments = construction.arguments
    if operation is seeds.ConstructionOp.EMPTY:
        return loci.FiniteConfiguration(
            loci.Carrier(
                contract,
                loci.Boundary(loci.BoundaryPolicy.NONE),
            ),
            (),
        )
    if operation is seeds.ConstructionOp.FILL:
        value = cast(alphabets.SemanticValue, arguments[0])
        targets = _construction_targets(contract)
        return loci.FiniteConfiguration(
            loci.Carrier(
                contract,
                loci.Boundary(loci.BoundaryPolicy.NONE),
            ),
            tuple((target, value) for target in targets),
        )
    if operation is seeds.ConstructionOp.POINT:
        target = cast(loci.Locus, arguments[0])
        value = cast(alphabets.SemanticValue, arguments[1])
        return loci.FiniteConfiguration(
            loci.Carrier(
                contract,
                loci.Boundary(loci.BoundaryPolicy.NONE),
            ),
            ((target, value),),
        )
    if operation is seeds.ConstructionOp.SEQUENCE:
        if not arguments:
            raise ValueError("sequence construction has no values")
        values = cast(tuple[alphabets.SemanticValue, ...], arguments[0])
        return _configuration_from_values(contract, values)
    if operation is seeds.ConstructionOp.RECORD:
        if not arguments:
            raise ValueError("record construction has no fields")
        fields_value = cast(
            tuple[tuple[str, alphabets.SemanticValue], ...],
            arguments[0],
        )
        return loci.record_configuration(fields_value)
    if operation is seeds.ConstructionOp.GRID:
        if not arguments:
            raise ValueError("grid construction has no values")
        shape = cast(tuple[int, ...], arguments[0])
        values = cast(tuple[alphabets.SemanticValue, ...], arguments[1])
        boundary_fields = dict(
            cast(tuple[tuple[str, alphabets.SemanticValue], ...], arguments[2])
        )
        policy = loci.BoundaryPolicy(
            cast(str, boundary_fields["policy"])
        )
        exterior = boundary_fields.get("exterior")
        boundary = loci.Boundary(
            policy,
            exterior if policy is loci.BoundaryPolicy.FIXED else None,
        )
        if contract.shape is not None and contract.shape != shape:
            raise ValueError("grid construction shape disagrees with its contract")
        concrete_contract = loci.CarrierContract(
            loci.CarrierKind.GRID,
            rank=len(shape),
            shape=shape,
            axes=contract.axes or ("x", "y", "z")[: len(shape)],
        )
        if not contract.accepts(concrete_contract):
            raise ValueError("grid construction violates its output contract")
        return _configuration_from_values(
            concrete_contract,
            values,
            boundary=boundary,
        )
    raise ValueError(f"construction {operation.value} has no finite realizer")


def _enumerate_uniform_tuple(
    source: seeds.LawSource,
    contract: loci.CarrierContract,
    value_profile: alphabets.ValueProfile,
) -> tuple[
    tuple[loci.FiniteConfiguration[alphabets.SemanticValue], ...],
    tuple[Fraction, ...],
]:
    law = cast(seeds.UniformTupleLaw, source.law)
    candidates = tuple(
        item
        for item in cartesian_product(range(law.value_count), repeat=law.length)
        if item not in law.excluded
    )
    configurations = tuple(
        _configuration_from_values(
            contract,
            tuple(
                (
                    bool(value)
                    if (
                        law.value_count == 2
                        and value_profile is alphabets.ValueProfile.BOOLEAN
                    )
                    else value
                )
                for value in item
            ),
        )
        for item in candidates
    )
    weight = Fraction(1, len(configurations))
    return configurations, (weight,) * len(configurations)


def _enumerate_bernoulli(
    source: seeds.LawSource,
    contract: loci.CarrierContract,
) -> tuple[
    tuple[loci.FiniteConfiguration[alphabets.SemanticValue], ...],
    tuple[Fraction, ...],
]:
    law = cast(seeds.BernoulliLaw, source.law)
    if law.support.kind is not loci.RegionKind.LITERAL or not law.support.loci:
        raise ValueError("finite Bernoulli realization requires literal support")
    targets = law.support.loci
    if contract.kind is loci.CarrierKind.HISTORY and contract.shape is not None:
        if len(targets) != contract.shape[0]:
            raise ValueError("Bernoulli support size disagrees with its history")
    if contract.kind is loci.CarrierKind.GRID:
        if contract.shape is None:
            raise ValueError("finite Bernoulli grid requires a concrete shape")
        expected_size = 1
        for extent in contract.shape:
            expected_size *= extent
        if len(targets) != expected_size:
            raise ValueError("Bernoulli support size disagrees with its carrier")
        if set(targets) != set(loci.grid_loci(contract.shape)):
            raise ValueError("Bernoulli support does not equal the grid carrier")
    if law.probability_true in (Fraction(0), Fraction(1)):
        selected_value = (
            law.true_value
            if law.probability_true == Fraction(1)
            else law.false_value
        )
        configuration = loci.FiniteConfiguration(
            loci.Carrier(contract, law.boundary),
            tuple((target, selected_value) for target in targets),
        )
        return (configuration,), (Fraction(1),)
    configurations: list[
        loci.FiniteConfiguration[alphabets.SemanticValue]
    ] = []
    weights: list[Fraction] = []
    for bits in cartesian_product((False, True), repeat=len(targets)):
        values = tuple(
            law.true_value if bit else law.false_value for bit in bits
        )
        if contract.kind in (
            loci.CarrierKind.RECORD,
            loci.CarrierKind.HISTORY,
            loci.CarrierKind.GRID,
        ):
            configuration = loci.FiniteConfiguration(
                loci.Carrier(contract, law.boundary),
                tuple(zip(targets, values)),
            )
        else:
            raise ValueError(
                "finite Bernoulli realization needs record/history/grid carrier"
            )
        true_count = sum(bits)
        probability = (
            law.probability_true**true_count
            * (1 - law.probability_true) ** (len(bits) - true_count)
        )
        if probability:
            configurations.append(configuration)
            weights.append(probability)
    return tuple(configurations), tuple(weights)


_MAX_ENUMERATED_SEED_ATOMS = 4096
_MAX_RETAINED_CARDINALITY_BITS = 1_000_000


def _seed_relation(
    denotation: seeds.SeedDenotation[object],
    label: str,
) -> rules.RuleExpr:
    """Reference a retained closed Seed denotation from a support relation."""

    return rules.RuleExpr(
        rules.ExpressionPrimitive.TUPLE,
        (
            rules.literal_expr(label),
            rules.literal_expr(loci.canonical_identity(denotation)),
        ),
    )


def _seed_cardinality(
    denotation: seeds.SeedDenotation[object],
    exact_size: int | None,
) -> rules.Cardinality:
    if exact_size is not None:
        return rules.finite_cardinality(exact_size)
    relation = _seed_relation(denotation, "seed-cardinality")
    return rules.Undetermined(
        relation,
        rules.Certificate(
            rules.CertificateKind.CARDINALITY,
            rules.RuleExpr(
                rules.ExpressionPrimitive.TUPLE,
                (
                    rules.literal_expr("seed-cardinality-obligation"),
                    relation,
                ),
            ),
        ),
    )


def _law_support_size(
    law: seeds.ProbabilityLaw,
) -> int | None:
    if isinstance(law, seeds.UniformTupleLaw):
        estimated_bits = law.length * max(
            1,
            (law.value_count - 1).bit_length(),
        )
        if estimated_bits > _MAX_RETAINED_CARDINALITY_BITS:
            return None
        return law.value_count**law.length - len(law.excluded)
    if isinstance(law, seeds.BernoulliLaw):
        if law.support.kind is not loci.RegionKind.LITERAL:
            return None
        if law.probability_true in (Fraction(0), Fraction(1)):
            return 1
        if len(law.support.loci) > _MAX_RETAINED_CARDINALITY_BITS:
            return None
        return 1 << len(law.support.loci)
    return None


def _intensional_seed_law(
    denotation: seeds.SeedDenotation[object],
) -> rules.ProbabilityLaw:
    measure = _seed_relation(denotation, "seed-probability-law")
    return rules.ProbabilityLaw(
        rules.ProbabilityPresentation.INTENSIONAL,
        (),
        measure,
        rules.Certificate(
            rules.CertificateKind.NORMALIZATION,
            rules.RuleExpr(
                rules.ExpressionPrimitive.TUPLE,
                (rules.literal_expr("seed-law-normalized"), measure),
            ),
        ),
        rules.Certificate(
            rules.CertificateKind.MEASURABILITY,
            rules.RuleExpr(
                rules.ExpressionPrimitive.TUPLE,
                (rules.literal_expr("seed-law-measurable"), measure),
            ),
        ),
    )


def _finite_seed_outcome(
    configurations: tuple[C, ...],
    weights: tuple[Fraction, ...] | None,
) -> rules.OutcomeSpace[C]:
    support = rules.finite_support(configurations, label="seed-roots")
    law: rules.ProbabilityLaw | None = None
    if weights is not None:
        law = rules.ProbabilityLaw(
            rules.ProbabilityPresentation.FINITE,
            tuple(
                rules.AtomMass(
                    loci.configuration_identity(configuration),
                    weight,
                )
                for configuration, weight in zip(
                    configurations,
                    weights,
                    strict=True,
                )
                if weight > 0
            ),
            None,
            rules.Certificate(
                rules.CertificateKind.NORMALIZATION,
                rules.literal_expr("seed-law:normalized"),
            ),
            rules.Certificate(
                rules.CertificateKind.MEASURABILITY,
                rules.literal_expr("seed-law:measurable"),
            ),
        )
    return rules.OutcomeSpace(support, law)


def _denote_seed_space(
    seed: seeds.Seed[C],
) -> tuple[rules.OutcomeSpace[C], seeds.SeedDenotation[C]]:
    """Retain the complete Seed space, enumerating only bounded finite laws."""

    denotation = seed.denote()
    source = denotation.source
    if isinstance(source, seeds.ExactSource):
        return _finite_seed_outcome((source.configuration,), None), denotation
    if isinstance(source, seeds.ConstructiveSource):
        configuration = cast(
            C,
            _realize_construction(
                source.construction,
                seed.configuration_contract,
            ),
        )
        return _finite_seed_outcome((configuration,), None), denotation
    if isinstance(source, seeds.LawSource):
        support_size = _law_support_size(source.law)
        if (
            support_size is not None
            and support_size <= _MAX_ENUMERATED_SEED_ATOMS
        ):
            if isinstance(source.law, seeds.UniformTupleLaw):
                configurations, weights = _enumerate_uniform_tuple(
                    source,
                    seed.configuration_contract,
                    seed.value_profile,
                )
                return (
                    _finite_seed_outcome(
                        cast(tuple[C, ...], configurations),
                        weights,
                    ),
                    denotation,
                )
            if isinstance(source.law, seeds.BernoulliLaw):
                configurations, weights = _enumerate_bernoulli(
                    source,
                    seed.configuration_contract,
                )
                return (
                    _finite_seed_outcome(
                        cast(tuple[C, ...], configurations),
                        weights,
                    ),
                    denotation,
                )

    relation = _seed_relation(
        cast(seeds.SeedDenotation[object], denotation),
        "seed-source-space",
    )
    support = rules.intensional_support(
        relation,
        _seed_cardinality(
            cast(seeds.SeedDenotation[object], denotation),
            (
                _law_support_size(source.law)
                if isinstance(source, seeds.LawSource)
                else None
            ),
        ),
        completeness_evidence=rules.Certificate(
            rules.CertificateKind.COMPLETENESS,
            rules.RuleExpr(
                rules.ExpressionPrimitive.TUPLE,
                (rules.literal_expr("seed-space-complete"), relation),
            ),
        ),
        soundness_evidence=rules.Certificate(
            rules.CertificateKind.SOUNDNESS,
            rules.RuleExpr(
                rules.ExpressionPrimitive.TUPLE,
                (rules.literal_expr("seed-space-sound"), relation),
            ),
        ),
    )
    law = (
        _intensional_seed_law(
            cast(seeds.SeedDenotation[object], denotation)
        )
        if seed.entropy_interface is seeds.EntropyInterface.REPLAY_KEY
        else None
    )
    return (
        rules.OutcomeSpace(cast(rules.SupportSpace[C], support), law),
        denotation,
    )


def _point_identity(value: object) -> str:
    canonical = getattr(value, "canonical_identity", None)
    if isinstance(canonical, str) and canonical:
        return canonical
    if isinstance(value, (loci.FiniteConfiguration, loci.IntensionalConfiguration)):
        return loci.configuration_identity(value)
    return loci.canonical_identity(value)


def _uniform_index(
    total: int,
    *,
    subkey_identity: str,
) -> tuple[int, int]:
    """Map one replay subkey exactly to ``range(total)`` without modulo bias."""

    if isinstance(total, bool) or not isinstance(total, int) or total <= 0:
        raise ValueError("uniform draw range must be a positive integer")
    bit_count = max(1, (total - 1).bit_length())
    block_count = (bit_count + 255) // 256
    mask = (1 << bit_count) - 1
    rejection_round = 0
    while True:
        candidate = 0
        for block in range(block_count):
            material = loci.canonical_identity(
                (
                    SamplerProfile.SHA256_REJECTION_V1.value,
                    subkey_identity,
                    rejection_round,
                    block,
                )
            )
            candidate = (
                candidate << 256
            ) | int.from_bytes(
                hashlib.sha256(material.encode("utf-8")).digest(),
                "big",
            )
        candidate &= mask
        if candidate < total:
            return candidate, rejection_round
        rejection_round += 1


def _select_weighted(
    values: tuple[C, ...],
    weights: tuple[Fraction, ...],
    *,
    law_identity: str,
    application_identity: str,
    replay_key_identity: str,
    coordinate: tuple[str, ...],
) -> tuple[C, DrawEvidence]:
    if not values or len(values) != len(weights):
        raise ValueError("weighted draw needs aligned nonempty values and weights")
    if any(
        isinstance(weight, bool)
        or not isinstance(weight, Fraction)
        or weight < 0
        for weight in weights
    ):
        raise TypeError("weighted draw requires nonnegative exact Fractions")
    denominator = 1
    for weight in weights:
        denominator = lcm(denominator, weight.denominator)
    tickets = tuple(
        weight.numerator * (denominator // weight.denominator)
        for weight in weights
    )
    total = sum(tickets)
    if total <= 0:
        raise ValueError("weighted draw has zero total mass")
    subkey_identity = loci.canonical_identity(
        (
            replay_key_identity,
            application_identity,
            law_identity,
            coordinate,
            SamplerProfile.SHA256_REJECTION_V1.value,
            NumericProfile.FRACTION_TICKETS_V1.value,
        )
    )
    draw, rejection_rounds = _uniform_index(
        total,
        subkey_identity=subkey_identity,
    )
    cumulative = 0
    for value, tickets_for_value in zip(values, tickets, strict=True):
        cumulative += tickets_for_value
        if draw < cumulative:
            selected_identity = _point_identity(value)
            return (
                value,
                DrawEvidence(
                    law_identity,
                    application_identity,
                    replay_key_identity,
                    subkey_identity,
                    coordinate,
                    SamplerProfile.SHA256_REJECTION_V1,
                    NumericProfile.FRACTION_TICKETS_V1,
                    selected_identity,
                    rejection_rounds,
                ),
            )
    raise AssertionError("weighted selection failed")


def _select_uniform_integer(
    upper_bound: int,
    *,
    law_identity: str,
    application_identity: str,
    replay_key_identity: str,
    coordinate: tuple[str, ...],
) -> tuple[int, DrawEvidence]:
    """Draw directly from ``range(upper_bound)`` without materializing it."""

    subkey_identity = loci.canonical_identity(
        (
            replay_key_identity,
            application_identity,
            law_identity,
            coordinate,
            SamplerProfile.SHA256_REJECTION_V1.value,
            NumericProfile.FRACTION_TICKETS_V1.value,
        )
    )
    selected, rejection_rounds = _uniform_index(
        upper_bound,
        subkey_identity=subkey_identity,
    )
    return (
        selected,
        DrawEvidence(
            law_identity,
            application_identity,
            replay_key_identity,
            subkey_identity,
            coordinate,
            SamplerProfile.SHA256_REJECTION_V1,
            NumericProfile.FRACTION_TICKETS_V1,
            _point_identity(selected),
            rejection_rounds,
        ),
    )


def _realize_uniform_tuple(
    seed: seeds.Seed[C],
    source: seeds.LawSource,
    *,
    replay_key_identity: str,
    application_identity: str,
) -> tuple[C, tuple[DrawEvidence, ...]]:
    law = cast(seeds.UniformTupleLaw, source.law)
    law_identity = loci.canonical_identity(law)
    excluded = set(law.excluded)
    attempt = 0
    all_draws: list[DrawEvidence] = []
    while True:
        digits: list[int] = []
        attempt_draws: list[DrawEvidence] = []
        for position in range(law.length):
            selected, evidence = _select_uniform_integer(
                law.value_count,
                law_identity=law_identity,
                application_identity=application_identity,
                replay_key_identity=replay_key_identity,
                coordinate=(
                    "seed",
                    "uniform-tuple",
                    f"attempt:{attempt}",
                    f"position:{position}",
                ),
            )
            digits.append(selected)
            attempt_draws.append(evidence)
        all_draws.extend(attempt_draws)
        selected_tuple = tuple(digits)
        if selected_tuple not in excluded:
            values = tuple(
                bool(value)
                if (
                    law.value_count == 2
                    and seed.value_profile is alphabets.ValueProfile.BOOLEAN
                )
                else value
                for value in selected_tuple
            )
            configuration = _configuration_from_values(
                seed.configuration_contract,
                cast(tuple[alphabets.SemanticValue, ...], values),
            )
            return cast(C, configuration), tuple(all_draws)
        attempt += 1


def _realize_bernoulli(
    seed: seeds.Seed[C],
    source: seeds.LawSource,
    *,
    replay_key_identity: str,
    application_identity: str,
) -> tuple[C, tuple[DrawEvidence, ...]]:
    law = cast(seeds.BernoulliLaw, source.law)
    if law.support.kind is not loci.RegionKind.LITERAL or not law.support.loci:
        raise ValueError("keyed Bernoulli realization requires literal support")
    law_identity = loci.canonical_identity(law)
    values: list[alphabets.SemanticValue] = []
    draws: list[DrawEvidence] = []
    for target in law.support.loci:
        selected, evidence = _select_weighted(
            (law.false_value, law.true_value),
            (Fraction(1) - law.probability_true, law.probability_true),
            law_identity=law_identity,
            application_identity=application_identity,
            replay_key_identity=replay_key_identity,
            coordinate=(
                "seed",
                "bernoulli",
                loci.canonical_identity(target),
            ),
        )
        values.append(selected)
        draws.append(evidence)
    configuration = loci.FiniteConfiguration(
        loci.Carrier(seed.configuration_contract, law.boundary),
        tuple(zip(law.support.loci, values, strict=True)),
    )
    return cast(C, configuration), tuple(draws)


def _realize_seed_with_key(
    seed: seeds.Seed[C],
    *,
    replay_key_identity: str,
    application_identity: str,
) -> tuple[C, tuple[DrawEvidence, ...]]:
    source = seed.denote().source
    if isinstance(source, seeds.ExactSource):
        return source.configuration, ()
    if isinstance(source, seeds.ConstructiveSource):
        return (
            cast(
                C,
                _realize_construction(
                    source.construction,
                    seed.configuration_contract,
                ),
            ),
            (),
        )
    if isinstance(source, seeds.PartialSource):
        raise ValueError(
            "a partial Seed retains unresolved roles and cannot be realized "
            "as a complete finite configuration"
        )
    if isinstance(source, seeds.LawSource):
        if isinstance(source.law, seeds.UniformTupleLaw):
            return _realize_uniform_tuple(
                seed,
                source,
                replay_key_identity=replay_key_identity,
                application_identity=application_identity,
            )
        if isinstance(source.law, seeds.BernoulliLaw):
            return _realize_bernoulli(
                seed,
                source,
                replay_key_identity=replay_key_identity,
                application_identity=application_identity,
            )
        raise ValueError(
            "this closed intensional Seed law has no finite realization profile"
        )
    if isinstance(source, seeds.MixtureSource):
        selected_part, choice = _select_weighted(
            tuple(part.seed for part in source.parts),
            tuple(part.weight for part in source.parts),
            law_identity=loci.canonical_identity(source),
            application_identity=application_identity,
            replay_key_identity=replay_key_identity,
            coordinate=("seed", "mixture-choice"),
        )
        realized, nested = _realize_seed_with_key(
            cast(seeds.Seed[C], selected_part),
            replay_key_identity=replay_key_identity,
            application_identity=loci.canonical_identity(
                (
                    application_identity,
                    choice.subkey_identity,
                    "mixture-part",
                )
            ),
        )
        return realized, (choice, *nested)
    raise ValueError(
        "this closed Seed composition has no generic finite realization profile"
    )


def _root_space(
    program: SimpleProgram[C, V, W, R],
    *,
    initial: C | None,
    replay_key: ReplayKey | None,
) -> tuple[
    rules.OutcomeSpace[C],
    rules.SupportSpace[ContinuingLeaf[C]],
    SeedRealizationEvidence[C],
] | RolloutRejected:
    try:
        denotation: seeds.SeedDenotation[C] | None
        draws: tuple[DrawEvidence, ...] = ()
        if initial is not None:
            _validate_configuration(initial, program)
            roots = _finite_seed_outcome((initial,), None)
            source_identity = "explicit-initial"
            denotation = None
        else:
            roots, denotation = _denote_seed_space(program.seed)
            source_identity = loci.canonical_identity(denotation)
            if roots.support.presentation is rules.SupportPresentation.FINITE:
                for configuration in roots.support.atoms:
                    _validate_configuration(configuration, program)

        replay_identity = (
            None if replay_key is None else loci.canonical_identity(replay_key)
        )
        selected_identity: str | None = None
        if (
            initial is None
            and replay_identity is not None
            and program.seed.entropy_interface
            is seeds.EntropyInterface.REPLAY_KEY
        ):
            selected, draws = _realize_seed_with_key(
                program.seed,
                replay_key_identity=replay_identity,
                application_identity=loci.canonical_identity(
                    (
                        "seed-realization",
                        program.canonical_identity,
                        source_identity,
                    )
                ),
            )
            _validate_configuration(selected, program)
            selected_identity = loci.configuration_identity(selected)
            realized_support: rules.SupportSpace[ContinuingLeaf[C]] = (
                rules.finite_support(
                    (
                        ContinuingLeaf(
                            selected,
                            TraceLineage(
                                loci.canonical_identity(
                                    (
                                        "seed-root",
                                        loci.configuration_identity(selected),
                                    )
                                )
                            ),
                        ),
                    ),
                    label="realized-seed-root",
                )
            )
        elif roots.support.presentation is rules.SupportPresentation.FINITE:
            realized_support = rules.finite_support(
                tuple(
                    ContinuingLeaf(
                        configuration,
                        TraceLineage(
                            loci.canonical_identity(
                                (
                                    "seed-root",
                                    loci.configuration_identity(configuration),
                                )
                            )
                        ),
                    )
                    for configuration in roots.support.atoms
                ),
                label="realized-seed-roots",
            )
        else:
            relation = cast(rules.RuleExpr, roots.support.relation)
            continuing_relation = rules.RuleExpr(
                rules.ExpressionPrimitive.TUPLE,
                (
                    rules.literal_expr("continuing-seed-roots"),
                    relation,
                ),
            )
            realized_support = rules.intensional_support(
                continuing_relation,
                roots.support.cardinality,
                completeness_evidence=rules.Certificate(
                    rules.CertificateKind.COMPLETENESS,
                    rules.RuleExpr(
                        rules.ExpressionPrimitive.TUPLE,
                        (
                            rules.literal_expr(
                                "continuing-seed-roots-complete"
                            ),
                            continuing_relation,
                        ),
                    ),
                ),
                soundness_evidence=rules.Certificate(
                    rules.CertificateKind.SOUNDNESS,
                    rules.RuleExpr(
                        rules.ExpressionPrimitive.TUPLE,
                        (
                            rules.literal_expr(
                                "continuing-seed-roots-sound"
                            ),
                            continuing_relation,
                        ),
                    ),
                ),
            )
        evidence = SeedRealizationEvidence(
            source_identity,
            replay_identity,
            selected_identity,
            denotation,
            draws,
        )
        return roots, realized_support, evidence
    except (TypeError, ValueError) as error:
        return RolloutRejected(
            RolloutFault(str(error), (type(error).__name__,))
        )


def _select_applied_atom(
    result: ApplicationComplete[C],
    lineage: TraceLineage,
    replay_key_identity: str,
) -> tuple[AppliedAtom[C], DrawEvidence]:
    atoms = result.applied_atoms.atoms
    law = result.source_outcomes.probability_law
    if law is None or law.presentation is not rules.ProbabilityPresentation.FINITE:
        raise ValueError("application does not expose a finite realizable law")
    weights = tuple(
        law.mass_for(atom.source.canonical_identity)
        for atom in atoms
    )
    return _select_weighted(
        atoms,
        weights,
        law_identity=loci.canonical_identity(law),
        application_identity=result.evidence.application_identity,
        replay_key_identity=replay_key_identity,
        coordinate=(
            "rule",
            "outcome",
            lineage.canonical_identity,
        ),
    )


def _raw_trace(
    roots: rules.OutcomeSpace[C],
    applications: list[ApplicationComplete[C]],
    edges: list[AppliedAtom[C]],
    lineage_edges: list[TraceEdge],
    seed_evidence: SeedRealizationEvidence[C],
    rule_draws: list[DrawEvidence],
) -> RawTrace[C]:
    return RawTrace(
        roots,
        rules.finite_support(tuple(applications), label="rollout-applications"),
        rules.finite_support(tuple(edges), label="rollout-edges"),
        tuple(lineage_edges),
        seed_evidence,
        (*seed_evidence.draws, *rule_draws),
    )


def rollout(
    program: SimpleProgram[C, V, W, R],
    *,
    steps: int,
    initial: C | None = None,
    replay_key: ReplayKey | None = None,
) -> RolloutResult[C]:
    """Traverse continuing derivation fibers only by invoking ``apply``."""

    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 0:
        return RolloutRejected(
            RolloutFault("steps must be a nonnegative integer")
        )
    roots_result = _root_space(
        program,
        initial=initial,
        replay_key=replay_key,
    )
    if isinstance(roots_result, RolloutRejected):
        return roots_result
    roots, initial_leaf_space, seed_evidence = roots_result

    rule_draws: list[DrawEvidence] = []
    if (
        initial_leaf_space.presentation
        is rules.SupportPresentation.INTENSIONAL
    ):
        trace = _raw_trace(
            roots,
            [],
            [],
            [],
            seed_evidence,
            rule_draws,
        )
        return RolloutTruncated(
            trace,
            initial_leaf_space,
            TruncationCause.INTENSIONAL_SUPPORT,
        )

    continuing = list(initial_leaf_space.atoms)
    closed: list[ClosedLeaf[C]] = []
    applications: list[ApplicationComplete[C]] = []
    edges: list[AppliedAtom[C]] = []
    lineage_edges: list[TraceEdge] = []

    for _depth in range(steps):
        if not continuing:
            break
        next_continuing: list[ContinuingLeaf[C]] = []
        for leaf in continuing:
            result = apply(
                program,
                ApplicationInput(leaf.configuration, leaf.trace_lineage),
            )
            if isinstance(result, ApplicationRejected):
                return RolloutRejected(
                    RolloutFault(
                        result.fault.reason,
                        (
                            result.fault.phase.value,
                            *result.fault.evidence,
                        ),
                    )
                )
            if result.applied_atoms.presentation is not rules.SupportPresentation.FINITE:
                applications.append(result)
                trace = _raw_trace(
                    roots,
                    applications,
                    edges,
                    lineage_edges,
                    seed_evidence,
                    rule_draws,
                )
                relation = cast(rules.RuleExpr, result.applied_atoms.relation)
                continuing_space: rules.SupportSpace[
                    ContinuingLeaf[C]
                ] = rules.intensional_support(
                    rules.RuleExpr(
                        rules.ExpressionPrimitive.TUPLE,
                        (rules.literal_expr("continuing-fibers"), relation),
                    ),
                    rules.Undetermined(
                        rules.literal_expr("continuing-cardinality"),
                        rules.Certificate(
                            rules.CertificateKind.CARDINALITY,
                            rules.literal_expr("continuing-cardinality-obligation"),
                        ),
                    ),
                    completeness_evidence=result.applied_atoms.completeness_evidence,
                    soundness_evidence=result.applied_atoms.soundness_evidence,
                )
                return RolloutTruncated(
                    trace,
                    continuing_space,
                    TruncationCause.INTENSIONAL_SUPPORT,
                )

            chosen_atoms: tuple[AppliedAtom[C], ...]
            if (
                replay_key is not None
                and result.source_outcomes.probability_law is not None
            ):
                replay_identity = loci.canonical_identity(replay_key)
                chosen, draw = _select_applied_atom(
                    result,
                    leaf.trace_lineage,
                    replay_identity,
                )
                chosen_atoms = (chosen,)
                rule_draws.append(draw)
            else:
                chosen_atoms = result.applied_atoms.atoms

            applications.append(result)
            for atom in chosen_atoms:
                edges.append(atom)
                lineage_edges.append(
                    TraceEdge(
                        leaf.trace_lineage,
                        atom.output_trace_lineage,
                        atom.canonical_identity,
                    )
                )
                if isinstance(atom, AppliedNoSuccessor):
                    closed.append(ClosedLeaf(None, atom))
                elif isinstance(atom.source.continuation, rules.Stop):
                    closed.append(ClosedLeaf(atom.successor, atom))
                else:
                    next_continuing.append(
                        ContinuingLeaf(
                            atom.successor,
                            atom.output_trace_lineage,
                        )
                    )
        continuing = next_continuing

    trace = _raw_trace(
        roots,
        applications,
        edges,
        lineage_edges,
        seed_evidence,
        rule_draws,
    )
    if continuing:
        return RolloutTruncated(
            trace,
            rules.finite_support(
                tuple(continuing),
                label="continuing-leaves",
            ),
            TruncationCause.DEPTH_BOUND,
        )
    return RolloutComplete(
        trace,
        rules.finite_support(tuple(closed), label="closed-leaves"),
    )


__all__ = [
    "APPLICATION_PHASES",
    "ApplicationComplete",
    "ApplicationEvidence",
    "ApplicationFault",
    "ApplicationInput",
    "ApplicationPhase",
    "ApplicationRejected",
    "ApplicationResult",
    "AppliedAtom",
    "AppliedDerivation",
    "AppliedNoSuccessor",
    "ClosedLeaf",
    "CompatibilityEvidence",
    "ContinuingLeaf",
    "DrawEvidence",
    "FreshBinding",
    "MeasureAbsent",
    "MeasureAvailable",
    "MeasureMass",
    "MeasureUnavailable",
    "MeasureView",
    "ProgramCompatibilityError",
    "ProgramMeasure",
    "RawTrace",
    "ReplayKey",
    "RolloutComplete",
    "RolloutFault",
    "RolloutRejected",
    "RolloutResult",
    "RolloutTruncated",
    "SeedRealizationEvidence",
    "SamplerProfile",
    "NumericProfile",
    "SimpleProgram",
    "SuccessorGroup",
    "TraceEdge",
    "TraceLineage",
    "TruncationCause",
    "apply",
    "rollout",
]
