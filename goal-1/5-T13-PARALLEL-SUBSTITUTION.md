# 5-T13-PARALLEL-SUBSTITUTION

Status: **COMPLETE — EVIDENCE AND ARCHITECTURE RECLOSED**

Architecture authority: the T13 row and runner contract in `architecture-audit.md` supersede any separate-executor/top-level-class framing below.

The evidence/search closure and conformance fixtures remain valid. T13 justifies a support-changing ordered-replacement policy on the shared `UPDATE` axis, not a construction-specific executor or top-level semantic class.

## Current Facts

- Exact catalog row: T13, CSV line 14, `Neighbor-Independent Substitution Systems`; taxonomy seed `ref/notes/CA-Types.md:331-360`.
- Canonical source is `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md` (`BOOK`).
- A state is an ordered sequence of symbols. At one step every old occurrence is independently replaced by a finite nonempty ordered word determined only by that occurrence's symbol; the successor is the source-order concatenation of all emitted words.
- Replacement is structural. It consumes old occurrences and creates ordered child occurrences, so it is not fixed-locus `Assign` and cannot be represented honestly by same-index writes.
- The ordinary T13 rule is a total alphabet-closed morphism `h: Sigma -> Sigma+`. Allowing the empty word is the T15 creation/destruction extension, not an identity/default convention in T13.
- Finite words beginning with one symbol are the canonical Chapter 3 experiments, but ordinary substitution also has documented infinite-sequence initial conditions. Finite support, one-sided infinite support, and their computation/observation realizations must therefore be explicit.
- Fixed-size growing rows, width-normalized subdivision, trees, turn paths, and row-wrapped 2D pictures are observations of the same sequence/lineage, not alternate program states.
- T13 is deterministic and non-halting: a complete nonempty replacement table yields one successor. An empty input sequence evolves vacuously to itself; it is not an implicit halt.

## Updated Assumptions

- `FRONTIER -> NEIGHBORHOOD -> RULE -> UPDATE` remains substantive only after `UPDATE` becomes an explicit algebra choice. T13 reuses source selection and self-only reads but requires an ordered structural update distinct from assignment/control transition.
- A source is an occurrence handle in the old snapshot, not merely its symbol and not a writable coordinate in a preallocated next slice. Equal-valued occurrences remain distinct sources.
- Sequence position is snapshot-relative. Inserting children to the left changes later integer positions; integer index is not persistent element identity.
- Persistent ancestry is not needed to advance T13, so it must not be smuggled into program state. The update can emit an inspectable parent-to-child interval relation as trace provenance for the canonical tree rendering.
- Parallelism means exactly one generation: only occurrences present in the old snapshot fire, and no newborn is rewritten until the next step.
- Rule completeness and alphabet closure are semantic validation. Mathematica's unmatched-expression behavior is an implementation artifact, not an identity fallback.
- Variable length is semantic, not a fixed-capacity array with padding, masks, truncation, or fake empty cells.
- Native infinite sequences are not permission to hide an infinite object in one value. A lazy/stream realization must expose support kind, anchoring, demanded extent, and loss at any finite trace boundary.

## Big Picture Objective

Exhaustively reconstruct neighbor-independent parallel substitution and use it as the first adversarial test of fixed-support assignment. Preserve only the shared source/read/rule orchestration, add an honest ordered replacement result and structural commit, keep lineage and rendering downstream, and hand Goal 2 a finite canonical reference path plus an explicit design obligation for documented infinite support.

## Catalog Identity

- Stable ID: T13.
- Exact name: Neighbor-Independent Substitution Systems.
- Canonical and Index aliases: substitution systems, subdivision systems, sequence homomorphisms, iterated morphisms, uniform tag systems, `0L`/`D0L` systems, and Lindenmayer/L systems. The word/string and colored-element presentations are equivalent.
- `uniform tag systems` is an historical alias here; it does not turn T13 into the queue/deletion construction cataloged as T17.
- Entry kind: variable-support deterministic parallel replacement construction.
- Search vocabulary: substitution/subdivision/replacement system, replace each/every element, fixed block, independently/neighbor-independent, sequence/string/word, concatenate/flatten, parallel/simultaneous, morphism/homomorphism, 0L/D0L/L system, initial condition/word, Thue-Morse, Fibonacci, Cantor, growth matrix/eigenvalue, boxes/subdivision/rescale/tree/branch/path, random infinite sequence, sequential/tag/cyclic/neighbor-dependent/creation-destruction/2D/geometrical variants, and CA/TM/tag emulation.

## Search Log

### Coverage and method

The taxonomy was read before searching. Case-insensitive fixed and regex searches covered direct names, definition phrases, replacement verbs, aliases, examples, Notes functions, renderings, initial conditions, Index routes, and emulation relations. Every one of the 288 canonical lines containing `substitution system` was dispositioned; targeted searches then covered aliases and construction phrases that do not use the direct name.

