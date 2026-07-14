# 39-T28-CONTEXTUAL-2D-SUBSTITUTION

Status: **IN PROGRESS — SOURCE, ASSET, SEMANTIC, AND ARCHITECTURE AUDITS ACTIVE**

## Current Facts

- T28 is CSV physical line 29, `Neighbor-Dependent Two-Dimensional Substitution Systems`; `ref/notes/CA-Types.md` section 28 is search vocabulary, not primary mechanics.
- The main text first contrasts neighbor-independent grid subdivision and free geometric replacement, then says non-nested behavior comes from allowing a grid element's replacement to depend on neighboring elements (`BOOK:2350-2356`).
- The main plate is `BOOK:2362 -> _page_207_Figure_1.jpeg`. Its printed caption declares a two-dimensional neighbor-dependent substitution system whose grid wraps in both dimensions, one seven-snapshot trace, five displayed compact rule rows, and eight eight-step examples. The rule glyphs remain raster evidence until any transcription is independently bounded and verified.
- The Notes give the exact step skeleton `Flatten2D[Partition[list, {2, 2}, 1, -1] /. rule]` and one displayed contextual row, followed by an explicit warning that unequal subdivision can create arbitrarily many possible neighborhood configurations (`BOOK:13806-13810`).
- The local extraction corrupts the first slot of that displayed row as `-`. The official Wolfram Science text at `https://www.wolframscience.com/nks/notes-5-4--neighbor-dependent-2d-substitution-systems/` gives the exact Mathematica blank `_`: `{{_,1},{0,1}} -> {{1,0},{1,1}}`. This is a one-glyph official-source repair, not a generic normalization rule.
- The scalar fourth argument `-1` in this source expression aligns the old cell at the lower-right position of each cyclic `2 x 2` window. Together with the plate's wrap caption, the strict contextual read is provisionally the periodic northwest block `(NW,N,W,Self)` for every old tile; this alignment remains a semantic-oracle obligation rather than an uncited convention.
- T14 established that overlapping old reads change FRONTIER/NEIGHBORHOOD/RULE choice without creating overlapping writes or a new executor. T26 established generic rank-two compatible mosaic assembly and its positive uniform-block preset. T28 must test their composition rather than introduce a contextual-2D engine.
- The Notes recover one binary `2 x 2` output row, but not the complete plate table or a palette-to-label map. Uniform `2 x 2` output is therefore a declared executable restriction used in the proof, not a claimed transcription of all five raster glyphs. The Notes explicitly allow a broader mixed-subdivision variant and state that its neighborhood configuration space is generally unbounded; the finite rectangular profile and that broader warning must not be conflated.
- Current `simple_programs.md` and `src/ca` are fixed-array/CA-shaped realizations. They do not currently expose changing rectangular support, source-bound patch writes, explicit UPDATE policies, structured step results, or branch-free family-independent execution. These are Goal 2 gaps, not evidence for a T28 state class or rollout.

## Updated Assumptions

- **Retained:** T28 has canonical parallel stepwise evolution and belongs in the common `SimpleProgram` runner.
- **Retained:** context selection belongs to NEIGHBORHOOD/RULE, while patch compatibility and assembly belong to UPDATE.
- **Retained:** periodic boundary behavior is part of the strict source profile and must be explicit in CONFIGURATION/topology or its declared realization.
- **Under test:** every strict source row can be represented faithfully as a finite closed ordered literal/wildcard contextual table, or compiled to an exhaustive table while separately preserving source spelling/provenance, plus a positive rectangular patch. `ReplaceAll` establishes first-match priority; the audit must not reorder overlapping rows.
- **Retained:** any finite source-defined compatible patch table uses D132 directly; a declared common positive `2 x 2` shape uses D132's uniform restriction. The complete raster plate is not replayable, so its full shape table is unclaimed.
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

## Source Audit

`39-T28-source-oracle.py` is the fail-closed evidence record. Its 25 frozen query lanes cover the direct construction name, contextual mechanics, the exact Notes expression, wrap/cyclic aliases, page routes, the T14 one-dimensional analog, the T26 aligned base, the T27 free-geometric contrast, the higher-dimensional sequential-scan boundary, the CA singleton-output relation, network and constraint controls, actual Index entries, native/cross-reference image links, and explicit absence of common modern aliases and padding language.

