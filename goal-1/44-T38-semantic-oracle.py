#!/usr/bin/env python3
"""Dependency-free semantic oracle for T38 variable-index recurrences.

T38 reuses T37's complete indexed prefix, unique trailing ``End`` locus,
complete-prefix NEIGHBORHOOD read, ``End -> Val End`` write, and T16 exactly-one
ordered splice.  Its only native delta is a closed RULE expression whose
``TermAt`` addresses may depend on values read earlier in the same expression.
Every demand is evaluated leftmost-innermost against one immutable old prefix.

This oracle independently evaluates the eight Book rows as direct equations and
through the structural SimpleProgram path:

    NumericPrefix -> unique End -> complete old-prefix read -> closed RULE
                  -> endpoint replacement -> T16 single splice

It binds successful and partial ``StepResult`` envelopes, complete access
witnesses, structural program identity, full validation traces plus compact
D073 reconstruction projections, the page-131 case (d) observers, and the
lossless prefix/tagged-word commuting square.  It imports no project/runtime
modules, is silent on import, and fails closed under ``python -O``.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, fields, is_dataclass, replace
from hashlib import sha256
from typing import TypeAlias


if not __debug__:
    raise RuntimeError("T38 semantic oracle must run with assertions enabled")


DOMAIN = "discrete_t_plus_1D"
VALUE_CARRIER = "positive_arbitrary_precision_integer"
DEMAND_ORDER = "leftmost_innermost"
END_ROLE = "unique_trailing_end"
UPDATE_ROLE = "T16_exactly_one_ordered_splice"


SOURCE_CLAIMS = (
    ("BOOK:1559-1561", "the state exposes stable indexed earlier terms"),
    ("BOOK:1569", "term values compute non-fixed historical addresses"),
    ("BOOK:1571-1575", "a demanded nonpositive index is meaningless and the eight displayed rows avoid it"),
    ("BOOK:_page_144_Figure_3.jpeg", "eight exact rules, seeds, and visible term rows"),
    ("BOOK:_page_145_Figure_1.jpeg", "cases c through h are analyzed as fluctuation profiles"),
    ("BOOK:12720-12724", "memoization stores old indexed values and textually fixes case e"),
    ("BOOK:12726", "ordinary evaluation is leftmost innermost and does not cancel demanded invalid reads"),
    ("BOOK:12728-12742", "case d has exact digit and multiplicity observers with one guarded missing initial 1"),
    ("BOOK:12761-12765", "address plots and evaluation trees are observers of p and q dependencies"),
)


ARCHITECTURE_CLASSIFICATION = (
    "1: reuse D070/T37 NumericPrefix, exact positive values, unique End, endpoint write, trace, and StepResult",
    "1: reuse T37 complete explicit old-prefix NEIGHBORHOOD access without a T38 selector or neighborhood type",
    "2: extend the closed RULE AST with ordered nested TermAt demands and exact witnesses",
    "2: a demanded absent old term is common Error(UndefinedTermReference), not Invalid, halt, boundary, or default",
    "3: inherit D072's lossless Val* End representation and T16 exactly-one splice commuting square",
    "4: add no T38 state, frontier, update, executor, family branch, callback, hidden memo table, or execution algebra",
)


GOAL2_DELTA = (
    "Reuse the complete consecutive NumericPrefix and its bijective Val* End codec.",
    "Reuse the unique trailing End selector and End(n) to Val(n,value) End(n+1) replacement.",
    "Reuse complete explicit old-prefix NEIGHBORHOOD access; add no T38 selector or neighborhood type.",
    "Extend the closed RULE expression algebra with structural TermAt(address_expression) nodes.",
    "Evaluate TermAt occurrences leftmost-innermost against that immutable read and retain occurrence multiplicity.",
    "Record exact target, address, stable indexed handle, expression path, demand order, and program provenance.",
    "Return common zero-successor Error(UndefinedTermReference) on a demanded address outside [origin,next_index).",
    "Keep malformed AST, value type, seed, and tagged-word inputs as construction/invariant rejection.",
    "Reuse T16 exactly-one ordered splice for every successful append; no endpoint UPDATE is added.",
    "Keep memoization, digit formulae, multiplicity lists, p/q plots, and evaluation trees as implementations or observers.",
    "Add no VariableRecurrenceState, FRONTIER, UPDATE, executor, callback, family dispatch, padding, wrap, clamp, or default.",
)


RAW_12738_SPELLING = "Flatten[Table[n, {IntegerExponent[n, 2] + 1}], {n, m}]]"
GUARDED_12738_REPAIR = (
    "BOOK:12738",
    "the multiplicity list begins 1,2,2,... and omits the second initial 1",
    "prepend exactly one 1; BOOK:12742 independently gives last_index(1)=2",
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


def checked_positive(value: object, name: str) -> int:
    integer = exact_int(value, name)
    if integer <= 0:
        raise ValueError(f"{name} must be positive")
    return integer


def checked_nonnegative(value: object, name: str) -> int:
    integer = exact_int(value, name)
    if integer < 0:
        raise ValueError(f"{name} must be nonnegative")
    return integer


def checked_path(value: object, name: str = "path") -> tuple[int, ...]:
    path = exact_tuple(value, name)
    out = tuple(exact_int(item, f"{name} component") for item in path)
    if any(item < 0 for item in out):
        raise ValueError(f"{name} components must be nonnegative")
    return out


@dataclass(frozen=True)
class Literal:
    value: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", exact_int(self.value, "literal value"))


@dataclass(frozen=True)
class TargetIndex:
    """The exact next consecutive term index supplied by the endpoint locus."""


@dataclass(frozen=True)
class Add:
    terms: tuple[Expression, ...]

    def __post_init__(self) -> None:
        terms = exact_tuple(self.terms, "Add terms")
        if len(terms) < 2:
            raise ValueError("Add requires at least two ordered terms")
        for term in terms:
            checked_expression(term)
        object.__setattr__(self, "terms", terms)


@dataclass(frozen=True)
class Sub:
    left: Expression
    right: Expression

    def __post_init__(self) -> None:
        checked_expression(self.left)
        checked_expression(self.right)


@dataclass(frozen=True)
class Mul:
    factors: tuple[Expression, ...]

    def __post_init__(self) -> None:
        factors = exact_tuple(self.factors, "Mul factors")
        if len(factors) < 2:
            raise ValueError("Mul requires at least two ordered factors")
        for factor in factors:
            checked_expression(factor)
        object.__setattr__(self, "factors", factors)


@dataclass(frozen=True)
class TermAt:
    address: Expression

    def __post_init__(self) -> None:
        checked_expression(self.address)


Expression: TypeAlias = Literal | TargetIndex | Add | Sub | Mul | TermAt
ResolvedExpression: TypeAlias = Literal | Add | Sub | Mul


EXPRESSION_TYPES = (Literal, TargetIndex, Add, Sub, Mul, TermAt)
RESOLVED_EXPRESSION_TYPES = (Literal, Add, Sub, Mul)


def checked_expression(value: object) -> Expression:
    if type(value) not in EXPRESSION_TYPES:
        raise TypeError("expression must be a closed T38 integer-expression node")
    return value


def checked_resolved_expression(value: object) -> ResolvedExpression:
    if type(value) not in RESOLVED_EXPRESSION_TYPES:
        raise TypeError("resolved expression cannot retain TargetIndex or TermAt")
    if type(value) is Add:
        for term in value.terms:
            checked_resolved_expression(term)
    elif type(value) is Sub:
        checked_resolved_expression(value.left)
        checked_resolved_expression(value.right)
    elif type(value) is Mul:
        for factor in value.factors:
            checked_resolved_expression(factor)
    return value


def expression_key(expression: object) -> tuple[object, ...]:
    node = checked_expression(expression)
    if type(node) is Literal:
        return ("Literal/v1", str(node.value))
    if type(node) is TargetIndex:
        return ("TargetIndex/v1",)
    if type(node) is Add:
        return ("Add/v1", tuple(expression_key(term) for term in node.terms))
    if type(node) is Sub:
        return ("Sub/v1", expression_key(node.left), expression_key(node.right))
    if type(node) is Mul:
        return ("Mul/v1", tuple(expression_key(factor) for factor in node.factors))
    if type(node) is TermAt:
        return ("TermAt/v1", expression_key(node.address))
    raise TypeError("unreachable expression node")


def evaluate_resolved(expression: object) -> int:
    node = checked_resolved_expression(expression)
    if type(node) is Literal:
        return node.value
    if type(node) is Add:
        return sum(evaluate_resolved(term) for term in node.terms)
    if type(node) is Sub:
        return evaluate_resolved(node.left) - evaluate_resolved(node.right)
    if type(node) is Mul:
        value = 1
        for factor in node.factors:
            value *= evaluate_resolved(factor)
        return value
    raise TypeError("unreachable resolved expression node")


@dataclass(frozen=True)
class NumericPrefix:
    """The reused T37 complete consecutive indexed-prefix configuration."""

    origin: int
    terms: tuple[int, ...]

    def __post_init__(self) -> None:
        origin = exact_int(self.origin, "prefix origin")
        if origin != 1:
            raise ValueError("strict T38 requires origin one")
        terms = exact_tuple(self.terms, "prefix terms")
        if not terms:
            raise ValueError("prefix terms cannot be empty")
        checked = tuple(checked_positive(term, "prefix term") for term in terms)
        object.__setattr__(self, "origin", origin)
        object.__setattr__(self, "terms", checked)

    @property
    def next_index(self) -> int:
        return self.origin + len(self.terms)

    def value_at(self, index: object) -> int:
        exact_index = exact_int(index, "term index")
        if not self.origin <= exact_index < self.next_index:
            raise IndexError("term index is outside the old prefix")
        return self.terms[exact_index - self.origin]


@dataclass(frozen=True)
class Val:
    index: int
    value: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "index", checked_positive(self.index, "Val index"))
        object.__setattr__(self, "value", checked_positive(self.value, "Val value"))


@dataclass(frozen=True)
class End:
    next_index: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "next_index", checked_positive(self.next_index, "End index"))


WordToken: TypeAlias = Val | End


def checked_word(value: object) -> tuple[WordToken, ...]:
    word = exact_tuple(value, "tagged word")
    if len(word) < 2:
        raise ValueError("tagged prefix word needs at least one Val and one End")
    if type(word[-1]) is not End:
        raise ValueError("tagged prefix word must end in End")
    if sum(type(token) is End for token in word) != 1:
        raise ValueError("tagged prefix word must have exactly one End")
    expected_index = 1
    for token in word[:-1]:
        if type(token) is not Val:
            raise TypeError("only Val tokens may precede End")
        if token.index != expected_index:
            raise ValueError("Val indices must be consecutive from one")
        expected_index += 1
    if word[-1].next_index != expected_index:
        raise ValueError("End index must follow the final Val")
    return word


def encode_prefix(prefix: object) -> tuple[WordToken, ...]:
    if type(prefix) is not NumericPrefix:
        raise TypeError("encode_prefix requires exact NumericPrefix")
    return tuple(
        [Val(prefix.origin + offset, value) for offset, value in enumerate(prefix.terms)]
        + [End(prefix.next_index)]
    )


def decode_prefix(word: object) -> NumericPrefix:
    checked = checked_word(word)
    return NumericPrefix(1, tuple(token.value for token in checked[:-1]))


def select_unique_end(word: object) -> tuple[int, End]:
    checked = checked_word(word)
    return len(checked) - 1, checked[-1]


@dataclass(frozen=True)
class RecurrenceProgram:
    """Immutable closed expression data, not a callback or family executor."""

    expression: Expression
    carrier: str = VALUE_CARRIER
    demand_order: str = DEMAND_ORDER

    def __post_init__(self) -> None:
        expression = checked_expression(self.expression)
        carrier = exact_str(self.carrier, "program carrier")
        order = exact_str(self.demand_order, "demand order")
        if carrier != VALUE_CARRIER:
            raise ValueError("strict T38 uses the positive exact-integer carrier")
        if order != DEMAND_ORDER:
            raise ValueError("strict T38 demand order is leftmost innermost")
        object.__setattr__(self, "expression", expression)
        object.__setattr__(self, "carrier", carrier)
        object.__setattr__(self, "demand_order", order)


def structural_program_key(program: object) -> tuple[object, ...]:
    if type(program) is not RecurrenceProgram:
        raise TypeError("program must be exact RecurrenceProgram")
    return (
        "ComputedPrefixRecurrence/v1",
        program.carrier,
        program.demand_order,
        expression_key(program.expression),
    )


def checked_expression_key(value: object) -> tuple[object, ...]:
    key = exact_tuple(value, "expression key")
    if not key or type(key[0]) is not str:
        raise TypeError("expression key requires an exact string tag")
    tag = key[0]
    if tag == "Literal/v1":
        if len(key) != 2 or type(key[1]) is not str:
            raise ValueError("Literal key must contain one decimal string")
        try:
            integer = int(key[1])
        except ValueError as error:
            raise ValueError("Literal key decimal is invalid") from error
        if str(integer) != key[1]:
            raise ValueError("Literal key decimal must be canonical")
        return key
    if tag == "TargetIndex/v1":
        if len(key) != 1:
            raise ValueError("TargetIndex key has no payload")
        return key
    if tag in ("Add/v1", "Mul/v1"):
        if len(key) != 2:
            raise ValueError(f"{tag} key requires one child tuple")
        children = exact_tuple(key[1], f"{tag} children")
        if len(children) < 2:
            raise ValueError(f"{tag} key requires at least two children")
        for child in children:
            checked_expression_key(child)
        return key
    if tag == "Sub/v1":
        if len(key) != 3:
            raise ValueError("Sub key requires left and right children")
        checked_expression_key(key[1])
        checked_expression_key(key[2])
        return key
    if tag == "TermAt/v1":
        if len(key) != 2:
            raise ValueError("TermAt key requires one address child")
        checked_expression_key(key[1])
        return key
    raise ValueError(f"unknown closed expression-key tag {tag!r}")


def checked_program_key(value: object) -> tuple[object, ...]:
    key = exact_tuple(value, "program key")
    if len(key) != 4:
        raise ValueError("program key must contain four fields")
    if key[0] != "ComputedPrefixRecurrence/v1":
        raise ValueError("unknown program-key version")
    if key[1] != VALUE_CARRIER or key[2] != DEMAND_ORDER:
        raise ValueError("program-key profile mismatch")
    checked_expression_key(key[3])
    return key


@dataclass(frozen=True)
class ProgramProvenance:
    structural_key: tuple[object, ...]
    identifier: str

    def __post_init__(self) -> None:
        key = checked_program_key(self.structural_key)
        identifier = exact_str(self.identifier, "program identifier")
        expected = sha256(repr(key).encode("utf-8")).hexdigest()
        if identifier != expected:
            raise ValueError("program identifier does not match structural key")
        object.__setattr__(self, "structural_key", key)
        object.__setattr__(self, "identifier", identifier)


def program_provenance(program: object) -> ProgramProvenance:
    key = structural_program_key(program)
    return ProgramProvenance(key, sha256(repr(key).encode("utf-8")).hexdigest())


@dataclass(frozen=True)
class TermHandle:
    index: int
    value: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "index", checked_positive(self.index, "term-handle index"))
        object.__setattr__(self, "value", checked_positive(self.value, "term-handle value"))


@dataclass(frozen=True)
class ReadDemand:
    order: int
    path: tuple[int, ...]
    target_index: int
    address: int
    handle: TermHandle

    def __post_init__(self) -> None:
        order = checked_nonnegative(self.order, "demand order")
        path = checked_path(self.path, "demand path")
        target = checked_positive(self.target_index, "demand target")
        address = checked_positive(self.address, "demand address")
        if type(self.handle) is not TermHandle:
            raise TypeError("demand handle must be exact TermHandle")
        if self.handle.index != address:
            raise ValueError("demand handle index must equal demanded address")
        if address >= target:
            raise ValueError("successful demand must reference the old prefix")
        object.__setattr__(self, "order", order)
        object.__setattr__(self, "path", path)
        object.__setattr__(self, "target_index", target)
        object.__setattr__(self, "address", address)


@dataclass(frozen=True)
class UndefinedTermReference:
    target_index: int
    address: int
    support_start: int
    support_stop: int
    path: tuple[int, ...]
    demand_order: int

    def __post_init__(self) -> None:
        target = checked_positive(self.target_index, "undefined target")
        address = exact_int(self.address, "undefined address")
        start = checked_positive(self.support_start, "support start")
        stop = checked_positive(self.support_stop, "support stop")
        path = checked_path(self.path, "undefined path")
        order = checked_nonnegative(self.demand_order, "undefined demand order")
        if start >= stop or stop != target:
            raise ValueError("undefined-reference support must be [origin,target)")
        if start <= address < stop:
            raise ValueError("UndefinedTermReference address must be absent")
        object.__setattr__(self, "target_index", target)
        object.__setattr__(self, "address", address)
        object.__setattr__(self, "support_start", start)
        object.__setattr__(self, "support_stop", stop)
        object.__setattr__(self, "path", path)
        object.__setattr__(self, "demand_order", order)


@dataclass(frozen=True)
class ResultOutsideCarrier:
    target_index: int
    value: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "target_index", checked_positive(self.target_index, "result target"))
        value = exact_int(self.value, "outside-carrier value")
        if value > 0:
            raise ValueError("ResultOutsideCarrier requires a nonpositive value")
        object.__setattr__(self, "value", value)


@dataclass(frozen=True)
class ResolvedAccess:
    provenance: ProgramProvenance
    target_index: int
    resolved_expression: ResolvedExpression
    demands: tuple[ReadDemand, ...]

    def __post_init__(self) -> None:
        if type(self.provenance) is not ProgramProvenance:
            raise TypeError("resolved access provenance must be exact ProgramProvenance")
        target = checked_positive(self.target_index, "resolved target")
        expression = checked_resolved_expression(self.resolved_expression)
        demands = exact_tuple(self.demands, "resolved demands")
        for order, demand in enumerate(demands):
            if type(demand) is not ReadDemand:
                raise TypeError("resolved demands must contain ReadDemand")
            if demand.order != order or demand.target_index != target:
                raise ValueError("resolved demand order/target mismatch")
        object.__setattr__(self, "target_index", target)
        object.__setattr__(self, "resolved_expression", expression)
        object.__setattr__(self, "demands", demands)


@dataclass(frozen=True)
class AccessFailure:
    provenance: ProgramProvenance
    target_index: int
    old_prefix: NumericPrefix
    successful_demands: tuple[ReadDemand, ...]
    reason: UndefinedTermReference

    def __post_init__(self) -> None:
        if type(self.provenance) is not ProgramProvenance:
            raise TypeError("access failure provenance must be exact ProgramProvenance")
        target = checked_positive(self.target_index, "failure target")
        if type(self.old_prefix) is not NumericPrefix:
            raise TypeError("access failure must retain exact NumericPrefix")
        if self.old_prefix.next_index != target:
            raise ValueError("access failure prefix must end at target")
        demands = exact_tuple(self.successful_demands, "successful demands")
        for order, demand in enumerate(demands):
            if type(demand) is not ReadDemand:
                raise TypeError("successful demands must contain ReadDemand")
            if demand.order != order or demand.target_index != target:
                raise ValueError("failure demand order/target mismatch")
            if self.old_prefix.value_at(demand.address) != demand.handle.value:
                raise ValueError("failure demand handle does not match retained prefix")
        if type(self.reason) is not UndefinedTermReference:
            raise TypeError("access failure reason must be UndefinedTermReference")
        if self.reason.target_index != target or self.reason.demand_order != len(demands):
            raise ValueError("failure reason must follow all successful demands")
        if (
            self.reason.support_start != self.old_prefix.origin
            or self.reason.support_stop != self.old_prefix.next_index
        ):
            raise ValueError("failure reason support must match retained prefix")
        object.__setattr__(self, "target_index", target)
        object.__setattr__(self, "successful_demands", demands)


AccessResult: TypeAlias = ResolvedAccess | AccessFailure


class _DemandFailure(Exception):
    def __init__(self, reason: UndefinedTermReference) -> None:
        super().__init__("undefined historical term")
        self.reason = reason


def read_complete_prefix(
    prefix: object,
    active: object,
) -> NumericPrefix:
    """Reused T37 NEIGHBORHOOD: expose the complete immutable old prefix."""

    if type(prefix) is not NumericPrefix:
        raise TypeError("complete-prefix read requires exact NumericPrefix")
    if type(active) is not End:
        raise TypeError("complete-prefix read source must be the trailing End token")
    if active.next_index != prefix.next_index:
        raise ValueError("active End does not match complete-prefix target")
    return prefix


def resolve_rule_expression(
    program: object,
    prefix: object,
    active: object,
) -> AccessResult:
    """RULE helper: resolve one closed AST against its complete old-prefix read."""

    if type(program) is not RecurrenceProgram:
        raise TypeError("access requires exact RecurrenceProgram")
    if type(prefix) is not NumericPrefix:
        raise TypeError("access requires exact NumericPrefix")
    if type(active) is not End:
        raise TypeError("access source must be the trailing End token")
    if active.next_index != prefix.next_index:
        raise ValueError("active End does not match prefix target")

    provenance = program_provenance(program)
    demands: list[ReadDemand] = []

    def resolve(node: Expression, path: tuple[int, ...]) -> ResolvedExpression:
        checked_expression(node)
        if type(node) is Literal:
            return node
        if type(node) is TargetIndex:
            return Literal(active.next_index)
        if type(node) is Add:
            return Add(tuple(resolve(term, path + (index,)) for index, term in enumerate(node.terms)))
        if type(node) is Sub:
            return Sub(resolve(node.left, path + (0,)), resolve(node.right, path + (1,)))
        if type(node) is Mul:
            return Mul(tuple(resolve(factor, path + (index,)) for index, factor in enumerate(node.factors)))
        if type(node) is TermAt:
            resolved_address = resolve(node.address, path + (0,))
            address = evaluate_resolved(resolved_address)
            if not prefix.origin <= address < active.next_index:
                raise _DemandFailure(
                    UndefinedTermReference(
                        target_index=active.next_index,
                        address=address,
                        support_start=prefix.origin,
                        support_stop=active.next_index,
                        path=path,
                        demand_order=len(demands),
                    )
                )
            handle = TermHandle(address, prefix.value_at(address))
            demands.append(
                ReadDemand(
                    order=len(demands),
                    path=path,
                    target_index=active.next_index,
                    address=address,
                    handle=handle,
                )
            )
            return Literal(handle.value)
        raise TypeError("unreachable expression node")

    try:
        resolved = resolve(program.expression, ())
    except _DemandFailure as failure:
        return AccessFailure(
            provenance,
            active.next_index,
            prefix,
            tuple(demands),
            failure.reason,
        )
    return ResolvedAccess(provenance, active.next_index, resolved, tuple(demands))


@dataclass(frozen=True)
class EndpointReplacement:
    source: End
    replacement: tuple[WordToken, ...]
    provenance: ProgramProvenance
    access: ResolvedAccess

    def __post_init__(self) -> None:
        if type(self.source) is not End:
            raise TypeError("replacement source must be End")
        replacement = exact_tuple(self.replacement, "replacement word")
        if len(replacement) != 2 or type(replacement[0]) is not Val or type(replacement[1]) is not End:
            raise ValueError("endpoint replacement must be exactly Val then End")
        if replacement[0].index != self.source.next_index:
            raise ValueError("new Val must occupy the old endpoint")
        if replacement[1].next_index != self.source.next_index + 1:
            raise ValueError("new End must advance by one")
        if type(self.provenance) is not ProgramProvenance:
            raise TypeError("replacement provenance must be ProgramProvenance")
        if type(self.access) is not ResolvedAccess:
            raise TypeError("replacement access must be ResolvedAccess")
        if self.access.provenance != self.provenance or self.access.target_index != self.source.next_index:
            raise ValueError("replacement access/provenance mismatch")
        object.__setattr__(self, "replacement", replacement)


@dataclass(frozen=True)
class RuleFailure:
    provenance: ProgramProvenance
    source: End
    old_prefix: NumericPrefix
    access: ResolvedAccess
    reason: ResultOutsideCarrier

    def __post_init__(self) -> None:
        if type(self.provenance) is not ProgramProvenance:
            raise TypeError("RULE failure provenance must be ProgramProvenance")
        if type(self.source) is not End:
            raise TypeError("RULE failure source must be End")
        if type(self.old_prefix) is not NumericPrefix:
            raise TypeError("RULE failure must retain exact NumericPrefix")
        if type(self.access) is not ResolvedAccess:
            raise TypeError("RULE failure must retain ResolvedAccess")
        if type(self.reason) is not ResultOutsideCarrier:
            raise TypeError("RULE failure reason must be ResultOutsideCarrier")
        if (
            self.access.provenance != self.provenance
            or self.access.target_index != self.source.next_index
            or self.reason.target_index != self.source.next_index
            or self.old_prefix.next_index != self.source.next_index
        ):
            raise ValueError("RULE failure source/prefix/access/reason mismatch")
        for demand in self.access.demands:
            if self.old_prefix.value_at(demand.address) != demand.handle.value:
                raise ValueError("RULE failure demand handle does not match retained prefix")
        if evaluate_resolved(self.access.resolved_expression) != self.reason.value:
            raise ValueError("RULE failure reason must equal the resolved RULE value")


RuleResult: TypeAlias = EndpointReplacement | RuleFailure


def emit_endpoint_replacement(
    program: object,
    active: object,
    old_prefix: object,
    access: object,
) -> RuleResult:
    """Pure RULE: evaluate already-resolved exact data and emit one splice."""

    if type(program) is not RecurrenceProgram:
        raise TypeError("RULE requires exact RecurrenceProgram")
    if type(active) is not End:
        raise TypeError("RULE source must be End")
    if type(old_prefix) is not NumericPrefix:
        raise TypeError("RULE emitter requires complete NumericPrefix read")
    if type(access) is not ResolvedAccess:
        raise TypeError("RULE requires successful ResolvedAccess")
    provenance = program_provenance(program)
    if access.provenance != provenance or access.target_index != active.next_index:
        raise ValueError("RULE access does not belong to program/source")
    if old_prefix.next_index != active.next_index:
        raise ValueError("RULE emitter prefix does not match source")
    for demand in access.demands:
        if old_prefix.value_at(demand.address) != demand.handle.value:
            raise ValueError("RULE emitter demand handle does not match old prefix")
    value = evaluate_resolved(access.resolved_expression)
    if value <= 0:
        return RuleFailure(
            provenance,
            active,
            old_prefix,
            access,
            ResultOutsideCarrier(active.next_index, value),
        )
    return EndpointReplacement(
        source=active,
        replacement=(Val(active.next_index, value), End(active.next_index + 1)),
        provenance=provenance,
        access=access,
    )


RuleAttempt: TypeAlias = EndpointReplacement | AccessFailure | RuleFailure


def evaluate_recurrence_rule(
    program: object,
    active: object,
    old_prefix: object,
) -> RuleAttempt:
    """Closed RULE: independently evaluate TermAt nodes and emit the endpoint write.

    This merged interpreter deliberately does not call ``resolve_rule_expression``
    or ``emit_endpoint_replacement``.  The audit compares it with that optional
    split compilation as two independently implemented semantic paths.
    """

    if type(program) is not RecurrenceProgram:
        raise TypeError("RULE requires exact RecurrenceProgram")
    if type(active) is not End:
        raise TypeError("RULE source must be End")
    if type(old_prefix) is not NumericPrefix:
        raise TypeError("RULE requires the complete NumericPrefix read")
    if active.next_index != old_prefix.next_index:
        raise ValueError("RULE source does not match complete-prefix target")

    provenance = program_provenance(program)
    demands: list[ReadDemand] = []

    def evaluate(node: Expression, path: tuple[int, ...]) -> tuple[int, ResolvedExpression]:
        checked_expression(node)
        if type(node) is Literal:
            return node.value, node
        if type(node) is TargetIndex:
            return active.next_index, Literal(active.next_index)
        if type(node) is Add:
            values: list[int] = []
            resolved_terms: list[ResolvedExpression] = []
            for index, term in enumerate(node.terms):
                value, resolved = evaluate(term, path + (index,))
                values.append(value)
                resolved_terms.append(resolved)
            return sum(values), Add(tuple(resolved_terms))
        if type(node) is Sub:
            left_value, left = evaluate(node.left, path + (0,))
            right_value, right = evaluate(node.right, path + (1,))
            return left_value - right_value, Sub(left, right)
        if type(node) is Mul:
            value = 1
            resolved_factors: list[ResolvedExpression] = []
            for index, factor in enumerate(node.factors):
                factor_value, resolved = evaluate(factor, path + (index,))
                value *= factor_value
                resolved_factors.append(resolved)
            return value, Mul(tuple(resolved_factors))
        if type(node) is TermAt:
            address, _ = evaluate(node.address, path + (0,))
            if not old_prefix.origin <= address < active.next_index:
                raise _DemandFailure(
                    UndefinedTermReference(
                        active.next_index,
                        address,
                        old_prefix.origin,
                        active.next_index,
                        path,
                        len(demands),
                    )
                )
            handle = TermHandle(address, old_prefix.value_at(address))
            demands.append(
                ReadDemand(
                    len(demands),
                    path,
                    active.next_index,
                    address,
                    handle,
                )
            )
            return handle.value, Literal(handle.value)
        raise TypeError("unreachable expression node")

    try:
        value, resolved_expression = evaluate(program.expression, ())
    except _DemandFailure as failure:
        return AccessFailure(
            provenance,
            active.next_index,
            old_prefix,
            tuple(demands),
            failure.reason,
        )

    access = ResolvedAccess(
        provenance,
        active.next_index,
        resolved_expression,
        tuple(demands),
    )
    if value <= 0:
        return RuleFailure(
            provenance,
            active,
            old_prefix,
            access,
            ResultOutsideCarrier(active.next_index, value),
        )
    return EndpointReplacement(
        active,
        (Val(active.next_index, value), End(active.next_index + 1)),
        provenance,
        access,
    )


def apply_endpoint_splice(
    word: object,
    source_position: object,
    replacement: object,
) -> tuple[WordToken, ...]:
    """The reused T16 exactly-one ordered splice, not a T38 UPDATE."""

    checked = checked_word(word)
    position = checked_nonnegative(source_position, "source position")
    if position != len(checked) - 1:
        raise ValueError("endpoint splice must consume the unique trailing End")
    if type(replacement) is not EndpointReplacement:
        raise TypeError("splice requires exact EndpointReplacement")
    if checked[position] != replacement.source:
        raise ValueError("replacement source does not match old word")
    successor = checked[:position] + replacement.replacement + checked[position + 1 :]
    return checked_word(successor)


@dataclass(frozen=True)
class Advanced:
    changed: bool

    def __post_init__(self) -> None:
        if type(self.changed) is not bool:
            raise TypeError("changed must be exact bool")
        if not self.changed:
            raise ValueError("successful prefix append always changes support")


ErrorReason: TypeAlias = UndefinedTermReference | ResultOutsideCarrier


@dataclass(frozen=True)
class ErrorOutcome:
    reason: ErrorReason

    def __post_init__(self) -> None:
        if type(self.reason) not in (UndefinedTermReference, ResultOutsideCarrier):
            raise TypeError("unknown T38 common error reason")


@dataclass(frozen=True)
class AppendEvent:
    provenance: ProgramProvenance
    before: NumericPrefix
    before_word: tuple[WordToken, ...]
    active_position: int
    active: End
    access: ResolvedAccess
    write: EndpointReplacement
    after_word: tuple[WordToken, ...]
    after: NumericPrefix

    def __post_init__(self) -> None:
        if type(self.provenance) is not ProgramProvenance:
            raise TypeError("event provenance must be ProgramProvenance")
        if type(self.before) is not NumericPrefix or type(self.after) is not NumericPrefix:
            raise TypeError("event endpoints must be NumericPrefix")
        before_word = checked_word(self.before_word)
        after_word = checked_word(self.after_word)
        if decode_prefix(before_word) != self.before or decode_prefix(after_word) != self.after:
            raise ValueError("event word/prefix codec mismatch")
        position = checked_nonnegative(self.active_position, "event active position")
        if type(self.active) is not End or before_word[position] != self.active:
            raise ValueError("event active source mismatch")
        if type(self.access) is not ResolvedAccess or type(self.write) is not EndpointReplacement:
            raise TypeError("event access/write types are invalid")
        if self.access.provenance != self.provenance or self.write.provenance != self.provenance:
            raise ValueError("event provenance mismatch")
        if self.write.access != self.access or self.write.source != self.active:
            raise ValueError("event write does not bind its source/access")
        if self.after.terms != self.before.terms + (self.write.replacement[0].value,):
            raise ValueError("event must preserve all old terms and append exactly one")
        if after_word != apply_endpoint_splice(before_word, position, self.write):
            raise ValueError("event after word is not the declared single splice")
        object.__setattr__(self, "before_word", before_word)
        object.__setattr__(self, "after_word", after_word)
        object.__setattr__(self, "active_position", position)


AttemptWitness: TypeAlias = ResolvedAccess | AccessFailure | RuleFailure
Outcome: TypeAlias = Advanced | ErrorOutcome


@dataclass(frozen=True)
class StepResult:
    successors: tuple[NumericPrefix, ...]
    outcome: Outcome
    event: AppendEvent | None
    attempt: AttemptWitness

    def __post_init__(self) -> None:
        successors = exact_tuple(self.successors, "successors")
        for successor in successors:
            if type(successor) is not NumericPrefix:
                raise TypeError("successors must contain NumericPrefix")
        if type(self.outcome) is Advanced:
            if len(successors) != 1 or type(self.event) is not AppendEvent:
                raise ValueError("Advanced append requires one successor and one event")
            if type(self.attempt) is not ResolvedAccess or self.event.access != self.attempt:
                raise ValueError("Advanced attempt must be the event access witness")
            if self.event.after != successors[0]:
                raise ValueError("event successor mismatch")
        elif type(self.outcome) is ErrorOutcome:
            if successors or self.event is not None:
                raise ValueError("Error must have zero successors and no event")
            if type(self.attempt) is AccessFailure:
                if self.outcome.reason != self.attempt.reason:
                    raise ValueError("access failure/outcome mismatch")
            elif type(self.attempt) is RuleFailure:
                if self.outcome.reason != self.attempt.reason:
                    raise ValueError("rule failure/outcome mismatch")
            else:
                raise TypeError("Error attempt must be AccessFailure or RuleFailure")
        else:
            raise TypeError("unknown StepResult outcome")
        object.__setattr__(self, "successors", successors)


def generic_step(program: object, prefix: object) -> StepResult:
    """Branch-free-by-family T38 specialization of the common typed axes."""

    if type(program) is not RecurrenceProgram:
        raise TypeError("step requires exact RecurrenceProgram")
    if type(prefix) is not NumericPrefix:
        raise TypeError("step requires exact NumericPrefix")
    before_word = encode_prefix(prefix)
    position, active = select_unique_end(before_word)
    reads = read_complete_prefix(prefix, active)
    write = evaluate_recurrence_rule(program, active, reads)
    if type(write) is AccessFailure:
        return StepResult((), ErrorOutcome(write.reason), None, write)
    if type(write) is RuleFailure:
        return StepResult((), ErrorOutcome(write.reason), None, write)
    access = write.access
    after_word = apply_endpoint_splice(before_word, position, write)
    after = decode_prefix(after_word)
    event = AppendEvent(
        provenance=program_provenance(program),
        before=prefix,
        before_word=before_word,
        active_position=position,
        active=active,
        access=access,
        write=write,
        after_word=after_word,
        after=after,
    )
    return StepResult((after,), Advanced(True), event, access)


def verify_append_event(program: object, event: object) -> bool:
    if type(program) is not RecurrenceProgram or type(event) is not AppendEvent:
        return False
    if event.provenance != program_provenance(program):
        return False
    replay = generic_step(program, event.before)
    return type(replay.outcome) is Advanced and replay.event == event


class _DirectUndefined(Exception):
    def __init__(self, address: int, successful: tuple[int, ...]) -> None:
        super().__init__("direct equation demanded an undefined term")
        self.address = address
        self.successful = successful


def direct_row_attempt(
    label: object,
    prefix: object,
) -> tuple[int, tuple[int, ...]] | tuple[UndefinedTermReference, tuple[int, ...]]:
    """Independent literal transcription of the eight source equations."""

    row = exact_str(label, "row label")
    if row not in tuple("abcdefgh"):
        raise ValueError("row label must be a through h")
    if type(prefix) is not NumericPrefix:
        raise TypeError("direct row evaluation requires NumericPrefix")
    n = prefix.next_index
    successful: list[int] = []

    def f(index: object) -> int:
        address = exact_int(index, "direct address")
        if not prefix.origin <= address < n:
            raise _DirectUndefined(address, tuple(successful))
        successful.append(address)
        return prefix.value_at(address)

    try:
        if row == "a":
            value = 1 + f(n - f(n - 1))
        elif row == "b":
            value = 2 + f(n - f(n - 1))
        elif row == "c":
            value = f(f(n - 1)) + f(n - f(n - 1))
        elif row == "d":
            value = f(n - f(n - 1)) + f(n - f(n - 2) - 1)
        elif row == "e":
            value = f(n - f(n - 1)) + f(n - f(n - 2))
        elif row == "f":
            value = f(n - f(n - 1) - 1) + f(n - f(n - 2) - 1)
        elif row == "g":
            value = f(f(n - 1)) + f(n - f(n - 2) - 1)
        else:
            value = f(f(n - 1)) + f(n - 2 * f(n - 1) + 1)
    except _DirectUndefined as failure:
        return (
            UndefinedTermReference(
                target_index=n,
                address=failure.address,
                support_start=prefix.origin,
                support_stop=n,
                path=(),
                demand_order=len(failure.successful),
            ),
            failure.successful,
        )
    return checked_positive(value, "direct next value"), tuple(successful)


def direct_row_terms(label: object, seed: object, final_length: object) -> tuple[int, ...]:
    row = exact_str(label, "row label")
    if type(seed) is not NumericPrefix:
        raise TypeError("direct seed must be NumericPrefix")
    length = checked_positive(final_length, "final length")
    if length < len(seed.terms):
        raise ValueError("final length cannot be shorter than seed")
    prefix = seed
    while len(prefix.terms) < length:
        attempt = direct_row_attempt(row, prefix)
        if type(attempt[0]) is UndefinedTermReference:
            raise RuntimeError("source row unexpectedly demanded an invalid index")
        prefix = NumericPrefix(prefix.origin, prefix.terms + (attempt[0],))
    return prefix.terms


def N() -> TargetIndex:
    return TargetIndex()


def C(value: int) -> Literal:
    return Literal(value)


def plus(*terms: Expression) -> Add:
    return Add(tuple(terms))


def minus(left: Expression, right: Expression) -> Sub:
    return Sub(left, right)


def times(*factors: Expression) -> Mul:
    return Mul(tuple(factors))


def at(address: Expression) -> TermAt:
    return TermAt(address)


def lag(distance: int) -> TermAt:
    return at(minus(N(), C(distance)))


def source_programs() -> tuple[tuple[str, RecurrenceProgram], ...]:
    previous_1 = lag(1)
    previous_2 = lag(2)
    dynamic_1 = at(minus(N(), previous_1))
    return (
        ("a", RecurrenceProgram(plus(C(1), dynamic_1))),
        ("b", RecurrenceProgram(plus(C(2), dynamic_1))),
        ("c", RecurrenceProgram(plus(at(previous_1), dynamic_1))),
        (
            "d",
            RecurrenceProgram(
                plus(
                    dynamic_1,
                    at(minus(minus(N(), previous_2), C(1))),
                )
            ),
        ),
        (
            "e",
            RecurrenceProgram(
                plus(
                    dynamic_1,
                    at(minus(N(), previous_2)),
                )
            ),
        ),
        (
            "f",
            RecurrenceProgram(
                plus(
                    at(minus(minus(N(), previous_1), C(1))),
                    at(minus(minus(N(), previous_2), C(1))),
                )
            ),
        ),
        (
            "g",
            RecurrenceProgram(
                plus(
                    at(previous_1),
                    at(minus(minus(N(), previous_2), C(1))),
                )
            ),
        ),
        (
            "h",
            RecurrenceProgram(
                plus(
                    at(previous_1),
                    at(plus(minus(N(), times(C(2), previous_1)), C(1))),
                )
            ),
        ),
    )


SOURCE_FORMULAS = (
    ("a", "f[n] = 1 + f[n - f[n-1]]", "BOOK:_page_144_Figure_3.jpeg"),
    ("b", "f[n] = 2 + f[n - f[n-1]]", "BOOK:_page_144_Figure_3.jpeg"),
    ("c", "f[n] = f[f[n-1]] + f[n - f[n-1]]", "BOOK:_page_144_Figure_3.jpeg"),
    ("d", "f[n] = f[n - f[n-1]] + f[n - f[n-2] - 1]", "BOOK:_page_144_Figure_3.jpeg"),
    ("e", "f[n] = f[n - f[n-1]] + f[n - f[n-2]]", "BOOK:12722-12724"),
    ("f", "f[n] = f[n - f[n-1] - 1] + f[n - f[n-2] - 1]", "BOOK:_page_144_Figure_3.jpeg"),
    ("g", "f[n] = f[f[n-1]] + f[n - f[n-2] - 1]", "BOOK:_page_144_Figure_3.jpeg"),
    ("h", "f[n] = f[f[n-1]] + f[n - 2 f[n-1] + 1]", "BOOK:_page_144_Figure_3.jpeg"),
)


VISIBLE_SOURCE_TERMS = (
    (
        "a",
        (1,),
        (1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10),
    ),
    (
        "b",
        (1, 1),
        (1, 1, 3, 3, 3, 5, 3, 5, 5, 5, 7, 5, 7, 5, 7, 7, 7, 9, 7, 9, 7, 9, 7, 9, 9, 9, 11, 9, 11, 9, 11, 9, 11, 9, 11, 11, 11, 13, 11, 13, 11, 13, 11, 13),
    ),
    (
        "c",
        (1, 1),
        (1, 1, 2, 2, 3, 4, 4, 4, 5, 6, 7, 7, 8, 8, 8, 8, 9, 10, 11, 12, 12, 13, 14, 14, 15, 15, 15, 16, 16, 16, 16, 16, 17, 18, 19, 20, 21, 21, 22, 23),
    ),
    (
        "d",
        (1, 1),
        (1, 1, 2, 2, 3, 4, 4, 4, 5, 6, 6, 7, 8, 8, 8, 8, 9, 10, 10, 11, 12, 12, 12, 13, 14, 14, 15, 16, 16, 16, 16, 16, 17, 18, 18, 19, 20, 20, 20, 21),
    ),
    (
        "e",
        (1, 1),
        (1, 1, 2, 3, 3, 4, 5, 5, 6, 6, 6, 8, 8, 8, 10, 9, 10, 11, 11, 12, 12, 12, 12, 16, 14, 14, 16, 16, 16, 16, 20, 17, 17, 20, 21, 19, 20, 22, 21, 22),
    ),
    (
        "f",
        (1, 1),
        (1, 1, 2, 2, 2, 4, 3, 4, 4, 4, 8, 5, 5, 8, 8, 6, 8, 12, 8, 11, 9, 9, 10, 13, 16, 9, 12, 20, 10, 12, 23, 12, 15, 21, 13, 17, 18, 19, 19, 22, 21, 19),
    ),
    (
        "g",
        (1, 1),
        (1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8, 9, 10, 10, 10, 11, 13, 15, 15, 14, 15, 16, 16, 16, 16, 16, 16, 16, 17, 18, 18, 18, 18),
    ),
    (
        "h",
        (1, 1),
        (1, 1, 2, 2, 2, 3, 3, 4, 3, 4, 4, 4, 5, 4, 6, 5, 6, 6, 7, 6, 7, 6, 7, 7, 7, 8, 8, 9, 7, 9, 7, 10, 8, 11, 8, 11, 9, 10, 10, 11, 10, 11, 10, 11, 11),
    ),
)


VISIBLE_HORIZONS = (48, 44, 40, 40, 40, 42, 41, 45)


@dataclass(frozen=True)
class SourcePreset:
    label: str
    formula: str
    source_ref: str
    program: RecurrenceProgram
    seed: NumericPrefix
    visible_terms: tuple[int, ...]

    def __post_init__(self) -> None:
        label = exact_str(self.label, "preset label")
        if label not in tuple("abcdefgh"):
            raise ValueError("preset label must be a through h")
        formula = exact_str(self.formula, "preset formula")
        source_ref = exact_str(self.source_ref, "preset source ref")
        if not formula or not source_ref.startswith("BOOK:"):
            raise ValueError("preset formula/source cannot be empty")
        if type(self.program) is not RecurrenceProgram or type(self.seed) is not NumericPrefix:
            raise TypeError("preset program/seed types are invalid")
        visible = exact_tuple(self.visible_terms, "visible terms")
        checked = tuple(checked_positive(value, "visible term") for value in visible)
        if checked[: len(self.seed.terms)] != self.seed.terms:
            raise ValueError("visible row must begin with its exact source seed")
        object.__setattr__(self, "label", label)
        object.__setattr__(self, "formula", formula)
        object.__setattr__(self, "source_ref", source_ref)
        object.__setattr__(self, "visible_terms", checked)


def source_presets() -> tuple[SourcePreset, ...]:
    programs = dict(source_programs())
    formulas = {label: (formula, source) for label, formula, source in SOURCE_FORMULAS}
    rows = {label: (seed, terms) for label, seed, terms in VISIBLE_SOURCE_TERMS}
    return tuple(
        SourcePreset(
            label=label,
            formula=formulas[label][0],
            source_ref=formulas[label][1],
            program=programs[label],
            seed=NumericPrefix(1, rows[label][0]),
            visible_terms=rows[label][1],
        )
        for label in "abcdefgh"
    )


@dataclass(frozen=True)
class RunTrace:
    provenance: ProgramProvenance
    initial: NumericPrefix
    requested_events: int
    states: tuple[NumericPrefix, ...]
    events: tuple[AppendEvent, ...]
    outcome: Advanced | ErrorOutcome | None
    terminal_attempt: AccessFailure | RuleFailure | None

    def __post_init__(self) -> None:
        if type(self.provenance) is not ProgramProvenance:
            raise TypeError("trace provenance must be ProgramProvenance")
        if type(self.initial) is not NumericPrefix:
            raise TypeError("trace initial must be NumericPrefix")
        requested = checked_nonnegative(self.requested_events, "requested events")
        states = exact_tuple(self.states, "trace states")
        events = exact_tuple(self.events, "trace events")
        if not states or states[0] != self.initial:
            raise ValueError("trace states must begin with exact initial prefix")
        if len(states) != len(events) + 1:
            raise ValueError("trace requires one more state than committed events")
        for index, event in enumerate(events):
            if type(event) is not AppendEvent:
                raise TypeError("trace events must contain AppendEvent")
            if event.provenance != self.provenance:
                raise ValueError("trace event provenance mismatch")
            if event.before != states[index] or event.after != states[index + 1]:
                raise ValueError("trace event/state continuity failure")
        if self.outcome is None:
            if requested != 0 or events or self.terminal_attempt is not None:
                raise ValueError("empty trace marker is valid only for a zero-event request")
        elif type(self.outcome) is Advanced:
            if requested == 0 or len(events) != requested or self.terminal_attempt is not None:
                raise ValueError("completed trace must commit every requested event")
        elif type(self.outcome) is ErrorOutcome:
            if len(events) >= requested or type(self.terminal_attempt) not in (AccessFailure, RuleFailure):
                raise ValueError("error trace must stop before requested event count")
            if self.terminal_attempt.provenance != self.provenance:
                raise ValueError("trace terminal attempt provenance mismatch")
            if self.terminal_attempt.old_prefix != states[-1]:
                raise ValueError("trace terminal attempt must retain the final state")
            reason = self.terminal_attempt.reason
            if reason != self.outcome.reason:
                raise ValueError("trace error reason/attempt mismatch")
        else:
            raise TypeError("trace outcome must be None, Advanced, or ErrorOutcome")
        object.__setattr__(self, "requested_events", requested)
        object.__setattr__(self, "states", states)
        object.__setattr__(self, "events", events)


def run(program: object, initial: object, requested_events: object) -> RunTrace:
    if type(program) is not RecurrenceProgram:
        raise TypeError("run requires exact RecurrenceProgram")
    if type(initial) is not NumericPrefix:
        raise TypeError("run requires exact NumericPrefix")
    requested = checked_nonnegative(requested_events, "requested events")
    states = [initial]
    events: list[AppendEvent] = []
    current = initial
    for _ in range(requested):
        result = generic_step(program, current)
        if type(result.outcome) is ErrorOutcome:
            return RunTrace(
                program_provenance(program),
                initial,
                requested,
                tuple(states),
                tuple(events),
                result.outcome,
                result.attempt,
            )
        events.append(result.event)
        current = result.successors[0]
        states.append(current)
    return RunTrace(
        program_provenance(program),
        initial,
        requested,
        tuple(states),
        tuple(events),
        None if requested == 0 else Advanced(True),
        None,
    )


def verify_trace(program: object, trace: object) -> bool:
    if type(program) is not RecurrenceProgram or type(trace) is not RunTrace:
        return False
    if trace.provenance != program_provenance(program):
        return False
    replay = run(program, trace.initial, trace.requested_events)
    return replay == trace and all(verify_append_event(program, event) for event in trace.events)


CompactAppendRecord: TypeAlias = tuple[int, ResolvedAccess]
CompactTraceProjection: TypeAlias = tuple[
    ProgramProvenance,
    NumericPrefix,
    int,
    tuple[CompactAppendRecord, ...],
    AccessFailure | RuleFailure | None,
]


def compact_trace_projection(trace: object) -> CompactTraceProjection:
    """Project a full validation trace to D073 seed-plus-append reconstruction data."""

    if type(trace) is not RunTrace:
        raise TypeError("compact projection requires exact RunTrace")
    records = tuple((event.after.terms[-1], event.access) for event in trace.events)
    return (
        trace.provenance,
        trace.initial,
        trace.requested_events,
        records,
        trace.terminal_attempt,
    )


def replay_compact_trace(program: object, value: object) -> RunTrace:
    """Losslessly rebuild every full prefix/event from a compact projection."""

    if type(program) is not RecurrenceProgram:
        raise TypeError("compact replay requires exact RecurrenceProgram")
    projection = exact_tuple(value, "compact trace projection")
    if len(projection) != 5:
        raise ValueError("compact trace projection requires five fields")
    provenance, initial, requested_raw, records_raw, terminal_attempt = projection
    if type(provenance) is not ProgramProvenance or provenance != program_provenance(program):
        raise ValueError("compact trace provenance mismatch")
    if type(initial) is not NumericPrefix:
        raise TypeError("compact trace initial state must be NumericPrefix")
    requested = checked_nonnegative(requested_raw, "compact requested events")
    records = exact_tuple(records_raw, "compact append records")
    if terminal_attempt is not None and type(terminal_attempt) not in (AccessFailure, RuleFailure):
        raise TypeError("compact terminal attempt has an invalid type")
    if len(records) > requested:
        raise ValueError("compact trace contains more records than requested")
    if terminal_attempt is None and len(records) != requested:
        raise ValueError("completed compact trace must contain every requested record")
    if terminal_attempt is not None and len(records) >= requested:
        raise ValueError("partial compact trace must stop before its requested horizon")

    states = [initial]
    events: list[AppendEvent] = []
    current = initial
    for raw_record in records:
        record = exact_tuple(raw_record, "compact append record")
        if len(record) != 2:
            raise ValueError("compact append record requires next value and access witness")
        next_value = checked_positive(record[0], "compact append value")
        access = record[1]
        if type(access) is not ResolvedAccess:
            raise TypeError("compact append access must be ResolvedAccess")
        step = generic_step(program, current)
        if type(step.outcome) is not Advanced or type(step.event) is not AppendEvent:
            raise ValueError("compact append record claims advancement where evaluation fails")
        if step.attempt != access or step.successors[0].terms[-1] != next_value:
            raise ValueError("compact append record does not match deterministic replay")
        events.append(step.event)
        current = step.successors[0]
        states.append(current)

    if terminal_attempt is None:
        outcome: Advanced | ErrorOutcome | None = None if requested == 0 else Advanced(True)
    else:
        failed = generic_step(program, current)
        if type(failed.outcome) is not ErrorOutcome or failed.attempt != terminal_attempt:
            raise ValueError("compact terminal attempt does not match deterministic replay")
        outcome = failed.outcome

    trace = RunTrace(
        provenance,
        initial,
        requested,
        tuple(states),
        tuple(events),
        outcome,
        terminal_attempt,
    )
    if compact_trace_projection(trace) != projection:
        raise ValueError("compact projection was not canonical")
    return trace


def binary_digits(value: object) -> tuple[int, ...]:
    integer = checked_positive(value, "binary digit input")
    return tuple(int(character) for character in bin(integer)[2:])


def from_binary_digits(digits: object) -> int:
    sequence = exact_tuple(digits, "binary digits")
    if not sequence:
        raise ValueError("binary digits cannot be empty")
    value = 0
    for digit in sequence:
        exact_digit = exact_int(digit, "binary digit")
        if exact_digit not in (0, 1):
            raise ValueError("binary digits must be zero or one")
        value = 2 * value + exact_digit
    return value


def page131_g(digits: object) -> int:
    """Exact transcription of the Book's recursive binary-word observer."""

    sequence = exact_tuple(digits, "g digits")
    if not sequence or sequence[0] != 1:
        raise ValueError("g requires canonical positive binary digits")
    if any(type(digit) is not int or digit not in (0, 1) for digit in sequence):
        raise ValueError("g digits must be exact binary integers")
    if all(digit == 1 for digit in sequence):
        return 1
    if all(digit == 0 for digit in sequence[1:]):
        return 0
    suffix_plus_one = from_binary_digits(sequence[1:]) + 1
    return 1 + page131_g(binary_digits(suffix_plus_one))


