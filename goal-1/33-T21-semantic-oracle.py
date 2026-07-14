#!/usr/bin/env python3
"""Dependency-free semantic checks for Goal 1 stage T21.

This is research evidence, not runtime code.  It tests the claim that the
strict two-dimensional cellular automata in Chapter 5 are an ordinary
parameterization of the already-generic cellular-automaton construction:

    all sites -> old-snapshot local read -> same-site assignment
              -> atomic parallel commit

The native support is the square integer lattice.  Finite periodic/fixed
boxes are explicit computational realizations, never an implicit change to
that support.  The NEIGHBORHOOD read schema explicitly composes one Self
component with exactly four ordered orthogonal OffsetAccess components; the
RULE input preserves Self separately from the four surrounding values.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product
from math import prod
from typing import Protocol


if not __debug__:
    raise RuntimeError("T21 semantic verification requires assertions; do not run with -O")


Coord = tuple[int, ...]
Offset = tuple[int, ...]
Cells = tuple[int, ...]

NEG_AXIS_0: Offset = (-1, 0)
NEG_AXIS_1: Offset = (0, -1)
POS_AXIS_1: Offset = (0, 1)
POS_AXIS_0: Offset = (1, 0)

# BOOK:13513-13518 gives the sorted five-cell position list including center.
# The complete access schema below represents its zero displacement as a
# declared Self component and its other four positions as OffsetAccess values.
ORTHOGONAL_2D: tuple[Offset, ...] = (
    NEG_AXIS_0,
    NEG_AXIS_1,
    POS_AXIS_1,
    POS_AXIS_0,
)
STRICT_T21_SORTED_INPUTS: tuple[Offset, ...] = (
    NEG_AXIS_0,
    NEG_AXIS_1,
    (0, 0),
    POS_AXIS_1,
    POS_AXIS_0,
)

# Raw tuples are authoritative.  Compass words are coordinate-convention
# isomorphisms, not offset identity.  A row/column raster convention and the
# current simple-programs x-east/y-north convention attach different names to
# precisely the same ordered geometry.
ROW_COLUMN_COMPASS: tuple[tuple[str, Offset], ...] = (
    ("north", NEG_AXIS_0),
    ("west", NEG_AXIS_1),
    ("east", POS_AXIS_1),
    ("south", POS_AXIS_0),
)
XY_EAST_NORTH_COMPASS: tuple[tuple[str, Offset], ...] = (
    ("west", NEG_AXIS_0),
    ("south", NEG_AXIS_1),
    ("north", POS_AXIS_1),
    ("east", POS_AXIS_0),
)

# Projection codes for the five raw BOOK positions in exact sorted order.
BOOK_GENERAL_PROJECTION_CODES: tuple[int, ...] = (
    0xFFFF0000,
    0xFF00FF00,
    0xF0F0F0F0,
    0xCCCCCCCC,
    0xAAAAAAAA,
)

# T22 boundary: the eight surrounding cells, still excluding center from the
# geometric offset collection.  It uses the same kernel with a different
# explicit neighborhood value.
MOORE_2D: tuple[Offset, ...] = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


def require_exact_int(value: object, name: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{name} must be an exact int")
    return value


def require_exact_tuple(value: object, name: str) -> tuple[object, ...]:
    if type(value) is not tuple:
        raise TypeError(f"{name} must be an exact tuple")
    return value


def checked_coord(value: object, dimension: int, name: str = "coordinate") -> Coord:
    raw = require_exact_tuple(value, name)
    if len(raw) != dimension:
        raise ValueError(f"{name} has the wrong dimension")
    return tuple(require_exact_int(item, f"{name} component") for item in raw)


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
        size = require_exact_int(self.size, "alphabet size")
        if size < 2:
            raise ValueError("a cellular alphabet must contain at least two values")

    def check(self, value: object, name: str = "cell value") -> int:
        checked = require_exact_int(value, name)
        if checked < 0 or checked >= self.size:
            raise ValueError(f"{name} is outside the finite alphabet")
        return checked


@dataclass(frozen=True)
class PeriodicBoundary:
    """A finite torus realization; not the native square-lattice boundary."""


@dataclass(frozen=True)
class FixedBoundary:
    """A finite box realization with an explicitly declared exterior value."""

    value: int

    def __post_init__(self) -> None:
        require_exact_int(self.value, "fixed boundary value")


Boundary = PeriodicBoundary | FixedBoundary


@dataclass(frozen=True)
class FiniteGrid:
    shape: tuple[int, ...]
    boundary: Boundary

    def __post_init__(self) -> None:
        raw_shape = require_exact_tuple(self.shape, "grid shape")
        if not raw_shape:
            raise ValueError("a finite grid must have positive dimension")
        checked = tuple(require_exact_int(n, "shape extent") for n in raw_shape)
        if any(n <= 0 for n in checked):
            raise ValueError("all shape extents must be positive")
        if type(self.boundary) not in (PeriodicBoundary, FixedBoundary):
            raise TypeError("boundary must be an explicit supported boundary profile")

    @property
    def dimension(self) -> int:
        return len(self.shape)

    @property
    def size(self) -> int:
        return prod(self.shape)


@dataclass(frozen=True, eq=False)
class SnapshotToken:
    """Opaque configuration identity; generation is diagnostic only."""

    generation: int

    def __post_init__(self) -> None:
        generation = require_exact_int(self.generation, "generation")
        if generation < 0:
            raise ValueError("generation must be nonnegative")


def all_coords(shape: tuple[int, ...]) -> tuple[Coord, ...]:
    return tuple(product(*(range(n) for n in shape)))


def flat_index(shape: tuple[int, ...], coord: Coord) -> int:
    if len(shape) != len(coord):
        raise ValueError("coordinate has the wrong dimension")
    index = 0
    for extent, component in zip(shape, coord, strict=True):
        if component < 0 or component >= extent:
            raise ValueError("coordinate is outside the finite grid")
        index = index * extent + component
    return index


@dataclass(frozen=True)
class GridConfiguration:
    """One explicit finite realization of a lattice configuration."""

    alphabet: FiniteAlphabet
    topology: FiniteGrid
    cells: Cells
    snapshot_token: SnapshotToken = field(compare=False, repr=False)

    def __post_init__(self) -> None:
        if type(self.alphabet) is not FiniteAlphabet:
            raise TypeError("alphabet must be FiniteAlphabet")
        if type(self.topology) is not FiniteGrid:
            raise TypeError("topology must be FiniteGrid")
        raw_cells = require_exact_tuple(self.cells, "cells")
        if len(raw_cells) != self.topology.size:
            raise ValueError("cell count does not match grid shape")
        for value in raw_cells:
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
    """Declared access to the firing locus itself."""


@dataclass(frozen=True)
class OffsetAccess:
    """Declared access at one raw displacement from the firing locus."""

    offset: Offset

    def __post_init__(self) -> None:
        raw = require_exact_tuple(self.offset, "access offset")
        if not raw:
            raise ValueError("access offsets must have positive dimension")
        checked = tuple(require_exact_int(value, "access offset component") for value in raw)
        if all(value == 0 for value in checked):
            raise ValueError("zero displacement must be declared as SelfAccess")


AccessComponent = SelfAccess | OffsetAccess


@dataclass(frozen=True)
class LocalAccess:
    """Complete NEIGHBORHOOD schema: Self plus ordered offset components."""

    components: tuple[AccessComponent, ...]

    def __post_init__(self) -> None:
        raw_components = require_exact_tuple(self.components, "access components")
        if not raw_components:
            raise ValueError("local access must declare components")
        if sum(type(component) is SelfAccess for component in raw_components) != 1:
            raise ValueError("local access must declare Self exactly once")
        offsets: list[Offset] = []
        dimension: int | None = None
        for component in raw_components:
            if type(component) is SelfAccess:
                continue
            if type(component) is not OffsetAccess:
                raise TypeError("unsupported local access component")
            offset = component.offset
            if dimension is None:
                dimension = len(offset)
            if len(offset) != dimension:
                raise ValueError("local access offsets have different dimensions")
            offsets.append(offset)
        if dimension is None or not offsets:
            raise ValueError("spatial local access must declare at least one offset")
        if len(set(offsets)) != len(offsets):
            raise ValueError("local access offsets must be unique")

    @property
    def offsets(self) -> tuple[Offset, ...]:
        return tuple(
            component.offset
            for component in self.components
            if type(component) is OffsetAccess
        )

    @property
    def self_position(self) -> int:
        return next(
            index
            for index, component in enumerate(self.components)
            if type(component) is SelfAccess
        )

    @property
    def dimension(self) -> int:
        return len(self.offsets[0])

    @property
    def slots(self) -> int:
        return len(self.offsets)


def make_local_access(offsets: tuple[Offset, ...], self_position: int) -> LocalAccess:
    raw_offsets = require_exact_tuple(offsets, "offsets")
    position = require_exact_int(self_position, "Self position")
    if position < 0 or position > len(raw_offsets):
        raise ValueError("Self position is outside the composed access schema")
    components: list[AccessComponent] = [OffsetAccess(offset) for offset in raw_offsets]
    components.insert(position, SelfAccess())
    return LocalAccess(tuple(components))


@dataclass(frozen=True)
class LocalRead:
    """RULE input: explicit center value plus ordered geometric neighbors."""

    center: int
    neighbors: tuple[int, ...]

    def __post_init__(self) -> None:
        require_exact_int(self.center, "center value")
        raw = require_exact_tuple(self.neighbors, "neighbor values")
        for value in raw:
            require_exact_int(value, "neighbor value")


def validate_read(read: LocalRead, alphabet_size: int, slots: int) -> None:
    if type(read) is not LocalRead:
        raise TypeError("rule input must be LocalRead")
    alphabet = FiniteAlphabet(alphabet_size)
    alphabet.check(read.center, "center value")
    if len(read.neighbors) != slots:
        raise ValueError("rule input has the wrong number of neighbor slots")
    for value in read.neighbors:
        alphabet.check(value, "neighbor value")


class LocalRule(Protocol):
    alphabet_size: int
    neighbor_slots: int

    def evaluate(self, read: LocalRead) -> int: ...


@dataclass(frozen=True)
class BinaryOuterTotalistic:
    """Binary output indexed by (neighbor black count, old center)."""

    code: int
    neighbor_slots: int
    alphabet_size: int = field(default=2, init=False)

    def __post_init__(self) -> None:
        code = require_exact_int(self.code, "outer-totalistic code")
        slots = require_exact_int(self.neighbor_slots, "neighbor slot count")
        if slots <= 0:
            raise ValueError("neighbor slot count must be positive")
        if code < 0 or code >= 1 << (2 * (slots + 1)):
            raise ValueError("outer-totalistic code is out of range")

    def evaluate(self, read: LocalRead) -> int:
        validate_read(read, 2, self.neighbor_slots)
        index = 2 * sum(read.neighbors) + read.center
        return (self.code >> index) & 1


@dataclass(frozen=True)
class BinaryTotalistic:
    """Binary output indexed by the sum of center and neighbor values."""

    code: int
    neighbor_slots: int
    alphabet_size: int = field(default=2, init=False)

    def __post_init__(self) -> None:
        code = require_exact_int(self.code, "totalistic code")
        slots = require_exact_int(self.neighbor_slots, "neighbor slot count")
        if slots <= 0:
            raise ValueError("neighbor slot count must be positive")
        if code < 0 or code >= 1 << (slots + 2):
            raise ValueError("totalistic code is out of range")

    def evaluate(self, read: LocalRead) -> int:
        validate_read(read, 2, self.neighbor_slots)
        return (self.code >> (read.center + sum(read.neighbors))) & 1


@dataclass(frozen=True)
class GeneralLookup:
    """Closed positional table over center followed by ordered neighbors."""

    alphabet_size: int
    neighbor_slots: int
    outputs: tuple[int, ...]

    def __post_init__(self) -> None:
        alphabet = FiniteAlphabet(self.alphabet_size)
        slots = require_exact_int(self.neighbor_slots, "neighbor slot count")
        if slots <= 0:
            raise ValueError("neighbor slot count must be positive")
        raw_outputs = require_exact_tuple(self.outputs, "lookup outputs")
        expected = alphabet.size ** (slots + 1)
        if len(raw_outputs) != expected:
            raise ValueError("lookup table does not cover every typed context")
        for output in raw_outputs:
            alphabet.check(output, "lookup output")

    def evaluate(self, read: LocalRead) -> int:
        validate_read(read, self.alphabet_size, self.neighbor_slots)
        index = 0
        for value in (read.center, *read.neighbors):
            index = index * self.alphabet_size + value
        return self.outputs[index]


Rule = BinaryOuterTotalistic | BinaryTotalistic | GeneralLookup


def projection_rule(alphabet_size: int, neighbor_slots: int, slot: int) -> GeneralLookup:
    """Create a closed table selecting center (-1) or one neighbor slot."""

    alphabet = FiniteAlphabet(alphabet_size)
    slots = require_exact_int(neighbor_slots, "neighbor slot count")
    selected = require_exact_int(slot, "projection slot")
    if slots <= 0:
        raise ValueError("neighbor slot count must be positive")
    if selected < -1 or selected >= slots:
        raise ValueError("projection slot is out of range")
    context_index = 0 if selected == -1 else selected + 1
    outputs = tuple(
        context[context_index]
        for context in product(range(alphabet.size), repeat=slots + 1)
    )
    return GeneralLookup(alphabet.size, slots, outputs)


def strict_t21_sorted_context(read: LocalRead) -> tuple[int, int, int, int, int]:
    """BOOK:13513 raw order: (-1,0),(0,-1),(0,0),(0,1),(1,0)."""

    validate_read(read, 2, 4)
    return (
        read.neighbors[0],
        read.neighbors[1],
        read.center,
        read.neighbors[2],
        read.neighbors[3],
    )


def binary_digits_to_index(digits: tuple[int, ...]) -> int:
    index = 0
    for digit in digits:
        if type(digit) is not int or digit not in (0, 1):
            raise TypeError("binary context must contain exact bits")
        index = 2 * index + digit
    return index


def strict_t21_general_from_code(code: int) -> GeneralLookup:
    """Decode a 32-row binary rule using the book's raw sorted-offset order."""

    checked = require_exact_int(code, "general 5-cell code")
    if checked < 0 or checked >= 1 << 32:
        raise ValueError("general 5-cell code is out of range")
    outputs: list[int] = []
    for context in product((0, 1), repeat=5):
        # GeneralLookup's transparent carrier is center followed by geometric
        # slots.  Rule-number significance is independently pinned to the
        # book's sorted raw input tuples.
        read = LocalRead(context[0], context[1:])
        index = binary_digits_to_index(strict_t21_sorted_context(read))
        outputs.append((checked >> index) & 1)
    return GeneralLookup(2, 4, tuple(outputs))


