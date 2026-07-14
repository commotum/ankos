# 39-T28-CONTEXTUAL-2D-SUBSTITUTION

Status: **IN PROGRESS — SOURCE, ASSET, SEMANTIC, AND ARCHITECTURE AUDITS ACTIVE**

## Current Facts

- T28 is CSV physical line 29, `Neighbor-Dependent Two-Dimensional Substitution Systems`; `ref/notes/CA-Types.md` section 28 is search vocabulary, not primary mechanics.
- The main text first contrasts neighbor-independent grid subdivision and free geometric replacement, then says non-nested behavior comes from allowing a grid element's replacement to depend on neighboring elements (`BOOK:2350-2356`).
- The main plate is `BOOK:2354 -> _page_207_Figure_1.jpeg`. Its printed caption declares a two-dimensional neighbor-dependent substitution system whose grid wraps in both dimensions, one seven-snapshot trace, five displayed compact rule rows, and eight eight-step examples. The rule glyphs remain raster evidence until any transcription is independently bounded and verified.
- The Notes give the exact step skeleton `Flatten2D[Partition[list, {2, 2}, 1, -1] /. rule]` and one displayed contextual row, followed by an explicit warning that unequal subdivision can create arbitrarily many possible neighborhood configurations (`BOOK:13806-13810`).
- The scalar fourth argument `-1` in this source expression aligns the old cell at the lower-right position of each cyclic `2 x 2` window. Together with the plate's wrap caption, the strict contextual read is provisionally the periodic northwest block `(NW,N,W,Self)` for every old tile; this alignment remains a semantic-oracle obligation rather than an uncited convention.
- T14 established that overlapping old reads change FRONTIER/NEIGHBORHOOD/RULE choice without creating overlapping writes or a new executor. T26 established generic rank-two compatible mosaic assembly and its positive uniform-block preset. T28 must test their composition rather than introduce a contextual-2D engine.
- The main plate appears to use uniform `2 x 2` outputs. The Notes explicitly allow a broader mixed-subdivision variant, but also state that its neighborhood configuration space is generally unbounded. The strict executable profile and that broader warning must not be conflated.
- Current `simple_programs.md` and `src/ca` are fixed-array/CA-shaped realizations. They do not currently expose changing rectangular support, source-bound patch writes, explicit UPDATE policies, structured step results, or branch-free family-independent execution. These are Goal 2 gaps, not evidence for a T28 state class or rollout.

## Updated Assumptions

- **Retained:** T28 has canonical parallel stepwise evolution and belongs in the common `SimpleProgram` runner.
- **Retained:** context selection belongs to NEIGHBORHOOD/RULE, while patch compatibility and assembly belong to UPDATE.
- **Retained:** periodic boundary behavior is part of the strict source profile and must be explicit in CONFIGURATION/topology or its declared realization.
- **Under test:** every strict source row can be represented losslessly as a finite closed contextual table over an ordered old-snapshot projection plus a positive rectangular patch.
- **Under test:** the strict plate is exactly the positive uniform `2 x 2` restriction of T26 UPDATE; the Notes' unequal-subdivision warning may instead be a non-finite-schema boundary rather than a second native preset.
- **Rejected unless evidenced:** open, padded, reflected, dropped, infinite-background, or user-callback boundary menus; free geometric neighbors; sequential scans; hidden raster decoding; and a T28 executor.

## Big Picture Objective

Reconstruct the exact two-dimensional contextual substitution construction and every evidenced variant, then determine whether it is precisely T14-style immutable contextual choice feeding T26 rank-two patch assembly. Close source, plate, Notes, Index, split, cross-reference, false-positive, semantic, runtime-fit, and Goal 2 obligations without duplicating either prior construction or inventing unsupported boundary and pattern languages.

## Catalog Identity

- Stable ID: T28.
- Exact CSV name: `Neighbor-Dependent Two-Dimensional Substitution Systems`.
- CSV physical line: 29.
- Taxonomy section: 28.
- Provisional entry kind: contextual rank-two grid-replacement preset in discrete `t+2D`.
- Initial vocabulary: neighbor-dependent/contextual two-dimensional/2D substitution, neighboring elements, grid replacement, subdivision, `Partition[list,{2,2},1,-1]`, `Flatten2D`, cyclic/wraparound grid, northwest context, compact pattern rules, page 192/935, non-nested behavior, unequal subdivision, sequential higher-dimensional scanning, cellular-automaton relation, L-system relation, and Index aliases.

