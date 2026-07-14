#!/usr/bin/env python3
"""Dependency-free semantic checks for Goal 1 stage T21.

This is research evidence, not runtime code.  It tests the claim that the
strict two-dimensional cellular automata in Chapter 5 are an ordinary
parameterization of the already-generic cellular-automaton construction:

    all sites -> old-snapshot local read -> same-site assignment
              -> atomic parallel commit

The native support is the square integer lattice.  Finite periodic/fixed
boxes are explicit computational realizations, never an implicit change to
that support.  The center cell is a distinct member of the RULE input schema;
the T21 geometric neighborhood contains exactly the four orthogonal offsets.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from itertools import product
from math import prod
from typing import Protocol


if not __debug__:
    raise RuntimeError("T21 semantic verification requires assertions; do not run with -O")


Coord = tuple[int, ...]
Offset = tuple[int, ...]
Cells = tuple[int, ...]

NORTH: Offset = (-1, 0)
WEST: Offset = (0, -1)
EAST: Offset = (0, 1)
SOUTH: Offset = (1, 0)

# BOOK:13513-13518 gives the sorted five-cell offset list including center.
# The architecture normalized here keeps center in LocalRead/RULE and keeps
# only the four geometric neighbors in the neighborhood axis.
ORTHOGONAL_2D: tuple[Offset, ...] = (NORTH, WEST, EAST, SOUTH)

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
class OffsetNeighborhood:
    """Ordered geometric access offsets; center is intentionally absent."""

    offsets: tuple[Offset, ...]

    def __post_init__(self) -> None:
        raw_offsets = require_exact_tuple(self.offsets, "offsets")
        if not raw_offsets:
            raise ValueError("a spatial neighborhood must have at least one offset")
        first = require_exact_tuple(raw_offsets[0], "offset")
        if not first:
            raise ValueError("offsets must have positive dimension")
        dimension = len(first)
        checked: list[Offset] = []
        for raw in raw_offsets:
            offset = checked_coord(raw, dimension, "offset")
            if all(component == 0 for component in offset):
                raise ValueError("center belongs to RULE input, not geometric offsets")
            checked.append(offset)
        if len(set(checked)) != len(checked):
            raise ValueError("geometric offsets must be unique")

    @property
    def dimension(self) -> int:
        return len(self.offsets[0])

    @property
    def slots(self) -> int:
        return len(self.offsets)


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


@dataclass(frozen=True)
class CAProgram:
    alphabet: FiniteAlphabet
    neighborhood: OffsetNeighborhood
    rule: Rule

    def __post_init__(self) -> None:
        if type(self.alphabet) is not FiniteAlphabet:
            raise TypeError("program alphabet must be FiniteAlphabet")
        if type(self.neighborhood) is not OffsetNeighborhood:
            raise TypeError("program neighborhood must be OffsetNeighborhood")
        if type(self.rule) not in (BinaryOuterTotalistic, BinaryTotalistic, GeneralLookup):
            raise TypeError("program rule must be a closed local rule schema")
        if self.rule.alphabet_size != self.alphabet.size:
            raise ValueError("rule alphabet disagrees with program alphabet")
        if self.rule.neighbor_slots != self.neighborhood.slots:
            raise ValueError("rule input arity disagrees with neighborhood")


def strict_t21_program(rule: Rule) -> CAProgram:
    return CAProgram(FiniteAlphabet(rule.alphabet_size), OffsetNeighborhood(ORTHOGONAL_2D), rule)


def strict_t22_program(rule: Rule) -> CAProgram:
    return CAProgram(FiniteAlphabet(rule.alphabet_size), OffsetNeighborhood(MOORE_2D), rule)


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
    neighborhood: OffsetNeighborhood,
) -> tuple[LocalRead, ...]:
    validate_handles(old, active)
    if neighborhood.dimension != old.topology.dimension:
        raise ValueError("neighborhood and configuration dimensions differ")
    return tuple(
        LocalRead(
            old.value_at(handle.coord),
            tuple(old.value_at(add_coord(handle.coord, offset)) for offset in neighborhood.offsets),
        )
        for handle in active
    )


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


def native_2d_step(program: CAProgram, old: Native2DState) -> Native2DState:
    """Direct T21 definition, independent of handles and generic UPDATE."""

    if program.neighborhood.dimension != 2:
        raise ValueError("native 2D step requires a two-dimensional neighborhood")
    if program.alphabet.size != old.alphabet_size:
        raise ValueError("native program/state alphabets differ")
    values: list[int] = []
    for row in range(old.shape[0]):
        for column in range(old.shape[1]):
            center = old.value_at(row, column)
            neighbors = tuple(
                old.value_at(row + offset[0], column + offset[1])
                for offset in program.neighborhood.offsets
            )
            values.append(program.rule.evaluate(LocalRead(center, neighbors)))
    return Native2DState(old.alphabet_size, old.shape, old.boundary, tuple(values))


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
    return LocalRead(
        field_state.value_at(checked),
        tuple(
            field_state.value_at(add_coord(checked, offset))
            for offset in program.neighborhood.offsets
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

