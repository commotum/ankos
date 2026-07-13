# 7-T17-TAG

Status: **COMPLETE**

## Current Facts

- Exact catalog row: T17, CSV line 18, `Tag Systems`; taxonomy seed `ref/notes/CA-Types.md:441-468`.
- The native state is a finite ordered word with semantic front and back. At an eligible step, an exact leading word chooses an appendant, a fixed leading span is consumed, and that appendant is added after the old suffix in one atomic queue event.
- Wolfram's ordinary construction reads exactly the same `n` leading symbols that it deletes. It is not Post's historical tag construction, whose appendant depends only on the first symbol even when `n` symbols are deleted.
- The direct history also identifies Wang lag systems, which may inspect more than the first symbol but delete only the first. Read width and deletion number are therefore independent semantic integers in the evidenced prefix-queue family, not a mode flag or one overloaded neighborhood radius.
- The appendant table is a total alphabet-closed map from every readable prefix to a finite word, including the empty word. The Notes count all words of lengths `0..r`, and their canonical rule contains `10 -> {}`. A missing table row is invalid; host-language unmatched identity is not a default appendant, no-op, or terminal case.
- One event uses the old prefix, deletes the old leading span, preserves the remaining old occurrences in order, and creates the appendant at the tail. New symbols cannot be read in the event that creates them.
- The native rule relation has no applicable event when the word is too short for the required read/delete spans. It retains that short residue as a typed zero-successor terminal state. The supplied `TSEvolveList` is a reference-history totalization that maps a short residue to `{}` on the next requested sample; it must not silently redefine the operational halt.
- Empty appendants are direct T17 evidence for zero-length structural output. They broaden a private ordered-edit word/splice capability to `Sigma*`, but do not broaden T13's public `Sigma -> Sigma+` morphism or T16's evidence-strict nonempty RHS validator.
- The base construction is deterministic: every eligible state has exactly one successor, every insufficient state has zero, and there is no scan cursor, program counter, branch set, spatial boundary, blank symbol, padding, or capacity.
- For `k` symbols, read width `q`, and appendants of length at most `r`, the total number of complete tables is `(sum_{j=0}^r k^j)^(k^q)`; for Wolfram `q=n`, `k=2`, `n=2`, `r=3`, this is `50,625`. The corpus gives no canonical integer rule-code ordering.
- The one-deletion case is event-time equivalent to a slowed neighbor-independent substitution system at complete queue cycles. Cyclic tag systems, multiway tag systems, CA/Turing/recursive-function compilers, and compressed first-symbol/length histories are relations or observers, not native T17 execution.

## Updated Assumptions

- T13's finite `OrderedSequence`, occurrence handles, ragged snapshots, and consumed/created provenance remain reusable. T17 does not inherit T13's all-occurrence source coverage or `ParallelReplaceConcat` commit.
- T16's typed terminal/outcome split and policy-guarded private ordered-span edit kernel remain reusable. `SingleSpliceUpdate` is not T17's public update: replacing the consumed prefix in place would put output before the suffix, while a tag event appends after it.
- A closed `RequiredQueuePrefix` source can return one `QueueHeadSource` only when the word supplies both the declared read and delete spans. It consumes the same immutable `PrefixQueueProgram` widths used by the read/rule/update validators; no duplicated selector settings or queue callback are allowed.
- `QueueHeadRead` and `ConsumePrefixAppend` must expose `read_span=[0,q)`, `consume_span=[0,d)`, selected prefix, appendant, and snapshot occurrence identities. In Post variants some consumed symbols are not read; in Wang variants some read symbols persist. Conflating these roles would erase evidenced constructions.
- Ends are properties of the finite word, not out-of-range lattice reads. Fixed, periodic, and reflective boundary policies are not applicable; wrapping or padding would create a different program.
- A typed `InsufficientPrefix` terminal reason is construction-specific. It differs from T16 `NoMatch`, T12 terminal control, an externally requested stop, horizon exhaustion, invalid program data, and a successful event whose successor happens to be empty.
- The Notes' short-to-empty behavior belongs in an explicit reference trace projection/totalizer. It may emit a normalized `{}` frame after the terminal residue for exact-source comparison, but it cannot manufacture another semantic transition or hide the retained terminal state.
- Prefix deletion and endpoint insertion can share a private ordered edit engine only after `QueueSpliceUpdate` validates their coupled queue geometry. A public generic collection of arbitrary edits would weaken the construction and invite callbacks.

## Big Picture Objective

Recover ordinary tag systems as direct finite-word prefix-queue transitions, including their exact Wolfram/Post/Wang selector distinctions, empty appendants, short-word halting, and source-code display convention. Add only a closed prefix source/read, total word table, typed consume-and-tail-append result, queue update law, and terminal/reference-projection boundary. Reuse ordered support and typed orchestration without adding a tag rollout, hidden deque, capacity, compiler, or family flag.

## Catalog Identity

- Stable ID: T17.
- Exact name: Tag Systems.
- Canonical aliases and historical variants: ordinary tag systems, Post tag systems, one-element-dependence tag systems, and Wang lag systems. `Uniform tag systems` is an Index/historical name for ordinary neighbor-independent substitution systems, not T17.
- Entry kind: deterministic finite-word prefix-queue rewrite construction.
- Wolfram base parameters: finite alphabet `Sigma`, positive deletion/read number `n`, complete table `Sigma^n -> Sigma*`, independent finite initial word, and optional horizon/observers.
- Evidenced generic parameters: positive read width `q`, positive deletion number `d`, complete table `Sigma^q -> Sigma*`; Wolfram pins `q=d`, Post pins `q=1`, and Wang pins `d=1` with a wider dependency.
- Search vocabulary: tag system/machine, ordinary/Post/uniform tag, one-element/first-element dependence, lag system/Wang, deletion number, delete/remove/drop/take first/beginning/left, append/add/tag/join/end/right, appendant/block, short/too few/length/halt/stop/extinction/empty, initial word/condition, `TSEvolveList`/`TSToPR`/`CAToTS`/`TagToMTM`/`TS1ToCT`, rule count/number/enumeration, cyclic/multiway tag, PCP, substitution/Turing/CA/recursive emulation, universality, randomness, and Index/history routes.

## Search Log

### Coverage and method

The taxonomy was treated only as search vocabulary. Independent passes searched the monolithic book for direct names, mechanical phrases, deletion/append roles, named historical variants, code symbols, halting/extinction, counts, initial conditions, captions, compilers, universality, and the flattened Index. Every direct construction candidate was inspected in context; cyclic-only and multiway-only results were separated rather than merged into ordinary T17.

