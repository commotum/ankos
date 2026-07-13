# 13-T31-CONSTRAINTS

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T31, CSV line 32, `Local Constraint Systems`; taxonomy seed `ref/notes/CA-Types.md:842-864`. Taxonomy suggestions for custom predicates, global requirements, infinite approximations, and solver choice are hypotheses, not evidence.
- T31 is not a dynamics construction. It denotes a mathematical set of total configurations satisfying one translation-invariant local neighbor-count relation at every site.
- The strict carrier is a total field `X: Z^d -> Sigma` on an evidenced regular lattice. A finite periodic tile is an exact representation/proof of an infinite periodic field, not a finite evolution state.
- The local relation observes the center symbol and the orientation-insensitive histogram of symbols on a declared finite neighbor footprint. The center is separate from the footprint.
- A closed program maps every center symbol to a finite set of allowed histograms. Missing center rows, duplicate footprint offsets, malformed histograms, wrong total degree, callbacks, and implicit defaults are invalid.
- T31 owns neighbor-count constraints. T32 owns exact oriented allowed neighborhood templates; T33 owns an existential requirement that a particular template appear. These distinctions cannot become optional flags/global predicates on T31.
- There is no seed, initial condition, time, frontier, read event, rule result, update, successor, halt, control, or RNG in the constraint system.
- A complete configuration is a model/witness, not a final state. The solution set may be empty, one symmetry orbit, several or infinitely many models.
- Exact configurations remain pointwise distinct. Translation, rotation, reflection, color exchange, period minimization, or a displayed representative are observers/relations, not semantic equality.
- Verification and solving are outside the immutable constraint data. A local verifier returns explicit violations; a solver returns query outcomes with witnesses/certificates/scope.
- The 1D constraint “each cell has exactly one black and one white neighbor” has precisely translations of period-4 `(0011)^infinity`. Its allowed triples and de Bruijn cycle give an exact proof.
- The 1D constraint “at least one differently colored neighbor” is exactly the set of binary sequences whose runs have length at most two. It admits many models, including alternating and `0011` periodic fields.
- In one dimension, any satisfiable finite local constraint has some periodic model. This does not imply uniqueness or that arbitrary search bounds decide satisfiability.
- The canonical 2D cardinal-neighbor profile requires a black center to have exactly one black neighbor and a white center exactly two white neighbors. A recovered `5x5` periodic tile verifies it exactly.
- The page-227 grid studies all `5x5=25` pairs of same-color neighbor counts for black and white centers. Two profiles are unsatisfiable; the image labels require an independent transcription check before freezing.
- Failure to find a model in a bounded tile/patch search is `Unknown`, never proof of infinite unsatisfiability. A sound unsatisfiability result requires a replayable certificate such as a finite obstruction with its full variable halo.
- Gray/unassigned cells and backtracking order are solver diagnostics, never a third alphabet symbol or trajectory.
- Infinite existence is undecidable in the broader setting and finite-region existence is NP-complete. No total solver, custom-solver fallback, or one-witness-as-whole-solution-set representation is honest.
- Current runtime has finite dense trajectory arrays and totalistic update rules, but no immutable constraint specification, infinite-model verifier, solution-set semantics, certificate/query outcome, or honest incomplete solver boundary.
- T31 is the first direct construction that breaks the transition `SOURCE -> READ -> RESULT -> UPDATE` shell: a constraint relation and solver query are different semantic categories.

## Updated Assumptions

- `LatticeFootprint` is an explicit finite unordered duplicate-free set of nonzero offsets in `Z^d`. It owns topology only; it is not a CA neighborhood with boundary/update policy.
- `NeighborHistogram` is an alphabet-indexed tuple of nonnegative counts summing to footprint degree. Histogram ordering follows a declared alphabet codec, not hash order.
- `LocalCountConstraint` is total closed relation data `center_symbol -> allowed_histograms`. “Exactly,” “at least,” and “at most” profiles compile to finite allowed sets rather than predicate callbacks.
- Native model scope is the total infinite field. A periodic tile plus lattice basis/origin denotes a total periodic field exactly. A finite open patch is only `LocallyConsistentPatch(scope)` and never silently a global solution.
- `violation_at` is pure verification, not an evolution source. It reports locus, center symbol, observed histogram, and allowed set.
- A solver is an independent algorithm over a constraint/query scope. Search order, propagation, SAT encoding, de Bruijn analysis, memoization, and bounds do not belong to the constraint object.
- Query outcomes are `Satisfiable(witness,proof_scope)`, `Unsatisfiable(certificate,scope)`, `Unknown(reason,explored_scope)`, and `ResourceLimit`. They are not `Advanced`, `Terminal`, or program traces.
- Any solver witness must reverify independently. Any unsatisfiability certificate must replay independently. Bounded exhaustion alone supplies neither.
- Finite periodic search in 2D is incomplete by design. The 1D de Bruijn analyzer may be complete for its explicitly bounded local profile.
- Symmetry quotienting may summarize solutions only after exact pointwise models are established.

