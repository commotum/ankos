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
    return MechanicsRun(row, simple_program, source, ca.apply(simple_program, source))


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


def _px01(row: MechanicsRow) -> MechanicsRun:
    """Couple source, control, and every possible destination atomically."""

    source, alphabet, writable, readable = _finite_history_components((0, 1, 0))
    base = (
        _existing_plan(0, rules.DispositionAction.REPLACE, rules.observation(1)),
        _existing_plan(1, rules.DispositionAction.REPLACE, rules.literal_expr(0)),
        _existing_plan(2, rules.DispositionAction.REPLACE, rules.literal_expr(0)),
    )
    clauses = [_clause(rules.literal_expr(1), _derivation_result(row.fixture, existing=base))]
    if row.spf == "SPF030":
        other = (
            _existing_plan(0, rules.DispositionAction.REPLACE, rules.literal_expr(0)),
            _existing_plan(1, rules.DispositionAction.REPLACE, rules.literal_expr(0)),
            _existing_plan(2, rules.DispositionAction.REPLACE, rules.observation(1)),
        )
        clauses.append(
            _clause(
                rules.equal(rules.observation(1), rules.literal_expr(1)),
                _derivation_result(f"{row.fixture}:alternate", existing=other),
            )
        )
    rule = _kernel(
        source,
        alphabet,
        writable,
        readable,
        tuple(clauses),
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


_PX02_SHAPES = {
    "SPF002": (0, 1),
    "SPF005": (2, 2),
    "SPF016": (2, 1),
    "SPF022": (0, 1),
    "SPF023": (0, 1),
    "SPF025": (1, 0),
    "SPF028": (2, 3),
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


def _px02(row: MechanicsRow) -> MechanicsRun:
    """Apply one input-derived total delete/create structural patch."""

    delete_count, create_count = _PX02_SHAPES[row.spf]
    source = _word_configuration((1, 2))
    alphabet = alphabets.integers()
    existing = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
        effects=(frontiers.Effect.REPLACE, frontiers.Effect.DELETE),
    )
    parent = source.entries[0][0]
    references = tuple(
        loci.FreshReference(
            f"g7-{row.spf.lower()}",
            index,
            parent=parent,
            interface=(parent,),
        )
        for index in range(create_count)
    )
    if references:
        fresh_region = frontiers.fresh(
            loci.fresh_children(references),
            namespace=frontiers.FreshNamespace(
                f"g7-{row.spf.lower()}",
                parent=parent,
            ),
            configuration_contract=source.contract,
            value_profile=alphabet.value_profile,
        )
        writable = frontiers.union((existing, fresh_region))
    else:
        writable = existing
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    existing_plans = tuple(
        _existing_plan(index, rules.DispositionAction.DELETE)
        for index in range(delete_count)
    )
    fresh_plans = tuple(
        _fresh_plan(
            index,
            rules.DispositionAction.CREATE,
            rules.add(rules.observation(0), rules.literal_expr(index + 10)),
        )
        for index in range(create_count)
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
                    existing=existing_plans,
                    fresh=fresh_plans,
                ),
            ),
        ),
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _px03(row: MechanicsRow) -> MechanicsRun:
    """Use the complete immutable snapshot in one coupled global decision."""

    marker = int(row.spf[-3:])
    source, alphabet, writable, readable = _finite_history_components(
        (marker, 2, 3, 0)
    )
    aggregate = rules.add(
        rules.observation(0),
        rules.observation(1),
        rules.observation(2),
    )
    rule = _kernel(
        source,
        alphabet,
        writable,
        readable,
        (
            _clause(
                rules.less_than(rules.observation(3), aggregate),
                _derivation_result(
                    row.fixture,
                    existing=(
                        _existing_plan(
                            3,
                            rules.DispositionAction.REPLACE,
                            aggregate,
                        ),
                    ),
                ),
            ),
        ),
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _px04(row: MechanicsRow) -> MechanicsRun:
    """Denote typed zero, witnessed one, or witnessed many alternatives."""

    desired = {
        "SPF014": 1,
        "SPF018": 2,
        "SPF024": 1,
        "SPF026": 0,
        "SPF029": 2,
        "SPF033": 2,
    }[row.spf]
    source, alphabet, writable, readable = _finite_history_components((desired,))
    solution_clauses = tuple(
        _clause(
            rules.less_than(rules.literal_expr(solution), rules.observation(0)),
            _derivation_result(
                f"{row.fixture}:solution-{solution}",
                existing=(
                    _existing_plan(
                        0,
                        rules.DispositionAction.REPLACE,
                        # SPF033 deliberately demonstrates two witnesses that
                        # quotient to one successor.
                        rules.literal_expr(
                            1 if row.spf == "SPF033" else solution + 1
                        ),
                    ),
                ),
                stop=row.spf in {"SPF014", "SPF024", "SPF026", "SPF029"},
            ),
        )
        for solution in range(2)
    )
    fallback = _clause(
        rules.equal(rules.observation(0), rules.literal_expr(0)),
        _no_successor_result(f"{row.fixture}:zero"),
    )
    rule = _kernel(
        source,
        alphabet,
        writable,
        readable,
        (*solution_clauses, fallback),
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _px05_finite(row: MechanicsRow) -> MechanicsRun:
    """Commit an exact Fraction-valued flow/event segment and stop."""

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


def _px06(row: MechanicsRow) -> MechanicsRun:
    """Return an exact law without drawing, then expose both submeasures."""

    source, alphabet, writable, readable = _finite_history_components((1, 0))
    accepted = _derivation_result(
        f"{row.fixture}:accepted",
        existing=(
            _existing_plan(
                1,
                rules.DispositionAction.REPLACE,
                rules.add(rules.observation(0), rules.literal_expr(1)),
            ),
        ),
    )
    continued = _derivation_result(f"{row.fixture}:rejected-continue")
    rule = _kernel(
        source,
        alphabet,
        writable,
        readable,
        (
            _clause(rules.literal_expr(1), accepted, mass=Fraction(1, 2)),
            _clause(rules.literal_expr(1), continued, mass=Fraction(1, 2)),
        ),
        stochastic=True,
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _px07(row: MechanicsRow) -> MechanicsRun:
    """Mutate carrier data and visible program/instruction state together."""

    source, alphabet, writable, readable = _finite_history_components((1, 30, 0))
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
                            0,
                            rules.DispositionAction.REPLACE,
                            rules.literal_expr(0),
                        ),
                        _existing_plan(
                            1,
                            rules.DispositionAction.REPLACE,
                            rules.add(rules.observation(1), rules.literal_expr(1)),
                        ),
                        _existing_plan(
                            2,
                            rules.DispositionAction.REPLACE,
                            rules.add(rules.observation(2), rules.literal_expr(1)),
                        ),
                    ),
                ),
            ),
        ),
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _px08(row: MechanicsRow) -> MechanicsRun:
    """Produce a typed one-shot successor whose continuation is stopped."""

    source, alphabet, writable, readable = _finite_history_components((1, 0))
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
                            rules.add(rules.observation(0), rules.literal_expr(6)),
                        ),
                    ),
                    stop=True,
                ),
            ),
            _clause(
                rules.equal(rules.observation(0), rules.literal_expr(0)),
                _no_successor_result(
                    f"{row.fixture}:divergent",
                    rules.NoSuccessorOutcome.DIVERGENT,
                ),
            ),
        ),
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


