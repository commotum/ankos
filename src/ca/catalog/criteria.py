"""Whole-program constructors defined by admissibility and solutions.

This module owns audited constructions whose result is defined by constraints,
objectives, witnesses, solution relations, or weighted alternatives.  It does
not own solver policy, searches hidden inside application, component
mechanics, metadata, or numerical realization.  Goal 7 implementations will
encode defining relations as closed Rule data and return ordinary
``SimpleProgram`` values.

Canonical signatures follow the migration matrix exactly.  Unsettled legacy
presets are retained only as private spelling-to-family inventory.
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


def finite_model_satisfaction(
    *,
    axioms,
    finite_domain,
    signatures,
    fixed_tables,
) -> SimpleProgram:
    """SPF014 / F015: denote every finite interpretation satisfying axioms."""

    _not_implemented()


def geometric_embedding_relation(
    *,
    mesh,
    growth,
    metric_constraints,
    boundary_embedding,
) -> SimpleProgram:
    """SPF017 / F018: denote valid embeddings under global metric constraints."""

    _not_implemented()


def global_equation_relation(
    *,
    equation,
    domain,
    known_assignments,
    witness_schema,
) -> SimpleProgram:
    """SPF018 / F019: denote every exact completion solving an equation."""

    _not_implemented()


def inverse_local_system_reconstruction(
    *,
    observations,
    local_law,
    boundary,
    unknown_schema,
    search_order,
) -> SimpleProgram:
    """SPF024 / F025: reconstruct unknowns with witnessed branch and prune."""

    _not_implemented()


def local_factor_weighted_relation(
    *,
    seed,
    factors,
    reduction,
    normalization,
    objective,
) -> SimpleProgram:
    """SPF027 / F028: combine overlapping factors into weighted completions."""

    _not_implemented()


def local_satisfaction_relation(
    *,
    partial_assignment,
    templates,
    boundary,
    obligations,
) -> SimpleProgram:
    """SPF029 / F030: denote jointly satisfying local-template completions."""

    _not_implemented()


def program_randomization_test(
    *,
    observed,
    surrogate_law,
    program,
    statistic,
    replicates,
    calibration,
) -> SimpleProgram:
    """SPF042 / F045: compare observed data with replayable surrogate results."""

    _not_implemented()


def stochastic_local_search(
    *,
    incumbent,
    objective,
    constraints,
    proposal,
    acceptance,
) -> SimpleProgram:
    """SPF047 / F050: propose and accept stochastic incumbent replacements."""

    _not_implemented()


def weighted_history_sum_relation(
    *,
    domain,
    side_data,
    histories,
    action,
    measure,
    observables,
) -> SimpleProgram:
    """SPF051 / F054: denote an exact weighted sum over admissible histories."""

    _not_implemented()


# ---------------------------------------------------------------------------
# Phase 2. Presets
# ---------------------------------------------------------------------------

# T32 is intentionally a preset rather than a true alias.
_PENDING_PRESETS: tuple[tuple[str, str], ...] = (
    ("local_constraint_system", "SPF029"),
    ("template_constraint_system", "SPF029"),
    ("seeded_template_constraint_system", "SPF029"),
)


# ---------------------------------------------------------------------------
# Phase 3. True aliases
# ---------------------------------------------------------------------------

_PENDING_ALIASES: tuple[tuple[str, str], ...] = ()


# ---------------------------------------------------------------------------
# Phase 4. Compatibility adapters
# ---------------------------------------------------------------------------

_PENDING_COMPATIBILITY: tuple[tuple[str, str], ...] = ()


__all__ = (
    "finite_model_satisfaction",
    "geometric_embedding_relation",
    "global_equation_relation",
    "inverse_local_system_reconstruction",
    "local_factor_weighted_relation",
    "local_satisfaction_relation",
    "program_randomization_test",
    "stochastic_local_search",
    "weighted_history_sum_relation",
)
