# 38-T26-2D-SUBSTITUTION

Status: **SOURCE, ASSET, AND CORRECTED ARCHITECTURE COMPLETE — REGENERATED SEMANTIC ORACLE AND HOSTILE REVIEW PENDING**

## Current Facts

- T26 is CSV physical line 27, `Two-Dimensional Substitution Systems`; `ref/notes/CA-Types.md` section 26 is a vocabulary guide, not primary mechanics.
- The frozen Q00-Q29 source protocol closes 94 unique query lines at `67 pre-Index / 27 actual-Index`. It retains 115 lines at `26 native / 64 relation / 25 control`, excludes 11 pre-Index false positives, and leaves zero unresolved candidates.
- The retained source consists of 56 direct query hits plus 59 governed continuations. All 115 lines reverse-join to the 17-file split corpus as `77 exact + 38 mapped variants`; none is monolith-only.
- The construction is a finite nonempty rectangular grid of finite tile labels in discrete `t+2D`. Every old tile fires exactly once from one immutable generation, reads only its own old label, and emits a nonempty rectangular patch from a total closed table. The uniform-patch profile is the core total-on-all-grids preset; `BOOK:13744` also gives a complete native mixed-patch table and seed.
- UPDATE is the Notes' exact `Flatten2D` product-order assembly. Generic `RankedBlockMosaicAssemble(rank=2)` accepts a step exactly when all emitted patches within each old source row have equal heights and all resulting row slabs have equal widths. `RankedUniformBlockAssemble` is its always-compatible uniform restriction. Both preserve source/product order, consume the complete old generation, and defer every newborn tile until the next event.
- White is an ordinary label. The explicit non-white-background variant proves that a white tile may emit black descendants; there is no implicit white identity, blank-skip optimization, or ambient fill rule.
- T26 is not merely a rank-two parameter value of D019's linear `OrderedGenerationConcat`: naive flattened concatenation loses rank-two placement. Generic `RankedBlockMosaicAssemble` extends that UPDATE pattern by rank and compatibility; rank-one is D019 variable-length concatenation, its uniform rank-one restriction overlaps fixed-block T13/D019, and rank two is T26 mosaic assembly.
- The same state has a category-3 lossless representation inside T27's posed occurrence bag exactly on the aligned, uniform, hole-free, overlap-free rectangular-tiling image. Arbitrary free geometry remains T27.
- The `Other shapes` text supplies the complete encoded-label rule `0..3`, seed `{{3}}`, and enough `Flatten2D` semantics to execute its compatible mixed patches natively; its square side lengths begin `1,2,3,5,8,13,21`. What remains unspecified is the inverse map from labels to geometric shape/orientation roles, not the encoded grid evolution. Neighbor-dependent patch choice remains T28.
- The source-governed asset universe closes 26 unique JPEGs at `3 native / 16 relation / 7 control`, 52 exact monolith/split references, 26 unique hashes, and 1,838,481 bytes. The honest boundary is `26 HASH_BOUND / 0 TRANSCRIBED / 0 PIXEL_REPLAYED`.
- The previous semantic-oracle totals (`6,664` native/generic events, `13,915` commuting proofs, `20,992` old-tile firings, `6,659` posed-bag commutations, `600` rank-one commutations, and `53` hostile rejections) cover only the uniform core and are superseded as final stage totals. Regenerated totals and digests incorporating the native mixed-patch trajectory are pending.
- D132's corrected architecture result is rank-two compatible block-mosaic assembly with a lossless aligned posed-bag representation. Generic UPDATE-policy implementation is required, but no new execution algebra, T26 state or UPDATE class, executor, family branch, callback, padding scheme, hidden control, or raster-defined program follows.

## Final Semantic Conclusions

