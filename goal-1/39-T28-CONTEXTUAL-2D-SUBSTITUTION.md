# 39-T28-CONTEXTUAL-2D-SUBSTITUTION

Status: **COMPLETE — SOURCE, ASSET, SEMANTIC, RUNTIME-FIT, ARCHITECTURE, AND INDEPENDENT HOSTILE REVIEW CLOSED**

## Current Facts

- T28 is CSV physical line 29, `Neighbor-Dependent Two-Dimensional Substitution Systems`; `ref/notes/CA-Types.md` section 28 is search vocabulary, not primary mechanics.
- The main text first contrasts neighbor-independent grid subdivision and free geometric replacement, then says non-nested behavior comes from allowing a grid element's replacement to depend on neighboring elements (`BOOK:2350-2356`).
- The main plate is `BOOK:2362 -> _page_207_Figure_1.jpeg`. Its printed caption declares a two-dimensional neighbor-dependent substitution system whose grid wraps in both dimensions, one seven-snapshot trace, five displayed compact rule rows, and eight eight-step examples. The rule glyphs remain raster evidence until any transcription is independently bounded and verified.
- The Notes give the exact step skeleton `Flatten2D[Partition[list, {2, 2}, 1, -1] /. rule]` and one displayed contextual row, followed by an explicit warning that unequal subdivision can create arbitrarily many possible neighborhood configurations (`BOOK:13806-13810`).
- The local extraction corrupts the first slot of that displayed row as `-`. The official Wolfram Science text at `https://www.wolframscience.com/nks/notes-5-4--neighbor-dependent-2d-substitution-systems/` gives the exact Mathematica blank `_`: `{{_,1},{0,1}} -> {{1,0},{1,1}}`. This is a one-glyph official-source repair, not a generic normalization rule.
- The scalar fourth argument `-1` in this source expression aligns the old cell at the lower-right position of each cyclic `2 x 2` window. The hash-bound Wolfram Language semantics snapshot freezes the official `Partition` scalar-to-pair law, multidimensional scalar expansion, beginning-overhang alignment, default cyclic padding, and negative-position convention. Together with the plate's wrap caption, these derive the periodic northwest block `(NW,N,W,Self)` for every old tile; 682 exhaustive small-torus configurations and a divergent upper-left control then close implementation agreement and distinguish the opposite alignment.
- T14 established that overlapping old reads change FRONTIER/NEIGHBORHOOD/RULE choice without creating overlapping writes or a new executor. T26 established generic rank-two compatible mosaic assembly and its positive uniform-block preset. T28 must test their composition rather than introduce a contextual-2D engine.
- The Notes recover one binary `2 x 2` output row, but not the complete plate table or a palette-to-label map. Uniform `2 x 2` output is therefore a declared executable restriction used in the proof, not a claimed transcription of all five raster glyphs. The Notes explicitly allow a broader mixed-subdivision variant and state that its neighborhood configuration space is generally unbounded; the finite rectangular profile and that broader warning must not be conflated.
- Current `simple_programs.md` and `src/ca` are fixed-array/CA-shaped realizations. They do not currently expose changing rectangular support, source-bound patch writes, explicit UPDATE policies, structured step results, or branch-free family-independent execution. These are Goal 2 gaps, not evidence for a T28 state class or rollout.

## Updated Assumptions

- **Retained:** T28 has canonical parallel stepwise evolution and belongs in the common `SimpleProgram` runner.
- **Retained:** context selection belongs to NEIGHBORHOOD/RULE, while patch compatibility and assembly belong to UPDATE.
- **Retained:** periodic boundary behavior is part of the strict source profile and must be explicit in CONFIGURATION/topology or its declared realization.
- **Retained:** every recovered source row can be represented faithfully as a finite closed ordered literal/anonymous-wildcard contextual table, or compiled behaviorally to an exhaustive table while separately preserving source spelling/provenance, plus a positive rectangular patch. The official `Blank` and `ReplaceAll` documentation binds `_` as one anonymous expression pattern, first-applicable-rule priority, and unchanged nonmatch behavior; the audit must not reorder overlapping rows or inherit fallback implicitly.
- **Retained:** any finite aligned rectangular product-grid profile whose emitted patches satisfy D132 compatibility uses D132 directly; a declared common positive `2 x 2` shape uses D132's uniform restriction. The complete raster plate is not replayable, so its full shape table is unclaimed, and this result does not cover the adaptive unequal-subdivision profile.
- **Rejected unless evidenced:** open, padded, reflected, dropped, infinite-background, or user-callback boundary menus; free geometric neighbors; sequential scans; hidden raster decoding; and a T28 executor.

