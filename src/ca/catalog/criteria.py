"""Whole-program constructors defined by admissibility and solutions.

This module owns audited constructions whose result is defined by constraints,
objectives, witnesses, solution relations, or weighted alternatives.  It does
not own solver policy, searches hidden inside application, component
mechanics, metadata, or numerical realization.  Defining relations remain
closed Rule data inside ordinary ``SimpleProgram`` values.

Canonical constructors expose the five component values directly.  The
migration matrix's semantic parameter lists remain descriptive metadata;
catalog construction never interprets a parallel recipe language.  Constraint
presets bind explicit closed source presentations to that same relation
mechanic.
"""

from __future__ import annotations

from .. import alphabets, frontiers, loci, neighborhoods, rules, seeds
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


def _certificate(
    kind: rules.CertificateKind,
    label: str,
) -> rules.Certificate:
    return rules.Certificate(kind, rules.literal_expr(label))


def _constraint_components(
    state: alphabets.ValueNode,
    relation: rules.RuleExpr,
    cardinality: rules.Cardinality,
    *,
    label: str,
) -> tuple[
    seeds.Seed,
    alphabets.Alphabet,
    frontiers.WritableRegion,
    neighborhoods.ReadableRegion,
    rules.Rule,
]:
    """Compile a closed constraint presentation without running a solver."""

    if type(state) is not alphabets.ValueNode:
        raise TypeError(f"{label} state must be a ValueNode")
    if type(relation) is not rules.RuleExpr:
        raise TypeError(f"{label} relation must be a RuleExpr")
    alphabet = alphabets.enum((state,))
    source = loci.record_configuration((("constraint", state),))
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    rule = rules.relation(
        relation,
        cardinality,
        contract=rules.RuleContract(
            source.contract,
            alphabet.value_profile,
            readable.result_shape,
            readable.join_shape,
            frontiers.EffectProfile(),
        ),
        completeness_evidence=_certificate(
            rules.CertificateKind.COMPLETENESS,
            f"{label}:complete",
        ),
        soundness_evidence=_certificate(
            rules.CertificateKind.SOUNDNESS,
            f"{label}:sound",
        ),
    )
    return (
        seeds.exact(source, value_profile=alphabet.value_profile),
        alphabet,
        writable,
        readable,
        rule,
    )


def local_constraint_system(
    *,
    partial_assignment: alphabets.ValueNode,
    predicates: alphabets.ValueNode,
    relation: rules.RuleExpr,
    cardinality: rules.Cardinality,
) -> SimpleProgram:
    """Bind T31 to explicit local predicates and a complete solution relation."""

    if type(partial_assignment) is not alphabets.ValueNode:
        raise TypeError("partial_assignment must be a ValueNode")
    if type(predicates) is not alphabets.ValueNode:
        raise TypeError("predicates must be a ValueNode")
    state = alphabets.record_value(
        (
            ("partial_assignment", partial_assignment),
            ("predicates", predicates),
        ),
        tag="local-constraint-system",
    )
    seed, alphabet, frontier, neighborhood, rule = _constraint_components(
        state,
        relation,
        cardinality,
        label="local-constraint-system",
    )
    return local_satisfaction_relation(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def template_constraint_system(
    *,
    partial_assignment: alphabets.ValueNode,
    allowed_templates: alphabets.ValueNode,
    relation: rules.RuleExpr,
    cardinality: rules.Cardinality,
) -> SimpleProgram:
    """Bind T32 to an explicit allowed-template representation."""

    if type(partial_assignment) is not alphabets.ValueNode:
        raise TypeError("partial_assignment must be a ValueNode")
    if type(allowed_templates) is not alphabets.ValueNode:
        raise TypeError("allowed_templates must be a ValueNode")
    state = alphabets.record_value(
        (
            ("partial_assignment", partial_assignment),
            ("allowed_templates", allowed_templates),
        ),
        tag="template-constraint-system",
    )
    seed, alphabet, frontier, neighborhood, rule = _constraint_components(
        state,
        relation,
        cardinality,
        label="template-constraint-system",
    )
    return local_satisfaction_relation(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def seeded_template_constraint_system(
    *,
    partial_assignment: alphabets.ValueNode,
    allowed_templates: alphabets.ValueNode,
    required_occurrences: tuple[alphabets.ValueNode, ...],
    relation: rules.RuleExpr,
    cardinality: rules.Cardinality,
) -> SimpleProgram:
    """Bind T33 with fixed occurrences represented in the Seed state."""

    if type(partial_assignment) is not alphabets.ValueNode:
        raise TypeError("partial_assignment must be a ValueNode")
    if type(allowed_templates) is not alphabets.ValueNode:
        raise TypeError("allowed_templates must be a ValueNode")
    if (
        type(required_occurrences) is not tuple
        or not required_occurrences
        or any(
            type(occurrence) is not alphabets.ValueNode
            for occurrence in required_occurrences
        )
    ):
        raise ValueError(
            "required_occurrences must be a nonempty ValueNode tuple"
        )
    occurrences = alphabets.word_value(
        required_occurrences,
        tag="required-occurrences",
    )
    state = alphabets.record_value(
        (
            ("partial_assignment", partial_assignment),
            ("allowed_templates", allowed_templates),
            ("required_occurrences", occurrences),
        ),
        tag="seeded-template-constraint-system",
    )
    seed, alphabet, frontier, neighborhood, rule = _constraint_components(
        state,
        relation,
        cardinality,
        label="seeded-template-constraint-system",
    )
    return local_satisfaction_relation(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


# ---------------------------------------------------------------------------
# Phase 3. True aliases
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Phase 4. Compatibility adapters
# ---------------------------------------------------------------------------

__all__ = (
    "finite_model_satisfaction",
    "geometric_embedding_relation",
    "global_equation_relation",
    "inverse_local_system_reconstruction",
    "local_factor_weighted_relation",
    "local_constraint_system",
    "local_satisfaction_relation",
    "program_randomization_test",
    "seeded_template_constraint_system",
    "stochastic_local_search",
    "template_constraint_system",
    "weighted_history_sum_relation",
)
