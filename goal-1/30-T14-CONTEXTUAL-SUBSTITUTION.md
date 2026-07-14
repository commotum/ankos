# 30-T14-CONTEXTUAL-SUBSTITUTION

Status: **IN PROGRESS — EVIDENCE, ASSETS, SEMANTICS, AND INTEGRATION CLOSED; HOSTILE REVIEW AND FINAL GATES OPEN**

## Current Facts

- T14 is CSV line 15, Neighbor-Dependent Substitution Systems. `CA-Types.md` is search vocabulary, not primary evidence.
- The frozen 13-query source audit closes 308 unique lines at 231 pre-Index and 77 actual-Index. It retains 27 query hits plus 13 governed continuations, excludes 204 pre-Index false positives, reverse-closes all 17 split documents, and leaves zero source candidate unresolved.
- The source-bound asset fixed point contains 22 unique JPEGs at `C/O/R/X=1/0/16/5`, with 44 exact monolith/split references and 22 distinct hashes. BOOK:1020 is the only native T14 raster; all other included assets are typed relations or adjacency controls.
- The direct Chapter 3 construction is a finite ordered word whose eligible elements are replaced in parallel by nonempty words selected from the element's own color and the color immediately to its right (`BOOK:1018-1026`).
- The direct Notes implementation is executable and more precise: it partitions the old word into every overlapping adjacent pair, replaces every pair from one old snapshot, flattens the replacement words in pair order, and uses that concatenation as the complete successor (`BOOK:12109-12115`).
- The first displayed rule is exactly `11 -> 01`, `10 -> 10`, `01 -> 0`, `00 -> 01`. The plate and Notes agree. The displayed seed is `0110`; the extracted Notes sentence loses the seed expression after “is”, so the hash-bound raster supplies a transparent recovery rather than a silent text repair.
- The second raster-only rule is `11 -> 00`, `10 -> 11`, `01 -> 1`, `00 -> 0`, again from seed `0110`. Its first four rows are independently reproduced by the Notes operator.
- The rightmost old occurrence is not an emitting source because it has no right neighbor. It is still read by the preceding source. It is absent from the successor unless emitted by some eligible pair; this is the source-defined “rightmost element is always dropped” behavior (`BOOK:1022`).
- `SS2EvolveList` defines the zero-source case structurally: a word of length zero or one has no adjacent pair, so its successor is the empty concatenation. This is not an empty rule-table output and does not transfer T15's creation/destruction validator into T14.
- DOMAIN is discrete `t+1D`. The finite ordered word and its occurrence topology are CONFIGURATION, not DOMAIN.
- T13 already evidenced an ordered, snapshot-parallel block-emission UPDATE axis. The 164,592-case commuting proof confirms that T14 parameterizes its `OrderedGenerationConcat` kernel with a `HasRightNeighbor` frontier and a two-occurrence read; it adds no UPDATE algebra, executor, or top-level semantic state class.
- Overlapping adjacent reads do not imply overlapping writes: each eligible anchor produces one ordered block, and UPDATE concatenates blocks in anchor order. Newborn elements do not participate until the next event.
- The current `simple_programs.md` and `src/ca` realization is fixed-shape and CA-shaped. Architecture-audit decisions, rather than those historical limitations, govern Goal 2: the library is a broad SimpleProgram library with branch-free `FRONTIER/NEIGHBORHOOD/RULE/UPDATE` execution.
- Goal 1 changes only `goal-1/`. Runtime implementation and tests remain Goal 2 work.

## Updated Assumptions

- The strict base profile is a total, alphabet-closed table `h : Sigma^2 -> Sigma+`. Empty replacement words remain T15's separate evidence question.
- Source order is semantic. For old word `w[0:n]`, eligible anchors are exactly `0, ..., n-2`; result blocks are concatenated in that order.
- The right boundary is an eligibility condition evidenced by the construction, not a generic menu containing padding, wrapping, reflection, a blank symbol, or a hidden sentinel.
- There is no left-boundary read in the displayed base system. Wider or two-sided L-system contexts must remain variants until primary evidence establishes their exact schedule and boundary laws.
- The Chapter 3 statement that the two displayed trajectories never decrease is trajectory-scoped, not a universal validator. The exact first rule maps the valid seed `01` from length two to length one.
- The exact zero-source profile is `[] -> []` and `[a] -> []`. “No active sources” has construction-specific meaning under D024 and must not be globally translated to halt, error, or a copy-forward stutter.
- T13's public `AllOccurrences`/complete-singleton-coverage invariant belongs to its preset, not the reusable UPDATE base. The base validates exact coverage of the selected ordered frontier and rebuilds the complete successor solely from those emissions.
- A one-step CA encoding or emulation is evidence of a commuting relation, not permission to execute T14 through a CA compiler.