def page131_case_d_value(index: object) -> int:
    n = checked_positive(index, "case-d observer index")
    numerator = n + page131_g(binary_digits(n))
    if numerator % 2:
        raise AssertionError("page-131 case-d formula must yield an integer")
    return numerator // 2


def exponent_of_two(value: object) -> int:
    integer = checked_positive(value, "two-adic exponent input")
    exponent = 0
    while integer % 2 == 0:
        integer //= 2
        exponent += 1
    return exponent


def raw_12738_multiplicity_list(maximum_value: object) -> tuple[int, ...]:
    maximum = checked_positive(maximum_value, "maximum multiplicity value")
    return tuple(
        value
        for value in range(1, maximum + 1)
        for _ in range(exponent_of_two(value) + 1)
    )


def repaired_12738_case_d_list(maximum_value: object) -> tuple[int, ...]:
    """The one guarded repair: prepend the omitted second initial ``1``."""

    return (1,) + raw_12738_multiplicity_list(maximum_value)


def page131_case_d_last_index(value: object) -> int:
    m = checked_positive(value, "case-d value")
    return 2 * m + 1 - m.bit_count()


def factorial_two_exponent(value: object) -> int:
    m = checked_positive(value, "factorial observer value")
    n = 2 * m
    total = 0
    divisor = 2
    while divisor <= n:
        total += n // divisor
        divisor *= 2
    return total


