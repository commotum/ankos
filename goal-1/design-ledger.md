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

## Completed Construction Records

| Type | State | Active/read/rule | Result/update | Successor and boundaries | Goal 2 obligation |
|---|---|---|---|---|---|
| T01 Elementary CA | Fixed ordered 1D lattice + total Boolean field; no control | `AllSites`; ordered old `(left,self,right)`; arbitrary 8-entry table with `index=4l+2c+r` | Typed same-site `Assign`; atomic parallel commit | One deterministic successor, no halt; native `Z` or explicit finite cycle/segment/causal-window realization; seed independent | Generic ordered lookup + parallel assignment + support/realization/trace split; all 256 rules and asymmetric trajectory oracle; no ECA branch |
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
| T44 Continuous Cellular Automata | Fixed ordered 1D lattice + total exact or explicitly represented real field, strict range `[0,1]`; no control/history; integer-line and explicit finite-cycle/segment realizations | `AllSites`; ordered old `(left,self,right)`; closed exact affine neighborhood aggregate with divisor followed by a closed scalar map and replayable composite closure | Typed same-site `Assign`; T01 atomic parallel fixed-field commit, so no eleventh update law; stochastic siblings resolve explicit draws before the same commit | One deterministic strict successor including unchanged fields; `h` events give `h+1` states; no native halt; native topology not explicit, Notes ring/causal work/crop distinct; local failure commits nothing | Total continuous fields, affine aggregate/map rules, exact/certified/tracked/represented field feedback, field runs/analysis/views/stochastic draws/presets, strict/supporting asset oracles; T01/T41/T43 reuse with no float alphabet/callback/field pack/family branch |

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
| Support/topology | Fixed fields including total Boolean/symbol/real-valued lattice fields, one scalar slot including a domain-tagged real interval, ordered sequences and indexed numeric prefixes, ordered finite/intensional integer domains, named banks, rooted trees, affine bags, rooted graphs, exact word sets, declarative model sets, and explicit real boxes/tori are support members; declared real/complex function domains can instead be definition scopes | PROVISIONAL lattice/scalar/real-interval/box/torus/sequence/prefix/integer-domain/bank/tree/bag/graph/word-set/model-set members plus function-definition domains; other continuous/general topology UNRESOLVED | T01, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30, T31, T34, T37, T39, T41, T43, T44 |
| Values/alphabet | Explicit finite values; epsilon words; exact naturals/signed integers/reduced rationals; named/algebraic/certified/declared-precision real/complex values and enclosures; represented finite-format values; total exact/represented continuous fields; fixed numeric vectors; indexed prefixes/candidate partitions; pattern/geometry/graph values; exact sets; histograms and periodic fields | PROVISIONAL finite/infinite discrete, exact/declared/represented numeric and field, function/map value, prefix/filter, affine/point/vector, graph-reference, set-lifted, and constraint values | T01, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30, T31, T34, T37, T39, T41, T43, T44 |
| Control | Visible Markov control includes `SingleControl(key,position,payload)` over typed addresses and construction-owned cursors such as the next sieve divisor; unit payload for T09/T19, finite head-state payload for T12 | PROVISIONAL single-control and explicit scalar-cursor members; multiple/structural control UNRESOLVED; absent from pure T41 definitions/queries and T43/T44 numeric transitions | T09, T12, T19, T39; absent T01/T13/T16/T17/T20/T27/T29-parallel/T30/T31/T34/T37/T41/T43/T44 |
| Active loci | Firing/source selectors include sites, a unique scalar, the next sequence term or sieve stage, control loci, ordered/bag occurrences, network nodes, program-coupled flat/tree matches, queue prefixes, instructions, and every literal match across every word in a layer | PROVISIONAL fixed/scalar/prefix-end/stage/control/sequence/bag/graph/interval/queue/code/tree/multiway-match sources; not applicable to pure specifications/queries | T01, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30, T34, T37, T39, T43, T44; absent T31/T41 |
| Reads/access | Ordered topology values and continuous neighborhood triples, the complete current scalar or old vector tuple, fixed indexed old-prefix lags, complete explicit prefix contexts, proper-multiple survivor partitions, control payload, self values, spans/prefixes, operands, tree bindings, geometric poses, graph path/signatures, or exact matched parent intervals; read and mutation coverage may differ | PROVISIONAL for transition profiles; mathematical function evaluation remains a distinct pure query | T01, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30, T34, T37, T39, T43, T44; distinct T41 |
| Rule choice | Total tables/morphisms, ordered rewrite programs, closed instructions/templates/ASTs, topology tables, unordered finite literal relations, closed constant arithmetic, normalized fixed-lag affine programs, closed integer predicate/measurement plus schedules, a closed self-map AST, or a closed affine neighborhood aggregate followed by a scalar AST with replayable composite contract; no implicit defaults/callbacks | PROVISIONAL transition-program members; closed mathematical expressions are definition data for T41 and feedback programs under explicit T43/T44 contracts | T01, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30, T34, T37, T39, T43, T44; distinct T41 |
| Rule result | Typed members include assignment/control effects, scalar/map/continuous-field assignments, numeric term appends, candidate-subset removals, word/queue/tree/bag/graph replacements, instruction branches, and one literal interval replacement per multiway witness | PROVISIONAL result sum; never a universal category; T41 evaluation/zero results are pure query records | T01, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30, T34, T37, T39, T43, T44; distinct T41 |
| Commit/update | Explicit siblings: fixed effects, ordered replacement, one splice, queue edit, prefix-free tree replacement, bag replacement, rooted graph reroute/create/project, exact multiway branch union, numeric-prefix append, and monotone candidate-subset removal | PROVISIONAL ten-member transition family; T34/T43/T44 reuse fixed assignment, T37 adds append, T39 adds removal; T31, pure T39 specs, and T41 are categorically outside | T01, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30, T34, T37, T39, T43, T44; not applicable T31/pure T39/T41 |
| Successors | Execution may yield one advanced successor—including unchanged scalar/field events and a complete set-valued macro successor—typed quiescence/reference stutter, retained zero-successor terminal outcome, or typed no-commit partial/evaluation failure | PROVISIONAL transition outcomes; T31/T41 pure query results and pure T39 filter/measurement results are distinct; derivatives UNRESOLVED | T01, T12, T16, T17, T19, T20, T27, T29, T30, T34, T37, T39, T43, T44; distinct T31/T41 |
| Halting/invalidity | Base continuation, terminal/no-match/prefix outcomes, quiescence, explicit exit, all-dead-to-empty advancement, empty-layer stutter, undefined/escape/evaluation failure, observers, certificates, projection, validation, resource, and rendering cutoffs are distinct | PROVISIONAL outcome model; T43/T44 strict fixed/cycle/convergence/background repetition has no native halt; query completeness/partiality/resources and render horizons are not native halts | T12, T16, T17, T19, T20, T27, T29, T30, T31, T34, T37, T39, T41, T43, T44 |
| Trace encoding | Transition snapshots/events remain distinct from pure filter/measurement/function results, verified models, constraint/function/map/field-analysis records/certificates, numerical-realization relations, solver diagnostics, algorithm work traces, stochastic draw records, and downstream renderings | PROVISIONAL transition traces plus explicit non-trace records; `h` T43/T44 events produce `h+1` states; global schema UNRESOLVED | T01, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30, T31, T34, T37, T39, T41, T43, T44 |
| Constraint/solution | Closed local relations denote mathematical model sets; periodic/open/window presentations have explicit scopes; exact verification differs from search and solution enumeration | ACTIVE category split; T32/T33 and other constraint carriers must re-audit relation syntax | T31 |
| Function/denotation | Closed unary mathematical expressions declare one argument, parameters, real/complex domain, scalar/fixed-vector codomain, primitive versions, partiality, and branches; point/sample/zero/crossing queries are separate; compatible syntax can sit inside a map contract | ACTIVE pure T41 category and reusable syntax responsibility; structural identity, certified functional equivalence, map relation, and observation equality remain distinct | T41, T43 |
| Map/feedback | A closed self-map over an explicit state space repeatedly feeds one result into atomic state assignment; strict totality/invariance, partiality, and numerical realization are explicit | ACTIVE T43 transition category; ideal exact, certified computation, tracked significance, and fixed-rounded feedback are distinct profiles/relations | T43 |
| Field/feedback | A closed affine neighborhood aggregate followed by a closed scalar expression updates a total real field from one old snapshot; exact/certified/tracked/fixed-rounded/stochastic profiles and support/work/crop scopes remain explicit | ACTIVE T44 transition category; reuses fixed assignment without a new update law and keeps additive/coupled/noisy/block/PDE siblings typed | T44 |
| Solver/numerics | Exact numeric evaluation is semantic where declared; approximate/certified queries carry full context; fixed-rounded feedback changes T43's effective map and T44's effective field transition; constraint/function/map/field solvers use separate scoped results/certificates; evaluators and fast-forward methods never replace definitions or requested traces | PROVISIONAL exact/declared/represented numeric, evaluator, query-result, and solver boundaries | T27, T31, T34, T37, T39, T41, T43, T44 |

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

