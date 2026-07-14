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

- `32-T18-semantic-oracle.py` proves that the occurrence-addressed normalization `(slot,word)` maps losslessly to `Phase(slot) · Data(word)` with exactly one phase marker at the left endpoint. The literal Notes pair `{rotated block values,word}` is its step-compatible quotient when a cycle has rotational symmetry; it is not falsely claimed to distinguish equal rotations.
- On a nonempty event, the generic pipeline reads the marker and first data symbol from one immutable snapshot, replaces that prefix by `Phase(next_slot)`, conditionally inserts the scheduled data block at the old endpoint, and commits both anchored writes atomically.
- On an empty event, `Phase(slot)` has no data head. The explicit Notes clause and semantic oracle give one identity successor with the phase frozen, not T17's zero-successor `InsufficientPrefix`.
- The bounded 71,442-case commuting square finds no counterexample requiring a new UPDATE algebra. Empty activity also flows through empty NEIGHBORHOOD/RULE collections before the configured UPDATE/outcome is invoked, so the four-axis call path needs no family branch. The phase marker is a tagged ALPHABET role and invariant, not a family control class.

## Big Picture Objective

Reconstruct cyclic tag systems from primary evidence, prove whether visible cyclic control composes with the existing ordered rewrite machinery, and produce an implementation-ready Goal 2 handoff without hidden time, family dispatch, fixed capacity, or a cyclic-specific executor.

## Catalog Identity

- Stable ID: T18.
- Exact catalog name: Cyclic Tag Systems.
- Entry kind: deterministic finite-word transition construction with visible finite cyclic control.
- Initial vocabulary: cyclic tag system, alternating/cyclic cases, append block, black trigger, first/leftmost element, rotate/rotary element, `CTStep`, `CTEvolveList`, `CTList`, page 95/96, substitution relation, ordinary-tag compiler, rule 110, universality, Kolakoski, growth/randomness, empty word.

## Search Log

`32-T18-source-oracle.py` freezes 19 case-insensitive line queries, their hashes, and every pre-Index/actual-Index disposition. Per-query counts are:

| Query | Scope | total | pre-Index | actual-Index |
|---|---|---:|---:|---:|
| Q00 | direct cyclic-tag name | 60 | 44 | 16 |
| Q01 | broad tag-system family | 111 | 81 | 30 |
| Q02 | ordinary/Post/Wang/uniform/multiway boundary names | 17 | 11 | 6 |
| Q03 | native scheduled-block definition | 5 | 5 | 0 |
| Q04 | head removal, trigger, and tail append | 6 | 6 | 0 |
| Q05 | alternation/cycle/rotary schedule | 13 | 13 | 0 |
| Q06 | implementation/compiler symbols | 17 | 17 | 0 |
| Q07 | generalized cycles/values/block lengths | 5 | 5 | 0 |
| Q08 | growth and substitution properties | 7 | 7 | 0 |
| Q09 | history names and Kolakoski relation | 21 | 20 | 1 |
| Q10 | randomness/frequency observations | 7 | 7 | 0 |
| Q11 | initial-condition scope | 8 | 8 | 0 |
| Q12 | cyclic-tag emulation relations | 24 | 21 | 3 |
| Q13 | universality routes | 13 | 12 | 1 |
| Q14 | substitution controls | 33 | 30 | 3 |
| Q15 | rule-110 saturation control | 138 | 121 | 17 |
| Q16 | focused Turing/CA tag relations | 21 | 16 | 5 |
| Q17 | empty clause versus trough overflow | 2 | 2 | 0 |
| Q18 | requested terminology/alias control | 3 | 2 | 1 |

After union and deduplication:

- query union: 305, digest `db3643b42768e2079aa28e248b05aeeb77bcaae4c6e0e610fd080d63ca4ab15c`;
- pre-Index: 259, digest `ec4955e232ed49260218ca482044cd632cadc5bf726366f2cceba763370fc78a`;
- actual Index: 46, digest `34dc4b774ced6937c57f069923339c584525ebae542cd59d83678ecb317afaf6`;
- matched native/relation/control lines: `30/43/36`;
- governed continuations: 51;
- final retained: 160, digest `698fb02434bd7d28565f4dd5c6e8597c079f41d94339374638e9d2a925e7630c`;
- retained partition: 39 native, 84 explicit relations, and 37 construction controls;
- excluded pre-Index candidates: 150, digest `d0a2a1652b2ca5aaf5e897cf236f1d70e790ba28ca009606fa346ce518e64f0b`.