## Big Picture Objective

Reconstruct the exact two-dimensional contextual substitution construction and every evidenced variant, then determine whether it is precisely T14-style immutable contextual choice feeding T26 rank-two patch assembly. Close source, plate, Notes, Index, split, cross-reference, false-positive, semantic, runtime-fit, and Goal 2 obligations without duplicating either prior construction or inventing unsupported boundary and pattern languages.

## Catalog Identity

- Stable ID: T28.
- Exact CSV name: `Neighbor-Dependent Two-Dimensional Substitution Systems`.
- CSV physical line: 29.
- Taxonomy section: 28.
- Entry kind: contextual rank-two grid-replacement preset in discrete `t+2D`; the adaptive unequal-subdivision generalization remains an open profile.
- Initial vocabulary: neighbor-dependent/contextual two-dimensional/2D substitution, neighboring elements, grid replacement, subdivision, `Partition[list,{2,2},1,-1]`, `Flatten2D`, cyclic/wraparound grid, northwest context, compact pattern rules, page 192/935, non-nested behavior, unequal subdivision, sequential higher-dimensional scanning, cellular-automaton relation, L-system relation, and Index aliases.

## Source Audit

`39-T28-source-oracle.py` is the fail-closed evidence record. The offline `39-T28-official-note-snapshot.txt` freezes the canonical Wolfram Science URL, retrieval date, fetched-document SHA-256, exact raw HTML rule and step spans, decoded rule, and one-glyph normalization scope; the oracle hash-checks the snapshot and derives the repaired Book row from it. The separate `39-T28-wolfram-language-semantics-snapshot.txt` freezes official `Partition`, `Part`, `Blank`, and `ReplaceAll` URLs, fetched-document hashes, anchored semantics, and their exact T28 consequence; the oracle derives and compares the language-defined window and checks ordered-match/nonmatch witnesses. Its 25 frozen query lanes cover the direct construction name, contextual mechanics, the exact Notes expression, wrap/cyclic aliases, page routes, the T14 one-dimensional analog, the T26 aligned base, the T27 free-geometric contrast, the higher-dimensional sequential-scan boundary, the CA singleton-output relation, network and constraint controls, actual Index entries, native/cross-reference image links, and explicit absence of common modern aliases and padding language.

The query union contains 67 canonical monolith lines: 52 before the actual Index and 15 actual-Index routes. The pre-Index hits close as 41 retained plus 11 excluded. Thirty-one semantically governed continuation lines make 72 retained lines in total, partitioned as `6 native / 13 relation / 53 control`. All 15 Index routes are guarded by exact entry fragments and partition as `2 native T28 / 3 T14 alias controls / 10 T26 sibling routes`. The split-corpus reverse join closes 66 query records as `53 exact + 13 mapped` and all 72 retained lines as `49 exact + 23 mapped`, with zero monolith-only retained evidence and zero unresolved candidates. The added exact split witness at `BOOK:2358` closes the cited ordinary-versus-sequential setup immediately before the higher-dimensional scanning control.

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
- Source repair: the hash-bound official-note snapshot corrects the local OCR/extraction glyph `-` to the Mathematica blank `_` in the exact example row. The snapshot SHA is `ba1aff54973afd0cd42cb7afc41220dd11835a0cb5b3d8d9ce8f5e9fe3d1b866`; it records fetched-document SHA `f28a332211082048417abce950a75756a4bdae7c7d48f3f12ab87ffdab02328c`.
- Host-language binding: the Wolfram Language semantics snapshot SHA is `89dc720f5f905d41821c4284457cf75d08de2cae66af501789f26746682c6589`. It records fetched-document SHAs for `Partition`, `Part`, `Blank`, and `ReplaceAll` as `8aa77bf72ab99e507767c443d4150d5f466627e73c5e221c56e15a12690867f1`, `942ef91b5cb8275b1ef594e8802ad568ed88a8444b5138576380bd861c9fd470`, `0e4fd687eee1e87dbe7b8d311718787e135b5736591ce0ff6aa18edba6ad2b3d`, and `e3e1e4e2f3a47c677b17c83e8541f9a355ce2c72d844b7fd9a366e4938626366`.

