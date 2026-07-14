# 38-T26-2D-SUBSTITUTION

Status: **COMPLETE — SOURCE, ASSET, SEMANTIC, ARCHITECTURE, AND HOSTILE-REVIEW GATES PASS**

## Current Facts

- T26 is CSV physical line 27, `Two-Dimensional Substitution Systems`; `ref/notes/CA-Types.md` section 26 is a vocabulary guide, not primary mechanics.
- The regenerated Q00-Q29 source protocol closes 94 unique query lines at `67 pre-Index / 27 actual-Index`. It retains 115 lines at `23 native / 67 relation / 25 control`, excludes 11 pre-Index false positives, and leaves zero unresolved candidates.
- The retained source consists of 56 direct query hits plus 59 governed continuations. All 115 lines reverse-join to the 17-file split corpus as `77 exact + 38 mapped variants`; none is monolith-only.
- The construction is a finite nonempty rectangular grid of finite tile labels in discrete `t+2D`. Every old tile fires exactly once from one immutable generation, reads only its own old label, and emits a nonempty rectangular patch from a total closed table. The uniform-patch profile is the core preset total on valid positive rectangular grids; `BOOK:13744` also gives a complete native mixed-patch table and seed.
- UPDATE is the Notes' exact `Flatten2D` product-order assembly. Generic `RankedBlockMosaicAssemble(rank=2)` accepts a step exactly when all emitted patches within each old source row have equal heights and all resulting row slabs have equal widths. Patch widths need not agree down old source columns. `RankedUniformBlockAssemble` is the common-positive-shape restriction, total only on valid positive rectangular grids. Both rank-two profiles preserve source/product order, consume the complete old generation, and defer every newborn tile until the next event.
- White is an ordinary label. The explicit non-white-background variant proves that a white tile may emit black descendants; there is no implicit white identity, blank-skip optimization, or ambient fill rule.
- T26 is not merely a rank-two parameter value of D019's linear `OrderedGenerationConcat`: naive flattened concatenation loses rank-two placement. Generic `RankedBlockMosaicAssemble` extends that UPDATE pattern by rank and compatibility. Its rank-one member is the D019 selected-source behavior: it accepts an ordered selected subset of old sources, concatenates only the selected outputs in source order, retains selected epsilon outputs, and consumes each unselected old source with a zero-width lineage region. Empty input and a nonempty input with no selected source both yield the empty successor. All-selected rank one is D019's full-coverage subset; the common-positive-shape restriction overlaps fixed-block T13/D019; rank two is T26 full-source mosaic assembly.
- The same state has a category-3 lossless representation inside T27's posed occurrence bag exactly on the aligned, uniform, hole-free, overlap-free rectangular-tiling image. Arbitrary free geometry remains T27.
- The `Other shapes` text supplies the complete encoded-label rule over operationally opaque labels `0..3`, seed `{{3}}`, and enough `Flatten2D` semantics to execute its compatible mixed patches natively; its square side lengths begin `1,2,3,5,8,13,21`. The extraction has one disclosed surplus-brace repair, and neither the source nor the oracle constructs a numeric-label-to-geometric-role assignment. Neighbor-dependent patch choice remains T28.
- The source-governed asset universe closes 26 unique JPEGs at `3 native / 16 relation / 7 control`, 52 exact monolith/split references, 26 unique hashes, and 1,838,481 bytes. The honest boundary is `26 HASH_BOUND / 0 TRANSCRIBED / 0 PIXEL_REPLAYED`.
- The semantic oracle closes the unique partition `6,667 native/generic + 6,658 full-StepResult posed-bag + 16,709 selected-rank-one = 30,034` commuting proofs. Rank one partitions as 1,519 all-selected cases, including 1,470 positive-input cases and 49 empty-input cases, plus 15,190 cases that consume at least one unselected source. The 98 singleton/no-selected extinctions, 1,390 selected-epsilon cases, 1,519 right-neighbor-frontier cases, and 600 common-positive fixed-block cases are crossing, non-additive subsets. It closes 81 hostile rejections, including two typed incompatible/no-commit outcomes.
- D132's corrected architecture result is rank-two compatible block-mosaic assembly with a lossless aligned posed-bag representation. Generic UPDATE-policy implementation is required, but no new execution algebra, T26 state or UPDATE class, executor, family branch, callback, padding scheme, hidden control, or raster-defined program follows.

## Final Semantic Conclusions

- RULE data is a total, canonical, finite, alphabet-closed, callback-free map `delta : TileLabel -> RectPatch(TileLabel)`. The core uniform profile declares one positive `(h,w)` shared by every row; the native mixed-patch profile allows label-dependent positive rectangular shapes and validates mosaic compatibility per old snapshot.
- CONFIGURATION is a finite nonempty rectangular label grid. Under uniform blocks the dimensions change from `(H,W)` to `(H*h,W*w)`; under a compatible mosaic the successor height is the sum of source-row patch heights and its width is the common assembled slab width. A fixed-capacity canvas is not state.
- FRONTIER is `AllOldTiles`, with opaque old-snapshot handles. Canonical row/column order supports deterministic assembly and lineage, but a tile's product address—not incidental flat enumeration—determines its descendants' placement.
- NEIGHBORHOOD is `SelfOnly`. Surrounding labels, coordinates, generation number, raster scale, finite-automaton digits, ancestry, and output geometry are not RULE inputs.
- RULE returns a typed source-bound patch write. UPDATE validates exact full coverage, provenance, and rank-two mosaic compatibility, consumes every old tile, and constructs one successor using product coordinates.
- A complete uniform table produces one deterministic successor on every valid positive rectangular grid. A mixed table produces one deterministic successor on compatible grids. An incompatible old snapshot returns exactly `PatchStepResult(Invalid(IncompatibleMosaic(...)), successors=(), step=None)` before commit: no successor is allocated, and the old configuration and opaque token remain unchanged. Missing rows and malformed/empty patches are invalid programs; they are not halts. A fixed point or a `1×1` identity row is still an applicable `Advanced(changed=false)` event.
- The source gives no numeric T26 rule codec. The structural table is program identity. For the uniform subfamily with alphabet size `k` and fixed patch shape `(h,w)`, the derived rule-family count is `k^(k*h*w)`.
- Display scale, raster colors, nestedness, fractal limits/dimensions, coordinate formulas, compression, constraints, and Walsh/Kronecker descriptions are observers, relations, or alternative generators. None may replace native stepping.
- T26 shares the branch-free SimpleProgram runner:

```text
active = AllOldTiles.select(configuration)
reads  = SelfOnly.read(configuration, active)
writes = ClosedPatchTable.apply(active, reads)
result = RankedBlockMosaicAssemble(rank=2).apply(configuration, active, writes)
```

`RankedUniformBlockAssemble(rank=2)` is the common-positive-shape preset of that same UPDATE policy; its totality claim is restricted to positive rectangular old supports and positive block extents.

## Big Picture Objective

Reconstruct two-dimensional substitution systems from primary Book evidence, distinguish compatible rank-two block mosaics from T27 geometry and T28 contextual choice, and identify the smallest faithful reuse of DOMAIN, CONFIGURATION, ALPHABET, FRONTIER, NEIGHBORHOOD, RULE result, UPDATE, trace, and representation machinery. Prove one native event at a time that T26 uses generic rank-two mosaic assembly, that its rank-one member coincides with D019's ordered selected-source concatenation including consumption and epsilon/empty cases, and that uniform grid snapshots and complete step results have a checked category-3 T27 representation, without inventing a family executor or using rasters as program data.

## Catalog Identity

- Stable ID: T26.
- Exact CSV name: Two-Dimensional Substitution Systems.
- CSV physical line: 27.
- Taxonomy section: 26.
- Entry kind: deterministic rank-two preset of generic compatible block-mosaic assembly under the shared SimpleProgram algebra; uniform blocks are the common-positive-shape restriction, total on valid positive rectangular grids.
- Canonical source vocabulary: two-dimensional/2D substitution system, square subdivision, fixed block, `SS2DEvolve`, `Flatten2D`, `SSEvolve`, `FlattenArray`, non-white background, digit sequence, finite automaton, Sierpinski/Menger, other shapes, shape/orientation colors, Penrose tiling, recursive subdivision/quadtree, nested patterns, Kronecker product, neighbor-dependent substitution, and sequential higher-dimensional scanning.
- Modern terms checked but absent as direct Book names include tile/block/array substitution systems, picture grammars, orientation policy, and scale-factor terminology.

