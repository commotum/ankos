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

### Exact word-set carrier

```text
Alphabet = FiniteNonEmptySet[Symbol]
Word = FiniteTuple[Symbol]                 # epsilon allowed
MultiwayLayer = FrozenSet[Word]            # finite, exact, unweighted

LiteralClause = {
    lhs: NonEmptyWord,
    rhs: Word
}

MultiwayLiteralProgram = {
    alphabet,
    clauses: FiniteSet[LiteralClause]
}
```

Every word, clause side, and seed is alphabet-closed. Word order is semantic; layer enumeration is not. Equal word values occur at most once in a layer. No parent occurrence ID, branch weight, active control, derivation history, graph node, or first-seen depth is needed to advance.

The empty word and empty layer are distinct:

```text
epsilon = ()
{epsilon} = one live state whose word has length zero
empty_layer = no live states
```

The finite program is a relation:

- `lhs` is nonempty;
- `rhs` may be epsilon;
- several clauses may share one `lhs` if their `rhs` differs;
- clause order is nonsemantic;
- an exact duplicate pair is invalid at sequence/JSON construction and impossible in the normalized set value;
- there is no missing-rule fallback, default identity, priority, numeric rule code, or implicit reverse rule.

Empty `lhs` is rejected because it would require an insertion-position convention absent from the base sources. A finite empty program is valid and causes every nonempty seed state to die at its first event.

### All applicable old matches

Source selection is intrinsically program-coupled:

```text
AllApplicableLiteralMatches.select(old_layer, program)
  = {
      Match(
        snapshot_id,
        parent_word,
        clause,
        start,
        stop = start + len(clause.lhs)
      )
      for every parent_word in old_layer
      for every clause in program.clauses
      for every exact occurrence of clause.lhs in parent_word
    }
```

Occurrences include overlaps. For parent `AAA` and `AA -> B`, starts 0 and 1 both fire. Parent enumeration, clause enumeration, and match enumeration order cannot change the match set or successor.

`MatchedWord` validates:

- the source belongs to the declared snapshot/layer;
- interval bounds are exact and in range;
- the old slice equals the selected `lhs`;
- clause/alphabet/program identity is authoritative;
- the parent has not been packed or canonicalized by an observer.

This reuses T16's exact literal matching and matched-span read meaning. It explicitly does not reuse `FirstApplicableMatch`, clause priority, or leftmost-only selection.

### One splice per branch

Each match independently yields:

```text
BranchIntervalReplacement = {
    source: Match,
    replacement: clause.rhs
}

child(match) =
    parent_word[:start]
    + replacement
    + parent_word[stop:]
```

One child contains one splice. Two overlapping or disjoint matches are alternatives, not a simultaneous edit set. A child is not rescanned until the next layer. Thus `A -> AA` sends `{A} -> {AA} -> {AAA}`, not directly to an unbounded result.

### The eighth update law: exact branch merge

`DistinctBranchMerge` commits one old layer:

1. validate that the supplied match/result set is exactly every applicable match of every clause in every old parent;
2. apply one interval splice per match against the frozen parent word;
3. group all results by exact child word;
4. make the successor the set of group keys;
5. record every parent with zero matches as a dead end;
6. attach every rewrite witness to its child's derivation group;
7. never carry an old parent merely because it existed in the previous layer.

```text
ParallelLiteralMultiway =
    STATE: MultiwayLayer
    SOURCE: AllApplicableLiteralMatches
    READ: MatchedWord
    RULE: MultiwayLiteralProgram
    RESULT: BranchIntervalReplacement
    UPDATE: DistinctBranchMerge
```

This is an eighth public update sibling after T29. T16's one-splice operation can be a private child-construction kernel, but T16 selects exactly one match and returns one word, whereas T30 covers all matches and exact-unions their children. Repeatedly invoking T16 with altered priorities cannot reproduce a single atomic multiway event without duplicating applicability, merge, dead-end, and snapshot semantics.

The macro transition is deterministic:

```text
step: MultiwayLayer -> MultiwayLayer
```

Word-level alternatives do not imply random executor choice or a list of nondeterministic API returns. The one semantic successor is the complete set of alternatives.

### Outcome semantics

For every nonempty old layer:

```text
Advanced(
    state = exact_set_of_children,
    changed = (old_layer != exact_set_of_children),
    event = MultiwayRewriteEvent(...)
)
```

This includes an all-dead event whose successor is `empty_layer`. An identity clause can produce an eventful `Advanced(changed=false)`. A recurrent layer or two-cycle continues to advance; no fixed/cycle stop is intrinsic.

The executable reference maps `empty_layer` to itself with no witnesses. The architecture labels this:

```text
Quiescent(EmptyLayer, state=empty_layer)
reference_successor = empty_layer
```

This label distinguishes event-free empty-set stutter from the preceding all-dead rewrite event. It is not a claim that the book names a halt. Horizon, fixed/cycle observation, resource exhaustion, cancellation, invalidity, and error remain separate.

### Lossless trace and graph projections

`MultiwayRewriteEvent` records:

```text
snapshot_id
old_layer
rewrite_witnesses {
    parent_word
    clause
    start
    stop
    matched_lhs
    replacement_rhs
    child_word
}
dead_end_parents
child_to_witness_set
next_layer
```

Exact reconstruction invariants are:

- witnesses equal all and only applicable old matches;
- every witness child equals the one-splice formula;
- `next_layer` equals the exact set of witness children;
- every next word has at least one witness;
- dead ends equal old parents with no witness;
- witness multiplicity does not change `next_layer`.

From the raw layered trace one may derive:

- a layered diagram with one occurrence of a word per time layer;
- a simple layer edge relation `(parent,child)` with duplicate witnesses collapsed;
- a derivation multigraph retaining clause/span witnesses;
- a compressed graph with one node per exact word ever seen;
- first-seen depth, accumulated language, path sets, causal networks, state/edge counts, growth differences, confluence, normal forms, and renderings.

The same exact word can belong to many layers. Compressed-node reuse never suppresses its later firing. A merged child has all inbound witnesses but no chosen semantic parent or persistent occurrence identity.

## Exact Book Presets and Oracles

### Page-219 simple nested system

For program `{A->A, A->AA}` and seed `{A}`:

```text
t0 = {A}
t1 = {A, AA}
t2 = {A, AA, AAA}
t3 = {A, AA, AAA, AAAA}
in general: t_n = { A^k | 1 <= k <= n+1 }
```

Identity retains shorter words only because it is an explicit clause. Each `A->AA` occurrence in `A^k` yields the same `A^(k+1)` and merges.

### Exact page-206 deletion trajectory

Program and seed:

```text
AB     -> epsilon
ABA    -> ABBAB
ABABBB -> AAAAABA

t0 = {ABABAB}
```

The executable exact layers are:

```text
t1 = {
  ABAB,
  ABABBABB,
  ABBABBAB
}

t2 = {
  AB,
  ABABBB,
  ABBABB,
  ABBABBBABB,
  ABBBAB,
  BABBAB
}

t3 = {
  epsilon,
  AAAAABA,
  ABBABBBB,
  ABBB,
  ABBBBABB,
  BABB,
  BABBBABB,
  BBAB
}
```

Epsilon is present as a real word at `t3` and disappears at `t4` unless regenerated. Starting instead from `{ABA}` yields layer cardinalities `1,2,2,1,0` for `t0..t4`, followed by empty-layer reference stutter. This distinguishes deletion, dead-end dropping, epsilon, all-dead advancement, and quiescence.

### Exact cross-parent merge trajectory

Official program data for:

```text
AAB -> BB
BA  -> ABB
seed = {ABBAAB}
```

gives:

```text
t0 = {ABBAAB}
t1 = {ABABBAB, ABBBB}
t2 = {AABBBBAB, ABABABBB}
t3 = {AABBBABBB, ABAABBBBB, BBBBBAB}
```

There are four `t2 -> t3` rewrite witnesses but only three exact targets. `AABBBABBB` has one witness from each parent and appears once in `t3`. This is a direct differential oracle against path-copy state, per-parent-only deduplication, and witness-weighted branching.

### Sorted-word invariant profile

The local OCR damages this example. The official page-937 primary source gives:

```text
AB  -> BBB       delta counts = (-1,+2)
ABB -> AAAB      delta counts = (+2,-1)
```

