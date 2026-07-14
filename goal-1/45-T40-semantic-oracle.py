#!/usr/bin/env python3
"""Dependency-free semantic oracle for T40 mathematical-constant digits.

T40 is an immutable arity-zero closed mathematical denotation together with a
pure, typed representation query and result.  Positional base, continued-
fraction convention, coefficient selection, evaluator, budget, certificate,
and rendering are not fields of the constant.  A returned coefficient prefix
is result data, not a T37 recurrence configuration.

There is no native transition state, FRONTIER, NEIGHBORHOOD, RULE, UPDATE,
StepResult, or executor here.  Long division, the Book's ``(r,s)`` square-root
procedure, and the Gauss map are audited as optional ordinary SimpleProgram
realizations whose visible work records commute with direct representation
queries.  They are not the identity of T40; direct random-access queries are a
concrete reason that no canonical prefix rollout exists.

The Book's literal square-root branch ``r > s`` is integer-safe.  Its Notes
claim for arbitrary rational inputs is false as written: rational work can
satisfy ``s < r < s + 1``.  The separately named rational repair uses
``r >= s + 1`` and is never silently attributed to the literal source rule.

This is proof code, not a proposed runtime API.  It uses only the Python
standard library, is silent on import, and fails closed under ``python -O``.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, fields, is_dataclass, replace
from fractions import Fraction
from hashlib import sha256
from math import isqrt
from typing import TypeAlias


if not __debug__:
    raise RuntimeError("T40 semantic oracle must run with assertions enabled")


REGISTRY_VERSION = "ankos.closed-numeric/v1"
VALUE_SCHEMA = "exact_real_denotation"
BRANCH_CONVENTIONS = "positive_principal_real"
POSITIONAL_SCOPE = "fractional_coefficients_after_radix"
POSITIONAL_CANONICAL_TAIL = "terminating_zero_tail"
CF_CANONICAL_TERMINAL = "last_coefficient_gt_one_unless_singleton"
FINITE_TERMINATED = "finite_terminated"
PREFIX_OF_INFINITE = "prefix_of_infinite"
UNKNOWN_TERMINATION = "unknown_termination"
EXACT_METHOD = "closed_exact"
MACHIN_METHOD = "machin_rational_interval"
BOOK_INTEGER_SQRT = "book_literal_r_gt_s_integer_safe"
REPAIRED_RATIONAL_SQRT = "labeled_rational_r_ge_s_plus_one"


SOURCE_CLAIMS = (
    ("BOOK:1665-1687", "a simple constant definition is distinct from its complicated digit sequence"),
    ("BOOK:1689-1715", "rational positional digits terminate or repeat and long division generates them"),
    ("BOOK:1738-1746", "the displayed square-root digit realization uses visible r and s work values"),
    ("BOOK:1776-1794", "base expansions and continued fractions are representation procedures"),
    ("BOOK:1796-1798", "symbolic denotation and evaluation effort are distinct"),
    ("BOOK:12923-12958", "progressive and direct nth-digit algorithms need not share a canonical work trace"),
    ("BOOK:12972-12976", "finite digit evidence does not prove randomness or base-specific normality"),
    ("BOOK:13030-13060", "continued-fraction coefficients arise from reciprocal fractional-part iteration"),
    ("BOOK:13052-13074", "continued-fraction coefficients are unbounded"),
)


ARCHITECTURE_CLASSIFICATION = (
    "1: reuse T41 closed definitions, pure query/result provenance, certificates, and proof-strength separation",
    "1: reuse T34 exact numeric carriers/codecs and T37 indexed-prefix result representation only",
    "2: specialize the declarative definition category to arity zero and parameterize positional/simple-CF queries",
    "2: canonicalize terminating positional tails and finite simple-CF terminals without changing denotation identity",
    "3: retain lossless structural source/query/evaluator provenance and explicit T40-to-T42 coefficient handoffs",
    "1-3 only: D139 stays inside D082/T41's declarative category and adds no class-4 category or execution algebra",
    "D082 nonfit: forcing a pure denotation query into rollout is invalid; optional work procedures separately reuse the runner",
)


GOAL2_DELTA = (
    "Generalize the shared closed mathematical-definition schema to arity zero; do not add ConstantState.",
    "Keep representation, base, canonical convention, selection, method, and resource budget outside constant identity.",
    "Add pure positional/simple-CF query and typed exact/certified/partial/resource result records.",
    "Use exact rationals, arbitrary-precision integers, algebraic nodes, and certified rational enclosures; never float digits.",
    "Canonical positional rationals use the terminating zero tail rather than an eventual all-(base-1) dual.",
    "Canonical finite simple continued fractions use a final coefficient greater than one except for a singleton.",
    "Treat coefficient prefixes as immutable indexed result payloads, not T37 state, End loci, append writes, or rollout time.",
    "Expose optional work algorithms with complete visible work and explicit provenance only when their traces are requested.",
    "Restrict the Book r>s square-root procedure to integer-safe input; label r>=s+1 as the rational repair.",
    "For rational misuse the printed sqrt algebraic identity still propagates, but nonnegative-r and approximation bounds fail.",
    "T42 consumes explicit finalized T40 continued-fraction coefficients and never invokes a hidden evaluator.",
    "Add no T40 state, frontier, neighborhood, rule-result, update, StepResult, executor, callback, or family dispatch.",
)


T42_HANDOFF_CONTRACT = (
    "producer=T40_representation_query",
    "payload=immutable_indexed_simple_CF_coefficients",
    "accepted_strength=complete_exact_or_complete_certified",
    "consumer=T42_substitution_schedule",
    "forbidden=lazy_hidden_coefficient_evaluator_or_partial_prefix",
)


def exact_int(value: object, name: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{name} must be an exact int")
    return value


def exact_str(value: object, name: str) -> str:
    if type(value) is not str:
        raise TypeError(f"{name} must be an exact str")
    return value


def exact_tuple(value: object, name: str) -> tuple[object, ...]:
    if type(value) is not tuple:
        raise TypeError(f"{name} must be an exact tuple")
    return value


def exact_fraction(value: object, name: str) -> Fraction:
    if type(value) is not Fraction:
        raise TypeError(f"{name} must be an exact Fraction")
    return value


def checked_nonnegative(value: object, name: str) -> int:
    integer = exact_int(value, name)
    if integer < 0:
        raise ValueError(f"{name} must be nonnegative")
    return integer


def checked_positive(value: object, name: str) -> int:
    integer = exact_int(value, name)
    if integer <= 0:
        raise ValueError(f"{name} must be positive")
    return integer


def checked_base(value: object) -> int:
    base = exact_int(value, "base")
    if base < 2:
        raise ValueError("base must be at least two")
    return base


def checked_digest(value: object, key: tuple[object, ...], name: str) -> str:
    digest = exact_str(value, name)
    expected = sha256(repr(key).encode("utf-8")).hexdigest()
    if digest != expected:
        raise ValueError(f"{name} does not match its structural key")
    return digest


def must_raise(error: type[BaseException], thunk: object) -> int:
    if not callable(thunk):
        raise TypeError("thunk must be callable")
    try:
        thunk()
    except error:
        return 1
    except BaseException as caught:
        raise AssertionError(
            f"expected {error.__name__}, received {type(caught).__name__}"
        ) from caught
    raise AssertionError(f"expected {error.__name__}")


@dataclass(frozen=True)
class RationalLiteral:
    numerator: int
    denominator: int

    def __post_init__(self) -> None:
        numerator = checked_nonnegative(self.numerator, "rational numerator")
        denominator = checked_positive(self.denominator, "rational denominator")
        object.__setattr__(self, "numerator", numerator)
        object.__setattr__(self, "denominator", denominator)

    @property
    def value(self) -> Fraction:
        return Fraction(self.numerator, self.denominator)


@dataclass(frozen=True)
class PiConstant:
    """The exact named denotation, not a host floating value."""


@dataclass(frozen=True)
class EulerConstant:
    """The exact named denotation e, not Euler's gamma and not a float."""


@dataclass(frozen=True)
class SquareRoot:
    radicand: int

    def __post_init__(self) -> None:
        radicand = checked_positive(self.radicand, "square-root radicand")
        if isqrt(radicand) ** 2 == radicand:
            raise ValueError("strict quadratic-surd node requires a nonsquare radicand")
        object.__setattr__(self, "radicand", radicand)


ClosedNumericExpr: TypeAlias = RationalLiteral | PiConstant | EulerConstant | SquareRoot
CLOSED_EXPR_TYPES = (RationalLiteral, PiConstant, EulerConstant, SquareRoot)


def checked_closed_expr(value: object) -> ClosedNumericExpr:
    if type(value) not in CLOSED_EXPR_TYPES:
        raise TypeError("definition must use a closed numeric expression node")
    return value


