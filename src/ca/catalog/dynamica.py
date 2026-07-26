"""Whole-program constructors for continuous and differential relations.

This module owns audited constructions defined by continuous flow, event, or
differential-field laws.  It does not own numerical solvers, integration
policy, component mechanics, metadata, application dispatch, or sampled
approximations.  Goal 7 implementations will compose exact or intensional
five-field ``SimpleProgram`` values whose realizations remain external.

The three canonical constructors expose the five component values directly.
The migration matrix's semantic parameter lists remain descriptive metadata.
The one true alias copies its canonical delegate's exact parameter surface.
"""

from __future__ import annotations

from .. import alphabets, frontiers, neighborhoods, rules, seeds
from ..program import SimpleProgram


def _program(
    *,
    seed: seeds.Seed,
    alphabet: alphabets.Alphabet,
    frontier: frontiers.WritableRegion,
    neighborhood: neighborhoods.ReadableRegion,
    rule: rules.Rule,
) -> SimpleProgram:
    """Compose one ordinary catalog-free program value."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


# ---------------------------------------------------------------------------
# Phase 1. Canonical families
# ---------------------------------------------------------------------------


def continuous_event_dynamics(
    *,
    seed: seeds.Seed,
    alphabet: alphabets.Alphabet,
    frontier: frontiers.WritableRegion,
    neighborhood: neighborhoods.ReadableRegion,
    rule: rules.Rule,
) -> SimpleProgram:
    """SPF006 / F006: flow to an intrinsic event and apply its reset."""

    return _program(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def ordinary_differential_flow(
    *,
    seed: seeds.Seed,
    alphabet: alphabets.Alphabet,
    frontier: frontiers.WritableRegion,
    neighborhood: neighborhoods.ReadableRegion,
    rule: rules.Rule,
) -> SimpleProgram:
    """SPF036 / F037: denote a selected or maximal ordinary flow segment."""

    return _program(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def partial_differential_relation(
    *,
    seed: seeds.Seed,
    alphabet: alphabets.Alphabet,
    frontier: frontiers.WritableRegion,
    neighborhood: neighborhoods.ReadableRegion,
    rule: rules.Rule,
) -> SimpleProgram:
    """SPF039 / F041: denote every field satisfying a differential relation."""

    return _program(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


# ---------------------------------------------------------------------------
# Phase 2. Presets
# ---------------------------------------------------------------------------

_PENDING_PRESETS: tuple[tuple[str, str], ...] = ()


# ---------------------------------------------------------------------------
# Phase 3. True aliases
# ---------------------------------------------------------------------------


def pde(
    *,
    seed: seeds.Seed,
    alphabet: alphabets.Alphabet,
    frontier: frontiers.WritableRegion,
    neighborhood: neighborhoods.ReadableRegion,
    rule: rules.Rule,
) -> SimpleProgram:
    """An alias for SPF039 with the canonical differential-relation signature."""

    return partial_differential_relation(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


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
