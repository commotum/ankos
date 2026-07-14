# 30-T14-CONTEXTUAL-SUBSTITUTION

Status: **IN PROGRESS — SOURCE, ASSET, AND ARCHITECTURE AUDITS OPEN**

## Current Facts

- T14 is CSV line 15, Neighbor-Dependent Substitution Systems. `CA-Types.md` is search vocabulary, not primary evidence.
- The direct Chapter 3 construction is a finite ordered word whose eligible elements are replaced in parallel by nonempty words selected from the element's own color and the color immediately to its right (`BOOK:1018-1026`).
- The direct Notes implementation is executable and more precise: it partitions the old word into every overlapping adjacent pair, replaces every pair from one old snapshot, flattens the replacement words in pair order, and uses that concatenation as the complete successor (`BOOK:12109-12115`).
- The first displayed rule is exactly `11 -> 01`, `10 -> 10`, `01 -> 0`, `00 -> 01`. The plate and Notes agree. The displayed seed is visually `0110`; the extracted Notes sentence loses the seed expression after “is”, so the asset audit must bind that recovery rather than silently repairing the text.
- The rightmost old occurrence is not an emitting source because it has no right neighbor. It is still read by the preceding source. It is absent from the successor unless emitted by some eligible pair; this is the source-defined “rightmost element is always dropped” behavior (`BOOK:1022`).
- `SS2EvolveList` defines the zero-source case structurally: a word of length zero or one has no adjacent pair, so its successor is the empty concatenation. This is not an empty rule-table output and does not transfer T15's creation/destruction validator into T14.
- DOMAIN is discrete `t+1D`. The finite ordered word and its occurrence topology are CONFIGURATION, not DOMAIN.
- T13 already evidenced an ordered, snapshot-parallel block-emission UPDATE axis. T14 is provisionally a parameterization of its ordered emission/concatenation kernel with a `HasRightNeighbor` frontier and a two-occurrence read, not a new executor or top-level semantic state class.
- Overlapping adjacent reads do not imply overlapping writes: each eligible anchor produces one ordered block, and UPDATE concatenates blocks in anchor order. Newborn elements do not participate until the next event.
- The current `simple_programs.md` and `src/ca` realization is fixed-shape and CA-shaped. Architecture-audit decisions, rather than those historical limitations, govern Goal 2: the library is a broad SimpleProgram library with branch-free `FRONTIER/NEIGHBORHOOD/RULE/UPDATE` execution.
- Goal 1 changes only `goal-1/`. Runtime implementation and tests remain Goal 2 work.

## Updated Assumptions

- The strict base profile is provisionally a total, alphabet-closed table `h : Sigma^2 -> Sigma+`. Empty replacement words remain T15's separate evidence question.
- Source order is semantic. For old word `w[0:n]`, eligible anchors are exactly `0, ..., n-2`; result blocks are concatenated in that order.
- The right boundary is an eligibility condition evidenced by the construction, not a generic menu containing padding, wrapping, reflection, a blank symbol, or a hidden sentinel.
- There is no left-boundary read in the displayed base system. Wider or two-sided L-system contexts must remain variants until primary evidence establishes their exact schedule and boundary laws.
- The Chapter 3 statement that the two displayed trajectories never decrease is not yet treated as a universal validator. The exact first rule maps the valid seed `01` from length two to length one; the source claim is therefore about the displayed evolutions or their intended regime unless further evidence resolves it.
- The empty word can be an absorbing successor under the Notes operator. “No active sources” has construction-specific meaning under D024 and must not be globally translated to halt, error, or stutter.
- T13's public `AllOccurrences`/complete-singleton-coverage preset is too narrow to rename as T14. The reusable base, if confirmed, is the lower ordered emission/concatenation kernel plus construction-specific frontier and validation presets.
- A one-step CA encoding or emulation is evidence of a commuting relation, not permission to execute T14 through a CA compiler.

## Big Picture Objective

