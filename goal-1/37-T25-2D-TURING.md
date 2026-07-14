# 37-T25-2D-TURING

Status: **COMPLETE — SOURCE, ASSET, SEMANTIC, ARCHITECTURE, AND HOSTILE-REVIEW GATES PASS**

## Current Facts

- T25 is CSV line 26, `Two-Dimensional Turing Machines`; the catalog and `ref/notes/CA-Types.md:687-710` are search guides, not primary mechanics.
- The frozen 30-query source protocol closes 71 candidate lines (`50` pre-Index and `21` guarded actual-Index routes), retains 63 at `30 native / 29 relation / 4 control`, excludes 13, and leaves zero unresolved. All 63 retained lines reverse-join to the split corpus as `47 exact + 16 normalized variants`; none is monolith-only.
- T12 supplies the lossless cell alphabet `Plain(symbol) | Head(state,symbol)` with exactly one head. D127/D130 supply discrete `t+2D`, square-grid support, explicit coordinate frames, and semantic topology ports. T25 composes those axes; it does not turn the existing `src/ca` SimpleProgram substrate into a different library.
- The Chapter 5 construction places the head on a two-dimensional grid and gives four movements (`BOOK:2264-2270`). The displayed arrow orientation denotes head state and explicitly does not determine movement.
- The Notes use closed rows `{state,symbol} -> {next_state,next_symbol,{dx,dy}}`, read only `(state,symbol)` at the head, write the old head cell, and add the displacement to the old position (`BOOK:13660-13664`).
- RULE therefore returns typed source assignment plus `MoveHead(next_state,port)`. UPDATE—not NEIGHBORHOOD or RULE—resolves the destination through visible topology, preserves its old symbol, and applies the move atomically.
- The 12 source-governed images close at `12 hash-bound / 0 transcribed / 0 pixel-replayed`: nine main/path assets plus the indivisible three-file Turing-to-CA relation plate. No raster supplies an executable table, direction codec, seed, or trace fixture.
- The semantic oracle proves 3,118 native/generic one-event commutations, 38 hostile rejections, exact Langton and relative-turn behavior, six-port topology reuse, explicit frame mapping, quotient-alias rejection, frozen setup-table provenance, and the underdetermined worm boundary.
- No T25 evidence requires a construction-named state class, family executor, hidden control, callback, arbitrary-CA compiler, wider RULE neighborhood, or new UPDATE algebra.

## Final Semantic Conclusions

- The strict main-text family is the T12 unique-head construction parameterized by discrete `t+2D` square-grid topology and four nonzero axis-adjacent movement ports. The Book does not define a numeric direction codec or compass-name ordering, so the raw declared coordinate frame remains explicit.
- A transparent configuration is a total `Z^2` field over `Plain(Sigma) | Head(Q,Sigma)` with exactly one head. The head-bearing cell must retain the underlying tape symbol.
- `NEIGHBORHOOD.read` exposes only the unique head's `(q,a)`. RULE emits `AssignSource(a_next)` plus `MoveHead(q_next,port)`. UPDATE resolves the port and preserves the old destination symbol from the immutable configuration; a concrete two-label assignment batch is only a lossless lowering.
- Absolute displacements and relative turns are distinct program schemas unless a visible orientation factor and a lossless one-event map are supplied. A display arrow must not be reused as motion control without source evidence.
- A finite array used by `TM2DStep` is an implementation realization, not native tape capacity, edge behavior, or halt semantics.
- The strict family is total and ordinarily non-halting. Missing rows, finite-array edge failures, horizons, path-window exits, and fixed/repetitive behavior are not halts.
- Hexagonal worms parameterize topology and visible heading, but the local evidence does not specify the rule schema behind the stated count `1296`. The count and state-as-direction fact are retained without inventing an executable preset or factorization.

## Big Picture Objective

Exhaustively reconstruct two-dimensional Turing machines and every construction-relevant variant from primary Book evidence, then determine the smallest faithful composition of DOMAIN, CONFIGURATION topology/invariants, ALPHABET, FRONTIER, NEIGHBORHOOD, RULE writes, and UPDATE. Prove or refute one-event reuse of T12/T21/T24 without a 2D-Turing executor or lossy simulation.

## Catalog Identity

