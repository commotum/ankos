"""Closed schemas for semantic values and exact semantic equality."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Generic, TypeAlias, TypeVar


V = TypeVar("V")
ExactScalar: TypeAlias = bool | int | Fraction | str


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


@dataclass(frozen=True)
class ValueNode:
    """One closed composite value."""

    kind: ValueKind
    tag: str
    items: tuple[ExactScalar | "ValueNode" | "RepresentedNumber", ...] = ()
    fields: tuple[
        tuple[str, ExactScalar | "ValueNode" | "RepresentedNumber"],
        ...,
    ] = ()
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
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
        if self.kind in (ValueKind.RECORD, ValueKind.MAP):
            ordered = tuple(sorted(self.fields, key=lambda item: item[0]))
            if ordered != self.fields:
                object.__setattr__(self, "fields", ordered)
        if self.kind is ValueKind.TAG and (
            len(self.items) != 1 or self.fields
        ):
            raise ValueError("tag values need exactly one payload item")
        if self.kind in (ValueKind.PRODUCT, ValueKind.WORD) and self.fields:
            raise ValueError(f"{self.kind.value} values cannot carry named fields")
        if self.kind in (ValueKind.RECORD, ValueKind.MAP) and self.items:
            raise ValueError(f"{self.kind.value} values cannot carry positional items")


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
        if self.version != 1:
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


SemanticValue: TypeAlias = ExactScalar | RepresentedNumber | ValueNode


def _is_semantic_value(value: object) -> bool:
    return type(value) in (
        bool,
        int,
        Fraction,
        str,
        RepresentedNumber,
        ValueNode,
    )


class AlphabetKind(Enum):
    ENUM = "enum"
    ORDERED = "ordered"
    NATURALS = "naturals"
    INTEGERS = "integers"
    RATIONALS = "rationals"
    MODULAR = "modular"
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
    REFINEMENT = "refinement"


class ValueProfile(Enum):
    BOOLEAN = "boolean"
    INTEGER = "integer"
    RATIONAL = "rational"
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
        if self.version != 1:
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
    if descriptor.kind in (
        AlphabetKind.NATURALS,
        AlphabetKind.INTEGERS,
        AlphabetKind.MODULAR,
    ):
        return ValueProfile.INTEGER
    if descriptor.kind is AlphabetKind.RATIONALS:
        return ValueProfile.RATIONAL
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
    ):
        return ValueProfile.STRUCTURAL
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
    if kind is AlphabetKind.MODULAR:
        modulus = int(_scalar_parameter(descriptor, "modulus"))
        return isinstance(value, int) and not isinstance(value, bool) and 0 <= value < modulus
    if kind is AlphabetKind.REPRESENTED_NUMBER:
        return (
            isinstance(value, RepresentedNumber)
            and value.profile is descriptor.represented_profile
        )
    if kind is AlphabetKind.UNION:
        return any(_contains(child, value) for child in descriptor.children)
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
            and not value.items
            and all(
                _contains(descriptor.children[0], name)
                and _contains(descriptor.children[1], item)
                for name, item in value.fields
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
    if kind in (AlphabetKind.NATURALS, AlphabetKind.RATIONALS):
        if values or scalars or children or fields or profile:
            raise ValueError(f"{kind.value} alphabet carries irrelevant fields")
        return
    if kind is AlphabetKind.INTEGERS:
        if values or children or fields or profile:
            raise ValueError("integer alphabet carries irrelevant fields")
        if any(name not in ("minimum", "maximum") for name, _ in descriptor.scalars):
            raise ValueError("integer alphabet has an unknown bound")
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
            or fields
            or profile
            or len(descriptor.children) != 1
            or not scalars
        ):
            raise ValueError("refinement alphabet descriptor shape is invalid")


def _value_key(value: SemanticValue) -> tuple[str, ...]:
    if isinstance(value, bool):
        return ("bool", str(int(value)))
    if isinstance(value, int):
        return ("int", str(value))
    if isinstance(value, Fraction):
        return ("fraction", str(value.numerator), str(value.denominator))
    if isinstance(value, str):
        return ("str", value)
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
    "Alphabet",
    "AlphabetDescriptor",
    "AlphabetKind",
    "ExactScalar",
    "RepresentedNumber",
    "RepresentedNumberProfile",
    "SemanticValue",
    "ValueKind",
    "ValueNode",
    "ValueProfile",
    "boolean",
    "distribution",
    "enum",
    "equation",
    "field",
    "graph",
    "instruction",
    "int_range_alphabet",
    "integers",
    "map_values",
    "modular",
    "naturals",
    "ordered",
    "pattern",
    "product",
    "rationals",
    "record",
    "represented_numeric",
    "semantic_equal",
    "symbolic",
    "tag",
    "union",
    "word",
]
