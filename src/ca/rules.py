"""Closed Rule denotations and their complete result algebra.

``Rule`` is a frozen, versioned relation over one resolved readable view and
one resolved writable envelope.  This module owns the closed expression
interpreter and Rule-side results; it never commits configurations, realizes a
probability law, calls a solver, imports the program/catalog/RNG layers, or
dispatches on a semantic family name.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from string import Formatter
from typing import Generic, Protocol, TypeAlias, TypeVar, cast

from . import alphabets, frontiers, loci, neighborhoods, seeds


C = TypeVar("C")
R = TypeVar("R")
W = TypeVar("W")
A = TypeVar("A")
V = TypeVar("V", bound=alphabets.SemanticValue)

RuleScalar: TypeAlias = (
    bool
    | int
    | Fraction
    | str
    | alphabets.AlgebraicNumber
    | alphabets.ExactComplex
    | alphabets.StructuralReference
    | alphabets.RepresentedNumber
    | alphabets.ValueNode
)
RuleRuntimeValue: TypeAlias = (
    alphabets.SemanticValue | tuple["RuleRuntimeValue", ...]
)
_BindingFrame: TypeAlias = tuple[RuleRuntimeValue, int]
_BindingContext: TypeAlias = tuple[_BindingFrame, ...]


def _require_version_one(version: object, owner: str) -> None:
    if type(version) is not int:
        raise TypeError(f"{owner} version must be an integer")
    if version != 1:
        raise ValueError(f"unsupported {owner} version {version}")


def _is_rule_scalar(value: object) -> bool:
    return type(value) in (
        bool,
        int,
        Fraction,
        str,
        alphabets.AlgebraicNumber,
        alphabets.ExactComplex,
        alphabets.StructuralReference,
        alphabets.RepresentedNumber,
        alphabets.ValueNode,
    )


# ---------------------------------------------------------------------------
# Closed Rule syntax and compatibility declarations
# ---------------------------------------------------------------------------


class RulePrimitive(Enum):
    """The closed top-level Rule denotation variants."""

    LITERAL = "rule.literal"
    EXPRESSION = "rule.expression"
    CLAUSE_KERNEL = "rule.clause-kernel"
    RELATION = "rule.relation"
    DISTRIBUTION = "rule.distribution"
    PARALLEL = "rule.parallel"
    DIFFERENTIAL = "rule.differential"


class ExpressionPrimitive(Enum):
    """Small, reusable operations admitted by the Rule interpreter."""

    LITERAL = "expression.literal"
    OBSERVATION = "expression.observation"
    GROUP = "expression.group"
    TARGET_REFERENCE = "expression.target-reference"
    BOUND_VALUE = "expression.bound-value"
    BOUND_INDEX = "expression.bound-index"
    PROJECT = "expression.project"
    TUPLE = "expression.tuple"
    ADD = "expression.add"
    SUBTRACT = "expression.subtract"
    MULTIPLY = "expression.multiply"
    DIVIDE = "expression.divide"
    MODULO = "expression.modulo"
    COUNT = "expression.count"
    GATE = "expression.gate"
    LOOKUP = "expression.lookup"
    EQUAL = "expression.equal"
    LESS = "expression.less"
    LESS_EQUAL = "expression.less-equal"
    CONDITIONAL = "expression.conditional"
    ALL = "expression.all"
    ANY = "expression.any"
    RECORD_FIELD = "expression.record-field"
    RECORD_UPDATE = "expression.record-update"
    LENGTH = "expression.length"
    ITEM_AT = "expression.item-at"
    SLICE = "expression.slice"
    CONCATENATE = "expression.concatenate"
    REVERSE = "expression.reverse"
    REPLACE_AT = "expression.replace-at"
    MAP_LOOKUP = "expression.map-lookup"
    MAP_UPDATE = "expression.map-update"
    INDEX_OF = "expression.index-of"
    INDEX_OF_TAG = "expression.index-of-tag"
    FLOOR_DIVIDE = "expression.floor-divide"
    ABSOLUTE = "expression.absolute"
    FRACTIONAL_PART = "expression.fractional-part"
    INTEGER_DIGITS = "expression.integer-digits"
    FROM_DIGITS = "expression.from-digits"
    MAXIMAL_RUNS = "expression.maximal-runs"
    PRODUCT_VALUE = "expression.product-value"
    WORD_VALUE = "expression.word-value"
    FLAT_MAP_LOOKUP = "expression.flat-map-lookup"
    MAP_ITEMS = "expression.map-items"
    FILTER_ITEMS = "expression.filter-items"
    FLAT_MAP_ITEMS = "expression.flat-map-items"
    SLIDING_WINDOWS = "expression.sliding-windows"


class GateKind(Enum):
    """Closed predicates over an exact integer aggregate."""

    ANY = "any"
    ALL = "all"
    MAJORITY = "majority"
    AT_LEAST = "at-least"
    AT_MOST = "at-most"
    EXACTLY = "exactly"


class SequenceBoundary(Enum):
    """Closed boundary laws for finite sequence windows."""

    FIXED = "fixed"
    PERIODIC = "periodic"
    REFLECTIVE = "reflective"


@dataclass(frozen=True)
class RuleExpr:
    """One recursively closed, versioned expression AST node."""

    primitive: ExpressionPrimitive
    arguments: tuple[RuleScalar | "RuleExpr", ...] = ()
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "Rule expression")
        if type(self.primitive) is not ExpressionPrimitive:
            raise TypeError("Rule expression primitive is not recognized")
        if type(self.arguments) is not tuple:
            raise TypeError("Rule expression arguments must be an immutable tuple")
        if any(
            not (_is_rule_scalar(argument) or type(argument) is RuleExpr)
            for argument in self.arguments
        ):
            raise TypeError(
                "Rule expression contains an opaque or executable argument"
            )
        _validate_rule_expr_shape(self)

    @property
    def canonical_identity(self) -> str:
        return loci.canonical_identity(self)


def _validate_rule_expr_shape(expression: RuleExpr) -> None:
    primitive = expression.primitive
    arguments = expression.arguments

    def require_arity(size: int) -> None:
        if len(arguments) != size:
            raise ValueError(
                f"{primitive.value} requires exactly {size} argument"
                f"{'' if size == 1 else 's'}"
            )

    def require_expression(index: int) -> None:
        if type(arguments[index]) is not RuleExpr:
            raise TypeError(f"{primitive.value} argument {index} must be a RuleExpr")

    def require_index(index: int) -> None:
        value = arguments[index]
        if type(value) is not int or value < 0:
            raise ValueError(
                f"{primitive.value} argument {index} must be a non-negative integer"
            )

    if primitive is ExpressionPrimitive.LITERAL:
        require_arity(1)
        if not _is_rule_scalar(arguments[0]):
            raise TypeError("literal expression requires one closed scalar")
        return
    if primitive in (ExpressionPrimitive.OBSERVATION, ExpressionPrimitive.GROUP):
        require_arity(1)
        require_index(0)
        return
    if primitive in (
        ExpressionPrimitive.BOUND_VALUE,
        ExpressionPrimitive.BOUND_INDEX,
    ):
        require_arity(1)
        require_index(0)
        return
    if primitive is ExpressionPrimitive.TARGET_REFERENCE:
        require_arity(0)
        return
    if primitive is ExpressionPrimitive.PROJECT:
        require_arity(2)
        require_expression(0)
        require_index(1)
        return
    if primitive is ExpressionPrimitive.TUPLE:
        if any(type(argument) is not RuleExpr for argument in arguments):
            raise TypeError("tuple expressions may contain only RuleExpr children")
        return
    if primitive in (ExpressionPrimitive.ADD, ExpressionPrimitive.MULTIPLY):
        if not arguments:
            raise ValueError(f"{primitive.value} requires at least one argument")
        if any(type(argument) is not RuleExpr for argument in arguments):
            raise TypeError(
                f"{primitive.value} may contain only RuleExpr operands"
            )
        return
    if primitive in (
        ExpressionPrimitive.SUBTRACT,
        ExpressionPrimitive.DIVIDE,
        ExpressionPrimitive.EQUAL,
        ExpressionPrimitive.LESS,
        ExpressionPrimitive.LESS_EQUAL,
    ):
        require_arity(2)
        require_expression(0)
        require_expression(1)
        return
    if primitive is ExpressionPrimitive.CONDITIONAL:
        require_arity(3)
        require_expression(0)
        require_expression(1)
        require_expression(2)
        return
    if primitive is ExpressionPrimitive.MODULO:
        require_arity(2)
        require_expression(0)
        modulus = arguments[1]
        if type(modulus) is not int or modulus <= 0:
            raise ValueError("modulo expression requires a positive integer modulus")
        return
    if primitive in (
        ExpressionPrimitive.COUNT,
        ExpressionPrimitive.ALL,
        ExpressionPrimitive.ANY,
    ):
        require_arity(1)
        require_expression(0)
        return
    if primitive is ExpressionPrimitive.RECORD_FIELD:
        require_arity(2)
        require_expression(0)
        if type(arguments[1]) is not str or not arguments[1]:
            raise ValueError(
                "record-field expression needs one nonempty literal field name"
            )
        return
    if primitive is ExpressionPrimitive.RECORD_UPDATE:
        require_arity(3)
        require_expression(0)
        if type(arguments[1]) is not str or not arguments[1]:
            raise ValueError(
                "record-update expression needs one nonempty literal field name"
            )
        require_expression(2)
        return
    if primitive in (
        ExpressionPrimitive.LENGTH,
        ExpressionPrimitive.REVERSE,
        ExpressionPrimitive.ABSOLUTE,
        ExpressionPrimitive.FRACTIONAL_PART,
        ExpressionPrimitive.MAXIMAL_RUNS,
    ):
        require_arity(1)
        require_expression(0)
        return
    if primitive in (
        ExpressionPrimitive.ITEM_AT,
        ExpressionPrimitive.SLICE,
        ExpressionPrimitive.REPLACE_AT,
        ExpressionPrimitive.MAP_LOOKUP,
        ExpressionPrimitive.MAP_UPDATE,
        ExpressionPrimitive.INDEX_OF,
    ):
        require_arity(3)
        require_expression(0)
        require_expression(1)
        require_expression(2)
        return
    if primitive is ExpressionPrimitive.CONCATENATE:
        if not arguments:
            raise ValueError(
                "concatenate expression requires at least one operand"
            )
        if any(type(argument) is not RuleExpr for argument in arguments):
            raise TypeError(
                "concatenate expression may contain only RuleExpr operands"
            )
        return
    if primitive is ExpressionPrimitive.INDEX_OF_TAG:
        require_arity(3)
        require_expression(0)
        if type(arguments[1]) is not str or not arguments[1]:
            raise ValueError(
                "index-of-tag expression needs one nonempty literal tag"
            )
        require_expression(2)
        return
    if primitive is ExpressionPrimitive.FLOOR_DIVIDE:
        require_arity(2)
        require_expression(0)
        require_expression(1)
        return
    if primitive is ExpressionPrimitive.INTEGER_DIGITS:
        if len(arguments) not in (2, 3):
            raise ValueError(
                "integer-digits expression requires value, base, and "
                "optional width"
            )
        require_expression(0)
        base = arguments[1]
        if type(base) is not int or base < 2:
            raise ValueError(
                "integer-digits expression base must be an integer >= 2"
            )
        if len(arguments) == 3:
            width = arguments[2]
            if type(width) is RuleExpr:
                return
            if type(width) is not int or width <= 0:
                raise ValueError(
                    "integer-digits expression width must be a positive "
                    "integer or RuleExpr"
                )
        return
    if primitive is ExpressionPrimitive.FROM_DIGITS:
        require_arity(2)
        require_expression(0)
        base = arguments[1]
        if type(base) is not int or base < 2:
            raise ValueError(
                "from-digits expression base must be an integer >= 2"
            )
        return
    if primitive in (
        ExpressionPrimitive.PRODUCT_VALUE,
        ExpressionPrimitive.WORD_VALUE,
    ):
        if not arguments or type(arguments[0]) is not str or not arguments[0]:
            raise ValueError(
                f"{primitive.value} needs one leading nonempty literal tag"
            )
        if (
            primitive is ExpressionPrimitive.PRODUCT_VALUE
            and len(arguments) < 2
        ):
            raise ValueError(
                "product-value expression needs at least one item"
            )
        if any(type(argument) is not RuleExpr for argument in arguments[1:]):
            raise TypeError(
                f"{primitive.value} items must be RuleExpr values"
            )
        return
    if primitive is ExpressionPrimitive.FLAT_MAP_LOOKUP:
        require_arity(2)
        require_expression(0)
        require_expression(1)
        return
    if primitive in (
        ExpressionPrimitive.MAP_ITEMS,
        ExpressionPrimitive.FLAT_MAP_ITEMS,
    ):
        require_arity(3)
        require_expression(0)
        require_expression(1)
        if type(arguments[2]) is not str or not arguments[2]:
            raise ValueError(
                f"{primitive.value} needs one nonempty literal output tag"
            )
        return
    if primitive is ExpressionPrimitive.FILTER_ITEMS:
        require_arity(2)
        require_expression(0)
        require_expression(1)
        return
    if primitive is ExpressionPrimitive.SLIDING_WINDOWS:
        if len(arguments) not in (4, 5):
            raise ValueError(
                "sliding-windows expression requires source, before, after, "
                "boundary, and a fixed exterior only when needed"
            )
        require_expression(0)
        require_index(1)
        require_index(2)
        if type(arguments[3]) is not str:
            raise TypeError(
                "sliding-windows boundary must be a literal string"
            )
        try:
            boundary = SequenceBoundary(arguments[3])
        except ValueError as error:
            raise ValueError(
                "sliding-windows boundary is not recognized"
            ) from error
        if boundary is SequenceBoundary.FIXED:
            if len(arguments) != 5:
                raise ValueError(
                    "fixed sliding-windows requires one exterior expression"
                )
            require_expression(4)
        elif len(arguments) != 4:
            raise ValueError(
                "non-fixed sliding-windows cannot carry an exterior"
            )
        return
    if primitive is ExpressionPrimitive.GATE:
        require_arity(3)
        require_expression(0)
        gate_kind = arguments[1]
        if type(gate_kind) is not str:
            raise TypeError("gate expression kind must be a string")
        try:
            GateKind(gate_kind)
        except ValueError as error:
            raise ValueError("gate expression kind is not recognized") from error
        if type(arguments[2]) is not int:
            raise TypeError("gate expression threshold must be an integer")
        return
    if primitive is ExpressionPrimitive.LOOKUP:
        require_arity(2)
        require_expression(0)
        require_expression(1)
        return
    raise TypeError("Rule expression primitive is not recognized")


@dataclass(frozen=True)
class RuleContract:
    """Immutable declarations used for five-field compatibility checking."""

    configuration_contract: loci.CarrierContract
    value_profile: alphabets.ValueProfile
    required_read_shape: neighborhoods.ResultShape
    required_join_shape: neighborhoods.JoinShape
    required_effect_profile: frontiers.EffectProfile
    exactness_profile: seeds.ExactnessProfile = seeds.ExactnessProfile.EXACT
    entropy_interface: seeds.EntropyInterface = seeds.EntropyInterface.NONE
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "Rule contract")
        if type(self.configuration_contract) is not loci.CarrierContract:
            raise TypeError("Rule configuration contract is not recognized")
        if not isinstance(self.value_profile, alphabets.ValueProfile):
            raise TypeError("Rule value profile is not recognized")
        if type(self.required_read_shape) is not neighborhoods.ResultShape:
            raise TypeError("Rule read shape is not recognized")
        if type(self.required_join_shape) is not neighborhoods.JoinShape:
            raise TypeError("Rule join shape is not recognized")
        if type(self.required_effect_profile) is not frontiers.EffectProfile:
            raise TypeError("Rule effect profile is not recognized")
        if not isinstance(self.exactness_profile, seeds.ExactnessProfile):
            raise TypeError("Rule exactness_profile must be seeds.ExactnessProfile")
        if not isinstance(self.entropy_interface, seeds.EntropyInterface):
            raise TypeError("Rule entropy_interface must be seeds.EntropyInterface")


def literal_expr(value: RuleScalar) -> RuleExpr:
    """Build one exact literal expression."""

    return RuleExpr(ExpressionPrimitive.LITERAL, (value,))


def observation(index: int) -> RuleExpr:
    """Read one value from the flat, identity-preserving old-snapshot view."""

    if isinstance(index, bool) or index < 0:
        raise ValueError("observation index must be a non-negative integer")
    return RuleExpr(ExpressionPrimitive.OBSERVATION, (index,))


def group(index: int) -> RuleExpr:
    """Read the ordered values of one group in the current join context."""

    if isinstance(index, bool) or index < 0:
        raise ValueError("group index must be a non-negative integer")
    return RuleExpr(ExpressionPrimitive.GROUP, (index,))


def target_reference() -> RuleExpr:
    """Reference the existing or fresh target currently evaluating a plan."""

    return RuleExpr(ExpressionPrimitive.TARGET_REFERENCE)


def bound_value(depth: int = 0) -> RuleExpr:
    """Read the value from one enclosing lexical sequence binding."""

    if type(depth) is not int or depth < 0:
        raise ValueError("bound-value depth must be a non-negative integer")
    return RuleExpr(ExpressionPrimitive.BOUND_VALUE, (depth,))


def bound_index(depth: int = 0) -> RuleExpr:
    """Read the index from one enclosing lexical sequence binding."""

    if type(depth) is not int or depth < 0:
        raise ValueError("bound-index depth must be a non-negative integer")
    return RuleExpr(ExpressionPrimitive.BOUND_INDEX, (depth,))


def project(source: RuleExpr, index: int) -> RuleExpr:
    """Project an exact position from a tuple-valued expression."""

    if isinstance(index, bool) or index < 0:
        raise ValueError("projection index must be a non-negative integer")
    return RuleExpr(ExpressionPrimitive.PROJECT, (source, index))


def add(*parts: RuleExpr) -> RuleExpr:
    if not parts:
        raise ValueError("add requires at least one expression")
    return RuleExpr(ExpressionPrimitive.ADD, tuple(parts))


def subtract(left: RuleExpr, right: RuleExpr) -> RuleExpr:
    return RuleExpr(ExpressionPrimitive.SUBTRACT, (left, right))


def multiply(*parts: RuleExpr) -> RuleExpr:
    if not parts:
        raise ValueError("multiply requires at least one expression")
    return RuleExpr(ExpressionPrimitive.MULTIPLY, tuple(parts))


def divide(left: RuleExpr, right: RuleExpr) -> RuleExpr:
    return RuleExpr(ExpressionPrimitive.DIVIDE, (left, right))


def modulo(value: RuleExpr, modulus: int) -> RuleExpr:
    if isinstance(modulus, bool) or modulus <= 0:
        raise ValueError("modulus must be a positive integer")
    return RuleExpr(ExpressionPrimitive.MODULO, (value, modulus))


def count(source: RuleExpr) -> RuleExpr:
    return RuleExpr(ExpressionPrimitive.COUNT, (source,))


def gate(
    source: RuleExpr,
    kind: GateKind,
    *,
    threshold: int = 0,
) -> RuleExpr:
    if isinstance(threshold, bool):
        raise TypeError("gate threshold must be an integer")
    return RuleExpr(
        ExpressionPrimitive.GATE,
        (source, kind.value, int(threshold)),
    )


def lookup(table_values: tuple[RuleScalar, ...], index: RuleExpr) -> RuleExpr:
    """Build an exact finite lookup; concrete table data is stored directly."""

    if not table_values:
        raise ValueError("lookup table cannot be empty")
    table_node = RuleExpr(
        ExpressionPrimitive.TUPLE,
        tuple(literal_expr(value) for value in table_values),
    )
    return RuleExpr(ExpressionPrimitive.LOOKUP, (table_node, index))


def equal(left: RuleExpr, right: RuleExpr) -> RuleExpr:
    return RuleExpr(ExpressionPrimitive.EQUAL, (left, right))


def less_than(left: RuleExpr, right: RuleExpr) -> RuleExpr:
    return RuleExpr(ExpressionPrimitive.LESS, (left, right))


def less_equal(left: RuleExpr, right: RuleExpr) -> RuleExpr:
    return RuleExpr(ExpressionPrimitive.LESS_EQUAL, (left, right))


def conditional(
    condition: RuleExpr,
    when_true: RuleExpr,
    when_false: RuleExpr,
) -> RuleExpr:
    return RuleExpr(
        ExpressionPrimitive.CONDITIONAL,
        (condition, when_true, when_false),
    )


def record_field(source: RuleExpr, field: str) -> RuleExpr:
    """Read one existing named field from a semantic record value."""

    if type(field) is not str or not field:
        raise ValueError("record field name must be a nonempty string")
    return RuleExpr(ExpressionPrimitive.RECORD_FIELD, (source, field))


def record_update(
    source: RuleExpr,
    field: str,
    value: RuleExpr,
) -> RuleExpr:
    """Replace one existing named field and return a new semantic record."""

    if type(field) is not str or not field:
        raise ValueError("record field name must be a nonempty string")
    return RuleExpr(
        ExpressionPrimitive.RECORD_UPDATE,
        (source, field, value),
    )


def length(source: RuleExpr) -> RuleExpr:
    """Return the exact length of a semantic word or runtime tuple."""

    return RuleExpr(ExpressionPrimitive.LENGTH, (source,))


def item_at(
    source: RuleExpr,
    index: RuleExpr,
    default: RuleExpr,
) -> RuleExpr:
    """Read an integer index, defaulting outside ``[0, length)`` without wrap."""

    return RuleExpr(ExpressionPrimitive.ITEM_AT, (source, index, default))


def slice_items(
    source: RuleExpr,
    start: RuleExpr,
    stop: RuleExpr,
) -> RuleExpr:
    """Return one strict half-open slice as a semantic word."""

    return RuleExpr(ExpressionPrimitive.SLICE, (source, start, stop))


def concatenate(*sources: RuleExpr) -> RuleExpr:
    """Concatenate semantic words/runtime tuples into one semantic word."""

    if not sources:
        raise ValueError("concatenate requires at least one expression")
    return RuleExpr(ExpressionPrimitive.CONCATENATE, tuple(sources))


def reverse(source: RuleExpr) -> RuleExpr:
    """Reverse a semantic word/runtime tuple into one semantic word."""

    return RuleExpr(ExpressionPrimitive.REVERSE, (source,))


def replace_at(
    source: RuleExpr,
    index: RuleExpr,
    value: RuleExpr,
) -> RuleExpr:
    """Strictly replace one dynamic sequence position."""

    return RuleExpr(ExpressionPrimitive.REPLACE_AT, (source, index, value))


def map_lookup(
    source: RuleExpr,
    key: RuleExpr,
    default: RuleExpr,
) -> RuleExpr:
    """Look up one arbitrary semantic key in a sealed association value."""

    return RuleExpr(ExpressionPrimitive.MAP_LOOKUP, (source, key, default))


def map_update(
    source: RuleExpr,
    key: RuleExpr,
    value: RuleExpr,
) -> RuleExpr:
    """Replace or insert one semantic association and return a new map."""

    return RuleExpr(ExpressionPrimitive.MAP_UPDATE, (source, key, value))


def index_of(
    source: RuleExpr,
    needle: RuleExpr,
    default: RuleExpr,
) -> RuleExpr:
    """Return the first semantic-equality index or an explicit integer default."""

    return RuleExpr(ExpressionPrimitive.INDEX_OF, (source, needle, default))


def index_of_tag(
    source: RuleExpr,
    tag: str,
    default: RuleExpr,
) -> RuleExpr:
    """Return the first ValueNode carrying ``tag`` or an integer default."""

    if type(tag) is not str or not tag:
        raise ValueError("searched tag must be a nonempty string")
    return RuleExpr(ExpressionPrimitive.INDEX_OF_TAG, (source, tag, default))


def floor_divide(left: RuleExpr, right: RuleExpr) -> RuleExpr:
    """Return the mathematical floor of one exact quotient."""

    return RuleExpr(ExpressionPrimitive.FLOOR_DIVIDE, (left, right))


def absolute(value: RuleExpr) -> RuleExpr:
    """Return the exact absolute value."""

    return RuleExpr(ExpressionPrimitive.ABSOLUTE, (value,))


def fractional_part(value: RuleExpr) -> RuleExpr:
    """Return ``value - IntegerPart[value]`` exactly.

    IntegerPart truncates toward zero, so negative inputs retain a negative
    fractional part rather than silently acquiring modulo-one semantics.
    """

    return RuleExpr(ExpressionPrimitive.FRACTIONAL_PART, (value,))


def integer_digits(
    value: RuleExpr,
    base: int,
    *,
    width: int | RuleExpr | None = None,
) -> RuleExpr:
    """Encode an integer using canonical or expression-selected positive width."""

    if type(base) is not int or base < 2:
        raise ValueError("integer-digits base must be an integer >= 2")
    arguments: tuple[RuleScalar | RuleExpr, ...] = (value, base)
    if width is not None:
        if type(width) is not RuleExpr and (
            type(width) is not int or width <= 0
        ):
            raise ValueError(
                "integer-digits width must be a positive integer or RuleExpr"
            )
        arguments = (*arguments, width)
    return RuleExpr(ExpressionPrimitive.INTEGER_DIGITS, arguments)


def from_digits(source: RuleExpr, base: int) -> RuleExpr:
    """Decode one nonempty semantic digit word exactly."""

    if type(base) is not int or base < 2:
        raise ValueError("from-digits base must be an integer >= 2")
    return RuleExpr(ExpressionPrimitive.FROM_DIGITS, (source, base))


def maximal_runs(source: RuleExpr) -> RuleExpr:
    """Encode maximal equal runs as a semantic word of named records."""

    return RuleExpr(ExpressionPrimitive.MAXIMAL_RUNS, (source,))


def product_value(tag: str, *items: RuleExpr) -> RuleExpr:
    """Construct one dynamic semantic product value."""

    if type(tag) is not str or not tag:
        raise ValueError("product tag must be a nonempty string")
    if not items:
        raise ValueError("product value requires at least one item")
    return RuleExpr(ExpressionPrimitive.PRODUCT_VALUE, (tag, *items))


def word_value(tag: str, *items: RuleExpr) -> RuleExpr:
    """Construct one dynamic semantic word value."""

    if type(tag) is not str or not tag:
        raise ValueError("word tag must be a nonempty string")
    return RuleExpr(ExpressionPrimitive.WORD_VALUE, (tag, *items))


def flat_map_lookup(source: RuleExpr, table: RuleExpr) -> RuleExpr:
    """Map each semantic word item through a total word-valued association."""

    return RuleExpr(ExpressionPrimitive.FLAT_MAP_LOOKUP, (source, table))


def map_items(
    source: RuleExpr,
    body: RuleExpr,
    output_tag: str,
) -> RuleExpr:
    """Evaluate ``body`` once per item under one lexical value/index binding."""

    if type(output_tag) is not str or not output_tag:
        raise ValueError("map-items output tag must be a nonempty string")
    return RuleExpr(
        ExpressionPrimitive.MAP_ITEMS,
        (source, body, output_tag),
    )


def filter_items(source: RuleExpr, predicate: RuleExpr) -> RuleExpr:
    """Retain source items whose bound predicate evaluates to one."""

    return RuleExpr(
        ExpressionPrimitive.FILTER_ITEMS,
        (source, predicate),
    )


def flat_map_items(
    source: RuleExpr,
    body: RuleExpr,
    output_tag: str,
) -> RuleExpr:
    """Evaluate one word-valued body per item and concatenate the results."""

    if type(output_tag) is not str or not output_tag:
        raise ValueError("flat-map-items output tag must be a nonempty string")
    return RuleExpr(
        ExpressionPrimitive.FLAT_MAP_ITEMS,
        (source, body, output_tag),
    )


def sliding_windows(
    source: RuleExpr,
    before: int,
    after: int,
    boundary: SequenceBoundary,
    *,
    exterior: RuleExpr | None = None,
) -> RuleExpr:
    """Build one fixed-width semantic window around every source item."""

    if type(before) is not int or before < 0:
        raise ValueError(
            "sliding-windows before extent must be a non-negative integer"
        )
    if type(after) is not int or after < 0:
        raise ValueError(
            "sliding-windows after extent must be a non-negative integer"
        )
    if type(boundary) is not SequenceBoundary:
        raise TypeError("sliding-windows boundary is not recognized")
    if boundary is SequenceBoundary.FIXED:
        if type(exterior) is not RuleExpr:
            raise ValueError(
                "fixed sliding-windows requires one exterior expression"
            )
        arguments: tuple[RuleScalar | RuleExpr, ...] = (
            source,
            before,
            after,
            boundary.value,
            exterior,
        )
    else:
        if exterior is not None:
            raise ValueError(
                "non-fixed sliding-windows cannot carry an exterior"
            )
        arguments = (source, before, after, boundary.value)
    return RuleExpr(ExpressionPrimitive.SLIDING_WINDOWS, arguments)


def capability_index(index: int) -> CapabilitySelector:
    """Select one resolved writable capability by canonical sequence index."""

    return CapabilitySelector(CapabilitySelectorKind.INDEX, index=index)


def capability_target(
    target: loci.Locus | loci.FreshReference,
) -> CapabilitySelector:
    """Select one resolved writable capability by exact target identity."""

    return CapabilitySelector(CapabilitySelectorKind.TARGET, target=target)


def every_capability() -> CapabilitySelector:
    """Select every capability in the existing or fresh side of a plan."""

    return CapabilitySelector(CapabilitySelectorKind.EVERY)


# ---------------------------------------------------------------------------
# Evidence, cardinality, total dispositions, and Rule atoms
# ---------------------------------------------------------------------------


class CertificateKind(Enum):
    """Recognized proof/evidence obligations retained by Rule results."""

    SOUNDNESS = "soundness"
    COMPLETENESS = "completeness"
    CARDINALITY = "cardinality"
    TOTALITY = "totality"
    NORMALIZATION = "normalization"
    MEASURABILITY = "measurability"
    DERIVATION = "derivation"
    TERMINALITY = "terminality"
    DIVERGENCE = "divergence"
    CONFORMANCE = "conformance"
    COMPOSITION = "composition"


@dataclass(frozen=True)
class Certificate:
    """Closed structural evidence; never an executable proof callback."""

    kind: CertificateKind
    statement: RuleExpr
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "certificate")
        if type(self.kind) is not CertificateKind:
            raise TypeError("certificate kind is not recognized")
        if type(self.statement) is not RuleExpr:
            raise TypeError("certificate statement must be a closed RuleExpr")

    @property
    def canonical_identity(self) -> str:
        return loci.canonical_identity(self)


def _certificate(kind: CertificateKind, label: str) -> Certificate:
    return Certificate(kind, literal_expr(label))


def _require_cardinality_certificate(
    evidence: object,
    owner: str,
) -> None:
    if (
        type(evidence) is not Certificate
        or evidence.kind is not CertificateKind.CARDINALITY
    ):
        raise ValueError(f"{owner} needs exact cardinality evidence")


@dataclass(frozen=True)
class ExactlyZero:
    evidence: Certificate

    def __post_init__(self) -> None:
        _require_cardinality_certificate(self.evidence, "ExactlyZero")


@dataclass(frozen=True)
class ExactlyOne:
    evidence: Certificate

    def __post_init__(self) -> None:
        _require_cardinality_certificate(self.evidence, "ExactlyOne")


class InfiniteCardinality(Enum):
    COUNTABLY_INFINITE = "countably-infinite"
    UNCOUNTABLE = "uncountable"


@dataclass(frozen=True)
class Many:
    """An exact finite size of at least two, or one named infinite size."""

    exact_finite_size: int | None
    infinite: InfiniteCardinality | None
    evidence: Certificate

    def __post_init__(self) -> None:
        finite = self.exact_finite_size
        if (finite is None) == (self.infinite is None):
            raise ValueError("Many requires exactly one finite or infinite size")
        if finite is not None and (
            isinstance(finite, bool)
            or not isinstance(finite, int)
            or finite < 2
        ):
            raise ValueError("finite Many cardinality must be at least two")
        if self.infinite is not None and type(self.infinite) is not InfiniteCardinality:
            raise TypeError("Many infinite cardinality is not recognized")
        _require_cardinality_certificate(self.evidence, "Many")


@dataclass(frozen=True)
class Undetermined:
    """Exact relation data whose cardinality is not established."""

    reason: RuleExpr
    obligation: Certificate

    def __post_init__(self) -> None:
        if type(self.reason) is not RuleExpr:
            raise TypeError("Undetermined reason must be a RuleExpr")
        _require_cardinality_certificate(self.obligation, "Undetermined")


Cardinality: TypeAlias = ExactlyZero | ExactlyOne | Many | Undetermined
CardinalityClaim: TypeAlias = Cardinality


def finite_cardinality(size: int) -> Cardinality:
    """Construct the exact cardinality claim for a finite support."""

    if isinstance(size, bool) or size < 0:
        raise ValueError("finite cardinality must be a non-negative integer")
    evidence = _certificate(CertificateKind.CARDINALITY, f"exactly:{size}")
    if size == 0:
        return ExactlyZero(evidence)
    if size == 1:
        return ExactlyOne(evidence)
    return Many(size, None, evidence)


def cardinality_size(cardinality: Cardinality) -> int | None:
    if isinstance(cardinality, ExactlyZero):
        return 0
    if isinstance(cardinality, ExactlyOne):
        return 1
    if isinstance(cardinality, Many):
        return cardinality.exact_finite_size
    return None


class DispositionAction(Enum):
    """The complete action vocabulary over writable capabilities."""

    PRESERVE = "preserve"
    REPLACE = "replace"
    DELETE = "delete"
    ABSENT = "absent"
    CREATE = "create"


@dataclass(frozen=True)
class NoPayload:
    """Payload marker for Preserve/Delete/Absent."""


@dataclass(frozen=True)
class ValuePayload(Generic[V]):
    value: V

    def __post_init__(self) -> None:
        if not alphabets._is_semantic_value(self.value):
            raise TypeError(
                "disposition value payload needs a semantic alphabet value"
            )


DispositionPayload: TypeAlias = NoPayload | ValuePayload[V]


@dataclass(frozen=True)
class Disposition(Generic[W, V]):
    """One explicit action for one existing or fresh writable target."""

    target: W
    action: DispositionAction
    payload: DispositionPayload[V]
    evidence: Certificate
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "disposition")
        if type(self.action) is not DispositionAction:
            raise TypeError("disposition action is not recognized")
        if self.action in (
            DispositionAction.PRESERVE,
            DispositionAction.REPLACE,
            DispositionAction.DELETE,
        ):
            if type(self.target) is not loci.Locus:
                raise TypeError("existing disposition target must be a Locus")
        elif type(self.target) is not loci.FreshReference:
            raise TypeError("fresh disposition target must be a FreshReference")
        if type(self.payload) not in (NoPayload, ValuePayload):
            raise TypeError("disposition payload variant is not recognized")
        if (
            type(self.evidence) is not Certificate
            or self.evidence.kind is not CertificateKind.TOTALITY
        ):
            raise ValueError("disposition needs totality evidence")
        has_value = isinstance(self.payload, ValuePayload)
        requires_value = self.action in (
            DispositionAction.REPLACE,
            DispositionAction.CREATE,
        )
        if has_value != requires_value:
            raise ValueError(
                f"{self.action.value} disposition payload does not match its action"
            )

    @property
    def canonical_identity(self) -> str:
        return loci.canonical_identity(self)


@dataclass(frozen=True)
class TotalDisposition(Generic[V]):
    """Total existing/fresh meaning over one resolved writable envelope."""

    existing: tuple[Disposition[loci.Locus, V], ...]
    fresh: tuple[Disposition[loci.FreshReference, V], ...]
    totality_evidence: Certificate
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "total-disposition")
        if type(self.existing) is not tuple or type(self.fresh) is not tuple:
            raise TypeError("total disposition entries must be immutable tuples")
        if any(type(item) is not Disposition for item in self.entries):
            raise TypeError("total disposition contains an unknown entry variant")
        if (
            type(self.totality_evidence) is not Certificate
            or self.totality_evidence.kind is not CertificateKind.TOTALITY
        ):
            raise ValueError("total disposition needs totality evidence")
        existing_targets = tuple(item.target for item in self.existing)
        fresh_targets = tuple(item.target for item in self.fresh)
        if len(existing_targets) != len(set(existing_targets)):
            raise ValueError("existing dispositions contain duplicate targets")
        if len(fresh_targets) != len(set(fresh_targets)):
            raise ValueError("fresh dispositions contain duplicate targets")
        if any(
            item.action
            not in (
                DispositionAction.PRESERVE,
                DispositionAction.REPLACE,
                DispositionAction.DELETE,
            )
            for item in self.existing
        ):
            raise ValueError("existing target has a fresh-only disposition")
        if any(
            item.action not in (DispositionAction.ABSENT, DispositionAction.CREATE)
            for item in self.fresh
        ):
            raise ValueError("fresh target has an existing-only disposition")

    @property
    def entries(
        self,
    ) -> tuple[
        Disposition[loci.Locus, V] | Disposition[loci.FreshReference, V],
        ...,
    ]:
        return (*self.existing, *self.fresh)

    @property
    def canonical_identity(self) -> str:
        return loci.canonical_identity(self)


def preserve(target: loci.Locus) -> Disposition[loci.Locus, V]:
    return Disposition(
        target,
        DispositionAction.PRESERVE,
        NoPayload(),
        _certificate(CertificateKind.TOTALITY, "existing:preserve"),
    )


def replace(
    target: loci.Locus,
    value: V,
) -> Disposition[loci.Locus, V]:
    return Disposition(
        target,
        DispositionAction.REPLACE,
        ValuePayload(value),
        _certificate(CertificateKind.TOTALITY, "existing:replace"),
    )


def delete(target: loci.Locus) -> Disposition[loci.Locus, V]:
    return Disposition(
        target,
        DispositionAction.DELETE,
        NoPayload(),
        _certificate(CertificateKind.TOTALITY, "existing:delete"),
    )


def absent(
    target: loci.FreshReference,
) -> Disposition[loci.FreshReference, V]:
    return Disposition(
        target,
        DispositionAction.ABSENT,
        NoPayload(),
        _certificate(CertificateKind.TOTALITY, "fresh:absent"),
    )


def create(
    target: loci.FreshReference,
    value: V,
) -> Disposition[loci.FreshReference, V]:
    return Disposition(
        target,
        DispositionAction.CREATE,
        ValuePayload(value),
        _certificate(CertificateKind.TOTALITY, "fresh:create"),
    )


class Progress(Enum):
    ADVANCED = "advanced"
    QUIESCENT = "quiescent"


class NoSuccessorOutcome(Enum):
    TERMINAL = "terminal"
    UNDEFINED = "undefined"
    DECLARED_FAILURE = "declared-failure"
    DIVERGENT = "divergent"


@dataclass(frozen=True)
class Continue:
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "continuation")


@dataclass(frozen=True)
class Stop:
    reason: RuleExpr
    certificate: Certificate
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "continuation")
        if type(self.reason) is not RuleExpr:
            raise TypeError("stopping reason must be a RuleExpr")
        if (
            type(self.certificate) is not Certificate
            or self.certificate.kind is not CertificateKind.TERMINALITY
        ):
            raise ValueError("Stop needs terminality evidence")


Continuation: TypeAlias = Continue | Stop


@dataclass(frozen=True)
class Witness:
    """Stable structural identity sufficient to reproduce one atom."""

    identity: str
    descriptor: RuleExpr
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "witness")
        if not isinstance(self.identity, str) or not self.identity:
            raise ValueError("witness identity cannot be empty")
        if type(self.descriptor) is not RuleExpr:
            raise TypeError("witness descriptor must be a RuleExpr")

    @property
    def canonical_identity(self) -> str:
        return self.identity


Provenance: TypeAlias = tuple[str, ...]


@dataclass(frozen=True)
class Derivation(Generic[V]):
    replacement: TotalDisposition[V]
    progress: Progress
    continuation: Continuation
    witness: Witness
    provenance: Provenance
    certificate: Certificate
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "derivation")
        if type(self.replacement) is not TotalDisposition:
            raise TypeError("derivation replacement is not recognized")
        if type(self.progress) is not Progress:
            raise TypeError("derivation progress is not recognized")
        if type(self.continuation) not in (Continue, Stop):
            raise TypeError("derivation continuation is not recognized")
        if type(self.witness) is not Witness:
            raise TypeError("derivation witness is not recognized")
        if type(self.provenance) is not tuple:
            raise TypeError("derivation provenance must be an immutable tuple")
        if (
            not self.provenance
            or any(type(item) is not str or not item for item in self.provenance)
        ):
            raise ValueError("derivation provenance cannot be empty")
        if (
            type(self.certificate) is not Certificate
            or self.certificate.kind is not CertificateKind.DERIVATION
        ):
            raise ValueError("derivation needs derivation evidence")

    @property
    def canonical_identity(self) -> str:
        return self.witness.canonical_identity


@dataclass(frozen=True)
class NoSuccessor:
    outcome: NoSuccessorOutcome
    reason: RuleExpr
    witness: Witness
    provenance: Provenance
    certificate: Certificate
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "no-successor")
        if type(self.outcome) is not NoSuccessorOutcome:
            raise TypeError("no-successor outcome is not recognized")
        if type(self.reason) is not RuleExpr:
            raise TypeError("no-successor reason must be a RuleExpr")
        if type(self.witness) is not Witness:
            raise TypeError("no-successor witness is not recognized")
        if type(self.provenance) is not tuple:
            raise TypeError("no-successor provenance must be an immutable tuple")
        if (
            not self.provenance
            or any(type(item) is not str or not item for item in self.provenance)
        ):
            raise ValueError("no-successor provenance cannot be empty")
        if type(self.certificate) is not Certificate:
            raise TypeError("no-successor certificate is not recognized")
        if (
            self.outcome is NoSuccessorOutcome.DIVERGENT
            and self.certificate.kind is not CertificateKind.DIVERGENCE
        ):
            raise ValueError("Divergent needs a divergence certificate")
        if (
            self.outcome is not NoSuccessorOutcome.DIVERGENT
            and self.certificate.kind is not CertificateKind.TERMINALITY
        ):
            raise ValueError("no-successor atom needs terminality evidence")

    @property
    def canonical_identity(self) -> str:
        return self.witness.canonical_identity


RuleAtom: TypeAlias = Derivation[V] | NoSuccessor


# ---------------------------------------------------------------------------
# Complete finite/intensional supports and exact probability laws
# ---------------------------------------------------------------------------


class SupportPresentation(Enum):
    FINITE = "finite"
    INTENSIONAL = "intensional"


@dataclass(frozen=True)
class SupportSpace(Generic[A]):
    """Complete finite atoms or one complete intensional relation."""

    presentation: SupportPresentation
    atoms: tuple[A, ...]
    relation: RuleExpr | None
    cardinality: Cardinality
    completeness_evidence: Certificate
    soundness_evidence: Certificate
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "support")
        if type(self.presentation) is not SupportPresentation:
            raise TypeError("support presentation is not recognized")
        if type(self.atoms) is not tuple:
            raise TypeError("support atoms must be an immutable tuple")
        if self.relation is not None and type(self.relation) is not RuleExpr:
            raise TypeError("support relation must be a RuleExpr or None")
        if type(self.cardinality) not in (
            ExactlyZero,
            ExactlyOne,
            Many,
            Undetermined,
        ):
            raise TypeError("support cardinality variant is not recognized")
        if (
            type(self.completeness_evidence) is not Certificate
            or self.completeness_evidence.kind is not CertificateKind.COMPLETENESS
        ):
            raise ValueError("support needs completeness evidence")
        if (
            type(self.soundness_evidence) is not Certificate
            or self.soundness_evidence.kind is not CertificateKind.SOUNDNESS
        ):
            raise ValueError("support needs soundness evidence")
        if self.presentation is SupportPresentation.FINITE:
            if self.relation is not None:
                raise ValueError("finite support cannot carry an intensional relation")
            expected = cardinality_size(self.cardinality)
            if expected is None or expected != len(self.atoms):
                raise ValueError("finite support cardinality must equal atom count")
            identities = tuple(_atom_identity(atom) for atom in self.atoms)
            if len(identities) != len(set(identities)):
                raise ValueError("finite support repeats a canonical atom identity")
            ordered_pairs = tuple(
                sorted(
                    zip(identities, self.atoms, strict=True),
                    key=lambda item: item[0],
                )
            )
            ordered_identities = tuple(identity for identity, _ in ordered_pairs)
            if ordered_identities != identities:
                object.__setattr__(
                    self,
                    "atoms",
                    tuple(atom for _, atom in ordered_pairs),
                )
        else:
            if self.atoms:
                raise ValueError("intensional support cannot carry enumerated atoms")
            if self.relation is None:
                raise ValueError("intensional support needs a closed relation AST")


def finite_support(
    atoms: tuple[A, ...],
    *,
    label: str = "finite-support",
) -> SupportSpace[A]:
    return SupportSpace(
        SupportPresentation.FINITE,
        atoms,
        None,
        finite_cardinality(len(atoms)),
        _certificate(CertificateKind.COMPLETENESS, f"{label}:complete"),
        _certificate(CertificateKind.SOUNDNESS, f"{label}:sound"),
    )


def intensional_support(
    relation: RuleExpr,
    cardinality: Cardinality,
    *,
    completeness_evidence: Certificate,
    soundness_evidence: Certificate,
) -> SupportSpace[A]:
    return SupportSpace(
        SupportPresentation.INTENSIONAL,
        (),
        relation,
        cardinality,
        completeness_evidence,
        soundness_evidence,
    )


class ProbabilityPresentation(Enum):
    FINITE = "finite"
    INTENSIONAL = "intensional"


@dataclass(frozen=True)
class AtomMass:
    atom_identity: str
    mass: Fraction

    def __post_init__(self) -> None:
        if type(self.atom_identity) is not str or not self.atom_identity:
            raise ValueError("probability mass needs an atom identity")
        if type(self.mass) is not Fraction:
            raise TypeError("probability mass must be an exact Fraction")
        if self.mass <= 0:
            raise ValueError("probability masses must be strictly positive")


@dataclass(frozen=True)
class ProbabilityLaw:
    """An exact normalized law over atoms; never a random draw."""

    presentation: ProbabilityPresentation
    masses: tuple[AtomMass, ...]
    measure: RuleExpr | None
    normalization_evidence: Certificate
    measurable_space_evidence: Certificate
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "probability-law")
        if type(self.presentation) is not ProbabilityPresentation:
            raise TypeError("probability presentation is not recognized")
        if type(self.masses) is not tuple or any(
            type(item) is not AtomMass for item in self.masses
        ):
            raise TypeError("probability masses must be an immutable AtomMass tuple")
        if self.measure is not None and type(self.measure) is not RuleExpr:
            raise TypeError("probability measure must be a RuleExpr or None")
        if (
            type(self.normalization_evidence) is not Certificate
            or self.normalization_evidence.kind is not CertificateKind.NORMALIZATION
        ):
            raise ValueError("probability law needs normalization evidence")
        if (
            type(self.measurable_space_evidence) is not Certificate
            or self.measurable_space_evidence.kind
            is not CertificateKind.MEASURABILITY
        ):
            raise ValueError("probability law needs measurability evidence")
        if self.presentation is ProbabilityPresentation.FINITE:
            if self.measure is not None:
                raise ValueError("finite probability law cannot carry a measure AST")
            if not self.masses:
                raise ValueError("finite probability law cannot be empty")
            identities = tuple(item.atom_identity for item in self.masses)
            if len(identities) != len(set(identities)):
                raise ValueError("finite probability law repeats an atom identity")
            if sum((item.mass for item in self.masses), Fraction(0)) != Fraction(1):
                raise ValueError("finite probability law must normalize exactly to one")
            ordered = tuple(sorted(self.masses, key=lambda item: item.atom_identity))
            ordered_identities = tuple(item.atom_identity for item in ordered)
            if ordered_identities != identities:
                object.__setattr__(self, "masses", ordered)
        else:
            if self.masses:
                raise ValueError("intensional probability law cannot enumerate masses")
            if self.measure is None:
                raise ValueError("intensional probability law needs a measure AST")

    def mass_for(self, atom_identity: str) -> Fraction:
        for item in self.masses:
            if item.atom_identity == atom_identity:
                return item.mass
        return Fraction(0)


@dataclass(frozen=True)
class OutcomeSpace(Generic[A]):
    support: SupportSpace[A]
    probability_law: ProbabilityLaw | None = None
    projection_cardinalities: "ProjectionCardinalities | None" = None
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "outcome-space")
        if type(self.support) is not SupportSpace:
            raise TypeError("outcome support variant is not recognized")
        if self.probability_law is not None and type(
            self.probability_law
        ) is not ProbabilityLaw:
            raise TypeError("outcome probability law is not recognized")
        if self.projection_cardinalities is not None and type(
            self.projection_cardinalities
        ) is not ProjectionCardinalities:
            raise TypeError("outcome projection cardinalities are not recognized")
        if (
            self.projection_cardinalities is not None
            and self.support.presentation is not SupportPresentation.INTENSIONAL
        ):
            raise ValueError(
                "finite supports derive projection cardinalities from their atoms"
            )
        if self.projection_cardinalities is not None:
            _validate_projection_cardinality_claims(
                self.support.cardinality,
                self.projection_cardinalities,
            )
        law = self.probability_law
        if law is None:
            return
        if self.support.presentation is SupportPresentation.FINITE:
            identities = tuple(_atom_identity(atom) for atom in self.support.atoms)
            if set(identities) != {item.atom_identity for item in law.masses}:
                raise ValueError("probability-law support does not equal atom support")
        elif law.presentation is not ProbabilityPresentation.INTENSIONAL:
            raise ValueError("intensional support needs an intensional law")


@dataclass(frozen=True)
class ProjectionCardinalities:
    """Exact cardinalities proved for intensional application projections.

    A source relation may mix derivations and typed no-successor atoms, and
    distinct derivations may quotient to one successor.  These claims are
    therefore independent of the source-atom cardinality and are accepted
    only with closed composition evidence.
    """

    derivations: Cardinality
    no_successors: Cardinality
    successors: Cardinality
    mapping_evidence: Certificate
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "projection cardinalities")
        cardinality_types = (ExactlyZero, ExactlyOne, Many, Undetermined)
        if any(
            type(value) not in cardinality_types
            for value in (
                self.derivations,
                self.no_successors,
                self.successors,
            )
        ):
            raise TypeError("projection cardinality claim is not recognized")
        if (
            type(self.mapping_evidence) is not Certificate
            or self.mapping_evidence.kind is not CertificateKind.COMPOSITION
        ):
            raise ValueError(
                "projection cardinalities need closed composition evidence"
            )


def _validate_projection_cardinality_claims(
    source: Cardinality,
    claims: ProjectionCardinalities,
) -> None:
    """Reject exact projection claims that violate partition/quotient arithmetic."""

    # ``Undetermined`` is an honest absence of a cardinality proof, not an
    # infinite value.  It remains admissible unless the known claims around it
    # force a contradictory bound or exact complement.
    source_shape = _known_cardinality_shape(source)
    derivation_shape = _known_cardinality_shape(claims.derivations)
    no_successor_shape = _known_cardinality_shape(claims.no_successors)
    successor_shape = _known_cardinality_shape(claims.successors)

    raw_partition_shape = _known_cardinality_sum(
        derivation_shape,
        no_successor_shape,
    )
    if (
        source_shape is not None
        and raw_partition_shape is not None
        and source_shape != raw_partition_shape
    ):
        raise ValueError(
            "derivation and no-successor cardinalities do not partition "
            "the source support"
        )

    if source_shape is not None:
        for label, component_shape in (
            ("derivation", derivation_shape),
            ("no-successor", no_successor_shape),
        ):
            if (
                component_shape is not None
                and not _known_cardinality_leq(component_shape, source_shape)
            ):
                raise ValueError(
                    f"{label} cardinality cannot exceed the source support"
                )

    inferred_derivations: list[KnownCardinalityShape] = []
    if successor_shape == ("finite", 0):
        inferred_derivations.append(("finite", 0))
    complement_shape = _known_partition_complement(
        source_shape,
        no_successor_shape,
    )
    if complement_shape is not None:
        inferred_derivations.append(complement_shape)
    if derivation_shape is None and inferred_derivations:
        derivation_shape = inferred_derivations[0]
        if any(
            inferred != derivation_shape
            for inferred in inferred_derivations[1:]
        ):
            raise ValueError(
                "known projection claims force inconsistent derivation "
                "cardinalities"
            )

    partition_shape = _known_cardinality_sum(
        derivation_shape,
        no_successor_shape,
    )
    if (
        source_shape is not None
        and partition_shape is not None
        and source_shape != partition_shape
    ):
        raise ValueError(
            "derivation and no-successor cardinalities do not partition "
            "the source support"
        )

    if derivation_shape is None or successor_shape is None:
        if (
            source_shape is not None
            and successor_shape is not None
            and not _known_cardinality_leq(successor_shape, source_shape)
        ):
            raise ValueError(
                "successor cardinality cannot exceed the source support"
            )
        return
    derivation_kind = derivation_shape[0]
    if derivation_shape == ("finite", 0):
        if successor_shape != ("finite", 0):
            raise ValueError(
                "zero derivations require zero distinct successors"
            )
        return
    if successor_shape == ("finite", 0):
        raise ValueError(
            "nonzero derivations cannot have zero successors"
        )
    if not _known_cardinality_leq(successor_shape, derivation_shape):
        if derivation_kind == "countable":
            raise ValueError(
                "a successor quotient cannot exceed countably many derivations"
            )
        raise ValueError(
            "successor cardinality cannot exceed derivation cardinality"
        )
    if (
        source_shape is not None
        and not _known_cardinality_leq(successor_shape, source_shape)
    ):
        raise ValueError(
            "successor cardinality cannot exceed the source support"
        )


KnownCardinalityShape: TypeAlias = tuple[str, int | None]


def _known_cardinality_shape(
    value: Cardinality,
) -> KnownCardinalityShape | None:
    size = cardinality_size(value)
    if size is not None:
        return ("finite", size)
    if isinstance(value, Many):
        if value.infinite is InfiniteCardinality.COUNTABLY_INFINITE:
            return ("countable", None)
        if value.infinite is InfiniteCardinality.UNCOUNTABLE:
            return ("uncountable", None)
    return None


def _known_cardinality_sum(
    left: KnownCardinalityShape | None,
    right: KnownCardinalityShape | None,
) -> KnownCardinalityShape | None:
    if left is None or right is None:
        return None
    if "uncountable" in (left[0], right[0]):
        return ("uncountable", None)
    if "countable" in (left[0], right[0]):
        return ("countable", None)
    assert left[1] is not None and right[1] is not None
    return ("finite", left[1] + right[1])


def _known_cardinality_leq(
    left: KnownCardinalityShape,
    right: KnownCardinalityShape,
) -> bool:
    if left[0] == "finite":
        if right[0] != "finite":
            return True
        assert left[1] is not None and right[1] is not None
        return left[1] <= right[1]
    if left[0] == "countable":
        return right[0] in ("countable", "uncountable")
    return right[0] == "uncountable"


def _known_partition_complement(
    source: KnownCardinalityShape | None,
    known_part: KnownCardinalityShape | None,
) -> KnownCardinalityShape | None:
    """Return an exact complement only when cardinal arithmetic determines it."""

    if source is None or known_part is None:
        return None
    if not _known_cardinality_leq(known_part, source):
        return None
    source_kind, source_size = source
    part_kind, part_size = known_part
    if source_kind == "finite":
        assert source_size is not None and part_size is not None
        return ("finite", source_size - part_size)
    if source_kind == "countable" and part_kind == "finite":
        return ("countable", None)
    if source_kind == "uncountable" and part_kind in ("finite", "countable"):
        return ("uncountable", None)
    return None


def _atom_identity(atom: object) -> str:
    canonical = getattr(atom, "canonical_identity", None)
    if isinstance(canonical, str) and canonical:
        return canonical
    identity = getattr(atom, "identity", None)
    if isinstance(identity, str) and identity:
        return identity
    return loci.canonical_identity(atom)


def finite_probability_law(
    masses: tuple[tuple[A, Fraction], ...],
) -> ProbabilityLaw:
    return ProbabilityLaw(
        ProbabilityPresentation.FINITE,
        tuple(AtomMass(_atom_identity(atom), Fraction(mass)) for atom, mass in masses),
        None,
        _certificate(CertificateKind.NORMALIZATION, "finite-law:normalized"),
        _certificate(CertificateKind.MEASURABILITY, "finite-law:measurable"),
    )


# ---------------------------------------------------------------------------
# Rule denotation nodes and faults
# ---------------------------------------------------------------------------


class ExistingPlanKind(Enum):
    BY_INDEX = "by-index"
    BY_TARGET = "by-target"
    BY_LOCUS = "by-locus"
    PRESERVE = "preserve"


@dataclass(frozen=True)
class ExistingPlan:
    """Closed construction of all existing-target dispositions."""

    kind: ExistingPlanKind
    expressions: tuple[RuleExpr, ...]
    targets: tuple[loci.Locus, ...] = ()
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "existing-plan")
        if type(self.kind) is not ExistingPlanKind:
            raise TypeError("existing-plan kind is not recognized")
        if type(self.expressions) is not tuple or type(self.targets) is not tuple:
            raise TypeError("existing-plan collections must be immutable tuples")
        if any(type(item) is not RuleExpr for item in self.expressions):
            raise TypeError("existing-plan expressions must be RuleExpr values")
        if any(type(item) is not loci.Locus for item in self.targets):
            raise TypeError("existing-plan targets must be Locus values")
        if self.kind is ExistingPlanKind.BY_TARGET and len(self.expressions) != 1:
            raise ValueError("by-target plan needs exactly one expression")
        if self.kind is ExistingPlanKind.BY_LOCUS:
            if not self.targets or len(self.targets) != len(self.expressions):
                raise ValueError(
                    "by-locus plan needs one target per expression"
                )
            if len(set(self.targets)) != len(self.targets):
                raise ValueError("by-locus targets must be unique")
        elif self.targets:
            raise ValueError("only by-locus plans carry target identities")
        if self.kind is ExistingPlanKind.PRESERVE and (
            self.expressions or self.targets
        ):
            raise ValueError("preserve plan cannot carry expressions or targets")
        if self.kind is ExistingPlanKind.BY_INDEX and not self.expressions:
            raise ValueError("by-index plan cannot be empty")


class EvaluationScope(Enum):
    ONCE = "once"
    EACH_TARGET = "each-target"


@dataclass(frozen=True)
class EvidenceExpression:
    """A closed expression projected into denotation evidence."""

    expression: RuleExpr
    scope: EvaluationScope = EvaluationScope.ONCE
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "evidence-expression")
        if type(self.expression) is not RuleExpr:
            raise TypeError("evidence expression must contain a RuleExpr")
        if type(self.scope) is not EvaluationScope:
            raise TypeError("evidence-expression scope is not recognized")


@dataclass(frozen=True)
class FormattedEvidence:
    """One restricted text rendering of an evaluated exact scalar."""

    template: str
    expression: RuleExpr
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "formatted-evidence")
        if self.template not in ("{}", "0x{:016x}"):
            raise ValueError("formatted evidence uses an unsupported template")
        if type(self.expression) is not RuleExpr:
            raise TypeError("formatted evidence requires a RuleExpr")


@dataclass(frozen=True)
class EvidenceTerm:
    """A closed tree whose expression leaves are evaluated at denotation."""

    tag: str
    arguments: tuple[
        RuleScalar | EvidenceExpression | FormattedEvidence | "EvidenceTerm",
        ...,
    ] = ()
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "evidence-term")
        if type(self.tag) is not str or not self.tag:
            raise ValueError("evidence-term tag must be a nonempty string")
        if type(self.arguments) is not tuple:
            raise TypeError("evidence-term arguments must be an immutable tuple")
        if any(
            not (
                _is_rule_scalar(argument)
                or type(argument)
                in (EvidenceExpression, FormattedEvidence, EvidenceTerm)
            )
            for argument in self.arguments
        ):
            raise TypeError("evidence term contains an opaque argument")


@dataclass(frozen=True)
class ProvenanceTemplate:
    """Restricted scalar formatting over closed evaluated expressions."""

    template: str
    expressions: tuple[RuleExpr, ...]
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "provenance-template")
        if type(self.template) is not str or not self.template:
            raise ValueError("provenance template cannot be empty")
        if type(self.expressions) is not tuple:
            raise TypeError(
                "provenance-template expressions must be an immutable tuple"
            )
        if any(type(item) is not RuleExpr for item in self.expressions):
            raise TypeError("provenance templates require RuleExpr values")
        fields = []
        for _, field_name, format_spec, conversion in Formatter().parse(
            self.template
        ):
            if field_name is None:
                continue
            if conversion is not None or format_spec not in ("", "016x"):
                raise ValueError("unsupported provenance formatting operation")
            if not field_name.isdecimal():
                raise ValueError("provenance fields must use numeric indices")
            fields.append(int(field_name))
        if fields and (
            min(fields) < 0 or max(fields) >= len(self.expressions)
        ):
            raise ValueError("provenance template field is out of range")


@dataclass(frozen=True)
class LiteralDenotation(Generic[V]):
    outcomes: OutcomeSpace[RuleAtom[V]]

    def __post_init__(self) -> None:
        if type(self.outcomes) is not OutcomeSpace:
            raise TypeError("literal denotation needs an OutcomeSpace")


@dataclass(frozen=True)
class ExpressionDenotation:
    existing_plan: ExistingPlan
    progress: Progress
    continuation: Continuation
    witness: RuleExpr
    provenance: Provenance
    certificate: Certificate
    certificate_template: EvidenceTerm | None = None
    provenance_templates: tuple[ProvenanceTemplate, ...] = ()

    def __post_init__(self) -> None:
        if type(self.existing_plan) is not ExistingPlan:
            raise TypeError("expression denotation plan is not recognized")
        if not isinstance(self.progress, Progress):
            raise TypeError("expression progress is not recognized")
        if type(self.continuation) not in (Continue, Stop):
            raise TypeError("expression continuation is not recognized")
        if type(self.witness) is not RuleExpr:
            raise TypeError("expression witness is not recognized")
        if type(self.provenance) is not tuple:
            raise TypeError("expression provenance must be an immutable tuple")
        if (
            not self.provenance
            or any(type(item) is not str or not item for item in self.provenance)
        ):
            raise ValueError("expression provenance must be closed and nonempty")
        if type(self.certificate) is not Certificate:
            raise TypeError("expression certificate is not recognized")
        if self.certificate_template is not None and type(
            self.certificate_template
        ) is not EvidenceTerm:
            raise TypeError("expression certificate template is not recognized")
        if type(self.provenance_templates) is not tuple or any(
            type(item) is not ProvenanceTemplate
            for item in self.provenance_templates
        ):
            raise TypeError("expression provenance templates are not recognized")


@dataclass(frozen=True)
class IntensionalDenotation:
    relation: RuleExpr
    cardinality: Cardinality
    completeness_evidence: Certificate
    soundness_evidence: Certificate
    probability_law: ProbabilityLaw | None = None
    projection_cardinalities: ProjectionCardinalities | None = None

    def __post_init__(self) -> None:
        if type(self.relation) is not RuleExpr:
            raise TypeError("intensional relation must be a RuleExpr")
        if type(self.cardinality) not in (
            ExactlyZero,
            ExactlyOne,
            Many,
            Undetermined,
        ):
            raise TypeError("intensional cardinality is not recognized")
        if (
            type(self.completeness_evidence) is not Certificate
            or self.completeness_evidence.kind
            is not CertificateKind.COMPLETENESS
        ):
            raise ValueError("intensional denotation needs completeness evidence")
        if (
            type(self.soundness_evidence) is not Certificate
            or self.soundness_evidence.kind is not CertificateKind.SOUNDNESS
        ):
            raise ValueError("intensional denotation needs soundness evidence")
        if self.probability_law is not None and type(
            self.probability_law
        ) is not ProbabilityLaw:
            raise TypeError("intensional probability law is not recognized")
        if self.projection_cardinalities is not None and type(
            self.projection_cardinalities
        ) is not ProjectionCardinalities:
            raise TypeError(
                "intensional projection cardinalities are not recognized"
            )


class ClauseSelection(Enum):
    """How an ordered closed clause kernel retains matching clauses."""

    ALL = "all"
    FIRST = "first"


class CapabilitySelectorKind(Enum):
    """Closed ways for a disposition plan to address resolved capabilities."""

    INDEX = "index"
    TARGET = "target"
    EVERY = "every"


@dataclass(frozen=True)
class CapabilitySelector:
    """One closed reference into an existing or fresh capability sequence."""

    kind: CapabilitySelectorKind
    index: int | None = None
    target: loci.Locus | loci.FreshReference | None = None
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "capability selector")
        if type(self.kind) is not CapabilitySelectorKind:
            raise TypeError("capability selector kind is not recognized")
        if self.kind is CapabilitySelectorKind.INDEX:
            if type(self.index) is not int or self.index < 0:
                raise ValueError(
                    "index capability selector needs a non-negative integer"
                )
            if self.target is not None:
                raise ValueError("index capability selector cannot carry a target")
            return
        if self.kind is CapabilitySelectorKind.TARGET:
            if self.index is not None:
                raise ValueError("target capability selector cannot carry an index")
            if type(self.target) not in (loci.Locus, loci.FreshReference):
                raise TypeError(
                    "target capability selector needs a Locus or FreshReference"
                )
            return
        if self.index is not None or self.target is not None:
            raise ValueError("every capability selector carries no index or target")


@dataclass(frozen=True)
class ExistingDispositionPlan:
    """One closed existing-capability action selected by index, identity, or all."""

    selector: CapabilitySelector
    action: DispositionAction
    value: RuleExpr | None = None
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "existing disposition plan")
        if type(self.selector) is not CapabilitySelector:
            raise TypeError("existing disposition selector is not recognized")
        if (
            self.selector.kind is CapabilitySelectorKind.TARGET
            and type(self.selector.target) is not loci.Locus
        ):
            raise TypeError("existing target selector needs a bound Locus")
        if self.action not in (
            DispositionAction.PRESERVE,
            DispositionAction.REPLACE,
            DispositionAction.DELETE,
        ):
            raise ValueError("existing disposition plan has a fresh-only action")
        if self.action is DispositionAction.REPLACE:
            if type(self.value) is not RuleExpr:
                raise TypeError("replace plan needs one closed value expression")
        elif self.value is not None:
            raise ValueError("preserve/delete plans cannot carry a value expression")


@dataclass(frozen=True)
class FreshDispositionPlan:
    """One closed fresh-capability action selected by index, identity, or all."""

    selector: CapabilitySelector
    action: DispositionAction
    value: RuleExpr | None = None
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "fresh disposition plan")
        if type(self.selector) is not CapabilitySelector:
            raise TypeError("fresh disposition selector is not recognized")
        if (
            self.selector.kind is CapabilitySelectorKind.TARGET
            and type(self.selector.target) is not loci.FreshReference
        ):
            raise TypeError("fresh target selector needs a FreshReference")
        if self.action not in (
            DispositionAction.ABSENT,
            DispositionAction.CREATE,
        ):
            raise ValueError("fresh disposition plan has an existing-only action")
        if self.action is DispositionAction.CREATE:
            if type(self.value) is not RuleExpr:
                raise TypeError("create plan needs one closed value expression")
        elif self.value is not None:
            raise ValueError("absent plans cannot carry a value expression")


def _validate_plan_selectors(
    plans: tuple[ExistingDispositionPlan, ...]
    | tuple[FreshDispositionPlan, ...],
    *,
    owner: str,
) -> None:
    if len({plan.selector for plan in plans}) != len(plans):
        raise ValueError(f"{owner} contains duplicate capability selectors")
    if any(
        plan.selector.kind is CapabilitySelectorKind.EVERY for plan in plans
    ) and len(plans) != 1:
        raise ValueError(
            f"{owner} cannot combine an every selector with another selector"
        )


@dataclass(frozen=True)
class DerivationClauseResult:
    """A matched clause's complete, input-dependent derivation plan."""

    existing_plans: tuple[ExistingDispositionPlan, ...]
    fresh_plans: tuple[FreshDispositionPlan, ...]
    progress: Progress
    continuation: Continuation
    witness: RuleExpr
    provenance: Provenance
    certificate: Certificate
    existing_default: DispositionAction = DispositionAction.PRESERVE
    fresh_default: DispositionAction = DispositionAction.ABSENT
    certificate_template: EvidenceTerm | None = None
    provenance_templates: tuple[ProvenanceTemplate, ...] = ()
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "derivation clause result")
        if type(self.existing_plans) is not tuple or any(
            type(plan) is not ExistingDispositionPlan
            for plan in self.existing_plans
        ):
            raise TypeError(
                "derivation existing plans must be an immutable plan tuple"
            )
        if type(self.fresh_plans) is not tuple or any(
            type(plan) is not FreshDispositionPlan for plan in self.fresh_plans
        ):
            raise TypeError("derivation fresh plans must be an immutable plan tuple")
        _validate_plan_selectors(self.existing_plans, owner="existing plans")
        _validate_plan_selectors(self.fresh_plans, owner="fresh plans")
        if type(self.progress) is not Progress:
            raise TypeError("derivation clause progress is not recognized")
        if type(self.continuation) not in (Continue, Stop):
            raise TypeError("derivation clause continuation is not recognized")
        if type(self.witness) is not RuleExpr:
            raise TypeError("derivation clause witness is not recognized")
        if type(self.provenance) is not tuple or not self.provenance or any(
            type(item) is not str or not item for item in self.provenance
        ):
            raise ValueError(
                "derivation clause provenance must be a nonempty immutable tuple"
            )
        if (
            type(self.certificate) is not Certificate
            or self.certificate.kind is not CertificateKind.DERIVATION
        ):
            raise ValueError("derivation clause needs derivation evidence")
        if self.existing_default is not DispositionAction.PRESERVE:
            raise ValueError("existing clause default must explicitly Preserve")
        if self.fresh_default is not DispositionAction.ABSENT:
            raise ValueError("fresh clause default must explicitly Absent")
        if self.certificate_template is not None and type(
            self.certificate_template
        ) is not EvidenceTerm:
            raise TypeError("derivation clause certificate template is not recognized")
        if type(self.provenance_templates) is not tuple or any(
            type(item) is not ProvenanceTemplate
            for item in self.provenance_templates
        ):
            raise TypeError(
                "derivation clause provenance templates are not recognized"
            )


