# 3-APPLICATION

Status: **COMPLETE — result algebra, atomic application, and run/tool boundary verified**

## Current Facts

- Stages 1 and 2 are complete, and the working tree began this stage clean at
  commit `96305d34cf2fb097e9d45e161375ebd20bf45999`.
- `SimpleProgram[C, V, W, R]` has exactly five stored fields.
- Frontier and Neighborhood independently resolve from one immutable
  configuration while sharing snapshot and locus identity; Rule consumes the
  resulting `R` and `W`.
- Stage 2 fixes the denotational minimum that every alternative is a total
  disposition over `W`, everything outside `W` is preserved, and read/effect
  containment is proved or carried as a closed conformance obligation.
- Stage 3 owns concrete result variants and encoding, outcomes, application,
  witness/deduplication semantics, fresh allocation, stochastic realization,
  and the boundary between one application and run/tooling requests.
- Goal 5 remains the semantic/API authority. Goal 2 may supply only the result,
  provenance, generic-application, exactness, and conformance strengths
  explicitly preserved by the integration handoff.
- No behavioral file under `src/ca`, frozen Goal 2 file, public API narrative,
  or reference scaffold is authorized to change in this stage.

## Updated Assumptions

- One result algebra can distinguish relational cardinality from execution
  outcome without creating a sixth program component.
- A family-blind commit can operate on typed dispositions and configuration
  capabilities without dispatching on carrier or semantic family.
- Witness identity can precede successor canonicalization and deduplication
  without making traversal/materialization order semantic.
- Probability laws can remain Rule denotations while concrete realization keys
  and draw evidence cross the application request/result boundary.
- One-shot relations use the same application contract; rollout is a request
  to repeat application, not an intrinsic trajectory field.

## Big Picture Objective

Define one complete Rule-result algebra and atomic application law for
deterministic, branching, stochastic, structural, continuous, symbolic, and
one-shot programs, while preserving the five-field architecture and one
family-blind execution path.

## Detailed Implementation Plan

- Consolidate Goal 5 application pressures and the explicitly preserved Goal 2
  result semantics.
- Define result cardinality, alternatives, total dispositions, outcomes,
  failure phases, evidence, witnesses, provenance, and canonical successor
  grouping.
- Define exact fresh-identity and probability realization semantics without
  ambient entropy or enumeration-dependent identity.
- Write complete family-blind application pseudocode from input validation
  through region resolution, Rule denotation, alternative validation, atomic
  commit, successor validation, and evidence retention.
- Define the boundary between one application and horizon, query, realization,
  replay, resource, trace, observer, renderer, and export requests.
- Paper-execute coupled writes, structural birth/deletion, zero/one/many
  relations, stochastic transitions, continuous/event results, symbolic
  solution families, and one-shot transforms.
- Conduct one focused hostile review and resolve every substantive Stage 3
  finding.

Files expected to change:

- `goal-6/architecture.md`
- `goal-6/3-APPLICATION.md`
- `goal-6/0-plan.md`

## No-Cheating Checks

- Application contains no catalog, family, semantic-class, carrier, locus-kind,
  or Book-source dispatch.
- Commit enforces only generic capability, disposition, identity, atomicity,
  and configuration-validity laws; it makes no construction-specific choice.
- Rule owns applicability, schedule, priority, conflicts, stochastic law,
  stopping, and actual changed set.
- Empty alternatives do not collapse quiescence, termination, invalidity,
  undefinedness, failure, or resource exhaustion.
- Successor deduplication cannot erase derivation witnesses or probability
  mass.
- Fresh identity and replay evidence do not depend on ambient RNG, UUIDs,
  global counters, traversal, branch enumeration, or materialization order.
- One-shot, continuous, and intensional relations are not forced into finite
  step lists or fake trajectories.
- No sixth program field, public helper module, behavioral runtime edit,
  frozen Goal 2 edit, Goal 4 machinery, or Goal 7 work is introduced.

## Completion Requirements

- [x] Every result cardinality, outcome, and failure phase is distinguishable
      and testable.
- [x] Total dispositions, coupled writes, overlap resolution, fresh/deleted
      structure, and preserve-outside behavior are unambiguous.
- [x] Witness-before-deduplication and successor equivalence preserve lineage,
      multiplicity, and probability correctly.
