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
        if not self.scope:
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
        if not self.namespace:
            raise ValueError("fresh namespace cannot be empty")


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
        if self.rank is not None and self.rank < 0:
            raise ValueError("carrier rank cannot be negative")
        if self.shape is not None:
            if any(size <= 0 for size in self.shape):
                raise ValueError("carrier shape extents must be positive")
            if self.rank is not None and len(self.shape) != self.rank:
                raise ValueError("carrier shape and rank disagree")
        if self.axes and self.rank is not None and len(self.axes) != self.rank:
            raise ValueError("carrier axes and rank disagree")

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
        if not self.tag:
            raise ValueError("structural relation tag cannot be empty")


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
        targets = tuple(target for target, _ in self.entries)
        if len(targets) != len(set(targets)):
            raise ValueError("configuration entries must have unique loci")
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


def grid_loci(shape: tuple[int, ...]) -> tuple[Locus, ...]:
    if len(shape) not in (1, 2, 3):
        raise ValueError("grid rank must be 1, 2, or 3")
    axes = ("x", "y", "z")[: len(shape)]
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
        return tuple(
            target
            for target in region.loci
            if configuration.contains(target)
        )
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
    raise ValueError(f"region {region.kind.value} is not finitely resolvable here")


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


def canonical_order_key(value: Locus | FreshReference) -> tuple[str, ...]:
    """Return an exact, cross-type ordering key for structural identities."""

    if isinstance(value, FreshReference):
        return (
            "fresh-reference",
            value.namespace,
            _canonical_scalar(value.local_key),
            "" if value.parent is None else canonical_identity(value.parent),
            *(canonical_identity(item) for item in value.interface),
        )
    return (
        value.kind.value,
        value.scope,
        *(_canonical_scalar(part) for part in value.path),
    )


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
    "FiniteConfiguration",
    "FreshReference",
    "IntensionalConfiguration",
    "Locus",
    "LocusKind",
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
    "record_configuration",
    "region_product",
    "relative",
    "resolve_region",
    "semantic_equal",
    "span",
    "union",
]