The exact repaired row and source step expression are:

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

The local monolith's `BOOK:13806` renders the first pattern slot as `-`, which is not executable as the intended Mathematica blank. The official Wolfram Science note, `notes-5-4--neighbor-dependent-2d-substitution-systems`, gives `_`. The offline note snapshot stores the exact raw HTML span and the `Flatten2D` span, is itself SHA-bound, and records the SHA of the fetched official document; the oracle derives the escaped repaired row from the decoded snapshot row. The separate official-language snapshot binds `_` to `Blank[]`, which can stand for any one expression. The audit permits exactly this one substitution in exactly this one example row. It does not repair any raster glyph, infer a complete table, or establish a general OCR-normalization policy.

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
- **RULE:** a finite closed ordered contextual product-pattern table over typed `Literal(label) | AnonymousAny` slots, with source `_` parsed as `AnonymousAny`, or a behavior-equivalent exhaustive expansion with source form retained separately. Each selected source returns one positive rectangular patch over the same alphabet. Ordered overlap is valid and uses first match; construction validation proves every finite context has a match after any explicit source-import totalization. A desired fallback must be explicit data, never latent host behavior.
- **UPDATE:** T26 `RankedBlockMosaicAssemble(rank=2)`; a declared uniform positive `2 x 2` rule set uses `RankedUniformBlockAssemble(rank=2)`. UPDATE validates complete source/write coverage and mosaic compatibility before allocating and committing one successor. No exact execution of the unrecovered plate table is claimed.
- **SCHEDULE:** all reads and rule choices use one immutable old toroidal snapshot; all patches commit atomically; newborn tiles wait until the next event.
- **OUTCOME:** a valid complete strict table advances one deterministic generation even for an identity result. Malformed patterns and missing finite coverage reject the program at construction time; ordered overlap is resolved by priority and is not ambiguous. Only state-dependent failure such as D132 mosaic incompatibility yields a typed step-level `Invalid` with no successor or partial commit.
- **LINEAGE:** every old tile owns its emitted patch rectangle and exact parent-local children. Context cells influence rule choice without becoming additional parents.
- **OBSERVERS:** raster scale, grayscale antialiasing, nestedness/complexity descriptions, and display crops do not enter program state.

### Exact one-step factorization

For an old grid `G` of shape `H x W`, let source `(y,x)` read

```text
C_G(y,x) = ((G[y-1,x-1], G[y-1,x]),
            (G[y,  x-1], G[y,  x]))
```

with both indices reduced modulo `(H,W)`. This is the official-language-derived lower-right/self alignment of `Partition[..., {2,2}, 1, -1]`: scalar `d=1` applies at both levels; scalar `k=-1` expands to the same alignment pair at both levels; negative `-1` denotes the last block position; beginning overhang uses the old array as cyclic padding. It deliberately retains four ordered slot occurrences even when periodic aliasing makes several slots name the same physical tile on `1 x 1`, `1 x W`, or `H x 1` grids. Incidence multiplicity is part of the read; deduplicating coordinates changes the rule input.

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
((AnonymousAny, Literal(1)), (Literal(0), Literal(1)))
    -> ((1,0), (1,1))