For a proved invariant that every word is sorted as `A*B*`, the exact word can be represented by its count pair. From `(4,3)` the possible next pairs are `{(3,5),(6,2)}`.

This is a strict invariant-backed lowering/optimization. Sorting an arbitrary word, identifying anagrams, or replacing exact word equality with count equality changes the base construction.

### Adversarial conformance suite

1. **Overlapping matches.** `AAA` under `AA->B` yields exactly `{BA,AB}`, not one preferred child, a simultaneous `B`, or an error.
2. **Multiple RHS values.** `A->B` and `A->C` yield `{B,C}`. Permuting clause serialization preserves state and witness set.
3. **Newborn deferral.** `A->AA` gives `{A}->{AA}->{AAA}`. The two positions in `AA` both yield `AAA`, which appears once with two witnesses.
4. **One-splice alternatives.** Disjoint matches do not combine in a child unless a later layer applies another clause.
5. **Merge witness.** `{AA}` with `A->epsilon` and `AA->A` has three witnesses but successor exactly `{A}`.
6. **Diamond merge.** `A->B,A->C,B->D,C->D,D->E` yields `{A}->{B,C}->{D}->{E}`. `D` fires once while its event retains both inbound witnesses.
7. **Dead branch.** Seed `{A,C}` under `A->B` yields `{B}` with `C` recorded dead, then `empty_layer` with `B` dead.
8. **Epsilon versus empty.** `{epsilon}` is nonempty state; with no empty-LHS clauses it advances once to `empty_layer`.
9. **No global visited set.** `A->A` produces an event every layer; `A->B,B->A` alternates forever. A compressed graph cache cannot suppress recurrence.
10. **Cross-parent merge.** If `AB` and `BA` both rewrite to `X`, successor is `{X}` with two inbound witnesses and no chosen parent.
11. **No implicit accumulation.** A parent absent from all child values disappears even if it appeared in an earlier or compressed graph layer.
12. **Exact reconstruction.** Recompute all match positions, splice every witness, set-union children, and compare dead ends/child groups exactly.
13. **Order invariance.** Permuting old-layer, clause, match, hash, or worker order preserves semantic state and the mathematical witness set.
14. **Validation.** Reject empty LHS, out-of-alphabet sides/seeds, stale snapshot, wrong span/LHS, fabricated/missing match, duplicate serialized clause, callback matcher/canonicalizer, and implicit cyclic matching.

## Variants, Relations, and Boundaries

- **Base literal multiway systems:** the native finite exact word-set construction above.
- **Semi-Thue/Thue systems:** bidirectional clause-pair restrictions over the same literal engine; reachability equivalence is a relation, not base state identity.
- **Semigroups/groups/monoids:** strict reverse/inverse rule presets plus algebraic interpretation. Connected components, equivalence classes, and Cayley graphs are observers/relations.
- **Formal grammars:** regular/context-free/context-sensitive/unrestricted restrictions can use the literal engine where their rules are literal. Terminal/nonterminal status and accumulated terminal language are program metadata/observers.
- **Pattern-variable term/canonical systems:** require a structural matcher/template carrier, not literal-word flags or callbacks.
- **Sorted systems:** exact count-vector lowering only under a proved sorted invariant.
- **Cyclic limited-size systems:** the Notes state the idea but do not fix wraparound match/splice conventions; defer a separate cyclic-word matcher.
- **Multidimensional and network substitution systems:** require block/subgraph topology and reconnection semantics.
- **Multiway tag systems:** the supplied code omits `Union` and therefore retains duplicate derivations. Whether deliberate or incidental is underdetermined; treat it as a separate multiplicity-sensitive variant, not a base merge switch.
- **Arithmetic/complex-number multiway systems:** typed numeric carriers and closed arithmetic results; they may reuse exact branch merging after their own evidence stages.
- **Nondeterministic Turing machines and games:** different state/control and move algebras; not word callbacks.
- **Chapter 9 causal-event systems:** event order, causal invariance, and branchial/causal graphs require a separate audit.
- **Infinite random initial words:** explicitly unsuitable for the base all-possible finite expansion in the cited seed discussion; finite exact seeds are native.
- **Layered diagrams, compressed state graphs, derivation multigraphs, path-causal networks, confluence, Church-Rosser, normal forms, counts, growth, periods, frequencies, and rendering:** downstream analyses/views.
- **Random-rule frequency claims:** no canonical enumeration, size profile, sampling distribution, or complexity criterion is supplied; no conformance sampler can be inferred.

