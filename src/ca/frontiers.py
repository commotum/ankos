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

from . import loci
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
    value_profile: tuple[str, ...] | None
    frame: WriteFrame = WriteFrame.SUCCESSOR

    def __post_init__(self) -> None:
        if self.value_profile is not None:
            if not self.value_profile or any(not item for item in self.value_profile):
                raise WritableResolutionError("value_profile cannot be empty")


@dataclass(frozen=True)
class FreshNamespace:
    """Stable local namespace for possible structural births."""

    namespace: str
    parent: loci.Locus | None = None

    def __post_init__(self) -> None:
        if not self.namespace:
            raise WritableResolutionError("fresh namespace cannot be empty")


@dataclass(frozen=True)
class ReconstructionLens:
    """Closed path used by generic commit; never a host callback."""

    target: loci.Locus
    frame: WriteFrame


@dataclass(frozen=True)
class ReconstructionEvidence:
    """Application-private proof that all target lenses are reconstructible."""

    snapshot_identity: loci.ConfigurationIdentity
    lenses: tuple[ReconstructionLens, ...]
    preserves_outside: bool = True
    complete: bool = True

    def __post_init__(self) -> None:
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
        if self.target.kind is loci.LocusKind.FRESH:
            raise WritableResolutionError("existing capability cannot target FRESH")
        if not self.effects:
            raise WritableResolutionError("existing capability needs an effect")
        if any(effect is Effect.CREATE for effect in self.effects):
            raise WritableResolutionError("existing capability cannot CREATE")


@dataclass(frozen=True)
class FreshCapability:
    """One potential target that may be absent or created."""

    target: loci.Locus
    contract: TargetContract
    namespace: FreshNamespace

    def __post_init__(self) -> None:
        if self.target.kind is not loci.LocusKind.FRESH:
            raise WritableResolutionError("fresh capability target must be FRESH")


@dataclass(frozen=True)
class WritableCapabilities:
    """Resolved complete writable envelope for one snapshot."""

    snapshot_identity: loci.ConfigurationIdentity
    existing: tuple[ExistingCapability, ...]
    fresh: tuple[FreshCapability, ...]
    reconstruction: ReconstructionEvidence

    def __post_init__(self) -> None:
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
    def targets(self) -> tuple[loci.Locus, ...]:
        return tuple(item.target for item in (*self.existing, *self.fresh))


@dataclass(frozen=True)
class WritableRegion(Generic[C, W]):
    """Closed resolver for one complete possible-write envelope."""

    descriptor: loci.Region
    configuration_contract: loci.CarrierContract | None = None
    value_profile: tuple[str, ...] | None = None
    effect_profile: EffectProfile = EffectProfile()
    target_contract: TargetContract = TargetContract(
        None, None, WriteFrame.SUCCESSOR
    )
    fresh_namespace: FreshNamespace | None = None
    exactness_profile: ExactnessProfile = ExactnessProfile.EXACT

    def __post_init__(self) -> None:
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
            snapshot_identity = loci.configuration_identity(configuration)
            targets = loci.resolve_region(self.descriptor, configuration)
        except loci.LociResolutionError as error:
            raise WritableResolutionError(str(error)) from error

        if len(set(targets)) != len(targets):
            raise WritableResolutionError("resolved region contains duplicate targets")

        existing: list[ExistingCapability] = []
        fresh: list[FreshCapability] = []
        lenses: list[ReconstructionLens] = []
        for target in targets:
            if target.kind is loci.LocusKind.FRESH:
                if self.fresh_namespace is None:
                    raise WritableResolutionError(
                        "region resolved a fresh target without a namespace"
                    )
                capability = FreshCapability(
                    target, self.target_contract, self.fresh_namespace
                )
                fresh.append(capability)
            else:
                existing.append(
                    ExistingCapability(
                        target, self.target_contract, self.effect_profile.existing
                    )
                )
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


def literal(
    targets: tuple[loci.Locus, ...],
    *,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: tuple[str, ...] | None = None,
    effects: tuple[Effect, ...] = (Effect.REPLACE,),
    frame: WriteFrame = WriteFrame.SUCCESSOR,
) -> WritableRegion[C, WritableCapabilities]:
    """Authorize a literal ordered set of existing targets."""

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
    value_profile: tuple[str, ...] | None = None,
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
    value_profile: tuple[str, ...] | None = None,
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
    value_profile: tuple[str, ...] | None = None,
) -> WritableRegion[C, WritableCapabilities]:
    """Authorize a closed region of potential fresh structural targets."""

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
    value_profile: tuple[str, ...] | None = None,
    effects: tuple[Effect, ...] = (Effect.REPLACE,),
) -> WritableRegion[C, WritableCapabilities]:
    """Authorize a closed non-enumerated existing-target region."""

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

    if not parts:
        raise WritableResolutionError("union needs at least one region")
    first = parts[0]
    for part in parts[1:]:
        if (
            part.configuration_contract != first.configuration_contract
            or part.value_profile != first.value_profile
            or part.effect_profile != first.effect_profile
            or part.target_contract != first.target_contract
            or part.fresh_namespace != first.fresh_namespace
            or part.exactness_profile is not first.exactness_profile
        ):
            raise WritableResolutionError(
                "union parts have incompatible writable declarations"
            )
    return WritableRegion(
        loci.union(tuple(part.descriptor for part in parts)),
        first.configuration_contract,
        first.value_profile,
        first.effect_profile,
        first.target_contract,
        first.fresh_namespace,
        first.exactness_profile,
    )


def product(
    fields: tuple[tuple[str, WritableRegion[C, W]], ...],
) -> WritableRegion[C, WritableCapabilities]:
    """Compose disjoint named envelopes without flattening their identity."""

    if not fields:
        raise WritableResolutionError("product needs at least one field")
    keys = tuple(key for key, _ in fields)
    if any(not key for key in keys) or len(set(keys)) != len(keys):
        raise WritableResolutionError("product field keys must be nonempty and unique")
    return union(tuple(region for _, region in fields))
