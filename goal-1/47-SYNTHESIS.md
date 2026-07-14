# 47-SYNTHESIS

Status: **IN PROGRESS — 45/45 TYPE EVIDENCE CLOSED; FINAL INTEGRATION AND GLOBAL GATES REMAIN**.

## Current Facts

- All 45 catalog rows have complete evidence stages, zero unresolved source candidates, and an architecture disposition in `architecture-audit.md`.
- D000-D118 were reclassified from first principles after T09/T12 exposed the false equation of semantic role with storage class. D119-D140 then closed every bounded follow-on stage without restoring that mistake.
- `src/ca` is the current, CA-shaped realization and namespace of the intended SimplePrograms library. Its current fixed tensor shapes, target-coordinate frontiers, six family resolvers, and family-branched rollout are implementation limitations, not the definition of the library.
- Wolfram's common object is a finitely described transition or rewrite system. Cellular automata are its fixed-lattice, all-sites, local-read, scalar-write, snapshot-parallel preset.
- DOMAIN means the task/program's dimensional space (`t+0D`, `t+1D`, `t+2D`, and so on), with discrete or continuous status explicit. Support and topology belong to CONFIGURATION; values, colors, symbols, states, addresses, and numeric carriers belong to ALPHABET/value schemas or other typed roles.
- T31-T33, T40-T41, and T45 contain declarative definitions or relations with no canonical next configuration. Their query/verification/solution responsibilities are real library responsibilities but are not rollout.

## Updated Assumptions

### Confirmed

1. Every evidenced stepwise construction fits one branch-free, axis-polymorphic `SimpleProgram` runner.
2. Distinct source terminology does not justify a semantic class. A head, active marker, instruction marker, cursor, phase, or endpoint may be a tag, product factor, marker, or structural field subject to explicit invariants.
3. A new ALPHABET, CONFIGURATION/support, FRONTIER, NEIGHBORHOOD, closed RULE schema, UPDATE policy, seed constructor, invariant, result reason, or lossless representation can extend the common construction without creating a family executor.
4. UPDATE policies with different conflict and structural-composition semantics need distinct closed policy data/evaluators, but they remain implementations of one UPDATE axis invoked by one runner.
5. Multiway rewriting does not require a multiway executor. `StepResult[C]` already admits an exact finite successor set and separate derivation witnesses.
6. The smallest non-rollout companion is one declarative definition/relation/query layer. Constraints, functions, exact-denotation representation queries, and differential problems instantiate that layer with different closed syntax and proof obligations.

### Rejected

1. The current tensor/writable-target shape of `src/ca` is not the SimplePrograms abstraction.
2. One runtime class per catalog row, family, state-role name, or source decomposition is not warranted.
3. A common Python base class is not semantic reuse when each subclass hides the whole construction in an arbitrary callback.
4. Compilation to cellular automata is not native reuse unless a complete, one-native-step, lossless commuting representation is established. A multi-step simulation remains an explicit compiler/relation.
5. Static model sets, function definitions, and general PDE relations must not receive fake seeds, frontiers, or time steps merely to pass through rollout.
6. Goal 2 should not allocate one implementation stage per catalog type. It should implement shared mechanisms once while retaining exactly one conformance obligation per type.

## Big Picture Objective

Derive the smallest cohesive construction algebra supported by all 45 evidence stages, identify the exact non-rollout boundary, and give Goal 2 a concrete revision target for `simple_programs.md` and `src/ca` without implementing runtime code in Goal 1.

## Synthesis Result

There is **one execution algebra** and **one non-execution declarative algebra**.

### 1. Step/rewrite execution

```text
SimpleProgram[C, L, R, W]:
    DOMAIN
    ALPHABET_OR_VALUE_SCHEMA
    CONFIGURATION_SCHEMA
    FRONTIER
    NEIGHBORHOOD
    RULE
    UPDATE

RunSpec[C]:
    PROGRAM
    SEED_OR_INITIAL_CONFIGURATION
    REALIZATION
    HORIZON_AND_EXTERNAL_STOPS

step(program, state) -> StepResult[C]:
    validate state against program.configuration_schema
    active = program.frontier.select(state)
    reads  = program.neighborhood.read(state, active)
    writes = program.rule.apply(active, reads)
    result = program.update.apply(state, active, writes)
    validate every successor against program.configuration_schema
    return result
```

Every line is a typed success/failure sum. A failure becomes one common no-commit `StepResult` and suppresses later semantic work. Specifications use sealed structural descriptors and versioned codecs; they do not contain unrestricted callables, evaluator strings, host expressions, or hidden producer objects.

