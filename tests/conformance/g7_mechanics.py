"""Test-owned G7-02 mechanics ledger and ordinary-program fixtures.

This module deliberately lives outside :mod:`ca`.  SPF/F identities are
coverage labels used to prove that the audited taxonomy is mechanically
covered; no production descriptor or application branch may inspect them.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import ca
from ca import alphabets, frontiers, loci, neighborhoods, program, rules, seeds


@dataclass(frozen=True)
class MechanicsRow:
    """One audited family joined to its dominant reusable pressure fixture."""

    spf: str
    family: str
    name: str
    workstream: str
    primary: str
    fixture: str
    secondary: tuple[str, ...] = ()


MECHANICS_ROWS = (
    # PX01 — coupled writes.
    MechanicsRow("SPF001", "F001", "alternating-partition-local-evolution", "M-A", "PX01", "phase-and-block-coupled-write"),
    MechanicsRow("SPF003", "F003", "asynchronous-local-state-automaton", "M-A", "PX01", "selected-site-and-visible-schedule"),
    MechanicsRow("SPF007", "F007", "coupled-field-mobile-locus-evolution", "M-A", "PX01", "field-and-mobile-marker"),
    MechanicsRow("SPF008", "F008", "digit-emitting-register-transduction", "M-B", "PX01", "register-and-output-end"),
    MechanicsRow("SPF011", "F012", "error-diffusion-transform", "M-A", "PX01", "pixel-error-and-cursor"),
    MechanicsRow("SPF021", "F022", "history-dependent-agent-game", "M-B", "PX01", "joint-actions-scores-and-history"),
    MechanicsRow("SPF030", "F031", "mobile-head-grid-rewrite", "M-A", "PX01", "source-symbol-state-and-destination"),
    MechanicsRow("SPF032", "F033", "multi-active-local-rewrite", "M-A", "PX01", "multi-source-collision-result"),
    MechanicsRow("SPF045", "F048", "register-machine", "M-A", "PX01", "counter-and-register"),
    MechanicsRow("SPF050", "F053", "synchronous-local-state-transform", "M-A", "PX01", "immutable-pass-and-coupled-output"),
    MechanicsRow("SPF052", "F055", "weighted-network-state-update", "M-A", "PX01", "activation-and-weight"),
    # PX02 — variable structure.
    MechanicsRow("SPF002", "F002", "append-only-sequence-generation", "M-B", "PX02", "preserved-prefix-fresh-suffix"),
    MechanicsRow("SPF005", "F005", "context-dependent-substitution", "M-B", "PX02", "variable-length-context-splice"),
    MechanicsRow("SPF016", "F017", "front-delete-rear-append-system", "M-B", "PX02", "prefix-delete-and-suffix-append"),
    MechanicsRow("SPF022", "F023", "history-dependent-growth-rewrite", "M-B", "PX02", "offspring-and-parent-provenance"),
    MechanicsRow("SPF023", "F024", "indexed-history-recurrence", "M-B", "PX02", "value-addressed-fresh-term"),
    MechanicsRow("SPF025", "F026", "iterated-erasure-process", "M-B", "PX02", "ranked-delete-preserving-order"),
    MechanicsRow("SPF028", "F029", "local-graph-rewrite", "M-B", "PX02", "interface-preserving-node-edge-patch"),
    MechanicsRow("SPF031", "F032", "moving-frontier-shell-accretion", "M-B", "PX02", "rim-to-fresh-strip"),
    MechanicsRow("SPF037", "F038", "parallel-independent-substitution", "M-B", "PX02", "generation-wide-delete-create"),
    MechanicsRow("SPF038", "F040", "parallel-network-rewrite", "M-B", "PX02", "compatible-parallel-graph-patches"),
    MechanicsRow("SPF049", "F052", "structural-pattern-rewrite", "M-B", "PX02", "bound-subtree-replacement"),
    # PX03 — nonlocal reads.
    MechanicsRow("SPF017", "F018", "geometric-embedding-relation", "M-C", "PX03", "whole-mesh-metric-relation"),
    MechanicsRow("SPF019", "F020", "global-score-sequential-placement", "M-B", "PX03", "global-score-and-tie"),
    MechanicsRow("SPF027", "F028", "local-factor-weighted-relation", "M-C", "PX03", "overlapping-factor-reduction"),
    MechanicsRow("SPF035", "F036", "nearest-neighbor-retrieval", "M-A", "PX03", "global-metric-minimum", ("PX08",)),
    MechanicsRow("SPF040", "F043", "population-evolutionary-search", "M-B", "PX03", "whole-population-selection"),
    MechanicsRow("SPF046", "F049", "sampled-causal-order-network", "M-B", "PX03", "global-causal-cover"),
    MechanicsRow("SPF051", "F054", "weighted-history-sum-relation", "M-C", "PX03", "complete-history-amplitude-sum"),
    # PX04 — zero/one/many.
    MechanicsRow("SPF014", "F015", "finite-model-satisfaction", "M-C", "PX04", "finite-model-zero-or-one", ("PX08",)),
    MechanicsRow("SPF018", "F019", "global-equation-relation", "M-C", "PX04", "modular-zero-one-many", ("PX03",)),
    MechanicsRow("SPF024", "F025", "inverse-local-system-reconstruction", "M-C", "PX04", "witnessed-predecessor-space", ("PX08",)),
    MechanicsRow("SPF026", "F027", "iterated-map", "M-A", "PX04", "guarded-image-or-no-successor"),
    MechanicsRow("SPF029", "F030", "local-satisfaction-relation", "M-C", "PX04", "joint-xor-completions"),
    MechanicsRow("SPF033", "F034", "multiway-rewrite", "M-B", "PX04", "witnesses-before-quotient"),
    # PX05 — exact continuous/intensional relations.
    MechanicsRow("SPF006", "F006", "continuous-event-dynamics", "M-C", "PX05", "exact-earliest-hit-and-reset"),
    MechanicsRow("SPF036", "F037", "ordinary-differential-flow", "M-C", "PX05", "exact-maximal-flow-relation"),
    MechanicsRow("SPF039", "F041", "partial-differential-relation", "M-C", "PX05", "intensional-constant-field-family", ("PX04",)),
    # PX06 — stochastic laws.
    MechanicsRow("SPF009", "F009", "driven-relaxation", "M-A", "PX06", "drive-law-and-relaxation"),
    MechanicsRow("SPF015", "F016", "first-passage-aggregation", "M-B", "PX06", "first-contact-microtrajectory-law"),
    MechanicsRow("SPF041", "F044", "probabilistic-transition-model-fitting", "M-C", "PX06", "fit-phase-then-path-law"),
    MechanicsRow("SPF043", "F046", "random-functional-graph-construction", "M-B", "PX06", "product-law-over-successors"),
    MechanicsRow("SPF047", "F050", "stochastic-local-search", "M-C", "PX06", "accept-reject-continue-law"),
    # PX07 — mutable program state.
    MechanicsRow("SPF034", "F035", "mutable-rule-local-automaton", "M-B", "PX07", "carrier-and-rule-table-mutation"),
    MechanicsRow("SPF048", "F051", "stored-program-random-access-machine", "M-A", "PX07", "self-modifying-code-and-counter"),
    # PX08 — stopped one-shot programs.
    MechanicsRow("SPF010", "F011", "enumerative-semidecision", "M-A", "PX08", "first-witness-stop-or-diverge"),
    MechanicsRow("SPF020", "F021", "hash-index-transform", "M-B", "PX08", "typed-hit-or-miss-stop"),
    MechanicsRow("SPF044", "F047", "recursive-function-evaluator", "M-B", "PX08", "visible-frame-reduction-and-stop"),
    # PX09 — fixed gates.
    MechanicsRow("SPF013", "F014", "finite-gate-circuit", "M-A", "PX09", "closed-wiring-gate", ("PX08",)),
    # PX10 — explicit representations.
    MechanicsRow("SPF012", "F013", "maximal-run-record-transduction", "M-B", "PX10", "run-record-inverse", ("PX08",)),
    MechanicsRow("SPF054", "F057", "weighted-prefix-block-transduction", "M-B", "PX10", "prefix-tree-inverse"),
    MechanicsRow("SPF055", "F058", "nested-interval-symbol-transduction", "M-B", "PX10", "exact-nested-interval"),
    MechanicsRow("SPF056", "F059", "history-reference-record-transduction", "M-B", "PX10", "literal-pointer-reconstruction"),
    MechanicsRow("SPF057", "F060", "recursive-uniform-region-decomposition", "M-B", "PX10", "leaf-or-child-region-tree"),
    MechanicsRow("SPF058", "F061", "orthogonal-basis-coefficient-transform", "M-C", "PX10", "exact-basis-project-invert"),
    MechanicsRow("SPF059", "F062", "predictive-residual-transduction", "M-B", "PX10", "predict-residual-reconstruct"),
    MechanicsRow("SPF060", "F063", "aligned-xor-stream-transduction", "M-B", "PX10", "xor-involution-with-alignment"),
    # PX11 — shared priority/injury.
    MechanicsRow("SPF053", "F056", "priority-dovetailed-oracle-construction", "M-C", "PX11", "priority-write-injury-and-schedule"),
    # PX12 — executable construction versus observer role.
    MechanicsRow("SPF004", "F004", "event-provenance-causal-network", "M-B", "PX12", "trace-event-to-causal-patch"),
    MechanicsRow("SPF042", "F045", "program-randomization-test", "M-C", "PX12", "visible-surrogate-evaluator-state", ("PX08",)),
)


PRIMARY_PRESSURES = tuple(f"PX{index:02d}" for index in range(1, 13))
WORKSTREAM_COUNTS = (("M-A", 15), ("M-B", 30), ("M-C", 15))
SECONDARY_JOINS = (
    ("SPF018", "PX03"),
    ("SPF039", "PX04"),
    ("SPF012", "PX08"),
    ("SPF013", "PX08"),
    ("SPF014", "PX08"),
    ("SPF024", "PX08"),
    ("SPF035", "PX08"),
    ("SPF042", "PX08"),
)


Semantic = alphabets.SemanticValue
Configuration = loci.FiniteConfiguration[Semantic] | loci.IntensionalConfiguration


@dataclass(frozen=True)
class MechanicsRun:
    """One test-owned expanded program, its source, and its complete result."""

    row: MechanicsRow
    simple_program: ca.SimpleProgram
    source: Configuration
    result: program.ApplicationResult
    representation: alphabets.RepresentationRelation | None = None
    representation_source: alphabets.SemanticValue | None = None
    representation_target: alphabets.SemanticValue | None = None
    recipe: FiniteRecipe | None = None
    trajectory: tuple[
        tuple[Configuration, program.ApplicationComplete],
        ...,
    ] = ()


@dataclass(frozen=True)
class FiniteRecipe:
    """Exact test-owned finite mechanics expected from one family fixture."""

    read_targets: tuple[loci.Locus, ...]
    write_targets: tuple[loci.Locus, ...]
    successor_entries: tuple[
        tuple[tuple[loci.Locus, alphabets.SemanticValue], ...],
        ...,
    ]
    stop: tuple[bool, ...]


def _record_configuration(
    fields: tuple[tuple[str, alphabets.SemanticValue], ...],
) -> loci.FiniteConfiguration:
    return loci.record_configuration(fields)


def _structural_configuration(
    kind: loci.CarrierKind,
    entries: tuple[tuple[loci.Locus, alphabets.SemanticValue], ...],
    *,
    rank: int | None = None,
    axes: tuple[str, ...] = (),
    attributes: tuple[tuple[str, loci.ClosedScalar], ...] = (),
) -> loci.FiniteConfiguration:
    """Build a small variable-support carrier without an executor sidecar."""

    return loci.FiniteConfiguration(
        loci.Carrier(
            loci.CarrierContract(kind, rank=rank, axes=axes),
            loci.Boundary(loci.BoundaryPolicy.NONE),
            attributes,
        ),
        entries,
    )


def _literal_regions(
    source: loci.FiniteConfiguration,
    alphabet: alphabets.Alphabet,
    *,
    write_targets: tuple[loci.Locus, ...],
    read_targets: tuple[loci.Locus, ...],
    effects: tuple[frontiers.Effect, ...] = (frontiers.Effect.REPLACE,),
) -> tuple[frontiers.WritableRegion, neighborhoods.ReadableRegion]:
    """Resolve the exact W/R named by a closed finite recipe."""

    writable = frontiers.literal(
        write_targets,
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
        effects=effects,
    )
    readable = neighborhoods.literal(
        read_targets,
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
        key="family-input",
    )
    return writable, readable


def _existing_target_plan(
    target: loci.Locus,
    action: rules.DispositionAction,
    value: rules.RuleExpr | None = None,
) -> rules.ExistingDispositionPlan:
    return rules.ExistingDispositionPlan(
        rules.capability_target(target),
        action,
        value,
    )


def _fresh_target_plan(
    target: loci.FreshReference,
    action: rules.DispositionAction,
    value: rules.RuleExpr | None = None,
) -> rules.FreshDispositionPlan:
    return rules.FreshDispositionPlan(
        rules.capability_target(target),
        action,
        value,
    )


def _certificate(kind: rules.CertificateKind, label: str) -> rules.Certificate:
    return rules.Certificate(kind, rules.literal_expr(label))


def _stop(label: str) -> rules.Stop:
    return rules.Stop(
        rules.literal_expr(label),
        _certificate(rules.CertificateKind.TERMINALITY, f"{label}:terminal"),
    )


def _contract(
    source: Configuration,
    alphabet: alphabets.Alphabet,
    writable: frontiers.WritableRegion,
    readable: neighborhoods.ReadableRegion,
    *,
    stochastic: bool = False,
    exactness: seeds.ExactnessProfile = seeds.ExactnessProfile.EXACT,
) -> rules.RuleContract:
    return rules.RuleContract(
        source.contract,
        alphabet.value_profile,
        readable.result_shape,
        readable.join_shape,
        writable.effect_profile,
        exactness_profile=exactness,
        entropy_interface=(
            seeds.EntropyInterface.REPLAY_KEY
            if stochastic
            else seeds.EntropyInterface.NONE
        ),
    )


def _existing_plan(
    index: int,
    action: rules.DispositionAction,
    value: rules.RuleExpr | None = None,
) -> rules.ExistingDispositionPlan:
    return rules.ExistingDispositionPlan(
        rules.capability_index(index),
        action,
        value,
    )


def _fresh_plan(
    index: int,
    action: rules.DispositionAction,
    value: rules.RuleExpr | None = None,
) -> rules.FreshDispositionPlan:
    return rules.FreshDispositionPlan(
        rules.capability_index(index),
        action,
        value,
    )


def _derivation_result(
    label: str,
    *,
    existing: tuple[rules.ExistingDispositionPlan, ...] = (),
    fresh: tuple[rules.FreshDispositionPlan, ...] = (),
    stop: bool = False,
) -> rules.DerivationClauseResult:
    return rules.DerivationClauseResult(
        existing,
        fresh,
        rules.Progress.ADVANCED,
        _stop(f"{label}:completed") if stop else rules.Continue(),
        rules.literal_expr(label),
        (f"mechanics:{label}",),
        _certificate(rules.CertificateKind.DERIVATION, f"{label}:derived"),
    )


def _no_successor_result(
    label: str,
    outcome: rules.NoSuccessorOutcome = rules.NoSuccessorOutcome.TERMINAL,
) -> rules.NoSuccessorClauseResult:
    kind = (
        rules.CertificateKind.DIVERGENCE
        if outcome is rules.NoSuccessorOutcome.DIVERGENT
        else rules.CertificateKind.TERMINALITY
    )
    return rules.NoSuccessorClauseResult(
        outcome,
        rules.literal_expr(f"{label}:reason"),
        rules.literal_expr(label),
        (f"mechanics:{label}",),
        _certificate(kind, f"{label}:no-successor"),
    )


def _clause(
    condition: rules.RuleExpr,
    result: rules.ClauseResult,
    *,
    mass: Fraction | None = None,
) -> rules.RuleClause:
    return rules.RuleClause(condition, result, mass)


def _kernel(
    source: Configuration,
    alphabet: alphabets.Alphabet,
    writable: frontiers.WritableRegion,
    readable: neighborhoods.ReadableRegion,
    clauses: tuple[rules.RuleClause, ...],
    *,
    stochastic: bool = False,
    selection: rules.ClauseSelection = rules.ClauseSelection.ALL,
) -> rules.Rule:
    return rules.clause_kernel(
        clauses,
        contract=_contract(
            source,
            alphabet,
            writable,
            readable,
            stochastic=stochastic,
        ),
        completeness_evidence=_certificate(
            rules.CertificateKind.COMPLETENESS,
            "g7-mechanics:closed-clause-space",
        ),
        selection=selection,
    )


def _assemble(
    row: MechanicsRow,
    source: Configuration,
    alphabet: alphabets.Alphabet,
    writable: frontiers.WritableRegion,
    readable: neighborhoods.ReadableRegion,
    rule: rules.Rule,
    *,
    exactness: seeds.ExactnessProfile = seeds.ExactnessProfile.EXACT,
    representation: alphabets.RepresentationRelation | None = None,
    representation_source: alphabets.SemanticValue | None = None,
    representation_target: alphabets.SemanticValue | None = None,
    recipe: FiniteRecipe | None = None,
) -> MechanicsRun:
    simple_program = ca.SimpleProgram(
        seeds.exact(
            source,
            value_profile=alphabet.value_profile,
            exactness_profile=exactness,
        ),
        alphabet,
        writable,
        readable,
        rule,
    )
    return MechanicsRun(
        row,
        simple_program,
        source,
        ca.apply(simple_program, source),
        representation,
        representation_source,
        representation_target,
        recipe,
    )


def _finite_history_components(
    values: tuple[int | Fraction, ...],
    *,
    alphabet: alphabets.Alphabet | None = None,
    effects: tuple[frontiers.Effect, ...] = (frontiers.Effect.REPLACE,),
) -> tuple[
    loci.FiniteConfiguration,
    alphabets.Alphabet,
    frontiers.WritableRegion,
    neighborhoods.ReadableRegion,
]:
    source = loci.history_configuration(values)
    if alphabet is None:
        alphabet = (
            alphabets.rationals()
            if any(type(value) is Fraction for value in values)
            else alphabets.integers()
        )
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
        effects=effects,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    return source, alphabet, writable, readable


_PX01_CASES: dict[
    str,
    tuple[
        tuple[tuple[str, int], ...],
        tuple[str, ...],
        tuple[str, ...],
        tuple[tuple[tuple[str, int], ...], ...],
        bool,
    ],
] = {
    # fields, R, W, complete alternative write maps, stop
    "SPF001": (
        (("phase", 0), ("left", 1), ("right", 0), ("block", 0)),
        ("phase", "left", "right", "block"),
        ("phase", "left", "right", "block"),
        ((("phase", 1), ("left", 0), ("right", 1), ("block", 1)),),
        False,
    ),
    "SPF003": (
        (("site0", 1), ("site1", 0), ("scheduler", 0)),
        ("site0", "site1", "scheduler"),
        ("site0", "scheduler"),
        ((("site0", 0), ("scheduler", 1)),),
        False,
    ),
    "SPF007": (
        (("field0", 2), ("field1", 1), ("field2", 0), ("marker", 1), ("phase", 0)),
        ("field0", "field1", "field2", "marker", "phase"),
        ("field0", "field1", "field2", "marker", "phase"),
        (
            (
                ("field0", 1),
                ("field1", 1),
                ("field2", 0),
                ("marker", 2),
                ("phase", 1),
            ),
        ),
        False,
    ),
    "SPF008": (
        (("register", 13), ("radix", 10), ("digit", -1), ("output_end", 0)),
        ("register", "radix"),
        ("register", "digit", "output_end"),
        ((("register", 1), ("digit", 3), ("output_end", 1)),),
        False,
    ),
    "SPF011": (
        (("pixel", 6), ("threshold", 4), ("error", 0), ("cursor", 0)),
        ("pixel", "threshold", "error", "cursor"),
        ("pixel", "error", "cursor"),
        ((("pixel", 1), ("error", 2), ("cursor", 1)),),
        False,
    ),
    "SPF021": (
        (("action_a", 1), ("action_b", 0), ("score_a", 0), ("score_b", 0), ("history", 0)),
        ("action_a", "action_b", "score_a", "score_b", "history"),
        ("score_a", "score_b", "history"),
        ((("score_a", 1), ("score_b", -1), ("history", 2)),),
        False,
    ),
    "SPF030": (
        (("left", 0), ("source", 1), ("right", 0)),
        ("left", "source", "right"),
        ("left", "source", "right"),
        (
            (("left", 2), ("source", 0), ("right", 0)),
            (("left", 0), ("source", 0), ("right", 2)),
        ),
        False,
    ),
    "SPF032": (
        (("source_a", 1), ("source_b", 1), ("collision", 0), ("phase", 0)),
        ("source_a", "source_b", "collision", "phase"),
        ("source_a", "source_b", "collision", "phase"),
        ((("source_a", 0), ("source_b", 0), ("collision", 2), ("phase", 1)),),
        False,
    ),
    "SPF045": (
        (("pc", 0), ("counter", 2), ("register", 5)),
        ("pc", "counter", "register"),
        ("pc", "counter", "register"),
        ((("pc", 1), ("counter", 1), ("register", 7)),),
        False,
    ),
    "SPF050": (
        (("old0", 1), ("old1", 0), ("next0", 0), ("next1", 0), ("cursor", 0)),
        ("old0", "old1", "cursor"),
        ("next0", "next1", "cursor"),
        ((("next0", 0), ("next1", 1), ("cursor", 2)),),
        True,
    ),
    "SPF052": (
        (("input", 2), ("weight", 3), ("bias", -1), ("activation", 0)),
        ("input", "weight", "bias"),
        ("activation",),
        ((("activation", 5),),),
        False,
    ),
}


def _record_targets(
    source: loci.FiniteConfiguration,
) -> dict[str, loci.Locus]:
    return {
        str(target.path[-1]): target
        for target, _ in source.entries
    }


def _px01(row: MechanicsRow) -> MechanicsRun:
    """Couple source, control, and every possible destination atomically."""

    fields, read_names, write_names, alternatives, stop = _PX01_CASES[row.spf]
    source = _record_configuration(fields)
    alphabet = alphabets.integers()
    targets = _record_targets(source)
    read_targets = tuple(targets[name] for name in read_names)
    write_targets = tuple(targets[name] for name in write_names)
    writable, readable = _literal_regions(
        source,
        alphabet,
        write_targets=write_targets,
        read_targets=read_targets,
    )
    clauses = tuple(
        _clause(
            rules.literal_expr(1),
            _derivation_result(
                f"{row.fixture}:alternative-{index}",
                existing=tuple(
                    _existing_target_plan(
                        targets[name],
                        rules.DispositionAction.REPLACE,
                        rules.literal_expr(value),
                    )
                    for name, value in replacements
                ),
                stop=stop,
            ),
        )
        for index, replacements in enumerate(alternatives)
    )
    rule = _kernel(
        source,
        alphabet,
        writable,
        readable,
        clauses,
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


_PX02_SHAPES = {
    "SPF002": (0, 1),
    "SPF005": (2, 2),
    "SPF016": (2, 1),
    "SPF022": (0, 1),
    "SPF023": (0, 1),
    "SPF025": (1, 0),
    "SPF028": (3, 5),
    "SPF031": (1, 2),
    "SPF037": (2, 2),
    "SPF038": (1, 2),
    "SPF049": (1, 1),
}


def _word_configuration(values: tuple[int, ...]) -> loci.FiniteConfiguration[int]:
    contract = loci.CarrierContract(loci.CarrierKind.WORD, rank=1, axes=("word",))
    entries = tuple(
        (loci.occurrence("word", index), value)
        for index, value in enumerate(values)
    )
    return loci.FiniteConfiguration(
        loci.Carrier(contract, loci.Boundary(loci.BoundaryPolicy.NONE)),
        entries,
    )


def _fresh_children_writable(
    source: loci.FiniteConfiguration,
    alphabet: alphabets.Alphabet,
    *,
    parent: loci.Locus,
    namespace: str,
    keys: tuple[loci.ClosedScalar, ...],
) -> tuple[frontiers.WritableRegion, tuple[loci.FreshReference, ...]]:
    references = tuple(
        loci.FreshReference(namespace, key, parent=parent)
        for key in keys
    )
    return (
        frontiers.fresh(
            loci.fresh_children(parent, namespace, keys),
            namespace=frontiers.FreshNamespace(namespace, parent=parent),
            configuration_contract=source.contract,
            value_profile=alphabet.value_profile,
        ),
        references,
    )


def _graph_node(name: str) -> alphabets.ValueNode:
    return alphabets.ValueNode(
        alphabets.ValueKind.GRAPH,
        "node",
        fields=(("name", name),),
    )


def _graph_edge(
    left: loci.Locus | loci.FreshReference,
    right: loci.Locus | loci.FreshReference,
    *,
    name: str,
) -> alphabets.ValueNode:
    return alphabets.ValueNode(
        alphabets.ValueKind.GRAPH,
        "edge",
        fields=(
            ("left", alphabets.StructuralReference(left)),
            ("name", name),
            ("right", alphabets.StructuralReference(right)),
        ),
    )


def _px02_graph(row: MechanicsRow) -> MechanicsRun:
    """Replace ``a-b-c`` by the explicit interface patch ``a-x-y-c``."""

    node_a = loci.graph_element("node", "a")
    node_b = loci.graph_element("node", "b")
    node_c = loci.graph_element("node", "c")
    edge_ab = loci.graph_element("edge", "a-b")
    edge_bc = loci.graph_element("edge", "b-c")
    source = _structural_configuration(
        loci.CarrierKind.GRAPH,
        (
            (node_a, _graph_node("a")),
            (node_b, _graph_node("b")),
            (node_c, _graph_node("c")),
            (edge_ab, _graph_edge(node_a, node_b, name="a-b")),
            (edge_bc, _graph_edge(node_b, node_c, name="b-c")),
        ),
    )
    alphabet = alphabets.graph()
    existing = frontiers.literal(
        (node_b, edge_ab, edge_bc),
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
        effects=(frontiers.Effect.DELETE,),
    )

    node_namespace = "g7-graph-nodes"
    node_region, node_references = _fresh_children_writable(
        source,
        alphabet,
        parent=node_b,
        namespace=node_namespace,
        keys=("x", "y"),
    )
    node_x, node_y = node_references

    edge_namespace = "g7-graph-edges"
    edge_references = tuple(
        loci.FreshReference(
            edge_namespace,
            key,
            interface=(node_a, node_c),
        )
        for key in ("a-x", "x-y", "y-c")
    )
    edge_region = frontiers.fresh(
        loci.fresh_edges(
            (node_a, node_c),
            edge_namespace,
            ("a-x", "x-y", "y-c"),
        ),
        namespace=frontiers.FreshNamespace(edge_namespace),
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    writable = frontiers.union((existing, node_region, edge_region))
    readable = neighborhoods.literal(
        (node_a, node_b, node_c, edge_ab, edge_bc),
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
        key="matched-path-and-interface",
    )

    created = (
        (node_x, _graph_node("x")),
        (node_y, _graph_node("y")),
        (
            edge_references[0],
            _graph_edge(node_a, node_x, name="a-x"),
        ),
        (
            edge_references[1],
            _graph_edge(node_x, node_y, name="x-y"),
        ),
        (
            edge_references[2],
            _graph_edge(node_y, node_c, name="y-c"),
        ),
    )
    rule = _kernel(
        source,
        alphabet,
        writable,
        readable,
        (
            _clause(
                rules.literal_expr(1),
                _derivation_result(
                    row.fixture,
                    existing=tuple(
                        _existing_target_plan(
                            target,
                            rules.DispositionAction.DELETE,
                        )
                        for target in (node_b, edge_ab, edge_bc)
                    ),
                    fresh=tuple(
                        _fresh_target_plan(
                            reference,
                            rules.DispositionAction.CREATE,
                            rules.literal_expr(value),
                        )
                        for reference, value in created
                    ),
                ),
            ),
        ),
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _px02(row: MechanicsRow) -> MechanicsRun:
    """Apply one input-derived total delete/create structural patch."""

    if row.spf == "SPF028":
        return _px02_graph(row)

    delete_count, create_count = _PX02_SHAPES[row.spf]
    if row.spf in {"SPF002", "SPF005", "SPF016", "SPF025", "SPF037"}:
        values = {
            "SPF002": (1, 2),
            "SPF005": (0, 1, 2, 3),
            "SPF016": (1, 1, 0, 1),
            "SPF025": (4, 9, 5),
            "SPF037": (1, 2),
        }[row.spf]
        source = _word_configuration(values)
    elif row.spf == "SPF022":
        source = _structural_configuration(
            loci.CarrierKind.TREE,
            (
                (loci.path("root", scope="growth-tree"), 1),
                (loci.path("root", "left", scope="growth-tree"), 2),
            ),
        )
    elif row.spf == "SPF023":
        source = _structural_configuration(
            loci.CarrierKind.HISTORY,
            tuple(
                (loci.occurrence("history", index), value)
                for index, value in enumerate((1, 1))
            ),
            rank=1,
            axes=("history",),
        )
    elif row.spf == "SPF031":
        source = _structural_configuration(
            loci.CarrierKind.GRID,
            (
                (loci.cell((-1, 0), axes=("x", "y")), 1),
                (loci.cell((0, 0), axes=("x", "y")), 2),
                (loci.cell((1, 0), axes=("x", "y")), 1),
            ),
            rank=2,
            axes=("x", "y"),
        )
    elif row.spf == "SPF038":
        source = _structural_configuration(
            loci.CarrierKind.GRAPH,
            (
                (loci.graph_element("node", "a"), 1),
                (loci.graph_element("node", "b"), 2),
                (loci.graph_element("edge", "a-b"), 3),
            ),
        )
    elif row.spf == "SPF049":
        source = _structural_configuration(
            loci.CarrierKind.TREE,
            (
                (loci.path("add", scope="term"), 7),
                (loci.path("add", "x", scope="term"), 8),
                (loci.path("add", "zero", scope="term"), 0),
            ),
        )
    else:
        raise AssertionError(f"missing PX02 recipe for {row.spf}")

    alphabet = alphabets.integers()
    source_targets = tuple(target for target, _ in source.entries)
    if row.spf in {"SPF002", "SPF022", "SPF023"}:
        delete_targets = ()
    elif row.spf in {"SPF005", "SPF016"}:
        delete_targets = source_targets[1:3] if row.spf == "SPF005" else source_targets[:2]
    elif row.spf in {"SPF025", "SPF031"}:
        delete_targets = (source_targets[1],)
    elif row.spf == "SPF037":
        delete_targets = source_targets
    elif row.spf == "SPF038":
        delete_targets = (
            next(
                target
                for target in source_targets
                if target.kind is loci.LocusKind.GRAPH_ELEMENT
                and target.path[0] == "edge"
            ),
        )
    else:
        assert row.spf == "SPF049"
        delete_targets = (loci.path("add", scope="term"),)
    assert len(delete_targets) == delete_count

    parts: list[frontiers.WritableRegion] = []
    if delete_targets:
        parts.append(
            frontiers.literal(
                delete_targets,
                configuration_contract=source.contract,
                value_profile=alphabet.value_profile,
                effects=(frontiers.Effect.DELETE,),
            )
        )
    parent = {
        "SPF002": source_targets[-1],
        "SPF005": source_targets[0],
        "SPF016": source_targets[-1],
        "SPF022": loci.path("root", scope="growth-tree"),
        "SPF023": source_targets[-1],
        "SPF025": source_targets[0],
        "SPF031": source_targets[-1],
        "SPF037": source_targets[0],
        "SPF038": source_targets[0],
        "SPF049": loci.path("add", "x", scope="term"),
    }[row.spf]
    references: tuple[loci.FreshReference, ...] = ()
    if create_count:
        fresh_region, references = _fresh_children_writable(
            source,
            alphabet,
            parent=parent,
            namespace=f"g7-{row.spf.lower()}",
            keys=tuple(f"created-{index}" for index in range(create_count)),
        )
        parts.append(fresh_region)
    if len(parts) == 1:
        writable = parts[0]
    else:
        writable = frontiers.union(tuple(parts))
    readable = neighborhoods.literal(
        source_targets,
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
        key="matched-old-structure",
    )
    existing_plans = tuple(
        _existing_target_plan(target, rules.DispositionAction.DELETE)
        for target in delete_targets
    )
    created_values = {
        "SPF002": (3,),
        "SPF005": (7, 8),
        "SPF016": (9,),
        "SPF022": (3,),
        "SPF023": (2,),
        "SPF025": (),
        "SPF031": (4, 5),
        "SPF037": (1, 2),
        "SPF038": (4, 5),
        "SPF049": (8,),
    }[row.spf]
    fresh_plans = tuple(
        _fresh_target_plan(
            reference,
            rules.DispositionAction.CREATE,
            rules.literal_expr(value),
        )
        for reference, value in zip(references, created_values, strict=True)
    )
    rule = _kernel(
        source,
        alphabet,
        writable,
        readable,
        (
            _clause(
                rules.literal_expr(1),
                _derivation_result(
                    row.fixture,
                    existing=existing_plans,
                    fresh=fresh_plans,
                ),
            ),
        ),
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _px03(row: MechanicsRow) -> MechanicsRun:
    """Use the complete immutable snapshot in one coupled global decision."""

    fields, read_names, result_name = {
        "SPF017": (
            (("fixed", 0), ("metric", 2), ("movable", -1)),
            ("fixed", "metric"),
            "movable",
        ),
        "SPF019": (
            (("score0", 2), ("score1", 5), ("score2", 3), ("winner", -1)),
            ("score0", "score1", "score2"),
            "winner",
        ),
        "SPF027": (
            (("factor_xy", 2), ("factor_yz", 3), ("normalization", 1)),
            ("factor_xy", "factor_yz"),
            "normalization",
        ),
        "SPF035": (
            (("stored0", 0), ("stored1", 2), ("query", 1), ("nearest", -1)),
            ("stored0", "stored1", "query"),
            "nearest",
        ),
        "SPF040": (
            (("fitness0", 3), ("fitness1", 7), ("fitness2", 5), ("selected", -1)),
            ("fitness0", "fitness1", "fitness2"),
            "selected",
        ),
        "SPF046": (
            (("event0", 1), ("event1", 1), ("event2", 0), ("cover_size", -1)),
            ("event0", "event1", "event2"),
            "cover_size",
        ),
        "SPF051": (
            (("history0", 1), ("history1", -1), ("amplitude", 9)),
            ("history0", "history1"),
            "amplitude",
        ),
    }[row.spf]
    source = _record_configuration(fields)
    alphabet = (
        alphabets.rationals()
        if row.spf == "SPF017"
        else alphabets.integers()
    )
    targets = _record_targets(source)
    read_targets = tuple(targets[name] for name in read_names)
    result_target = targets[result_name]
    writable, readable = _literal_regions(
        source,
        alphabet,
        write_targets=(result_target,),
        read_targets=read_targets,
    )
    outputs: tuple[rules.RuleExpr, ...] = {
        "SPF017": (
            rules.divide(
                rules.add(rules.observation(0), rules.observation(1)),
                rules.literal_expr(2),
            ),
        ),
        "SPF019": (rules.literal_expr(1),),
        "SPF027": (
            rules.multiply(rules.observation(0), rules.observation(1)),
        ),
        "SPF035": (
            rules.observation(0),
            rules.observation(1),
        ),
        "SPF040": (
            rules.conditional(
                rules.less_than(rules.observation(0), rules.observation(1)),
                rules.literal_expr(1),
                rules.literal_expr(0),
            ),
        ),
        "SPF046": (
            rules.add(
                rules.observation(0),
                rules.observation(1),
                rules.observation(2),
            ),
        ),
        "SPF051": (
            rules.add(rules.observation(0), rules.observation(1)),
        ),
    }[row.spf]
    condition = rules.less_equal(
        rules.literal_expr(0),
        rules.add(*(rules.observation(index) for index in range(len(read_targets)))),
    )
    rule = _kernel(
        source,
        alphabet,
        writable,
        readable,
        tuple(
            _clause(
                condition,
                _derivation_result(
                    f"{row.fixture}:result-{index}",
                    existing=(
                        _existing_target_plan(
                            result_target,
                            rules.DispositionAction.REPLACE,
                            output,
                        ),
                    ),
                    stop=row.spf == "SPF035",
                ),
            )
            for index, output in enumerate(outputs)
        ),
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _px04(row: MechanicsRow) -> MechanicsRun:
    """Denote typed zero, witnessed one, or witnessed many alternatives."""

    if row.spf == "SPF014":
        source = _record_configuration((("axiom", 1), ("model", -1)))
        targets = _record_targets(source)
        read_targets = (targets["axiom"],)
        write_targets = (targets["model"],)
        alternatives = (((targets["model"], 0),),)
    elif row.spf == "SPF018":
        source = _record_configuration((("rhs", 1), ("x", -1), ("y", -1)))
        targets = _record_targets(source)
        read_targets = (targets["rhs"],)
        write_targets = (targets["x"], targets["y"])
        alternatives = (
            ((targets["x"], 0), (targets["y"], 1)),
            ((targets["x"], 1), (targets["y"], 0)),
        )
    elif row.spf == "SPF024":
        source = _record_configuration((("observed", 1), ("predecessor", -1)))
        targets = _record_targets(source)
        read_targets = (targets["observed"],)
        write_targets = (targets["predecessor"],)
        alternatives = (((targets["predecessor"], 0),),)
    elif row.spf == "SPF026":
        source = _record_configuration((("guard", 0), ("image", -1)))
        targets = _record_targets(source)
        read_targets = (targets["guard"],)
        write_targets = (targets["image"],)
        alternatives = ()
    elif row.spf == "SPF029":
        source = _record_configuration((("rhs", 1), ("x", -1), ("y", -1)))
        targets = _record_targets(source)
        read_targets = (targets["rhs"],)
        write_targets = (targets["x"], targets["y"])
        alternatives = (
            ((targets["x"], 0), (targets["y"], 1)),
            ((targets["x"], 1), (targets["y"], 0)),
        )
    elif row.spf == "SPF033":
        source = _record_configuration((("symbol", 0),))
        targets = _record_targets(source)
        read_targets = (targets["symbol"],)
        write_targets = (targets["symbol"],)
        alternatives = (
            ((targets["symbol"], 1),),
            ((targets["symbol"], 1),),
        )
    else:
        raise AssertionError(f"missing PX04 recipe for {row.spf}")

    alphabet = alphabets.integers()
    writable, readable = _literal_regions(
        source,
        alphabet,
        write_targets=write_targets,
        read_targets=read_targets,
    )
    if alternatives:
        clauses = tuple(
            _clause(
                rules.literal_expr(1),
                _derivation_result(
                    f"{row.fixture}:solution-{index}",
                    existing=tuple(
                        _existing_target_plan(
                            target,
                            rules.DispositionAction.REPLACE,
                            rules.literal_expr(value),
                        )
                        for target, value in replacements
                    ),
                    stop=row.spf != "SPF033",
                ),
            )
            for index, replacements in enumerate(alternatives)
        )
    else:
        clauses = (
            _clause(
                rules.equal(rules.observation(0), rules.literal_expr(0)),
                _no_successor_result(f"{row.fixture}:guarded-zero"),
            ),
        )
    rule = _kernel(
        source,
        alphabet,
        writable,
        readable,
        clauses,
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _px05_finite(row: MechanicsRow) -> MechanicsRun:
    """Commit an exact Fraction-valued flow/event segment and stop."""

    if row.spf == "SPF036":
        initial = alphabets.ValueNode(
            alphabets.ValueKind.FIELD,
            "ode-state",
            fields=(("equation", "dx/dt=1"), ("initial", 0)),
        )
        unset = alphabets.ValueNode(
            alphabets.ValueKind.FIELD,
            "solution-slot",
            fields=(("status", "unset"),),
        )
        solution = alphabets.ValueNode(
            alphabets.ValueKind.FIELD,
            "maximal-solution",
            fields=(
                ("domain", "maximal-real-line"),
                ("expression", "x(t)=t"),
                ("initial", 0),
            ),
        )
        source = loci.history_configuration((initial, unset))
        alphabet = alphabets.field()
        read_targets = (source.entries[0][0],)
        write_targets = (source.entries[1][0],)
        writable, readable = _literal_regions(
            source,
            alphabet,
            write_targets=write_targets,
            read_targets=read_targets,
        )
        rule = _kernel(
            source,
            alphabet,
            writable,
            readable,
            (
                _clause(
                    rules.literal_expr(1),
                    _derivation_result(
                        row.fixture,
                        existing=(
                            _existing_target_plan(
                                write_targets[0],
                                rules.DispositionAction.REPLACE,
                                rules.literal_expr(solution),
                            ),
                        ),
                        stop=True,
                    ),
                ),
            ),
        )
        return _assemble(row, source, alphabet, writable, readable, rule)

    assert row.spf == "SPF006"
    source, alphabet, writable, readable = _finite_history_components(
        (Fraction(1, 4), Fraction(-1), Fraction(0), Fraction(0)),
        alphabet=alphabets.rationals(),
    )
    rule = _kernel(
        source,
        alphabet,
        writable,
        readable,
        (
            _clause(
                rules.less_equal(rules.literal_expr(0), rules.observation(0)),
                _derivation_result(
                    row.fixture,
                    existing=(
                        _existing_plan(
                            0,
                            rules.DispositionAction.REPLACE,
                            rules.literal_expr(Fraction(0)),
                        ),
                        _existing_plan(
                            1,
                            rules.DispositionAction.REPLACE,
                            rules.subtract(
                                rules.literal_expr(0),
                                rules.observation(1),
                            ),
                        ),
                        _existing_plan(
                            2,
                            rules.DispositionAction.REPLACE,
                            rules.add(rules.observation(2), rules.observation(0)),
                        ),
                        _existing_plan(
                            3,
                            rules.DispositionAction.REPLACE,
                            rules.literal_expr(1),
                        ),
                    ),
                    stop=True,
                ),
            ),
        ),
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _px05_intensional(row: MechanicsRow) -> MechanicsRun:
    """Retain an exact uncountable differential solution relation."""

    contract = loci.CarrierContract(loci.CarrierKind.FIELD)
    dependency = loci.selector_differential_germ("u", 1)
    source = loci.IntensionalConfiguration(
        contract,
        dependency,
        "spf039:all-exact-field-presentations",
    )
    alphabet = alphabets.field()
    writable = frontiers.intensional(
        "u",
        dependency,
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.differential_germ(
        "u",
        1,
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    relation = rules.RuleExpr(
        rules.ExpressionPrimitive.TUPLE,
        (
            rules.literal_expr("constant-field-solution-relation"),
            rules.literal_expr("binder:c"),
            rules.literal_expr("du/dx=0"),
            rules.literal_expr("domain:[0,1]"),
            rules.literal_expr("replace-entire-field:u"),
        ),
    )
    uncountable = rules.Many(
        None,
        rules.InfiniteCardinality.UNCOUNTABLE,
        _certificate(
            rules.CertificateKind.CARDINALITY,
            "constant-field:uncountable",
        ),
    )
    rule = rules.differential(
        relation,
        uncountable,
        contract=_contract(source, alphabet, writable, readable),
        completeness_evidence=_certificate(
            rules.CertificateKind.COMPLETENESS,
            "constant-field:complete",
        ),
        soundness_evidence=_certificate(
            rules.CertificateKind.SOUNDNESS,
            "constant-field:sound",
        ),
        projection_cardinalities=rules.ProjectionCardinalities(
            uncountable,
            rules.finite_cardinality(0),
            uncountable,
            _certificate(
                rules.CertificateKind.COMPOSITION,
                "constant-field:injective-total-projection",
            ),
        ),
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _px05(row: MechanicsRow) -> MechanicsRun:
    return _px05_intensional(row) if row.spf == "SPF039" else _px05_finite(row)


def _px06(row: MechanicsRow) -> MechanicsRun:
    """Return an exact law without drawing, then expose both submeasures."""

    if row.spf == "SPF009":
        source = _record_configuration(
            (("site", 0), ("energy", 2), ("drive_count", 0))
        )
        targets = _record_targets(source)
        read_targets = (targets["site"], targets["energy"], targets["drive_count"])
        write_targets = (targets["site"], targets["energy"], targets["drive_count"])
        branches: tuple[
            tuple[Fraction, tuple[tuple[loci.Locus, int], ...] | None, str],
            ...,
        ] = (
            (
                Fraction(1, 2),
                (
                    (targets["site"], 1),
                    (targets["energy"], 1),
                    (targets["drive_count"], 1),
                ),
                "drive-right",
            ),
            (
                Fraction(1, 2),
                (
                    (targets["site"], -1),
                    (targets["energy"], 1),
                    (targets["drive_count"], 1),
                ),
                "drive-left",
            ),
        )
    elif row.spf == "SPF015":
        source = _record_configuration(
            (
                ("source", 2),
                ("contact_site", 0),
                ("free_site", 0),
                ("attached", 0),
                ("relaunch", 0),
                ("phase", 0),
            )
        )
        targets = _record_targets(source)
        read_targets = tuple(targets[name] for name in (
            "source",
            "contact_site",
            "free_site",
            "attached",
        ))
        write_targets = tuple(targets[name] for name in (
            "source",
            "contact_site",
            "free_site",
            "attached",
            "relaunch",
            "phase",
        ))
        branches = (
            (
                Fraction(1, 2),
                (
                    (targets["source"], 0),
                    (targets["contact_site"], 1),
                    (targets["attached"], 1),
                    (targets["relaunch"], 0),
                    (targets["phase"], 1),
                ),
                "first-contact-attach",
            ),
            (
                Fraction(1, 2),
                (
                    (targets["source"], 0),
                    (targets["free_site"], 1),
                    (targets["attached"], 0),
                    (targets["relaunch"], 1),
                    (targets["phase"], 1),
                ),
                "free-flight-relaunch",
            ),
        )
    elif row.spf == "SPF041":
        source = _record_configuration(
            (
                ("count_a", 2),
                ("count_b", 1),
                ("fit_parameter", 0),
                ("generated_path", -1),
                ("phase", 0),
            )
        )
        targets = _record_targets(source)
        read_targets = tuple(targets[name] for name in (
            "count_a",
            "count_b",
            "fit_parameter",
            "phase",
        ))
        write_targets = tuple(targets[name] for name in (
            "fit_parameter",
            "generated_path",
            "phase",
        ))
        branches = (
            (
                Fraction(2, 3),
                (
                    (targets["fit_parameter"], 2),
                    (targets["generated_path"], 0),
                    (targets["phase"], 1),
                ),
                "fitted-path-a",
            ),
            (
                Fraction(1, 3),
                (
                    (targets["fit_parameter"], 2),
                    (targets["generated_path"], 1),
                    (targets["phase"], 1),
                ),
                "fitted-path-b",
            ),
        )
    elif row.spf == "SPF043":
        source = _record_configuration(
            (("node0_successor", -1), ("node1_successor", -1), ("phase", 0))
        )
        targets = _record_targets(source)
        read_targets = (targets["phase"],)
        write_targets = tuple(targets[name] for name in (
            "node0_successor",
            "node1_successor",
            "phase",
        ))
        branches = tuple(
            (
                Fraction(1, 4),
                (
                    (targets["node0_successor"], left),
                    (targets["node1_successor"], right),
                    (targets["phase"], 1),
                ),
                f"functional-graph-{left}{right}",
            )
            for left in (0, 1)
            for right in (0, 1)
        )
    elif row.spf == "SPF047":
        source = _record_configuration(
            (("incumbent", 0), ("proposal_counter", 0))
        )
        targets = _record_targets(source)
        read_targets = (targets["incumbent"], targets["proposal_counter"])
        write_targets = (targets["incumbent"], targets["proposal_counter"])
        branches = (
            (
                Fraction(1, 2),
                (
                    (targets["incumbent"], 1),
                    (targets["proposal_counter"], 1),
                ),
                "accepted",
            ),
            (
                Fraction(1, 4),
                ((targets["proposal_counter"], 1),),
                "rejected-continue",
            ),
            (Fraction(1, 4), None, "no-proposal"),
        )
    else:
        raise AssertionError(f"missing PX06 recipe for {row.spf}")

    alphabet = alphabets.integers()
    writable, readable = _literal_regions(
        source,
        alphabet,
        write_targets=write_targets,
        read_targets=read_targets,
    )
    clauses = tuple(
        _clause(
            rules.literal_expr(1),
            (
                _no_successor_result(
                    f"{row.fixture}:{label}",
                    rules.NoSuccessorOutcome.DECLARED_FAILURE,
                )
                if replacements is None
                else _derivation_result(
                    f"{row.fixture}:{label}",
                    existing=tuple(
                        _existing_target_plan(
                            target,
                            rules.DispositionAction.REPLACE,
                            rules.literal_expr(value),
                        )
                        for target, value in replacements
                    ),
                )
            ),
            mass=mass,
        )
        for mass, replacements, label in branches
    )
    rule = _kernel(
        source,
        alphabet,
        writable,
        readable,
        clauses,
        stochastic=True,
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _px07(row: MechanicsRow) -> MechanicsRun:
    """Mutate carrier data and visible program/instruction state together."""

    if row.spf == "SPF034":
        fields = (
            ("cell", 1),
            ("mutable_rule_entry", 30),
            ("phase", 0),
        )
        read_names = ("cell", "mutable_rule_entry", "phase")
        replacements = (
            ("cell", 0),
            ("mutable_rule_entry", 31),
            ("phase", 1),
        )
    else:
        assert row.spf == "SPF048"
        fields = (
            ("pc", 0),
            ("memory0_opcode", 7),
            ("memory1_data", 7),
            ("halted", 0),
        )
        read_names = ("pc", "memory0_opcode", "memory1_data")
        replacements = (
            ("pc", 0),
            ("memory0_opcode", 0),
            ("halted", 1),
        )
    source = _record_configuration(fields)
    alphabet = alphabets.integers()
    targets = _record_targets(source)
    writable, readable = _literal_regions(
        source,
        alphabet,
        write_targets=tuple(targets[name] for name, _ in replacements),
        read_targets=tuple(targets[name] for name in read_names),
    )
    rule = _kernel(
        source,
        alphabet,
        writable,
        readable,
        (
            _clause(
                rules.literal_expr(1),
                _derivation_result(
                    row.fixture,
                    existing=tuple(
                        _existing_target_plan(
                            targets[name],
                            rules.DispositionAction.REPLACE,
                            rules.literal_expr(value),
                        )
                        for name, value in replacements
                    ),
                ),
            ),
        ),
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _px08(row: MechanicsRow) -> MechanicsRun:
    """Produce a typed one-shot successor whose continuation is stopped."""

    fields, read_names, replacements = {
        "SPF010": (
            (("candidate", 4), ("bound", 5), ("witness", -1), ("phase", 0)),
            ("candidate", "bound", "phase"),
            (("witness", 4), ("phase", 1)),
        ),
        "SPF020": (
            (("query_hash", 0), ("bucket_key", 0), ("bucket_value", 7), ("result", -1), ("phase", 0)),
            ("query_hash", "bucket_key", "bucket_value", "phase"),
            (("result", 7), ("phase", 1)),
        ),
        "SPF044": (
            (("argument", 3), ("frame_depth", 1), ("accumulator", 2), ("result", -1), ("phase", 0)),
            ("argument", "frame_depth", "accumulator", "phase"),
            (("frame_depth", 0), ("result", 5), ("phase", 1)),
        ),
    }[row.spf]
    source = _record_configuration(fields)
    alphabet = alphabets.integers()
    targets = _record_targets(source)
    writable, readable = _literal_regions(
        source,
        alphabet,
        write_targets=tuple(targets[name] for name, _ in replacements),
        read_targets=tuple(targets[name] for name in read_names),
    )
    rule = _kernel(
        source,
        alphabet,
        writable,
        readable,
        (
            _clause(
                rules.literal_expr(1),
                _derivation_result(
                    row.fixture,
                    existing=tuple(
                        _existing_target_plan(
                            targets[name],
                            rules.DispositionAction.REPLACE,
                            rules.literal_expr(value),
                        )
                        for name, value in replacements
                    ),
                    stop=True,
                ),
            ),
        ),
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _px09(row: MechanicsRow) -> MechanicsRun:
    """Evaluate a closed fixed wiring/gate expression and stop."""

    source = _record_configuration((("wire_x", True), ("wire_y", False), ("cursor", False)))
    alphabet = alphabets.boolean()
    targets = _record_targets(source)
    writable, readable = _literal_regions(
        source,
        alphabet,
        write_targets=(targets["wire_x"], targets["wire_y"], targets["cursor"]),
        read_targets=(targets["wire_x"], targets["wire_y"], targets["cursor"]),
    )
    addressed_pair = rules.gate(
        rules.RuleExpr(
            rules.ExpressionPrimitive.TUPLE,
            (
                rules.observation(0),
                rules.equal(rules.observation(1), rules.literal_expr(False)),
            ),
        ),
        rules.GateKind.ALL,
    )
    rule = _kernel(
        source,
        alphabet,
        writable,
        readable,
        (
            _clause(
                rules.literal_expr(1),
                _derivation_result(
                    row.fixture,
                    existing=(
                        _existing_plan(
                            0,
                            rules.DispositionAction.REPLACE,
                            rules.literal_expr(True),
                        ),
                        _existing_plan(
                            1,
                            rules.DispositionAction.REPLACE,
                            rules.conditional(
                                addressed_pair,
                                rules.literal_expr(True),
                                rules.observation(1),
                            ),
                        ),
                        _existing_plan(
                            2,
                            rules.DispositionAction.REPLACE,
                            rules.literal_expr(True),
                        ),
                    ),
                    stop=True,
                ),
            ),
        ),
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _exact_representation(row: MechanicsRow) -> alphabets.RepresentationRelation:
    """Build a row-specific exact finite map with a proved inverse on image."""

    offset = 1000 + int(row.spf[-3:]) * 10
    source_schema = alphabets.enum((0, 1)).descriptor
    target_schema = alphabets.enum((offset, offset + 1)).descriptor
    relation = (
        alphabets.RepresentationPair(0, offset),
        alphabets.RepresentationPair(1, offset + 1),
    )
    return alphabets.RepresentationRelation(
        source_schema,
        target_schema,
        alphabets.RepresentationProfile.EXACT,
        relation,
        (offset, offset + 1),
        (
            alphabets.RepresentationPair(offset, 0),
            alphabets.RepresentationPair(offset + 1, 1),
        ),
    )


def _px10(row: MechanicsRow) -> MechanicsRun:
    """Apply one exact representation map and retain its inverse obligation."""

    representation = _exact_representation(row)
    encoded = representation.forward(1)
    assert type(encoded) is int
    source = loci.history_configuration((1, 0))
    alphabet = alphabets.enum((0, 1, *representation.image_evidence))
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    rule = _kernel(
        source,
        alphabet,
        writable,
        readable,
        (
            _clause(
                rules.equal(rules.observation(0), rules.literal_expr(1)),
                _derivation_result(
                    row.fixture,
                    existing=(
                        _existing_plan(
                            1,
                            rules.DispositionAction.REPLACE,
                            rules.literal_expr(encoded),
                        ),
                    ),
                    stop=True,
                ),
            ),
        ),
    )
    return _assemble(
        row,
        source,
        alphabet,
        writable,
        readable,
        rule,
        representation=representation,
    )


def _px11(row: MechanicsRow) -> MechanicsRun:
    """Advance one priority requirement and atomically injure the lower one."""

    source, alphabet, writable, readable = _finite_history_components((0, 1, 1, 0))
    rule = _kernel(
        source,
        alphabet,
        writable,
        readable,
        (
            _clause(
                rules.equal(rules.observation(0), rules.literal_expr(0)),
                _derivation_result(
                    row.fixture,
                    existing=(
                        _existing_plan(0, rules.DispositionAction.REPLACE, rules.literal_expr(1)),
                        _existing_plan(1, rules.DispositionAction.REPLACE, rules.literal_expr(0)),
                        _existing_plan(2, rules.DispositionAction.REPLACE, rules.literal_expr(0)),
                        _existing_plan(3, rules.DispositionAction.REPLACE, rules.literal_expr(1)),
                    ),
                ),
            ),
        ),
        selection=rules.ClauseSelection.FIRST,
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _px12(row: MechanicsRow) -> MechanicsRun:
    """Keep executable transform/evaluator state inside an ordinary program."""

    if row.spf == "SPF004":
        # The structural birth is the causal node; producer and cursor remain
        # explicit existing state and the completed transform stops.
        source = _word_configuration((1, 0))
        alphabet = alphabets.integers()
        existing = frontiers.everywhere(
            configuration_contract=source.contract,
            value_profile=alphabet.value_profile,
        )
        parent = source.entries[0][0]
        reference = loci.FreshReference(
            "g7-causal",
            "event-1",
            parent=parent,
            interface=(parent,),
        )
        fresh = frontiers.fresh(
            loci.fresh_children(parent, "g7-causal", ("event-1",)),
            namespace=frontiers.FreshNamespace("g7-causal", parent=parent),
            configuration_contract=source.contract,
            value_profile=alphabet.value_profile,
        )
        writable = frontiers.union((existing, fresh))
        readable = neighborhoods.global_view(
            configuration_contract=source.contract,
            value_profile=alphabet.value_profile,
        )
        rule = _kernel(
            source,
            alphabet,
            writable,
            readable,
            (
                _clause(
                    rules.literal_expr(1),
                    _derivation_result(
                        row.fixture,
                        existing=(
                            _existing_plan(
                                1,
                                rules.DispositionAction.REPLACE,
                                rules.literal_expr(1),
                            ),
                        ),
                        fresh=(
                            _fresh_plan(
                                0,
                                rules.DispositionAction.CREATE,
                                rules.literal_expr(1),
                            ),
                        ),
                        stop=True,
                    ),
                ),
            ),
        )
        return _assemble(row, source, alphabet, writable, readable, rule)
    return _px08(row)


def run_mechanics_fixture(row: MechanicsRow) -> MechanicsRun:
    """Run one row through its pressure's reusable, family-blind mechanics."""

    builders = {
        "PX01": _px01,
        "PX02": _px02,
        "PX03": _px03,
        "PX04": _px04,
        "PX05": _px05,
        "PX06": _px06,
        "PX07": _px07,
        "PX08": _px08,
        "PX09": _px09,
        "PX10": _px10,
        "PX11": _px11,
        "PX12": _px12,
    }
    execution = builders[row.primary](row)
    if not isinstance(execution.result, program.ApplicationComplete):
        fault = execution.result.fault
        raise AssertionError(
            f"{row.spf}/{row.fixture} rejected: {fault.reason}; "
            f"{fault.evidence!r}"
        )
    return execution


