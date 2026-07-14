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
from hashlib import sha256
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

    ``ordered`` means semantically positional, not merely stored in a tuple.
    Such rows therefore require unique stable port labels.  Unlabelled rows are
    occurrence-valued but permutation invariant.
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
            if self.ordered:
                raise ValueError("ordered incidence requires explicit semantic port labels")
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
        if self.port_labels is None:
            if self.ordered:
                raise ValueError("ordered reads require explicit semantic port labels")
            return
        labels = require_tuple(self.port_labels, "read port labels")
        if len(labels) != len(raw) or not self.ordered:
            raise ValueError("read port labels require aligned ordered neighbors")
        for label in labels:
            require_str(label, "read port label")
        if len(set(labels)) != len(labels):
            raise ValueError("read port labels must be unique")


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
    slots: tuple[str, ...]
    table: TableCarrier

    def __post_init__(self) -> None:
        require_str(self.site_type, "positional-case site type")
        slots = require_tuple(self.slots, "positional-case slot schema")
        if not slots:
            raise ValueError("positional-case slot schema must be nonempty")
        for slot in slots:
            require_str(slot, "positional-case slot")
        if len(set(slots)) != len(slots):
            raise ValueError("positional-case slots must be unique")
        if type(self.table) not in (DenseTable, DefaultOverridesTable):
            raise TypeError("positional-case table must be a closed table")

    @property
    def width(self) -> int:
        return len(self.slots)


@dataclass(frozen=True)
class PositionalRule:
    """Complete map over a declared semantic port-slot schema."""

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
        if not relation.ordered or relation.port_labels is None:
            raise ValueError("positional rules require explicitly labelled semantic slots")
        for site_index, site_type in enumerate(support.site_types):
            case = self.case_for(site_type)
            if len(relation.rows[site_index]) != case.width:
                raise ValueError("positional-rule width does not match typed incidence")
            labels = relation.port_labels[site_index]
            if len(labels) != case.width or set(labels) != set(case.slots):
                raise ValueError("positional relation labels do not match the declared slot schema")
        if set(support.site_types) != {case.site_type for case in self.cases}:
            raise ValueError("positional cases must exactly cover support site types")

    def evaluate(self, read: LocalRead) -> int:
        if read.center is not None or not read.ordered or read.port_labels is None:
            raise ValueError("positional rule requires labelled slots and no implicit Self")
        case = self.case_for(read.site_type)
        if len(read.neighbors) != case.width:
            raise ValueError("positional-rule read has the wrong width")
        if len(read.port_labels) != case.width or set(read.port_labels) != set(case.slots):
            raise ValueError("positional read labels do not match the declared slot schema")
        by_slot = dict(zip(read.port_labels, read.neighbors, strict=True))
        canonical = tuple(by_slot[slot] for slot in case.slots)
        return case.table.at(context_index(canonical, self.alphabet_size))


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


