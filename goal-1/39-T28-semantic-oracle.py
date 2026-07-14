#!/usr/bin/env python3
"""Independent semantic and architecture oracle for Goal 1 stage T28.

The strict Book construction is a finite positive rectangular grid with cyclic
incidence in both axes.  Every old tile fires once.  Its ordered old-snapshot
read is the 2 by 2 block ``((NW, N), (W, Self))`` produced by
``Partition[list, {2, 2}, 1, -1]``.  A closed ordered Literal/Any pattern
program chooses one nonempty rectangular patch, and the already established
T26 ranked block-mosaic UPDATE assembles every patch atomically.  Context cells
influence the row choice but do not become parents of the emitted children.

This file proves that composition directly.  It does not implement runtime
code.  In particular it:

* guards the one-character OCR repair in BOOK:13806 (bare ``-`` to Blank
  ``_``) and tests the exact recovered row for both values of its NW wildcard;
* gives ordered first-match pattern clauses an explicit exhaustive lowering,
  while rejecting missing coverage instead of inheriting ReplaceAll fallback;
* checks cyclic Partition alignment on every binary rectangle through 3 by 3;
* exhausts all 65,536 Boolean choices over the 16 binary 2 by 2 contexts on a
  de Bruijn torus containing every context exactly once, using two distinct
  uniform 2 by 2 output patches;
* proves compatible mixed mosaics, typed incompatible/no-commit outcomes,
  exact lineage, old-snapshot reads, newborn deferral, and product placement;
* rejects fixed/open/reflected boundaries, sequential mutation, flat patch
  concatenation, callbacks, raster rules, stale provenance, and partial tables;
* records a concrete unequal-subdivision counterexample.  Compatible mixed
  patches still use T26 UPDATE, but arbitrary coarse/fine adjacency has
  unbounded context arity and is not silently packed into the strict profile.

The oracle is dependency-free, deterministic, portable outside the repository
root, silent on import, and intentionally fails closed under ``python -O``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from itertools import product
from typing import Callable, Iterable


if not __debug__:
    raise RuntimeError("T28 semantic verification requires assertions; do not run with -O")


Label = int
Grid = tuple[tuple[Label, ...], ...]
Patch = Grid
Context4 = tuple[Label, Label, Label, Label]
Coord2 = tuple[int, int]

BITS = (0, 1)
BINARY_CONTEXTS: tuple[Context4, ...] = tuple(product(BITS, repeat=4))
SLOT_NAMES = ("NW", "N", "W", "Self")
SLOT_OFFSETS: tuple[Coord2, ...] = ((-1, -1), (-1, 0), (0, -1), (0, 0))


def exact_int(value: object, name: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{name} must be an exact int")
    return value


def exact_tuple(value: object, name: str) -> tuple[object, ...]:
    if type(value) is not tuple:
        raise TypeError(f"{name} must be an exact tuple")
    return value


def checked_alphabet_size(value: object) -> int:
    size = exact_int(value, "alphabet size")
    if size < 2:
        raise ValueError("T28 requires a finite alphabet with at least two labels")
    return size


def all_contexts(alphabet_size: int) -> tuple[Context4, ...]:
    size = checked_alphabet_size(alphabet_size)
    return tuple(product(range(size), repeat=4))


def checked_context(value: object, alphabet_size: int, name: str = "context") -> Context4:
    size = checked_alphabet_size(alphabet_size)
    raw = exact_tuple(value, name)
    if len(raw) != 4:
        raise ValueError(f"{name} must contain exactly NW, N, W, Self")
    labels: list[int] = []
    for index, item in enumerate(raw):
        label = exact_int(item, f"{name}[{SLOT_NAMES[index]}]")
        if label < 0 or label >= size:
            raise ValueError(f"{name} label is outside the alphabet")
        labels.append(label)
    return (labels[0], labels[1], labels[2], labels[3])


def checked_patch(
    value: object,
    alphabet_size: int,
    *,
    name: str = "patch",
) -> Patch:
    size = checked_alphabet_size(alphabet_size)
    raw_rows = exact_tuple(value, name)
    if not raw_rows:
        raise ValueError(f"{name} must have positive height")
    rows: list[tuple[int, ...]] = []
    width: int | None = None
    for row_index, raw_row in enumerate(raw_rows):
        row = exact_tuple(raw_row, f"{name} row")
        if not row:
            raise ValueError(f"{name} must have positive width")
        labels: list[int] = []
        for column_index, item in enumerate(row):
            label = exact_int(item, f"{name}[{row_index},{column_index}]")
            if label < 0 or label >= size:
                raise ValueError(f"{name} label is outside the alphabet")
            labels.append(label)
        if width is None:
            width = len(labels)
        elif width != len(labels):
            raise ValueError(f"{name} rows must be rectangular")
        rows.append(tuple(labels))
    return tuple(rows)


def checked_grid(value: object, alphabet_size: int) -> Grid:
    return checked_patch(value, alphabet_size, name="configuration")


def patch_shape(patch: Patch) -> tuple[int, int]:
    return (len(patch), len(patch[0]))


@dataclass(frozen=True, eq=False)
class SnapshotToken:
    """Opaque exact-snapshot identity; generation is diagnostic only."""

    generation: int
    parent: SnapshotToken | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        generation = exact_int(self.generation, "generation")
        if generation < 0:
            raise ValueError("generation must be nonnegative")
        if self.parent is not None:
            if type(self.parent) is not SnapshotToken:
                raise TypeError("snapshot parent must be an exact SnapshotToken")
            if generation != self.parent.generation + 1:
                raise ValueError("successor generation must advance its parent once")


@dataclass(frozen=True)
class PeriodicRectGrid:
    """A positive rectangular grid whose row and column incidence is cyclic."""

    alphabet_size: int
    cells: Grid
    token: SnapshotToken = field(compare=False, repr=False)

    def __post_init__(self) -> None:
        checked_alphabet_size(self.alphabet_size)
        checked_grid(self.cells, self.alphabet_size)
        if type(self.token) is not SnapshotToken:
            raise TypeError("configuration token must be an exact SnapshotToken")

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self.cells), len(self.cells[0]))

    @property
    def generation(self) -> int:
        return self.token.generation


def make_grid(
    cells: object,
    alphabet_size: int = 2,
    *,
    generation: int = 0,
) -> PeriodicRectGrid:
    checked = checked_grid(cells, alphabet_size)
    return PeriodicRectGrid(alphabet_size, checked, SnapshotToken(generation))


@dataclass(frozen=True)
class AnyLabel:
    """Closed pattern atom corresponding to Wolfram Language Blank ``_``."""


ANY = AnyLabel()
PatternAtom = int | AnyLabel


@dataclass(frozen=True)
class ContextPattern:
    slots: tuple[PatternAtom, PatternAtom, PatternAtom, PatternAtom]

    def checked(self, alphabet_size: int) -> ContextPattern:
        size = checked_alphabet_size(alphabet_size)
        raw = exact_tuple(self.slots, "pattern slots")
        if len(raw) != 4:
            raise ValueError("pattern must contain exactly NW, N, W, Self")
        for atom in raw:
            if atom is ANY:
                continue
            label = exact_int(atom, "literal pattern atom")
            if label < 0 or label >= size:
                raise ValueError("literal pattern atom is outside the alphabet")
        return self

    def matches(self, context: Context4) -> bool:
        return all(atom is ANY or atom == label for atom, label in zip(self.slots, context))


@dataclass(frozen=True)
class PatternClause:
    pattern: ContextPattern
    patch: Patch


@dataclass(frozen=True)
class ClosedContextPatchTable:
    """Canonical exhaustive ``Sigma^4 -> positive rectangular patch`` data."""

    alphabet_size: int
    rows: tuple[tuple[Context4, Patch], ...]

    def __post_init__(self) -> None:
        size = checked_alphabet_size(self.alphabet_size)
        raw_rows = exact_tuple(self.rows, "table rows")
        checked_rows: list[tuple[Context4, Patch]] = []
        for row_index, raw_row in enumerate(raw_rows):
            row = exact_tuple(raw_row, f"table row {row_index}")
            if len(row) != 2:
                raise ValueError("table rows must be context/patch pairs")
            context = checked_context(row[0], size, "table input context")
            patch = checked_patch(row[1], size, name="table output patch")
            checked_rows.append((context, patch))
        expected = all_contexts(size)
        if tuple(context for context, _patch in checked_rows) != expected:
            raise ValueError("table must cover every context once in canonical order")

    def at(self, context: Context4) -> Patch:
        key = checked_context(context, self.alphabet_size)
        index = 0
        for label in key:
            index = index * self.alphabet_size + label
        row_context, patch = self.rows[index]
        if row_context != key:
            raise RuntimeError("canonical context-table invariant failed")
        return patch


@dataclass(frozen=True)
class ClosedOrderedPatternProgram:
    """Ordered Literal/Any clauses plus an explicit exhaustive lowering.

    Clause order is semantic first-match data.  Missing coverage is invalid.
    The original clauses remain stored because lowering overlapping or shadowed
    clauses to an exhaustive table is denotational, not a lossless source-syntax
    representation.  An exact importer for an incomplete Wolfram ``ReplaceAll``
    rule list must materialize the unmatched expressions explicitly; the core
    schema never treats host fallback as a patch row.
    """

    alphabet_size: int
    clauses: tuple[PatternClause, ...]
    table: ClosedContextPatchTable = field(init=False)

    def __post_init__(self) -> None:
        size = checked_alphabet_size(self.alphabet_size)
        clauses = exact_tuple(self.clauses, "pattern clauses")
        if not clauses:
            raise ValueError("pattern program requires at least one clause")
        for clause in clauses:
            if type(clause) is not PatternClause:
                raise TypeError("pattern clauses must be exact PatternClause values")
            if type(clause.pattern) is not ContextPattern:
                raise TypeError("clause pattern must be an exact ContextPattern")
            clause.pattern.checked(size)
            checked_patch(clause.patch, size, name="clause output patch")

        rows: list[tuple[Context4, Patch]] = []
        for context in all_contexts(size):
            selected: PatternClause | None = None
            for clause in clauses:
                if clause.pattern.matches(context):
                    selected = clause
                    break
            if selected is None:
                raise ValueError(f"pattern program does not cover context {context}")
            rows.append((context, selected.patch))
        object.__setattr__(self, "table", ClosedContextPatchTable(size, tuple(rows)))


OCR_MINUS = "-"
RAW_BOOK_13806_PATTERN: tuple[tuple[object, object], tuple[object, object]] = (
    (OCR_MINUS, 1),
    (0, 1),
)
BOOK_13806_PATCH: Patch = ((1, 0), (1, 1))


def guarded_repair_book_13806_pattern(
    raw: object,
) -> ContextPattern:
    """Repair exactly the one bare OCR minus into one Blank wildcard."""

    outer = exact_tuple(raw, "BOOK:13806 raw pattern")
    if len(outer) != 2:
        raise ValueError("BOOK:13806 raw pattern must have two rows")
    flattened: list[object] = []
    for raw_row in outer:
        row = exact_tuple(raw_row, "BOOK:13806 raw pattern row")
        if len(row) != 2:
            raise ValueError("BOOK:13806 raw pattern rows must have length two")
        flattened.extend(row)
    if flattened.count(OCR_MINUS) != 1:
        raise ValueError("BOOK:13806 repair requires exactly one bare OCR minus")
    repaired: list[PatternAtom] = []
    for atom in flattened:
        if atom == OCR_MINUS:
            repaired.append(ANY)
        else:
            repaired.append(exact_int(atom, "BOOK:13806 literal"))
    return ContextPattern((repaired[0], repaired[1], repaired[2], repaired[3]))


BOOK_13806_PATTERN = guarded_repair_book_13806_pattern(RAW_BOOK_13806_PATTERN)


@dataclass(frozen=True)
class TileHandle:
    token: SnapshotToken = field(repr=False)
    row: int
    column: int


@dataclass(frozen=True)
class ContextRead:
    source: TileHandle
    values: Context4


@dataclass(frozen=True)
class PatchWrite:
    source: TileHandle
    context: Context4
    patch: Patch


@dataclass(frozen=True)
class ChildRectangle:
    source: TileHandle
    row_start: int
    row_stop: int
    column_start: int
    column_stop: int


@dataclass(frozen=True)
class GridChildOccurrence:
    source: TileHandle
    local_row: int
    local_column: int
    target_row: int
    target_column: int
    label: int


@dataclass(frozen=True)
class Advanced:
    changed: bool


@dataclass(frozen=True)
class IncompatibleMosaic:
    kind: str
    source_row: int | None
    expected: int
    actual: int


@dataclass(frozen=True)
class Invalid:
    reason: IncompatibleMosaic


@dataclass(frozen=True)
class PatchStep:
    source_token: SnapshotToken = field(repr=False)
    successor: PeriodicRectGrid
    reads: tuple[ContextRead, ...]
    writes: tuple[PatchWrite, ...]
    child_rectangles: tuple[ChildRectangle, ...]
    child_occurrences: tuple[GridChildOccurrence, ...]


@dataclass(frozen=True)
class PatchStepResult:
    outcome: Advanced | Invalid
    successors: tuple[PeriodicRectGrid, ...]
    step: PatchStep | None


def all_old_tiles(configuration: PeriodicRectGrid) -> tuple[TileHandle, ...]:
    height, width = configuration.shape
    return tuple(
        TileHandle(configuration.token, row, column)
        for row in range(height)
        for column in range(width)
    )


def validate_active(
    configuration: PeriodicRectGrid,
    active: tuple[TileHandle, ...],
) -> None:
    if type(active) is not tuple:
        raise TypeError("active frontier must be an exact tuple")
    expected_coords = {
        (row, column)
        for row in range(configuration.shape[0])
        for column in range(configuration.shape[1])
    }
    observed: set[Coord2] = set()
    for source in active:
        if type(source) is not TileHandle:
            raise TypeError("active source must be an exact TileHandle")
        if source.token is not configuration.token:
            raise ValueError("active source is stale or foreign")
        row = exact_int(source.row, "source row")
        column = exact_int(source.column, "source column")
        coord = (row, column)
        if coord not in expected_coords:
            raise ValueError("active source is outside the old configuration")
        if coord in observed:
            raise ValueError("active frontier contains a duplicate source")
        observed.add(coord)
    if observed != expected_coords:
        raise ValueError("T28 frontier must cover every old tile exactly once")


def read_periodic_nw_n_w_self(
    configuration: PeriodicRectGrid,
    active: tuple[TileHandle, ...],
) -> tuple[ContextRead, ...]:
    validate_active(configuration, active)
    height, width = configuration.shape
    reads: list[ContextRead] = []
    for source in active:
        values = tuple(
            configuration.cells[(source.row + dr) % height][(source.column + dc) % width]
            for dr, dc in SLOT_OFFSETS
        )
        context: Context4 = (values[0], values[1], values[2], values[3])
        reads.append(ContextRead(source, context))
    return tuple(reads)


def apply_context_table(
    table: ClosedContextPatchTable,
    active: tuple[TileHandle, ...],
    reads: tuple[ContextRead, ...],
) -> tuple[PatchWrite, ...]:
    if len(active) != len(reads):
        raise ValueError("RULE requires one read per active source")
    writes: list[PatchWrite] = []
    for source, read in zip(active, reads, strict=True):
        if type(read) is not ContextRead or read.source != source:
            raise ValueError("context read is not bound to its active source")
        writes.append(PatchWrite(source, read.values, table.at(read.values)))
    return tuple(writes)


def invalid_result(reason: IncompatibleMosaic) -> PatchStepResult:
    return PatchStepResult(Invalid(reason), (), None)


def apply_ranked_block_mosaic(
    old: PeriodicRectGrid,
    active: tuple[TileHandle, ...],
    reads: tuple[ContextRead, ...],
    writes: tuple[PatchWrite, ...],
) -> PatchStepResult:
    """Apply the existing T26 rank-two product assembler, not a T28 UPDATE."""

    validate_active(old, active)
    if type(reads) is not tuple or type(writes) is not tuple:
        raise TypeError("reads and writes must be exact tuples")
    if len(reads) != len(active) or len(writes) != len(active):
        raise ValueError("UPDATE requires exact read/write coverage")

    expected_coords = {(source.row, source.column) for source in active}
    read_by_coord: dict[Coord2, ContextRead] = {}
    for read in reads:
        if type(read) is not ContextRead:
            raise TypeError("read must be an exact ContextRead")
        source = read.source
        if source.token is not old.token:
            raise ValueError("read is stale or foreign")
        coord = (source.row, source.column)
        if coord not in expected_coords or coord in read_by_coord:
            raise ValueError("read coverage does not match the old frontier")
        checked_context(read.values, old.alphabet_size, "read context")
        read_by_coord[coord] = read
    if set(read_by_coord) != expected_coords:
        raise ValueError("read coverage does not match the old frontier")

    write_by_coord: dict[Coord2, PatchWrite] = {}
    for write in writes:
        if type(write) is not PatchWrite:
            raise TypeError("write must be an exact PatchWrite")
        source = write.source
        if source.token is not old.token:
            raise ValueError("write is stale or foreign")
        coord = (source.row, source.column)
        if coord not in expected_coords or coord in write_by_coord:
            raise ValueError("write coverage does not match the old frontier")
        context = checked_context(write.context, old.alphabet_size, "write context")
        if context != read_by_coord[coord].values:
            raise ValueError("write context does not match the old-snapshot read")
        checked_patch(write.patch, old.alphabet_size, name="emitted patch")
        write_by_coord[coord] = write
    if set(write_by_coord) != expected_coords:
        raise ValueError("write coverage does not match the old frontier")

    old_height, old_width = old.shape
    row_heights: list[int] = []
    slab_widths: list[int] = []
    for row in range(old_height):
        first_height = patch_shape(write_by_coord[(row, 0)].patch)[0]
        slab_width = 0
        for column in range(old_width):
            patch = write_by_coord[(row, column)].patch
            height, width = patch_shape(patch)
            if height != first_height:
                return invalid_result(
                    IncompatibleMosaic("row_patch_height", row, first_height, height)
                )
            slab_width += width
        row_heights.append(first_height)
        slab_widths.append(slab_width)

    expected_slab_width = slab_widths[0]
    for row, width in enumerate(slab_widths[1:], start=1):
        if width != expected_slab_width:
            return invalid_result(
                IncompatibleMosaic("row_slab_width", row, expected_slab_width, width)
            )

    row_offsets: list[int] = []
    cursor = 0
    for height in row_heights:
        row_offsets.append(cursor)
        cursor += height

    assembled: list[tuple[int, ...]] = []
    rectangles: list[ChildRectangle] = []
    children: list[GridChildOccurrence] = []
    for row in range(old_height):
        column_offsets: list[int] = []
        column_cursor = 0
        for column in range(old_width):
            column_offsets.append(column_cursor)
            column_cursor += patch_shape(write_by_coord[(row, column)].patch)[1]

        for local_row in range(row_heights[row]):
            assembled_row: list[int] = []
            for column in range(old_width):
                assembled_row.extend(write_by_coord[(row, column)].patch[local_row])
            assembled.append(tuple(assembled_row))

        for column in range(old_width):
            write = write_by_coord[(row, column)]
            patch = write.patch
            patch_height, patch_width = patch_shape(patch)
            row_start = row_offsets[row]
            column_start = column_offsets[column]
            rectangles.append(
                ChildRectangle(
                    write.source,
                    row_start,
                    row_start + patch_height,
                    column_start,
                    column_start + patch_width,
                )
            )
            for local_row in range(patch_height):
                for local_column in range(patch_width):
                    children.append(
                        GridChildOccurrence(
                            write.source,
                            local_row,
                            local_column,
                            row_start + local_row,
                            column_start + local_column,
                            patch[local_row][local_column],
                        )
                    )

    successor_cells = tuple(assembled)
    successor = PeriodicRectGrid(
        old.alphabet_size,
        successor_cells,
        SnapshotToken(old.generation + 1, old.token),
    )
    canonical_reads = tuple(
        read_by_coord[(row, column)]
        for row in range(old_height)
        for column in range(old_width)
    )
    canonical_writes = tuple(
        write_by_coord[(row, column)]
        for row in range(old_height)
        for column in range(old_width)
    )
    step = PatchStep(
        old.token,
        successor,
        canonical_reads,
        canonical_writes,
        tuple(rectangles),
        tuple(children),
    )
    return PatchStepResult(
        Advanced(successor.cells != old.cells),
        (successor,),
        step,
    )


def generic_step(
    old: PeriodicRectGrid,
    table: ClosedContextPatchTable,
) -> PatchStepResult:
    if table.alphabet_size != old.alphabet_size:
        raise ValueError("rule table and configuration alphabets differ")
    active = all_old_tiles(old)
    reads = read_periodic_nw_n_w_self(old, active)
    writes = apply_context_table(table, active, reads)
    return apply_ranked_block_mosaic(old, active, reads, writes)


def direct_partition_windows(cells: Grid) -> tuple[tuple[Context4, ...], ...]:
    """Independent cyclic-padding construction for Partition[..., -1]."""

    padded_rows = (cells[-1],) + cells
    padded = tuple((row[-1],) + row for row in padded_rows)
    height = len(cells)
    width = len(cells[0])
    out: list[tuple[Context4, ...]] = []
    for row in range(height):
        contexts: list[Context4] = []
        for column in range(width):
            contexts.append(
                (
                    padded[row][column],
                    padded[row][column + 1],
                    padded[row + 1][column],
                    padded[row + 1][column + 1],
                )
            )
        out.append(tuple(contexts))
    return tuple(out)


def direct_flatten2d(patches: tuple[tuple[Patch, ...], ...]) -> Grid | None:
    """Independent typed analogue of the source's Flatten2D expression."""

    row_heights: list[int] = []
    slabs: list[tuple[tuple[int, ...], ...]] = []
    for patch_row in patches:
        height = len(patch_row[0])
        if any(len(patch) != height for patch in patch_row):
            return None
        row_heights.append(height)
        slab: list[tuple[int, ...]] = []
        for local_row in range(height):
            slab.append(tuple(value for patch in patch_row for value in patch[local_row]))
        slabs.append(tuple(slab))
    slab_widths = tuple(len(slab[0]) for slab in slabs)
    if len(set(slab_widths)) != 1:
        return None
    return tuple(row for slab in slabs for row in slab)


