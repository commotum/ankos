# Goal 2 Implementation and Conformance Handoff

Status: **COMPLETE — IMPLEMENTATION-READY DEPENDENCY PLAN, EXACT 45-ROW COVERAGE, AND 45-LEAF CONFORMANCE DEPENDENCIES GLOBALLY VERIFIED**.

## Objective

Implement the evidence-grounded SimplePrograms architecture in `src/ca` without repeating Goal 1 research, without introducing a second executor, and without losing the separate conformance identity of any row in `ref/notes/CA-Types.csv`.

This handoff is subordinate to the evidence and semantic boundaries in the 45 type-stage files, `architecture-audit.md`, `design-ledger.md`, and `47-SYNTHESIS.md`. If implementation pressure contradicts those records, stop and re-derive the affected Goal 1 decision; do not add a family switch, second semantic/execution compatibility path, callback, or lossy representation.

## Canonical Book Source

All source lookup for this handoff must use the repository's canonical
*A New Kind of Science* Markdown corpus:

- [Source overview](../ref/A-New-Kind-of-Science/README.md)
- [Ordered contents and links to all 29 book documents](../ref/A-New-Kind-of-Science/Contents.md)

Search and cite the linked front matter, chapters, Notes, Index, and Colophon
documents directly. These files and their colocated figures are the only live
book-source surface for Goal 2. Goal 1 stage files remain the design and
conformance authorities, but any quotation, example, rule table, or fixture
used by an implementation must be rebound to the canonical document that
contains it.

## Target Architecture

`src/ca` remains the package path and is revised **in place** as the SimplePrograms library. The path does not delimit the semantics to cellular automata. Do not build a second `simple_programs` package and route old calls through a legacy CA executor.

```text
active = FRONTIER.select(configuration)
reads  = NEIGHBORHOOD.read(configuration, active)
writes = RULE.apply(active, reads)
next   = UPDATE.apply(configuration, active, writes)
```

One generic runner invokes those axes and returns `StepResult[Configuration]`. Cellular automata, mobile automata, Turing machines, substitutions, register machines, scalar maps, sieves, geometric replacements, networks, and multiway rewrites differ in typed axis data and invariants, never in the runner selected.

Declarative constraints, closed function/constant definitions, and differential problems use a sibling immutable definition/relation/query/certificate layer. They do not pass through the runner unless a separately identified work program has its own complete step law.

## Non-Negotiable Implementation Rules

1. DOMAIN is dimensional task/program space. CONFIGURATION owns support/topology and invariants; ALPHABET/value schemas own labels and semantic payloads.
2. Every specification is closed structural data with explicit versioning and validation. No public semantic field accepts unrestricted `Callable`, `eval`, formula text, host CAS objects, generators, iterators, or `Any` as an interpreter escape.
3. Every next-step dependency is in immutable program data or visible configuration. IDs and digests are derived provenance/cache data, never authority.
4. `step` and repeated rollout contain no catalog ID, family tag, type-name branch, or executor lookup. Construction-time decoding may use a versioned registry of closed axis tags; execution may not dispatch on catalog identity.
5. UPDATE policies are typed implementations of one axis. Do not assign ordinal “update-law” classes or construction-named executors.
6. A preset constructs an ordinary `SimpleProgram`; it does not register a rollout function.
7. A representation claim requires an inverse on the invariant-valid image and one-native-step full-result commutation. A compiler, numerical method, or simulation that fails that test remains an explicit relation.
8. Public execution is migrated atomically to the new model. Do not retain a `LegacyDynamics`, old family rollout, fallback conversion, or shadow semantic implementation. A deprecated construction-time façade is permitted only if its total lossless mapping immediately returns an ordinary `SimpleProgram` and never selects or implements execution.
9. Goal 1 raster assets remain evidence fixtures under their recorded authority levels. Hash binding or limited transcription does not authorize pixel-decoded rules.
10. Unsupported evidence boundaries fail with typed reasons. They are never filled with textbook defaults or implementation convenience.

## Planned Module Responsibilities

The exact internal split may be refined without changing the semantic ownership below.

| Target file or area | Responsibility |
|---|---|
| `src/ca/domains.py` | Discrete/continuous dimensional DOMAIN descriptors; no topology or value semantics |
| `src/ca/alphabets.py` | Finite ordered, product, and tagged-union label schemas and validation |
| `src/ca/values.py` | Exact integer/rational/algebraic and explicitly represented/declared numeric value schemas |
| `src/ca/configurations.py` | Support/topology descriptors, complete configuration carriers, invariants, canonical equality |
| `src/ca/loci.py` | Typed locus/address/path/span/occurrence data and composable predicates/orderings |
| `src/ca/frontiers.py` | Closed firing-source selectors and program-coupled applicability views |
| `src/ca/neighborhoods.py` | Closed old-snapshot access patterns and typed read batches |
| `src/ca/rules.py` | Closed rule tables/ASTs and typed writes/replacements; no commit behavior |
| `src/ca/updates.py` | Closed atomic composition policies for keyed, ordered, bag, graph, and successor-set writes |
| `src/ca/seeds.py` | Complete event-zero configurations, constructors, classes/laws, and explicit realizations |
| `src/ca/outcomes.py` | `StepResult`, typed outcomes/failures, exact successor sets, query result sums |
| `src/ca/traces.py` | Raw states/events/witnesses/lineage/provenance and replay validation |
| `src/ca/expressions.py` | Bound closed numeric/function/differential expression syntax shared by rules and queries |
| `src/ca/relations.py` | Closed model-set and differential relations, verification, scopes, witnesses, certificates |
| `src/ca/queries.py` | Immutable definitions, scoped queries, exact/certified/approximate results, solver-adapter contracts |
| `src/ca/serialization.py` | Versioned structural codecs and construction-time axis/preset registry |
| `src/ca/specs.py` | `SimpleProgram` composition, cross-axis validation, program construction from closed data |
| `src/ca/rollout.py` | One generic `step`, repeated run, and batch orchestration; no semantic family branches |
| `src/ca/datasets.py`, `src/ca/viz/` | Downstream planning/export/rendering over raw traces; never program state or semantics |
| `tests/conformance/` | One authoritative obligation per T01-T45 plus shared commuting/codec/adversarial suites |

## Dependency Order