def strict_t21_general_to_code(table: GeneralLookup) -> int:
    """Inverse of strict_t21_general_from_code for every 32-context table."""

    if type(table) is not GeneralLookup:
        raise TypeError("general rule must be GeneralLookup")
    if table.alphabet_size != 2 or table.neighbor_slots != 4:
        raise ValueError("strict T21 general table must be binary with four offsets")
    code = 0
    for context in product((0, 1), repeat=5):
        read = LocalRead(context[0], context[1:])
        index = binary_digits_to_index(strict_t21_sorted_context(read))
        code |= table.evaluate(read) << index
    return code


def book_row_column_to_enu(raw_offset: object) -> Offset:
    """Declared basis map (row,column) -> (x=column,y=-row)."""

    row, column = checked_coord(raw_offset, 2, "BOOK row/column offset")
    return (column, -row)


def basis_permutations() -> tuple[
    tuple[Offset, ...], tuple[Offset, ...], tuple[int, ...], tuple[int, ...]
]:
    """Derive BOOK-order/lex-runtime permutations from the basis map."""

    transformed_in_book_order = tuple(
        book_row_column_to_enu(offset) for offset in STRICT_T21_SORTED_INPUTS
    )
    lex_runtime_positions = tuple(sorted(transformed_in_book_order))
    runtime_to_book = tuple(
        transformed_in_book_order.index(position) for position in lex_runtime_positions
    )
    book_to_runtime = tuple(
        lex_runtime_positions.index(position) for position in transformed_in_book_order
    )
    return (
        transformed_in_book_order,
        lex_runtime_positions,
        runtime_to_book,
        book_to_runtime,
    )


def runtime_context_to_book_context(
    runtime_context: tuple[int, int, int, int, int]
) -> tuple[int, int, int, int, int]:
    raw = require_exact_tuple(runtime_context, "runtime context")
    if len(raw) != 5:
        raise ValueError("runtime context must contain five values")
    for value in raw:
        if type(value) is not int or value not in (0, 1):
            raise TypeError("runtime context must contain exact bits")
    _transformed, _runtime, _runtime_to_book, book_to_runtime = basis_permutations()
    return tuple(raw[runtime_index] for runtime_index in book_to_runtime)  # type: ignore[return-value]


def book_context_to_runtime_context(
    book_context: tuple[int, int, int, int, int]
) -> tuple[int, int, int, int, int]:
    raw = require_exact_tuple(book_context, "BOOK context")
    if len(raw) != 5:
        raise ValueError("BOOK context must contain five values")
    for value in raw:
        if type(value) is not int or value not in (0, 1):
            raise TypeError("BOOK context must contain exact bits")
    _transformed, _runtime, runtime_to_book, _book_to_runtime = basis_permutations()
    return tuple(raw[book_index] for book_index in runtime_to_book)  # type: ignore[return-value]


def permute_book_code_to_runtime(code: int) -> int:
    """Reindex all 32 table rows for lexicographic ENU runtime inputs."""

    checked = require_exact_int(code, "BOOK general code")
    if checked < 0 or checked >= 1 << 32:
        raise ValueError("BOOK general code is out of range")
    runtime_code = 0
    for runtime_context in product((0, 1), repeat=5):
        book_context = runtime_context_to_book_context(runtime_context)
        book_index = binary_digits_to_index(book_context)
        runtime_index = binary_digits_to_index(runtime_context)
        runtime_code |= ((checked >> book_index) & 1) << runtime_index
    return runtime_code


def permute_runtime_code_to_book(code: int) -> int:
    """Inverse table reindexing from lexicographic ENU inputs to BOOK inputs."""

    checked = require_exact_int(code, "runtime general code")
    if checked < 0 or checked >= 1 << 32:
        raise ValueError("runtime general code is out of range")
    book_code = 0
    for book_context in product((0, 1), repeat=5):
        runtime_context = book_context_to_runtime_context(book_context)
        runtime_index = binary_digits_to_index(runtime_context)
        book_index = binary_digits_to_index(book_context)
        book_code |= ((checked >> runtime_index) & 1) << book_index
    return book_code


def expand_outer_totalistic(rule: BinaryOuterTotalistic) -> GeneralLookup:
    """Losslessly expand one qualifying Self x CardinalCount factor table."""

    if type(rule) is not BinaryOuterTotalistic or rule.neighbor_slots != 4:
        raise TypeError("strict T21 outer-totalistic rule is required")
    outputs = tuple(
        rule.evaluate(LocalRead(context[0], context[1:]))
        for context in product((0, 1), repeat=5)
    )
    return GeneralLookup(2, 4, outputs)


def factor_outer_totalistic(table: GeneralLookup) -> BinaryOuterTotalistic:
    """Factor only tables constant on every (Self, cardinal count) fiber."""

    if type(table) is not GeneralLookup:
        raise TypeError("general rule must be GeneralLookup")
    if table.alphabet_size != 2 or table.neighbor_slots != 4:
        raise ValueError("strict T21 general table must have 32 binary contexts")
    fibers: dict[tuple[int, int], int] = {}
    for context in product((0, 1), repeat=5):
        read = LocalRead(context[0], context[1:])
        key = (read.center, sum(read.neighbors))
        output = table.evaluate(read)
        prior = fibers.setdefault(key, output)
        if prior != output:
            raise ValueError("table is not outer-totalistic")
    if len(fibers) != 10:
        raise AssertionError("outer-totalistic fibers are incomplete")
    code = sum(
        fibers[(center, count)] << (center + 2 * count)
        for count in range(5)
        for center in (0, 1)
    )
    factored = BinaryOuterTotalistic(code, 4)
    if expand_outer_totalistic(factored) != table:
        raise AssertionError("outer-totalistic factorization was not lossless")
    return factored


