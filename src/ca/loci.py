"""Closed structural identities, carriers, configurations, and regions.

``loci`` supplies structure shared by Seeds, writable regions, and readable
regions without itself granting read or write authority.  Every public value
is immutable and versioned; selectors are data, never Python callbacks.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from itertools import product as cartesian_product
from typing import Generic, TypeAlias, TypeVar


V = TypeVar("V")
ClosedScalar: TypeAlias = bool | int | Fraction | str
ConfigurationIdentity: TypeAlias = str


class LociResolutionError(ValueError):
    """A closed structural region cannot resolve against a configuration."""


class LocusAbsentError(KeyError):
    """A requested locus is absent under the configuration's boundary law."""


class LocusKind(Enum):
    """Recognized structural identity forms."""

    COORDINATE = "coordinate"
    NAMED = "named"
    OCCURRENCE = "occurrence"
    PATH = "path"
    SPAN = "span"
    PORT = "port"
    INTERFACE = "interface"
    PRODUCT = "product"
    GRAPH_ELEMENT = "graph-element"
    FIELD_POINT = "field-point"
    CONTINUOUS = "continuous"
    INTENSIONAL = "intensional"
    FRESH = "fresh"


@dataclass(frozen=True)
class Locus:
    """One semantic identity; it carries no access capability."""

    kind: LocusKind
    scope: str
    path: tuple[ClosedScalar, ...]
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported locus version {self.version}")
        if not isinstance(self.kind, LocusKind):
            raise TypeError("locus kind is not recognized")
        if not isinstance(self.scope, str) or not self.scope:
            raise ValueError("locus scope cannot be empty")
        if any(not isinstance(part, (bool, int, Fraction, str)) for part in self.path):
            raise TypeError("locus path contains an unclosed value")


@dataclass(frozen=True)
class FreshReference:
    """A Rule-local fresh key, not yet a globally bound identity."""

    namespace: str
    local_key: ClosedScalar
    parent: Locus | None = None
    interface: tuple[Locus, ...] = ()
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported fresh-reference version {self.version}")
        if not isinstance(self.namespace, str) or not self.namespace:
            raise ValueError("fresh namespace cannot be empty")
        if not isinstance(self.local_key, (bool, int, Fraction, str)):
            raise TypeError("fresh-reference local key is not closed")
        if self.parent is not None and not isinstance(self.parent, Locus):
            raise TypeError("fresh-reference parent must be a Locus")
        if any(not isinstance(item, Locus) for item in self.interface):
            raise TypeError("fresh-reference interface must contain Loci")


def _locus_token(value: Locus | FreshReference) -> str:
    return canonical_identity(value)


def named(name: str, *, scope: str = "configuration") -> Locus:
    if not isinstance(name, str) or not name:
        raise ValueError("name must be a nonempty string")
    return Locus(LocusKind.NAMED, scope, (name,))


def coordinate(axis: str, value: int, *, scope: str = "offset") -> Locus:
    if axis not in ("t", "x", "y", "z"):
        raise ValueError("axis must be one of t, x, y, z")
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("coordinate value must be an integer")
    return Locus(LocusKind.COORDINATE, scope, (axis, value))


def cell(coordinates: tuple[int, ...], *, axes: tuple[str, ...] | None = None) -> Locus:
    if any(isinstance(value, bool) or not isinstance(value, int) for value in coordinates):
        raise TypeError("cell coordinates must be integers")
    if axes is None:
        axes = ("x", "y", "z")[: len(coordinates)]
    if len(axes) != len(coordinates):
        raise ValueError("axes and coordinates must have equal length")
    return Locus(
        LocusKind.COORDINATE,
        "grid:" + ",".join(axes),
        tuple(part for pair in zip(axes, coordinates) for part in pair),
    )


def occurrence(container: Locus | str, index: int) -> Locus:
    token = container if isinstance(container, str) else _locus_token(container)
    return Locus(LocusKind.OCCURRENCE, "occurrence", (token, int(index)))


def path(*segments: ClosedScalar, scope: str = "path") -> Locus:
    if not segments:
        raise ValueError("path requires at least one segment")
    return Locus(LocusKind.PATH, scope, tuple(segments))