| Stage | Depends on | Delivers | Catalog obligations closed here |
|---|---|---|---|
| G2-00 | Goal 1 complete | Baseline, migration contract, canonical fixture manifest | None |
| G2-01 | G2-00 | Structural DOMAIN/value/configuration/codec kernel | None |
| G2-02 | G2-01 | Branch-free axes, runner, results, traces, failures | None |
| G2-03 | G2-02 | Fixed-support snapshot assignment and finite-alphabet CA presets | 12 |
| G2-04 | G2-03 | Visible tag/marker roles and atomic movement/keyed writes | 6 |
| G2-05 | G2-02, G2-03 | Exact scalar/positional/map rules and continuous-valued fields | 5 |
| G2-06 | G2-02 | Declarative model-set relation/query/certificate core | 3 |
| G2-07 | G2-05, G2-06 | Closed function/constant/differential definitions and queries | 3 |
| G2-08 | G2-02 | Multiplicity-preserving occurrence bags | 1 |
| G2-09 | G2-04, G2-05, G2-07, G2-08 | Ordered generation/edit/mosaic substrate, sieve composition, and scheduled presets | 13 |
| G2-10 | G2-02 | Rooted port-graph access and structural commit | 1 |
| G2-11 | G2-09 | Finite successor-set lift and branch-witness merge | 1 |
| G2-12 | G2-03..G2-11 | Registry, migration, datasets/viz, all-catalog verification | None; verifies all 45 |

The ordering is semantic, not a family hierarchy. For example, G2-09 depends on G2-07 only because the T42 preset consumes a complete T40 result, and on G2-08 only to verify T26's restricted posed-bag representation.

### Leaf conformance order inside shared stages

Each catalog row is one leaf obligation `C01` through `C45`, executed inside exactly one shared implementation stage. These dependencies order proofs and reuse; they never select runtime behavior.

| Shared stage | Required leaf order |
|---|---|
| G2-03 | `C01 -> C02 -> C03 -> {C04,C05,C06,C21}`; `C07` after C02; C08 independent; `C21 -> C22 -> C23 -> C24` |
| G2-04 | `C09 -> {C10,C11,C12}`; C19 independent; C25 after C12, C21, and C24 |
| G2-05 | `C34 -> {C35,C36,C43}`; C44 after C01 and C43 |
| G2-06 | `C31 -> C32 -> C33` |
| G2-07 | C41 first; C40 after C34, C36, C41, and C43; C45 after C31, C41, and C44 |
| G2-08 | C27 |
| G2-09 | C14, C16, and C17 after C13; C26 after C13 and C27; C15 after C14; C18 after C17; C20 and C37 after C16; C28 after C14, C21, and C26; C38 after C37; C39 after C37; C42 after C13 and C40 |
| G2-10 | C29 |
| G2-11 | C30 after C16; its compressed/folded graph remains a trace/view relation rather than a T29 runtime dependency |

The following matrix is normative. `Cnn` is the leaf obligation for `Tnn`; `—` means that the leaf has no prerequisite catalog proof beyond its shared-stage substrate. These are direct leaf dependencies, while the stage DAG above supplies transitive implementation dependencies.

| Catalog row | Leaf | Direct leaf dependencies |
|---|---|---|
| T01 | C01 | — |
| T02 | C02 | C01 |
| T03 | C03 | C02 |
| T04 | C04 | C03 |
| T05 | C05 | C03 |
| T06 | C06 | C03 |
| T07 | C07 | C02 |
| T08 | C08 | — |
| T09 | C09 | — |
| T10 | C10 | C09 |
| T11 | C11 | C09 |
| T12 | C12 | C09 |
| T13 | C13 | — |
| T14 | C14 | C13 |
| T15 | C15 | C14 |
| T16 | C16 | C13 |
| T17 | C17 | C13 |
| T18 | C18 | C17 |
| T19 | C19 | — |
| T20 | C20 | C16 |
| T21 | C21 | C03 |
| T22 | C22 | C21 |
| T23 | C23 | C22 |
| T24 | C24 | C23 |
| T25 | C25 | C12, C21, C24 |
| T26 | C26 | C13, C27 |
| T27 | C27 | — |
| T28 | C28 | C14, C21, C26 |
| T29 | C29 | — |
| T30 | C30 | C16 |
| T31 | C31 | — |
| T32 | C32 | C31 |
| T33 | C33 | C32 |
| T34 | C34 | — |
| T35 | C35 | C34 |
| T36 | C36 | C34 |
| T37 | C37 | C16 |
| T38 | C38 | C37 |
| T39 | C39 | C37 |
| T40 | C40 | C34, C36, C41, C43 |
| T41 | C41 | — |
| T42 | C42 | C13, C40 |
| T43 | C43 | C34 |
| T44 | C44 | C01, C43 |
| T45 | C45 | C31, C41, C44 |

## Detailed Goal 2 Stages

### G2-00 — Freeze the Baseline and Migration Contract

**Depends on:** completed Goal 1.

**Files:** `pyproject.toml`, `README-V2.md`, `simple_programs.md`, current `src/ca/*.py`, current `tests/*.py`, new `tests/conformance/catalog-manifest.json`.

**Implementation:**

- Record the current 141-test baseline and classify each assertion as canonical evidence, retained public behavior, or incidental Phase 1 behavior.
- Create a machine-readable 45-row conformance manifest joining CSV ID, exact name, Goal 1 stage, Goal 2 stage, canonical fixtures/oracles, and evidence authority.
- State the in-place migration: `SimpleProgram` replaces the current CA-only `Dynamics` semantic contract; current CA constructors become direct presets; repeated `rollout` becomes generic iteration of `step`; no legacy executor survives. Decide separately whether a deprecated construction-only façade is worth retaining under rule 8.
- Update project language to “SimplePrograms library based on *A New Kind of Science*” while retaining `ca` as the package path.
- Pin the Python/NumPy serialization assumptions that must be removed from semantic identity.

**Tests/evidence:** current suite passes before semantic changes; CSV/manifest join proves 45 unique rows; fixture hashes match Goal 1; source inventory is frozen.

**Complete when:** the baseline and migration manifest are reviewed, every current behavior has a disposition, and no promised compatibility surface requires two semantic implementations or execution paths.

**Re-derive if:** a current behavior claimed as canonical contradicts a Goal 1 oracle, or package migration would require a second executor rather than a direct replacement.

