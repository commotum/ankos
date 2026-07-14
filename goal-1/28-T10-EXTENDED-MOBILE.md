# 28-T10-EXTENDED-MOBILE

Status: **COMPLETE — EVIDENCE, ASSETS, AND ARCHITECTURE RECLOSED**

## Current Facts

- Exact catalog row: T10, CSV line 11, `Extended Mobile Automata`; taxonomy section 10 at `ref/notes/CA-Types.md:239-265` is search vocabulary only, not book evidence.
- The canonical book never uses the catalog phrase. T10 is the unnamed Chapter 3 extension at `BOOK:882`, made executable for page 73 at `BOOK:11982-11993`.
- Strict T09 already establishes a discrete `t+1D` fixed line, transparent `Plain(bit) | Active(bit)` labels, exactly one active tag, a unique firing-source frontier, physical left/self/right reads, movement by `-1` or `+1`, atomic finite label writes, and no family executor.
- T10 keeps all of those roles. Its one semantic change is that each rule row returns a complete three-bit replacement block plus displacement, so the active cell and both immediate neighbors are written together.
- This is a proper extension of the strict T09 RULE-result preset but a parameterization of the existing generic typed-write axis. D011 already admits multiple typed writes from one firing source and atomic UPDATE composition.
- There are eight binary input triples and sixteen possible row results, hence `16^8 = 2^32 = 4,294,967,296` total rules, exactly matching `BOOK:882`.
- The Notes provide one complete structural eight-row table but no T10 integer rule-number convention. Any bit-plane number is a derived, versioned representation rather than source identity.
- The source oracle closes 183 query-union lines as 161 pre-Index and 22 actual-Index records. It retains 66 matched lines plus 22 governed continuations, excludes 95 pre-Index false/control lines, reverse-covers the retained set in all 17 split documents at `83 exact + 5 mapped extraction variants`, and leaves zero unresolved candidate.
- The asset oracle closes 37 JPEGs at `4 construction / 6 direct observer / 21 typed relation or sibling / 6 adjacency control`, 74 monolith/split references, no split absence, and 37 unique hashes. Raster layout is never state, RULE, UPDATE, or identity.
- Goal 1 changes only `goal-1/`; runtime, tests, `principles.md`, and `simple_programs.md` remain Goal 2 work.

## Updated Assumptions

- The library target is Wolfram-style `SimpleProgram`, not a cellular-automaton-only abstraction. Cellular automata, mobile automata, and Turing machines are presets over one branch-free transition pipeline when their axes commute:

```text
active = FRONTIER.select(configuration)
reads  = NEIGHBORHOOD.read(configuration, active)
writes = RULE(active, reads)
next   = UPDATE.apply(configuration, active, writes)
```

- DOMAIN names the task/program dimensional space. T10 has discrete `t+1D`; its fixed integer-line support, three-cell read/write footprint, storage window, and display crop are distinct concepts.
- ALPHABET may be a transparent product or tagged union. Distinct bit and active-control roles do not require separate top-level state classes.
- A representation claim requires a lossless map with an inverse on the invariant-valid image and one-step commutation. The factored `(bits,active_position)` and tagged-cell forms satisfy that test.
- One firing locus does not imply one write target. `BOOK:914` uses “update only one cell” as shorthand for one active firing event; it cannot override the explicit three-cell definition and executable Notes table.
- A wider typed RULE result does not justify a new UPDATE law. Only a concrete transition that cannot lower to existing typed writes and atomic composition could do so; no such T10 transition exists.
- Native construction, optional CA/substitution compilation, compressed histories, active-motion plots, and causal networks remain separate. An emulation is not native rule identity merely because it is exact.

## Big Picture Objective

Exhaustively reconstruct the page-73 mobile-automaton extension and decide whether its wider write scope requires a new SimpleProgram execution algebra. Preserve its compact table, complete tagged state, atomicity, and source-relative result while finding the smallest Goal 2 extension with no T10 rollout, family flag, opaque packing, callback, fake capacity, or invented collision/boundary behavior.

## Catalog Identity

