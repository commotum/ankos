# Goal 1 Design Ledger

This is the evolving architecture record for Goal 1. It inventories observed semantics, current implementation mechanisms, evidence-backed decisions, hypotheses, rejected shortcuts, and integration consequences. The completed architecture audit now establishes one branch-free runner for step/rewrite systems; declarative categories without canonical evolution remain outside rollout.

## Decision Rules

1. Principle 0 governs every entry: a prior plan or abstraction is revisable when construction evidence does not compose naturally.
2. Book evidence precedes semantic reuse or extension. Catalog names and `CA-Types.md` sections provide search vocabulary, not construction proof.
3. A mechanism is shared only when state, reads, rule result, commit, and successor semantics are genuinely the same.
4. Configuration must expose its DOMAIN/support/topology, ALPHABET/value labels, structural invariants, and every control role needed to advance. Control may be a lossless tagged/product/marker role inside those labels or structures; executor-local control and opaque whole-state packing remain invalid.
5. Program state, trace, ANKoS encoding, batching, visualization, solvers, and numerical approximations stay distinct unless evidence proves coupling is defining.
6. A new primitive remains `PROVISIONAL` until a completed type stage supplies direct evidence, invariants, and at least one conformance case.

## Fit Labels

- `DIRECT`: an existing semantic component expresses the construction without reinterpretation.
- `PARAMETERIZATION`: semantics already match; only data, validation, or a named preset is required.
- `PRINCIPLED EXTENSION`: evidence requires a new semantic capability.
- `SEMANTIC MISMATCH`: the mechanism expresses a different construction or depends on prohibited packing, inversion, fallback, or hidden behavior.
- `NOT APPLICABLE`: the component is genuinely absent.
- `UNRESOLVED`: evidence is insufficient or contradictory.

## Architecture Audit Authority

`architecture-audit.md` is the authoritative first-principles disposition of D000-D118 and every completed type-stage handoff. It establishes the branch-free SimpleProgram protocol:

```text
active = FRONTIER.select(configuration)
reads  = NEIGHBORHOOD.read(configuration, active)
writes = RULE(active, reads)
next   = UPDATE.apply(configuration, active, writes)
```

DOMAIN/support/topology, ALPHABET/value schema, FRONTIER, NEIGHBORHOOD, RULE result, UPDATE composition/schedule, seed, and invariants are typed axes of that protocol. Cellular automata are one fixed-lattice/all-sites/local-stencil/scalar-write/parallel-update preset. Catalog types and axis implementations never select a family executor.

The audit retires required top-level `SingleControl`, `TransitionControl`, `ArithmeticAssignment`, `MapAssignment`, and construction-named executor/state classes. Visible heads, active markers, counters, and cursors remain semantic roles, represented losslessly by tags, products, markers, or structural fields. Constraint/model sets, uniterated functions, and general PDE relations without a specified evolution problem remain declarative nonfits; multiway rewriting stays inside the runner through set-valued successors.

The decision text and construction rows below retain their evidence bases and historical derivations. Wherever historical wording conflicts with the complete matrix in `architecture-audit.md`, that matrix and its stage-disposition table permanently supersede it.

## Construction Record Schema

Every completed type will update the relevant rows below and record:

- configuration = DOMAIN/support/topology + ALPHABET/value labels + structural invariants, with control as an explicit role rather than a mandated storage class;
- active loci or frontier;
- reads/access pattern and rule inputs;
- explicit result type;
- update/commit semantics;
- successor structure, branching, deduplication, and halting;
- boundary and initial conditions;
- parameters and variants;
- observables distinct from program state;
- current API/runtime fit, evidence provenance, and Goal 2 dependencies.

## Historical Evidence-Closed Construction Records (Superseded Architecture)

These rows preserve the pre-audit derivation and evidence inventory. The current construction classification and Goal 2 obligation for every row are the authoritative stage-disposition entries in `architecture-audit.md`; names such as `SingleControl`, ordinal update laws, and family-shaped state classes below are not current requirements.

| Type | State | Active/read/rule | Result/update | Successor and boundaries | Goal 2 obligation |
|---|---|---|---|---|---|
| T01 Elementary CA | Fixed ordered 1D lattice + total Boolean field; no control | `AllSites`; ordered old `(left,self,right)`; arbitrary 8-entry table with `index=4l+2c+r` | Typed same-site `Assign`; atomic parallel commit | One deterministic successor, no halt; native `Z` or explicit finite cycle/segment/causal-window realization; seed independent | Generic ordered lookup + parallel assignment + support/realization/trace split; all 256 rules and asymmetric trajectory oracle; no ECA branch |
| T02 Multi-Color Nearest-Neighbor CA | Fixed ordered 1D lattice + total field over an explicitly ordered finite alphabet `A`, strict `k=card(A)>=3`; no control | `AllSites`; ordered old `(left,self,right)`; arbitrary complete `k^3`-entry table with `index=k^2l+kc+r` | Typed same-site `Assign`; T01 atomic parallel commit, so no new update law | One deterministic successor, no halt; native `Z` or explicit finite cycle/segment/causal-window realization; initial field/background independent and evolving | Parameterize the generic T01 executor by alphabet/table; structural table + Wolfram positional arbitrary-precision base-`k` codec; exact count/source-code/trajectory oracles; no T02 branch, binary packing, or implicit row default |
| T03 Totalistic Cellular Automata | Fixed ordered 1D lattice + total field over a finite alphabet with explicit numeric valuation `nu:A->{0,...,k-1}`; no control | `AllSites`; fixed old radius-`r` stencil of arity `q=2r+1`; exact sum `s=sum nu(read)`; complete `M=1+(k-1)q`-entry table | Typed same-site `Assign`; T01 atomic parallel commit, so no new update law | One deterministic successor, no halt; native `Z` or explicit finite cycle/segment/causal-window realization; seed/background independent and evolving | Closed equal-weight sum + typed structural sum table + arbitrary-precision least-significant-sum base-`k` codec; T04/T05 presets and T06/T07 predicates; no T03 branch, histogram substitute, float mean, or exhaustive-table masquerade |
| T09 Mobile Automata | Fixed ordered 1D lattice + total Boolean field + exactly one visible unit-payload active position | `ControlLocus("active")`; ordered old `(left,self,right)`; arbitrary 8-entry finite table returning color/displacement | `Assign(source,value)` + `TransitionControl(active,source±1,Unit)`; atomic compound commit | One deterministic successor, no halt/stay/split; native line or explicit relocation-aware realization; initial values/control independent | Source-frontier semantics, structured state/control, finite typed result codec, compound effects/update, control-preserving trace; all 65,536 code pairs; no mobile branch/CA packing |
| T12 Turing Machines | Fixed ordered integer tape + total default/override symbol field + one head `(position,state)` | `ControlLocus("head")`; control payload + self-only tape symbol; complete `Q×Sigma` table | `Assign(old_head,symbol)` + `TransitionControl(head,old±1,next_state)`; atomic | Base has one successor and never halts; terminal-control variant has zero successors after final state; external stops distinct; no native finite edge | Payload control, total tape, product-key/result table, termination/stop reasons, structured trace; `(2sk)^(sk)`/known-code/trajectory oracles; no head packing/Turing branch |
| T13 Neighbor-Independent Substitution | Explicit discrete ordered symbol sequence; canonical finite support plus explicit countably infinite support/cut realization | `AllOccurrences` over old snapshot; self symbol only; total alphabet-closed `h:Sigma->Sigma+` | `ReplaceOccurrence(source,word)` + atomic `ParallelReplaceConcat`; parents consumed, children ordered by source then word position | One deterministic non-halting successor; empty input is a fixed successor; no endpoint boundary for self-only read | Ordered support/occurrence sources, structured nonempty-word tables, sibling structural update algebra, ragged/lineage trace and infinite realization; exact morphism/growth/order oracles; no padding/callback/compiler/branch |
| T16 Sequential Substitution | Finite discrete ordered word; no cursor/control | Program-coupled `FirstApplicableMatch`; ordered literal `Sigma+->Sigma+` clauses; rule-major then leftmost interval | `ReplaceInterval(match,word)` + atomic `SingleSpliceUpdate`; prefix/suffix persist, match consumed, output created | One deterministic successor for a match; zero successors with retained final state for `NoMatch`; no endpoint wrap/boundary | Ordered rewrite IR, matched-span sources/reads, single-splice sibling update, typed no-match outcome, ragged event/lineage trace; exact priority/overlap/no-op oracles; no callback/regex/family branch |
| T17 Tag Systems | Finite discrete ordered word with semantic front/back; no cursor/control | Program-coupled `RequiredQueuePrefix`; exact leading `q` read; total `Sigma^q->Sigma*` table; Wolfram pins `q=d` | `ConsumePrefixAppend(read_span,consume_span,word)` + atomic `QueueSpliceUpdate`; consumed front removed, old suffix persists, output created at tail | One deterministic successor when `len>=max(q,d)`; zero with retained residue for `InsufficientPrefix`; explicit Notes short-to-empty projection; no spatial boundary | Prefix-queue program/source/read/result/update, epsilon-capable private word/edit carrier, terminal/reference split, ragged event/lineage trace; case(a)/case(c)/Post/Wang/count oracles; no deque/callback/fallback/compiler/branch |
| T19 Register Machines | Finite named register bank over arbitrary-precision naturals + visible unit-payload program counter into immutable code | Program-coupled `ActiveInstruction`; exact tagged instruction plus instruction-owned named operand reads; closed increment/decrement-jump algebra | `IncrementResult`, `DecrementJumpTaken`, or `ZeroFallthrough` return `Assign(RegisterSlot, Natural)` + `TransitionControl`; shared atomic effects commit | One `Advanced` successor per valid instruction; past-end reference `Quiescent` stutters without events; explicit `ProgramExit` interpretation has zero successors; no wrap/spatial boundary | Infinite `Naturals`, finite bank, program-address control/source/read, closed results, quiescent outcome, structured event trace/count profiles; exact trajectory/halt/sqrt/big-int oracles; no packing/callback/family branch |
| T20 Symbolic Systems | Finite rooted ordered expression tree over declared atoms; expression-valued head plus ordered arguments; no control | Program-coupled `OutermostNonOverlappingPatternMatches`; structural patterns bind whole subtrees; functional preorder and ordered rule priority | `ReplaceSubtree(match,bindings,tree)` + atomic `ParallelPrefixFreeTreeReplace`; context persists, selected subtrees consumed, bindings copied/deleted with lineage | One `Advanced` successor for any nonempty match set; no-match reference `Quiescent` stutters event-free; optional fixed-point stop; no spatial boundary | Native trees/paths, closed pattern/template program, bindings, fifth update law, ragged structural trace; exact trajectory/overlap/newborn/fixed/count/S-K oracles; no host evaluator/string packing/family branch |
| T27 Geometric Replacement And Fractal Systems | Finite multiplicity-preserving bag of immutable prototype occurrences with complete exact or declared local-to-world affine poses; no control; distinct extended-complex point-bag profile | `AllGeometricOccurrences`; each old occurrence reads only its prototype/full pose; total prototype row of parent-local child templates or closed point-map AST | `ReplaceGeometricOccurrence` composes `parent_pose∘local_pose`; atomic `ParallelOccurrenceBagReplace` consumes all parents and bag-unions all children with parent/slot lineage | One deterministic `Advanced` successor for every nonempty total program, including an identity event; no intrinsic halt or ambient edge; overlap/coincidence is inert and multiplicity persists; horizon/limit/rendering are external | Exact rational/algebraic and declared-precision affine values, prototypes/poses, permutation-invariant bags, sixth update law, closed point-map profile, ragged geometry trace; exact center/count/overlap/frame/composition/equivariance/provenance oracles; no raster/center/callback/family branch |
| T29 Network Systems | Finite nonempty root-reachable directed graph with exactly two semantic outgoing ports per vertex; alpha-renamable vertex tokens; no control in the parallel profile | `AllNetworkNodes`; old-snapshot port-word endpoints and exact-length reach-count signatures; total closed topology-key table | Two typed `DirectOld`/`InsertFresh` port expressions per old vertex; atomic `ParallelRerouteCreateProject` retains old nodes, allocates distinct fresh nodes, builds raw edges, then directed-projects from the root | One deterministic `Advanced` successor including isomorphic identity events; root prevents empty state; no intrinsic halt/cap/boundary; fixed/cycle/count/horizon observers external | Rooted-port graph values, path/signature reads, exact BFS isomorphism codec, seventh update law, raw/projection provenance, exact page-rule tables/periods/counts; sequential variant unavailable until source order is resolved; no layout/padding/callback/family branch |
| T30 Multiway Systems | Finite exact set of finite alphabet-closed words, including epsilon; no control, branch weights, or derivation occurrences in semantic state | Program-coupled `AllApplicableLiteralMatches` finds every overlapping occurrence of every unordered literal clause in every old parent; exact matched-span read | One `BranchIntervalReplacement` per match; atomic `DistinctBranchMerge` exact-unions children across spans/rules/parents and records dead parents plus witnesses | One deterministic set-valued `Advanced` successor for every nonempty layer, including all-dead to empty and identity events; empty layer is event-free `Quiescent` reference stutter; recurrence is not globally suppressed | T13 words/T16 literal edit reuse, finite word-set carrier, every-match source, eighth update law, layered/witness/compressed graph traces; exact page/merge/epsilon/diamond oracles; no path sampling/visited/pruning/callback/family branch |
| T31 Local Constraint Systems | Mathematical model set of total fields `X:Z^d->Sigma` satisfying a translation-invariant center-conditioned neighbor-histogram relation; no time/control/seed/materialized all-model state | No transition source/read/rule; pure local verifier over closed periodic/open representations; optional external scoped solver queries | No result/update law; exact violations, periodic witnesses, finite-obstruction certificates, and `Satisfiable/Unsatisfiable/Unknown/ResourceLimit` query records are separate categories | Solution set may be empty/one/many/infinite; periodic witness proves global SAT, replayed finite obstruction global UNSAT, bounded failure Unknown; pointwise models distinct and no halting notion | Separate constraint/verifier/query/solver modules, exact footprint/histogram data, periodic presentations/scopes, 1D de Bruijn analyzer, page-225/226/227 oracles; no dynamics/callback/fake grid/T32-T33 flag |
| T34 Arithmetic Iteration Systems | One domain-tagged arbitrary-precision exact integer or reduced rational scalar; no spatial support/control; program and seed separate | `UniqueScalar`; complete current-value read; closed structural `AddConstant(c)` or `MultiplyConstant(c)` | `ArithmeticAssignment` returns typed `Assign(ScalarSlot,next)`; existing atomic effects commit, so no ninth update law | One deterministic `Advanced` successor per valid event, including identity; no native halt/boundary/cap/cycle stop; requested horizon/resource outcomes external | Exact scalar/domain/string codecs, closed arithmetic programs, typed scalar traces, exact digit/fraction/size observers, quotient sibling and canonical page-117..122 oracles; no callback/float/history/NumPy packing/family branch |
| T37 Recursive Sequences | Consecutive indexed prefix over domain-tagged arbitrary-precision exact integers/rationals; origin and every prior term are state; no control | `NextSequenceTerm`; old-prefix `FixedLagRead`; normalized `AffineFixedLag` strict program plus named closed arithmetic-expression extension | `AppendTerm(index,dependencies,value)` + ninth sibling `AppendOnlySequenceUpdate`; every old term persists and exactly one endpoint is created | One deterministic `Advanced` successor per valid append, including repeated values; no native halt/cycle/boundary; invalid fixed references rejected before execution; external completion/resource outcomes | Exact prefixes/seeds/verified checkpoints, fixed-lag programs/reads, append update, compact reconstructible trace, lag-window quotient, page-143/Lucas/Perrin/factorial oracles; no callback/hidden trajectory history/fixed width/family branch |
| T39 Number-Theoretic Filtering Systems | Strict transition state is a closed ordered finite/intensional natural domain, consecutive-stage program, visible next-divisor cursor, and finite ordered survivors where materialized; pure filter and measurement specs are separate non-transition categories | `NextSieveStage`; proper-multiple read distinguishes all hits from newly removed survivors; closed predicates/measurements; `FirstAcceptedAscendingCandidate` may read an explicit old T37 prefix | `RemoveCandidateSubset(stage,hits,newly_removed)` + tenth sibling `MonotoneFilterUpdate`; retained candidate identities/order persist; pure filters/measurements have no update | Every valid strict stage advances, including composite zero-removal rows; no native halt; finite certification/requested horizons/items/resources distinct; infinite completion never claimed | Structural integer domains/predicates/measurements, pure filters/streams, strict sieve/trace, numeric observers, T37/Ulam composition, page-147/148/150 oracles; no callback/table/PrimeQ trace bypass/bitmap packing/family branch |
| T41 Function-Combination Systems | No transition state; immutable `MathematicalFunctionSpec` declares exact parameters, real/complex argument domain, scalar/fixed-vector codomain, closed expression, primitive version, partiality, and branches | No transition source/read/rule; pure point/sample/real-zero/complex-zero/crossing/extremum queries declare scope and numerical context | No transition result/update; typed exact/certified/approximate/undefined/failure values and multiplicity-aware zero events are query records | No successor or native halt; query completeness, partiality, resource limits, diagnostics, render horizons, and algorithm work traces remain distinct | Closed function AST/registry, exact/declared numeric codecs, domain/branch profiles, pure query/result algebra, segmented views, page-160..163/Notes presets, T42 bridge; no callback/sample-as-function/fake time/family branch |
| T43 Iterated Maps | One domain-tagged exact or explicitly represented real scalar in a verified interval; no control/history; explicit fixed-vector box/torus sibling | `UniqueScalar`; complete old-value read; immutable closed map AST with exact parameters, ordered piecewise/fractional primitives, version, and replayable self-map/partial contract | `MapAssignment` returns typed `Assign(MapStateSlot,next)` and reuses atomic fixed-effects commit; vector outputs read one old tuple and assign simultaneously | One deterministic successor per strict event, including unchanged fixed points; `h` events give `h+1` states; no native halt/boundary/escape; partial siblings retain last state on typed undefined/escape/failure | Exact/certified/tracked/fixed-realization values, closed map/invariance records, typed orbit traces and analyzers, 11 asset presets/oracles, T41 expression/T34 assignment reuse; no callback/float/raster/history/family branch or eleventh law |
| T44 Continuous Cellular Automata | Fixed ordered 1D lattice + total exact or explicitly represented real field, strict range `[0,1]`; no control/history; integer-line and explicit finite-cycle/segment realizations | `AllSites`; ordered old `(left,self,right)`; closed exact affine neighborhood aggregate with divisor followed by a closed scalar map and replayable composite closure | Typed same-site `Assign`; T01 atomic parallel fixed-field commit, so no eleventh update law; stochastic siblings resolve explicit draws before the same commit | One deterministic strict successor including unchanged fields; `h` events give `h+1` states; no native halt; native topology not explicit, Notes ring/causal work/crop distinct; local failure commits nothing | Total continuous fields, affine aggregate/map rules, exact field state, certified/tracked computation records, represented field feedback, field runs/analysis/views/stochastic draws/presets, strict/supporting asset oracles; T01/T41/T43 reuse with no float alphabet/callback/field pack/family branch |
| T45 Partial Differential Equation Systems | No transition state/control; an immutable differential equation plus continuous region, side data, `Classical` solution concept, and regularity contract denotes a set of real-scalar, complex-scalar, or fixed-real-vector fields | No transition source/read/rule; closed multivariate bound expressions, field references, derivative multi-indices, fixed matrices, equations, trace relations, and pure verify/solve/evaluate/property requests | No transition result/update; exact witnesses, approximate numerical solutions, nonuniqueness/no-solution/uniqueness/singularity claims, and `Unknown`/`Unsupported`/resource/numerical failures retain their proof strength | No native successor or halt; the solution set may be empty, singleton, or multiple; only a separately justified IVP profile derives a continuous flow with explicit Cauchy traces; discretizations are related realizations | Continuous-region/differential-expression/problem/query/verifier modules plus explicit discretization, solver, analysis, sample, and view records; reuse T31/T41/T44 responsibilities without a `pde` rollout branch or an eleventh update law |

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
| DOMAIN/support/topology | DOMAIN is the task/program space with its dimensional character, labeled support, and topology; it is not restricted to dense `Z^4`. Evidence includes fixed/variable 1D words and lattices, scalar `t+0D`, trees, bags in continuous geometry, rooted graphs, candidate supports, and continuous problem regions. Number systems, alphabets, address sets, function definition sets, and numeric representations are not DOMAINs. | ACTIVE shared axis; each topology has typed invariants/realizations, while declarative scopes remain explicit | T01, T02, T03, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30, T31, T34, T37, T39, T41, T43, T44, T45 |
| Values/alphabet | Explicit finite values with ordered ranks and separately declared numeric color valuations; epsilon words; exact naturals/signed integers/reduced rationals; named/algebraic/certified/declared-precision real/complex values and enclosures; represented finite-format values; total exact/represented continuous fields; fixed numeric vectors; indexed prefixes/candidate partitions; pattern/geometry/graph values; exact sets; histograms and periodic fields | PROVISIONAL finite/infinite discrete, exact/declared/represented numeric and field, function/map value, prefix/filter, affine/point/vector, graph-reference, set-lifted, and constraint values | T01, T02, T03, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30, T31, T34, T37, T39, T41, T43, T44 |
| Control roles | Heads, active markers, instruction markers, and stage cursors must be visible in the complete configuration, but may be lossless tagged/product/marker roles within the ALPHABET or structure. A separate control object is an optional commuting view, never a second source of truth. | ACTIVE representation-neutral invariant; top-level `SingleControl` mandate retired | T09, T12, T19, T39; absent where no control role exists |
| Active loci | Firing/source selectors include sites, a unique scalar, the next sequence term or sieve stage, control loci, ordered/bag occurrences, network nodes, program-coupled flat/tree matches, queue prefixes, instructions, and every literal match across every word in a layer | PROVISIONAL fixed/scalar/prefix-end/stage/control/sequence/bag/graph/interval/queue/code/tree/multiway-match sources; not applicable to pure specifications/queries | T01, T02, T03, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30, T34, T37, T39, T43, T44; absent T31/T41 |
| Reads/access | Ordered topology values, exact fixed-arity finite-color sum quotients, and continuous neighborhood triples; the complete current scalar or old vector tuple; fixed indexed old-prefix lags; complete explicit prefix contexts; proper-multiple survivor partitions; control payload; self values; spans/prefixes; operands; tree bindings; geometric poses; graph path/signatures; or exact matched parent intervals; read and mutation coverage may differ | PROVISIONAL for transition profiles; mathematical function evaluation remains a distinct pure query | T01, T02, T03, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30, T34, T37, T39, T43, T44; distinct T41 |
| Rule choice | Complete ordered-context and exact-sum tables, total morphisms, ordered rewrite programs, closed instructions/templates/ASTs, topology tables, unordered finite literal relations, closed constant arithmetic, normalized fixed-lag affine programs, closed integer predicate/measurement plus schedules, a closed self-map AST, or a closed affine neighborhood aggregate followed by a scalar AST with replayable composite contract; no implicit defaults/callbacks | PROVISIONAL transition-program members; closed mathematical expressions are definition data for T41 and feedback programs under explicit T43/T44 contracts | T01, T02, T03, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30, T34, T37, T39, T43, T44; distinct T41 |
| RULE writes/replacements | Closed typed results name scalar/label writes, blocks, spans, tree/graph/geometry replacements, endpoint insertions, subset removals, marker moves, or successor alternatives. Semantic roles may be tags/products; no control-specific or family-specific result wrapper is required. | ACTIVE RULE axis; declarative query results remain outside rollout | T01, T02, T03, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30, T34, T37, T39, T43, T44; distinct T31/T41/T45 |
| UPDATE composition/schedule | One runner calls a typed UPDATE axis. Implementations compose snapshot label writes, ordered replacements/splices, tree/bag/graph replacements, endpoint growth, subset removal, and set-valued successors according to explicit schedules and invariants. These are policies inside the protocol, not numbered executors or top-level construction classes. | ACTIVE shared axis; exact implementation sum remains Goal 2 work; not applicable to declarative nonfits | T01, T02, T03, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30, T34, T37, T39, T43, T44; not applicable T31/T41/T45 |
| Successors | UPDATE may yield one configuration, a finite exact set of configurations for multiway rewriting, typed quiescence/reference stutter, a retained zero-successor terminal outcome, or typed no-commit failure. A powerset/layer view is an explicit lift with full witnesses. | ACTIVE runner result algebra; declarative query/model results remain distinct | T01, T02, T03, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30, T34, T37, T39, T43, T44; distinct T31/T41/T45 |
| Halting/invalidity | Base continuation, terminal/no-match/prefix outcomes, quiescence, explicit exit, all-dead-to-empty advancement, empty-layer stutter, undefined/escape/evaluation failure, observers, certificates, projection, validation, resource, and rendering cutoffs are distinct | PROVISIONAL outcome model; T02/T03/T43/T44 strict fixed/cycle/convergence/background repetition has no native halt; query completeness/partiality/resources and render horizons are not native halts | T02, T03, T12, T16, T17, T19, T20, T27, T29, T30, T31, T34, T37, T39, T41, T43, T44 |
| Trace encoding | Transition snapshots/events remain distinct from pure filter/measurement/function results, verified models, constraint/function/map/field-analysis records/certificates, numerical-realization relations, solver diagnostics, algorithm work traces, stochastic draw records, and downstream renderings | PROVISIONAL transition traces plus explicit non-trace records; `h` T43/T44 events produce `h+1` states; global schema UNRESOLVED | T01, T02, T03, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30, T31, T34, T37, T39, T41, T43, T44 |
| Constraint/solution | Closed local relations denote mathematical model sets; periodic/open/window presentations have explicit scopes; exact verification differs from search and solution enumeration | ACTIVE category split; T32/T33 and other constraint carriers must re-audit relation syntax | T31 |
| Function/denotation | Closed unary mathematical expressions declare one argument, parameters, real/complex domain, scalar/fixed-vector codomain, primitive versions, partiality, and branches; point/sample/zero/crossing queries are separate; compatible syntax can sit inside a map contract | ACTIVE pure T41 category and reusable syntax responsibility; structural identity, certified functional equivalence, map relation, and observation equality remain distinct | T41, T43 |
| Map/feedback | A closed self-map over an explicit state space repeatedly feeds one result into atomic state assignment; strict totality/invariance, partiality, and numerical realization are explicit | ACTIVE T43 transition category; ideal exact, certified computation, tracked significance, and fixed-rounded feedback are distinct profiles/relations | T43 |
| Field/feedback | A closed affine neighborhood aggregate followed by a closed scalar expression updates a total real field from one old snapshot; exact/certified/tracked/fixed-rounded/stochastic profiles and support/work/crop scopes remain explicit | ACTIVE T44 transition category; directly reuses the CA snapshot UPDATE and keeps additive/coupled/noisy/block/PDE siblings typed | T44 |
| Solver/numerics | Exact numeric evaluation is semantic where declared; approximate/certified queries carry full context; fixed-rounded feedback changes T43's effective map and T44's effective field transition; constraint/function/map/field solvers use separate scoped results/certificates; evaluators and fast-forward methods never replace definitions or requested traces | PROVISIONAL exact/declared/represented numeric, evaluator, query-result, and solver boundaries | T27, T31, T34, T37, T39, T41, T43, T44 |

