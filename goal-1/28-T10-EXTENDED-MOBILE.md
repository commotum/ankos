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
- The asset oracle closes 38 JPEGs at `4 construction / 6 direct observer / 22 typed relation or sibling / 6 adjacency control`, 76 monolith/split references, no split absence, and 38 unique hashes. Raster layout is never state, RULE, UPDATE, or identity.
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
| Q17 | pseudocode `new_left/new_self/new_right` vocabulary | `0 / 0 / 0` |

The union is 183 unique lines, digest `e9d4066e4446c0ea8481ef9ba215f9fce60400019b3484064887cead0f7af421`: 161 pre-Index lines and 22 actual-Index lines. Context adjudication partitions the pre-Index union into 66 matched retained and 95 excluded. Twenty-two non-hit continuations complete tables, executable bodies, and contrasts, yielding 88 retained lines with digest `b840e59085605f26a24f07a1100fa4ccc4390be1eb37a274a8e6e68588681f1c` and a 205-line declared audit universe.

### Split, Atlas, and catalog closure

- All 17 physical split Markdown documents are hashed and searched without trusting extraction-shifted folder names or line structure. The 183 monolith query records map to `171 exact + 12 explicit fragment/join variants`; the 88 retained lines reverse-map as `83 exact + 5 variants`. There is no split-only T10 evidence.
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

Normalized from the preserved escaped Notes table:

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

The CA passages are for the page-71/basic scalar-output mobile rule and support transparent tagged state plus the existence of exact one-step compiler relations in that scope. The substitution passage directly covers the page-73 wider-write rule. None proves that a basic radius-one CA compiler works unchanged for T10, and none makes an arbitrary four-color CA table or a substitution rule the native T10 program.

### E11 — native execution has no intrinsic halt

`BOOK:5874`, causal-network discussion:

> The underlying way any mobile automaton works forces time to continue forever.

Strict total T10 therefore has one successor per event. Horizon, realization failure, and external stop remain separate outcomes.

## Asset Ledger

`goal-1/28-T10-asset-oracle.py` derives a fixed point from every retained source line: a mechanical distance-four set of 35 images plus three explicitly governed continuation images at `BOOK:5882,5886,5900`. The last follows the same-rule facing-page chain at `BOOK:5896`; `BOOK:5912` starts a different binary-counter rule and closes it. The oracle pins physical path, byte count, dimensions, SHA-256, monolith line, split file/line, source/asset hashes, and the complete ledger digest `e569e03f4bd1830789a40ee29ce5928165446c2d741125828608a61123e9ae29` over universe digest `c65ce970d643cda4cc441d0ec5e8567beee3cfd5a0fe42a3146c6311e6bb95ed`. The direct/adjacent strict 14-file subledger is independently frozen at universe digest `8914fda71f91933f3de2785ed01470291443a3fe75ee709e0d0621f306353354` and ledger digest `25bda40f87de92226bbe1ed6b6461987429814aec3e7574efc637fdd3590304a`; the broader 38-file universe prevents silent relation/control omissions without promoting them.

| Class | BOOK image lines | Disposition |
|---|---|---|
| `C` construction | `888,896,910,16070` | three strict T10 rule plates plus the reversible three-cell-output rule plate |
| `O` direct observer | `886,892,900,902,906,908` | strict evolution, compressed, and motion views; evidence only |
| `R` typed relation/sibling | `858,860,866,876,922,926,932,944,946,5834,5878,5882,5886,5900,5932,5934,7928,7932,7934,8006,12004,16650` | T09/T11/T12 contrasts, causal/substitution/CA emulations, reverse emulation, active-motion relation, or network variant |
| `X` adjacency control | `8018,11998,12000,12006,14273,16658` | nearby Turing, T09 distribution, T11 heading, random-initial-condition, or network-adjacent material with no added T10 semantics |

