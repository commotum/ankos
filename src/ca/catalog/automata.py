"""Ordinary five-component constructors for persistent-carrier automata.

Canonical family names are typed, family-blind assembly functions: they
validate only through :class:`~ca.program.SimpleProgram` and attach no catalog
identity or alternate execution behavior.  Concrete presets bind those same
five components explicitly.
"""

from __future__ import annotations

from fractions import Fraction
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

# Remaining spelling/SPF inventory only. These names stay non-callable until
# their concrete component bindings are settled.
_PENDING_PRESETS: tuple[tuple[str, str], ...] = (
    ("multicolor_cellular_automaton", "SPF050"),
    ("totalistic_cellular_automaton", "SPF050"),
    ("three_color_totalistic_cellular_automaton", "SPF050"),
    ("higher_color_totalistic_cellular_automaton", "SPF050"),
    ("quiescent_cellular_automaton", "SPF050"),
    ("symmetric_cellular_automaton", "SPF050"),
    ("generalized_mobile_automaton", "SPF032"),
    ("cellular_automaton_2d", "SPF050"),
    ("moore_cellular_automaton", "SPF050"),
    ("cellular_automaton_3d", "SPF050"),
    ("lattice_cellular_automaton", "SPF050"),
    ("arithmetic_iteration", "SPF026"),
    ("piecewise_integer_map", "SPF026"),
    ("digit_reversal_map", "SPF026"),
    ("continuous_cellular_automaton", "SPF050"),
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


# ---------------------------------------------------------------------------
# Phase 4. Compatibility adapters
# ---------------------------------------------------------------------------

_PENDING_COMPATIBILITY: tuple[tuple[str, str], ...] = ()


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
    "eca",
    "elementary_cellular_automaton",
)