def run_secondary_fixture(row: MechanicsRow, pressure: str) -> MechanicsRun:
    """Exercise one of the eight deliberate cross-pressure joins."""

    if pressure not in row.secondary:
        raise ValueError(f"{row.spf} has no declared {pressure} secondary join")
    secondary_row = MechanicsRow(
        row.spf,
        row.family,
        row.name,
        row.workstream,
        pressure,
        f"{row.fixture}:secondary-{pressure.lower()}",
    )
    builders = {
        "PX03": _px03,
        "PX04": _px04,
        "PX08": _px08,
    }
    execution = builders[pressure](secondary_row)
    if not isinstance(execution.result, program.ApplicationComplete):
        fault = execution.result.fault
        raise AssertionError(
            f"{row.spf}/{pressure} secondary fixture rejected: "
            f"{fault.reason}; {fault.evidence!r}"
        )
    return execution


def _finite_successors(
    result: program.ApplicationComplete,
) -> tuple[loci.FiniteConfiguration, ...]:
    return tuple(
        group.successor
        for group in result.successor_quotient_with_derivation_fibers.atoms
        if isinstance(group.successor, loci.FiniteConfiguration)
    )


def assert_mechanics_run(
    execution: MechanicsRun,
    *,
    pressure: str | None = None,
) -> None:
    """Assert the pressure-specific invariant, not merely a successful call."""

    row = execution.row
    pressure = row.primary if pressure is None else pressure
    result = execution.result
    assert type(execution.simple_program) is ca.SimpleProgram
    assert isinstance(result, program.ApplicationComplete)
    assert result.evidence.program_identity == execution.simple_program.canonical_identity
    assert result.evidence.input_configuration_identity == execution.source.identity

    successors = _finite_successors(result)
    derivations = tuple(
        atom
        for atom in result.applied_atoms.atoms
        if isinstance(atom, program.AppliedDerivation)
    )

    if pressure == "PX01":
        assert derivations
        for derivation in derivations:
            before = dict(execution.source.entries)
            after = dict(derivation.successor.entries)
            changed = {
                target
                for target in before
                if before.get(target) != after.get(target)
            }
            assert len(changed) >= 2
        if row.spf == "SPF030":
            assert rules.cardinality_size(result.derivation_cardinality) == 2
            assert rules.cardinality_size(result.successor_cardinality) == 2
        return

    if pressure == "PX02":
        delete_count, create_count = _PX02_SHAPES[row.spf]
        assert len(derivations) == 1
        derivation = derivations[0]
        assert len(derivation.fresh_bindings) == create_count
        successor = derivation.successor
        assert isinstance(successor, loci.FiniteConfiguration)
        assert len(successor.entries) == (
            len(execution.source.entries) - delete_count + create_count
        )
        assert successor.contract.kind is loci.CarrierKind.WORD
        return

    if pressure == "PX03":
        assert len(successors) == 1
        values = tuple(value for _, value in successors[0].entries)
        assert values[-1] == sum(
            value for _, value in execution.source.entries[:3]
        )
        return

    if pressure == "PX04":
        expected = {
            "SPF014": (1, 1),
            "SPF018": (2, 2),
            "SPF024": (1, 1),
            "SPF026": (0, 0),
            "SPF029": (2, 2),
            "SPF033": (2, 1),
            "SPF039": (2, 2),
        }[row.spf]
        assert rules.cardinality_size(result.derivation_cardinality) == expected[0]
        assert rules.cardinality_size(result.successor_cardinality) == expected[1]
        if expected[0] == 0:
            assert len(result.no_successor_partition.atoms) == 1
        if row.spf == "SPF033":
            fibers = result.successor_quotient_with_derivation_fibers.atoms
            assert len(fibers) == 1
            assert len(fibers[0].derivations) == 2
        return

    if pressure == "PX05":
        if row.spf == "SPF039":
            assert (
                result.source_outcomes.support.presentation
                is rules.SupportPresentation.INTENSIONAL
            )
            for cardinality in (
                result.outcome_atom_cardinality,
                result.derivation_cardinality,
                result.successor_cardinality,
            ):
                assert isinstance(cardinality, rules.Many)
                assert (
                    cardinality.infinite
                    is rules.InfiniteCardinality.UNCOUNTABLE
                )
            assert (
                result.successor_quotient_with_derivation_fibers.relation
                is not None
            )
            return
        assert len(derivations) == 1
        assert isinstance(derivations[0].source.continuation, rules.Stop)
        successor = successors[0]
        values = tuple(value for _, value in successor.entries)
        assert values == (
            Fraction(0),
            Fraction(1),
            Fraction(1, 4),
            1,
        )
        return

    if pressure == "PX06":
        law = result.source_outcomes.probability_law
        assert law is not None
        assert tuple(item.mass for item in law.masses) == (
            Fraction(1, 2),
            Fraction(1, 2),
        )
        assert isinstance(result.applied_atom_measure, program.MeasureAvailable)
        assert result.applied_atom_measure.measure.total_mass == Fraction(1)
        assert isinstance(result.successor_submeasure, program.MeasureAvailable)
        assert result.successor_submeasure.measure.total_mass == Fraction(1)
        return

    if pressure == "PX07":
        assert len(successors) == 1
        assert tuple(value for _, value in successors[0].entries) == (0, 31, 1)
        return

    if pressure == "PX08":
        assert len(derivations) == 1
        assert isinstance(derivations[0].source.continuation, rules.Stop)
        return

    if pressure == "PX10":
        assert len(derivations) == 1
        assert isinstance(derivations[0].source.continuation, rules.Stop)
        representation = execution.representation
        assert representation is not None
        assert representation.profile is alphabets.RepresentationProfile.EXACT
        encoded = representation.forward(1)
        assert representation.inverse(encoded) == 1
        assert tuple(value for _, value in successors[0].entries) == (1, encoded)
        return

    if pressure == "PX09":
        assert len(successors) == 1
        assert tuple(value for _, value in successors[0].entries) == (
            True,
            True,
            True,
        )
        assert isinstance(derivations[0].source.continuation, rules.Stop)
        return

    if pressure == "PX11":
        assert len(successors) == 1
        assert tuple(value for _, value in successors[0].entries) == (1, 0, 0, 1)
        return

    if pressure == "PX12":
        assert len(derivations) == 1
        assert isinstance(derivations[0].source.continuation, rules.Stop)
        if row.spf == "SPF004":
            assert len(derivations[0].fresh_bindings) == 1
        return

    raise AssertionError(f"missing pressure assertion for {pressure}")