## Decision Log

### D000 — Foundation defers, and the completed audit establishes, the common algebra

- Status: ACTIVE after architecture reclosure.
- Basis: `principles.md:3-28` and the absence of completed type evidence.
- Consequence: evidence through T45 establishes the branch-free `FRONTIER -> NEIGHBORHOOD -> RULE -> UPDATE` SimpleProgram runner for transition/rewrite systems. Constraint/model sets, uniterated function definitions, and general PDE relations without a posed evolution remain evidenced nonfits rather than receiving fabricated steps.

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

### D004 — First validated executor algebra is fixed-lattice synchronous assignment

- Status: SUPERSEDED by the SimpleProgram architecture audit.
- Basis: `goal-1/2-T01-ELEMENTARY.md`, especially `BOOK:418-430`, `850-854`, and `10984-10992`.
- Shape: `AllSites -> ordered old-snapshot read -> exhaustive table -> Assign -> ParallelUpdate`.
- Consequence: T01 validates the cellular-automaton preset of the branch-free runner: fixed lattice, all-site frontier, local stencil, scalar label writes, and snapshot-parallel UPDATE. These are axis values, not the executor algebra. Step/rewrite systems share the runner; nonstep constraints/functions/general PDEs do not.

### D005 — Separate semantic support, computation realization, and trace extent

- Status: ACTIVE.
- Basis: T01's infinite local line (`BOOK:8832`, `11250`), finite cyclic programs (`:3026`, `10986`), exact causal width (`:11124`), and Principles 6–8/12.
- Consequence: native `Z`, a finite cycle/segment or causal-halo work region, and emitted `[t,x,0,0]` coordinates are three inspectable layers. Current `Dynamics.shape` cannot silently represent all three.

### D006 — Ordered reads and rule-code significance are separate validated objects

- Status: ACTIVE.
- Basis: T01 exact rule index `right + 2*self + 4*left` (`BOOK:10988`) versus current `_channel_state` low-significance-first encoding (`src/ca/rollout.py:742-760`).
- Consequence: a neighborhood owns semantic read order; an exhaustive codec owns digit significance and validates it against arity/alphabet. Family-local selector reversal is rejected as a shim.

### D007 — Same-site assignment is an explicit result member

- Status: ACTIVE as one RULE-result preset.
- Basis: the rule chooses the center cell's next color (`BOOK:428-430`) and all such choices commit from old values in parallel (`:10984`).
- Consequence: use a typed same-locus label write with explicit snapshot-parallel UPDATE. Other typed replacements extend the RULE/UPDATE axes; do not create family-specific assignment wrappers or treat a bare callback-returned value as universal mutation semantics.

### D008 — Elementary identity is a strict preset over generic data semantics

- Status: PROVISIONAL pending Goal 2 synthesis.
- Basis: `k=2,r=1` identity (`BOOK:11050`), arbitrary eight-case table (`:712-720`), and Principles 9–10.
- Consequence: a discoverable `elementary(n)` entry may pin Boolean alphabet, fixed 1D support, all sites, ordered radius-one reads, exhaustive table, and parallel assignment, but cannot select a separate executor or embed a seed/boundary.

### D009 — Frontier selects firing sources, not writable targets

- Status: ACTIVE; revalidated by the representation-architecture audit.
- Basis: T09's rule applies at the old active cell, writes that source, and independently moves control to a neighbor (`BOOK:854-862`, `11957-11970`).
- Consequence: `FRONTIER.select(configuration)` returns rule-firing loci, occurrences, or matches. `RULE` results name typed writes/replacements and `UPDATE` composes them. T01 is the all-sites/source-equals-target preset; the current writable-next-coordinate-only schema wording must broaden without adding a second executor.

### D010 — Visible control is a role in the complete configuration, not a mandated storage class

- Status: ACTIVE after architecture correction.
- Basis: Notes state `{list,n}` explicitly exposes values and active position (`BOOK:11957`), random values still require one active locus (`:14275`), and `ref/notes/alphabets.md:54-101` gives finite composite/tagged values as the lossless alternative.
- Consequence: snapshots, seeds, equality, serialization, batching, and traces preserve every control role. `Plain(v) | Active(v)` with exactly one tag is equivalent to `(values,position)`; explicit products/markers are likewise valid. Metadata, executor locals, display marks, opaque integers, and any second unsynchronized control source remain invalid.

### D011 — RULE may return multiple typed writes/replacements for one atomic UPDATE

- Status: ACTIVE after architecture correction.
- Basis: each T09 table entry returns new active-cell value plus displacement, and `MAStep` returns the changed field and relocated control together (`BOOK:11960-11970`); T12 also changes control payload (`BOOK:12014-12023`).
- Consequence: the compact T09/T12 tuples lower to ordinary typed label writes at source/destination and commit from one old snapshot. Atomicity is required; `TransitionControl` is not. Other block/span/tree/bag/graph/set-valued replacements remain closed RULE-result/UPDATE-axis variants inside the same runner.

### D012 — Ordered read codec is shared across T01 and T09

- Status: ACTIVE; revalidated by the architecture audit.
- Basis: T09 executable `Take[n-1..n+1]` and the rule figure establish physical `[left,self,right]`; its `{35,57}` bytes use `index=4L+2C+R`, the same ordering established by T01.
- Consequence: no mobile-specific permutation is required. The shared current low-significance-first runtime codec remains a defect, and asymmetric physical `100`/`011` cases are required tests.

### D013 — Full traces preserve every control role before observations compress them

- Status: ACTIVE after representation-neutral correction.
- Basis: the standard mobile trace includes both cell colors and active-position dots (`BOOK:5840`); record-extrema compression (`:878`) and causal networks derived from position history (`:16388`) are later transformations.
- Consequence: raw traces preserve the complete labeled configuration, including active/head tags or other visible control factors. A separate control stream is optional and must commute with the canonical representation. Frame compression, causal graphs, and visualization are downstream and never feed execution.

### D014 — Head state is an explicit finite role in a lossless composite label

- Status: ACTIVE after architecture correction.
- Basis: Turing state explicitly separates head state, tape values, and head position (`BOOK:12014`), while each transition changes both state and position (`:12016-12023`).
- Consequence: canonical cells may be `Plain(sigma) | Head(q,sigma)` (equivalently `Sigma x Option[Q]`) with exactly one head. This is bijective to a factored tape/position/state view and commutes one step at a time; the head-bearing cell retains the underlying symbol. `SingleControl` is at most an optional checked view/cache, never a required class or second source of truth.

### D015 — Unbounded fixed tapes use inspectable total fields

- Status: PROVISIONAL; evidenced by T12 blank tape.
- Basis: the Notes define `a[_]=0` and allow writes at integer head positions (`BOOK:12034-12040`); the finite-list guard gives no edge semantics.
- Consequence: represent at least uniform-default plus explicit overrides as semantic field data. Finite tensors, gather boundaries, and display extents are realizations and cannot fake unbounded writes or control motion.

### D016 — Termination, episode stopping, horizons, and errors are distinct