| Query family | Canonical line count or coverage |
|---|---:|
| `substitution` / `substitution system` | 310 / 288 lines, all classified |
| hyphenated/unhyphenated `neighbor independent` | 31 / 2 lines, all classified |
| `replacement` / `replaced` / `replace each` | 90 / 47 / 5 lines, all classified or explicitly excluded |
| subdivision stems | 21 lines, all classified |
| `morphism` / `homomorphism` | 6 / 4 lines, T13 aliases separated from unrelated mathematics |
| bounded `0L`/`1L`/`D0L`/`L system` forms | 8 direct hits plus Index redirects |
| `Thue-Morse` / `Fibonacci` | 23 / 77 lines, construction routes separated from properties |
| `SSEvolveList` / `StringReplace` | both canonical implementations and sequential contrast inspected |
| rendering/tree/path and random-initial-condition terms | direct Chapter 3/Notes/Index targets followed |

Representative command form was `rg -n -i -e '<term>' BOOK`; broad matches were never treated as evidence without context.

### Candidate disposition

| Region/candidates | Disposition |
|---|---|
| `980-1016` | Base construction, fixed-array contrast, examples, two box renderings, and tree/lineage view included |
| `1018-1052` | Neighbor context, right boundary, empty replacement, creation/destruction, and shifting positions retained only as T14/T15 boundaries or shared structural pressure |
| `1054-1106` | String representation and all-elements parallel contrast included; ordered first-match sequential semantics redirected to T16 |
| `1124-1154` | Ordinary/cyclic tag time-scaled correspondences classified as emulations/relations, not native T13 execution |
| `2358-2366`, `2462` | Ordinary all-elements replacement contrast included; multidimensional scanning/network analogy redirected |
| `4818-4824` | Plant/stem L-system geometry classified as T27 interpretation sharing replacement ancestry, not T13 symbol state |
| `5928-6018` | General/overlapping substitution audited; the one-symbol all-occurrence case and regular causal tree retained, other match policies redirected |
| `6826`, `7118` | Compression/block-frequency observations excluded from state; named substitution rules remain conformance candidates only |
| `7938-7960`, `8022-8040` | CA emulation and inability of basic T13 to emulate complex CA classified; compilation rejected as implementation mechanism |
| `12097-12113` | Complete list/string implementations, rule, seed, flattening, and generation boundary included |
| `12117-12253` | Page 83/84 examples, growth invariant, digit/tree relation, path/2D renderings, aliases, and history classified; behavioral formulas are observations |
| `12352-12356` | Restricted cyclic-tag correspondence retained as an encoding; no queue schedule admitted |
| `12587-13758` | Continued-fraction-driven rules, look-and-say subsequence encoding, nested digits/maps, and geometric projections redirected to T42/T27 or observation relations |
| `14147` | Clean three-symbol, unequal-block T13 rule retained as a secondary conformance fixture |
| `14275` | Infinite random initial sequences included as a genuine support/seed variant |
| `14672`, `17531` | Cantor/attractor and spectral analyses classified as downstream properties |
| `16418-16423`, `16444` | Unique generated-element IDs retained as trace provenance; causal-invariant generalized construction redirected |
| `17596` | Probabilistic neighbor-independent substitution retained as a stochastic variant, not deterministic T13 base |
| `18374-18394` | Binary/at-most-two-child CA compiler limit classified as an emulation, not a native constructor |
| Index `20828-22498` | `0L`, `D0L`, subdivision, substitution, uniform tag, Thue-Morse, and related routes followed; Index supplies navigation only |

Chapter 3 split lines 297-369 and Chapter 5 split lines 165-217 duplicate the corresponding monolith. `BACK-MATTER/Notes/Notes.md` is one unrelated truncated Busy-Beaver line. Misnamed `BACK-MATTER/Index/Index.md` is actually a duplicate Notes tail: its T13 implementation at 9-25, aliases at 154-164, later sequential/2D/generalized sections, and OCR repairs add no unique evidence. Atlas lines 89-95/181-183 are summary only. The actual Index exists only in the monolith from 20826. Figure rule glyphs were cross-checked against clean textual Notes rules rather than parsed through merged color/OCR labels.

### Ambiguities resolved

1. `Flatten[# /. rule]` would leave an unmatched Mathematica atom unchanged. Prose says each kind is replaced, and later steps otherwise leave the declared system. T13 therefore requires one unique row for every declared symbol and rejects missing rows rather than inventing an identity fallback.
2. Mathematica can flatten an empty right-hand side, but `BOOK:1026-1028` explicitly introduces disappearance after examples whose every source yields at least one element, and the catalog separates T15. T13 uses `Sigma+`; T15 will test `Sigma*` with deletion.
3. The list implementation does not state parallelism by itself. `BOOK:1060` explicitly says all existing elements are operated on in parallel, and one `NestList` generation rewrites only the old list before flattening. New children never fire in the same step.
4. The implementation's output order is not arbitrary: list replacement preserves old occurrence order and `Flatten` concatenates each replacement word left-to-right. The string implementation independently corroborates the same order.
5. A finite list is not the only native support. `BOOK:14275` explicitly admits infinite random sequences; this is recorded as a support/realization variant rather than silently contradicted by the canonical finite API path.

**Search closure:** two independent audits agree. All direct-name lines, definition phrases, aliases, Notes/Index/split routes, seeds, renderings, growth cases, stochastic/infinite variants, and emulation relations are included, marked duplicate/property-only, or assigned to another catalog construction. Zero T13 evidence candidates remain unresolved.

## Book Excerpts

All excerpts are verbatim from `BOOK`.

### E01 — variable ordered support and fixed neighbor-independent block

`BOOK:982-986`, Chapter 3, “Substitution Systems”:

> cellular automata, mobile automata and Turing machines ... consist of a fixed array of cells. ... the underlying number and organization of cells always stays the same.
>
> Substitution systems, however, are set up so that the number of elements can change. ... one has a sequence of elements ... and at each step each one of these elements is replaced by a new block of elements.
>
> each element of a particular color should be replaced by a fixed block of new elements, independent of the colors of any neighboring elements.

### E02 — replacement happens for every kind at every step

`BOOK:992`, same section:

> at every step each kind of element is replaced by a fixed block of new elements.

The two examples distinguish constant doubling from variable Fibonacci growth.

### E03 — fixed-size and subdivision renderings

`BOOK:996-1004`:

> start from a single element represented by a long box going all the way across the picture. Then on successive steps the rules ... specify how each box should be subdivided into a sequence of shorter and shorter boxes.
>
> any time an element of a particular color appears it will always get subdivided in the same way.

The same rules yield Thue-Morse-, Fibonacci-, and Cantor-related pictures; box scale is not state.

### E04 — replacement lineage has a canonical tree view

`BOOK:1006-1016`:

> start from the trunk of the tree, and then at each step ... determine how every branch should be split into smaller branches.
>
> at each step every branch of a particular color should split into smaller branches in the same way.

Parent-to-child order/ancestry is observable even though persistent identities are unnecessary for the next transition.

### E05 — neighbor dependence is a distinct read model

`BOOK:1018-1022`:

> rules depend not only on the color of a single element, but also on the color of at least one of its neighbors.
>
> the rightmost element is always dropped, since no rule is given for how to replace it.

This is T14 context/boundary behavior, not a T13 option.

### E06 — nonempty output boundary and disappearance extension

`BOOK:1026-1028`:

> every single element should be replaced by at least one new element.
>
> It is, however, also possible to consider substitution systems in which elements can simply disappear.

The first sentence establishes the nondecreasing-length invariant used by ordinary examples; the second is the explicit T15 extension.

### E07 — dynamic positions are not persistent identity

`BOOK:1032` and `1046`:

> the boxes representing each element are scaled to keep the total width the same, whereas on the right each box has a fixed size
>
> only the order of elements is ever significant: ... a particular element may change its position as a result of the addition or subtraction of elements to its left.

The second passage is shown for creation/destruction systems but establishes why sequence order cannot be replaced by stable dense coordinates.

### E08 — explicit string state and all-source parallelism

`BOOK:1058-1062`, sequential-system contrast:

> the state of a substitution system at a particular step can be represented by the string ABBBABA
>
> replacing each element in such a string by a new sequence of elements—so that in a sense these systems operate in parallel on all the elements that exist in the string at each step.
>
> sequential substitution systems ... scan the string from left to right ... perform a replacement for the first such sequence that is found.

### E09 — tag-system equality is time-scaled emulation

`BOOK:1124-1126`:

> after every complete cycle, the sequences obtained correspond exactly to the sequences produced on successive steps in the first three ordinary neighbor-independent substitution systems
>
> a tag system always effectively acts just like a slow version of a neighbor-independent substitution system

The queue schedule remains T17 rather than a T13 rollout mode.

### E10 — ordinary versus sequential replacement count

`BOOK:2358`, Chapter 5:

> ordinary one-dimensional substitution systems, in which every element is replaced at each step, and sequential substitution systems, in which just a single block of elements are replaced at each step.

### E11 — exact list rule, seed, and generation operator

`BOOK:12097-12103`, Notes:

> The rule for a neighbor-independent substitution system ... can conveniently be given as `{1 -> {1, 0}, 0 -> {0, 1}}`.

```text
SSEvolveList[rule_, init_List, t_Integer] :=
  NestList[Flatten[# /. rule] &, init, t]
```

> the initial condition is `{1}`.

Replacement occurs over the old list, each result retains internal order, and flattening concatenates blocks in source order.

### E12 — independently equivalent string presentation

`BOOK:12105-12113`, same Notes:

> representing the rule by `{"B" -> "BA", "A" -> "AB"}` and the initial condition by `"B"`.

```text
SSEvolveList[rule_, init_String, t_Integer] :=
  NestList[StringReplace[#, rule] &, init, t]
```

This independently guards symbol mapping, output order, and the one-generation boundary.

### E13 — growth is derived from emitted-symbol counts

`BOOK:12136`, Notes “Growth rates”:

> form[] the matrix m where m[[i, j]] gives the number of elements of color j + 1 that appear in the block that replaces an element of color i + 1.
>
> A list that gives the number of elements of each color at step t can then be found from init . MatrixPower[m, t]

The same note gives exponential, linear, and quadratic nonempty-rule examples; variable length is genuine semantics, not display width.

### E14 — lineage explains fixed-length digit indexing

`BOOK:12194-12206`, Notes “Connections with digit sequences”:

> the evolution of the substitution system always yields a tree, and the successive digits in n determine which branch is taken at each level in order to reach the element at position n.
>
> where each element is subdivided into exactly k elements [behavior] can be reproduced by a finite automaton ... operating on digit sequences in base k.

This is a derived observer/accelerator for constant block length, not a replacement for native evolution or the variable-length case.

### E15 — paths and wrapped rows are observations

`BOOK:12210-12232`:

> An alternative to representing substitution systems by 1D sequences of black and white squares is to use 2D paths consisting of sequences of left and right turns.
>
> Individual sequences from 1D substitution systems can be displayed in 2D by breaking them into a succession of rows.