@dataclass(frozen=True)
class NoSuccessorClauseResult:
    """A matched clause's typed, input-dependent no-successor result."""

    outcome: NoSuccessorOutcome
    reason: RuleExpr
    witness: RuleExpr
    provenance: Provenance
    certificate: Certificate
    certificate_template: EvidenceTerm | None = None
    provenance_templates: tuple[ProvenanceTemplate, ...] = ()
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "no-successor clause result")
        if type(self.outcome) is not NoSuccessorOutcome:
            raise TypeError("no-successor clause outcome is not recognized")
        if type(self.reason) is not RuleExpr:
            raise TypeError("no-successor clause reason is not recognized")
        if type(self.witness) is not RuleExpr:
            raise TypeError("no-successor clause witness is not recognized")
        if type(self.provenance) is not tuple or not self.provenance or any(
            type(item) is not str or not item for item in self.provenance
        ):
            raise ValueError(
                "no-successor clause provenance must be a nonempty immutable tuple"
            )
        expected = (
            CertificateKind.DIVERGENCE
            if self.outcome is NoSuccessorOutcome.DIVERGENT
            else CertificateKind.TERMINALITY
        )
        if (
            type(self.certificate) is not Certificate
            or self.certificate.kind is not expected
        ):
            raise ValueError(
                f"{self.outcome.value} clause needs {expected.value} evidence"
            )
        if self.certificate_template is not None and type(
            self.certificate_template
        ) is not EvidenceTerm:
            raise TypeError(
                "no-successor clause certificate template is not recognized"
            )
        if type(self.provenance_templates) is not tuple or any(
            type(item) is not ProvenanceTemplate
            for item in self.provenance_templates
        ):
            raise TypeError(
                "no-successor clause provenance templates are not recognized"
            )


