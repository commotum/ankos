"""Whole-program constructors for transformations between representations.

This module owns audited constructions that transform information, events, or
signals from one explicit representation into another.  It does not own
dataset views, serialization, codecs for semantic identity, component
mechanics, metadata, or execution dispatch.  Its constructors make all work
state visible and compose ordinary five-field ``SimpleProgram`` values from
the component modules.

Canonical family names retain their semantic source surfaces as unfinished
builders.  Presets compile bounded source-facing data into the five fields.
"""

from __future__ import annotations

from typing import NoReturn, TypeVar

from .. import alphabets, frontiers, loci, neighborhoods, rules, seeds
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


def _program(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """Compose one ordinary catalog-free program value for a real preset."""

    return SimpleProgram(seed, alphabet, frontier, neighborhood, rule)


def _not_implemented() -> NoReturn:
    """Mark one canonical family builder as unfinished."""

    raise NotImplementedError("canonical family builder is not implemented")


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


def _single_value_components(
    value: alphabets.SemanticValue,
    alphabet: alphabets.Alphabet,
    expression: rules.RuleExpr,
    *,
    label: str,
) -> tuple[
    seeds.Seed,
    alphabets.Alphabet,
    frontiers.WritableRegion,
    neighborhoods.ReadableRegion,
    rules.Rule,
]:
    """Compile one closed structural-value transduction."""

    if type(expression) is not rules.RuleExpr:
        raise TypeError(f"{label} expression must be a RuleExpr")
    source = loci.record_configuration((("state", value),))
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    rule = rules.expression(
        rules.ExistingPlan(
            rules.ExistingPlanKind.BY_INDEX,
            (expression,),
        ),
        contract=rules.RuleContract(
            source.contract,
            alphabet.value_profile,
            readable.result_shape,
            readable.join_shape,
            writable.effect_profile,
        ),
        witness=rules.literal_expr("single-value-transduction"),
        provenance=("single-value-transduction",),
    )
    return (
        seeds.exact(source, value_profile=alphabet.value_profile),
        alphabet,
        writable,
        readable,
        rule,
    )


def constant_digit_register(
    *,
    register: int,
    register_law: rules.RuleExpr,
    digit_projection: rules.RuleExpr,
    base: int = 10,
) -> SimpleProgram:
    """Build the T40 register branch from exact closed register expressions.

    Both expressions evaluate over ``observation(0)``, a record with
    ``register`` and ``digit`` fields.  The transition replaces that record
    atomically; no draw or host callback participates.  Generic application
    validates both evaluated fields against the declared record alphabet
    before committing either one.
    """

    if type(register) is not int or register < 0:
        raise ValueError("constant-digit register must be a nonnegative integer")
    if type(base) is not int or base < 2:
        raise ValueError("constant-digit base must be an integer >= 2")
    if type(register_law) is not rules.RuleExpr:
        raise TypeError("register_law must be a RuleExpr")
    if type(digit_projection) is not rules.RuleExpr:
        raise TypeError("digit_projection must be a RuleExpr")
    state = alphabets.record_value(
        (
            ("register", register),
            ("digit", register % base),
        ),
        tag="digit-register-state",
    )
    alphabet = alphabets.record(
        (
            ("register", alphabets.naturals()),
            ("digit", alphabets.int_range_alphabet(base)),
        )
    )
    updated = rules.record_update(
        rules.record_update(
            rules.observation(0),
            "register",
            register_law,
        ),
        "digit",
        digit_projection,
    )
    seed, alphabet, frontier, neighborhood, rule = _single_value_components(
        state,
        alphabet,
        updated,
        label="constant-digit-register",
    )
    return _program(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def look_and_say(
    *,
    digits: tuple[int, ...],
) -> SimpleProgram:
    """Build one exact feedback step over maximal equal digit runs."""

    if type(digits) is not tuple or not digits:
        raise ValueError("look-and-say digits must be a nonempty tuple")
    if any(type(digit) is not int or digit < 0 for digit in digits):
        raise ValueError("look-and-say digits must be nonnegative integers")
    source = alphabets.word_value(digits, tag="digits")
    runs = rules.maximal_runs(rules.observation(0))
    emitted_run = rules.word_value(
        "digits",
        rules.record_field(rules.bound_value(), "length"),
        rules.record_field(rules.bound_value(), "value"),
    )
    output = rules.flat_map_items(runs, emitted_run, "digits")
    alphabet = alphabets.word(alphabets.naturals())
    seed, alphabet, frontier, neighborhood, rule = _single_value_components(
        source,
        alphabet,
        output,
        label="look-and-say",
    )
    return _program(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )

__all__ = (
    "aligned_xor_stream_transduction",
    "constant_digit_register",
    "digit_emitting_register_transduction",
    "error_diffusion_transform",
    "event_provenance_causal_network",
    "hash_index_transform",
    "history_reference_record_transduction",
    "look_and_say",
    "maximal_run_record_transduction",
    "nested_interval_symbol_transduction",
    "orthogonal_basis_coefficient_transform",
    "predictive_residual_transduction",
    "probabilistic_transition_model_fitting",
    "recursive_uniform_region_decomposition",
    "sampled_causal_order_network",
    "weighted_prefix_block_transduction",
)
