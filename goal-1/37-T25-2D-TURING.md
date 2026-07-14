# 37-T25-2D-TURING

Status: **IN PROGRESS — SOURCE, ASSET, SEMANTIC, AND ARCHITECTURE AUDITS OPEN**

## Current Facts

- T25 is CSV line 26, `Two-Dimensional Turing Machines`; the catalog and `ref/notes/CA-Types.md:687-710` are search guides rather than primary evidence.
- T12 is architecture-reclosed around the lossless cell alphabet `Plain(symbol) | Head(state,symbol)` with exactly one head. The compact `Q x Sigma -> Q x Sigma x Move` table remains native identity; a factored tape/head record is an equivalent view, not a mandatory control class.
- T21/T24 establish discrete `t+2D`, square-grid support, typed coordinates/incidence, and the distinction between DOMAIN, CONFIGURATION topology, representations, realizations, and views.
- The Chapter 5 construction places the head on a two-dimensional grid and gives four possible absolute movement directions (`BOOK:2264-2270`). The displayed arrow orientation denotes head state and explicitly does not denote the next movement direction.
- The Notes implementation uses rows `{state,symbol} -> {next_state,next_symbol,{dx,dy}}`, reads only the symbol at the head, writes the old head cell, and adds the displacement to the old head position (`BOOK:13660-13664`).
- Blank initial cells, repeated visits, head-path drawings, behavior classifications, and random rule sampling are seed/observer/experiment facts until evidence proves otherwise.
- The Notes separately identify turning-relative rules and hexagonal-grid worms, plus `vants`, `turmites`, `turning machines`, and Langton's ant (`BOOK:13666-13678`). Their exact relationship to the strict square-grid absolute-displacement family must be proved rather than inferred from names.
- No T25 evidence inspected so far requires a construction-named state class, family executor, hidden control, opaque CA packing, callback, or new UPDATE policy.

## Updated Assumptions

- The strict main-text family is provisionally the T12 unique-head construction parameterized by discrete `t+2D` square-grid topology and four nonzero axis-adjacent movement ports. The Book does not name an ordered north/east/south/west codec, so the raw declared coordinate frame remains explicit.
- A transparent configuration is a total `Z^2` field over `Plain(Sigma) | Head(Q,Sigma)` with exactly one head. The head-bearing cell must retain the underlying tape symbol.
- The compact RULE reads the unique head's `(q,a)` only. Its structural lowering additionally preserves the old destination symbol while atomically emitting `source -> Plain(a_next)` and `destination -> Head(q_next,old_destination_symbol)`.
- Absolute displacements and relative turns are distinct program schemas unless a visible orientation factor and a lossless one-event map are supplied. A display arrow must not be reused as motion control without source evidence.
- A finite array used by `TM2DStep` is an implementation realization, not native tape capacity, edge behavior, or halt semantics.
- The base family is provisionally total and non-halting. Missing rows, finite-array edge failures, horizons, path-window exits, and fixed/repetitive behavior are not halts.
- Worms on a hexagonal grid may parameterize CONFIGURATION incidence and RULE/result data, but the local Book evidence does not specify the rule schema behind the stated count `1296`. That count and the state-as-direction fact are retained without inventing an executable worm preset or factorization.

## Big Picture Objective

Exhaustively reconstruct two-dimensional Turing machines and every construction-relevant variant from primary Book evidence, then determine the smallest faithful composition of DOMAIN, CONFIGURATION topology/invariants, ALPHABET, FRONTIER, NEIGHBORHOOD, RULE writes, and UPDATE. Prove or refute one-event reuse of T12/T21/T24 without a 2D-Turing executor or lossy simulation.

## Catalog Identity

- Stable ID: T25.
- Exact catalog name: Two-Dimensional Turing Machines.
- CSV line: 26.
- Taxonomy section: 25.
- Entry kind: unresolved while the source/variant audit is open; strict evidence presently indicates fixed-support unique-head label evolution.
- Initial vocabulary: two-dimensional/2D Turing machine(s), planar/grid tape, four directions, `TM2DStep`, head state/orientation, displacement, turning rules, turtles, worms/Paterson worms, Vants, Turmites, turning machines, Langton's ant, hexagonal grid, path/trajectory, repeated visits, random rules, 2D mobile automata, three-dimensional paths, Notes, captions, actual Index, and emulation relations.

## Search Log

The exhaustive protocol is under construction in `37-T25-source-oracle.py`. Initial primary routes are `BOOK:2264-2306`, `BOOK:11566`, `BOOK:13660-13679`, and the actual Index aliases near `BOOK:22378-22380`, `BOOK:22394`, and `BOOK:22434`. Every direct, alias, Notes, caption, split, history, relation, behavior, and false-positive route remains open until the frozen oracle partitions it with zero unresolved candidates.

Representative searches begun:

```bash
rg -n -i -e 'two-dimensional Turing' -e '2D Turing' -e 'TM2DStep' \
  -e 'turmite' -e 'vant' -e 'turning machine' -e 'Paterson.*worm' \
  ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
rg -n -i -e 'rules based on turning' -e 'Langton.*ant' -e 'mobile turtle' \
  -e 'hexagonal grid' -e 'four possible directions' \
  ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
```

No search-count or exhaustion claim is made yet.

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

## Construction Model Under Test