### D004 — First validated executor algebra is fixed-lattice synchronous assignment

- Status: PROVISIONAL; evidenced by T01 only.
- Basis: `goal-1/2-T01-ELEMENTARY.md`, especially `BOOK:418-430`, `850-854`, and `10984-10992`.
- Shape: `AllSites -> ordered old-snapshot read -> exhaustive table -> Assign -> ParallelUpdate`.
- Consequence: this is a substantive shared transition protocol candidate, not a universal executor conclusion. Move, replacement, structural mutation, branching, constraints, derivatives, and observations must still challenge it.

### D005 — Separate semantic support, computation realization, and trace extent

- Status: ACTIVE.
- Basis: T01's infinite local line (`BOOK:8832`, `11250`), finite cyclic programs (`:3026`, `10986`), exact causal width (`:11124`), and Principles 6–8/12.
- Consequence: native `Z`, a finite cycle/segment or causal-halo work region, and emitted `[t,x,0,0]` coordinates are three inspectable layers. Current `Dynamics.shape` cannot silently represent all three.

### D006 — Ordered reads and rule-code significance are separate validated objects

- Status: ACTIVE.
- Basis: T01 exact rule index `right + 2*self + 4*left` (`BOOK:10988`) versus current `_channel_state` low-significance-first encoding (`src/ca/rollout.py:742-760`).
- Consequence: a neighborhood owns semantic read order; an exhaustive codec owns digit significance and validates it against arity/alphabet. Family-local selector reversal is rejected as a shim.

### D007 — Same-site assignment is an explicit result member

- Status: PROVISIONAL; evidenced by T01 only.
- Basis: the rule chooses the center cell's next color (`BOOK:428-430`) and all such choices commit from old values in parallel (`:10984`).
- Consequence: use a typed `Assign(value)`-equivalent with explicit parallel update. Do not generalize bare returned values into universal mutation semantics.

