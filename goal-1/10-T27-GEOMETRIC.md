# 10-T27-GEOMETRIC

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T27, CSV line 28, `Geometric Replacement And Fractal Systems`; taxonomy seed `ref/notes/CA-Types.md:737-758`.
- The likely canonical book name is “geometrical substitution systems,” with main text around page 189 and Notes around page 933. Exact aliases and scope are under audit.
- The taxonomy hypothesis is a collection of geometric objects replaced by transformed descendants without a required lattice. It mentions scale, translation, rotation, reflection, possible overlap, and rendering depth, but none is accepted until canonical evidence fixes the construction.
- Main-text candidate lines `BOOK:2316-2334` distinguish grid-aligned two-dimensional substitution from geometrical rules that replace each square with smaller squares and may allow overlap.
- Notes candidate lines `BOOK:13770-13777` mention geometric-system visualization, affine maps, rotations/translations/rescalings, reflection/skew, arbitrary dimensions, and nonlinear complex maps. Native versus variant scope remains unresolved.
- T13 supplies full-generation replacement and lineage over a discrete ordered sequence; T20 supplies immutable tree structure and transform-like descendant provenance only conceptually. Neither yet represents embedded geometry, affine frames, shape instances, overlap multiplicity, or coordinate/numeric fidelity.
- Current `src/ca/seeds.py` has geometric-looking seed and predicate callbacks, while the dense runtime has fixed coordinate arrays. These are current mechanisms to audit, not proof of native geometric replacement.
- Whether state is a multiset of independently transformed primitive instances, a geometric union/set, a scene graph, a point set, or merely the limiting fractal is the central unresolved question.

## Updated Assumptions

- Geometry that determines future child placement, orientation, scale, or reflection is semantic state/program data, not visualization metadata.
- Parent-local transforms and their composition order must be explicit. Applying a child transform in world coordinates versus the parent's local frame generally gives different successors.
- Coincident or overlapping objects must retain whatever multiplicity, identity, occlusion, union, or merge semantics the construction requires. A renderer's paint order cannot silently choose.
- Exact affine or complex coefficients should remain inspectable values. Floating-point approximations, raster pixels, and bounded canvases are realizations unless the book makes them native.
- Every old object may fire once from the same snapshot, suggesting potential reuse of T13 full-generation coverage and lineage. Reuse cannot be declared until the output carrier, child ordering, and overlap law are reconstructed.
- A finite-depth picture, infinite limiting set, fractal dimension, bounding box, and three-dimensional visualization are distinct from the stepwise state unless evidence couples them.
- Shape type, embedded transform/frame, stable occurrence identity, parent/child lineage, layer/multiplicity, and any global normalization required to advance must be Markov-visible.

## Big Picture Objective

Exhaustively reconstruct geometric replacement/fractal systems: native object and coordinate carriers, primitive shapes, local/world transforms, composition, replacement coverage, child order or multiplicity, overlap, exact numeric domain, seed, step and limit semantics, variants, observers, and relations. Determine the smallest honest reuse or extension beyond T13/T20 without rasterization, lattice packing, coordinate callbacks, fixed canvases, hidden normalization, or family dispatch.

## Catalog Identity

- Stable ID: T27.
- Exact name: Geometric Replacement And Fractal Systems.
- Entry kind: unresolved pending evidence; expected deterministic full-generation geometric replacement construction plus fractal/limit observations.
- Search vocabulary: geometric/geometrical substitution/replacement/system; two-dimensional substitution; fractal/nested/self-similar; affine/linear/complex transformation/map; iterated function system; similarity; scale/rescale; translate; rotate; reflect; skew; square/triangle/segment/polygon/curve; overlap/intersection/union; local/world coordinates; parent/child; visualization; parameter space; dimension; limiting set; fractal dimension; Lévy C curve/dragon/space-filling curve; exact Notes implementation symbols and Index routes.

## Search Log

In progress. Independent canonical core/figure, Notes/Index/history/variant, and Principle-0/API/runtime/oracle audits are running.