SEED remains a first-class SimplePrograms-library responsibility and must produce one complete valid event-zero configuration, but a concrete seed, horizon, realization, or external stop is run/preset identity rather than transition-program identity. This is why T08 can generalize initial-condition construction without changing execution and why T42's strict `(0,)` seed is absent from its transition table identity.

### 2. Declarative definition/relation/query

```text
DeclarativeSystem[D, Q, A]:
    DEFINITION_OR_RELATION
    SCOPE
    QUERY
    RESULT_SCHEMA
    CERTIFICATE_SCHEMA

answer = evaluate_or_verify(definition, scope, query)
```

This layer constructs and validates immutable mathematical definitions, relations, candidates, queries, results, witnesses, and certificates. A solver or numerical method is an explicit implementation relation with its own scope and diagnostics. It is not an UPDATE and its work trace is not the mathematical object.

T31-T33 instantiate model-set relations; T41 instantiates closed function definitions; T40 is an arity-zero exact-denotation/representation specialization with separately identified work programs; T45 instantiates differential equations/problems/solution relations. When an IVP, coefficient algorithm, verifier search, or other computation has an evidenced step law, that work object may independently be a `SimpleProgram`; this does not turn the declarative object itself into rollout.

T39 is intentionally mixed: its consecutive-divisor sieve is a SimpleProgram, while direct integer filters, streams, and arithmetic measurements are declarative queries/observers. The catalog obligation preserves both without making the query siblings into steps.

## The Irreducible Axes

| Axis | Semantic responsibility | Required forms established by the catalog | What it must not absorb |
|---|---|---|---|
| DOMAIN | Dimensional task/program space and discrete/continuous status | `t+0D`, `t+1D`, `t+2D`, `t+3D`, generic `t+dD`; continuous-coordinate variants | Support shape, topology, alphabet, precision, head states, addresses |
| CONFIGURATION | Complete Markov state: labeled/structured support or topology plus invariants | Fixed/total/sparse fields, words, keyed banks, trees through lossless token views, occurrence bags, rooted graphs, exact scalars, prefixes, survivor fields | Trace history, rendering, solver object, hidden cursor, opaque whole-machine cell |
| ALPHABET / VALUE | Closed label and value schemas | Finite ordered alphabets, products, tagged unions, naturals/rationals/algebraics, declared represented reals, prototypes/poses, markers and addresses | Palette, DOMAIN, arbitrary host objects, implicit float coercion |
| SEED | One complete valid event-zero configuration or typed law/constructor for one | Exact states, deterministic constructors, complete-configuration laws, finite-cylinder laws, explicit realizations | Per-step RNG, family choice, hidden history, transition program identity |
| FRONTIER | Applicable rule-firing loci, occurrences, matches, or structural sources | All sites/occurrences, unique tags/markers/endpoints, predicate composition, first/every match, prefix/source spans, graph vertices | Merely writable tensor coordinates, verification anchors, solver search nodes |
| NEIGHBORHOOD | Ordered or named information visible to each selected source from the old snapshot | Stencils, self/product reads, spans/prefixes, full explicit prefixes, paths/reach signatures, named-register access | Destination preservation data not natively read, callbacks, implicit boundaries |
| RULE | Closed typed transformation from source/read data to writes or replacements | Complete tables, restricted/factorized tables, closed numeric/expression ASTs, blocks/spans/patches, movement intentions, child proposals | UPDATE conflict resolution, mutable host evaluator state, unrestricted formula escape |
| UPDATE | Atomic composition/schedule turning old state plus selected typed writes into exact successor configuration(s) | Keyed assignment/movement, ordered generation/edit/mosaic, bag replacement, graph replacement, exact successor-set merge | Catalog dispatch, observer work, hidden schedule, solver or numerical method |
| RESULT / TRACE | Successors, outcome, events, witnesses, provenance, and replay data | Finite exact successors; `Advanced`, `Quiescent`, `Terminal`, `Invalid`, `Error`; lineage and derivation witnesses | Lossy chosen ancestry, padded arrays as state, IDs as authority, rendering identity |
| REPRESENTATION | Explicit lossless codec or qualified approximation/relation | Tagged/product views, sparse/default fields, positional codes, token words, canonical graph codecs, fixed numerical realizations | Silent quotient, invented inverse, multi-step simulation called one-step reuse |

These axes are substantive. They do not become vacuous merely because they share one runner: the runner knows only their typed interfaces, while each specification contains complete closed data needed to execute and reproduce a step.

## UPDATE Is One Axis, Not One Data Shape

The catalog establishes the following closed policy forms. They are not separate executors.