### G2-01 — Structural Schema, Values, Configurations, and Codecs

**Depends on:** G2-00.

**Files:** `src/ca/domains.py`, `alphabets.py`, `values.py`, `configurations.py`, `loci.py`, `serialization.py`, `specs.py`; `tests/test_domains.py`, `test_alphabets.py`, `test_values.py`, `test_configurations.py`, `test_serialization.py`.

**Implementation:**

- Add explicit discrete/continuous `t+dD` descriptors without embedding support shapes.
- Add finite ordered alphabets, product factors, tagged unions, semantic address/key types, and exact cardinality/order validation.
- Add exact naturals, integers, reduced rationals, algebraic values, sealed structural exact-denotation profiles with typed `Unsupported` evaluation where no backend exists, and explicit represented-real profiles. Machine floats never impersonate exact values, and an exact-denotation profile never contains a lazy evaluator or CAS object.
- Add complete carriers for fixed/total/sparse fields, finite words, keyed products, scalars, prefixes, bags, and rooted graphs as structural schemas, while delaying their UPDATE behavior to later stages.
- Add invariant combinators such as exactly-one tag, uniform product factor, nonempty word, total default-plus-overrides field, graph port/root constraints, and carrier closure.
- Define canonical structural equality, identity, provenance, and JSON-safe bigint/exact-value codecs. Digests are derived from validated structure.
- Implement a versioned construction-time registry for closed descriptor tags. Unknown, duplicate, shadowed, or extra fields fail closed.

**Tests/evidence:** product/tag round trips; bare `TapeSymbol | HeadState` information-loss adversary; exactly-one violations; signed/large bigint and rational round trips; sparse/default equivalence; key-kind separation; unknown/duplicate/shadowed codec mutations; digest-not-authority tests.

**Complete when:** every carrier required by the architecture matrix can be represented without opaque or unvalidated object cells, callbacks, hidden control, whole-interpreter payloads, or catalog-specific state classes. A validated product/tag value may use an object-array storage strategy without making that storage representation semantic.

**Re-derive if:** a carrier cannot expose all next-step information, canonical equality depends on rendering/storage order, or one schema must contain a hidden interpreter.

### G2-02 — Generic Axes, Runner, Outcomes, and Traces

**Depends on:** G2-01.

**Files:** `src/ca/frontiers.py`, `neighborhoods.py`, `rules.py`, new `updates.py`, `outcomes.py`, `traces.py`, revised `specs.py`, `rollout.py`; focused tests plus `tests/conformance/test_runner_contract.py`.

**Implementation:**

- Define typed selection/read/write batches tied to immutable snapshot/program identities.
- Generalize FRONTIER from next-tensor targets to firing sources, with composable predicates, ordering, occurrence identity, and program-coupled applicability where required.
- Generalize NEIGHBORHOOD from offset tensors to closed access patterns over loci/spans/paths/named keys while retaining ordered offset stencils.
- Define closed RULE result schemas; RULE never commits, resolves conflicts, allocates global identity, or reads undeclared data.
- Implement UPDATE as a closed policy axis. Start with atomic keyed assignments and typed no-commit validation; later stages add structural policies.
- Implement one generic `step` exactly in the four-call order and generic repeated/batch traversal over `StepResult`.
- Add exact finite successor sets and `Advanced | Quiescent | Terminal | Invalid | Error` outcomes with typed reasons, events, witnesses, and provenance.
- Make every axis fallible through one generic bind; later axes do not execute after failure.
- Separate raw semantic traces from coordinates, padding, batches, and renderings.
- Keep this runner non-public scaffolding until G2-12 performs the single atomic public cutover. Intermediate conformance stages may test it directly, but no released/public call graph may expose both the old and new executors.

**Tests/evidence:** AST/source inspection forbids catalog/family dispatch in `step` and repeated run; axis-spy ordering; snapshot identity; no-commit failure; invariant validation before/after; deterministic singleton, quiescent self, terminal empty, and exact multi-successor envelopes; witness retention; replay; batch/scalar parity.

**Complete when:** current fixed-field behavior can be expressed by ordinary axis data, the runner has no knowledge of any catalog construction or closed policy tag beyond the typed interface it invokes, and the public API still exposes exactly one execution path pending the G2-12 cutover.

**Re-derive if:** a type needs runner-visible family information, failure requires an ad hoc early-return branch, or result data cannot distinguish outcome from successor cardinality.

### G2-03 — Fixed-Support Assignment and Finite-Alphabet CA-Preset Conformance

**Depends on:** G2-02.

**Files:** `src/ca/configurations.py`, `loci.py`, `frontiers.py`, `neighborhoods.py`, `rules.py`, `updates.py`, `seeds.py`, `specs.py`; fixed-field preset constructors; `tests/conformance/test_t01_t08.py`, `test_t21_t24.py`.

**Implementation:**

- Implement generic fixed-incidence supports, total fields, finite realizations/quotients, boundary reads, `AllSites`, named ordered offsets, snapshot reads, same-site assignments, and atomic parallel commit.
- Implement complete positional tables, exact fixed-arity sum quotients, predicate counts, orbit/property restrictions, factor maps, arbitrary-precision codes, and explicit frame/table permutations as closed RULE data.
- Implement T04/T05 as strict presets, T06/T07 as validated program restrictions/properties, and T08 as independent event-zero configuration constructors/laws/realizations over an unchanged program.
- Support generic square/cubic/higher-dimensional fixed incidence and schema-tagged site/kind rule banks without eager impossible tables or runtime RNG.
- Preserve native support versus finite work/crop/rendering distinctions.

**Tests/evidence:** all T01-T08 and T21-T24 canonical tables, counts, codecs, asymmetric trajectories, aggregate counterexamples, frame permutations, old-snapshot adversaries, seed/configuration distinctions, arbitrary-precision codes, and recorded asset guards.

**Complete when:** the nine evolving fixed-support obligations T01-T05 and T21-T24 pass through the unmodified generic runner; T06/T07 remain pure validated program properties/restrictions; T08 supplies typed event-zero run inputs to an unchanged program; and no preset name occurs in execution code.

**Re-derive if:** a compact rule schema cannot denotationally round-trip, a boundary/shape becomes native semantics accidentally, or an initial-condition law affects per-step execution.

