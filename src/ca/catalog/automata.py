"""Ordinary five-component constructors for persistent-carrier automata.

Canonical family names are typed, family-blind assembly functions: they
validate only through :class:`~ca.program.SimpleProgram` and attach no catalog
identity or alternate execution behavior.  Concrete presets bind those same
five components explicitly.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product as cartesian_product
from math import prod
from typing import TypeVar

from .. import alphabets, frontiers, loci, neighborhoods, rules, seeds
from ..program import SimpleProgram


C = TypeVar("C")
V = TypeVar("V")
W = TypeVar("W")
R = TypeVar("R")


# ---------------------------------------------------------------------------
# Phase 1. Canonical families
# ---------------------------------------------------------------------------


def alternating_partition_local_evolution(
    *,
    seed: seeds.Seed[C],
    alphabet: alphabets.Alphabet[V],
    frontier: frontiers.WritableRegion[C, W],
    neighborhood: neighborhoods.ReadableRegion[C, R],
    rule: rules.Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """Assemble the SPF001 / F001 structural profile."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def asynchronous_local_state_automaton(
    *,
    seed: seeds.Seed[C],
    alphabet: alphabets.Alphabet[V],
    frontier: frontiers.WritableRegion[C, W],
    neighborhood: neighborhoods.ReadableRegion[C, R],
    rule: rules.Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """Assemble the SPF003 / F003 structural profile."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def coupled_field_mobile_locus_evolution(
    *,
    seed: seeds.Seed[C],
    alphabet: alphabets.Alphabet[V],
    frontier: frontiers.WritableRegion[C, W],
    neighborhood: neighborhoods.ReadableRegion[C, R],
    rule: rules.Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """Assemble the SPF007 / F007 structural profile."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def driven_relaxation(
    *,
    seed: seeds.Seed[C],
    alphabet: alphabets.Alphabet[V],
    frontier: frontiers.WritableRegion[C, W],
    neighborhood: neighborhoods.ReadableRegion[C, R],
    rule: rules.Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """Assemble the SPF009 / F009 structural profile."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def history_dependent_agent_game(
    *,
    seed: seeds.Seed[C],
    alphabet: alphabets.Alphabet[V],
    frontier: frontiers.WritableRegion[C, W],
    neighborhood: neighborhoods.ReadableRegion[C, R],
    rule: rules.Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """Assemble the SPF021 / F022 structural profile."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def iterated_map(
    *,
    seed: seeds.Seed[C],
    alphabet: alphabets.Alphabet[V],
    frontier: frontiers.WritableRegion[C, W],
    neighborhood: neighborhoods.ReadableRegion[C, R],
    rule: rules.Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """Assemble the SPF026 / F027 structural profile."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def multi_active_local_rewrite(
    *,
    seed: seeds.Seed[C],
    alphabet: alphabets.Alphabet[V],
    frontier: frontiers.WritableRegion[C, W],
    neighborhood: neighborhoods.ReadableRegion[C, R],
    rule: rules.Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """Assemble the SPF032 / F033 structural profile."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def mutable_rule_local_automaton(
    *,
    seed: seeds.Seed[C],
    alphabet: alphabets.Alphabet[V],
    frontier: frontiers.WritableRegion[C, W],
    neighborhood: neighborhoods.ReadableRegion[C, R],
    rule: rules.Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """Assemble the SPF034 / F035 structural profile."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def population_evolutionary_search(
    *,
    seed: seeds.Seed[C],
    alphabet: alphabets.Alphabet[V],
    frontier: frontiers.WritableRegion[C, W],
    neighborhood: neighborhoods.ReadableRegion[C, R],
    rule: rules.Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """Assemble the SPF040 / F043 structural profile."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def synchronous_local_state_transform(
    *,
    seed: seeds.Seed[C],
    alphabet: alphabets.Alphabet[V],
    frontier: frontiers.WritableRegion[C, W],
    neighborhood: neighborhoods.ReadableRegion[C, R],
    rule: rules.Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """Assemble the SPF050 / F053 structural profile."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def weighted_network_state_update(
    *,
    seed: seeds.Seed[C],
    alphabet: alphabets.Alphabet[V],
    frontier: frontiers.WritableRegion[C, W],
    neighborhood: neighborhoods.ReadableRegion[C, R],
    rule: rules.Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """Assemble the SPF052 / F055 structural profile."""

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
_PERIODIC_INTEGER_BOUNDARY = loci.Boundary(loci.BoundaryPolicy.PERIODIC)
_ZERO_RATIONAL_BOUNDARY = loci.Boundary(
    loci.BoundaryPolicy.FIXED,
    Fraction(0),
)
_RADIUS_ONE = ((-1,), (0,), (1,))
_VON_NEUMANN_2D = (
    (-1, 0),
    (0, -1),
    (0, 0),
    (0, 1),
    (1, 0),
)
_MOORE_2D = tuple(cartesian_product(range(-1, 2), repeat=2))


def _strict_positive_int(value: object, *, label: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{label} must be an integer")
    if value <= 0:
        raise ValueError(f"{label} must be positive")
    return value


def _shape(
    value: object,
    *,
    rank: int | None,
    label: str,
) -> tuple[int, ...]:
    if type(value) is not tuple:
        raise TypeError(f"{label} must be an immutable tuple")
    if not value:
        raise ValueError(f"{label} cannot be empty")
    if rank is not None and len(value) != rank:
        raise ValueError(f"{label} must have rank {rank}")
    if any(type(size) is not int for size in value):
        raise TypeError(f"{label} extents must be integers")
    if any(size <= 0 for size in value):
        raise ValueError(f"{label} extents must be positive")
    return value


def _axes(
    value: object,
    *,
    rank: int,
) -> tuple[str, ...] | None:
    if value is None:
        return None
    if type(value) is not tuple:
        raise TypeError("lattice axes must be an immutable tuple or None")
    if len(value) != rank:
        raise ValueError("lattice axes must match the lattice rank")
    if any(type(axis) is not str or not axis for axis in value):
        raise TypeError("lattice axes must be nonempty strings")
    if len(set(value)) != len(value):
        raise ValueError("lattice axes must be unique")
    return value


def _offsets(
    value: object,
    *,
    rank: int,
    label: str,
) -> tuple[tuple[int, ...], ...]:
    if type(value) is not tuple:
        raise TypeError(f"{label} must be an immutable tuple")
    if not value:
        raise ValueError(f"{label} cannot be empty")
    if any(type(offset) is not tuple for offset in value):
        raise TypeError(f"{label} must contain immutable coordinate tuples")
    if any(len(offset) != rank for offset in value):
        raise ValueError(f"{label} coordinates must have rank {rank}")
    if any(any(type(part) is not int for part in offset) for offset in value):
        raise TypeError(f"{label} coordinates must be integers")
    if len(set(value)) != len(value):
        raise ValueError(f"{label} coordinates must be unique")
    if (0,) * rank not in value:
        raise ValueError(f"{label} must include the source coordinate")
    return value


def _palette_values(
    values: object,
    *,
    colors: int,
    count: int | None,
    label: str,
) -> tuple[int, ...]:
    if type(values) is not tuple:
        raise TypeError(f"{label} must be an immutable tuple")
    if count is not None and len(values) != count:
        raise ValueError(f"{label} must contain exactly {count} values")
    if any(type(value) is not int for value in values):
        raise TypeError(f"{label} values must be integers")
    if any(value < 0 or value >= colors for value in values):
        raise ValueError(f"{label} values must lie in range({colors})")
    return values


def _integer_boundary(
    boundary: object,
    *,
    colors: int,
    label: str,
) -> loci.Boundary[int]:
    if type(boundary) is not loci.Boundary:
        raise TypeError(f"{label} boundary must be a Boundary")
    if boundary.policy is loci.BoundaryPolicy.FIXED and (
        type(boundary.exterior) is not int
        or boundary.exterior < 0
        or boundary.exterior >= colors
    ):
        raise ValueError(
            f"{label} fixed exterior must be an integer in range({colors})"
        )
    return boundary


def _table_index(
    *,
    colors: int,
    width: int,
) -> rules.RuleExpr:
    """Encode declared observation order with the first value most significant."""

    terms = tuple(
        rules.multiply(
            rules.literal_expr(colors ** (width - index - 1)),
            rules.project(rules.group(0), index),
        )
        for index in range(width)
    )
    return terms[0] if len(terms) == 1 else rules.add(*terms)


def _grid_expression_program(
    *,
    shape: tuple[int, ...],
    initial: tuple[alphabets.SemanticValue, ...],
    alphabet: alphabets.Alphabet,
    offsets: tuple[tuple[int, ...], ...],
    expression: rules.RuleExpr,
    boundary: loci.Boundary,
    axes: tuple[str, ...] | None,
) -> SimpleProgram:
    if (
        boundary.policy is loci.BoundaryPolicy.NONE
        and any(
            any(part != 0 for part in offset)
            for offset in offsets
        )
    ):
        raise ValueError(
            "BoundaryPolicy.NONE cannot totalize a finite neighborhood "
            "with nonzero offsets"
        )
    source = loci.grid_configuration(
        shape,
        initial,
        boundary=boundary,
        axes=axes,
    )
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.grid_relative(
        offsets,
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    rule = rules.expression(
        rules.ExistingPlan(
            rules.ExistingPlanKind.BY_TARGET,
            (expression,),
        ),
        contract=rules.RuleContract(
            source.contract,
            alphabet.value_profile,
            readable.result_shape,
            readable.join_shape,
            writable.effect_profile,
        ),
        witness=rules.literal_expr("expression-replacement"),
        provenance=("mechanics:expression-replacement",),
    )
    return synchronous_local_state_transform(
        seed=seeds.exact(source, value_profile=alphabet.value_profile),
        alphabet=alphabet,
        frontier=writable,
        neighborhood=readable,
        rule=rule,
    )


def _finite_table_program(
    *,
    shape: tuple[int, ...],
    initial: tuple[int, ...],
    colors: int,
    offsets: tuple[tuple[int, ...], ...],
    table: tuple[int, ...],
    boundary: loci.Boundary[int],
    axes: tuple[str, ...] | None,
    totalistic: bool = False,
) -> SimpleProgram:
    alphabet = alphabets.int_range_alphabet(colors)
    index = (
        rules.add(
            *(rules.project(rules.group(0), index) for index in range(len(offsets)))
        )
        if totalistic
        else _table_index(colors=colors, width=len(offsets))
    )
    return _grid_expression_program(
        shape=shape,
        initial=initial,
        alphabet=alphabet,
        offsets=offsets,
        expression=rules.lookup(table, index),
        boundary=boundary,
        axes=axes,
    )


def _rank_one_table_inputs(
    *,
    initial: object,
    colors: object,
    rule: object,
    boundary: object,
    label: str,
) -> tuple[tuple[int, ...], int, tuple[int, ...], loci.Boundary[int]]:
    resolved_colors = _strict_positive_int(colors, label=f"{label} colors")
    if resolved_colors < 2:
        raise ValueError(f"{label} colors must be at least two")
    resolved_initial = _palette_values(
        initial,
        colors=resolved_colors,
        count=None,
        label=f"{label} initial state",
    )
    if not resolved_initial:
        raise ValueError(f"{label} initial state cannot be empty")
    expected = resolved_colors ** len(_RADIUS_ONE)
    resolved_rule = _palette_values(
        rule,
        colors=resolved_colors,
        count=expected,
        label=f"{label} rule table",
    )
    resolved_boundary = _integer_boundary(
        boundary,
        colors=resolved_colors,
        label=label,
    )
    return resolved_initial, resolved_colors, resolved_rule, resolved_boundary


def multicolor_cellular_automaton(
    *,
    initial: tuple[int, ...],
    colors: int,
    rule: tuple[int, ...],
    boundary: loci.Boundary[int] = _ZERO_INTEGER_BOUNDARY,
) -> SimpleProgram:
    """Construct a rank-one radius-one finite-palette cellular automaton.

    The rule table is indexed in declared offset order ``(-1, 0, 1)`` with
    the first observed value as the most-significant base-``colors`` digit.
    """

    values, size, table, resolved_boundary = _rank_one_table_inputs(
        initial=initial,
        colors=colors,
        rule=rule,
        boundary=boundary,
        label="multicolor cellular automaton",
    )
    return _finite_table_program(
        shape=(len(values),),
        initial=values,
        colors=size,
        offsets=_RADIUS_ONE,
        table=table,
        boundary=resolved_boundary,
        axes=("x",),
    )


def totalistic_cellular_automaton(
    *,
    initial: tuple[int, ...],
    colors: int,
    rule: tuple[int, ...],
    radius: int = 1,
    boundary: loci.Boundary[int] = _ZERO_INTEGER_BOUNDARY,
) -> SimpleProgram:
    """Construct a rank-one finite-palette totalistic cellular automaton."""

    size = _strict_positive_int(colors, label="totalistic colors")
    if size < 2:
        raise ValueError("totalistic colors must be at least two")
    resolved_radius = _strict_positive_int(radius, label="totalistic radius")
    values = _palette_values(
        initial,
        colors=size,
        count=None,
        label="totalistic initial state",
    )
    if not values:
        raise ValueError("totalistic initial state cannot be empty")
    offsets = tuple((offset,) for offset in range(-resolved_radius, resolved_radius + 1))
    table = _palette_values(
        rule,
        colors=size,
        count=(size - 1) * len(offsets) + 1,
        label="totalistic rule table",
    )
    return _finite_table_program(
        shape=(len(values),),
        initial=values,
        colors=size,
        offsets=offsets,
        table=table,
        boundary=_integer_boundary(
            boundary,
            colors=size,
            label="totalistic cellular automaton",
        ),
        axes=("x",),
        totalistic=True,
    )


def three_color_totalistic_cellular_automaton(
    *,
    initial: tuple[int, ...],
    rule: tuple[int, ...],
    boundary: loci.Boundary[int] = _ZERO_INTEGER_BOUNDARY,
) -> SimpleProgram:
    """Construct the three-color radius-one totalistic specialization."""

    return totalistic_cellular_automaton(
        initial=initial,
        colors=3,
        rule=rule,
        radius=1,
        boundary=boundary,
    )


def higher_color_totalistic_cellular_automaton(
    *,
    initial: tuple[int, ...],
    colors: int,
    rule: tuple[int, ...],
    radius: int = 1,
    boundary: loci.Boundary[int] = _ZERO_INTEGER_BOUNDARY,
) -> SimpleProgram:
    """Construct a totalistic cellular automaton with four or more colors."""

    size = _strict_positive_int(colors, label="higher-color totalistic colors")
    if size < 4:
        raise ValueError("higher-color totalistic colors must be at least four")
    return totalistic_cellular_automaton(
        initial=initial,
        colors=size,
        rule=rule,
        radius=radius,
        boundary=boundary,
    )


def quiescent_cellular_automaton(
    *,
    initial: tuple[int, ...],
    colors: int,
    rule: tuple[int, ...],
    background: int = 0,
    boundary: loci.Boundary[int] = _ZERO_INTEGER_BOUNDARY,
) -> SimpleProgram:
    """Construct a finite radius-one table whose background is quiescent."""

    values, size, table, resolved_boundary = _rank_one_table_inputs(
        initial=initial,
        colors=colors,
        rule=rule,
        boundary=boundary,
        label="quiescent cellular automaton",
    )
    if type(background) is not int:
        raise TypeError("quiescent background must be an integer")
    if background < 0 or background >= size:
        raise ValueError("quiescent background must lie in the palette")
    background_index = sum(
        background * size ** power for power in range(len(_RADIUS_ONE))
    )
    if table[background_index] != background:
        raise ValueError("rule table does not preserve the uniform background")
    return _finite_table_program(
        shape=(len(values),),
        initial=values,
        colors=size,
        offsets=_RADIUS_ONE,
        table=table,
        boundary=resolved_boundary,
        axes=("x",),
    )


def symmetric_cellular_automaton(
    *,
    initial: tuple[int, ...],
    colors: int,
    rule: tuple[int, ...],
    boundary: loci.Boundary[int] = _ZERO_INTEGER_BOUNDARY,
) -> SimpleProgram:
    """Construct a finite radius-one table invariant under left/right reflection."""

    values, size, table, resolved_boundary = _rank_one_table_inputs(
        initial=initial,
        colors=colors,
        rule=rule,
        boundary=boundary,
        label="symmetric cellular automaton",
    )
    for left, center, right in cartesian_product(range(size), repeat=3):
        forward = left * size * size + center * size + right
        reflected = right * size * size + center * size + left
        if table[forward] != table[reflected]:
            raise ValueError("rule table is not reflection symmetric")
    return _finite_table_program(
        shape=(len(values),),
        initial=values,
        colors=size,
        offsets=_RADIUS_ONE,
        table=table,
        boundary=resolved_boundary,
        axes=("x",),
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


def _anchored_result(
    replacements: tuple[tuple[int, alphabets.SemanticValue], ...],
    *,
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
        rules.literal_expr("anchored-replacement"),
        ("mechanics:anchored-replacement",),
        _certificate(
            rules.CertificateKind.DERIVATION,
            "anchored-replacement:derived",
        ),
    )


def _mobile_value(symbol: int, *, active: bool) -> alphabets.ValueNode:
    return alphabets.tag_value("active", symbol) if active else alphabets.tag_value(
        "cell",
        symbol,
    )


def _tagged_boundary(
    boundary: loci.Boundary[int],
    *,
    colors: int,
    label: str,
) -> loci.Boundary[alphabets.ValueNode]:
    resolved = _integer_boundary(boundary, colors=colors, label=label)
    return loci.Boundary(
        resolved.policy,
        (
            _mobile_value(resolved.exterior, active=False)
            if resolved.policy is loci.BoundaryPolicy.FIXED
            else None
        ),
    )


def generalized_mobile_automaton(
    *,
    initial: tuple[int, ...],
    active: tuple[int, ...],
    colors: int,
    transitions: tuple[
        tuple[
            tuple[int, int, int],
            tuple[int, tuple[int, ...]],
        ],
        ...,
    ],
    boundary: loci.Boundary[int] = _PERIODIC_INTEGER_BOUNDARY,
    conflict_policy: rules.ProposalConflictPolicy = (
        rules.ProposalConflictPolicy.REQUIRE_EQUAL
    ),
) -> SimpleProgram:
    """Construct a finite multi-active mobile automaton.

    Every transition maps the observed ``(left, source, right)`` symbols to a
    new source symbol and a unique tuple of active offsets drawn from
    ``(-1, 0, 1)``. Empty output tuples delete an active locus; multiple output
    offsets split it.
    """

    size = _strict_positive_int(colors, label="generalized mobile colors")
    if size < 2:
        raise ValueError("generalized mobile colors must be at least two")
    values = _palette_values(
        initial,
        colors=size,
        count=None,
        label="generalized mobile initial state",
    )
    if len(values) < 3:
        raise ValueError("generalized mobile initial state needs at least three cells")
    if type(active) is not tuple:
        raise TypeError("generalized mobile active positions must be a tuple")
    if any(type(index) is not int for index in active):
        raise TypeError("generalized mobile active positions must be integers")
    if len(set(active)) != len(active):
        raise ValueError("generalized mobile active positions must be unique")
    if any(index < 0 or index >= len(values) for index in active):
        raise ValueError("generalized mobile active position is outside the grid")
    if type(conflict_policy) is not rules.ProposalConflictPolicy:
        raise TypeError("generalized mobile conflict policy is not recognized")
    if type(transitions) is not tuple:
        raise TypeError("generalized mobile transitions must be an immutable tuple")
    parsed: list[
        tuple[tuple[int, int, int], tuple[int, tuple[int, ...]]]
    ] = []
    seen: set[tuple[int, int, int]] = set()
    for entry in transitions:
        if type(entry) is not tuple or len(entry) != 2:
            raise TypeError("each generalized mobile transition must be a pair")
        key, output = entry
        key = _palette_values(
            key,
            colors=size,
            count=3,
            label="generalized mobile transition key",
        )
        if key in seen:
            raise ValueError("generalized mobile transition keys must be unique")
        seen.add(key)
        if type(output) is not tuple or len(output) != 2:
            raise TypeError("generalized mobile transition output must be a pair")
        new_symbol, destinations = output
        if type(new_symbol) is not int:
            raise TypeError("generalized mobile output symbol must be an integer")
        if new_symbol < 0 or new_symbol >= size:
            raise ValueError("generalized mobile output symbol is outside the palette")
        if type(destinations) is not tuple:
            raise TypeError("generalized mobile destinations must be a tuple")
        if any(type(offset) is not int for offset in destinations):
            raise TypeError("generalized mobile destinations must be integers")
        if len(set(destinations)) != len(destinations):
            raise ValueError("generalized mobile destinations must be unique")
        if any(offset not in (-1, 0, 1) for offset in destinations):
            raise ValueError("generalized mobile destinations must be -1, 0, or 1")
        parsed.append((key, (new_symbol, destinations)))
    expected_keys = set(cartesian_product(range(size), repeat=3))
    if seen != expected_keys:
        raise ValueError(
            "generalized mobile transitions must be total on all symbol triples"
        )
    resolved_boundary = _integer_boundary(
        boundary,
        colors=size,
        label="generalized mobile automaton",
    )
    if resolved_boundary.policy is not loci.BoundaryPolicy.PERIODIC:
        raise ValueError(
            "generalized mobile automaton requires a periodic boundary"
        )

    alphabet = alphabets.union(
        (
            alphabets.tag("cell", alphabets.int_range_alphabet(size)),
            alphabets.tag("active", alphabets.int_range_alphabet(size)),
        )
    )
    source_values = tuple(
        _mobile_value(value, active=index in active)
        for index, value in enumerate(values)
    )
    source = loci.grid_configuration(
        (len(values),),
        source_values,
        boundary=_tagged_boundary(
            resolved_boundary,
            colors=size,
            label="generalized mobile automaton",
        ),
        axes=("x",),
    )
    anchor = alphabets.ValueAnchor(
        alphabets.value_tagged("active"),
        alphabets.AnchorCardinality.ZERO_OR_MORE,
    )
    writable = frontiers.value_relative(
        anchor,
        _RADIUS_ONE,
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.value_relative(
        anchor,
        _RADIUS_ONE,
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    clauses: list[rules.RuleClause] = []
    for key, (new_symbol, destinations) in parsed:
        for left_active, right_active in cartesian_product((False, True), repeat=2):
            expected = (
                _mobile_value(key[0], active=left_active),
                _mobile_value(key[1], active=True),
                _mobile_value(key[2], active=right_active),
            )
            output_indices = {1, *(offset + 1 for offset in destinations)}
            replacements = tuple(
                (
                    index,
                    _mobile_value(
                        new_symbol if index == 1 else key[index],
                        active=(index - 1) in destinations,
                    ),
                )
                for index in sorted(output_indices)
            )
            clauses.append(
                rules.RuleClause(
                    _all_equal(expected),
                    _anchored_result(replacements),
                )
            )
    zero_result = rules.NoSuccessorClauseResult(
        rules.NoSuccessorOutcome.TERMINAL,
        rules.literal_expr("no-active-loci"),
        rules.literal_expr("no-active-loci"),
        ("mechanics:no-active-loci",),
        _certificate(
            rules.CertificateKind.TERMINALITY,
            "terminal:no-active-loci",
        ),
    )
    rule = rules.anchored_clause_kernel(
        tuple(clauses),
        group_channel=0,
        zero_result=zero_result,
        contract=rules.RuleContract(
            source.contract,
            alphabet.value_profile,
            readable.result_shape,
            readable.join_shape,
            writable.effect_profile,
        ),
        completeness_evidence=_certificate(
            rules.CertificateKind.COMPLETENESS,
            "anchored-clause-kernel:complete",
        ),
        conflict_policy=conflict_policy,
        selection=rules.ClauseSelection.FIRST,
    )
    return multi_active_local_rewrite(
        seed=seeds.exact(source, value_profile=alphabet.value_profile),
        alphabet=alphabet,
        frontier=writable,
        neighborhood=readable,
        rule=rule,
    )


def _finite_grid_table_preset(
    *,
    shape: object,
    initial: object,
    colors: object,
    offsets: tuple[tuple[int, ...], ...],
    rule: object,
    boundary: object,
    axes: tuple[str, ...] | None,
    rank: int,
    label: str,
) -> SimpleProgram:
    resolved_shape = _shape(shape, rank=rank, label=f"{label} shape")
    size = _strict_positive_int(colors, label=f"{label} colors")
    if size < 2:
        raise ValueError(f"{label} colors must be at least two")
    values = _palette_values(
        initial,
        colors=size,
        count=prod(resolved_shape),
        label=f"{label} initial state",
    )
    table = _palette_values(
        rule,
        colors=size,
        count=size ** len(offsets),
        label=f"{label} rule table",
    )
    return _finite_table_program(
        shape=resolved_shape,
        initial=values,
        colors=size,
        offsets=offsets,
        table=table,
        boundary=_integer_boundary(boundary, colors=size, label=label),
        axes=axes,
    )


def cellular_automaton_2d(
    *,
    shape: tuple[int, int],
    initial: tuple[int, ...],
    colors: int,
    rule: tuple[int, ...],
    boundary: loci.Boundary[int] = _ZERO_INTEGER_BOUNDARY,
) -> SimpleProgram:
    """Construct a 2D von-Neumann cellular automaton.

    Its fixed declared table order is ``(-1,0), (0,-1), (0,0), (0,1),
    (1,0)``; the first value is the most-significant table digit.
    """

    return _finite_grid_table_preset(
        shape=shape,
        initial=initial,
        colors=colors,
        offsets=_VON_NEUMANN_2D,
        rule=rule,
        boundary=boundary,
        axes=("x", "y"),
        rank=2,
        label="cellular-automaton-2d",
    )


def moore_cellular_automaton(
    *,
    shape: tuple[int, int],
    initial: tuple[int, ...],
    colors: int,
    rule: tuple[int, ...],
    boundary: loci.Boundary[int] = _ZERO_INTEGER_BOUNDARY,
) -> SimpleProgram:
    """Construct a 2D radius-one Moore-neighborhood cellular automaton.

    The nine offsets use lexicographic order over ``(-1, 0, 1)²``.
    """

    return _finite_grid_table_preset(
        shape=shape,
        initial=initial,
        colors=colors,
        offsets=_MOORE_2D,
        rule=rule,
        boundary=boundary,
        axes=("x", "y"),
        rank=2,
        label="moore-cellular-automaton",
    )


def cellular_automaton_3d(
    *,
    shape: tuple[int, int, int],
    initial: tuple[int, ...],
    colors: int,
    offsets: tuple[tuple[int, int, int], ...],
    rule: tuple[int, ...],
    boundary: loci.Boundary[int] = _ZERO_INTEGER_BOUNDARY,
) -> SimpleProgram:
    """Construct a 3D finite-table cellular automaton on declared offsets."""

    resolved_offsets = _offsets(
        offsets,
        rank=3,
        label="3D cellular automaton offsets",
    )
    return _finite_grid_table_preset(
        shape=shape,
        initial=initial,
        colors=colors,
        offsets=resolved_offsets,
        rule=rule,
        boundary=boundary,
        axes=("x", "y", "z"),
        rank=3,
        label="cellular-automaton-3d",
    )


def lattice_cellular_automaton(
    *,
    shape: tuple[int, ...],
    initial: tuple[int, ...],
    colors: int,
    offsets: tuple[tuple[int, ...], ...],
    rule: tuple[int, ...],
    boundary: loci.Boundary[int] = _ZERO_INTEGER_BOUNDARY,
    axes: tuple[str, ...] | None = None,
) -> SimpleProgram:
    """Construct a finite-table cellular automaton on a rank-N lattice."""

    resolved_shape = _shape(shape, rank=None, label="lattice shape")
    resolved_axes = _axes(axes, rank=len(resolved_shape))
    resolved_offsets = _offsets(
        offsets,
        rank=len(resolved_shape),
        label="lattice offsets",
    )
    return _finite_grid_table_preset(
        shape=resolved_shape,
        initial=initial,
        colors=colors,
        offsets=resolved_offsets,
        rule=rule,
        boundary=boundary,
        axes=resolved_axes,
        rank=len(resolved_shape),
        label="lattice-cellular-automaton",
    )


def _single_state_program(
    *,
    initial: alphabets.SemanticValue,
    alphabet: alphabets.Alphabet,
    expression: rules.RuleExpr,
) -> SimpleProgram:
    if type(alphabet) is not alphabets.Alphabet:
        raise TypeError("single-state alphabet must be an Alphabet")
    if type(expression) is not rules.RuleExpr:
        raise TypeError("single-state expression must be a RuleExpr")
    alphabet.require(initial)
    source = loci.record_configuration((("state", initial),))
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    rule = rules.expression(
        rules.ExistingPlan(
            rules.ExistingPlanKind.BY_INDEX,
            (expression,),
        ),
        contract=rules.RuleContract(
            source.contract,
            alphabet.value_profile,
            readable.result_shape,
            readable.join_shape,
            writable.effect_profile,
        ),
        witness=rules.literal_expr("expression-replacement"),
        provenance=("mechanics:expression-replacement",),
    )
    return iterated_map(
        seed=seeds.exact(source, value_profile=alphabet.value_profile),
        alphabet=alphabet,
        frontier=writable,
        neighborhood=readable,
        rule=rule,
    )


def arithmetic_iteration(
    *,
    initial: alphabets.SemanticValue,
    alphabet: alphabets.Alphabet,
    map_expression: rules.RuleExpr,
) -> SimpleProgram:
    """Iterate one closed exact arithmetic expression over ``observation(0)``."""

    return _single_state_program(
        initial=initial,
        alphabet=alphabet,
        expression=map_expression,
    )


def piecewise_integer_map(
    *,
    initial: int,
    cases: tuple[tuple[int, int, rules.RuleExpr], ...],
    otherwise: rules.RuleExpr,
) -> SimpleProgram:
    """Construct an integer map from ordered residue cases and a total fallback."""

    if type(initial) is not int:
        raise TypeError("piecewise integer initial value must be an integer")
    if type(cases) is not tuple:
        raise TypeError("piecewise integer cases must be an immutable tuple")
    if not cases:
        raise ValueError("piecewise integer map needs at least one case")
    if type(otherwise) is not rules.RuleExpr:
        raise TypeError("piecewise integer fallback must be a RuleExpr")
    expression = otherwise
    for entry in reversed(cases):
        if type(entry) is not tuple or len(entry) != 3:
            raise TypeError("each piecewise integer case must be a triple")
        modulus, residue, case_expression = entry
        if type(modulus) is not int:
            raise TypeError("piecewise integer modulus must be an integer")
        if modulus <= 0:
            raise ValueError("piecewise integer modulus must be positive")
        if type(residue) is not int:
            raise TypeError("piecewise integer residue must be an integer")
        if residue < 0 or residue >= modulus:
            raise ValueError("piecewise integer residue must lie in range(modulus)")
        if type(case_expression) is not rules.RuleExpr:
            raise TypeError("piecewise integer branch must be a RuleExpr")
        expression = rules.conditional(
            rules.equal(
                rules.modulo(rules.observation(0), modulus),
                rules.literal_expr(residue),
            ),
            case_expression,
            expression,
        )
    return _single_state_program(
        initial=initial,
        alphabet=alphabets.integers(),
        expression=expression,
    )


def digit_reversal_map(
    *,
    initial: int,
    base: int = 2,
) -> SimpleProgram:
    """Construct the reverse-add map in the declared integer base."""

    if type(initial) is not int:
        raise TypeError("digit-reversal initial value must be an integer")
    if initial < 0:
        raise ValueError("digit-reversal initial value must be nonnegative")
    resolved_base = _strict_positive_int(base, label="digit-reversal base")
    if resolved_base < 2:
        raise ValueError("digit-reversal base must be at least two")
    source = rules.observation(0)
    reversed_value = rules.from_digits(
        rules.reverse(rules.integer_digits(source, resolved_base)),
        resolved_base,
    )
    return _single_state_program(
        initial=initial,
        alphabet=alphabets.naturals(),
        expression=rules.add(source, reversed_value),
    )


def continuous_cellular_automaton(
    *,
    initial: tuple[Fraction, ...],
    local_rule: rules.RuleExpr,
    radius: int = 1,
    boundary: loci.Boundary[Fraction] = _ZERO_RATIONAL_BOUNDARY,
) -> SimpleProgram:
    """Construct an exact rational-valued local automaton on ``[0, 1]``."""

    if type(initial) is not tuple:
        raise TypeError("continuous cellular initial state must be a tuple")
    if not initial:
        raise ValueError("continuous cellular initial state cannot be empty")
    if any(type(value) is not Fraction for value in initial):
        raise TypeError("continuous cellular values must be exact Fractions")
    if any(value < 0 or value > 1 for value in initial):
        raise ValueError("continuous cellular values must lie in [0, 1]")
    if type(local_rule) is not rules.RuleExpr:
        raise TypeError("continuous cellular local rule must be a RuleExpr")
    resolved_radius = _strict_positive_int(radius, label="continuous radius")
    if type(boundary) is not loci.Boundary:
        raise TypeError("continuous cellular boundary must be a Boundary")
    if boundary.policy is loci.BoundaryPolicy.FIXED and (
        type(boundary.exterior) is not Fraction
        or boundary.exterior < 0
        or boundary.exterior > 1
    ):
        raise ValueError(
            "continuous cellular fixed exterior must be a Fraction in [0, 1]"
        )
    offsets = tuple((offset,) for offset in range(-resolved_radius, resolved_radius + 1))
    return _grid_expression_program(
        shape=(len(initial),),
        initial=initial,
        alphabet=alphabets.rational_interval(Fraction(0), Fraction(1)),
        offsets=offsets,
        expression=local_rule,
        boundary=boundary,
        axes=("x",),
    )


def eca(
    *,
    rule: int = 30,
    width: int = 79,
) -> SimpleProgram[
    loci.FiniteConfiguration[bool],
    bool,
    frontiers.WritableCapabilities,
    neighborhoods.ReadableView[bool],
]:
    """Construct a finite binary radius-one cellular automaton."""

    if type(width) is not int:
        raise TypeError("ECA width must be an integer")
    if width <= 0:
        raise ValueError("ECA width must be positive")
    carrier = loci.CarrierContract(
        loci.CarrierKind.GRID,
        rank=1,
        shape=(width,),
        axes=("x",),
    )
    value_schema = alphabets.boolean()
    boundary = loci.Boundary(loci.BoundaryPolicy.FIXED, False)
    initial = seeds.bernoulli(
        loci.literal(loci.grid_loci((width,), axes=("x",))),
        Fraction(1, 2),
        configuration_contract=carrier,
        value_profile=value_schema.value_profile,
        boundary=boundary,
    )
    return synchronous_local_state_transform(
        seed=initial,
        alphabet=value_schema,
        frontier=frontiers.everywhere(
            configuration_contract=carrier,
            value_profile=value_schema.value_profile,
        ),
        neighborhood=neighborhoods.eca(
            configuration_contract=carrier,
            value_profile=value_schema.value_profile,
        ),
        rule=rules.elementary(rule),
    )


# ---------------------------------------------------------------------------
# Phase 3. True aliases
# ---------------------------------------------------------------------------


def elementary_cellular_automaton(
    *,
    rule: int = 30,
    width: int = 79,
) -> SimpleProgram[
    loci.FiniteConfiguration[bool],
    bool,
    frontiers.WritableCapabilities,
    neighborhoods.ReadableView[bool],
]:
    """Return the exact alternate spelling of :func:`eca`."""

    return eca(rule=rule, width=width)

__all__ = (
    "alternating_partition_local_evolution",
    "asynchronous_local_state_automaton",
    "coupled_field_mobile_locus_evolution",
    "driven_relaxation",
    "history_dependent_agent_game",
    "iterated_map",
    "multi_active_local_rewrite",
    "mutable_rule_local_automaton",
    "population_evolutionary_search",
    "synchronous_local_state_transform",
    "weighted_network_state_update",
    "arithmetic_iteration",
    "cellular_automaton_2d",
    "cellular_automaton_3d",
    "continuous_cellular_automaton",
    "digit_reversal_map",
    "eca",
    "elementary_cellular_automaton",
    "generalized_mobile_automaton",
    "higher_color_totalistic_cellular_automaton",
    "lattice_cellular_automaton",
    "moore_cellular_automaton",
    "multicolor_cellular_automaton",
    "piecewise_integer_map",
    "quiescent_cellular_automaton",
    "symmetric_cellular_automaton",
    "three_color_totalistic_cellular_automaton",
    "totalistic_cellular_automaton",
)
