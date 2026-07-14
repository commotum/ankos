#!/usr/bin/env python3
"""Dependency-free semantic audit for T22 Moore-neighborhood cellular automata.

This is Goal 1 evidence, not runtime code.  It compares a literal row/column
reference implementation with a dimension-generic SimpleProgram-shaped route:

    active = FRONTIER.select(configuration)
    reads  = NEIGHBORHOOD.read(configuration, active)
    writes = RULE(active, reads)
    next   = UPDATE.apply(configuration, active, writes)

The strict read is an explicit composition of SelfAccess and all eight Moore
offsets.  Native square-lattice support, finite realizations, coordinate-frame
adapters, and views remain separate.  Compact 18-case outer-totalistic and
10-case equal-sum tables are schema-tagged representations of qualifying
512-context maps, never executor modes.  The source's broader finite-k,
dimension-d profile is separately represented by a complete table indexed as
``Self + k*FullTotal`` with exactly
``k*((3**d - 1)*(k - 1) + 1)`` entries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product
from math import comb, prod
from typing import Protocol


if not __debug__:
    raise RuntimeError("T22 semantic verification requires assertions; do not run with -O")


Coord = tuple[int, ...]
Offset = tuple[int, ...]
Cells = tuple[int, ...]

BOOK_NINE_POSITIONS: tuple[Offset, ...] = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 0),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)
MOORE_OFFSETS: tuple[Offset, ...] = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)
CARDINAL_2D: tuple[Offset, ...] = ((-1, 0), (0, -1), (0, 1), (1, 0))


def require_int(value: object, name: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{name} must be an exact int")
    return value


def require_tuple(value: object, name: str) -> tuple[object, ...]:
    if type(value) is not tuple:
        raise TypeError(f"{name} must be an exact tuple")
    return value


def checked_coord(value: object, dimension: int, name: str = "coordinate") -> Coord:
    raw = require_tuple(value, name)
    if len(raw) != dimension:
        raise ValueError(f"{name} has the wrong dimension")
    return tuple(require_int(item, f"{name} component") for item in raw)


def add_coord(left: Coord, right: Offset) -> Coord:
    if len(left) != len(right):
        raise ValueError("coordinate dimensions differ")
    return tuple(a + b for a, b in zip(left, right, strict=True))


def subtract_coord(left: Coord, right: Offset) -> Coord:
    if len(left) != len(right):
        raise ValueError("coordinate dimensions differ")
    return tuple(a - b for a, b in zip(left, right, strict=True))


@dataclass(frozen=True)
class FiniteAlphabet:
    size: int

    def __post_init__(self) -> None:
        size = require_int(self.size, "alphabet size")
        if size < 2:
            raise ValueError("alphabet size must be at least two")

    def check(self, value: object, name: str = "cell value") -> int:
        checked = require_int(value, name)
        if checked < 0 or checked >= self.size:
            raise ValueError(f"{name} is outside the alphabet")
        return checked


@dataclass(frozen=True)
class PeriodicBoundary:
    """Finite quotient realization."""


@dataclass(frozen=True)
class FixedBoundary:
    value: int

    def __post_init__(self) -> None:
        require_int(self.value, "fixed boundary value")


Boundary = PeriodicBoundary | FixedBoundary


@dataclass(frozen=True)
class FiniteGrid:
    shape: tuple[int, ...]
    boundary: Boundary

    def __post_init__(self) -> None:
        raw = require_tuple(self.shape, "grid shape")
        if not raw:
            raise ValueError("grid dimension must be positive")
        checked = tuple(require_int(item, "shape extent") for item in raw)
        if any(item <= 0 for item in checked):
            raise ValueError("shape extents must be positive")
        if type(self.boundary) not in (PeriodicBoundary, FixedBoundary):
            raise TypeError("unsupported boundary")

    @property
    def dimension(self) -> int:
        return len(self.shape)

    @property
    def size(self) -> int:
        return prod(self.shape)


@dataclass(frozen=True, eq=False)
class SnapshotToken:
    generation: int

    def __post_init__(self) -> None:
        generation = require_int(self.generation, "generation")
        if generation < 0:
            raise ValueError("generation must be nonnegative")


def all_coords(shape: tuple[int, ...]) -> tuple[Coord, ...]:
    return tuple(product(*(range(extent) for extent in shape)))


def flat_index(shape: tuple[int, ...], coord: Coord) -> int:
    if len(shape) != len(coord):
        raise ValueError("coordinate has the wrong dimension")
    result = 0
    for extent, component in zip(shape, coord, strict=True):
        if component < 0 or component >= extent:
            raise ValueError("coordinate is outside the finite grid")
        result = result * extent + component
    return result


@dataclass(frozen=True)
class GridConfiguration:
    alphabet: FiniteAlphabet
    topology: FiniteGrid
    cells: Cells
    snapshot_token: SnapshotToken = field(compare=False, repr=False)

    def __post_init__(self) -> None:
        if type(self.alphabet) is not FiniteAlphabet:
            raise TypeError("alphabet must be FiniteAlphabet")
        if type(self.topology) is not FiniteGrid:
            raise TypeError("topology must be FiniteGrid")
        raw = require_tuple(self.cells, "cells")
        if len(raw) != self.topology.size:
            raise ValueError("cell count does not match shape")
        for value in raw:
            self.alphabet.check(value)
        if type(self.topology.boundary) is FixedBoundary:
            self.alphabet.check(self.topology.boundary.value, "fixed boundary value")
        if type(self.snapshot_token) is not SnapshotToken:
            raise TypeError("snapshot token must be exact SnapshotToken")

    @property
    def generation(self) -> int:
        return self.snapshot_token.generation

    def value_at(self, raw_coord: object) -> int:
        coord = checked_coord(raw_coord, self.topology.dimension)
        if type(self.topology.boundary) is PeriodicBoundary:
            resolved = tuple(
                component % extent
                for component, extent in zip(coord, self.topology.shape, strict=True)
            )
            return self.cells[flat_index(self.topology.shape, resolved)]
        assert type(self.topology.boundary) is FixedBoundary
        if any(
            component < 0 or component >= extent
            for component, extent in zip(coord, self.topology.shape, strict=True)
        ):
            return self.topology.boundary.value
        return self.cells[flat_index(self.topology.shape, coord)]


@dataclass(frozen=True)
class SelfAccess:
    """Declared access to the firing locus."""


@dataclass(frozen=True)
class OffsetAccess:
    offset: Offset

    def __post_init__(self) -> None:
        raw = require_tuple(self.offset, "offset")
        if not raw:
            raise ValueError("offset dimension must be positive")
        checked = tuple(require_int(item, "offset component") for item in raw)
        if all(item == 0 for item in checked):
            raise ValueError("zero displacement must be SelfAccess")


AccessComponent = SelfAccess | OffsetAccess


@dataclass(frozen=True)
class LocalAccess:
    components: tuple[AccessComponent, ...]

    def __post_init__(self) -> None:
        raw = require_tuple(self.components, "access components")
        if sum(type(component) is SelfAccess for component in raw) != 1:
            raise ValueError("local access must declare Self exactly once")
        offsets: list[Offset] = []
        dimension: int | None = None
        for component in raw:
            if type(component) is SelfAccess:
                continue
            if type(component) is not OffsetAccess:
                raise TypeError("unsupported access component")
            if dimension is None:
                dimension = len(component.offset)
            if len(component.offset) != dimension:
                raise ValueError("offset dimensions differ")
            offsets.append(component.offset)
        if dimension is None or not offsets:
            raise ValueError("spatial access needs at least one offset")
        if len(set(offsets)) != len(offsets):
            raise ValueError("offsets must be unique")

    @property
    def self_position(self) -> int:
        return next(
            index
            for index, component in enumerate(self.components)
            if type(component) is SelfAccess
        )

    @property
    def offsets(self) -> tuple[Offset, ...]:
        return tuple(
            component.offset
            for component in self.components
            if type(component) is OffsetAccess
        )

    @property
    def dimension(self) -> int:
        return len(self.offsets[0])

    @property
    def slots(self) -> int:
        return len(self.offsets)


def make_access(offsets: tuple[Offset, ...], self_position: int) -> LocalAccess:
    raw = require_tuple(offsets, "offsets")
    position = require_int(self_position, "Self position")
    if position < 0 or position > len(raw):
        raise ValueError("Self position is outside the schema")
    components: list[AccessComponent] = [OffsetAccess(offset) for offset in raw]
    components.insert(position, SelfAccess())
    return LocalAccess(tuple(components))


@dataclass(frozen=True)
class LocalRead:
    center: int
    neighbors: tuple[int, ...]

    def __post_init__(self) -> None:
        require_int(self.center, "center value")
        raw = require_tuple(self.neighbors, "neighbor values")
        for value in raw:
            require_int(value, "neighbor value")


def validate_read(read: LocalRead, alphabet_size: int, slots: int) -> None:
    if type(read) is not LocalRead:
        raise TypeError("rule input must be LocalRead")
    alphabet = FiniteAlphabet(alphabet_size)
    alphabet.check(read.center, "center value")
    if len(read.neighbors) != slots:
        raise ValueError("wrong neighbor arity")
    for value in read.neighbors:
        alphabet.check(value, "neighbor value")


class LocalRule(Protocol):
    alphabet_size: int
    neighbor_slots: int

    def evaluate(self, read: LocalRead) -> int: ...


@dataclass(frozen=True)
class BinaryOuterTotalistic:
    """Binary output indexed by 2*surrounding-count + Self."""

    code: int
    neighbor_slots: int
    alphabet_size: int = field(default=2, init=False)

    def __post_init__(self) -> None:
        code = require_int(self.code, "outer-totalistic code")
        slots = require_int(self.neighbor_slots, "neighbor slots")
        if slots <= 0:
            raise ValueError("neighbor slots must be positive")
        if code < 0 or code >= 1 << (2 * (slots + 1)):
            raise ValueError("outer-totalistic code is out of range")

    def evaluate(self, read: LocalRead) -> int:
        validate_read(read, 2, self.neighbor_slots)
        index = 2 * sum(read.neighbors) + read.center
        return (self.code >> index) & 1


@dataclass(frozen=True)
class BinaryTotalistic:
    """Binary output indexed by Self plus all surrounding values."""

    code: int
    neighbor_slots: int
    alphabet_size: int = field(default=2, init=False)

    def __post_init__(self) -> None:
        code = require_int(self.code, "totalistic code")
        slots = require_int(self.neighbor_slots, "neighbor slots")
        if slots <= 0:
            raise ValueError("neighbor slots must be positive")
        if code < 0 or code >= 1 << (slots + 2):
            raise ValueError("totalistic code is out of range")

    def evaluate(self, read: LocalRead) -> int:
        validate_read(read, 2, self.neighbor_slots)
        return (self.code >> (read.center + sum(read.neighbors))) & 1


@dataclass(frozen=True)
class LabelEquals:
    """Closed typed predicate descriptor, never an executor callback."""

    label: int

    def __post_init__(self) -> None:
        label = require_int(self.label, "predicate label")
        if label < 0:
            raise ValueError("predicate label must be nonnegative")

    def matches(self, value: int) -> bool:
        return require_int(value, "predicate input") == self.label


@dataclass(frozen=True)
class PredicateCountLookup:
    """Output table indexed by (Self, count(neighbor satisfying predicate))."""

    alphabet_size: int
    neighbor_slots: int
    predicate: LabelEquals
    outputs: tuple[tuple[int, ...], ...]

    def __post_init__(self) -> None:
        alphabet = FiniteAlphabet(self.alphabet_size)
        slots = require_int(self.neighbor_slots, "predicate-count neighbor slots")
        if slots <= 0:
            raise ValueError("predicate-count neighbor slots must be positive")
        if type(self.predicate) is not LabelEquals:
            raise TypeError("predicate must be a closed LabelEquals descriptor")
        alphabet.check(self.predicate.label, "predicate label")
        raw_outputs = require_tuple(self.outputs, "predicate-count outputs")
        if len(raw_outputs) != alphabet.size:
            raise ValueError("predicate-count table has the wrong Self arity")
        for raw_row in raw_outputs:
            row = require_tuple(raw_row, "predicate-count output row")
            if len(row) != slots + 1:
                raise ValueError("predicate-count output row is incomplete")
            for output in row:
                alphabet.check(output, "predicate-count output")

    def evaluate(self, read: LocalRead) -> int:
        validate_read(read, self.alphabet_size, self.neighbor_slots)
        match_count = sum(self.predicate.matches(value) for value in read.neighbors)
        return self.outputs[read.center][match_count]


def full_total_product_case_count(dimension: int, alphabet_size: int) -> int:
    """BOOK:13475-13481 count for Self + k*FullTotal profiles."""

    checked_dimension = require_int(dimension, "profile dimension")
    if checked_dimension <= 0:
        raise ValueError("profile dimension must be positive")
    alphabet = FiniteAlphabet(alphabet_size)
    surrounding_slots = 3**checked_dimension - 1
    full_total_values = surrounding_slots * (alphabet.size - 1) + 1
    return alphabet.size * full_total_values


@dataclass(frozen=True)
class FullTotalProduct:
    """Finite-k table indexed by Self + k*sum(surrounding values).

    This is the source's dimension/alphabet generalization of the compact
    Moore profile.  It is deliberately not the strict binary T22 code type.
    """

    dimension: int
    alphabet_size: int
    outputs: tuple[int, ...]
    neighbor_slots: int = field(init=False)

    def __post_init__(self) -> None:
        dimension = require_int(self.dimension, "profile dimension")
        if dimension <= 0:
            raise ValueError("profile dimension must be positive")
        alphabet = FiniteAlphabet(self.alphabet_size)
        slots = 3**dimension - 1
        raw = require_tuple(self.outputs, "full-total product outputs")
        expected = alphabet.size * (slots * (alphabet.size - 1) + 1)
        if len(raw) != expected:
            raise ValueError("full-total product table is incomplete")
        for value in raw:
            alphabet.check(value, "full-total product output")
        object.__setattr__(self, "neighbor_slots", slots)

    def evaluate(self, read: LocalRead) -> int:
        validate_read(read, self.alphabet_size, self.neighbor_slots)
        index = read.center + self.alphabet_size * sum(read.neighbors)
        return self.outputs[index]


@dataclass(frozen=True)
class GeneralLookup:
    """Complete positional table over center followed by ordered offsets."""

    alphabet_size: int
    neighbor_slots: int
    outputs: tuple[int, ...]

    def __post_init__(self) -> None:
        alphabet = FiniteAlphabet(self.alphabet_size)
        slots = require_int(self.neighbor_slots, "neighbor slots")
        if slots <= 0:
            raise ValueError("neighbor slots must be positive")
        raw = require_tuple(self.outputs, "lookup outputs")
        if len(raw) != alphabet.size ** (slots + 1):
            raise ValueError("lookup table is incomplete")
        for value in raw:
            alphabet.check(value, "lookup output")

    def evaluate(self, read: LocalRead) -> int:
        validate_read(read, self.alphabet_size, self.neighbor_slots)
        index = 0
        for value in (read.center, *read.neighbors):
            index = index * self.alphabet_size + value
        return self.outputs[index]


Rule = (
    BinaryOuterTotalistic
    | BinaryTotalistic
    | PredicateCountLookup
    | FullTotalProduct
    | GeneralLookup
)

CASE_ZERO_IS_LEAST_SIGNIFICANT = "case-0-is-least-significant"


@dataclass(frozen=True)
class PrintedCodeProvenance:
    """Source spelling adapter; never a canonical rule identifier.

    Notes/T03 defines declared-width outputs by
    U_s = floor(printed / radix**s) mod radix, so case zero is the least
    significant digit.  The original spelling remains inspectable even when
    digits above the declared table width have no denotation.
    """

    printed: int
    radix: int
    width: int
    digit_direction: str

    def __post_init__(self) -> None:
        printed = require_int(self.printed, "printed code")
        radix = require_int(self.radix, "printed code radix")
        width = require_int(self.width, "printed code width")
        if printed < 0:
            raise ValueError("printed code must be nonnegative")
        if radix < 2:
            raise ValueError("printed code radix must be at least two")
        if width <= 0:
            raise ValueError("printed code width must be positive")
        if type(self.digit_direction) is not str:
            raise TypeError("digit direction must be an exact str")
        if self.digit_direction != CASE_ZERO_IS_LEAST_SIGNIFICANT:
            raise ValueError("unsupported printed-code digit direction")

    @property
    def canonical_table(self) -> tuple[int, ...]:
        return tuple(
            (self.printed // self.radix**case_index) % self.radix
            for case_index in range(self.width)
        )

    @property
    def canonical_code(self) -> int:
        return sum(
            output * self.radix**case_index
            for case_index, output in enumerate(self.canonical_table)
        )


def projection_rule(alphabet_size: int, slots: int, selected: int) -> GeneralLookup:
    alphabet = FiniteAlphabet(alphabet_size)
    count = require_int(slots, "neighbor slots")
    slot = require_int(selected, "selected slot")
    if count <= 0:
        raise ValueError("neighbor slots must be positive")
    if slot < -1 or slot >= count:
        raise ValueError("projection slot is out of range")
    context_index = 0 if slot == -1 else slot + 1
    outputs = tuple(
        context[context_index]
        for context in product(range(alphabet.size), repeat=count + 1)
    )
    return GeneralLookup(alphabet.size, count, outputs)


def wireworld_rule() -> PredicateCountLookup:
    """Source table with neighbor predicate label == electron-head label 1."""

    return PredicateCountLookup(
        alphabet_size=4,
        neighbor_slots=8,
        predicate=LabelEquals(1),
        outputs=(
            (0,) * 9,
            (2,) * 9,
            (3,) * 9,
            (3, 1, 1, 3, 3, 3, 3, 3, 3),
        ),
    )


def dyadaxes_2d_summary(read: LocalRead) -> tuple[int, bool, bool]:
    """Current lossy channels: Self and two strict-majority gate bits."""

    validate_read(read, 2, 8)
    cardinal_count = sum(
        value
        for offset, value in zip(MOORE_OFFSETS, read.neighbors, strict=True)
        if abs(offset[0]) + abs(offset[1]) == 1
    )
    diagonal_count = sum(
        value
        for offset, value in zip(MOORE_OFFSETS, read.neighbors, strict=True)
        if abs(offset[0]) + abs(offset[1]) == 2
    )
    return (read.center, cardinal_count > 2, diagonal_count > 2)


def book_nine_context(read: LocalRead) -> tuple[int, ...]:
    validate_read(read, 2, 8)
    return (
        read.neighbors[0],
        read.neighbors[1],
        read.neighbors[2],
        read.neighbors[3],
        read.center,
        read.neighbors[4],
        read.neighbors[5],
        read.neighbors[6],
        read.neighbors[7],
    )


def binary_index(bits: tuple[int, ...]) -> int:
    index = 0
    for bit in bits:
        if type(bit) is not int or bit not in (0, 1):
            raise TypeError("binary context must contain exact bits")
        index = 2 * index + bit
    return index


def strict_general_from_code(code: int) -> GeneralLookup:
    checked = require_int(code, "general nine-position code")
    if checked < 0 or checked >= 1 << 512:
        raise ValueError("general code is outside the 512-row schema")
    outputs: list[int] = []
    for context in product((0, 1), repeat=9):
        read = LocalRead(context[0], context[1:])
        outputs.append((checked >> binary_index(book_nine_context(read))) & 1)
    return GeneralLookup(2, 8, tuple(outputs))


def strict_general_to_code(table: GeneralLookup) -> int:
    if type(table) is not GeneralLookup:
        raise TypeError("general rule must be GeneralLookup")
    if table.alphabet_size != 2 or table.neighbor_slots != 8:
        raise ValueError("strict T22 table must have 512 binary contexts")
    code = 0
    for context in product((0, 1), repeat=9):
        read = LocalRead(context[0], context[1:])
        code |= table.evaluate(read) << binary_index(book_nine_context(read))
    return code


def book_position_projection(position: int, alphabet_size: int = 2) -> GeneralLookup:
    selected = require_int(position, "Book position")
    if selected < 0 or selected >= 9:
        raise ValueError("Book position is out of range")
    local_slot = -1 if selected == 4 else selected if selected < 4 else selected - 1
    return projection_rule(alphabet_size, 8, local_slot)


def expected_projection_hex() -> tuple[str, ...]:
    """Independent bit-pattern fixtures for nine big-endian context digits."""

    return (
        "f" * 64 + "0" * 64,
        ("f" * 32 + "0" * 32) * 2,
        ("f" * 16 + "0" * 16) * 4,
        ("f" * 8 + "0" * 8) * 8,
        ("f" * 4 + "0" * 4) * 16,
        ("ff" + "00") * 32,
        ("f" + "0") * 64,
        "c" * 128,
        "a" * 128,
    )


def square_position_permutation(
    quarter_turns: int, reflected: bool = False
) -> tuple[int, ...]:
    """Target-to-source permutation in canonical Book row/column order."""

    turns = require_int(quarter_turns, "quarter turns")
    if turns < 0 or turns >= 4:
        raise ValueError("quarter turns must be in range(4)")
    if type(reflected) is not bool:
        raise TypeError("reflected must be an exact bool")
    position_index = {
        position: index for index, position in enumerate(BOOK_NINE_POSITIONS)
    }
    permutation: list[int] = []
    for row, column in BOOK_NINE_POSITIONS:
        if reflected:
            column = -column
        for _ in range(turns):
            row, column = column, -row
        permutation.append(position_index[(row, column)])
    return tuple(permutation)


def c4_square_permutations() -> tuple[tuple[int, ...], ...]:
    return tuple(square_position_permutation(turns) for turns in range(4))


def d4_square_permutations() -> tuple[tuple[int, ...], ...]:
    return c4_square_permutations() + tuple(
        square_position_permutation(turns, reflected=True)
        for turns in range(4)
    )


def book_context_from_index(index: int) -> tuple[int, ...]:
    checked = require_int(index, "Book context index")
    if checked < 0 or checked >= 512:
        raise ValueError("Book context index is outside the nine-bit schema")
    return tuple((checked >> shift) & 1 for shift in range(8, -1, -1))


def permute_book_context_by_positions(
    context: tuple[int, ...], permutation: tuple[int, ...]
) -> tuple[int, ...]:
    raw_context = require_tuple(context, "Book context")
    if len(raw_context) != 9:
        raise ValueError("Book context must have nine positions")
    for value in raw_context:
        if type(value) is not int or value not in (0, 1):
            raise TypeError("Book context must contain exact bits")
    raw_permutation = require_tuple(permutation, "position permutation")
    if (
        len(raw_permutation) != 9
        or any(type(index) is not int for index in raw_permutation)
        or set(raw_permutation) != set(range(9))
    ):
        raise ValueError("position permutation must contain range(9) exactly")
    return tuple(raw_context[index] for index in raw_permutation)


def derive_book_context_orbits(
    permutations: tuple[tuple[int, ...], ...]
) -> tuple[tuple[int, ...], ...]:
    """Derive a partition of all 512 contexts from a finite group action."""

    raw = require_tuple(permutations, "symmetry permutations")
    if not raw:
        raise ValueError("symmetry group cannot be empty")
    seen: set[int] = set()
    result: list[tuple[int, ...]] = []
    for index in range(512):
        if index in seen:
            continue
        context = book_context_from_index(index)
        orbit = tuple(
            sorted(
                {
                    binary_index(
                        permute_book_context_by_positions(context, permutation)
                    )
                    for permutation in raw
                }
            )
        )
        if seen.intersection(orbit):
            raise ValueError("permutations do not induce disjoint complete orbits")
        seen.update(orbit)
        result.append(orbit)
    if seen != set(range(512)):
        raise AssertionError("symmetry orbits do not cover all contexts")
    return tuple(result)


def validate_context_orbits(orbits: tuple[tuple[int, ...], ...]) -> None:
    raw = require_tuple(orbits, "context orbits")
    if not raw:
        raise ValueError("context orbit partition cannot be empty")
    seen: set[int] = set()
    previous_minimum = -1
    for raw_orbit in raw:
        orbit = require_tuple(raw_orbit, "context orbit")
        if not orbit:
            raise ValueError("context orbit cannot be empty")
        if any(type(index) is not int for index in orbit):
            raise TypeError("context orbit indices must be exact ints")
        if tuple(sorted(orbit)) != orbit or len(set(orbit)) != len(orbit):
            raise ValueError("context orbit must be sorted and unique")
        if orbit[0] <= previous_minimum:
            raise ValueError("context orbits must use canonical minimum order")
        if orbit[0] < 0 or orbit[-1] >= 512 or seen.intersection(orbit):
            raise ValueError("context orbit partition overlaps or is out of range")
        seen.update(orbit)
        previous_minimum = orbit[0]
    if seen != set(range(512)):
        raise ValueError("context orbit partition must cover range(512)")


def expand_symmetry_restriction(
    outputs: tuple[int, ...], orbits: tuple[tuple[int, ...], ...]
) -> GeneralLookup:
    """Expand orbit outputs to the existing complete 512-context map."""

    validate_context_orbits(orbits)
    raw_outputs = require_tuple(outputs, "symmetry outputs")
    if len(raw_outputs) != len(orbits):
        raise ValueError("symmetry output table is incomplete")
    code = 0
    for output, orbit in zip(raw_outputs, orbits, strict=True):
        if type(output) is not int or output not in (0, 1):
            raise TypeError("symmetry output must be an exact bit")
        if output:
            for context_index in orbit:
                code |= 1 << context_index
    return strict_general_from_code(code)


def factor_symmetry_restriction(
    table: GeneralLookup, orbits: tuple[tuple[int, ...], ...]
) -> tuple[int, ...]:
    """Factor a complete map iff every symmetry orbit has one output."""

    if type(table) is not GeneralLookup:
        raise TypeError("symmetry factorization requires GeneralLookup")
    if table.alphabet_size != 2 or table.neighbor_slots != 8:
        raise ValueError("symmetry factorization requires a strict T22 table")
    validate_context_orbits(orbits)
    code = strict_general_to_code(table)
    outputs: list[int] = []
    for orbit in orbits:
        output = (code >> orbit[0]) & 1
        if any(((code >> index) & 1) != output for index in orbit[1:]):
            raise ValueError("complete map disagrees within a symmetry orbit")
        outputs.append(output)
    result = tuple(outputs)
    if expand_symmetry_restriction(result, orbits) != table:
        raise AssertionError("symmetry factorization lost information")
    return result


# Canonical identity is the orbit-output tuple ordered by least Book context.
# It intentionally has no integer codec.  A printed compact spelling needs a
# separate, source-bound adapter carrying radix, width, digit direction, and
# orbit order.  Notes code 3702 is handled by PrintedCodeProvenance and its
# declared-width normalization cannot redefine canonical table identity.


def expand_outer(rule: BinaryOuterTotalistic) -> GeneralLookup:
    if type(rule) is not BinaryOuterTotalistic or rule.neighbor_slots != 8:
        raise TypeError("strict T22 outer-totalistic rule required")
    return GeneralLookup(
        2,
        8,
        tuple(
            rule.evaluate(LocalRead(context[0], context[1:]))
            for context in product((0, 1), repeat=9)
        ),
    )


def factor_outer(table: GeneralLookup) -> BinaryOuterTotalistic:
    if type(table) is not GeneralLookup:
        raise TypeError("general rule must be GeneralLookup")
    if table.alphabet_size != 2 or table.neighbor_slots != 8:
        raise ValueError("strict T22 general table required")
    fibers: dict[tuple[int, int], int] = {}
    for context in product((0, 1), repeat=9):
        read = LocalRead(context[0], context[1:])
        key = (read.center, sum(read.neighbors))
        output = table.evaluate(read)
        prior = fibers.setdefault(key, output)
        if prior != output:
            raise ValueError("table is not Self x MooreCount constant")
    if len(fibers) != 18:
        raise AssertionError("outer-totalistic fibers are incomplete")
    code = sum(
        fibers[(center, count)] << (2 * count + center)
        for count in range(9)
        for center in (0, 1)
    )
    result = BinaryOuterTotalistic(code, 8)
    if expand_outer(result) != table:
        raise AssertionError("outer-totalistic factorization lost information")
    return result


def expand_totalistic(rule: BinaryTotalistic) -> GeneralLookup:
    if type(rule) is not BinaryTotalistic or rule.neighbor_slots != 8:
        raise TypeError("strict T22 totalistic rule required")
    return GeneralLookup(
        2,
        8,
        tuple(
            rule.evaluate(LocalRead(context[0], context[1:]))
            for context in product((0, 1), repeat=9)
        ),
    )


def factor_totalistic(table: GeneralLookup) -> BinaryTotalistic:
    if type(table) is not GeneralLookup:
        raise TypeError("general rule must be GeneralLookup")
    if table.alphabet_size != 2 or table.neighbor_slots != 8:
        raise ValueError("strict T22 general table required")
    fibers: dict[int, int] = {}
    for context in product((0, 1), repeat=9):
        read = LocalRead(context[0], context[1:])
        total = read.center + sum(read.neighbors)
        output = table.evaluate(read)
        prior = fibers.setdefault(total, output)
        if prior != output:
            raise ValueError("table is not equal-sum totalistic")
    if len(fibers) != 10:
        raise AssertionError("totalistic fibers are incomplete")
    code = sum(fibers[total] << total for total in range(10))
    result = BinaryTotalistic(code, 8)
    if expand_totalistic(result) != table:
        raise AssertionError("totalistic factorization lost information")
    return result


@dataclass(frozen=True)
class CAProgram:
    alphabet: FiniteAlphabet
    neighborhood: LocalAccess
    rule: Rule

    def __post_init__(self) -> None:
        if type(self.alphabet) is not FiniteAlphabet:
            raise TypeError("program alphabet must be FiniteAlphabet")
        if type(self.neighborhood) is not LocalAccess:
            raise TypeError("program neighborhood must be LocalAccess")
        if type(self.rule) not in (
            BinaryOuterTotalistic,
            BinaryTotalistic,
            PredicateCountLookup,
            FullTotalProduct,
            GeneralLookup,
        ):
            raise TypeError("unsupported closed rule schema")
        if self.alphabet.size != self.rule.alphabet_size:
            raise ValueError("rule and alphabet disagree")
        if self.neighborhood.slots != self.rule.neighbor_slots:
            raise ValueError("rule and neighborhood arities disagree")
        if (
            type(self.rule) is FullTotalProduct
            and self.neighborhood.dimension != self.rule.dimension
        ):
            raise ValueError("profile and neighborhood dimensions disagree")


def strict_t22_program(rule: Rule) -> CAProgram:
    return CAProgram(
        FiniteAlphabet(rule.alphabet_size),
        make_access(MOORE_OFFSETS, self_position=4),
        rule,
    )


@dataclass(frozen=True)
class SiteHandle:
    snapshot_token: SnapshotToken = field(repr=False)
    coord: Coord

    def __post_init__(self) -> None:
        if type(self.snapshot_token) is not SnapshotToken:
            raise TypeError("site handle needs an exact snapshot token")
        raw = require_tuple(self.coord, "site coordinate")
        for item in raw:
            require_int(item, "site coordinate component")


@dataclass(frozen=True)
class SiteAssignment:
    source: SiteHandle
    target: Coord
    value: int

    def __post_init__(self) -> None:
        if type(self.source) is not SiteHandle:
            raise TypeError("assignment source must be SiteHandle")
        raw = require_tuple(self.target, "assignment target")
        for item in raw:
            require_int(item, "target component")
        require_int(self.value, "assignment value")


def select_all_sites(old: GridConfiguration) -> tuple[SiteHandle, ...]:
    if type(old) is not GridConfiguration:
        raise TypeError("configuration must be GridConfiguration")
    return tuple(SiteHandle(old.snapshot_token, coord) for coord in all_coords(old.topology.shape))


def validate_handles(old: GridConfiguration, active: tuple[SiteHandle, ...]) -> None:
    raw = require_tuple(active, "active sites")
    seen: set[Coord] = set()
    for handle in raw:
        if type(handle) is not SiteHandle:
            raise TypeError("active item must be SiteHandle")
        if handle.snapshot_token is not old.snapshot_token:
            raise ValueError("stale or foreign site handle")
        coord = checked_coord(handle.coord, old.topology.dimension, "active coordinate")
        flat_index(old.topology.shape, coord)
        if coord in seen:
            raise ValueError("duplicate active site")
        seen.add(coord)


def read_local(
    old: GridConfiguration,
    active: tuple[SiteHandle, ...],
    neighborhood: LocalAccess,
) -> tuple[LocalRead, ...]:
    validate_handles(old, active)
    if type(neighborhood) is not LocalAccess:
        raise TypeError("neighborhood must be LocalAccess")
    if neighborhood.dimension != old.topology.dimension:
        raise ValueError("neighborhood and configuration dimensions differ")
    result: list[LocalRead] = []
    for handle in active:
        declared = tuple(
            old.value_at(handle.coord)
            if type(component) is SelfAccess
            else old.value_at(add_coord(handle.coord, component.offset))
            for component in neighborhood.components
        )
        center = declared[neighborhood.self_position]
        neighbors = tuple(
            value
            for component, value in zip(neighborhood.components, declared, strict=True)
            if type(component) is OffsetAccess
        )
        result.append(LocalRead(center, neighbors))
    return tuple(result)


def make_assignments(
    program: CAProgram,
    active: tuple[SiteHandle, ...],
    reads: tuple[LocalRead, ...],
) -> tuple[SiteAssignment, ...]:
    require_tuple(reads, "local reads")
    if len(active) != len(reads):
        raise ValueError("active/read cardinality mismatch")
    return tuple(
        SiteAssignment(handle, handle.coord, program.rule.evaluate(read))
        for handle, read in zip(active, reads, strict=True)
    )


def validate_plan(
    old: GridConfiguration,
    program: CAProgram,
    active: tuple[SiteHandle, ...],
    reads: tuple[LocalRead, ...],
    writes: tuple[SiteAssignment, ...],
) -> None:
    validate_handles(old, active)
    require_tuple(reads, "local reads")
    require_tuple(writes, "assignments")
    if len(active) != len(reads) or len(active) != len(writes):
        raise ValueError("plan cardinalities differ")
    if reads != read_local(old, active, program.neighborhood):
        raise ValueError("reads are not from the exact old snapshot")
    for handle, read, write in zip(active, reads, writes, strict=True):
        if type(write) is not SiteAssignment:
            raise TypeError("write must be SiteAssignment")
        if write.source != handle or write.target != handle.coord:
            raise ValueError("write source/target correspondence is invalid")
        old.alphabet.check(write.value, "assignment value")
        if write.value != program.rule.evaluate(read):
            raise ValueError("assignment does not match rule")


def apply_parallel(
    old: GridConfiguration,
    active: tuple[SiteHandle, ...],
    writes: tuple[SiteAssignment, ...],
) -> GridConfiguration:
    validate_handles(old, active)
    require_tuple(writes, "assignments")
    if len(active) != len(writes):
        raise ValueError("active/write cardinality mismatch")
    next_cells = list(old.cells)
    targets: set[Coord] = set()
    for handle, write in zip(active, writes, strict=True):
        if type(write) is not SiteAssignment:
            raise TypeError("write must be SiteAssignment")
        if write.source != handle or write.source.snapshot_token is not old.snapshot_token:
            raise ValueError("stale, foreign, or reordered write")
        target = checked_coord(write.target, old.topology.dimension, "target")
        if target != handle.coord:
            raise ValueError("CA assignments must be same-site")
        if target in targets:
            raise ValueError("duplicate assignment target")
        targets.add(target)
        next_cells[flat_index(old.topology.shape, target)] = old.alphabet.check(write.value)
    return GridConfiguration(
        old.alphabet,
        old.topology,
        tuple(next_cells),
        SnapshotToken(old.generation + 1),
    )


def generic_step(program: CAProgram, old: GridConfiguration) -> GridConfiguration:
    if type(program) is not CAProgram or type(old) is not GridConfiguration:
        raise TypeError("generic step needs exact program and configuration")
    if program.alphabet != old.alphabet:
        raise ValueError("program and configuration alphabets differ")
    if program.neighborhood.dimension != old.topology.dimension:
        raise ValueError("program and configuration dimensions differ")
    active = select_all_sites(old)
    reads = read_local(old, active, program.neighborhood)
    writes = make_assignments(program, active, reads)
    validate_plan(old, program, active, reads, writes)
    successor = apply_parallel(old, active, writes)
    if len(active) != old.topology.size:
        raise AssertionError("AllSites was not exhaustive")
    return successor


@dataclass(frozen=True)
class Native2DState:
    """Independent row-major T22 reference carrier."""

    alphabet_size: int
    shape: tuple[int, int]
    boundary: Boundary
    cells: Cells

    def __post_init__(self) -> None:
        alphabet = FiniteAlphabet(self.alphabet_size)
        raw_shape = require_tuple(self.shape, "native shape")
        if len(raw_shape) != 2:
            raise ValueError("native state must be two-dimensional")
        rows, columns = (require_int(item, "native extent") for item in raw_shape)
        if rows <= 0 or columns <= 0:
            raise ValueError("native extents must be positive")
        if type(self.boundary) not in (PeriodicBoundary, FixedBoundary):
            raise TypeError("native boundary is unsupported")
        raw_cells = require_tuple(self.cells, "native cells")
        if len(raw_cells) != rows * columns:
            raise ValueError("native cell count does not match shape")
        for value in raw_cells:
            alphabet.check(value, "native cell")
        if type(self.boundary) is FixedBoundary:
            alphabet.check(self.boundary.value, "native boundary value")

    def value_at(self, row: int, column: int) -> int:
        row = require_int(row, "row")
        column = require_int(column, "column")
        rows, columns = self.shape
        if type(self.boundary) is PeriodicBoundary:
            row %= rows
            column %= columns
        elif row < 0 or row >= rows or column < 0 or column >= columns:
            assert type(self.boundary) is FixedBoundary
            return self.boundary.value
        return self.cells[row * columns + column]


def encode_native(state: Native2DState, generation: int = 0) -> GridConfiguration:
    if type(state) is not Native2DState:
        raise TypeError("native state must be Native2DState")
    return GridConfiguration(
        FiniteAlphabet(state.alphabet_size),
        FiniteGrid(state.shape, state.boundary),
        state.cells,
        SnapshotToken(generation),
    )


def decode_generic(state: GridConfiguration) -> Native2DState:
    if type(state) is not GridConfiguration or state.topology.dimension != 2:
        raise TypeError("generic state must be a 2D GridConfiguration")
    return Native2DState(
        state.alphabet.size,
        (state.topology.shape[0], state.topology.shape[1]),
        state.topology.boundary,
        state.cells,
    )


def native_book_context(
    old: Native2DState, row: int, column: int
) -> tuple[int, ...]:
    """Literal sorted row/column 3x3 order, including Self."""

    if type(old) is not Native2DState:
        raise TypeError("native state must be Native2DState")
    row = require_int(row, "row")
    column = require_int(column, "column")
    return tuple(
        old.value_at(row + drow, column + dcolumn)
        for drow, dcolumn in BOOK_NINE_POSITIONS
    )


def native_general_step(code: int, old: Native2DState) -> Native2DState:
    """Independent literal nine-bit numeric evaluator."""

    checked = require_int(code, "native general code")
    if checked < 0 or checked >= 1 << 512:
        raise ValueError("native general code is out of range")
    if old.alphabet_size != 2:
        raise ValueError("native general code requires binary cells")
    values: list[int] = []
    weights = (256, 128, 64, 32, 16, 8, 4, 2, 1)
    for row in range(old.shape[0]):
        for column in range(old.shape[1]):
            context = native_book_context(old, row, column)
            index = sum(weight * value for weight, value in zip(weights, context, strict=True))
            values.append((checked >> index) & 1)
    return Native2DState(2, old.shape, old.boundary, tuple(values))


def native_outer_step(code: int, old: Native2DState) -> Native2DState:
    """Independent direct Self+2*MooreCount evaluator."""

    checked = require_int(code, "native outer code")
    if checked < 0 or checked >= 1 << 18:
        raise ValueError("native outer code is out of range")
    if old.alphabet_size != 2:
        raise ValueError("native outer code requires binary cells")
    values: list[int] = []
    for row in range(old.shape[0]):
        for column in range(old.shape[1]):
            context = native_book_context(old, row, column)
            center = context[4]
            count = sum(context[:4]) + sum(context[5:])
            values.append((checked >> (2 * count + center)) & 1)
    return Native2DState(2, old.shape, old.boundary, tuple(values))


def native_totalistic_step(code: int, old: Native2DState) -> Native2DState:
    """Independent direct nine-value-sum evaluator."""

    checked = require_int(code, "native totalistic code")
    if checked < 0 or checked >= 1 << 10:
        raise ValueError("native totalistic code is out of range")
    if old.alphabet_size != 2:
        raise ValueError("native totalistic code requires binary cells")
    values = tuple(
        (checked >> sum(native_book_context(old, row, column))) & 1
        for row in range(old.shape[0])
        for column in range(old.shape[1])
    )
    return Native2DState(2, old.shape, old.boundary, values)


def native_full_total_product_step(
    outputs: tuple[int, ...], old: Native2DState
) -> Native2DState:
    """Independent literal 2D evaluator for Self + k*FullTotal."""

    raw = require_tuple(outputs, "native full-total product outputs")
    alphabet = FiniteAlphabet(old.alphabet_size)
    expected = alphabet.size * (8 * (alphabet.size - 1) + 1)
    if len(raw) != expected:
        raise ValueError("native full-total product table is incomplete")
    for value in raw:
        alphabet.check(value, "native full-total product output")
    values: list[int] = []
    for row in range(old.shape[0]):
        for column in range(old.shape[1]):
            context = native_book_context(old, row, column)
            center = context[4]
            full_total = sum(context[:4]) + sum(context[5:])
            values.append(raw[center + alphabet.size * full_total])
    return Native2DState(
        alphabet.size,
        old.shape,
        old.boundary,
        tuple(values),
    )


def native_wireworld_local(book_context: tuple[int, ...]) -> int:
    """Independent literal source transition over one raw Book context."""

    raw = require_tuple(book_context, "native WireWorld context")
    if len(raw) != 9:
        raise ValueError("native WireWorld context must have nine positions")
    for value in raw:
        if type(value) is not int:
            raise TypeError("native WireWorld context values must be exact ints")
        if value < 0 or value >= 4:
            raise ValueError("native WireWorld context value is outside range(4)")
    center = raw[4]
    head_count = sum(value == 1 for value in (*raw[:4], *raw[5:]))
    if center == 0:
        return 0
    if center == 1:
        return 2
    if center == 2:
        return 3
    assert center == 3
    return 1 if head_count in (1, 2) else 3


def native_wireworld_step(old: Native2DState) -> Native2DState:
    """Independent literal row-major WireWorld evaluator."""

    if type(old) is not Native2DState:
        raise TypeError("native WireWorld state must be Native2DState")
    if old.alphabet_size != 4:
        raise ValueError("native WireWorld requires four cell labels")
    values = tuple(
        native_wireworld_local(native_book_context(old, row, column))
        for row in range(old.shape[0])
        for column in range(old.shape[1])
    )
    return Native2DState(4, old.shape, old.boundary, values)


def native_projection_step(position: int, old: Native2DState) -> Native2DState:
    selected = require_int(position, "native Book position")
    if selected < 0 or selected >= 9:
        raise ValueError("native Book position is out of range")
    values = tuple(
        native_book_context(old, row, column)[selected]
        for row in range(old.shape[0])
        for column in range(old.shape[1])
    )
    return Native2DState(old.alphabet_size, old.shape, old.boundary, values)


def book_row_column_to_enu(raw_offset: object) -> Offset:
    row, column = checked_coord(raw_offset, 2, "Book row/column offset")
    return (column, -row)


def basis_permutations() -> tuple[
    tuple[Offset, ...], tuple[Offset, ...], tuple[int, ...], tuple[int, ...]
]:
    transformed = tuple(book_row_column_to_enu(offset) for offset in BOOK_NINE_POSITIONS)
    runtime_sorted = tuple(sorted(transformed))
    runtime_to_book = tuple(transformed.index(offset) for offset in runtime_sorted)
    book_to_runtime = tuple(runtime_sorted.index(offset) for offset in transformed)
    return transformed, runtime_sorted, runtime_to_book, book_to_runtime


def runtime_context_to_book(runtime_context: tuple[int, ...]) -> tuple[int, ...]:
    raw = require_tuple(runtime_context, "runtime context")
    if len(raw) != 9 or any(type(value) is not int or value not in (0, 1) for value in raw):
        raise TypeError("runtime context must be nine exact bits")
    _transformed, _runtime, _runtime_to_book, book_to_runtime = basis_permutations()
    return tuple(raw[index] for index in book_to_runtime)


def book_context_to_runtime(book_context: tuple[int, ...]) -> tuple[int, ...]:
    raw = require_tuple(book_context, "Book context")
    if len(raw) != 9 or any(type(value) is not int or value not in (0, 1) for value in raw):
        raise TypeError("Book context must be nine exact bits")
    _transformed, _runtime, runtime_to_book, _book_to_runtime = basis_permutations()
    return tuple(raw[index] for index in runtime_to_book)


def permute_book_code_to_runtime(code: int) -> int:
    checked = require_int(code, "Book general code")
    if checked < 0 or checked >= 1 << 512:
        raise ValueError("Book general code is out of range")
    runtime_code = 0
    for runtime_context in product((0, 1), repeat=9):
        book_context = runtime_context_to_book(runtime_context)
        runtime_code |= (
            ((checked >> binary_index(book_context)) & 1)
            << binary_index(runtime_context)
        )
    return runtime_code


def permute_runtime_code_to_book(code: int) -> int:
    checked = require_int(code, "runtime general code")
    if checked < 0 or checked >= 1 << 512:
        raise ValueError("runtime general code is out of range")
    book_code = 0
    for book_context in product((0, 1), repeat=9):
        runtime_context = book_context_to_runtime(book_context)
        book_code |= (
            ((checked >> binary_index(runtime_context)) & 1)
            << binary_index(book_context)
        )
    return book_code


def native_to_enu(state: Native2DState, generation: int = 0) -> GridConfiguration:
    if type(state) is not Native2DState:
        raise TypeError("native state must be Native2DState")
    generation = require_int(generation, "generation")
    rows, columns = state.shape
    runtime_shape = (columns, rows)
    values = [0] * (rows * columns)
    for row in range(rows):
        for column in range(columns):
            runtime_coord = (column, rows - 1 - row)
            values[flat_index(runtime_shape, runtime_coord)] = state.value_at(row, column)
    return GridConfiguration(
        FiniteAlphabet(state.alphabet_size),
        FiniteGrid(runtime_shape, state.boundary),
        tuple(values),
        SnapshotToken(generation),
    )


@dataclass(frozen=True)
class SparseField:
    """Complete Z^d field: visible uniform background plus finite deviations."""

    alphabet: FiniteAlphabet
    dimension: int
    background: int
    entries: tuple[tuple[Coord, int], ...]
    generation: int = 0

    def __post_init__(self) -> None:
        if type(self.alphabet) is not FiniteAlphabet:
            raise TypeError("sparse alphabet must be FiniteAlphabet")
        dimension = require_int(self.dimension, "sparse dimension")
        if dimension <= 0:
            raise ValueError("sparse dimension must be positive")
        self.alphabet.check(self.background, "sparse background")
        raw = require_tuple(self.entries, "sparse entries")
        previous: Coord | None = None
        seen: set[Coord] = set()
        for item in raw:
            entry = require_tuple(item, "sparse entry")
            if len(entry) != 2:
                raise ValueError("sparse entry must be (coord,value)")
            coord = checked_coord(entry[0], dimension, "sparse coordinate")
            value = self.alphabet.check(entry[1], "sparse value")
            if value == self.background:
                raise ValueError("sparse entry must differ from background")
            if coord in seen or (previous is not None and coord <= previous):
                raise ValueError("sparse entries must be unique and sorted")
            seen.add(coord)
            previous = coord
        generation = require_int(self.generation, "sparse generation")
        if generation < 0:
            raise ValueError("sparse generation must be nonnegative")

    def value_at(self, raw_coord: object) -> int:
        coord = checked_coord(raw_coord, self.dimension, "sparse coordinate")
        for stored, value in self.entries:
            if stored == coord:
                return value
        return self.background


def sparse_field(
    alphabet_size: int,
    dimension: int,
    background: int,
    entries: tuple[tuple[Coord, int], ...],
    generation: int = 0,
) -> SparseField:
    raw = require_tuple(entries, "sparse entries")
    return SparseField(
        FiniteAlphabet(alphabet_size),
        dimension,
        background,
        tuple(sorted(raw, key=lambda item: item[0])),
        generation,
    )


def sparse_read(program: CAProgram, state: SparseField, coord: Coord) -> LocalRead:
    if program.neighborhood.dimension != state.dimension:
        raise ValueError("sparse field and program dimensions differ")
    checked = checked_coord(coord, state.dimension)
    declared = tuple(
        state.value_at(checked)
        if type(component) is SelfAccess
        else state.value_at(add_coord(checked, component.offset))
        for component in program.neighborhood.components
    )
    return LocalRead(
        declared[program.neighborhood.self_position],
        tuple(
            value
            for component, value in zip(program.neighborhood.components, declared, strict=True)
            if type(component) is OffsetAccess
        ),
    )


def sparse_step(program: CAProgram, old: SparseField) -> SparseField:
    if program.alphabet != old.alphabet:
        raise ValueError("sparse field and program alphabets differ")
    if program.neighborhood.dimension != old.dimension:
        raise ValueError("sparse field and program dimensions differ")
    uniform = LocalRead(
        old.background,
        tuple(old.background for _ in program.neighborhood.offsets),
    )
    next_background = program.rule.evaluate(uniform)
    candidates: set[Coord] = set()
    for coord, _value in old.entries:
        candidates.add(coord)
        for offset in program.neighborhood.offsets:
            candidates.add(subtract_coord(coord, offset))
    next_entries = tuple(
        (coord, value)
        for coord in sorted(candidates)
        if (value := program.rule.evaluate(sparse_read(program, old, coord)))
        != next_background
    )
    return SparseField(
        old.alphabet,
        old.dimension,
        next_background,
        next_entries,
        old.generation + 1,
    )


def fixed_background_sparse_step(program: CAProgram, old: SparseField) -> SparseField:
    uniform = LocalRead(
        old.background,
        tuple(old.background for _ in program.neighborhood.offsets),
    )
    if program.rule.evaluate(uniform) != old.background:
        raise ValueError("fixed-background lowering requires quiescence proof")
    successor = sparse_step(program, old)
    if successor.background != old.background:
        raise AssertionError("proved fixed background changed")
    return successor


def expect_raises(error: type[BaseException], thunk: object) -> None:
    if not callable(thunk):
        raise TypeError("test thunk must be callable")
    try:
        thunk()
    except error:
        return
    except Exception as exc:
        raise AssertionError(
            f"expected {error.__name__}, got {type(exc).__name__}"
        ) from exc
    raise AssertionError(f"expected {error.__name__}")


def cells_with_one(shape: tuple[int, ...], coord: Coord, alphabet_size: int = 2) -> Cells:
    FiniteAlphabet(alphabet_size)
    values = [0] * prod(shape)
    values[flat_index(shape, coord)] = 1
    return tuple(values)


def nonzero_coords(state: GridConfiguration) -> tuple[Coord, ...]:
    return tuple(
        coord
        for coord in all_coords(state.topology.shape)
        if state.cells[flat_index(state.topology.shape, coord)] != 0
    )


def outer_code(predicate: object) -> int:
    if not callable(predicate):
        raise TypeError("predicate must be callable in this oracle helper")
    code = 0
    for count in range(9):
        for center in (0, 1):
            output = predicate(center, count)
            if type(output) is not int or output not in (0, 1):
                raise TypeError("predicate must return an exact bit")
            code |= output << (2 * count + center)
    return code


def assert_named_rules() -> None:
    """Reconstruct BOOK:2226-2234 and BOOK:14239-14249 predicates."""

    code_175850 = outer_code(
        lambda center, count: 1 if count in (3, 5) else center
    )
    code_746 = outer_code(
        lambda center, count: 1 if count == 3 else 0 if count >= 5 else center
    )
    code_174826 = outer_code(
        lambda center, count: 1 if count == 3 else center
    )
    code_224 = outer_code(
        lambda center, count: 1
        if count == 3 or (center == 1 and count == 2)
        else 0
    )
    assert (code_175850, code_746, code_174826, code_224) == (
        175850,
        746,
        174826,
        224,
    )

    expected = {
        175850: lambda center, count: 1 if count in (3, 5) else center,
        746: lambda center, count: 1 if count == 3 else 0 if count >= 5 else center,
        174826: lambda center, count: 1 if count == 3 else center,
        224: lambda center, count: 1
        if count == 3 or (center == 1 and count == 2)
        else 0,
    }
    for code, predicate in expected.items():
        rule = BinaryOuterTotalistic(code, 8)
        for center in (0, 1):
            for count in range(9):
                neighbors = (1,) * count + (0,) * (8 - count)
                assert rule.evaluate(LocalRead(center, neighbors)) == predicate(center, count)

    shape = (11, 11)
    seeds: list[Cells] = []
    for length in (7, 7, 5, 3):
        values = [0] * 121
        start = (11 - length) // 2
        for column in range(start, start + length):
            values[flat_index(shape, (5, column))] = 1
        seeds.append(tuple(values))
    for code, cells in zip((175850, 746, 174826, 224), seeds, strict=True):
        native = Native2DState(2, shape, FixedBoundary(0), cells)
        direct = native_outer_step(code, native)
        generic = generic_step(
            strict_t22_program(BinaryOuterTotalistic(code, 8)),
            encode_native(native),
        )
        assert decode_generic(generic) == direct
        if code == 224:
            alive = tuple(
                (row, column)
                for row in range(shape[0])
                for column in range(shape[1])
                if direct.value_at(row, column) == 1
            )
            assert alive == ((4, 5), (5, 5), (6, 5))


def assert_printed_code_provenance() -> dict[str, int]:
    """Keep Notes code 3702 distinct from its ten-case denotation."""

    spelling = PrintedCodeProvenance(
        printed=3702,
        radix=2,
        width=10,
        digit_direction=CASE_ZERO_IS_LEAST_SIGNIFICANT,
    )
    assert spelling.printed == 3702
    assert spelling.radix == 2 and spelling.width == 10
    assert spelling.digit_direction == CASE_ZERO_IS_LEAST_SIGNIFICANT
    assert spelling.canonical_table == (0, 1, 1, 0, 1, 1, 1, 0, 0, 1)
    assert spelling.canonical_table != tuple(reversed(spelling.canonical_table))
    assert spelling.canonical_code == 630
    assert spelling.canonical_code == spelling.printed % (2**10)
    assert spelling.printed == 3 * (2**10) + spelling.canonical_code

    canonical = BinaryTotalistic(spelling.canonical_code, 8)
    for total, expected in enumerate(spelling.canonical_table):
        if total <= 8:
            read = LocalRead(0, (1,) * total + (0,) * (8 - total))
        else:
            read = LocalRead(1, (1,) * 8)
        assert canonical.evaluate(read) == expected
    assert factor_totalistic(expand_totalistic(canonical)) == canonical

    # The canonical schema never silently normalizes an out-of-range integer.
    expect_raises(
        ValueError,
        lambda: BinaryTotalistic(spelling.printed, 8),
    )
    return {
        "printed": spelling.printed,
        "canonical": spelling.canonical_code,
        "width": spelling.width,
        "radix": spelling.radix,
        "high_quotient": spelling.printed // (spelling.radix**spelling.width),
    }


def assert_wireworld_predicate_count() -> dict[str, int]:
    """Close all 4^9 local contexts against an independent literal rule."""

    rule = wireworld_rule()
    assert rule.alphabet_size == 4 and rule.neighbor_slots == 8
    assert rule.predicate == LabelEquals(1)
    assert rule.outputs == (
        (0,) * 9,
        (2,) * 9,
        (3,) * 9,
        (3, 1, 1, 3, 3, 3, 3, 3, 3),
    )
    fiber_counts: dict[tuple[int, int], int] = {}
    local_contexts = 0
    for context in product(range(4), repeat=9):
        neighbors = context[:4] + context[5:]
        read = LocalRead(context[4], neighbors)
        head_count = sum(value == 1 for value in neighbors)
        expected = native_wireworld_local(context)
        assert rule.evaluate(read) == expected
        key = (read.center, head_count)
        fiber_counts[key] = fiber_counts.get(key, 0) + 1
        local_contexts += 1
    assert local_contexts == 4**9 == 262_144
    assert len(fiber_counts) == 4 * 9 == 36
    assert all(
        fiber_counts[(center, count)] == comb(8, count) * 3 ** (8 - count)
        for center in range(4)
        for count in range(9)
    )

    # Equal numeric sums can have different typed predicate counts and outputs.
    two_heads = LocalRead(3, (1, 1, 0, 0, 0, 0, 0, 0))
    one_tail = LocalRead(3, (2, 0, 0, 0, 0, 0, 0, 0))
    assert sum(two_heads.neighbors) == sum(one_tail.neighbors) == 2
    assert sum(value == 1 for value in two_heads.neighbors) == 2
    assert sum(value == 1 for value in one_tail.neighbors) == 0
    assert (rule.evaluate(two_heads), rule.evaluate(one_tail)) == (1, 3)

    return {
        "local_contexts": local_contexts,
        "predicate_fibers": len(fiber_counts),
        "numeric_sum_collisions": 1,
    }


def assert_dyadaxes_lossy_summary() -> dict[str, int]:
    """Exhibit a Moore distinction erased by the current channel summary."""

    cardinal_offsets = tuple(
        offset
        for offset in MOORE_OFFSETS
        if abs(offset[0]) + abs(offset[1]) == 1
    )
    diagonal_offsets = tuple(
        offset
        for offset in MOORE_OFFSETS
        if abs(offset[0]) + abs(offset[1]) == 2
    )
    assert cardinal_offsets == CARDINAL_2D
    assert len(diagonal_offsets) == 4
    assert set(cardinal_offsets).isdisjoint(diagonal_offsets)
    assert set(cardinal_offsets).union(diagonal_offsets) == set(MOORE_OFFSETS)

    empty = LocalRead(0, (0,) * 8)
    three_neighbors = LocalRead(0, (1, 1, 0, 1, 0, 0, 0, 0))
    assert len(empty.neighbors) == len(three_neighbors.neighbors) == len(MOORE_OFFSETS)
    assert sum(empty.neighbors) == 0
    assert sum(three_neighbors.neighbors) == 3
    assert dyadaxes_2d_summary(empty) == dyadaxes_2d_summary(three_neighbors)
    assert dyadaxes_2d_summary(empty) == (0, False, False)

    named = BinaryOuterTotalistic(174826, 8)
    assert (named.evaluate(empty), named.evaluate(three_neighbors)) == (0, 1)
    return {
        "counterexamples": 1,
        "first_moore_count": sum(empty.neighbors),
        "second_moore_count": sum(three_neighbors.neighbors),
        "distinct_required_outputs": 2,
    }


def assert_rule_representations() -> dict[str, int]:
    """Close codecs/factors without a wasteful 2^18 x 512 product.

    Outer compact tables are all 18-bit vectors.  Every one of the 2^18
    vectors is decoded/re-encoded exactly.  Independently, all 512 contexts
    establish the complete 18-fiber map and each of its 18 bit bases is fully
    expanded/factored.  Because expansion selects exactly one independent bit
    per context, those two exhaustive facts prove every compact table.

    The smaller 2^10 equal-sum universe is expanded and factored in full.
    """

    assert BOOK_NINE_POSITIONS == tuple(product((-1, 0, 1), repeat=2))
    assert tuple(position for position in BOOK_NINE_POSITIONS if position != (0, 0)) == MOORE_OFFSETS
    assert (1 << 512).bit_length() == 513
    assert 1 << 18 == 262_144
    assert 1 << 10 == 1_024
    assert 1 << 9 == 512

    projection_codes = tuple(
        strict_general_to_code(book_position_projection(position))
        for position in range(9)
    )
    assert tuple(format(code, "0128x") for code in projection_codes) == expected_projection_hex()

    general_basis = (0, (1 << 512) - 1, *(1 << index for index in range(512)))
    for code in general_basis:
        table = strict_general_from_code(code)
        assert strict_general_to_code(table) == code
    assert len(general_basis) == 514

    fiber_counts: dict[tuple[int, int], int] = {}
    for context in product((0, 1), repeat=9):
        center = context[4]
        count = sum(context[:4]) + sum(context[5:])
        fiber_counts[(center, count)] = fiber_counts.get((center, count), 0) + 1
    assert len(fiber_counts) == 18
    assert all(
        fiber_counts[(center, count)] == comb(8, count)
        for count in range(9)
        for center in (0, 1)
    )

    outer_tables = 0
    for code in range(1 << 18):
        signature = tuple((code >> index) & 1 for index in range(18))
        reconstructed = sum(bit << index for index, bit in enumerate(signature))
        assert reconstructed == code
        outer_tables += 1
    for code in (0, (1 << 18) - 1, *(1 << index for index in range(18))):
        compact = BinaryOuterTotalistic(code, 8)
        expanded = expand_outer(compact)
        assert factor_outer(expanded) == compact
        assert strict_general_from_code(strict_general_to_code(expanded)) == expanded

    totalistic_tables = 0
    for code in range(1 << 10):
        compact = BinaryTotalistic(code, 8)
        expanded = expand_totalistic(compact)
        assert factor_totalistic(expanded) == compact
        assert strict_general_from_code(strict_general_to_code(expanded)) == expanded
        totalistic_tables += 1

    directional = book_position_projection(0)
    expect_raises(ValueError, lambda: factor_outer(directional))
    center_projection = book_position_projection(4)
    assert factor_outer(center_projection)
    expect_raises(ValueError, lambda: factor_totalistic(center_projection))
    valid = expand_outer(BinaryOuterTotalistic(175850, 8))
    outputs = list(valid.outputs)
    outputs[1] = 1 - outputs[1]
    expect_raises(ValueError, lambda: factor_outer(GeneralLookup(2, 8, tuple(outputs))))

    assert outer_tables == 262_144 and totalistic_tables == 1_024
    return {
        "general_basis": len(general_basis),
        "outer_tables": outer_tables,
        "outer_expansion_basis": 20,
        "totalistic_tables": totalistic_tables,
    }


def assert_symmetry_restrictions() -> dict[str, int]:
    """Derive the source's 2^140 C4 and 2^102 D4 restrictions."""

    c4_permutations = c4_square_permutations()
    d4_permutations = d4_square_permutations()
    assert c4_permutations == (
        (0, 1, 2, 3, 4, 5, 6, 7, 8),
        (2, 5, 8, 1, 4, 7, 0, 3, 6),
        (8, 7, 6, 5, 4, 3, 2, 1, 0),
        (6, 3, 0, 7, 4, 1, 8, 5, 2),
    )
    assert len(set(d4_permutations)) == 8
    for group in (c4_permutations, d4_permutations):
        group_set = set(group)
        for left, right in product(group, repeat=2):
            composition = tuple(left[right[index]] for index in range(9))
            assert composition in group_set

    contexts = tuple(book_context_from_index(index) for index in range(512))
    c4_fixed = tuple(
        sum(
            permute_book_context_by_positions(context, permutation) == context
            for context in contexts
        )
        for permutation in c4_permutations
    )
    d4_fixed = tuple(
        sum(
            permute_book_context_by_positions(context, permutation) == context
            for context in contexts
        )
        for permutation in d4_permutations
    )
    assert c4_fixed == (512, 8, 32, 8)
    assert d4_fixed == (512, 8, 32, 8, 64, 64, 64, 64)
    assert sum(c4_fixed) // len(c4_permutations) == 140
    assert sum(d4_fixed) // len(d4_permutations) == 102

    c4_orbits = derive_book_context_orbits(c4_permutations)
    d4_orbits = derive_book_context_orbits(d4_permutations)
    assert len(c4_orbits) == 140
    assert len(d4_orbits) == 102
    assert tuple(
        (size, sum(len(orbit) == size for orbit in c4_orbits))
        for size in (1, 2, 4)
    ) == ((1, 8), (2, 12), (4, 120))
    assert tuple(
        (size, sum(len(orbit) == size for orbit in d4_orbits))
        for size in (1, 2, 4, 8)
    ) == ((1, 8), (2, 8), (4, 50), (8, 36))

    for permutations, orbits in (
        (c4_permutations, c4_orbits),
        (d4_permutations, d4_orbits),
    ):
        for orbit in orbits:
            representative = book_context_from_index(orbit[0])
            derived = tuple(
                sorted(
                    binary_index(
                        permute_book_context_by_positions(
                            representative, permutation
                        )
                    )
                    for permutation in permutations
                )
            )
            assert tuple(sorted(set(derived))) == orbit

    # D4 adds reflections, so every C4 fiber lies wholly within one D4 fiber.
    d4_owner: dict[int, int] = {}
    for orbit_index, orbit in enumerate(d4_orbits):
        for context_index in orbit:
            d4_owner[context_index] = orbit_index
    assert len(d4_owner) == 512
    assert all(
        len({d4_owner[context_index] for context_index in orbit}) == 1
        for orbit in c4_orbits
    )

    basis_counts: dict[str, int] = {}
    disagreement_rejections = 0
    for name, orbits in (("c4", c4_orbits), ("d4", d4_orbits)):
        basis_cases = 0
        zero = (0,) * len(orbits)
        full = (1,) * len(orbits)
        for outputs, expected_code in (
            (zero, 0),
            (full, (1 << 512) - 1),
        ):
            expanded = expand_symmetry_restriction(outputs, orbits)
            assert strict_general_to_code(expanded) == expected_code
            assert factor_symmetry_restriction(expanded, orbits) == outputs
            basis_cases += 1
        for selected, orbit in enumerate(orbits):
            outputs = tuple(
                int(index == selected) for index in range(len(orbits))
            )
            expanded = expand_symmetry_restriction(outputs, orbits)
            expected_code = sum(1 << context_index for context_index in orbit)
            assert strict_general_to_code(expanded) == expected_code
            assert factor_symmetry_restriction(expanded, orbits) == outputs
            basis_cases += 1

        # Since the fibers are disjoint and every complete-map row selects one
        # compact bit, zero/full plus every one-bit basis certifies the entire
        # 2^140 or 2^102 table space without a Cartesian enumeration.
        assert basis_cases == len(orbits) + 2
        basis_counts[name] = basis_cases
        nontrivial = next(orbit for orbit in orbits if len(orbit) > 1)
        broken = strict_general_from_code(1 << nontrivial[0])
        expect_raises(
            ValueError,
            lambda broken=broken, orbits=orbits: factor_symmetry_restriction(
                broken, orbits
            ),
        )
        disagreement_rejections += 1

    assert basis_counts == {"c4": 142, "d4": 104}
    assert disagreement_rejections == 2
    return {
        "c4_orbits": len(c4_orbits),
        "d4_orbits": len(d4_orbits),
        "c4_basis": basis_counts["c4"],
        "d4_basis": basis_counts["d4"],
        "group_context_cases": len(contexts)
        * (len(c4_permutations) + len(d4_permutations)),
        "orbit_memberships": sum(map(len, c4_orbits))
        + sum(map(len, d4_orbits)),
        "disagreement_rejections": disagreement_rejections,
    }