def must_raise(exception_type: type[BaseException], thunk: object) -> int:
    if type(exception_type) is not type or not issubclass(exception_type, BaseException):
        raise TypeError("exception_type must be an exception class")
    if not callable(thunk):
        raise TypeError("thunk must be callable")
    try:
        thunk()
    except exception_type:
        return 1
    raise AssertionError(f"expected {exception_type.__name__}")


def demand_addresses(access: object) -> tuple[int, ...]:
    if type(access) is ResolvedAccess:
        return tuple(demand.address for demand in access.demands)
    if type(access) is AccessFailure:
        return tuple(demand.address for demand in access.successful_demands)
    raise TypeError("demand_addresses requires an access result")


def audit_complete_prefix_rule_factorization() -> tuple[int, int, int, int, int, int, int]:
    """Prove computed lookup is RULE work over a reused complete-prefix read.

    ``resolve_rule_expression`` plus ``emit_endpoint_replacement`` is retained as
    an optional compiled factorization.  It must agree exactly with the single
    closed RULE evaluator; it is not a required NEIGHBORHOOD semantic.
    """

    compiled_calls = 0

    def compiled_factor_step(program: RecurrenceProgram, prefix: NumericPrefix) -> StepResult:
        nonlocal compiled_calls
        compiled_calls += 1
        before_word = encode_prefix(prefix)
        position, active = select_unique_end(before_word)
        reads = read_complete_prefix(prefix, active)
        resolved = resolve_rule_expression(program, reads, active)
        if type(resolved) is AccessFailure:
            return StepResult((), ErrorOutcome(resolved.reason), None, resolved)
        write = emit_endpoint_replacement(program, active, reads, resolved)
        if type(write) is RuleFailure:
            return StepResult((), ErrorOutcome(write.reason), None, write)
        after_word = apply_endpoint_splice(before_word, position, write)
        after = decode_prefix(after_word)
        event = AppendEvent(
            program_provenance(program),
            prefix,
            before_word,
            position,
            active,
            resolved,
            write,
            after_word,
            after,
        )
        return StepResult((after,), Advanced(True), event, resolved)

    def compare(program: RecurrenceProgram, prefix: NumericPrefix) -> StepResult:
        merged = generic_step(program, prefix)
        compiled = compiled_factor_step(program, prefix)
        assert merged == compiled
        return merged

    visible = 0
    long = 0
    partial = 0
    fixed_lag = 0
    bigint = 0
    failures = 0

    for preset in source_presets():
        requested = len(preset.visible_terms) - len(preset.seed.terms)
        trace = run(preset.program, preset.seed, requested)
        for event in trace.events:
            assert compare(preset.program, event.before).event == event
            visible += 1

        long_trace = run(preset.program, preset.seed, 256 - len(preset.seed.terms))
        for event in long_trace.events:
            assert compare(preset.program, event.before).event == event
            long += 1

    partial_cases = (
        (RecurrenceProgram(at(at(lag(1)))), NumericPrefix(1, (2, 1))),
        (RecurrenceProgram(plus(lag(1), lag(1))), NumericPrefix(1, (1, 1))),
        (RecurrenceProgram(lag(1)), NumericPrefix(1, (1, 1))),
        (RecurrenceProgram(lag(2)), NumericPrefix(1, (1, 1))),
        (RecurrenceProgram(at(C(0))), NumericPrefix(1, (7,))),
        (RecurrenceProgram(at(C(-1))), NumericPrefix(1, (7,))),
        (RecurrenceProgram(at(N())), NumericPrefix(1, (7,))),
        (RecurrenceProgram(at(plus(N(), C(1)))), NumericPrefix(1, (7,))),
        (RecurrenceProgram(Sub(at(C(-1)), at(C(-1)))), NumericPrefix(1, (9,))),
        (RecurrenceProgram(plus(lag(1), at(C(0)))), NumericPrefix(1, (5,))),
        (RecurrenceProgram(plus(at(C(0)), lag(1))), NumericPrefix(1, (5,))),
        (RecurrenceProgram(at(at(C(0)))), NumericPrefix(1, (5,))),
        (RecurrenceProgram(at(lag(1))), NumericPrefix(1, (7,))),
        (RecurrenceProgram(Sub(C(1), lag(1))), NumericPrefix(1, (1,))),
    )
    for program, prefix in partial_cases:
        result = compare(program, prefix)
        failures += type(result.outcome) is ErrorOutcome
        partial += 1

    for length in range(2, 18):
        terms = tuple((index * index % 17) + 1 for index in range(1, length + 1))
        prefix = NumericPrefix(1, terms)
        for distance in range(1, min(length, 7) + 1):
            assert type(compare(RecurrenceProgram(lag(distance)), prefix).outcome) is Advanced
            fixed_lag += 1

    huge = (1 << 4096) + (1 << 2048) + 123456789
    bigint_program = RecurrenceProgram(plus(C(huge), lag(1)))
    bigint_trace = run(bigint_program, NumericPrefix(1, (1,)), 64)
    for event in bigint_trace.events:
        assert compare(bigint_program, event.before).event == event
        bigint += 1

    total = visible + long + partial + fixed_lag + bigint
    assert (visible, long, partial, fixed_lag, bigint, failures, total) == (
        325,
        2_033,
        14,
        97,
        64,
        10,
        2_533,
    )
    assert compiled_calls == total
    return visible, long, partial, fixed_lag, bigint, failures, total