The excluded partition is exhaustive: 102 unrelated rule-110 background lines, 23 substitution background lines, one other tag-family line, 15 history lines, and nine contextual false positives. The 46 actual-Index candidates likewise partition into 16 T18 routes, 16 tag controls, two substitution controls, 11 rule-110 background routes, and one history route. Both unresolved remainders are zero.

Candidate disposition is closed:

| Region | Final disposition |
|---|---|
| `BOOK:1134-1158` | direct definition, five native programs/seeds/traces, and growth observers |
| `BOOK:1108-1132` | ordinary/Post/Wang tag predecessors and extinction controls |
| `BOOK:7952,8032-8080` | uniform/ordinary-tag and Turing/CA compiler chain; explicit relation only |
| `BOOK:8172-8272` | rule-110 realization, alternate views, mechanisms, and compiler constraints; relation only |
| `BOOK:12315-12364` | native Notes implementation, visible rotated schedule, empty totalization, generalizations, properties, mechanical realization, and history |
| `BOOK:13265,14275` | finite-initial-condition qualifications, not queue capacity |
| `BOOK:17236` | derived growth observer |
| `BOOK:18514-18530` | `TS1ToCT` ordinary-tag compiler relation |
| `BOOK:18672-18740` | rule-110 initial-condition compiler and multiple-of-six constraints; encoding restrictions only |
| `BOOK:18215,18488-18568,18794-19324` | neighboring recursive/Turing/multiway/compiler controls |
| `BOOK:20908-22390` | all 16 actual-Index T18 routes followed and classified |

The direct Notes state is `{rotating rule list, finite word}`: cyclic focus is visible state, not executor time. `BOOK:12323` is OCR-damaged and is not treated as literal executable evidence; the main prose and hash-bound native rasters independently fix the black-trigger branch. The requested phrases “program counter”, “trigger symbol”, “deletion number”, and “appendant” are useful typed roles but are not native cyclic-tag terminology in the Book.

All 17 split documents are hash-bound. The split query closure has 302 records—269 exact and 33 explicitly reverse-joined extraction variants—with digests `eefde3b65b5fb97ca3a4c52a3d6addd9d8df2f36b4c1e382d18e1cede5acfa96`, `7ded0f714fdf9f2d971d0e9cb57f4638e47c85d4c43971ea2f10cdf249202b35`, and `d1c7c63f615bd2e4d728c79540ea2532ac1f899d1a019d7c3ffde229c4e7d0b2`. Retained evidence reverse-joins as 125 exact and 35 nonexact records. The 542-line Atlas contributes nine broad routes and no additional native rule table. Catalog/taxonomy identity passes. Root and `/tmp` runs pass; optimized mode fails closed; import is silent. Zero source candidate remains unresolved.

## Book Excerpts

### Excerpt 1: the rule schedule chooses the possible block

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:1134-1138`
- Context: Chapter 3 introduction.
- Establishes: the append-block choice is a cyclic schedule, while the old head symbol decides whether that already-selected block is appended.

> The idea of a cyclic tag system is to make the underlying rule already specify exactly what block can be added at each step.
>
> In the simplest case there are two possible blocks, and the rule simply alternates on successive steps between these blocks, adding a block at a particular step when the first element in the sequence at that step is black.

### Excerpt 2: one head is removed and a conditional block is appended

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:1140-1146`
- Context: page-95 rule/trajectory caption.
- Establishes: delete-one, tail append, and alternating phase form one native event; the circle is a visible phase observation, not movement direction.

> There are two cases in the rule, and these cases are used on alternate steps, as indicated by the circle icons on the left. In each case a single element is removed from the beginning of the sequence, and then a new block is added at the end whenever the element removed is black.

