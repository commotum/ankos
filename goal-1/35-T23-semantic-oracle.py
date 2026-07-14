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
        self_count = sum(type(component) is SelfAccess for component in raw)
        if self_count > 1:
            raise ValueError("local access cannot declare duplicate Self")
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
    def self_position(self) -> int | None:
        return next(
            (
                index
                for index, component in enumerate(self.components)
                if type(component) is SelfAccess
            ),
            None,
        )

    @property
    def has_self(self) -> bool:
        return self.self_position is not None

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


def make_access(
    offsets: tuple[Offset, ...], self_position: int | None
) -> LocalAccess:
    raw = require_tuple(offsets, "offsets")
    components: list[AccessComponent] = [OffsetAccess(offset) for offset in raw]
    if self_position is not None:
        position = require_int(self_position, "Self position")
        if position < 0 or position > len(raw):
            raise ValueError("Self position is outside the schema")
        components.insert(position, SelfAccess())
    return LocalAccess(tuple(components))


@dataclass(frozen=True)
class LocalRead:
    center: int | None
    neighbors: tuple[int, ...]

    def __post_init__(self) -> None:
        if self.center is not None:
            require_int(self.center, "center value")
        raw = require_tuple(self.neighbors, "neighbor values")
        for value in raw:
            require_int(value, "neighbor value")


def validate_read(
    read: LocalRead,
    alphabet_size: int,
    slots: int,
    *,
    require_self: bool,
) -> None:
    if type(read) is not LocalRead:
        raise TypeError("rule input must be LocalRead")
    alphabet = FiniteAlphabet(alphabet_size)
    if type(require_self) is not bool:
        raise TypeError("require_self must be an exact bool")
    if require_self:
        if read.center is None:
            raise ValueError("rule input is missing required Self")
        alphabet.check(read.center, "center value")
    elif read.center is not None:
        raise ValueError("shell-only rule input must omit Self")
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


def complete_context_case_count(profile: str, dimension: int, alphabet_size: int) -> int:
    if type(profile) is not str:
        raise TypeError("profile must be an exact str")
    alphabet = FiniteAlphabet(alphabet_size)
    slots = axes_slots(dimension) if profile == "axes" else full_slots(dimension) if profile == "full" else None
    if slots is None:
        raise ValueError("profile must be axes or full")
    return alphabet.size ** (slots + 1)


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
        validate_read(
            read,
            self.alphabet_size,
            self.neighbor_slots,
            require_self=True,
        )
        assert read.center is not None
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
        validate_read(
            read,
            self.alphabet_size,
            self.neighbor_slots,
            require_self=False,
        )
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
        validate_read(
            read,
            self.alphabet_size,
            self.neighbor_slots,
            require_self=True,
        )
        assert read.center is not None
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
        validate_read(
            read,
            self.alphabet_size,
            self.neighbor_slots,
            require_self=True,
        )
        assert read.center is not None
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
        if type(self.rule) is ShellCountRule:
            if self.neighborhood.has_self:
                raise ValueError("shell-only rule access must omit Self")
        elif not self.neighborhood.has_self:
            raise ValueError("product/positional rule access requires Self")
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
        center = (
            None
            if neighborhood.self_position is None
            else declared[neighborhood.self_position]
        )
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
RUNTIME_FACE_SHELL_ACCESS = make_access(RUNTIME_FACE_OFFSETS, self_position=None)
RUNTIME_FULL_SHELL_ACCESS = make_access(RUNTIME_FULL_OFFSETS, self_position=None)


def access_for_profile(
    profile: str, dimension: int = 3, *, include_self: bool = True
) -> LocalAccess:
    if type(profile) is not str:
        raise TypeError("profile must be an exact str")
    if type(include_self) is not bool:
        raise TypeError("include_self must be an exact bool")
    checked = require_int(dimension, "dimension")
    if checked <= 0:
        raise ValueError("dimension must be positive")
    if checked == 3 and profile == "axes":
        return RUNTIME_FACE_ACCESS if include_self else RUNTIME_FACE_SHELL_ACCESS
    if checked == 3 and profile == "full":
        return RUNTIME_FULL_ACCESS if include_self else RUNTIME_FULL_SHELL_ACCESS
    offsets = axis_offsets(checked) if profile == "axes" else cube_offsets(checked) if profile == "full" else None
    if offsets is None:
        raise ValueError("profile must be axes or full")
    return make_access(
        offsets,
        self_position=len(offsets) // 2 if include_self else None,
    )


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
        access = access_for_profile(
            rule.profile,
            rule.dimension,
            include_self=type(rule) is CountProductRule,
        )
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
    # BOOK:2256,2262,13632,14263,19588 supply predicates/triples.  These
    # integers are derived below under the declared least-significant-case
    # convention; they are not printed source rule numbers.
    ("face_any_neighbor", "axes", 16_380),
    ("face_exactly_one", "axes", 12),
    ("full_exactly_one", "full", 12),
    ("full_exactly_two", "full", 48),
    ("full_exactly_three", "full", 192),
    ("face_self_plus_six_majority", "axes", 16_256),
    ("life3d_5_7_6", "full", 47_104),
    ("life3d_4_5_5", "full", 3_584),
    ("life3d_5_6_5", "full", 11_264),
)