- Status: ACTIVE.
- Basis: base machines do not typically halt (`BOOK:18812`); Busy Beaver reaches explicit halt state 0 (`:12081`); head-position/tape-pattern criteria are alternatives (`:19240`).
- Consequence: base T12 uses `Never`; terminal-control variants retain one final state then have zero successors; external stop policies report separate reasons. Missing rules, invalid moves, finite edges, and horizon exhaustion never become implicit halts.

### D017 — Source corruption is repaired transparently and guarded by independent evidence

- Status: ACTIVE evidence practice.
- Basis: Turing numbering Notes at `BOOK:12047-12049` drop `k` from a divisor; literal text cannot enumerate `2sk` outputs. Rule count, output roles, mixed-radix bijection, page-94 image, and known code 3024 determine `{2k,2,1}`.
- Consequence: preserve the OCR caveat, state the repaired mapping, and require known-code/table/trajectory tests. Do not silently copy broken source or discard a recoverable codec.

### D018 — `UPDATE` is a real semantic algebra choice

- Status: ACTIVE.
- Basis: T13 replaces every old occurrence by an ordered word and constructs successor support by concatenation (`BOOK:982-986`, `1058-1062`, `12099-12107`). Fixed-support assignment instead preserves loci.
- Consequence: preserve one branch-free FRONTIER/NEIGHBORHOOD/RULE/UPDATE runner. UPDATE is a typed axis whose policies compose label writes, ordered structural replacements, graph/bag edits, or successor alternatives according to explicit schedules. T13's length growth justifies an ordered-replacement policy beyond same-locus scalar writes, not a second executor or top-level construction class.

### D019 — Ordered replacement consumes parents and derives children

- Status: PROVISIONAL; evidenced by T13.
- Basis: every old element fires once in parallel, blocks retain internal/source order, and tree/causal views expose descendant relations (`BOOK:1006-1016`, `5944-5952`, `16418-16423`).
- Consequence: `AllOccurrences` yields snapshot-scoped ordered source handles; `ReplaceOccurrence(source,word)` proposals cover every old source exactly once; commit creates children in `(parent_order,child_ordinal)` order and may emit lineage events. IDs never enter the T13 rule, and semantic word equality can quotient over order-preserving ID renaming.

### D020 — Basic T13 tables are total, closed, nonempty morphisms

- Status: ACTIVE for T13; T15 must re-audit empty outputs.
- Basis: prose says each symbol kind is replaced and ordinary examples replace each source by at least one new element (`BOOK:986`, `992`, `1026-1028`), while Notes implement `Sigma -> word` (`:12099-12107`).
- Consequence: validate one unique row for every declared symbol, outputs in the same alphabet, and `word in Sigma+`. Mathematica unmatched identity and syntactic empty lists are not defaults. The unbounded family has no evidenced integer rule numbering; bounded counts are derived only under an explicit bound.

### D021 — Dynamic ordered support, lineage, and trace addresses are separate

- Status: ACTIVE for T13.
- Basis: only sequence order is significant when positions shift (`BOOK:1046`); ordinary substitution admits infinite random input (`:14275`); tree/path/box/2D views are alternate observations (`:996-1016`, `12210-12230`).
- Consequence: represent a discrete ordered configuration natively, with explicit finite or countably infinite support and an explicit cut when needed. Row-local `[t,x,0,0]`, finite observation windows, ragged storage, lineage events, padding, and render scale are downstream layers. An infinite seeded field is inspectable/query-order-independent data, never a callback or hidden RNG cursor.

### D022 — Match-source applicability may be intrinsically program-coupled

- Status: ACTIVE for literal rewrite systems.
- Basis: T16 must scan the whole word for clause 0 before trying clause 1, and choose that clause's leftmost match (`BOOK:1062-1078`, `12289`). A source interval cannot be selected without the ordered left sides.
- Consequence: `FRONTIER.select(state)` remains the runner interface. A program-coupled `FirstApplicableMatch` frontier holds a typed reference to the one authoritative immutable `OrderedLiteralRewriteProgram` also used by RULE; it never receives a duplicate LHS table or unrestricted matcher callback. T01/T09/T12/T13 remain program-independent frontier presets.

### D023 — Single interval splice is an exactly-one ordered UPDATE schedule

- Status: ACTIVE as a restriction of the ordered-replacement UPDATE axis; former separate-law framing retired.
- Basis: exactly one matched block is replaced per step while its prefix/suffix remain in order (`BOOK:1062-1068`, `2358`, `5936-5940`). T13 instead consumes every old occurrence and concatenates all child blocks.
- Consequence: use one typed ordered-replacement UPDATE with an `exactly_one` old-span schedule, clause-priority/leftmost FRONTIER, and preserved prefix/suffix order. T13 uses the same axis with complete singleton coverage. Public presets retain their validators without separate executors.

### D024 — Empty source selection has construction-specific outcomes

- Status: ACTIVE.
- Basis: T16 effectively stops only when no replacement applies (`BOOK:12289`), while T13's empty occurrence set evolves vacuously and T12 can terminate through explicit control.
- Consequence: the executor returns typed `Advanced` or `Terminal(reason)` outcomes; it has no global empty-frontier rule. T16 retains the final snapshot once and reports `NoMatch`. An applicable identity clause is an event/self-loop, not a terminal state; horizon, external stop, invalidity, and error remain distinct.

### D025 — Base T16 is an ordered nonempty literal-clause program without rule numbering

- Status: PROVISIONAL for T16; T15 must re-audit erasing outputs.
- Basis: all direct examples and Notes rules use nonempty literal sides (`BOOK:1064-1072`, `12269-12288`), rule order matters (`:1070-1078`, `12289`), variable block sizes are ordinary (`:19164`), and no T16 numbering/count convention exists.
- Consequence: validate an ordered nonempty clause sequence with `lhs,rhs in Sigma+`, preserve duplicates/order, and reject empty LHS. Do not require an integer ID or infer deletion from multiway examples/host syntax. T17 later proves that the private word/edit carrier must support `Sigma*` (D028), but the T16 public validator remains nonempty; T15 must still audit deletion without an `allow_empty` flag.

### D026 — Prefix-queue read width and deletion number are distinct semantic roles

- Status: ACTIVE for the T17 family; Wolfram ordinary tags pin the roles equal.
- Basis: Wolfram selects from and deletes the full leading `n` (`BOOK:1112`, `12296-12305`); Post selects by only the first element while deleting `n`, and Wang lag systems inspect more than the first while deleting one (`:12311-12313`).
- Consequence: represent an immutable `PrefixQueueProgram(q,d,total Sigma^q->Sigma*)` with positive typed widths. `RequiredQueuePrefix` exposes separate read/consume spans and exact occurrence IDs. Strict `tag_system(n,table)` constructs `q=d=n`; Post/Wang restrictions are structured data, not booleans, widened neighborhoods, callbacks, or executor modes.

### D027 — Prefix consumption plus remote tail append is an anchored ordered UPDATE policy

- Status: ACTIVE as an anchored ordered-replacement UPDATE policy; former separate-law framing retired.
- Basis: tag systems remove the beginning and tag the selected block onto the end (`BOOK:1112`, `1124`, `1132`); executable order is `Join[Drop[word,n],appendant]` (`:12300-12306`). For canonical `01->10`, `011` becomes `110`, whereas a T16 front splice would produce `101`.
- Consequence: RULE returns the appendant and consume extent; the ordered UPDATE deletes `[0,d)` and inserts at the old endpoint atomically. Separate read/delete widths, old-tail order, and short-residue outcomes remain semantic validation, while the shared runner and ordered-replacement axis remain unchanged.

### D028 — Generic structural words/edits admit epsilon without weakening construction validators

- Status: ACTIVE.
- Basis: canonical T17 case (a) has `10->{}` and the bounded count includes words of length zero (`BOOK:12298`, `12308`), while T13 and direct T16 evidence require their public outputs to remain nonempty.
- Consequence: the private `Word`/ordered-edit carrier supports `Sigma*`. T17 `ConsumePrefixAppend` may carry epsilon; T13 `ReplaceOccurrence` and base T16 `ReplaceInterval` retain `NonEmptyWord` validation. No `allow_empty` flag, silent family-wide broadening, or reopening is needed; T15 will still audit its own deletion construction.

### D029 — Insufficient prefix retains its residue; source-compatible extinction is a projection

- Status: ACTIVE for T17 and the general outcome/trace boundary.
- Basis: the direct prefix rules cannot apply to `|w|<n`, and PCP calls halt a state where no rule applies (`BOOK:12302-12306`, `19294`). The supplied `TSEvolveList` instead maps a short state to `{}` on the next requested sample (`:12300`); figure case (c) reaches disabled residue `0` at step 287 and reference `{}` at 288.
- Consequence: return `Terminal(InsufficientPrefix, residue=w)` with zero successors. An opt-in, labeled reference-history projection may emit/pad `{}` while preserving its source residue/reason. Successful empty output, empty/short terminal state, `NoMatch`, external stop, horizon, invalidity, and error remain distinct; no fake deletion event or hidden normalization occurs.

### D030 — Complete prefix-word tables have bounded counts but no canonical integer code

- Status: ACTIVE for T17.
- Basis: the Notes count `(sum_{j=0}^r k^j)^(k^n)` complete tables and give `50,625` for `k=2,n=2,r=3` (`BOOK:12308`); no numeric row/digit convention is supplied. Host `/.` would accidentally append an unmatched key unchanged.
- Consequence: validate exactly one alphabet-closed output for every `Sigma^q` key, including epsilon, and reject missing/duplicate rows. Structured program serialization is authoritative; compute counts only under explicit bounds, use the sum form at `k=1`, and never invent a rule ID, default appendant, or first-match row priority.

### D031 — Finite named banks and exact infinite values are native state members

- Status: ACTIVE for T19.
- Basis: the base registers store non-negative numbers “of any size” (`BOOK:1166-1170`), and state explicitly contains a finite register list (`BOOK:12368-12374`).
- Consequence: add `FiniteRegisterBank` over exact arbitrary-precision `Naturals`; stable register keys provide identity/serialization but no lattice adjacency. Finite alphabets, NumPy integers, floats, unary regions, saturation, fake maxima, and object-array substitution are not equivalent.

### D032 — Visible control may address immutable program data rather than mutable support

- Status: ACTIVE after representation-neutral correction.
- Basis: the program counter is visible state and selects the current instruction from a fixed sequence (`BOOK:1176-1180`, `12368`), while the selected instruction names its register operands.
- Consequence: represent the program counter as one visible marker/tag or explicit product factor in the complete configuration. `ActiveInstruction` is a FRONTIER and instruction-owned operands are a NEIGHBORHOOD over typed address spaces. No `SingleControl` class, duplicated table, hidden fetch loop, arbitrary-address callback, or family dispatcher is required.

### D033 — Closed register instruction results reuse atomic typed effects

- Status: ACTIVE after representation-neutral correction.
- Basis: increment changes one register and falls through; positive decrement changes one register and jumps; zero decrement preserves the value and falls through (`BOOK:1166-1172` and the repaired `RMStep` at `BOOK:12377`).
- Consequence: use tagged instruction results to return validated register-label and program-marker writes against one snapshot. The shared atomic UPDATE applies them together; no `TransitionControl`, register executor, partial timing, formula callback, or zero-as-negative/clamp behavior is required.

### D034 — Past-program-end quiescence and program-exit termination are distinct

- Status: ACTIVE for T19 and the general outcome/trace boundary.
- Basis: repaired reference `RMStep` returns an out-of-range counter/register state unchanged, while the Notes separately call a special halt interpretation merely convenient (`BOOK:12377`, `12382`). Main examples loop through explicit jumps (`:1176-1180`).
- Consequence: return event-free `Quiescent(PastProgramEnd,state)` for exact reference semantics and label repeated reference samples. An explicit `ProgramExitStop` may instead yield retained zero-successor `Terminal(ProgramExit)`. The last valid event, quiescence, terminal interpretation, wrap, external stop, horizon, invalidity, and error never collapse.

### D035 — Register programs have structured identities, explicit target profiles, and independent seeds

- Status: ACTIVE for T19.
- Basis: exact-length count `(k(n+1))^n` counts `k` increments plus `kn` in-program decrement-jumps at each ordered slot (`BOOK:12380`), while the square-root program deliberately targets one past its 14 instructions (`:18619-18624`). Figures use zero seed but arbitrary register values are native/compilable (`:1176-1182`, `12374-12380`). No numeric code ordering is supplied.
- Consequence: preserve ordered tagged-instruction serialization; use a counted `EnumeratedInProgram` profile and a general positive-exit-target profile. Keep program and seed separate, treat prepend-increment setup and register swaps as relations, and derive zero-hit/arithmetic views from full events. Never invent an integer rule code, behavior quotient, default wrap, or canonical random register distribution.

### D036 — Ordered expression trees require typed head/argument paths

- Status: ACTIVE for T20.
- Basis: symbolic heads may themselves be arbitrary expressions, while the Chapter 3 unary profile forms binary trees (`BOOK:12408-12426`). The canonical seed's first selected redex is its head occurrence, not an argument or flat substring (`BOOK:1222-1224` and the page-117 figure).
- Consequence: add finite well-founded `Expression = Atom | Apply(head,args)` and `ExpressionPath = Head | Argument(i)` data. Equal subtrees remain distinct occurrences; display coordinates, bracket offsets, host object identity, mutable-DAG aliasing, and whole-tree scalar packing are forbidden semantics.

### D037 — Symbolic programs are closed structural pattern/template data

- Status: ACTIVE for T20.
- Basis: named blanks bind complete expressions, arbitrary structural LHSs and anonymous blanks are documented, the base/S rules duplicate bindings, and K deletes one (`BOOK:1222`, `12456`, `18924-18930`).
- Consequence: add literal/application/bind/anonymous pattern nodes, literal/application/binding-reference template nodes, ordered clauses, immutable binding environments, and inert substitution. Repeated references create occurrence-distinct copies; unbound references and undeclared atoms reject. No regex, condition/evaluator callback, `Any`, or opaque host pattern object.

### D038 — One symbolic pass selects an ordered maximal prefix-free old-tree match set

- Status: ACTIVE for T20.
- Basis: each step scans functional notation once left to right, applies wherever possible, and avoids overlap; `NestList[# /. rule&,init,t]` fixes one-pass timing (`BOOK:1224`, `12407`, `12466`). Figure boxes and the exact trajectory establish head eligibility, disjoint coverage, ancestor suppression, and newborn deferral.
- Consequence: use program-coupled outermost preorder selection: try clauses in order at a node, prune descendants of the first match, then continue head/arguments left to right. Every selected path and binding is snapshot-scoped. Bottom-up, rule-major, first-only, overlapping, unordered, in-place, or same-pass-rescan execution is a different construction.

### D039 — Prefix-free parallel subtree replacement is a tree UPDATE strategy

- Status: ACTIVE as a tree-topology UPDATE strategy; former ordinal-law framing retired.
- Basis: one pass can consume several disjoint subtrees, preserve surrounding context, duplicate/delete/rearrange whole bound subtrees, and atomically produce one tree (`BOOK:1222-1224`, `12456`, `18924-18930`).
- Consequence: add typed subtree replacement writes and a prefix-free tree UPDATE implementation with exact path/source validation, one old snapshot, context preservation, and lineage. It is one topology-specific strategy on the shared UPDATE axis, not a symbolic executor or fifth top-level law.

### D040 — No-pattern quiescence, applicable identity, and symbolic representations remain distinct

- Status: ACTIVE for T20 and the general outcome/trace boundary.
- Basis: `/.` returns an unchanged expression when no rule applies; the book calls reached forms fixed and `NestList` can keep sampling them (`BOOK:12407`, `12446`, `12466`). Bracket/Polish/tree forms, valuations, depths, and size plots are separately described representations or properties (`:1228-1238`, `12409-12454`).
- Consequence: emit event-free `Quiescent(NoPatternMatch,state)` with an exact reference self-successor; optional quiescent/value-fixed stops are observers. An applicable identity is `Advanced(changed=false)`. Preserve ragged tree snapshots and match/binding lineage before any codec, padding, raster, numeric valuation, normalization, confluence quotient, cycle observer, or rule enumeration.

### D041 — Geometric state is a multiplicity-preserving bag of fully posed occurrences

- Status: ACTIVE for T27.
- Basis: the main construction replaces independently placed oriented squares, requires each parent's orientation, and permits later descendants to overlap (`BOOK:2326-2344`). In the exact page-190 orbit, two occurrences after three replacements have the same center and same square footprint but frames differing by 90 degrees and different next descendants (`goal-1/10-T27-GEOMETRIC.md`).
- Consequence: add immutable local-frame prototypes and finite occurrence bags of `(prototype_id,full_local_to_world_affine_pose)`. Bag permutation is immaterial and multiplicity is material. Center clouds, present footprints, unions, rasters, prototype-symmetry quotients, branch indices, stable IDs, and list positions cannot replace native state; IDs/order remain trace or reference-codec data.

### D042 — Child geometry is parent-local and composed in an explicit scalar carrier