## Search Log

`38-T26-source-oracle.py` is the reproducible search/adjudication record. Its 30 query families cover direct names and spelling variants, inherited fixed-block mechanics, Notes symbols and executable forms, non-white backgrounds, rank generalization, shape/orientation encoding, named examples, coordinate and algebraic relations, T27/T28/sequential controls, actual Index routes, and explicit modern-term absence.

Representative manual saturation commands were:

```bash
rg -n -i -e 'two-dimensional substitution' -e '2D substitution' \
  -e 'SS2DEvolve' -e 'Flatten2D' -e 'Non-white backgrounds' \
  ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
rg -n -i -e 'Other shapes' -e 'neighbor-dependent substitution' \
  -e 'digit sequences' -e 'Kronecker product' -e 'recursive subdivision' \
  ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
python3 goal-1/38-T26-source-oracle.py
```

Closure:

- Monolith identity: 22,498 physical lines; SHA-256 `55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20`.
- Query union: 94 = 67 pre-Index + 27 actual-Index.
- Retained: 115 = 23 native + 67 relation + 25 control.
- Directly matched retained lines: 56; governed continuations: 59.
- Excluded: 11, including one-dimensional systems merely represented in 2D, 1D contextual/L-system routes, generic heading collisions, and unrelated `Flatten2D` uses.
- Actual Index: all 27 dense physical lines have exact occurrence guards. The partition is 15 direct/grid/named/alias/representation routes, 2 geometric/contextual sibling routes, 2 one-dimensional alias controls, and 8 generic Penrose collisions.
- Split query reverse join: 92 records = 80 exact + 12 mapped variants.
- Split retained reverse join: 115 records = 77 exact + 38 mapped variants; 0 monolith-only.
- Atlas: 2 summary-only hits. Catalog and taxonomy text remain vocabulary controls only.
- Governed source-image interface: 26 lines, digest `9018acedd5ff638608aa2a79feb5059de5b8a671792ab0c8ec501437eea85ee7`.
- Source-oracle SHA-256: `124b2be2c5ac1121946f7fe952d83ca93403782998992ffcd5974d9c8339b5f2`.
- `unresolved_total=0`.

## Book Excerpts

### E01 — inherited all-parent, self-only block substitution

- Source: `BOOK:984-992`.
- Establishes: changing support, one fixed block per old label, neighbor independence, and all-source replacement each step.

> Substitution systems, however, are set up so that the number of elements can change. ... at each step each one of these elements is replaced by a new block of elements.
>
> the rules specify that each element of a particular color should be replaced by a fixed block of new elements, independent of the colors of any neighboring elements.
>
> at every step each kind of element is replaced by a fixed block of new elements.

### E02 — the two-dimensional construction reuses the same mechanism

- Source: `BOOK:2310-2316`.
- Establishes: T26 is the two-dimensional rank of ordinary subdivision, and the canonical rule replaces one square by four smaller squares.

> One-dimensional substitution systems ... can be thought of as working by progressively subdividing each element they contain into several smaller elements.
>
> One can construct two-dimensional substitution systems that work in essentially the same way ...
>
> A two-dimensional substitution system in which each square is replaced by four smaller squares at every step according to the rule shown on the left.

### E03 — snapshot generations create nested copies

- Source: `BOOK:2318-2324`.
- Establishes: every old square emits the same local descendants, and those newborns evolve only on subsequent steps.

> at every step the rules for the substitution system simply replace each black square with several smaller black squares. And on subsequent steps, each of these new black squares is then in turn replaced in exactly the same way ...

### E04 — exact text-owned rule, seed, and `Flatten2D` assembly

- Source: `BOOK:13683-13689`.
- Establishes: the page-187 binary table, seed `{{1}}`, repeated old-generation replacement, and exact row-wise patch assembly.

```text
{1 -> {{1,0},{1,1}}, 0 -> {{0,0},{0,0}}}
initial condition {{1}}

SS2DEvolve[rule_, init_, t_1 :=
 Nest[Flatten2D[# /. rule] &, init, t]
Flatten2D[list_] :=
 Apply[Join, Map[MapThread[Join, #] &, list]]
```

The malformed first function line is preserved exactly; the transition meaning is independently checked from the intact replacement and `Flatten2D` lines rather than silently repairing the source.

### E05 — non-white backgrounds are ordinary rule rows

- Source: `BOOK:13722-13724`.
- Establishes: white is not an implicit identity/background value; a white-label row may emit black labels.

> Non-white backgrounds. The pictures below substitution systems in which white squares are replaced by blocks which contain black squares.

### E06 — dimension is a rank parameter

- Source: `BOOK:13726-13738`.
- Establishes: nested-array depth represents dimension, and the same replacement-plus-flatten pattern generalizes by rank.

```text
SSEvolve[rule_, init_, t_, d_Integer] :=
  Nest[FlattenArray[# /. rule, d] &, init, t]
```

The 3D example and `d+1` non-hyperplane observation are relations supporting ranked assembly. They do not turn dimension into a family executor.

### E07 — geometric orientation and overlap are T27 controls

- Source: `BOOK:2326-2334`.
- Establishes: off-grid replacement requires orientation and may overlap; those facts are not implicit properties of strict aligned T26 patches.

> there is nothing about this basic process that depends on the squares being arranged in any kind of rigid grid.
>
> in applying the rule to a particular square, one must take account of the orientation of that square.
>
> if there is just a geometrical rule ... it is possible for the squares produced to overlap

### E08 — neighbor-dependent choice is a distinct T28 construction

- Source: `BOOK:2350-2356`, `BOOK:13806-13810`.
- Establishes: contextual rule choice adds neighbor reads; strict T26 does not read them.

> the replacement for a particular element at a given step can depend ... on the characteristics of other neighboring elements.
>
> if one sets up elements on a grid it is straightforward to allow the replacements for a given element to depend on its neighbors

```text
Flatten2D[Partition[list, {2, 2}, 1, -1] /. rule]
```

### E09 — higher-dimensional sequential scanning is not parallel T26

- Source: `BOOK:2358-2366`.
- Establishes: replacing every element and scanning one selected block are different schedules; a scan order is not hidden in T26.

> ordinary one-dimensional substitution systems, in which every element is replaced at each step, and sequential substitution systems, in which just a single block of elements are replaced at each step.
>
> as soon as one defines any particular order for elements ... this in effect reduces one to dealing with a one-dimensional system.

### E10 — coordinate finite automata are alternative evaluators

- Source: `BOOK:13692-13699`.
- Establishes: a digit-sequence finite automaton can determine a nested pattern's labels without becoming transition state or UPDATE.

> the color of a cell at position {i, j} in a 2D substitution system can be determined using a finite automaton from the digit sequences of the numbers i and j.

The local extraction says `IntegerDigits[{i, i}, ...]` while its enclosing loops use `i` and `j`; this route is retained as defective relation evidence, not repaired into a native evaluator.

### E11 — `Other shapes` gives a native opaque-label mixed-patch preset

- Source: `BOOK:13740-13744`.
- Establishes: after the exact one-brace extraction repair disclosed below, the encoded equal-square grid evolution is completely specified by a four-label mixed-patch rule, seed `{{3}}`, and the source's `Flatten2D`. Labels `0..3` are sufficient as operationally opaque values; no label-to-shape/orientation assignment is constructed.

> one can also set up substitution systems that are based on subdividing other geometrical figures
>
> Labelling each shape and orientation with a different color, the behavior of this system can be reproduced with equal-sized squares using the rule ...