def span(container: Locus | str, start: int, stop: int) -> Locus:
    if stop < start:
        raise ValueError("span stop must be >= start")
    token = container if isinstance(container, str) else _locus_token(container)
    return Locus(LocusKind.SPAN, "span", (token, int(start), int(stop)))


def port(owner: Locus | str, name: str) -> Locus:
    token = owner if isinstance(owner, str) else _locus_token(owner)
    return Locus(LocusKind.PORT, "port", (token, name))


def interface(left: Locus, right: Locus, *, name: str = "interface") -> Locus:
    return Locus(
        LocusKind.INTERFACE,
        name,
        tuple(sorted((_locus_token(left), _locus_token(right)))),
    )


def product_locus(name: str, parts: tuple[Locus, ...]) -> Locus:
    if not parts:
        raise ValueError("product locus requires at least one part")
    return Locus(
        LocusKind.PRODUCT,
        name,
        tuple(_locus_token(part) for part in parts),
    )


def graph_element(kind: str, identity: ClosedScalar) -> Locus:
    if kind not in ("node", "edge", "port"):
        raise ValueError("graph element kind must be node, edge, or port")
    return Locus(LocusKind.GRAPH_ELEMENT, "graph", (kind, identity))


def field_point(
    field: str,
    coordinates: tuple[Fraction | int, ...],
    *,
    component: str | None = None,
) -> Locus:
    path_parts: tuple[ClosedScalar, ...] = (
        field,
        *(Fraction(value) for value in coordinates),
    )
    if component is not None:
        path_parts = (*path_parts, component)
    return Locus(LocusKind.FIELD_POINT, "field", path_parts)


def continuous_region(name: str, bounds: tuple[Fraction, ...]) -> Locus:
    return Locus(
        LocusKind.CONTINUOUS,
        "continuous",
        (name, *(Fraction(bound) for bound in bounds)),
    )


def intensional_reference(binder: str, relation_id: str) -> Locus:
    return Locus(LocusKind.INTENSIONAL, "intensional", (binder, relation_id))


def fresh_reference(
    namespace: str,
    local_key: ClosedScalar,
    *,
    parent: Locus | None = None,
    interface_loci: tuple[Locus, ...] = (),
) -> FreshReference:
    return FreshReference(namespace, local_key, parent, interface_loci)


class SelectorPrimitive(Enum):
    """Closed operations admitted inside selector expressions."""

    LITERAL = "selector.literal"
    EQUAL = "selector.equal"
    TAGGED = "selector.tagged"
    RELATIVE = "selector.relative"
    METRIC = "selector.metric"
    PATH = "selector.path"
    INCIDENCE = "selector.incidence"
    REACHABLE = "selector.reachable"
    FIELD_RESTRICTION = "selector.field-restriction"
    DIFFERENTIAL_GERM = "selector.differential-germ"
    HISTORY = "selector.history"
    MEMBERSHIP = "selector.membership"
    AND = "selector.and"
    OR = "selector.or"
    NOT = "selector.not"


SelectorArgument: TypeAlias = ClosedScalar | Locus | FreshReference


@dataclass(frozen=True)
class SelectorExpr:
    """One closed selector AST node."""

    primitive: SelectorPrimitive
    arguments: tuple[SelectorArgument, ...] = ()
    children: tuple["SelectorExpr", ...] = ()
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported selector version {self.version}")
        if not isinstance(self.primitive, SelectorPrimitive):
            raise TypeError("selector primitive is not recognized")
        if any(
            not isinstance(
                argument,
                (bool, int, Fraction, str, Locus, FreshReference),
            )
            for argument in self.arguments
        ):
            raise TypeError("selector contains an opaque or executable argument")
        if any(not isinstance(child, SelectorExpr) for child in self.children):
            raise TypeError("selector children must be SelectorExpr values")


