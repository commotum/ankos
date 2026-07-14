# 36-T24-HIGHERDIM-CA

Status: **IN PROGRESS — SOURCE, ASSET, SEMANTIC, AND ARCHITECTURE AUDITS OPEN**

## Current Facts

- T24 is CSV line 25, `Higher-Dimensional Lattice Cellular Automata`. The catalog name is search vocabulary, not a runtime family or executor.
- DOMAIN means the dimensional task/program space. T24 must determine which discrete dimensions and lattice/topology declarations the primary source actually groups here; an array rank, renderer, coordinate tuple, or current API limit is not itself a DOMAIN.
- T21/D127, T22/D128, and T23/D129 establish one branch-free fixed-lattice SimpleProgram event through discrete `t+2D` square and `t+3D` cubic presets. T24 must first test whether dimension, topology, access, and closed RULE data continue to suffice one native event for one generic event.
- The current `src/ca` realization accepts only spatial ranks zero through three. That is an implementation envelope, not evidence that higher-dimensional or alternative-lattice programs need another semantic state class, UPDATE, or executor.
- “Lattice” may denote a support topology or incidence structure different from an orthogonal integer grid. Dimension, native support/topology, coordinate representation, access, finite realization, projection, and rendering must remain separate.
- T23 routes other three-dimensional lattices and arbitrary dimension to this stage. Those controls are search entrances, not conclusions about one undifferentiated family.
- The governing event remains:

  ```text
  active = FRONTIER.select(configuration)
  reads  = NEIGHBORHOOD.read(configuration, active)
  writes = RULE(active, reads)
  next   = UPDATE.apply(configuration, active, writes)
  ```

## Initial Hypotheses to Test

- A regular `Z^d` cellular automaton with finite alphabet, fixed local offsets, all-site selection, one same-site write, and snapshot-parallel commit is expected to parameterize the T01/T21/T23 fixed-lattice preset by dimension and access data only.
- A non-orthogonal lattice may still fit the same event through a typed topology/incidence descriptor and ordered local access. A different coordinate codec or embedding does not justify a new executor when a lossless one-step map carries the complete configuration and rule table.
- A graph presentation is not automatically T29 network evolution. If incidence is fixed and only labels change, it may be a fixed-support configuration representation; structural vertex/edge creation or rerouting would instead require the already evidenced graph-write UPDATE axis.
- Finite fundamental cells, periodic quotients, boundary work regions, sparse carriers, projections, and lower-dimensional slices are candidate representations, realizations, or views. None may silently define the native program.
- Symmetry-reduced, totalistic, outer-totalistic, or named lattice rules are candidate restrictions/representations of complete local maps. Their factor maps must be total and invertible on the declared image.
- No source fact presently justifies a `HigherDimensionalState`, lattice-family control payload, rank-specific UPDATE, catalog dispatch, hidden coordinate flattening, or callback rule.

## Big Picture Objective

Reconstruct higher-dimensional and alternative-lattice cellular automata from primary evidence and identify the smallest faithful composition of DOMAIN, CONFIGURATION topology, ALPHABET, FRONTIER, NEIGHBORHOOD, RULE, and UPDATE. Produce an implementation-ready Goal 2 handoff with concrete one-step counterexamples for any claimed new execution algebra.

## Catalog Identity

- Stable ID: T24.
- Exact catalog name: Higher-Dimensional Lattice Cellular Automata.
- CSV line: 25.
- Taxonomy section: 24.
- Entry kind: source audit open; fixed-support label evolution with dimensional/topological/access parameterization is the initial hypothesis.
- Initial vocabulary: higher-dimensional, arbitrary-dimensional, `d` dimensions, lattice cellular automata, crystal lattice, cubic, tetrahedral, rhombic, close-packed, honeycomb, triangular, hexagonal, face-centered, body-centered, neighbors, tilings, tessellations, Notes implementations, captions, actual Index, projections, slices, and embeddings.

## First-Principles Fit Standard

The `src/ca` namespace and its rank-three tensor realization are not the semantic boundary. Every T24 finding must be classified as:

1. direct reuse of an existing construction;
2. a parameterization, restriction, preset, invariant, or named role;
3. a lossless tagged/product/coordinate/topology/table representation of an existing construction;
4. or a genuinely different execution algebra justified by a concrete one-step counterexample.

A proposed representation must supply a lossless map `e` satisfying `e(step_A(s)) = step_B(e(s))` one native event for one generic event, preserving complete state, topology, outcomes, and rule identity without hidden interpretation or microsteps.

## Audit Questions

1. Which source lines define the native dimensions, support/topology, label schema, firing loci, access relation, rule result, and update schedule?
2. Does “higher-dimensional lattice” join arbitrary dimension, alternative lattice incidence, or both, and which examples are strict construction evidence rather than relations or views?
3. Can every fixed-incidence example use `AllSites`, declared old-snapshot reads, one same-site label write, and snapshot-parallel UPDATE?
4. Which coordinate systems are native addresses, which are lossless representations, and which are geometric embeddings or render-only projections?
5. Do periodic cells, finite boxes, sparse backgrounds, slices, or displayed shapes change native support, or are they realizations/representations/views?
6. Which compact count/symmetry schemas factor complete local tables exactly, and what ordering or multiplicity is lost by current runtime summaries?
7. Does any example structurally change incidence, successor cardinality, or schedule, thereby requiring an existing different UPDATE implementation or a concrete new one?
8. Can T21, T22, T23, and strict T24 examples execute through the identical generic step function with only dimension, topology, access, and RULE data changed?

## Detailed Implementation Plan

1. Freeze a zero-remainder source query union across the monolith, Notes, actual Index, split corpus, Atlas, catalog, and taxonomy; partition native, relation, control, exclusion, and governed continuation evidence.
2. Derive a source-bound asset candidate universe and bind every governed or adjacency-only plate to source lines and physical hashes without inventing pixel, coordinate, seed, or stochastic replay.
3. Build independent native/generic semantic oracles for each strict dimension/topology/access/RULE profile, including coordinate/table maps, quotient multiplicity, finite realization boundaries, and old-snapshot update.
4. Audit `simple_programs.md`, current `src/ca` modules/tests, D004-D008, D111-D129, and the broader SimpleProgram axes from first principles.
5. Add a decision only if evidence establishes a new parameterization/representation boundary or supplies a concrete category-4 counterexample.
6. Obtain independent hostile review; run root/relocated/optimized/import/compile/Markdown/diff/scope/status/test gates; integrate the plan, evidence index, design ledger, architecture audit, and Goal 2 handoff.

## No-Cheating Checks

- No `higher_dimensional`, lattice-name, rank, or T24 rollout branch or executor.
- No flattening, opaque packing, callback, hidden topology, hidden boundary, or display embedding accepted as a native one-step representation.
- No coordinate deduplication after quotient aliasing unless the source access is itself set-valued rather than occurrence-valued.
- No finite tensor, crop, slice, projection, density, shape, palette, or raster promoted into native program identity without source evidence.
- No fixed-incidence label evolution conflated with T29 structural graph rewriting, and no graph spelling rejected merely because it is not a dense tensor.
- No compact count or symmetry table accepted as a complete positional rule without a validated constant-fiber proof.
- No arbitrary CA encodability substituted for native one-event reuse.

## Completion Requirements

- [ ] Exhaustive source/split/Notes/Index/alias audit closes with zero unresolved candidates.
- [ ] The source-bound asset candidate universe closes with honest claim boundaries.
- [ ] Every strict dimensional/topological/access/RULE profile and required representation map is independently proven.
- [ ] Smallest reusable bases are classified with a concrete-counterexample gate for every claimed new algebra.
- [ ] Current API/runtime/principles audit and Goal 2 handoff are implementation-ready.
- [ ] Independent hostile review and all oracle/test/Markdown/diff/scope/coverage gates pass.
- [ ] `0-plan.md`, `evidence-index.md`, `design-ledger.md`, and `architecture-audit.md` agree.

## Stage Results

In progress.