### D008 — Elementary identity is a strict preset over generic data semantics

- Status: PROVISIONAL pending Goal 2 synthesis.
- Basis: `k=2,r=1` identity (`BOOK:11050`), arbitrary eight-case table (`:712-720`), and Principles 9–10.
- Consequence: a discoverable `elementary(n)` entry may pin Boolean alphabet, fixed 1D support, all sites, ordered radius-one reads, exhaustive table, and parallel assignment, but cannot select a separate executor or embed a seed/boundary.

### D009 — Frontier selects firing sources, not writable targets

- Status: ACTIVE.
- Basis: T09's rule applies at the old active cell, writes that source, and independently moves control to a neighbor (`BOOK:854-862`, `11957-11970`).
- Consequence: `FRONTIER.select(state)` returns rule-firing/source loci. `RULE` results name effect targets and `UPDATE` applies them. T01 remains valid because each source and assignment target coincide; current writable-next-coordinate frontier wording must migrate.

### D010 — Visible control is a first-class state component

- Status: PROVISIONAL; evidenced by T09.
- Basis: Notes state `{list,n}` explicitly separates cell values from active position (`BOOK:11957`) and random initial values still require a definite active location (`:14275`).
- Consequence: state snapshots, seeds, equality, serialization, batching, and traces must preserve typed control. Extra colors, metadata, executor locals, or display marks cannot stand in for it.

### D011 — Transition results may be atomic compounds of typed effects

- Status: PROVISIONAL; evidenced by T01 and T09.
- Basis: each T09 table entry returns new active-cell value plus displacement, and `MAStep` returns the changed field and relocated control together (`BOOK:11960-11970`); T12 also changes control payload (`BOOK:12014-12023`).
- Consequence: the candidate protocol supports at least `Assign` and payload-bearing `TransitionControl`, with atomic application and unchanged-value preservation. T09 uses a unit payload. This does not yet justify insert/delete/rewire/branch semantics.

### D012 — Ordered read codec is shared across T01 and T09

- Status: ACTIVE for these two constructions.
- Basis: T09 executable `Take[n-1..n+1]` and the rule figure establish physical `[left,self,right]`; its `{35,57}` bytes use `index=4L+2C+R`, the same ordering established by T01.
- Consequence: no mobile-specific permutation is required. The shared current low-significance-first runtime codec remains a defect, and asymmetric physical `100`/`011` cases are required tests.

### D013 — Full traces preserve control before observations compress them

- Status: ACTIVE for controlled systems.
- Basis: the standard mobile trace includes both cell colors and active-position dots (`BOOK:5840`); record-extrema compression (`:878`) and causal networks derived from position history (`:16388`) are later transformations.
- Consequence: raw state traces cannot be only dense value arrays. Frame compression, causal graph construction, and visualization are downstream and never feed execution.

### D014 — Single control carries an explicit finite payload

- Status: PROVISIONAL; evidenced by T09/T12.
- Basis: Turing state explicitly separates head state, tape values, and head position (`BOOK:12014`), while each transition changes both state and position (`:12016-12023`).
- Consequence: use `SingleControl(key,position,payload)` and atomic `TransitionControl(expected_from,to,next_payload)`. T09 is the unit-payload specialization; no separate hidden head-state channel is allowed.

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
- Consequence: preserve a shared source/read/rule/update orchestration, but give it at least sibling `AtomicEffectsUpdate` and `ParallelReplaceConcat` implementations selected by typed spec/result contracts. `Assign` is not stretched into insertion, and no T13/family rollout branch is added.

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
- Consequence: refine the source-first shell to `SOURCE.select(state, program.applicability)`. `FirstApplicableMatch` and result lookup consume one authoritative immutable `OrderedLiteralRewriteProgram`; no second LHS table, matcher callback, or claim of independent frontier/rule composition is allowed. T01/T09/T12/T13 remain program-independent special cases and are not reopened.

### D023 — Single interval splice is a distinct ordered update law

- Status: ACTIVE for T16.
- Basis: exactly one matched block is replaced per step while its prefix/suffix remain in order (`BOOK:1062-1068`, `2358`, `5936-5940`). T13 instead consumes every old occurrence and concatenates all child blocks.
- Consequence: add `ReplaceInterval` plus `SingleSpliceUpdate` as a sibling of `ParallelReplaceConcat` and fixed-support atomic effects. Both ordered updates may share a private `ApplyOrderedSpans` kernel only after their public policies validate, respectively, complete singleton coverage or exactly one arbitrary span; the shared kernel never erases those laws.

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

### D027 — Prefix consumption plus remote tail append is a distinct atomic update law

- Status: ACTIVE for T17.
- Basis: tag systems remove the beginning and tag the selected block onto the end (`BOOK:1112`, `1124`, `1132`); executable order is `Join[Drop[word,n],appendant]` (`:12300-12306`). For canonical `01->10`, `011` becomes `110`, whereas a T16 front splice would produce `101`.
- Consequence: add `ConsumePrefixAppend` and `QueueSpliceUpdate` as a public sibling of `SingleSpliceUpdate`, `ParallelReplaceConcat`, and fixed-support atomic effects. A private ordered-edit carrier may perform deletion at zero plus insertion at the old endpoint only after queue geometry is validated; the two edits are one event and never independently observable.

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

