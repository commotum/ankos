# 31-T15-CREATION-DESTRUCTION

Status: **IN PROGRESS — SOURCE CLOSED; ASSET, SEMANTIC, AND ARCHITECTURE AUDITS OPEN**

## Current Facts

- T15 is CSV line 16, Creation-Destruction Substitution Systems. The catalog and `CA-Types.md` supply search vocabulary only; neither is primary construction evidence.
- The frozen 22-query source audit closes 349 unique lines at 271 pre-Index and 78 actual-Index. It retains 32 matched hits plus eight governed continuations, excludes 239 pre-Index false positives, reverse-closes all 17 split documents, and leaves zero source candidate unresolved.
- The catalog name does not occur in the Book or Atlas. The actual Index has no dedicated T15 heading; eight broad 0L/1L/D1L/L-system/substitution routes lead to pages 82–87 and 70 Index candidates are excluded.
- The direct Chapter 3 discussion begins at `BOOK:1028` immediately after the strict nonempty neighbor-dependent examples. It says elements may disappear, distinguishes excessive disappearance from rapid growth, and studies rules whose creation and destruction are nearly balanced (`BOOK:1028-1040`).
- The direct figures use variable-cardinality ordered words. Equal-total-width and fixed-box rows are alternate views, and only sequence order remains semantic as insertions/deletions shift later displayed positions (`BOOK:1032-1048`).
- The facing-page three- and four-color examples retain the same creation/destruction theme; one has a CA-like regular region away from the right edge and the others create and destroy elements throughout (`BOOK:1044-1052`). Exact table arity, empty rows, seeds, and boundary behavior must be decoded and independently bound before this becomes a construction claim.
- No T15 rule table, seed, or operator is transcribed in the Notes. The prose contains no literal “empty replacement”, “epsilon”, or erasing terminology; the corpus's only explicit syntactic empty right-hand side is a T17 tag-system row at `BOOK:12298`, under a different consume-prefix/append-tail schedule.
- T14 established `OrderedGenerationConcat`: selected old anchors emit ordered words and UPDATE consumes the old generation, concatenating writes in source/child order. T13 and strict T14 currently validate `Sigma+`; T15 must determine whether the reusable base is actually `Sigma*` with nonempty output only a preset invariant.
- An empty RULE emission, zero selected sources, an empty successor, extinction, halt, and zero successors are distinct. T14's `[]->[]`/singleton-to-empty behavior comes from zero eligible pairs and cannot serve as evidence for a native epsilon-valued T15 row.
- DOMAIN is expected to remain discrete `t+1D`; the finite ordered word and its occurrence topology belong to CONFIGURATION. This remains a hypothesis until the direct rule plates and Notes/Index routes close.
- Goal 1 changes only `goal-1/`. Runtime implementation and tests remain Goal 2 work.

## Updated Assumptions

- Leading reuse hypothesis: T15 keeps the T14 finite-word/frontier/read schedule and widens the pair-table output from `Sigma+` to `Sigma*`; the shared UPDATE then needs no new algebra. This is not accepted until a direct empty-output row and one-step commuting reconstruction are proved.
- If the source instead mixes self-only and contextual profiles, they should be named presets over the same ordered-generation base, not one family switch or a table that accepts ambiguous key shapes.
- Empty emissions must remain explicit typed writes/events bound to their old sources even though they create no children. Lineage must not invent epsilon symbols, zero-width child objects, or sentinels.
- Extinction to the valid empty word is a successor. Whether the empty word subsequently stutters, terminates, or has another source-defined outcome must follow the exact native operator rather than a global empty-frontier rule.
- Balanced/slow growth is initially an observer or rule/trajectory property, not a `growth_policy`, update mode, or hidden selection criterion.

## Big Picture Objective

Reconstruct creation-destruction substitution directly from exhaustive primary evidence and decide whether native empty emissions are a typed-result parameterization of the existing ordered-generation construction. Preserve the distinctions among deletion, zero-source events, extinction, terminal outcomes, and rendering while requiring a concrete counterexample before introducing any new UPDATE algebra or executor.

## Catalog Identity

- Stable ID: T15.
- CSV line: 16.
- Catalog name: Creation-Destruction Substitution Systems.
- Taxonomy section: 15.
- Provisional construction kind: deterministic parallel transition system over a dynamically sized ordered symbol configuration.
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

Open evidence questions:

- Does the strict direct profile use ordered pair contexts exactly as T14, and which old anchors are eligible?
- Which exact rows emit zero, one, or multiple symbols, over which alphabets?
- Does the rightmost old occurrence remain source-ineligible, and what happens after the word becomes empty?
- Are the displayed seeds/tables/textual rules recoverable from Notes, raster, or both?
- Does one shared `OrderedGenerationConcat[Word]` commute with the native operator when `Word` permits epsilon?
- How should an empty source-bound emission be represented in event/lineage data without creating a child or alphabet symbol?

