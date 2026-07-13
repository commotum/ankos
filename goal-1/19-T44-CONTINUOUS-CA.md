# 19-T44-CONTINUOUS-CA

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T44, CSV line 45, `Continuous Cellular Automata`; taxonomy vocabulary is `ref/notes/CA-Types.md:1215-1245`. T45 begins at taxonomy line 1247.
- Canonical strict main `Continuous Cellular Automata` is `BOOK:1948-2014`; T45 begins at `2016`. The clean chapter duplicate is `Systems-Based-on-Numbers.md:405-471`, with T45 at 473.
- Native Notes are `BOOK:13281-13315`; T45 Notes begin at `13316`. The useful line-oriented duplicate is `BACK-MATTER/Index/Index.md:1184-1217`, with T45 at 1219. The actual Index begins at `BOOK:20826`.
- The strict construction is a fixed one-dimensional lattice with a gray value at every cell and discrete synchronous time. Each event reads the old left/self/right values, forms their average, applies one fixed scalar mapping, and assigns the result to the same cell in parallel.
- Strict value language is continuous gray from white `0` through black `1`. This is a real interval, not a finite float alphabet or a rendered gray palette.
- The three strict map profiles are identity on the average, `FractionalPart[3 average/2]`, and `FractionalPart[average+c]`; the displayed additive family includes exact `c=1/4` and a parameter gallery.
- The average-only profile is linear diffusion. The `3/2` profile composes T44 neighborhood aggregation with T43 strict map `(a)`. The constant-add profile has a uniform background `FractionalPart[c t]`, but nonuniform deviations can be complex.
- A single black cell on white background is the strict seed. Program, initial field, boundary/realization, requested horizon, numerical profile, and rendering remain separate.
- Notes implementation maps a scalar function over `(RotateLeft[list]+list+RotateRight[list])/3` and uses `NestList`, directly supporting old-snapshot averaging, simultaneous assignment, and initial-inclusive traces.
- `RotateLeft`/`RotateRight` implements a finite periodic-list realization. Whether the strict native figures instead denote the ordinary infinite line with a finite crop/light cone must be resolved from rasters and CA context rather than silently inferred from the implementation helper.
- T01 already establishes fixed-lattice all-site old-snapshot reads and atomic parallel assignment. T44 appears to reuse that public update law with exact/declared real values, a closed aggregate-plus-map rule, and a new continuous value carrier; no new update law is presumed.
- T43 supplies reusable scalar map-expression and numerical-realization responsibilities, but T44 is not a packed collection of independent T43 states: every new cell value depends on a neighborhood aggregate.
- Native Notes state that exact rationals are essential for detailed profiles: ordinary 64-bit double precision makes the lower page-157 pattern qualitatively wrong and nearly every page-160 parameter panel wrong. Numerical realization therefore affects feedback semantics over the whole field.
- The strict source exposes a potential two-level realization identity: the ideal exact field construction and a fully declared finite-arithmetic field recurrence. T43's ideal/tracked/fixed distinction must be lifted without conflating cell values, computation work state, or rendered gray levels.
- The `c=1/4` background repeats every four events. Notes generalize this to rational `c`, with period equal to the reduced denominator; irrational `c` never repeats. Background periodicity is an observer/property, not a native halt.
- Notes add an additive profile `Mod[RotateLeft[list]+RotateRight[list],1]`. With a single nonzero value `1/k`, it relates coefficients to Pascal's triangle and finite versus equidistributed value sets. The displayed formula/text's exact normalization and possible reciprocal/modulus defect are under audit.
- Parameter scans, center-cell plots, background plots, adjacent-cell differences, localized-structure views, value equality, and pattern classes are observers. The page-175 difference image cannot replace the underlying field.
- Coupled map lattices/lattice dynamical systems are a historical related family. Probabilistic cellular automata are explicitly an alternative discrete-value stochastic construction, not a T44 flag.
- T45 removes discrete cells and discrete time and must remain a distinct continuous-space/time differential-equation category. A finite-difference approximation or PDE limit is a relation, not T44 native identity.
- Six strict image links and two native-Notes image links are identified. Their dimensions, hashes, grids, constants, horizons, exact pixels, source repairs, and missing/cropped status are under parallel audit.
- Current finite lattice selectors and parallel assignment are closer to T44 than to T43, but current alphabets discretize floats, current rules admit callbacks, current rollout uses family branches/NumPy rounding, and current exporters treat arrays/renders as the public result. Exact continuous-field semantics are absent.