ClauseResult: TypeAlias = DerivationClauseResult | NoSuccessorClauseResult


@dataclass(frozen=True)
class RuleClause:
    """One ordered closed predicate/result branch in a reusable Rule kernel."""

    condition: RuleExpr
    result: ClauseResult
    mass: Fraction | None = None
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "Rule clause")
        if type(self.condition) is not RuleExpr:
            raise TypeError("Rule clause condition is not recognized")
        if type(self.result) not in (
            DerivationClauseResult,
            NoSuccessorClauseResult,
        ):
            raise TypeError("Rule clause result is not recognized")
        if self.mass is not None:
            if type(self.mass) is not Fraction:
                raise TypeError("Rule clause mass must be an exact Fraction")
            if self.mass <= 0:
                raise ValueError("Rule clause mass must be strictly positive")


@dataclass(frozen=True)
class ClauseKernelDenotation:
    """An ordered finite clause relation evaluated over one immutable ``(R, W)``."""

    clauses: tuple[RuleClause, ...]
    selection: ClauseSelection
    completeness_evidence: Certificate
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "clause-kernel denotation")
        if type(self.clauses) is not tuple or any(
            type(clause) is not RuleClause for clause in self.clauses
        ):
            raise TypeError("clause kernel needs an immutable RuleClause tuple")
        if not self.clauses:
            raise ValueError("clause kernel needs at least one clause")
        if type(self.selection) is not ClauseSelection:
            raise TypeError("clause-kernel selection is not recognized")
        if (
            type(self.completeness_evidence) is not Certificate
            or self.completeness_evidence.kind is not CertificateKind.COMPLETENESS
        ):
            raise ValueError("clause kernel needs completeness evidence")
        weighted = tuple(clause.mass is not None for clause in self.clauses)
        if any(weighted) and not all(weighted):
            raise ValueError(
                "clause-kernel masses must be present on every clause or none"
            )


