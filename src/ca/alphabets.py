"""Closed schemas for semantic values and exact semantic equality."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from math import gcd
from typing import Generic, TypeAlias, TypeVar

from . import loci


V = TypeVar("V")
ExactScalar: TypeAlias = bool | int | Fraction | str


@dataclass(frozen=True)
class AlgebraicNumber:
    """One exact real root of a normalized integer polynomial.

    ``polynomial`` is written in descending degree order.  The rational
    interval must isolate exactly one real root.  ``root_index`` is the
    zero-based position of that root among all distinct real roots and is
    derived when omitted.
    """

    polynomial: tuple[int, ...]
    isolating_interval: tuple[Fraction, Fraction]
    root_index: int | None = None
    version: int = 1

    def __post_init__(self) -> None:
        if type(self.version) is not int or self.version != 1:
            raise ValueError(
                f"unsupported algebraic-number version {self.version!r}"
            )
        if type(self.polynomial) is not tuple or any(
            type(coefficient) is not int for coefficient in self.polynomial
        ):
            raise TypeError(
                "algebraic polynomial must be an immutable tuple of integers"
            )
        normalized = _normalize_integer_polynomial(self.polynomial)
        if normalized != self.polynomial:
            object.__setattr__(self, "polynomial", normalized)
        interval = self.isolating_interval
        if (
            type(interval) is not tuple
            or len(interval) != 2
            or any(type(endpoint) is not Fraction for endpoint in interval)
        ):
            raise TypeError(
                "algebraic isolating interval needs two exact Fractions"
            )
        lower, upper = interval
        if lower >= upper:
            raise ValueError(
                "algebraic isolating interval endpoints must be increasing"
            )
        sequence = _sturm_sequence(normalized)
        if _polynomial_at(normalized, lower) == 0:
            raise ValueError("algebraic lower endpoint cannot be a root")
        if _polynomial_at(normalized, upper) == 0:
            raise ValueError("algebraic upper endpoint cannot be a root")
        root_count = _sturm_variations_at(sequence, lower) - (
            _sturm_variations_at(sequence, upper)
        )
        if root_count != 1:
            raise ValueError(
                "algebraic interval must isolate exactly one distinct real root"
            )
        derived_index = _sturm_variations_at_infinity(
            sequence, negative=True
        ) - _sturm_variations_at(sequence, lower)
        if self.root_index is None:
            object.__setattr__(self, "root_index", derived_index)
        elif type(self.root_index) is not int or self.root_index < 0:
            raise ValueError("algebraic root_index must be a nonnegative integer")
        elif self.root_index != derived_index:
            raise ValueError(
                "algebraic root_index disagrees with the isolating interval"
            )


ExactReal: TypeAlias = int | Fraction | AlgebraicNumber


@dataclass(frozen=True)
class ExactComplex:
    """An exact complex value with rational or algebraic components."""

    real: ExactReal
    imaginary: ExactReal
    version: int = 1

    def __post_init__(self) -> None:
        if type(self.version) is not int or self.version != 1:
            raise ValueError(
                f"unsupported exact-complex version {self.version!r}"
            )
        if type(self.real) not in (int, Fraction, AlgebraicNumber) or type(
            self.imaginary
        ) not in (int, Fraction, AlgebraicNumber):
            raise TypeError(
                "exact-complex components must be integers, Fractions, "
                "or AlgebraicNumbers"
            )


@dataclass(frozen=True)
class StructuralReference:
    """A semantic value that names an existing or Rule-local fresh locus."""

    reference: loci.Locus | loci.FreshReference
    version: int = 1

    def __post_init__(self) -> None:
        if type(self.version) is not int or self.version != 1:
            raise ValueError(
                f"unsupported structural-reference version {self.version!r}"
            )
        if type(self.reference) not in (loci.Locus, loci.FreshReference):
            raise TypeError(
                "structural reference must contain a Locus or FreshReference"
            )

    @property
    def is_bound(self) -> bool:
        return type(self.reference) is loci.Locus


Polynomial: TypeAlias = tuple[Fraction, ...]


def _trim_polynomial(polynomial: Polynomial) -> Polynomial:
    index = 0
    while index < len(polynomial) - 1 and polynomial[index] == 0:
        index += 1
    return polynomial[index:]


def _normalize_integer_polynomial(
    polynomial: tuple[int, ...],
) -> tuple[int, ...]:
    if len(polynomial) < 2:
        raise ValueError("algebraic polynomial must have positive degree")
    index = 0
    while index < len(polynomial) and polynomial[index] == 0:
        index += 1
    if index == len(polynomial) or len(polynomial) - index < 2:
        raise ValueError("algebraic polynomial must have positive degree")
    coefficients = polynomial[index:]
    content = 0
    for coefficient in coefficients:
        content = gcd(content, abs(coefficient))
    assert content > 0
    coefficients = tuple(coefficient // content for coefficient in coefficients)
    if coefficients[0] < 0:
        coefficients = tuple(-coefficient for coefficient in coefficients)
    return coefficients


def _polynomial_at(
    polynomial: tuple[int, ...] | Polynomial,
    point: Fraction,
) -> Fraction:
    value = Fraction(0)
    for coefficient in polynomial:
        value = value * point + coefficient
    return value


def _polynomial_derivative(polynomial: Polynomial) -> Polynomial:
    degree = len(polynomial) - 1
    return tuple(
        coefficient * (degree - index)
        for index, coefficient in enumerate(polynomial[:-1])
    )


def _polynomial_remainder(dividend: Polynomial, divisor: Polynomial) -> Polynomial:
    dividend = _trim_polynomial(dividend)
    divisor = _trim_polynomial(divisor)
    if len(divisor) == 1 and divisor[0] == 0:
        raise ZeroDivisionError("polynomial division by zero")
    remainder = list(dividend)
    while len(remainder) >= len(divisor) and any(remainder):
        factor = remainder[0] / divisor[0]
        for index, coefficient in enumerate(divisor):
            remainder[index] -= factor * coefficient
        remainder = list(_trim_polynomial(tuple(remainder)))
        if len(remainder) == 1 and remainder[0] == 0:
            break
    return _trim_polynomial(tuple(remainder))


def _sturm_sequence(polynomial: tuple[int, ...]) -> tuple[Polynomial, ...]:
    first = tuple(Fraction(coefficient) for coefficient in polynomial)
    second = _trim_polynomial(_polynomial_derivative(first))
    sequence = [first, second]
    while not (len(sequence[-1]) == 1 and sequence[-1][0] == 0):
        remainder = _polynomial_remainder(sequence[-2], sequence[-1])
        if len(remainder) == 1 and remainder[0] == 0:
            break
        sequence.append(tuple(-coefficient for coefficient in remainder))
    return tuple(sequence)


def _sign(value: Fraction) -> int:
    return (value > 0) - (value < 0)


def _sign_variations(signs: tuple[int, ...]) -> int:
    nonzero = tuple(sign for sign in signs if sign)
    return sum(left != right for left, right in zip(nonzero, nonzero[1:]))


def _sturm_variations_at(
    sequence: tuple[Polynomial, ...],
    point: Fraction,
) -> int:
    return _sign_variations(
        tuple(_sign(_polynomial_at(polynomial, point)) for polynomial in sequence)
    )


def _sturm_variations_at_infinity(
    sequence: tuple[Polynomial, ...],
    *,
    negative: bool,
) -> int:
    signs = []
    for polynomial in sequence:
        sign = _sign(polynomial[0])
        degree = len(polynomial) - 1
        if negative and degree % 2:
            sign = -sign
        signs.append(sign)
    return _sign_variations(tuple(signs))


class ValueKind(Enum):
    TAG = "tag"
    PRODUCT = "product"
    RECORD = "record"
    WORD = "word"
    MAP = "map"
    GRAPH = "graph"
    FIELD = "field"
    INSTRUCTION = "instruction"
    PATTERN = "pattern"
    EQUATION = "equation"
    DISTRIBUTION = "distribution"
    SYMBOLIC = "symbolic"


_MAP_ENTRY_TAG = "entry"


@dataclass(frozen=True)
class ValueNode:
    """One closed composite value."""

    kind: ValueKind
    tag: str
    items: tuple["SemanticValue", ...] = ()
    fields: tuple[tuple[str, "SemanticValue"], ...] = ()
    version: int = 1

    def __post_init__(self) -> None:
        if type(self.version) is not int or self.version != 1:
            raise ValueError(f"unsupported value-node version {self.version}")
        if not isinstance(self.kind, ValueKind):
            raise TypeError("value-node kind is not recognized")
        if not isinstance(self.tag, str) or not self.tag:
            raise ValueError("value-node tag cannot be empty")
        if type(self.items) is not tuple or type(self.fields) is not tuple:
            raise TypeError("value-node collections must be immutable tuples")
        if any(not _is_semantic_value(item) for item in self.items):
            raise TypeError("value-node items contain an opaque value")
        if any(
            type(field) is not tuple
            or len(field) != 2
            or not isinstance(field[0], str)
            or not field[0]
            or not _is_semantic_value(field[1])
            for field in self.fields
        ):
            raise TypeError("value-node fields contain an opaque value")
        names = tuple(name for name, _ in self.fields)
        if len(names) != len(set(names)):
            raise ValueError("value-node fields must have unique names")
        if self.fields:
            ordered = tuple(sorted(self.fields, key=lambda item: item[0]))
            if ordered != self.fields:
                object.__setattr__(self, "fields", ordered)
        if self.kind is ValueKind.TAG and (
            len(self.items) != 1 or self.fields
        ):
            raise ValueError("tag values need exactly one payload item")
        if self.kind in (ValueKind.PRODUCT, ValueKind.WORD) and self.fields:
            raise ValueError(f"{self.kind.value} values cannot carry named fields")
        if self.kind is ValueKind.RECORD and self.items:
            raise ValueError("record values cannot carry positional items")
        if self.kind is ValueKind.MAP:
            if self.fields:
                raise ValueError(
                    "map values use explicit semantic-key entry items, not fields"
                )
            if any(
                type(entry) is not ValueNode
                or entry.kind is not ValueKind.PRODUCT
                or entry.tag != _MAP_ENTRY_TAG
                or len(entry.items) != 2
                or entry.fields
                for entry in self.items
            ):
                raise ValueError(
                    "map values need explicit entry products with key/value items"
                )
            keys = tuple(_value_key(entry.items[0]) for entry in self.items)
            if len(keys) != len(set(keys)):
                raise ValueError("map values require semantically unique keys")
            ordered_items = tuple(
                sorted(self.items, key=lambda entry: _value_key(entry.items[0]))
            )
            if ordered_items != self.items:
                object.__setattr__(self, "items", ordered_items)


class RepresentedNumberProfile(Enum):
    IEEE754_BINARY32 = "ieee754-binary32"
    IEEE754_BINARY64 = "ieee754-binary64"
    FIXED_POINT = "fixed-point"
    DECIMAL = "decimal"
    INTERVAL = "interval"


@dataclass(frozen=True)
class RepresentedNumber:
    """An explicit represented number; it never claims exact-real identity."""

    profile: RepresentedNumberProfile
    representation: int | Fraction | str | tuple[Fraction, Fraction]
    version: int = 1

    def __post_init__(self) -> None:
        if type(self.version) is not int or self.version != 1:
            raise ValueError(f"unsupported represented-number version {self.version}")
        if not isinstance(self.profile, RepresentedNumberProfile):
            raise TypeError("represented-number profile is not recognized")
        value = self.representation
        if self.profile in (
            RepresentedNumberProfile.IEEE754_BINARY32,
            RepresentedNumberProfile.IEEE754_BINARY64,
        ):
            if isinstance(value, bool) or not isinstance(value, (int, str)):
                raise TypeError(
                    "IEEE represented numbers require raw integer bits or a bit string"
                )
            if isinstance(value, int):
                width = (
                    32
                    if self.profile
                    is RepresentedNumberProfile.IEEE754_BINARY32
                    else 64
                )
                if not 0 <= value < 1 << width:
                    raise ValueError("IEEE raw bits exceed the declared width")
            elif not value:
                raise ValueError("IEEE bit string cannot be empty")
        elif self.profile is RepresentedNumberProfile.FIXED_POINT:
            if isinstance(value, bool) or not isinstance(
                value, (int, Fraction, str)
            ):
                raise TypeError(
                    "fixed-point representation must be integer, Fraction, or text"
                )
        elif self.profile is RepresentedNumberProfile.DECIMAL:
            if not isinstance(value, str) or not value:
                raise TypeError("decimal representation must be nonempty text")
        elif self.profile is RepresentedNumberProfile.INTERVAL:
            if (
                type(value) is not tuple
                or len(value) != 2
                or any(type(item) is not Fraction for item in value)
            ):
                raise TypeError("represented interval needs two exact Fractions")
            if value[0] > value[1]:
                raise ValueError("represented interval endpoints are reversed")


SemanticValue: TypeAlias = (
    ExactScalar
    | AlgebraicNumber
    | ExactComplex
    | StructuralReference
    | RepresentedNumber
    | ValueNode
)


def _is_semantic_value(value: object) -> bool:
    return type(value) in (
        bool,
        int,
        Fraction,
        str,
        AlgebraicNumber,
        ExactComplex,
        StructuralReference,
        RepresentedNumber,
        ValueNode,
    )


def _require_node_kind(
    value: SemanticValue,
    kind: ValueKind,
) -> ValueNode:
    if type(value) is not ValueNode or value.kind is not kind:
        raise TypeError(f"expected a {kind.value} ValueNode")
    return value


def _structured_value(
    kind: ValueKind,
    tag: str,
    *,
    items: tuple[SemanticValue, ...],
    fields: tuple[tuple[str, SemanticValue], ...],
) -> ValueNode:
    """Build one canonically ordered closed structural value."""

    node = ValueNode(kind, tag, items=items, fields=fields)
    ordered_fields = tuple(sorted(node.fields, key=lambda item: item[0]))
    if ordered_fields == node.fields:
        return node
    return ValueNode(kind, tag, items=node.items, fields=ordered_fields)


def tag_value(name: str, payload: SemanticValue) -> ValueNode:
    """Construct one tagged union value with exactly one closed payload."""

    return ValueNode(ValueKind.TAG, name, items=(payload,))


def tag_payload(value: SemanticValue) -> SemanticValue:
    """Return the sole payload of a tagged value."""

    return _require_node_kind(value, ValueKind.TAG).items[0]


def product_value(
    items: tuple[SemanticValue, ...],
    *,
    tag: str = "product",
) -> ValueNode:
    """Construct a nonempty ordered product value."""

    if type(items) is not tuple:
        raise TypeError("product value items must be an immutable tuple")
    if not items:
        raise ValueError("product value requires at least one item")
    return ValueNode(ValueKind.PRODUCT, tag, items=items)


def product_items(value: SemanticValue) -> tuple[SemanticValue, ...]:
    """Return the ordered components of a product value."""

    return _require_node_kind(value, ValueKind.PRODUCT).items


def record_value(
    fields: tuple[tuple[str, SemanticValue], ...],
    *,
    tag: str = "record",
) -> ValueNode:
    """Construct a nonempty canonical string-field record value."""

    if type(fields) is not tuple:
        raise TypeError("record value fields must be an immutable tuple")
    if not fields:
        raise ValueError("record value requires at least one field")
    return ValueNode(ValueKind.RECORD, tag, fields=fields)


def record_fields(
    value: SemanticValue,
) -> tuple[tuple[str, SemanticValue], ...]:
    """Return the canonical named fields of a record value."""

    return _require_node_kind(value, ValueKind.RECORD).fields


def node_get(value: SemanticValue, name: str) -> SemanticValue:
    """Read one named field from any structural ValueNode."""

    if type(value) is not ValueNode:
        raise TypeError("named field access needs a ValueNode")
    if type(name) is not str or not name:
        raise ValueError("field name must be a nonempty string")
    for field_name, field_value in value.fields:
        if field_name == name:
            return field_value
    raise KeyError(name)


def record_get(value: SemanticValue, name: str) -> SemanticValue:
    """Read one named field from a record value."""

    return node_get(_require_node_kind(value, ValueKind.RECORD), name)


def word_value(
    items: tuple[SemanticValue, ...],
    *,
    tag: str = "word",
) -> ValueNode:
    """Construct an ordered, possibly empty, word value."""

    if type(items) is not tuple:
        raise TypeError("word value items must be an immutable tuple")
    return ValueNode(ValueKind.WORD, tag, items=items)


def word_items(value: SemanticValue) -> tuple[SemanticValue, ...]:
    """Return the ordered symbols of a word value."""

    return _require_node_kind(value, ValueKind.WORD).items


def map_entry_value(
    key: SemanticValue,
    value: SemanticValue,
) -> ValueNode:
    """Construct one explicit semantic-key association entry."""

    return ValueNode(
        ValueKind.PRODUCT,
        _MAP_ENTRY_TAG,
        items=(key, value),
    )


def map_value(
    entries: tuple[ValueNode, ...],
    *,
    tag: str = "map",
) -> ValueNode:
    """Construct a canonical map from explicit semantic-key entry products."""

    if type(entries) is not tuple:
        raise TypeError("map value entries must be an immutable tuple")
    return ValueNode(ValueKind.MAP, tag, items=entries)


def map_entries(
    value: SemanticValue,
) -> tuple[tuple[SemanticValue, SemanticValue], ...]:
    """Return canonical semantic-key/value pairs from a map value."""

    node = _require_node_kind(value, ValueKind.MAP)
    return tuple((entry.items[0], entry.items[1]) for entry in node.items)


def map_get(value: SemanticValue, key: SemanticValue) -> SemanticValue:
    """Look up one semantic key using exact semantic equality."""

    if not _is_semantic_value(key):
        raise TypeError("map lookup key must be a closed semantic value")
    for entry_key, entry_value in map_entries(value):
        if semantic_equal(entry_key, key):
            return entry_value
    raise KeyError(_value_key(key))


def node_items(value: SemanticValue) -> tuple[SemanticValue, ...]:
    """Return positional items from any structural ValueNode."""

    if type(value) is not ValueNode:
        raise TypeError("positional item access needs a ValueNode")
    return value.items


def node_fields(
    value: SemanticValue,
) -> tuple[tuple[str, SemanticValue], ...]:
    """Return named fields from any structural ValueNode."""

    if type(value) is not ValueNode:
        raise TypeError("named field access needs a ValueNode")
    return value.fields


def pattern_value(
    tag: str,
    *,
    items: tuple[SemanticValue, ...] = (),
    fields: tuple[tuple[str, SemanticValue], ...] = (),
) -> ValueNode:
    """Construct one closed pattern AST node."""

    return _structured_value(
        ValueKind.PATTERN,
        tag,
        items=items,
        fields=fields,
    )


def symbolic_value(
    tag: str,
    *,
    items: tuple[SemanticValue, ...] = (),
    fields: tuple[tuple[str, SemanticValue], ...] = (),
) -> ValueNode:
    """Construct one closed symbolic expression node."""

    return _structured_value(
        ValueKind.SYMBOLIC,
        tag,
        items=items,
        fields=fields,
    )


def field_value(
    tag: str,
    *,
    items: tuple[SemanticValue, ...] = (),
    fields: tuple[tuple[str, SemanticValue], ...] = (),
) -> ValueNode:
    """Construct one closed field-state value."""

    return _structured_value(
        ValueKind.FIELD,
        tag,
        items=items,
        fields=fields,
    )


StructuralBinding: TypeAlias = tuple[loci.FreshReference, loci.Locus]


def bind_structural_references(
    value: SemanticValue,
    bindings: tuple[StructuralBinding, ...],
) -> SemanticValue:
    """Recursively replace every fresh value reference with its bound locus.

    Bindings are immutable semantic pairs.  Missing references, duplicate
    local references, and target collisions fail closed.
    """

    if not _is_semantic_value(value):
        raise TypeError("structural-reference binding needs a semantic value")
    if type(bindings) is not tuple or any(
        type(binding) is not tuple
        or len(binding) != 2
        or type(binding[0]) is not loci.FreshReference
        or type(binding[1]) is not loci.Locus
        for binding in bindings
    ):
        raise TypeError(
            "bindings must be immutable (FreshReference, Locus) pairs"
        )
    fresh = tuple(reference for reference, _ in bindings)
    targets = tuple(target for _, target in bindings)
    if len(set(fresh)) != len(fresh):
        raise ValueError("structural bindings contain duplicate fresh references")
    if len(set(targets)) != len(targets):
        raise ValueError("structural bindings contain colliding bound loci")

    if type(value) is StructuralReference:
        reference = value.reference
        if type(reference) is loci.Locus:
            return value
        for fresh_reference, target in bindings:
            if reference == fresh_reference:
                return StructuralReference(target)
        raise ValueError("structural value contains an unbound fresh reference")
    if type(value) is ValueNode:
        return ValueNode(
            value.kind,
            value.tag,
            items=tuple(
                bind_structural_references(item, bindings)
                for item in value.items
            ),
            fields=tuple(
                (name, bind_structural_references(item, bindings))
                for name, item in value.fields
            ),
            version=value.version,
        )
    return value


class AlphabetKind(Enum):
    ENUM = "enum"
    ORDERED = "ordered"
    NATURALS = "naturals"
    INTEGERS = "integers"
    RATIONALS = "rationals"
    RATIONAL_INTERVAL = "rational-interval"
    MODULAR = "modular"
    ALGEBRAIC = "algebraic"
    EXACT_COMPLEX = "exact-complex"
    REPRESENTED_NUMBER = "represented-number"
    TAG = "tag"
    UNION = "union"
    PRODUCT = "product"
    RECORD = "record"
    WORD = "word"
    MAP = "map"
    GRAPH = "graph"
    FIELD = "field"
    INSTRUCTION = "instruction"
    PATTERN = "pattern"
    EQUATION = "equation"
    DISTRIBUTION = "distribution"
    SYMBOLIC = "symbolic"
    STRUCTURAL_REFERENCE = "structural-reference"
    REFINEMENT = "refinement"


class ValueProfile(Enum):
    BOOLEAN = "boolean"
    INTEGER = "integer"
    RATIONAL = "rational"
    ALGEBRAIC = "algebraic"
    COMPLEX = "complex"
    REPRESENTED = "represented"
    SYMBOLIC = "symbolic"
    STRUCTURAL = "structural"
    EXACT = "exact"


@dataclass(frozen=True)
class AlphabetDescriptor:
    """One versioned schema AST node."""

    kind: AlphabetKind
    values: tuple[SemanticValue, ...] = ()
    scalars: tuple[tuple[str, ExactScalar], ...] = ()
    children: tuple["AlphabetDescriptor", ...] = ()
    fields: tuple[tuple[str, "AlphabetDescriptor"], ...] = ()
    represented_profile: RepresentedNumberProfile | None = None
    version: int = 1

    def __post_init__(self) -> None:
        if type(self.version) is not int or self.version != 1:
            raise ValueError(f"unsupported alphabet version {self.version}")
        if not isinstance(self.kind, AlphabetKind):
            raise TypeError("alphabet kind is not recognized")
        if any(
            type(value) is not tuple
            for value in (self.values, self.scalars, self.children, self.fields)
        ):
            raise TypeError("alphabet collections must be immutable tuples")
        if any(not _is_semantic_value(value) for value in self.values):
            raise TypeError("alphabet contains an opaque semantic value")
        if any(
            type(item) is not tuple
            or len(item) != 2
            or not isinstance(item[0], str)
            or not item[0]
            or type(item[1]) not in (bool, int, Fraction, str)
            for item in self.scalars
        ):
            raise TypeError("alphabet scalar parameters are not closed")
        if any(
            type(child) is not AlphabetDescriptor
            for child in self.children
        ):
            raise TypeError("alphabet children must be AlphabetDescriptor values")
        if any(
            type(item) is not tuple
            or len(item) != 2
            or not isinstance(item[0], str)
            or not item[0]
            or type(item[1]) is not AlphabetDescriptor
            for item in self.fields
        ):
            raise TypeError("alphabet fields must contain closed descriptors")
        scalar_names = tuple(name for name, _ in self.scalars)
        field_names = tuple(name for name, _ in self.fields)
        if len(scalar_names) != len(set(scalar_names)):
            raise ValueError("alphabet scalar parameters must have unique names")
        if len(field_names) != len(set(field_names)):
            raise ValueError("alphabet fields must have unique names")
        if self.fields:
            ordered_fields = tuple(sorted(self.fields, key=lambda item: item[0]))
            if ordered_fields != self.fields:
                object.__setattr__(self, "fields", ordered_fields)
        if self.kind in (AlphabetKind.ENUM, AlphabetKind.ORDERED, AlphabetKind.SYMBOLIC):
            if not self.values:
                raise ValueError(f"{self.kind.value} alphabet cannot be empty")
            keys = tuple(_value_key(value) for value in self.values)
            if len(keys) != len(set(keys)):
                raise ValueError("alphabet values must be semantically unique")
        if self.kind is AlphabetKind.ENUM:
            ordered_values = tuple(sorted(self.values, key=_value_key))
            if tuple(_value_key(value) for value in ordered_values) != tuple(
                _value_key(value) for value in self.values
            ):
                object.__setattr__(self, "values", ordered_values)
        if self.kind in (AlphabetKind.UNION,):
            ordered_children = tuple(sorted(self.children, key=_descriptor_key))
            if tuple(_descriptor_key(child) for child in ordered_children) != tuple(
                _descriptor_key(child) for child in self.children
            ):
                object.__setattr__(self, "children", ordered_children)
        if self.kind is AlphabetKind.MODULAR:
            modulus = _scalar_parameter(self, "modulus")
            if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus <= 0:
                raise ValueError("modular alphabet needs a positive integer modulus")
        if self.kind is AlphabetKind.REPRESENTED_NUMBER and self.represented_profile is None:
            raise ValueError("represented-number alphabet needs an explicit profile")
        _validate_descriptor_shape(self)


@dataclass(frozen=True)
class Alphabet(Generic[V]):
    """One closed schema for semantic values."""

    descriptor: AlphabetDescriptor

    def __post_init__(self) -> None:
        if type(self.descriptor) is not AlphabetDescriptor:
            raise TypeError("Alphabet descriptor is not recognized")

    @property
    def value_profile(self) -> ValueProfile:
        return _profile(self.descriptor)

    def contains(self, value: SemanticValue) -> bool:
        return _contains(self.descriptor, value)

    def require(self, value: SemanticValue) -> None:
        if not self.contains(value):
            raise ValueError(
                f"value {value!r} does not conform to {self.descriptor.kind.value}"
            )

    def equal(self, left: SemanticValue, right: SemanticValue) -> bool:
        self.require(left)
        self.require(right)
        return semantic_equal(left, right)


class RepresentationProfile(Enum):
    """The semantic strength claimed by a finite representation map."""

    EXACT = "exact"
    LOSSY = "lossy"
    APPROXIMATE = "approximate"


@dataclass(frozen=True)
class RepresentationPair:
    """One source-to-target atom in a closed finite representation map."""

    source: SemanticValue
    target: SemanticValue
    version: int = 1

    def __post_init__(self) -> None:
        if type(self.version) is not int or self.version != 1:
            raise ValueError(
                f"unsupported representation-pair version {self.version!r}"
            )
        if not _is_semantic_value(self.source) or not _is_semantic_value(
            self.target
        ):
            raise TypeError("representation pairs require closed semantic values")


@dataclass(frozen=True)
class RepresentationRelation:
    """A validated finite map with explicit image and inverse evidence.

    The source schema must enumerate its complete finite domain.  Exact maps
    are injective and carry their complete inverse-on-image graph.  Lossy and
    approximate maps cannot expose that exact inverse and instead require
    explicit qualification data.
    """

    source_schema: AlphabetDescriptor
    target_schema: AlphabetDescriptor
    profile: RepresentationProfile
    relation: tuple[RepresentationPair, ...]
    image_evidence: tuple[SemanticValue, ...]
    inverse_evidence: tuple[RepresentationPair, ...] = ()
    qualification: tuple[tuple[str, ExactScalar], ...] = ()
    version: int = 1

    def __post_init__(self) -> None:
        if type(self.version) is not int or self.version != 1:
            raise ValueError(
                f"unsupported representation-relation version {self.version!r}"
            )
        if type(self.source_schema) is not AlphabetDescriptor or type(
            self.target_schema
        ) is not AlphabetDescriptor:
            raise TypeError("representation schemas must be AlphabetDescriptors")
        if type(self.profile) is not RepresentationProfile:
            raise TypeError("representation profile is not recognized")
        if type(self.relation) is not tuple or any(
            type(pair) is not RepresentationPair for pair in self.relation
        ):
            raise TypeError(
                "representation relation must be an immutable tuple of pairs"
            )
        if not self.relation:
            raise ValueError("representation relation cannot be empty")
        if type(self.image_evidence) is not tuple or any(
            not _is_semantic_value(value) for value in self.image_evidence
        ):
            raise TypeError(
                "representation image evidence must contain semantic values"
            )
        if type(self.inverse_evidence) is not tuple or any(
            type(pair) is not RepresentationPair
            for pair in self.inverse_evidence
        ):
            raise TypeError(
                "representation inverse evidence must be an immutable pair tuple"
            )
        if type(self.qualification) is not tuple or any(
            type(item) is not tuple
            or len(item) != 2
            or type(item[0]) is not str
            or not item[0]
            or type(item[1]) not in (bool, int, Fraction, str)
            for item in self.qualification
        ):
            raise TypeError(
                "representation qualification must contain closed named scalars"
            )
        qualification_names = tuple(name for name, _ in self.qualification)
        if len(set(qualification_names)) != len(qualification_names):
            raise ValueError("representation qualification names must be unique")
        object.__setattr__(
            self,
            "qualification",
            tuple(sorted(self.qualification, key=lambda item: item[0])),
        )

        finite_kinds = (
            AlphabetKind.ENUM,
            AlphabetKind.ORDERED,
            AlphabetKind.SYMBOLIC,
        )
        if self.source_schema.kind not in finite_kinds:
            raise ValueError(
                "finite representation relation needs an enumerable source schema"
            )
        for pair in self.relation:
            if not _contains(self.source_schema, pair.source):
                raise ValueError(
                    "representation relation contains a value outside its "
                    "source schema"
                )
            if not _contains(self.target_schema, pair.target):
                raise ValueError(
                    "representation relation contains a value outside its "
                    "target schema"
                )

        source_keys = tuple(_value_key(pair.source) for pair in self.relation)
        if len(source_keys) != len(set(source_keys)):
            raise ValueError(
                "representation relation must map each source exactly once"
            )
        expected_sources = {
            _value_key(value) for value in self.source_schema.values
        }
        if set(source_keys) != expected_sources:
            raise ValueError(
                "representation relation does not cover its finite source schema"
            )
        ordered_relation = tuple(
            sorted(self.relation, key=lambda pair: _value_key(pair.source))
        )
        object.__setattr__(self, "relation", ordered_relation)

        image_keys = tuple(_value_key(value) for value in self.image_evidence)
        if len(image_keys) != len(set(image_keys)):
            raise ValueError("representation image evidence contains duplicates")
        expected_image_by_key = {
            _value_key(pair.target): pair.target for pair in ordered_relation
        }
        if set(image_keys) != set(expected_image_by_key):
            raise ValueError(
                "representation image evidence disagrees with the relation"
            )
        object.__setattr__(
            self,
            "image_evidence",
            tuple(
                expected_image_by_key[key]
                for key in sorted(expected_image_by_key)
            ),
        )

        if self.profile is RepresentationProfile.EXACT:
            target_keys = tuple(
                _value_key(pair.target) for pair in ordered_relation
            )
            if len(target_keys) != len(set(target_keys)):
                raise ValueError("exact representation relation must be injective")
            expected_inverse = {
                (_value_key(pair.target), _value_key(pair.source))
                for pair in ordered_relation
            }
            actual_inverse = {
                (_value_key(pair.source), _value_key(pair.target))
                for pair in self.inverse_evidence
            }
            if (
                not self.inverse_evidence
                or len(actual_inverse) != len(self.inverse_evidence)
                or actual_inverse != expected_inverse
            ):
                raise ValueError(
                    "exact representation needs complete inverse-on-image evidence"
                )
            if self.qualification:
                raise ValueError(
                    "exact representation cannot carry lossy/approximate "
                    "qualification"
                )
            object.__setattr__(
                self,
                "inverse_evidence",
                tuple(
                    sorted(
                        self.inverse_evidence,
                        key=lambda pair: _value_key(pair.source),
                    )
                ),
            )
        else:
            if self.inverse_evidence:
                raise ValueError(
                    "lossy/approximate representation cannot claim an exact "
                    "inverse"
                )
            if not self.qualification:
                raise ValueError(
                    "lossy/approximate representation needs explicit "
                    "qualification"
                )
            if (
                self.profile is RepresentationProfile.APPROXIMATE
                and not {
                    "error-bound",
                    "error-model",
                }.intersection(qualification_names)
            ):
                raise ValueError(
                    "approximate representation needs error-bound or "
                    "error-model evidence"
                )

    @property
    def mapping(self) -> tuple[RepresentationPair, ...]:
        return self.relation

    def forward(self, value: SemanticValue) -> SemanticValue:
        if not _contains(self.source_schema, value):
            raise ValueError("value is outside the representation source schema")
        for pair in self.relation:
            if semantic_equal(pair.source, value):
                return pair.target
        raise ValueError("value is outside the declared finite relation")

    def inverse(self, value: SemanticValue) -> SemanticValue:
        if self.profile is not RepresentationProfile.EXACT:
            raise ValueError(
                "only exact representations have an inverse-on-image"
            )
        for pair in self.inverse_evidence:
            if semantic_equal(pair.source, value):
                return pair.target
        raise ValueError("value is outside the declared representation image")


def _scalar_parameter(
    descriptor: AlphabetDescriptor,
    name: str,
) -> ExactScalar | None:
    for parameter_name, value in descriptor.scalars:
        if parameter_name == name:
            return value
    return None


def enum(values: tuple[SemanticValue, ...]) -> Alphabet[SemanticValue]:
    return Alphabet(AlphabetDescriptor(AlphabetKind.ENUM, values=values))


def ordered(values: tuple[SemanticValue, ...]) -> Alphabet[SemanticValue]:
    return Alphabet(AlphabetDescriptor(AlphabetKind.ORDERED, values=values))


def naturals() -> Alphabet[int]:
    return Alphabet(AlphabetDescriptor(AlphabetKind.NATURALS))


def integers(
    *,
    minimum: int | None = None,
    maximum: int | None = None,
) -> Alphabet[int]:
    if minimum is not None and (
        isinstance(minimum, bool) or not isinstance(minimum, int)
    ):
        raise TypeError("minimum must be an integer or None")
    if maximum is not None and (
        isinstance(maximum, bool) or not isinstance(maximum, int)
    ):
        raise TypeError("maximum must be an integer or None")
    scalars: list[tuple[str, ExactScalar]] = []
    if minimum is not None:
        scalars.append(("minimum", int(minimum)))
    if maximum is not None:
        scalars.append(("maximum", int(maximum)))
    if minimum is not None and maximum is not None and minimum > maximum:
        raise ValueError("minimum cannot exceed maximum")
    return Alphabet(
        AlphabetDescriptor(AlphabetKind.INTEGERS, scalars=tuple(scalars))
    )


def rationals() -> Alphabet[Fraction]:
    return Alphabet(AlphabetDescriptor(AlphabetKind.RATIONALS))


def rational_interval(
    lower: Fraction,
    upper: Fraction,
    *,
    lower_closed: bool = True,
    upper_closed: bool = True,
) -> Alphabet[Fraction]:
    """Construct one nonempty exact interval of rational values."""

    if type(lower) is not Fraction or type(upper) is not Fraction:
        raise TypeError("rational-interval bounds must be exact Fractions")
    if type(lower_closed) is not bool or type(upper_closed) is not bool:
        raise TypeError("rational-interval endpoint flags must be booleans")
    if lower > upper:
        raise ValueError("rational-interval lower bound cannot exceed its upper")
    if lower == upper and not (lower_closed and upper_closed):
        raise ValueError("rational interval cannot be empty")
    return Alphabet(
        AlphabetDescriptor(
            AlphabetKind.RATIONAL_INTERVAL,
            scalars=(
                ("lower", lower),
                ("upper", upper),
                ("lower_closed", lower_closed),
                ("upper_closed", upper_closed),
            ),
        )
    )


def algebraics() -> Alphabet[AlgebraicNumber]:
    return Alphabet(AlphabetDescriptor(AlphabetKind.ALGEBRAIC))


def exact_complexes(
    components: Alphabet[SemanticValue] | None = None,
) -> Alphabet[ExactComplex]:
    """Construct exact complex values over one exact component schema."""

    if components is None:
        components = union(
            (
                rationals(),  # type: ignore[arg-type]
                algebraics(),  # type: ignore[arg-type]
            )
        )
    if type(components) is not Alphabet:
        raise TypeError("exact-complex components must be an Alphabet")
    if components.value_profile is ValueProfile.REPRESENTED:
        raise ValueError(
            "exact-complex components cannot use a represented-number schema"
        )
    return Alphabet(
        AlphabetDescriptor(
            AlphabetKind.EXACT_COMPLEX,
            children=(components.descriptor,),
        )
    )


def modular(modulus: int) -> Alphabet[int]:
    if isinstance(modulus, bool) or not isinstance(modulus, int):
        raise TypeError("modulus must be an integer")
    return Alphabet(
        AlphabetDescriptor(
            AlphabetKind.MODULAR,
            scalars=(("modulus", int(modulus)),),
        )
    )


def represented_numeric(
    profile: RepresentedNumberProfile,
) -> Alphabet[RepresentedNumber]:
    return Alphabet(
        AlphabetDescriptor(
            AlphabetKind.REPRESENTED_NUMBER,
            represented_profile=profile,
        )
    )


def structural_references() -> Alphabet[StructuralReference]:
    return Alphabet(AlphabetDescriptor(AlphabetKind.STRUCTURAL_REFERENCE))


def tag(
    name: str,
    payload: Alphabet[SemanticValue],
) -> Alphabet[ValueNode]:
    return Alphabet(
        AlphabetDescriptor(
            AlphabetKind.TAG,
            scalars=(("name", name),),
            children=(payload.descriptor,),
        )
    )


def union(
    parts: tuple[Alphabet[SemanticValue], ...],
) -> Alphabet[SemanticValue]:
    if not parts:
        raise ValueError("alphabet union requires parts")
    return Alphabet(
        AlphabetDescriptor(
            AlphabetKind.UNION,
            children=tuple(part.descriptor for part in parts),
        )
    )


def product(
    parts: tuple[Alphabet[SemanticValue], ...],
) -> Alphabet[ValueNode]:
    if not parts:
        raise ValueError("alphabet product requires parts")
    return Alphabet(
        AlphabetDescriptor(
            AlphabetKind.PRODUCT,
            children=tuple(part.descriptor for part in parts),
        )
    )


def record(
    fields: tuple[tuple[str, Alphabet[SemanticValue]], ...],
) -> Alphabet[ValueNode]:
    if not fields:
        raise ValueError("record alphabet requires fields")
    return Alphabet(
        AlphabetDescriptor(
            AlphabetKind.RECORD,
            fields=tuple((name, part.descriptor) for name, part in fields),
        )
    )


def word(symbols: Alphabet[SemanticValue]) -> Alphabet[ValueNode]:
    return Alphabet(
        AlphabetDescriptor(AlphabetKind.WORD, children=(symbols.descriptor,))
    )


def map_values(
    keys: Alphabet[SemanticValue],
    values: Alphabet[SemanticValue],
) -> Alphabet[ValueNode]:
    return Alphabet(
        AlphabetDescriptor(
            AlphabetKind.MAP,
            children=(keys.descriptor, values.descriptor),
        )
    )


def _structural_schema(kind: AlphabetKind) -> Alphabet[ValueNode]:
    return Alphabet(AlphabetDescriptor(kind))


def graph() -> Alphabet[ValueNode]:
    return _structural_schema(AlphabetKind.GRAPH)


def field() -> Alphabet[ValueNode]:
    return _structural_schema(AlphabetKind.FIELD)


def instruction() -> Alphabet[ValueNode]:
    return _structural_schema(AlphabetKind.INSTRUCTION)


def pattern() -> Alphabet[ValueNode]:
    return _structural_schema(AlphabetKind.PATTERN)


def equation() -> Alphabet[ValueNode]:
    return _structural_schema(AlphabetKind.EQUATION)


def distribution() -> Alphabet[ValueNode]:
    return _structural_schema(AlphabetKind.DISTRIBUTION)


def symbolic(values: tuple[int | str, ...]) -> Alphabet[int | str]:
    return Alphabet(
        AlphabetDescriptor(AlphabetKind.SYMBOLIC, values=tuple(values))
    )


def refine(
    base: Alphabet[SemanticValue],
    constraint: Alphabet[SemanticValue],
) -> Alphabet[SemanticValue]:
    """Intersect a base schema with one closed schema-valued constraint."""

    if type(base) is not Alphabet or type(constraint) is not Alphabet:
        raise TypeError("alphabet refinement needs two Alphabet values")
    return Alphabet(
        AlphabetDescriptor(
            AlphabetKind.REFINEMENT,
            children=(base.descriptor, constraint.descriptor),
        )
    )


def boolean() -> Alphabet[bool]:
    return Alphabet(
        AlphabetDescriptor(AlphabetKind.ENUM, values=(False, True))
    )


def int_range_alphabet(size: int, start: int = 0) -> Alphabet[int]:
    if isinstance(size, bool) or not isinstance(size, int) or size <= 0:
        raise ValueError("size must be a positive integer")
    if isinstance(start, bool) or not isinstance(start, int):
        raise TypeError("start must be an integer")
    return enum(tuple(range(start, start + size)))  # type: ignore[return-value]


def _profile(descriptor: AlphabetDescriptor) -> ValueProfile:
    if descriptor.kind is AlphabetKind.ENUM and descriptor.values == (False, True):
        return ValueProfile.BOOLEAN
    if descriptor.kind in (AlphabetKind.ENUM, AlphabetKind.ORDERED):
        if all(isinstance(value, int) and not isinstance(value, bool) for value in descriptor.values):
            return ValueProfile.INTEGER
        if all(
            isinstance(value, (int, Fraction)) and not isinstance(value, bool)
            for value in descriptor.values
        ):
            return ValueProfile.RATIONAL
        if all(isinstance(value, (int, str)) and not isinstance(value, bool) for value in descriptor.values):
            return ValueProfile.SYMBOLIC
        if all(type(value) is AlgebraicNumber for value in descriptor.values):
            return ValueProfile.ALGEBRAIC
        if all(type(value) is ExactComplex for value in descriptor.values):
            return ValueProfile.COMPLEX
    if descriptor.kind in (
        AlphabetKind.NATURALS,
        AlphabetKind.INTEGERS,
        AlphabetKind.MODULAR,
    ):
        return ValueProfile.INTEGER
    if descriptor.kind in (
        AlphabetKind.RATIONALS,
        AlphabetKind.RATIONAL_INTERVAL,
    ):
        return ValueProfile.RATIONAL
    if descriptor.kind is AlphabetKind.ALGEBRAIC:
        return ValueProfile.ALGEBRAIC
    if descriptor.kind is AlphabetKind.EXACT_COMPLEX:
        return ValueProfile.COMPLEX
    if descriptor.kind is AlphabetKind.REPRESENTED_NUMBER:
        return ValueProfile.REPRESENTED
    if descriptor.kind is AlphabetKind.SYMBOLIC:
        return ValueProfile.SYMBOLIC
    if descriptor.kind in (
        AlphabetKind.TAG,
        AlphabetKind.PRODUCT,
        AlphabetKind.RECORD,
        AlphabetKind.WORD,
        AlphabetKind.MAP,
        AlphabetKind.GRAPH,
        AlphabetKind.FIELD,
        AlphabetKind.INSTRUCTION,
        AlphabetKind.PATTERN,
        AlphabetKind.EQUATION,
        AlphabetKind.DISTRIBUTION,
        AlphabetKind.STRUCTURAL_REFERENCE,
    ):
        return ValueProfile.STRUCTURAL
    if descriptor.kind is AlphabetKind.REFINEMENT:
        return _profile(descriptor.children[0])
    return ValueProfile.EXACT


def _contains(descriptor: AlphabetDescriptor, value: SemanticValue) -> bool:
    kind = descriptor.kind
    if kind in (AlphabetKind.ENUM, AlphabetKind.ORDERED, AlphabetKind.SYMBOLIC):
        return any(semantic_equal(value, candidate) for candidate in descriptor.values)
    if kind is AlphabetKind.NATURALS:
        return isinstance(value, int) and not isinstance(value, bool) and value >= 0
    if kind is AlphabetKind.INTEGERS:
        if not isinstance(value, int) or isinstance(value, bool):
            return False
        minimum = _scalar_parameter(descriptor, "minimum")
        maximum = _scalar_parameter(descriptor, "maximum")
        return (
            (minimum is None or value >= int(minimum))
            and (maximum is None or value <= int(maximum))
        )
    if kind is AlphabetKind.RATIONALS:
        return (
            isinstance(value, (int, Fraction))
            and not isinstance(value, bool)
        )
    if kind is AlphabetKind.RATIONAL_INTERVAL:
        if not isinstance(value, (int, Fraction)) or isinstance(value, bool):
            return False
        lower = _scalar_parameter(descriptor, "lower")
        upper = _scalar_parameter(descriptor, "upper")
        lower_closed = _scalar_parameter(descriptor, "lower_closed")
        upper_closed = _scalar_parameter(descriptor, "upper_closed")
        assert type(lower) is Fraction and type(upper) is Fraction
        assert type(lower_closed) is bool and type(upper_closed) is bool
        exact_value = Fraction(value)
        return (
            exact_value >= lower
            if lower_closed
            else exact_value > lower
        ) and (
            exact_value <= upper
            if upper_closed
            else exact_value < upper
        )
    if kind is AlphabetKind.ALGEBRAIC:
        return type(value) is AlgebraicNumber
    if kind is AlphabetKind.EXACT_COMPLEX:
        return (
            type(value) is ExactComplex
            and _contains(descriptor.children[0], value.real)
            and _contains(descriptor.children[0], value.imaginary)
        )
    if kind is AlphabetKind.MODULAR:
        modulus = int(_scalar_parameter(descriptor, "modulus"))
        return isinstance(value, int) and not isinstance(value, bool) and 0 <= value < modulus
    if kind is AlphabetKind.REPRESENTED_NUMBER:
        return (
            isinstance(value, RepresentedNumber)
            and value.profile is descriptor.represented_profile
        )
    if kind is AlphabetKind.STRUCTURAL_REFERENCE:
        return type(value) is StructuralReference
    if kind is AlphabetKind.UNION:
        return any(_contains(child, value) for child in descriptor.children)
    if kind is AlphabetKind.REFINEMENT:
        base, constraint = descriptor.children
        return _contains(base, value) and _contains(constraint, value)
    if kind is AlphabetKind.TAG:
        expected_tag = str(_scalar_parameter(descriptor, "name"))
        return (
            isinstance(value, ValueNode)
            and value.kind is ValueKind.TAG
            and value.tag == expected_tag
            and len(value.items) == 1
            and _contains(descriptor.children[0], value.items[0])
        )
    if kind is AlphabetKind.PRODUCT:
        return (
            isinstance(value, ValueNode)
            and value.kind is ValueKind.PRODUCT
            and len(value.items) == len(descriptor.children)
            and all(
                _contains(child, item)
                for child, item in zip(descriptor.children, value.items)
            )
        )
    if kind is AlphabetKind.RECORD:
        if not isinstance(value, ValueNode) or value.kind is not ValueKind.RECORD:
            return False
        value_fields = dict(value.fields)
        return (
            tuple(sorted(value_fields)) == tuple(sorted(name for name, _ in descriptor.fields))
            and all(_contains(child, value_fields[name]) for name, child in descriptor.fields)
        )
    if kind is AlphabetKind.WORD:
        return (
            isinstance(value, ValueNode)
            and value.kind is ValueKind.WORD
            and all(_contains(descriptor.children[0], item) for item in value.items)
        )
    if kind is AlphabetKind.MAP:
        return (
            isinstance(value, ValueNode)
            and value.kind is ValueKind.MAP
            and not value.fields
            and all(
                type(entry) is ValueNode
                and entry.kind is ValueKind.PRODUCT
                and entry.tag == _MAP_ENTRY_TAG
                and len(entry.items) == 2
                and _contains(descriptor.children[0], entry.items[0])
                and _contains(descriptor.children[1], entry.items[1])
                for entry in value.items
            )
        )
    structural_kinds = {
        AlphabetKind.GRAPH: ValueKind.GRAPH,
        AlphabetKind.FIELD: ValueKind.FIELD,
        AlphabetKind.INSTRUCTION: ValueKind.INSTRUCTION,
        AlphabetKind.PATTERN: ValueKind.PATTERN,
        AlphabetKind.EQUATION: ValueKind.EQUATION,
        AlphabetKind.DISTRIBUTION: ValueKind.DISTRIBUTION,
    }
    if kind in structural_kinds:
        return isinstance(value, ValueNode) and value.kind is structural_kinds[kind]
    return False


def _descriptor_key(descriptor: AlphabetDescriptor) -> tuple[object, ...]:
    return (
        descriptor.kind.value,
        tuple(_value_key(value) for value in descriptor.values),
        descriptor.scalars,
        tuple(_descriptor_key(child) for child in descriptor.children),
        tuple(
            (name, _descriptor_key(child))
            for name, child in descriptor.fields
        ),
        (
            None
            if descriptor.represented_profile is None
            else descriptor.represented_profile.value
        ),
        descriptor.version,
    )


def _validate_descriptor_shape(descriptor: AlphabetDescriptor) -> None:
    kind = descriptor.kind
    values = bool(descriptor.values)
    scalars = bool(descriptor.scalars)
    children = bool(descriptor.children)
    fields = bool(descriptor.fields)
    profile = descriptor.represented_profile is not None

    if kind in (AlphabetKind.ENUM, AlphabetKind.ORDERED, AlphabetKind.SYMBOLIC):
        if scalars or children or fields or profile:
            raise ValueError(f"{kind.value} alphabet carries irrelevant fields")
        return
    if kind in (
        AlphabetKind.NATURALS,
        AlphabetKind.RATIONALS,
        AlphabetKind.ALGEBRAIC,
        AlphabetKind.STRUCTURAL_REFERENCE,
    ):
        if values or scalars or children or fields or profile:
            raise ValueError(f"{kind.value} alphabet carries irrelevant fields")
        return
    if kind is AlphabetKind.INTEGERS:
        if values or children or fields or profile:
            raise ValueError("integer alphabet carries irrelevant fields")
        if any(name not in ("minimum", "maximum") for name, _ in descriptor.scalars):
            raise ValueError("integer alphabet has an unknown bound")
        return
    if kind is AlphabetKind.RATIONAL_INTERVAL:
        expected_names = (
            "lower",
            "upper",
            "lower_closed",
            "upper_closed",
        )
        if (
            values
            or children
            or fields
            or profile
            or tuple(name for name, _ in descriptor.scalars) != expected_names
        ):
            raise ValueError(
                "rational-interval alphabet has an invalid descriptor shape"
            )
        lower = _scalar_parameter(descriptor, "lower")
        upper = _scalar_parameter(descriptor, "upper")
        lower_closed = _scalar_parameter(descriptor, "lower_closed")
        upper_closed = _scalar_parameter(descriptor, "upper_closed")
        if type(lower) is not Fraction or type(upper) is not Fraction:
            raise TypeError(
                "rational-interval bounds must be exact Fractions"
            )
        if type(lower_closed) is not bool or type(upper_closed) is not bool:
            raise TypeError(
                "rational-interval endpoint flags must be booleans"
            )
        if lower > upper:
            raise ValueError(
                "rational-interval lower bound cannot exceed its upper"
            )
        if lower == upper and not (lower_closed and upper_closed):
            raise ValueError("rational interval cannot be empty")
        return
    if kind is AlphabetKind.MODULAR:
        if (
            values
            or children
            or fields
            or profile
            or tuple(name for name, _ in descriptor.scalars) != ("modulus",)
        ):
            raise ValueError("modular alphabet has an invalid descriptor shape")
        return
    if kind is AlphabetKind.REPRESENTED_NUMBER:
        if values or scalars or children or fields or not profile:
            raise ValueError("represented-number descriptor shape is invalid")
        return
    if kind is AlphabetKind.EXACT_COMPLEX:
        if (
            values
            or scalars
            or fields
            or profile
            or len(descriptor.children) != 1
        ):
            raise ValueError("exact-complex descriptor shape is invalid")
        return
    if kind is AlphabetKind.TAG:
        if (
            values
            or fields
            or profile
            or len(descriptor.children) != 1
            or tuple(name for name, _ in descriptor.scalars) != ("name",)
        ):
            raise ValueError("tag alphabet descriptor shape is invalid")
        return
    if kind in (AlphabetKind.UNION, AlphabetKind.PRODUCT):
        if values or scalars or fields or profile or not children:
            raise ValueError(f"{kind.value} alphabet descriptor shape is invalid")
        return
    if kind is AlphabetKind.RECORD:
        if values or scalars or children or profile or not fields:
            raise ValueError("record alphabet descriptor shape is invalid")
        return
    if kind is AlphabetKind.WORD:
        if (
            values
            or scalars
            or fields
            or profile
            or len(descriptor.children) != 1
        ):
            raise ValueError("word alphabet descriptor shape is invalid")
        return
    if kind is AlphabetKind.MAP:
        if (
            values
            or scalars
            or fields
            or profile
            or len(descriptor.children) != 2
        ):
            raise ValueError("map alphabet descriptor shape is invalid")
        return
    if kind in (
        AlphabetKind.GRAPH,
        AlphabetKind.FIELD,
        AlphabetKind.INSTRUCTION,
        AlphabetKind.PATTERN,
        AlphabetKind.EQUATION,
        AlphabetKind.DISTRIBUTION,
    ):
        if values or scalars or children or fields or profile:
            raise ValueError(f"{kind.value} alphabet carries irrelevant fields")
        return
    if kind is AlphabetKind.REFINEMENT:
        if (
            values
            or scalars
            or fields
            or profile
            or len(descriptor.children) != 2
        ):
            raise ValueError("refinement alphabet descriptor shape is invalid")
        return


def _value_key(value: SemanticValue) -> tuple[str, ...]:
    if isinstance(value, bool):
        return ("bool", str(int(value)))
    if isinstance(value, int):
        return ("int", str(value))
    if isinstance(value, Fraction):
        return ("fraction", str(value.numerator), str(value.denominator))
    if isinstance(value, str):
        return ("str", value)
    if type(value) is AlgebraicNumber:
        assert value.root_index is not None
        return (
            "algebraic",
            *(str(coefficient) for coefficient in value.polynomial),
            "root-index",
            str(value.root_index),
        )
    if type(value) is ExactComplex:
        return (
            "exact-complex",
            *_value_key(value.real),
            "imaginary",
            *_value_key(value.imaginary),
        )
    if type(value) is StructuralReference:
        return (
            "structural-reference",
            (
                "locus"
                if type(value.reference) is loci.Locus
                else "fresh-reference"
            ),
            loci.canonical_identity(value.reference),
        )
    if isinstance(value, RepresentedNumber):
        return (
            "represented",
            value.profile.value,
            repr(value.representation),
        )
    return (
        "node",
        value.kind.value,
        value.tag,
        *(part for item in value.items for part in _value_key(item)),
        *(
            part
            for name, item in value.fields
            for part in (name, *_value_key(item))
        ),
    )


def semantic_equal(left: SemanticValue, right: SemanticValue) -> bool:
    """Exact equality independent of object identity or mapping insertion order."""

    return _value_key(left) == _value_key(right)


__all__ = [
    "AlgebraicNumber",
    "Alphabet",
    "AlphabetDescriptor",
    "AlphabetKind",
    "ExactComplex",
    "ExactReal",
    "ExactScalar",
    "RepresentedNumber",
    "RepresentedNumberProfile",
    "RepresentationPair",
    "RepresentationProfile",
    "RepresentationRelation",
    "SemanticValue",
    "StructuralBinding",
    "StructuralReference",
    "ValueKind",
    "ValueNode",
    "ValueProfile",
    "algebraics",
    "bind_structural_references",
    "boolean",
    "distribution",
    "enum",
    "equation",
    "exact_complexes",
    "field",
    "field_value",
    "graph",
    "instruction",
    "int_range_alphabet",
    "integers",
    "map_entries",
    "map_entry_value",
    "map_get",
    "map_value",
    "map_values",
    "modular",
    "naturals",
    "node_fields",
    "node_get",
    "node_items",
    "ordered",
    "pattern",
    "pattern_value",
    "product",
    "product_items",
    "product_value",
    "rational_interval",
    "rationals",
    "record",
    "record_fields",
    "record_get",
    "record_value",
    "refine",
    "represented_numeric",
    "semantic_equal",
    "symbolic",
    "symbolic_value",
    "structural_references",
    "tag",
    "tag_payload",
    "tag_value",
    "union",
    "word",
    "word_items",
    "word_value",
]
