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


@dataclass(frozen=True)
class CompatibilityEvidence:
    """Ephemeral proof summary; it is never stored on ``SimpleProgram``."""

    configuration_contract: loci.CarrierContract
    value_profile: alphabets.ValueProfile
    clauses: tuple[str, ...]


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
        (
            "seed-output-unifies",
            "seed-values-conform",
            "frontier-accepts-carrier",
            "neighborhood-accepts-carrier",
            "read-shape-matches",
            "join-shape-matches",
            "effects-fit-frontier",
            "exactness-and-entropy-explicit",
        ),
    )


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
                candidates: tuple[alphabets.SemanticValue, ...] = (
                    (False, True)
                    if (
                        source.law.value_count == 2
                        and program.alphabet.value_profile
                        is alphabets.ValueProfile.BOOLEAN
                    )
                    else tuple(range(source.law.value_count))
                )
                for value in candidates:
                    try:
                        program.alphabet.require(value)
                    except ValueError as error:
                        raise ProgramCompatibilityError(
                            "uniform Seed value does not conform to Alphabet"
                        ) from error
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
        if self.trace_lineage is not None and type(self.trace_lineage) is not TraceLineage:
            raise TypeError("trace_lineage must be a recognized TraceLineage")


@dataclass(frozen=True)
class FreshBinding:
    reference: loci.FreshReference
    identity: loci.Locus


@dataclass(frozen=True)
class AppliedEvidence:
    application_identity: str
    disposition_identity: str
    version: int = 1


@dataclass(frozen=True)
class AppliedDerivation(Generic[C]):
    successor: C
    source: rules.Derivation[alphabets.SemanticValue]
    fresh_bindings: tuple[FreshBinding, ...]
    input_trace_lineage: TraceLineage
    output_trace_lineage: TraceLineage
    evidence: AppliedEvidence

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
        if not self.derivations:
            raise ValueError("successor group needs a derivation fiber")
        if any(
            not loci.semantic_equal(item.successor, self.successor)
            for item in self.derivations
        ):
            raise ValueError("successor fiber contains a different successor")

    @property
    def canonical_identity(self) -> str:
        return loci.configuration_identity(self.successor)


@dataclass(frozen=True)
class MeasureMass:
    point_identity: str
    mass: Fraction

    def __post_init__(self) -> None:
        if not self.point_identity:
            raise ValueError("measure point identity cannot be empty")
        if self.mass <= 0:
            raise ValueError("measure mass must be positive")


@dataclass(frozen=True)
class ProgramMeasure:
    masses: tuple[MeasureMass, ...]
    total_mass: Fraction
    intensional_descriptor: rules.RuleExpr | None = None

    def __post_init__(self) -> None:
        if self.total_mass < 0 or self.total_mass > 1:
            raise ValueError("submeasure mass must lie in [0, 1]")
        if self.masses and self.intensional_descriptor is not None:
            raise ValueError("measure cannot be finite and intensional together")
        if self.masses and sum(
            (item.mass for item in self.masses), Fraction(0)
        ) != self.total_mass:
            raise ValueError("finite measure masses do not match total")


@dataclass(frozen=True)
class MeasureAbsent:
    """No source probability law exists."""


@dataclass(frozen=True)
class MeasureAvailable:
    measure: ProgramMeasure


@dataclass(frozen=True)
class MeasureUnavailable:
    reason: str
    retained_source_law_and_mapping_evidence: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.reason or not self.retained_source_law_and_mapping_evidence:
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

    def __post_init__(self) -> None:
        if self.phases != tuple(ApplicationPhase):
            raise ValueError("complete application evidence needs every phase")


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


@dataclass(frozen=True)
class ApplicationFault:
    phase: ApplicationPhase
    reason: str
    evidence: tuple[str, ...]
    attempted_phases: tuple[ApplicationPhase, ...]

    def __post_init__(self) -> None:
        if not self.reason or not self.evidence:
            raise ValueError("application fault needs reason and evidence")
        if not self.attempted_phases or self.attempted_phases[-1] is not self.phase:
            raise ValueError("fault phase must be the final attempted phase")


