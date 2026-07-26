"""Closed identity-preserving readable views.

A :class:`ReadableRegion` resolves independently from the same immutable
snapshot as a program's writable region.  The resolved view preserves target
identity, ordering, grouping, and boundary evidence.  It grants no write
authority and carries no update or scheduling policy.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Generic, TypeVar

from . import alphabets, loci
from .seeds import ExactnessProfile


C = TypeVar("C")
R = TypeVar("R")
V = TypeVar("V")


class ReadableResolutionError(ValueError):
    """A ReadableRegion cannot be resolved against the supplied snapshot."""


def _closed_observed_value(value: object) -> bool:
    """Recognize the exact closed semantic-value variants."""

    return type(value) in (bool, int, Fraction, str) or type(value) in (
        alphabets.RepresentedNumber,
        alphabets.ValueNode,
    )


class ReadArity(Enum):
    ONE = "one"
    FIXED = "fixed"
    VARIABLE = "variable"
    INTENSIONAL = "intensional"


@dataclass(frozen=True)
class ReadField:
    """One ordered field in a resolved result shape."""

    key: str
    arity: ReadArity
    size: int | None = None

    def __post_init__(self) -> None:
        if type(self.key) is not str or not self.key:
            raise ReadableResolutionError("read-field key cannot be empty")
        if type(self.arity) is not ReadArity:
            raise TypeError("read-field arity is not recognized")
        if self.size is not None and (
            type(self.size) is not int or self.size <= 0
        ):
            raise ReadableResolutionError(
                "read-field size must be a positive integer"
            )
        if self.arity is ReadArity.ONE and self.size not in (None, 1):
            raise ReadableResolutionError("ONE fields have size one")
        if self.arity is ReadArity.FIXED and (
            self.size is None
        ):
            raise ReadableResolutionError("FIXED fields need a positive size")
        if self.arity in (ReadArity.VARIABLE, ReadArity.INTENSIONAL) and (
            self.size is not None
        ):
            raise ReadableResolutionError(
                "variable/intensional fields cannot declare a fixed size"
            )


@dataclass(frozen=True)
class ResultShape:
    """Closed ordered shape supplied to Rule denotation."""

    fields: tuple[ReadField, ...]

    def __post_init__(self) -> None:
        if type(self.fields) is not tuple or any(
            type(field) is not ReadField for field in self.fields
        ):
            raise TypeError("result-shape fields must be an immutable tuple")
        if not self.fields:
            raise ReadableResolutionError("result shape cannot be empty")
        keys = tuple(field.key for field in self.fields)
        if len(set(keys)) != len(keys):
            raise ReadableResolutionError("result-shape keys must be unique")


class JoinMode(Enum):
    """How resolved read groups align with writable targets."""

    NONE = "none"
    TARGET_IDENTITY = "target-identity"
    ANCHOR_IDENTITY = "anchor-identity"
    PRODUCT = "product"
    GLOBAL = "global"


@dataclass(frozen=True)
class JoinShape:
    """Closed declaration of the R-to-W index relation."""

    mode: JoinMode
    fields: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.mode) is not JoinMode:
            raise TypeError("join mode is not recognized")
        if type(self.fields) is not tuple or any(
            type(field) is not str or not field for field in self.fields
        ):
            raise TypeError("join fields must be nonempty strings in a tuple")
        if len(set(self.fields)) != len(self.fields):
            raise ReadableResolutionError("join fields must be unique")
        if self.mode in (JoinMode.TARGET_IDENTITY, JoinMode.ANCHOR_IDENTITY):
            if not self.fields:
                raise ReadableResolutionError("identity joins need a field")
        elif self.mode is JoinMode.NONE:
            if self.fields:
                raise ReadableResolutionError("NONE joins cannot carry fields")
        elif not self.fields:
            raise ReadableResolutionError(
                f"{self.mode.value} joins need at least one field"
            )


@dataclass(frozen=True)
class Present(Generic[V]):
    """A value stored at an existing resolved locus."""

    value: V

    def __post_init__(self) -> None:
        if not _closed_observed_value(self.value):
            raise TypeError("present observation contains an opaque value")


@dataclass(frozen=True)
class BoundaryDefault(Generic[V]):
    """A value obtained through configuration-owned boundary data."""

    value: V
    evidence: loci.SelectorExpr
    boundary: loci.Boundary[V]

    def __post_init__(self) -> None:
        if not _closed_observed_value(self.value):
            raise TypeError("boundary observation contains an opaque value")
        if type(self.evidence) is not loci.SelectorExpr:
            raise TypeError("boundary evidence is not recognized")
        if type(self.boundary) is not loci.Boundary:
            raise TypeError("boundary descriptor is not recognized")


@dataclass(frozen=True)
class Absent:
    """An explicitly absent observation."""

    evidence: loci.SelectorExpr

    def __post_init__(self) -> None:
        if type(self.evidence) is not loci.SelectorExpr:
            raise TypeError("absence evidence is not recognized")


ObservedState = Present[V] | BoundaryDefault[V] | Absent


@dataclass(frozen=True)
class Observation(Generic[V]):
    """One identity-preserving old-snapshot observation."""

    target: loci.Locus
    state: ObservedState[V]
    anchor: loci.Locus | None = None

    def __post_init__(self) -> None:
        if type(self.target) is not loci.Locus:
            raise TypeError("observation target must be a Locus")
        if type(self.state) not in (Present, BoundaryDefault, Absent):
            raise TypeError("observation state variant is not recognized")
        if self.anchor is not None and type(self.anchor) is not loci.Locus:
            raise TypeError("observation anchor must be a Locus or None")

    @property
    def value(self) -> V:
        """Return a present/defaulted value, rejecting explicit absence."""

        if isinstance(self.state, Absent):
            raise ReadableResolutionError("the observation is explicitly absent")
        return self.state.value


@dataclass(frozen=True)
class GroupKey:
    """Stable Rule-facing key for one anchor/channel read group."""

    anchor: loci.Locus | None
    channel: int

    def __post_init__(self) -> None:
        if self.anchor is not None and type(self.anchor) is not loci.Locus:
            raise TypeError("group-key anchor must be a Locus or None")
        if type(self.channel) is not int or self.channel < 0:
            raise ReadableResolutionError("group channel cannot be negative")


@dataclass(frozen=True)
class ObservationGroup:
    """An ordered semantic group within ``ReadableView.observations``."""

    key: GroupKey
    indices: tuple[int, ...]
    anchor: loci.Locus | None = None

    def __post_init__(self) -> None:
        if type(self.key) is not GroupKey:
            raise TypeError("observation-group key is not recognized")
        if type(self.indices) is not tuple or any(
            type(index) is not int for index in self.indices
        ):
            raise TypeError("observation indices must be an immutable integer tuple")
        if self.anchor is not None and type(self.anchor) is not loci.Locus:
            raise TypeError("group anchor must be a Locus or None")
        if not self.indices:
            raise ReadableResolutionError("observation groups cannot be empty")
        if any(index < 0 for index in self.indices):
            raise ReadableResolutionError("observation indices cannot be negative")
        if len(set(self.indices)) != len(self.indices):
            raise ReadableResolutionError("observation indices must be unique")
        if self.key.anchor != self.anchor:
            raise ReadableResolutionError("group key and group anchor disagree")


@dataclass(frozen=True)
class ReadableView(Generic[V]):
    """Resolved ordered read view bound to one snapshot identity."""

    snapshot_identity: loci.ConfigurationIdentity
    observations: tuple[Observation[V], ...]
    groups: tuple[ObservationGroup, ...]
    join_shape: JoinShape

    def __post_init__(self) -> None:
        if type(self.snapshot_identity) is not str or not self.snapshot_identity:
            raise ReadableResolutionError(
                "readable view needs a snapshot identity"
            )
        if type(self.observations) is not tuple or any(
            type(item) is not Observation for item in self.observations
        ):
            raise TypeError("view observations must be an immutable tuple")
        if type(self.groups) is not tuple or any(
            type(item) is not ObservationGroup for item in self.groups
        ):
            raise TypeError("view groups must be an immutable tuple")
        if type(self.join_shape) is not JoinShape:
            raise TypeError("view join shape is not recognized")
        covered: list[int] = []
        for group in self.groups:
            covered.extend(group.indices)
        if tuple(covered) != tuple(range(len(self.observations))):
            raise ReadableResolutionError(
                "observation groups must partition observations in order"
            )
        for group in self.groups:
            if group.anchor is None:
                continue
            for index in group.indices:
                observation_anchor = self.observations[index].anchor
                if observation_anchor != group.anchor:
                    raise ReadableResolutionError(
                        "group and observation anchors disagree"
                    )


class GroupingKind(Enum):
    SINGLE = "single"
    FIXED_CHUNKS = "fixed-chunks"
    PRODUCT = "product"


@dataclass(frozen=True)
class GroupingPlan:
    """Closed grouping instruction interpreted only by this module."""

    kind: GroupingKind
    key: str
    chunk_size: int | None = None

    def __post_init__(self) -> None:
        if type(self.kind) is not GroupingKind:
            raise TypeError("grouping kind is not recognized")
        if type(self.key) is not str or not self.key:
            raise ReadableResolutionError("grouping key cannot be empty")
        if self.chunk_size is not None and (
            type(self.chunk_size) is not int or self.chunk_size <= 0
        ):
            raise ReadableResolutionError(
                "grouping chunk size must be a positive integer"
            )
        if self.kind is GroupingKind.FIXED_CHUNKS:
            if (
                self.chunk_size is None
            ):
                raise ReadableResolutionError(
                    "fixed-chunk grouping needs a positive size"
                )
        elif self.chunk_size is not None:
            raise ReadableResolutionError(
                "only fixed-chunk grouping carries a chunk size"
            )


@dataclass(frozen=True)
class ReadableField(Generic[C, R]):
    key: str
    region: "ReadableRegion[C, R]"

    def __post_init__(self) -> None:
        if type(self.key) is not str or not self.key:
            raise ReadableResolutionError("readable product key cannot be empty")
        if type(self.region) is not ReadableRegion:
            raise TypeError("readable product field needs a ReadableRegion")


@dataclass(frozen=True)
class ReadableRegion(Generic[C, R]):
    """Closed resolver for one complete old-snapshot read view."""

    descriptor: loci.Region
    configuration_contract: loci.CarrierContract | None
    value_profile: alphabets.ValueProfile | None
    result_shape: ResultShape
    join_shape: JoinShape
    grouping: GroupingPlan
    parts: tuple[ReadableField[C, R], ...] = ()
    exactness_profile: ExactnessProfile = ExactnessProfile.EXACT

    def __post_init__(self) -> None:
        if type(self.descriptor) is not loci.Region:
            raise TypeError("readable descriptor is not recognized")
        if self.configuration_contract is not None and type(
            self.configuration_contract
        ) is not loci.CarrierContract:
            raise TypeError("readable configuration contract is not recognized")
        if self.value_profile is not None and type(
            self.value_profile
        ) is not alphabets.ValueProfile:
            raise TypeError("value_profile must be alphabets.ValueProfile")
        if type(self.result_shape) is not ResultShape:
            raise TypeError("readable result shape is not recognized")
        if type(self.join_shape) is not JoinShape:
            raise TypeError("readable join shape is not recognized")
        if type(self.grouping) is not GroupingPlan:
            raise TypeError("readable grouping plan is not recognized")
        if type(self.parts) is not tuple or any(
            type(part) is not ReadableField for part in self.parts
        ):
            raise TypeError("readable parts must be an immutable tuple")
        if type(self.exactness_profile) is not ExactnessProfile:
            raise TypeError("readable exactness profile is not recognized")
        is_product = self.grouping.kind is GroupingKind.PRODUCT
        if is_product != bool(self.parts):
            raise ReadableResolutionError(
                "product grouping and readable parts must appear together"
            )

    @property
    def required_read_shape(self) -> ResultShape:
        return self.result_shape

    @property
    def required_join_shape(self) -> JoinShape:
        return self.join_shape

    @property
    def compatibility_read_shape(self) -> tuple[str, ...]:
        """Normalized spelling compared directly with ``RuleContract``."""

        return tuple(field.key for field in self.result_shape.fields)

    @property
    def compatibility_join_shape(self) -> tuple[str, ...]:
        """Normalized spelling compared directly with ``RuleContract``."""

        return self.join_shape.fields

    @property
    def compatibility_exactness_profile(self) -> str:
        return self.exactness_profile.value

    def resolve(self, configuration: C) -> ReadableView[V]:
        """Resolve independently against one immutable configuration."""

        if self.parts:
            return self._resolve_product(configuration)

        try:
            if type(configuration) is not loci.FiniteConfiguration:
                raise ReadableResolutionError(
                    "finite ReadableRegion resolution needs FiniteConfiguration"
                )
            if (
                self.configuration_contract is not None
                and not self.configuration_contract.accepts(configuration.contract)
            ):
                raise ReadableResolutionError(
                    "ReadableRegion does not accept this carrier contract"
                )
            snapshot_identity = loci.configuration_identity(configuration)
            targets = loci.resolve_region(self.descriptor, configuration)
            if self.descriptor.kind is loci.RegionKind.RELATIVE:
                anchors = loci.resolve_relative_anchors(
                    self.descriptor, configuration
                )
                chunk_size = len(self.descriptor.offsets)
            else:
                anchors = ()
                chunk_size = 0
        except (TypeError, ValueError) as error:
            raise ReadableResolutionError(str(error)) from error

        observations: list[Observation[V]] = []
        for index, target in enumerate(targets):
            anchor = anchors[index // chunk_size] if anchors else None
            try:
                value = loci.read_locus(configuration, target)
            except loci.LocusAbsentError as error:
                evidence = loci.SelectorExpr(
                    loci.SelectorPrimitive.RELATIVE,
                    arguments=(target,),
                )
                observations.append(Observation(target, Absent(evidence), anchor))
                continue
            if configuration.contains(target):
                state: ObservedState[V] = Present(value)
            else:
                evidence = loci.SelectorExpr(
                    loci.SelectorPrimitive.RELATIVE,
                    arguments=(target,),
                )
                state = BoundaryDefault(
                    value,
                    evidence,
                    configuration.carrier.boundary,
                )
            observations.append(Observation(target, state, anchor))

        groups = _groups_for(self.grouping, tuple(observations))
        view = ReadableView(
            snapshot_identity,
            tuple(observations),
            groups,
            self.join_shape,
        )
        _validate_view_shape(view, self.result_shape)
        return view

    def _resolve_product(self, configuration: C) -> ReadableView[V]:
        views = tuple(field.region.resolve(configuration) for field in self.parts)
        snapshot_ids = tuple(view.snapshot_identity for view in views)
        if len(set(snapshot_ids)) != 1:
            raise ReadableResolutionError(
                "product fields resolved against different snapshots"
            )

        observations: list[Observation[V]] = []
        groups: list[ObservationGroup] = []
        next_channel: dict[loci.Locus | None, int] = {}
        for field, view in zip(self.parts, views):
            start = len(observations)
            observations.extend(view.observations)
            for group in view.groups:
                indices = tuple(start + index for index in group.indices)
                channel = next_channel.get(group.anchor, 0)
                next_channel[group.anchor] = channel + 1
                groups.append(
                    ObservationGroup(
                        GroupKey(group.anchor, channel),
                        indices,
                        group.anchor,
                    )
                )
        view = ReadableView(
            snapshot_ids[0],
            tuple(observations),
            tuple(groups),
            self.join_shape,
        )
        _validate_view_shape(view, self.result_shape)
        return view


def _groups_for(
    grouping: GroupingPlan,
    observations: tuple[Observation[V], ...],
) -> tuple[ObservationGroup, ...]:
    if not observations:
        raise ReadableResolutionError("a finite resolved read view cannot be empty")
    if grouping.kind is GroupingKind.SINGLE:
        anchor = observations[0].anchor
        return (
            ObservationGroup(
                GroupKey(anchor, 0),
                tuple(range(len(observations))),
                anchor,
            ),
        )
    if grouping.kind is GroupingKind.FIXED_CHUNKS:
        assert grouping.chunk_size is not None
        if len(observations) % grouping.chunk_size:
            raise ReadableResolutionError(
                "resolved view does not divide into declared fixed groups"
            )
        groups: list[ObservationGroup] = []
        next_channel: dict[loci.Locus | None, int] = {}
        for start in range(0, len(observations), grouping.chunk_size):
            indices = tuple(range(start, start + grouping.chunk_size))
            anchor = observations[start].anchor
            channel = next_channel.get(anchor, 0)
            next_channel[anchor] = channel + 1
            groups.append(
                ObservationGroup(
                    GroupKey(anchor, channel),
                    indices,
                    anchor,
                )
            )
        return tuple(groups)
    raise ReadableResolutionError("PRODUCT grouping resolves through its fields")


def _validate_view_shape(view: ReadableView[V], shape: ResultShape) -> None:
    """Prove every materialized anchor has exactly the declared field arities."""

    grouped: dict[loci.Locus | None, list[ObservationGroup]] = {}
    for group in view.groups:
        grouped.setdefault(group.anchor, []).append(group)
    for groups in grouped.values():
        channels = tuple(group.key.channel for group in groups)
        if channels != tuple(range(len(shape.fields))):
            raise ReadableResolutionError(
                "resolved groups do not match the declared result fields"
            )
        for field, group in zip(shape.fields, groups):
            expected = 1 if field.arity is ReadArity.ONE else field.size
            if expected is not None and len(group.indices) != expected:
                raise ReadableResolutionError(
                    f"resolved group {field.key!r} violates its declared arity"
                )


def literal(
    targets: tuple[loci.Locus, ...],
    *,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: alphabets.ValueProfile | None = None,
    key: str = "literal",
) -> ReadableRegion[C, ReadableView[V]]:
    """Read an explicit ordered set of existing identities."""

    if type(targets) is not tuple or any(type(target) is not loci.Locus for target in targets):
        raise TypeError("literal targets must be an immutable tuple of Loci")
    if not targets:
        raise ReadableResolutionError("literal targets cannot be empty")
    return ReadableRegion(
        loci.literal(targets),
        configuration_contract,
        value_profile,
        ResultShape((ReadField(key, ReadArity.FIXED, len(targets)),)),
        JoinShape(JoinMode.NONE, ()),
        GroupingPlan(GroupingKind.SINGLE, key),
    )


def global_view(
    *,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: alphabets.ValueProfile | None = None,
    key: str = "global",
) -> ReadableRegion[C, ReadableView[V]]:
    """Read the complete old configuration as one ordered group."""

    return ReadableRegion(
        loci.all_support(),
        configuration_contract,
        value_profile,
        ResultShape((ReadField(key, ReadArity.VARIABLE),)),
        JoinShape(JoinMode.GLOBAL, (key,)),
        GroupingPlan(GroupingKind.SINGLE, key),
    )


def grid_relative(
    offsets: tuple[tuple[int, ...], ...],
    *,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: alphabets.ValueProfile | None = None,
    key: str = "relative",
) -> ReadableRegion[C, ReadableView[V]]:
    """Read one ordered relative-offset group for every carrier anchor."""

    if type(offsets) is not tuple or any(
        type(offset) is not tuple
        or any(type(coordinate) is not int for coordinate in offset)
        for offset in offsets
    ):
        raise TypeError("relative offsets must be immutable integer tuples")
    if not offsets:
        raise ReadableResolutionError("relative offsets cannot be empty")
    rank = len(offsets[0])
    if rank < 1 or any(len(offset) != rank for offset in offsets):
        raise ReadableResolutionError("relative offsets must have one common rank")
    if len(set(offsets)) != len(offsets):
        raise ReadableResolutionError("relative offsets must be unique")
    offset_loci = tuple(
        loci.Locus(loci.LocusKind.COORDINATE, "relative", tuple(offset))
        for offset in offsets
    )
    region = loci.relative(loci.all_support(), offset_loci)
    return ReadableRegion(
        region,
        configuration_contract,
        value_profile,
        ResultShape((ReadField(key, ReadArity.FIXED, len(offsets)),)),
        JoinShape(JoinMode.ANCHOR_IDENTITY, ("target", "channel")),
        GroupingPlan(GroupingKind.FIXED_CHUNKS, key, len(offsets)),
    )


def intensional(
    binder: str,
    relation: loci.SelectorExpr,
    *,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: alphabets.ValueProfile | None = None,
    key: str = "intensional",
) -> ReadableRegion[C, ReadableView[V]]:
    """Describe a closed non-enumerated read view."""

    if type(binder) is not str or not binder:
        raise ReadableResolutionError("intensional binder cannot be empty")
    if type(relation) is not loci.SelectorExpr:
        raise TypeError("intensional relation is not recognized")
    return ReadableRegion(
        loci.intensional(binder, relation),
        configuration_contract,
        value_profile,
        ResultShape((ReadField(key, ReadArity.INTENSIONAL),)),
        JoinShape(JoinMode.GLOBAL, (key,)),
        GroupingPlan(GroupingKind.SINGLE, key),
        exactness_profile=ExactnessProfile.SYMBOLIC,
    )


def product(
    fields: tuple[tuple[str, ReadableRegion[C, R]], ...],
) -> ReadableRegion[C, ReadableView[V]]:
    """Compose named read fields while preserving every group boundary."""

    if type(fields) is not tuple or any(
        type(field) is not tuple
        or len(field) != 2
        or type(field[0]) is not str
        or type(field[1]) is not ReadableRegion
        for field in fields
    ):
        raise TypeError(
            "product fields must be immutable (name, ReadableRegion) pairs"
        )
    if not fields:
        raise ReadableResolutionError("product needs at least one field")
    keys = tuple(key for key, _ in fields)
    if any(not key for key in keys) or len(set(keys)) != len(keys):
        raise ReadableResolutionError("product keys must be nonempty and unique")
    first = fields[0][1]
    for _, region in fields[1:]:
        if (
            region.configuration_contract != first.configuration_contract
            or region.value_profile != first.value_profile
            or region.exactness_profile is not first.exactness_profile
        ):
            raise ReadableResolutionError(
                "product fields have incompatible read declarations"
            )
    parts = tuple(ReadableField(key, region) for key, region in fields)
    shape_fields = tuple(
        ReadField(f"{key}.{field.key}", field.arity, field.size)
        for key, region in fields
        for field in region.result_shape.fields
    )
    return ReadableRegion(
        loci.region_product(
            tuple((key, region.descriptor) for key, region in fields)
        ),
        first.configuration_contract,
        first.value_profile,
        ResultShape(shape_fields),
        JoinShape(JoinMode.PRODUCT, ("target", "channel")),
        GroupingPlan(GroupingKind.PRODUCT, "product"),
        parts,
        first.exactness_profile,
    )


def _with_compatibility_shape(
    region: ReadableRegion[C, R],
    read_fields: tuple[tuple[str, int], ...],
    join_fields: tuple[str, ...] = ("target", "channel"),
    *,
    split_single_group: bool = False,
) -> ReadableRegion[C, R]:
    """Retain mechanics while assigning the exact Rule-facing shape."""

    if type(region) is not ReadableRegion:
        raise TypeError("compatibility shape needs a ReadableRegion")
    if type(read_fields) is not tuple or any(
        type(field) is not tuple
        or len(field) != 2
        or type(field[0]) is not str
        or not field[0]
        or type(field[1]) is not int
        or field[1] <= 0
        for field in read_fields
    ):
        raise TypeError("compatibility fields need closed positive arities")
    grouping = (
        GroupingPlan(GroupingKind.FIXED_CHUNKS, "compatibility-fields", 1)
        if split_single_group
        else region.grouping
    )
    return ReadableRegion(
        region.descriptor,
        region.configuration_contract,
        region.value_profile,
        ResultShape(
            tuple(
                ReadField(
                    key,
                    ReadArity.ONE if size == 1 else ReadArity.FIXED,
                    size,
                )
                for key, size in read_fields
            )
        ),
        JoinShape(region.join_shape.mode, join_fields),
        grouping,
        region.parts,
        region.exactness_profile,
    )


def self_at(
    history_offset: int = 0,
    *,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: alphabets.ValueProfile | None = None,
    key: str = "self",
) -> ReadableRegion[C, ReadableView[V]]:
    """Read the same identity at one current/history offset."""

    if type(history_offset) is not int:
        raise TypeError("history_offset must be an integer")
    return grid_relative(
        ((history_offset,),),
        configuration_contract=configuration_contract,
        value_profile=value_profile,
        key=key,
    )


def history(
    offsets: tuple[int, ...],
    *,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: alphabets.ValueProfile | None = None,
    key: str = "history",
) -> ReadableRegion[C, ReadableView[V]]:
    """Read one ordered temporal/history group per anchor."""

    if type(offsets) is not tuple or any(type(offset) is not int for offset in offsets):
        raise TypeError("history offsets must be an immutable integer tuple")
    return grid_relative(
        tuple((offset,) for offset in offsets),
        configuration_contract=configuration_contract,
        value_profile=value_profile,
        key=key,
    )


def eca(
    radius: int = 1,
    *,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: alphabets.ValueProfile | None = alphabets.ValueProfile.BOOLEAN,
) -> ReadableRegion[C, ReadableView[V]]:
    """Read the ordered one-dimensional ``left .. self .. right`` stencil."""

    if type(radius) is not int or radius <= 0:
        raise ReadableResolutionError("ECA radius must be positive")
    carrier = (
        loci.CarrierContract(
            loci.CarrierKind.GRID,
            rank=1,
            axes=("x",),
        )
        if configuration_contract is None
        else configuration_contract
    )
    return grid_relative(
        tuple((offset,) for offset in range(-radius, radius + 1)),
        configuration_contract=carrier,
        value_profile=value_profile,
        key="eca",
    )


def ar2_0d(
    *,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: alphabets.ValueProfile | None = None,
) -> ReadableRegion[C, ReadableView[V]]:
    """Read current and previous scalar values."""

    previous = loci.named("previous", scope="record")
    current = loci.named("current", scope="record")
    carrier = (
        loci.CarrierContract(loci.CarrierKind.RECORD, rank=0, shape=())
        if configuration_contract is None
        else configuration_contract
    )
    return literal(
        (previous, current),
        configuration_contract=carrier,
        value_profile=value_profile,
        key="ar2",
    )


def dyadlags_0d(
    *,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: alphabets.ValueProfile | None = alphabets.ValueProfile.BOOLEAN,
) -> ReadableRegion[C, ReadableView[V]]:
    """Read current and two previous binary values."""

    carrier = (
        loci.CarrierContract(
            loci.CarrierKind.HISTORY,
            rank=1,
            shape=(3,),
            axes=("history",),
        )
        if configuration_contract is None
        else configuration_contract
    )
    region = history(
        (-2, -1, 0),
        configuration_contract=carrier,
        value_profile=value_profile,
        key="dyadlags",
    )
    return _with_compatibility_shape(
        region,
        (("older", 1), ("previous", 1), ("current", 1)),
        split_single_group=True,
    )


def lagcounts_0d(
    band_size: int = 3,
    band_count: int = 3,
    *,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: alphabets.ValueProfile | None = alphabets.ValueProfile.BOOLEAN,
) -> ReadableRegion[C, ReadableView[V]]:
    """Read current self followed by explicit lag-count bands."""

    if type(band_size) is not int or band_size <= 0:
        raise ReadableResolutionError("band_size must be positive")
    if type(band_count) is not int or band_count != 3:
        raise ReadableResolutionError(
            "the native lagcounts view requires exactly three bands"
        )
    carrier = (
        loci.CarrierContract(
            loci.CarrierKind.HISTORY,
            rank=1,
            shape=(1 + band_size * band_count,),
            axes=("history",),
        )
        if configuration_contract is None
        else configuration_contract
    )
    fields: list[tuple[str, ReadableRegion[C, ReadableView[V]]]] = [
        (
            "self",
            history(
                (0,),
                configuration_contract=carrier,
                value_profile=value_profile,
                key="self",
            ),
        )
    ]
    for band in range(band_count):
        start = 1 + band * band_size
        fields.append(
            (
                f"band-{band}",
                history(
                    tuple(-offset for offset in range(start, start + band_size)),
                    configuration_contract=carrier,
                    value_profile=value_profile,
                    key=f"band-{band}",
                ),
            )
        )
    return _with_compatibility_shape(
        product(tuple(fields)),
        (
            ("history", 1),
            ("recent", band_size),
            ("middle", band_size),
            ("oldest", band_size),
        ),
    )


def dyadrads_1d(
    *,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: alphabets.ValueProfile | None = alphabets.ValueProfile.BOOLEAN,
) -> ReadableRegion[C, ReadableView[V]]:
    """Read self, radius-one, and radius-two one-dimensional groups."""

    carrier = (
        loci.CarrierContract(
            loci.CarrierKind.GRID,
            rank=1,
            axes=("x",),
        )
        if configuration_contract is None
        else configuration_contract
    )
    region = product(
        (
            (
                "self",
                grid_relative(
                    ((0,),),
                    configuration_contract=carrier,
                    value_profile=value_profile,
                    key="self",
                ),
            ),
            (
                "radius-1",
                grid_relative(
                    ((-1,), (1,)),
                    configuration_contract=carrier,
                    value_profile=value_profile,
                    key="radius-1",
                ),
            ),
            (
                "radius-2",
                grid_relative(
                    ((-2,), (2,)),
                    configuration_contract=carrier,
                    value_profile=value_profile,
                    key="radius-2",
                ),
            ),
        )
    )
    return _with_compatibility_shape(
        region,
        (("self", 1), ("primary", 2), ("secondary", 2)),
    )


def dyadaxes_2d(
    *,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: alphabets.ValueProfile | None = alphabets.ValueProfile.BOOLEAN,
) -> ReadableRegion[C, ReadableView[V]]:
    """Read self, four cardinal neighbors, and four diagonals."""

    carrier = (
        loci.CarrierContract(
            loci.CarrierKind.GRID,
            rank=2,
            axes=("x", "y"),
        )
        if configuration_contract is None
        else configuration_contract
    )
    region = product(
        (
            (
                "self",
                grid_relative(
                    ((0, 0),),
                    configuration_contract=carrier,
                    value_profile=value_profile,
                    key="self",
                ),
            ),
            (
                "faces",
                grid_relative(
                    ((-1, 0), (0, -1), (0, 1), (1, 0)),
                    configuration_contract=carrier,
                    value_profile=value_profile,
                    key="faces",
                ),
            ),
            (
                "diagonals",
                grid_relative(
                    ((-1, -1), (-1, 1), (1, -1), (1, 1)),
                    configuration_contract=carrier,
                    value_profile=value_profile,
                    key="diagonals",
                ),
            ),
        )
    )
    return _with_compatibility_shape(
        region,
        (("self", 1), ("primary", 4), ("secondary", 4)),
    )


def dyadaxes_3d(
    *,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: alphabets.ValueProfile | None = alphabets.ValueProfile.BOOLEAN,
) -> ReadableRegion[C, ReadableView[V]]:
    """Read self, six face neighbors, and twenty edge/corner neighbors."""

    carrier = (
        loci.CarrierContract(
            loci.CarrierKind.GRID,
            rank=3,
            axes=("x", "y", "z"),
        )
        if configuration_contract is None
        else configuration_contract
    )
    faces = tuple(
        offset
        for offset in (
            (-1, 0, 0),
            (1, 0, 0),
            (0, -1, 0),
            (0, 1, 0),
            (0, 0, -1),
            (0, 0, 1),
        )
    )
    outer = tuple(
        (x, y, z)
        for x in (-1, 0, 1)
        for y in (-1, 0, 1)
        for z in (-1, 0, 1)
        if (x, y, z) != (0, 0, 0) and (x, y, z) not in faces
    )
    region = product(
        (
            (
                "self",
                grid_relative(
                    ((0, 0, 0),),
                    configuration_contract=carrier,
                    value_profile=value_profile,
                    key="self",
                ),
            ),
            (
                "faces",
                grid_relative(
                    faces,
                    configuration_contract=carrier,
                    value_profile=value_profile,
                    key="faces",
                ),
            ),
            (
                "edges-corners",
                grid_relative(
                    outer,
                    configuration_contract=carrier,
                    value_profile=value_profile,
                    key="edges-corners",
                ),
            ),
        )
    )
    return _with_compatibility_shape(
        region,
        (("self", 1), ("primary", 6), ("secondary", 20)),
    )