The raw math span at `BOOK:13744` contains 11 escaped opening braces and 12 closing braces. The source oracle removes exactly the surplus final `\}` immediately before `\$`; this is a literal one-brace repair, not delimiter normalization. Four otherwise intact rule-row fragments plus the seed `{{3}}` disambiguate the repaired table:

```text
3 -> ((1,0),(3,2))
2 -> ((1,),(3,))
1 -> ((3,2),)
0 -> ((3,),)
seed = ((3,),)
```

The emitted patch shapes are `2×2`, `2×1`, `1×2`, and `1×1`. The source `Flatten2D` supplies their assembly law: within each old source row, patches must have the same height so corresponding local rows can be joined; the resulting row slabs must have equal widths so the successor remains rectangular. There is no requirement that patch widths agree down an old source column. The crossed-width witness with rule widths `0 -> 1`, `1 -> 2` and old grid `((0,1),(1,0))` produces two width-3 slabs and is valid even though both source columns see widths `{1,2}`. The source trajectory is compatible and has square side lengths `1,2,3,5,8,13,21` through six steps. The prose says colors label shapes and orientations but does not assign numeric labels to those roles; the oracle keeps `0..3` opaque and constructs no role codec.

### E12 — rule counts are structural, not raster codecs

- Source: `BOOK:14099-14109`.
- Establishes: the source's “4 billion or so” matches the derived four-color `2×2` family, and a 16-color relation uses only 51 possible local blocks.

> searching all 4 billion or so possible such systems with 2×2 blocks and up to four colors

For a complete `k`-label uniform `h×w` table the derived count is `k^(k*h*w)`: binary `2×2` gives 256, ternary `3×3` gives `3^27 = 7,625,597,484,987`, and four-color `2×2` gives `4^16 = 2^32 = 4,294,967,296`.

### E13 — Kronecker/Walsh generation is a relation

- Source: `BOOK:17297-17301`.
- Establishes: a nested array can have an algebraically equivalent generator; that formula is not hidden native state.

> It ... can be obtained ... from the evolution of a 2D substitution system, or equivalently from a Kronecker product

## Source-Extraction Defects and Repair Boundary

The source oracle guards defects literally so later work cannot mistake a silent cleanup for primary evidence:

| BOOK line | Preserved extraction | Disposition |
|---|---|---|
| `13686` | `SS2DEvolve[rule_, init_, t_1 :=` | Malformed signature; intact replacement/flatten body and independent evaluator establish semantics. |
| `13695-13696` | `IntegerDigits[{i, i}, ...]` with loops over `i` and `j` | Coordinate-evaluator relation only; no correction is promoted to native execution. |
| `13722` | “The pictures below substitution systems ...” | Missing verb retained; caption meaning is bounded by its heading and asset. |
| `13726` | `ddimensional` | OCR joining retained. |
| `13731-13733` | malformed `FlattenArray [list . d ]` typography | Rank relation retained; no literal runtime transcription. |
| `13738` | `d-1hyperplane` | OCR spacing retained. |
| `13744` | 11 escaped opening braces and 12 closing braces in the raw math span | Remove exactly the surplus final `\}` immediately before `\$`; four intact rule rows plus seed `{{3}}` disambiguate this single literal repair. No delimiter normalization or role assignment is inferred. |
| `13752` | massively repeated/corrupted Penrose expression | Relation only; never executable T26 data. |
| `14105` | malformed multi-kilobyte 16-color table row | Constraint relation only; no table recovery claimed. |
| `19197` | tuple/bracket transcription in a relation rule | Literal relation retained; no strict fixture derived from it. |

No raster, external formula, or guessed broad bracket normalization is used to fill these gaps. The sole native repair is the guarded `BOOK:13744` surplus brace just disclosed.

## Asset Closure

`38-T26-asset-oracle.py` depends fail-closed on the exact source-oracle evidence/image sets and binds every governed image to its unique file, monolith and split references, byte length, dimensions, SHA-256, evidence class, and assembly membership.

- 26 governed assets = 3 native + 16 relation + 7 control.
- Native: two strict square-grid plates (`BOOK:2314,2322`) and one non-white-background plate (`BOOK:13724`).
- Five indivisible assemblies contain 14 files: geometric orientation, geometric overlap, perception comparison, coordinate/finite-automaton, and Walsh/Kronecker.
- The remaining governed relations/controls cover recursive subdivision, nestedness perception, coordinate gallery, other shapes, Penrose, constraint-forced nesting, the geometric gallery, the T28 grid control, and a 3D geometric observer.
- Fixed-radius saturation closes 50 nearby candidates as 26 governed + 24 explicitly excluded. The inherited Chapter 3 one-dimensional substitution plates remain governed by T13 rather than being double-counted by T26.
- 52 exact Markdown references, 26 unique files, 26 unique hashes, 1,838,481 total bytes, and zero exact duplicates.
- Ledger digest: `6efdf22fdacd0bc9c9b5f59ef61e56c29cdbb9d76624dad5c088c8aed0e17beb`.
- Asset-oracle SHA-256: `e36e7ec66460c81cd5d78f0dbe39188c431961c135b7c76a87be68e369ffd438`.
- Honest boundary: `HASH_BOUND=26`, `TRANSCRIBED=0`, `PIXEL_REPLAYED=0`.

The exact page-187 rule/seed and the `Other shapes` opaque-label rule/seed come from `BOOK:13683` and the explicitly repaired `BOOK:13744` math span, not pixels. Page-188 displayed rules, all displayed intermediate arrays, panel seeds/traces, palettes, glyph meanings, and renderers remain unrecovered. A hash-bound raster cannot become an executable rule or conformance trace.

## Construction Model

Let `Sigma = {0,...,k-1}`, with `k >= 2`. A program contains a complete table

```text
delta : Sigma -> NonemptyRectPatch(Sigma)
```

whose outputs are rectangular and alphabet-closed. The uniform core additionally chooses one positive patch shape `(p_h,p_w)` and requires every `delta(a)` to have that shape. A configuration is

```text
RectGrid = {
    alphabet: Sigma,
    cells: Sigma^(H x W),
    snapshot_token
}

invariants: H > 0, W > 0, rectangular, alphabet-closed
```

Every event first computes exactly one old-snapshot write per source tile:

```text
active = (TileHandle(snapshot,r,c) for r=0..H-1 for c=0..W-1)
read[r,c] = cells[r,c]
write[r,c] = delta[read[r,c]]
```

`RankedBlockMosaicAssemble(rank=2)` then requires:

```text
for each source row r:
    all height(write[r,c]) are equal; call that row_height[r]
    slab[r] = join corresponding local rows of write[r,0],...,write[r,W-1]

all width(slab[r]) are equal
next = vertical_join(slab[0],...,slab[H-1])
```

This is the complete rank-two compatibility law. It does **not** require widths of patches in the same old source column to agree. For the crossed witness

```text
width(delta(0)) = 1
width(delta(1)) = 2
old = ((0,1),
       (1,0))
```

both old rows assemble to width 3, so the step succeeds, although each old source column contains patch widths `{1,2}`.

Equivalently, child `(i,j)` of source `(r,c)` is placed at

```text
target_row = sum(row_height[r0] for r0 < r) + i
target_col = sum(width(write[r,c0]) for c0 < c) + j
```

only after compatibility and exact old-source coverage are validated. If a source row mixes patch heights, or assembled row slabs have unequal widths, UPDATE returns

```text
PatchStepResult(
    outcome=Invalid(IncompatibleMosaic(...)),
    successors=(),
    step=None,
)
```

before allocation or commit. The old configuration and its opaque snapshot token remain unchanged. UPDATE never pads, crops, guesses a collision rule, or emits a ragged configuration. Every compatible target address has exactly one parent/local-coordinate pair, so assembly has neither a collision policy nor an overlap policy.

`RankedUniformBlockAssemble(rank=2)` is the restriction where every write has the same positive `(p_h,p_w)`. It is compatible for every positive rectangular old grid and reduces the offsets to

```text
next[r*p_h+i, c*p_w+j] = write[r,c][i,j]
next.shape = (H*p_h,W*p_w)
```

Each successful event returns exact lineage rectangles:

```text
parent (r,c) -> rows [row_offset[r], row_offset[r] + height(write[r,c]))
                cols [col_offset[r,c], col_offset[r,c] + width(write[r,c]))
```

Its `PatchStep` also enumerates every child occurrence with the exact source handle, parent-local row/column, successor target row/column, and label. Rectangle coverage is exactly once per old source, child coverage is exactly once per expected local slot, and the lineage children exactly cover the committed successor. Lineage is event/witness data: RULE cannot read it, and semantic grid equality does not depend on occurrence IDs.

The page-187 text fixture is:

```text
0 -> ((0,0),(0,0))
1 -> ((1,0),(1,1))
t0 = ((1,),)
t1 = ((1,0),
      (1,1))
t2 = ((1,0,0,0),
      (1,1,0,0),
      (1,0,1,0),
      (1,1,1,1))
```

`t1` and `t2` are independently assembled from immutable old generations. They are not transcribed from a figure.

Applying the text-owned, single-brace-repaired `BOOK:13744` mixed table from seed `((3,),)` gives compatible square shapes `1,2,3,5,8,13,21`. This is native opaque-label evolution. The source does not assign labels `0..3` to the pictured square/GoldenRatio-rectangle roles, and the oracle constructs no such role codec.

### State, outcomes, and boundaries

| Axis | Strict T26 semantics |
|---|---|
| DOMAIN | Discrete `t+2D`. Time is event order; the spatial configuration is a finite rectangular product support. |
| CONFIGURATION | Complete finite `H x W` grid of tile labels with an opaque snapshot identity. Shape may change each event. |
| ALPHABET | Finite ordered tile labels. The `BOOK:13744` labels `0..3` are operationally opaque; no shape/orientation role codec is part of this construction. |
| SEED | Any valid finite nonempty rectangular grid; canonical source seeds include page-187 `{{1}}` and mixed-patch `{{3}}`. |
| FRONTIER | Every old tile exactly once, using snapshot-scoped handles. |
| NEIGHBORHOOD | Self label only. No boundary read is required. |
| RULE | Total closed label-to-nonempty-rectangular-patch table. The core preset adds a table-wide uniform-shape invariant. |
| RESULT | One typed source-bound ranked block write per old tile. |
| UPDATE | Exact `RankedBlockMosaicAssemble(rank=2)`/`Flatten2D` assembly with within-source-row equal heights and across-source-row equal slab widths, but no per-source-column width invariant; old-snapshot full coverage, parent consumption, and newborn deferral. Uniform assembly is its common-positive-shape restriction, total on positive rectangular inputs. |
| SUCCESSOR | Exactly one valid grid for a compatible `Advanced` step. A fixed point remains `Advanced(changed=false)`. Incompatibility returns exact `PatchStepResult(Invalid(IncompatibleMosaic(...)), successors=(), step=None)` before commit. |
| HALTING | No intrinsic halt for a compatible valid step; horizon/cancel/resource/invalidity remain external or typed outcomes. |
| TRACE | Ragged rectangular snapshots plus exact parent rectangles and per-child source/local/target/label lineage for each successful event; padding and raster coordinates are downstream representations. |

## One-Step Reuse Proofs

### Ranked block-mosaic UPDATE and its D019 overlap

D019's `OrderedGenerationConcat` is a linear UPDATE policy over an explicit ordered selection of old source indices. A selected source emits its possibly empty output word; an unselected source is consumed rather than copied and receives an exact zero-width lineage region at the current output cursor. Selected-source order and child order are preserved. Empty input produces the empty successor, and a nonempty input with no selected sources also produces the empty successor. The all-selected specialization is D019's full-coverage subset and concatenates every source word.

T26 does not turn that combiner into rank two by changing one integer. It requires generic `RankedBlockMosaicAssemble` on the existing UPDATE axis. At rank one, mosaic assembly has no cross-row constraint, accepts the ordered selected-source locus map, admits variable and zero-length selected outputs, records every selected and unselected source, and exactly matches the D019 contract above. T26's rank-two profile separately selects every old tile and requires positive rectangular blocks. D019 keeps its existing policy and behavior; this shared rank-one semantics does not require replacing its named combiner.

The named uniform restriction `RankedUniformBlockAssemble` requires positive old extents `S=(s_0,...,s_(d-1))`, a common positive block shape `B=(b_0,...,b_(d-1))`, and one block per old product address. It places local coordinate `u` from source coordinate `x` at

```text
target_axis[a] = x[a] * B[a] + u[a]
```

and produces shape `S*B` componentwise.

- At rank one with common positive `B=(q)` and positive old extent, it is the fixed-block restriction/commuting overlap of T13/D019, with parent/child order preserved.
- It does not cover D019's empty input, nonempty/no-selected extinction, selected epsilon output, or other zero-length rank-one cases; those remain in generic `RankedBlockMosaicAssemble`/`OrderedGenerationConcat`.
- At rank one with an explicit ordered selected subset and label-dependent block lengths, including zero, `RankedBlockMosaicAssemble` coincides with general D019 `OrderedGenerationConcat`.
- At rank two with common positive `B=(p_h,p_w)`, uniform assembly is the compatible core T26 `Flatten2D` preset for every positive rectangular grid.
- At rank two with label-dependent positive rectangular blocks, mosaic assembly applies equal heights within each old source row and equal total slab widths across old source rows. It imposes no per-source-column width equality. `BOOK:13744` supplies a native compatible trajectory.

The semantic oracle exhausts 16,709 selected-rank-one commutations over input lengths 0 through 4, every ordered subset, and binary output words of lengths 0 through 2. The disjoint top-level partition is 1,519 all-selected cases plus 15,190 cases consuming at least one unselected source. The all-selected group contains 1,470 positive-input cases and 49 empty-input cases. Singleton/no-selected extinction (98), selected epsilon (1,390), right-neighbor frontier (1,519), and common-positive fixed block (600) are crossing, non-additive subsets and must not be summed into the total.

A nonsymmetric two-source `2×2` adversary proves that flattening every patch and concatenating the flat streams gives the wrong grid: one parent's second local row is placed before the adjacent parent's first local row. The crossed-width `((0,1),(1,0))` witness separately proves that both width-3 row slabs are compatible even though each source column sees patch widths `{1,2}`. Rank-two placement therefore requires product-aware mosaic assembly without an invented per-column width invariant. This is a justified generic policy on the shared UPDATE axis, not a new execution algebra, family executor, or T26-named class.

### Category-3 addressed posed-bag representation

For grid shape `(H,W)`, declare a bijection `prototype : TileLabel <-> PrototypeID`. Every prototype has the same declared unit-square geometry, but prototype identity remains distinct because T27 rules are keyed by prototype. Encode tile `(r,c)` with label `X[r,c]` as the T27 carrier pair `(prototype(X[r,c]), pose[r,c])`, where

```text
linear      = diag(1/W, 1/H)
translation = (c/W, r/H)
```

A uniform-patch T27 rule is keyed by the parent prototype ID. It decodes that ID to the T26 label, selects the closed patch row, and emits child `(prototype(delta(label)[i,j]), local_pose[i,j])`, where

```text
local.linear      = diag(1/p_w, 1/p_h)
local.translation = (j/p_w, i/p_h)
```

and world pose `parent_pose o local_pose`. Decoding is defined only when:

1. every occurrence has one identical positive axis-aligned diagonal scale;
2. scale components are reciprocals of positive integers;
3. translations are exact integer multiples of those scales inside the unit rectangle;
4. exactly one occurrence exists at every rectangular address;
5. there are no holes, overlaps, duplicate multiplicities, rotations, or skews.

Decoding applies the inverse prototype-label bijection and the exact address recovered from the pose. On that invariant-valid image, encode and decode are explicit inverses. For the uniform-patch restriction, parent-local pose composition additionally gives the one-event commuting square

```text
encode(step_T26(grid)) = step_T27_bag(encode(grid))
```

for one event. The representation encoding maps and shares the source token. Grid UPDATE and bag UPDATE then mint their successor tokens independently; raw successor-token identity is neither expected nor used. An explicit reversible bijection between the two source/successor token pairs is applied consistently to the successor carrier and every typed lineage handle before equality is checked.