## Search Log

The frozen source oracle will replace this provisional log with a query-by-query disjoint manifest. Searches already inspected include:

```bash
rg -n -i 'neighbor[- ]dependent (two[- ]dimensional|2D)|two[- ]dimensional.*neighbor[- ]dependent|neighbor[- ]dependent.*substitution' \
  ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
rg -n -i 'replacement for a particular element|sets up elements on a grid|depend on its neighbors|arbitrarily large set of different possible neighborhood' \
  ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
rg -n 'Flatten2D|Partition\[list, \{2, 2\}, 1, -1\]' \
  ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
```

Known high-signal candidates are `BOOK:2312-2356`, `BOOK:2358-2366`, `BOOK:8024-8028`, `BOOK:12109-12115`, `BOOK:12249-12251`, `BOOK:13806-13810`, and the actual Index route at `BOOK:22144`. Their native/relation/control dispositions remain to be frozen.

## Book Excerpts

### E01 — contextual choice is the mechanism that breaks pure nesting

- Source: `BOOK:2350-2356`.
- Section/context: Chapter 5, `Substitution Systems and Fractals`, immediately before the page-192 plate.
- Establishes: replacements read neighboring old elements; a grid supplies a stable neighbor relation; free geometric replacement does not.

> the replacement for a particular element at a given step can depend not only on the characteristics of that element itself, but also on the characteristics of other neighboring elements.
>
> if one sets up elements on a grid it is straightforward to allow the replacements for a given element to depend on its neighbors

### E02 — the main plate is the strict visual construction record

- Source: `BOOK:2354 -> ref/A-New-Kind-of-Science/CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_207_Figure_1.jpeg`.
- Section/context: page-192 figure between contextual-grid prose and the sequential-scanning boundary.
- Establishes: the strict displayed grid wraps in both dimensions; one full trace reaches step 7; five compact rule glyphs and eight eight-step examples are shown.
- Evidence boundary: image identity, dimensions, and linkage will be hash-bound. No rule row or trace cell is semantic data unless separately transcribed and verified.

### E03 — exact Notes step skeleton

- Source: `BOOK:13806-13810`.
- Section/context: Notes for page 192, `Neighbor-dependent substitution systems`.
- Establishes: every step partitions the complete old rank-two list into overlapping periodic `2 x 2` contexts, applies individual replacement rules, and assembles the resulting patches with `Flatten2D`; unequal subdivision generally destroys a finite bounded neighborhood-schema assumption.

```text
Flatten2D[Partition[list, {2, 2}, 1, -1] /. rule]
```

### E04 — ordinary aligned substitution is the noncontextual base

- Source: `BOOK:2312-2324` and the exact T26 Notes implementation at `BOOK:13681-13689`.
- Section/context: beginning of Chapter 5 substitution discussion and Notes for page 187.
- Establishes: T26 already owns rank-two old-generation patch assembly; T28 changes the rule input, not product-order placement.

### E05 — sequential higher-dimensional scanning is a control, not the T28 schedule

- Source: `BOOK:2358-2366`.
- Section/context: prose immediately following the T28 plate.
- Establishes: a particular 2D scan order reduces to a 1D ordering and is not the parallel contextual system shown above it.

> as soon as one defines any particular order for elements ... this in effect reduces one to dealing with a one-dimensional system.

Additional direct, caption, Notes, history, Index, emulation, constraint, and false-positive excerpts remain under audit.

## Construction Model

The following is provisional until source and semantic oracles close.

