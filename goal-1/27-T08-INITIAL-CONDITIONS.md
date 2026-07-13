# 27-T08-INITIAL-CONDITIONS

Status: **IN PROGRESS — SOURCE/ASSET/ARCHITECTURE AUDIT ACTIVE**

## Current Facts

- Exact catalog row: T08, CSV line 9, `Initial-Condition Classes`; taxonomy section 8 at `ref/notes/CA-Types.md:177-192` is search vocabulary only, not book evidence.
- The working hypothesis is that T08 classifies seed/run inputs to an existing resolved program, not new transition semantics. The same program can be paired with several initial configurations without changing FRONTIER, NEIGHBORHOOD, RULE, UPDATE, or program identity.
- A deterministic seed description, a probability distribution over seeds, one realized initial configuration, a finite computation realization, and a displayed crop are different objects. Randomness used only to sample event-zero state is not hidden per-step executor state.
- For an infinite fixed lattice, a point seed is naturally a total background field plus a finite override. Rendering that field into a centered finite array is a realization/projection choice, not the seed's native support or boundary policy.
- Seed validity is configuration-schema dependent. A gray value must belong to the declared ALPHABET; composite/tagged control configurations must satisfy structural invariants; a temporal recurrence prefix contains Markov state that cannot be replaced by a spatial point marker.
- T01-T07 already require program, seed, realization/boundary, trace, and view identities to remain distinct. T06/T07 property evidence cannot smuggle a preferred seed into program identity.
- Current `src/ca/seeds.py` contains deterministic, selector-backed, stochastic, compound, geometric, and structured factories plus a finite-shape renderer. Its reusable role and its callback/finite-realization/RNG boundaries require fresh inspection; current behavior is not presumed to define T08.
- DOMAIN means the task/program dimensional support/topology. A seed selects or constructs a valid configuration on that DOMAIN; “seed class” is not a new DOMAIN merely because its support pattern has a different shape.
- Goal 1 changes only `goal-1/`; runtime, root documentation, and tests remain Goal 2 work.

## Updated Assumptions

- Preserve one branch-free SimpleProgram runner:

```text
active = FRONTIER.select(state)
reads  = NEIGHBORHOOD.read(state, active)
writes = RULE(active, reads)
next   = UPDATE.apply(state, active, writes)
```

- Treat a seed as an explicit, typed constructor or sampler for one valid event-zero configuration. Do not add seed-aware RULE or rollout branches.
- Require a lossless distinction among native configuration, compact seed descriptor, realized sample, finite materialization, and observation crop.
- Keep open until book evidence closes: the exact named T08 classes; whether randomness is Bernoulli, fixed-density, uniform over a finite support, or underdetermined; which background/value/centering choices are source-mandated; and whether any seed class carries native symmetry or periodicity invariants beyond event zero.

## Big Picture Objective

Determine exactly which initial-condition classes the source uses, reconstruct their typed configuration semantics and probability/provenance where applicable, and hand Goal 2 the smallest generic seed/profile layer that composes with existing SimplePrograms without changing their execution algebra or conflating infinite support with finite rendering.

## Catalog Identity

- Stable ID: T08.
- Exact CSV name: `Initial-Condition Classes`.
- Taxonomy section: 8, vocabulary seed only.
- Working entry kind: cataloged seed/run-profile classes over existing constructions; not a construction or executor.
- Initial vocabulary: initial condition/configuration/state/pattern/arrangement, simple and random initial conditions, single black/gray/white cell, point/finite/block/row/line seed, all-white/all-black background, periodic/repeating/random configurations, starting configuration, and changes/sensitivity in initial conditions.

## Search Log

Audit in progress. The final log will include exact monolith candidate generators, governed continuations, split reverse joins, Index routes, asset closure, classifications, and zero-remainder checks without claiming semantic exhaustiveness for unformalized manual supplements.

## Book Excerpts

Audit in progress.

## Construction Model

Working model pending evidence closure:

- **Program:** one already resolved SimpleProgram; excluded from seed identity.
- **Seed descriptor:** a typed deterministic configuration constructor or a typed probability law plus its parameters.
- **Realized initial configuration:** one complete invariant-valid event-zero state on the native DOMAIN/support.
- **Compact fixed-lattice form:** background value plus finite exceptions, or an explicit periodic/finite presentation when that is the declared native profile.
- **Random form:** an explicit probability law and sampling scope; RNG algorithm/key/sample provenance are realization data unless the mathematical law names them.
- **Execution:** unchanged FRONTIER/NEIGHBORHOOD/RULE/UPDATE after event zero.
- **Relations:** translation, reflection, complement, density, finite crop, and seed equivalence are explicit transforms/claims, not implicit identity.
- **Invalidity:** alphabet mismatch, unsupported infinite sampling/materialization, conflicting assignments, violated structural invariants, or missing stochastic parameters fail before rollout.
- **Observers:** behavior class, growth, sensitivity, entropy, image, and dataset split remain downstream analyses.

## Current API Fit

Pending complete evidence and `simple_programs.md` audit.

## Current Runtime Fit

Pending complete `src/ca`, test, and dataset audit.

## Principles Audit

- Principles 1, 9, and 10 suggest a discoverable catalog preset/profile over the independent seed axis, not a family executor.
- Principles 5, 7, and 8 require every realized seed to be a complete valid configuration on native support; compact finite-exception and periodic forms need explicit lossless mappings.
- Principle 11 keeps a one-time stochastic seed law distinct from RNG implementation and from stochastic transition rules.
- Principle 12 keeps held-out-seed streams, batching, padding, centering, and rasterization outside program semantics.
- Principles 13-16 require adversaries for background evolution, translation/centering, finite boundaries, ALPHABET mismatch, composite invariants, random-law identity, replay, and opaque callback rejection.

## Detailed Implementation Plan

1. Close a reproducible source universe across direct terminology, concrete seed descriptions, captions, Notes, Index routes, aliases, and cross-references; disposition every candidate.
2. Close the governed visual-asset universe with exact monolith/split references, dimensions, hashes, semantic classifications, and run/caption stop rules.
3. Reconstruct deterministic, stochastic, finite-exception, periodic, and structured seed profiles from evidence; separate seed, realized configuration, realization, boundary, trace, and view.
4. Audit `simple_programs.md`, `src/ca`, tests, datasets, and completed stages; identify exact reuse and mismatches without preserving incidental Phase 1 behavior.
5. Specify Goal 2 schemas, identity/provenance, validation, serialization, transformations, acceptance tests, and no-cheating checks.
6. Run all embedded oracles, independent hostile review, repository tests, Markdown/coverage/decision/diff gates, integrate the ledgers, and advance only after clean closure.

## Goal 2 Implementation Stage

Pending evidence closure. The working target is **G2-T08 — typed seed profiles, stochastic realization, and configuration validation**, layered over resolved programs/configuration schemas with no executor change.

## No-Cheating Checks

- No T08/seed-family rollout branch, seed-aware RULE, implicit boundary, forced finite tensor DOMAIN, or preferred seed stored in program identity.
- No opaque predicate/callback or whole-configuration integer accepted as a semantic seed merely because it can render an array.
- No RNG cursor hidden in executor state for a one-time seed draw; no stochastic seed distribution conflated with stochastic transition semantics.
- No centered array, crop, padding, batch shape, held-out split, palette, or raster treated as the native initial configuration.
- No single-black-cell assumption used to prove T06/T07 or a behavior class; no symmetric seed used as rule-symmetry evidence.
- No “gray” value inferred from palette order without an explicit ALPHABET member/valuation.
- No compact seed representation accepted without an inverse on its invariant-valid image and a one-step identity mapping after realization.

## Completion Requirements

- [ ] Every declared source candidate and governed asset is dispositioned under reproducible, honestly scoped protocols.
- [ ] Every retained excerpt/asset has exact provenance and its construction fact is separated from behavior, boundary, and view claims.
- [ ] The seed/profile model covers every evidenced deterministic and stochastic class, validation invariant, identity, transform, and realization distinction.
- [ ] Current API/runtime fit and a concrete Goal 2 handoff are implementation-ready with adversarial conformance cases.
- [ ] Global ledgers, independent review, all embedded checks, coverage/diff gates, and repository tests pass.

## Stage Results

IN PROGRESS.

