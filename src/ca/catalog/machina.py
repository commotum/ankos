"""Whole-program constructors for visible controllers and machines.

This module owns audited constructions driven by a head, instruction,
register, traversal, stack, or explicit controller.  It does not own machine
execution branches, component mechanics, metadata, hidden evaluation, or
application.  Goal 7 implementations will encode control as visible
configuration data and return ordinary five-field ``SimpleProgram`` values.

Canonical signatures come directly from the migration matrix.  Unsettled
presets and the sole compatibility adapter remain private inert inventories.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

if TYPE_CHECKING:
    from ..program import SimpleProgram


def _not_implemented() -> NoReturn:
    """Raise the uniform catalog-skeleton error."""

    raise NotImplementedError("catalog construction is not implemented in this scaffold")


# ---------------------------------------------------------------------------
# Phase 1. Canonical families
# ---------------------------------------------------------------------------


def enumerative_semidecision(
    *,
    query,
    enumeration,
    predicate,
    start,
) -> SimpleProgram:
    """SPF010 / F011: enumerate until the first witnessed positive answer."""

    _not_implemented()


def finite_gate_circuit(
    *,
    inputs,
    wiring,
    gates,
    schedule,
    measurement,
) -> SimpleProgram:
    """SPF013 / F014: apply fixed wiring and visible gate-layer control."""

    _not_implemented()


def mobile_head_grid_rewrite(
    *,
    tape,
    transitions,
    head,
    stencil,
    boundary,
) -> SimpleProgram:
    """SPF030 / F031: atomically rewrite a tagged head and its destination."""

    _not_implemented()


def nearest_neighbor_retrieval(
    *,
    items,
    query,
    metric,
    index,
    traversal,
) -> SimpleProgram:
    """SPF035 / F036: traverse an index and return every nearest witness."""

    _not_implemented()


def recursive_function_evaluator(
    *,
    call,
    definitions,
    evaluation_order,
    cache,
) -> SimpleProgram:
    """SPF044 / F047: reduce recursive calls with visible frames and cache."""

    _not_implemented()


def register_machine(
    *,
    program,
    registers,
    entry,
) -> SimpleProgram:
    """SPF045 / F048: commit one fetched register instruction atomically."""

    _not_implemented()


def stored_program_random_access_machine(
    *,
    memory,
    entry,
    instruction_set,
) -> SimpleProgram:
    """SPF048 / F051: execute visible writable code and indirect memory."""

    _not_implemented()


def priority_dovetailed_oracle_construction(
    *,
    approximations,
    machines,
    requirements,
    priority,
    fair_schedule,
) -> SimpleProgram:
    """SPF053 / F056: dovetail work with explicit priority and injury state."""

    _not_implemented()


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