- Status: ACTIVE for T19 and the general control/source boundary.
- Basis: the program counter is visible state and selects the current instruction from a fixed sequence (`BOOK:1176-1180`, `12368`), while the selected instruction names its register operands.
- Consequence: generalize `SingleControl` over typed address domains and add program-coupled `ActiveInstruction` plus instruction-owned operand access. The counter does not turn code or registers into spatial cells; no duplicated instruction table, hidden fetch loop, arbitrary-address callback, or family dispatcher is allowed.

### D033 — Closed register instruction results reuse atomic typed effects

- Status: ACTIVE for T19.
- Basis: increment changes one register and falls through; positive decrement changes one register and jumps; zero decrement preserves the value and falls through (`BOOK:1166-1172` and the repaired `RMStep` at `BOOK:12377`).
- Consequence: use `IncrementResult`, `DecrementJumpTaken`, and `ZeroFallthrough` to return validated `Assign(RegisterSlot, Natural)` and `TransitionControl` effects against one snapshot. Reuse `AtomicEffectsUpdate`; do not add a register-specific commit, partial value/control timing, formula callback, or zero-as-negative/clamp behavior.

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

### D039 — Prefix-free parallel subtree replacement is a fifth update law

- Status: ACTIVE for T20 and the general structural-update boundary.
- Basis: one pass can consume several disjoint subtrees, preserve surrounding context, duplicate/delete/rearrange whole bound subtrees, and atomically produce one tree (`BOOK:1222-1224`, `12456`, `18924-18930`).
- Consequence: add `ReplaceSubtree` and `ParallelPrefixFreeTreeReplace` with exact path/source validation, pairwise prefix independence, one old snapshot, and context/binding/literal lineage. T13 concatenation, T16 one-interval splice, T17 queue edit, and fixed-support effects remain distinct siblings; only a private persistent-tree edit kernel may be shared.

### D040 — No-pattern quiescence, applicable identity, and symbolic representations remain distinct

- Status: ACTIVE for T20 and the general outcome/trace boundary.
- Basis: `/.` returns an unchanged expression when no rule applies; the book calls reached forms fixed and `NestList` can keep sampling them (`BOOK:12407`, `12446`, `12466`). Bracket/Polish/tree forms, valuations, depths, and size plots are separately described representations or properties (`:1228-1238`, `12409-12454`).
- Consequence: emit event-free `Quiescent(NoPatternMatch,state)` with an exact reference self-successor; optional quiescent/value-fixed stops are observers. An applicable identity is `Advanced(changed=false)`. Preserve ragged tree snapshots and match/binding lineage before any codec, padding, raster, numeric valuation, normalization, confluence quotient, cycle observer, or rule enumeration.

### D041 — Geometric state is a multiplicity-preserving bag of fully posed occurrences

- Status: ACTIVE for T27.
- Basis: the main construction replaces independently placed oriented squares, requires each parent's orientation, and permits later descendants to overlap (`BOOK:2326-2344`). In the exact page-190 orbit, two occurrences after three replacements have the same center and same square footprint but frames differing by 90 degrees and different next descendants (`goal-1/10-T27-GEOMETRIC.md`).
- Consequence: add immutable local-frame prototypes and finite occurrence bags of `(prototype_id,full_local_to_world_affine_pose)`. Bag permutation is immaterial and multiplicity is material. Center clouds, present footprints, unions, rasters, prototype-symmetry quotients, branch indices, stable IDs, and list positions cannot replace native state; IDs/order remain trace or reference-codec data.

### D042 — Child geometry is parent-local and composed in an explicit scalar domain

- Status: ACTIVE for T27.
- Basis: the page-204 orientation arrow and primary rule diagrams require local child placement. The exact page-189/page-190 Notes formulas admit rational matrices with `A'=A_parent A_child` and `b'=A_parent b_child+b_parent`; a rotated/translated adversary distinguishes `P∘C` from `C∘P`. Page-191 also contains source-declared approximate coefficients.
- Consequence: total prototype rows contain closed local affine child templates and stable slot IDs. Composition is `parent_pose∘local_pose` over normalized exact rationals/algebraics or an explicitly separate finite-precision profile with literal, precision, and rounding provenance. No world-coordinate transform callback, silent float coercion, tolerance equality, or fabricated exactification is allowed.

### D043 — Full-generation occurrence-bag replacement is a sixth update law

- Status: ACTIVE for T27 and the general structural-update boundary.
- Basis: every old square is replaced once by all of its local children; parents disappear, newborns wait, descendants coexist through overlap, and duplicate/coincident branches retain multiplicity (`BOOK:2326-2354`, `13760-13762`).
- Consequence: add `AllGeometricOccurrences`, self prototype/full-pose reads, `ReplaceGeometricOccurrence`, and atomic `ParallelOccurrenceBagReplace`. Validate exactly one authoritative result per old occurrence, consume all parents, compose every declared slot, bag-union every child, and record parent/slot lineage. T13 source-generation concepts may share private orchestration, but ordered concatenation, flat/tree splices, and fixed-support writes remain different public commits.

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
- Consequence: use finite `PortWord` data, `PortPathRead`, and declared `ExactLengthReachCounts` key domains. Epsilon is self; words fold left-to-right. No traversal callback, reversed codec, cumulative ball substitution, or synthesized generic-depth domain/count is allowed.

### D048 — Fresh graph vertices are typed result occurrences