- Stable ID: T10.
- CSV line: 11.
- Exact catalog name: `Extended Mobile Automata`.
- Taxonomy section: 10.
- Source-native name: none; the book calls it an extension or “slightly more complicated rules” for mobile automata.
- Entry kind: strict binary, radius-one-read, one-active-source transition preset with a fixed three-target RULE-result footprint.
- Aliases/search vocabulary: mobile automaton/automata, page 73, active cell, immediate neighbors updated, slightly more complicated rules, three-cell/block replacement, `4,294,967,296`, `MAStep`, `MAEvolveList`, displacement, reversible mobile automata, compressed evolution, active-cell motion, causal network, CA/substitution emulation, generalized/2D/network mobile variants, Notes, captions, and Index.
- Explicitly unsupported generalizations: arbitrary alphabet size, arbitrary read/write radius, movement `0`, multiple active cells, split/disappear results, collision rules, native finite boundaries, intrinsic halt, and a canonical integer code.

## Search Log

`goal-1/28-T10-source-oracle.py` freezes the canonical monolith, Atlas, CSV, taxonomy, 17 split Markdown files, regexes, every line-set digest, split mapping, and source hashes. It fails closed under optimized Python and can run from the repository root or `/tmp`.

### Exact query protocol

| Query | Purpose | Total / pre-Index / Index hits |
|---|---|---:|
| Q00 | exact extended-mobile names | `0 / 0 / 0` |
| Q01 | mobile automaton/automata | `119 / 98 / 21` |
| Q02 | active cell(s) | `47 / 44 / 3` |
| Q03 | immediate neighbor(s) | `18 / 18 / 0` |
| Q04 | `4,294,967,296` forms | `8 / 8 / 0` |
| Q05 | `MAStep`, `MAEvolveList`, `GMAStep` | `7 / 7 / 0` |
| Q06 | page 73 | `2 / 2 / 0` |
| Q07 | extension/widening near mobile terms | `1 / 1 / 0` |
| Q08 | replacement/write-window jargon | `0 / 0 / 0` |
| Q09 | one/single cell update wording | `4 / 4 / 0` |
| Q10 | movement/displacement near active cell | `17 / 17 / 0` |
| Q11 | generalized/reversible/network/2D/universal variants | `13 / 11 / 2` |
| Q12 | historical/alias controls | `1 / 0 / 1` |
| Q13 | compression and active-position observations | `19 / 18 / 1` |
| Q14 | executable `Join`/`Take`/`ReplacePart` forms | `5 / 5 / 0` |
| Q15 | hostile multiple-cell/block update wording | `3 / 3 / 0` |
| Q16 | `65,536` T09 boundary | `7 / 7 / 0` |

The union is 183 unique lines, digest `e9d4066e4446c0ea8481ef9ba215f9fce60400019b3484064887cead0f7af421`: 161 pre-Index lines and 22 actual-Index lines. Context adjudication partitions the pre-Index union into 66 matched retained and 95 excluded. Twenty-two non-hit continuations complete tables, executable bodies, and contrasts, yielding 88 retained lines with digest `b840e59085605f26a24f07a1100fa4ccc4390be1eb37a274a8e6e68588681f1c` and a 205-line declared audit universe.

### Split, Atlas, and catalog closure

- All 17 split Markdown documents are hashed and searched. The 183 monolith query records map to `171 exact + 12 extraction variants`; the 88 retained lines reverse-map as `83 exact + 5 variants`.
- The 542-line Atlas has only generic hits at lines `7,81,83`; it supplies no T10 name, rule cardinality, or additional construction.
- CSV line 11 and taxonomy section 10 are pinned. Their `Extended Mobile Automata` label is absent from the source, so it is catalog traceability, not a source quotation.
- Both monolith and split copies corrupt the displayed page-73 `MAStep` line. The eight-row table and the visible `Join[Take[...,n-2], block, Take[...,n+2]]` bounds unambiguously establish replacement of `n-1..n+1` followed by position `n+d`; the extracted line is not claimed executable verbatim.

### Candidate disposition