## Big Picture Objective

Reconstruct local constraint systems as declarative model sets over regular total fields: explicit lattice footprint, center-conditioned neighbor histograms, exact local satisfaction, periodic witnesses, solution multiplicity, and verifier/solver/certificate boundaries. Determine how Goal 2 must split constraints from transition execution while excluding repair dynamics, callback predicates/solvers, fake finite capacity, bound-as-proof, gray-state packing, symmetry quotienting, T32/T33 collapse, and CA fixed-point compilation as native coverage.

## Catalog Identity

- Stable ID: T31.
- Exact name: Local Constraint Systems.
- CSV provenance: `ref/notes/CA-Types.csv:32`; taxonomy provenance: `ref/notes/CA-Types.md:842-864`.
- Canonical strict main core: `BOOK:2568-2612`. Exact oriented templates begin T32 at `2614`; required-template existence begins T33 at `2634`.
- General constraint-versus-search discussion: `BOOK:2642-2666`.
- Native Notes core: `BOOK:14029-14047` and `14080-14084`.
- Entry kind: declarative translation-invariant local neighbor-count relation defining a possibly empty model set; not a transition system or solver.
- Search vocabulary: systems based on constraints, constraint system(s), local constraint(s), satisfy/satisfaction, neighbor count, black/white neighbor, allowed block, forbidden block, periodic/repetitive solution, no solution/unsatisfiable, finite obstruction, search/backtracking, undecidable/NP-complete, ground state, fixed point, de Bruijn graph, subshift, tiling, template, and the T32/T33 boundary terms.

## Search Log

1. Verified CSV line 32 and read `ref/notes/CA-Types.md:842-864`; its predicate/global-requirement/custom-solver suggestions remain unaccepted.
2. Read the strict main count-constraint core `BOOK:2568-2612` and inspected the page-225/page-226/page-227 figures. The page-227 profile labels remain under independent visual confirmation.
3. Read `BOOK:2642-2666` for the defining absence of direct evolution and separation of constraint data from external search/backtracking.
4. Read Notes `BOOK:14029-14047` for equations, allowed blocks, 1D periodicity, and the cellular-automaton fixed-point relation; read `14080-14084` for search, undecidability, and finite NP-completeness.
5. Preliminary searches found exact `system(s) based on constraint(s)` 17/17 occurrences/lines, `constraint system(s)` 9/9, `local constraint(s)` 3/3, broad `constraint(s)` 467/312, and satisfy/constraint proximity 178/144. Counts remain provisional until actual Index/split disposition closes.
6. Followed relations to CA/ground states, tilings, template/required-template systems, network constraints, sequence equations, pattern avoidance, PCP, Diophantine equations, CA fixed points/spacetime, and no-initial-condition evidence. Full disposition remains in progress.
7. Audited current runtime/API pressure preliminarily. No constraint spec/verifier/solver-result boundary exists; the existing totalistic update pipeline is not a constraint engine.

## Book Excerpts

Canonical `BOOK` means `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`. Final groups remain open until the figure/Index/variant audit closes.

### E01 — Constraints instead of evolution

- Provenance: `BOOK:2568-2578`.
- Fact: constraints specify which complete configurations are allowed without giving any procedure that generates them.

### E02 — Unique 1D count profile

- Provenance: `BOOK:2574-2582`, page-225.
- Fact: requiring exactly one black and one white immediate neighbor forces the period-4 pattern, modulo translation.

### E03 — More permissive 1D profile and periodic sufficiency

- Provenance: `BOOK:2582-2598`, page-226 top.
- Fact: requiring at least one unlike neighbor permits exactly runs of length at most two. More generally, every satisfiable finite local 1D constraint has a periodic model.

### E04 — Canonical 2D neighbor-count model

- Provenance: `BOOK:2596-2608`, page-226 bottom.
- Fact: on the four-cardinal-neighbor square lattice, black requires one black neighbor and white requires two white neighbors; the displayed periodic `5x5` tessellation and symmetries satisfy it.

### E05 — Solution-set multiplicity and unsatisfiable profiles

- Provenance: `BOOK:2608-2612`, page-227.
- Fact: among the 25 same-color count pairs, some have no model, many one/two periodic families, and some infinitely many mixtures. A periodic model suffices whenever these specific profiles are satisfiable.

### E06 — Search is external to the system

- Provenance: `BOOK:2642-2666`.
- Fact: unlike explicit evolution, constraint satisfaction requires going outside the system to enumerate/build/backtrack. Finite obstructions can certify some global impossibility; large patches alone do not guarantee an infinite extension.

### E07 — Notes equation/constraint distinction

- Provenance: `BOOK:14029-14039`.
- Fact: equations may encode evolution or same-time constraints; this distinction is often obscured in continuous mathematics.

### E08 — Allowed blocks and 1D periodic proof

