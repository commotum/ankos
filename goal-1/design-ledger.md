# Goal 1 Design Ledger

This is the evolving architecture record for Goal 1. It inventories observed semantics, current implementation mechanisms, evidence-backed decisions, hypotheses, rejected shortcuts, and integration consequences. It does not prescribe a universal executor in advance.

## Decision Rules

1. Principle 0 governs every entry: a prior plan or abstraction is revisable when construction evidence does not compose naturally.
2. Book evidence precedes semantic reuse or extension. Catalog names and `CA-Types.md` sections provide search vocabulary, not construction proof.
3. A mechanism is shared only when state, reads, rule result, commit, and successor semantics are genuinely the same.
4. State must expose support/topology, values, and control needed to advance; executor-local control or opaque whole-state packing is not accepted.
5. Program state, trace, ANKoS encoding, batching, visualization, solvers, and numerical approximations stay distinct unless evidence proves coupling is defining.
6. A new primitive remains `PROVISIONAL` until a completed type stage supplies direct evidence, invariants, and at least one conformance case.

## Fit Labels

- `DIRECT`: an existing semantic component expresses the construction without reinterpretation.
- `PARAMETERIZATION`: semantics already match; only data, validation, or a named preset is required.
- `PRINCIPLED EXTENSION`: evidence requires a new semantic capability.
- `SEMANTIC MISMATCH`: the mechanism expresses a different construction or depends on prohibited packing, inversion, fallback, or hidden behavior.
- `NOT APPLICABLE`: the component is genuinely absent.
- `UNRESOLVED`: evidence is insufficient or contradictory.

## Construction Record Schema

Every completed type will update the relevant rows below and record:

- state = support/topology + values + control;
- active loci or frontier;
- reads/access pattern and rule inputs;
- explicit result type;
- update/commit semantics;
- successor structure, branching, deduplication, and halting;
- boundary and initial conditions;
- parameters and variants;
- observables distinct from program state;
- current API/runtime fit, evidence provenance, and Goal 2 dependencies.

## Current Documented API Baseline

These are current facts from `simple_programs.md`, not accepted final architecture.

| Concern | Current documented mechanism | Proven scope | Pressure to test |
|---|---|---|---|
| Address/domain | Dense canonical `[t,x,y,z]` coordinates; `t+0D` through `t+3D` (`simple_programs.md:1-24`, `simple_programs.md:115-167`) | Fixed finite rank-0..3 fields | Dynamic support, trees, graphs, arbitrary dimension, continuous domains |
| State | Persistent trajectory field `X:D->A` with current snapshot (`simple_programs.md:87-113`) | Dense value field | Explicit topology and control; Markov state versus stored trace |
| Seed | Selected support plus fill value/distribution (`simple_programs.md:235-290`) | Initial dense slice | History, structural seeds, global requirements, exact sources |
| Boundary | Fixed, periodic, reflective spatial reads (`simple_programs.md:292-358`) | Rectangular spatial intervals | Sparse/unbounded support and non-lattice boundaries |
| Reads | Ordered relative-offset selectors with compact or masked reads (`simple_programs.md:360-731`) | Finite coordinate stencils | Path/tree reads, data-dependent addresses, nonlocal access |
| Active loci | Absolute next-state frontier selectors (`simple_programs.md:1412-1765`) | Writable sites in a preallocated next slice | Source events, structural matches, queue heads, branch sets |
| Rule | Exhaustive, isotropic, semi-totalistic, totalistic, formulaic, stochastic value return (`simple_programs.md:1767-2122`) | Per-target value choice | Typed effects, rewrites, constraints, derivatives, distributions |
| Commit | Parallel same-site write; non-frontier values copy forward (`simple_programs.md:1767-1793`, `simple_programs.md:2156-2199`) | Synchronous fixed-support transitions | Movement, splice, insert/delete, rewire, ordered replacement, multiway successors |
| Representation | Generator semantics use the canonical address directly | Rank-0..3 dense trajectories | Principle 6 requires changing the experiment schema rather than distorting state |

## Current Runtime Baseline