- **Native T10:** `BOOK:882-912`, `11982-11993`, and the page-73/74/75 observer continuation at `12002`.
- **Shared T09/T10 facts:** the one active source, physical read, fixed line, factored state, indefinite evolution, initial-position requirement, and complete active-position trace at `BOOK:850-880`, `982`, `5874`, `11957-11977`, and `14275`.
- **Restriction:** reversible three-cell-output mobile rules at `BOOK:16066-16070` stay within T10's result/update shape.
- **Observers:** compressed evolution, active motion, and causal networks at `BOOK:878`, `890-912`, `11995`, `12002`, and `16388-16398` consume native traces; they do not feed execution.
- **Relations only:** substitution and CA emulations at `BOOK:5926-5938`, `7924-7936`, `8004-8014`, `16442-16444`, `18352-18361`, and `18457-18463` do not replace the compact native table.
- **Sibling boundaries:** T11 multiple-active splitting/disappearance (`BOOK:916-934`), T12 head-state/no-neighbor-read semantics (`940-948`), 2D mobile rules (`13679`), and network mobile replacement (`16648-16654`) remain separately typed stages or relations.
- **Excluded false positives:** the other seven occurrences of `4,294,967,296`, hostile multi-cell terms, generic “immediate neighbor,” unrelated CA counts, and all actual-Index lines add no construction beyond the followed page routes.
- Remaining unresolved source candidates: **zero**.

## Book Excerpts

### E01 — strict T09 context and the defining extension

`BOOK:850-882`, Chapter 3, “Mobile Automata”:

> Mobile automata ... have just a single "active cell" that gets updated at each step ... The rule applies only to this active cell. It looks at the color of the active cell and its immediate neighbors ... One can extend the set of rules ... by allowing not only the color of the active cell itself but also the colors of its immediate neighbors to be updated at each step. And with this extension, there are a total of 4,294,967,296 possible rules.

This pins the unchanged single firing source and radius-one read while widening the write result to all three cells.

### E02 — behavior and compressed views are observations

`BOOK:884-912`, captions for pages 73-75:

> A mobile automaton with slightly more complicated rules that yields a nested pattern. Each column on the left shows 200 steps ... The compressed form ... is based on a total of 8000 steps.

> A mobile automaton that yields a pattern with seemingly random features. The motion of the active cell is still quite regular ... the compressed form below corresponds to 50,000 steps.

> A mobile automaton in which the position of the active cell moves in a seemingly random way. Each column above shows 400 steps; the compressed form corresponds to 50,000 steps.

These establish example horizons and observers, not additional state or update inputs.

### E03 — “one cell” means one firing event, not one target

`BOOK:914`, after the T10 examples:

> Despite the fact that mobile automata update only one cell at a time, it is thus still possible for them to produce behavior of great complexity.

The explicit extension and Notes implementation control write cardinality. This sentence preserves the single active source/event distinction documented by D009.

### E04 — fixed support and sibling boundaries

`BOOK:916-982`:

> The basic idea of such generalized mobile automata is to allow more than one cell to be active at a time ... an active cell can split in two, or can disappear entirely.

> Turing machines ... have one active cell or "head" ... the rule ... can depend on the state of the head, and on the color of the cell at the position of the head, but not on the colors of any neighboring cells.

> cellular automata, mobile automata and Turing machines ... consist of a fixed array of cells ... the underlying number and organization of cells always stays the same.

T11 changes activity cardinality/results, T12 changes the read/control product, and T10 retains fixed support.

### E05 — complete native table and block replacement

`BOOK:11982-11993`, Notes for page 73:

> For the mobile automaton on page 73, the rule can be given

```text
111 -> {000,-1}
110 -> {101,-1}
101 -> {111,+1}
100 -> {100,+1}
011 -> {000,+1}
010 -> {011,-1}
001 -> {101,+1}
000 -> {111,+1}
```

> and MAStep must be rewritten

The damaged displayed body visibly joins the prefix through `n-2`, the returned three-value block, and the suffix from `n+2`, then returns `n + displacement`. It establishes one old `[left,self,right]` snapshot read, complete replacement of that block, and relocation within it.

### E06 — finite Notes guard is defined input, not native boundary

`BOOK:11957-11977`, ordinary mobile implementation:

> The state of a mobile automaton at a particular step can conveniently be represented by a pair `{list,n}`, where `list` gives the values of the cells, and `n` specifies the position of the active cell ...

```text
MAStep[rule_, {list_List, n_Integer}] /; 1 < n < Length[list] := ...
MAEvolveList[rule_, init_List, t_Integer] := NestList[MAStep[rule,#]&,init,t]
```

The guard states where this finite sample function is defined. It gives no wrap, reflection, truncation, halt, or exterior value.

### E07 — initial values and the unique active locus are independent roles

`BOOK:14275`, Notes:

> In systems like mobile automata and Turing machines the colors of initial cells can be random, but the active cell must start at a definite location ...