## Current API Fit

| T30 responsibility | Current proposal fit | Required conclusion |
|---|---|---|
| State/support | One dense `D -> A` field on rank-0..3 coordinates | SEMANTIC MISMATCH; add a finite exact set of finite words |
| Alphabet/word value | Finite symbolic alphabet | PARAMETERIZATION for symbols; dynamic words/layers still required |
| Source | Writable coordinate frontier | SEMANTIC MISMATCH; all program-owned matches in all parent words |
| Read | Coordinate offsets or one selected match | T16 matched-span semantics DIRECT; selection coverage differs |
| Program | Scalar table/formula or ordered literal clauses | PRINCIPLED EXTENSION; unordered finite literal relation with epsilon RHS |
| Result | Same-site scalar or one interval replacement | T16 pure one-splice child construction DIRECT per branch |
| Update | Fixed-support write or T16 single-splice successor | SEMANTIC MISMATCH; exact all-branch child union |
| Equality | Array equality | SEMANTIC MISMATCH; exact word equality inside finite set equality |
| No match | Copy-forward or T16 terminal state | SEMANTIC MISMATCH; dead parent drops from next layer |
| Successor | One scalar/dense/word state | PRINCIPLED EXTENSION; one set-valued macro successor |
| Trace | Dense fixed frame | SEMANTIC MISMATCH; ragged word sets plus witness groups |
| Graph | No native state graph | NOT REQUIRED for execution; layered/compressed graphs are projections |
| Horizon/resources | Dataset/executor limits | DIRECT only as external policy; pruning never exact state |
| Orchestration | Source/read/result/update shell | DIRECT at the responsibility level |

`simple_programs.md:3-22,87-105,169-195` fixes dense fields/shapes; `40-69,394-452` describes coordinate selectors; `1767-1791,2124-2198` assumes scalar fixed-support writes/copy-forward. `FORMULAIC` at `2036-2071` would hide branch enumeration/merge in a callback and is rejected.

T13 contributes finite ordered words and ragged word serialization. T16 contributes literal occurrence discovery, exact matched-span validation, and one interval splice. T30 changes program order, selection coverage, deletion validation, outcomes, state carrier, and commit, so neither prior public construction is weakened or repeatedly invoked as a workaround. T29's port graph is only a possible trace visualization target.

## Current Runtime Fit

| Runtime area | Finding | T30 disposition |
|---|---|---|
| `alphabets.py` | Finite symbolic values exist | Reuse declared symbols, not scalar-array state |
| `loci.py:31-94` | Finite coordinate loci and predicate callbacks | Cannot address word values/match intervals across a layer |
| `frontiers.py:38-80` | Only dense `time_slice` | Wrong source coverage |
| `neighborhoods.py:46-60` | Offset gathers, no literal matcher | Reuse none; synthesis may place shared matcher outside spatial neighborhoods |
| `rules.py:30,65-78` | Scalar/callable family rule | Reject; add closed literal-relation data |
| `specs.py:23-82` | Fixed shape and raw family payloads | Cannot validate finite word-set state/program |
| `rollout.py:40-175,576-660,825-831` | Fixed preallocation plus family dispatch | No multiway execution; do not add a branch |
| `datasets.py:321-330` | Equal-shape stack | Requires explicit ragged layer/episode collation |
| current tests | No branching/merge/epsilon/recurrent-layer coverage | Add structural conformance tests |
| visualization | Dense array assumptions | Add downstream layered/compressed graph renderer only after raw trace |

No existing module provides all-match enumeration, exact child-set union, dead-end accounting, derivation witness groups, recurrent time layers, or compressed-state-graph lowering.

## Principles Audit