def audit_visible_source_rows() -> tuple[int, int, int, int, int]:
    events = 0
    demands = 0
    event_replays = 0
    codec_commutations = 0
    nested_demands = 0

    presets = source_presets()
    assert tuple(len(preset.visible_terms) for preset in presets) == VISIBLE_HORIZONS
    assert tuple(preset.label for preset in presets) == tuple("abcdefgh")

    for preset in presets:
        direct = direct_row_terms(preset.label, preset.seed, len(preset.visible_terms))
        assert direct == preset.visible_terms
        requested = len(preset.visible_terms) - len(preset.seed.terms)
        trace = run(preset.program, preset.seed, requested)
        assert type(trace.outcome) is Advanced
        assert trace.states[-1].terms == preset.visible_terms
        assert verify_trace(preset.program, trace)
        assert len(trace.states) == requested + 1
        assert len(trace.events) == requested
        events += requested

        for event_index, event in enumerate(trace.events):
            direct_attempt = direct_row_attempt(preset.label, event.before)
            assert type(direct_attempt[0]) is int
            assert direct_attempt[0] == event.after.terms[-1]
            assert direct_attempt[1] == demand_addresses(event.access)
            assert event.before_word == encode_prefix(event.before)
            assert event.after_word == encode_prefix(event.after)
            assert decode_prefix(event.after_word) == event.after
            assert event.after.terms[:-1] == event.before.terms
            assert event.after.next_index == event.before.next_index + 1
            assert event.access.target_index == event.before.next_index
            assert all(
                event.before.origin <= demand.address < event.before.next_index
                for demand in event.access.demands
            )
            assert all(demand.order == index for index, demand in enumerate(event.access.demands))
            assert verify_append_event(preset.program, event)
            assert trace.states[event_index] == event.before
            event_replays += 1
            demands += len(event.access.demands)
            codec_commutations += 1
            nested_demands += sum(len(demand.path) >= 2 for demand in event.access.demands)

    assert events == 325
    assert event_replays == events == codec_commutations
    assert demands > 1_000
    assert nested_demands > 0
    return events, demands, event_replays, codec_commutations, nested_demands


