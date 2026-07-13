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

`allowed[center]` may be empty, so the syntax can denote an inconsistent relation. Every histogram is a vector in declared alphabet order with nonnegative entries summing to `degree`. A constraint value is valid without knowing whether `Models(C)` is empty.

There is no materialized “state containing all models.” `Models(C)` is the mathematical denotation of finite program data. It is not enumerated, evolved, approximated by one tile, or packed into an object array.

### Exact count relation and local verification

For a closed model representation `X` and locus `p`:

```text
observed(C,X,p) =
    histogram(
      X[p + delta]
      for delta in C.footprint
    )

satisfied_at(C,X,p) =
    observed(C,X,p) in C.allowed[X[p]]

violation_at(C,X,p) =
    None
    if satisfied_at(...)
    else LocalViolation(
      locus=p,
      center=X[p],
      observed=observed(...),
      allowed=C.allowed[X[p]]
    )
```

This is a pure relation check. The locus is not an active source; the violation is not a rule result; changing a cell to “repair” it is not T31.

The strict reusable representation profiles are:

```text
PeriodicLatticeModel = {
    dimension,
    period_lattice / rectangular_period,
    finite_fundamental_domain_values,
    origin
}

FinitePatch = {
    finite_values,
    checked_anchor_set,
    required_halo
}
```

A periodic model defines an exact total field by quotienting lattice points through its declared period. Since the constraint is translation invariant, checking one complete fundamental domain proves the infinite field. An origin shift changes the pointwise field even when it lies in the same translation orbit.

A finite patch makes only a scoped claim. Every checked anchor must have its entire footprint halo in the finite value map. Passing this check yields `LocallyConsistentPatch`, not an infinite model. Open, periodic, and infinite scopes are explicit types and cannot share a silent boundary option.

### Model equality, symmetries, and solution-set observations

Semantic models are pointwise total fields. Two periodic representations can be compared exactly by reducing both to a common period; structural tile equality alone is not the only possible representation equality. General infinite extensional equality need not be decidable and is not promised by the API.

Translations, rotations, reflections, color permutations, minimal periods, orbit representatives, model counts, uniqueness, and entropy are explicit relations/observers. A caption that displays “the only” pattern with its rotations/reflections does not authorize quotienting exact models or prove a particular origin convention.

### Verifier, certificates, and solver queries

Constraint data and solving remain separate:

```text
ConstraintSystem             # immutable denotation
ConstraintVerifier           # pure exact checks
ConstraintSolver             # optional external algorithm

QueryOutcome =
    Satisfiable(witness, claim_scope, verification)
  | Unsatisfiable(certificate, claim_scope)
  | Unknown(reason, explored_scope)
  | ResourceLimit(resource, explored_scope)
```

Examples of sound claims:

- a verified periodic witness proves global satisfiability;
- a verified finite patch proves only local consistency on its anchors;
- failure to find any tile up to a period bound proves only “no witness in this search scope” and returns `Unknown` for global existence;
- an exhaustive finite obstruction can prove global unsatisfiability.

An exact replayable finite obstruction is:

```text
ExhaustiveFiniteObstruction = {
    anchors: FiniteSet[LatticePoint],
    variables: anchors + footprint_halo
}

replay:
  for every assignment variables -> alphabet:
      at least one anchor violates its local relation
```

If a global model existed, its restriction to `variables` would contradict this finite exhaustive proof. The checker recomputes the finite enumeration; no solver callback or trusted “unsat” boolean is accepted. More compact SAT/resolution certificates may be added later only with their own closed proof AST/checker.

Search algorithms—square-spiral growth, backtracking, propagation, de Bruijn graphs, SAT encodings, memoization, symmetry breaking, heuristic ordering, and periodic bounds—consume a constraint/query but never become fields of the constraint value. Their diagnostic search trees are not program trajectories.

### Exact 1D de Bruijn analyzer

For a contiguous allowed-block profile of length `n` over `k` symbols:

1. vertices are all length-`n-1` words;
2. each allowed length-`n` block gives an edge from its prefix to suffix;
3. a bi-infinite model exists iff the remaining finite graph contains a directed cycle;
4. a directed cycle yields a periodic witness of period at most `k^(n-1)`;
5. a DAG/no-cycle certificate proves unsatisfiability.

For the first T31 profile, allowed triples are:

```text
001, 011, 100, 110
```

and the graph is the one cycle:

```text
00 -> 01 -> 11 -> 10 -> 00
```

It yields translations of `(0011)^infinity` and saturates the `2^(3-1)=4` period bound.

### Canonical strict profiles

Using binary alphabet `0=white,1=black`:

```text
one_black_one_white_neighbors_1d:
  dimension = 1
  footprint = {(-1),(+1)}
  allowed[0] = {(one 0, one 1)}
  allowed[1] = {(one 0, one 1)}

at_least_one_unlike_neighbor_1d:
  dimension = 1
  footprint = {(-1),(+1)}
  allowed[0] = {
      (one 0, one 1),
      (zero 0, two 1)
  }
  allowed[1] = {
      (two 0, zero 1),
      (one 0, one 1)
  }

black1_white2_same_neighbors_2d:
  dimension = 2
  footprint = {(-1,0),(+1,0),(0,-1),(0,+1)}
  allowed[0] = {(two 0, two 1)}
  allowed[1] = {(three 0, one 1)}
```

The second profile is equivalently “every run has length at most two.” The third profile's exact periodic witness is:

```text
00110
11000
00011
01100
10001
```

with both axes periodic of length 5. All 25 torus anchors satisfy the relation. Flipping the top-left bit produces exactly five violations at `(0,0),(1,0),(4,0),(0,1),(0,4)` under zero-based `(x,y)` coordinates, a strong boundary/orientation/histogram oracle.

### Adversarial conformance oracles

1. **Period-4 proof.** Verify all four phases of `0011` and the exact de Bruijn cycle; reject a phase containing a triple run.
2. **Run constraint.** Alternating and `0011` models pass the at-least-one-unlike profile; any `000` or `111` occurrence produces an exact violation.
3. **2D torus.** The recovered `5x5` tile has zero violations across all anchors; its one-bit perturbation has the five exact violations above.
4. **Center-conditioned rows.** Swapping `allowed[0]` and `allowed[1]` generally changes the result; color counts are not a single center-blind totalistic rule.
5. **Footprint orientation.** Cardinal degree four excludes diagonals and center. Duplicating or including the center is invalid.
6. **Histogram codec.** Permuting alphabet serialization together with histogram entries is equivariant; permuting counts alone is not.
7. **Pointwise identity.** A translated periodic field is a separate model even when an orbit observer groups it.
8. **Scope.** A locally consistent open patch cannot be accepted as an infinite/torus model; missing halo is reported, not padded.
9. **Witness replay.** Every `Satisfiable` periodic witness independently re-verifies over its fundamental domain.
10. **Unsat replay.** On the 1D nearest-neighbor profile `allowed[0]={(one 0,one 1)}` and `allowed[1]=empty`, anchors `{0,1,2}` with halo `{-1,0,1,2,3}` are an exhaustive obstruction: every anchor would have to be 0, so the middle anchor sees two 0 neighbors. The checker must independently replay all assignments.
11. **Unknown.** Exhausting a deliberately small period/search bound returns `Unknown` for the global problem, never `Unsatisfiable`.
12. **Search independence.** Different search orders may find different exact models but cannot change the constraint or validity of a witness.
13. **No gray state.** Partial assignments belong only to a solver trace; model verification rejects undeclared gray/unassigned values.
14. **Validation.** Reject empty alphabet/footprint, zero/duplicate/mixed-dimension offsets, missing center row, undeclared symbol, negative/wrong-sum histogram, malformed period, incomplete tile, and callbacks.

## Variants, Relations, and Boundaries

