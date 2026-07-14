# 32-T18-CYCLIC-TAG

Status: **IN PROGRESS — SEMANTIC AUDIT CLOSED; SOURCE, ASSET, AND ARCHITECTURE AUDITS OPEN**

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

- `32-T18-semantic-oracle.py` proves that `(slot,word)` maps losslessly to `Phase(slot) · Data(word)` with exactly one phase marker at the left endpoint.
- On a nonempty event, the generic pipeline reads the marker and first data symbol from one immutable snapshot, replaces that prefix by `Phase(next_slot)`, conditionally inserts the scheduled data block at the old endpoint, and commits both anchored writes atomically.
- On an empty event, `Phase(slot)` has no data head. The explicit Notes clause and semantic oracle give one identity successor with the phase frozen, not T17's zero-successor `InsufficientPrefix`.
- The bounded 71,442-case commuting square finds no counterexample requiring a new UPDATE algebra. The phase marker is a tagged ALPHABET role and invariant, not a family control class.

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

## Semantic Audit

The direct state is `(phase,word)` under an immutable nonempty ordered cycle of append blocks. The tagged encoding

```text
e(phase, a0...am) = Phase(phase) Data(a0)...Data(am)
```

has an explicit inverse on the invariant-valid image. For every binary block of length zero through two, every cycle of one through three block occurrences, every valid phase, and every word through length five, the direct and generic successors agree one event for one event. This covers 399 programs and 71,442 state/program cases:

- 1,134 already-empty identity events with frozen phase;
- 30,132 nonempty events with a nonempty append;
- 40,176 nonempty events with no appended data;
- opaque exact-snapshot source identity, fresh snapshot identity, phase-marker persistence, consumed-head identity, old-suffix order, and fresh-tail lineage.

The same generic `apply_ordered_spans` function independently realizes 1,806 bounded T17 prefix-delete/tail-append cases. T18 changes the prefix write from pure deletion to replacement by the next phase marker; the old-end insertion and one-snapshot atomicity remain the same ordered multi-span UPDATE. A 255-case bounded audit also confirms the Notes multiplicity generalization, in which a removed natural value `n` appends `n` copies of the scheduled block.

The adversarial cases establish:

- equal words at different phases can have different successors, so word-only state and trace-time-derived phase are invalid;
- phase advances on every nonempty event, including false-trigger and successful-extinction events;
- a successful transition to empty is distinct from the subsequent empty identity event, where phase freezes;
- one-block and cycles longer than two use the same semantics and no special execution path;
- same-generation foreign, stale, and successor-reused handles reject through opaque snapshot identity;
- missing, reordered, wrong-phase, wrong-anchor, and fake-append results reject before commit;
- structured program/state serialization retains phase and duplicate slot positions.

The canonical Notes rule `{{1,1},{1,0}}` from a one-black seed passes the frozen `t0..t12` trace. Asset closure must still confirm which direct raster(s) this exact fixture is entitled to reproduce.

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

The broad SimpleProgram responsibilities fit, while their current CA-shaped realization does not:

| Concern | Fit | Finding |
|---|---|---|
| DOMAIN | DIRECT | T18 is discrete `t+1D`; DOMAIN does not mean the phase carrier or queue storage class. |
| CONFIGURATION/support | PRINCIPLED EXTENSION | `simple_programs.md:87-169` fixes a dense slice shape. T18 needs a finite variable-length ordered support with one tagged left-end phase invariant. |
| ALPHABET | PARAMETERIZATION | The value responsibility at `:200-233` generalizes to `Phase(slot) | Data(symbol)`; strict binary and natural-multiplicity data are validators/presets. |
| FRONTIER | PRINCIPLED EXTENSION | Absolute writable coordinates at `:1412-1510` must generalize to the unique old phase/head occurrence pair, or zero data-head sources when empty. |
| NEIGHBORHOOD | PRINCIPLED EXTENSION | Geometric offsets at `:360-731` must generalize to structural endpoint access; all reads still come from one old snapshot. |
| RULE/write | PRINCIPLED EXTENSION | Scalar next-coordinate values at `:1767-1793` must admit two closed ordered span writes computed from `(phase,head)` and immutable program data. |
| UPDATE | PARAMETERIZATION | D039 generic ordered multi-span commit already expresses phase/head prefix replacement plus old-end insertion; no cyclic update or executor is needed. |
| outcome | PARAMETERIZATION | D024's construction-specific empty policy gains an evidenced identity event with frozen phase; T17 `InsufficientPrefix` remains unchanged. |
| trace/encoding | PRINCIPLED EXTENSION | Dense copied slices at `:2124-2199` cannot natively preserve ragged tagged words, event provenance, and zero/nonzero-length distinctions. |