Reconstruct neighbor-dependent substitution systems from complete primary evidence and determine the smallest lossless branch-free fit. In particular, test whether overlapping contextual reads, right-edge source eligibility, and ordered variable-length emissions are parameterizations of the T13 axes or expose a concrete failure of the existing ordered replacement algebra.

## Catalog Identity

- Stable ID: T14.
- CSV line: 15.
- Catalog name: Neighbor-Dependent Substitution Systems.
- Taxonomy section: 14.
- Construction kind: deterministic parallel transition construction over a dynamically sized ordered symbol configuration.
- Direct aliases found so far: neighbor-dependent substitution system, 1L system, D1L system.
- Search vocabulary in progress: neighbor dependent/neighbor-dependent, contextual substitution, adjacent pair, immediate/right neighbor, rightmost drop, `SS2EvolveList`, `Partition[...,2,1]`, 1L/D1L, L system, substitution systems emulating cellular automata, one-element dependence, generalized substitution, context-sensitive/context-dependent rewriting, and actual Index routes.

## Search Log

The authoritative exhaustive counts, digests, split reverse closure, candidate dispositions, and zero-remainder assertion will be generated by `30-T14-source-oracle.py`. The audit is still open; the following are established seed searches, not an exhaustiveness claim.

```text
rg -n -i "neighbor[- ]dependent|rightmost element|immediately to its right|1L systems|substitution systems whose rules depend" \
  ref/A-New-Kind-of-Science
rg -n "Page 85|page 85|SS2EvolveList|Partition\[#.*, 2, 1\]|D1L systems|one-element-dependence" \
  ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
rg -n "Neighbor-dependent substitution systems|Substitution systems" \
  ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
```

Candidate regions currently retained for full disposition include:

| Region | Provisional disposition |
|---|---|
| `BOOK:1018-1026` | direct definition, plate, display convention, right-edge rule, and observed growth |
| `BOOK:1028-1052` | T15 continuation and CA-like relation; retain only construction boundaries actually shared by T14 |
| `BOOK:1058-1062` | ordinary parallel versus sequential schedule contrast |
| `BOOK:12109-12115` | exact T14 table and executable one-step operator; extracted seed defect |
| `BOOK:12249-12251` | L-system history and 0L/1L alias boundary |
| `BOOK:8022-8028` | CA-emulation relation and one-symbol-output restriction |
| `BOOK:2350` | T28 two-dimensional contextual analogy, not base T14 semantics |
| `BOOK:5944-5952` | generalized-substitution/causal relation; applicability still under review |
| `BOOK:20828,21068,21652,22144` | actual Index aliases and routes to follow |

No candidate will be called resolved until the source oracle closes aliases, captions, Notes, Index, split files, and cross-references.

## Book Excerpts

### Excerpt 1: replacement reads current and immediate-right colors

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:1018`
- Context: Chapter 3, “Substitution Systems”.
- Establishes: pair-context rule input and the contrast with T13's self-only read.

> To get behavior that is more complicated than simple nesting, it follows therefore that one must consider substitution systems whose rules depend not only on the color of a single element, but also on the color of at least one of its neighbors. The pictures below show examples in which the rules for replacing an element depend not only on its own color, but also on the color of the element immediately to its right.

### Excerpt 2: rendering is not alignment semantics; the rightmost source is absent

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:1022`
- Context: caption for `_page_100_Picture_3.jpeg`.
- Establishes: row-wise rescaling is an observer and no rule fires at the rightmost occurrence.

> Rules of this kind cannot readily be interpreted in terms of simple subdivision of one element into several. And as a result, there is no obvious way to choose what size of box should be used to represent each element in the picture. What I do here is simply to divide the whole width of the picture equally among all elements that appear at each step. Note that on every step the rightmost element is always dropped, since no rule is given for how to replace it.

