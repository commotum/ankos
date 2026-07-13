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
| Support/topology | Fixed fields, ordered sequences, named banks, rooted expression trees, affine occurrence bags, rooted port graphs, and finite exact sets of words are members | PROVISIONAL lattice/sequence/bank/tree/bag/graph/word-set members; continuous/general topology UNRESOLVED | T01, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30 |
| Values/alphabet | Explicit finite field/word/atom values; independent value/control domains; epsilon-capable words; exact `Naturals`; pattern/geometry/graph values; finite word-set membership is exact and unweighted | PROVISIONAL finite/infinite discrete, affine/point, graph-reference, and set-lifted members; other continuous/function values UNRESOLVED | T01, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30 |
| Control | `SingleControl(key,position,payload)` in visible Markov state over a typed address domain; unit payload for T09/T19, finite head-state payload for T12 | PROVISIONAL single-control member; multiple/structural control UNRESOLVED | T09, T12, T19; absent T01/T13/T16/T17/T20/T27/T29-parallel/T30 |
| Active loci | Firing/source selectors include sites, control loci, ordered/bag occurrences, network nodes, program-coupled flat/tree matches, queue prefixes, instructions, and every literal match across every word in a layer | PROVISIONAL fixed/control/sequence/bag/graph/interval/queue/code/tree/multiway-match sources | T01, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30 |
| Reads/access | Ordered topology values, control payload, self values, spans/prefixes, operands, tree bindings, geometric poses, graph path/signatures, or exact matched parent intervals; read and mutation coverage may differ | PROVISIONAL for fixed/control/word/bank/tree/bag/graph/multiway profiles | T01, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30 |
| Rule choice | Total tables/morphisms, ordered rewrite programs, closed instructions/templates/ASTs, topology tables, or unordered finite literal relations; no implicit defaults/callbacks | PROVISIONAL local/control/morphism/rewrite/queue/register/tree/geometric/graph/multiway programs; broader calculations UNRESOLVED | T01, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30 |
| Rule result | Typed members include effects/control transitions, word/queue/tree/bag/graph replacements, instruction branches, and one literal interval replacement per multiway witness | PROVISIONAL result sum; never a universal category | T01, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30 |
| Commit/update | Explicit siblings: fixed effects, ordered replacement, one splice, queue edit, prefix-free tree replacement, bag replacement, rooted graph reroute/create/project, and exact multiway branch union | PROVISIONAL eight-member update family; constraints/derivatives/other mutation remain distinct | T01, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30 |
| Successors | Execution may yield one advanced successor—including a complete set-valued macro successor—typed quiescence/reference stutter, or retained zero-successor terminal outcome | PROVISIONAL deterministic/set-lifted/quiescent/terminal cases; solution sets/derivatives remain distinct and UNRESOLVED | T01, T12, T16, T17, T19, T20, T27, T29, T30 |
| Halting/invalidity | Base continuation, terminal/no-match/prefix outcomes, quiescence, explicit exit, all-dead-to-empty advancement, empty-layer stutter, observers, projection, validation, resource, and rendering cutoffs are distinct | PROVISIONAL outcome model; other construction-specific invalidity UNRESOLVED | T12, T16, T17, T19, T20, T27, T29, T30 |
| Trace encoding | Structured snapshots preserve fields/control, ragged words/trees, affine bags, rooted graphs, or exact word sets; events preserve effects/matches/paths/births/projection/branch witnesses before graph/count/render lowerings | PROVISIONAL fixed/ordered/bank/tree/geometry/graph/multiway traces; global schema UNRESOLVED | T01, T09, T12, T13, T16, T17, T19, T20, T27, T29, T30 |
| Solver/numerics | Exact rational/algebraic affine and point evaluation is semantic where declared; finite precision has explicit literal/precision/rounding provenance; limits, dimension, parameter filters, rendering, and tolerance are observers/algorithms | PROVISIONAL exact/declared numeric profiles and semantic-versus-observer boundary | T01 (not applicable), T27 |

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

## Open Architecture Questions

1. Which remaining catalog rows are constructions versus restrictions, presets, seed classes, observables, or solver-defined systems? T01 is a construction; T06/T07/T08 are already cross-referenced as restriction/seed hypotheses requiring their own evidence.
2. The source/read/result/update protocol remains substantive through T30: one macro successor can be a complete exact branch set when `DistinctBranchMerge` is an explicit commit. T31 constraints are the next direct test because they denote models/solutions rather than transition sources/results.
3. T30 establishes that base branch occurrences are provenance, while exact child words form semantic set state and recur independently of a compressed graph. Which later stochastic/quantum/multiway-tag systems instead make weights or derivation multiplicity semantic must be separately evidenced.
4. Can T14/T15 reuse the epsilon-capable private ordered-span kernel without erasing contextual eligibility or their own deletion laws? T17 proves reuse is safe only behind a distinct public queue validator/update.
5. What trace encoding preserves types whose semantic address is not a rank-0..3 lattice coordinate? T20 establishes ragged typed paths/events and T27 exact occurrence bags/parent-slot lineage before lowering, but neither settles a universal schema.
6. Which current selector, alphabet, rule-summary, seed, RNG, and raw-result components survive later evidence without semantic reinterpretation?
7. Which current tests are canonical-construction evidence and which merely preserve incidental Phase 1 behavior? T01 shows that geometry and self-parity tests alone do not prove rule semantics.
