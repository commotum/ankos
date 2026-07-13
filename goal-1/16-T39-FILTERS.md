# 16-T39-FILTERS

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T39, CSV line 40, `Number-Theoretic Filtering Systems`; taxonomy vocabulary at `ref/notes/CA-Types.md:1071-1102`.
- Canonical main section `The Sequence of Primes` is `BOOK:1619-1663`; T40 `Mathematical Constants` begins cleanly at `BOOK:1665`.
- The strict constructive example starts from candidate integers, repeatedly removes larger candidates divisible by a stage integer, and identifies the limiting survivors with primes. `_page_147_Figure_4.jpeg` shows the finite `1..100` realization.
- The prose/caption starts the displayed range at `1`, while standard primality excludes `1`. Whether the raster separately removes/marks `1`, the text is using a display convention, or the “exactly primes” sentence is imprecise is under explicit audit.
- The sieve's evolving survivor/removal masks, its eventual prime set, the increasing prime sequence, primality of one queried integer, and a plotted statistic of primes are different objects and must not be conflated.
- Page 148 presents six derived features/statistics of the prime sequence. Page 150 presents five number-theoretic measurement sequences, including divisor/representation counts. They are not automatically transition states merely because they are indexed by integers.
- A finite interval sieve, a lazy infinite prime stream, and the mathematical infinite set of primes have different completion and trace semantics. The main figure's range `1..100` is a realization/display scope, not proof of native finite support.
- T37's Ulam sequence also searches candidates using the accumulated prefix. T39 must determine whether a closed candidate-filter primitive composes honestly with T37 append or whether Ulam needs a broader global-history selection category.
- Current `simple_programs.md` and `src/ca` expose finite alphabets, dense rollout families, formula callbacks, and scalar/temporal transitions, but no evidenced candidate-stream/filter/sieve specification. API/runtime fit is under audit.

## Updated Assumptions

- Candidate domain/order, filter stage, active predicate, survivors, newly removed values, previously removed values, and emitted outputs will be explicit.
- A number-theoretic predicate will be closed inspectable data/operations, not `Callable[[int],bool]`, `PrimeQ` hidden behind a boolean, or a trusted precomputed prime table.
- The defining sieve process will not be replaced by direct primality testing when an event trace is requested; direct tests may be analyzers/alternative algorithms with checked output equivalence.
- Removed candidates do not reappear. Whether composite stages are explicit no-op events or skipped by a prime-only stage schedule must come from the figure/Notes rather than convention.
- Finite realization bounds, infinite-domain meaning, stopping after a candidate/prime count, resource limits, and mathematical infinitude will remain distinct.
- Derived number-theoretic sequences may be pure functions/observers instead of mutable filters. Each page-150 row will be classified independently.
- Prime gaps/counting errors/random-walk plots and digit/divisor representations remain observers unless the rule reads them.

## Big Picture Objective

Reconstruct number-theoretic filtering without forcing mathematical sets, finite sieve algorithms, generated streams, and derived measurements into one fake dynamics API. Pin down candidate domains, stage policies, closed predicates, survivor/removal state, finite/infinite realizations, outputs and outcomes, exact figures/statistics, equality/serialization/traces, alternative algorithms, Ulam composition, and the smallest honest Goal 2 integration.

## Catalog Identity

- Stable ID: T39.
- Exact name: Number-Theoretic Filtering Systems.
- CSV provenance: `ref/notes/CA-Types.csv:40`; taxonomy provenance: `ref/notes/CA-Types.md:1071-1102`.
- Canonical strict main: `BOOK:1619-1663`; T40 begins `1665`.
- Entry kind, strict sieve profile, prime-stream relation, measurement profiles, Notes boundary, aliases, and variants are under audit.

## Search Log

1. Verified the catalog/taxonomy identity and read the strict main section through the T40 boundary.
2. Confirmed one prime-sieve figure on page 147, one six-panel prime-feature figure on page 148, and five page-150 number-theoretic sequence images/captions in the scoped main range.
3. Opened parallel exact figure/profile, exhaustive Notes/Index/search, and architecture/runtime audits.
4. Direct terms, aliases, programs, history, sieve variants, primality/factorization relations, observers, and actual Index routes are in progress.

## Book Excerpts

Canonical excerpt groups are under audit.

## Construction Model

The audit must resolve at least three separately typed categories:

1. a mathematical filtered set/ordered stream defined by a number-theoretic property;
2. a constructive finite or incremental sieve with stage-by-stage survivor/removal state;
3. a derived arithmetic measurement sequence `g(n)` with no necessary mutable filter state.

State, support, stage schedule, reads, predicate/result data, update law, no-op stages, finite/infinite completion, equality, serialization, trace, and observers remain under audit.

## Exact Book Presets and Oracles

The `1..100` sieve rows, prime list, page-148 panels, page-150 formulas/horizons, and source convention for `1` are under exact reconstruction.

## Variants, Relations, and Boundaries

T37/Ulam, T40 digit streams, direct primality, factorization, divisor enumeration, prime-counting functions, finite sieves, lazy streams, stochastic prime models, and CA/Turing/register emulations are under audit as native profiles, analyzers, outputs, or relations.

## Current API Fit

In progress.

## Current Runtime Fit

In progress.

## Principles Audit

No transition algebra or update law is chosen until the source distinguishes the limiting prime set, finite figure state, stage schedule, and derived curves. A predicate callback or precomputed list is not an acceptable shortcut.

## Detailed Implementation Plan

1. Complete main/raster, Notes, actual Index, split, program, history, alias, variant, and relation searches.
2. Reconstruct the exact page-147 sieve including candidate `1`, stage schedule, row count, removals, survivors, and finite/infinite interpretation.
3. Decode every page-148/page-150 curve as an exact formula/observer or separate construction and independently generate anchor values.
4. Derive closed candidate/predicate/stage/output data and determine which categories are transitions versus specifications or pure measurements.
5. Specify outcomes, equality, serialization, traces, realizations, algorithm/output equivalence, and Ulam composition.
6. Audit current API/runtime/tests, write Goal 2/no-cheating work, integrate global artifacts, and verify the repository.

## Goal 2 Implementation Stage

Pending the evidence audit.

## No-Cheating Checks

The final stage must reject unrestricted predicate callbacks, trusted prime tables/booleans, direct primality substituted for a requested sieve trace, hidden candidate/stage cursors, fixed capacity presented as the infinite set, `1` silently changed, survivor/removal loss, composite-stage skipping without an explicit schedule, derived curves fed back as state, and family-specific rollout branches.

## Completion Requirements

- [ ] Every main figure/curve, Notes, actual Index, split, program, history, alias, named variant, and relation candidate is dispositioned.
- [ ] Candidate/stage/predicate/survivor/removal/output/outcome semantics and finite/infinite scopes are explicit.
- [ ] Page-147, page-148, and page-150 profiles have independent exact oracles and source repairs.
- [ ] Mathematical set, ordered stream, sieve trace, direct analyzer, and derived measurement remain distinct.
- [ ] Ulam/T37 and T40 boundaries plus current API/runtime fit are explicit.
- [ ] Goal 2 handoff, global ledgers, diff checks, and repository tests are integrated.

## Stage Results

In progress.

## Integration Results

In progress.