class RegionKind(Enum):
    """Raw structural regions shared by read and write components."""

    LITERAL = "literal"
    ALL_SUPPORT = "all-support"
    CURRENT_SUPPORT = "current-support"
    RELATIVE = "relative"
    PRODUCT = "product"
    UNION = "union"
    INTERSECTION = "intersection"
    DIFFERENCE = "difference"
    SPAN = "span"
    PATH = "path"
    MATCHED_INTERFACE = "matched-interface"
    DYNAMIC_ADDRESS = "dynamic-address"
    FRESH_CHILDREN = "fresh-children"
    FRESH_EDGES = "fresh-edges"
    CONTINUOUS = "continuous"
    DIFFERENTIAL = "differential"
    INTENSIONAL = "intensional"


@dataclass(frozen=True)
class Region:
    """A closed raw region.  It grants neither read nor write authority."""

    kind: RegionKind
    name: str | None = None
    loci: tuple[Locus, ...] = ()
    fresh: tuple[FreshReference, ...] = ()
    parts: tuple["Region", ...] = ()
    offsets: tuple[Locus, ...] = ()
    relation: SelectorExpr | None = None
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported region version {self.version}")
        if not isinstance(self.kind, RegionKind):
            raise TypeError("region kind is not recognized")
        if self.name is not None and not isinstance(self.name, str):
            raise TypeError("region name must be a string or None")
        if any(not isinstance(item, Locus) for item in self.loci):
            raise TypeError("region loci must contain Locus values")
        if any(not isinstance(item, FreshReference) for item in self.fresh):
            raise TypeError("region fresh targets must contain FreshReference values")
        if any(not isinstance(item, Region) for item in self.parts):
            raise TypeError("region parts must contain Region values")
        if any(not isinstance(item, Locus) for item in self.offsets):
            raise TypeError("region offsets must contain Locus values")
        if self.relation is not None and not isinstance(
            self.relation, SelectorExpr
        ):
            raise TypeError("region relation must be a SelectorExpr")
        if self.kind is RegionKind.LITERAL and not (self.loci or self.fresh):
            raise ValueError("literal region cannot be empty")
        if self.kind in (RegionKind.UNION, RegionKind.PRODUCT) and not self.parts:
            raise ValueError(f"{self.kind.value} region requires parts")
        if self.kind is RegionKind.INTENSIONAL and self.relation is None:
            raise ValueError("intensional region requires a relation")


def literal(
    loci_values: tuple[Locus, ...] = (),
    *,
    fresh: tuple[FreshReference, ...] = (),
    name: str | None = None,
) -> Region:
    return Region(RegionKind.LITERAL, name=name, loci=loci_values, fresh=fresh)


def all_support(carrier: str = "current-carrier") -> Region:
    return Region(RegionKind.ALL_SUPPORT, name=carrier)


def current_support(carrier: str = "current-carrier") -> Region:
    return Region(RegionKind.CURRENT_SUPPORT, name=carrier)


def relative(anchors: Region, offsets: tuple[Locus, ...]) -> Region:
    if not offsets:
        raise ValueError("relative region requires offsets")
    return Region(RegionKind.RELATIVE, parts=(anchors,), offsets=offsets)


def union(parts: tuple[Region, ...]) -> Region:
    return Region(RegionKind.UNION, parts=parts)


def region_product(parts: tuple[tuple[str, Region], ...]) -> Region:
    if not parts:
        raise ValueError("region product requires named parts")
    named_parts = tuple(
        Region(RegionKind.PRODUCT, name=name, parts=(part,))
        for name, part in parts
    )
    return Region(RegionKind.PRODUCT, parts=named_parts)


def fresh_children(
    parent: Locus,
    namespace: str,
    local_keys: tuple[ClosedScalar, ...],
) -> Region:
    return Region(
        RegionKind.FRESH_CHILDREN,
        name=namespace,
        fresh=tuple(
            FreshReference(namespace, local_key, parent)
            for local_key in local_keys
        ),
    )


def intensional(binder: str, relation: SelectorExpr) -> Region:
    return Region(RegionKind.INTENSIONAL, name=binder, relation=relation)


class BoundaryPolicy(Enum):
    NONE = "none"
    FIXED = "fixed"
    PERIODIC = "periodic"
    REFLECTIVE = "reflective"


