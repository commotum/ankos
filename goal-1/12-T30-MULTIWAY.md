# 12-T30-MULTIWAY

Status: **REOPENED — ARCHITECTURE AUDIT; EVIDENCE CLOSED**

The evidence/search closure and conformance fixtures remain valid. Multiway uses the shared rewrite runner with an UPDATE that lifts one successor to a set of successors; it does not require a multiway executor.

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
- Main book time labels count the initial layer as step 1; the implementation contract and goldens use zero-based `t0` and state the shift explicitly.
- Every page-219 through page-224 local figure and every page-952 Notes observer has been inspected. Image-only page-223 examples establish diversity but lack textual seeds; no mandatory presets are fabricated.
- Two source corruptions are repaired transparently: the alternative list code uses sequence blanks in the official CDF, and the sorted example is `AB->BBB, ABB->AAAB` in the official page-937 source.
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
2. Read the complete main core `BOOK:2494-2566` and its clean split duplicate `CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:325-395`. Canonical provenance remains the monolith.
3. Exact phrase `multiway system(s)` found 267 occurrences on 182 lines. The broader token regex `multi(?:way|-way)` found 277/186: 204/136 before the actual Index and 73/50 in it; the main core contributes 20/13 and native Notes 24/16.
4. A narrower direct/alias/confluence vocabulary found 352/218. Expanding it to semi-Thue, string/term rewrite, production/associative/canonical systems, nondeterminism, generative grammar, Church-Rosser, word problem, branching time, and all-possible replacements found 388/224: 269/152 before the Index and 119/72 in it.
5. The core implementation-symbol regex `MWStep1?|MWEvolveList|ReplaceList|StringReplacePart|StringPosition` found 18/16 whole, 15/14 before the Index, 3/2 in it, and 10/9 in native Notes. The extended sweep including multiway-tag symbols found 20/18.
6. Inspected every local page-219 through page-224 raster and page-952 Notes raster. Exact main rules/seeds/layers/count anchors were decoded where present; page-223 panels with absent seeds remain observers, not invented presets.
7. Read `BOOK:13921-14025` and verified the string/list implementations, no-match drop, exact `Union` merge, diagram multiplicity projection, growth, history, group/grammar relations, and all named variants.
8. Verified deletion, page-224, and official sample trajectories independently. Inspected the official Chapter 5 CDF and official page-937 general-properties note to repair sequence-blank and sorted-rule OCR damage.
9. Followed Chapter 9 `BOOK:6016-6076` and Notes `16511-16556` for paths, compressed spacetime graphs, convergence/confluence, completion, and causal-network relations.
10. Followed `BOOK:19324-19339` for multiway tags/word problems and `19816-19822` for proof-search deduplication/heuristics. These are distinct variants/algorithms, not base stepping.
11. Verified `BOOK:14275` explicitly excludes infinite random multiway initial conditions.
12. Resolved the consolidated actual Index route `BOOK:21531-21556` after the actual Index start at `20826`. Every main, numeric, branching-time, confluence, causal, complexity, path, spacetime, tag, word-problem, and variant endpoint was dispositioned.
13. Audited `simple_programs.md`, runtime modules, tests, prior T13/T16/T29 stages, and no-cheating constraints. No current multiway semantics were found.
14. All direct names, aliases, figures, Notes/programs, actual Index/splits, history, variants, observers, and relations are dispositioned. The base literal construction has zero unresolved mechanics; explicit variant/source gaps are recorded rather than guessed.

## Book Excerpts

Canonical `BOOK` means `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`. These 25 groups cover every unique construction-relevant passage; split duplicates and primary-source repairs are logged in the search.

### E01 — Collections of possible states

- Provenance: `BOOK:2494-2510`, page-219.
- Fact: each state is a finite word; every possible block replacement is applied, and all distinct resulting words are kept. The page-219 preset is `{A->A,A->AA}` from seed `{A}`.

### E02 — Simple exact growth laws