def audit_long_source_traces() -> tuple[int, int, int, int, int, int]:
    final_length = 256
    total_events = 0
    total_demands = 0
    minimum_address = 10**9
    maximum_lag = 0
    maximum_value = 0
    trace_replays = 0

    for preset in source_presets():
        requested = final_length - len(preset.seed.terms)
        trace = run(preset.program, preset.seed, requested)
        assert type(trace.outcome) is Advanced
        assert len(trace.states[-1].terms) == final_length
        assert direct_row_terms(preset.label, preset.seed, final_length) == trace.states[-1].terms
        assert verify_trace(preset.program, trace)
        trace_replays += 1
        total_events += len(trace.events)
        for event in trace.events:
            assert event.after.terms[-1] > 0
            maximum_value = max(maximum_value, event.after.terms[-1])
            for demand in event.access.demands:
                minimum_address = min(minimum_address, demand.address)
                maximum_lag = max(maximum_lag, event.before.next_index - demand.address)
                assert demand.handle.value == event.before.value_at(demand.address)
                assert demand.address < event.before.next_index
                total_demands += 1

    assert total_events == 2_033
    assert total_demands > 6_000
    assert minimum_address == 1
    assert maximum_lag > 100
    assert trace_replays == 8
    return total_events, total_demands, minimum_address, maximum_lag, maximum_value, trace_replays


