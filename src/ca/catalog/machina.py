"""Ordinary five-component constructors for controllers and machines.

Canonical family names assemble already-closed components into
:class:`~ca.program.SimpleProgram` values.  They attach no family identity,
perform no execution dispatch, and contain no hidden interpreter.
"""

from __future__ import annotations

from typing import TypeVar

from .. import alphabets, frontiers, neighborhoods, rules, seeds
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

# Spelling and SPF target only; these tuples do not settle signatures.
_PENDING_PRESETS: tuple[tuple[str, str], ...] = (
    ("mobile_automaton", "SPF030"),
    ("neighbor_updating_mobile_automaton", "SPF030"),
    ("turing_machine", "SPF030"),
    ("turing_machine_2d", "SPF030"),
)


# ---------------------------------------------------------------------------
# Phase 3. True aliases
# ---------------------------------------------------------------------------

_PENDING_ALIASES: tuple[tuple[str, str], ...] = ()


# ---------------------------------------------------------------------------
# Phase 4. Compatibility adapters
# ---------------------------------------------------------------------------

# The sole K spelling is category-qualified and deprecated.  Its exact legacy
# argument domain is unsettled, so this is deliberately not a callable.
_PENDING_COMPATIBILITY: tuple[tuple[str, str], ...] = (
    (
        "extended_mobile_automaton",
        "neighbor_updating_mobile_automaton / SPF030",
    ),
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
)