- Provenance: `BOOK:2512-2522` and local page-220 pictures 4/5/figure 6.
- Fact: three literal presets have one-indexed counts `Ceiling[t/2]`, `t`, and `Fibonacci[t+1]`. The rules/seeds and zero-index layers are recorded in the oracle section.

### E03 — Fluctuating slow growth

- Provenance: `BOOK:2524-2532` and local page-220 figures 9-11.
- Fact: two image-decoded systems show roughly quadratic and linear growth with essentially repetitive fluctuations at scales 40 and 161. Count/difference plots are observers, not state.

### E04 — Deletion, epsilon, and complex count behavior

- Provenance: `BOOK:2534-2542` and local page-221 figures 2-3; printed page 206.
- Fact: one clause deletes without inserting, so zero-element words appear. Count differences exhibit a shifted 1071-step repetition; rapid branching creates practical resource pressure but no semantic pruning.

### E05 — Rapid growth and layer geometry

- Provenance: `BOOK:2542-2550` and local page-222 picture 3/page-223 figure 1.
- Fact: a simple preset eventually generates all binary words beginning with `A` with Fibonacci layer counts and exact first-occurrence ranks. Other panels establish repetitive, nested, and complex layer geometries; several image-only seeds are absent and not reconstructed.

### E06 — Recurrent layers and compressed state graph

- Provenance: `BOOK:2552-2566` and local page-224 pictures 2/3/6.
- Fact: an exact word can recur on several layers and always has the same outgoing relation. The figure shows repeated-per-layer, globally folded, and accumulated-network views of the same `{AA->epsilon,BA->ABB,BB->A}` evolution.

### E07 — Exact string implementation

- Provenance: `BOOK:13921-13938`.
- Fact: `StringPosition` finds every occurrence of one LHS and `StringReplacePart` produces one child per position; `MWStep` maps over every rule and old string and applies `Union`. `MWEvolveList` iterates complete layers.

### E08 — Equivalent list implementation and OCR repair

- Provenance: `BOOK:13940-13948` and the official Chapter 5 CDF.
- Fact: list `ReplaceList` supplies equivalent positional context matching. The local `x_{--}`/`y_{--}` is OCR-damaged; the primary source has sequence blanks. This implementation device does not add rule-visible pattern variables to base literal clauses.

### E09 — Page-206 deletion program and dead-parent rule

- Provenance: `BOOK:13950-13957`.
- Fact: the exact three-clause program and `ABABAB` seed are supplied, and a string with no applicable replacement is explicitly dropped. Empty RHS is native.

### E10 — Exact merging and diagram projection

- Provenance: `BOOK:13959-13963`.
- Fact: `Union` merging is crucial; pictures record only whether one state yields another, not how many rule applications do so. Explicit identity clauses retain old states.

### E11 — Sorted count-vector profile

- Provenance: `BOOK:13963-13968`, repaired against the official page-937 general-properties source.
- Fact: when a program/seed invariant keeps all words sorted, exact words can be represented by symbol counts and clauses by difference vectors. The local printed rule is corrupt; the primary `AB->BBB, ABB->AAAB` gives deltas `(-1,2),(2,-1)`.

### E12 — Page-206 properties and alternate seeds

- Provenance: `BOOK:13970-13986` and page-952 Notes images.
- Fact: total count is roughly quadratic with shifted 1071-period differences; new-string growth is roughly linear with 21-period differences; the third rule appears every step after 50. Stack/reach plots are observers. Seed `ABA` dies, while `ABAABABA` grows exponentially.

### E13 — Frequency and history aliases

- Provenance: `BOOK:13988-13989`.
- Fact: qualitative random-rule frequencies lack a declared sampler. Historical aliases include semi-Thue, string/term rewrite, production, associative-calculus, and Post canonical systems; applications include formal languages and proofs.

### E14 — Semigroup/group restrictions and Cayley graphs