- **T31 local count constraints:** orientation-insensitive center-conditioned neighbor histograms on declared regular-lattice footprints.
- **T32 template constraints:** exact oriented allowed local templates; histograms cannot preserve orientation.
- **T33 seeded/required-template constraints:** adds an existential global occurrence/anchor requirement; not an optional T31 predicate.
- **General allowed-block/subshift-of-finite-type systems:** a relation/bridge; contiguous 1D blocks admit the de Bruijn analyzer, while T32 owns general oriented template syntax.
- **Cellular-automaton fixed points/spacetime encodings:** reductions/relations. A CA update or fixed-point search is not native constraint coverage.
- **Spin/Ising ground states and energy minimization:** optimization constructions; zero-energy local clauses may compile only under proved equivalence.
- **Tilings/Wang tiles and network constraints:** different carriers/topologies and matching rules.
- **Sequence/string equations, pattern avoidance, PCP, Diophantine equations:** constraint relatives with separate value domains and decision problems.
- **Finite periodic torus:** exact representation/query scope for a periodic infinite field, not a finite approximation or boundary default.
- **Finite open region:** local verification/search scope only.
- **Model finding, enumeration, counting, uniqueness, entropy, symmetry orbits, and visualization:** solver/query/observer layers.
- **Repair dynamics, belief propagation, SAT, backtracking, and stochastic search:** algorithms external to the constraint semantics.

## Current API Fit

| T31 responsibility | Current proposal fit | Required conclusion |
|---|---|---|
| Infinite regular domain | Current finite dense rank-0..3 shape | SEMANTIC MISMATCH; reuse T01 total-lattice concept and exact periodic realizations |
| Alphabet | Declared finite symbolic/integer values | DIRECT |
| Footprint | Offset neighborhoods/Von Neumann shapes | PARAMETERIZATION as topology-owned data, without time/boundary/update semantics |
| Local summary | Totalistic neighbor aggregation | PRIVATE KERNEL REUSE for histograms only |
| Constraint relation | Per-target next-value rule/predicate | SEMANTIC MISMATCH; add total center->allowed-histogram data |
| State/time | Current snapshot/trajectory | NOT APPLICABLE; denotation is a model set |
| Source/read/result/update | Frontier pipeline | NOT APPLICABLE; no transition event exists |
| Seed/initial condition | Seed catalog | NOT APPLICABLE |
| Boundary | Fixed/periodic/reflective gather | SEMANTIC MISMATCH as native semantics; scope/model representation owns periodicity |
| Outcome | `Advanced/Terminal/Quiescent` | SEMANTIC MISMATCH; solver query outcomes are separate |
| Trace | Dense temporal episode | NOT APPLICABLE; solver diagnostics and model encodings are separate |
| Solver | `FORMULAIC` or family rollout | SEMANTIC MISMATCH; external explicit incomplete algorithms/certificates |

This is the first categorical failure of the transition executor shell. Sharing finite alphabets, lattice offsets, histogram kernels, serialization, and error infrastructure remains meaningful, but no vacuous “zero-step rollout” or constraint `UPDATE` is introduced.

## Current Runtime Fit

| Runtime area | Finding | T31 disposition |
|---|---|---|
| `alphabets.py` | Closed finite symbolic/integer alphabets | Reuse |
| `loci.py` | Finite coordinate universes and predicates | Extract/reuse typed offsets only; no finite shape as `Z^d` |
| `neighborhoods.py` | Axis/L1/Von Neumann geometry plus temporal gathers | Reuse a topology-owned footprint value, not CA read behavior |
| `rules.py` | Aggregate/gate/lookup/callable next values | No constraint semantics; private histogram utility at most |
| `frontiers.py` | Dense time slice | Not applicable |
| `specs.py` | `Dynamics` with shape/rule/boundary | Add a separate constraint spec category, not a dynamics family |
| `rollout.py` | Family-dispatched time evolution | Must not receive a constraint branch |
| `datasets.py` | Trajectory planning/stacking | Constraint datasets require model/query/result records downstream |
| tests | No verifier/certificate/unknown/scope coverage | Add independent structural tests |
| visualization | Dense frame/trajectory views | Render verified models or solver diagnostics only downstream |

