# 31-T15-CREATION-DESTRUCTION

Status: **IN PROGRESS — SOURCE, ASSET, SEMANTIC, AND ARCHITECTURE AUDITS CLOSED; HOSTILE REVIEW OPEN**

## Current Facts

- T15 is CSV line 16, Creation-Destruction Substitution Systems. The catalog and `CA-Types.md` supply search vocabulary only; neither is primary construction evidence.
- The frozen 22-query source audit closes 349 unique lines at 271 pre-Index and 78 actual-Index. It retains 32 matched hits plus eight governed continuations, excludes 239 pre-Index false positives, reverse-closes all 17 split documents, and leaves zero source candidate unresolved.
- The catalog name does not occur in the Book or Atlas. The actual Index has no dedicated T15 heading; eight broad 0L/1L/D1L/L-system/substitution routes lead to pages 82–87 and 70 Index candidates are excluded.
- The direct Chapter 3 discussion begins at `BOOK:1028` immediately after the strict nonempty neighbor-dependent examples. It says elements may disappear, distinguishes excessive disappearance from rapid growth, and studies rules whose creation and destruction are nearly balanced (`BOOK:1028-1040`).
- The direct figures use variable-cardinality ordered words. Equal-total-width and fixed-box rows are alternate views, and only sequence order remains semantic as insertions/deletions shift later displayed positions (`BOOK:1032-1048`).
- The fixed-point asset audit closes 23 source-bound files at `C/O/R/X=3/1/13/6` with 23 monolith references, 23 split references, and 23 unique hashes. It directly decodes one binary, four ternary, and two quaternary total pair tables plus all seven seeds/`t0..t11` traces.
- The page-101 table is `11->11, 10->0, 01->10, 00->epsilon`. Five of the six page-102 tables contain respectively `2,2,1,4,3` epsilon rows; page-102 (a) contains none. All use the same immediate-right contextual schedule.
- No T15 rule table, seed, or operator is transcribed in the Notes. The prose contains no literal “empty replacement”, “epsilon”, or erasing terminology; the corpus's only explicit syntactic empty right-hand side is a T17 tag-system row at `BOOK:12298`, under a different consume-prefix/append-tail schedule.
- T14 established `OrderedGenerationConcat`: selected old anchors emit ordered words and UPDATE consumes the old generation, concatenating writes in source/child order. T15 proves that its private result carrier is `Sigma*` while strict T13/T14 validators remain `Sigma+`.
- An empty RULE emission, zero selected sources, an empty successor, extinction, halt, and zero successors are distinct. T14's `[]->[]`/singleton-to-empty behavior comes from zero eligible pairs and cannot serve as evidence for a native epsilon-valued T15 row.
- DOMAIN is discrete `t+1D`; the finite ordered word, including epsilon, and its occurrence topology belong to CONFIGURATION.
- Goal 1 changes only `goal-1/`. Runtime implementation and tests remain Goal 2 work.

## Updated Assumptions

- Closed reuse result: T15 keeps the T14 finite-word/frontier/read schedule and widens only the pair-table output validator from `Sigma+` to `Sigma*`; the shared UPDATE needs no new algebra.
- If the source instead mixes self-only and contextual profiles, they should be named presets over the same ordered-generation base, not one family switch or a table that accepts ambiguous key shapes.
- Empty emissions must remain explicit typed writes/events bound to their old sources even though they create no children. Lineage must not invent epsilon symbols, zero-width child objects, or sentinels.
- Extinction to the valid empty word is a successor. Under the accepted `Partition/Flatten` operator, the empty word has the derived successor empty word; this is construction-specific, not a global empty-frontier rule.
- Balanced/slow growth is an observer or rule/trajectory property, not a `growth_policy`, update mode, or hidden selection criterion.

## Big Picture Objective

Reconstruct creation-destruction substitution directly from exhaustive primary evidence and decide whether native empty emissions are a typed-result parameterization of the existing ordered-generation construction. Preserve the distinctions among deletion, zero-source events, extinction, terminal outcomes, and rendering while requiring a concrete counterexample before introducing any new UPDATE algebra or executor.

## Catalog Identity

- Stable ID: T15.
- CSV line: 16.
- Catalog name: Creation-Destruction Substitution Systems.
- Taxonomy section: 15.
- Construction kind: deterministic contextual ordered-generation preset over a dynamically sized finite word.
- Search vocabulary: creation/destruction, disappear/disappearance, die out/extinction, slow/balanced/fixed growth, empty replacement, page 86/page 87, substitution rule plates, Notes/Index routes, multicolor variants, and adjacent contextual relations.

