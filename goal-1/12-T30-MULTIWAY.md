# 12-T30-MULTIWAY

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T30, CSV line 31, `Multiway Systems`; taxonomy seed `ref/notes/CA-Types.md:814-835`. The taxonomy's proposed branch policies, custom state, pruning, memoization, and growth controls are hypotheses, not evidence.
- The strict main/Notes construction evolves a finite set of distinct finite words. It is not one selected path and not a bag of derivation occurrences.
- A literal program is a finite relation of nonempty left words to epsilon-capable right words. The same left side may have multiple right sides; rule order is nonsemantic.
- One event considers every exact occurrence of every left side in every parent word in the frozen old layer, including overlapping occurrences.
- Each match independently performs exactly one interval splice. Matches are alternatives; no child performs multiple matches simultaneously, and newborn words do not fire in their birth layer.
- The successor exact-word-unions every generated child. Equal children produced by different rules, spans, or parents become one semantic word for the next event.
- Parents with no applicable match contribute nothing. They do not persist unless an explicit identity rule regenerates them.
- Epsilon is a valid word/state and differs from the empty layer. A layer containing only epsilon advances to the empty layer when no empty-LHS rule is allowed.
- The supplied reference `MWStep` maps the empty layer to itself. `Quiescent(EmptyLayer)` with an event-free self-successor is an architectural label for that exact stutter, not a book-named halt.
- A nonempty layer whose branches all die returns `Advanced(empty_layer)` once. This is not T16 `Terminal(NoMatch)`.
- Multiway micro-branching therefore lifts to one deterministic set-valued macro successor. `DistinctBranchMerge` is a new update algebra, not a branch-policy option.
- Raw events must retain every `(parent,clause,span,child)` rewrite witness and every dead-end parent. Witness multiplicity never weights or duplicates successor state.
- Book diagrams deliberately record only whether a source leads to a target, not how many applications do so. A simple state graph and a witness multigraph are distinct trace projections.
- The same word can reappear at many time layers and must fire again. A compressed graph with one node per distinct word is downstream; global visited-state suppression changes evolution.
- The exact page-206 deletion preset visibly produces epsilon, and its executable trajectory distinguishes epsilon from empty-layer extinction.
- An exact official-CDF trajectory has four derivation witnesses but only three children at one event, directly proving cross-parent target merging.
- T30 can reuse T13's finite word carrier and T16's literal match/span/splice semantics. It cannot reuse T16's first-applicable selector, ordered clause priority, no-match terminal outcome, or single-successor commit.
- T29 graph topology is not T30 state. The network of state-to-state arrows is a trace representation built from word layers, not a mutable graph advanced by the T29 port rewrite.
- Multiway tag code preserves duplicate derivations instead of applying `Union`. It is a distinct multiplicity-sensitive variant/source boundary and cannot silently inherit the base merge law.
- Cyclic, multidimensional/network, tag, arithmetic, nondeterministic Turing, game, term-pattern, and Chapter 9 causal-event multiway systems require separately typed carriers/matchers even when they may reuse branch merging.
- No canonical rule numbering, finite exhaustive count, or random-rule distribution is supplied. No pruning, beam width, maximum state count, or maximum word length is native.
- Current runtime support is fixed dense coordinate arrays with scalar family-dispatched updates. It has no word-set state, all-match source, branch result bundle, exact deduplication, dead-end accounting, or multiway trace.

## Updated Assumptions

- `Word = tuple[Symbol,...]` admits epsilon. `MultiwayLayer = FiniteSet[Word]` is exact structural set equality: layer order and multiplicity are immaterial, symbol and word order are material.
- `{epsilon} != empty_layer`. The empty program and empty layer are valid finite data unless later direct evidence narrows them.
- Program clauses are a mathematical relation, not an ordered rewrite list. Exact duplicate pairs should canonicalize or reject at validation; they cannot create branch weight.
- Empty left sides are invalid because they introduce insertion-position conventions not evidenced by `StringPosition` examples. Empty right sides are native deletion.
- All matches are enumerated on each old parent before any child exists. Every match carries clause identity, exact old interval, and snapshot identity.
- A child is `prefix + rhs + suffix` for one match only. Overlapping matches produce separate children.
- Exact child equality alone merges base branches. Length, symbol counts, anagram sorting, symmetry, group equivalence, normal form, or graph layout never defines base state identity.
- A merged word fires once in the next layer while retaining all inbound derivations only in the event. It has no chosen parent occurrence or persistent ancestry.
- A finite layer has one semantic successor even when it contains many word-level alternatives. The trace may expose the branch relation without turning executor behavior stochastic.
- Resource exhaustion must not publish a pruned successor as exact. It is a distinct failure/stop diagnostic.
- Counts, differences, accumulated languages, first-seen depth, paths, confluence, normal forms, causal graphs, compressed spacetime networks, and rendering are downstream.