## Current Runtime Fit

`src/ca` is the intended SimplePrograms implementation namespace, but its current Phase-1 components realize only the fixed-lattice preset:

- `alphabets.py` can supply finite data/phase factors, but needs a closed tagged-union schema and cross-factor invariant rather than opaque object cells.
- `loci.py` provides finite rank-0..3 coordinate spaces and mask algebra; ordered occurrence/end-anchor identities are not currently representable by integer proximity alone.
- `frontiers.py:38-80` exposes the `time_slice` preset only. T18 needs a generic structural selector for the unique left marker/head pair.
- `neighborhoods.py:110-549` constructs geometric offset stencils. T18 needs the already-planned ordered endpoint access pattern.
- `rules.py:30,65-78` stores a family string, optional `Any` parameters/callable, and scalar-oriented rule data. T18 needs an immutable serialized cycle table and typed span writes, never a whole-word callback.
- `specs.py:24-82` requires one fixed shape and NumPy-backed `RawEpisode`/`RawBatch`. T18 needs ragged structured snapshots/events before optional experiment packing.
- `rollout.py:40-175` validates fixed shapes, requires `time_slice`, and dispatches by family names. Goal 2 must replace that limitation with component-driven execution, not add a `cyclic_tag` branch.
- `seeds.py:879-939` and `datasets.py:313-334` materialize/stack fixed arrays. A finite tagged word plus explicit initial phase is native state; capacity, padding, masks, and overflow are downstream computation/encoding concerns.
- Existing tests enforce fixed-shape/current-family contracts and contain no cyclic phase, marker invariant, queue-head, remote append, empty-stutter, or ragged serialization case. They must remain passing while generic schemas are added.

## Principles Audit

- Prefer the tagged/product representation and exact invariant over a `CyclicControl` class or executor-local counter.
- Require an explicit inverse and one-step commuting square between `(slot,word)` and `Phase(slot) · Data(word)`.
- Reuse D027/D039 only if old-tail order, phase advancement, empty behavior, provenance, and atomicity all commute without a hidden interpreter.
- Keep immutable rule-cycle data separate from its visible instantaneous focus.
- Reject deriving phase from trace time: arbitrary snapshots, resumptions, and future branching can share a generation number while requiring different schedule positions.

### Decision audit

| Decision | Evidence/proof | Classification | Smallest reusable base | Action |
|---|---|---:|---|---|
| D024 outcomes | explicit empty `CTStep` clause + extinction adversary | 2 | typed construction-specific outcome | add T18 empty identity witness; keep T17 terminal |
| D027 queue geometry | direct remove-one/conditional-tail append + 1,806 shared cases | 2 | anchored prefix/tail schedule | reuse data-tail order |
| D028 epsilon carrier | empty blocks, false triggers, extinction | 2 | `Sigma*` private word/edit carrier | reuse |
| D029 short residue | T17 direct evidence versus T18 empty clause | 2 | typed outcome envelope | keep T17 unchanged |
| D032 visible counter | cyclic schedule focus is required Markov state | 3 | marker/named configuration factor | reuse visible-control representation |
| D039 span commit | 71,442 commuting cases | 3 | generic atomic ordered multi-span replacement | reuse; no UPDATE addition |
| D126 T18 boundary | direct state plus tagged inverse | 3 | `Phase(slot) · Data(word)` preset/invariant | add T18 composition only |

