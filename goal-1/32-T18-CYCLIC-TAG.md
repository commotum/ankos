# 32-T18-CYCLIC-TAG

Status: **IN PROGRESS — SOURCE, ASSET, SEMANTIC, AND ARCHITECTURE AUDITS OPEN**

## Current Facts

- T18 is CSV line 19, `Cyclic Tag Systems`. The taxonomy is search vocabulary only; construction facts must come from the monolithic book and source-bound assets.
- The direct Chapter 3 description uses a finite word, removes one leading element per nonempty event, advances through a finite cyclic list of possible append blocks, and appends the current block exactly when the removed element is black (`BOOK:1134-1144`).
- The Notes implementation represents the instantaneous control by a rotated rule list, rotates it on every nonempty event, and explicitly leaves both the schedule and word unchanged once the word is empty (`BOOK:12317-12335`).
- The Notes generalize from two blocks to any nonempty finite cycle and from binary triggering to a removed nonnegative value that repeats the scheduled block that many times (`BOOK:12337-12344`).
- One-block repetition, growth estimates, substitution-system relations, mechanical realization, emulation, universality, random-looking growth, and display rearrangements are properties, relations, realizations, or observers until evidence proves otherwise.
- T17 already supplies finite ordered words, queue-head reads, delete-one/tail-append geometry, epsilon appendants, occurrence provenance, and typed outcomes through the common runner. D027 is an anchored prefix-delete/old-end-insert schedule, while D039 supplies generic atomic ordered multi-span lowering.
- A word alone is not Markov state for T18: the same word at different schedule positions can have different successors. The cyclic focus must be visible configuration state, never executor time or a hidden rotated-rule cursor.
- The current `src/ca` modules remain a fixed-shape CA-shaped implementation of the broader SimplePrograms library. T18 may require modest generic alphabet/configuration/locus/write schemas, but not a `cyclic_tag` rollout branch.

## Updated Assumptions

- The governing runner remains:

  ```text
  active = FRONTIER.select(configuration)
  reads  = NEIGHBORHOOD.read(configuration, active)
  writes = RULE(active, reads)
  next   = UPDATE.apply(configuration, active, writes)
  ```

- Preliminary smallest representation: encode direct state `(slot,word)` losslessly as the invariant-valid tagged word `Phase(slot) · Data(word)`, with exactly one phase marker at the left endpoint.
- Preliminary nonempty event: read the marker and first data symbol from one immutable snapshot; replace that prefix by `Phase(next_slot)`; conditionally insert the scheduled data block at the old endpoint; commit both anchored writes atomically.
- Preliminary empty event: `Phase(slot)` has no data head. The explicit Notes clause appears to define one identity successor with the phase frozen, not T17's zero-successor `InsufficientPrefix`. This remains subject to source/semantic hostile audit.
- No new UPDATE algebra is justified if the direct and tagged steps commute through the existing generic ordered multi-span commit. The phase marker is a tagged alphabet role and invariant, not a family control class.

## Big Picture Objective

Reconstruct cyclic tag systems from primary evidence, prove whether visible cyclic control composes with the existing ordered rewrite machinery, and produce an implementation-ready Goal 2 handoff without hidden time, family dispatch, fixed capacity, or a cyclic-specific executor.

## Catalog Identity

- Stable ID: T18.
- Exact catalog name: Cyclic Tag Systems.
- Entry kind: deterministic finite-word transition construction with visible finite cyclic control.
- Initial vocabulary: cyclic tag system, alternating/cyclic cases, append block, black trigger, first/leftmost element, rotate/rotary element, `CTStep`, `CTEvolveList`, `CTList`, page 95/96, substitution relation, ordinary-tag compiler, rule 110, universality, Kolakoski, growth/randomness, empty word.

## Search Log

Source and asset fixed-point oracles are in progress. No exhaustive count, digest, or zero-remainder claim is made yet.

## Book Excerpts

Pending frozen source closure and exact disposition table.

## Construction Model

