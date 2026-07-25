# Whole-Book Construction Taxonomy Census

## Final Count

The Book inventory resolves to **60 executable semantic families**. The current
45-row catalog covers **19** of those families; **41** source-grounded families
are absent at the family level. Two additional mechanics groups are retained
as close exclusions because they are observers or interfaces rather than
distinct transition mechanics.

These numbers describe semantic construction families, not required public
classes. Presets, aliases, representations, seeds, applications, and named
examples do not inflate the family count.

| Census level | Count | Meaning |
|---|---:|---|
| Raw source leads | 1,564 | Cheap inherited and newly recorded pointers |
| Serious source leads | 190 | Passages requiring mechanics-level resolution |
| Resolved or weak leads | 1,374 | Aliases, repeated evidence, roles, exposition, or insufficient mechanics |
| Full mechanics candidates | 102 | Source-grounded constructions and close cases with semantic fingerprints |
| Executable candidate roots | 60 | Representatives of distinct executable mechanics |
| Presets or variants | 35 | Runnable differences representable as family data |
| Close-exclusion candidates | 7 | Non-family roles retained for boundary clarity |
| Consolidated mechanics groups | 62 | 60 executable families plus two close-only groups |
| Current-catalog family coverage | 19 | Executable families represented by T01–T45 |
| Proposed family additions | 41 | Executable families missing from the current catalog |
| Unresolved serious questions | 0 | No open lead, family, catalog, or API decision |

The count ladder matters: “190 serious leads,” “102 candidates,” and “60 types”
are not competing answers. They are successive consolidation levels.

## Current-Catalog Coverage: 19 Families

| ID | Semantic family |
|---|---|
| F002 | `append-only-sequence-generation` |
| F005 | `context-dependent-substitution` |
| F008 | `digit-emitting-register-transduction` |
| F017 | `front-delete-rear-append-system` |
| F024 | `indexed-history-recurrence` |
| F026 | `iterated-erasure-process` |
| F027 | `iterated-map` |
| F030 | `local-satisfaction-relation` |
| F031 | `mobile-head-grid-rewrite` |
| F033 | `multi-active-local-rewrite` |
| F034 | `multiway-rewrite` |
| F038 | `parallel-independent-substitution` |
| F040 | `parallel-network-rewrite` |
| F041 | `partial-differential-relation` |
| F047 | `recursive-function-evaluator` |
| F048 | `register-machine` |
| F052 | `structural-pattern-rewrite` |
| F053 | `synchronous-local-state-transform` |
| F055 | `weighted-network-state-update` |

## Proposed Family Additions: 41

| ID | Semantic family |
|---|---|
| F001 | `alternating-partition-local-evolution` |
| F003 | `asynchronous-local-state-automaton` |
| F004 | `event-provenance-causal-network` |
| F006 | `continuous-event-dynamics` |
| F007 | `coupled-field-mobile-locus-evolution` |
| F009 | `driven-relaxation` |
| F011 | `enumerative-semidecision` |
| F012 | `error-diffusion-transform` |
| F013 | `maximal-run-record-transduction` |
| F014 | `finite-gate-circuit` |
| F015 | `finite-model-satisfaction` |
| F016 | `first-passage-aggregation` |
| F018 | `geometric-embedding-relation` |
| F019 | `global-equation-relation` |
| F020 | `global-score-sequential-placement` |
| F021 | `hash-index-transform` |
| F022 | `history-dependent-agent-game` |
| F023 | `history-dependent-growth-rewrite` |
| F025 | `inverse-local-system-reconstruction` |
| F028 | `local-factor-weighted-relation` |
| F029 | `local-graph-rewrite` |
| F032 | `moving-frontier-shell-accretion` |
| F035 | `mutable-rule-local-automaton` |
| F036 | `nearest-neighbor-retrieval` |
| F037 | `ordinary-differential-flow` |
| F043 | `population-evolutionary-search` |
| F044 | `probabilistic-transition-model-fitting` |
| F045 | `program-randomization-test` |
| F046 | `random-functional-graph-construction` |
| F049 | `sampled-causal-order-network` |
| F050 | `stochastic-local-search` |
| F051 | `stored-program-random-access-machine` |
| F054 | `weighted-history-sum-relation` |
| F056 | `priority-dovetailed-oracle-construction` |
| F057 | `weighted-prefix-block-transduction` |
| F058 | `nested-interval-symbol-transduction` |
| F059 | `history-reference-record-transduction` |
| F060 | `recursive-uniform-region-decomposition` |
| F061 | `orthogonal-basis-coefficient-transform` |
| F062 | `predictive-residual-transduction` |
| F063 | `aligned-xor-stream-transduction` |