- Provenance: `BOOK:13990-14000`.
- Fact: semigroup/group presentations add paired reverse/inverse rules. Reachability components represent algebra elements, while Cayley graphs connect quotient elements by generator append operations; neither changes exact base word equality.

### E15 — Generative grammar restrictions

- Provenance: `BOOK:14002-14012`.
- Fact: regular, context-free, context-sensitive, and unrestricted grammars restrict rule shapes/nonterminals. A formal language accumulates terminal words over reachability; terminal no-match words still drop from the next active layer.

### E16 — Multidimensional, cyclic, and tag boundaries

- Provenance: `BOOK:14014-14016`.
- Fact: array blocks, cyclic limited-size strings, and multiway tag systems are named variants with different support/matching or multiplicity questions. The short cyclic note does not define wrap-splice details.

### E17 — Numeric, nondeterministic, physics, and game relations

- Provenance: `BOOK:14017-14025`.
- Fact: `n->{n+1,2n}` is a numeric exact-set lift; complex numbers, nondeterministic machines, fundamental-physics systems, and games share branching only and retain their own carriers/rules.

### E18 — Infinite random initial conditions are excluded

- Provenance: `BOOK:14275`.
- Fact: an infinite random multiway seed would normally generate infinitely many possibilities, so the base construction cannot meaningfully use it. Finite exact seeds remain independent program data.

### E19 — Multiple histories in Chapter 9

- Provenance: `BOOK:6016-6022`.
- Fact: a path chooses one single replacement at each event, while the multiway structure retains all such histories. This corroborates one-splice branches rather than simultaneous edits.

### E20 — Path convergence and causal invariance

- Provenance: `BOOK:6042-6076`.
- Fact: alternative paths can diverge/converge and yield causal networks. Path-causal behavior is derived from event histories, not identical to the Chapter 5 state-transition graph.

### E21 — Spacetime graph as an alternative model

- Provenance: `BOOK:16511-16519`.
- Fact: keeping one node per exact word ever produced defines a complete spacetime network instead of successive layers. This is explicitly an alternative representation/model and cannot justify global visited suppression in base stepping.

### E22 — Convergence, confluence, normal forms, and completion

- Provenance: `BOOK:16521-16556`.
- Fact: convergence/Church-Rosser, termination, normal forms, and Knuth-Bendix-style completion are program properties or program-transforming analyses; causal networks can vary by rewrite path.

### E23 — Multiway tags and word problems

- Provenance: `BOOK:19324-19339`.
- Fact: the supplied multiway-tag implementation flattens derivations without `Union`, so multiplicity may persist. Word reachability/equivalence is a decision problem over the graph, not state equality or stepping.

### E24 — Proof-search optimizations

- Provenance: `BOOK:19816-19822`.
- Fact: path deduplication, length heuristics, lemmas, canonicalization, and bidirectional search optimize proof finding. They do not license pruning or quotienting an exact layer.

### E25 — Actual Index routing

- Provenance: consolidated actual Index route `BOOK:21531-21556`.
- Fact: the Index routes main pages 204-209, numeric systems, branching time, canonical/confluence/causal properties, sequential comparison, completion, reducibility, termination, paths, spacetime networks, tags, word problems, grammars, groups, and variants to passages dispositioned above.

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

### Three page-220 simple systems

All use seed `{A}` and zero-based API layers.

```text
case 1: {A->AA, AA->A}
  counts = 1,1,2,2,3,3,...
  S0={A}
  S1={AA}
  S2={A,AAA}
  S3={AA,AAAA}
  book one-index formula: Ceiling[t/2]

case 2: {A->A, A->AA, AA->A}
  S_n={A^k | 1<=k<=n+1}
  count=n+1
  book one-index formula: t

case 3: {A->AB, B->A}
  counts = 1,1,2,3,5,8,13,21,...
  S0={A}
  S1={AB}
  S2={AA,ABB}
  S3={AAB,ABA,ABBB}
  S4={AAA,AABB,ABAB,ABBA,ABBBB}
```