The query union contains 67 canonical monolith lines: 52 before the actual Index and 15 actual-Index routes. The pre-Index hits close as 41 retained plus 11 excluded. Thirty semantically governed continuation lines make 71 retained lines in total, partitioned as `6 native / 13 relation / 52 control`. All 15 Index routes are guarded by exact entry fragments and partition as `2 native T28 / 3 T14 alias controls / 10 T26 sibling routes`. The split-corpus reverse join closes 66 query records as `53 exact + 13 mapped` and all 71 retained lines as `48 exact + 23 mapped`, with zero monolith-only retained evidence and zero unresolved candidates.

The frozen searches can be reproduced directly:

```bash
rg -n -i 'neighbor[- ]dependent (two[- ]dimensional|2D)|two[- ]dimensional.*neighbor[- ]dependent|neighbor[- ]dependent.*substitution' \
  ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
rg -n -i 'replacement for a particular element|sets up elements on a grid|depend on its neighbors|arbitrarily large set of different possible neighborhood' \
  ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
rg -n 'Flatten2D|Partition\[list, \{2, 2\}, 1, -1\]' \
  ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
python3 goal-1/39-T28-source-oracle.py
```

The oracle deliberately returns no direct hits for modern phrases such as `contextual two-dimensional substitution`, `tile substitution`, or padding/boundary-symbol menus. It does not treat those absences as proof that the construction is missing; they prevent modern terminology from silently becoming source semantics. Its eleven exclusions are nine ordinary-T26 downstream references, one unrelated CA-cryptanalysis occurrence, and one generic encoding-function occurrence.

## Book Excerpts

### E01 — contextual choice is the mechanism that breaks pure nesting

- Source: `BOOK:2350-2356`.
- Section/context: Chapter 5, `Substitution Systems and Fractals`, immediately before the page-192 plate.
- Establishes: replacements read neighboring old elements; a grid supplies a stable neighbor relation; free geometric replacement does not.

> the replacement for a particular element at a given step can depend not only on the characteristics of that element itself, but also on the characteristics of other neighboring elements.
>
> if one sets up elements on a grid it is straightforward to allow the replacements for a given element to depend on its neighbors

### E02 — the main plate is the strict visual construction record

- Source: `BOOK:2362 -> ref/A-New-Kind-of-Science/CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_207_Figure_1.jpeg`.
- Section/context: page-192 figure between contextual-grid prose and the sequential-scanning boundary.
- Establishes: the strict displayed grid wraps in both dimensions; one full trace reaches step 7; five compact rule glyphs and eight eight-step examples are shown.
- Evidence boundary: image identity, dimensions, and linkage will be hash-bound. No rule row or trace cell is semantic data unless separately transcribed and verified.

### E03 — exact Notes step skeleton

- Source: `BOOK:13806-13810`.
- Section/context: Notes for page 192, `Neighbor-dependent substitution systems`.
- Establishes: every step partitions the complete old rank-two list into overlapping periodic `2 x 2` contexts, applies individual replacement rules, and assembles the resulting patches with `Flatten2D`; unequal subdivision generally destroys a finite bounded neighborhood-schema assumption.
- Source repair: the official online note corrects the local OCR/extraction glyph `-` to the Mathematica blank `_` in the exact example row:

```text
{{_,1},{0,1}} -> {{1,0},{1,1}}
```

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

### E06 — the one-dimensional contextual analog changes reads and eligibility

- Source: `BOOK:1018-1024`, exact Notes at `BOOK:12109-12115`, and relation plate `BOOK:1020`.
- Establishes: T14 reads an old element and its immediate right neighbor; the final old element is excluded because it has no complete open-boundary context. This is a responsibility-level precedent for contextual rule choice, not T28's frontier or boundary preset.

### E07 — singleton outputs recover fixed-support CA behavior

- Source: `BOOK:8022-8028` and relation plate `BOOK:8026`.
- Establishes: highly uniform neighbor-dependent substitution rules whose every replacement contains one cell correspond directly to cellular automata. This is a restriction/representation relation, not evidence that CA is the enclosing abstraction and not evidence for a separate executor.

### E08 — the actual Index fixes the native route

- Source: `BOOK:22144`.
- Establishes: the Book indexes `Substitution systems ... neighbor-dependent 2D, 192, 935`. The ordinary 2D, one-dimensional neighbor-dependent, and CA-emulation entries are separately dispositioned rather than silently merged.

### E09 — networks and constraints are semantic controls

- Source: `BOOK:2368-2376`, `2464`, and `2568-2600`.
- Establishes: loss of fixed underlying support motivates network systems, while constraint systems replace explicit evolution with model conditions. Neither distinction applies to T28's explicit periodic grid step, but both prevent overclaiming that every later Book construction is this same preset.

### Exact source-repair boundary