class CarrierKind(Enum):
    RECORD = "record"
    HISTORY = "history"
    GRID = "grid"
    WORD = "word"
    TREE = "tree"
    GRAPH = "graph"
    FIELD = "field"
    PRODUCT = "product"
    INTENSIONAL = "intensional"


@dataclass(frozen=True)
class CarrierContract:
    """Closed structural contract shared independently by program components."""

    kind: CarrierKind
    rank: int | None = None
    shape: tuple[int, ...] | None = None
    axes: tuple[str, ...] = ()
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported carrier-contract version {self.version}")
        if not isinstance(self.kind, CarrierKind):
            raise TypeError("carrier kind is not recognized")
        if self.rank is not None and (
            isinstance(self.rank, bool)
            or not isinstance(self.rank, int)
            or self.rank < 0
        ):
            raise ValueError("carrier rank cannot be negative")
        if self.shape is not None:
            if any(
                isinstance(size, bool)
                or not isinstance(size, int)
                or size <= 0
                for size in self.shape
            ):
                raise ValueError("carrier shape extents must be positive")
            if self.rank is not None and len(self.shape) != self.rank:
                raise ValueError("carrier shape and rank disagree")
        if self.axes and self.rank is not None and len(self.axes) != self.rank:
            raise ValueError("carrier axes and rank disagree")
        if any(not isinstance(axis, str) or not axis for axis in self.axes):
            raise TypeError("carrier axes must be nonempty strings")
        if len(set(self.axes)) != len(self.axes):
            raise ValueError("carrier axes must be unique")

    def accepts(self, other: "CarrierContract") -> bool:
        return (
            self.kind is other.kind
            and (self.rank is None or self.rank == other.rank)
            and (self.shape is None or self.shape == other.shape)
            and (not self.axes or self.axes == other.axes)
        )


@dataclass(frozen=True)
class Boundary(Generic[V]):
    policy: BoundaryPolicy
    exterior: V | None = None
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported boundary version {self.version}")
        if not isinstance(self.policy, BoundaryPolicy):
            raise TypeError("boundary policy is not recognized")
        if self.policy is BoundaryPolicy.FIXED and self.exterior is None:
            raise ValueError("fixed boundary requires an exterior value")
        if self.policy is not BoundaryPolicy.FIXED and self.exterior is not None:
            raise ValueError("only fixed boundary carries an exterior value")


@dataclass(frozen=True)
class Carrier(Generic[V]):
    """Closed carrier/support/topology data for a finite configuration."""

    contract: CarrierContract
    boundary: Boundary[V]
    attributes: tuple[tuple[str, ClosedScalar], ...] = ()
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported carrier version {self.version}")
        if not isinstance(self.contract, CarrierContract):
            raise TypeError("carrier contract is not recognized")
        if not isinstance(self.boundary, Boundary):
            raise TypeError("carrier boundary is not recognized")
        if any(
            not isinstance(name, str)
            or not isinstance(value, (bool, int, Fraction, str))
            for name, value in self.attributes
        ):
            raise TypeError("carrier attributes are not closed")
        names = tuple(name for name, _ in self.attributes)
        if len(names) != len(set(names)):
            raise ValueError("carrier attributes must have unique names")


@dataclass(frozen=True)
class StructuralRelation:
    """Closed structural side data such as incidence or order."""

    tag: str
    arguments: tuple[ClosedScalar | Locus, ...] = ()
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported structural relation version {self.version}")
        if not isinstance(self.tag, str) or not self.tag:
            raise ValueError("structural relation tag cannot be empty")
        if any(
            not isinstance(argument, (bool, int, Fraction, str, Locus))
            for argument in self.arguments
        ):
            raise TypeError("structural relation contains an opaque argument")


