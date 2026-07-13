# Goal 1 Representation and Execution Architecture Audit

Status: **IN PROGRESS — HARD PREREQUISITE FOR T06 AND ALL FURTHER TYPE WORK**

## Trigger and Scope

T09/T12 and decisions D009-D014 are reopened because they promoted one state decomposition—separate `SingleControl`/`TransitionControl` records—into a semantic requirement. The audit covers every completed decision and every proposed state, control, frontier, neighborhood, rule result, update law, executor, and runtime API extension. It updates affected stage files, the design ledger, the global plan, and Goal 2 handoffs before T06 or any other type stage resumes.

In this audit, **DOMAIN** is the task/program's dimensional space together with its support/topology: `t+0D`, `t+1D`, `t+2D`, `t+3D`, and so on, with discreteness or continuity stated explicitly. The configuration labels or structures that space; DOMAIN itself is not restricted to a dense `Z^4` tensor. A tape alphabet, head-state set, scalar value set, parameter set, address set, or numeric representation is not a DOMAIN; those are ALPHABET/value-schema factors, keys, or profiles.

## Governing Simple-Program Algebra

The library target is Wolfram's finitely described transition/rewrite system, not a cellular-automaton library with other constructions attached. Cellular automata are one preset of the following common algebra:

```text
SimpleProgram:
    CONFIGURATION  labeled DOMAIN/support/topology plus structural invariants
    SEED           one valid initial configuration
    FRONTIER       rule-firing loci, occurrences, or matches
    NEIGHBORHOOD   information visible at each firing locus
    RULE           typed writes/replacements
    UPDATE         composition/schedule producing next configuration(s)

active = FRONTIER.select(state)
reads  = NEIGHBORHOOD.read(state, active)
writes = RULE(active, reads)
next   = UPDATE.apply(state, active, writes)
```

The runner is branch-free over this protocol. Different domains/topologies, finite or structured alphabets, composite/tagged values, frontier selectors, access patterns, typed rule-result schemas, and update composition policies are implementations or values of these axes—not family executors or top-level semantic state classes. A cellular automaton is the fixed-lattice/all-sites/local-stencil/scalar-label/snapshot-parallel preset.

A lossless representation map `e` establishes reuse when it preserves the complete configuration, requires no hidden interpreter, and commutes one step at a time:

```text
e(step_A(state)) = step_B(e(state))
```

Pure constraint/model sets, uniterated function definitions, and general PDE relations without a specified evolution problem lack canonical stepwise evolution and therefore remain genuine nonfits. Multiway systems still fit by lifting one successor to a set of configurations.

### Primary Evidence for the Abstraction

- `BOOK:402` defines programs by rules specifying what happens at each step and introduces cellular automata as one program class, not as the universal container.
- `BOOK:684` and `BOOK:1248` deliberately vary fixed arrays, parallel application, and fixed size while retaining stepwise rule application.
- `BOOK:7918` gives one-step cellular encodings of mobile automata and Turing machines using additional cell colors. This is direct evidence for transparent composite labels and a commuting representation, not evidence that their compact native rule tables become arbitrary CA tables.
- `ref/notes/alphabets.md:54-101` explicitly records `CellAlphabet = TapeSymbol union (TapeSymbol x HeadState)` and treats tape-symbol and head-state roles inside a finite/composite alphabet.
- `ref/roadmap/alphabets.py:33-67` already sketches product and tagged-union alphabet support as an extension of the existing alphabet axis.

## Classification Vocabulary

1. **DIRECT REUSE** — an existing construction expresses the complete state and transition semantics unchanged.
2. **PARAMETER / RESTRICTION / PRESET / INVARIANT / NAMED ROLE** — no new execution algebra; validation or a closed specialization distinguishes the construction.
3. **LOSSLESS TAGGED / PRODUCT REPRESENTATION** — an explicit structural isomorphism preserves every state component and transition, without hidden data or altered behavior.
4. **GENUINELY DIFFERENT EXECUTION ALGEBRA** — a concrete counterexample proves the smallest existing construction cannot express the state change faithfully.

Different source terminology, semantic role names, or decompositions of equally shaped state do not by themselves justify a new class. Conversely, a collapse is rejected if it requires hidden state, callbacks, family dispatch, lossy encoding, invented behavior, or altered update semantics.

## Reopened Core Finding

For a Turing machine, let

```text
Cell = Plain(TapeSymbol) | Head(HeadState, TapeSymbol)
X : Z -> Cell
invariant: exactly one coordinate contains Head(...)
```

This is losslessly equivalent on valid states to a tape-symbol field plus one `(position,head_state)` record. It keeps both the head state and the symbol beneath it visible. A bare `TapeSymbol union HeadState` is not equivalent because it loses the underlying symbol.

The compact rule remains `delta : Q x Sigma -> Q x Sigma x {L,R}`. `FRONTIER` selects the unique old head cell. The native decision reads `(q,sigma)` at the source; its structural lowering also reads the selected destination label so the symbol under the moved head is retained. From that one old snapshot, the rule writes a plain symbol at the source and a head-tagged old destination symbol at the neighbor, then `UPDATE` commits both writes atomically. No zero-head or two-head intermediate configuration is observable. This does not identify the compact Turing program with the enormous set of arbitrary cellular-automaton tables over `Cell`.

The T09 specialization uses `Cell = Plain(bit) | Active(bit)` and the same exactly-one invariant. Its compact eight-row, four-result rule remains native. Because the mobile direction can depend on the old head's radius-one context, a full-slice radius-one target-local CA lowering is not assumed; a closed two-target structural lowering suffices, and any full-slice lowering must prove its required radius.

