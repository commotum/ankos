# 3-T09-MOBILE

Status: **COMPLETE — EVIDENCE AND ARCHITECTURE RECLOSED**

Architecture authority: the T09 row, commuting tagged representation, and runner contract in `architecture-audit.md` supersede incompatible separate-control/head-packing claims below.

## Current Facts

- Reopening finding: visibility of the active role does not require a separate control object. `Plain(bit) | Active(bit)` preserves the cell value and active marker losslessly, with exactly one `Active` cell as a validated invariant.
- The source-frontier conclusion remains valid for the broad simple-program algebra: `FRONTIER` selects the unique tagged active cell where the native rule fires. The current writable-coordinate-only schema wording is the CA-shaped realization to revise; typed rule writes name both affected targets.
- The compact 65,536-rule mobile table remains the native program identity; a structural lowering to tagged-cell assignments is not the identity of an arbitrary four-color cellular-automaton table.

- Exact catalog row: T09, CSV line 10, `Mobile Automata`.
- Complete taxonomy seed: `ref/notes/CA-Types.md:207-238`.
- Canonical source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md` (abbreviated `BOOK`).
- A basic mobile automaton has a fixed ordered 1D binary field and exactly one visible active position. Only the active/source cell fires at a step.
- The rule reads the physical left/self/right triple, writes a new value at the old active cell, and moves the active position exactly one cell left or right. The two state changes are one atomic transition.
- There are 8 binary input triples and 4 results per triple (`2` colors x `2` directions), hence `4^8 = 65,536` rules.
- The canonical Notes example is the code pair `{35,57}`. With `i=4*left+2*self+right`, the new value is `(35>>i)&1` and displacement is `1-2*((57>>i)&1)`.
- T09 resolves a T01 ambiguity: a frontier selects firing/source loci. Effect targets belong to rule results. In T01 source and target coincide; in T09 the assignment targets the source while control moves to a neighbor.
- Current state, frontier, rule, update, boundary, and raw-trace mechanisms cannot express T09 without visible control and typed compound effects. No mobile runtime or conformance test exists.

## Updated Assumptions

- The active position is a visible control role. Canonically it may be the unique `Active(bit)` tag in a composite finite ALPHABET; a factored position is an optional lossless view. Visualization marks, metadata, and executor locals are invalid substitutes.
- “The active cell and its left and right neighbors” on `BOOK:11965` names the participants, not tuple order. The executable `Take[list,{n-1,n+1}]` on `:11968-11970` and the rule figure establish physical `[left,self,right]` order.
- A frontier is where a rule fires, not a list of all locations a result might mutate. This re-derivation preserves T01 behavior and extends its protocol honestly.
- The native rule returns `(new_bit,displacement)`. With `Plain(bit) | Active(bit)`, it lowers to two ordinary label writes—`source -> Plain(new_bit)` and `destination -> Active(old_destination_bit)`—applied atomically from one snapshot.
- The Notes finite-list guard does not define wrapping, reflection, truncation, or halting. It is a defined-input guard on the sample implementation around a construction that can use an infinite initial cell sequence.
- Record-extrema compression and causal networks are derived observables. They must not feed the next transition.
- Extended mobile automata, generalized mobile automata, Turing machines, 2D/network variants, and CA/substitution encodings are distinct constructions or emulations, not T09 options.

## Big Picture Objective

Exhaustively recover basic mobile automata and use them to validate the broad SimpleProgram protocol. Derive the smallest source/read/write/update semantics with a visible tagged active role and atomic writes, without opaque packing, hidden state, fixed capacity, callbacks, or a mobile-family rollout.

## Catalog Identity

- Stable ID: T09.
- Exact name: Mobile Automata.
- Taxonomy section: 9, `ref/notes/CA-Types.md:207-238`.
- Entry kind: fixed-support controlled transition construction.
- Search vocabulary: mobile automaton/automata, sequential automata (Index alias), active cell, single active cell, head/dot, position of the active cell, move/displacement left or right, update one cell, immediate neighbors, two colors, fixed line/array, 65,536/65536, `{35,57}`, `MAStep`, `MAEvolveList`, compressed evolution/form/version, record extrema, random initial cells, extended/generalized/2D/network/reversible mobile automata, Turing comparison, substitution encoding, and CA emulation.

## Search Log

### Reproducible searches

The taxonomy section was read first. Case-insensitive fixed-string searches were run on `BOOK` for each vocabulary term; combined direct-name/control/function queries produced 135 candidate lines. Every hit was inspected in section context. Targeted number, compression, schedule, boundary, Notes function, Index, and cross-type searches closed common-term remainders.

| Query | Matching canonical lines |
|---|---:|
| `mobile automata` | 71 |
| `mobile automaton` | 61 |
| `active cell` | 47 |
| `single active cell` | 7 |
| `65,536` / `65536` | 5 / 2 |
| `4,294,967,296` | 8 |
| `compressed evolution` / `compressed form` / `compressed version` | 4 / 10 / 2 |
| `position of the active cell` | 3 |
| `colors of its immediate neighbors` | 1 |
| `one cell at a time` / `single cell gets updated` | 1 / 1 |
| `MAEvolveList` / `MAStep` | 2 / 5 |
| `generalized mobile automata` / `extended mobile automata` | 5 / 0 |
| `sequential automata` | 1 |
| `mobile cellular`, `moving autom`, `moving head` | 0 each |

Representative command form:

```bash
rg -n -i -F '<term>' ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
rg -n -i -e 'mobile automata?' -e 'active cell' -e 'MAStep' -e 'MAEvolveList' ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
```

### Candidate disposition

| Disposition | Canonical candidates | Resolution |
|---|---|---|
| Base construction/observation | `848-864`, `874-878`, `982`, `5818-5820`, `5836-5848`, `5874`, `11955-11980`, `11995`, `14275`, `16388-16398` | Included below; establishes state, source, read, result, update, cardinality, no halt, seed/control, and observables |
| T10 extended write scope | `882`, `890`, `898`, `904`, `11982-11993`, `16066-16068` | Followed and included as boundary evidence; three-cell writes are not basic T09 |
| T11 generalized activity | `916-934`, `12008-12010` | Multiple active cells plus split/disappear are a later construction |
| T12 contrast | `940-948` | Turing head has internal states and reads no neighboring tape colors |
| Other topology variants | `13679`, `16400`, `16648-16654` | 2D/network variants change topology, movement set, or replacement scope |
| Explicit emulations | `5926-5938`, `7924-7938`, `8004-8014`, `16442`, `18352-18361`, `18457-18463` | Retained as rejected-shortcut/cross-type evidence, never native fit |
| Behavior/history only | `868-872`, `880`, `912-914`, `958`, `1042`, `1352-1360`, `4136`, `4196`, `5822-5830`, `5870`, `11996`, `12002` | Distribution, complexity, history, motion plot, or period adds no construction primitive |
| Derived causal analysis | `5846-5922`, `16388-16398` | The construction-to-observable mapping is recorded; network properties do not enter state |
| Index/navigation | `20840`, `20898`, `20946`, `20957`, `20965`, `21014`, `21168`, `21213`, `21521`, `21683`, `21771`, `21893`, `21899`, `21927`, `21933`, `21994`, `21998`, `22096`, `22316`, `22352`, `22380`, `22390` | All targets followed; `Sequential automata` redirects to Mobile automata; no primary construction prose |

Number/common-term remainder: mobile `65,536` hits are `864,872,880`; the other occurrences (`1238,14109`) are unrelated. Only `882` of the eight `4,294,967,296` hits is T10. Relevant compression hits are `874,878,890,898,912,11995`; all others describe different systems. `updated sequentially` at `16446` and `18111` concerns sequential CA/neural systems. No base-boundary term produced wrap/reflect evidence.

### Split-file and image audit

- All matching Markdown was searched: canonical monolith, split Chapters 3/7/9/11/12, malformed BACK-MATTER Notes/Index/Colophon splits, and the Atlas. Every split/Atlas hit duplicates the monolith or is summary/navigation; no unique passage exists outside `BOOK`.
- The canonical rule image at `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_86_Picture_8.jpeg` was inspected. It displays physical left-to-right triples with the active dot on the center cell, corroborating the executable `[left,self,right]` order.
- `BOOK:11965`'s wording was explicitly reconciled with `Take[list,{n-1,n+1}]`: the prose lists participating cells; the executable contiguous sublist and figure determine ordering. This candidate is resolved, not left ambiguous.

**Search closure:** every one of the 135 combined-query candidates, targeted-number/compression remainder, split-file match, Index link, variant, and emulation cross-reference is included, labeled duplicate/behavior, or assigned to another construction. Zero T09 candidates remain unresolved.

## Book Excerpts

All excerpts are verbatim from `BOOK`; code and OCR are preserved.

### E01 — active source, local read, compound result, binary line, and rule count

`BOOK:850-864`, Chapter 3, “Mobile Automata”:

> Mobile automata are similar to cellular automata except that instead of updating all cells in parallel, they have just a single "active cell" that gets updated at each step-and then they have rules that specify how this active cell should move from one step to the next.
>
> The rule applies only to this active cell. It looks at the color of the active cell and its immediate neighbors, then specifies what the new color of the active cell should be, and whether the active cell should move left or right.
>
> a mobile automaton consists of a line of cells, with each cell having two possible colors. ... a mobile automaton has only one "active cell" ... at any particular step. The rule ... specifies both how the color of this active cell should be updated, and whether it should move to the left or right.
>
> one can enumerate all possible rules of this kind; it turns out that there are 65,536 of them.

### E02 — record-extrema compression is an observable

`BOOK:874-878`, same section:

> Compressed versions of the evolution ... obtained by showing only those steps at which the active cell is further to the left or right than it has ever been before.

### E03 — T10 widens writes; T11 changes activity cardinality

`BOOK:882` and `916-924`:

> One can extend the set of rules one considers by allowing not only the color of the active cell itself but also the colors of its immediate neighbors to be updated at each step. And with this extension, there are a total of 4,294,967,296 possible rules.
>
> The basic idea of such generalized mobile automata is to allow more than one cell to be active at a time. And the underlying rule is then typically set up so that under certain circumstances an active cell can split in two, or can disappear entirely.
>
> A generalized mobile automaton in which any number of cells can be active at a time. ... the active cell should split in two, thereby creating an additional active cell.

### E04 — Turing machines add head state and remove neighbor reads

`BOOK:940-942`, “Turing Machines”:

> Turing machines are similar to mobile automata in that they consist of a line of cells ... together with a single active cell, known as the "head". But unlike in a mobile automaton, the head in a Turing machine can have several possible states
>
> the rule for a Turing machine can depend on the state of the head, and on the color of the cell at the position of the head, but not on the colors of any neighboring cells.

### E05 — fixed support organization

`BOOK:982`, “Substitution Systems”:

> cellular automata, mobile automata and Turing machines ... consist of a fixed array of cells. ... the colors of these cells can be updated ... [but] the underlying number and organization of cells always stays the same.

### E06 — exactly one update event and lossless standard trace

`BOOK:5818-5820`, `5836`, and `5840-5848`, Chapter 9:

> a mobile automaton or Turing machine, in which just a single cell gets updated at each step.
>
> a mobile automaton has just a single active cell which moves around from one step to the next. And because this active cell is the only one that ever gets updated, there is never any issue about synchronizing behavior of different elements at a given step.
>
> only the single active cell indicated by a dot is updated at each step
>
> successive lines give the colors of cells on successive steps, and the position of the active cell is indicated at each step by a gray dot. The subsequent pictures ... give essentially the same information, but ... emphasize ... updating events and causal relationships.

### E07 — no intrinsic halt

`BOOK:5874`, same chapter:

> The underlying way any mobile automaton works forces time to continue forever.

### E08 — substitution representation is an encoding

`BOOK:5926-5938`, “The Sequencing of Events in the Universe”:

> mobile automata—in which the presence of a single active cell forces only one event ever to occur ... at once.
>
> One can think of mobile automata as being special cases of substitution systems
>
> Substitution systems that correspond to mobile automata can be thought of as having rules and initial conditions that are specially set up so that only one updating event can ever occur on any particular step.

This is a cross-construction encoding, not evidence to use a substitution executor for native T09.

### E09 — CA packing is explicitly an emulation

`BOOK:7924-7936`, Chapter 11:

> The main difference between a mobile automaton and a cellular automaton is that in a mobile automaton there is a special active cell that moves around from one step to the next
>
> In the mobile automaton ... each cell has two possible colors. In the cellular automaton ... the cells have four possible colors, with two darker colors corresponding to the active cell
>
> to emulate a mobile automaton with a cellular automaton ... divide the possible colors ... into two sets: lighter ones that correspond to ordinary cells ... and darker ones that correspond to active cells.

This passage supplies the exact lossless tagged representation: two plain and two active label variants. It is valid when the unique-active invariant and compact mobile table remain explicit; replacing the native program by an arbitrary four-color CA table or opaque color code remains invalid.

### E10 — exact state, table, read order, source write, control move, and iteration

`BOOK:11957-11977`, Notes for page 71:

> The state of a mobile automaton at a particular step can conveniently be represented by a pair {list, n}, where list gives the values of the cells, and n specifies the position of the active cell (the value of the active cell is thus `list[[n]]`).

```text
{{1,1,1}->{0,1}, {1,1,0}->{0,1},
 {1,0,1}->{1,-1}, {1,0,0}->{0,-1},
 {0,1,1}->{0,-1}, {0,1,0}->{0,1},
 {0,0,1}->{1,1}, {0,0,0}->{1,-1}}