def direct_notes_step(cells: Grid, table: ClosedContextPatchTable) -> Grid | None:
    windows = direct_partition_windows(cells)
    patches = tuple(
        tuple(table.at(context) for context in context_row)
        for context_row in windows
    )
    return direct_flatten2d(patches)


def verify_success_result(old: PeriodicRectGrid, result: PatchStepResult) -> None:
    if type(result.outcome) is not Advanced:
        raise AssertionError("expected an Advanced result")
    assert len(result.successors) == 1
    assert result.step is not None
    step = result.step
    successor = result.successors[0]
    assert step.successor is successor
    assert step.source_token is old.token
    assert successor.token is not old.token
    assert successor.token.parent is old.token
    assert successor.generation == old.generation + 1
    assert result.outcome.changed == (successor.cells != old.cells)
    assert len(step.reads) == old.shape[0] * old.shape[1]
    assert len(step.writes) == old.shape[0] * old.shape[1]
    assert len(step.child_rectangles) == old.shape[0] * old.shape[1]

    targets: dict[Coord2, int] = {}
    for child in step.child_occurrences:
        assert child.source.token is old.token
        target = (child.target_row, child.target_column)
        assert target not in targets
        targets[target] = child.label
    expected_targets = {
        (row, column): successor.cells[row][column]
        for row in range(successor.shape[0])
        for column in range(successor.shape[1])
    }
    assert targets == expected_targets

    for rectangle, write in zip(step.child_rectangles, step.writes, strict=True):
        assert rectangle.source == write.source
        extracted = tuple(
            successor.cells[row][rectangle.column_start : rectangle.column_stop]
            for row in range(rectangle.row_start, rectangle.row_stop)
        )
        assert extracted == write.patch


