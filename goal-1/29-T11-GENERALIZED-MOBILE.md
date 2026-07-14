# 29-T11-GENERALIZED-MOBILE

Status: **IN PROGRESS — SOURCE, ASSET, AND SEMANTIC CLOSURE ACTIVE**

## Current Facts

- T11 is CSV row 12, `Generalized Mobile Automata`, taxonomy section 11. The taxonomy is search vocabulary only.
- The worktree was clean at stage start. Goal 1 had 27 COMPLETE type stages, 18 PENDING stages, and no reopened stage; T11 was the first incomplete stage.
- `BOOK:916-934` directly names generalized mobile automata, permits any number of active cells, applies the rule to every old active cell, and describes movement, splitting, disappearance, proliferation, and the cellular-automaton limiting case.
- The extracted Notes at `BOOK:12008-12010` give a factored state `{list,nlist}`, a local rule result `{new_source_value,relative_active_positions}`, old-snapshot reads at every active position, source-site color writes, and `Union[Flatten[...]]` construction of the next active set. The extraction has lost the beginning/header of the Note, so provenance and split/reverse coverage must be guarded explicitly.
- T09 and T10 establish the same discrete `t+1D` fixed line, physical left/self/right underlying-value read, visible active role, and atomic snapshot semantics. Neither supplies T11's multiple-source result composition.
- The corrected architecture treats `DOMAIN` as dimensional task/program space and represents the finite active set as a visible configuration factor or tagged ALPHABET role, not hidden executor state or a new top-level state class.
- Goal 1 may edit only `goal-1/`; runtime implementation belongs to the Goal 2 handoff.

## Updated Assumptions

- The strict construction appears to keep a binary fixed integer line and replace the exactly-one-active invariant with a finite active-set invariant; the complete source/asset audit must confirm the strict alphabet and seed.
- Every locus active in the old configuration fires once against the same old value field. Newborn active loci do not fire until the next event.
- A strict rule row appears to return one new value for the old active source and a finite set/list of relative next-active offsets. Movement, splitting, survival, collision, and disappearance are result data, not family branches.
- The Notes implementation appears to make activity collision idempotent by exact set union. It writes colors only at distinct old active sources, so overlapping read neighborhoods and colliding activity destinations do not by themselves create conflicting color writes. This must be proved rather than replaced by the taxonomy's speculative conflict-policy note.
- A transparent cell representation is provisionally `Cell = (Bit,ActiveFlag)` or `Plain(Bit) | Active(Bit)` with any finite number of active tags. A factored `(value_field,active_set)` representation is acceptable only with a checked inverse and one-step commuting proof.
- It remains unresolved whether the strict family permits only `{-1}`, `{+1}`, `{-1,+1}`, and `{}`, whether offset `0` or other finite offset sets occur, whether a canonical rule count/codec is stated, and what exact finite realization/initial-condition conventions the figures use.

## Big Picture Objective

Reconstruct generalized mobile automata from complete primary evidence and determine the smallest honest extension of the shared SimpleProgram axes for multiple simultaneous firing sources, finite activity creation/deletion, and idempotent activity-destination composition. Do not invent write conflicts, collision policies, rule counts, boundaries, halts, or generalized parameters absent from the source.

## Catalog Identity

- Stable ID: `T11`.
- CSV line: 12.
- Catalog name: `Generalized Mobile Automata`.
- Taxonomy section: 11.
- Provisional kind: transition construction extending the T09/T10 mobile source cardinality and result composition.
- Initial vocabulary: `generalized mobile automata`, `generalized mobile automaton`, `active cells`, `any number of cells`, `more than one cell`, `split in two`, `disappear entirely`, `proliferate`, `nlist`, `GMAStep`, `relative positions of active cells`, `Page 76`, mobile/CA interpolation, particles/paths, and every discovered caption/Notes/Index cross-reference.

## Search Log

Initial synchronization searches:

```text
rg -n -i 'generalized mobile automata|generalized mobile automaton|multiple active cells|several active cells|active cells.*split|active cells.*disappear' BOOK
rg -n -C 4 'GMAStep|nlist|new relative positions|Generalized mobile' BOOK
rg -n -C 8 'Generalized Mobile|^## 11\.' ref/notes/CA-Types.md
```

Initial direct candidates are `BOOK:916-934`, `BOOK:12008-12010`, and the actual Index route at `BOOK:21213`. These are not yet the complete candidate universe. The source oracle must record exact queries, union/deduplication, dispositions, governed continuations, split reverse joins, extraction variants, and zero unresolved remainder.

## Book Excerpts

