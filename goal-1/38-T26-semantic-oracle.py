#!/usr/bin/env python3
"""Independent semantic and architecture oracle for T26.

The source construction is a finite rectangular grid of tile labels in
discrete ``t+2D``.  Every old tile fires once, reads only its own old label,
and emits one nonempty rectangular patch from a total closed table.  ``UPDATE``
performs the Notes' ``Flatten2D`` mosaic assembly: patches selected within one
source row have equal heights, and the assembled slabs for all source rows
have equal widths.  The familiar uniform-patch profile is a restriction of
that law.  Source rows remain source rows, local patch rows are interleaved
within them, and local patch columns are joined within source columns.  New
tiles do not fire until the following event.

The generic evaluator below is one ranked ordered-block UPDATE policy.  Its
rank-one member accepts explicit selected old-source indices, consumes every
unselected source, preserves selected-source/child order, and retains epsilon;
its named uniform restriction requires a positive common block shape.  Rank
two is T26.  The direct Notes evaluator and generic evaluator commute one
event at a time.  State-dependent rank-two incompatibility returns the exact
typed no-successor outcome ``Invalid(IncompatibleMosaic)`` before commit.
A second exact commuting map embeds a rectangular grid as a restricted T27
bag of fully posed tile occurrences.  Its successor provenance is derived
independently on each side; an explicit two-token bijection proves equality
modulo opaque-token renaming while preserving typed lineage.  The embedding
is lossless only under a rectangular-tiling invariant; arbitrary free geometry
remains T27, and neighbor-dependent patch choice remains T28.

The Book's ``Other shapes`` encoded-label table is executed natively under
that compatibility law.  From seed ``{{3}}`` it has exact Fibonacci side
lengths 1, 2, 3, 5, 8, 13, and 21.  Incompatible mosaics are rejected before
assembly.  Rasters, display scale, coordinate formulae, and limiting fractals
likewise never become programs or state.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import prod
from typing import Callable


if not __debug__:
    raise RuntimeError("T26 semantic verification requires assertions; do not run with -O")


Grid = tuple[tuple[int, ...], ...]
Patch = Grid
Coord2 = tuple[int, int]


def exact_int(value: object, name: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{name} must be an exact int")
    return value


def exact_str(value: object, name: str) -> str:
    if type(value) is not str or not value:
        raise TypeError(f"{name} must be a nonempty exact str")
    return value


def exact_tuple(value: object, name: str) -> tuple[object, ...]:
    if type(value) is not tuple:
        raise TypeError(f"{name} must be an exact tuple")
    return value


def checked_alphabet_size(value: object) -> int:
    size = exact_int(value, "alphabet size")
    if size < 2:
        raise ValueError("strict T26 requires a finite alphabet with at least two labels")
    return size


def checked_patch(
    value: object,
    alphabet_size: int,
    *,
    expected_shape: tuple[int, int] | None = None,
    name: str = "patch",
) -> Patch:
    size = checked_alphabet_size(alphabet_size)
    rows = exact_tuple(value, name)
    if not rows:
        raise ValueError(f"{name} must have positive height")
    checked_rows: list[tuple[int, ...]] = []
    width: int | None = None
    for row_index, raw_row in enumerate(rows):
        row = exact_tuple(raw_row, f"{name} row")
        if not row:
            raise ValueError(f"{name} must have positive width")
        values: list[int] = []
        for column_index, raw_label in enumerate(row):
            label = exact_int(raw_label, f"{name}[{row_index},{column_index}]")
            if label < 0 or label >= size:
                raise ValueError(f"{name} label is outside the declared alphabet")
            values.append(label)
        if width is None:
            width = len(values)
        elif len(values) != width:
            raise ValueError(f"{name} rows must be rectangular")
        checked_rows.append(tuple(values))
    assert width is not None
    shape = (len(checked_rows), width)
    if expected_shape is not None and shape != expected_shape:
        raise ValueError(f"{name} shape {shape} does not match uniform shape {expected_shape}")
    return tuple(checked_rows)


@dataclass(frozen=True, eq=False)
class SnapshotToken:
    """Opaque identity with an inspectable parent chain."""

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
                raise ValueError("successor snapshot generation must advance its parent once")


@dataclass(frozen=True)
class RectGrid:
    alphabet_size: int
    cells: Grid
    token: SnapshotToken = field(compare=False, repr=False)

    def __post_init__(self) -> None:
        size = checked_alphabet_size(self.alphabet_size)
        checked_patch(self.cells, size, name="configuration")
        if type(self.token) is not SnapshotToken:
            raise TypeError("configuration token must be an exact SnapshotToken")

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self.cells), len(self.cells[0]))

    @property
    def generation(self) -> int:
        return self.token.generation


def make_grid(cells: object, alphabet_size: int, generation: int = 0) -> RectGrid:
    checked = checked_patch(cells, alphabet_size, name="configuration")
    return RectGrid(alphabet_size, checked, SnapshotToken(generation))


@dataclass(frozen=True)
class ClosedPatchTable:
    """Total finite ``TileLabel -> nonempty rectangular patch`` data."""

    alphabet_size: int
    rows: tuple[tuple[int, Patch], ...]

    def __post_init__(self) -> None:
        size = checked_alphabet_size(self.alphabet_size)
        raw_rows = exact_tuple(self.rows, "table rows")
        keys: list[int] = []
        for raw_row in raw_rows:
            row = exact_tuple(raw_row, "table row")
            if len(row) != 2:
                raise ValueError("table rows must be label/patch pairs")
            label = exact_int(row[0], "table input label")
            if label < 0 or label >= size:
                raise ValueError("table input label is outside the alphabet")
            patch = checked_patch(
                row[1],
                size,
                name="table output patch",
            )
            keys.append(label)
        if tuple(keys) != tuple(range(size)):
            raise ValueError("table rows must cover every label once in canonical order")

    @property
    def patch_shapes(self) -> tuple[tuple[int, int], ...]:
        return tuple((len(patch), len(patch[0])) for _label, patch in self.rows)

    @property
    def is_uniform(self) -> bool:
        return len(set(self.patch_shapes)) == 1

    @property
    def patch_shape(self) -> tuple[int, int]:
        if not self.is_uniform:
            raise ValueError("this operation requires one uniform patch shape")
        return self.patch_shapes[0]

    def at(self, label: int) -> Patch:
        key = exact_int(label, "table lookup label")
        if key < 0 or key >= self.alphabet_size:
            raise ValueError("table lookup label is outside the alphabet")
        row_key, patch = self.rows[key]
        if row_key != key:
            raise RuntimeError("closed table canonical-order invariant failed")
        return patch


@dataclass(frozen=True)
class TileHandle:
    token: SnapshotToken = field(repr=False)
    row: int
    column: int


@dataclass(frozen=True)
class TileRead:
    token: SnapshotToken = field(repr=False)
    source: TileHandle
    label: int


@dataclass(frozen=True)
class PatchWrite:
    token: SnapshotToken = field(repr=False)
    source: TileHandle
    old_label: int
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
class PatchStep:
    source_token: SnapshotToken = field(repr=False)
    successor: RectGrid
    child_rectangles: tuple[ChildRectangle, ...]
    child_occurrences: tuple[GridChildOccurrence, ...]


@dataclass(frozen=True)
class IncompatibleMosaic:
    """Typed state-dependent reason for a rank-two no-commit outcome."""

    code: str
    source_row: int | None
    observed_extents: tuple[int, ...]

    def __post_init__(self) -> None:
        code = exact_str(self.code, "mosaic incompatibility code")
        if code not in {"row_patch_heights", "row_slab_widths"}:
            raise ValueError("unknown mosaic incompatibility code")
        if self.source_row is not None:
            row = exact_int(self.source_row, "incompatible source row")
            if row < 0:
                raise ValueError("incompatible source row must be nonnegative")
        extents = exact_tuple(self.observed_extents, "observed mosaic extents")
        if not extents or any(exact_int(value, "observed extent") <= 0 for value in extents):
            raise ValueError("observed mosaic extents must be positive")


class IncompatibleMosaicError(Exception):
    """Strict-convenience unwrap of ``Invalid(IncompatibleMosaic)``."""

    def __init__(self, reason: IncompatibleMosaic) -> None:
        if type(reason) is not IncompatibleMosaic:
            raise TypeError("mosaic error requires an exact IncompatibleMosaic reason")
        self.reason = reason
        super().__init__(f"{reason.code}: {reason.observed_extents}")


@dataclass(frozen=True)
class Advanced:
    changed: bool

    def __post_init__(self) -> None:
        if type(self.changed) is not bool:
            raise TypeError("Advanced.changed must be an exact bool")


@dataclass(frozen=True)
class Invalid:
    reason: IncompatibleMosaic

    def __post_init__(self) -> None:
        if type(self.reason) is not IncompatibleMosaic:
            raise TypeError("Invalid requires an exact IncompatibleMosaic reason")


@dataclass(frozen=True)
class PatchStepResult:
    """Exact deterministic UPDATE envelope used for advance or invalidity."""

    outcome: Advanced | Invalid
    successors: tuple[RectGrid, ...]
    step: PatchStep | None

    def __post_init__(self) -> None:
        successors = exact_tuple(self.successors, "step-result successors")
        if type(self.outcome) is Advanced:
            if type(self.step) is not PatchStep:
                raise TypeError("Advanced result requires an exact PatchStep")
            if len(successors) != 1 or successors[0] is not self.step.successor:
                raise ValueError("Advanced result must expose exactly its committed successor")
        elif type(self.outcome) is Invalid:
            if self.step is not None or successors:
                raise ValueError("Invalid(IncompatibleMosaic) must not commit a successor")
        else:
            raise TypeError("step result requires exact Advanced or Invalid outcome")


def all_old_tiles(configuration: RectGrid) -> tuple[TileHandle, ...]:
    if type(configuration) is not RectGrid:
        raise TypeError("FRONTIER requires an exact RectGrid")
    height, width = configuration.shape
    return tuple(
        TileHandle(configuration.token, row, column)
        for row in range(height)
        for column in range(width)
    )


def read_self(
    configuration: RectGrid,
    active: tuple[TileHandle, ...],
) -> tuple[TileRead, ...]:
    if type(configuration) is not RectGrid:
        raise TypeError("NEIGHBORHOOD requires an exact RectGrid")
    handles = exact_tuple(active, "active frontier")
    height, width = configuration.shape
    reads: list[TileRead] = []
    for raw_source in handles:
        if type(raw_source) is not TileHandle:
            raise TypeError("active sources must be exact TileHandles")
        source = raw_source
        if source.token is not configuration.token:
            raise ValueError("source handle is stale or belongs to another snapshot")
        row = exact_int(source.row, "source row")
        column = exact_int(source.column, "source column")
        if row < 0 or row >= height or column < 0 or column >= width:
            raise ValueError("source handle is outside the old grid")
        reads.append(
            TileRead(configuration.token, source, configuration.cells[row][column])
        )
    return tuple(reads)


def make_patch_writes(
    configuration: RectGrid,
    table: ClosedPatchTable,
    active: tuple[TileHandle, ...],
    reads: tuple[TileRead, ...],
) -> tuple[PatchWrite, ...]:
    if type(configuration) is not RectGrid:
        raise TypeError("RULE requires an exact RectGrid")
    if type(table) is not ClosedPatchTable:
        raise TypeError("RULE requires exact closed patch-table data")
    if table.alphabet_size != configuration.alphabet_size:
        raise ValueError("table and configuration alphabets differ")
    handles = exact_tuple(active, "active frontier")
    read_values = exact_tuple(reads, "tile reads")
    if len(handles) != len(read_values):
        raise ValueError("RULE requires one read for every active source")
    writes: list[PatchWrite] = []
    for source, raw_read in zip(handles, read_values, strict=True):
        if type(raw_read) is not TileRead:
            raise TypeError("RULE reads must be exact TileReads")
        read = raw_read
        if read.token is not configuration.token or read.source != source:
            raise ValueError("RULE read provenance does not match the old source")
        if source.token is not configuration.token:
            raise ValueError("RULE source provenance does not match the old snapshot")
        expected = configuration.cells[source.row][source.column]
        if read.label != expected:
            raise ValueError("RULE read label does not match the old snapshot")
        writes.append(
            PatchWrite(
                configuration.token,
                source,
                read.label,
                table.at(read.label),
            )
        )
    return tuple(writes)


def flat_index(coordinate: tuple[int, ...], shape: tuple[int, ...]) -> int:
    if len(coordinate) != len(shape):
        raise ValueError("coordinate rank does not match shape rank")
    index = 0
    for axis_coordinate, extent in zip(coordinate, shape, strict=True):
        position = exact_int(axis_coordinate, "ranked coordinate")
        size = exact_int(extent, "ranked extent")
        if size <= 0 or position < 0 or position >= size:
            raise ValueError("ranked coordinate is outside positive shape")
        index = index * size + position
    return index


@dataclass(frozen=True)
class RankedSourceRegion:
    source_index: int
    selected: bool
    starts: tuple[int, ...]
    stops: tuple[int, ...]


@dataclass(frozen=True)
class RankedMosaicAssembly:
    shape: tuple[int, ...]
    values: tuple[int, ...]
    source_regions: tuple[RankedSourceRegion, ...]


def ranked_block_mosaic_assemble(
    old_shape: tuple[int, ...],
    block_shapes: tuple[tuple[int, ...], ...],
    blocks: tuple[tuple[int, ...], ...],
    *,
    selected_source_indices: tuple[int, ...] | None = None,
) -> RankedMosaicAssembly:
    """Ranked mosaic with explicit rank-one locus selection and consumption."""

    old = exact_tuple(old_shape, "old mosaic shape")
    shapes = exact_tuple(block_shapes, "mosaic block shapes")
    emitted = exact_tuple(blocks, "mosaic blocks")
    if len(old) not in (1, 2):
        raise ValueError("the evidenced ranked mosaic kernel supports rank one or two")
    old_extents = tuple(exact_int(value, "old mosaic extent") for value in old)
    if len(old_extents) == 1:
        if old_extents[0] < 0:
            raise ValueError("rank-one old extent must be nonnegative")
    elif any(value <= 0 for value in old_extents):
        raise ValueError("rank-two old mosaic extents must be positive")
    source_count = prod(old_extents)
    if selected_source_indices is None:
        selected = tuple(range(source_count))
    else:
        raw_selected = exact_tuple(selected_source_indices, "selected source indices")
        selected = tuple(exact_int(value, "selected source index") for value in raw_selected)
        if selected != tuple(sorted(set(selected))):
            raise ValueError("selected source indices must be unique and in source order")
        if any(value < 0 or value >= source_count for value in selected):
            raise ValueError("selected source index is outside the old support")
    if len(old_extents) == 2 and selected != tuple(range(source_count)):
        raise ValueError("rank-two T26 mosaic requires every old source exactly once")
    if len(shapes) != len(selected) or len(emitted) != len(selected):
        raise ValueError("mosaic blocks must cover every selected source exactly")

    checked_shapes: list[tuple[int, ...]] = []
    checked_blocks: list[tuple[int, ...]] = []
    for raw_shape, raw_values in zip(shapes, emitted, strict=True):
        shape = exact_tuple(raw_shape, "mosaic block shape")
        if len(shape) != len(old_extents):
            raise ValueError("mosaic block rank must equal old support rank")
        extents = tuple(exact_int(value, "mosaic block extent") for value in shape)
        if len(old_extents) == 1:
            if extents[0] < 0:
                raise ValueError("rank-one replacement length cannot be negative")
        elif any(value <= 0 for value in extents):
            raise ValueError("rank-two patch extents must be positive")
        values = exact_tuple(raw_values, "mosaic block")
        if len(values) != prod(extents):
            raise ValueError("mosaic block volume does not match its declared shape")
        checked_shapes.append(extents)
        checked_blocks.append(
            tuple(exact_int(value, "mosaic child label") for value in values)
        )

    if len(old_extents) == 1:
        cursor = 0
        values: list[int] = []
        regions: list[RankedSourceRegion] = []
        selected_position = 0
        for source_index in range(source_count):
            is_selected = (
                selected_position < len(selected)
                and selected[selected_position] == source_index
            )
            if is_selected:
                shape = checked_shapes[selected_position]
                block = checked_blocks[selected_position]
                stop = cursor + shape[0]
                regions.append(
                    RankedSourceRegion(source_index, True, (cursor,), (stop,))
                )
                values.extend(block)
                cursor = stop
                selected_position += 1
            else:
                regions.append(
                    RankedSourceRegion(source_index, False, (cursor,), (cursor,))
                )
        assert selected_position == len(selected)
        return RankedMosaicAssembly((cursor,), tuple(values), tuple(regions))

    old_height, old_width = old_extents
    row_heights: list[int] = []
    row_widths: list[int] = []
    for source_row in range(old_height):
        row_shapes = checked_shapes[
            source_row * old_width : (source_row + 1) * old_width
        ]
        heights = {shape[0] for shape in row_shapes}
        if len(heights) != 1:
            raise IncompatibleMosaicError(
                IncompatibleMosaic(
                    "row_patch_heights",
                    source_row,
                    tuple(sorted(heights)),
                )
            )
        row_heights.append(next(iter(heights)))
        row_widths.append(sum(shape[1] for shape in row_shapes))
    if len(set(row_widths)) != 1:
        raise IncompatibleMosaicError(
            IncompatibleMosaic(
                "row_slab_widths",
                None,
                tuple(row_widths),
            )
        )

    next_height = sum(row_heights)
    next_width = row_widths[0]
    result: list[int | None] = [None] * (next_height * next_width)
    regions: list[RankedSourceRegion] = []
    row_start = 0
    for source_row in range(old_height):
        column_start = 0
        for source_column in range(old_width):
            source_index = source_row * old_width + source_column
            patch_height, patch_width = checked_shapes[source_index]
            block = checked_blocks[source_index]
            regions.append(
                RankedSourceRegion(
                    source_index,
                    True,
                    (row_start, column_start),
                    (row_start + patch_height, column_start + patch_width),
                )
            )
            for local_row in range(patch_height):
                for local_column in range(patch_width):
                    target_index = (
                        (row_start + local_row) * next_width
                        + column_start
                        + local_column
                    )
                    if result[target_index] is not None:
                        raise RuntimeError("rank-two mosaic assembly produced an overlap")
                    result[target_index] = block[local_row * patch_width + local_column]
            column_start += patch_width
        assert column_start == next_width
        row_start += row_heights[source_row]
    assert row_start == next_height
    if any(value is None for value in result):
        raise RuntimeError("rank-two mosaic assembly left a hole")
    return RankedMosaicAssembly(
        (next_height, next_width),
        tuple(value for value in result if value is not None),
        tuple(regions),
    )


def ranked_block_assemble(
    old_shape: tuple[int, ...],
    block_shape: tuple[int, ...],
    blocks: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    """Uniform restriction retained as a compatibility wrapper."""

    old = exact_tuple(old_shape, "old ranked shape")
    block = exact_tuple(block_shape, "uniform block shape")
    emitted = exact_tuple(blocks, "ranked blocks")
    if not old or len(old) != len(block):
        raise ValueError("old and block shapes must have the same positive rank")
    old_extents = tuple(exact_int(value, "old extent") for value in old)
    if any(value <= 0 for value in old_extents):
        raise ValueError("old ranked extents must be positive")
    block_extents = tuple(exact_int(value, "uniform block extent") for value in block)
    if any(value <= 0 for value in block_extents):
        raise ValueError("uniform block extents must be positive")
    assembly = ranked_block_mosaic_assemble(
        old_extents,
        tuple(block_extents for _ in range(prod(old_extents))),
        emitted,
    )
    expected_shape = tuple(
        old_extent * block_extent
        for old_extent, block_extent in zip(old_extents, block_extents, strict=True)
    )
    if assembly.shape != expected_shape:
        raise RuntimeError("uniform mosaic wrapper produced the wrong ranked shape")
    return assembly.values


def apply_flatten2d(
    configuration: RectGrid,
    active: tuple[TileHandle, ...],
    writes: tuple[PatchWrite, ...],
) -> PatchStep:
    if type(configuration) is not RectGrid:
        raise TypeError("UPDATE requires an exact RectGrid")
    handles = exact_tuple(active, "active frontier")
    write_values = exact_tuple(writes, "patch writes")
    expected_active = all_old_tiles(configuration)
    if handles != expected_active:
        raise ValueError("strict T26 UPDATE requires every old tile exactly once in grid order")
    if len(write_values) != len(handles):
        raise ValueError("patch writes must cover the active frontier exactly")

    patch_shapes: list[tuple[int, int]] = []
    patches: list[Patch] = []
    blocks: list[tuple[int, ...]] = []
    rectangles: list[ChildRectangle] = []
    child_occurrences: list[GridChildOccurrence] = []
    for source, raw_write in zip(handles, write_values, strict=True):
        if type(raw_write) is not PatchWrite:
            raise TypeError("UPDATE writes must be exact PatchWrites")
        write = raw_write
        if write.token is not configuration.token or write.source != source:
            raise ValueError("patch-write provenance does not match the old snapshot")
        expected_label = configuration.cells[source.row][source.column]
        if write.old_label != expected_label:
            raise ValueError("patch write is not bound to the old source label")
        patch = checked_patch(
            write.patch,
            configuration.alphabet_size,
            name="emitted patch",
        )
        patch_shapes.append((len(patch), len(patch[0])))
        patches.append(patch)
        blocks.append(tuple(value for row in patch for value in row))

    old_height, old_width = configuration.shape
    assembly = ranked_block_mosaic_assemble(
        (old_height, old_width),
        tuple(patch_shapes),
        tuple(blocks),
    )
    next_height, next_width = assembly.shape
    cells = tuple(
        tuple(assembly.values[offset : offset + next_width])
        for offset in range(0, len(assembly.values), next_width)
    )
    assert len(cells) == next_height
    for source, patch, region in zip(
        handles,
        patches,
        assembly.source_regions,
        strict=True,
    ):
        if region.source_index != source.row * old_width + source.column:
            raise RuntimeError("mosaic region/source order invariant failed")
        row_start, column_start = region.starts
        row_stop, column_stop = region.stops
        rectangles.append(
            ChildRectangle(
                source,
                row_start,
                row_stop,
                column_start,
                column_stop,
            )
        )
        for local_row, patch_row in enumerate(patch):
            for local_column, label in enumerate(patch_row):
                child_occurrences.append(
                    GridChildOccurrence(
                        source,
                        local_row,
                        local_column,
                        row_start + local_row,
                        column_start + local_column,
                        label,
                    )
                )
    return PatchStep(
        configuration.token,
        RectGrid(
            configuration.alphabet_size,
            cells,
            SnapshotToken(configuration.generation + 1, configuration.token),
        ),
        tuple(rectangles),
        tuple(child_occurrences),
    )


def generic_step(table: ClosedPatchTable, configuration: RectGrid) -> PatchStep:
    """Strict convenience that unwraps the typed UPDATE result."""

    result = generic_step_result(table, configuration)
    if type(result.outcome) is Invalid:
        raise IncompatibleMosaicError(result.outcome.reason)
    assert type(result.step) is PatchStep
    return result.step


def apply_flatten2d_result(
    configuration: RectGrid,
    active: tuple[TileHandle, ...],
    writes: tuple[PatchWrite, ...],
) -> PatchStepResult:
    """Return ``Invalid(IncompatibleMosaic)`` without a successor or commit."""

    try:
        step = apply_flatten2d(configuration, active, writes)
    except IncompatibleMosaicError as error:
        return PatchStepResult(Invalid(error.reason), (), None)
    changed = step.successor.cells != configuration.cells
    return PatchStepResult(Advanced(changed), (step.successor,), step)


def generic_step_result(
    table: ClosedPatchTable,
    configuration: RectGrid,
) -> PatchStepResult:
    if type(table) is not ClosedPatchTable:
        raise TypeError("generic step requires an exact ClosedPatchTable")
    if type(configuration) is not RectGrid:
        raise TypeError("generic step requires an exact RectGrid")
    active = all_old_tiles(configuration)
    reads = read_self(configuration, active)
    writes = make_patch_writes(configuration, table, active, reads)
    return apply_flatten2d_result(configuration, active, writes)


def notes_flatten2d(block_grid: tuple[tuple[Patch, ...], ...]) -> Grid:
    """Independent direct reading of ``Apply[Join,Map[MapThread...]]``."""

    source_rows = exact_tuple(block_grid, "nested replacement blocks")
    if not source_rows:
        raise ValueError("Flatten2D source must have a positive number of rows")
    old_width: int | None = None
    result: list[tuple[int, ...]] = []
    result_width: int | None = None
    for source_row_index, raw_source_row in enumerate(source_rows):
        source_row = exact_tuple(raw_source_row, "nested replacement block row")
        if not source_row:
            raise ValueError("Flatten2D source rows must be nonempty")
        if old_width is None:
            old_width = len(source_row)
        elif len(source_row) != old_width:
            raise ValueError("Flatten2D source must be rectangular")
        checked_blocks: list[Patch] = []
        row_patch_height: int | None = None
        for raw_patch in source_row:
            patch = exact_tuple(raw_patch, "replacement patch")
            if not patch:
                raise ValueError("replacement patches must be nonempty")
            rows: list[tuple[int, ...]] = []
            for raw_row in patch:
                row = exact_tuple(raw_row, "replacement patch row")
                if not row:
                    raise ValueError("replacement patch rows must be nonempty")
                rows.append(tuple(exact_int(value, "replacement label") for value in row))
            if len({len(row) for row in rows}) != 1:
                raise ValueError("replacement patches must be rectangular")
            checked = tuple(rows)
            if row_patch_height is None:
                row_patch_height = len(checked)
            elif len(checked) != row_patch_height:
                raise IncompatibleMosaicError(
                    IncompatibleMosaic(
                        "row_patch_heights",
                        source_row_index,
                        (row_patch_height, len(checked)),
                    )
                )
            checked_blocks.append(checked)
        assert row_patch_height is not None
        slab = tuple(
            tuple(
                value
                for patch in checked_blocks
                for value in patch[local_row]
            )
            for local_row in range(row_patch_height)
        )
        slab_width = len(slab[0])
        if result_width is None:
            result_width = slab_width
        elif slab_width != result_width:
            raise IncompatibleMosaicError(
                IncompatibleMosaic(
                    "row_slab_widths",
                    None,
                    (result_width, slab_width),
                )
            )
        result.extend(slab)
    return tuple(result)


def native_step(table: ClosedPatchTable, cells: Grid) -> Grid:
    if type(table) is not ClosedPatchTable:
        raise TypeError("native step requires exact closed table data")
    old = checked_patch(cells, table.alphabet_size, name="native grid")
    nested = tuple(
        tuple(table.at(label) for label in row)
        for row in old
    )
    return notes_flatten2d(nested)


def assert_commutes(table: ClosedPatchTable, configuration: RectGrid) -> None:
    assert native_step(table, configuration.cells) == generic_step(table, configuration).successor.cells


def patch_from_flat(values: tuple[int, ...], shape: tuple[int, int]) -> Patch:
    height, width = shape
    if len(values) != height * width:
        raise ValueError("flat patch data has the wrong volume")
    return tuple(
        tuple(values[offset : offset + width])
        for offset in range(0, len(values), width)
    )


def binary_tables_2x2() -> tuple[ClosedPatchTable, ...]:
    patches = tuple(
        patch_from_flat(tuple(values), (2, 2))
        for values in product((0, 1), repeat=4)
    )
    return tuple(
        ClosedPatchTable(2, ((0, zero_patch), (1, one_patch)))
        for zero_patch, one_patch in product(patches, repeat=2)
    )


def binary_grids() -> tuple[RectGrid, ...]:
    grids: list[RectGrid] = []
    for height, width in ((1, 1), (1, 2), (2, 1), (2, 2)):
        for values in product((0, 1), repeat=height * width):
            cells = tuple(
                tuple(values[offset : offset + width])
                for offset in range(0, len(values), width)
            )
            grids.append(make_grid(cells, 2))
    return tuple(grids)


# ---------------------------------------------------------------------------
# Lossless restricted T27 bag representation
# ---------------------------------------------------------------------------


Matrix2 = tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]
Vector2 = tuple[Fraction, Fraction]


@dataclass(frozen=True)
class AffinePose2:
    linear: Matrix2
    translation: Vector2

    def __post_init__(self) -> None:
        rows = exact_tuple(self.linear, "affine linear rows")
        if len(rows) != 2 or any(type(row) is not tuple or len(row) != 2 for row in rows):
            raise ValueError("affine linear part must be an exact 2x2 tuple")
        translation = exact_tuple(self.translation, "affine translation")
        if len(translation) != 2:
            raise ValueError("affine translation must have two components")
        values = tuple(value for row in rows for value in row) + tuple(translation)
        if any(type(value) is not Fraction for value in values):
            raise TypeError("affine pose values must be exact Fractions")
        determinant = rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0]
        if determinant == 0:
            raise ValueError("affine tile pose must be nonsingular")


def diagonal_pose(scale_x: Fraction, scale_y: Fraction, x: Fraction, y: Fraction) -> AffinePose2:
    return AffinePose2(
        ((scale_x, Fraction(0)), (Fraction(0), scale_y)),
        (x, y),
    )


def compose_pose(parent: AffinePose2, child: AffinePose2) -> AffinePose2:
    if type(parent) is not AffinePose2 or type(child) is not AffinePose2:
        raise TypeError("pose composition requires exact AffinePose2 values")
    pa, pb = parent.linear, parent.translation
    ca, cb = child.linear, child.translation
    linear: Matrix2 = (
        (
            pa[0][0] * ca[0][0] + pa[0][1] * ca[1][0],
            pa[0][0] * ca[0][1] + pa[0][1] * ca[1][1],
        ),
        (
            pa[1][0] * ca[0][0] + pa[1][1] * ca[1][0],
            pa[1][0] * ca[0][1] + pa[1][1] * ca[1][1],
        ),
    )
    translation: Vector2 = (
        pa[0][0] * cb[0] + pa[0][1] * cb[1] + pb[0],
        pa[1][0] * cb[0] + pa[1][1] * cb[1] + pb[1],
    )
    return AffinePose2(linear, translation)


@dataclass(frozen=True)
class PrototypeGeometry:
    kind: str
    vertices: tuple[Vector2, ...]

    def __post_init__(self) -> None:
        exact_str(self.kind, "prototype geometry kind")
        vertices = exact_tuple(self.vertices, "prototype vertices")
        if len(vertices) < 3:
            raise ValueError("prototype geometry requires at least three vertices")
        for vertex in vertices:
            point = exact_tuple(vertex, "prototype vertex")
            if len(point) != 2 or any(type(value) is not Fraction for value in point):
                raise TypeError("prototype vertices require exact Fraction pairs")


UNIT_SQUARE_GEOMETRY = PrototypeGeometry(
    "unit-square",
    (
        (Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(1)),
        (Fraction(0), Fraction(1)),
    ),
)


@dataclass(frozen=True)
class TilePrototype:
    prototype_id: int
    geometry: PrototypeGeometry

    def __post_init__(self) -> None:
        prototype_id = exact_int(self.prototype_id, "prototype id")
        if prototype_id < 0:
            raise ValueError("prototype id must be nonnegative")
        if type(self.geometry) is not PrototypeGeometry:
            raise TypeError("prototype geometry must be an exact PrototypeGeometry")


def canonical_tile_prototypes(alphabet_size: int) -> tuple[TilePrototype, ...]:
    size = checked_alphabet_size(alphabet_size)
    return tuple(TilePrototype(label, UNIT_SQUARE_GEOMETRY) for label in range(size))


@dataclass(frozen=True)
class PlacedTile:
    prototype_id: int
    pose: AffinePose2

    def __post_init__(self) -> None:
        prototype_id = exact_int(self.prototype_id, "placed-tile prototype id")
        if prototype_id < 0:
            raise ValueError("placed-tile prototype id must be nonnegative")
        if type(self.pose) is not AffinePose2:
            raise TypeError("placed tile requires an exact AffinePose2")


def placed_tile_key(tile: PlacedTile) -> tuple[object, ...]:
    return (tile.pose.linear, tile.pose.translation, tile.prototype_id)


@dataclass(frozen=True)
class BagSnapshotProvenance:
    """Explicit bijection back to one operational grid snapshot token."""

    grid_token: SnapshotToken = field(repr=False)
    representation: str = "T26-aligned-addressed-pose-bag-v1"

    def __post_init__(self) -> None:
        if type(self.grid_token) is not SnapshotToken:
            raise TypeError("bag provenance requires an exact grid SnapshotToken")
        tag = exact_str(self.representation, "bag representation tag")
        if tag != "T26-aligned-addressed-pose-bag-v1":
            raise ValueError("unknown bag provenance representation")

    @property
    def generation(self) -> int:
        return self.grid_token.generation


@dataclass(frozen=True)
class SnapshotTokenRenaming:
    """Bijection for the mapped source and independently derived successors."""

    bag_source: SnapshotToken = field(repr=False)
    grid_source: SnapshotToken = field(repr=False)
    bag_successor: SnapshotToken = field(repr=False)
    grid_successor: SnapshotToken = field(repr=False)

    def __post_init__(self) -> None:
        tokens = (
            self.bag_source,
            self.grid_source,
            self.bag_successor,
            self.grid_successor,
        )
        if any(type(token) is not SnapshotToken for token in tokens):
            raise TypeError("token renaming requires exact SnapshotTokens")
        if self.bag_successor.parent is not self.bag_source:
            raise ValueError("bag successor is not derived from the bag source")
        if self.grid_successor.parent is not self.grid_source:
            raise ValueError("grid successor is not derived from the grid source")
        if self.bag_source.generation != self.grid_source.generation:
            raise ValueError("renamed source tokens must have equal generations")
        if self.bag_successor.generation != self.grid_successor.generation:
            raise ValueError("renamed successor tokens must have equal generations")
        if self.bag_source is self.bag_successor:
            raise ValueError("bag token image must distinguish source and successor")
        if self.grid_source is self.grid_successor:
            raise ValueError("grid token image must distinguish source and successor")
        if self.bag_successor is self.grid_successor:
            raise ValueError("successor tokens must be independently derived before renaming")

    def bag_to_grid(self, token: SnapshotToken) -> SnapshotToken:
        if type(token) is not SnapshotToken:
            raise TypeError("token renaming requires an exact SnapshotToken")
        if token is self.bag_source:
            return self.grid_source
        if token is self.bag_successor:
            return self.grid_successor
        raise ValueError("token lies outside the declared two-token bijection")

    def grid_to_bag(self, token: SnapshotToken) -> SnapshotToken:
        if type(token) is not SnapshotToken:
            raise TypeError("token renaming requires an exact SnapshotToken")
        if token is self.grid_source:
            return self.bag_source
        if token is self.grid_successor:
            return self.bag_successor
        raise ValueError("token lies outside the inverse two-token bijection")


@dataclass(frozen=True)
class PlacedTileBag:
    prototypes: tuple[TilePrototype, ...]
    occurrences: tuple[PlacedTile, ...]
    provenance: BagSnapshotProvenance = field(repr=False)

    def __post_init__(self) -> None:
        raw_prototypes = exact_tuple(self.prototypes, "bag prototypes")
        checked_alphabet_size(len(raw_prototypes))
        prototype_ids: list[int] = []
        for prototype in raw_prototypes:
            if type(prototype) is not TilePrototype:
                raise TypeError("bag prototypes must be exact TilePrototypes")
            prototype_ids.append(prototype.prototype_id)
        if len(set(prototype_ids)) != len(prototype_ids):
            raise ValueError("bag prototype ids must be unique")
        declared = set(prototype_ids)
        raw = exact_tuple(self.occurrences, "bag occurrences")
        checked: list[PlacedTile] = []
        for occurrence in raw:
            if type(occurrence) is not PlacedTile:
                raise TypeError("bag occurrences must be exact PlacedTiles")
            if occurrence.prototype_id not in declared:
                raise ValueError("placed tile uses an undeclared prototype")
            checked.append(occurrence)
        if type(self.provenance) is not BagSnapshotProvenance:
            raise TypeError("bag requires exact snapshot provenance")
        object.__setattr__(self, "occurrences", tuple(sorted(checked, key=placed_tile_key)))

    @property
    def alphabet_size(self) -> int:
        return len(self.prototypes)

    @property
    def generation(self) -> int:
        return self.provenance.generation


def strict_prototype_labels(bag: PlacedTileBag) -> dict[int, int]:
    if type(bag) is not PlacedTileBag:
        raise TypeError("prototype decoding requires an exact PlacedTileBag")
    expected_ids = tuple(range(bag.alphabet_size))
    actual_ids = tuple(prototype.prototype_id for prototype in bag.prototypes)
    if actual_ids != expected_ids:
        raise ValueError("T26 bag image requires canonical label/prototype ids")
    if any(prototype.geometry != UNIT_SQUARE_GEOMETRY for prototype in bag.prototypes):
        raise ValueError("T26 bag image requires one declared unit-square geometry")
    return {prototype_id: prototype_id for prototype_id in expected_ids}


def encode_grid_as_bag(configuration: RectGrid) -> PlacedTileBag:
    if type(configuration) is not RectGrid:
        raise TypeError("bag encoding requires an exact RectGrid")
    height, width = configuration.shape
    sx, sy = Fraction(1, width), Fraction(1, height)
    occurrences = tuple(
        PlacedTile(
            configuration.cells[row][column],
            diagonal_pose(sx, sy, Fraction(column, width), Fraction(row, height)),
        )
        for row in range(height)
        for column in range(width)
    )
    return PlacedTileBag(
        canonical_tile_prototypes(configuration.alphabet_size),
        occurrences,
        BagSnapshotProvenance(configuration.token),
    )


def exact_positive_reciprocal(value: Fraction, name: str) -> int:
    if type(value) is not Fraction or value <= 0:
        raise ValueError(f"{name} must be a positive exact Fraction")
    reciprocal = Fraction(1, 1) / value
    if reciprocal.denominator != 1:
        raise ValueError(f"{name} must be the reciprocal of a positive integer")
    return reciprocal.numerator


def bag_grid_image(
    bag: PlacedTileBag,
) -> tuple[int, int, dict[Coord2, PlacedTile]]:
    if type(bag) is not PlacedTileBag:
        raise TypeError("bag decoding requires an exact PlacedTileBag")
    labels = strict_prototype_labels(bag)
    if not bag.occurrences:
        raise ValueError("strict T26 image cannot be an empty occurrence bag")
    first = bag.occurrences[0].pose
    if first.linear[0][1] != 0 or first.linear[1][0] != 0:
        raise ValueError("free rotation/skew is outside the aligned T26 bag image")
    sx, sy = first.linear[0][0], first.linear[1][1]
    width = exact_positive_reciprocal(sx, "tile x scale")
    height = exact_positive_reciprocal(sy, "tile y scale")
    values: dict[Coord2, PlacedTile] = {}
    for occurrence in bag.occurrences:
        pose = occurrence.pose
        if pose.linear != first.linear:
            raise ValueError("T26 bag image requires one uniform aligned tile pose")
        column_value = pose.translation[0] / sx
        row_value = pose.translation[1] / sy
        if column_value.denominator != 1 or row_value.denominator != 1:
            raise ValueError("tile translations are off the rectangular grid")
        column, row = column_value.numerator, row_value.numerator
        if row < 0 or row >= height or column < 0 or column >= width:
            raise ValueError("tile pose is outside the unit rectangular support")
        coordinate = (row, column)
        if coordinate in values:
            raise ValueError("overlap/multiplicity is outside the strict T26 bag image")
        if occurrence.prototype_id not in labels:
            raise ValueError("bag occurrence prototype has no tile-label inverse")
        values[coordinate] = occurrence
    expected = {(row, column) for row in range(height) for column in range(width)}
    if set(values) != expected:
        raise ValueError("T26 bag image must tile the rectangle without holes")
    return height, width, values


def decode_bag_as_grid(
    bag: PlacedTileBag,
    expected_token: SnapshotToken | None = None,
) -> RectGrid:
    if expected_token is not None:
        if type(expected_token) is not SnapshotToken:
            raise TypeError("expected grid token must be an exact SnapshotToken")
        if bag.provenance.grid_token is not expected_token:
            raise ValueError("bag provenance belongs to a different grid snapshot")
    height, width, values = bag_grid_image(bag)
    cells = tuple(
        tuple(values[(row, column)].prototype_id for column in range(width))
        for row in range(height)
    )
    return RectGrid(bag.alphabet_size, cells, bag.provenance.grid_token)


@dataclass(frozen=True)
class BagParentHandle:
    provenance: BagSnapshotProvenance = field(repr=False)
    occurrence: PlacedTile


@dataclass(frozen=True)
class BagChildOccurrence:
    source: BagParentHandle
    local_row: int
    local_column: int
    local_pose: AffinePose2
    child: PlacedTile


@dataclass(frozen=True)
class BagChildPatch:
    source: BagParentHandle
    patch_height: int
    patch_width: int
    children: tuple[BagChildOccurrence, ...]


@dataclass(frozen=True)
class BagStep:
    source_provenance: BagSnapshotProvenance = field(repr=False)
    successor: PlacedTileBag
    child_patches: tuple[BagChildPatch, ...]


@dataclass(frozen=True)
class BagStepResult:
    outcome: Advanced | Invalid
    successors: tuple[PlacedTileBag, ...]
    step: BagStep | None

    def __post_init__(self) -> None:
        successors = exact_tuple(self.successors, "bag-step-result successors")
        if type(self.outcome) is Advanced:
            if type(self.step) is not BagStep:
                raise TypeError("Advanced bag result requires an exact BagStep")
            if len(successors) != 1 or successors[0] is not self.step.successor:
                raise ValueError("Advanced bag result must expose its committed successor")
        elif type(self.outcome) is Invalid:
            if self.step is not None or successors:
                raise ValueError("Invalid bag result must not commit a successor")
        else:
            raise TypeError("bag result requires exact Advanced or Invalid outcome")


def bag_step(
    table: ClosedPatchTable,
    bag: PlacedTileBag,
) -> BagStep:
    if type(table) is not ClosedPatchTable:
        raise TypeError("bag step requires exact closed patch-table data")
    if type(bag) is not PlacedTileBag:
        raise TypeError("bag step requires an exact PlacedTileBag")
    if table.alphabet_size != bag.alphabet_size:
        raise ValueError("bag and patch-table alphabets differ")
    strict_prototype_labels(bag)
    decode_bag_as_grid(bag, bag.provenance.grid_token)
    patch_height, patch_width = table.patch_shape
    successor_provenance = BagSnapshotProvenance(
        SnapshotToken(bag.generation + 1, bag.provenance.grid_token)
    )
    successor_token = successor_provenance.grid_token
    assert successor_token.parent is bag.provenance.grid_token
    assert successor_token.generation == bag.generation + 1
    children: list[PlacedTile] = []
    child_patches: list[BagChildPatch] = []
    for parent in bag.occurrences:
        patch = table.at(parent.prototype_id)
        source = BagParentHandle(bag.provenance, parent)
        witnesses: list[BagChildOccurrence] = []
        for local_row in range(patch_height):
            for local_column in range(patch_width):
                local_pose = diagonal_pose(
                    Fraction(1, patch_width),
                    Fraction(1, patch_height),
                    Fraction(local_column, patch_width),
                    Fraction(local_row, patch_height),
                )
                child = PlacedTile(
                    patch[local_row][local_column],
                    compose_pose(parent.pose, local_pose),
                )
                children.append(child)
                witnesses.append(
                    BagChildOccurrence(
                        source,
                        local_row,
                        local_column,
                        local_pose,
                        child,
                    )
                )
        child_patches.append(
            BagChildPatch(
                source,
                patch_height,
                patch_width,
                tuple(witnesses),
            )
        )
    successor = PlacedTileBag(
        bag.prototypes,
        tuple(children),
        successor_provenance,
    )
    return BagStep(bag.provenance, successor, tuple(child_patches))


def bag_step_result(
    table: ClosedPatchTable,
    bag: PlacedTileBag,
) -> BagStepResult:
    """Full successful runner envelope for the uniform T27 restriction."""

    decode_bag_as_grid(bag, bag.provenance.grid_token)
    step = bag_step(table, bag)
    decode_bag_as_grid(
        step.successor,
        step.successor.provenance.grid_token,
    )
    changed = (
        (step.successor.prototypes, step.successor.occurrences)
        != (bag.prototypes, bag.occurrences)
    )
    return BagStepResult(Advanced(changed), (step.successor,), step)


def rename_patch_step_tokens(
    step: PatchStep,
    renaming: SnapshotTokenRenaming,
) -> PatchStep:
    """Apply the declared bag-to-grid token bijection to typed grid lineage."""

    if type(step) is not PatchStep or type(renaming) is not SnapshotTokenRenaming:
        raise TypeError("patch-step renaming requires exact typed values")
    source_token = renaming.bag_to_grid(step.source_token)
    successor_token = renaming.bag_to_grid(step.successor.token)

    def rename_source(source: TileHandle) -> TileHandle:
        if type(source) is not TileHandle:
            raise TypeError("renamed patch lineage requires exact TileHandles")
        return TileHandle(
            renaming.bag_to_grid(source.token),
            source.row,
            source.column,
        )

    rectangles = tuple(
        ChildRectangle(
            rename_source(rectangle.source),
            rectangle.row_start,
            rectangle.row_stop,
            rectangle.column_start,
            rectangle.column_stop,
        )
        for rectangle in step.child_rectangles
    )
    children = tuple(
        GridChildOccurrence(
            rename_source(child.source),
            child.local_row,
            child.local_column,
            child.target_row,
            child.target_column,
            child.label,
        )
        for child in step.child_occurrences
    )
    return PatchStep(
        source_token,
        RectGrid(step.successor.alphabet_size, step.successor.cells, successor_token),
        rectangles,
        children,
    )


def rename_bag_step_tokens(
    step: BagStep,
    renaming: SnapshotTokenRenaming,
) -> BagStep:
    """Apply the same bijection to bag provenance and every typed parent handle."""

    if type(step) is not BagStep or type(renaming) is not SnapshotTokenRenaming:
        raise TypeError("bag-step renaming requires exact typed values")
    source_token = renaming.bag_to_grid(step.source_provenance.grid_token)
    successor_token = renaming.bag_to_grid(step.successor.provenance.grid_token)
    source_provenance = BagSnapshotProvenance(
        source_token,
        step.source_provenance.representation,
    )
    successor_provenance = BagSnapshotProvenance(
        successor_token,
        step.successor.provenance.representation,
    )
    patches: list[BagChildPatch] = []
    for patch in step.child_patches:
        if type(patch) is not BagChildPatch:
            raise TypeError("renamed bag lineage requires exact BagChildPatches")
        if patch.source.provenance is not step.source_provenance:
            raise ValueError("bag patch source lies outside the renamed provenance")
        source = BagParentHandle(source_provenance, patch.source.occurrence)
        witnesses: list[BagChildOccurrence] = []
        for witness in patch.children:
            if type(witness) is not BagChildOccurrence or witness.source != patch.source:
                raise ValueError("bag child witness lies outside its renamed parent")
            witnesses.append(
                BagChildOccurrence(
                    source,
                    witness.local_row,
                    witness.local_column,
                    witness.local_pose,
                    witness.child,
                )
            )
        patches.append(
            BagChildPatch(
                source,
                patch.patch_height,
                patch.patch_width,
                tuple(witnesses),
            )
        )
    successor = PlacedTileBag(
        step.successor.prototypes,
        step.successor.occurrences,
        successor_provenance,
    )
    return BagStep(source_provenance, successor, tuple(patches))


def rename_patch_step_result_tokens(
    result: PatchStepResult,
    renaming: SnapshotTokenRenaming,
) -> PatchStepResult:
    if type(result) is not PatchStepResult:
        raise TypeError("patch-result renaming requires an exact PatchStepResult")
    if type(result.outcome) is Invalid:
        return result
    assert type(result.step) is PatchStep
    step = rename_patch_step_tokens(result.step, renaming)
    return PatchStepResult(result.outcome, (step.successor,), step)


def rename_bag_step_result_tokens(
    result: BagStepResult,
    renaming: SnapshotTokenRenaming,
) -> BagStepResult:
    if type(result) is not BagStepResult:
        raise TypeError("bag-result renaming requires an exact BagStepResult")
    if type(result.outcome) is Invalid:
        return result
    assert type(result.step) is BagStep
    step = rename_bag_step_tokens(result.step, renaming)
    return BagStepResult(result.outcome, (step.successor,), step)


def assert_patch_steps_operationally_equal(left: PatchStep, right: PatchStep) -> None:
    assert type(left) is type(right) is PatchStep
    assert left.source_token is right.source_token
    assert left.successor.token is right.successor.token
    assert left.successor.alphabet_size == right.successor.alphabet_size
    assert left.successor.cells == right.successor.cells
    assert left.child_rectangles == right.child_rectangles
    assert left.child_occurrences == right.child_occurrences


def encode_patch_step_as_bag_step(
    table: ClosedPatchTable,
    configuration: RectGrid,
    step: PatchStep,
) -> BagStep:
    if type(step) is not PatchStep or step.source_token is not configuration.token:
        raise ValueError("patch step is not bound to the represented source snapshot")
    if step.successor.token.parent is not configuration.token:
        raise ValueError("patch successor provenance is not derived from the source")
    patch_height, patch_width = table.patch_shape
    source_bag = encode_grid_as_bag(configuration)
    successor_bag = encode_grid_as_bag(step.successor)
    _height, _width, source_image = bag_grid_image(source_bag)
    source_coordinates = {occurrence: coordinate for coordinate, occurrence in source_image.items()}
    expected_grid_sources = tuple(
        TileHandle(configuration.token, row, column)
        for row in range(_height)
        for column in range(_width)
    )
    if any(type(rectangle) is not ChildRectangle for rectangle in step.child_rectangles):
        raise TypeError("patch-step rectangle lineage must be exact")
    actual_rectangle_sources = tuple(
        rectangle.source for rectangle in step.child_rectangles
    )
    if actual_rectangle_sources != expected_grid_sources:
        raise ValueError(
            "patch-step rectangle lineage must cover each source exactly once in order"
        )
    rectangle_by_source = {rectangle.source: rectangle for rectangle in step.child_rectangles}
    expected_child_keys = tuple(
        (source, local_row, local_column)
        for source in expected_grid_sources
        for local_row in range(patch_height)
        for local_column in range(patch_width)
    )
    if any(type(child) is not GridChildOccurrence for child in step.child_occurrences):
        raise TypeError("patch-step child lineage must be exact")
    actual_child_keys = tuple(
        (child.source, child.local_row, child.local_column)
        for child in step.child_occurrences
    )
    if actual_child_keys != expected_child_keys:
        raise ValueError(
            "patch-step child lineage must cover every expected local slot exactly once in order"
        )
    child_by_key = {
        (
            child.source,
            child.local_row,
            child.local_column,
        ): child
        for child in step.child_occurrences
    }
    assert len(rectangle_by_source) == len(source_bag.occurrences)
    patches: list[BagChildPatch] = []
    for parent in source_bag.occurrences:
        row, column = source_coordinates[parent]
        grid_source = TileHandle(configuration.token, row, column)
        rectangle = rectangle_by_source.get(grid_source)
        expected_rectangle = ChildRectangle(
            grid_source,
            row * patch_height,
            (row + 1) * patch_height,
            column * patch_width,
            (column + 1) * patch_width,
        )
        if rectangle != expected_rectangle:
            raise ValueError("patch-step rectangle does not match uniform bag placement")
        bag_source = BagParentHandle(source_bag.provenance, parent)
        witnesses: list[BagChildOccurrence] = []
        patch = table.at(parent.prototype_id)
        for local_row in range(patch_height):
            for local_column in range(patch_width):
                child = child_by_key.get((grid_source, local_row, local_column))
                if child is None:
                    raise ValueError("patch-step child lineage is incomplete")
                if (
                    child.target_row != row * patch_height + local_row
                    or child.target_column != column * patch_width + local_column
                    or child.label != patch[local_row][local_column]
                ):
                    raise ValueError("patch-step child lineage is forged")
                local_pose = diagonal_pose(
                    Fraction(1, patch_width),
                    Fraction(1, patch_height),
                    Fraction(local_column, patch_width),
                    Fraction(local_row, patch_height),
                )
                placed_child = PlacedTile(
                    child.label,
                    compose_pose(parent.pose, local_pose),
                )
                if placed_child not in successor_bag.occurrences:
                    raise ValueError("mapped child is absent from the bag successor")
                witnesses.append(
                    BagChildOccurrence(
                        bag_source,
                        local_row,
                        local_column,
                        local_pose,
                        placed_child,
                    )
                )
        patches.append(
            BagChildPatch(
                bag_source,
                patch_height,
                patch_width,
                tuple(witnesses),
            )
        )
    assert len(child_by_key) == len(step.child_occurrences)
    return BagStep(source_bag.provenance, successor_bag, tuple(patches))


def decode_bag_step_as_patch_step(
    table: ClosedPatchTable,
    configuration: RectGrid,
    step: BagStep,
) -> PatchStep:
    if type(step) is not BagStep:
        raise TypeError("bag-step decoding requires an exact BagStep")
    if step.source_provenance.grid_token is not configuration.token:
        raise ValueError("bag-step source provenance is stale or cross-snapshot")
    if step.successor.provenance.grid_token.parent is not configuration.token:
        raise ValueError("bag-step successor provenance is not source-derived")
    patch_height, patch_width = table.patch_shape
    source_bag = encode_grid_as_bag(configuration)
    _height, _width, source_image = bag_grid_image(source_bag)
    source_coordinates = {occurrence: coordinate for coordinate, occurrence in source_image.items()}
    expected_sources = set(source_bag.occurrences)
    seen_sources: set[PlacedTile] = set()
    seen_children: list[PlacedTile] = []
    rectangles: list[ChildRectangle] = []
    children: list[GridChildOccurrence] = []
    for patch_lineage in step.child_patches:
        if type(patch_lineage) is not BagChildPatch:
            raise TypeError("bag-step patch lineage must be exact")
        source = patch_lineage.source
        if type(source) is not BagParentHandle:
            raise TypeError("bag-step parent handle must be exact")
        if source.provenance is not step.source_provenance:
            raise ValueError("bag parent handle has forged snapshot provenance")
        parent = source.occurrence
        if parent not in expected_sources or parent in seen_sources:
            raise ValueError("bag lineage source coverage is incomplete or duplicated")
        seen_sources.add(parent)
        if (
            patch_lineage.patch_height != patch_height
            or patch_lineage.patch_width != patch_width
        ):
            raise ValueError("bag lineage patch shape disagrees with the rule")
        row, column = source_coordinates[parent]
        grid_source = TileHandle(configuration.token, row, column)
        rectangles.append(
            ChildRectangle(
                grid_source,
                row * patch_height,
                (row + 1) * patch_height,
                column * patch_width,
                (column + 1) * patch_width,
            )
        )
        expected_patch = table.at(parent.prototype_id)
        local_keys: set[Coord2] = set()
        for witness in patch_lineage.children:
            if type(witness) is not BagChildOccurrence or witness.source != source:
                raise ValueError("bag child witness is not bound to its parent")
            local = (
                exact_int(witness.local_row, "bag child local row"),
                exact_int(witness.local_column, "bag child local column"),
            )
            if (
                local[0] < 0
                or local[0] >= patch_height
                or local[1] < 0
                or local[1] >= patch_width
                or local in local_keys
            ):
                raise ValueError("bag child local occurrence is invalid or duplicated")
            local_keys.add(local)
            expected_local_pose = diagonal_pose(
                Fraction(1, patch_width),
                Fraction(1, patch_height),
                Fraction(local[1], patch_width),
                Fraction(local[0], patch_height),
            )
            expected_child = PlacedTile(
                expected_patch[local[0]][local[1]],
                compose_pose(parent.pose, expected_local_pose),
            )
            if witness.local_pose != expected_local_pose or witness.child != expected_child:
                raise ValueError("bag child witness pose/prototype is forged")
            seen_children.append(witness.child)
            children.append(
                GridChildOccurrence(
                    grid_source,
                    local[0],
                    local[1],
                    row * patch_height + local[0],
                    column * patch_width + local[1],
                    witness.child.prototype_id,
                )
            )
        expected_locals = {
            (local_row, local_column)
            for local_row in range(patch_height)
            for local_column in range(patch_width)
        }
        if local_keys != expected_locals:
            raise ValueError("bag child witnesses do not cover the parent patch exactly")
    if seen_sources != expected_sources:
        raise ValueError("bag lineage does not cover every old occurrence")
    if tuple(sorted(seen_children, key=placed_tile_key)) != step.successor.occurrences:
        raise ValueError("bag lineage children do not equal the successor occurrence bag")
    successor = decode_bag_as_grid(
        step.successor,
        step.successor.provenance.grid_token,
    )
    rectangles.sort(key=lambda item: (item.source.row, item.source.column))
    children.sort(
        key=lambda item: (
            item.source.row,
            item.source.column,
            item.local_row,
            item.local_column,
        )
    )
    return PatchStep(
        configuration.token,
        successor,
        tuple(rectangles),
        tuple(children),
    )


def encode_patch_step_result_as_bag_step_result(
    table: ClosedPatchTable,
    configuration: RectGrid,
    result: PatchStepResult,
) -> BagStepResult:
    if type(result) is not PatchStepResult:
        raise TypeError("result encoding requires an exact PatchStepResult")
    if type(result.outcome) is Invalid:
        return BagStepResult(result.outcome, (), None)
    assert type(result.step) is PatchStep
    step = encode_patch_step_as_bag_step(table, configuration, result.step)
    return BagStepResult(result.outcome, (step.successor,), step)


def decode_bag_step_result_as_patch_step_result(
    table: ClosedPatchTable,
    configuration: RectGrid,
    result: BagStepResult,
) -> PatchStepResult:
    if type(result) is not BagStepResult:
        raise TypeError("result decoding requires an exact BagStepResult")
    if type(result.outcome) is Invalid:
        return PatchStepResult(result.outcome, (), None)
    assert type(result.step) is BagStep
    step = decode_bag_step_as_patch_step(table, configuration, result.step)
    changed = step.successor.cells != configuration.cells
    if result.outcome != Advanced(changed):
        raise ValueError("bag Advanced.changed disagrees with the semantic grid carrier")
    return PatchStepResult(result.outcome, (step.successor,), step)


def assert_patch_step_results_operationally_equal(
    left: PatchStepResult,
    right: PatchStepResult,
) -> None:
    assert type(left) is type(right) is PatchStepResult
    assert left.outcome == right.outcome
    assert len(left.successors) == len(right.successors)
    if type(left.outcome) is Invalid:
        assert left.successors == right.successors == ()
        assert left.step is right.step is None
        return
    assert type(left.step) is type(right.step) is PatchStep
    assert len(left.successors) == len(right.successors) == 1
    assert left.successors[0] is left.step.successor
    assert right.successors[0] is right.step.successor
    assert_patch_steps_operationally_equal(left.step, right.step)


def assert_bag_commutes(table: ClosedPatchTable, configuration: RectGrid) -> None:
    encoded = encode_grid_as_bag(configuration)
    decoded = decode_bag_as_grid(encoded, configuration.token)
    assert decoded.token is configuration.token
    assert decoded.cells == configuration.cells
    assert encode_grid_as_bag(decoded) == encoded

    generic_result = generic_step_result(table, configuration)
    assert type(generic_result.outcome) is Advanced
    assert type(generic_result.step) is PatchStep
    geometric_result = bag_step_result(table, encoded)
    assert type(geometric_result.outcome) is Advanced
    assert type(geometric_result.step) is BagStep
    assert (
        geometric_result.step.successor.provenance.grid_token
        is not generic_result.step.successor.token
    )
    renaming = SnapshotTokenRenaming(
        geometric_result.step.source_provenance.grid_token,
        generic_result.step.source_token,
        geometric_result.step.successor.provenance.grid_token,
        generic_result.step.successor.token,
    )
    for bag_token in (renaming.bag_source, renaming.bag_successor):
        assert renaming.grid_to_bag(renaming.bag_to_grid(bag_token)) is bag_token
    for grid_token in (renaming.grid_source, renaming.grid_successor):
        assert renaming.bag_to_grid(renaming.grid_to_bag(grid_token)) is grid_token
    independently_mapped = decode_bag_step_result_as_patch_step_result(
        table,
        configuration,
        geometric_result,
    )
    mapped_result = rename_patch_step_result_tokens(independently_mapped, renaming)
    assert_patch_step_results_operationally_equal(mapped_result, generic_result)
    encoded_result = encode_patch_step_result_as_bag_step_result(
        table,
        configuration,
        generic_result,
    )
    renamed_geometric_result = rename_bag_step_result_tokens(
        geometric_result,
        renaming,
    )
    assert renamed_geometric_result == encoded_result
    assert (
        encode_patch_step_result_as_bag_step_result(
            table,
            configuration,
            mapped_result,
        )
        == renamed_geometric_result
    )


# ---------------------------------------------------------------------------
# Evidence fixtures, representation boundaries, and hostile controls
# ---------------------------------------------------------------------------


PAGE_187_TABLE = ClosedPatchTable(
    2,
    (
        (0, ((0, 0), (0, 0))),
        (1, ((1, 0), (1, 1))),
    ),
)

PAGE_187_T0 = ((1,),)
PAGE_187_T1 = ((1, 0), (1, 1))
PAGE_187_T2 = (
    (1, 0, 0, 0),
    (1, 1, 0, 0),
    (1, 0, 1, 0),
    (1, 1, 1, 1),
)


NONWHITE_BACKGROUND_TABLE = ClosedPatchTable(
    2,
    (
        (0, ((1, 0), (0, 1))),
        (1, ((1, 1), (1, 0))),
    ),
)


# Exact BOOK:13744 encoded-label table.  Geometry-role decoding is unspecified,
# but the label table and seed are complete and Notes ``Flatten2D`` executes it.
OTHER_SHAPES_MIXED_RELATION = (
    (3, ((1, 0), (3, 2))),
    (2, ((1,), (3,))),
    (1, ((3, 2),)),
    (0, ((3,),)),
)
OTHER_SHAPES_TABLE = ClosedPatchTable(
    4,
    tuple(sorted(OTHER_SHAPES_MIXED_RELATION)),
)
OTHER_SHAPES_SEED = ((3,),)
OTHER_SHAPES_CHECKPOINTS = (
    (1, "f22f1e2ecd4e0ee531ef5bbd4d6dfd81c05d0f489b7dd6770e47e5f7ca2aea78"),
    (2, "2f4e9a2550a17188991a8b35c0a7d921aa00d15f1395325e493da2cead660831"),
    (3, "dcaa0bcd149aadd6bb79be9371bbbcfa0d2801d46122c6695e468791389d28a6"),
    (5, "03a5fb3b36e5d55991946788f33fb3450bc73767e8050d648ca5283fce69dc2f"),
    (8, "a62492543f41827fdf78d749a1e17fdc475fe92525369c6e90257a66c22fd513"),
    (13, "fb5d48d7ee1f24a0986a6bb8caf93348d38678c17aa7ee844fe68fafca03dfe9"),
    (21, "dfa78082ff57197eecaf8b92f164ab83d4dcc4e5400421503a3dac61f31c4505"),
)


def naive_row_major_patch_flatten(table: ClosedPatchTable, cells: Grid) -> Grid:
    """Deliberately wrong: flatten patches, then reshape the whole stream."""

    old = checked_patch(cells, table.alphabet_size, name="naive old grid")
    patch_height, patch_width = table.patch_shape
    target_width = len(old[0]) * patch_width
    stream = tuple(
        value
        for row in old
        for label in row
        for patch_row in table.at(label)
        for value in patch_row
    )
    assert len(stream) == len(old) * patch_height * target_width
    return tuple(
        tuple(stream[offset : offset + target_width])
        for offset in range(0, len(stream), target_width)
    )


def render_rectangles(cells: Grid, scale: int) -> tuple[tuple[int, int, int, int, int], ...]:
    """Downstream observer; its scale cannot enter transition semantics."""

    checked = checked_patch(cells, 2, name="render grid")
    pixels = exact_int(scale, "render scale")
    if pixels <= 0:
        raise ValueError("render scale must be positive")
    return tuple(
        (column * pixels, row * pixels, pixels, pixels, label)
        for row, labels in enumerate(checked)
        for column, label in enumerate(labels)
    )


def table_count(alphabet_size: int, patch_shape: tuple[int, int]) -> int:
    size = checked_alphabet_size(alphabet_size)
    shape = exact_tuple(patch_shape, "patch shape")
    if len(shape) != 2:
        raise ValueError("T26 patch shape must have rank two")
    height = exact_int(shape[0], "patch height")
    width = exact_int(shape[1], "patch width")
    if height <= 0 or width <= 0:
        raise ValueError("patch dimensions must be positive")
    return size ** (size * height * width)


def assert_exhaustive_binary_commutation() -> dict[str, int]:
    tables = binary_tables_2x2()
    grids = binary_grids()
    assert len(tables) == 256
    # There are 2 + 4 + 4 + 16 = 26 labeled grids across these four
    # rectangular shapes.  Keeping both one-tile grids matters: deleting them
    # would silently bias the exhaustive table check by old label.
    assert len(grids) == 26
    events = 0
    bag_events = 0
    firings = 0
    nonwhite_tables = 0
    for table in tables:
        if any(value == 1 for row in table.at(0) for value in row):
            nonwhite_tables += 1
        for configuration in grids:
            assert_commutes(table, configuration)
            assert_bag_commutes(table, configuration)
            step = generic_step(table, configuration)
            assert len(step.child_rectangles) == prod(configuration.shape)
            firings += prod(configuration.shape)
            events += 1
            bag_events += 1
    assert events == 256 * 26 == 6_656
    assert bag_events == events
    assert firings == 20_992
    assert nonwhite_tables == 240
    return {
        "binary_2x2_tables": len(tables),
        "binary_rectangular_grids": len(grids),
        "native_generic_events": events,
        "t27_bag_commuting_events": bag_events,
        "old_tile_firings": firings,
        "nonwhite_background_tables": nonwhite_tables,
    }


def assert_source_fixture_and_rectangles() -> dict[str, int]:
    assert table_count(2, (2, 2)) == 2**8 == 256
    assert table_count(3, (3, 3)) == 3**27 == 7_625_597_484_987
    assert table_count(4, (2, 2)) == 4**16 == 2**32 == 4_294_967_296

    configuration = make_grid(PAGE_187_T0, 2)
    exhaustive_tables = set(binary_tables_2x2())
    exhaustive_cells = {grid.cells for grid in binary_grids()}
    assert PAGE_187_TABLE in exhaustive_tables
    assert PAGE_187_T0 in exhaustive_cells
    assert PAGE_187_T1 in exhaustive_cells
    assert PAGE_187_T2 not in exhaustive_cells
    assert native_step(PAGE_187_TABLE, configuration.cells) == PAGE_187_T1
    first = generic_step(PAGE_187_TABLE, configuration).successor
    assert first.cells == PAGE_187_T1
    second = generic_step(PAGE_187_TABLE, first).successor
    assert second.cells == PAGE_187_T2
    assert_bag_commutes(PAGE_187_TABLE, configuration)
    assert_bag_commutes(PAGE_187_TABLE, first)

    trace: list[Grid] = [configuration.cells]
    for _ in range(4):
        assert_commutes(PAGE_187_TABLE, configuration)
        configuration = generic_step(PAGE_187_TABLE, configuration).successor
        trace.append(configuration.cells)
    trace_digest = sha256(repr(tuple(trace)).encode("utf-8")).hexdigest()

    rectangular = ClosedPatchTable(
        3,
        (
            (0, ((0, 1, 2), (2, 1, 0))),
            (1, ((1, 2, 0), (0, 2, 1))),
            (2, ((2, 0, 1), (1, 0, 2))),
        ),
    )
    rectangular_grid = make_grid(((0, 1), (2, 0)), 3)
    assert rectangular.patch_shape == (2, 3)
    assert_commutes(rectangular, rectangular_grid)
    assert_bag_commutes(rectangular, rectangular_grid)
    result = generic_step(rectangular, rectangular_grid).successor
    assert result.shape == (4, 6)

    # Compatibility is row-slab based, not an invented source-column width
    # constraint.  Each column sees widths 1 and 2 in opposite order, while
    # both assembled source-row slabs have width three and must advance.
    cross_column_widths = ClosedPatchTable(
        2,
        (
            (0, ((0,),)),
            (1, ((1, 0),)),
        ),
    )
    cross_column_grid = make_grid(((0, 1), (1, 0)), 2)
    cross_column_expected = ((0, 1, 0), (1, 0, 0))
    assert native_step(cross_column_widths, cross_column_grid.cells) == cross_column_expected
    cross_column_result = generic_step_result(cross_column_widths, cross_column_grid)
    assert cross_column_result.outcome == Advanced(True)
    assert len(cross_column_result.successors) == 1
    assert cross_column_result.successors[0].cells == cross_column_expected
    assert type(cross_column_result.step) is PatchStep

    # BOOK:13744 is a complete encoded-label table, not merely a geometric
    # relation.  Exact Notes Flatten2D execution yields Fibonacci side lengths.
    mixed = make_grid(OTHER_SHAPES_SEED, 4)
    for checkpoint_index, (expected_side, expected_digest) in enumerate(
        OTHER_SHAPES_CHECKPOINTS
    ):
        assert mixed.shape == (expected_side, expected_side)
        assert sha256(repr(mixed.cells).encode("utf-8")).hexdigest() == expected_digest
        if checkpoint_index < len(OTHER_SHAPES_CHECKPOINTS) - 1:
            assert_commutes(OTHER_SHAPES_TABLE, mixed)
            mixed = generic_step(OTHER_SHAPES_TABLE, mixed).successor

    return {
        "page187_generic_events": 4,
        "page187_exhaustive_overlap_events": 2,
        "page187_unique_nonoverlap_events": 2,
        "page187_bag_commuting_events": 2,
        "page187_bag_exhaustive_overlap_events": 2,
        "page187_bag_unique_nonoverlap_events": 0,
        "page187_exact_checkpoints": 3,
        "page187_trace_digest_words": len(trace_digest),
        "page187_trace_digest_int": int(trace_digest[:12], 16),
        "rectangular_2x3_events": 1,
        "compatible_cross_column_width_events": 1,
        "other_shapes_mosaic_events": len(OTHER_SHAPES_CHECKPOINTS) - 1,
        "other_shapes_exact_checkpoints": len(OTHER_SHAPES_CHECKPOINTS),
        "derived_rule_count_checks": 3,
        "source_numeric_codecs": 0,
    }


def assert_rank_parameterization() -> dict[str, int]:
    # Explicit selected-source indices are the rank-one locus map.  Every old
    # source receives one lineage record: selected sources emit their ordered
    # block (possibly epsilon), while unselected sources are consumed with a
    # typed zero-width region.  Exhaust all subsets through old length four.
    events = 0
    fixed_events = 0
    all_selected_events = 0
    original_positive_all_selected_events = 0
    right_neighbor_frontier_events = 0
    unselected_consumption_events = 0
    empty_input_events = 0
    singleton_to_empty_events = 0
    selected_epsilon_events = 0
    words = tuple(
        word
        for block_length in range(3)
        for word in product((0, 1), repeat=block_length)
    )
    for zero_word, one_word in product(words, repeat=2):
        for length in range(5):
            for word in product((0, 1), repeat=length):
                for selection_mask in product((False, True), repeat=length):
                    selected_indices = tuple(
                        index for index, selected in enumerate(selection_mask) if selected
                    )
                    selected_blocks = tuple(
                        zero_word if word[index] == 0 else one_word
                        for index in selected_indices
                    )
                    direct = tuple(
                        child for block in selected_blocks for child in block
                    )
                    assembly = ranked_block_mosaic_assemble(
                        (length,),
                        tuple((len(block),) for block in selected_blocks),
                        selected_blocks,
                        selected_source_indices=selected_indices,
                    )
                    assert assembly.shape == (len(direct),)
                    assert assembly.values == direct

                    selected_blocks_by_source = dict(
                        zip(selected_indices, selected_blocks, strict=True)
                    )
                    expected_regions: list[
                        tuple[int, bool, tuple[int, ...], tuple[int, ...]]
                    ] = []
                    cursor = 0
                    for source_index in range(length):
                        selected = source_index in selected_blocks_by_source
                        start = cursor
                        if selected:
                            cursor += len(selected_blocks_by_source[source_index])
                        expected_regions.append(
                            (source_index, selected, (start,), (cursor,))
                        )
                    assert tuple(
                        (
                            region.source_index,
                            region.selected,
                            region.starts,
                            region.stops,
                        )
                        for region in assembly.source_regions
                    ) == tuple(expected_regions)
                    assert cursor == len(direct)

                    events += 1
                    all_selected = selected_indices == tuple(range(length))
                    if all_selected:
                        all_selected_events += 1
                        if length >= 1:
                            original_positive_all_selected_events += 1
                    else:
                        unselected_consumption_events += 1
                    if selected_indices == tuple(range(max(0, length - 1))):
                        right_neighbor_frontier_events += 1
                    if length == 0:
                        assert selected_indices == () and assembly == RankedMosaicAssembly(
                            (0,), (), ()
                        )
                        empty_input_events += 1
                    if length == 1 and not selected_indices:
                        assert assembly.shape == (0,) and assembly.values == ()
                        assert assembly.source_regions == (
                            RankedSourceRegion(0, False, (0,), (0,)),
                        )
                        singleton_to_empty_events += 1
                    if selected_indices and not direct:
                        selected_epsilon_events += 1
                    if (
                        all_selected
                        and length >= 1
                        and len(zero_word) == len(one_word)
                        and len(zero_word) in (1, 2)
                    ):
                        fixed_events += 1
    assert events == 16_709
    assert all_selected_events == 1_519
    assert original_positive_all_selected_events == 1_470
    assert right_neighbor_frontier_events == 1_519
    assert unselected_consumption_events == 15_190
    assert empty_input_events == 49
    assert singleton_to_empty_events == 98
    assert selected_epsilon_events == 1_390
    assert fixed_events == 600

    adversarial = ClosedPatchTable(
        2,
        (
            (0, ((0, 1), (1, 0))),
            (1, ((1, 1), (0, 0))),
        ),
    )
    old = ((0, 1), (1, 0))
    correct = native_step(adversarial, old)
    naive = naive_row_major_patch_flatten(adversarial, old)
    assert correct != naive
    assert tuple(value for row in ((0, 1), (1, 0)) for value in row) == tuple(
        value for row in ((0, 1, 1, 0),) for value in row
    )

    return {
        "rank1_selected_mosaic_events": events,
        "rank1_all_selected_events": all_selected_events,
        "rank1_original_positive_all_selected_subset": (
            original_positive_all_selected_events
        ),
        "rank1_right_neighbor_frontier_events": right_neighbor_frontier_events,
        "rank1_unselected_consumption_events": unselected_consumption_events,
        "rank1_empty_input_events": empty_input_events,
        "rank1_singleton_to_empty_events": singleton_to_empty_events,
        "rank1_selected_epsilon_events": selected_epsilon_events,
        "t13_fixed_block_rank1_subset": fixed_events,
        "rank2_block_assembly_events": 1,
        "naive_row_major_divergences": 1,
        "flat_whole_state_loss_witnesses": 1,
    }


def assert_boundaries_and_observers() -> dict[str, int]:
    all_white = make_grid(((0, 0), (0, 0)), 2)
    exhaustive_tables = set(binary_tables_2x2())
    exhaustive_cells = {grid.cells for grid in binary_grids()}
    assert NONWHITE_BACKGROUND_TABLE in exhaustive_tables
    assert all_white.cells in exhaustive_cells
    assert_commutes(NONWHITE_BACKGROUND_TABLE, all_white)
    changed = generic_step(NONWHITE_BACKGROUND_TABLE, all_white).successor
    assert any(value == 1 for row in changed.cells for value in row)

    page = make_grid(PAGE_187_T1, 2)
    semantic_next = generic_step(PAGE_187_TABLE, page).successor
    small = render_rectangles(page.cells, 1)
    large = render_rectangles(page.cells, 7)
    assert small != large
    assert generic_step(PAGE_187_TABLE, page).successor == semantic_next
    assert len(small) == len(large) == prod(page.shape)

    identity_table = ClosedPatchTable(
        2,
        (
            (0, ((0,),)),
            (1, ((1,),)),
        ),
    )
    identity_grid = make_grid(((0,),), 2)
    assert identity_table not in exhaustive_tables
    identity_grid_result = generic_step_result(identity_table, identity_grid)
    identity_bag_result = bag_step_result(
        identity_table,
        encode_grid_as_bag(identity_grid),
    )
    assert identity_grid_result.outcome == Advanced(False)
    assert identity_bag_result.outcome == Advanced(False)
    assert native_step(identity_table, identity_grid.cells) == identity_grid.cells
    assert_commutes(identity_table, identity_grid)
    assert_bag_commutes(identity_table, identity_grid)

    mixed_shapes = {
        (len(patch), len(patch[0]))
        for _label, patch in OTHER_SHAPES_MIXED_RELATION
    }
    assert mixed_shapes == {(2, 2), (2, 1), (1, 2), (1, 1)}

    # One event cannot recursively fire newborns.  The second event has a
    # different extent and is observably distinct from the first event.
    seed = make_grid(((1,),), 2)
    assert seed.cells in exhaustive_cells
    assert_commutes(NONWHITE_BACKGROUND_TABLE, seed)
    first = generic_step(NONWHITE_BACKGROUND_TABLE, seed).successor
    assert first.cells in exhaustive_cells
    assert_commutes(NONWHITE_BACKGROUND_TABLE, first)
    second = generic_step(NONWHITE_BACKGROUND_TABLE, first).successor
    assert first.shape == (2, 2)
    assert second.shape == (4, 4)
    assert first.cells != second.cells

    # Bag state is permutation invariant, but the strict decoder still checks
    # exactly one occurrence at every aligned rectangular address.
    encoded = encode_grid_as_bag(page)
    reversed_bag = PlacedTileBag(
        encoded.prototypes,
        tuple(reversed(encoded.occurrences)),
        encoded.provenance,
    )
    assert reversed_bag == encoded
    reversed_result = bag_step(PAGE_187_TABLE, reversed_bag)
    encoded_result = bag_step(PAGE_187_TABLE, encoded)
    permutation_renaming = SnapshotTokenRenaming(
        reversed_result.source_provenance.grid_token,
        encoded_result.source_provenance.grid_token,
        reversed_result.successor.provenance.grid_token,
        encoded_result.successor.provenance.grid_token,
    )
    assert rename_bag_step_tokens(
        reversed_result,
        permutation_renaming,
    ) == encoded_result

    # The same selected old label yields the same write in unlike surrounding
    # contexts.  This is the operational proof that T26 reads self only; it is
    # not a merely nominal absence of a ``neighbors`` field.
    quiet_context = make_grid(((0, 0), (0, 0)), 2)
    busy_context = make_grid(((0, 1), (1, 1)), 2)
    quiet_active = (all_old_tiles(quiet_context)[0],)
    busy_active = (all_old_tiles(busy_context)[0],)
    quiet_write = make_patch_writes(
        quiet_context,
        NONWHITE_BACKGROUND_TABLE,
        quiet_active,
        read_self(quiet_context, quiet_active),
    )[0]
    busy_write = make_patch_writes(
        busy_context,
        NONWHITE_BACKGROUND_TABLE,
        busy_active,
        read_self(busy_context, busy_active),
    )[0]
    assert quiet_write.old_label == busy_write.old_label == 0
    assert quiet_write.patch == busy_write.patch

    return {
        "nonwhite_background_events": 1,
        "nonwhite_background_exhaustive_overlap_events": 1,
        "implicit_white_identity_divergences": 1,
        "render_scale_variants": 2,
        "render_inputs_to_rule": 0,
        "identity_stepresult_events": 1,
        "identity_unique_stepresult_events": 1,
        "identity_bag_stepresult_commutations": 1,
        "other_shapes_encoded_rows": len(OTHER_SHAPES_MIXED_RELATION),
        "other_shapes_strict_executions": len(OTHER_SHAPES_CHECKPOINTS) - 1,
        "newborn_deferral_events": 2,
        "newborn_deferral_exhaustive_overlap_events": 2,
        "bag_permutation_checks": 1,
        "context_independence_checks": 1,
    }


def expect_rejection(expected: type[BaseException], operation: Callable[[], object]) -> None:
    try:
        operation()
    except expected:
        return
    except BaseException as error:  # pragma: no cover - diagnostic path
        raise AssertionError(
            f"expected {expected.__name__}, got {type(error).__name__}"
        ) from error
    raise AssertionError(f"expected {expected.__name__}")


def assert_hostile_validation() -> dict[str, int]:
    rejections = 0
    typed_invalid_outcomes = 0

    def rejects(expected: type[BaseException], operation: Callable[[], object]) -> None:
        nonlocal rejections
        expect_rejection(expected, operation)
        rejections += 1

    def rejects_incompatible(
        table: ClosedPatchTable,
        configuration: RectGrid,
        expected_code: str,
    ) -> None:
        nonlocal rejections, typed_invalid_outcomes
        old_cells = configuration.cells
        old_token = configuration.token
        result = generic_step_result(table, configuration)
        assert type(result.outcome) is Invalid
        assert type(result.outcome.reason) is IncompatibleMosaic
        assert result.outcome.reason.code == expected_code
        assert result.successors == ()
        assert result.step is None
        assert configuration.cells is old_cells
        assert configuration.token is old_token
        rejections += 1
        typed_invalid_outcomes += 1

    rejects(TypeError, lambda: checked_alphabet_size(True))
    rejects(ValueError, lambda: checked_alphabet_size(1))
    rejects(TypeError, lambda: make_grid([[0]], 2))
    rejects(ValueError, lambda: make_grid((), 2))
    rejects(ValueError, lambda: make_grid(((),), 2))
    rejects(ValueError, lambda: make_grid(((0, 1), (1,)), 2))
    rejects(ValueError, lambda: make_grid(((2,),), 2))
    rejects(TypeError, lambda: make_grid(((True,),), 2))
    rejects(TypeError, lambda: RectGrid(2, ((0,),), "token"))
    rejects(TypeError, lambda: SnapshotToken(1, "parent"))
    rejects(ValueError, lambda: SnapshotToken(0, SnapshotToken(0)))

    good_rows = PAGE_187_TABLE.rows
    rejects(ValueError, lambda: ClosedPatchTable(2, good_rows[:-1]))
    rejects(ValueError, lambda: ClosedPatchTable(2, (good_rows[0], good_rows[0])))
    rejects(ValueError, lambda: ClosedPatchTable(2, tuple(reversed(good_rows))))
    rejects(TypeError, lambda: ClosedPatchTable(2, "callback"))
    rejects(TypeError, lambda: ClosedPatchTable(2, b"\x89PNG"))
    rejects(ValueError, lambda: ClosedPatchTable(2, ((0, ()), (1, ((1,),)))))
    rejects(ValueError, lambda: ClosedPatchTable(2, ((0, ((),)), (1, ((1,),)))))
    rejects(
        ValueError,
        lambda: ClosedPatchTable(2, ((0, ((0, 1), (1,))), (1, ((1, 0), (0, 1))))),
    )
    rejects(
        ValueError,
        lambda: ClosedPatchTable(2, ((0, ((0, 2),)), (1, ((1, 0),)))),
    )
    rejects(
        TypeError,
        lambda: ClosedPatchTable(2, (((0, 1), ((0,),)), (1, ((1,),)))),
    )

    unequal_heights = ClosedPatchTable(
        2,
        ((0, ((0,),)), (1, ((1,), (0,)))),
    )
    unequal_slab_widths = ClosedPatchTable(
        2,
        ((0, ((0,),)), (1, ((1, 0),))),
    )
    unequal_heights_grid = make_grid(((0, 1),), 2)
    unequal_slab_widths_grid = make_grid(((0,), (1,)), 2)
    rejects_incompatible(
        unequal_heights,
        unequal_heights_grid,
        "row_patch_heights",
    )
    rejects_incompatible(
        unequal_slab_widths,
        unequal_slab_widths_grid,
        "row_slab_widths",
    )
    rejects(
        IncompatibleMosaicError,
        lambda: generic_step(unequal_heights, unequal_heights_grid),
    )
    rejects(
        IncompatibleMosaicError,
        lambda: generic_step(unequal_slab_widths, unequal_slab_widths_grid),
    )
    rejects(
        IncompatibleMosaicError,
        lambda: notes_flatten2d((((((0,),), ((1,), (0,)))),)),
    )
    rejects(
        IncompatibleMosaicError,
        lambda: notes_flatten2d(((((0,),),), (((1, 0),),))),
    )

    configuration = make_grid(((0, 1), (1, 0)), 2)
    active = all_old_tiles(configuration)
    reads = read_self(configuration, active)
    writes = make_patch_writes(configuration, PAGE_187_TABLE, active, reads)
    foreign = make_grid(configuration.cells, 2, generation=configuration.generation)
    foreign_active = all_old_tiles(foreign)
    rejects(ValueError, lambda: read_self(configuration, foreign_active))
    rejects(
        ValueError,
        lambda: read_self(
            configuration,
            (TileHandle(configuration.token, 2, 0),),
        ),
    )
    rejects(TypeError, lambda: read_self(configuration, ((0, 0),)))
    rejects(
        ValueError,
        lambda: make_patch_writes(
            configuration,
            PAGE_187_TABLE,
            active,
            (replace(reads[0], label=1 - reads[0].label), *reads[1:]),
        ),
    )
    rejects(
        ValueError,
        lambda: make_patch_writes(
            configuration,
            PAGE_187_TABLE,
            active,
            (replace(reads[0], token=foreign.token), *reads[1:]),
        ),
    )
    rejects(
        TypeError,
        lambda: make_patch_writes(configuration, lambda value: value, active, reads),
    )
    rejects(
        TypeError,
        lambda: make_patch_writes(
            configuration,
            PAGE_187_TABLE,
            active,
            ((reads[0].label, 99), *reads[1:]),
        ),
    )
    rejects(ValueError, lambda: apply_flatten2d(configuration, active[:-1], writes[:-1]))
    rejects(ValueError, lambda: apply_flatten2d(configuration, active, writes[:-1]))
    rejects(ValueError, lambda: apply_flatten2d(configuration, active, tuple(reversed(writes))))
    rejects(
        ValueError,
        lambda: apply_flatten2d(
            configuration,
            active,
            (replace(writes[0], token=foreign.token), *writes[1:]),
        ),
    )
    rejects(
        ValueError,
        lambda: apply_flatten2d(
            configuration,
            active,
            (
                replace(
                    writes[0],
                    source=TileHandle(configuration.token, 2, 0),
                ),
                *writes[1:],
            ),
        ),
    )
    rejects(
        ValueError,
        lambda: apply_flatten2d(
            configuration,
            active,
            (replace(writes[0], old_label=1 - writes[0].old_label), *writes[1:]),
        ),
    )
    rejects(
        IncompatibleMosaicError,
        lambda: apply_flatten2d(
            configuration,
            active,
            (replace(writes[0], patch=((0,),)), *writes[1:]),
        ),
    )
    rejects(
        IncompatibleMosaicError,
        lambda: apply_flatten2d(
            configuration,
            active,
            (replace(writes[0], patch=((0, 0, 0), (0, 0, 0))), *writes[1:]),
        ),
    )
    rejects(TypeError, lambda: generic_step(PAGE_187_TABLE, ((0, 1, 1, 0),)))
    rejects(TypeError, lambda: generic_step(lambda grid: grid, configuration))

    rejects(ValueError, lambda: ranked_block_assemble((), (), ()))
    rejects(ValueError, lambda: ranked_block_assemble((1, 1), (2,), (((0, 1),),)))
    rejects(ValueError, lambda: ranked_block_assemble((1,), (0,), ((0,),)))
    rejects(ValueError, lambda: ranked_block_assemble((1,), (0,), ((),)))
    rejects(ValueError, lambda: ranked_block_assemble((2,), (2,), ((0, 1),)))
    rejects(ValueError, lambda: ranked_block_assemble((1,), (2,), ((0,),)))
    rejects(
        ValueError,
        lambda: ranked_block_mosaic_assemble(
            (2,), ((1,),), ((0,),), selected_source_indices=(1, 1)
        ),
    )
    rejects(
        ValueError,
        lambda: ranked_block_mosaic_assemble(
            (2,), ((1,),), ((0,),), selected_source_indices=(2,)
        ),
    )
    rejects(
        ValueError,
        lambda: ranked_block_mosaic_assemble(
            (1, 1), (), (), selected_source_indices=()
        ),
    )
    rejects(ValueError, lambda: notes_flatten2d(()))

    bag = encode_grid_as_bag(configuration)
    duplicate = PlacedTileBag(
        bag.prototypes,
        (bag.occurrences[0], bag.occurrences[0], *bag.occurrences[2:]),
        bag.provenance,
    )
    rejects(ValueError, lambda: decode_bag_as_grid(duplicate))
    rotated = PlacedTileBag(
        bag.prototypes,
        (
            PlacedTile(
                0,
                AffinePose2(
                    ((Fraction(0), Fraction(-1)), (Fraction(1), Fraction(0))),
                    (Fraction(0), Fraction(0)),
                ),
            ),
        ),
        bag.provenance,
    )
    rejects(ValueError, lambda: decode_bag_as_grid(rotated))
    rejects(TypeError, lambda: bag_step("callback", bag))
    rejects(ValueError, lambda: bag_step(ClosedPatchTable(3, ((0, ((0,),)), (1, ((1,),)), (2, ((2,),)))), bag))
    rejects(ValueError, lambda: bag_step(OTHER_SHAPES_TABLE, encode_grid_as_bag(make_grid(OTHER_SHAPES_SEED, 4))))

    rejects(TypeError, lambda: BagSnapshotProvenance("token"))
    rejects(ValueError, lambda: BagSnapshotProvenance(configuration.token, "forged"))
    rejects(
        ValueError,
        lambda: PlacedTileBag(
            bag.prototypes,
            (PlacedTile(99, bag.occurrences[0].pose),),
            bag.provenance,
        ),
    )
    triangle = PrototypeGeometry(
        "triangle",
        (
            (Fraction(0), Fraction(0)),
            (Fraction(1), Fraction(0)),
            (Fraction(0), Fraction(1)),
        ),
    )
    wrong_geometry = PlacedTileBag(
        (TilePrototype(0, triangle), *bag.prototypes[1:]),
        bag.occurrences,
        bag.provenance,
    )
    rejects(ValueError, lambda: decode_bag_as_grid(wrong_geometry))

    cross_bag = replace(bag, provenance=BagSnapshotProvenance(foreign.token))
    rejects(ValueError, lambda: decode_bag_as_grid(cross_bag, configuration.token))
    native_result = generic_step(PAGE_187_TABLE, configuration)
    good_bag_result = bag_step(PAGE_187_TABLE, bag)
    assert good_bag_result.successor.provenance.grid_token is not native_result.successor.token
    stale_successor = BagSnapshotProvenance(
        SnapshotToken(configuration.generation + 1)
    )
    rejects(
        TypeError,
        lambda: bag_step(PAGE_187_TABLE, bag, stale_successor),  # type: ignore[call-arg]
    )
    cross_successor = BagSnapshotProvenance(
        SnapshotToken(foreign.generation + 1, foreign.token)
    )
    rejects(
        TypeError,
        lambda: SnapshotTokenRenaming(
            "bag-source",  # type: ignore[arg-type]
            configuration.token,
            good_bag_result.successor.provenance.grid_token,
            native_result.successor.token,
        ),
    )
    rejects(
        ValueError,
        lambda: SnapshotTokenRenaming(
            configuration.token,
            configuration.token,
            stale_successor.grid_token,
            native_result.successor.token,
        ),
    )
    rejects(
        ValueError,
        lambda: SnapshotTokenRenaming(
            configuration.token,
            configuration.token,
            good_bag_result.successor.provenance.grid_token,
            good_bag_result.successor.provenance.grid_token,
        ),
    )
    good_renaming = SnapshotTokenRenaming(
        configuration.token,
        configuration.token,
        good_bag_result.successor.provenance.grid_token,
        native_result.successor.token,
    )
    rejects(ValueError, lambda: good_renaming.bag_to_grid(foreign.token))
    rejects(ValueError, lambda: good_renaming.grid_to_bag(foreign.token))
    foreign_provenance = BagSnapshotProvenance(foreign.token)
    rejects(
        ValueError,
        lambda: decode_bag_step_as_patch_step(
            PAGE_187_TABLE,
            configuration,
            replace(good_bag_result, source_provenance=foreign_provenance),
        ),
    )
    first_patch = good_bag_result.child_patches[0]
    forged_parent = BagParentHandle(
        foreign_provenance,
        first_patch.source.occurrence,
    )
    rejects(
        ValueError,
        lambda: decode_bag_step_as_patch_step(
            PAGE_187_TABLE,
            configuration,
            replace(
                good_bag_result,
                child_patches=(
                    replace(first_patch, source=forged_parent),
                    *good_bag_result.child_patches[1:],
                ),
            ),
        ),
    )
    rejects(
        ValueError,
        lambda: decode_bag_step_as_patch_step(
            PAGE_187_TABLE,
            configuration,
            replace(
                good_bag_result,
                child_patches=good_bag_result.child_patches[:-1],
            ),
        ),
    )
    forged_witness = replace(first_patch.children[0], local_row=99)
    rejects(
        ValueError,
        lambda: decode_bag_step_as_patch_step(
            PAGE_187_TABLE,
            configuration,
            replace(
                good_bag_result,
                child_patches=(
                    replace(
                        first_patch,
                        children=(forged_witness, *first_patch.children[1:]),
                    ),
                    *good_bag_result.child_patches[1:],
                ),
            ),
        ),
    )
    rejects(
        ValueError,
        lambda: decode_bag_step_as_patch_step(
            PAGE_187_TABLE,
            configuration,
            replace(
                good_bag_result,
                child_patches=(
                    replace(first_patch, children=first_patch.children[:-1]),
                    *good_bag_result.child_patches[1:],
                ),
            ),
        ),
    )
    forged_successor_bag = replace(
        good_bag_result.successor,
        provenance=cross_successor,
    )
    rejects(
        ValueError,
        lambda: decode_bag_step_as_patch_step(
            PAGE_187_TABLE,
            configuration,
            replace(good_bag_result, successor=forged_successor_bag),
        ),
    )
    rejects(
        ValueError,
        lambda: encode_patch_step_as_bag_step(
            PAGE_187_TABLE,
            configuration,
            replace(native_result, source_token=foreign.token),
        ),
    )
    rejects(
        ValueError,
        lambda: encode_patch_step_as_bag_step(
            PAGE_187_TABLE,
            configuration,
            replace(
                native_result,
                child_rectangles=(
                    native_result.child_rectangles[0],
                    *native_result.child_rectangles,
                ),
            ),
        ),
    )
    extra_child = replace(
        native_result.child_occurrences[-1],
        local_row=99,
        target_row=99,
    )
    rejects(
        ValueError,
        lambda: encode_patch_step_as_bag_step(
            PAGE_187_TABLE,
            configuration,
            replace(
                native_result,
                child_occurrences=(
                    *native_result.child_occurrences,
                    extra_child,
                ),
            ),
        ),
    )

    rejects(ValueError, lambda: render_rectangles(((0,),), 0))
    rejects(ValueError, lambda: table_count(2, (2, 0)))

    # Only self is rule-visible.  Neighbor/context keys and arbitrary geometry
    # are rejected above instead of becoming T28 or T27 callbacks.
    assert tuple(TileRead.__dataclass_fields__) == ("token", "source", "label")
    assert "neighbors" not in TileRead.__dataclass_fields__
    assert "raster" not in PatchWrite.__dataclass_fields__
    assert "pose" not in PatchWrite.__dataclass_fields__
    assert len({read.label for read in reads}) == 2
    assert rejections == 81
    assert typed_invalid_outcomes == 2

    return {
        "hostile_rejections": rejections,
        "typed_incompatible_no_commit_outcomes": typed_invalid_outcomes,
        "context_fields_exposed": 0,
        "raster_program_fields": 0,
        "free_geometry_rule_fields": 0,
    }


def semantic_digest(counts: dict[str, int]) -> str:
    transcript = "\n".join(f"{key}={counts[key]}" for key in sorted(counts))
    return sha256(transcript.encode("utf-8")).hexdigest()


EXPECTED_SEMANTIC_DIGEST = (
    "e380704a0626ad7a578e0937007cfa6ea8cc0dd6cee1b8c2d24a7eab18b7c57c"
)


def main() -> None:
    groups = {
        "exhaustive": assert_exhaustive_binary_commutation(),
        "source": assert_source_fixture_and_rectangles(),
        "rank": assert_rank_parameterization(),
        "boundaries": assert_boundaries_and_observers(),
        "hostile": assert_hostile_validation(),
    }
    counts = {
        f"{group}.{key}": value
        for group, values in groups.items()
        for key, value in values.items()
    }
    assert groups["source"]["page187_generic_events"] == (
        groups["source"]["page187_exhaustive_overlap_events"]
        + groups["source"]["page187_unique_nonoverlap_events"]
    )
    assert groups["source"]["page187_bag_commuting_events"] == (
        groups["source"]["page187_bag_exhaustive_overlap_events"]
        + groups["source"]["page187_bag_unique_nonoverlap_events"]
    )
    assert groups["boundaries"]["nonwhite_background_events"] == groups[
        "boundaries"
    ]["nonwhite_background_exhaustive_overlap_events"]
    assert groups["boundaries"]["newborn_deferral_events"] == groups[
        "boundaries"
    ]["newborn_deferral_exhaustive_overlap_events"]
    counts["total.native_generic_events"] = (
        groups["exhaustive"]["native_generic_events"]
        + groups["source"]["page187_unique_nonoverlap_events"]
        + groups["source"]["rectangular_2x3_events"]
        + groups["source"]["compatible_cross_column_width_events"]
        + groups["source"]["other_shapes_mosaic_events"]
        + groups["boundaries"]["identity_unique_stepresult_events"]
    )
    counts["total.bag_stepresult_commutations"] = (
        groups["exhaustive"]["t27_bag_commuting_events"]
        + groups["source"]["page187_bag_unique_nonoverlap_events"]
        + groups["source"]["rectangular_2x3_events"]
        + groups["boundaries"]["identity_bag_stepresult_commutations"]
    )
    counts["total.rank1_mosaic_commutations"] = groups["rank"][
        "rank1_selected_mosaic_events"
    ]
    counts["total.commuting_proofs"] = (
        counts["total.native_generic_events"]
        + counts["total.bag_stepresult_commutations"]
        + counts["total.rank1_mosaic_commutations"]
    )
    assert counts["total.native_generic_events"] == 6_667
    assert counts["total.bag_stepresult_commutations"] == 6_658
    assert counts["total.rank1_mosaic_commutations"] == 16_709
    assert counts["total.commuting_proofs"] == 30_034
    digest = semantic_digest(counts)
    assert digest == EXPECTED_SEMANTIC_DIGEST, (digest, counts)

    print("T26 semantic oracle: PASS")
    print(f"native_generic_events={counts['total.native_generic_events']}")
    print(f"commuting_proofs={counts['total.commuting_proofs']}")
    print(
        "unique_event_partition="
        f"binary_2x2:{groups['exhaustive']['native_generic_events']},"
        f"page187_nonoverlap:{groups['source']['page187_unique_nonoverlap_events']},"
        f"rectangular_2x3:{groups['source']['rectangular_2x3_events']},"
        f"compatible_cross_column_width:{groups['source']['compatible_cross_column_width_events']},"
        f"other_shapes_mosaic:{groups['source']['other_shapes_mosaic_events']},"
        f"identity_stepresult:{groups['boundaries']['identity_unique_stepresult_events']}"
    )
    print(
        "named_overlap_coverage_nonadditive="
        f"page187_native:{groups['source']['page187_exhaustive_overlap_events']},"
        f"page187_bag:{groups['source']['page187_bag_exhaustive_overlap_events']},"
        f"nonwhite:{groups['boundaries']['nonwhite_background_exhaustive_overlap_events']},"
        f"newborn:{groups['boundaries']['newborn_deferral_exhaustive_overlap_events']}"
    )
    print(
        "strict_T26=discrete_t+2D;configuration=finite_nonempty_rectangular_tile_grid;"
        "alphabet=finite_tile_labels;frontier=AllOldTiles;neighborhood=SelfOnly"
    )
    print(
        "rule=total_closed_TileLabel_to_nonempty_rectangular_patch;"
        "UPDATE=exact_rank2_compatible_Flatten2D_mosaic;old_snapshot=YES;newborn_deferral=YES;"
        "incompatibility=Invalid(IncompatibleMosaic)+zero_successors+no_commit;"
        "overlap_policy=NOT_APPLICABLE"
    )
    print(
        "rule_counts=derived_k^(k*h*w);"
        "binary_2x2:256;ternary_3x3:7625597484987;four_color_2x2:4294967296;"
        "source_numeric_codec=NONE"
    )
    print(
        "rank_relation=generic_ranked_mosaic_has_explicit_selected_source_indices;"
        "unselected_sources=CONSUMED;epsilon=RETAINED;"
        "T26_is_rank2_member;"
        f"rank1_commutations={groups['rank']['rank1_selected_mosaic_events']};"
        f"original_positive_all_selected_subset={groups['rank']['rank1_original_positive_all_selected_subset']};"
        f"all_selected_including_empty={groups['rank']['rank1_all_selected_events']};"
        f"unselected_consumption={groups['rank']['rank1_unselected_consumption_events']};"
        f"empty_input={groups['rank']['rank1_empty_input_events']};"
        f"singleton_to_empty={groups['rank']['rank1_singleton_to_empty_events']};"
        f"fixed_block_subset={groups['rank']['t13_fixed_block_rank1_subset']};"
        f"nonadditive_right_neighbor_subset={groups['rank']['rank1_right_neighbor_frontier_events']};"
        f"nonadditive_selected_epsilon_subset={groups['rank']['rank1_selected_epsilon_events']};"
        "plain_row_major_T13_concatenation_for_rank2=REJECTED"
    )
    print(
        "bag_relation=lossless_restriction_of_T27_addressed_pose_bag;"
        f"bag_commutations={counts['total.bag_stepresult_commutations']};"
        "carrier=(prototype_id,pose);prototype_catalog=one_declared_unit_square_per_label;"
        "proof=full_StepResult+independent_successor_tokens+explicit_token_bijection+typed_lineage;"
        "identity_changed_false=PROVED;"
        "required_invariant=aligned_uniform_no_hole_no_overlap_rectangular_tiling;"
        "arbitrary_free_geometry=T27"
    )
    print(
        "other_shapes=encoded_labels_0_through_3;geometric_role_codec=UNSPECIFIED;"
        f"printed_mixed_patch_rule=NATIVE_T26;strict_executions={groups['source']['other_shapes_mosaic_events']};"
        "exact_sides=1,2,3,5,8,13,21;source_role_to_color_assignment=UNSPECIFIED;"
        "compatibility=row_equal_heights+equal_slab_widths"
    )
    print(
        "boundaries=white_is_ordinary_label_not_implicit_identity;"
        "nonwhite_background_rows_execute_normally;display_scale+raster+digit_formula+fractal_limit="
        "OBSERVERS_OR_RELATIONS"
    )
    print(
        "runtime_audit=reuse_finite_values+selector_responsibility+old_snapshot_orchestration;"
        "gaps=rectangular_dynamic_configuration,old_tile_handles,self_projection,closed_patch_tables,"
        "ranked_block_writes,Flatten2D_lineage,ragged_structured_traces;"
        "family_dispatch+fixed_shape_arrays+callbacks_are_not_semantics"
    )
    print(
        "classification=UPDATE_axis_ranked_mosaic_generalization+"
        "T27_category3_restricted_representation;"
        "new_T26_UPDATE_algebra=NONE;new_executor=NONE;T28_contextual_choice=SEPARATE"
    )
    print(f"hostile_rejections={groups['hostile']['hostile_rejections']}")
    print(
        "typed_incompatible_no_commit_outcomes="
        f"{groups['hostile']['typed_incompatible_no_commit_outcomes']}"
    )
    print(f"semantic_digest={digest}")


if __name__ == "__main__":
    main()
