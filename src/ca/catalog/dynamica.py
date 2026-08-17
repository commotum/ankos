"""Whole-program constructors for continuous and differential relations.

This module retains the source-facing contracts for continuous flow, event,
and differential-field builders.  They remain explicit progress stubs until
their exact descriptor languages and lowerings are implemented.
"""

from __future__ import annotations

from typing import NoReturn

from ..program import SimpleProgram


def _not_implemented() -> NoReturn:
    """Mark one canonical family builder as unfinished."""

    raise NotImplementedError("canonical family builder is not implemented")


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
# Phase 3. True aliases
# ---------------------------------------------------------------------------


def pde(
    *,
    domain,
    coefficients,
    differential_relation,
    side_data,
) -> SimpleProgram:
    """An alias for SPF039 with the canonical differential-relation signature."""

    return partial_differential_relation(
        domain=domain,
        coefficients=coefficients,
        differential_relation=differential_relation,
        side_data=side_data,
    )


__all__ = (
    "continuous_event_dynamics",
    "ordinary_differential_flow",
    "partial_differential_relation",
    "pde",
)