### E01 — defining multiple-active construction

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:916-924`
- Context: Chapter 3, after ordinary/extended mobile behavior and before the page-76 evolution.
- Establishes: the named family, multiple simultaneous active cells, splitting, disappearance, and all-old-active application.

> One can get some insight into the origin of this difference by studying a class of generalized mobile automata, that in a sense interpolate between ordinary mobile automata and cellular automata.
>
> The basic idea of such generalized mobile automata is to allow more than one cell to be active at a time. And the underlying rule is then typically set up so that under certain circumstances an active cell can split in two, or can disappear entirely.
>
> A generalized mobile automaton in which any number of cells can be active at a time. The rule given above is applied to every cell that is active at a particular step. In many cases, the rule specifies just that the active cell should move to the left or right. But in some cases, it specifies that the active cell should split in two, thereby creating an additional active cell.

### E02 — proliferation and CA limiting behavior

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:928-934`
- Context: Chapter 3, page-76 examples and caption.
- Establishes: random-rule behavior observations, unbounded active-count growth in examples, and almost-all-active CA-like operation as behavior rather than native CA identity.

> If one chooses generalized mobile automata at random, most of them will produce simple behavior ... But in a few percent of all cases, the behavior is much more complicated.
>
> Examples of generalized mobile automata with various rules. In case (a), only a limited number of cells ever become active. But in all the other cases shown active cells proliferate forever. In case (d), almost all cells are active, and the system operates essentially like a cellular automaton.