| Query family | Canonical hit count or disposition |
|---|---:|
| `tag systems?` / `tag-system` | 175 occurrences on 111 unique lines: 81 before the Index and 30 OCR-interleaved Index lines; all classified. |
| bare `tag`/`tags`/`tagged`/`tagging` | 177 occurrences on 112 unique lines; non-system uses excluded by context. |
| `ordinary tag` / `Post's tag` / `one-element-dependence` | 3 / 2 / 4 unique lines respectively; all Wolfram-versus-Post and universality routes classified. |
| `uniform tag system` / `lag system` / `multiway tag system` | 2 / 3 / 5 unique lines; T13 false friend, Wang variant, and branching construction separated. |
| remove/delete/drop/take + beginning/first | Core, implementation, historical, cyclic, compiler, and unrelated list-operation contexts classified. |
| append/tag/add + block/end | Core, implementation, cyclic, Turing-emulation, and unrelated string contexts classified. |
| `TSEvolve`/`TS1*`/`CAToTS`/`TagToMTM`/`TSToPR`/`TSToPCP` | 85 raw occurrences on 10 lines; the raw count is inflated by corrupted `TS1Step` duplication, and every line was inspected. |
| halting state / reaches `{}` / all elements removed / `Length[#] < n` | 5 construction-bearing lines, all reconciled. |
| fixed-number/beginning/end/first-element mechanical phrases | 2 / 6 / 7 / 4 direct lines respectively, all classified. |
| rule count/number/enumeration / `50,625` | Notes count recovered; flattened Index interleaving rejected as a T17 numbering route. |
| random initial condition / first-element sequence / length plot | Finite seed semantics separated from downstream observers. |
| cyclic/multiway/substitution/CA/Turing/recursive/PCP relations | All construction-bearing routes included or explicitly bounded below. |

Representative commands were `rg -n -i -e '<term>' ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`, followed by exact line-context inspection. Counts in this section are audit metadata, not evidence by themselves.

### Candidate disposition

| Region/candidates | Disposition |
|---|---|
| `1108-1132` | Complete base definition, one- and two-deletion variants, one-deletion/T13 relation, pair-black seed, length observer, and extinction caption included. |
| `1134-1158` | Read only to establish the T18 boundary: cyclic rules add visible step-dependent program control and are not an ordinary T17 option. |
| `7952`, `8032-8046` | CA emulation in both directions included as relations; compilers do not define native state/update. |
| `8058-8078`, `8498-8500` | First-element-dependence tag/Turing/cyclic universality chain included as a Post-variant relation. |
| `11540` | Post historical timeline included; it adds no mechanics beyond Notes. |
| `12294-12313` | Exact Wolfram rule/table, step code, direct prefix patterns, empty appendant, count, randomness observer, Post/Wang distinctions, and examples included. |
| `13265`, `14275` | Finite/integer-like initial-condition limitation classified; the latter explicitly includes ordinary tag systems. |
| `18488-18498` | Exact CA-to-two-tag compiler and seed included only as a relation/observer test. |
| `18514-18530` | First-element tag-to-cyclic compiler classified as a T17/T18 boundary, not ordinary execution. |
| `18794-18806` | Turing-machine emulator of one-element-dependence, delete-two tags included as a relation and parameter guard. |
| `18910-18916` | Recursive-function state encoding and empty-state halt observer included; not a native integer representation requirement. |
| `19294-19302` | PCP reduction's “none of its rules apply” wording used to resolve operational halting. |
| `19324-19331` | Multiway tag systems classified as a separate list-of-strings/branching successor algebra. |
| rule-110 cyclic material after `8172` | Excluded from T17 mechanics except where it explicitly routes through first-element ordinary tags; the evolving rule counter belongs to T18. |
| `uniform tag systems` at `12249` and Index | Classified as a neighbor-independent substitution alias, consistent with T13, not ordinary queue semantics. |

### Split, Index, image, and source-defect audit

- Chapter 3 split lines 429-449 duplicate canonical `BOOK:1108-1132`; split Notes/Index material duplicates the monolith. Canonical provenance below always uses `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md` as `BOOK`.
- `ANKoS-Atlas.md:97-103` is a high-level summary and adds no mechanics beyond the canonical core.
- Mispartitioned `BACK-MATTER/Index/Index.md:199-218` duplicates canonical Notes `BOOK:12294-12313`; it is not the actual flattened Index. The actual Index is embedded near the end of the monolith.
- The flattened Index entry at `BOOK:22150` routes Tag systems to pages 93-94, implementation/density/history at 894, random initial conditions at 949, emulation by CA/Turing/recursive functions and of CA/Turing machines, one-element dependence, multiway tags, undecidability, and universality. All construction-bearing routes were followed. Adjacent column text about string concatenation, sequential substitution, enumeration, or other systems was not assigned to T17.
- `ref/A-New-Kind-of-Science/CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_109_Figure_2.jpeg` was inspected. The main caption and clean Notes establish case (a); an independent transcription/interpreter establishes case (c) as `11->011, 10->101, 01->000, 00->0` from seed `11`, reaching the short residue `0` at event-time step 287 and Notes-normalized `{}` at sample 288.
- The printed Post rules at `BOOK:12313` contain OCR-damaged wildcards/braces. The surrounding prose unambiguously establishes `q=1,d=3` for the binary rule and `q=1,d=2` for the multicolor rule, so the handoff uses those roles without inventing damaged literal syntax.
- `TSEvolveList` uses Mathematica `/.`; an absent prefix row would remain unchanged and be appended, which conflicts with the complete table/count model. Validation therefore rejects missing rows rather than copying this host fallback.
- The count formula is singular at `k=1` only in its quotient form. The equivalent sum `sum_{j=0}^r k^j` supplies the exact limit and avoids an implementation special-case disguised as semantics.

### Ambiguities resolved