```

and therefore matches both values of the northwest slot in the binary profile. The official `Blank` documentation supplies that anonymous one-expression meaning. Rows are immutable ordered data. Official `ReplaceAll` semantics select the first applicable rule for a part and return that part unchanged if none applies, though traversal can still rewrite matching subparts. Under this declared importer every left-hand side is a complete `2 x 2` product pattern over scalar slots, so such patterns cannot match row or scalar subparts; an unmatched whole context is therefore unchanged. First-match priority is observable when two patterns overlap, so an unordered map or row sorting is not equivalent. Because the finite alphabet and four slots make the strict context space finite, validation can expand rows to a complete literal table and reject any missing context before execution. If a separate importer promises this exact Mathematica `ReplaceAll` behavior for incomplete rule lists, it must materialize every nonmatch as explicit context-preserving literal rows (or an explicit closed final template) during import; the core runtime never inherits the now-explicitly-bound host fallback implicitly. Expansion is a behavior realization, not by itself a lossless encoding of source syntax: shadowed rows, different factorizations, and different orderings can denote the same literal function. Retaining the normalized source rows and provenance alongside the compiled table preserves program identity without a hidden host-pattern interpreter.

The complete native plate table, native seed, and native trace are raster-only and deliberately unavailable. The executable oracle therefore uses the one exact repaired row as a matching fixture and independently declared synthetic complete tables to prove the construction. It never claims to replay the page-192 example.

### Unequal-subdivision boundary

`BOOK:13810` explicitly permits replacements where only some elements subdivide, then warns that the two-dimensional neighborhood configurations around a cell are generally arbitrarily numerous. This is native evidence for a broader adaptive construction, but not enough evidence to freeze its carrier, adjacency update, matching schema, compatibility conditions, or exact trace. A fixed four-slot rectangular-grid rule table cannot claim that variant merely by accepting differently sized arrays.

The honest result is an open profile that may require a dynamic hierarchical/cell-complex CONFIGURATION and topology-derived NEIGHBORHOOD. If its canonical step is later recovered, the shared branch-free select/read/write/apply runner is the first candidate, but the missing carrier/incidence/matching/update mechanics prevent claiming that fit now. Goal 2 must not add a callback, unbounded opaque pattern object, family executor, or padded rectangular approximation. The strict finite periodic product-grid profile can be implemented independently; the adaptive profile remains unavailable until primary evidence or an explicit separately sourced specification closes those mechanics.

## Semantic Proof

`39-T28-semantic-oracle.py` defines two independent evaluators:

1. a direct mathematical operator that takes periodic lower-right `2 x 2` contexts, chooses the first matching clause, and performs compatible rank-two mosaic assembly; and
2. the generic four-axis pipeline with snapshot-bound sources, declared ordered access, compiled closed table rows, source-bound patch writes, and D132 UPDATE.

The comparison is over complete typed results rather than successor pixels alone. Each evaluator independently mints source/successor tokens; an explicit reversible token relation compares them while preserving outcome, successor cardinality, `changed`, step presence, grid/topology, every source/read/write record, patch rectangle, local child ordinal/coordinate, parent ownership, and complete lineage. The test never makes raw token equality semantic.

The bounded proof includes a `4 x 4` binary de Bruijn torus for `2 x 2` contexts containing all sixteen ordered contexts exactly once, exhaustive small periodic rectangles including degenerate `1 x 1`, `1 x 2`, `2 x 1`, and larger asymmetric shapes, multiple complete uniform tables, synthetic D132-compatible aligned mixed patches used only as a composition stress test, identity advancement, and a one-cell-output fixed-support restriction. The repaired source row is tested for both northwest values.

The proof, closed schemas, documented source boundary, and explicit hostile witnesses jointly exclude:

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

The frozen proof closes:

- 682 exhaustive binary periodic rectangles through `3 x 3`, comprising 5,506 independently checked `(NW,N,W,Self)` reads;
- the guarded source Blank row, which matches exactly two of sixteen binary contexts;
- 65,536 bounded full-`StepResult` commutations on the `4 x 4` de Bruijn torus, comprising 1,048,576 firings and 4,194,304 parent-local child witnesses;
- one D132-compatible crossed-width mixed mosaic and two independently commuting typed incompatible/no-commit outcomes;
- one explicit lower-right/upper-left divergence; and
- 57 hostile construction, provenance, representation, boundary, schedule, and shortcut rejections.

The bounded family chooses between two distinct asymmetric `2 x 2` patches for each of the sixteen binary contexts. It is a proof basis of `2^16 = 65,536` tables, not a source-authored rule numbering. The full derived binary uniform-`2 x 2` family has `(2^4)^(2^4) = 2^64` tables; the Book supplies no integer codec for it. The frozen semantic digest is `82b03edcc186e9ceccdffb33f1e90fb671a64e4dd008eec057a11f6339f44209`.

## API Classification

| Element | Audit class | Smallest reusable base | Required invariant or mapping |
|---|---|---|---|
| DOMAIN | 2, parameterization | D127 discrete `t+2D` | DOMAIN records dimensional task space only; support/topology stay in CONFIGURATION |
| Periodic changing grid | 1/2, direct composition | D127 periodic incidence + D132 rectangular changing configuration | finite nonempty rectangle, both axes cyclic, successor revalidated; no fixed NumPy-shape assumption |
| FRONTIER | 1, direct reuse | T26 `AllOldTiles` | every old tile exactly once with an opaque exact-snapshot handle |
| Context read | 2, parameterization/new schema on an existing axis | generic ordered product access, with T14 contextual responsibility and D127 periodic slots | declared `(NW,N,W,Self)` order, lower-right alignment, periodic slot multiplicity, old-snapshot provenance |
| Pattern table | 2 plus behavior realization | D037-style closed structural pattern data restricted to a fixed product, or generic finite RULE data | immutable ordered `Literal | AnonymousAny` rows, first-match priority, finite total coverage, explicit defaults only; exhaustive compilation retains source rows/provenance because compilation is not injective |
| Patch write | 1, direct reuse | T26 source-bound positive rectangular patch | owner is `Self`; context participants are influences, not parents |
| UPDATE | 1, direct reuse for the finite aligned profile | D132 `RankedBlockMosaicAssemble(rank=2)`; a separately declared common-shape restriction uses its named uniform wrapper | Cartesian source-address coverage, aligned rectangular mosaic compatibility, exact product placement, atomic no-commit invalidity, parent consumption, newborn deferral, lineage; no claim over the unresolved adaptive profile |
| Result/trace | 2, parameterization | D132 structured `PatchStepResult` | dynamic shapes, periodic topology, full read/write witnesses, opaque token relation, typed invalidity |

T28 therefore uses audit categories 1–3 and introduces no category-4 execution algebra. The only Goal 2 implementation additions specifically exposed by T28 are reusable access and RULE schemas. D132 already owns the required UPDATE implementation.

## Current Runtime Fit

- `src/ca/loci.py:531-614` already maps periodic axes independently and preserves repeated query occurrences after quotient aliasing. Its fixed `[t,x,y,z]` dense realization and lack of snapshot-bound source handles remain gaps. Goal 2 must declare a bijection such as semantic `(row,column) <-> (x=column,y=row)` and apply the corresponding storage transpose/offset map; it may not derive meaning from array order.
- `src/ca/neighborhoods.py:140-174` already provides an ordered four-offset stencil mechanism, and a direct `1 x 2` periodic probe retains all four aliased occurrences. T28 is therefore a named-slot/provenance parameterization of existing geometric gathering, not a new neighborhood execution algebra. `loci.py:22,257-280` exposes only incidental `none|lex` ordering, so semantic slot names and the axis codec must wrap it explicitly.
- `src/ca/frontiers.py:54-80` has the all-current-site responsibility needed by `AllOldTiles`, but executable rollout does not expose typed source-bound old-tile occurrences.
- `src/ca/rules.py` returns scalar same-site values and has family-specific finite codecs; it lacks typed rectangular patch results and closed contextual pattern expansion.
- `src/ca/rollout.py` assumes same-shape dense outputs and branches on family names. T28 must not add another branch.
- `src/ca/specs.py` and raw trace records require fixed shapes/dense homogeneous arrays; changing grids and structured lineage require Goal 2 trace/result work already motivated by T13/T26.
- `src/ca/specs.py:23-55` has no ALPHABET or UPDATE field, so it cannot validate finite-context totality or patch-label closure; `:117-198` cannot declare literal offsets or a closed ordered pattern table structurally.
- `src/ca/rollout.py:155,190,825-831` family-checks the frontier but does not execute its selector, instead re-enumerating coordinates at `:691-702`. Existing tests pin only a one-dimensional periodic gather and fixed dense two-dimensional rollout, not torus corners, degenerate-axis occurrence multiplicity, pattern priority/totalization, patches, provenance, or lineage.

## Principles Audit

- Principles 0-3: test composition before naming a construction class. T28 currently changes access and rule data while reusing T26 UPDATE.
- Principle 4: RULE returns a typed source-bound patch, not a scalar, callback, whole-grid replacement, or raster.
- Principles 5-8: the periodic topology and complete old grid remain visible. Compact-to-exhaustive lowering is behavior-preserving but not injective; lossless program identity retains the ordered closed source AST and provenance alongside compiled behavior, with no hidden host interpreter.
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

Dependencies: D011 old-snapshot atomicity; D019/D124 source-bound contextual reads and exact-snapshot provenance; D037 closed structural pattern data at the responsibility level; D127/D130 topology-aware offsets/ports and coordinate codecs; D132 ranked mosaic assembly, compatibility, invalidity, and lineage.

Implementation-ready delta:

1. Reuse the generic finite-alphabet schema. Add no T28 alphabet; validate every patch label against the declared alphabet.
2. Reuse D132's finite positive rectangular configuration and per-successor extent validation, with explicit periodic incidence on both axes. Declare the semantic `(row,column) <-> (x=column,y=row)` codec and corresponding dense-storage transpose when using current arrays.
3. Reuse `AllOldTiles`, upgraded to return opaque source handles bound to the exact old snapshot and Cartesian addresses. Do not depend on the current rollout's implicit coordinate enumeration.
4. Add or name a generic ordered product access schema with semantic slots `NW,N,W,Self`, offsets `(-1,-1),(-1,0),(0,-1),(0,0)`, lower-right source alignment, periodic mapping, and preserved occurrence multiplicity after aliases. Current `literal_offsets`/`gather(periodic)` can realize the value read after the slot/axis/provenance wrapper is explicit.
5. Add a closed ordered fixed-product pattern schema with `Literal(value)` and `AnonymousAny`. Parse the repaired source `_` only through the guarded source adapter. Validate first-match rows, output patch closure, and finite total coverage at construction.
6. Compile valid clauses to the canonical exhaustive context table for execution, but retain the ordered source AST and provenance. If a source importer promises Wolfram `ReplaceAll` nonmatch semantics, make every fallback row/template explicit during import.
7. Reuse T26 source-bound positive rectangular patch writes. Bind each patch only to the selected `Self` source; context participants stay read witnesses, not parents.
8. Reuse `RankedBlockMosaicAssemble(rank=2)` unchanged. It validates Cartesian coverage and row-height/slab-width compatibility before allocation, commits exact product placement atomically, consumes parents, defers newborns, and returns D132 typed invalid/no-commit results.
9. Extend structured ragged traces only as already required by D132: preserve periodic topology, every named-slot read, chosen clause/source form, compiled row, write, patch rectangle, child witness, lineage, and opaque token scope. Do not store raster or host matcher state.
10. Offer an optional T28 preset that assembles these ordinary axes. It must be data construction only—no state class, UPDATE class, executor, rollout branch, callback, or hidden boundary menu.
11. Mark adaptive unequal subdivision unavailable. Do not implement it until its dynamic carrier, incidence, neighborhood matching, and update mechanics are separately specified and proved.

Required conformance includes the exact Notes row, synthetic exhaustive tables over all finite contexts, strict periodic edge/corner and degenerate-axis witnesses, direct/generic full-result commutation through explicit token renaming, declared uniform patches, synthetic D132-compatible mixed patches as a composition stress test rather than a native plate claim, incompatible no-commit outcomes, and static absence of T28 dispatch, callbacks, padding, hidden raster data, flat assembly, in-place reads, or sequential scans.

## No-Cheating Checks

- No `Contextual2DSubstitutionState`, T28 UPDATE, T28 executor, family branch, or callback.
- No whole old grid or source program packed into one alphabet value.
- No raster glyph, grayscale, pixel position, or display crop used as an unstated rule row.
- No padding/reflection/open boundary imported into the strict periodic profile.
- No sequential row-major/spiral scan hidden inside parallel rule choice.
- No flat concatenation substituted for rank-two product assembly.
- No context cell assigned parenthood merely because it influenced a source's patch.
- No newborn tile read during its producing event.
- No compact pattern reordered or treated as an unordered map; the source's ordered first-match behavior is preserved. Missing coverage is rejected during program construction unless an explicit source importer has materialized the promised `ReplaceAll` nonmatch behavior as closed total data.
- No unequal-subdivision profile declared finite/total without closing its potentially unbounded neighborhood configurations.

## Completion Requirements

- [x] Every direct name, alias, variant, caption, Notes line, actual Index route, cross-reference, candidate match, and false positive is dispositioned with zero unresolved candidates.
- [x] Every retained line has canonical monolith provenance and split reverse coverage or an explicit split omission.
- [x] The governed asset universe is exact, hash-bound, and honest about transcription and pixel replay.
- [x] Strict configuration, topology, seed boundary, frontier, reads, rule data, writes, update, successor, invalidity, lineage, and observer semantics are reconstructed.
- [x] The `Partition[...,{2,2},1,-1]` alignment and wraparound behavior are independently proved.
- [x] The local `-`/official `_` source defect, literal/wildcard schema, first-match priority, and complete-coverage law are independently pinned.
- [x] Direct and generic one-step semantics commute non-vacuously, including adversarial boundaries, overlap, snapshot, assembly, invalidity, and full typed results.
- [x] The compact-pattern and unequal-subdivision boundaries are explicit and do not introduce callbacks or hidden infinite schemas.
- [x] Current API/runtime/tests are inspected and the smallest Goal 2 delta is implementation-ready.
- [x] T14/T26 reuse and every affected ledger decision are re-audited; no completed stage is contradicted.
- [x] All oracle, portability, fail-closed, import, compile, repository-test, mode, Markdown, diff, scope, and hostile-review gates pass.
- [x] `0-plan.md`, `evidence-index.md`, `design-ledger.md`, and `architecture-audit.md` are synchronized.

## Stage Results

**COMPLETE.** The frozen 25-query source audit closes 67 canonical lines at `52 pre-Index / 15 actual-Index`; 41 matched-retained lines plus 31 governed continuations yield 72 retained lines at `6 native / 13 relation / 53 control`, with 11 exclusions, retained split closure `49 exact + 23 mapped`, and zero monolith-only or unresolved evidence. Its SHA is `28fa3d71612a3d3ae109f6e245c1155ea9d4e74967c6a3c32394e77778a6aee3`. The hash-bound official-note snapshot SHA is `ba1aff54973afd0cd42cb7afc41220dd11835a0cb5b3d8d9ce8f5e9fe3d1b866`, recording fetched-document SHA `f28a332211082048417abce950a75756a4bdae7c7d48f3f12ab87ffdab02328c`. The official-language semantics snapshot SHA is `89dc720f5f905d41821c4284457cf75d08de2cae66af501789f26746682c6589`; it binds `Partition` alignment/cyclic padding, negative positions, `_`/`Blank[]`, and `ReplaceAll` priority/nonmatch semantics under the declared product-pattern importer. The ten governed assets partition `1 native / 2 relation / 7 control`, close 20 monolith/split references, ten hashes, 1,112,143 bytes, and two assemblies/four files, and remain `10 hash-bound / 1 limited-transcribed / 0 pixel-replayed`; seven adjacency candidates are explicitly excluded. The asset SHA is `95fe4b6dbda261a9068d6c7a6b8aa1765bcb0ef19e444abebe47895569731c77`.

The semantic oracle closes 682 exhaustive binary periodic configurations/5,506 ordered reads, the repaired source Blank row at exactly two of sixteen contexts, and 65,536 independently typed complete-result commutations comprising 1,048,576 firings and 4,194,304 child witnesses. An explicit reversible source/successor-token bijection preserves outcomes, changed flags, successor cardinality, step presence, carriers, reads, writes, rectangles, local children, and lineage. Fifty-seven hostile rejections, one lower-right/upper-left divergence, one compatible crossed-width aligned mixed mosaic, and two typed incompatible/no-commit commutations close the adversaries. The semantic SHA is `1faca62a3261a4b328cb70d6daebd00b916788c63e4e4f77109754ccee8715ef`; its digest is `82b03edcc186e9ceccdffb33f1e90fb671a64e4dd008eec057a11f6339f44209`.

D133 classifies the finite aligned construction in categories 1–3: discrete `t+2D` periodic rectangular CONFIGURATION; T26 `AllOldTiles`; a declared lower-right `(NW,N,W,Self)` old-snapshot access with alias multiplicity; ordered closed `Literal | AnonymousAny` product rows with first-match and construction-time totality; T26 source-bound patches; and direct D132 `RankedBlockMosaicAssemble(rank=2)`. Compiled exhaustive behavior retains the ordered source AST/provenance because compilation alone is not injective. Context participants are not parents. Malformed/incomplete programs reject before execution, while state-dependent incompatibility yields no commit. The raster table, seed, trace, and palette map remain unrecovered, and `BOOK:13810` unequal subdivision remains an open adaptive carrier/incidence/matching/update profile rather than a false D132 claim. No state class, UPDATE, executor, family branch, callback, implicit host fallback, raster program, padding/reflection menu, hidden scan, or flat concatenation is added. All portability, fail-closed, silent-import, compile, repository-test, mode, Markdown, diff, scope, runtime-fit, and independent hostile-review gates pass; no prior stage reopens. Next: T32.