### E03 — executable state, rule result, and simultaneous composition

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:12008-12010`
- Context: Notes implementation immediately before `Turing Machines`; extracted opening/header is missing.
- Establishes: value-field plus active-position-list state; result `new source value + relative next-active positions`; old-snapshot reads for every old active; source-site writes; exact union/deduplication of next active destinations.

> specified by `{list, nlist}`, where `list` gives the values of the cells, and `nlist` is a list of the positions of active cells. The rule can be given by specifying a list of cases such as `{0, 0, 0} -> {1, {1, -1}}`, where in each case the second sublist specifies the new relative positions of active cells.

```text
GMAStep[rules_, {list_, nlist_}] := Module[{a, na},
  {a, na} = Transpose[
    Map[Replace[Take[list, {# - 1, # + 1}], rules] &, nlist]];
  {Fold[ReplacePart[#1, Last[#2], First[#2]] &,
        list, Transpose[{nlist, a}]],
   Union[Flatten[nlist + na]]}]
```

Further excerpt groups remain pending source closure.

## Construction Model

Provisional source-faithful factorization:

```text
configuration = (value_field : Z -> Bit,
                 active_set : FiniteSet[Z])

active = sorted(active_set)
reads[p] = (value_field[p-1], value_field[p], value_field[p+1])
(new_value[p], offsets[p]) = table[reads[p]]

next_values = value_field with every p in active_set assigned new_value[p]
next_active = union { p + d | p in active_set, d in offsets[p] }

next = (next_values, next_active)
```

All reads and results are derived from the old configuration. Old active sources are distinct, so strict color-write targets are distinct. Activity destinations may coincide; the executable definition applies exact set union. An empty active set is provisionally a valid quiescent configuration, but the source/outcome audit must establish whether native stepping stutters, halts, or is simply a total fixed point under `GMAStep`.

A transparent tagged/product lowering is:

```text
Cell = (Bit, ActiveFlag)
encode(values,A)[x] = (values[x], x in A)
```

The inverse projects the bit field and finite set of flagged positions. The semantic oracle must prove this mapping and one-step commutation, including split, disappear, destination collision, old-source/new-destination overlap, and empty-frontier cases.

## Current API Fit

Pending complete re-read and exact citations. Expected pressure points are multi-source FRONTIER selection, typed factor writes, per-result activity-set proposals, and UPDATE composition by source assignments plus finite-set union. The current CA-shaped writable-coordinate frontier and scalar RULE return are hypotheses to audit, not boundaries of the SimpleProgram abstraction.

## Current Runtime Fit

Pending complete re-read of `src/ca` and relevant tests. No current family-specific rollout may be reused as a semantic shortcut. Existing dense-array, time-slice, ordered-offset, old-snapshot, and atomic parallel behavior must be separated into reusable responsibilities.

## Principles Audit

- Principles 0-4 require evidence-first typed composition rather than a `generalized_mobile` branch or unrestricted rule callback.
- Principle 5 requires the complete active set in configuration; it may be a tagged/product ALPHABET role and need not be a separate top-level control class.
- Principles 6-9 require discrete `t+1D`, fixed-line support, values, activity, finite realization, and display marks to remain distinct.
- Principle 11 keeps the evidenced all-old-active schedule and union composition in native semantics; a solver/conflict policy cannot be invented or extracted away.
- Principles 13-16 require collision, split, disappearance, source/destination overlap, empty activity, and representation commutation adversaries.

Smallest provisional model: reuse the T09 physical read and tagged active role, broaden exactly-one to finite activity, return a closed `(new_source_value,FiniteOffsetSet)` result, and compose all source results atomically using distinct source assignments plus exact finite-set union. Whether this is a named preset of generic factor-update composition or needs a new UPDATE-axis implementation remains pending the complete audit.

Rejected in advance: a T11 state class, family executor, sequential/in-place firing, last-writer-wins, arbitrary collision callback, CA compilation as native identity, multiplicity-preserving activity without evidence, hidden active list, forced nonempty activity, fake finite capacity, or taxonomy-derived write policy.

## Detailed Implementation Plan

1. Close the exact canonical source query union, candidate partition, continuations, Index, split reverse coverage, and extraction defects in `goal-1/29-T11-source-oracle.py`.
2. Close every governed physical asset and relation/control image with hashes and reverse references in `goal-1/29-T11-asset-oracle.py`.
3. Reconstruct strict rule/result/seed/step/empty-frontier semantics and variants before comparing architecture.
4. Re-read `simple_programs.md`, `src/ca`, tests, T09/T10/T12, and D009-D014/D122 from current files.
5. Build a dependency-free fail-closed semantic oracle covering source examples, exact composition, representation commutation, and adversarial collisions.
6. Write the implementation-ready Goal 2 handoff, decision record, no-cheating checks, and dependent-stage audit.
7. Run independent hostile review, all oracles from required working directories, optimized-mode guards, Markdown/diff/coverage checks, and repository tests.
8. Only then mark T11 COMPLETE and reintegrate `0-plan.md`, `evidence-index.md`, and `design-ledger.md`.

## Goal 2 Implementation Stage

Pending evidence closure. The handoff must target shared configuration/ALPHABET/FRONTIER/NEIGHBORHOOD/RULE/UPDATE components and run T09/T10/T11/T12 through the same branch-free runner. It must specify structural serialization, exact identity, migration, invalidity/outcome behavior, and adversarial conformance without a T11 family field.

## No-Cheating Checks

- No `generalized_mobile` executor, family switch, callback rule, or hidden active-set cache.
- No sequential firing or observer-visible intermediate state.
- No arbitrary last/first-writer conflict policy; use only source-evidenced composition.
- No destination multiplicity unless the source makes multiplicity semantic; `Union` currently indicates a set.
- No CA compiler, raster, activity plot, or rule glyph treated as native configuration/rule identity.
- No fixed tensor edge, crop, padding, or initial display width promoted to native boundary/support.
- No exactly-one invariant retained from T09, and no nonempty invariant imposed without evidence.
- No T10 neighbor-color writes imported into T11 unless direct evidence establishes them.
- No new semantic class merely because activity and values are separate roles in the Notes representation.

## Completion Requirements

- [ ] Every direct/alias/caption/Notes/Index/cross-reference candidate is dispositioned with zero unresolved remainder.
- [ ] Every governed physical asset is pinned or explicitly excluded with exact provenance and hashes.
- [ ] Strict state, DOMAIN/support, ALPHABET/activity, frontier, read, result, schedule, composition, successor, boundary, seed, variant, relation, observer, rule-count, and identity semantics are resolved or explicitly source-underdetermined.
- [ ] The tagged/factored representation has an explicit inverse and exhaustive or otherwise complete one-step commuting proof.
- [ ] Split, disappear, activity collision, source/destination overlap, empty-frontier, outside-preservation, and atomic-failure adversaries pass.
- [ ] Current API/runtime/tests and dependent decisions are audited from actual files.
- [ ] Goal 2 files/dependencies/APIs/tests/migration/no-cheating gates are implementation-ready without runtime implementation.
- [ ] Independent hostile review, source/asset/semantic, optimized-mode, Markdown, diff, coverage, and repository-test gates pass.
- [ ] Global plan, evidence index, design ledger, and any dependent stages are current.

## Re-Integration Audit

Pending completion. T09/T10/T12 remain closed unless T11 supplies a concrete contradiction. The main open question is whether exact set-union activity composition is already a generic typed factor combiner or justifies a new closed UPDATE-axis policy; it cannot justify a separate runner.

## Stage Results

IN PROGRESS. Stage scaffolded from the current loop after a clean sync and a full reread of `principles.md`. Three independent audits are active: source closure, physical assets, and semantic/runtime architecture. Next work is to reconcile their candidate universes and freeze exact oracles before making a completion claim.