def assert_basis_permutation() -> dict[str, int]:
    transformed, runtime_sorted, runtime_to_book, book_to_runtime = basis_permutations()
    assert transformed == (
        (-1, 1),
        (0, 1),
        (1, 1),
        (-1, 0),
        (0, 0),
        (1, 0),
        (-1, -1),
        (0, -1),
        (1, -1),
    )
    assert runtime_sorted == BOOK_NINE_POSITIONS
    assert runtime_to_book == (6, 3, 0, 7, 4, 1, 8, 5, 2)
    assert book_to_runtime == (2, 5, 8, 1, 4, 7, 0, 3, 6)

    book_projection_codes = tuple(
        strict_general_to_code(book_position_projection(position))
        for position in range(9)
    )
    expected_runtime_codes = tuple(
        book_projection_codes[book_to_runtime[position]]
        for position in range(9)
    )
    assert tuple(
        permute_book_code_to_runtime(code) for code in book_projection_codes
    ) == expected_runtime_codes
    assert tuple(
        permute_runtime_code_to_book(code) for code in expected_runtime_codes
    ) == book_projection_codes

    context_cases = 0
    for book_code in book_projection_codes:
        runtime_code = permute_book_code_to_runtime(book_code)
        for runtime_context in product((0, 1), repeat=9):
            book_context = runtime_context_to_book(runtime_context)
            assert book_context_to_runtime(book_context) == runtime_context
            book_output = (book_code >> binary_index(book_context)) & 1
            runtime_output = (runtime_code >> binary_index(runtime_context)) & 1
            assert runtime_output == book_output
            context_cases += 1
    assert context_cases == 4_608

    basis_cases = 0
    for index in range(512):
        book_code = 1 << index
        runtime_code = permute_book_code_to_runtime(book_code)
        assert runtime_code.bit_count() == 1
        assert permute_runtime_code_to_book(runtime_code) == book_code
        basis_cases += 1

    # Book north is row -1/column 0 (position 1); in ENU it is runtime
    # position 5.  Reusing the Book code after runtime re-sort instead reads W.
    book_north = book_projection_codes[1]
    runtime_north = permute_book_code_to_runtime(book_north)
    runtime_context = (0, 0, 0, 0, 0, 1, 0, 0, 0)
    book_context = runtime_context_to_book(runtime_context)
    assert book_context == (0, 1, 0, 0, 0, 0, 0, 0, 0)
    direct = (book_north >> binary_index(book_context)) & 1
    naive = (book_north >> binary_index(runtime_context)) & 1
    certified = (runtime_north >> binary_index(runtime_context)) & 1
    assert (direct, naive, certified) == (1, 0, 1)

    native = Native2DState(
        2,
        (5, 5),
        FixedBoundary(0),
        cells_with_one((5, 5), (2, 2)),
    )
    native_next = native_general_step(book_north, native)
    runtime_old = native_to_enu(native)
    certified_next = generic_step(
        strict_t22_program(strict_general_from_code(runtime_north)), runtime_old
    )
    naive_next = generic_step(
        strict_t22_program(strict_general_from_code(book_north)), runtime_old
    )
    expected = native_to_enu(native_next, generation=1)
    assert certified_next == expected
    assert naive_next != expected
    assert nonzero_coords(certified_next) == ((2, 1),)
    assert nonzero_coords(naive_next) == ((3, 2),)
    return {"context_cases": context_cases, "basis_cases": basis_cases}


