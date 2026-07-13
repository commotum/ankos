# 10-T27-GEOMETRIC

Status: **COMPLETE**

## Current Facts

- Exact catalog row: T27, CSV line 28, `Geometric Replacement And Fractal Systems`; taxonomy seed `ref/notes/CA-Types.md:737-758`. The canonical book name is “geometrical substitution systems.”
- The native main-text state is a finite multiplicity-preserving collection of oriented placed square occurrences in a fixed affine plane. It is neither a rigid grid nor the rasterized union of their black footprints.
- The canonical seed is one oriented black square. A rule contains a finite family of two or more smaller child-square placements expressed in the parent's local frame.
- Every old occurrence fires once from the same generation. If parent local-to-world pose is `P` and a child template is `C`, the child world pose is `P∘C`. Parent orientation is explicitly required to apply the rule.
- The successor consumes all old occurrences and multiset-unions all composed children atomically. Source enumeration and child-slot order can reproduce the Notes list, but no rule reads occurrence order; permutation is not geometric topology.
- Overlapping or coincident occurrences remain independently present with full multiplicity and lineage. Overlap does not collide, merge, mask, deduplicate, block, or alter later replacement.
- Off-grid geometry supplies no canonical neighbor relation. Each replacement depends only on its own parent, which is why the book says these systems inevitably generate nested/self-similar structure. T28 adds interaction only by returning to a grid.
- The exact page-189 and page-190 rules admit rational 2D affine matrices/vectors. Exact semantic equality needs no floating-point tolerance.
- The Notes reference `Nest[Flatten[f[#]] &, {0}, n]` stores an ordered list of complex centers. It preserves multiplicity and exactly reproduces the canonical generation sets, but it is an orbit-specific projection: a center alone is not Markovian for arbitrary oriented-square states.
- In the page-190 orbit, after three replacements two occurrences have center `(-1/8,-1/8)` but different orientations and different next local descendants. Full affine pose, not center or center multiplicity, is therefore native.
- Main figures label the unreplaced seed `step 1`; displayed step `k` is `k-1` replacement events. A one-parent rule with `b` child slots has exactly `b^n` occurrences after `n` events, regardless of overlap.
- The page-191 figure supplies four more rules. Rules (a)-(c) have two children; (d) has three. Several coefficients are only approximate in the official source and must retain an explicit finite-precision numeric profile.
- Arbitrary affine maps add translation, linear scaling, rotation, reflection, skew, and any finite dimension without changing full-generation bag expansion.
- Nonlinear Möbius and inverse-square-root branch maps are an evidenced native point-map variant, not affine rigid-shape poses. They require a separate closed map AST/carrier while sharing all-occurrence branching and bag commit.
- A limiting fractal/attractor, geometric union, 3D generation stack, complex-digit description, box-counting dimension, multifractal moments, and Mandelbrot parameter set are representations, observers, limits, or relations. None is the finite step state.
- T13 supplies the all-old-occurrences/parent-child lineage pattern, but its ordered concatenation is not permutation-invariant bag union. T20 supplies typed structural provenance but not affine geometry. T27 proves a sixth sibling update law.
- Current `seeds.fractal` is an unrestricted predicate rasterizer and current dataset “affine” transforms are downstream integer-coordinate augmentation metadata. Neither executes geometric replacement.

## Updated Assumptions

- A placed occurrence carries its complete local-to-world affine pose. A visually symmetric square is still orientation-sensitive because the rule's arrow/orientation marker affects future child placement; poses are not quotient by prototype symmetries.
- Semantic occurrence IDs and list positions are absent. Stable parent/child IDs and reference order belong to events and serialization; semantic equality is exact multiset equality of `(prototype,pose)` values with multiplicity.
- Child templates are parent-local. `P∘C` means `A'=A_p A_c` and `b'=A_p b_c+b_p` for column vectors. `C∘P` is a different ancestry even when complete homogeneous generation bags coincide under word reversal.
- The prototype shape and ambient coordinate space are explicit program data. They are not scalar alphabet values or pixel masks.
- The canonical exact profile uses rationals; algebraic coefficients and explicit finite-precision decimals are separate scalar profiles. Approximate values carry precision/rounding provenance and never participate in tolerance-based semantic equality.
- A rule row has stable child slots and may retain authored order for a reference enumeration, but geometric state and evolution are invariant under permutation. Duplicate transforms remain duplicate slots and create multiplicity.
- The strict fractal profile validates one nonempty seed and at least two contractive child placements. Empty output/deletion is not inferred; T15 remains responsible for creation-destruction semantics.
- The affine profile and nonlinear branched-point profile share only typed all-occurrence expansion and bag union. A generic transform callback would erase their distinct value/evaluation algebras.
- The Notes center recurrence is a differential oracle for canonical snapshots up to reference ordering/path reversal. It is not the production state contract.
- Overlap, intersection area, union, occlusion, antialiasing, viewport, and crop are observations. No overlap query is needed to advance.
- Nonempty canonical programs always advance and have no intrinsic halt. Requested depth/horizon, analytical convergence, rendering cutoff, undefined nonlinear map, numeric failure, and cancellation remain distinct.