def audit_dependent_access_and_partiality() -> tuple[int, int, int, int, int, int]:
    cases = 0
    errors = 0
    successful_demands = 0
    repeated_occurrences = 0
    old_snapshot_guards = 0
    order_guards = 0

    nested_program = RecurrenceProgram(at(at(lag(1))))
    nested_prefix = NumericPrefix(1, (2, 1))
    nested_result = generic_step(nested_program, nested_prefix)
    assert type(nested_result.outcome) is Advanced
    assert nested_result.successors[0].terms == (2, 1, 1)
    assert type(nested_result.attempt) is ResolvedAccess
    assert demand_addresses(nested_result.attempt) == (2, 1, 2)
    assert tuple(demand.path for demand in nested_result.attempt.demands) == ((0, 0), (0,), ())
    cases += 1
    successful_demands += 3

    repeated_program = RecurrenceProgram(plus(lag(1), lag(1)))
    repeated_result = generic_step(repeated_program, NumericPrefix(1, (1, 1)))
    assert type(repeated_result.outcome) is Advanced
    assert type(repeated_result.attempt) is ResolvedAccess
    repeated = repeated_result.attempt.demands
    assert len(repeated) == 2
    assert repeated[0].address == repeated[1].address == 2
    assert repeated[0].handle == repeated[1].handle
    assert repeated[0].path != repeated[1].path
    repeated_occurrences += 2
    successful_demands += 2
    cases += 1

    equal_values = NumericPrefix(1, (1, 1))
    last = generic_step(RecurrenceProgram(lag(1)), equal_values)
    older = generic_step(RecurrenceProgram(lag(2)), equal_values)
    assert last.successors[0].terms[-1] == older.successors[0].terms[-1] == 1
    assert type(last.attempt) is ResolvedAccess and last.attempt.demands[0].address == 2
    assert type(older.attempt) is ResolvedAccess and older.attempt.demands[0].address == 1
    cases += 2
    successful_demands += 2

    invalid_expressions = (
        (at(C(0)), 0),
        (at(C(-1)), -1),
        (at(N()), 2),
        (at(plus(N(), C(1))), 3),
    )
    for expression, expected_address in invalid_expressions:
        before = NumericPrefix(1, (7,))
        result = generic_step(RecurrenceProgram(expression), before)
        assert type(result.outcome) is ErrorOutcome
        assert type(result.outcome.reason) is UndefinedTermReference
        assert result.outcome.reason.address == expected_address
        assert result.outcome.reason.support_start == 1
        assert result.outcome.reason.support_stop == 2
        assert result.successors == () and result.event is None
        assert type(result.attempt) is AccessFailure
        assert result.attempt.successful_demands == ()
        errors += 1
        cases += 1
    old_snapshot_guards += 2  # current and future reads above

    # The source's explicit counterexample: eager leftmost-innermost demand
    # rejects f[-1]-f[-1]; algebraic cancellation must not produce zero.
    cancellation = RecurrenceProgram(Sub(at(C(-1)), at(C(-1))))
    cancelled = generic_step(cancellation, NumericPrefix(1, (9,)))
    assert type(cancelled.outcome) is ErrorOutcome
    assert cancelled.outcome.reason.address == -1
    assert cancelled.outcome.reason.path == (0,)
    assert cancelled.outcome.reason.demand_order == 0
    assert cancelled.attempt.successful_demands == ()
    errors += 1
    cases += 1
    order_guards += 1

    valid_then_invalid = RecurrenceProgram(plus(lag(1), at(C(0))))
    attempt = generic_step(valid_then_invalid, NumericPrefix(1, (5,)))
    assert type(attempt.outcome) is ErrorOutcome
    assert demand_addresses(attempt.attempt) == (1,)
    assert attempt.outcome.reason.path == (1,)
    assert attempt.outcome.reason.demand_order == 1
    successful_demands += 1
    errors += 1
    cases += 1
    order_guards += 1

    invalid_then_valid = RecurrenceProgram(plus(at(C(0)), lag(1)))
    reverse_attempt = generic_step(invalid_then_valid, NumericPrefix(1, (5,)))
    assert type(reverse_attempt.outcome) is ErrorOutcome
    assert reverse_attempt.attempt.successful_demands == ()
    assert reverse_attempt.outcome.reason.path == (0,)
    errors += 1
    cases += 1
    order_guards += 1

    inner_invalid = RecurrenceProgram(at(at(C(0))))
    inner_attempt = generic_step(inner_invalid, NumericPrefix(1, (5,)))
    assert type(inner_attempt.outcome) is ErrorOutcome
    assert inner_attempt.outcome.reason.path == (0,)
    assert inner_attempt.attempt.successful_demands == ()
    errors += 1
    cases += 1
    order_guards += 1

    inner_valid_outer_invalid = RecurrenceProgram(at(lag(1)))
    outer_attempt = generic_step(inner_valid_outer_invalid, NumericPrefix(1, (7,)))
    assert type(outer_attempt.outcome) is ErrorOutcome
    assert demand_addresses(outer_attempt.attempt) == (1,)
    assert outer_attempt.outcome.reason.address == 7
    assert outer_attempt.outcome.reason.path == ()
    successful_demands += 1
    errors += 1
    cases += 1

    nonpositive_result = generic_step(
        RecurrenceProgram(Sub(C(1), lag(1))),
        NumericPrefix(1, (1,)),
    )
    assert type(nonpositive_result.outcome) is ErrorOutcome
    assert type(nonpositive_result.outcome.reason) is ResultOutsideCarrier
    assert nonpositive_result.outcome.reason.value == 0
    assert nonpositive_result.successors == () and nonpositive_result.event is None
    assert type(nonpositive_result.attempt) is RuleFailure
    assert nonpositive_result.attempt.reason == nonpositive_result.outcome.reason
    assert demand_addresses(nonpositive_result.attempt.access) == (1,)
    same_reason_other_program = generic_step(
        RecurrenceProgram(Sub(C(2), plus(lag(1), C(1)))),
        NumericPrefix(1, (1,)),
    )
    assert same_reason_other_program.outcome.reason == nonpositive_result.outcome.reason
    assert same_reason_other_program.attempt != nonpositive_result.attempt
    assert same_reason_other_program.attempt.access.provenance != nonpositive_result.attempt.access.provenance
    successful_demands += 1
    errors += 1
    cases += 1

    assert errors == 10
    return cases, errors, successful_demands, repeated_occurrences, old_snapshot_guards, order_guards


def audit_lossiness_and_fixed_lag_boundary() -> tuple[int, int, int, int, int]:
    fixed_lag_commutations = 0
    window_counterexamples = 0
    maximum_window = 64
    dynamic_lags: list[int] = []

    # Every T37 fixed lag is the named restriction TermAt(TargetIndex-k).
    for length in range(2, 18):
        terms = tuple((index * index % 17) + 1 for index in range(1, length + 1))
        prefix = NumericPrefix(1, terms)
        for distance in range(1, min(length, 7) + 1):
            program = RecurrenceProgram(lag(distance))
            result = generic_step(program, prefix)
            assert type(result.outcome) is Advanced
            assert result.successors[0].terms[-1] == prefix.value_at(prefix.next_index - distance)
            assert type(result.attempt) is ResolvedAccess
            assert demand_addresses(result.attempt) == (prefix.next_index - distance,)
            fixed_lag_commutations += 1

    row_a = dict(source_programs())["a"]
    prefix = NumericPrefix(1, (1,))
    for _ in range(32):
        result = generic_step(row_a, prefix)
        assert type(result.attempt) is ResolvedAccess
        first = result.attempt.demands[0]
        second = result.attempt.demands[1]
        assert first.address == prefix.next_index - 1
        dynamic_lags.append(prefix.next_index - second.address)
        prefix = result.successors[0]
    assert len(set(dynamic_lags)) > 4
    assert dynamic_lags[:4] == [1, 2, 2, 3]

    # For every tested bounded suffix, two complete prefixes share that suffix
    # but row (c)'s f[f[n-1]] reaches index 1 and distinguishes them.
    row_c = dict(source_programs())["c"]
    for window in range(1, maximum_window + 1):
        shared_suffix = tuple([2] * (window - 1) + [1])
        left = NumericPrefix(1, (7,) + shared_suffix)
        right = NumericPrefix(1, (8,) + shared_suffix)
        assert left.terms[-window:] == right.terms[-window:]
        left_step = generic_step(row_c, left)
        right_step = generic_step(row_c, right)
        assert type(left_step.outcome) is Advanced and type(right_step.outcome) is Advanced
        assert left_step.successors[0].terms[-1] == 8
        assert right_step.successors[0].terms[-1] == 9
        window_counterexamples += 1

    newest_scalar_counterexample = 1
    assert NumericPrefix(1, (7, 2, 1)).terms[-1] == NumericPrefix(1, (8, 2, 1)).terms[-1]
    assert generic_step(row_c, NumericPrefix(1, (7, 2, 1))).successors[0].terms[-1] != generic_step(
        row_c, NumericPrefix(1, (8, 2, 1))
    ).successors[0].terms[-1]

    assert fixed_lag_commutations > 80
    assert window_counterexamples == maximum_window
    return fixed_lag_commutations, window_counterexamples, maximum_window, newest_scalar_counterexample, len(set(dynamic_lags))


def audit_page131_observers() -> tuple[int, int, int, int, int, int]:
    formula_checks = 4_096
    seed = NumericPrefix(1, (1, 1))
    # The formula is an observer, so compare it to an independently generated
    # term stream without materializing thousands of nested semantic prefixes.
    values = direct_row_terms("d", seed, formula_checks)
    for index, value in enumerate(values, start=1):
        assert page131_case_d_value(index) == value

    maximum_value = values[-1]
    repaired = repaired_12738_case_d_list(maximum_value)
    raw = raw_12738_multiplicity_list(maximum_value)
    assert raw[:8] == (1, 2, 2, 3, 4, 4, 4, 5)
    assert repaired[:9] == (1, 1, 2, 2, 3, 4, 4, 4, 5)
    assert repaired[1:] == raw
    assert repaired[: len(values)] == values
    assert raw != values[: len(raw)]

    last_index_checks = 1_024
    for value in range(1, last_index_checks + 1):
        expected = page131_case_d_last_index(value)
        assert expected == len(repaired_12738_case_d_list(value))
        assert expected == factorial_two_exponent(value) + 1

    defect_guards = 4
    assert RAW_12738_SPELLING == "Flatten[Table[n, {IntegerExponent[n, 2] + 1}], {n, m}]]"
    assert GUARDED_12738_REPAIR[0] == "BOOK:12738"
    assert raw[0] == 1 and repaired[:2] == (1, 1)
    assert page131_case_d_last_index(1) == 2
    return formula_checks, last_index_checks, len(raw), len(repaired), maximum_value, defect_guards


def audit_arbitrary_precision() -> tuple[int, int, int, int]:
    huge = (1 << 4096) + (1 << 2048) + 123456789
    program = RecurrenceProgram(plus(C(huge), lag(1)))
    trace = run(program, NumericPrefix(1, (1,)), 64)
    assert type(trace.outcome) is Advanced
    assert trace.states[-1].terms[-1] == 1 + 64 * huge
    assert trace.states[-1].terms[-1].bit_length() > 4096
    assert verify_trace(program, trace)
    for index, state in enumerate(trace.states):
        assert state.terms[-1] == 1 + index * huge
    maximum = trace.states[-1].terms[-1]
    return len(trace.events), maximum.bit_length(), len(str(maximum)), len(trace.events)


def audit_structural_identity_and_replay() -> tuple[int, int, int, int, int, int]:
    programs = dict(source_programs())
    keys = tuple(structural_program_key(program) for program in programs.values())
    identifiers = tuple(program_provenance(program).identifier for program in programs.values())
    assert len(set(keys)) == 8
    assert len(set(identifiers)) == 8

    order_left = RecurrenceProgram(plus(lag(1), lag(2)))
    order_right = RecurrenceProgram(plus(lag(2), lag(1)))
    assert structural_program_key(order_left) != structural_program_key(order_right)
    assert generic_step(order_left, NumericPrefix(1, (1, 1))).successors == generic_step(
        order_right, NumericPrefix(1, (1, 1))
    ).successors

    event = generic_step(programs["e"], NumericPrefix(1, (1, 1))).event
    assert verify_append_event(programs["e"], event)
    cross_rejections = 0
    for label, program in programs.items():
        if label == "e":
            continue
        assert not verify_append_event(program, event)
        cross_rejections += 1

    trace = run(programs["g"], NumericPrefix(1, (1, 1)), 128)
    assert verify_trace(programs["g"], trace)
    assert not verify_trace(programs["h"], trace)
    cross_rejections += 1

    serialization_roundtrips = 0
    for program in (*programs.values(), order_left, order_right):
        provenance = program_provenance(program)
        assert ProgramProvenance(provenance.structural_key, provenance.identifier) == provenance
        assert checked_program_key(provenance.structural_key) == provenance.structural_key
        serialization_roundtrips += 1

    ordered_program_guards = 2
    assert expression_key(order_left.expression) != expression_key(order_right.expression)
    left_attempt = generic_step(order_left, NumericPrefix(1, (2, 3))).attempt
    right_attempt = generic_step(order_right, NumericPrefix(1, (2, 3))).attempt
    assert type(left_attempt) is ResolvedAccess and demand_addresses(left_attempt) == (2, 1)
    assert type(right_attempt) is ResolvedAccess and demand_addresses(right_attempt) == (1, 2)
    return len(keys), len(identifiers), cross_rejections, serialization_roundtrips, ordered_program_guards, len(trace.events)