Neither interpretation changes the ordered-symbol program state.

### E16 — exact historical aliases and 0L boundary

`BOOK:12249-12251`:

> general neighbor-independent substitution systems (sometimes under such names as sequence homomorphisms, iterated morphisms and uniform tag systems)
>
> under the name of L systems ... So-called 0L systems correspond to my neighbor-independent substitution systems; 1L systems correspond to the neighbor-dependent substitution systems

The Index also routes `D0L systems` to neighbor-independent substitution (`BOOK:21068`).

### E17 — CA compilation has a different time/space realization

`BOOK:7944-7952`:

> these can also be emulated by cellular automata. But ... this is no longer in general true [with] a single step of cellular automaton evolution
>
> the total number of elements in a substitution system can be multiplied by a factor from one step to the next, while in a cellular automaton the size of a pattern can only ever increase by a fixed amount at each step.

A CA compiler is an emulation with progressive time dilation, not native T13 support.

### E18 — basic T13 cannot emulate arbitrary CA behavior

`BOOK:8022-8028`:

> neighbor-independent substitution systems can generate only patterns that are either repetitive or nested—so they can never yield ... patterns ... needed to emulate rule 30.
>
> if one generalizes to neighbor-dependent substitution systems then ... [it is] straightforward to emulate cellular automata

This guards the T13/T14 boundary and rejects a hidden CA-equivalence claim.

### E19 — documented infinite-sequence initial conditions

`BOOK:14275`, Notes “Random initial conditions in other systems”:

> Ordinary substitution systems can operate on infinite sequences of elements chosen at random. Sequential substitution systems, however, rely on scanning limited sequences of elements, and so cannot readily be given infinite random initial conditions.

Infinite support is therefore a real T13 variant; finite padding is not an implementation of it.

### E20 — one-symbol all-occurrence rewrites yield a regular causal tree

`BOOK:5944-5952`, generalized-substitution comparison:

> the result is to update every single element at every step. But since the replacements in these particular rules involve only one element at a time, one in effect has a neighbor-independent substitution system
>
> each element repeatedly branches into several others, yielding a causal network that has the form of a regular tree.

This independently confirms all-source firing and makes replacement events/ancestry observable.

### E21 — generated-element IDs are an explicit provenance representation

`BOOK:16418-16423`, Notes “Generating causal networks”:

> If every element generated in the evolution of a generalized substitution system is assigned a unique number, then events can be represented for example by `{4, 5} -> {11, 12, 13}`

T13 can derive child IDs from `(parent,child_ordinal)` and retain events without making IDs a rule input. Semantic word equality can ignore an order-preserving renaming while raw lineage remains lossless.

### E22 — probabilistic neighbor-independent replacement is a distinct variant

`BOOK:17596`, probabilistic-model Notes:

> probabilistic neighbor-independent substitution systems can yield sequences with hierarchical structures that have approximate nesting.

This changes a table row from one word to a distribution over words and therefore belongs to a later stochastic result algebra, not a hidden RNG option in deterministic T13.

### E23 — changing rule sequences are not one fixed T13 morphism

`BOOK:12587-12595`, “Relation to substitution systems”:

> can in fact be generated by a sequence of substitution rules.
>
> If h is the solution to a quadratic equation, then the continued fraction form is repetitive ... [and] the original sequence can be found by a neighbor-independent substitution system

The general rule-stream construction is catalog T42. Only the collapsed fixed-rule cases are ordinary T13 fixtures.

### E24 — clean multicolor unequal-block example

`BOOK:14147`, pattern-avoiding-sequence Notes:

> the substitution system `{0 -> {0, 1, 2}, 1 -> {0, 2}, 2 -> {1}}`, starting with `{0}`.

This is an unambiguous three-symbol fixture with output lengths 3, 2, and 1.

### E25 — the published CA compiler is explicitly restricted

`BOOK:18374-18394`, Notes “Substitution systems”:

> The specific definition given above works for neighbor-independent substitution systems whose elements have two possible colors, and in which each element is replaced at each step by at most two new elements.

The compiler cannot define general T13 and remains an emulation even within its restricted validity scope.

### E26 — plant L-system geometry adds semantic configuration

`BOOK:4818-4824`, “Growth of Plants and Animals”:

> the tip of each stem is at each step replaced by a collection of smaller stems in some fixed configuration.
>
> every stem in effect just branches into exactly three new stems at each step.

The branching ancestry is shared, but lengths, angles, orientation, and overlap belong to T27 geometric replacement or a declared renderer, not the T13 symbol word.

## Construction Model

### Base deterministic morphism

The native support is a discrete countable linear order: finite for the canonical examples, one-sided `omega` for a stream, or two-sided `zeta` only when a distinguished cut/origin is supplied explicitly. Let old occurrences be `p` and let `h: Sigma -> Sigma+`. The successor occurrence set is

```text
O' = {(p,j) | p in O and 0 <= j < |h(value(p))|}
```

ordered lexicographically by old source order and then child ordinal, with `value'(p,j)=h(value(p))[j]`. `(p,j)` is a derivable lineage identity in the raw transition; the semantic word/configuration may quotient over order-preserving ID renaming because T13 rules read only values.

For a finite word `w = (w_0,...,w_{n-1})`, this abstract rewrite materializes as:

```text
state   = OrderedSequence(support=FiniteOrder(n), values=w)
sources = AllOccurrences(state.old)       # old order, snapshot-scoped handles

for source in sources:
    symbol = SelfSymbol(source)
    result[source] = ReplaceOccurrence(source, h[symbol])

next.values = ParallelReplaceConcat(state.old, results)
            = h[w_0] ++ h[w_1] ++ ... ++ h[w_(n-1)]
```

`ParallelReplaceConcat` validates that every and only old occurrence appears exactly once, every word is nonempty and alphabet-closed, and the source handle belongs to the current snapshot. It then consumes all parents and creates children in lexicographic `(parent_order, child_order)` order. It can return lineage intervals alongside the successor:

```text
parent i -> child interval
[sum_(j<i) |h[w_j]|, sum_(j<=i) |h[w_j]|)
```

The lineage record belongs to the raw transition trace. T13 rules do not read ancestry, so it is not hidden control and must never enter the rule input. A raw snapshot may retain occurrence IDs for lossless provenance while semantic state equality is value/order equality up to ID renaming.

| Dimension | T13 semantics |
|---|---|
| State/support | Explicit ordered symbol sequence; canonical finite word, plus documented infinite-sequence variant with explicit support kind/realization. |
| Alphabet | Finite declared `Sigma`; replacement outputs are words over the same closed alphabet. |
| Sources | Every occurrence present in the old snapshot, in sequence order. Duplicate symbols are still distinct occurrences. |
| Read | Source symbol only; no left/right neighbor, index, ancestry, time, rendering coordinate, or whole word. |
| Rule | Complete deterministic finite table `h: Sigma -> Sigma+`; no missing-row identity and no unrestricted whole-state callback. |
| Result | Typed `ReplaceOccurrence(source, nonempty_word)` structural proposal. |
| Update | Atomic `ParallelReplaceConcat`: one old generation, source-order block concatenation, all parents consumed and children created. |
| Successor | Exactly one ordered sequence. No branch or intrinsic halt; empty input is a vacuous fixed successor. |
| Seed | Initial finite word or explicitly supported infinite sequence is independent of the morphism; canonical seed is `[1]`/`"B"`. |
| Boundary | None for finite words/self-only reads. Infinite support type and origin/finite observation policy are explicit realization data, not padding. |
| Trace | Ragged ordered snapshots plus optional parent-child intervals; later lowering may assign row-local integer positions. |

### Structural invariants

For finite `w`:

```text
|next| = sum_i |h[w_i]|
count(next, b) = sum_a count(w, a) * M[a,b]
M[a,b] = count(h[a], b)
```

- Since `|h[a]| >= 1`, length is nondecreasing; strict growth depends on symbols encountered.
- For constant block length `q`, `|h^t(w)| = |w| q^t`.
- For alphabet size `k` and a declared maximum block length `r`, the derived bounded table count is `(sum_(j=1)^r k^j)^k`; without a length bound the rule family is countably infinite and the book supplies no canonical integer numbering.
- A table object, not an incidental `rule_id: int`, is therefore the native T13 rule identity. Any later codec must be explicit, bounded, bijective, and separately tested.

### Exact canonical trajectory oracle

Using E11's `1 -> [1,0]`, `0 -> [0,1]`, initial `[1]`:

```text
t0 [1]
t1 [1,0]
t2 [1,0,0,1]
t3 [1,0,0,1,0,1,1,0]
t4 [1,0,0,1,0,1,1,0,0,1,1,0,1,0,0,1]
```

This was independently generated from an immutable old word, not by the Notes expression. At `t1 -> t2`, parent 0 emits child interval `[0,2)` and parent 1 emits `[2,4)`.

An ordering adversary uses `A -> BA`, `B -> A`, initial `AB`; the only valid successor is `BAA`. It catches output reversal, source reversal, target sorting, and in-place rewriting.

### Infinite-sequence variant

E19 requires native semantics beyond finite lists. The same pointwise morphism extends to explicitly one-sided infinite support. A two-sided support is coherent only with an explicit cut: the successor cut is placed before the child block of the first source to the right of the old cut. This is a declared realization convention, not a fact to infer from `[x]`. Goal 2 must:

- represent the support kind and origin/cut explicitly;
- use an inspectable lazy/stream or finite-demand realization rather than one opaque value;
- distinguish the infinite state from a requested finite observation window;
- never claim a padded finite tensor is the infinite sequence;
- reject an unspecified two-sided reindex/origin convention rather than inventing one;
- represent an infinite random seed as inspectable index-keyed seed/distribution data with query-order-independent derivation, never a callback or hidden advancing RNG cursor.

The finite reference executor may be delivered first, but the public semantic model must not assert that T13 itself is finite-only.

### Variant disposition