1. Wolfram's ordinary T17 appendant depends on the whole deleted prefix: the prose says “these elements,” the two-deletion caption says “based on what these elements are,” the canonical table has all four binary pairs, and the count exponent is `k^n`.
2. Post's historical system is not the same selector: it reads only the first element while deleting `n`. Wang's lag system independently reads more than the first while deleting one. A generic prefix-queue program therefore has distinct positive `q` and `d`; strict Wolfram `tag_system` pins them equal.
3. Empty appendants are native. The canonical case (a) contains `10->{}`, and the rule count includes length zero. This does not imply empty left/read words: `q,d >= 1`.
4. A complete table is required. There are `k^q` input cases in the count and direct canonical rules cover all four pairs. Missing, duplicate, or out-of-alphabet rows are validation errors, never fallback, identity, or terminality.
5. The short-state sources describe two layers. Prefix rules/PCP have no applicable rule once required symbols are absent, so the operational state halts with its residue. `TSEvolveList` deliberately totalizes a requested next sample to `{}`; figure case (c) independently exposes the one-step difference.
6. A successful event may itself create `{}`. That event has one empty successor; a subsequent step attempt returns `Terminal(InsufficientPrefix)`. This is different from a short nonempty terminal residue and from a missing program row.
7. The appendant is attached after the preserved suffix, not substituted at the front. The alternative Notes patterns put `s` before the output, and `Join[Drop[...,n], appendant]` fixes the same order.
8. No canonical integer rule codec was found. The finite count assumes explicit bounds and validates coverage; table serialization, not an invented digit order, is the rule identity.
9. “All elements are eventually removed” is compatible with semantic residue `0`: the published trace convention maps that already-disabled state to `{}` on the next sample. Neither padding nor a hidden deletion event is required.

**Search closure:** direct-name, mechanism, caption, Notes, Index, split, image, historical-variant, rule-count, initial-condition, halt/extinction, observer, emulation, universality, PCP, cyclic, and multiway audits agree. Every unique construction-bearing candidate is included or dispositioned; zero evidence candidates remain unresolved.

## Book Excerpts

All excerpts are from `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`, abbreviated `BOOK`.

### E01 — finite sequence, fixed front deletion, full-prefix choice, and tail append

`BOOK:1110-1112`, Chapter 3, “Tag Systems”:

> A tag system consists of a sequence of elements, each colored say black or white. The rules for the system specify that at each step a fixed number of elements should be removed from the beginning of the sequence. And then, depending on the colors of these elements, one of several possible blocks is tagged onto the end of the sequence.

The state is an ordered word; both ends and the entire deleted prefix have semantic roles.

### E02 — one-deletion mechanics and exact T13 checkpoint relation

`BOOK:1114-1126`:

> Examples of tag systems in which a single element is removed from the beginning of the sequence at each step, and a new block of elements is added to the end of the sequence according to the rules shown. Because only a single element is removed at each step, the systems effectively just cycle through all elements, replacing each one in turn. And after every complete cycle, the sequences obtained correspond exactly to the sequences produced on successive steps in the first three ordinary neighbor-independent substitution systems shown on page 83.
>
> if only one element is removed at each step, then a tag system always effectively acts just like a slow version of a neighbor-independent substitution system

The relation is sampled after complete queue cycles; it does not make a tag event an all-occurrence T13 generation.

### E03 — two-deletion rule, pair-black seed, length observer, and extinction

`BOOK:1128-1132`:

> If two elements are removed at each step ... the behavior that is obtained in this case can often be very complicated.
>
> at each step two elements are removed from the beginning of the sequence and then, based on what these elements are, a specified block of new elements is added to the end of the sequence. ... starting from a pair of black elements. The plots show the total lengths ... Note that in case (c), all the elements are eventually removed from the sequence.

Deletion number two changes the construction's behavior; the plots are derived length observations.

### E04 — cyclic tag systems add a different source of rule choice

`BOOK:1134-1138`:

> In an ordinary tag system, one does not know in advance which of several possible blocks will be added at each step. But the idea of a cyclic tag system is to make the underlying rule already specify exactly what block can be added at each step.
>
> the rule simply alternates on successive steps between these blocks, adding a block at a particular step when the first element ... is black.

The cyclic program phase is visible control belonging to T18, not a T17 boolean option.

### E05 — CA can emulate tag systems only through a different realization

`BOOK:7948-7954`:

> it can take progressively larger numbers of cellular automaton steps to reproduce each successive step
>
> The same kind of problem occurs ... in tag systems. But ... it is still perfectly possible to emulate systems like these using cellular automata.

Variable word growth and queue event time must not be replaced by CA space/time encoding.

### E06 — ordinary tags can emulate CA rules 90 and 30

`BOOK:8030-8046`:

> the same is also true for ordinary tag systems. And even though such systems operate in an extremely simple underlying way ... they can still quite easily emulate cellular automata.
>
> Tag systems that emulate the rule 90 and rule 30 cellular automata. ... Both tag systems involve 6 colors.

This is a compiler/universality relation, not a six-color restriction on native T17.

### E07 — first-element-dependence is the ordinary-tag subset used by cyclic/Turing emulations

`BOOK:8058-8078`:

> get a cyclic tag system to emulate an ordinary tag system with the property that its rules depend only on the very first element that appears at each step.
>
> Emulating a Turing machine with a tag system that depends only on the first element at each step.

The repeated qualifier proves that first-element dependence is a restricted ordinary-tag variant, not Wolfram's general selector.

### E08 — exact complete table, empty appendant, and atomic queue order

`BOOK:12294-12306`, Notes “Implementation”:

> `{{0,0}->{1,1}, {1,0}->{}, {0,1}->{1,0}, {1,1}->{0,0,0}}`
>
> `TSEvolveList[{n_,rule_},init_,t_] := NestList[If[Length[#] < n, {}, Join[Drop[#,n], Take[#,n] /. rule]] &, init,t]`

The alternative explicit patterns place the old remainder `s` before the appendant. The empty output is intentional and direct.

### E09 — finite rule count requires all prefix cases and includes empty words

`BOOK:12308`:

> There are a total of `((k^(r+1)-1)/(k-1))^(k^n)` possible rules if blocks up to length r can be added at each step and k colors are allowed. For r=3, k=2 and n=2 this is 50,625.

There are `k^n` table inputs and `1+k+...+k^r` possible appendants per input.

### E10 — first-element sequence is an observer

`BOOK:12310`:

> To get some idea of the randomness of the behavior, one can look at the sequence of first elements produced on successive steps.

This sampled sequence and the main-text length plot derive from full states; neither is sufficient Markov state.

### E11 — Wolfram, Post, and Wang separate read width from deletion number

`BOOK:12311-12313`, Notes “History”:

> Post's tag systems differ from mine in that his allow the choice of block that is added at each step to depend only on the very first element in the sequence at that step. ... The lag systems studied ... by Hao Wang allow dependence on more than just the first element, but remove only the first element.
>
> he looked at rules that remove three elements at each step

The directly named variants justify `q` and `d` as independent typed data while keeping strict named presets.