T08 constructs the valid event-zero configuration; T10 does not add seed semantics.

### E08 — reversible rules are a restriction over the same shape

`BOOK:16066-16070`, Notes, “Other reversible systems”:

> Reversible mobile automata can for instance be constructed using ... `If[First[#] == 0, {#,-1}, {Reverse[#],1}]` ... where `perm` is an element of `Permutations[Range[8]]`.

The result remains a three-bit block plus direction. Reversibility constrains valid tables; it neither changes the runner nor adds a commit policy.

### E09 — motion and causal networks are trace-derived

`BOOK:12002` and `16388-16398`:

> The pictures below show the positions of the active cell for 20,000 steps ... (a), (b) and (c) correspond respectively to the rules on pages 73, 74 and 75.

> Given a list of successive positions of the active cell, as from `Map[Last, MAEvolveList[rule,init,t]]` ... the network can be generated ... causal networks derived from them.

The full state trajectory precedes the observer. Active position, motion plot, compressed trace, and causal graph are not interchangeable identities.

### E10 — exact emulations remain relations

`BOOK:7924-7936`, `16442-16444`, and `18352-18361`:

> a cellular automaton can be made to emulate a mobile automaton ... four possible colors ... two darker colors corresponding to the active cell ... an exact emulation of every step

> Given a mobile automaton like the one from page 73 ... [a] causal-invariant substitution system ... emulates it

These support transparent tagged labels and exact compiler relations. They do not make an arbitrary four-color CA table or a substitution rule the native T10 program.

### E11 — native execution has no intrinsic halt

`BOOK:5874`, causal-network discussion:

> The underlying way any mobile automaton works forces time to continue forever.

Strict total T10 therefore has one successor per event. Horizon, realization failure, and external stop remain separate outcomes.

## Asset Ledger

`goal-1/28-T10-asset-oracle.py` derives a fixed point from every retained source line: a mechanical distance-four set of 35 images plus the two explicitly governed continuation images at `BOOK:5882,5886`. It pins physical path, byte count, dimensions, SHA-256, monolith line, split file/line, source/asset hashes, and the complete ledger digest `9c031dc0878d3e8fcacea4669fe175fd290a8f86a3cee711607f25a80a79c668`.

| Class | BOOK image lines | Disposition |
|---|---|---|
| `C` construction | `888,896,910,16070` | three strict T10 rule plates plus the reversible three-cell-output rule plate |
| `O` direct observer | `886,892,900,902,906,908` | strict evolution, compressed, and motion views; evidence only |
| `R` typed relation/sibling | `858,860,866,876,922,926,932,944,946,5834,5878,5882,5886,5932,5934,7928,7932,7934,8006,12004,16650` | T09/T11/T12 contrasts, causal/substitution/CA emulations, reverse emulation, active-motion relation, or network variant |
| `X` adjacency control | `8018,11998,12000,12006,14273,16658` | nearby Turing, T09 distribution, T11 heading, random-initial-condition, or network-adjacent material with no added T10 semantics |

Counts are `C/O/R/X = 4/6/21/6`, with 37 unique physical files, `37 + 37 = 74` monolith/split references, no missing split reference, and 37 unique hashes. Direct construction/observer evidence totals ten assets. The rule diagrams visually corroborate ordered input triples, three output colors, and one destination dot; their layout, gray palette, crop, and raster dimensions are not a program schema.

## Construction Model

### Native state and transition

```text
Bit  = {0,1}
Cell = Plain(Bit) | Active(Bit)

configuration : Z -> Cell
invariant: exactly one cell is Active(...)

h      = UniqueTag("active").select(configuration)
reads  = bit(configuration[h-1]), bit(configuration[h]), bit(configuration[h+1])
(block,d) = table[reads]
block  = (b[-1], b[0], b[+1])
d      in {-1,+1}

writes = {
  h-1: Active(b[-1]) if d=-1 else Plain(b[-1]),
  h  : Plain(b[0]),
  h+1: Active(b[+1]) if d=+1 else Plain(b[+1]),
}

next = AtomicFiniteWrites.apply(configuration, h, writes)
```

All reads and writes are source-relative but refer to physical left/center/right order. The three targets are distinct and there is one source, so T10 introduces no collision-resolution or ordering policy. Every write is a complete next-cell label derived from the same old snapshot; outside the block the configuration is unchanged.