- Provenance: `BOOK:14040-14047`.
- Fact: a finite allowed-block representation/de Bruijn argument proves a satisfiable 1D local constraint has a periodic solution and relates solutions to fixed points/spacetime patterns of cellular automata.

### E09 — Search complexity

- Provenance: `BOOK:14080-14084`.
- Fact: general infinite satisfaction is undecidable and finite constraint satisfaction is NP-complete; search algorithms are external.

### E10 — No initial conditions

- Provenance: `BOOK:14275`.
- Fact: systems based on constraints do not have initial conditions.

## Construction Model

The current evidence-backed candidate is:

```text
LocalCountConstraintSystem = {
    dimension: PositiveInt,
    alphabet: FiniteNonEmptyOrderedSet[Symbol],
    footprint: FiniteNonEmptySet[NonzeroOffset[Z^dimension]],
    allowed: TotalMap[
        center_symbol,
        FiniteSet[NeighborHistogram[alphabet, degree=len(footprint)]]
    ]
}

Models(C) = {
    X: Z^dimension -> alphabet
    | for every p in Z^dimension:
        histogram(X[p+delta] for delta in footprint)
        in C.allowed[X[p]]
}
```

The remaining evidence pass must freeze exact figures/profile tables, scopes, verification/certificate APIs, solver outcomes, variants, runtime fit, adversarial tests, and Goal 2 handoff.

## Current API Fit

Initial conclusion: finite alphabet and lattice offset geometry may be reusable data responsibilities, but every frontier/rule/update/trajectory mechanism is not applicable. Constraints require a declarative spec plus verifier/solver-query boundary outside the transition executor.

## Current Runtime Fit

Initial audit finds no model-set, violation, periodic-witness, finite-obstruction, `Unknown`, or solver-certificate types. Totalistic CA summaries may share a private histogram kernel only; compiling to CA fixed points or adding a constraint family rollout is rejected.

## Principles Audit

Pending evidence closure. Provisional rejections include repair/update dynamics, predicate/solver callbacks, gray as a color, one witness as the solution set, bound exhaustion as unsatisfiability, open/periodic scope confusion, finite grids as `Z^d`, CA fixed-point substitution, automatic symmetry quotient, T32 oriented templates collapsed to counts, T33 existential requirements hidden in a global predicate, and solver traces as trajectories.

## Detailed Implementation Plan

1. Close direct/alias/proximity, figures, Notes, actual Index, split, search/complexity, allowed-block, periodicity, ground-state/CA, tiling, T32/T33, network, equation, and solver candidates.
2. Freeze declarative carrier, histogram relation, exact model equality, infinite/periodic/open scopes, verification, witnesses, finite obstruction, solver outcomes, and incompleteness.
3. Recover exact 1D/2D profiles, page-227 satisfiability table, periodic witnesses, and adversarial verification/certificate tests.
4. Compare every responsibility with current API/runtime and prior transition stages; record the first categorical executor split.
5. Audit no-cheating constraints, variants, symmetry/views, serialization, batching, and Goal 2 dependencies.
6. Reintegrate all ledgers and write the implementation-ready constraint/verifier/solver handoff.

## Goal 2 Implementation Stage

Pending evidence closure. It will specify immutable count-constraint data, infinite/periodic model representations, exact verifier/violations, replayable certificates, independent incomplete solver outcomes, canonical profiles, tests, and repository integration without a transition rollout or solver callback.

## No-Cheating Checks

- No repair/evolution dynamics, frontier, rule result, update, rollout family, or trajectory presented as the constraint system.
- No predicate/solver/SAT/backtracking callback inside the immutable semantic spec.
- No gray/unassigned value in the declared model alphabet.
- No one witness presented as the complete solution set or uniqueness proof.
- No bounded search failure presented as infinite unsatisfiability; no unverifiable certificate.
- No open-edge patch silently treated as a torus or total infinite field.
- No finite shape/capacity presented as native `Z^d`.
- No CA fixed-point compilation, totalistic next-value rule, ground-state minimizer, or T32/T33 collapse used merely to claim coverage.
- No automatic translation/rotation/reflection/color quotient as model equality.
- No solver search trace, branch ordering, heuristic, limit, or gray picture serialized as a program trajectory.

## Completion Requirements

- [ ] All names, aliases, figures, Notes, actual Index entries, splits, history, variants, observers, and relations resolved with zero silent remainder.
- [ ] Native local-count relation, total model set, exact equality, scopes, verifier, witnesses/certificates, solver outcomes, and complexity boundary reconstructed.
- [ ] Exact 1D/2D periodic models and adversarial verification/unsat/unknown/scope invariants specified.
- [ ] Current API/runtime/principles fit and transition-executor split explicit.
- [ ] Goal 2 implementation/conformance handoff and global reintegration complete.

## Stage Results

In progress. Core evidence already establishes that T31 is a declarative neighbor-count model set, not dynamics, and that verification, periodic representation, external search, incomplete outcomes, and solver certificates must remain distinct. The page-227 table, full search/variant disposition, and Goal 2 handoff remain open.