### E12 — native initial words are finite

`BOOK:14275`, Notes “Random initial conditions in other systems”:

> The same is true of ordinary and cyclic tag systems.

Here “the same” refers to not readily admitting infinite random initial conditions. T17 does not receive T13's infinite-support variant.

### E13 — exact CA compiler is downstream of ordinary tag semantics

`BOOK:18488-18498`:

> Given the rules for an elementary cellular automaton ... the following will construct a tag system which emulates it
>
> The initial condition ... is `{s[0],s[0],s[1],s[0],s[0]}`. Given a list of all steps ... `Cases[list,{__s}]` picks out successive steps in the cellular automaton evolution.

`CAToTS` emits a two-deletion tag program; the `Cases` expression is a trace observer selecting CA checkpoints.

### E14 — first-element ordinary tags compile to cyclic tags

`BOOK:18514-18530`:

> From a tag system which depends only on its first element ... constructs a cyclic tag system emulating it

The converted seed and history interpretation are encoding/projection layers. T18 must own the cyclic rule phase.

### E15 — Turing emulation preserves delete-two and copy-to-tail roles

`BOOK:18794-18806`:

> If the rules for a one-element-dependence tag system are given in the form `{2,{{0,1},{0,1,1}}}`
>
> Each step of tag system evolution is implemented by having the head ... copy the appropriate elements to the end of the sequence on the right. ... it can only emulate directly rules that delete exactly 2 elements at each step.

The emulator corroborates first-symbol selection, fixed deletion, and remote tail creation while remaining non-native machinery.

### E16 — integer encoding and empty-state search are emulation/observation

`BOOK:18910-18916`:

> With the state of a 2-color tag system encoded as an integer ... a primitive recursive function ... emulates a single step
>
> `mu[...]` returns the smallest t for which the tag system reaches state `{}`—and never returns if the tag system does not halt.

Opaque integer packing is not native state. This empty-state observer follows the Notes trace convention and cannot erase the operational short-residue distinction.

### E17 — operational halting is absence of an applicable rule

`BOOK:19294`:

> a tag system ... ever reaches a halting state (where none of its rules apply)

Combined with exact prefix patterns, this makes a word shorter than the required prefix already terminal even if a plotting totalizer later emits `{}`.

### E18 — multiway tag systems change the successor carrier

`BOOK:19324-19331`:

> one can generalize tag systems ... to allow a list of strings at each step
>
> `Nest[Flatten[Map[ReplaceList[#,rule]&,#],1]&,list,t]`

Lists of strings and all matching successors belong to a branching construction, not a T17 source policy.

### E19 — historical provenance

`BOOK:11540`:

> 1921: Emil Post looks at a simple tag system ... whose behavior is difficult to predict

This corroborates the Post lineage but adds no rule semantics beyond E11.

### E20 — one-element-dependence has a direct first-symbol executor and TM compiler

`BOOK:18556-18568`:

> the evolution of a tag system that depends only on its first element
>
> `Drop[Join[list, First[list] /. subs], n]`
>
> construct a tag system that emulates [a Turing machine]

The extracted executor line is massively duplicated after its intelligible prefix, so only its independently corroborated first-symbol/read and fixed-delete roles are retained. The TM compiler and its seed `{a[i],a[i],c[i]}` are relation fixtures, not base mechanisms.

### E21 — documented universality restrictions

`BOOK:18877`:

> Marvin Minsky showed in 1961 that oneelement-dependence tag systems ... can be universal. Hao Wang in 1963 constructed an example that deletes just 2 elements at each step and adds at most 3 elements—but has a large number of colors.

Universality is a property of restricted tables/alphabet sizes. It neither changes queue execution nor imposes those bounds on the base program.

## Construction Model

### EVIDENCED prefix-queue family and strict T17 preset

Let `Sigma` be a finite declared alphabet and `w in Sigma*` a finite ordered word. The directly evidenced generic data is:

```text
PrefixQueueProgram(
    alphabet=Sigma,
    read_width=q,             # q >= 1
    deletion_number=d,        # d >= 1
    appendants=T,             # total T: Sigma^q -> Sigma*
)
```

Named constructions are data-preserving restrictions:

```text
Wolfram ordinary tag: q = d = n
Post tag:             q = 1, d = n
Wang lag:             q > 1, d = 1
```

No preset changes the executor. The direct `tag_system(n, table)` constructor means Wolfram ordinary tags and validates `q=d=n`; structured `PrefixQueueProgram` data can also express the documented Post and Wang variants without a flag.

The required source is:

```text
eligible(w,P) := len(w) >= max(P.read_width, P.deletion_number)

if not eligible:
    Terminal(state=w, reason=InsufficientPrefix(required=max(q,d), actual=len(w)))
else:
    QueueHeadSource(
        snapshot_id,
        read_interval=[0,q),
        consume_interval=[0,d),
        read_occurrence_ids=w.ids[0:q],
        consumed_occurrence_ids=w.ids[0:d],
    )
```

The old-snapshot read, rule result, and commit are:

```text
prefix     = old.symbols[0:q]
appendant  = T[prefix]                     # exact required row
result     = ConsumePrefixAppend(source, prefix, appendant)
next       = old.symbols[d:] ++ appendant
```

`T` has exactly one row for each member of `Sigma^q`; outputs may be empty and must be alphabet-closed. Duplicate/missing keys, wrong key widths, symbols outside `Sigma`, nonpositive widths, stale sources, and read/result mismatches are errors. They do not turn into identity, skip, partial matching, or terminal outcomes.

`QueueSpliceUpdate` commits deletion and tail insertion atomically. Old occurrence IDs `[0,d)` are consumed. Old IDs `[d,|w|)` persist in the same order, even though their row-local positions shift. Output IDs are created at the tail in appendant order. When `q<d`, some consumed occurrences were not rule inputs; when `q>d`, the read occurrences `[d,q)` persist in the successor. This is precisely why the two spans cannot be conflated.

The update can internally lower to ordered edits against the same old snapshot:

```text
delete [0,d) -> epsilon
insert appendant at old endpoint |w|
```

but only after the public queue validator proves the geometry and shared event. A generic public edit list, T16 front replacement, or two separately observable commits would permit invalid reorderings. In particular:

```text
old = 0111, d=2, T[01]=10
tag result      = 11 ++ 10 = 1110
front replace   = 10 ++ 11 = 1011       # wrong construction
```