The destination's underlying bit is the **new replacement bit at offset `d`**. It is not the old destination bit retained by strict T09. The Notes row `000 -> {111,+1}` is the decisive counterexample: its lowered labels are `Plain(1), Plain(1), Active(1)`, whereas composing T09's center write and tag movement would leave the destination bit `0`.

### Structural table and rule cardinality

The native program is a closed total table

```text
Bit^3 -> Bit^3 x {-1,+1}
```

with eight unique physical input rows. Each row has `2^3 * 2 = 16` possible results, so the family size is

```text
16^(2^3) = 16^8 = 2^32 = 4,294,967,296.
```

The table above is the exact page-73 fixture. It has no source-defined integer number. Under an optional explicitly inferred convention `i=4L+2C+R` and direction bit `1=left`, its four bit planes are `(left,center,right,move) = (115,37,103,196)`. That tuple is a derived codec fixture only; it must be versioned with ordering and round-trip semantics and never replace structural identity.

### Lossless factored/tagged equivalence

Let `F=(bits,h)` be the Notes representation and `e(F)` tag position `h` while retaining `bits[h]`. On exactly-one-active states, `e` has the inverse “strip tags and return the unique tagged coordinate.” The stage oracle proves for every input triple, every one of the sixteen possible row results, and sixteen outside-background assignments:

```text
e(step_factored(F)) = step_tagged(e(F)).
```

This is 2,048 exhaustive commuting cases, plus outside-block preservation and exactly-one-tag checks. It is a transparent representation of the complete state, not opaque head packing or a hidden interpreter.

### Exact derived page-73 trajectory

Starting from the all-zero field with active position `0`, the Notes table yields:

```text
t0  h= 0  ones={}
t1  h= 1  ones={-1,0,1}
t2  h= 0  ones={-1,0,2}
t3  h=-1  ones={-1,1,2}
t4  h=-2  ones={-1,0,1,2}
t5  h=-1  ones={-3,-1,0,1,2}
t6  h= 0  ones={-3,1,2}
t7  h= 1  ones={-3,-1,1,2}
t8  h= 2  ones={-3,-1}
t9  h= 3  ones={-3,-1,1,2,3}
t10 h= 2  ones={-3,-1,1,2,4}
t11 h= 1  ones={-3,-1,1,3,4}
t12 h= 0  ones={-3,-1,1,2,3,4}
```

This is an independently replayed semantic checkpoint, not a raster-decoded rule or a published T10 number.

### DOMAIN, support, boundary, and finite realization

- DOMAIN: discrete `t+1D`.
- Native support/topology: fixed ordered integer line; support neither grows nor shrinks.
- Read footprint: offsets `{-1,0,+1}` around the one source.
- Write footprint: the same three offsets, each exactly once.
- Successor structure: exactly one deterministic successor for every valid state/table row; no intrinsic halt.
- Seed: any T08-valid binary field presentation plus one definite active tag.
- Boundary: none in the native construction. A finite work realization must prevalidate every read/write coordinate or carry an explicit, separately identified boundary/causal-lowering contract.
- Trace: complete tagged configurations and event witnesses. Position, width, compression, motion, behavior class, and causal network are derived observers.

For `h` requested transitions from a default field, a finite exact realization may be justified through a dependency/write cone and proved through the complete horizon. A finite array edge must not silently wrap, reflect, truncate, freeze, or become a halt.

### Compiler and variant boundaries

- **Reversible mobile:** a table restriction/property over the same result/update axes; no new runner.
- **Full-slice CA compiler:** a valid transparent relation may encode `Plain/Active` as four colors and restrict to exactly-one-active configurations. For general T10 it requires target-local radius two, not automatically radius one: the left target of a source may depend on the source's right neighbor. The oracle gives two states that agree on the target's complete radius-one tagged neighborhood but yield different target bits under rows `110` and `111`.
- **Arbitrary composite CA table:** not T10 identity. It admits invalid multi-head states and vastly more tables than the structured `Bit^3 -> Bit^3 x Move` family.
- **Substitution compiler/causal network:** exact relations or observers only.
- **T11:** owns multiple sources, split/disappear results, overlaps, and any evidenced collision semantics.
- **T12:** owns payload head states and symbol-only source reads.
- **2D/network mobile:** distinct DOMAIN/topology and read/replacement schemas; not flags on strict T10.