| Policy form | Smallest semantics | Concrete reason scalar target assignment alone is insufficient |
|---|---|---|
| Atomic keyed writes and semantic movement | Resolve all source-bound assignments/movements from one snapshot, validate ownership/collisions/invariants, then commit together | T09/T12/T25 must preserve the old destination symbol while moving a unique tag; T19 updates a named register and marker atomically |
| Ordered structural composition | Consume selected old occurrences/spans and compose emitted blocks in declared source/child order; includes single/multi-span edit and ranked mosaic assembly | T13 changes support length; T17 deletes a prefix and appends remotely; T26 validates rank-two block compatibility; padding would invent capacity and lineage |
| Multiplicity-preserving bag replacement | Consume parent occurrences and bag-union posed children with parent/slot lineage | T27 permits coincident occurrences with equal footprints but distinct frames/descendants; keyed-set assignment would collapse semantic multiplicity |
| Rooted graph structural commit | Resolve old-snapshot paths, allocate distinct fresh identities, rewire ports atomically, and project from the preserved root | T29 creates incidence and identity not expressible as label writes on a fixed support |
| Exact finite successor-set merge | Build each branch independently, exact-deduplicate configurations, and retain every derivation witness | T30 has multiple native successors and equal children reached by different rules/positions/parents |

The distinction is therefore `UPDATE` policy semantics, not `rollout_turing`, `rollout_substitution`, `rollout_network`, or `rollout_multiway`.

## Uniform `StepResult`

```text
StepResult[C] = {
    successors: FiniteExactSet[C],
    outcome: Advanced | Quiescent | Terminal | Invalid | Error,
    events: tuple[TypedEvent, ...],
    witnesses: tuple[TypedWitness, ...],
    provenance: StructuralProvenance
}
```

- Deterministic advancement has one successor.
- A multiway event has any finite number of exact successors.
- Terminal, invalid, and error outcomes normally have none and retain the inspected final state in the typed outcome/event envelope where required.
- Event-free quiescence may retain one explicit self-successor.
- Equal successor values do not erase distinct derivations.
- A failed axis commits nothing and fabricates neither a successor nor an event.
- Transition results remain distinct from declarative query/solver results.

## Reuse and Equivalence Tests

Three different claims require three different proofs.

1. **Configuration representation.** A map `e` must be injective with an explicit inverse on its invariant-valid image, preserve every semantic state component and outcome, require no hidden interpreter, and commute at native step granularity:

   ```text
   map_step_result(e, step_A(s)) = step_B(e(s))
   ```

   Here `map_step_result` maps successors and every representation-dependent event, witness, and provenance reference while preserving the outcome exactly; successor equality alone is insufficient.

2. **Program/rule codec.** Encode/decode must round-trip structural program data, and the decoded RULE must be denotationally equal on every admitted input. A compact totalistic table is not a configuration encoding.
3. **Implementation relation.** A compiler, numerical method, solver, finite realization, or multi-step simulation must keep source and target identities, scope, approximation/proof strength, and correspondence evidence. It is not native reuse unless the stronger one-step representation test also holds.

The T09/T12 composite alphabets, T20 token view, T36 canonical digit view, T39 finite survivor pack, and T42 product/tagged views satisfy the first test on stated invariant-valid images. T03/T21-T24 compact rule schemas satisfy the second. General CA emulations and PDE discretizations satisfy at most the third.

## Catalog-Wide Construction Reduction

| Smallest shared construction | Catalog obligations | Count |
|---|---|---:|
| Fixed-support snapshot assignment plus closed table/map schemas | T01-T07, T21-T24, T44 | 12 |
| Event-zero configuration/constructor/law axis over an unchanged program | T08 | 1 |
| Visible tag/marker/key roles plus atomic assignment/movement | T09-T12, T19, T25 | 6 |
| Ordered support, source selection, structural emission/edit/mosaic | T13-T18, T20, T26, T28, T37-T38, T42 | 12 |
| Exact scalar/field assignment with closed unary or sieve RULE data | T34-T36, T39, T43 | 5 |
| Multiplicity-preserving occurrence-bag replacement | T27 | 1 |
| Rooted port-graph structural replacement | T29 | 1 |
| Finite successor-set lift over literal ordered rewrite | T30 | 1 |
| Declarative model-set relation/query/certificate layer | T31-T33 | 3 |
| Closed definition/representation/differential query layer | T40-T41, T45 | 3 |
| **Total** | **Every T01-T45 catalog obligation exactly once** | **45** |

These groups organize implementation and conformance; they are not runtime family tags. A catalog ID may identify a preset or test fixture, but it never selects execution behavior.

## Genuine Rollout Nonfits

The following counterexamples justify the declarative boundary.