## Updated Assumptions

- Strict ideal state is a total field from a declared 1D lattice support into exact/certified values in `[0,1]`, with no control or stored history.
- A finite periodic list, a finite open segment, an infinite line with finite-support/default presentation, a causal window, and a rendered crop are distinct realizations/scopes.
- `AllSites` is the active source. Each site reads the complete ordered old triple `(left,self,right)`, computes an exact average, applies one closed scalar expression, and returns a typed same-site assignment. All results commit atomically.
- Aggregation order, rational divisor `3`, map expression, exact parameter, interval/endpoints, boundary, and numeric realization are reproducible data. They are not a formula callback or backend default.
- Source-spelled `FractionalPart` retains the T43/Wolfram `x-IntegerPart[x]` semantics. Strict aggregate/map arguments are nonnegative, where it agrees with modulo one; the additive Notes profile explicitly uses `Mod[...,1]` and remains a distinct primitive.
- Ideal exact field state, certified/tracked computation state, and fixed represented field state remain different. Per-operation rounding locations include addition, division/average, map arithmetic, comparison, and assignment.
- An unchanged field still represents a completed event. Diffusive convergence, exact background periods, repeated finite realizations, localized structures, and observer horizons do not halt the base construction.
- A complete run with `h` events has `h+1` field snapshots. Compact events may reconstruct fields, but a bitmap/float tensor is not the semantic codec.
- Exact field equality, realized-field equality, translational equivalence, observer equality, and visual equality are distinct.
- Parameter-family scans execute separately identified rules/runs. The parameter coordinate is not hidden control and a gallery is not one evolving field.
- Additive, coupled-map, stochastic, PDE-limit, higher-dimensional, alternate-neighborhood, weighted-average, and asynchronous profiles will be admitted only to the extent supported by evidence.

## Big Picture Objective

Reconstruct continuous cellular automata as exact or explicitly represented continuous-valued lattice evolution: fixed support, old-neighborhood aggregate, closed scalar map, parallel same-site commit, explicit boundary/seed/numerical realization, exact figures and parameter profiles, observer boundaries, T01/T43 composition, and the smallest honest Goal 2 extension without finite-float alphabets, callbacks, or a continuous-CA rollout branch.

## Catalog Identity

- Stable ID: T44.
- Exact CSV name: `Continuous Cellular Automata` at `ref/notes/CA-Types.csv:45`.
- Taxonomy vocabulary: `ref/notes/CA-Types.md:1215-1245`; search seed only.
- Canonical strict main: `BOOK:1948-2014`; clean duplicate `Systems-Based-on-Numbers.md:405-471`.
- Native Notes: `BOOK:13281-13315`; line-oriented duplicate `BACK-MATTER/Index/Index.md:1184-1217`.
- Entry kind: synchronous one-dimensional continuous-valued lattice transition construction with neighborhood aggregation followed by a scalar map.
- Strict profiles: mean/diffusion; fractional `3/2` mean; fractional mean-plus-constant family; single-black-cell seed; value/difference/parameter observers.
- Supplementary profiles: additive modulo-one rules, exact/approximate realizations, coupled map lattices, finite periodic implementation, irrational parameters, and PDE/probabilistic relations.
- Aliases/routes under audit: continuous cellular automata, continuous-valued/real-valued CA, coupled map lattices, lattice dynamical systems, analog CA, additive continuous rules, gray-level automata, diffusion/averaging CA, Kaneko lattices, local maps, totalistic continuous rules, and finite-difference relations.

## Search Log