“Addition” means the current semantic catalog lacks the mechanics. It does not
mean the implementation should add one bespoke runtime or public class per row.

## Close Exclusions: 2 Groups

| ID | Close group | Why it is not a family |
|---|---|---|
| F010 | `encode-evolve-decode-interface` | Wraps an unchanged target construction with an encoder, stop/query, and decoder. |
| F042 | `percolation-connectivity-analysis` | Observes global connectivity of a sampled configuration rather than defining its evolution. |

Each can be implemented as an ordinary transform or observer where useful.
The exclusion says only that it should not masquerade as a new underlying
construction family.

## T01–T45 Reconciliation

Every current catalog row received exactly one disposition:

| Disposition | Count |
|---|---:|
| Retain as family | 15 |
| Retain as preset | 21 |
| Merge | 2 |
| Repair | 3 |
| Alias | 2 |
| Retire semantic role | 1 |
| Split | 1 |

The changes with architectural consequences are:

- merge T05 into the general synchronous local-state family;
- merge T15 into independent substitution with empty output as rule data;
- retire T08 because initial-condition classes are `Seed` constructors or laws;
- repair T10 to the neighbor-updating mobile mechanics actually described;
- repair T27 so geometric substitution is the construction and “fractal” is an
  output or property;
- alias T32 to local satisfaction relations and T44 to synchronous local-state
  automata;
- repair T41 from the role-like “function combination” label to executable
  recursive function evaluator F047; and
- split T40 between append-only generation and digit-emitting register
  transduction.

Family normalization also makes T09 and T25 presets under T12's common
mobile-head family, T16 a flat-string preset under T20's structural rewrite
family, T28 a dimensional preset under T14, and T34 an arithmetic preset under
generic iterated-map row T43.

The exact row-by-row mapping is in `10-RECONCILE.md`. Family definitions,
candidate membership, source anchors, and distinguishing tests are in
`11-FAMILIES.md`.

## API Finding

All 60 executable families fit:

```python
SimpleProgram(
    seed,
    alphabet,
    frontier,
    neighborhood,
    rule,
)
```

No sixth top-level component and no configurable `UpdatePolicy` survived a
family-level counterexample test. The component contracts must become more
general than the present `simple_programs.md`, especially for structured
support, nonlocal reads, complete region replacements, relations,
stochasticity, and continuous objects. The complete mapping is in
`api-pressure.md`.

## Evidence and Traceability

- `coverage.md` records sequential chapter/Notes and selective-image coverage.
- `raw-leads.csv` retains all 1,564 source pointers and terminal statuses.
- `candidates.md` contains the 102 full semantic fingerprints.
- `source-decision-matrix.csv` maps every lead to its final decision, candidate,
  catalog action, and family.
- `9-SATURATION.md` records the single frozen 40-query whole-book omission
  challenge and the final correction of its one missed interactive-system hit.
- `10-RECONCILE.md` and `11-FAMILIES.md` record catalog and family decisions.
- `13-HOSTILE-REVIEW.md` records the independent final challenge.

No serious discovery, family, catalog, or API question remains open.