- RULE data is a total, canonical, finite, alphabet-closed, callback-free map `delta : TileLabel -> RectPatch(TileLabel)`. The core uniform profile declares one positive `(h,w)` shared by every row; the native mixed-patch profile allows label-dependent positive rectangular shapes and validates mosaic compatibility per old snapshot.
- CONFIGURATION is a finite nonempty rectangular label grid. The dimensions change from `(H,W)` to `(H*h,W*w)` after one event; a fixed-capacity canvas is not state.
- FRONTIER is `AllOldTiles`, with opaque old-snapshot handles. Canonical row/column order supports deterministic assembly and lineage, but a tile's product address—not incidental flat enumeration—determines its descendants' placement.
- NEIGHBORHOOD is `SelfOnly`. Surrounding labels, coordinates, generation number, raster scale, finite-automaton digits, ancestry, and output geometry are not RULE inputs.
- RULE returns a typed source-bound patch write. UPDATE validates exact full coverage, provenance, and rank-two mosaic compatibility, consumes every old tile, and constructs one successor using product coordinates.
- A complete uniform table produces one deterministic successor on every valid rectangular grid. A mixed table produces one deterministic successor on compatible grids and a typed `Invalid(IncompatibleMosaic)` step otherwise. Missing rows and malformed/empty patches are invalid programs; they are not halts. A fixed point or a `1 x 1` identity row is still an applicable event.
- The source gives no numeric T26 rule codec. The structural table is program identity. For the uniform subfamily with alphabet size `k` and fixed patch shape `(h,w)`, the derived rule-family count is `k^(k*h*w)`.
- Display scale, raster colors, nestedness, fractal limits/dimensions, coordinate formulas, compression, constraints, and Walsh/Kronecker descriptions are observers, relations, or alternative generators. None may replace native stepping.
- T26 shares the branch-free SimpleProgram runner:

```text
active = AllOldTiles.select(configuration)
reads  = SelfOnly.read(configuration, active)
writes = ClosedPatchTable.apply(active, reads)
next   = RankedBlockMosaicAssemble(rank=2).apply(configuration, active, writes)
```

`RankedUniformBlockAssemble(rank=2)` is the validated uniform preset of that same UPDATE policy.

## Big Picture Objective

Reconstruct two-dimensional substitution systems from primary Book evidence, distinguish the strict aligned uniform-patch construction from T27 geometry and T28 contextual choice, and identify the smallest faithful reuse of DOMAIN, CONFIGURATION, ALPHABET, FRONTIER, NEIGHBORHOOD, RULE result, UPDATE, trace, and representation machinery. Prove one native event at a time that T26 uses a generic rank-two uniform-block UPDATE policy, overlaps fixed-block D019 at rank one without subsuming general variable-length D019, and is a checked category-3 restriction of T27, without inventing a family executor or using rasters as program data.

## Catalog Identity

- Stable ID: T26.
- Exact CSV name: Two-Dimensional Substitution Systems.
- CSV physical line: 27.
- Taxonomy section: 26.
- Entry kind: deterministic rank-two preset of generic uniform-block assembly under the shared SimpleProgram algebra.
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
- Retained: 115 = 26 native + 64 relation + 25 control.
- Directly matched retained lines: 56; governed continuations: 59.
- Excluded: 11, including one-dimensional systems merely represented in 2D, 1D contextual/L-system routes, generic heading collisions, and unrelated `Flatten2D` uses.
- Actual Index: all 27 dense physical lines have exact occurrence guards. The partition is 15 direct/grid/named/alias/representation routes, 2 geometric/contextual sibling routes, 2 one-dimensional alias controls, and 8 generic Penrose collisions.
- Split query reverse join: 92 records = 80 exact + 12 mapped variants.
- Split retained reverse join: 115 records = 77 exact + 38 mapped variants; 0 monolith-only.
- Atlas: 2 summary-only hits. Catalog and taxonomy text remain vocabulary controls only.
- Governed source-image interface: 26 lines, digest `9018acedd5ff638608aa2a79feb5059de5b8a671792ab0c8ec501437eea85ee7`.
- Source-oracle SHA-256: `549df7bf05804ac977985152671845e2d5ac70d3576bd2715e1e1e5e1ab9a029`.
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

### E11 — `Other shapes` gives a native encoded-label mixed-patch preset

- Source: `BOOK:13740-13744`.
- Establishes: the encoded equal-square grid evolution is completely specified by a four-label mixed-patch rule, seed `{{3}}`, and the source's `Flatten2D`; only the geometric decoding of the four labels remains unspecified.

> one can also set up substitution systems that are based on subdividing other geometrical figures
>
> Labelling each shape and orientation with a different color, the behavior of this system can be reproduced with equal-sized squares using the rule ...

The text-owned rule data, with only Markdown/TeX delimiters normalized, is:

```text
3 -> ((1,0),(3,2))
2 -> ((1,),(3,))
1 -> ((3,2),)
0 -> ((3,),)
seed = ((3,),)
```