- **Principle 0:** all alternatives and exact merging are defining semantics. One sampled path, derivation bag, or precompressed graph changes the construction.
- **Principles 1-4:** word-set state, all-match sources, matched spans, closed clauses, one-splice branch results, exact merge, and provenance are explicit.
- **Principle 5:** the current layer is Markovian. Global visited sets, accumulated language, first-seen depth, and chosen ancestry remain trace/observer data.
- **Principles 6-8:** word positions, layer membership, derivation witnesses, compressed graph nodes, render coordinates, and batch slots are distinct address/identity domains.
- **Principles 9-10:** named examples are strict clause/seed presets, not family executors or hidden branch policies.
- **Principle 11:** overlapping all-match selection, one splice per child, newborn deferral, exact target union, and dead-parent dropping are semantic; enumeration/hash/worker order is incidental.
- **Principle 12:** exact ragged layer/event traces precede count plots, layered drawings, compressed graphs, causal graphs, and batching.
- **Principles 13-15:** overlap, diamonds, cross-parent merge, epsilon/empty, identity recurrence, and witness reconstruction are adversarial cases.
- **Principles 16-17:** `DistinctBranchMerge` is an honest eighth update sibling. Replaying T16 or passing `successors(state)` to a generic loop would be a shim/vacuous executor.

Rejected shortcuts:

- repeated first-match/T16 rollouts, rule priority, leftmost choice, random branch sampling, or arbitrary `successors`/matcher/canonicalizer callback;
- simultaneous multiple splices in one child, in-step rescan/newborn firing, or mutation of the old layer during enumeration;
- derivation copies or weights as base state, per-parent-only deduplication, one chosen ancestry after a merge, or duplicate-clause branch weighting;
- preserve-no-match fallback, implicit identity, accumulating prior layers, terminalizing each dead word, or collapsing all-dead advancement with empty-layer stutter;
- global visited suppression, memoized first-seen-only firing, compressed graph used as live state, or confluence/normal-form quotient;
- length, count, sorted/anagram, symmetry, semigroup/group, or renderer equality substituted for exact word equality;
- fixed word length/state count/branch count, pruning, beam search, truncation, silent resource partials, or padded capacity presented as semantics;
- packing a whole layer/graph in a scalar, dense tensor, coordinate field, T29 graph, host graph engine, or `Any` payload;
- applying base `Union` to the multiplicity-sensitive multiway-tag code without separate evidence.

## Detailed Implementation Plan

1. Close direct-name, alias/confluence, implementation-symbol, main figure, Notes, program, actual Index, split, history, group/grammar, variant, graph, seed, growth, and relation searches with no silent candidates.
2. Reconstruct exact word-set state, literal relation, all overlapping old matches, one-splice child results, exact branch union, dead ends, epsilon/empty layer, recurrence, outcomes, and traces.
3. Recover executable main/deletion/merge/sorted presets and independently derive overlap, diamond, recurrent, dead, and validation adversaries.
4. Separate layered state, derivation multigraph, simple edges, compressed state graph, accumulated language, confluence, counts, and renderings.
5. Compare every responsibility with T13/T16/T29, `simple_programs.md`, runtime, and tests; establish the eighth update law without reopening prior public validators/commits.
6. Audit no-cheating constraints, resources, variant boundaries, ragged collation, and graph views.
7. Reintegrate global evidence/design/plan ledgers and write the implementation-ready Goal 2 stage.

## Goal 2 Implementation Stage

### G2-T30 — Exact literal multiway branching and distinct-child merge

Dependencies: the synthesis-selected finite `Word` carrier and epsilon-capable private ordered edit from T13/T17; T16's pure literal occurrence/span/splice utilities; shared typed outcomes/errors and executor orchestration. Do not depend on T16 priority/terminal semantics, T29 graph state, a host rewrite engine, or a successor callback.