### G2-04 — Visible Control Roles, Movement, and Keyed Atomic Writes

**Depends on:** G2-03.

**Files:** `src/ca/alphabets.py`, `configurations.py`, `loci.py`, `frontiers.py`, `neighborhoods.py`, `rules.py`, `updates.py`, `traces.py`; `tests/conformance/test_t09_t12.py`, `test_t19.py`, `test_t25.py`.

**Implementation:**

- Add tag/marker-selecting frontiers and payload projection reads over composite alphabets and keyed product configurations.
- Add semantic movement intentions whose destinations are resolved by CONFIGURATION topology during UPDATE, not exposed to RULE unless natively read.
- Atomically preserve the old destination value, rewrite the source, move the tag/payload, validate ownership/collision, and recheck exactly-one invariants.
- Support fixed-block writes and finite activity-factor union as closed write combiners without changing the runner.
- Support named register/instruction topology, typed register/address keys, active-instruction selection, referenced-register reads, and marker writes.
- Add total sparse tapes/planes and semantic movement ports/heading actions; keep compact rule tables distinct from arbitrary CA tables over composite labels.

**Tests/evidence:** factored/tagged one-step and result commutations; zero/two-head adversaries; underlying destination preservation; native-radius versus compiled-radius counterexample; finite activity union; register bigints/branches/past-end outcomes; 2D movement/frame/hex/Langton cases; no `SingleControl` or `TransitionControl` class.

**Complete when:** the six mapped obligations use ordinary composite values/frontiers/reads/writes and one atomic UPDATE implementation, with no mobile/Turing/register executor.

**Re-derive if:** complete state cannot be recovered from a representation, movement needs undeclared destination reads in RULE, or collision semantics are selected by catalog identity.

### G2-05 — Exact Scalar, Positional, Iterated-Map, and Continuous-Field Programs

**Depends on:** G2-02 and G2-03.

**Files:** `src/ca/values.py`, `expressions.py`, `configurations.py`, `frontiers.py`, `neighborhoods.py`, `rules.py`, `updates.py`, `traces.py`; `tests/conformance/test_t34_t36.py`, `test_t43.py`, `test_t44.py`.

**Implementation:**

- Implement the exact discrete `t+0D` singleton event with unique locus, self read, closed unary RULE AST, same-site assignment, and ordinary atomic UPDATE.
- Add add/multiply, complete Euclidean-residue, ordered-fraction partial, positional encode/reverse/decode/add, and closed exact/piecewise map nodes with structural program identity.
- Preserve canonical versus fixed/growing-width positional representations and prove only valid lossless commutations.
- Separate ideal exact, certified enclosure, tracked significance, fixed binary, and fixed decimal feedback for iterated maps.
- Add continuous-valued fixed-field carriers plus closed affine-aggregate/scalar-map RULE profiles over G2-03 while keeping exact, certified, tracked, and represented feedback distinct.

**Tests/evidence:** arbitrary-precision scalar events; missing-branch no-commit; ordered-fraction priority; canonical/fixed/grow width-loss adversary; exact rational maps; declared-precision fixtures; discontinuity/partiality and fixed-point event semantics; T44 exact field profiles, old-snapshot updates, aggregate/map factoring, and represented-feedback boundaries.

**Complete when:** all five mapped obligations use the generic runner and exact value schemas without scalar/map/continuous-CA state or executor classes.

**Re-derive if:** equality needs tolerance, exact requests fall back to float, a representation hides width/state needed for the next event, or a pure measurement is being evolved.

### G2-06 — Declarative Model Sets, Verification, and Certificates

**Depends on:** G2-02.

**Files:** `src/ca/relations.py`, `queries.py`, `outcomes.py`, `serialization.py`; `tests/conformance/test_t31_t33.py` and solver-adapter contract tests.

**Implementation:**

- Define immutable model-set relation ASTs, exact periodic/open/window scopes, candidate presentations, local observations, verification reports, witnesses, and replayable certificates.
- Implement closed center-conditioned histogram relations and exact oriented `AllowedLocalPatterns`; normalize the former into the latter with a guarded partial inverse.
- Add structural conjunction and independent unanchored `RequiredPatternOccurrences(EACH_SOMEWHERE)` requirements.
- Keep pointwise equality, structural support/codec order, explicit symmetry transforms, witness gauge, and mathematical denotation distinct.
- Define `Satisfiable | Unsatisfiable | Unknown | ResourceLimit` query results with proof-strength rules. Solver adapters may return results only through scoped replayable evidence.
- Do not create FRONTIER/NEIGHBORHOOD/RULE/UPDATE placeholders.

**Tests/evidence:** T31 `0011`, 5x5 perturbation, gallery, finite obstruction and scope cases; all T32 exact-pattern/histogram commutations and north/east noninverse; T33 independent requirements, required-not-allowed empty denotation, remote-defect and conjunct witness cases; bounded failure never promotes to global UNSAT.

**Complete when:** all three mapped obligations are constructed and queried without rollout, callbacks, hidden solvers, implicit symmetry, or repair dynamics.

**Re-derive if:** a query result lacks replayable scope/certificate evidence, one witness is treated as the model set, or implementation starts inventing a transition schedule.

### G2-07 — Closed Functions, Constant Representations, and Differential Problems

**Depends on:** G2-05 and G2-06.

**Files:** `src/ca/expressions.py`, `values.py`, `relations.py`, `queries.py`, `outcomes.py`, `serialization.py`; optional work-program presets using G2-05; `tests/conformance/test_t40.py`, `test_t41.py`, `test_t45.py`.

**Implementation:**

- Add bound closed scalar/vector function syntax, exact parameters, definition sets, partiality, branch/continuation profiles, primitive versions, and point/zero/crossing/extremum queries.
- Add arity-zero exact-denotation definitions with positive-radix positional and simple-continued-fraction representation queries; separate query identity, evaluation context, coefficient payload, proof strength, termination, and provenance.
- Implement optional long-division, square-root, and residual coefficient algorithms as separately identified visible `t+0D` work SimplePrograms over G2-05, not as T40 state.
- Add bound multivariate fields, derivative multi-indices, equations, side-data claims, problem/solution concepts, candidates, residual/witness schemas, and scoped PDE query results.
- Treat discretizations, integrators, samples, diagnostics, and solver traces as explicit implementation relations. Only a separately justified IVP may derive a SimpleProgram.
- Select or explicitly defer an exact-real/interval backend. Unsupported exact operations return typed `Unsupported` without float fallback.

