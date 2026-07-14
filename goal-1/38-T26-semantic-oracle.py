#!/usr/bin/env python3
"""Independent semantic and architecture oracle for T26.

The strict source construction is a finite rectangular grid of tile labels in
discrete ``t+2D``.  Every old tile fires once, reads only its own old label,
and emits one nonempty rectangular patch from a total closed table.  All
patches in the strict profile have the same shape.  ``UPDATE`` performs the
Notes' ``Flatten2D`` block assembly: source rows remain source rows, local
patch rows are interleaved within them, and local patch columns are joined
within source columns.  New tiles do not fire until the following event.

The generic evaluator below is one rank-parameterized ordered-block update.
Its rank-one restriction is fixed-block T13 concatenation; rank two is T26.
The direct Notes evaluator and generic evaluator commute one event at a time.
A second exact commuting map embeds a rectangular grid as a restricted T27
bag of fully posed tile occurrences.  The embedding is lossless only under a
rectangular-tiling invariant; arbitrary free geometry remains T27, and
neighbor-dependent patch choice remains T28.

The Book's ``Other shapes`` note is deliberately not promoted into the strict
evaluator.  It gives a finite shape/orientation-as-color relation, but its
printed right-hand sides have mixed sizes.  Without a source-closed general
compatibility law, those four rows remain relation evidence and are rejected
by the uniform-patch T26 validator.  Rasters, display scale, coordinate
formulae, and limiting fractals likewise never become programs or state.
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
    """Opaque old-snapshot identity; generation is diagnostic only."""

    generation: int

    def __post_init__(self) -> None:
        generation = exact_int(self.generation, "generation")
        if generation < 0:
            raise ValueError("generation must be nonnegative")


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
    """Total finite ``TileLabel -> uniform rectangular patch`` data."""

    alphabet_size: int
    rows: tuple[tuple[int, Patch], ...]

    def __post_init__(self) -> None:
        size = checked_alphabet_size(self.alphabet_size)
        raw_rows = exact_tuple(self.rows, "table rows")
        keys: list[int] = []
        patch_shape: tuple[int, int] | None = None
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
                expected_shape=patch_shape,
                name="table output patch",
            )
            if patch_shape is None:
                patch_shape = (len(patch), len(patch[0]))
            keys.append(label)
        if tuple(keys) != tuple(range(size)):
            raise ValueError("table rows must cover every label once in canonical order")

    @property
    def patch_shape(self) -> tuple[int, int]:
        patch = self.rows[0][1]
        return (len(patch), len(patch[0]))

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
class PatchStep:
    successor: RectGrid
    child_rectangles: tuple[ChildRectangle, ...]


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


def ranked_block_assemble(
    old_shape: tuple[int, ...],
    block_shape: tuple[int, ...],
    blocks: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    """One rank-parameterized D019 ordered block-assembly kernel."""

    old = exact_tuple(old_shape, "old ranked shape")
    block = exact_tuple(block_shape, "block ranked shape")
    emitted = exact_tuple(blocks, "ranked blocks")
    if not old or len(old) != len(block):
        raise ValueError("old and block shapes must have the same positive rank")
    old_extents = tuple(exact_int(value, "old extent") for value in old)
    block_extents = tuple(exact_int(value, "block extent") for value in block)
    if any(value <= 0 for value in (*old_extents, *block_extents)):
        raise ValueError("ranked shapes must have positive extents")
    if len(emitted) != prod(old_extents):
        raise ValueError("ranked blocks must cover every old occurrence exactly")
    block_volume = prod(block_extents)
    for raw_values in emitted:
        values = exact_tuple(raw_values, "ranked block")
        if len(values) != block_volume:
            raise ValueError("ranked block volume does not match block shape")

    next_shape = tuple(
        old_extent * block_extent
        for old_extent, block_extent in zip(old_extents, block_extents, strict=True)
    )
    result: list[int | None] = [None] * prod(next_shape)
    for old_coordinate in product(*(range(extent) for extent in old_extents)):
        source_index = flat_index(old_coordinate, old_extents)
        source_block = emitted[source_index]
        for local_coordinate in product(*(range(extent) for extent in block_extents)):
            local_index = flat_index(local_coordinate, block_extents)
            target_coordinate = tuple(
                source * block_extent + local
                for source, block_extent, local in zip(
                    old_coordinate,
                    block_extents,
                    local_coordinate,
                    strict=True,
                )
            )
            target_index = flat_index(target_coordinate, next_shape)
            if result[target_index] is not None:
                raise RuntimeError("uniform block assembly produced an overlap")
            result[target_index] = exact_int(source_block[local_index], "ranked child label")
    if any(value is None for value in result):
        raise RuntimeError("uniform block assembly left a hole")
    return tuple(value for value in result if value is not None)


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

    patch_shape: tuple[int, int] | None = None
    blocks: list[tuple[int, ...]] = []
    rectangles: list[ChildRectangle] = []
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
            expected_shape=patch_shape,
            name="emitted patch",
        )
        if patch_shape is None:
            patch_shape = (len(patch), len(patch[0]))
        blocks.append(tuple(value for row in patch for value in row))

    assert patch_shape is not None
    old_height, old_width = configuration.shape
    patch_height, patch_width = patch_shape
    flat_successor = ranked_block_assemble(
        (old_height, old_width),
        patch_shape,
        tuple(blocks),
    )
    next_width = old_width * patch_width
    cells = tuple(
        tuple(flat_successor[offset : offset + next_width])
        for offset in range(0, len(flat_successor), next_width)
    )
    for source in handles:
        rectangles.append(
            ChildRectangle(
                source,
                source.row * patch_height,
                (source.row + 1) * patch_height,
                source.column * patch_width,
                (source.column + 1) * patch_width,
            )
        )
    return PatchStep(
        RectGrid(
            configuration.alphabet_size,
            cells,
            SnapshotToken(configuration.generation + 1),
        ),
        tuple(rectangles),
    )


def generic_step(table: ClosedPatchTable, configuration: RectGrid) -> PatchStep:
    if type(table) is not ClosedPatchTable:
        raise TypeError("generic step requires an exact ClosedPatchTable")
    if type(configuration) is not RectGrid:
        raise TypeError("generic step requires an exact RectGrid")
    active = all_old_tiles(configuration)
    reads = read_self(configuration, active)
    writes = make_patch_writes(configuration, table, active, reads)
    return apply_flatten2d(configuration, active, writes)


def notes_flatten2d(block_grid: tuple[tuple[Patch, ...], ...]) -> Grid:
    """Independent direct reading of ``Apply[Join,Map[MapThread...]]``."""

    source_rows = exact_tuple(block_grid, "nested replacement blocks")
    if not source_rows:
        raise ValueError("Flatten2D source must have a positive number of rows")
    old_width: int | None = None
    patch_shape: tuple[int, int] | None = None
    result: list[tuple[int, ...]] = []
    for raw_source_row in source_rows:
        source_row = exact_tuple(raw_source_row, "nested replacement block row")
        if not source_row:
            raise ValueError("Flatten2D source rows must be nonempty")
        if old_width is None:
            old_width = len(source_row)
        elif len(source_row) != old_width:
            raise ValueError("Flatten2D source must be rectangular")
        checked_blocks: list[Patch] = []
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
            shape = (len(checked), len(checked[0]))
            if patch_shape is None:
                patch_shape = shape
            elif shape != patch_shape:
                raise ValueError("strict T26 Flatten2D patches must have one uniform shape")
            checked_blocks.append(checked)
        assert patch_shape is not None
        for local_row in range(patch_shape[0]):
            result.append(
                tuple(
                    value
                    for patch in checked_blocks
                    for value in patch[local_row]
                )
            )
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
class PlacedTile:
    label: int
    pose: AffinePose2

    def __post_init__(self) -> None:
        exact_int(self.label, "placed-tile label")
        if type(self.pose) is not AffinePose2:
            raise TypeError("placed tile requires an exact AffinePose2")


def placed_tile_key(tile: PlacedTile) -> tuple[object, ...]:
    return (tile.pose.linear, tile.pose.translation, tile.label)


@dataclass(frozen=True)
class PlacedTileBag:
    alphabet_size: int
    occurrences: tuple[PlacedTile, ...]
    generation: int = 0

    def __post_init__(self) -> None:
        size = checked_alphabet_size(self.alphabet_size)
        raw = exact_tuple(self.occurrences, "bag occurrences")
        checked: list[PlacedTile] = []
        for occurrence in raw:
            if type(occurrence) is not PlacedTile:
                raise TypeError("bag occurrences must be exact PlacedTiles")
            if occurrence.label < 0 or occurrence.label >= size:
                raise ValueError("placed-tile label is outside the alphabet")
            checked.append(occurrence)
        generation = exact_int(self.generation, "bag generation")
        if generation < 0:
            raise ValueError("bag generation must be nonnegative")
        object.__setattr__(self, "occurrences", tuple(sorted(checked, key=placed_tile_key)))


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
    return PlacedTileBag(configuration.alphabet_size, occurrences, configuration.generation)


def exact_positive_reciprocal(value: Fraction, name: str) -> int:
    if type(value) is not Fraction or value <= 0:
        raise ValueError(f"{name} must be a positive exact Fraction")
    reciprocal = Fraction(1, 1) / value
    if reciprocal.denominator != 1:
        raise ValueError(f"{name} must be the reciprocal of a positive integer")
    return reciprocal.numerator


def decode_bag_as_grid(bag: PlacedTileBag) -> RectGrid:
    if type(bag) is not PlacedTileBag:
        raise TypeError("bag decoding requires an exact PlacedTileBag")
    if not bag.occurrences:
        raise ValueError("strict T26 image cannot be an empty occurrence bag")
    first = bag.occurrences[0].pose
    if first.linear[0][1] != 0 or first.linear[1][0] != 0:
        raise ValueError("free rotation/skew is outside the aligned T26 bag image")
    sx, sy = first.linear[0][0], first.linear[1][1]
    width = exact_positive_reciprocal(sx, "tile x scale")
    height = exact_positive_reciprocal(sy, "tile y scale")
    values: dict[Coord2, int] = {}
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
        values[coordinate] = occurrence.label
    expected = {(row, column) for row in range(height) for column in range(width)}
    if set(values) != expected:
        raise ValueError("T26 bag image must tile the rectangle without holes")
    cells = tuple(
        tuple(values[(row, column)] for column in range(width))
        for row in range(height)
    )
    return make_grid(cells, bag.alphabet_size, bag.generation)


def bag_step(table: ClosedPatchTable, bag: PlacedTileBag) -> PlacedTileBag:
    if type(table) is not ClosedPatchTable:
        raise TypeError("bag step requires exact closed patch-table data")
    if type(bag) is not PlacedTileBag:
        raise TypeError("bag step requires an exact PlacedTileBag")
    if table.alphabet_size != bag.alphabet_size:
        raise ValueError("bag and patch-table alphabets differ")
    patch_height, patch_width = table.patch_shape
    children: list[PlacedTile] = []
    for parent in bag.occurrences:
        patch = table.at(parent.label)
        for local_row in range(patch_height):
            for local_column in range(patch_width):
                local_pose = diagonal_pose(
                    Fraction(1, patch_width),
                    Fraction(1, patch_height),
                    Fraction(local_column, patch_width),
                    Fraction(local_row, patch_height),
                )
                children.append(
                    PlacedTile(
                        patch[local_row][local_column],
                        compose_pose(parent.pose, local_pose),
                    )
                )
    return PlacedTileBag(table.alphabet_size, tuple(children), bag.generation + 1)


def assert_bag_commutes(table: ClosedPatchTable, configuration: RectGrid) -> None:
    encoded = encode_grid_as_bag(configuration)
    assert decode_bag_as_grid(encoded).cells == configuration.cells
    generic_next = generic_step(table, configuration).successor
    bag_next = decode_bag_as_grid(bag_step(table, encoded))
    assert bag_next.cells == generic_next.cells
    assert bag_next.generation == generic_next.generation
    assert encode_grid_as_bag(bag_next) == bag_step(table, encoded)


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


@dataclass(frozen=True)
class ShapeOrientationRole:
    shape_id: str
    orientation_id: str

    def __post_init__(self) -> None:
        exact_str(self.shape_id, "shape role")
        exact_str(self.orientation_id, "orientation role")


@dataclass(frozen=True)
class FiniteRoleCodec:
    rows: tuple[tuple[int, ShapeOrientationRole], ...]

    def __post_init__(self) -> None:
        raw = exact_tuple(self.rows, "role-codec rows")
        labels: list[int] = []
        roles: list[ShapeOrientationRole] = []
        for raw_row in raw:
            row = exact_tuple(raw_row, "role-codec row")
            if len(row) != 2:
                raise ValueError("role-codec rows must be label/role pairs")
            label = exact_int(row[0], "role-codec label")
            role = row[1]
            if type(role) is not ShapeOrientationRole:
                raise TypeError("role-codec values must be exact ShapeOrientationRoles")
            labels.append(label)
            roles.append(role)
        if tuple(labels) != tuple(range(len(raw))):
            raise ValueError("role-codec labels must be canonical and complete")
        if len(set(roles)) != len(roles):
            raise ValueError("role-codec roles must be unique")

    def encode(self, role: ShapeOrientationRole) -> int:
        if type(role) is not ShapeOrientationRole:
            raise TypeError("role encoding requires an exact ShapeOrientationRole")
        matches = tuple(label for label, candidate in self.rows if candidate == role)
        if len(matches) != 1:
            raise ValueError("role is outside the declared finite codec")
        return matches[0]

    def decode(self, label: int) -> ShapeOrientationRole:
        key = exact_int(label, "role-codec label")
        if key < 0 or key >= len(self.rows):
            raise ValueError("role-codec label is outside the declared range")
        return self.rows[key][1]


OTHER_SHAPES_CODEC = FiniteRoleCodec(
    tuple(
        (
            label,
            ShapeOrientationRole("source-declared-shape-role", f"source-role-{label}"),
        )
        for label in range(4)
    )
)

# Exact printed patch shapes only.  The source does not state the role-to-color
# assignment or a complete mixed-size compatibility law, so these are never
# passed to ClosedPatchTable or executed as the strict T26 construction.
OTHER_SHAPES_MIXED_RELATION = (
    (3, ((1, 0), (3, 2))),
    (2, ((1,), (3,))),
    (1, ((3, 2),)),
    (0, ((3,),)),
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

    return {
        "page187_generic_events": 4,
        "page187_bag_commuting_events": 2,
        "page187_exact_checkpoints": 3,
        "page187_trace_digest_words": len(trace_digest),
        "page187_trace_digest_int": int(trace_digest[:12], 16),
        "rectangular_2x3_events": 1,
        "derived_rule_count_checks": 3,
        "source_numeric_codecs": 0,
    }


def assert_rank_parameterization() -> dict[str, int]:
    # The same ordered-block kernel has T13 fixed-block concatenation at rank
    # one.  General variable-length T13 remains a broader D019 profile; no
    # claim is made that a plain row-major T13 word retains rank-two topology.
    events = 0
    for block_length in (1, 2):
        words = tuple(product((0, 1), repeat=block_length))
        morphisms = tuple(product(words, repeat=2))
        for zero_word, one_word in morphisms:
            for length in range(1, 5):
                for word in product((0, 1), repeat=length):
                    direct = tuple(
                        child
                        for label in word
                        for child in (zero_word if label == 0 else one_word)
                    )
                    generic = ranked_block_assemble(
                        (len(word),),
                        (block_length,),
                        tuple(zero_word if label == 0 else one_word for label in word),
                    )
                    assert generic == direct
                    events += 1
    assert events == 600

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
        "t13_fixed_block_rank1_events": events,
        "rank2_block_assembly_events": 1,
        "naive_row_major_divergences": 1,
        "flat_whole_state_loss_witnesses": 1,
    }


def assert_boundaries_and_observers() -> dict[str, int]:
    all_white = make_grid(((0, 0), (0, 0)), 2)
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

    for label, role in OTHER_SHAPES_CODEC.rows:
        assert OTHER_SHAPES_CODEC.encode(role) == label
        assert OTHER_SHAPES_CODEC.decode(label) == role
    mixed_shapes = {
        (len(patch), len(patch[0]))
        for _label, patch in OTHER_SHAPES_MIXED_RELATION
    }
    assert mixed_shapes == {(2, 2), (2, 1), (1, 2), (1, 1)}

    # One event cannot recursively fire newborns.  The second event has a
    # different extent and is observably distinct from the first event.
    seed = make_grid(((1,),), 2)
    assert_commutes(NONWHITE_BACKGROUND_TABLE, seed)
    first = generic_step(NONWHITE_BACKGROUND_TABLE, seed).successor
    assert_commutes(NONWHITE_BACKGROUND_TABLE, first)
    second = generic_step(NONWHITE_BACKGROUND_TABLE, first).successor
    assert first.shape == (2, 2)
    assert second.shape == (4, 4)
    assert first.cells != second.cells

    # Bag state is permutation invariant, but the strict decoder still checks
    # exactly one occurrence at every aligned rectangular address.
    encoded = encode_grid_as_bag(page)
    reversed_bag = PlacedTileBag(
        encoded.alphabet_size,
        tuple(reversed(encoded.occurrences)),
        encoded.generation,
    )
    assert reversed_bag == encoded
    assert bag_step(PAGE_187_TABLE, reversed_bag) == bag_step(PAGE_187_TABLE, encoded)

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
        "implicit_white_identity_divergences": 1,
        "render_scale_variants": 2,
        "render_inputs_to_rule": 0,
        "shape_orientation_role_roundtrips": len(OTHER_SHAPES_CODEC.rows),
        "other_shapes_relation_rows": len(OTHER_SHAPES_MIXED_RELATION),
        "other_shapes_strict_executions": 0,
        "newborn_deferral_events": 2,
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

    def rejects(expected: type[BaseException], operation: Callable[[], object]) -> None:
        nonlocal rejections
        expect_rejection(expected, operation)
        rejections += 1

    rejects(TypeError, lambda: checked_alphabet_size(True))
    rejects(ValueError, lambda: checked_alphabet_size(1))
    rejects(TypeError, lambda: make_grid([[0]], 2))
    rejects(ValueError, lambda: make_grid((), 2))
    rejects(ValueError, lambda: make_grid(((),), 2))
    rejects(ValueError, lambda: make_grid(((0, 1), (1,)), 2))
    rejects(ValueError, lambda: make_grid(((2,),), 2))
    rejects(TypeError, lambda: make_grid(((True,),), 2))
    rejects(TypeError, lambda: RectGrid(2, ((0,),), "token"))

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
        lambda: ClosedPatchTable(2, ((0, ((0,),)), (1, ((1, 0),)))),
    )
    rejects(
        ValueError,
        lambda: ClosedPatchTable(2, ((0, ((0, 2),)), (1, ((1, 0),)))),
    )
    rejects(
        ValueError,
        lambda: ClosedPatchTable(2, ((0, ((0,),)), (1, ((1,), (0,))))),
    )
    # Canonicalize the source rows so rejection proves mixed patch shapes are
    # the boundary, not merely the source note's descending presentation.
    mixed_shape_rows = tuple(sorted(OTHER_SHAPES_MIXED_RELATION))
    rejects(ValueError, lambda: ClosedPatchTable(4, mixed_shape_rows))
    rejects(
        TypeError,
        lambda: ClosedPatchTable(2, (((0, 1), ((0,),)), (1, ((1,),)))),
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
        ValueError,
        lambda: apply_flatten2d(
            configuration,
            active,
            (replace(writes[0], patch=((0,),)), *writes[1:]),
        ),
    )
    rejects(
        ValueError,
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
    rejects(ValueError, lambda: ranked_block_assemble((2,), (2,), ((0, 1),)))
    rejects(ValueError, lambda: ranked_block_assemble((1,), (2,), ((0,),)))
    rejects(ValueError, lambda: notes_flatten2d(()))

    bag = encode_grid_as_bag(configuration)
    duplicate = PlacedTileBag(
        2,
        (bag.occurrences[0], bag.occurrences[0], *bag.occurrences[2:]),
        0,
    )
    rejects(ValueError, lambda: decode_bag_as_grid(duplicate))
    rotated = PlacedTileBag(
        2,
        (
            PlacedTile(
                0,
                AffinePose2(
                    ((Fraction(0), Fraction(-1)), (Fraction(1), Fraction(0))),
                    (Fraction(0), Fraction(0)),
                ),
            ),
        ),
        0,
    )
    rejects(ValueError, lambda: decode_bag_as_grid(rotated))
    rejects(TypeError, lambda: bag_step("callback", bag))
    rejects(ValueError, lambda: bag_step(ClosedPatchTable(3, ((0, ((0,),)), (1, ((1,),)), (2, ((2,),)))), bag))

    rejects(
        ValueError,
        lambda: FiniteRoleCodec(
            (
                (0, ShapeOrientationRole("s", "o0")),
                (0, ShapeOrientationRole("s", "o1")),
            )
        ),
    )
    rejects(
        ValueError,
        lambda: FiniteRoleCodec(
            (
                (0, ShapeOrientationRole("s", "o")),
                (1, ShapeOrientationRole("s", "o")),
            )
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

    return {
        "hostile_rejections": rejections,
        "context_fields_exposed": 0,
        "raster_program_fields": 0,
        "free_geometry_rule_fields": 0,
    }


def semantic_digest(counts: dict[str, int]) -> str:
    transcript = "\n".join(f"{key}={counts[key]}" for key in sorted(counts))
    return sha256(transcript.encode("utf-8")).hexdigest()


EXPECTED_SEMANTIC_DIGEST = (
    "b4fdbf272ff544cb824c0244e07240b8bb7b43967efd89ed70ef0637f9488a2a"
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
    counts["total.native_generic_events"] = (
        groups["exhaustive"]["native_generic_events"]
        + groups["source"]["page187_generic_events"]
        + groups["source"]["rectangular_2x3_events"]
        + groups["boundaries"]["nonwhite_background_events"]
        + groups["boundaries"]["newborn_deferral_events"]
    )
    counts["total.commuting_proofs"] = (
        groups["exhaustive"]["native_generic_events"]
        + groups["exhaustive"]["t27_bag_commuting_events"]
        + groups["source"]["page187_bag_commuting_events"]
        + groups["source"]["rectangular_2x3_events"]
        + groups["rank"]["t13_fixed_block_rank1_events"]
    )
    digest = semantic_digest(counts)
    assert digest == EXPECTED_SEMANTIC_DIGEST

    print("T26 semantic oracle: PASS")
    print(f"native_generic_events={counts['total.native_generic_events']}")
    print(f"commuting_proofs={counts['total.commuting_proofs']}")
    print(
        "event_partition="
        f"binary_2x2:{groups['exhaustive']['native_generic_events']},"
        f"page187:{groups['source']['page187_generic_events']},"
        f"rectangular_2x3:{groups['source']['rectangular_2x3_events']},"
        f"nonwhite_background:{groups['boundaries']['nonwhite_background_events']},"
        f"newborn_deferral:{groups['boundaries']['newborn_deferral_events']}"
    )
    print(
        "strict_T26=discrete_t+2D;configuration=finite_nonempty_rectangular_tile_grid;"
        "alphabet=finite_tile_labels;frontier=AllOldTiles;neighborhood=SelfOnly"
    )
    print(
        "rule=total_closed_TileLabel_to_uniform_nonempty_rectangular_patch;"
        "UPDATE=exact_Flatten2D_block_assembly;old_snapshot=YES;newborn_deferral=YES;"
        "overlap_policy=NOT_APPLICABLE"
    )
    print(
        "rule_counts=derived_k^(k*h*w);"
        "binary_2x2:256;ternary_3x3:7625597484987;four_color_2x2:4294967296;"
        "source_numeric_codec=NONE"
    )
    print(
        "rank_relation=T13_fixed_block_is_rank1;T26_is_rank2_parameterization_of_D019;"
        f"rank1_commutations={groups['rank']['t13_fixed_block_rank1_events']};"
        "plain_row_major_T13_concatenation_for_rank2=REJECTED"
    )
    print(
        "bag_relation=lossless_restriction_of_T27_addressed_pose_bag;"
        f"bag_commutations={groups['exhaustive']['t27_bag_commuting_events'] + groups['source']['page187_bag_commuting_events'] + groups['source']['rectangular_2x3_events']};"
        "required_invariant=aligned_uniform_no_hole_no_overlap_rectangular_tiling;"
        "arbitrary_free_geometry=T27"
    )
    print(
        "other_shapes=finite_shape_orientation_roles_may_be_color_encoded;"
        "printed_mixed_patch_rule=RELATION_CONTROL;strict_executions=0;"
        "source_role_to_color_assignment=UNSPECIFIED;invented_compatibility_law=NONE"
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
        "classification=T13_D019_rank2_parameterization+T27_category3_restricted_representation;"
        "new_T26_UPDATE_algebra=NONE;new_executor=NONE;T28_contextual_choice=SEPARATE"
    )
    print(f"hostile_rejections={groups['hostile']['hostile_rejections']}")
    print(f"semantic_digest={digest}")


if __name__ == "__main__":
    main()