The local monolith's `BOOK:13806` renders the first pattern slot as `-`, which is not executable as the intended Mathematica blank. The official Wolfram Science note, `notes-5-4--neighbor-dependent-2d-substitution-systems`, gives `_`. The audit permits exactly this one substitution in exactly this one example row. It does not repair any raster glyph, infer a complete table, or establish a general OCR-normalization policy.

## Asset Audit

`39-T28-asset-oracle.py` binds the exact source-governed universe of ten JPEGs to unique physical paths, monolith references, split references, byte lengths, dimensions, SHA-256 values, evidence roles, and assembly membership. It partitions them as `1 native / 2 relation / 7 control`, closes `20 references = 10 monolith + 10 split`, ten unique hashes, 1,112,143 bytes, and two paired assemblies covering four files. The other six assets are standalone.

| Role | `BOOK` image lines | Evidence boundary |
|---|---|---|
| Native | `2362` | Exact T28 plate; caption and panel counts only |
| Relation | `1020`, `8026` | T14 contextual analog and singleton-output CA relation |
| Control | `2314`, `2322`, `2328`, `2330`, `2340`, `2344`, `2354` | T26 aligned replacement and T27 free-geometry contrasts |

The mechanical adjacency closure contains seventeen candidates. Seven are explicitly excluded and not hash-bound: `2302`, `8018`, `8036`, `8038`, `13800`, `13802`, and `13804`. They are, respectively, the preceding T25 path observer, adjacent Turing/sequential CA-emulation plates, and unrelated Mandelbrot images near the Notes heading.

The evidence boundary is `10 HASH_BOUND / 1 LIMITED_TRANSCRIBED / 0 PIXEL_REPLAYED`. For `BOOK:2362`, the limited manual transcription records only the printed construction name, the statement that the grid wraps in both dimensions, displayed labels `step 1` through `step 7`, five top rule panels, eight gallery panels `(a)` through `(h)`, and the gallery's eight-step caption. Exact glyph contents, complete rule table, seed, intermediate arrays, trace, palette map, and gallery cell arrays remain unrecovered.

## Construction Model

- **DOMAIN:** discrete `t+2D`.
- **CONFIGURATION:** finite nonempty rectangular grid with periodic incidence in both spatial axes; dimensions may change after replacement.
- **ALPHABET:** finite tile labels. The exact Notes row uses `0/1`; the proof's binary profile is explicit, while the raster palette-to-label map remains untranscribed.
- **SEED:** the plate begins from a displayed finite grid; no exact raster seed is claimed.
- **FRONTIER:** every old tile exactly once, with row/column product order used for assembly and source-bound lineage.
- **NEIGHBORHOOD:** an ordered cyclic `2 x 2` old-snapshot block aligned so `Self` is the lower-right member. The one exact Notes row ignores its northwest slot; no global factorization of the unrecovered plate table is claimed.
- **RULE:** a finite closed ordered contextual product-pattern table over typed `Literal(label) | Blank` slots, or a behavior-equivalent exhaustive expansion with source form retained separately, returning one positive rectangular patch over the same alphabet for each selected old source. Ordered overlap uses first match; validation proves every finite context has a match. A desired fallback must be an explicit final row, never host `ReplaceAll` behavior.
- **UPDATE:** T26 `RankedBlockMosaicAssemble(rank=2)`; a declared uniform positive `2 x 2` rule set uses `RankedUniformBlockAssemble(rank=2)`. UPDATE validates complete source/write coverage and mosaic compatibility before allocating and committing one successor. No exact execution of the unrecovered plate table is claimed.
- **SCHEDULE:** all reads and rule choices use one immutable old toroidal snapshot; all patches commit atomically; newborn tiles wait until the next event.
- **OUTCOME:** a valid complete strict table advances one deterministic generation even for an identity result. Invalid/missing/ambiguous pattern coverage or incompatible patches produce typed no-commit invalidity, not a halt or partial successor.
- **LINEAGE:** every old tile owns its emitted patch rectangle and exact parent-local children. Context cells influence rule choice without becoming additional parents.
- **OBSERVERS:** raster scale, grayscale antialiasing, nestedness/complexity descriptions, and display crops do not enter program state.

### Exact one-step factorization

For an old grid `G` of shape `H x W`, let source `(y,x)` read

```text
C_G(y,x) = ((G[y-1,x-1], G[y-1,x]),
            (G[y,  x-1], G[y,  x]))
```

with both indices reduced modulo `(H,W)`. This is the derived lower-right/self alignment of `Partition[..., {2,2}, 1, -1]`. It deliberately retains four ordered slot occurrences even when periodic aliasing makes several slots name the same physical tile on `1 x 1`, `1 x W`, or `H x 1` grids. Incidence multiplicity is part of the read; deduplicating coordinates changes the rule input.