@dataclass(frozen=True)
class ParallelDenotation(Generic[R, W, C]):
    parts: tuple["Rule[R, W, C]", ...]

    def __post_init__(self) -> None:
        if type(self.parts) is not tuple:
            raise TypeError("parallel Rule parts must be an immutable tuple")
        if not self.parts:
            raise ValueError("parallel Rule needs at least one part")
        if any(type(part) is not Rule for part in self.parts):
            raise TypeError("parallel Rule parts must be recognized Rules")


RuleDenotation: TypeAlias = (
    LiteralDenotation[alphabets.SemanticValue]
    | ExpressionDenotation
    | ClauseKernelDenotation
    | IntensionalDenotation
    | ParallelDenotation[R, W, C]
)


@dataclass(frozen=True)
class RuleDescriptor(Generic[R, W, C]):
    primitive: RulePrimitive
    denotation: RuleDenotation[R, W, C]
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "Rule descriptor")
        if not isinstance(self.primitive, RulePrimitive):
            raise TypeError("Rule primitive is not recognized")
        expected = {
            RulePrimitive.LITERAL: LiteralDenotation,
            RulePrimitive.EXPRESSION: ExpressionDenotation,
            RulePrimitive.CLAUSE_KERNEL: ClauseKernelDenotation,
            RulePrimitive.RELATION: IntensionalDenotation,
            RulePrimitive.DISTRIBUTION: IntensionalDenotation,
            RulePrimitive.DIFFERENTIAL: IntensionalDenotation,
            RulePrimitive.PARALLEL: ParallelDenotation,
        }[self.primitive]
        if not isinstance(self.denotation, expected):
            raise ValueError("Rule primitive and denotation variant disagree")

    @property
    def canonical_identity(self) -> str:
        return loci.canonical_identity(self)


class RuleFaultPhase(Enum):
    DENOTATION = "rule-denotation"
    RESULT_VALIDATION = "result-validation"
    COMPOSITION = "composition"


class RuleFaultReason(Enum):
    INVALID_DESCRIPTOR = "invalid-descriptor"
    INCOMPATIBLE_READ_VIEW = "incompatible-read-view"
    INCOMPATIBLE_WRITABLE = "incompatible-writable"
    EVALUATION_FAILURE = "evaluation-failure"
    NO_MATCHING_CLAUSE = "no-matching-clause"
    INCOMPLETE_DISPOSITION = "incomplete-disposition"
    UNAUTHORIZED_EFFECT = "unauthorized-effect"
    CONFLICTING_EFFECT = "conflicting-effect"
    INVALID_PROBABILITY_LAW = "invalid-probability-law"
    UNSUPPORTED_EXACTNESS = "unsupported-exactness"


@dataclass(frozen=True)
class RuleFault:
    phase: RuleFaultPhase
    reason: RuleFaultReason
    evidence: tuple[Certificate, ...]
    detail: str
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "Rule fault")
        if type(self.phase) is not RuleFaultPhase:
            raise TypeError("Rule fault phase is not recognized")
        if type(self.reason) is not RuleFaultReason:
            raise TypeError("Rule fault reason is not recognized")
        if type(self.evidence) is not tuple or any(
            type(item) is not Certificate for item in self.evidence
        ):
            raise TypeError("Rule fault evidence must be a Certificate tuple")
        if not self.evidence:
            raise ValueError("Rule fault needs closed evidence")
        if type(self.detail) is not str or not self.detail:
            raise ValueError("Rule fault detail cannot be empty")


@dataclass(frozen=True)
class RuleRejected:
    fault: RuleFault

    def __post_init__(self) -> None:
        if type(self.fault) is not RuleFault:
            raise TypeError("RuleRejected fault variant is not recognized")