## Audit Matrix

| Decision / stage | Evidence and former claim | Classification | Smallest reusable base | Required invariants / structural mapping | Reopen action |
|---|---|---|---|---|---|
| D009 / T09 | Mobile event originates at the old active cell | DIRECT REUSE | Simple-program `FRONTIER` as rule-firing loci | Select the unique tagged active cell; typed rule writes may target source and destination; broaden the current writable-coordinate-only schema | Retain source-frontier conclusion; revise storage assumptions and Goal 2 lowering |
| D010 / T09 | Active position must be visible; former conclusion required a separate state component | LOSSLESS TAGGED / PRODUCT REPRESENTATION | Finite composite alphabet on the existing field | `Plain(bit) <-> (bit,None)`; `Active(bit) <-> (bit,Unit)`; exactly one active tag | Replace storage mandate with representation-neutral visibility and validation |
| D011 / T09/T12 | Write and move/state change are one atomic event; former conclusion required `TransitionControl` effects | DIRECT REUSE / PARAMETERIZATION | Existing old-snapshot atomic UPDATE with a typed finite-write result | Two writes are computed from one valid old state; collision/coverage validation; successor preserves exactly-one tag | Reuse atomic commit, broaden its write schema, and remove the unjustified effect class |
| D012 / T01/T09 | Physical `[left,self,right]` read and codec are shared | DIRECT REUSE | Existing ordered NEIGHBORHOOD/read codec | Preserve physical order before rule decoding; no mobile-specific permutation | Retain unchanged |
| D013 / controlled traces | Raw traces must retain active/head information | PARAMETER / INVARIANT / NAMED ROLE | Existing complete state trace over composite values | Tagged field round-trips exactly; compressed/display traces remain observers | Rewrite representation-neutral wording |
| D014 / T09/T12 | Head payload and position must be visible; former conclusion required `SingleControl` | LOSSLESS TAGGED / PRODUCT REPRESENTATION | Composite finite cell alphabet plus fixed field | `Plain(sigma) | Head(q,sigma)` isomorphic to `(tape,position,q)` on exactly-one states | Replace required class with optional named projection/view |

## Complete Decision Matrix

The classification number in this matrix refers to the four categories above. A class-2 result may still require a new closed implementation of an existing axis—for example a graph replacement `UPDATE`—but never a family executor or top-level construction class. “Basis” retains the direct book/runtime evidence already quoted in the named ledger decision; the extra citations below are the evidence that changes or constrains its architectural conclusion.

### Foundation through T17 (D000-D030)