The emitted shapes are `2×2`, `2×1`, `1×2`, and `1×1`. The source `Flatten2D` supplies their assembly law: within each old source row, patches must have the same height so corresponding local rows can be joined; the resulting row slabs must have equal widths so the successor remains rectangular. The source trajectory is compatible and has square side lengths `1,2,3,5,8,13,21` through six steps. The prose does not state which numeric label denotes which geometric shape/orientation, so geometric role decoding remains a relation with no guessed codec.

### E12 — rule counts are structural, not raster codecs

- Source: `BOOK:14099-14109`.
- Establishes: the source's “4 billion or so” matches the derived four-color `2x2` family, and a 16-color relation uses only 51 possible local blocks.

> searching all 4 billion or so possible such systems with 2×2 blocks and up to four colors

For a complete `k`-label, `h x w` table the derived count is `k^(k*h*w)`: binary `2x2` gives 256, ternary `3x3` gives `3^27 = 7,625,597,484,987`, and four-color `2x2` gives `4^16 = 2^32 = 4,294,967,296`.

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
| `13752` | massively repeated/corrupted Penrose expression | Relation only; never executable T26 data. |
| `14105` | malformed multi-kilobyte 16-color table row | Constraint relation only; no table recovery claimed. |
| `19197` | tuple/bracket transcription in a relation rule | Literal relation retained; no strict fixture derived from it. |

No raster, external formula, or guessed bracket repair is used to fill these gaps.

## Asset Closure

`38-T26-asset-oracle.py` depends fail-closed on the exact source-oracle evidence/image sets and binds every governed image to its unique file, monolith and split references, byte length, dimensions, SHA-256, evidence class, and assembly membership.

- 26 governed assets = 3 native + 16 relation + 7 control.
- Native: two strict square-grid plates (`BOOK:2314,2322`) and one non-white-background plate (`BOOK:13724`).
- Five indivisible assemblies contain 14 files: geometric orientation, geometric overlap, perception comparison, coordinate/finite-automaton, and Walsh/Kronecker.
- The remaining governed relations/controls cover recursive subdivision, nestedness perception, coordinate gallery, other shapes, Penrose, constraint-forced nesting, the geometric gallery, the T28 grid control, and a 3D geometric observer.
- Fixed-radius saturation closes 50 nearby candidates as 26 governed + 24 explicitly excluded. The inherited Chapter 3 one-dimensional substitution plates remain governed by T13 rather than being double-counted by T26.
- 52 exact Markdown references, 26 unique files, 26 unique hashes, 1,838,481 total bytes, and zero exact duplicates.
- Ledger digest: `6efdf22fdacd0bc9c9b5f59ef61e56c29cdbb9d76624dad5c088c8aed0e17beb`.
- Asset-oracle SHA-256: `b7ceda835ef6092a6993e84560fcec1253b605b795815d52736f74331758c5e3`.
- Honest boundary: `HASH_BOUND=26`, `TRANSCRIBED=0`, `PIXEL_REPLAYED=0`.

The exact page-187 rule/seed and the `Other shapes` encoded-label rule/seed come from `BOOK:13683` and `BOOK:13744`, not pixels. Page-188 displayed rules, all displayed intermediate arrays, panel seeds/traces, palettes, glyph meanings, and renderers remain unrecovered. A hash-bound raster cannot become an executable rule or conformance trace.

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

Equivalently, child `(i,j)` of source `(r,c)` is placed at

```text
target_row = sum(row_height[r0] for r0 < r) + i
target_col = sum(width(write[r,c0]) for c0 < c) + j
```

only after compatibility and exact old-source coverage are validated. If a source row mixes patch heights, or assembled row slabs have unequal widths, UPDATE returns typed `Invalid(IncompatibleMosaic)` rather than padding, cropping, guessing a collision rule, or emitting a ragged configuration. Every compatible target address has exactly one parent/local-coordinate pair, so assembly has neither a collision policy nor an overlap policy.

`RankedUniformBlockAssemble(rank=2)` is the restriction where every write has `(p_h,p_w)`. It is compatible for every rectangular old grid and reduces the offsets to

```text
next[r*p_h+i, c*p_w+j] = write[r,c][i,j]
next.shape = (H*p_h,W*p_w)
```

Each event may return lineage rectangles:

```text
parent (r,c) -> rows [row_offset[r], row_offset[r] + height(write[r,c]))
                cols [col_offset[r,c], col_offset[r,c] + width(write[r,c]))
```