- [x] Probability laws, realization requests, draw evidence, and replay are
      distinct and lossless.
- [x] Family-blind application pseudocode covers validation, resolution,
      denotation, atomic commit, successor validation, and evidence.
- [x] Continuous, event, symbolic/intensional, stochastic, structural, and
      one-shot cases cross the same boundary without special dispatch.
- [x] `ca.rollout` is derivable from repeated application without becoming a
      program component or being mandatory for one-shot use.
- [x] Hostile review, scoped diff/whitespace checks, frozen hashes, and runtime
      baseline checks pass.
- [x] Stage 4 can settle file/public ownership without reopening application
      semantics.

## Stage Results

- `goal-6/architecture.md` now defines one exact envelope with finite or
  intensional `SupportSpace`, optional probability law, soundness-and-coverage
  evidence, typed no-successor outcomes, three independent cardinalities, and
  one `ApplicationComplete` payload. Certified zero and undetermined
  intensional emptiness are no longer conflated.
- Every derivation contains a normalized total disposition over `W`. Writable
  resolution also yields an application-private sealed `ReconstructionPlan`
  that applies structural payloads atomically and preserves everything outside
  `W` without becoming `UpdatePolicy` or a Rule read channel.
- `Rule.denote(R, W)` is closed and resource-free. The normative application
  path uses an ephemeral compatibility/configuration certificate and
  phase-wide result validation, fresh binding, reconstruction, successor
  validation, quotient, and measure passes. No later phase runs after an
  earlier fault and no traversal-first partial result becomes authoritative.
- Applied derivations and applied no-successor outcomes retain explicit output
  trace lineage. Semantic fresh identity depends on input-configuration, Rule,
  witness, parent/interface, namespace, and local-key identity—not external
  lineage. Current stochastic draws use already-known input lineage; the
  selected atom then derives output lineage for replay and the next
  application.
- Probability keeps the full tagged applied-atom law, an unrenormalized
  successor-group submeasure, and a separate no-successor submeasure. Scores,
  amplitudes, and arbitrary weights never become probability implicitly;
  intensional pushforwards require measurable closed maps or retain an honest
  unavailable derived view.
- Rollout is repeated family-blind application over continuing
  `(configuration, output-lineage)` fibers. Semantic successor grouping is an
  aggregation view and cannot erase witnesses, mixed continuation, draw
  evidence, or replay paths. One-shot results require no fake trajectory.
- Paper execution covers coupled mobile/field writes, graph birth/deletion,
  multiway diamond merge, stochastic accept/reject and mixed outcomes,
  eventful and event-free continuous flows, PDE/completion relations, and
  one-shot transforms. A refreshed F001–F063 scan found no counterexample
  among all 60 executable families; F010 and F042 remain close non-family
  roles.
- The focused hostile review's substantive challenges were resolved:
  completeness now requires coverage; unknown emptiness does not fabricate
  terminality; application payload and quotient-valued measures are exact;
  continuous endpoints require intrinsic or explicit semantic selection;
  reconstruction is closed and application-private; validation is phase-wide;
  and replay-key derivation is causal.
- Scoped verification found no behavioral change from Stage 1:
  `src/ca` remains tree
  `6e6b34769d60508c03d0a69fad1ede4fef75e217`, `tests` remains
  `02ad081e039a46efbf61855fdeae60abb7bb70ad`, and frozen `goal-2` remains
  `48b6309655ec7c1d3aaa1a0ec5dfb700385e16d1`. Goal 2 handoff and README
  SHA-256 values remain
  `5792ac1810dafdd0be6343e1d03c4b1ab20c48551efd73400fea5a1812a9f192`
  and
  `e063609c7a52d32bd0a4d3bb384cd5da233c34f57a169e2db6cce197c76e0c4d`.
- Markdown fence parity, `git diff --check`, the scoped worktree diff, and
  direct no-dispatch inspection pass. The runtime suite was not rerun because
  this stage changed documentation only; the Stage 1/2 baseline remains
  `102 passed`, and both runtime tree hashes are unchanged.
- Stage 4 (`4-SURFACE`) is now the first incomplete stage. It may assign
  minimal file/public ownership and update the public/reference documents
  without reopening these semantics.