@dataclass(frozen=True)
class MathematicalDenotationSpec:
    expression: ClosedNumericExpr
    parameters: tuple[object, ...] = ()
    value_schema: str = VALUE_SCHEMA
    primitive_registry_version: str = REGISTRY_VERSION
    branch_conventions: str = BRANCH_CONVENTIONS

    def __post_init__(self) -> None:
        checked_closed_expr(self.expression)
        parameters = exact_tuple(self.parameters, "parameters")
        if parameters:
            raise ValueError("T40 denotations are arity zero")
        if exact_str(self.value_schema, "value schema") != VALUE_SCHEMA:
            raise ValueError("unknown T40 value schema")
        if exact_str(self.primitive_registry_version, "registry version") != REGISTRY_VERSION:
            raise ValueError("unknown primitive registry version")
        if exact_str(self.branch_conventions, "branch conventions") != BRANCH_CONVENTIONS:
            raise ValueError("unknown branch convention profile")


def expression_key(expression: object) -> tuple[object, ...]:
    node = checked_closed_expr(expression)
    if type(node) is RationalLiteral:
        return ("RationalLiteral/v1", str(node.numerator), str(node.denominator))
    if type(node) is PiConstant:
        return ("PiConstant/v1",)
    if type(node) is EulerConstant:
        return ("EulerConstant/v1",)
    if type(node) is SquareRoot:
        return ("SquareRoot/v1", str(node.radicand))
    raise TypeError("unreachable numeric expression")


def denotation_key(spec: object) -> tuple[object, ...]:
    if type(spec) is not MathematicalDenotationSpec:
        raise TypeError("spec must be an exact MathematicalDenotationSpec")
    return (
        "MathematicalDenotationSpec/v1",
        expression_key(spec.expression),
        (),
        spec.value_schema,
        spec.primitive_registry_version,
        spec.branch_conventions,
    )


@dataclass(frozen=True)
class DenotationProvenance:
    structural_key: tuple[object, ...]
    structural_id: str

    def __post_init__(self) -> None:
        key = exact_tuple(self.structural_key, "denotation structural key")
        if not key or key[0] != "MathematicalDenotationSpec/v1":
            raise ValueError("malformed denotation structural key")
        object.__setattr__(
            self,
            "structural_id",
            checked_digest(self.structural_id, key, "denotation structural id"),
        )


def denotation_provenance(spec: object) -> DenotationProvenance:
    key = denotation_key(spec)
    return DenotationProvenance(key, sha256(repr(key).encode("utf-8")).hexdigest())


@dataclass(frozen=True)
class PositionalDigits:
    base: int
    coefficient_scope: str = POSITIONAL_SCOPE
    canonical_tail: str = POSITIONAL_CANONICAL_TAIL

    def __post_init__(self) -> None:
        object.__setattr__(self, "base", checked_base(self.base))
        if exact_str(self.coefficient_scope, "coefficient scope") != POSITIONAL_SCOPE:
            raise ValueError("unknown positional coefficient scope")
        if exact_str(self.canonical_tail, "canonical tail") != POSITIONAL_CANONICAL_TAIL:
            raise ValueError("positional rationals require a terminating zero tail")


@dataclass(frozen=True)
class SimpleContinuedFraction:
    canonical_terminal: str = CF_CANONICAL_TERMINAL

    def __post_init__(self) -> None:
        if exact_str(self.canonical_terminal, "CF terminal convention") != CF_CANONICAL_TERMINAL:
            raise ValueError("unknown simple-CF terminal convention")


RepresentationSpec: TypeAlias = PositionalDigits | SimpleContinuedFraction
REPRESENTATION_TYPES = (PositionalDigits, SimpleContinuedFraction)


def checked_representation(value: object) -> RepresentationSpec:
    if type(value) not in REPRESENTATION_TYPES:
        raise TypeError("representation must be positional digits or a simple continued fraction")
    return value


@dataclass(frozen=True)
class Prefix:
    count: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "count", checked_nonnegative(self.count, "prefix count"))


@dataclass(frozen=True)
class CoefficientAt:
    index: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "index", checked_nonnegative(self.index, "coefficient index"))


Selection: TypeAlias = Prefix | CoefficientAt
SELECTION_TYPES = (Prefix, CoefficientAt)


@dataclass(frozen=True)
class RepresentationQuery:
    denotation: MathematicalDenotationSpec
    representation: RepresentationSpec
    selection: Selection

    def __post_init__(self) -> None:
        if type(self.denotation) is not MathematicalDenotationSpec:
            raise TypeError("query denotation must be exact MathematicalDenotationSpec")
        checked_representation(self.representation)
        if type(self.selection) not in SELECTION_TYPES:
            raise TypeError("query selection must be Prefix or CoefficientAt")


@dataclass(frozen=True)
class EvaluationContext:
    method: str
    term_budget: int

    def __post_init__(self) -> None:
        method = exact_str(self.method, "evaluation method")
        if method not in (EXACT_METHOD, MACHIN_METHOD):
            raise ValueError("unknown evaluation method")
        budget = checked_nonnegative(self.term_budget, "term budget")
        if method == EXACT_METHOD and budget != 0:
            raise ValueError("closed exact evaluation has no approximation term budget")
        object.__setattr__(self, "method", method)
        object.__setattr__(self, "term_budget", budget)


def representation_key(spec: object) -> tuple[object, ...]:
    representation = checked_representation(spec)
    if type(representation) is PositionalDigits:
        return (
            "PositionalDigits/v1",
            str(representation.base),
            representation.coefficient_scope,
            representation.canonical_tail,
        )
    return ("SimpleContinuedFraction/v1", representation.canonical_terminal)


def selection_key(selection: object) -> tuple[object, ...]:
    if type(selection) is Prefix:
        return ("Prefix/v1", str(selection.count))
    if type(selection) is CoefficientAt:
        return ("CoefficientAt/v1", str(selection.index))
    raise TypeError("selection must be Prefix or CoefficientAt")


def query_key(query: object) -> tuple[object, ...]:
    if type(query) is not RepresentationQuery:
        raise TypeError("query must be exact RepresentationQuery")
    return (
        "RepresentationQuery/v1",
        denotation_key(query.denotation),
        representation_key(query.representation),
        selection_key(query.selection),
    )


def context_key(context: object) -> tuple[object, ...]:
    if type(context) is not EvaluationContext:
        raise TypeError("context must be exact EvaluationContext")
    return ("EvaluationContext/v1", context.method, str(context.term_budget))


@dataclass(frozen=True)
class QueryProvenance:
    query_key: tuple[object, ...]
    query_id: str
    context_key: tuple[object, ...]
    context_id: str

    def __post_init__(self) -> None:
        query = exact_tuple(self.query_key, "query key")
        context = exact_tuple(self.context_key, "context key")
        if not query or query[0] != "RepresentationQuery/v1":
            raise ValueError("malformed query key")
        if not context or context[0] != "EvaluationContext/v1":
            raise ValueError("malformed evaluation context key")
        object.__setattr__(self, "query_id", checked_digest(self.query_id, query, "query id"))
        object.__setattr__(self, "context_id", checked_digest(self.context_id, context, "context id"))


def query_provenance(query: object, context: object) -> QueryProvenance:
    q_key = query_key(query)
    c_key = context_key(context)
    return QueryProvenance(
        q_key,
        sha256(repr(q_key).encode("utf-8")).hexdigest(),
        c_key,
        sha256(repr(c_key).encode("utf-8")).hexdigest(),
    )


@dataclass(frozen=True)
class RationalInterval:
    lower: Fraction
    upper: Fraction

    def __post_init__(self) -> None:
        lower = exact_fraction(self.lower, "interval lower")
        upper = exact_fraction(self.upper, "interval upper")
        if not lower < upper:
            raise ValueError("rational interval must have positive width")


@dataclass(frozen=True)
class MachinCertificate:
    terms: int
    interval: RationalInterval
    representation_key: tuple[object, ...]
    integer_digits: tuple[int, ...]
    certified_coefficients: tuple[int, ...]

    def __post_init__(self) -> None:
        terms = checked_positive(self.terms, "Machin terms")
        if type(self.interval) is not RationalInterval:
            raise TypeError("Machin certificate requires a rational interval")
        key = exact_tuple(self.representation_key, "certificate representation key")
        if not key or key[0] not in ("PositionalDigits/v1", "SimpleContinuedFraction/v1"):
            raise ValueError("malformed certificate representation key")
        integers = exact_tuple(self.integer_digits, "certificate integer digits")
        coefficients = exact_tuple(self.certified_coefficients, "certified coefficients")
        for value in integers + coefficients:
            checked_nonnegative(value, "certificate coefficient")
        object.__setattr__(self, "terms", terms)


@dataclass(frozen=True)
class CompleteExact:
    derivation: str

    def __post_init__(self) -> None:
        if not exact_str(self.derivation, "exact derivation"):
            raise ValueError("exact derivation cannot be empty")