```text
DOMAIN = discrete t+2D
Cell   = Plain(TapeSymbol) | Head(HeadState,TapeSymbol)
X      : Z^2 -> Cell
invariant: exactly one site contains Head(...)

active = UniqueTag(Head).select(X)
reads  = HeadRead.read(X, active)  # (state, underlying symbol), plus destination preservation for lowering
(q_next, a_next, move) = delta(reads)
writes = {
    active:        Plain(a_next),
    active + move: Head(q_next, old_underlying_symbol_at_destination),
}
next = AtomicLabelUpdate.apply(X, active, writes)
```

The native table is provisionally `delta : Q x Sigma -> Q x Sigma x Move2D`, with `Move2D` a declared four-port square-grid displacement schema whose storage order is nonsemantic. The representation proof must show a bijection with factored `(tape,head_position,head_state)` state and one-event commutation. A nonzero native move can still alias its source, or another port, in a small periodic quotient. Any finite realization must therefore prove the required source/destination and port distinctions, provide a step-commuting virtual-coordinate adapter, or identify itself as a different quotient program.

Turning-relative variants require a visible orientation/state role and a declared action from `(orientation,turn)` to `(orientation_next,absolute_move)`. A hexagonal worm requires a six-port topology and exact coupling evidence. Neither may be implemented by reading renderer arrows or incidental storage order.

## Current API Fit

Open. The audit must compare the construction with `simple_programs.md`, especially composite alphabets, typed coordinates/topology, unique-tag selection, access provenance, compact closed tables, typed multi-write results, atomic old-snapshot UPDATE, total sparse/default support, outcomes, and trace encoding.

## Current Runtime Fit

Open. Expected reusable pieces include finite scalar alphabets, selector concepts, typed same-site assignment machinery, and fixed-lattice snapshot behavior. Expected mismatches include scalar-only labels, rank-specific coordinate/address assumptions, absent unique-tag frontier, absent total sparse `Z^2` support, scalar rule outputs, named-family dispatch, fixed-width rule identities, and value-only traces. These are hypotheses until exact modules/tests are cited.

## Principles Audit

- Apply Principle 0 if turning rules, hexagonal worms, or source images expose a state/topology coupling that the provisional parameterization cannot preserve.
- Reuse T12's transparent head-tag representation only with an explicit inverse and one-event commuting proof.
- Keep DOMAIN (`t+2D`), CONFIGURATION topology, ALPHABET roles, rule schema, seed, finite realization, trace, and path visualization distinct.
- Do not compile T25 to an arbitrary cellular automaton, infer movement from display orientation, use family dispatch, hide orientation/history, treat finite edges as halt, or substitute a callback for closed rule data.

## Detailed Implementation Plan

1. Freeze a zero-remainder source protocol across monolith, Notes, actual Index, split corpus, Atlas, catalog, and taxonomy controls.
2. Derive and hash-bind the source-governed asset universe; separate source-stated rule/seed/horizon data from raster inference.
3. Build independent native/factored and generic/tagged one-event semantic oracles for strict square-grid rules and every source-supported rule/topology variant.
4. Audit current API/runtime/tests and D009-D014, D122, D127, and D130 from first principles.
5. Add a new decision only if a concrete event cannot be expressed by reuse, parameterization, or lossless representation.
6. Obtain independent hostile review, run all portability/fail-closed/import/compile/Markdown/diff/scope/test gates, and synchronize all global Goal 1 artifacts.

## Goal 2 Implementation Stage

Open pending evidence closure. The likely smallest delta is to compose T12's compact unique-head table/tagged-cell representation with T21/T24's `t+2D` typed square-grid support and a four-displacement result schema. Turning-relative and hexagonal presets require explicit source-backed mappings and invariants, not family executors.

## No-Cheating Checks

- No `TwoDimensionalTuringState`, T25 rollout, family-name branch, callback, hidden head/orientation, or opaque CA compiler.
- No bare `TapeSymbol union HeadState` that loses the symbol beneath the head.
- No arrow glyph, palette, raster orientation, storage row order, or coordinate convention used as semantic movement without an explicit mapping.
- No finite tensor edge, crop, horizon, unvisited cell, fixed point, or missing rule treated as native halt.
- No path image, visit count, behavior class, or random-rule ensemble fed back into the transition.
- No relative-turn and absolute-displacement tables conflated without a visible orientation factor and commuting conversion.
- No hexagonal worm accepted as a square-grid table by invented directions or lossy projection.

## Completion Requirements

- [ ] Every alias, variant, caption, Notes line, actual Index route, cross-reference, candidate match, and false positive is dispositioned.
- [ ] Every unique construction-relevant excerpt has exact canonical provenance and split-source coverage.
- [ ] The strict family and each source-supported variant have complete state/read/rule/write/update/seed/outcome semantics.
- [ ] Source-governed assets close with honest transcription and replay boundaries.
- [ ] Independent semantic oracles prove non-vacuous native/generic commutation and hostile invariant rejection.
- [ ] Current API/runtime/principles fit and smallest Goal 2 delta are implementation-ready.
- [ ] Any claimed new execution algebra has a concrete one-event counterexample; otherwise categories 1–3 reuse is recorded.
- [ ] Independent hostile review and all oracle/test/Markdown/diff/scope gates pass.
- [ ] `0-plan.md`, `evidence-index.md`, `design-ledger.md`, `architecture-audit.md`, and `goal-2-handoff.md` are synchronized.

## Stage Results

In progress. Source, asset, semantic, architecture, hostile-review, and global integration closure remain open.