| Decision | Basis / audit evidence | Class | Smallest reusable base | Required invariants or mapping | Disposition / reopen |
|---|---|---:|---|---|---|
| D000 | Principles 0-2; `BOOK:402,1248` | 2 | Branch-free `SimpleProgram` protocol for step/rewrite systems | Nonstep categories do not receive fake empty fields | Rewrite candidate as confirmed scope; Foundation architecture reopens |
| D001 | Principles 4,11; constraint/function/PDE counterexamples | 2 | Tagged semantic categories beside `SimpleProgram` | Different roles may share representation without sharing denotation | Keep and add role-vs-class guard |
| D002 | Current family dispatch in `rollout.py`; Principles 2,14 | 1 | One runner calling typed axes | No `if family`, hidden state, callback, or duplicated rollout | Keep |
| D003 | Exact CSV join | 2 | Provenance/conformance IDs | Catalog ID never chooses runtime class | Keep and clarify |
| D004 | T01 old-snapshot step; `BOOK:418-430,10984-10992` | 2 | `SimpleProgram` CA preset | Fixed lattice/all sites/table are axis values, not the executor algebra | Rewrite; T01 handoff reopens |
| D005 | T01 infinite line, finite realization, trace evidence | 3 | DOMAIN/support declaration plus explicit realization and trace mapping | Lowering is inspectable and lossless at declared scope | Keep; normalize DOMAIN vocabulary |
| D006 | `BOOK:10988`; asymmetric runtime defect | 2/3 | Ordered NEIGHBORHOOD plus explicit table codec | Read order and serialization significance commute | Keep |
| D007 | T01 center replacement | 2 | Generic typed write/replacement result | Same-site scalar assignment is one RULE-result preset | Rewrite class wording; no assignment subclass per family |
| D008 | Binary radius-one evidence | 2 | CA preset over generic axes | Preset fixes values only; no executor/seed/boundary | Keep |
| D009 | T09 old active cell fires; `BOOK:854-862,11957-11970` | 1 | FRONTIER selects rule applications | Unique active tag; writes may name other targets | Revalidated; current writable-coordinate schema must broaden |
| D010 | Notes `{list,n}` plus `alphabets.md:54-101` | 3/2 | Composite ALPHABET `Plain(v) | Active(v)` | Exactly one tag; pack/unpack bijection; visible in state/trace | Rewrite; retire required separate control component |
| D011 | T09/T12 simultaneous value/move evidence | 1/2 | RULE returns finite typed writes; UPDATE commits atomically | All reads from one snapshot; collision/coverage checks; valid successor | Rewrite; retire required `TransitionControl` effect |
| D012 | Physical `[left,self,right]` Notes code | 1 | Shared ordered NEIGHBORHOOD/codec | No family permutation; asymmetric oracle | Keep |
| D013 | Mobile trace/observer evidence | 2/3 | Full configuration trace | Composite tags round-trip; compression remains observer | Keep with representation-neutral wording |
| D014 | Turing head-state evidence plus composite-alphabet note | 3/2 | `Plain(sigma) | Head(q,sigma)` | Exactly one head; underlying symbol retained; optional factored view commutes | Replace `SingleControl` mandate; T12/T19 dependencies reopen |
| D015 | Sparse blank tape Notes | 2/3 | Fixed-line DOMAIN with default/override labeled field | Total inspectable value at every integer; finite realization separate | Keep |
| D016 | Base/nonhalting/Busy-Beaver/stop evidence | 2 | Typed run outcomes around runner | Terminal, external stop, horizon, invalidity, error distinct | Keep |
| D017 | OCR-damaged codec plus code 3024 guards | 2 | Evidence/provenance policy | Repair explicit and independently replayed | Keep |
| D018 | T13 length-changing `1 -> 10` defeats scalar same-locus writes | 2 | UPDATE axis supporting typed structural replacement | One branch-free runner; update policy owns composition/schedule | Rewrite: real axis extension, not executor split |
| D019 | All parents replace in order; lineage evidence | 2/3 | Ordered parallel-replacement UPDATE | Full old-source coverage, source/child order, newborn deferral | Keep semantics; demote construction-specific class |
| D020 | Total `Sigma -> Sigma+` evidence | 2 | Closed RULE table validator | Complete, alphabet-closed, nonempty rows | Keep |
| D021 | Dynamic order/trace/view evidence | 2/3 | Variable-support ordered DOMAIN plus trace mapping | Sequence order explicit; realization/cut/padding/view separate | Keep; normalize DOMAIN/support vocabulary |
| D022 | T16 rule-major/leftmost matching | 2 | Program-coupled FRONTIER implementation | One authoritative clause list; deterministic priority; no matcher callback | Keep; remove new-class implication |
| D023 | One old span replaced per event | 2 | Ordered replacement UPDATE with `exactly_one` schedule | One snapshot, one selected span, prefix/suffix order | Rewrite as restriction, not separate executor |
| D024 | T16 no-match versus T13/T12 outcomes | 2 | Shared typed outcome envelope | Empty frontier interpreted by program/update policy | Keep |
| D025 | Ordered nonempty literal clauses | 2 | RULE/FRONTIER preset and validator | Clause order/duplicates retained; no invented integer code | Keep |
| D026 | Tag/Post/Wang q/d evidence | 2/3 | Product of named read-width/delete-width roles | Positive widths; strict tag preset pins equality | Keep roles; no separate semantic classes |
| D027 | Prefix delete plus old-tail append | 2 | Ordered structural UPDATE with two anchored replacements | Delete `[0,d)` and append at old endpoint atomically | Rewrite as UPDATE policy/preset, not queue executor |
| D028 | Epsilon in T17, nonempty T13/T16 | 2/3 | Shared word ALPHABET with validator refinements | `Sigma*` carrier; construction-specific nonempty invariants | Keep |
| D029 | Short residue versus reference `{}` history | 2/3 | Outcome plus labeled trace projection | Native residue retained; projection never feeds execution | Keep |
| D030 | Complete bounded prefix table count | 2 | Closed RULE table serialization | Every key present; epsilon allowed; no default/code invention | Keep |

### T19 through T30 (D031-D057)