- **T31-T33 model sets:** one constraint denotes zero, one, many, or infinitely many total fields. Nothing in the relation chooses one model as the next state. Verification anchors are observations; solver decisions are scoped query results. A repair/search algorithm would be an additional program, not the constraint.
- **T41 function definitions:** a function definition maps an argument to a value but supplies no canonical argument sequence. Treating expression-tree traversal or requested sample order as time makes the client query schedule into hidden state.
- **T45 PDE relations:** an equation plus region does not choose initial/boundary data, a solution, a time orientation, or a solver. Only a separately posed and justified IVP derives evolution; a discretizer or integrator remains an explicit implementation relation.
- **T40 direct representations:** an exact constant definition can answer an indexed representation query without generating every earlier digit/coefficient through a single canonical algorithm. Mandatory prefix rollout would invent an algorithm and state. Its explicit coefficient algorithms still fit the common runner as distinct work programs.

These are absences of canonical stepwise evolution, not evidence for four more executors.

## Evidence-Backed Boundaries Left for Goal 2

No unresolved contradiction remains, but implementation must preserve these honest boundaries:

1. **Stochastic transition semantics:** T08 supplies event-zero laws only. Goal 2 must not infer probability-bearing transitions or hide RNG state. A later evidence stage may add a replayable draw-input/state construction or a probability-measure successor result.
2. **First-class continuous-time flow:** the catalog closes discrete step systems and declarative continuous relations, but does not yet establish a common native flow/semigroup interface or continuous-time trace contract. A separately posed evolution may be supported only after its state, time parameter, solution law, and evidence are explicit; it must not be fabricated from a PDE relation or numerical integrator.
3. **T28 adaptive unequal subdivision:** the source establishes a warning but not enough carrier, incidence, matching, or commit semantics. The profile remains typed `Unsupported`, while the compatible rectangular profile is complete.
4. **T29 sequential network evolution:** primary evidence does not fix selection order, projection anchor, or move timing. The parallel profile is complete; the sequential profile remains typed `Unsupported` rather than receiving an invented convention.
5. **Exact-real backend:** named transcendental values, exact piecewise comparisons, and replayable invariant certificates require an explicit backend/profile choice. Unsupported exact requests must fail structurally; they must never fall back to machine floats.
6. **Serialization and registry versioning:** construction-time decoding needs a closed versioned registry for axis descriptors and presets. That registry may parse data but must never become execution-time catalog dispatch.

## Proposed Revision Strategy

1. Revise `simple_programs.md` from a fixed-array CA schema into the axis contract above, retaining its selector/access work where semantics already match.
2. Evolve `src/ca` in place as the SimplePrograms implementation. The package path is historical; do not build a second library plus compatibility bridge.
3. Replace the current family-branched rollout with one generic `step` and repeated-run routine over closed axis descriptors.
4. Generalize current alphabets, loci/selectors, neighborhoods, rules, seeds, specifications, and raw traces; add configuration/support, UPDATE, outcome, structural value, relation/query, certificate, and serialization responsibilities only where the audit establishes them.
5. Migrate current CA constructors and manifests directly to ordinary SimpleProgram presets. Do not retain a legacy executor, `family` switch, or adapter that secretly calls it.
6. Implement the dependency-aware stages and one-per-row conformance matrix in `goal-2-handoff.md`.

## No-Cheating Gates

- The generic runner contains no catalog ID, family tag, type-name switch, rule-family branch, or executor lookup.
- Public semantic schemas contain no unrestricted `Callable`, `eval`, formula string, host CAS object, opaque object cell, or `Any` payload that can carry a whole interpreter.
- Every closed descriptor has structural validation, versioned serialization, and mutation/fail-closed tests.
- Every control role needed for the next step is present in configuration or immutable program data and round-trips through traces.
- Every claimed representation has an inverse-on-image and full-result one-step commutation test, including outcomes, successors, events, and witnesses.
- Fixed capacity, padding, crops, finite boxes, raster dimensions, array memory order, and visualization coordinates never define native semantics unless the evidence stage says so.
- Declarative relations never pass through `step`; derived work programs retain separate identities and correspondence evidence.
- Catalog presets construct ordinary axis values. Catalog IDs appear in conformance and provenance, never in execution branching.

## Verification

Before this stage becomes complete:

- [ ] `goal-1/goal-2-handoff.md` defines dependencies, target files, tests, completion evidence, and re-derivation triggers for every Goal 2 stage.
- [ ] Its coverage matrix contains every CSV row exactly once and no duplicate T-ID.
- [ ] D141 records this synthesis in `design-ledger.md`; `architecture-audit.md`, `evidence-index.md`, and `0-plan.md` agree.
- [ ] T42's completion checklist and Stage Results are closed against the final frozen oracles.
- [ ] All three T42 oracles pass normally and under their documented portability/fail-closed modes.
- [ ] Repository tests, Markdown fence checks, Goal-1-only scope checks, and `git diff --check` pass.

## Stage Results

Pending Goal 2 handoff, global synchronization, and final verification.