The ordered table selects one patch `P[y,x]` from `C_G(y,x)`. UPDATE receives exactly one source-bound patch for every old tile and applies D132:

```text
active = AllOldTiles.select(G)
reads  = PeriodicProductWindow(NW,N,W,Self).read(G, active)
writes = OrderedProductPatternTable(rows).apply(active, reads)
next   = RankedBlockMosaicAssemble(rank=2).apply(G, active, writes)
```

No context slot is itself a write target. Each patch is owned by the selected `Self` source; the other three old occurrences influence choice only. UPDATE first validates source-token provenance, exactly-once source coverage, positive rectangular patches, and D132 mosaic compatibility, then assembles one successor in old-source/product order. This makes overlapping reads harmless: there is no overlapping write ownership to resolve.

### Pattern language and executable-profile boundary

The repaired Notes row means exactly

```text
((Blank, Literal(1)), (Literal(0), Literal(1)))
    -> ((1,0), (1,1))
```

and therefore matches both values of the northwest slot in the binary profile. Rows are immutable ordered data. First-match priority is observable when two patterns overlap, so an unordered map or row sorting is not equivalent. Because the finite alphabet and four slots make the strict context space finite, validation can expand rows to a complete literal table and reject any missing context before execution. If a separate importer promises exact Mathematica `ReplaceAll` behavior for incomplete rule lists, it must materialize every nonmatch as explicit context-preserving literal rows (or an explicit closed final template) during import; the core runtime never inherits a host fallback implicitly. Expansion is a behavior realization, not by itself a lossless encoding of source syntax: shadowed rows, different factorizations, and different orderings can denote the same literal function. Retaining the normalized source rows and provenance alongside the compiled table preserves program identity without a hidden host-pattern interpreter.

The complete native plate table, native seed, and native trace are raster-only and deliberately unavailable. The executable oracle therefore uses the one exact repaired row as a matching fixture and independently declared synthetic complete tables to prove the construction. It never claims to replay the page-192 example.

### Unequal-subdivision boundary

`BOOK:13810` explicitly permits replacements where only some elements subdivide, then warns that the two-dimensional neighborhood configurations around a cell are generally arbitrarily numerous. This is native evidence for a broader adaptive construction, but not enough evidence to freeze its carrier, adjacency update, matching schema, compatibility conditions, or exact trace. A fixed four-slot rectangular-grid rule table cannot claim that variant merely by accepting differently sized arrays.

The honest result is an open profile inside the same SimpleProgram architecture: it may require a dynamic hierarchical/cell-complex CONFIGURATION and a topology-derived NEIGHBORHOOD, while still using the same branch-free select/read/write/apply runner. Goal 2 must not add a callback, unbounded opaque pattern object, family executor, or padded rectangular approximation. The strict finite periodic profile can be implemented independently; the adaptive profile remains unavailable until primary evidence or an explicit separately sourced specification closes those mechanics.

## Semantic Proof

`39-T28-semantic-oracle.py` defines two independent evaluators:

1. a direct mathematical operator that takes periodic lower-right `2 x 2` contexts, chooses the first matching clause, and performs compatible rank-two mosaic assembly; and
2. the generic four-axis pipeline with snapshot-bound sources, declared ordered access, compiled closed table rows, source-bound patch writes, and D132 UPDATE.

The comparison is over complete typed results rather than successor pixels alone. Each evaluator independently mints source/successor tokens; an explicit reversible token relation compares them while preserving outcome, successor cardinality, `changed`, step presence, grid/topology, every source/read/write record, patch rectangle, local child ordinal/coordinate, parent ownership, and complete lineage. The test never makes raw token equality semantic.

The bounded proof includes a binary order-four de Bruijn torus containing all sixteen ordered contexts exactly once, exhaustive small periodic rectangles including degenerate `1 x 1`, `1 x 2`, `2 x 1`, and larger asymmetric shapes, multiple complete uniform tables, compatible mixed patches, identity advancement, and a one-cell-output fixed-support restriction. The repaired source row is tested for both northwest values.

The hostile set independently forces divergences or typed rejection for:

- lower-right versus upper-left alignment;
- periodic versus open/padded boundaries;
- four ordered incidence occurrences versus coordinate deduplication on small tori;
- first-match clause order versus unordered/reordered rows;
- missing table coverage and implicit host fallback;
- stale, cross-run, duplicate, missing, and forged source handles;
- old-snapshot evaluation versus row-major newborn/in-place reads;
- product-aware mosaic assembly versus flat source-block concatenation;
- context participants incorrectly recorded as co-parents;
- patch incompatibility, partial commit, padding, or cropping;
- syntax-losing wildcard compilation, raster-derived rules, callbacks, and family dispatch; and
- treating the adaptive unequal-subdivision caveat as a finite four-slot rectangular preset.