| Decision | Basis / audit evidence | Class | Smallest reusable base | Required invariants or mapping | Disposition / reopen |
|---|---|---:|---|---|---|
| D031 | Arbitrary-size registers and finite bank | 3/2 | Structured ALPHABET/configuration over register-key support | Natural values exact; keys explicit; no fake capacity | Keep semantics; rename value DOMAIN terminology |
| D032 | Visible program counter selects instruction | 3/2 | Marker/tag or explicit product factor in CONFIGURATION; active-instruction FRONTIER | One counter, valid address/exit profile, immutable program separate | Rewrite; retire required generalized `SingleControl` |
| D033 | Increment/decrement branch effects | 1/3 | Tagged RULE writes through shared atomic UPDATE | Reads and all register/marker writes use one snapshot | Rewrite result names as roles; retire `TransitionControl` requirement |
| D034 | Past-end reference versus explicit exit | 2 | Shared outcome envelope | Quiescent, terminal interpretation, wrap, stop distinct | Keep |
| D035 | Program counts, exits, seeds | 2/3 | Structured program/seed/profile records | Seed independent; target profile explicit; no invented code | Keep |
| D036 | Tree/head-path evidence; `alphabets.md:84-103` | 3 | Recursive tagged ALPHABET with typed occurrence paths/topology | Well-founded tree; equal occurrences distinct; path round-trip | Rewrite prohibition on transparent structured values |
| D037 | Structural pattern/template evidence | 3/2 | Closed RULE AST | Binding scope, duplication/deletion, literal validity | Keep as data, not executor class |
| D038 | One-pass outermost prefix-free matching | 2 | Program-coupled FRONTIER/schedule | Old snapshot, preorder/priority, ancestor suppression, newborn deferral | Keep |
| D039 | Multiple disjoint subtree replacements | 2 | Structural replacement UPDATE on typed paths | Prefix-free targets, exact sources, atomic context preservation | Retain UPDATE variant; retire “fifth executor/law” framing |
| D040 | No-match/fixed form/representations | 2/3 | Shared outcomes plus observers/codecs | Applicable identity remains eventful; views never feed back | Keep |
| D041 | Fully posed multiplicity-preserving geometry | 3/2 | Geometric DOMAIN/support with product labels and bag occurrence identity | Full pose retained, multiplicity material, order nonsemantic | Keep; normalize scalar-carrier terminology |
| D042 | Parent-local affine composition | 2/3 | Closed geometric NEIGHBORHOOD/RULE data | `P o C` order; exact/declared numeric profile explicit | Keep; rename scalar DOMAIN to carrier/profile |
| D043 | Every old occurrence expands to bag children | 2 | Parallel replacement UPDATE with commutative bag combiner | Complete old coverage, consume parents, retain duplicate children/lineage | Keep as UPDATE-axis implementation, not geometric executor |
| D044 | Overlap/order/limit/render evidence | 2 | Observer/run policy | Overlap inert; identity event advances; views separate | Keep |
| D045 | Möbius/inverse-root point variants | 3/2 | Tagged closed RULE forms on point-labeled geometric support | Poles/infinity/branches/multiplicity explicit | Keep semantic profile; no separate executor |
| D046 | Rooted two-port graph versus drawing | 3 | Graph DOMAIN/topology with labeled vertices/ports | Root/ports/cycles/sharing preserved; alpha-renaming lossless | Keep; delete whole-graph-value prohibition |
| D047 | Port paths/exact reach | 2 | Graph NEIGHBORHOOD/access-pattern type | Old snapshot, path order, declared key set | Keep; rename key DOMAIN terminology |
| D048 | Fresh vertices in results | 3/2 | Typed graph replacement writes | Each insertion occurrence fresh; newborns do not fire | Keep |
| D049 | Parallel reroute/create/project | 2 | Graph UPDATE implementation in shared runner | Frozen proposals, injective allocation, directed-root projection, provenance | Retain update policy; retire seventh executor/law framing |
| D050 | Rooted graph BFS codec | 2/3 | Exact serialization/equality mapping | Root/port order preserved; no vertex merging | Keep |
| D051 | Sequential-network evidence gap | 2 | Evidence gate on an UPDATE schedule | No invented anchor/timing/projection order | Keep |
| D052 | Distinct words and exact set layers | 3 | One word CONFIGURATION plus explicit finite powerset/layer lift | Epsilon distinct; equality exact; multiplicity absent; branch provenance retained | Rewrite layer as lossless batch/lift, not top-level executor class |
| D053 | Every overlapping literal match | 2 | Multi-match FRONTIER over T16 access/replacement | All overlaps, alternatives not simultaneous edits, newborn deferral | Keep |
| D054 | Exact child merge across all witnesses | 2/3 | UPDATE lifts one configuration to a finite set of successors | Exact dedupe; all witnesses/dead parents preserved in event trace | Rewrite as successor-set UPDATE, not eighth executor/law |
| D055 | Dead parents, epsilon, empty successor set | 2 | Shared successor/outcome semantics | No-match branch disappears; epsilon remains configuration; empty set distinct | Keep with one-to-many wording |
| D056 | Layer recurrence versus compressed graph | 2/3 | Full branching trace plus derived graph projections | No visited suppression; every witness retained | Keep |
| D057 | Literal restrictions versus other carriers | 2 | Presets/typed axis variants | Reuse only when matching/support/multiplicity commute | Keep |

### T31 through T41 (D058-D087)