def _ct12_expr(
    tag: str,
    *arguments: rules.RuleScalar | rules.RuleExpr,
) -> rules.RuleExpr:
    """Build inert semantic syntax independently of the frozen oracle module."""

    return rules.RuleExpr(
        rules.ExpressionPrimitive.TUPLE,
        (
            rules.literal_expr(tag),
            *(
                argument
                if isinstance(argument, rules.RuleExpr)
                else rules.literal_expr(argument)
                for argument in arguments
            ),
        ),
    )


def _ct12_value(
    tag: str,
    *items: alphabets.SemanticValue,
    kind: alphabets.ValueKind = alphabets.ValueKind.SYMBOLIC,
) -> alphabets.ValueNode:
    return alphabets.ValueNode(kind, tag, items=items)


def _ct12_certificate(
    kind: rules.CertificateKind,
    statement: rules.RuleExpr,
) -> rules.Certificate:
    return rules.Certificate(kind, statement)


def _ct12_witness(statement: rules.RuleExpr) -> rules.Witness:
    return rules.Witness(loci.canonical_identity(statement), statement)


def _ct12_stop() -> rules.Stop:
    return rules.Stop(
        rules.literal_expr("completed"),
        _ct12_certificate(
            rules.CertificateKind.TERMINALITY,
            _ct12_expr("terminal", "completed"),
        ),
    )