Counts are `C/O/R/X = 4/6/22/6`, with 38 unique physical files, `38 + 38 = 76` monolith/split references, no missing split reference, and 38 unique hashes. Direct construction/observer evidence totals ten assets. The rule diagrams visually corroborate ordered input triples, three output colors, and one destination dot; their layout, gray palette, crop, and raster dimensions are not a program schema.

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
- **2D/network mobile:** 2D mobile changes the dimensional DOMAIN and geometry; network mobile changes configuration support/topology and access/replacement schemas. Neither is a flag on strict T10.

## Current API Fit

The broad intended SimpleProgram algebra is the correct fit; the present `simple_programs.md` is a CA-shaped realization of it. T10 calls for axis generalization, not a second top-level construction.

| T10 responsibility | Current document fit | Classification | Smallest correction |
|---|---|---|---|
| discrete `t+1D` task space | `simple_programs.md:115-198` names `t+1D` and ordered coordinates | `DIRECT` for dimensional responsibility; realization caveat | keep DOMAIN dimensional character separate from native integer support and finite `SHAPE` |
| tagged binary cell | `:200-234` admits finite values but not structural product/tagged schemas and invariants | `PRINCIPLED EXTENSION` already required by T09/T12 | add finite tagged/product ALPHABET schemas and exactly-one-tag configuration validation |
| unique firing source | `:1412-1510` defines FRONTIER as writable next coordinates | `SEMANTIC MISMATCH` in current wording | restore D009: FRONTIER selects the unique active rule-firing locus |
| physical left/self/right read | `:360-420` gives current-snapshot relative offsets and ordered selectors | `PARAMETERIZATION` | reuse radius-one offsets with a typed projection from `Plain/Active` to underlying bit |
| structural exhaustive table | `:1795+` has ordered exhaustive lookup responsibility | `PARAMETERIZATION` | generalize table output schema from one alphabet scalar to a closed typed product |
| three complete writes | `:1767-1791` returns one value for each writable coordinate | `PRINCIPLED EXTENSION` of current realization; `DIRECT` reuse of D011 | RULE returns the source-native block/direction and lowers losslessly to three relative label writes |
| atomic commit | `:1510,1791,2191-2197` already requires one old snapshot and parallel writes | `DIRECT` execution responsibility | reuse generic `AtomicFiniteWrites`; do not add a T10 UPDATE policy |
| unchanged outside block | current non-frontier copy-forward at `:1785-1787,2197` | `DIRECT` | generic finite-write UPDATE preserves all non-target labels |
| one deterministic successor | current schema generates one next state | `DIRECT` | return ordinary one-successor `StepResult` with event witness |
| unbounded semantic line | finite `D`, `SHAPE`, and boundary extension are realization-oriented | `SEMANTIC MISMATCH` if treated as native | use T09/T08 total-field and explicit finite-lowering responsibilities |
| full tagged trace | scalar trajectory field at `:87-113` | `PRINCIPLED EXTENSION` already required | preserve complete structured configurations before encoding/visualization |

The conceptual pipeline is therefore unchanged:

```text
active = UniqueTag.select(X)
reads  = OrderedRelativeRead([-1,0,+1], UnderlyingBit).read(X, active)
native = OrderedTable.evaluate(reads)          # Block3(Bit) x Direction
writes = lower(native, active)                 # three complete Cell labels
next   = AtomicFiniteWrites.apply(X, active, writes)
```

The explicit lowering is an architectural boundary: it is total, typed, invertible on valid T10 row results, and exhaustively tested. It is not a compatibility shim.

## Current Runtime Fit