## Big Picture Objective

Reconstruct neighbor-dependent substitution systems from complete primary evidence and determine the smallest lossless branch-free fit. In particular, test whether overlapping contextual reads, right-edge source eligibility, and ordered variable-length emissions are parameterizations of the T13 axes or expose a concrete failure of the existing ordered replacement algebra.

## Catalog Identity

- Stable ID: T14.
- CSV line: 15.
- Catalog name: Neighbor-Dependent Substitution Systems.
- Taxonomy section: 14.
- Construction kind: deterministic parallel transition construction over a dynamically sized ordered symbol configuration.
- Direct aliases: neighbor-dependent substitution system, 1L system, D1L system.
- Search vocabulary: neighbor dependent/neighbor-dependent, substitution system, adjacent pair, immediate/right neighbor, rightmost drop, `SS2EvolveList`, `Partition[...,2,1]`, 1L/D1L/L system, page 85, CA emulation, parallel replacement, generalized substitution, contextual/context-sensitive candidates, and boundary alternatives.

## Search Log

`30-T14-source-oracle.py` freezes 13 case-insensitive line queries, content hashes, and every disposition. Per-query counts are:

| Query | total | pre-Index | actual-Index |
|---|---:|---:|---:|
| Q00 direct name | 7 | 6 | 1 |
| Q01 broad substitution family | 288 | 213 | 75 |
| Q02 1L/D1L/L-system aliases | 9 | 4 | 5 |
| Q03 executable implementation | 1 | 1 | 0 |
| Q04 contextual-dependence wording | 12 | 12 | 0 |
| Q05 right-edge wording | 2 | 2 | 0 |
| Q06 growth/deletion/one-output wording | 3 | 3 | 0 |
| Q07 page/index routes | 8 | 5 | 3 |
| Q08 exact four-row table | 2 | 2 | 0 |
| Q09 parallel word replacement | 1 | 1 | 0 |
| Q10 neighbor-dependent growth | 1 | 1 | 0 |
| Q11 contextual/context-sensitive alias control | 0 | 0 | 0 |
| Q12 pad/wrap/boundary-symbol control | 0 | 0 | 0 |

After union and deduplication:

- query union: 308, digest `17902ddb945809f7b2c66adbb5372a20a4fedb723093891db54dc6f28a6ef484`;
- pre-Index: 231, digest `a5b2d7348d117d40130205dc7d708a4857bcb170ec85cb59eb6a5af0f45a4fb7`;
- actual Index: 77, digest `3ad1376a743e1cc0193b21c27c06b51410da403e3ec5fbcee9f6e05f49c75462`;
- matched retained: 27; governed continuations: 13; final retained: 40, digest `24213ee950c26341f210496994a3b91202ccb5c560c1b078192ee85a8b33410a`;
- excluded pre-Index candidates: 204, digest `0721f005cf8d1ec233b98b04bd89222b87f18bb1f5533ac6615fb19f6902b2ef`;
- seven relevant Index lines and 70 dispositioned Index false positives.

```text
rg -n -i "neighbor[- ]dependent|rightmost element|immediately to its right|1L systems|substitution systems whose rules depend" \
  ref/A-New-Kind-of-Science
rg -n "Page 85|page 85|SS2EvolveList|Partition\[#.*, 2, 1\]|D1L systems|one-element-dependence" \
  ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
rg -n "Neighbor-dependent substitution systems|Substitution systems" \
  ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
```

Candidate disposition is closed:

| Region | Final disposition |
|---|---|
| `BOOK:1018-1026` | direct definition, plate, display convention, right-edge rule, and observed growth |
| `BOOK:1028-1052` | T15 continuation and CA-like relation; retain only construction boundaries actually shared by T14 |
| `BOOK:1058-1062` | ordinary parallel versus sequential schedule contrast |
| `BOOK:12109-12115` | exact T14 table and executable one-step operator; extracted seed defect |
| `BOOK:12249-12251` | L-system history and 0L/1L alias boundary |
| `BOOK:8022-8028` | CA-emulation relation and one-symbol-output restriction |
| `BOOK:2350` | T28 two-dimensional contextual analogy, not base T14 semantics |
| `BOOK:5928-5954,16404` | generalized left-to-right nonoverlap schedule relation; not T14's overlapping contextual reads |
| `BOOK:12136` | extraction-truncated neighbor-dependent growth observation; no execution primitive inferred |
| `BOOK:13806-13810` | T28 two-dimensional sibling and implementation, not base T14 |
| `BOOK:18788` | encoder use only |
| `BOOK:20828,21068,21422,21461,21652,22114,22144` | actual Index aliases/routes, all followed |

All 17 split documents are hash-bound. The 306 split query records reverse-join as 276 exact and 30 explicit extraction variants. Retained evidence reverse-joins as 29 exact lines, ten explicit variant witnesses, and the one documented split omission at BOOK:12115. Atlas has four generic summary hits and no direct or executable T14 evidence. Zero candidate remains unresolved.

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

### Excerpt 8: dynamic ordered support and parallel word schedule

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:982-986,1058-1062`
- Context: Chapter 3 construction and sequential-system contrast.
- Establishes: the configuration is a variable-cardinality ordered word and the native schedule replaces all eligible old elements in one generation.

> Substitution systems, however, are set up so that the number of elements can change. In the typical case ... one has a sequence of elements ... and at each step each one of these elements is replaced by a new block of elements.
>
> the state of a substitution system at a particular step can be represented by the string ABBBABA ... these systems operate in parallel on all the elements that exist in the string at each step.

### Excerpt 9: order is semantic; displayed positions are not identity

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:1046`
- Context: multicolor creation/destruction continuation.
- Establishes: sequence order survives changing row-local positions.

> on each line in each picture, only the order of elements is ever significant: ... a particular element may change its position as a result of the addition or subtraction of elements to its left.

### Excerpt 10: generalized left-to-right block replacement is a different schedule

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:5928,5944-5954,16404`
- Context: generalized substitution/causal systems and Notes implementation.
- Establishes: multi-element matches are selected by a left-to-right nonoverlap scan, unlike T14's overlapping read windows; they cannot supply T14 conflict semantics.

> one again scans from left to right, but now one performs all replacements that fit ... every replacement that is found to fit in a left-to-right scan is performed at each step.
>
> using different schemes yields quite different behavior—and a quite different causal network.

### Excerpt 11: two-dimensional contextual substitution is a sibling

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:2350-2356,13806-13810`
- Context: Chapter 5 and Notes, page 192.
- Establishes: T28 changes configuration topology and neighborhood geometry; its `Partition[list,{2,2},1,-1]` operator is not the T14 base.

> the replacement for a particular element at a given step can depend not only on the characteristics of that element itself, but also on the characteristics of other neighboring elements.

```text
Flatten2D[Partition[list, {2, 2}, 1, -1] /. rule]
```

### Excerpt 12: relation and observation boundaries

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:12136,18788`
- Context: extraction-truncated growth Note and encoding discussion.
- Establishes: neighbor dependence permits richer growth and can be used inside an encoder, but neither statement defines a new transition component.

> For neighbor-dependent rules, any form of growth can in principle
>
> types of encoding functions that are at least somewhat powerful yet can realistically be sampled systematically may perhaps include those based on neighbor-dependent substitution systems

The first quotation is deliberately left truncated exactly as extracted; no missing continuation is invented.

## Asset Ledger

`30-T14-asset-oracle.py` starts from the 40-line retained source set and closes a radius-four set `C4=17` plus five governed companions. Its 22-asset universe is:

| Class | Lines | Meaning |
|---|---|---|
| C | `1020` | native page-100 pair tables plus their evolutions |
| O | none | the composite native raster is classified by its stronger construction role |
| R | `988,990,1008,1014,1034,1036,1044,1048,1066,2354,2362,5932,5934,5950,5958,8026` | T13/T15/T16/T28/general-rewrite/CA-emulation relations |
| X | `8018,12134,13800,13802,13804` | mechanical adjacency controls |

Every asset has exactly one monolith reference, one split reference, one physical file, and one unique hash: 44 references and 22 hashes total. The strict native plate is 912 by 614 pixels, 106,884 bytes, SHA-256 `25df45fbfcb5f0f57d18779b2b8af7cb31c9a9400d81b69779663c448882d183`.

The plate establishes both `0110` seeds, the two exact tables, their first four rows, equal-total-width row rendering, and open-right source eligibility. It shows no padding, wrapping, sentinel, finite capacity, or alternate boundary. Rule 2 remains raster-only.

The relation raster at BOOK:8026 is independently hash-bound as `66295968a40bcb9140d67e3fba6ec15420849d298afac6ddf6583b5108f9c51a`. Its left strip has four ordered binary-pair inputs, its right strip has nine ordered three-color-pair inputs, and every row emits one cell. It is not an eight-row native width-three elementary-CA table; rules 90 and 30 are the emulation targets.

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
seed = 0110                    # hash-bound plate recovery

t0 = 0110
t1 = h(0,1) ++ h(1,1) ++ h(1,0)
   = 0 ++ 01 ++ 10
   = 00110
```