- Stable ID: T25.
- Exact catalog name: Two-Dimensional Turing Machines.
- CSV line: 26.
- Taxonomy section: 25.
- Entry kind: fixed-support unique-head label evolution under the shared SimpleProgram algebra.
- Audited vocabulary: two-dimensional/2D Turing machine(s), planar/grid tape, four directions, `TM2DStep`, head state/orientation, displacement, turning rules, turtles, worms/Paterson worms, Vants, Turmites, turning machines, Langton's ant, hexagonal grid, path/trajectory, repeated visits, random rules, 2D mobile automata, three-dimensional paths, Notes, captions, actual Index, and emulation relations.

## Search Log

`37-T25-source-oracle.py` freezes Q00-Q29 over direct names, dimensional generalization, captions, executable Notes forms, fixed/relative movement, all aliases and people, Langton/worm/hex history, paths, the distinct 2D-mobile family, inherited Turing semantics, random-start language, broad worm/turning/grid collisions, and dense actual-Index routes. Representative query families include:

```bash
rg -n -i -e 'two-dimensional Turing' -e '2D Turing' -e 'TM2DStep' \
  -e 'turmite' -e 'vant' -e 'turning machine' -e 'Paterson.*worm' \
  ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
rg -n -i -e 'rules based on turning' -e 'Langton.*ant' -e 'mobile turtle' \
  -e 'hexagonal grid' -e 'four possible directions' \
  ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
```

Closure:

- Query union: 71 physical lines = 50 pre-Index + 21 actual Index.
- Retained source: 63 = 30 native + 29 relation + 4 control; 26 are governed continuations outside the direct query union.
- Exclusions: 13 = 2 unrelated worms + 3 unrelated turning + 5 other hex-grid systems + 2 other 2D-grid systems + 1 other emulation construction.
- Index: all 21 routed lines have exact entry guards, including artificial ants, hexagonal/square lattices, randomness, named people, Logo/robotics, worms, `TMs`, Turing aliases, vants, turmites, and turning machines.
- Split corpus: 17 files; query reverse join `63 exact + 7 normalized variants`; retained reverse join `47 exact + 16 normalized variants`; 0 monolith-only.
- Atlas: one taxonomy-summary hit only. Catalog/taxonomy are vocabulary controls.
- Frozen source-oracle SHA-256: `8e20f958faac60cecc4a733282fdcb05a34e003d6bb1da5ec1dc924b49ae723d`.
- Root, relocated-cwd, optimized-mode rejection, silent import, explicit compile, diff, and mode-644 gates pass; `unresolved_total=0`.

## Book Excerpts

### E01 — two-dimensional grid and four absolute movements

- Source: `BOOK:2264-2270`.
- Establishes: dimensional support, unique head movement, four-direction result alphabet, and state/orientation separation.

> Much as for cellular automata, it is straightforward to generalize Turing machines to two dimensions. The basic idea—shown in the picture below—is to allow the head of the Turing machine to move around on a two-dimensional grid rather than just going backwards and forwards on a one-dimensional tape.
>
> the three possible orientations of the arrow on this dot correspond to the three possible states of the head. The rule specifies in which of the four possible directions the head should move at each step. Note that the orientation of the arrow representing the state of the head has no direct relationship to directions on the grid—or to which way the head will move at the next step.

### E02 — blank seed and revisitation

- Source: `BOOK:2294`.
- Establishes: blank initial field for displayed experiments and revisitation without any visit-history state.

> In each case, all cells are initially white, and one of the rules given on the left is applied for the specified number of steps. Note that in the later cases shown, the head often visits the same position on the grid many times.

### E03 — head trajectory is a visualization

- Source: `BOOK:2306`.
- Establishes: the path is derived from the head-position trace rather than additional transition state.

> The path traced out by the head of the two-dimensional Turing machine with rule (e) from the previous page. There are many seemingly random fluctuations in this path, though in general it tends to grow to the right.

### E04 — exact compact rule and step implementation

- Source: `BOOK:13660-13664`.
- Establishes: compact input/output schema, self-only tape read, old-head write, and vector relocation.

> With rules represented as a list of elements of the form `{s, a} -> {sp, ap, {dx, dy}}` (s is the state of the head and a the color of the cell under the head) each step in the evolution of a 2D Turing machine is given by

```text
TM2DStep[rule_, {s_, tape_, r : {x_, y_}}] :=
  Apply[{#1, ReplacePart[tape, #2, {r}], r + #3} &,
        {s, tape[[x, y]]} /. rule]
```

### E05 — aliases and hexagonal/state-direction variant

- Source: `BOOK:13666-13670`.
- Establishes: historical aliases, a hexagonal-grid worm variant whose head state records direction, and Langton's ant as a specific closed rule.