| Current surface | Evidence from current files | Classification | Goal 2 migration |
|---|---|---|---|
| `alphabets.py` | `Value = int | float | str` and flat `Alphabet.values` at `:40-56` | `SEMANTIC MISMATCH` for transparent tags | add generic product/tagged-union schemas, member references, structural codecs, and invariant-aware validation |
| `frontiers.py` | doc and `Frontier` at `:1-51` define update-site masks; only `time_slice` is executable | `SEMANTIC MISMATCH` | generalize to typed firing loci and add `UniqueTag`; retain `time_slice` as the all-sites preset |
| `loci.py` | coordinate universes and selectors at `:31-60,179+` are reusable only for finite tensor coordinates | `PARAMETERIZATION` plus support extension | retain ordered relative-coordinate machinery, add typed structural/source loci without callbacks |
| `neighborhoods.py` | `literal_offsets` at `:140-174` expresses the geometry | `PARAMETERIZATION` | reuse ordered offsets and add typed underlying-bit projection/support reads |
| `rules.py` | `Rule` stores family strings/`Any` callback at `:30,64-78`; lookup returns scalar at `:262-295` | `SEMANTIC MISMATCH` | closed generic `OrderedTable[Read,Result]`, structural result schemas, no unrestricted `formulaic` fallback |
| `specs.py` | `Dynamics` uses `Any`, dense shape, family decoders, and only `time_slice` at `:23-55,117-198` | `SEMANTIC MISMATCH` | decode structural axis specs through a typed registry; keep preset/catalog names outside executor control flow |
| `rollout.py` | `_rollout_states`/batch branch on family at `:145-212`; `_ensure_time_slice` rejects every other frontier at `:825-831` | `SEMANTIC MISMATCH` | replace family branches with the common runner and typed UPDATE polymorphism |
| spatial lookup | `_next_spatial_state` at `:643-660` computes a dense scalar next array directly | `SEMANTIC MISMATCH` for source-relative compound results | collect native row results/writes and commit generically; preserve dense vectorization as a realization optimization only after equivalence proof |
| seed path | current arrays and T08-audited scalar rendering | `SEMANTIC MISMATCH` for tagged invariant state | accept one complete validated tagged configuration; reuse T08 constructors/lowerings |
| `RawEpisode` | `np.ndarray` state at `specs.py:58-81` | `SEMANTIC MISMATCH` | structured complete configurations and event witnesses first; dense encodings remain explicit adapters |
| tests | `tests/test_rollout.py:529-544` proves unsupported frontiers are rejected; no mobile/tag/multiwrite tests exist | current behavior evidence only | add cross-family same-runner, commutation, invariant, atomicity, edge, and serialization tests |

No current behavior can execute T10 faithfully by selecting another family string. `formulaic(fn)` would hide the construction in a callback; a four-state dense CA would change native identity and, for direct one-step target-local lowering, require a proved radius-two compiler. Both are forbidden substitutes for the small generic axis revisions above.

## Principles Audit

- Principle 0 requires re-derivation rather than protecting CA-shaped wording. The source proves the current one-value RULE realization is too narrow, not that the SimpleProgram algebra fails.
- Principles 1-3 classify T10 by construction responsibilities: the active cell is FRONTIER, its old physical triple is NEIGHBORHOOD, the table returns a typed block/move result, and UPDATE composes three label writes.
- Principle 4 directly supports explicit typed multi-write results. T10 is the smallest concrete adversary showing that “one firing source” and “one scalar target” are different.
- Principle 5 is satisfied by either lossless complete-state form. Active control is visible in the tagged ALPHABET role; it is not executor state and need not be a separate runtime class.
- Principles 6-8 keep integer-line topology, source-relative offsets, finite addresses, sparse/default storage, and raster encodings distinct.
- Principles 9-10 justify a strict named preset that returns an ordinary generic specification. The block/direction result is intrinsically coupled to the binary radius-one table and is validated as one closed product, not decomposed into freely incompatible flags.
- Principle 11 keeps atomic synchronous commit as defining semantics. It may not be sequentialized merely because the event has one source.
- Principle 12 keeps compression, motion plots, causal networks, batches, and images downstream of the native trace.
- Principles 13-15 are covered in Goal 1 by the `000 -> 111,+1` adversary, exhaustive commuting square, lowering inverse, radius-two CA-lowering counterexample, and exact table/trajectory. The Goal 2 acceptance groups require the still-prospective invalid-tag, finite-edge, and cross-runner tests; the current 102-test suite is regression evidence, not T10 runtime conformance.
- Principle 16 treats the block/direction-to-label-write map as an explicit total mapping between layers, not a fallback. There is one runner and no T10 switch.

