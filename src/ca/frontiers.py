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
        existing = tuple(
            effect for effect in Effect if effect in self.existing
        )
        fresh = tuple(effect for effect in Effect if effect in self.fresh)
        if existing != self.existing:
            object.__setattr__(self, "existing", existing)
        if fresh != self.fresh:
            object.__setattr__(self, "fresh", fresh)


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
        capability_frames = tuple(
            capability.contract.frame
            for capability in (*self.existing, *self.fresh)
        )
        lens_frames = tuple(lens.frame for lens in self.reconstruction.lenses)
        if lens_frames != capability_frames:
            raise WritableResolutionError(
                "reconstruction lens frames must match target contracts"
            )

    @property
    def targets(self) -> tuple[loci.Locus | loci.FreshReference, ...]:
        return tuple(item.target for item in (*self.existing, *self.fresh))


@dataclass(frozen=True)
class IntensionalReconstructionEvidence:
    """Closed reconstruction law for a non-enumerated writable envelope."""

    snapshot_identity: str
    region: loci.Region
    target_contract: TargetContract
    preserves_outside: bool = True
    complete: bool = True
    version: int = 1

    def __post_init__(self) -> None:
        if type(self.snapshot_identity) is not str or not self.snapshot_identity:
            raise WritableResolutionError(
                "intensional reconstruction needs a snapshot identity"
            )
        if type(self.region) is not loci.Region:
            raise TypeError("intensional reconstruction region is not recognized")
        if type(self.target_contract) is not TargetContract:
            raise TypeError(
                "intensional reconstruction target contract is not recognized"
            )
        if type(self.preserves_outside) is not bool or type(self.complete) is not bool:
            raise TypeError(
                "intensional reconstruction proof flags must be booleans"
            )
        if not self.preserves_outside or not self.complete:
            raise WritableResolutionError(
                "intensional reconstruction must be complete and preserve outside"
            )
        if type(self.version) is not int or self.version != 1:
            raise WritableResolutionError(
                f"unsupported intensional reconstruction version {self.version!r}"
            )


@dataclass(frozen=True)
class IntensionalWritableCapabilities:
    """One complete, closed, non-enumerated writable capability relation."""

    snapshot_identity: str
    region: loci.Region
    effect_profile: EffectProfile
    target_contract: TargetContract
    reconstruction: IntensionalReconstructionEvidence
    version: int = 1

    def __post_init__(self) -> None:
        if type(self.snapshot_identity) is not str or not self.snapshot_identity:
            raise WritableResolutionError(
                "intensional writable capabilities need a snapshot identity"
            )
        if type(self.region) is not loci.Region:
            raise TypeError("intensional writable region is not recognized")
        if type(self.effect_profile) is not EffectProfile:
            raise TypeError("intensional writable effects are not recognized")
        if not self.effect_profile.existing:
            raise WritableResolutionError(
                "intensional writable capabilities need an existing-target effect"
            )
        if self.effect_profile.fresh:
            raise WritableResolutionError(
                "non-enumerated fresh binding is not an implemented capability"
            )
        if type(self.target_contract) is not TargetContract:
            raise TypeError("intensional writable target contract is not recognized")
        if type(self.reconstruction) is not IntensionalReconstructionEvidence:
            raise TypeError(
                "intensional writable reconstruction evidence is not recognized"
            )
        if (
            self.reconstruction.snapshot_identity != self.snapshot_identity
            or self.reconstruction.region != self.region
            or self.reconstruction.target_contract != self.target_contract
        ):
            raise WritableResolutionError(
                "intensional writable reconstruction disagrees with its envelope"
            )
        if type(self.version) is not int or self.version != 1:
            raise WritableResolutionError(
                f"unsupported intensional writable version {self.version!r}"
            )

    @property
    def existing(self) -> tuple[ExistingCapability, ...]:
        """Finite Rule kernels see no fabricated enumerable capabilities."""

        return ()

    @property
    def fresh(self) -> tuple[FreshCapability, ...]:
        """Fresh identities cannot be invented from an intensional envelope."""

        return ()

    @property
    def targets(self) -> tuple[loci.Locus | loci.FreshReference, ...]:
        """The target set is denoted by ``region`` rather than enumerated."""

        return ()