SOURCE_SEED_DESCRIPTORS: tuple[tuple[str, str], ...] = (
    # BOOK:2256,2262 and BOOK:13632.  The latter's "rather than" identifies
    # the 3x1x1 control for the displayed 3x3x1 exact-three variant.
    ("face_any_neighbor", "single_black_cell"),
    ("face_exactly_one", "single_black_cell"),
    ("full_exactly_one", "single_black_cell"),
    ("full_exactly_two", "3x1x1_black_block"),
    ("full_exactly_three", "3x1x1_black_block"),
    ("full_exactly_three_projection_variant", "3x3x1_black_block"),
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
        (
            "face_self_plus_six_majority",
            binary_count_rule(
                "axes",
                named_count_code(
                    lambda center, count: int(center + count >= 4),
                    6,
                ),
            ),
        ),
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
                require_self=True,
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
        validate_read(
            read,
            self.compact.alphabet_size,
            self.compact.neighbor_slots,
            require_self=True,
        )
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


@dataclass(frozen=True)
class SparseField:
    """Exact uniform-background-plus-finite-deviations Z^d representation."""

    dimension: int
    alphabet_size: int
    background: int
    entries: tuple[tuple[Coord, int], ...]

    def __post_init__(self) -> None:
        dimension = require_int(self.dimension, "sparse dimension")
        if dimension <= 0:
            raise ValueError("sparse dimension must be positive")
        alphabet = FiniteAlphabet(self.alphabet_size)
        alphabet.check(self.background, "sparse background")
        raw = require_tuple(self.entries, "sparse entries")
        prior: Coord | None = None
        for coord, value in raw:
            checked = checked_coord(coord, dimension, "sparse coordinate")
            alphabet.check(value, "sparse value")
            if value == self.background:
                raise ValueError("sparse entry must differ from background")
            if prior is not None and checked <= prior:
                raise ValueError("sparse entries must be uniquely sorted")
            prior = checked

    def value_at(self, raw_coord: object) -> int:
        coord = checked_coord(raw_coord, self.dimension)
        for key, value in self.entries:
            if key == coord:
                return value
            if key > coord:
                break
        return self.background


def sparse_field(
    dimension: int,
    alphabet_size: int,
    background: int,
    entries: tuple[tuple[Coord, int], ...],
) -> SparseField:
    raw = require_tuple(entries, "sparse entries")
    normalized = tuple(sorted(raw))
    return SparseField(dimension, alphabet_size, background, normalized)


def sparse_step(program: CAProgram, old: SparseField) -> SparseField:
    if type(program) is not CAProgram or type(old) is not SparseField:
        raise TypeError("sparse step needs exact program and field")
    if program.alphabet.size != old.alphabet_size:
        raise ValueError("sparse program and field alphabets differ")
    if program.neighborhood.dimension != old.dimension:
        raise ValueError("sparse program and field dimensions differ")
    uniform = LocalRead(
        old.background if program.neighborhood.has_self else None,
        (old.background,) * program.neighborhood.slots,
    )
    next_background = program.rule.evaluate(uniform)
    candidates: set[Coord] = set()
    for coord, _value in old.entries:
        candidates.add(coord)
        for offset in program.neighborhood.offsets:
            candidates.add(subtract_coord(coord, offset))
    next_entries: list[tuple[Coord, int]] = []
    for coord in sorted(candidates):
        read = LocalRead(
            old.value_at(coord) if program.neighborhood.has_self else None,
            tuple(old.value_at(add_coord(coord, offset)) for offset in program.neighborhood.offsets),
        )
        value = program.rule.evaluate(read)
        if value != next_background:
            next_entries.append((coord, value))
    return SparseField(
        old.dimension,
        old.alphabet_size,
        next_background,
        tuple(next_entries),
    )


def expect_raises(error: type[BaseException], action: object) -> None:
    if not callable(action):
        raise TypeError("test action must be callable")
    try:
        action()
    except error:
        return
    except Exception as exc:
        raise AssertionError(
            f"expected {error.__name__}, received {type(exc).__name__}"
        ) from exc
    raise AssertionError(f"expected {error.__name__}")


def assert_source_profiles_and_formulas() -> dict[str, int]:
    assert BOOK_CUBE_POSITIONS == tuple(sorted(BOOK_CUBE_POSITIONS))
    assert BOOK_FACE_POSITIONS == tuple(sorted(BOOK_FACE_POSITIONS))
    assert len(BOOK_FACE_POSITIONS) == 7
    assert len(BOOK_FACE_OFFSETS) == 6
    assert len(BOOK_CUBE_POSITIONS) == 27
    assert len(BOOK_FULL_OFFSETS) == 26
    assert (0, 0, 0) not in BOOK_FACE_OFFSETS
    assert (0, 0, 0) not in BOOK_FULL_OFFSETS

    formula_cases = 0
    for dimension in range(1, 5):
        for alphabet_size in range(2, 5):
            axes_shell = 2 * dimension * (alphabet_size - 1) + 1
            full_shell = (3**dimension - 1) * (alphabet_size - 1) + 1
            assert shell_count_case_count("axes", dimension, alphabet_size) == axes_shell
            assert shell_count_case_count("full", dimension, alphabet_size) == full_shell
            assert count_product_case_count("axes", dimension, alphabet_size) == alphabet_size * axes_shell
            assert count_product_case_count("full", dimension, alphabet_size) == alphabet_size * full_shell
            assert complete_context_case_count(
                "axes", dimension, alphabet_size
            ) == alphabet_size ** (2 * dimension + 1)
            assert complete_context_case_count(
                "full", dimension, alphabet_size
            ) == alphabet_size ** (3**dimension)
            formula_cases += 6

    assert shell_count_case_count("axes", 3, 2) == 7
    assert count_product_case_count("axes", 3, 2) == 14
    assert shell_count_case_count("full", 3, 2) == 27
    assert count_product_case_count("full", 3, 2) == 54
    assert shell_count_case_count("axes", 3, 3) == 13
    assert count_product_case_count("axes", 3, 3) == 39
    assert shell_count_case_count("full", 3, 3) == 53
    assert count_product_case_count("full", 3, 3) == 159
    assert complete_context_case_count("axes", 3, 2) == 128
    assert complete_context_case_count("full", 3, 2) == 134_217_728
    assert SOURCE_SEED_DESCRIPTORS == (
        ("face_any_neighbor", "single_black_cell"),
        ("face_exactly_one", "single_black_cell"),
        ("full_exactly_one", "single_black_cell"),
        ("full_exactly_two", "3x1x1_black_block"),
        ("full_exactly_three", "3x1x1_black_block"),
        ("full_exactly_three_projection_variant", "3x3x1_black_block"),
    )

    predicates = {
        "face_any_neighbor": lambda center, count: int(count > 0),
        "face_exactly_one": lambda center, count: int(count == 1),
        "full_exactly_one": lambda center, count: int(count == 1),
        "full_exactly_two": lambda center, count: int(count == 2),
        "full_exactly_three": lambda center, count: int(count == 3),
    }
    derived = {
        name: named_count_code(predicate, 6 if name.startswith("face") else 26)
        for name, predicate in predicates.items()
    }
    assert derived == {
        "face_any_neighbor": 16_380,
        "face_exactly_one": 12,
        "full_exactly_one": 12,
        "full_exactly_two": 48,
        "full_exactly_three": 192,
    }
    assert life3d_code(5, 7, 6) == 47_104
    assert life3d_code(4, 5, 5) == 3_584
    assert life3d_code(5, 6, 5) == 11_264
    assert named_count_code(lambda center, count: int(center + count >= 4), 6) == 16_256
    assert tuple((name, rule.profile) for name, rule in named_rules()) == tuple(
        (name, profile) for name, profile, _code in NAMED_CODES
    )
    for (name, rule), (_same_name, _profile, derived_code) in zip(
        named_rules(), NAMED_CODES, strict=True
    ):
        product_rule = expand_shell_to_product(rule) if type(rule) is ShellCountRule else rule
        assert code_from_outputs(product_rule.outputs) == derived_code, name
    majority = dict(named_rules())["face_self_plus_six_majority"]
    for count in range(7):
        for center in (0, 1):
            read = LocalRead(center, (1,) * count + (0,) * (6 - count))
            assert majority.evaluate(read) == int(center + count >= 4)

    # Literal local evaluators cover every binary face context and every
    # ternary face context without invoking any family dispatch.
    binary_face_contexts = 0
    exact_one = named_rules()[1][1]
    for context in product((0, 1), repeat=7):
        read = LocalRead(context[0], context[1:])
        assert exact_one.evaluate(read) == int(sum(context[1:]) == 1)
        binary_face_contexts += 1
    ternary_face_contexts = 0
    ternary = CountProductRule("axes", 3, 3, tuple(index % 3 for index in range(39)))
    for context in product(range(3), repeat=7):
        read = LocalRead(context[0], context[1:])
        assert ternary.evaluate(read) == (context[0] + 3 * sum(context[1:])) % 3
        ternary_face_contexts += 1
    return {
        "formula_cases": formula_cases,
        "binary_face_contexts": binary_face_contexts,
        "ternary_face_contexts": ternary_face_contexts,
        "source_seed_descriptors": len(SOURCE_SEED_DESCRIPTORS),
    }


def assert_ignore_self_factor() -> dict[str, int]:
    face_signatures = 0
    for code in range(1 << 7):
        shell = binary_shell_rule("axes", code)
        product_rule = expand_shell_to_product(shell)
        assert factor_product_to_shell(product_rule) == shell
        assert factor_product_to_shell(factor_face(expand_face(product_rule))) == shell
        face_signatures += 1

    full_bases = (
        binary_shell_rule("full", 0),
        binary_shell_rule("full", (1 << 27) - 1),
        *(binary_shell_rule("full", 1 << index) for index in range(27)),
    )
    for shell in full_bases:
        product_rule = expand_shell_to_product(shell)
        assert factor_product_to_shell(product_rule) == shell
        assert factor_product_to_shell(
            factor_symbolic(expand_symbolic(product_rule))
        ) == shell

    valid = expand_shell_to_product(binary_shell_rule("axes", 0))
    broken_outputs = list(valid.outputs)
    broken_outputs[1] = 1
    broken = CountProductRule("axes", 3, 2, tuple(broken_outputs))
    expect_raises(ValueError, lambda: factor_product_to_shell(broken))
    assert broken.evaluate(LocalRead(0, (0,) * 6)) == 0
    assert broken.evaluate(LocalRead(1, (0,) * 6)) == 1
    return {
        "face_shell_signatures": face_signatures,
        "full_shell_bases": len(full_bases),
        "self_row_rejections": 1,
    }


def assert_complete_compact_maps() -> dict[str, int]:
    face_signatures = 0
    for code in range(1 << 14):
        compact = binary_count_rule("axes", code)
        complete = expand_face(compact)
        assert factor_face(complete) == compact
        face_signatures += 1

    face_multiplicities = fiber_multiplicities(6)
    assert len(face_multiplicities) == 14
    assert sum(face_multiplicities) == 128
    assert face_multiplicities == tuple(
        comb(6, count) for count in range(7) for _center in (0, 1)
    )

    full_bases = (
        binary_count_rule("full", 0),
        binary_count_rule("full", (1 << 54) - 1),
        *(binary_count_rule("full", 1 << index) for index in range(54)),
    )
    for compact in full_bases:
        expanded = expand_symbolic(compact)
        assert expanded.row_count == 1 << 27
        assert factor_symbolic(expanded) == compact

    full_multiplicities = fiber_multiplicities(26)
    assert len(full_multiplicities) == 54
    assert sum(full_multiplicities) == 1 << 27
    assert full_multiplicities == tuple(
        comb(26, count) for count in range(27) for _center in (0, 1)
    )
    full_zero = binary_count_rule("full", 0)
    disagreement_context = (0, 1, *((0,) * 25))
    broken = SymbolicCompleteMap(
        full_zero,
        ((disagreement_context, 1),),
    )
    expect_raises(ValueError, lambda: factor_symbolic(broken))
    peer_context = (0, 0, 1, *((0,) * 24))
    assert sum(disagreement_context[1:]) == sum(peer_context[1:]) == 1
    assert broken.evaluate_context(disagreement_context) == 1
    assert broken.evaluate_context(peer_context) == 0

    face_zero = expand_face(binary_count_rule("axes", 0))
    face_outputs = list(face_zero.outputs)
    face_outputs[context_index((0, 1, 0, 0, 0, 0, 0), 2)] = 1
    face_broken = GeneralLookup(2, 6, tuple(face_outputs))
    expect_raises(ValueError, lambda: factor_face(face_broken))
    return {
        "face_compact_signatures": face_signatures,
        "face_complete_rows_per_signature": 128,
        "face_expanded_rows_checked": face_signatures * 128,
        "full_compact_bases": len(full_bases),
        "full_complete_rows": 1 << 27,
        "face_fibers": len(face_multiplicities),
        "full_fibers": len(full_multiplicities),
        "disagreement_rejections": 2,
    }


def assert_frame_and_table_permutations() -> dict[str, int]:
    assert BOOK_TO_RUNTIME_FRAME.endswith("_v1")
    for position in BOOK_CUBE_POSITIONS:
        assert runtime_offset_to_book(book_offset_to_runtime(position)) == position
    for position in RUNTIME_CUBE_POSITIONS:
        assert book_offset_to_runtime(runtime_offset_to_book(position)) == position
    assert set(RUNTIME_FACE_OFFSETS) == set(axis_offsets(3))
    assert set(RUNTIME_FULL_OFFSETS) == set(cube_offsets(3))
    assert RUNTIME_FACE_ACCESS.offsets == tuple(sorted(RUNTIME_FACE_OFFSETS))
    assert RUNTIME_FULL_ACCESS.offsets == tuple(sorted(RUNTIME_FULL_OFFSETS))

    face_context_cases = 0
    for book_context in product((0, 1), repeat=7):
        runtime = book_context_to_runtime_context(
            book_context, BOOK_FACE_POSITIONS, RUNTIME_FACE_ACCESS
        )
        assert runtime_context_to_book_context(
            runtime, BOOK_FACE_POSITIONS, RUNTIME_FACE_ACCESS
        ) == book_context
        face_context_cases += 1

    face_table_bases = 0
    for row in range(128):
        book_table = tuple(int(index == row) for index in range(128))
        runtime = permute_book_face_table_to_runtime(book_table)
        assert permute_runtime_face_table_to_book(runtime) == book_table
        face_table_bases += 1

    face_projection_tables = 0
    for position in BOOK_FACE_POSITIONS:
        book_table = book_projection_face_table(position)
        permuted = permute_book_face_table_to_runtime(book_table)
        projection = projection_program("axes", position).rule
        assert type(projection) is ProjectionRule
        assert tuple(
            projection.evaluate(LocalRead(context[0], context[1:]))
            for context in product((0, 1), repeat=7)
        ) == permuted.outputs
        face_projection_tables += 1

    zero = (0,) * 27
    full = (1,) * 27
    full_digit_bases = (zero, full) + tuple(
        tuple(int(index == selected) for index in range(27))
        for selected in range(27)
    ) + tuple(
        tuple(int(index != selected) for index in range(27))
        for selected in range(27)
    )
    assert len(full_digit_bases) == 56
    for book_context in full_digit_bases:
        runtime = permute_full_book_context(book_context)
        assert inverse_permute_full_context(runtime) == book_context
        assert context_from_index(context_index(runtime, 2), 27, 2) == runtime

    runtime_to_book_positions = tuple(
        BOOK_CUBE_POSITIONS.index(runtime_offset_to_book(position))
        for position in RUNTIME_CUBE_POSITIONS
    )
    assert sorted(runtime_to_book_positions) == list(range(27))

    # The Notes' graphics coordinate is separately typed and demonstrably not
    # used as this representation adapter.
    witness = (1, 0, 0)
    assert book_offset_to_runtime(witness) == (0, 0, 1)
    assert book_cuboid_view_position(witness) == (0, 0, -1)
    assert book_offset_to_runtime(witness) != book_cuboid_view_position(witness)
    return {
        "frame_position_cases": 54,
        "face_context_cases": face_context_cases,
        "face_table_bases": face_table_bases,
        "face_projection_tables": face_projection_tables,
        "full_digit_bases": len(full_digit_bases),
        "full_position_permutation": len(runtime_to_book_positions),
        "view_separation_witnesses": 1,
    }


def assert_native_generic_commutation() -> dict[str, int]:
    counts = {
        "face_quotient": 0,
        "full_quotient": 0,
        "directional": 0,
        "named": 0,
        "ternary": 0,
    }

    face_bases = (
        binary_count_rule("axes", 0),
        binary_count_rule("axes", (1 << 14) - 1),
        *(binary_count_rule("axes", 1 << index) for index in range(14)),
    )
    for rule in face_bases:
        program = program_for(rule)
        for mask in range(256):
            native = Native3DState(2, (2, 2, 2), PeriodicBoundary(), cells_from_mask((2, 2, 2), mask))
            generic = generic_step(program, encode_native(native))
            assert decode_generic(generic) == native_count_step(rule, native)
            counts["face_quotient"] += 1

    full_bases = (
        binary_count_rule("full", 0),
        binary_count_rule("full", (1 << 54) - 1),
        *(binary_count_rule("full", 1 << index) for index in range(54)),
    )
    masks = (0, 255, 1, 2, 4, 8, 16, 32, 64, 128, 254, 253, 251, 247, 239, 223)
    assert len(masks) == 16
    for rule in full_bases:
        program = program_for(rule)
        for mask in masks:
            native = Native3DState(2, (2, 2, 2), PeriodicBoundary(), cells_from_mask((2, 2, 2), mask))
            assert decode_generic(generic_step(program, encode_native(native))) == native_count_step(
                rule, native
            )
            counts["full_quotient"] += 1

    directional_native = Native3DState(
        2,
        (3, 4, 5),
        FixedBoundary(0),
        native_cells_with_points((3, 4, 5), ((((1, 2, 2), 1), ((0, 0, 4), 1)))),
    )
    for profile, positions in (
        ("axes", BOOK_FACE_POSITIONS),
        ("full", BOOK_CUBE_POSITIONS),
    ):
        for position in positions:
            generic = generic_step(
                projection_program(profile, position),
                encode_native(directional_native),
            )
            assert decode_generic(generic) == native_projection_step(
                position, profile, directional_native
            )
            counts["directional"] += 1

    fixtures: dict[str, Native3DState] = {}
    single = Native3DState(
        2,
        (5, 5, 5),
        FixedBoundary(0),
        native_cells_with_points((5, 5, 5), ((((2, 2, 2), 1),))),
    )
    line_three = Native3DState(
        2,
        (5, 5, 5),
        FixedBoundary(0),
        native_cells_with_points(
            (5, 5, 5),
            ((((2, 2, 1), 1), ((2, 2, 2), 1), ((2, 2, 3), 1))),
        ),
    )
    for name, _rule in named_rules():
        fixtures[name] = (
            line_three
            if name in ("full_exactly_two", "full_exactly_three")
            else single
        )
    for name, rule in named_rules():
        native = fixtures[name]
        assert decode_generic(generic_step(program_for(rule), encode_native(native))) == native_count_step(
            rule, native
        )
        counts["named"] += 1

    ternary_cells = tuple((index * 2 + 1) % 3 for index in range(8))
    ternary_native = Native3DState(3, (2, 2, 2), PeriodicBoundary(), ternary_cells)
    for profile, width in (("axes", 39), ("full", 159)):
        rule = CountProductRule(profile, 3, 3, tuple(index % 3 for index in range(width)))
        assert decode_generic(
            generic_step(program_for(rule), encode_native(ternary_native))
        ) == native_count_step(rule, ternary_native)
        counts["ternary"] += 1

    assert counts == {
        "face_quotient": 4_096,
        "full_quotient": 896,
        "directional": 34,
        "named": 9,
        "ternary": 2,
    }
    return counts


@dataclass(frozen=True)
class CompletePositionalSchema:
    """Declared finite domain for an arbitrary complete positional map."""

    alphabet_size: int
    positions: tuple[Offset, ...]

    def __post_init__(self) -> None:
        FiniteAlphabet(self.alphabet_size)
        raw = require_tuple(self.positions, "positional schema")
        if not raw:
            raise ValueError("positional schema must be nonempty")
        dimension: int | None = None
        seen: set[Offset] = set()
        for position in raw:
            checked = require_tuple(position, "position")
            if dimension is None:
                dimension = len(checked)
            if len(checked) != dimension:
                raise ValueError("position dimensions differ")
            normalized = tuple(require_int(value, "position component") for value in checked)
            if normalized in seen:
                raise ValueError("positions must be unique")
            seen.add(normalized)

    @property
    def context_rows(self) -> int:
        return self.alphabet_size ** len(self.positions)

    def address(self, context: tuple[int, ...]) -> int:
        if len(require_tuple(context, "schema context")) != len(self.positions):
            raise ValueError("schema context has wrong width")
        return context_index(context, self.alphabet_size)

    def decode_address(self, address: int) -> tuple[int, ...]:
        return context_from_index(address, len(self.positions), self.alphabet_size)


def assert_complete_positional_domains() -> dict[str, int]:
    face = CompletePositionalSchema(2, BOOK_FACE_POSITIONS)
    full = CompletePositionalSchema(2, BOOK_CUBE_POSITIONS)
    assert face.context_rows == 128
    assert full.context_rows == 134_217_728 == 1 << 27

    face_addresses = 0
    for address in range(face.context_rows):
        context = face.decode_address(address)
        assert face.address(context) == address
        face_addresses += 1

    zero = (0,) * 27
    ones = (1,) * 27
    algebraic_context_witnesses = (zero, ones) + tuple(
        tuple(int(index == selected) for index in range(27))
        for selected in range(27)
    ) + tuple(
        tuple(int(index != selected) for index in range(27))
        for selected in range(27)
    )
    for context in algebraic_context_witnesses:
        assert full.decode_address(full.address(context)) == context
    # address/decode are the same exact finite mixed-radix algorithms for every
    # declared row; the 56 witnesses certify digit placement, not all tables.
    assert full.decode_address(0) == zero
    assert full.decode_address(full.context_rows - 1) == ones
    return {
        "face_declared_rows": face.context_rows,
        "face_exhaustive_addresses": face_addresses,
        "full_declared_rows": full.context_rows,
        "full_digit_address_witnesses": len(algebraic_context_witnesses),
        "full_positional_projections": 27,
    }


def assert_small_quotient_and_parallelism() -> None:
    def multiplicities(offsets: tuple[Offset, ...]) -> tuple[int, ...]:
        counts: dict[Coord, int] = {}
        for offset in offsets:
            resolved = tuple(value % 2 for value in offset)
            counts[resolved] = counts.get(resolved, 0) + 1
        return tuple(sorted(counts.values()))

    assert multiplicities(RUNTIME_FACE_OFFSETS) == (2, 2, 2)
    assert multiplicities(RUNTIME_FULL_OFFSETS) == (2, 2, 2, 4, 4, 4, 8)

    topology = FiniteGrid((2, 2, 2), PeriodicBoundary())
    face_old = GridConfiguration(
        FiniteAlphabet(2),
        topology,
        cells_with_one((2, 2, 2), (1, 0, 0)),
        SnapshotToken(0),
    )
    handle = SiteHandle(face_old.snapshot_token, (0, 0, 0))
    face_read = read_local(face_old, (handle,), RUNTIME_FACE_ACCESS)[0]
    assert sum(face_read.neighbors) == 2
    assert len(face_read.neighbors) == 6

    corner_old = GridConfiguration(
        FiniteAlphabet(2),
        topology,
        cells_with_one((2, 2, 2), (1, 1, 1)),
        SnapshotToken(0),
    )
    corner_handle = SiteHandle(corner_old.snapshot_token, (0, 0, 0))
    full_read = read_local(corner_old, (corner_handle,), RUNTIME_FULL_ACCESS)[0]
    assert sum(full_read.neighbors) == 8
    assert len(full_read.neighbors) == 26

    # Runtime -x projection shifts the one toward +x under one old snapshot.
    selected = RUNTIME_FACE_ACCESS.offsets.index((-1, 0, 0))
    shift = program_for(
        ProjectionRule(2, 6, selected),
        RUNTIME_FACE_ACCESS,
    )
    line = GridConfiguration(
        FiniteAlphabet(2),
        FiniteGrid((4, 1, 1), FixedBoundary(0)),
        cells_with_one((4, 1, 1), (0, 0, 0)),
        SnapshotToken(4),
    )
    assert generic_step(shift, line).cells == (0, 1, 0, 0)
    in_place = list(line.cells)
    for x in range(4):
        old_left = 0 if x == 0 else in_place[x - 1]
        in_place[x] = old_left
    assert tuple(in_place) == (0, 0, 0, 0)


def assert_support_boundary_and_background() -> None:
    selected = RUNTIME_FACE_ACCESS.offsets.index((-1, 0, 0))
    shift = program_for(ProjectionRule(2, 6, selected), RUNTIME_FACE_ACCESS)
    shape = (3, 3, 3)
    edge = cells_with_one(shape, (2, 1, 1))
    periodic = GridConfiguration(
        FiniteAlphabet(2), FiniteGrid(shape, PeriodicBoundary()), edge, SnapshotToken(0)
    )
    fixed = GridConfiguration(
        FiniteAlphabet(2), FiniteGrid(shape, FixedBoundary(0)), edge, SnapshotToken(0)
    )
    assert nonzero_coords(generic_step(shift, periodic)) == ((0, 1, 1),)
    assert nonzero_coords(generic_step(shift, fixed)) == ()

    face_any = program_for(named_rules()[0][1])
    state = sparse_field(3, 2, 0, ((((0, 0, 0), 1),)))
    expected_sizes = (1, 6, 19, 44)
    for expected_size in expected_sizes:
        assert state.background == 0
        assert len(state.entries) == expected_size
        state = sparse_step(face_any, state)

    # A nonquiescent rule evolves the uniform background explicitly; it is not
    # smuggled in as a fixed finite boundary.
    toggle = binary_count_rule("axes", 1)
    white = sparse_field(3, 2, 0, ())
    black = sparse_step(program_for(toggle), white)
    assert black.background == 1 and black.entries == ()
    white_again = sparse_step(program_for(toggle), black)
    # Code 1 is one only for Self=0,count=0; uniform black maps to zero.
    assert white_again.background == 0 and white_again.entries == ()

    # Exact sparse lowering and a sufficiently padded fixed-background work
    # realization agree inside the one-step causal region.
    sparse_seed = sparse_field(3, 2, 0, ((((0, 0, 0), 1),)))
    sparse_next = sparse_step(face_any, sparse_seed)
    finite_seed = GridConfiguration(
        FiniteAlphabet(2),
        FiniteGrid((5, 5, 5), FixedBoundary(0)),
        cells_with_one((5, 5, 5), (2, 2, 2)),
        SnapshotToken(0),
    )
    finite_next = generic_step(face_any, finite_seed)
    translated = tuple(
        sorted(
            ((coord[0] - 2, coord[1] - 2, coord[2] - 2), finite_next.value_at(coord))
            for coord in nonzero_coords(finite_next)
        )
    )
    assert translated == sparse_next.entries


def assert_same_runner_across_t21_t22_t23() -> None:
    profiles = (
        (2, axis_offsets(2)),
        (2, cube_offsets(2)),
        (3, axis_offsets(3)),
        (3, cube_offsets(3)),
    )
    outputs: list[GridConfiguration] = []
    for dimension, offsets in profiles:
        access = make_access(offsets, self_position=len(offsets) // 2)
        rule = ProjectionRule(2, len(offsets), 0)
        program = CAProgram(FiniteAlphabet(2), access, rule)
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
        outputs.append(successor)
    assert tuple(output.topology.dimension for output in outputs) == (2, 2, 3, 3)


def dyadaxes_3d_summary(read: LocalRead) -> tuple[int, bool, bool]:
    """Current src/ca summary: Self, face majority, other at-least-ten."""

    validate_read(read, 2, 26, require_self=True)
    by_offset = dict(zip(RUNTIME_FULL_OFFSETS, read.neighbors, strict=True))
    face_count = sum(by_offset[offset] for offset in RUNTIME_FACE_OFFSETS)
    other_count = sum(
        value for offset, value in by_offset.items() if offset not in RUNTIME_FACE_OFFSETS
    )
    return (read.center, face_count > 3, other_count >= 10)


def assert_dyadaxes_information_loss() -> dict[str, int]:
    empty = LocalRead(0, (0,) * 26)
    values = [0] * 26
    face_slot = RUNTIME_FULL_OFFSETS.index(RUNTIME_FACE_OFFSETS[0])
    values[face_slot] = 1
    one_face = LocalRead(0, tuple(values))
    assert dyadaxes_3d_summary(empty) == dyadaxes_3d_summary(one_face) == (0, False, False)
    face_exactly_one = named_rules()[1][1]
    full_exactly_one = named_rules()[2][1]
    face_read_empty = LocalRead(0, tuple(empty.neighbors[RUNTIME_FULL_OFFSETS.index(offset)] for offset in RUNTIME_FACE_OFFSETS))
    face_read_one = LocalRead(0, tuple(one_face.neighbors[RUNTIME_FULL_OFFSETS.index(offset)] for offset in RUNTIME_FACE_OFFSETS))
    assert face_exactly_one.evaluate(face_read_empty) == 0
    assert face_exactly_one.evaluate(face_read_one) == 1
    assert full_exactly_one.evaluate(empty) == 0
    assert full_exactly_one.evaluate(one_face) == 1

    # A second witness loses full edge/corner counts 0 versus 1 as well.
    one_other_values = [0] * 26
    other_slot = next(
        index
        for index, offset in enumerate(RUNTIME_FULL_OFFSETS)
        if offset not in RUNTIME_FACE_OFFSETS
    )
    one_other_values[other_slot] = 1
    one_other = LocalRead(0, tuple(one_other_values))
    assert dyadaxes_3d_summary(empty) == dyadaxes_3d_summary(one_other)
    assert full_exactly_one.evaluate(one_other) == 1
    return {
        "summary_collision_pairs": 2,
        "face_required_output_splits": 1,
        "full_required_output_splits": 2,
    }


RUNTIME_GAP_MATRIX: tuple[tuple[str, str, str], ...] = (
    (
        "src/ca/alphabets.py",
        "reuse for T23 / broader gap",
        "boolean/int-range/symbolic cover T23 finite labels; Value excludes product/tagged values and has no composite constructor",
    ),
    (
        "src/ca/loci.py",
        "reuse",
        "rank-3 [t,x,y,z] coordinate spaces, selectors, gather, and boundary reads already exist",
    ),
    (
        "src/ca/neighborhoods.py",
        "reuse/parameterize",
        "Self, von_neumann/l1_shell six-face, moore/full-cube twenty-six, and literal offsets exist",
    ),
    (
        "src/ca/frontiers.py",
        "reuse",
        "time_slice over the complete rank-3 shape supplies AllSites",
    ),
    (
        "src/ca/rollout.py:apply_rule",
        "gap",
        "public evaluation branches on named family instead of applying one closed typed RULE descriptor",
    ),
    (
        "src/ca/rollout.py:_normalize_rule_ids",
        "gap",
        "rule ids are coerced to numpy int64, which cannot serialize arbitrary-precision T23 table codes",
    ),
    (
        "src/ca/rules.py:dyadaxes_3d",
        "lossy preset only",
        "Self plus face-majority plus edge/corner-atLeast10 cannot recover exact 6/26 shell counts",
    ),
    (
        "src/ca/specs.py + datasets.py",
        "gap",
        "named Phase-1 family dispatch and the 256-rule dyadaxes pool do not expose schema-tagged T23 maps",
    ),
    (
        "src/ca/viz",
        "observer",
        "TXYZ export, slices, projections, palettes, and Cuboid-style transforms are views, never program identity",
    ),
)


DECISION_MATRIX: tuple[tuple[str, str, str, str], ...] = (
    (
        "DOMAIN",
        "parameterization",
        "DiscreteSpace(dimension=3)",
        "t+3D is dimensional task space, not a construction class",
    ),
    (
        "CONFIGURATION",
        "parameterization",
        "FixedLattice(CubicGrid(Z^3),FiniteAlphabet)",
        "labels evolve while support/topology stay fixed",
    ),
    (
        "ALPHABET",
        "direct reuse",
        "FiniteAlphabet",
        "binary examples and finite-k formulas need no 3D alphabet class",
    ),
    (
        "FRONTIER",
        "direct reuse",
        "AllSites",
        "every old lattice site fires exactly once",
    ),
    (
        "NEIGHBORHOOD",
        "parameterization",
        "Compose(Self,OrderedOffsets[6|26])",
        "face and full-cube access are explicit ordered data",
    ),
    (
        "RULE",
        "restriction/lossless representation",
        "SchemaTagged(Positional|ShellCount|SelfXCount)",
        "IgnoreSelf, product, and arbitrary positional domains remain distinct",
    ),
    (
        "UPDATE",
        "direct reuse",
        "SnapshotParallelSameSite",
        "one complete same-site assignment per old source",
    ),
    (
        "SEED",
        "direct reuse",
        "IndependentValidatedConfiguration",
        "point, line, random, and structure fixtures are run data",
    ),
    (
        "REALIZATION/VIEW",
        "parameterization/observer",
        "BoundaryWorkFrameCropProjection",
        "finite boundaries, frame adapters, and graphics do not define native Z^3",
    ),
)


def assert_architecture_matrices() -> None:
    assert tuple(row[0] for row in DECISION_MATRIX) == (
        "DOMAIN",
        "CONFIGURATION",
        "ALPHABET",
        "FRONTIER",
        "NEIGHBORHOOD",
        "RULE",
        "UPDATE",
        "SEED",
        "REALIZATION/VIEW",
    )
    assert DECISION_MATRIX[6][1] == "direct reuse"
    assert "lossless representation" in DECISION_MATRIX[5][1]
    assert all("executor" not in row[2].lower() for row in DECISION_MATRIX)
    assert len(RUNTIME_GAP_MATRIX) == 9
    assert sum(row[1] == "gap" for row in RUNTIME_GAP_MATRIX) == 3
    assert any(row[1] == "lossy preset only" for row in RUNTIME_GAP_MATRIX)
    assert any(row[1] == "observer" for row in RUNTIME_GAP_MATRIX)


def assert_hostile_validation() -> None:
    expect_raises(TypeError, lambda: FiniteAlphabet(True))
    expect_raises(ValueError, lambda: FiniteAlphabet(1))
    expect_raises(TypeError, lambda: FiniteGrid([2, 2, 2], PeriodicBoundary()))
    expect_raises(ValueError, lambda: FiniteGrid((2, 0, 2), PeriodicBoundary()))
    expect_raises(TypeError, lambda: FixedBoundary(False))
    expect_raises(TypeError, lambda: SnapshotToken(True))
    expect_raises(ValueError, lambda: SnapshotToken(-1))
    expect_raises(TypeError, lambda: book_offset_to_runtime([0, 0, 0]))
    expect_raises(ValueError, lambda: book_offset_to_runtime((0, 0)))
    expect_raises(TypeError, lambda: access_for_profile(1))
    expect_raises(ValueError, lambda: access_for_profile("unknown"))
    expect_raises(TypeError, lambda: make_access(list(RUNTIME_FACE_OFFSETS), 3))
    expect_raises(
        ValueError,
        lambda: make_access((RUNTIME_FACE_OFFSETS[0], RUNTIME_FACE_OFFSETS[0]), 1),
    )
    expect_raises(
        ValueError,
        lambda: LocalAccess(
            (SelfAccess(), OffsetAccess((-1, 0, 0)), SelfAccess())
        ),
    )
    expect_raises(TypeError, lambda: LocalAccess((SelfAccess(), object())))
    expect_raises(TypeError, lambda: count_product_case_count("axes", 3, False))
    expect_raises(ValueError, lambda: count_product_case_count("bad", 3, 2))
    expect_raises(ValueError, lambda: shell_count_case_count("bad", 3, 2))
    expect_raises(
        ValueError,
        lambda: CountProductRule("axes", 3, 2, (0,) * 13),
    )
    expect_raises(
        ValueError,
        lambda: ShellCountRule("full", 3, 2, (0,) * 26),
    )
    expect_raises(
        TypeError,
        lambda: ShellCountRule("axes", 3, 2, (*((0,) * 6), False)),
    )
    expect_raises(ValueError, lambda: GeneralLookup(2, 6, (0,) * 127))
    expect_raises(TypeError, lambda: GeneralLookup(2, 1, (0, 0, 0, False)))
    expect_raises(ValueError, lambda: ProjectionRule(2, 6, 6))
    expect_raises(TypeError, lambda: ProjectionRule(2, 6, False))
    expect_raises(ValueError, lambda: binary_count_rule("axes", 1 << 14))
    expect_raises(ValueError, lambda: binary_shell_rule("full", 1 << 27))
    expect_raises(
        ValueError,
        lambda: CAProgram(
            FiniteAlphabet(2),
            RUNTIME_FULL_ACCESS,
            binary_count_rule("axes", 0),
        ),
    )
    expect_raises(
        ValueError,
        lambda: CompletePositionalSchema(2, ((0, 0, 0), (0, 0, 0))),
    )
    expect_raises(
        ValueError,
        lambda: CompletePositionalSchema(2, ((0, 0), (0, 0, 1))),
    )
    expect_raises(
        ValueError,
        lambda: permute_book_face_table_to_runtime((0,) * 127),
    )
    expect_raises(
        TypeError,
        lambda: permute_book_face_table_to_runtime((*((0,) * 127), False)),
    )
    expect_raises(ValueError, lambda: runtime_slot_for_book_position((1, 1, 0), RUNTIME_FACE_ACCESS))
    expect_raises(
        ValueError,
        lambda: SymbolicCompleteMap(
            binary_count_rule("full", 0),
            (((0,) * 27, 0), ((0,) * 27, 0)),
        ),
    )
    expect_raises(
        ValueError,
        lambda: SparseField(3, 2, 0, ((((0, 0, 0), 0),))),
    )
    expect_raises(
        ValueError,
        lambda: SparseField(
            3,
            2,
            0,
            ((((0, 0, 0), 1), ((0, 0, 0), 1))),
        ),
    )

    alphabet = FiniteAlphabet(2)
    topology = FiniteGrid((2, 2, 2), FixedBoundary(0))
    old = GridConfiguration(
        alphabet,
        topology,
        cells_with_one((2, 2, 2), (0, 0, 0)),
        SnapshotToken(5),
    )
    program = program_for(binary_count_rule("axes", 12))
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
        SiteAssignment(writes[0].source, (1, 1, 1), writes[0].value),
        *writes[1:],
    )
    expect_raises(
        ValueError,
        lambda: validate_plan(old, program, active, reads, wrong_target),
    )
    successor = apply_parallel(old, active, writes)
    assert successor.snapshot_token is not old.snapshot_token
    expect_raises(ValueError, lambda: read_local(successor, active, program.neighborhood))


def main() -> None:
    source_counts = assert_source_profiles_and_formulas()
    ignore_self_counts = assert_ignore_self_factor()
    representation_counts = assert_complete_compact_maps()
    positional_counts = assert_complete_positional_domains()
    permutation_counts = assert_frame_and_table_permutations()
    commutation_counts = assert_native_generic_commutation()
    assert_small_quotient_and_parallelism()
    assert_support_boundary_and_background()
    assert_same_runner_across_t21_t22_t23()
    dyadaxes_counts = assert_dyadaxes_information_loss()
    assert_architecture_matrices()
    assert_hostile_validation()

    commutations = sum(commutation_counts.values())
    assert commutations == 5_037
    print("T23 semantic oracle: PASS")
    print(f"native_generic_commutations={commutations}")
    print(
        "commutation_partition="
        f"face_quotient:{commutation_counts['face_quotient']},"
        f"full_quotient:{commutation_counts['full_quotient']},"
        f"directional:{commutation_counts['directional']},"
        f"named:{commutation_counts['named']},"
        f"ternary:{commutation_counts['ternary']}"
    )
    print(
        "declared_access=Self+6_faces|Self+26_face_edge_corner; "
        "raw_Book_triples_lexicographic=PASS"
    )
    print(
        "case_formulas="
        "AxesShell=2d(k-1)+1,AxesProduct=k*(2d(k-1)+1),"
        "FullShell=(3^d-1)(k-1)+1,FullProduct=k*((3^d-1)(k-1)+1); "
        f"formula_checks:{source_counts['formula_cases']}; "
        "d3k2=7/14_axes,27/54_full; d3k3=13/39_axes,53/159_full"
    )
    print(
        "complete_positional_formulas="
        "axes_context_rows=k^(2d+1),axes_rules=k^(k^(2d+1));"
        "full_context_rows=k^(3^d),full_rules=k^(k^(3^d))"
    )
    print(
        "local_context_checks="
        f"binary_face:{source_counts['binary_face_contexts']},"
        f"ternary_face:{source_counts['ternary_face_contexts']}"
    )
    print(
        "IgnoreSelf_factor="
        f"all_face_shell_signatures:{ignore_self_counts['face_shell_signatures']},"
        f"full_shell_algebraic_bases:{ignore_self_counts['full_shell_bases']},"
        f"one_Self_row_rejected:{ignore_self_counts['self_row_rejections']}; "
        "shell_predicate_identity_primary=PASS"
    )
    print(
        "complete_compact_maps="
        f"all_face_product_signatures:{representation_counts['face_compact_signatures']},"
        f"face_rows_each:{representation_counts['face_complete_rows_per_signature']},"
        f"face_rows_checked:{representation_counts['face_expanded_rows_checked']},"
        f"full_product_algebraic_bases:{representation_counts['full_compact_bases']},"
        f"fibers:{representation_counts['face_fibers']}/{representation_counts['full_fibers']},"
        f"one_row_disagreements_rejected:{representation_counts['disagreement_rejections']}"
    )
    print(
        "general_positional_domains="
        f"face_rows:{positional_counts['face_declared_rows']},"
        f"full_rows:{positional_counts['full_declared_rows']}; "
        "binary_rule_counts=2^128_face_general,2^(2^27)_full_general,"
        "2^7_face_shell,2^14_face_product,2^27_full_shell,2^54_full_product"
    )
    print(
        "full_positional_address_proof="
        f"mixed_radix_digit_witnesses:{positional_counts['full_digit_address_witnesses']},"
        f"ordered_projections:{positional_counts['full_positional_projections']}; "
        "declared_domain_is_all_2^27_contexts; arbitrary_table_not_eagerly_enumerated"
    )
    print(
        "frame_and_table_permutation="
        f"positions:{permutation_counts['frame_position_cases']},"
        f"face_contexts:{permutation_counts['face_context_cases']},"
        f"face_table_bases:{permutation_counts['face_table_bases']},"
        f"full_digit_bases:{permutation_counts['full_digit_bases']}; "
        f"adapter:{BOOK_TO_RUNTIME_FRAME}; inverse=PASS"
    )
    print(
        "view_separation=Cuboid[-Reverse(position)]_display_only; "
        "not_native_coordinates; witness=PASS"
    )
    print(
        "named_structural_profiles="
        "face(any,exact1,self+shell>=4);full(exact1,exact2,exact3);"
        "Life3D[(5,7,6),(4,5,5),(5,6,5)]"
    )
    print(
        "derived_canonical_codes_under_index_self+2*shell_count="
        "face_any:16380,face_exact1:12,full_exact1:12,full_exact2:48,"
        "full_exact3:192,face_self_plus_six_majority:16256,"
        "Life3D:47104/3584/11264; "
        "not_source_given_rule_numbers"
    )
    print(
        "source_seed_descriptors="
        f"{source_counts['source_seed_descriptors']}; "
        "single_cell(face_any,face_exact1,full_exact1),"
        "3x1x1(full_exact2,full_exact3),3x3x1(full_exact3_projection_variant); "
        "class4_exact_seed_not_in_text"
    )
    print(
        "fiber_multiplicity="
        "face:2*C(6,n)_total128;full:2*C(26,n)_total134217728; "
        "small_2^3_quotient=faces[2,2,2],full[2,2,2,4,4,4,8]"
    )
    print("old_snapshot_parallelism=PASS; same_site_atomic_commit=PASS")
    print("exact_Z3_sparse_background=PASS; finite_boundary/support/view_separation=PASS")
    print(
        "dyadaxes_3d_information_loss="
        f"collision_pairs:{dyadaxes_counts['summary_collision_pairs']},"
        f"face_output_splits:{dyadaxes_counts['face_required_output_splits']},"
        f"full_output_splits:{dyadaxes_counts['full_required_output_splits']}; "
        "summary=(self,face_count>3,other_count>=10)"
    )
    print(
        "runtime_audit="
        "finite_scalar_alphabet+rank3_loci+6/26_access+boundaries+views_reusable; "
        "gaps=family_branches,schema_tables,bigint_rule_ids; "
        "broader_composite_alphabet_gap=product/tagged; dyadaxes_is_lossy_preset"
    )
    print("T21_T22_T23_same_runner=PASS; new_UPDATE=NONE; family_executor=NONE")
    print("exact_type_and_opaque_snapshot_validation=PASS")
    print(
        "proposed_D129=3D cubic dimension/access and schema-tagged RULE "
        "parameterizations; audit_categories_1_to_3; no category_4 execution algebra"
    )


if __name__ == "__main__":
    main()