| Decision | Basis / audit evidence | Class | Smallest reusable base | Required invariants or mapping | Disposition / reopen |
|---|---|---:|---|---|---|
| D058 | Constraints denote complete model sets without a chosen step | 4 | Declarative relation/model-set category | No invented seed, frontier, successor, repair, or time | Keep nonfit; generalize category beyond T31 |
| D059 | Center-conditioned neighbor-count evidence | 3/2 | Closed local-relation AST on a declared lattice DOMAIN | Complete allowed sets; offsets distinct; no predicate callback | Keep as relation node, not class/executor |
| D060 | Infinite/periodic/window/open scopes | 3/2 | Tagged support presentations/query scopes | Promotion rules explicit; no padding/boundary substitution | Keep |
| D061 | Verification versus search/proof | 1/2 | Generic query/result/certificate envelope | Witnesses reverified; certificates replayed; bounded failure unknown | Keep; normalize value-set terminology |
| D062 | 1D de Bruijn theorem | 2 | Analyzer/certificate preset | Scope limited to proved 1D relation | Keep outside state |
| D063 | Count/oriented/existential evidence | 3/2 | Tagged relation forms in one constraint algebra | Orientation/global-existence roles preserved | Rewrite “separate classes” as variants; T31 handoff reopens |
| D064 | Add/multiply one scalar per step | 2/1 | `t+0D` SimpleProgram with closed unary RULE and same-site write | Exact value carrier explicit; program/seed separate | Rewrite as unary-map presets, shared with T43 |
| D065 | Integer/rational exactness and serialization | 3/2 | Tagged numeric ALPHABET/value carriers and representations | Exact normalization; no implicit float/promotion | Keep; replace numeric DOMAIN terminology |
| D066 | One scalar replacement | 1 | Generic same-locus write and atomic UPDATE | One old read, one validated result; identity event advances | Keep reuse; retire `ArithmeticAssignment` class |
| D067 | Digit views and modular sibling | 2/3 | Observers plus unary-rule/value-carrier preset | Views never feed back; modulus explicit | Keep; no new executor |
| D068 | Closed forms/compilers | 2/3 | Explicit evaluator/representation relation | Requested event trace still one-step faithful | Keep |
| D069 | T34/T35/T43 rule differences | 2 | Shared closed unary RULE algebra on `t+0D` | Predicate/number/digit/map nodes typed; no callback or family switch | Rewrite categorical split; preserve value/schema distinctions |
| D070 | Source exposes indexed accumulated sequence; window map is noninjective | 3/2 | Variable-support sequence CONFIGURATION | Complete prefix and index retained when source state requires them; no hidden history | Keep canonical full-state conclusion; do not mistake future sufficiency for lossless equivalence |
| D071 | Fixed-lag linear recurrences and factorial sibling | 2/3 | Closed sequence NEIGHBORHOOD/RULE forms | Positive lags, seed/checkpoint replay, no dynamic index callback | Keep |
| D072 | Each event appends one term | 2 | Ordered-support UPDATE with endpoint insertion | Old prefix preserved; exact next index; one newborn | Rewrite as shared UPDATE-axis preset, not ninth executor/law |
| D073 | Seed+append log reconstructs prefixes; lag window loses history | 3/2 | Lossless event-log representation; optional noninjective evaluator quotient | `state_at` exact; quotient never replaces full state/trace | Keep (earlier audit proposal to reverse it is rejected) |
| D074 | Repeated term still advances | 2 | Outcome/update policy | Event identity depends on applied rule, not value inequality | Keep; phrase structural change by chosen representation |
| D075 | Analyzers/modular/Ulam relations | 2 | Explicit observers/presets/compositions | No hidden global search or alternate trace | Keep |
| D076 | Stateful sieve versus pure filters/measurements | 4/2 | SimpleProgram for sieve; generic pure-query category for others | No fake transition state for pure definitions | Keep split without proliferating top-level classes |
| D077 | Consecutive divisor stages and cursor | 3/2 | Visible marker/tag/product factor plus stage FRONTIER | Cursor round-trips; composite zero-removal stage still fires | Keep; no separate control class |
| D078 | Remove subset and advance cursor | 2 | Typed subset-removal/product UPDATE in shared runner | Exact hits, no resurrection, retained identity/order, atomic cursor write | Retain UPDATE policy; retire tenth executor/law framing |
| D079 | Figure scope/certification/completion | 2/3 | Tagged seed/support/query/run profiles | Figure keeps 1; math preset starts 2; certification not native halt | Keep; rename candidate DOMAIN to set/support |
| D080 | Measurement conventions | 2/3 | Generic pure measurement/query records | Tuple/sign/zero/repetition conventions explicit | Keep |
| D081 | Ulam first-accepted selection plus append | 2/1 | Program-coupled FRONTIER/RULE feeding shared endpoint UPDATE | Complete prefix read; distinct unordered indices; accepted witness explicit | Keep composition; remove dependency on numbered ninth law |
| D082 | Mathematical function definition has no step | 4 | Closed-function declarative category | Argument definition set, codomain, partiality, branches explicit | Keep nonfit; generalize record beyond T41 |
| D083 | Definition set versus numerical query scope | 2/3 | Tagged function/query scopes | View/evaluator/mesh absent from identity | Keep; reserve DOMAIN for task space/support topology |
| D084 | Point/zero/crossing/etc. queries | 2/3 | Generic tagged query/result envelope | Undefined/failure/completeness/multiplicity/poles explicit | Keep variants, not classes |
| D085 | Structural identity/equivalence/observation | 2/3 | Explicit identity and certified-relation records | Ordered AST and numeric provenance preserved | Keep |
| D086 | Finite sum versus infinite series | 3/2 | Tagged closed definition nodes plus convergence invariants | No hidden truncation/infinity sentinel | Rewrite separate-spec mandate as representation variants |
| D087 | T41 query feeds T42 rewrite | 2 | Typed cross-category composition | Finalized result only; neither embeds other's state/callback | Keep |

### T43 through totalistic reintegration (D088-D118)