The smallest honest classification is:

1. Same DOMAIN/support, tagged ALPHABET, exactly-one invariant, FRONTIER, NEIGHBORHOOD, movement set, UPDATE, successor algebra, seed relation, and trace responsibilities as T09.
2. A proper parameterization/extension of strict T09's RULE result from `Bit x Move` to `Bit^3 x Move`.
3. A lossless tagged/product representation of the Notes' factored state and result.
4. **No new execution algebra.** No T10 transition supplies a counterexample to generic atomic finite writes.

## Dependent Decision Audit

T10 strengthens rather than reopens D009-D014:

| Decision | T10 result |
|---|---|
| D009 | One active firing source can name three write targets. FRONTIER cannot mean the union of writable coordinates. |
| D010 | `Plain(bit) | Active(bit)` is a transparent complete-state ALPHABET role, with exactly one tag; no `SingleControl` mandate returns. |
| D011 | The existing generic finite typed-write capability is sufficient. T10 supplies the first exact three-target fixture but no new UPDATE law. |
| D012 | Physical `[left,self,right]` order remains shared. T10 structural table identity is primary; the optional four-plane codec is explicitly derived. |
| D013 | Raw traces preserve tagged configurations and native block/move/write witnesses before compression or causal observation. |
| D014 | T10 corroborates the same lossless-tag principle used by T12; it does not change head payload semantics. |

T09 needs only the already-intended clarification that its center-only underlying-bit write is a preset restriction, not a universal RULE/UPDATE limit. T12 remains closed. T11 remains pending because T10 has one source and distinct targets and therefore provides no evidence for multi-source overlap, splitting, disappearance, or collision composition.

### D122 — Extended mobile widens a typed RULE result, not the execution algebra

- **Status:** ACTIVE after source, asset, semantic, and architecture closure.
- **Basis:** `BOOK:882` explicitly widens the written cells and gives `2^32` rules; `BOOK:11982-11993` gives `Bit^3 -> Bit^3 x {-1,+1}` and replaces `n-1..n+1` before carrying `n+d`; `BOOK:16066-16070` restricts the same result shape for reversible examples.
- **Configuration:** discrete `t+1D` fixed line with `Plain(Bit) | Active(Bit)` and exactly one active tag, losslessly equivalent to `(bit_field,active_position)`.
- **Execution:** `UniqueTag` selects one source; ordered old `[L,C,R]` bits are read; one total eight-row table returns `(new_left,new_center,new_right,d)`; a closed lowering emits three distinct complete label writes with the unique active tag at offset `d`; generic atomic finite-write UPDATE commits from one snapshot and preserves all other labels.
- **Identity:** the structural table and typed result schema are primary. There are `16^8` rules and no source-defined integer codec. Reversibility, seed, horizon, finite realization, compiler, trace, and observer identities are separate.
- **Consequence:** add no T10 state class, control payload, UPDATE law, executor, callback, family branch, or collision policy. Goal 2 consumes generic tagged alphabets, invariants, source frontiers, ordered projections, typed tables/results, finite writes, `StepResult`, and serialization already required by shared stages.

## Detailed Implementation Plan

1. **COMPLETE:** freeze and disposition direct name, mobile/active/movement, cardinality, Notes implementation, page route, variant, observer, alias, hostile wording, and actual-Index searches.
2. **COMPLETE:** reverse-map every query/retained line through all 17 split documents and the Atlas; pin source corruption and zero unresolved remainder.
3. **COMPLETE:** close the governed raster fixed point with exact physical identities, split references, hashes, semantic classes, and explicit relation/control exclusions.
4. **COMPLETE:** reconstruct the table, state, read, block/move result, lowering, atomic commit, rule count, continuation, boundary, variants, relations, and observers before API comparison.
5. **COMPLETE:** audit `simple_programs.md`, `src/ca`, tests, T09/T12, D009-D014, and the corrected SimpleProgram architecture from current files.
6. **COMPLETE:** implement dependency-free rule-space, trajectory, atomicity, factored/tagged commutation, derived-codec, and radius-two-compiler adversaries in `goal-1/28-T10-semantic-oracle.py`.
7. **COMPLETE:** specify the Goal 2 stage, hostile conformance groups, no-cheating checks, and D122; run independent review and repository gates before global integration.