| Dimension | T17 semantics |
|---|---|
| State/support | Explicit finite discrete ordered word with semantic front/back; no cursor/control. |
| Alphabet | Finite declared `Sigma`; table keys/outputs are alphabet-closed. |
| Program | Positive `q,d` plus a complete `Sigma^q -> Sigma*` table. Wolfram base pins `q=d`. |
| Source | Zero or one old-snapshot `QueueHeadSource`, requiring both spans to exist. |
| Read | Exact ordered leading `q` symbols; no padding, wrap, partial key, or default. |
| Result | Typed `ConsumePrefixAppend(source, prefix, appendant)`. |
| Update | Atomic `QueueSpliceUpdate`: consume old `[0,d)`, preserve old suffix, append newborns at tail. |
| Successor | One deterministic successor when eligible; zero with retained residue for `InsufficientPrefix`. |
| Seed | Independent finite word; canonical figures use `11`. Empty/short seeds are valid terminal states. |
| Boundary | None: word ends are semantic and no position outside the word is read. |
| Trace | Ragged snapshots plus prefix/consumption/creation event data; first-symbol, length, CA checkpoints, and extinction normalization are downstream. |

### Structural, length, and terminal invariants

For every successful event:

```text
prefix == old[0:q]
next == old[d:] ++ T[prefix]
|next| == |old| - d + |T[prefix]|
next[0:|old|-d] == old[d:]
```

At occurrence level:

```text
consumed_ids == old.ids[0:d]
persisted_ids == old.ids[d:]
next.ids[0:|old|-d] == persisted_ids
produced_ids are fresh and ordered after persisted_ids
read_ids == old.ids[0:q]
```

The appendant is read from the old prefix before either edit. A newborn is never eligible inside its creating event. There is exactly one logical event; append-before-read, iterative deletion, and in-place rescanning are invalid.

When `len(w)<max(q,d)`, the semantic transition relation returns zero successors and retains `w` as its final state. For Wolfram `q=d=n`, this is exactly `len(w)<n`. Distinguish:

- `Advanced(next={})`: a valid table row with an empty appendant consumed the whole word;
- `Terminal(InsufficientPrefix,residue={})`: the next step attempt from that empty successor;
- `Terminal(InsufficientPrefix,residue={0})`: a short nonempty word has no applicable prefix rule;
- `ReferenceExtinctionSample({})`: the Notes projection requested one sample after that terminal residue;
- `Horizon`, external stops, invalid tables, stale sources, and execution errors.

The exact Notes-compatible projector is allowed to map a newly encountered short terminal residue to `{}` on the next requested sample and then pad `{}` for additional requested samples. It must carry the original terminal reason/residue and label the synthesized frames; it is not the default semantic trace and cannot be resumed as if transitions occurred.

### Complete-table count and identity

With `k=|Sigma|`, maximum appendant length `r`, and read width `q`, the number of possible output words is:

```text
A(k,r) = sum(j=0..r, k^j)
```

and the number of complete tables is:

```text
A(k,r)^(k^q)
```

For `k>1`, `A=(k^(r+1)-1)/(k-1)`; for `k=1`, `A=r+1`. Wolfram's direct `q=n=2,k=2,r=3` fixture yields `15^4=50,625`. This proves cardinality under explicit bounds but not a digit significance or integer enumeration. Program identity is structured `(alphabet,q,d,ordered canonical key/table rows)` serialization.

### Exact trajectory and relation oracles

Canonical case (a), from E08, `q=d=2`, seed `11`:

```text
00 -> 11
10 -> epsilon
01 -> 10
11 -> 000

t0   11
t1   000
t2   011
t3   110
t4   0000
t5   0011
t6   1111
t7   11000
t8   000000
t9   000011
t10  001111
t11  111111
t12  1111000
t13  11000000
t14  000000000
t15  000000011
```

Every transition independently checks prefix selection, two-symbol consumption, suffix persistence, tail order, empty-output support, and the length equation.

Figure case (c), independently transcribed and interpreted, `q=d=2`, seed `11`:

```text
11 -> 011
10 -> 101
01 -> 000
00 -> 0

t278 0000000000
t279 000000000
...
t286 00
t287 0           # semantic Terminal(InsufficientPrefix)
t288 {}          # TSEvolveList/reference extinction sample only
```

This is the required discriminator between operational halt and published history normalization.

For the one-deletion/T13 relation, use `T[1]=10`, `T[0]=01`, seed `1`:

```text
tag event frames:
1 -> 10 -> 010 -> 1001 -> 00110 -> 011001 -> 1100101 -> 10010110

complete-cycle checkpoints:
1, 10, 1001, 10010110
```

The checkpoints are exactly T13 generations under `h(1)=10,h(0)=01`; intermediate tag states remain distinct and must not be dropped from native traces.

### Adversarial conformance fixtures

1. **Whole prefix, not first symbol:** with a complete binary `q=d=2` table containing `00->0` and `01->1`, assert `001->10` and `011->11`. Both prefixes begin with `0`; a Post selector collapses them incorrectly.
2. **Delete/read distinction:** Post `q=1,d=3` consumes three occurrences but selects solely from the first. Wang `q=2,d=1` selects from two occurrences while the second persists. Validate both event ID sets.
3. **Tail append, not front replacement:** `0111` with `01->10` yields `1110`, never `1011`.
4. **Empty appendant:** `1001` with `10->epsilon` yields `01`; exact `10` yields `{}` through a successful event.
5. **Newborn deferral:** `q=d=1`, `A->AA`, seed `A` gives lengths `1,2,3,4`, not parallel doubling or in-event recursion.
6. **Short boundary:** `q=d=2`, seed `0` is immediately terminal with residue `0`; no fabricated blank, partial key, boundary policy, no-op, or automatic semantic `{}`.
7. **Complete table:** reject missing/duplicate keys and extra/wrong-width keys. Specifically prove a missing prefix cannot inherit Mathematica `/.` identity and append itself.
8. **Alphabet closure:** reject key/output/seed symbols outside `Sigma`; none is coerced to a pad or blank.
9. **Provenance:** repeated symbols still consume exact leading IDs, preserve all suffix IDs in order, and create fresh tail IDs.
10. **Length law:** test shrinking, equal, and growing appendants, including zero length and successful empty successor.
11. **No cyclic leakage:** ordinary T17 results are independent of step number. A cyclic program phase cannot be supplied to this spec.
12. **No branch leakage:** a multiway table/list returns multiple strings under its own successor algebra and is rejected by deterministic T17.

### Variant disposition