| Decision | Basis / audit evidence | Class | Smallest reusable base | Required invariants or mapping | Disposition / reopen |
|---|---|---:|---|---|---|
| D088 | One scalar under one fixed map | 2/3 | `t+0D` SimpleProgram with closed unary RULE | State interval is ALPHABET/value space, not DOMAIN; no history/counter | Rewrite and merge base with T34 |
| D089 | Complete self-read and replacement | 1 | Generic singleton FRONTIER/NEIGHBORHOOD/write/UPDATE | Identity/fixed-point application remains eventful | Keep reuse; names become roles/presets |
| D090 | Strict total self-map versus partial siblings | 2/3 | RULE validator/certificate and tagged outcomes | Replayable invariance proof; no trusted boolean | Keep |
| D091 | Exact/tracked/fixed feedback evidence | 3/2 | Tagged numeric representation and RULE-realization profiles | Every feedback-affecting rounding choice serialized | Keep semantics; avoid multiple top-level state classes |
| D092 | Initial-inclusive orbit; no native cycle halt | 2 | Shared trace/outcome policy | `h` writes gives `h+1` snapshots; equality profile explicit | Keep |
| D093 | Digits/sensitivity/Lyapunov/etc. | 2 | Observer/analyzer records | Never feed execution or prove more than scope | Keep |
| D094 | Identity/equivalence/conjugacy/fast-forward | 2/3 | Explicit relations and codecs | Structural/realized IDs distinct; event provenance not fabricated | Keep |
| D095 | Vector box/torus siblings | 3/2 | Product ALPHABET/value carrier plus topology/equality preset | Simultaneous tuple read/write; quotient semantics explicit | Keep; no vector executor |
| D096 | Continuous-valued cells on a fixed 1D lattice | 1/3 | Discrete `t+1D` DOMAIN with real-interval ALPHABET | Support and value continuity separated; total field inspectable | Rewrite `ContinuousFieldState` as generic field specialization |
| D097 | Affine aggregate then scalar map | 3/2 | Factorized closed local RULE representation | Ordered coefficients/divisor/map and range proof explicit | Keep as RULETYPE variant, not construction class |
| D098 | All sites assign from old local reads | 1 | CA preset of shared runner | Snapshot parallelism; no partial/in-place commit | Keep; remove ten-law inventory |
| D099 | Native support/ring/work/crop | 3/2 | DOMAIN/support/realization/view records | Boundary and finite work never masquerade as native support | Keep |
| D100 | Whole-field numeric realization | 3/2 | Tagged representation/realization profile | Rounding locations and feedback semantics complete | Keep |
| D101 | Initial-inclusive fields and observers | 2 | Shared trace/observer policy | Background/difference/gallery/view never feed rule | Keep |
| D102 | Deterministic/stochastic/block/PDE relations | 2/3/4 | Closed RULETYPE and UPDATE-schedule variants; PDE declarative category | Draws explicit; block schedule typed; no discretization identity | Rewrite blanket separate-construction claim; re-audit unsupported block evidence |
| D103 | General PDE relation lacks canonical step | 4 | Declarative differential-relation/model-set category | No invented time/frontier/successor; specified IVP may derive a SimpleProgram | Keep nonfit; reuse T31/T41 infrastructure |
| D104 | Bound differential syntax | 3/2 | Shared closed expression/function algebra | Variables, derivative multi-indices, codomain, matrices typed | Keep; rename definition-set terminology |
| D105 | Equation/problem/candidate/witness/etc. | 2/3 | Referenced roles and identity layers | Equality never promoted across layers without relation | Keep roles, not unrelated ontologies |
| D106 | Derived IVP flow/admissibility | 2/3 | Certified relation from PDE problem to SimpleProgram | Time order/data/locus/well-posed scope explicit | Keep |
| D107 | Proof-strength results | 1/2 | Generic query/result/certificate envelope | Existence/nonuniqueness/no-solution/unknown not conflated | Keep |
| D108 | Numerical discretization | 2/3 | Explicit representation/approximation relation | Mesh/stencil/integrator/arithmetic/proof claims serialized | Keep |
| D109 | Mathematical/numerical/sample/view scopes | 2/3 | DOMAIN/support plus tagged realization/query/view scopes | Continuous region never replaced by grid/raster | Keep |
| D110 | Solver work/diagnostics/views | 2 | Observer/work records | No hidden mathematical feedback or false certification | Keep |
| D111 | T02 only changes finite alphabet/table data | 1/2/3 | CA preset with arbitrary finite composite ALPHABET | Complete table; same DOMAIN/frontier/neighborhood/update | Keep; explicitly admit tagged/product cells |
| D112 | Table, rank, codec identities | 3/2 | One semantic local function with explicit serialization maps | Complete keys; rank/code round-trip; no fixed-width coercion | Rewrite table denotation versus code identity wording |
| D113 | Mutation/reversibility/search/emulation | 2/3 | Provenance/property/analyzer/representation relations | None becomes state or missing-row behavior | Keep |
| D114 | Rank/valuation/palette roles | 2/3 | Mappings over one ALPHABET/value carrier | Each role explicit; equal shape does not imply same mapping | Keep and add role-vs-class rule |
| D115 | Valuation-sum-table totalistic form | 2/3 | Factorized local RULE representation | Exact valuation, fixed arity, reachable-sum set, complete output table | Keep semantics; not a new executor/class |
| D116 | Compact sum table expands losslessly to exhaustive table | 3/2 | Same denoted local function with two representations | Expansion/compaction commute and compact source identity/provenance retained | Rewrite denial of semantic equivalence; T03 handoff reopens |
| D117 | Same lattice/frontier/read/commit | 1 | Shared CA preset/runner | General radius only parameterizes NEIGHBORHOOD/RULE validation | Keep |
| D118 | T04/T05/T06/T07 and related reducers | 2/3 | Presets, predicates, properties, DOMAIN/NEIGHBORHOOD/RULETYPE variants | No executor flags; every representation/restriction validated | Keep preset ownership; rewrite claim that weighted/histogram/dimension/continuous values imply new construction classes |

### Concrete Counterexample Gate

The class-4 label and every axis extension are justified by behavior that the smaller candidate cannot express faithfully:

| Candidate reuse | Concrete counterexample | Smallest justified response |
|---|---|---|
| Same-site fixed-support assignment UPDATE for T13 | The rule `a -> aa` changes support cardinality in one native event. A scalar write at the old locus cannot preserve both ordered children or their lineage. | Add an ordered block-replacement UPDATE implementation to the existing runner; do not add a substitution executor. |
| Value-only fixed-support assignment UPDATE for T29 | A rule can allocate a fresh vertex and reroute two old ports to it in one event. Relabeling old vertices cannot express fresh identity or the new incidence relation. | Add typed graph writes plus a graph UPDATE implementation to the existing runner; do not add a network executor. |
| Single-successor UPDATE for T30 | From word `aaa` under `aa -> b`, the two overlapping matches yield distinct children `ba` and `ab` in the same native step. Choosing one invents a schedule; merging them into one configuration loses branching. | Lift UPDATE's result from one configuration to a finite set while retaining match witnesses; do not add a multiway runner. |
| SimpleProgram rollout for D058/T31 | The local constraint `x_i != x_(i+1)` denotes a model set but supplies no seed, distinguished firing locus, or next model. Any repair order or successor relation would be invented behavior. | Keep a generic declarative relation/model-set and query category outside rollout. |
| SimpleProgram rollout for D082/T41 | The definition `f(x)=x^2` maps arguments to values but does not say that a value is state or that `f` must be iterated. Choosing an initial argument or feeding outputs back invents an iterated-map program. | Keep a generic closed-function/query category; derive a T43 program only when iteration is explicitly requested. |
| SimpleProgram rollout for D103/T45 | The relation `u_xx + u_yy = 0` on a region, without boundary/initial data or a time variable, denotes possible fields and has no canonical state-to-state step. A mesh relaxation schedule would be an invented numerical method. | Keep a generic differential-relation/model-set category; derive evolution only from an explicitly posed, well-defined problem. |