@dataclass(frozen=True)
class RuleComplete(Generic[C, V]):
    outcome_space: OutcomeSpace[RuleAtom[V]]

    def __post_init__(self) -> None:
        if type(self.outcome_space) is not OutcomeSpace:
            raise TypeError("RuleComplete outcome space is not recognized")
        support = self.outcome_space.support
        if (
            support.presentation is SupportPresentation.FINITE
            and any(type(atom) not in (Derivation, NoSuccessor) for atom in support.atoms)
        ):
            raise TypeError("RuleComplete support contains an unknown atom variant")


RuleResult: TypeAlias = RuleComplete[C, V] | RuleRejected


class _Observation(Protocol):
    target: loci.Locus
    value: alphabets.SemanticValue
    state: object


class _GroupKey(Protocol):
    anchor: loci.Locus | None
    channel: int


class _ObservationGroup(Protocol):
    key: _GroupKey
    indices: tuple[int, ...]


class _ReadableView(Protocol):
    observations: tuple[_Observation, ...]
    groups: tuple[_ObservationGroup, ...]


class _ExistingCapability(Protocol):
    target: loci.Locus


class _FreshCapability(Protocol):
    target: loci.FreshReference


class _WritableCapabilities(Protocol):
    existing: tuple[_ExistingCapability, ...]
    fresh: tuple[_FreshCapability, ...]


@dataclass(frozen=True)
class Rule(Generic[R, W, C]):
    """A frozen closed denotation plus immutable compatibility declarations."""

    descriptor: RuleDescriptor[R, W, C]
    contract: RuleContract

    def __post_init__(self) -> None:
        if type(self.descriptor) is not RuleDescriptor:
            raise TypeError("Rule descriptor is not recognized")
        if type(self.contract) is not RuleContract:
            raise TypeError("Rule contract is not recognized")

    @property
    def canonical_identity(self) -> str:
        return loci.canonical_identity((self.descriptor, self.contract))

    def denote(self, readable: R, writable: W) -> RuleResult[C, alphabets.SemanticValue]:
        """Interpret only this module's sealed AST over the supplied ``R``/``W``."""

        try:
            view = cast(_ReadableView, readable)
            envelope = cast(_WritableCapabilities, writable)
            # Access eagerly so malformed structural records reject at this boundary.
            tuple(view.observations)
            tuple(view.groups)
            tuple(envelope.existing)
            tuple(envelope.fresh)
            return _denote_descriptor(self.descriptor, view, envelope)
        except (IndexError, KeyError, TypeError, ValueError) as exc:
            return _rejected(
                RuleFaultPhase.DENOTATION,
                RuleFaultReason.EVALUATION_FAILURE,
                f"{type(exc).__name__}: {exc}",
            )


def _rejected(
    phase: RuleFaultPhase,
    reason: RuleFaultReason,
    detail: str,
) -> RuleRejected:
    return RuleRejected(
        RuleFault(
            phase,
            reason,
            (_certificate(CertificateKind.CONFORMANCE, detail),),
            detail,
        )
    )


def _denote_descriptor(
    descriptor: RuleDescriptor[R, W, C],
    readable: _ReadableView,
    writable: _WritableCapabilities,
) -> RuleResult[C, alphabets.SemanticValue]:
    denotation = descriptor.denotation
    if isinstance(denotation, LiteralDenotation):
        return RuleComplete(denotation.outcomes)
    if isinstance(denotation, ExpressionDenotation):
        return _denote_expression(denotation, readable, writable)
    if isinstance(denotation, ClauseKernelDenotation):
        return _denote_clause_kernel(denotation, readable, writable)
    if isinstance(denotation, IntensionalDenotation):
        support: SupportSpace[RuleAtom[alphabets.SemanticValue]] = (
            intensional_support(
                denotation.relation,
                denotation.cardinality,
                completeness_evidence=denotation.completeness_evidence,
                soundness_evidence=denotation.soundness_evidence,
            )
        )
        return RuleComplete(
            OutcomeSpace(
                support,
                denotation.probability_law,
                denotation.projection_cardinalities,
            )
        )
    if isinstance(denotation, ParallelDenotation):
        return _denote_parallel(denotation, readable, writable)
    return _rejected(
        RuleFaultPhase.DENOTATION,
        RuleFaultReason.INVALID_DESCRIPTOR,
        "unknown closed Rule denotation variant",
    )


def _denote_expression(
    denotation: ExpressionDenotation,
    readable: _ReadableView,
    writable: _WritableCapabilities,
) -> RuleResult[C, alphabets.SemanticValue]:
    existing_targets = tuple(item.target for item in writable.existing)
    fresh_targets = tuple(item.target for item in writable.fresh)
    plan = denotation.existing_plan
    proofs: list[EvaluationProof] = []

    def evaluate(
        expression: RuleExpr,
        *,
        anchor: loci.Locus | None,
    ) -> RuleRuntimeValue:
        value, proof = _evaluate_proven(
            expression,
            readable,
            anchor=anchor,
        )
        proofs.append(proof)
        return value

    if plan.kind is ExistingPlanKind.PRESERVE:
        existing = tuple(preserve(target) for target in existing_targets)
    elif plan.kind is ExistingPlanKind.BY_INDEX:
        if len(plan.expressions) != len(existing_targets):
            return _rejected(
                RuleFaultPhase.RESULT_VALIDATION,
                RuleFaultReason.INCOMPLETE_DISPOSITION,
                "by-index expression count does not equal existing capability count",
            )
        existing = tuple(
            replace(
                target,
                _require_semantic_value(
                    evaluate(expression, anchor=None)
                ),
            )
            for target, expression in zip(
                existing_targets,
                plan.expressions,
                strict=True,
            )
        )
    elif plan.kind is ExistingPlanKind.BY_TARGET:
        expression = plan.expressions[0]
        existing = tuple(
            replace(
                target,
                _require_semantic_value(
                    evaluate(expression, anchor=target)
                ),
            )
            for target in existing_targets
        )
    else:
        expression_by_target = dict(
            zip(plan.targets, plan.expressions, strict=True)
        )
        if set(expression_by_target) != set(existing_targets):
            return _rejected(
                RuleFaultPhase.RESULT_VALIDATION,
                RuleFaultReason.INCOMPLETE_DISPOSITION,
                "by-locus plan targets do not equal existing capabilities",
            )
        existing = tuple(
            replace(
                target,
                _require_semantic_value(
                    evaluate(
                        expression_by_target[target],
                        anchor=target,
                    )
                ),
            )
            for target in existing_targets
        )

    fresh = tuple(absent(target) for target in fresh_targets)
    total = TotalDisposition(
        existing,
        fresh,
        _certificate(CertificateKind.TOTALITY, "expression-plan:total"),
    )
    if denotation.certificate_template is None:
        certificate = denotation.certificate
    else:
        certificate = Certificate(
            denotation.certificate.kind,
            _materialize_evidence_term(
                denotation.certificate_template,
                readable,
                existing_targets,
                proofs,
            ),
        )
    dynamic_provenance = tuple(
        _materialize_provenance(
            template,
            readable,
            proofs,
        )
        for template in denotation.provenance_templates
    )
    boundary_provenance = _boundary_provenance(readable)
    provenance = (
        denotation.provenance
        if not boundary_provenance
        else (
            denotation.provenance[0],
            *boundary_provenance,
            *denotation.provenance[1:],
        )
    )
    provenance = (*provenance, *dynamic_provenance)
    proof_expression = (
        _evaluation_proofs_as_expr(tuple(proofs))
        if proofs
        else RuleExpr(
            ExpressionPrimitive.TUPLE,
            (literal_expr("evaluation-proof-v1"),),
        )
    )
    witness_descriptor = RuleExpr(
        ExpressionPrimitive.TUPLE,
        (
            denotation.witness,
            proof_expression,
            literal_expr(total.canonical_identity),
        ),
    )
    witness = Witness(
        identity=loci.canonical_identity(witness_descriptor),
        descriptor=witness_descriptor,
    )
    atom = Derivation(
        total,
        denotation.progress,
        denotation.continuation,
        witness,
        provenance,
        certificate,
    )
    return RuleComplete(OutcomeSpace(finite_support((atom,), label="expression")))


DispositionPlan: TypeAlias = ExistingDispositionPlan | FreshDispositionPlan


def _capability_indices(
    selector: CapabilitySelector,
    targets: tuple[loci.Locus | loci.FreshReference, ...],
) -> tuple[int, ...]:
    if selector.kind is CapabilitySelectorKind.EVERY:
        return tuple(range(len(targets)))
    if selector.kind is CapabilitySelectorKind.INDEX:
        assert selector.index is not None
        if selector.index >= len(targets):
            raise IndexError(
                f"capability index {selector.index} is outside resolved envelope"
            )
        return (selector.index,)
    assert selector.target is not None
    try:
        return (targets.index(selector.target),)
    except ValueError as error:
        raise KeyError(
            "capability target identity is absent from resolved envelope"
        ) from error


def _plans_by_index(
    plans: tuple[DispositionPlan, ...],
    targets: tuple[loci.Locus | loci.FreshReference, ...],
) -> dict[int, DispositionPlan]:
    selected: dict[int, DispositionPlan] = {}
    for plan in plans:
        for index in _capability_indices(plan.selector, targets):
            if index in selected:
                raise ValueError(
                    "disposition plans overlap on one resolved capability"
                )
            selected[index] = plan
    return selected


def _materialize_clause_provenance(
    provenance: Provenance,
    templates: tuple[ProvenanceTemplate, ...],
    readable: _ReadableView,
    proofs: list[EvaluationProof],
) -> Provenance:
    dynamic = tuple(
        _materialize_provenance(template, readable, proofs)
        for template in templates
    )
    boundary = _boundary_provenance(readable)
    base = (
        provenance
        if not boundary
        else (provenance[0], *boundary, *provenance[1:])
    )
    return (*base, *dynamic)


def _materialize_clause_derivation(
    result: DerivationClauseResult,
    *,
    clause_index: int,
    selection_proofs: tuple[EvaluationProof, ...],
    readable: _ReadableView,
    writable: _WritableCapabilities,
) -> Derivation[alphabets.SemanticValue]:
    existing_targets = tuple(item.target for item in writable.existing)
    fresh_targets = tuple(item.target for item in writable.fresh)
    proofs = list(selection_proofs)

    def evaluate(
        expression: RuleExpr,
        *,
        anchor: loci.Locus | None,
        target: loci.Locus | loci.FreshReference | None = None,
    ) -> RuleRuntimeValue:
        value, proof = _evaluate_proven(
            expression,
            readable,
            anchor=anchor,
            target=target,
        )
        proofs.append(proof)
        return value

    existing_plans = _plans_by_index(
        tuple(result.existing_plans),
        tuple(existing_targets),
    )
    existing: list[Disposition[loci.Locus, alphabets.SemanticValue]] = []
    for index, target in enumerate(existing_targets):
        plan = existing_plans.get(index)
        if plan is None or plan.action is DispositionAction.PRESERVE:
            existing.append(preserve(target))
        elif plan.action is DispositionAction.DELETE:
            existing.append(delete(target))
        else:
            assert plan.action is DispositionAction.REPLACE
            assert plan.value is not None
            existing.append(
                replace(
                    target,
                    _require_semantic_value(
                        evaluate(plan.value, anchor=target)
                    ),
                )
            )

    fresh_plans = _plans_by_index(
        tuple(result.fresh_plans),
        tuple(fresh_targets),
    )
    fresh: list[Disposition[loci.FreshReference, alphabets.SemanticValue]] = []
    for index, target in enumerate(fresh_targets):
        plan = fresh_plans.get(index)
        if plan is None or plan.action is DispositionAction.ABSENT:
            fresh.append(absent(target))
        else:
            assert plan.action is DispositionAction.CREATE
            assert plan.value is not None
            fresh.append(
                create(
                    target,
                    _require_semantic_value(
                        evaluate(
                            plan.value,
                            anchor=None,
                            target=target,
                        )
                    ),
                )
            )

    total = TotalDisposition(
        tuple(existing),
        tuple(fresh),
        _certificate(
            CertificateKind.TOTALITY,
            f"clause-kernel:{clause_index}:total",
        ),
    )
    continuation = result.continuation
    if isinstance(continuation, Stop):
        continuation = Stop(
            _runtime_as_expr(evaluate(continuation.reason, anchor=None)),
            continuation.certificate,
        )
    witness_value = evaluate(result.witness, anchor=None)
    certificate = (
        result.certificate
        if result.certificate_template is None
        else Certificate(
            result.certificate.kind,
            _materialize_evidence_term(
                result.certificate_template,
                readable,
                existing_targets,
                proofs,
            ),
        )
    )
    provenance = _materialize_clause_provenance(
        result.provenance,
        result.provenance_templates,
        readable,
        proofs,
    )
    proof_expression = _evaluation_proofs_as_expr(tuple(proofs))
    witness_descriptor = RuleExpr(
        ExpressionPrimitive.TUPLE,
        (
            literal_expr("clause-kernel-witness-v1"),
            literal_expr(clause_index),
            result.witness,
            _runtime_as_expr(witness_value),
            proof_expression,
            literal_expr(total.canonical_identity),
        ),
    )
    return Derivation(
        total,
        result.progress,
        continuation,
        Witness(
            loci.canonical_identity(witness_descriptor),
            witness_descriptor,
        ),
        provenance,
        certificate,
    )


def _materialize_clause_no_successor(
    result: NoSuccessorClauseResult,
    *,
    clause_index: int,
    selection_proofs: tuple[EvaluationProof, ...],
    readable: _ReadableView,
    writable: _WritableCapabilities,
) -> NoSuccessor:
    existing_targets = tuple(item.target for item in writable.existing)
    proofs = list(selection_proofs)

    def evaluate(expression: RuleExpr) -> RuleRuntimeValue:
        value, proof = _evaluate_proven(expression, readable, anchor=None)
        proofs.append(proof)
        return value

    reason = _runtime_as_expr(evaluate(result.reason))
    witness_value = evaluate(result.witness)
    certificate = (
        result.certificate
        if result.certificate_template is None
        else Certificate(
            result.certificate.kind,
            _materialize_evidence_term(
                result.certificate_template,
                readable,
                existing_targets,
                proofs,
            ),
        )
    )
    provenance = _materialize_clause_provenance(
        result.provenance,
        result.provenance_templates,
        readable,
        proofs,
    )
    proof_expression = _evaluation_proofs_as_expr(tuple(proofs))
    witness_descriptor = RuleExpr(
        ExpressionPrimitive.TUPLE,
        (
            literal_expr("clause-kernel-witness-v1"),
            literal_expr(clause_index),
            literal_expr(result.outcome.value),
            result.witness,
            _runtime_as_expr(witness_value),
            reason,
            proof_expression,
        ),
    )
    return NoSuccessor(
        result.outcome,
        reason,
        Witness(
            loci.canonical_identity(witness_descriptor),
            witness_descriptor,
        ),
        provenance,
        certificate,
    )


def _denote_clause_kernel(
    denotation: ClauseKernelDenotation,
    readable: _ReadableView,
    writable: _WritableCapabilities,
) -> RuleResult[C, alphabets.SemanticValue]:
    selected: list[tuple[int, RuleClause]] = []
    selection_proofs: list[EvaluationProof] = []
    for index, clause in enumerate(denotation.clauses):
        condition, proof = _evaluate_proven(
            clause.condition,
            readable,
            anchor=None,
        )
        selection_proofs.append(proof)
        if _require_bit(condition):
            selected.append((index, clause))
            if denotation.selection is ClauseSelection.FIRST:
                break

    if not selected:
        return _rejected(
            RuleFaultPhase.DENOTATION,
            RuleFaultReason.NO_MATCHING_CLAUSE,
            "complete clause kernel had no matching typed outcome",
        )

    atoms: list[RuleAtom[alphabets.SemanticValue]] = []
    masses: list[Fraction] = []
    retained_selection_proofs = tuple(selection_proofs)
    for index, clause in selected:
        if isinstance(clause.result, DerivationClauseResult):
            atom: RuleAtom[alphabets.SemanticValue] = (
                _materialize_clause_derivation(
                    clause.result,
                    clause_index=index,
                    selection_proofs=retained_selection_proofs,
                    readable=readable,
                    writable=writable,
                )
            )
        else:
            atom = _materialize_clause_no_successor(
                clause.result,
                clause_index=index,
                selection_proofs=retained_selection_proofs,
                readable=readable,
                writable=writable,
            )
        atoms.append(atom)
        if clause.mass is not None:
            masses.append(clause.mass)

    try:
        support = finite_support(tuple(atoms), label="clause-kernel")
    except (TypeError, ValueError) as error:
        return _rejected(
            RuleFaultPhase.RESULT_VALIDATION,
            RuleFaultReason.INVALID_DESCRIPTOR,
            f"invalid clause-kernel support: {error}",
        )
    probability_law: ProbabilityLaw | None = None
    if masses:
        try:
            probability_law = finite_probability_law(
                tuple(zip(atoms, masses, strict=True))
            )
        except (TypeError, ValueError) as error:
            return _rejected(
                RuleFaultPhase.RESULT_VALIDATION,
                RuleFaultReason.INVALID_PROBABILITY_LAW,
                f"invalid clause-kernel probability law: {error}",
            )
    return RuleComplete(OutcomeSpace(support, probability_law))


def _materialize_evidence_term(
    term: EvidenceTerm,
    readable: _ReadableView,
    existing_targets: tuple[loci.Locus, ...],
    proofs: list[EvaluationProof],
) -> RuleExpr:
    arguments: list[RuleExpr] = [literal_expr(term.tag)]
    for argument in term.arguments:
        if isinstance(argument, EvidenceTerm):
            arguments.append(
                _materialize_evidence_term(
                    argument,
                    readable,
                    existing_targets,
                    proofs,
                )
            )
        elif isinstance(argument, EvidenceExpression):
            anchors: tuple[loci.Locus | None, ...] = (
                (None,)
                if argument.scope is EvaluationScope.ONCE
                else existing_targets
            )
            for anchor in anchors:
                value, proof = _evaluate_proven(
                    argument.expression,
                    readable,
                    anchor=anchor,
                )
                proofs.append(proof)
                arguments.append(_runtime_as_expr(value))
        elif isinstance(argument, FormattedEvidence):
            value, proof = _evaluate_proven(
                argument.expression,
                readable,
                anchor=None,
            )
            proofs.append(proof)
            if isinstance(value, tuple):
                raise TypeError("formatted evidence expression must be scalar")
            normalized = int(value) if isinstance(value, bool) else value
            arguments.append(literal_expr(argument.template.format(normalized)))
        else:
            arguments.append(literal_expr(argument))
    return RuleExpr(ExpressionPrimitive.TUPLE, tuple(arguments))


def _materialize_provenance(
    template: ProvenanceTemplate,
    readable: _ReadableView,
    proofs: list[EvaluationProof],
) -> str:
    values: list[RuleScalar] = []
    for expression in template.expressions:
        value, proof = _evaluate_proven(expression, readable, anchor=None)
        proofs.append(proof)
        if isinstance(value, tuple):
            raise TypeError("provenance template expression must be scalar")
        values.append(int(value) if isinstance(value, bool) else value)
    return template.template.format(*values)