## Search Log

`31-T15-source-oracle.py` freezes 22 case-insensitive line queries, hashes, and every disposition. Per-query counts are:

| Query | total | pre-Index | actual-Index |
|---|---:|---:|---:|
| Q00 catalog analytic name | 0 | 0 | 0 |
| Q01 broad substitution family | 288 | 213 | 75 |
| Q02 direct disappearance wording | 1 | 1 | 0 |
| Q03 creation/destruction/addition/subtraction | 4 | 4 | 0 |
| Q04 balance/slow/fixed growth | 8 | 7 | 1 |
| Q05 extinction/die-out/removal | 22 | 22 | 0 |
| Q06 disappear forms | 15 | 15 | 0 |
| Q07 destruction/destroy forms | 12 | 12 | 0 |
| Q08 literal empty replacement/block/word | 0 | 0 | 0 |
| Q09 erasing terminology | 0 | 0 | 0 |
| Q10 epsilon terminology control | 4 | 3 | 1 |
| Q11 shared substitution implementation | 2 | 2 | 0 |
| Q12 strict nonempty predecessor | 1 | 1 | 0 |
| Q13 old-generation parallel schedule | 1 | 1 | 0 |
| Q14 order/position shift | 1 | 1 | 0 |
| Q15 rendering alternatives | 1 | 1 | 0 |
| Q16 literal page 86/87 control | 0 | 0 | 0 |
| Q17 0L/1L/L-system aliases | 9 | 4 | 5 |
| Q18 syntactic empty RHS | 1 | 1 | 0 |
| Q19 T14 right-edge boundary | 1 | 1 | 0 |
| Q20 T16 sequential boundary | 2 | 2 | 0 |
| Q21 T17 short/extinction boundary | 2 | 2 | 0 |

After union and deduplication:

- query union: 349, digest `d5d15e7a4c2c9555440c64782dca47ad02c1550c01bde86e0cd4648d2d67813a`;
- pre-Index: 271, digest `da7be8b67ea869d5ba3e4ceccd48b254ca01d0dbf90b1067e3f4db4d4d708fcb`;
- actual Index: 78, digest `e811eee57e862b90876a86bfa6096928dc6e122e2ac31bac663397c7314e576f`;
- matched retained: 32; governed continuations: eight; final retained: 40, digest `03fc9177af658074d7a276757fcc742a1afb3e5fe976ec6b08d438c1a57f7e73`;
- excluded pre-Index candidates: 239, digest `65d4ccb8d5d2c2f6d97db0d035d5c6e3f0c9193ef695325361ec9dfcf7926b24`;
- eight relevant broad Index routes and 70 dispositioned Index false positives.

Candidate disposition is closed:

| Region | Final disposition |
|---|---|
| `BOOK:980-992` | T13 variable-word and ordinary replacement setup |
| `BOOK:1018-1026` | strict T14 contextual/nonempty/right-edge predecessor boundary |
| `BOOK:1028-1052` | direct T15 disappearance, balance, four plates, order, multicolor behavior, and CA-like relation |
| `BOOK:1054-1062` | T16 transition plus explicit contrast with prior old-generation parallelism |
| `BOOK:1132` | T17 extinction relation, not T15 mechanics |
| `BOOK:2358` | shared every-old-element substitution schedule |
| `BOOK:7940-7950` | dynamic-support/CA-emulation relation, not native fallback |
| `BOOK:12097-12113` | T13/T14 implementation boundary; no T15 table transcription |
| `BOOK:12136` | extraction-truncated neighbor-dependent growth observation; no missing text invented |
| `BOOK:12251` | 1L/T14 historical alias route |
| `BOOK:12298-12300` | explicit T17 empty appendant and short-state totalizer; different schedule |
| `BOOK:20828,21068,21422,21461,21652,21656,22114,22144` | all relevant actual-Index routes followed |

All 17 split documents are hash-bound. The 348 split query records reverse-join as 319 exact and 29 mapped extraction variants; retained evidence reverse-joins as 30 exact and ten mapped variants with zero omission. Atlas has four broad summary hits and no executable or rule-table T15 evidence. Root and `/tmp` runs pass; optimized mode fails closed. Zero source candidate remains unresolved.

## Book Excerpts