The mixed-size boundary is constructive: adjacent sources emitting `1 x 1` and `2 x 2` patches fail D132's row compatibility, while the Book warns that a faithful adaptive continuation can require unbounded neighborhood configurations. This counterexample proves only that the regular rectangular preset is not total for the broader variant. It does not justify a T28 executor or prove that the shared SimpleProgram runner is inadequate.

## API Classification

| Element | Audit class | Smallest reusable base | Required invariant or mapping |
|---|---|---|---|
| DOMAIN | 2, parameterization | D127 discrete `t+2D` | DOMAIN records dimensional task space only; support/topology stay in CONFIGURATION |
| Periodic changing grid | 1/2, direct composition | D127 periodic incidence + D132 rectangular changing configuration | finite nonempty rectangle, both axes cyclic, successor revalidated; no fixed NumPy-shape assumption |
| FRONTIER | 1, direct reuse | T26 `AllOldTiles` | every old tile exactly once with an opaque exact-snapshot handle |
| Context read | 2, parameterization/new schema on an existing axis | generic ordered product access, with T14 contextual responsibility and D127 periodic slots | declared `(NW,N,W,Self)` order, lower-right alignment, periodic slot multiplicity, old-snapshot provenance |
| Pattern table | 2 plus behavior realization | generic closed finite RULE data | immutable ordered `Literal | Blank` rows, first-match priority, finite total coverage, explicit defaults only; exhaustive compilation retains source rows/provenance because compilation is not injective |
| Patch write | 1, direct reuse | T26 source-bound positive rectangular patch | owner is `Self`; context participants are influences, not parents |
| UPDATE | 1, direct reuse | D132 `RankedBlockMosaicAssemble(rank=2)`; uniform plate restriction uses its named uniform wrapper | complete coverage, mosaic compatibility, exact product placement, atomic no-commit invalidity, parent consumption, newborn deferral, lineage |
| Result/trace | 2, parameterization | D132 structured `PatchStepResult` | dynamic shapes, periodic topology, full read/write witnesses, opaque token relation, typed invalidity |

T28 therefore uses audit categories 1–3 and introduces no category-4 execution algebra. The only Goal 2 implementation additions specifically exposed by T28 are reusable access and RULE schemas. D132 already owns the required UPDATE implementation.

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
- No compact pattern reordered or treated as an unordered map; the source's ordered first-match behavior is preserved, and missing coverage is rejected rather than delegated to host `ReplaceAll` fallback.
- No unequal-subdivision profile declared finite/total without closing its potentially unbounded neighborhood configurations.

## Completion Requirements

- [ ] Every direct name, alias, variant, caption, Notes line, actual Index route, cross-reference, candidate match, and false positive is dispositioned with zero unresolved candidates.
- [ ] Every retained line has canonical monolith provenance and split reverse coverage or an explicit split omission.
- [ ] The governed asset universe is exact, hash-bound, and honest about transcription and pixel replay.
- [ ] Strict configuration, topology, seed, frontier, reads, rule data, writes, update, successor, invalidity, lineage, and observer semantics are reconstructed.
- [ ] The `Partition[...,{2,2},1,-1]` alignment and wraparound behavior are independently proved.
- [ ] The local `-`/official `_` source defect, literal/wildcard schema, first-match priority, and complete-coverage law are independently pinned.
- [ ] Direct and generic one-step semantics commute non-vacuously, including adversarial boundaries, overlap, snapshot, assembly, and invalidity.
- [ ] The compact-pattern and unequal-subdivision boundaries are explicit and do not introduce callbacks or hidden infinite schemas.
- [ ] Current API/runtime/tests are inspected and the smallest Goal 2 delta is implementation-ready.
- [ ] T14/T26 reuse and every affected ledger decision are re-audited; contradicted stages are reopened rather than patched.
- [ ] All oracle, portability, fail-closed, import, compile, repository-test, mode, Markdown, diff, scope, and hostile-review gates pass.
- [ ] `0-plan.md`, `evidence-index.md`, `design-ledger.md`, and `architecture-audit.md` are synchronized.

## Stage Results

**IN PROGRESS.** Source, asset, and semantic audits are running independently. No final construction classification, decision ID, metric, hash, or completion claim is frozen yet.