def binary_basis_table(rule_number: int) -> ClosedContextPatchTable:
    number = exact_int(rule_number, "bounded rule number")
    if number < 0 or number >= 2**16:
        raise ValueError("bounded rule number must be in 0..65535")
    patch_zero: Patch = ((0, 0), (0, 1))
    patch_one: Patch = ((1, 0), (1, 1))
    rows = tuple(
        (context, patch_one if (number >> index) & 1 else patch_zero)
        for index, context in enumerate(BINARY_CONTEXTS)
    )
    return ClosedContextPatchTable(2, rows)


DEBRUIJN_TORUS: Grid = (
    (0, 0, 0, 1),
    (0, 0, 1, 0),
    (1, 0, 1, 1),
    (0, 1, 1, 1),
)


def audit_periodic_alignment() -> tuple[int, int]:
    configurations = 0
    reads_checked = 0
    for height in range(1, 4):
        for width in range(1, 4):
            for flat in product(BITS, repeat=height * width):
                cells = tuple(
                    tuple(flat[row * width : (row + 1) * width])
                    for row in range(height)
                )
                old = make_grid(cells)
                active = all_old_tiles(old)
                generic = read_periodic_nw_n_w_self(old, active)
                direct = tuple(
                    context
                    for context_row in direct_partition_windows(cells)
                    for context in context_row
                )
                assert tuple(read.values for read in generic) == direct
                assert tuple(read.source for read in generic) == active
                configurations += 1
                reads_checked += len(active)
    assert configurations == 682
    assert reads_checked == 5_506

    singleton = make_grid(((1,),))
    singleton_read = read_periodic_nw_n_w_self(singleton, all_old_tiles(singleton))[0]
    assert singleton_read.values == (1, 1, 1, 1)
    return configurations, reads_checked