Lineage is event/witness data. RULE cannot read it, and semantic grid equality does not depend on occurrence IDs.

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

Applying the text-owned `BOOK:13744` mixed table from seed `((3,),)` gives compatible square shapes `1,2,3,5,8,13,21`. This is native encoded-label evolution. Recovering the pictured square/GoldenRatio-rectangle geometry would additionally require the absent label-to-role codec and remains outside the native fixture.

### State, outcomes, and boundaries

| Axis | Strict T26 semantics |
|---|---|
| DOMAIN | Discrete `t+2D`. Time is event order; the spatial configuration is a finite rectangular product support. |
| CONFIGURATION | Complete finite `H x W` grid of tile labels with an opaque snapshot identity. Shape may change each event. |
| ALPHABET | Finite ordered tile labels; optional shape/orientation roles require an explicit finite lossless codec. |
| SEED | Any valid finite nonempty rectangular grid; canonical source seeds include page-187 `{{1}}` and mixed-patch `{{3}}`. |
| FRONTIER | Every old tile exactly once, using snapshot-scoped handles. |
| NEIGHBORHOOD | Self label only. No boundary read is required. |
| RULE | Total closed label-to-nonempty-rectangular-patch table. The core preset adds a table-wide uniform-shape invariant. |
| RESULT | One typed source-bound ranked block write per old tile. |
| UPDATE | Exact `RankedBlockMosaicAssemble(rank=2)`/`Flatten2D` assembly with row-height and slab-width compatibility, old-snapshot full coverage, parent consumption, and newborn deferral. Uniform assembly is its total-on-all-grids restriction. |
| SUCCESSOR | Exactly one valid grid for a compatible step. A fixed point remains an `Advanced(changed=false)` event; incompatibility is typed invalidity. |
| HALTING | No intrinsic halt for a compatible valid step; horizon/cancel/resource/invalidity remain external or typed outcomes. |
| TRACE | Ragged rectangular snapshots plus optional parent-child rectangles; padding and raster coordinates are downstream representations. |

## One-Step Reuse Proofs

### Ranked block-mosaic UPDATE and its D019 overlap

D019's existing `OrderedGenerationConcat` is a linear UPDATE policy: in source order it concatenates each source symbol's possibly variable-length output word. T26 does not turn that combiner into rank two by changing one integer. It requires generic `RankedBlockMosaicAssemble` on the existing UPDATE axis. At rank one, mosaic assembly has no cross-row constraint and its semantics are exactly D019 variable-length concatenation. D019 keeps its existing linear policy and behavior; this shared rank-one semantics does not require rewriting that stage or replacing its named combiner.

The uniform restriction `RankedUniformBlockAssemble` uses an old product shape `S=(s_0,...,s_(d-1))`, a common positive block shape `B=(b_0,...,b_(d-1))`, and one block per old product address. It places local coordinate `u` from source coordinate `x` at

```text
target_axis[a] = x[a] * B[a] + u[a]
```

and produces shape `S*B` componentwise.

- At rank one with common `B=(q)`, it is the fixed-block restriction/commuting overlap of T13/D019, with parent/child order preserved.
- At rank one with label-dependent block lengths, `RankedBlockMosaicAssemble` coincides with general D019 `OrderedGenerationConcat`.
- At rank two with common `B=(p_h,p_w)`, uniform assembly is the always-compatible core T26 `Flatten2D` preset.
- At rank two with label-dependent rectangular blocks, mosaic assembly applies the row-height and slab-width compatibility law. `BOOK:13744` supplies a native compatible trajectory.

The existing semantic-oracle baseline proves 600 exhaustive binary rank-one commutations for uniform block lengths 1 and 2. A nonsymmetric two-source `2×2` adversary proves that flattening every patch and concatenating the flat streams gives the wrong grid: one parent's second local row is placed before the adjacent parent's first local row. Rank-two placement therefore requires product-aware mosaic assembly. This is a justified generic policy on the shared UPDATE axis, not a new execution algebra, family executor, or T26-named class.

### Category-3 addressed posed-bag representation

For grid shape `(H,W)`, declare a bijection `prototype : TileLabel <-> PrototypeID`. Every prototype has the same declared unit-square geometry, but prototype identity remains distinct because T27 rules are keyed by prototype. Encode tile `(r,c)` with label `X[r,c]` as the T27 carrier pair `(prototype(X[r,c]), pose[r,c])`, where