**Tests/evidence:** T41 exact identities/periods/zeros/poles/branches and source-defect guards; T40 positional/CF canonicalization, proof/termination taxonomy, random access, complete replay-verified handoffs, and forged-provenance rejection; T45 equation/problem/candidate/solution separation, scope/proof-strength, heat witness, numerical-relation and unsupported-concept cases.

**Complete when:** the three mapped obligations use one declarative query substrate, optional work uses the generic runner, and no evaluator/CAS object or numerical realization becomes semantic identity.

**Re-derive if:** direct query requires fabricated rollout, an approximate backend silently claims exactness, or a PDE solver step is confused with native continuous evolution.

### G2-08 — Multiplicity-Preserving Occurrence Bags

**Depends on:** G2-02.

**Files:** `src/ca/values.py`, `configurations.py`, `frontiers.py`, `neighborhoods.py`, `rules.py`, `updates.py`, `traces.py`; `tests/conformance/test_t27.py`.

**Implementation:**

- Add immutable prototype/pose products, exact/declared affine values, multiplicity-preserving occurrence bags, and permutation-invariant state equality.
- Add all-occurrence frontier, self prototype/full-pose reads, parent-local child templates, and closed extended-complex point-map sibling syntax.
- Add bag replacement UPDATE: consume all selected parents, compose `parent_pose o local_pose`, bag-union children, preserve parent/slot lineage, and defer newborns.
- Keep centers, footprints, unions, limits, dimensions, renderings, and parameter filters downstream.

**Tests/evidence:** exact page-189/page-190 centers/counts; composition order; equivariance; permutation; duplicate slots; same-center/same-footprint/different-frame descendants; overlap inertness; declared-precision boundaries; source/program provenance.

**Complete when:** T27 passes through the generic runner without keyed-set collapse, geometric callbacks, raster rules, or a geometric executor.

**Re-derive if:** state equality erases multiplicity/frame identity, geometry leaks from visualization, or child creation requires runner special cases.

### G2-09 — Ordered Generation, Structural Edit, Mosaic, Sieve Composition, and Scheduled Presets

**Depends on:** G2-04, G2-05, G2-07, and G2-08.

**Files:** `src/ca/configurations.py`, `loci.py`, `frontiers.py`, `neighborhoods.py`, `rules.py`, `updates.py`, `traces.py`, `expressions.py`, `queries.py`, `outcomes.py`, `serialization.py`; `tests/conformance/test_t13_t18.py`, `test_t20.py`, `test_t26_t28.py`, `test_t37_t39.py`, `test_t42.py`.

**Implementation:**

- Add finite ordered words and source occurrences/spans/old-end handles with snapshot identity and exact lineage.
- Add `AllOccurrences`, contextual neighbor eligibility, first-applicable match, required prefix, visible phase/head, prefix endpoint, and program-coupled selector composition.
- Add self/pair/span/prefix/complete-prefix/periodic-product reads with explicit alias multiplicity and access order.
- Add total nonempty/epsilon-capable word emission, literal structural patterns/templates, dependent `TermAt(AddressExpr)`, and typed failure witnesses as closed RULE data.
- Implement ordered generation and generic single/multi-span edit policies, including prefix-consume/tail-append, exact endpoint append, and ranked block mosaic assembly. Preserve newborn deferral, source/child order, zero-length witnesses, compatibility validation, and no-commit invalidity.
- Implement tree steps through a bijective balanced/prefix token representation and disjoint ordered spans; do not add a tree UPDATE.
- Implement finite rectangular rank-two substitution and contextual lower-right periodic reads; retain adaptive unequal subdivision as typed `Unsupported`.
- Implement the consecutive-divisor sieve with a visible stage marker, proper-multiple witnesses, finite Boolean field/ordered-survivor bijection, and intensional infinite presentation. Keep direct filters/streams/measurements as pure queries; implement Ulam's construction by visible complete-prefix search followed by the ordinary append substrate.
- Implement T42 as a finite phase-indexed T13 preset consuming only a complete replay-verified T40 result/handoff or separately tagged closed execution-order schedule. Live phases use T13/D019; exhausted phase retains the final word through the common terminal envelope without D019.
- Verify the restricted uniform-aligned T26/T27 representation and reject broader mixed-mosaic claims.

**Tests/evidence:** all strict T13-T18 histories, priorities, overlap/newborn, epsilon/extinction/terminal distinctions, Post/Wang widths, cyclic phase quotient, tree S/K/codec cases, T26 compatibility and T27 commutations, T28 context/mosaic/source-Blank rules, T37/T38 prefix/checkpoint/demand/failure cases, exact T39 rows retaining source `1`, composite-stage marker advancement, filter/query separation and Ulam composition, and the full frozen T42 source/asset/semantic oracle interfaces.

**Complete when:** every evolving member of the thirteen mapped obligations—including T39's consecutive sieve—uses the one runner and closed UPDATE policies; T39's direct filters, streams, and measurements remain pure query/observer objects over the shared declarative substrate; and no padding, regex/host pattern engine, deque callback, hidden cursor, tree/substitution/sieve executor, raster program, or online coefficient stream exists.

**Re-derive if:** a structural edit cannot preserve complete order/lineage, a snapshot handle can be forged or reused across states, a representation needs hidden source data, or an unsupported adaptive/sequential convention is being guessed.

### G2-10 — Rooted Port Graphs and Structural Commit

**Depends on:** G2-02.

**Files:** `src/ca/configurations.py`, `loci.py`, `frontiers.py`, `neighborhoods.py`, `rules.py`, `updates.py`, `traces.py`, `serialization.py`; `tests/conformance/test_t29.py`.

**Implementation:**

- Add finite nonempty root-reachable two-port graphs, alpha-renamable vertex occurrences, exact root/port-preserving equality, and canonical BFS codec.
- Add all-old-vertex selection; old-snapshot port-path and exact-length reach-signature reads; closed direct-old/fresh-node result data.
- Add graph UPDATE that allocates collision-free event-local fresh identities, commits all reroutes/births atomically, retains raw event evidence, defers newborns, and projects forward reachability from the preserved root.
- Keep layouts, dimensions, graph drawings, fixed-network label updates, constraints, causal graphs, and multiway graphs separate.
- Expose the source-underdetermined sequential profile only as typed `Unsupported` with the missing ordering/anchor/timing evidence named.