def audit_book_row_and_pattern_lowering() -> tuple[int, int]:
    pattern = BOOK_13806_PATTERN.checked(2)
    assert pattern.slots == (ANY, 1, 0, 1)
    matching = tuple(context for context in BINARY_CONTEXTS if pattern.matches(context))
    assert matching == ((0, 1, 0, 1), (1, 1, 0, 1))

    fallback_patch: Patch = ((0, 0), (0, 0))
    explicit_default = PatternClause(ContextPattern((ANY, ANY, ANY, ANY)), fallback_patch)
    source_clause = PatternClause(pattern, BOOK_13806_PATCH)
    program = ClosedOrderedPatternProgram(2, (source_clause, explicit_default))
    for context in BINARY_CONTEXTS:
        expected = BOOK_13806_PATCH if pattern.matches(context) else fallback_patch
        assert program.table.at(context) == expected

    # Rule priority is semantic for overlapping patterns.  Reversing the
    # explicit clauses shadows the source row and changes the lowered function.
    reversed_program = ClosedOrderedPatternProgram(2, (explicit_default, source_clause))
    for context in matching:
        assert reversed_program.table.at(context) == fallback_patch
        assert reversed_program.table.at(context) != program.table.at(context)

    # Exact exhaustive clauses have a transparent inverse back to table rows.
    exact_clauses = tuple(
        PatternClause(ContextPattern(context), patch)
        for context, patch in program.table.rows
    )
    exact_program = ClosedOrderedPatternProgram(2, exact_clauses)
    assert exact_program.table == program.table
    assert tuple((clause.pattern.slots, clause.patch) for clause in exact_clauses) == program.table.rows

    old = make_grid(DEBRUIJN_TORUS)
    result = generic_step(old, program.table)
    verify_success_result(old, result)
    assert result.successors[0].cells == direct_notes_step(old.cells, program.table)
    source_row_reads = tuple(
        read for read in result.step.reads if pattern.matches(read.values)  # type: ignore[union-attr]
    )
    assert len(source_row_reads) == 2
    for read in source_row_reads:
        write = next(
            write for write in result.step.writes if write.source == read.source  # type: ignore[union-attr]
        )
        assert write.patch == BOOK_13806_PATCH

    return len(matching), len(BINARY_CONTEXTS)