def audit_trace_shape_and_error_retention() -> tuple[int, int, int, int, int, int]:
    program = dict(source_programs())["c"]
    horizons = (0, 1, 2, 7, 31, 127)
    events = 0
    states = 0
    replays = 0
    for horizon in horizons:
        trace = run(program, NumericPrefix(1, (1, 1)), horizon)
        assert len(trace.events) == horizon
        assert len(trace.states) == horizon + 1
        assert len(trace.states[-1].terms) == 2 + horizon
        assert verify_trace(program, trace)
        events += len(trace.events)
        states += len(trace.states)
        replays += len(trace.events)

    partial = RecurrenceProgram(at(minus(N(), lag(1))))
    # Seed 1 advances forever for this expression, while seed 2 fails on the
    # first attempted event; both are well-formed configurations/programs.
    success = run(partial, NumericPrefix(1, (1,)), 3)
    assert type(success.outcome) is Advanced
    failure = run(partial, NumericPrefix(1, (2,)), 5)
    assert type(failure.outcome) is ErrorOutcome
    assert failure.states == (NumericPrefix(1, (2,)),)
    assert failure.events == ()
    assert type(failure.terminal_attempt) is AccessFailure
    assert failure.terminal_attempt.reason.address == 0
    assert verify_trace(partial, failure)

    delayed = RecurrenceProgram(at(minus(lag(1), C(1))))
    delayed_failure = run(delayed, NumericPrefix(1, (1, 2)), 5)
    assert type(delayed_failure.outcome) is ErrorOutcome
    assert len(delayed_failure.events) == 1
    assert len(delayed_failure.states) == 2
    assert delayed_failure.states[-1].terms == (1, 2, 1)
    assert type(delayed_failure.terminal_attempt) is AccessFailure
    assert delayed_failure.terminal_attempt.reason.address == 0
    assert verify_trace(delayed, delayed_failure)

    no_partial_events = 2
    retained_last_states = 2
    return len(horizons), events, states, replays, no_partial_events, retained_last_states


def audit_compact_trace_reconstruction() -> tuple[int, int, int, int, int, int]:
    full_traces: list[tuple[RecurrenceProgram, RunTrace]] = []
    for preset in source_presets():
        requested = len(preset.visible_terms) - len(preset.seed.terms)
        full_traces.append((preset.program, run(preset.program, preset.seed, requested)))

    row_c = dict(source_programs())["c"]
    zero = run(row_c, NumericPrefix(1, (1, 1)), 0)
    assert zero.outcome is None
    full_traces.append((row_c, zero))

    partial_program = RecurrenceProgram(Sub(lag(1), C(1)))
    partial = run(partial_program, NumericPrefix(1, (2,)), 5)
    assert type(partial.outcome) is ErrorOutcome
    assert type(partial.terminal_attempt) is RuleFailure
    assert demand_addresses(partial.terminal_attempt.access) == (2,)
    assert len(partial.events) == 1
    full_traces.append((partial_program, partial))

    record_count = 0
    full_prefix_cells = 0
    compact_value_cells = 0
    terminal_replays = 0
    for program, trace in full_traces:
        projection = compact_trace_projection(trace)
        rebuilt = replay_compact_trace(program, projection)
        assert rebuilt == trace
        assert compact_trace_projection(rebuilt) == projection
        record_count += len(projection[3])
        full_prefix_cells += sum(len(state.terms) for state in trace.states)
        compact_value_cells += len(trace.initial.terms) + len(projection[3])
        if projection[4] is not None:
            # A terminal failure is a first-class witness and retains exactly
            # one complete final prefix.  Count that snapshot explicitly; the
            # compact form still omits every intermediate transition snapshot.
            compact_value_cells += len(projection[4].old_prefix.terms)
        terminal_replays += projection[4] is not None

    assert record_count == 326
    assert terminal_replays == 1
    assert full_prefix_cells > 10 * compact_value_cells

    mutations = 0
    baseline_program, baseline_trace = full_traces[0]
    baseline = compact_trace_projection(baseline_trace)
    first_value, first_access = baseline[3][0]
    wrong_value_records = ((first_value + 1, first_access), *baseline[3][1:])
    wrong_value = (baseline[0], baseline[1], baseline[2], wrong_value_records, baseline[4])
    mutations += must_raise(ValueError, lambda: replay_compact_trace(baseline_program, wrong_value))

    other_access = compact_trace_projection(full_traces[1][1])[3][0][1]
    wrong_access_records = ((first_value, other_access), *baseline[3][1:])
    wrong_access = (baseline[0], baseline[1], baseline[2], wrong_access_records, baseline[4])
    mutations += must_raise(ValueError, lambda: replay_compact_trace(baseline_program, wrong_access))

    truncated = (baseline[0], baseline[1], baseline[2], baseline[3][:-1], None)
    mutations += must_raise(ValueError, lambda: replay_compact_trace(baseline_program, truncated))
    partial_projection = compact_trace_projection(partial)
    missing_terminal = (
        partial_projection[0],
        partial_projection[1],
        partial_projection[2],
        partial_projection[3],
        None,
    )
    mutations += must_raise(ValueError, lambda: replay_compact_trace(partial_program, missing_terminal))
    assert mutations == 4

    return len(full_traces), record_count, full_prefix_cells, compact_value_cells, terminal_replays, mutations


FORBIDDEN_EXECUTION_ROLE_SUFFIXES = (
    "State",
    "Frontier",
    "Neighborhood",
    "Update",
    "Executor",
)


SHARED_EXECUTION_ROLE_MANIFEST = (
    ("configuration", "NumericPrefix", "D070/T37 complete consecutive indexed prefix"),
    ("alphabet", "positive exact int", "shared arbitrary-precision numeric carrier"),
    ("frontier", "select_unique_end", "T37 unique trailing End role"),
    ("neighborhood", "read_complete_prefix", "T37 complete explicit old-prefix context"),
    ("rule", "evaluate_recurrence_rule", "closed TermAt AST plus End-to-Val-End write"),
    ("update", "apply_endpoint_splice", "D072/T16 exactly-one ordered splice"),
    ("result", "StepResult", "common Advanced/Error envelope"),
    ("trace", "RunTrace", "D073 complete prefix/event reconstruction"),
)


EXPECTED_DATACLASS_ROLE_MANIFEST = (
    "AccessFailure",
    "Add",
    "Advanced",
    "AppendEvent",
    "End",
    "EndpointReplacement",
    "ErrorOutcome",
    "Literal",
    "Mul",
    "NumericPrefix",
    "ProgramProvenance",
    "ReadDemand",
    "RecurrenceProgram",
    "ResolvedAccess",
    "ResultOutsideCarrier",
    "RuleFailure",
    "RunTrace",
    "SourcePreset",
    "StepResult",
    "Sub",
    "TargetIndex",
    "TermAt",
    "TermHandle",
    "UndefinedTermReference",
    "Val",
)


def dataclass_role_manifest(namespace: object) -> tuple[str, ...]:
    if type(namespace) is not dict:
        raise TypeError("namespace must be exact dict")
    return tuple(
        sorted(
            name
            for name, value in namespace.items()
            if type(name) is str and isinstance(value, type) and is_dataclass(value)
        )
    )


def forbidden_execution_role_symbols(namespace: object) -> tuple[tuple[str, tuple[str, ...]], ...]:
    if type(namespace) is not dict:
        raise TypeError("namespace must be exact dict")
    rows = []
    for suffix in FORBIDDEN_EXECUTION_ROLE_SUFFIXES:
        names = tuple(
            sorted(
                name
                for name, value in namespace.items()
                if type(name) is str
                and isinstance(value, type)
                and name.endswith(suffix)
                and name not in {"StepResult"}
            )
        )
        rows.append((suffix, names))
    return tuple(rows)


def audit_no_new_execution_surface() -> tuple[int, int, int, int, int, int, int, int]:
    manifest = dataclass_role_manifest(dict(globals()))
    assert manifest == EXPECTED_DATACLASS_ROLE_MANIFEST
    forbidden = dict(forbidden_execution_role_symbols(dict(globals())))
    assert forbidden == {
        "State": (),
        "Frontier": (),
        "Neighborhood": (),
        "Update": (),
        "Executor": (),
    }
    assert len([name for name in manifest if name == "NumericPrefix"]) == 1
    assert len([name for name in manifest if name == "StepResult"]) == 1
    assert len([name for name in manifest if name == "RecurrenceProgram"]) == 1
    assert SHARED_EXECUTION_ROLE_MANIFEST[2][1] == "select_unique_end"
    assert SHARED_EXECUTION_ROLE_MANIFEST[3][1] == "read_complete_prefix"
    assert SHARED_EXECUTION_ROLE_MANIFEST[4][1] == "evaluate_recurrence_rule"
    assert SHARED_EXECUTION_ROLE_MANIFEST[5][1] == "apply_endpoint_splice"
    return 1, 0, 0, 0, 0, 1, 1, len(manifest)