### Excerpt 3: displayed rules use nonempty blocks

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:1024-1028`
- Context: discussion immediately after the page-85 examples.
- Establishes: the two displayed examples precede the explicit disappearance extension.

> One feature of both examples, however, is that the total number of elements never decreases from one step to the next. The reason for this is that the basic rules we used specify that every single element should be replaced by at least one new element.
>
> It is, however, also possible to consider substitution systems in which elements can simply disappear.

### Excerpt 4: exact first rule and executable generation operator

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:12109-12115`
- Context: Notes, “Substitution Systems — Implementation”.
- Establishes: total binary-pair lookup, overlapping snapshot partitions, ordered flattening, and the source extraction defect after the seed lead-in.

> For a neighbor-dependent substitution system such as the first one on page 85 the rule can be given as
>
> `{{1,1}->{0,1}, {1,0}->{1,0}, {0,1}->{0}, {0,0}->{0,1}}`

```text
SS2EvolveList[rule_, init_List, t_Integer] :=
  NestList[Flatten[Partition[#, 2, 1] /. rule] &, init, t]
```

> where the initial condition for the first example on page 85 is

### Excerpt 5: 1L is the historical alias

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:12251`
- Context: Notes history.
- Establishes: 0L/T13 versus 1L/T14 identity.

> So-called 0L systems correspond to my neighbor-independent substitution systems; 1L systems correspond to the neighbor-dependent substitution systems on page 85.

### Excerpt 6: restricted one-output rows directly emulate CAs

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:8022-8028`
- Context: Chapter 11, emulation relations.
- Establishes: a length-one-output restriction has one-step CA-like behavior, but is not the definition of general T14.

> But if one generalizes to neighbor-dependent substitution systems then it immediately becomes very straightforward to emulate cellular automata ... The systems shown are simple examples of neighbor-dependent substitution systems with highly uniform rules always yielding just one cell and corresponding quite directly to cellular automata.

### Excerpt 7: actual Index routes

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:20828,21068,21652,22144`
- Context: Index.
- Establishes: 1L/D1L and neighbor-dependent routes, page scope 85–87, and broader substitution cross-references.

> 1L systems, 85–88, 893 ... D1L systems, 85–87 ... Neighbor-dependent substitution systems, 85–87 ... Substitution systems ... neighbor-dependent, 85–87.

## Construction Model

### Strict finite base

For a finite old word

```text
W = (w_0, ..., w_{n-1}) in Sigma*
```

and a total contextual table

```text
h : Sigma x Sigma -> Sigma+
```

the source-defined event is

```text
active  = FRONTIER.select(W)
        = (Occurrence(0), ..., Occurrence(n-2))

reads_i = NEIGHBORHOOD.read(W, Occurrence(i))
        = (w_i, w_{i+1})

result_i = RULE(Occurrence(i), reads_i)
         = EmitWord(source=i, word=h(w_i, w_{i+1}))

next = UPDATE.apply(W, active, results)
     = result_0.word ++ ... ++ result_(n-2).word
```

All reads use the immutable old word. Results are ordered source emissions, not assignments into an old or preallocated target coordinate set. The old rightmost occurrence participates in `reads_(n-2)` but has no source result of its own. The complete next support is derived from the concatenated emissions; no old occurrence is copied forward implicitly.

For `n < 2`, `active` and `results` are empty and the Notes expression yields the empty concatenation. Thus `[] -> []` and `[a] -> []`. This is a defined vacuous structural event, not a missing rule and not evidence that a pair-table row may emit epsilon.

### Exact first example

```text
Sigma = {0,1}
h(1,1) = 01
h(1,0) = 10
h(0,1) = 0
h(0,0) = 01
seed = 0110                    # plate recovery; asset binding pending

t0 = 0110
t1 = h(0,1) ++ h(1,1) ++ h(1,0)
   = 0 ++ 01 ++ 10
   = 00110