## Goal 2 Implementation Stage

### G2-T10 — typed fixed-block mobile results over the shared runner

Implement after the generic configuration/tag/source-frontier/finite-write work shared with G2-T09 and before T11 collision semantics. The stage adds one strict result/table preset and conformance suite, not another runner.

| Goal 2 surface | Required work |
|---|---|
| dependencies | G2-T01 configuration/runner shell; G2-T02 ordered finite tables/codecs; G2-T08 valid initial configurations and finite lowerings; G2-T09 tagged active cells, `UniqueTag`, bit projection, movement, atomic finite writes, and complete traces |
| ALPHABET/configuration | construct `Plain(Bit) | Active(Bit)` through generic tagged-union data; validate exact one tag and fixed ordered line support; retain a checked factored view and round-trip proof without duplicate authority |
| FRONTIER | reuse `UniqueTag("active")`; return one stable source handle and reject zero/multiple tags before reads |
| NEIGHBORHOOD | reuse ordered relative offsets `[-1,0,+1]` and an explicit underlying-bit projection; validate physical order and old-snapshot scope |
| RULE schema | add/use a generic closed total `OrderedTable[Bit^3, Block3(Bit) x Direction]`; require all eight unique rows, three typed output bits, and `d in {-1,+1}` |
| lowering | implement a closed structural map from `(block,d,source)` to exactly three relative complete-cell writes; tag the new bit at offset `d`, not the old destination bit; provide inverse on valid lowered rows |
| UPDATE | reuse `AtomicFiniteWrites`; require distinct in-support targets, validate all writes/result invariants before commit, and emit no partial/intermediate state on failure |
| `StepResult`/trace | retain source handle, ordered read, native block/move row result, normalized writes, validation evidence, before/after configuration references, and ordinary one-successor `Advanced` outcome |
| strict preset | `extended_mobile_binary(table)` resolves to an ordinary `SimpleProgram` with the shared axes. The catalog name never enters runner dispatch. Seed, support realization, boundary, horizon, and observers remain separate inputs/records |
| identity/serialization | version structural table order and result schema; round-trip arbitrary-precision derived codecs only when explicitly requested; keep native program, codec, reversible claim, compiler, run, trace, and view digests separate |
| finite realization | use T08 horizon lowering or explicit boundary/topology records; prevalidate the entire read/write footprint. Edge failure is a typed realization failure, not semantic halt or truncation |
| optional compiler | if implemented, provide a separate proved mapping to a constrained composite-alphabet CA. Pin required target radius and invariant-valid image; never replace native table identity or admit arbitrary CA rules as T10 rules |
| migration | remove any need to route mobile systems through `formulaic`, scalar lookup, `time_slice`, hidden active metadata, or family branches. Preserve existing CA results through the same runner as a separate preset |

### Acceptance groups