The provisional candidate, subject to those answers, is:

```text
active = FRONTIER.select(configuration)
reads  = NEIGHBORHOOD.read(configuration, active)
writes = RULE(active, reads)                  # source-bound words in Sigma*
next   = UPDATE.apply(configuration, active, writes)
```

## Current API Fit

Pending exact reconstruction. The reuse target is the generic finite ordered configuration, occurrence frontier predicates, occurrence-relative reads, total structured lookup, source-bound word writes, and `OrderedGenerationConcat`. Any new semantic class or UPDATE requires a direct counterexample to that composition.

## Current Runtime Fit

`src/ca` is the runtime namespace for the broader SimplePrograms library, not a cellular-automata library. Its currently implemented fixed-shape components and family-dispatched rollout do not yet realize the full intended axes. T15 is expected to stress ragged empty/nonempty word frames and epsilon-capable typed writes; Goal 2 must complete those generic axes rather than add a T15 rollout branch, sentinel, fixed capacity, callback, or family dispatch.

## Principles Audit

- DOMAIN/configuration/topology must remain separated: dynamic ordered support is not a new dimensional DOMAIN.
- Empty output is a value of a typed word-result schema, not an empty alphabet symbol or hidden delete callback.
- If T15 commutes with the same ordered-generation commit, nonempty output belongs to T13/T14 preset validation rather than the reusable UPDATE base.
- Extinction and subsequent evolution must remain source-defined outcomes; the runner has no universal empty-frontier behavior.
- Slow growth, balance, eventual repetition, CA-like patches, and display scaling remain claims/observers/relations unless evidence makes one transition-defining.

## Detailed Implementation Plan

1. Freeze the exhaustive monolith/split/Notes/Index source union and every disposition in `31-T15-source-oracle.py`.
2. Close the source-bound asset universe, hashes, rule/seed/trajectory decoding, and observer classifications in `31-T15-asset-oracle.py`.
3. Build an independent native/generic semantic oracle covering epsilon rows, deletion, creation, source order, snapshot/newborn behavior, extinction, and malformed writes.
4. Audit D019, D020, D024, and D124 from first principles; factor only the smallest reusable base and reopen any contradicted preset wording.
5. Complete the API/runtime comparison, Goal 2 handoff, no-cheating checks, hostile review, global integration, and all root/`/tmp`/optimized-mode/Markdown/diff/scope/coverage/test gates.

## Goal 2 Implementation Stage

Pending evidence closure. The provisional obligation is to make the ordered-generation result carrier honestly epsilon-capable while keeping strict T13/T14 constructors nonempty, preserving explicit source-bound empty-emission witnesses, and executing through the same branch-free runner.

## No-Cheating Checks

- Reject treating T14's zero eligible pairs as proof of a T15 epsilon rule row.
- Reject an empty string/sentinel/padding cell standing for deletion.
- Reject removing old sources in place before all reads are taken from the old snapshot.
- Reject copying unmatched or non-emitting old sources forward unless the source explicitly does so.
- Reject treating extinction as halt, error, no successor, or automatic episode termination without evidence.
- Reject a `growth_policy` that changes execution or filters native successors.
- Reject T15-specific state, UPDATE, rollout, callback, family switch, CA compiler, fixed capacity, or rendering-fed execution.
- Require source/asset/semantic oracles to pass from the repository and `/tmp` and fail closed under `python -O`.

## Completion Requirements

- [ ] Exhaustive source/split/Notes/Index/alias audit closes with zero unresolved candidates.
- [ ] Source-bound asset fixed point closes with all rule/seed/trajectory and observer facts independently decoded.
- [ ] Native empty outputs, zero-source cases, extinction, and subsequent evolution are distinguished exactly.
- [ ] Semantic oracle proves or refutes reuse of the shared ordered-generation UPDATE with adversarial cases.
- [ ] API/runtime/principles audits identify the smallest reusable base and any narrowly reopened decisions.
- [ ] Goal 2 handoff is implementation-ready and contains canonical conformance/no-cheating tests.
- [ ] Independent hostile review is clean and every oracle/test/Markdown/diff/scope/coverage gate passes.
- [ ] `0-plan.md`, `evidence-index.md`, and `design-ledger.md` are integrated consistently.

## Stage Results

In progress. Direct prose establishes native disappearance pressure, balanced-growth observations, dynamic ordered support, and multiple renderings, but the exact rule/seed/operator semantics remain open pending exhaustive source and asset closure. No runtime code has changed and no new UPDATE algebra has been accepted.