No row is class 4. Source and asset closure may narrow evidence scope but would need a concrete noncommuting counterexample to justify a new execution algebra.

## Detailed Implementation Plan

1. Freeze exhaustive monolith/split/Notes/Index source closure and exact candidate dispositions.
2. Freeze the source-bound asset fixed point and independently decode direct programs, seeds, and trajectories.
3. Preserve the closed 71,442-case direct/tagged proof and adversarial phase, trigger, empty, provenance, and update behavior.
4. Audit `simple_programs.md`, every relevant `src/ca` module/test, principles, D024/D027/D028/D029/D039, T13/T17, and emulation boundaries.
5. Decide the smallest reusable construction, integrate the design ledger, and write the Goal 2 conformance/no-cheating handoff.
6. Obtain independent hostile review and run every oracle, `/tmp`, optimized-mode, Markdown, diff, scope, coverage, and repository-test gate.

## Goal 2 Implementation Stage

### G2-T18 objective

Add cyclic tag systems as a validated visible-control composition over the shared ordered-support runner: one tagged phase marker, one finite data word, one structural head read, and one atomic ordered multi-span commit.

### Dependencies

- the broad branch-free SimpleProgram runner and typed `StepResult`;
- T13/T17 finite ordered support, occurrence identity, ragged snapshots, epsilon-capable private words, and lineage;
- D024 construction-specific empty outcomes;
- D027 prefix-consume/old-end-append validation;
- D032 visible marker/named-factor control representation;
- D039 generic atomic ordered multi-span lowering;
- generic closed finite alphabets, tagged unions, products, structured serialization, and opaque exact-snapshot handles.

### Proposed public composition

```text
Configuration = TaggedWord[PhaseSlot[BlockCount] | Data[Symbol]]
Invariant     = Phase(slot) · Data*
Frontier      = LeftPhaseHeadPair
Neighborhood  = Read(PhaseSlot, FirstData)
Rule          = CyclicBlockTable + BinaryTrigger
Update        = AtomicOrderedSpans
Seed          = (InitialPhase, FiniteWord)
EmptyPolicy   = IdentityWithFrozenPhase
```

These are component roles and validators, not a requirement for one class per line. An equivalent explicit product `(PhaseSlot, FiniteWord)` is acceptable only if it round-trips with the tagged representation and commits both factors atomically.

### Implementation areas