1. Add immutable `MultiwayLayer` as a finite set of normalized alphabet-closed words with exact serialization/hash/equality and explicit epsilon/empty-layer distinctions.
2. Add `MultiwayLiteralProgram` as a finite unordered relation `NonEmptyWord -> Word`. Reject duplicate serialized pairs, empty LHS, undeclared symbols, callbacks, and implicit reverse/identity/default behavior.
3. Add program-coupled `AllApplicableLiteralMatches` and `MatchedWord` using shared literal occurrence code. Enumerate every overlapping occurrence in every old parent and retain exact snapshot/clause/span identity.
4. Add `BranchIntervalReplacement` using the shared pure prefix+replacement+suffix kernel. Do not expose a simultaneous match set as one child result.
5. Add `DistinctBranchMerge` through the shared executor shell. Validate exact match coverage, build one child per witness, exact-set-union children across rules/spans/parents, record dead parents and witness groups, and emit one atomic macro successor without a multiway family branch.
6. Add `Advanced` for every nonempty old layer, including all-dead to empty and identity `changed=false`. Add event-free `Quiescent(EmptyLayer)` with explicit reference stutter. Keep horizon/fixed/cycle/resource/cancel/error policies separate.
7. Add raw ragged `MultiwayTrace` frames/events. Build layered simple edges, witness multigraphs, compressed one-node-per-word graphs, counts, first-seen/accumulated-language, paths/confluence, and rendering strictly downstream.
8. Add exact page-219, page-206, official merge, and sorted-invariant presets/diagnostics. Preserve source repairs/provenance and keep program, seed, and horizon independent.
9. Represent semi-Thue/group/grammar profiles as strict data restrictions only where literal semantics match. Defer cyclic, pattern-term, multidimensional/network, tag-multiplicity, numeric, Turing/game, and causal-event variants to separately typed stages; add no mode flags.
10. Audit exports/specs/serialization/datasets/batching/visualization and production source for callbacks, family dispatch, T16 replay, ordering leaks, global visited sets, path-copy state, improper dedupe, implicit persistence, pruning/caps, epsilon collapse, and observer feedback.

Completion requires:

- exact word/layer/program normalization, hashing, permutation invariance, epsilon/empty, and malformed-data tests;
- every-overlapping-match and `AAA/AA->B` goldens;
- page-219 `{A^1..A^(n+1)}` layers and newborn/identity merge witnesses;
- page-206 `t0..t3` exact layers, `ABA` cardinalities `1,2,2,1,0`, epsilon disappearance, all-dead event, and empty-layer quiescence;
- official cross-parent `t0..t3` trajectory, four-witness/three-child assertion, and child grouping;
- three-witness/one-child, diamond, cross-parent, dead-branch, identity, two-cycle, no-accumulation, and clause/enumeration-order adversaries;
- exact reconstruction of matches, one-splice children, next set, dead ends, and witnesses;
- sorted-count lowering only after invariant proof, with repaired `{(-1,2),(2,-1)}` oracle;
- raw ragged trace before explicit graph/count/render/batch lowering;
- explicit rejection/defer tests for cyclic conventions and base-versus-tag multiplicity;
- unchanged T13/T16/T29 semantics, one shared executor shell, no multiway rollout/callback, and all repository tests passing.

## No-Cheating Checks

- No repeated deterministic-path executor, random branch choice, branch callback, `successors(state)` callback, or named multiway rollout.
- No one-path selection, rule priority, first-match selection, simultaneous multi-match splice, in-step newborn firing, or no-match parent preservation.
- No derivation-copy multiplicity in base state, witness weighting, global visited suppression, or old-layer accumulation without an identity rule.
- No epsilon/empty-layer collapse, terminal reinterpretation, fake boundary, fixed word/state capacity, pruning, beam search, or silent resource truncation.
- No length/count/anagram/symmetry/group/normal-form quotient as base equality.
- No whole layer/state graph packed in a scalar, tensor, coordinate lattice, T29 port graph, or host graph engine.
- No partial semantic successor on resource exhaustion and no hidden maximum word/layer/branch count.
- No base exact-state `Union` silently imposed on a variant whose primary executable code preserves multiplicity.

## Completion Requirements

- [ ] All names, aliases, figures, Notes/programs, actual Index entries, splits, history, variants, observers, and relations resolved with zero silent remainder.
- [ ] Native word-set state, program, all-match source/read/result/update, exact merge, dead ends, epsilon/empty layer, recurrence, outcomes, and traces reconstructed.
- [ ] Exact canonical trajectories and adversarial overlap/merge/recurrent/dead/identity/provenance invariants specified.
- [ ] Current API/runtime/principles fit and T13/T16/T29 reuse/divergence explicit.
- [ ] Goal 2 implementation/conformance handoff and global reintegration complete.

## Stage Results

In progress. Core prose and executable Notes already establish all-overlapping-match, one-splice-per-branch, exact-word union, dead-parent dropping, deletion, epsilon, and the layered-versus-compressed-graph distinction. The remaining figure/index/variant audit must close before the semantic contract is marked complete.
