#!/usr/bin/env python3
"""Dependency-free semantic and runtime-architecture audit for T23.

This file is Goal 1 evidence, not runtime code.  It compares an independent
literal three-index Book-frame evaluator with the same branch-free
SimpleProgram route used by T21 and T22:

    active = FRONTIER.select(configuration)
    reads  = NEIGHBORHOOD.read(configuration, active)
    writes = RULE(active, reads)
    next   = UPDATE.apply(configuration, active, writes)

The source-backed T23 profiles are explicit Self-plus-six-face and
Self-plus-twenty-six-cube accesses.  Their compact tables use
Self + k*AxesTotal and Self + k*FullTotal respectively.  Dimension, access,
and table schema are parameters; finite boundaries, sparse lowering,
coordinate adapters, and views are separate realization/representation roles.
No construction-named state, UPDATE, executor, or family branch appears here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product
from math import comb, prod
from typing import Protocol


if not __debug__:
    raise RuntimeError("T23 semantic verification requires assertions; do not run with -O")


Coord = tuple[int, ...]
Offset = tuple[int, ...]
Cells = tuple[int, ...]

BOOK_CUBE_POSITIONS: tuple[Offset, ...] = tuple(product((-1, 0, 1), repeat=3))
BOOK_FACE_POSITIONS: tuple[Offset, ...] = tuple(
    offset for offset in BOOK_CUBE_POSITIONS if sum(abs(value) for value in offset) <= 1
)
BOOK_FACE_OFFSETS: tuple[Offset, ...] = tuple(
    offset for offset in BOOK_FACE_POSITIONS if offset != (0, 0, 0)
)
BOOK_FULL_OFFSETS: tuple[Offset, ...] = tuple(
    offset for offset in BOOK_CUBE_POSITIONS if offset != (0, 0, 0)
)


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
    return tuple(require_int(component, f"{name} component") for component in raw)


def add_coord(left: Coord, right: Offset) -> Coord:
    if len(left) != len(right):
        raise ValueError("coordinate dimensions differ")
    return tuple(a + b for a, b in zip(left, right, strict=True))


def subtract_coord(left: Coord, right: Offset) -> Coord:
    if len(left) != len(right):
        raise ValueError("coordinate dimensions differ")
    return tuple(a - b for a, b in zip(left, right, strict=True))


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


def context_index(context: tuple[int, ...], alphabet_size: int) -> int:
    alphabet = FiniteAlphabet(alphabet_size)
    raw = require_tuple(context, "context")
    result = 0
    for value in raw:
        result = result * alphabet.size + alphabet.check(value, "context value")
    return result


def context_from_index(index: int, width: int, alphabet_size: int) -> tuple[int, ...]:
    value = require_int(index, "context index")
    count = require_int(width, "context width")
    alphabet = FiniteAlphabet(alphabet_size)
    if count <= 0:
        raise ValueError("context width must be positive")
    if value < 0 or value >= alphabet.size**count:
        raise ValueError("context index is out of range")
    digits = [0] * count
    for position in range(count - 1, -1, -1):
        value, digits[position] = divmod(value, alphabet.size)
    return tuple(digits)


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
    """Finite quotient realization, not native Z^d support."""


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
            raise TypeError("snapshot token must be SnapshotToken")

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
        checked = tuple(require_int(value, "offset component") for value in raw)
        if all(value == 0 for value in checked):
            raise ValueError("zero displacement must use SelfAccess")


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


def axes_slots(dimension: int) -> int:
    checked = require_int(dimension, "dimension")
    if checked <= 0:
        raise ValueError("dimension must be positive")
    return 2 * checked


def full_slots(dimension: int) -> int:
    checked = require_int(dimension, "dimension")
    if checked <= 0:
        raise ValueError("dimension must be positive")
    return 3**checked - 1


def count_product_case_count(profile: str, dimension: int, alphabet_size: int) -> int:
    if type(profile) is not str:
        raise TypeError("profile must be an exact str")
    alphabet = FiniteAlphabet(alphabet_size)
    slots = axes_slots(dimension) if profile == "axes" else full_slots(dimension) if profile == "full" else None
    if slots is None:
        raise ValueError("profile must be axes or full")
    return alphabet.size * (slots * (alphabet.size - 1) + 1)


class LocalRule(Protocol):
    alphabet_size: int
    neighbor_slots: int

    def evaluate(self, read: LocalRead) -> int: ...


@dataclass(frozen=True)
class CountProductRule:
    """Closed table indexed by Self + k*sum(neighbor values)."""

    profile: str
    dimension: int
    alphabet_size: int
    outputs: tuple[int, ...]
    neighbor_slots: int = field(init=False)

    def __post_init__(self) -> None:
        if type(self.profile) is not str or self.profile not in ("axes", "full"):
            raise ValueError("profile must be axes or full")
        dimension = require_int(self.dimension, "dimension")
        if dimension <= 0:
            raise ValueError("dimension must be positive")
        alphabet = FiniteAlphabet(self.alphabet_size)
        slots = axes_slots(dimension) if self.profile == "axes" else full_slots(dimension)
        raw = require_tuple(self.outputs, "count-product outputs")
        expected = alphabet.size * (slots * (alphabet.size - 1) + 1)
        if len(raw) != expected:
            raise ValueError("count-product table is incomplete")
        for value in raw:
            alphabet.check(value, "count-product output")
        object.__setattr__(self, "neighbor_slots", slots)

    def evaluate(self, read: LocalRead) -> int:
        validate_read(read, self.alphabet_size, self.neighbor_slots)
        return self.outputs[read.center + self.alphabet_size * sum(read.neighbors)]


@dataclass(frozen=True)
class ShellCountRule:
    """Closed IgnoreSelf table indexed only by the surrounding-value sum."""

    profile: str
    dimension: int
    alphabet_size: int
    outputs: tuple[int, ...]
    neighbor_slots: int = field(init=False)

    def __post_init__(self) -> None:
        if type(self.profile) is not str or self.profile not in ("axes", "full"):
            raise ValueError("profile must be axes or full")
        dimension = require_int(self.dimension, "dimension")
        if dimension <= 0:
            raise ValueError("dimension must be positive")
        alphabet = FiniteAlphabet(self.alphabet_size)
        slots = axes_slots(dimension) if self.profile == "axes" else full_slots(dimension)
        raw = require_tuple(self.outputs, "shell-count outputs")
        expected = slots * (alphabet.size - 1) + 1
        if len(raw) != expected:
            raise ValueError("shell-count table is incomplete")
        for value in raw:
            alphabet.check(value, "shell-count output")
        object.__setattr__(self, "neighbor_slots", slots)

    def evaluate(self, read: LocalRead) -> int:
        validate_read(read, self.alphabet_size, self.neighbor_slots)
        return self.outputs[sum(read.neighbors)]


@dataclass(frozen=True)
class GeneralLookup:
    """Materialized complete map over center followed by declared offsets."""

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
        return self.outputs[context_index((read.center, *read.neighbors), self.alphabet_size)]


@dataclass(frozen=True)
class ProjectionRule:
    """Closed positional projection used to certify ordered access."""

    alphabet_size: int
    neighbor_slots: int
    selected: int

    def __post_init__(self) -> None:
        FiniteAlphabet(self.alphabet_size)
        slots = require_int(self.neighbor_slots, "neighbor slots")
        selected = require_int(self.selected, "selected position")
        if slots <= 0:
            raise ValueError("neighbor slots must be positive")
        if selected < -1 or selected >= slots:
            raise ValueError("selected position is out of range")

    def evaluate(self, read: LocalRead) -> int:
        validate_read(read, self.alphabet_size, self.neighbor_slots)
        return read.center if self.selected == -1 else read.neighbors[self.selected]


Rule = CountProductRule | ShellCountRule | GeneralLookup | ProjectionRule


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
            CountProductRule,
            ShellCountRule,
            GeneralLookup,
            ProjectionRule,
        ):
            raise TypeError("unsupported closed rule schema")
        if self.alphabet.size != self.rule.alphabet_size:
            raise ValueError("rule and alphabet disagree")
        if self.neighborhood.slots != self.rule.neighbor_slots:
            raise ValueError("rule and neighborhood arities disagree")
        if type(self.rule) in (CountProductRule, ShellCountRule):
            if self.neighborhood.dimension != self.rule.dimension:
                raise ValueError("profile and neighborhood dimensions disagree")
            expected = (
                axes_slots(self.rule.dimension)
                if self.rule.profile == "axes"
                else full_slots(self.rule.dimension)
            )
            if self.neighborhood.slots != expected:
                raise ValueError("profile and declared access disagree")


@dataclass(frozen=True)
class SiteHandle:
    snapshot_token: SnapshotToken = field(repr=False)
    coord: Coord

    def __post_init__(self) -> None:
        if type(self.snapshot_token) is not SnapshotToken:
            raise TypeError("site handle needs a SnapshotToken")
        raw = require_tuple(self.coord, "site coordinate")
        for value in raw:
            require_int(value, "site coordinate component")


@dataclass(frozen=True)
class SiteAssignment:
    source: SiteHandle
    target: Coord
    value: int

    def __post_init__(self) -> None:
        if type(self.source) is not SiteHandle:
            raise TypeError("assignment source must be SiteHandle")
        raw = require_tuple(self.target, "assignment target")
        for component in raw:
            require_int(component, "target component")
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


# Raw Book triples remain authoritative.  This signed permutation is an
# explicit, optional representation choice for the audit, not source-defined
# native semantics and not the Notes' Cuboid display transform.
BOOK_TO_RUNTIME_FRAME = "book-layer-row-column_to_runtime-x-east-y-north-z-layer_v1"


def book_offset_to_runtime(raw: object) -> Offset:
    layer, row, column = checked_coord(raw, 3, "Book offset")
    return (column, -row, layer)


def runtime_offset_to_book(raw: object) -> Offset:
    x, y, z = checked_coord(raw, 3, "runtime offset")
    return (z, -y, x)


def book_cuboid_view_position(raw: object) -> Coord:
    """BOOK:13511 display-only -Reverse transform."""

    first, second, third = checked_coord(raw, 3, "Book view position")
    return (-third, -second, -first)


RUNTIME_CUBE_POSITIONS: tuple[Offset, ...] = tuple(sorted(BOOK_CUBE_POSITIONS))
RUNTIME_FACE_OFFSETS: tuple[Offset, ...] = tuple(
    sorted(book_offset_to_runtime(offset) for offset in BOOK_FACE_OFFSETS)
)
RUNTIME_FULL_OFFSETS: tuple[Offset, ...] = tuple(
    sorted(book_offset_to_runtime(offset) for offset in BOOK_FULL_OFFSETS)
)
RUNTIME_FACE_ACCESS = make_access(RUNTIME_FACE_OFFSETS, self_position=3)
RUNTIME_FULL_ACCESS = make_access(RUNTIME_FULL_OFFSETS, self_position=13)


def access_for_profile(profile: str, dimension: int = 3) -> LocalAccess:
    if type(profile) is not str:
        raise TypeError("profile must be an exact str")
    checked = require_int(dimension, "dimension")
    if checked <= 0:
        raise ValueError("dimension must be positive")
    if checked == 3 and profile == "axes":
        return RUNTIME_FACE_ACCESS
    if checked == 3 and profile == "full":
        return RUNTIME_FULL_ACCESS
    offsets = axis_offsets(checked) if profile == "axes" else cube_offsets(checked) if profile == "full" else None
    if offsets is None:
        raise ValueError("profile must be axes or full")
    return make_access(offsets, self_position=len(offsets) // 2)


def axis_offsets(dimension: int) -> tuple[Offset, ...]:
    checked = require_int(dimension, "dimension")
    if checked <= 0:
        raise ValueError("dimension must be positive")
    return tuple(
        offset
        for offset in product((-1, 0, 1), repeat=checked)
        if sum(abs(value) for value in offset) == 1
    )


def cube_offsets(dimension: int) -> tuple[Offset, ...]:
    checked = require_int(dimension, "dimension")
    if checked <= 0:
        raise ValueError("dimension must be positive")
    zero = (0,) * checked
    return tuple(offset for offset in product((-1, 0, 1), repeat=checked) if offset != zero)


def program_for(rule: Rule, access: LocalAccess | None = None) -> CAProgram:
    if type(rule) not in (
        CountProductRule,
        ShellCountRule,
        GeneralLookup,
        ProjectionRule,
    ):
        raise TypeError("unsupported rule")
    if access is None:
        if type(rule) not in (CountProductRule, ShellCountRule):
            raise ValueError("non-profile rules require explicit access")
        access = access_for_profile(rule.profile, rule.dimension)
    return CAProgram(FiniteAlphabet(rule.alphabet_size), access, rule)


@dataclass(frozen=True)
class Native3DState:
    """Independent row-major carrier in raw (layer,row,column) Book frame."""

    alphabet_size: int
    shape: tuple[int, int, int]
    boundary: Boundary
    cells: Cells

    def __post_init__(self) -> None:
        alphabet = FiniteAlphabet(self.alphabet_size)
        raw_shape = require_tuple(self.shape, "native shape")
        if len(raw_shape) != 3:
            raise ValueError("native state must be three-dimensional")
        checked = tuple(require_int(extent, "native extent") for extent in raw_shape)
        if any(extent <= 0 for extent in checked):
            raise ValueError("native extents must be positive")
        if type(self.boundary) not in (PeriodicBoundary, FixedBoundary):
            raise TypeError("native boundary is unsupported")
        raw_cells = require_tuple(self.cells, "native cells")
        if len(raw_cells) != prod(checked):
            raise ValueError("native cell count does not match shape")
        for value in raw_cells:
            alphabet.check(value, "native cell")
        if type(self.boundary) is FixedBoundary:
            alphabet.check(self.boundary.value, "native boundary value")

    def value_at(self, layer: int, row: int, column: int) -> int:
        layer = require_int(layer, "layer")
        row = require_int(row, "row")
        column = require_int(column, "column")
        layers, rows, columns = self.shape
        if type(self.boundary) is PeriodicBoundary:
            layer %= layers
            row %= rows
            column %= columns
        elif (
            layer < 0
            or layer >= layers
            or row < 0
            or row >= rows
            or column < 0
            or column >= columns
        ):
            assert type(self.boundary) is FixedBoundary
            return self.boundary.value
        return self.cells[(layer * rows + row) * columns + column]


def encode_native(state: Native3DState, generation: int = 0) -> GridConfiguration:
    """Lossless explicit frame adapter; it is not native T23 identity."""

    if type(state) is not Native3DState:
        raise TypeError("native state must be Native3DState")
    layers, rows, columns = state.shape
    runtime_shape = (columns, rows, layers)
    runtime_cells = [0] * prod(runtime_shape)
    for layer in range(layers):
        for row in range(rows):
            for column in range(columns):
                runtime_coord = (column, rows - 1 - row, layer)
                runtime_cells[flat_index(runtime_shape, runtime_coord)] = state.value_at(
                    layer, row, column
                )
    return GridConfiguration(
        FiniteAlphabet(state.alphabet_size),
        FiniteGrid(runtime_shape, state.boundary),
        tuple(runtime_cells),
        SnapshotToken(generation),
    )


def decode_generic(state: GridConfiguration) -> Native3DState:
    if type(state) is not GridConfiguration or state.topology.dimension != 3:
        raise TypeError("generic state must be a 3D GridConfiguration")
    columns, rows, layers = state.topology.shape
    native_cells: list[int] = []
    for layer in range(layers):
        for row in range(rows):
            for column in range(columns):
                native_cells.append(state.value_at((column, rows - 1 - row, layer)))
    return Native3DState(
        state.alphabet.size,
        (layers, rows, columns),
        state.topology.boundary,
        tuple(native_cells),
    )


def native_book_context(
    old: Native3DState, layer: int, row: int, column: int
) -> tuple[int, ...]:
    if type(old) is not Native3DState:
        raise TypeError("native state must be Native3DState")
    layer = require_int(layer, "layer")
    row = require_int(row, "row")
    column = require_int(column, "column")
    return tuple(
        old.value_at(layer + dlayer, row + drow, column + dcolumn)
        for dlayer, drow, dcolumn in BOOK_CUBE_POSITIONS
    )


def native_neighbor_values(
    old: Native3DState,
    layer: int,
    row: int,
    column: int,
    profile: str,
) -> tuple[int, ...]:
    offsets = BOOK_FACE_OFFSETS if profile == "axes" else BOOK_FULL_OFFSETS if profile == "full" else None
    if offsets is None:
        raise ValueError("profile must be axes or full")
    return tuple(
        old.value_at(layer + dlayer, row + drow, column + dcolumn)
        for dlayer, drow, dcolumn in offsets
    )


def native_count_step(
    rule: CountProductRule | ShellCountRule, old: Native3DState
) -> Native3DState:
    if type(rule) not in (CountProductRule, ShellCountRule) or rule.dimension != 3:
        raise TypeError("native T23 step requires a closed 3D count rule")
    if old.alphabet_size != rule.alphabet_size:
        raise ValueError("native rule and state alphabets differ")
    values: list[int] = []
    for layer in range(old.shape[0]):
        for row in range(old.shape[1]):
            for column in range(old.shape[2]):
                center = old.value_at(layer, row, column)
                neighbors = native_neighbor_values(old, layer, row, column, rule.profile)
                if type(rule) is CountProductRule:
                    index = center + rule.alphabet_size * sum(neighbors)
                else:
                    index = sum(neighbors)
                values.append(rule.outputs[index])
    return Native3DState(old.alphabet_size, old.shape, old.boundary, tuple(values))


def runtime_slot_for_book_position(position: Offset, access: LocalAccess) -> int:
    checked = checked_coord(position, 3, "Book position")
    if checked == (0, 0, 0):
        return -1
    runtime_offset = book_offset_to_runtime(checked)
    try:
        return access.offsets.index(runtime_offset)
    except ValueError as exc:
        raise ValueError("Book position is outside declared access") from exc


def native_projection_step(
    book_position: Offset, profile: str, old: Native3DState
) -> Native3DState:
    position = checked_coord(book_position, 3, "Book position")
    admitted = BOOK_FACE_POSITIONS if profile == "axes" else BOOK_CUBE_POSITIONS if profile == "full" else None
    if admitted is None or position not in admitted:
        raise ValueError("projection position is outside profile")
    values = tuple(
        old.value_at(layer + position[0], row + position[1], column + position[2])
        for layer in range(old.shape[0])
        for row in range(old.shape[1])
        for column in range(old.shape[2])
    )
    return Native3DState(old.alphabet_size, old.shape, old.boundary, values)


def projection_program(profile: str, book_position: Offset, alphabet_size: int = 2) -> CAProgram:
    access = access_for_profile(profile, 3)
    selected = runtime_slot_for_book_position(book_position, access)
    return program_for(ProjectionRule(alphabet_size, access.slots, selected), access)


def cells_from_mask(shape: tuple[int, ...], mask: int) -> Cells:
    value = require_int(mask, "cell mask")
    size = prod(shape)
    if value < 0 or value >= 1 << size:
        raise ValueError("cell mask is out of range")
    return tuple((value >> index) & 1 for index in range(size))


def cells_with_one(shape: tuple[int, ...], coord: Coord, value: int = 1) -> Cells:
    checked = checked_coord(coord, len(shape))
    cells = [0] * prod(shape)
    cells[flat_index(shape, checked)] = require_int(value, "point value")
    return tuple(cells)


def native_cells_with_points(
    shape: tuple[int, int, int], points: tuple[tuple[Coord, int], ...]
) -> Cells:
    cells = [0] * prod(shape)
    for coord, value in require_tuple(points, "native points"):
        checked = checked_coord(coord, 3, "native point")
        cells[flat_index(shape, checked)] = require_int(value, "native point value")
    return tuple(cells)


def nonzero_coords(state: GridConfiguration) -> tuple[Coord, ...]:
    return tuple(coord for coord in all_coords(state.topology.shape) if state.value_at(coord) != 0)


def outputs_from_code(code: int, width: int, alphabet_size: int = 2) -> tuple[int, ...]:
    value = require_int(code, "rule code")
    count = require_int(width, "table width")
    alphabet = FiniteAlphabet(alphabet_size)
    if count <= 0:
        raise ValueError("table width must be positive")
    if value < 0 or value >= alphabet.size**count:
        raise ValueError("rule code is out of range")
    outputs: list[int] = []
    for _ in range(count):
        value, digit = divmod(value, alphabet.size)
        outputs.append(digit)
    return tuple(outputs)


def code_from_outputs(outputs: tuple[int, ...], alphabet_size: int = 2) -> int:
    raw = require_tuple(outputs, "rule outputs")
    alphabet = FiniteAlphabet(alphabet_size)
    result = 0
    place = 1
    for output in raw:
        result += alphabet.check(output, "rule output") * place
        place *= alphabet.size
    return result


def binary_count_rule(profile: str, code: int) -> CountProductRule:
    width = count_product_case_count(profile, 3, 2)
    return CountProductRule(profile, 3, 2, outputs_from_code(code, width))


def shell_count_case_count(profile: str, dimension: int, alphabet_size: int) -> int:
    if type(profile) is not str:
        raise TypeError("profile must be an exact str")
    alphabet = FiniteAlphabet(alphabet_size)
    slots = axes_slots(dimension) if profile == "axes" else full_slots(dimension) if profile == "full" else None
    if slots is None:
        raise ValueError("profile must be axes or full")
    return slots * (alphabet.size - 1) + 1


def binary_shell_rule(profile: str, code: int) -> ShellCountRule:
    width = shell_count_case_count(profile, 3, 2)
    return ShellCountRule(profile, 3, 2, outputs_from_code(code, width))


def expand_shell_to_product(rule: ShellCountRule) -> CountProductRule:
    if type(rule) is not ShellCountRule:
        raise TypeError("IgnoreSelf expansion requires ShellCountRule")
    outputs = tuple(
        rule.outputs[count]
        for count in range(rule.neighbor_slots * (rule.alphabet_size - 1) + 1)
        for _center in range(rule.alphabet_size)
    )
    return CountProductRule(
        rule.profile,
        rule.dimension,
        rule.alphabet_size,
        outputs,
    )


def factor_product_to_shell(rule: CountProductRule) -> ShellCountRule:
    if type(rule) is not CountProductRule:
        raise TypeError("IgnoreSelf factorization requires CountProductRule")
    outputs: list[int] = []
    sums = rule.neighbor_slots * (rule.alphabet_size - 1) + 1
    for count in range(sums):
        fiber = tuple(
            rule.outputs[center + rule.alphabet_size * count]
            for center in range(rule.alphabet_size)
        )
        if len(set(fiber)) != 1:
            raise ValueError("product table is not constant across the Self fiber")
        outputs.append(fiber[0])
    result = ShellCountRule(
        rule.profile,
        rule.dimension,
        rule.alphabet_size,
        tuple(outputs),
    )
    if expand_shell_to_product(result) != rule:
        raise AssertionError("IgnoreSelf factorization lost information")
    return result


def named_count_code(predicate: object, neighbor_slots: int) -> int:
    if not callable(predicate):
        raise TypeError("named predicate must be callable for evidence construction")
    slots = require_int(neighbor_slots, "neighbor slots")
    if slots <= 0:
        raise ValueError("neighbor slots must be positive")
    code = 0
    for count in range(slots + 1):
        for center in (0, 1):
            output = predicate(center, count)
            if type(output) is not int or output not in (0, 1):
                raise TypeError("named predicate must return an exact bit")
            code |= output << (center + 2 * count)
    return code


NAMED_CODES: tuple[tuple[str, str, int], ...] = (
    ("face_any_neighbor", "axes", 16_380),
    ("face_exactly_one", "axes", 12),
    ("full_exactly_one", "full", 12),
    ("full_exactly_two", "full", 48),
    ("full_exactly_three", "full", 192),
    ("life3d_5_7_6", "full", 47_104),
    ("life3d_4_5_5", "full", 3_584),
    ("life3d_5_6_5", "full", 11_264),
)


def shell_predicate_rule(profile: str, predicate: object) -> ShellCountRule:
    if not callable(predicate):
        raise TypeError("shell predicate must be callable for evidence construction")
    slots = 6 if profile == "axes" else 26 if profile == "full" else None
    if slots is None:
        raise ValueError("profile must be axes or full")
    outputs: list[int] = []
    for count in range(slots + 1):
        output = predicate(count)
        if type(output) is not int or output not in (0, 1):
            raise TypeError("shell predicate must return an exact bit")
        outputs.append(output)
    return ShellCountRule(profile, 3, 2, tuple(outputs))


def named_rules() -> tuple[tuple[str, CountProductRule | ShellCountRule], ...]:
    """Structural predicates/triples are primary; integers are derived codecs."""

    return (
        ("face_any_neighbor", shell_predicate_rule("axes", lambda count: int(count > 0))),
        ("face_exactly_one", shell_predicate_rule("axes", lambda count: int(count == 1))),
        ("full_exactly_one", shell_predicate_rule("full", lambda count: int(count == 1))),
        ("full_exactly_two", shell_predicate_rule("full", lambda count: int(count == 2))),
        ("full_exactly_three", shell_predicate_rule("full", lambda count: int(count == 3))),
        ("life3d_5_7_6", binary_count_rule("full", life3d_code(5, 7, 6))),
        ("life3d_4_5_5", binary_count_rule("full", life3d_code(4, 5, 5))),
        ("life3d_5_6_5", binary_count_rule("full", life3d_code(5, 6, 5))),
    )


def life3d_code(survival_low: int, survival_high: int, birth: int) -> int:
    low = require_int(survival_low, "survival low")
    high = require_int(survival_high, "survival high")
    born = require_int(birth, "birth count")
    if low < 0 or high < low or high > 26 or born < 0 or born > 26:
        raise ValueError("3D Life counts are out of range")
    return named_count_code(
        lambda center, count: int((center == 1 and low <= count <= high) or count == born),
        26,
    )


def expand_face(rule: CountProductRule) -> GeneralLookup:
    if type(rule) is not CountProductRule or (
        rule.profile,
        rule.dimension,
        rule.alphabet_size,
    ) != ("axes", 3, 2):
        raise TypeError("strict binary T23 face rule required")
    return GeneralLookup(
        2,
        6,
        tuple(
            rule.evaluate(LocalRead(context[0], context[1:]))
            for context in product((0, 1), repeat=7)
        ),
    )


def factor_face(table: GeneralLookup) -> CountProductRule:
    if type(table) is not GeneralLookup:
        raise TypeError("face factorization requires GeneralLookup")
    if table.alphabet_size != 2 or table.neighbor_slots != 6:
        raise ValueError("strict binary T23 face table required")
    fibers: dict[tuple[int, int], int] = {}
    for context in product((0, 1), repeat=7):
        read = LocalRead(context[0], context[1:])
        key = (read.center, sum(read.neighbors))
        output = table.evaluate(read)
        prior = fibers.setdefault(key, output)
        if prior != output:
            raise ValueError("complete face map disagrees within a count fiber")
    if len(fibers) != 14:
        raise AssertionError("face fibers are incomplete")
    outputs = tuple(
        fibers[(center, count)]
        for count in range(7)
        for center in (0, 1)
    )
    result = CountProductRule("axes", 3, 2, outputs)
    if expand_face(result) != table:
        raise AssertionError("face factorization lost information")
    return result


@dataclass(frozen=True)
class SymbolicCompleteMap:
    """Exact denotation of a huge complete table by fibers plus finite overrides.

    This is proof data only.  The runtime route evaluates the closed compact
    CountProductRule directly; it does not invoke an interpreter or callback.
    """

    compact: CountProductRule
    overrides: tuple[tuple[tuple[int, ...], int], ...] = ()

    def __post_init__(self) -> None:
        if type(self.compact) is not CountProductRule:
            raise TypeError("symbolic expansion needs CountProductRule")
        raw = require_tuple(self.overrides, "symbolic overrides")
        seen: set[tuple[int, ...]] = set()
        for context, output in raw:
            checked = require_tuple(context, "override context")
            validate_read(
                LocalRead(checked[0], checked[1:]),
                self.compact.alphabet_size,
                self.compact.neighbor_slots,
            )
            self.compact.alphabet_size
            FiniteAlphabet(self.compact.alphabet_size).check(output, "override output")
            if checked in seen:
                raise ValueError("duplicate override context")
            seen.add(checked)

    @property
    def row_count(self) -> int:
        return self.compact.alphabet_size ** (self.compact.neighbor_slots + 1)

    def evaluate_context(self, context: tuple[int, ...]) -> int:
        raw = require_tuple(context, "complete context")
        read = LocalRead(raw[0], raw[1:])
        validate_read(read, self.compact.alphabet_size, self.compact.neighbor_slots)
        for key, output in self.overrides:
            if raw == key:
                return output
        return self.compact.evaluate(read)


def expand_symbolic(rule: CountProductRule) -> SymbolicCompleteMap:
    if type(rule) is not CountProductRule:
        raise TypeError("symbolic expansion requires CountProductRule")
    return SymbolicCompleteMap(rule)


def factor_symbolic(table: SymbolicCompleteMap) -> CountProductRule:
    if type(table) is not SymbolicCompleteMap:
        raise TypeError("symbolic factorization requires SymbolicCompleteMap")
    for context, output in table.overrides:
        read = LocalRead(context[0], context[1:])
        if output != table.compact.evaluate(read):
            raise ValueError("complete map disagrees within a count fiber")
    return table.compact


def fiber_multiplicities(neighbor_slots: int) -> tuple[int, ...]:
    slots = require_int(neighbor_slots, "neighbor slots")
    if slots <= 0:
        raise ValueError("neighbor slots must be positive")
    return tuple(comb(slots, count) for count in range(slots + 1) for _center in (0, 1))


def book_context_to_runtime_context(
    book_context: tuple[int, ...], positions: tuple[Offset, ...], access: LocalAccess
) -> tuple[int, ...]:
    raw = require_tuple(book_context, "Book context")
    declared = require_tuple(positions, "Book positions")
    if len(raw) != len(declared) or len(raw) != access.slots + 1:
        raise ValueError("Book context and access arities differ")
    if declared.count((0, 0, 0)) != 1:
        raise ValueError("Book positions must contain Self exactly once")
    by_runtime_offset: dict[Offset, int] = {}
    center: int | None = None
    for position, value in zip(declared, raw, strict=True):
        checked_value = require_int(value, "Book context value")
        if position == (0, 0, 0):
            center = checked_value
        else:
            by_runtime_offset[book_offset_to_runtime(position)] = checked_value
    if center is None or set(by_runtime_offset) != set(access.offsets):
        raise ValueError("Book positions do not match runtime access")
    return (center, *(by_runtime_offset[offset] for offset in access.offsets))


def runtime_context_to_book_context(
    runtime_context: tuple[int, ...], positions: tuple[Offset, ...], access: LocalAccess
) -> tuple[int, ...]:
    raw = require_tuple(runtime_context, "runtime context")
    declared = require_tuple(positions, "Book positions")
    if len(raw) != access.slots + 1 or len(declared) != len(raw):
        raise ValueError("runtime context and access arities differ")
    center = require_int(raw[0], "runtime center")
    values = {
        offset: require_int(value, "runtime neighbor")
        for offset, value in zip(access.offsets, raw[1:], strict=True)
    }
    return tuple(
        center if position == (0, 0, 0) else values[book_offset_to_runtime(position)]
        for position in declared
    )


def permute_book_face_table_to_runtime(book_outputs: tuple[int, ...]) -> GeneralLookup:
    raw = require_tuple(book_outputs, "Book face table")
    if len(raw) != 128:
        raise ValueError("Book face table must have 128 rows")
    for value in raw:
        if type(value) is not int or value not in (0, 1):
            raise TypeError("Book face outputs must be exact bits")
    return GeneralLookup(
        2,
        6,
        tuple(
            raw[
                context_index(
                    runtime_context_to_book_context(
                        runtime_context, BOOK_FACE_POSITIONS, RUNTIME_FACE_ACCESS
                    ),
                    2,
                )
            ]
            for runtime_context in product((0, 1), repeat=7)
        ),
    )


def permute_runtime_face_table_to_book(runtime_table: GeneralLookup) -> tuple[int, ...]:
    if type(runtime_table) is not GeneralLookup:
        raise TypeError("runtime table must be GeneralLookup")
    if runtime_table.alphabet_size != 2 or runtime_table.neighbor_slots != 6:
        raise ValueError("runtime table must be strict binary face table")
    return tuple(
        runtime_table.outputs[
            context_index(
                book_context_to_runtime_context(
                    book_context, BOOK_FACE_POSITIONS, RUNTIME_FACE_ACCESS
                ),
                2,
            )
        ]
        for book_context in product((0, 1), repeat=7)
    )


def permute_full_book_context(book_context: tuple[int, ...]) -> tuple[int, ...]:
    return book_context_to_runtime_context(
        book_context, BOOK_CUBE_POSITIONS, RUNTIME_FULL_ACCESS
    )


def inverse_permute_full_context(runtime_context: tuple[int, ...]) -> tuple[int, ...]:
    return runtime_context_to_book_context(
        runtime_context, BOOK_CUBE_POSITIONS, RUNTIME_FULL_ACCESS
    )


def book_projection_face_table(book_position: Offset) -> tuple[int, ...]:
    position = checked_coord(book_position, 3, "Book face position")
    if position not in BOOK_FACE_POSITIONS:
        raise ValueError("position is outside Book face access")
    selected = BOOK_FACE_POSITIONS.index(position)
    return tuple(context[selected] for context in product((0, 1), repeat=7))