| Variant/relation | Disposition |
|---|---|
| Different finite initial words / canonical single symbol | Seed only |
| Infinite random sequence | Genuine support/seed variant; explicit lazy/observation realization required |
| Probabilistic replacement word | Stochastic distribution-over-words variant; defer until a typed stochastic result/update is evidenced |
| Equal-size row, width-normalized subdivision, tree, turn path, wrapped 2D display | Observers/renderers over sequence and optional lineage |
| Constant versus variable nonempty block length | Same T13 table/result/update with different validated word lengths |
| Empty replacement/disappearance | T15 extension from `Sigma+` to `Sigma*`; same update candidate to be re-audited there |
| Neighbor-dependent replacement/rightmost drop | T14 changes reads, eligibility, and boundary; structural update reuse remains provisional |
| Sequential substitution | T16 first-match source and one splice per step; not parallel commit |
| Ordinary/cyclic tag correspondence | T17/T18 queue schedule and time-scaled emulation |
| 2D/geometric/network substitution | T26/T27/T29 topology/result extensions |
| 0L/D0L/sequence homomorphism/iterated morphism | T13 aliases |
| 1L system | T14 alias, not T13 |
| Plant geometry/turtle interpretation | Rendering/geometric construction, not symbol-state mutation |
| CA/TM emulation | Compiler/relation; never a T13 implementation path |
| Continued-fraction rule stream | T42 schedule/control construction; fixed quadratic cases collapse to ordinary T13 tables |
| Digit finite automaton, incidence matrix, spectrum, compression | Derived analysis/accelerator/observation only |

## Corrected Architecture and Goal 2 Handoff

T13 is the first evidence that the shared UPDATE axis must support variable-support ordered replacement: FRONTIER selects every old word occurrence, NEIGHBORHOOD reads its symbol, RULE returns an alphabet-closed nonempty block, and UPDATE consumes all old occurrences and concatenates child blocks in source/child order. The counterexample `1 -> 10` changes support cardinality and cannot be expressed by same-locus scalar writes without padding or opaque packing.

Revised G2-T13 adds a variable-support ordered DOMAIN, occurrence loci, self reads, total morphism tables, typed block replacements, and a snapshot-parallel ordered-replacement UPDATE implementation inside the branch-free runner. Full coverage, order, newborn deferral, lineage, infinite-realization, and ragged-trace invariants remain. `ParallelReplaceConcat` may name the preset/policy, but it is not a substitution executor or second runner.

The historical API/handoff below remains evidence provenance; this section governs its executor/class classification.

## Historical Current API Fit (Superseded by Architecture Audit)

| Element | Fit | Finding |
|---|---|---|
| Finite alphabet | DIRECT/PARAMETERIZATION | `ALPHABET` can describe symbols (`simple_programs.md:200-230`) |
| Ordered sequence topology | SEMANTIC MISMATCH / PRINCIPLED EXTENSION | Current `D subseteq Z^4` rectangular field and finite `SHAPE` (`:87-198`) make coordinates/support persistent and fixed |
| Finite/infinite support choice | PRINCIPLED EXTENSION | Native support and finite realization/trace extent need separate typed objects, extending D005 |
| All old occurrences as sources | PRINCIPLED EXTENSION of D009 | Current frontier selects absolute writable next coordinates (`:1412-1510`), not snapshot occurrence handles |
| Self-symbol read | DIRECT conceptually | A one-value ordered read is sufficient, but it is relative to an occurrence rather than a dense coordinate |
| Total finite table | DIRECT conceptually | Exhaustive lookup is reusable as table semantics (`:1795-1829`) after structured word-output schema and validation |
| Replacement word result | PRINCIPLED EXTENSION | Current rule returns one alphabet value for a preselected target (`:1767-1793`) |
| Structural commit | NEW UPDATE ALGEBRA | Current parallel write/copy-forward (`:2156-2199`) preserves support/loci and cannot consume/create ordered occurrences |
| Seed | PARTIAL | Initial values exist, but fixed shape/fill selectors (`:235-290`) cannot express a word independently of capacity or an infinite stream |
| Boundary | NOT APPLICABLE for finite base | Fixed/periodic/reflective spatial reads (`:292-358`) do not define sequence ends or infinite support |
| Trace/encoding | PRINCIPLED EXTENSION | Persistent dense trajectory assumes equal slice shape; T13 needs ragged frames and explicit lineage/row-local lowering |
| Rule ID | SEMANTIC MISMATCH | Unbounded output words have no evidenced finite `rule_id` catalog |

The common protocol survives only at this level:

```text
sources = FRONTIER.select(old_state)
reads   = NEIGHBORHOOD.read(old_state, sources)
results = RULE(sources, reads)             # typed structural results
next    = UPDATE.apply(old_state, results)  # selected by spec/result algebra
```

This is not empty interface unification: assignment update preserves old loci; parallel replacement consumes a complete ordered source generation and derives new support. Each has different validation and commit laws.

## Historical Current Runtime Fit (Superseded by Architecture Audit)