> Michael Paterson and John Conway constructed what they described as an idealization of a prehistoric worm, which was essentially a 2D Turing machine in which the state of the head records the direction of the motion taken at each step. Michael Beeler in 1973 used a computer at MIT to investigate all 1296 possible worms with rules of the simplest type on a hexagonal grid ... systems equivalent to simple 2D Turing machines were reinvented again ... under the name "vants"; ... "turmites"; and ... "turning machines".
>
> The specific 4-state rule ... has been called Langton's ant.

### E06 — relative-turn rules are an explicit alternative

- Source: `BOOK:13678`.
- Establishes: absolute-grid displacements and relative-turn programs are distinct rule presentations whose equivalence obligations remain to be audited.

> The rules used in the main text specify the displacement of the head at each step in terms of fixed directions in the underlying grid. An alternative is to specify the turns to make at each step in the motion of the head. This is how turtles in the Logo computer language are set up.

### E07 — inherited Turing state, self-only rule input, and tagged representation

- Source: `BOOK:940-982`, `BOOK:12014-12037`.
- Establishes: one stateful head, dependence only on head state and the symbol under it, factored `(state,tape,position)` state, atomic write/state/move, total default tape, and an alternative representation that stores head state with the head-bearing cell.

The inherited construction explicitly says neighboring colors do not affect the transition. The Notes give both the factored triple and `MapAt[{state,#},tape,position]` form; the latter is the direct source route to `Plain(symbol) | Head(state,symbol)`.

### E08 — finite table cardinality and the 2D derived count

- Source: `BOOK:12039-12042`; T25 movement arity from `BOOK:2270`.
- Establishes: one row for every `Q x Sigma` input, with `s*k*movement_count` legal outputs per row.

The source gives `(2sk)^(sk)` for two one-dimensional moves. Substituting the four T25 movement ports yields the derived strict-square count `(4sk)^(sk)`: `16^4=65,536` for two states/two symbols, `24^6=191,102,976` for three/two, and `32^8=2^40` for four/two. The Book supplies no T25 integer numbering scheme or direction digit order.

### E09 — transparent composite labels commute one native step at a time

- Source: `BOOK:7938-7948`, `BOOK:18363-18372`.
- Establishes: ordinary and head-bearing cell colors, `k(s+1)` composite labels, exactly one head-bearing label in the seed, and one CA step for one Turing step.

This is evidence for a lossless tagged representation within the existing simple-program machinery. It is not evidence that the compact Turing table should be replaced by an arbitrary table over all composite-label neighborhoods.

### E10 — random examples and initial colors are setup provenance

- Source: `BOOK:2278`, `BOOK:14275`, `BOOK:21899`.
- Establishes: displayed machines may be selected randomly and initial tape colors may be random, while the active/head locus remains definite.

Sampling chooses a complete immutable table or seed before execution. No per-event RNG, stochastic UPDATE, or hidden random state follows.

### E11 — 2D mobile automata remain a distinct RULE restriction

- Source: `BOOK:13679`, with the T25 schema at `BOOK:13662`.
- Establishes: the adjacent 2D-mobile family has `(4k)^k` rules because it has no independent head-state factor; T25 has `(4sk)^(sk)`.

Both use the same SimpleProgram axes and runner. Their different compact input/result schemas are presets, not executor boundaries.

### E12 — histories, paths, and aliases do not add state

- Source: `BOOK:11566`, `BOOK:13666-13674`, actual Index routes `BOOK:20868,20910,20940,21050,21243,21432,21475,21521,21761,21899,21970,21990,22136,22346,22362,22378,22380,22394,22434`.
- Establishes: the Paterson/Conway worm history, Beeler's `1296` count, vants/turmites/turning-machine aliases, and position/path visualizations.

These routes recover provenance and variants. They do not supply the missing exact 1,296-worm rule factorization, make a path native state, or turn an alias into a semantic class.

## Asset Closure

`37-T25-asset-oracle.py` binds exactly the 12 source-governed JPEGs, their 24 monolith/split references, byte lengths, dimensions, unique paths, and SHA-256 hashes:

- 6 native: page-199 construction, four page-200 evolution panels, and the page-200 displayed-rule plate.
- 6 relation: two page-201 path panels, the three-file page-673 Turing-to-CA assembly, and the page-946 Notes path plate.
- 0 control images; 12 unique files/hashes; 562,275 bytes.
- Honest boundary: `HASH_BOUND=12 / TRANSCRIBED=0 / PIXEL_REPLAYED=0`.