### Excerpt 1: disappearance, extinction pressure, and balance

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:1028-1030`
- Context: Chapter 3, continuation of neighbor-dependent substitution systems.
- Establishes: native disappearance is permitted and balance/extinction are trajectory-level phenomena to reconstruct.

> It is, however, also possible to consider substitution systems in which elements can simply disappear. If the rate of such disappearances is too large, then almost any pattern will quickly die out. And if there are too few disappearances, then most patterns will grow very rapidly.
>
> But there is always a small fraction of rules in which the creation and destruction of elements is almost perfectly balanced.

### Excerpt 2: two renderings of one dynamic ordered evolution

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:1032-1038`
- Context: caption and discussion for the page-86 example.
- Establishes: equal-total-width and fixed-box views are observers; fixed-amount growth describes the example, not an update policy.

> Two views of a substitution system whose rules allow both creation and destruction of elements. In the view on the left, the boxes representing each element are scaled to keep the total width the same, whereas on the right each box has a fixed size, as in our original pictures of substitution systems on page 82. The right-hand view shows that the rates of creation and destruction of elements are balanced closely enough that the total number of elements grows by only a fixed amount at each step.

### Excerpt 3: order survives addition and subtraction

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:1046`
- Context: caption for three- and four-color examples.
- Establishes: occurrence order is semantic while row-local displayed positions are not persistent addresses.

> Note that on each line in each picture, only the order of elements is ever significant: as the insets show, a particular element may change its position as a result of the addition or subtraction of elements to its left.

### Excerpt 4: multicolor rules preserve the same contextual profile

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:1044-1052`
- Context: facing-page caption and discussion.
- Establishes: three- and four-symbol variants retain dynamic ordered words and immediate-right dependence; CA-like patches are behavior/relations, not an alternate executor.

> Examples of substitution systems that have three and four possible colors for each element. The particular rules shown are ones that lead to slow growth in the total number of elements.
>
> As it turns out, the first substitution system shown works almost exactly like a cellular automaton. Indeed, away from the right-hand edge, all the elements effectively behave as if they were lying on a regular grid, with the color of each element depending only on the previous color of that element and the element immediately to its right.
>
> The second substitution system shown again has patches that exhibit a regular grid structure. But between these patches, there are regions in which elements are created and destroyed. And in the other substitution systems shown, elements are created and destroyed throughout, leaving no trace of any simple grid structure.

### Excerpt 5: old-generation parallelism is the schedule boundary

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:1054-1062`
- Context: transition into sequential substitution systems.
- Establishes: the preceding T13–T15 systems operate in parallel on the old word; T16's first-match scan is a different preset, not a deletion fallback.

> The substitution systems that we discussed in the previous section work by replacing each element in such a string by a new sequence of elements—so that in a sense these systems operate in parallel on all the elements that exist in the string at each step.
>
> But it is also possible to consider sequential substitution systems, in which the idea is instead to scan the string from left to right, looking for a particular sequence of elements, and then to perform a replacement for the first such sequence that is found.

### Excerpt 6: the accepted contextual operator

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:12109-12115`
- Context: Notes, Substitution Systems implementation.
- Establishes: adjacent overlapping old pairs are replaced and flattened under one `NestList` operator; applying this already accepted operator to epsilon-capable rows determines the derived short/empty-word cases.

> For a neighbor-dependent substitution system such as the first one on page 85 the rule can be given as
>
> `SS2EvolveList[rule_, init_List, t_Integer] := NestList[Flatten[Partition[#, 2, 1] /. rule] &, init, t]`