def audit_bounded_commutation() -> tuple[int, int, int]:
    contexts = tuple(
        context
        for row in direct_partition_windows(DEBRUIJN_TORUS)
        for context in row
    )
    assert len(contexts) == 16
    assert set(contexts) == set(BINARY_CONTEXTS)
    assert len(set(contexts)) == 16

    old = make_grid(DEBRUIJN_TORUS)
    event_count = 0
    firing_count = 0
    child_count = 0
    for rule_number in range(2**16):
        table = binary_basis_table(rule_number)
        direct = direct_notes_step(old.cells, table)
        assert direct is not None
        generic = generic_step(old, table)
        assert type(generic.outcome) is Advanced
        assert len(generic.successors) == 1
        assert generic.step is not None
        assert generic.successors[0].cells == direct
        assert len(generic.step.reads) == 16
        assert len(generic.step.child_occurrences) == 64
        event_count += 1
        firing_count += len(generic.step.reads)
        child_count += len(generic.step.child_occurrences)
    assert event_count == 65_536
    assert firing_count == 1_048_576
    assert child_count == 4_194_304
    return event_count, firing_count, child_count


def table_from_function(
    function: Callable[[Context4], Patch],
    *,
    alphabet_size: int = 2,
) -> ClosedContextPatchTable:
    if not callable(function):
        raise TypeError("test table builder requires a callable")
    # This helper exists only inside the oracle.  The resulting program data is
    # the closed table; runtime specifications must never store this callback.
    return ClosedContextPatchTable(
        alphabet_size,
        tuple((context, function(context)) for context in all_contexts(alphabet_size)),
    )