def expand_totalistic(rule: BinaryTotalistic) -> GeneralLookup:
    """Losslessly expand one qualifying equal-sum six-row table."""

    if type(rule) is not BinaryTotalistic or rule.neighbor_slots != 4:
        raise TypeError("strict T21 totalistic rule is required")
    outputs = tuple(
        rule.evaluate(LocalRead(context[0], context[1:]))
        for context in product((0, 1), repeat=5)
    )
    return GeneralLookup(2, 4, outputs)


def factor_totalistic(table: GeneralLookup) -> BinaryTotalistic:
    """Factor only tables constant on every center-plus-neighbors sum fiber."""

    if type(table) is not GeneralLookup:
        raise TypeError("general rule must be GeneralLookup")
    if table.alphabet_size != 2 or table.neighbor_slots != 4:
        raise ValueError("strict T21 general table must have 32 binary contexts")
    fibers: dict[int, int] = {}
    for context in product((0, 1), repeat=5):
        read = LocalRead(context[0], context[1:])
        key = read.center + sum(read.neighbors)
        output = table.evaluate(read)
        prior = fibers.setdefault(key, output)
        if prior != output:
            raise ValueError("table is not equal-sum totalistic")
    if len(fibers) != 6:
        raise AssertionError("totalistic fibers are incomplete")
    code = sum(fibers[total] << total for total in range(6))
    factored = BinaryTotalistic(code, 4)
    if expand_totalistic(factored) != table:
        raise AssertionError("totalistic factorization was not lossless")
    return factored


@dataclass(frozen=True)
class CAProgram:
    alphabet: FiniteAlphabet
    neighborhood: LocalAccess
    rule: Rule

    def __post_init__(self) -> None:
        if type(self.alphabet) is not FiniteAlphabet:
            raise TypeError("program alphabet must be FiniteAlphabet")
        if type(self.neighborhood) is not LocalAccess:
            raise TypeError("program neighborhood must be complete LocalAccess")
        if type(self.rule) not in (BinaryOuterTotalistic, BinaryTotalistic, GeneralLookup):
            raise TypeError("program rule must be a closed local rule schema")
        if self.rule.alphabet_size != self.alphabet.size:
            raise ValueError("rule alphabet disagrees with program alphabet")
        if self.rule.neighbor_slots != self.neighborhood.slots:
            raise ValueError("rule input arity disagrees with neighborhood")


def strict_t21_program(rule: Rule) -> CAProgram:
    return CAProgram(
        FiniteAlphabet(rule.alphabet_size),
        make_local_access(ORTHOGONAL_2D, self_position=2),
        rule,
    )


def strict_t22_program(rule: Rule) -> CAProgram:
    return CAProgram(
        FiniteAlphabet(rule.alphabet_size),
        make_local_access(MOORE_2D, self_position=4),
        rule,
    )


@dataclass(frozen=True)
class SiteHandle:
    snapshot_token: SnapshotToken = field(repr=False)
    coord: Coord

    def __post_init__(self) -> None:
        if type(self.snapshot_token) is not SnapshotToken:
            raise TypeError("site handle requires an exact snapshot token")
        require_exact_tuple(self.coord, "site coordinate")
        for component in self.coord:
            require_exact_int(component, "site coordinate component")


@dataclass(frozen=True)
class SiteAssignment:
    source: SiteHandle
    target: Coord
    value: int

    def __post_init__(self) -> None:
        if type(self.source) is not SiteHandle:
            raise TypeError("assignment source must be a SiteHandle")
        require_exact_tuple(self.target, "assignment target")
        for component in self.target:
            require_exact_int(component, "assignment target component")
        require_exact_int(self.value, "assignment value")


def select_all_sites(old: GridConfiguration) -> tuple[SiteHandle, ...]:
    """Finite realization of the semantic all-sites FRONTIER."""

    if type(old) is not GridConfiguration:
        raise TypeError("old state must be GridConfiguration")
    return tuple(SiteHandle(old.snapshot_token, coord) for coord in all_coords(old.topology.shape))


def validate_handles(
    old: GridConfiguration, active: tuple[SiteHandle, ...]
) -> tuple[SiteHandle, ...]:
    raw_active = require_exact_tuple(active, "active sites")
    seen: set[Coord] = set()
    for handle in raw_active:
        if type(handle) is not SiteHandle:
            raise TypeError("active entry must be SiteHandle")
        if handle.snapshot_token is not old.snapshot_token:
            raise ValueError("stale or foreign site handle")
        coord = checked_coord(handle.coord, old.topology.dimension, "active coordinate")
        flat_index(old.topology.shape, coord)
        if coord in seen:
            raise ValueError("duplicate active site")
        seen.add(coord)
    return active


def read_local(
    old: GridConfiguration,
    active: tuple[SiteHandle, ...],
    neighborhood: LocalAccess,
) -> tuple[LocalRead, ...]:
    validate_handles(old, active)
    if type(neighborhood) is not LocalAccess:
        raise TypeError("neighborhood must be complete LocalAccess")
    if neighborhood.dimension != old.topology.dimension:
        raise ValueError("neighborhood and configuration dimensions differ")
    reads: list[LocalRead] = []
    for handle in active:
        declared_values = tuple(
            old.value_at(handle.coord)
            if type(component) is SelfAccess
            else old.value_at(add_coord(handle.coord, component.offset))
            for component in neighborhood.components
        )
        center = declared_values[neighborhood.self_position]
        neighbors = tuple(
            value
            for component, value in zip(
                neighborhood.components, declared_values, strict=True
            )
            if type(component) is OffsetAccess
        )
        reads.append(LocalRead(center, neighbors))
    return tuple(reads)


def rule_assignments(
    program: CAProgram,
    active: tuple[SiteHandle, ...],
    reads: tuple[LocalRead, ...],
) -> tuple[SiteAssignment, ...]:
    require_exact_tuple(reads, "local reads")
    if len(active) != len(reads):
        raise ValueError("active/read cardinalities differ")
    return tuple(
        SiteAssignment(handle, handle.coord, program.rule.evaluate(read))
        for handle, read in zip(active, reads, strict=True)
    )


def validate_rule_plan(
    old: GridConfiguration,
    program: CAProgram,
    active: tuple[SiteHandle, ...],
    reads: tuple[LocalRead, ...],
    writes: tuple[SiteAssignment, ...],
) -> None:
    validate_handles(old, active)
    raw_reads = require_exact_tuple(reads, "local reads")
    raw_writes = require_exact_tuple(writes, "assignments")
    if len(active) != len(raw_reads) or len(active) != len(raw_writes):
        raise ValueError("step plan cardinalities differ")
    expected_reads = read_local(old, active, program.neighborhood)
    if reads != expected_reads:
        raise ValueError("local reads were not taken from the exact old snapshot")
    for handle, read, write in zip(active, reads, writes, strict=True):
        if type(write) is not SiteAssignment:
            raise TypeError("write must be SiteAssignment")
        if write.source != handle:
            raise ValueError("write/source correspondence is invalid")
        if write.target != handle.coord:
            raise ValueError("cellular assignment must target its source site")
        old.alphabet.check(write.value, "assignment value")
        if write.value != program.rule.evaluate(read):
            raise ValueError("assignment does not match the closed rule")


def apply_parallel(
    old: GridConfiguration,
    active: tuple[SiteHandle, ...],
    writes: tuple[SiteAssignment, ...],
) -> GridConfiguration:
    """Atomic same-site commit; no write can affect another old read."""

    validate_handles(old, active)
    raw_writes = require_exact_tuple(writes, "assignments")
    if len(active) != len(raw_writes):
        raise ValueError("active/write cardinalities differ")
    next_cells = list(old.cells)
    targets: set[Coord] = set()
    for handle, write in zip(active, writes, strict=True):
        if type(write) is not SiteAssignment:
            raise TypeError("write must be SiteAssignment")
        if write.source != handle or write.source.snapshot_token is not old.snapshot_token:
            raise ValueError("assignment is stale, foreign, or reordered")
        target = checked_coord(write.target, old.topology.dimension, "assignment target")
        if target != handle.coord:
            raise ValueError("cellular assignment must be same-site")
        if target in targets:
            raise ValueError("duplicate assignment target")
        targets.add(target)
        next_cells[flat_index(old.topology.shape, target)] = old.alphabet.check(
            write.value, "assignment value"
        )
    return GridConfiguration(
        old.alphabet,
        old.topology,
        tuple(next_cells),
        SnapshotToken(old.generation + 1),
    )


def generic_ca_step(program: CAProgram, old: GridConfiguration) -> GridConfiguration:
    """Dimension- and family-agnostic CA runner used for T01/T21/T22/T23."""

    if type(program) is not CAProgram:
        raise TypeError("program must be CAProgram")
    if type(old) is not GridConfiguration:
        raise TypeError("old state must be GridConfiguration")
    if program.alphabet != old.alphabet:
        raise ValueError("program and configuration alphabets differ")
    if program.neighborhood.dimension != old.topology.dimension:
        raise ValueError("program and configuration dimensions differ")
    active = select_all_sites(old)
    reads = read_local(old, active, program.neighborhood)
    writes = rule_assignments(program, active, reads)
    validate_rule_plan(old, program, active, reads, writes)
    successor = apply_parallel(old, active, writes)
    if len(active) != old.topology.size:
        raise AssertionError("all-sites frontier was not exhaustive")
    return successor