def _ct12_total_disposition(
    writable: frontiers.WritableCapabilities,
    *,
    existing: tuple[
        tuple[int, rules.DispositionAction, alphabets.SemanticValue | None],
        ...,
    ] = (),
    fresh: tuple[
        tuple[int, rules.DispositionAction, alphabets.SemanticValue | None],
        ...,
    ] = (),
) -> rules.TotalDisposition:
    existing_overrides = {index: (action, value) for index, action, value in existing}
    fresh_overrides = {index: (action, value) for index, action, value in fresh}
    if len(existing_overrides) != len(existing):
        raise ValueError("CT12 existing disposition indices repeat")
    if len(fresh_overrides) != len(fresh):
        raise ValueError("CT12 fresh disposition indices repeat")

    existing_dispositions = []
    for index, capability in enumerate(writable.existing):
        action, value = existing_overrides.get(
            index,
            (rules.DispositionAction.PRESERVE, None),
        )
        if action is rules.DispositionAction.PRESERVE:
            existing_dispositions.append(rules.preserve(capability.target))
        elif action is rules.DispositionAction.REPLACE:
            assert value is not None
            existing_dispositions.append(rules.replace(capability.target, value))
        elif action is rules.DispositionAction.DELETE:
            assert value is None
            existing_dispositions.append(rules.delete(capability.target))
        else:
            raise ValueError("CT12 existing disposition action is invalid")

    fresh_dispositions = []
    for index, capability in enumerate(writable.fresh):
        action, value = fresh_overrides.get(
            index,
            (rules.DispositionAction.ABSENT, None),
        )
        if action is rules.DispositionAction.ABSENT:
            fresh_dispositions.append(rules.absent(capability.target))
        elif action is rules.DispositionAction.CREATE:
            assert value is not None
            fresh_dispositions.append(rules.create(capability.target, value))
        else:
            raise ValueError("CT12 fresh disposition action is invalid")

    return rules.TotalDisposition(
        tuple(existing_dispositions),
        tuple(fresh_dispositions),
        _ct12_certificate(
            rules.CertificateKind.TOTALITY,
            _ct12_expr("totality", "complete-writable-envelope"),
        ),
    )