The comparison covers the complete result envelope, not merely successor labels: exact `Advanced.changed` (including the proved identity `changed=false` case), successor cardinality, step presence, successor carrier, grid child rectangles, every grid parent-local child occurrence and target, every bag parent patch, every local pose/prototype witness, and the condition that lineage children equal the successor occurrence bag exactly. The two typed incompatible controls separately prove the `Invalid` envelope has zero successors and no step.

The oracle proves 6,658 unique full-`StepResult` commutations—6,656 exhaustive binary `2×2` events, one rectangular `2×3` witness, and one identity event. The two canonical page-187 bag events overlap the exhaustive set and are reported as non-additive fixture coverage. The proof uses distinct prototype IDs, independent successor tokens plus the explicit token bijection, exact snapshot provenance, complete typed lineage, bag-enumeration invariance, and rejection of bags outside the inverse image rather than coercion into T26.

The mixed-patch native preset is still losslessly encodable snapshot by snapshot through distinct prototype IDs, but its global equal-square mosaic reflow is not claimed to commute with the same parent-local T27 pose update. Such a claim requires a separately proved T27 representation; it does not license inventing a geometric role codec for opaque labels `0..3`.

## Semantic and Conformance Closure

`38-T26-semantic-oracle.py` closes the uniform core, native mixed-patch preset, selected-rank-one/D019 relation, corrected prototype-keyed T27 representation, exact result envelopes, opaque provenance, complete lineage, and hostile boundaries:

- Unique native/generic events: 6,667 = 6,656 exhaustive binary `2×2` + 2 page-187 non-overlap + 1 rectangular `2×3` + 1 compatible crossed-column-width witness + 6 `Other shapes` mosaic + 1 identity `StepResult`.
- Exhaustive uniform space: all 256 binary `2×2` tables across all 26 labeled grids of shapes `1×1`, `1×2`, `2×1`, and `2×2`; 20,992 old-tile firings.
- Named overlap coverage is non-additive: 2 page-187 native events and 2 page-187 bag events overlap the exhaustive binary set, as do 1 non-white-background event and 2 newborn-deferral events. They are checked as named fixtures but are not added again.
- Unique proof partition: `6,667 native/generic + 6,658 full-StepResult posed-bag + 16,709 selected-rank-one = 30,034` commuting proofs.
- Rank-one relation: 16,709 selected-source mosaic/D019 commutations partition exactly as 1,519 all-selected plus 15,190 consuming at least one unselected source. Within/crossing that partition are 1,470 positive all-selected, 49 empty-input, 98 singleton/no-selected extinction, 1,390 selected-epsilon, 1,519 right-neighbor-frontier, and 600 common-positive fixed-block cases; these nested/crossing counters are non-additive.
- T27 relation: 6,658 unique full-`StepResult` commutations with carrier `(prototype_id, pose)`, one declared unit-square prototype per label, a shared/mapped source token, independently minted grid and bag successor tokens, an explicit reversible two-token bijection, exact outcome/changed/successor-count/step/carrier comparison, complete rectangle and per-child lineage, inverse-image validation, and bag-permutation invariance.
- Native mixed-patch fixture: six compatible events from `{{3}}`, producing side lengths `1,2,3,5,8,13,21`; `BOOK:13744` uses the exact disclosed surplus-brace repair, labels `0..3` remain opaque, and no geometric role codec is constructed.
- Compatibility controls: unequal patch heights within an old source row and unequal total slab widths across old source rows are rejected; the crossed-width case succeeds and proves no per-source-column width invariant exists.
- Rule-count checks: 256, `3^27`, and `2^32`; no source numeric codec exists.
- Hostile rejections: 81, covering invalid alphabets/grids/tables/blocks, callbacks and raster bytes, incompatible row heights or slab widths, stale/foreign/forged provenance and lineage, missing/reordered writes, selected-index/rank/naive-flatten errors, malformed prototype catalogs/token bijections/poses/bags, invalid observer parameters, and prohibited semantic shortcuts. Exactly two are typed incompatible-mosaic controls returning `Invalid` with zero successors, no step, and no commit.
- Semantic digest: `e380704a0626ad7a578e0937007cfa6ea8cc0dd6cee1b8c2d24a7eab18b7c57c`.
- Semantic-oracle SHA-256: `10395a02c1bd44514e610c98e1efc861513541a0b8b7046fedd557629e43a0f4`.

The `2x3` table is deliberately an architecture witness for general rectangular ranked assembly, not a claim that a displayed Book raster supplied that rule.

## Strict Boundary and Variant Disposition

| Candidate | Disposition |
|---|---|
| Page-187 binary `2×2` and page-188 ternary `3×3` square-grid systems | Native uniform T26 presets. |
| Non-white backgrounds | Native table/seed variant; label 0 is ordinary. |
| Any closed uniform positive rectangular patch shape | Native common-positive-shape restriction of generic `RankedBlockMosaicAssemble`, total on valid positive rectangular grids; source canonical fixtures remain square. |
| Higher-dimensional `SSEvolve`/`FlattenArray` | Ranked relation/generalization, not a T26 executor mode. |
| `BOOK:13744` opaque-label rule `0..3` from seed `{{3}}` | Native mixed-patch T26 preset under source `Flatten2D`, after the exact disclosed one-brace repair; compatible side lengths `1,2,3,5,8,13,21`. |
| Shape/orientation interpretation of labels `0..3` | Unspecified relation only. The source gives no numeric role assignment, and this stage constructs no role codec. |
| Other mixed-patch table/grid pair | Native only for a step satisfying within-source-row height equality and across-source-row total slab-width equality; no per-column width constraint exists. Otherwise return exact `PatchStepResult(Invalid(IncompatibleMosaic(...)), successors=(), step=None)` before commit. |
| Off-grid oriented squares, overlap, Penrose geometry | T27 free-geometric construction or relation; not strict grid UPDATE. |
| Neighbor-dependent patch choice / `Partition[...,{2,2},1,-1]` | T28; changes NEIGHBORHOOD and rule key. |
| Higher-dimensional sequential scanning | Different frontier/schedule; not hidden T26 order. |
| Adaptive recursive subdivision/quadtree | Relation; some sources remain unchanged while others subdivide, outside strict full uniform replacement. |
| Coordinate finite automata and digit formulas | Alternative evaluators/observers; no transition control. |
| Sierpinski formulas, Walsh/Kronecker product | Lossless or extensional generation relations where proved; not native program identity. |
| Constraint-forced nesting | T32-style relation; constraints do not become T26 UPDATE. |
| Fractal dimension, limit set, perception, compression, raster, 3D stack | Observers or applications. |

## Current API Fit

The governing architecture supersedes the CA-limited title and fixed-lattice assumptions of the legacy root document. `src/ca` remains the Phase-1 namespace for the broader SimplePrograms substrate.

| Axis | Root `simple_programs.md` evidence | Fit |
|---|---|---|
| DOMAIN | `:115-167` directly names `t+2D`. | `DIRECT` for dimensional role. |
| CONFIGURATION/SHAPE | `:87-113,169-198` uses one persistent fixed finite tensor shape. | `PRINCIPLED EXTENSION` to generic per-generation rectangular configuration; shared changing-support semantics, not a new T26 state class. |
| ALPHABET | `:200-215` permits finite/symbolic values. | `DIRECT` for finite opaque tile labels. No `OTHER_SHAPES` role codec is evidenced or required. |
| SEED | `:235-291` separates initialization from rules. | `PARAMETERIZATION` by a valid rectangular tile grid. |
| FRONTIER | `:396-454` provides shared selectors; `:1412-1510` currently frames frontier as writable next coordinates. | Selector responsibility is reusable, but old occurrence handles/full-source coverage need a generic `PRINCIPLED EXTENSION`. |
| NEIGHBORHOOD | `:360-394` separates reads from frontier; `:1303-1328` gives current-self-only access. | `DIRECT`. |
| RULE | `:1767-1791` returns one scalar next-site value. | `PRINCIPLED EXTENSION` to closed nonempty rectangular-block data/results, with uniform shape as a validated restriction; no callback. |
| UPDATE | The root schema lists no explicit UPDATE axis and hardwires fixed-shape scalar copy/write at `:22-38,1767-1791`. | Generic `RankedBlockMosaicAssemble` is the smallest `PRINCIPLED EXTENSION` on the existing UPDATE axis. Rank one is D019 selected-source concatenation; rank two plus compatibility is T26. `RankedUniformBlockAssemble` is the positive-old-shape/common-positive-block restriction, not a fresh algebra and not the carrier for D019 empty/no-selected/epsilon cases. |
| TRACE | `:87-113,2124-2199` stores a rectangular persistent tensor. | `PRINCIPLED EXTENSION` to ragged structured snapshots plus lineage; padding stays downstream. |
| BOUNDARY | `:292-359,697-703` governs out-of-support reads. | `NOT APPLICABLE` to strict self-only finite-grid reads. |