These mechanisms are implementation evidence to preserve only when later stages show semantic fidelity.

| Module | Current responsibility and limits | Design status |
|---|---|---|
| `src/ca/alphabets.py` | Finite integer, evenly spaced float, Boolean, and explicit symbolic value spaces; explicitly excludes topology, role, and rule semantics (`:1-31`, `:44-173`) | Useful responsibility boundary; type coverage unproved |
| `src/ca/loci.py` | Canonical rank-0..3 coordinate spaces, finite absolute/relative universes, selectors, mask algebra, ordering, boundary gather (`:1-61`, `:62-319`, `:321-636`) | Candidate finite-lattice selector machinery only |
| `src/ca/neighborhoods.py` | Composes relative selector components; includes spatial stencils and negative-time history families (`:1-59`, `:110-549`, `:551-766`) | Component preservation is useful; temporal reads conflict with the documented current-state convention and require stage evidence |
| `src/ca/frontiers.py` | Structured frontier wrapper, but executable catalog exposes only full `time_slice` (`:1-80`) | Insufficient for claimed generality; no extension chosen |
| `src/ca/rules.py` | Rule channels, aggregate/gate pipelines, lookup and callable formula rules, plus named experiment families (`:1-79`, `:81-334`, `:336-515`) | Typed read summaries are candidate reuse; callable and family semantics require audit |
| `src/ca/seeds.py` | Selector-backed support and rendering plus pair/history, random, geometric, periodic, and structured catalogs (`:1-57`, `:136-878`, `:879-1056`) | Seed/render separation is candidate reuse; `fractal`/`spiral` predicate callbacks are not accepted extension mechanisms |
| `src/ca/specs.py` | `Dynamics`, raw result records, JSON-safe resolution of six named Phase 1 families, one frontier, and four boundary policies (`:24-82`, `:84-253`) | Current handoff contract; family resolver is not evidence of a family index design |
| `src/ca/rollout.py` | Public raw episode/batch boundary, rank validation, canonical coordinates, then explicit rule-family branches (`:40-290`, `:292-831`) | Current behavior only; branch dispatch and hidden history contradict Goal 1 constraints |
| `src/ca/rng.py` | Deterministic seed derivation and NumPy generator construction (`:1-79`) | Incidental algorithm kept separate; stochastic construction semantics still unproved |
| `src/ca/datasets.py` | Four PE-compatible dataset recipes; plans streams, seeds, rule pools, OOD variants, transforms, and invokes raw rollout (`:1-345`, `:346-842`) | Downstream dataset concern; must not determine program semantics |
| `src/ca/__init__.py` | Exports current runtime surface (`:1-93`) | Inventory only; not a Goal 2 API commitment |

## Current Tests as Evidence

The current tests establish behavior of the current implementation, not universal construction coverage.

- Loci tests cover centered coordinates, selectors, gathering, time-axis access, and boundary policy validation.
- Neighborhood tests cover literal/history components, ECA/Moore/Von Neumann geometry, directional lines/FOVs, and invalid inputs.
- Rule tests cover finite declared rule counts, including Lagcounts metadata.
- Rollout tests cover AR2, Dyadlags, Lagcounts, Dyadrads/Dyadaxes, batch parity, optional coordinates, and validation. They exercise separate family branches rather than proving one executor.
- Seed tests cover pair/uniform-bit/constant/point/Bernoulli and limited compound/structured behavior.
- Spec tests cover only the six supported named Phase 1 families and reject the legacy frontier name.
- Dataset tests cover the four current dataset recipes, planning, deterministic streams, batching, and OOD metadata.
- Visualization export tests exercise the downstream raw-result boundary, storage typing, coordinate export, and palette validation.

## Semantic Dimension Inventory

No row below is a committed universal primitive at Foundation. Type stages must replace `UNRESOLVED` with evidence-backed structure or an explicit algebra split.