- Status: ACTIVE for T27.
- Basis: the page-204 orientation arrow and primary rule diagrams require local child placement. The exact page-189/page-190 Notes formulas admit rational matrices with `A'=A_parent A_child` and `b'=A_parent b_child+b_parent`; a rotated/translated adversary distinguishes `P∘C` from `C∘P`. Page-191 also contains source-declared approximate coefficients.
- Consequence: total prototype rows contain closed local affine child templates and stable slot IDs. Composition is `parent_pose∘local_pose` over normalized exact rationals/algebraics or an explicitly separate finite-precision profile with literal, precision, and rounding provenance. No world-coordinate transform callback, silent float coercion, tolerance equality, or fabricated exactification is allowed.

### D043 — Full-generation occurrence-bag replacement is a bag-composition UPDATE strategy

- Status: ACTIVE as a bag-composition UPDATE strategy; former ordinal-law framing retired.
- Basis: every old square is replaced once by all of its local children; parents disappear, newborns wait, descendants coexist through overlap, and duplicate/coincident branches retain multiplicity (`BOOK:2326-2354`, `13760-13762`).
- Consequence: use all-occurrence FRONTIER, self pose reads, typed child replacements, and a parallel occurrence UPDATE parameterized by the multiplicity-preserving bag combiner. Validate full old coverage, consume parents, compose slots, retain duplicates, and record lineage. This is not a geometric executor or sixth top-level law.

### D044 — Geometric overlap, enumeration order, limits, and rendering do not feed back

- Status: ACTIVE for T27.
- Basis: overlap appears without collision behavior, off-grid elements have no obvious neighbors, and interaction is introduced only in the separate gridded construction (`BOOK:2334-2366`). The Notes center list is a parent-major reference projection, while dimensions, generation stacks, parameter maps, and fractal limits are analyses/views (`BOOK:13758-13804`).
- Consequence: occurrence order, overlap graphs, intersection/union, painter order, rasterization, viewport/crop, branch-word and center codecs, convergence, dimension, and parameter filters are downstream. A nonempty total program always emits one `Advanced` generation, including an applicable identity; horizon and resource/cancel stops are external. T28 must establish any neighbor/collision policy rather than adding a flag here.

### D045 — Nonlinear complex branches require a distinct closed point-map profile

- Status: ACTIVE for T27.
- Basis: the Notes separately iterate finite Möbius-map sets and the two inverse-square-root branches `{Sqrt[z-c],-Sqrt[z-c]}` (`BOOK:13774-13782`). These maps warp/branch points and are not affine poses of a rigid prototype; Mandelbrot boundedness is a parameter observer rather than that transition.
- Consequence: use a separate bag of exact algebraic extended-complex points and a closed affine/Möbius/inverse-square-root AST. Möbius poles map to infinity; an inverse branch emits both signed results, retaining coincident multiplicity at branch points and infinity. It may share all-old-source bag expansion with geometry, but not a generic function callback, host NaN, affine-shape state, chaos-game sampler, or Mandelbrot filter.

### D046 — Mutable network state is a rooted labeled graph, not a drawing

- Status: ACTIVE for T29.
- Basis: the construction makes positions explicitly nonfundamental, gives every node two distinguished outgoing connections, permits loops/cycles/sharing, and retains the component of the first node (`BOOK:2368-2448`).
- Consequence: add finite nonempty `RootedPortGraph` with total `Vertex×{Above,Below}->Vertex` and directed root reachability. Tokens are alpha-renamable occurrence identities. Layouts, display indices, adjacency padding, automorphism/bisimulation quotients, and T20/T27 carriers are not state.

### D047 — Port-path and exact-length reach reads are closed old-snapshot data

- Status: ACTIVE for T29.
- Basis: page-214 rules follow written labeled paths, while `Follow` and `NeighborNumbers` evaluate them against one old graph and compute exact-length endpoint-set cardinalities (`BOOK:2424-2484`, `13814-13887`).
- Consequence: use finite `PortWord` data, `PortPathRead`, and declared `ExactLengthReachCounts` key sets. Epsilon is self; words fold left-to-right. No traversal callback, reversed codec, cumulative ball substitution, or synthesized generic-depth key/count is allowed.

### D048 — Fresh graph vertices are typed result occurrences

- Status: ACTIVE for T29.
- Basis: page-215 inserts one new node from every old node, and the Notes allocator appends distinct new nodes whose outgoing links resolve through old paths (`BOOK:2452-2464`, `13848-13872`).
- Consequence: `NodePortRewrite` contains two `DirectOld(path) | InsertFresh(a,b)` expressions. Each syntactic insertion occurrence creates a distinct event-local token; equal descriptors never alias. Fresh targets are old endpoints, tokens are not rule data, and newborns do not fire.

### D049 — Parallel graph reroute/create/project is a graph UPDATE strategy

- Status: ACTIVE as a justified graph UPDATE-axis extension; former ordinal-law framing retired.
- Basis: every old node is rewritten from one old snapshot; old nodes persist in the raw successor, fresh nodes are installed, then `ConnectedNodes`/`RenumberNodes` retain directed reachability from node 1 (`BOOK:2440-2464`, `13848-13872`).
- Consequence: the shared runner needs a graph-capable UPDATE implementation with exact old coverage, frozen proposals, injective births, rewiring, newborn deferral, directed root projection, and provenance. Fixed-support label writes cannot create vertices without a hidden pool, but this does not justify a network executor or seventh top-level law.

### D050 — Rooted two-port isomorphism has an exact BFS codec

- Status: ACTIVE for T29.
- Basis: graph meaning ignores drawing/list labels but preserves the first/root node and above/below connections (`BOOK:2380-2394`, `2424-2448`). Every strict state is root-reachable and deterministic by port.
- Consequence: breadth-first discovery from root with `Above` before `Below` gives an exact canonical pair array. Use it for equality/serialization/cycle observers while retaining raw token maps in events. Do not merge vertices, erase ports/root, or use general layout/graph-library behavior as semantics. An isomorphic successor is still `Advanced(changed=false)`.

### D051 — Sequential-network source gaps must remain an explicit boundary

- Status: ACTIVE evidence practice.
- Basis: the sequential Notes and official CDF give six `{rewrite,move_port}` rows and a node-count figure evidences pruning, but no evaluator fixes old-versus-committed movement, projection anchor, or movement/projection order (`BOOK:13889-13903`).
- Consequence: parallel T29 remains complete, but Goal 2 must mark the sequential FRONTIER/schedule/profile unavailable pending decisive primary evidence. Do not silently inherit node-1 projection, choose a timing, expose both as flags, or treat figure layout as an oracle.

### D052 — A base multiway configuration is one word; layers are explicit finite-set lifts

- Status: REVISED by the architecture audit.
- Basis: the main definition retains all **distinct** sequences, and executable `MWStep` applies `Union` to all generated strings (`BOOK:2494-2510`, `13921-13938`).
- Consequence: the smallest native configuration is one exact word. UPDATE returns its finite exact successor set; a `FiniteSet[Word]` layer is the explicit powerset/rollout lift across branches. Epsilon, the empty successor set, exact equality, nonmultiplicity, and full derivation witnesses remain distinct; clause/worker/hash order is nonsemantic.

### D053 — Multiway applicability selects every overlapping old literal match

- Status: ACTIVE for T30.
- Basis: `StringPosition` enumerates every occurrence of each LHS in every old string, and `StringReplacePart` produces one result per position (`BOOK:13921-13948`); Chapter 9 describes paths as sequences of single replacements (`6016-6022`).
- Consequence: add program-coupled `AllApplicableLiteralMatches` and reuse T16's pure matched-span/one-splice kernel per branch. Matches include overlaps, are alternatives rather than simultaneous edits, and newborns wait. T16 priority/leftmost selection and host pattern callbacks are not reused.

### D054 — Multiway UPDATE returns an exact finite successor set

- Status: ACTIVE as the generic successor-set lift; former ordinal-law framing retired.
- Basis: `MWStep` maps all rules/parents and `Union`s exact targets; the Notes call merging crucial and explicitly erase derivation multiplicity in pictures (`BOOK:13923-13938`, `13959-13961`).
- Consequence: UPDATE makes one successor configuration per alternative write, deduplicates exact-equal children, and retains every inbound witness/dead end. Layer evolution exact-unions those successor sets. This is the runner's zero/many-successor result algebra, not a multiway executor or eighth top-level law.

### D055 — Dead parents, epsilon, all-dead advancement, and empty-layer stutter differ

- Status: ACTIVE for T30 and the outcome boundary.
- Basis: page-206 uses `AB->""` and explicitly drops no-match strings (`BOOK:13950-13957`); the reference maps an empty input list to itself through `Union[{}]`.
- Consequence: epsilon is a live word. Every nonempty layer yields an eventful `Advanced`, even when its child set is empty or unchanged. Only the empty layer is event-free `Quiescent(EmptyLayer)` with reference stutter. No T16 per-word terminal outcome, implicit identity, persistence, or epsilon/empty collapse.

### D056 — Layer recurrence and compressed graphs are separate from provenance

- Status: ACTIVE for T30 and trace design.
- Basis: the same word can occur at many steps, while page-224 separately folds it to one graph node (`BOOK:2552-2566`); pictures omit how many applications create an edge (`13959`), and the spacetime model is explicitly alternative (`16511-16519`).
- Consequence: raw traces preserve exact layer sets, every `(parent,clause,span,child)` witness, dead ends, and child groups. Simple edges, derivation multigraphs, and one-node-per-word compressed graphs are derived. Global visited suppression, chosen ancestry, or witness weighting cannot affect later firing.

### D057 — Literal restrictions may share the engine; other multiway carriers do not

- Status: ACTIVE for T30.
- Basis: semi-Thue/group and literal grammar profiles restrict clause data, while pattern variables, arrays/networks, cyclic strings, tags, numbers, machines/games, and causal-event systems alter matching, support, multiplicity, or state (`BOOK:13988-14025`, `19324-19339`).
- Consequence: bidirectional and literal grammar presets may reuse base stepping without quotienting exact words. Defer separately typed variants; notably, multiway-tag code omits `Union` and cyclic conventions are underspecified. No canonical rule number/random distribution exists, and no mode flag or callback fills these gaps.

### D058 — Constraint systems denote model sets, not transitions

- Status: ACTIVE genuine nonfit; evidenced by T31 and revalidated by the architecture audit.
- Basis: the main text contrasts explicit stepwise evolution with complete configurations implicitly selected by constraints and says search must go outside the system (`BOOK:2568-2578`, `2642-2664`).
- Consequence: T31 has no canonical frontier/write/update, successor, seed, or trajectory. Use the generic declarative relation/model-set and query/certificate category, never zero-step dynamics, fixed-point rollout, or an invented repair process.

### D059 — Local count constraints are closed center-conditioned histogram relations

- Status: ACTIVE for T31.
- Basis: the strict examples constrain neighbor color counts around each center on the nearest-neighbor line or four-cardinal grid (`BOOK:2574-2612`).
- Consequence: use `LatticeFootprint` plus total `center_symbol -> finite allowed NeighborHistogram set`. Footprint offsets are nonzero/distinct and each contributes once; alphabet/footprint order is representational. Exact/at-least profiles compile to explicit sets. No predicate, boundary, custom graph, solver, or totalistic next-value rule belongs in the spec.

### D060 — Infinite, periodic, finite-window, and open-patch scopes are distinct

- Status: ACTIVE for T31 and representation design.
- Basis: the native line/grid is infinite, page-226 wrap/tessellation supplies an exact periodic witness, and the search discussion distinguishes finite regions from global extendibility (`BOOK:2594-2604`, `2642-2664`).
- Consequence: support closed axis-aligned periodic presentations with exact LCM-box equivalence, finite windows with full variable halo, and diagnostic open patches. Periodic SAT promotes globally; finite-window SAT/open consistency does not; certified finite-window UNSAT may. No padding, fake finite `Z^d`, vacuous patch SAT, or silent boundary conversion.

### D061 — Verification, solver results, and certificates are separate closed data

- Status: ACTIVE for T31 and the solver boundary.
- Basis: candidate checking is local while finding/proving absence can require backtracking and unbounded work (`BOOK:2642-2664`, `3980-4064`, `14080-14084`).
- Consequence: pure violations and verification reports are separate from scoped `Satisfiable/Unsatisfiable/Unknown/ResourceLimit` query records. Reverify every witness; replay every closed case-split/domain-wipeout obstruction. Bounded failure is `Unknown`, solver state/gray cells are diagnostics, and no callback/trusted boolean enters semantics.

### D062 — One-dimensional local constraints admit an exact de Bruijn analyzer

- Status: ACTIVE for T31.
- Basis: allowed length-`n` blocks form arcs among `k^(n-1)` overlap states, so any infinite path contains a periodic cycle (`BOOK:14040-14044`). The page-225 profile gives the exact 4-cycle.
- Consequence: a cycle is a periodic global witness; acyclicity/topological order is an exact UNSAT certificate for the 1D profile. Periodic sufficiency does not say every model is periodic and does not generalize to arbitrary 2D constraints.

### D063 — Count, oriented-template, and existential-template constraints stay separate

- Status: ACTIVE boundary across T31/T32/T33.
- Basis: neighbor counts occupy `BOOK:2568-2612`, exact oriented allowed templates begin `2614`, and a required occurrence begins `2632`.
- Consequence: count, oriented-template, and existential-template are tagged closed relation forms under one declarative constraint algebra, with distinct validation and denotation. Do not collapse their roles into opaque predicates/flags, over-attribute undecidability, or use reductions as native coverage.

### D064 — Arithmetic iteration is a unary exact scalar construction

- Status: ACTIVE as a `t+0D` unary SimpleProgram preset.
- Basis: the strict main examples start from one scalar and repeatedly add one constant or multiply by one constant (`BOOK:1439-1495`).
- Consequence: use a singleton `t+0D` DOMAIN, an explicit exact numeric value carrier, singleton FRONTIER/self NEIGHBORHOOD, and closed unary RULE nodes `AddConstant | MultiplyConstant`. T43 shares this runner and write semantics. Do not introduce scalar executors, callbacks, digit-state packing, or hidden history.

### D065 — Exact numeric carriers, typed identity, and serialization are explicit

- Status: ACTIVE for T34 and shared numeric infrastructure.
- Basis: canonical integer powers/addition and exact rational powers of `3/2` are stated directly, while the Notes distinguish real/finite representations and their limitations (`BOOK:1479-1495`, `12503-12536`, `13217-13247`).
- Consequence: initial Goal 2 support is arbitrary-precision signed integers and normalized rationals; numeric-carrier tags participate in identity, while cross-carrier numeric equivalence is an observer. Serialize big integer components as decimal strings. Certified-real and declared-precision profiles are separate; reject implicit promotion, booleans/floats, tolerance equality, undeclared rounding, or exact-to-approximate coercion.

### D066 — Arithmetic scalar assignment reuses fixed typed effects

- Status: ACTIVE for T34.
- Basis: each valid operation replaces the one old scalar with exactly one result and has no structural support change (`BOOK:1443-1495`).
- Consequence: RULE emits the ordinary same-locus next value and the shared atomic UPDATE commits it. `ArithmeticAssignment` is at most an event/provenance role, not a semantic effect class. Every valid application advances, including identity, with no native halt/capacity/cycle/threshold.

### D067 — Digits and plots are exact observers, while modulus is an explicit sibling

- Status: ACTIVE for T34 and representation design.
- Basis: the source presents the same values as base-2 rows, fractional-part dots, lengths, counts, and cropped views; it separately identifies `3^n mod 2^s` as an LCG relation (`BOOK:1443-1495`, `12538-12570`, `3722-3744`).
- Consequence: digit views declare base/order/radix/sign/window/crop/padding and never feed back. Fractional/value/size/count/leading-digit views remain downstream. Finite suffix evolution is separately typed `MultiplyMod` over a residue ring, not a render crop, hidden overflow, or current AR2.

### D068 — Closed forms and compilers do not change event traces

- Status: ACTIVE for T34 and evaluator design.
- Basis: `x_0+t*c`, `x_0*c^t`, direct digit formulas, repeated squaring, and special CA encodings reproduce requested observations more quickly or in another carrier (`BOOK:7380-7424`, `7974-7980`, `9058-9080`, `17849-17920`).
- Consequence: expose optional exact random-access evaluators and explicit compilation mappings, but a requested `h`-event trace still has `h+1` states and `h` real events. No fast-forward result may fabricate provenance, skip requested snapshots, or turn CA/substitution/LCG state into native arithmetic state.

### D069 — Neighboring scalar catalogs share a shell, not one rule algebra

- Status: REVISED: neighboring scalar catalogs share the unary-rule axis as well as the runner where their closed syntax fits.
- Basis: parity branching begins T35 at `BOOK:1497`, digit feedback begins T36, recursive-history and real interval maps have different state/access invariants, and continuous fields/PDEs add spatial or derivative semantics.
- Consequence: T34/T35/T36/T43 can use one closed tagged unary RULE algebra over explicit value carriers and invariants; their predicates/digit transforms/self-map contracts remain typed nodes, not operation flags or callbacks. T37/T38 have growing sequence DOMAIN/support, T44 has a spatial field, and T45 is declarative unless a flow is derived.

### D070 — Recursive-sequence state is the complete indexed numeric prefix