ResolvedWritableCapabilities = (
    WritableCapabilities | IntensionalWritableCapabilities
)


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
    parts: tuple["WritableRegion[C, W]", ...] = ()
    version: int = 1

    def __post_init__(self) -> None:
        if type(self.version) is not int or self.version != 1:
            raise WritableResolutionError(
                f"unsupported writable-region version {self.version!r}"
            )
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
        if type(self.parts) is not tuple or any(
            type(part) is not WritableRegion for part in self.parts
        ):
            raise TypeError(
                "writable composition parts must contain WritableRegion values"
            )
        if self.value_profile != self.target_contract.value_profile:
            raise WritableResolutionError(
                "region and target-contract value profiles disagree"
            )
        if self.parts:
            if self.descriptor.kind not in (
                loci.RegionKind.UNION,
                loci.RegionKind.PRODUCT,
            ):
                raise WritableResolutionError(
                    "writable composition needs a union or product descriptor"
                )
            if self.descriptor.kind is loci.RegionKind.UNION:
                descriptor_parts = {
                    loci.canonical_identity(part)
                    for part in self.descriptor.parts
                }
                writable_parts = {
                    loci.canonical_identity(part.descriptor)
                    for part in self.parts
                }
                if descriptor_parts != writable_parts:
                    raise WritableResolutionError(
                        "writable union parts disagree with its descriptor"
                    )
            elif len(self.parts) != len(self.descriptor.parts):
                raise WritableResolutionError(
                    "writable product parts disagree with its descriptor"
                )
            if any(
                part.exactness_profile is not self.exactness_profile
                for part in self.parts
            ):
                raise WritableResolutionError(
                    "writable composition exactness declarations disagree"
                )
            expected_effects = _combined_effect_profile(self.parts)
            if self.effect_profile != expected_effects:
                raise WritableResolutionError(
                    "writable composition effect profile is not its part union"
                )
            expected_contract = _common_configuration_contract(self.parts)
            if self.configuration_contract != expected_contract:
                raise WritableResolutionError(
                    "writable composition carrier contract is not its common "
                    "part contract"
                )
            expected_profile = _common_value_profile(self.parts)
            if self.value_profile != expected_profile:
                raise WritableResolutionError(
                    "writable composition value profile is not its common "
                    "part profile"
                )
            namespaces = _part_fresh_namespaces(self.parts)
            expected_namespace = namespaces[0] if len(namespaces) == 1 else None
            if self.fresh_namespace != expected_namespace:
                raise WritableResolutionError(
                    "writable composition legacy namespace does not match its "
                    "part namespaces"
                )
        has_fresh_effect = bool(self.effect_profile.fresh)
        has_fresh_namespace = bool(self.fresh_namespaces)
        if has_fresh_effect != has_fresh_namespace:
            raise WritableResolutionError(
                "fresh effects and fresh namespaces must be declared together"
            )
        if (
            has_fresh_effect
            and not self.parts
            and self.target_contract.locus_kind not in (
                None,
                loci.LocusKind.FRESH,
            )
        ):
            raise WritableResolutionError(
                "fresh effects cannot declare a non-fresh target kind"
            )

    @property
    def required_effect_profile(self) -> EffectProfile:
        return self.effect_profile

    @property
    def fresh_namespaces(self) -> tuple[FreshNamespace, ...]:
        """All declared namespaces, including heterogeneous compositions."""

        if self.parts:
            return _part_fresh_namespaces(self.parts)
        return () if self.fresh_namespace is None else (self.fresh_namespace,)

    def resolve(self, configuration: C) -> ResolvedWritableCapabilities:
        """Resolve independently against one immutable configuration."""

        if self.parts:
            return self._resolve_composition(configuration)

        try:
            if type(configuration) not in (
                loci.FiniteConfiguration,
                loci.IntensionalConfiguration,
            ):
                raise WritableResolutionError(
                    "WritableRegion resolution needs a recognized configuration"
                )
            snapshot_identity = loci.configuration_identity(configuration)
            if (
                self.configuration_contract is not None
                and not self.configuration_contract.accepts(configuration.contract)
            ):
                raise WritableResolutionError(
                    "WritableRegion does not accept this carrier contract"
                )
            if (
                type(configuration) is loci.IntensionalConfiguration
                or _requires_intensional_resolution(self.descriptor)
            ):
                if self.fresh_namespaces or self.effect_profile.fresh:
                    raise WritableResolutionError(
                        "non-enumerated fresh capabilities are not implemented"
                    )
                reconstruction = IntensionalReconstructionEvidence(
                    snapshot_identity,
                    self.descriptor,
                    self.target_contract,
                )
                return IntensionalWritableCapabilities(
                    snapshot_identity,
                    self.descriptor,
                    self.effect_profile,
                    self.target_contract,
                    reconstruction,
                )
            assert type(configuration) is loci.FiniteConfiguration
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

        if (
            self.effect_profile.fresh
            and not fresh
            and not _contains_fresh_template(self.descriptor)
        ):
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

    def _resolve_composition(
        self,
        configuration: C,
    ) -> ResolvedWritableCapabilities:
        """Resolve each part under its own declarations, then compose targets."""

        if type(configuration) not in (
            loci.FiniteConfiguration,
            loci.IntensionalConfiguration,
        ):
            raise WritableResolutionError(
                "writable composition needs a recognized configuration"
            )
        resolved_parts = tuple(part.resolve(configuration) for part in self.parts)
        snapshot_identity = loci.configuration_identity(configuration)
        if any(
            resolved.snapshot_identity != snapshot_identity
            for resolved in resolved_parts
        ):
            raise WritableResolutionError(
                "writable parts resolved against different snapshots"
            )
        if any(
            type(resolved) is IntensionalWritableCapabilities
            for resolved in resolved_parts
        ):
            if self.fresh_namespaces or self.effect_profile.fresh:
                raise WritableResolutionError(
                    "non-enumerated fresh capabilities are not implemented"
                )
            reconstruction = IntensionalReconstructionEvidence(
                snapshot_identity,
                self.descriptor,
                self.target_contract,
            )
            return IntensionalWritableCapabilities(
                snapshot_identity,
                self.descriptor,
                self.effect_profile,
                self.target_contract,
                reconstruction,
            )
        assert all(type(resolved) is WritableCapabilities for resolved in resolved_parts)

        existing_by_target: dict[loci.Locus, ExistingCapability] = {}
        existing_order: list[loci.Locus] = []
        fresh_by_target: dict[loci.FreshReference, FreshCapability] = {}
        fresh_order: list[loci.FreshReference] = []
        for resolved in resolved_parts:
            for capability in resolved.existing:
                prior = existing_by_target.get(capability.target)
                if prior is None:
                    existing_by_target[capability.target] = capability
                    existing_order.append(capability.target)
                    continue
                if prior.contract != capability.contract:
                    raise WritableResolutionError(
                        "overlapping writable parts attach incompatible target "
                        "contracts"
                    )
                effects = tuple(
                    effect
                    for effect in Effect
                    if effect in prior.effects or effect in capability.effects
                )
                existing_by_target[capability.target] = ExistingCapability(
                    capability.target,
                    capability.contract,
                    effects,
                )
            for capability in resolved.fresh:
                prior = fresh_by_target.get(capability.target)
                if prior is None:
                    fresh_by_target[capability.target] = capability
                    fresh_order.append(capability.target)
                    continue
                if (
                    prior.contract != capability.contract
                    or prior.namespace != capability.namespace
                ):
                    raise WritableResolutionError(
                        "overlapping fresh parts attach incompatible declarations"
                    )

        if self.descriptor.kind is loci.RegionKind.UNION:
            existing_order.sort(key=loci.canonical_order_key)
            fresh_order.sort(key=loci.canonical_order_key)
        existing = tuple(existing_by_target[target] for target in existing_order)
        fresh = tuple(fresh_by_target[target] for target in fresh_order)
        lenses = tuple(
            ReconstructionLens(capability.target, capability.contract.frame)
            for capability in (*existing, *fresh)
        )
        return WritableCapabilities(
            snapshot_identity,
            existing,
            fresh,
            ReconstructionEvidence(snapshot_identity, lenses),
        )