@dataclass(frozen=True)
class Native2DState:
    """Independent row-major native representation for commutation tests."""

    alphabet_size: int
    shape: tuple[int, int]
    boundary: Boundary
    cells: Cells

    def __post_init__(self) -> None:
        alphabet = FiniteAlphabet(self.alphabet_size)
        raw_shape = require_exact_tuple(self.shape, "native shape")
        if len(raw_shape) != 2:
            raise ValueError("native T21 state must be two-dimensional")
        checked_shape = tuple(require_exact_int(n, "native shape extent") for n in raw_shape)
        if any(n <= 0 for n in checked_shape):
            raise ValueError("native shape extents must be positive")
        if type(self.boundary) not in (PeriodicBoundary, FixedBoundary):
            raise TypeError("native boundary profile is invalid")
        raw_cells = require_exact_tuple(self.cells, "native cells")
        if len(raw_cells) != checked_shape[0] * checked_shape[1]:
            raise ValueError("native cell count does not match shape")
        for value in raw_cells:
            alphabet.check(value, "native cell")
        if type(self.boundary) is FixedBoundary:
            alphabet.check(self.boundary.value, "native fixed boundary")

    def value_at(self, row: int, column: int) -> int:
        row = require_exact_int(row, "row")
        column = require_exact_int(column, "column")
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
        raise TypeError("generic state must be a two-dimensional grid configuration")
    shape = state.topology.shape
    return Native2DState(
        state.alphabet.size,
        (shape[0], shape[1]),
        state.topology.boundary,
        state.cells,
    )


def native_book_context(
    old: Native2DState, row: int, column: int
) -> tuple[int, int, int, int, int]:
    """Literal BOOK row/column positions: (-1,0),(0,-1),Self,(0,1),(1,0)."""

    if type(old) is not Native2DState:
        raise TypeError("native state must be Native2DState")
    row = require_exact_int(row, "row")
    column = require_exact_int(column, "column")
    return (
        old.value_at(row - 1, column),
        old.value_at(row, column - 1),
        old.value_at(row, column),
        old.value_at(row, column + 1),
        old.value_at(row + 1, column),
    )


def native_book_general_step(code: int, old: Native2DState) -> Native2DState:
    """Independent 32-context evaluator using the literal BOOK bit formula."""

    checked = require_exact_int(code, "native general code")
    if checked < 0 or checked >= 1 << 32:
        raise ValueError("native general code is out of range")
    if old.alphabet_size != 2:
        raise ValueError("native general code requires the binary alphabet")
    values: list[int] = []
    for row in range(old.shape[0]):
        for column in range(old.shape[1]):
            negative_0, negative_1, center, positive_1, positive_0 = (
                native_book_context(old, row, column)
            )
            index = (
                16 * negative_0
                + 8 * negative_1
                + 4 * center
                + 2 * positive_1
                + positive_0
            )
            values.append((checked >> index) & 1)
    return Native2DState(2, old.shape, old.boundary, tuple(values))


def native_book_outer_step(code: int, old: Native2DState) -> Native2DState:
    """Independent Self+2*cardinal-count evaluator for the ten-row form."""

    checked = require_exact_int(code, "native outer-totalistic code")
    if checked < 0 or checked >= 1 << 10:
        raise ValueError("native outer-totalistic code is out of range")
    if old.alphabet_size != 2:
        raise ValueError("native outer-totalistic code requires binary cells")
    values: list[int] = []
    for row in range(old.shape[0]):
        for column in range(old.shape[1]):
            negative_0, negative_1, center, positive_1, positive_0 = (
                native_book_context(old, row, column)
            )
            cardinal_count = negative_0 + negative_1 + positive_1 + positive_0
            values.append((checked >> (center + 2 * cardinal_count)) & 1)
    return Native2DState(2, old.shape, old.boundary, tuple(values))


def native_book_totalistic_step(code: int, old: Native2DState) -> Native2DState:
    """Independent equal-sum evaluator for the six-row BOOK:2922 form."""

    checked = require_exact_int(code, "native totalistic code")
    if checked < 0 or checked >= 1 << 6:
        raise ValueError("native totalistic code is out of range")
    if old.alphabet_size != 2:
        raise ValueError("native totalistic code requires binary cells")
    values: list[int] = []
    for row in range(old.shape[0]):
        for column in range(old.shape[1]):
            total = sum(native_book_context(old, row, column))
            values.append((checked >> total) & 1)
    return Native2DState(2, old.shape, old.boundary, tuple(values))


def native_book_projection_step(
    sorted_position: int, old: Native2DState
) -> Native2DState:
    """Independent finite-alphabet projection used by positional guards."""

    selected = require_exact_int(sorted_position, "native sorted position")
    if selected < 0 or selected >= 5:
        raise ValueError("native sorted position is out of range")
    values = tuple(
        native_book_context(old, row, column)[selected]
        for row in range(old.shape[0])
        for column in range(old.shape[1])
    )
    return Native2DState(old.alphabet_size, old.shape, old.boundary, values)


def native_row_column_to_enu_grid(
    state: Native2DState, generation: int = 0
) -> GridConfiguration:
    """Map a finite row/column realization through x=column,y=-row.

    The added y translation by rows-1 only keeps finite array indices
    nonnegative; it does not alter the declared linear basis map.
    """

    if type(state) is not Native2DState:
        raise TypeError("native state must be Native2DState")
    generation = require_exact_int(generation, "generation")
    rows, columns = state.shape
    runtime_shape = (columns, rows)
    runtime_cells = [0] * (rows * columns)
    for row in range(rows):
        for column in range(columns):
            runtime_coord = (column, rows - 1 - row)
            runtime_cells[flat_index(runtime_shape, runtime_coord)] = state.value_at(row, column)
    return GridConfiguration(
        FiniteAlphabet(state.alphabet_size),
        FiniteGrid(runtime_shape, state.boundary),
        tuple(runtime_cells),
        SnapshotToken(generation),
    )


@dataclass(frozen=True)
class SparseLatticeField:
    """Complete Z^d field: uniform background plus finite deviations."""

    alphabet: FiniteAlphabet
    dimension: int
    background: int
    entries: tuple[tuple[Coord, int], ...]
    generation: int = 0

    def __post_init__(self) -> None:
        if type(self.alphabet) is not FiniteAlphabet:
            raise TypeError("sparse field alphabet must be FiniteAlphabet")
        dimension = require_exact_int(self.dimension, "field dimension")
        if dimension <= 0:
            raise ValueError("field dimension must be positive")
        self.alphabet.check(self.background, "field background")
        raw_entries = require_exact_tuple(self.entries, "field entries")
        seen: set[Coord] = set()
        previous: Coord | None = None
        for raw_entry in raw_entries:
            entry = require_exact_tuple(raw_entry, "field entry")
            if len(entry) != 2:
                raise ValueError("field entry must be (coordinate, value)")
            coord = checked_coord(entry[0], dimension, "field coordinate")
            value = self.alphabet.check(entry[1], "field value")
            if value == self.background:
                raise ValueError("sparse entries must differ from the background")
            if coord in seen:
                raise ValueError("duplicate sparse coordinate")
            if previous is not None and coord <= previous:
                raise ValueError("sparse entries must be in canonical coordinate order")
            seen.add(coord)
            previous = coord
        generation = require_exact_int(self.generation, "field generation")
        if generation < 0:
            raise ValueError("field generation must be nonnegative")

    def value_at(self, raw_coord: object) -> int:
        coord = checked_coord(raw_coord, self.dimension, "field coordinate")
        # The test universes are deliberately small; a tuple lookup makes the
        # canonical, fully inspectable representation more important than speed.
        for stored_coord, value in self.entries:
            if stored_coord == coord:
                return value
        return self.background


def make_sparse_field(
    alphabet_size: int,
    dimension: int,
    background: int,
    entries: tuple[tuple[Coord, int], ...],
    generation: int = 0,
) -> SparseLatticeField:
    checked_entries = require_exact_tuple(entries, "field entries")
    normalized = tuple(sorted(checked_entries, key=lambda item: item[0]))
    return SparseLatticeField(
        FiniteAlphabet(alphabet_size), dimension, background, normalized, generation
    )


def sparse_read(
    program: CAProgram, field_state: SparseLatticeField, coord: Coord
) -> LocalRead:
    if program.neighborhood.dimension != field_state.dimension:
        raise ValueError("program and infinite field dimensions differ")
    checked = checked_coord(coord, field_state.dimension)
    declared_values = tuple(
        field_state.value_at(checked)
        if type(component) is SelfAccess
        else field_state.value_at(add_coord(checked, component.offset))
        for component in program.neighborhood.components
    )
    return LocalRead(
        declared_values[program.neighborhood.self_position],
        tuple(
            value
            for component, value in zip(
                program.neighborhood.components, declared_values, strict=True
            )
            if type(component) is OffsetAccess
        ),
    )


def sparse_lattice_step(
    program: CAProgram, old: SparseLatticeField
) -> SparseLatticeField:
    """Exact all-Z^d step for a uniform background plus finite deviations."""

    if program.alphabet != old.alphabet:
        raise ValueError("program and infinite field alphabets differ")
    if program.neighborhood.dimension != old.dimension:
        raise ValueError("program and infinite field dimensions differ")
    uniform_read = LocalRead(
        old.background, tuple(old.background for _ in program.neighborhood.offsets)
    )
    next_background = program.rule.evaluate(uniform_read)

    # A target can differ from the next uniform background only if its center
    # or one of its input positions is an old deviation.  This is an exact
    # finite dependency reduction, not a finite boundary condition.
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
    return SparseLatticeField(
        old.alphabet,
        old.dimension,
        next_background,
        next_entries,
        old.generation + 1,
    )


def fixed_background_sparse_step(
    program: CAProgram, old: SparseLatticeField
) -> SparseLatticeField:
    """Lowering for storage whose implicit background value cannot change."""

    if program.alphabet != old.alphabet:
        raise ValueError("program and sparse storage alphabets differ")
    uniform = LocalRead(
        old.background, tuple(old.background for _ in program.neighborhood.offsets)
    )
    if program.rule.evaluate(uniform) != old.background:
        raise ValueError("fixed-background sparse lowering requires quiescence proof")
    successor = sparse_lattice_step(program, old)
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
    except Exception as exc:  # pragma: no cover - diagnostic path
        raise AssertionError(f"expected {error.__name__}, got {type(exc).__name__}") from exc
    raise AssertionError(f"expected {error.__name__}")