- Status: ACTIVE for T37 and a required starting point for T38.
- Basis: the source names stable terms `f[1],f[2],...`, computes `f[n]` from earlier terms, and presents the accumulated sequence (`BOOK:1555-1567`).
- Consequence: add `NumericPrefix(carrier,origin,terms)` with consecutive support and exact ordered values. A newest scalar, hidden trajectory history, or bounded lag window is not canonical equality. T34 remains unary scalar assignment even when its value stream matches a T37 projection.

### D071 — Strict T37 programs are normalized affine fixed-lag data

- Status: ACTIVE for T37.
- Basis: the main text fixes positive distances behind `n`, and the Notes explicitly classify every page-128 row as linear (`BOOK:1561-1567`, `12690`). Factorial is separately named nonlinear evidence (`12692-12696`).
- Consequence: strict programs are `bias + sum(coefficient[lag]*f[n-lag])` with unique positive literal lags and exact numeric-carrier values. Fresh seed length equals `max_lag`; longer resumptions are replay-verified checkpoints. A named closed `Literal|TargetIndex|Lag|Neg|Add|Sub|Mul` extension covers factorial after strict conformance; callbacks, computed indices, branches, and arbitrary recursion remain excluded.

### D072 — One-term persistent append is an endpoint-insertion UPDATE preset

- Status: ACTIVE as an endpoint-insertion UPDATE policy; former ordinal-law framing retired.
- Basis: each step determines the next indexed term from the old sequence while every earlier term persists (`BOOK:1559-1567`).
- Consequence: use an endpoint FRONTIER, declared old-prefix reads, one typed term insertion, and the shared ordered structural UPDATE. Validate the exact next index/dependencies, preservation of the complete old prefix, and one newborn endpoint. This remains a construction preset/validator, not a recursive executor or ninth top-level law.

### D073 — Prefix traces may be stored compactly; lag windows are only quotients

- Status: ACTIVE for T37 and trace architecture.
- Basis: a seed of length `L` plus `h` appended terms determines `h+1` nested prefixes, while fixed-lag evaluation needs only the next index and last `L` values.
- Consequence: store seed/checkpoint plus ordered append events and reconstruct `state_at(j)`; do not duplicate prefixes quadratically. The lag-window map may accelerate execution when its commuting law is checked, but it is non-injective and cannot replace canonical state or reproduce discarded history without the full log. The page figure is a final term-stream view, not the rollout state sequence.

### D074 — Repeated values still advance and fixed-reference invalidity is static

- Status: ACTIVE for T37.
- Basis: rows (b) and (e) repeat numeric values, yet every ellipsis continues an ever-longer indexed sequence; runtime invalid indices appear only with T38's value-computed references (`BOOK:1567-1575`).
- Consequence: every validated exact T37 event has one structurally changed `Advanced` successor and no native halt/cycle/fixed-point stop. Reject nonpositive/current/future/dynamic lags and insufficient fresh seeds before execution; do not add padding, wrap, clamp, default, or halt-on-missing policies. Completion, cancellation, resources, and backend failure stay external.

### D075 — Recurrence analyzers, modular variants, and global-history searches remain explicit

- Status: ACTIVE boundary across T37/T38/T39/T43 and numeric infrastructure.
- Basis: characteristic equations and Fibonacci formulas are derived evaluators; logistic is explicitly an iterated-map relation; generalized Fibonacci RNGs add modulus; Ulam searches all previous pairs for the next candidate (`BOOK:12146-12163`, `12698-12702`, `15049-15053`, `12840-12844`).
- Consequence: closed forms/matrices/generating functions/memoization do not change requested append traces. Modular AR2 uses a residue-ring value carrier, not exact T37. T39 resolves Ulam as `FirstAcceptedAscendingCandidate` over the complete old prefix followed by the existing T37 append; it is not hidden in the fixed-lag AST and does not reopen T37 state/update semantics.

### D076 — T39 splits transition sieves from pure filters and measurements

- Status: ACTIVE category split for T39.
- Basis: page 147 explicitly shows successive removal rows, while page 148 calls its curves features of the resulting prime sequence and page 150 describes sequences based on number properties (`BOOK:1623-1633`, `1641-1663`).
- Consequence: use separately typed `SuccessiveDivisibilitySieve`, `IntegerFilterSpec`, and `IntegerMeasurementSpec`. Only the sieve has source/read/result/update/successor semantics. Finite accepted/rejected partitions, lazy streams, direct queries, and exact `g(n)` results remain pure records; do not invent empty transition fields or force them through rollout.

### D077 — The strict sieve uses consecutive stages and a visible cursor

- Status: ACTIVE for T39 strict execution.
- Basis: the prose advances from divisor 2 to 3 “and so on,” and the page-147 raster labels every row `2..13`, including composite stages with zero new removals (`BOOK:1623-1627`). All 1,200 cells match the proper-multiple rule.
- Consequence: `SuccessiveDivisibilitySieveProgram` has `ConsecutiveIntegers(first=2)` and finite/intensional state includes a `next_divisor` marker. Hits are all original-support proper multiples, while `newly_removed=hits intersect old_survivors`. Equal survivor sets at different markers are unequal states; a zero-removal composite row is still `Advanced(changed=false)` because the marker advances. Prime-pivot scheduling is an explicit trace-distinct variant.

### D078 — Monotone candidate-subset removal is a subset/marker UPDATE policy

- Status: ACTIVE as a typed subset-removal/marker UPDATE policy; former ordinal-law framing retired.
- Basis: each stage deletes a possibly noncontiguous survivor subset, never resurrects a removed value, and preserves every retained integer's identity and increasing order (`BOOK:1623-1627`; exact page-147 masks).
- Consequence: RULE returns typed survivor removals and the next-stage marker write; the shared UPDATE commits them atomically. Validate exact old-snapshot witnesses, subset membership, cursor advance, no resurrection, and retained identity/order. A mask is only a realization; no sieve executor or tenth top-level law is introduced.

### D079 — Literal display, candidate support, certification, and completion are explicit scopes

- Status: ACTIVE for T39 and finite/infinite execution policy.
- Basis: the caption starts with `1..100`, but the rule and raster retain `1` while bottom labels omit it; rows continue through 13 even though a bound-100 primality certificate is available after divisor 10 (`BOOK:1627`; original raster).
- Consequence: preserve a faithful figure profile whose final black set is `{1} union primes<=100`, and define the mathematical prime preset with lower bound 2 or an explicit pre-exclusion. Never call `1` prime or silently repair the figure. Finite certification uses `next_divisor^2>upper_bound`; requested rows/items, certification, cancellation, resources, finite crops, and infinite mathematical scope remain distinct. An infinite sieve never reports global completion.

### D080 — Number-theoretic measurements and observers carry exact conventions

- Status: ACTIVE for T39 pure specifications and observers.
- Basis: page-150 Notes specify divisor/aliquot formulas, signed integers including zero for square representations, Jacobi's four-square formula, and an ordered prime-choice program; page 148 names prime/count/gap/analytic profiles (`BOOK:12869-12873`, `12881-12901`).
- Consequence: closed `IntegerMeasurementSpec` data declares tuple order, signs, zero, repetition, and distinctness; a filter arises only through an explicit comparison. Prime prefixes, `PrimePi`, gaps, residue excesses, spectra, and analytic errors are observers. `LogIntegral` names normalization and numerical context. Direct `PrimeQ`, factor tables, analytic formulas, and precomputed outputs cannot replace a requested sieve trace.

### D081 — Closed first-accepted selection composes T39 with T37 Ulam append

- Status: ACTIVE across T37/T39.
- Basis: the Ulam Note starts `(1,2)`, appends the smallest value having one representation as a sum of two previous values, and supplies `1,2,3,4,6,...` (`BOOK:12840-12844`). The value 3 rejects ordered-pair double counting; value 4 rejects self-pairs; advancement past 3 rejects rescanning emitted values.
- Consequence: add `FirstAcceptedAscendingCandidate(start=last(prefix)+1,predicate,explicit_context)` with `UniqueUnorderedDistinctPriorPairSum` over indices `i<j` in the complete old prefix. Candidate checks form a nested selection witness; only the accepted value is a T37 endpoint insertion. Pair-sum tables are reproducible caches, not semantic state. T37's full-prefix state and fixed-lag boundary remain unchanged.

### D082 — T41 mathematical functions are immutable closed definitions outside transition execution

- Status: ACTIVE genuine nonfit; revalidated by the architecture audit.
- Basis: the source asks about “functions themselves,” plots their curves, and describes finite arithmetic combinations without any update/evolution language (`BOOK:1834-1848`). Supporting Notes explicitly identify named mathematical functions as accepted primitives in formulas (`BOOK:17794-17798`).
- Consequence: use a generic versioned closed-function definition plus query/result records declaring argument space/definition set, codomain, exact parameters, expression, primitives, partiality, and branches. It has no canonical frontier/write/update/successor. Iteration is an additional T43 SimpleProgram, not fake argument-as-time rollout.

### D083 — Function argument set and numerical query context are separate scopes

- Status: ACTIVE for T41 definition/evaluation boundaries.
- Basis: strict rasters show finite windows while named functions have larger mathematical domains; `Tan`/`Sec` contain poles; high-precision evaluation depends on precision and algorithm (`BOOK:1838-1842`, `19185-19187`; original page-160 raster).
- Consequence: the spec owns argument space, domain restrictions, exact parameters, codomain, partiality, continuation, and branches. Each query separately owns interval/region, endpoint policy, exact/arbitrary/fixed/certified mode, precision, rounding/error targets, method, and resources. Raster size, mesh, viewport, evaluator, and plot settings never enter function identity.

### D084 — Function evaluation and zero/crossing analysis use typed pure query results

- Status: ACTIVE query/result algebra for T41.
- Basis: exact factorization yields two sine/cosine zero families, three-term sums introduce complex zeros and spacing distributions, and page 162 relates a derived interval word to T42 (`BOOK:13153-13172`). `Cos[x]-Cos[alpha x]` has a double zero at zero, while `Tan`/`Sec` pole branches can mimic sample sign changes.
- Consequence: distinguish point, sample, real-zero, complex-zero, crossing, and extremum queries. Results are exact values, certified enclosures, approximate values with context, typed undefined values, or failures. Zero events record multiplicity, crossing/tangent classification, endpoint membership, and certification; result status records complete/partial/unknown/resource. Sampled sign changes are candidates only and cannot certify completeness or distinguish poles/even roots by themselves.

### D085 — Structural function identity, certified equivalence, and observation equality remain distinct

- Status: ACTIVE identity/serialization boundary for T41 and shared mathematical syntax.
- Basis: the source explicitly factors a two-sine expression and attempts an ODE alternate definition (`BOOK:13153-13154`), but the printed derivative `2` yields `Sin[x]+Sin[sqrt(2)x]/sqrt(2)` rather than the stated target, which needs `1+sqrt(2)`. Evaluation precision and algorithms vary independently (`BOOK:19185-19187`).
- Consequence: structural IDs cover the normalized tagged argument, parameters, exact/declared values, domain/codomain, ordered AST, primitive version, partiality, and branches. Child order is preserved even for mathematically commutative operators; commutation, factoring, or alternate-definition equality is a separately certified relation over a domain. Literal and corrected ODE profiles remain distinct. Equal samples/rasters/tolerances never imply function identity. Tagged JSON preserves arbitrary integers, rationals, algebraics, decimal provenance, complex values, enclosures, and undefined reasons.

### D086 — Finite sums and infinite series require different closed definitions

- Status: ACTIVE boundary for T41 Fourier/Weierstrass variants.
- Basis: Notes distinguish finite sums with explicit `k` from approximations to an infinite weighted lacunary sum (`BOOK:13174-13192`). The displayed `a=0` terms do not approach zero generically, so ordinary infinite convergence is impossible.
- Consequence: strict expressions support exact bounded finite sums or expanded additions. Infinite series use a distinct tagged definition with convergence set, summation meaning, and evaluation context. No `infinity` sentinel in a finite binder, hidden truncation, raster width, or resource cap may masquerade as a mathematical infinite sum; the `a=0` picture is an explicitly truncated/otherwise specified approximation only.

### D087 — Page 162 is a typed T41-query/T42-construction composition

- Status: ACTIVE boundary across T41/T42.
- Basis: the main and Notes first derive two exact zero families and interval counts, then say the resulting word can be reproduced by a sequence of substitution rules whose choices come from continued-fraction terms (`BOOK:1850-1858`, `13170-13172`). The connection is explicitly absent for more than two sine terms.
- Consequence: T41 owns source functions, zero/crossing/touch semantics, and exact interval-count query results. T42 owns continued-fraction expansion, coefficient stream, symbols, rule schedule, substitution state/update, and trace. A typed finalized T41 result may feed T42; neither category embeds the other's callbacks/state, and the page-162 bitmap is never executable source data.

### D088 — T43 state is one real scalar in an explicit state interval under one immutable closed self-map

- Status: ACTIVE as a `t+0D` unary SimpleProgram profile.
- Basis: the defining paragraph repeatedly updates “a number between 0 and 1” by a fixed map that returns a definite number in the same interval (`BOOK:1868-1872`). Strict figures use four unary expressions and separate exact initial conditions (`BOOK:1874-1896`; page-165 raster).
- Consequence: use the same singleton FRONTIER/self-read/same-locus UPDATE as T34 with a real/represented value carrier, closed unary map AST, self-map invariant, and independent seed. `[0,1]` is a state/value interval, not DOMAIN; orbit prefixes, digits, counters, and hidden control stay outside configuration.

### D089 — T43 directly reuses generic singleton read/write/UPDATE

- Status: ACTIVE reuse across T34/T43.
- Basis: every event reads the current scalar, applies one map, and replaces it with one result; `NestList` confirms one initial snapshot plus one state per application (`BOOK:1870`, `10682-10687`).
- Consequence: singleton FRONTIER/self NEIGHBORHOOD and ordinary same-locus write/UPDATE are shared with T34. `UniqueScalar` and `MapAssignment` are descriptive roles/presets, not semantic classes. A fixed point application remains an event; only value, RULE, invariant, and realization profiles extend.

### D090 — Strict map admission requires replayable totality and invariance evidence

- Status: ACTIVE validation/partiality boundary for T43.
- Basis: the strict definition requires every possible input to yield a definite in-domain output (`BOOK:1870`), while Gauss/Newton variants can have poles and the strict maps include defined jumps/cusps (`BOOK:13218-13222`; page-165 raster).
- Consequence: admit a strict self-map only through a mechanically checked known constructor or replayable certificate tied to normalized syntax, state space, parameters, and primitive version. A trusted boolean is invalid. Source-faithful `FractionalPart(x)=x-IntegerPart(x)` and ordered exact `Piecewise` are closed primitives; on the strict nonnegative scope `FractionalPart` agrees with modulo one, but those tags differ on negative inputs. A discontinuity is not failure. Partial siblings return typed pole/missing-branch/outside/escape/evaluation outcomes and commit no partial event.

### D091 — Numerical feedback profiles are semantic and reproducible

- Status: ACTIVE exact/numerical split for T43.
- Basis: native Notes contrast tracked arbitrary precision, roughly 53-bit fixed binary arithmetic that drives doubling to zero, and 12-decimal-digit calculator arithmetic with a different eventual orbit (`BOOK:13223-13255`; page-934 raster).
- Consequence: distinguish ideal exact state, certified enclosure computation, tracked-significance work state/trace, and fixed-rounded recurrence. Tracked computation serializes its approximate value plus precision/error provenance without calling it the ideal mathematical point. A fixed realization includes radix, format, rounding, nonfinite/subnormal behavior, literal conversion, comparisons, rounding locations, and a normalized represented closure contract because rounded results feed later events. Unknown digits stay unknown. Binary and decimal realizations are related effective maps, not interchangeable query contexts or hidden backend defaults.

### D092 — Orbit events are initial-inclusive and cycles/convergence do not halt strict maps

- Status: ACTIVE trace/outcome policy for T43.
- Basis: `NestList` includes its initial argument, and strict digit rasters contain 81 or 121 initial-inclusive rows. The source repeatedly speaks of iteration/evolution but specifies no halt (`BOOK:10682-10687`, page-165/page-168/page-170 rasters).
- Consequence: `h` requested events yield `h+1` snapshots and `h` committed event records. Strict total maps always have one successor, even at fixed points and cycles. Cycle/fixed witnesses use replay-safe equality for the selected profile—canonical exact values for ideal runs and complete represented-state identity or proven transition congruence for fixed realizations. Period/convergence records, requested horizons, cancellation, resources, and render crops are analyzers/run outcomes; partial failures retain the last complete state.

### D093 — Digit/sensitivity/Lyapunov/attractor/parameter views remain outside transition state

- Status: ACTIVE observation boundary for T43.
- Basis: the main explicitly separates binary digits from sizes and explains sensitivity through digit transport without equating it to intrinsic randomness (`BOOK:1874-1886`, `1902-1946`). Native Notes define base-two Lyapunov growth and parameter families; attractor/bifurcation language occurs only in supporting passages (`BOOK:13273-13279`, `14699-14701`, `14936-14944`).
- Consequence: value/digit views, two-orbit comparisons, symbolic partitions, cycle/periodic-point solvers, finite/asymptotic Lyapunov records, attractor analysis, parameter sweeps, bifurcation plots, and rendering are typed consumers. Each declares its scope/conventions/evidence. None changes rule choice, stops native execution, proves randomness from sensitivity, or treats a finite raster as an exact theorem.