The bound trajectory begins:

```text
rule 1: 0110 -> 00110 -> 0100110 -> 0100100110
rule 2: 0110 -> 10011 -> 110100 -> 00111110
```

Rule 1's text, raster, and independently evaluated pipeline agree. Rule 2's raster glyphs and lineage polygons agree with its independently evaluated rows.

For every valid finite word,

```text
|next| = sum_(i=0)^(n-2) |h(w_i,w_(i+1))|.
```

Nonempty rows imply only `|next| >= n-1`, not `|next| >= n`. The exact `01 -> 0` counterexample resolves BOOK:1026 as a claim about the displayed trajectories. Under an explicit maximum output length `r`, a `k`-symbol pair table has the derived count `(sum_(j=1)^r k^j)^(k^2)`; the plate-bounded binary `r=2` audit therefore has `6^4=1296` tables. The book gives neither this T14 count nor an integer codec.

### State and invariants

- DOMAIN: discrete `t+1D`.
- CONFIGURATION: finite ordered occurrences carrying symbols; dynamic cardinality and sequence order are semantic.
- ALPHABET: finite `Sigma`; the native page-100 examples use `Bit`, while the page-681 relation visibly uses both two- and three-symbol pair tables.
- CONTROL: none.
- FRONTIER: ordered old occurrences satisfying `HasRightNeighbor`.
- NEIGHBORHOOD: ordered `(Self,Right)` occurrence read from one old snapshot.
- RULE result: typed nonempty `EmitWord` over the same alphabet.
- UPDATE: atomic ordered concatenation of all validated source emissions; it derives the whole successor support.
- Successor algebra: one deterministic successor for a valid total program, including the vacuous empty concatenation.
- Boundary: right-edge source ineligibility; no left-edge special case for the direct profile.
- Seed: arbitrary valid finite word; `0110` is the hash-bound direct example.
- Observers: equal-total-width rows, fixed-size boxes, lineage polygons, and CA-like grids are representations, not state.

### Conflicts and lineage

Adjacent sources overlap only in their old reads. They do not claim an old target span or persistent coordinate. UPDATE validates one result for each selected source and concatenates by source order; consequently there is no write collision policy to invent. Optional lineage associates every emitted child interval with its anchor occurrence. The right-context occurrence can influence a block without thereby becoming that block's parent.

### Variants and relations

| Variant or relation | Current disposition |
|---|---|
| Different finite seeds | seed parameterization |
| Wider left/right context | not established by the direct profile; requires its own offsets, source eligibility, and boundary evidence |
| Length-one output for every pair | restriction that directly realizes a one-sided local CA rule away from the edge |
| Three-color pair input | finite-alphabet parameterization evidenced by the page-681 rule-30 emulation relation |
| Empty pair output | T15 creation/destruction extension, not strict T14 |
| Right pad/wrap/blank/reflection | taxonomy speculation unless primary evidence is found |
| Infinite word | support/boundary variant requiring an explicit end/origin model; not inferred from finite T14 |
| Sequential first-match replacement | T16 schedule, not a T14 option |
| Two-dimensional contextual substitution | T28 topology/neighborhood extension |
| CA emulation | explicit mapping/relation; never an execution fallback |

## Current API Fit

The historical `simple_programs.md` is CA-shaped, while `architecture-audit.md` supplies the governing broad axes. T14 confirms that the document's present dense defaults are not the abstraction boundary.