@dataclass(frozen=True)
class FiniteConfiguration(Generic[V]):
    """One immutable finite structural configuration."""

    carrier: Carrier[V]
    entries: tuple[tuple[Locus, V], ...]
    structure: tuple[StructuralRelation, ...] = ()
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported configuration version {self.version}")
        if not isinstance(self.carrier, Carrier):
            raise TypeError("configuration carrier is not recognized")
        if any(
            not isinstance(target, Locus)
            for target, _ in self.entries
        ):
            raise TypeError("configuration targets must be Locus values")
        if any(not isinstance(item, StructuralRelation) for item in self.structure):
            raise TypeError("configuration structure must contain closed relations")
        targets = tuple(target for target, _ in self.entries)
        if len(targets) != len(set(targets)):
            raise ValueError("configuration entries must have unique loci")
        contract = self.carrier.contract
        if contract.kind is CarrierKind.HISTORY and contract.shape is not None:
            expected = tuple(
                occurrence("history", index)
                for index in range(contract.shape[0])
            )
            if set(targets) != set(expected):
                raise ValueError(
                    "finite history entries do not equal the declared carrier"
                )
        if contract.kind is CarrierKind.GRID and contract.shape is not None:
            expected = grid_loci(contract.shape, axes=contract.axes or None)
            if set(targets) != set(expected):
                raise ValueError(
                    "finite grid entries do not equal the declared carrier"
                )
        ordered = tuple(
            sorted(self.entries, key=lambda item: canonical_order_key(item[0]))
        )
        if ordered != self.entries:
            object.__setattr__(self, "entries", ordered)

    @property
    def contract(self) -> CarrierContract:
        return self.carrier.contract

    @property
    def identity(self) -> str:
        return canonical_identity(self)

    @property
    def canonical_identity(self) -> str:
        return self.identity

    def value_at(self, target: Locus) -> V:
        for locus_value, value in self.entries:
            if locus_value == target:
                return value
        raise KeyError(target)

    def contains(self, target: Locus) -> bool:
        return any(locus_value == target for locus_value, _ in self.entries)

    def with_entries(
        self,
        entries: tuple[tuple[Locus, V], ...],
        *,
        structure: tuple[StructuralRelation, ...] | None = None,
    ) -> "FiniteConfiguration[V]":
        return FiniteConfiguration(
            self.carrier,
            entries,
            self.structure if structure is None else structure,
        )


@dataclass(frozen=True)
class IntensionalConfiguration:
    """A complete closed presentation of a non-enumerated configuration."""

    contract: CarrierContract
    relation: SelectorExpr
    identity_evidence: str
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise ValueError(f"unsupported configuration version {self.version}")
        if not self.identity_evidence:
            raise ValueError("intensional configuration needs identity evidence")

    @property
    def identity(self) -> str:
        return canonical_identity(self)

    @property
    def canonical_identity(self) -> str:
        return self.identity


Configuration: TypeAlias = FiniteConfiguration[V] | IntensionalConfiguration


def record_configuration(
    fields: tuple[tuple[str, V], ...],
) -> FiniteConfiguration[V]:
    if not fields:
        raise ValueError("record configuration requires fields")
    entries = tuple((named(name, scope="record"), value) for name, value in fields)
    contract = CarrierContract(CarrierKind.RECORD, rank=0, shape=(), axes=())
    return FiniteConfiguration(
        Carrier(contract, Boundary(BoundaryPolicy.NONE)),
        entries,
    )


def history_configuration(values: tuple[V, ...]) -> FiniteConfiguration[V]:
    if not values:
        raise ValueError("history configuration requires values")
    entries = tuple(
        (occurrence("history", index), value)
        for index, value in enumerate(values)
    )
    contract = CarrierContract(
        CarrierKind.HISTORY,
        rank=1,
        shape=(len(values),),
        axes=("history",),
    )
    return FiniteConfiguration(
        Carrier(contract, Boundary(BoundaryPolicy.NONE)),
        entries,
    )