Two tempting collapses also fail the losslessness gate without justifying new executors. A T37 fixed-lag window is future-sufficient but cannot reconstruct the full source prefix, and `TapeSymbol | HeadState` cannot recover the tape symbol under a head. They remain optional quotients only when their information loss is explicit; neither may replace canonical state.

### Matrix Result

- All canonical step/rewrite stages audited so far fit the same `SimpleProgram` runner. Differences live in DOMAIN/support/topology, ALPHABET/value schema, FRONTIER, NEIGHBORHOOD, RULE result, UPDATE composition/schedule, seed, and validation.
- D058 (constraint/model sets), D082 (uniterated function definitions), and D103 (general PDE relations without a specified evolution problem) are genuine class-4 nonfits because none supplies a canonical successor. Their commonality is declarative relation/query infrastructure, not rollout.
- Multiway rewriting is not a nonfit: its UPDATE returns a finite set of successor configurations and the same runner can iterate or layer that relation.
- No completed transition stage supplies a counterexample requiring a family executor or top-level `SingleControl`, `TransitionControl`, `ArithmeticAssignment`, `MapAssignment`, or construction-named state class.

## Stage Disposition and Revised Goal 2 Handoffs

This table is the authoritative architecture replacement for the reopened stages' former API/Goal 2 conclusions. Their evidence searches, excerpts, construction facts, codecs, trajectories, assets, and observer distinctions remain authoritative unless the row says otherwise.

| Stage | DOMAIN / CONFIGURATION / ALPHABET | FRONTIER / NEIGHBORHOOD | RULE writes / UPDATE | Goal 2 correction |
|---|---|---|---|---|
| T01 | Discrete `t+1D` fixed ordered lattice; Boolean labels | All sites; old left/self/right | One next label per active site; snapshot-parallel replacement | Implement the CA preset through the branch-free runner; fix table count/order, not a T01 executor |
| T02 | T01 DOMAIN with arbitrary finite, including tagged/product, ALPHABET | T01 reuse | Complete local table; same UPDATE | Generalize alphabet/table validation and bigint codec; no rollout branch |
| T03 | T01 DOMAIN; finite alphabet plus explicit numeric valuation | Radius/offset parameter; exact equal-weight sum view | Compact sum table and exhaustive expansion denote the same local RULE; T01 UPDATE | Add a factorized RULETYPE/codec mapping, not a T03 engine or identity split |
| T04 | Exact `k=3,r=1` T03 data | T03 reuse | T03 reuse | Strict preset only; finish independent asset repair |
| T05 | Exact finite `k>=4,r=1` canonical T03 data | T03 reuse | T03 reuse | Strict preset only |
| T09 | Discrete `t+1D` line; `Plain(bit) | Active(bit)`; exactly one active tag | Unique active tag; physical left/self/right | Native `(new_bit,direction)` lowers to source value write plus tag movement; atomic UPDATE | Add composite alphabet, tag-selecting frontier, typed two-write result/lowering, invariant checks; no control class/mobile executor |
| T12 | Discrete `t+1D` unbounded tape; `Plain(sigma) | Head(q,sigma)`; exactly one head | Unique head tag; source `(q,sigma)` for the native decision plus destination label for lossless structural lowering | Native `(q_next,sigma_next,direction)` writes symbol and moves tag while preserving destination symbol; atomic UPDATE | Reuse T09 axes with payload tag, total sparse field, terminal outcome; no `SingleControl`/Turing executor |
| T13 | Discrete variable-support `t+1D` word; finite symbol labels | Every old occurrence; self symbol | Block replacement per occurrence; ordered snapshot-parallel concatenate UPDATE | Add ordered replacement UPDATE policy within runner; no substitution executor |
| T16 | T13 word configuration | Rule-major/leftmost match; exact matched span | One replacement block; exactly-one splice UPDATE | Add program-coupled frontier and schedule restriction over ordered replacement |
| T17 | Discrete variable-support `t+1D` word | Applicable prefix; required prefix access with separate read/delete widths | Appendant plus consume extent; atomic prefix-delete/old-tail-append UPDATE | Add prefix selector/access and anchored ordered update preset; no tag executor |
| T19 | Discrete `t+0D` task with explicit register/instruction topology; natural values plus visible program marker/product factor | Marked active instruction; referenced registers | Tagged register and marker writes; atomic UPDATE | Add named-key/marker labels, instruction frontier, reference access; no generalized control or register executor |
| T20 | Discrete `t+0D` task with explicit recursive tree topology and tagged expression labels | Ordered maximal prefix-free matches; matched subtrees/bindings | Replacement subtrees; atomic prefix-free structural UPDATE | Add tree topology/path selectors and closed pattern/template rules inside runner; no symbolic executor |
| T27 | Canonical continuous-coordinate `t+2D` geometric support; prototype/pose products in a multiplicity-preserving bag | Every old occurrence; self prototype/full pose | Parent-local child occurrences; parallel bag-replacement UPDATE | Add geometric support/value schemas and bag combiner policy; no geometric executor |
| T29 | Non-Euclidean graph topology represented as a `t+0D` structured task; rooted port-labeled graph | Old vertices; port-path/reach views | Direct/fresh reroutes; create/rewire/root-project UPDATE | Add graph domain/topology, structural access, and graph update policy within runner; no network executor |
| T30 | Discrete `t+1D` word configuration with finite successor-set semantics | Every overlapping literal match; matched span | One child per match; UPDATE returns exact finite set of successor configurations | Generalize runner result to configuration(s); preserve witness trace; no multiway executor |
| T31 | Static discrete 1D/2D labeled support; local relation denotes a model set | Not applicable | No canonical write/UPDATE | Implement generic declarative relation/query/certificate category, not rollout |
| T34 | Discrete `t+0D` singleton with exact numeric value carrier | Unique locus; self | Closed add/multiply unary result; same-site UPDATE | Use generic unary RULE and assignment; no scalar-domain or arithmetic executor class |
| T37 | Discrete variable-support `t+1D` indexed sequence; complete prefix visible | Next endpoint; declared lag/index access | One next term; endpoint-append UPDATE | Reuse ordered structural update and preserve full prefix/event log; no recursive executor |
| T39 | Discrete ordered candidate support with visible stage marker | Current-stage hit loci; membership/access witnesses | Remove selected survivors and advance marker atomically | Add candidate-set selectors and typed subset/marker update policy; pure filters/measurements stay queries |
| T41 | Continuous argument-space definition with no stepwise configuration | Not applicable | No canonical write/UPDATE | Implement generic closed-function/query/result category, not rollout |
| T43 | Discrete `t+0D` singleton with real/represented value carrier | Unique locus; self | Closed unary map result; same-site UPDATE | Reuse T34 unary SimpleProgram; self-map/numeric representations are validation/profile data |
| T44 | Discrete `t+1D` lattice with continuous-valued ALPHABET | All sites; local stencil | Factorized aggregate/map next label; snapshot-parallel UPDATE | Reuse CA runner with new value carrier and RULETYPE; deterministic profiles are presets |
| T45 | Continuous independent-variable support; differential relation/model set unless an IVP is supplied | Not applicable natively | No canonical write/UPDATE; certified IVP may derive one | Reuse declarative relation/function/query infrastructure; discretization is an explicit relation |