No current verifier, periodic-model proof, obstruction certificate, scoped query outcome, or honest incomplete solver exists.

## Principles Audit

- **Principle 0:** the model set/constraint relation must remain declarative. A repair trajectory or one witness does not preserve the construction.
- **Principles 1-4:** immutable domain/footprint/histogram relation, exact verifier, and explicit query outcomes are closed data; transition responsibilities are correctly absent.
- **Principle 5:** no hidden solver/search state is needed to define satisfaction. Partial assignments belong to algorithm diagnostics.
- **Principles 6-8:** infinite loci, periodic quotient coordinates, finite patch loci, solver variables, display pixels, and batch slots are separate. No finite capacity fakes `Z^d`.
- **Principles 9-10:** canonical profiles are strict constraint data presets, not solver/rollout families.
- **Principle 11:** center-conditioned histogram membership at every site is semantic; enumeration order, SAT encoding, and heuristics are incidental.
- **Principle 12:** verified model/certificate/query data precede tiles, symmetry representatives, search trees, and images.
- **Principles 13-15:** period proofs, one-bit perturbation, open/torus scope, bounded `Unknown`, and certificate replay are adversarial tests.
- **Principles 16-17:** constraints require a distinct semantic category rather than a ninth transition update. T32/T33 cannot be flags or callbacks.

Rejected shortcuts:

- repair CA/dynamics, fixed-point iteration, relaxation, belief propagation, or local recoloring presented as the constraint;
- predicate/SAT/backtracking/whole-problem callback inside the spec or a `constraint` rollout family;
- gray/unassigned as a semantic symbol, hidden search state, random seed, or solver trace as trajectory;
- one witness as the whole solution set, one failed solver as unsatisfiability, one found tile as uniqueness, or symmetry orbit as pointwise equality;
- bounded periodic/patch exhaustion as global unsat; unscoped/trusted certificates or `Unknown` collapsed into false;
- finite grids/padding/boundaries as infinite fields; open edges used as torus/infinite checks;
- CA fixed-point, totalistic next-value, tiling, energy, or graph compilation solely to claim native coverage;
- T32 oriented templates collapsed to histograms or T33 existential requirements smuggled into a global predicate/flag.

## Detailed Implementation Plan

1. Close direct/alias/proximity, figure, Notes, actual Index, split, history, allowed-block, periodicity, search/complexity, CA/ground-state, tiling, T32/T33, network, equation, solver, and observer candidates.
2. Freeze declarative total-field denotation, footprint/histogram relation, exact pointwise model identity, periodic/open scopes, verifier/violations, witnesses, finite obstructions, solver outcomes, and incompleteness.
3. Recover exact 1D profiles/de Bruijn proof, the 2D `5x5` tile, all page-227 profile classifications, and adversarial verification/certificate/scope tests.
4. Compare every responsibility with `simple_programs.md`, current runtime/tests, and prior transition stages; record the first categorical executor split.
5. Audit no-cheating constraints, variants, symmetry/views, serialization, model/query datasets, and Goal 2 dependencies.
6. Reintegrate global evidence/design/plan ledgers and write the implementation-ready constraint/verifier/solver stage.

## Goal 2 Implementation Stage

### G2-T31 — Declarative local-count models, exact verification, and scoped solver results

Dependencies: finite alphabet values; T01's semantic total-lattice/finite-realization distinction; a synthesis-selected exact lattice-point/offset value and error/serialization infrastructure. Do not depend on `Dynamics`, the transition executor, totalistic next-value rules, a SAT/solver callback, or T32/T33 semantics.