- `alphabets.symbolic()` can provide a finite symbol domain (`src/ca/alphabets.py:146-177`), but an alphabet does not provide ordered support.
- `CoordinateSpace` is finite rank 0-3 (`src/ca/loci.py:31-94`); its integer proximity cannot stand in for occurrence ancestry or a changing order.
- `Dynamics.shape` is mandatory and fixed (`src/ca/specs.py:24-55`); `rollout` rejects a produced shape different from it (`rollout.py:40-91`). T13 length changes by rule and state.
- `RawEpisode.states`/`RawBatch.states` are single NumPy arrays with one spatial shape (`specs.py:58-82`); ragged sequence snapshots and lineage cannot survive this boundary.
- `canonical_coords` builds the same dense spatial coordinate grid at every time (`rollout.py:215-267`). Row-local sequence positions require an explicit ragged lowering, and are not persistent identity.
- `_rollout_states` and `_rollout_batch_states` switch on `rule.family` (`rollout.py:145-212`); adding a substitution branch would violate the shared-executor requirement.
- Only the full `time_slice` frontier executes (`frontiers.py:54-80`, `rollout.py:825-831`); no old-occurrence source frontier exists.
- `Rule`/`UpdateFn` permit `Any` but lookup execution assumes scalar alphabet outputs (`rules.py:30,64-78,262-295`). `Any` is not structural typing and cannot legalize a whole-sequence callback.
- `formulaic(fn)` (`rules.py:316-328`) would merely smuggle the morphism/update into an unrestricted function and is rejected.
- The dense spatial updater allocates/copies fixed arrays and assigns selected scalar values (`rollout.py:576-660`); it has no explicit update algebra or source coverage/order validation.
- Current seeds render fixed NumPy values (`seeds.py:39-55,879-939`), and batching presumes stackable equal shapes. Padding belongs only after a ragged raw trace.
- No current test covers a changing-length word, one-generation parallelism, ordered block concatenation, total/closed morphism validation, parent-child intervals, infinite support distinction, or rendering independence.
- Existing rollout tests instead lock fixed shapes and reject non-full frontiers (`tests/test_rollout.py:263-309,529-560`); visualization export tests assume rectangular `T/TX/TXY/TXYZ` layouts (`tests/test_viz_export.py:72-105`). These are current-scope facts, not tests to weaken.

## Historical Principles Audit (Superseded by Architecture Audit)

| Principles | T13 result |
|---|---|
| 0-2 | Fixed-locus assignment fails composition. Retain one generic orchestration but add a distinct structural update; no substitution rollout. |
| 3-4 | Frontier selects old occurrences; neighborhood reads self symbol; rule returns typed replacement; update owns coverage, consumption, concatenation, and child support. |
| 5 | Ordered values/support are visible state. Lineage is trace provenance because T13 does not read it. |
| 6-8,12 | Sequence order, snapshot address, infinite support, finite realization, ragged trace, padding, and rendering stay separate. |
| 9 | Alphabet closure, total key set, output-word domain, and update algebra are coupled; seed and renderer remain independent. |
| 10 | A neighbor-independent preset returns an ordinary structural-transition spec, not an executor branch. |
| 11 | Parallel one-generation replacement and concatenation order are defining semantics; incidence matrices/digit formulas/lazy evaluation are incidental algorithms. |
| 13-15 | Duplicate symbols, asymmetric words, source-order adversaries, changing lengths, infinite support, and lineage/render separation are mandatory tests. |
| 16 | Typed replacement plus structural update is architecture; callbacks, CA compilation, target inversion, capacity masks, and family switches are shims. |

## Historical Detailed Implementation Plan (Superseded by Architecture Audit)

1. Add explicit ordered-sequence support/state with snapshot-scoped occurrence handles; deliver finite words first while preserving a typed infinite-support extension point.
2. Generalize frontier semantics from fixed-lattice locations to sources and add `AllOccurrences` without converting occurrences into next-slice targets.
3. Reuse a self-symbol read and finite exhaustive table machinery with a structured nonempty-word output schema, total-key and alphabet-closure validation.
4. Add `ReplaceOccurrence(source,word)` and `ParallelReplaceConcat`; validate exact old-source coverage, snapshot ownership, uniqueness, order, and nonempty words.
5. Return ragged structured snapshots and optional parent-child intervals before any coordinate encoding, batching, padding, visualization, or compression.
6. Expose a strict `neighbor_independent_substitution(alphabet,table)` preset that remains independent of initial word/support realization.
7. Add independent canonical, adversarial order, growth, lineage, invalidity, observer, finite/infinite-boundary, and shared-executor conformance tests.

## Historical Goal 2 Implementation Stage (Superseded by Corrected Handoff)

### G2-T13 — Ordered sequence state, parallel replacement, and structural traces

**Dependencies:** generic typed source/read/rule/update orchestration from G2-T01/T09/T12. T13 does not depend on fixed-lattice `Assign` or control effects; it introduces a sibling update algebra.

**Implementation areas:**

- Synthesis-selected state/support module: `OrderedSequence`, finite ordered support, snapshot occurrence handles, and an explicit one-sided infinite/lazy support contract or a clearly tracked deferred implementation that does not narrow public semantics.
- `frontiers.py`: generic source frontier plus `AllOccurrences`.
- `neighborhoods.py`: `SelfSymbol` over sequence occurrences; do not reuse dense integer offsets as topology.
- `rules.py`: total alphabet-keyed tables whose output schema is validated `NonEmptyWord[Symbol]`; no mandatory integer rule ID and no callable morphism escape hatch.
- Typed results/update module: `ReplaceOccurrence` and `ParallelReplaceConcat` as a distinct update member, with exact coverage and ordered child construction.
- Generic executor: dispatch by typed update/result protocol supplied in the ordinary spec, never by catalog/family name.
- `specs.py`/preset index: `neighbor_independent_substitution(alphabet,table)` returns the ordinary structural spec; initial word and render/observation choices are episode inputs.
- Structured raw trace: ragged sequence frames and optional lineage transitions; downstream ANKoS lowering emits `(t,row_local_x,0,0,symbol)` records or a synthesis-selected lossless schema.
- Infinite seeds/realizations: closed index-keyed random/periodic fields, explicit seed/distribution/cut, lazy substituted sequences, and deterministic finite-window observation independent of query order.
- Downstream ragged batching/padding masks only after trace generation.
- New `tests/test_t13_parallel_substitution.py` plus shared structural-update/trace tests.