- Status: ACTIVE for T29.
- Basis: page-215 inserts one new node from every old node, and the Notes allocator appends distinct new nodes whose outgoing links resolve through old paths (`BOOK:2452-2464`, `13848-13872`).
- Consequence: `NodePortRewrite` contains two `DirectOld(path) | InsertFresh(a,b)` expressions. Each syntactic insertion occurrence creates a distinct event-local token; equal descriptors never alias. Fresh targets are old endpoints, tokens are not rule data, and newborns do not fire.

### D049 — Parallel graph reroute/create/project is a seventh update law

- Status: ACTIVE for T29 and the general structural-update boundary.
- Basis: every old node is rewritten from one old snapshot; old nodes persist in the raw successor, fresh nodes are installed, then `ConnectedNodes`/`RenumberNodes` retain directed reachability from node 1 (`BOOK:2440-2464`, `13848-13872`).
- Consequence: add `ParallelRerouteCreateProject` with exact old coverage, frozen proposals, injective event allocation, raw graph construction, newborn deferral, directed root closure, and raw/retained/dropped provenance. In-place updates, weak connectivity, pre-commit pruning, keep-all flags, and relabeled tree/bag/assignment commits are different semantics.

### D050 — Rooted two-port isomorphism has an exact BFS codec

- Status: ACTIVE for T29.
- Basis: graph meaning ignores drawing/list labels but preserves the first/root node and above/below connections (`BOOK:2380-2394`, `2424-2448`). Every strict state is root-reachable and deterministic by port.
- Consequence: breadth-first discovery from root with `Above` before `Below` gives an exact canonical pair array. Use it for equality/serialization/cycle observers while retaining raw token maps in events. Do not merge vertices, erase ports/root, or use general layout/graph-library behavior as semantics. An isomorphic successor is still `Advanced(changed=false)`.

### D051 — Sequential-network source gaps must remain an explicit boundary

- Status: ACTIVE evidence practice.
- Basis: the sequential Notes and official CDF give six `{rewrite,move_port}` rows and a node-count figure evidences pruning, but no evaluator fixes old-versus-committed movement, projection anchor, or movement/projection order (`BOOK:13889-13903`).
- Consequence: parallel T29 remains complete, but Goal 2 must mark the sequential executor unavailable pending decisive primary evidence. Do not silently inherit node-1 projection, choose a timing, expose both as flags, or treat figure layout as an oracle.

### D052 — A base multiway layer is an exact finite set of words

- Status: ACTIVE for T30.
- Basis: the main definition retains all **distinct** sequences, and executable `MWStep` applies `Union` to all generated strings (`BOOK:2494-2510`, `13921-13938`).
- Consequence: add `MultiwayLayer = FiniteSet[Word]` with exact word/set equality, epsilon allowed, no multiplicity/control/ancestry, and a distinct empty layer. Clause/worker/hash order is nonsemantic. Length, counts, anagrams, algebraic equivalence, graph nodes, and derivation copies cannot replace state.

### D053 — Multiway applicability selects every overlapping old literal match

- Status: ACTIVE for T30.
- Basis: `StringPosition` enumerates every occurrence of each LHS in every old string, and `StringReplacePart` produces one result per position (`BOOK:13921-13948`); Chapter 9 describes paths as sequences of single replacements (`6016-6022`).
- Consequence: add program-coupled `AllApplicableLiteralMatches` and reuse T16's pure matched-span/one-splice kernel per branch. Matches include overlaps, are alternatives rather than simultaneous edits, and newborns wait. T16 priority/leftmost selection and host pattern callbacks are not reused.

### D054 — Exact distinct-child branch merge is an eighth update law

- Status: ACTIVE for T30 and the general successor/update boundary.
- Basis: `MWStep` maps all rules/parents and `Union`s exact targets; the Notes call merging crucial and explicitly erase derivation multiplicity in pictures (`BOOK:13923-13938`, `13959-13961`).
- Consequence: add `DistinctBranchMerge`: validate complete match coverage, make one child per witness, exact-union across spans/rules/parents, and record all inbound witnesses plus dead parents. No random choice, path-copy bag, per-parent-only dedupe, repeated T16 rollout, or arbitrary successor callback.

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

- Status: ACTIVE categorical split; evidenced by T31.
- Basis: the main text contrasts explicit stepwise evolution with complete configurations implicitly selected by constraints and says search must go outside the system (`BOOK:2568-2578`, `2642-2664`).
- Consequence: T31 has no source/read/result/update, successor, seed, time, halt, or trajectory. Add a separate constraint/specification category rather than a ninth update, zero-step dynamics, fixed-point rollout, or repair process.

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
- Consequence: T31 owns orientation-insensitive histogram relations. T32 must preserve oriented templates and T33 a global existential condition. Do not collapse them into predicates/flags, over-attribute template/tiling undecidability to the 25 classified count profiles, or use CA/ground-state/network/tiling reductions as native coverage.

### D064 — Arithmetic iteration is a unary exact scalar construction

- Status: ACTIVE for T34.
- Basis: the strict main examples start from one scalar and repeatedly add one constant or multiply by one constant (`BOOK:1439-1495`).
- Consequence: use a domain-tagged scalar slot, `UniqueScalar`, the complete current-value read, and the closed public sum `AddConstant | MultiplyConstant`. Do not expose a general affine/expression AST, rule ID, predicate, formula callback, digit grid, temporal-history seed, or finite alphabet as the construction.

### D065 — Exact numeric domains, typed identity, and serialization are explicit