### Excerpt 7: CA encoding is a relation, not native execution

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:7940-7950`
- Context: Chapter 11 emulation discussion.
- Establishes: substitution systems can be encoded by CA, but in general not one native step per one CA step; the encoding cannot justify a CA execution fallback.

> The pictures on the facing page demonstrate that in fact these can also be emulated by cellular automata. But while one can emulate each step in the evolution of a mobile automaton or a Turing machine with a single step of cellular automaton evolution, this is no longer in general true for substitution systems.
>
> That this must ultimately be the case one can see from the fact that the total number of elements in a substitution system can be multiplied by a factor from one step to the next, while in a cellular automaton the size of a pattern can only ever increase by a fixed amount at each step.

## Asset Audit

`31-T15-asset-oracle.py` derives a radius-four asset closure from the frozen 40-line source set and then closes four governed caption companions. The fixed point contains 23 assets: `C/O/R/X = 3/1/13/6`, 23 monolith references, 23 split-document references, 23 physical files, and 23 unique hashes. Its manifest digest is `5ecf88946cd1a840d0a2444a562ee83592306b1693ddb3d31bbb057a31c3b38a`.

| BOOK line | Class | Dimensions | Bytes | SHA-256 | Disposition |
|---:|:---:|---:|---:|---|---|
| 1034 | O | 366x370 | 33,265 | `669c209eabf0a35d9095bf553b1c959946f72da0b0584de566a3a9032240a50e` | equal-total-width observer of the page-101 trace |
| 1036 | C | 348x360 | 26,355 | `9390efdb915dfdf78e870f85b0f2964791a00714f8619525e256098b98919c4e` | binary table, seed, and fixed-cell trace |
| 1044 | C | 1120x1263 | 300,371 | `cc6b3fdffceecf66543d9f6dbfc1628913eec7356e11e5716473a112b5b728a4` | six multicolor fixed-cell traces and connector insets |
| 1048 | C | 458x175 | 22,030 | `77c261cf4c9b83d08aead4601916dbc6ac96f371b00a30549c96586295d18585` | six complete multicolor pair tables |

The page-101 fixed-cell raster directly transcribes, in displayed input order,

```text
11 -> 11
10 -> 0
01 -> 10
00 -> epsilon
seed = 0110
t0..t11 =
0110
10110
010110
10010110
010010110
10010010110
010010010110
10010010010110
010010010010110
10010010010010110
010010010010010110
10010010010010010110
```

The page-102 rule strip directly gives four ternary and two quaternary tables. Inputs below retain the raster's descending ordered-pair presentation; epsilon is a zero-symbol word, not a color.

| Case | k | Seed | Complete table | Epsilon rows |
|---|---:|---|---|---:|
| a | 3 | `0110` | `22:0, 21:0, 20:2, 12:00, 11:01, 10:11, 02:2, 01:2, 00:0` | 0 |
| b | 3 | `0121` | `22:2, 21:01, 20:0, 12:epsilon, 11:epsilon, 10:2, 02:0, 01:01, 00:2` | 2 |
| c | 3 | `0110` | `22:1, 21:epsilon, 20:01, 12:21, 11:02, 10:22, 02:epsilon, 01:12, 00:0` | 2 |
| d | 3 | `0120` | `22:20, 21:11, 20:20, 12:2, 11:1, 10:epsilon, 02:0, 01:0, 00:21` | 1 |
| e | 4 | `0100` | `33:12, 32:23, 31:0, 30:10, 23:epsilon, 22:2, 21:13, 20:epsilon, 13:20, 12:epsilon, 11:1, 10:30, 03:epsilon, 02:20, 01:33, 00:22` | 4 |
| f | 4 | `0100` | `33:13, 32:03, 31:2, 30:epsilon, 23:02, 22:epsilon, 21:01, 20:3, 13:03, 12:0, 11:21, 10:22, 03:epsilon, 02:3, 01:10, 00:13` | 3 |

The directly sampled `t0..t11` rows, independently reproduced by the transcribed tables, are:

```text
a: 0110 | 20111 | 220101 | 022112 | 2000100 | 2002110 |
   20200111 | 222020101 | 002222112 | 0200000100 | 2200002110 | 02000200111
b: 0121 | 0101 | 01201 | 01001 | 012201 | 012001 |
   010201 | 0120001 | 0102201 | 01202001 | 01000201 | 012220001
c: 0110 | 120222 | 210111 | 22120202 | 1210101 | 2122122212 |
   211211121 | 0221020221 | 122011 | 211011202 | 022212022101 | 11210112212
d: 0120 | 0220 | 02020 | 020020 | 02021020 | 020011020 |
   0202101020 | 0200110020 | 020210121020 | 0200110211020 |
   02021010111020 | 0200110011020
e: 0100 | 333022 | 121210202 | 1313302020 | 2002012102020 |
   22203313302020 | 221202012102020 | 213203313302020 |
   1320231202012102020 | 2023200203313302020 |
   202322201202012102020 | 20232233203313302020
f: 0100 | 102213 | 2230103 | 021022 | 301223 | 10002 |
   2213133 | 010320313 | 1022033203 | 223313033 | 021320313 | 30103033203
