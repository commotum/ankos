# 18-T43-ITERATED-MAPS

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T43, CSV line 44, `Iterated Maps`; taxonomy vocabulary is `ref/notes/CA-Types.md:1184-1213`. T44 begins at taxonomy line 1215.
- Canonical strict main `Iterated Maps and the Chaos Phenomenon` is `BOOK:1868-1946`; T44 begins cleanly at `1948`. The clean chapter duplicate is `CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:327-404`.
- Native Notes are `BOOK:13215-13280`; T44 Notes begin at `13281`. The line-oriented duplicate is `BACK-MATTER/Index/Index.md:1118-1183`.
- The source explicitly defines a transition construction: one number `x` between 0 and 1 is updated at every step by one fixed total self-map of that interval. Unlike T41, argument evaluation is now repeatedly committed as evolving state.
- The strict page-165 raster fixes panel order that surrounding extracted formula lines obscure: (a) `FractionalPart[3x/2]`; (b) `If[x<1/2,3x/2,3(1-x)/2]`; (c) `FractionalPart[3x/4]`; (d) `FractionalPart[2x]`.
- Strict initial conditions are `1/2` and `pi/4`. For `1/2`, (a)/(b) generate complex-looking rational orbits, (c) decays geometrically, and (d) reaches exact zero in one update. For `pi/4`, (d) shifts the exact binary digit sequence rather than intrinsically creating randomness.
- Every strict map is a unary piecewise-linear/fractional-part expression over `[0,1]`. A closed map AST can reuse compatible T41 expression nodes, but T43 adds scalar state, one current-value read, assignment, successors, and orbit traces; a function specification alone is not execution.
- T34 already established unary scalar state and typed scalar assignment. T43 may reuse that update law if exact/declared real values and a richer closed map program preserve the same one-slot replacement semantics; no new update law is presumed.
- Mathematical exact-real state, arbitrary-precision approximation with tracked uncertainty, fixed-precision rounded arithmetic, and interval/certified propagation are different execution profiles. In chaotic cases they can yield different later orbits, so precision policy cannot be incidental metadata.
- Notes explicitly warn that fixed binary precision forces the shift map to zero, fixed decimal representation gives a different eventually repetitive process, and arbitrary-precision significance degrades as unknown initial digits are amplified.
- `FractionalPart[2x]` has exact iterate `FractionalPart[2^n x]`. It exposes initial digits; sensitive dependence is not by itself evidence of intrinsic randomness. Digit rows, size plots, pairwise divergence, Lyapunov exponents, attractors, periods, and bifurcation diagrams are observers of an orbit/program.
- Notes add smooth logistic maps, rational/complex Newton maps, Gauss maps, tent-map closed forms, higher-dimensional Anosov maps, parameter distributions, and bitwise analogs. Their state domains/map algebras and strict-versus-related status are under audit.
- A probable Notes inconsistency is under review: the higher-dimensional paragraph first says rational initial values under an integer matrix are repetitive, then appears to say a rational matrix produces complexity from `{1,1}`. Exact wording, intended repair, and disposition must be resolved before closure.
- Eight strict image links and three native-Notes image links have been identified; original formulas, horizons, pixels, hashes, and independent oracles are under parallel audit.
- Current rank-0 rollout is update-oriented but fixed-width NumPy/family-dispatched and limited to modular integer AR2. It has no closed real-map AST, exact/interval real value, explicit precision/rounding semantics, or digit-sensitive conformance path.

## Updated Assumptions

- Strict T43 state is one domain-tagged exact or explicitly numerical real value plus no hidden history. Program, initial value, numerical profile, requested horizon, and observations remain separate.
- The active source is `UniqueScalar`; it reads the complete old value. A closed unary map expression returns the next typed scalar value, and atomic scalar assignment commits exactly one successor when evaluation succeeds.
- Map validation proves the strict `[0,1] -> [0,1]` contract for the declared parameter/domain or requires an explicit partial/escape profile. Out-of-domain, nonfinite, evaluation-failure, and unresolved-uncertainty outcomes are typed. A declared discontinuity is not itself a failure.
- The piecewise boundary convention at `x=1/2`, `FractionalPart` value at integers, interval endpoint convention, and exact parameter values are semantic program data. One-sided derivative/sampling metadata remains an observer concern; the strict tent map is continuous at its cusp.
- Exact rational/algebraic/named-real values, symbolic exact expressions, certified intervals, arbitrary-precision decimals, and fixed-precision machine values remain distinguishable in state and serialization.
- Fixed-precision execution is a different declared numerical realization, not a transparent implementation of the exact orbit. Rounding base/mode/width and unknown-digit fill policy must be reproducible.
- Orbit state/effects remain separate from digit/sizes/difference/period/attractor/bifurcation/Lyapunov observers and from solver/fast-forward formulas.
- Smooth, discontinuous, piecewise, higher-dimensional, complex, bitwise, stochastic/noisy, and continuous-CA uses will share only responsibilities justified by evidence; they will not be hidden behind flags in one permissive callback map.

## Big Picture Objective

Reconstruct iterated maps as exact or explicitly numerical scalar-state evolution under a fixed closed self-map. Pin down state/domain/value carriers, piecewise/fractional/smooth map syntax, update and failure semantics, precision/rounding/uncertainty, orbit equality and traces, digit-sensitive randomness distinctions, strict figures and exact oracles, observer boundaries, related map profiles, and the smallest coherent Goal 2 extension of T34/T41 without callbacks or family dispatch.

## Catalog Identity