## Big Picture Objective

Reconstruct base multiway systems as exact finite word-set evolution: closed literal relation, every overlapping old match, one independent splice per branch, exact target merging, dead-end dropping, epsilon/empty-layer behavior, recurrent-layer semantics, lossless derivation provenance, and derived graph views. Determine the smallest honest reuse of T13/T16 plus the required branch-merge update while excluding repeated deterministic rollouts, callbacks, random branch choice, global visited suppression, pruning, witness-weighted state, family dispatch, and opaque graph packing.

## Catalog Identity

- Stable ID: T30.
- Exact name: Multiway Systems.
- CSV provenance: `ref/notes/CA-Types.csv:31`; taxonomy provenance: `ref/notes/CA-Types.md:814-835`.
- Canonical section: Chapter 5 `Multiway Systems`, `BOOK:2494-2566`. T29 ends at `2492` and T31 begins at `2568`.
- Native Notes core: `BOOK:13921-13961`; broader native/variant Notes neighborhood extends through `14025`.
- Entry kind: deterministic set-lifted evolution generated by all possible single literal replacements.
- Search vocabulary: multiway system(s), all possible replacement(s), possible/distinct states/sequences, branch/branching, merge/merging, state graph/network in time, semi-Thue/Thue, string rewrite, confluence/Church-Rosser/normal form, deletion/empty string, `MWStep`/`MWStep1`/`StringPosition`/`StringReplacePart`/`Union`, cyclic/multidimensional/tag/arithmetic/nondeterministic variants, causal network, derivation/path, and growth/count/period.

## Search Log

1. Verified CSV line 31 and read `ref/notes/CA-Types.md:814-835`; its API suggestions remain hypotheses.
2. Read the complete main core `BOOK:2494-2566` and inspected page-219 through page-224 local figures. Detailed image rule recovery is still being cross-checked.
3. Direct `multiway system(s)` search found 267 occurrences on 182 lines: 199/134 before the Index and 68/48 in it. The main core contributes 20/13; the native Notes neighborhood contributes 23/15.
4. Conservative direct/alias/confluence vocabulary found 352 occurrences on 218 lines: 247/156 before the Index and 105/62 in the actual Index.
5. The implementation-symbol sweep found 20 occurrences on 18 lines: 10/9 in native Notes plus 3/3 in the multiway-tag neighborhood. All candidates are under disposition.
6. Read `BOOK:13921-13961` and verified that `MWStep1` enumerates every overlapping literal position and performs one splice, while `MWStep` maps over parents/rules and exact-`Union`s children.
7. Verified exact deletion and merge trajectories against the official Chapter 5 CDF and inspected the official general-properties note to repair one local OCR-damaged sorted-system rule.
8. Followed `BOOK:16511-16556` for compressed state graphs, derivation paths, confluence/normal forms, and causal-network relations.
9. Current remaining work: complete figure/table recovery, split/actual-Index disposition, histories/variants, full adversarial oracle audit, and repository/global integration.

## Book Excerpts

Canonical `BOOK` means `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`. The final excerpt grouping remains open until the full search closes.

### E01 — Collections of possible states

- Provenance: `BOOK:2494-2510`, page-219.
- Fact: each state is a word; every possible replacement is applied, and all distinct resulting words are kept.

### E02 — Growth, deletion, and epsilon

- Provenance: `BOOK:2512-2542`, pages 220-223.
- Fact: state counts may grow uniformly, fluctuate, or explode. A three-rule example deletes blocks and visibly includes zero-element sequences.

### E03 — Recurrent states and compressed state graph

- Provenance: `BOOK:2544-2566`, page-224.
- Fact: a word can occur at multiple steps and always has the same outgoing behavior. One may display it once in a compressed network, but recurrence in the layered evolution remains real.

### E04 — Exact all-match implementation

- Provenance: `BOOK:13921-13937`.
- Fact: `MWStep1` finds every literal occurrence and splices one occurrence per result; `MWStep` applies this to every rule and parent, then `Union` merges equal words.

### E05 — Deletion program and exact trajectory

- Provenance: `BOOK:13950-13956`, official CDF.
- Fact: `{AB->epsilon, ABA->ABBAB, ABABBB->AAAAABA}` on `ABABAB` produces exact word sets and reaches epsilon. Deletion is a valid result; epsilon and the empty layer differ.

### E06 — Diagram multiplicity projection

- Provenance: `BOOK:13959`.
- Fact: pictures show only existence of a source-target relation, not the number of matching applications. Lossless event witnesses precede simple-edge projection.

### E07 — Sorted-word special representation

- Provenance: `BOOK:13963-13968`, repaired against the official page-937 note.
- Fact: for a special order-insensitive rule profile, words can be lowered to symbol-count vectors. This requires a proved invariant and is not general anagram equality.

### E08 — Multiway variants