```text
linear      = diag(1/W, 1/H)
translation = (c/W, r/H)
```

A local uniform-patch child `(i,j)` has

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

for one event. The oracle proves 6,659 such commutations: 6,656 exhaustive binary `2x2` events, two page-187 events, and one rectangular `2x3` architecture witness. Permuting bag enumeration does not change state or the successor. Bags outside the invariant image remain T27 rather than being coerced into T26.

The mixed-patch native preset is still losslessly encodable snapshot by snapshot through distinct prototype IDs, but this document does not claim that its global equal-square mosaic reflow commutes with the same parent-local T27 pose update. Such a claim would require the absent geometric role codec or a separately proved T27 representation. The regenerated oracle must keep that boundary explicit.

## Semantic and Conformance Closure

The checked-in `38-T26-semantic-oracle.py` currently predates the two architecture corrections in this stage. Its uniform-core baseline remains useful but is not the final semantic closure:

- Superseded baseline: 6,664 native/generic events, 13,915 commuting proofs, 20,992 old-tile firings, 6,659 uniform addressed-bag commutations, 600 uniform rank-one proofs, and 53 hostile rejections.
- Superseded baseline digest: `b4fdbf272ff544cb824c0244e07240b8bb7b43967efd89ed70ef0637f9488a2a`.
- Superseded baseline oracle SHA-256: `0f5fb7d720ddce69a9e1bcfcdde102d9052de44f2d06575b07dcaade0f2723ee`.
- Still valid baseline partitions include all 256 binary `2×2` uniform tables across the 26 labeled grids, the page-187 fixtures, rectangular `2×3` uniform witness, non-white-background witness, newborn deferral, rule-count checks, and the wrong-flat-concatenation rejection.
- Required regenerated coverage: D019 variable-length rank-one overlap; `RankedBlockMosaicAssemble` direct/generic commutation; exact `BOOK:13744` rule and seed through side lengths `1,2,3,5,8,13,21`; row-height and slab-width compatibility; incompatible-mosaic typed rejection; exact child provenance/lineage; and prototype-keyed T27 carrier checks.
- Final native/generic count: **PENDING REGENERATED ORACLE**.
- Final commuting/rejection counts and semantic digest: **PENDING REGENERATED ORACLE**.
- Final semantic-oracle SHA-256: **PENDING REGENERATED ORACLE**.

The `2x3` table is deliberately an architecture witness for general rectangular ranked assembly, not a claim that a displayed Book raster supplied that rule.

## Strict Boundary and Variant Disposition