@dataclass(frozen=True)
class ApplicationRejected:
    fault: ApplicationFault


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
    readable: neighborhoods.ReadableView[alphabets.SemanticValue],
    writable: frontiers.WritableCapabilities,
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
        if anchors != set(existing_targets):
            raise ValueError("target-identity join does not cover writable targets")
    elif readable.join_shape.mode in (
        neighborhoods.JoinMode.ANCHOR_IDENTITY,
        neighborhoods.JoinMode.PRODUCT,
    ):
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
    writable: frontiers.WritableCapabilities,
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
        return outcome_space
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
) -> C:
    if not isinstance(configuration, loci.FiniteConfiguration):
        raise TypeError("finite derivation commit requires FiniteConfiguration")
    replacement_by_target = {
        disposition.target: disposition
        for disposition in atom.replacement.existing
    }
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
            entries.append((target, payload.value))
        elif disposition.action is rules.DispositionAction.DELETE:
            continue
        else:
            raise ValueError("existing disposition uses a fresh-only action")

    binding_by_reference = {
        binding.reference: binding.identity for binding in bindings
    }
    structure = list(configuration.structure)
    for disposition in atom.replacement.fresh:
        if disposition.action is rules.DispositionAction.ABSENT:
            continue
        if disposition.action is not rules.DispositionAction.CREATE:
            raise ValueError("fresh disposition uses an existing-only action")
        bound = binding_by_reference.get(disposition.target)
        if bound is None:
            raise ValueError("fresh creation has no deterministic binding")
        payload = cast(rules.ValuePayload[alphabets.SemanticValue], disposition.payload)
        entries.append((bound, payload.value))
        reference = cast(loci.FreshReference, disposition.target)
        if reference.parent is not None:
            structure.append(
                loci.StructuralRelation(
                    "fresh-parent",
                    (bound, reference.parent),
                )
            )
        structure.extend(
            loci.StructuralRelation(
                "fresh-interface",
                (bound, interface),
            )
            for interface in reference.interface
        )

    successor = configuration.with_entries(
        tuple(entries),
        structure=tuple(structure),
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
        descriptor = law.measure or rules.literal_expr("intensional-rule-law")
        applied_measure = MeasureAvailable(
            ProgramMeasure((), Fraction(1), descriptor)
        )
        no_successor = MeasureAvailable(
            ProgramMeasure(
                (),
                Fraction(0),
                rules.literal_expr("intensional-no-successor-submeasure"),
            )
        )
        successor = MeasureUnavailable(
            "semantic successor quotient measurability is not established",
            (
                law.normalization_evidence.canonical_identity,
                law.measurable_space_evidence.canonical_identity,
            ),
        )
        return applied_measure, successor, no_successor

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
    for derivation in derivations:
        for index, group in enumerate(groups):
            if loci.semantic_equal(group.successor, derivation.successor):
                groups[index] = SuccessorGroup(
                    group.successor,
                    (*group.derivations, derivation),
                )
                break
        else:
            groups.append(SuccessorGroup(derivation.successor, (derivation,)))
    return tuple(groups)


def _intensional_application(
    outcome_space: rules.OutcomeSpace[
        rules.Derivation[alphabets.SemanticValue] | rules.NoSuccessor
    ],
    evidence: ApplicationEvidence,
) -> ApplicationComplete[C]:
    support = outcome_space.support
    relation = cast(rules.RuleExpr, support.relation)
    unknown = rules.Undetermined(
        rules.literal_expr("application-intensional-cardinality"),
        rules.Certificate(
            rules.CertificateKind.CARDINALITY,
            rules.literal_expr("application-cardinality-obligation"),
        ),
    )
    applied_support: rules.SupportSpace[AppliedAtom[C]] = rules.intensional_support(
        rules.RuleExpr(
            rules.ExpressionPrimitive.TUPLE,
            (rules.literal_expr("applied-map"), relation),
        ),
        unknown,
        completeness_evidence=support.completeness_evidence,
        soundness_evidence=support.soundness_evidence,
    )
    no_successor: rules.SupportSpace[AppliedNoSuccessor] = rules.intensional_support(
        rules.RuleExpr(
            rules.ExpressionPrimitive.TUPLE,
            (rules.literal_expr("no-successor-partition"), relation),
        ),
        unknown,
        completeness_evidence=support.completeness_evidence,
        soundness_evidence=support.soundness_evidence,
    )
    successors: rules.SupportSpace[SuccessorGroup[C]] = rules.intensional_support(
        rules.RuleExpr(
            rules.ExpressionPrimitive.TUPLE,
            (rules.literal_expr("successor-quotient"), relation),
        ),
        unknown,
        completeness_evidence=support.completeness_evidence,
        soundness_evidence=support.soundness_evidence,
    )
    applied_measure, successor_measure, no_successor_measure = _finite_measures(
        outcome_space.probability_law,
        (),
        (),
    )
    return ApplicationComplete(
        outcome_space,
        applied_support,
        no_successor,
        support.cardinality,
        unknown,
        unknown,
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
        )
        return _intensional_application(outcome_space, evidence)

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
                _commit(configuration, atom, bindings)
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
                and not loci.semantic_equal(configuration, successor)
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


@dataclass(frozen=True)
class SeedRealizationEvidence:
    source_identity: str
    replay_key_identity: str | None
    selected_identity: str | None


@dataclass(frozen=True)
class ContinuingLeaf(Generic[C]):
    configuration: C
    trace_lineage: TraceLineage

    @property
    def canonical_identity(self) -> str:
        return loci.canonical_identity(
            (loci.configuration_identity(self.configuration), self.trace_lineage)
        )


@dataclass(frozen=True)
class ClosedLeaf(Generic[C]):
    final_configuration: C | None
    source: AppliedAtom[C]

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


@dataclass(frozen=True)
class RawTrace(Generic[C]):
    roots: rules.OutcomeSpace[C]
    applications: rules.SupportSpace[ApplicationComplete[C]]
    derivation_edges: rules.SupportSpace[AppliedAtom[C]]
    lineage_graph: tuple[TraceEdge, ...]
    seed_evidence: SeedRealizationEvidence


@dataclass(frozen=True)
class RolloutComplete(Generic[C]):
    raw_trace: RawTrace[C]
    closed_leaves: rules.SupportSpace[ClosedLeaf[C]]


class TruncationCause(Enum):
    DEPTH_BOUND = "depth-bound"
    RESOURCE_EXHAUSTED = "resource-exhausted"
    CANCELLED = "cancelled"
    PRUNED = "pruned"


@dataclass(frozen=True)
class RolloutTruncated(Generic[C]):
    raw_trace: RawTrace[C]
    continuing_leaves: rules.SupportSpace[ContinuingLeaf[C]]
    cause: TruncationCause


@dataclass(frozen=True)
class RolloutFault:
    reason: str
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True)
class RolloutRejected:
    fault: RolloutFault


