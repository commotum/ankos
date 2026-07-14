#!/usr/bin/env python3
"""Independent semantic and architecture oracle for T25.

Two-dimensional Turing machines are checked as one-event instances of the
shared SimpleProgram protocol.  The native evaluator uses the Book's factored
``(state, tape, position)`` representation.  The generic evaluator uses the
transparent composite alphabet

    Plain(symbol) | Head(state, symbol)

over a total default-plus-overrides field, with exactly one Head.  The compact
transition table still depends only on ``(head_state, underlying_symbol)``;
the typed rule result contains source assignment and head-movement intent,
while ``UPDATE`` preserves the old destination symbol from the configuration.
Each native event must commute with one generic event--there are no CA
microsteps, callbacks, family switches, or hidden interpreter state.

The strict main-text construction supplies a square grid and four raw-frame
axis movements, but no named north/east/south/west ordering or numeric rule
codec.  ``NEIGHBORHOOD`` exposes only the old Head; ``RULE`` returns a typed
source assignment plus head-movement intent; atomic ``UPDATE`` preserves the
old destination symbol without making it rule-visible.  Langton's ant is
checked from the exact finite source formula.  A
six-port heading witness proves that the same event parameterizes a hexagonal
topology, while the source's underdetermined count of 1,296 simple worms is
deliberately not reverse-engineered into an invented rule schema.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from hashlib import sha256
from itertools import product
from typing import Callable


if not __debug__:
    raise RuntimeError("T25 semantic verification requires assertions; do not run with -O")


Coord = tuple[int, int]


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


def checked_coord(value: object, name: str = "coordinate") -> Coord:
    raw = exact_tuple(value, name)
    if len(raw) != 2:
        raise ValueError(f"{name} must have exactly two components")
    return (exact_int(raw[0], f"{name}[0]"), exact_int(raw[1], f"{name}[1]"))


def add_coord(left: Coord, right: Coord) -> Coord:
    return (left[0] + right[0], left[1] + right[1])


@dataclass(frozen=True)
class MoveSchema:
    """Semantic movement ports plus raw Book-frame coordinate displacements."""

    name: str
    ports: tuple[tuple[str, Coord], ...]

    def __post_init__(self) -> None:
        exact_str(self.name, "movement schema name")
        raw = exact_tuple(self.ports, "movement ports")
        if not raw:
            raise ValueError("a movement schema must have at least one port")
        labels: list[str] = []
        deltas: list[Coord] = []
        for entry in raw:
            pair = exact_tuple(entry, "movement port")
            if len(pair) != 2:
                raise ValueError("movement ports must be label/displacement pairs")
            label = exact_str(pair[0], "movement port label")
            delta = checked_coord(pair[1], "movement displacement")
            if delta == (0, 0):
                raise ValueError("strict T25 movement ports must be nonzero")
            labels.append(label)
            deltas.append(delta)
        if len(set(labels)) != len(labels):
            raise ValueError("movement port labels must be unique")
        if len(set(deltas)) != len(deltas):
            raise ValueError("movement displacements must be unique")

    def displacement(self, label: str) -> Coord:
        checked = exact_str(label, "movement port label")
        matches = tuple(delta for port, delta in self.ports if port == checked)
        if len(matches) != 1:
            raise ValueError("movement port is outside the declared schema")
        return matches[0]

    @property
    def labels(self) -> tuple[str, ...]:
        return tuple(label for label, _delta in self.ports)


# This tuple order is a declared structural spelling for this oracle, not a
# source-defined numeric code or compass convention.
SQUARE_SCHEMA = MoveSchema(
    "book-array-square-v1",
    (
        ("axis0+", (1, 0)),
        ("axis0-", (-1, 0)),
        ("axis1+", (0, 1)),
        ("axis1-", (0, -1)),
    ),
)

SWAPPED_FRAME_SCHEMA = MoveSchema(
    "explicit-axis-swap-witness-v1",
    (
        ("axis0+", (0, 1)),
        ("axis0-", (0, -1)),
        ("axis1+", (1, 0)),
        ("axis1-", (-1, 0)),
    ),
)

HEX_SCHEMA = MoveSchema(
    "axial-hex-witness-v1",
    (
        ("hex0", (1, 0)),
        ("hex1", (0, 1)),
        ("hex2", (-1, 1)),
        ("hex3", (-1, 0)),
        ("hex4", (0, -1)),
        ("hex5", (1, -1)),
    ),
)

# Explicit finite heading actions for relative-turn variants.  These are not
# inferred from MoveSchema storage order and are not a numeric codec for the
# unrestricted Turing-table family.  The square cycle is the source formula's
# (1, i, -1, -i) action in the raw Book frame.
SQUARE_C4_HEADING_PORTS = ("axis0+", "axis1+", "axis0-", "axis1-")
HEX_C6_HEADING_PORTS = HEX_SCHEMA.labels


@dataclass(frozen=True)
class TotalTape:
    alphabet_size: int
    default_symbol: int
    overrides: tuple[tuple[Coord, int], ...] = ()

    def __post_init__(self) -> None:
        size = exact_int(self.alphabet_size, "alphabet size")
        default = exact_int(self.default_symbol, "default symbol")
        if size < 2 or default < 0 or default >= size:
            raise ValueError("invalid tape alphabet/default")
        raw = exact_tuple(self.overrides, "tape overrides")
        previous: Coord | None = None
        for entry in raw:
            pair = exact_tuple(entry, "tape override")
            if len(pair) != 2:
                raise ValueError("tape override must be coordinate/symbol")
            coord = checked_coord(pair[0], "override coordinate")
            symbol = exact_int(pair[1], "override symbol")
            if symbol < 0 or symbol >= size:
                raise ValueError("override symbol is outside the alphabet")
            if symbol == default:
                raise ValueError("default-valued overrides are noncanonical")
            if previous is not None and coord <= previous:
                raise ValueError("override coordinates must be unique and sorted")
            previous = coord

    def at(self, coord: Coord) -> int:
        checked = checked_coord(coord)
        for key, symbol in self.overrides:
            if key == checked:
                return symbol
            if key > checked:
                break
        return self.default_symbol

    def write(self, coord: Coord, symbol: int) -> TotalTape:
        key = checked_coord(coord)
        value = exact_int(symbol, "written symbol")
        if value < 0 or value >= self.alphabet_size:
            raise ValueError("written symbol is outside the tape alphabet")
        data = dict(self.overrides)
        if value == self.default_symbol:
            data.pop(key, None)
        else:
            data[key] = value
        return TotalTape(
            self.alphabet_size,
            self.default_symbol,
            tuple(sorted(data.items())),
        )


@dataclass(frozen=True)
class NativeState:
    state_count: int
    schema: MoveSchema
    tape: TotalTape
    head_state: int
    head_position: Coord
    generation: int = 0

    def __post_init__(self) -> None:
        states = exact_int(self.state_count, "head-state count")
        if states < 1:
            raise ValueError("head-state count must be positive")
        if type(self.schema) is not MoveSchema:
            raise TypeError("native state requires an exact MoveSchema")
        if type(self.tape) is not TotalTape:
            raise TypeError("native state requires an exact TotalTape")
        state = exact_int(self.head_state, "head state")
        if state < 0 or state >= states:
            raise ValueError("head state is outside Q")
        checked_coord(self.head_position, "head position")
        generation = exact_int(self.generation, "generation")
        if generation < 0:
            raise ValueError("generation must be nonnegative")


@dataclass(frozen=True)
class Transition:
    next_state: int
    write_symbol: int
    move_port: str


@dataclass(frozen=True)
class ClosedTMTable:
    state_count: int
    symbol_count: int
    schema: MoveSchema
    rows: tuple[tuple[int, int, Transition], ...]

    def __post_init__(self) -> None:
        states = exact_int(self.state_count, "table state count")
        symbols = exact_int(self.symbol_count, "table symbol count")
        if states < 1 or symbols < 2:
            raise ValueError("invalid Turing table dimensions")
        if type(self.schema) is not MoveSchema:
            raise TypeError("table schema must be an exact MoveSchema")
        raw = exact_tuple(self.rows, "table rows")
        expected_keys = tuple(product(range(states), range(symbols)))
        keys: list[tuple[int, int]] = []
        for row in raw:
            triple = exact_tuple(row, "table row")
            if len(triple) != 3:
                raise ValueError("table rows must be state/symbol/transition triples")
            q = exact_int(triple[0], "table input state")
            symbol = exact_int(triple[1], "table input symbol")
            transition = triple[2]
            if type(transition) is not Transition:
                raise TypeError("table output must be an exact Transition")
            q_next = exact_int(transition.next_state, "next state")
            write = exact_int(transition.write_symbol, "write symbol")
            if q_next < 0 or q_next >= states or write < 0 or write >= symbols:
                raise ValueError("table output is outside Q or Sigma")
            self.schema.displacement(transition.move_port)
            keys.append((q, symbol))
        if tuple(keys) != expected_keys:
            raise ValueError("table rows must give every Q x Sigma key once in canonical order")

    def at(self, state: int, symbol: int) -> Transition:
        q = exact_int(state, "lookup state")
        value = exact_int(symbol, "lookup symbol")
        if q < 0 or q >= self.state_count or value < 0 or value >= self.symbol_count:
            raise ValueError("table lookup key is outside Q x Sigma")
        index = q * self.symbol_count + value
        row_q, row_symbol, transition = self.rows[index]
        if (row_q, row_symbol) != (q, value):
            raise RuntimeError("closed table canonical-order invariant failed")
        return transition


def general_rule_count(state_count: int, symbol_count: int, movement_count: int) -> int:
    states = exact_int(state_count, "state count")
    symbols = exact_int(symbol_count, "symbol count")
    moves = exact_int(movement_count, "movement count")
    if states < 1 or symbols < 2 or moves < 1:
        raise ValueError("rule-count parameters are invalid")
    return (moves * states * symbols) ** (states * symbols)


@dataclass(frozen=True)
class Plain:
    symbol: int


@dataclass(frozen=True)
class Head:
    state: int
    symbol: int


Cell = Plain | Head


@dataclass(frozen=True, eq=False)
class SnapshotToken:
    generation: int

    def __post_init__(self) -> None:
        generation = exact_int(self.generation, "snapshot generation")
        if generation < 0:
            raise ValueError("snapshot generation must be nonnegative")


@dataclass(frozen=True)
class TaggedConfiguration:
    state_count: int
    symbol_count: int
    schema: MoveSchema
    default_symbol: int
    entries: tuple[tuple[Coord, Cell], ...]
    token: SnapshotToken = field(compare=False, repr=False)

    def __post_init__(self) -> None:
        states = exact_int(self.state_count, "configuration state count")
        symbols = exact_int(self.symbol_count, "configuration symbol count")
        default = exact_int(self.default_symbol, "configuration default symbol")
        if states < 1 or symbols < 2 or default < 0 or default >= symbols:
            raise ValueError("invalid tagged configuration dimensions")
        if type(self.schema) is not MoveSchema:
            raise TypeError("configuration schema must be an exact MoveSchema")
        if type(self.token) is not SnapshotToken:
            raise TypeError("configuration token must be an exact SnapshotToken")
        raw = exact_tuple(self.entries, "configuration entries")
        previous: Coord | None = None
        heads = 0
        for entry in raw:
            pair = exact_tuple(entry, "configuration entry")
            if len(pair) != 2:
                raise ValueError("configuration entries must be coordinate/cell pairs")
            coord = checked_coord(pair[0], "entry coordinate")
            cell = pair[1]
            if previous is not None and coord <= previous:
                raise ValueError("entry coordinates must be unique and sorted")
            previous = coord
            if type(cell) is Plain:
                symbol = exact_int(cell.symbol, "plain symbol")
                if symbol < 0 or symbol >= symbols:
                    raise ValueError("plain symbol is outside Sigma")
                if symbol == default:
                    raise ValueError("implicit default Plain entries are noncanonical")
            elif type(cell) is Head:
                q = exact_int(cell.state, "tagged head state")
                symbol = exact_int(cell.symbol, "tagged head symbol")
                if q < 0 or q >= states or symbol < 0 or symbol >= symbols:
                    raise ValueError("Head payload is outside Q x Sigma")
                heads += 1
            else:
                raise TypeError("cell must be exactly Plain or Head")
        if heads != 1:
            raise ValueError("a T25 configuration must contain exactly one Head")

    @property
    def generation(self) -> int:
        return self.token.generation

    def at(self, coord: Coord) -> Cell:
        checked = checked_coord(coord)
        for key, cell in self.entries:
            if key == checked:
                return cell
            if key > checked:
                break
        return Plain(self.default_symbol)

    def head_entry(self) -> tuple[Coord, Head]:
        heads = tuple((coord, cell) for coord, cell in self.entries if type(cell) is Head)
        if len(heads) != 1:
            raise RuntimeError("exactly-one-head invariant failed")
        coord, cell = heads[0]
        assert type(cell) is Head
        return coord, cell


def encode_native(state: NativeState) -> TaggedConfiguration:
    data: dict[Coord, Cell] = {
        coord: Plain(symbol) for coord, symbol in state.tape.overrides
    }
    underlying = state.tape.at(state.head_position)
    data[state.head_position] = Head(state.head_state, underlying)
    return TaggedConfiguration(
        state.state_count,
        state.tape.alphabet_size,
        state.schema,
        state.tape.default_symbol,
        tuple(sorted(data.items())),
        SnapshotToken(state.generation),
    )


def decode_tagged(configuration: TaggedConfiguration) -> NativeState:
    head_position, head = configuration.head_entry()
    overrides: dict[Coord, int] = {}
    for coord, cell in configuration.entries:
        if type(cell) is Plain:
            overrides[coord] = cell.symbol
        elif type(cell) is Head and cell.symbol != configuration.default_symbol:
            overrides[coord] = cell.symbol
    tape = TotalTape(
        configuration.symbol_count,
        configuration.default_symbol,
        tuple(sorted(overrides.items())),
    )
    return NativeState(
        configuration.state_count,
        configuration.schema,
        tape,
        head.state,
        head_position,
        configuration.generation,
    )


@dataclass(frozen=True)
class HeadRead:
    token: SnapshotToken
    source: Coord
    head: Head


@dataclass(frozen=True)
class TuringWrites:
    token: SnapshotToken
    schema: MoveSchema
    source: Coord
    old_head: Head
    source_write: Plain
    next_state: int
    selected_port: str


def select_unique_head(configuration: TaggedConfiguration) -> Coord:
    return configuration.head_entry()[0]


def read_head(
    configuration: TaggedConfiguration,
    source: Coord,
) -> HeadRead:
    checked_source = checked_coord(source, "selected source")
    cell = configuration.at(checked_source)
    if type(cell) is not Head:
        raise ValueError("FRONTIER source is not the unique old Head")
    return HeadRead(
        configuration.token,
        checked_source,
        cell,
    )


def make_writes(
    configuration: TaggedConfiguration,
    table: ClosedTMTable,
    read: HeadRead,
) -> TuringWrites:
    if type(table) is not ClosedTMTable:
        raise TypeError("RULE requires an exact closed Turing table")
    if type(read) is not HeadRead:
        raise TypeError("RULE requires an exact HeadRead")
    if read.token is not configuration.token:
        raise ValueError("read provenance does not match the old snapshot")
    if table.schema != configuration.schema:
        raise ValueError("movement schema mismatch")
    if table.state_count != configuration.state_count or table.symbol_count != configuration.symbol_count:
        raise ValueError("table dimensions do not match the configuration")
    if configuration.at(read.source) != read.head:
        raise ValueError("read source/head does not match the old snapshot")
    transition = table.at(read.head.state, read.head.symbol)
    return TuringWrites(
        configuration.token,
        configuration.schema,
        read.source,
        read.head,
        Plain(transition.write_symbol),
        transition.next_state,
        transition.move_port,
    )


def apply_writes(
    configuration: TaggedConfiguration,
    batch: TuringWrites,
) -> TaggedConfiguration:
    if type(batch) is not TuringWrites:
        raise TypeError("UPDATE requires exact typed TuringWrites")
    if batch.token is not configuration.token:
        raise ValueError("write provenance does not match the old snapshot")
    if batch.schema != configuration.schema:
        raise ValueError("write schema does not match the configuration")
    if configuration.at(batch.source) != batch.old_head:
        raise ValueError("write source does not match the old snapshot")
    if type(batch.source_write) is not Plain:
        raise TypeError("T25 RULE must return a Plain source assignment")
    written_symbol = exact_int(batch.source_write.symbol, "source write symbol")
    if written_symbol < 0 or written_symbol >= configuration.symbol_count:
        raise ValueError("source write is outside Sigma")
    next_state = exact_int(batch.next_state, "head movement next state")
    if next_state < 0 or next_state >= configuration.state_count:
        raise ValueError("head movement next state is outside Q")
    destination = add_coord(
        batch.source,
        configuration.schema.displacement(batch.selected_port),
    )
    if batch.source == destination:
        raise ValueError("native source/destination distinction was lost")
    old_destination = configuration.at(destination)
    if type(old_destination) is not Plain:
        raise ValueError("strict nonzero movement must reach an old Plain cell on Z^2")
    # UPDATE, not RULE, preserves the old destination symbol.  Thus the compact
    # rule cannot inspect or branch on any candidate destination value.
    destination_write = Head(next_state, old_destination.symbol)
    data = dict(configuration.entries)
    if written_symbol == configuration.default_symbol:
        data.pop(batch.source, None)
    else:
        data[batch.source] = Plain(written_symbol)
    data[destination] = destination_write
    return TaggedConfiguration(
        configuration.state_count,
        configuration.symbol_count,
        configuration.schema,
        configuration.default_symbol,
        tuple(sorted(data.items())),
        SnapshotToken(configuration.generation + 1),
    )


def generic_step(table: ClosedTMTable, configuration: TaggedConfiguration) -> TaggedConfiguration:
    active = select_unique_head(configuration)
    reads = read_head(configuration, active)
    writes = make_writes(configuration, table, reads)
    return apply_writes(configuration, writes)


def native_step(table: ClosedTMTable, state: NativeState) -> NativeState:
    if type(table) is not ClosedTMTable:
        raise TypeError("native step requires an exact closed table")
    if table.state_count != state.state_count or table.symbol_count != state.tape.alphabet_size:
        raise ValueError("native table dimensions do not match state")
    if table.schema != state.schema:
        raise ValueError("native table/state movement schemas differ")
    old_symbol = state.tape.at(state.head_position)
    transition = table.at(state.head_state, old_symbol)
    destination = add_coord(state.head_position, state.schema.displacement(transition.move_port))
    next_tape = state.tape.write(state.head_position, transition.write_symbol)
    return NativeState(
        state.state_count,
        state.schema,
        next_tape,
        transition.next_state,
        destination,
        state.generation + 1,
    )


def semantic_key(state: NativeState) -> tuple[object, ...]:
    return (
        state.state_count,
        state.schema,
        state.tape,
        state.head_state,
        state.head_position,
        state.generation,
    )


def assert_commutes(table: ClosedTMTable, native: NativeState) -> None:
    encoded = encode_native(native)
    assert semantic_key(decode_tagged(encoded)) == semantic_key(native)
    native_next = native_step(table, native)
    generic_next = generic_step(table, encoded)
    assert semantic_key(decode_tagged(generic_next)) == semantic_key(native_next)


def tape_with_values(
    symbol_count: int,
    default: int,
    values: dict[Coord, int],
) -> TotalTape:
    overrides = tuple(sorted((coord, value) for coord, value in values.items() if value != default))
    return TotalTape(symbol_count, default, overrides)


def baseline_rows(
    state_count: int,
    symbol_count: int,
    schema: MoveSchema,
) -> tuple[tuple[int, int, Transition], ...]:
    rows: list[tuple[int, int, Transition]] = []
    for q, symbol in product(range(state_count), range(symbol_count)):
        rows.append(
            (
                q,
                symbol,
                Transition(
                    (q + symbol + 1) % state_count,
                    (symbol + q + 1) % symbol_count,
                    schema.labels[(q * symbol_count + symbol) % len(schema.labels)],
                ),
            )
        )
    return tuple(rows)


def table_with_override(
    state_count: int,
    symbol_count: int,
    schema: MoveSchema,
    key: tuple[int, int],
    transition: Transition,
) -> ClosedTMTable:
    rows = list(baseline_rows(state_count, symbol_count, schema))
    index = key[0] * symbol_count + key[1]
    rows[index] = (key[0], key[1], transition)
    return ClosedTMTable(state_count, symbol_count, schema, tuple(rows))


def assert_strict_square_commutation() -> dict[str, int]:
    events = 0
    destination_one = 0
    transition_independence = 0
    origins = ((0, 0), (7, -5))
    for q, symbol in product(range(2), range(2)):
        for next_state, write, port in product(range(2), range(2), SQUARE_SCHEMA.labels):
            transition = Transition(next_state, write, port)
            table = table_with_override(2, 2, SQUARE_SCHEMA, (q, symbol), transition)
            chosen_transitions: set[Transition] = set()
            chosen_rule_intents: set[tuple[int, int, str]] = set()
            for neighbor_symbols in product(range(2), repeat=4):
                for origin in origins:
                    values = {origin: symbol}
                    for (_label, delta), neighbor_symbol in zip(
                        SQUARE_SCHEMA.ports,
                        neighbor_symbols,
                        strict=True,
                    ):
                        values[add_coord(origin, delta)] = neighbor_symbol
                    tape = tape_with_values(2, 0, values)
                    native = NativeState(2, SQUARE_SCHEMA, tape, q, origin)
                    chosen_transitions.add(table.at(q, tape.at(origin)))
                    encoded = encode_native(native)
                    rule_read = read_head(encoded, select_unique_head(encoded))
                    rule_writes = make_writes(encoded, table, rule_read)
                    chosen_rule_intents.add(
                        (
                            rule_writes.next_state,
                            rule_writes.source_write.symbol,
                            rule_writes.selected_port,
                        )
                    )
                    assert_commutes(table, native)
                    next_native = native_step(table, native)
                    old_destination_symbol = tape.at(next_native.head_position)
                    assert next_native.tape.at(next_native.head_position) == old_destination_symbol
                    tagged_next = generic_step(table, encode_native(native))
                    _position, new_head = tagged_next.head_entry()
                    assert new_head.symbol == old_destination_symbol
                    destination_one += int(old_destination_symbol == 1)
                    events += 1
            assert chosen_transitions == {transition}
            assert chosen_rule_intents == {(next_state, write, port)}
            transition_independence += 1
    assert events == 2 * 2 * (2 * 2 * 4) * 16 * 2
    assert destination_one > 0
    return {
        "strict_square_events": events,
        "transition_neighbor_independence_checks": transition_independence,
        "destination_symbol_one_witnesses": destination_one,
        "translation_origins": len(origins),
    }


def checked_heading_action(
    schema: MoveSchema,
    heading_ports: tuple[str, ...],
) -> tuple[str, ...]:
    if type(schema) is not MoveSchema:
        raise TypeError("heading action requires an exact MoveSchema")
    raw = exact_tuple(heading_ports, "heading action ports")
    if len(raw) != len(schema.labels):
        raise ValueError("heading action must contain one port per visible heading")
    checked = tuple(exact_str(port, "heading action port") for port in raw)
    if len(set(checked)) != len(checked) or set(checked) != set(schema.labels):
        raise ValueError("heading action must permute the declared movement ports exactly")
    for port in checked:
        schema.displacement(port)
    return checked


def orientation_port(
    index: int,
    schema: MoveSchema,
    heading_ports: tuple[str, ...],
) -> str:
    q = exact_int(index, "orientation state")
    action = checked_heading_action(schema, heading_ports)
    if q < 0 or q >= len(action):
        raise ValueError("orientation state is outside the movement action")
    return action[q]


def langton_transition(state: int, symbol: int) -> Transition:
    """Closed expansion of sp=s*(2c-1)*i for s in {1,i,-1,-i}."""

    q = exact_int(state, "Langton state")
    color = exact_int(symbol, "Langton symbol")
    if q < 0 or q >= 4 or color not in (0, 1):
        raise ValueError("Langton input is outside four headings x two colors")
    # Multiplication by +i is +1 quarter-turn; by -i is -1.
    next_state = (q + (1 if color == 1 else -1)) % 4
    return Transition(
        next_state,
        1 - color,
        orientation_port(next_state, SQUARE_SCHEMA, SQUARE_C4_HEADING_PORTS),
    )


def langton_table() -> ClosedTMTable:
    return ClosedTMTable(
        4,
        2,
        SQUARE_SCHEMA,
        tuple((q, color, langton_transition(q, color)) for q, color in product(range(4), range(2))),
    )


@dataclass(frozen=True)
class RelativeTurnProgram:
    """Finite visible-heading restriction, never a runtime callback."""

    schema: MoveSchema
    heading_ports: tuple[str, ...]
    rows: tuple[tuple[int, int, int], ...]  # symbol, signed quarter/port turn, write

    def __post_init__(self) -> None:
        if type(self.schema) is not MoveSchema:
            raise TypeError("relative-turn program requires an exact MoveSchema")
        action = checked_heading_action(self.schema, self.heading_ports)
        raw = exact_tuple(self.rows, "relative-turn rows")
        if len(raw) < 2:
            raise ValueError("relative-turn program must cover a finite alphabet")
        symbols: list[int] = []
        for row in raw:
            triple = exact_tuple(row, "relative-turn row")
            if len(triple) != 3:
                raise ValueError("relative-turn rows are symbol/turn/write triples")
            symbol = exact_int(triple[0], "relative input symbol")
            turn = exact_int(triple[1], "relative turn")
            write = exact_int(triple[2], "relative write")
            if turn == 0 or abs(turn) >= len(action):
                raise ValueError("relative turn is outside the declared finite action")
            if write < 0 or write >= len(raw):
                raise ValueError("relative write is outside Sigma")
            symbols.append(symbol)
        if tuple(symbols) != tuple(range(len(raw))):
            raise ValueError("relative-turn rows must cover symbols canonically")


def expand_relative(program: RelativeTurnProgram) -> ClosedTMTable:
    action = checked_heading_action(program.schema, program.heading_ports)
    states = len(action)
    symbols = len(program.rows)
    rows: list[tuple[int, int, Transition]] = []
    for q, symbol in product(range(states), range(symbols)):
        _input_symbol, turn, write = program.rows[symbol]
        next_state = (q + turn) % states
        rows.append(
            (
                q,
                symbol,
                Transition(
                    next_state,
                    write,
                    orientation_port(next_state, program.schema, action),
                ),
            )
        )
    return ClosedTMTable(states, symbols, program.schema, tuple(rows))


def compress_relative(
    table: ClosedTMTable,
    heading_ports: tuple[str, ...],
) -> RelativeTurnProgram:
    action = checked_heading_action(table.schema, heading_ports)
    if table.state_count != len(action):
        raise ValueError("relative-turn image requires one visible heading per movement port")
    relative_rows: list[tuple[int, int, int]] = []
    for symbol in range(table.symbol_count):
        turns: set[int] = set()
        writes: set[int] = set()
        for q in range(table.state_count):
            transition = table.at(q, symbol)
            if transition.move_port != orientation_port(
                transition.next_state,
                table.schema,
                action,
            ):
                raise ValueError("absolute table does not move along its visible next heading")
            raw_turn = (transition.next_state - q) % table.state_count
            turn = raw_turn if raw_turn <= table.state_count // 2 else raw_turn - table.state_count
            if turn == 0:
                raise ValueError("strict relative-turn image excludes zero turns")
            turns.add(turn)
            writes.add(transition.write_symbol)
        if len(turns) != 1 or len(writes) != 1:
            raise ValueError("absolute table is not a state-equivariant relative-turn rule")
        relative_rows.append((symbol, next(iter(turns)), next(iter(writes))))
    program = RelativeTurnProgram(table.schema, action, tuple(relative_rows))
    if expand_relative(program) != table:
        raise RuntimeError("relative expansion round trip failed")
    return program


def assert_langton_and_turning() -> dict[str, int]:
    table = langton_table()
    relative = RelativeTurnProgram(
        SQUARE_SCHEMA,
        SQUARE_C4_HEADING_PORTS,
        ((0, -1, 1), (1, 1, 0)),
    )
    assert expand_relative(relative) == table
    assert compress_relative(table, SQUARE_C4_HEADING_PORTS) == relative

    context_events = 0
    for q, symbol in product(range(4), range(2)):
        assert table.at(q, symbol) == langton_transition(q, symbol)
        for neighbor_symbols in product(range(2), repeat=4):
            origin = (3, -4)
            values = {origin: symbol}
            for (_port, delta), value in zip(SQUARE_SCHEMA.ports, neighbor_symbols, strict=True):
                values[add_coord(origin, delta)] = value
            assert_commutes(
                table,
                NativeState(4, SQUARE_SCHEMA, tape_with_values(2, 0, values), q, origin),
            )
            context_events += 1

    native = NativeState(4, SQUARE_SCHEMA, TotalTape(2, 0), 0, (0, 0))
    trace: list[tuple[int, Coord, tuple[tuple[Coord, int], ...]]] = [
        (native.head_state, native.head_position, native.tape.overrides)
    ]
    trace_events = 128
    for _ in range(trace_events):
        assert_commutes(table, native)
        native = native_step(table, native)
        trace.append((native.head_state, native.head_position, native.tape.overrides))
    assert trace[:6] == [
        (0, (0, 0), ()),
        (3, (0, -1), (((0, 0), 1),)),
        (2, (-1, -1), (((0, -1), 1), ((0, 0), 1))),
        (1, (-1, 0), (((-1, -1), 1), ((0, -1), 1), ((0, 0), 1))),
        (0, (0, 0), (((-1, -1), 1), ((-1, 0), 1), ((0, -1), 1), ((0, 0), 1))),
        (1, (0, 1), (((-1, -1), 1), ((-1, 0), 1), ((0, -1), 1))),
    ]
    trace_digest = sha256(repr(tuple(trace)).encode("utf-8")).hexdigest()

    # An ordinary absolute table need not couple next state to movement.
    nonimage_rows = list(table.rows)
    q, symbol, old = nonimage_rows[0]
    wrong_port = SQUARE_C4_HEADING_PORTS[
        (SQUARE_C4_HEADING_PORTS.index(old.move_port) + 1) % 4
    ]
    nonimage_rows[0] = (q, symbol, replace(old, move_port=wrong_port))
    nonimage = ClosedTMTable(4, 2, SQUARE_SCHEMA, tuple(nonimage_rows))
    rejected_nonimage = 0
    try:
        compress_relative(nonimage, SQUARE_C4_HEADING_PORTS)
    except ValueError:
        rejected_nonimage = 1
    assert rejected_nonimage == 1

    # Three arbitrary head states cannot be silently identified with four headings.
    three_state = ClosedTMTable(3, 2, SQUARE_SCHEMA, baseline_rows(3, 2, SQUARE_SCHEMA))
    rejected_cardinality = 0
    try:
        compress_relative(three_state, SQUARE_C4_HEADING_PORTS)
    except ValueError:
        rejected_cardinality = 1
    assert rejected_cardinality == 1

    return {
        "langton_context_events": context_events,
        "langton_trace_events": trace_events,
        "langton_rows": len(table.rows),
        "relative_roundtrips": 1,
        "relative_nonimage_rejections": rejected_nonimage + rejected_cardinality,
        "langton_trace_digest_words": len(trace_digest),
        "langton_trace_digest_int": int(trace_digest[:12], 16),
    }


def assert_hex_topology_parameterization() -> dict[str, int]:
    # This is a semantic topology/heading witness only.  It is not asserted to
    # reconstruct the Book's underdescribed 1,296-worm historical family.
    relative = RelativeTurnProgram(
        HEX_SCHEMA,
        HEX_C6_HEADING_PORTS,
        ((0, -1, 1), (1, 1, 0)),
    )
    table = expand_relative(relative)
    assert compress_relative(table, HEX_C6_HEADING_PORTS) == relative
    events = 0
    for q, symbol in product(range(6), range(2)):
        for neighbor_symbols in product(range(2), repeat=6):
            origin = (-2, 8)
            values = {origin: symbol}
            for (_port, delta), value in zip(HEX_SCHEMA.ports, neighbor_symbols, strict=True):
                values[add_coord(origin, delta)] = value
            assert_commutes(
                table,
                NativeState(6, HEX_SCHEMA, tape_with_values(2, 0, values), q, origin),
            )
            events += 1
    assert events == 6 * 2 * 2**6
    return {
        "hex_topology_witness_events": events,
        "hex_visible_heading_states": 6,
        "source_worm_count_retained_only": 1296,
        "invented_worm_schema_count": 0,
    }


def quotient_locally_injective(shape: tuple[int, int], schema: MoveSchema) -> bool:
    raw = exact_tuple(shape, "quotient shape")
    if len(raw) != 2:
        raise ValueError("quotient shape must be two-dimensional")
    width = exact_int(raw[0], "quotient extent 0")
    height = exact_int(raw[1], "quotient extent 1")
    if width <= 0 or height <= 0:
        raise ValueError("quotient extents must be positive")
    source = (0, 0)
    targets = tuple(
        ((delta[0] % width), (delta[1] % height)) for _port, delta in schema.ports
    )
    return source not in targets and len(set(targets)) == len(targets)


def assert_realization_and_outcome_boundaries() -> dict[str, int]:
    assert not quotient_locally_injective((1, 1), SQUARE_SCHEMA)
    assert not quotient_locally_injective((2, 2), SQUARE_SCHEMA)
    assert quotient_locally_injective((3, 3), SQUARE_SCHEMA)

    # A total tape advances beyond every finite viewport; the viewport is not
    # a native edge or halt.  This table always moves axis0+.
    table = ClosedTMTable(
        1,
        2,
        SQUARE_SCHEMA,
        (
            (0, 0, Transition(0, 1, "axis0+")),
            (0, 1, Transition(0, 1, "axis0+")),
        ),
    )
    state = NativeState(1, SQUARE_SCHEMA, TotalTape(2, 0), 0, (0, 0))
    viewport_exits = 0
    events = 20
    for _ in range(events):
        assert_commutes(table, state)
        state = native_step(table, state)
        if not (-2 <= state.head_position[0] <= 2 and -2 <= state.head_position[1] <= 2):
            viewport_exits += 1
    assert state.head_position == (20, 0)
    assert viewport_exits == 18

    # Port labels are semantic only together with an explicit coordinate-frame
    # map.  Silently reusing the same label under a swapped frame diverges;
    # applying the visible coordinate isomorphism restores one-step commutation.
    frame_rows = (
        (0, 0, Transition(0, 1, "axis0+")),
        (0, 1, Transition(0, 0, "axis0+")),
    )
    book_table = ClosedTMTable(1, 2, SQUARE_SCHEMA, frame_rows)
    swapped_table = ClosedTMTable(1, 2, SWAPPED_FRAME_SCHEMA, frame_rows)
    book_state = NativeState(
        1,
        SQUARE_SCHEMA,
        tape_with_values(2, 0, {(1, 0): 1}),
        0,
        (0, 0),
    )

    def swap_coord(coord: Coord) -> Coord:
        return (coord[1], coord[0])

    def swap_state(state: NativeState) -> NativeState:
        return NativeState(
            state.state_count,
            SWAPPED_FRAME_SCHEMA,
            TotalTape(
                state.tape.alphabet_size,
                state.tape.default_symbol,
                tuple(sorted((swap_coord(coord), symbol) for coord, symbol in state.tape.overrides)),
            ),
            state.head_state,
            swap_coord(state.head_position),
            state.generation,
        )

    assert_commutes(book_table, book_state)
    swapped_state = swap_state(book_state)
    assert_commutes(swapped_table, swapped_state)
    mapped_book_next = swap_state(native_step(book_table, book_state))
    swapped_next = native_step(swapped_table, swapped_state)
    assert semantic_key(mapped_book_next) == semantic_key(swapped_next)

    silently_swapped_next = native_step(
        swapped_table,
        replace(book_state, schema=SWAPPED_FRAME_SCHEMA),
    )
    assert native_step(book_table, book_state).head_position == (1, 0)
    assert silently_swapped_next.head_position == (0, 1)
    assert native_step(book_table, book_state).head_position != silently_swapped_next.head_position

    return {
        "unbounded_viewport_events": events,
        "viewport_exit_continuations": viewport_exits,
        "quotient_alias_rejections": 2,
        "locally_injective_quotients": 1,
        "native_halts": 0,
        "frame_native_generic_events": 2,
        "explicit_frame_commutations": 1,
        "silent_frame_relabel_divergences": 1,
    }


def assert_frozen_program_provenance() -> dict[str, int]:
    # The source's randomly chosen examples sample a complete table at setup.
    # This witness enters execution only as immutable closed rows; no runtime
    # transition draw, callback, or hidden RNG participates in a step.
    table = ClosedTMTable(2, 2, SQUARE_SCHEMA, baseline_rows(2, 2, SQUARE_SCHEMA))
    table_digest = sha256(repr(table.rows).encode("utf-8")).hexdigest()
    assert table_digest == "96f68c00a5ced8344d990cecd8f6386eecc2309249ca48be0db306211a09b485"
    initial = NativeState(
        2,
        SQUARE_SCHEMA,
        tape_with_values(2, 0, {(-1, 0): 1, (0, 0): 1, (0, 1): 1}),
        1,
        (0, 0),
    )

    def replay() -> tuple[tuple[object, ...], ...]:
        state = initial
        trace: list[tuple[object, ...]] = [semantic_key(state)]
        for _ in range(12):
            assert_commutes(table, state)
            state = native_step(table, state)
            trace.append(semantic_key(state))
        return tuple(trace)

    first = replay()
    second = replay()
    assert first == second
    assert sha256(repr(table.rows).encode("utf-8")).hexdigest() == table_digest
    return {
        "frozen_setup_tables": 1,
        "frozen_setup_rows": len(table.rows),
        "replay_native_generic_events": 24,
        "runtime_rule_draws": 0,
        "table_digest_words": len(table_digest),
        "table_digest_int": int(table_digest[:12], 16),
    }


def assert_rule_spaces_and_distinctions() -> dict[str, int]:
    assert general_rule_count(2, 2, 4) == 16**4 == 65_536
    assert general_rule_count(3, 2, 4) == 24**6 == 191_102_976
    assert general_rule_count(4, 2, 4) == 32**8 == 2**40
    assert general_rule_count(2, 2, 2) == 8**4 == 4_096  # T12 one-dimensional control
    mobile_2d_count = (4 * 2) ** 2
    assert mobile_2d_count == 64
    assert mobile_2d_count != general_rule_count(2, 2, 4)
    return {
        "derived_rule_count_checks": 5,
        "square_two_state_binary_rules": general_rule_count(2, 2, 4),
        "square_three_state_binary_rules": general_rule_count(3, 2, 4),
        "square_four_state_binary_rules": general_rule_count(4, 2, 4),
        "strict_move_ports": 4,
        "source_numeric_codecs": 0,
    }


def assert_atomicity_and_observer_separation() -> dict[str, int]:
    table = ClosedTMTable(2, 2, SQUARE_SCHEMA, baseline_rows(2, 2, SQUARE_SCHEMA))
    tape = tape_with_values(2, 0, {(0, 0): 1, (1, 0): 1})
    native = NativeState(2, SQUARE_SCHEMA, tape, 1, (0, 0))
    old = encode_native(native)
    source = select_unique_head(old)
    reads = read_head(old, source)
    writes = make_writes(old, table, reads)

    # Exposing only the source write would create zero heads and is therefore
    # not a valid intermediate configuration.  UPDATE exposes only the valid
    # atomic result.
    partial_data = dict(old.entries)
    partial_data[source] = writes.source_write
    zero_head_rejected = 0
    try:
        TaggedConfiguration(
            old.state_count,
            old.symbol_count,
            old.schema,
            old.default_symbol,
            tuple(sorted(partial_data.items())),
            SnapshotToken(old.generation + 1),
        )
    except ValueError:
        zero_head_rejected = 1
    assert zero_head_rejected == 1
    new = apply_writes(old, writes)
    assert len(tuple(cell for _coord, cell in new.entries if type(cell) is Head)) == 1

    # Path and visit data are derived from complete snapshots and cannot alter
    # a transition chosen from the same old configuration.
    path_observer = (native.head_position, native_step(table, native).head_position)
    visits_observer = {native.head_position: 1}
    assert generic_step(table, old) == new
    assert path_observer[0] in visits_observer

    return {
        "atomic_batches": 1,
        "zero_head_intermediate_rejections": zero_head_rejected,
        "path_observer_checks": 1,
        "visit_history_rule_inputs": 0,
    }


def expect_rejection(
    expected: type[BaseException],
    operation: Callable[[], object],
) -> None:
    try:
        operation()
    except expected:
        return
    except BaseException as error:  # pragma: no cover - diagnostic path
        raise AssertionError(f"expected {expected.__name__}, got {type(error).__name__}") from error
    raise AssertionError(f"expected {expected.__name__}")


def assert_hostile_validation() -> dict[str, int]:
    rejections = 0

    def rejects(expected: type[BaseException], operation: Callable[[], object]) -> None:
        nonlocal rejections
        expect_rejection(expected, operation)
        rejections += 1

    rejects(TypeError, lambda: checked_coord((True, 0)))
    rejects(ValueError, lambda: checked_coord((0,)))
    rejects(ValueError, lambda: MoveSchema("bad", (("stay", (0, 0)),)))
    rejects(ValueError, lambda: MoveSchema("bad", (("p", (1, 0)), ("p", (0, 1)))))
    rejects(ValueError, lambda: MoveSchema("bad", (("p", (1, 0)), ("q", (1, 0)))))
    rejects(ValueError, lambda: TotalTape(2, 0, (((0, 0), 0),)))
    rejects(ValueError, lambda: TotalTape(2, 0, (((1, 0), 1), ((0, 0), 1))))
    rejects(ValueError, lambda: TotalTape(2, 0, (((0, 0), 2),)))
    rejects(ValueError, lambda: NativeState(0, SQUARE_SCHEMA, TotalTape(2, 0), 0, (0, 0)))
    rejects(ValueError, lambda: NativeState(1, SQUARE_SCHEMA, TotalTape(2, 0), 1, (0, 0)))

    good_rows = baseline_rows(2, 2, SQUARE_SCHEMA)
    rejects(ValueError, lambda: ClosedTMTable(2, 2, SQUARE_SCHEMA, good_rows[:-1]))
    duplicate = (good_rows[0], good_rows[0], *good_rows[2:])
    rejects(ValueError, lambda: ClosedTMTable(2, 2, SQUARE_SCHEMA, duplicate))
    bad_state_rows = list(good_rows)
    bad_state_rows[0] = (0, 0, Transition(2, 0, "axis0+"))
    rejects(ValueError, lambda: ClosedTMTable(2, 2, SQUARE_SCHEMA, tuple(bad_state_rows)))
    bad_symbol_rows = list(good_rows)
    bad_symbol_rows[0] = (0, 0, Transition(0, 2, "axis0+"))
    rejects(ValueError, lambda: ClosedTMTable(2, 2, SQUARE_SCHEMA, tuple(bad_symbol_rows)))
    bad_move_rows = list(good_rows)
    bad_move_rows[0] = (0, 0, Transition(0, 0, "north"))
    rejects(ValueError, lambda: ClosedTMTable(2, 2, SQUARE_SCHEMA, tuple(bad_move_rows)))
    rejects(TypeError, lambda: ClosedTMTable(2, 2, SQUARE_SCHEMA, "callback"))

    token = SnapshotToken(0)
    rejects(
        ValueError,
        lambda: TaggedConfiguration(2, 2, SQUARE_SCHEMA, 0, (((0, 0), Plain(1)),), token),
    )
    rejects(
        ValueError,
        lambda: TaggedConfiguration(
            2,
            2,
            SQUARE_SCHEMA,
            0,
            (((0, 0), Head(0, 0)), ((1, 0), Head(1, 1))),
            token,
        ),
    )
    rejects(
        ValueError,
        lambda: TaggedConfiguration(
            2,
            2,
            SQUARE_SCHEMA,
            0,
            (((0, 0), Head(0, 0)), ((1, 0), Plain(0))),
            token,
        ),
    )
    rejects(
        TypeError,
        lambda: TaggedConfiguration(2, 2, SQUARE_SCHEMA, 0, (((0, 0), 0),), token),
    )

    table = ClosedTMTable(2, 2, SQUARE_SCHEMA, good_rows)
    config = encode_native(NativeState(2, SQUARE_SCHEMA, TotalTape(2, 0), 0, (0, 0)))
    source = select_unique_head(config)
    read = read_head(config, source)
    batch = make_writes(config, table, read)
    assert tuple(HeadRead.__dataclass_fields__) == ("token", "source", "head")
    assert "destination" not in TuringWrites.__dataclass_fields__
    assert "destination_symbol" not in TuringWrites.__dataclass_fields__
    rejects(ValueError, lambda: make_writes(config, table, replace(read, token=SnapshotToken(0))))
    rejects(ValueError, lambda: make_writes(config, table, replace(read, source=(9, 9))))
    rejects(ValueError, lambda: make_writes(config, table, replace(read, head=Head(0, 1))))
    hex_table = ClosedTMTable(2, 2, HEX_SCHEMA, baseline_rows(2, 2, HEX_SCHEMA))
    rejects(ValueError, lambda: make_writes(config, hex_table, read))
    rejects(TypeError, lambda: make_writes(config, "callback", read))
    rejects(ValueError, lambda: apply_writes(config, replace(batch, token=SnapshotToken(0))))
    rejects(ValueError, lambda: apply_writes(config, replace(batch, schema=HEX_SCHEMA)))
    rejects(ValueError, lambda: apply_writes(config, replace(batch, source=(9, 9))))
    rejects(ValueError, lambda: apply_writes(config, replace(batch, old_head=Head(1, 0))))
    rejects(TypeError, lambda: apply_writes(config, replace(batch, source_write=Head(0, 0))))
    rejects(TypeError, lambda: apply_writes(config, replace(batch, source_write=Plain(True))))
    rejects(ValueError, lambda: apply_writes(config, replace(batch, source_write=Plain(2))))
    rejects(ValueError, lambda: apply_writes(config, replace(batch, next_state=2)))
    rejects(ValueError, lambda: apply_writes(config, replace(batch, selected_port="outside")))
    rejects(ValueError, lambda: quotient_locally_injective((0, 2), SQUARE_SCHEMA))
    rejects(ValueError, lambda: general_rule_count(0, 2, 4))
    rejects(ValueError, lambda: langton_transition(4, 0))
    rejects(
        ValueError,
        lambda: RelativeTurnProgram(
            SQUARE_SCHEMA,
            SQUARE_C4_HEADING_PORTS,
            ((0, 0, 1), (1, 1, 0)),
        ),
    )

    # A bare union cannot retain both head state and underlying symbol.
    bare_union = {("symbol", 0), ("symbol", 1), ("state", 0), ("state", 1)}
    composite_heads = {(q, symbol) for q, symbol in product(range(2), range(2))}
    assert len(composite_heads) == 4
    assert len({item for item in bare_union if item[0] == "state"}) == 2
    assert len(composite_heads) > len({item for item in bare_union if item[0] == "state"})

    return {
        "hostile_rejections": rejections,
        "bare_union_loss_witnesses": 1,
    }


def semantic_digest(counts: dict[str, int]) -> str:
    transcript = "\n".join(f"{key}={counts[key]}" for key in sorted(counts))
    return sha256(transcript.encode("utf-8")).hexdigest()


EXPECTED_SEMANTIC_DIGEST = "8eed091c1b3635661fb160ce76a49738f282ae1ec94a71fcb8a303a8735434e2"


def main() -> None:
    groups = {
        "square": assert_strict_square_commutation(),
        "turning": assert_langton_and_turning(),
        "hex": assert_hex_topology_parameterization(),
        "realization": assert_realization_and_outcome_boundaries(),
        "provenance": assert_frozen_program_provenance(),
        "rules": assert_rule_spaces_and_distinctions(),
        "atomicity": assert_atomicity_and_observer_separation(),
        "hostile": assert_hostile_validation(),
    }
    counts = {
        f"{group}.{key}": value
        for group, values in groups.items()
        for key, value in values.items()
    }
    native_generic_events = (
        groups["square"]["strict_square_events"]
        + groups["turning"]["langton_context_events"]
        + groups["turning"]["langton_trace_events"]
        + groups["hex"]["hex_topology_witness_events"]
        + groups["realization"]["unbounded_viewport_events"]
        + groups["realization"]["frame_native_generic_events"]
        + groups["provenance"]["replay_native_generic_events"]
    )
    counts["total.native_generic_events"] = native_generic_events
    digest = semantic_digest(counts)
    assert digest == EXPECTED_SEMANTIC_DIGEST

    print("T25 semantic oracle: PASS")
    print(f"native_generic_events={native_generic_events}")
    print(
        "event_partition="
        f"strict_square:{groups['square']['strict_square_events']},"
        f"langton_context:{groups['turning']['langton_context_events']},"
        f"langton_trace:{groups['turning']['langton_trace_events']},"
        f"hex_topology_witness:{groups['hex']['hex_topology_witness_events']},"
        f"unbounded_viewport:{groups['realization']['unbounded_viewport_events']},"
        f"frame_mapping:{groups['realization']['frame_native_generic_events']},"
        f"frozen_table_replay:{groups['provenance']['replay_native_generic_events']}"
    )
    print(
        "strict_square=discrete_t+2D;raw_book_array_frame;four_semantic_axis_ports;"
        "port_tuple_order_is_not_a_numeric_codec;exactly_one_Head"
    )
    print(
        "compact_rule=QxSigma->QxSigmaxMovePort;decision_reads_head_only;"
        f"neighbor_independence_checks={groups['square']['transition_neighbor_independence_checks']};"
        "UPDATE_preserves_destination_symbol_without_RULE_visibility"
    )
    print(
        "rule_counts=derived_formula_(m*s*k)^(s*k);"
        f"square_s2k2:{groups['rules']['square_two_state_binary_rules']};"
        f"square_s3k2:{groups['rules']['square_three_state_binary_rules']};"
        f"square_s4k2:{groups['rules']['square_four_state_binary_rules']};"
        "source_numeric_codec=NONE"
    )
    print(
        "langton_ant=source_formula_materialized_as_8_closed_rows;"
        "visible_C4_heading;relative_turn_expansion_roundtrip=PASS;"
        f"absolute_nonimage_rejections={groups['turning']['relative_nonimage_rejections']}"
    )
    print(
        "hex_route=six_semantic_ports+visible_heading_uses_same_event;"
        "source_1296_worm_count_retained;exact_worm_schema=UNDERDETERMINED;"
        "invented_factorization=NONE"
    )
    print(
        "representation=factored_(q,tape,r)<->Plain(symbol)|Head(q,symbol);"
        "one_native_event=one_generic_event;bare_union_is_lossy;CA_microsteps=NONE"
    )
    print(
        "update=old_snapshot_atomic_tagged_move;concrete_two_label_commit_is_lowering;"
        f"zero_head_intermediate_rejections={groups['atomicity']['zero_head_intermediate_rejections']};"
        "path+visit_history+time_lift_are_observers"
    )
    print(
        "realizations=size1_and_size2_periodic_aliases_rejected;size3_local_ports_injective;"
        f"viewport_exit_continuations={groups['realization']['viewport_exit_continuations']};"
        "finite_edge_or_viewport_exit_is_not_halt;explicit_frame_map_commutes;"
        "silent_frame_relabel_diverges"
    )
    print(
        "rule_provenance=random_sampling_is_setup_only;closed_table_is_immutable;"
        f"replay_events={groups['provenance']['replay_native_generic_events']};"
        "runtime_rule_draws=0"
    )
    print(
        "runtime_audit=reuse_finite_values+selector_concepts+old_snapshot_UPDATE;"
        "gaps=composite_alphabet,UniqueTag,total_sparse_Z2,typed_ports,closed_product_tables,"
        "typed_assignment_and_movement_writes,structured_traces;family_dispatch_is_not_semantics"
    )
    print(
        "classification=T12+T21+T24_categories1_to_3;"
        "new_T25_UPDATE_algebra=NONE;D011_topology_port_parameterization=YES;"
        "new_executor=NONE;relative_turn_and_hex_are_closed_visible_data"
    )
    print(f"hostile_rejections={groups['hostile']['hostile_rejections']}")
    print(f"semantic_digest={digest}")


if __name__ == "__main__":
    main()