| Candidate | Disposition |
|---|---|
| Page-187 binary `2×2` and page-188 ternary `3×3` square-grid systems | Native uniform T26 presets. |
| Non-white backgrounds | Native table/seed variant; label 0 is ordinary. |
| Any closed uniform positive rectangular patch shape | Native total-on-all-grids restriction of generic `RankedBlockMosaicAssemble`; source canonical fixtures remain square. |
| Higher-dimensional `SSEvolve`/`FlattenArray` | Ranked relation/generalization, not a T26 executor mode. |
| `BOOK:13744` encoded-label rule `0..3` from seed `{{3}}` | Native mixed-patch T26 preset under source `Flatten2D`; compatible side lengths `1,2,3,5,8,13,21`. |
| Shape/orientation meaning of labels `0..3` | Geometric representation relation only; source gives no role-to-label inverse codec. |
| Other mixed-patch table/grid pair | Native only for a step satisfying row-height and slab-width compatibility; otherwise typed invalidity, never implicit padding/cropping. |
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
| ALPHABET | `:200-215` permits finite/symbolic values. | `DIRECT` for finite tile labels; explicit role products/codecs are a `PARAMETERIZATION`. |
| SEED | `:235-291` separates initialization from rules. | `PARAMETERIZATION` by a valid rectangular tile grid. |
| FRONTIER | `:396-454` provides shared selectors; `:1412-1510` currently frames frontier as writable next coordinates. | Selector responsibility is reusable, but old occurrence handles/full-source coverage need a generic `PRINCIPLED EXTENSION`. |
| NEIGHBORHOOD | `:360-394` separates reads from frontier; `:1303-1328` gives current-self-only access. | `DIRECT`. |
| RULE | `:1767-1791` returns one scalar next-site value. | `PRINCIPLED EXTENSION` to closed nonempty rectangular-block data/results, with uniform shape as a validated restriction; no callback. |
| UPDATE | The root schema lists no explicit UPDATE axis and hardwires fixed-shape scalar copy/write at `:22-38,1767-1791`. | Generic `RankedBlockMosaicAssemble` is the smallest `PRINCIPLED EXTENSION` on the existing UPDATE axis. Rank one coincides with D019 variable concatenation; rank two plus compatibility is T26. `RankedUniformBlockAssemble` is the total-on-all-grids restriction, not a fresh algebra. |
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
| Finite labels | 1/2 | Existing finite ALPHABET | Deterministic order; optional explicit role codec. | No. |
| `AllOldTiles` | 2 | T13 `AllOccurrences` frontier | Every and only old tile once; opaque exact-snapshot provenance. | No. |
| `SelfOnly` | 1 | Existing self projection | Only the selected old label is RULE-visible. | No. |
| Closed rectangular patch table | 2 | D020 closed morphism data plus generic ranked result | Total canonical rows; positive rectangular outputs; alphabet closure; optional uniform-shape restriction. | No. |
| Ranked patch write | 2 | Existing typed result axis plus D019 ordered-emission precedent | Source-bound block plus product-local order and exact provenance. | No. |
| `RankedBlockMosaicAssemble` UPDATE | 2 plus shared-axis implementation gap | Existing UPDATE axis; rank-one D019 semantics are the commuting base | Rank-two row-height/slab-width compatibility, full old coverage, product-order assembly, parent consumption, newborn deferral. | Goal 2 adds a generic policy, not a new algebra or T26 class. |
| `RankedUniformBlockAssemble` | 2 | Restriction of ranked mosaic assembly | One common positive shape; total on every rectangular grid; fixed-block D019 overlap at rank one. | No separate executor. |
| Dense grid to posed bag | 3 | D041-D043 `(prototype_id, pose)` occurrence bag | Label/prototype bijection; shared declared unit-square geometry; inverse on aligned/no-hole/no-overlap image. Uniform-patch steps commute with parent-local pose composition; mixed mosaic is only snapshot-encoded absent a further proof. | No; T27 remains broader. |
| Other-shape color roles | 3 where a complete finite codec is declared | Finite tagged/product ALPHABET | Lossless role round trip; no guessed assignment. | No. |
| `BOOK:13744` mixed-size encoded table | 2 | Ranked mosaic assembly plus text-owned `Flatten2D` | Complete `0..3` table, seed `{{3}}`, compatible reachable trajectory. | Native T26 preset; geometric decoding remains unclaimed. |
| Contextual patch choice | Separate T28 parameterization | T14-style contextual read plus T26 result shape | Neighbor reads and boundary must be explicit. | T28 remains pending. |

No class-4 execution algebra is justified. D019's existing variable-length linear policy is preserved; its behavior is the rank-one member of mosaic assembly. D041-D043 remain unrestricted geometry, and Goal 2 implements the missing generic UPDATE policy without reopening T13 semantics.

## Principles Audit

- The user's correction governs: Wolfram's simple programs are the abstraction; cellular automata are one preset. `src/ca` is the current SimplePrograms substrate, not a boundary that forces T26 outside it.
- Semantic role and representation are separated. A tile grid and an aligned prototype-keyed posed bag are complete snapshot representations with an explicit inverse. The one-event T27 parent-local commuting square is proved only for the uniform-patch restriction.
- `OrderedGenerationConcat` remains D019's linear implementation. Generic mosaic assembly agrees with it at rank one, while rank two adds explicit compatibility and product placement. Neither policy is copied under a T26 name.
- Complete state contains every tile label and product address needed to advance. Lineage, renderer scale, and coordinate analyzers are downstream.
- RULE data is closed and inspectable. No host callback, raster decoder, formula bypass, family dispatch, or hidden interpreter is admitted.
- The uniform-patch invariant is the evidence-bearing total-on-all-grids core. Mixed-size compatibility is also source-backed through `Flatten2D`, but is validated exactly; overlap, collision, orientation, geometric role decoding, and neighbor choice are not fabricated.
- A fixed padded canvas, giant sparse background, or same-shape NumPy trajectory would alter the support semantics. It is not a valid implementation shortcut.

## Goal 2 Implementation Stage

### G2-T26 — ranked block-mosaic replacement and aligned-grid representation