The rule plates remain visual evidence only; no glyph row, arrow, coordinate direction, palette, configuration, or trace is recovered from pixels. The page-673 assembly is relation evidence for a one-dimensional Turing machine, not native T25 identity. Root/relocated, optimized rejection, silent import, compile, diff, and mode-644 gates pass. Oracle SHA-256: `06f802c706c26dc4093db6f2004e0ca926a891d10a8a1f16edd5a97de2004e42`.

## Construction Model

```text
DOMAIN = discrete t+2D
Cell   = Plain(TapeSymbol) | Head(HeadState,TapeSymbol)
X      : Z^2 -> Cell
invariant: exactly one site contains Head(...)

active = UniqueTag(Head).select(X)
reads  = HeadSelf.read(X, active)  # exactly (state, underlying symbol)
writes = delta(reads)
       = AssignSource(a_next) + MoveHead(q_next, semantic_port)
next   = AtomicTaggedMove.apply(X, active, writes)

# Inside UPDATE, from the same immutable X:
destination = topology.follow(active, semantic_port)
active      -> Plain(a_next)
destination -> Head(q_next, X[destination].underlying_symbol)
```

The native table is `delta : Q x Sigma -> Q x Sigma x Move2D`, with `Move2D` a declared four-port square-grid displacement schema whose storage order is nonsemantic. The tagged representation is bijective with factored `(tape,head_position,head_state)` state and commutes one event at a time. A nonzero native move can still alias its source, or another port, in a small periodic quotient. Any finite realization must therefore prove the required source/destination and port distinctions, provide a step-commuting virtual-coordinate adapter, or identify itself as a different quotient program.

Turning-relative variants require a visible orientation/state role and a declared action from `(orientation,turn)` to `(orientation_next,absolute_move)`. A hexagonal worm requires a six-port topology and exact coupling evidence. Neither may be implemented by reading renderer arrows or incidental storage order.

## Semantic and Conformance Closure

`37-T25-semantic-oracle.py` keeps two independent representations:

- native `NativeState(state_count,schema,total_tape,head_state,head_position)`;
- generic `TaggedConfiguration` over `Plain(symbol) | Head(state,symbol)` with exactly one `Head`.

It proves `decode(generic_step(delta,encode(native))) = native_step(delta,native)` for 3,118 events:

- 2,048 exhaustive strict-square events: every binary `(q,a)`, every legal `(q_next,a_next,port)`, all 16 neighboring-symbol assignments, and two translated origins;
- 128 Langton context events plus a 128-step exact trace from the source formula;
- 768 six-port visible-heading events on an explicit hex topology;
- 20 unbounded-viewport events, 2 explicit coordinate-frame mapping events, and 24 immutable-table replay events.

The strict exhaustive set proves that changing every candidate destination symbol never changes RULE output, while UPDATE preserves the selected old destination symbol. The exact Langton formula expands to eight closed rows and round-trips through the C4 relative-turn restriction. Two counterexamples prove that arbitrary absolute tables need not factor through relative turns. The hex witness proves topology/action reuse while explicitly leaving the source's `1296` worm schema underdetermined.

Additional guards cover total-default canonicalization, product-table completeness, exact types, stale snapshot tokens, foreign topology frames, invalid ports/states/symbols, zero/two heads, bare-union information loss, atomic zero-head intermediate rejection, size-1/size-2 quotient aliases, size-3 local injectivity, silent coordinate-frame divergence, immutable setup-table replay, observer noninterference, and 38 hostile failures. Semantic digest: `8eed091c1b3635661fb160ce76a49738f282ae1ec94a71fcb8a303a8735434e2`. Root/relocated outputs match, optimized mode fails closed, import is silent, compilation/diff gates pass, and mode is `644`.

## Current API Fit

`src/ca` is the implementation home for the broader SimpleProgram abstraction; its name and current CA-shaped presets do not define its semantic ceiling. `ref/principles/simple_programs.md:15-57,71-87` already requires the branch-free axes, visible control, typed effects, and explicit representations used here.

The legacy `simple_programs.md` specification has reusable mathematical and geometric pieces: abstract alphabet `A` (`:200-215`) and self-only access (`:1303-1322`). Its current frontier-as-writable-target framing (`:1412-1430`), scalar rule result (`:1767-1791`), and absence of an explicit UPDATE axis (`:28-38`) are generic-axis gaps, not proof that T25 needs another library or executor.

