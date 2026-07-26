"""Test-owned G7-02 mechanics ledger and ordinary-program fixtures.

This module deliberately lives outside :mod:`ca`.  SPF/F identities are
coverage labels used to prove that the audited taxonomy is mechanically
covered; no production descriptor or application branch may inspect them.
"""

from __future__ import annotations

from dataclasses import dataclass


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