## Book Excerpts

In progress.

## Construction Model

Pending evidence closure. Working questions, not conclusions:

```text
state = finite collection of geometric object instances
program = per-kind finite child transforms/shapes

sources = every old object occurrence
results = transformed child instances in the parent's local frame
next = atomic full-generation replacement
```

Canonical evidence must determine the primitive carrier, transform direction and composition order, whether a child inherits parent shape/style/orientation, whether objects are ordered or form a multiset, whether coincident instances remain distinct, and whether overlap changes future evolution.

## Current API Fit

Pending evidence reconstruction. Expected direct responsibility reuse is immutable program data, visible structured state, old-snapshot full-generation source coverage, typed results, and lineage. Expected mismatches are lattice coordinates, scalar alphabets, writable-target frontiers, scalar rules, fixed-shape traces, formula/predicate callbacks, and geometry treated only as seed/render data.

## Current Runtime Fit

Pending full audit. Current `src/ca` has no inspectable affine transform value, primitive-frame instance, exact composition law, object multiset/source, transformed child result, generation replacement commit, or geometry-preserving ragged trace.

## Principles Audit

Pending evidence closure. Principle 0 must determine whether T13's all-occurrence replacement law generalizes honestly from ordered words to a geometric occurrence collection or whether T27 proves a distinct transform-aware update. No raster/lattice packing, predicate-generated point cloud, hidden scene-graph engine, unrestricted transform callback, float-only coordinates, family rollout, fixed canvas, or limit-set-only substitution is accepted.

## Detailed Implementation Plan

1. Close direct, alias, caption/figure, Notes, actual Index, split, history, implementation, affine/complex/IFS/fractal, overlap, seed, visualization, higher-dimensional, curve, and relation searches.
2. Reconstruct object/shape/coordinate state, transform algebra and composition, source coverage, reads, results, update, multiplicity/overlap, successors, seeds, parameters, variants, observers, and limiting constructions.
3. Compare T27 with T13/T20 and rederive source/read/result/update responsibilities wherever ordering, geometry, transform frames, or overlap prevent honest reuse.
4. Specify exact canonical trajectory and adversarial composition/order/reflection/overlap/coincidence/multiplicity/exactness/lineage invariants with an independent oracle.
5. Write the implementation-ready Goal 2 stage, reintegrate all ledgers, verify, and advance.

## Goal 2 Implementation Stage

Pending evidence closure and fit audit.

## No-Cheating Checks

- No geometric-family rollout, whole-generation callback, host scene/fractal engine, unrestricted transform function, or `Any` object/result.
- No raster, pixel mask, dense lattice, point-cloud sample, SVG path string, image, or scalar code as native state unless a total evidenced lowering preserves all future-relevant distinctions.
- No fixed canvas, depth, object count, coordinate bound, precision, or silent clipping presented as program semantics.
- No hidden parent frames, transform composition order, normalization, deduplication, merge/union, painter order, object identity, or RNG state.
- No float equality, pixel overlap, display resolution, antialiasing, or rendering order deciding semantic overlap.
- No reuse of T13/T20 commits until source coverage, child ordering/multiplicity, geometry, and provenance invariants are proven equivalent.
- No limiting fractal, dimension, bounding box, or visualization substituted for finite step state.

## Completion Requirements

- [ ] All aliases, captions/figures, Notes, actual Index entries, splits, variants, duplicates, and false positives are resolved.
- [ ] Native geometric carrier, transform algebra/order, source coverage, result/update, multiplicity/overlap, seed, successor, and limit/observer boundaries are reconstructed.
- [ ] Exact trajectories and adversarial composition/reflection/overlap/multiplicity/exactness/provenance invariants have independent tests.
- [ ] Current API/runtime/principles fit and T13/T20 reuse/divergence are explicit.
- [ ] Goal 2 implementation/conformance handoff and global reintegration are complete.

## Stage Results

In progress. No T27 architectural conclusion is complete.