**Tests/evidence:** exact periods/collapse, singleton growth, depth-one `1296`, five depth-two count/table anchors, canonical isomorphism, path/signature snapshots, distinct fresh identities, alias/projection/frozen cases, raw-event replay, and unsupported sequential rejection.

**Complete when:** T29 passes through the same runner with one graph UPDATE policy and no network executor, callback, layout identity, or invented sequential schedule.

**Re-derive if:** canonical equality merges semantic vertices, fresh allocation depends on enumeration accidents, or projection/order cannot be replayed from visible data.

### G2-11 — Exact Finite Successor Sets and Multiway Conformance

**Depends on:** G2-09.

**Files:** `src/ca/outcomes.py`, `frontiers.py`, `rules.py`, `updates.py`, `traces.py`; `tests/conformance/test_t30.py`.

**Implementation:**

- Add every-overlapping-literal-match selection over one word and one branch replacement per match using the ordered edit substrate.
- Add exact finite successor-set merge that deduplicates equal child configurations across positions/rules/parents while retaining every derivation witness and dead-parent record.
- Add the explicit finite-powerset layer lift outside native one-word state; keep recurrence independent of compressed-graph visited state.
- Preserve epsilon word versus empty successor set, eventful identity, all-dead-to-empty-layer advancement, and empty-layer event-free quiescence.
- Keep weights, derivation multiplicity as semantic state, pruning, beam search, global visited suppression, confluence, and proof-search policy outside the base construction.

**Tests/evidence:** page-219/page-220 layers, page-206 extinction, cross-parent merge, folded graph relation, overlap/diamond/epsilon/identity/recurrence, witness reconstruction, ordering invariance, and no path sampling/pruning.

**Complete when:** T30 uses ordinary `StepResult[Word]` and the generic runner with no multiway executor or lossy chosen ancestry.

**Re-derive if:** exact child equality loses derivations, the native state must contain a global graph/visited set, or branch cardinality is truncated.

### G2-12 — Registry, In-Place Migration, Downstream APIs, and Final Conformance

**Depends on:** G2-03 through G2-11.

**Files:** `src/ca/__init__.py`, `specs.py`, `serialization.py`, `rollout.py`, `datasets.py`, `rng.py`, `viz/`, all tests, `README-V2.md`, `simple_programs.md`, `pyproject.toml`.

**Implementation:**

- Replace the current six-family `specs.py` resolution with versioned construction of closed axis descriptors and presets. Registry tags choose codecs/constructors only.
- Replace all family branches in `rollout.py` with generic `step`/run/batch traversal; delete the old paths in the same change.
- Atomically expose the generic runner and migrate current CA manifests, constructors, datasets, exports, and tests to `SimpleProgram`. Remove every fallback executor. A deprecated `Dynamics`-named constructor may remain only if it is a total lossless façade that immediately returns `SimpleProgram`, has no semantic methods or serialized identity of its own, and passes direct-construction equivalence tests.
- Make dataset planning select already constructed programs/seeds; RNG remains explicit seed/realization work and never hidden transition state.
- Generalize raw trace export without flattening semantic state into canonical `[t,x,y,z]`; coordinates and visualization remain type-specific views over raw structural traces.
- Publish the 45-row preset/conformance manifest and validate that every preset is ordinary structural axis data.
- Update the API document to the synthesis algebra, document declarative query APIs separately, and state every typed unsupported boundary.

**Tests/evidence:** all shared/unit/conformance/mutation/replay suites; all 45 Goal 1 oracle interfaces or ported fixtures; current canonical behavior; serialization compatibility only through the new versioned schema; runner AST no-family gate; no-callback/no-`Any` schema gate; all-catalog one-to-one join; optional deprecated-façade direct-construction equivalence and call-graph tests; docs examples; install/import/export/dataset/viz smoke tests.

**Complete when:** all 45 rows pass their unique conformance obligation, the old executor is gone, one runner advances every stepwise preset, declarative objects never enter rollout, and source inspection finds no semantic family branch or fallback path.

**Re-derive if:** migration requires two execution paths, registry tags leak into runtime behavior, downstream flattening becomes semantic state, or any catalog row can pass only by weakening its Goal 1 oracle.

## Exact 45-Row Coverage Matrix

The `Coverage stage` column assigns each catalog row exactly once. Leaf obligation `Cnn` is definitionally the conformance obligation for catalog row `Tnn`; there is no independent remapping. The normative 45-row leaf-dependency matrix above maps every row exactly once and gives direct proof dependencies, while the stage DAG supplies the shared-substrate dependencies. Shared implementation is planned above and is not duplicated here. The named Goal 1 file is the design authority for exact fixtures, variants, and negative tests; the linked canonical book corpus above is the source authority for text, figures, and rule material.