| Candidate | Disposition |
|---|---|
| Wolfram one- and two-deletion systems | Native `q=d=n` parameter choices; figures directly cover `n=1,2`. |
| Arbitrary positive Wolfram deletion number | Native structured parameter; Notes implementation/count use general `n`. |
| Post tag systems | Direct historical variant `q=1,d=n`; same prefix-queue algebra, stricter read role. |
| Wang lag systems | Direct historical variant `q>1,d=1`; same algebra, read may include persistent symbols. |
| Empty appendant | Native table value in `Sigma*`; directly evidenced. |
| Missing table row | Invalid program; never fallback, identity, or halt. |
| Short word | Intrinsic zero-successor `InsufficientPrefix` with residue retained. |
| Short-to-empty sample | Explicit Notes/reference projection, not a native transition. |
| One-deletion/T13 equivalence | Checkpoint relation after complete cycles; no executor substitution. |
| Cyclic tag system | T18: adds step-dependent cyclic control and different rule choice. |
| Multiway tag system | Separate branching/list-of-strings successor algebra. |
| CA/Turing/recursive-function/PCP encodings | Relations, compilers, and observers; never native representation. |
| Length/first-symbol/compressed histories | Downstream observers over full trace. |
| Infinite random initial word | Not native ordinary-tag seed. |
| Integer rule code | Not evidenced; only bounded rule cardinality is canonical. |

## Current API Fit

| Concern | Fit | Finding |
|---|---|---|
| Canonical dense domain/address | SEMANTIC MISMATCH | `simple_programs.md:1-24,87-113` fixes state on dense `[t,x,y,z]`; T17 needs a changing finite word whose row-local positions shift after every deletion. |
| Alphabet | DIRECT | The documented alphabet/value-set responsibility (`:200-233`) can represent finite symbols if it does not also encode queue roles/state. |
| Seed | PRINCIPLED EXTENSION | Current selector/fill/distribution seeds (`:235-290`) materialize a fixed slice; T17 requires an explicit finite word independent of program and horizon. |
| Boundary | NOT APPLICABLE | Fixed/periodic/reflective policies (`:292-358`) resolve spatial out-of-range reads. T17 instead has an intrinsic insufficient-prefix terminal predicate. |
| Neighborhood/read | SEMANTIC MISMATCH | Relative coordinate stencils (`:360-731`) cannot express a semantic word prefix of program-declared width, especially when read and deletion spans differ. |
| Frontier/source | SEMANTIC MISMATCH | Writable next coordinates (`:1412-1510`) do not describe one old-snapshot queue-head event or typed short-source failure. |
| Rule | SEMANTIC MISMATCH | Current rules return scalar target values (`:1767-1793`); T17 requires a complete structured word table and `ConsumePrefixAppend`. |
| Formulaic rule | SEMANTIC MISMATCH | Whole-field formulas (`:2036-2073`) could hide the queue step but would erase validation, provenance, and shared executor responsibilities. |
| Update | SEMANTIC MISMATCH | Parallel fixed-support assignment/copy (`:1767-1793,2156-2199`) cannot delete a prefix and append a remote variable word atomically. |
| Successor/termination | PRINCIPLED EXTENSION | The fixed-horizon model lacks `InsufficientPrefix`, retained residues, and reference-projection metadata. |
| Trace/encoding | SEMANTIC MISMATCH | A persistent dense trajectory cannot preserve ragged words, occurrence identities, queue events, terminal residues, or synthetic extinction samples truthfully. |
| Rule ID/count | PARAMETERIZATION | Exhaustive table cardinality can be computed under `k,q,r`; no canonical integer ID may be required. |
| Observers | PARAMETERIZATION | Length, leading-symbol, complete-cycle, CA-checkpoint, and Notes-extinction views are derivable once native states/events/outcomes are retained. |

## Current Runtime Fit

- `alphabets.symbolic()` is useful finite-value machinery (`src/ca/alphabets.py:146-177`), but defines neither word order nor prefix/table roles.
- `CoordinateSpace` is finite rank 0-3 (`src/ca/loci.py:31-94`). Dense coordinate proximity cannot make row-local index zero a persistent queue head or preserve occurrence identity across shifts.
- `Dynamics.shape` is mandatory/fixed (`src/ca/specs.py:24-55`), and rollout rejects shape changes (`src/ca/rollout.py:40-75`). T17 length changes by `-d+|appendant|` on every event.
- `RawEpisode`/`RawBatch` store one NumPy state array and integer `rule_id` (`src/ca/specs.py:58-82`). They cannot hold structured tables, ragged snapshots, event provenance, terminal residues/reasons, or labeled reference samples.
- `frontiers.py` exposes only dense `time_slice` (`src/ca/frontiers.py:38-80`), and rollout rejects other frontiers (`src/ca/rollout.py:825-831`). There is no queue-head source or insufficient-source result.
- `neighborhoods.py` builds finite relative coordinate stencils (`src/ca/neighborhoods.py:110-549`). A prefix is topology/endpoint-relative, not a centered stencil or padded gather.
- `Rule` stores a family string, optional integer ID, `Any` params, and optional callable (`src/ca/rules.py:30,65-78`). None validates a total `Sigma^q -> Sigma*` table; `formulaic(fn)` would be a prohibited whole-queue callback.
- Family dispatch in `_rollout_states`/`_rollout_batch_states` (`src/ca/rollout.py:145-212`) cannot gain a `tag` branch. The spatial path preallocates fixed arrays and computes scalar per-site writes (`:576-660`), so it also has the wrong update carrier.
- `canonical_coords` repeats one dense grid at each time (`src/ca/rollout.py:215-267`). A truthful lowering must keep occurrence/event tables and mark row-local word coordinates as observations, not identity.
- Seeds render fixed arrays (`src/ca/seeds.py:879-939`) and datasets stack equal shapes (`src/ca/datasets.py:313-334`). A fixed-capacity deque, padding symbol, mask, truncation, or overflow is not native T17 semantics.
- Existing tests enforce current fixed-shape/full-frontier behavior but contain no prefix-read/delete discriminator, tail append, empty output, complete word table, short-residue halt, reference normalization, newborn timing, or queue provenance case. They must remain passing while the raw boundary is extended rather than weakened.

## Principles Audit