```

> the left-hand side in each case gives the value of the active cell and its left and right neighbors, while the righthand side consists of a pair containing the new value of the active cell and the displacement of its position. (In analogy with cellular automata, this rule can be labelled {35, 57} where the first number refers to colors, and the second displacements.)

```text
MAStep[rule_, {list_List, n_Integer}] /; 1 < n < Length[list] :=
  Apply[{ReplacePart[list, #1, n], n+#2}&,
        Replace[Take[list, {n-1, n+1}], rule]]

MAEvolveList[rule_, init_List, t_Integer] :=
  NestList[MAStep[rule, #] &, init, t]
```

The executable `Take` yields `[list[n-1],list[n],list[n+1]] = [left,self,right]`; `ReplacePart` writes old position `n`; only then does the returned state carry `n+displacement`. The guard defines the sample function's valid input set, not a boundary or halt rule.

### E11 — T10 changes the result type to a three-cell block

`BOOK:11982-11993`, adjacent Notes:

> For the mobile automaton on page 73, the rule can be given

```text
{left,self,right} -> {{new_left,new_self,new_right}, displacement}
```

> and MAStep must be rewritten

The displayed implementation replaces the three-cell block around `n`; this corroborates that base T09 writes only `n` and T10 has a distinct effect scope.

### E12 — initial values and active control are independent

`BOOK:14275`, Notes, “Random initial conditions in other systems”:

> In systems like mobile automata and Turing machines the colors of initial cells can be random, but the active cell must start at a definite location, and depending on the behavior only a limited region of initial cells near this location may ever be sampled.

### E13 — causal network is derived from the active-position trace

`BOOK:16388-16398`, Notes:

> Given a list of successive positions of the active cell, as from Map[Last, MAEvolveList[rule, init, t]] ... the network can be generated
>
> causal networks derived from them

The network consumes the full evolution; it is not state required by `MAStep`.

### E14 — topology variants and compiler relations stay distinct

`BOOK:13679`, `16648-16654`, `18352-18361`, and `18457-18463`:

> 2D mobile automata. Mobile automata can be generalized just like Turing machines. ... with only four neighbors involved there are already  $(4k)^k$ possible rules
>
> Network mobile automata. The analog ... for networks [has] a single active node, then ... rules which replace clusters of nodes around this active node, and move its position.
>
> Given a mobile automaton ... a cellular automaton which emulates it can be constructed
>
> it yields a cellular automaton with four possible colors for each cell.
>
> Given the rules for an elementary cellular automaton ... [one] will construct a mobile automaton which emulates it

These passages prove relations and variants but not native reuse by compilation.

The displayed 2D-mobile formula in the local Markdown has lost an exponent. The same source sentence says the binary count is nearly `10^29`; a rule reads the active cell plus four neighbors (`k^5` contexts) and chooses a new color plus one of four moves (`4k` outputs), so the repaired count is `(4k)^(k^5)`, giving `8^32 ≈ 7.92×10^28` for `k=2`. The corrupt `(4k)^k=64` fragment is retained above only as verbatim corpus provenance.

## Construction Model

### Native transition

```text
Cell = Plain(bit) | Active(bit)
configuration : integer-line DOMAIN -> Cell
invariant: exactly one Active(...)

source = unique Active locus selected by FRONTIER
reads  = projected bits at (source-1, source, source+1)
(new_value, displacement) = table[reads]

writes = {
  AssignSource(new_value),
  MoveActive(displacement)
}
next = UPDATE.apply(configuration, source, writes)
```

| Dimension | Reconstructed T09 semantics |
|---|---|
| Configuration | Fixed ordered 1D DOMAIN/support + composite finite labels `Plain(bit) \| Active(bit)` with exactly one active tag. Factored `(values,position)` is a checked isomorphic view, not required storage. |
| Support | Same fixed line class as T01; it may be unbounded. The number and organization of cells do not change. A finite work array is an explicit realization. |
| Active/source frontier | `UniqueTag("active")`, exactly one source determined from the labeled configuration. It is where the rule fires, not the union of write targets. |
| Read | Ordered physical `[left,self,right]` values around the source, from the pre-transition state. |
| Rule | Arbitrary total 8-entry table. Each entry returns `(new binary value, displacement in {-1,+1})`. |
| Result | Native typed `AssignSource(new_bit)` plus `MoveActive(displacement)` writes; an explicit two-label assignment batch is an optional lossless lowering. |
| Update | Resolve the selected port from the active source, preserve the old destination bit from the same snapshot, atomically replace the source label and move the active tag, preserve every other label, and validate exactly one active tag. |
| Successor/halting | One deterministic successor; exactly one firing per step; no stay, branch, split, disappearance, rejection, or intrinsic halt. |
| Seed | Initial bit field and active-tag locus are independently supplied parts of one valid labeled configuration. Values may be explicit, uniform, periodic, or random; exactly one locus is tagged. |
| Boundary/realization | No base wrap/reflect/exterior rule is stated. Notes guard a finite implementation away from edges. Exact canonical execution uses an integer line or an explicit realization whose relocation semantics are declared. |
| Observables | Full value plus active-position trace; record-extreme subsequence; update-event/causal network. Compression/network never feeds execution. |

### Exact table codec and conformance oracle

There are `2^3=8` contexts and `2*2=4` result choices, hence `4^8=65,536 = 256*256` rules. Representing colors and directions as separate eight-bit tables is evidence-backed and inspectable:

| `[L,C,R]` | New | Move |
|---|---:|---:|
| `111` | 0 | +1 |
| `110` | 0 | +1 |
| `101` | 1 | -1 |
| `100` | 0 | -1 |
| `011` | 0 | -1 |
| `010` | 0 | +1 |
| `001` | 1 | +1 |
| `000` | 1 | -1 |

For `{color_code,move_code}={35,57}`:

```text
i = 4*L + 2*C + R
new_value = (35 >> i) & 1
direction_bit = (57 >> i) & 1
displacement = 1 - 2*direction_bit
```

The independently decoded all-zero-line trace `(ones, active)` is:

```text
t0  ({}, 0)
t1  ({0}, -1)
t2  ({-1,0}, 0)
t3  ({-1}, 1)
t4  ({-1,1}, 0)
t5  ({-1,0,1}, -1)
t6  ({0,1}, -2)
t7  ({-2,0,1}, -3)
t8  ({-3,-2,0,1}, -2)
t9  ({-3,0,1}, -1)
```

Asymmetric ordering guards: physical `100` must move left (a self-first decoder misreads `010` and moves right); physical `011` must write 0 (self-first misreads `101` and writes 1).

### Variant disposition

| Candidate | Relation to base T09 |
|---|---|
| Record-extrema compressed evolution | Downstream frame selector |
| Causal/update-event network | Derived observable from full trace |
| T10 extended mobile automaton | Same single control, wider three-cell write result; separate stage |
| T11 generalized mobile automaton | Multiple control markers plus split/disappear; separate stage |
| T12 Turing machine | Active position plus internal head state; self-only tape read; separate stage |
| 2D/network mobile automata | Different topology/read/move/replacement primitives |
| Reversible three-cell examples | T10-like block write, not base T09 |
| CA/substitution encodings | Exact emulations, explicitly rejected as native representation |

## Corrected Architecture and Goal 2 Handoff

### Commuting representation

For factored state `(v,h)`, define `E(v,h)[x] = Active(v[x])` when `x=h` and `Plain(v[x])` otherwise. On exactly-one-active configurations, `E` is bijective. If the compact rule gives `mu(v[h-1],v[h],v[h+1])=(b,d)`, the typed assignment/movement writes above satisfy

```text
E(step_native(v,h)) = step_tagged(E(v,h)).
```

This proves category-3 lossless reuse. The eight-row/65,536-rule mobile program remains authoritative; arbitrary four-color CA tables are not admitted. A full-slice target-local lowering generally needs radius two, while the native unique-frontier/two-write form keeps the radius-one semantic read.

### Corrected axis fit

| Axis | Fit and Goal 2 delta |
|---|---|
| DOMAIN/configuration | Reuse fixed ordered 1D support; add composite finite labels and an exactly-one-tag invariant |
| FRONTIER | Reuse the broad rule-firing role; add `UniqueTag(active)` over configuration labels |
| NEIGHBORHOOD | Reuse ordered physical `[-1,0,+1]` access and T01 codec |
| RULE | Add the closed eight-row result schema yielding `AssignSource(bit)` plus `MoveActive(direction)`; keep any concrete two-label lowering explicit |
| UPDATE | Reuse old-snapshot atomic application; resolve movement, preserve the destination bit, validate source/destination distinctions, and require exactly one successor tag |
| Runner | Use the shared branch-free protocol; no mobile dispatch |
| Trace | Store/encode the complete tagged configuration; optional factored active-position projection must round-trip |

### Revised G2-T09

- `alphabets.py`: finite tagged/product values and codecs; `Plain(bit) | Active(bit)` preset.
- `frontiers.py`/`loci.py`: state-dependent `UniqueTag` firing selector over native/infinite or explicit finite realization support.
- `neighborhoods.py`: existing ordered radius-one read projected from composite labels.
- `rules.py`: inspectable eight-row or `{color_code,move_code}` mobile table; typed source-assignment and movement writes, never a callback.
- UPDATE axis: atomic old-snapshot assignment/movement application with destination preservation and collision/coverage/invariant validation; no `RelocateControl` class.
- `specs.py`/runner: structural axis decoding and branch-free execution; seed supplies one tagged configuration.
- Tests retain all existing truth-table, asymmetric, trajectory, unbounded-movement, state-distinction, trace, observer, and 65,536-count oracles, and add pack/unpack plus commuting-square checks.
- Static completion check: no family branch, hidden active position, opaque color code, arbitrary composite-CA table, boundary invention, or second control source.

The historical analysis below is retained to show how the rejected separate-control conclusion arose. Wherever it conflicts with this section, this corrected handoff governs.

## Historical Current API Fit (Superseded by Architecture Audit)

| Construction element | Fit | Evidence and consequence |
|---|---|---|
| Binary values | DIRECT | Existing explicit values fit (`simple_programs.md:200-230`) |
| Fixed 1D topology | DIRECT conceptually / PRINCIPLED EXTENSION for native support | Finite `SHAPE` (`:138-198`) is a realization, not moving-head capacity |
| Visible `SingleActive(position)` | PRINCIPLED EXTENSION | Current field-only state lacks Markov control; Principles 5 requires it in state |
| Source frontier | SEMANTIC MISMATCH | Current frontier is specified as writable next-state coordinates (`:1412-1510`); T09 selects the firing source from control |
| Ordered local read | DIRECT/PARAMETERIZATION | Relative reads fit (`:360-394`); pin physical `[-1,0,+1]` and T01's MSB-first codec |
| Exhaustive input table | DIRECT conceptually | Existing exhaustive rule idea fits (`:1767-1829`); output schema must become finite typed writes |
| `Assign + RelocateControl` result | PRINCIPLED EXTENSION | Current rule returns one bare next value (`:1767-1791`) |
| Atomic update | PRINCIPLED EXTENSION | One firing coordinates a source write and control move; unchanged values copy |
| Initial values/control | PRINCIPLED EXTENSION | Value seed machinery can contribute, but initial active position must be explicit and validated |
| Structured trace | PRINCIPLED EXTENSION | `[t,x,0,0]` values alone collapse states with different active positions; add a typed control stream/record before lowering |
| Compression/causal network | NOT APPLICABLE to execution | Downstream trace transformations only |

T09 extends rather than splits the T01 protocol after `FRONTIER` is rederived as a source selector and `RULE`/`UPDATE` become explicit typed-effect boundaries. T01 is not reopened: every T01 source is also its assignment target, so its behavior and handoff remain correct.

## Historical Current Runtime Fit (Superseded by Architecture Audit)

| Component | Fit | Exact finding |
|---|---|---|
| `alphabets.boolean()` | DIRECT primitive | Correct values (`src/ca/alphabets.py:129-143`), but `Dynamics` does not carry an alphabet/structured state (`specs.py:23-55`) |
| `loci.CoordinateSpace` | PARAMETERIZATION only | Finite line/gathers can realize a window (`loci.py:31-94,531-614`); no unbounded moving support |
| `neighborhoods.eca()` | DIRECT geometry/order | Physical lex `[left,self,right]` (`neighborhoods.py:551-569`); it must use the corrected MSB-first codec identified by T01 |
| Frontier catalog | SEMANTIC MISMATCH | Only `time_slice` is executable (`frontiers.py:54-80`, `rollout.py:825-831`); spatial rollout updates the dense field rather than executing selected source coordinates (`rollout.py:576-660`) |
| Rule/result | SEMANTIC MISMATCH | `Rule`/callable types expose `Any` and lookup assumes scalar alphabet output (`rules.py:1-30,64-78,262-295`); no typed finite compound result schema |
| Executor/update | SEMANTIC MISMATCH | Family switches drive scalar/batch/rule application (`rollout.py:145-212,292-331`); no atomic effect application |
| Seed/state | SEMANTIC MISMATCH | `Seed` renders only value arrays (`seeds.py:39-55,879-939`); active position would be hidden or lost |
| Boundary | SEMANTIC MISMATCH for control | Gather policies affect reads (`loci.py:531-614`, `specs.py:227-252`) but define nothing about control relocation past a finite extent |
| Raw trace | SEMANTIC MISMATCH | `RawEpisode.states` is one NumPy value array and coords enumerate those values (`specs.py:58-68`, `rollout.py:75-84,215-235`); identical fields with different control collapse |
| Tests | NO COVERAGE | `tests/test_rollout.py:529-544` locks rejection of non-full frontiers; no control, compound-effect, source-frontier, code-pair, or control-trace test exists |

The current full-state formula callback is not a valid fallback: T09 has a finite local table and finite typed result schema. A callable would merely smuggle the construction.

## Historical Principles Audit (Superseded by Architecture Audit)

| Principle | T09 result |
|---|---|
| 0–2 | T09 composes with T01 only after rederiving frontier as source selection and adding visible effects/control. This is a principled extension, not a mobile executor. |
| 3 | Frontier chooses the active source, neighborhood reads, rule proposes value/control effects, update atomically applies them. Effect targets do not leak into frontier responsibility. |
| 4 | `Assign` and `RelocateControl` are distinct typed effects; movement is not disguised as a value. |
| 5 | Active position is visible Markov control. Packing it into color or executor locals violates state completeness. |
| 6–8 | The fixed line topology, unbounded/finite realization, value address, control trace, and visualization dot remain separately inspectable. |
| 9 | Initial field and active start are independent; table arity/order and write-result schema are coupled and strictly validated. |
| 10 | `mobile(35,57)` may be a strict preset only if it returns the ordinary source/read/effect/update spec. |
| 11–12 | Single-event schedule is defining. Compression, causal graph, emulation, batching, and plotting are downstream/incidental. |
| 13–14 | Physical `100`/`011`, a moving head beyond a display window, and identical fields with different control are adversarial cases that expose false composition. |
| 15 | Tests must inspect both state components, both effects, tuple order, exact code pair, and atomicity. Value-only trajectories are insufficient. |
| 16 | A structured-state/effect boundary is architectural. Four-color packing, family dispatch, hidden head metadata, and boundary fallback are shims. |

## Historical Detailed Implementation Plan (Superseded by Architecture Audit)

1. Generalize the T01 candidate protocol's frontier from write targets to firing sources without changing T01 behavior.
2. Add visible structured state `support/topology + values + control` and a strict exactly-one active-position invariant.
3. Reuse physical `[left,self,right]` reads and the MSB-first context codec established by T01.
4. Give exhaustive tables a finite typed result schema containing color and displacement, lowered to transparent composite-label writes.
5. Apply both effects atomically, preserve untouched values, and validate exactly one active control marker in the successor.
6. Execute over the native integer line or an explicit realization with declared control-edge semantics; never infer halt/wrap/reflect from the Notes guard.
7. Emit a structured trace that preserves values and control, then derive canonical addresses, compressed frames, causal networks, batching, and visualization downstream.
8. Expose a strict preset over the shared executor and add independent truth-table/trajectory/state-distinction tests.

## Historical Goal 2 Implementation Stage (Superseded by Revised G2-T09)

### G2-T09 — Visible control, source frontiers, typed compound effects, and Mobile conformance

**Objective:** run T01 and T09 through one non-vacuous transition protocol, with T09 expressed as one active source returning atomic value/control effects. Never add a mobile rollout branch.

**Dependencies:** T01's fixed regular support, explicit realization/trace split, ordered exhaustive codec, typed `Assign`, and generic executor. T09 extends these with structured control, `ControlLocus`, `RelocateControl`, typed compound table results, and structured trace records.

**Concrete implementation areas:**

- Add a synthesis-selected state/support module with `support`, `values`, and visible typed `control`; implement an exactly-one active-position value and invariant.
- `src/ca/frontiers.py`: define semantic source selectors `AllSites` and `ControlLocus(key)`. Migrate wording/API away from next-state writable targets.
- `src/ca/rules.py`: support explicit ordered exhaustive input states and a finite typed result codec. A mobile table is two validated byte codes or the equivalent inspectable 8-entry `(value,displacement)` table, never a callable.
- Add a typed effects/update module with `Assign(at,value)`, `RelocateControl(key,from,to)`, and atomic total application. Reject missing/duplicate control relocation and invalid sources/targets.
- Replace family dispatch in the synthesis-selected generic executor: select sources, read old state, produce effects, apply atomically. T01 uses `AllSites+Assign`; T09 uses `ControlLocus+Assign+RelocateControl` through the same path.
- `src/ca/specs.py` and preset index: make `mobile(color_code,move_code)` return the ordinary shared spec with Boolean field, fixed 1D support, one active control, `[left,self,right]` read, one table, and atomic update. Seed/value field and active start are episode inputs.
- Raw trace/encoding: retain a structured snapshot containing values and control. Lower value observations to `[t,x,0,0]` plus an explicit typed control channel/record so states differing only in active position remain distinct.
- Add `tests/test_t09_mobile.py` and shared state/effect/frontier/update tests. Preserve current tests without weakening them.

**Migration/removal:** resolve the documented/runtime frontier source-target inconsistency; do not add `mobile` to current family switches. Keep CA/substitution compilers, record compression, causal network, dataset, and visualization outside native execution. Current finite read boundaries cannot silently become control-relocation policies.

**Canonical tests:**

1. Assert all eight `{35,57}` truth-table rows and both asymmetric guards `100`/`011` using `i=4L+2C+R`.
2. Assert the exact `t0..t9` all-zero trace above with an independent sparse-dictionary/head oracle.
3. Exhaust all `256*256=65,536` code pairs and 8 contexts; reject each code outside `0..255`; assert four result choices per context and `4^8` tables.
4. Prove only the old active cell is written and control moves once after the read. The destination is read but not updated by base T09.
5. Give identical value fields two different active positions; states and encoded traces must differ, and choose a field where their successors differ.
6. Assert exactly one active position before and after every valid step; reject missing/multiple active control.
7. Run `{0,0}` or another steadily moving rule beyond any initial display window on `Z`; it must not wrap, reflect, truncate, pad, or implicitly halt.
8. Reuse one mobile spec with two value fields and active starts. No seed/control start is baked into the preset.
9. Round-trip values plus active positions through raw trace and experiment encoding without collapsing control.
10. Derive record-extreme compression and causal network from the full trace and prove neither is read by execution.
11. Execute T01 `AllSites -> Assign` and T09 `ControlLocus -> Assign + RelocateControl` through the same reference protocol; use independent oracles rather than scalar/batch self-parity alone.
12. Inspect the returned preset and code path: no mobile family branch, callback, active-color packing, or hidden state.

**Completion evidence:** all tests pass; static inspection finds no family-name dispatch for T09 and no control stored outside state; the code pair round-trips; physical input order and effect atomicity are independently proven; unbounded movement and structured trace survive; existing T01 and baseline tests pass unchanged.

## Historical No-Cheating Checks (Superseded where they prohibit transparent tagged labels)

- No four-color CA lowering or active-marker value packing.
- No active position in executor locals, closure state, metadata, rule callable, or visualization marks.
- No `if family == "mobile"`, separate mobile rollout, or unrestricted callback.
- No fixed-capacity line presented as native support; no implicit edge halt/wrap/reflect/fallback.
- No compressed frames or causal-network nodes used as Markov state.
- No source/target conflation: assignment targets the old active site; relocation targets its neighbor.
- No self-first tuple interpretation or ECA-selector permutation shim.
- No T10 three-cell write, T11 split/disappear, or T12 head-state feature admitted by the basic preset.
- No value-only trace/test and no scalar/batch self-comparison as the sole oracle.
- No test weakening or duplicated effect logic.

## Completion Requirements

- [x] All aliases, captions, Notes, Index entries, cross-references, duplicates, and false positives are resolved.
- [x] All unique construction-relevant excerpts have exact canonical provenance.
- [x] Visible control, read order, compound result, atomic update, support/boundary, seed, and observables are reconstructed.
- [x] The 65,536 tables and canonical example have independent conformance oracles.
- [x] Current API/runtime/test fit is reclassified without presuming separate control storage, while retaining source-frontier semantics.
- [x] Goal 2 handoff is revised around a lossless composite state, exactly-one invariant, and structural atomic lowering.
- [x] Global ledgers and all dependent decisions are re-integrated and independently verified.

## Architecture-Reclosed Stage Result

**COMPLETE.** T09 uses `Plain(bit) | Active(bit)` with an exactly-one invariant, a firing-source frontier, the native radius-one read, typed source-assignment plus tag-movement writes, and atomic destination-preserving UPDATE in the common runner. The commuting map, compact rule identity, and revised Goal 2 handoff above replace the historical separate-control conclusion.

## Historical Stage Results (Evidence Retained; Architecture Superseded)

**Reopened:** the evidence, native mobile rule, and source-frontier semantics remain valid, but the separate-control architecture is withdrawn pending `architecture-audit.md`. Neither visibility nor atomicity requires a `SingleControl` class; a unique tagged active cell supplies the firing locus and complete state.

T09 is complete with zero unresolved evidence candidates. It preserves T01's fixed-lattice transition protocol only after a first-principles correction: `FRONTIER` selects rule-firing sources, while typed results name mutation targets. T09 adds directly evidenced visible control, `ControlLocus`, `RelocateControl`, a finite compound rule-result schema, atomic multi-effect update, and structured control-preserving traces. The exact `{35,57}` codec uses physical `[left,self,right]`; an apparent prose-order ambiguity was resolved against executable Notes and the rule image, and independent asymmetric cases/trajectory prevent regression. T01 remains complete because its sources and assignment targets coincide. No family-specific executor, CA packing, boundary invention, or compressed-state shortcut is accepted. Next: T12 Turing Machines.