| ID | Exact catalog name | Coverage stage | Goal 1 authority | Required conformance focus |
|---|---|---|---|---|
| T01 | Elementary Cellular Automata | G2-03 | `2-T01-ELEMENTARY.md` | All 256 tables, physical bit order, snapshot trajectory, native/realization split |
| T02 | Multi-Color Nearest-Neighbor Cellular Automata | G2-03 | `21-T02-MULTICOLOR-CA.md` | Ordered finite alphabet, complete `k^3` table, arbitrary-precision codec |
| T03 | Totalistic Cellular Automata | G2-03 | `22-T03-TOTALISTIC-CA.md` | Exact valuation/sum quotient, compact/exhaustive denotation, histogram counterexample |
| T04 | Three-Color Totalistic Cellular Automata | G2-03 | `23-T04-THREECOLOR-TOTALISTIC.md` | Strict `k=3,r=1` T03 preset and repaired asset/trace fixtures |
| T05 | Higher-Color Totalistic Cellular Automata | G2-03 | `24-T05-HIGHERCOLOR-TOTALISTIC.md` | Strict `k>=4,r=1` presets, code 1004600, huge-table identity |
| T06 | Quiescent-Background-Preserving Cellular Automata | G2-03 | `25-T06-QUIESCENT.md` | Eligible-program restriction and evidence/claim identity; no execution change |
| T07 | Left-Right Symmetric Cellular Automata | G2-03 | `26-T07-SYMMETRIC.md` | Explicit action/property, invariant rule space, orbit representation separation |
| T08 | Initial-Condition Classes | G2-03 | `27-T08-INITIAL-CONDITIONS.md` | Complete event-zero configurations/laws/realizations over unchanged programs |
| T09 | Mobile Automata | G2-04 | `3-T09-MOBILE.md` | Composite active label, unique source, physical read, atomic write/move |
| T10 | Extended Mobile Automata | G2-04 | `28-T10-EXTENDED-MOBILE.md` | Three-label fixed-block result, movement, radius-two compiler adversary |
| T11 | Generalized Mobile Automata | G2-04 | `29-T11-GENERALIZED-MOBILE.md` | Finite activity proposals and exact translated-set union before commit |
| T12 | Turing Machines | G2-04 | `4-T12-TURING.md` | Tagged head/state/symbol, self read, destination preservation, outcomes |
| T13 | Neighbor-Independent Substitution Systems | G2-09 | `5-T13-PARALLEL-SUBSTITUTION.md` | All old occurrences, nonempty morphism, ordered concat, ragged lineage |
| T14 | Neighbor-Dependent Substitution Systems | G2-09 | `30-T14-CONTEXTUAL-SUBSTITUTION.md` | Right-neighbor eligibility/read and shared ordered generation |
| T15 | Creation-Destruction Substitution Systems | G2-09 | `31-T15-CREATION-DESTRUCTION.md` | Epsilon emissions, zero-length witnesses, extinction without new UPDATE |
| T16 | Sequential Substitution Systems | G2-09 | `6-T16-SEQUENTIAL-SUBSTITUTION.md` | Rule-major/leftmost match, one splice, no-match terminal |
| T17 | Tag Systems | G2-09 | `7-T17-TAG.md` | Separate read/delete widths, prefix consume/tail append, retained residue |
| T18 | Cyclic Tag Systems | G2-09 | `32-T18-CYCLIC-TAG.md` | Visible phase/head, old-end insertion, empty identity, quotient commutation |
| T19 | Register Machines | G2-04 | `8-T19-REGISTER.md` | Named bank/marker, instruction-owned reads, bigint branches and end outcomes |
| T20 | Symbolic Systems | G2-09 | `9-T20-SYMBOLIC.md` | Closed tree patterns/templates, prefix-free matches, token-span commutation |
| T21 | Two-Dimensional Cellular Automata | G2-03 | `33-T21-2D-CA.md` | Square topology, Self/cardinals, positional/count/sum schemas, frame permutation |
| T22 | Moore-Neighborhood Cellular Automata | G2-03 | `34-T22-MOORE-CA.md` | Self/eight offsets, alias multiplicity, orbit/count schemas, Life preset |
| T23 | Three-Dimensional Cellular Automata | G2-03 | `35-T23-3D-CA.md` | Cubic face/full shells, product/shell/positional schemas, frame maps |
| T24 | Higher-Dimensional Lattice Cellular Automata | G2-03 | `36-T24-HIGHERDIM-CA.md` | Generic dimension/fixed incidence/kinds/ports and closed dependent tables |
| T25 | Two-Dimensional Turing Machines | G2-04 | `37-T25-2D-TURING.md` | Sparse plane, self read, semantic ports/headings, Langton and hex cases |
| T26 | Two-Dimensional Substitution Systems | G2-09 | `38-T26-2D-SUBSTITUTION.md` | Ranked mosaic compatibility, no-commit invalidity, restricted bag commutation |
| T27 | Geometric Replacement And Fractal Systems | G2-08 | `10-T27-GEOMETRIC.md` | Posed occurrence bags, multiplicity, affine composition, lineage |
| T28 | Neighbor-Dependent Two-Dimensional Substitution Systems | G2-09 | `39-T28-CONTEXTUAL-2D-SUBSTITUTION.md` | Periodic lower-right context, ordered patterns, mosaic commit, adaptive unsupported |
| T29 | Network Systems | G2-10 | `11-T29-NETWORK.md` | Rooted two-port graphs, path/reach reads, fresh identities, projection |
| T30 | Multiway Systems | G2-11 | `12-T30-MULTIWAY.md` | Every match, exact successor merge, derivation witnesses, layer lift |
| T31 | Local Constraint Systems | G2-06 | `13-T31-CONSTRAINTS.md` | Static model relation, scoped verification, witnesses/certificates/solver results |
| T32 | Template Constraint Systems | G2-06 | `40-T32-TEMPLATE-CONSTRAINTS.md` | Oriented allowed patterns, T31 normalization, explicit transforms/scopes |
| T33 | Seeded Template Constraint Systems | G2-06 | `41-T33-SEEDED-CONSTRAINTS.md` | Independent unanchored occurrence conjuncts and proof-strength boundaries |
| T34 | Arithmetic Iteration Systems | G2-05 | `14-T34-ARITHMETIC.md` | Exact scalar add/multiply events, bigints/rationals, representation separation |
| T35 | Piecewise Integer Maps | G2-05 | `42-T35-PIECEWISE-INTEGER.md` | Complete residue and ordered-fraction rules, missing-branch no-commit |
| T36 | Digit-Reversal Arithmetic Systems | G2-05 | `43-T36-DIGIT-REVERSAL.md` | Closed positional rule, canonical commutation, fixed/grow width distinction |
| T37 | Recursive Sequences | G2-09 | `15-T37-RECURSIVE.md` | Complete prefix, unique endpoint, fixed-lag read, exact append/replay |
| T38 | Variable-Index Recursive Sequences | G2-09 | `44-T38-VARIABLE-RECURRENCE.md` | Dependent term-address AST, ordered demands/failures, unchanged append |
| T39 | Number-Theoretic Filtering Systems | G2-09 | `16-T39-FILTERS.md` | Consecutive sieve events/marker plus pure filter/measurement separation |
| T40 | Mathematical-Constant Digit Systems | G2-07 | `45-T40-CONSTANT-DIGITS.md` | Pure representations, proof/termination taxonomy, work programs, T42 handoffs |
| T41 | Function-Combination Systems | G2-07 | `17-T41-FUNCTIONS.md` | Closed definitions/domains/branches and scoped exact/certified queries |
| T42 | Continued-Fraction-Driven Substitution Systems | G2-09 | `46-T42-CF-SUBSTITUTION.md` | Replay-verified finite schedule, phased T13 lowering, exact exhaustion |
| T43 | Iterated Maps | G2-05 | `18-T43-ITERATED-MAPS.md` | Exact/represented scalar feedback, closed maps, event and analyzer separation |
| T44 | Continuous Cellular Automata | G2-05 | `19-T44-CONTINUOUS-CA.md` | Continuous value carrier, affine aggregate/map, old-snapshot field update |
| T45 | Partial Differential Equation Systems | G2-07 | `20-T45-PDE.md` | Differential problem/solution/query/certificate and numerical-relation boundary |

