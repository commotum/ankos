#!/usr/bin/env python3
"""Dependency-free semantic oracle for T36 digit-reversal arithmetic.

The strict Book construction remains the T34/T35 discrete ``t+0D`` scalar
event.  Its rule makes a positional representation visible, reverses that
representation, decodes it, and adds it to the old exact integer.  Canonical
digit words and nonnegative integers are losslessly equivalent representations;
neither requires a new state, FRONTIER, NEIGHBORHOOD, UPDATE, or executor.

Two Notes variants make leading-zero policy explicit.  Fixed-width evolution
drops a carry beyond the declared width.  Grow-width evolution adds exactly
one position at every event, even when its new leading digit is zero.  The
latter therefore uses a tagged ``(integer, width)`` value: width is
future-determining state, but it is still one value at the shared scalar
locus and is committed by the ordinary same-locus assignment.

This proof oracle evaluates every governed profile in two independent ways:
an integer encode/reverse/decode/add path and a direct grade-school digit-word
addition path.  It binds exact structural program keys, replayable witnesses,
events, outcomes, and traces.  It imports no runtime code, is silent on
import, and fails closed under ``python -O``.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass, replace
from hashlib import sha256
from typing import TypeAlias


if not __debug__:
    raise RuntimeError("T36 semantic oracle must run with assertions enabled")


DOMAIN = "discrete_t_plus_0D"
SCALAR_LOCUS = "unique_scalar"
POSITIVE = "positive_integer"
NONNEGATIVE = "nonnegative_integer"
WIDTH_TAGGED = "width_tagged_nonnegative_integer"
CARRIERS = (POSITIVE, NONNEGATIVE, WIDTH_TAGGED)


SOURCE_CLAIMS = (
    ("BOOK:12503-12505", "whole integers have exact positional digit codecs"),
    ("BOOK:1531-1541", "digit-coordinate arithmetic can be nonlocal"),
    ("BOOK:1543-1545", "binary reversal-add starts at 16 and is shown for 180 events"),
    ("BOOK:1547-1553", "the seed-512 run is shown at 1000 and one million events"),
    ("BOOK:12635-12637", "the rule is n plus decoded reversed binary digits"),
    ("BOOK:12639", "growth, regular regions, and effective periods are observations"),
    ("BOOK:12643", "fixed-width drops carry while grow-width adds one left position"),
    ("BOOK:12646-12658", "fixed-width digit reversal is a finite positional relation"),
)


ARCHITECTURE_CLASSIFICATION = (
    "1: reuse the T34/T35 exact scalar configuration, UniqueScalar FRONTIER, Self read, assignment, UPDATE, trace, and StepResult",
    "2: parameterize the closed unary RULE by an exact base and explicit canonical/fixed/grow positional codec",
    "3: canonical scalar and word forms commute losslessly; grow width is a tagged product value rather than a state class",
    "4: no new execution algebra, executor, family branch, callback, hidden word, or history-bearing state",
)


GOAL2_DELTA = (
    "Add exact positional encode/decode and ReverseDigits nodes to the closed unary scalar RULE algebra.",
    "Keep base, codec profile, and fixed width in exact structural program identity.",
    "Use arbitrary-precision integers and tuple digits; never string reversal, machine width, or JSON-number identity.",
    "Retain leading zeros in rule witnesses and in fixed/grow codecs even when decoding discards their numeric contribution.",
    "Represent grow-width values as a transparent tagged product (integer,width) at the same scalar locus.",
    "Treat fixed carry truncation and grow-width increment as RULE-result semantics, not new UPDATE laws.",
    "Keep visual periodicity, localized structures, regular-region lengths, crops, and randomness as observers.",
    "Add no T36 state class, frontier, neighborhood, update, executor, callback, family dispatch, or hidden history.",
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
    if carrier not in CARRIERS:
        raise ValueError("unknown scalar carrier")
    return carrier


def checked_base(value: object) -> int:
    base = exact_int(value, "base")
    if base < 2:
        raise ValueError("base must be at least two")
    return base


def checked_width(value: object) -> int:
    width = exact_int(value, "width")
    if width < 1:
        raise ValueError("width must be positive")
    return width


def checked_horizon(value: object) -> int:
    horizon = exact_int(value, "horizon")
    if horizon < 0:
        raise ValueError("horizon must be nonnegative")
    return horizon


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


@dataclass(frozen=True)
class CanonicalDigits:
    """Minimal most-significant-first digits; zero is represented by ``(0,)``."""


@dataclass(frozen=True)
class FixedWidthDropCarry:
    """Exactly ``width`` digits; a carry beyond the left edge is discarded."""

    width: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "width", checked_width(self.width))


@dataclass(frozen=True)
class GrowWidth:
    """Read the old width and include exactly one new left digit per event."""


DigitProfile: TypeAlias = CanonicalDigits | FixedWidthDropCarry | GrowWidth


@dataclass(frozen=True)
class WidthTaggedInteger:
    """Transparent product value used only when width affects future evolution."""

    value: int
    width: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", checked_nonnegative(self.value, "value"))
        object.__setattr__(self, "width", checked_width(self.width))


ScalarValue: TypeAlias = int | WidthTaggedInteger


def checked_scalar_value(value: object, name: str = "value") -> ScalarValue:
    if type(value) is int:
        return value
    if type(value) is WidthTaggedInteger:
        return value
    raise TypeError(f"{name} must be an exact int or WidthTaggedInteger")


@dataclass(frozen=True)
class ScalarConfiguration:
    """The reused carrier-tagged single-value configuration."""

    carrier: str
    value: ScalarValue

    def __post_init__(self) -> None:
        carrier = checked_carrier(self.carrier)
        value = checked_scalar_value(self.value)
        if carrier == POSITIVE:
            value = checked_positive(value, "value")
        elif carrier == NONNEGATIVE:
            value = checked_nonnegative(value, "value")
        elif type(value) is not WidthTaggedInteger:
            raise TypeError("width-tagged carrier requires WidthTaggedInteger")
        object.__setattr__(self, "carrier", carrier)
        object.__setattr__(self, "value", value)


@dataclass(frozen=True)
class ScalarAssignment:
    """The reused generic same-locus write."""

    locus: str
    value: ScalarValue

    def __post_init__(self) -> None:
        locus = exact_str(self.locus, "assignment locus")
        if locus != SCALAR_LOCUS:
            raise ValueError("assignment must target the unique scalar locus")
        object.__setattr__(self, "locus", locus)
        object.__setattr__(self, "value", checked_scalar_value(self.value, "assignment value"))


def select_unique_scalar(configuration: object) -> tuple[str, ...]:
    if type(configuration) is not ScalarConfiguration:
        raise TypeError("configuration must be exact ScalarConfiguration")
    return (SCALAR_LOCUS,)


def read_self(configuration: object, locus: object) -> ScalarValue:
    if type(configuration) is not ScalarConfiguration:
        raise TypeError("configuration must be exact ScalarConfiguration")
    if exact_str(locus, "locus") != SCALAR_LOCUS:
        raise ValueError("Self read requires the unique scalar locus")
    return configuration.value


def apply_scalar_assignment(
    configuration: object,
    assignment: object,
) -> ScalarConfiguration:
    if type(configuration) is not ScalarConfiguration:
        raise TypeError("configuration must be exact ScalarConfiguration")
    if type(assignment) is not ScalarAssignment:
        raise TypeError("assignment must be exact ScalarAssignment")
    if assignment.locus != SCALAR_LOCUS:
        raise ValueError("assignment locus mismatch")
    return ScalarConfiguration(configuration.carrier, assignment.value)


@dataclass(frozen=True)
class ReversalAddProgram:
    """Closed positional reversal-add RULE data; never a callback."""

    carrier: str
    base: int
    profile: DigitProfile

    def __post_init__(self) -> None:
        carrier = checked_carrier(self.carrier)
        base = checked_base(self.base)
        if type(self.profile) not in (CanonicalDigits, FixedWidthDropCarry, GrowWidth):
            raise TypeError("profile must be a closed T36 digit profile")
        if type(self.profile) is CanonicalDigits:
            if carrier not in (POSITIVE, NONNEGATIVE):
                raise ValueError("canonical profile requires an integer carrier")
        elif type(self.profile) is FixedWidthDropCarry:
            if carrier != NONNEGATIVE:
                raise ValueError("fixed-width profile requires nonnegative integers")
        elif carrier != WIDTH_TAGGED:
            raise ValueError("grow-width profile requires width-tagged values")
        object.__setattr__(self, "carrier", carrier)
        object.__setattr__(self, "base", base)


ProgramKey: TypeAlias = tuple[object, ...]


def profile_key(profile: object) -> tuple[object, ...]:
    if type(profile) is CanonicalDigits:
        return ("CanonicalDigits/v1",)
    if type(profile) is FixedWidthDropCarry:
        return ("FixedWidthDropCarry/v1", profile.width)
    if type(profile) is GrowWidth:
        return ("GrowWidth/v1",)
    raise TypeError("unknown digit profile")


def checked_program_key(value: object) -> ProgramKey:
    key = exact_tuple(value, "program key")
    if len(key) != 4 or key[0] != "ReversalAddProgram/v1":
        raise ValueError("invalid T36 program key shape")
    carrier = checked_carrier(key[1])
    base = checked_base(key[2])
    encoded_profile = exact_tuple(key[3], "profile key")
    if encoded_profile == ("CanonicalDigits/v1",):
        profile: DigitProfile = CanonicalDigits()
    elif len(encoded_profile) == 2 and encoded_profile[0] == "FixedWidthDropCarry/v1":
        profile = FixedWidthDropCarry(encoded_profile[1])
    elif encoded_profile == ("GrowWidth/v1",):
        profile = GrowWidth()
    else:
        raise ValueError("invalid T36 profile key")
    ReversalAddProgram(carrier, base, profile)
    return key


def structural_program_key(program: object) -> ProgramKey:
    if type(program) is not ReversalAddProgram:
        raise TypeError("program must be exact ReversalAddProgram")
    return (
        "ReversalAddProgram/v1",
        program.carrier,
        program.base,
        profile_key(program.profile),
    )


def structural_program_id(program: object) -> str:
    key = structural_program_key(program)
    return sha256(repr(key).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ProgramProvenance:
    """Exact key governs replay; SHA is only derived display/cache metadata."""

    key: ProgramKey
    display_id: str

    def __post_init__(self) -> None:
        key = checked_program_key(self.key)
        display_id = exact_str(self.display_id, "display id")
        expected = sha256(repr(key).encode("utf-8")).hexdigest()
        if display_id != expected:
            raise ValueError("display id is not derived from the exact key")
        object.__setattr__(self, "key", key)


def program_provenance(program: object) -> ProgramProvenance:
    return ProgramProvenance(structural_program_key(program), structural_program_id(program))


def validate_program_configuration(
    program: object,
    configuration: object,
) -> None:
    if type(program) is not ReversalAddProgram:
        raise TypeError("program must be exact ReversalAddProgram")
    if type(configuration) is not ScalarConfiguration:
        raise TypeError("configuration must be exact ScalarConfiguration")
    if configuration.carrier != program.carrier:
        raise ValueError("program/configuration carrier mismatch")
    if type(program.profile) is CanonicalDigits:
        if type(configuration.value) is not int:
            raise TypeError("canonical profile requires an exact integer value")
    elif type(program.profile) is FixedWidthDropCarry:
        if type(configuration.value) is not int:
            raise TypeError("fixed-width profile requires an exact integer value")
        if configuration.value >= program.base ** program.profile.width:
            raise ValueError("value does not fit the fixed width")
    else:
        if type(configuration.value) is not WidthTaggedInteger:
            raise TypeError("grow-width profile requires WidthTaggedInteger")
        if configuration.value.value >= program.base ** configuration.value.width:
            raise ValueError("value does not fit its tagged width")


def encode_canonical(value: object, base: object) -> tuple[int, ...]:
    integer = checked_nonnegative(value, "value")
    radix = checked_base(base)
    if integer == 0:
        return (0,)
    reversed_digits: list[int] = []
    remaining = integer
    while remaining:
        remaining, digit = divmod(remaining, radix)
        reversed_digits.append(digit)
    digits = tuple(reversed(reversed_digits))
    if not digits or digits[0] == 0:
        raise ArithmeticError("canonical encoder produced a leading zero")
    return digits


def checked_digits(value: object, base: object, name: str = "digits") -> tuple[int, ...]:
    digits = exact_tuple(value, name)
    radix = checked_base(base)
    if not digits:
        raise ValueError(f"{name} must be nonempty")
    checked: list[int] = []
    for index, item in enumerate(digits):
        digit = exact_int(item, f"{name}[{index}]")
        if not 0 <= digit < radix:
            raise ValueError(f"{name}[{index}] is outside the base")
        checked.append(digit)
    return tuple(checked)


def encode_fixed(value: object, base: object, width: object) -> tuple[int, ...]:
    integer = checked_nonnegative(value, "value")
    radix = checked_base(base)
    size = checked_width(width)
    if integer >= radix ** size:
        raise ValueError("value does not fit fixed-width codec")
    canonical = encode_canonical(integer, radix)
    return (0,) * (size - len(canonical)) + canonical


def decode_digits(digits: object, base: object) -> int:
    radix = checked_base(base)
    sequence = checked_digits(digits, radix)
    result = 0
    for digit in sequence:
        result = result * radix + digit
    return result


def trim_leading_zeros(digits: object, base: object) -> tuple[int, ...]:
    sequence = checked_digits(digits, base)
    index = 0
    while index + 1 < len(sequence) and sequence[index] == 0:
        index += 1
    return sequence[index:]


def add_digit_words_full(
    left: object,
    right: object,
    base: object,
) -> tuple[int, ...]:
    """Independent grade-school addition, retaining one carry position."""

    radix = checked_base(base)
    lhs = checked_digits(left, radix, "left digits")
    rhs = checked_digits(right, radix, "right digits")
    if len(lhs) != len(rhs):
        raise ValueError("word addition requires equal-width operands")
    output = [0] * (len(lhs) + 1)
    carry = 0
    for offset in range(1, len(lhs) + 1):
        total = lhs[-offset] + rhs[-offset] + carry
        carry, output[-offset] = divmod(total, radix)
    output[0] = carry
    if not 0 <= carry < radix:
        raise ArithmeticError("word addition produced an invalid carry")
    return tuple(output)


def reversal_table(base: object, width: object) -> tuple[int, ...]:
    radix = checked_base(base)
    size = checked_width(width)
    return tuple(
        decode_digits(tuple(reversed(encode_fixed(value, radix, size))), radix)
        for value in range(radix ** size)
    )


def numeric_parts(configuration: ScalarConfiguration) -> tuple[int, int | None]:
    if type(configuration.value) is int:
        return configuration.value, None
    return configuration.value.value, configuration.value.width


@dataclass(frozen=True)
class ReversalWitness:
    """Replayable evidence for the complete positional rule evaluation."""

    old_value: int
    old_width: int | None
    digits: tuple[int, ...]
    reversed_digits: tuple[int, ...]
    addend: int
    untruncated_sum: int
    dropped_carry: int | None
    new_value: int
    new_width: int | None
    provenance: ProgramProvenance

    def __post_init__(self) -> None:
        old_value = checked_nonnegative(self.old_value, "old value")
        new_value = checked_nonnegative(self.new_value, "new value")
        old_width = None if self.old_width is None else checked_width(self.old_width)
        new_width = None if self.new_width is None else checked_width(self.new_width)
        digits = exact_tuple(self.digits, "witness digits")
        reversed_digits = exact_tuple(self.reversed_digits, "witness reversed digits")
        for name, sequence in (("digits", digits), ("reversed digits", reversed_digits)):
            if not sequence:
                raise ValueError(f"witness {name} must be nonempty")
            for index, item in enumerate(sequence):
                if exact_int(item, f"witness {name}[{index}]") < 0:
                    raise ValueError("witness digits must be nonnegative")
        if reversed_digits != tuple(reversed(digits)):
            raise ValueError("witness reversal does not reverse the digit tuple")
        addend = checked_nonnegative(self.addend, "addend")
        total = checked_nonnegative(self.untruncated_sum, "untruncated sum")
        if total != old_value + addend:
            raise ValueError("witness sum does not equal old value plus addend")
        dropped = self.dropped_carry
        if dropped is not None:
            dropped = exact_int(dropped, "dropped carry")
            if dropped not in (0, 1):
                raise ValueError("dropped carry must be zero or one")
        if type(self.provenance) is not ProgramProvenance:
            raise TypeError("witness provenance must be exact ProgramProvenance")
        object.__setattr__(self, "old_value", old_value)
        object.__setattr__(self, "old_width", old_width)
        object.__setattr__(self, "digits", digits)
        object.__setattr__(self, "reversed_digits", reversed_digits)
        object.__setattr__(self, "addend", addend)
        object.__setattr__(self, "untruncated_sum", total)
        object.__setattr__(self, "dropped_carry", dropped)
        object.__setattr__(self, "new_value", new_value)
        object.__setattr__(self, "new_width", new_width)


@dataclass(frozen=True)
class ProposedScalarWrite:
    assignment: ScalarAssignment
    witness: ReversalWitness

    def __post_init__(self) -> None:
        if type(self.assignment) is not ScalarAssignment:
            raise TypeError("proposal assignment must be exact ScalarAssignment")
        if type(self.witness) is not ReversalWitness:
            raise TypeError("proposal witness must be exact ReversalWitness")


def _profile_input(
    program: ReversalAddProgram,
    configuration: ScalarConfiguration,
) -> tuple[int, int | None, tuple[int, ...]]:
    validate_program_configuration(program, configuration)
    old_value, tagged_width = numeric_parts(configuration)
    if type(program.profile) is CanonicalDigits:
        return old_value, None, encode_canonical(old_value, program.base)
    if type(program.profile) is FixedWidthDropCarry:
        width = program.profile.width
        return old_value, width, encode_fixed(old_value, program.base, width)
    assert tagged_width is not None
    return old_value, tagged_width, encode_fixed(old_value, program.base, tagged_width)


def _proposal_from_components(
    program: ReversalAddProgram,
    old_value: int,
    old_width: int | None,
    digits: tuple[int, ...],
    reversed_digits: tuple[int, ...],
    addend: int,
    total: int,
    fixed_low_digits: tuple[int, ...] | None = None,
    word_carry: int | None = None,
) -> ProposedScalarWrite:
    if type(program.profile) is CanonicalDigits:
        next_scalar: ScalarValue = total
        dropped_carry = None
        new_width = None
        new_value = total
    elif type(program.profile) is FixedWidthDropCarry:
        width = program.profile.width
        modulus = program.base ** width
        next_integer = total % modulus
        if fixed_low_digits is not None and decode_digits(fixed_low_digits, program.base) != next_integer:
            raise ArithmeticError("word/scalar fixed-width results disagree")
        scalar_carry = total // modulus
        if word_carry is not None and word_carry != scalar_carry:
            raise ArithmeticError("word/scalar carry results disagree")
        next_scalar = next_integer
        dropped_carry = scalar_carry
        new_width = width
        new_value = next_integer
    else:
        if old_width is None:
            raise ArithmeticError("grow-width input lost its width")
        next_scalar = WidthTaggedInteger(total, old_width + 1)
        dropped_carry = None
        new_width = old_width + 1
        new_value = total
    witness = ReversalWitness(
        old_value,
        old_width,
        digits,
        reversed_digits,
        addend,
        total,
        dropped_carry,
        new_value,
        new_width,
        program_provenance(program),
    )
    return ProposedScalarWrite(ScalarAssignment(SCALAR_LOCUS, next_scalar), witness)


def evaluate_closed_rule(
    program: object,
    configuration: object,
) -> ProposedScalarWrite:
    """Integer encode/reverse/decode/add evaluator."""

    if type(program) is not ReversalAddProgram:
        raise TypeError("program must be exact ReversalAddProgram")
    if type(configuration) is not ScalarConfiguration:
        raise TypeError("configuration must be exact ScalarConfiguration")
    old_value, old_width, digits = _profile_input(program, configuration)
    reversed_digits = tuple(reversed(digits))
    addend = decode_digits(reversed_digits, program.base)
    total = old_value + addend
    return _proposal_from_components(
        program,
        old_value,
        old_width,
        digits,
        reversed_digits,
        addend,
        total,
    )


def evaluate_word_rule(
    program: object,
    configuration: object,
) -> ProposedScalarWrite:
    """Independent direct word reversal and grade-school addition evaluator."""

    if type(program) is not ReversalAddProgram:
        raise TypeError("program must be exact ReversalAddProgram")
    if type(configuration) is not ScalarConfiguration:
        raise TypeError("configuration must be exact ScalarConfiguration")
    old_value, old_width, digits = _profile_input(program, configuration)
    reversed_digits = tuple(reversed(digits))
    full_sum_digits = add_digit_words_full(digits, reversed_digits, program.base)
    addend = decode_digits(reversed_digits, program.base)
    total = decode_digits(full_sum_digits, program.base)
    fixed_low: tuple[int, ...] | None = None
    word_carry: int | None = None
    if type(program.profile) is CanonicalDigits:
        if encode_canonical(total, program.base) != trim_leading_zeros(full_sum_digits, program.base):
            raise ArithmeticError("canonical scalar/word encoding did not commute")
    elif type(program.profile) is FixedWidthDropCarry:
        word_carry = full_sum_digits[0]
        fixed_low = full_sum_digits[1:]
    else:
        assert old_width is not None
        if len(full_sum_digits) != old_width + 1:
            raise ArithmeticError("grow-width result does not add one position")
        if encode_fixed(total, program.base, old_width + 1) != full_sum_digits:
            raise ArithmeticError("grow-width scalar/word encoding did not commute")
    return _proposal_from_components(
        program,
        old_value,
        old_width,
        digits,
        reversed_digits,
        addend,
        total,
        fixed_low,
        word_carry,
    )


@dataclass(frozen=True)
class TransitionEvent:
    before: ScalarConfiguration
    read_value: ScalarValue
    assignment: ScalarAssignment
    after: ScalarConfiguration
    witness: ReversalWitness

    def __post_init__(self) -> None:
        if type(self.before) is not ScalarConfiguration:
            raise TypeError("event before must be exact ScalarConfiguration")
        if type(self.after) is not ScalarConfiguration:
            raise TypeError("event after must be exact ScalarConfiguration")
        if self.before.carrier != self.after.carrier:
            raise ValueError("event cannot change the scalar carrier")
        if self.read_value != self.before.value:
            raise ValueError("event read does not equal the old scalar value")
        if type(self.assignment) is not ScalarAssignment:
            raise TypeError("event assignment must be exact ScalarAssignment")
        if self.assignment.value != self.after.value:
            raise ValueError("event assignment does not equal the after value")
        if type(self.witness) is not ReversalWitness:
            raise TypeError("event witness must be exact ReversalWitness")
        old_value, old_width = numeric_parts(self.before)
        new_value, new_width = numeric_parts(self.after)
        expected_old_width = old_width
        if old_width is None and self.witness.old_width is not None:
            expected_old_width = self.witness.old_width
        if (self.witness.old_value, self.witness.old_width) != (
            old_value,
            expected_old_width,
        ):
            raise ValueError("event witness does not describe the before value")
        expected_new_width = new_width
        if new_width is None and self.witness.old_width is not None:
            expected_new_width = self.witness.old_width
        if (self.witness.new_value, self.witness.new_width) != (
            new_value,
            expected_new_width,
        ):
            raise ValueError("event witness does not describe the after value")


@dataclass(frozen=True)
class Advanced:
    changed: bool

    def __post_init__(self) -> None:
        if type(self.changed) is not bool:
            raise TypeError("Advanced.changed must be an exact bool")


@dataclass(frozen=True)
class StepResult:
    successors: tuple[ScalarConfiguration, ...]
    outcome: Advanced
    event: TransitionEvent

    def __post_init__(self) -> None:
        successors = exact_tuple(self.successors, "successors")
        if len(successors) != 1 or type(successors[0]) is not ScalarConfiguration:
            raise ValueError("a valid T36 step has exactly one scalar successor")
        if type(self.outcome) is not Advanced:
            raise TypeError("T36 outcome must be exact Advanced")
        if type(self.event) is not TransitionEvent:
            raise TypeError("T36 result requires an exact TransitionEvent")
        if successors[0] != self.event.after:
            raise ValueError("successor does not equal event after state")
        if self.outcome.changed != (self.event.after != self.event.before):
            raise ValueError("Advanced.changed disagrees with complete state equality")
        object.__setattr__(self, "successors", successors)


def advance(program: object, configuration: object) -> StepResult:
    if type(program) is not ReversalAddProgram:
        raise TypeError("program must be exact ReversalAddProgram")
    if type(configuration) is not ScalarConfiguration:
        raise TypeError("configuration must be exact ScalarConfiguration")
    validate_program_configuration(program, configuration)
    locus = select_unique_scalar(configuration)[0]
    old = read_self(configuration, locus)
    proposal = evaluate_closed_rule(program, configuration)
    after = apply_scalar_assignment(configuration, proposal.assignment)
    validate_program_configuration(program, after)
    event = TransitionEvent(
        configuration,
        old,
        proposal.assignment,
        after,
        proposal.witness,
    )
    return StepResult((after,), Advanced(after != configuration), event)


def verify_transition_event(program: object, event: object) -> bool:
    if type(program) is not ReversalAddProgram or type(event) is not TransitionEvent:
        return False
    try:
        validate_program_configuration(program, event.before)
        expected = evaluate_closed_rule(program, event.before)
        after = apply_scalar_assignment(event.before, expected.assignment)
        validate_program_configuration(program, after)
        return event == TransitionEvent(
            event.before,
            event.before.value,
            expected.assignment,
            after,
            expected.witness,
        )
    except (TypeError, ValueError, ArithmeticError):
        return False


@dataclass(frozen=True)
class ScalarTrace:
    provenance: ProgramProvenance
    requested_horizon: int
    states: tuple[ScalarConfiguration, ...]
    events: tuple[TransitionEvent, ...]

    def __post_init__(self) -> None:
        if type(self.provenance) is not ProgramProvenance:
            raise TypeError("trace provenance must be exact ProgramProvenance")
        horizon = checked_horizon(self.requested_horizon)
        states = exact_tuple(self.states, "trace states")
        events = exact_tuple(self.events, "trace events")
        if len(states) != horizon + 1 or len(events) != horizon:
            raise ValueError("trace shape must be h events and h+1 states")
        if not states or any(type(state) is not ScalarConfiguration for state in states):
            raise TypeError("trace states must be exact ScalarConfiguration values")
        if any(type(event) is not TransitionEvent for event in events):
            raise TypeError("trace events must be exact TransitionEvent values")
        for index, event in enumerate(events):
            if event.before != states[index] or event.after != states[index + 1]:
                raise ValueError("trace event continuity is broken")
        object.__setattr__(self, "requested_horizon", horizon)
        object.__setattr__(self, "states", states)
        object.__setattr__(self, "events", events)


def run(program: object, seed: object, horizon: object) -> ScalarTrace:
    if type(program) is not ReversalAddProgram:
        raise TypeError("program must be exact ReversalAddProgram")
    if type(seed) is not ScalarConfiguration:
        raise TypeError("seed must be exact ScalarConfiguration")
    count = checked_horizon(horizon)
    validate_program_configuration(program, seed)
    states = [seed]
    events: list[TransitionEvent] = []
    for _ in range(count):
        result = advance(program, states[-1])
        states.append(result.successors[0])
        events.append(result.event)
    return ScalarTrace(program_provenance(program), count, tuple(states), tuple(events))


def verify_trace_provenance(program: object, trace: object) -> bool:
    if type(program) is not ReversalAddProgram or type(trace) is not ScalarTrace:
        return False
    if trace.provenance != program_provenance(program):
        return False
    if (
        len(trace.states) != trace.requested_horizon + 1
        or len(trace.events) != trace.requested_horizon
        or not trace.states
    ):
        return False
    try:
        validate_program_configuration(program, trace.states[0])
    except (TypeError, ValueError):
        return False
    for index, event in enumerate(trace.events):
        if event.before != trace.states[index] or event.after != trace.states[index + 1]:
            return False
        if not verify_transition_event(program, event):
            return False
    return True


def canonical_program(base: int = 2) -> ReversalAddProgram:
    """Native/default canonical profile over nonnegative exact integers."""

    return ReversalAddProgram(NONNEGATIVE, base, CanonicalDigits())


def positive_canonical_program(base: int = 2) -> ReversalAddProgram:
    """Named positive-only restriction of the native canonical profile."""

    return ReversalAddProgram(POSITIVE, base, CanonicalDigits())


def fixed_program(base: int, width: int) -> ReversalAddProgram:
    return ReversalAddProgram(NONNEGATIVE, base, FixedWidthDropCarry(width))


def grow_program(base: int) -> ReversalAddProgram:
    return ReversalAddProgram(WIDTH_TAGGED, base, GrowWidth())


COMPUTED_SEED16_PREFIX = (
    16,
    17,
    34,
    51,
    102,
    153,
    306,
    459,
    882,
    1197,
    2646,
    4347,
    11484,
    15273,
    24864,
    25443,
    50886,
    76329,
    152274,
    229371,
    458742,
)


COMPUTED_SEED512_PREFIX = (
    512,
    513,
    1026,
    1539,
    3078,
    4617,
    9234,
    13851,
    27702,
    41553,
    76950,
    130815,
    261630,
    392445,
    784122,
    1175031,
    3138792,
    3518181,
    6261840,
    6595917,
    12449760,
)


COMPUTED_SEED16_ENDPOINT_180 = 3987197239207620088799663177286543360
COMPUTED_SEED16_TRACE_SHA = "3a6be7627a2e42a8f5f1b94e30d0ca7894bd3361ff9c187d3f124e8962db52ec"
COMPUTED_SEED512_TRACE_SHA = "397c4cf26c075bc45a2a864b88322b99ec7af0fc773c5644174892328b8e9c5a"


FIXED_REVERSAL_CSV_DIGESTS = {
    (2, 7): "6bb5ed6569fb273a047c617ea21976c1bbf1c526241a3ce30d3a6b4025c11a9f",
    (2, 10): "cf22bf5df4813c70ebc731f2ff530fa0a4a2682a63c5735b05c1cf1e88dceaf3",
    (3, 6): "1d257ba2c08d032fcd0620417b75fe4b5c5df3909ca5c13608067017f7d9b707",
}


def integer_trace_values(trace: ScalarTrace) -> tuple[int, ...]:
    values: list[int] = []
    for state in trace.states:
        if type(state.value) is not int:
            raise ValueError("trace does not contain plain integer values")
        values.append(state.value)
    return tuple(values)


def trace_decimal_digest(trace: ScalarTrace) -> str:
    payload = "\n".join(map(str, integer_trace_values(trace))).encode("ascii")
    return sha256(payload).hexdigest()


def must_raise(error: type[BaseException], operation: object) -> int:
    if not callable(operation):
        raise TypeError("operation must be callable")
    try:
        operation()
    except error:
        return 1
    except Exception as caught:
        raise AssertionError(
            f"expected {error.__name__}, got {type(caught).__name__}"
        ) from caught
    raise AssertionError(f"expected {error.__name__}")


def audit_source_traces() -> tuple[int, int, int, int, int, int]:
    program = canonical_program()
    seed16 = run(program, ScalarConfiguration(NONNEGATIVE, 16), 180)
    values16 = integer_trace_values(seed16)
    assert values16[: len(COMPUTED_SEED16_PREFIX)] == COMPUTED_SEED16_PREFIX
    assert values16[-1] == COMPUTED_SEED16_ENDPOINT_180
    assert values16[-1].bit_length() == 122
    assert trace_decimal_digest(seed16) == COMPUTED_SEED16_TRACE_SHA
    assert verify_trace_provenance(program, seed16)

    seed512 = run(program, ScalarConfiguration(NONNEGATIVE, 512), 1000)
    values512 = integer_trace_values(seed512)
    assert values512[: len(COMPUTED_SEED512_PREFIX)] == COMPUTED_SEED512_PREFIX
    assert values512[-1].bit_length() == 627
    assert trace_decimal_digest(seed512) == COMPUTED_SEED512_TRACE_SHA
    assert verify_trace_provenance(program, seed512)

    growth_checks = 0
    direct_source_replays = 0
    for trace, values in ((seed16, values16), (seed512, values512)):
        assert all(value > 0 for value in values)
        assert all(right > left for left, right in zip(values, values[1:]))
        for index in range(len(values) - 2):
            assert values[index + 2].bit_length() >= values[index].bit_length() + 1
            growth_checks += 1
        for event in trace.events:
            direct = evaluate_word_rule(program, event.before)
            assert direct.assignment == event.assignment
            assert direct.witness == event.witness
            direct_source_replays += 1
    assert direct_source_replays == len(seed16.events) + len(seed512.events)
    return (
        len(seed16.events),
        len(seed512.events),
        len(seed16.states) + len(seed512.states),
        direct_source_replays,
        growth_checks,
        values512[-1].bit_length(),
    )


def assert_scalar_word_commutes(
    program: ReversalAddProgram,
    configuration: ScalarConfiguration,
) -> int:
    generic = evaluate_closed_rule(program, configuration)
    direct = evaluate_word_rule(program, configuration)
    assert generic == direct
    result = advance(program, configuration)
    assert result.event.assignment == generic.assignment
    assert result.event.witness == generic.witness
    assert verify_transition_event(program, result.event)

    digits = generic.witness.digits
    full = add_digit_words_full(digits, tuple(reversed(digits)), program.base)
    after = result.successors[0]
    if type(program.profile) is CanonicalDigits:
        assert type(after.value) is int
        assert encode_canonical(after.value, program.base) == trim_leading_zeros(full, program.base)
    elif type(program.profile) is FixedWidthDropCarry:
        assert type(after.value) is int
        assert encode_fixed(after.value, program.base, program.profile.width) == full[1:]
        assert generic.witness.dropped_carry == full[0]
    else:
        assert type(after.value) is WidthTaggedInteger
        assert encode_fixed(after.value.value, program.base, after.value.width) == full
    return 1


def audit_scalar_word_commutations() -> tuple[int, int, int, int]:
    canonical_checks = 0
    for base in range(2, 13):
        program = canonical_program(base)
        for value in range(0, 1025):
            canonical_checks += assert_scalar_word_commutes(
                program,
                ScalarConfiguration(NONNEGATIVE, value),
            )

    fixed_checks = 0
    for base, width in ((2, 4), (2, 7), (2, 10), (3, 6), (5, 5)):
        program = fixed_program(base, width)
        for value in range(base ** width):
            fixed_checks += assert_scalar_word_commutes(
                program,
                ScalarConfiguration(NONNEGATIVE, value),
            )

    grow_checks = 0
    for base in range(2, 9):
        program = grow_program(base)
        for width in range(1, 7):
            for value in range(min(base ** width, 257)):
                grow_checks += assert_scalar_word_commutes(
                    program,
                    ScalarConfiguration(WIDTH_TAGGED, WidthTaggedInteger(value, width)),
                )
    total = canonical_checks + fixed_checks + grow_checks
    return canonical_checks, fixed_checks, grow_checks, total


def audit_fixed_reversal_tables() -> tuple[int, int, int, int]:
    entries = 0
    involutions = 0
    digests = 0
    permutation_profiles = 0
    for (base, width), expected_digest in FIXED_REVERSAL_CSV_DIGESTS.items():
        table = reversal_table(base, width)
        size = base ** width
        assert len(table) == size
        assert set(table) == set(range(size))
        permutation_profiles += 1
        for value, reversed_value in enumerate(table):
            assert table[reversed_value] == value
            involutions += 1
        actual_digest = sha256(",".join(map(str, table)).encode("ascii")).hexdigest()
        assert actual_digest == expected_digest
        digests += 1
        entries += size
    assert reversal_table(2, 2)[2] == 1
    assert reversal_table(2, 2)[1] == 2
    assert decode_digits(tuple(reversed(encode_canonical(2, 2))), 2) == 1
    assert decode_digits(tuple(reversed(encode_canonical(1, 2))), 2) == 1
    return entries, involutions, digests, permutation_profiles


def audit_width_and_leading_zero_boundaries() -> tuple[int, int, int, int, int, int, int]:
    checks = 0

    canonical_two = advance(
        canonical_program(2),
        ScalarConfiguration(NONNEGATIVE, 2),
    )
    assert canonical_two.successors == (ScalarConfiguration(NONNEGATIVE, 3),)
    assert canonical_two.event.witness.digits == (1, 0)
    assert canonical_two.event.witness.reversed_digits == (0, 1)
    checks += 1

    fixed_two = advance(fixed_program(2, 4), ScalarConfiguration(NONNEGATIVE, 2))
    assert fixed_two.successors == (ScalarConfiguration(NONNEGATIVE, 6),)
    assert fixed_two.event.witness.digits == (0, 0, 1, 0)
    assert fixed_two.event.witness.reversed_digits == (0, 1, 0, 0)
    checks += 1

    grow_two = run(
        grow_program(2),
        ScalarConfiguration(WIDTH_TAGGED, WidthTaggedInteger(2, 4)),
        2,
    )
    assert grow_two.states == (
        ScalarConfiguration(WIDTH_TAGGED, WidthTaggedInteger(2, 4)),
        ScalarConfiguration(WIDTH_TAGGED, WidthTaggedInteger(6, 5)),
        ScalarConfiguration(WIDTH_TAGGED, WidthTaggedInteger(18, 6)),
    )
    checks += 1

    power = advance(canonical_program(2), ScalarConfiguration(NONNEGATIVE, 16))
    assert power.successors == (ScalarConfiguration(NONNEGATIVE, 17),)
    assert power.event.witness.reversed_digits == (0, 0, 0, 0, 1)
    checks += 1

    carry = advance(fixed_program(2, 4), ScalarConfiguration(NONNEGATIVE, 15))
    assert carry.successors == (ScalarConfiguration(NONNEGATIVE, 14),)
    assert carry.event.witness.untruncated_sum == 30
    assert carry.event.witness.dropped_carry == 1
    checks += 1

    default_program = canonical_program()
    assert default_program == ReversalAddProgram(NONNEGATIVE, 2, CanonicalDigits())
    canonical_zero = advance(default_program, ScalarConfiguration(NONNEGATIVE, 0))
    fixed_zero = advance(fixed_program(2, 4), ScalarConfiguration(NONNEGATIVE, 0))
    grow_zero = run(
        grow_program(2),
        ScalarConfiguration(WIDTH_TAGGED, WidthTaggedInteger(0, 4)),
        3,
    )
    assert canonical_zero.successors == (ScalarConfiguration(NONNEGATIVE, 0),)
    assert canonical_zero.outcome.changed is False
    assert canonical_zero.event.before == canonical_zero.event.after
    assert verify_transition_event(default_program, canonical_zero.event)
    assert fixed_zero.outcome.changed is False
    assert tuple(state.value for state in grow_zero.states) == (
        WidthTaggedInteger(0, 4),
        WidthTaggedInteger(0, 5),
        WidthTaggedInteger(0, 6),
        WidthTaggedInteger(0, 7),
    )
    assert all(event.before != event.after for event in grow_zero.events)
    assert all(
        event.witness.digits == (0,) * event.witness.old_width
        for event in grow_zero.events
        if event.witness.old_width is not None
    )
    zero_fixed_point_events = 1

    narrow_seed = ScalarConfiguration(WIDTH_TAGGED, WidthTaggedInteger(1, 1))
    padded_seed = ScalarConfiguration(WIDTH_TAGGED, WidthTaggedInteger(1, 2))
    assert narrow_seed.value.value == padded_seed.value.value == 1
    narrow_result = advance(grow_program(2), narrow_seed)
    padded_result = advance(grow_program(2), padded_seed)
    assert narrow_result.successors == (
        ScalarConfiguration(WIDTH_TAGGED, WidthTaggedInteger(2, 2)),
    )
    assert padded_result.successors == (
        ScalarConfiguration(WIDTH_TAGGED, WidthTaggedInteger(3, 3)),
    )
    assert encode_fixed(2, 2, 2) == (1, 0)
    assert encode_fixed(3, 2, 3) == (0, 1, 1)
    assert narrow_result.event.witness.digits == (1,)
    assert padded_result.event.witness.digits == (0, 1)
    assert narrow_result.successors[0] != padded_result.successors[0]
    width_loss_counterexample_pairs = 1
    width_loss_witness_states = 2

    fixed_cycle = run(
        fixed_program(2, 4),
        ScalarConfiguration(NONNEGATIVE, 15),
        9,
    )
    assert integer_trace_values(fixed_cycle) == (15, 14, 5, 15, 14, 5, 15, 14, 5, 15)
    assert len(fixed_cycle.events) == 9 and len(fixed_cycle.states) == 10
    continuing_cycle_events = len(fixed_cycle.events)
    return (
        checks,
        width_loss_counterexample_pairs,
        width_loss_witness_states,
        zero_fixed_point_events,
        len(grow_zero.events),
        continuing_cycle_events,
        3,
    )


def audit_arbitrary_precision() -> tuple[int, int, int, int]:
    cases = (
        (positive_canonical_program(2), ScalarConfiguration(POSITIVE, 2**4096), 2**4096 + 1),
        (
            positive_canonical_program(2),
            ScalarConfiguration(POSITIVE, 2**4096 + 1),
            2**4097 + 2,
        ),
        (
            positive_canonical_program(10),
            ScalarConfiguration(POSITIVE, 10**2000),
            10**2000 + 1,
        ),
        (
            fixed_program(2, 4097),
            ScalarConfiguration(NONNEGATIVE, 2**4096),
            2**4096 + 1,
        ),
        (
            grow_program(2),
            ScalarConfiguration(WIDTH_TAGGED, WidthTaggedInteger(2**4096, 4097)),
            WidthTaggedInteger(2**4096 + 1, 4098),
        ),
    )
    checks = 0
    max_bits = 0
    max_decimal_digits = 0
    word_commutations = 0
    for program, seed, expected in cases:
        result = advance(program, seed)
        assert result.successors[0].value == expected
        assert evaluate_closed_rule(program, seed) == evaluate_word_rule(program, seed)
        assert verify_transition_event(program, result.event)
        numeric = expected if type(expected) is int else expected.value
        max_bits = max(max_bits, numeric.bit_length())
        max_decimal_digits = max(max_decimal_digits, len(str(numeric)))
        checks += 1
        word_commutations += 1
    return checks, max_bits, max_decimal_digits, word_commutations


def audit_trace_shape_and_outcomes() -> tuple[int, int, int, int, int]:
    profiles = (
        (canonical_program(2), ScalarConfiguration(NONNEGATIVE, 16)),
        (
            canonical_program(10),
            ScalarConfiguration(NONNEGATIVE, 0),
        ),
        (fixed_program(2, 4), ScalarConfiguration(NONNEGATIVE, 15)),
        (
            grow_program(2),
            ScalarConfiguration(WIDTH_TAGGED, WidthTaggedInteger(0, 4)),
        ),
    )
    horizon_checks = 0
    total_events = 0
    total_states = 0
    changed_false = 0
    event_replays = 0
    for program, seed in profiles:
        for horizon in range(0, 65):
            trace = run(program, seed, horizon)
            assert len(trace.events) == horizon
            assert len(trace.states) == horizon + 1
            assert verify_trace_provenance(program, trace)
            horizon_checks += 1
            total_events += len(trace.events)
            total_states += len(trace.states)
            event_replays += len(trace.events)
            changed_false += sum(event.before == event.after for event in trace.events)
    assert changed_false > 0
    return horizon_checks, total_events, total_states, changed_false, event_replays


def audit_structural_identity_and_replay() -> tuple[int, int, int, int, int, int]:
    programs = (
        positive_canonical_program(2),
        canonical_program(2),
        positive_canonical_program(10),
        fixed_program(2, 4),
        fixed_program(2, 5),
        grow_program(2),
        grow_program(3),
    )
    keys = {structural_program_key(program) for program in programs}
    ids = {structural_program_id(program) for program in programs}
    assert len(keys) == len(programs)
    assert len(ids) == len(programs)

    source = positive_canonical_program(2)
    event = advance(source, ScalarConfiguration(POSITIVE, 16)).event
    assert verify_transition_event(source, event)
    cross_program_rejections = 0
    for other in (
        positive_canonical_program(10),
        canonical_program(2),
    ):
        assert not verify_transition_event(other, event)
        cross_program_rejections += 1
    fixed_event = advance(fixed_program(2, 4), ScalarConfiguration(NONNEGATIVE, 2)).event
    assert not verify_transition_event(fixed_program(2, 5), fixed_event)
    cross_program_rejections += 1

    zero_left = run(
        canonical_program(2),
        ScalarConfiguration(NONNEGATIVE, 0),
        0,
    )
    zero_right = run(
        canonical_program(10),
        ScalarConfiguration(NONNEGATIVE, 0),
        0,
    )
    assert zero_left.states == zero_right.states
    assert zero_left.events == zero_right.events == ()
    assert zero_left.provenance != zero_right.provenance
    assert not verify_trace_provenance(canonical_program(10), zero_left)
    assert not verify_trace_provenance(canonical_program(2), zero_right)
    zero_horizon_rejections = 2

    key_roundtrips = 0
    for program in programs:
        key = structural_program_key(program)
        assert checked_program_key(key) == key
        assert program_provenance(program).key == key
        key_roundtrips += 1
    return (
        len(keys),
        len(ids),
        key_roundtrips,
        cross_program_rejections,
        zero_horizon_rejections,
        len(programs),
    )


EXPECTED_DATACLASS_ROLE_MANIFEST = (
    ("Advanced", ("changed",)),
    ("CanonicalDigits", ()),
    ("FixedWidthDropCarry", ("width",)),
    ("GrowWidth", ()),
    ("ProgramProvenance", ("key", "display_id")),
    ("ProposedScalarWrite", ("assignment", "witness")),
    ("ReversalAddProgram", ("carrier", "base", "profile")),
    (
        "ReversalWitness",
        (
            "old_value",
            "old_width",
            "digits",
            "reversed_digits",
            "addend",
            "untruncated_sum",
            "dropped_carry",
            "new_value",
            "new_width",
            "provenance",
        ),
    ),
    ("ScalarAssignment", ("locus", "value")),
    ("ScalarConfiguration", ("carrier", "value")),
    ("ScalarTrace", ("provenance", "requested_horizon", "states", "events")),
    ("StepResult", ("successors", "outcome", "event")),
    ("TransitionEvent", ("before", "read_value", "assignment", "after", "witness")),
    ("WidthTaggedInteger", ("value", "width")),
)


SHARED_EXECUTION_ROLE_MANIFEST = (
    ("FRONTIER.select", "select_unique_scalar"),
    ("NEIGHBORHOOD.read", "read_self"),
    ("RULE.evaluate", "evaluate_closed_rule"),
    ("RULE.direct_word_oracle", "evaluate_word_rule"),
    ("UPDATE.apply", "apply_scalar_assignment"),
    ("STEP", "advance"),
    ("RUN", "run"),
)


FORBIDDEN_EXECUTION_ROLE_SUFFIXES = (
    "Control",
    "Executor",
    "Frontier",
    "Neighborhood",
    "Runner",
    "Schedule",
    "State",
    "Update",
)


def module_dataclass_role_manifest(namespace: object) -> tuple[tuple[str, tuple[str, ...]], ...]:
    if type(namespace) is not dict:
        raise TypeError("namespace must be an exact dict")
    manifest = []
    module_name = exact_str(namespace.get("__name__"), "module name")
    for name, value in namespace.items():
        if (
            type(name) is str
            and type(value) is type
            and value.__module__ == module_name
            and is_dataclass(value)
        ):
            manifest.append((name, tuple(field.name for field in fields(value))))
    return tuple(sorted(manifest))


def forbidden_execution_role_symbols(
    namespace: object,
) -> tuple[tuple[str, tuple[str, ...]], ...]:
    if type(namespace) is not dict:
        raise TypeError("namespace must be an exact dict")
    return tuple(
        (
            suffix,
            tuple(sorted(
                name
                for name in namespace
                if type(name) is str and name.endswith(suffix)
            )),
        )
        for suffix in FORBIDDEN_EXECUTION_ROLE_SUFFIXES
    )


def audit_no_new_execution_surface() -> tuple[int, int, int, int, int, int, int, int, int]:
    actual_dataclasses = module_dataclass_role_manifest(globals())
    assert actual_dataclasses == EXPECTED_DATACLASS_ROLE_MANIFEST
    manifest_by_name = dict(actual_dataclasses)
    state_fields = manifest_by_name["ScalarConfiguration"]
    assignment_fields = manifest_by_name["ScalarAssignment"]
    program_fields = manifest_by_name["ReversalAddProgram"]
    tagged_value_fields = manifest_by_name["WidthTaggedInteger"]
    step_result_fields = manifest_by_name["StepResult"]
    assert state_fields == ("carrier", "value")
    assert assignment_fields == ("locus", "value")
    assert program_fields == ("carrier", "base", "profile")
    assert tagged_value_fields == ("value", "width")
    assert step_result_fields == ("successors", "outcome", "event")
    forbidden = {"history", "time", "control", "callback", "digits"}
    assert not (forbidden & set(state_fields))
    assert not (forbidden & set(assignment_fields))
    assert not (forbidden & set(program_fields))
    for _role, symbol in SHARED_EXECUTION_ROLE_MANIFEST:
        assert symbol in globals() and callable(globals()[symbol])
    forbidden_symbols = forbidden_execution_role_symbols(globals())
    assert tuple(names for _suffix, names in forbidden_symbols) == ((),) * len(
        FORBIDDEN_EXECUTION_ROLE_SUFFIXES
    )
    seed = ScalarConfiguration(NONNEGATIVE, 16)
    assert select_unique_scalar(seed) == (SCALAR_LOCUS,)
    assert read_self(seed, SCALAR_LOCUS) == 16
    forbidden_by_suffix = dict(forbidden_symbols)
    frontier_fields = len(forbidden_by_suffix["Frontier"])
    neighborhood_fields = len(forbidden_by_suffix["Neighborhood"])
    update_fields = len(forbidden_by_suffix["Update"])
    executor_fields = len(forbidden_by_suffix["Executor"])
    return (
        len(state_fields),
        len(assignment_fields),
        frontier_fields,
        neighborhood_fields,
        update_fields,
        executor_fields,
        len(step_result_fields),
        len(tagged_value_fields),
        len(actual_dataclasses),
    )


def audit_hostile_validation() -> int:
    rejected = 0
    rejected += must_raise(TypeError, lambda: checked_base(True))
    rejected += must_raise(TypeError, lambda: checked_base(2.0))
    rejected += must_raise(TypeError, lambda: checked_base("2"))
    rejected += must_raise(ValueError, lambda: checked_base(1))
    rejected += must_raise(ValueError, lambda: checked_base(0))
    rejected += must_raise(TypeError, lambda: checked_width(True))
    rejected += must_raise(TypeError, lambda: checked_width(4.0))
    rejected += must_raise(ValueError, lambda: checked_width(0))
    rejected += must_raise(ValueError, lambda: checked_width(-1))
    rejected += must_raise(TypeError, lambda: checked_horizon(True))
    rejected += must_raise(TypeError, lambda: checked_horizon(1.0))
    rejected += must_raise(ValueError, lambda: checked_horizon(-1))

    rejected += must_raise(TypeError, lambda: ScalarConfiguration(POSITIVE, True))
    rejected += must_raise(TypeError, lambda: ScalarConfiguration(POSITIVE, 1.0))
    rejected += must_raise(TypeError, lambda: ScalarConfiguration(POSITIVE, "1"))
    rejected += must_raise(ValueError, lambda: ScalarConfiguration(POSITIVE, 0))
    rejected += must_raise(ValueError, lambda: ScalarConfiguration(POSITIVE, -1))
    rejected += must_raise(ValueError, lambda: ScalarConfiguration(NONNEGATIVE, -1))
    rejected += must_raise(TypeError, lambda: ScalarConfiguration(WIDTH_TAGGED, 1))
    rejected += must_raise(ValueError, lambda: ScalarConfiguration("integer", 1))
    rejected += must_raise(TypeError, lambda: WidthTaggedInteger(True, 2))
    rejected += must_raise(TypeError, lambda: WidthTaggedInteger(1, False))
    rejected += must_raise(ValueError, lambda: WidthTaggedInteger(-1, 2))
    rejected += must_raise(ValueError, lambda: WidthTaggedInteger(1, 0))

    rejected += must_raise(
        TypeError,
        lambda: ReversalAddProgram(POSITIVE, 2, lambda digits: tuple(reversed(digits))),
    )
    rejected += must_raise(
        ValueError,
        lambda: ReversalAddProgram(WIDTH_TAGGED, 2, CanonicalDigits()),
    )
    rejected += must_raise(
        ValueError,
        lambda: ReversalAddProgram(POSITIVE, 2, FixedWidthDropCarry(4)),
    )
    rejected += must_raise(
        ValueError,
        lambda: ReversalAddProgram(NONNEGATIVE, 2, GrowWidth()),
    )
    rejected += must_raise(TypeError, lambda: ReversalAddProgram(POSITIVE, True, CanonicalDigits()))

    rejected += must_raise(TypeError, lambda: encode_canonical(True, 2))
    rejected += must_raise(ValueError, lambda: encode_canonical(-1, 2))
    rejected += must_raise(ValueError, lambda: encode_fixed(16, 2, 4))
    rejected += must_raise(TypeError, lambda: encode_fixed(1, 2, True))
    rejected += must_raise(TypeError, lambda: decode_digits([1, 0], 2))
    rejected += must_raise(ValueError, lambda: decode_digits((), 2))
    rejected += must_raise(TypeError, lambda: decode_digits((1, True), 2))
    rejected += must_raise(ValueError, lambda: decode_digits((1, 2), 2))
    rejected += must_raise(ValueError, lambda: decode_digits((1, -1), 2))
    rejected += must_raise(ValueError, lambda: add_digit_words_full((1,), (1, 0), 2))

    rejected += must_raise(ValueError, lambda: ScalarAssignment("head", 1))
    rejected += must_raise(TypeError, lambda: ScalarAssignment(SCALAR_LOCUS, True))
    rejected += must_raise(
        ValueError,
        lambda: validate_program_configuration(
            fixed_program(2, 4),
            ScalarConfiguration(NONNEGATIVE, 16),
        ),
    )
    rejected += must_raise(
        ValueError,
        lambda: validate_program_configuration(
            grow_program(2),
            ScalarConfiguration(WIDTH_TAGGED, WidthTaggedInteger(16, 4)),
        ),
    )
    rejected += must_raise(
        ValueError,
        lambda: validate_program_configuration(
            positive_canonical_program(2),
            ScalarConfiguration(NONNEGATIVE, 1),
        ),
    )
    rejected += must_raise(TypeError, lambda: evaluate_closed_rule(lambda n: n, ScalarConfiguration(POSITIVE, 1)))
    rejected += must_raise(TypeError, lambda: advance(canonical_program(), 1))
    rejected += must_raise(TypeError, lambda: run(canonical_program(), 1, 3))

    valid_program = positive_canonical_program(2)
    valid_result = advance(valid_program, ScalarConfiguration(POSITIVE, 16))
    valid_event = valid_result.event
    rejected += must_raise(
        ValueError,
        lambda: TransitionEvent(
            valid_event.before,
            17,
            valid_event.assignment,
            valid_event.after,
            valid_event.witness,
        ),
    )
    rejected += must_raise(
        ValueError,
        lambda: TransitionEvent(
            valid_event.before,
            valid_event.read_value,
            ScalarAssignment(SCALAR_LOCUS, 18),
            valid_event.after,
            valid_event.witness,
        ),
    )
    rejected += must_raise(
        ValueError,
        lambda: StepResult(
            valid_result.successors,
            Advanced(False),
            valid_event,
        ),
    )
    rejected += must_raise(
        ValueError,
        lambda: StepResult((), Advanced(True), valid_event),
    )
    rejected += must_raise(
        ValueError,
        lambda: ScalarTrace(
            program_provenance(valid_program),
            2,
            (valid_event.before, valid_event.after),
            (valid_event,),
        ),
    )

    witness = valid_event.witness
    forged_digits = replace(witness, digits=(1, 1, 1, 1, 1), reversed_digits=(1, 1, 1, 1, 1))
    forged_event = TransitionEvent(
        valid_event.before,
        valid_event.read_value,
        valid_event.assignment,
        valid_event.after,
        forged_digits,
    )
    assert not verify_transition_event(valid_program, forged_event)
    rejected += 1
    forged_witness_trace = ScalarTrace(
        program_provenance(valid_program),
        1,
        (forged_event.before, forged_event.after),
        (forged_event,),
    )
    assert not verify_trace_provenance(valid_program, forged_witness_trace)
    rejected += 1

    valid_two_event_trace = run(
        valid_program,
        ScalarConfiguration(POSITIVE, 16),
        2,
    )
    rejected += must_raise(
        ValueError,
        lambda: ScalarTrace(
            valid_two_event_trace.provenance,
            2,
            (
                valid_two_event_trace.states[0],
                valid_two_event_trace.states[2],
                valid_two_event_trace.states[2],
            ),
            valid_two_event_trace.events,
        ),
    )

    unsafe_discontinuous_trace = object.__new__(ScalarTrace)
    object.__setattr__(
        unsafe_discontinuous_trace,
        "provenance",
        valid_two_event_trace.provenance,
    )
    object.__setattr__(unsafe_discontinuous_trace, "requested_horizon", 2)
    object.__setattr__(
        unsafe_discontinuous_trace,
        "states",
        (
            valid_two_event_trace.states[0],
            valid_two_event_trace.states[2],
            valid_two_event_trace.states[2],
        ),
    )
    object.__setattr__(
        unsafe_discontinuous_trace,
        "events",
        valid_two_event_trace.events,
    )
    assert not verify_trace_provenance(valid_program, unsafe_discontinuous_trace)
    rejected += 1
    forged_addend = replace(
        witness,
        addend=witness.addend + 1,
        untruncated_sum=witness.untruncated_sum + 1,
    )
    forged_event = TransitionEvent(
        valid_event.before,
        valid_event.read_value,
        valid_event.assignment,
        valid_event.after,
        forged_addend,
    )
    assert not verify_transition_event(valid_program, forged_event)
    rejected += 1

    other_program = positive_canonical_program(10)
    other_provenance = program_provenance(other_program)
    forged_provenance = replace(witness, provenance=other_provenance)
    forged_event = TransitionEvent(
        valid_event.before,
        valid_event.read_value,
        valid_event.assignment,
        valid_event.after,
        forged_provenance,
    )
    assert not verify_transition_event(valid_program, forged_event)
    rejected += 1

    key = structural_program_key(valid_program)
    rejected += must_raise(
        ValueError,
        lambda: ProgramProvenance(key, "0" * 64),
    )
    rejected += must_raise(
        TypeError,
        lambda: ProgramProvenance([*key], structural_program_id(valid_program)),
    )
    rejected += must_raise(
        TypeError,
        lambda: checked_program_key(("ReversalAddProgram/v1", POSITIVE, True, ("CanonicalDigits/v1",))),
    )
    rejected += must_raise(
        ValueError,
        lambda: checked_program_key(("ReversalAddProgram/v1", POSITIVE, 2, ("Callback/v1",))),
    )

    fixed = fixed_program(2, 4)
    fixed_event = advance(fixed, ScalarConfiguration(NONNEGATIVE, 15)).event
    forged_carry_witness = replace(fixed_event.witness, dropped_carry=0)
    forged_carry_event = TransitionEvent(
        fixed_event.before,
        fixed_event.read_value,
        fixed_event.assignment,
        fixed_event.after,
        forged_carry_witness,
    )
    assert not verify_transition_event(fixed, forged_carry_event)
    rejected += 1

    grow = grow_program(2)
    grow_event = advance(
        grow,
        ScalarConfiguration(WIDTH_TAGGED, WidthTaggedInteger(0, 4)),
    ).event
    forged_width_witness = replace(grow_event.witness, new_width=6)
    rejected += must_raise(
        ValueError,
        lambda: TransitionEvent(
            grow_event.before,
            grow_event.read_value,
            grow_event.assignment,
            grow_event.after,
            forged_width_witness,
        ),
    )

    # Concrete mutation sentinels for the most tempting lossy implementations.
    assert int(str(16)[::-1]) + 16 == 77  # decimal-string reversal is not binary reversal
    assert advance(valid_program, ScalarConfiguration(POSITIVE, 16)).successors[0].value == 17
    rejected += 1
    assert decode_digits(tuple(reversed(encode_canonical(2, 2))), 2) + 2 == 3
    assert advance(fixed_program(2, 4), ScalarConfiguration(NONNEGATIVE, 2)).successors[0].value == 6
    rejected += 1
    assert advance(grow_program(2), ScalarConfiguration(WIDTH_TAGGED, WidthTaggedInteger(2, 4))).successors[0].value == WidthTaggedInteger(6, 5)
    assert decode_digits(tuple(reversed(encode_fixed(2, 2, 5))), 2) + 2 == 10
    rejected += 1
    mutated_namespace = dict(globals())
    mutated_namespace["DigitReversalExecutor"] = object()
    mutated_roles = dict(forbidden_execution_role_symbols(mutated_namespace))
    assert mutated_roles["Executor"] == ("DigitReversalExecutor",)
    rejected += 1
    return rejected


EXPECTED_DIGEST = "30539868a2202ffdae0e4574e0ceefb68e5715d6d3a7a543efd63bd730a5ccc8"


def collect_audit_summary() -> tuple[tuple[str, object], ...]:
    source_metrics = audit_source_traces()
    commutation_metrics = audit_scalar_word_commutations()
    table_metrics = audit_fixed_reversal_tables()
    width_metrics = audit_width_and_leading_zero_boundaries()
    bigint_metrics = audit_arbitrary_precision()
    trace_metrics = audit_trace_shape_and_outcomes()
    identity_metrics = audit_structural_identity_and_replay()
    surface_metrics = audit_no_new_execution_surface()
    hostile_rejections = audit_hostile_validation()

    return (
        ("source", source_metrics),
        ("commutations", commutation_metrics),
        ("fixed_tables", table_metrics),
        ("width_boundaries", width_metrics),
        ("arbitrary_precision", bigint_metrics),
        ("trace_shape", trace_metrics),
        ("structural_identity", identity_metrics),
        ("execution_surface", surface_metrics),
        ("hostile_rejections", hostile_rejections),
        ("source_claims", SOURCE_CLAIMS),
        ("architecture_classes", ARCHITECTURE_CLASSIFICATION),
        ("goal2_delta", GOAL2_DELTA),
        ("dataclass_role_manifest", EXPECTED_DATACLASS_ROLE_MANIFEST),
        ("shared_execution_roles", SHARED_EXECUTION_ROLE_MANIFEST),
        ("forbidden_execution_suffixes", FORBIDDEN_EXECUTION_ROLE_SUFFIXES),
    )


def main() -> None:
    summary = collect_audit_summary()
    digest = sha256(repr(summary).encode("utf-8")).hexdigest()
    assert digest == EXPECTED_DIGEST
    metrics = dict(summary)
    source_metrics = metrics["source"]
    commutation_metrics = metrics["commutations"]
    table_metrics = metrics["fixed_tables"]
    width_metrics = metrics["width_boundaries"]
    bigint_metrics = metrics["arbitrary_precision"]
    trace_metrics = metrics["trace_shape"]
    identity_metrics = metrics["structural_identity"]
    surface_metrics = metrics["execution_surface"]
    hostile_rejections = metrics["hostile_rejections"]

    print(
        "source_events="
        f"{source_metrics[0] + source_metrics[1]}; "
        f"source_event_replays={source_metrics[3]}; "
        f"growth_checks={source_metrics[4]}; seed512_bits={source_metrics[5]}"
    )
    print(
        "scalar_word_commutations="
        f"{commutation_metrics[3]} "
        f"({commutation_metrics[0]}/{commutation_metrics[1]}/{commutation_metrics[2]}); "
        f"fixed_relation_entries={table_metrics[0]}"
    )
    print(
        "bigint_cases="
        f"{bigint_metrics[0]}; max_bits={bigint_metrics[1]}; "
        f"max_decimal_digits={bigint_metrics[2]}; "
        f"width_loss_counterexample_pairs={width_metrics[1]}; "
        f"width_loss_witness_states={width_metrics[2]}; "
        f"zero_fixed_events={width_metrics[3]}"
    )
    print(
        "trace_horizons="
        f"{trace_metrics[0]}; trace_events={trace_metrics[1]}; "
        f"event_replays={trace_metrics[4]}; changed_false={trace_metrics[3]}"
    )
    print(
        "structural_keys="
        f"{identity_metrics[0]}; cross_rejections={identity_metrics[3]}; "
        f"hostile_rejections={hostile_rejections}"
    )
    print(
        "surface="
        f"state{surface_metrics[0]}/assignment{surface_metrics[1]}/"
        f"frontier{surface_metrics[2]}/neighborhood{surface_metrics[3]}/"
        f"update{surface_metrics[4]}/executor{surface_metrics[5]}/"
        f"StepResult{surface_metrics[6]}/tagged_value{surface_metrics[7]}/"
        f"dataclasses{surface_metrics[8]}"
    )
    print(f"semantic_digest={digest}")


if __name__ == "__main__":
    main()