Case 3 eventually generates every binary word beginning with `A`. A word with `m` As and `n` Bs first appears at book step `2m+n-1`, or zero-based layer `2m+n-2`. These fixtures jointly guard single-splice timing, exact merging, recurrence, and the book/API time shift.

### Two page-220 fluctuating systems

The first image-decoded preset is:

```text
seed = {BABBAAB}
rules = {ABA->BBAA, BAA->AAB}
counts t0..t16 =
  1,1,2,2,3,3,3,2,4,3,4,3,5,5,5,4,6
c40=16, c80=40, c100=56, c200=172, c250=238
```

The book describes essentially 40-step fluctuation and roughly quadratic growth. It does not claim exact count periodicity, so conformance must not strengthen it.

The second is:

```text
seed = {ABAAB}
rules = {AA->BABBBBA, BAB->A}
counts t0..t16 =
  1,1,2,2,2,3,4,4,4,4,4,4,6,8,6,6,6
c40=16, c80=27, c100=33, c161=55, c200=66, c250=86
```

Direct exact evolution of the decoded preset gives first differences with period 161 from index 2 and roughly linear growth, matching the caption. These count sequences are derived regression oracles; exact word layers remain authoritative state.

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

t4 = {AAAAA,AAAAABBAB,ABBBBB,BABBBB,BB,BBBABB}
t5 = {AAAAABB,AAAABAB,BBBB}
t6 = {AAAAB,AAAABBABB}
t7 = {AAA,AAAABBB,AAABABB}
t8 = {AAABB,AAABBABBB}
t9 = {AAABBBB,AAB,AABABBB}
t10 = {A,AAAAAABA,AABBABBBB,AABBB}
```

The initial counts are `1,3,6,8,6,3,2,3,2,3,4`. Epsilon is present as a real word at `t3` and disappears at `t4` unless regenerated. Starting instead from `{ABA}` yields layer cardinalities `1,2,2,1,0` for `t0..t4`, followed by empty-layer reference stutter. This distinguishes deletion, dead-end dropping, epsilon, all-dead advancement, and quiescence.

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

### Exact page-224 layered/folded/network fixture

Program and seed:

```text
AA -> epsilon
BA -> ABB
BB -> A
seed = {BBA}
```

The exact layers shown across the repeated, globally folded, and accumulated-network views are:

```text
S0 = {BBA}
S1 = {AA,BABB}
S2 = {epsilon,ABBBB,BAA}
S3 = {AABB,ABAB,ABBA,B}
S4 = {AAA,AABBB,ABABB,BB}
S5 = {A,AAAB,AABA,AABBBB,ABAA,BBB}
S6 = {AAABB,AABAB,AABBA,AB,BA,BBBB}
S7 = {AAAA,AAABBB,AABABB,ABB,BAB,BBA}
S8 = {AA,AAAAB,AAABA,AAABBBB,AABAA,ABBB,BABB}
```

At `S2 -> S3`, `ABBA` is reached from both `ABBBB` and `BAA`. At `S3 -> S4`, `AAA` is reached from both `AABB` and `ABBA`. In `AAA`, `AA` matches at positions 0 and 1 and both yield `A`, producing two witnesses but one child and one simple edge. Folding each word to its first picture occurrence must preserve these later layer memberships and outgoing applications.

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
15. **Single versus simultaneous.** `{AA}` under `A->B` yields `{AB,BA}` at `t1` and `{BB}` at `t2`; `BB` must not appear at `t1`.
16. **Self-loop multiplicity.** `AAA` under `A->A` yields one state and one simple self-edge but exactly three span witnesses.
17. **Cross-rule duplicate.** `AA` under `A->B` and `AA->BA` yields `{AB,BA}`; `BA` has two witnesses but one semantic occurrence.
18. **Symbol alpha-equivariance.** Apply any bijection to alphabet, program, and layer. Successor and witnesses must be the corresponding renaming.
19. **Graph invariant.** `S_t` equals exact-length-`t` reachability from the seed in the simple state graph; accumulated graph nodes equal `union_{i<=t} S_i` without replacing `S_t`.
20. **Resource limit.** A deliberately tiny cap returns an explicit resource/partial diagnostic and publishes no ordinary pruned successor.

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
- **Arithmetic/complex-number multiway systems:** typed numeric carriers and closed arithmetic results; they may reuse exact branch merging after their own evidence stages. The documented `n->{n+1,2n}` profile from 0 begins `{0}`, `{0,1}`, `{0,1,2}`, `{0,1,2,3,4}`, but must use a closed arithmetic AST coordinated with T34 rather than a callback.
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

- [x] All names, aliases, figures, Notes/programs, actual Index entries, splits, history, variants, observers, and relations resolved with zero silent remainder.
- [x] Native word-set state, program, all-match source/read/result/update, exact merge, dead ends, epsilon/empty layer, recurrence, outcomes, and traces reconstructed.
- [x] Exact canonical trajectories and adversarial overlap/merge/recurrent/dead/identity/provenance invariants specified.
- [x] Current API/runtime/principles fit and T13/T16/T29 reuse/divergence explicit.
- [x] Goal 2 implementation/conformance handoff and global reintegration complete.

## Stage Results

T30 is complete. The exact-name audit dispositioned 267 occurrences on 182 lines and the broader token audit 277/186; narrower and expanded alias/confluence audits dispositioned 352/218 and 388/224; core and extended implementation-symbol audits dispositioned 18/16 and 20/18. Twenty-five canonical groups cover the definition, every page-219 through page-224 figure, executable Notes/programs, page-952 observers, actual Index/splits, history, groups/grammars, numeric/tag/structural variants, spacetime/causal graphs, confluence/completion, proof search, and relations. Zero base-literal mechanics remain unresolved.

The construction is a finite exact set of finite words under a finite unordered relation `NonEmptyWord -> Word`. Every overlapping occurrence of every clause in every old parent independently produces one one-splice child; `DistinctBranchMerge` exact-word-unions all children and records dead parents plus every rewrite witness. Equal targets merge across positions, rules, and parents. Epsilon is a word; the empty layer is an event-free reference stutter reached only after an all-dead `Advanced` event. Recurring words fire on every layer, so a compressed one-node-per-word graph is downstream and never a global visited set.

Page-219/page-220 layers and growth, page-206 `t0..t10` and extinction, the official four-layer cross-parent merge, page-224 repeated/folded/network views, repaired sorted count vectors, overlap, one-versus-simultaneous splice, diamond/cross-rule/cross-parent merging, identity/two-cycle recurrence, epsilon/empty, reconstruction, order, alpha, and graph invariants close the handoff. T13 words and T16 matching/splicing compose privately; their public updates/outcomes remain unchanged. T29 graph state remains distinct.

## Integration Results

- Added finite exact word-set layers and unordered epsilon-capable literal rewrite relations to the semantic inventory.
- Added program-coupled every-overlapping-match sources and one-splice branch results while reusing T16's pure literal occurrence/edit kernel.
- Added `DistinctBranchMerge` as the eighth public update law, with exact target union, dead-parent dropping, and lossless witness grouping.
- Distinguished eventful identity/all-dead advancement, epsilon, and event-free empty-layer quiescence.
- Separated layered state from derivation multiplicity, simple/derivation graphs, globally compressed spacetime graphs, accumulated languages, confluence, counts, proof search, and rendering.
- Preserved base exact-set semantics while isolating the no-`Union` multiway-tag code and cyclic/pattern/block/numeric/control variants for separate audits.
- Preserved T01/T09/T12/T13/T16/T17/T19/T20/T27/T29 conclusions; no prior stage is reopened.
- Next stage: T31, Local Constraint Systems.