- **DOMAIN:** discrete `t+2D`.
- **CONFIGURATION:** finite nonempty rectangular grid with periodic incidence in both spatial axes; dimensions may change after replacement.
- **ALPHABET:** finite tile labels; the strict plate is binary.
- **SEED:** the plate begins from a displayed finite grid; exact raster transcription is not yet claimed.
- **FRONTIER:** every old tile exactly once, with row/column product order used for assembly and source-bound lineage.
- **NEIGHBORHOOD:** an ordered cyclic `2 x 2` old-snapshot block aligned so `Self` is the lower-right member; the compact plate appears to ignore/factor at least one slot, but the exact factorization remains to be proved.
- **RULE:** a finite closed ordered contextual pattern table or its lossless exhaustive expansion, returning one positive rectangular patch over the same alphabet for each selected old source.
- **UPDATE:** T26 `RankedBlockMosaicAssemble(rank=2)`; the strict uniform `2 x 2` plate uses `RankedUniformBlockAssemble(rank=2)`. UPDATE validates complete source/write coverage and mosaic compatibility before allocating and committing one successor.
- **SCHEDULE:** all reads and rule choices use one immutable old toroidal snapshot; all patches commit atomically; newborn tiles wait until the next event.
- **OUTCOME:** a valid complete strict table advances one deterministic generation even for an identity result. Invalid/missing/ambiguous pattern coverage or incompatible patches produce typed no-commit invalidity, not a halt or partial successor.
- **LINEAGE:** every old tile owns its emitted patch rectangle and exact parent-local children. Context cells influence rule choice without becoming additional parents.
- **OBSERVERS:** raster scale, grayscale antialiasing, nestedness/complexity descriptions, and display crops do not enter program state.

## Current API Fit

| Element | Provisional fit | Smallest base | Gap/obligation |
|---|---|---|---|
| DOMAIN | `PARAMETERIZATION` | discrete `t+2D` | normalize DOMAIN/support vocabulary |
| Periodic changing grid | `PRINCIPLED EXTENSION` of current document realization | D127 periodic incidence plus D132 changing rectangular support | explicit configuration/topology and per-successor validation |
| FRONTIER | `DIRECT` | T26 `AllOldTiles` | opaque exact-snapshot handles |
| Context read | `PARAMETERIZATION` | generic ordered access; T14 contextual-read precedent | exact periodic `2 x 2` alignment and slot significance |
| Pattern table | `PARAMETERIZATION` or lossless representation | closed finite tuple-key table | prove totality, rule order/overlap behavior, wildcard expansion, and inverse-on-image |
| Patch write | `DIRECT` | T26 source-bound rectangular patch | bind to exact old source and alphabet |
| UPDATE | `DIRECT` if strict outputs are uniform; otherwise D132 general policy | `RankedBlockMosaicAssemble(rank=2)` | full coverage, compatibility, no-commit invalidity, lineage |
| Trace/result | `PARAMETERIZATION` | structured `PatchStepResult` | ragged generation shapes and periodic topology metadata |

## Current Runtime Fit

- `src/ca/loci.py` supplies reusable selector composition and finite coordinate ordering, but its fixed `[t,x,y,z]` dense realization is not the native changing-grid configuration.
- `src/ca/neighborhoods.py` supplies ordered offset-selection ideas, but reads are currently dense-array coordinate gathers rather than topology-bound source projections with exact snapshot provenance.
- `src/ca/frontiers.py` exposes only dense current-slice selection for executable rollout, not source-bound old-tile occurrences.
- `src/ca/rules.py` returns scalar same-site values and has family-specific finite codecs; it lacks typed rectangular patch results and closed contextual pattern expansion.
- `src/ca/rollout.py` assumes same-shape dense outputs and branches on family names. T28 must not add another branch.
- `src/ca/specs.py` and raw trace records require fixed shapes/dense homogeneous arrays; changing grids and structured lineage require Goal 2 trace/result work already motivated by T13/T26.

## Principles Audit

- Principles 0-3: test composition before naming a construction class. T28 currently changes access and rule data while reusing T26 UPDATE.
- Principle 4: RULE returns a typed source-bound patch, not a scalar, callback, whole-grid replacement, or raster.
- Principles 5-8: the periodic topology and complete old grid remain visible; an exhaustive compact-table lowering must be lossless and one-step, with no hidden pattern interpreter.
- Principles 9-10: contextual offsets, compact independence restrictions, periodicity, and uniform block shape are declarative schema/preset choices with strict validation.
- Principle 11: snapshot-parallel rule choice and rank-two product assembly are defining semantics, not incidental algorithms.
- Principles 13-16: adversaries must cover alignment, wraparound, overlapping reads, wildcard overlap/order, missing rows, incompatible patches, in-place newborn reads, flat concatenation, raster dependence, and family dispatch.