**Canonical and adversarial tests:**

1. Assert the exact E11 `t0..t4` trajectory and equivalent list/string symbol renaming.
2. At every step assert `|next| = sum |h[source]|` and symbol counts via the incidence matrix; cover doubling, Fibonacci-like, linear-growth, and unequal block lengths.
   - Fibonacci fixture `1 -> 10, 0 -> 1`: `1, 10, 101, 10110, 10110101` with lengths `1,2,3,5,8`.
   - Linear fixture `0 -> 01, 1 -> 1`: `0, 01, 011, 0111` with length `t+1`.
   - E24 three-color fixture exercises output lengths 3/2/1 and alphabet closure.
3. `A -> BA`, `B -> A`, `AB -> BAA`; catch source/output reversal, target sorting, and in-place/newborn rewriting.
4. Use repeated equal symbols and prove every old occurrence fires exactly once as a distinct source.
5. Assert parent-child intervals partition the next word contiguously in old-source order and reconstruct both the next word and tree observer.
6. Reject missing/duplicate table keys, outputs outside `Sigma`, empty T13 outputs, stale/duplicate/missing source results, and whole-state callbacks. None becomes identity, deletion, skip, or halt.
7. Reuse one morphism with different finite seeds, including the vacuous empty word; a self-successor is not intrinsic halt.
8. Render one trace as fixed-size rows, normalized subdivisions, trees, turn paths, and row-wrapped 2D output; rerendering cannot change evolution or state equality.
9. Round-trip ragged snapshots of different lengths without padding; if batched later, prove mask/pad never reaches execution.
10. Exercise documented infinite support through explicit lazy finite-demand oracles on `omega`; if `zeta` is implemented, verify the distinguished cut. Query windows in different orders and require identical symbols/ancestry; never silently truncate/pad or advance hidden RNG.
11. Run T01/T09/T12/T13 through the same orchestration with typed assignment/control/structural updates and statically reject family switches, callback smuggling, target inversion, CA compilation, and hidden capacities.
12. Conditional bounded-count test: for declared `(k,r)`, enumerate `(sum_(j=1)^r k^j)^k` unique nonempty tables; do not claim a canonical book rule numbering.

**Completion evidence:** canonical and adversarial tests plus the existing suite pass; state length changes natively; every old source fires once; word/source order and lineage are inspectable; infinite support is not misrepresented; no T13 branch, padding, callback, CA compiler, missing-row fallback, or value-only fixed-shape trace exists.

## Historical No-Cheating Checks

- No fixed-capacity array, fake blank symbol, pad token, mask, truncation, or preallocated maximum as program semantics.
- No deriving old sources by inverting next target coordinates and no same-index `Assign` reinterpretation.
- No sequential/in-place rewriting and no rewriting newborns in the same generation.
- No whole-state/string callback hidden behind `formula`, `Any`, or a preset.
- No family-name rollout or substitution-only executor.
- No missing-row identity fallback and no empty output admitted before T15 re-audits deletion.
- No CA/TM/tag compilation used to claim native support.
- No display scale, `[t,x,0,0]`, array slot, or path coordinate treated as persistent topology/identity.
- No ancestry hidden in state when it is only an observation, and no ancestry discarded before a requested tree trace can be formed.
- No finite tensor claimed to be an infinite random sequence; realization extent and loss are explicit.
- No behavior/property formula, incidence matrix, digit automaton, or renderer allowed to feed the transition implicitly.
- No weakened fixed-shape tests; replace the raw boundary with a truthful ragged representation.

## Completion Requirements

- [x] All aliases, captions, Notes, Index entries, splits, variants, duplicates, and false positives are resolved.
- [x] All unique known construction-relevant excerpts have exact canonical provenance.
- [x] Ordered state/support, sources, reads, replacement words, parallel commit, order, seed, successor, lineage, and observables are reconstructed.
- [x] Canonical rules/trajectories and structural invariants have independent conformance oracles.
- [x] Current API/runtime/test fit and T01/T09/T12 reuse/divergence are explicit.
- [x] Goal 2 implementation/conformance handoff is implementation-ready.
- [x] Global ledgers and plan are reintegrated and all verification checks pass.

## Architecture-Reclosed Stage Result

**COMPLETE.** T13 requires an ordered block-replacement UPDATE policy because native rules such as `a -> aa` change support in one event. That is a typed UPDATE-axis extension inside the common runner, not a substitution executor or a separate top-level algebra; the corrected handoff above governs.

## Historical Stage Results (Evidence Retained; Architecture Superseded)

T13 is complete with zero unresolved evidence candidates. It forces the first principled split in update algebra. The shared transition shell remains useful, but fixed-locus `Assign` cannot express ordered replacement: `ParallelReplaceConcat` consumes every old occurrence exactly once and creates the next support by source-order concatenation of typed nonempty words. Finite canonical evolution, explicit infinite-sequence support/cuts, ragged trace, lineage, stochastic/rule-stream variants, and rendering are separated. T01/T09/T12 remain valid fixed-support members and no prior stage is reopened. Next: T16 Sequential Substitution Systems.
