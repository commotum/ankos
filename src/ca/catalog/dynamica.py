"""Whole-program constructors for continuous and differential relations.

This module owns audited constructions defined by continuous flow, event, or
differential-field laws.  It does not own numerical solvers, integration
policy, component mechanics, metadata, application dispatch, or sampled
approximations.  Goal 7 implementations will compose exact or intensional
five-field ``SimpleProgram`` values whose realizations remain external.

The three canonical signatures come directly from the migration matrix.  The
one true alias copies its canonical delegate's exact parameter surface.
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


def continuous_event_dynamics(
    *,
    seed,
    geometry,
    flow_law,
    reset_law,
    terminal_condition,
) -> SimpleProgram:
    """SPF006 / F006: flow to an intrinsic event and apply its reset."""

    _not_implemented()


def ordinary_differential_flow(
    *,
    seed,
    rhs,
    parameters,
    duration_or_event,
) -> SimpleProgram:
    """SPF036 / F037: denote a selected or maximal ordinary flow segment."""

    _not_implemented()


def partial_differential_relation(
    *,
    domain,
    coefficients,
    differential_relation,
    side_data,
) -> SimpleProgram:
    """SPF039 / F041: denote every field satisfying a differential relation."""

    _not_implemented()


# ---------------------------------------------------------------------------
# Phase 2. Presets
# ---------------------------------------------------------------------------

_PENDING_PRESETS: tuple[tuple[str, str], ...] = ()


# ---------------------------------------------------------------------------
# Phase 3. True aliases
# ---------------------------------------------------------------------------


def pde(
    *,
    domain,
    coefficients,
    differential_relation,
    side_data,
) -> SimpleProgram:
    """A alias for SPF039 with the canonical differential-relation signature."""

    _not_implemented()


_PENDING_ALIASES: tuple[tuple[str, str], ...] = ()


# ---------------------------------------------------------------------------
# Phase 4. Compatibility adapters
# ---------------------------------------------------------------------------

_PENDING_COMPATIBILITY: tuple[tuple[str, str], ...] = ()


__all__ = (
    "continuous_event_dynamics",
    "ordinary_differential_flow",
    "partial_differential_relation",
    "pde",
)