1. **Exact table:** encode all eight Notes rows in physical input/output-offset order; reject missing, duplicate, extra, malformed, or nonbinary rows and movement `0`.
2. **Rule space:** prove eight inputs, sixteen row results, and `16^8 = 2^32`; keep the structural table primary and test any optional codec as a versioned bijection.
3. **Destination-new-bit adversary:** `000 -> 111,+1` must yield `Plain(1),Plain(1),Active(1)` at offsets `-1,0,+1`; strict T09 composition must fail this fixture.
4. **Both directions:** cover tag movement left and right while writing every underlying output bit exactly once.
5. **Atomicity:** derive all writes from one snapshot, preserve outside labels, and expose no zero-head/two-head intermediate configuration. Failed validation commits nothing.
6. **Exhaustive representation commutation:** for all `8 * 16 * 16 = 2,048` local/result/outside cases, prove tagged and factored steps equal and inverse round trips hold.
7. **Exact trajectory:** replay the all-zero `t0..t12` Notes-table checkpoint independently in factored and tagged forms.
8. **Configuration invariants:** reject zero/multiple active tags, wrong underlying type, invalid support, duplicate sources, and unsynchronized factored/tagged caches; preserve exactly one valid tag after every event.
9. **Identity:** distinguish states with equal bit planes and different active loci; distinguish tables, result schemas, codecs, seeds, horizons, realizations, and observers.
10. **Boundary/continuation:** prove native deterministic continuation separately from finite edge failure, genuine finite topology, explicit boundary approximation, and external horizon/stop.
11. **Same runner:** execute representative T01, T09, T10, and T12 programs through one runner with no catalog/family condition below preset resolution.
12. **Compiler radius:** pin the page-73 target-radius-one counterexample and require radius two or an independently proved alternative for a one-step all-sites CA lowering.
13. **Reversible restriction:** validate the source constructor as a property/subset of ordinary T10 tables; do not add a reversible executor or infer a source rule number.
14. **Trace/serialization:** round-trip complete tagged configurations and native event witnesses; active-motion/compression/causal views must be reproducible from traces but unable to feed state.
15. **Static no-cheating:** reject T10 switches, `Any`/callbacks, hidden active positions, opaque whole-machine values, arbitrary four-state CA substitution, sequential in-place mutation, fake capacity, invented collision policies, and observer-defined behavior.

Completion requires exact source/asset fixtures, public typed schemas, cross-family runner tests, exhaustive commuting-square coverage, static branch/callback scans, serialization tamper tests, finite-lowering adversaries, and no regression in existing canonical CA/mobile/Turing fixtures.

## No-Cheating Checks

- No `ExtendedMobileState`, `ExtendedMobileUpdate`, T10 executor, family flag, rollout branch, callback, or opaque packed machine.
- No conflation of the current CA-shaped public realization with the intended SimpleProgram abstraction; fix axes at their owning responsibility.
- No use of the catalog label or taxonomy summary as construction evidence.
- No bare `Bit | ActiveMarker` union that loses the bit under the active tag; no separate unsynchronized control cache.
- No strict T09 result falsely claimed sufficient: both neighbor bits and the destination's new bit must be applied.
- No sequential `ReplacePart` loop whose intermediate states are observable or whose order changes the result.
- No union of write targets called FRONTIER; the one old active source is the firing locus.
- No arbitrary radius, alphabet size, stay move, multi-active split/disappear behavior, overlap/collision policy, boundary, or halt inferred from strict T10.
- No source-corrupted Notes line copied as executable code; preserve the repair and table/bounds evidence.
- No numeric rule code invented as native identity; the optional `(115,37,103,196)` planes remain an explicitly inferred codec.
- No arbitrary four-color CA table presented as the compact T10 program; any compiler must be lossless, invariant-restricted, one-step commuting, and radius-correct.
- No finite tensor, wrap/reflect/fixed exterior, crop, padding, or edge exception presented as the native integer line.
- No compressed history, motion plot, causal graph, raster, behavior class, search frequency, or reversible claim fed into execution.
- No T11 collision semantics derived from T10's one-source/distinct-target case.
- No weakened T09/T12 tests or reopened storage-class mandate; T10 reuses their corrected visible tagged roles.

## Completion Requirements

- [x] Every declared source query, candidate, governed continuation, split/Atlas/Index route, and source limitation is frozen and dispositioned with zero unresolved remainder.
- [x] Every governed asset is physically pinned or explicitly rejected as relation/control material; direct rule/evolution/reversible evidence remains separate from raster representation.
- [x] State, DOMAIN/support, ALPHABET/control, read, table, result, lowering, atomic commit, cardinality, successor, boundary, seed, variant, relation, and observer semantics are reconstructed from source evidence.
- [x] Current API/runtime/tests and all D009-D014 dependencies are audited from actual files under the broad SimpleProgram architecture.
- [x] D122 and a dependency-aware Goal 2 handoff identify the smallest generic changes and adversarial completion evidence without a new execution algebra.
- [x] Source, asset, semantic, representation, compiler-radius, coverage, Markdown, diff, scope, hostile-review, and repository-test gates pass before completion.