## Current Runtime Fit

The Phase-1 runtime contains useful components but does not yet implement the generic ranked structural UPDATE path:

| Runtime evidence | Fit and required preservation |
|---|---|
| `src/ca/alphabets.py:40-56` finite deterministic scalar values | `DIRECT` for ordinary tile labels. A T26-named alphabet is unnecessary. |
| `src/ca/loci.py:31-94` finite rank-0..3 coordinate spaces/selectors | `PARAMETERIZATION` for rank-two addresses and selector responsibility; `SEMANTIC MISMATCH` if a fixed tensor extent is treated as the changing configuration. |
| `src/ca/frontiers.py:37-80` full `time_slice` | `PARAMETERIZATION` of all-site responsibility, but old-tile snapshot handles and structural-source semantics are absent. |
| `src/ca/neighborhoods.py:46-60,110-137` structured neighborhoods and `self_at` | `DIRECT` self projection after it is generalized from dense coordinate reads to typed old-tile handles. |
| `src/ca/rules.py:64-78,262-328` family/callable/scalar lookup rules | `SEMANTIC MISMATCH` for native identity and result shape. Add closed nonempty-rectangular patch-table data and ranked writes; do not use `formulaic(fn)` as a semantic escape hatch. |
| `src/ca/specs.py:23-80,117-198` fixed `Dynamics.shape` and named family resolution | `SEMANTIC MISMATCH` for dynamic shape and branch-free composition. Generalize axes rather than add a T26 family case. |
| `src/ca/rollout.py:145-212` family dispatch | Current implementation debt. A new T26 branch is prohibited. |
| `src/ca/rollout.py:576-682` fixed-shape NumPy trajectories and scalar spatial lookup | Old-snapshot orchestration is reusable; fixed shape, binary scalar output, and dense rectangular stacking cannot represent ranked replacement or ragged traces. |
| `tests/test_loci.py:9-72`, `tests/test_neighborhoods.py:15-39`, `tests/test_rollout.py:312-376`, `tests/test_specs.py:9-36` | Existing tests protect coordinate order, selectors, old-state reads, and fixed 2D CA behavior. No current test covers dynamic rectangles, patch tables, full old-tile provenance, `Flatten2D`, newborn deferral, or ragged structural traces. |

The generic Goal 2 gaps are therefore: rectangular dynamic configuration, opaque old-tile handles, self projection over those handles, closed rectangular-patch table data, ranked block writes, mosaic compatibility/assembly, exact `Flatten2D` lineage, and ragged structured traces. They are not evidence for `TwoDimensionalSubstitutionState`, a T26 engine, or another rollout function.

## First-Principles Architecture Audit

D132 uses only the audit's categories 2 and 3:

| Component/decision | Class | Smallest reusable base | Invariant or mapping | Reopen? |
|---|---:|---|---|---|
| Discrete `t+2D` | 2 | Existing DOMAIN axis | Rank is task/program space, not value magnitude or family identity. | No. |
| Rectangular tile configuration | 2 | Existing ranked DOMAIN/CONFIGURATION axes | Positive finite extents; complete alphabet-closed grid. | No. |
| Finite labels | 1/2 | Existing finite ALPHABET | Deterministic order; `BOOK:13744` labels `0..3` remain operationally opaque. | No. |
| `AllOldTiles` | 2 | T13 `AllOccurrences` frontier | Every and only old tile once; opaque exact-snapshot provenance. | No. |
| `SelfOnly` | 1 | Existing self projection | Only the selected old label is RULE-visible. | No. |
| Closed rectangular patch table | 2 | D020 closed morphism data plus generic ranked result | Total canonical rows; positive rectangular outputs; alphabet closure; optional uniform-shape restriction. | No. |
| Ranked patch write | 2 | Existing typed result axis plus D019 ordered-emission precedent | Source-bound block plus product-local order and exact provenance. | No. |
| `RankedBlockMosaicAssemble` UPDATE | 2 plus shared-axis implementation gap | Existing UPDATE axis; rank-one D019 semantics are the commuting base | Rank one: explicit ordered selection, selected epsilon retained, unselected sources consumed with zero-width lineage, empty/no-selected cases preserved. Rank two: equal heights within source rows, equal slab widths across source rows, no per-column width invariant, full old coverage, product-order assembly, parent consumption, newborn deferral. | Goal 2 adds a generic policy, not a new algebra or T26 class. |
| `RankedUniformBlockAssemble` | 2 | Restriction of ranked mosaic assembly | Positive old extents and one common positive block shape; total on positive rectangular grids; fixed-block D019 overlap at rank one. It excludes empty/no-selected/zero-length D019 cases. | No separate executor. |
| Dense grid to posed bag | 3 | D041-D043 `(prototype_id, pose)` occurrence bag | Label/prototype bijection; shared declared unit-square geometry; inverse on aligned/no-hole/no-overlap image. Uniform-patch full `StepResult`s commute after independently minted successor tokens are compared through an explicit reversible token bijection; complete lineage is preserved. Mixed mosaic is only snapshot-encoded absent a further proof. | No; T27 remains broader. |
| `BOOK:13744` mixed-size opaque-label table | 2 | Ranked mosaic assembly plus text-owned `Flatten2D` | Complete `0..3` table after one guarded surplus-brace repair, seed `{{3}}`, compatible reachable trajectory; no numeric role assignment or role codec. | Native T26 preset; geometric interpretation remains unclaimed. |
| Contextual patch choice | Separate T28 parameterization | T14-style contextual read plus T26 result shape | Neighbor reads and boundary must be explicit. | T28 remains pending. |

No class-4 execution algebra is justified. D019's existing selected-source, variable/epsilon-length linear policy is preserved; its behavior is the rank-one member of mosaic assembly. D041-D043 remain unrestricted geometry, and Goal 2 implements the missing generic UPDATE policy without reopening T13 semantics.

## Principles Audit

- The user's correction governs: Wolfram's simple programs are the abstraction; cellular automata are one preset. `src/ca` is the current SimplePrograms substrate, not a boundary that forces T26 outside it.
- Semantic role and representation are separated. A tile grid and an aligned prototype-keyed posed bag are complete snapshot representations with an explicit inverse. The one-event T27 parent-local commuting square is proved only for the uniform-patch restriction, over the complete result envelope and lineage after explicit opaque-token renaming.
- `OrderedGenerationConcat` remains D019's selected-source linear implementation. Generic mosaic assembly agrees with it at rank one, including consumption of unselected sources, selected epsilon, and empty/no-selected cases, while rank two adds explicit compatibility and product placement. Neither policy is copied under a T26 name.
- Complete state contains every tile label and product address needed to advance. Lineage, renderer scale, and coordinate analyzers are downstream.
- RULE data is closed and inspectable. No host callback, raster decoder, formula bypass, family dispatch, or hidden interpreter is admitted.
- The common-positive-shape invariant is the evidence-bearing core total on valid positive rectangular grids; it does not subsume D019's empty/no-selected/zero-length rank-one cases. Mixed-size compatibility is also source-backed through `Flatten2D`, but is validated exactly without a per-source-column width condition; overlap, collision, orientation, numeric role assignment, and neighbor choice are not fabricated.
- A fixed padded canvas, giant sparse background, or same-shape NumPy trajectory would alter the support semantics. It is not a valid implementation shortcut.