def outer_code(slots: int, predicate: object) -> int:
    slots = require_exact_int(slots, "neighbor slot count")
    if not callable(predicate):
        raise TypeError("predicate must be callable in this oracle helper")
    code = 0
    for count in range(slots + 1):
        for center in (0, 1):
            output = predicate(center, count)
            if type(output) is not int or output not in (0, 1):
                raise TypeError("oracle predicate must return an exact bit")
            code |= output << (2 * count + center)
    return code


def cells_with_one(shape: tuple[int, ...], coord: Coord, alphabet_size: int = 2) -> Cells:
    result = [0] * prod(shape)
    result[flat_index(shape, coord)] = 1
    FiniteAlphabet(alphabet_size)
    return tuple(result)


def nonzero_coords(state: GridConfiguration) -> tuple[Coord, ...]:
    return tuple(
        coord
        for coord in all_coords(state.topology.shape)
        if state.cells[flat_index(state.topology.shape, coord)] != 0
    )


def assert_book_codes_and_counts() -> None:
    """Freeze the exact Chapter 5/Notes counts and two direct rule codes."""

    # BOOK:2174-2190 and BOOK:13536-13549.  With four surrounding cells,
    # outer totalism has 2*(4+1)=10 binary rows and ordinary totalism over
    # center plus neighbors has 6 possible sums.
    assert 1 << 10 == 1024
    assert 1 << 6 == 64
    assert 1 << 32 == 4_294_967_296
    assert 1 << 12 == 4096

    # The T22 Moore boundary has eight surrounding cells.  BOOK:13542-13549
    # gives the corresponding 9-neighbor counts.
    assert 1 << 18 == 262_144
    assert 1 << 10 == 1024
    assert (1 << 512).bit_length() == 513

    code_1022 = outer_code(4, lambda center, count: 1 if center == 1 or count > 0 else 0)
    code_942 = outer_code(
        4, lambda center, count: 1 if count in (1, 4) else center
    )
    assert code_1022 == 1022
    assert code_942 == 942

    rule_1022 = BinaryOuterTotalistic(1022, 4)
    rule_942 = BinaryOuterTotalistic(942, 4)
    for center in (0, 1):
        for count in range(5):
            neighbors = (1,) * count + (0,) * (4 - count)
            assert rule_1022.evaluate(LocalRead(center, neighbors)) == (
                1 if center == 1 or count > 0 else 0
            )
            assert rule_942.evaluate(LocalRead(center, neighbors)) == (
                1 if count in (1, 4) else center
            )


def assert_strict_local_form_roundtrips() -> dict[str, int]:
    """Close general, outer-totalistic, and equal-sum representations."""

    assert STRICT_T21_SORTED_INPUTS == tuple(sorted(STRICT_T21_SORTED_INPUTS))
    assert STRICT_T21_SORTED_INPUTS == (
        (-1, 0),
        (0, -1),
        (0, 0),
        (0, 1),
        (1, 0),
    )

    # Zero/full plus every one-hot digit prove the 32-bit positional codec;
    # the directional projection supplies an asymmetric multi-bit guard.
    asymmetric = projection_rule(2, 4, 0)  # raw (-1,0), not a compass assumption
    asymmetric_code = strict_t21_general_to_code(asymmetric)
    projection_tables = (
        projection_rule(2, 4, 0),
        projection_rule(2, 4, 1),
        projection_rule(2, 4, -1),
        projection_rule(2, 4, 2),
        projection_rule(2, 4, 3),
    )
    assert tuple(strict_t21_general_to_code(table) for table in projection_tables) == (
        0xFFFF0000,
        0xFF00FF00,
        0xF0F0F0F0,
        0xCCCCCCCC,
        0xAAAAAAAA,
    )
    general_codes = {0, (1 << 32) - 1, asymmetric_code}
    general_codes.update(1 << index for index in range(32))
    for code in general_codes:
        decoded = strict_t21_general_from_code(code)
        assert strict_t21_general_to_code(decoded) == code
        assert strict_t21_general_from_code(strict_t21_general_to_code(decoded)) == decoded

    outer_cases = 0
    for code in range(1 << 10):
        compact = BinaryOuterTotalistic(code, 4)
        exhaustive = expand_outer_totalistic(compact)
        assert len(exhaustive.outputs) == 32
        assert factor_outer_totalistic(exhaustive) == compact
        assert expand_outer_totalistic(factor_outer_totalistic(exhaustive)) == exhaustive
        assert strict_t21_general_from_code(strict_t21_general_to_code(exhaustive)) == exhaustive
        outer_cases += 1

    totalistic_cases = 0
    for code in range(1 << 6):
        compact = BinaryTotalistic(code, 4)
        exhaustive = expand_totalistic(compact)
        assert len(exhaustive.outputs) == 32
        assert factor_totalistic(exhaustive) == compact
        assert expand_totalistic(factor_totalistic(exhaustive)) == exhaustive
        assert strict_t21_general_from_code(strict_t21_general_to_code(exhaustive)) == exhaustive
        totalistic_cases += 1

    # Quotient adversary 1: raw (-1,0)-only and (+1,0)-only contexts have the
    # same cardinal count, yet an asymmetric exhaustive table distinguishes
    # them.  Outer-totalistic compression must reject rather than lose it.
    negative_axis_0_only = LocalRead(0, (1, 0, 0, 0))
    positive_axis_0_only = LocalRead(0, (0, 0, 0, 1))
    assert sum(negative_axis_0_only.neighbors) == sum(positive_axis_0_only.neighbors) == 1
    assert asymmetric.evaluate(negative_axis_0_only) == 1
    assert asymmetric.evaluate(positive_axis_0_only) == 0
    expect_raises(ValueError, lambda: factor_outer_totalistic(asymmetric))

    # Quotient adversary 2: (Self=1,count=0) and (Self=0,count=1) collide under
    # the five-cell sum but are distinct in Self x CardinalCount.  A center
    # projection is a valid outer table and an invalid equal-sum table.
    center_projection = projection_rule(2, 4, -1)
    self_one_count_zero = LocalRead(1, (0, 0, 0, 0))
    self_zero_count_one = LocalRead(0, (1, 0, 0, 0))
    assert self_one_count_zero.center + sum(self_one_count_zero.neighbors) == 1
    assert self_zero_count_one.center + sum(self_zero_count_one.neighbors) == 1
    assert center_projection.evaluate(self_one_count_zero) == 1
    assert center_projection.evaluate(self_zero_count_one) == 0
    assert expand_outer_totalistic(factor_outer_totalistic(center_projection)) == center_projection
    expect_raises(ValueError, lambda: factor_totalistic(center_projection))

    # One changed positional row is sufficient to invalidate a formerly
    # qualifying factorization; qualification inspects all 32 rows.
    valid = expand_outer_totalistic(BinaryOuterTotalistic(942, 4))
    outputs = list(valid.outputs)
    outputs[8] = 1 - outputs[8]
    tampered = GeneralLookup(2, 4, tuple(outputs))
    expect_raises(ValueError, lambda: factor_outer_totalistic(tampered))

    assert outer_cases == 1024 and totalistic_cases == 64
    assert len(general_codes) == 35
    return {
        "general_codec": len(general_codes),
        "outer_factor": outer_cases,
        "totalistic_factor": totalistic_cases,
    }


def assert_book_to_runtime_basis_permutation() -> int:
    """Prove the row/column -> ENU basis and table permutation commute."""

    transformed, runtime_sorted, runtime_to_book, book_to_runtime = basis_permutations()
    assert transformed == (
        (0, 1),
        (-1, 0),
        (0, 0),
        (1, 0),
        (0, -1),
    )
    assert runtime_sorted == (
        (-1, 0),
        (0, -1),
        (0, 0),
        (0, 1),
        (1, 0),
    )
    assert runtime_to_book == (1, 4, 2, 0, 3)
    assert book_to_runtime == (3, 0, 2, 4, 1)

    expected_runtime_projection_codes = (
        0xCCCCCCCC,
        0xFFFF0000,
        0xF0F0F0F0,
        0xAAAAAAAA,
        0xFF00FF00,
    )
    assert tuple(
        permute_book_code_to_runtime(code) for code in BOOK_GENERAL_PROJECTION_CODES
    ) == expected_runtime_projection_codes
    assert tuple(
        permute_runtime_code_to_book(code) for code in expected_runtime_projection_codes
    ) == BOOK_GENERAL_PROJECTION_CODES

    permutation_cases = 0
    for book_code in BOOK_GENERAL_PROJECTION_CODES:
        runtime_code = permute_book_code_to_runtime(book_code)
        assert permute_runtime_code_to_book(runtime_code) == book_code
        for runtime_context in product((0, 1), repeat=5):
            book_context = runtime_context_to_book_context(runtime_context)
            assert book_context_to_runtime_context(book_context) == runtime_context
            book_output = (
                book_code >> binary_digits_to_index(book_context)
            ) & 1
            runtime_output = (
                runtime_code >> binary_digits_to_index(runtime_context)
            ) & 1
            assert runtime_output == book_output
            permutation_cases += 1

    # Naively reusing the BOOK code after lexicographically sorting the ENU
    # positions silently changes north projection into west projection.
    book_north_code = BOOK_GENERAL_PROJECTION_CODES[0]
    runtime_north_code = permute_book_code_to_runtime(book_north_code)
    runtime_context = (0, 0, 0, 1, 0)  # W,S,Self,N,E in lex ENU order
    book_context = runtime_context_to_book_context(runtime_context)
    assert book_context == (1, 0, 0, 0, 0)
    direct_output = (
        book_north_code >> binary_digits_to_index(book_context)
    ) & 1
    naive_output = (
        book_north_code >> binary_digits_to_index(runtime_context)
    ) & 1
    certified_output = (
        runtime_north_code >> binary_digits_to_index(runtime_context)
    ) & 1
    assert (direct_output, naive_output, certified_output) == (1, 0, 1)
    assert runtime_north_code == 0xCCCCCCCC

    # The same distinction is visible in a complete non-aliasing 5x5 step.
    native = Native2DState(
        2,
        (5, 5),
        FixedBoundary(0),
        cells_with_one((5, 5), (2, 2)),
    )
    native_next = native_book_general_step(book_north_code, native)
    runtime_old = native_row_column_to_enu_grid(native)
    certified_program = strict_t21_program(
        strict_t21_general_from_code(runtime_north_code)
    )
    naive_program = strict_t21_program(strict_t21_general_from_code(book_north_code))
    certified_next = generic_ca_step(certified_program, runtime_old)
    naive_next = generic_ca_step(naive_program, runtime_old)
    expected_runtime_next = native_row_column_to_enu_grid(native_next, generation=1)
    assert certified_next == expected_runtime_next
    assert naive_next != expected_runtime_next
    assert nonzero_coords(certified_next) == ((2, 1),)
    assert nonzero_coords(naive_next) == ((3, 2),)

    assert permutation_cases == 160
    return permutation_cases


