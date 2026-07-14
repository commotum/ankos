# 28-T10-EXTENDED-MOBILE

Status: **IN PROGRESS — SOURCE/ASSET/ARCHITECTURE AUDIT ACTIVE**

## Current Facts

- Exact catalog row: T10, CSV line 11, `Extended Mobile Automata`; taxonomy section 10 at `ref/notes/CA-Types.md:239-265` is search vocabulary only, not book evidence.
- T09 is already reclosed as a fixed ordered one-dimensional field with a visible unique `Plain(bit) | Active(bit)` tag, unique firing-source frontier, physical left/self/right read, compact native table, atomic source write plus active-tag movement, and no family executor.
- The strict Chapter 3 description at `BOOK:882` says the extension permits the active cell and both immediate neighbors to be updated at each step and gives `4,294,967,296` possible rules.
- The adjacent Notes at `BOOK:11982-11993` present a rule result shaped as a three-value replacement block plus displacement and replace the old three-cell block atomically before carrying the active position.
- These lines make T10 a strong parameterization/restriction hypothesis over the T09 axes: the read window and unique active control appear unchanged while the typed write scope widens. This remains a hypothesis until exhaustive source, asset, boundary, variant, and architecture audits close.
- Goal 1 changes only `goal-1/`; runtime, tests, `principles.md`, and `simple_programs.md` remain Goal 2 work.

## Updated Assumptions

- Preserve the branch-free SimpleProgram runner:

```text
active = FRONTIER.select(configuration)
reads  = NEIGHBORHOOD.read(configuration, active)
writes = RULE(active, reads)
next   = UPDATE.apply(configuration, active, writes)
```

- DOMAIN means the task/program support/topology, not the write window. T10 is provisionally the same fixed `t+1D` line as T09.
- ALPHABET/control visibility provisionally reuse T09's transparent tagged representation and exactly-one-active invariant; a wider write result does not itself justify a new state class.
- RULE writes must retain source-relative target identity and complete replacement values. UPDATE must commit them from one old snapshot together with active-tag relocation; sequential mutation order, hidden buffering, and a T10 executor are forbidden unless source evidence requires them.
- The displayed cardinality must be reconstructed from the exact input/result spaces, not accepted from the catalog summary.
- Page images, compressed histories, motion plots, causal networks, and emulations are evidence/observers/relations, not native state or execution inputs.

## Big Picture Objective

Exhaustively reconstruct extended mobile automata from the book and determine whether they are exactly a T09 parameterization with a wider typed replacement block, or whether some evidenced variant requires a genuinely different FRONTIER, NEIGHBORHOOD, RULE-write, UPDATE, state, or successor algebra. Produce the smallest implementation-ready Goal 2 handoff without family dispatch, opaque packing, fake capacity, callbacks, hidden state, or invented collision/boundary behavior.

## Catalog Identity

- Stable ID: T10.
- Exact name: Extended Mobile Automata.
- Taxonomy section: 10, `ref/notes/CA-Types.md:239-265`.
- Entry kind: unresolved pending evidence; current hypothesis is a fixed-support, unique-active controlled transition parameterization of T09.
- Initial search vocabulary: extended mobile automaton/automata, extension of mobile rules, page 73, active cell and immediate neighbors updated, three-cell/block replacement, multiple cells updated, colors of neighboring cells updated, `4,294,967,296`, `2^32`, `{new_left,new_self,new_right}`, displacement/move, `MAStep`, compressed evolution/form, active dot/head, wider write scope, generalized mobile automata boundary, Turing/mobile/CA/substitution emulations, reversible/2D/network variants, Notes, Index, captions, and rule figures.

## Search Log

IN PROGRESS. Every query, candidate partition, governed continuation, split/Index route, asset, false positive, and unresolved item will be frozen here and in scoped oracles before completion.

## Book Excerpts

IN PROGRESS. Only complete construction-relevant excerpts read in context will be retained with canonical line provenance.

