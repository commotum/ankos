#!/usr/bin/env python3
"""Dependency-free semantic and runtime-architecture audit for T24.

This Goal 1 oracle reconstructs higher-dimensional and alternative-lattice
cellular automata as instances of one branch-free SimpleProgram event:

    active = FRONTIER.select(configuration)
    reads  = NEIGHBORHOOD.read(configuration, active)
    writes = RULE(active, reads)
    next   = UPDATE.apply(configuration, active, writes)

The native evaluators below operate directly on periodic ``Z^d`` coefficient
coordinates or on literal fixed-incidence rows.  The generic evaluator instead
uses a typed immutable support, an incidence relation, closed rule-table data,
and snapshot-parallel same-site assignments.  Equality is checked one native
event for one generic event; no microstep encoding, callback, family switch, or
arbitrary-CA interpreter is used as evidence.

Strict source-backed profiles covered here are:

* ``Self + k*AxesTotal`` over ``2d`` axial neighbors;
* ``Self + k*FullTotal`` over ``3**d - 1`` surrounding positions;
* complete positional maps over an explicitly sorted offset list;
* the six-neighbor hexagonal distortion codec and its rule schemas/codes;
* fixed repetitive lattices with the source-declared neighbor counts;
* alternating-orientation, congruent-tile, two-tile, and homogeneous or
  finite-type fixed-incidence presentations; and
* unlabelled-incidence totalistic restrictions versus labelled-port maps.

The Book gives only neighbor counts, not complete global incidence data, for
several named 3D/4D lattices.  Tests of those entries therefore prove exactly
the declared degree schema over arbitrary validated fixed incidence and do not
invent a plate-derived global lattice.  Explicit coordinate fixtures used to
exercise the same generic carrier are marked as semantic witnesses rather than
source transcriptions.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from itertools import permutations, product
from math import comb, prod
from typing import Protocol


if not __debug__:
    raise RuntimeError("T24 semantic verification requires assertions; do not run with -O")


Coord = tuple[int, ...]
Offset = tuple[int, ...]
Cells = tuple[int, ...]


def require_int(value: object, name: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{name} must be an exact int")
    return value


def require_bool(value: object, name: str) -> bool:
    if type(value) is not bool:
        raise TypeError(f"{name} must be an exact bool")
    return value


def require_str(value: object, name: str) -> str:
    if type(value) is not str or not value:
        raise TypeError(f"{name} must be a nonempty exact str")
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


def checked_shape(value: object, name: str = "shape") -> tuple[int, ...]:
    raw = require_tuple(value, name)
    if not raw:
        raise ValueError("shape must have positive dimension")
    shape = tuple(require_int(item, "shape extent") for item in raw)
    if any(item <= 0 for item in shape):
        raise ValueError("shape extents must be positive")
    return shape


def add_coord(left: Coord, right: Offset) -> Coord:
    if len(left) != len(right):
        raise ValueError("coordinate dimensions differ")
    return tuple(a + b for a, b in zip(left, right, strict=True))


def all_coords(shape: tuple[int, ...]) -> tuple[Coord, ...]:
    return tuple(product(*(range(extent) for extent in shape)))


def flat_index(shape: tuple[int, ...], coord: Coord) -> int:
    if len(shape) != len(coord):
        raise ValueError("coordinate has the wrong dimension")
    result = 0
    for extent, component in zip(shape, coord, strict=True):
        if component < 0 or component >= extent:
            raise ValueError("coordinate is outside the finite quotient")
        result = result * extent + component
    return result


def coord_from_flat(shape: tuple[int, ...], index: int) -> Coord:
    value = require_int(index, "flat index")
    size = prod(shape)
    if value < 0 or value >= size:
        raise ValueError("flat index is outside the finite quotient")
    digits = [0] * len(shape)
    for position in range(len(shape) - 1, -1, -1):
        value, digits[position] = divmod(value, shape[position])
    return tuple(digits)


def context_index(context: tuple[int, ...], alphabet_size: int) -> int:
    k = require_int(alphabet_size, "alphabet size")
    if k < 2:
        raise ValueError("alphabet size must be at least two")
    raw = require_tuple(context, "context")
    result = 0
    for item in raw:
        value = require_int(item, "context value")
        if value < 0 or value >= k:
            raise ValueError("context value is outside the alphabet")
        result = result * k + value
    return result


def context_from_index(index: int, width: int, alphabet_size: int) -> tuple[int, ...]:
    value = require_int(index, "context index")
    count = require_int(width, "context width")
    k = require_int(alphabet_size, "alphabet size")
    if count <= 0 or k < 2:
        raise ValueError("context width and alphabet size are invalid")
    if value < 0 or value >= k**count:
        raise ValueError("context index is outside the declared table")
    out = [0] * count
    for position in range(count - 1, -1, -1):
        value, out[position] = divmod(value, k)
    return tuple(out)


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


class ClosedTable(Protocol):
    alphabet_size: int
    row_count: int

    def at(self, index: int) -> int: ...


@dataclass(frozen=True)
class DenseTable:
    """Complete finite table; no evaluator callback is stored."""

    alphabet_size: int
    row_count: int
    outputs: tuple[int, ...]

    def __post_init__(self) -> None:
        k = require_int(self.alphabet_size, "table alphabet size")
        rows = require_int(self.row_count, "table row count")
        raw = require_tuple(self.outputs, "table outputs")
        if k < 2 or rows <= 0:
            raise ValueError("table dimensions are invalid")
        if len(raw) != rows:
            raise ValueError("dense table output count is wrong")
        alphabet = FiniteAlphabet(k)
        for output in raw:
            alphabet.check(output, "table output")

    def at(self, index: int) -> int:
        checked = require_int(index, "table index")
        if checked < 0 or checked >= self.row_count:
            raise ValueError("table index is out of range")
        return self.outputs[checked]


@dataclass(frozen=True)
class DefaultOverridesTable:
    """Complete bounded table encoded by a default and sorted finite overrides."""

    alphabet_size: int
    row_count: int
    default: int
    overrides: tuple[tuple[int, int], ...]

    def __post_init__(self) -> None:
        k = require_int(self.alphabet_size, "table alphabet size")
        rows = require_int(self.row_count, "table row count")
        if k < 2 or rows <= 0:
            raise ValueError("table dimensions are invalid")
        alphabet = FiniteAlphabet(k)
        alphabet.check(self.default, "default output")
        raw = require_tuple(self.overrides, "table overrides")
        previous = -1
        for entry in raw:
            pair = require_tuple(entry, "table override")
            if len(pair) != 2:
                raise ValueError("table override must be an index/output pair")
            index = require_int(pair[0], "override index")
            alphabet.check(pair[1], "override output")
            if index <= previous or index >= rows:
                raise ValueError("override indices must be unique, sorted, and in range")
            previous = index

    def at(self, index: int) -> int:
        checked = require_int(index, "table index")
        if checked < 0 or checked >= self.row_count:
            raise ValueError("table index is out of range")
        for override_index, output in self.overrides:
            if override_index == checked:
                return output
            if override_index > checked:
                break
        return self.default


TableCarrier = DenseTable | DefaultOverridesTable


def validate_closed_table(table: object, alphabet_size: int, row_count: int) -> TableCarrier:
    if type(table) not in (DenseTable, DefaultOverridesTable):
        raise TypeError("rule tables must use a closed immutable carrier")
    assert isinstance(table, (DenseTable, DefaultOverridesTable))
    if table.alphabet_size != alphabet_size or table.row_count != row_count:
        raise ValueError("rule table dimensions do not match the schema")
    return table


def deterministic_table(alphabet_size: int, row_count: int, salt: int) -> DenseTable:
    k = require_int(alphabet_size, "alphabet size")
    rows = require_int(row_count, "row count")
    shift = require_int(salt, "table salt")
    return DenseTable(k, rows, tuple((index * 7 + shift) % k for index in range(rows)))


def binary_table_from_code(code: int, row_count: int) -> DenseTable:
    number = require_int(code, "binary rule code")
    rows = require_int(row_count, "binary table row count")
    if rows <= 0 or number < 0 or number >= 1 << rows:
        raise ValueError("binary rule code is outside the declared table")
    return DenseTable(2, rows, tuple((number >> index) & 1 for index in range(rows)))


def binary_code_from_table(table: DenseTable) -> int:
    if type(table) is not DenseTable or table.alphabet_size != 2:
        raise TypeError("binary code requires a dense binary table")
    return sum(output << index for index, output in enumerate(table.outputs))


@dataclass(frozen=True)
class IncidenceRelation:
    """One fixed occurrence-valued access relation over a support.

    Rows deliberately permit repeated targets: distinct offsets, ports, or
    parallel edges remain distinct rule inputs after quotient aliasing.
    """

    name: str
    rows: tuple[tuple[int, ...], ...]
    ordered: bool
    port_labels: tuple[tuple[str, ...], ...] | None = None

    def __post_init__(self) -> None:
        require_str(self.name, "relation name")
        raw_rows = require_tuple(self.rows, "incidence rows")
        require_bool(self.ordered, "ordered flag")
        for raw_row in raw_rows:
            row = require_tuple(raw_row, "incidence row")
            for target in row:
                index = require_int(target, "incidence target")
                if index < 0:
                    raise ValueError("incidence targets must be nonnegative")
        if self.port_labels is None:
            return
        labels = require_tuple(self.port_labels, "port-label rows")
        if not self.ordered:
            raise ValueError("unlabelled incidence cannot carry ordered port labels")
        if len(labels) != len(raw_rows):
            raise ValueError("port-label rows do not match incidence rows")
        for row, label_row in zip(raw_rows, labels, strict=True):
            declared = require_tuple(label_row, "port-label row")
            if len(declared) != len(row):
                raise ValueError("port labels do not match incidence arity")
            for label in declared:
                require_str(label, "port label")
            if len(set(declared)) != len(declared):
                raise ValueError("port labels must be unique within a row")


@dataclass(frozen=True)
class FixedSupport:
    keys: tuple[Coord, ...]
    site_types: tuple[str, ...]
    relations: tuple[IncidenceRelation, ...]

    def __post_init__(self) -> None:
        keys = require_tuple(self.keys, "support keys")
        types = require_tuple(self.site_types, "site types")
        relations = require_tuple(self.relations, "support relations")
        if not keys or len(types) != len(keys):
            raise ValueError("support keys and site types must be nonempty and aligned")
        dimension: int | None = None
        for raw_key in keys:
            key = require_tuple(raw_key, "support key")
            if dimension is None:
                dimension = len(key)
            if len(key) != dimension:
                raise ValueError("support keys must share one coordinate width")
            for value in key:
                require_int(value, "support-key component")
        if len(set(keys)) != len(keys):
            raise ValueError("support keys must be unique")
        for site_type in types:
            require_str(site_type, "site type")
        if not relations:
            raise ValueError("support must declare at least one incidence relation")
        names: set[str] = set()
        for relation in relations:
            if type(relation) is not IncidenceRelation:
                raise TypeError("support relations must be exact IncidenceRelation values")
            if relation.name in names:
                raise ValueError("relation names must be unique")
            names.add(relation.name)
            if len(relation.rows) != len(keys):
                raise ValueError("incidence row count must equal support size")
            for row in relation.rows:
                if any(target >= len(keys) for target in row):
                    raise ValueError("incidence target is outside the support")

    def relation(self, name: str) -> IncidenceRelation:
        key = require_str(name, "relation name")
        matches = tuple(relation for relation in self.relations if relation.name == key)
        if len(matches) != 1:
            raise ValueError(f"support has no unique relation {key!r}")
        return matches[0]


@dataclass(frozen=True, eq=False)
class SnapshotToken:
    generation: int

    def __post_init__(self) -> None:
        generation = require_int(self.generation, "generation")
        if generation < 0:
            raise ValueError("generation must be nonnegative")


@dataclass(frozen=True)
class Configuration:
    alphabet: FiniteAlphabet
    support: FixedSupport
    cells: Cells
    snapshot_token: SnapshotToken = field(compare=False, repr=False)

    def __post_init__(self) -> None:
        if type(self.alphabet) is not FiniteAlphabet:
            raise TypeError("configuration alphabet must be FiniteAlphabet")
        if type(self.support) is not FixedSupport:
            raise TypeError("configuration support must be FixedSupport")
        raw = require_tuple(self.cells, "configuration cells")
        if len(raw) != len(self.support.keys):
            raise ValueError("configuration cell count does not match the support")
        for value in raw:
            self.alphabet.check(value)
        if type(self.snapshot_token) is not SnapshotToken:
            raise TypeError("configuration token must be exact SnapshotToken")

    @property
    def generation(self) -> int:
        return self.snapshot_token.generation


@dataclass(frozen=True)
class AllSites:
    """Every old support site fires once."""


@dataclass(frozen=True)
class RelationNeighborhood:
    relation_name: str
    include_self: bool

    def __post_init__(self) -> None:
        require_str(self.relation_name, "neighborhood relation name")
        require_bool(self.include_self, "include-self flag")


@dataclass(frozen=True)
class LocalRead:
    site_index: int
    site_type: str
    center: int | None
    neighbors: tuple[int, ...]
    ordered: bool
    port_labels: tuple[str, ...] | None

    def __post_init__(self) -> None:
        index = require_int(self.site_index, "read site index")
        if index < 0:
            raise ValueError("read site index must be nonnegative")
        require_str(self.site_type, "read site type")
        if self.center is not None:
            require_int(self.center, "read center")
        raw = require_tuple(self.neighbors, "read neighbors")
        for value in raw:
            require_int(value, "read neighbor")
        require_bool(self.ordered, "read ordered flag")
        if self.port_labels is not None:
            labels = require_tuple(self.port_labels, "read port labels")
            if len(labels) != len(raw) or not self.ordered:
                raise ValueError("read port labels require aligned ordered neighbors")
            for label in labels:
                require_str(label, "read port label")


@dataclass(frozen=True)
class CountCase:
    site_type: str
    degree: int
    table: TableCarrier

    def __post_init__(self) -> None:
        require_str(self.site_type, "count-case site type")
        degree = require_int(self.degree, "count-case degree")
        if degree < 0:
            raise ValueError("count-case degree must be nonnegative")
        if type(self.table) not in (DenseTable, DefaultOverridesTable):
            raise TypeError("count-case table must be a closed table")


@dataclass(frozen=True)
class SelfCountRule:
    """Table indexed by ``Self + k*sum(neighbor occurrences)``."""

    alphabet_size: int
    cases: tuple[CountCase, ...]

    def __post_init__(self) -> None:
        k = require_int(self.alphabet_size, "count-rule alphabet size")
        raw = require_tuple(self.cases, "count-rule cases")
        if k < 2 or not raw:
            raise ValueError("count-rule schema is invalid")
        seen: set[str] = set()
        for case in raw:
            if type(case) is not CountCase:
                raise TypeError("count-rule cases must be exact CountCase values")
            if case.site_type in seen:
                raise ValueError("count-rule site types must be unique")
            seen.add(case.site_type)
            rows = k * (case.degree * (k - 1) + 1)
            validate_closed_table(case.table, k, rows)

    def case_for(self, site_type: str) -> CountCase:
        matches = tuple(case for case in self.cases if case.site_type == site_type)
        if len(matches) != 1:
            raise ValueError("count rule has no unique case for the site type")
        return matches[0]

    def validate(self, alphabet: FiniteAlphabet, support: FixedSupport, read: RelationNeighborhood) -> None:
        if alphabet.size != self.alphabet_size:
            raise ValueError("count rule and configuration alphabets differ")
        if not read.include_self:
            raise ValueError("SelfCountRule requires an explicit Self read")
        relation = support.relation(read.relation_name)
        for site_index, site_type in enumerate(support.site_types):
            case = self.case_for(site_type)
            if len(relation.rows[site_index]) != case.degree:
                raise ValueError("count-rule degree does not match typed incidence")
        if set(support.site_types) != {case.site_type for case in self.cases}:
            raise ValueError("count-rule cases must exactly cover support site types")

    def evaluate(self, read: LocalRead) -> int:
        if read.center is None:
            raise ValueError("count rule received no Self value")
        case = self.case_for(read.site_type)
        if len(read.neighbors) != case.degree:
            raise ValueError("count-rule read has the wrong degree")
        index = read.center + self.alphabet_size * sum(read.neighbors)
        return case.table.at(index)


@dataclass(frozen=True)
class PositionalCase:
    site_type: str
    width: int
    table: TableCarrier

    def __post_init__(self) -> None:
        require_str(self.site_type, "positional-case site type")
        width = require_int(self.width, "positional-case width")
        if width <= 0:
            raise ValueError("positional-case width must be positive")
        if type(self.table) not in (DenseTable, DefaultOverridesTable):
            raise TypeError("positional-case table must be a closed table")


@dataclass(frozen=True)
class PositionalRule:
    """Complete map over an explicitly ordered occurrence list."""

    alphabet_size: int
    cases: tuple[PositionalCase, ...]

    def __post_init__(self) -> None:
        k = require_int(self.alphabet_size, "positional-rule alphabet size")
        raw = require_tuple(self.cases, "positional-rule cases")
        if k < 2 or not raw:
            raise ValueError("positional-rule schema is invalid")
        seen: set[str] = set()
        for case in raw:
            if type(case) is not PositionalCase:
                raise TypeError("positional-rule cases must be exact PositionalCase values")
            if case.site_type in seen:
                raise ValueError("positional-rule site types must be unique")
            seen.add(case.site_type)
            validate_closed_table(case.table, k, k**case.width)

    def case_for(self, site_type: str) -> PositionalCase:
        matches = tuple(case for case in self.cases if case.site_type == site_type)
        if len(matches) != 1:
            raise ValueError("positional rule has no unique case for the site type")
        return matches[0]

    def validate(self, alphabet: FiniteAlphabet, support: FixedSupport, read: RelationNeighborhood) -> None:
        if alphabet.size != self.alphabet_size:
            raise ValueError("positional rule and configuration alphabets differ")
        if read.include_self:
            raise ValueError("positional Self, if used, must be a declared relation slot")
        relation = support.relation(read.relation_name)
        if not relation.ordered:
            raise ValueError("unlabelled incidence supports only permutation-invariant rules")
        for site_index, site_type in enumerate(support.site_types):
            case = self.case_for(site_type)
            if len(relation.rows[site_index]) != case.width:
                raise ValueError("positional-rule width does not match typed incidence")
        if set(support.site_types) != {case.site_type for case in self.cases}:
            raise ValueError("positional cases must exactly cover support site types")

    def evaluate(self, read: LocalRead) -> int:
        if read.center is not None or not read.ordered:
            raise ValueError("positional rule requires ordered slots and no implicit Self")
        case = self.case_for(read.site_type)
        if len(read.neighbors) != case.width:
            raise ValueError("positional-rule read has the wrong width")
        return case.table.at(context_index(read.neighbors, self.alphabet_size))


Rule = SelfCountRule | PositionalRule


@dataclass(frozen=True)
class SimpleProgram:
    alphabet: FiniteAlphabet
    frontier: AllSites
    neighborhood: RelationNeighborhood
    rule: Rule

    def __post_init__(self) -> None:
        if type(self.alphabet) is not FiniteAlphabet:
            raise TypeError("program alphabet must be FiniteAlphabet")
        if type(self.frontier) is not AllSites:
            raise TypeError("T24 strict programs use AllSites")
        if type(self.neighborhood) is not RelationNeighborhood:
            raise TypeError("program neighborhood must be RelationNeighborhood")
        if type(self.rule) not in (SelfCountRule, PositionalRule):
            raise TypeError("program rule must be a closed typed rule")


@dataclass(frozen=True)
class SiteHandle:
    snapshot_token: SnapshotToken
    site_index: int

    def __post_init__(self) -> None:
        if type(self.snapshot_token) is not SnapshotToken:
            raise TypeError("site handle token must be exact SnapshotToken")
        index = require_int(self.site_index, "site-handle index")
        if index < 0:
            raise ValueError("site-handle index must be nonnegative")


@dataclass(frozen=True)
class SiteAssignment:
    source: SiteHandle
    target_index: int
    value: int

    def __post_init__(self) -> None:
        if type(self.source) is not SiteHandle:
            raise TypeError("assignment source must be SiteHandle")
        target = require_int(self.target_index, "assignment target")
        if target < 0:
            raise ValueError("assignment target must be nonnegative")
        require_int(self.value, "assignment value")


def select_all_sites(old: Configuration, frontier: AllSites) -> tuple[SiteHandle, ...]:
    if type(frontier) is not AllSites:
        raise TypeError("unsupported frontier")
    return tuple(SiteHandle(old.snapshot_token, index) for index in range(len(old.cells)))


def validate_handles(old: Configuration, active: tuple[SiteHandle, ...]) -> None:
    raw = require_tuple(active, "active handles")
    if len(raw) != len(old.cells):
        raise ValueError("AllSites must select every support site exactly once")
    indices: list[int] = []
    for handle in raw:
        if type(handle) is not SiteHandle or handle.snapshot_token is not old.snapshot_token:
            raise ValueError("active handle is foreign or stale")
        if handle.site_index >= len(old.cells):
            raise ValueError("active handle is outside the support")
        indices.append(handle.site_index)
    if tuple(sorted(indices)) != tuple(range(len(old.cells))):
        raise ValueError("AllSites handles are duplicated or incomplete")


def read_neighborhood(
    old: Configuration,
    active: tuple[SiteHandle, ...],
    neighborhood: RelationNeighborhood,
) -> tuple[LocalRead, ...]:
    validate_handles(old, active)
    relation = old.support.relation(neighborhood.relation_name)
    reads: list[LocalRead] = []
    for handle in active:
        index = handle.site_index
        row = relation.rows[index]
        labels = None if relation.port_labels is None else relation.port_labels[index]
        reads.append(
            LocalRead(
                index,
                old.support.site_types[index],
                old.cells[index] if neighborhood.include_self else None,
                tuple(old.cells[target] for target in row),
                relation.ordered,
                labels,
            )
        )
    return tuple(reads)


def make_assignments(
    old: Configuration,
    program: SimpleProgram,
    active: tuple[SiteHandle, ...],
    reads: tuple[LocalRead, ...],
) -> tuple[SiteAssignment, ...]:
    validate_handles(old, active)
    program.rule.validate(program.alphabet, old.support, program.neighborhood)
    if len(reads) != len(active):
        raise ValueError("read count does not match active count")
    out: list[SiteAssignment] = []
    for handle, read in zip(active, reads, strict=True):
        if read.site_index != handle.site_index:
            raise ValueError("read order does not match active order")
        value = program.rule.evaluate(read)
        program.alphabet.check(value, "rule output")
        out.append(SiteAssignment(handle, handle.site_index, value))
    return tuple(out)


def apply_parallel(
    old: Configuration,
    active: tuple[SiteHandle, ...],
    assignments: tuple[SiteAssignment, ...],
) -> Configuration:
    validate_handles(old, active)
    raw = require_tuple(assignments, "assignments")
    if len(raw) != len(active):
        raise ValueError("assignment count does not match active count")
    targets: list[int] = []
    next_cells = list(old.cells)
    for handle, assignment in zip(active, raw, strict=True):
        if type(assignment) is not SiteAssignment:
            raise TypeError("assignments must be exact SiteAssignment values")
        if assignment.source != handle or assignment.source.snapshot_token is not old.snapshot_token:
            raise ValueError("assignment source is foreign, stale, or reordered")
        if assignment.target_index != handle.site_index:
            raise ValueError("T24 strict UPDATE requires one same-site write")
        old.alphabet.check(assignment.value, "assignment value")
        targets.append(assignment.target_index)
        next_cells[assignment.target_index] = assignment.value
    if tuple(sorted(targets)) != tuple(range(len(old.cells))):
        raise ValueError("assignment targets are duplicated or incomplete")
    return Configuration(
        old.alphabet,
        old.support,
        tuple(next_cells),
        SnapshotToken(old.generation + 1),
    )


def generic_step(program: SimpleProgram, old: Configuration) -> Configuration:
    if old.alphabet != program.alphabet:
        raise ValueError("program and configuration alphabets differ")
    active = select_all_sites(old, program.frontier)
    reads = read_neighborhood(old, active, program.neighborhood)
    writes = make_assignments(old, program, active, reads)
    return apply_parallel(old, active, writes)


# ---------------------------------------------------------------------------
# Independent native translation-lattice semantics and lossless compilation
# ---------------------------------------------------------------------------


def axis_offsets(dimension: int) -> tuple[Offset, ...]:
    d = require_int(dimension, "dimension")
    if d <= 0:
        raise ValueError("dimension must be positive")
    offsets: list[Offset] = []
    for axis in range(d):
        for sign in (-1, 1):
            value = [0] * d
            value[axis] = sign
            offsets.append(tuple(value))
    return tuple(sorted(offsets))


def full_shell_offsets(dimension: int) -> tuple[Offset, ...]:
    d = require_int(dimension, "dimension")
    if d <= 0:
        raise ValueError("dimension must be positive")
    zero = (0,) * d
    return tuple(offset for offset in product((-1, 0, 1), repeat=d) if offset != zero)


def axis_positions(dimension: int) -> tuple[Offset, ...]:
    d = require_int(dimension, "dimension")
    return tuple(sorted((*axis_offsets(d), (0,) * d)))


def full_positions(dimension: int) -> tuple[Offset, ...]:
    d = require_int(dimension, "dimension")
    if d <= 0:
        raise ValueError("dimension must be positive")
    return tuple(product((-1, 0, 1), repeat=d))


def self_count_case_count(degree: int, alphabet_size: int) -> int:
    s = require_int(degree, "neighbor degree")
    k = require_int(alphabet_size, "alphabet size")
    if s < 0 or k < 2:
        raise ValueError("count-profile dimensions are invalid")
    return k * (s * (k - 1) + 1)


def bareiss_determinant(matrix: tuple[tuple[int, ...], ...]) -> int:
    raw = require_tuple(matrix, "basis matrix")
    if not raw:
        raise ValueError("basis matrix must be nonempty")
    n = len(raw)
    work: list[list[int]] = []
    for raw_row in raw:
        row = require_tuple(raw_row, "basis row")
        if len(row) != n:
            raise ValueError("basis matrix must be square")
        work.append([require_int(value, "basis component") for value in row])
    sign = 1
    denominator = 1
    for pivot_index in range(n - 1):
        pivot_row = next(
            (row for row in range(pivot_index, n) if work[row][pivot_index] != 0),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != pivot_index:
            work[pivot_index], work[pivot_row] = work[pivot_row], work[pivot_index]
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, n):
            for column in range(pivot_index + 1, n):
                numerator = work[row][column] * pivot - work[row][pivot_index] * work[pivot_index][column]
                if numerator % denominator:
                    raise AssertionError("Bareiss elimination lost exact divisibility")
                work[row][column] = numerator // denominator
            work[row][pivot_index] = 0
        denominator = pivot
    return sign * work[-1][-1]


@dataclass(frozen=True)
class LatticeDescriptor:
    """Coefficient-address lattice plus declared local occurrence offsets.

    ``basis`` is a lossless geometric coordinate representation.  Evolution
    uses the declared incidence offsets; a renderer is not allowed to infer or
    replace them.
    """

    name: str
    basis: tuple[tuple[int, ...], ...]
    offsets: tuple[Offset, ...]

    def __post_init__(self) -> None:
        require_str(self.name, "lattice name")
        basis = require_tuple(self.basis, "lattice basis")
        if not basis or bareiss_determinant(self.basis) == 0:
            raise ValueError("lattice basis must be square and nonsingular")
        dimension = len(basis)
        offsets = require_tuple(self.offsets, "lattice offsets")
        if not offsets:
            raise ValueError("lattice offsets cannot be empty")
        checked = tuple(checked_coord(offset, dimension, "lattice offset") for offset in offsets)
        if len(set(checked)) != len(checked):
            raise ValueError("native lattice offsets must be unique before quotienting")

    @property
    def dimension(self) -> int:
        return len(self.basis)

    def embed(self, raw_coord: object) -> Coord:
        coord = checked_coord(raw_coord, self.dimension)
        return tuple(
            sum(coord[column] * self.basis[row][column] for column in range(self.dimension))
            for row in range(self.dimension)
        )


def identity_basis(dimension: int) -> tuple[tuple[int, ...], ...]:
    d = require_int(dimension, "dimension")
    if d <= 0:
        raise ValueError("dimension must be positive")
    return tuple(tuple(int(row == column) for column in range(d)) for row in range(d))


@dataclass(frozen=True)
class NativeTranslationState:
    shape: tuple[int, ...]
    alphabet_size: int
    cells: Cells
    generation: int = 0

    def __post_init__(self) -> None:
        shape = checked_shape(self.shape)
        alphabet = FiniteAlphabet(self.alphabet_size)
        raw = require_tuple(self.cells, "native translation cells")
        if len(raw) != prod(shape):
            raise ValueError("native translation cell count does not match shape")
        for value in raw:
            alphabet.check(value)
        generation = require_int(self.generation, "native generation")
        if generation < 0:
            raise ValueError("native generation must be nonnegative")

    def value_at(self, raw_coord: object) -> int:
        coord = checked_coord(raw_coord, len(self.shape))
        resolved = tuple(
            component % extent
            for component, extent in zip(coord, self.shape, strict=True)
        )
        return self.cells[flat_index(self.shape, resolved)]


def compile_translation_support(
    state: NativeTranslationState,
    offsets: tuple[Offset, ...],
    relation_name: str,
    *,
    ordered: bool,
    port_names: tuple[str, ...] | None = None,
) -> FixedSupport:
    raw_offsets = require_tuple(offsets, "translation offsets")
    checked = tuple(
        checked_coord(offset, len(state.shape), "translation offset")
        for offset in raw_offsets
    )
    if len(set(checked)) != len(checked):
        raise ValueError("translation offsets must be unique before quotienting")
    coords = all_coords(state.shape)
    key_to_index = {coord: index for index, coord in enumerate(coords)}
    rows: list[tuple[int, ...]] = []
    for coord in coords:
        targets = []
        for offset in checked:
            resolved = tuple(
                (component + delta) % extent
                for component, delta, extent in zip(coord, offset, state.shape, strict=True)
            )
            targets.append(key_to_index[resolved])
        rows.append(tuple(targets))
    labels = None
    if port_names is not None:
        names = require_tuple(port_names, "port names")
        if len(names) != len(checked):
            raise ValueError("port names do not match translation offsets")
        for name in names:
            require_str(name, "port name")
        labels = tuple(tuple(names) for _ in coords)
    relation = IncidenceRelation(relation_name, tuple(rows), ordered, labels)
    return FixedSupport(coords, ("cell",) * len(coords), (relation,))


def encode_translation(
    state: NativeTranslationState,
    offsets: tuple[Offset, ...],
    relation_name: str = "local",
    *,
    ordered: bool = True,
    port_names: tuple[str, ...] | None = None,
) -> Configuration:
    support = compile_translation_support(
        state,
        offsets,
        relation_name,
        ordered=ordered,
        port_names=port_names,
    )
    return Configuration(
        FiniteAlphabet(state.alphabet_size),
        support,
        state.cells,
        SnapshotToken(state.generation),
    )


def decode_translation(generic: Configuration, shape: tuple[int, ...]) -> NativeTranslationState:
    expected_shape = checked_shape(shape)
    if generic.support.keys != all_coords(expected_shape):
        raise ValueError("generic support is not the declared coordinate quotient")
    return NativeTranslationState(
        expected_shape,
        generic.alphabet.size,
        generic.cells,
        generic.generation,
    )


def native_translation_count_step(
    old: NativeTranslationState,
    offsets: tuple[Offset, ...],
    table: TableCarrier,
) -> NativeTranslationState:
    degree = len(offsets)
    validate_closed_table(
        table,
        old.alphabet_size,
        self_count_case_count(degree, old.alphabet_size),
    )
    next_cells: list[int] = []
    for coord in all_coords(old.shape):
        center = old.value_at(coord)
        neighbor_sum = sum(old.value_at(add_coord(coord, offset)) for offset in offsets)
        next_cells.append(table.at(center + old.alphabet_size * neighbor_sum))
    return NativeTranslationState(old.shape, old.alphabet_size, tuple(next_cells), old.generation + 1)


def native_translation_positional_step(
    old: NativeTranslationState,
    offsets: tuple[Offset, ...],
    table: TableCarrier,
) -> NativeTranslationState:
    validate_closed_table(
        table,
        old.alphabet_size,
        old.alphabet_size ** len(offsets),
    )
    next_cells: list[int] = []
    for coord in all_coords(old.shape):
        context = tuple(old.value_at(add_coord(coord, offset)) for offset in offsets)
        next_cells.append(table.at(context_index(context, old.alphabet_size)))
    return NativeTranslationState(old.shape, old.alphabet_size, tuple(next_cells), old.generation + 1)


def count_program(alphabet_size: int, degree: int, table: TableCarrier, relation: str = "local") -> SimpleProgram:
    k = require_int(alphabet_size, "alphabet size")
    case = CountCase("cell", degree, table)
    return SimpleProgram(
        FiniteAlphabet(k),
        AllSites(),
        RelationNeighborhood(relation, True),
        SelfCountRule(k, (case,)),
    )


def positional_program(alphabet_size: int, width: int, table: TableCarrier, relation: str = "local") -> SimpleProgram:
    k = require_int(alphabet_size, "alphabet size")
    case = PositionalCase("cell", width, table)
    return SimpleProgram(
        FiniteAlphabet(k),
        AllSites(),
        RelationNeighborhood(relation, False),
        PositionalRule(k, (case,)),
    )


# ---------------------------------------------------------------------------
# Independent native fixed-incidence semantics
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class NativeIncidenceState:
    keys: tuple[Coord, ...]
    site_types: tuple[str, ...]
    rows: tuple[tuple[int, ...], ...]
    ordered: bool
    alphabet_size: int
    cells: Cells
    generation: int = 0
    port_labels: tuple[tuple[str, ...], ...] | None = None

    def __post_init__(self) -> None:
        relation = IncidenceRelation("native", self.rows, self.ordered, self.port_labels)
        FixedSupport(self.keys, self.site_types, (relation,))
        alphabet = FiniteAlphabet(self.alphabet_size)
        raw = require_tuple(self.cells, "native incidence cells")
        if len(raw) != len(self.keys):
            raise ValueError("native incidence cells do not match support")
        for value in raw:
            alphabet.check(value)
        generation = require_int(self.generation, "native incidence generation")
        if generation < 0:
            raise ValueError("native incidence generation must be nonnegative")


def encode_incidence(state: NativeIncidenceState, relation_name: str = "local") -> Configuration:
    relation = IncidenceRelation(
        relation_name,
        state.rows,
        state.ordered,
        state.port_labels,
    )
    support = FixedSupport(state.keys, state.site_types, (relation,))
    return Configuration(
        FiniteAlphabet(state.alphabet_size),
        support,
        state.cells,
        SnapshotToken(state.generation),
    )


def decode_incidence(generic: Configuration, template: NativeIncidenceState) -> NativeIncidenceState:
    relation = generic.support.relations[0]
    return NativeIncidenceState(
        generic.support.keys,
        generic.support.site_types,
        relation.rows,
        relation.ordered,
        generic.alphabet.size,
        generic.cells,
        generic.generation,
        relation.port_labels,
    )


def native_count_step(old: NativeIncidenceState, cases: tuple[CountCase, ...]) -> NativeIncidenceState:
    case_by_type = {case.site_type: case for case in cases}
    if set(case_by_type) != set(old.site_types):
        raise ValueError("native count cases do not cover site types")
    next_cells: list[int] = []
    for site_index, (site_type, row) in enumerate(zip(old.site_types, old.rows, strict=True)):
        case = case_by_type[site_type]
        if len(row) != case.degree:
            raise ValueError("native count degree mismatch")
        index = old.cells[site_index] + old.alphabet_size * sum(old.cells[target] for target in row)
        next_cells.append(case.table.at(index))
    return NativeIncidenceState(
        old.keys,
        old.site_types,
        old.rows,
        old.ordered,
        old.alphabet_size,
        tuple(next_cells),
        old.generation + 1,
        old.port_labels,
    )


def native_positional_step(old: NativeIncidenceState, cases: tuple[PositionalCase, ...]) -> NativeIncidenceState:
    if not old.ordered:
        raise ValueError("native positional rule requires labelled/ordered incidence")
    case_by_type = {case.site_type: case for case in cases}
    if set(case_by_type) != set(old.site_types):
        raise ValueError("native positional cases do not cover site types")
    next_cells: list[int] = []
    for site_type, row in zip(old.site_types, old.rows, strict=True):
        case = case_by_type[site_type]
        if len(row) != case.width:
            raise ValueError("native positional width mismatch")
        context = tuple(old.cells[target] for target in row)
        next_cells.append(case.table.at(context_index(context, old.alphabet_size)))
    return NativeIncidenceState(
        old.keys,
        old.site_types,
        old.rows,
        old.ordered,
        old.alphabet_size,
        tuple(next_cells),
        old.generation + 1,
        old.port_labels,
    )


def typed_count_program(
    alphabet_size: int,
    cases: tuple[CountCase, ...],
    relation: str = "local",
) -> SimpleProgram:
    return SimpleProgram(
        FiniteAlphabet(alphabet_size),
        AllSites(),
        RelationNeighborhood(relation, True),
        SelfCountRule(alphabet_size, cases),
    )


def typed_positional_program(
    alphabet_size: int,
    cases: tuple[PositionalCase, ...],
    relation: str = "local",
) -> SimpleProgram:
    return SimpleProgram(
        FiniteAlphabet(alphabet_size),
        AllSites(),
        RelationNeighborhood(relation, False),
        PositionalRule(alphabet_size, cases),
    )


# ---------------------------------------------------------------------------
# Hexagonal source codec, exact quotient maps, and symmetry actions
# ---------------------------------------------------------------------------


# Coefficient-array offsets selected by the Book's 3x3 convolution mask.
HEX_SQUARE_OFFSETS: tuple[Offset, ...] = (
    (-1, -1),
    (-1, 0),
    (0, -1),
    (0, 1),
    (1, 0),
    (1, 1),
)


@dataclass(frozen=True)
class HexDistortionCodec:
    """Exact coefficient-to-center codec behind the distorted square array.

    ``(row, column) -> (row, 2*column-row)`` records the coefficient of
    ``sqrt(3)`` and the exact integer vertical center.  Multiplying the first
    output by ``sqrt(3)`` is a view operation.  The parity invariant makes the
    map lossless without floating-point geometry.
    """

    def encode(self, raw: object) -> Coord:
        row, column = checked_coord(raw, 2, "hex coefficient address")
        return (row, 2 * column - row)

    def decode(self, raw: object) -> Coord:
        row, vertical = checked_coord(raw, 2, "hex center address")
        numerator = vertical + row
        if numerator % 2:
            raise ValueError("hex center violates the staggered parity invariant")
        return (row, numerator // 2)

    def squared_scaled_distance(self, raw_delta: object) -> int:
        row, vertical = checked_coord(raw_delta, 2, "hex-center displacement")
        return 3 * row * row + vertical * vertical


HEX_CODEC = HexDistortionCodec()


def hex_context_rotations(context: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    raw = require_tuple(context, "hex context")
    if len(raw) != 7:
        raise ValueError("hex context must contain Self and six neighbors")
    center = raw[0]
    ring = raw[1:]
    return tuple((center, *(ring[shift:] + ring[:shift])) for shift in range(6))


def hex_context_dihedral(context: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    rotations = hex_context_rotations(context)
    center = context[0]
    reflected_ring = tuple(reversed(context[1:]))
    reflected = tuple(
        (center, *(reflected_ring[shift:] + reflected_ring[:shift]))
        for shift in range(6)
    )
    return (*rotations, *reflected)


def orbit_partition(
    contexts: tuple[tuple[int, ...], ...],
    action: str,
) -> tuple[tuple[tuple[int, ...], ...], ...]:
    if action not in ("rotation", "dihedral"):
        raise ValueError("unknown hex symmetry action")
    remaining = set(contexts)
    orbits: list[tuple[tuple[int, ...], ...]] = []
    while remaining:
        seed = min(remaining)
        images = (
            hex_context_rotations(seed)
            if action == "rotation"
            else hex_context_dihedral(seed)
        )
        orbit = tuple(sorted(set(images)))
        if any(image not in contexts for image in orbit):
            raise AssertionError("group action left the context domain")
        remaining.difference_update(orbit)
        orbits.append(orbit)
    return tuple(sorted(orbits, key=lambda orbit: orbit[0]))


def expand_self_count_table(degree: int, compact: DenseTable) -> DenseTable:
    if type(compact) is not DenseTable:
        raise TypeError("fiber expansion requires a dense table")
    k = compact.alphabet_size
    validate_closed_table(compact, k, self_count_case_count(degree, k))
    width = degree + 1
    outputs: list[int] = []
    for index in range(k**width):
        context = context_from_index(index, width, k)
        outputs.append(compact.at(context[0] + k * sum(context[1:])))
    return DenseTable(k, k**width, tuple(outputs))


def factor_self_count_table(degree: int, complete: DenseTable) -> DenseTable:
    if type(complete) is not DenseTable:
        raise TypeError("fiber factoring requires a dense table")
    k = complete.alphabet_size
    width = degree + 1
    validate_closed_table(complete, k, k**width)
    rows = self_count_case_count(degree, k)
    fibers: list[set[int]] = [set() for _ in range(rows)]
    for index, output in enumerate(complete.outputs):
        context = context_from_index(index, width, k)
        compact_index = context[0] + k * sum(context[1:])
        fibers[compact_index].add(output)
    if any(len(fiber) != 1 for fiber in fibers):
        raise ValueError("complete table is not constant on Self/count fibers")
    return DenseTable(k, rows, tuple(next(iter(fiber)) for fiber in fibers))


def factor_orbit_table(
    complete: DenseTable,
    orbits: tuple[tuple[tuple[int, ...], ...], ...],
) -> tuple[int, ...]:
    if type(complete) is not DenseTable or complete.alphabet_size != 2 or complete.row_count != 128:
        raise ValueError("hex orbit factoring requires a complete binary 7-position map")
    outputs: list[int] = []
    for orbit in orbits:
        values = {
            complete.at(context_index(context, 2))
            for context in orbit
        }
        if len(values) != 1:
            raise ValueError("complete map is not constant on the declared symmetry orbit")
        outputs.append(next(iter(values)))
    return tuple(outputs)


def expand_orbit_table(
    outputs: tuple[int, ...],
    orbits: tuple[tuple[tuple[int, ...], ...], ...],
) -> DenseTable:
    raw = require_tuple(outputs, "orbit outputs")
    if len(raw) != len(orbits):
        raise ValueError("orbit output count does not match partition")
    complete = [0] * 128
    seen: set[int] = set()
    for output, orbit in zip(raw, orbits, strict=True):
        value = FiniteAlphabet(2).check(output, "orbit output")
        for context in orbit:
            index = context_index(context, 2)
            if index in seen:
                raise ValueError("symmetry orbits overlap")
            seen.add(index)
            complete[index] = value
    if len(seen) != 128:
        raise ValueError("symmetry orbits do not cover the context domain")
    return DenseTable(2, 128, tuple(complete))


# ---------------------------------------------------------------------------
# Closed topology fixtures (semantic witnesses, not invented source plates)
# ---------------------------------------------------------------------------


SOURCE_NEAREST_DEGREES: tuple[tuple[str, int, int], ...] = (
    ("2D-square", 2, 4),
    ("2D-hexagonal", 2, 6),
    ("3D-cube", 3, 6),
    ("3D-hexagonal-prism", 3, 8),
    ("3D-rhombic-dodecahedron-fcc", 3, 12),
    ("3D-rhombo-hexagonal-elongated-dodecahedron", 3, 12),
    ("3D-truncated-octahedron-bcc", 3, 14),
    ("4D-neighbor-count-8", 4, 8),
    ("4D-neighbor-count-16", 4, 16),
    ("4D-neighbor-count-24", 4, 24),
)


def circulant_rows(size: int, degree: int) -> tuple[tuple[int, ...], ...]:
    n = require_int(size, "circulant size")
    s = require_int(degree, "circulant degree")
    if n <= 0 or s <= 0 or s % 2 or s >= n:
        raise ValueError("circulant witness requires even degree below its size")
    half = s // 2
    return tuple(
        tuple((site + delta) % n for delta in (*range(-half, 0), *range(1, half + 1)))
        for site in range(n)
    )


def raw_regular_incidence(degree: int, cells: Cells, generation: int = 0) -> NativeIncidenceState:
    size = degree + 3 if (degree + 3) % 2 else degree + 3 + 1
    rows = circulant_rows(size, degree)
    if len(cells) != size:
        raise ValueError("regular-incidence cells have the wrong size")
    return NativeIncidenceState(
        tuple((index,) for index in range(size)),
        ("cell",) * size,
        rows,
        False,
        2,
        cells,
        generation,
    )


def complete_bipartite_rows(left: int, right: int) -> tuple[tuple[int, ...], ...]:
    a = require_int(left, "left partition size")
    b = require_int(right, "right partition size")
    if a <= 0 or b <= 0:
        raise ValueError("bipartite partitions must be positive")
    return tuple(
        tuple(range(a, a + b)) if index < a else tuple(range(a))
        for index in range(a + b)
    )


def triangular_tile_state(shape: tuple[int, int], cells: Cells, generation: int = 0) -> NativeIncidenceState:
    rows_count, columns_count = checked_shape(shape)
    keys = tuple(
        (row, column, orientation)
        for row in range(rows_count)
        for column in range(columns_count)
        for orientation in (0, 1)
    )
    index = {key: position for position, key in enumerate(keys)}
    rows: list[tuple[int, ...]] = []
    types: list[str] = []
    for row, column, orientation in keys:
        if orientation == 0:
            targets = (
                (row, column, 1),
                ((row - 1) % rows_count, column, 1),
                (row, (column - 1) % columns_count, 1),
            )
            types.append("up")
        else:
            targets = (
                (row, column, 0),
                ((row + 1) % rows_count, column, 0),
                (row, (column + 1) % columns_count, 0),
            )
            types.append("down")
        rows.append(tuple(index[target] for target in targets))
    if len(cells) != len(keys):
        raise ValueError("triangular-tile cells do not match support")
    labels = tuple(("base", "row", "column") for _ in keys)
    return NativeIncidenceState(
        keys,
        tuple(types),
        tuple(rows),
        True,
        2,
        cells,
        generation,
        labels,
    )


def cells_pattern(size: int, alphabet_size: int, variant: int) -> Cells:
    count = require_int(size, "cell count")
    k = require_int(alphabet_size, "alphabet size")
    salt = require_int(variant, "pattern variant")
    if count <= 0 or k < 2:
        raise ValueError("pattern dimensions are invalid")
    if salt == 0:
        return (0,) * count
    if salt == 1:
        return tuple(index % k for index in range(count))
    if salt == 2:
        return tuple((index * index + 2 * index + 1) % k for index in range(count))
    if salt == 3:
        return tuple(int(index == count // 2) % k for index in range(count))
    return tuple((index * 5 + salt) % k for index in range(count))


def expect_raises(error: type[BaseException], action: object) -> None:
    if not callable(action):
        raise TypeError("expect_raises action must be callable")
    try:
        action()
    except error:
        return
    except Exception as caught:  # pragma: no cover - hostile failure detail
        raise AssertionError(f"expected {error.__name__}, got {type(caught).__name__}") from caught
    raise AssertionError(f"expected {error.__name__}")