| Construction element | Fit | Finding |
|---|---|---|
| DOMAIN | `DIRECT` | discrete `t+1D`; word topology belongs to CONFIGURATION |
| Finite symbol alphabet | `DIRECT` / `PARAMETERIZATION` | reuse a generic finite alphabet; semantic pair roles do not require new alphabet classes |
| Dynamic ordered configuration | `DIRECT` from T13 base | same finite-word support/topology and ragged trace requirements |
| Eligible anchored occurrences | `PARAMETERIZATION` | restrict the generic occurrence frontier by `HasRightNeighbor`; do not invent a contextual-system frontier executor |
| `(Self,Right)` read | `PARAMETERIZATION` | ordered occurrence access pattern widens T13's self read |
| Pair-to-word table | `PARAMETERIZATION` | same total finite lookup and `EmitWord` result shape with input arity two |
| Ordered structural commit | `PARAMETERIZATION` | reuse `OrderedGenerationConcat`; exact full-old-source coverage moves to the T13 preset, while the base covers the selected frontier exactly |
| Rightmost drop | `PARAMETERIZATION` | follows from frontier eligibility plus complete successor derivation; not an epsilon sentinel row |
| Equal-width rendering | `NOT APPLICABLE` to semantics | downstream observer only |
| Rule number | `SEMANTIC MISMATCH` absent an explicit output-length bound | no source-defined integer codec exists in the retained evidence; `1296` is a labelled bounded derivation only |

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
- Principles 1–3: the catalog label creates no executor. T14 changes source eligibility and reads; the exhaustive commuting proof confirms UPDATE remains ordered emission/concatenation.
- Principle 4: RULE returns a typed `EmitWord`, not an object-array scalar or unrestricted callback.
- Principles 5–8: the complete dynamic word is state; row-local coordinates, box widths, polygons, and padded tensors are representations.
- Principles 9–10: `HasRightNeighbor`, `(Self,Right)`, total pair table, and strict nonempty outputs are composable presets/invariants, not flags selecting hidden family paths.
- Principle 11: snapshot parallelism, source order, and right-edge ineligibility are defining semantics and stay in the declared axes.
- Principles 12–16: ragged trace encoding remains downstream; no CA compiler, fixed capacity, callback, family branch, or sentinel is admitted.

The one-step map `e(word)=OrderedConfiguration(word)` has an explicit inverse on the invariant-valid image. For every bounded binary table and every word through length six, the direct Notes operator and the generic pipeline select the same anchors, read the same old pairs, emit the same blocks, and concatenate them in the same order. `30-T14-semantic-oracle.py` proves this independently for 164,592 cases, including 3,888 short-word cases. It separately checks 4,080 singleton-output pair/finite-interior cases, the XOR/sheared-rule-90 fixture, both direct traces, false pair-as-splice conflicts, copy-forward, order reversal, and malformed handle/result rejection.

### Decision audit

| Decision | Evidence | Classification | Smallest reusable base | Required invariant | Reopen? |
|---|---|---|---|---|---|
| DOMAIN/configuration | BOOK:982-984,1046 | direct reuse | T13 finite ordered `t+1D` configuration | finite linear order, alphabet closure | no stage |
| FRONTIER | BOOK:1022,12113 | parameterization/restriction | ordered occurrence selector | exactly anchors `0..n-2`; unique old handles | no stage |
| NEIGHBORHOOD | BOOK:1018,12113 | parameterization | occurrence-relative ordered read | immutable `(self,right)`; overlap allowed | no stage |
| RULE result | BOOK:1026,12111 | direct typed-product reuse | T13 ordered nonempty word emission | total `Sigma^2`, output in `Sigma+` | no stage |
| UPDATE | BOOK:12113 plus commuting oracle | factored reuse | `OrderedGenerationConcat` | results cover selected frontier exactly; source/child order; no copy-forward | D019 wording only |
| empty frontier | unguarded BOOK:12113, BOOK:1022 | preset outcome | D024 construction-specific result | `[]->[]`, `[x]->[]`; no epsilon row/halt | D024 wording only |
| CA relation | BOOK:8024-8028 plus asset | restriction/relation | singleton-output pair table | declared finite interior and encoder; never native fallback | no |
| executor | all above | direct reuse | branch-free `select/read/rule/apply` | no family dispatch/callback/hidden state | no |

