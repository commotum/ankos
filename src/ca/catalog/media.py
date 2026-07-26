"""Whole-program constructors for transformations between representations.

This module owns audited constructions that transform information, events, or
signals from one explicit representation into another.  It does not own
dataset views, serialization, codecs for semantic identity, component
mechanics, metadata, or execution dispatch.  Goal 7 implementations will make
all work state visible and compose ordinary five-field ``SimpleProgram``
values from the component modules.

Canonical signatures are fixed by the migration matrix.  Preset signatures
that are not fixed remain private non-callable inventory.
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


def event_provenance_causal_network(
    *,
    event_trace,
    read_sets,
    initial_provenance,
) -> SimpleProgram:
    """SPF004 / F004: convert an event trace into direct causal provenance."""

    _not_implemented()


def digit_emitting_register_transduction(
    *,
    seed,
    register_law,
    base,
    digit_projection,
) -> SimpleProgram:
    """SPF008 / F008: update registers while emitting one visible digit."""

    _not_implemented()


def error_diffusion_transform(
    *,
    input,
    palette,
    diffusion_kernel,
    scan,
) -> SimpleProgram:
    """SPF011 / F012: quantize a sample and diffuse error to future sites."""

    _not_implemented()


def maximal_run_record_transduction(
    *,
    input,
    record_grammar,
    direction,
    scan,
    feedback,
) -> SimpleProgram:
    """SPF012 / F013: translate maximal runs and self-delimiting records."""

    _not_implemented()


def hash_index_transform(
    *,
    key,
    table,
    hash_fold,
    collision,
    operation,
) -> SimpleProgram:
    """SPF020 / F021: transform a key through hashing and collision paths."""

    _not_implemented()


def probabilistic_transition_model_fitting(
    *,
    observations,
    topology,
    estimator,
    generation_law,
    generation_request,
) -> SimpleProgram:
    """SPF041 / F044: fit a transition model and denote generated paths."""

    _not_implemented()


def sampled_causal_order_network(
    *,
    region,
    causal_order,
    density,
    event_measure,
) -> SimpleProgram:
    """SPF046 / F049: sample events and transform them into a causal cover."""

    _not_implemented()


def weighted_prefix_block_transduction(
    *,
    input,
    block_partition,
    weights_or_tree,
    direction,
) -> SimpleProgram:
    """SPF054 / F057: encode or decode blocks through a weighted prefix tree."""

    _not_implemented()


def nested_interval_symbol_transduction(
    *,
    input,
    probability_model,
    precision,
    direction,
) -> SimpleProgram:
    """SPF055 / F058: refine or invert one message-wide nested interval."""

    _not_implemented()


def history_reference_record_transduction(
    *,
    input,
    match_policy,
    dictionary,
    record_grammar,
    direction,
) -> SimpleProgram:
    """SPF056 / F059: emit or expand records that reference prior history."""

    _not_implemented()


def recursive_uniform_region_decomposition(
    *,
    input,
    root_region,
    split,
    uniformity,
    cutoff,
    direction,
) -> SimpleProgram:
    """SPF057 / F060: recursively split regions into a hierarchical record."""

    _not_implemented()


def orthogonal_basis_coefficient_transform(
    *,
    input,
    basis,
    ordering,
    retention,
    quantization,
    direction,
) -> SimpleProgram:
    """SPF058 / F061: map a full block to or from ordered basis coefficients."""

    _not_implemented()


def predictive_residual_transduction(
    *,
    input,
    predictor,
    history,
    fitting,
    residual_code,
    direction,
) -> SimpleProgram:
    """SPF059 / F062: translate samples through a causal predictive residual."""

    _not_implemented()


def aligned_xor_stream_transduction(
    *,
    input,
    keystream,
    alignment,
    generator,
) -> SimpleProgram:
    """SPF060 / F063: XOR aligned input with explicit replayable stream state."""

    _not_implemented()


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