def assert_full_total_product_generalization() -> dict[str, int]:
    """Certify BOOK:13475-13481 beyond the strict binary T22 schemas."""

    expected_counts = {
        (1, 2): 6,
        (2, 2): 18,
        (3, 2): 54,
        (1, 3): 15,
        (2, 3): 51,
        (3, 3): 159,
        (2, 4): 100,
    }
    for (dimension, alphabet_size), expected in expected_counts.items():
        slots = 3**dimension - 1
        full_total_values = slots * (alphabet_size - 1) + 1
        assert full_total_product_case_count(dimension, alphabet_size) == expected
        assert expected == alphabet_size * full_total_values

    # All 3^9 ternary Moore contexts hit precisely the 51 source-defined
    # Self x FullTotal cases.  The fiber counts are checked independently.
    outputs = tuple(
        ((index // 3) + 2 * (index % 3)) % 3
        for index in range(full_total_product_case_count(2, 3))
    )
    rule = FullTotalProduct(2, 3, outputs)
    fibers = [0] * len(outputs)
    for book_context in product(range(3), repeat=9):
        center = book_context[4]
        neighbors = book_context[:4] + book_context[5:]
        index = center + 3 * sum(neighbors)
        assert rule.evaluate(LocalRead(center, neighbors)) == outputs[index]
        fibers[index] += 1
    neighbor_sum_counts = [0] * 17
    for neighbors in product(range(3), repeat=8):
        neighbor_sum_counts[sum(neighbors)] += 1
    assert all(count > 0 for count in fibers)
    assert sum(fibers) == 3**9
    for full_total, multiplicity in enumerate(neighbor_sum_counts):
        for center in range(3):
            assert fibers[center + 3 * full_total] == multiplicity

    # The generalized profile overlaps the binary outer-totalistic function
    # space losslessly, but the strict T22 integer-code schema stays distinct.
    binary_code = 174826
    strict_binary = BinaryOuterTotalistic(binary_code, 8)
    product_binary = FullTotalProduct(
        2,
        2,
        tuple((binary_code >> index) & 1 for index in range(18)),
    )
    assert type(strict_binary) is BinaryOuterTotalistic
    assert type(product_binary) is FullTotalProduct
    for context in product((0, 1), repeat=9):
        read = LocalRead(context[0], context[1:])
        assert strict_binary.evaluate(read) == product_binary.evaluate(read)

    return {
        "formula_cases": len(expected_counts),
        "ternary_table_cases": len(outputs),
        "ternary_contexts": sum(fibers),
    }


def assert_native_generic_commutation() -> dict[str, int]:
    periodic = PeriodicBoundary()
    binary_states = tuple(product((0, 1), repeat=4))
    counts = {
        "outer_basis": 0,
        "totalistic_basis": 0,
        "general_basis": 0,
        "directional": 0,
        "named": 0,
        "wireworld": 0,
        "ternary_projection": 0,
        "ternary_full_total": 0,
    }

    # Each local result selects exactly one compact-table bit.  Zero, full,
    # and every one-bit basis therefore span every 18-bit/10-bit rule without
    # the wasteful Cartesian product of all rules and all finite states.
    for code in (0, (1 << 18) - 1, *(1 << index for index in range(18))):
        program = strict_t22_program(BinaryOuterTotalistic(code, 8))
        for cells in binary_states:
            native = Native2DState(2, (2, 2), periodic, cells)
            generic = generic_step(program, encode_native(native, generation=7))
            assert decode_generic(generic) == native_outer_step(code, native)
            assert generic.generation == 8
            counts["outer_basis"] += 1

    for code in (0, (1 << 10) - 1, *(1 << index for index in range(10))):
        program = strict_t22_program(BinaryTotalistic(code, 8))
        for cells in binary_states:
            native = Native2DState(2, (2, 2), periodic, cells)
            assert decode_generic(generic_step(program, encode_native(native))) == native_totalistic_step(code, native)
            counts["totalistic_basis"] += 1

    # Every row of the 512-context codec receives a nonaliasing center witness.
    general_codes = (0, (1 << 512) - 1, *(1 << index for index in range(512)))
    positions = tuple((2 + drow, 2 + dcolumn) for drow, dcolumn in BOOK_NINE_POSITIONS)
    for code in general_codes:
        active_index = code.bit_length() - 1 if code and code != (1 << 512) - 1 else 0
        context = tuple((active_index >> shift) & 1 for shift in range(8, -1, -1))
        values = [0] * 25
        for coord, value in zip(positions, context, strict=True):
            values[flat_index((5, 5), coord)] = value
        native = Native2DState(2, (5, 5), FixedBoundary(0), tuple(values))
        direct = native_general_step(code, native)
        generic = generic_step(
            strict_t22_program(strict_general_from_code(code)), encode_native(native)
        )
        assert decode_generic(generic) == direct
        if code not in (0, (1 << 512) - 1):
            assert direct.value_at(2, 2) == 1
        counts["general_basis"] += 1

    projection_codes = tuple(
        strict_general_to_code(book_position_projection(position))
        for position in range(9)
    )
    for position, code in enumerate(projection_codes):
        program = strict_t22_program(strict_general_from_code(code))
        for seed in all_coords((5, 5)):
            native = Native2DState(
                2,
                (5, 5),
                FixedBoundary(0),
                cells_with_one((5, 5), seed),
            )
            direct = native_general_step(code, native)
            assert direct == native_projection_step(position, native)
            assert decode_generic(generic_step(program, encode_native(native))) == direct
            counts["directional"] += 1

    for code in (175850, 746, 174826, 224):
        native = Native2DState(
            2,
            (7, 7),
            FixedBoundary(0),
            cells_with_one((7, 7), (3, 3)),
        )
        assert decode_generic(
            generic_step(
                strict_t22_program(BinaryOuterTotalistic(code, 8)),
                encode_native(native),
            )
        ) == native_outer_step(code, native)
        counts["named"] += 1

    printed_totalistic = PrintedCodeProvenance(
        3702,
        2,
        10,
        CASE_ZERO_IS_LEAST_SIGNIFICANT,
    )
    native = Native2DState(
        2,
        (7, 7),
        FixedBoundary(0),
        cells_with_one((7, 7), (3, 3)),
    )
    direct = native_totalistic_step(printed_totalistic.canonical_code, native)
    assert sum(direct.cells) == 9
    assert decode_generic(
        generic_step(
            strict_t22_program(
                BinaryTotalistic(printed_totalistic.canonical_code, 8)
            ),
            encode_native(native),
        )
    ) == direct
    counts["named"] += 1

    wireworld_cells = [0] * 25
    for coord, value in (
        ((2, 1), 1),
        ((1, 1), 2),
        ((2, 2), 3),
        ((2, 3), 3),
        ((4, 4), 3),
    ):
        wireworld_cells[flat_index((5, 5), coord)] = value
    native = Native2DState(
        4,
        (5, 5),
        FixedBoundary(0),
        tuple(wireworld_cells),
    )
    direct = native_wireworld_step(native)
    assert tuple(
        direct.value_at(*coord)
        for coord in ((2, 1), (1, 1), (2, 2), (2, 3), (4, 4))
    ) == (2, 3, 1, 3, 3)
    assert decode_generic(
        generic_step(
            strict_t22_program(wireworld_rule()),
            encode_native(native),
        )
    ) == direct
    counts["wireworld"] += 1

    ternary_program = strict_t22_program(book_position_projection(8, alphabet_size=3))
    for cells in product(range(3), repeat=4):
        native = Native2DState(3, (2, 2), periodic, cells)
        direct = native_projection_step(8, native)
        assert decode_generic(generic_step(ternary_program, encode_native(native))) == direct
        counts["ternary_projection"] += 1

    ternary_outputs = tuple(
        ((index // 3) + 2 * (index % 3)) % 3
        for index in range(full_total_product_case_count(2, 3))
    )
    ternary_full_total = strict_t22_program(
        FullTotalProduct(2, 3, ternary_outputs)
    )
    for cells in product(range(3), repeat=4):
        native = Native2DState(3, (2, 2), periodic, cells)
        direct = native_full_total_product_step(ternary_outputs, native)
        assert decode_generic(
            generic_step(ternary_full_total, encode_native(native))
        ) == direct
        counts["ternary_full_total"] += 1

    assert counts == {
        "outer_basis": 320,
        "totalistic_basis": 192,
        "general_basis": 514,
        "directional": 225,
        "named": 5,
        "wireworld": 1,
        "ternary_projection": 81,
        "ternary_full_total": 81,
    }
    return counts


def assert_aliasing_and_parallelism() -> None:
    topology = FiniteGrid((2, 2), PeriodicBoundary())
    old = GridConfiguration(
        FiniteAlphabet(2),
        topology,
        cells_with_one((2, 2), (1, 1)),
        SnapshotToken(0),
    )
    handle = SiteHandle(old.snapshot_token, (0, 0))
    access = make_access(MOORE_OFFSETS, self_position=4)
    read = read_local(old, (handle,), access)[0]
    assert read == LocalRead(0, (1, 0, 1, 0, 0, 1, 0, 1))
    resolved = tuple(
        tuple(
            component % extent
            for component, extent in zip(add_coord(handle.coord, offset), topology.shape, strict=True)
        )
        for offset in MOORE_OFFSETS
    )
    assert len(resolved) == 8 and len(set(resolved)) == 3
    assert sum(read.neighbors) == 4
    assert sum(old.value_at(coord) for coord in set(resolved)) == 1
    sum_four = strict_t22_program(BinaryTotalistic(1 << 4, 8))
    assert generic_step(sum_four, old).value_at((0, 0)) == 1

    # A projection of Book west, raw (0,-1), shifts a one right under parallel
    # old-snapshot update.  Left-to-right in-place traversal erases it first.
    west_slot = MOORE_OFFSETS.index((0, -1))
    west = strict_t22_program(projection_rule(2, 8, west_slot))
    line = GridConfiguration(
        FiniteAlphabet(2),
        FiniteGrid((1, 4), FixedBoundary(0)),
        cells_with_one((1, 4), (0, 0)),
        SnapshotToken(3),
    )
    assert generic_step(west, line).cells == (0, 1, 0, 0)
    in_place = list(line.cells)
    for column in range(4):
        old_west = 0 if column == 0 else in_place[column - 1]
        neighbors = [0] * 8
        neighbors[west_slot] = old_west
        in_place[column] = west.rule.evaluate(LocalRead(in_place[column], tuple(neighbors)))
    assert tuple(in_place) == (0, 0, 0, 0)


def assert_support_boundary_and_background() -> None:
    west_slot = MOORE_OFFSETS.index((0, -1))
    west = strict_t22_program(projection_rule(2, 8, west_slot))
    shape = (3, 3)
    edge_cells = cells_with_one(shape, (1, 2))
    periodic = GridConfiguration(
        FiniteAlphabet(2), FiniteGrid(shape, PeriodicBoundary()), edge_cells, SnapshotToken(0)
    )
    fixed = GridConfiguration(
        FiniteAlphabet(2), FiniteGrid(shape, FixedBoundary(0)), edge_cells, SnapshotToken(0)
    )
    assert nonzero_coords(generic_step(west, periodic)) == ((1, 0),)
    assert nonzero_coords(generic_step(west, fixed)) == ()

    growth_code = outer_code(lambda center, count: 1 if center == 1 or count > 0 else 0)
    growth = strict_t22_program(BinaryOuterTotalistic(growth_code, 8))
    state = sparse_field(2, 2, 0, (((0, 0), 1),))
    for time in range(5):
        expected = {
            (row, column)
            for row in range(-time, time + 1)
            for column in range(-time, time + 1)
        }
        assert state.background == 0
        assert {coord for coord, value in state.entries if value == 1} == expected
        assert len(state.entries) == (2 * time + 1) ** 2
        state = sparse_step(growth, state)

    nonquiescent = strict_t22_program(BinaryOuterTotalistic(1, 8))
    white = sparse_field(2, 2, 0, ())
    expect_raises(ValueError, lambda: fixed_background_sparse_step(nonquiescent, white))
    black = sparse_step(nonquiescent, white)
    assert black.background == 1 and black.entries == ()
    white_again = sparse_step(nonquiescent, black)
    assert white_again.background == 0 and white_again.entries == ()
    seed = sparse_field(2, 2, 0, (((0, 0), 1),))
    assert fixed_background_sparse_step(growth, seed) == sparse_step(growth, seed)

    shift = (5, -7)
    original = sparse_field(2, 2, 0, (((0, 0), 1), ((1, 0), 1)))
    translated = sparse_field(
        2,
        2,
        0,
        tuple((add_coord(coord, shift), value) for coord, value in original.entries),
    )
    original_next = sparse_step(growth, original)
    translated_next = sparse_step(growth, translated)
    assert translated_next.background == original_next.background
    assert translated_next.entries == tuple(
        (add_coord(coord, shift), value) for coord, value in original_next.entries
    )


def axis_offsets(dimension: int) -> tuple[Offset, ...]:
    dimension = require_int(dimension, "dimension")
    if dimension <= 0:
        raise ValueError("dimension must be positive")
    result: list[Offset] = []
    for axis in range(dimension):
        negative = [0] * dimension
        positive = [0] * dimension
        negative[axis] = -1
        positive[axis] = 1
        result.extend((tuple(negative), tuple(positive)))
    return tuple(result)


def assert_t21_t23_same_runner() -> None:
    """T21/T22/T23 differ in access data, not the generic step function."""

    for dimension in (2, 3):
        offsets = axis_offsets(dimension)
        program = CAProgram(
            FiniteAlphabet(2),
            make_access(offsets, self_position=0),
            projection_rule(2, len(offsets), 0),
        )
        shape = (3,) * dimension
        seed = (1,) * dimension
        old = GridConfiguration(
            FiniteAlphabet(2),
            FiniteGrid(shape, FixedBoundary(0)),
            cells_with_one(shape, seed),
            SnapshotToken(0),
        )
        successor = generic_step(program, old)
        assert nonzero_coords(successor) == (subtract_coord(seed, offsets[0]),)

    t21 = CAProgram(
        FiniteAlphabet(2),
        make_access(CARDINAL_2D, self_position=2),
        projection_rule(2, 4, 0),
    )
    t22 = strict_t22_program(projection_rule(2, 8, 0))
    old2 = GridConfiguration(
        FiniteAlphabet(2),
        FiniteGrid((5, 5), FixedBoundary(0)),
        cells_with_one((5, 5), (2, 2)),
        SnapshotToken(0),
    )
    assert type(generic_step(t21, old2)) is GridConfiguration
    assert type(generic_step(t22, old2)) is GridConfiguration
    assert len(t21.neighborhood.offsets) == 4
    assert len(t22.neighborhood.offsets) == 8


def assert_hostile_validation() -> None:
    expect_raises(TypeError, lambda: FiniteAlphabet(True))
    expect_raises(ValueError, lambda: FiniteAlphabet(1))
    expect_raises(TypeError, lambda: FiniteGrid([2, 2], PeriodicBoundary()))
    expect_raises(ValueError, lambda: FiniteGrid((2, 0), PeriodicBoundary()))
    expect_raises(TypeError, lambda: FixedBoundary(False))
    expect_raises(TypeError, lambda: SnapshotToken(True))
    expect_raises(ValueError, lambda: SnapshotToken(-1))
    expect_raises(TypeError, lambda: make_access(list(MOORE_OFFSETS), 4))
    expect_raises(ValueError, lambda: make_access(((0, 0), *MOORE_OFFSETS), 4))
    expect_raises(ValueError, lambda: make_access((MOORE_OFFSETS[0], MOORE_OFFSETS[0]), 1))
    expect_raises(ValueError, lambda: LocalAccess((SelfAccess(), OffsetAccess((-1, 0)), SelfAccess())))
    expect_raises(TypeError, lambda: LocalAccess((SelfAccess(), object())))
    expect_raises(TypeError, lambda: BinaryOuterTotalistic(True, 8))
    expect_raises(ValueError, lambda: BinaryOuterTotalistic(1 << 18, 8))
    expect_raises(TypeError, lambda: outer_code(object()))
    expect_raises(TypeError, lambda: outer_code(lambda _center, _count: True))
    expect_raises(TypeError, lambda: BinaryTotalistic(False, 8))
    expect_raises(ValueError, lambda: BinaryTotalistic(1 << 10, 8))
    expect_raises(ValueError, lambda: BinaryTotalistic(3702, 8))
    expect_raises(TypeError, lambda: LabelEquals(True))
    expect_raises(ValueError, lambda: LabelEquals(-1))
    expect_raises(TypeError, lambda: LabelEquals(1).matches(False))
    expect_raises(
        TypeError,
        lambda: PredicateCountLookup(4, 8, object(), ((0,) * 9,) * 4),
    )
    expect_raises(
        ValueError,
        lambda: PredicateCountLookup(4, 8, LabelEquals(4), ((0,) * 9,) * 4),
    )
    expect_raises(
        ValueError,
        lambda: PredicateCountLookup(4, 8, LabelEquals(1), ((0,) * 9,) * 3),
    )
    expect_raises(
        ValueError,
        lambda: PredicateCountLookup(4, 8, LabelEquals(1), ((0,) * 8,) * 4),
    )
    expect_raises(
        TypeError,
        lambda: PredicateCountLookup(
            4,
            8,
            LabelEquals(1),
            ((0,) * 9, (0,) * 9, (0,) * 9, (*((0,) * 8), False)),
        ),
    )
    expect_raises(
        ValueError,
        lambda: wireworld_rule().evaluate(LocalRead(3, (1,) * 7)),
    )
    expect_raises(
        ValueError,
        lambda: wireworld_rule().evaluate(LocalRead(4, (1,) * 8)),
    )
    expect_raises(TypeError, lambda: native_wireworld_local([0] * 9))
    expect_raises(ValueError, lambda: native_wireworld_local((0,) * 8))
    expect_raises(
        TypeError,
        lambda: native_wireworld_local((*((0,) * 8), False)),
    )
    expect_raises(ValueError, lambda: native_wireworld_local((*((0,) * 8), 4)))
    expect_raises(ValueError, lambda: dyadaxes_2d_summary(LocalRead(0, (0,) * 7)))
    expect_raises(ValueError, lambda: dyadaxes_2d_summary(LocalRead(2, (0,) * 8)))
    expect_raises(
        TypeError,
        lambda: PrintedCodeProvenance(
            True, 2, 10, CASE_ZERO_IS_LEAST_SIGNIFICANT
        ),
    )
    expect_raises(
        ValueError,
        lambda: PrintedCodeProvenance(
            -1, 2, 10, CASE_ZERO_IS_LEAST_SIGNIFICANT
        ),
    )
    expect_raises(
        ValueError,
        lambda: PrintedCodeProvenance(
            3702, 1, 10, CASE_ZERO_IS_LEAST_SIGNIFICANT
        ),
    )
    expect_raises(
        ValueError,
        lambda: PrintedCodeProvenance(
            3702, 2, 0, CASE_ZERO_IS_LEAST_SIGNIFICANT
        ),
    )
    expect_raises(TypeError, lambda: PrintedCodeProvenance(3702, 2, 10, 0))
    expect_raises(
        ValueError,
        lambda: PrintedCodeProvenance(3702, 2, 10, "most-significant-first"),
    )
    expect_raises(TypeError, lambda: full_total_product_case_count(True, 3))
    expect_raises(ValueError, lambda: full_total_product_case_count(0, 3))
    expect_raises(TypeError, lambda: FullTotalProduct(True, 3, (0,) * 51))
    expect_raises(TypeError, lambda: FullTotalProduct(2, False, (0,) * 51))
    expect_raises(TypeError, lambda: FullTotalProduct(2, 3, [0] * 51))
    expect_raises(ValueError, lambda: FullTotalProduct(2, 3, (0,) * 50))
    expect_raises(
        TypeError,
        lambda: FullTotalProduct(2, 3, (*((0,) * 50), False)),
    )
    expect_raises(ValueError, lambda: GeneralLookup(2, 8, (0,) * 511))
    expect_raises(TypeError, lambda: GeneralLookup(2, 1, (0, 0, 0, False)))
    expect_raises(TypeError, lambda: strict_general_from_code(True))
    expect_raises(ValueError, lambda: strict_general_from_code(1 << 512))
    expect_raises(TypeError, lambda: factor_outer(BinaryTotalistic(0, 8)))
    expect_raises(TypeError, lambda: factor_totalistic(BinaryOuterTotalistic(0, 8)))
    expect_raises(TypeError, lambda: square_position_permutation(True))
    expect_raises(ValueError, lambda: square_position_permutation(4))
    expect_raises(TypeError, lambda: square_position_permutation(0, reflected=1))
    expect_raises(TypeError, lambda: book_context_from_index(False))
    expect_raises(ValueError, lambda: book_context_from_index(512))
    expect_raises(
        TypeError,
        lambda: permute_book_context_by_positions(
            [0] * 9, c4_square_permutations()[0]
        ),
    )
    expect_raises(
        ValueError,
        lambda: permute_book_context_by_positions(
            (0,) * 9, (0, 1, 2, 3, 4, 5, 6, 7, 7)
        ),
    )
    expect_raises(ValueError, lambda: derive_book_context_orbits(()))
    c4_orbits = derive_book_context_orbits(c4_square_permutations())
    expect_raises(
        ValueError,
        lambda: expand_symmetry_restriction((0,) * 139, c4_orbits),
    )
    expect_raises(
        TypeError,
        lambda: expand_symmetry_restriction((*((0,) * 139), False), c4_orbits),
    )
    expect_raises(
        TypeError,
        lambda: factor_symmetry_restriction(BinaryOuterTotalistic(0, 8), c4_orbits),
    )
    expect_raises(TypeError, lambda: book_row_column_to_enu([-1, 0]))
    expect_raises(TypeError, lambda: permute_book_code_to_runtime(True))
    expect_raises(ValueError, lambda: permute_book_code_to_runtime(1 << 512))

    alphabet = FiniteAlphabet(2)
    topology = FiniteGrid((2, 2), FixedBoundary(0))
    one_dimensional_eight_offsets = make_access(
        ((-4,), (-3,), (-2,), (-1,), (1,), (2,), (3,), (4,)),
        4,
    )
    expect_raises(
        ValueError,
        lambda: CAProgram(
            FiniteAlphabet(3),
            one_dimensional_eight_offsets,
            FullTotalProduct(2, 3, (0,) * 51),
        ),
    )
    expect_raises(
        TypeError,
        lambda: GridConfiguration(alphabet, topology, [0, 0, 0, 0], SnapshotToken(0)),
    )
    expect_raises(
        ValueError,
        lambda: GridConfiguration(alphabet, topology, (0, 0, 0), SnapshotToken(0)),
    )
    expect_raises(
        TypeError,
        lambda: GridConfiguration(alphabet, topology, (0, 0, False, 0), SnapshotToken(0)),
    )

    program = strict_t22_program(book_position_projection(1))
    old = GridConfiguration(alphabet, topology, (1, 0, 0, 0), SnapshotToken(5))
    active = select_all_sites(old)
    reads = read_local(old, active, program.neighborhood)
    writes = make_assignments(program, active, reads)
    validate_plan(old, program, active, reads, writes)
    peer = GridConfiguration(alphabet, topology, old.cells, SnapshotToken(5))
    foreign = (SiteHandle(peer.snapshot_token, active[0].coord), *active[1:])
    expect_raises(ValueError, lambda: read_local(old, foreign, program.neighborhood))
    expect_raises(ValueError, lambda: read_local(old, (active[0], active[0]), program.neighborhood))
    tampered_reads = (LocalRead(1 - reads[0].center, reads[0].neighbors), *reads[1:])
    expect_raises(
        ValueError,
        lambda: validate_plan(old, program, active, tampered_reads, writes),
    )
    wrong_target = (
        SiteAssignment(writes[0].source, (1, 1), writes[0].value),
        *writes[1:],
    )
    expect_raises(
        ValueError,
        lambda: validate_plan(old, program, active, reads, wrong_target),
    )
    successor = apply_parallel(old, active, writes)
    assert successor.snapshot_token is not old.snapshot_token
    expect_raises(ValueError, lambda: read_local(successor, active, program.neighborhood))
    expect_raises(
        ValueError,
        lambda: sparse_field(2, 2, 0, (((0, 0), 1), ((0, 0), 1))),
    )
    expect_raises(
        ValueError,
        lambda: sparse_field(2, 2, 0, (((0, 0), 0),)),
    )


DECISION_MATRIX: tuple[tuple[str, str, str, str], ...] = (
    ("DOMAIN", "direct reuse", "DiscreteSpace(dimension=2)", "T22 does not change dimensional space"),
    ("CONFIGURATION", "direct reuse", "FixedLattice(SquareGrid(Z^2),Alphabet)", "support and topology remain fixed"),
    ("FRONTIER", "direct reuse", "AllSites", "every old lattice site fires once"),
    ("NEIGHBORHOOD", "parameterization", "Compose(Self,OrderedMooreOffsets)", "one Self plus eight unique ordered surrounding positions"),
    ("RULE", "restriction/lossless representation", "SchemaTaggedClosedLocalMap", "512-context, Self x count, and equal-sum schemas remain distinct"),
    ("UPDATE", "direct reuse", "SnapshotParallelSameSite", "one old-snapshot assignment per source"),
    ("SEED", "direct reuse", "IndependentValidatedConfiguration", "rows, horizons, and random laws are not program identity"),
    ("REALIZATION", "direct reuse/parameterization", "ExplicitBoundaryWorkView", "finite boundaries and views never define native Z^2"),
)


def assert_decision_matrix() -> None:
    assert tuple(row[0] for row in DECISION_MATRIX) == (
        "DOMAIN",
        "CONFIGURATION",
        "FRONTIER",
        "NEIGHBORHOOD",
        "RULE",
        "UPDATE",
        "SEED",
        "REALIZATION",
    )
    assert "lossless representation" in DECISION_MATRIX[4][1]
    assert DECISION_MATRIX[5][1] == "direct reuse"
    assert all("executor" not in row[2].lower() for row in DECISION_MATRIX)


def main() -> None:
    assert BOOK_NINE_POSITIONS == tuple(sorted(BOOK_NINE_POSITIONS))
    assert MOORE_OFFSETS == tuple(sorted(MOORE_OFFSETS))
    assert (0, 0) not in MOORE_OFFSETS
    access = strict_t22_program(BinaryTotalistic(0, 8)).neighborhood
    assert tuple(type(component) for component in access.components) == (
        OffsetAccess,
        OffsetAccess,
        OffsetAccess,
        OffsetAccess,
        SelfAccess,
        OffsetAccess,
        OffsetAccess,
        OffsetAccess,
        OffsetAccess,
    )
    assert access.self_position == 4 and access.offsets == MOORE_OFFSETS

    assert_named_rules()
    printed_code_counts = assert_printed_code_provenance()
    wireworld_counts = assert_wireworld_predicate_count()
    dyadaxes_counts = assert_dyadaxes_lossy_summary()
    representation_counts = assert_rule_representations()
    symmetry_counts = assert_symmetry_restrictions()
    permutation_counts = assert_basis_permutation()
    generalized_counts = assert_full_total_product_generalization()
    commutation_counts = assert_native_generic_commutation()
    assert_aliasing_and_parallelism()
    assert_support_boundary_and_background()
    assert_t21_t23_same_runner()
    assert_hostile_validation()
    assert_decision_matrix()

    commutations = sum(commutation_counts.values())
    assert commutations == 1_419
    print("T22 semantic oracle: PASS")
    print(f"native_generic_commutations={commutations}")
    print(
        "commutation_partition="
        f"outer_basis:{commutation_counts['outer_basis']},"
        f"sum_basis:{commutation_counts['totalistic_basis']},"
        f"general_basis:{commutation_counts['general_basis']},"
        f"directional:{commutation_counts['directional']},"
        f"named:{commutation_counts['named']},"
        f"wireworld:{commutation_counts['wireworld']},"
        f"ternary_projection:{commutation_counts['ternary_projection']},"
        f"ternary_full_total:{commutation_counts['ternary_full_total']}"
    )
    print(
        f"outer_18_case_tables={representation_counts['outer_tables']} "
        "(all signatures round-trip; complete 512-context fibers + 20 expansion bases)"
    )
    print(f"equal_sum_10_case_tables={representation_counts['totalistic_tables']} (all expand/factor)")
    print(f"general_512_context_codec_basis={representation_counts['general_basis']}")
    print(f"book_to_ENU_context_cases={permutation_counts['context_cases']}")
    print(f"book_to_ENU_table_basis_cases={permutation_counts['basis_cases']}")
    print(
        "named_codes=175850,746,174826,224 "
        "reconstructed_from_source_predicates=PASS; life_224=B3/S23"
    )
    print(
        "printed_code_adapter="
        f"radix:{printed_code_counts['radix']},"
        f"width:{printed_code_counts['width']},"
        f"direction:{CASE_ZERO_IS_LEAST_SIGNIFICANT},"
        f"printed:{printed_code_counts['printed']},"
        f"canonical:{printed_code_counts['canonical']},"
        f"high_quotient:{printed_code_counts['high_quotient']}; "
        "strict_out_of_range_rejection=PASS; native_generic_as_630=PASS"
    )
    print(
        "wireworld_predicate_count="
        f"local_contexts:{wireworld_counts['local_contexts']},"
        f"predicate_fibers:{wireworld_counts['predicate_fibers']},"
        f"equal_numeric_sum_collisions:{wireworld_counts['numeric_sum_collisions']},"
        f"native_generic_steps:{commutation_counts['wireworld']}; "
        "predicate=neighbor_label_equals_1; alphabet=4; table=0->0,1->2,2->3,"
        "3->1_if_count_1_or_2_else_3"
    )
    print(
        "dyadaxes_lossy_summary="
        f"counterexamples:{dyadaxes_counts['counterexamples']},"
        f"moore_counts:{dyadaxes_counts['first_moore_count']}_vs_"
        f"{dyadaxes_counts['second_moore_count']},"
        f"distinct_required_outputs:{dyadaxes_counts['distinct_required_outputs']}; "
        "raw_geometry=Self+8_Moore_offsets; "
        "summary=(self,cardinal_count>2,diagonal_count>2); new_commutations=0"
    )
    print(
        "symmetry_restrictions="
        f"C4_orbits:{symmetry_counts['c4_orbits']},"
        f"D4_orbits:{symmetry_counts['d4_orbits']}; "
        f"expansion_factor_basis:C4:{symmetry_counts['c4_basis']},"
        f"D4:{symmetry_counts['d4_basis']}; "
        f"group_context_cases:{symmetry_counts['group_context_cases']},"
        f"orbit_memberships:{symmetry_counts['orbit_memberships']},"
        f"one_row_disagreements_rejected:{symmetry_counts['disagreement_rejections']}"
    )
    print(
        "rule_counts=2^512_general,2^140_C4,2^102_D4,"
        "2^18_outer,2^10_equal_sum,2^9_growth"
    )
    print(
        "generalized_profile=self+k*FullTotal; "
        "table_length=k*((3^d-1)*(k-1)+1); "
        f"formula_cases={generalized_counts['formula_cases']}; "
        f"ternary_d2_cases={generalized_counts['ternary_table_cases']}; "
        f"ternary_contexts={generalized_counts['ternary_contexts']}"
    )
    print("complete_declared_access=Self+eight_Moore_offsets=PASS")
    print("projection_patterns=9x512_bits; nonaliasing_5x5_directional=PASS")
    print("row_column_to_ENU_full_permutation=PASS; naive_resort_counterexample=PASS")
    print("small_torus_slot_multiplicity=PASS; old_snapshot_parallelism=PASS")
    print("exact_Z2_sparse_background=PASS; finite_boundary_separation=PASS")
    print("T21_T22_T23_same_runner=PASS; new_UPDATE=NONE; family_executor=NONE")
    print("exact_type_and_opaque_snapshot_validation=PASS")
    print("proposed_D128=Moore access/RULE parameterization and lossless representations")


if __name__ == "__main__":
    main()