### Excerpt 3: the page-96 seed and observers are not state

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:1152-1158`
- Context: five direct examples and their growth plots.
- Establishes: each direct fixture begins with one black element; nested-form and growth-fluctuation claims are observations of full word/phase trajectories.

> In each case the initial condition consists of a single black element.
>
> The fluctuations are shown with respect to growth at an average rate of half an element per step.

### Excerpt 4: rearranged and rule-110 views are explicit relations

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:8172-8192`
- Context: rule-110 universality construction.
- Establishes: standard, stationary-position, skewed, and mechanism views all represent the same cyclic evolution; they do not replace its native configuration or executor.

> Picture (a) shows an example of the evolution of a cyclic tag system in the standard representation from pages 95 and 96. Picture (b) then shows another version of this same evolution, but now rearranged so that each element stays in the same position, rather than always shifting to the left at each step.

### Excerpt 5: the Notes keep phase in state and freeze it on empty

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:12317-12335`
- Context: `CTEvolveList`/`CTStep` implementation.
- Establishes: the program data and word are paired as instantaneous state; live steps rotate the rule list, while the explicit empty clause returns both components unchanged.

> With the rules for the cyclic tag system on page 95 given as `{{1, 1}, {1, 0}}`, the evolution can be obtained from `CTEvolveList` and `CTStep`.

The extraction damages the black-head clause, so no executable text is invented from it. The intact empty clause and independent main-text/raster trajectory determine the audited boundary.

### Excerpt 6: longer cycles and natural multiplicity are rule presets

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:12337-12344`
- Context: Notes generalizations.
- Establishes: a nonempty cycle may have more than two slots; for natural-valued data, removing `n` repeats the scheduled block `n` times. Neither variation changes the firing/update algebra.

> The implementation above immediately allows cyclic tag systems which cycle through a list of more than two blocks.