D018 remains active. D019 reopens only to factor full old-source coverage out of the shared UPDATE and into T13's `AllOccurrences` preset. D020 remains T13-specific and its nonempty/total/closed law is mirrored at pair arity. D021 is reused only for the evidenced finite configuration; T13's infinite-support variant is not silently inherited. D022 is not applicable, D023's interval splice is explicitly not used, and D024 gains T14's defined zero-emission successor. T13's observable semantics do not change, so no completed type stage reopens.

## Detailed Implementation Plan

1. Freeze the exhaustive monolith/split source union, retained/governed/excluded dispositions, actual Index boundary, aliases, cross-references, and content hashes in `30-T14-source-oracle.py`.
2. Freeze the source-bound asset fixed point, reference closure, hashes, C/O/R/X classification, and exact page-100 rule/seed/trajectory facts in `30-T14-asset-oracle.py`.
3. Freeze direct and generic one-step semantics, snapshot/newborn deferral, source order, boundary, zero-source behavior, and adversarial non-reuse checks in `30-T14-semantic-oracle.py`.
4. Resolve D019 by naming the generic `OrderedGenerationConcat` base with T13/T14 presets; the exhaustive commuting and hostile cases supply no counterexample requiring a distinct schedule.
5. Complete the API/runtime fit, Goal 2 handoff, no-cheating tests, source/asset/semantic root and `/tmp` checks, optimized-mode fail-closed checks, Markdown/diff/scope gates, and independent hostile review.
6. Integrate only closed findings into `0-plan.md`, `evidence-index.md`, and `design-ledger.md`; reopen any contradicted prior stage before advancing.

## Goal 2 Implementation Stage

### G2-T14 objective

Add a strict neighbor-context substitution preset by composing the generic finite ordered configuration, occurrence selectors, ordered reads, total structured lookup tables, typed word emissions, and ordered structural UPDATE inside the shared runner.

### Dependencies

- corrected broad SimpleProgram runner and typed `StepResult`;
- T13 finite ordered configuration, occurrence identity/order, word result validation, ragged trace, and ordered emission kernel;
- D019/D124 factored ordered-generation coverage and D024 construction-specific empty-frontier outcomes;
- generic finite alphabet/table machinery.

### Proposed public composition

```text
Configuration = FiniteWord[Symbol]
Frontier      = OccurrencesWhere(HasRelative(+1))
Neighborhood  = OccurrenceOffsets((0,+1))
Rule          = TotalTable[Pair[Symbol,Symbol], NonEmptyWord[Symbol]]
Update        = OrderedGenerationConcat
Seed          = FiniteWordSeed
```

The names are design roles, not required one-class-per-line commitments. Goal 2 should prefer generic typed products, predicates, table schemas, and validated presets.

### Implementation areas

- Synthesis-selected ordered-configuration module: reuse T13's finite word and snapshot occurrence handles unchanged.
- `src/ca/loci.py` / `frontiers.py`: add or compose a topology-aware `HasRelative(+1)` selector over old occurrence handles. The selector is generic data, not `T14Frontier` or a family callback.
- `src/ca/neighborhoods.py`: parameterize the T13 occurrence read as ordered relative offsets `(0,+1)` with strict availability; overlapping reads are valid.
- `src/ca/rules.py`: reuse the total structured table with a pair/product key and `NonEmptyWord[Symbol]` output validator. Support any finite alphabet, including the evidenced three-symbol relation, without a binary branch or mandatory rule ID.
- Typed result/update module: factor D019's base as `OrderedGenerationConcat(old,active,emissions)`. Validate unique monotone old handles, exact selected-frontier result coverage, alphabet closure, source binding, and child order; do not require `active` to equal every old occurrence. T13's preset retains that stronger invariant.
- `src/ca/specs.py` / catalog presets: `neighbor_dependent_substitution(alphabet,table)` resolves to ordinary shared components. Seed, trace horizon, renderer, and CA-emulation relation remain separate inputs/records.
- Generic runner: always invoke the selected UPDATE even when `active` is empty; do not install a global empty-frontier shortcut or catalog-family dispatch.
- Structured trace/encoding: reuse T13 ragged frames and child intervals. Record the unmatched rightmost old occurrence as having no descendants when provenance is requested; never copy it or synthesize an epsilon child.
- New `tests/test_t14_contextual_substitution.py`, plus shared ordered-update tests that run T13 and T14 through the same runner.

### Conformance tests required

