"""Whole-program constructors for structural substitution and growth.

This module owns audited catalog spellings whose dominant mechanic matches,
replaces, grows, deletes, or branches structure.  It does not own structural
identity primitives, component mechanics, metadata, application, conflict
repair, or execution dispatch.  Goal 7 implementations will compose the five
component algebras into ordinary ``SimpleProgram`` values.

Canonical declarations follow the settled matrix exactly.  Presets with
unsettled Python signatures remain inert private inventory; only true aliases
whose signatures are identical to canonical delegates are scaffolded.
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


def append_only_sequence_generation(
    *,
    seed,
    emitter,
    control_schema,
    support,
) -> SimpleProgram:
    """SPF002 / F002: append finite output while preserving prior support."""

    _not_implemented()


def context_dependent_substitution(
    *,
    seed,
    productions,
    context_shape,
    boundary,
) -> SimpleProgram:
    """SPF005 / F005: replace items from bounded old-generation context."""

    _not_implemented()


def first_passage_aggregation(
    *,
    seed,
    walk_law,
    contact,
    release,
    boundary,
    target,
) -> SimpleProgram:
    """SPF015 / F016: attach a walker irreversibly at first contact."""

    _not_implemented()


def front_delete_rear_append_system(
    *,
    seed,
    deletion_width,
    productions,
    phase_cycle,
) -> SimpleProgram:
    """SPF016 / F017: delete a prefix and append its selected production."""

    _not_implemented()


def global_score_sequential_placement(
    *,
    seed,
    score_expression,
    placement_shape,
    depletion_kernel,
    tie_law,
) -> SimpleProgram:
    """SPF019 / F020: score globally and commit one structural placement."""

    _not_implemented()


def history_dependent_growth_rewrite(
    *,
    seed,
    eligibility,
    provenance_law,
    boundary,
) -> SimpleProgram:
    """SPF022 / F023: grow support using occupancy and provenance history."""

    _not_implemented()


def indexed_history_recurrence(
    *,
    prefix,
    recurrence,
    index_law,
    invalidity,
) -> SimpleProgram:
    """SPF023 / F024: append a term read through value-addressed history."""

    _not_implemented()


def iterated_erasure_process(
    *,
    seed,
    erasure_predicate,
    rank_convention,
) -> SimpleProgram:
    """SPF025 / F026: repeatedly erase selected ranked survivors."""

    _not_implemented()


def local_graph_rewrite(
    *,
    seed,
    patterns,
    replacements,
    match_schedule,
    interface_schema,
) -> SimpleProgram:
    """SPF028 / F029: replace graph matches through explicit interfaces."""

    _not_implemented()


def moving_frontier_shell_accretion(
    *,
    seed,
    strip_constructor,
    rim_law,
    geometry,
    terminal_condition,
) -> SimpleProgram:
    """SPF031 / F032: append geometric strips along a moving open rim."""

    _not_implemented()


def multiway_rewrite(
    *,
    seed,
    rewrites,
    match_semantics,
    quotient,
) -> SimpleProgram:
    """SPF033 / F034: expose every witnessed successor before quotienting."""

    _not_implemented()


def parallel_independent_substitution(
    *,
    seed,
    productions,
    schedule,
    geometry,
) -> SimpleProgram:
    """SPF037 / F038: assemble independent offspring in one generation."""

    _not_implemented()


def parallel_network_rewrite(
    *,
    seed,
    patches,
    port_schema,
    overlap_law,
) -> SimpleProgram:
    """SPF038 / F040: commit compatible graph patches in parallel."""

    _not_implemented()


def random_functional_graph_construction(
    *,
    nodes,
    successor_measure,
) -> SimpleProgram:
    """SPF043 / F046: denote a random one-successor graph construction."""

    _not_implemented()


def structural_pattern_rewrite(
    *,
    expression,
    patterns,
    replacements,
    scan,
    nonoverlap,
) -> SimpleProgram:
    """SPF049 / F052: rewrite structural matches with explicit scan conflicts."""

    _not_implemented()


# ---------------------------------------------------------------------------
# Phase 2. Presets
# ---------------------------------------------------------------------------

# Spelling and SPF target only; these tuples do not settle signatures.
_PENDING_PRESETS: tuple[tuple[str, str], ...] = (
    ("constant_digit_sequence", "SPF002"),
    ("neighbor_dependent_substitution", "SPF005"),
    ("context_dependent_substitution_2d", "SPF005"),
    ("tag_system", "SPF016"),
    ("cyclic_tag_system", "SPF016"),
    ("recursive_sequence", "SPF023"),
    ("variable_index_recursive_sequence", "SPF023"),
    ("number_theoretic_filtering", "SPF025"),
    ("neighbor_independent_substitution", "SPF037"),
    ("creation_destruction_substitution", "SPF037"),
    ("substitution_system_2d", "SPF037"),
    ("geometric_substitution", "SPF037"),
    ("continued_fraction_substitution", "SPF037"),
    ("sequential_substitution", "SPF049"),
    ("symbolic_system", "SPF049"),
)


# ---------------------------------------------------------------------------
# Phase 3. True aliases
# ---------------------------------------------------------------------------


def multiway_system(
    *,
    seed,
    rewrites,
    match_semantics,
    quotient,
) -> SimpleProgram:
    """A alias for SPF033 with the exact ``multiway_rewrite`` signature."""

    _not_implemented()


def network_rewrite(
    *,
    seed,
    patches,
    port_schema,
    overlap_law,
) -> SimpleProgram:
    """A alias for SPF038 with the exact canonical network signature."""

    _not_implemented()


_PENDING_ALIASES: tuple[tuple[str, str], ...] = ()


# ---------------------------------------------------------------------------
# Phase 4. Compatibility adapters
# ---------------------------------------------------------------------------

_PENDING_COMPATIBILITY: tuple[tuple[str, str], ...] = ()


__all__ = (
    "append_only_sequence_generation",
    "context_dependent_substitution",
    "first_passage_aggregation",
    "front_delete_rear_append_system",
    "global_score_sequential_placement",
    "history_dependent_growth_rewrite",
    "indexed_history_recurrence",
    "iterated_erasure_process",
    "local_graph_rewrite",
    "moving_frontier_shell_accretion",
    "multiway_rewrite",
    "multiway_system",
    "network_rewrite",
    "parallel_independent_substitution",
    "parallel_network_rewrite",
    "random_functional_graph_construction",
    "structural_pattern_rewrite",
)
