"""Whole-program constructors defined by admissibility and solutions.

This module owns audited constructions whose result is defined by constraints,
objectives, witnesses, solution relations, or weighted alternatives.  It does
not own solver policy, searches hidden inside application, component
mechanics, metadata, or numerical realization.  Goal 7 implementations will
encode defining relations as closed Rule data and return ordinary
``SimpleProgram`` values.

Canonical constructors expose the five component values directly.  The
migration matrix's semantic parameter lists remain descriptive metadata;
catalog construction never interprets a parallel recipe language.  Unsettled
legacy presets are retained only as private spelling-to-family inventory.
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


def finite_model_satisfaction(
    *,
    seed: seeds.Seed,
    alphabet: alphabets.Alphabet,
    frontier: frontiers.WritableRegion,
    neighborhood: neighborhoods.ReadableRegion,
    rule: rules.Rule,
) -> SimpleProgram:
    """SPF014 / F015: denote every finite interpretation satisfying axioms."""

    return _program(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def geometric_embedding_relation(
    *,
    seed: seeds.Seed,
    alphabet: alphabets.Alphabet,
    frontier: frontiers.WritableRegion,
    neighborhood: neighborhoods.ReadableRegion,
    rule: rules.Rule,
) -> SimpleProgram:
    """SPF017 / F018: denote valid embeddings under global metric constraints."""

    return _program(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def global_equation_relation(
    *,
    seed: seeds.Seed,
    alphabet: alphabets.Alphabet,
    frontier: frontiers.WritableRegion,
    neighborhood: neighborhoods.ReadableRegion,
    rule: rules.Rule,
) -> SimpleProgram:
    """SPF018 / F019: denote every exact completion solving an equation."""

    return _program(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def inverse_local_system_reconstruction(
    *,
    seed: seeds.Seed,
    alphabet: alphabets.Alphabet,
    frontier: frontiers.WritableRegion,
    neighborhood: neighborhoods.ReadableRegion,
    rule: rules.Rule,
) -> SimpleProgram:
    """SPF024 / F025: reconstruct unknowns with witnessed branch and prune."""

    return _program(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def local_factor_weighted_relation(
    *,
    seed: seeds.Seed,
    alphabet: alphabets.Alphabet,
    frontier: frontiers.WritableRegion,
    neighborhood: neighborhoods.ReadableRegion,
    rule: rules.Rule,
) -> SimpleProgram:
    """SPF027 / F028: combine overlapping factors into weighted completions."""

    return _program(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def local_satisfaction_relation(
    *,
    seed: seeds.Seed,
    alphabet: alphabets.Alphabet,
    frontier: frontiers.WritableRegion,
    neighborhood: neighborhoods.ReadableRegion,
    rule: rules.Rule,
) -> SimpleProgram:
    """SPF029 / F030: denote jointly satisfying local-template completions."""

    return _program(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def program_randomization_test(
    *,
    seed: seeds.Seed,
    alphabet: alphabets.Alphabet,
    frontier: frontiers.WritableRegion,
    neighborhood: neighborhoods.ReadableRegion,
    rule: rules.Rule,
) -> SimpleProgram:
    """SPF042 / F045: compare observed data with replayable surrogate results."""

    return _program(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def stochastic_local_search(
    *,
    seed: seeds.Seed,
    alphabet: alphabets.Alphabet,
    frontier: frontiers.WritableRegion,
    neighborhood: neighborhoods.ReadableRegion,
    rule: rules.Rule,
) -> SimpleProgram:
    """SPF047 / F050: propose and accept stochastic incumbent replacements."""

    return _program(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def weighted_history_sum_relation(
    *,
    seed: seeds.Seed,
    alphabet: alphabets.Alphabet,
    frontier: frontiers.WritableRegion,
    neighborhood: neighborhoods.ReadableRegion,
    rule: rules.Rule,
) -> SimpleProgram:
    """SPF051 / F054: denote an exact weighted sum over admissible histories."""

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