def wrong_in_place_step(cells: Grid, table: ClosedContextPatchTable) -> Grid:
    """Deliberately prohibited sequential mutation for a singleton-patch table."""

    mutable = [list(row) for row in cells]
    height = len(mutable)
    width = len(mutable[0])
    for row in range(height):
        for column in range(width):
            context: Context4 = (
                mutable[(row - 1) % height][(column - 1) % width],
                mutable[(row - 1) % height][column],
                mutable[row][(column - 1) % width],
                mutable[row][column],
            )
            patch = table.at(context)
            if patch_shape(patch) != (1, 1):
                raise ValueError("wrong in-place control requires singleton patches")
            mutable[row][column] = patch[0][0]
    return tuple(tuple(row) for row in mutable)


def wrong_flat_patch_concatenation(writes: tuple[PatchWrite, ...]) -> tuple[int, ...]:
    return tuple(
        label
        for write in writes
        for patch_row in write.patch
        for label in patch_row
    )


def audit_schedule_boundary_and_assembly() -> dict[str, int]:
    counts = {
        "snapshot": 0,
        "boundary": 0,
        "identity": 0,
        "mixed_compatible": 0,
        "typed_invalid": 0,
        "permutation": 0,
        "flat_rejected": 0,
        "adaptive_boundary": 0,
    }

    # Snapshot parallelism/newborn deferral: sequential mutation changes later
    # reads and gives an all-zero row instead of the correct checker pattern.
    xor_table = table_from_function(lambda context: ((context[1] ^ context[2],),))
    old = make_grid(((1, 0), (0, 0)))
    result = generic_step(old, xor_table)
    verify_success_result(old, result)
    assert result.successors[0].cells == ((0, 1), (1, 0))
    assert wrong_in_place_step(old.cells, xor_table) == ((0, 0), (0, 0))
    assert wrong_in_place_step(old.cells, xor_table) != result.successors[0].cells
    counts["snapshot"] += 1

    # Wrap occurs independently in both axes and slot multiplicity is retained.
    boundary_old = make_grid(((0, 1, 1), (1, 0, 0)))
    reads = read_periodic_nw_n_w_self(boundary_old, all_old_tiles(boundary_old))
    source_00 = next(read for read in reads if (read.source.row, read.source.column) == (0, 0))
    assert source_00.values == (0, 1, 1, 0)
    fixed_zero_context = (0, 0, 0, 0)
    reflected_context = (0, 0, 0, 0)
    assert source_00.values != fixed_zero_context
    assert source_00.values != reflected_context
    counts["boundary"] += 1

    # Applicable identity remains Advanced(changed=false), not halt/quiescence.
    identity_table = table_from_function(lambda context: ((context[3],),))
    identity_old = make_grid(((0, 1, 0), (1, 1, 0)))
    identity = generic_step(identity_old, identity_table)
    verify_success_result(identity_old, identity)
    assert identity.successors[0].cells == identity_old.cells
    assert identity.outcome == Advanced(False)
    counts["identity"] += 1

    # Context-dependent crossed widths: both slabs have width three, although
    # each old source column sees patch widths {1,2}.  Per-column equality is
    # not a T26/T28 invariant.
    crossed_old = make_grid(((0, 1), (1, 0)))
    context_a = (0, 1, 1, 0)
    context_b = (1, 0, 0, 1)
    patch_a: Patch = ((0,),)
    patch_b: Patch = ((1, 0),)
    crossed_table = table_from_function(
        lambda context: patch_a if context == context_a else patch_b
    )
    crossed = generic_step(crossed_old, crossed_table)
    verify_success_result(crossed_old, crossed)
    assert crossed.successors[0].shape == (2, 3)
    assert crossed.successors[0].cells == ((0, 1, 0), (1, 0, 0))
    assert direct_notes_step(crossed_old.cells, crossed_table) == crossed.successors[0].cells
    assert {
        patch_shape(crossed.step.writes[index].patch)[1]  # type: ignore[union-attr]
        for index in (0, 2)
    } == {1, 2}
    counts["mixed_compatible"] += 1

    # Write materialization order is incidental; source product addresses own
    # placement.  Reverse all reads/writes and obtain the same semantic result.
    active = all_old_tiles(crossed_old)
    crossed_reads = read_periodic_nw_n_w_self(crossed_old, active)
    crossed_writes = apply_context_table(crossed_table, active, crossed_reads)
    permuted = apply_ranked_block_mosaic(
        crossed_old,
        active,
        tuple(reversed(crossed_reads)),
        tuple(reversed(crossed_writes)),
    )
    verify_success_result(crossed_old, permuted)
    assert permuted.successors[0] == crossed.successors[0]
    counts["permutation"] += 1

    # Product assembly cannot be replaced by flattening source patches.
    nonsymmetric_table = table_from_function(
        lambda context: ((context[0], context[1]), (context[2], context[3]))
    )
    flat_old = make_grid(((0, 1), (1, 1)))
    flat_result = generic_step(flat_old, nonsymmetric_table)
    verify_success_result(flat_old, flat_result)
    flat_stream = wrong_flat_patch_concatenation(flat_result.step.writes)  # type: ignore[union-attr]
    correct_stream = tuple(label for row in flat_result.successors[0].cells for label in row)
    assert flat_stream != correct_stream
    counts["flat_rejected"] += 1

    # Unequal patch heights inside one source row produce a typed no-commit
    # result.  This is also the smallest adjacent coarse/fine subdivision
    # counterexample against claiming the strict rectangular assembler is total.
    tall_patch: Patch = ((1,), (0,))
    incompatible_height_table = table_from_function(
        lambda context: patch_a if context == context_a else tall_patch
    )
    before_cells = crossed_old.cells
    before_token = crossed_old.token
    invalid_height = generic_step(crossed_old, incompatible_height_table)
    assert invalid_height == PatchStepResult(
        Invalid(IncompatibleMosaic("row_patch_height", 0, 1, 2)), (), None
    )
    assert crossed_old.cells == before_cells and crossed_old.token is before_token
    counts["typed_invalid"] += 1
    counts["adaptive_boundary"] += 1

    # Equal heights do not suffice: row slabs must have a common total width.
    slab_old = make_grid(((0, 0, 1), (0, 1, 1)))
    wide_only_row_zero = (0, 1, 0, 0)
    incompatible_width_table = table_from_function(
        lambda context: patch_b if context == wide_only_row_zero else patch_a
    )
    invalid_width = generic_step(slab_old, incompatible_width_table)
    assert invalid_width == PatchStepResult(
        Invalid(IncompatibleMosaic("row_slab_width", 1, 4, 3)), (), None
    )
    assert slab_old.cells == ((0, 0, 1), (0, 1, 1))
    assert slab_old.generation == 0
    counts["typed_invalid"] += 1

    # A coarse edge can meet 2^n fine descendants after n unequal subdivisions;
    # no fixed finite context arity bounds the warned adaptive variant.
    touching_counts = tuple(2**depth for depth in range(9))
    assert touching_counts == (1, 2, 4, 8, 16, 32, 64, 128, 256)
    assert all(right > left for left, right in zip(touching_counts, touching_counts[1:]))

    return counts