## Big Picture Objective

Reconstruct geometric replacement/fractal systems as native finite-generation geometry: placed primitive occurrences, exact/declared numeric domains, parent-local transform composition, all-occurrence source coverage, multiplicity-preserving commit, overlap independence, seeds, variants, and limit observations. Determine the smallest honest reuse beyond T13/T20 while excluding lattice/raster packing, transform callbacks, hidden scene engines, float tolerance, fixed canvases, random IFS shortcuts, and family dispatch.

## Catalog Identity

- Stable ID: T27.
- Exact name: Geometric Replacement And Fractal Systems.
- CSV provenance: `ref/notes/CA-Types.csv:28`; taxonomy provenance: `ref/notes/CA-Types.md:737-758`.
- Canonical name: geometrical substitution systems; related standard term: iterated function systems.
- Entry kind: deterministic full-generation geometric replacement construction. “Fractal” primarily describes its nested patterns and limits rather than another executor.
- Native profiles: oriented-square similarity replacement; finite affine-map replacement in arbitrary dimension; explicitly branched complex point maps.
- Search vocabulary: geometric/geometrical substitution/replacement/system/rule; fractal/nested/self-similar; IFS; affine/linear/complex transformation/map; Möbius/fractional-linear/modular; Julia/Mandelbrot; similarity/scale/translate/rotate/reflect/skew; square/orientation/overlap; complex base/digit; C/dragon/Koch/space-filling curve; dimension/box count/multifractal; parameter space; visualization; exact implementation and Index routes.

## Search Log

1. Verified CSV line 28 and read the complete taxonomy section. The taxonomy supplied vocabulary only.
2. Exact `geometric/geometrical substitution system(s)` searches found four occurrences on four monolith lines: two pre-Index and two actual-Index routes. The sparse canonical wording required mechanism and alias expansion.
3. The combined family regex covering geometric substitution, iterated function systems, affine transformations, complex maps, fractals/dimensions, Möbius, Julia, and Mandelbrot found 129 occurrences on 88 lines: 89/59 before the Index and 40/29 in it. Every line was dispositioned.
4. Component audits found `iterated function system(s)` 3/3 occurrences/lines, `affine transformations` 5/2, `complex maps` 5/5, and `fractal(s)` 88/69. Broad fractal matches were classified rather than treated as one construction.
5. Inspected the Chapter 5 core `BOOK:2308-2366`; native T27 mechanics are `2326-2354`. The grid-aligned predecessor at `2310-2324` remains T26 and the neighbor-dependent successor at `2350-2366` remains T28.
6. Inspected all native original rasters: page-204 trajectory/rule, page-205 overlapping trajectory/rule, page-206 four rules/patterns, and Notes page-948 generation-stack/dimension figures. Image-only arrows and child placements establish orientation, child cardinality, overlap, and seed/step convention.
7. Recovered the complete page-189/page-190/page-191(a-d) affine triples from the official primary image source. This repairs the complete absence of page-191(d) from Markdown and preserves approximate coefficients as approximate rather than inventing exact forms.
8. Read the complete Notes neighborhood `BOOK:13681-13812`, with native/close T27 material `13758-13804`: implementation, complex digits, visualization, parameter spaces, affine and nonlinear variants, dimensions, history, and Julia/Mandelbrot relations.
9. Verified split files. `CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:165-217` is the cleaner core duplicate. `BACK-MATTER/Index/Index.md:1582-1713` is actually a Notes duplicate; `BACK-MATTER/Notes/Notes.md` is unusable. Canonical provenance remains the monolith.
10. Resolved the OCR-interleaved alphabetic Index against the official per-letter primary index. The direct hub routes to pages 189-192, implementation 933, and visualization 933. C/dragon/Koch curves, IFS, L systems, affine/complex maps, dimensions, and the umbrella substitution entry were all followed.
11. Followed related routes to page-892 paths/paperfolding, page-893 substitution history, page-921 iterated maps, pages 400-407/1005 plants and parameter ensembles, higher-dimensional substitution, and T28. They establish compilers/applications/boundaries, not new base mechanics.
12. Repaired crushed one-line Notes formulas, imaginary-unit OCR, local Index columns, and the page-break split at `2334` from clean split/official sources. T26-adjacent implementation corruptions were logged but excluded.
13. Excluded CA/rule-90, fluid, landscape, financial, network, art, and biological uses of “fractal” unless they supplied a direct relation. Chaos-game random sampling is not the documented all-branches IFS executor.
14. All direct names, aliases, figures, Notes, Index endpoints, splits, history, affine/nonlinear variants, observers, and relations are dispositioned. Zero native rules or semantic questions remain unresolved.

## Book Excerpts

`BOOK` below means `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`. These 18 groups capture every unique material passage; split duplicates are logged above.

### E01 — Grid subdivision is the predecessor, not free geometry

- Provenance: `BOOK:2308-2324`, Chapter 5, “Substitution Systems and Fractals.”
- Fact: grid-aligned 2D substitution replaces every square by smaller grid squares and produces nested structure. This motivates T27 but remains T26 because grid position/orientation is fixed.