def _resolve_targets(
    region: loci.Region,
    configuration: loci.FiniteConfiguration[object],
) -> tuple[tuple[loci.Locus, ...], tuple[loci.FreshReference, ...]]:
    """Resolve existing and local-fresh identities without binding births."""

    try:
        existing = tuple(
            target
            for target in loci.resolve_region(region, configuration)
            if configuration.contains(target)
        )
        fresh_targets = loci.resolve_fresh_references(region, configuration)
        return existing, fresh_targets
    except ValueError as error:
        raise WritableResolutionError(str(error)) from error


def _contains_fresh_template(region: loci.Region) -> bool:
    return bool(region.templates) or any(
        _contains_fresh_template(part) for part in region.parts
    )


def _requires_intensional_resolution(region: loci.Region) -> bool:
    return region.kind in (
        loci.RegionKind.CONTINUOUS,
        loci.RegionKind.DIFFERENTIAL,
        loci.RegionKind.INTENSIONAL,
    ) or any(
        _requires_intensional_resolution(part)
        for part in region.parts
    )


def _combined_effect_profile(
    parts: tuple[WritableRegion[object, object], ...],
) -> EffectProfile:
    return EffectProfile(
        tuple(
            effect
            for effect in Effect
            if any(effect in part.effect_profile.existing for part in parts)
        ),
        tuple(
            effect
            for effect in Effect
            if any(effect in part.effect_profile.fresh for part in parts)
        ),
    )


def _common_configuration_contract(
    parts: tuple[WritableRegion[object, object], ...],
) -> loci.CarrierContract | None:
    first = parts[0].configuration_contract
    return first if all(
        part.configuration_contract == first for part in parts
    ) else None