### D094 — Structural map identity, denotational equivalence, conjugacy, and observation equality differ

- Status: ACTIVE identity/serialization policy for T43 and shared function syntax.
- Basis: `FractionalPart[3x/4]` agrees with `3x/4` on `[0,1]` while remaining a distinct displayed expression; logistic `a=4` becomes the doubling map under `x=Sin[Pi u]^2`; exact iterate formulas can replace repeated algebra only for random-access evaluation (`BOOK:13222`, `13268`, `18010-18048`).
- Consequence: mathematical structural identity includes state space, ordered parameters/AST, primitive version, and normalized partiality/invariance contract, but excludes evaluator/realization choices and proof artifacts. A separate realized-transition ID references the ideal map plus complete finite-format feedback semantics and normalized represented closure contract. Certified functional equivalence, conjugacy/semiconjugacy, profile-specific orbit equality, and finite observation equality are separate replayable relations. Fast-forward formulas do not fabricate event traces. Tagged codecs preserve exact numbers, endpoints, enclosures, represented patterns, validation proofs, events, and analyzers without JSON floats.

### D095 — Vector maps are explicit simultaneous torus/box siblings; coupled fields remain T44

- Status: ACTIVE supplementary T43 profile and T44 boundary.
- Basis: native Notes give `{x,y}->Mod[m.{x,y},1]`, while T44 applies a map to neighborhood aggregates at every site (`BOOK:13272`, `1954`, `1982`, `13298`).
- Consequence: add fixed-dimensional `RealBox` and `UnitTorus` state spaces only as tagged siblings. Every output reads the same old tuple and commits one tuple assignment; torus quotient equality differs from box endpoint equality. Integer matrices descend to quotient-torus maps. The nonintegral-rational clause instead uses an ordinary closed representative box `[0,1]^d`, where literal `{1,1}` remains distinct from `{0,0}` before the first componentwise `Mod[...,1]`; its outputs lie in `[0,1)^d`. The repeated “rational” sentence is read in that integer/nonintegral sense, not silently changed to irrational. T44 owns lattice support, neighborhoods, aggregation, and simultaneous field commit; complex, partial, stochastic, and continuous-time maps retain explicit boundaries.

### D096 — T44 state is a total real-valued fixed-lattice field

- Status: ACTIVE generic-field specialization after DOMAIN/value correction.
- Basis: each discrete cell has any gray level from white `0` to black `1`, the point seed is one black cell on white background, and every next field is computed locally (`BOOK:1954-1960`, `2018`). The cardinality Note gives `2^aleph_0` possible configurations (`BOOK:19070-19072`) but does not determine support: a single real cell or any nonempty finite real vector has that cardinality too.
- Consequence: specialize the generic field configuration to a discrete `t+1D` fixed ordered lattice with continuous-valued `[0,1]` labels and no control/history. Value continuity does not make DOMAIN continuous. Preserve integer-line inference, periodic realization, sparse/default presentation, random-field provenance, and seed/rule/realization/trace/view separation.

### D097 — Closed affine aggregate and scalar map form one validated local program

- Status: ACTIVE rule/data boundary for T44.
- Basis: the strict law averages left/self/right and applies one fixed map; a later profile multiplies both neighbors by declared `1.13` before the literal division by three (`BOOK:1956`, `1982`, `2904`).
- Consequence: add `AffineNeighborhoodAggregate(offset_weight_terms,divisor)` and `AggregateThenMap` with ordered closed scalar syntax and replayable composite range validation from the value cube to the output interval. The intermediate need not stay in `[0,1]`: exact reconstruction `{113/100,1,113/100}/3` reaches `163/150`. Never use an arbitrary reducer/map callback, a normalized `2w+1` divisor, a trusted closure flag, or implicit clamp/modulo.

### D098 — T44 directly reuses T01 fixed-field snapshot UPDATE

- Status: ACTIVE reuse across T01/T44.
- Basis: all sites read the same old left/self/right values and assign one next value to the same site in parallel; Notes express the operation as one `Map` over old rotated lists (`BOOK:1956`, `13283-13292`).
- Consequence: reuse the CA preset's all-site FRONTIER, ordered old reads, typed next-label writes, and snapshot-parallel UPDATE. Infinite events may use compact before/after field identities. In-place/asynchronous/partial commit is invalid; there is one runner and no numbered update-family count.

### D099 — Native support, periodic helper, causal work, and raster crop stay distinct

- Status: ACTIVE T01/T44 support discipline.
- Basis: strict point-seed figures show finite causal observations but state no edge; `RotateLeft`/`RotateRight` explicitly defines a finite ring only in Notes (`BOOK:1956`, `13283-13292`). The add-constant background evolves at every site as `FractionalPart[t a]` (`BOOK:13300`).
- Consequence: serialize integer line, labeled finite cycle, finite segment/exterior, causal halo/work window, and crop separately. A zero-padded raster is not an infinite field. Mean diffusion tends pointwise to white on the line but to uniform `1/n` on an `n`-cycle; this realization difference is preserved rather than “resolved” by hidden boundary defaults.

### D100 — Numerical realization lifts from one map value to the whole field recurrence

- Status: ACTIVE exact/numerical split for T44.
- Basis: native Notes permit exact rationals or approximate `N` values and state that binary64 makes detailed page-157/page-160 behavior qualitatively wrong (`BOOK:13294`).
- Consequence: distinguish ideal exact fields, certified enclosure work/results, tracked-significance work/results, and fixed represented feedback fields. A represented transition records radix/format, literals, addition tree, division/map/assignment rounding, comparisons, `FractionalPart`, nonfinite policy, and versions because every rounded cell feeds later neighborhoods. Binary64/NumPy is never implicit exact semantics, and a public exact codec is tagged numeric/field data rather than an object array.

### D101 — T44 runs are initial-inclusive; backgrounds, differences, galleries, and classes are observers

- Status: ACTIVE trace/observation policy for T44.
- Basis: `NestList[...,init,t]` yields the initial list plus `t` updates; strict captions distinguish background repetition, adjacent differences, parameter galleries, and localized structures from the evolving gray field (`BOOK:2002-2014`, `13283-13292`, `13300-13304`).
- Consequence: `h` events yield `h+1` snapshots and never halt at an unchanged field, cycle, uniform limit, background period, or localized profile. Raw gray, center/background/mass, differences, palettes, sensitivity, parameter/class scans, and renders are typed consumers. Each gallery panel is an independently identified rule/run. Prose states only an adjacent difference; raster evidence strongly supports an absolute-right reconstruction, while direction/sign/wrap/normalization remain explicitly serialized observer data rather than source formula.

### D102 — Additive, coupled, boiling, stochastic, probabilistic, block, and PDE relations remain typed siblings

- Status: ACTIVE T44 boundary record.
- Basis: Notes separately give broader coupled-map aliases, `Mod[L+R,1]`, a discrete probabilistic-CA alternative, finite-difference relations, noisy continuous rule-90/rule-30 expressions, boiling as mean-plus-heating with a literal `>1` wrap threshold, and a complex unitary block construction (`BOOK:13296-13298`, `13306-13314`, `13401-13403`, `15074-15081`, `15644`, `17002-17008`).
- Consequence: the additive Pascal profile excludes center/division and has normalized binomial residues. Coupled maps are a typed relation/general constructor requiring user-declared closed combination/map data, not a promised book-exact logistic preset. Boiling keeps two records—literal threshold-conditional and strict cross-reference reconstruction—distinct at exact one. Noisy profiles consume explicit replayable draws and use widened/partial range because the literal formula exceeds `[0,1]`; numerical error is not noise. Discrete probabilistic CA, complex block updates, and T45 continuous-space/time equations do not enter strict T44 through flags, field packing, or discretization identity.

### D103 — T45 is a declarative differential problem and solution set, not an update system

- Status: ACTIVE genuine nonfit; revalidated by the architecture audit.
- Basis: strict T45 removes explicit cells/time steps and specifies derivative relations (`BOOK:2018-2026`); the native Notes state that a PDE has no built-in evolution or time and is a constraint on a function over a region whose data may admit many or no solutions (`BOOK:13357`).
- Consequence: closed differential relations/problems denote solution/model sets and have no canonical frontier/write/update/successor. They reuse generic declarative function/relation/query/certificate infrastructure. A fully specified and certified IVP may derive a SimpleProgram flow; solver work, formulas, discretizations, and views remain separate relations.

### D104 — T45 uses closed bound differential syntax over explicit variables and evidenced field codomains

- Status: ACTIVE expression/type boundary for T41/T45.
- Basis: strict equations bind time/space derivatives of one real field (`BOOK:2036-2042,2052-2066`); Notes add a fixed two-component concentration vector with matrix diffusion/coupling (`BOOK:15961-15969`) and a complex nonlinear-Schrodinger profile with `I` and `Abs` (`BOOK:13453`).
- Consequence: extend reusable exact/declared values and closed primitive/domain/branch syntax with ordered real independent-variable binders, field references, validated derivative multi-indices, scalar/vector equality, and fixed dimension-checked matrices. `ClosedBoundExpression` supplies one reusable multivariate carrier for complete candidate fields and locus-parameterized trace right-hand sides. The v1 field is real scalar, complex scalar, or one fixed real vector; callbacks, strings, host CAS objects, arbitrary tensors/manifolds, and T41's unary function wrapper are not PDE data.

### D105 — Equation, problem, candidate, witness, realization, sample, and view identities remain distinct

- Status: ACTIVE identity/serialization policy for T45.
- Basis: one explicit solution formula can answer a point without following the full behavior (`BOOK:2032`); the same differential constraint can have many or no solutions depending on region-edge information (`BOOK:13357`); numerical methods introduce separate discrete computations (`BOOK:13401-13435`).
- Consequence: structural equation identity includes variables, field/codomain, parameters, expression, and operator versions; problem identity adds region, side data, regularity, and concept. Candidate definition, verified witness/claim scope, numerical realization, sampled evaluation, and rendering each receive their own referenced identity and provenance. Equality at one layer never implies equality at another.

### D106 — Evolution is a derived IVP relation with explicit class, locus, and admissibility evidence

- Status: ACTIVE T45 flow/side-data boundary.
- Basis: diffusion, wave, and nonlinear profiles have different temporal orders and stated initial traces (`BOOK:2036-2042,2052-2066`), while Notes distinguish hyperbolic finite-domain dependence from elliptic global dependence and warn that too little or too much data changes solvability (`BOOK:13357,14031-14033`).
- Consequence: equation order is derived from the AST but never guesses sufficient data or well-posedness. A versioned equation-class claim, locus analysis, and `SideDataAdmissibilityClaim` must justify any derived flow. The scoped `t45-cauchy-core-v1` preset may validate only its evidenced noncharacteristic profiles and required traces; the literal diffusion-plus-zero-velocity data is reported incompatible rather than silently repaired.

### D107 — PDE results preserve proof strength and v1 exposes only the classical solution concept

- Status: ACTIVE query/result/certificate policy for T31/T45.
- Basis: equations may lose regular behavior (`BOOK:2074,13349-13355`), region data may admit many or no solutions (`BOOK:13357`), numerical details can remain uncertain despite work and approximate conservation (`BOOK:13437-13443`), and one exact solution can belong to a wider family (`BOOK:19159`).
- Consequence: exact candidate witnesses prove only scoped existence; two verified distinct witnesses prove only nonuniqueness; solver failure or bounded search proves neither nonexistence nor singularity. `NoSolution` and `UniqueSolution` require replayable certificates, while `Unknown`, `Unsupported`, `ResourceLimit`, instability, nonconvergence, and invalidity stay distinct. `Classical` plus one `DifferentialRegularity` owner is the only public v1 concept; weak/distributional claims remain unsupported rather than guessed.

### D108 — Every numerical discretization is an explicit relation to the PDE problem

- Status: ACTIVE mathematical/numerical boundary for T45 and T44.
- Basis: finite difference replaces continuous space/time with discrete cells, every named numerical method ultimately discretizes, and artifacts can masquerade as PDE behavior (`BOOK:13401-13411`); the source code fixes periodic rotations, two time layers, `dx=.1`, `dt=.05`, 401 spatial samples, and 400 iterations (`BOOK:13413-13435`).
- Consequence: a numerical realization records truncation, mesh/coordinates, stencils, side-data lowering, integrator/adaptivity, arithmetic, tolerances, stopping/resources, backend versions, and output sampling. The Notes recurrence is a reproducible related discrete experiment, never native PDE state or T44 identity. Residual, consistency, stability/Courant, refinement/convergence, conservation, and proved total-error claims remain distinct.

### D109 — Mathematical, numerical, sampling, and display scopes stay separate

- Status: ACTIVE scope/topology policy for T45.
- Basis: periodic side data are explicit in one two-Gaussian problem (`BOOK:13328-13332`), one-, two-, and three-dimensional solutions differ while the figures show transformed one-dimensional slices (`BOOK:13340-13347`), and PDE constraints apply inside named regions from edge information (`BOOK:13357`).
- Consequence: serialize whole Euclidean space, finite regions, named strata/hypersurfaces, and periodic identifications independently from numerical truncations, meshes/halos, requested sample sets, and viewports/crops. A grid, CA boundary option, sampled array, or finite raster cannot stand in for a continuous region or field.

### D110 — Solver work, sampled values, diagnostics, and views are observers

- Status: ACTIVE observation/work boundary for T45.
- Basis: direct formula evaluation is distinct from following a solution (`BOOK:2032`); displayed dimensional slices are transformed observations (`BOOK:13340-13347`); source plates depend on numerical methods and can contain uncertain artifacts (`BOOK:13413-13443`); the nonlinear-Schrodinger plate displays `Abs[u]` rather than the complex field itself (`BOOK:13453`).
- Consequence: iteration histories, adaptive/rejected steps, refinement and residual histories, energy/stability diagnostics, point/restriction/sample evaluations, projections/slices, absolute-value transforms, tones/palettes, crops, and labels never enter equation, problem, solution, or solver-realization identity. Work cannot feed back as hidden mathematical data, and a view cannot certify correctness.

### D111 — T02 parameterizes T01 and directly reuses its runner axes

- Status: ACTIVE shared fixed-lattice construction for T01/T02.
- Basis: strict T02 changes the elementary alphabet from two to three colors while retaining nearest-neighbor CA rules (`BOOK:772,4684`); the Notes expose the general nearest-neighbor form `{n,k}` (`BOOK:11051-11056`), the same ordered triple (`BOOK:11014`), and old-value parallel assignment (`BOOK:850,10984`).
- Consequence: the CA preset accepts any explicit finite ALPHABET, including product/tagged cells, with fixed ordered support, all-site FRONTIER, old local reads, typed next-label writes, snapshot UPDATE, realization, and trace semantics. T01 fixes `k=2`; strict T02 validates `k>=3`. No branch or executor is added.

### D112 — Ordered alphabets, complete structural tables, and positional codes have separate identities

- Status: ACTIVE alphabet/table/codec policy for T01/T02.
- Basis: three colors produce all 27 three-cell cases (`BOOK:4684`); Wolfram's general rule uses ordered positional weights `{k^2,k,1}` (`BOOK:11066-11067`), exactly `k^(k^(2r+1))` rules and base-`k` digit lookup (`BOOK:11897-11900`), with neighborhood colors ordered like their offsets (`BOOK:13513`).
- Consequence: the semantic RULE is a total function/table over explicit labels; rank order and Wolfram integer code are lossless serialization/provenance maps, not extra semantics unless the preset declares them. The codec formula, leading rows, bounds, bigint strings, and round-trip invariants remain exact.

### D113 — Mutation, reversibility, search, and emulation stay outside T02 execution state

- Status: ACTIVE provenance/property/analyzer/relation boundary for T02.
- Basis: the source's mutation sequence edits one of 27 rule cases between immutable programs (`BOOK:4684`); reversibility selects 1,800 members of the full rule space (`BOOK:5218-5222`); purpose search can leave cases unvisited without reducing the full table (`BOOK:20573-20579`); and binary emulation explicitly converts a three-color rule into another construction (`BOOK:18339-18348`).
- Consequence: a run references one immutable complete table. A mutation is a table-delta/provenance record, reversibility is a scoped property with evidence, search work and behavior classifications are analyzer records, and emulation is an explicit relation among programs/supports/step groupings/decoders. None becomes cell/control state, a stochastic rule event, native backward execution, an incomplete-table fallback, or native binary storage.

### D114 — Alphabet rank, numeric aggregation, and palette are distinct color roles

- Status: ACTIVE T02/T03/T06/T07 and representation boundary.
- Basis: the strict text separates unrestricted three-color rules from totalistic rules (`BOOK:772-776`); for `k>2`, totalistic status depends on the numeric values assigned to colors (`BOOK:11897`), while the general codec depends only on ordered positions/ranks (`BOOK:11066-11067,13513`). White/gray/black are presentation names in the strict example, not a mandated arithmetic or display contract.
- Consequence: T02 requires only value identity plus an explicit rank/unrank map for exhaustive lookup and coding. T03 owns any declared numeric aggregate, a palette owns only rendering, T06 owns quiescent/background-preserving table predicates, and T07 owns reflection/symmetry predicates or transforms. Base T02 accepts non-totalistic, non-quiescent, asymmetric tables; none of these siblings becomes an executor flag or changes native T02 state/update semantics.

