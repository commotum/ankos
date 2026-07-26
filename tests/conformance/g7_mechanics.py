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
    representation_case_index: int = 0
    trajectory: tuple[
        tuple[Configuration, program.ApplicationComplete],
        ...,
    ] = ()


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


def _total_existing_plans(
    targets: tuple[loci.Locus, ...],
    replacements: tuple[tuple[loci.Locus, rules.RuleExpr], ...],
) -> tuple[rules.ExistingDispositionPlan, ...]:
    """Preserve every writable target not replaced by one trajectory step."""

    replacement_by_target = dict(replacements)
    return tuple(
        _existing_target_plan(
            target,
            (
                rules.DispositionAction.REPLACE
                if target in replacement_by_target
                else rules.DispositionAction.PRESERVE
            ),
            replacement_by_target.get(target),
        )
        for target in targets
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
    representation_case_index: int = 0,
    seed_source: Configuration | None = None,
) -> MechanicsRun:
    if seed_source is None:
        seed_source = source
    simple_program = ca.SimpleProgram(
        seeds.exact(
            seed_source,
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
        representation_case_index,
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


def _all_conditions(*conditions: rules.RuleExpr) -> rules.RuleExpr:
    return rules.gate(
        rules.RuleExpr(rules.ExpressionPrimitive.TUPLE, conditions),
        rules.GateKind.ALL,
    )


def _px01_multi_active_collision(row: MechanicsRow) -> MechanicsRun:
    """Resolve two active sources competing for one shared destination."""

    source = loci.grid_configuration(
        (5,),
        (0, 1, 0, 2, 0),
        boundary=loci.Boundary(loci.BoundaryPolicy.NONE),
    )
    alphabet = alphabets.integers()
    (
        priority,
        source_a,
        destination,
        source_b,
        resolution,
    ) = tuple(target for target, _ in source.entries)
    writable, readable = _literal_regions(
        source,
        alphabet,
        write_targets=(source_a, source_b, destination, resolution),
        read_targets=(source_a, source_b, destination, priority),
    )
    active_sources = (
        rules.less_than(rules.literal_expr(0), rules.observation(0)),
        rules.less_than(rules.literal_expr(0), rules.observation(1)),
    )

    def resolve_collision(
        label: str,
        selected_source: rules.RuleExpr,
        selected_marker: int,
    ) -> rules.DerivationClauseResult:
        return _derivation_result(
            f"{row.fixture}:{label}",
            existing=(
                _existing_target_plan(
                    source_a,
                    rules.DispositionAction.REPLACE,
                    rules.literal_expr(0),
                ),
                _existing_target_plan(
                    source_b,
                    rules.DispositionAction.REPLACE,
                    rules.literal_expr(0),
                ),
                _existing_target_plan(
                    destination,
                    rules.DispositionAction.REPLACE,
                    selected_source,
                ),
                _existing_target_plan(
                    resolution,
                    rules.DispositionAction.REPLACE,
                    rules.literal_expr(selected_marker),
                ),
            ),
        )

    rule = _kernel(
        source,
        alphabet,
        writable,
        readable,
        (
            _clause(
                _all_conditions(
                    *active_sources,
                    rules.equal(
                        rules.observation(3),
                        rules.literal_expr(0),
                    ),
                ),
                resolve_collision(
                    "source-a-wins",
                    rules.observation(0),
                    1,
                ),
            ),
            _clause(
                _all_conditions(*active_sources),
                resolve_collision(
                    "source-b-wins",
                    rules.observation(1),
                    2,
                ),
            ),
        ),
        selection=rules.ClauseSelection.FIRST,
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _px01_register_machine(row: MechanicsRow) -> MechanicsRun:
    """Execute one visible instruction over pc, counter, and register state."""

    source = _record_configuration(
        (
            ("pc", 0),
            ("instruction", 1),
            ("counter", 2),
            ("register", 5),
        )
    )
    alphabet = alphabets.integers()
    targets = _record_targets(source)
    read_targets = tuple(
        targets[name]
        for name in ("pc", "instruction", "counter", "register")
    )
    write_targets = tuple(
        targets[name] for name in ("pc", "counter", "register")
    )
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
                _all_conditions(
                    rules.equal(
                        rules.observation(1),
                        rules.literal_expr(1),
                    ),
                    rules.less_than(
                        rules.literal_expr(0),
                        rules.observation(2),
                    ),
                ),
                _derivation_result(
                    row.fixture,
                    existing=(
                        _existing_target_plan(
                            targets["pc"],
                            rules.DispositionAction.REPLACE,
                            rules.add(
                                rules.observation(0),
                                rules.literal_expr(1),
                            ),
                        ),
                        _existing_target_plan(
                            targets["counter"],
                            rules.DispositionAction.REPLACE,
                            rules.subtract(
                                rules.observation(2),
                                rules.literal_expr(1),
                            ),
                        ),
                        _existing_target_plan(
                            targets["register"],
                            rules.DispositionAction.REPLACE,
                            rules.add(
                                rules.observation(3),
                                rules.observation(2),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _px01(row: MechanicsRow) -> MechanicsRun:
    """Couple source, control, and every possible destination atomically."""

    if row.spf == "SPF032":
        return _px01_multi_active_collision(row)
    if row.spf == "SPF045":
        return _px01_register_machine(row)

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
    "SPF038": (2, 2),
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


def _px02_parallel_graph(row: MechanicsRow) -> MechanicsRun:
    """Commit two compatible edge rewrites as one typed network patch."""

    node_a = loci.graph_element("node", "a")
    node_b = loci.graph_element("node", "b")
    node_c = loci.graph_element("node", "c")
    node_d = loci.graph_element("node", "d")
    edge_ab = loci.graph_element("edge", "a-b")
    edge_cd = loci.graph_element("edge", "c-d")
    source = _structural_configuration(
        loci.CarrierKind.GRAPH,
        (
            (node_a, _graph_node("a")),
            (node_b, _graph_node("b")),
            (node_c, _graph_node("c")),
            (node_d, _graph_node("d")),
            (edge_ab, _graph_edge(node_a, node_b, name="a-b")),
            (edge_cd, _graph_edge(node_c, node_d, name="c-d")),
        ),
    )
    alphabet = alphabets.graph()
    existing = frontiers.literal(
        (edge_ab, edge_cd),
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
        effects=(frontiers.Effect.DELETE,),
    )
    namespace = "g7-parallel-network-edges"
    edge_ac = loci.FreshReference(
        namespace,
        "a-c",
        interface=(node_a, node_c),
    )
    edge_bd = loci.FreshReference(
        namespace,
        "b-d",
        interface=(node_b, node_d),
    )
    fresh = frontiers.fresh(
        loci.Region(
            loci.RegionKind.FRESH_EDGES,
            name=namespace,
            fresh=(edge_ac, edge_bd),
        ),
        namespace=frontiers.FreshNamespace(namespace),
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    writable = frontiers.union((existing, fresh))
    readable = neighborhoods.literal(
        (node_a, node_b, node_c, node_d, edge_ab, edge_cd),
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
        key="two-compatible-network-matches",
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
                            edge_ab,
                            rules.DispositionAction.DELETE,
                        ),
                        _existing_target_plan(
                            edge_cd,
                            rules.DispositionAction.DELETE,
                        ),
                    ),
                    fresh=(
                        _fresh_target_plan(
                            edge_ac,
                            rules.DispositionAction.CREATE,
                            rules.literal_expr(
                                _graph_edge(node_a, node_c, name="a-c")
                            ),
                        ),
                        _fresh_target_plan(
                            edge_bd,
                            rules.DispositionAction.CREATE,
                            rules.literal_expr(
                                _graph_edge(node_b, node_d, name="b-d")
                            ),
                        ),
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
    if row.spf == "SPF038":
        return _px02_parallel_graph(row)

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


def _causal_event(name: str, time: int, position: int) -> alphabets.ValueNode:
    return alphabets.ValueNode(
        alphabets.ValueKind.GRAPH,
        "event",
        fields=(
            ("name", name),
            ("position", position),
            ("time", time),
        ),
    )


def _px03_causal_cover(row: MechanicsRow) -> MechanicsRun:
    """Construct the causal cover relation from the complete event set."""

    event_0 = loci.graph_element("node", "event/e0")
    event_1 = loci.graph_element("node", "event/e1")
    event_2 = loci.graph_element("node", "event/e2")
    source = _structural_configuration(
        loci.CarrierKind.GRAPH,
        (
            (event_0, _causal_event("e0", 0, 0)),
            (event_1, _causal_event("e1", 1, 1)),
            (event_2, _causal_event("e2", 2, 1)),
        ),
    )
    alphabet = alphabets.graph()
    namespace = "g7-causal-cover-edges"
    causal_01 = loci.FreshReference(
        namespace,
        "e0->e1",
        interface=(event_0, event_1),
    )
    causal_12 = loci.FreshReference(
        namespace,
        "e1->e2",
        interface=(event_1, event_2),
    )
    writable = frontiers.fresh(
        loci.Region(
            loci.RegionKind.FRESH_EDGES,
            name=namespace,
            fresh=(causal_01, causal_12),
        ),
        namespace=frontiers.FreshNamespace(namespace),
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
        key="complete-event-set",
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
                    fresh=(
                        _fresh_target_plan(
                            causal_01,
                            rules.DispositionAction.CREATE,
                            rules.literal_expr(
                                _graph_edge(event_0, event_1, name="e0->e1")
                            ),
                        ),
                        _fresh_target_plan(
                            causal_12,
                            rules.DispositionAction.CREATE,
                            rules.literal_expr(
                                _graph_edge(event_1, event_2, name="e1->e2")
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _px03(row: MechanicsRow) -> MechanicsRun:
    """Use the complete immutable snapshot in one coupled global decision."""

    if row.spf == "SPF046":
        return _px03_causal_cover(row)

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
        source = _record_configuration(
            (
                ("domain_size", 1),
                ("required_p0", 1),
                ("p0", -1),
                ("model_complete", 0),
            )
        )
        targets = _record_targets(source)
        read_targets = (targets["domain_size"], targets["required_p0"])
        write_targets = (targets["p0"], targets["model_complete"])
        alternatives = (
            (
                (targets["p0"], 1),
                (targets["model_complete"], 1),
            ),
        )
    elif row.spf == "SPF018":
        source = _record_configuration((("rhs", 1), ("x", -1), ("y", -1)))
        targets = _record_targets(source)
        read_targets = (targets["rhs"], targets["x"], targets["y"])
        write_targets = (targets["x"], targets["y"])
        alternatives = (
            ((targets["x"], 0), (targets["y"], 1)),
            ((targets["x"], 1), (targets["y"], 0)),
        )
    elif row.spf == "SPF024":
        source = loci.grid_configuration(
            (5,),
            (1, 0, -1, -1, 0),
            boundary=loci.Boundary(loci.BoundaryPolicy.NONE),
        )
        (
            observed_left,
            observed_right,
            predecessor_left,
            predecessor_right,
            cursor,
        ) = tuple(target for target, _ in source.entries)
        read_targets = (observed_left, observed_right)
        write_targets = (predecessor_left, predecessor_right, cursor)
        alternatives = (
            (
                (predecessor_left, 0),
                (predecessor_right, 1),
                (cursor, 1),
            ),
        )
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
            ("rule_version", 0),
            ("phase", 0),
        )
        read_names = (
            "cell",
            "mutable_rule_entry",
            "rule_version",
            "phase",
        )
        replacements = (
            ("cell", 0),
            ("mutable_rule_entry", 31),
            ("rule_version", 1),
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
    if row.spf == "SPF034":
        condition = _all_conditions(
            rules.equal(rules.observation(0), rules.literal_expr(1)),
            rules.equal(rules.observation(1), rules.literal_expr(30)),
        )
        replacement_expressions = (
            ("cell", rules.literal_expr(0)),
            (
                "mutable_rule_entry",
                rules.add(
                    rules.observation(1),
                    rules.literal_expr(1),
                ),
            ),
            (
                "rule_version",
                rules.add(
                    rules.observation(2),
                    rules.literal_expr(1),
                ),
            ),
            (
                "phase",
                rules.add(
                    rules.observation(3),
                    rules.literal_expr(1),
                ),
            ),
        )
    else:
        condition = rules.literal_expr(1)
        replacement_expressions = tuple(
            (name, rules.literal_expr(value))
            for name, value in replacements
        )
    rule = _kernel(
        source,
        alphabet,
        writable,
        readable,
        (
            _clause(
                condition,
                _derivation_result(
                    row.fixture,
                    existing=tuple(
                        _existing_target_plan(
                            targets[name],
                            rules.DispositionAction.REPLACE,
                            expression,
                        )
                        for name, expression in replacement_expressions
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
            (
                ("query_hash", 0),
                ("bucket_key", 0),
                ("bucket_value", 7),
                ("result", -1),
                ("phase", 0),
            ),
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


def _exact_representation(
    source_value: alphabets.SemanticValue,
    target_value: alphabets.SemanticValue,
    alternate_source: alphabets.SemanticValue,
    alternate_target: alphabets.SemanticValue,
) -> alphabets.RepresentationRelation:
    """Build one exact two-point relation with a complete inverse on image."""

    source_schema = alphabets.enum((source_value, alternate_source)).descriptor
    target_schema = alphabets.enum((target_value, alternate_target)).descriptor
    relation = (
        alphabets.RepresentationPair(source_value, target_value),
        alphabets.RepresentationPair(alternate_source, alternate_target),
    )
    return alphabets.RepresentationRelation(
        source_schema,
        target_schema,
        alphabets.RepresentationProfile.EXACT,
        relation,
        (target_value, alternate_target),
        (
            alphabets.RepresentationPair(target_value, source_value),
            alphabets.RepresentationPair(alternate_target, alternate_source),
        ),
    )


def _codec_word(tag: str, *items: alphabets.SemanticValue) -> alphabets.ValueNode:
    return alphabets.ValueNode(alphabets.ValueKind.WORD, tag, items=items)


def _codec_record(
    tag: str,
    **fields: alphabets.SemanticValue,
) -> alphabets.ValueNode:
    return alphabets.ValueNode(
        alphabets.ValueKind.RECORD,
        tag,
        fields=tuple(fields.items()),
    )


def _run_record(symbol: str, length: int) -> alphabets.ValueNode:
    return _codec_record(
        "run-record",
        symbol=symbol,
        length=length,
    )


def _literal_history_record(symbol: str) -> alphabets.ValueNode:
    return _codec_record("literal-record", symbol=symbol)


def _reference_history_record(offset: int, length: int) -> alphabets.ValueNode:
    return _codec_record(
        "reference-record",
        offset=offset,
        length=length,
    )


def _codec_product(
    tag: str,
    *items: alphabets.SemanticValue,
) -> alphabets.ValueNode:
    return alphabets.ValueNode(alphabets.ValueKind.PRODUCT, tag, items=items)


def _closed_enum(
    values: tuple[alphabets.SemanticValue, ...],
) -> alphabets.Alphabet:
    distinct: list[alphabets.SemanticValue] = []
    for value in values:
        if not any(alphabets.semantic_equal(value, prior) for prior in distinct):
            distinct.append(value)
    return alphabets.enum(tuple(distinct))


def _representation_case(
    primary_source: alphabets.SemanticValue,
    primary_target: alphabets.SemanticValue,
    alternate_source: alphabets.SemanticValue,
    alternate_target: alphabets.SemanticValue,
    case_index: int,
) -> tuple[alphabets.SemanticValue, alphabets.SemanticValue]:
    """Select one of the two declared PX10 relation pairs exactly."""

    if type(case_index) is not int or case_index not in (0, 1):
        raise ValueError("PX10 representation case index must be 0 or 1")
    if case_index == 0:
        return primary_source, primary_target
    return alternate_source, alternate_target


def _px10(row: MechanicsRow, *, case_index: int = 0) -> MechanicsRun:
    """Run either declared pair through one of eight distinct workspaces."""

    unset = _codec_record("unset", status="unset")
    fresh_parent: loci.Locus | None = None
    fresh_namespace = ""
    fresh_keys: tuple[loci.ClosedScalar, ...] = ()
    fresh_values: tuple[alphabets.SemanticValue, ...] = ()
    additional_future_values: tuple[alphabets.SemanticValue, ...] = ()
    custom_clauses: tuple[rules.RuleClause, ...] | None = None
    trajectory_steps = 1
    rule_condition = rules.literal_expr(1)
    program_seed_source: Configuration | None = None
    program_domain_values: tuple[alphabets.SemanticValue, ...] = ()
    if row.spf == "SPF012":
        native = _codec_word("source-word", "A", "A", "A", "B", "B")
        encoded = _codec_record("run-records", run0="A:3", run1="B:2")
        alternate_native = _codec_word("source-word", "B")
        alternate_encoded = _codec_record("run-records", run0="B:1")
        selected_native, selected_encoded = _representation_case(
            native,
            encoded,
            alternate_native,
            alternate_encoded,
            case_index,
        )
        primary_symbols = ("A", "A", "A", "B", "B")
        alternate_symbols = ("B", "<end>", "<end>", "<end>", "<end>")
        symbols = primary_symbols if case_index == 0 else alternate_symbols

        def run_source(values: tuple[str, ...]) -> loci.FiniteConfiguration:
            return _record_configuration(
                (
                    *tuple(
                        (f"symbol{index}", symbol)
                        for index, symbol in enumerate(values)
                    ),
                    ("run0", unset),
                    ("run1", unset),
                    ("cursor", 0),
                )
            )

        program_seed_source = run_source(primary_symbols)
        source = run_source(symbols)
        targets = _record_targets(source)
        symbol_targets = tuple(
            targets[f"symbol{index}"]
            for index in range(5)
        )
        read_targets = (
            *symbol_targets,
            targets["cursor"],
        )
        primary_run0 = _run_record("A", 3)
        primary_run1 = _run_record("B", 2)
        alternate_run0 = _run_record("B", 1)
        writes = (
            (targets["run0"], rules.literal_expr(primary_run0)),
            (targets["run1"], rules.literal_expr(primary_run1)),
            (targets["cursor"], rules.literal_expr("done")),
        )
        writable_targets = tuple(target for target, _ in writes)

        def symbol_case(
            expected: tuple[str, ...],
        ) -> rules.RuleExpr:
            return _all_conditions(
                *(
                    rules.equal(
                        rules.observation(index),
                        rules.literal_expr(symbol),
                    )
                    for index, symbol in enumerate(expected)
                ),
                rules.equal(rules.observation(5), rules.literal_expr(0)),
            )

        custom_clauses = (
            _clause(
                _all_conditions(
                    symbol_case(primary_symbols),
                    rules.equal(rules.observation(0), rules.observation(1)),
                    rules.equal(rules.observation(1), rules.observation(2)),
                    rules.equal(
                        rules.equal(rules.observation(2), rules.observation(3)),
                        rules.literal_expr(False),
                    ),
                    rules.equal(rules.observation(3), rules.observation(4)),
                ),
                _derivation_result(
                    row.fixture,
                    existing=_total_existing_plans(
                        writable_targets,
                        tuple(writes),
                    ),
                    stop=True,
                ),
            ),
            _clause(
                symbol_case(alternate_symbols),
                _derivation_result(
                    f"{row.fixture}:single-B",
                    existing=_total_existing_plans(
                        writable_targets,
                        (
                            (
                                targets["run0"],
                                rules.literal_expr(alternate_run0),
                            ),
                            (
                                targets["cursor"],
                                rules.literal_expr("done"),
                            ),
                        ),
                    ),
                    stop=True,
                ),
            ),
            _clause(
                symbol_case(("A", "A", "A", "<end>", "<end>")),
                _derivation_result(
                    f"{row.fixture}:AAA",
                    existing=_total_existing_plans(
                        writable_targets,
                        (
                            (
                                targets["run0"],
                                rules.literal_expr(primary_run0),
                            ),
                            (
                                targets["cursor"],
                                rules.literal_expr("done"),
                            ),
                        ),
                    ),
                    stop=True,
                ),
            ),
        )
        additional_future_values = (
            primary_run0,
            primary_run1,
            alternate_run0,
            "<end>",
        )
        program_domain_values = (
            alternate_run0,
            "<end>",
        )
    elif row.spf == "SPF054":
        native = _codec_word("prefix-block", "A")
        encoded = _codec_word("prefix-bits", 0)
        alternate_native = _codec_word("prefix-block", "B")
        alternate_encoded = _codec_word("prefix-bits", 1, 0)
        selected_native, selected_encoded = _representation_case(
            native,
            encoded,
            alternate_native,
            alternate_encoded,
            case_index,
        )
        block = loci.path("root", "block", scope="prefix-tree")
        codebook = loci.path("root", "codebook", scope="prefix-tree")
        cursor = loci.path("root", "cursor", scope="prefix-tree")
        codebook_value = _codec_record(
            "prefix-tree",
            A="0",
            B="10",
            C="11",
        )
        def prefix_source(
            value: alphabets.SemanticValue,
        ) -> loci.FiniteConfiguration:
            return _structural_configuration(
                loci.CarrierKind.TREE,
                (
                    (block, value),
                    (codebook, codebook_value),
                    (cursor, "block-0"),
                ),
            )

        program_seed_source = prefix_source(native)
        source = prefix_source(selected_native)
        read_targets = (block, codebook, cursor)
        writes = (
            (cursor, rules.literal_expr("done")),
        )
        fresh_parent = block
        fresh_namespace = "g7-prefix-output"
        fresh_keys = (0, 1)
        fresh_values = (0, 0)
        prefix_references = tuple(
            loci.FreshReference(
                fresh_namespace,
                key,
                parent=block,
            )
            for key in fresh_keys
        )
        cursor_plan = _existing_target_plan(
            cursor,
            rules.DispositionAction.REPLACE,
            rules.literal_expr("done"),
        )

        def prefix_condition(
            value: alphabets.SemanticValue,
        ) -> rules.RuleExpr:
            return _all_conditions(
                rules.equal(
                    rules.observation(0),
                    rules.literal_expr(value),
                ),
                rules.equal(
                    rules.observation(1),
                    rules.literal_expr(codebook_value),
                ),
                rules.equal(
                    rules.observation(2),
                    rules.literal_expr("block-0"),
                ),
            )

        custom_clauses = (
            _clause(
                prefix_condition(native),
                _derivation_result(
                    f"{row.fixture}:A",
                    existing=(cursor_plan,),
                    fresh=(
                        _fresh_target_plan(
                            prefix_references[0],
                            rules.DispositionAction.CREATE,
                            rules.literal_expr(0),
                        ),
                        _fresh_target_plan(
                            prefix_references[1],
                            rules.DispositionAction.ABSENT,
                        ),
                    ),
                    stop=True,
                ),
            ),
            _clause(
                prefix_condition(alternate_native),
                _derivation_result(
                    f"{row.fixture}:B",
                    existing=(cursor_plan,),
                    fresh=(
                        _fresh_target_plan(
                            prefix_references[0],
                            rules.DispositionAction.CREATE,
                            rules.literal_expr(1),
                        ),
                        _fresh_target_plan(
                            prefix_references[1],
                            rules.DispositionAction.CREATE,
                            rules.literal_expr(0),
                        ),
                    ),
                    stop=True,
                ),
            ),
        )
        program_domain_values = (alternate_native,)
    elif row.spf == "SPF055":
        native = _codec_word("message", "A", "B")
        encoded = _codec_record(
            "nested-interval",
            low=Fraction(1, 4),
            high=Fraction(1, 2),
        )
        alternate_native = _codec_word("message", "A", "A")
        alternate_encoded = _codec_record(
            "nested-interval",
            low=Fraction(0),
            high=Fraction(1, 4),
        )
        selected_native, selected_encoded = _representation_case(
            native,
            encoded,
            alternate_native,
            alternate_encoded,
            case_index,
        )
        symbol0 = loci.field_point("codec", (0,), component="symbol-0")
        symbol1 = loci.field_point("codec", (0,), component="symbol-1")
        partition = loci.field_point("codec", (0,), component="partition")
        low = loci.field_point("codec", (0,), component="low")
        high = loci.field_point("codec", (0,), component="high")
        cursor = loci.field_point("codec", (0,), component="cursor")
        second_symbol = "B" if case_index == 0 else "A"
        partition_value = _codec_record(
            "cumulative-partition",
            A=_codec_record(
                "interval",
                low=Fraction(0),
                high=Fraction(1, 2),
            ),
            B=_codec_record(
                "interval",
                low=Fraction(1, 2),
                high=Fraction(1),
            ),
        )
        def interval_source(second: str) -> loci.FiniteConfiguration:
            return _structural_configuration(
                loci.CarrierKind.FIELD,
                (
                    (symbol0, "A"),
                    (symbol1, second),
                    (partition, partition_value),
                    (low, Fraction(0)),
                    (high, Fraction(1)),
                    (cursor, 0),
                ),
                rank=1,
                axes=("x",),
            )

        program_seed_source = interval_source("B")
        source = interval_source(second_symbol)
        read_targets = (symbol0, symbol1, partition, low, high, cursor)
        writes = (
            (low, rules.literal_expr(Fraction(0))),
            (high, rules.literal_expr(Fraction(1, 2))),
            (cursor, rules.literal_expr(1)),
        )
    elif row.spf == "SPF056":
        native = _codec_word("history-input", "A", "B", "A", "B")
        encoded = _codec_word(
            "history-records",
            "literal:A",
            "literal:B",
            "ref:offset=2,length=2",
        )
        alternate_native = _codec_word("history-input", "A", "B", "C")
        alternate_encoded = _codec_word(
            "history-records",
            "literal:A",
            "literal:B",
            "literal:C",
        )
        selected_native, selected_encoded = _representation_case(
            native,
            encoded,
            alternate_native,
            alternate_encoded,
            case_index,
        )
        primary_raw = ("A", "B", "A", "B")
        alternate_raw = ("A", "B", "C", "<end>")
        raw_symbols = primary_raw if case_index == 0 else alternate_raw
        input_targets = tuple(
            loci.occurrence("codec-input", index)
            for index in range(4)
        )
        current = loci.named("current-symbol", scope="history-workspace")
        queue = loci.named("symbol-queue", scope="history-workspace")
        history_targets = tuple(
            loci.occurrence("codec-history", index)
            for index in range(4)
        )
        record_targets = tuple(
            loci.occurrence("codec-record", index)
            for index in range(3)
        )
        reconstruction_targets = tuple(
            loci.occurrence("codec-reconstruction", index)
            for index in range(4)
        )
        cursor = loci.named("cursor", scope="history-workspace")
        empty_queue = _codec_word("symbol-queue")
        primary_queues = (
            _codec_word("symbol-queue", "B", "A", "B"),
            _codec_word("symbol-queue", "A", "B"),
            _codec_word("symbol-queue", "B"),
            empty_queue,
        )
        alternate_queues = (
            _codec_word("symbol-queue", "B", "C"),
            _codec_word("symbol-queue", "C"),
            empty_queue,
            empty_queue,
        )

        def history_source(
            values: tuple[str, ...],
            initial_queue: alphabets.ValueNode,
        ) -> loci.FiniteConfiguration:
            return _structural_configuration(
                loci.CarrierKind.HISTORY,
                (
                    *tuple(zip(input_targets, values, strict=True)),
                    (current, values[0]),
                    (queue, initial_queue),
                    *tuple((target, unset) for target in history_targets),
                    *tuple((target, unset) for target in record_targets),
                    *tuple((target, unset) for target in reconstruction_targets),
                    (cursor, 0),
                ),
                rank=1,
                axes=("history",),
            )

        program_seed_source = history_source(primary_raw, primary_queues[0])
        source = history_source(
            raw_symbols,
            primary_queues[0] if case_index == 0 else alternate_queues[0],
        )
        candidate_targets = input_targets[2:4]
        read_targets = (
            current,
            queue,
            *candidate_targets,
            *history_targets,
            cursor,
        )
        writable_targets = (
            current,
            queue,
            *history_targets,
            *record_targets,
            *reconstruction_targets,
            cursor,
        )
        writes = tuple(
            (target, rules.literal_expr(unset))
            for target in writable_targets
        )
        literal_a = _literal_history_record("A")
        literal_b = _literal_history_record("B")
        literal_c = _literal_history_record("C")
        reference_record = _reference_history_record(2, 2)
        history_observation = 2 + len(candidate_targets)
        cursor_observation = history_observation + len(history_targets)

        def scan_condition(
            symbol: str,
            queue_value: alphabets.ValueNode,
            step: int,
            *extra: rules.RuleExpr,
        ) -> rules.RuleExpr:
            return _all_conditions(
                rules.equal(
                    rules.observation(0),
                    rules.literal_expr(symbol),
                ),
                rules.equal(
                    rules.observation(1),
                    rules.literal_expr(queue_value),
                ),
                rules.equal(
                    rules.observation(cursor_observation),
                    rules.literal_expr(step),
                ),
                *extra,
            )

        shared_first = (
            (current, rules.literal_expr("B")),
            (history_targets[0], rules.observation(0)),
            (record_targets[0], rules.literal_expr(literal_a)),
            (reconstruction_targets[0], rules.observation(0)),
            (cursor, rules.literal_expr(1)),
        )
        shared_second = (
            (history_targets[1], rules.observation(0)),
            (record_targets[1], rules.literal_expr(literal_b)),
            (reconstruction_targets[1], rules.observation(0)),
            (cursor, rules.literal_expr(2)),
        )
        primary_third = (
            (queue, rules.literal_expr(empty_queue)),
            (
                history_targets[2],
                rules.observation(history_observation),
            ),
            (
                history_targets[3],
                rules.observation(history_observation + 1),
            ),
            (record_targets[2], rules.literal_expr(reference_record)),
            (
                reconstruction_targets[2],
                rules.observation(history_observation),
            ),
            (
                reconstruction_targets[3],
                rules.observation(history_observation + 1),
            ),
            (cursor, rules.literal_expr("done")),
        )
        alternate_third = (
            (queue, rules.literal_expr(empty_queue)),
            (history_targets[2], rules.observation(0)),
            (record_targets[2], rules.literal_expr(literal_c)),
            (reconstruction_targets[2], rules.observation(0)),
            (cursor, rules.literal_expr("done")),
        )
        clause_specs = (
            (
                scan_condition("A", primary_queues[0], 0),
                (*shared_first, (queue, rules.literal_expr(primary_queues[1]))),
                False,
                "primary-0",
            ),
            (
                scan_condition("A", alternate_queues[0], 0),
                (*shared_first, (queue, rules.literal_expr(alternate_queues[1]))),
                False,
                "alternate-0",
            ),
            (
                scan_condition("B", primary_queues[1], 1),
                (
                    *shared_second,
                    (current, rules.literal_expr("A")),
                    (queue, rules.literal_expr(primary_queues[2])),
                ),
                False,
                "primary-1",
            ),
            (
                scan_condition("B", alternate_queues[1], 1),
                (
                    *shared_second,
                    (current, rules.literal_expr("C")),
                    (queue, rules.literal_expr(alternate_queues[2])),
                ),
                False,
                "alternate-1",
            ),
            (
                scan_condition(
                    "A",
                    primary_queues[2],
                    2,
                    rules.equal(
                        rules.observation(2),
                        rules.observation(history_observation),
                    ),
                    rules.equal(
                        rules.observation(3),
                        rules.observation(history_observation + 1),
                    ),
                ),
                primary_third,
                True,
                "primary-2",
            ),
            (
                scan_condition(
                    "C",
                    alternate_queues[2],
                    2,
                    rules.equal(
                        rules.observation(2),
                        rules.literal_expr("C"),
                    ),
                    rules.equal(
                        rules.observation(3),
                        rules.literal_expr("<end>"),
                    ),
                ),
                alternate_third,
                True,
                "alternate-2",
            ),
        )
        custom_clauses = tuple(
            _clause(
                condition,
                _derivation_result(
                    f"{row.fixture}:{label}",
                    existing=_total_existing_plans(
                        writable_targets,
                        replacements,
                    ),
                    stop=stop,
                ),
            )
            for condition, replacements, stop, label in clause_specs
        )
        trajectory_steps = 3
        additional_future_values = (
            literal_a,
            literal_b,
            literal_c,
            reference_record,
            *primary_queues,
            *alternate_queues,
            "<end>",
        )
        program_domain_values = (
            "C",
            "<end>",
            *alternate_queues,
            literal_c,
        )
    elif row.spf == "SPF057":
        native = _codec_product("uniform-grid", 1, 1, 1, 1)
        encoded = _codec_record("region-leaf", bounds="2x2", value=1)
        alternate_native = _codec_product("nonuniform-grid", 1, 0, 0, 1)
        alternate_encoded = _codec_record(
            "region-branch",
            children=4,
            bounds="2x2",
        )
        selected_native, selected_encoded = _representation_case(
            native,
            encoded,
            alternate_native,
            alternate_encoded,
            case_index,
        )
        cell_values = (1, 1, 1, 1) if case_index == 0 else (1, 0, 0, 1)
        cells = (
            loci.cell((-1, -1), axes=("x", "y")),
            loci.cell((-1, 0), axes=("x", "y")),
            loci.cell((0, -1), axes=("x", "y")),
            loci.cell((0, 0), axes=("x", "y")),
        )
        result_target = loci.named("region-tree", scope="grid-workspace")
        cursor = loci.named("cursor", scope="grid-workspace")
        def region_source(
            values: tuple[int, ...],
        ) -> loci.FiniteConfiguration:
            return _structural_configuration(
                loci.CarrierKind.GRID,
                (
                    *tuple(zip(cells, values, strict=True)),
                    (result_target, unset),
                    (cursor, "root"),
                ),
                rank=2,
                axes=("x", "y"),
            )

        program_seed_source = region_source((1, 1, 1, 1))
        source = region_source(cell_values)
        read_targets = cells
        writes = (
            (result_target, rules.literal_expr(encoded)),
            (cursor, rules.literal_expr("done")),
        )
        fresh_parent = result_target
        fresh_namespace = "g7-region-children"
        fresh_keys = ("north-west", "north-east", "south-west", "south-east")
        fresh_values = tuple(
            _codec_record(
                "region-leaf",
                bounds=key,
                value=value,
            )
            for key, value in zip(
                fresh_keys,
                (1, 0, 0, 1),
                strict=True,
            )
        )
        region_references = tuple(
            loci.FreshReference(
                fresh_namespace,
                key,
                parent=result_target,
            )
            for key in fresh_keys
        )

        def region_condition(values: tuple[int, ...]) -> rules.RuleExpr:
            return _all_conditions(
                *(
                    rules.equal(
                        rules.observation(index),
                        rules.literal_expr(value),
                    )
                    for index, value in enumerate(values)
                )
            )

        uniform_existing = tuple(
            _existing_target_plan(
                target,
                rules.DispositionAction.REPLACE,
                value,
            )
            for target, value in writes
        )
        branch_existing = (
            _existing_target_plan(
                result_target,
                rules.DispositionAction.REPLACE,
                rules.literal_expr(alternate_encoded),
            ),
            _existing_target_plan(
                cursor,
                rules.DispositionAction.REPLACE,
                rules.literal_expr("done"),
            ),
        )
        custom_clauses = (
            _clause(
                region_condition((1, 1, 1, 1)),
                _derivation_result(
                    f"{row.fixture}:uniform",
                    existing=uniform_existing,
                    fresh=tuple(
                        _fresh_target_plan(
                            reference,
                            rules.DispositionAction.ABSENT,
                        )
                        for reference in region_references
                    ),
                    stop=True,
                ),
            ),
            _clause(
                region_condition((1, 0, 0, 1)),
                _derivation_result(
                    f"{row.fixture}:nonuniform",
                    existing=branch_existing,
                    fresh=tuple(
                        _fresh_target_plan(
                            reference,
                            rules.DispositionAction.CREATE,
                            rules.literal_expr(value),
                        )
                        for reference, value in zip(
                            region_references,
                            fresh_values,
                            strict=True,
                        )
                    ),
                    stop=True,
                ),
            ),
        )
        additional_future_values = fresh_values
        program_domain_values = (
            alternate_encoded,
            *fresh_values,
        )
    elif row.spf == "SPF058":
        native = _codec_word("vector", 1, 1)
        encoded = _codec_word("walsh-coefficients", 1, 0)
        alternate_native = _codec_word("vector", 1, -1)
        alternate_encoded = _codec_word("walsh-coefficients", 0, 1)
        selected_native, selected_encoded = _representation_case(
            native,
            encoded,
            alternate_native,
            alternate_encoded,
            case_index,
        )
        vector_values = (1, 1) if case_index == 0 else (1, -1)
        base = loci.named("basis-workspace", scope="product")
        vector0 = loci.product_locus("vector-0", (base,))
        vector1 = loci.product_locus("vector-1", (base,))
        basis00 = loci.product_locus("basis-0-0", (base,))
        basis01 = loci.product_locus("basis-0-1", (base,))
        basis10 = loci.product_locus("basis-1-0", (base,))
        basis11 = loci.product_locus("basis-1-1", (base,))
        selection = loci.product_locus("basis-selection", (base,))
        exact_mode = loci.product_locus("exact-mode", (base,))
        coefficient0 = loci.product_locus("coefficient-0", (base,))
        coefficient1 = loci.product_locus("coefficient-1", (base,))
        cursor = loci.product_locus("cursor", (base,))
        def basis_source(values: tuple[int, int]) -> loci.FiniteConfiguration:
            return _structural_configuration(
                loci.CarrierKind.PRODUCT,
                (
                    (vector0, values[0]),
                    (vector1, values[1]),
                    (basis00, 1),
                    (basis01, 1),
                    (basis10, 1),
                    (basis11, -1),
                    (selection, "walsh-2"),
                    (exact_mode, True),
                    (coefficient0, -1),
                    (coefficient1, -1),
                    (cursor, 0),
                ),
            )

        program_seed_source = basis_source((1, 1))
        source = basis_source(vector_values)
        read_targets = (
            vector0,
            vector1,
            basis00,
            basis01,
            basis10,
            basis11,
            selection,
            exact_mode,
            cursor,
        )
        dot0 = rules.add(
            rules.multiply(rules.observation(0), rules.observation(2)),
            rules.multiply(rules.observation(1), rules.observation(3)),
        )
        dot1 = rules.add(
            rules.multiply(rules.observation(0), rules.observation(4)),
            rules.multiply(rules.observation(1), rules.observation(5)),
        )

        def exact_walsh_coefficient(dot: rules.RuleExpr) -> rules.RuleExpr:
            return rules.conditional(
                rules.equal(dot, rules.literal_expr(2)),
                rules.literal_expr(1),
                rules.conditional(
                    rules.equal(dot, rules.literal_expr(-2)),
                    rules.literal_expr(-1),
                    rules.literal_expr(0),
                ),
            )

        writes = (
            (coefficient0, exact_walsh_coefficient(dot0)),
            (coefficient1, exact_walsh_coefficient(dot1)),
            (cursor, rules.literal_expr("done")),
        )
        rule_condition = _all_conditions(
            rules.equal(
                rules.observation(6),
                rules.literal_expr("walsh-2"),
            ),
            rules.equal(
                rules.observation(7),
                rules.literal_expr(True),
            ),
            rules.equal(
                rules.observation(8),
                rules.literal_expr(0),
            ),
        )
    elif row.spf == "SPF059":
        native = _codec_word("samples", 1, 2, 3)
        encoded = _codec_word("residuals", 1, 1, 1)
        alternate_native = _codec_word("samples", 2, 4, 6)
        alternate_encoded = _codec_word("residuals", 2, 2, 2)
        selected_native, selected_encoded = _representation_case(
            native,
            encoded,
            alternate_native,
            alternate_encoded,
            case_index,
        )
        primary_samples = (1, 2, 3)
        alternate_samples = (2, 4, 6)
        samples = primary_samples if case_index == 0 else alternate_samples
        input_targets = tuple(
            loci.occurrence("predictive-input", index)
            for index in range(3)
        )
        current = loci.named("current-sample", scope="predictive-workspace")
        previous = loci.named("previous-sample", scope="predictive-workspace")
        queue = loci.named("sample-queue", scope="predictive-workspace")
        model = loci.named("predictor-model", scope="predictive-workspace")
        residual_targets = tuple(
            loci.occurrence("residual", index)
            for index in range(3)
        )
        reconstruction_targets = tuple(
            loci.occurrence("predictive-reconstruction", index)
            for index in range(3)
        )
        cursor = loci.named("cursor", scope="predictive-workspace")
        empty_queue = _codec_word("sample-queue")
        primary_queues = (
            _codec_word("sample-queue", 2, 3),
            _codec_word("sample-queue", 3),
            empty_queue,
        )
        alternate_queues = (
            _codec_word("sample-queue", 4, 6),
            _codec_word("sample-queue", 6),
            empty_queue,
        )

        def predictive_source(
            values: tuple[int, int, int],
            initial_queue: alphabets.ValueNode,
        ) -> loci.FiniteConfiguration:
            return _structural_configuration(
                loci.CarrierKind.HISTORY,
                (
                    *tuple(zip(input_targets, values, strict=True)),
                    (current, values[0]),
                    (previous, 0),
                    (queue, initial_queue),
                    (model, "previous-sample"),
                    *tuple((target, 0) for target in residual_targets),
                    *tuple((target, 0) for target in reconstruction_targets),
                    (cursor, 0),
                ),
                rank=1,
                axes=("history",),
            )

        program_seed_source = predictive_source(
            primary_samples,
            primary_queues[0],
        )
        source = predictive_source(
            samples,
            primary_queues[0] if case_index == 0 else alternate_queues[0],
        )
        read_targets = (current, previous, queue, model, cursor)
        writable_targets = (
            current,
            previous,
            queue,
            *residual_targets,
            *reconstruction_targets,
            cursor,
        )
        writes = tuple(
            (target, rules.literal_expr(0))
            for target in writable_targets
        )
        residual = rules.subtract(
            rules.observation(0),
            rules.observation(1),
        )
        reconstructed = rules.add(rules.observation(1), residual)
        clause_specs: list[
            tuple[rules.RuleExpr, tuple[tuple[loci.Locus, rules.RuleExpr], ...], bool, str]
        ] = []
        for domain, domain_samples, queues in (
            ("primary", primary_samples, primary_queues),
            ("alternate", alternate_samples, alternate_queues),
        ):
            replacements_by_step = (
                (
                    (current, rules.literal_expr(domain_samples[1])),
                    (previous, rules.observation(0)),
                    (queue, rules.literal_expr(queues[1])),
                    (residual_targets[0], residual),
                    (reconstruction_targets[0], reconstructed),
                    (cursor, rules.literal_expr(1)),
                ),
                (
                    (current, rules.literal_expr(domain_samples[2])),
                    (previous, rules.observation(0)),
                    (queue, rules.literal_expr(queues[2])),
                    (residual_targets[1], residual),
                    (reconstruction_targets[1], reconstructed),
                    (cursor, rules.literal_expr(2)),
                ),
                (
                    (previous, rules.observation(0)),
                    (residual_targets[2], residual),
                    (reconstruction_targets[2], reconstructed),
                    (cursor, rules.literal_expr("done")),
                ),
            )
            for step, replacements in enumerate(replacements_by_step):
                condition = _all_conditions(
                    rules.equal(
                        rules.observation(0),
                        rules.literal_expr(domain_samples[step]),
                    ),
                    rules.equal(
                        rules.observation(1),
                        rules.literal_expr(
                            0 if step == 0 else domain_samples[step - 1]
                        ),
                    ),
                    rules.equal(
                        rules.observation(2),
                        rules.literal_expr(queues[step]),
                    ),
                    rules.equal(
                        rules.observation(3),
                        rules.literal_expr("previous-sample"),
                    ),
                    rules.equal(
                        rules.observation(4),
                        rules.literal_expr(step),
                    ),
                )
                clause_specs.append(
                    (
                        condition,
                        replacements,
                        step == 2,
                        f"{domain}-{step}",
                    )
                )
        custom_clauses = tuple(
            _clause(
                condition,
                _derivation_result(
                    f"{row.fixture}:{label}",
                    existing=_total_existing_plans(
                        writable_targets,
                        replacements,
                    ),
                    stop=stop,
                ),
            )
            for condition, replacements, stop, label in clause_specs
        )
        trajectory_steps = 3
        additional_future_values = (*primary_queues, *alternate_queues)
        program_domain_values = (
            4,
            6,
            *alternate_queues,
        )
    elif row.spf == "SPF060":
        native = _codec_product(
            "xor-operands",
            _codec_word("data", 1, 0, 1),
            _codec_word("generator", 0, 1, 1),
        )
        encoded = _codec_word("xor-output", 1, 1, 0)
        alternate_native = _codec_product(
            "xor-operands",
            _codec_word("data", 1, 1, 0),
            _codec_word("generator", 0, 1, 1),
        )
        alternate_encoded = _codec_word("xor-output", 1, 0, 1)
        selected_native, selected_encoded = _representation_case(
            native,
            encoded,
            alternate_native,
            alternate_encoded,
            case_index,
        )
        data_bits, generator_bits = (
            ((1, 0, 1), (0, 1, 1))
            if case_index == 0
            else ((1, 1, 0), (0, 1, 1))
        )
        word_targets = tuple(loci.occurrence("word", index) for index in range(9))
        alignment = loci.named("alignment", scope="xor-workspace")
        stream_cursor = loci.named("stream-cursor", scope="xor-workspace")
        generator_cursor = loci.named("generator-cursor", scope="xor-workspace")
        def xor_source(
            data: tuple[int, int, int],
            generator: tuple[int, int, int],
        ) -> loci.FiniteConfiguration:
            return _structural_configuration(
                loci.CarrierKind.WORD,
                (
                    *tuple(
                        zip(
                            word_targets,
                            (
                                *data,
                                *generator,
                                0,
                                0,
                                0,
                            ),
                            strict=True,
                        )
                    ),
                    (alignment, "aligned"),
                    (stream_cursor, 0),
                    (generator_cursor, 0),
                ),
                rank=1,
                axes=("word",),
            )

        program_seed_source = xor_source((1, 0, 1), (0, 1, 1))
        source = xor_source(data_bits, generator_bits)
        read_targets = (
            *word_targets[:6],
            alignment,
            stream_cursor,
            generator_cursor,
        )
        writes = (
            (
                word_targets[6],
                rules.modulo(
                    rules.add(rules.observation(0), rules.observation(3)),
                    2,
                ),
            ),
            (
                word_targets[7],
                rules.modulo(
                    rules.add(rules.observation(1), rules.observation(4)),
                    2,
                ),
            ),
            (
                word_targets[8],
                rules.modulo(
                    rules.add(rules.observation(2), rules.observation(5)),
                    2,
                ),
            ),
            (alignment, rules.literal_expr("done")),
            (stream_cursor, rules.literal_expr(3)),
            (generator_cursor, rules.literal_expr(3)),
        )
        rule_condition = _all_conditions(
            rules.equal(
                rules.observation(6),
                rules.literal_expr("aligned"),
            ),
            rules.equal(
                rules.observation(7),
                rules.literal_expr(0),
            ),
            rules.equal(
                rules.observation(8),
                rules.literal_expr(0),
            ),
        )
    else:
        raise AssertionError(f"missing PX10 recipe for {row.spf}")

    representation = _exact_representation(
        native,
        encoded,
        alternate_native,
        alternate_encoded,
    )
    future_values = (
        native,
        encoded,
        alternate_native,
        alternate_encoded,
        "A",
        "B",
        "C",
        "done",
        Fraction(1, 4),
        Fraction(1, 2),
        -1,
        0,
        1,
        2,
        3,
        *additional_future_values,
    )
    assert program_seed_source is not None
    assert program_seed_source.contract == source.contract
    alphabet = _closed_enum(
        tuple(value for _, value in program_seed_source.entries)
        + program_domain_values
        + future_values
    )
    write_targets = tuple(target for target, _ in writes)
    existing_writable, readable = _literal_regions(
        source,
        alphabet,
        write_targets=write_targets,
        read_targets=read_targets,
    )
    fresh_plans: tuple[rules.FreshDispositionPlan, ...] = ()
    if fresh_parent is None:
        writable = existing_writable
    else:
        fresh_writable, fresh_references = _fresh_children_writable(
            source,
            alphabet,
            parent=fresh_parent,
            namespace=fresh_namespace,
            keys=fresh_keys,
        )
        writable = frontiers.union((existing_writable, fresh_writable))
        fresh_plans = tuple(
            _fresh_target_plan(
                reference,
                rules.DispositionAction.CREATE,
                rules.literal_expr(value),
            )
            for reference, value in zip(
                fresh_references,
                fresh_values,
                strict=True,
            )
        )

    existing_plans = tuple(
        _existing_target_plan(
            target,
            rules.DispositionAction.REPLACE,
            value,
        )
        for target, value in writes
    )
    if custom_clauses is not None:
        clauses = custom_clauses
    elif row.spf == "SPF055":
        low, high, cursor = write_targets
        clauses = (
            _clause(
                _all_conditions(
                    rules.equal(
                        rules.observation(0),
                        rules.literal_expr("A"),
                    ),
                    rules.equal(
                        rules.observation(2),
                        rules.literal_expr(partition_value),
                    ),
                    rules.equal(
                        rules.observation(3),
                        rules.literal_expr(Fraction(0)),
                    ),
                    rules.equal(
                        rules.observation(4),
                        rules.literal_expr(Fraction(1)),
                    ),
                    rules.equal(
                        rules.observation(5),
                        rules.literal_expr(0),
                    ),
                ),
                _derivation_result(
                    f"{row.fixture}:first-symbol",
                    existing=existing_plans,
                ),
            ),
            _clause(
                _all_conditions(
                    rules.gate(
                        rules.RuleExpr(
                            rules.ExpressionPrimitive.TUPLE,
                            (
                                rules.equal(
                                    rules.observation(1),
                                    rules.literal_expr("A"),
                                ),
                                rules.equal(
                                    rules.observation(1),
                                    rules.literal_expr("B"),
                                ),
                            ),
                        ),
                        rules.GateKind.ANY,
                    ),
                    rules.equal(
                        rules.observation(2),
                        rules.literal_expr(partition_value),
                    ),
                    rules.equal(
                        rules.observation(3),
                        rules.literal_expr(Fraction(0)),
                    ),
                    rules.equal(
                        rules.observation(4),
                        rules.literal_expr(Fraction(1, 2)),
                    ),
                    rules.equal(
                        rules.observation(5),
                        rules.literal_expr(1),
                    ),
                ),
                _derivation_result(
                    f"{row.fixture}:second-symbol",
                    existing=(
                        _existing_target_plan(
                            low,
                            rules.DispositionAction.REPLACE,
                            rules.conditional(
                                rules.equal(
                                    rules.observation(1),
                                    rules.literal_expr("B"),
                                ),
                                rules.literal_expr(Fraction(1, 4)),
                                rules.literal_expr(Fraction(0)),
                            ),
                        ),
                        _existing_target_plan(
                            high,
                            rules.DispositionAction.REPLACE,
                            rules.conditional(
                                rules.equal(
                                    rules.observation(1),
                                    rules.literal_expr("B"),
                                ),
                                rules.literal_expr(Fraction(1, 2)),
                                rules.literal_expr(Fraction(1, 4)),
                            ),
                        ),
                        _existing_target_plan(
                            cursor,
                            rules.DispositionAction.REPLACE,
                            rules.literal_expr("done"),
                        ),
                    ),
                    stop=True,
                ),
            ),
        )
    else:
        clauses = (
            _clause(
                rule_condition,
                _derivation_result(
                    row.fixture,
                    existing=existing_plans,
                    fresh=fresh_plans,
                    stop=True,
                ),
            ),
        )

    rule = _kernel(
        source,
        alphabet,
        writable,
        readable,
        clauses,
    )
    execution = _assemble(
        row,
        source,
        alphabet,
        writable,
        readable,
        rule,
        representation=representation,
        representation_source=selected_native,
        representation_target=selected_encoded,
        representation_case_index=case_index,
        seed_source=program_seed_source,
    )
    if row.spf == "SPF055":
        trajectory_steps = 2
    if trajectory_steps == 1:
        return execution

    if not isinstance(execution.result, program.ApplicationComplete):
        fault = execution.result.fault
        raise AssertionError(
            f"{row.spf}/{row.fixture}/case-{case_index}/step-0 rejected: "
            f"{fault.reason}; {fault.evidence!r}"
        )
    trajectory: list[tuple[Configuration, program.ApplicationComplete]] = [
        (execution.source, execution.result)
    ]
    current_result = execution.result
    for step in range(1, trajectory_steps):
        prior_successors = _finite_successors(current_result)
        assert len(prior_successors) == 1
        current_source = prior_successors[0]
        application_result = ca.apply(execution.simple_program, current_source)
        if not isinstance(application_result, program.ApplicationComplete):
            fault = application_result.fault
            raise AssertionError(
                f"{row.spf}/{row.fixture}/case-{case_index}/step-{step} "
                f"rejected: {fault.reason}; {fault.evidence!r}"
            )
        current_result = application_result
        trajectory.append((current_source, current_result))
    return MechanicsRun(
        row=execution.row,
        simple_program=execution.simple_program,
        source=execution.source,
        result=execution.result,
        representation=execution.representation,
        representation_source=execution.representation_source,
        representation_target=execution.representation_target,
        representation_case_index=execution.representation_case_index,
        trajectory=tuple(trajectory),
    )


def _spf012_maximal_run_secondary(row: MechanicsRow) -> MechanicsRun:
    """Execute the audited AAA -> self-delimiting (A, 3) stopped case."""

    primary = _px10(row, case_index=0)
    unset = _codec_record("unset", status="unset")
    source = _record_configuration(
        (
            ("symbol0", "A"),
            ("symbol1", "A"),
            ("symbol2", "A"),
            ("symbol3", "<end>"),
            ("symbol4", "<end>"),
            ("run0", unset),
            ("run1", unset),
            ("cursor", 0),
        )
    )
    result = ca.apply(primary.simple_program, source)
    return MechanicsRun(
        row=row,
        simple_program=primary.simple_program,
        source=source,
        result=result,
    )


def _px11(row: MechanicsRow) -> MechanicsRun:
    """Advance one priority requirement and atomically injure the lower one."""

    source = _record_configuration(
        (
            ("oracle_default", 0),
            ("p0_state", 0),
            ("p1_state", 1),
            ("p1_use_o0", 0),
            ("p1_work", 7),
            ("scheduler_next", 0),
        )
    )
    alphabet = alphabets.integers()
    targets = _record_targets(source)
    existing_targets = tuple(
        targets[name]
        for name in (
            "p0_state",
            "p1_state",
            "p1_use_o0",
            "p1_work",
            "scheduler_next",
        )
    )
    existing = frontiers.literal(
        existing_targets,
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    oracle_region, (oracle_o0,) = _fresh_children_writable(
        source,
        alphabet,
        parent=targets["oracle_default"],
        namespace="g7-priority-oracle",
        keys=("O[0]",),
    )
    writable = frontiers.union((existing, oracle_region))
    readable = neighborhoods.literal(
        tuple(target for target, _ in source.entries),
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
        key="priority-runs-uses-and-scheduler",
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
                            targets["p0_state"],
                            rules.DispositionAction.REPLACE,
                            rules.literal_expr(1),
                        ),
                        _existing_target_plan(
                            targets["p1_state"],
                            rules.DispositionAction.REPLACE,
                            rules.literal_expr(2),
                        ),
                        _existing_target_plan(
                            targets["p1_use_o0"],
                            rules.DispositionAction.REPLACE,
                            rules.literal_expr(-1),
                        ),
                        _existing_target_plan(
                            targets["p1_work"],
                            rules.DispositionAction.REPLACE,
                            rules.literal_expr(0),
                        ),
                        _existing_target_plan(
                            targets["scheduler_next"],
                            rules.DispositionAction.REPLACE,
                            rules.literal_expr(1),
                        ),
                    ),
                    fresh=(
                        _fresh_target_plan(
                            oracle_o0,
                            rules.DispositionAction.CREATE,
                            rules.literal_expr(1),
                        ),
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
        causal_e0 = loci.graph_element("node", "causal/e0")
        trace_e1 = loci.graph_element("node", "trace/e1")
        producer_y = loci.graph_element("node", "producer/y")
        cursor = loci.graph_element("node", "cursor")
        source = _structural_configuration(
            loci.CarrierKind.GRAPH,
            (
                (causal_e0, _graph_node("causal/e0")),
                (
                    trace_e1,
                    alphabets.ValueNode(
                        alphabets.ValueKind.GRAPH,
                        "trace-event",
                        fields=(("reads", "x"), ("writes", "y")),
                    ),
                ),
                (producer_y, _graph_node("unset-producer/y")),
                (cursor, _graph_node("trace/e1")),
            ),
        )
        alphabet = alphabets.graph()
        existing = frontiers.literal(
            (producer_y, cursor),
            configuration_contract=source.contract,
            value_profile=alphabet.value_profile,
        )
        node_region, (causal_e1,) = _fresh_children_writable(
            source,
            alphabet,
            parent=trace_e1,
            namespace="g7-causal-node",
            keys=("causal/e1",),
        )
        edge_reference = loci.FreshReference(
            "g7-causal-edge",
            "causal/e0->causal/e1",
            interface=(causal_e0, trace_e1),
        )
        edge_region = frontiers.fresh(
            loci.fresh_edges(
                (causal_e0, trace_e1),
                "g7-causal-edge",
                ("causal/e0->causal/e1",),
            ),
            namespace=frontiers.FreshNamespace("g7-causal-edge"),
            configuration_contract=source.contract,
            value_profile=alphabet.value_profile,
        )
        writable = frontiers.union((existing, node_region, edge_region))
        readable = neighborhoods.literal(
            (trace_e1, causal_e0, producer_y, cursor),
            configuration_contract=source.contract,
            value_profile=alphabet.value_profile,
            key="trace-event-and-current-producers",
        )
        producer_value = alphabets.ValueNode(
            alphabets.ValueKind.GRAPH,
            "producer",
            fields=(
                ("event", alphabets.StructuralReference(causal_e1)),
                ("variable", "y"),
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
                        existing=(
                            _existing_target_plan(
                                producer_y,
                                rules.DispositionAction.REPLACE,
                                rules.literal_expr(producer_value),
                            ),
                            _existing_target_plan(
                                cursor,
                                rules.DispositionAction.REPLACE,
                                rules.literal_expr(_graph_node("done")),
                            ),
                        ),
                        fresh=(
                            _fresh_target_plan(
                                causal_e1,
                                rules.DispositionAction.CREATE,
                                rules.literal_expr(_graph_node("causal/e1")),
                            ),
                            _fresh_target_plan(
                                edge_reference,
                                rules.DispositionAction.CREATE,
                                rules.literal_expr(
                                    _graph_edge(
                                        causal_e0,
                                        causal_e1,
                                        name="causal/e0->causal/e1",
                                    )
                                ),
                            ),
                        ),
                        stop=True,
                    ),
                ),
            ),
        )
        return _assemble(row, source, alphabet, writable, readable, rule)

    assert row.spf == "SPF042"
    source = _record_configuration(
        (
            ("observed0", 1),
            ("observed1", 1),
            ("surrogate0", 1),
            ("surrogate1", 0),
            ("program_descriptor", 1),
            ("phase", 0),
            ("frame_depth", 0),
            ("observed_result", -1),
            ("surrogate_result", -1),
            ("decision", -1),
        )
    )
    alphabet = alphabets.integers()
    targets = _record_targets(source)
    read_targets = tuple(
        targets[name]
        for name in (
            "observed0",
            "observed1",
            "surrogate0",
            "surrogate1",
            "program_descriptor",
            "phase",
            "frame_depth",
            "observed_result",
            "surrogate_result",
            "decision",
        )
    )
    write_targets = tuple(
        targets[name]
        for name in (
            "phase",
            "frame_depth",
            "observed_result",
            "surrogate_result",
            "decision",
        )
    )
    writable, readable = _literal_regions(
        source,
        alphabet,
        write_targets=write_targets,
        read_targets=read_targets,
    )
    clauses = (
        _clause(
            rules.equal(rules.observation(5), rules.literal_expr(0)),
            _derivation_result(
                f"{row.fixture}:evaluate-observed",
                existing=(
                    _existing_target_plan(
                        targets["observed_result"],
                        rules.DispositionAction.REPLACE,
                        rules.add(rules.observation(0), rules.observation(1)),
                    ),
                    _existing_target_plan(
                        targets["phase"],
                        rules.DispositionAction.REPLACE,
                        rules.literal_expr(1),
                    ),
                    _existing_target_plan(
                        targets["frame_depth"],
                        rules.DispositionAction.REPLACE,
                        rules.literal_expr(1),
                    ),
                ),
            ),
        ),
        _clause(
            rules.equal(rules.observation(5), rules.literal_expr(1)),
            _derivation_result(
                f"{row.fixture}:evaluate-surrogate",
                existing=(
                    _existing_target_plan(
                        targets["surrogate_result"],
                        rules.DispositionAction.REPLACE,
                        rules.add(rules.observation(2), rules.observation(3)),
                    ),
                    _existing_target_plan(
                        targets["phase"],
                        rules.DispositionAction.REPLACE,
                        rules.literal_expr(2),
                    ),
                    _existing_target_plan(
                        targets["frame_depth"],
                        rules.DispositionAction.REPLACE,
                        rules.literal_expr(1),
                    ),
                ),
            ),
        ),
        _clause(
            rules.equal(rules.observation(5), rules.literal_expr(2)),
            _derivation_result(
                f"{row.fixture}:calibrate",
                existing=(
                    _existing_target_plan(
                        targets["decision"],
                        rules.DispositionAction.REPLACE,
                        rules.conditional(
                            rules.less_than(
                                rules.observation(8),
                                rules.observation(7),
                            ),
                            rules.literal_expr(1),
                            rules.literal_expr(0),
                        ),
                    ),
                    _existing_target_plan(
                        targets["phase"],
                        rules.DispositionAction.REPLACE,
                        rules.literal_expr(3),
                    ),
                    _existing_target_plan(
                        targets["frame_depth"],
                        rules.DispositionAction.REPLACE,
                        rules.literal_expr(0),
                    ),
                ),
                stop=True,
            ),
        ),
    )
    rule = _kernel(
        source,
        alphabet,
        writable,
        readable,
        clauses,
        selection=rules.ClauseSelection.FIRST,
    )
    first = _assemble(row, source, alphabet, writable, readable, rule)
    assert isinstance(first.result, program.ApplicationComplete)

    def successor_of(
        result: program.ApplicationComplete,
    ) -> loci.FiniteConfiguration:
        groups = result.successor_quotient_with_derivation_fibers.atoms
        assert len(groups) == 1
        successor = groups[0].successor
        assert isinstance(successor, loci.FiniteConfiguration)
        return successor

    second_source = successor_of(first.result)
    second_result = ca.apply(first.simple_program, second_source)
    assert isinstance(second_result, program.ApplicationComplete)
    third_source = successor_of(second_result)
    third_result = ca.apply(first.simple_program, third_source)
    assert isinstance(third_result, program.ApplicationComplete)
    return MechanicsRun(
        row=row,
        simple_program=first.simple_program,
        source=source,
        result=first.result,
        trajectory=(
            (source, first.result),
            (second_source, second_result),
            (third_source, third_result),
        ),
    )


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


def run_px10_representation_case(
    row: MechanicsRow,
    case_index: int,
) -> MechanicsRun:
    """Execute either pair in a PX10 relation through its family mechanics."""

    if row.primary != "PX10":
        raise ValueError(f"{row.spf} is not a PX10 representation row")
    if type(case_index) is not int or case_index not in (0, 1):
        raise ValueError("PX10 representation case index must be 0 or 1")
    primary = _px10(row, case_index=0)
    alternate_recipe = _px10(row, case_index=1)
    assert (
        primary.simple_program.canonical_identity
        == alternate_recipe.simple_program.canonical_identity
    )
    assert primary.representation == alternate_recipe.representation
    if case_index == 0:
        return primary

    source = alternate_recipe.source
    first_result = ca.apply(primary.simple_program, source)
    if not isinstance(first_result, program.ApplicationComplete):
        fault = first_result.fault
        raise AssertionError(
            f"{row.spf}/{row.fixture}/case-1/step-0 rejected: "
            f"{fault.reason}; {fault.evidence!r}"
        )
    step_count = len(alternate_recipe.trajectory) or 1
    trajectory: list[tuple[Configuration, program.ApplicationComplete]] = []
    if step_count > 1:
        trajectory.append((source, first_result))
        current_result = first_result
        for step in range(1, step_count):
            successors = _finite_successors(current_result)
            assert len(successors) == 1
            step_source = successors[0]
            step_result = ca.apply(primary.simple_program, step_source)
            if not isinstance(step_result, program.ApplicationComplete):
                fault = step_result.fault
                raise AssertionError(
                    f"{row.spf}/{row.fixture}/case-1/step-{step} rejected: "
                    f"{fault.reason}; {fault.evidence!r}"
                )
            trajectory.append((step_source, step_result))
            current_result = step_result
    execution = MechanicsRun(
        row=row,
        simple_program=primary.simple_program,
        source=source,
        result=first_result,
        representation=primary.representation,
        representation_source=alternate_recipe.representation_source,
        representation_target=alternate_recipe.representation_target,
        representation_case_index=1,
        trajectory=tuple(trajectory),
    )
    if not isinstance(execution.result, program.ApplicationComplete):
        fault = execution.result.fault
        raise AssertionError(
            f"{row.spf}/{row.fixture}/case-{case_index} rejected: "
            f"{fault.reason}; {fault.evidence!r}"
        )
    return execution


def run_secondary_fixture(row: MechanicsRow, pressure: str) -> MechanicsRun:
    """Re-assert a secondary invariant on the same family construction."""

    if pressure not in row.secondary:
        raise ValueError(f"{row.spf} has no declared {pressure} secondary join")
    execution = (
        _spf012_maximal_run_secondary(row)
        if row.spf == "SPF012" and pressure == "PX08"
        else run_mechanics_fixture(row)
    )
    if row.spf == "SPF042" and pressure == "PX08":
        source, result = execution.trajectory[-1]
        return MechanicsRun(
            row=row,
            simple_program=execution.simple_program,
            source=source,
            result=result,
            trajectory=execution.trajectory,
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


def _materialized_px10_target(
    execution: MechanicsRun,
    result: program.ApplicationComplete,
    successor: loci.FiniteConfiguration,
) -> alphabets.SemanticValue:
    """Extract the represented value produced by the family workspace."""

    spf = execution.row.spf
    if spf == "SPF012":
        unset = _codec_record("unset", status="unset")
        fields: list[tuple[str, alphabets.SemanticValue]] = []
        reached_unset = False
        for index in range(2):
            record = successor.value_at(
                loci.named(f"run{index}", scope="record")
            )
            if alphabets.semantic_equal(record, unset):
                reached_unset = True
                continue
            assert not reached_unset
            assert type(record) is alphabets.ValueNode
            assert record.kind is alphabets.ValueKind.RECORD
            assert record.tag == "run-record"
            record_fields = dict(record.fields)
            symbol = record_fields["symbol"]
            length = record_fields["length"]
            assert type(symbol) is str
            assert type(length) is int
            fields.append((f"run{index}", f"{symbol}:{length}"))
        assert fields
        return alphabets.ValueNode(
            alphabets.ValueKind.RECORD,
            "run-records",
            fields=tuple(fields),
        )
    if spf == "SPF054":
        derivations = tuple(
            atom
            for atom in result.applied_atoms.atoms
            if isinstance(atom, program.AppliedDerivation)
        )
        assert len(derivations) == 1
        bindings = {
            binding.reference: binding.identity
            for binding in derivations[0].fresh_bindings
        }
        created = {
            disposition.target.local_key: bindings[disposition.target]
            for disposition in derivations[0].source.replacement.fresh
            if disposition.action is rules.DispositionAction.CREATE
        }
        bits = tuple(
            successor.value_at(created[index])
            for index in range(len(created))
        )
        return _codec_word("prefix-bits", *bits)
    if spf == "SPF055":
        low = successor.value_at(
            loci.field_point("codec", (0,), component="low")
        )
        high = successor.value_at(
            loci.field_point("codec", (0,), component="high")
        )
        return _codec_record("nested-interval", low=low, high=high)
    if spf == "SPF056":
        items: list[alphabets.SemanticValue] = []
        for index in range(3):
            record = successor.value_at(loci.occurrence("codec-record", index))
            assert type(record) is alphabets.ValueNode
            assert record.kind is alphabets.ValueKind.RECORD
            record_fields = dict(record.fields)
            if record.tag == "literal-record":
                symbol = record_fields["symbol"]
                assert type(symbol) is str
                items.append(f"literal:{symbol}")
            else:
                assert record.tag == "reference-record"
                offset = record_fields["offset"]
                length = record_fields["length"]
                assert type(offset) is int
                assert type(length) is int
                items.append(f"ref:offset={offset},length={length}")
        return _codec_word("history-records", *items)
    if spf == "SPF057":
        region = successor.value_at(
            loci.named("region-tree", scope="grid-workspace")
        )
        assert type(region) is alphabets.ValueNode
        assert region.kind is alphabets.ValueKind.RECORD
        if region.tag == "region-leaf":
            return region
        assert region.tag == "region-branch"
        derivations = tuple(
            atom
            for atom in result.applied_atoms.atoms
            if isinstance(atom, program.AppliedDerivation)
        )
        assert len(derivations) == 1
        binding_by_reference = {
            binding.reference: binding.identity
            for binding in derivations[0].fresh_bindings
        }
        child_payloads = {
            disposition.target.local_key: successor.value_at(
                binding_by_reference[disposition.target]
            )
            for disposition in derivations[0].source.replacement.fresh
            if disposition.action is rules.DispositionAction.CREATE
        }
        expected_values = {
            "north-west": 1,
            "north-east": 0,
            "south-west": 0,
            "south-east": 1,
        }
        assert set(child_payloads) == set(expected_values)
        for key, expected_value in expected_values.items():
            payload = child_payloads[key]
            assert type(payload) is alphabets.ValueNode
            assert payload.kind is alphabets.ValueKind.RECORD
            assert payload.tag == "region-leaf"
            assert dict(payload.fields) == {
                "bounds": key,
                "value": expected_value,
            }
        assert dict(region.fields) == {
            "children": len(child_payloads),
            "bounds": "2x2",
        }
        return region
    if spf == "SPF058":
        base = loci.named("basis-workspace", scope="product")
        coefficients = tuple(
            successor.value_at(
                loci.product_locus(f"coefficient-{index}", (base,))
            )
            for index in range(2)
        )
        return _codec_word("walsh-coefficients", *coefficients)
    if spf == "SPF059":
        residuals = tuple(
            successor.value_at(loci.occurrence("residual", index))
            for index in range(3)
        )
        return _codec_word("residuals", *residuals)
    if spf == "SPF060":
        bits = tuple(
            successor.value_at(loci.occurrence("word", index))
            for index in range(6, 9)
        )
        return alphabets.ValueNode(
            alphabets.ValueKind.WORD,
            "xor-output",
            items=bits,
        )

    raise AssertionError(f"missing PX10 output extractor for {spf}")


def _materialized_px10_source(
    execution: MechanicsRun,
) -> alphabets.SemanticValue:
    """Reconstruct the native relation value from the workspace's real reads."""

    resolved = execution.simple_program.neighborhood.resolve(execution.source)
    assert type(resolved) is neighborhoods.ReadableView
    values = tuple(observation.value for observation in resolved.observations)
    spf = execution.row.spf
    if spf == "SPF012":
        symbols = tuple(
            execution.source.value_at(
                loci.named(f"symbol{index}", scope="record")
            )
            for index in range(5)
        )
        while symbols and symbols[-1] == "<end>":
            symbols = symbols[:-1]
        assert symbols
        assert "<end>" not in symbols
        return _codec_word(
            "source-word",
            *symbols,
        )
    if spf == "SPF054":
        return values[0]
    if spf == "SPF055":
        return _codec_word(
            "message",
            execution.source.value_at(
                loci.field_point("codec", (0,), component="symbol-0")
            ),
            execution.source.value_at(
                loci.field_point("codec", (0,), component="symbol-1")
            ),
        )
    if spf == "SPF056":
        symbols = tuple(
            execution.source.value_at(loci.occurrence("codec-input", index))
            for index in range(4)
        )
        while symbols and symbols[-1] == "<end>":
            symbols = symbols[:-1]
        assert symbols
        assert "<end>" not in symbols
        return _codec_word(
            "history-input",
            *symbols,
        )
    if spf == "SPF057":
        tag = "uniform-grid" if len(set(values)) == 1 else "nonuniform-grid"
        return _codec_product(tag, *values)
    if spf == "SPF058":
        return _codec_word("vector", *values[:2])
    if spf == "SPF059":
        return _codec_word(
            "samples",
            *(
                execution.source.value_at(
                    loci.occurrence("predictive-input", index)
                )
                for index in range(3)
            ),
        )
    if spf == "SPF060":
        return _codec_product(
            "xor-operands",
            _codec_word("data", *values[:3]),
            _codec_word("generator", *values[3:6]),
        )
    raise AssertionError(f"missing PX10 input extractor for {spf}")


def materialized_px10_target(
    execution: MechanicsRun,
) -> alphabets.SemanticValue:
    """Return the terminal represented value derived from workspace loci."""

    if execution.row.primary != "PX10":
        raise ValueError(f"{execution.row.spf} is not a PX10 representation row")
    if execution.trajectory:
        _, result = execution.trajectory[-1]
    else:
        result = execution.result
    assert isinstance(result, program.ApplicationComplete)
    successors = _finite_successors(result)
    assert len(successors) == 1
    return _materialized_px10_target(execution, result, successors[0])


def materialized_px10_source(
    execution: MechanicsRun,
) -> alphabets.SemanticValue:
    """Return the native value reconstructed only from initial workspace loci."""

    if execution.row.primary != "PX10":
        raise ValueError(f"{execution.row.spf} is not a PX10 representation row")
    return _materialized_px10_source(execution)


def _materialized_read_targets(execution: MechanicsRun) -> tuple[loci.Locus, ...]:
    resolved = execution.simple_program.neighborhood.resolve(execution.source)
    if type(resolved) is neighborhoods.IntensionalReadableView:
        return ()
    return tuple(observation.target for observation in resolved.observations)


def _resolved_write_targets(
    execution: MechanicsRun,
) -> tuple[loci.Locus | loci.FreshReference, ...]:
    return execution.simple_program.frontier.resolve(execution.source).targets


def normalized_mechanics_signature(execution: MechanicsRun) -> tuple[object, ...]:
    """Return a label-, identity-, and payload-independent mechanics shape."""

    assert isinstance(execution.result, program.ApplicationComplete)
    assert isinstance(execution.source, loci.FiniteConfiguration)
    readable_targets = _materialized_read_targets(execution)
    writable = execution.simple_program.frontier.resolve(execution.source)
    derivation_shapes = tuple(
        sorted(
            (
                tuple(
                    sorted(
                        item.action.value
                        for item in atom.source.replacement.existing
                    )
                ),
                tuple(
                    sorted(
                        item.action.value
                        for item in atom.source.replacement.fresh
                    )
                ),
                type(atom.source.continuation).__name__,
                len(atom.successor.entries) - len(execution.source.entries),
            )
            for atom in execution.result.applied_atoms.atoms
            if isinstance(atom, program.AppliedDerivation)
        )
    )
    no_successor_shapes = tuple(
        sorted(
            atom.source.outcome.value
            for atom in execution.result.no_successor_partition.atoms
        )
    )
    return (
        execution.source.contract.kind.value,
        len(execution.source.entries),
        tuple(sorted(target.kind.value for target, _ in execution.source.entries)),
        len(readable_targets),
        tuple(sorted(target.kind.value for target in readable_targets)),
        len(writable.existing),
        tuple(
            sorted(capability.target.kind.value for capability in writable.existing)
        ),
        len(writable.fresh),
        tuple(
            sorted(len(capability.target.interface) for capability in writable.fresh)
        ),
        derivation_shapes,
        no_successor_shapes,
        rules.cardinality_size(execution.result.derivation_cardinality),
        rules.cardinality_size(execution.result.successor_cardinality),
    )


def _payload(disposition: rules.Disposition) -> alphabets.SemanticValue | None:
    if type(disposition.payload) is rules.NoPayload:
        return None
    assert type(disposition.payload) is rules.ValuePayload
    return disposition.payload.value


def _record_values(configuration: loci.FiniteConfiguration) -> dict[str, object]:
    return {
        str(target.path[-1]): value
        for target, value in configuration.entries
        if target.kind is loci.LocusKind.NAMED
    }


def _assert_exact_total_replacement(
    derivation: program.AppliedDerivation,
    *,
    existing: tuple[
        tuple[loci.Locus, rules.DispositionAction, alphabets.SemanticValue | None],
        ...,
    ],
    fresh: tuple[
        tuple[
            loci.FreshReference,
            rules.DispositionAction,
            alphabets.SemanticValue | None,
        ],
        ...,
    ] = (),
) -> None:
    actual_existing = {
        item.target: (item.action, _payload(item))
        for item in derivation.source.replacement.existing
    }
    actual_fresh = {
        item.target: (item.action, _payload(item))
        for item in derivation.source.replacement.fresh
    }
    assert actual_existing == {
        target: (action, value)
        for target, action, value in existing
    }
    assert actual_fresh == {
        target: (action, value)
        for target, action, value in fresh
    }


def _assert_px10_step_algebra(
    execution: MechanicsRun,
    source: loci.FiniteConfiguration,
    result: program.ApplicationComplete,
    *,
    terminal: bool,
) -> program.AppliedDerivation:
    """Prove one deterministic codec step's complete result algebra."""

    writable = execution.simple_program.frontier.resolve(source)
    readable = execution.simple_program.neighborhood.resolve(source)
    assert type(writable) is frontiers.WritableCapabilities

    source_outcomes = result.source_outcomes
    support = source_outcomes.support
    assert source_outcomes.probability_law is None
    assert support.presentation is rules.SupportPresentation.FINITE
    assert support.relation is None
    assert len(support.atoms) == 1
    source_atom = support.atoms[0]
    assert type(source_atom) is rules.Derivation
    assert type(support.cardinality) is rules.ExactlyOne
    assert type(result.outcome_atom_cardinality) is rules.ExactlyOne
    assert type(result.derivation_cardinality) is rules.ExactlyOne
    assert type(result.successor_cardinality) is rules.ExactlyOne

    assert len(result.applied_atoms.atoms) == 1
    applied = result.applied_atoms.atoms[0]
    assert type(applied) is program.AppliedDerivation
    assert applied.source == source_atom
    assert type(result.applied_atoms.cardinality) is rules.ExactlyOne
    assert result.no_successor_partition.atoms == ()
    assert type(result.no_successor_partition.cardinality) is rules.ExactlyZero

    fibers = result.successor_quotient_with_derivation_fibers
    assert len(fibers.atoms) == 1
    fiber = fibers.atoms[0]
    assert fiber.derivations == (applied,)
    assert loci.configuration_equal(fiber.successor, applied.successor)
    assert type(fibers.cardinality) is rules.ExactlyOne
    for measure in (
        result.applied_atom_measure,
        result.successor_submeasure,
        result.no_successor_submeasure,
    ):
        assert type(measure) is program.MeasureAbsent

    disposition = source_atom.replacement
    assert disposition.totality_evidence.kind is rules.CertificateKind.TOTALITY
    assert tuple(item.target for item in disposition.existing) == tuple(
        capability.target for capability in writable.existing
    )
    assert tuple(item.target for item in disposition.fresh) == tuple(
        capability.target for capability in writable.fresh
    )
    assert all(
        item.evidence.kind is rules.CertificateKind.TOTALITY
        for item in disposition.entries
    )
    assert source_atom.progress is rules.Progress.ADVANCED
    assert type(source_atom.continuation) is (
        rules.Stop if terminal else rules.Continue
    )

    evidence = result.evidence
    assert evidence.phases == tuple(program.ApplicationPhase)
    assert evidence.program_identity == execution.simple_program.canonical_identity
    assert evidence.input_configuration_identity == source.identity
    assert evidence.readable_binding_identity == loci.canonical_identity(readable)
    assert evidence.writable_binding_identity == loci.canonical_identity(writable)
    assert evidence.application_identity == loci.canonical_identity(
        (
            evidence.program_identity,
            evidence.input_configuration_identity,
            evidence.readable_binding_identity,
            evidence.writable_binding_identity,
        )
    )
    assert (
        evidence.canonical_rule_identity
        == execution.simple_program.rule.canonical_identity
    )

    input_lineage = program.TraceLineage(
        loci.canonical_identity(("direct-application-root", source.identity))
    )
    assert evidence.input_trace_lineage_identity == input_lineage.canonical_identity
    assert applied.input_trace_lineage == input_lineage
    edge = loci.canonical_identity(
        (
            input_lineage.canonical_identity,
            evidence.application_identity,
            source_atom.canonical_identity,
            source_atom.progress.value,
        )
    )
    assert applied.output_trace_lineage == program.TraceLineage(
        input_lineage.root_identity,
        (*input_lineage.path, edge),
    )
    assert applied.evidence.application_identity == evidence.application_identity
    assert applied.evidence.disposition_identity == disposition.canonical_identity
    assert tuple(
        binding.reference for binding in applied.fresh_bindings
    ) == tuple(item.target for item in disposition.fresh)
    assert tuple(
        binding.identity for binding in applied.fresh_bindings
    ) == tuple(
        loci.bind_fresh(
            item.target,
            input_configuration_identity=source.identity,
            canonical_rule_identity=evidence.canonical_rule_identity,
            witness_identity=source_atom.witness.canonical_identity,
        )
        for item in disposition.fresh
    )
    for item, binding in zip(
        disposition.fresh,
        applied.fresh_bindings,
        strict=True,
    ):
        assert applied.successor.contains(binding.identity) == (
            item.action is rules.DispositionAction.CREATE
        )
    return applied


def _assert_px10_trajectory_algebra(
    execution: MechanicsRun,
) -> tuple[
    program.ApplicationComplete,
    loci.FiniteConfiguration,
    program.AppliedDerivation,
]:
    """Prove every step and return the terminal result, state, and atom."""

    steps = (
        execution.trajectory
        if execution.trajectory
        else ((execution.source, execution.result),)
    )
    assert loci.configuration_equal(steps[0][0], execution.source)
    assert steps[0][1] == execution.result
    prior_applied: program.AppliedDerivation | None = None
    for index, (step_source, step_result) in enumerate(steps):
        assert type(step_source) is loci.FiniteConfiguration
        assert isinstance(step_result, program.ApplicationComplete)
        if prior_applied is not None:
            assert loci.configuration_equal(step_source, prior_applied.successor)
        prior_applied = _assert_px10_step_algebra(
            execution,
            step_source,
            step_result,
            terminal=index == len(steps) - 1,
        )
    assert prior_applied is not None
    terminal_result = steps[-1][1]
    assert isinstance(terminal_result, program.ApplicationComplete)
    return terminal_result, prior_applied.successor, prior_applied


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
        if row.spf == "SPF032":
            assert isinstance(execution.source, loci.FiniteConfiguration)
            assert execution.source.contract.kind is loci.CarrierKind.GRID
            (
                priority,
                source_a,
                destination,
                source_b,
                resolution,
            ) = tuple(target for target, _ in execution.source.entries)
            assert _materialized_read_targets(execution) == (
                source_a,
                source_b,
                destination,
                priority,
            )
            assert _resolved_write_targets(execution) == (
                source_a,
                source_b,
                destination,
                resolution,
            )
            assert len(derivations) == len(successors) == 1
            assert tuple(value for _, value in successors[0].entries) == (
                0,
                0,
                1,
                0,
                1,
            )
            _assert_exact_total_replacement(
                derivations[0],
                existing=(
                    (
                        source_a,
                        rules.DispositionAction.REPLACE,
                        0,
                    ),
                    (
                        source_b,
                        rules.DispositionAction.REPLACE,
                        0,
                    ),
                    (
                        destination,
                        rules.DispositionAction.REPLACE,
                        1,
                    ),
                    (
                        resolution,
                        rules.DispositionAction.REPLACE,
                        1,
                    ),
                ),
            )
            assert isinstance(
                derivations[0].source.continuation,
                rules.Continue,
            )
            denotation = execution.simple_program.rule.descriptor.denotation
            assert type(denotation) is rules.ClauseKernelDenotation
            assert denotation.selection is rules.ClauseSelection.FIRST
            assert len(denotation.clauses) == 2
            assert all(
                clause.condition.primitive is rules.ExpressionPrimitive.GATE
                for clause in denotation.clauses
            )
            assert all(
                type(clause.result) is rules.DerivationClauseResult
                and any(
                    plan.selector.target == destination
                    for plan in clause.result.existing_plans
                )
                for clause in denotation.clauses
            )
            assert rules.cardinality_size(result.derivation_cardinality) == 1
            assert rules.cardinality_size(result.successor_cardinality) == 1
            return

        if row.spf == "SPF045":
            assert isinstance(execution.source, loci.FiniteConfiguration)
            assert execution.source.contract.kind is loci.CarrierKind.RECORD
            targets = _record_targets(execution.source)
            assert _materialized_read_targets(execution) == tuple(
                targets[name]
                for name in ("pc", "instruction", "counter", "register")
            )
            assert _resolved_write_targets(execution) == tuple(
                targets[name] for name in ("pc", "counter", "register")
            )
            assert len(derivations) == len(successors) == 1
            assert _record_values(successors[0]) == {
                "pc": 1,
                "instruction": 1,
                "counter": 1,
                "register": 7,
            }
            _assert_exact_total_replacement(
                derivations[0],
                existing=(
                    (
                        targets["pc"],
                        rules.DispositionAction.REPLACE,
                        1,
                    ),
                    (
                        targets["counter"],
                        rules.DispositionAction.REPLACE,
                        1,
                    ),
                    (
                        targets["register"],
                        rules.DispositionAction.REPLACE,
                        7,
                    ),
                ),
            )
            assert isinstance(
                derivations[0].source.continuation,
                rules.Continue,
            )
            denotation = execution.simple_program.rule.descriptor.denotation
            assert type(denotation) is rules.ClauseKernelDenotation
            assert len(denotation.clauses) == 1
            assert (
                denotation.clauses[0].condition.primitive
                is rules.ExpressionPrimitive.GATE
            )
            assert rules.cardinality_size(result.derivation_cardinality) == 1
            assert rules.cardinality_size(result.successor_cardinality) == 1
            return

        fields, read_names, write_names, alternatives, stopped = _PX01_CASES[
            row.spf
        ]
        assert isinstance(execution.source, loci.FiniteConfiguration)
        targets = _record_targets(execution.source)
        assert _materialized_read_targets(execution) == tuple(
            targets[name] for name in read_names
        )
        assert set(_resolved_write_targets(execution)) == {
            targets[name] for name in write_names
        }
        assert len(derivations) == len(alternatives)
        source_values = dict(execution.source.entries)
        for derivation, replacements in zip(
            derivations, alternatives, strict=True
        ):
            expected_map = dict(source_values)
            expected_map.update(
                (targets[name], value) for name, value in replacements
            )
            assert dict(derivation.successor.entries) == expected_map
            _assert_exact_total_replacement(
                derivation,
                existing=tuple(
                    (
                        targets[name],
                        rules.DispositionAction.REPLACE,
                        value,
                    )
                    for name, value in replacements
                ),
            )
            assert isinstance(
                derivation.source.continuation,
                rules.Stop if stopped else rules.Continue,
            )
        assert rules.cardinality_size(result.derivation_cardinality) == len(
            alternatives
        )
        assert rules.cardinality_size(result.successor_cardinality) == len(
            alternatives
        )
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
        expected_carrier = {
            "SPF002": loci.CarrierKind.WORD,
            "SPF005": loci.CarrierKind.WORD,
            "SPF016": loci.CarrierKind.WORD,
            "SPF022": loci.CarrierKind.TREE,
            "SPF023": loci.CarrierKind.HISTORY,
            "SPF025": loci.CarrierKind.WORD,
            "SPF028": loci.CarrierKind.GRAPH,
            "SPF031": loci.CarrierKind.GRID,
            "SPF037": loci.CarrierKind.WORD,
            "SPF038": loci.CarrierKind.GRAPH,
            "SPF049": loci.CarrierKind.TREE,
        }[row.spf]
        assert successor.contract.kind is expected_carrier
        if row.spf == "SPF028":
            expected_reads = (
                loci.graph_element("node", "a"),
                loci.graph_element("node", "b"),
                loci.graph_element("node", "c"),
                loci.graph_element("edge", "a-b"),
                loci.graph_element("edge", "b-c"),
            )
        elif row.spf == "SPF038":
            expected_reads = (
                loci.graph_element("node", "a"),
                loci.graph_element("node", "b"),
                loci.graph_element("node", "c"),
                loci.graph_element("node", "d"),
                loci.graph_element("edge", "a-b"),
                loci.graph_element("edge", "c-d"),
            )
        else:
            expected_reads = tuple(
                target for target, _ in execution.source.entries
            )
        assert _materialized_read_targets(execution) == expected_reads
        writable = execution.simple_program.frontier.resolve(execution.source)
        assert set(item.target for item in writable.existing) == {
            item.target
            for item in derivation.source.replacement.existing
        }
        assert set(item.target for item in writable.fresh) == {
            item.target
            for item in derivation.source.replacement.fresh
        }
        assert all(
            item.action is rules.DispositionAction.DELETE
            for item in derivation.source.replacement.existing
        )
        assert all(
            item.action is rules.DispositionAction.CREATE
            for item in derivation.source.replacement.fresh
        )
        deleted = {
            item.target for item in derivation.source.replacement.existing
        }
        for target, value in execution.source.entries:
            if target not in deleted:
                assert successor.value_at(target) == value
        if row.spf == "SPF028":
            assert execution.source.structure == successor.structure == ()
            bindings = {
                binding.reference: binding.identity
                for binding in derivation.fresh_bindings
            }
            edge_refs = tuple(
                reference
                for reference in bindings
                if reference.namespace == "g7-graph-edges"
            )
            assert len(edge_refs) == 3
            node_a = loci.graph_element("node", "a")
            node_c = loci.graph_element("node", "c")
            assert all(reference.interface == (node_a, node_c) for reference in edge_refs)
            created = {
                binding.reference: successor.value_at(binding.identity)
                for binding in derivation.fresh_bindings
            }
            node_by_name = {
                dict(value.fields)["name"]: bindings[reference]
                for reference, value in created.items()
                if isinstance(value, alphabets.ValueNode)
                and value.tag == "node"
            }
            assert set(node_by_name) == {"x", "y"}
            edges = {
                dict(value.fields)["name"]: dict(value.fields)
                for value in created.values()
                if isinstance(value, alphabets.ValueNode)
                and value.tag == "edge"
            }
            assert set(edges) == {"a-x", "x-y", "y-c"}
            assert edges["a-x"]["left"] == alphabets.StructuralReference(node_a)
            assert edges["a-x"]["right"] == alphabets.StructuralReference(node_by_name["x"])
            assert edges["x-y"]["left"] == alphabets.StructuralReference(node_by_name["x"])
            assert edges["x-y"]["right"] == alphabets.StructuralReference(node_by_name["y"])
            assert edges["y-c"]["left"] == alphabets.StructuralReference(node_by_name["y"])
            assert edges["y-c"]["right"] == alphabets.StructuralReference(node_c)
        elif row.spf == "SPF038":
            assert execution.source.structure == successor.structure == ()
            for target, value in execution.source.entries:
                assert isinstance(value, alphabets.ValueNode)
                expected_tag = (
                    "node" if target.path[0] == "node" else "edge"
                )
                assert value.kind is alphabets.ValueKind.GRAPH
                assert value.tag == expected_tag
            bindings = {
                binding.reference: binding.identity
                for binding in derivation.fresh_bindings
            }
            assert {
                reference.local_key: reference.interface
                for reference in bindings
            } == {
                "a-c": (
                    loci.graph_element("node", "a"),
                    loci.graph_element("node", "c"),
                ),
                "b-d": (
                    loci.graph_element("node", "b"),
                    loci.graph_element("node", "d"),
                ),
            }
            created_values = tuple(
                successor.value_at(identity) for identity in bindings.values()
            )
            assert all(
                isinstance(value, alphabets.ValueNode)
                and value.kind is alphabets.ValueKind.GRAPH
                and value.tag == "edge"
                for value in created_values
            )
            created_edges = {
                dict(value.fields)["name"]: dict(value.fields)
                for value in created_values
            }
            node_a = loci.graph_element("node", "a")
            node_b = loci.graph_element("node", "b")
            node_c = loci.graph_element("node", "c")
            node_d = loci.graph_element("node", "d")
            assert set(created_edges) == {"a-c", "b-d"}
            assert created_edges["a-c"] == {
                "left": alphabets.StructuralReference(node_a),
                "name": "a-c",
                "right": alphabets.StructuralReference(node_c),
            }
            assert created_edges["b-d"] == {
                "left": alphabets.StructuralReference(node_b),
                "name": "b-d",
                "right": alphabets.StructuralReference(node_d),
            }
            assert not successor.contains(loci.graph_element("edge", "a-b"))
            assert not successor.contains(loci.graph_element("edge", "c-d"))
        return

    if pressure == "PX03":
        assert isinstance(execution.source, loci.FiniteConfiguration)
        if row.spf == "SPF018":
            assert set(_materialized_read_targets(execution)) == {
                target for target, _ in execution.source.entries
            }
            assert set(_resolved_write_targets(execution)) == {
                _record_targets(execution.source)["x"],
                _record_targets(execution.source)["y"],
            }
            assert len(successors) == 2
            assert {
                (
                    _record_values(successor)["x"],
                    _record_values(successor)["y"],
                )
                for successor in successors
            } == {(0, 1), (1, 0)}
            return
        if row.spf == "SPF046":
            assert execution.source.contract.kind is loci.CarrierKind.GRAPH
            assert execution.source.structure == ()
            assert _materialized_read_targets(execution) == tuple(
                target for target, _ in execution.source.entries
            )
            assert len(derivations) == len(successors) == 1
            derivation = derivations[0]
            assert len(derivation.source.replacement.existing) == 0
            assert len(derivation.source.replacement.fresh) == 2
            assert all(
                disposition.action is rules.DispositionAction.CREATE
                for disposition in derivation.source.replacement.fresh
            )
            assert len(derivation.fresh_bindings) == 2
            successor = successors[0]
            assert successor.structure == ()
            assert len(successor.entries) == 5
            event_0 = loci.graph_element("node", "event/e0")
            event_1 = loci.graph_element("node", "event/e1")
            event_2 = loci.graph_element("node", "event/e2")
            assert {
                reference.local_key: reference.interface
                for reference in (
                    binding.reference
                    for binding in derivation.fresh_bindings
                )
            } == {
                "e0->e1": (event_0, event_1),
                "e1->e2": (event_1, event_2),
            }
            for event in (event_0, event_1, event_2):
                value = successor.value_at(event)
                assert isinstance(value, alphabets.ValueNode)
                assert value.tag == "event"
            causal_edges = {
                dict(value.fields)["name"]: dict(value.fields)
                for binding in derivation.fresh_bindings
                for value in (successor.value_at(binding.identity),)
                if isinstance(value, alphabets.ValueNode)
            }
            assert causal_edges == {
                "e0->e1": {
                    "left": alphabets.StructuralReference(event_0),
                    "name": "e0->e1",
                    "right": alphabets.StructuralReference(event_1),
                },
                "e1->e2": {
                    "left": alphabets.StructuralReference(event_1),
                    "name": "e1->e2",
                    "right": alphabets.StructuralReference(event_2),
                },
            }
            return
        expected = {
            "SPF017": (("fixed", "metric"), "movable", (Fraction(1),)),
            "SPF019": (("score0", "score1", "score2"), "winner", (1,)),
            "SPF027": (("factor_xy", "factor_yz"), "normalization", (6,)),
            "SPF035": (("stored0", "stored1", "query"), "nearest", (0, 2)),
            "SPF040": (("fitness0", "fitness1", "fitness2"), "selected", (1,)),
            "SPF051": (("history0", "history1"), "amplitude", (0,)),
        }[row.spf]
        read_names, result_name, expected_values = expected
        targets = _record_targets(execution.source)
        assert _materialized_read_targets(execution) == tuple(
            targets[name] for name in read_names
        )
        assert _resolved_write_targets(execution) == (targets[result_name],)
        assert len(successors) == len(expected_values)
        assert {
            _record_values(successor)[result_name]
            for successor in successors
        } == set(expected_values)
        for derivation in derivations:
            disposition = derivation.source.replacement.existing
            assert len(disposition) == 1
            assert disposition[0].target == targets[result_name]
            assert disposition[0].action is rules.DispositionAction.REPLACE
            assert isinstance(
                derivation.source.continuation,
                rules.Stop if row.spf == "SPF035" else rules.Continue,
            )
        return

    if pressure == "PX04":
        if row.spf == "SPF039":
            for cardinality in (
                result.outcome_atom_cardinality,
                result.derivation_cardinality,
                result.successor_cardinality,
            ):
                assert isinstance(cardinality, rules.Many)
                assert cardinality.infinite is rules.InfiniteCardinality.UNCOUNTABLE
            return
        expected = {
            "SPF014": (1, 1),
            "SPF018": (2, 2),
            "SPF024": (1, 1),
            "SPF026": (0, 0),
            "SPF029": (2, 2),
            "SPF033": (2, 1),
        }[row.spf]
        assert rules.cardinality_size(result.derivation_cardinality) == expected[0]
        assert rules.cardinality_size(result.successor_cardinality) == expected[1]
        if expected[0] == 0:
            assert len(result.no_successor_partition.atoms) == 1
            no_successor = result.no_successor_partition.atoms[0]
            assert (
                no_successor.source.outcome
                is rules.NoSuccessorOutcome.TERMINAL
            )
        if row.spf == "SPF033":
            fibers = result.successor_quotient_with_derivation_fibers.atoms
            assert len(fibers) == 1
            assert len(fibers[0].derivations) == 2
            assert _record_values(fibers[0].successor)["symbol"] == 1
        if row.spf in {"SPF018", "SPF029"}:
            assert {
                (
                    _record_values(successor)["x"],
                    _record_values(successor)["y"],
                )
                for successor in successors
            } == {(0, 1), (1, 0)}
        if row.spf == "SPF014":
            assert execution.source.contract.kind is loci.CarrierKind.RECORD
            targets = _record_targets(execution.source)
            assert _materialized_read_targets(execution) == (
                targets["domain_size"],
                targets["required_p0"],
            )
            assert set(_resolved_write_targets(execution)) == {
                targets["p0"],
                targets["model_complete"],
            }
            assert len(successors) == 1
            assert _record_values(successors[0]) == {
                "domain_size": 1,
                "required_p0": 1,
                "p0": 1,
                "model_complete": 1,
            }
        elif row.spf == "SPF024":
            assert execution.source.contract.kind is loci.CarrierKind.GRID
            source_targets = tuple(
                target for target, _ in execution.source.entries
            )
            assert _materialized_read_targets(execution) == source_targets[:2]
            assert _resolved_write_targets(execution) == source_targets[2:]
            assert len(successors) == 1
            assert tuple(value for _, value in successors[0].entries) == (
                1,
                0,
                0,
                1,
                1,
            )
        if row.spf in {"SPF014", "SPF024"}:
            assert all(
                isinstance(item.source.continuation, rules.Stop)
                for item in derivations
            )
        return

    if pressure == "PX05":
        if row.spf == "SPF039":
            assert isinstance(execution.source, loci.IntensionalConfiguration)
            assert type(
                execution.simple_program.frontier.resolve(execution.source)
            ) is frontiers.IntensionalWritableCapabilities
            assert type(
                execution.simple_program.neighborhood.resolve(execution.source)
            ) is neighborhoods.IntensionalReadableView
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
        if row.spf == "SPF006":
            assert tuple(value for _, value in successor.entries) == (
                Fraction(0),
                Fraction(1),
                Fraction(1, 4),
                1,
            )
        else:
            assert row.spf == "SPF036"
            solution = successor.entries[1][1]
            assert isinstance(solution, alphabets.ValueNode)
            assert solution.tag == "maximal-solution"
            assert dict(solution.fields) == {
                "domain": "maximal-real-line",
                "expression": "x(t)=t",
                "initial": 0,
            }
        return

    if pressure == "PX06":
        law = result.source_outcomes.probability_law
        assert law is not None
        expected_masses = {
            "SPF009": (Fraction(1, 2), Fraction(1, 2)),
            "SPF015": (Fraction(1, 2), Fraction(1, 2)),
            "SPF041": (Fraction(1, 3), Fraction(2, 3)),
            "SPF043": (Fraction(1, 4),) * 4,
            "SPF047": (Fraction(1, 4), Fraction(1, 4), Fraction(1, 2)),
        }[row.spf]
        assert tuple(sorted(item.mass for item in law.masses)) == expected_masses
        assert isinstance(result.applied_atom_measure, program.MeasureAvailable)
        assert result.applied_atom_measure.measure.total_mass == Fraction(1)
        assert isinstance(result.successor_submeasure, program.MeasureAvailable)
        successor_mass = Fraction(3, 4) if row.spf == "SPF047" else Fraction(1)
        assert result.successor_submeasure.measure.total_mass == successor_mass
        if row.spf == "SPF047":
            assert isinstance(
                result.no_successor_submeasure,
                program.MeasureAvailable,
            )
            assert (
                result.no_successor_submeasure.measure.total_mass
                == Fraction(1, 4)
            )
            assert len(result.no_successor_partition.atoms) == 1
            assert len(derivations) == 2
            assert {
                (
                    _record_values(successor)["incumbent"],
                    _record_values(successor)["proposal_counter"],
                )
                for successor in successors
            } == {(1, 1), (0, 1)}
        elif row.spf == "SPF043":
            assert len(derivations) == len(successors) == 4
            assert {
                (
                    _record_values(successor)["node0_successor"],
                    _record_values(successor)["node1_successor"],
                )
                for successor in successors
            } == {(0, 0), (0, 1), (1, 0), (1, 1)}
        elif row.spf == "SPF041":
            assert {
                (
                    _record_values(successor)["fit_parameter"],
                    _record_values(successor)["generated_path"],
                    _record_values(successor)["phase"],
                )
                for successor in successors
            } == {(2, 0, 1), (2, 1, 1)}
        elif row.spf == "SPF015":
            assert {
                (
                    _record_values(successor)["contact_site"],
                    _record_values(successor)["free_site"],
                    _record_values(successor)["attached"],
                    _record_values(successor)["relaunch"],
                )
                for successor in successors
            } == {(1, 0, 1, 0), (0, 1, 0, 1)}
        else:
            assert row.spf == "SPF009"
            assert {
                _record_values(successor)["site"]
                for successor in successors
            } == {-1, 1}
        assert all(
            isinstance(item.source.continuation, rules.Continue)
            for item in derivations
        )
        return

    if pressure == "PX07":
        assert len(successors) == 1
        expected = {
            "SPF034": {
                "cell": 0,
                "mutable_rule_entry": 31,
                "rule_version": 1,
                "phase": 1,
            },
            "SPF048": {
                "pc": 0,
                "memory0_opcode": 0,
                "memory1_data": 7,
                "halted": 1,
            },
        }[row.spf]
        assert _record_values(successors[0]) == expected
        if row.spf == "SPF034":
            assert len(derivations) == 1
            targets = _record_targets(execution.source)
            assert _materialized_read_targets(execution) == tuple(
                targets[name]
                for name in (
                    "cell",
                    "mutable_rule_entry",
                    "rule_version",
                    "phase",
                )
            )
            assert _resolved_write_targets(execution) == tuple(
                targets[name]
                for name in (
                    "cell",
                    "mutable_rule_entry",
                    "rule_version",
                    "phase",
                )
            )
            denotation = execution.simple_program.rule.descriptor.denotation
            assert type(denotation) is rules.ClauseKernelDenotation
            assert len(denotation.clauses) == 1
            clause = denotation.clauses[0]
            assert (
                clause.condition.primitive
                is rules.ExpressionPrimitive.GATE
            )
            assert type(clause.result) is rules.DerivationClauseResult
            plans = {
                plan.selector.target: plan
                for plan in clause.result.existing_plans
            }
            assert (
                plans[targets["mutable_rule_entry"]].value.primitive
                is rules.ExpressionPrimitive.ADD
            )
            assert (
                plans[targets["rule_version"]].value.primitive
                is rules.ExpressionPrimitive.ADD
            )
            _assert_exact_total_replacement(
                derivations[0],
                existing=(
                    (
                        targets["cell"],
                        rules.DispositionAction.REPLACE,
                        0,
                    ),
                    (
                        targets["mutable_rule_entry"],
                        rules.DispositionAction.REPLACE,
                        31,
                    ),
                    (
                        targets["rule_version"],
                        rules.DispositionAction.REPLACE,
                        1,
                    ),
                    (
                        targets["phase"],
                        rules.DispositionAction.REPLACE,
                        1,
                    ),
                ),
            )
        return

    if pressure == "PX08":
        expected_count = 2 if row.spf == "SPF035" else 1
        assert len(derivations) == expected_count
        assert all(
            isinstance(item.source.continuation, rules.Stop)
            for item in derivations
        )
        if row.primary == "PX08":
            expected = {
                "SPF010": {"witness": 4, "phase": 1},
                "SPF020": {"result": 7, "phase": 1},
                "SPF044": {"frame_depth": 0, "result": 5, "phase": 1},
            }[row.spf]
            values = _record_values(successors[0])
            assert all(values[name] == value for name, value in expected.items())
        if row.spf == "SPF012":
            assert row.primary == "PX10"
            assert len(successors) == 1
            _assert_px10_step_algebra(
                execution,
                execution.source,
                result,
                terminal=True,
            )
            source_values = _record_values(execution.source)
            assert tuple(
                source_values[f"symbol{index}"]
                for index in range(3)
            ) == ("A", "A", "A")
            assert (source_values["symbol3"], source_values["symbol4"]) == (
                "<end>",
                "<end>",
            )
            output_values = _record_values(successors[0])
            record = output_values["run0"]
            assert type(record) is alphabets.ValueNode
            assert record.kind is alphabets.ValueKind.RECORD
            assert record.tag == "run-record"
            assert dict(record.fields) == {"symbol": "A", "length": 3}
            assert output_values["run1"] == _codec_record(
                "unset",
                status="unset",
            )
            assert output_values["cursor"] == "done"
        return

    if pressure == "PX10":
        assert type(execution.representation_case_index) is int
        assert execution.representation_case_index in (0, 1)
        representation = execution.representation
        assert representation is not None
        assert representation.profile is alphabets.RepresentationProfile.EXACT
        assert execution.representation_source is not None
        assert execution.representation_target is not None
        encoded = representation.forward(execution.representation_source)
        assert encoded == execution.representation_target
        assert representation.inverse(encoded) == execution.representation_source
        assert alphabets.semantic_equal(
            _materialized_px10_source(execution),
            execution.representation_source,
        )
        final_result, final_successor, final_derivation = (
            _assert_px10_trajectory_algebra(execution)
        )
        expected_step_count = {
            "SPF055": 2,
            "SPF056": 3,
            "SPF059": 3,
        }.get(row.spf, 1)
        actual_steps = (
            execution.trajectory
            if execution.trajectory
            else ((execution.source, execution.result),)
        )
        assert len(actual_steps) == expected_step_count
        expected_shapes = {
            "SPF012": (loci.CarrierKind.RECORD, 6, 3),
            "SPF054": (loci.CarrierKind.TREE, 3, 3),
            "SPF055": (loci.CarrierKind.FIELD, 6, 3),
            "SPF056": (loci.CarrierKind.HISTORY, 9, 14),
            "SPF057": (loci.CarrierKind.GRID, 4, 6),
            "SPF058": (loci.CarrierKind.PRODUCT, 9, 3),
            "SPF059": (loci.CarrierKind.HISTORY, 5, 10),
            "SPF060": (loci.CarrierKind.WORD, 9, 6),
        }[row.spf]
        carrier, read_count, write_count = expected_shapes
        assert execution.source.contract.kind is carrier
        assert len(_materialized_read_targets(execution)) == read_count
        assert len(_resolved_write_targets(execution)) == write_count

        if row.spf == "SPF055":
            assert len(execution.trajectory) == 2
            first_source, first_result = execution.trajectory[0]
            second_source, second_result = execution.trajectory[1]
            assert loci.configuration_equal(first_source, execution.source)
            first_successors = _finite_successors(first_result)
            second_successors = _finite_successors(second_result)
            assert len(first_successors) == len(second_successors) == 1
            assert loci.configuration_equal(second_source, first_successors[0])
            first_derivations = tuple(
                atom
                for atom in first_result.applied_atoms.atoms
                if isinstance(atom, program.AppliedDerivation)
            )
            final_derivations = tuple(
                atom
                for atom in second_result.applied_atoms.atoms
                if isinstance(atom, program.AppliedDerivation)
            )
            assert len(first_derivations) == len(final_derivations) == 1
            assert (
                first_derivations[0].source.progress
                is rules.Progress.ADVANCED
            )
            assert isinstance(
                first_derivations[0].source.continuation,
                rules.Continue,
            )
            assert (
                first_successors[0].value_at(
                    loci.field_point("codec", (0,), component="low")
                )
                == Fraction(0)
            )
            assert (
                first_successors[0].value_at(
                    loci.field_point("codec", (0,), component="high")
                )
                == Fraction(1, 2)
            )
            assert (
                first_successors[0].value_at(
                    loci.field_point("codec", (0,), component="cursor")
                )
                == 1
            )
            assert (
                final_derivations[0].source.progress
                is rules.Progress.ADVANCED
            )
            assert isinstance(
                final_derivations[0].source.continuation,
                rules.Stop,
            )
            final_result = second_result
            final_successor = second_successors[0]
            assert (
                final_successor.value_at(
                    loci.field_point("codec", (0,), component="cursor")
                )
                == "done"
            )
        final_derivations = (final_derivation,)

        materialized_target = _materialized_px10_target(
            execution,
            final_result,
            final_successor,
        )
        assert alphabets.semantic_equal(
            materialized_target,
            execution.representation_target,
        )
        if row.spf == "SPF012":
            materialized_source = _materialized_px10_source(execution)
            assert type(materialized_source) is alphabets.ValueNode
            source_symbols = materialized_source.items
            unset = _codec_record("unset", status="unset")
            run_specs = []
            reached_unset = False
            for index in range(2):
                record = final_successor.value_at(
                    loci.named(f"run{index}", scope="record")
                )
                if alphabets.semantic_equal(record, unset):
                    reached_unset = True
                    continue
                assert not reached_unset
                assert type(record) is alphabets.ValueNode
                assert record.tag == "run-record"
                fields = dict(record.fields)
                run_specs.append((fields["symbol"], fields["length"]))
            assert run_specs
            assert sum(length for _, length in run_specs) == len(source_symbols)
            assert tuple(
                symbol
                for symbol, length in run_specs
                for _ in range(length)
            ) == source_symbols
            assert all(
                left_symbol != right_symbol
                for (left_symbol, _), (right_symbol, _) in zip(
                    run_specs,
                    run_specs[1:],
                )
            )
            assert (
                final_successor.value_at(loci.named("cursor", scope="record"))
                == "done"
            )
            denotation = execution.simple_program.rule.descriptor.denotation
            assert type(denotation) is rules.ClauseKernelDenotation
            assert denotation.clauses[0].condition.primitive is (
                rules.ExpressionPrimitive.GATE
            )
        if row.spf == "SPF054":
            derivation = final_derivations[0]
            assert type(encoded) is alphabets.ValueNode
            expected_created = len(encoded.items)
            assert len(derivation.source.replacement.existing) == 1
            assert len(derivation.source.replacement.fresh) == 2
            assert len(derivation.fresh_bindings) == 2
            assert sum(
                item.action is rules.DispositionAction.CREATE
                for item in derivation.source.replacement.fresh
            ) == expected_created
            assert all(
                binding.reference.namespace == "g7-prefix-output"
                for binding in derivation.fresh_bindings
            )
            binding_by_reference = {
                binding.reference: binding.identity
                for binding in derivation.fresh_bindings
            }
            created_bits = tuple(
                final_successor.value_at(
                    binding_by_reference[disposition.target]
                )
                for disposition in derivation.source.replacement.fresh
                if disposition.action is rules.DispositionAction.CREATE
            )
            assert created_bits == encoded.items
            assert (
                execution.source.value_at(
                    loci.path("root", "codebook", scope="prefix-tree")
                )
                == _codec_record(
                    "prefix-tree",
                    A="0",
                    B="10",
                    C="11",
                )
            )
        if row.spf == "SPF055":
            partition_value = execution.source.value_at(
                loci.field_point("codec", (0,), component="partition")
            )
            assert type(partition_value) is alphabets.ValueNode
            assert partition_value.tag == "cumulative-partition"
            assert all(
                step_result.source_outcomes.probability_law is None
                for _, step_result in execution.trajectory
            )
            materialized_source = _materialized_px10_source(execution)
            assert type(materialized_source) is alphabets.ValueNode
            assert (
                execution.trajectory[1][0].value_at(
                    loci.field_point("codec", (0,), component="symbol-1")
                )
                == materialized_source.items[1]
            )
        if row.spf == "SPF056":
            materialized_source = _materialized_px10_source(execution)
            assert type(materialized_source) is alphabets.ValueNode
            symbols = materialized_source.items
            reconstruction = tuple(
                final_successor.value_at(
                    loci.occurrence("codec-reconstruction", index)
                )
                for index in range(len(symbols))
            )
            history = tuple(
                final_successor.value_at(
                    loci.occurrence("codec-history", index)
                )
                for index in range(len(symbols))
            )
            assert reconstruction == symbols
            assert history == symbols
            assert (
                final_successor.value_at(
                    loci.named("cursor", scope="history-workspace")
                )
                == "done"
            )
            assert (
                final_successor.value_at(
                    loci.named("symbol-queue", scope="history-workspace")
                )
                == _codec_word("symbol-queue")
            )
            third_record = final_successor.value_at(
                loci.occurrence("codec-record", 2)
            )
            assert type(third_record) is alphabets.ValueNode
            if third_record.tag == "reference-record":
                assert third_record.tag == "reference-record"
                assert dict(third_record.fields) == {"offset": 2, "length": 2}
                third_source = execution.trajectory[2][0]
                assert (
                    third_source.value_at(loci.occurrence("codec-input", 2)),
                    third_source.value_at(loci.occurrence("codec-input", 3)),
                ) == (
                    third_source.value_at(loci.occurrence("codec-history", 0)),
                    third_source.value_at(loci.occurrence("codec-history", 1)),
                )
            else:
                assert third_record.tag == "literal-record"
                assert dict(third_record.fields) == {"symbol": "C"}
        if (
            row.spf == "SPF057"
            and type(materialized_target) is alphabets.ValueNode
            and materialized_target.tag == "region-branch"
        ):
            derivation = final_derivations[0]
            assert len(derivation.source.replacement.existing) == 2
            assert len(derivation.source.replacement.fresh) == 4
            assert len(derivation.fresh_bindings) == 4
            assert {
                binding.reference.local_key
                for binding in derivation.fresh_bindings
            } == {
                "north-west",
                "north-east",
                "south-west",
                "south-east",
            }
            assert all(
                item.action is rules.DispositionAction.CREATE
                for item in derivation.source.replacement.fresh
            )
            assert all(
                type(final_successor.value_at(binding.identity))
                is alphabets.ValueNode
                for binding in derivation.fresh_bindings
            )
        if (
            row.spf == "SPF057"
            and type(materialized_target) is alphabets.ValueNode
            and materialized_target.tag == "region-leaf"
        ):
            derivation = final_derivations[0]
            assert len(derivation.source.replacement.existing) == 2
            assert len(derivation.source.replacement.fresh) == 4
            assert len(derivation.fresh_bindings) == 4
            assert all(
                item.action is rules.DispositionAction.ABSENT
                for item in derivation.source.replacement.fresh
            )
            assert all(
                not final_successor.contains(binding.identity)
                for binding in derivation.fresh_bindings
            )
            assert type(materialized_target) is alphabets.ValueNode
            assert materialized_target.tag == "region-leaf"
            assert dict(materialized_target.fields) == {
                "bounds": "2x2",
                "value": 1,
            }
            assert tuple(
                execution.source.value_at(target)
                for target in (
                    loci.cell((-1, -1), axes=("x", "y")),
                    loci.cell((-1, 0), axes=("x", "y")),
                    loci.cell((0, -1), axes=("x", "y")),
                    loci.cell((0, 0), axes=("x", "y")),
                )
            ) == (1, 1, 1, 1)
        if row.spf == "SPF058":
            base = loci.named("basis-workspace", scope="product")
            assert tuple(
                execution.source.value_at(
                    loci.product_locus(f"basis-{row_index}-{column}", (base,))
                )
                for row_index in range(2)
                for column in range(2)
            ) == (1, 1, 1, -1)
            assert (
                execution.source.value_at(
                    loci.product_locus("basis-selection", (base,))
                )
                == "walsh-2"
            )
            assert (
                execution.source.value_at(
                    loci.product_locus("exact-mode", (base,))
                )
                is True
            )
            assert type(encoded) is alphabets.ValueNode
            assert tuple(
                final_successor.value_at(
                    loci.product_locus(f"coefficient-{index}", (base,))
                )
                for index in range(2)
            ) == encoded.items
            assert not final_successor.contains(
                loci.product_locus("result", (base,))
            )
        if row.spf == "SPF059":
            assert type(execution.representation_source) is alphabets.ValueNode
            assert type(encoded) is alphabets.ValueNode
            samples = execution.representation_source.items
            residuals = tuple(
                final_successor.value_at(loci.occurrence("residual", index))
                for index in range(3)
            )
            reconstruction = tuple(
                final_successor.value_at(
                    loci.occurrence("predictive-reconstruction", index)
                )
                for index in range(3)
            )
            assert residuals == encoded.items
            assert reconstruction == samples
            for index, (step_source, _) in enumerate(execution.trajectory):
                assert (
                    step_source.value_at(
                        loci.named(
                            "current-sample",
                            scope="predictive-workspace",
                        )
                    )
                    == samples[index]
                )
                assert (
                    step_source.value_at(
                        loci.named(
                            "previous-sample",
                            scope="predictive-workspace",
                        )
                    )
                    == (0 if index == 0 else samples[index - 1])
                )
                assert (
                    step_source.value_at(
                        loci.named(
                            "predictor-model",
                            scope="predictive-workspace",
                        )
                    )
                    == "previous-sample"
                )
            assert (
                final_successor.value_at(
                    loci.named("cursor", scope="predictive-workspace")
                )
                == "done"
            )
        if row.spf == "SPF060":
            assert type(materialized_target) is alphabets.ValueNode
            assert materialized_target.kind is alphabets.ValueKind.WORD
            assert materialized_target.tag == "xor-output"
            assert materialized_target.items == encoded.items
            assert (
                final_successor.value_at(
                    loci.named("alignment", scope="xor-workspace")
                )
                == "done"
            )
            assert (
                final_successor.value_at(
                    loci.named("stream-cursor", scope="xor-workspace")
                )
                == 3
            )
            assert (
                final_successor.value_at(
                    loci.named("generator-cursor", scope="xor-workspace")
                )
                == 3
            )
        denotation = execution.simple_program.rule.descriptor.denotation
        assert type(denotation) is rules.ClauseKernelDenotation
        assert denotation.clauses
        assert all(
            clause.condition.primitive is rules.ExpressionPrimitive.GATE
            for clause in denotation.clauses
        )
        return

    if pressure == "PX09":
        assert len(successors) == 1
        assert _record_values(successors[0]) == {
            "cursor": True,
            "wire_x": True,
            "wire_y": True,
        }
        assert isinstance(derivations[0].source.continuation, rules.Stop)
        return

    if pressure == "PX11":
        assert len(successors) == 1
        assert len(derivations) == 1
        derivation = derivations[0]
        assert len(derivation.fresh_bindings) == 1
        binding = derivation.fresh_bindings[0]
        assert binding.reference.namespace == "g7-priority-oracle"
        assert binding.reference.local_key == "O[0]"
        assert derivation.successor.value_at(binding.identity) == 1
        values = _record_values(successors[0])
        assert {
            name: values[name]
            for name in (
                "p0_state",
                "p1_state",
                "p1_use_o0",
                "p1_work",
                "scheduler_next",
            )
        } == {
            "p0_state": 1,
            "p1_state": 2,
            "p1_use_o0": -1,
            "p1_work": 0,
            "scheduler_next": 1,
        }
        assert len(_materialized_read_targets(execution)) == 6
        assert len(_resolved_write_targets(execution)) == 6
        return

    if pressure == "PX12":
        if row.spf == "SPF004":
            assert len(derivations) == 1
            assert isinstance(derivations[0].source.continuation, rules.Stop)
            assert len(derivations[0].fresh_bindings) == 2
            assert execution.source.contract.kind is loci.CarrierKind.GRAPH
            assert all(
                isinstance(
                    derivations[0].successor.value_at(binding.identity),
                    alphabets.ValueNode,
                )
                for binding in derivations[0].fresh_bindings
            )
            return
        assert row.spf == "SPF042"
        assert len(execution.trajectory) == 3
        phase_trace = []
        for index, (step_source, step_result) in enumerate(execution.trajectory):
            step_derivations = tuple(
                atom
                for atom in step_result.applied_atoms.atoms
                if isinstance(atom, program.AppliedDerivation)
            )
            assert len(step_derivations) == 1
            step = step_derivations[0]
            assert (
                step_result.evidence.program_identity
                == execution.simple_program.canonical_identity
            )
            assert step_result.evidence.input_configuration_identity == step_source.identity
            assert isinstance(
                step.source.continuation,
                rules.Stop if index == 2 else rules.Continue,
            )
            phase_trace.append(_record_values(step.successor))
        assert (
            phase_trace[0]["phase"],
            phase_trace[0]["frame_depth"],
            phase_trace[0]["observed_result"],
        ) == (1, 1, 2)
        assert (
            phase_trace[1]["phase"],
            phase_trace[1]["frame_depth"],
            phase_trace[1]["surrogate_result"],
        ) == (2, 1, 1)
        assert (
            phase_trace[2]["phase"],
            phase_trace[2]["frame_depth"],
            phase_trace[2]["decision"],
        ) == (3, 0, 1)
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