```

The asset audit will freeze the full visible trajectory and verify that the recovered seed/rule glyphs commute with the Notes operator.

### State and invariants

- DOMAIN: discrete `t+1D`.
- CONFIGURATION: finite ordered occurrences carrying symbols; dynamic cardinality and sequence order are semantic.
- ALPHABET: finite `Sigma`; the direct examples use `Bit`.
- CONTROL: none.
- FRONTIER: ordered old occurrences satisfying `HasRightNeighbor`.
- NEIGHBORHOOD: ordered `(Self,Right)` occurrence read from one old snapshot.
- RULE result: typed nonempty `EmitWord` over the same alphabet.
- UPDATE: atomic ordered concatenation of all validated source emissions; it derives the whole successor support.
- Successor algebra: one deterministic successor for a valid total program, including the vacuous empty concatenation.
- Boundary: right-edge source ineligibility; no left-edge special case for the direct profile.
- Seed: arbitrary valid finite word semantically; `0110` is the recovered direct example pending physical closure.
- Observers: equal-total-width rows, fixed-size boxes, lineage polygons, and CA-like grids are representations, not state.

### Conflicts and lineage

Adjacent sources overlap only in their old reads. They do not claim an old target span or persistent coordinate. UPDATE validates one result for each selected source and concatenates by source order; consequently there is no write collision policy to invent. Optional lineage associates every emitted child interval with its anchor occurrence. The right-context occurrence can influence a block without thereby becoming that block's parent.

### Variants and relations under audit

| Variant or relation | Current disposition |
|---|---|
| Different finite seeds | seed parameterization |
| Wider left/right context | possible L-system neighborhood parameterization; exact source evidence pending |
| Length-one output for every pair | restriction that directly realizes a one-sided local CA rule away from the edge |
| Empty pair output | T15 creation/destruction extension, not strict T14 |
| Right pad/wrap/blank/reflection | taxonomy speculation unless primary evidence is found |
| Infinite word | support/boundary variant requiring an explicit end/origin model; not inferred from finite T14 |
| Sequential first-match replacement | T16 schedule, not a T14 option |
| Two-dimensional contextual substitution | T28 topology/neighborhood extension |
| CA emulation | explicit mapping/relation; never an execution fallback |

## Current API Fit

The historical `simple_programs.md` is CA-shaped, while `architecture-audit.md` supplies the governing broad axes. Final line citations and labels remain subject to the architecture audit.

| Construction element | Fit | Finding |
|---|---|---|
| DOMAIN | `DIRECT` | discrete `t+1D`; word topology belongs to CONFIGURATION |
| Finite symbol alphabet | `DIRECT` / `PARAMETERIZATION` | reuse a generic finite alphabet; semantic pair roles do not require new alphabet classes |
| Dynamic ordered configuration | `DIRECT` from T13 base | same finite-word support/topology and ragged trace requirements |
| Eligible anchored occurrences | `PARAMETERIZATION` | restrict the generic occurrence frontier by `HasRightNeighbor`; do not invent a contextual-system frontier executor |
| `(Self,Right)` read | `PARAMETERIZATION` | ordered occurrence access pattern widens T13's self read |
| Pair-to-word table | `PARAMETERIZATION` | same total finite lookup and `EmitWord` result shape with input arity two |
| Ordered structural commit | `PARAMETERIZATION` provisionally | reuse the T13 ordered emission/concatenation kernel; its T13 complete-coverage preset remains stricter |
| Rightmost drop | `PARAMETERIZATION` | follows from frontier eligibility plus complete successor derivation; not an epsilon sentinel row |
| Equal-width rendering | `NOT APPLICABLE` to semantics | downstream observer only |
| Rule number | `SEMANTIC MISMATCH` absent an explicit output-length bound | no source-defined integer codec found so far |

## Current Runtime Fit

- `src/ca/alphabets.py` supplies finite scalar alphabets but not products/tags or ordered configuration topology: alphabet reuse is partial representation reuse, not a T14 implementation.
- `src/ca/loci.py` provides dense rank-0..3 coordinate spaces/selectors. Integer proximity cannot stand in for dynamic occurrence order or ancestry.
- `src/ca/specs.py` requires one fixed `shape`; `RawEpisode`/`RawBatch` use stackable arrays. T14 requires ragged native frames before optional encoding/padding.
- `src/ca/frontiers.py` currently exposes a dense next-time slice, not ordered old occurrence anchors with `HasRightNeighbor` eligibility.
- `src/ca/neighborhoods.py` reads geometric offsets on fixed arrays; Goal 2 needs typed occurrence-relative access while retaining the same read-axis responsibility.
- `src/ca/rules.py` permits `Any`/callables historically, but T14 must use a closed serializable pair table returning validated alphabet words.
- `src/ca/rollout.py` assumes fixed-shape scalar writes and contains family dispatch. Goal 2 must implement the common branch-free runner and typed UPDATE dispatch by result/algebra, not add a T14 rollout branch.
- Existing fixed-array boundary functions must not be reused to pad the word's right edge. The direct boundary is no eligible source.

## Principles Audit

- Principle 0: the provisional T13 coverage invariant is reopened at its reusable-kernel boundary rather than patched with a fake rightmost result.
- Principles 1–3: the catalog label creates no executor. T14 changes source eligibility and reads; UPDATE remains ordered emission/concatenation unless a counterexample disproves that reuse.
- Principle 4: RULE returns a typed `EmitWord`, not an object-array scalar or unrestricted callback.
- Principles 5–8: the complete dynamic word is state; row-local coordinates, box widths, polygons, and padded tensors are representations.
- Principles 9–10: `HasRightNeighbor`, `(Self,Right)`, total pair table, and strict nonempty outputs are composable presets/invariants, not flags selecting hidden family paths.
- Principle 11: snapshot parallelism, source order, and right-edge ineligibility are defining semantics and stay in the declared axes.
- Principles 12–16: ragged trace encoding remains downstream; no CA compiler, fixed capacity, callback, family branch, or sentinel is admitted.

The strongest current reuse statement is a one-step identity mapping between the direct Notes operator and the generic ordered-emission construction. For every finite word and valid table, both select the same ordered adjacent-pair anchors, read the same old pairs, produce the same blocks, and concatenate them in the same order. The semantic oracle must test this commuting square independently rather than invoke the Notes expression as its implementation.

## Detailed Implementation Plan

1. Freeze the exhaustive monolith/split source union, retained/governed/excluded dispositions, actual Index boundary, aliases, cross-references, and content hashes in `30-T14-source-oracle.py`.
2. Freeze the source-bound asset fixed point, reference closure, hashes, C/O/R/X classification, and exact page-100 rule/seed/trajectory facts in `30-T14-asset-oracle.py`.
3. Freeze direct and generic one-step semantics, snapshot/newborn deferral, source order, boundary, zero-source behavior, and adversarial non-reuse checks in `30-T14-semantic-oracle.py`.
4. Resolve whether D019 should name a generic `OrderedEmissionConcat` base with T13/T14 presets, or whether a concrete counterexample requires a distinct schedule. Do not add a new algebra without that counterexample.
5. Complete the API/runtime fit, Goal 2 handoff, no-cheating tests, source/asset/semantic root and `/tmp` checks, optimized-mode fail-closed checks, Markdown/diff/scope gates, and independent hostile review.
6. Integrate only closed findings into `0-plan.md`, `evidence-index.md`, and `design-ledger.md`; reopen any contradicted prior stage before advancing.

## Goal 2 Implementation Stage

### Provisional G2-T14 objective

Add a strict neighbor-context substitution preset by composing the generic finite ordered configuration, occurrence selectors, ordered reads, total structured lookup tables, typed word emissions, and ordered structural UPDATE inside the shared runner.

### Dependencies

- corrected broad SimpleProgram runner and typed `StepResult`;
- T13 finite ordered configuration, occurrence identity/order, word result validation, ragged trace, and ordered emission kernel;
- D024 construction-specific empty-frontier outcomes;
- generic finite alphabet/table machinery.

### Proposed public composition

```text
Configuration = FiniteWord[Symbol]
Frontier      = OccurrencesWhere(HasRelative(+1))
Neighborhood  = OccurrenceOffsets((0,+1))
Rule          = TotalTable[Pair[Symbol,Symbol], NonEmptyWord[Symbol]]
Update        = OrderedEmissionConcat(derive_complete_successor=True)
Seed          = FiniteWordSeed
```

The names are design roles, not required one-class-per-line commitments. Goal 2 should prefer generic typed products, predicates, table schemas, and validated presets.

### Conformance tests required

- exact first page-85 rule/seed evolution for every asset-visible generation;
- independent `Partition(old,2,1)` commuting oracle over exhaustive short binary words and all bounded nonempty binary pair tables;
- snapshot/newborn adversary where in-place iteration produces a different row;
- source-order and block-internal-order adversaries;
- explicit `[a] -> []` and `[] -> []` behavior without halt/error invention;
- rightmost context participates in the last read but emits no separate block;
- rule totality, alphabet closure, pair arity, nonempty output, duplicate row, and malformed source-result rejection;
- length-one-output restriction commuting with the corresponding one-sided local CA step on a declared finite interior, while proving that no CA compiler is used for native execution;
- ragged trace and optional lineage round trips without padding as state;
- serialization round trip with no callbacks, `Any`, family tags controlling execution, hidden boundary symbol, or duplicated rule table.

### Completion evidence

One shared runner executes T13 and T14 through data-selected generic components; the exact direct examples pass; the generic/direct step square commutes; no runtime family switch or T14 executor exists; and the public validator preserves the strict evidence boundary rather than exposing unsupported generic boundary policies.

## No-Cheating Checks

- Reject an implementation that preallocates a fixed maximum word, pads the right context, or treats padding as alphabet state.
- Reject a rule/function that receives the whole word or source index when only the pair read is declared.
- Reject in-place left-to-right rewriting; every read must come from the same old snapshot.
- Reject sorting outputs, target-coordinate assignment, or collision callbacks; result order is source order then child order.
- Reject a fabricated right-boundary table row such as `(symbol,Boundary) -> epsilon` in the strict base preset.
- Reject a T14-specific rollout, family switch, callback, object-cell packing, or CA-compilation fallback.
- Reject treating display width, polygon alignment, row-local x coordinates, or asset crop limits as native support.
- Reject universal nondecreasing-length validation unless the source audit resolves the direct `01 -> 0` counterexample.
- Require all source/asset/semantic oracles to fail closed under `python -O` and when invoked outside the repository root.

## Completion Requirements

- [ ] Exhaustive source oracle passes with zero unresolved candidate and complete split/Index/alias closure.
- [ ] Source-bound asset fixed point closes with all references and hashes classified.
- [ ] Direct rules, seed, trajectories, and display-only facts are independently decoded and source-bound.
- [ ] Construction model covers finite words, right-edge eligibility, empty/singleton cases, variants, and relations without invention.
- [ ] Semantic oracle proves direct/generic one-step commutation and adversarial schedule/order/boundary properties.
- [ ] The smallest reusable base construction is decided with evidence; any new algebra has a concrete counterexample.
- [ ] API/runtime fit and implementation-ready Goal 2 handoff cite actual definitions and tests.
- [ ] Independent hostile review has no unresolved blocker, major, or minor finding.
- [ ] Source, asset, semantic, Markdown, diff, scope, status/coverage, and repository-test gates pass.
- [ ] `0-plan.md`, `evidence-index.md`, and `design-ledger.md` are integrated consistently.

## Stage Results

In progress. The direct evidence already strongly supports the user's architecture correction: T14 is the T13 ordered structural pipeline with a contextual access pattern and a right-neighbor eligibility restriction. The open work is to prove exhaustive evidence/asset closure and decide whether D019's reusable base should be stated more generally than T13's complete singleton-source preset.