| Axis | Smallest fit |
|---|---|
| DOMAIN / CONFIGURATION | Reuse discrete `t+2D`, square `Z^2`, explicit frame/ports; add total default-plus-overrides support and exactly-one-head validation. |
| ALPHABET | Add generic tagged/product finite values; `Plain(Sigma) | Head(Q,Sigma)` is a preset with a checked factored inverse. |
| FRONTIER | Add/reuse configuration-dependent `UniqueTag(Head)`; sources remain distinct from write targets. |
| NEIGHBORHOOD | Directly reuse self-only structured access; do not feed cardinal neighbors or destinations to the compact rule. |
| RULE | Add closed product-key tables returning typed `AssignSource + MoveHead`; no callback or forced T25 integer codec. |
| UPDATE | Generalize D011 movement resolution from line ports to topology ports while keeping one atomic old-snapshot application. |
| Trace / outcome | Preserve complete tagged configurations, events, terminal/external/horizon/error distinctions, then derive paths and rasters. |

## Current Runtime Fit

Current Phase-1 code supplies useful pieces but not yet this generic composition:

- `pyproject.toml:4` and current `rules.py`/`frontiers.py` module prose call the package CA-oriented. Those descriptions lag the governing SimpleProgram design and should be corrected in Goal 2; the `src/ca` path may remain a compatibility namespace without becoming an architecture boundary.
- `src/ca/alphabets.py:40-55` has finite scalar values; tagged/product schemas are the small missing alphabet extension.
- `src/ca/loci.py:31-94` supplies typed coordinate/selectors but only finite rank-0..3 shapes; `:531-614` supplies finite read-boundary machinery, not native unbounded head motion.
- `src/ca/neighborhoods.py:110-137` supplies the correct self access. Cardinal geometry at `:594-614` is reusable as topology-port data, not as T25 RULE input.
- `src/ca/frontiers.py:54-80` exposes only the full time slice. `UniqueTag` is absent.
- `src/ca/rules.py:64-78,262-328` assumes scalar/callable-oriented results. T25 needs closed typed table data and assignment/movement writes.
- `src/ca/specs.py:23-81` has no configuration/alphabet/invariant schema and narrows traces/rule IDs; `:117-198` resolves named families.
- `src/ca/rollout.py:145-212,292-331` dispatches by family; `:643-682` performs dense scalar field updates. Goal 2 replaces this with the already-designed branch-free runner rather than adding a T25 branch.
- Existing neighborhood and dense 2D tests (`tests/test_neighborhoods.py:157-184`, `tests/test_rollout.py:312-376`) validate reusable geometry/realization behavior but not composite labels, unique tags, movement writes, or unbounded support.

Thus the runtime delta is generic and modest: new alphabet, frontier, support, typed-result, topology-port, update, and trace members on existing axes. No construction-named runtime class follows.

## Principles Audit

- Principle 0 is satisfied: no source-supported event defeats the existing SimpleProgram algebra; all T25 profiles classify as reuse, parameterization/restriction, or lossless representation.
- T12's transparent head-tag representation has an explicit inverse and 3,118 one-event commuting witnesses.
- Keep DOMAIN (`t+2D`), CONFIGURATION topology, ALPHABET roles, rule schema, seed, finite realization, trace, and path visualization distinct.
- Do not compile T25 to an arbitrary cellular automaton, infer movement from display orientation, use family dispatch, hide orientation/history, treat finite edges as halt, or substitute a callback for closed rule data.

## Architecture Decision Audit

| Decision | Class | T25 disposition |
|---|---:|---|
| D009 | 1 | Reuse unique old-head firing source; destination is resolved by UPDATE, not added to FRONTIER. |
| D010 | 3 | Reuse visible tagged control; no separate control class or cache. |
| D011 | 1/2 | Reuse atomic old-snapshot UPDATE with typed assignment/movement writes; UPDATE owns destination preservation. |
| D012 | unaffected | T25 does not reuse T09's radius-one read or integer codec; its NEIGHBORHOOD is self-only. |
| D013 | 1/2 | Reuse complete tagged traces; path, visit map, and time-lift are observers. |
| D014 | 3 | Directly reuse `Plain(sigma) | Head(q,sigma)` and exactly-one-head invariance. |
| D121 | 2/3 | Reuse validated blank/default configuration and seed separation. |
| D122 | unaffected | T10 supplies every new block bit; it does not make T25 destinations RULE-visible. |
| D127 | 1/2/3 | Reuse discrete `t+2D`, square `Z^2`, frame/coordinate machinery, and semantic cardinal ports—not T21's all-site frontier or five-cell read. |
| D130 | 1/2/3 | Reuse typed ports/fixed incidence for movement and six-port topology—not its all-site neighborhood preset. |