@dataclass(frozen=True)
class CompleteCertified:
    certificate: MachinCertificate

    def __post_init__(self) -> None:
        if type(self.certificate) is not MachinCertificate:
            raise TypeError("certified outcome requires MachinCertificate")


@dataclass(frozen=True)
class Partial:
    completed_count: int
    requested_count: int
    reason: str
    certificate: MachinCertificate

    def __post_init__(self) -> None:
        completed = checked_positive(self.completed_count, "partial completed count")
        requested = checked_positive(self.requested_count, "partial requested count")
        if completed >= requested:
            raise ValueError("partial result must be strictly incomplete")
        if not exact_str(self.reason, "partial reason"):
            raise ValueError("partial reason cannot be empty")
        if type(self.certificate) is not MachinCertificate:
            raise TypeError("partial result requires a certificate for returned coefficients")


@dataclass(frozen=True)
class ResourceLimit:
    resource: str
    limit: int
    requested_count: int

    def __post_init__(self) -> None:
        if not exact_str(self.resource, "resource"):
            raise ValueError("resource cannot be empty")
        checked_nonnegative(self.limit, "resource limit")
        checked_nonnegative(self.requested_count, "resource requested count")


QueryOutcome: TypeAlias = CompleteExact | CompleteCertified | Partial | ResourceLimit
OUTCOME_TYPES = (CompleteExact, CompleteCertified, Partial, ResourceLimit)


def checked_digit_tuple(values: object, base: int, name: str) -> tuple[int, ...]:
    raw = exact_tuple(values, name)
    digits = tuple(exact_int(value, f"{name} digit") for value in raw)
    if any(value < 0 or value >= base for value in digits):
        raise ValueError(f"{name} contains a digit outside its base")
    return digits


@dataclass(frozen=True)
class ExpansionResult:
    query: RepresentationQuery
    context: EvaluationContext
    provenance: QueryProvenance
    start_index: int
    coefficients: tuple[int, ...]
    integer_digits: tuple[int, ...]
    outcome: QueryOutcome
    termination: str

    def __post_init__(self) -> None:
        if type(self.query) is not RepresentationQuery:
            raise TypeError("result query must be exact RepresentationQuery")
        if type(self.context) is not EvaluationContext:
            raise TypeError("result context must be exact EvaluationContext")
        if type(self.provenance) is not QueryProvenance:
            raise TypeError("result provenance must be exact QueryProvenance")
        if self.provenance != query_provenance(self.query, self.context):
            raise ValueError("result provenance does not match query and context")
        start = checked_nonnegative(self.start_index, "result start index")
        coefficients = exact_tuple(self.coefficients, "result coefficients")
        integers = exact_tuple(self.integer_digits, "result integer digits")
        if type(self.outcome) not in OUTCOME_TYPES:
            raise TypeError("unknown query outcome")
        termination = exact_str(self.termination, "termination")
        if termination not in (FINITE_TERMINATED, PREFIX_OF_INFINITE, UNKNOWN_TERMINATION):
            raise ValueError("unknown representation termination status")
        if type(self.query.selection) is Prefix and start != 0:
            raise ValueError("prefix results must start at coefficient zero")
        if type(self.query.selection) is CoefficientAt and start != self.query.selection.index:
            raise ValueError("random-access result start does not match requested index")
        if type(self.query.representation) is PositionalDigits:
            base = self.query.representation.base
            checked_digit_tuple(coefficients, base, "result coefficients")
            checked_digit_tuple(integers, base, "result integer digits")
            if type(self.outcome) is not ResourceLimit and not integers:
                raise ValueError("completed positional results require integer digits")
        else:
            if integers:
                raise ValueError("continued-fraction results have no positional integer field")
            for offset, value in enumerate(coefficients):
                coefficient = exact_int(value, "continued-fraction coefficient")
                absolute_index = start + offset
                if coefficient < 0 or (absolute_index > 0 and coefficient < 1):
                    raise ValueError("invalid simple continued-fraction coefficient")
        target = (
            self.query.selection.count
            if type(self.query.selection) is Prefix
            else 1
        )
        if type(self.outcome) in (CompleteExact, CompleteCertified):
            if len(coefficients) != target:
                finite_short = termination == FINITE_TERMINATED and len(coefficients) < target
                random_past_end = (
                    finite_short
                    and type(self.query.selection) is CoefficientAt
                    and len(coefficients) == 0
                )
                prefix_at_end = finite_short and type(self.query.selection) is Prefix
                if not (random_past_end or prefix_at_end):
                    raise ValueError("complete result has the wrong coefficient count")
        elif type(self.outcome) is Partial:
            if type(self.query.selection) is not Prefix:
                raise ValueError("partial coefficient payloads are prefix-only")
            if len(coefficients) != self.outcome.completed_count:
                raise ValueError("partial outcome count does not match payload")
            if target != self.outcome.requested_count:
                raise ValueError("partial requested count does not match query")
        else:
            if coefficients or integers:
                raise ValueError("resource-limited result cannot invent coefficients")
        if type(self.outcome) in (CompleteCertified, Partial):
            certificate = self.outcome.certificate
            if type(self.query.denotation.expression) is not PiConstant:
                raise ValueError("Machin certificates are scoped to the Pi denotation")
            if certificate.representation_key != representation_key(self.query.representation):
                raise ValueError("certificate representation does not match the query")
            if not verify_machin_certificate(certificate):
                raise ValueError("Machin certificate does not independently verify")
            if type(self.query.selection) is Prefix:
                if coefficients != certificate.certified_coefficients[: len(coefficients)]:
                    raise ValueError("certificate does not cover returned prefix")
            else:
                index = self.query.selection.index
                if index >= len(certificate.certified_coefficients):
                    raise ValueError("certificate does not reach random-access coefficient")
                if coefficients != (certificate.certified_coefficients[index],):
                    raise ValueError("certificate does not cover random-access coefficient")
            if integers != certificate.integer_digits:
                raise ValueError("certificate integer digits do not match the result")
        object.__setattr__(self, "start_index", start)
        object.__setattr__(self, "coefficients", coefficients)
        object.__setattr__(self, "integer_digits", integers)


def encode_nonnegative_integer(value: object, base: object) -> tuple[int, ...]:
    integer = checked_nonnegative(value, "integer value")
    radix = checked_base(base)
    if integer == 0:
        return (0,)
    reversed_digits: list[int] = []
    while integer:
        integer, digit = divmod(integer, radix)
        reversed_digits.append(digit)
    return tuple(reversed(reversed_digits))


def decode_digits(digits: object, base: object) -> int:
    radix = checked_base(base)
    values = checked_digit_tuple(digits, radix, "digits")
    if not values:
        raise ValueError("digit tuple cannot be empty")
    result = 0
    for digit in values:
        result = radix * result + digit
    return result