1. Read CSV line 45, taxonomy section 44, strict main through the T45 boundary, clean chapter duplicate, native Notes through the T45 Notes boundary, line-oriented duplicate, and the initial source/asset inventory.
2. Confirmed exact boundaries and started independent exhaustive text/Index/history, strict/Notes raster/oracle, and architecture/API/runtime audits.
3. Direct names, aliases, aggregation/map formulas, precision vocabulary, boundaries, parameter families, additive/Pascal profiles, coupled-map/probabilistic/PDE relations, and false positives are in progress.

## Book Excerpts

Canonical excerpt groups are under audit.

## Construction Model

The audit must resolve independently:

1. native lattice support versus finite periodic/open/infinite/default/crop realizations;
2. exact/certified/represented `[0,1]` field values, seeds, equality, and serialization;
3. `AllSites`, ordered radius-one old reads, exact mean reducer, closed scalar map, typed assignment, and parallel commit;
4. boundary, endpoints, fractional/modulo semantics, numeric rounding/uncertainty, failure, interruption, and trace outcomes;
5. parameter-family identity, background periods, additive profiles, compact reconstruction, and reproducible presets;
6. value/difference/center/background/parameter/localized-structure observers;
7. T01/T03/T04/T05/T43/T45, coupled maps, probabilistic CA, finite differences, and implementation-helper boundaries.

## Exact Book Presets and Oracles

Pages 171/172/173/174/175 and Notes page 937 assets, exact tables, rational horizons, parameter grids, hashes, pixel classifiers, and declared limitations are under reconstruction.

## Variants, Relations, and Boundaries

T01 fixed lattice assignment, totalistic aggregation, T43 scalar maps/realizations, additive modulo-one rules, coupled-map lattices, probabilistic alternatives, and T45 PDE limits are under audit for exact reuse versus explicit sibling status.

## Current API Fit

In progress.

## Current Runtime Fit

In progress.

## Principles Audit

The smallest current hypothesis composes T01's all-site old-snapshot parallel assignment with an exact mean reducer and T43's closed scalar-map/numerical-realization discipline. It must not replace continuous values with a finite float alphabet, hide exactness inside NumPy, treat periodic helper boundaries as native without evidence, or fuse observer galleries into state.

## Detailed Implementation Plan

1. Complete strict main/raster, Notes, actual Index, split, history, alias, variant, relation, program, and false-positive searches.
2. Decode every rule, seed, support/boundary, horizon, constant, color/difference convention, precision warning, and source defect; regenerate exact or declared oracles.
3. Derive ideal/realized field state, source/read/aggregate/map/result/update, numerical profiles, outcomes, equality, codecs, traces, and observers from evidence.
4. Resolve T01/T43 primitive reuse and T03/T04/T05/T45/additive/coupled/probabilistic boundaries without flags or family dispatch.
5. Audit current API/runtime/tests and write an implementation-ready Goal 2 handoff.
6. Integrate global artifacts and run source/oracle, hash, Markdown, coverage, diff, and repository verification before closure.

## Goal 2 Implementation Stage

Pending the evidence audit.

## No-Cheating Checks

The final stage must reject float-range alphabets as the continuum, opaque aggregate/map callbacks, NumPy arrays as exact field state, hidden periodic boundaries, hidden precision/rounding, render pixels as values, parameter galleries as one run, T43 scalar packing, observer-fed differences, PDE discretizations presented as PDE identity, probabilistic rules hidden as numerical noise, and a T44-specific rollout branch.

## Completion Requirements

- [ ] Every strict main/Notes/actual-Index/split passage, history item, alias, figure, program, variant, relation, and false positive is dispositioned.
- [ ] Support/value/control, source/read/aggregate/map/result/update, boundary/seed, precision/outcome, equality/serialization, trace, and observer semantics are explicit.
- [ ] All six strict and two Notes assets have source-permitted exact or declared oracles, hashes, measurements, and source repairs.
- [ ] T01/totalistic/T43/additive/coupled/probabilistic/T45 boundaries and reuse are explicit.
- [ ] Current API/runtime fit, Goal 2 files/dependencies/tests, global ledgers, diff checks, and repository tests are integrated.

## Stage Results

In progress.

## Integration Results

In progress.