### D115 — T03 numeric valuation and exact fixed-arity sum quotient are program semantics

- Status: ACTIVE value/aggregate boundary for T03.
- Basis: strict totalistic rules assign white, gray, and black the exact values `0,1,2` and depend only on the neighborhood average (`BOOK:774-776`); the general count notes that for `k>2` totalistic identity depends on the values assigned to colors (`BOOK:11897`); and the executable definitions sum all `2r+1` old neighborhood values with equal weight (`BOOK:11902,11904,11908,11914,11916`).
- Consequence: T03 declares a validated bijection `nu:A->{0,...,k-1}`, fixed radius `r>=1`, arity `q=2r+1`, and exact quotient `s=sum_i nu(read_i)` with image `0..q(k-1)`. The source's average is the exact label `s/q`, never a floating computation. Equal-sum contexts merge even when their order or color histograms differ; alphabet rank, host order, and palette cannot silently supply arithmetic meaning.

### D116 — The complete sum table is native; its code and exhaustive lowering are explicit relations

- Status: REVISED by the lossless-representation audit.
- Basis: the strict code places the result for average zero at the rightmost digit and proceeds through increasing averages to the left (`BOOK:776`); the general rule count gives `k^(1+(k-1)(2r+1))` tables (`BOOK:11897`); and the Notes construct a padded `M=1+(k-1)(2r+1)`-digit base-`k` rule and index it by the neighborhood sum (`BOOK:11902,11904,11908,11910,11912`).
- Consequence: valuation, equal-weight sum descriptor, and complete `U` remain the compact source-faithful representation and codec provenance. The validated expansion `T(context)=U(sum_i nu(context_i))` is a lossless representation of the same local function and commutes one step at a time; it is not an arbitrary CA table, hidden shortcut, or permission to substitute a different reducer.

### D117 — T03 reuses the fixed-lattice CA preset and runner

- Status: ACTIVE shared execution boundary for T01/T02/T03.
- Basis: the direct one-dimensional nearest/range signatures remain ordinary cellular-automaton invocations (`BOOK:11037,11056,11060`); totalistic `CAStep` computes the complete next array from rotations of one input array and its sum-table rule (`BOOK:11902,11904,11908`); and the Notes place general and totalistic rules in one convolution framework with different weight descriptions (`BOOK:11914,11916`).
- Consequence: fixed support, `AllSites`, one old-snapshot finite stencil, typed same-site writes, atomic parallel commit, deterministic successor, support realization, and trace semantics remain the T01/T02 CA preset. T03 changes only the closed rule-input quotient/table; general `r` parameterizes read geometry and table validation. T03/T04/T05 presets must return this ordinary shared spec, with no `totalistic` branch, second executor, or new UPDATE policy.

### D118 — Totalistic presets, restrictions, properties, and siblings retain separate ownership

- Status: ACTIVE T03/T04/T05/T06/T07 and aggregate-sibling boundary.
- Basis: the same totalistic construction is counted for two, three, and five colors (`BOOK:1282`); the displayed three-color survey explicitly filters rules that change the white background and attributes reflection symmetry to totalistic structure (`BOOK:784`); code 420 is separately identified as additive (`BOOK:11918`); built-in signatures distinguish general, totalistic, weighted, and outer-totalistic rules (`BOOK:11037,11056,11060,11068-11072`); and binary emulation of code 1599 is an explicit encoding relation (`BOOK:7912`).
- Consequence: T04/T05 remain strict presets; T06/T07 are validated predicates/properties; additivity, seeds, galleries, palettes, and emulations remain explicit roles. Outer/semi-totalistic, histogram/count, unequal-weight/threshold, higher-dimensional, and continuous-valued forms are typed DOMAIN/NEIGHBORHOOD/RULETYPE/ALPHABET axis extensions or presets when their one-step mappings commute—not automatically new construction classes or executors.

## Rejected Shortcuts

These are globally rejected unless Principle 0 re-derivation replaces the goal itself:

- family-name rollout dispatch as the proposed universal runtime;
- a T02/multicolor family branch, duplicate fixed-lattice executor or update law, binary shifts/`&1` used as a base-`k` codec, mirrored positional indexing, fixed-width/float/JSON-number rule codes, incomplete `k^3` tables, or implicit center/background row defaults;
- deriving alphabet order from a host set or palette, treating rank as totalistic magnitude, folding T03 aggregation or T06/T07 restrictions into base T02, or making mutation schedules, reversibility/search work, behavior labels, and emulation/encoded programs native state or execution;
- a T03/totalistic/lookup rollout branch or second fixed-lattice executor; palette/host order/incidental rank used as numeric valuation; floating/tolerant averages; variable or masked arity; or histogram, nonzero-count, min/max, gate, callback, or ordered-context lookup substituted for the exact equal-weight sum quotient;
- partial/sparse sum tables, reversed sum-digit order, binary shifts/`&1`, fixed-width/float/JSON-number codes, aggregate-to-exhaustive expansion as native T03 identity, implicit center/background defaults, or quiescence/symmetry/additivity/outer/weighted/seed/gallery/emulation data folded into base totalistic execution;
- opaque packing of a machine, graph, tree, history, or whole state into a nominal cell value;
- fixed-capacity padding presented as dynamic-support semantics;
- unrestricted formula or predicate callbacks that contain the entire construction;
- hidden head state, program counters, cyclic counters, history, RNG state, or solver state;
- hidden scan cursors, host regex/rewrite engines, duplicated pattern tables, or unordered rule maps;
- bounded queues, padded/ring-buffer fronts, missing prefix-table fallbacks, or unlabeled short-to-empty normalization;
- fixed-width/saturating registers, implicit program wrap, hidden counters, scalar/prime/unary state packing, or observer-defined zero-hit execution;
- bracket/string/Polish/CA/scalar packing of expression trees, regex or host pattern execution, hidden bindings/cursors, overlapping or in-place tree rewrites, mutable-DAG alias semantics, or fixed tree capacities;
- treating `//.` normalization, Church-Rosser confluence, value equality, operator equations, or multiway branching as the documented one-pass symbolic step;
- center/point-cloud/footprint/union/raster/scalar packing of placed geometry, hidden orientation or composition order, prototype-symmetry quotienting, occurrence deduplication, overlap collision/merge/mask, painter semantics, or fixed canvases/depths/object capacities;
- host IFS/scene/complex-map callbacks, silent exact-to-float coercion, tolerance equality, undeclared precision, random chaos-game substitution, dropped pole/branch results, or limits/dimensions/parameter filters fed back as finite geometric state;
- layout/coordinate/adjacency-tensor/scalar packing of graphs, host graph or traversal callbacks, fixed node capacities, hidden roots/ports/node counters/projection, in-place rewiring, newborn firing, equal-node/fresh-descriptor deduplication, weak-component pruning, or invented random-network distributions;
- guessing sequential-network move/projection timing, inheriting parallel node-1 garbage collection without evidence, or hiding alternatives behind a convention flag;
- sampling one multiway path, replaying priority/first-match rewrites, combining several matches in one child, rescanning newborns, preserving dead parents, or accumulating old layers without explicit identity clauses;
- derivation-copy/weight state, incomplete/per-parent deduplication, chosen merged ancestry, global visited suppression, compressed graphs as live state, epsilon/empty collapse, or confluence/normal-form/algebraic quotient as exact word equality;
- multiway successor/matcher/canonicalizer callbacks, fixed word/layer/branch caps, beam/pruning/truncation as exact evolution, or silently imposing base `Union` on multiplicity-sensitive tag variants;
- repair/relaxation/fixed-point dynamics presented as a constraint system, predicate/solver/SAT callbacks in constraint data, gray/unassigned semantic values, hidden search state, or a constraint rollout family;
- one constraint witness as the whole solution set/uniqueness proof, bounded failure as global UNSAT, trusted/unscoped certificates, open-patch success as an infinite model, or `Unknown` collapsed into false;
- finite grids/padding/boundaries as native `Z^d`, wrapped-offset deduplication, structural tile equality as pointwise equality, automatic symmetry quotient, CA/ground-state/tiling/network compilation as native count constraints, or T32/T33 mechanics hidden behind flags;
- fixed-width/float/object-array packing of exact scalar arithmetic, implicit promotion/rounding/overflow/modulus, JSON numeric big integers, tolerance or cross-domain identity, temporal-history seeds, opaque arithmetic callbacks, generic affine exposure, or native cycle/fixed-point stops;
- digit strings/rasters as scalar state, blank padding as zeros, hidden sign/radix/crop, finite truncation of repeating rationals labeled exact, page width as capacity, `MultiplyMod` as a view flag, or a direct power/CA/substitution compiler presented as the requested T34 event trace;
- newest-term/scalar/trajectory/object-cell packing of an indexed numeric prefix; hidden seed history; negative-time reads; fixed-width/modular substitution; implicit missing-term defaults; surplus unverified seeds; or a lag window presented as canonical/lossless T37 state;
- recurrence callbacks/evaluator strings, computed/current/future fixed-profile indices, arbitrary recursive calls, multi-term/in-place append, old-term mutation/deduplication, periodic-value halts, figure-width horizons, closed-form event skipping, or Ulam/global-history search hidden inside the fixed-lag AST;
- conflating a mathematical prime set, ordered stream, direct primality query, consecutive sieve trace, finite raster, or arithmetic measurement; silently deleting/renaming the page-147 `1`; skipping composite stages; merging all hits with new removals; hidden survivor/stage cursors; finite capacity presented as the infinite primes; trusted prime/factor tables; unordered Goldbach or unsigned/unordered square counts substituted for the evidenced profiles; or direct `PrimeQ`/CA/analytic execution presented as the requested sieve trace;
- callbacks/eval/formula strings/host CAS objects/primitive-name reflection as mathematical-function data; argument traversal as fake time; finite float alphabets, object cells, trajectory arrays, samples, rasters, contours, sounds, histograms, spectra, or tables as the function; viewport/mesh/precision/evaluator-dependent identity; silent exact-to-float coercion; dropped pole/branch/outside-domain results; sign scans presented as complete root finding; tangent zeros or poles mislabeled as crossings; principal-`Arg` substituted for the continuous Riemann-Siegel phase; ordinary critical-line Dirichlet-series evaluation; hidden infinite-series truncation, especially the divergent `a=0` profile; or T42 substitutions hidden inside a T41 query;
- callbacks/eval/formula strings/host CAS objects/raster-decoded rules as iterated maps; finite float alphabets, digit rows, trajectory arrays, rule IDs, or NumPy objects as exact real state; orbit-prefix/history packing; trusted self-map flags; implicit float/radix/precision/rounding/fill/comparison defaults; unknown-digit invention; discontinuities treated as failures; implicit clamp/wrap/modulo; arbitrary uncertain piecewise arms; in-place vector updates; box/torus conflation; tolerance cycle halts; observer-fed evolution; finite traces/rasters treated as attractor, bifurcation, Lyapunov-limit, randomness, or exact-period proofs; analytic iterates substituted for requested events; the false arbitrary-rational-`a` repetition claim; the Anosov clause silently changed to irrational; or a T43 rollout-family branch;
- callbacks/opaque reducers/raster rules, finite float alphabets or NumPy arrays as continuous fields, whole-field scalar/vector packing, hidden periodic edges/zero padding/crops/capacities, integer or implicit-float means, hidden reduction/rounding/format semantics, normalized weights substituted for the divisor-three rule, conditional-only strict `FractionalPart` or a silently chosen boiling equality repair, implicit clamp/modulo, in-place/asynchronous or partial field commits, history/time/parameter/draw/difference state pollution, gallery-as-run, observer-fed execution, cycle/background/class/localized halts, numerical error disguised as stochasticity, unreplayable/global RNG, finite PRNG samples called exact continuum samples, additive/strict or probabilistic/noisy conflation, page-325 silent clipping, finite-difference PDE identity, or a T44 rollout-family branch;
- finite CA/T44 fields, float alphabets, NumPy arrays, meshes, samples, interpolants, or rasters presented as a mathematical PDE field/solution set; a `pde` rollout branch, zero-dimensional packing, fake native step, or solver time steps called continuous evolution; callbacks, formula strings, host CAS objects, opaque derivative predicates, or trusted solver booleans as differential data;
- conflating an equation with one problem, candidate, solution set, witness, derived flow, integrator, `NDSolve` object, sample, or gallery panel; hidden initial/boundary data, implicit time variables, blind universal seed rules, order-only well-posedness guesses, constructor-hidden equation-class/locus/admissibility heuristics, or unsupported weak/distributional concepts;
- one witness as uniqueness or a complete solution set, two witnesses as enumeration, solver failure/bounded search as no solution, residual tolerance as exact satisfaction, Courant/stability as convergence or correctness, refinement appearance as proof, approximate conservation as invariance, or a raster as genuine PDE complexity;
- hidden truncation/periodicity/mesh/halo/stencil/order/condition-lowering/integrator/adaptivity/precision/rounding/tolerance/backend/resource choices; finite difference, method of lines, pseudospectral methods, ODE reductions, iterated maps, CA continuum limits, or emulators presented as native PDE identity; source defects or missing settings silently repaired with textbook defaults;
- compiling another construction to a CA merely to claim native coverage;
- treating canonical `[t,x,y,z]` encoding or visualization coordinates as topology;
- conflating a constraint with a solver, a PDE with a discretization/integrator, or a stochastic law with an RNG implementation;
- weakening tests, adding flags/shims/fallbacks, or duplicating shared primitives under family-specific names.

## Architecture-Reclosed Integration Result

- `architecture-audit.md` audits D000-D118 individually, assigns one primary class to each decision, and gives the smallest reusable base plus invariants and dependent-stage disposition.
- Every evidenced transition/rewrite construction reuses one branch-free `SimpleProgram` runner. Differences are typed DOMAIN/topology, ALPHABET/value schema, FRONTIER, NEIGHBORHOOD, RULE-write, UPDATE-policy, seed, invariant, outcome, and representation choices—not catalog-family executors.
- T09 and T12 use the commuting composite-label representations `Plain(bit) | Active(bit)` and `Plain(symbol) | Head(q,symbol)`. T19 uses an explicit marker/product role. None requires `SingleControl` or `TransitionControl`.
- Ordered block/splice, tree, bag, graph, endpoint, subset/marker, snapshot-field, and finite-successor-set commits are implementations or presets of the UPDATE axis. Their counterexamples justify those typed policies, not ordinal top-level laws or construction executors.
- T30's native configuration is one word and UPDATE returns `Successors[Word]`; a layer is the explicit finite-powerset lift and derivation witnesses remain separate from exact configuration deduplication.
- T31 model sets, T41 uniterated function definitions, and T45 differential relations without a posed evolution are the three evidenced declarative nonfits. No fake seed/frontier/update is invented. A well-posed derived evolution may return to the common runner through an explicit relation.
- The corrected stage addenda and Goal 2 handoffs supersede the historical integration entries below. T03/T04 remain reopened solely for bounded evidence-asset repairs; T06 resumes after this architecture closure.

## Historical Integration Log (Superseded by Architecture Audit)

The entries below preserve what each evidence stage originally concluded. Their search closure, excerpts, fixtures, and source repairs remain evidence; their class names, ordinal update-law inventory, and executor implications are not current architecture.