| Principles | T17 result |
|---|---|
| 0-3 | T16 single-splice semantics fails the tail-order discriminator. Rederive a closed queue event/result/update; retain only genuinely shared ordered support, outcomes, and private edit machinery. |
| 4 | `ConsumePrefixAppend` is an explicit rule result and `QueueSpliceUpdate` is a public sibling update law. Empty output is represented directly, not as a flag. |
| 5 | The finite word is complete Markov state for ordinary T17. No deque cursor, capacity, program phase, last prefix, or extinction flag is hidden in the executor. |
| 6-8,12 | Occurrence identity, row-local position, ragged storage, dense ANKoS lowering, first-symbol/length plots, and reference extinction samples remain separate. |
| 9 | Read width, deletion number, total prefix table, source validation, and update spans are intrinsically coupled through one immutable program/result contract; seed/horizon/observers remain independent. |
| 10 | `tag_system(n,table)` is a strict ordinary-program preset over the generic protocol. Post/Wang are structured restrictions, not family dispatch or booleans. |
| 11 | Old-prefix read, fixed deletion, suffix-before-append order, one-event timing, and short terminal threshold are defining semantics. Host list/deque implementation is incidental only if equivalent. |
| 13-15 | Whole-prefix/first-symbol, `q<d`/`q>d`, tail/front, empty/missing, newborn, short-residue/reference-empty, provenance, and complete-table adversaries are mandatory. |
| 16 | Typed prefix/table/result/update/outcome boundaries are architecture; callbacks, CA/TM compilers, fixed buffers, padding, fallback rows, and cyclic/multiway branches are shims. |

The substantive shared orchestration remains:

```text
source  = SOURCE.select(old_state, program.applicability)
reads   = READ.read(old_state, source)
result  = RULE(program, source, reads)
outcome = UPDATE.apply(old_state, result)
```

T17 validates this shell only because each boundary is construction-bearing: `RequiredQueuePrefix`, `QueueHeadRead`, a total word table, `ConsumePrefixAppend`, and `QueueSpliceUpdate`. Replacing those with a whole-word function would make the shell decorative. No earlier public behavior changes: T13 remains nonerasing/full-generation, and T16 remains nonerasing/single-interval. The shared private ordered edit representation alone expands to carry epsilon insertions/deletions after public validation.

## Detailed Implementation Plan

1. Record the closed direct/Notes/Index/split/image/history/variant/halting/count/emulation audit and the operational/reference short-state distinction.
2. Reuse T13 finite ordered words and occurrence provenance; make generic low-level `Word` capable of empty values while preserving `NonEmptyWord` at T13/T16 public validators.
3. Add immutable `PrefixQueueProgram(q,d,total_table)`, strict Wolfram `tag_system(n,table)`, and evidence-backed Post/Wang structured restrictions without booleans or executor branches.
4. Add `RequiredQueuePrefix`, `QueueHeadSource`, exact prefix reads, typed `ConsumePrefixAppend`, and policy-guarded `QueueSpliceUpdate` over the old snapshot.
5. Extend typed outcomes with `InsufficientPrefix` and add an explicitly labeled Notes extinction projector; prove native terminal residues, successful empty outputs, horizons, and errors remain distinct.
6. Specify canonical case (a), figure case (c), T13 checkpoint, count, selector/delete, tail-order, empty/missing, newborn, lineage, and shared-executor conformance tests.
7. Reintegrate the plan, evidence index, and design ledger; re-audit T13/T16 public nonempty guarantees and reopen them only if their behavior changes.

## Goal 2 Implementation Stage

### G2-T17 — Prefix-queue programs, consume-and-tail-append update, and short-residue terminal projection

**Dependencies:** G2-T13 finite ordered sequence state, occurrence handles, ragged snapshots, and structural provenance; G2-T16 policy-guarded private ordered edits; G2-T12/T16 typed advanced/terminal/stop/horizon/error outcomes; synthesis-selected generic source/read/rule/update orchestration. T17 reuses neither T13's source coverage/commit nor T16's match selection/public splice.

**Implementation areas:**

- Ordered-state module: reuse finite `OrderedSequence`; add/use `Word[Symbol]` including epsilon at generic result/edit level. Retain `NonEmptyWord` wrappers in T13/T16 programs so T17 cannot silently broaden them.
- Prefix-queue program module: immutable `PrefixQueueProgram(alphabet,read_width,deletion_number,appendants)` with positive widths, canonical `Sigma^q` key order, exactly one row per key, alphabet-closed `Word` outputs, and no rule-ID requirement. Preserve structured serialization and equality.
- Presets: `tag_system(alphabet,n,appendants)` pins `q=d=n`. If exposed, `post_tag_system` and `lag_system` construct the same program data with their evidenced restrictions; no flag, callback, or family name reaches execution.
- Source/frontier module: `RequiredQueuePrefix` returns `QueueHeadSource(snapshot_id,read_span,consume_span,read_ids,consumed_ids)` or typed `InsufficientPrefix`. It consumes widths from the authoritative program applicability object.
- Read module: `QueueHeadRead` validates snapshot ownership, exact intervals, occurrence order, and key width, returning the old leading `q` symbols. It never pads, wraps, partially reads, or observes newborns.
- Rule/result module: exact total lookup returns `ConsumePrefixAppend(source,prefix,appendant)`. The result carries enough evidence for update validation; there is no `Any`, default row, identity fallback, or whole-word callable.
- Update module: `QueueSpliceUpdate` atomically preserves `old[d:]` and appends fresh output. It validates the shared event geometry and emits a `TagEvent` with read/consumed/persisted/produced IDs. A private `ApplyOrderedSpans` may execute delete-at-zero plus insert-at-old-end only after this validation.
- Outcome module: `TerminalReason.InsufficientPrefix(required,actual)` retains the exact residue once and yields zero successors. Keep successful empty successors, `NoMatch`, terminal control, external stops, horizons, invalidity, and errors distinct.
- Reference projection module: opt-in `WolframTagHistoryProjection` reproduces `TSEvolveList` short-to-empty sampling with labels linking synthetic `{}` frames to the terminal residue/reason. It is downstream of execution and never changes resumption/state equality.
- Generic executor: run T17 entirely through typed source/read/rule/update/outcome protocols. Dispatch by result/update types supplied by the spec, never by T17/catalog name.
- Structured raw trace: ragged word snapshots, outcomes, and optional `TagEvent`s. Downstream lowerings may emit row-local `(t,x,0,0,symbol)`, length/first-symbol series, T13/CA checkpoints, and reference extinction frames without feeding them back.
- New `tests/test_t17_tag_systems.py` plus shared word/edit/outcome/trace conformance tests.

**Canonical and adversarial tests:**