def _ct12_derivation(
    writable: frontiers.WritableCapabilities,
    *,
    witness: rules.RuleExpr,
    provenance: tuple[str, ...],
    certificate: rules.RuleExpr,
    existing: tuple[
        tuple[int, rules.DispositionAction, alphabets.SemanticValue | None],
        ...,
    ] = (),
    fresh: tuple[
        tuple[int, rules.DispositionAction, alphabets.SemanticValue | None],
        ...,
    ] = (),
    stop: bool = False,
) -> rules.Derivation:
    return rules.Derivation(
        _ct12_total_disposition(
            writable,
            existing=existing,
            fresh=fresh,
        ),
        rules.Progress.ADVANCED,
        _ct12_stop() if stop else rules.Continue(),
        _ct12_witness(witness),
        provenance,
        _ct12_certificate(rules.CertificateKind.DERIVATION, certificate),
    )


def _ct12_no_successor(
    *,
    witness: rules.RuleExpr,
    provenance: tuple[str, ...],
    reason: rules.RuleExpr,
    certificate: rules.RuleExpr,
) -> rules.NoSuccessor:
    return rules.NoSuccessor(
        rules.NoSuccessorOutcome.TERMINAL,
        reason,
        _ct12_witness(witness),
        provenance,
        _ct12_certificate(rules.CertificateKind.TERMINALITY, certificate),
    )