- `1-FOUNDATION` — COMPLETE: established the catalog join, source/runtime/test baseline, fit labels, unresolved semantic dimensions, and global rejection criteria. No type evidence or construction primitive was declared complete.
- `2-T01-ELEMENTARY` — COMPLETE: validated fixed-lattice synchronous assignment, explicit Wolfram pattern codec, and the separation of native support from finite realization and trace. Found current exhaustive cardinality (`R=4` instead of 256), mirrored asymmetric bit order, and non-executable generic lookup. Added the implementation/conformance handoff without an elementary rollout branch. No prior stage reopened.
- `3-T09-MOBILE` — COMPLETE: rederived frontier as source selection; added visible single-position control, typed compound assignment/relocation effects, atomic update, and control-preserving traces. Resolved physical read order against executable Notes and the rule image; recorded exhaustive `{35,57}` and 65,536-rule oracles. T01 was re-audited but not reopened because its source/target coincidence preserves its result.
- `4-T12-TURING` — COMPLETE: refined control to a payload-bearing form, added self-only control/value product reads, total default-symbol tapes, and explicit terminal/stop/error distinctions. Reconstructed `(2sk)^(sk)` tables, repaired the OCR-damaged numeric codec with independent guards, and recorded exact table/trajectory tests. T09 remains valid as unit-payload control; no stage reopened.
- `5-T13-PARALLEL-SUBSTITUTION` — COMPLETE: preserved the generic source/read/rule/update shell but split `UPDATE` into honest fixed-support and ordered structural members. Added explicit discrete ordered support, `AllOccurrences`, total `Sigma->Sigma+` tables, typed occurrence replacement, source-order child construction, ragged/lineage traces, and explicit infinite realization pressure. Empty/contextual/sequential/stochastic/scheduled/geometric variants remain separate. T01/T09/T12 were re-audited and remain valid; no stage reopened.
- `6-T16-SEQUENTIAL-SUBSTITUTION` — COMPLETE: refined source selection with explicit program-owned applicability, added rule-major/leftmost `FirstApplicableMatch`, exact matched-span reads, typed single-interval replacement/splice, and `NoMatch` termination. Reused T13 ordered support/provenance but kept its all-occurrence commit distinct. Empty RHS remains an evidence boundary for T15. T01/T09/T12/T13 were re-audited and remain valid; no stage reopened.
- `7-T17-TAG` — COMPLETE: added separate prefix read/delete roles, complete epsilon-valued prefix tables, one queue-head source, atomic prefix-consume/tail-append update, and retained-residue `InsufficientPrefix` termination with an explicit Notes history projection. Reused finite T13 ordered state/provenance, typed outcomes, and a broadened private ordered-edit carrier, but kept all T13/T16 public validators and commits unchanged. Wolfram/Post/Wang, case (a), case (c), bounded-count, and T13-checkpoint oracles close the handoff. T01/T09/T12/T13/T16 remain valid; no stage reopened.
- `8-T19-REGISTER` — COMPLETE: added finite named banks over exact naturals, typed program-address control, program-coupled instruction/operand access, closed branch-specific results, and event-free past-end quiescence. Reused T09/T12 `SingleControl`, typed effects, atomic update, structured traces, and outcome distinctions without spatial/tape reinterpretation. Exact counts, five/eight-instruction trajectories, zero-hit recurrence, repaired 1,280-step witness, square-root exit, and arbitrary-precision oracles close the handoff. T01/T09/T12/T13/T16/T17 remain valid; no stage reopened.
- `9-T20-SYMBOLIC` — COMPLETE: added finite ordered expression trees, head/argument paths, closed structural patterns/templates, whole-subtree bindings, functional outermost prefix-free selection, typed subtree results, and a fifth atomic update law. Exact t0-t5, overlap/disjoint/newborn, invariant/fixed-time, Catalan-count, S/K deletion/duplication, priority, identity, no-match, codec, and provenance oracles close the handoff. Reused T13 lineage and T16 program coupling only at the responsibility level; their public commits remain distinct. T01/T09/T12/T13/T16/T17/T19 remain valid; no stage reopened.
- `10-T27-GEOMETRIC` — COMPLETE: added finite multiplicity-preserving bags of prototype occurrences with full affine poses, exact/declared scalar profiles, parent-local child templates and `P∘C`, permutation-invariant all-occurrence sources, self-only full-pose reads, typed geometric results, and a sixth atomic bag-replacement law. Exact page-189/page-190 centers/counts, overlap, same-center/same-footprint/different-frame, composition-order, equivariance, duplicate-slot, permutation, and provenance oracles close the handoff. Center lists, rasters, unions, limits, dimensions, and Mandelbrot filters remain downstream; nonlinear branches use a distinct closed extended-complex point profile. T13 lineage composes but ordered concatenation does not; T01/T09/T12/T13/T16/T17/T19/T20 remain valid and no stage reopened.
- `11-T29-NETWORK` — COMPLETE: added finite rooted two-port graphs, alpha-renamable vertex identity, old-snapshot port-path/exact-reach reads, closed direct/fresh result data, collision-free event births, and `ParallelRerouteCreateProject` as a seventh update law. Uniform periods/collapse, singleton growth, depth-one `1296`, five depth-two tables/count anchors, canonical BFS equality, signature witnesses, and frozen/projection/freshness/alias/provenance adversaries close the parallel handoff. Layout/dimension/fixed-network/constraint/causal/multiway/grammar variants remain distinct. Sequential pruning is evidenced but its anchor/order and move timing are source-underdetermined, so its executor is explicitly deferred. No prior stage reopened.
- `12-T30-MULTIWAY` — COMPLETE: added finite exact word-set layers, unordered literal relations, every-overlapping-match selection, one-splice branch results, and `DistinctBranchMerge` as an eighth update law. Equal children merge across positions/rules/parents while full witnesses and dead parents remain trace data. Page-219/page-220, page-206 extinction, official cross-parent merge, page-224 folded-network, sorted-vector, overlap/diamond/recurrence/epsilon/reconstruction oracles close the handoff. Layer recurrence remains separate from compressed graphs and global visited state. Literal semi-Thue/grammar restrictions compose; tag/cyclic/pattern/block/numeric/control variants remain separate. T13/T16/T29 stay valid; no prior stage reopened.
- `13-T31-CONSTRAINTS` — COMPLETE: established the first categorical split from transition execution. Added total-lattice local count relations, closed center-conditioned histograms, axis-aligned periodic/open/window scopes, exact local verification, pointwise periodic equivalence, replayable finite obstructions, and separate scoped solver outcomes. The `0011` de Bruijn cycle, permissive run profile, exact `5x5` tile/five-violation perturbation, full 25-profile gallery, 1D/page-227 obstructions, scope/Unknown/alias/equality tests close the handoff. T32 oriented templates and T33 existential occurrences stay distinct; CA/tiling/ground-state/network reductions and solver heuristics remain external. No prior transition stage reopened.
- `14-T34-ARITHMETIC` — COMPLETE: added a domain-tagged unary exact scalar carrier, normalized integer/rational values and string codecs, closed fixed-add/fixed-multiply programs, `UniqueScalar` reads, and typed scalar assignment through the existing atomic effects update. Exact page-117..122 add/power/rational/fraction/crop/overflow oracles close the handoff. Digit/size/fraction observers, residue-ring `MultiplyMod`, random-access formulas, CA/substitution compilers, and numerical contexts remain explicitly separate. T35/T36/T37/T38/T43 boundaries are preserved; no prior stage reopened and no ninth update law was added.
- `15-T37-RECURSIVE` — COMPLETE: added consecutive domain-tagged exact numeric prefixes, explicit index origins, minimal fresh seeds and replay-verified checkpoints, normalized affine fixed-lag programs, a named closed factorial-capable expression extension, `NextSequenceTerm`/old-prefix dependency reads, typed `AppendTerm`, and `AppendOnlySequenceUpdate` as the ninth law. Exact six-row page-143 horizons/terms, the (e)/(f) source-erratum guard, Fibonacci overflow, Lucas/Perrin/factorial, append cardinality, checkpoint, and non-injective lag-window oracles close the handoff. Compact seed-plus-event traces reconstruct nested prefix states; closed forms/windows remain evaluators. Current AR2 is an explicit modular relation, T38 computed indices remain separate, and T37 defers Ulam until the following T39 composition audit. No prior stage reopened.
- `16-T39-FILTERS` — COMPLETE: split pure integer filters/streams and pointwise measurements from the strict consecutive-divisor sieve; added explicit finite/intensional domains, stage cursor, all-hit/new-removal reads, typed subset results, and `MonotoneFilterUpdate` as the tenth law. Exact page-147 masks/source inconsistency, six page-148 observers, five page-150 measurements, OCR/normalization repairs, finite certification, and Ulam first-accepted/T37-append composition close the handoff. Exact semantic assertions, seven raster hashes, Markdown fences, diff checks, and 102 repository tests pass; no prior stage reopened.
- `17-T41-FUNCTIONS` — COMPLETE: established immutable unary mathematical-function definitions and pure evaluation/observation records as a non-transition category; added closed exact expression/primitive/domain/branch semantics, typed point/sample/zero/crossing/extremum results, ordered structural identity versus certified equivalence, and explicit finite-sum/infinite-series boundaries without an eleventh update law. Eighteen evidence groups, four strict/eight Notes raster identities, exact two-term period/root formulas, endpoint/multiplicity adversaries, the repaired ODE profile, page-162 T41/T42 seam, and Riemann-Siegel continuation/phase/value/numerical-zero anchors close the handoff. T20/T27/T31/T34/T39 responsibilities compose without reopening their public semantics; T43/T44/T45 remain distinct. Exact/declared-precision assertions, twelve hashes, Markdown fences, diff checks, and 102 repository tests pass; no prior stage reopened.
- `18-T43-ITERATED-MAPS` — COMPLETE: established one domain-tagged ideal real scalar plus distinct fixed-realization state under an immutable closed self-map/realization contract, complete old-value reads, typed `MapAssignment`, and reuse of the fixed-effects atomic update without an eleventh law. Exact, certified, tracked-significance, and fixed-rounded feedback profiles are distinct; `h` events produce `h+1` states; fixed points/cycles never halt native execution. Nineteen evidence groups, eight strict/three Notes assets, exact-rational page-165 and declared-180-decimal page-168/page-170 cell matches, precision-collapse/period anchors, logistic/vector profiles, and rational-`a`/matrix/source repairs close the handoff. T34 assignment and T41 syntax compose; T37 prefixes, T44 fields, T45 flows, digit/sensitivity/Lyapunov/attractor/parameter observers, and fast-forward methods remain distinct. Exact/declared-precision assertions, eleven hashes, Markdown fences, diff checks, and 102 repository tests pass; no prior stage reopened.
- `19-T44-CONTINUOUS-CA` — COMPLETE: established a total `[0,1]` field on fixed ordered 1D support, synchronous left/self/right reads, a closed exact affine aggregate followed by a closed scalar map, typed same-site assignments, and reuse of T01 atomic fixed-effects commit without an eleventh update law. Strict integer-line support remains inferential; Notes ring, finite-segment exterior, causal work, and raster crop have separate identities. Exact field state, certified/tracked computation records, represented feedback, and stochastic draws stay distinct. Twenty-five evidence groups, 17 included assets plus the page-339 exclusion, exact semantic rows, and page-172/173/174/175/Notes raster oracles close the handoff. D096-D102 preserve weighted/additive/coupled/boiling/noisy/probabilistic/block/PDE boundaries. Search, semantic, metadata, raster, source, Markdown, diff, and 102 repository tests pass; no prior stage reopened.
- `20-T45-PDE` — COMPLETE: established immutable scalar/complex/fixed-vector differential equations and classical continuous-region/side-data problems whose denotation is a solution set, with no native source, update, successor, halt, or eleventh law. Closed multivariate binders, derivative multi-indices, fixed matrices, candidate/trace expressions, scoped proof-strength-preserving queries, versioned class/locus/admissibility claims, and explicit numerical-relation records preserve the equation/problem/witness/realization/sample/view splits. Twenty-eight evidence groups, a 27-query zero-remainder oracle, 23 included assets plus the Chapter 5 title-art exclusion, exact heat/wave/nonlinear/background/period/finite-difference semantic checks, metadata hashes, and the heat raster oracle close the handoff. D103-D110 preserve T31/T41/T44 reuse, the ODE/IVP/finite-difference boundaries, and Classical-only v1 scope; source, Markdown, diff, and 102 repository tests pass; no prior stage reopened.
- `21-T02-MULTICOLOR-CA` — COMPLETE: established strict `k>=3` nearest-neighbor CA as the finite-alphabet/table parameterization of T01, with one complete ordered `k^3` table and the arbitrary-precision Wolfram positional base-`k` codec. The exact `3^27` count, codes `921408`/`5407067979`, nonbinary/asymmetric/evolving-background adversaries, and source trajectory/raster oracles expose the current mirrored binary-only/fixed-width runtime defects. D111-D114 keep table identity separate from codecs, properties, provenance, analyzers, emulation, numeric aggregation, and palettes; T03/T06/T07 remain separate, no prior stage reopened, and no executor or update law was added.
- `22-T03-TOTALISTIC-CA` — REOPENED again during the T04/T06 repair: T04's downstream-comparator audit proved that inherited page-263 raster `BOOK:2928` belongs to the two-dimensional totalistic gallery but is absent from T03's 313-candidate/119-asset closure. The bounded one-control source/asset/reverse repair and independent re-review are active. Explicit valuation, exact sum/table/codec, the shared executor, and D115-D118 remain unchanged.
- `23-T04-THREECOLOR-TOTALISTIC` — REOPENED during T06: retained captions `BOOK:17431` and `BOOK:2922` explicitly govern omitted rasters `BOOK:17433` and `BOOK:2924`, invalidating the prior 243-candidate/72-asset exhaustion claim. The bounded source/asset/metadata/reverse repair and independent re-review are active. The strict `k=3,r=1,A=(0,1,2),nu(i)=i` T03-preset identity, executor result, and D115-D118 remain unchanged.
- `24-T05-HIGHERCOLOR-TOTALISTIC` — COMPLETE: the exact 11-query/142-lexical-line manifest plus five governed follows and 25 assets closes 172 candidates with zero remainder; 12 evidence groups close 47 provenance lines/47 fragments/40 quote lines, and assets close at 5 included/13 relation-only/7 excluded. Exact `k>=4,r=1` canonical preset, `M=3k-2`, arbitrary-precision `R=k^M`, code-`1004600`, label-corpus, snapshot, and boundary oracles prove resolution to unchanged generic T03. T03's discovered source omission was independently repaired and reclosed; no stage remains reopened. Five embedded checks, independent review, fences, diff checks, and 102 tests pass. D118 is sharpened; no D119, executor, or update law was added.

## Open Architecture Questions

1. Which remaining catalog rows are constructions versus restrictions, presets, seed classes, observables, or solver-defined systems? T01 is the fixed-lattice construction; T02 parameterizes its alphabet/ordered table; T03 adds the exact numeric-sum rule quotient without a second executor; T04/T05 are color-count presets, T06/T07 table/property restrictions, and T08 a seed-class hypothesis requiring its own evidence.
2. T02/T03 confirm that T01's `AllSites`/old-read/typed-assignment/atomic-update protocol survives unchanged under finite-alphabet ordered-table and exact-sum-table rule descriptions. The source/read/result/update protocol remains substantive through T30 and the T34/T37/T39/T43/T44 transition profiles but explicitly does not cover T31, pure T39 filters/measurements, T41, or T45. T45 resolves derivatives and PDE solution/operator categories as immutable differential definitions/problems plus scoped query/results, with no native update; T41 values and closed syntax compose only through new bound multivariate/differential nodes. T42 may consume a T41 result without importing evaluator or substitution state. Distribution-valued constructions still require independent evidence.
3. T30 establishes that base branch occurrences are provenance, while exact child words form semantic set state and recur independently of a compressed graph. Which later stochastic/quantum/multiway-tag systems instead make weights or derivation multiplicity semantic must be separately evidenced.
4. T31 proves that a single witness, an orbit representative, and a mathematical solution set are distinct. T45 now reuses T31's scoped query, witness, certificate, and `Unknown`/resource discipline while adding continuous-region, differential-expression, side-data, and classical-regularity carriers; equation, problem, candidate, witness, realization, sample, and view remain distinct. How T32/T33 template relations reuse that infrastructure without collapsing their own carriers remains open.
5. Can T14/T15 reuse the epsilon-capable private ordered-span kernel without erasing contextual eligibility or their own deletion laws? T17 proves reuse is safe only behind a distinct public queue validator/update.
6. T02/T03 resolve finite-CA rule-code big integers: the typed structural ordered-context or exact-sum table is primary, the case-domain tag prevents their conflation, and any numeric code uses tagged arbitrary-precision decimal-string serialization rather than JSON-number identity. What lossless record encoding preserves the remaining non-rank-0..3 semantic addresses and categories—including exact scalar/prefix/sieve/map/continuous-field transitions, represented-number/field realizations, stochastic draw records, constraint records, immutable function specs, and reproducible function/map-query results—while keeping mathematical identity, equivalence/conjugacy proofs, certificates, diagnostics, and renderings distinct across JSON consumers?
7. T02 confirms explicit alphabet order and radius-one selector responsibilities; T03 confirms explicit numeric valuation, fixed arity, and an exact equal-weight sum descriptor while rejecting the current broad `TOTALISTIC` conflation with histograms/counts. Both reject palette/host-derived meanings, binary-only decoding, fixed-width rule IDs, and family dispatch; seed/background and raw traces survive only with T01's program/run/view separation. Which remaining selector, alphabet, rule-summary, seed, RNG, and raw-result components survive later evidence without semantic reinterpretation?
8. Which current tests are canonical-construction evidence and which merely preserve incidental Phase 1 behavior? T01/T02/T03 show that geometry, binary self-parity, scalar/batch parity, and pixels alone do not prove rule semantics; asymmetric positional tables, equal-sum/different-histogram contexts, nonbinary outputs, sum-digit order, radius variation, evolving backgrounds, old-snapshot adversaries, arbitrary-precision round trips, and source trajectories are canonical conformance evidence.
9. T45 resolves the semantic sharing boundary: T41/T43/T44/T45 may share tagged exact/declared numeric values, closed primitive/domain/branch syntax, generic scoped certificate envelopes, errors, and codecs. T45 alone adds bound multivariate fields, differential operators, equations/problems, side-data claims, and explicit solver/discretization relations; T43/T44 feedback transitions, T45 solver work, samples, diagnostics, and views retain separate identities. Synthesis must still select the concrete versioned registry and backend adapters without weakening those boundaries.
10. Which exact-real/interval backend can Goal 2 support honestly for named transcendental states such as `Pi/4`, exact piecewise comparison, and replayable invariant certificates? Until synthesis selects one, executable exact profiles must expose typed unsupported cases rather than silently fall back to machine arithmetic.