def expect_error(
    expected: type[BaseException],
    operation: Callable[[], object],
) -> None:
    try:
        operation()
    except expected:
        return
    except BaseException as exc:  # pragma: no cover - diagnostic guard
        raise AssertionError(f"expected {expected.__name__}, got {type(exc).__name__}") from exc
    raise AssertionError(f"expected {expected.__name__}")


def audit_hostile_rejections() -> int:
    rejects = 0

    def reject(expected: type[BaseException], operation: Callable[[], object]) -> None:
        nonlocal rejects
        expect_error(expected, operation)
        rejects += 1

    reject(TypeError, lambda: checked_alphabet_size(True))
    reject(ValueError, lambda: checked_alphabet_size(1))
    reject(TypeError, lambda: checked_grid([[0]], 2))
    reject(ValueError, lambda: checked_grid((), 2))
    reject(ValueError, lambda: checked_grid(((),), 2))
    reject(ValueError, lambda: checked_grid(((0,), (0, 1)), 2))
    reject(TypeError, lambda: checked_grid(((False,),), 2))
    reject(ValueError, lambda: checked_grid(((2,),), 2))
    reject(TypeError, lambda: PeriodicRectGrid(2, ((0,),), "token"))  # type: ignore[arg-type]
    reject(ValueError, lambda: SnapshotToken(-1))
    reject(ValueError, lambda: SnapshotToken(3, SnapshotToken(1)))

    reject(TypeError, lambda: checked_context([0, 0, 0, 0], 2))
    reject(ValueError, lambda: checked_context((0, 0, 0), 2))
    reject(ValueError, lambda: checked_context((0, 0, 0, 2), 2))
    reject(TypeError, lambda: checked_context((0, 0, 0, False), 2))
    reject(TypeError, lambda: checked_patch([[0]], 2))
    reject(ValueError, lambda: checked_patch((), 2))
    reject(ValueError, lambda: checked_patch(((),), 2))
    reject(ValueError, lambda: checked_patch(((0,), (0, 1)), 2))
    reject(ValueError, lambda: checked_patch(((2,),), 2))

    complete_rows = tuple((context, ((0,),)) for context in BINARY_CONTEXTS)
    reject(TypeError, lambda: ClosedContextPatchTable(2, list(complete_rows)))  # type: ignore[arg-type]
    reject(ValueError, lambda: ClosedContextPatchTable(2, complete_rows[:-1]))
    reject(
        ValueError,
        lambda: ClosedContextPatchTable(2, complete_rows[:-1] + (complete_rows[0],)),
    )
    reject(
        ValueError,
        lambda: ClosedContextPatchTable(2, tuple(reversed(complete_rows))),
    )
    reject(
        ValueError,
        lambda: ClosedContextPatchTable(2, complete_rows[:-1] + (((0, 0, 0, 2), ((0,),)),)),
    )
    reject(ValueError, lambda: binary_basis_table(-1))
    reject(ValueError, lambda: binary_basis_table(2**16))

    reject(
        ValueError,
        lambda: guarded_repair_book_13806_pattern((("_", 1), (0, 1))),
    )
    reject(
        ValueError,
        lambda: guarded_repair_book_13806_pattern(((OCR_MINUS, 1), (OCR_MINUS, 1))),
    )
    reject(
        ValueError,
        lambda: ContextPattern((ANY, 1, 0, 2)).checked(2),
    )
    reject(
        ValueError,
        lambda: ClosedOrderedPatternProgram(
            2,
            (PatternClause(BOOK_13806_PATTERN, BOOK_13806_PATCH),),
        ),
    )
    reject(
        TypeError,
        lambda: ClosedOrderedPatternProgram(2, ("callback",)),  # type: ignore[arg-type]
    )
    reject(
        TypeError,
        lambda: ClosedOrderedPatternProgram(2, (lambda _context: ((0,),),)),  # type: ignore[arg-type]
    )

    old = make_grid(((0, 1), (1, 0)))
    table = table_from_function(lambda context: ((context[3],),))
    active = all_old_tiles(old)
    reads = read_periodic_nw_n_w_self(old, active)
    writes = apply_context_table(table, active, reads)
    foreign_same_generation = make_grid(old.cells)
    stale = make_grid(old.cells, generation=1)
    reject(
        ValueError,
        lambda: read_periodic_nw_n_w_self(
            old,
            (TileHandle(foreign_same_generation.token, 0, 0),) + active[1:],
        ),
    )
    reject(
        ValueError,
        lambda: read_periodic_nw_n_w_self(
            old,
            (TileHandle(stale.token, 0, 0),) + active[1:],
        ),
    )
    reject(ValueError, lambda: read_periodic_nw_n_w_self(old, active[:-1]))
    reject(ValueError, lambda: read_periodic_nw_n_w_self(old, active + (active[0],)))
    reject(
        ValueError,
        lambda: read_periodic_nw_n_w_self(
            old,
            (TileHandle(old.token, 9, 0),) + active[1:],
        ),
    )
    reject(ValueError, lambda: apply_context_table(table, active, reads[:-1]))
    reject(
        ValueError,
        lambda: apply_context_table(
            table,
            active,
            (ContextRead(active[1], reads[0].values),) + reads[1:],
        ),
    )
    reject(
        ValueError,
        lambda: apply_ranked_block_mosaic(old, active, reads, writes[:-1]),
    )
    reject(
        ValueError,
        lambda: apply_ranked_block_mosaic(old, active, reads[:-1], writes),
    )
    reject(
        ValueError,
        lambda: apply_ranked_block_mosaic(
            old,
            active,
            reads,
            (writes[0],) + writes,
        ),
    )
    forged_context_write = PatchWrite(writes[0].source, (1, 1, 1, 1), writes[0].patch)
    reject(
        ValueError,
        lambda: apply_ranked_block_mosaic(
            old,
            active,
            reads,
            (forged_context_write,) + writes[1:],
        ),
    )
    foreign_write = PatchWrite(
        TileHandle(foreign_same_generation.token, 0, 0),
        writes[0].context,
        writes[0].patch,
    )
    reject(
        ValueError,
        lambda: apply_ranked_block_mosaic(
            old,
            active,
            reads,
            (foreign_write,) + writes[1:],
        ),
    )
    reject(ValueError, lambda: generic_step(old, ClosedContextPatchTable(3, tuple(
        (context, ((0,),)) for context in all_contexts(3)
    ))))

    reject(TypeError, lambda: table_from_function("callback"))  # type: ignore[arg-type]
    reject(ValueError, lambda: wrong_in_place_step(old.cells, binary_basis_table(0)))

    # Semantic shortcut controls are deliberately outside the closed schemas.
    reject(TypeError, lambda: checked_patch((b"raster",), 2))
    reject(TypeError, lambda: checked_grid(((lambda: 0,),), 2))
    reject(TypeError, lambda: checked_context((0, 0, 0, {"whole_grid": old.cells}), 2))

    assert rejects == 51
    return rejects