### Minimal Goal 2 Runner Contract

```text
step(program, configuration):
    validate(configuration, program.configuration_schema.invariants)
    active = program.frontier.select(configuration, program.rule)
    reads = program.neighborhood.read(configuration, active)
    writes = program.rule.apply(active, reads)
    next = program.update.apply(configuration, active, writes)
    validate_each(next, program.configuration_schema.invariants)
    return next
```

`next` is one configuration for deterministic programs and a finite typed set for multiway programs. Polymorphism occurs through the typed axes stored in the specification; the runner contains no catalog/family switch. RULE and UPDATE implementations are closed data/evaluators, never unrestricted callbacks. A preset returns an ordinary `SimpleProgram` specification.

### Current-Code Migration Boundary

| Current area | Smallest Goal 2 revision |
|---|---|
| `alphabets.py` | Add finite product/tagged-union and structured value schemas with invariant-aware codecs; keep role maps explicit |
| `loci.py` | Generalize finite coordinate-only selectors to typed loci/occurrences/matches while retaining existing geometric selectors |
| `frontiers.py` | Restore rule-firing semantics and add all-occurrence, unique-tag, match, prefix, endpoint, graph, and candidate selectors as typed implementations |
| `neighborhoods.py` | Generalize offsets to typed access patterns: spans, prefixes, keys, tree paths, graph paths, and self/product projections |
| `rules.py` | Return closed typed writes/replacements; add composite-table, structural-rewrite, unary-map, and factorized local-rule forms without callbacks |
| UPDATE specification | Introduce one typed UPDATE axis for snapshot assignment, ordered replacement, structural replacement, graph replacement, bag combination, subset removal, and successor-set lift; these are policies used by one runner |
| `specs.py` | Replace string-family construction branches with structural decoders/registries for the typed axes; seeds and run requests remain separate |
| `rollout.py` | Replace family branches with the branch-free runner; batching/realization adapts configurations and traces without changing semantics |
| outcomes/traces | Preserve complete configurations, invariant evidence, typed writes, branch witnesses, and stop/error reasons before downstream encoding |

## Completion Gate

- [ ] D009-D014 have final classifications and revised consequences.
- [ ] Every completed D000-D118 decision appears in the audit matrix, individually or in an explicit lossless grouped row with per-decision disposition.
- [ ] Every completed stage's state/control/frontier/read/result/update/executor/API claims have been checked from first principles.
- [ ] Each class-4 abstraction includes a concrete counterexample against the smallest reusable base.
- [ ] T09/T12 and every affected dependent stage have revised stage results and Goal 2 handoffs.
- [ ] `0-plan.md`, `evidence-index.md`, and `design-ledger.md` agree exactly.
- [ ] Fresh independent review, Markdown-fence checks, `git diff --check`, and scope checks pass.
- [ ] Only after every gate passes may T06 or prior asset repairs resume.