def _px09(row: MechanicsRow) -> MechanicsRun:
    """Evaluate a closed fixed wiring/gate expression and stop."""

    source = loci.history_configuration((True, True, False))
    alphabet = alphabets.boolean()
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    gate_value = rules.gate(
        rules.RuleExpr(
            rules.ExpressionPrimitive.TUPLE,
            (rules.observation(0), rules.observation(1)),
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
                            2,
                            rules.DispositionAction.REPLACE,
                            gate_value,
                        ),
                    ),
                    stop=True,
                ),
            ),
        ),
    )
    return _assemble(row, source, alphabet, writable, readable, rule)


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
            loci.fresh_children((reference,)),
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
        "PX05": _px05_finite,
        "PX06": _px06,
        "PX07": _px07,
        "PX08": _px08,
        "PX09": _px09,
        # G7-02 representation relations are joined here after their value
        # owner lands; until then the ordinary stopped transduction path is
        # still exercised by the same Rule/application boundary.
        "PX10": _px08,
        "PX11": _px11,
        "PX12": _px12,
    }
    execution = builders[row.primary](row)
    if not isinstance(execution.result, program.ApplicationComplete):
        detail = execution.result.fault.detail
        raise AssertionError(f"{row.spf}/{row.fixture} rejected: {detail}")
    return execution
