"""Closed semantic value schemas and their composition.

The Goal 7 target layer in this module owns exact value validity, semantic
equality, represented-number profiles, and scalar or structural schema
composition. It does not own carrier support, topology, scheduling, program
families, or transition behavior. Seeds and Rules declare values against these
schemas; ``program.py`` performs cross-field and successor validation.

The target ``Alphabet(descriptor=...)`` contract replaces the current finite
recipe record only during the atomic G7-01 cutover. Until then, non-colliding
target declarations remain inert above the complete 0.1 catalog.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any, NoReturn


# ---------------------------------------------------------------------------
# Goal 7 Phase 1.1: Singular Value-Schema Primitives
# ---------------------------------------------------------------------------


class AlphabetPrimitive(Enum):
    """Closed schema primitives fixed by the Goal 7 reference scaffold."""

    ENUM = "alphabet.enum"
    PRODUCT = "alphabet.product"


def _not_implemented() -> NoReturn:
    """Raise the standard error for an unfinished Goal 7 alphabet factory."""

    raise NotImplementedError("Goal 7 alphabet scaffold is not implemented")


# The target frozen ``Alphabet`` stores one closed descriptor. Its live class
# declaration cannot coexist truthfully with the incompatible 0.1 class below.


# ---------------------------------------------------------------------------
# Goal 7 Phase 1.2: Compound Value Schemas
# ---------------------------------------------------------------------------


def product(parts: tuple["Alphabet", ...]) -> "Alphabet":
    """Compose named schema parts without flattening semantic distinctions."""

    _not_implemented()


# ---------------------------------------------------------------------------
# Goal 7 Phase 2: General Exact and Structural Families
# ---------------------------------------------------------------------------

# Exact numeric, tag, union, record, word, map, graph, field, instruction,
# pattern, equation, distribution, and represented-number schemas enter here
# after their closed descriptors and equality laws are fixed.


# ---------------------------------------------------------------------------
# Goal 7 Phase 3: Presets and Aliases
# ---------------------------------------------------------------------------

# Presets delegate to singular or compound schemas and introduce no new value
# semantics.


# ===========================================================================
# Legacy 0.1 implementation retained until atomic G7-01 cutover
# ===========================================================================


Value = int | float | str


@dataclass(frozen=True)
class Alphabet:
    """Finite set of raw trajectory values.

    `values` stores the legal cell values in deterministic order. `family` and
    `params` preserve the catalog recipe that produced the alphabet so configs
    can be compared, deduplicated, and rebuilt without relying on hard-coded
    constants.
    """

    values: tuple[Value, ...]
    family: str
    params: Mapping[str, Any]
    name: str | None = None


def int_range_alphabet(size: int, start: int = 0) -> Alphabet:
    """Build a contiguous integer alphabet.

    This is the default family for scalar numerical recurrences and other
    numeric value spaces. `int_range_alphabet(size=97)` represents values
    `{0, ..., 96}`.

    This family should be preferred over named constants whenever a simple
    finite integer range is the semantic value space.
    """

    if isinstance(size, bool) or not isinstance(size, int):
        raise TypeError(f"size must be an integer, got {type(size).__name__}")

    if isinstance(start, bool) or not isinstance(start, int):
        raise TypeError(f"start must be an integer, got {type(start).__name__}")

    if size <= 0:
        raise ValueError(f"size must be positive, got {size}")

    values = tuple(range(start, start + size))

    return Alphabet(
        values=values,
        family="int_range_alphabet",
        params={"size": size, "start": start},
    )


def float_range_alphabet(size: int, start: float = 0.0, step: float = 1.0) -> Alphabet:
    """Build a finite evenly spaced float-valued alphabet.

    This is for discretized real scalar values, not continuous intervals.
    `float_range_alphabet(size=5, start=0.0, step=0.25)` represents
    `{0.0, 0.25, 0.5, 0.75, 1.0}`.
    """

    if isinstance(size, bool) or not isinstance(size, int):
        raise TypeError(f"size must be an integer, got {type(size).__name__}")

    if isinstance(start, bool) or not isinstance(start, (int, float)):
        raise TypeError(f"start must be an int or float, got {type(start).__name__}")

    if isinstance(step, bool) or not isinstance(step, (int, float)):
        raise TypeError(f"step must be an int or float, got {type(step).__name__}")

    if size <= 0:
        raise ValueError(f"size must be positive, got {size}")

    start = float(start)
    step = float(step)

    if not math.isfinite(start):
        raise ValueError(f"start must be finite, got {start}")

    if not math.isfinite(step):
        raise ValueError(f"step must be finite, got {step}")

    if step == 0.0:
        raise ValueError("step cannot be zero")

    values = tuple(start + index * step for index in range(size))

    return Alphabet(
        values=values,
        family="float_range_alphabet",
        params={"size": size, "start": start, "step": step},
    )


def boolean() -> Alphabet:
    """Build the canonical two-state boolean alphabet.

    The raw values are still `0` and `1`, but the family records that these are
    boolean off/on states rather than scalar numerical values. Downstream
    representation can therefore treat boolean states consistently without
    merging them with numeric range alphabets that happen to contain the same
    integers.
    """

    return Alphabet(
        values=(0, 1),
        family="boolean",
        params={},
    )


def symbolic(values: Sequence[int | str]) -> Alphabet:
    """Build an alphabet from explicit symbolic values.

    This is reserved for non-numeric or semantically named cell states. Values
    should remain finite, deterministic, and directly representable.
    """

    values = tuple(values)

    if not values:
        raise ValueError("values cannot be empty")

    seen = set()
    for value in values:
        if isinstance(value, bool):
            raise TypeError("symbolic values must be int or str, not bool")

        if not isinstance(value, (int, str)):
            raise TypeError(
                f"symbolic values must be int or str, got {type(value).__name__}"
            )

        if value in seen:
            raise ValueError(f"symbolic values must be unique, duplicate {value!r}")

        seen.add(value)

    return Alphabet(
        values=values,
        family="symbolic",
        params={"values": values},
    )