RolloutResult: TypeAlias = (
    RolloutComplete[C] | RolloutTruncated[C] | RolloutRejected
)
ReplayKey: TypeAlias = bool | int | Fraction | str


def _configuration_from_values(
    contract: loci.CarrierContract,
    values: tuple[alphabets.SemanticValue, ...],
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
    raise ValueError(
        f"tuple realization is unsupported for {contract.kind.value}"
    )


def _realize_construction(
    construction: seeds.Construction,
    contract: loci.CarrierContract,
) -> loci.FiniteConfiguration[alphabets.SemanticValue]:
    operation = construction.operation
    arguments = construction.arguments
    if operation is seeds.ConstructionOp.SEQUENCE:
        if not arguments:
            raise ValueError("sequence construction has no values")
        values = cast(tuple[alphabets.SemanticValue, ...], arguments[0])
        return _configuration_from_values(contract, values)
    if operation is seeds.ConstructionOp.RECORD:
        fields_value = cast(
            tuple[tuple[str, alphabets.SemanticValue], ...],
            arguments[0],
        )
        return loci.record_configuration(fields_value)
    if operation is seeds.ConstructionOp.GRID:
        shape = cast(tuple[int, ...], arguments[0])
        values = cast(tuple[alphabets.SemanticValue, ...], arguments[1])
        boundary_fields = dict(
            cast(tuple[tuple[str, alphabets.SemanticValue], ...], arguments[2])
        )
        policy = loci.BoundaryPolicy(str(boundary_fields["policy"]))
        exterior = boundary_fields.get("exterior")
        boundary = loci.Boundary(
            policy,
            exterior if policy is loci.BoundaryPolicy.FIXED else None,
        )
        return loci.grid_configuration(shape, values, boundary=boundary)
    raise ValueError(f"construction {operation.value} has no finite realizer")


def _enumerate_uniform_tuple(
    source: seeds.LawSource,
    contract: loci.CarrierContract,
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
                bool(value) if law.value_count == 2 else value
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


def _finite_seed_space(
    seed: seeds.Seed[C],
) -> tuple[
    tuple[C, ...],
    tuple[Fraction, ...] | None,
]:
    source = seed.denote().source
    if isinstance(source, seeds.ExactSource):
        return (source.configuration,), None
    if isinstance(source, seeds.ConstructiveSource):
        configuration = _realize_construction(
            source.construction,
            seed.configuration_contract,
        )
        return (cast(C, configuration),), None
    if isinstance(source, seeds.PartialSource):
        # Partiality is semantic data, not a request for generic filling.  It
        # may advance when its explicit unresolved values are admitted by the
        # Alphabet and the Rule reads/completes them.
        return (source.configuration,), None
    if isinstance(source, seeds.LawSource):
        if isinstance(source.law, seeds.UniformTupleLaw):
            configurations, weights = _enumerate_uniform_tuple(
                source,
                seed.configuration_contract,
            )
            return cast(tuple[C, ...], configurations), weights
        if isinstance(source.law, seeds.BernoulliLaw):
            configurations, weights = _enumerate_bernoulli(
                source,
                seed.configuration_contract,
            )
            return cast(tuple[C, ...], configurations), weights
    raise ValueError("Seed has a complete non-finite source presentation")


def _select_weighted(
    values: tuple[C, ...],
    weights: tuple[Fraction, ...],
    *,
    key_material: str,
) -> C:
    denominator = 1
    for weight in weights:
        denominator = lcm(denominator, weight.denominator)
    tickets = tuple(
        weight.numerator * (denominator // weight.denominator)
        for weight in weights
    )
    total = sum(tickets)
    digest = hashlib.sha256(key_material.encode("utf-8")).digest()
    draw = int.from_bytes(digest, "big") % total
    cumulative = 0
    for value, tickets_for_value in zip(values, tickets, strict=True):
        cumulative += tickets_for_value
        if draw < cumulative:
            return value
    raise AssertionError("weighted selection failed")


def _root_space(
    program: SimpleProgram[C, V, W, R],
    *,
    initial: C | None,
    replay_key: ReplayKey | None,
) -> tuple[
    rules.OutcomeSpace[C],
    tuple[ContinuingLeaf[C], ...],
    SeedRealizationEvidence,
] | RolloutRejected:
    try:
        if initial is not None:
            _validate_configuration(initial, program)
            configurations = (initial,)
            weights = None
            source_identity = "explicit-initial"
        else:
            configurations, weights = _finite_seed_space(program.seed)
            for configuration in configurations:
                _validate_configuration(configuration, program)
            source_identity = loci.canonical_identity(program.seed)

        replay_identity = (
            None if replay_key is None else loci.canonical_identity(replay_key)
        )
        selected_identity: str | None = None
        realized_configurations = configurations
        if replay_key is not None and weights is not None:
            selected = _select_weighted(
                configurations,
                weights,
                key_material=loci.canonical_identity(
                    (
                        program.canonical_identity,
                        source_identity,
                        replay_key,
                    )
                ),
            )
            realized_configurations = (selected,)
            selected_identity = loci.configuration_identity(selected)

        support = rules.finite_support(configurations, label="seed-roots")
        probability_law: rules.ProbabilityLaw | None = None
        if weights is not None:
            probability_law = rules.ProbabilityLaw(
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
        roots = rules.OutcomeSpace(support, probability_law)
        leaves = tuple(
            ContinuingLeaf(
                configuration,
                TraceLineage(
                    loci.canonical_identity(
                        ("seed-root", loci.configuration_identity(configuration))
                    )
                ),
            )
            for configuration in realized_configurations
        )
        evidence = SeedRealizationEvidence(
            source_identity,
            replay_identity,
            selected_identity,
        )
        return roots, leaves, evidence
    except (TypeError, ValueError) as error:
        return RolloutRejected(
            RolloutFault(str(error), (type(error).__name__,))
        )


def _select_applied_atom(
    result: ApplicationComplete[C],
    lineage: TraceLineage,
    replay_key: ReplayKey,
) -> AppliedAtom[C]:
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
        key_material=loci.canonical_identity(
            (
                replay_key,
                lineage.canonical_identity,
                result.evidence.application_identity,
                "rule-law-draw",
            )
        ),
    )


def _raw_trace(
    roots: rules.OutcomeSpace[C],
    applications: list[ApplicationComplete[C]],
    edges: list[AppliedAtom[C]],
    lineage_edges: list[TraceEdge],
    seed_evidence: SeedRealizationEvidence,
) -> RawTrace[C]:
    return RawTrace(
        roots,
        rules.finite_support(tuple(applications), label="rollout-applications"),
        rules.finite_support(tuple(edges), label="rollout-edges"),
        tuple(lineage_edges),
        seed_evidence,
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
    roots, initial_leaves, seed_evidence = roots_result

    continuing = list(initial_leaves)
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
                trace = _raw_trace(
                    roots,
                    applications,
                    edges,
                    lineage_edges,
                    seed_evidence,
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
                    TruncationCause.DEPTH_BOUND,
                )

            chosen_atoms: tuple[AppliedAtom[C], ...]
            if (
                replay_key is not None
                and result.source_outcomes.probability_law is not None
            ):
                chosen_atoms = (
                    _select_applied_atom(result, leaf.trace_lineage, replay_key),
                )
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
    "SimpleProgram",
    "SuccessorGroup",
    "TraceEdge",
    "TraceLineage",
    "TruncationCause",
    "apply",
    "rollout",
]