def _boundary_provenance(readable: _ReadableView) -> tuple[str, ...]:
    boundaries = tuple(
        item.state.boundary
        for item in readable.observations
        if isinstance(item.state, neighborhoods.BoundaryDefault)
    )
    unique = tuple(dict.fromkeys(boundaries))
    tags: list[str] = []
    for boundary in unique:
        if boundary.policy is loci.BoundaryPolicy.FIXED:
            exterior = boundary.exterior
            if exterior is False or exterior == 0:
                suffix = "fixed-zero"
            elif exterior is True or exterior == 1:
                suffix = "fixed-one"
            else:
                suffix = "fixed-" + loci.canonical_identity(exterior)
        else:
            suffix = boundary.policy.value
        tags.append(f"configuration-topology:{suffix}")
    return tuple(tags)


def _denote_parallel(
    denotation: ParallelDenotation[R, W, C],
    readable: _ReadableView,
    writable: _WritableCapabilities,
) -> RuleResult[C, alphabets.SemanticValue]:
    parts: list[Derivation[alphabets.SemanticValue]] = []
    for rule in denotation.parts:
        result = rule.denote(cast(R, readable), cast(W, writable))
        if isinstance(result, RuleRejected):
            return result
        support = result.outcome_space.support
        if (
            support.presentation is not SupportPresentation.FINITE
            or len(support.atoms) != 1
            or not isinstance(support.atoms[0], Derivation)
            or result.outcome_space.probability_law is not None
        ):
            return _rejected(
                RuleFaultPhase.COMPOSITION,
                RuleFaultReason.UNSUPPORTED_EXACTNESS,
                "parallel currently requires deterministic finite derivation parts",
            )
        parts.append(support.atoms[0])

    merged = _merge_dispositions(tuple(parts))
    if isinstance(merged, RuleRejected):
        return merged
    progress = (
        Progress.ADVANCED
        if any(part.progress is Progress.ADVANCED for part in parts)
        else Progress.QUIESCENT
    )
    continuation: Continuation = Continue()
    stops = tuple(
        part.continuation
        for part in parts
        if isinstance(part.continuation, Stop)
    )
    if stops:
        if len(set(stops)) != 1:
            return _rejected(
                RuleFaultPhase.COMPOSITION,
                RuleFaultReason.CONFLICTING_EFFECT,
                "parallel parts declare incompatible stopping reasons",
            )
        continuation = stops[0]
    witness_expr = RuleExpr(
        ExpressionPrimitive.TUPLE,
        tuple(part.witness.descriptor for part in parts),
    )
    atom = Derivation(
        merged,
        progress,
        continuation,
        Witness(loci.canonical_identity(witness_expr), witness_expr),
        tuple(item for part in parts for item in part.provenance),
        _certificate(CertificateKind.COMPOSITION, "parallel:closed-product"),
    )
    return RuleComplete(OutcomeSpace(finite_support((atom,), label="parallel")))


def _merge_dispositions(
    parts: tuple[Derivation[alphabets.SemanticValue], ...],
) -> TotalDisposition[alphabets.SemanticValue] | RuleRejected:
    if not parts:
        return _rejected(
            RuleFaultPhase.COMPOSITION,
            RuleFaultReason.INVALID_DESCRIPTOR,
            "parallel derivation product cannot be empty",
        )
    first = parts[0].replacement
    existing: list[Disposition[loci.Locus, alphabets.SemanticValue]] = []
    fresh: list[
        Disposition[loci.FreshReference, alphabets.SemanticValue]
    ] = []
    for index in range(len(first.existing)):
        candidates = tuple(part.replacement.existing[index] for part in parts)
        if len({item.target for item in candidates}) != 1:
            return _rejected(
                RuleFaultPhase.COMPOSITION,
                RuleFaultReason.INCOMPATIBLE_WRITABLE,
                "parallel existing-target order disagrees",
            )
        active = tuple(
            item
            for item in candidates
            if item.action is not DispositionAction.PRESERVE
        )
        if not active:
            existing.append(candidates[0])
        elif len(set(active)) == 1:
            existing.append(active[0])
        else:
            return _rejected(
                RuleFaultPhase.COMPOSITION,
                RuleFaultReason.CONFLICTING_EFFECT,
                "parallel existing-target effects conflict",
            )
    for index in range(len(first.fresh)):
        candidates = tuple(part.replacement.fresh[index] for part in parts)
        if len({item.target for item in candidates}) != 1:
            return _rejected(
                RuleFaultPhase.COMPOSITION,
                RuleFaultReason.INCOMPATIBLE_WRITABLE,
                "parallel fresh-target order disagrees",
            )
        active = tuple(
            item
            for item in candidates
            if item.action is not DispositionAction.ABSENT
        )
        if not active:
            fresh.append(candidates[0])
        elif len(set(active)) == 1:
            fresh.append(active[0])
        else:
            return _rejected(
                RuleFaultPhase.COMPOSITION,
                RuleFaultReason.CONFLICTING_EFFECT,
                "parallel fresh-target effects conflict",
            )
    return TotalDisposition(
        tuple(existing),
        tuple(fresh),
        _certificate(CertificateKind.TOTALITY, "parallel:merged-total"),
    )


@dataclass(frozen=True)
class EvaluationStep:
    """One exact postorder step in a closed expression evaluation."""

    expression: RuleExpr
    anchor: loci.Locus | None
    result: RuleRuntimeValue
    read_evidence: tuple[str, ...] = ()
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "evaluation-step")
        if type(self.expression) is not RuleExpr:
            raise TypeError("evaluation step expression is not recognized")
        if self.anchor is not None and type(self.anchor) is not loci.Locus:
            raise TypeError("evaluation step anchor must be a Locus or None")
        if not _is_rule_runtime_value(self.result):
            raise TypeError("evaluation step result is not a closed runtime value")
        if type(self.read_evidence) is not tuple or any(
            type(item) is not str or not item for item in self.read_evidence
        ):
            raise TypeError(
                "evaluation step read evidence must be a nonempty-string tuple"
            )


@dataclass(frozen=True)
class EvaluationProof:
    """Complete closed evaluation trace for one top-level expression."""

    steps: tuple[EvaluationStep, ...]
    version: int = 1

    def __post_init__(self) -> None:
        _require_version_one(self.version, "evaluation-proof")
        if type(self.steps) is not tuple or any(
            type(step) is not EvaluationStep for step in self.steps
        ):
            raise TypeError("evaluation proof steps must be an EvaluationStep tuple")
        if not self.steps:
            raise ValueError("evaluation proof cannot be empty")


def _is_rule_runtime_value(value: object) -> bool:
    if _is_rule_scalar(value):
        return True
    return type(value) is tuple and all(
        _is_rule_runtime_value(item) for item in value
    )


def _evaluate(
    expression: RuleExpr,
    readable: _ReadableView,
    *,
    anchor: loci.Locus | None,
    target: loci.Locus | loci.FreshReference | None = None,
) -> RuleRuntimeValue:
    result, _ = _evaluate_proven(
        expression,
        readable,
        anchor=anchor,
        target=target,
    )
    return result


def _evaluate_proven(
    expression: RuleExpr,
    readable: _ReadableView,
    *,
    anchor: loci.Locus | None,
    target: loci.Locus | loci.FreshReference | None = None,
) -> tuple[RuleRuntimeValue, EvaluationProof]:
    steps: list[EvaluationStep] = []
    result = _evaluate_value(
        expression,
        readable,
        anchor=anchor,
        target=anchor if target is None else target,
        bindings=(),
        steps=steps,
    )
    return result, EvaluationProof(tuple(steps))


