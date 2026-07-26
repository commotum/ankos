"""Closed writable capability envelopes.

A :class:`WritableRegion` resolves one immutable configuration into the
complete set of existing and fresh targets a Rule may affect.  It grants no
read access and says nothing about firing sites, scheduling, collisions, or
commit policy.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar

from . import alphabets, loci
from .seeds import ExactnessProfile


C = TypeVar("C")
W = TypeVar("W")


class WritableResolutionError(ValueError):
    """A WritableRegion cannot be resolved against the supplied snapshot."""


class Effect(Enum):
    """Closed effects that a target contract may authorize."""

    REPLACE = "replace"
    DELETE = "delete"
    CREATE = "create"


class WriteFrame(Enum):
    """Which structural frame a capability addresses."""

    CURRENT = "current"
    SUCCESSOR = "successor"


@dataclass(frozen=True)
class EffectProfile:
    """Immutable compatibility declaration for possible Rule effects."""

    existing: tuple[Effect, ...] = (Effect.REPLACE,)
    fresh: tuple[Effect, ...] = ()

    def __post_init__(self) -> None:
        if type(self.existing) is not tuple or type(self.fresh) is not tuple:
            raise TypeError("effect profiles must use immutable tuples")
        if any(type(effect) is not Effect for effect in (*self.existing, *self.fresh)):
            raise TypeError("effect profile contains an unknown effect")
        if len(set(self.existing)) != len(self.existing):
            raise WritableResolutionError("existing effects must be unique")
        if len(set(self.fresh)) != len(self.fresh):
            raise WritableResolutionError("fresh effects must be unique")
        if Effect.CREATE in self.existing:
            raise WritableResolutionError("CREATE cannot target existing structure")
        if any(effect is not Effect.CREATE for effect in self.fresh):
            raise WritableResolutionError("fresh capabilities authorize only CREATE")


@dataclass(frozen=True)
class TargetContract:
    """Value/structure contract attached to each writable capability."""

    locus_kind: loci.LocusKind | None
    value_profile: alphabets.ValueProfile | None
    frame: WriteFrame = WriteFrame.SUCCESSOR

    def __post_init__(self) -> None:
        if self.locus_kind is not None and type(self.locus_kind) is not loci.LocusKind:
            raise TypeError("target locus kind is not recognized")
        if (
            self.value_profile is not None
            and type(self.value_profile) is not alphabets.ValueProfile
        ):
            raise TypeError("value_profile must be alphabets.ValueProfile")
        if type(self.frame) is not WriteFrame:
            raise TypeError("target write frame is not recognized")


@dataclass(frozen=True)
class FreshNamespace:
    """Stable local namespace for possible structural births."""

    namespace: str
    parent: loci.Locus | None = None

    def __post_init__(self) -> None:
        if type(self.namespace) is not str or not self.namespace:
            raise WritableResolutionError("fresh namespace cannot be empty")
        if self.parent is not None and type(self.parent) is not loci.Locus:
            raise TypeError("fresh namespace parent must be a Locus")


@dataclass(frozen=True)
class ReconstructionLens:
    """Closed path used by generic commit; never a host callback."""

    target: loci.Locus | loci.FreshReference
    frame: WriteFrame

    def __post_init__(self) -> None:
        if type(self.target) not in (loci.Locus, loci.FreshReference):
            raise TypeError("reconstruction target is not recognized")
        if type(self.frame) is not WriteFrame:
            raise TypeError("reconstruction frame is not recognized")


@dataclass(frozen=True)
class ReconstructionEvidence:
    """Application-private proof that all target lenses are reconstructible."""

    snapshot_identity: str
    lenses: tuple[ReconstructionLens, ...]
    preserves_outside: bool = True
    complete: bool = True

    def __post_init__(self) -> None:
        if type(self.snapshot_identity) is not str or not self.snapshot_identity:
            raise WritableResolutionError(
                "reconstruction needs a snapshot identity"
            )
        if type(self.lenses) is not tuple or any(
            type(item) is not ReconstructionLens for item in self.lenses
        ):
            raise TypeError("reconstruction lenses are not recognized")
        if type(self.preserves_outside) is not bool or type(self.complete) is not bool:
            raise TypeError("reconstruction proof flags must be booleans")
        if not self.preserves_outside or not self.complete:
            raise WritableResolutionError(
                "writable reconstruction must be complete and preserve outside"
            )


@dataclass(frozen=True)
class ExistingCapability:
    """One existing target that may be preserved/replaced/deleted."""

    target: loci.Locus
    contract: TargetContract
    effects: tuple[Effect, ...]

    def __post_init__(self) -> None:
        if type(self.target) is not loci.Locus:
            raise TypeError("existing capability target must be a bound Locus")
        if type(self.contract) is not TargetContract:
            raise TypeError("existing capability contract is not recognized")
        if type(self.effects) is not tuple or any(
            type(effect) is not Effect for effect in self.effects
        ):
            raise TypeError("existing capability effects are not recognized")
        if not self.effects:
            raise WritableResolutionError("existing capability needs an effect")
        if any(effect is Effect.CREATE for effect in self.effects):
            raise WritableResolutionError("existing capability cannot CREATE")
        if len(set(self.effects)) != len(self.effects):
            raise WritableResolutionError("existing capability effects must be unique")
        if (
            self.contract.locus_kind is not None
            and self.target.kind is not self.contract.locus_kind
        ):
            raise WritableResolutionError(
                "existing target kind violates its target contract"
            )


@dataclass(frozen=True)
class FreshCapability:
    """One potential target that may be absent or created."""

    target: loci.FreshReference
    contract: TargetContract
    namespace: FreshNamespace

    def __post_init__(self) -> None:
        if type(self.target) is not loci.FreshReference:
            raise WritableResolutionError(
                "fresh capability target must be a FreshReference"
            )
        if type(self.contract) is not TargetContract:
            raise TypeError("fresh capability contract is not recognized")
        if type(self.namespace) is not FreshNamespace:
            raise TypeError("fresh capability namespace is not recognized")
        if self.contract.locus_kind not in (None, loci.LocusKind.FRESH):
            raise WritableResolutionError(
                "fresh capability target contract cannot name a non-fresh kind"
            )
        if self.target.namespace != self.namespace.namespace:
            raise WritableResolutionError(
                "fresh capability lies outside its declared namespace"
            )
        if (
            self.namespace.parent is not None
            and self.target.parent != self.namespace.parent
        ):
            raise WritableResolutionError(
                "fresh capability parent violates its namespace"
            )


@dataclass(frozen=True)
class WritableCapabilities:
    """Resolved complete writable envelope for one snapshot."""

    snapshot_identity: str
    existing: tuple[ExistingCapability, ...]
    fresh: tuple[FreshCapability, ...]
    reconstruction: ReconstructionEvidence

    def __post_init__(self) -> None:
        if type(self.snapshot_identity) is not str or not self.snapshot_identity:
            raise WritableResolutionError(
                "writable capabilities need a snapshot identity"
            )
        if type(self.existing) is not tuple or type(self.fresh) is not tuple:
            raise TypeError("writable capabilities must use immutable tuples")
        if any(type(item) is not ExistingCapability for item in self.existing):
            raise TypeError("existing writable capability is not recognized")
        if any(type(item) is not FreshCapability for item in self.fresh):
            raise TypeError("fresh writable capability is not recognized")
        if type(self.reconstruction) is not ReconstructionEvidence:
            raise TypeError("writable reconstruction evidence is not recognized")
        targets = tuple(
            capability.target for capability in (*self.existing, *self.fresh)
        )
        if len(set(targets)) != len(targets):
            raise WritableResolutionError("writable targets must be unique")
        if self.reconstruction.snapshot_identity != self.snapshot_identity:
            raise WritableResolutionError(
                "reconstruction evidence has a different snapshot identity"
            )
        lens_targets = tuple(lens.target for lens in self.reconstruction.lenses)
        if lens_targets != targets:
            raise WritableResolutionError(
                "reconstruction lenses must cover capabilities in order"
            )

    @property
    def targets(self) -> tuple[loci.Locus | loci.FreshReference, ...]:
        return tuple(item.target for item in (*self.existing, *self.fresh))


@dataclass(frozen=True)
class WritableRegion(Generic[C, W]):
    """Closed resolver for one complete possible-write envelope."""

    descriptor: loci.Region
    configuration_contract: loci.CarrierContract | None = None
    value_profile: alphabets.ValueProfile | None = None
    effect_profile: EffectProfile = EffectProfile()
    target_contract: TargetContract = TargetContract(
        None, None, WriteFrame.SUCCESSOR
    )
    fresh_namespace: FreshNamespace | None = None
    exactness_profile: ExactnessProfile = ExactnessProfile.EXACT

    def __post_init__(self) -> None:
        if type(self.descriptor) is not loci.Region:
            raise TypeError("writable descriptor is not recognized")
        if self.configuration_contract is not None and type(
            self.configuration_contract
        ) is not loci.CarrierContract:
            raise TypeError("writable configuration contract is not recognized")
        if self.value_profile is not None and type(
            self.value_profile
        ) is not alphabets.ValueProfile:
            raise TypeError("writable value profile is not recognized")
        if type(self.effect_profile) is not EffectProfile:
            raise TypeError("writable effect profile is not recognized")
        if type(self.target_contract) is not TargetContract:
            raise TypeError("writable target contract is not recognized")
        if self.fresh_namespace is not None and type(
            self.fresh_namespace
        ) is not FreshNamespace:
            raise TypeError("writable fresh namespace is not recognized")
        if type(self.exactness_profile) is not ExactnessProfile:
            raise TypeError("writable exactness profile is not recognized")
        if self.value_profile != self.target_contract.value_profile:
            raise WritableResolutionError(
                "region and target-contract value profiles disagree"
            )
        has_fresh_effect = bool(self.effect_profile.fresh)
        if has_fresh_effect != (self.fresh_namespace is not None):
            raise WritableResolutionError(
                "fresh effects and a fresh namespace must be declared together"
            )

    @property
    def required_effect_profile(self) -> EffectProfile:
        return self.effect_profile

    def resolve(self, configuration: C) -> WritableCapabilities:
        """Resolve independently against one immutable configuration."""

        try:
            if type(configuration) is not loci.FiniteConfiguration:
                raise WritableResolutionError(
                    "finite WritableRegion resolution needs FiniteConfiguration"
                )
            snapshot_identity = configuration.identity
            if (
                self.configuration_contract is not None
                and not self.configuration_contract.accepts(configuration.contract)
            ):
                raise WritableResolutionError(
                    "WritableRegion does not accept this carrier contract"
                )
            targets, fresh_targets = _resolve_targets(
                self.descriptor, configuration
            )
        except (TypeError, ValueError) as error:
            raise WritableResolutionError(str(error)) from error

        if len(set(targets)) != len(targets) or len(set(fresh_targets)) != len(
            fresh_targets
        ):
            raise WritableResolutionError("resolved region contains duplicate targets")

        existing: list[ExistingCapability] = []
        fresh: list[FreshCapability] = []
        lenses: list[ReconstructionLens] = []
        for target in targets:
            if (
                self.target_contract.locus_kind is not None
                and target.kind is not self.target_contract.locus_kind
            ):
                raise WritableResolutionError(
                    "resolved target kind violates the target contract"
                )
            existing.append(
                ExistingCapability(
                    target, self.target_contract, self.effect_profile.existing
                )
            )
            lenses.append(ReconstructionLens(target, self.target_contract.frame))
        for target in fresh_targets:
            if self.fresh_namespace is None:
                raise WritableResolutionError(
                    "region resolved a fresh target without a namespace"
                )
            if target.namespace != self.fresh_namespace.namespace:
                raise WritableResolutionError(
                    "fresh target lies outside the declared namespace"
                )
            if target.parent is not None and not configuration.contains(target.parent):
                raise WritableResolutionError(
                    "fresh target parent is absent from the input configuration"
                )
            if any(
                not configuration.contains(interface)
                for interface in target.interface
            ):
                raise WritableResolutionError(
                    "fresh target interface is absent from the input configuration"
                )
            if (
                self.fresh_namespace.parent is not None
                and target.parent != self.fresh_namespace.parent
            ):
                raise WritableResolutionError(
                    "fresh target parent lies outside the declared namespace"
                )
            capability = FreshCapability(
                target, self.target_contract, self.fresh_namespace
            )
            fresh.append(capability)
            lenses.append(ReconstructionLens(target, self.target_contract.frame))

        if self.effect_profile.fresh and not fresh:
            raise WritableResolutionError(
                "fresh effect profile resolved no fresh capabilities"
            )

        reconstruction = ReconstructionEvidence(
            snapshot_identity,
            tuple(lenses),
        )
        return WritableCapabilities(
            snapshot_identity,
            tuple(existing),
            tuple(fresh),
            reconstruction,
        )


def _resolve_targets(
    region: loci.Region,
    configuration: loci.FiniteConfiguration[object],
) -> tuple[tuple[loci.Locus, ...], tuple[loci.FreshReference, ...]]:
    """Resolve existing and local-fresh identities without binding births."""

    if region.kind is loci.RegionKind.LITERAL:
        existing = tuple(
            target for target in region.loci if configuration.contains(target)
        )
        return existing, region.fresh
    if region.kind in (
        loci.RegionKind.ALL_SUPPORT,
        loci.RegionKind.CURRENT_SUPPORT,
    ):
        return tuple(target for target, _ in configuration.entries), ()
    if region.kind in (loci.RegionKind.UNION, loci.RegionKind.PRODUCT):
        existing: list[loci.Locus] = []
        fresh_targets: list[loci.FreshReference] = []
        seen_existing: set[loci.Locus] = set()
        seen_fresh: set[loci.FreshReference] = set()
        for part in region.parts:
            part_existing, part_fresh = _resolve_targets(part, configuration)
            for target in part_existing:
                if target not in seen_existing:
                    seen_existing.add(target)
                    existing.append(target)
            for target in part_fresh:
                if target not in seen_fresh:
                    seen_fresh.add(target)
                    fresh_targets.append(target)
        return tuple(existing), tuple(fresh_targets)
    if region.kind in (
        loci.RegionKind.FRESH_CHILDREN,
        loci.RegionKind.FRESH_EDGES,
    ):
        return (), region.fresh
    if region.kind is loci.RegionKind.INTENSIONAL:
        raise WritableResolutionError(
            "finite application cannot materialize an intensional writable region"
        )
    try:
        return loci.resolve_region(region, configuration), ()
    except ValueError as error:
        raise WritableResolutionError(str(error)) from error


def literal(
    targets: tuple[loci.Locus, ...],
    *,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: alphabets.ValueProfile | None = None,
    effects: tuple[Effect, ...] = (Effect.REPLACE,),
    frame: WriteFrame = WriteFrame.SUCCESSOR,
) -> WritableRegion[C, WritableCapabilities]:
    """Authorize a literal ordered set of existing targets."""

    if type(targets) is not tuple or any(type(target) is not loci.Locus for target in targets):
        raise TypeError("literal targets must be an immutable tuple of Loci")
    if not targets:
        raise WritableResolutionError("literal targets cannot be empty")
    return WritableRegion(
        loci.literal(targets),
        configuration_contract,
        value_profile,
        EffectProfile(existing=effects),
        TargetContract(None, value_profile, frame),
    )


def everywhere(
    *,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: alphabets.ValueProfile | None = None,
    effects: tuple[Effect, ...] = (Effect.REPLACE,),
) -> WritableRegion[C, WritableCapabilities]:
    """Authorize every existing locus in the current carrier."""

    return WritableRegion(
        loci.all_support(),
        configuration_contract,
        value_profile,
        EffectProfile(existing=effects),
        TargetContract(None, value_profile, WriteFrame.SUCCESSOR),
    )


def next_grid(
    *,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: alphabets.ValueProfile | None = None,
) -> WritableRegion[C, WritableCapabilities]:
    """Authorize the complete grid-shaped successor frame."""

    return WritableRegion(
        loci.all_support(),
        configuration_contract,
        value_profile,
        EffectProfile(existing=(Effect.REPLACE,)),
        TargetContract(None, value_profile, WriteFrame.SUCCESSOR),
    )


def fresh(
    region: loci.Region,
    *,
    namespace: FreshNamespace,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: alphabets.ValueProfile | None = None,
) -> WritableRegion[C, WritableCapabilities]:
    """Authorize a closed region of potential fresh structural targets."""

    if type(region) is not loci.Region:
        raise TypeError("fresh writable region descriptor is not recognized")
    if type(namespace) is not FreshNamespace:
        raise TypeError("fresh writable namespace is not recognized")
    return WritableRegion(
        region,
        configuration_contract,
        value_profile,
        EffectProfile(existing=(), fresh=(Effect.CREATE,)),
        TargetContract(loci.LocusKind.FRESH, value_profile, WriteFrame.SUCCESSOR),
        namespace,
    )


def intensional(
    binder: str,
    relation: loci.SelectorExpr,
    *,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: alphabets.ValueProfile | None = None,
    effects: tuple[Effect, ...] = (Effect.REPLACE,),
) -> WritableRegion[C, WritableCapabilities]:
    """Authorize a closed non-enumerated existing-target region."""

    if type(binder) is not str or not binder:
        raise WritableResolutionError("intensional binder cannot be empty")
    if type(relation) is not loci.SelectorExpr:
        raise TypeError("intensional relation is not recognized")
    return WritableRegion(
        loci.intensional(binder, relation),
        configuration_contract,
        value_profile,
        EffectProfile(existing=effects),
        TargetContract(None, value_profile, WriteFrame.SUCCESSOR),
    )


def union(
    parts: tuple[WritableRegion[C, W], ...],
) -> WritableRegion[C, WritableCapabilities]:
    """Union envelopes after proving their local declarations agree."""

    if type(parts) is not tuple or any(type(part) is not WritableRegion for part in parts):
        raise TypeError("union parts must be an immutable tuple of WritableRegions")
    if not parts:
        raise WritableResolutionError("union needs at least one region")
    first = parts[0]
    for part in parts[1:]:
        if (
            part.configuration_contract != first.configuration_contract
            or part.value_profile != first.value_profile
            or part.target_contract.value_profile
            != first.target_contract.value_profile
            or part.target_contract.frame is not first.target_contract.frame
            or part.exactness_profile is not first.exactness_profile
        ):
            raise WritableResolutionError(
                "union parts have incompatible writable declarations"
            )
    namespaces = tuple(
        part.fresh_namespace
        for part in parts
        if part.fresh_namespace is not None
    )
    if len(set(namespaces)) > 1:
        raise WritableResolutionError(
            "one WritableRegion cannot merge distinct fresh namespaces"
        )
    existing_effects = tuple(
        effect
        for effect in Effect
        if any(effect in part.effect_profile.existing for part in parts)
    )
    fresh_effects = tuple(
        effect
        for effect in Effect
        if any(effect in part.effect_profile.fresh for part in parts)
    )
    profile = EffectProfile(existing_effects, fresh_effects)
    namespace = namespaces[0] if namespaces else None
    return WritableRegion(
        loci.union(tuple(part.descriptor for part in parts)),
        first.configuration_contract,
        first.value_profile,
        profile,
        TargetContract(
            None,
            first.value_profile,
            first.target_contract.frame,
        ),
        namespace,
        first.exactness_profile,
    )


def product(
    fields: tuple[tuple[str, WritableRegion[C, W]], ...],
) -> WritableRegion[C, WritableCapabilities]:
    """Compose disjoint named envelopes without flattening their identity."""

    if type(fields) is not tuple or any(
        type(field) is not tuple
        or len(field) != 2
        or type(field[0]) is not str
        or type(field[1]) is not WritableRegion
        for field in fields
    ):
        raise TypeError(
            "product fields must be immutable (name, WritableRegion) pairs"
        )
    if not fields:
        raise WritableResolutionError("product needs at least one field")
    keys = tuple(key for key, _ in fields)
    if any(not key for key in keys) or len(set(keys)) != len(keys):
        raise WritableResolutionError("product field keys must be nonempty and unique")
    combined = union(tuple(region for _, region in fields))
    return WritableRegion(
        loci.region_product(
            tuple((key, region.descriptor) for key, region in fields)
        ),
        combined.configuration_contract,
        combined.value_profile,
        combined.effect_profile,
        combined.target_contract,
        combined.fresh_namespace,
        combined.exactness_profile,
    )