- Status: ACTIVE for T34 and shared numeric infrastructure.
- Basis: canonical integer powers/addition and exact rational powers of `3/2` are stated directly, while the Notes distinguish real/finite representations and their limitations (`BOOK:1479-1495`, `12503-12536`, `13217-13247`).
- Consequence: initial Goal 2 support is arbitrary-precision signed integers and normalized rationals; domain tags participate in identity, while cross-domain numeric equivalence is an observer. Serialize big integer components as decimal strings. Certified-real and declared-precision profiles are separate; reject implicit promotion, booleans/floats, tolerance equality, undeclared rounding, or exact-to-approximate coercion.

### D066 — Arithmetic scalar assignment reuses fixed typed effects

- Status: ACTIVE for T34.
- Basis: each valid operation replaces the one old scalar with exactly one result and has no structural support change (`BOOK:1443-1495`).
- Consequence: `ArithmeticAssignment` lowers to `Assign(ScalarSlot,next)` and atomic effects commit. Every valid event yields one `Advanced` successor, including identity events. T34 adds no ninth update law and no native halt, boundary, modulus, capacity, cycle stop, or target threshold.

### D067 — Digits and plots are exact observers, while modulus is an explicit sibling

- Status: ACTIVE for T34 and representation design.
- Basis: the source presents the same values as base-2 rows, fractional-part dots, lengths, counts, and cropped views; it separately identifies `3^n mod 2^s` as an LCG relation (`BOOK:1443-1495`, `12538-12570`, `3722-3744`).
- Consequence: digit views declare base/order/radix/sign/window/crop/padding and never feed back. Fractional/value/size/count/leading-digit views remain downstream. Finite suffix evolution is separately typed `MultiplyMod` over a residue ring, not a render crop, hidden overflow, or current AR2.

### D068 — Closed forms and compilers do not change event traces

- Status: ACTIVE for T34 and evaluator design.
- Basis: `x_0+t*c`, `x_0*c^t`, direct digit formulas, repeated squaring, and special CA encodings reproduce requested observations more quickly or in another carrier (`BOOK:7380-7424`, `7974-7980`, `9058-9080`, `17849-17920`).
- Consequence: expose optional exact random-access evaluators and explicit compilation mappings, but a requested `h`-event trace still has `h+1` states and `h` real events. No fast-forward result may fabricate provenance, skip requested snapshots, or turn CA/substitution/LCG state into native arithmetic state.

### D069 — Neighboring scalar catalogs share a shell, not one rule algebra

- Status: ACTIVE boundary across T34-T45.
- Basis: parity branching begins T35 at `BOOK:1497`, digit feedback begins T36, recursive-history and real interval maps have different state/access invariants, and continuous fields/PDEs add spatial or derivative semantics.
- Consequence: T35 may reuse the scalar carrier/source/effect but owns predicate-selected arms; T36 owns base-sensitive digit transforms; T37/T38 own growing histories; T43 owns closed nonlinear interval maps and real precision; T44/T45 remain field categories. Do not hide these behind operation flags or a universal 0D callback.

### D070 — Recursive-sequence state is the complete indexed numeric prefix

- Status: ACTIVE for T37 and a required starting point for T38.
- Basis: the source names stable terms `f[1],f[2],...`, computes `f[n]` from earlier terms, and presents the accumulated sequence (`BOOK:1555-1567`).
- Consequence: add `NumericPrefix(domain,origin,terms)` with consecutive support and exact ordered values. A newest scalar, hidden trajectory history, or bounded lag window is not canonical equality. T34 remains unary scalar assignment even when its value stream matches a T37 projection.

### D071 — Strict T37 programs are normalized affine fixed-lag data

- Status: ACTIVE for T37.
- Basis: the main text fixes positive distances behind `n`, and the Notes explicitly classify every page-128 row as linear (`BOOK:1561-1567`, `12690`). Factorial is separately named nonlinear evidence (`12692-12696`).
- Consequence: strict programs are `bias + sum(coefficient[lag]*f[n-lag])` with unique positive literal lags and exact domain values. Fresh seed length equals `max_lag`; longer resumptions are replay-verified checkpoints. A named closed `Literal|TargetIndex|Lag|Neg|Add|Sub|Mul` extension covers factorial after strict conformance; callbacks, computed indices, branches, and arbitrary recursion remain excluded.

### D072 — One-term persistent append is the ninth update law

- Status: ACTIVE for T37.
- Basis: each step determines the next indexed term from the old sequence while every earlier term persists (`BOOK:1559-1567`).
- Consequence: add `NextSequenceTerm`, old-prefix `FixedLagRead`, `AppendTerm`, and atomic `AppendOnlySequenceUpdate`. Validate one old-snapshot result, exact next index/dependencies, byte/value preservation of the entire old prefix, and exactly one newborn endpoint. Private endpoint-insert mechanics may compose, but T34 assignment, T16 nonempty splice, and T17 consume/append remain different public laws.

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
- Consequence: closed forms/matrices/generating functions/memoization do not change requested append traces. Modular AR2 is a residue-domain variant, not exact T37. T39 resolves Ulam as `FirstAcceptedAscendingCandidate` over the complete old prefix followed by the existing T37 append; it is not hidden in the fixed-lag AST and does not reopen T37 state/update semantics.

### D076 — T39 splits transition sieves from pure filters and measurements