def assert_exhaustive_native_commutation() -> dict[str, int]:
    """Prove e(step_native(x)) = step_generic(e(x)) on bounded universes."""

    binary_states = tuple(product((0, 1), repeat=4))
    periodic = PeriodicBoundary()
    outer_cases = 0
    totalistic_cases = 0
    positional_cases = 0
    general_basis_cases = 0
    nonaliasing_directional_cases = 0
    ternary_cases = 0

    # All 1024 four-neighbor binary outer-totalistic tables and every binary
    # 2x2 torus.  A 2x2 torus is intentionally adversarial: opposite offsets
    # resolve to the same cell but remain separate read slots.
    for code in range(1 << 10):
        program = strict_t21_program(BinaryOuterTotalistic(code, 4))
        for cells in binary_states:
            native = Native2DState(2, (2, 2), periodic, cells)
            encoded = encode_native(native, generation=7)
            direct = native_book_outer_step(code, native)
            generic = generic_ca_step(program, encoded)
            assert decode_generic(generic) == direct
            assert generic.snapshot_token is not encoded.snapshot_token
            assert generic.generation == 8
            assert decode_generic(encode_native(decode_generic(encoded))) == native
            outer_cases += 1

    # All 64 equal-weight five-cell totalistic tables on the same state space.
    for code in range(1 << 6):
        program = strict_t21_program(BinaryTotalistic(code, 4))
        for cells in binary_states:
            native = Native2DState(2, (2, 2), periodic, cells)
            direct = native_book_totalistic_step(code, native)
            generic = generic_ca_step(program, encode_native(native))
            assert decode_generic(generic) == direct
            totalistic_cases += 1

    # Every one-hot row of the full 32-context code is exercised at the
    # center of a non-aliasing 5x5 native configuration; zero and full tables
    # guard both endpoints.  This tests the direct numeric evaluator beyond
    # the five projection patterns.
    general_basis_codes = (0, (1 << 32) - 1, *(1 << index for index in range(32)))
    for code in general_basis_codes:
        active_index = code.bit_length() - 1 if code and code != (1 << 32) - 1 else 0
        context = tuple((active_index >> shift) & 1 for shift in (4, 3, 2, 1, 0))
        literal_positions = ((1, 2), (2, 1), (2, 2), (2, 3), (3, 2))
        native_cells = [0] * 25
        for coord, value in zip(literal_positions, context, strict=True):
            native_cells[flat_index((5, 5), coord)] = value
        native = Native2DState(2, (5, 5), FixedBoundary(0), tuple(native_cells))
        direct = native_book_general_step(code, native)
        generic = generic_ca_step(
            strict_t21_program(strict_t21_general_from_code(code)),
            encode_native(native),
        )
        assert decode_generic(generic) == direct
        if code not in (0, (1 << 32) - 1):
            assert direct.value_at(2, 2) == 1
        general_basis_cases += 1

    # Totalistic tests cannot catch an offset-order reversal.  Each center or
    # directional projection is therefore checked against every 2x2 state.
    local_to_sorted = {0: 0, 1: 1, -1: 2, 2: 3, 3: 4}
    assert tuple(BOOK_GENERAL_PROJECTION_CODES) == (
        0xFFFF0000,
        0xFF00FF00,
        0xF0F0F0F0,
        0xCCCCCCCC,
        0xAAAAAAAA,
    )
    for selected in (-1, 0, 1, 2, 3):
        sorted_position = local_to_sorted[selected]
        code = BOOK_GENERAL_PROJECTION_CODES[sorted_position]
        program = strict_t21_program(strict_t21_general_from_code(code))
        for cells in binary_states:
            native = Native2DState(2, (2, 2), periodic, cells)
            direct = native_book_general_step(code, native)
            generic = generic_ca_step(program, encode_native(native))
            assert decode_generic(generic) == direct
            positional_cases += 1

    # A 5x5 fixed box prevents opposite directions from aliasing.  Every
    # literal BOOK projection is checked from every one-hot source location
    # against the independent numeric-code evaluator.
    for sorted_position, code in enumerate(BOOK_GENERAL_PROJECTION_CODES):
        program = strict_t21_program(strict_t21_general_from_code(code))
        for seed in all_coords((5, 5)):
            native = Native2DState(
                2,
                (5, 5),
                FixedBoundary(0),
                cells_with_one((5, 5), seed),
            )
            direct = native_book_general_step(code, native)
            generic = generic_ca_step(program, encode_native(native))
            assert decode_generic(generic) == direct
            # The independent projection helper is a second direct guard on
            # the pinned code significance.
            assert direct == native_book_projection_step(sorted_position, native)
            nonaliasing_directional_cases += 1

    # Finite alphabet is an axis, not a binary/T21 executor assumption.
    ternary_program = strict_t21_program(projection_rule(3, 4, 2))
    for cells in product(range(3), repeat=4):
        native = Native2DState(3, (2, 2), periodic, cells)
        direct = native_book_projection_step(3, native)
        generic = generic_ca_step(ternary_program, encode_native(native))
        assert decode_generic(generic) == direct
        ternary_cases += 1

    assert outer_cases == 16_384
    assert totalistic_cases == 1_024
    assert positional_cases == 80
    assert general_basis_cases == 34
    assert nonaliasing_directional_cases == 125
    assert ternary_cases == 81
    return {
        "outer": outer_cases,
        "totalistic": totalistic_cases,
        "positional": positional_cases,
        "general_basis": general_basis_cases,
        "nonaliasing_directional": nonaliasing_directional_cases,
        "ternary": ternary_cases,
    }


def assert_wrapped_slot_multiplicity() -> None:
    """Periodic aliasing must not deduplicate neighborhood occurrences."""

    topology = FiniteGrid((2, 2), PeriodicBoundary())
    old = GridConfiguration(
        FiniteAlphabet(2),
        topology,
        cells_with_one((2, 2), (1, 0)),
        SnapshotToken(0),
    )
    handle = SiteHandle(old.snapshot_token, (0, 0))
    neighborhood = make_local_access(ORTHOGONAL_2D, self_position=2)
    read = read_local(old, (handle,), neighborhood)[0]
    assert read == LocalRead(0, (1, 0, 0, 1))

    resolved = tuple(
        tuple(
            component % extent
            for component, extent in zip(
                add_coord(handle.coord, offset), topology.shape, strict=True
            )
        )
        for offset in ORTHOGONAL_2D
    )
    assert len(resolved) == 4 and len(set(resolved)) == 2

    # Code 4 accepts exactly total sum 2.  Retaining N and S as separate slots
    # yields 1; a wrong resolved-coordinate deduplication would yield sum 1.
    program = strict_t21_program(BinaryTotalistic(1 << 2, 4))
    successor = generic_ca_step(program, old)
    assert successor.value_at((0, 0)) == 1
    wrong_deduplicated_sum = old.value_at((0, 0)) + sum(
        old.value_at(coord) for coord in set(resolved)
    )
    assert wrong_deduplicated_sum == 1
    assert ((1 << 2) >> wrong_deduplicated_sum) & 1 == 0


def assert_asymmetric_orientation_and_parallelism() -> None:
    fixed = FixedBoundary(0)
    shape = (5, 5)
    seed = (2, 2)
    old = GridConfiguration(
        FiniteAlphabet(2), FiniteGrid(shape, fixed), cells_with_one(shape, seed), SnapshotToken(0)
    )

    for slot, offset in enumerate(ORTHOGONAL_2D):
        program = strict_t21_program(projection_rule(2, 4, slot))
        successor = generic_ca_step(program, old)
        expected = subtract_coord(seed, offset)
        assert nonzero_coords(successor) == (expected,)

    negative_axis_1 = strict_t21_program(projection_rule(2, 4, 1))
    positive_axis_1 = strict_t21_program(projection_rule(2, 4, 2))
    assert nonzero_coords(generic_ca_step(negative_axis_1, old)) == ((2, 3),)
    assert nonzero_coords(generic_ca_step(positive_axis_1, old)) == ((2, 1),)

    # A left-to-right in-place update loses the old black value before the
    # next site reads it.  The generic old-snapshot commit correctly shifts it.
    line_shape = (1, 4)
    line_old = GridConfiguration(
        FiniteAlphabet(2),
        FiniteGrid(line_shape, fixed),
        cells_with_one(line_shape, (0, 0)),
        SnapshotToken(4),
    )
    parallel = generic_ca_step(negative_axis_1, line_old)
    assert parallel.cells == (0, 1, 0, 0)

    in_place = list(line_old.cells)
    for column in range(4):
        negative_neighbor = 0 if column == 0 else in_place[column - 1]
        # Under the explicitly declared row/column isomorphism, slot 1 is
        # west.  The raw semantic identity remains offset (0,-1).
        in_place[column] = negative_axis_1.rule.evaluate(
            LocalRead(in_place[column], (0, negative_neighbor, 0, 0))
        )
    assert tuple(in_place) == (0, 0, 0, 0)
    assert tuple(in_place) != parallel.cells