Objective: implement generic rank-two compatible block-mosaic assembly in the shared branch-free SimpleProgram runner, expose uniform assembly as its total-on-all-grids restriction, preserve D019's existing rank-one linear behavior, and implement the checked prototype-keyed T27 snapshot representation without overclaiming mixed-patch pose commutation.

Dependencies:

- D018/D019/D020 and T13: old-generation coverage, closed morphism data, ordered child assembly, newborn deferral, opaque snapshot provenance, lineage, and ragged traces.
- D041-D043 and T27: exact posed occurrences, parent-local composition, multiplicity-preserving bag semantics, and the aligned-grid restriction map.
- Generic typed `StepResult`, configuration, selector, rule-result, UPDATE, serialization, and trace axes from the architecture audit.

Implementation work, in shared-axis terms:

1. Add a generic finite ranked rectangular configuration with positive extents, closed labels, immutable values, and opaque snapshot identity. Successor shape belongs to the successor configuration, not a fixed `Dynamics.shape`.
2. Add snapshot-scoped ranked occurrence handles and an `AllOccurrences`/`AllOldTiles` selector preset that proves exact old coverage.
3. Reuse the generic self projection for a typed `TileRead(source,label)`.
4. Add closed finite `Label -> RankedBlock` table data with canonical complete keys, declared rank, positive rectangular per-row extents, and alphabet closure. Add a uniform-shape table invariant as a restriction; do not require an integer rule ID.
5. Add a generic source-bound nonempty ranked-block result. Leave D019/T15's existing variable/zero-length linear result semantics intact rather than forcing them through the stricter T26 carrier.
6. Add generic `RankedBlockMosaicAssemble` on the UPDATE axis. At rank two validate equal patch height within each old source row and equal assembled slab width across source rows before committing. Its rank-one behavior must equal D019 `OrderedGenerationConcat`, while D019 keeps its existing implementation.
7. Add `RankedUniformBlockAssemble` as the common-positive-shape restriction using `target[a]=source[a]*block_shape[a]+local[a]`. Preserve fixed-block rank-one concatenation byte-for-byte and expose rank two through policy data, not family dispatch.
8. Return exact child hyperrectangles, product-local coordinates, source handles, and snapshot/run/branch provenance as typed lineage events, while keeping them out of RULE reads.
9. Extend trace storage to ragged structured configurations. Any padded tensor export must carry an explicit mask/shape and remain a downstream lossy-or-scoped representation.
10. Add encode/decode adapters between rectangular grids and T27 `(prototype_id, pose)` bags: map each label bijectively to its own prototype ID, declare unit-square geometry for every prototype, use exact rational poses, and enforce all image invariants. Reject holes, overlaps, duplicates, rotations, skews, off-grid translations, unknown prototypes, and nonbijective codecs. Prove parent-local step commutation only for uniform blocks unless a separate mixed-mosaic proof is supplied.
11. Expose optional named T26 presets that assemble these existing axes. They must not introduce a T26 state class, UPDATE class, executor, or rollout branch.

Expected shared runtime homes include generic configuration/update/result modules plus extensions to `alphabets.py`, `loci.py`, `frontiers.py`, `neighborhoods.py`, `rules.py`, `specs.py`, and the branch-free rollout path. Exact file decomposition belongs to the Goal 2 architecture synthesis; catalog identity must never choose execution code.

Required conformance:

- Exact page-187 `t0 -> t1 -> t2` fixture from text-owned rule/seed data.
- Exact `BOOK:13744` mixed-patch table from seed `{{3}}`, producing square side lengths `1,2,3,5,8,13,21` with exact lineage.
- All 6,656 exhaustive binary `2x2` table/grid events and 20,992 old-tile firings.
- The rectangular `2x3` architecture witness and wrong-flat-concatenation counterexample.
- All 600 rank-one T13 fixed-block commutations.
- Variable-length rank-one equivalence with D019 `OrderedGenerationConcat`.
- Hostile rejection of unequal patch heights within one source row and unequal assembled slab widths across source rows.
- The uniform baseline's 6,659 addressed-bag commutations and inverse/image rejections, with distinct prototype IDs for distinct labels.
- Non-white-background, context-independence, newborn-deferral, renderer-noninterference, and bag-permutation tests.
- All 53 hostile validation cases.
- Static absence of T26 family dispatch, callback execution, raster rule ingestion, fixed-capacity padding, implicit white identity, and invented mixed-size compatibility.

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
- No mixed-size `Other shapes` table executed without a complete source-backed compatibility law and role codec.
- No source line repaired silently and no JPEG glyph, palette, seed, table, trace, or scale treated as semantic data.
- No digit formula, finite automaton, Kronecker product, constraint solver, compression method, or fractal limit used to bypass native stepping.
- No integer rule codec invented; structural table identity is preserved.
- No source handle validated by generation number alone; exact snapshot/run/branch provenance is required.
- No addressed-bag equivalence claimed outside the explicit inverse image.
- No T13 rank-one behavior altered while adding ranked assembly.