def _ct12_literal_run(
    row: MechanicsRow,
    source: loci.FiniteConfiguration,
    alphabet: alphabets.Alphabet,
    writable: frontiers.WritableRegion,
    readable: neighborhoods.ReadableRegion,
    atoms: tuple[rules.Derivation | rules.NoSuccessor, ...],
    *,
    masses: tuple[Fraction, ...] | None = None,
) -> MechanicsRun:
    law = (
        None
        if masses is None
        else rules.finite_probability_law(
            tuple(zip(atoms, masses, strict=True))
        )
    )
    rule = rules.finite_rule(
        atoms,
        contract=_contract(
            source,
            alphabet,
            writable,
            readable,
            stochastic=masses is not None,
        ),
        probability_law=law,
        label="ct12-independent-literal",
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _ct12_mobile() -> MechanicsRun:
    row = next(row for row in MECHANICS_ROWS if row.spf == "SPF030")
    head_q1 = _ct12_value("head", "q", 1)
    head_p0 = _ct12_value("head", "p", 0)
    source = loci.history_configuration((0, head_q1, 0))
    alphabet = alphabets.enum((0, head_q1, head_p0))
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    capabilities = writable.resolve(source)
    left = _ct12_derivation(
        capabilities,
        witness=_ct12_expr("transition-witness", "q", 1, "p", 0, "left"),
        provenance=("PX01:F031", "transition:left"),
        certificate=_ct12_expr("single-head-certificate", -1),
        existing=(
            (0, rules.DispositionAction.REPLACE, head_p0),
            (1, rules.DispositionAction.REPLACE, 0),
        ),
    )
    right = _ct12_derivation(
        capabilities,
        witness=_ct12_expr("transition-witness", "q", 1, "p", 0, "right"),
        provenance=("PX01:F031", "transition:right"),
        certificate=_ct12_expr("single-head-certificate", 1),
        existing=(
            (1, rules.DispositionAction.REPLACE, 0),
            (2, rules.DispositionAction.REPLACE, head_p0),
        ),
    )
    return _ct12_literal_run(
        row,
        source,
        alphabet,
        writable,
        readable,
        (left, right),
    )


def _ct12_substitution() -> MechanicsRun:
    row = next(row for row in MECHANICS_ROWS if row.spf == "SPF037")
    source = _word_configuration(("A", "B"))
    alphabet = alphabets.enum(("A", "B"))
    existing = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
        effects=(frontiers.Effect.REPLACE, frontiers.Effect.DELETE),
    )
    parent = source.entries[0][0]
    namespace = "px02.parallel-substitution"
    fresh = frontiers.fresh(
        loci.fresh_children(parent, namespace, ("old:0:0", "old:0:1")),
        namespace=frontiers.FreshNamespace(namespace, parent=parent),
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    writable = frontiers.union((existing, fresh))
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    capabilities = writable.resolve(source)
    atom = _ct12_derivation(
        capabilities,
        witness=_ct12_expr(
            "generation-witness",
            "A->AB",
            "B->epsilon",
        ),
        provenance=("PX02:F038",),
        certificate=_ct12_expr(
            "ordered-offspring-certificate",
            _ct12_expr(
                "fresh-slot",
                "offspring",
                _ct12_expr("occurrence", "old", 0),
                0,
            ),
            _ct12_expr(
                "fresh-slot",
                "offspring",
                _ct12_expr("occurrence", "old", 0),
                1,
            ),
        ),
        existing=(
            (0, rules.DispositionAction.DELETE, None),
            (1, rules.DispositionAction.DELETE, None),
        ),
        fresh=(
            (0, rules.DispositionAction.CREATE, "A"),
            (1, rules.DispositionAction.CREATE, "B"),
        ),
    )
    return _ct12_literal_run(
        row,
        source,
        alphabet,
        writable,
        readable,
        (atom,),
    )


def _ct12_multiway() -> MechanicsRun:
    row = next(row for row in MECHANICS_ROWS if row.spf == "SPF033")
    source = _word_configuration(("a",))
    alphabet = alphabets.enum(("a", "b"))
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    capabilities = writable.resolve(source)
    atoms = tuple(
        _ct12_derivation(
            capabilities,
            witness=_ct12_expr(
                "rewrite-witness",
                f"rule-{side}",
                "match:0",
                "parent:a",
            ),
            provenance=("PX04:F034", f"rule:{side}"),
            certificate=_ct12_expr(
                "rewrite-certificate",
                "a->b",
                side,
            ),
            existing=((0, rules.DispositionAction.REPLACE, "b"),),
        )
        for side in ("left", "right")
    )
    return _ct12_literal_run(
        row,
        source,
        alphabet,
        writable,
        readable,
        atoms,
    )


def _ct12_constraint(rhs: int) -> MechanicsRun:
    row = next(row for row in MECHANICS_ROWS if row.spf == "SPF018")
    source = loci.record_configuration(
        (
            ("domain", "Z/3Z"),
            ("equation", "x^2=rhs"),
            ("rhs", rhs),
            ("x", "unset"),
        )
    )
    alphabet = alphabets.enum(("Z/3Z", "x^2=rhs", "unset", 0, 1, 2))
    x_target = next(
        target for target, _ in source.entries if target.path[-1] == "x"
    )
    writable = frontiers.literal(
        (x_target,),
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    capabilities = writable.resolve(source)
    if rhs == 2:
        atoms: tuple[rules.Derivation | rules.NoSuccessor, ...] = (
            _ct12_no_successor(
                witness=_ct12_expr("relation-witness", "x^2=2", "Z/3Z"),
                provenance=("PX04:F019", "rhs=2"),
                reason=_ct12_expr("terminal", "no-solution"),
                certificate=_ct12_expr(
                    "truth-table",
                    _ct12_expr(
                        "row",
                        0,
                        _ct12_expr("square-residue", 0),
                        False,
                    ),
                    _ct12_expr(
                        "row",
                        1,
                        _ct12_expr("square-residue", 1),
                        False,
                    ),
                    _ct12_expr(
                        "row",
                        2,
                        _ct12_expr("square-residue", 1),
                        False,
                    ),
                ),
            ),
        )
    else:
        solutions = (0,) if rhs == 0 else (1, 2)
        atoms = tuple(
            _ct12_derivation(
                capabilities,
                witness=_ct12_expr("solution-witness", "x", solution),
                provenance=("PX04:F019", f"rhs={rhs}"),
                certificate=_ct12_expr(
                    "equation-certificate",
                    f"{solution}^2={rhs} mod 3",
                ),
                existing=(
                    (0, rules.DispositionAction.REPLACE, solution),
                ),
                stop=True,
            )
            for solution in solutions
        )
    return _ct12_literal_run(
        row,
        source,
        alphabet,
        writable,
        readable,
        atoms,
    )


def _ct12_graph() -> MechanicsRun:
    row = next(row for row in MECHANICS_ROWS if row.spf == "SPF028")
    node_a = loci.graph_element("node", "a")
    node_b = loci.graph_element("node", "b")
    node_c = loci.graph_element("node", "c")
    edge_ab = loci.graph_element("edge", "a-b")
    edge_bc = loci.graph_element("edge", "b-c")
    node = lambda label: _ct12_value(  # noqa: E731
        "node-value",
        label,
        kind=alphabets.ValueKind.GRAPH,
    )
    edge = lambda left, right: _ct12_value(  # noqa: E731
        "edge-value",
        left,
        right,
        kind=alphabets.ValueKind.GRAPH,
    )
    contract = loci.CarrierContract(loci.CarrierKind.GRAPH)
    source = loci.FiniteConfiguration(
        loci.Carrier(contract, loci.Boundary(loci.BoundaryPolicy.NONE)),
        (
            (node_a, node("a")),
            (node_b, node("b")),
            (node_c, node("c")),
            (
                edge_ab,
                edge(
                    alphabets.StructuralReference(node_a),
                    alphabets.StructuralReference(node_b),
                ),
            ),
            (
                edge_bc,
                edge(
                    alphabets.StructuralReference(node_b),
                    alphabets.StructuralReference(node_c),
                ),
            ),
        ),
    )
    alphabet = alphabets.graph()
    existing = frontiers.literal(
        (node_b, edge_ab, edge_bc),
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
        effects=(frontiers.Effect.REPLACE, frontiers.Effect.DELETE),
    )
    namespace = "px02.graph-interface-replacement"
    fresh_nodes = frontiers.fresh(
        loci.fresh_children(node_b, namespace, ("x", "y")),
        namespace=frontiers.FreshNamespace(namespace, parent=node_b),
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    fresh_edges = frontiers.fresh(
        loci.fresh_edges(
            (node_a, node_c),
            namespace,
            ("a-x", "x-y", "y-c"),
        ),
        namespace=frontiers.FreshNamespace(namespace),
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    writable = frontiers.union((existing, fresh_nodes, fresh_edges))
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    capabilities = writable.resolve(source)
    fresh_by_key = {
        capability.target.local_key: (index, capability.target)
        for index, capability in enumerate(capabilities.fresh)
    }
    x_index, x_ref = fresh_by_key["x"]
    y_index, y_ref = fresh_by_key["y"]
    ax_index, _ = fresh_by_key["a-x"]
    xy_index, _ = fresh_by_key["x-y"]
    yc_index, _ = fresh_by_key["y-c"]
    existing_index = {
        capability.target: index
        for index, capability in enumerate(capabilities.existing)
    }
    atom = _ct12_derivation(
        capabilities,
        witness=_ct12_expr(
            "match",
            _ct12_expr("node", "b"),
            _ct12_expr("ports", "a", "c"),
        ),
        provenance=("PX02:F029",),
        certificate=_ct12_expr(
            "interface-certificate",
            _ct12_expr("external", "a", "c"),
            _ct12_expr(
                "authorized-fresh-slots",
                *(
                    _ct12_expr("fresh-slot", kind, key)
                    for kind, key in (
                        ("node", "x"),
                        ("node", "y"),
                        ("edge", "a-x"),
                        ("edge", "x-y"),
                        ("edge", "y-c"),
                    )
                ),
            ),
        ),
        existing=tuple(
            (
                existing_index[target],
                rules.DispositionAction.DELETE,
                None,
            )
            for target in (node_b, edge_ab, edge_bc)
        ),
        fresh=(
            (x_index, rules.DispositionAction.CREATE, node("x")),
            (y_index, rules.DispositionAction.CREATE, node("y")),
            (
                ax_index,
                rules.DispositionAction.CREATE,
                edge(
                    alphabets.StructuralReference(node_a),
                    alphabets.StructuralReference(x_ref),
                ),
            ),
            (
                xy_index,
                rules.DispositionAction.CREATE,
                edge(
                    alphabets.StructuralReference(x_ref),
                    alphabets.StructuralReference(y_ref),
                ),
            ),
            (
                yc_index,
                rules.DispositionAction.CREATE,
                edge(
                    alphabets.StructuralReference(y_ref),
                    alphabets.StructuralReference(node_c),
                ),
            ),
        ),
    )
    return _ct12_literal_run(
        row,
        source,
        alphabet,
        writable,
        readable,
        (atom,),
    )


def _ct12_stochastic() -> MechanicsRun:
    """The exact mixed search law: accept, reject-and-count, or no proposal."""

    row = next(row for row in MECHANICS_ROWS if row.spf == "SPF047")
    plain_source = loci.record_configuration((("x", 0), ("k", 0)))
    source = loci.FiniteConfiguration(
        loci.Carrier(
            plain_source.contract,
            plain_source.carrier.boundary,
            (
                ("objective", "(x-1)^2"),
                ("proposal-law", "closed"),
            ),
        ),
        plain_source.entries,
    )
    alphabet = alphabets.integers()
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    capabilities = writable.resolve(source)
    by_name = {
        str(capability.target.path[-1]): index
        for index, capability in enumerate(capabilities.existing)
    }
    accepted = _ct12_derivation(
        capabilities,
        witness=_ct12_expr("proposal-witness", 1, "accepted"),
        provenance=("PX06:F050",),
        certificate=_ct12_expr(
            "law-atom-certificate",
            "accept",
            Fraction(1, 2),
        ),
        existing=(
            (by_name["x"], rules.DispositionAction.REPLACE, 1),
            (by_name["k"], rules.DispositionAction.REPLACE, 1),
        ),
    )
    rejected = _ct12_derivation(
        capabilities,
        witness=_ct12_expr("proposal-witness", 0, "rejected"),
        provenance=("PX06:F050",),
        certificate=_ct12_expr(
            "law-atom-certificate",
            "reject",
            Fraction(1, 4),
        ),
        existing=(
            (by_name["k"], rules.DispositionAction.REPLACE, 1),
        ),
    )
    absent_proposal = _ct12_no_successor(
        witness=_ct12_expr("proposal-witness", "none"),
        provenance=("PX06:F050",),
        reason=_ct12_expr("terminal", "no-proposal"),
        certificate=_ct12_expr(
            "law-atom-certificate",
            "no-proposal",
            Fraction(1, 4),
        ),
    )
    return _ct12_literal_run(
        row,
        source,
        alphabet,
        writable,
        readable,
        (accepted, rejected, absent_proposal),
        masses=(Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)),
    )


def _ct12_flow() -> MechanicsRun:
    """One exact maximal solution object selected by closed differential data."""

    row = next(row for row in MECHANICS_ROWS if row.spf == "SPF036")
    equation = _ct12_value("derivative-equals", "x", "t", 1)
    initial = _ct12_value("initial-condition", "x", 0, 0)
    solution = _ct12_value(
        "maximal-solution",
        _ct12_value("binder", "t", "exact-real"),
        _ct12_value("equals", _ct12_value("x-of", "t"), "t"),
        kind=alphabets.ValueKind.FIELD,
    )
    plain_source = loci.record_configuration(
        (
            ("equation", equation),
            ("initial", initial),
            ("solution", "unset"),
        )
    )
    source = loci.FiniteConfiguration(
        loci.Carrier(
            plain_source.contract,
            plain_source.carrier.boundary,
            (("duration-or-event-selector", "none"),),
        ),
        plain_source.entries,
    )
    alphabet = alphabets.enum((equation, initial, "unset", solution))
    solution_target = next(
        target for target, _ in source.entries if target.path[-1] == "solution"
    )
    writable = frontiers.literal(
        (solution_target,),
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    capabilities = writable.resolve(source)
    atom = _ct12_derivation(
        capabilities,
        witness=_ct12_expr(
            "differential-proof",
            _ct12_expr("derivative-of", "t", "t", 1),
            _ct12_expr("initial-value", 0, 0),
            _ct12_expr("coverage", "maximal-exact-real-solution"),
        ),
        provenance=("PX05:F037",),
        certificate=_ct12_expr(
            "equation-and-initial-condition-certificate",
            "exact",
        ),
        existing=((0, rules.DispositionAction.REPLACE, solution),),
        stop=True,
    )
    return _ct12_literal_run(
        row,
        source,
        alphabet,
        writable,
        readable,
        (atom,),
    )


def _ct12_intensional() -> MechanicsRun:
    row = next(row for row in MECHANICS_ROWS if row.spf == "SPF039")
    domain = _ct12_value(
        "closed-interval",
        0,
        1,
        kind=alphabets.ValueKind.FIELD,
    )
    unknown = _ct12_value(
        "unknown-field",
        "u",
        kind=alphabets.ValueKind.FIELD,
    )
    contract = loci.CarrierContract(loci.CarrierKind.FIELD)
    domain_target = loci.named("domain", scope="field")
    u_target = loci.named("u", scope="field")
    source = loci.FiniteConfiguration(
        loci.Carrier(
            contract,
            loci.Boundary(loci.BoundaryPolicy.NONE),
            (
                ("differential-germ", "du/dx=0"),
                ("side-data", "none"),
            ),
        ),
        ((domain_target, domain), (u_target, unknown)),
    )
    alphabet = alphabets.field()
    writable = frontiers.literal(
        (u_target,),
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    field_u = _ct12_expr("field-capability", "u")
    relation = _ct12_expr(
        "intensional-source-outcome-relation",
        _ct12_expr("binder", "c"),
        _ct12_expr("domain", "exact-real"),
        _ct12_expr(
            "source-derivation-template",
            _ct12_expr(
                "atom-id",
                _ct12_expr("parameterized", "constant-field", "c"),
            ),
            _ct12_expr(
                "total-disposition",
                _ct12_expr(
                    "replace",
                    field_u,
                    _ct12_expr("constant-field", "c"),
                ),
            ),
            _ct12_expr(
                "witness",
                _ct12_expr("derivative", "u", "x"),
                0,
            ),
            _ct12_expr("stop", "completed"),
        ),
    )
    uncountable = rules.Many(
        None,
        rules.InfiniteCardinality.UNCOUNTABLE,
        _certificate(
            rules.CertificateKind.CARDINALITY,
            "constant-field:uncountable",
        ),
    )
    rule = rules.differential(
        relation,
        uncountable,
        contract=_contract(source, alphabet, writable, readable),
        completeness_evidence=_certificate(
            rules.CertificateKind.COMPLETENESS,
            "constant-field:complete",
        ),
        soundness_evidence=_certificate(
            rules.CertificateKind.SOUNDNESS,
            "constant-field:sound",
        ),
        projection_cardinalities=rules.ProjectionCardinalities(
            uncountable,
            rules.finite_cardinality(0),
            uncountable,
            _certificate(
                rules.CertificateKind.COMPOSITION,
                "constant-field:injective-total-projection",
            ),
        ),
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def runtime_ct12_fixture(case_id: str) -> MechanicsRun:
    """Build one of the ten frozen non-native CT12 mechanics cases."""

    builders = {
        "px01.mobile-head-branching": _ct12_mobile,
        "px02.parallel-substitution": _ct12_substitution,
        "px04.multiway-diamond": _ct12_multiway,
        "px04.constraint-mod3-zero": lambda: _ct12_constraint(2),
        "px04.constraint-mod3-one": lambda: _ct12_constraint(0),
        "px04.constraint-mod3-many": lambda: _ct12_constraint(1),
        "px02.graph-interface-replacement": _ct12_graph,
        "px06.stochastic-search-law": _ct12_stochastic,
        "px05.exact-differential-flow": _ct12_flow,
        "px05.constant-field-intensional": _ct12_intensional,
    }
    try:
        execution = builders[case_id]()
    except KeyError as error:
        raise ValueError(f"unknown CT12 mechanics case {case_id!r}") from error
    if not isinstance(execution.result, program.ApplicationComplete):
        raise AssertionError(
            f"{case_id} rejected: {execution.result.fault.reason}"
        )
    return execution