## Goal 2 Implementation Stage

### G2-T26 — ranked block-mosaic replacement and aligned-grid representation

Objective: implement generic rank-two compatible block-mosaic assembly in the shared branch-free SimpleProgram runner, expose uniform assembly as its positive-old-shape/common-positive-block restriction, preserve D019's existing selected-source rank-one behavior, and implement the checked prototype-keyed T27 snapshot/result representation without overclaiming mixed-patch pose commutation.

Dependencies:

- D018/D019/D020 and T13: ordered selected-source loci, consumption of unselected sources, selected epsilon and empty/no-selected outcomes, closed morphism data, ordered child assembly, newborn deferral, opaque snapshot provenance, lineage, and ragged traces.
- D041-D043 and T27: exact posed occurrences, parent-local composition, multiplicity-preserving bag semantics, and the aligned-grid restriction map.
- Generic typed `StepResult`, configuration, selector, rule-result, UPDATE, serialization, and trace axes from the architecture audit.

Implementation work, in shared-axis terms:

1. Add a generic finite ranked rectangular configuration with positive extents, closed labels, immutable values, and opaque snapshot identity. Successor shape belongs to the successor configuration, not a fixed `Dynamics.shape`.
2. Add snapshot-scoped ranked occurrence handles and an `AllOccurrences`/`AllOldTiles` selector preset that proves exact old coverage.
3. Reuse the generic self projection for a typed `TileRead(source,label)`.
4. Add closed finite `Label -> RankedBlock` table data with canonical complete keys, declared rank, positive rectangular per-row extents, and alphabet closure. Add a uniform-shape table invariant as a restriction; do not require an integer rule ID.
5. Add a generic source-bound ranked-block result whose rank-one profile preserves D019/T15 ordered selection and variable/zero-length capability and whose T26 rank-two profile validates positive rectangular blocks. Selected sources may emit epsilon; unselected old sources are consumed with typed zero-width lineage. Do not let the T26 restriction narrow existing linear result semantics.
6. Add generic `RankedBlockMosaicAssemble` on the UPDATE axis. At rank one accept explicit ordered selected-source indices and preserve empty input and nonempty/no-selected extinction. At rank two require every old tile, validate equal patch heights within each old source row and equal assembled slab widths across source rows before committing, and impose no patch-width equality down source columns. Rank-one behavior must equal D019 `OrderedGenerationConcat`, while D019 keeps its existing implementation.
7. Add `RankedUniformBlockAssemble` only as the positive-old-shape/common-positive-block restriction using `target[a]=source[a]*block_shape[a]+local[a]`. It must not claim D019 empty/no-selected/zero-length cases. Preserve the common-positive fixed-block rank-one subset byte-for-byte and expose rank two through policy data, not family dispatch.
8. Return exact child hyperrectangles, every parent-local child occurrence, product-local and successor target coordinates, source handles, labels, and snapshot/run/branch provenance as typed lineage events, while keeping them out of RULE reads. On `Invalid(IncompatibleMosaic)`, return zero successors and no step before allocation or commit.
9. Extend trace storage to ragged structured configurations. Any padded tensor export must carry an explicit mask/shape and remain a downstream lossy-or-scoped representation.
10. Add encode/decode adapters between rectangular grids and T27 `(prototype_id, pose)` bags: map each label bijectively to its own prototype ID, declare unit-square geometry for every prototype, use exact rational poses, and enforce all image invariants. Reject holes, overlaps, duplicates, rotations, skews, off-grid translations, unknown prototypes, and nonbijective codecs. The encoding maps/shares the source token; grid and bag UPDATE mint their successor tokens independently, and an explicit reversible mapping between the source/successor token pairs must cover the successor carrier and every lineage handle. Prove equality of the complete `StepResult` envelope and lineage, and prove parent-local step commutation only for uniform blocks unless a separate mixed-mosaic proof is supplied.
11. Expose optional named T26 presets that assemble these existing axes. They must not introduce a T26 state class, UPDATE class, executor, or rollout branch.

Expected shared runtime homes include generic configuration/update/result modules plus extensions to `alphabets.py`, `loci.py`, `frontiers.py`, `neighborhoods.py`, `rules.py`, `specs.py`, and the branch-free rollout path. Exact file decomposition belongs to the Goal 2 architecture synthesis; catalog identity must never choose execution code.

Required conformance:

- Exact page-187 `t0 -> t1 -> t2` fixture from text-owned rule/seed data.
- Exact `BOOK:13744` mixed-patch table after removing only the guarded surplus final `\}` immediately before `\$`, from seed `{{3}}`, producing square side lengths `1,2,3,5,8,13,21` with exact lineage and operationally opaque labels `0..3`; no `OTHER_SHAPES` role codec.
- All 6,656 exhaustive binary `2×2` table/grid events and 20,992 old-tile firings, plus the complete 6,667 unique native/generic partition. Keep the overlapping named fixtures non-additive: page native 2, page bag 2, non-white background 1, newborn deferral 2.
- The rectangular `2×3` architecture witness, wrong-flat-concatenation counterexample, and crossed-column-width success witness.
- All 16,709 selected-rank-one/D019 commutations, partitioned as 1,519 all-selected plus 15,190 with an unselected source; the nested/crossing 1,470 positive all-selected, 49 empty-input, 98 singleton/no-selected, 1,390 selected-epsilon, 1,519 right-neighbor-frontier, and 600 common-positive fixed-block counters remain non-additive.
- Exact D019 equivalence for ordered selected sources, consumption of every unselected source with zero-width lineage, selected epsilon, empty input, and nonempty/no-selected extinction. The named uniform wrapper covers only positive old extents and a common positive block shape.
- Hostile rejection of unequal patch heights within one source row and unequal total slab widths across source rows, with no invented per-source-column width invariant.
- Both typed incompatible cases return exact `PatchStepResult(Invalid(IncompatibleMosaic(...)), successors=(), step=None)` before allocation/commit and preserve the old configuration/token.
- All 6,658 unique prototype-keyed full-`StepResult` posed-bag commutations and inverse-image rejections, with distinct prototype IDs, the mapped/shared source token, independently minted successor tokens, an explicit reversible source/successor token bijection, exact result outcome/changed/successor-count/step/carrier coverage, every rectangle and local child/target/prototype/pose witness, and lineage children exactly equal to the successor.
- Non-white-background, context-independence, newborn-deferral, renderer-noninterference, and bag-permutation tests.
- All 81 hostile validation cases, including the 2 typed incompatible/no-commit outcomes, selected-index, mosaic, prototype, token-bijection, full-provenance, and typed-lineage cases.
- Static absence of T26 family dispatch, callback execution, raster rule ingestion, fixed-capacity padding, implicit white identity, and unchecked mixed-size assembly.

T28 will compose contextual reads and its own boundary evidence with the ranked patch result. G2-T26 must not preempt it with a neighbor-aware flag.

## No-Cheating Checks