1. Add a separate constraint-owned module such as `src/ca/constraints.py` with `LatticeFootprint`, `NeighborHistogram`, and immutable `LocalCountConstraintSystem`. Validate dimension, nonzero duplicate-free offsets, total center rows, alphabet order, histogram nonnegativity/degree, and closed serialization.
2. Add exact `PeriodicLatticeModel` and `FinitePatch` representations with explicit period/origin or anchor/halo scopes. Implement exact point queries, normalization, pointwise comparison for periodic models, and no padding/boundary fallback.
3. Add pure `observed_histogram`, `satisfied_at`, `violation_at`, `verify_periodic`, and `verify_patch`. Periodic verification checks a complete fundamental domain and returns proof metadata; patch verification labels only the checked scope.
4. Add a separate constraint-query/result module with `ClaimScope` and closed `Satisfiable`, `Unsatisfiable`, `Unknown`, and `ResourceLimit` records. These must not implement or subclass transition `Advanced/Terminal/Quiescent` outcomes.
5. Add replayable `ExhaustiveFiniteObstruction` checking: derive the complete halo, enumerate every finite assignment, and prove each violates an anchor. Keep future compact proof ASTs behind independent verified types, never callbacks or trusted booleans.
6. Add a solver-owned module such as `src/ca/constraint_solvers.py` with an exact 1D de Bruijn analyzer, bounded periodic-model search, and bounded finite-obstruction search. Every returned witness/certificate rechecks independently; exhausted incomplete bounds return `Unknown`.
7. Add strict constructors for the two 1D profiles, canonical 2D black1/white2 profile, recovered `5x5` model, and page-227 profile data once independently transcribed. Keep constraint, query bounds, and solver strategy separate.
8. Add downstream symmetry-orbit, period, model-count, tile/image, search-tree, and dataset encodings. Do not represent solution sets as episodes or stack unlike query/model records into dense trajectories.
9. Add exact canonical/adversarial tests below and cross-check small finite/periodic scopes by independent brute force. Image tests are supplementary.
10. Audit exports, specs, docs, datasets, and production code for transition/family branches, callbacks, gray values, hidden bounds, one-witness collapse, false UNSAT, scope confusion, symmetry quotienting, finite-capacity claims, CA compilation, and T32/T33 flags.

Completion requires:

- constraint/footprint/histogram normalization, serialization, equality, and malformed-data tests;
- exact `0011` translations, allowed triples, de Bruijn cycle/period bound, and a no-cycle unsat certificate;
- at-least-one-unlike run tests including triple-run violations;
- exact `5x5` periodic tile verification at all 25 anchors, rotations/reflections as explicit relations, and the five-violation one-bit perturbation;
- page-227 `25` profile/classification data including the two unsatisfiable and infinite/two-family cells;
- explicit pointwise-versus-symmetry-orbit and structural-versus-extensional periodic equality tests;
- open patch/halo, torus, and infinite claim-scope separation;
- a three-anchor 1D exhaustive obstruction such as `allowed[0]={(1,1)}, allowed[1]=empty`, with independent replay;
- solver witness reverification, bounded-period exhaustion as `Unknown`, resource outcome, and search-order independence;
- no gray/model callback/solver callback/repair dynamics/transition outcome/fake finite domain tests;
- unchanged prior transition semantics, no constraint rollout branch, and all repository tests passing.

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
- No `Advanced/Terminal/Quiescent` alias for solver results and no “zero-step dynamics” wrapper around the solution set.
- No structural tile equality presented as full pointwise equality when periods/origins differ.
- No incomplete bounded search allowed to publish an ordinary exact result.

## Completion Requirements

- [ ] All names, aliases, figures, Notes, actual Index entries, splits, history, variants, observers, and relations resolved with zero silent remainder.
- [ ] Native local-count relation, total model set, exact equality, scopes, verifier, witnesses/certificates, solver outcomes, and complexity boundary reconstructed.
- [ ] Exact 1D/2D periodic models and adversarial verification/unsat/unknown/scope invariants specified.
- [ ] Current API/runtime/principles fit and transition-executor split explicit.
- [ ] Goal 2 implementation/conformance handoff and global reintegration complete.

## Stage Results

In progress. Core evidence already establishes that T31 is a declarative neighbor-count model set, not dynamics, and that verification, periodic representation, external search, incomplete outcomes, and solver certificates must remain distinct. The page-227 table, full search/variant disposition, and Goal 2 handoff remain open.
