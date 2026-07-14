#!/usr/bin/env python3
"""Dependency-free semantic oracle for T35 piecewise integer maps.

T35 does not need a new scalar state, FRONTIER, NEIGHBORHOOD, assignment,
UPDATE, executor, or history-bearing configuration.  Its strict construction
is a closed, complete table indexed by the Euclidean residue of the current
exact integer.  The selected row computes one exact integer and the ordinary
T34 singleton assignment commits it::

    active = UniqueScalar.select(state)
    old    = Self.read(state, active)
    row    = program.rows[EuclideanMod(old, modulus)]
    write  = ScalarAssignment(active, row(old))
    next   = AtomicAssignment.apply(state, write)

The main parity examples are modulus-two presets of that generic construction.
Rows of a complete residue table do not overlap and therefore have no rule
precedence.  Branch selection is nevertheless retained as replayable event
evidence.

Conway's ordered fraction systems (now commonly called FRACTRAN) are modeled
separately as a tagged partial sibling.  They choose the *first* fraction whose
product is integral, so source order and the first-applicable witness are
semantic.  Their divisibility predicates are periodic modulo the least common
multiple of denominators, but the source program's modulus has 6,469,693,230
residues.  The exact residue view below is consequently lazy and never
materializes that table.

This is proof code, not a proposed runtime API.  It uses only the Python
standard library, is silent on import, and fails closed under ``python -O``.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from hashlib import sha256
from itertools import permutations
from math import gcd, lcm
from typing import TypeAlias


if not __debug__:
    raise RuntimeError("T35 semantic oracle must run with assertions enabled")


SIGNED = "signed_integer"
NONNEGATIVE = "nonnegative_integer"
POSITIVE = "positive_integer"
INTEGER_CARRIERS = (SIGNED, NONNEGATIVE, POSITIVE)
SCALAR_LOCUS = "unique_scalar"
DOMAIN = "discrete_t_plus_0D"


SOURCE_CLAIMS = (
    ("BOOK:1497-1503", "parity chooses between two exact integer formulas"),
    ("BOOK:1505-1511", "the page-122 seed-one prefix begins 1,3,6,9,15"),
    ("BOOK:1513-1529", "the 5-over-2 variant has fixed and repetitive seeds"),
    ("BOOK:1531-1541", "digit pictures and size plots expose behavior but are not state"),
    ("BOOK:1198", "a related register-machine projection obeys a scalar parity map"),
    ("BOOK:12598", "NestList includes the initial seed and then t applications"),
    ("BOOK:12599-12608", "standard 3n+1 positive and signed cycles are analysis claims"),
    ("BOOK:12625-12631", "many-to-one behavior means current value does not retain history"),
    ("BOOK:8102-8120", "complete remainder-indexed arithmetic systems emulate register machines"),
    ("BOOK:18636-18648", "arithmetic emulation uses a complete Mod-indexed rule table"),
    ("BOOK:18648-18658", "Conway fraction systems select the first integral product"),
    ("BOOK:19102", "a continuous cosine map agrees with parity map A only on integer inputs"),
)


ARCHITECTURE_CLASSIFICATION = (
    "1: reuse T34 discrete t+0D singleton state, self read, scalar assignment, atomic UPDATE, trace, and outcomes",
    "2: parameterize T34's closed unary rule by a complete finite Euclidean-residue table and carrier invariant",
    "3: name parity presets and retain lossless branch witnesses; ordered fractions are a tagged partial rule sibling",
    "4: no new execution algebra; first-applicable and no-applicable belong to closed RULE/result data",
)


GOAL2_DELTA = (
    "Reuse T34's carrier-tagged exact integer singleton configuration and generic same-locus assignment unchanged.",
    "Add closed AffineQuotient and CompleteResidueIntegerMap rule nodes; never accept a callback or implicit default.",
    "Index complete tables by Euclidean Mod in 0..m-1, with exactly one row per residue and no precedence semantics.",
    "Validate integrality and carrier closure analytically for the whole residue class, not by sampled execution.",
    "Keep strict positive, principled nonnegative, and signed-extension carriers explicit; never silently admit zero.",
    "Retain selected residue/formula/result as replayable event evidence without putting branch or history in state.",
    "Treat cycles and fixed points as ordinary Advanced events; h total events always yield h+1 snapshots.",
    "Represent ordered positive-fraction programs as a tagged partial rule with first-applicable/no-applicable results.",
    "If exposing a residue relation for fractions, keep source order/index witnesses and use a lazy LCM view.",
    "A bare fraction decision table is behavior-preserving but not injective; retain the ordered source AST and provenance.",
    "Separate exact integer closure from positive/reachable invariants in general remainder tables such as register encodings.",
    "Keep digit/size/parity views, stopping-time/cycle/growth analysis, CA/register encodings, and real maps outside execution.",
    "Add no T35 state class, control, frontier, neighborhood, assignment, update law, executor, family branch, or hidden history.",
)


MAIN_A_PREFIX = (
    1,
    3,
    6,
    9,
    15,
    24,
    36,
    54,
    81,
    123,
    186,
    279,
    420,
    630,
    945,
    1419,
    2130,
    3195,
    4794,
)

MAIN_B_SEED6_PREFIX = (
    6,
    15,
    8,
    20,
    50,
    125,
    63,
    32,
    80,
    200,
    500,
    1250,
    3125,
    1563,
    782,
    1955,
    978,
    2445,
    1223,
    612,
    1530,
)

STANDARD_POSITIVE_CYCLE = (1, 2)
STANDARD_SIGNED_CYCLES = (
    (-1,),
    (-5, -7, -10),
    (-17, -25, -37, -55, -82, -41, -61, -91, -136, -68, -34),
)
MAIN_B_SOURCE_CYCLES = (
    (2, 5, 3),
    (4, 10, 25, 13, 7),
    (40, 100, 250, 625, 313, 157, 79),
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


def checked_carrier(value: object) -> str:
    carrier = exact_str(value, "carrier")
    if carrier not in INTEGER_CARRIERS:
        raise ValueError("unknown integer carrier")
    return carrier


def checked_integer_value(value: object, carrier: object, name: str = "value") -> int:
    integer = exact_int(value, name)
    tag = checked_carrier(carrier)
    if tag == NONNEGATIVE and integer < 0:
        raise ValueError(f"{name} must be nonnegative")
    if tag == POSITIVE and integer <= 0:
        raise ValueError(f"{name} must be positive")
    return integer


def checked_modulus(value: object) -> int:
    modulus = exact_int(value, "modulus")
    if modulus <= 0:
        raise ValueError("modulus must be positive")
    return modulus


def checked_horizon(value: object) -> int:
    horizon = exact_int(value, "horizon")
    if horizon < 0:
        raise ValueError("horizon must be nonnegative")
    return horizon


def euclidean_mod(value: object, modulus: object) -> int:
    """Exact Euclidean remainder, including for negative integers."""

    integer = exact_int(value, "value")
    divisor = checked_modulus(modulus)
    quotient, residue = divmod(integer, divisor)
    if integer != quotient * divisor + residue or not 0 <= residue < divisor:
        raise ArithmeticError("host divmod did not satisfy Euclidean division")
    return residue


@dataclass(frozen=True)
class ScalarConfiguration:
    """The reused carrier-tagged T34 singleton configuration."""

    carrier: str
    value: int

    def __post_init__(self) -> None:
        carrier = checked_carrier(self.carrier)
        value = checked_integer_value(self.value, carrier)
        object.__setattr__(self, "carrier", carrier)
        object.__setattr__(self, "value", value)


@dataclass(frozen=True)
class ScalarAssignment:
    """The reused generic same-locus scalar write."""

    locus: str
    value: int

    def __post_init__(self) -> None:
        locus = exact_str(self.locus, "assignment locus")
        if locus != SCALAR_LOCUS:
            raise ValueError("assignment must target the unique scalar locus")
        object.__setattr__(self, "value", exact_int(self.value, "assignment value"))


def select_unique_scalar(configuration: object) -> tuple[str, ...]:
    if type(configuration) is not ScalarConfiguration:
        raise TypeError("configuration must be exact ScalarConfiguration")
    return (SCALAR_LOCUS,)


def read_self(configuration: object, locus: object) -> int:
    if type(configuration) is not ScalarConfiguration:
        raise TypeError("configuration must be exact ScalarConfiguration")
    if exact_str(locus, "locus") != SCALAR_LOCUS:
        raise ValueError("self read requires the unique scalar locus")
    return configuration.value


def apply_scalar_assignment(
    configuration: object,
    assignment: object,
) -> ScalarConfiguration:
    """The one ordinary atomic UPDATE used by every advanced event here."""

    if type(configuration) is not ScalarConfiguration:
        raise TypeError("configuration must be exact ScalarConfiguration")
    if type(assignment) is not ScalarAssignment:
        raise TypeError("assignment must be exact ScalarAssignment")
    checked_integer_value(assignment.value, configuration.carrier, "result")
    return ScalarConfiguration(configuration.carrier, assignment.value)


@dataclass(frozen=True)
class AffineQuotient:
    """Closed exact formula ``(multiplier*n + offset) / divisor``."""

    multiplier: int
    offset: int
    divisor: int

    def __post_init__(self) -> None:
        multiplier = exact_int(self.multiplier, "multiplier")
        offset = exact_int(self.offset, "offset")
        divisor = exact_int(self.divisor, "divisor")
        if divisor <= 0:
            raise ValueError("formula divisor must be positive")
        object.__setattr__(self, "multiplier", multiplier)
        object.__setattr__(self, "offset", offset)
        object.__setattr__(self, "divisor", divisor)

    def apply(self, value: object) -> int:
        integer = exact_int(value, "formula input")
        numerator = self.multiplier * integer + self.offset
        quotient, remainder = divmod(numerator, self.divisor)
        if remainder != 0:
            raise ValueError("formula output is not an exact integer")
        return quotient


def first_value_in_residue(carrier: str, modulus: int, residue: int) -> int | None:
    if carrier == SIGNED:
        return None
    if carrier == NONNEGATIVE:
        return residue
    return residue if residue > 0 else modulus


def validate_formula_on_residue(
    formula: AffineQuotient,
    carrier: str,
    modulus: int,
    residue: int,
) -> None:
    """Prove exact integrality and carrier closure for an entire residue class."""

    if (formula.multiplier * modulus) % formula.divisor != 0:
        raise ValueError("formula is not integral throughout its residue class")
    if (formula.multiplier * residue + formula.offset) % formula.divisor != 0:
        raise ValueError("formula is not integral on the indexed residue")
    if carrier == SIGNED:
        return
    first = first_value_in_residue(carrier, modulus, residue)
    if first is None:
        raise AssertionError("bounded carrier requires a first residue member")
    first_output = formula.apply(first)
    step_output = formula.multiplier * modulus // formula.divisor
    lower_bound = 0 if carrier == NONNEGATIVE else 1
    if step_output < 0 or first_output < lower_bound:
        raise ValueError("formula is not closed over the declared integer carrier")


@dataclass(frozen=True)
class CompleteResidueIntegerMap:
    """One formula for each disjoint Euclidean residue; no precedence exists."""

    carrier: str
    modulus: int
    formulas: tuple[AffineQuotient, ...]

    def __post_init__(self) -> None:
        carrier = checked_carrier(self.carrier)
        modulus = checked_modulus(self.modulus)
        raw = exact_tuple(self.formulas, "formulas")
        if len(raw) != modulus:
            raise ValueError("complete residue table needs exactly modulus rows")
        formulas: list[AffineQuotient] = []
        for residue, formula in enumerate(raw):
            if type(formula) is not AffineQuotient:
                raise TypeError("each residue formula must be exact AffineQuotient")
            validate_formula_on_residue(formula, carrier, modulus, residue)
            formulas.append(formula)
        object.__setattr__(self, "carrier", carrier)
        object.__setattr__(self, "modulus", modulus)
        object.__setattr__(self, "formulas", tuple(formulas))

    def formula_for(self, value: object) -> tuple[int, AffineQuotient]:
        integer = checked_integer_value(value, self.carrier, "rule input")
        residue = euclidean_mod(integer, self.modulus)
        return residue, self.formulas[residue]


def complete_residue_map_from_rows(
    carrier: object,
    modulus: object,
    rows: object,
) -> CompleteResidueIntegerMap:
    """Canonicalize keyed rows without giving their input order precedence."""

    tag = checked_carrier(carrier)
    divisor = checked_modulus(modulus)
    raw = exact_tuple(rows, "residue rows")
    if len(raw) != divisor:
        raise ValueError("complete residue rows need exactly modulus entries")
    by_residue: dict[int, AffineQuotient] = {}
    for row in raw:
        pair = exact_tuple(row, "residue row")
        if len(pair) != 2:
            raise ValueError("residue row must contain residue and formula")
        residue = exact_int(pair[0], "row residue")
        if not 0 <= residue < divisor:
            raise ValueError("row residue is outside the canonical range")
        formula = pair[1]
        if type(formula) is not AffineQuotient:
            raise TypeError("row formula must be exact AffineQuotient")
        if residue in by_residue:
            raise ValueError("duplicate residue row")
        by_residue[residue] = formula
    if tuple(sorted(by_residue)) != tuple(range(divisor)):
        raise ValueError("residue table is incomplete")
    return CompleteResidueIntegerMap(
        tag,
        divisor,
        tuple(by_residue[residue] for residue in range(divisor)),
    )


@dataclass(frozen=True)
class ResidueBranchWitness:
    modulus: int
    residue: int
    formula: AffineQuotient
    old_value: int
    new_value: int

    def __post_init__(self) -> None:
        modulus = checked_modulus(self.modulus)
        residue = exact_int(self.residue, "witness residue")
        if not 0 <= residue < modulus:
            raise ValueError("witness residue is outside the canonical range")
        if type(self.formula) is not AffineQuotient:
            raise TypeError("witness formula must be exact AffineQuotient")
        object.__setattr__(self, "old_value", exact_int(self.old_value, "old value"))
        object.__setattr__(self, "new_value", exact_int(self.new_value, "new value"))


@dataclass(frozen=True)
class PositiveFraction:
    """Canonical positive rational used by ordered fraction programs."""

    numerator: int
    denominator: int

    def __post_init__(self) -> None:
        numerator = exact_int(self.numerator, "fraction numerator")
        denominator = exact_int(self.denominator, "fraction denominator")
        if numerator <= 0 or denominator <= 0:
            raise ValueError("ordered fractions must be positive")
        common = gcd(numerator, denominator)
        object.__setattr__(self, "numerator", numerator // common)
        object.__setattr__(self, "denominator", denominator // common)

    def integral_product(self, value: object) -> int | None:
        integer = checked_integer_value(value, POSITIVE, "fraction input")
        numerator = integer * self.numerator
        quotient, remainder = divmod(numerator, self.denominator)
        return quotient if remainder == 0 else None

    def as_formula(self) -> AffineQuotient:
        return AffineQuotient(self.numerator, 0, self.denominator)


@dataclass(frozen=True)
class OrderedFractionProgram:
    """Ordered first-applicable positive-fraction RULE sibling."""

    fractions: tuple[PositiveFraction, ...]

    def __post_init__(self) -> None:
        raw = exact_tuple(self.fractions, "fractions")
        if not raw:
            raise ValueError("ordered fraction program must be nonempty")
        checked: list[PositiveFraction] = []
        for fraction in raw:
            if type(fraction) is not PositiveFraction:
                raise TypeError("each fraction must be exact PositiveFraction")
            checked.append(fraction)
        # Order and duplicates are deliberately retained.
        object.__setattr__(self, "fractions", tuple(checked))


@dataclass(frozen=True)
class FractionBranchWitness:
    selected_index: int
    selected_fraction: PositiveFraction
    tested_integral: tuple[bool, ...]
    old_value: int
    new_value: int

    def __post_init__(self) -> None:
        selected_index = exact_int(self.selected_index, "selected index")
        if selected_index < 0:
            raise ValueError("selected index must be nonnegative")
        if type(self.selected_fraction) is not PositiveFraction:
            raise TypeError("selected fraction must be exact PositiveFraction")
        raw = exact_tuple(self.tested_integral, "tested-integral flags")
        flags: list[bool] = []
        for flag in raw:
            if type(flag) is not bool:
                raise TypeError("tested-integral flags must be exact bools")
            flags.append(flag)
        if len(flags) != selected_index + 1:
            raise ValueError("fraction witness must retain the tested prefix")
        if not flags or flags[-1] is not True or any(flags[:-1]):
            raise ValueError("fraction witness must identify the first applicable row")
        object.__setattr__(self, "tested_integral", tuple(flags))
        object.__setattr__(self, "old_value", checked_integer_value(self.old_value, POSITIVE, "old value"))
        object.__setattr__(self, "new_value", checked_integer_value(self.new_value, POSITIVE, "new value"))


@dataclass(frozen=True)
class NoApplicableFraction:
    """Typed zero-successor result; the retained scalar is not advanced."""

    retained: ScalarConfiguration
    tested_integral: tuple[bool, ...]

    def __post_init__(self) -> None:
        if type(self.retained) is not ScalarConfiguration:
            raise TypeError("retained state must be exact ScalarConfiguration")
        if self.retained.carrier != POSITIVE:
            raise ValueError("fraction systems retain a positive-integer state")
        raw = exact_tuple(self.tested_integral, "tested-integral flags")
        for flag in raw:
            if type(flag) is not bool:
                raise TypeError("tested-integral flags must be exact bools")
            if flag:
                raise ValueError("NoApplicableFraction cannot contain an applicable row")
        object.__setattr__(self, "tested_integral", tuple(raw))


BranchWitness: TypeAlias = ResidueBranchWitness | FractionBranchWitness
RuleProgram: TypeAlias = CompleteResidueIntegerMap | OrderedFractionProgram


@dataclass(frozen=True)
class ProposedScalarWrite:
    assignment: ScalarAssignment
    witness: BranchWitness

    def __post_init__(self) -> None:
        if type(self.assignment) is not ScalarAssignment:
            raise TypeError("proposed write needs exact ScalarAssignment")
        if type(self.witness) not in (ResidueBranchWitness, FractionBranchWitness):
            raise TypeError("proposed write needs an exact branch witness")


def evaluate_closed_rule(
    program: object,
    configuration: ScalarConfiguration,
    old_value: int,
) -> ProposedScalarWrite | NoApplicableFraction:
    """Evaluate the closed RULE sum; UPDATE remains completely generic."""

    if type(program) is CompleteResidueIntegerMap:
        if configuration.carrier != program.carrier:
            raise ValueError("program and configuration carriers differ")
        residue, formula = program.formula_for(old_value)
        new_value = formula.apply(old_value)
        witness = ResidueBranchWitness(
            program.modulus,
            residue,
            formula,
            old_value,
            new_value,
        )
        return ProposedScalarWrite(
            ScalarAssignment(SCALAR_LOCUS, new_value),
            witness,
        )
    if type(program) is OrderedFractionProgram:
        if configuration.carrier != POSITIVE:
            raise ValueError("ordered fraction programs require positive integers")
        flags: list[bool] = []
        for index, fraction in enumerate(program.fractions):
            result = fraction.integral_product(old_value)
            flags.append(result is not None)
            if result is not None:
                witness = FractionBranchWitness(
                    index,
                    fraction,
                    tuple(flags),
                    old_value,
                    result,
                )
                return ProposedScalarWrite(
                    ScalarAssignment(SCALAR_LOCUS, result),
                    witness,
                )
        return NoApplicableFraction(configuration, tuple(flags))
    raise TypeError("program must be a closed T35 rule node")


@dataclass(frozen=True)
class TransitionEvent:
    before: ScalarConfiguration
    read_value: int
    assignment: ScalarAssignment
    after: ScalarConfiguration
    witness: BranchWitness
    outcome: str = "Advanced"

    def __post_init__(self) -> None:
        if type(self.before) is not ScalarConfiguration or type(self.after) is not ScalarConfiguration:
            raise TypeError("event endpoints must be exact ScalarConfiguration")
        read_value = exact_int(self.read_value, "read value")
        if read_value != self.before.value:
            raise ValueError("event read must be the complete old scalar")
        if type(self.assignment) is not ScalarAssignment:
            raise TypeError("event assignment must be exact ScalarAssignment")
        if type(self.witness) not in (ResidueBranchWitness, FractionBranchWitness):
            raise TypeError("event witness has an unknown type")
        if exact_str(self.outcome, "outcome") != "Advanced":
            raise ValueError("committed transition outcome must be Advanced")


@dataclass(frozen=True)
class Advanced:
    configuration: ScalarConfiguration
    event: TransitionEvent


@dataclass(frozen=True)
class Terminal:
    configuration: ScalarConfiguration
    outcome: NoApplicableFraction


StepResult: TypeAlias = Advanced | Terminal


def advance(program: object, configuration: object) -> StepResult:
    """One branch-free singleton executor over the closed RULE result sum."""

    if type(configuration) is not ScalarConfiguration:
        raise TypeError("configuration must be exact ScalarConfiguration")
    active = select_unique_scalar(configuration)
    if active != (SCALAR_LOCUS,):
        raise AssertionError("UniqueScalar must select exactly one locus")
    old_value = read_self(configuration, active[0])
    proposal = evaluate_closed_rule(program, configuration, old_value)
    if type(proposal) is NoApplicableFraction:
        return Terminal(configuration, proposal)
    if type(proposal) is not ProposedScalarWrite:
        raise TypeError("closed RULE returned an unknown result")
    next_configuration = apply_scalar_assignment(configuration, proposal.assignment)
    event = TransitionEvent(
        configuration,
        old_value,
        proposal.assignment,
        next_configuration,
        proposal.witness,
    )
    return Advanced(next_configuration, event)


@dataclass(frozen=True)
class ScalarTrace:
    requested_horizon: int
    states: tuple[ScalarConfiguration, ...]
    events: tuple[TransitionEvent, ...]
    terminal: NoApplicableFraction | None

    def __post_init__(self) -> None:
        horizon = checked_horizon(self.requested_horizon)
        states = exact_tuple(self.states, "trace states")
        events = exact_tuple(self.events, "trace events")
        if not states:
            raise ValueError("trace must include its initial state")
        for state in states:
            if type(state) is not ScalarConfiguration:
                raise TypeError("trace states must be exact ScalarConfiguration")
        for event in events:
            if type(event) is not TransitionEvent:
                raise TypeError("trace events must be exact TransitionEvent")
        if len(states) != len(events) + 1:
            raise ValueError("each committed event must add exactly one snapshot")
        if len(events) > horizon:
            raise ValueError("trace exceeds requested horizon")
        for index, event in enumerate(events):
            if event.before != states[index] or event.after != states[index + 1]:
                raise ValueError("trace event endpoints do not align with snapshots")
        if self.terminal is None:
            if len(events) != horizon:
                raise ValueError("unterminated trace must reach its horizon")
        else:
            if type(self.terminal) is not NoApplicableFraction:
                raise TypeError("terminal must be exact NoApplicableFraction")
            if self.terminal.retained != states[-1]:
                raise ValueError("terminal result must retain the last snapshot")
            if len(events) >= horizon:
                raise ValueError("terminal trace must stop before its horizon")
        object.__setattr__(self, "requested_horizon", horizon)
        object.__setattr__(self, "states", tuple(states))
        object.__setattr__(self, "events", tuple(events))


def run(program: object, seed: object, horizon: object) -> ScalarTrace:
    if type(seed) is not ScalarConfiguration:
        raise TypeError("seed must be exact ScalarConfiguration")
    steps = checked_horizon(horizon)
    states = [seed]
    events: list[TransitionEvent] = []
    terminal: NoApplicableFraction | None = None
    for _ in range(steps):
        result = advance(program, states[-1])
        if type(result) is Terminal:
            terminal = result.outcome
            break
        if type(result) is not Advanced:
            raise TypeError("executor returned an unknown StepResult")
        states.append(result.configuration)
        events.append(result.event)
    return ScalarTrace(steps, tuple(states), tuple(events), terminal)


def verify_residue_witness(
    program: object,
    witness: object,
) -> bool:
    if type(program) is not CompleteResidueIntegerMap:
        return False
    if type(witness) is not ResidueBranchWitness:
        return False
    try:
        residue, formula = program.formula_for(witness.old_value)
        return (
            witness.modulus == program.modulus
            and witness.residue == residue
            and witness.formula == formula
            and witness.new_value == formula.apply(witness.old_value)
        )
    except (TypeError, ValueError):
        return False


def verify_fraction_witness(
    program: object,
    witness: object,
) -> bool:
    if type(program) is not OrderedFractionProgram:
        return False
    if type(witness) is not FractionBranchWitness:
        return False
    if witness.selected_index >= len(program.fractions):
        return False
    flags: list[bool] = []
    result: int | None = None
    for index, fraction in enumerate(program.fractions[: witness.selected_index + 1]):
        candidate = fraction.integral_product(witness.old_value)
        flags.append(candidate is not None)
        if candidate is not None:
            result = candidate
            if index != witness.selected_index:
                return False
            break
    return (
        tuple(flags) == witness.tested_integral
        and program.fractions[witness.selected_index] == witness.selected_fraction
        and result == witness.new_value
    )


def verify_no_applicable(
    program: object,
    outcome: object,
) -> bool:
    if type(program) is not OrderedFractionProgram:
        return False
    if type(outcome) is not NoApplicableFraction:
        return False
    flags = tuple(
        fraction.integral_product(outcome.retained.value) is not None
        for fraction in program.fractions
    )
    return flags == outcome.tested_integral and not any(flags)


def parity_program_a(carrier: str = POSITIVE) -> CompleteResidueIntegerMap:
    return CompleteResidueIntegerMap(
        carrier,
        2,
        (AffineQuotient(3, 0, 2), AffineQuotient(3, 3, 2)),
    )


def parity_program_b(carrier: str = POSITIVE) -> CompleteResidueIntegerMap:
    return CompleteResidueIntegerMap(
        carrier,
        2,
        (AffineQuotient(5, 0, 2), AffineQuotient(1, 1, 2)),
    )


def standard_3n_plus_1(carrier: str = POSITIVE) -> CompleteResidueIntegerMap:
    return CompleteResidueIntegerMap(
        carrier,
        2,
        (AffineQuotient(1, 0, 2), AffineQuotient(3, 1, 2)),
    )


def direct_parity_a(value: object) -> int:
    integer = exact_int(value, "value")
    if euclidean_mod(integer, 2) == 0:
        return 3 * integer // 2
    return 3 * (integer + 1) // 2


def direct_parity_b(value: object) -> int:
    integer = exact_int(value, "value")
    if euclidean_mod(integer, 2) == 0:
        return 5 * integer // 2
    return (integer + 1) // 2


def direct_standard_3n_plus_1(value: object) -> int:
    integer = exact_int(value, "value")
    if euclidean_mod(integer, 2) == 0:
        return integer // 2
    return (3 * integer + 1) // 2


def integer_locus_cosine_relation_a(value: object) -> int:
    """Exact BOOK:19102 relation, using cos(pi*n)=(-1)^n symbolically.

    This is deliberately not a real-valued cosine evaluator or a T35 RULE.
    It checks the integer-locus conjugate expression
    ``(3 + 6*n - 3*cos(pi*n))/4`` without floating-point arithmetic.
    """

    integer = exact_int(value, "integer relation input")
    cosine_at_integer = 1 if euclidean_mod(integer, 2) == 0 else -1
    numerator = 3 + 6 * integer - 3 * cosine_at_integer
    quotient, remainder = divmod(numerator, 4)
    if remainder != 0:
        raise ArithmeticError("integer-locus cosine relation failed exact division")
    return quotient


def trace_values(trace: ScalarTrace) -> tuple[int, ...]:
    return tuple(state.value for state in trace.states)


def parity_observer(trace: ScalarTrace) -> tuple[int, ...]:
    """Downstream view; it is not read by execution."""

    if type(trace) is not ScalarTrace:
        raise TypeError("trace must be exact ScalarTrace")
    return tuple(euclidean_mod(state.value, 2) for state in trace.states)


def binary_digit_rows(trace: ScalarTrace) -> tuple[str, ...]:
    """Downstream exact rendering for nonnegative traces."""

    if type(trace) is not ScalarTrace:
        raise TypeError("trace must be exact ScalarTrace")
    rows: list[str] = []
    for state in trace.states:
        if state.value < 0:
            raise ValueError("binary digit rows require a nonnegative view profile")
        rows.append(format(state.value, "b"))
    return tuple(rows)


def bit_length_observer(trace: ScalarTrace) -> tuple[int, ...]:
    if type(trace) is not ScalarTrace:
        raise TypeError("trace must be exact ScalarTrace")
    return tuple(abs(state.value).bit_length() for state in trace.states)


@dataclass(frozen=True)
class CycleReport:
    first_index: int
    repeated_at: int
    cycle: tuple[int, ...]


def first_cycle(trace: ScalarTrace) -> CycleReport | None:
    """A pure analyzer: finding a repeat never changes requested execution."""

    seen: dict[int, int] = {}
    for index, state in enumerate(trace.states):
        if state.value in seen:
            first = seen[state.value]
            return CycleReport(
                first,
                index,
                tuple(item.value for item in trace.states[first:index]),
            )
        seen[state.value] = index
    return None


CONWAY_FRACTIONS = (
    PositiveFraction(17, 91),
    PositiveFraction(78, 85),
    PositiveFraction(19, 51),
    PositiveFraction(23, 38),
    PositiveFraction(29, 33),
    PositiveFraction(77, 29),
    PositiveFraction(95, 23),
    PositiveFraction(77, 19),
    PositiveFraction(1, 17),
    PositiveFraction(11, 13),
    PositiveFraction(13, 11),
    PositiveFraction(15, 14),
    PositiveFraction(15, 2),
    PositiveFraction(55, 1),
)


@dataclass(frozen=True)
class ResidueFractionChoice:
    residue: int
    selected_index: int | None
    selected_fraction: PositiveFraction | None
    tested_integral: tuple[bool, ...]


@dataclass(frozen=True)
class LazyOrderedFractionResidueView:
    """Exact periodic selection relation with zero materialized table rows."""

    program: OrderedFractionProgram
    modulus: int

    def __post_init__(self) -> None:
        if type(self.program) is not OrderedFractionProgram:
            raise TypeError("lazy residue view needs exact OrderedFractionProgram")
        expected = lcm(*(fraction.denominator for fraction in self.program.fractions))
        modulus = checked_modulus(self.modulus)
        if modulus != expected:
            raise ValueError("lazy residue modulus must be the denominator LCM")

    @classmethod
    def compile(cls, program: object) -> "LazyOrderedFractionResidueView":
        if type(program) is not OrderedFractionProgram:
            raise TypeError("compile needs exact OrderedFractionProgram")
        modulus = lcm(*(fraction.denominator for fraction in program.fractions))
        return cls(program, modulus)

    @property
    def materialized_entry_count(self) -> int:
        return 0

    def choice_for_residue(self, value: object) -> ResidueFractionChoice:
        residue = exact_int(value, "residue")
        if not 0 <= residue < self.modulus:
            raise ValueError("residue is outside the lazy view modulus")
        flags: list[bool] = []
        for index, fraction in enumerate(self.program.fractions):
            applicable = residue % fraction.denominator == 0
            flags.append(applicable)
            if applicable:
                return ResidueFractionChoice(
                    residue,
                    index,
                    fraction,
                    tuple(flags),
                )
        return ResidueFractionChoice(residue, None, None, tuple(flags))

    def choice_for_value(self, value: object) -> ResidueFractionChoice:
        integer = checked_integer_value(value, POSITIVE, "fraction input")
        return self.choice_for_residue(euclidean_mod(integer, self.modulus))


def must_raise(error: type[BaseException], operation: object) -> int:
    if not callable(operation):
        raise TypeError("hostile test operation must be callable")
    try:
        operation()
    except error:
        return 1
    except Exception as exc:  # pragma: no cover - diagnostic path
        raise AssertionError(
            f"expected {error.__name__}, got {type(exc).__name__}: {exc}"
        ) from exc
    raise AssertionError(f"expected {error.__name__}")


def audit_euclidean_mod() -> tuple[int, int, int]:
    checks = 0
    negative_checks = 0
    huge_checks = 0
    for modulus in range(1, 33):
        for value in range(-1024, 1025):
            residue = euclidean_mod(value, modulus)
            quotient = (value - residue) // modulus
            assert value == quotient * modulus + residue
            assert 0 <= residue < modulus
            checks += 1
            negative_checks += value < 0
    huge_values = (
        2**4096 + 17,
        -(2**4096) - 17,
        10**2000 + 123456789,
        -(10**2000) - 123456789,
    )
    for modulus in (2, 3, 17, 97, 65537):
        for value in huge_values:
            residue = euclidean_mod(value, modulus)
            assert value == ((value - residue) // modulus) * modulus + residue
            assert 0 <= residue < modulus
            checks += 1
            huge_checks += 1
    assert euclidean_mod(-1, 2) == 1
    assert euclidean_mod(-2, 2) == 0
    assert euclidean_mod(-17, 5) == 3
    return checks, negative_checks, huge_checks


def audit_direct_generic_commutation() -> tuple[int, int, int, int]:
    commutations = 0
    witness_replays = 0
    branch_zero = 0
    branch_one = 0
    profiles = (
        (parity_program_a, direct_parity_a),
        (parity_program_b, direct_parity_b),
        (standard_3n_plus_1, direct_standard_3n_plus_1),
    )
    carrier_values = (
        (POSITIVE, range(1, 513)),
        (NONNEGATIVE, range(0, 513)),
        (SIGNED, range(-512, 513)),
    )
    for constructor, direct in profiles:
        for carrier, values in carrier_values:
            program = constructor(carrier)
            for value in values:
                state = ScalarConfiguration(carrier, value)
                result = advance(program, state)
                assert type(result) is Advanced
                assert result.configuration == ScalarConfiguration(carrier, direct(value))
                witness = result.event.witness
                assert type(witness) is ResidueBranchWitness
                assert verify_residue_witness(program, witness)
                assert result.event.before == state
                assert result.event.assignment == ScalarAssignment(
                    SCALAR_LOCUS,
                    direct(value),
                )
                commutations += 1
                witness_replays += 1
                if witness.residue == 0:
                    branch_zero += 1
                else:
                    assert witness.residue == 1
                    branch_one += 1
    return commutations, witness_replays, branch_zero, branch_one


def audit_arbitrary_precision() -> tuple[int, int, int]:
    values = (
        2**4096,
        2**4096 + 1,
        10**2000,
        10**2000 + 1,
        -(2**4096),
        -(2**4096) - 1,
        -(10**2000),
        -(10**2000) - 1,
    )
    checks = 0
    max_bits = 0
    max_decimal_digits = 0
    profiles = (
        (parity_program_a(SIGNED), direct_parity_a),
        (parity_program_b(SIGNED), direct_parity_b),
        (standard_3n_plus_1(SIGNED), direct_standard_3n_plus_1),
    )
    for program, direct in profiles:
        for value in values:
            trace = run(program, ScalarConfiguration(SIGNED, value), 3)
            expected = [value]
            for _ in range(3):
                expected.append(direct(expected[-1]))
            assert trace_values(trace) == tuple(expected)
            assert len(trace.states) == 4 and len(trace.events) == 3
            checks += 1
            max_bits = max(max_bits, *(abs(item).bit_length() for item in expected))
            max_decimal_digits = max(
                max_decimal_digits,
                *(len(str(abs(item))) for item in expected),
            )
    return checks, max_bits, max_decimal_digits


def audit_complete_table_no_precedence() -> tuple[int, int, int]:
    formulas = (
        AffineQuotient(1, 0, 1),
        AffineQuotient(1, 2, 1),
        AffineQuotient(1, -2, 1),
    )
    rows = tuple(enumerate(formulas))
    canonical = complete_residue_map_from_rows(SIGNED, 3, rows)
    permutation_commutations = 0
    for order in permutations(rows):
        rebuilt = complete_residue_map_from_rows(SIGNED, 3, tuple(order))
        assert rebuilt == canonical
        for value in range(-30, 31):
            left = advance(canonical, ScalarConfiguration(SIGNED, value))
            right = advance(rebuilt, ScalarConfiguration(SIGNED, value))
            assert left == right
            permutation_commutations += 1
    selected_rows = 0
    for value in range(-300, 301):
        result = advance(canonical, ScalarConfiguration(SIGNED, value))
        assert type(result) is Advanced
        witness = result.event.witness
        assert type(witness) is ResidueBranchWitness
        assert witness.residue == euclidean_mod(value, 3)
        selected_rows += 1
    # The only branch identity is the canonical residue, never input row order.
    assert tuple(range(canonical.modulus)) == (0, 1, 2)
    return len(tuple(permutations(rows))), permutation_commutations, selected_rows


def audit_source_prefixes_and_relations() -> tuple[int, int, int, int]:
    main_a = run(parity_program_a(), ScalarConfiguration(POSITIVE, 1), len(MAIN_A_PREFIX) - 1)
    assert trace_values(main_a) == MAIN_A_PREFIX
    assert parity_observer(main_a) == tuple(value % 2 for value in MAIN_A_PREFIX)
    assert binary_digit_rows(main_a) == tuple(format(value, "b") for value in MAIN_A_PREFIX)

    main_b_seed1 = run(parity_program_b(), ScalarConfiguration(POSITIVE, 1), 32)
    assert trace_values(main_b_seed1) == (1,) * 33
    assert len(main_b_seed1.events) == 32
    assert all(event.outcome == "Advanced" for event in main_b_seed1.events)

    main_b_seed6 = run(
        parity_program_b(),
        ScalarConfiguration(POSITIVE, 6),
        len(MAIN_B_SEED6_PREFIX) - 1,
    )
    assert trace_values(main_b_seed6) == MAIN_B_SEED6_PREFIX
    assert bit_length_observer(main_b_seed6) == tuple(
        value.bit_length() for value in MAIN_B_SEED6_PREFIX
    )

    # Page 122's register-machine relation is checked as a relation only: after
    # A's first event, A[t+1] = 3 * R[t].  R is not installed as native state.
    register_relation = [1]
    for _ in range(64):
        old = register_relation[-1]
        register_relation.append(
            3 * old // 2 if old % 2 == 0 else (3 * old + 1) // 2
        )
    longer_a = run(parity_program_a(), ScalarConfiguration(POSITIVE, 1), 65)
    relation_checks = 0
    for index, value in enumerate(register_relation):
        assert longer_a.states[index + 1].value == 3 * value
        relation_checks += 1
    return (
        len(main_a.events),
        len(main_b_seed1.events),
        len(main_b_seed6.events),
        relation_checks,
    )


def assert_exact_cycle(
    program: CompleteResidueIntegerMap,
    cycle: tuple[int, ...],
) -> int:
    assert cycle
    trace = run(
        program,
        ScalarConfiguration(program.carrier, cycle[0]),
        len(cycle),
    )
    assert trace_values(trace) == cycle + (cycle[0],)
    assert len(trace.events) == len(cycle)
    assert all(event.outcome == "Advanced" for event in trace.events)
    report = first_cycle(trace)
    assert report == CycleReport(0, len(cycle), cycle)
    return len(cycle)


def audit_cycles_fixed_points_and_trace_shape() -> tuple[int, int, int, int, int]:
    source_cycles = 0
    cycle_events = 0
    cycle_states = 0
    for cycle in MAIN_B_SOURCE_CYCLES:
        cycle_events += assert_exact_cycle(parity_program_b(POSITIVE), cycle)
        cycle_states += len(cycle) + 1
        source_cycles += 1
    cycle_events += assert_exact_cycle(
        standard_3n_plus_1(POSITIVE),
        STANDARD_POSITIVE_CYCLE,
    )
    cycle_states += len(STANDARD_POSITIVE_CYCLE) + 1
    source_cycles += 1
    for cycle in STANDARD_SIGNED_CYCLES:
        cycle_events += assert_exact_cycle(standard_3n_plus_1(SIGNED), cycle)
        cycle_states += len(cycle) + 1
        source_cycles += 1

    fixed_runs = (
        run(parity_program_b(POSITIVE), ScalarConfiguration(POSITIVE, 1), 40),
        run(parity_program_a(NONNEGATIVE), ScalarConfiguration(NONNEGATIVE, 0), 40),
        run(parity_program_b(NONNEGATIVE), ScalarConfiguration(NONNEGATIVE, 0), 40),
        run(standard_3n_plus_1(NONNEGATIVE), ScalarConfiguration(NONNEGATIVE, 0), 40),
        run(standard_3n_plus_1(SIGNED), ScalarConfiguration(SIGNED, -1), 40),
    )
    fixed_point_events = 0
    for trace in fixed_runs:
        assert len(trace.events) == 40
        assert len(trace.states) == 41
        assert trace.terminal is None
        assert len(set(trace_values(trace))) == 1
        assert first_cycle(trace) is not None
        fixed_point_events += len(trace.events)

    trace_shape_checks = 0
    for horizon in range(0, 65):
        trace = run(parity_program_a(), ScalarConfiguration(POSITIVE, 1), horizon)
        assert len(trace.events) == horizon
        assert len(trace.states) == horizon + 1
        assert trace.terminal is None
        trace_shape_checks += 1
    return (
        source_cycles,
        cycle_events,
        cycle_states,
        fixed_point_events,
        trace_shape_checks,
    )


def audit_noninjective_history() -> tuple[int, int, int]:
    witnesses = (
        (parity_program_a(), 3, 4, 6),
        (parity_program_b(), 2, 9, 5),
        (standard_3n_plus_1(), 3, 10, 5),
    )
    merges = 0
    distinct_traces = 0
    retained_history_fields = 0
    for program, left_seed, right_seed, merged in witnesses:
        left = run(program, ScalarConfiguration(POSITIVE, left_seed), 1)
        right = run(program, ScalarConfiguration(POSITIVE, right_seed), 1)
        assert left.states[-1] == right.states[-1] == ScalarConfiguration(POSITIVE, merged)
        assert left.states[0] != right.states[0]
        assert left != right
        assert left.events[0].witness != right.events[0].witness
        merges += 1
        distinct_traces += 1
    state_field_names = tuple(field.name for field in fields(ScalarConfiguration))
    assert state_field_names == ("carrier", "value")
    assert not ({"history", "previous", "branch", "time", "control"} & set(state_field_names))
    return merges, distinct_traces, retained_history_fields


def audit_branch_witnesses() -> tuple[int, int, int]:
    residue_witnesses = 0
    fraction_witnesses = 0
    forged_rejections = 0
    for program in (
        parity_program_a(SIGNED),
        parity_program_b(SIGNED),
        standard_3n_plus_1(SIGNED),
    ):
        for value in range(-50, 51):
            result = advance(program, ScalarConfiguration(SIGNED, value))
            assert type(result) is Advanced
            witness = result.event.witness
            assert type(witness) is ResidueBranchWitness
            assert verify_residue_witness(program, witness)
            forged_residue = ResidueBranchWitness(
                witness.modulus,
                (witness.residue + 1) % witness.modulus,
                witness.formula,
                witness.old_value,
                witness.new_value,
            )
            assert not verify_residue_witness(program, forged_residue)
            forged_rejections += 1
            residue_witnesses += 1

    fractions = OrderedFractionProgram(
        (
            PositiveFraction(3, 2),
            PositiveFraction(5, 2),
            PositiveFraction(7, 3),
            PositiveFraction(1, 1),
        )
    )
    for value in range(1, 101):
        result = advance(fractions, ScalarConfiguration(POSITIVE, value))
        assert type(result) is Advanced
        witness = result.event.witness
        assert type(witness) is FractionBranchWitness
        assert verify_fraction_witness(fractions, witness)
        fraction_witnesses += 1
        if witness.selected_index + 1 < len(fractions.fractions):
            forged = FractionBranchWitness(
                witness.selected_index + 1,
                fractions.fractions[witness.selected_index + 1],
                (False,) * (witness.selected_index + 1) + (True,),
                witness.old_value,
                witness.new_value,
            )
            assert not verify_fraction_witness(fractions, forged)
            forged_rejections += 1
    return residue_witnesses, fraction_witnesses, forged_rejections


def audit_ordered_fraction_partiality() -> tuple[int, int, int, int, int]:
    overlap = OrderedFractionProgram(
        (
            PositiveFraction(3, 2),
            PositiveFraction(5, 2),
            PositiveFraction(1, 1),
        )
    )
    swapped = OrderedFractionProgram(
        (
            PositiveFraction(5, 2),
            PositiveFraction(3, 2),
            PositiveFraction(1, 1),
        )
    )
    left = advance(overlap, ScalarConfiguration(POSITIVE, 2))
    right = advance(swapped, ScalarConfiguration(POSITIVE, 2))
    assert type(left) is Advanced and type(right) is Advanced
    assert left.configuration.value == 3
    assert right.configuration.value == 5
    assert left.event.witness != right.event.witness

    partial = OrderedFractionProgram(
        (PositiveFraction(3, 2), PositiveFraction(5, 3))
    )
    no_applicable_values = (1, 5, 7, 11, 13, 17)
    terminal_outcomes = 0
    retained_states = 0
    for value in no_applicable_values:
        result = advance(partial, ScalarConfiguration(POSITIVE, value))
        assert type(result) is Terminal
        assert result.configuration == ScalarConfiguration(POSITIVE, value)
        assert result.outcome.tested_integral == (False, False)
        assert verify_no_applicable(partial, result.outcome)
        trace = run(partial, ScalarConfiguration(POSITIVE, value), 10)
        assert trace_values(trace) == (value,)
        assert len(trace.events) == 0
        assert trace.terminal == result.outcome
        terminal_outcomes += 1
        retained_states += 1

    # A partial program may advance before reaching an unapplied state.
    delayed = OrderedFractionProgram((PositiveFraction(3, 2),))
    delayed_trace = run(delayed, ScalarConfiguration(POSITIVE, 4), 10)
    assert trace_values(delayed_trace) == (4, 6, 9)
    assert len(delayed_trace.events) == 2
    assert delayed_trace.terminal is not None
    assert verify_no_applicable(delayed, delayed_trace.terminal)
    return 1, terminal_outcomes, retained_states, len(delayed_trace.events), 1


def audit_lazy_fraction_residue_view() -> tuple[int, int, int, int, int, int]:
    small = OrderedFractionProgram(
        (
            PositiveFraction(3, 2),
            PositiveFraction(5, 2),
            PositiveFraction(7, 3),
            PositiveFraction(1, 1),
        )
    )
    view = LazyOrderedFractionResidueView.compile(small)
    assert view.modulus == 6
    assert view.materialized_entry_count == 0
    small_residue_checks = 0
    for residue in range(view.modulus):
        representative = residue if residue > 0 else view.modulus
        choice = view.choice_for_residue(residue)
        result = advance(small, ScalarConfiguration(POSITIVE, representative))
        assert type(result) is Advanced
        witness = result.event.witness
        assert type(witness) is FractionBranchWitness
        assert choice.selected_index == witness.selected_index
        assert choice.selected_fraction == witness.selected_fraction
        assert choice.tested_integral == witness.tested_integral
        small_residue_checks += 1

    conway = OrderedFractionProgram(CONWAY_FRACTIONS)
    conway_view = LazyOrderedFractionResidueView.compile(conway)
    assert conway_view.modulus == 6_469_693_230
    assert conway_view.materialized_entry_count == 0
    assert tuple(field.name for field in fields(LazyOrderedFractionResidueView)) == (
        "program",
        "modulus",
    )
    conway_value_checks = 0
    for value in tuple(range(1, 1001)) + (
        2**127,
        2**127 + 1,
        3**80 * 17,
        5**60 * 91,
    ):
        choice = conway_view.choice_for_value(value)
        result = advance(conway, ScalarConfiguration(POSITIVE, value))
        assert type(result) is Advanced  # denominator-one fallback is total
        witness = result.event.witness
        assert type(witness) is FractionBranchWitness
        assert choice.selected_index == witness.selected_index
        assert choice.selected_fraction == witness.selected_fraction
        assert choice.tested_integral == witness.tested_integral
        conway_value_checks += 1

    # A lazy view also retains holes for genuinely partial ordered programs.
    partial = OrderedFractionProgram((PositiveFraction(3, 2), PositiveFraction(5, 3)))
    partial_view = LazyOrderedFractionResidueView.compile(partial)
    partial_holes = 0
    partial_choices = 0
    for residue in range(partial_view.modulus):
        choice = partial_view.choice_for_residue(residue)
        if choice.selected_index is None:
            partial_holes += 1
        else:
            partial_choices += 1
    assert partial_holes > 0 and partial_choices > 0
    return (
        small_residue_checks,
        conway_value_checks,
        conway_view.modulus,
        conway_view.materialized_entry_count,
        partial_holes,
        partial_choices,
    )


def audit_fraction_lowering_noninjectivity() -> tuple[int, int, int]:
    """Show why a bare compiled decision cannot replace ordered source data."""

    left = OrderedFractionProgram(
        (
            PositiveFraction(3, 2),
            PositiveFraction(5, 2),  # forever shadowed by the first row
            PositiveFraction(1, 1),
        )
    )
    right = OrderedFractionProgram(
        (
            PositiveFraction(3, 2),
            PositiveFraction(7, 2),  # distinct but equally shadowed row
            PositiveFraction(1, 1),
        )
    )
    assert left != right
    left_view = LazyOrderedFractionResidueView.compile(left)
    right_view = LazyOrderedFractionResidueView.compile(right)
    assert left_view.modulus == right_view.modulus == 2
    behavior_checks = 0
    for residue in range(2):
        left_choice = left_view.choice_for_residue(residue)
        right_choice = right_view.choice_for_residue(residue)
        # The selected behavior and selected index agree for every residue;
        # only the retained ordered AST reveals the different shadowed row.
        assert left_choice == right_choice
        representative = residue if residue > 0 else 2
        left_step = advance(left, ScalarConfiguration(POSITIVE, representative))
        right_step = advance(right, ScalarConfiguration(POSITIVE, representative))
        assert type(left_step) is Advanced and type(right_step) is Advanced
        assert left_step.configuration == right_step.configuration
        assert left_step.event.witness == right_step.event.witness
        behavior_checks += 1
    source_hashes = {
        sha256(repr(left).encode("utf-8")).hexdigest(),
        sha256(repr(right).encode("utf-8")).hexdigest(),
    }
    assert len(source_hashes) == 2
    assert left_view.program == left and right_view.program == right
    return 1, behavior_checks, len(source_hashes)


def audit_integer_relation_and_reachable_boundary() -> tuple[int, int, int]:
    relation_checks = 0
    values = tuple(range(-2048, 2049)) + (
        2**4096,
        2**4096 + 1,
        -(2**4096),
        -(2**4096) - 1,
    )
    for value in values:
        assert integer_locus_cosine_relation_a(value) == direct_parity_a(value)
        relation_checks += 1

    # The modulus-30 register-emulation family cannot inherit POSITIVE merely
    # from exact integer closure: its (n-1)/3 row at residue 1 maps n=1 to 0.
    # A reachable encoded subset may avoid that input, but that is a separate
    # invariant proof.  The formula is closed on NONNEGATIVE for this residue
    # and on SIGNED, while it correctly fails POSITIVE validation.
    register_row = AffineQuotient(1, -1, 3)
    validate_formula_on_residue(register_row, SIGNED, 30, 1)
    validate_formula_on_residue(register_row, NONNEGATIVE, 30, 1)
    positive_rejections = must_raise(
        ValueError,
        lambda: validate_formula_on_residue(register_row, POSITIVE, 30, 1),
    )
    assert register_row.apply(1) == 0
    reachable_invariant_separations = 1
    return relation_checks, positive_rejections, reachable_invariant_separations


def audit_conway_source_program() -> tuple[int, int, int, int]:
    program = OrderedFractionProgram(CONWAY_FRACTIONS)
    trace = run(program, ScalarConfiguration(POSITIVE, 2), 8068)
    assert trace.terminal is None
    assert len(trace.events) == 8068
    assert len(trace.states) == 8069
    assert all(
        type(event.witness) is FractionBranchWitness
        and verify_fraction_witness(program, event.witness)
        for event in trace.events
    )
    power_exponents: list[int] = []
    power_steps: list[int] = []
    for step, state in enumerate(trace.states):
        value = state.value
        if value > 0 and value & (value - 1) == 0:
            power_exponents.append(value.bit_length() - 1)
            power_steps.append(step)
    assert tuple(power_exponents[:8]) == (1, 2, 3, 5, 7, 11, 13, 17)
    assert tuple(power_steps[:8]) == (0, 19, 69, 280, 707, 2363, 3876, 8068)
    # Rest of the power-of-two exponents is exactly the initial prime prefix.
    assert tuple(power_exponents[1:8]) == (2, 3, 5, 7, 11, 13, 17)
    selected_indices = {event.witness.selected_index for event in trace.events}
    assert selected_indices
    return len(trace.events), len(power_exponents[:8]), len(selected_indices), 7


def audit_carrier_boundaries() -> tuple[int, int, int, int]:
    positive_checks = 0
    nonnegative_checks = 0
    signed_checks = 0
    closure_programs = 0
    for constructor in (parity_program_a, parity_program_b, standard_3n_plus_1):
        positive = constructor(POSITIVE)
        nonnegative = constructor(NONNEGATIVE)
        signed = constructor(SIGNED)
        closure_programs += 3
        for value in range(1, 257):
            result = advance(positive, ScalarConfiguration(POSITIVE, value))
            assert type(result) is Advanced and result.configuration.value > 0
            positive_checks += 1
        for value in range(0, 257):
            result = advance(nonnegative, ScalarConfiguration(NONNEGATIVE, value))
            assert type(result) is Advanced and result.configuration.value >= 0
            nonnegative_checks += 1
        for value in range(-256, 257):
            result = advance(signed, ScalarConfiguration(SIGNED, value))
            assert type(result) is Advanced
            signed_checks += 1
    return positive_checks, nonnegative_checks, signed_checks, closure_programs


def audit_observer_and_relation_boundaries() -> tuple[int, int, int, int, int]:
    trace = run(parity_program_a(), ScalarConfiguration(POSITIVE, 1), 32)
    parity = parity_observer(trace)
    digits = binary_digit_rows(trace)
    sizes = bit_length_observer(trace)
    assert len(parity) == len(digits) == len(sizes) == len(trace.states)
    assert trace == run(parity_program_a(), ScalarConfiguration(POSITIVE, 1), 32)

    # Closed rule data contain no renderer, analyzer, CA, register, or real-map
    # payload.  Those relations can consume a trace but cannot select a write.
    forbidden = {
        "digits",
        "base",
        "plot",
        "history",
        "cycle",
        "stopping_time",
        "cellular_automaton",
        "register_machine",
        "real_map",
        "callback",
    }
    program_fields = {field.name for field in fields(CompleteResidueIntegerMap)}
    state_fields = {field.name for field in fields(ScalarConfiguration)}
    assignment_fields = {field.name for field in fields(ScalarAssignment)}
    assert not (forbidden & program_fields)
    assert not (forbidden & state_fields)
    assert not (forbidden & assignment_fields)

    cyclic = run(standard_3n_plus_1(), ScalarConfiguration(POSITIVE, 1), 100)
    report = first_cycle(cyclic)
    assert report == CycleReport(0, 2, (1, 2))
    assert len(cyclic.events) == 100 and len(cyclic.states) == 101
    return len(parity), len(digits), len(sizes), len(cyclic.events), len(forbidden)


def audit_no_new_execution_surface() -> tuple[int, int, int, int, int, int]:
    state_fields = tuple(field.name for field in fields(ScalarConfiguration))
    assignment_fields = tuple(field.name for field in fields(ScalarAssignment))
    residue_rule_fields = tuple(field.name for field in fields(CompleteResidueIntegerMap))
    fraction_rule_fields = tuple(field.name for field in fields(OrderedFractionProgram))
    assert state_fields == ("carrier", "value")
    assert assignment_fields == ("locus", "value")
    assert residue_rule_fields == ("carrier", "modulus", "formulas")
    assert fraction_rule_fields == ("fractions",)
    assert select_unique_scalar(ScalarConfiguration(POSITIVE, 1)) == (SCALAR_LOCUS,)
    assert read_self(ScalarConfiguration(POSITIVE, 1), SCALAR_LOCUS) == 1
    # FRONTIER and UPDATE are functions over shared structural roles, not
    # stateful T35 objects; there are therefore zero added fields for either.
    frontier_fields = 0
    neighborhood_fields = 0
    update_fields = 0
    executor_fields = 0
    return (
        len(state_fields),
        len(assignment_fields),
        frontier_fields,
        neighborhood_fields,
        update_fields,
        executor_fields,
    )


def audit_hostile_validation() -> int:
    rejected = 0
    rejected += must_raise(TypeError, lambda: ScalarConfiguration(POSITIVE, True))
    rejected += must_raise(TypeError, lambda: ScalarConfiguration(POSITIVE, 1.0))
    rejected += must_raise(TypeError, lambda: ScalarConfiguration(POSITIVE, "1"))
    rejected += must_raise(ValueError, lambda: ScalarConfiguration(POSITIVE, 0))
    rejected += must_raise(ValueError, lambda: ScalarConfiguration(POSITIVE, -1))
    rejected += must_raise(ValueError, lambda: ScalarConfiguration(NONNEGATIVE, -1))
    rejected += must_raise(ValueError, lambda: ScalarConfiguration("natural", 1))
    rejected += must_raise(TypeError, lambda: euclidean_mod(True, 2))
    rejected += must_raise(TypeError, lambda: euclidean_mod(1, False))
    rejected += must_raise(ValueError, lambda: euclidean_mod(1, 0))
    rejected += must_raise(ValueError, lambda: euclidean_mod(1, -2))
    rejected += must_raise(TypeError, lambda: euclidean_mod(1, 2.0))
    rejected += must_raise(TypeError, lambda: AffineQuotient(True, 0, 1))
    rejected += must_raise(TypeError, lambda: AffineQuotient(1, 0.0, 1))
    rejected += must_raise(ValueError, lambda: AffineQuotient(1, 0, 0))
    rejected += must_raise(ValueError, lambda: AffineQuotient(1, 0, -1))
    rejected += must_raise(
        ValueError,
        lambda: CompleteResidueIntegerMap(POSITIVE, 2, (AffineQuotient(1, 0, 1),)),
    )
    rejected += must_raise(
        TypeError,
        lambda: CompleteResidueIntegerMap(POSITIVE, 1, (lambda n: n,)),
    )
    rejected += must_raise(
        ValueError,
        lambda: CompleteResidueIntegerMap(
            SIGNED,
            2,
            (AffineQuotient(1, 0, 3), AffineQuotient(1, 0, 1)),
        ),
    )
    rejected += must_raise(
        ValueError,
        lambda: CompleteResidueIntegerMap(
            POSITIVE,
            1,
            (AffineQuotient(-1, 0, 1),),
        ),
    )
    rejected += must_raise(
        ValueError,
        lambda: CompleteResidueIntegerMap(
            POSITIVE,
            1,
            (AffineQuotient(1, -1, 1),),
        ),
    )
    rejected += must_raise(
        ValueError,
        lambda: CompleteResidueIntegerMap(
            NONNEGATIVE,
            1,
            (AffineQuotient(-1, 0, 1),),
        ),
    )
    rejected += must_raise(
        ValueError,
        lambda: complete_residue_map_from_rows(
            SIGNED,
            2,
            ((0, AffineQuotient(1, 0, 1)), (0, AffineQuotient(1, 0, 1))),
        ),
    )
    rejected += must_raise(
        ValueError,
        lambda: complete_residue_map_from_rows(
            SIGNED,
            2,
            ((0, AffineQuotient(1, 0, 1)),),
        ),
    )
    rejected += must_raise(
        ValueError,
        lambda: complete_residue_map_from_rows(
            SIGNED,
            2,
            ((0, AffineQuotient(1, 0, 1)), (2, AffineQuotient(1, 0, 1))),
        ),
    )
    rejected += must_raise(
        TypeError,
        lambda: complete_residue_map_from_rows(
            SIGNED,
            1,
            ((0, lambda n: n),),
        ),
    )
    rejected += must_raise(ValueError, lambda: ScalarAssignment("head", 1))
    rejected += must_raise(TypeError, lambda: ScalarAssignment(SCALAR_LOCUS, True))
    rejected += must_raise(
        ValueError,
        lambda: apply_scalar_assignment(
            ScalarConfiguration(POSITIVE, 1),
            ScalarAssignment(SCALAR_LOCUS, 0),
        ),
    )
    rejected += must_raise(
        ValueError,
        lambda: advance(parity_program_a(POSITIVE), ScalarConfiguration(SIGNED, 1)),
    )
    rejected += must_raise(TypeError, lambda: advance(lambda n: n, ScalarConfiguration(POSITIVE, 1)))
    rejected += must_raise(TypeError, lambda: run(parity_program_a(), 1, 3))
    rejected += must_raise(TypeError, lambda: run(parity_program_a(), ScalarConfiguration(POSITIVE, 1), True))
    rejected += must_raise(ValueError, lambda: run(parity_program_a(), ScalarConfiguration(POSITIVE, 1), -1))
    rejected += must_raise(TypeError, lambda: PositiveFraction(True, 2))
    rejected += must_raise(ValueError, lambda: PositiveFraction(0, 1))
    rejected += must_raise(ValueError, lambda: PositiveFraction(-1, 2))
    rejected += must_raise(ValueError, lambda: PositiveFraction(1, 0))
    rejected += must_raise(ValueError, lambda: PositiveFraction(1, -2))
    rejected += must_raise(ValueError, lambda: OrderedFractionProgram(()))
    rejected += must_raise(TypeError, lambda: OrderedFractionProgram((AffineQuotient(1, 0, 1),)))
    rejected += must_raise(
        ValueError,
        lambda: advance(
            OrderedFractionProgram((PositiveFraction(1, 1),)),
            ScalarConfiguration(NONNEGATIVE, 0),
        ),
    )
    rejected += must_raise(
        ValueError,
        lambda: LazyOrderedFractionResidueView(
            OrderedFractionProgram((PositiveFraction(3, 2),)),
            3,
        ),
    )
    rejected += must_raise(
        ValueError,
        lambda: LazyOrderedFractionResidueView.compile(
            OrderedFractionProgram((PositiveFraction(3, 2),))
        ).choice_for_residue(2),
    )
    rejected += must_raise(
        ValueError,
        lambda: FractionBranchWitness(
            1,
            PositiveFraction(3, 2),
            (True, True),
            2,
            3,
        ),
    )
    rejected += must_raise(
        ValueError,
        lambda: FractionBranchWitness(
            0,
            PositiveFraction(3, 2),
            (False,),
            2,
            3,
        ),
    )
    rejected += must_raise(
        ValueError,
        lambda: NoApplicableFraction(
            ScalarConfiguration(POSITIVE, 1),
            (False, True),
        ),
    )
    rejected += must_raise(TypeError, lambda: binary_digit_rows("trace"))
    negative_trace = run(standard_3n_plus_1(SIGNED), ScalarConfiguration(SIGNED, -5), 1)
    rejected += must_raise(ValueError, lambda: binary_digit_rows(negative_trace))
    return rejected


EXPECTED_DIGEST = "95f4efd8620b4e7fed76ba2976dd3bd44cf71ae25112c073aa31359d9925cf74"


def main() -> None:
    euclidean_checks, negative_mod_checks, huge_mod_checks = audit_euclidean_mod()
    (
        direct_generic_commutations,
        residue_witness_replays,
        residue_zero_branches,
        residue_one_branches,
    ) = audit_direct_generic_commutation()
    arbitrary_precision_profiles, maximum_bits, maximum_decimal_digits = (
        audit_arbitrary_precision()
    )
    (
        row_permutations,
        row_permutation_commutations,
        canonical_row_selections,
    ) = audit_complete_table_no_precedence()
    (
        main_a_events,
        main_b_fixed_events,
        main_b_seed6_events,
        register_relation_checks,
    ) = audit_source_prefixes_and_relations()
    (
        source_cycles,
        source_cycle_events,
        source_cycle_states,
        fixed_point_events,
        trace_shape_checks,
    ) = audit_cycles_fixed_points_and_trace_shape()
    history_merges, distinct_merge_traces, retained_history_fields = (
        audit_noninjective_history()
    )
    residue_witnesses, fraction_witnesses, forged_witness_rejections = (
        audit_branch_witnesses()
    )
    (
        fraction_order_discriminators,
        no_applicable_outcomes,
        no_applicable_retained_states,
        delayed_fraction_events,
        delayed_fraction_terminals,
    ) = audit_ordered_fraction_partiality()
    (
        small_fraction_residues,
        conway_residue_value_checks,
        conway_lcm_residues,
        materialized_lcm_rows,
        partial_residue_holes,
        partial_residue_choices,
    ) = audit_lazy_fraction_residue_view()
    (
        noninjective_fraction_lowerings,
        shadowed_fraction_behavior_checks,
        retained_source_ast_hashes,
    ) = audit_fraction_lowering_noninjectivity()
    (
        integer_cosine_relation_checks,
        general_positive_row_rejections,
        reachable_invariant_separations,
    ) = audit_integer_relation_and_reachable_boundary()
    conway_events, conway_power_hits, conway_selected_rows, conway_prime_hits = (
        audit_conway_source_program()
    )
    (
        positive_closure_checks,
        nonnegative_closure_checks,
        signed_closure_checks,
        carrier_programs,
    ) = audit_carrier_boundaries()
    (
        parity_observations,
        digit_observations,
        size_observations,
        analyzer_did_not_stop_events,
        forbidden_execution_roles,
    ) = audit_observer_and_relation_boundaries()
    (
        state_field_count,
        assignment_field_count,
        frontier_field_count,
        neighborhood_field_count,
        update_field_count,
        executor_field_count,
    ) = audit_no_new_execution_surface()
    hostile_rejections = audit_hostile_validation()

    facts = (
        ("domain", DOMAIN),
        ("source_claims", SOURCE_CLAIMS),
        ("architecture_classification", ARCHITECTURE_CLASSIFICATION),
        ("goal2_delta", GOAL2_DELTA),
        ("euclidean_checks", euclidean_checks),
        ("negative_mod_checks", negative_mod_checks),
        ("huge_mod_checks", huge_mod_checks),
        ("direct_generic_commutations", direct_generic_commutations),
        ("residue_witness_replays", residue_witness_replays),
        ("residue_zero_branches", residue_zero_branches),
        ("residue_one_branches", residue_one_branches),
        ("arbitrary_precision_profiles", arbitrary_precision_profiles),
        ("maximum_bits", maximum_bits),
        ("maximum_decimal_digits", maximum_decimal_digits),
        ("row_permutations", row_permutations),
        ("row_permutation_commutations", row_permutation_commutations),
        ("canonical_row_selections", canonical_row_selections),
        ("main_a_prefix", MAIN_A_PREFIX),
        ("main_b_seed6_prefix", MAIN_B_SEED6_PREFIX),
        ("main_a_events", main_a_events),
        ("main_b_fixed_events", main_b_fixed_events),
        ("main_b_seed6_events", main_b_seed6_events),
        ("register_relation_checks", register_relation_checks),
        ("source_cycles", source_cycles),
        ("source_cycle_events", source_cycle_events),
        ("source_cycle_states", source_cycle_states),
        ("fixed_point_events", fixed_point_events),
        ("trace_shape_checks", trace_shape_checks),
        ("history_merges", history_merges),
        ("distinct_merge_traces", distinct_merge_traces),
        ("retained_history_fields", retained_history_fields),
        ("residue_witnesses", residue_witnesses),
        ("fraction_witnesses", fraction_witnesses),
        ("forged_witness_rejections", forged_witness_rejections),
        ("fraction_order_discriminators", fraction_order_discriminators),
        ("no_applicable_outcomes", no_applicable_outcomes),
        ("no_applicable_retained_states", no_applicable_retained_states),
        ("delayed_fraction_events", delayed_fraction_events),
        ("delayed_fraction_terminals", delayed_fraction_terminals),
        ("small_fraction_residues", small_fraction_residues),
        ("conway_residue_value_checks", conway_residue_value_checks),
        ("conway_lcm_residues", conway_lcm_residues),
        ("materialized_lcm_rows", materialized_lcm_rows),
        ("partial_residue_holes", partial_residue_holes),
        ("partial_residue_choices", partial_residue_choices),
        ("noninjective_fraction_lowerings", noninjective_fraction_lowerings),
        ("shadowed_fraction_behavior_checks", shadowed_fraction_behavior_checks),
        ("retained_source_ast_hashes", retained_source_ast_hashes),
        ("integer_cosine_relation_checks", integer_cosine_relation_checks),
        ("general_positive_row_rejections", general_positive_row_rejections),
        ("reachable_invariant_separations", reachable_invariant_separations),
        ("conway_events", conway_events),
        ("conway_power_hits", conway_power_hits),
        ("conway_selected_rows", conway_selected_rows),
        ("conway_prime_hits", conway_prime_hits),
        ("positive_closure_checks", positive_closure_checks),
        ("nonnegative_closure_checks", nonnegative_closure_checks),
        ("signed_closure_checks", signed_closure_checks),
        ("carrier_programs", carrier_programs),
        ("parity_observations", parity_observations),
        ("digit_observations", digit_observations),
        ("size_observations", size_observations),
        ("analyzer_did_not_stop_events", analyzer_did_not_stop_events),
        ("forbidden_execution_roles", forbidden_execution_roles),
        ("hostile_rejections", hostile_rejections),
        ("state_field_count", state_field_count),
        ("assignment_field_count", assignment_field_count),
        ("frontier_field_count", frontier_field_count),
        ("neighborhood_field_count", neighborhood_field_count),
        ("update_field_count", update_field_count),
        ("executor_field_count", executor_field_count),
        ("strict_rule", "complete_Euclidean_residue_indexed_closed_unary_integer_map"),
        ("table_precedence", "absent_disjoint_total_residue_partition"),
        ("fraction_sibling", "ordered_first_applicable_positive_fraction_partial_rule"),
        ("fraction_compilation", "lazy_LCM_residue_relation_with_order_source_AST_provenance_and_witness_retained"),
        ("bare_fraction_lowering", "behavior_preserving_but_not_injective_due_to_shadowed_duplicate_or_redundant_rows"),
        ("general_table_carrier", "integer_closure_is_distinct_from_positive_and_encoded_reachable_subset_invariants"),
        ("continuous_relation", "exact_integer_locus_cosine_identity_is_external_to_native_execution"),
        ("trace_contract", "h_advanced_events_yield_h_plus_1_snapshots"),
        ("history_contract", "trace_only_not_configuration_and_noninjective_steps_merge"),
        ("cycle_contract", "fixed_points_and_cycles_remain_Advanced"),
        ("observer_boundary", "digits_sizes_parity_cycles_growth_CA_register_real_maps_do_not_select_writes"),
    )
    digest = sha256(repr(facts).encode("utf-8")).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FROZEN":
        assert digest == EXPECTED_DIGEST

    print("T35 semantic oracle: PASS")
    print(
        f"euclidean_mod_checks={euclidean_checks}; signed_negative={negative_mod_checks}; "
        f"huge={huge_mod_checks}; exact_integer_carriers=positive/nonnegative/signed"
    )
    print(
        f"direct_generic_commutations={direct_generic_commutations}; "
        f"residue_witness_replays={residue_witness_replays}; "
        f"branches=r0:{residue_zero_branches}/r1:{residue_one_branches}; "
        "complete_table_precedence=absent"
    )
    print(
        f"arbitrary_precision_profiles={arbitrary_precision_profiles}; "
        f"max_bits={maximum_bits}; max_decimal_digits={maximum_decimal_digits}; "
        f"row_permutations={row_permutations}; "
        f"row_permutation_commutations={row_permutation_commutations}"
    )
    print(f"main_A_prefix={MAIN_A_PREFIX}")
    print(f"main_B_seed6_prefix={MAIN_B_SEED6_PREFIX}")
    print(
        f"main_events=A:{main_a_events}/B_fixed:{main_b_fixed_events}/B_seed6:{main_b_seed6_events}; "
        f"register_relation_checks={register_relation_checks}"
    )
    print(
        f"source_cycles={source_cycles}; cycle_events={source_cycle_events}; "
        f"fixed_point_advanced_events={fixed_point_events}; "
        f"trace_h_plus_1_checks={trace_shape_checks}; noninjective_merges={history_merges}"
    )
    print(
        f"branch_witnesses=residue:{residue_witnesses}/fraction:{fraction_witnesses}; "
        f"forged_witness_rejections={forged_witness_rejections}; "
        f"fraction_order_discriminators={fraction_order_discriminators}"
    )
    print(
        f"NoApplicableFraction={no_applicable_outcomes}; retained_states={no_applicable_retained_states}; "
        f"delayed_partial_trace={delayed_fraction_events}-events_then-{delayed_fraction_terminals}-terminal"
    )
    print(
        f"fraction_lazy_residue_checks=small:{small_fraction_residues}/Conway:{conway_residue_value_checks}; "
        f"Conway_LCM={conway_lcm_residues}; materialized_rows={materialized_lcm_rows}; "
        f"partial_residue_holes={partial_residue_holes}"
    )
    print(
        f"bare_fraction_lowering_noninjective={noninjective_fraction_lowerings}; "
        f"shadowed_behavior_checks={shadowed_fraction_behavior_checks}; "
        f"retained_source_AST_hashes={retained_source_ast_hashes}; "
        "lossless_claim=ordered_source_plus_provenance_required"
    )
    print(
        f"integer_cosine_relation_checks={integer_cosine_relation_checks}; "
        f"general_positive_row_rejections={general_positive_row_rejections}; "
        f"reachable_invariant_separations={reachable_invariant_separations}"
    )
    print(
        f"Conway_source_events={conway_events}; power_hits={conway_power_hits}; "
        f"prime_exponents={conway_prime_hits}; selected_fraction_rows={conway_selected_rows}"
    )
    print(
        f"carrier_closure_checks=positive:{positive_closure_checks}/"
        f"nonnegative:{nonnegative_closure_checks}/signed:{signed_closure_checks}; "
        f"hostile_rejections={hostile_rejections}"
    )
    print(
        f"execution_surface=state:{state_field_count}/assignment:{assignment_field_count}/"
        f"frontier:{frontier_field_count}/neighborhood:{neighborhood_field_count}/"
        f"update:{update_field_count}/executor:{executor_field_count}; "
        "architecture=T34_singleton_self_assignment_UPDATE_reused"
    )
    print(f"semantic_digest={digest}")


if __name__ == "__main__":
    main()