No completed stage reopens. D011/T09/T12 wording is synchronized so the native read remains exact; their classifications and results are unchanged.

## Goal 2 Implementation Stage

Implement T25 as one ordinary preset of the shared SimpleProgram runner:

1. Generic finite tagged/product alphabet and exactly-one-tag invariant.
2. Total default-plus-overrides `Z^2` field with square topology and four semantic movement ports.
3. `UniqueTag(Head)` FRONTIER and self-only structured projection `(q,a)`.
4. Complete closed `Q x Sigma` table returning `AssignSource(a_next) + MoveHead(q_next,port)`.
5. D011 atomic tagged-movement UPDATE generalized from 1D to topology ports; preserve the old destination symbol internally.
6. Blank tagged seed, complete structured trace/outcomes, and downstream path observers.
7. Closed C4/C6 heading actions for relative-turn/hex variants; exact eight-row Langton fixture; no invented 1,296-worm table.
8. One structural preset and conformance suite; no family branch, callback, or mandatory integer rule ID.

Canonical tests are the semantic-oracle partitions above plus static absence of T25 dispatch, destination-label RULE visibility, hidden control, runtime RNG, implicit boundary behavior, and raster-defined program data.

## No-Cheating Checks

- No `TwoDimensionalTuringState`, T25 rollout, family-name branch, callback, hidden head/orientation, or opaque CA compiler.
- No bare `TapeSymbol union HeadState` that loses the symbol beneath the head.
- No candidate destination label added to NEIGHBORHOOD or exposed to RULE; UPDATE alone resolves/preserves it.
- No arrow glyph, palette, raster orientation, storage row order, or coordinate convention used as semantic movement without an explicit mapping.
- No finite tensor edge, crop, horizon, unvisited cell, fixed point, or missing rule treated as native halt.
- No path image, visit count, behavior class, or random-rule ensemble fed back into the transition.
- No relative-turn and absolute-displacement tables conflated without a visible orientation factor and commuting conversion.
- No hexagonal worm accepted as a square-grid table by invented directions or lossy projection.

## Completion Requirements

- [x] Every alias, variant, caption, Notes line, actual Index route, cross-reference, candidate match, and false positive is dispositioned.
- [x] Every unique construction-relevant excerpt has exact canonical provenance and split-source coverage.
- [x] The strict family and each source-supported variant have complete state/read/rule/write/update/seed/outcome semantics.
- [x] Source-governed assets close with honest transcription and replay boundaries.
- [x] Independent semantic oracles prove non-vacuous native/generic commutation and hostile invariant rejection.
- [x] Current API/runtime/principles fit and smallest Goal 2 delta are implementation-ready.
- [x] All profiles classify in categories 1–3; no new execution algebra is claimed.
- [x] Independent hostile review and all oracle/test/Markdown/diff/scope gates pass.
- [x] `0-plan.md`, `evidence-index.md`, `design-ledger.md`, and `architecture-audit.md` are synchronized; the final cross-stage `goal-2-handoff.md` remains the goal-level synthesis deliverable.

## Stage Results

**COMPLETE.** The frozen Q00-Q29 source audit closes 71 lines at `50 pre-Index / 21 actual-Index`, retains 63 at `30 native / 29 relation / 4 control`, excludes 13, reverse-joins every retained line to the split corpus, and leaves zero unresolved. The dependent 12-image universe closes at 24 exact references, 12 unique hashes, 562,275 bytes, and `12 hash-bound / 0 transcribed / 0 pixel-replayed`. The semantic oracle proves 3,118 native/generic one-event commutations and 38 hostile rejections, including self-only RULE visibility, destination-preserving UPDATE, factored/tagged equivalence, all strict local transitions, exact Langton C4 behavior, six-port topology reuse, relative-turn nonimage counterexamples, coordinate-frame commutation/divergence, quotient aliases, unbounded travel, atomicity, frozen setup provenance, and observer separation.

D131 records a categories-1-to-3 composition of T12, D127, D130, and D011. `src/ca` remains the shared SimpleProgram substrate: T25 adds no state/control class, UPDATE algebra, executor, family branch, callback, hidden interpreter, arbitrary-CA identity, implicit boundary, or invented worm codec. No completed stage reopens. Source, asset, semantic, architecture, hostile-review, portability, fail-closed, import, compile, Markdown, diff, scope, mode, and repository-test gates pass. T26 is next.