1. Assert canonical case (a) exactly through at least `t15`, including selected prefixes, appendants, lengths, and consumed/persisted/created IDs.
2. Assert the canonical empty row: `1001->01` and `10->{}` are successful events; a later step from `{}` is terminal, not the same event.
3. Assert figure case (c) endpoints: seed `11`, `t278=0000000000`, `t286=00`, operational terminal residue `t287=0`, and projected empty sample `t288={}`. Default semantic history stops at `0`.
4. Assert the one-deletion relation: tag checkpoints after event counts `1,3,7` equal T13 generations for `1->10,0->01`, while intermediate tag frames and event provenance remain present.
5. Whole-prefix discriminator: complete table with `00->0,01->1` maps `001->10`, `011->11`; reject a first-symbol-only implementation for Wolfram T17.
6. Post/Wang role tests: for `q=1,d=3`, assert all three front IDs are consumed but only the first is read; for `q=2,d=1`, assert both are read but the second persists.
7. Tail-order discriminator `0111 -> 1110` under `01->10`; reject T16-style `1011`, append-before-drop, and two-phase visible states.
8. Newborn test `A->AA` with `q=d=1`: lengths `1,2,3,4`; no same-event read, T13 parallel doubling, or callback recursion.
9. Short seeds of every length `<max(q,d)` retain exact residues and yield `InsufficientPrefix`; no pad, blank, boundary, partial row, no-op, or implicit semantic emptying.
10. Reject nonpositive widths, incomplete/duplicate/extra/wrong-width tables, out-of-alphabet keys/outputs/seeds, stale sources, mismatched reads/results, and invalid spans. None becomes terminal, fallback, or identity.
11. Assert `A(k,r)^(k^q)` for bounded tables, including `15^4=50,625` and the `k=1` sum case. Do not invent an integer rule codec.
12. Prove repeated symbols retain identity correctly: consume exact front IDs, preserve suffix IDs/order, create fresh ordered tail IDs, and reconstruct every successor from the event.
13. Derive length, first-symbol, complete-cycle, CA-checkpoint, and extinction-projection observers from the same full trace; observation choices cannot alter state or event count.
14. Reject cyclic program control and multiway successor carriers at spec validation. T18/T30-like behaviors cannot be selected as modes of T17.
15. Run T01/T09/T12/T13/T16/T17 through the same typed orchestration and statically reject tag family switches, formula/queue callbacks, fixed-capacity deque/ring buffers, padding/masks, CA/TM/recursive compilers, opaque integer packing, and `Any` results.
16. Re-run all T13/T16 conformance tests to prove their public nonempty contracts and update laws remain unchanged despite epsilon support in private word/edit machinery.

**Completion evidence:** all canonical/adversarial and existing tests pass; Wolfram, Post, and Wang read/delete roles are inspectable; each eligible event performs exactly one old-prefix read and atomic consume/tail-append; incomplete input yields a retained typed residue; Notes projection is explicit; ragged words/events survive the raw boundary; T13/T16 behavior is unchanged; no T17 rollout branch, callback, capacity, padding, compiler, hidden phase, default row, or fake transition exists.

## No-Cheating Checks

- No tag-family rollout, queue-special executor, `is_post`/`is_lag`/`allow_empty` flags, or string family switch.
- No unrestricted whole-word formula, deque callback, predicate, host `ReplaceAll`, or `Any` result containing the transition.
- No table default, missing-row identity, duplicate-row precedence, partial prefix, fabricated blank, padding, wraparound, or boundary gather.
- No bounded deque/ring buffer, maximum length, overflow failure, truncation, mask, or fixed tensor presented as the finite word.
- No replacing the prefix in place, inserting before the suffix, exposing delete and append as separate semantic steps, or reading newborns in their creating event.
- No conflating read and consumed spans; Post and Wang discriminators must remain observable in typed sources/events.
- No treating short residue, successful empty output, missing table row, no-op, external stop, horizon, invalidity, and error as one halt path.
- No silently using the Notes short-to-empty totalizer as native semantics; synthetic samples must retain provenance and labels.
- No cyclic step counter hidden in ordinary T17 state/executor; T18 remains separate.
- No multiway list/branch successor algebra passed as a selector option.
- No CA/Turing/recursive/PCP compiler or integer encoding used to claim native support.
- No length or first-element observation fed back into rule choice; no row-local coordinate treated as persistent occurrence identity.
- No weakening T13/T16 nonempty validators merely because the private ordered edit core now supports epsilon.
- No existing fixed-support tests weakened; extend the raw boundary truthfully and preserve prior conformance.

## Completion Requirements

- [x] All direct names, aliases, captions, Notes, Index entries, splits, images, historical variants, duplicates, source defects, and false positives are resolved.
- [x] All unique construction-relevant excerpts have canonical provenance and disposition.
- [x] Finite state/front/back, read/delete roles, total table, empty appendant, atomic tail update, seed, successor, terminal residue, reference projection, parameters, and observers are reconstructed.
- [x] Canonical case (a), figure case (c), T13 checkpoints, bounded count, and adversarial selector/delete/order/empty/short/provenance invariants have independent conformance oracles.
- [x] Current API/runtime/test fit and T13/T16 reuse/divergence are explicit under Principle 0.
- [x] Goal 2 implementation/conformance handoff is implementation-ready without a family rollout, callback, capacity, padding, compiler, or fallback.
- [x] Global ledgers and plan are reintegrated and verification checks pass.

## Stage Results

T17 is complete with zero unresolved evidence candidates. Wolfram's ordinary tag system is a finite ordered word plus a complete `Sigma^n -> Sigma*` table: read and delete the same leading `n`, then atomically preserve the suffix and append the chosen word. Post and Wang variants prove that generic read width and deletion number are independent, while strict presets preserve each named construction. Empty appendants are direct and widen only the private word/edit carrier; T13 and T16 retain their public nonempty laws. `ConsumePrefixAppend` plus `QueueSpliceUpdate` is a new public sibling update because T16 front replacement fails tail order, though ordered support, provenance, typed outcomes, and a validated private span-edit kernel remain shared. Operational short input has zero successors with its residue retained; the Notes short-to-empty behavior is an explicit reference projection, independently guarded by figure case (c)'s `0` at step 287 and `{}` at sample 288. Complete-table validation, canonical case (a), one-deletion/T13 checkpoints, read/delete and tail-order discriminators, and provenance/length laws make the Goal 2 handoff executable. T01/T09/T12/T13/T16 remain complete and unchanged; no stage is reopened. Focused source-reference, coverage, whitespace, and 102-test baseline verification passed. Next: T19 Register Machines.