## Completion Requirements

- [x] Direct names, aliases, variants, captions, Notes, Index, cross-references, absent modern terms, and false positives are dispositioned with zero unresolved source candidates.
- [x] All retained source lines have exact monolith provenance and split reverse coverage.
- [x] Source extraction defects are explicit and no silent repair enters native semantics.
- [x] The 26-asset universe is hash/reference/dimension/classification closed with an honest zero-transcription boundary.
- [x] Strict state, frontier, read, rule, write, update, seed, successor, trace, variant, and observer semantics are reconstructed.
- [x] D019 rank-two reuse and the category-3 T27 representation have explicit one-step maps, inverses where claimed, exhaustive witnesses, and counterexamples.
- [x] Current API/runtime/tests are inspected and the smallest generic Goal 2 delta is implementation-ready.
- [x] Source, asset, semantic, architecture, portability, fail-closed, silent-import, compile, repository-test, and local scope gates pass.
- [ ] Independent hostile review of this stage document has run and all findings are resolved.
- [ ] Root integration into `0-plan.md`, `evidence-index.md`, `design-ledger.md`, and the eventual consolidated Goal 2 handoff is confirmed. Those global files are intentionally outside this stage-file-only task.

## Gate Results

| Command/gate | Result |
|---|---|
| `python3 goal-1/38-T26-source-oracle.py` | PASS; `unresolved_total OK 0`. |
| `python3 goal-1/38-T26-asset-oracle.py` | PASS; 26 governed, 52 references, 26 hashes, zero unresolved. |
| `python3 goal-1/38-T26-semantic-oracle.py` | PASS; 6,664 native/generic events, 13,915 commutations, 53 hostile rejections. |
| Absolute-path execution from `/tmp` for all three oracles | PASS; output is byte-identical to repository-root execution. |
| `python3 -O` for all three oracles | PASS as a fail-closed gate; each exits 1 before verification. |
| Silent `runpy.run_path(..., run_name='audit_import')` for all three | PASS; exit 0 and no output. |
| Explicit in-memory compilation of all three oracles | PASS. |
| `uv run pytest -q` | PASS; 102 tests in 1.29 seconds. |
| `git diff --check` and Markdown/scope checks | PASS; no whitespace errors, Markdown fences are balanced, and this task changed only this stage file. |

## Stage Results

**SOURCE, ASSET, SEMANTIC, AND ARCHITECTURE WORK COMPLETE; HOSTILE REVIEW PENDING.** The frozen 30-query source audit closes 94 lines at `67 pre-Index / 27 actual-Index`, retains 115 at `26 native / 64 relation / 25 control`, excludes 11, reverse-covers every retained line as `77 exact + 38 mapped`, and leaves zero unresolved. The dependent asset audit closes 26 unique JPEGs at `3/16/7`, 52 references, 26 hashes, 1,838,481 bytes, five complete assemblies, and `26 hash-bound / 0 transcribed / 0 pixel-replayed`.

The semantic oracle closes 6,664 native/generic events, 13,915 commuting proofs, 20,992 old-tile firings, 6,659 addressed-bag commutations, 600 rank-one commutations, 53 hostile rejections, exact page-187 checkpoints, uniform rectangular patch assembly, non-white backgrounds, newborn deferral, observer separation, and strict rejection of mixed-size `Other shapes`. D132 classifies T26 as D019 rank-two parameterization plus a category-3 restriction of D041-D043. The only Goal 2 gaps are generic typed-axis work: dynamic rectangular configurations, old-tile handles, self projection, closed patch tables, ranked block writes/assembly, lineage, and ragged traces.

No T26 class, UPDATE algebra, executor, family branch, callback, hidden control, fixed canvas, implicit white behavior, raster program, or mixed-size compatibility law is introduced. No completed stage reopens. Root must still run an independent hostile review of this document and integrate the final accepted result into the global Goal 1 ledgers and handoffs before declaring the stage fully complete.