def _common_value_profile(
    parts: tuple[WritableRegion[object, object], ...],
) -> alphabets.ValueProfile | None:
    first = parts[0].value_profile
    return first if all(part.value_profile == first for part in parts) else None


def _part_fresh_namespaces(
    parts: tuple[WritableRegion[object, object], ...],
) -> tuple[FreshNamespace, ...]:
    namespaces: list[FreshNamespace] = []
    for part in parts:
        for namespace in part.fresh_namespaces:
            if namespace not in namespaces:
                namespaces.append(namespace)
    return tuple(
        sorted(
            namespaces,
            key=lambda namespace: (
                namespace.namespace,
                ""
                if namespace.parent is None
                else loci.canonical_identity(namespace.parent),
            ),
        )
    )


def _aggregate_target_contract(
    parts: tuple[WritableRegion[object, object], ...],
    value_profile: alphabets.ValueProfile | None,
) -> TargetContract:
    first = parts[0].target_contract
    if all(part.target_contract == first for part in parts):
        return first
    frames = {part.target_contract.frame for part in parts}
    frame = next(iter(frames)) if len(frames) == 1 else WriteFrame.SUCCESSOR
    return TargetContract(None, value_profile, frame)


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


def dynamic_fresh(
    region: loci.Region,
    *,
    namespace: FreshNamespace,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: alphabets.ValueProfile | None = None,
) -> WritableRegion[C, WritableCapabilities]:
    """Authorize fresh references derived from each current configuration."""

    if region.kind not in (
        loci.RegionKind.FRESH_CHILDREN,
        loci.RegionKind.FRESH_EDGES,
    ) or not region.templates:
        raise WritableResolutionError(
            "dynamic fresh frontier needs a fresh-template region"
        )
    if any(
        template.namespace != namespace.namespace
        for template in region.templates
    ):
        raise WritableResolutionError(
            "dynamic fresh templates lie outside the declared namespace"
        )
    return fresh(
        region,
        namespace=namespace,
        configuration_contract=configuration_contract,
        value_profile=value_profile,
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
    """Union envelopes while retaining every part's local declarations."""

    if type(parts) is not tuple or any(type(part) is not WritableRegion for part in parts):
        raise TypeError("union parts must be an immutable tuple of WritableRegions")
    if not parts:
        raise WritableResolutionError("union needs at least one region")
    if any(
        part.exactness_profile is not parts[0].exactness_profile
        for part in parts[1:]
    ):
        raise WritableResolutionError(
            "union parts have incompatible exactness declarations"
        )
    ordered = tuple(
        sorted(
            parts,
            key=loci.canonical_identity,
        )
    )
    profile = _combined_effect_profile(ordered)  # type: ignore[arg-type]
    namespaces = _part_fresh_namespaces(ordered)  # type: ignore[arg-type]
    namespace = namespaces[0] if len(namespaces) == 1 else None
    value_profile = _common_value_profile(ordered)  # type: ignore[arg-type]
    descriptors: list[loci.Region] = []
    descriptor_identities: set[str] = set()
    for part in ordered:
        identity = loci.canonical_identity(part.descriptor)
        if identity in descriptor_identities:
            continue
        descriptor_identities.add(identity)
        descriptors.append(part.descriptor)
    return WritableRegion(
        descriptor=loci.union(tuple(descriptors)),
        configuration_contract=_common_configuration_contract(ordered),  # type: ignore[arg-type]
        value_profile=value_profile,
        effect_profile=profile,
        target_contract=_aggregate_target_contract(  # type: ignore[arg-type]
            ordered,
            value_profile,
        ),
        fresh_namespace=namespace,
        exactness_profile=ordered[0].exactness_profile,
        parts=ordered,
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
    regions = tuple(region for _, region in fields)
    if any(
        region.exactness_profile is not regions[0].exactness_profile
        for region in regions[1:]
    ):
        raise WritableResolutionError(
            "product fields have incompatible exactness declarations"
        )
    profile = _combined_effect_profile(regions)  # type: ignore[arg-type]
    namespaces = _part_fresh_namespaces(regions)  # type: ignore[arg-type]
    namespace = namespaces[0] if len(namespaces) == 1 else None
    value_profile = _common_value_profile(regions)  # type: ignore[arg-type]
    return WritableRegion(
        descriptor=loci.region_product(
            tuple((key, region.descriptor) for key, region in fields)
        ),
        configuration_contract=_common_configuration_contract(regions),  # type: ignore[arg-type]
        value_profile=value_profile,
        effect_profile=profile,
        target_contract=_aggregate_target_contract(  # type: ignore[arg-type]
            regions,
            value_profile,
        ),
        fresh_namespace=namespace,
        exactness_profile=regions[0].exactness_profile,
        parts=regions,
    )