| Dimension | Current candidate | Status | Evidence users |
|---|---|---|---|
| Support/topology | Dense finite canonical lattice | UNRESOLVED beyond current CA runtime | None completed |
| Values/alphabet | Finite explicit value space | UNRESOLVED across all catalog types | None completed |
| Control | Part of visible state | Principle-level requirement; representation UNRESOLVED | None completed |
| Active loci | Selector-produced finite set | UNRESOLVED | None completed |
| Reads/access | Ordered grouped reads | UNRESOLVED | None completed |
| Rule choice | Explicit finite lookup or structured calculation | UNRESOLVED | None completed |
| Rule result | Typed semantic result, not assumed value assignment | Principle-level requirement; algebra UNRESOLVED | None completed |
| Commit/update | Explicit total application of applicable results | UNRESOLVED | None completed |
| Successors | One next state, multiple outcomes, solution set, derivative, or observation | UNRESOLVED; do not collapse categories | None completed |
| Halting/invalidity | Visible semantic outcome or transition condition | UNRESOLVED | None completed |
| Trace encoding | Lossless mapping separate from program semantics | Principle-level requirement; schema UNRESOLVED | None completed |
| Solver/numerics | Separate from declarative system unless defining | Principle-level requirement; concrete boundaries UNRESOLVED | None completed |

## Decision Log

### D000 — No construction algebra selected at Foundation

- Status: ACTIVE.
- Basis: `principles.md:3-28` and the absence of completed type evidence.
- Consequence: `FRONTIER -> NEIGHBORHOOD -> RULE -> UPDATE` remains a candidate for transition/rewrite systems, not a universal conclusion.

### D001 — Preserve semantic categories in analysis

- Status: ACTIVE.
- Basis: `principles.md:41-57`, `principles.md:89-103`.
- Consequence: effects, constraints, derivatives, distributions, observations, solvers, and numerical approximations receive distinct fit analysis until evidence demonstrates a shared algebra.

### D002 — Treat current family branches and hidden temporal state as liabilities, not compatibility requirements

- Status: ACTIVE.
- Basis: `src/ca/rollout.py:145-213`, `src/ca/rollout.py:334-574`; Goal 1 prohibits family-specific rollouts and hidden executor state.
- Consequence: Goal 2 planning must preserve evidenced behavior through honest state/result semantics, not retain dispatch structure.

### D003 — Use stable type IDs independent of adversarial execution order

- Status: ACTIVE.
- Basis: exact 45-row CSV/taxonomy join and `0-plan.md` stage ordering.
- Consequence: shared implementation may be planned once, but T01 through T45 each retain separate evidence and conformance obligations.

## Rejected Shortcuts

These are globally rejected unless Principle 0 re-derivation replaces the goal itself:

- family-name rollout dispatch as the proposed universal runtime;
- opaque packing of a machine, graph, tree, history, or whole state into a nominal cell value;
- fixed-capacity padding presented as dynamic-support semantics;
- unrestricted formula or predicate callbacks that contain the entire construction;
- hidden head state, program counters, cyclic counters, history, RNG state, or solver state;
- compiling another construction to a CA merely to claim native coverage;
- treating canonical `[t,x,y,z]` encoding or visualization coordinates as topology;
- conflating a constraint with a solver, a PDE with a discretization/integrator, or a stochastic law with an RNG implementation;
- weakening tests, adding flags/shims/fallbacks, or duplicating shared primitives under family-specific names.

## Integration Log

- `1-FOUNDATION` — COMPLETE: established the catalog join, source/runtime/test baseline, fit labels, unresolved semantic dimensions, and global rejection criteria. No type evidence or construction primitive was declared complete.

## Open Architecture Questions

1. Which catalog rows are constructions versus restrictions, presets, seed classes, observables, or solver-defined systems?
2. Where does the candidate transition/rewrite algebra cease to be substantive?
3. Which state models require dynamic support, explicit topology, structural identity, or visible control?
4. Which result and commit algebras are genuinely shared across assignment, movement, replacement, structural mutation, and multiway branching?
5. What trace encoding preserves types whose semantic address is not a rank-0..3 lattice coordinate?
6. Which current selector, alphabet, rule-summary, seed, RNG, and raw-result components survive evidence without semantic reinterpretation?
7. Which current tests are canonical-construction evidence and which merely preserve incidental Phase 1 behavior?