### Excerpt 7: substitution and universality claims remain mappings

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:12350-12358,18514-18522`
- Context: Notes properties and the ordinary-tag-to-cyclic compiler.
- Establishes: substitution behavior follows only under stated block-length conditions, and ordinary tag/Turing/CA/rule-110 material is a compiler or emulation relation—not a native execution fallback.

> If all blocks in a cyclic tag system with n blocks have lengths divisible by n, then one can tell in advance on which steps blocks will be added, and the overall behavior obtained must correspond to a neighbor-independent substitution system.

## Asset Audit

`32-T18-asset-oracle.py` derives a 38-asset radius-four closure from the frozen source set and adds five governed source-bound companions. The resulting universe has 43 assets at `C/O/R/X = 4/1/24/14`. It closes 43 monolith references, 43 split references, 43 physical files, and 43 unique hashes. The complete universe digest is `986bcee8482b59913595889d5ef18523ac90ee2203feb4e70d919e6315a15f46`; its manifest digest is `1fce963be60513e3fead38d48f3a6ba8472a65e203a5e4c495da32908efb422b`.

The strict native/observer subledger is exactly five files (`C/O = 4/1`), with universe digest `95411e9d7c6de49bdd05049d5435bf0b935a6afdcde29619b5775b2205cfe82c` and manifest digest `bc91ba39ffb022ac91cdbbad2c7685523f8209de542d51a5f7d543c44f6fb488`:

| BOOK line | Class | Dimensions | Bytes | SHA-256 | Disposition |
|---:|:---:|---:|---:|---|---|
| 1140 | C | 248x458 | 18,568 | `b91df18a471d1e3e02e27bcf3a7b95a3f01e295223cf5ff4bd8b8fb2cc592a75` | page-95 alternating phase and finite-word trajectory |
| 1142 | C | 508x70 | 7,515 | `c8a203dc1ac1530065eb9372f5757991d22bc3c423b0c0c36041824f0acab222` | delete-head/black-trigger/tail-append schematic |
| 1146 | C | 226x45 | 2,558 | `daea1bcb06cb9715295c25a16a0bf33bb3f1ce0188d03e183596479bb1ffa3bb` | page-95 two-block rule summary |
| 1152 | C | 1185x547 | 106,271 | `26790ff2416466d111867c85794fd9b66aa18797cfd270f36e5631ccb7c41dee` | five page-96 rules, common seed, and 100-row traces |
| 1156 | O | 1237x650 | 99,927 | `b25c6520aed62856eedb5c0f1abe96d3e13ec3d9fd72306e3cb271fe1d24746a` | derived length-fluctuation plots for cases d/e |

Printed pages 95–96 correspond to physical filenames `_page_110_*` and `_page_111_*` because the extracted file numbering includes front matter. Literal `_page_95_*`/`_page_96_*` files are unrelated Turing-machine controls and are explicitly excluded.

The page-95 direct fixture is

```text
blocks = [11, 10]
seed   = 1 at phase 0
t0..t24 =
1
11
110
1011
01110
1110
11010
101011
0101110
101110
0111010
111010
1101010
10101011
010101110
10101110
010111010
10111010
011101010
11101010
110101010
1010101011
01010101110
1010101110
01010111010
```

The five page-96 fixtures all start from `1` at phase zero. Each full `t0..t99` word sequence is independently regenerated and digest-bound:

| Case | Ordered blocks | Final `t99` word | Full trace SHA-256 |
|:---:|---|---|---|
| a | `[11,10]` | `10101010101110101010` | `c9d9199aacac4298a05c9810d19654aa45ff1193067e636c3361cf4f87e21e79` |
| b | `[1,11]` | `11111111111111111111111111111111111111111111111111` | `d9a237a460cccbcd90bddc1b47a204b03f7a03941be3fc43388a0af9ae4966ef` |
| c | `[10,11]` | `11101110111110111110111011111011111011101111101110111110111110` | `adadc131e58c22729fc2651a1989d2fd5fae618cb402807f93e1b7648cbfe019` |
| d | `[1,101]` | `110110111011011110111011011101101111011110111011011` | `b7d44cb49a4fa6c6e84564e93ff29f85e12bce9eedc8ba1c6cb5324a4c29577a` |
| e | `[111,0]` | `001110011101110111011100111001110111011111101111110111` | `024da84c4d9e88aa4af7c6e2ef7441b805af16708be7f2157ec4ffdfabd4cfc1` |

The rule-110 relation plate at `BOOK:8180/8184` independently redraws case d through `t20`; it agrees exactly but remains class R. The Notes' mechanical paragraph refers to a picture that is absent from this extraction: `BOOK:12348` is an OCR placeholder, the nominal split Notes file contains one line, the actual T18 Notes are mispartitioned into `BACK-MATTER/Index/Index.md:220-267`, and no `_page_895_*` JPEG exists. The oracle freezes that absence rather than fabricating an asset.

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

The same generic `apply_ordered_spans` composition function independently realizes 1,806 bounded T17 prefix-delete/tail-append cases. Those cases establish shared old-coordinate span composition and provenance; T18's `apply_update` wrapper separately validates exact snapshot ownership, source/result correspondence, phase evolution, and its construction-specific witnesses. T18 changes the prefix write from pure deletion to replacement by the next phase marker; the old-end insertion and one-snapshot atomicity remain the same ordered multi-span UPDATE. A 255-case bounded audit also confirms the Notes multiplicity generalization, in which a removed natural value `n` appends `n` copies of the scheduled block.

The adversarial cases establish:

- equal words at different phases can have different successors, so word-only state and trace-time-derived phase are invalid;
- phase advances on every nonempty event, including false-trigger and successful-extinction events;
- a successful transition to empty is distinct from the subsequent empty identity event, where phase freezes;
- one-block and cycles longer than two use the same semantics and no special execution path;
- same-generation foreign, stale, and successor-reused handles reject through opaque snapshot identity;
- missing, reordered, wrong-phase, wrong-anchor, and fake-append results reject before commit;
- strict program and direct-state serialization rejects coercion and retains the occurrence-addressed phase; full tagged-configuration/event/trace serialization remains a Goal 2 conformance requirement.

The normalized integer phase is a faithful visible-control cover of the Notes' rotated block-value list. If a cycle is rotationally periodic, distinct named phases can project to the same Notes value-state; the oracle checks that their projected successors also agree. Goal 2 may therefore use named slot occurrences, or the explicit quotient by equal rotations, but it must declare which identity it serializes. It may not infer either representation from trace time.

Occurrence IDs are nonsemantic provenance. Reusing the phase marker's ID while its slot label changes is the audited canonical lineage profile, not a source-mandated semantic requirement; another lossless provenance policy is acceptable if visible phase, uniqueness, and one-step evolution are unchanged.

The canonical Notes rule `{{1,1},{1,0}}` from a one-black seed passes the hash-bound page-95 `t0..t24` trace. Both semantic paths also reproduce all five full page-96 `t0..t99` profiles, for 500 book-fixture states, including occurrence-distinct phase values and exact full-trace digests.

## Construction Model

- DOMAIN: discrete `t+1D`.
- Configuration/support: a finite ordered word together with one visible focus in a finite cyclic program schedule; equivalently an invariant-valid tagged word beginning with exactly one phase marker.
- ALPHABET: strict binary data plus a finite phase-slot tag; generalized data may use an explicit nonnegative multiplicity carrier.
- Program: immutable nonempty ordered cycle of alphabet-closed finite append words; the named-slot profile preserves occurrence positions, while the literal Notes-value profile may quotient exactly equal complete rotations.
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
| CONFIGURATION/support | REUSE + CURRENT GAP | T17/D027 already require finite variable-length ordered support; T18 composes it with one tagged left-end phase invariant. `simple_programs.md:87-169` has not implemented that generic support yet. |
| ALPHABET | PARAMETERIZATION | The value responsibility at `:200-233` generalizes to `Phase(slot) | Data(symbol)`; strict binary and natural-multiplicity data are validators/presets. |
| FRONTIER | PARAMETERIZATION + CURRENT GAP | Parameterize T17's anchored prefix selector to the unique old phase/head occurrence pair, or zero data-head sources when empty. Absolute writable coordinates at `:1412-1510` do not yet realize structural loci. |
| NEIGHBORHOOD | PARAMETERIZATION + CURRENT GAP | Reuse ordered endpoint/prefix access for `(phase,head)`; all reads still come from one old snapshot. Geometric offsets at `:360-731` do not yet implement that access type. |
| RULE/write | PARAMETERIZATION + CURRENT GAP | A closed immutable cycle/trigger preset emits two D039 ordered span writes from `(phase,head)`. Scalar next-coordinate values at `:1767-1793` do not yet admit the generic result carrier. |
| UPDATE | PARAMETERIZATION | D039 generic ordered multi-span commit already expresses phase/head prefix replacement plus old-end insertion; no cyclic update or executor is needed. |
| outcome | PARAMETERIZATION | D024's construction-specific empty policy gains an evidenced identity event with frozen phase; T17 `InsufficientPrefix` remains unchanged. |
| trace/encoding | REUSE + CURRENT GAP | Reuse T13/T17 ragged ordered snapshots and lineage, adding visible phase/witness fields. Dense copied slices at `:2124-2199` have not implemented that boundary. |

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
| D126 T18 boundary | occurrence-addressed direct state, tagged inverse, and Notes quotient | 3 | T17 ordered support + visible phase + anchored access + closed cycle/trigger + D039 spans + D024 empty policy | add T18 composition only |

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
- Program module: immutable nonempty ordered block cycle, alphabet-closed `Word` blocks including epsilon, explicit trigger policy, and a declared schedule identity. The occurrence-addressed profile preserves named slot positions even when values repeat; an optional Notes-value profile quotients phases only when their complete rotated block lists are equal. Strict Chapter 3 construction uses binary `TriggerEquals(black)`.
- Generalized preset: represent the Notes natural-value variant with a closed `RepeatScheduledBlockByRemovedNatural` rule form. It is not an `allow_multicolor` flag or callback.
- FRONTIER: select exactly the left phase marker plus first data occurrence when present. On `Phase(slot)` alone, select no data-head source but still invoke the configured UPDATE/outcome policy.
- NEIGHBORHOOD: return the old marker slot, removed value, exact occurrence IDs, and old endpoint. It does not read trace time, mutate/rotate program data, or inspect newborns.
- RULE/result: return two explicit ordered writes—`Replace([0,2),Phase(next))` and `Insert(old_endpoint,conditional_block)`—plus scheduled-slot/trigger witnesses. An epsilon insertion remains an explicit result, not a missing write or table row.
- UPDATE: reuse the generic atomic ordered multi-span committer. Validate exact snapshot ownership, prefix/end anchors, write ordering/nonoverlap, phase successor, source/result coverage, alphabet closure, consumed head identity, persisted suffix order, and fresh appended occurrences. Reusing the phase marker ID is the canonical lineage preset, not semantic identity.
- Outcome module: successful extinction is an advanced event with the next phase; a subsequent empty input is an identity event with frozen phase and one successor. T17 `InsufficientPrefix`, T16 `NoMatch`, T15 post-extinction empty rebuilding, halt, error, invalidity, and horizon remain distinct.
- Spec/preset module: `cyclic_tag_system(blocks,initial_phase=0,trigger=black)` returns the ordinary shared components. The catalog/family name never reaches execution.
- Runner: always executes selected component data. Empty activity yields empty reads and writes and still reaches the configured UPDATE/outcome. No `if cyclic_tag`, phase-from-step, hidden mutable rule rotation, callback, formula fallback, or CA compiler.
- Structured trace/raw boundary: retain tagged ragged states, phase/head/tail events, outcome witnesses, and optional lineage. Length, first-element, growth, substitution checkpoints, mechanical layouts, rule-110 encodings, and rasters are downstream records.
- Tests: add T18 conformance tests and shared tagged-alphabet/ordered-span/outcome/serialization tests; rerun T17 and every existing runtime test.

### Required conformance tests

1. Reproduce all five source-bound direct page-95/page-96 programs, their one-black seed, the page-95 `t0..t24` trace, and every page-96 `t0..t99` digest/checkpoint.
2. Reproduce `{{1,1},{1,0}}` from `Phase(0) · Data(1)` through `t24` and compare direct, tagged, and serialized runs.
3. Phase discriminator: blocks `{1}` and `{0}` map the same word `{1}` to different data successors at slots zero and one.
4. Assert true-trigger append, false-trigger no-append, empty scheduled block, and nonempty block after an old suffix, retaining scheduled-versus-appended witnesses.
5. Assert phase advances on every nonempty event even when nothing is appended; it wraps exactly modulo the number of slot occurrences.
6. Assert successful extinction advances phase once, then `Phase(slot)` produces an identity successor with phase frozen and a distinct empty-stutter witness.
7. Test cycles of one, two, and more than two blocks. One-block repetition is a property, never a halt or executor mode.
8. Test duplicate equal block values in different named slots and round-trip occurrence-addressed phase identity; separately test that rotationally identical Notes value-lists form a step-compatible quotient rather than claiming a false inverse.
9. Test the natural multiplicity rule with removed values zero, one, and greater than one; reject negative/nonintegral multiplicities rather than invoking host `Table` behavior.
10. Prove the tagged encoder has an inverse and the direct/generic square commutes over the bounded 399-program/71,442-state audit.
11. Run T17 prefix-delete/tail-append cases through the same ordered-span committer and prove T17 `InsufficientPrefix` and public program schema do not admit cyclic phase.
12. Reject missing/duplicate/out-of-range markers, phase outside the cycle, empty program cycles, out-of-alphabet blocks/seeds, stale/same-generation-foreign sources, wrong old endpoints, wrong phase successors, incomplete/reordered/colliding writes, reused removed IDs, and fake/freshness-violating children.
13. Verify one event exposes no intermediate headless/old-phase/partially-appended configuration.
14. Round-trip program, tagged state/configuration, writes, event, snapshot scope, and ragged trace data without coercion, callbacks, `Any`, mutable iterators, trace-time dependencies, family tags controlling execution, padding, capacity, or renderer state.
15. Verify substitution and ordinary-tag equivalences only through declared encoders/step groupings, and rule-110/Turing/CA material only through explicit realization relations.

### Completion evidence

One shared runner and generic ordered-span UPDATE execute T17 and T18 from typed component data. All direct fixtures and the commuting square pass; phase is present in every native snapshot; the named-slot/Notes-value identity choice is explicit; empty and extinction witnesses remain distinct; structured traces serialize losslessly; existing tests pass; and no cyclic state class, UPDATE algebra, executor, branch, hidden counter, callback, capacity, sentinel, or compiler fallback exists.

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