- Provenance: `BOOK:13989-14025`.
- Fact: pattern-variable, cyclic, multidimensional/network, tag, arithmetic/complex, nondeterministic-machine, and game variants change carrier, matching, or branch multiplicity and require separate audits.

### E09 — Compressed spacetime graph and confluence

- Provenance: `BOOK:16511-16556`.
- Fact: one node per distinct word gives a compressed graph; paths, causal networks, confluence, normal forms, and Church-Rosser properties are analyses of the rewrite relation.

## Construction Model

Evidence closure is in progress. The current candidate contract is:

```text
Word = FiniteTuple[Symbol]                 # epsilon allowed
MultiwayLayer = FiniteSet[Word]

LiteralClause = {
    lhs: NonEmptyWord,
    rhs: Word
}

MultiwayLiteralProgram = FiniteRelation[LiteralClause]

AllApplicableLiteralMatches(old_layer, program)
  -> every (parent, clause, start, stop), overlaps included

ReplaceInterval(match, rhs)
  -> prefix(parent,start) + rhs + suffix(parent,stop)

DistinctBranchMerge
  -> exact set union of all one-match children
```

The full contract, outcomes, traces, exact presets, adversarial tests, variants, API/runtime fit, principles audit, and Goal 2 implementation stage will be frozen after the remaining figure/search audit.

## Current API Fit

Initial conclusion: T13 words and T16 literal span/splice values are direct reuse; fixed dense state, coordinate frontiers, ordered first-match priority, one-word outcomes, no-match termination, scalar results, family rollout, and fixed-shape traces are semantic mismatches.

## Current Runtime Fit

Initial audit finds no native set-of-words state, all-match selector, exact child merge, dead-end accounting, derivation witness bundle, recurrent layered trace, or compressed-graph projection. `FORMULAIC` would hide the construction and is rejected.

## Principles Audit

Pending full evidence closure. Provisional rejections include repeated T16 rollouts, rule priority, simultaneous multi-splice children, random path choice, retained path copies, global visited suppression, preserve-no-match fallback, implicit old-layer accumulation, length/count/anagram quotient, witness weighting, pruning/caps, and whole-layer scalar/tensor/graph packing.

## Detailed Implementation Plan

1. Close all direct, alias, figure, Notes, program, actual Index, split, history, confluence, variant, graph, seed, count, and relation candidates.
2. Freeze word/layer equality, clause validation, overlapping match enumeration, one-splice branch construction, exact target merge, dead ends, epsilon, empty layer, recurrence, outcomes, and trace.
3. Recover every executable rule/trajectory/count and independently derive adversarial branch/merge oracles.
4. Compare T13/T16/T29 and every current API/runtime responsibility; decide the exact new update boundary.
5. Audit no-cheating constraints, resource behavior, variants, lowerings, batching, and graph visualization.
6. Write the complete Goal 2 implementation/conformance stage and reintegrate every global ledger.

## Goal 2 Implementation Stage

Pending evidence closure. It will specify closed word-set/program/match/result/update/outcome/trace APIs, shared T13/T16 dependencies, exact presets, validation, migrations, ragged batching, graph views, adversarial conformance tests, and forbidden-fallback audits without a multiway rollout branch.

## No-Cheating Checks

- No repeated deterministic-path executor, random branch choice, branch callback, `successors(state)` callback, or named multiway rollout.
- No one-path selection, rule priority, first-match selection, simultaneous multi-match splice, in-step newborn firing, or no-match parent preservation.
- No derivation-copy multiplicity in base state, witness weighting, global visited suppression, or old-layer accumulation without an identity rule.
- No epsilon/empty-layer collapse, terminal reinterpretation, fake boundary, fixed word/state capacity, pruning, beam search, or silent resource truncation.
- No length/count/anagram/symmetry/group/normal-form quotient as base equality.
- No whole layer/state graph packed in a scalar, tensor, coordinate lattice, T29 port graph, or host graph engine.

## Completion Requirements

- [ ] All names, aliases, figures, Notes/programs, actual Index entries, splits, history, variants, observers, and relations resolved with zero silent remainder.
- [ ] Native word-set state, program, all-match source/read/result/update, exact merge, dead ends, epsilon/empty layer, recurrence, outcomes, and traces reconstructed.
- [ ] Exact canonical trajectories and adversarial overlap/merge/recurrent/dead/identity/provenance invariants specified.
- [ ] Current API/runtime/principles fit and T13/T16/T29 reuse/divergence explicit.
- [ ] Goal 2 implementation/conformance handoff and global reintegration complete.

## Stage Results

In progress. Core prose and executable Notes already establish all-overlapping-match, one-splice-per-branch, exact-word union, dead-parent dropping, deletion, epsilon, and the layered-versus-compressed-graph distinction. The remaining figure/index/variant audit must close before the semantic contract is marked complete.