### E02 — No rigid grid, single-square seed, and orientation

- Provenance: `BOOK:2326-2332`, page-204 trajectory/rule rasters.
- Fact: a simple geometrical rule starts from one black square and replaces every square by two smaller squares. Applying the rule must account for each parent's orientation.

### E03 — Overlap persists without interaction

- Provenance: `BOOK:2334-2344`, page-205 trajectory/rule rasters.
- Fact: free geometric descendants may overlap even when the immediate rule children do not. The pattern is still evolved by the same replacement and remains nested; no collision, union, or blocking rule is introduced.

### E04 — Exact rule family and independent nested behavior

- Provenance: `BOOK:2346-2354`, page-206 four-rule raster/caption.
- Fact: all rules replace one black square by two or more smaller oriented squares; page-191(a-c) have two child slots and (d) has three. Twelve displayed generations remain nested precisely because a parent's rule does not depend on other elements.

### E05 — Neighbor dependence requires a different grid construction

- Provenance: `BOOK:2350-2366`.
- Fact: off-grid elements can occur anywhere, so there is no obvious neighbor notion. Interaction is introduced only on a grid and produces non-purely-nested behavior; this is T28, not a T27 overlap policy.

### E06 — Geometry remains a plane; network layout is different

- Provenance: `BOOK:2380-2394`.
- Fact: geometrical replacement has more freedom than a regular array but retains a fixed plane. Network systems remove fixed geometric layout entirely, establishing the T29 boundary.

### E07 — Paths, paperfolding, dragon curves, and space filling

- Provenance: `BOOK:12218-12259`.
- Fact: paths from 1D substitution sequences can be represented by 2D geometrical systems. Lévy C/dragon and Peano/Hilbert curves are representation/compiler/history relations, not an ordered-string state inside T27.

### E08 — Dragon-curve property

- Provenance: `BOOK:13758`.
- Fact: the page-189 pattern has paperfolding and complex-base descriptions, and its boundary has a stated fractal dimension. These are derived properties.

### E09 — Exact reference implementation and affine formulas

- Provenance: `BOOK:13760-13762`.
- Fact: a pattern is conveniently projected to a complex-center list and evolved by `Nest[Flatten[f[#]] &, {0}, n]`. Page 189 uses `(1-i)/2 {z+1/2,z-1/2}`; page 190 uses `(1-i)/2 {iz+1/2,z-1/2}`; page-191(a-c) formulas are also supplied, some explicitly numerical.

### E10 — Complex-digit representation

- Provenance: `BOOK:13764-13768`.
- Fact: page-189 generation `t` equals all `t`-digit base-`i-1` values with digits 0/1. This is an exact alternative enumeration/codec, not numeric native state for general oriented instances.

### E11 — Generation-stack visualization and parameter ensembles

- Provenance: `BOOK:13770-13774`, page-948 stack raster.
- Fact: 3D pictures stack successive 2D generations; parameter-space sets vary geometric programs. Both are downstream views/ensembles.

### E12 — General affine and higher-dimensional variant

- Provenance: `BOOK:13775`.
- Fact: finite affine maps `v -> Mv+b` generate nested patterns; complex linear maps cover rotation, translation, and rescaling, while general matrices add reflection/skew and arbitrary dimension.

### E13 — Nonlinear complex branch-map variant

- Provenance: `BOOK:13777`.
- Fact: finite Möbius-map sets and the two inverse-square-root branches `{Sqrt[z-c],-Sqrt[z-c]}` generate nested point patterns. These are closed point maps, not affine rigid-square transformations.

### E14 — Fractal dimension and stronger descriptors are observers

- Provenance: `BOOK:13778-13784`, page-948 grid raster.
- Fact: box-count scaling defines a dimension when it converges; more complex patterns may fluctuate and formal variants can be noncomputable. Moment-based descriptors generalize dimension. None advances a generation.

### E15 — History of fractals

- Provenance: `BOOK:13786`.
- Fact: the Notes trace nested art, Riemann/Weierstrass, Koch, Sierpiński, Menger, Lévy, 1960s graphics, Mandelbrot, and multifractals. History supplies aliases/examples, not extra state.

### E16 — Julia inverse branches and Mandelbrot parameter set

- Provenance: `BOOK:13788-13804`.
- Fact: iterating both inverse quadratic branches from a point yields Julia patterns. The Mandelbrot set instead filters parameters by connectivity/bounded forward behavior; it is an ensemble/analysis relation.

### E17 — IFS plant-rendering relation

- Provenance: `BOOK:15796-15804`.
- Fact: Barnsley used iterated function systems for fern pictures, alongside L-system plant models. These are applications; random chaos-game sampling is not specified as the T27 transition.

### E18 — Exhaustive Index hub

- Provenance: actual merged Index routes at `BOOK:21213`, `21360`, and `22144`, resolved against the official primary index.
- Fact: the Index routes geometrical systems to pages 189-192 and Notes 933, and separately routes curves, IFS, affine maps, dimensions, plants, iterated maps, and neighboring substitution types. Every endpoint above is dispositioned.