## Re-Integration Audit

1. **Prior assumption invalidated?** No active corrected decision fails. T10 further invalidates only the historical CA-shaped assumption that FRONTIER is a writable set and RULE returns one scalar; D009/D011 already retired it.
2. **Existing primitive reuse?** Yes. T10 reuses T09's complete state/source/read/movement and D011's atomic finite writes, parameterizing only the source-native RULE result and fixed footprint.
3. **Exception/flag/hidden state/callback?** None. The strict preset resolves to ordinary typed axes and a total structural lowering.
4. **Complete Markov state/trace?** Yes. The tagged field contains every bit and the unique active locus; full snapshots and event witnesses reproduce the factored trace exactly.
5. **DOMAIN/support/value/control/representation separation?** Yes. Discrete `t+1D`, fixed integer support, tagged binary values, active role, sparse/dense storage, and raster/compiler encodings remain distinct.
6. **Defining versus incidental algorithm?** Atomic three-label replacement and movement are defining. Notes host syntax, finite guard, search method, compression, CA/substitution emulation, and visualization are incidental implementations/relations/observers.
7. **ANKoS encoding fidelity?** Complete structured configurations and event witnesses are canonical. Any `[t,x,y,z]`/tensor encoding must preserve tag and bit and prove its realization relation; a color-only or motion-only projection is lossy.
8. **Reopened completed stages?** None. T09/T12 remain architecture-closed; T09's center-only result is simply a narrower preset.
9. **Goal 2 dependency changes?** G2-T10 consumes G2-T08/G2-T09 generic tagged-state and finite-write work, contributes the fixed-block result fixture before T11, and adds the radius-two compiler guard. It adds no runner/update dependency.
10. **Overall API simpler/coherent?** Yes. One explicit product result and one lossless lowering replace any temptation for a control class, family executor, sequential patcher, or arbitrary CA disguise.

## Stage Results

COMPLETE after exhaustive source, split, Atlas, Index, asset, semantic, runtime, and architecture closure. The exact 18-query protocol yields a 183-line union at `161 pre-Index / 22 actual-Index`; context partition is `66 retained matches / 95 excluded / 22 Index`, plus 22 governed continuations for 88 retained lines. All 17 split documents close at `171 exact + 12 mapped query variants` and `83 exact + 5 mapped retained variants`. The catalog name, replacement/write-window jargon, and normalized `new_left/new_self/new_right` vocabulary are absent; the source-native construction is the unnamed page-73 extension. Zero source candidate remains unresolved.

T10 is `Bit^3 -> Bit^3 x {-1,+1}` over the same one-active binary line as T09. Its result lowers to three distinct complete tagged labels and reuses generic atomic finite-write UPDATE. The destination carries its new block bit; `000 -> 111,+1` proves strict T09's center-only result is insufficient. `16^8 = 2^32`; no canonical T10 number is invented. Factored and tagged states commute through all 2,048 exhaustive local/result/background cases, the exact `t0..t12` trace replays, and the optional bit planes `(115,37,103,196)` are explicitly derived. A one-step full-slice CA compiler is separately guarded by a target-radius-two counterexample.

The governed asset universe and direct subset are fully dispositioned with no silent remainder; construction plates, evolutions, compression, motion, relation/control images, and reversible rules remain semantically separated. D122 is ACTIVE. No prior stage reopens; T11 remains responsible for multiple-source creation/deletion and collisions. Source/asset oracles pass from the repository root and `/tmp`; all three T10 oracles fail closed under `-O`. The semantic oracle, independent architecture review, Markdown/diff/scope/coverage gates, and all 102 repository tests pass. Next: T11.
