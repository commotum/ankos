# 15-T37-RECURSIVE

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T37, CSV line 38, `Recursive Sequences`; taxonomy seed `ref/notes/CA-Types.md:1023-1053`. The taxonomy supplies vocabulary only.
- Canonical source heading `Recursive Sequences` begins at `BOOK:1555`. The strict fixed-distance examples occupy `BOOK:1555-1567`; data-dependent index expressions begin T38 at `BOOK:1569` even though they share the printed heading.
- The source describes `f[n]` as computed from earlier sequence values such as `f[n-1]` and `f[n-2]`. Whether the semantic Markov state is the entire generated prefix, a sufficient fixed lag window plus absolute index, or another closed representation must be derived rather than copied from the taxonomy.
- Page 143 contains the strict figure, including powers-of-two and Fibonacci examples. Exact rule rows, seeds, term counts, indexing, Notes, Index routes, variants, and observers remain under audit.
- T34 can reproduce powers of two with one scalar multiplication, but observationally equal values do not prove identical state or append semantics.
- Current AR2/temporal 0D code reads stored prior trajectory slices or hidden seed histories and uses fixed-width modular arithmetic. It is candidate evidence to audit, not an accepted T37 implementation.

## Updated Assumptions

- Fixed-lag references will be closed structural offsets, not arbitrary sequence callbacks or data-dependent expressions.
- Initial terms, index origin, seed coverage, and every dependency required for the first generated term will be explicit.
- Appending a term must not mutate prior terms. A compact sufficient-state execution, if valid, must retain enough visible index/lag data and an exact projection to the canonical generated prefix.
- Exact values, sequence state, stored trace, rendered plots, closed-form formulas, and acceleration algorithms will remain distinct.
- Invalid forward/current/nonpositive references will be rejected at program validation unless primary evidence requires a typed runtime outcome.

## Big Picture Objective

Reconstruct fixed-dependency recursive sequences as an exact append construction. Pin down semantic state, index origin, initial prefix, closed recurrence expressions, dependency reads, append result/update, deterministic outcomes, equality/serialization, compact realizations, observers, exact presets, neighboring T34/T38/T39/T43 boundaries, and the smallest honest Goal 2 integration.

## Catalog Identity

- Stable ID: T37.
- Exact name: Recursive Sequences.
- CSV provenance: `ref/notes/CA-Types.csv:38`; taxonomy provenance: `ref/notes/CA-Types.md:1023-1053`.
- Canonical strict main range: `BOOK:1555-1567`; T38 boundary begins `1569`.
- Entry kind, strict profiles, aliases, native Notes, actual Index, figures, programs, and history: under audit.

## Search Log

1. Verified catalog/taxonomy identity and read the scoped main boundary through the start of primes.
2. Opened parallel source/figure, Notes/Index/search, and architecture/runtime audits.
3. Exhaustive queries and candidate dispositions are in progress.

## Book Excerpts

Canonical excerpt groups are under audit.

## Construction Model

State, closed recurrence grammar, dependency validation, append/update semantics, trace projection, and outcomes are under audit.

## Exact Book Presets and Oracles

Page-143 rows and independent trajectories are under audit.

## Variants, Relations, and Boundaries

T34 scalar iteration, T38 variable-index recursion, T39 filtering, T40 constant digits, and T43 maps are under audit as distinct constructions or relations.

## Current API Fit

The documented API comparison is in progress.

## Current Runtime Fit

The current AR2/history/neighborhood/rule/rollout/trace comparison is in progress.

## Principles Audit

No prefix-versus-lag-window conclusion is closed until the source, exact presets, recurrence dependencies, and trace requirements have all been checked.

## Detailed Implementation Plan

1. Complete main, figure, Notes, actual Index, split, program, history, alias, and relation searches.
2. Reconstruct every strict rule/seed/term row and independently generate exact trajectories.
3. Derive the minimal closed fixed-lag expression grammar and dependency validator.
4. Resolve canonical prefix state versus compact sufficient-state realization and their trace mapping.
5. Specify typed append result/update, outcomes, equality, serialization, observers, and no-cheating tests.
6. Audit current API/runtime/tests, write the Goal 2 handoff, integrate global artifacts, and verify the repository.

## Goal 2 Implementation Stage

Pending the evidence audit.

## No-Cheating Checks

The final stage must reject unrestricted recurrence callbacks, hidden trajectory reads, fixed-width/modular substitution, variable-index T38 expressions, future/current references, implicit seed padding, scalar packing of the entire prefix, and confusion between generated prefix and stored execution trace.

## Completion Requirements

- [ ] Every main-text, figure, Notes, actual Index, program, history, alias, variant, and relation candidate is dispositioned.
- [ ] State/index/seed/dependency/expression/append/outcome/equality/trace semantics are explicit.
- [ ] Every strict figure row has independently checked exact terms and adversarial tests.
- [ ] Prefix semantics and any compact realization are related without hidden history or lost reproduction.
- [ ] T34/T38/T39/T40/T43 boundaries and current runtime fit are explicit.
- [ ] Goal 2 handoff, global ledgers, diff checks, and repository tests are integrated.

## Stage Results

In progress.

## Integration Results

In progress.