def assert_boundary_and_support_separation() -> None:
    """Finite edge policies are realization data, not native Z^2 semantics."""

    program = strict_t21_program(projection_rule(2, 4, 1))  # read raw (0,-1)
    shape = (3, 3)
    edge_seed = cells_with_one(shape, (1, 2))
    periodic = GridConfiguration(
        FiniteAlphabet(2), FiniteGrid(shape, PeriodicBoundary()), edge_seed, SnapshotToken(0)
    )
    fixed = GridConfiguration(
        FiniteAlphabet(2), FiniteGrid(shape, FixedBoundary(0)), edge_seed, SnapshotToken(0)
    )
    assert nonzero_coords(generic_ca_step(program, periodic)) == ((1, 0),)
    assert nonzero_coords(generic_ca_step(program, fixed)) == ()

    interior_seed = cells_with_one(shape, (1, 1))
    periodic_interior = GridConfiguration(
        FiniteAlphabet(2),
        FiniteGrid(shape, PeriodicBoundary()),
        interior_seed,
        SnapshotToken(0),
    )
    fixed_interior = GridConfiguration(
        FiniteAlphabet(2),
        FiniteGrid(shape, FixedBoundary(0)),
        interior_seed,
        SnapshotToken(0),
    )
    assert nonzero_coords(generic_ca_step(program, periodic_interior)) == ((1, 2),)
    assert nonzero_coords(generic_ca_step(program, fixed_interior)) == ((1, 2),)


def axis_offsets(dimension: int) -> tuple[Offset, ...]:
    dimension = require_exact_int(dimension, "dimension")
    if dimension <= 0:
        raise ValueError("dimension must be positive")
    offsets: list[Offset] = []
    for axis in range(dimension):
        negative = [0] * dimension
        positive = [0] * dimension
        negative[axis] = -1
        positive[axis] = 1
        offsets.extend((tuple(negative), tuple(positive)))
    return tuple(offsets)