## Detailed Implementation Plan

1. Freeze a complete monolith query manifest with direct/alias/mechanics/caption/Notes/Index/cross-reference/control dispositions and split reverse coverage.
2. Freeze the source-governed image universe and honest transcription/replay boundary.
3. Implement an independent direct operator for periodic `2 x 2` contexts and compare it against a generic T14-read/T26-write/update pipeline.
4. Prove exact alignment, all-source coverage, overlapping read/non-overlapping ownership, newborn deferral, product-order assembly, boundary effects, typed invalidity, and lineage.
5. Decide the finite compact-pattern representation and explicitly bound the unequal-subdivision warning.
6. Audit `simple_programs.md`, concrete runtime modules/tests, and every affected ledger decision.
7. Integrate accepted facts into `0-plan.md`, `evidence-index.md`, `design-ledger.md`, `architecture-audit.md`, and the eventual Goal 2 handoff.
8. Run portability, fail-closed, silent-import, compile, test, mode, Markdown, diff, stale-fact, and independent hostile-review gates.

## Goal 2 Implementation Stage

Objective: add no T28 executor. Compose a finite periodic changing-grid configuration, `AllOldTiles`, an exact ordered cyclic contextual access schema, a closed finite context-to-patch table, T26 source-bound patch writes, and D132 ranked mosaic UPDATE in the shared branch-free runner.

Provisional dependencies: D011 old-snapshot atomicity; D019/D124 source-bound contextual reads and exact-snapshot provenance; D127/D130 topology-aware offsets/ports; D132 ranked mosaic assembly, compatibility, invalidity, and lineage.

Required conformance will include the source's exact Notes row, synthetic exhaustive tables over all finite contexts, strict periodic edge/corner witnesses, direct/generic one-step commutation, uniform and compatible-mixed patches where evidenced, incompatible no-commit outcomes, and static absence of T28 dispatch, callbacks, padding, hidden raster data, flat assembly, in-place reads, or sequential scans.

## No-Cheating Checks

- No `Contextual2DSubstitutionState`, T28 UPDATE, T28 executor, family branch, or callback.
- No whole old grid or source program packed into one alphabet value.
- No raster glyph, grayscale, pixel position, or display crop used as an unstated rule row.
- No padding/reflection/open boundary imported into the strict periodic profile.
- No sequential row-major/spiral scan hidden inside parallel rule choice.
- No flat concatenation substituted for rank-two product assembly.
- No context cell assigned parenthood merely because it influenced a source's patch.
- No newborn tile read during its producing event.
- No missing or ambiguous compact pattern resolved by rule-order guesses unless the source establishes that order.
- No unequal-subdivision profile declared finite/total without closing its potentially unbounded neighborhood configurations.

## Completion Requirements

- [ ] Every direct name, alias, variant, caption, Notes line, actual Index route, cross-reference, candidate match, and false positive is dispositioned with zero unresolved candidates.
- [ ] Every retained line has canonical monolith provenance and split reverse coverage or an explicit split omission.
- [ ] The governed asset universe is exact, hash-bound, and honest about transcription and pixel replay.
- [ ] Strict configuration, topology, seed, frontier, reads, rule data, writes, update, successor, invalidity, lineage, and observer semantics are reconstructed.
- [ ] The `Partition[...,{2,2},1,-1]` alignment and wraparound behavior are independently proved.
- [ ] Direct and generic one-step semantics commute non-vacuously, including adversarial boundaries, overlap, snapshot, assembly, and invalidity.
- [ ] The compact-pattern and unequal-subdivision boundaries are explicit and do not introduce callbacks or hidden infinite schemas.
- [ ] Current API/runtime/tests are inspected and the smallest Goal 2 delta is implementation-ready.
- [ ] T14/T26 reuse and every affected ledger decision are re-audited; contradicted stages are reopened rather than patched.
- [ ] All oracle, portability, fail-closed, import, compile, repository-test, mode, Markdown, diff, scope, and hostile-review gates pass.
- [ ] `0-plan.md`, `evidence-index.md`, `design-ledger.md`, and `architecture-audit.md` are synchronized.

## Stage Results

**IN PROGRESS.** Source, asset, and semantic audits are running independently. No final construction classification, decision ID, metric, hash, or completion claim is frozen yet.