## Construction Model

IN PROGRESS. The audit will resolve:

- native configuration, support/topology, ALPHABET, and exactly-one-active invariant;
- firing/source frontier and physical read order;
- native rule table input and result space;
- source-relative replacement targets and active movement;
- atomic commit, target distinctness, destination-label preservation, and any overlap/order issue;
- rule cardinality and compact structural identity;
- boundary/defined-input scope, initial conditions, traces, observables, variants, and emulation relations; and
- exact reuse versus a concrete counterexample requiring a new execution-axis capability.

## Current API Fit

IN PROGRESS. Map each construction role to exact `simple_programs.md` definitions using `DIRECT`, `PARAMETERIZATION`, `PRINCIPLED EXTENSION`, `SEMANTIC MISMATCH`, `NOT APPLICABLE`, or `UNRESOLVED` only after the source model closes.

## Current Runtime Fit

IN PROGRESS. Re-read relevant `src/ca` modules and tests, preserve actual behavior only where construction-faithful, and identify Goal 2 migration without runtime edits in Goal 1.

## Principles Audit

IN PROGRESS. The leading smallest-model hypothesis is T09 plus a fixed three-target source-relative replacement descriptor. It will be rejected if any evidenced transition cannot be expressed faithfully with the same visible state, source frontier, read, atomic write composition, and movement semantics.

## Detailed Implementation Plan

1. Close a reproducible source universe across direct terminology, descriptive phrases, rule counts, captions, Notes code, Index routes, aliases, variants, and cross-references.
2. Close the governed visual/code asset universe with exact physical identity, monolith/split references or explicit absences, dimensions, hashes, semantic classes, and stop rules.
3. Reconstruct the strict construction and all evidenced variants before comparing abstractions.
4. Audit T09/T12/T01 decisions, `simple_programs.md`, `src/ca`, tests, datasets, and migration responsibilities from current files.
5. Specify the minimal Goal 2 API, identities, validation, serialization, lowering, acceptance fixtures, and no-cheating checks.
6. Run source/asset/semantic oracles, independent hostile review, repository tests, Markdown/coverage/diff/scope gates, and integrate global ledgers only after every requirement is proved.

## Goal 2 Implementation Stage

IN PROGRESS. The final handoff will name exact dependencies, shared primitives, files, migration, book fixtures, adversarial conformance tests, completion evidence, and effects on later T11/T25/network stages.

## No-Cheating Checks

- No T10/extended-mobile rollout branch, family flag, callback, opaque whole-state value, hidden active position, or sequential in-place block mutation.
- No arbitrary CA table substituted for the compact native extended-mobile rule table.
- No write-window padding or finite tensor boundary treated as native infinite-line semantics.
- No active tag lost when the destination lies inside the written block; complete tagged labels and atomic movement must preserve exactly one active cell.
- No generalized-mobile collision policy invented from a unique-active T10 example.
- No raster, compressed trace, causal graph, or emulation relation promoted into program state or identity.
- No new semantic class without a concrete evidenced transition that T09's generic axes cannot express faithfully.

## Completion Requirements

- [ ] Every declared source candidate, governed continuation, split/Index route, and asset is dispositioned under reproducible protocols with zero silent remainder.
- [ ] Every retained excerpt/asset has exact provenance and construction claims remain separate from behavior, observation, emulation, and boundary claims.
- [ ] The construction model proves the exact state/read/write/move/update/cardinality semantics and closes all variants or explicit source limitations.
- [ ] API/runtime fit and a dependency-aware Goal 2 handoff are implementation-ready with adversarial atomicity, tag, boundary, identity, and no-cheating cases.
- [ ] Re-integration answers all ten loop questions and records any reopened stage or changed dependency.
- [ ] Independent hostile review, all scoped oracles, 45-row coverage, Markdown/diff/scope gates, and repository tests pass.

## Stage Results

IN PROGRESS.
