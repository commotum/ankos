"""Closed structural identities, carriers, configurations, and regions.

``loci`` supplies structure shared by Seeds, writable regions, and readable
regions without itself granting read or write authority.  Every public value
is immutable and versioned; selectors are data, never Python callbacks.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from fractions import Fraction
from itertools import product as cartesian_product
from typing import Generic, TypeAlias, TypeVar


V = TypeVar("V")
ClosedScalar: TypeAlias = bool | int | Fraction | str
ConfigurationIdentity: TypeAlias = str


def _require_version_one(version: object, owner: str) -> None:
    if type(version) is not int:
        raise TypeError(f"{owner} version must be an integer")
    if version != 1:
        raise ValueError(f"unsupported {owner} version {version}")


def _is_closed_semantic_data(
    value: object,
    active: set[int] | None = None,
) -> bool:
    """Recognize immutable recursive data without importing downstream schemas."""

    if value is None or type(value) in (bool, int, Fraction, str):
        return True
    if isinstance(value, Enum):
        return _is_closed_semantic_data(value.value, active)
    if type(value) is tuple:
        return all(_is_closed_semantic_data(item, active) for item in value)
    if isinstance(value, type) or not is_dataclass(value):
        return False
    parameters = getattr(type(value), "__dataclass_params__", None)
    if parameters is None or not parameters.frozen:
        return False
    if active is None:
        active = set()
    marker = id(value)
    if marker in active:
        return False
    active.add(marker)
    try:
        return all(
            _is_closed_semantic_data(getattr(value, field.name), active)
            for field in fields(value)
        )
    finally:
        active.remove(marker)


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


@dataclass(frozen=True, eq=False)
class Locus:
    """One semantic identity; it carries no access capability."""

    kind: LocusKind
    scope: str
    path: tuple[ClosedScalar, ...]
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "locus")
        if type(self.kind) is not LocusKind:
            raise TypeError("locus kind is not recognized")
        if type(self.scope) is not str or not self.scope:
            raise ValueError("locus scope cannot be empty")
        if type(self.path) is not tuple:
            raise TypeError("locus path must be an immutable tuple")
        if any(type(part) not in (bool, int, Fraction, str) for part in self.path):
            raise TypeError("locus path contains an unclosed value")

    def __eq__(self, other: object) -> bool:
        return type(other) is Locus and canonical_identity(self) == canonical_identity(
            other
        )

    def __hash__(self) -> int:
        return hash((Locus, canonical_identity(self)))


@dataclass(frozen=True, eq=False)
class FreshReference:
    """A Rule-local fresh key, not yet a globally bound identity."""

    namespace: str
    local_key: ClosedScalar
    parent: Locus | None = None
    interface: tuple[Locus, ...] = ()
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "fresh-reference")
        if type(self.namespace) is not str or not self.namespace:
            raise ValueError("fresh namespace cannot be empty")
        if type(self.local_key) not in (bool, int, Fraction, str):
            raise TypeError("fresh-reference local key is not closed")
        if self.parent is not None and type(self.parent) is not Locus:
            raise TypeError("fresh-reference parent must be a Locus")
        if type(self.interface) is not tuple or any(
            type(item) is not Locus for item in self.interface
        ):
            raise TypeError("fresh-reference interface must contain Loci")

    def __eq__(self, other: object) -> bool:
        return type(
            other
        ) is FreshReference and canonical_identity(self) == canonical_identity(other)

    def __hash__(self) -> int:
        return hash((FreshReference, canonical_identity(self)))


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
    if type(coordinates) is not tuple:
        raise TypeError("cell coordinates must be an immutable tuple")
    if not coordinates:
        raise ValueError("cell coordinates cannot be empty")
    if any(type(value) is not int for value in coordinates):
        raise TypeError("cell coordinates must be integers")
    if axes is None:
        axes = ("x", "y", "z")[: len(coordinates)]
    elif type(axes) is not tuple:
        raise TypeError("cell axes must be an immutable tuple")
    if len(axes) != len(coordinates):
        raise ValueError("axes and coordinates must have equal length")
    if any(type(axis) is not str or not axis for axis in axes):
        raise TypeError("cell axes must be nonempty strings")
    if len(set(axes)) != len(axes):
        raise ValueError("cell axes must be unique")
    return Locus(
        LocusKind.COORDINATE,
        "grid:" + ",".join(axes),
        tuple(part for pair in zip(axes, coordinates) for part in pair),
    )


def occurrence(container: Locus | str, index: int) -> Locus:
    if type(container) is str:
        if not container:
            raise ValueError("occurrence container cannot be empty")
        token = container
    elif type(container) is Locus:
        token = _locus_token(container)
    else:
        raise TypeError("occurrence container must be a Locus or string")
    if type(index) is not int:
        raise TypeError("occurrence index must be an integer")
    return Locus(LocusKind.OCCURRENCE, "occurrence", (token, index))


def path(*segments: ClosedScalar, scope: str = "path") -> Locus:
    if not segments:
        raise ValueError("path requires at least one segment")
    return Locus(LocusKind.PATH, scope, tuple(segments))


def span(container: Locus | str, start: int, stop: int) -> Locus:
    if type(start) is not int or type(stop) is not int:
        raise TypeError("span bounds must be integers")
    if stop < start:
        raise ValueError("span stop must be >= start")
    if type(container) is str:
        if not container:
            raise ValueError("span container cannot be empty")
        token = container
    elif type(container) is Locus:
        token = _locus_token(container)
    else:
        raise TypeError("span container must be a Locus or string")
    return Locus(LocusKind.SPAN, "span", (token, start, stop))


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
    if type(field) is not str or not field:
        raise ValueError("field name must be a nonempty string")
    if type(coordinates) is not tuple:
        raise TypeError("field coordinates must be an immutable tuple")
    if any(
        type(value) not in (int, Fraction)
        for value in coordinates
    ):
        raise TypeError("field coordinates must be exact integers or Fractions")
    if component is not None and (type(component) is not str or not component):
        raise ValueError("field component must be a nonempty string or None")
    path_parts: tuple[ClosedScalar, ...] = (
        field,
        *(Fraction(value) for value in coordinates),
    )
    if component is not None:
        path_parts = (*path_parts, component)
    return Locus(LocusKind.FIELD_POINT, "field", path_parts)


def continuous_region(name: str, bounds: tuple[Fraction, ...]) -> Locus:
    if type(name) is not str or not name:
        raise ValueError("continuous-region name must be a nonempty string")
    if type(bounds) is not tuple or any(
        type(bound) is not Fraction for bound in bounds
    ):
        raise TypeError("continuous bounds must be exact Fractions")
    return Locus(
        LocusKind.CONTINUOUS,
        "continuous",
        (name, *(Fraction(bound) for bound in bounds)),
    )


def intensional_reference(binder: str, relation_id: str) -> Locus:
    if type(binder) is not str or not binder:
        raise ValueError("intensional binder must be a nonempty string")
    if type(relation_id) is not str or not relation_id:
        raise ValueError("intensional relation identity must be a nonempty string")
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
        _require_version_one(self.version, "selector")
        if type(self.primitive) is not SelectorPrimitive:
            raise TypeError("selector primitive is not recognized")
        if type(self.arguments) is not tuple or type(self.children) is not tuple:
            raise TypeError("selector arguments/children must be immutable tuples")
        if any(
            type(argument)
            not in (bool, int, Fraction, str, Locus, FreshReference)
            for argument in self.arguments
        ):
            raise TypeError("selector contains an opaque or executable argument")
        if any(type(child) is not SelectorExpr for child in self.children):
            raise TypeError("selector children must be SelectorExpr values")
        _validate_selector_shape(self)


def _validate_selector_shape(expression: SelectorExpr) -> None:
    primitive = expression.primitive
    arguments = expression.arguments
    children = expression.children
    if primitive is SelectorPrimitive.LITERAL:
        if (
            not arguments
            or children
            or any(
                type(argument) not in (Locus, FreshReference)
                for argument in arguments
            )
        ):
            raise ValueError(
                "literal selector needs only structural identity arguments"
            )
        return
    if primitive is SelectorPrimitive.EQUAL:
        if len(arguments) != 2 or children:
            raise ValueError(
                "selector.equal needs exactly two closed arguments"
            )
        return
    if primitive is SelectorPrimitive.TAGGED:
        if (
            len(arguments) != 1
            or type(arguments[0]) is not str
            or not arguments[0]
            or children
        ):
            raise ValueError("selector.tagged needs one nonempty tag")
        return
    if primitive is SelectorPrimitive.MEMBERSHIP:
        if arguments or children:
            raise ValueError(
                "membership selector is an obligation marker with no payload"
            )
        return
    if primitive is SelectorPrimitive.RELATIVE:
        if (
            len(arguments) != 1
            or type(arguments[0]) is not Locus
            or children
        ):
            raise ValueError(
                "relative selector needs exactly one Locus argument"
            )
        return
    if primitive is SelectorPrimitive.METRIC:
        if (
            len(arguments) != 2
            or type(arguments[0]) is not Locus
            or type(arguments[1]) not in (int, Fraction)
            or arguments[1] < 0
            or children
        ):
            raise ValueError(
                "selector.metric needs a Locus and a nonnegative exact radius"
            )
        return
    if primitive is SelectorPrimitive.PATH:
        if (
            len(arguments) != 1
            or type(arguments[0]) is not Locus
            or arguments[0].kind is not LocusKind.PATH
            or children
        ):
            raise ValueError("selector.path needs one path-prefix Locus")
        return
    if primitive is SelectorPrimitive.INCIDENCE:
        if (
            len(arguments) != 2
            or type(arguments[0]) is not Locus
            or type(arguments[1]) is not str
            or not arguments[1]
            or children
        ):
            raise ValueError(
                "selector.incidence needs an anchor Locus and relation tag"
            )
        return
    if primitive is SelectorPrimitive.REACHABLE:
        if (
            len(arguments) != 3
            or type(arguments[0]) is not Locus
            or type(arguments[1]) is not int
            or arguments[1] < 0
            or type(arguments[2]) is not str
            or not arguments[2]
            or children
        ):
            raise ValueError(
                "selector.reachable needs an anchor, nonnegative depth, and "
                "relation tag"
            )
        return
    if primitive is SelectorPrimitive.FIELD_RESTRICTION:
        bounds = arguments[1:]
        if (
            len(arguments) < 3
            or len(bounds) % 2
            or type(arguments[0]) is not str
            or not arguments[0]
            or any(type(bound) not in (int, Fraction) for bound in bounds)
            or any(
                bounds[index] > bounds[index + 1]
                for index in range(0, len(bounds), 2)
            )
            or children
        ):
            raise ValueError(
                "selector.field-restriction needs a field and exact "
                "lower/upper bound pairs"
            )
        return
    if primitive is SelectorPrimitive.DIFFERENTIAL_GERM:
        if (
            len(arguments) not in (2, 3)
            or type(arguments[0]) is not str
            or not arguments[0]
            or type(arguments[1]) is not int
            or arguments[1] < 0
            or (
                len(arguments) == 3
                and (
                    type(arguments[2]) is not str
                    or not arguments[2]
                )
            )
            or children
        ):
            raise ValueError(
                "selector.differential-germ needs a field, nonnegative "
                "derivative order, and optional component"
            )
        return
    if primitive is SelectorPrimitive.HISTORY:
        if (
            len(arguments) not in (0, 2)
            or any(type(argument) is not int for argument in arguments)
            or (
                len(arguments) == 2
                and arguments[1] < arguments[0]
            )
            or children
        ):
            raise ValueError(
                "selector.history needs no bounds or one ordered integer range"
            )
        return
    if primitive in (SelectorPrimitive.AND, SelectorPrimitive.OR):
        if arguments or len(children) < 2:
            raise ValueError(
                f"{primitive.value} needs at least two child selectors"
            )
        return
    if primitive is SelectorPrimitive.NOT:
        if arguments or len(children) != 1:
            raise ValueError("selector.not needs exactly one child selector")
        return
    raise AssertionError(f"unhandled selector primitive {primitive.value}")


def selector_literal(
    *targets: Locus | FreshReference,
) -> SelectorExpr:
    """Select an explicit nonempty tuple of structural identities."""

    return SelectorExpr(SelectorPrimitive.LITERAL, arguments=targets)


def selector_equal(
    left: SelectorArgument,
    right: SelectorArgument,
) -> SelectorExpr:
    """State exact equality between two closed selector terms."""

    return SelectorExpr(SelectorPrimitive.EQUAL, arguments=(left, right))


def selector_tagged(tag: str) -> SelectorExpr:
    """Select structure carrying one exact tag."""

    return SelectorExpr(SelectorPrimitive.TAGGED, arguments=(tag,))


def selector_path(
    *segments: ClosedScalar | Locus,
    scope: str = "path",
) -> SelectorExpr:
    """Select paths having one closed prefix."""

    if len(segments) == 1 and type(segments[0]) is Locus:
        prefix = segments[0]
    else:
        if any(type(segment) is Locus for segment in segments):
            raise TypeError("path selector cannot mix a Locus with path segments")
        prefix = path(*segments, scope=scope)  # type: ignore[arg-type]
    return SelectorExpr(SelectorPrimitive.PATH, arguments=(prefix,))


def selector_incidence(
    anchor: Locus,
    relation_tag: str = "incidence",
) -> SelectorExpr:
    """Select finite structure incident to ``anchor``."""

    return SelectorExpr(
        SelectorPrimitive.INCIDENCE,
        arguments=(anchor, relation_tag),
    )


def selector_reachable(
    anchor: Locus,
    max_depth: int,
    relation_tag: str = "incidence",
) -> SelectorExpr:
    """Select finite structure reachable within ``max_depth`` relations."""

    return SelectorExpr(
        SelectorPrimitive.REACHABLE,
        arguments=(anchor, max_depth, relation_tag),
    )


def selector_metric(
    anchor: Locus,
    radius: int | Fraction,
) -> SelectorExpr:
    """Select exact coordinate/field points within an L1 radius."""

    return SelectorExpr(
        SelectorPrimitive.METRIC,
        arguments=(anchor, radius),
    )


def selector_field_restriction(
    field: str,
    bounds: tuple[int | Fraction, ...],
) -> SelectorExpr:
    """Select one field over exact lower/upper bound pairs."""

    if type(bounds) is not tuple:
        raise TypeError("field restriction bounds must be an immutable tuple")
    return SelectorExpr(
        SelectorPrimitive.FIELD_RESTRICTION,
        arguments=(field, *bounds),
    )


def selector_differential_germ(
    field: str,
    order: int,
    *,
    component: str | None = None,
) -> SelectorExpr:
    """Describe an exact differential germ without choosing a stencil."""

    arguments: tuple[SelectorArgument, ...] = (field, order)
    if component is not None:
        arguments = (*arguments, component)
    return SelectorExpr(
        SelectorPrimitive.DIFFERENTIAL_GERM,
        arguments=arguments,
    )


def selector_history(
    start: int | None = None,
    stop: int | None = None,
) -> SelectorExpr:
    """Select all history occurrences or one exact half-open range."""

    if (start is None) != (stop is None):
        raise ValueError("history selector bounds must be supplied together")
    arguments: tuple[SelectorArgument, ...] = ()
    if start is not None and stop is not None:
        arguments = (start, stop)
    return SelectorExpr(SelectorPrimitive.HISTORY, arguments=arguments)


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


class FreshTemplateKind(Enum):
    """Closed ways to derive fresh references from current structure."""

    CHILDREN = "children"
    EDGES = "edges"


@dataclass(frozen=True)
class FreshTemplate:
    """A per-configuration fresh-reference template.

    A child template pairs every resolved parent with every local key.  An
    edge template takes the Cartesian product of its endpoint regions and
    pairs every resulting interface with every local key.
    """

    kind: FreshTemplateKind
    namespace: str
    local_keys: tuple[ClosedScalar, ...]
    parent_region: "Region | None" = None
    interface_regions: tuple["Region", ...] = ()
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "fresh-template")
        if type(self.kind) is not FreshTemplateKind:
            raise TypeError("fresh-template kind is not recognized")
        if type(self.namespace) is not str or not self.namespace:
            raise ValueError("fresh-template namespace cannot be empty")
        if type(self.local_keys) is not tuple or not self.local_keys:
            raise ValueError("fresh-template local keys must be a nonempty tuple")
        if any(
            type(local_key) not in (bool, int, Fraction, str)
            for local_key in self.local_keys
        ):
            raise TypeError("fresh-template local key is not closed")
        local_key_terms = tuple(
            _canonical_scalar(local_key) for local_key in self.local_keys
        )
        if len(set(local_key_terms)) != len(local_key_terms):
            raise ValueError("fresh-template local keys must be unique")
        if self.parent_region is not None and type(self.parent_region) is not Region:
            raise TypeError("fresh-template parent region is not recognized")
        if type(self.interface_regions) is not tuple or any(
            type(region) is not Region for region in self.interface_regions
        ):
            raise TypeError(
                "fresh-template interface regions must contain Region values"
            )
        if self.kind is FreshTemplateKind.CHILDREN:
            if self.parent_region is None or self.interface_regions:
                raise ValueError(
                    "child fresh-template needs one parent region only"
                )
        elif self.parent_region is not None or len(self.interface_regions) < 2:
            raise ValueError(
                "edge fresh-template needs at least two interface regions only"
            )


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
    templates: tuple[FreshTemplate, ...] = ()
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "region")
        if type(self.kind) is not RegionKind:
            raise TypeError("region kind is not recognized")
        if any(
            type(value) is not tuple
            for value in (
                self.loci,
                self.fresh,
                self.parts,
                self.offsets,
                self.templates,
            )
        ):
            raise TypeError("region collections must be immutable tuples")
        if self.name is not None and (type(self.name) is not str or not self.name):
            raise TypeError("region name must be a string or None")
        if any(type(item) is not Locus for item in self.loci):
            raise TypeError("region loci must contain Locus values")
        if any(type(item) is not FreshReference for item in self.fresh):
            raise TypeError("region fresh targets must contain FreshReference values")
        if any(type(item) is not Region for item in self.parts):
            raise TypeError("region parts must contain Region values")
        if any(type(item) is not Locus for item in self.offsets):
            raise TypeError("region offsets must contain Locus values")
        if self.relation is not None and type(self.relation) is not SelectorExpr:
            raise TypeError("region relation must be a SelectorExpr")
        if any(type(item) is not FreshTemplate for item in self.templates):
            raise TypeError("region templates must contain FreshTemplate values")
        if len(set(map(canonical_identity, self.templates))) != len(
            self.templates
        ):
            raise ValueError("region contains duplicate fresh templates")
        if self.kind is RegionKind.LITERAL and not (self.loci or self.fresh):
            raise ValueError("literal region cannot be empty")
        if self.kind in (
            RegionKind.UNION,
            RegionKind.INTERSECTION,
            RegionKind.PRODUCT,
        ) and not self.parts:
            raise ValueError(f"{self.kind.value} region requires parts")
        if self.kind is RegionKind.INTENSIONAL and self.relation is None:
            raise ValueError("intensional region requires a relation")
        if self.kind in (RegionKind.UNION, RegionKind.INTERSECTION):
            ordered = tuple(sorted(self.parts, key=canonical_identity))
            identities = tuple(canonical_identity(part) for part in self.parts)
            ordered_identities = tuple(canonical_identity(part) for part in ordered)
            if len(set(ordered_identities)) != len(ordered):
                raise ValueError(
                    f"{self.kind.value} region contains duplicate parts"
                )
            if ordered_identities != identities:
                object.__setattr__(self, "parts", ordered)
        _validate_region_shape(self)


def _validate_region_shape(region: Region) -> None:
    kind = region.kind
    if kind is RegionKind.LITERAL:
        if (
            not (region.loci or region.fresh)
            or region.parts
            or region.offsets
            or region.relation is not None
            or region.templates
        ):
            raise ValueError("literal region carries irrelevant fields")
        if len(set(region.loci)) != len(region.loci):
            raise ValueError("literal region contains duplicate loci")
        if len(set(region.fresh)) != len(region.fresh):
            raise ValueError("literal region contains duplicate fresh references")
        return
    if kind in (RegionKind.ALL_SUPPORT, RegionKind.CURRENT_SUPPORT):
        if (
            not region.name
            or region.loci
            or region.fresh
            or region.parts
            or region.offsets
            or region.relation is not None
            or region.templates
        ):
            raise ValueError(f"{kind.value} region carries irrelevant fields")
        return
    if kind is RegionKind.RELATIVE:
        if (
            region.name is not None
            or region.loci
            or region.fresh
            or len(region.parts) != 1
            or not region.offsets
            or region.relation is not None
            or region.templates
        ):
            raise ValueError("relative region descriptor shape is invalid")
        return
    if kind is RegionKind.UNION:
        if (
            region.name is not None
            or region.loci
            or region.fresh
            or not region.parts
            or region.offsets
            or region.relation is not None
            or region.templates
        ):
            raise ValueError("union region carries irrelevant fields")
        return
    if kind is RegionKind.INTERSECTION:
        if (
            region.name is not None
            or region.loci
            or region.fresh
            or len(region.parts) < 2
            or region.offsets
            or region.relation is not None
            or region.templates
        ):
            raise ValueError("intersection region carries irrelevant fields")
        return
    if kind is RegionKind.DIFFERENCE:
        if (
            region.name is not None
            or region.loci
            or region.fresh
            or len(region.parts) != 2
            or region.offsets
            or region.relation is not None
            or region.templates
        ):
            raise ValueError("difference region descriptor shape is invalid")
        return
    if kind is RegionKind.SPAN:
        if (
            region.name is not None
            or len(region.loci) != 1
            or region.loci[0].kind is not LocusKind.SPAN
            or region.fresh
            or region.parts
            or region.offsets
            or region.relation is not None
            or region.templates
        ):
            raise ValueError("span region descriptor shape is invalid")
        return
    if kind is RegionKind.PATH:
        if (
            region.name is not None
            or len(region.loci) != 1
            or region.loci[0].kind is not LocusKind.PATH
            or region.fresh
            or region.parts
            or region.offsets
            or region.relation is not None
            or region.templates
        ):
            raise ValueError("path region descriptor shape is invalid")
        return
    if kind is RegionKind.MATCHED_INTERFACE:
        if (
            not region.name
            or region.loci
            or region.fresh
            or len(region.parts) != 2
            or region.offsets
            or region.relation is not None
            or region.templates
        ):
            raise ValueError(
                "matched-interface region descriptor shape is invalid"
            )
        return
    if kind is RegionKind.DYNAMIC_ADDRESS:
        if (
            not region.name
            or region.loci
            or region.fresh
            or len(region.parts) != 1
            or region.offsets
            or region.relation is not None
            or region.templates
        ):
            raise ValueError(
                "dynamic-address region descriptor shape is invalid"
            )
        return
    if kind is RegionKind.PRODUCT:
        if (
            region.loci
            or region.fresh
            or not region.parts
            or region.offsets
            or region.relation is not None
            or region.templates
            or (region.name is not None and len(region.parts) != 1)
        ):
            raise ValueError("product region descriptor shape is invalid")
        return
    if kind in (RegionKind.FRESH_CHILDREN, RegionKind.FRESH_EDGES):
        if (
            not region.name
            or region.loci
            or region.parts
            or region.offsets
            or region.relation is not None
            or bool(region.fresh) == bool(region.templates)
        ):
            raise ValueError(f"{kind.value} region descriptor shape is invalid")
        if any(reference.namespace != region.name for reference in region.fresh):
            raise ValueError(
                f"{kind.value} references must use the region namespace"
            )
        if len(set(region.fresh)) != len(region.fresh):
            raise ValueError(f"{kind.value} region contains duplicate references")
        if kind is RegionKind.FRESH_CHILDREN and any(
            reference.parent is None or reference.interface
            for reference in region.fresh
        ):
            raise ValueError(
                "fresh-children references need one parent and no interface"
            )
        if kind is RegionKind.FRESH_EDGES and any(
            reference.parent is not None or len(reference.interface) < 2
            for reference in region.fresh
        ):
            raise ValueError(
                "fresh-edges references need an interface and no parent"
            )
        expected_template_kind = (
            FreshTemplateKind.CHILDREN
            if kind is RegionKind.FRESH_CHILDREN
            else FreshTemplateKind.EDGES
        )
        if any(
            template.namespace != region.name
            or template.kind is not expected_template_kind
            for template in region.templates
        ):
            raise ValueError(
                f"{kind.value} templates must use the region namespace and kind"
            )
        return
    if kind is RegionKind.CONTINUOUS:
        if (
            not region.name
            or len(region.loci) != 1
            or region.loci[0].kind is not LocusKind.CONTINUOUS
            or region.fresh
            or region.parts
            or region.offsets
            or region.relation is not None
            or region.templates
        ):
            raise ValueError("continuous region descriptor shape is invalid")
        return
    if kind is RegionKind.DIFFERENTIAL:
        if (
            not region.name
            or region.loci
            or region.fresh
            or region.parts
            or region.offsets
            or region.relation is None
            or region.templates
        ):
            raise ValueError("differential region descriptor shape is invalid")
        if region.relation.primitive is not SelectorPrimitive.DIFFERENTIAL_GERM:
            raise ValueError(
                "differential region requires a differential-germ selector"
            )
        return
    if kind is RegionKind.INTENSIONAL:
        if (
            not region.name
            or region.loci
            or region.fresh
            or region.parts
            or region.offsets
            or region.relation is None
            or region.templates
        ):
            raise ValueError("intensional region descriptor shape is invalid")
        return
    raise AssertionError(f"unhandled region kind {kind.value}")


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


def intersection(parts: tuple[Region, ...]) -> Region:
    """Return the canonical finite intersection of at least two regions."""

    return Region(RegionKind.INTERSECTION, parts=parts)


def difference(base: Region, excluded: Region) -> Region:
    """Return loci in ``base`` that are not in ``excluded``."""

    return Region(RegionKind.DIFFERENCE, parts=(base, excluded))


def span_region(container: Locus | str, start: int, stop: int) -> Region:
    """Select existing ordered occurrences in one half-open span."""

    return Region(
        RegionKind.SPAN,
        loci=(span(container, start, stop),),
    )


def path_region(prefix: Locus) -> Region:
    """Select existing path loci whose paths begin with ``prefix``."""

    if type(prefix) is not Locus:
        raise TypeError("path-region prefix must be a Locus")
    return Region(RegionKind.PATH, loci=(prefix,))


def matched_interface(
    left: Region,
    right: Region,
    relation_tag: str = "interface",
) -> Region:
    """Select existing interface/edge loci joining two finite regions."""

    return Region(
        RegionKind.MATCHED_INTERFACE,
        name=relation_tag,
        parts=(left, right),
    )


def dynamic_address(
    sources: Region,
    relation_tag: str = "address",
) -> Region:
    """Resolve targets addressed by current structural state."""

    return Region(
        RegionKind.DYNAMIC_ADDRESS,
        name=relation_tag,
        parts=(sources,),
    )


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


def fresh_edges(
    interface_loci: tuple[Locus, ...],
    namespace: str,
    local_keys: tuple[ClosedScalar, ...],
) -> Region:
    """Declare static fresh edges over one explicit interface."""

    if type(interface_loci) is not tuple or len(interface_loci) < 2:
        raise ValueError("fresh edges require at least two interface Loci")
    if any(type(target) is not Locus for target in interface_loci):
        raise TypeError("fresh-edge interface must contain Loci")
    return Region(
        RegionKind.FRESH_EDGES,
        name=namespace,
        fresh=tuple(
            FreshReference(
                namespace,
                local_key,
                interface=interface_loci,
            )
            for local_key in local_keys
        ),
    )


def fresh_children_dynamic(
    parents: Region,
    namespace: str,
    local_keys: tuple[ClosedScalar, ...],
) -> Region:
    """Derive child capabilities afresh from every current parent."""

    return Region(
        RegionKind.FRESH_CHILDREN,
        name=namespace,
        templates=(
            FreshTemplate(
                FreshTemplateKind.CHILDREN,
                namespace,
                local_keys,
                parent_region=parents,
            ),
        ),
    )


def fresh_edges_dynamic(
    interface_regions: tuple[Region, ...],
    namespace: str,
    local_keys: tuple[ClosedScalar, ...],
) -> Region:
    """Derive edge capabilities from current endpoint combinations."""

    return Region(
        RegionKind.FRESH_EDGES,
        name=namespace,
        templates=(
            FreshTemplate(
                FreshTemplateKind.EDGES,
                namespace,
                local_keys,
                interface_regions=interface_regions,
            ),
        ),
    )


def continuous(
    name: str,
    bounds: tuple[Fraction, ...],
) -> Region:
    """Describe a closed continuous region without finite enumeration."""

    return Region(
        RegionKind.CONTINUOUS,
        name=name,
        loci=(continuous_region(name, bounds),),
    )


def differential(
    name: str,
    relation: SelectorExpr,
) -> Region:
    """Describe a closed differential region without choosing a stencil."""

    return Region(
        RegionKind.DIFFERENTIAL,
        name=name,
        relation=relation,
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


class ConfigurationIdentityLaw(Enum):
    """Semantic equality law declared by a configuration carrier."""

    EXACT = "exact"
    BOUND_FRESH_ALPHA = "bound-fresh-alpha"


@dataclass(frozen=True)
class CarrierContract:
    """Closed structural contract shared independently by program components."""

    kind: CarrierKind
    rank: int | None = None
    shape: tuple[int, ...] | None = None
    axes: tuple[str, ...] = ()
    version: int = 1
    identity_law: ConfigurationIdentityLaw = ConfigurationIdentityLaw.EXACT

    def __post_init__(self) -> None:
        _require_version_one(self.version, "carrier-contract")
        if type(self.kind) is not CarrierKind:
            raise TypeError("carrier kind is not recognized")
        if type(self.identity_law) is not ConfigurationIdentityLaw:
            raise TypeError("configuration identity law is not recognized")
        if self.shape is not None and type(self.shape) is not tuple:
            raise TypeError("carrier shape must be an immutable tuple")
        if type(self.axes) is not tuple:
            raise TypeError("carrier axes must be an immutable tuple")
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
            and self.identity_law is other.identity_law
        )


@dataclass(frozen=True)
class Boundary(Generic[V]):
    policy: BoundaryPolicy
    exterior: V | None = None
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "boundary")
        if type(self.policy) is not BoundaryPolicy:
            raise TypeError("boundary policy is not recognized")
        if self.policy is BoundaryPolicy.FIXED and self.exterior is None:
            raise ValueError("fixed boundary requires an exterior value")
        if self.policy is not BoundaryPolicy.FIXED and self.exterior is not None:
            raise ValueError("only fixed boundary carries an exterior value")
        if (
            self.policy is BoundaryPolicy.FIXED
            and not _is_closed_semantic_data(self.exterior)
        ):
            raise TypeError(
                "fixed boundary exterior must be closed immutable semantic data"
            )


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
        if type(self.attributes) is not tuple:
            raise TypeError("carrier attributes must be an immutable tuple")
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
        _require_version_one(self.version, "structural relation")
        if type(self.tag) is not str or not self.tag:
            raise ValueError("structural relation tag cannot be empty")
        if type(self.arguments) is not tuple:
            raise TypeError("structural relation arguments must be an immutable tuple")
        if any(
            type(argument) not in (bool, int, Fraction, str, Locus)
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
        if type(self.entries) is not tuple or type(self.structure) is not tuple:
            raise TypeError("configuration data must use immutable tuples")
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
        if any(
            isinstance(argument, Locus) and argument not in targets
            for relation in self.structure
            for argument in relation.arguments
        ):
            raise ValueError(
                "configuration structural relations reference absent loci"
            )
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
        if (
            contract.identity_law
            is ConfigurationIdentityLaw.BOUND_FRESH_ALPHA
        ):
            _validate_bound_fresh_identity_targets(targets)
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
        return configuration_identity(self)

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
        if type(self.contract) is not CarrierContract:
            raise TypeError("intensional configuration contract is not recognized")
        if type(self.relation) is not SelectorExpr:
            raise TypeError("intensional configuration relation is not recognized")
        if not isinstance(self.identity_evidence, str):
            raise TypeError("intensional identity evidence must be a string")

    @property
    def identity(self) -> str:
        return configuration_identity(self)

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
    if region.kind is RegionKind.INTERSECTION:
        resolved_parts = tuple(
            resolve_region(part, configuration) for part in region.parts
        )
        common = set(resolved_parts[0])
        for resolved in resolved_parts[1:]:
            common.intersection_update(resolved)
        return tuple(sorted(common, key=canonical_order_key))
    if region.kind is RegionKind.DIFFERENCE:
        base = resolve_region(region.parts[0], configuration)
        excluded = set(resolve_region(region.parts[1], configuration))
        return tuple(target for target in base if target not in excluded)
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
    if region.kind is RegionKind.SPAN:
        descriptor = region.loci[0]
        container, start, stop = descriptor.path
        return tuple(
            target
            for target, _ in configuration.entries
            if target.kind is LocusKind.OCCURRENCE
            and len(target.path) >= 2
            and target.path[0] == container
            and type(target.path[-1]) is int
            and start <= target.path[-1] < stop
        )
    if region.kind is RegionKind.PATH:
        prefix = region.loci[0]
        return tuple(
            target
            for target, _ in configuration.entries
            if _has_path_prefix(target, prefix)
        )
    if region.kind is RegionKind.MATCHED_INTERFACE:
        return _resolve_matched_interface(region, configuration)
    if region.kind is RegionKind.DYNAMIC_ADDRESS:
        return _resolve_dynamic_address(region, configuration)
    if region.kind in (
        RegionKind.CONTINUOUS,
        RegionKind.DIFFERENTIAL,
        RegionKind.INTENSIONAL,
    ):
        raise LociResolutionError(
            f"{region.kind.value} region is closed but non-enumerated"
        )
    if region.kind in (
        RegionKind.FRESH_CHILDREN,
        RegionKind.FRESH_EDGES,
    ):
        return ()
    raise LociResolutionError(
        f"region {region.kind.value} is not finitely resolvable"
    )


def resolve_fresh_references(
    region: Region,
    configuration: FiniteConfiguration[object] | None = None,
) -> tuple[FreshReference, ...]:
    """Resolve the structurally declared fresh portion without binding it."""

    if region.kind is RegionKind.LITERAL:
        return region.fresh
    if region.kind in (RegionKind.FRESH_CHILDREN, RegionKind.FRESH_EDGES):
        if region.fresh:
            return region.fresh
        if configuration is None:
            raise LociResolutionError(
                "dynamic fresh-template resolution needs a configuration"
            )
        out: list[FreshReference] = []
        for template in region.templates:
            if template.kind is FreshTemplateKind.CHILDREN:
                assert template.parent_region is not None
                parents = tuple(
                    parent
                    for parent in resolve_region(
                        template.parent_region,
                        configuration,
                    )
                    if configuration.contains(parent)
                )
                out.extend(
                    FreshReference(template.namespace, local_key, parent)
                    for parent in parents
                    for local_key in template.local_keys
                )
            else:
                interfaces = tuple(
                    tuple(
                        target
                        for target in resolve_region(
                            interface_region,
                            configuration,
                        )
                        if configuration.contains(target)
                    )
                    for interface_region in template.interface_regions
                )
                out.extend(
                    FreshReference(
                        template.namespace,
                        local_key,
                        interface=tuple(interface_loci),
                    )
                    for interface_loci in cartesian_product(*interfaces)
                    for local_key in template.local_keys
                )
        if len(out) != len(set(out)):
            raise LociResolutionError(
                "dynamic fresh templates resolve duplicate references"
            )
        return tuple(sorted(out, key=canonical_order_key))
    if region.kind in (RegionKind.UNION, RegionKind.PRODUCT):
        out: list[FreshReference] = []
        for part in region.parts:
            out.extend(resolve_fresh_references(part, configuration))
        if len(out) != len(set(out)):
            raise LociResolutionError("fresh region contains duplicate local keys")
        return tuple(out)
    if region.kind is RegionKind.INTERSECTION:
        resolved_parts = tuple(
            resolve_fresh_references(part, configuration)
            for part in region.parts
        )
        common = set(resolved_parts[0])
        for resolved in resolved_parts[1:]:
            common.intersection_update(resolved)
        return tuple(sorted(common, key=canonical_order_key))
    if region.kind is RegionKind.DIFFERENCE:
        base = resolve_fresh_references(region.parts[0], configuration)
        excluded = set(
            resolve_fresh_references(region.parts[1], configuration)
        )
        return tuple(target for target in base if target not in excluded)
    return ()


def resolve_selector(
    expression: SelectorExpr,
    configuration: FiniteConfiguration[V],
    *,
    candidates: tuple[Locus, ...] | None = None,
) -> tuple[Locus, ...]:
    """Resolve one finitely decidable selector over a finite configuration.

    Membership and differential-germ expressions deliberately remain closed
    non-enumerated contracts and therefore fail rather than approximate.
    """

    if type(expression) is not SelectorExpr:
        raise TypeError("selector expression is not recognized")
    if type(configuration) is not FiniteConfiguration:
        raise TypeError("selector resolution needs a FiniteConfiguration")
    if candidates is None:
        candidates = tuple(target for target, _ in configuration.entries)
    elif type(candidates) is not tuple or any(
        type(target) is not Locus for target in candidates
    ):
        raise TypeError("selector candidates must be an immutable tuple of Loci")

    primitive = expression.primitive
    arguments = expression.arguments
    if primitive is SelectorPrimitive.LITERAL:
        return tuple(
            target
            for target in arguments
            if type(target) is Locus and target in candidates
        )
    if primitive is SelectorPrimitive.EQUAL:
        left, right = arguments
        selected: list[Locus] = []
        if type(left) is Locus and type(right) is Locus:
            if (
                configuration.contains(left)
                and configuration.contains(right)
                and _canonical_term(configuration.value_at(left))
                == _canonical_term(configuration.value_at(right))
            ):
                selected.extend(
                    target
                    for target in (left, right)
                    if target in candidates and target not in selected
                )
        elif type(left) is Locus and configuration.contains(left):
            if _canonical_term(configuration.value_at(left)) == _canonical_term(
                right
            ):
                selected.append(left)
        elif type(right) is Locus and configuration.contains(right):
            if _canonical_term(configuration.value_at(right)) == _canonical_term(
                left
            ):
                selected.append(right)
        return tuple(selected)
    if primitive is SelectorPrimitive.TAGGED:
        tag = arguments[0]
        assert type(tag) is str
        structurally_tagged = {
            argument
            for relation in configuration.structure
            if relation.tag == tag
            for argument in relation.arguments
            if type(argument) is Locus
        }
        return tuple(
            target
            for target in candidates
            if target.kind.value == tag
            or target.scope == tag
            or target in structurally_tagged
        )
    if primitive is SelectorPrimitive.RELATIVE:
        target = arguments[0]
        assert type(target) is Locus
        return (target,) if target in candidates else ()
    if primitive is SelectorPrimitive.METRIC:
        anchor, radius = arguments
        assert type(anchor) is Locus
        assert type(radius) in (int, Fraction)
        selected: list[Locus] = []
        for target in candidates:
            distance = _l1_distance(anchor, target)
            if distance is not None and distance <= radius:
                selected.append(target)
        return tuple(selected)
    if primitive is SelectorPrimitive.PATH:
        prefix = arguments[0]
        assert type(prefix) is Locus
        return tuple(
            target
            for target in candidates
            if _has_path_prefix(target, prefix)
        )
    if primitive in (
        SelectorPrimitive.INCIDENCE,
        SelectorPrimitive.REACHABLE,
    ):
        anchor = arguments[0]
        assert type(anchor) is Locus
        depth = 1
        relation_tag = arguments[1]
        if primitive is SelectorPrimitive.REACHABLE:
            depth = arguments[1]
            relation_tag = arguments[2]
        assert type(depth) is int and type(relation_tag) is str
        reachable = _reachable_loci(
            configuration,
            anchor,
            depth,
            relation_tag,
        )
        if primitive is SelectorPrimitive.INCIDENCE:
            reachable.discard(anchor)
        return tuple(target for target in candidates if target in reachable)
    if primitive is SelectorPrimitive.FIELD_RESTRICTION:
        field = arguments[0]
        bounds = arguments[1:]
        assert type(field) is str
        return tuple(
            target
            for target in candidates
            if _field_point_within(target, field, bounds)
        )
    if primitive is SelectorPrimitive.HISTORY:
        if arguments:
            start, stop = arguments
            assert type(start) is int and type(stop) is int
        else:
            start = None
            stop = None
        return tuple(
            target
            for target in candidates
            if target.kind is LocusKind.OCCURRENCE
            and len(target.path) >= 2
            and target.path[0] == "history"
            and type(target.path[-1]) is int
            and (
                start is None
                or start <= target.path[-1] < stop  # type: ignore[operator]
            )
        )
    if primitive in (SelectorPrimitive.AND, SelectorPrimitive.OR):
        resolved_children = tuple(
            resolve_selector(child, configuration, candidates=candidates)
            for child in expression.children
        )
        if primitive is SelectorPrimitive.AND:
            selected = set(resolved_children[0])
            for child_targets in resolved_children[1:]:
                selected.intersection_update(child_targets)
        else:
            selected = {
                target
                for child_targets in resolved_children
                for target in child_targets
            }
        return tuple(target for target in candidates if target in selected)
    if primitive is SelectorPrimitive.NOT:
        excluded = set(
            resolve_selector(
                expression.children[0],
                configuration,
                candidates=candidates,
            )
        )
        return tuple(target for target in candidates if target not in excluded)
    if primitive in (
        SelectorPrimitive.MEMBERSHIP,
        SelectorPrimitive.DIFFERENTIAL_GERM,
    ):
        raise LociResolutionError(
            f"{primitive.value} selector is closed but non-enumerated"
        )
    raise AssertionError(f"unhandled selector primitive {primitive.value}")


def _has_path_prefix(target: Locus, prefix: Locus) -> bool:
    return (
        target.kind is LocusKind.PATH
        and prefix.kind is LocusKind.PATH
        and target.scope == prefix.scope
        and target.path[: len(prefix.path)] == prefix.path
    )


def _relation_loci(relation: StructuralRelation) -> tuple[Locus, ...]:
    return tuple(
        argument
        for argument in relation.arguments
        if type(argument) is Locus
    )


def _resolve_matched_interface(
    region: Region,
    configuration: FiniteConfiguration[V],
) -> tuple[Locus, ...]:
    left = set(resolve_region(region.parts[0], configuration))
    right = set(resolve_region(region.parts[1], configuration))
    selected: set[Locus] = set()
    for relation in configuration.structure:
        if relation.tag != region.name:
            continue
        relation_loci = _relation_loci(relation)
        if not any(target in left for target in relation_loci) or not any(
            target in right for target in relation_loci
        ):
            continue
        selected.update(
            target
            for target in relation_loci
            if target.kind is LocusKind.INTERFACE
            or (
                target.kind is LocusKind.GRAPH_ELEMENT
                and target.path
                and target.path[0] in ("edge", "port")
            )
        )
    interface_candidates = tuple(
        target
        for target, _ in configuration.entries
        if target.kind is LocusKind.INTERFACE
    )
    for left_target in left:
        for right_target in right:
            expected = interface(
                left_target,
                right_target,
                name=region.name or "interface",
            )
            if expected in interface_candidates:
                selected.add(expected)
    return tuple(sorted(selected, key=canonical_order_key))


def _resolve_dynamic_address(
    region: Region,
    configuration: FiniteConfiguration[V],
) -> tuple[Locus, ...]:
    sources = set(resolve_region(region.parts[0], configuration))
    selected: set[Locus] = set()
    for relation in configuration.structure:
        if relation.tag != region.name:
            continue
        relation_loci = _relation_loci(relation)
        if relation_loci and relation_loci[0] in sources:
            selected.update(
                target
                for target in relation_loci[1:]
                if configuration.contains(target)
            )
    for source in sources:
        if not configuration.contains(source):
            continue
        value = configuration.value_at(source)
        if type(value) is Locus and configuration.contains(value):
            selected.add(value)
    return tuple(sorted(selected, key=canonical_order_key))


def _reachable_loci(
    configuration: FiniteConfiguration[V],
    anchor: Locus,
    max_depth: int,
    relation_tag: str,
) -> set[Locus]:
    adjacency: dict[Locus, set[Locus]] = {}
    for relation in configuration.structure:
        if relation.tag != relation_tag:
            continue
        relation_loci = _relation_loci(relation)
        for source in relation_loci:
            adjacency.setdefault(source, set()).update(
                target for target in relation_loci if target != source
            )
    reached = {anchor}
    frontier = {anchor}
    for _ in range(max_depth):
        frontier = {
            target
            for source in frontier
            for target in adjacency.get(source, ())
            if target not in reached
        }
        reached.update(frontier)
        if not frontier:
            break
    return reached


def _l1_distance(left: Locus, right: Locus) -> int | Fraction | None:
    if (
        left.kind is LocusKind.COORDINATE
        and right.kind is LocusKind.COORDINATE
        and left.scope == right.scope
    ):
        if left.scope.startswith("grid:"):
            left_values = grid_coordinates(left)
            right_values = grid_coordinates(right)
        elif (
            len(left.path) == 2
            and len(right.path) == 2
            and type(left.path[0]) is str
            and type(right.path[0]) is str
            and left.path[0] == right.path[0]
            and type(left.path[1]) is int
            and type(right.path[1]) is int
        ):
            left_values = (left.path[1],)
            right_values = (right.path[1],)
        elif all(type(value) is int for value in (*left.path, *right.path)):
            left_values = left.path
            right_values = right.path
        else:
            return None
    elif (
        left.kind is LocusKind.FIELD_POINT
        and right.kind is LocusKind.FIELD_POINT
        and left.path
        and right.path
        and left.path[0] == right.path[0]
    ):
        left_component = tuple(
            value for value in left.path[1:] if type(value) is str
        )
        right_component = tuple(
            value for value in right.path[1:] if type(value) is str
        )
        if left_component != right_component:
            return None
        left_values = tuple(
            value
            for value in left.path[1:]
            if type(value) in (int, Fraction)
        )
        right_values = tuple(
            value
            for value in right.path[1:]
            if type(value) in (int, Fraction)
        )
    else:
        return None
    if len(left_values) != len(right_values):
        return None
    return sum(
        (abs(left_value - right_value) for left_value, right_value in zip(
            left_values, right_values
        )),
        Fraction(0),
    )


def _field_point_within(
    target: Locus,
    field: str,
    bounds: tuple[SelectorArgument, ...],
) -> bool:
    if (
        target.kind is not LocusKind.FIELD_POINT
        or not target.path
        or target.path[0] != field
    ):
        return False
    coordinates = tuple(
        value
        for value in target.path[1:]
        if type(value) in (int, Fraction)
    )
    if len(coordinates) * 2 != len(bounds):
        return False
    return all(
        bounds[2 * index] <= coordinate <= bounds[2 * index + 1]  # type: ignore[operator]
        for index, coordinate in enumerate(coordinates)
    )


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
    semantic_term = _configuration_semantic_term(configuration)
    return hashlib.sha256(semantic_term.encode("utf-8")).hexdigest()


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


def _bound_fresh_key(
    target: Locus,
) -> tuple[str, str, tuple[str, ...]] | None:
    if target.kind is not LocusKind.FRESH:
        return None
    if (
        len(target.path) < 2
        or type(target.path[0]) is not str
        or not target.path[0]
        or type(target.path[1]) not in (bool, int, Fraction, str)
    ):
        raise ValueError(
            "bound-fresh alpha identity requires bound loci with "
            "(binding-scope, local-key, optional-anchor) paths"
        )
    anchor = target.path[2:]
    index = 0
    if index < len(anchor) and anchor[index] == "parent":
        if index + 1 >= len(anchor) or type(anchor[index + 1]) is not str:
            raise ValueError("bound-fresh parent anchor is malformed")
        index += 2
    if index < len(anchor) and anchor[index] == "interface":
        if (
            index + 1 >= len(anchor)
            or type(anchor[index + 1]) is not int
            or anchor[index + 1] <= 0
        ):
            raise ValueError("bound-fresh interface anchor is malformed")
        interface_size = anchor[index + 1]
        interface_tokens = anchor[index + 2 :]
        if (
            len(interface_tokens) != interface_size
            or any(type(token) is not str for token in interface_tokens)
        ):
            raise ValueError("bound-fresh interface anchor is malformed")
        index = len(anchor)
    if index != len(anchor):
        raise ValueError("bound-fresh alpha anchor is malformed")
    return (
        target.scope,
        _canonical_scalar(target.path[1]),
        tuple(_canonical_scalar(part) for part in anchor),
    )


def _validate_bound_fresh_identity_targets(
    targets: tuple[Locus, ...],
) -> None:
    keys = tuple(
        key
        for target in targets
        if (key := _bound_fresh_key(target)) is not None
    )
    if len(keys) != len(set(keys)):
        raise ValueError(
            "bound-fresh alpha identity requires unique "
            "namespace/local-key/anchor tuples"
        )


def _alpha_term(value: object) -> str:
    """Canonical term modulo bound-fresh binding-scope names only."""

    if type(value) is Locus and value.kind is LocusKind.FRESH:
        key = _bound_fresh_key(value)
        assert key is not None
        namespace, local_key, anchor = key
        return (
            "BoundFreshAlpha("
            f"namespace={_canonical_scalar(namespace)},"
            f"local_key={local_key},"
            "anchor=tuple[" + ",".join(anchor) + "]"
            ")"
        )
    if isinstance(value, (bool, int, Fraction, str)):
        return _canonical_scalar(value)
    if isinstance(value, Enum):
        return f"enum:{value.__class__.__name__}:{value.value}"
    if type(value) is tuple:
        return "tuple[" + ",".join(_alpha_term(item) for item in value) + "]"
    if value is None:
        return "none"
    dataclass_fields = getattr(value, "__dataclass_fields__", None)
    if dataclass_fields is not None:
        parts = tuple(
            f"{name}={_alpha_term(getattr(value, name))}"
            for name in dataclass_fields
        )
        return f"{value.__class__.__name__}(" + ",".join(parts) + ")"
    raise TypeError(f"{type(value).__name__} is not closed structural data")


def _configuration_semantic_term(
    configuration: FiniteConfiguration[object] | IntensionalConfiguration,
) -> str:
    law = configuration.contract.identity_law
    if law is ConfigurationIdentityLaw.EXACT:
        return _canonical_term(configuration)
    if law is ConfigurationIdentityLaw.BOUND_FRESH_ALPHA:
        if type(configuration) is FiniteConfiguration:
            entries = tuple(
                sorted(
                    (
                        "tuple["
                        + _alpha_term(target)
                        + ","
                        + _alpha_term(value)
                        + "]"
                    )
                    for target, value in configuration.entries
                )
            )
            return (
                "FiniteConfiguration("
                f"carrier={_alpha_term(configuration.carrier)},"
                "entries=tuple[" + ",".join(entries) + "],"
                f"structure={_alpha_term(configuration.structure)},"
                f"version={_alpha_term(configuration.version)}"
                ")"
            )
        return _alpha_term(configuration)
    raise AssertionError(f"unhandled configuration identity law {law.value}")


def configuration_equal(left: object, right: object) -> bool:
    """Compare snapshots under their explicitly declared identity law."""

    if type(left) is not type(right) or not isinstance(
        left, (FiniteConfiguration, IntensionalConfiguration)
    ):
        return False
    if left.contract.identity_law is not right.contract.identity_law:
        return False
    return _configuration_semantic_term(left) == _configuration_semantic_term(
        right
    )


def canonical_identity(value: object) -> str:
    """Derive a stable semantic identity from closed structural data."""

    payload = _canonical_term(value).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def semantic_equal(left: object, right: object) -> bool:
    """Exact structural equality with no representation or hash shortcut."""

    if isinstance(left, (FiniteConfiguration, IntensionalConfiguration)) or isinstance(
        right, (FiniteConfiguration, IntensionalConfiguration)
    ):
        return configuration_equal(left, right)
    return type(left) is type(right) and _canonical_term(left) == _canonical_term(right)


def _alpha_locus_reference_token(target: Locus) -> str:
    """Encode a parent/interface identity without a fresh binding-scope name."""

    key = _bound_fresh_key(target)
    if key is None:
        return canonical_identity(target)
    return canonical_identity(("bound-fresh-alpha-reference", key))


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
    alpha_anchor: tuple[ClosedScalar, ...] = ()
    if reference.parent is not None:
        alpha_anchor = (
            *alpha_anchor,
            "parent",
            _alpha_locus_reference_token(reference.parent),
        )
    if reference.interface:
        alpha_anchor = (
            *alpha_anchor,
            "interface",
            len(reference.interface),
            *(
                _alpha_locus_reference_token(target)
                for target in reference.interface
            ),
        )
    return Locus(
        LocusKind.FRESH,
        reference.namespace,
        (scope, reference.local_key, *alpha_anchor),
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
    "ConfigurationIdentityLaw",
    "FiniteConfiguration",
    "FreshReference",
    "FreshTemplate",
    "FreshTemplateKind",
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
    "configuration_equal",
    "continuous",
    "continuous_region",
    "configuration_identity",
    "coordinate",
    "current_support",
    "field_point",
    "fresh_children",
    "fresh_children_dynamic",
    "fresh_edges",
    "fresh_edges_dynamic",
    "fresh_reference",
    "graph_element",
    "grid_configuration",
    "grid_coordinates",
    "grid_loci",
    "history_configuration",
    "intersection",
    "intensional",
    "intensional_reference",
    "interface",
    "literal",
    "matched_interface",
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
    "difference",
    "differential",
    "dynamic_address",
    "resolve_region",
    "resolve_fresh_references",
    "resolve_relative_anchors",
    "resolve_selector",
    "selector_differential_germ",
    "selector_equal",
    "selector_field_restriction",
    "selector_history",
    "selector_incidence",
    "selector_literal",
    "selector_metric",
    "selector_path",
    "selector_reachable",
    "selector_tagged",
    "semantic_equal",
    "span",
    "span_region",
    "path_region",
    "union",
]