def centered_axis_values(size: int) -> tuple[int, ...]:
    if size <= 0:
        raise ValueError("axis size must be positive")
    low = -(size // 2)
    return tuple(range(low, low + size))


def grid_loci(
    shape: tuple[int, ...],
    *,
    axes: tuple[str, ...] | None = None,
) -> tuple[Locus, ...]:
    if len(shape) not in (1, 2, 3):
        raise ValueError("grid rank must be 1, 2, or 3")
    if axes is None:
        axes = ("x", "y", "z")[: len(shape)]
    if len(axes) != len(shape):
        raise ValueError("grid axes and shape must have equal rank")
    return tuple(
        cell(tuple(values), axes=axes)
        for values in cartesian_product(
            *(centered_axis_values(size) for size in shape)
        )
    )


def grid_configuration(
    shape: tuple[int, ...],
    values: tuple[V, ...],
    *,
    boundary: Boundary[V],
) -> FiniteConfiguration[V]:
    targets = grid_loci(shape)
    if len(values) != len(targets):
        raise ValueError(
            f"grid needs {len(targets)} values for shape {shape}, got {len(values)}"
        )
    axes = ("x", "y", "z")[: len(shape)]
    contract = CarrierContract(
        CarrierKind.GRID,
        rank=len(shape),
        shape=shape,
        axes=axes,
    )
    return FiniteConfiguration(
        Carrier(contract, boundary),
        tuple(zip(targets, values)),
    )


def resolve_region(
    region: Region,
    configuration: FiniteConfiguration[V],
) -> tuple[Locus, ...]:
    """Resolve the finite existing-locus portion of a raw region."""

    if region.kind is RegionKind.LITERAL:
        return region.loci
    if region.kind in (RegionKind.ALL_SUPPORT, RegionKind.CURRENT_SUPPORT):
        return tuple(target for target, _ in configuration.entries)
    if region.kind is RegionKind.UNION:
        seen: set[Locus] = set()
        out: list[Locus] = []
        for part in region.parts:
            for target in resolve_region(part, configuration):
                if target not in seen:
                    seen.add(target)
                    out.append(target)
        return tuple(sorted(out, key=canonical_order_key))
    if region.kind is RegionKind.PRODUCT:
        out: list[Locus] = []
        for part in region.parts:
            out.extend(resolve_region(part, configuration))
        return tuple(out)
    if region.kind is RegionKind.RELATIVE:
        anchors = resolve_relative_anchors(region, configuration)
        resolved: list[Locus] = []
        for anchor in anchors:
            for offset in region.offsets:
                resolved.append(_relative_target(configuration, anchor, offset))
        return tuple(resolved)
    raise LociResolutionError(
        f"region {region.kind.value} is not finitely resolvable"
    )


def resolve_fresh_references(region: Region) -> tuple[FreshReference, ...]:
    """Resolve the structurally declared fresh portion without binding it."""

    if region.kind in (
        RegionKind.LITERAL,
        RegionKind.FRESH_CHILDREN,
        RegionKind.FRESH_EDGES,
    ):
        return region.fresh
    if region.kind in (RegionKind.UNION, RegionKind.PRODUCT):
        out: list[FreshReference] = []
        for part in region.parts:
            out.extend(resolve_fresh_references(part))
        if len(out) != len(set(out)):
            raise LociResolutionError("fresh region contains duplicate local keys")
        return tuple(out)
    return ()


def resolve_relative_anchors(
    region: Region,
    configuration: FiniteConfiguration[V],
) -> tuple[Locus, ...]:
    """Resolve the anchor identities of one relative region."""

    if region.kind is not RegionKind.RELATIVE or len(region.parts) != 1:
        raise LociResolutionError("relative region needs one anchor part")
    anchors = resolve_region(region.parts[0], configuration)
    if configuration.contract.kind is CarrierKind.HISTORY:
        if not anchors:
            raise LociResolutionError("history has no relative anchor")
        return (max(anchors, key=_history_index),)
    return anchors


def _history_index(target: Locus) -> int:
    if target.kind is not LocusKind.OCCURRENCE or len(target.path) < 2:
        raise LociResolutionError("history anchor is not an occurrence")
    return int(target.path[-1])


def _offset_values(
    offset: Locus,
    axes: tuple[str, ...],
) -> tuple[int, ...]:
    if offset.kind is not LocusKind.COORDINATE:
        raise LociResolutionError("relative offset must be a coordinate locus")
    if offset.scope == "relative":
        if len(offset.path) != len(axes):
            raise LociResolutionError("relative offset rank disagrees with carrier")
        return tuple(int(value) for value in offset.path)
    if len(offset.path) == 2 and isinstance(offset.path[0], str):
        values = [0] * len(axes)
        try:
            index = axes.index(offset.path[0])
        except ValueError as error:
            raise LociResolutionError("offset axis is absent from carrier") from error
        values[index] = int(offset.path[1])
        return tuple(values)
    raise LociResolutionError("malformed relative coordinate offset")


def _relative_target(
    configuration: FiniteConfiguration[V],
    anchor: Locus,
    offset: Locus,
) -> Locus:
    contract = configuration.contract
    if contract.kind is CarrierKind.HISTORY:
        delta = _offset_values(offset, ("history",))[0]
        return occurrence("history", _history_index(anchor) + delta)
    if contract.kind is CarrierKind.GRID:
        coordinates = grid_coordinates(anchor)
        deltas = _offset_values(offset, contract.axes)
        return cell(
            tuple(value + delta for value, delta in zip(coordinates, deltas)),
            axes=contract.axes,
        )
    raise LociResolutionError(
        f"relative selection is unsupported for {contract.kind.value}"
    )


def grid_coordinates(target: Locus) -> tuple[int, ...]:
    if target.kind is not LocusKind.COORDINATE or not target.scope.startswith("grid:"):
        raise ValueError("target is not a grid-cell locus")
    values = target.path
    if len(values) % 2:
        raise ValueError("malformed grid-cell locus")
    return tuple(int(values[index]) for index in range(1, len(values), 2))


def read_grid_value(
    configuration: FiniteConfiguration[V],
    coordinates: tuple[int, ...],
) -> V | None:
    """Read one grid coordinate using the carrier's explicit boundary law."""

    contract = configuration.contract
    if contract.kind is not CarrierKind.GRID or contract.shape is None:
        raise ValueError("configuration is not a finite grid")
    axes = contract.axes
    bounds = tuple(centered_axis_values(size) for size in contract.shape)
    adjusted = list(coordinates)
    outside = False
    for index, (coordinate_value, axis_values) in enumerate(zip(adjusted, bounds)):
        if coordinate_value in axis_values:
            continue
        outside = True
        policy = configuration.carrier.boundary.policy
        if policy is BoundaryPolicy.NONE:
            return None
        if policy is BoundaryPolicy.FIXED:
            return configuration.carrier.boundary.exterior
        if policy is BoundaryPolicy.PERIODIC:
            adjusted[index] = axis_values[
                (coordinate_value - axis_values[0]) % len(axis_values)
            ]
        elif policy is BoundaryPolicy.REFLECTIVE:
            if len(axis_values) == 1:
                adjusted[index] = axis_values[0]
            else:
                period = 2 * (len(axis_values) - 1)
                offset = (coordinate_value - axis_values[0]) % period
                if offset >= len(axis_values):
                    offset = period - offset
                adjusted[index] = axis_values[offset]
    if outside and configuration.carrier.boundary.policy is BoundaryPolicy.FIXED:
        return configuration.carrier.boundary.exterior
    return configuration.value_at(cell(tuple(adjusted), axes=axes))


def configuration_identity(configuration: object) -> ConfigurationIdentity:
    """Validate and return the canonical identity of a recognized snapshot."""

    if not isinstance(configuration, (FiniteConfiguration, IntensionalConfiguration)):
        raise LociResolutionError(
            f"unknown configuration variant {type(configuration).__name__}"
        )
    return configuration.identity


def read_locus(
    configuration: FiniteConfiguration[V],
    target: Locus,
) -> V:
    """Read one locus using only configuration-owned absence/boundary data."""

    if configuration.contains(target):
        return configuration.value_at(target)
    if configuration.contract.kind is CarrierKind.GRID:
        try:
            coordinates = grid_coordinates(target)
        except ValueError as error:
            raise LocusAbsentError(target) from error
        value = read_grid_value(configuration, coordinates)
        if value is not None:
            return value
    raise LocusAbsentError(target)


OrderPart: TypeAlias = tuple[int, int | Fraction | str]


def canonical_order_key(
    value: Locus | FreshReference,
) -> tuple[OrderPart, ...]:
    """Return an exact, cross-type ordering key for structural identities."""

    if isinstance(value, FreshReference):
        return (
            (0, "fresh-reference"),
            (0, value.namespace),
            _scalar_order_part(value.local_key),
            (
                0,
                "" if value.parent is None else canonical_identity(value.parent),
            ),
            *((0, canonical_identity(item)) for item in value.interface),
        )
    return (
        (0, value.kind.value),
        (0, value.scope),
        *(_scalar_order_part(part) for part in value.path),
    )


def _scalar_order_part(value: ClosedScalar) -> OrderPart:
    if isinstance(value, bool):
        return (1, int(value))
    if isinstance(value, int):
        return (2, value)
    if isinstance(value, Fraction):
        return (3, value)
    return (4, value)


def _canonical_scalar(value: ClosedScalar) -> str:
    if isinstance(value, bool):
        return f"bool:{int(value)}"
    if isinstance(value, Fraction):
        return f"fraction:{value.numerator}/{value.denominator}"
    if isinstance(value, int):
        return f"int:{value}"
    return f"str:{len(value)}:{value}"


def _canonical_term(value: object) -> str:
    if isinstance(value, (bool, int, Fraction, str)):
        return _canonical_scalar(value)
    if isinstance(value, Enum):
        return f"enum:{value.__class__.__name__}:{value.value}"
    if isinstance(value, tuple):
        return "tuple[" + ",".join(_canonical_term(item) for item in value) + "]"
    if value is None:
        return "none"
    fields = getattr(value, "__dataclass_fields__", None)
    if fields is not None:
        parts = tuple(
            f"{name}={_canonical_term(getattr(value, name))}"
            for name in fields
        )
        return f"{value.__class__.__name__}(" + ",".join(parts) + ")"
    raise TypeError(f"{type(value).__name__} is not closed structural data")


def canonical_identity(value: object) -> str:
    """Derive a stable semantic identity from closed structural data."""

    payload = _canonical_term(value).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def semantic_equal(left: object, right: object) -> bool:
    """Exact structural equality with no representation or hash shortcut."""

    return type(left) is type(right) and _canonical_term(left) == _canonical_term(right)


def bind_fresh(
    reference: FreshReference,
    *,
    input_configuration_identity: str,
    canonical_rule_identity: str,
    witness_identity: str,
) -> Locus:
    """Bind one fresh local key from its semantic structural scope."""

    scope = canonical_identity(
        (
            input_configuration_identity,
            canonical_rule_identity,
            witness_identity,
            reference.namespace,
            reference.local_key,
            reference.parent,
            reference.interface,
        )
    )
    return Locus(
        LocusKind.FRESH,
        reference.namespace,
        (scope, reference.local_key),
    )


__all__ = [
    "Boundary",
    "BoundaryPolicy",
    "Carrier",
    "CarrierContract",
    "CarrierKind",
    "ClosedScalar",
    "Configuration",
    "ConfigurationIdentity",
    "FiniteConfiguration",
    "FreshReference",
    "IntensionalConfiguration",
    "Locus",
    "LocusAbsentError",
    "LocusKind",
    "LociResolutionError",
    "Region",
    "RegionKind",
    "SelectorExpr",
    "SelectorPrimitive",
    "StructuralRelation",
    "all_support",
    "bind_fresh",
    "canonical_identity",
    "canonical_order_key",
    "cell",
    "centered_axis_values",
    "continuous_region",
    "configuration_identity",
    "coordinate",
    "current_support",
    "field_point",
    "fresh_children",
    "fresh_reference",
    "graph_element",
    "grid_configuration",
    "grid_coordinates",
    "grid_loci",
    "history_configuration",
    "intensional",
    "intensional_reference",
    "interface",
    "literal",
    "named",
    "occurrence",
    "path",
    "port",
    "product_locus",
    "read_grid_value",
    "read_locus",
    "record_configuration",
    "region_product",
    "relative",
    "resolve_region",
    "resolve_fresh_references",
    "resolve_relative_anchors",
    "semantic_equal",
    "span",
    "union",
]