- Status: ACTIVE category split for T39.
- Basis: page 147 explicitly shows successive removal rows, while page 148 calls its curves features of the resulting prime sequence and page 150 describes sequences based on number properties (`BOOK:1623-1633`, `1641-1663`).
- Consequence: use separately typed `SuccessiveDivisibilitySieve`, `IntegerFilterSpec`, and `IntegerMeasurementSpec`. Only the sieve has source/read/result/update/successor semantics. Finite accepted/rejected partitions, lazy streams, direct queries, and exact `g(n)` results remain pure records; do not invent empty transition fields or force them through rollout.

### D077 — The strict sieve uses consecutive stages and a visible cursor

- Status: ACTIVE for T39 strict execution.
- Basis: the prose advances from divisor 2 to 3 “and so on,” and the page-147 raster labels every row `2..13`, including composite stages with zero new removals (`BOOK:1623-1627`). All 1,200 cells match the proper-multiple rule.
- Consequence: `SuccessiveDivisibilitySieveProgram` has `ConsecutiveIntegers(first=2)` and finite/intensional state includes `next_divisor`. Hits are all original-domain proper multiples, while `newly_removed=hits intersect old_survivors`. Equal survivor sets at different cursors are unequal states; a zero-removal composite row is still `Advanced(changed=false)` because the cursor advances. Prime-pivot scheduling is an explicit trace-distinct variant.

### D078 — Monotone candidate-subset removal is the tenth update law

- Status: ACTIVE for T39 strict execution and candidate-elimination reuse.
- Basis: each stage deletes a possibly noncontiguous survivor subset, never resurrects a removed value, and preserves every retained integer's identity and increasing order (`BOOK:1623-1627`; exact page-147 masks).
- Consequence: add `RemoveCandidateSubset(stage,hits,newly_removed)` and atomic `MonotoneFilterUpdate`. Validate exact old-snapshot witnesses, subset membership, cursor increment, no resurrection, and retained identity/order. A finite Boolean mask can realize the law privately, but fixed assignment, interval/queue/tree/bag/graph/multiway updates, and prefix append retain different public validators.

### D079 — Literal display, mathematical domain, certification, and completion are explicit scopes

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
- Consequence: add `FirstAcceptedAscendingCandidate(start=last(prefix)+1,predicate,explicit_context)` with `UniqueUnorderedDistinctPriorPairSum` over indices `i<j` in the complete old prefix. Candidate checks form a nested selection witness; only the accepted value is T37 `AppendTerm`. Pair-sum tables are reproducible caches, not semantic state. T37's ninth update law and fixed-lag boundary remain unchanged.

### D082 — T41 mathematical functions are immutable closed definitions outside transition execution

- Status: ACTIVE category split for T41.
- Basis: the source asks about “functions themselves,” plots their curves, and describes finite arithmetic combinations without any update/evolution language (`BOOK:1834-1848`). Supporting Notes explicitly identify named mathematical functions as accepted primitives in formulas (`BOOK:17794-17798`).
- Consequence: add a versioned unary `MathematicalFunctionSpec` declaring one argument, exact parameters, real/complex domain, scalar/fixed-vector codomain, closed expression, primitive registry, partiality, and branch conventions. It has no state/source/read/result/update/successor shell; multivariate syntax needs later evidence. Reuse T20 tree/codec responsibility only; callbacks, strings, host CAS objects, sampled arrays, and fake argument-as-time rollout are invalid.

### D083 — Mathematical domain and numerical query context are separate scopes

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
- Consequence: strict expressions support exact bounded finite sums or expanded additions. Infinite series use a distinct `SeriesFunctionSpec` with convergence domain, summation meaning, and evaluation context. No `infinity` sentinel in a finite binder, hidden truncation, raster width, or resource cap may masquerade as a mathematical infinite sum; the `a=0` picture is an explicitly truncated/otherwise specified approximation only.

### D087 — Page 162 is a typed T41-query/T42-construction composition

- Status: ACTIVE boundary across T41/T42.
- Basis: the main and Notes first derive two exact zero families and interval counts, then say the resulting word can be reproduced by a sequence of substitution rules whose choices come from continued-fraction terms (`BOOK:1850-1858`, `13170-13172`). The connection is explicitly absent for more than two sine terms.
- Consequence: T41 owns source functions, zero/crossing/touch semantics, and exact interval-count query results. T42 owns continued-fraction expansion, coefficient stream, symbols, rule schedule, substitution state/update, and trace. A typed finalized T41 result may feed T42; neither category embeds the other's callbacks/state, and the page-162 bitmap is never executable source data.

### D088 — T43 state is one domain-tagged real scalar under one immutable closed self-map

- Status: ACTIVE construction profile for strict T43.
- Basis: the defining paragraph repeatedly updates “a number between 0 and 1” by a fixed map that returns a definite number in the same interval (`BOOK:1868-1872`). Strict figures use four unary expressions and separate exact initial conditions (`BOOK:1874-1896`; page-165 raster).
- Consequence: add `IteratedMapSpec`, exact `RealInterval` state space, one scalar slot, exact/declared parameters, ordered map AST/version, and an independently serialized seed. State contains no orbit prefix, digit row, step counter, or hidden control. Strict `[0,1]` endpoints are explicit even though prose says “between.”

### D089 — T43 reuses complete scalar assignment and adds no eleventh update law

- Status: ACTIVE reuse across T34/T43.
- Basis: every event reads the current scalar, applies one map, and replaces it with one result; `NestList` confirms one initial snapshot plus one state per application (`BOOK:1870`, `10682-10687`).
- Consequence: `UniqueScalar` returns a complete old-value read; `MapAssignment` lowers to `Assign(MapStateSlot,next)` and existing `AtomicEffectsUpdate`. A fixed point/identity event is still `Advanced(changed=false)`. Fixed-effects preservation is unchanged from T34; only value/program/evaluator profiles extend.

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