def assert_dimension_agnostic_kernel() -> None:
    """One runner executes t+1D, t+2D, and t+3D parameterizations."""

    for dimension in (1, 2, 3):
        offsets = axis_offsets(dimension)
        program = CAProgram(
            FiniteAlphabet(2),
            make_local_access(offsets, self_position=0),
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
        successor = generic_ca_step(program, old)
        expected = subtract_coord(seed, offsets[0])
        assert nonzero_coords(successor) == (expected,)


def assert_exact_infinite_support() -> None:
    """Check native Z^2 evolution without inventing a finite boundary."""

    growth = strict_t21_program(BinaryOuterTotalistic(1022, 4))
    state = make_sparse_field(2, 2, 0, (((0, 0), 1),))
    expected_counts = (1, 5, 13, 25, 41, 61, 85)
    for time, expected_count in enumerate(expected_counts):
        expected_support = {
            (row, column)
            for row in range(-time, time + 1)
            for column in range(-time, time + 1)
            if abs(row) + abs(column) <= time
        }
        assert state.background == 0
        assert {coord for coord, value in state.entries if value == 1} == expected_support
        assert len(state.entries) == expected_count == 1 + 2 * time * (time + 1)
        state = sparse_lattice_step(growth, state)

    # A non-quiescent uniform background is still a valid complete Z^2 state.
    # The transparent background field changes value; no finite edge or giant
    # explicit array is needed.
    nonquiescent = strict_t21_program(BinaryOuterTotalistic(1, 4))
    uniform_white = make_sparse_field(2, 2, 0, ())
    expect_raises(
        ValueError,
        lambda: fixed_background_sparse_step(nonquiescent, uniform_white),
    )
    uniform_black = sparse_lattice_step(nonquiescent, uniform_white)
    assert uniform_black.background == 1 and uniform_black.entries == ()
    back_to_white = sparse_lattice_step(nonquiescent, uniform_black)
    assert back_to_white.background == 0 and back_to_white.entries == ()
    quiescent_seed = make_sparse_field(2, 2, 0, (((0, 0), 1),))
    assert fixed_background_sparse_step(growth, quiescent_seed) == sparse_lattice_step(
        growth, quiescent_seed
    )

    # Exact finite-horizon dependency along raw axis 1: with (0,-1)
    # projection, a source two negative-axis cells away reaches the origin in
    # two steps; one three cells away does not.
    negative_axis_1 = strict_t21_program(projection_rule(2, 4, 1))
    empty = make_sparse_field(2, 2, 0, ())
    outside_halo = make_sparse_field(2, 2, 0, (((0, -3), 1),))
    on_halo = make_sparse_field(2, 2, 0, (((0, -2), 1),))
    for _ in range(2):
        empty = sparse_lattice_step(negative_axis_1, empty)
        outside_halo = sparse_lattice_step(negative_axis_1, outside_halo)
        on_halo = sparse_lattice_step(negative_axis_1, on_halo)
    assert empty.value_at((0, 0)) == outside_halo.value_at((0, 0)) == 0
    assert on_halo.value_at((0, 0)) == 1

    # Translation covariance is a support/topology property, not a renderer.
    shift = (7, -4)
    original = make_sparse_field(2, 2, 0, (((0, 0), 1), ((1, 0), 1)))
    translated = make_sparse_field(
        2,
        2,
        0,
        tuple((add_coord(coord, shift), value) for coord, value in original.entries),
    )
    original_next = sparse_lattice_step(growth, original)
    translated_next = sparse_lattice_step(growth, translated)
    assert translated_next.background == original_next.background
    assert translated_next.entries == tuple(
        (add_coord(coord, shift), value) for coord, value in original_next.entries
    )


def assert_t22_moore_boundary() -> None:
    """Diagonal access changes the preset, not the execution algebra."""

    shape = (3, 3)
    old = GridConfiguration(
        FiniteAlphabet(2),
        FiniteGrid(shape, FixedBoundary(0)),
        cells_with_one(shape, (0, 0)),
        SnapshotToken(0),
    )
    moore = strict_t22_program(projection_rule(2, 8, 0))  # raw (-1,-1)
    orthogonal = strict_t21_program(projection_rule(2, 4, 0))  # raw (-1,0)
    assert generic_ca_step(moore, old).value_at((1, 1)) == 1
    assert generic_ca_step(orthogonal, old).value_at((1, 1)) == 0
    assert moore.neighborhood.offsets == MOORE_2D
    assert orthogonal.neighborhood.offsets == ORTHOGONAL_2D

    # Both use precisely the same all-sites/read/rule/parallel-update runner.
    assert type(generic_ca_step(moore, old)) is GridConfiguration
    assert type(generic_ca_step(orthogonal, old)) is GridConfiguration


def assert_hostile_validation() -> None:
    """Reject coercion, malformed schemas, stale scope, and tampered plans."""

    expect_raises(TypeError, lambda: FiniteAlphabet(True))
    expect_raises(ValueError, lambda: FiniteAlphabet(1))
    expect_raises(TypeError, lambda: FixedBoundary(False))
    expect_raises(TypeError, lambda: FiniteGrid([2, 2], PeriodicBoundary()))
    expect_raises(TypeError, lambda: FiniteGrid((2, True), PeriodicBoundary()))
    expect_raises(ValueError, lambda: FiniteGrid((2, 0), PeriodicBoundary()))
    expect_raises(TypeError, lambda: FiniteGrid((2, 2), object()))
    expect_raises(TypeError, lambda: SnapshotToken(True))
    expect_raises(ValueError, lambda: SnapshotToken(-1))

    alphabet = FiniteAlphabet(2)
    topology = FiniteGrid((2, 2), FixedBoundary(0))
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
    expect_raises(
        ValueError,
        lambda: GridConfiguration(alphabet, topology, (0, 0, 2, 0), SnapshotToken(0)),
    )

    expect_raises(TypeError, lambda: make_local_access([NEG_AXIS_0, POS_AXIS_0], 1))
    expect_raises(ValueError, lambda: make_local_access(((0, 0), NEG_AXIS_0), 1))
    expect_raises(ValueError, lambda: make_local_access((NEG_AXIS_0, NEG_AXIS_0), 1))
    expect_raises(ValueError, lambda: make_local_access(((-1,), POS_AXIS_0), 1))
    expect_raises(TypeError, lambda: make_local_access(((-1, False), POS_AXIS_0), 1))
    expect_raises(ValueError, lambda: LocalAccess((OffsetAccess(NEG_AXIS_0),)))
    expect_raises(ValueError, lambda: LocalAccess((SelfAccess(), SelfAccess(), OffsetAccess(NEG_AXIS_0))))
    expect_raises(TypeError, lambda: LocalAccess((SelfAccess(), object())))
    expect_raises(TypeError, lambda: make_local_access((NEG_AXIS_0,), True))
    expect_raises(TypeError, lambda: LocalAccess([SelfAccess(), OffsetAccess(NEG_AXIS_0)]))
    expect_raises(TypeError, lambda: BinaryOuterTotalistic(True, 4))
    expect_raises(ValueError, lambda: BinaryOuterTotalistic(1024, 4))
    expect_raises(TypeError, lambda: BinaryTotalistic(False, 4))
    expect_raises(ValueError, lambda: BinaryTotalistic(64, 4))
    expect_raises(TypeError, lambda: GeneralLookup(2, 1, [0, 1, 0, 1]))
    expect_raises(ValueError, lambda: GeneralLookup(2, 1, (0, 1)))
    expect_raises(TypeError, lambda: GeneralLookup(2, 1, (0, 1, 0, False)))
    expect_raises(TypeError, lambda: projection_rule(2, 4, True))
    expect_raises(ValueError, lambda: projection_rule(2, 4, 4))
    expect_raises(TypeError, lambda: strict_t21_general_from_code(True))
    expect_raises(ValueError, lambda: strict_t21_general_from_code(1 << 32))
    expect_raises(TypeError, lambda: strict_t21_general_to_code(BinaryTotalistic(0, 4)))
    expect_raises(TypeError, lambda: factor_outer_totalistic(BinaryTotalistic(0, 4)))
    expect_raises(TypeError, lambda: factor_totalistic(BinaryOuterTotalistic(0, 4)))
    expect_raises(TypeError, lambda: book_row_column_to_enu([-1, 0]))
    expect_raises(TypeError, lambda: book_row_column_to_enu((-1, False)))
    expect_raises(TypeError, lambda: permute_book_code_to_runtime(True))
    expect_raises(ValueError, lambda: permute_book_code_to_runtime(1 << 32))
    expect_raises(TypeError, lambda: runtime_context_to_book_context([0, 0, 0, 0, 0]))
    expect_raises(
        TypeError,
        lambda: runtime_context_to_book_context((0, 0, False, 0, 0)),
    )

    expect_raises(
        ValueError,
        lambda: CAProgram(
            alphabet,
            make_local_access(ORTHOGONAL_2D, 2),
            projection_rule(3, 4, 0),
        ),
    )
    expect_raises(
        ValueError,
        lambda: CAProgram(
            alphabet,
            make_local_access(ORTHOGONAL_2D, 2),
            projection_rule(2, 3, 0),
        ),
    )

    program = strict_t21_program(projection_rule(2, 4, 1))
    old = GridConfiguration(alphabet, topology, (1, 0, 0, 0), SnapshotToken(9))
    active = select_all_sites(old)
    reads = read_local(old, active, program.neighborhood)
    writes = rule_assignments(program, active, reads)
    validate_rule_plan(old, program, active, reads, writes)

    peer = GridConfiguration(alphabet, topology, old.cells, SnapshotToken(9))
    foreign = (SiteHandle(peer.snapshot_token, active[0].coord), *active[1:])
    assert peer.snapshot_token is not old.snapshot_token
    expect_raises(ValueError, lambda: read_local(old, foreign, program.neighborhood))
    expect_raises(
        ValueError,
        lambda: read_local(
            old, (SiteHandle(old.snapshot_token, (2, 0)),), program.neighborhood
        ),
    )
    expect_raises(ValueError, lambda: read_local(old, (active[0], active[0]), program.neighborhood))
    expect_raises(TypeError, lambda: read_local(old, active, object()))

    tampered_reads = (LocalRead(1 - reads[0].center, reads[0].neighbors), *reads[1:])
    expect_raises(
        ValueError,
        lambda: validate_rule_plan(old, program, active, tampered_reads, writes),
    )
    tampered_value = (
        SiteAssignment(writes[0].source, writes[0].target, 1 - writes[0].value),
        *writes[1:],
    )
    expect_raises(
        ValueError,
        lambda: validate_rule_plan(old, program, active, reads, tampered_value),
    )
    wrong_target = (
        SiteAssignment(writes[0].source, (1, 1), writes[0].value),
        *writes[1:],
    )
    expect_raises(
        ValueError,
        lambda: validate_rule_plan(old, program, active, reads, wrong_target),
    )
    expect_raises(
        ValueError,
        lambda: validate_rule_plan(old, program, active, reads, writes[:-1]),
    )
    expect_raises(TypeError, lambda: rule_assignments(program, active, list(reads)))

    successor = apply_parallel(old, active, writes)
    assert successor.snapshot_token is not old.snapshot_token
    expect_raises(ValueError, lambda: read_local(successor, active, program.neighborhood))
    expect_raises(
        ValueError,
        lambda: generic_ca_step(
            program,
            GridConfiguration(
                alphabet,
                FiniteGrid((4,), FixedBoundary(0)),
                (0, 0, 0, 0),
                SnapshotToken(0),
            ),
        ),
    )

    expect_raises(
        TypeError,
        lambda: Native2DState(2, [2, 2], PeriodicBoundary(), (0, 0, 0, 0)),
    )
    expect_raises(
        ValueError,
        lambda: Native2DState(2, (2, 2, 2), PeriodicBoundary(), (0,) * 8),
    )
    native = Native2DState(2, (2, 2), PeriodicBoundary(), (0, 0, 0, 0))
    expect_raises(TypeError, lambda: native_book_general_step(True, native))
    expect_raises(ValueError, lambda: native_book_general_step(1 << 32, native))
    expect_raises(TypeError, lambda: native_book_outer_step(False, native))
    expect_raises(ValueError, lambda: native_book_outer_step(1 << 10, native))
    expect_raises(TypeError, lambda: native_book_totalistic_step(False, native))
    expect_raises(ValueError, lambda: native_book_totalistic_step(1 << 6, native))
    expect_raises(TypeError, lambda: native_book_projection_step(True, native))
    expect_raises(ValueError, lambda: native_book_projection_step(5, native))
    expect_raises(TypeError, lambda: native_row_column_to_enu_grid(native, generation=True))
    expect_raises(
        TypeError,
        lambda: make_sparse_field(2, True, 0, ()),
    )
    expect_raises(
        ValueError,
        lambda: make_sparse_field(2, 2, 0, (((0, 0), 1), ((0, 0), 1))),
    )
    expect_raises(
        ValueError,
        lambda: make_sparse_field(2, 2, 0, (((0, 0), 0),)),
    )
    expect_raises(
        TypeError,
        lambda: make_sparse_field(2, 2, 0, (((0, False), 1),)),
    )
    expect_raises(
        TypeError,
        lambda: make_sparse_field(2, 2, 0, (), generation=True),
    )


DECISION_MATRIX: tuple[tuple[str, str, str, str], ...] = (
    (
        "DOMAIN",
        "parameterization",
        "DiscreteLattice(d=2)",
        "square Z^2 support; finite boxes are explicit realizations",
    ),
    (
        "ALPHABET",
        "direct reuse",
        "FiniteAlphabet(k)",
        "closed exact values 0..k-1",
    ),
    (
        "FRONTIER",
        "direct reuse",
        "AllSites",
        "every semantic lattice site fires once per step",
    ),
    (
        "NEIGHBORHOOD",
        "parameterization",
        "ComposedLocalAccess(Self,OrderedOffsets)",
        "exactly one declared Self plus four unique ordered cardinal offsets",
    ),
    (
        "RULE",
        "preset/restriction",
        "ClosedLocalMap",
        "general, totalistic, and outer-totalistic tables share one schema",
    ),
    (
        "UPDATE",
        "direct reuse",
        "ParallelSameSiteAssign",
        "all reads use one old snapshot; exactly one write per active site",
    ),
    (
        "BOUNDARY",
        "realization parameter",
        "PeriodicOrFixedFiniteGrid",
        "never inferred as native Z^2 semantics",
    ),
)


def assert_decision_matrix() -> None:
    assert len(DECISION_MATRIX) == 7
    assert tuple(row[0] for row in DECISION_MATRIX) == (
        "DOMAIN",
        "ALPHABET",
        "FRONTIER",
        "NEIGHBORHOOD",
        "RULE",
        "UPDATE",
        "BOUNDARY",
    )
    assert DECISION_MATRIX[0][1] == "parameterization"
    assert DECISION_MATRIX[5][1] == "direct reuse"
    assert all("executor" not in row[2].lower() for row in DECISION_MATRIX)


def main() -> None:
    assert ORTHOGONAL_2D == tuple(sorted(ORTHOGONAL_2D))
    assert MOORE_2D == tuple(sorted(MOORE_2D))
    assert (0, 0) not in ORTHOGONAL_2D and (0, 0) not in MOORE_2D
    assert tuple(offset for _name, offset in ROW_COLUMN_COMPASS) == ORTHOGONAL_2D
    assert tuple(offset for _name, offset in XY_EAST_NORTH_COMPASS) == ORTHOGONAL_2D
    assert tuple(name for name, _offset in ROW_COLUMN_COMPASS) != tuple(
        name for name, _offset in XY_EAST_NORTH_COMPASS
    )
    t21_access = strict_t21_program(BinaryTotalistic(0, 4)).neighborhood
    assert tuple(type(component) for component in t21_access.components) == (
        OffsetAccess,
        OffsetAccess,
        SelfAccess,
        OffsetAccess,
        OffsetAccess,
    )
    assert t21_access.self_position == 2 and t21_access.offsets == ORTHOGONAL_2D
    t22_access = strict_t22_program(BinaryTotalistic(0, 8)).neighborhood
    assert t22_access.self_position == 4 and t22_access.offsets == MOORE_2D
    assert_book_codes_and_counts()
    form_counts = assert_strict_local_form_roundtrips()
    basis_cases = assert_book_to_runtime_basis_permutation()
    counts = assert_exhaustive_native_commutation()
    assert_wrapped_slot_multiplicity()
    assert_asymmetric_orientation_and_parallelism()
    assert_boundary_and_support_separation()
    assert_dimension_agnostic_kernel()
    assert_exact_infinite_support()
    assert_t22_moore_boundary()
    assert_hostile_validation()
    assert_decision_matrix()

    total_cases = sum(counts.values())
    assert total_cases == 17_728
    assert basis_cases == 160
    print("T21 semantic oracle: PASS")
    print(f"commutation_cases={total_cases}")
    print(f"outer_totalistic_cases={counts['outer']}")
    print(f"totalistic_cases={counts['totalistic']}")
    print(f"positional_cases={counts['positional']}")
    print(f"general_basis_commutation_cases={counts['general_basis']}")
    print(f"nonaliasing_directional_cases={counts['nonaliasing_directional']}")
    print(f"ternary_alphabet_cases={counts['ternary']}")
    print(f"basis_permutation_cases={basis_cases}")
    print(f"general_codec_basis_cases={form_counts['general_codec']}")
    print(f"outer_factor_roundtrips={form_counts['outer_factor']}")
    print(f"totalistic_factor_roundtrips={form_counts['totalistic_factor']}")
    print("book_codes=1022,942; rule_counts=2^32,2^12,2^10,2^6")
    print("code_1022_t0_t6=PASS; exact_Z2_sparse_support=PASS")
    print("projection_codes=FFFF0000,FF00FF00,F0F0F0F0,CCCCCCCC,AAAAAAAA")
    print("complete_declared_access=Self+four_orthogonal_offsets=PASS")
    print("all_sites=PASS; old_snapshot_parallel_same_site=PASS")
    print("raw_sorted_offsets=PASS; row_column_to_ENU_basis_permutation=PASS")
    print("naive_resort_adversary=PASS; certified_table_input_permutation=PASS")
    print("asymmetric_orientation=PASS; wrapped_slot_multiplicity=PASS")
    print("outer_and_equal_sum_quotient_adversaries=PASS")
    print("finite_realization_boundary_separation=PASS")
    print("fixed_background_sparse_quiescence_guard=PASS")
    print("dimension_agnostic_t1D_t2D_t3D=PASS")
    print("T22_moore_boundary=PASS; no_family_executor=PASS")
    print("exact_type_validation=PASS; opaque_snapshot_identity=PASS")
    print("proposed_D127=dimension/neighborhood parameterization of generic CA preset")
    print("counterexample=NONE; new_shared_axis=NONE")


if __name__ == "__main__":
    main()