def _evaluate_value(
    expression: RuleExpr,
    readable: _ReadableView,
    *,
    anchor: loci.Locus | None,
    target: loci.Locus | loci.FreshReference | None,
    bindings: _BindingContext,
    steps: list[EvaluationStep],
) -> RuleRuntimeValue:
    def evaluate(child: RuleExpr) -> RuleRuntimeValue:
        return _evaluate_value(
            child,
            readable,
            anchor=anchor,
            target=target,
            bindings=bindings,
            steps=steps,
        )

    def evaluate_bound(
        child: RuleExpr,
        value: RuleRuntimeValue,
        index: int,
    ) -> RuleRuntimeValue:
        return _evaluate_value(
            child,
            readable,
            anchor=anchor,
            target=target,
            bindings=((value, index), *bindings),
            steps=steps,
        )

    def finish(
        result: RuleRuntimeValue,
        read_evidence: tuple[str, ...] = (),
    ) -> RuleRuntimeValue:
        steps.append(
            EvaluationStep(
                expression,
                anchor,
                result,
                read_evidence,
            )
        )
        return result

    primitive = expression.primitive
    arguments = expression.arguments
    if primitive is ExpressionPrimitive.LITERAL:
        if len(arguments) != 1 or isinstance(arguments[0], RuleExpr):
            raise ValueError("literal expression is malformed")
        return finish(arguments[0])
    if primitive is ExpressionPrimitive.OBSERVATION:
        index = _literal_int(arguments, 0)
        item = readable.observations[index]
        return finish(
            item.value,
            _observation_evidence((item,)),
        )
    if primitive is ExpressionPrimitive.GROUP:
        channel = _literal_int(arguments, 0)
        items = tuple(
            readable.observations[index]
            for index in _group_indices(readable, anchor, channel)
        )
        return finish(
            tuple(item.value for item in items),
            _observation_evidence(items),
        )
    if primitive is ExpressionPrimitive.TARGET_REFERENCE:
        if target is None:
            raise ValueError(
                "target-reference expression requires a writable-target context"
            )
        return finish(alphabets.StructuralReference(target))
    if primitive in (
        ExpressionPrimitive.BOUND_VALUE,
        ExpressionPrimitive.BOUND_INDEX,
    ):
        depth = _literal_int(arguments, 0)
        if depth >= len(bindings):
            raise IndexError(
                f"lexical binding depth {depth} is outside the active context"
            )
        value, index = bindings[depth]
        evidence = _binding_read_evidence(
            primitive,
            depth,
            bindings,
        )
        return finish(
            value
            if primitive is ExpressionPrimitive.BOUND_VALUE
            else index,
            evidence,
        )
    if primitive is ExpressionPrimitive.PROJECT:
        source = evaluate(_child(arguments, 0))
        if not isinstance(source, tuple):
            raise TypeError("project source is not tuple-valued")
        return finish(source[_literal_int(arguments, 1)])
    if primitive is ExpressionPrimitive.TUPLE:
        return finish(tuple(
            evaluate(_as_expression(argument))
            for argument in arguments
        ))
    if primitive is ExpressionPrimitive.RECORD_FIELD:
        source = _require_value_node(
            evaluate(_child(arguments, 0)),
            alphabets.ValueKind.RECORD,
            owner="record-field",
        )
        field = _literal_str(arguments, 1)
        fields_by_name = dict(source.fields)
        if field not in fields_by_name:
            raise KeyError(f"record field {field!r} is absent")
        return finish(fields_by_name[field])
    if primitive is ExpressionPrimitive.RECORD_UPDATE:
        source = _require_value_node(
            evaluate(_child(arguments, 0)),
            alphabets.ValueKind.RECORD,
            owner="record-update",
        )
        field = _literal_str(arguments, 1)
        fields_by_name = dict(source.fields)
        if field not in fields_by_name:
            raise KeyError(f"record field {field!r} is absent")
        fields_by_name[field] = _require_semantic_value(
            evaluate(_child(arguments, 2))
        )
        return finish(
            alphabets.ValueNode(
                alphabets.ValueKind.RECORD,
                source.tag,
                fields=tuple(fields_by_name.items()),
                version=source.version,
            )
        )
    if primitive is ExpressionPrimitive.LENGTH:
        items, _ = _sequence_items(evaluate(_child(arguments, 0)))
        return finish(len(items))
    if primitive is ExpressionPrimitive.ITEM_AT:
        items, _ = _sequence_items(evaluate(_child(arguments, 0)))
        index = _require_strict_int(evaluate(_child(arguments, 1)))
        if 0 <= index < len(items):
            return finish(_require_semantic_value(items[index]))
        return finish(
            _require_semantic_value(evaluate(_child(arguments, 2)))
        )
    if primitive is ExpressionPrimitive.SLICE:
        items, tag = _sequence_items(evaluate(_child(arguments, 0)))
        start = _require_strict_int(evaluate(_child(arguments, 1)))
        stop = _require_strict_int(evaluate(_child(arguments, 2)))
        if start < 0 or stop < start or stop > len(items):
            raise IndexError(
                "slice bounds must satisfy 0 <= start <= stop <= length"
            )
        return finish(_word_from_items(items[start:stop], tag=tag))
    if primitive is ExpressionPrimitive.CONCATENATE:
        sequences = tuple(
            _sequence_items(evaluate(_as_expression(argument)))
            for argument in arguments
        )
        tags = tuple(tag for _, tag in sequences if tag is not None)
        if tags and any(tag != tags[0] for tag in tags[1:]):
            raise ValueError(
                "concatenated semantic words must carry one common tag"
            )
        combined = tuple(
            item
            for items, _ in sequences
            for item in items
        )
        return finish(
            _word_from_items(
                combined,
                tag=tags[0] if tags else None,
            )
        )
    if primitive is ExpressionPrimitive.REVERSE:
        items, tag = _sequence_items(evaluate(_child(arguments, 0)))
        return finish(_word_from_items(tuple(reversed(items)), tag=tag))
    if primitive is ExpressionPrimitive.REPLACE_AT:
        items, tag = _sequence_items(evaluate(_child(arguments, 0)))
        index = _require_strict_int(evaluate(_child(arguments, 1)))
        if index < 0 or index >= len(items):
            raise IndexError("replace-at index is outside the sequence")
        replacement = _require_semantic_value(
            evaluate(_child(arguments, 2))
        )
        updated = (*items[:index], replacement, *items[index + 1 :])
        return finish(_word_from_items(updated, tag=tag))
    if primitive is ExpressionPrimitive.MAP_LOOKUP:
        entries = _association_entries(evaluate(_child(arguments, 0)))
        key = _require_semantic_value(evaluate(_child(arguments, 1)))
        found = _association_lookup(entries, key)
        if found is not None:
            return finish(found)
        return finish(
            _require_semantic_value(evaluate(_child(arguments, 2)))
        )
    if primitive is ExpressionPrimitive.MAP_UPDATE:
        source = _require_value_node(
            evaluate(_child(arguments, 0)),
            alphabets.ValueKind.MAP,
            owner="map-update",
        )
        entries = alphabets.map_entries(source)
        key = _require_semantic_value(evaluate(_child(arguments, 1)))
        value = _require_semantic_value(evaluate(_child(arguments, 2)))
        updated: list[
            tuple[alphabets.SemanticValue, alphabets.SemanticValue]
        ] = []
        replaced = False
        for old_key, old_value in entries:
            if alphabets.semantic_equal(old_key, key):
                updated.append((key, value))
                replaced = True
            else:
                updated.append((old_key, old_value))
        if not replaced:
            updated.append((key, value))
        return finish(
            alphabets.map_value(
                tuple(
                    alphabets.map_entry_value(
                        entry_key,
                        entry_value,
                    )
                    for entry_key, entry_value in updated
                ),
                tag=source.tag,
            )
        )
    if primitive is ExpressionPrimitive.INDEX_OF:
        items, _ = _sequence_items(evaluate(_child(arguments, 0)))
        needle = _require_semantic_value(evaluate(_child(arguments, 1)))
        for index, item in enumerate(items):
            semantic_item = _require_semantic_value(item)
            if alphabets.semantic_equal(semantic_item, needle):
                return finish(index)
        return finish(
            _require_strict_int(evaluate(_child(arguments, 2)))
        )
    if primitive is ExpressionPrimitive.INDEX_OF_TAG:
        items, _ = _sequence_items(evaluate(_child(arguments, 0)))
        tag = _literal_str(arguments, 1)
        for index, item in enumerate(items):
            if type(item) is alphabets.ValueNode and item.tag == tag:
                return finish(index)
        return finish(
            _require_strict_int(evaluate(_child(arguments, 2)))
        )
    if primitive is ExpressionPrimitive.PRODUCT_VALUE:
        tag = _literal_str(arguments, 0)
        items = tuple(
            _require_semantic_value(evaluate(_as_expression(argument)))
            for argument in arguments[1:]
        )
        return finish(
            alphabets.ValueNode(
                alphabets.ValueKind.PRODUCT,
                tag,
                items=items,
            )
        )
    if primitive is ExpressionPrimitive.WORD_VALUE:
        tag = _literal_str(arguments, 0)
        items = tuple(
            _require_semantic_value(evaluate(_as_expression(argument)))
            for argument in arguments[1:]
        )
        return finish(
            alphabets.ValueNode(
                alphabets.ValueKind.WORD,
                tag,
                items=items,
            )
        )
    if primitive is ExpressionPrimitive.FLAT_MAP_LOOKUP:
        source = _require_value_node(
            evaluate(_child(arguments, 0)),
            alphabets.ValueKind.WORD,
            owner="flat-map-lookup",
        )
        entries = _association_entries(evaluate(_child(arguments, 1)))
        output: list[alphabets.SemanticValue] = []
        for item in source.items:
            mapped = _association_lookup(entries, item)
            if mapped is None:
                raise KeyError(
                    "flat-map lookup table is not total on the source word"
                )
            mapped_word = _require_value_node(
                mapped,
                alphabets.ValueKind.WORD,
                owner="flat-map-lookup result",
            )
            if mapped_word.tag != source.tag:
                raise ValueError(
                    "flat-map result word tag disagrees with source word tag"
                )
            output.extend(mapped_word.items)
        return finish(
            alphabets.ValueNode(
                alphabets.ValueKind.WORD,
                source.tag,
                items=tuple(output),
            )
        )
    if primitive is ExpressionPrimitive.MAP_ITEMS:
        items, _ = _sequence_items(evaluate(_child(arguments, 0)))
        body = _child(arguments, 1)
        output_tag = _literal_str(arguments, 2)
        output = tuple(
            _require_semantic_value(
                evaluate_bound(body, item, index)
            )
            for index, item in enumerate(items)
        )
        return finish(
            alphabets.ValueNode(
                alphabets.ValueKind.WORD,
                output_tag,
                items=output,
            )
        )
    if primitive is ExpressionPrimitive.FILTER_ITEMS:
        items, tag = _sequence_items(evaluate(_child(arguments, 0)))
        semantic_items = tuple(
            _require_semantic_value(item) for item in items
        )
        predicate = _child(arguments, 1)
        retained: list[alphabets.SemanticValue] = []
        for index, item in enumerate(semantic_items):
            if _require_bit(evaluate_bound(predicate, item, index)):
                retained.append(item)
        return finish(_word_from_items(tuple(retained), tag=tag))
    if primitive is ExpressionPrimitive.FLAT_MAP_ITEMS:
        items, _ = _sequence_items(evaluate(_child(arguments, 0)))
        body = _child(arguments, 1)
        output_tag = _literal_str(arguments, 2)
        output: list[alphabets.SemanticValue] = []
        for index, item in enumerate(items):
            mapped = _require_value_node(
                evaluate_bound(body, item, index),
                alphabets.ValueKind.WORD,
                owner="flat-map-items body",
            )
            if mapped.tag != output_tag:
                raise ValueError(
                    "flat-map-items body word tag disagrees with output tag"
                )
            output.extend(mapped.items)
        return finish(
            alphabets.ValueNode(
                alphabets.ValueKind.WORD,
                output_tag,
                items=tuple(output),
            )
        )
    if primitive is ExpressionPrimitive.SLIDING_WINDOWS:
        items, tag = _sequence_items(evaluate(_child(arguments, 0)))
        semantic_items = tuple(
            _require_semantic_value(item) for item in items
        )
        before = _literal_int(arguments, 1)
        after = _literal_int(arguments, 2)
        boundary = SequenceBoundary(_literal_str(arguments, 3))
        output_tag = "word" if tag is None else tag
        if not semantic_items:
            return finish(
                alphabets.ValueNode(
                    alphabets.ValueKind.WORD,
                    output_tag,
                )
            )
        exterior: alphabets.SemanticValue | None = None
        if (
            boundary is SequenceBoundary.FIXED
            and (before or after)
        ):
            exterior = _require_semantic_value(
                evaluate(_child(arguments, 4))
            )
        windows: list[alphabets.ValueNode] = []
        size = len(semantic_items)
        for anchor_index in range(size):
            window: list[alphabets.SemanticValue] = []
            for raw_index in range(
                anchor_index - before,
                anchor_index + after + 1,
            ):
                if 0 <= raw_index < size:
                    window.append(semantic_items[raw_index])
                elif boundary is SequenceBoundary.FIXED:
                    assert exterior is not None
                    window.append(exterior)
                elif boundary is SequenceBoundary.PERIODIC:
                    window.append(semantic_items[raw_index % size])
                else:
                    window.append(
                        semantic_items[
                            _reflect_sequence_index(raw_index, size)
                        ]
                    )
            windows.append(
                alphabets.ValueNode(
                    alphabets.ValueKind.WORD,
                    output_tag,
                    items=tuple(window),
                )
            )
        return finish(
            alphabets.ValueNode(
                alphabets.ValueKind.WORD,
                output_tag,
                items=tuple(windows),
            )
        )
    if primitive in (ExpressionPrimitive.ADD, ExpressionPrimitive.MULTIPLY):
        values = tuple(
            _require_exact_number(evaluate(_as_expression(argument)))
            for argument in arguments
        )
        if primitive is ExpressionPrimitive.ADD:
            return finish(sum(values))
        product: int | Fraction = 1
        for value in values:
            product *= value
        return finish(product)
    if primitive in (ExpressionPrimitive.SUBTRACT, ExpressionPrimitive.DIVIDE):
        left = _require_exact_number(evaluate(_child(arguments, 0)))
        right = _require_exact_number(evaluate(_child(arguments, 1)))
        if primitive is ExpressionPrimitive.SUBTRACT:
            return finish(left - right)
        if right == 0:
            raise ZeroDivisionError("division expression denominator is zero")
        return finish(Fraction(left, right))
    if primitive is ExpressionPrimitive.FLOOR_DIVIDE:
        left = _require_strict_exact_number(evaluate(_child(arguments, 0)))
        right = _require_strict_exact_number(evaluate(_child(arguments, 1)))
        if right == 0:
            raise ZeroDivisionError(
                "floor-divide expression denominator is zero"
            )
        quotient = Fraction(left) / Fraction(right)
        return finish(quotient.numerator // quotient.denominator)
    if primitive is ExpressionPrimitive.ABSOLUTE:
        value = _require_strict_exact_number(evaluate(_child(arguments, 0)))
        return finish(abs(value))
    if primitive is ExpressionPrimitive.FRACTIONAL_PART:
        value = _require_strict_exact_number(evaluate(_child(arguments, 0)))
        return finish(value - int(value))
    if primitive is ExpressionPrimitive.MODULO:
        value = _require_int(evaluate(_child(arguments, 0)))
        modulus_value = _literal_int(arguments, 1)
        if modulus_value <= 0:
            raise ValueError("modulo expression needs positive modulus")
        return finish(value % modulus_value)
    if primitive is ExpressionPrimitive.INTEGER_DIGITS:
        value = _require_strict_int(evaluate(_child(arguments, 0)))
        if value < 0:
            raise ValueError(
                "integer-digits expression requires a nonnegative value"
            )
        base = _literal_int(arguments, 1)
        width = (
            None
            if len(arguments) == 2
            else (
                _require_strict_int(evaluate(_child(arguments, 2)))
                if type(arguments[2]) is RuleExpr
                else _literal_int(arguments, 2)
            )
        )
        if width is not None and width <= 0:
            raise ValueError(
                "integer-digits expression width must evaluate positive"
            )
        digits = _integer_digit_values(value, base)
        if width is not None:
            if len(digits) > width:
                raise OverflowError(
                    "integer value does not fit the declared digit width"
                )
            digits = (0,) * (width - len(digits)) + digits
        return finish(
            alphabets.ValueNode(
                alphabets.ValueKind.WORD,
                "digits",
                items=digits,
            )
        )
    if primitive is ExpressionPrimitive.FROM_DIGITS:
        items, _ = _sequence_items(evaluate(_child(arguments, 0)))
        if not items:
            raise ValueError("from-digits expression needs a nonempty word")
        base = _literal_int(arguments, 1)
        value = 0
        for item in items:
            digit = _require_strict_int(item)
            if digit < 0 or digit >= base:
                raise ValueError(
                    "digit lies outside the declared positional base"
                )
            value = value * base + digit
        return finish(value)
    if primitive is ExpressionPrimitive.MAXIMAL_RUNS:
        items, _ = _sequence_items(evaluate(_child(arguments, 0)))
        semantic_items = tuple(
            _require_semantic_value(item) for item in items
        )
        runs: list[alphabets.ValueNode] = []
        start = 0
        while start < len(semantic_items):
            stop = start + 1
            while (
                stop < len(semantic_items)
                and alphabets.semantic_equal(
                    semantic_items[start],
                    semantic_items[stop],
                )
            ):
                stop += 1
            runs.append(
                alphabets.ValueNode(
                    alphabets.ValueKind.RECORD,
                    "run",
                    fields=(
                        ("value", semantic_items[start]),
                        ("start", start),
                        ("length", stop - start),
                    ),
                )
            )
            start = stop
        return finish(
            alphabets.ValueNode(
                alphabets.ValueKind.WORD,
                "runs",
                items=tuple(runs),
            )
        )
    if primitive is ExpressionPrimitive.COUNT:
        values = _require_tuple(evaluate(_child(arguments, 0)))
        return finish(sum(1 for value in values if _require_bit(value) == 1))
    if primitive is ExpressionPrimitive.GATE:
        source = evaluate(_child(arguments, 0))
        threshold = _literal_int(arguments, 2)
        gate_name = _literal_str(arguments, 1)
        values = source if isinstance(source, tuple) else (source,)
        total = sum(_require_bit(value) for value in values)
        kind = GateKind(gate_name)
        if kind is GateKind.ANY:
            return finish(int(total > 0))
        if kind is GateKind.ALL:
            return finish(int(total == len(values)))
        if kind is GateKind.MAJORITY:
            return finish(int(total * 2 > len(values)))
        if kind is GateKind.AT_LEAST:
            return finish(int(total >= threshold))
        if kind is GateKind.AT_MOST:
            return finish(int(total <= threshold))
        return finish(int(total == threshold))
    if primitive is ExpressionPrimitive.LOOKUP:
        table = _require_tuple(evaluate(_child(arguments, 0)))
        index = _require_int(evaluate(_child(arguments, 1)))
        return finish(table[index])
    if primitive is ExpressionPrimitive.EQUAL:
        left = evaluate(_child(arguments, 0))
        right = evaluate(_child(arguments, 1))
        return finish(_runtime_equal(left, right))
    if primitive in (ExpressionPrimitive.LESS, ExpressionPrimitive.LESS_EQUAL):
        left = _require_exact_number(evaluate(_child(arguments, 0)))
        right = _require_exact_number(evaluate(_child(arguments, 1)))
        if primitive is ExpressionPrimitive.LESS:
            return finish(int(left < right))
        return finish(int(left <= right))
    if primitive is ExpressionPrimitive.CONDITIONAL:
        condition = _require_bit(evaluate(_child(arguments, 0)))
        selected = _child(arguments, 1 if condition else 2)
        return finish(evaluate(selected))
    if primitive in (ExpressionPrimitive.ALL, ExpressionPrimitive.ANY):
        values = _require_tuple(evaluate(_child(arguments, 0)))
        bits = tuple(_require_bit(value) for value in values)
        return finish(
            int(all(bits))
            if primitive is ExpressionPrimitive.ALL
            else int(any(bits))
        )
    raise ValueError(f"unsupported expression primitive {primitive.value}")


def _observation_evidence(
    observations: tuple[_Observation, ...],
) -> tuple[str, ...]:
    evidence: list[str] = []
    for item in observations:
        state = item.state
        state_identity = loci.canonical_identity(state)
        evidence.append(
            loci.canonical_identity((item.target, state_identity))
        )
    return tuple(evidence)


def _binding_read_evidence(
    primitive: ExpressionPrimitive,
    depth: int,
    bindings: _BindingContext,
) -> tuple[str, ...]:
    """Identify one exact lexical frame read without adding a proof-node type."""

    return (
        loci.canonical_identity(
            (
                "rule-expression-binding",
                primitive.value,
                depth,
                bindings,
            )
        ),
    )


def _runtime_as_expr(value: RuleRuntimeValue) -> RuleExpr:
    if isinstance(value, tuple):
        return RuleExpr(
            ExpressionPrimitive.TUPLE,
            tuple(_runtime_as_expr(item) for item in value),
        )
    return literal_expr(value)


def _evaluation_proofs_as_expr(
    proofs: tuple[EvaluationProof, ...],
) -> RuleExpr:
    steps = tuple(step for proof in proofs for step in proof.steps)
    return RuleExpr(
        ExpressionPrimitive.TUPLE,
        (
            literal_expr("evaluation-proof-v1"),
            *(
                RuleExpr(
                    ExpressionPrimitive.TUPLE,
                    (
                        literal_expr("step"),
                        literal_expr(
                            "none"
                            if step.anchor is None
                            else loci.canonical_identity(step.anchor)
                        ),
                        step.expression,
                        _runtime_as_expr(step.result),
                        RuleExpr(
                            ExpressionPrimitive.TUPLE,
                            (
                                literal_expr("read-evidence"),
                                *(
                                    literal_expr(item)
                                    for item in step.read_evidence
                                ),
                            ),
                        ),
                    ),
                )
                for step in steps
            ),
        ),
    )


def _group_indices(
    readable: _ReadableView,
    anchor: loci.Locus | None,
    channel: int,
) -> tuple[int, ...]:
    matches = tuple(
        item.indices
        for item in readable.groups
        if item.key.channel == channel
        and (anchor is None or item.key.anchor == anchor)
    )
    if len(matches) != 1:
        raise ValueError(
            f"read group {(anchor, channel)!r} resolved {len(matches)} times"
        )
    return matches[0]


def _as_expression(value: RuleScalar | RuleExpr) -> RuleExpr:
    return value if isinstance(value, RuleExpr) else literal_expr(value)


def _child(
    arguments: tuple[RuleScalar | RuleExpr, ...],
    index: int,
) -> RuleExpr:
    value = arguments[index]
    if not isinstance(value, RuleExpr):
        raise TypeError("expected a child Rule expression")
    return value


def _literal_int(
    arguments: tuple[RuleScalar | RuleExpr, ...],
    index: int,
) -> int:
    value = arguments[index]
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("expected an integer Rule literal")
    return value


def _literal_str(
    arguments: tuple[RuleScalar | RuleExpr, ...],
    index: int,
) -> str:
    value = arguments[index]
    if not isinstance(value, str):
        raise TypeError("expected a string Rule literal")
    return value


def _require_tuple(value: RuleRuntimeValue) -> tuple[RuleRuntimeValue, ...]:
    if not isinstance(value, tuple):
        raise TypeError("expected tuple-valued Rule expression")
    return value


def _require_int(value: RuleRuntimeValue) -> int:
    if isinstance(value, bool):
        return int(value)
    if not isinstance(value, int):
        raise TypeError("expected integer Rule expression")
    return value


def _require_exact_number(value: RuleRuntimeValue) -> int | Fraction:
    if isinstance(value, bool):
        return int(value)
    if type(value) not in (int, Fraction):
        raise TypeError("expected exact numeric Rule expression")
    return value


def _require_bit(value: RuleRuntimeValue) -> int:
    integer = _require_int(value)
    if integer not in (0, 1):
        raise ValueError("expected a binary Rule value")
    return integer


def _require_semantic_value(
    value: RuleRuntimeValue,
) -> alphabets.SemanticValue:
    if isinstance(
        value,
        (
            bool,
            int,
            Fraction,
            str,
            alphabets.AlgebraicNumber,
            alphabets.ExactComplex,
            alphabets.StructuralReference,
            alphabets.RepresentedNumber,
            alphabets.ValueNode,
        ),
    ):
        return value
    raise TypeError("Rule expression did not produce one semantic value")


def _require_strict_int(value: RuleRuntimeValue) -> int:
    if type(value) is not int:
        raise TypeError("expected a non-Boolean integer Rule expression")
    return value


def _require_strict_exact_number(
    value: RuleRuntimeValue,
) -> int | Fraction:
    if type(value) not in (int, Fraction):
        raise TypeError(
            "expected a non-Boolean exact numeric Rule expression"
        )
    return value


def _require_value_node(
    value: RuleRuntimeValue,
    kind: alphabets.ValueKind,
    *,
    owner: str,
) -> alphabets.ValueNode:
    if type(value) is not alphabets.ValueNode or value.kind is not kind:
        raise TypeError(
            f"{owner} requires a semantic {kind.value} ValueNode"
        )
    return value


def _sequence_items(
    value: RuleRuntimeValue,
) -> tuple[tuple[RuleRuntimeValue, ...], str | None]:
    if type(value) is tuple:
        return value, None
    word = _require_value_node(
        value,
        alphabets.ValueKind.WORD,
        owner="sequence operation",
    )
    return word.items, word.tag


def _word_from_items(
    items: tuple[RuleRuntimeValue, ...],
    *,
    tag: str | None,
) -> alphabets.ValueNode:
    semantic_items = tuple(
        _require_semantic_value(item) for item in items
    )
    return alphabets.ValueNode(
        alphabets.ValueKind.WORD,
        "word" if tag is None else tag,
        items=semantic_items,
    )


def _reflect_sequence_index(index: int, size: int) -> int:
    """Reflect an integer index without repeating either finite endpoint."""

    if type(index) is not int or type(size) is not int or size <= 0:
        raise ValueError("reflected sequence indices require one positive size")
    if size == 1:
        return 0
    period = 2 * (size - 1)
    offset = index % period
    return period - offset if offset >= size else offset


def _association_entries(
    value: RuleRuntimeValue,
) -> tuple[tuple[alphabets.SemanticValue, alphabets.SemanticValue], ...]:
    association = _require_value_node(
        value,
        alphabets.ValueKind.MAP,
        owner="map operation",
    )
    return alphabets.map_entries(association)


def _association_lookup(
    entries: tuple[
        tuple[alphabets.SemanticValue, alphabets.SemanticValue],
        ...,
    ],
    key: alphabets.SemanticValue,
) -> alphabets.SemanticValue | None:
    for candidate, value in entries:
        if alphabets.semantic_equal(candidate, key):
            return value
    return None


def _runtime_equal(
    left: RuleRuntimeValue,
    right: RuleRuntimeValue,
) -> bool:
    """Compare runtime tuples recursively and semantic leaves by alphabet law."""

    if type(left) is tuple or type(right) is tuple:
        if type(left) is not tuple or type(right) is not tuple:
            return False
        return len(left) == len(right) and all(
            _runtime_equal(left_item, right_item)
            for left_item, right_item in zip(left, right, strict=True)
        )
    return alphabets.semantic_equal(
        _require_semantic_value(left),
        _require_semantic_value(right),
    )


def _integer_digit_values(value: int, base: int) -> tuple[int, ...]:
    if type(value) is not int or value < 0:
        raise ValueError("digit encoding needs a nonnegative integer")
    if type(base) is not int or base < 2:
        raise ValueError("digit encoding base must be an integer >= 2")
    if value == 0:
        return (0,)
    reversed_digits: list[int] = []
    remaining = value
    while remaining:
        remaining, digit = divmod(remaining, base)
        reversed_digits.append(digit)
    return tuple(reversed(reversed_digits))


# ---------------------------------------------------------------------------
# General constructors and closed composition
# ---------------------------------------------------------------------------


def literal(
    outcomes: OutcomeSpace[RuleAtom[alphabets.SemanticValue]],
    *,
    contract: RuleContract,
) -> Rule[R, W, C]:
    """Build a Rule whose complete closed atom space is already supplied."""

    if (
        outcomes.support.presentation is SupportPresentation.FINITE
        and not outcomes.support.atoms
    ):
        raise ValueError(
            "a complete finite Rule result cannot be a bare empty support"
        )
    descriptor: RuleDescriptor[R, W, C] = RuleDescriptor(
        RulePrimitive.LITERAL,
        LiteralDenotation(outcomes),
    )
    return Rule(descriptor, contract)


def expression(
    existing_plan: ExistingPlan,
    *,
    contract: RuleContract,
    witness: RuleExpr,
    provenance: Provenance,
    progress: Progress = Progress.ADVANCED,
    continuation: Continuation = Continue(),
    certificate: Certificate | None = None,
    certificate_template: EvidenceTerm | None = None,
    provenance_templates: tuple[ProvenanceTemplate, ...] = (),
) -> Rule[R, W, C]:
    """Build one deterministic closed expression-to-disposition Rule."""

    if not provenance:
        raise ValueError("expression Rule provenance cannot be empty")
    descriptor: RuleDescriptor[R, W, C] = RuleDescriptor(
        RulePrimitive.EXPRESSION,
        ExpressionDenotation(
            existing_plan,
            progress,
            continuation,
            witness,
            provenance,
            certificate
            or _certificate(CertificateKind.DERIVATION, "expression:verified"),
            certificate_template,
            provenance_templates,
        ),
    )
    return Rule(descriptor, contract)


def clause_kernel(
    clauses: tuple[RuleClause, ...],
    *,
    contract: RuleContract,
    completeness_evidence: Certificate,
    selection: ClauseSelection = ClauseSelection.ALL,
) -> Rule[R, W, C]:
    """Build an ordered, closed, input-dependent finite Rule relation.

    Every matched clause denotes one typed outcome. ``ALL`` retains every
    match; ``FIRST`` retains only the first. A semantic fallback is therefore
    an explicit final always-true clause, not interpreter policy.
    """

    if type(contract) is not RuleContract:
        raise TypeError("clause kernel contract is not recognized")
    denotation = ClauseKernelDenotation(
        clauses,
        selection,
        completeness_evidence,
    )
    required_existing: set[frontiers.Effect] = set()
    required_fresh: set[frontiers.Effect] = set()
    for clause in clauses:
        result = clause.result
        if not isinstance(result, DerivationClauseResult):
            continue
        for plan in result.existing_plans:
            if plan.action is DispositionAction.REPLACE:
                required_existing.add(frontiers.Effect.REPLACE)
            elif plan.action is DispositionAction.DELETE:
                required_existing.add(frontiers.Effect.DELETE)
        if any(
            plan.action is DispositionAction.CREATE
            for plan in result.fresh_plans
        ):
            required_fresh.add(frontiers.Effect.CREATE)
    declared = contract.required_effect_profile
    if not required_existing.issubset(declared.existing):
        missing = required_existing.difference(declared.existing)
        raise ValueError(
            "clause kernel contract omits required existing effects: "
            + ", ".join(sorted(effect.value for effect in missing))
        )
    if not required_fresh.issubset(declared.fresh):
        missing = required_fresh.difference(declared.fresh)
        raise ValueError(
            "clause kernel contract omits required fresh effects: "
            + ", ".join(sorted(effect.value for effect in missing))
        )
    if (
        any(clause.mass is not None for clause in clauses)
        and contract.entropy_interface
        is not seeds.EntropyInterface.REPLAY_KEY
    ):
        raise ValueError(
            "probabilistic clause kernel requires a replay-key entropy interface"
        )
    descriptor: RuleDescriptor[R, W, C] = RuleDescriptor(
        RulePrimitive.CLAUSE_KERNEL,
        denotation,
    )
    return Rule(descriptor, contract)


def relation(
    relation_ast: RuleExpr,
    cardinality: Cardinality,
    *,
    contract: RuleContract,
    completeness_evidence: Certificate,
    soundness_evidence: Certificate,
    projection_cardinalities: ProjectionCardinalities | None = None,
) -> Rule[R, W, C]:
    """Build a complete intensional atom relation without running a solver."""

    descriptor: RuleDescriptor[R, W, C] = RuleDescriptor(
        RulePrimitive.RELATION,
        IntensionalDenotation(
            relation_ast,
            cardinality,
            completeness_evidence,
            soundness_evidence,
            projection_cardinalities=projection_cardinalities,
        ),
    )
    return Rule(descriptor, contract)


def distribution(
    relation_ast: RuleExpr,
    cardinality: Cardinality,
    law: ProbabilityLaw,
    *,
    contract: RuleContract,
    completeness_evidence: Certificate,
    soundness_evidence: Certificate,
    projection_cardinalities: ProjectionCardinalities | None = None,
) -> Rule[R, W, C]:
    """Build an intensional law-valued Rule without drawing from the law."""

    if law.presentation is not ProbabilityPresentation.INTENSIONAL:
        raise ValueError("intensional distribution requires an intensional law")
    descriptor: RuleDescriptor[R, W, C] = RuleDescriptor(
        RulePrimitive.DISTRIBUTION,
        IntensionalDenotation(
            relation_ast,
            cardinality,
            completeness_evidence,
            soundness_evidence,
            law,
            projection_cardinalities,
        ),
    )
    return Rule(descriptor, contract)


def differential(
    relation_ast: RuleExpr,
    cardinality: Cardinality,
    *,
    contract: RuleContract,
    completeness_evidence: Certificate,
    soundness_evidence: Certificate,
    projection_cardinalities: ProjectionCardinalities | None = None,
) -> Rule[R, W, C]:
    """Build an exact/intensional differential solution relation."""

    descriptor: RuleDescriptor[R, W, C] = RuleDescriptor(
        RulePrimitive.DIFFERENTIAL,
        IntensionalDenotation(
            relation_ast,
            cardinality,
            completeness_evidence,
            soundness_evidence,
            projection_cardinalities=projection_cardinalities,
        ),
    )
    return Rule(descriptor, contract)


def parallel(parts: tuple[Rule[R, W, C], ...]) -> Rule[R, W, C]:
    """Compose deterministic effects over one immutable ``(R, W)`` binding."""

    if not parts:
        raise ValueError("parallel requires at least one Rule")
    contract = parts[0].contract
    if any(part.contract != contract for part in parts[1:]):
        raise ValueError("parallel Rule contracts must be identical")
    descriptor: RuleDescriptor[R, W, C] = RuleDescriptor(
        RulePrimitive.PARALLEL,
        ParallelDenotation(parts),
    )
    return Rule(descriptor, contract)


def finite_rule(
    atoms: tuple[RuleAtom[alphabets.SemanticValue], ...],
    *,
    contract: RuleContract,
    probability_law: ProbabilityLaw | None = None,
    label: str = "finite-rule",
) -> Rule[R, W, C]:
    """Convenience constructor for closed finite zero/one/many fixtures."""

    if not atoms:
        raise ValueError("finite Rule needs a typed atom; bare empty is invalid")
    return literal(
        OutcomeSpace(finite_support(atoms, label=label), probability_law),
        contract=contract,
    )


# ---------------------------------------------------------------------------
# Retained native component presets, compiled from concrete construction data
# ---------------------------------------------------------------------------


def _native_contract(
    carrier: loci.CarrierContract,
    *,
    readable: neighborhoods.ReadableRegion[object, object],
    value_profile: alphabets.ValueProfile = alphabets.ValueProfile.BOOLEAN,
) -> RuleContract:
    return RuleContract(
        configuration_contract=carrier,
        value_profile=value_profile,
        required_read_shape=readable.result_shape,
        required_join_shape=readable.join_shape,
        required_effect_profile=frontiers.EffectProfile(
            existing=(frontiers.Effect.REPLACE,),
        ),
    )


def _rule_number(number: int) -> int:
    if isinstance(number, bool) or not isinstance(number, int):
        raise TypeError("rule construction data must be an integer")
    if not 0 <= number < 256:
        raise ValueError("rule construction data must be in range 0..255")
    return number


def _binary_table(number: int, width: int = 8) -> tuple[bool, ...]:
    return tuple(bool((number >> index) & 1) for index in range(width))


def ar2_modular_0d(
    *,
    rule: int,
    modulus: int = 97,
    coefficient_grid: tuple[int, int] = (16, 16),
    constant: int = 1,
) -> Rule[R, W, C]:
    """Compile one concrete second-order modular recurrence."""

    if isinstance(rule, bool) or not isinstance(rule, int):
        raise TypeError("rule construction data must be an integer")
    rows, columns = coefficient_grid
    if rows <= 0 or columns <= 0 or not 0 <= rule < rows * columns:
        raise ValueError("rule construction data is outside coefficient grid")
    if modulus <= 0:
        raise ValueError("modulus must be positive")
    a = rule // columns + 1
    b = rule % columns
    current_term = multiply(literal_expr(a), observation(1))
    previous_term = multiply(literal_expr(b), observation(0))
    sum_term = add(
        current_term,
        previous_term,
        literal_expr(constant),
    )
    next_value = modulo(
        sum_term,
        modulus,
    )
    carrier = loci.CarrierContract(loci.CarrierKind.RECORD, rank=0, shape=())
    readable = neighborhoods.ar2_0d(
        configuration_contract=carrier,
        value_profile=alphabets.ValueProfile.INTEGER,
    )
    return expression(
        ExistingPlan(
            ExistingPlanKind.BY_LOCUS,
            (observation(1), next_value),
            (
                loci.named("previous", scope="record"),
                loci.named("current", scope="record"),
            ),
        ),
        contract=_native_contract(
            carrier,
            readable=readable,
            value_profile=alphabets.ValueProfile.INTEGER,
        ),
        witness=RuleExpr(
            ExpressionPrimitive.TUPLE,
            (
                literal_expr("ar2-modular"),
                literal_expr(rule),
                literal_expr(a),
                literal_expr(b),
                literal_expr(constant),
                literal_expr(modulus),
            ),
        ),
        provenance=(
            "native:ar2_modular_0d",
            f"rule-{rule}:a={a},b={b},c={constant},mod={modulus}",
        ),
        certificate_template=EvidenceTerm(
            "arithmetic-certificate",
            (
                EvidenceTerm(
                    "equals",
                    (
                        EvidenceTerm(
                            "mod",
                            (
                                EvidenceTerm(
                                    "sum",
                                    (
                                        EvidenceExpression(current_term),
                                        EvidenceExpression(previous_term),
                                        constant,
                                    ),
                                ),
                                modulus,
                            ),
                        ),
                        EvidenceExpression(next_value),
                    ),
                ),
            ),
        ),
    )


def dyadlags_0d(*, rule: int) -> Rule[R, W, C]:
    """Compile one concrete binary temporal three-lag lookup."""

    number = _rule_number(rule)
    index = add(
        observation(2),
        multiply(literal_expr(2), observation(1)),
        multiply(literal_expr(4), observation(0)),
    )
    output = lookup(_binary_table(number), index)
    carrier = loci.CarrierContract(
        loci.CarrierKind.HISTORY,
        rank=1,
        shape=(3,),
        axes=("history",),
    )
    readable = neighborhoods.dyadlags_0d(
        configuration_contract=carrier,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    return expression(
        ExistingPlan(
            ExistingPlanKind.BY_INDEX,
            (observation(1), observation(2), output),
        ),
        contract=_native_contract(
            carrier,
            readable=readable,
        ),
        witness=RuleExpr(
            ExpressionPrimitive.TUPLE,
            (literal_expr("dyadlags-0d"), literal_expr(number), index),
        ),
        provenance=("native:dyadlags_0d",),
        certificate_template=EvidenceTerm(
            "lookup-certificate",
            (
                number,
                EvidenceExpression(index),
                EvidenceExpression(output),
            ),
        ),
        provenance_templates=(
            ProvenanceTemplate(
                f"rule-{number}:bit-{{0}}={{1}}",
                (index, output),
            ),
        ),
    )


_UINT64_MASK = (1 << 64) - 1
_LAGCOUNTS_HASH_KEY = 0xD1B54A32D192ED03


def _splitmix64(seed: int, stream: int) -> int:
    value = (seed + stream + 0x9E3779B97F4A7C15) & _UINT64_MASK
    value = (value ^ (value >> 30)) * 0xBF58476D1CE4E5B9 & _UINT64_MASK
    value = (value ^ (value >> 27)) * 0x94D049BB133111EB & _UINT64_MASK
    return (value ^ (value >> 31)) & _UINT64_MASK


def _sampled_lag_table(number: int) -> tuple[bool, ...]:
    base = (number ^ _LAGCOUNTS_HASH_KEY) & _UINT64_MASK
    return tuple(bool(_splitmix64(base, context) & 1) for context in range(128))


def _sampled_lag_hashes(number: int) -> tuple[int, ...]:
    base = (number ^ _LAGCOUNTS_HASH_KEY) & _UINT64_MASK
    return tuple(_splitmix64(base, context) for context in range(128))


def lagcounts_0d(
    *,
    rule: int,
    band_size: int = 3,
    band_count: int = 3,
) -> Rule[R, W, C]:
    """Compile one concrete count-banded temporal lookup."""

    number = _rule_number(rule)
    if band_size != 3 or band_count != 3:
        raise ValueError("G7-01 native lagcounts uses exactly three bands of three")
    context = add(
        observation(0),
        multiply(literal_expr(2), count(group(1))),
        multiply(literal_expr(8), count(group(2))),
        multiply(literal_expr(32), count(group(3))),
    )
    output = lookup(_sampled_lag_table(number), context)
    hash_word = lookup(_sampled_lag_hashes(number), context)
    # The readable contract presents each temporal band in chronological
    # order. Select the prior nine values by their semantic history position
    # so the successor remains the one-step left shift plus the new output.
    prior = tuple(
        observation(index)
        for index in (8, 9, 4, 5, 6, 1, 2, 3, 0)
    )
    carrier = loci.CarrierContract(
        loci.CarrierKind.HISTORY,
        rank=1,
        shape=(10,),
        axes=("history",),
    )
    readable = neighborhoods.lagcounts_0d(
        band_size,
        band_count,
        configuration_contract=carrier,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    return expression(
        ExistingPlan(ExistingPlanKind.BY_INDEX, (*prior, output)),
        contract=_native_contract(
            carrier,
            readable=readable,
        ),
        witness=RuleExpr(
            ExpressionPrimitive.TUPLE,
            (literal_expr("lagcounts-0d"), literal_expr(number), context),
        ),
        provenance=("native:lagcounts_0d",),
        certificate_template=EvidenceTerm(
            "deterministic-table-certificate",
            (
                number,
                EvidenceExpression(context),
                FormattedEvidence("0x{:016x}", hash_word),
                EvidenceExpression(output),
            ),
        ),
        provenance_templates=(
            ProvenanceTemplate(
                "hash-word:0x{0:016x}",
                (hash_word,),
            ),
            ProvenanceTemplate(
                "output-bit:{0}",
                (output,),
            ),
        ),
    )


def _spatial_lookup(
    *,
    rule: int,
    rank: int,
    secondary_gate: GateKind,
    secondary_threshold: int,
    label: str,
    readable: neighborhoods.ReadableRegion[object, object],
    certificate_template: EvidenceTerm,
) -> Rule[R, W, C]:
    number = _rule_number(rule)
    primary = gate(group(1), GateKind.MAJORITY)
    secondary = gate(
        group(2),
        secondary_gate,
        threshold=secondary_threshold,
    )
    index = add(
        project(group(0), 0),
        multiply(literal_expr(2), primary),
        multiply(literal_expr(4), secondary),
    )
    output = lookup(_binary_table(number), index)
    carrier = loci.CarrierContract(
        loci.CarrierKind.GRID,
        rank=rank,
        axes=("x", "y", "z")[:rank],
    )
    return expression(
        ExistingPlan(ExistingPlanKind.BY_TARGET, (output,)),
        contract=_native_contract(
            carrier,
            readable=readable,
        ),
        witness=RuleExpr(
            ExpressionPrimitive.TUPLE,
            (literal_expr(label), literal_expr(number), index),
        ),
        provenance=(f"native:{label.replace('-', '_')}", f"rule-{number}"),
        certificate_template=certificate_template,
    )


def dyadrads_1d(*, rule: int) -> Rule[R, W, C]:
    """Compile one concrete 1-D Dyadrads lookup."""

    number = _rule_number(rule)
    index = add(
        project(group(0), 0),
        multiply(literal_expr(2), gate(group(1), GateKind.ANY)),
        multiply(literal_expr(4), gate(group(2), GateKind.ANY)),
    )
    output = lookup(_binary_table(number), index)
    carrier = loci.CarrierContract(
        loci.CarrierKind.GRID,
        rank=1,
        axes=("x",),
    )
    readable = neighborhoods.dyadrads_1d(
        configuration_contract=carrier,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    return expression(
        ExistingPlan(ExistingPlanKind.BY_TARGET, (output,)),
        contract=_native_contract(
            carrier,
            readable=readable,
        ),
        witness=RuleExpr(
            ExpressionPrimitive.TUPLE,
            (literal_expr("dyadrads-1d"), literal_expr(number), index),
        ),
        provenance=("native:dyadrads_1d", f"rule-{number}"),
        certificate_template=EvidenceTerm(
            "lookup-certificate",
            (
                number,
                EvidenceTerm(
                    "indices",
                    (
                        EvidenceExpression(
                            index,
                            EvaluationScope.EACH_TARGET,
                        ),
                    ),
                ),
            ),
        ),
    )


def dyadaxes_2d(*, rule: int) -> Rule[R, W, C]:
    """Compile one concrete 2-D Dyadaxes lookup."""

    carrier = loci.CarrierContract(
        loci.CarrierKind.GRID,
        rank=2,
        axes=("x", "y"),
    )
    return _spatial_lookup(
        rule=rule,
        rank=2,
        secondary_gate=GateKind.MAJORITY,
        secondary_threshold=0,
        label="dyadaxes-2d",
        readable=neighborhoods.dyadaxes_2d(
            configuration_contract=carrier,
            value_profile=alphabets.ValueProfile.BOOLEAN,
        ),
        certificate_template=EvidenceTerm(
            "lookup-certificate",
            (rule, "bit-7-only"),
        ),
    )


def dyadaxes_3d(*, rule: int) -> Rule[R, W, C]:
    """Compile one concrete 3-D Dyadaxes lookup."""

    carrier = loci.CarrierContract(
        loci.CarrierKind.GRID,
        rank=3,
        axes=("x", "y", "z"),
    )
    return _spatial_lookup(
        rule=rule,
        rank=3,
        secondary_gate=GateKind.AT_LEAST,
        secondary_threshold=10,
        label="dyadaxes-3d",
        readable=neighborhoods.dyadaxes_3d(
            configuration_contract=carrier,
            value_profile=alphabets.ValueProfile.BOOLEAN,
        ),
        certificate_template=EvidenceTerm(
            "lookup-certificate",
            (
                rule,
                EvidenceTerm(
                    "bit-7-sites",
                    ("center-and-six-face-centers",),
                ),
            ),
        ),
    )


def elementary(number: int) -> Rule[R, W, C]:
    """Compile an elementary binary local lookup from concrete rule data."""

    number = _rule_number(number)
    index = add(
        multiply(literal_expr(4), project(group(0), 0)),
        multiply(literal_expr(2), project(group(0), 1)),
        project(group(0), 2),
    )
    carrier = loci.CarrierContract(
        loci.CarrierKind.GRID,
        rank=1,
        axes=("x",),
    )
    readable = neighborhoods.eca(
        configuration_contract=carrier,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    return expression(
        ExistingPlan(
            ExistingPlanKind.BY_TARGET,
            (lookup(_binary_table(number), index),),
        ),
        contract=_native_contract(
            carrier,
            readable=readable,
        ),
        witness=RuleExpr(
            ExpressionPrimitive.TUPLE,
            (literal_expr("elementary"), literal_expr(number), index),
        ),
        provenance=("preset:elementary", f"rule-{number}"),
    )


__all__ = [
    "AtomMass",
    "CapabilitySelector",
    "CapabilitySelectorKind",
    "Cardinality",
    "CardinalityClaim",
    "Certificate",
    "CertificateKind",
    "ClauseKernelDenotation",
    "ClauseResult",
    "ClauseSelection",
    "Continue",
    "Derivation",
    "DerivationClauseResult",
    "Disposition",
    "DispositionAction",
    "EvaluationProof",
    "EvaluationScope",
    "EvaluationStep",
    "EvidenceExpression",
    "EvidenceTerm",
    "ExactlyOne",
    "ExactlyZero",
    "ExistingDispositionPlan",
    "ExistingPlan",
    "ExistingPlanKind",
    "ExpressionPrimitive",
    "FormattedEvidence",
    "FreshDispositionPlan",
    "GateKind",
    "InfiniteCardinality",
    "Many",
    "NoPayload",
    "NoSuccessor",
    "NoSuccessorClauseResult",
    "NoSuccessorOutcome",
    "OutcomeSpace",
    "ProbabilityLaw",
    "ProbabilityPresentation",
    "Progress",
    "ProjectionCardinalities",
    "Provenance",
    "ProvenanceTemplate",
    "Rule",
    "RuleAtom",
    "RuleClause",
    "RuleComplete",
    "RuleContract",
    "RuleDescriptor",
    "RuleExpr",
    "RuleFault",
    "RuleFaultPhase",
    "RuleFaultReason",
    "RulePrimitive",
    "RuleRejected",
    "RuleResult",
    "SequenceBoundary",
    "Stop",
    "SupportPresentation",
    "SupportSpace",
    "TotalDisposition",
    "Undetermined",
    "ValuePayload",
    "Witness",
    "absent",
    "absolute",
    "add",
    "ar2_modular_0d",
    "bound_index",
    "bound_value",
    "capability_index",
    "capability_target",
    "cardinality_size",
    "clause_kernel",
    "conditional",
    "concatenate",
    "count",
    "create",
    "delete",
    "differential",
    "divide",
    "distribution",
    "dyadlags_0d",
    "dyadrads_1d",
    "dyadaxes_2d",
    "dyadaxes_3d",
    "elementary",
    "equal",
    "every_capability",
    "expression",
    "finite_cardinality",
    "finite_probability_law",
    "finite_rule",
    "finite_support",
    "filter_items",
    "flat_map_items",
    "flat_map_lookup",
    "floor_divide",
    "fractional_part",
    "from_digits",
    "gate",
    "group",
    "index_of",
    "index_of_tag",
    "integer_digits",
    "intensional_support",
    "item_at",
    "lagcounts_0d",
    "length",
    "less_equal",
    "less_than",
    "literal",
    "literal_expr",
    "lookup",
    "map_items",
    "map_lookup",
    "map_update",
    "maximal_runs",
    "modulo",
    "multiply",
    "observation",
    "parallel",
    "preserve",
    "product_value",
    "project",
    "record_field",
    "record_update",
    "relation",
    "replace",
    "replace_at",
    "reverse",
    "slice_items",
    "sliding_windows",
    "subtract",
    "target_reference",
    "word_value",
]