- No `TwoDimensionalSubstitutionState`, `T26Update`, T26 executor, family-name rollout branch, or alternate runner.
- No whole grid packed into one scalar/value and no arbitrary CA compilation used as native execution.
- No plain row-major flattening of patches; product coordinates must reproduce exact `Flatten2D`.
- No in-place firing or recursive newborn evaluation inside one event.
- No fixed output canvas, maximum-growth buffer, truncation, implicit crop, padding symbol, or sparse white background substituted for changing support.
- No implicit white identity, skipped white row, or default rule row.
- No neighbor/context label in strict RULE reads; that belongs to T28.
- No orientation, overlap, collision, or painter policy imported from T27 into strict T26.
- No mixed-patch step committed until equal heights within each source row and equal total slab widths across source rows are validated; no patch-width equality down source columns is invented.
- No incompatible result with a successor, step, token mutation, or partial commit.
- No geometric shape/orientation meaning inferred from opaque labels `0..3` and no `OTHER_SHAPES` role codec constructed.
- No undeclared source repair. The only native repair is the guarded removal of the surplus final `\}` immediately before `\$` at `BOOK:13744`; no JPEG glyph, palette, seed, table, trace, or scale is treated as semantic data.
- No digit formula, finite automaton, Kronecker product, constraint solver, compression method, or fractal limit used to bypass native stepping.
- No integer rule codec invented; structural table identity is preserved.
- No source handle validated by generation number alone; exact snapshot/run/branch provenance is required.
- No raw successor-token identity used for cross-representation equality; the independently minted successors are compared through the explicit reversible source/successor token bijection, including all typed lineage handles.
- No cells-only T27 claim: outcome/changed, successor count, step presence, carrier, rectangles, every local child/target/prototype/pose witness, and exact successor-lineage equality are part of the proof.
- No addressed-bag equivalence claimed outside the explicit inverse image.
- No D019/T13 selected-source, epsilon, empty/no-selected, or common-positive fixed-block behavior altered while adding ranked assembly.

## Completion Requirements

- [x] Direct names, aliases, variants, captions, Notes, Index, cross-references, absent modern terms, and false positives are dispositioned with zero unresolved source candidates.
- [x] All retained source lines have exact monolith provenance and split reverse coverage.
- [x] Source extraction defects are explicit, no undeclared repair enters native semantics, and the exact guarded one-brace repair at `BOOK:13744` is disclosed and tested.
- [x] The 26-asset universe is hash/reference/dimension/classification closed with an honest zero-transcription boundary.
- [x] Strict state, frontier, read, rule, write, update, seed, successor, trace, variant, and observer semantics are reconstructed.
- [x] The corrected D019 relationship is explicit: ordered selected-source concatenation is the rank-one mosaic member, unselected sources are consumed, selected epsilon and empty/no-selected cases are preserved, the positive common-block subset overlaps the named uniform wrapper, and T26 adds full-source rank-two compatibility/product placement.
- [x] The stage specifies the category-3 T27 carrier correctly as `(prototype_id, pose)` with one distinct prototype ID per label and common declared unit-square geometry, independently minted successor tokens compared through a reversible bijection, and the complete `StepResult` envelope and lineage preserved.
- [x] Current API/runtime/tests are inspected and the smallest generic Goal 2 delta is implementation-ready.
- [x] The semantic oracle proves the repaired `BOOK:13744` trajectory, crossed-width compatibility, incompatible no-successor outcomes, selected-rank-one/D019 contract, exact lineage/provenance, corrected full-result prototype-keyed bag representation, and final totals/digests.
- [x] Source, asset, semantic, architecture, portability, fail-closed, silent-import, compile, repository-test, file-mode, Markdown, and local-scope gates pass.
- [x] Independent hostile review of this stage document has run and all findings are resolved.
- [x] Root integration into `0-plan.md`, `evidence-index.md`, `design-ledger.md`, and `architecture-audit.md` is confirmed; the eventual consolidated Goal 2 handoff remains the goal-level synthesis deliverable.

## Gate Results

| Command/gate | Result |
|---|---|
| `python3 goal-1/38-T26-source-oracle.py` | PASS; exact `BOOK:13744` surplus-brace repair `raw=11/12 -> repaired=11/11`, crossed-column-width `2x3` acceptance with both columns seeing widths `1,2`, and `unresolved_total OK 0`; SHA-256 `124b2be2c5ac1121946f7fe952d83ca93403782998992ffcd5974d9c8339b5f2`. |
| `python3 goal-1/38-T26-asset-oracle.py` | PASS; 26 governed, 52 references, 26 hashes, zero unresolved; SHA-256 `e36e7ec66460c81cd5d78f0dbe39188c431961c135b7c76a87be68e369ffd438`. |
| `python3 goal-1/38-T26-semantic-oracle.py` | PASS; unique partition `6,667 native/generic + 6,658 full-StepResult bag + 16,709 selected-rank-one = 30,034`; 81 hostile rejections, including 2 typed incompatible/no-commit outcomes; digest `e380704a0626ad7a578e0937007cfa6ea8cc0dd6cee1b8c2d24a7eab18b7c57c`; SHA-256 `10395a02c1bd44514e610c98e1efc861513541a0b8b7046fedd557629e43a0f4`. |
| Absolute-path execution from `/tmp` for all three oracles | PASS; output is byte-identical to repository-root execution. |
| `python3 -O` for all three oracles | PASS as a fail-closed gate; each exits 1 before verification. |
| Silent `runpy.run_path(..., run_name='audit_import')` for all three | PASS; exit 0 and no output. |
| Explicit in-memory compilation of all three oracles | PASS. |
| `uv run pytest -q` | PASS; 102 tests in 1.29 seconds. |
| Independent hostile re-review | PASS; no blockers after a clean review of the final stage, global decisions, proofs, and oracles. |
| File mode, `git diff --check`, and Markdown/scope checks | PASS; stage mode is `0644`, no whitespace errors, Markdown fences are balanced, and this assigned edit touched only the stage file. |

## Stage Results

**COMPLETE.** The regenerated 30-query source audit closes 94 lines at `67 pre-Index / 27 actual-Index`, retains 115 at `23 native / 67 relation / 25 control`, excludes 11, reverse-covers every retained line as `77 exact + 38 mapped`, and leaves zero unresolved. The dependent asset audit closes 26 unique JPEGs at `3/16/7`, 52 references, 26 hashes, 1,838,481 bytes, five complete assemblies, and `26 hash-bound / 0 transcribed / 0 pixel-replayed`.

The corrected construction requires generic `RankedBlockMosaicAssemble` on the shared UPDATE axis. D019's ordered selected-source behavior is its rank-one member: selected epsilon is retained, every unselected source is consumed with zero-width lineage, and empty/no-selected cases yield the empty successor. `RankedUniformBlockAssemble` is only the positive-old-shape/common-positive-block restriction and overlaps the 600 common-positive T13/D019 cases; T26 uses positive full-source rank two. Rank-two compatibility requires equal patch heights within each source row and equal total slab widths across source rows, with no per-column width invariant. The exact crossed-width witness succeeds. Incompatibility returns `PatchStepResult(Invalid(IncompatibleMosaic(...)), successors=(), step=None)` before allocation or commit.

The complete `BOOK:13744` mixed table is native after the explicitly guarded removal of its one surplus final brace. From seed `{{3}}` it produces compatible square sides `1,2,3,5,8,13,21`. Labels `0..3` remain operationally opaque; no numeric geometric-role assignment or `OTHER_SHAPES` role codec is constructed.

The semantic oracle closes the unique partition `6,667 native/generic + 6,658 prototype-keyed full-StepResult posed-bag + 16,709 selected-rank-one = 30,034` commuting proofs and 81 hostile rejections, including 2 typed incompatible/no-commit outcomes. Rank one partitions as 1,519 all-selected plus 15,190 consuming an unselected source; its 1,470 positive all-selected, 49 empty-input, 98 singleton/no-selected, 1,390 selected-epsilon, 1,519 right-neighbor-frontier, and 600 common-positive counters are nested/crossing and non-additive. Named page/native/bag, non-white, and newborn fixtures that overlap exhaustive cases are likewise not double-counted.

T27 state encoding uses `(prototype_id, pose)`: each T26 label maps bijectively to a distinct prototype ID while all prototypes share declared unit-square geometry. Encoding maps/shares the source token; grid and bag UPDATE independently mint their successor tokens, then compare the two source/successor pairs through an explicit reversible token bijection. The proof covers outcome/changed, successor cardinality, step presence, successor carrier, every parent rectangle, every local child/target/prototype/pose witness, and exact equality between lineage children and the successor. Uniform steps have the parent-local pose commuting proof; mixed mosaics are not given that one-step T27 claim without further evidence. No T26 class, UPDATE algebra, executor, family branch, callback, hidden control, fixed canvas, implicit white behavior, or raster program is introduced. Independent hostile re-review found no blockers, and the accepted result is root-integrated into the Goal 1 architecture, plan, ledger, and evidence index.