```

Rule glyphs, seeds, and those displayed rows are direct hash-bound transcriptions. Table replay, `00 -> []` extinction, and the empty/singleton continuations are derived semantic checks. None of the six displayed multicolor seeds extinguishes through `t11`. Equal-width scaling, fixed-cell x positions, connector polygons, growth plots, repetition, nesting, and CA-like patches remain observers or behavior claims.

## Construction Model

T15 is a preset/refinement of the contextual ordered-generation construction, not a new executor or top-level state class.

```text
DOMAIN        = discrete t+1D
CONFIGURATION = FiniteWord[Symbol]             # includes epsilon
ALPHABET      = finite ordered Sigma
SEED          = any validated finite word
FRONTIER      = OccurrencesWhere(HasRightNeighbor)
NEIGHBORHOOD  = OccurrenceOffsets((Self, Right))
RULE          = TotalTable[Sigma^2, Word[Sigma]]
UPDATE        = OrderedGenerationConcat
```

For `w = w_0...w_(n-1)` and total table `h : Sigma^2 -> Sigma*`:

```text
active(w) = snapshot-scoped occurrences 0..n-2
read(i)   = (w_i, w_(i+1))
emit(i)   = h(read(i))
step(w)   = emit(0) ++ ... ++ emit(n-2)
```

Every read is taken from the same immutable old word. Adjacent sources may overlap in what they read, but the returned words are not replacement spans and therefore do not collide. UPDATE consumes the complete old generation, concatenates one emission per selected source in source/child order, and never copies the unselected rightmost occurrence.

The reusable emission/result carrier is `Word[Sigma] = Sigma*`. T13's `Sigma -> Sigma+` and T14's `Sigma^2 -> Sigma+` remain strict public validators. T15 supplies the distinct total `Sigma^2 -> Sigma*` validator; this is a typed schema refinement, not an `allow_empty` execution flag.

An epsilon row still produces one inspectable `OrderedEmission(source,())` and one zero-length lineage interval `[c,c)`. It produces no child occurrence, epsilon symbol, placeholder, or sentinel. Exact selected-frontier coverage counts that record.

The outcome distinctions are:

| Old word/event | Selected sources | RULE writes | Successor | Meaning |
|---|---:|---|---|---|
| `00` under page-101 row | 1 | one explicit epsilon emission | `[]` | active-source extinction |
| `001` under page-101 table | 2 | epsilon, then `10` | `10` | deletion without extinction |
| `[x]` | 0 | none | `[]` | derived zero-source pair commit; unmatched old source is dropped |
| `[]` | 0 | none | `[]` | derived post-extinction continuation |
| T16 no match | 0 applicable matches | none | zero successors, retained final word | `Terminal(NoMatch)` |
| T17 short prefix | disabled queue source | none | zero successors, retained residue | `Terminal(InsufficientPrefix)` |

The singleton and empty cases are not direct displayed traces. They follow from applying the accepted Notes `Partition/Flatten` operator to a T15 table. This is a construction-specific UPDATE outcome; it does not establish a universal empty-frontier policy.

The exact structural table is primary. If one explicitly bounds output length by `r`, the number of total `k`-symbol pair tables is

```text
(sum(j=0..r, k^j))^(k^2).
```

Thus the binary `r=2` audit space has `7^4 = 2401` tables; its nonempty T14 subset has `6^4 = 1296`. These are labelled bounded derivations, not source-defined rule numbers or a public codec. The unbounded finite-word family has no evidenced integer numbering.

The lossless map `e(w)=OrderedConfiguration(w)` has an obvious inverse on alphabet-valid words. `31-T15-semantic-oracle.py` proves

```text
e(native_step_h(w)) = generic_step_(e(h))(e(w))
```

for all 2,401 bounded binary tables and all 127 binary words through length six: 304,927 cases. It separately counts 1,105 epsilon-containing tables, 7,203 zero-source cases, 102,388 cases containing explicit epsilon records, 176,988 such records, 12,979 empty successors, and 5,776 active-source extinctions. Strict T14 replays 164,592 cases and strict T13 replays 4,572 cases unchanged. Exact page-101 and all six page-102 `t0..t11` fixtures also commute.

### Variants, properties, and relations

| Item | Disposition |
|---|---|
| Binary, ternary, quaternary alphabets | finite-alphabet parameterization |
| Tables with no epsilon row, including page-102 (a) | valid restriction of T15 schema and strict T14 when every row is nonempty |
| Different epsilon-row counts | ordinary RULE data |
| Output words longer than two | supported by the unbounded finite-word schema; no source count/codec inferred |
| Extinction | first transition from nonempty to empty; trajectory property, not halt |
| Slow/fixed/balanced growth | rule/trajectory observation, never UPDATE policy |
| Repetition, nesting, randomness, CA-like patches | behavior claims or relations |
| Equal-width and fixed-cell layouts | observers of one native word trace |
| Sequential erasing rule | T16 evidence question; not inferred from contextual T15 |
| Tag-system epsilon appendant | T17's different prefix-consume/tail-append preset |
| CA emulation | downstream encoding relation, generally not one-step commuting |

## Current API Fit

The current `simple_programs.md` describes one fixed-support CA-shaped realization: writable next coordinates, same-site scalar results, copy-forward, and parallel snapshot writes (`:22`, `:1510`, `:1769`, `:2180`). Those defaults are not the SimpleProgram abstraction boundary. `architecture-audit.md` supplies the governing axes used here.

| Construction element | Fit | Audit class | Smallest reusable base and invariant |
|---|---|---:|---|
| DOMAIN | `DIRECT` | 1 | discrete `t+1D`; ordered support belongs to CONFIGURATION |
| Finite ordered alphabet | `DIRECT` / `PARAMETERIZATION` | 1/2 | generic finite alphabet; no epsilon alphabet member |
| Finite ordered configuration, including empty | `DIRECT` | 1 | T13/T14 finite word with alphabet closure |
| Seed | `DIRECT` | 1 | validated complete word; exact raster seeds are fixtures |
| FRONTIER | `DIRECT` | 1 | T14 `HasRightNeighbor`; unique monotone old-snapshot handles |
| NEIGHBORHOOD | `DIRECT` | 1 | T14 immutable overlapping `(Self,Right)` occurrence read |
| RULE table | `PARAMETERIZATION` | 2 | total pair table whose output validator is `Word` rather than `NonEmptyWord` |
| RULE result | `PARAMETERIZATION` / lossless tagged product | 2/3 | `OrderedEmission(source,word)`; epsilon retains a source-bound record |
| UPDATE | `DIRECT` | 1 | `OrderedGenerationConcat` over `Sigma*`; exact coverage includes zero-length writes |
| Lineage | `PARAMETERIZATION` | 2 | zero-length interval and zero children; no fake occurrence |
| Empty successor | `PARAMETERIZATION` | 2 | D024 construction-specific one-successor result |
| Growth/layout/CA relation | `NOT APPLICABLE` to execution | 1 as observers/relations | trace queries, views, or explicit encoders |

No row is class 4: the exhaustive commuting square supplies no counterexample requiring a genuinely different execution algebra.

## Current Runtime Fit

`src/ca` is the current runtime namespace of the broader SimplePrograms library. The name and its Phase-1 CA-shaped implementation do not turn cellular automata into the top-level semantic abstraction.

- `src/ca/alphabets.py` supplies finite scalar alphabets but not the generic word-result validator split `Word`/`NonEmptyWord`. Epsilon belongs to the word carrier, not an alphabet.
- `src/ca/loci.py` provides composable dense rank-0..3 coordinate selectors. Goal 2 must preserve its selector responsibility while adding topology-aware ordered-occurrence handles; integer x coordinates cannot replace occurrence identity across length changes.
- `src/ca/frontiers.py` exposes only the dense `time_slice` preset. `HasRightNeighbor` is a generic occurrence predicate, not a T15 frontier class.
- `src/ca/neighborhoods.py` owns read access but currently uses geometric offsets on fixed tensors. `(Self,Right)` must be an ordered-occurrence access pattern over the old snapshot.
- `src/ca/rules.py` currently centers scalar outputs, family strings, and optional `Any` callables. T15 needs a closed serializable total product-key table returning typed finite words.
- `src/ca/specs.py` requires one fixed `shape` and `RawEpisode`/`RawBatch` stackable arrays. Dynamic words require native ragged frames and structured events before any optional packing.
- `src/ca/rollout.py` currently branches on rule-family names and assumes fixed-shape writes. Goal 2 must replace that limitation with the common data-composed runner; it must not add a T15 branch.
- Existing tensor boundary policies are not applicable to the open-right word operator. The absence of a right-neighbor source is already expressed by FRONTIER.

These are modest generalizations of the intended axes—alphabet/result schemas, occurrence selectors, access patterns, structural writes, and ragged results—not evidence for a parallel “non-CA” library or one executor per catalog family.

## Principles Audit

- Principle 0 requires correcting D019's private carrier rather than protecting T14 oracle wording that mistakenly rejected epsilon at UPDATE.
- Principles 1–3 favor the smallest structural reuse: T15 changes one total table/result validator; it does not create a construction class or runner branch.
- Principle 4 requires an inspectable typed empty word and source-bound record, not `Any`, a callback, or a delete side channel.
- Principles 5–8 keep the complete ordered word as state and row positions/scales as representation.
- Principles 9–10 keep `Sigma*` in the reusable carrier and `Sigma+` in strict T13/T14 validators; no `allow_empty` flag changes hidden behavior.
- Principle 11 preserves one old snapshot, right-edge eligibility, source order, and complete old-generation consumption.
- Principles 12–16 reject padding, epsilon sentinels, fixed capacity, CA compilation, rendering-fed execution, and family dispatch.

### Decision audit

| Decision | Evidence | Classification | Action |
|---|---|---|---|
| D018 UPDATE is semantic | BOOK:1028-1052,12113 | direct reuse | keep; no new UPDATE |
| D019 ordered generation | exact epsilon plates + 304,927 cases | narrow base clarification | private carrier is `Sigma*`; exact coverage counts epsilon records and permits empty child intervals |
| D020 T13 morphism | no T13 epsilon evidence; strict regression | restriction/preset | keep `Sigma -> Sigma+`; close T15 deferral |
| D024 empty selection/outcomes | active epsilon, singleton, empty, T16/T17 controls | parameterization | add three distinct T15 one-successor witnesses; no global policy |
| D025 T16 clauses | no direct T16 empty RHS | restriction/preset | keep `Sigma+ -> Sigma+`; close T15 deferral |
| D028 private word carrier | T17 plus direct T15 epsilon rows | direct confirmation | retain `Sigma*`; add T15 basis |
| D124 strict contextual substitution | all T14 outputs nonempty; strict regression | restriction/preset | keep `Sigma^2 -> Sigma+` and all T14 behavior |
| D125 T15 | direct plates + commuting proof | parameterization | add `Sigma^2 -> Sigma*` preset over the same runner |

No completed semantic stage reopens. D019, D024, D028, and historical audit wording receive narrow clarifications; D020, D025, and D124 retain their public contracts.

## Detailed Implementation Plan

1. Freeze the exhaustive monolith/split/Notes/Index source universe in `31-T15-source-oracle.py`.
2. Freeze the 23-asset fixed point and every direct table/seed/trace in `31-T15-asset-oracle.py`.
3. Prove native/generic commutation, strict T13/T14 regressions, explicit epsilon lineage, outcome distinctions, and hostile validation in `31-T15-semantic-oracle.py`.
4. Generalize only D019's private carrier, preserve public validators, and integrate D125 plus dependent wording.
5. Run independent hostile review and every source/asset/semantic, `/tmp`, optimized-mode, Markdown, diff, scope, coverage, and repository-test gate.

## Goal 2 Implementation Stage

### G2-T15 objective

Add the creation/destruction contextual preset by allowing epsilon in one generic ordered-emission carrier while preserving T13/T14's stricter constructors and executing all three through the same branch-free runner.

### Dependencies

- broad `SimpleProgram` component runner and typed `StepResult`;
- T13 finite ordered configuration, ragged trace, occurrence identity, and lineage;
- T14 `HasRightNeighbor` frontier, `(Self,Right)` read, pair-table schema, and open-right behavior;
- D019 `OrderedGenerationConcat` and D024 construction-specific empty-selection outcomes;
- D028 epsilon-capable private `Word` carrier.

### Proposed public composition

```text
Configuration = FiniteWord[Symbol]
Frontier      = OccurrencesWhere(HasRelative(+1))
Neighborhood  = OccurrenceOffsets((0,+1))
Rule          = TotalTable[Pair[Symbol,Symbol], Word[Symbol]]
Update        = OrderedGenerationConcat
Seed          = FiniteWordSeed
```

These are roles/compositions, not a requirement for one runtime class per line. `Word` and `NonEmptyWord` should be explicit schemas or validators, never a boolean `allow_empty` mode.

### Implementation areas

- Generic ordered data module: make the private `Word[Symbol]` carrier alphabet-closed and epsilon-capable. Retain `NonEmptyWord[Symbol]` as the T13/T14 validator.
- Typed result module: `OrderedEmission(source,word)` always exists for a selected source. Store `EmissionRecord(source,word,start,stop,children)`; epsilon requires `start == stop` and `children == ()`.
- Ordered UPDATE: accept `Sigma*` emissions, require exactly one emission per unique monotone snapshot-bound selected handle, concatenate in source/child order, consume all old sources, report unselected sources, and never copy them. Reject stale same-index handles from foreign generations.
- Rule/spec layer: add a serializable total `Pair -> Word` validator/preset over any declared finite alphabet. Missing rows are invalid; epsilon is not a missing/default row.
- Shared runner: invoke UPDATE even when FRONTIER selects zero sources. The selected program/preset supplies the outcome; no global empty-frontier shortcut is allowed.
- Trace/encoding: support ragged empty/nonempty frames and zero-length lineage intervals without padding or fake children. Extinction is a derived trace query.
- Observers: growth increments/rates, balance, repetition/nesting, equal-width/fixed-cell views, and CA relations consume native traces without controlling execution.
- Tests: add shared ordered-update tests plus T15 conformance tests; run T13/T14/T15 through the identical runner.

### Required conformance tests

- exact page-101 total table, seed, and `t0..t11` trace;
- all six page-102 complete tables, seeds, `t0..t11` traces, and epsilon-row counts `(0,2,2,1,4,3)`;
- exhaustive `7^4` binary tables x all words through length six commuting with the direct pair-concatenation oracle;
- strict `6^4` T14 and bounded T13 regressions proving their public validators still reject epsilon;
- `00 -> []` with one emission record/zero children, `001 -> 10` with epsilon preceding a nonempty block, `[x] -> []` with no emission, and `[] -> []` after extinction;
- explicit distinction from T16 `NoMatch` and T17 `InsufficientPrefix` zero-successor outcomes;
- old-snapshot/newborn, source order, rightmost read-but-non-source, and no-copy-forward adversaries;
- missing/duplicate/wrong-key/out-of-alphabet rows and emissions;
- duplicate/unordered/out-of-range/stale/foreign-generation handles and incomplete/reordered result coverage;
- tampered zero-length intervals and fake epsilon child records;
- serialization and ragged-trace round trips with no callback, `Any`, sentinel, capacity, family tag controlling execution, or renderer dependency.

### Completion evidence

One shared runner and one `OrderedGenerationConcat` execute strict T13, strict T14, and T15. Their only relevant difference is validated FRONTIER/read/table/result data. Exact plates and the exhaustive commuting square pass, every selected epsilon remains inspectable, and no T15 executor/update/state class exists.

## No-Cheating Checks

- Reject treating T14's zero eligible pairs as proof of a T15 epsilon rule row.
- Reject representing epsilon by an alphabet symbol, empty-string sentinel, padding cell, tombstone, or missing row.
- Reject removing old sources in place before all reads are taken from the old snapshot.
- Reject filtering epsilon writes before exact selected-source coverage/provenance validation.
- Reject copying the rightmost or an epsilon-emitting old source forward.
- Reject treating extinction as halt, error, no successor, or automatic episode termination without evidence.
- Reject a global empty-frontier halt/stutter/drop rule; invoke the declared UPDATE/outcome policy.
- Reject a `growth_policy` that changes execution or filters native successors.
- Reject T15-specific state, UPDATE, rollout, callback, family switch, CA compiler, fixed capacity, or rendering-fed execution.
- Reject weakening T13/T14/T16 public validators merely because the private carrier admits epsilon.
- Reject a T16 single splice or T17 prefix queue: each produces a different step on the page-101 seed.
- Require source/asset/semantic oracles to pass from the repository and `/tmp` and fail closed under `python3 -O`.

## Completion Requirements

- [x] Exhaustive source/split/Notes/Index/alias audit closes with zero unresolved candidates.
- [x] Source-bound asset fixed point closes with all rule/seed/trajectory and observer facts independently decoded.
- [x] Native empty outputs, zero-source cases, extinction, and subsequent evolution are distinguished exactly.
- [x] Semantic oracle proves reuse of the shared ordered-generation UPDATE with adversarial cases.
- [x] API/runtime/principles audits identify the smallest reusable base and narrow decision clarifications.
- [x] Goal 2 handoff is implementation-ready and contains canonical conformance/no-cheating tests.
- [ ] Independent hostile review is clean and every oracle/test/Markdown/diff/scope/coverage gate passes.
- [ ] `0-plan.md`, `evidence-index.md`, and `design-ledger.md` are integrated consistently.

## Stage Results

Evidence, assets, semantics, and architecture are closed; independent hostile review and final global gates remain. The exact plates prove `Sigma^2 -> Sigma*` under T14's old-snapshot adjacent-pair schedule. The exhaustive oracle finds no class-4 counterexample: T15 widens only the typed word-result carrier and retains zero-length source witnesses. Strict T13/T14/T16 contracts remain nonempty, no prior semantic stage reopens, no runtime code changed, and no new UPDATE algebra or executor was accepted.