- Status: ACTIVE construction profile for strict T44.
- Basis: each discrete cell has any gray level from white `0` to black `1`, the point seed is one black cell on white background, and every next field is computed locally (`BOOK:1954-1960`, `2018`). The cardinality Note gives `2^aleph_0` possible configurations (`BOOK:19070-19072`) but does not determine support: a single real cell or any nonempty finite real vector has that cardinality too.
- Consequence: add a total `[0,1]` field over fixed ordered 1D support with no control/history. The strict-main integer-line interpretation is explicitly inferential; Notes separately prove a finite periodic-list realization. For deterministic spatially homogeneous point-seed profiles at finite horizons, normalized uniform-default plus finite overrides is an exact presentation, not finite semantic support; random-initial/noisy total fields require their own finite or lazy random-field/draw presentations. Seed, rule, support/realization, numeric profile, trace, and view remain separate.

### D097 — Closed affine aggregate and scalar map form one validated local program

- Status: ACTIVE rule/data boundary for T44.
- Basis: the strict law averages left/self/right and applies one fixed map; a later profile multiplies both neighbors by declared `1.13` before the literal division by three (`BOOK:1956`, `1982`, `2904`).
- Consequence: add `AffineNeighborhoodAggregate(offset_weight_terms,divisor)` and `AggregateThenMap` with ordered closed scalar syntax and replayable composite range validation from the value cube to the output interval. The intermediate need not stay in `[0,1]`: exact reconstruction `{113/100,1,113/100}/3` reaches `163/150`. Never use an arbitrary reducer/map callback, a normalized `2w+1` divisor, a trusted closure flag, or implicit clamp/modulo.

### D098 — T44 reuses T01 fixed-field assignment and adds no eleventh update law

- Status: ACTIVE reuse across T01/T44.
- Basis: all sites read the same old left/self/right values and assign one next value to the same site in parallel; Notes express the operation as one `Map` over old rotated lists (`BOOK:1956`, `13283-13292`).
- Consequence: reuse `AllSites`, ordered old reads, typed `Assign(CellSlot,next)`, and atomic fixed-effects commit. Infinite semantic events may reference before/after total-field identities and compact reconstruction rather than enumerate infinite effects. In-place/asynchronous evaluation and partial commits are invalid. The provisional transition family remains at ten update members.

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

## Rejected Shortcuts

These are globally rejected unless Principle 0 re-derivation replaces the goal itself:

- family-name rollout dispatch as the proposed universal runtime;
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
- compiling another construction to a CA merely to claim native coverage;
- treating canonical `[t,x,y,z]` encoding or visualization coordinates as topology;
- conflating a constraint with a solver, a PDE with a discretization/integrator, or a stochastic law with an RNG implementation;
- weakening tests, adding flags/shims/fallbacks, or duplicating shared primitives under family-specific names.

## Integration Log

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

## Open Architecture Questions

1. Which remaining catalog rows are constructions versus restrictions, presets, seed classes, observables, or solver-defined systems? T01 is a construction; T06/T07/T08 are already cross-referenced as restriction/seed hypotheses requiring their own evidence.
2. The source/read/result/update protocol remains substantive through T30 and the T34/T37/T39/T43 transition profiles but explicitly does not cover T31, pure T39 filters/measurements, or T41. T41 adds immutable definitions plus scoped evaluation/zero records; T43 reuses compatible syntax only inside a feedback contract and fixed assignment. T42 may consume a T41 result without importing evaluator or substitution state. Derivatives, distributions, and PDE solution/operator categories still require independent evidence.
3. T30 establishes that base branch occurrences are provenance, while exact child words form semantic set state and recur independently of a compressed graph. Which later stochastic/quantum/multiway-tag systems instead make weights or derivation multiplicity semantic must be separately evidenced.
4. T31 proves that a single witness, an orbit representative, and a mathematical solution set are distinct. How should later T32/T33 template syntax and T45 PDE solution/operator categories reuse verifier/query infrastructure without collapsing their carriers?
5. Can T14/T15 reuse the epsilon-capable private ordered-span kernel without erasing contextual eligibility or their own deletion laws? T17 proves reuse is safe only behind a distinct public queue validator/update.
6. What lossless record encoding preserves non-rank-0..3 semantic addresses and categories—including exact scalar/prefix/sieve/map transitions, represented-number realizations, constraint records, immutable function specs, and reproducible function/map-query results—while keeping mathematical identity, equivalence/conjugacy proofs, certificates, diagnostics, renderings, and big numeric values distinct across JSON consumers?
7. Which current selector, alphabet, rule-summary, seed, RNG, and raw-result components survive later evidence without semantic reinterpretation?
8. Which current tests are canonical-construction evidence and which merely preserve incidental Phase 1 behavior? T01 shows that geometry and self-parity tests alone do not prove rule semantics.
9. Which versioned primitive/evaluator/certificate interfaces can T41/T43 share with later T45 while keeping denotation, feedback transition, solver/integrator algorithm, numerical realization, and diagnostic work traces separate?
10. Which exact-real/interval backend can Goal 2 support honestly for named transcendental states such as `Pi/4`, exact piecewise comparison, and replayable invariant certificates? Until synthesis selects one, executable exact profiles must expose typed unsupported cases rather than silently fall back to machine arithmetic.
