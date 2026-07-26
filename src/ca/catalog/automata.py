"""Whole-program constructors for persistent-carrier automata.

This module owns the audited catalog spellings whose dominant mechanic is
in-place or shared-generation evolution on a persistent carrier.  It does not
own component mechanics, application, metadata, execution dispatch, or
serialization.  Goal 7 implementations will compose values from ``seeds``,
``alphabets``, ``frontiers``, ``neighborhoods``, and ``rules`` into
``SimpleProgram`` values consumed by ``ca.apply``.

Only matrix-authorized canonical signatures are declared here.  Preset and
alias spellings whose signatures remain unsettled are recorded as private
non-authoritative inventories rather than exposed as fake callables.
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


def alternating_partition_local_evolution(
    *,
    seed,
    partition,
    block_law,
    boundary,
    phase,
) -> SimpleProgram:
    """SPF001 / F001: evolve alternating disjoint partitions atomically."""

    _not_implemented()


def asynchronous_local_state_automaton(
    *,
    seed,
    local_law,
    schedule,
    boundary,
) -> SimpleProgram:
    """SPF003 / F003: apply scheduled local writes with immediate visibility."""

    _not_implemented()


def coupled_field_mobile_locus_evolution(
    *,
    seed,
    field_law,
    mobile_law,
    boundary,
) -> SimpleProgram:
    """SPF007 / F007: couple a distributed field update to one mobile locus."""

    _not_implemented()


def driven_relaxation(
    *,
    seed,
    drive_law,
    toppling_law,
    boundary,
    relaxation_form,
) -> SimpleProgram:
    """SPF009 / F009: drive a stable field and expose its relaxation closure."""

    _not_implemented()


def history_dependent_agent_game(
    *,
    agents,
    histories,
    payoff,
    action_schema,
    round_control,
) -> SimpleProgram:
    """SPF021 / F022: commit coupled agent actions, histories, and payoffs."""

    _not_implemented()


def iterated_map(
    *,
    seed,
    map_expression,
    guards,
    terminal_condition,
) -> SimpleProgram:
    """SPF026 / F027: replace an exact tuple by one guarded map image."""

    _not_implemented()


def multi_active_local_rewrite(
    *,
    seed,
    local_law,
    collision_law,
    schedule,
) -> SimpleProgram:
    """SPF032 / F033: evolve a finite active set with explicit collisions."""

    _not_implemented()


def mutable_rule_local_automaton(
    *,
    seed,
    rule_program,
    interpreter,
    mutation_law,
) -> SimpleProgram:
    """SPF034 / F035: evolve carrier state and visible rule-program state."""

    _not_implemented()


def population_evolutionary_search(
    *,
    population,
    fitness_expression,
    selection,
    recombination,
    mutation,
    size,
) -> SimpleProgram:
    """SPF040 / F043: replace a scored population by one evolved generation."""

    _not_implemented()


def synchronous_local_state_transform(
    *,
    seed,
    stencil,
    local_law,
    boundary,
    feedback,
) -> SimpleProgram:
    """SPF050 / F053: apply one shared local law to an old-state snapshot."""

    _not_implemented()


def weighted_network_state_update(
    *,
    network,
    seed,
    weights,
    schedule,
    learning_law,
) -> SimpleProgram:
    """SPF052 / F055: update network activations and optional visible weights."""

    _not_implemented()


# ---------------------------------------------------------------------------
# Phase 2. Presets
# ---------------------------------------------------------------------------

# Spelling and SPF target only.  These are not callable declarations, do not
# settle parameter surfaces, and are intentionally omitted from ``__all__``.
_PENDING_PRESETS: tuple[tuple[str, str], ...] = (
    ("eca", "SPF050"),
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


# ---------------------------------------------------------------------------
# Phase 3. True aliases
# ---------------------------------------------------------------------------

# The alias must eventually copy the still-unsettled ``eca`` signature.
_PENDING_ALIASES: tuple[tuple[str, str], ...] = (
    ("elementary_cellular_automaton", "eca / SPF050"),
)


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
)