- Generic alphabet/schema module: closed `TaggedUnion(PhaseSlot(n),Data(alphabet))` plus the structural invariant `Phase(slot) · Data*`. Do not use an object cell or pack the word behind one value.
- Ordered configuration module: reuse T17's finite word, occurrence IDs, opaque snapshot identity, ragged trace, and old-end anchor. The phase marker is ordinary visible state and survives with its occurrence identity as its slot label changes.
- Program module: immutable nonempty ordered block cycle, alphabet-closed `Word` blocks including epsilon, explicit trigger policy, and structured slot occurrence order. Duplicate/equal blocks do not erase slot identity. Strict Chapter 3 construction uses binary `TriggerEquals(black)`.
- Generalized preset: represent the Notes natural-value variant with a closed `RepeatScheduledBlockByRemovedNatural` rule form. It is not an `allow_multicolor` flag or callback.
- FRONTIER: select exactly the left phase marker plus first data occurrence when present. On `Phase(slot)` alone, select no data-head source but still invoke the configured UPDATE/outcome policy.
- NEIGHBORHOOD: return the old marker slot, removed value, exact occurrence IDs, and old endpoint. It does not read trace time, mutate/rotate program data, or inspect newborns.
- RULE/result: return two explicit ordered writes—`Replace([0,2),Phase(next))` and `Insert(old_endpoint,conditional_block)`—plus scheduled-slot/trigger witnesses. An epsilon insertion remains an explicit result, not a missing write or table row.
- UPDATE: reuse the generic atomic ordered multi-span committer. Validate exact snapshot ownership, prefix/end anchors, write ordering/nonoverlap, phase successor, source/result coverage, alphabet closure, reused phase ID, consumed head ID, persisted suffix IDs/order, and fresh appended IDs.
- Outcome module: successful extinction is an advanced event with the next phase; a subsequent empty input is an identity event with frozen phase and one successor. T17 `InsufficientPrefix`, T16 `NoMatch`, T15 post-extinction empty rebuilding, halt, error, invalidity, and horizon remain distinct.
- Spec/preset module: `cyclic_tag_system(blocks,initial_phase=0,trigger=black)` returns the ordinary shared components. The catalog/family name never reaches execution.
- Runner: always executes selected component data. No `if cyclic_tag`, phase-from-step, mutable rule rotation, callback, formula fallback, or CA compiler.
- Structured trace/raw boundary: retain tagged ragged states, phase/head/tail events, outcome witnesses, and optional lineage. Length, first-element, growth, substitution checkpoints, mechanical layouts, rule-110 encodings, and rasters are downstream records.
- Tests: add T18 conformance tests and shared tagged-alphabet/ordered-span/outcome/serialization tests; rerun T17 and every existing runtime test.

### Required conformance tests

1. Reproduce every source-bound direct page-95/page-96 program, seed, and audited trajectory checkpoint once asset closure freezes them.
2. Reproduce `{{1,1},{1,0}}` from `Phase(0) · Data(1)` through `t12` and compare direct, tagged, and serialized runs.
3. Phase discriminator: blocks `{1}` and `{0}` map the same word `{1}` to different data successors at slots zero and one.
4. Assert true-trigger append, false-trigger no-append, empty scheduled block, and nonempty block after an old suffix, retaining scheduled-versus-appended witnesses.
5. Assert phase advances on every nonempty event even when nothing is appended; it wraps exactly modulo the number of slot occurrences.
6. Assert successful extinction advances phase once, then `Phase(slot)` produces an identity successor with phase frozen and a distinct empty-stutter witness.
7. Test cycles of one, two, and more than two blocks. One-block repetition is a property, never a halt or executor mode.
8. Test duplicate equal block values in different slots and round-trip their occurrence-distinct phase identity.
9. Test the natural multiplicity rule with removed values zero, one, and greater than one; reject negative/nonintegral multiplicities rather than invoking host `Table` behavior.
10. Prove the tagged encoder has an inverse and the direct/generic square commutes over the bounded 399-program/71,442-state audit.
11. Run T17 prefix-delete/tail-append cases through the same ordered-span committer and prove T17 `InsufficientPrefix` and public program schema do not admit cyclic phase.
12. Reject missing/duplicate/out-of-range markers, phase outside the cycle, empty program cycles, out-of-alphabet blocks/seeds, stale/same-generation-foreign sources, wrong old endpoints, wrong phase successors, incomplete/reordered/colliding writes, reused removed IDs, and fake/freshness-violating children.
13. Verify one event exposes no intermediate headless/old-phase/partially-appended configuration.
14. Round-trip program/state/event data without callbacks, `Any`, mutable iterators, trace-time dependencies, family tags controlling execution, padding, capacity, or renderer state.
15. Verify substitution and ordinary-tag equivalences only through declared encoders/step groupings, and rule-110/Turing/CA material only through explicit realization relations.

### Completion evidence

One shared runner and generic ordered-span UPDATE execute T17 and T18 from typed component data. All direct fixtures and the commuting square pass; phase is present in every native snapshot; empty and extinction witnesses remain distinct; structured traces serialize losslessly; existing tests pass; and no cyclic state class, UPDATE algebra, executor, branch, hidden counter, callback, capacity, sentinel, or compiler fallback exists.

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
