"""Whole-program constructors for transformations between representations.

This module owns audited constructions that transform information, events, or
signals from one explicit representation into another.  It does not own
dataset views, serialization, codecs for semantic identity, component
mechanics, metadata, or execution dispatch.  Goal 7 implementations will make
all work state visible and compose ordinary five-field ``SimpleProgram``
values from the component modules.

Each canonical family is an explicitly typed, transparent five-component
constructor.  Preset signatures that are not fixed remain private non-callable
inventory.
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


def event_provenance_causal_network(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF004 / F004: convert an event trace into direct causal provenance."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def digit_emitting_register_transduction(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF008 / F008: update registers while emitting one visible digit."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def error_diffusion_transform(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF011 / F012: quantize a sample and diffuse error to future sites."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def maximal_run_record_transduction(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF012 / F013: translate maximal runs and self-delimiting records."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def hash_index_transform(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF020 / F021: transform a key through hashing and collision paths."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def probabilistic_transition_model_fitting(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF041 / F044: fit a transition model and denote generated paths."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def sampled_causal_order_network(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF046 / F049: sample events and transform them into a causal cover."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def weighted_prefix_block_transduction(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF054 / F057: encode or decode blocks through a weighted prefix tree."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def nested_interval_symbol_transduction(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF055 / F058: refine or invert one message-wide nested interval."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def history_reference_record_transduction(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF056 / F059: emit or expand records that reference prior history."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def recursive_uniform_region_decomposition(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF057 / F060: recursively split regions into a hierarchical record."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def orthogonal_basis_coefficient_transform(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF058 / F061: map a full block to or from ordered basis coefficients."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def predictive_residual_transduction(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF059 / F062: translate samples through a causal predictive residual."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def aligned_xor_stream_transduction(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF060 / F063: XOR aligned input with explicit replayable stream state."""

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

# The second spelling is a non-T public preset from the canonical matrix.
_PENDING_PRESETS: tuple[tuple[str, str], ...] = (
    ("constant_digit_register", "SPF008"),
    ("look_and_say", "SPF012"),
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
    "aligned_xor_stream_transduction",
    "digit_emitting_register_transduction",
    "error_diffusion_transform",
    "event_provenance_causal_network",
    "hash_index_transform",
    "history_reference_record_transduction",
    "maximal_run_record_transduction",
    "nested_interval_symbol_transduction",
    "orthogonal_basis_coefficient_transform",
    "predictive_residual_transduction",
    "probabilistic_transition_model_fitting",
    "recursive_uniform_region_decomposition",
    "sampled_causal_order_network",
    "weighted_prefix_block_transduction",
)