def primitive_period(period: tuple[int, ...]) -> bool:
    if not period:
        return True
    for width in range(1, len(period)):
        if len(period) % width == 0 and period == period[:width] * (len(period) // width):
            return False
    return True


@dataclass(frozen=True)
class RationalPositionalExpansion:
    base: int
    integer_digits: tuple[int, ...]
    nonrepeating: tuple[int, ...]
    period: tuple[int, ...]

    def __post_init__(self) -> None:
        base = checked_base(self.base)
        integers = checked_digit_tuple(self.integer_digits, base, "integer digits")
        nonrepeating = checked_digit_tuple(self.nonrepeating, base, "nonrepeating digits")
        period = checked_digit_tuple(self.period, base, "period digits")
        if not integers:
            raise ValueError("integer digits cannot be empty")
        if len(integers) > 1 and integers[0] == 0:
            raise ValueError("integer digits cannot have a leading zero")
        if not period and nonrepeating and nonrepeating[-1] == 0:
            raise ValueError("terminating zero tail must be implicit")
        if period and not primitive_period(period):
            raise ValueError("repeating block must be primitive")
        if period and all(digit == base - 1 for digit in period):
            raise ValueError("eventual all-(base-1) dual is not canonical")
        object.__setattr__(self, "base", base)
        object.__setattr__(self, "integer_digits", integers)
        object.__setattr__(self, "nonrepeating", nonrepeating)
        object.__setattr__(self, "period", period)

    def prefix(self, count: object) -> tuple[int, ...]:
        requested = checked_nonnegative(count, "digit count")
        out = list(self.nonrepeating[:requested])
        while len(out) < requested:
            if self.period:
                out.append(self.period[(len(out) - len(self.nonrepeating)) % len(self.period)])
            else:
                out.append(0)
        return tuple(out)


def raw_positional_value(
    integer_digits: object,
    nonrepeating: object,
    period: object,
    base: object,
) -> Fraction:
    radix = checked_base(base)
    integers = checked_digit_tuple(integer_digits, radix, "raw integer digits")
    finite = checked_digit_tuple(nonrepeating, radix, "raw nonrepeating digits")
    repeating = checked_digit_tuple(period, radix, "raw period digits")
    if not integers:
        raise ValueError("raw positional integer digits cannot be empty")
    value = Fraction(decode_digits(integers, radix), 1)
    if finite:
        value += Fraction(decode_digits(finite, radix), radix ** len(finite))
    if repeating:
        value += Fraction(
            decode_digits(repeating, radix),
            radix ** len(finite) * (radix ** len(repeating) - 1),
        )
    return value


def rational_positional_expansion(value: object, base: object) -> RationalPositionalExpansion:
    rational = exact_fraction(value, "rational value")
    if rational < 0:
        raise ValueError("strict oracle positional profile is nonnegative")
    radix = checked_base(base)
    whole, remainder = divmod(rational.numerator, rational.denominator)
    integer_digits = encode_nonnegative_integer(whole, radix)
    digits: list[int] = []
    seen: dict[int, int] = {}
    while remainder and remainder not in seen:
        seen[remainder] = len(digits)
        digit, remainder = divmod(remainder * radix, rational.denominator)
        digits.append(digit)
    if remainder == 0:
        while digits and digits[-1] == 0:
            digits.pop()
        nonrepeating = tuple(digits)
        period: tuple[int, ...] = ()
    else:
        split = seen[remainder]
        nonrepeating = tuple(digits[:split])
        period = tuple(digits[split:])
    expansion = RationalPositionalExpansion(radix, integer_digits, nonrepeating, period)
    if raw_positional_value(
        expansion.integer_digits,
        expansion.nonrepeating,
        expansion.period,
        radix,
    ) != rational:
        raise ArithmeticError("rational positional expansion did not round-trip")
    return expansion


@dataclass(frozen=True)
class CanonicalContinuedFraction:
    coefficients: tuple[int, ...]
    terminated: bool

    def __post_init__(self) -> None:
        coefficients = exact_tuple(self.coefficients, "continued-fraction coefficients")
        if not coefficients:
            raise ValueError("continued fraction cannot be empty")
        checked = tuple(exact_int(value, "continued-fraction coefficient") for value in coefficients)
        if checked[0] < 0 or any(value < 1 for value in checked[1:]):
            raise ValueError("invalid simple continued-fraction coefficients")
        if type(self.terminated) is not bool:
            raise TypeError("terminated must be an exact bool")
        if self.terminated and len(checked) > 1 and checked[-1] <= 1:
            raise ValueError("canonical finite CF terminal coefficient must exceed one")
        object.__setattr__(self, "coefficients", checked)


def continued_fraction_value(coefficients: object) -> Fraction:
    raw = exact_tuple(coefficients, "continued-fraction coefficients")
    if not raw:
        raise ValueError("continued fraction cannot be empty")
    values = tuple(exact_int(value, "continued-fraction coefficient") for value in raw)
    if values[0] < 0 or any(value < 1 for value in values[1:]):
        raise ValueError("invalid simple continued fraction")
    result = Fraction(values[-1], 1)
    for coefficient in reversed(values[:-1]):
        result = coefficient + Fraction(1, result)
    return result


def rational_continued_fraction(value: object) -> CanonicalContinuedFraction:
    current = exact_fraction(value, "rational value")
    if current < 0:
        raise ValueError("strict oracle CF profile is nonnegative")
    coefficients: list[int] = []
    while True:
        coefficient = current.numerator // current.denominator
        coefficients.append(coefficient)
        remainder = current - coefficient
        if remainder == 0:
            break
        current = Fraction(1, remainder)
    result = CanonicalContinuedFraction(tuple(coefficients), True)
    if continued_fraction_value(result.coefficients) != value:
        raise ArithmeticError("rational continued fraction did not round-trip")
    return result


@dataclass(frozen=True)
class PositionalCylinder:
    base: int
    integer_digits: tuple[int, ...]
    prefix: tuple[int, ...]
    lower: Fraction
    upper: Fraction

    def __post_init__(self) -> None:
        base = checked_base(self.base)
        integers = checked_digit_tuple(self.integer_digits, base, "cylinder integer digits")
        prefix = checked_digit_tuple(self.prefix, base, "cylinder prefix")
        lower = exact_fraction(self.lower, "cylinder lower")
        upper = exact_fraction(self.upper, "cylinder upper")
        scale = base ** len(prefix)
        expected = Fraction(decode_digits(integers, base) * scale + (decode_digits(prefix, base) if prefix else 0), scale)
        if lower != expected or upper != expected + Fraction(1, scale):
            raise ValueError("positional cylinder endpoints do not match prefix")
        object.__setattr__(self, "base", base)

    def contains(self, value: object) -> bool:
        rational = exact_fraction(value, "cylinder probe")
        return self.lower <= rational < self.upper


def positional_cylinder(
    integer_digits: object,
    prefix: object,
    base: object,
) -> PositionalCylinder:
    radix = checked_base(base)
    integers = checked_digit_tuple(integer_digits, radix, "integer digits")
    digits = checked_digit_tuple(prefix, radix, "prefix")
    scale = radix ** len(digits)
    lower = Fraction(
        decode_digits(integers, radix) * scale + (decode_digits(digits, radix) if digits else 0),
        scale,
    )
    return PositionalCylinder(radix, integers, digits, lower, lower + Fraction(1, scale))


def convergent_pair(coefficients: object) -> tuple[int, int, int, int]:
    raw = exact_tuple(coefficients, "continued-fraction prefix")
    if not raw:
        raise ValueError("continued-fraction prefix cannot be empty")
    p_minus_two, p_minus_one = 0, 1
    q_minus_two, q_minus_one = 1, 0
    for index, value in enumerate(raw):
        coefficient = exact_int(value, "continued-fraction coefficient")
        if coefficient < 0 or (index > 0 and coefficient < 1):
            raise ValueError("invalid simple continued-fraction prefix")
        p = coefficient * p_minus_one + p_minus_two
        q = coefficient * q_minus_one + q_minus_two
        p_minus_two, p_minus_one = p_minus_one, p
        q_minus_two, q_minus_one = q_minus_one, q
    return p_minus_one, q_minus_one, p_minus_two, q_minus_two


@dataclass(frozen=True)
class ContinuedFractionCylinder:
    prefix: tuple[int, ...]
    lower: Fraction
    upper: Fraction

    def __post_init__(self) -> None:
        prefix = exact_tuple(self.prefix, "CF cylinder prefix")
        p, q, previous_p, previous_q = convergent_pair(prefix)
        first = Fraction(p, q)
        second = Fraction(p + previous_p, q + previous_q)
        expected_lower, expected_upper = sorted((first, second))
        if self.lower != expected_lower or self.upper != expected_upper:
            raise ValueError("continued-fraction cylinder endpoints do not match prefix")

    def contains_interior(self, value: object) -> bool:
        rational = exact_fraction(value, "CF cylinder probe")
        return self.lower < rational < self.upper


def continued_fraction_cylinder(prefix: object) -> ContinuedFractionCylinder:
    values = exact_tuple(prefix, "continued-fraction prefix")
    p, q, previous_p, previous_q = convergent_pair(values)
    lower, upper = sorted((Fraction(p, q), Fraction(p + previous_p, q + previous_q)))
    return ContinuedFractionCylinder(values, lower, upper)


def atan_inverse_interval(denominator: object, terms: object) -> RationalInterval:
    q = checked_positive(denominator, "arctangent denominator")
    count = checked_positive(terms, "arctangent terms")
    total = Fraction(0, 1)
    for index in range(count):
        term = Fraction(1, (2 * index + 1) * q ** (2 * index + 1))
        total = total + term if index % 2 == 0 else total - term
    next_term = Fraction(1, (2 * count + 1) * q ** (2 * count + 1))
    if count % 2 == 1:
        return RationalInterval(total - next_term, total)
    return RationalInterval(total, total + next_term)


def machin_pi_interval(terms: object) -> RationalInterval:
    count = checked_positive(terms, "Machin terms")
    atan_five = atan_inverse_interval(5, count)
    atan_239 = atan_inverse_interval(239, count)
    return RationalInterval(
        16 * atan_five.lower - 4 * atan_239.upper,
        16 * atan_five.upper - 4 * atan_239.lower,
    )


def fixed_width_digits(value: object, base: object, width: object) -> tuple[int, ...]:
    integer = checked_nonnegative(value, "fixed-width value")
    radix = checked_base(base)
    count = checked_nonnegative(width, "fixed-width count")
    if integer >= radix ** count:
        raise ValueError("value does not fit requested digit width")
    if count == 0:
        return ()
    digits = encode_nonnegative_integer(integer, radix)
    return (0,) * (count - len(digits)) + digits


def certified_positional_prefix(
    interval: object,
    base: object,
    requested: object,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    enclosure = interval
    if type(enclosure) is not RationalInterval:
        raise TypeError("certification requires RationalInterval")
    radix = checked_base(base)
    target = checked_nonnegative(requested, "requested positional count")
    if enclosure.lower < 0:
        raise ValueError("strict positional certification requires nonnegative interval")
    for count in range(target, -1, -1):
        scale = radix ** count
        scaled_floor = (enclosure.lower.numerator * scale) // enclosure.lower.denominator
        if enclosure.upper * scale < scaled_floor + 1:
            integer = scaled_floor // scale
            fractional = scaled_floor % scale
            return encode_nonnegative_integer(integer, radix), fixed_width_digits(fractional, radix, count)
    return (), ()


def certified_cf_prefix(interval: object, requested: object) -> tuple[int, ...]:
    enclosure = interval
    if type(enclosure) is not RationalInterval:
        raise TypeError("CF certification requires RationalInterval")
    target = checked_nonnegative(requested, "requested CF count")
    lower, upper = enclosure.lower, enclosure.upper
    coefficients: list[int] = []
    for _ in range(target):
        lower_floor = lower.numerator // lower.denominator
        upper_floor = upper.numerator // upper.denominator
        if lower_floor != upper_floor or upper >= lower_floor + 1:
            break
        coefficients.append(lower_floor)
        lower_remainder = lower - lower_floor
        upper_remainder = upper - upper_floor
        if lower_remainder <= 0:
            break
        lower, upper = Fraction(1, upper_remainder), Fraction(1, lower_remainder)
    return tuple(coefficients)


def verify_machin_certificate(certificate: object) -> bool:
    if type(certificate) is not MachinCertificate:
        return False
    try:
        if certificate.interval != machin_pi_interval(certificate.terms):
            return False
        key = certificate.representation_key
        if key[0] == "PositionalDigits/v1":
            base = int(key[1])
            integers, coefficients = certified_positional_prefix(
                certificate.interval,
                base,
                len(certificate.certified_coefficients),
            )
            return (
                integers == certificate.integer_digits
                and coefficients == certificate.certified_coefficients
            )
        coefficients = certified_cf_prefix(
            certificate.interval,
            len(certificate.certified_coefficients),
        )
        return (
            certificate.integer_digits == ()
            and coefficients == certificate.certified_coefficients
        )
    except (TypeError, ValueError, ZeroDivisionError):
        return False


def sqrt_cf_period(radicand: object) -> tuple[int, tuple[int, ...]]:
    value = checked_positive(radicand, "square-root radicand")
    a0 = isqrt(value)
    if a0 * a0 == value:
        raise ValueError("quadratic-surd CF period requires a nonsquare radicand")
    m, denominator, coefficient = 0, 1, a0
    period: list[int] = []
    while True:
        m = denominator * coefficient - m
        numerator = value - m * m
        if numerator <= 0 or numerator % denominator:
            raise ArithmeticError("invalid exact quadratic-surd recurrence")
        denominator = numerator // denominator
        coefficient = (a0 + m) // denominator
        period.append(coefficient)
        if coefficient == 2 * a0:
            break
    return a0, tuple(period)


def sqrt_cf_prefix(radicand: object, count: object) -> tuple[int, ...]:
    requested = checked_nonnegative(count, "square-root CF count")
    if requested == 0:
        return ()
    a0, period = sqrt_cf_period(radicand)
    return (a0,) + tuple(period[(index - 1) % len(period)] for index in range(1, requested))


def e_cf_coefficient(index: object) -> int:
    position = checked_nonnegative(index, "e CF index")
    if position == 0:
        return 2
    if position % 3 == 2:
        return 2 * ((position + 1) // 3)
    return 1


def e_cf_prefix(count: object) -> tuple[int, ...]:
    requested = checked_nonnegative(count, "e CF count")
    return tuple(e_cf_coefficient(index) for index in range(requested))


def direct_sqrt_bits(radicand: object, count: object) -> tuple[int, ...]:
    value = exact_fraction(radicand, "normalized radicand")
    requested = checked_nonnegative(count, "square-root bit count")
    if value < 1 or value >= 4:
        raise ValueError("direct square-root bits require 1 <= radicand < 4")
    if requested == 0:
        return ()
    scale_power = requested - 1
    scaled_square_numerator = value.numerator * 4 ** scale_power
    quotient = scaled_square_numerator // value.denominator
    prefix_value = isqrt(quotient)
    bits = fixed_width_digits(prefix_value, 2, requested)
    if bits[0] != 1:
        raise ArithmeticError("normalized square root must begin with binary one")
    lower_square = Fraction(prefix_value * prefix_value, 4 ** scale_power)
    upper_square = Fraction((prefix_value + 1) ** 2, 4 ** scale_power)
    if not lower_square <= value < upper_square:
        raise ArithmeticError("direct square-root prefix failed exact cylinder check")
    return bits


def selection_target(selection: object) -> int:
    if type(selection) is Prefix:
        return selection.count
    if type(selection) is CoefficientAt:
        return selection.index + 1
    raise TypeError("unknown selection")


def select_coefficients(full_prefix: tuple[int, ...], selection: Selection) -> tuple[int, tuple[int, ...]]:
    if type(selection) is Prefix:
        return 0, full_prefix[: selection.count]
    if selection.index < len(full_prefix):
        return selection.index, (full_prefix[selection.index],)
    return selection.index, ()


def exact_result(
    query: RepresentationQuery,
    context: EvaluationContext,
    full_prefix: tuple[int, ...],
    integer_digits: tuple[int, ...],
    termination: str,
    derivation: str,
) -> ExpansionResult:
    start, selected = select_coefficients(full_prefix, query.selection)
    return ExpansionResult(
        query,
        context,
        query_provenance(query, context),
        start,
        selected,
        integer_digits,
        CompleteExact(derivation),
        termination,
    )


def evaluate_exact_query(
    query: RepresentationQuery,
    context: EvaluationContext,
) -> ExpansionResult:
    if context.method != EXACT_METHOD:
        raise ValueError("exact denotation profile requires closed_exact context")
    expression = query.denotation.expression
    target = selection_target(query.selection)
    representation = query.representation
    if type(expression) is RationalLiteral and type(representation) is PositionalDigits:
        expansion = rational_positional_expansion(expression.value, representation.base)
        return exact_result(
            query,
            context,
            expansion.prefix(target),
            expansion.integer_digits,
            FINITE_TERMINATED if not expansion.period else PREFIX_OF_INFINITE,
            "exact_long_division_denotation",
        )
    if type(expression) is RationalLiteral and type(representation) is SimpleContinuedFraction:
        expansion = rational_continued_fraction(expression.value)
        return exact_result(
            query,
            context,
            expansion.coefficients[:target],
            (),
            FINITE_TERMINATED,
            "exact_euclidean_continued_fraction",
        )
    if type(expression) is SquareRoot and type(representation) is SimpleContinuedFraction:
        return exact_result(
            query,
            context,
            sqrt_cf_prefix(expression.radicand, target),
            (),
            PREFIX_OF_INFINITE,
            "exact_quadratic_surd_period",
        )
    if type(expression) is SquareRoot and type(representation) is PositionalDigits:
        if representation.base != 2 or expression.radicand not in (2, 3):
            raise ValueError("direct exact square-root positional preset is normalized base two")
        all_bits = direct_sqrt_bits(Fraction(expression.radicand, 1), target + 1)
        return exact_result(
            query,
            context,
            all_bits[1:],
            (1,),
            PREFIX_OF_INFINITE,
            "exact_integer_square_comparison",
        )
    if type(expression) is EulerConstant and type(representation) is SimpleContinuedFraction:
        return exact_result(
            query,
            context,
            e_cf_prefix(target),
            (),
            PREFIX_OF_INFINITE,
            "Euler_simple_CF_pattern",
        )
    raise ValueError("closed exact evaluator does not support this denotation/representation pair")


def evaluate_pi_query(
    query: RepresentationQuery,
    context: EvaluationContext,
) -> ExpansionResult:
    if type(query.denotation.expression) is not PiConstant:
        raise ValueError("Machin evaluator is scoped only to the Pi denotation")
    if context.method != MACHIN_METHOD:
        raise ValueError("Pi certification requires the Machin rational-interval context")
    target = selection_target(query.selection)
    if context.term_budget == 0:
        return ExpansionResult(
            query,
            context,
            query_provenance(query, context),
            0 if type(query.selection) is Prefix else query.selection.index,
            (),
            (),
            ResourceLimit("Machin_terms", 0, target),
            PREFIX_OF_INFINITE,
        )
    interval = machin_pi_interval(context.term_budget)
    if type(query.representation) is PositionalDigits:
        integers, certified = certified_positional_prefix(
            interval,
            query.representation.base,
            target,
        )
    else:
        integers = ()
        certified = certified_cf_prefix(interval, target)
    certificate = MachinCertificate(
        context.term_budget,
        interval,
        representation_key(query.representation),
        integers,
        certified,
    )
    if not verify_machin_certificate(certificate):
        raise ArithmeticError("internally generated Machin certificate did not verify")
    completed = len(certified)
    if completed >= target:
        start, selected = select_coefficients(certified, query.selection)
        outcome: QueryOutcome = CompleteCertified(certificate)
        result_integers = integers
    elif type(query.selection) is Prefix and completed > 0:
        start, selected = 0, certified
        outcome = Partial(completed, target, "Machin term budget exhausted", certificate)
        result_integers = integers
    else:
        return ExpansionResult(
            query,
            context,
            query_provenance(query, context),
            0 if type(query.selection) is Prefix else query.selection.index,
            (),
            (),
            ResourceLimit("Machin_terms", context.term_budget, target),
            PREFIX_OF_INFINITE,
        )
    return ExpansionResult(
        query,
        context,
        query_provenance(query, context),
        start,
        selected,
        result_integers,
        outcome,
        PREFIX_OF_INFINITE,
    )


def evaluate_query(query: object, context: object) -> ExpansionResult:
    if type(query) is not RepresentationQuery:
        raise TypeError("query must be exact RepresentationQuery")
    if type(context) is not EvaluationContext:
        raise TypeError("context must be exact EvaluationContext")
    if type(query.denotation.expression) is PiConstant:
        return evaluate_pi_query(query, context)
    return evaluate_exact_query(query, context)


def verify_result(result: object) -> bool:
    if type(result) is not ExpansionResult:
        return False
    try:
        replay = evaluate_query(result.query, result.context)
        return replay == result
    except (TypeError, ValueError, ArithmeticError, ZeroDivisionError):
        return False


@dataclass(frozen=True)
class ExactEquivalenceCertificate:
    left: DenotationProvenance
    right: DenotationProvenance
    common_rational: Fraction

    def __post_init__(self) -> None:
        if type(self.left) is not DenotationProvenance or type(self.right) is not DenotationProvenance:
            raise TypeError("equivalence certificate requires denotation provenance")
        exact_fraction(self.common_rational, "common rational")


def certify_rational_equivalence(
    left: object,
    right: object,
) -> ExactEquivalenceCertificate | None:
    if type(left) is not MathematicalDenotationSpec or type(right) is not MathematicalDenotationSpec:
        raise TypeError("equivalence inputs must be denotation specs")
    if type(left.expression) is not RationalLiteral or type(right.expression) is not RationalLiteral:
        return None
    if left.expression.value != right.expression.value:
        return None
    return ExactEquivalenceCertificate(
        denotation_provenance(left),
        denotation_provenance(right),
        left.expression.value,
    )


@dataclass(frozen=True)
class LongDivisionWork:
    source: RationalLiteral
    base: int
    remainder: int
    emitted: tuple[int, ...]

    def __post_init__(self) -> None:
        if type(self.source) is not RationalLiteral:
            raise TypeError("long-division source must be RationalLiteral")
        base = checked_base(self.base)
        remainder = checked_nonnegative(self.remainder, "long-division remainder")
        if remainder >= self.source.denominator:
            raise ValueError("long-division remainder must be below denominator")
        emitted = checked_digit_tuple(self.emitted, base, "long-division emitted digits")
        expected = self.source.numerator % self.source.denominator
        replayed: list[int] = []
        for _ in emitted:
            digit, expected = divmod(expected * base, self.source.denominator)
            replayed.append(digit)
        if tuple(replayed) != emitted or expected != remainder:
            raise ValueError("long-division work does not replay from its source")
        object.__setattr__(self, "base", base)
        object.__setattr__(self, "remainder", remainder)
        object.__setattr__(self, "emitted", emitted)


def begin_long_division(source: object, base: object) -> LongDivisionWork:
    if type(source) is not RationalLiteral:
        raise TypeError("long-division source must be RationalLiteral")
    radix = checked_base(base)
    return LongDivisionWork(source, radix, source.numerator % source.denominator, ())


def long_division_next(work: object) -> LongDivisionWork:
    if type(work) is not LongDivisionWork:
        raise TypeError("long-division work must be exact LongDivisionWork")
    digit, remainder = divmod(work.remainder * work.base, work.source.denominator)
    return LongDivisionWork(work.source, work.base, remainder, work.emitted + (digit,))


@dataclass(frozen=True)
class SqrtDigitWork:
    radicand: Fraction
    profile: str
    iteration: int
    r: Fraction
    s: int
    visible_bits: tuple[int, ...]

    def __post_init__(self) -> None:
        radicand = exact_fraction(self.radicand, "square-root work radicand")
        if radicand < 1 or radicand >= 4:
            raise ValueError("square-root work requires 1 <= radicand < 4")
        profile = exact_str(self.profile, "square-root work profile")
        if profile not in (BOOK_INTEGER_SQRT, REPAIRED_RATIONAL_SQRT):
            raise ValueError("unknown square-root work profile")
        if profile == BOOK_INTEGER_SQRT and radicand.denominator != 1:
            raise ValueError("literal Book r>s profile is restricted to integer-safe input")
        iteration = checked_nonnegative(self.iteration, "square-root work iteration")
        r = exact_fraction(self.r, "square-root work r")
        s = checked_nonnegative(self.s, "square-root work s")
        bits = checked_digit_tuple(self.visible_bits, 2, "square-root visible bits")
        if len(bits) != iteration:
            raise ValueError("square-root visible prefix length must equal iteration")
        if s * s + 4 * r != Fraction(4 ** (iteration + 1), 1) * radicand:
            raise ValueError("square-root work violates s^2+4r invariant")
        upper_square = Fraction((s + 4) ** 2, 1)
        scaled_value = Fraction(4 ** (iteration + 1), 1) * radicand
        if not s * s <= scaled_value < upper_square:
            raise ValueError("square-root work violates exact prefix enclosure")
        if bits != direct_sqrt_bits(radicand, iteration):
            raise ValueError("square-root visible bits do not commute with direct prefix")
        if iteration and (s % 4 or decode_digits(bits, 2) != s // 4):
            raise ValueError("square-root s does not losslessly expose its current bit prefix")
        object.__setattr__(self, "profile", profile)
        object.__setattr__(self, "iteration", iteration)
        object.__setattr__(self, "s", s)
        object.__setattr__(self, "visible_bits", bits)


def begin_sqrt_digit_work(radicand: object, profile: object) -> SqrtDigitWork:
    value = exact_fraction(radicand, "square-root radicand")
    mode = exact_str(profile, "square-root profile")
    return SqrtDigitWork(value, mode, 0, value, 0, ())


def sqrt_digit_next(work: object) -> SqrtDigitWork:
    if type(work) is not SqrtDigitWork:
        raise TypeError("square-root work must be exact SqrtDigitWork")
    if work.profile == BOOK_INTEGER_SQRT:
        take_one = work.r > work.s
    else:
        take_one = work.r >= work.s + 1
    if take_one:
        r = 4 * (work.r - work.s - 1)
        s = 2 * (work.s + 2)
    else:
        r = 4 * work.r
        s = 2 * work.s
    iteration = work.iteration + 1
    return SqrtDigitWork(
        work.radicand,
        work.profile,
        iteration,
        r,
        s,
        direct_sqrt_bits(work.radicand, iteration),
    )


def unsafe_literal_rational_sqrt_next(r: object, s: object) -> tuple[Fraction, int]:
    """Literal source spelling, retained only to demonstrate its rational defect."""

    current_r = exact_fraction(r, "literal rational r")
    current_s = checked_nonnegative(s, "literal rational s")
    if current_r > current_s:
        return 4 * (current_r - current_s - 1), 2 * (current_s + 2)
    return 4 * current_r, 2 * current_s


@dataclass(frozen=True)
class GaussMapWork:
    source: RationalLiteral
    current: Fraction | None
    coefficients: tuple[int, ...]

    def __post_init__(self) -> None:
        if type(self.source) is not RationalLiteral:
            raise TypeError("Gauss source must be RationalLiteral")
        if self.current is not None:
            exact_fraction(self.current, "Gauss current value")
            if self.current < 0:
                raise ValueError("Gauss current value must be nonnegative")
        coefficients = exact_tuple(self.coefficients, "Gauss coefficients")
        for index, coefficient in enumerate(coefficients):
            value = exact_int(coefficient, "Gauss coefficient")
            if value < 0 or (index > 0 and value < 1):
                raise ValueError("invalid Gauss coefficient")
        expected: Fraction | None = self.source.value
        replayed: list[int] = []
        for _ in coefficients:
            if expected is None:
                raise ValueError("Gauss work continued beyond rational completion")
            coefficient = expected.numerator // expected.denominator
            replayed.append(coefficient)
            remainder = expected - coefficient
            expected = None if remainder == 0 else Fraction(1, remainder)
        if tuple(replayed) != coefficients or expected != self.current:
            raise ValueError("Gauss work does not replay from its source")
        object.__setattr__(self, "coefficients", tuple(coefficients))


def begin_gauss_map(source: object) -> GaussMapWork:
    if type(source) is not RationalLiteral:
        raise TypeError("Gauss source must be RationalLiteral")
    return GaussMapWork(source, source.value, ())


def gauss_map_next(work: object) -> GaussMapWork:
    if type(work) is not GaussMapWork:
        raise TypeError("Gauss work must be exact GaussMapWork")
    if work.current is None:
        raise ValueError("rational Gauss realization is already complete")
    coefficient = work.current.numerator // work.current.denominator
    remainder = work.current - coefficient
    current = None if remainder == 0 else Fraction(1, remainder)
    return GaussMapWork(work.source, current, work.coefficients + (coefficient,))


@dataclass(frozen=True)
class T42CoefficientInput:
    source_query_id: str
    source_result_id: str
    coefficients: tuple[int, ...]
    proof_strength: str

    def __post_init__(self) -> None:
        source_query = exact_str(self.source_query_id, "T42 source query id")
        source_result = exact_str(self.source_result_id, "T42 source result id")
        if len(source_query) != 64 or len(source_result) != 64:
            raise ValueError("T42 handoff ids must be SHA-256 hex strings")
        coefficients = exact_tuple(self.coefficients, "T42 coefficients")
        if not coefficients:
            raise ValueError("T42 coefficient input cannot be empty")
        for index, coefficient in enumerate(coefficients):
            value = exact_int(coefficient, "T42 coefficient")
            if value < 0 or (index > 0 and value < 1):
                raise ValueError("invalid T42 simple-CF coefficient")
        strength = exact_str(self.proof_strength, "T42 proof strength")
        if strength not in ("complete_exact", "complete_certified"):
            raise ValueError("T42 requires complete exact or certified coefficients")


def result_key(result: object) -> tuple[object, ...]:
    if type(result) is not ExpansionResult:
        raise TypeError("result must be exact ExpansionResult")
    outcome_name = type(result.outcome).__name__
    return (
        "ExpansionResult/v1",
        result.provenance.query_id,
        result.provenance.context_id,
        str(result.start_index),
        tuple(str(value) for value in result.coefficients),
        tuple(str(value) for value in result.integer_digits),
        outcome_name,
        result.termination,
    )


def make_t42_coefficient_input(result: object) -> T42CoefficientInput:
    if type(result) is not ExpansionResult:
        raise TypeError("T42 handoff requires exact ExpansionResult")
    if not verify_result(result):
        raise ValueError("T42 handoff requires a replay-verified result")
    if type(result.query.representation) is not SimpleContinuedFraction:
        raise ValueError("T42 handoff requires simple continued-fraction coefficients")
    if type(result.query.selection) is not Prefix or result.start_index != 0:
        raise ValueError("T42 handoff requires a prefix beginning at coefficient zero")
    if type(result.outcome) is CompleteExact:
        strength = "complete_exact"
    elif type(result.outcome) is CompleteCertified:
        strength = "complete_certified"
    else:
        raise ValueError("T42 handoff rejects partial and resource-limited results")
    key = result_key(result)
    return T42CoefficientInput(
        result.provenance.query_id,
        sha256(repr(key).encode("utf-8")).hexdigest(),
        result.coefficients,
        strength,
    )


def dataclass_manifest(namespace: dict[str, object]) -> tuple[tuple[str, tuple[str, ...]], ...]:
    rows: list[tuple[str, tuple[str, ...]]] = []
    for name, value in namespace.items():
        if type(name) is str and isinstance(value, type) and is_dataclass(value):
            rows.append((name, tuple(field.name for field in fields(value))))
    return tuple(sorted(rows))


FORBIDDEN_EXECUTION_ROLE_SUFFIXES = (
    "State",
    "Frontier",
    "Neighborhood",
    "Rule",
    "Update",
    "StepResult",
    "Executor",
)


def forbidden_execution_role_symbols(
    namespace: dict[str, object],
) -> tuple[tuple[str, tuple[str, ...]], ...]:
    rows: list[tuple[str, tuple[str, ...]]] = []
    for suffix in FORBIDDEN_EXECUTION_ROLE_SUFFIXES:
        names = tuple(
            sorted(
                name
                for name in namespace
                if type(name) is str
                and name.endswith(suffix)
            )
        )
        rows.append((suffix, names))
    return tuple(rows)


def rational_spec(numerator: object, denominator: object) -> MathematicalDenotationSpec:
    return MathematicalDenotationSpec(RationalLiteral(numerator, denominator))


def pi_spec() -> MathematicalDenotationSpec:
    return MathematicalDenotationSpec(PiConstant())


def e_spec() -> MathematicalDenotationSpec:
    return MathematicalDenotationSpec(EulerConstant())


def sqrt_spec(radicand: object) -> MathematicalDenotationSpec:
    return MathematicalDenotationSpec(SquareRoot(radicand))


def exact_context() -> EvaluationContext:
    return EvaluationContext(EXACT_METHOD, 0)


def machin_context(terms: object) -> EvaluationContext:
    return EvaluationContext(MACHIN_METHOD, terms)


def audit_rational_positional_and_duals() -> tuple[int, int, int, int, int]:
    cases = (
        (Fraction(3, 8), 10, (0,), (3, 7, 5), ()),
        (Fraction(1, 3), 10, (0,), (), (3,)),
        (Fraction(1, 7), 10, (0,), (), (1, 4, 2, 8, 5, 7)),
        (Fraction(1, 6), 10, (0,), (1,), (6,)),
        (Fraction(1, 81), 10, (0,), (), (0, 1, 2, 3, 4, 5, 6, 7, 9)),
        (Fraction(1, 3), 2, (0,), (), (0, 1)),
        (Fraction(1, 7), 2, (0,), (), (0, 0, 1)),
        (Fraction(3, 8), 2, (0,), (0, 1, 1), ()),
    )
    roundtrips = 0
    prefix_checks = 0
    total_period = 0
    terminating = 0
    for value, base, integer_digits, nonrepeating, period in cases:
        expansion = rational_positional_expansion(value, base)
        assert expansion.integer_digits == integer_digits
        assert expansion.nonrepeating == nonrepeating
        assert expansion.period == period
        assert raw_positional_value(integer_digits, nonrepeating, period, base) == value
        roundtrips += 1
        total_period += len(period)
        terminating += not period
        for count in range(25):
            prefix = expansion.prefix(count)
            cylinder = positional_cylinder(integer_digits, prefix, base)
            assert cylinder.contains(value)
            prefix_checks += 1

    terminating_half = raw_positional_value((0,), (5,), (), 10)
    repeating_dual = raw_positional_value((0,), (4,), (9,), 10)
    assert terminating_half == repeating_dual == Fraction(1, 2)
    canonical_half = rational_positional_expansion(Fraction(1, 2), 10)
    assert canonical_half == RationalPositionalExpansion(10, (0,), (5,), ())

    canonical_cf = rational_continued_fraction(Fraction(1, 2))
    assert canonical_cf.coefficients == (0, 2)
    assert continued_fraction_value((0, 2)) == continued_fraction_value((0, 1, 1))
    dual_checks = 4
    return len(cases), roundtrips, prefix_checks, total_period, terminating + dual_checks


def audit_long_division_realization() -> tuple[int, int, int, int]:
    cases = (
        (RationalLiteral(1, 7), 10, 50),
        (RationalLiteral(1, 6), 10, 40),
        (RationalLiteral(3, 8), 2, 30),
        (RationalLiteral(22, 7), 10, 45),
        (RationalLiteral(2**130 + 17, 2**67 + 9), 16, 55),
    )
    one_step_commutations = 0
    remainder_map_checks = 0
    arbitrary_precision_bits = 0
    zero_tail_steps = 0
    for source, base, horizon in cases:
        work = begin_long_division(source, base)
        assert work.emitted == ()
        for index in range(horizon):
            old_remainder = work.remainder
            work = long_division_next(work)
            expected_digit, expected_remainder = divmod(
                old_remainder * base,
                source.denominator,
            )
            assert work.emitted[-1] == expected_digit
            assert work.remainder == expected_remainder
            direct_value = (
                (source.numerator % source.denominator) * base ** (index + 1)
            ) // source.denominator
            assert work.emitted == fixed_width_digits(direct_value, base, index + 1)
            one_step_commutations += 1
            remainder_map_checks += 1
            zero_tail_steps += expected_remainder == 0
        arbitrary_precision_bits = max(
            arbitrary_precision_bits,
            source.numerator.bit_length(),
            source.denominator.bit_length(),
        )
    return one_step_commutations, remainder_map_checks, arbitrary_precision_bits, zero_tail_steps


PI_DECIMAL_60 = "141592653589793238462643383279502884197169399375105820974944"
PI_BINARY_96 = (
    "001001000011111101101010100010001000010110100011"
    "000010001101001100010011000110011000101000101110"
)
PI_CF_30 = (
    3,
    7,
    15,
    1,
    292,
    1,
    1,
    1,
    2,
    1,
    3,
    1,
    14,
    2,
    1,
    1,
    2,
    2,
    2,
    2,
    1,
    84,
    2,
    1,
    1,
    15,
    3,
    13,
    1,
    4,
)


def audit_pi_certification() -> tuple[int, int, int, int, int, int, int]:
    denotation = pi_spec()
    context = machin_context(70)
    decimal_query = RepresentationQuery(denotation, PositionalDigits(10), Prefix(60))
    binary_query = RepresentationQuery(denotation, PositionalDigits(2), Prefix(96))
    cf_query = RepresentationQuery(denotation, SimpleContinuedFraction(), Prefix(30))
    decimal = evaluate_query(decimal_query, context)
    binary = evaluate_query(binary_query, context)
    continued = evaluate_query(cf_query, context)
    assert type(decimal.outcome) is CompleteCertified
    assert type(binary.outcome) is CompleteCertified
    assert type(continued.outcome) is CompleteCertified
    assert decimal.integer_digits == (3,)
    assert binary.integer_digits == (1, 1)
    assert "".join(str(digit) for digit in decimal.coefficients) == PI_DECIMAL_60
    assert "".join(str(digit) for digit in binary.coefficients) == PI_BINARY_96
    assert continued.coefficients == PI_CF_30
    for result in (decimal, binary, continued):
        assert verify_result(result)
        assert verify_machin_certificate(result.outcome.certificate)

    decimal_cylinder = positional_cylinder((3,), decimal.coefficients, 10)
    decimal_interval = decimal.outcome.certificate.interval
    assert decimal_cylinder.lower <= decimal_interval.lower
    assert decimal_interval.upper < decimal_cylinder.upper
    binary_cylinder = positional_cylinder((1, 1), binary.coefficients, 2)
    binary_interval = binary.outcome.certificate.interval
    assert binary_cylinder.lower <= binary_interval.lower
    assert binary_interval.upper < binary_cylinder.upper
    cf_cylinder = continued_fraction_cylinder(continued.coefficients)
    cf_interval = continued.outcome.certificate.interval
    assert cf_cylinder.lower < cf_interval.lower < cf_interval.upper < cf_cylinder.upper
    widths = (
        decimal_interval.upper - decimal_interval.lower,
        binary_interval.upper - binary_interval.lower,
        cf_interval.upper - cf_interval.lower,
    )
    assert all(width > 0 for width in widths)
    return (
        len(decimal.coefficients),
        len(binary.coefficients),
        len(continued.coefficients),
        sum(result.outcome.certificate.terms for result in (decimal, binary, continued)),
        3,
        max(len(str(width.denominator)) for width in widths),
        3,
    )


def audit_exact_cf_families() -> tuple[int, int, int, int, int]:
    expected_periods = {
        2: (1, (2,)),
        3: (1, (1, 2)),
        5: (2, (4,)),
        7: (2, (1, 1, 1, 4)),
        23: (4, (1, 3, 1, 8)),
    }
    period_checks = 0
    prefix_checks = 0
    maximum_period = 0
    context = exact_context()
    for radicand, expected in expected_periods.items():
        assert sqrt_cf_period(radicand) == expected
        maximum_period = max(maximum_period, len(expected[1]))
        period_checks += 1
        query = RepresentationQuery(
            sqrt_spec(radicand),
            SimpleContinuedFraction(),
            Prefix(80),
        )
        result = evaluate_query(query, context)
        assert type(result.outcome) is CompleteExact
        assert result.coefficients == sqrt_cf_prefix(radicand, 80)
        assert verify_result(result)
        for index in range(80):
            expected_coefficient = expected[0] if index == 0 else expected[1][(index - 1) % len(expected[1])]
            assert result.coefficients[index] == expected_coefficient
            prefix_checks += 1

    expected_e = (
        2, 1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, 1, 1, 10, 1, 1, 12,
        1, 1, 14, 1, 1, 16, 1, 1, 18, 1, 1, 20,
    )
    assert e_cf_prefix(len(expected_e)) == expected_e
    e_query = RepresentationQuery(e_spec(), SimpleContinuedFraction(), Prefix(120))
    e_result = evaluate_query(e_query, context)
    assert e_result.coefficients == e_cf_prefix(120)
    assert type(e_result.outcome) is CompleteExact and verify_result(e_result)
    return period_checks, prefix_checks, maximum_period, len(expected_e), len(e_result.coefficients)


def audit_sqrt_digit_realization() -> tuple[int, int, int, int, int, int, int]:
    commutations = 0
    invariant_checks = 0
    strict_runs = 0
    repaired_runs = 0
    for radicand, profile, horizon in (
        (Fraction(2, 1), BOOK_INTEGER_SQRT, 90),
        (Fraction(3, 1), BOOK_INTEGER_SQRT, 90),
        (Fraction(9, 4), REPAIRED_RATIONAL_SQRT, 70),
        (Fraction(11, 5), REPAIRED_RATIONAL_SQRT, 70),
        (Fraction(17, 9), REPAIRED_RATIONAL_SQRT, 70),
    ):
        work = begin_sqrt_digit_work(radicand, profile)
        strict_runs += profile == BOOK_INTEGER_SQRT
        repaired_runs += profile == REPAIRED_RATIONAL_SQRT
        for iteration in range(1, horizon + 1):
            work = sqrt_digit_next(work)
            assert work.visible_bits == direct_sqrt_bits(radicand, iteration)
            assert work.s * work.s + 4 * work.r == Fraction(4 ** (iteration + 1), 1) * radicand
            commutations += 1
            invariant_checks += 2

    two = sqrt_digit_next(begin_sqrt_digit_work(Fraction(2, 1), REPAIRED_RATIONAL_SQRT))
    nine_fourths = sqrt_digit_next(
        begin_sqrt_digit_work(Fraction(9, 4), REPAIRED_RATIONAL_SQRT)
    )
    assert (two.r, two.s) == (Fraction(4, 1), 4)
    assert (nine_fourths.r, nine_fourths.s) == (Fraction(5, 1), 4)
    assert two.visible_bits == nine_fourths.visible_bits == (1,)
    two_next = sqrt_digit_next(two)
    nine_fourths_next = sqrt_digit_next(nine_fourths)
    assert two_next.visible_bits == (1, 0)
    assert nine_fourths_next.visible_bits == (1, 1)
    prefix_loss_witnesses = 1

    repaired = sqrt_digit_next(
        begin_sqrt_digit_work(Fraction(11, 5), REPAIRED_RATIONAL_SQRT)
    )
    assert (repaired.r, repaired.s) == (Fraction(24, 5), 4)
    literal_r, literal_s = unsafe_literal_rational_sqrt_next(repaired.r, repaired.s)
    repaired_next = sqrt_digit_next(repaired)
    old_identity = repaired.s * repaired.s + 4 * repaired.r
    literal_identity = literal_s * literal_s + 4 * literal_r
    assert literal_identity == 4 * old_identity
    assert literal_r == Fraction(-4, 5)
    assert repaired_next.r == Fraction(96, 5)
    scaled_value = Fraction(4 ** (repaired.iteration + 2), 1) * repaired.radicand
    assert not literal_s * literal_s <= scaled_value < (literal_s + 4) ** 2
    assert repaired_next.s * repaired_next.s <= scaled_value < (repaired_next.s + 4) ** 2
    algebraic_identity_survives = 1
    failed_literal_nonnegative_and_bound = 2
    return (
        commutations,
        invariant_checks,
        strict_runs,
        repaired_runs,
        prefix_loss_witnesses,
        algebraic_identity_survives,
        failed_literal_nonnegative_and_bound,
    )


def audit_gauss_map_realization() -> tuple[int, int, int, int]:
    sources = (
        RationalLiteral(1, 2),
        RationalLiteral(22, 7),
        RationalLiteral(415, 93),
        RationalLiteral(355, 113),
        RationalLiteral(2**140 + 1, 2**73 + 19),
    )
    coefficients = 0
    one_step_commutations = 0
    completions = 0
    maximum_coefficient_bits = 0
    for source in sources:
        expected = rational_continued_fraction(source.value).coefficients
        work = begin_gauss_map(source)
        for index, coefficient in enumerate(expected):
            work = gauss_map_next(work)
            assert work.coefficients == expected[: index + 1]
            assert work.coefficients[-1] == coefficient
            coefficients += 1
            one_step_commutations += 1
            maximum_coefficient_bits = max(maximum_coefficient_bits, coefficient.bit_length())
        assert work.current is None
        assert work.coefficients == expected
        completions += 1
        assert continued_fraction_value(work.coefficients) == source.value
    return len(sources), coefficients, one_step_commutations, completions + maximum_coefficient_bits