def audit_rule_counts() -> tuple[int, int]:
    # Derived structural counts, not source-authored integer codecs.
    binary_context_count = 2**4
    binary_patch_count = 2**4
    full_binary_2x2_table_count = binary_patch_count**binary_context_count
    bounded_basis_count = 2**binary_context_count
    assert full_binary_2x2_table_count == 2**64
    assert bounded_basis_count == 65_536
    return full_binary_2x2_table_count, bounded_basis_count


EXPECTED_DIGEST = "2f29901fa65a83b51f6841673172d1141b570e60d2c89d9478e2a10605456f40"


def main() -> None:
    alignment_configs, alignment_reads = audit_periodic_alignment()
    book_matches, compiled_contexts = audit_book_row_and_pattern_lowering()
    events, firings, children = audit_bounded_commutation()
    schedule = audit_schedule_boundary_and_assembly()
    hostile = audit_hostile_rejections()
    full_rule_count, bounded_rule_count = audit_rule_counts()

    facts = (
        ("alignment_configurations", alignment_configs),
        ("alignment_reads", alignment_reads),
        ("book_wildcard_matches", book_matches),
        ("compiled_contexts", compiled_contexts),
        ("bounded_commutations", events),
        ("bounded_firings", firings),
        ("bounded_children", children),
        ("schedule", tuple(sorted(schedule.items()))),
        ("hostile_rejections", hostile),
        ("typed_invalid_no_commit", schedule["typed_invalid"]),
        ("full_binary_2x2_table_count", full_rule_count),
        ("bounded_basis_count", bounded_rule_count),
        ("strict_update", "D132_RankedBlockMosaicAssemble_rank_2"),
        ("adaptive_unequal_subdivision", "unbounded_context_boundary"),
    )
    digest = sha256(repr(facts).encode("utf-8")).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FROZEN":
        assert digest == EXPECTED_DIGEST

    print("T28 semantic oracle: PASS")
    print(
        "periodic_alignment="
        f"{alignment_configs} configurations/{alignment_reads} NW,N,W,Self reads"
    )
    print(
        "source_row="
        f"guarded_minus_to_Blank; wildcard_matches={book_matches}; "
        f"compiled_contexts={compiled_contexts}; first_match_order=explicit"
    )
    print(
        "bounded_commutation="
        f"{events} events/{firings} firings/{children} child witnesses"
    )
    print(
        "composition="
        "periodic_context_access + closed_pattern_lowering + "
        "D132_RankedBlockMosaicAssemble(rank=2)"
    )
    print(
        "controls="
        f"hostile={hostile}; typed_invalid_no_commit={schedule['typed_invalid']}; "
        "compatible_mixed=1; adaptive_unequal_subdivision=unbounded-context boundary"
    )
    print(
        "rule_counts="
        f"full_binary_uniform_2x2={full_rule_count}; bounded_basis={bounded_rule_count}; "
        "no_source_numeric_codec"
    )
    print(f"semantic_digest={digest}")


if __name__ == "__main__":
    main()