- Stable ID: T43.
- Exact CSV name: `Iterated Maps` at `ref/notes/CA-Types.csv:44`.
- Taxonomy vocabulary: `ref/notes/CA-Types.md:1184-1213`; search seed only.
- Canonical strict main: `BOOK:1868-1946`; clean split `Systems-Based-on-Numbers.md:327-404`.
- Native Notes: `BOOK:13215-13280`; T44 Notes begin at `13281`.
- Entry kind: unary continuous-state transition construction with strict piecewise-linear/fractional maps; smooth, complex, vector, and numerical-realization variants require explicit profiles.
- Strict parameters: invariant interval `[0,1]`, four fixed maps, initial values `1/2` and `pi/4`, digit base 2 observer, and small-initial-change comparisons.
- Aliases/routes under audit: iterated maps/functions, iteration theory, chaos/chaos phenomenon, shift/tent/logistic/Gauss/Anosov/Newton maps, sensitive dependence, Lyapunov exponent, attractor, period doubling, bifurcation, symbolic dynamics, return maps, and dynamical systems.

## Search Log

1. Read the catalog/taxonomy seed, strict main through the T44 boundary, native Notes through the T44 Notes boundary, clean splits, and initial strict raster at original resolution.
2. Confirmed exact boundaries and opened parallel exhaustive text/Index/history, strict/Notes figure/oracle, and architecture/API/runtime audits.
3. Direct names, aliases, map formulas, iteration/update terms, chaos/sensitivity/precision/digit vocabulary, observers, related higher-dimensional/complex/smooth profiles, and false positives are in progress.

## Book Excerpts

Canonical excerpt groups are under audit.

## Construction Model

The audit must resolve independently:

1. exact/declared real scalar state and invariant domain;
2. fixed closed unary map program, old-value read, typed next-value result, and scalar assignment;
3. piecewise-boundary, fractional-part, discontinuity, partiality, escape, and evaluation-failure semantics;
4. exact symbolic/rational versus arbitrary/fixed/certified numerical execution and reproducible serialization;
5. orbit snapshots/events, compact reconstruction, equality, period/cycle, and interruption outcomes;
6. digit, size, divergence, entropy/randomness, Lyapunov, attractor, bifurcation, and parameter-scan observers;
7. related smooth, complex, vector, Newton/Gauss/Anosov/logistic/bitwise maps and T34/T35/T36/T37/T41/T44/T45 boundaries.

## Exact Book Presets and Oracles

Page-165/166 four-map profiles, page-168 perturbation comparison, page-170 digit differences, Notes finite-precision simulations, logistic map, all raster identities, and exact or declared-precision anchors are under reconstruction.

## Variants, Relations, and Boundaries

T34 exact arithmetic iteration, T35 piecewise integer maps, T36 digit reversal, T37 recursive prefixes, T41 function definitions, T44 continuous CA, T45 differential equations, exact fast-forward formulas, and numerical chaos diagnostics are under audit as reusable semantics, distinct state profiles, observers, or solvers.

## Current API Fit

In progress.

## Current Runtime Fit

In progress.

## Principles Audit

The strict source is a genuine scalar transition and should reuse T34's typed assignment if its preservation law remains unchanged. The map must nevertheless be closed inspectable data, and continuous-state precision cannot be hidden inside NumPy or a callback. No new update law, real-number representation, higher-dimensional generalization, or observer is accepted until the evidence audit closes it.

## Detailed Implementation Plan

1. Complete strict main/raster, Notes, actual Index, split, history, program, alias, variant, cross-reference, and false-positive searches.
2. Decode every strict map, parameter, initial value, horizon, digit/plot convention, perturbation, and source repair; regenerate exact or declared-precision oracles.
3. Derive state/domain/value, map AST, source/read/result/update, precision, outcomes, equality, serialization, orbit trace, and observer categories from evidence.
4. Separate T34/T35/T36/T37/T41/T44/T45, analytic fast-forward, parameter scans, and implementation work traces.
5. Audit current API/runtime/tests and write an implementation-ready Goal 2 handoff without callbacks, fixed precision masquerading as exactness, or a T43 rollout branch.
6. Integrate global artifacts and run source/oracle, hash, fence, coverage, diff, and repository verification before closure.

## Goal 2 Implementation Stage

Pending the evidence audit.

## No-Cheating Checks

The final stage must reject unrestricted map callbacks, `eval`/formula strings, opaque host numeric/symbolic objects, binary-float coercion of exact seeds, hidden precision/fill/rounding, finite digit arrays as exact reals, digit rasters as state, argument evaluation without committed orbit state, analytic iterate formulas substituted for a requested step trace, cycle/zero detection as native halt, observer-fed updates, higher-dimensional maps packed into one scalar, and family-specific rollout dispatch.

## Completion Requirements

- [ ] Every strict figure, main/Notes/actual-Index/split passage, history item, alias, map variant, program, and relation candidate is dispositioned.
- [ ] State/domain/value, closed map syntax, source/read/result/update, precision/rounding/uncertainty, failure/outcome, equality/serialization, trace, and observation semantics are explicit.
- [ ] Page-165/166/168/170 and Notes profiles have exact or declared-precision independent oracles, hashes, and source repairs.
- [ ] T34/T35/T36/T37/T41/T44/T45, fast-forward formulas, smooth/complex/vector maps, sampling, and observer boundaries are explicit.
- [ ] Current API/runtime fit, Goal 2 files/dependencies/tests, global ledgers, diff checks, and repository tests are integrated.

## Stage Results

In progress.

## Integration Results

In progress.