- DOMAIN: discrete `t+1D`.
- Configuration/support: a finite ordered word together with one visible focus in a finite cyclic program schedule; equivalently an invariant-valid tagged word beginning with exactly one phase marker.
- ALPHABET: strict binary data plus a finite phase-slot tag; generalized data may use an explicit nonnegative multiplicity carrier.
- Program: immutable nonempty ordered cycle of alphabet-closed finite append words; duplicate slots remain occurrence-distinct.
- FRONTIER: the unique phase/head occurrence pair when data are present; an explicit empty-word policy otherwise.
- NEIGHBORHOOD: old-snapshot read of the phase slot and removed first data value.
- RULE: choose the block by phase alone; the removed value determines whether/how many copies are appended; compute the next phase.
- UPDATE: atomically consume the first data occurrence, preserve the old suffix, append the selected output at the old endpoint, and advance the visible phase. A tagged lowering expresses this as ordered prefix replacement plus old-end insertion.
- Successor: one deterministic successor per evidenced event. Successful extinction and an already-empty identity event must retain distinct witnesses.
- Observers/relations: lengths, leading-symbol series, nested/substitution checkpoints, average growth, randomness claims, mechanical/rule-110 realizations, and compiler relations do not feed execution.

## Current API Fit

Pending exhaustive reread of the relevant `simple_programs.md` sections. The anticipated mismatch is the current fixed-support realization, not the SimpleProgram abstraction.

## Current Runtime Fit

Pending exact `src/ca`/test citations. No runtime edits are authorized in Goal 1.

## Principles Audit

- Prefer the tagged/product representation and exact invariant over a `CyclicControl` class or executor-local counter.
- Require an explicit inverse and one-step commuting square between `(slot,word)` and `Phase(slot) · Data(word)`.
- Reuse D027/D039 only if old-tail order, phase advancement, empty behavior, provenance, and atomicity all commute without a hidden interpreter.
- Keep immutable rule-cycle data separate from its visible instantaneous focus.
- Reject deriving phase from trace time: arbitrary snapshots, resumptions, and future branching can share a generation number while requiring different schedule positions.

## Detailed Implementation Plan

1. Freeze exhaustive monolith/split/Notes/Index source closure and exact candidate dispositions.
2. Freeze the source-bound asset fixed point and independently decode direct programs, seeds, and trajectories.
3. Prove direct/tagged one-step commutation and adversarial phase, trigger, empty, provenance, and update behavior.
4. Audit `simple_programs.md`, every relevant `src/ca` module/test, principles, D024/D027/D028/D029/D039, T13/T17, and emulation boundaries.
5. Decide the smallest reusable construction, integrate the design ledger, and write the Goal 2 conformance/no-cheating handoff.
6. Obtain independent hostile review and run every oracle, `/tmp`, optimized-mode, Markdown, diff, scope, coverage, and repository-test gate.

## Goal 2 Implementation Stage

Pending evidence and semantic closure.

## No-Cheating Checks

- No phase derived from event count, wall-clock time, trace row, executor local, or rotated mutable program object outside configuration state.
- No `cyclic_tag` family rollout, callback, whole-word formula, fixed-capacity queue, padding, sentinel, CA/rule-110 compiler, or opaque packed machine.
- No ordinary T17 table mode that silently consults phase.
- No two-step observable intermediate in which the head is removed but phase or tail append is not yet committed.
- No substitution-system relation or rule-110 realization used as native execution.
- No automatic halt inferred from repetition, bounded length, apparent randomness, or a rendered crop.

## Completion Requirements

- [ ] Exhaustive source/split/Notes/Index/alias audit closes with zero unresolved candidates.
- [ ] Source-bound asset fixed point closes and native rules/seeds/trajectories are decoded.
- [ ] Direct and tagged semantics commute with complete visible phase and exact empty behavior.
- [ ] Smallest reusable base is classified without a new family executor or unjustified UPDATE algebra.
- [ ] Current API/runtime/principles audit and Goal 2 handoff are implementation-ready.
- [ ] Independent hostile review and all oracle/test/Markdown/diff/scope/coverage gates pass.
- [ ] `0-plan.md`, `evidence-index.md`, and `design-ledger.md` are integrated consistently.

## Stage Results

In progress.
