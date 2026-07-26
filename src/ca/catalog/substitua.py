"""Whole-program constructors for structural substitution and growth.

This module owns audited catalog spellings whose dominant mechanic matches,
replaces, grows, deletes, or branches structure.  It does not own structural
identity primitives, component mechanics, metadata, application, conflict
repair, or execution dispatch.  Goal 7 implementations will compose the five
component algebras into ordinary ``SimpleProgram`` values.

Each canonical family is an explicitly typed, transparent five-component
constructor.  Presets with unsettled Python signatures remain inert private
inventory; true aliases delegate to their canonical constructor.
"""

from __future__ import annotations

from typing import TypeVar

from ..alphabets import Alphabet
from ..frontiers import WritableRegion
from ..neighborhoods import ReadableRegion
from ..program import SimpleProgram
from ..rules import Rule
from ..seeds import Seed


C = TypeVar("C")
V = TypeVar("V")
W = TypeVar("W")
R = TypeVar("R")


# ---------------------------------------------------------------------------
# Phase 1. Canonical families
# ---------------------------------------------------------------------------


def append_only_sequence_generation(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF002 / F002: append finite output while preserving prior support."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def context_dependent_substitution(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF005 / F005: replace items from bounded old-generation context."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def first_passage_aggregation(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF015 / F016: attach a walker irreversibly at first contact."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def front_delete_rear_append_system(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF016 / F017: delete a prefix and append its selected production."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def global_score_sequential_placement(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF019 / F020: score globally and commit one structural placement."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def history_dependent_growth_rewrite(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF022 / F023: grow support using occupancy and provenance history."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def indexed_history_recurrence(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF023 / F024: append a term read through value-addressed history."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def iterated_erasure_process(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF025 / F026: repeatedly erase selected ranked survivors."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def local_graph_rewrite(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF028 / F029: replace graph matches through explicit interfaces."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def moving_frontier_shell_accretion(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF031 / F032: append geometric strips along a moving open rim."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def multiway_rewrite(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF033 / F034: expose every witnessed successor before quotienting."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def parallel_independent_substitution(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF037 / F038: assemble independent offspring in one generation."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def parallel_network_rewrite(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF038 / F040: commit compatible graph patches in parallel."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def random_functional_graph_construction(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF043 / F046: denote a random one-successor graph construction."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def structural_pattern_rewrite(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF049 / F052: rewrite structural matches with explicit scan conflicts."""

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
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """An alias for SPF033 with the exact ``multiway_rewrite`` signature."""

    return multiway_rewrite(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def network_rewrite(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """An alias for SPF038 with the exact canonical network signature."""

    return parallel_network_rewrite(
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