- exact first and second page-85 `t0..t3` plate checkpoints, with the second table labelled raster-only;
- independent `Partition(old,2,1)` commuting oracle over exhaustive short binary words and all bounded nonempty binary pair tables;
- snapshot/newborn adversary where in-place iteration produces a different row;
- source-order and block-internal-order adversaries;
- explicit `[a] -> []` and `[] -> []` behavior without halt/error invention;
- rightmost context participates in the last read but emits no separate block;
- rule totality, alphabet closure, pair arity, nonempty output, duplicate row, and malformed source-result rejection;
- length-one-output restriction commuting with the corresponding one-sided local CA step on a declared finite interior, while proving that no CA compiler is used for native execution;
- binary and three-symbol pair-table validation without converting the latter into an eight-row width-three CA table;
- ragged trace and optional lineage round trips without padding as state;
- serialization round trip with no callbacks, `Any`, family tags controlling execution, hidden boundary symbol, or duplicated rule table.

### Completion evidence

One shared runner executes T13 and T14 through data-selected generic components; the exact direct examples pass; the generic/direct step square commutes; D019's base no longer mistakes T13 full coverage for a universal invariant; no runtime family switch or T14 executor exists; and the public validator exposes only the evidenced open-right profile rather than unsupported boundary policies.

## No-Cheating Checks

- Reject an implementation that preallocates a fixed maximum word, pads the right context, or treats padding as alphabet state.
- Reject a rule/function that receives the whole word or source index when only the pair read is declared.
- Reject in-place left-to-right rewriting; every read must come from the same old snapshot.
- Reject sorting outputs, target-coordinate assignment, or collision callbacks; result order is source order then child order.
- Reject a fabricated right-boundary table row such as `(symbol,Boundary) -> epsilon` in the strict base preset.
- Reject a T14-specific rollout, family switch, callback, object-cell packing, or CA-compilation fallback.
- Reject treating display width, polygon alignment, row-local x coordinates, or asset crop limits as native support.
- Reject universal nondecreasing-length validation: the exact source table gives `01 -> 0`; BOOK:1026 is trajectory-scoped.
- Reject reading the nine three-color pair panels at BOOK:8026 as an eight-row binary width-three native rule table.
- Require all source/asset/semantic oracles to fail closed under `python -O` and when invoked outside the repository root.

## Completion Requirements

- [x] Exhaustive source oracle passes with zero unresolved candidate and complete split/Index/alias closure.
- [x] Source-bound asset fixed point closes with all references and hashes classified.
- [x] Direct rules, seed, trajectories, and display-only facts are independently decoded and source-bound.
- [x] Construction model covers finite words, right-edge eligibility, empty/singleton cases, variants, and relations without invention.
- [x] Semantic oracle proves direct/generic one-step commutation and adversarial schedule/order/boundary properties.
- [x] The smallest reusable base construction is decided with evidence; no new UPDATE algebra is justified.
- [x] API/runtime fit and implementation-ready Goal 2 handoff cite actual definitions and tests.
- [ ] Independent hostile review has no unresolved blocker, major, or minor finding.
- [ ] Source, asset, semantic, Markdown, diff, scope, status/coverage, and repository-test gates pass.
- [x] `0-plan.md`, `evidence-index.md`, and `design-ledger.md` are integrated consistently.

## Stage Results

The evidence, asset, and semantic audits are closed. The 308-line source union retains 40 governed lines with zero unresolved candidate; all 17 split documents reverse-close. The 22-asset fixed point has one strict native raster, 16 typed relations, five controls, 44 exact references, and 22 hashes. It recovers both `0110` seeds, both pair tables, exact `t0..t3`, observer-only row rescaling, and the open-right edge; page 681 separately proves four binary and nine three-color pair rows with singleton emissions.

T14 is not a new construction executor or UPDATE algebra. It reuses T13's finite ordered configuration, nonempty word result, lineage, and `OrderedGenerationConcat`; it parameterizes FRONTIER to `HasRightNeighbor`, NEIGHBORHOOD to immutable overlapping `(Self,Right)` reads, and the total table to `Sigma^2 -> Sigma+`. D019 moves full-old-source coverage into T13's preset, while D024 records T14's `[]->[]` and `[a]->[]` zero-emission successors. The 164,592-case commuting oracle, 4,080 singleton-pair interior cases, exact fixtures, and hostile validation close this classification.

No prior type stage reopens and no runtime code changed. Independent hostile review, Markdown/diff/scope/status gates, and the repository regression suite remain before the status can become COMPLETE.
