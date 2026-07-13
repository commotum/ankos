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
| Support/topology | Fixed regular lines/total fields and explicit discrete ordered sequences are members; T19 adds a finite named register bank whose stable keys have no adjacency | PROVISIONAL lattice, ordered-sequence, and named-bank members; other dynamic topology UNRESOLVED | T01, T09, T12, T13, T16, T17, T19 |
| Values/alphabet | Explicit finite field/word values; independent value/control domains; epsilon-capable private words; exact infinite `Naturals` for numeric registers | PROVISIONAL finite alphabets/words and natural-number domain; other infinite/continuous values UNRESOLVED | T01, T09, T12, T13, T16, T17, T19 |
| Control | `SingleControl(key,position,payload)` in visible Markov state over a typed address domain; unit payload for T09/T19, finite head-state payload for T12; the address need not belong to mutable value support | PROVISIONAL single-control member; multiple/structural control UNRESOLVED | T09, T12, T19; absent T01/T13/T16/T17 |
| Active loci | Firing/source selector: `AllSites`, `ControlLocus`, `AllOccurrences`, program-coupled `FirstApplicableMatch`, program-width-coupled `RequiredQueuePrefix`, or program-address `ActiveInstruction`; finite materialization belongs to realization | PROVISIONAL fixed/control/sequence/matched/queue-head/code sources; branching sources UNRESOLVED | T01, T09, T12, T13, T16, T17, T19 |
| Reads/access | Explicitly ordered topology-relative values, source-control payload, occurrence self value, exact matched span/prefix, or instruction-owned named operands; read and mutation spans/targets may differ | PROVISIONAL for fixed lattices/single control/ordered words/named banks; path access UNRESOLVED | T01, T09, T12, T13, T16, T17, T19 |
| Rule choice | Explicit total finite tables, total word morphisms, immutable ordered literal/prefix programs, or a closed tagged instruction algebra with validated operands; no implicit defaults/callbacks | PROVISIONAL for local/control/morphism/rewrite/queue/register programs; broader calculations UNRESOLVED | T01, T09, T12, T13, T16, T17, T19 |
| Rule result | Typed members include `Assign`, payload-bearing `TransitionControl`, ordered replacement/queue results, and branch-specific register instruction results | PROVISIONAL result sum; never a universal category | T01, T09, T12, T13, T16, T17, T19 |
| Commit/update | Explicit siblings: fixed-support atomic effects, full-generation ordered replacement, exactly-one-interval ordered splice, and coupled prefix-consume/tail-append; T19 reuses atomic effects across named bank/control components | PROVISIONAL four-member update family; conflicts/rewire/other mutation UNRESOLVED | T01, T09, T12, T13, T16, T17, T19 |
| Successors | Deterministic execution may yield one advanced successor, typed quiescence with reference stutter, or a retained zero-successor terminal outcome | PROVISIONAL deterministic/quiescent/terminal case; branching/solutions/derivatives remain distinct and UNRESOLVED | T01, T12, T16, T17, T19 |
| Halting/invalidity | Base continuation, terminal-control, no-match, insufficient-prefix, past-end quiescence, explicit program exit, external stop, horizon, reference projection, invalidity, and error are distinct | PROVISIONAL outcome model; other construction-specific halt/invalidity UNRESOLVED | T12, T16, T17, T19; no intrinsic halt T01/T09/T13 |
| Trace encoding | Structured snapshots preserve values/control/outcomes or ragged occurrences; events preserve effects/branches/lineage; synthetic reference samples are labeled; dense coordinates are downstream lowerings | PROVISIONAL for fixed 1D, ordered sequences, and named register banks; global schema UNRESOLVED | T01, T09, T12, T13, T16, T17, T19 |
| Solver/numerics | None in deterministic table transition | NOT APPLICABLE to T01; global boundary remains UNRESOLVED | T01 |

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

## Open Architecture Questions

1. Which remaining catalog rows are constructions versus restrictions, presets, seed classes, observables, or solver-defined systems? T01 is a construction; T06/T07/T08 are already cross-referenced as restriction/seed hypotheses requiring their own evidence.
2. Where does the T01/T09/T12/T13/T16/T17/T19 source-read-result-update protocol cease to be substantive? Program-coupled matching, queue heads, and closed instruction access remain meaningful; multiway branching, constraints, and derivatives remain adversarial.
3. Which state models require topology richer than T13's discrete order/T19's named bank, lineage that affects future rules rather than traces only, or control beyond a single typed address/payload?
4. Can T14/T15 reuse the epsilon-capable private ordered-span kernel without erasing contextual eligibility or their own deletion laws? T17 proves reuse is safe only behind a distinct public queue validator/update.
5. What trace encoding preserves types whose semantic address is not a rank-0..3 lattice coordinate?
6. Which current selector, alphabet, rule-summary, seed, RNG, and raw-result components survive later evidence without semantic reinterpretation?
7. Which current tests are canonical-construction evidence and which merely preserve incidental Phase 1 behavior? T01 shows that geometry and self-parity tests alone do not prove rule semantics.