## Cross-Stage No-Cheating Verification

| Risk | Required automated gate |
|---|---|
| Family execution branch | Parse/inspect `step`, repeated run, and batch orchestration; reject catalog IDs, family tags, and executor registries |
| Opaque callback/interpreter | Reject unrestricted callable/formula/eval/CAS/generator fields in all public semantic dataclasses and serialized schemas |
| Whole-state packing | Require structural configuration schemas, invariant inspection, canonical equality, and representation inverse-on-image tests |
| Hidden control/schedule/RNG | Replay next step from serialized program+configuration; reject missing phase/head/marker/draw authority |
| Lossy claimed reuse | Full `StepResult` commuting tests cover successors, outcomes, events, witnesses, identity, and lineage |
| Fixed-capacity disguise | Adversarial growth/movement beyond fixture dimensions; native/finite-realization identities remain distinct |
| Raster-derived semantics | Mutation tests prove rule/program fixtures come only from authorized text/transcription records, never image pixels |
| Float fallback | Exact requests either return exact/certified results or typed unsupported/error; no silent machine arithmetic |
| ID/digest authority | Mutate payload under retained ID and ID under retained payload; both fail/rederive structurally |
| Solver as semantics | Query result requires scope and replayable witness/certificate; work trace and mathematical object IDs differ |
| Duplicate catalog work | Mechanical CSV/manifest/table join proves 45 unique IDs and exact names, each with one coverage stage |
| Second semantic/execution compatibility fork | Source scan and call-graph tests prove the old family rollout and fallback conversions are removed; any deprecated constructor returns the ordinary structural program before execution |

## Migration Map

| Current Phase 1 responsibility | Goal 2 disposition |
|---|---|
| `Dynamics(domain, shape, rule, neighborhoods, frontier, boundary)` | Replace the semantic contract with `SimpleProgram`, whose DOMAIN, configuration schema/realization, axes, and invariants are typed separately; an optional deprecated name may only be a direct construction façade |
| Fixed `Alphabet` helpers | Retain as finite-alphabet constructors; add ordered/product/tagged schemas and exact value separation |
| Tensor `Frontier` | Generalize to firing-source selection; fixed next-slice behavior becomes one preset |
| Offset-only `Neighborhood` | Retain offset access and add closed named/span/path/product patterns |
| `Rule.family` and family instantiation | Replace with closed structural RULE descriptors and construction-time codecs |
| Family-branched `_rollout_*` | Delete; all execution goes through generic `step` and repeated traversal |
| `RawEpisode`/`RawBatch` tensor identity | Replace with structural raw trace/batch records; tensor projection is a fixed-field view |
| `dynamics_from_spec` family switches | Replace with versioned structural `program_from_spec`; registry builds axes but never executes them |
| Current seed renderers | Retain valid constructors as T08-style event-zero responsibilities; remove callback escape and hidden histories |
| Canonical `[t,x,y,z]` coordinates | Keep as a downstream fixed-dimensional view, never universal topology or state identity |
| Dataset family recipes | Migrate to references to validated programs/seeds/realizations; no semantic family dispatch |

## Explicitly Deferred Boundaries

- Probability-bearing or stochastic transition semantics beyond event-zero T08 laws.
- First-class native continuous-time flow/semigroup and continuous-time trace semantics; a PDE relation or numerical integrator does not supply them by itself.
- T28 adaptive unequal subdivision without complete carrier/incidence/update evidence.
- T29 sequential network schedule without decisive primary-source order/anchor/timing evidence.
- Weak/distributional PDE solution concepts beyond the evidenced Classical v1 scope.
- Exact transcendental execution profiles until a backend can meet the required proof/round-trip contract.
- Any catalog-adjacent construction not among the 45 rows unless a later evidence stage extends the ledger.

Each deferred request must return a stable typed unsupported result naming the missing capability/evidence. None authorizes a callback or fallback path.

## Goal 2 Completion Gate

Goal 2 is complete only when:

- [ ] G2-00 through G2-12 satisfy their dependencies, tests, completion evidence, and re-derivation checks.
- [ ] The machine-readable catalog manifest joins the 45 CSV rows, this table, and 45 conformance suites exactly once.
- [ ] Every stepwise type advances through the same inspected `step` implementation.
- [ ] Every declarative type is constructible/queryable without fake rollout.
- [ ] All Goal 1 semantic/source/asset oracle interfaces or faithfully ported fixtures pass.
- [ ] The old family executor, second semantic/execution compatibility path, opaque callback fields, and silent conversions are absent; any deprecated construction façade is lossless and executor-free.
- [ ] Serialization is structural, versioned, fail-closed, and replay-complete.
- [ ] Documentation, datasets, and visualization consume semantic results without redefining them.
- [ ] Repository-wide tests, type/schema checks, mutation tests, Markdown/code examples, and `git diff --check` pass.

## Handoff Result

COMPLETE as a Goal 1 handoff. G2-00 through G2-12 form an acyclic dependency plan; every stage names target files, implementation work, tests/evidence, completion criteria, and re-derivation triggers. The coverage matrix matches all 45 CSV IDs and names exactly once, every Goal 1 authority exists, and the normative `Cnn = Tnn` matrix records every leaf and its direct dependencies without cycles.

The plan migrates `src/ca` in place, implements shared substrates once, keeps the generic runner private until a single atomic public cutover, and removes the family executor. An optional deprecated constructor is allowed only as a total lossless façade returning the ordinary `SimpleProgram`; it owns neither semantics nor execution. Hostile review, DAG/detail consistency, table/fence checks, scope checks, `git diff --check`, the frozen T42 oracles, and all 141 current repository tests pass. The unchecked Goal 2 completion gate above intentionally remains future implementation work.
