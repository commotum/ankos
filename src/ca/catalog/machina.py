"""Ordinary five-component constructors for controllers and machines.

Canonical family names assemble already-closed components into
:class:`~ca.program.SimpleProgram` values.  They attach no family identity,
perform no execution dispatch, and contain no hidden interpreter.
"""

from __future__ import annotations

from itertools import product as cartesian_product
from math import prod
from typing import TypeVar
import warnings

from .. import alphabets, frontiers, loci, neighborhoods, rules, seeds
from ..program import SimpleProgram


C = TypeVar("C")
V = TypeVar("V")
W = TypeVar("W")
R = TypeVar("R")


# ---------------------------------------------------------------------------
# Phase 1. Canonical families
# ---------------------------------------------------------------------------


def enumerative_semidecision(
    *,
    seed: seeds.Seed[C],
    alphabet: alphabets.Alphabet[V],
    frontier: frontiers.WritableRegion[C, W],
    neighborhood: neighborhoods.ReadableRegion[C, R],
    rule: rules.Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """Assemble the SPF010 / F011 structural profile."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def finite_gate_circuit(
    *,
    seed: seeds.Seed[C],
    alphabet: alphabets.Alphabet[V],
    frontier: frontiers.WritableRegion[C, W],
    neighborhood: neighborhoods.ReadableRegion[C, R],
    rule: rules.Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """Assemble the SPF013 / F014 structural profile."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def mobile_head_grid_rewrite(
    *,
    seed: seeds.Seed[C],
    alphabet: alphabets.Alphabet[V],
    frontier: frontiers.WritableRegion[C, W],
    neighborhood: neighborhoods.ReadableRegion[C, R],
    rule: rules.Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """Assemble the SPF030 / F031 structural profile."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def nearest_neighbor_retrieval(
    *,
    seed: seeds.Seed[C],
    alphabet: alphabets.Alphabet[V],
    frontier: frontiers.WritableRegion[C, W],
    neighborhood: neighborhoods.ReadableRegion[C, R],
    rule: rules.Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """Assemble the SPF035 / F036 structural profile."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def recursive_function_evaluator(
    *,
    seed: seeds.Seed[C],
    alphabet: alphabets.Alphabet[V],
    frontier: frontiers.WritableRegion[C, W],
    neighborhood: neighborhoods.ReadableRegion[C, R],
    rule: rules.Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """Assemble the SPF044 / F047 structural profile."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def register_machine(
    *,
    seed: seeds.Seed[C],
    alphabet: alphabets.Alphabet[V],
    frontier: frontiers.WritableRegion[C, W],
    neighborhood: neighborhoods.ReadableRegion[C, R],
    rule: rules.Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """Assemble the SPF045 / F048 structural profile."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def stored_program_random_access_machine(
    *,
    seed: seeds.Seed[C],
    alphabet: alphabets.Alphabet[V],
    frontier: frontiers.WritableRegion[C, W],
    neighborhood: neighborhoods.ReadableRegion[C, R],
    rule: rules.Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """Assemble the SPF048 / F051 structural profile."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def priority_dovetailed_oracle_construction(
    *,
    seed: seeds.Seed[C],
    alphabet: alphabets.Alphabet[V],
    frontier: frontiers.WritableRegion[C, W],
    neighborhood: neighborhoods.ReadableRegion[C, R],
    rule: rules.Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """Assemble the SPF053 / F056 structural profile."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


# ---------------------------------------------------------------------------
# Phase 2. Presets
# ---------------------------------------------------------------------------

_ZERO_INTEGER_BOUNDARY = loci.Boundary(loci.BoundaryPolicy.FIXED, 0)
_LINE_OFFSETS = ((-1,), (0,), (1,))
_CARDINAL_2D = (
    (-1, 0),
    (0, -1),
    (0, 0),
    (0, 1),
    (1, 0),
)


def _strict_positive_int(value: object, *, label: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{label} must be an integer")
    if value <= 0:
        raise ValueError(f"{label} must be positive")
    return value


def _palette_values(
    values: object,
    *,
    symbols: int,
    count: int | None,
    label: str,
) -> tuple[int, ...]:
    if type(values) is not tuple:
        raise TypeError(f"{label} must be an immutable tuple")
    if count is not None and len(values) != count:
        raise ValueError(f"{label} must contain exactly {count} values")
    if any(type(value) is not int for value in values):
        raise TypeError(f"{label} values must be integers")
    if any(value < 0 or value >= symbols for value in values):
        raise ValueError(f"{label} values must lie in range({symbols})")
    return values


def _states(value: object) -> tuple[str, ...]:
    if type(value) is not tuple:
        raise TypeError("Turing states must be an immutable tuple")
    if not value:
        raise ValueError("Turing states cannot be empty")
    if any(type(state) is not str or not state for state in value):
        raise TypeError("Turing states must be nonempty strings")
    if len(set(value)) != len(value):
        raise ValueError("Turing states must be unique")
    return value


def _integer_boundary(
    boundary: object,
    *,
    symbols: int,
    label: str,
) -> loci.Boundary[int]:
    if type(boundary) is not loci.Boundary:
        raise TypeError(f"{label} boundary must be a Boundary")
    if boundary.policy is loci.BoundaryPolicy.FIXED and (
        type(boundary.exterior) is not int
        or boundary.exterior < 0
        or boundary.exterior >= symbols
    ):
        raise ValueError(
            f"{label} fixed exterior must be an integer in range({symbols})"
        )
    return boundary


def _cell(symbol: int) -> alphabets.ValueNode:
    return alphabets.tag_value("cell", symbol)


def _mobile_head(symbol: int) -> alphabets.ValueNode:
    return alphabets.tag_value("head", symbol)


def _turing_head(state: str, symbol: int) -> alphabets.ValueNode:
    return alphabets.tag_value(f"head:{state}", symbol)


def _tagged_boundary(
    boundary: loci.Boundary[int],
    *,
    symbols: int,
    label: str,
) -> loci.Boundary[alphabets.ValueNode]:
    resolved = _integer_boundary(boundary, symbols=symbols, label=label)
    return loci.Boundary(
        resolved.policy,
        (
            _cell(resolved.exterior)
            if resolved.policy is loci.BoundaryPolicy.FIXED
            else None
        ),
    )


def _certificate(
    kind: rules.CertificateKind,
    label: str,
) -> rules.Certificate:
    return rules.Certificate(kind, rules.literal_expr(label))


def _all_equal(
    expected: tuple[alphabets.SemanticValue, ...],
) -> rules.RuleExpr:
    checks = tuple(
        rules.equal(
            rules.project(rules.group(0), index),
            rules.literal_expr(value),
        )
        for index, value in enumerate(expected)
    )
    return rules.RuleExpr(
        rules.ExpressionPrimitive.ALL,
        (rules.RuleExpr(rules.ExpressionPrimitive.TUPLE, checks),),
    )


def _derivation_result(
    replacements: tuple[tuple[int, alphabets.SemanticValue], ...],
    *,
    label: str,
    continuation: rules.Continuation = rules.Continue(),
) -> rules.DerivationClauseResult:
    return rules.DerivationClauseResult(
        tuple(
            rules.ExistingDispositionPlan(
                rules.capability_group_item(0, index),
                rules.DispositionAction.REPLACE,
                rules.literal_expr(value),
            )
            for index, value in replacements
        ),
        (),
        (
            rules.Progress.ADVANCED
            if replacements
            else rules.Progress.QUIESCENT
        ),
        continuation,
        rules.literal_expr(label),
        (f"catalog:{label}",),
        _certificate(rules.CertificateKind.DERIVATION, f"{label}:derived"),
    )


def _zero_anchor_result(*, label: str) -> rules.DerivationClauseResult:
    return _derivation_result(
        (),
        label=label,
        continuation=rules.Stop(
            rules.literal_expr("no-head"),
            _certificate(rules.CertificateKind.TERMINALITY, f"{label}:terminal"),
        ),
    )


def _terminal_transition_result(*, label: str) -> rules.DerivationClauseResult:
    """Return an explicit typed terminal continuation without hidden fallback."""

    return _derivation_result(
        (),
        label=label,
        continuation=rules.Stop(
            rules.literal_expr("missing-transition"),
            _certificate(rules.CertificateKind.TERMINALITY, f"{label}:terminal"),
        ),
    )


def _machine_alphabet(
    *,
    symbols: int,
    head_tags: tuple[str, ...],
) -> alphabets.Alphabet:
    symbol_alphabet = alphabets.int_range_alphabet(symbols)
    return alphabets.union(
        (
            alphabets.tag("cell", symbol_alphabet),
            *(alphabets.tag(tag, symbol_alphabet) for tag in head_tags),
        )
    )


def _machine_program(
    *,
    source: loci.FiniteConfiguration,
    alphabet: alphabets.Alphabet,
    offsets: tuple[tuple[int, ...], ...],
    anchor: alphabets.ValueAnchor,
    clauses: tuple[rules.RuleClause, ...],
    label: str,
) -> SimpleProgram:
    writable = frontiers.value_relative(
        anchor,
        offsets,
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.value_relative(
        anchor,
        offsets,
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    rule = rules.anchored_clause_kernel(
        clauses,
        group_channel=0,
        zero_result=_zero_anchor_result(label=f"{label}-no-head"),
        contract=rules.RuleContract(
            source.contract,
            alphabet.value_profile,
            readable.result_shape,
            readable.join_shape,
            writable.effect_profile,
        ),
        completeness_evidence=_certificate(
            rules.CertificateKind.COMPLETENESS,
            f"{label}:complete",
        ),
        conflict_policy=rules.ProposalConflictPolicy.REQUIRE_EQUAL,
        selection=rules.ClauseSelection.FIRST,
    )
    return mobile_head_grid_rewrite(
        seed=seeds.exact(source, value_profile=alphabet.value_profile),
        alphabet=alphabet,
        frontier=writable,
        neighborhood=readable,
        rule=rule,
    )


def _mobile_inputs(
    *,
    initial: object,
    head: object,
    colors: object,
    transitions: object,
    neighbor_updating: bool,
) -> tuple[
    tuple[int, ...],
    int,
    int,
    tuple[
        tuple[
            tuple[int, int, int],
            tuple[int, int] | tuple[tuple[int, int, int], int],
        ],
        ...,
    ],
]:
    size = _strict_positive_int(colors, label="mobile colors")
    if size < 2:
        raise ValueError("mobile colors must be at least two")
    values = _palette_values(
        initial,
        symbols=size,
        count=None,
        label="mobile initial state",
    )
    if len(values) < 3:
        raise ValueError("mobile initial state needs at least three cells")
    if type(head) is not int:
        raise TypeError("mobile head position must be an integer")
    if head < 0 or head >= len(values):
        raise ValueError("mobile head position is outside the grid")
    if type(transitions) is not tuple:
        raise TypeError("mobile transitions must be an immutable tuple")
    parsed: list[
        tuple[
            tuple[int, int, int],
            tuple[int, int] | tuple[tuple[int, int, int], int],
        ]
    ] = []
    seen: set[tuple[int, int, int]] = set()
    for entry in transitions:
        if type(entry) is not tuple or len(entry) != 2:
            raise TypeError("each mobile transition must be a pair")
        key, output = entry
        resolved_key = _palette_values(
            key,
            symbols=size,
            count=3,
            label="mobile transition key",
        )
        if resolved_key in seen:
            raise ValueError("mobile transition keys must be unique")
        seen.add(resolved_key)
        if type(output) is not tuple or len(output) != 2:
            raise TypeError("mobile transition output must be a pair")
        payload, movement = output
        if type(movement) is not int:
            raise TypeError("mobile transition movement must be an integer")
        if movement not in (-1, 1):
            raise ValueError("mobile transition movement must be -1 or 1")
        if neighbor_updating:
            resolved_payload = _palette_values(
                payload,
                symbols=size,
                count=3,
                label="neighbor-updating mobile output block",
            )
            parsed.append((resolved_key, (resolved_payload, movement)))
        else:
            if type(payload) is not int:
                raise TypeError("mobile output symbol must be an integer")
            if payload < 0 or payload >= size:
                raise ValueError("mobile output symbol is outside the palette")
            parsed.append((resolved_key, (payload, movement)))
    if seen != set(cartesian_product(range(size), repeat=3)):
        raise ValueError("mobile transitions must be total on all symbol triples")
    return values, head, size, tuple(parsed)


def mobile_automaton(
    *,
    initial: tuple[int, ...],
    head: int,
    colors: int,
    transitions: tuple[
        tuple[tuple[int, int, int], tuple[int, int]],
        ...,
    ],
    boundary: loci.Boundary[int] = _ZERO_INTEGER_BOUNDARY,
) -> SimpleProgram:
    """Construct a center-updating mobile automaton with one tagged head."""

    values, head_index, size, parsed = _mobile_inputs(
        initial=initial,
        head=head,
        colors=colors,
        transitions=transitions,
        neighbor_updating=False,
    )
    alphabet = _machine_alphabet(symbols=size, head_tags=("head",))
    source = loci.grid_configuration(
        (len(values),),
        tuple(
            _mobile_head(value) if index == head_index else _cell(value)
            for index, value in enumerate(values)
        ),
        boundary=_tagged_boundary(
            boundary,
            symbols=size,
            label="mobile automaton",
        ),
        axes=("x",),
    )
    clauses = tuple(
        rules.RuleClause(
            _all_equal(
                (
                    _cell(key[0]),
                    _mobile_head(key[1]),
                    _cell(key[2]),
                )
            ),
            _derivation_result(
                (
                    (1, _cell(output[0])),
                    (
                        output[1] + 1,
                        _mobile_head(key[output[1] + 1]),
                    ),
                ),
                label="mobile-transition",
            ),
        )
        for key, output in parsed
    )
    return _machine_program(
        source=source,
        alphabet=alphabet,
        offsets=_LINE_OFFSETS,
        anchor=alphabets.ValueAnchor(
            alphabets.value_tagged("head"),
            alphabets.AnchorCardinality.EXACTLY_ONE,
        ),
        clauses=clauses,
        label="mobile-automaton",
    )


def neighbor_updating_mobile_automaton(
    *,
    initial: tuple[int, ...],
    head: int,
    colors: int,
    transitions: tuple[
        tuple[
            tuple[int, int, int],
            tuple[tuple[int, int, int], int],
        ],
        ...,
    ],
    boundary: loci.Boundary[int] = _ZERO_INTEGER_BOUNDARY,
) -> SimpleProgram:
    """Construct a mobile automaton that atomically rewrites its full block."""

    values, head_index, size, parsed = _mobile_inputs(
        initial=initial,
        head=head,
        colors=colors,
        transitions=transitions,
        neighbor_updating=True,
    )
    alphabet = _machine_alphabet(symbols=size, head_tags=("head",))
    source = loci.grid_configuration(
        (len(values),),
        tuple(
            _mobile_head(value) if index == head_index else _cell(value)
            for index, value in enumerate(values)
        ),
        boundary=_tagged_boundary(
            boundary,
            symbols=size,
            label="neighbor-updating mobile automaton",
        ),
        axes=("x",),
    )
    clauses = tuple(
        rules.RuleClause(
            _all_equal(
                (
                    _cell(key[0]),
                    _mobile_head(key[1]),
                    _cell(key[2]),
                )
            ),
            _derivation_result(
                tuple(
                    (
                        index,
                        (
                            _mobile_head(output[0][index])
                            if index == output[1] + 1
                            else _cell(output[0][index])
                        ),
                    )
                    for index in range(3)
                ),
                label="neighbor-updating-mobile-transition",
            ),
        )
        for key, output in parsed
    )
    return _machine_program(
        source=source,
        alphabet=alphabet,
        offsets=_LINE_OFFSETS,
        anchor=alphabets.ValueAnchor(
            alphabets.value_tagged("head"),
            alphabets.AnchorCardinality.EXACTLY_ONE,
        ),
        clauses=clauses,
        label="neighbor-updating-mobile-automaton",
    )


def _turing_anchor(states: tuple[str, ...]) -> alphabets.ValueAnchor:
    predicates = tuple(
        alphabets.value_tagged(f"head:{state}") for state in states
    )
    predicate = (
        predicates[0]
        if len(predicates) == 1
        else alphabets.value_or(predicates)
    )
    return alphabets.ValueAnchor(
        predicate,
        alphabets.AnchorCardinality.EXACTLY_ONE,
    )


def _turing_transitions_1d(
    *,
    transitions: object,
    states: tuple[str, ...],
    symbols: int,
) -> tuple[tuple[tuple[str, int], tuple[str, int, int]], ...]:
    if type(transitions) is not tuple:
        raise TypeError("Turing transitions must be an immutable tuple")
    parsed: list[tuple[tuple[str, int], tuple[str, int, int]]] = []
    seen: set[tuple[str, int]] = set()
    allowed_states = set(states)
    for entry in transitions:
        if type(entry) is not tuple or len(entry) != 2:
            raise TypeError("each Turing transition must be a pair")
        key, output = entry
        if type(key) is not tuple or len(key) != 2:
            raise TypeError("Turing transition key must be (state, symbol)")
        state, symbol = key
        if type(state) is not str or state not in allowed_states:
            raise ValueError("Turing transition key state is not declared")
        if type(symbol) is not int:
            raise TypeError("Turing transition key symbol must be an integer")
        if symbol < 0 or symbol >= symbols:
            raise ValueError("Turing transition key symbol is outside the alphabet")
        resolved_key = (state, symbol)
        if resolved_key in seen:
            raise ValueError("Turing transition keys must be unique")
        seen.add(resolved_key)
        if type(output) is not tuple or len(output) != 3:
            raise TypeError(
                "Turing transition output must be (state, symbol, movement)"
            )
        next_state, write_symbol, movement = output
        if type(next_state) is not str or next_state not in allowed_states:
            raise ValueError("Turing output state is not declared")
        if type(write_symbol) is not int:
            raise TypeError("Turing output symbol must be an integer")
        if write_symbol < 0 or write_symbol >= symbols:
            raise ValueError("Turing output symbol is outside the alphabet")
        if type(movement) is not int:
            raise TypeError("Turing movement must be an integer")
        if movement not in (-1, 1):
            raise ValueError("Turing movement must be -1 or 1")
        parsed.append((resolved_key, (next_state, write_symbol, movement)))
    return tuple(parsed)


def turing_machine(
    *,
    tape: tuple[int, ...],
    head: int,
    initial_state: str,
    states: tuple[str, ...],
    symbols: int,
    transitions: tuple[
        tuple[tuple[str, int], tuple[str, int, int]],
        ...,
    ],
    boundary: loci.Boundary[int] = _ZERO_INTEGER_BOUNDARY,
) -> SimpleProgram:
    """Construct a one-tape Turing machine with explicit terminal gaps."""

    resolved_states = _states(states)
    if type(initial_state) is not str or initial_state not in resolved_states:
        raise ValueError("Turing initial state must be declared")
    size = _strict_positive_int(symbols, label="Turing symbols")
    values = _palette_values(
        tape,
        symbols=size,
        count=None,
        label="Turing tape",
    )
    if len(values) < 3:
        raise ValueError("Turing tape needs at least three cells")
    if type(head) is not int:
        raise TypeError("Turing head position must be an integer")
    if head < 0 or head >= len(values):
        raise ValueError("Turing head position is outside the tape")
    parsed = _turing_transitions_1d(
        transitions=transitions,
        states=resolved_states,
        symbols=size,
    )
    alphabet = _machine_alphabet(
        symbols=size,
        head_tags=tuple(f"head:{state}" for state in resolved_states),
    )
    source = loci.grid_configuration(
        (len(values),),
        tuple(
            (
                _turing_head(initial_state, value)
                if index == head
                else _cell(value)
            )
            for index, value in enumerate(values)
        ),
        boundary=_tagged_boundary(
            boundary,
            symbols=size,
            label="Turing machine",
        ),
        axes=("x",),
    )
    clauses: list[rules.RuleClause] = []
    for (state, scanned), (next_state, write_symbol, movement) in parsed:
        for left, right in cartesian_product(range(size), repeat=2):
            clauses.append(
                rules.RuleClause(
                    _all_equal(
                        (
                            _cell(left),
                            _turing_head(state, scanned),
                            _cell(right),
                        )
                    ),
                    _derivation_result(
                        (
                            (1, _cell(write_symbol)),
                            (
                                movement + 1,
                                _turing_head(
                                    next_state,
                                    left if movement == -1 else right,
                                ),
                            ),
                        ),
                        label="turing-transition",
                    ),
                )
            )
    clauses.append(
        rules.RuleClause(
            rules.literal_expr(True),
            _terminal_transition_result(label="turing-missing-transition"),
        )
    )
    return _machine_program(
        source=source,
        alphabet=alphabet,
        offsets=_LINE_OFFSETS,
        anchor=_turing_anchor(resolved_states),
        clauses=tuple(clauses),
        label="turing-machine",
    )


def _shape_2d(value: object) -> tuple[int, int]:
    if type(value) is not tuple:
        raise TypeError("2D Turing shape must be an immutable tuple")
    if len(value) != 2:
        raise ValueError("2D Turing shape must have rank two")
    if any(type(size) is not int for size in value):
        raise TypeError("2D Turing shape extents must be integers")
    if any(size <= 0 for size in value):
        raise ValueError("2D Turing shape extents must be positive")
    return value


def _turing_transitions_2d(
    *,
    transitions: object,
    states: tuple[str, ...],
    symbols: int,
) -> tuple[
    tuple[
        tuple[str, int],
        tuple[str, int, tuple[int, int]],
    ],
    ...,
]:
    if type(transitions) is not tuple:
        raise TypeError("2D Turing transitions must be an immutable tuple")
    parsed: list[
        tuple[
            tuple[str, int],
            tuple[str, int, tuple[int, int]],
        ]
    ] = []
    seen: set[tuple[str, int]] = set()
    allowed_states = set(states)
    movements = set(_CARDINAL_2D) - {(0, 0)}
    for entry in transitions:
        if type(entry) is not tuple or len(entry) != 2:
            raise TypeError("each 2D Turing transition must be a pair")
        key, output = entry
        if type(key) is not tuple or len(key) != 2:
            raise TypeError("2D Turing transition key must be (state, symbol)")
        state, symbol = key
        if type(state) is not str or state not in allowed_states:
            raise ValueError("2D Turing transition key state is not declared")
        if type(symbol) is not int:
            raise TypeError("2D Turing transition key symbol must be an integer")
        if symbol < 0 or symbol >= symbols:
            raise ValueError(
                "2D Turing transition key symbol is outside the alphabet"
            )
        resolved_key = (state, symbol)
        if resolved_key in seen:
            raise ValueError("2D Turing transition keys must be unique")
        seen.add(resolved_key)
        if type(output) is not tuple or len(output) != 3:
            raise TypeError(
                "2D Turing output must be (state, symbol, movement)"
            )
        next_state, write_symbol, movement = output
        if type(next_state) is not str or next_state not in allowed_states:
            raise ValueError("2D Turing output state is not declared")
        if type(write_symbol) is not int:
            raise TypeError("2D Turing output symbol must be an integer")
        if write_symbol < 0 or write_symbol >= symbols:
            raise ValueError("2D Turing output symbol is outside the alphabet")
        if type(movement) is not tuple:
            raise TypeError("2D Turing movement must be a coordinate tuple")
        if movement not in movements:
            raise ValueError("2D Turing movement must be a cardinal unit offset")
        parsed.append((resolved_key, (next_state, write_symbol, movement)))
    return tuple(parsed)


def turing_machine_2d(
    *,
    shape: tuple[int, int],
    tape: tuple[int, ...],
    head: tuple[int, int],
    initial_state: str,
    states: tuple[str, ...],
    symbols: int,
    transitions: tuple[
        tuple[
            tuple[str, int],
            tuple[str, int, tuple[int, int]],
        ],
        ...,
    ],
    boundary: loci.Boundary[int] = _ZERO_INTEGER_BOUNDARY,
) -> SimpleProgram:
    """Construct a square-grid Turing machine with cardinal head motion.

    ``head`` is a zero-based row-major array coordinate within ``shape``.
    """

    resolved_shape = _shape_2d(shape)
    resolved_states = _states(states)
    if type(initial_state) is not str or initial_state not in resolved_states:
        raise ValueError("2D Turing initial state must be declared")
    size = _strict_positive_int(symbols, label="2D Turing symbols")
    values = _palette_values(
        tape,
        symbols=size,
        count=prod(resolved_shape),
        label="2D Turing tape",
    )
    if type(head) is not tuple:
        raise TypeError("2D Turing head must be a coordinate tuple")
    if len(head) != 2:
        raise ValueError("2D Turing head must have rank two")
    if any(type(part) is not int for part in head):
        raise TypeError("2D Turing head coordinates must be integers")
    if any(part < 0 or part >= extent for part, extent in zip(head, resolved_shape)):
        raise ValueError("2D Turing head coordinate is outside the grid")
    parsed = _turing_transitions_2d(
        transitions=transitions,
        states=resolved_states,
        symbols=size,
    )
    alphabet = _machine_alphabet(
        symbols=size,
        head_tags=tuple(f"head:{state}" for state in resolved_states),
    )
    head_index = head[0] * resolved_shape[1] + head[1]
    source = loci.grid_configuration(
        resolved_shape,
        tuple(
            (
                _turing_head(initial_state, value)
                if index == head_index
                else _cell(value)
            )
            for index, value in enumerate(values)
        ),
        boundary=_tagged_boundary(
            boundary,
            symbols=size,
            label="2D Turing machine",
        ),
        axes=("x", "y"),
    )
    center_index = _CARDINAL_2D.index((0, 0))
    clauses: list[rules.RuleClause] = []
    for (state, scanned), (next_state, write_symbol, movement) in parsed:
        for neighbors in cartesian_product(range(size), repeat=4):
            expected_symbols = iter(neighbors)
            expected = tuple(
                (
                    _turing_head(state, scanned)
                    if offset == (0, 0)
                    else _cell(next(expected_symbols))
                )
                for offset in _CARDINAL_2D
            )
            destination_index = _CARDINAL_2D.index(movement)
            destination_symbol = alphabets.tag_payload(expected[destination_index])
            clauses.append(
                rules.RuleClause(
                    _all_equal(expected),
                    _derivation_result(
                        (
                            (center_index, _cell(write_symbol)),
                            (
                                destination_index,
                                _turing_head(next_state, destination_symbol),
                            ),
                        ),
                        label="turing-2d-transition",
                    ),
                )
            )
    clauses.append(
        rules.RuleClause(
            rules.literal_expr(True),
            _terminal_transition_result(label="turing-2d-missing-transition"),
        )
    )
    return _machine_program(
        source=source,
        alphabet=alphabet,
        offsets=_CARDINAL_2D,
        anchor=_turing_anchor(resolved_states),
        clauses=tuple(clauses),
        label="turing-machine-2d",
    )


# ---------------------------------------------------------------------------
# Phase 3. True aliases
# ---------------------------------------------------------------------------

_PENDING_ALIASES: tuple[tuple[str, str], ...] = ()


# ---------------------------------------------------------------------------
# Phase 4. Compatibility adapters
# ---------------------------------------------------------------------------

def extended_mobile_automaton(
    *,
    initial: tuple[int, ...],
    head: int,
    colors: int,
    transitions: tuple[
        tuple[
            tuple[int, int, int],
            tuple[tuple[int, int, int], int],
        ],
        ...,
    ],
    boundary: loci.Boundary[int] = _ZERO_INTEGER_BOUNDARY,
) -> SimpleProgram:
    """Deprecated exact spelling of :func:`neighbor_updating_mobile_automaton`."""

    warnings.warn(
        "extended_mobile_automaton is deprecated; use "
        "neighbor_updating_mobile_automaton",
        DeprecationWarning,
        stacklevel=2,
    )
    return neighbor_updating_mobile_automaton(
        initial=initial,
        head=head,
        colors=colors,
        transitions=transitions,
        boundary=boundary,
    )


__all__ = (
    "enumerative_semidecision",
    "finite_gate_circuit",
    "mobile_head_grid_rewrite",
    "nearest_neighbor_retrieval",
    "priority_dovetailed_oracle_construction",
    "recursive_function_evaluator",
    "register_machine",
    "stored_program_random_access_machine",
    "mobile_automaton",
    "neighbor_updating_mobile_automaton",
    "turing_machine",
    "turing_machine_2d",
    "extended_mobile_automaton",
)