def offset_slot_schema(offsets: tuple[Offset, ...]) -> tuple[str, ...]:
    """Give each literal translation offset a stable semantic slot identity."""

    raw = require_tuple(offsets, "translation slot offsets")
    if not raw:
        raise ValueError("translation slot offsets must be nonempty")
    first = require_tuple(raw[0], "translation slot offset")
    checked = tuple(
        checked_coord(offset, len(first), "translation slot offset")
        for offset in raw
    )
    if len(set(checked)) != len(checked):
        raise ValueError("translation slot offsets must be unique")
    return tuple(
        "offset[" + ",".join(str(component) for component in offset) + "]"
        for offset in checked
    )


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

    def decode(self, raw_physical: object) -> Coord:
        """Invert ``embed`` exactly, rejecting points outside its lattice image."""

        physical = checked_coord(raw_physical, self.dimension, "physical lattice coordinate")
        determinant = bareiss_determinant(self.basis)
        coefficients: list[int] = []
        for replaced_column in range(self.dimension):
            cramer_matrix = tuple(
                tuple(
                    physical[row] if column == replaced_column else self.basis[row][column]
                    for column in range(self.dimension)
                )
                for row in range(self.dimension)
            )
            numerator = bareiss_determinant(cramer_matrix)
            if numerator % determinant:
                raise ValueError("physical coordinate is outside the declared lattice image")
            coefficients.append(numerator // determinant)
        result = tuple(coefficients)
        if self.embed(result) != physical:
            raise AssertionError("exact lattice inverse failed to reconstruct its input")
        return result


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
    if ordered:
        names = offset_slot_schema(checked) if port_names is None else require_tuple(port_names, "port names")
        if len(names) != len(checked):
            raise ValueError("port names do not match translation offsets")
        for name in names:
            require_str(name, "port name")
        if len(set(names)) != len(names):
            raise ValueError("translation port names must be unique")
        labels = tuple(tuple(names) for _ in coords)
    elif port_names is not None:
        raise ValueError("unlabelled translation incidence cannot declare port names")
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


def positional_program(
    alphabet_size: int,
    slots: tuple[str, ...],
    table: TableCarrier,
    relation: str = "local",
) -> SimpleProgram:
    k = require_int(alphabet_size, "alphabet size")
    case = PositionalCase("cell", slots, table)
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


# ---------------------------------------------------------------------------
# Source-schema and semantic proofs
# ---------------------------------------------------------------------------


def assert_source_schemas_and_codes() -> dict[str, int]:
    formula_checks = 0
    positional_formula_checks = 0
    for dimension in range(1, 7):
        axes = axis_offsets(dimension)
        full = full_shell_offsets(dimension)
        assert len(axes) == 2 * dimension
        assert len(full) == 3**dimension - 1
        assert axes == tuple(sorted(axes))
        assert full == tuple(sorted(full))
        for alphabet_size in (2, 3, 4):
            assert self_count_case_count(len(axes), alphabet_size) == (
                alphabet_size * (2 * dimension * (alphabet_size - 1) + 1)
            )
            assert self_count_case_count(len(full), alphabet_size) == (
                alphabet_size * ((3**dimension - 1) * (alphabet_size - 1) + 1)
            )
            formula_checks += 2

    assert axis_positions(1) == ((-1,), (0,), (1,))
    assert axis_positions(2) == ((-1, 0), (0, -1), (0, 0), (0, 1), (1, 0))
    for dimension in range(1, 6):
        for alphabet_size in (2, 3):
            positions = axis_positions(dimension)
            assert len(positions) == 2 * dimension + 1
            assert alphabet_size ** len(positions) == alphabet_size ** (2 * dimension + 1)
            positional_formula_checks += 1
        assert len(full_positions(dimension)) == 3**dimension
        positional_formula_checks += 1

    address_roundtrips = 0
    for alphabet_size in (2, 3):
        for width in range(1, 8):
            for index in range(alphabet_size**width):
                context = context_from_index(index, width, alphabet_size)
                assert context_index(context, alphabet_size) == index
                address_roundtrips += 1

    outer_code_cases = 0
    old_self_preservation_cases = 0
    for degree, code in ((3, 254), (5, 4094), (6, 16382)):
        rows = 2 * (degree + 1)
        table = binary_table_from_code(code, rows)
        assert binary_code_from_table(table) == code
        assert table.outputs == (0, *((1,) * (rows - 1)))
        for center in (0, 1):
            for neighbor_count in range(degree + 1):
                index = center + 2 * neighbor_count
                assert table.at(index) == int(center == 1 or neighbor_count > 0)
                outer_code_cases += 1
                if center == 1 and neighbor_count == 0:
                    assert table.at(index) == 1
                    old_self_preservation_cases += 1

    source_10926 = binary_table_from_code(10926, 14)
    assert binary_code_from_table(source_10926) == 10926
    assert source_10926.outputs == (0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1)
    for center in (0, 1):
        for neighbor_count in range(7):
            assert source_10926.at(center + 2 * neighbor_count) == int(
                center == 1 or neighbor_count == 1
            )

    # A full 4D 3^d positional map is finite (2^81 input rows for k=2)
    # without being eagerly materialized.  This is closed data, not a callback.
    huge_rows = 2 ** len(full_positions(4))
    huge = DefaultOverridesTable(2, huge_rows, 0, ((0, 1), (huge_rows - 1, 1)))
    assert huge.at(0) == huge.at(huge_rows - 1) == 1
    assert huge.at(1) == 0

    return {
        "formula_checks": formula_checks,
        "positional_formula_checks": positional_formula_checks,
        "mixed_radix_roundtrips": address_roundtrips,
        "outer_code_local_cases": outer_code_cases,
        "old_self_preservation_cases": old_self_preservation_cases,
        "closed_4d_positional_rows_exponent": len(full_positions(4)),
    }


def assert_translation_commutation() -> dict[str, int]:
    shapes: dict[int, tuple[int, ...]] = {
        1: (5,),
        2: (3, 4),
        3: (3, 2, 2),
        4: (2, 2, 2, 2),
        5: (2, 2, 2, 2, 2),
    }
    count_events = 0
    positional_events = 0
    large_positional_events = 0

    for dimension, shape in shapes.items():
        for profile_offsets in (axis_offsets(dimension), full_shell_offsets(dimension)):
            for alphabet_size in (2, 3):
                table = deterministic_table(
                    alphabet_size,
                    self_count_case_count(len(profile_offsets), alphabet_size),
                    dimension + len(profile_offsets),
                )
                program = count_program(alphabet_size, len(profile_offsets), table)
                for variant in range(4):
                    native = NativeTranslationState(
                        shape,
                        alphabet_size,
                        cells_pattern(prod(shape), alphabet_size, variant),
                        generation=variant,
                    )
                    expected = native_translation_count_step(native, profile_offsets, table)
                    generic = encode_translation(native, profile_offsets)
                    actual = decode_translation(generic_step(program, generic), shape)
                    assert actual == expected
                    count_events += 1

        positions = axis_positions(dimension)
        positional_table = deterministic_table(2, 2 ** len(positions), dimension)
        positional = positional_program(2, len(positions), positional_table)
        for variant in range(3):
            native = NativeTranslationState(
                shape,
                2,
                cells_pattern(prod(shape), 2, variant + 1),
                generation=9 + variant,
            )
            expected = native_translation_positional_step(native, positions, positional_table)
            generic = encode_translation(native, positions)
            actual = decode_translation(generic_step(positional, generic), shape)
            assert actual == expected
            positional_events += 1

    # Complete full positional maps use a closed sparse table representation.
    # The table remains total over every input row; only non-default rows are
    # stored explicitly.
    for dimension, shape, variant in ((3, (2, 2, 2), 2), (4, (1, 1, 1, 1), 1)):
        positions = full_positions(dimension)
        native = NativeTranslationState(
            shape,
            2,
            cells_pattern(prod(shape), 2, variant),
            generation=4,
        )
        reached = sorted(
            {
                context_index(
                    tuple(native.value_at(add_coord(coord, offset)) for offset in positions),
                    2,
                )
                for coord in all_coords(shape)
            }
        )
        table = DefaultOverridesTable(
            2,
            2 ** len(positions),
            0,
            tuple((index, 1) for index in reached),
        )
        program = positional_program(2, len(positions), table)
        expected = native_translation_positional_step(native, positions, table)
        actual = decode_translation(
            generic_step(program, encode_translation(native, positions)),
            shape,
        )
        assert actual == expected
        large_positional_events += 1

    coordinate_roundtrips = 0
    for dimension, shape in shapes.items():
        for index in range(prod(shape)):
            coord = coord_from_flat(shape, index)
            assert flat_index(shape, coord) == index
            coordinate_roundtrips += 1

    # Exact coefficient-basis representations for two common 3D witnesses.
    fcc_offsets = tuple(
        sorted(
            {
                offset
                for vector in (
                    (1, 0, 0),
                    (0, 1, 0),
                    (0, 0, 1),
                    (1, -1, 0),
                    (1, 0, -1),
                    (0, 1, -1),
                )
                for offset in (vector, tuple(-item for item in vector))
            }
        )
    )
    bcc_offsets = tuple(
        sorted(
            {
                offset
                for vector in (
                    (1, 0, 0),
                    (0, 1, 0),
                    (0, 0, 1),
                    (1, 1, 1),
                    (1, 1, 0),
                    (1, 0, 1),
                    (0, 1, 1),
                )
                for offset in (vector, tuple(-item for item in vector))
            }
        )
    )
    fcc = LatticeDescriptor(
        "fcc-coordinate-witness",
        ((0, 1, 1), (1, 0, 1), (1, 1, 0)),
        fcc_offsets,
    )
    bcc = LatticeDescriptor(
        "bcc-coordinate-witness",
        ((-1, 1, 1), (1, -1, 1), (1, 1, -1)),
        bcc_offsets,
    )
    assert len(fcc.offsets) == 12 and len(bcc.offsets) == 14
    assert bareiss_determinant(fcc.basis) != 0
    assert bareiss_determinant(bcc.basis) != 0
    embedded = 0
    basis_access_events = 0
    for descriptor in (fcc, bcc):
        images = {descriptor.embed(coord) for coord in product(range(-1, 2), repeat=3)}
        assert len(images) == 27
        embedded += len(images)
        table = deterministic_table(2, self_count_case_count(len(descriptor.offsets), 2), len(descriptor.offsets))
        program = count_program(2, len(descriptor.offsets), table)
        for variant in (1, 3):
            native = NativeTranslationState(
                (3, 3, 3),
                2,
                cells_pattern(27, 2, variant),
                generation=variant,
            )
            expected = native_translation_count_step(native, descriptor.offsets, table)
            actual = decode_translation(
                generic_step(program, encode_translation(native, descriptor.offsets)),
                native.shape,
            )
            assert actual == expected
            basis_access_events += 1

    return {
        "translation_count_events": count_events,
        "translation_positional_events": positional_events,
        "large_closed_positional_events": large_positional_events,
        "coordinate_roundtrips": coordinate_roundtrips,
        "basis_embedding_witnesses": embedded,
        "basis_access_events": basis_access_events,
    }


def assert_hexagonal_semantics() -> dict[str, int]:
    contexts = tuple(product((0, 1), repeat=7))
    rotations = orbit_partition(contexts, "rotation")
    dihedral = orbit_partition(contexts, "dihedral")
    assert len(rotations) == 28
    assert len(dihedral) == 26
    assert sum(len(orbit) for orbit in rotations) == 128
    assert sum(len(orbit) for orbit in dihedral) == 128

    rotation_outputs = tuple(index % 2 for index in range(len(rotations)))
    complete_rotation = expand_orbit_table(rotation_outputs, rotations)
    assert factor_orbit_table(complete_rotation, rotations) == rotation_outputs
    dihedral_outputs = tuple((index // 2) % 2 for index in range(len(dihedral)))
    complete_dihedral = expand_orbit_table(dihedral_outputs, dihedral)
    assert factor_orbit_table(complete_dihedral, dihedral) == dihedral_outputs

    # Directional projection is a complete map but is not rotationally
    # invariant; compact orbit data must reject it.
    directional = DenseTable(2, 128, tuple(context[1] for context in contexts))
    expect_raises(ValueError, lambda: factor_orbit_table(directional, rotations))

    outer_fiber_checks = 0
    for code in (16382, 10926):
        compact = binary_table_from_code(code, 14)
        complete = expand_self_count_table(6, compact)
        assert factor_self_count_table(6, complete) == compact
        for center in (0, 1):
            for count in range(7):
                fiber = tuple(
                    context
                    for context in contexts
                    if context[0] == center and sum(context[1:]) == count
                )
                assert len(fiber) == comb(6, count)
                values = {complete.at(context_index(context, 2)) for context in fiber}
                assert values == {compact.at(center + 2 * count)}
                outer_fiber_checks += len(fiber)

    totalistic_fibers = Counter(sum(context) for context in contexts)
    assert tuple(totalistic_fibers[count] for count in range(8)) == tuple(comb(7, count) for count in range(8))
    assert sum(totalistic_fibers.values()) == 128

    # Explicit group/action derivation of the source rule-space exponents.
    assert 2**128 == 2 ** len(contexts)  # complete positional maps
    assert 2**28 == 2 ** len(rotations)
    assert 2**26 == 2 ** len(dihedral)
    assert 2**14 == 2 ** (2 * 7)  # Self x six-neighbor count
    assert 2**8 == 2 ** (7 + 1)  # inclusive total count 0..7
    assert 2**7 == 2 ** 7  # growth: only white-center count cases are free

    codec_roundtrips = 0
    centers: set[Coord] = set()
    for address in product(range(-4, 5), repeat=2):
        center = HEX_CODEC.encode(address)
        assert HEX_CODEC.decode(center) == address
        centers.add(center)
        codec_roundtrips += 1
    assert len(centers) == codec_roundtrips
    displacements = tuple(HEX_CODEC.encode(offset) for offset in HEX_SQUARE_OFFSETS)
    assert len(set(displacements)) == 6
    assert all(HEX_CODEC.squared_scaled_distance(delta) == 4 for delta in displacements)
    expect_raises(ValueError, lambda: HEX_CODEC.decode((0, 1)))

    global_events = 0
    shape = (3, 3)
    for code in (16382, 10926):
        table = binary_table_from_code(code, 14)
        program = count_program(2, 6, table)
        for mask in range(1 << prod(shape)):
            cells = tuple((mask >> index) & 1 for index in range(prod(shape)))
            native = NativeTranslationState(shape, 2, cells, generation=2)
            expected = native_translation_count_step(native, HEX_SQUARE_OFFSETS, table)
            actual = decode_translation(
                generic_step(program, encode_translation(native, HEX_SQUARE_OFFSETS)),
                shape,
            )
            assert actual == expected
            global_events += 1

    return {
        "hex_rotation_orbits": len(rotations),
        "hex_dihedral_orbits": len(dihedral),
        "hex_outer_fiber_rows": outer_fiber_checks,
        "hex_totalistic_contexts": sum(totalistic_fibers.values()),
        "hex_codec_roundtrips": codec_roundtrips,
        "hex_native_generic_events": global_events,
        "hex_noninvariant_rejections": 1,
    }


def assert_fixed_incidence_semantics() -> dict[str, int]:
    degree_profile_events = 0
    named_degree_profiles = 0
    for _name, dimension, degree in SOURCE_NEAREST_DEGREES:
        assert dimension in (2, 3, 4)
        assert degree in (4, 6, 8, 12, 14, 16, 24)
        size = degree + 3 if (degree + 3) % 2 else degree + 4
        rows = circulant_rows(size, degree)
        assert all(len(row) == degree for row in rows)
        for salt in (1, 4):
            table = deterministic_table(2, self_count_case_count(degree, 2), salt)
            cases = (CountCase("cell", degree, table),)
            program = typed_count_program(2, cases)
            for variant in range(4):
                native = NativeIncidenceState(
                    tuple((index,) for index in range(size)),
                    ("cell",) * size,
                    rows,
                    False,
                    2,
                    cells_pattern(size, 2, variant),
                    generation=variant,
                )
                expected = native_count_step(native, cases)
                actual = decode_incidence(generic_step(program, encode_incidence(native)), native)
                assert actual == expected
                assert actual.rows == native.rows
                degree_profile_events += 1
        named_degree_profiles += 1
    assert named_degree_profiles == 10

    # Congruent pentagonal-cell profile: five incidences and complete code
    # 4094.  K6 is only a bounded degree-5 semantic fixture; it is not claimed
    # to be the Book plate's planar global topology.
    pentagonal_events = 0
    pentagonal_rows = tuple(
        tuple(target for target in range(6) if target != site)
        for site in range(6)
    )
    pentagonal_table = binary_table_from_code(4094, 12)
    pentagonal_cases = (CountCase("pentagon", 5, pentagonal_table),)
    pentagonal_program = typed_count_program(2, pentagonal_cases)
    for mask in range(64):
        cells = tuple((mask >> index) & 1 for index in range(6))
        native = NativeIncidenceState(
            tuple((index,) for index in range(6)),
            ("pentagon",) * 6,
            pentagonal_rows,
            False,
            2,
            cells,
        )
        expected = native_count_step(native, pentagonal_cases)
        actual = decode_incidence(generic_step(pentagonal_program, encode_incidence(native)), native)
        assert actual == expected
        pentagonal_events += 1

    # Two source tile shapes treated by the same degree-3 code 254 table.
    # K3,3 proves the typed/same-rule invariant without pretending to replay a
    # Penrose patch not specified as coordinates in the prose.
    two_shape_events = 0
    two_shape_rows = complete_bipartite_rows(3, 3)
    code254 = binary_table_from_code(254, 8)
    two_shape_cases = (
        CountCase("shape-A", 3, code254),
        CountCase("shape-B", 3, code254),
    )
    two_shape_program = typed_count_program(2, two_shape_cases)
    for mask in range(64):
        cells = tuple((mask >> index) & 1 for index in range(6))
        native = NativeIncidenceState(
            tuple((index,) for index in range(6)),
            ("shape-A",) * 3 + ("shape-B",) * 3,
            two_shape_rows,
            False,
            2,
            cells,
        )
        expected = native_count_step(native, two_shape_cases)
        actual = decode_incidence(generic_step(two_shape_program, encode_incidence(native)), native)
        assert actual == expected
        two_shape_events += 1

    # A triangle tiling has two cell orientations.  Its incidence is fixed but
    # site-conditioned; the same code 254 applies to both types.
    alternating_events = 0
    alternating_cases = (
        CountCase("up", 3, code254),
        CountCase("down", 3, code254),
    )
    alternating_program = typed_count_program(2, alternating_cases)
    for mask in range(256):
        cells = tuple((mask >> index) & 1 for index in range(8))
        native = triangular_tile_state((2, 2), cells)
        expected = native_count_step(native, alternating_cases)
        actual = decode_incidence(generic_step(alternating_program, encode_incidence(native)), native)
        assert actual == expected
        alternating_events += 1

    # Concrete failure of one global static Cartesian offset list over
    # (row,column,orientation).  Even if orientation is reduced mod 2, the
    # row/column signs disagree on a quotient with extent > 2.
    up_offsets = ((0, 0, 1), (-1, 0, 1), (0, -1, 1))
    down_offsets = ((0, 0, -1), (1, 0, -1), (0, 1, -1))
    assert set(up_offsets) != set(down_offsets)
    down_site = (2, 2, 1)
    wrong_from_global_up = ((down_site[0] - 1) % 5, down_site[1], 0)
    required_from_down = ((down_site[0] + 1) % 5, down_site[1], 0)
    assert wrong_from_global_up == (1, 2, 0)
    assert required_from_down == (3, 2, 0)
    assert wrong_from_global_up != required_from_down

    # A fixed finite-type network may give each type its own incidence degree
    # and complete count table while using the same runner and UPDATE.
    finite_type_events = 0
    finite_type_rows = complete_bipartite_rows(2, 3)
    high_table = deterministic_table(2, 8, 1)  # degree 3
    low_table = deterministic_table(2, 6, 0)  # degree 2
    finite_type_cases = (
        CountCase("degree-3", 3, high_table),
        CountCase("degree-2", 2, low_table),
    )
    finite_type_program = typed_count_program(2, finite_type_cases)
    for mask in range(32):
        cells = tuple((mask >> index) & 1 for index in range(5))
        native = NativeIncidenceState(
            tuple((index,) for index in range(5)),
            ("degree-3",) * 2 + ("degree-2",) * 3,
            finite_type_rows,
            False,
            2,
            cells,
        )
        expected = native_count_step(native, finite_type_cases)
        actual = decode_incidence(generic_step(finite_type_program, encode_incidence(native)), native)
        assert actual == expected
        finite_type_events += 1

    # Unlabelled ports may be stored in any row order, but only a
    # permutation-invariant rule can consume them.
    local_permutation_checks = 0
    degree3_case = CountCase("cell", 3, code254)
    degree3_rule = SelfCountRule(2, (degree3_case,))
    for context in product((0, 1), repeat=4):
        center, neighbors = context[0], context[1:]
        expected = degree3_rule.evaluate(LocalRead(0, "cell", center, neighbors, False, None))
        for permuted in permutations(neighbors):
            actual = degree3_rule.evaluate(LocalRead(0, "cell", center, permuted, False, None))
            assert actual == expected
            local_permutation_checks += 1

    unlabelled_global_events = 0
    k4_rows = tuple(tuple(target for target in range(4) if target != site) for site in range(4))
    reversed_rows = tuple(tuple(reversed(row)) for row in k4_rows)
    unlabelled_program = typed_count_program(2, (degree3_case,))
    for mask in range(16):
        cells = tuple((mask >> index) & 1 for index in range(4))
        first = NativeIncidenceState(
            tuple((index,) for index in range(4)),
            ("cell",) * 4,
            k4_rows,
            False,
            2,
            cells,
        )
        second = NativeIncidenceState(
            first.keys,
            first.site_types,
            reversed_rows,
            False,
            2,
            cells,
        )
        next_first = generic_step(unlabelled_program, encode_incidence(first))
        next_second = generic_step(unlabelled_program, encode_incidence(second))
        assert decode_incidence(next_first, first) == native_count_step(first, (degree3_case,))
        assert decode_incidence(next_second, second) == native_count_step(second, (degree3_case,))
        assert next_first.cells == next_second.cells
        unlabelled_global_events += 2

    projection_table = DenseTable(2, 8, tuple(context[0] for context in product((0, 1), repeat=3)))
    positional_case = PositionalCase("cell", 3, projection_table)
    positional_on_unlabelled = typed_positional_program(2, (positional_case,))
    unlabelled_fixture = NativeIncidenceState(
        tuple((index,) for index in range(4)),
        ("cell",) * 4,
        k4_rows,
        False,
        2,
        (1, 0, 0, 0),
    )
    expect_raises(
        ValueError,
        lambda: generic_step(positional_on_unlabelled, encode_incidence(unlabelled_fixture)),
    )

    # Labelled ports make ordered positional data meaningful.  A closed table
    # projects the left port; reversing the rows without permuting the rule is
    # observably different, as it should be.
    labelled_events = 0
    cycle_size = 5
    labelled_rows = tuple(((site - 1) % cycle_size, (site + 1) % cycle_size) for site in range(cycle_size))
    labelled_port_rows = tuple(("left", "right") for _ in range(cycle_size))
    left_projection = DenseTable(2, 4, (0, 0, 1, 1))
    labelled_case = PositionalCase("cell", 2, left_projection)
    labelled_program = typed_positional_program(2, (labelled_case,))
    labelled_witness_outputs: tuple[Cells, Cells] | None = None
    for mask in range(32):
        cells = tuple((mask >> index) & 1 for index in range(cycle_size))
        native = NativeIncidenceState(
            tuple((index,) for index in range(cycle_size)),
            ("cell",) * cycle_size,
            labelled_rows,
            True,
            2,
            cells,
            port_labels=labelled_port_rows,
        )
        expected = native_positional_step(native, (labelled_case,))
        actual = decode_incidence(generic_step(labelled_program, encode_incidence(native)), native)
        assert actual == expected
        labelled_events += 1
        reversed_native = NativeIncidenceState(
            native.keys,
            native.site_types,
            tuple(tuple(reversed(row)) for row in native.rows),
            True,
            2,
            cells,
            port_labels=tuple(("right", "left") for _ in range(cycle_size)),
        )
        reversed_output = native_positional_step(reversed_native, (labelled_case,)).cells
        if expected.cells != reversed_output and labelled_witness_outputs is None:
            labelled_witness_outputs = (expected.cells, reversed_output)
    assert labelled_witness_outputs is not None

    return {
        "source_degree_profiles": named_degree_profiles,
        "degree_profile_events": degree_profile_events,
        "pentagonal_code4094_events": pentagonal_events,
        "two_shape_code254_events": two_shape_events,
        "alternating_orientation_events": alternating_events,
        "finite_type_network_events": finite_type_events,
        "unlabelled_local_permutation_checks": local_permutation_checks,
        "unlabelled_global_events": unlabelled_global_events,
        "labelled_positional_events": labelled_events,
        "unlabelled_positional_rejections": 1,
        "static_offset_failure_witnesses": 1,
    }


def assert_alias_multiplicity_and_parallel_update() -> dict[str, int]:
    alias_events = 0

    # On the 1^4 quotient, eight distinct axial offsets all address the one
    # stored site.  Occurrence multiplicity gives sum=8, not deduplicated sum=1.
    axes4 = axis_offsets(4)
    one = NativeTranslationState((1, 1, 1, 1), 2, (1,))
    rows = self_count_case_count(8, 2)
    distinguishing = DefaultOverridesTable(2, rows, 0, ((17, 1),))
    encoded = encode_translation(one, axes4)
    relation = encoded.support.relation("local")
    assert len(relation.rows[0]) == 8 and len(set(relation.rows[0])) == 1
    expected = native_translation_count_step(one, axes4, distinguishing)
    actual = decode_translation(generic_step(count_program(2, 8, distinguishing), encoded), one.shape)
    assert expected.cells == actual.cells == (1,)
    assert distinguishing.at(3) == 0  # the incorrect deduplicated address
    alias_events += 1

    # Full 2D access on 2x2 has three targets with multiplicities 4,2,2.
    square = NativeTranslationState((2, 2), 2, (1, 0, 0, 0))
    full2 = full_shell_offsets(2)
    square_generic = encode_translation(square, full2)
    first_row_counts = sorted(Counter(square_generic.support.relation("local").rows[0]).values())
    assert first_row_counts == [2, 2, 4]
    square_table = deterministic_table(2, self_count_case_count(8, 2), 1)
    assert decode_translation(
        generic_step(count_program(2, 8, square_table), square_generic),
        square.shape,
    ) == native_translation_count_step(square, full2, square_table)
    alias_events += 1

    # Three parallel ports to the same peer remain three occurrences.
    parallel_rows = ((1, 1, 1), (0, 0, 0))
    parallel = NativeIncidenceState(
        ((0,), (1,)),
        ("cell", "cell"),
        parallel_rows,
        False,
        2,
        (0, 1),
    )
    port_table = DefaultOverridesTable(2, 8, 0, ((6, 1),))
    port_case = CountCase("cell", 3, port_table)
    parallel_next = generic_step(typed_count_program(2, (port_case,)), encode_incidence(parallel))
    assert parallel_next.cells[0] == 1
    assert port_table.at(2) == 0  # the incorrect set-valued/deduplicated address
    assert decode_incidence(parallel_next, parallel) == native_count_step(parallel, (port_case,))
    alias_events += 1

    # Snapshot-parallel evaluation differs from an in-place site-order loop.
    predecessor_rows = ((2,), (0,), (1,))
    labels = (("predecessor",),) * 3
    old = NativeIncidenceState(
        ((0,), (1,), (2,)),
        ("cell",) * 3,
        predecessor_rows,
        True,
        2,
        (1, 0, 0),
        port_labels=labels,
    )
    identity = DenseTable(2, 2, (0, 1))
    case = PositionalCase("cell", 1, identity)
    expected = native_positional_step(old, (case,))
    old_generic = encode_incidence(old)
    actual_generic = generic_step(typed_positional_program(2, (case,)), old_generic)
    actual = decode_incidence(actual_generic, old)
    assert actual == expected
    assert actual.cells == (0, 1, 0)
    in_place = list(old.cells)
    for site, row in enumerate(old.rows):
        in_place[site] = in_place[row[0]]
    assert tuple(in_place) == (0, 0, 0)
    assert tuple(in_place) != actual.cells
    assert actual_generic.support is old_generic.support

    return {
        "alias_multiplicity_events": alias_events,
        "old_snapshot_events": 1,
        "in_place_disagreement_witnesses": 1,
    }


RUNTIME_GAP_MATRIX: tuple[tuple[str, str, str], ...] = (
    (
        "src/ca/alphabets.py",
        "direct reuse for strict T24",
        "boolean/int-range/symbolic finite scalar labels suffice; broader product/tagged alphabets remain a separate Goal2 gap",
    ),
    (
        "src/ca/loci.py",
        "parameterization gap",
        "canonical coordinates are hard-limited to [t,x,y,z] and spatial rank 0..3",
    ),
    (
        "src/ca/neighborhoods.py",
        "partial reuse/gap",
        "literal and metric selectors work through rank 3; no arbitrary-d coefficient offsets or typed fixed-incidence relation",
    ),
    (
        "src/ca/frontiers.py",
        "semantic reuse/realization gap",
        "time_slice is AllSites for dense rank<=3 tensors; fixed-incidence supports are not exposed",
    ),
    (
        "src/ca/rules.py",
        "schema gap",
        "no closed arbitrary-d count/positional tables, typed site cases, or labelled-port schemas",
    ),
    (
        "src/ca/rollout.py",
        "implementation gap",
        "evaluation branches on named families and dense numpy rank instead of applying a closed typed RULE to a support relation",
    ),
    (
        "src/ca/rollout.py:_normalize_rule_ids",
        "representation gap",
        "numpy int64 coercion cannot carry arbitrary-precision finite rule codes",
    ),
    (
        "src/ca/specs.py + datasets.py",
        "manifest gap",
        "Phase-1 family dispatch has no dimension/basis/incidence/access/table descriptors",
    ),
    (
        "src/ca/viz",
        "observer",
        "rank-3 coordinates, projections, palettes, and distorted centers are views, never topology or RULE identity",
    ),
)


DECISION_MATRIX: tuple[tuple[str, str, str, str], ...] = (
    (
        "DOMAIN",
        "parameterization",
        "DiscreteSpace(dimension=d)",
        "arbitrary finite d is dimensional task space, not a HigherDimensionalCA class",
    ),
    (
        "CONFIGURATION",
        "parameterization/lossless representation",
        "FixedSupport(FiniteAlphabet,TopologyOrIncidence)",
        "Z^d coefficients, finite quotients, and literal fixed incidence preserve complete label state and topology",
    ),
    (
        "ALPHABET",
        "direct reuse",
        "FiniteAlphabet",
        "binary and finite-k source profiles need no lattice-named alphabet",
    ),
    (
        "FRONTIER",
        "direct reuse",
        "AllSites",
        "every fixed-support site fires once",
    ),
    (
        "NEIGHBORHOOD",
        "parameterization/lossless representation",
        "OrderedOffsets | TypedIncidence | LabelledPorts",
        "occurrence multiplicity, site type, and port labels are explicit access data",
    ),
    (
        "RULE",
        "restriction/lossless representation",
        "ClosedTable(Positional | SelfXCount | OrbitFactor)",
        "compact tables factor complete maps only on certified constant fibers",
    ),
    (
        "UPDATE",
        "direct reuse",
        "SnapshotParallelSameSite",
        "strict T24 changes labels only and preserves support/incidence",
    ),
    (
        "REALIZATION/VIEW",
        "parameterization/observer",
        "FiniteQuotient + BasisCodec + Projection",
        "quotients preserve access occurrences; embeddings and displayed centers do not drive evolution",
    ),
)


def assert_architecture_and_structural_control() -> dict[str, int]:
    assert tuple(row[0] for row in DECISION_MATRIX) == (
        "DOMAIN",
        "CONFIGURATION",
        "ALPHABET",
        "FRONTIER",
        "NEIGHBORHOOD",
        "RULE",
        "UPDATE",
        "REALIZATION/VIEW",
    )
    assert DECISION_MATRIX[6][1] == "direct reuse"
    assert all("executor" not in row[2].lower() for row in DECISION_MATRIX)
    assert len(RUNTIME_GAP_MATRIX) == 9
    assert sum("gap" in row[1] for row in RUNTIME_GAP_MATRIX) == 7
    assert any(row[1] == "observer" for row in RUNTIME_GAP_MATRIX)

    # Concrete category-4 control: structural node creation cannot be the
    # result of same-site label assignments because that UPDATE preserves the
    # support object and site cardinality.  This is routed to the already
    # evidenced graph-write axis (T29), not made a T24 executor.
    old_rows = ((1, 2), (0, 2), (0, 1))
    old = NativeIncidenceState(
        ((0,), (1,), (2,)),
        ("cell",) * 3,
        old_rows,
        False,
        2,
        (1, 0, 0),
    )
    table = deterministic_table(2, self_count_case_count(2, 2), 1)
    case = CountCase("cell", 2, table)
    label_successor = generic_step(typed_count_program(2, (case,)), encode_incidence(old))
    assert label_successor.support.keys == old.keys
    assert len(label_successor.support.keys) == 3
    native_structural_keys = (*old.keys, (3,))
    native_structural_rows = ((1, 2, 3), (0, 2), (0, 1), (0,))
    assert len(native_structural_keys) == 4
    assert native_structural_rows != old.rows
    assert len(native_structural_keys) != len(label_successor.support.keys)

    return {
        "audit_category_1_to_3_rows": len(DECISION_MATRIX),
        "structural_graph_counterexamples": 1,
        "new_strict_t24_update_algebras": 0,
    }


def assert_hostile_validation() -> dict[str, int]:
    rejection_count = 0

    def rejects(error: type[BaseException], action: object) -> None:
        nonlocal rejection_count
        expect_raises(error, action)
        rejection_count += 1

    rejects(TypeError, lambda: FiniteAlphabet(True))
    rejects(ValueError, lambda: FiniteAlphabet(1))
    rejects(TypeError, lambda: DenseTable(2, 2, [0, 1]))
    rejects(ValueError, lambda: DenseTable(2, 2, (0,)))
    rejects(ValueError, lambda: DenseTable(2, 2, (0, 2)))
    rejects(ValueError, lambda: DefaultOverridesTable(2, 4, 0, ((2, 1), (2, 0))))
    rejects(ValueError, lambda: DefaultOverridesTable(2, 4, 0, ((4, 1),)))
    rejects(TypeError, lambda: validate_closed_table(lambda index: 0, 2, 4))
    rejects(ValueError, lambda: axis_offsets(0))
    rejects(ValueError, lambda: full_shell_offsets(-1))
    rejects(TypeError, lambda: checked_shape([2, 2]))
    rejects(ValueError, lambda: coord_from_flat((2, 2), 4))
    rejects(ValueError, lambda: context_from_index(8, 3, 2))
    rejects(ValueError, lambda: LatticeDescriptor("singular", ((1, 1), (1, 1)), ((1, 0),)))
    rejects(ValueError, lambda: LatticeDescriptor("duplicate", identity_basis(2), ((1, 0), (1, 0))))
    rejects(ValueError, lambda: IncidenceRelation("bad", ((0,),), False, (("port",),)))
    rejects(ValueError, lambda: IncidenceRelation("bad", ((0, 0),), True, (("x", "x"),)))
    rejects(
        ValueError,
        lambda: FixedSupport(((0,),), ("cell",), (IncidenceRelation("x", ((1,),), False),)),
    )
    rejects(
        ValueError,
        lambda: FixedSupport(
            ((0,),),
            ("cell",),
            (IncidenceRelation("x", ((0,),), False), IncidenceRelation("x", ((0,),), False)),
        ),
    )
    rejects(ValueError, lambda: SnapshotToken(-1))
    rejects(TypeError, lambda: SnapshotToken(False))
    rejects(ValueError, lambda: CountCase("cell", -1, DenseTable(2, 2, (0, 1))))
    rejects(
        ValueError,
        lambda: SelfCountRule(2, (CountCase("cell", 2, DenseTable(2, 5, (0,) * 5)),)),
    )
    rejects(
        ValueError,
        lambda: PositionalRule(2, (PositionalCase("cell", 2, DenseTable(2, 3, (0,) * 3)),)),
    )
    rejects(ValueError, lambda: HEX_CODEC.decode((1, 0)))
    rejects(ValueError, lambda: orbit_partition(tuple(product((0, 1), repeat=7)), "bad"))

    fixture = NativeIncidenceState(
        ((0,), (1,)),
        ("cell", "cell"),
        ((1,), (0,)),
        False,
        2,
        (1, 0),
    )
    generic = encode_incidence(fixture)
    table = deterministic_table(2, 4, 1)
    rule = SelfCountRule(2, (CountCase("cell", 1, table),))
    program = typed_count_program(2, rule.cases)
    active = select_all_sites(generic, program.frontier)
    reads = read_neighborhood(generic, active, program.neighborhood)
    writes = make_assignments(generic, program, active, reads)
    peer = encode_incidence(fixture)
    foreign = (SiteHandle(peer.snapshot_token, 0), active[1])
    rejects(ValueError, lambda: read_neighborhood(generic, foreign, program.neighborhood))
    rejects(ValueError, lambda: read_neighborhood(generic, (active[0], active[0]), program.neighborhood))
    rejects(
        ValueError,
        lambda: apply_parallel(
            generic,
            active,
            (SiteAssignment(writes[0].source, 1, writes[0].value), writes[1]),
        ),
    )
    successor = apply_parallel(generic, active, writes)
    rejects(ValueError, lambda: read_neighborhood(successor, active, program.neighborhood))

    # Wrong type-conditioned arity is rejected before any rule evaluation.
    wrong_case = CountCase("cell", 2, deterministic_table(2, 6, 0))
    rejects(
        ValueError,
        lambda: generic_step(typed_count_program(2, (wrong_case,)), generic),
    )

    return {"hostile_rejections": rejection_count}


def semantic_digest(counts: dict[str, int]) -> str:
    transcript = "\n".join(f"{key}={counts[key]}" for key in sorted(counts))
    return sha256(transcript.encode("utf-8")).hexdigest()


EXPECTED_SEMANTIC_DIGEST = "df6481886ae13040679ea00f005ce58b5382452bfc3ed72e7b59dcc25b8aa2f4"


def main() -> None:
    groups = {
        "source": assert_source_schemas_and_codes(),
        "translation": assert_translation_commutation(),
        "hex": assert_hexagonal_semantics(),
        "incidence": assert_fixed_incidence_semantics(),
        "update": assert_alias_multiplicity_and_parallel_update(),
        "architecture": assert_architecture_and_structural_control(),
        "hostile": assert_hostile_validation(),
    }
    counts = {
        f"{group}.{key}": value
        for group, values in groups.items()
        for key, value in values.items()
    }
    native_generic_events = sum(
        value
        for key, value in counts.items()
        if key.endswith("_events") and "in_place" not in key
    )
    counts["total.native_generic_events"] = native_generic_events
    digest = semantic_digest(counts)
    if EXPECTED_SEMANTIC_DIGEST != "TO_BE_FROZEN_AFTER_FIRST_PASS":
        assert digest == EXPECTED_SEMANTIC_DIGEST

    print("T24 semantic oracle: PASS")
    print(f"native_generic_events={native_generic_events}")
    print(
        "event_partition="
        f"translation_count:{groups['translation']['translation_count_events']},"
        f"translation_positional:{groups['translation']['translation_positional_events']},"
        f"large_closed_positional:{groups['translation']['large_closed_positional_events']},"
        f"basis_access:{groups['translation']['basis_access_events']},"
        f"hex:{groups['hex']['hex_native_generic_events']},"
        f"declared_degree:{groups['incidence']['degree_profile_events']},"
        f"pentagonal:{groups['incidence']['pentagonal_code4094_events']},"
        f"two_shape:{groups['incidence']['two_shape_code254_events']},"
        f"alternating_orientation:{groups['incidence']['alternating_orientation_events']},"
        f"finite_type_network:{groups['incidence']['finite_type_network_events']},"
        f"unlabelled_global:{groups['incidence']['unlabelled_global_events']},"
        f"labelled_positional:{groups['incidence']['labelled_positional_events']},"
        f"alias:{groups['update']['alias_multiplicity_events']},"
        f"old_snapshot:{groups['update']['old_snapshot_events']}"
    )
    print(
        "arbitrary_d_formulas="
        "axes_degree=2d,axes_cases=k*(2d*(k-1)+1);"
        "full_degree=3^d-1,full_cases=k*((3^d-1)*(k-1)+1);"
        "positional_rows=k^s,positional_rule_count=k^(k^s);"
        f"checks:{groups['source']['formula_checks'] + groups['source']['positional_formula_checks']}"
    )
    print(
        "closed_rule_data="
        "DenseTable|DefaultOverridesTable; callbacks=NONE;"
        "4D_full_width=81,rows=2^81; eager_materialization=NOT_REQUIRED"
    )
    print(
        "hex_rule_spaces="
        "general:2^128,rotation:2^28,dihedral_complete:2^26,"
        "outer:2^14,totalistic:2^8,growth:2^7;"
        f"explicit_orbits:{groups['hex']['hex_rotation_orbits']}/"
        f"{groups['hex']['hex_dihedral_orbits']};"
        f"fiber_rows:{groups['hex']['hex_outer_fiber_rows']}"
    )
    print(
        "hex_codec=(row,column)->(row,2*column-row);inverse=PASS;"
        "six_access_displacements_have_scaled_distance_squared_4;"
        "sqrt3_center_embedding=VIEW_ONLY"
    )
    print(
        "source_outer_codes="
        "degree3:254,degree5:4094,degree6:16382 all equal complete growth OR tables;"
        "old_Self_preserved_at_neighbor_count0;"
        "degree6_code10926=old_Self_persistence_OR_exactly_one_neighbor_birth"
    )
    print(
        "fixed_incidence="
        f"source_degree_profiles:{groups['incidence']['source_degree_profiles']};"
        "Book_degree_only_entries_do_not_invent_global_topology;"
        "typed/site-conditioned_access=PASS; fixed_topology=PASS"
    )
    print(
        "unlabelled_incidence="
        f"permutation_checks:{groups['incidence']['unlabelled_local_permutation_checks']};"
        "count_rule_invariant=PASS; positional_rule_rejected=PASS;"
        "labelled_ports_positional=PASS"
    )
    print(
        "alternating_orientation_static_offset_counterexample="
        "global_up_offset(-1,0,+1)@down(2,2,1)->(1,2,0),"
        "native_down_neighbor=(3,2,0); typed_incidence_repairs_without_new_UPDATE"
    )
    print(
        "occurrence_multiplicity="
        "1^4_axes:eight_aliases_not_one;2x2_full:multiplicities[2,2,4];"
        "parallel_ports:three_aliases_not_one; PASS"
    )
    print("old_snapshot_parallelism=PASS; same_site_atomic_commit=PASS; in_place_witness=PASS")
    print(
        "runtime_audit="
        "scalar_alphabet+selector concepts+AllSites+same-site kernel reusable;"
        "gaps=rank<=3,typed_incidence,closed_schema_tables,bigint_ids,family_dispatch;"
        "views_are_observers"
    )
    print(
        "classification=categories1_to_3_for_all_strict_T24_profiles;"
        "new_T24_UPDATE=NONE;new_executor=NONE;"
        "structural_node_creation_is_concrete_nonfit_routed_to_existing_graph-write_axis"
    )
    print(f"hostile_rejections={groups['hostile']['hostile_rejections']}")
    print(f"semantic_digest={digest}")


if __name__ == "__main__":
    main()