def audit_hostile_validation() -> int:
    rejected = 0

    rejected += must_raise(TypeError, lambda: Literal(True))
    rejected += must_raise(TypeError, lambda: Literal(1.0))
    rejected += must_raise(ValueError, lambda: Add(()))
    rejected += must_raise(TypeError, lambda: Add([C(1), C(2)]))
    rejected += must_raise(ValueError, lambda: Mul((C(1),)))
    rejected += must_raise(TypeError, lambda: TermAt(lambda: 1))
    rejected += must_raise(TypeError, lambda: RecurrenceProgram("f[n-1]"))
    rejected += must_raise(TypeError, lambda: RecurrenceProgram(lambda value: value))
    rejected += must_raise(ValueError, lambda: RecurrenceProgram(lag(1), demand_order="lazy"))
    rejected += must_raise(ValueError, lambda: RecurrenceProgram(lag(1), carrier="finite_int64"))

    rejected += must_raise(TypeError, lambda: NumericPrefix(True, (1,)))
    rejected += must_raise(ValueError, lambda: NumericPrefix(0, (1,)))
    rejected += must_raise(TypeError, lambda: NumericPrefix(1, [1]))
    rejected += must_raise(ValueError, lambda: NumericPrefix(1, ()))
    rejected += must_raise(ValueError, lambda: NumericPrefix(1, (0,)))
    rejected += must_raise(TypeError, lambda: NumericPrefix(1, (False,)))

    valid_prefix = NumericPrefix(1, (1, 2, 3))
    valid_word = encode_prefix(valid_prefix)
    rejected += must_raise(ValueError, lambda: checked_word((Val(1, 1),)))
    rejected += must_raise(ValueError, lambda: checked_word((Val(1, 1), End(2), End(2))))
    rejected += must_raise(ValueError, lambda: checked_word((Val(2, 1), End(3))))
    rejected += must_raise(ValueError, lambda: checked_word((Val(1, 1), End(3))))
    rejected += must_raise(ValueError, lambda: checked_word((End(1), Val(1, 1))))
    rejected += must_raise(ValueError, lambda: apply_endpoint_splice(valid_word, 0, EndpointReplacement(
        End(4), (Val(4, 4), End(5)), program_provenance(RecurrenceProgram(lag(1))),
        resolve_rule_expression(RecurrenceProgram(lag(1)), valid_prefix, End(4)),
    )))

    program = dict(source_programs())["e"]

    class _AxisProbe(Exception):
        pass

    original_read = read_complete_prefix

    def read_probe(prefix: object, active: object) -> NumericPrefix:
        raise _AxisProbe("complete-prefix NEIGHBORHOOD was invoked")

    globals()["read_complete_prefix"] = read_probe
    try:
        rejected += must_raise(
            _AxisProbe,
            lambda: generic_step(program, NumericPrefix(1, (1, 1))),
        )
    finally:
        globals()["read_complete_prefix"] = original_read

    original_rule = evaluate_recurrence_rule

    def rule_probe(program_value: object, active: object, reads: object) -> RuleAttempt:
        raise _AxisProbe("merged closed RULE was invoked")

    globals()["evaluate_recurrence_rule"] = rule_probe
    try:
        rejected += must_raise(
            _AxisProbe,
            lambda: generic_step(program, NumericPrefix(1, (1, 1))),
        )
    finally:
        globals()["evaluate_recurrence_rule"] = original_rule

    event = generic_step(program, NumericPrefix(1, (1, 1))).event
    assert verify_append_event(program, event)
    rejected += must_raise(
        ValueError,
        lambda: RuleFailure(
            event.provenance,
            event.active,
            event.before,
            event.access,
            ResultOutsideCarrier(event.active.next_index, 0),
        ),
    )
    bad_after = NumericPrefix(1, event.after.terms[:-1] + (99,))
    rejected += must_raise(ValueError, lambda: replace(event, after=bad_after))
    forged_after = object.__new__(AppendEvent)
    for field in fields(AppendEvent):
        object.__setattr__(forged_after, field.name, bad_after if field.name == "after" else getattr(event, field.name))
    assert not verify_append_event(program, forged_after)
    rejected += 1
    forged_access = replace(
        event.access,
        resolved_expression=Literal(evaluate_resolved(event.access.resolved_expression) + 1),
    )
    forged_write = EndpointReplacement(
        event.active,
        (Val(event.active.next_index, evaluate_resolved(forged_access.resolved_expression)), End(event.active.next_index + 1)),
        event.provenance,
        forged_access,
    )
    forged_word = apply_endpoint_splice(event.before_word, event.active_position, forged_write)
    forged_event = AppendEvent(
        event.provenance,
        event.before,
        event.before_word,
        event.active_position,
        event.active,
        forged_access,
        forged_write,
        forged_word,
        decode_prefix(forged_word),
    )
    assert not verify_append_event(program, forged_event)
    rejected += 1

    first_demand = event.access.demands[0]
    forged_demands = (replace(first_demand, path=(99,)),) + event.access.demands[1:]
    forged_access_path = ResolvedAccess(
        event.access.provenance,
        event.access.target_index,
        event.access.resolved_expression,
        forged_demands,
    )
    assert forged_access_path != event.access
    rejected += 1

    other = dict(source_programs())["d"]
    assert not verify_append_event(other, event)
    rejected += 1
    rejected += must_raise(
        ValueError,
        lambda: ProgramProvenance(event.provenance.structural_key, "0" * 64),
    )
    rejected += must_raise(TypeError, lambda: checked_program_key([*event.provenance.structural_key]))
    rejected += must_raise(ValueError, lambda: checked_program_key(("Callback/v1", VALUE_CARRIER, DEMAND_ORDER, ("x",))))
    forged_nested_key = (
        "ComputedPrefixRecurrence/v1",
        VALUE_CARRIER,
        DEMAND_ORDER,
        ("TermAt/v1", ("Callback/v1",)),
    )
    forged_nested_id = sha256(repr(forged_nested_key).encode("utf-8")).hexdigest()
    rejected += must_raise(ValueError, lambda: checked_program_key(forged_nested_key))
    rejected += must_raise(ValueError, lambda: ProgramProvenance(forged_nested_key, forged_nested_id))
    rejected += must_raise(ValueError, lambda: checked_expression_key(("Literal/v1", "01")))
    rejected += must_raise(ValueError, lambda: checked_expression_key(("Add/v1", (("Literal/v1", "1"),))))

    trace = run(program, NumericPrefix(1, (1, 1)), 4)
    unsafe = object.__new__(RunTrace)
    object.__setattr__(unsafe, "provenance", trace.provenance)
    object.__setattr__(unsafe, "initial", trace.initial)
    object.__setattr__(unsafe, "requested_events", trace.requested_events)
    object.__setattr__(unsafe, "states", (trace.states[0], trace.states[2], *trace.states[2:]))
    object.__setattr__(unsafe, "events", trace.events)
    object.__setattr__(unsafe, "outcome", trace.outcome)
    object.__setattr__(unsafe, "terminal_attempt", None)
    assert not verify_trace(program, unsafe)
    rejected += 1
    rejected += must_raise(
        ValueError,
        lambda: RunTrace(
            trace.provenance,
            trace.initial,
            4,
            (trace.states[0], trace.states[2], *trace.states[2:]),
            trace.events,
            trace.outcome,
            None,
        ),
    )

    # A terminal attempt is bound to the exact final configuration, not merely
    # to an equal program/error reason.  This pair deliberately has the same
    # ResultOutsideCarrier witness while retaining different old prefixes.
    binding_program = RecurrenceProgram(Sub(lag(1), lag(1)))
    binding_left = run(binding_program, NumericPrefix(1, (1,)), 1)
    binding_right = run(binding_program, NumericPrefix(1, (2,)), 1)
    assert type(binding_left.outcome) is ErrorOutcome
    assert type(binding_right.outcome) is ErrorOutcome
    assert type(binding_left.terminal_attempt) is RuleFailure
    assert type(binding_right.terminal_attempt) is RuleFailure
    assert binding_left.outcome == binding_right.outcome
    assert binding_left.terminal_attempt.old_prefix != binding_right.terminal_attempt.old_prefix
    rejected += must_raise(
        ValueError,
        lambda: RunTrace(
            binding_left.provenance,
            binding_left.initial,
            binding_left.requested_events,
            binding_left.states,
            binding_left.events,
            binding_left.outcome,
            binding_right.terminal_attempt,
        ),
    )

    # Explicit semantic mutation sentinels.
    invalid = generic_step(RecurrenceProgram(at(C(-1))), NumericPrefix(1, (7, 11)))
    assert type(invalid.outcome) is ErrorOutcome
    assert invalid.successors == ()
    assert (7, 11)[-1] == 11  # Python negative indexing would invent a value.
    rejected += 1
    current = generic_step(RecurrenceProgram(at(N())), NumericPrefix(1, (7, 11)))
    assert type(current.outcome) is ErrorOutcome
    rejected += 1
    cancellation = generic_step(
        RecurrenceProgram(Sub(at(C(-1)), at(C(-1)))),
        NumericPrefix(1, (7, 11)),
    )
    assert type(cancellation.outcome) is ErrorOutcome
    rejected += 1

    mutated_namespace = dict(globals())
    mutated_namespace["VariableRecurrenceExecutor"] = type("VariableRecurrenceExecutor", (), {})
    mutated_roles = dict(forbidden_execution_role_symbols(mutated_namespace))
    assert mutated_roles["Executor"] == ("VariableRecurrenceExecutor",)
    rejected += 1

    mutated_namespace = dict(globals())
    mutated_namespace["VariableRecurrenceState"] = dataclass(frozen=True)(
        type("VariableRecurrenceState", (), {"__annotations__": {"value": int}})
    )
    assert "VariableRecurrenceState" in dataclass_role_manifest(mutated_namespace)
    assert dict(forbidden_execution_role_symbols(mutated_namespace))["State"] == ("VariableRecurrenceState",)
    rejected += 1

    assert RAW_12738_SPELLING != "Flatten[Table[Table[n, {IntegerExponent[n, 2] + 1}], {n, m}]]"
    assert raw_12738_multiplicity_list(4) == (1, 2, 2, 3, 4, 4, 4)
    assert repaired_12738_case_d_list(4) == (1, 1, 2, 2, 3, 4, 4, 4)
    rejected += 1

    return rejected


EXPECTED_DIGEST = "3f56c8a84f473b5a7551f7a5cb91489cf96537426bb07536fa4d869e083f2f65"


def collect_audit_summary() -> tuple[tuple[str, object], ...]:
    factorization = audit_complete_prefix_rule_factorization()
    visible = audit_visible_source_rows()
    long_traces = audit_long_source_traces()
    partiality = audit_dependent_access_and_partiality()
    lossiness = audit_lossiness_and_fixed_lag_boundary()
    observers = audit_page131_observers()
    bigint = audit_arbitrary_precision()
    identity = audit_structural_identity_and_replay()
    trace_shape = audit_trace_shape_and_error_retention()
    compact_trace = audit_compact_trace_reconstruction()
    surface = audit_no_new_execution_surface()
    hostile = audit_hostile_validation()
    return (
        ("complete_prefix_rule_factorization", factorization),
        ("visible_source_rows", visible),
        ("long_source_traces", long_traces),
        ("dependent_access_partiality", partiality),
        ("lossiness_fixed_lag", lossiness),
        ("page131_observers", observers),
        ("arbitrary_precision", bigint),
        ("structural_identity_replay", identity),
        ("trace_shape_error_retention", trace_shape),
        ("compact_trace_reconstruction", compact_trace),
        ("execution_surface", surface),
        ("hostile_rejections", hostile),
        ("source_formulas", SOURCE_FORMULAS),
        ("visible_source_terms", VISIBLE_SOURCE_TERMS),
        ("visible_horizons", VISIBLE_HORIZONS),
        ("source_claims", SOURCE_CLAIMS),
        ("architecture_classes", ARCHITECTURE_CLASSIFICATION),
        ("goal2_delta", GOAL2_DELTA),
        ("raw_12738_spelling", RAW_12738_SPELLING),
        ("guarded_12738_repair", GUARDED_12738_REPAIR),
        ("shared_execution_roles", SHARED_EXECUTION_ROLE_MANIFEST),
        ("dataclass_role_manifest", EXPECTED_DATACLASS_ROLE_MANIFEST),
        ("forbidden_execution_suffixes", FORBIDDEN_EXECUTION_ROLE_SUFFIXES),
    )


def main() -> None:
    summary = collect_audit_summary()
    digest = sha256(repr(summary).encode("utf-8")).hexdigest()
    if EXPECTED_DIGEST == "TO_BE_COMPUTED":
        print(f"computed_semantic_digest={digest}")
        return
    assert digest == EXPECTED_DIGEST
    metrics = dict(summary)
    factorization = metrics["complete_prefix_rule_factorization"]
    visible = metrics["visible_source_rows"]
    long_traces = metrics["long_source_traces"]
    partiality = metrics["dependent_access_partiality"]
    lossiness = metrics["lossiness_fixed_lag"]
    observers = metrics["page131_observers"]
    bigint = metrics["arbitrary_precision"]
    identity = metrics["structural_identity_replay"]
    trace_shape = metrics["trace_shape_error_retention"]
    compact_trace = metrics["compact_trace_reconstruction"]
    surface = metrics["execution_surface"]

    print(
        f"merged_compiled_visible={factorization[0]}; "
        f"merged_compiled_long={factorization[1]}; "
        f"merged_compiled_partial={factorization[2]}; "
        f"merged_compiled_fixed_lag={factorization[3]}; "
        f"merged_compiled_bigint={factorization[4]}; "
        f"merged_compiled_failures={factorization[5]}; "
        f"merged_compiled_total={factorization[6]}"
    )
    print(
        f"visible_events={visible[0]}; visible_demands={visible[1]}; "
        f"event_replays={visible[2]}; codec_commutations={visible[3]}; nested_demands={visible[4]}"
    )
    print(
        f"long_events={long_traces[0]}; long_demands={long_traces[1]}; "
        f"minimum_address={long_traces[2]}; maximum_dynamic_lag={long_traces[3]}; "
        f"maximum_source_value={long_traces[4]}; long_trace_replays={long_traces[5]}"
    )
    print(
        f"partial_cases={partiality[0]}; partial_errors={partiality[1]}; "
        f"successful_demands={partiality[2]}; repeated_occurrences={partiality[3]}; "
        f"old_snapshot_guards={partiality[4]}; order_guards={partiality[5]}"
    )
    print(
        f"fixed_lag_commutations={lossiness[0]}; window_counterexamples={lossiness[1]}; "
        f"maximum_window={lossiness[2]}; newest_scalar_counterexamples={lossiness[3]}; "
        f"distinct_dynamic_lags={lossiness[4]}"
    )
    print(
        f"page131_formula_checks={observers[0]}; last_index_checks={observers[1]}; "
        f"raw_multiplicity_terms={observers[2]}; repaired_terms={observers[3]}; "
        f"observer_max_value={observers[4]}; defect_guards={observers[5]}"
    )
    print(
        f"bigint_events={bigint[0]}; max_bits={bigint[1]}; max_decimal_digits={bigint[2]}; "
        f"bigint_replays={bigint[3]}"
    )
    print(
        f"structural_keys={identity[0]}; structural_ids={identity[1]}; "
        f"cross_rejections={identity[2]}; serialization_roundtrips={identity[3]}; "
        f"order_guards={identity[4]}; identity_trace_events={identity[5]}"
    )
    print(
        f"trace_horizons={trace_shape[0]}; trace_events={trace_shape[1]}; "
        f"trace_states={trace_shape[2]}; trace_replays={trace_shape[3]}; "
        f"no_partial_events={trace_shape[4]}; retained_last_states={trace_shape[5]}"
    )
    print(
        f"compact_traces={compact_trace[0]}; compact_records={compact_trace[1]}; "
        f"full_prefix_cells={compact_trace[2]}; compact_value_cells={compact_trace[3]}; "
        f"compact_terminal_replays={compact_trace[4]}; compact_mutation_rejections={compact_trace[5]}"
    )
    print(
        f"surface=configuration{surface[0]}/state{surface[1]}/frontier{surface[2]}/"
        f"neighborhood{surface[3]}/update{surface[4]}/StepResult{surface[5]}/"
        f"program{surface[6]}/dataclasses{surface[7]}; "
        f"hostile_rejections={metrics['hostile_rejections']}"
    )
    print(f"semantic_digest={digest}")


if __name__ == "__main__":
    if len(sys.argv) != 1:
        raise SystemExit("usage: 44-T38-semantic-oracle.py")
    main()
