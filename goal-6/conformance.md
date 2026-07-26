# Goal 7 Conformance Contract

Status: **Stage 6 design contract**

This document turns the completed Goal 5 pressure selection into one
implementation-facing conformance plan. It tests the architecture in
[architecture.md](architecture.md) and the catalog in
[catalog-migration.md](catalog-migration.md); it does not create another
taxonomy, runtime ontology, or executor.

Goal 5 remains authoritative for family identity. The fixtures below are tiny
closed examples chosen to expose reusable mechanics. Catalog identity is never
an input to `apply`.

## Contract notation

- `C0` is one immutable input configuration.
- `W` is the resolved writable capability envelope.
- `R` is the resolved readable view from the same snapshot.
- `RC` abbreviates `RuleComplete`.
- `AC(o, d, s)` abbreviates `ApplicationComplete` with exact
  outcome-atom, replacement-derivation, and distinct-successor cardinalities.
- A disposition is total over `W`: every unmentioned existing capability below
  is explicitly `Preserve`, every unused fresh capability is explicitly
  `Absent`, and everything outside `W` is universally preserved.
- Unless a fixture says otherwise, all three measure views are `Absent`.

The paper-execution gate is always:

```text
validate five closed descriptors and their compatibility
→ freeze and validate C0
→ resolve W and R from the same snapshot
→ denote and validate one complete Rule outcome space
→ bind fresh identities
→ reconstruct every derivation independently from C0
→ validate successors
→ quotient only after retaining witnesses
```

No fixture authorizes commit-time scheduling, collision repair, endpoint
selection, solver execution, random draws, or catalog dispatch.

## PX01 — Coupled source, destination, and field writes

### F031 mobile head

```text
C0:
  tape[-1] = 0
  tape[ 0] = Head(q, 1)
  tape[ 1] = 0

closed transitions:
  (q, 1) → (p, 0, Left)
  (q, 1) → (p, 0, Right)
```

`W = {-1, 0, 1}` contains the tagged source and both possible destinations.
`R` is the keyed old-snapshot triple
`{-1: 0, 0: Head(q, 1), 1: 0}`.

`RC` has two witnessed `Advanced + Continue` derivations:

- left: replace source `0` with plain `0`, replace `-1` with `Head(p, 0)`,
  preserve `1`;
- right: replace source `0` with plain `0`, preserve `-1`, replace `1` with
  `Head(p, 0)`.

Application yields `AC(2, 2, 2)`. Each alternative is reconstructed from the
same old tape and contains exactly one head. Commit never recovers an omitted
destination value or performs a second movement pass.

### F007 coupled field extension

For `field=(2,1,0)` with the mobile marker at site `1`, let the closed field
law produce `(1,1,1)` and the mobile law move right and destructively zero its
destination. `W` contains the complete next-field slice plus every possible
marker source, destination, and destructive target; `R` contains the old field
stencils and destination views. One derivation commits the final field
`(1,1,0)` and marker at `2` together. Splitting the field pass from the marker
pass would fail this fixture.

Exact invariant:

```text
every possible source/destination/effect target ∈ W
∧ every atom has one conflict-free total disposition
∧ all effects observe one old snapshot
∧ outside(W) is unchanged
```

## PX02 — Variable support and structural replacement

### F029 graph birth, deletion, and interface repair

```text
C0:
  nodes = {a, b, c}
  edges = {a—b, b—c}
  selected match = b with its two external interfaces

replacement:
  a—b—c  →  a—x—y—c
```

Existing capabilities in `W` are `b`, `a—b`, and `b—c`. Fresh capabilities
are local keys `x`, `y`, `a—x`, `x—y`, and `y—c`. `R` contains the matched
occurrence, its labels and incident edges, and the external endpoints and
ports `a` and `c`. In this fixture each edge record owns its endpoint
incidence, so replacing edge records leaves the external endpoint identities
unchanged. If a carrier stores mutable port/incidence slots separately, those
slots must also occur in `W` with explicit total dispositions.

`RC` has one `Advanced + Continue` derivation that explicitly deletes the
three old components, creates all five fresh components, and carries witness
`match(node=b)`. Application binds `x` and `y` from input identity, Rule
identity, witness, interface, namespace, and local key, then yields
`AC(1, 1, 1)`.

Required variable-support variants:

| Family | Tiny closed execution | Required result |
|---|---|---|
| F017 | Word `1101`, delete width `2`, production `11 → 10` | `W` contains the consumed occurrences, end/control, and fresh suffix; `R` reads the old prefix/tail; one atom produces `0110` with surviving occurrence identity preserved |
| F038 | Old generation `AB`, productions `A → AB`, `B → ε` | `W` contains all old occurrences and all possible offspring; `R` reads each old item; one atomic generation deletes old items, creates ordered offspring, and does not expose newborns to the same pass |
| F040 | Two compatible graph matches selected under the closed overlap law | `R` exposes both old matches and ports; `W` covers every deleted, preserved-interface, and fresh component; Rule—not commit—returns the resolved parallel patch |
| F052 | Tree `add(x, 0)` with pattern `add(v, 0) → v` | `R` contains subtree, binding, and scan/nonoverlap context; `W` covers the removed structure and retained occurrence; one structural result produces `x` without an implicit tree repair |

Exact invariant:

```text
all birth, deletion, incidence, order, and interface effects are explicit
∧ outside structure preserves semantic identity
∧ fresh identity is traversal/materialization independent
∧ commit performs no cascade, overlap choice, or port repair
```

## PX03 — Global and nonlocal reads

### F054 weighted history aggregate

```text
C0:
  histories = {h0, h1}
  weight(h0) = +1
  weight(h1) = -1
  amplitude = Unset
```

`W = {amplitude}`. `R` is the complete admissible history space plus its exact
action and weight values. `RC` has one `Advanced + Stop(Completed)`
derivation replacing `amplitude` with exact complex zero, and application
yields `AC(1, 1, 1)`. A zero value is a successor, not an empty relation.

Required nonlocal variants:

| Family | `C0`, `R`, and `W` | Required result |
|---|---|---|
| F018 | Unit edge with one fixed and one unknown real coordinate; `R` is the complete mesh and metric constraint, `W` the movable coordinate | Return the exact embedding relation; an external relaxation method is not part of Rule |
| F019 | Equation `x + y = 3` over a closed exact domain; `R` contains all terms/domain/knowns, `W` the complete unknown tuple | Return all exact assignments or a sound-and-covering intensional relation |
| F020 | Three vacant candidate sites with globally computed scores; `R` contains complete scoring/occupancy geometry, `W` all candidate and induced field targets | Choose the unique/tied winner under the closed tie law and commit one coupled placement |
| F028 | Two unknown bits with overlapping factors and a normalization request; `R` contains every factor scope and normalization domain, `W` unknowns plus result slots | Return the complete weighted/feasible result, never a locally normalized approximation |
| F036 | Store `{0, 2}`, query `1`; `R` contains the reachable store/index and metric, `W` traversal/incumbent/result | Return two tied nearest witnesses and one result relation without assuming geometric locality |

Exact invariant:

```text
reads(Rule) ⊆ R
∧ effects(Rule) ⊆ W
∧ W grants no implicit read
∧ Rule has no hidden access to C0 outside R
```

## PX04 — Zero, one, many, and successor quotient

### F019 exact cardinality

Use one relation over `ℤ/3ℤ`:

```text
unknown x
equation x² = rhs (mod 3)
W = {x}
R = {rhs, domain ℤ/3ℤ, equation}
```

| Seed variant | Complete Rule result | Application result |
|---|---|---|
| `rhs=2` | One `NoSuccessor(Terminal(NoSolution))` with complete three-value truth-table certificate | `AC(1, 0, 0)` |
| `rhs=0` | One witnessed `Advanced + Stop`, `Replace(x, 0)` | `AC(1, 1, 1)` |
| `rhs=1` | Two witnessed `Advanced + Stop` atoms, `Replace(x, 1)` and `Replace(x, 2)` | `AC(2, 2, 2)` |

### F034 diamond

For input word `a`, two distinct `(rule, match, parent)` witnesses both
rewrite to `b`. `RC` has two derivations. Application records both applied
derivations before grouping, then yields `AC(2, 2, 1)` with one successor
whose fiber contains both witnesses.

Required relation variants:

| Family | Tiny closed execution | Required distinction |
|---|---|---|
| F015 | One-element domain with either a satisfiable table axiom or `P(0) ∧ ¬P(0)` | Exact models are `Advanced + Stop`; no model is certified `Terminal(NoSolution)`, not invalidity |
| F030 | Two unknown bits constrained by XOR `= 1` | Two complete jointly satisfying configurations; no per-locus independent commit |
| F041 | `du/dx = 0` on `[0,1]` without boundary value | Sound-and-covering intensional constant-field relation; never fabricate terminality from unenumerated support |

Exact invariant:

```text
certified zero has a typed NoSuccessor atom and coverage evidence
∧ an Undetermined intensional relation is not certified zero
∧ outcome, derivation, and distinct-successor cardinalities remain separate
∧ quotienting retains complete derivation fibers
```

## PX05 — Continuous evolution and relations

### F006 exact event

```text
C0:
  interval = [0,1]
  x = 1/4
  v = -1
  t = 0
  event = Unset
```

`W = {x, v, t, segment, event}`. `R` contains the state and exact interval
geometry; the flow and reflection laws are closed Rule data. The intrinsic
earliest hit is the left boundary at `τ=1/4`. `RC` has one
`Advanced + Continue` derivation replacing
`x→0`, `v→+1`, `t→1/4`, the exact segment, and `event→HitLeft`.
Application yields `AC(1, 1, 1)`.

### F037 maximal flow

For `dx/dt = 1`, `x(0)=0`, and no closed duration or event selector, `W`
contains the solution/result slot and `R` the exact initial state and any
visible parameters/event predicates. The vector field is closed Rule data.
Rule returns the maximal solution object `x(t)=t` as
`Advanced + Stop(Completed)`. An external query may evaluate it at `t=2`;
base application may not silently choose that endpoint.

### F041 intensional field

For `du/dx=0` on `[0,1]` without boundary value, `W` is one capability `u`
whose payload is the complete unknown field. `R` contains the readable
domain/side data and differential-germ observations/views. The differential
relation is closed Rule data. `RC` denotes
`Replace(u, constant_field(c))` for every exact real `c`, with
`Many(uncountable)` support and no inferred probability law.

Exact invariant:

```text
an endpoint exists only when closed semantics or an intrinsic event selects it
∧ numerical integration/meshing is a qualified realization, not Rule or commit
∧ continuous or intensional W need not be enumerated
∧ no top-level time axis is required
```

## PX06 — Probability laws, realization, and replay

### F050 mixed stochastic search law

```text
C0:
  incumbent x = 0
  proposal counter k = 0
  objective = (x - 1)²
```

`W = {x, k}`. `R` contains the incumbent, exact objective, constraints, and
closed proposal/acceptance law. `RC` is a normalized finite law over:

- mass `1/2`: replace `x→1`, `k→1`, `Advanced + Continue`;
- mass `1/4`: preserve `x`, replace `k→1`, `Advanced + Continue`;
- mass `1/4`: `NoSuccessor(Terminal(NoProposal))`.

Application yields `AC(3, 2, 2)`. Its applied-atom measure has mass `1`;
the successor submeasure has mass `3/4`; the no-successor submeasure has mass
`1/4`. Neither submeasure is renormalized.

Required stochastic variants:

| Family | Tiny closed execution | Required result |
|---|---|---|
| F016 | Aggregate at `0`, walker at `2`, equal law over first-contact site `1` and free site `3` | `W` includes source, every destination, attachment, and relaunch target; Rule denotes the law, and a keyed external realization records the selected microtrajectory |
| F044 | Observations `A,A,B` with a closed estimator and generation request | Fit parameters are visible state; Rule denotes a normalized generated-path law after fitting, not a sampled path |
| F046 | Two labeled nodes, each independently choosing either node as successor | Rule explicitly denotes the four complete functional graphs with product mass `1/4`; realization is not one engine draw per traversal-ordered node |

Exact invariant:

```text
probability law ≠ draw
∧ law identity is independent of replay key and worker/traversal order
∧ a draw requires external replay evidence
∧ successor/no-successor mass remains tagged and unrenormalized
∧ scores, amplitudes, and weights confer no sampling authority
```

## PX07 — Mutable program text as configuration state

### F051 self-modifying stored-program machine

```text
C0:
  pc = 0
  memory[0] = WriteHaltSelf
  memory[1] = Data(7)
```

`WriteHaltSelf` overwrites its own instruction with `Halt` and leaves `pc=0`.
`W = {pc, memory[0]}`; `R` contains the fetched opcode and decoded target.
`RC` has one `Advanced + Continue` derivation preserving `pc` and replacing
`memory[0]→Halt`, so application yields `AC(1, 1, 1)`. Applying the same
immutable outer Rule again yields `NoSuccessor(Terminal(Halt))`.

For F035, use a cell carrier plus a visible local rule-table entry. A trigger
atomically updates the selected cells and replaces that table entry; the
closed interpreter remains the immutable outer Rule.

Exact invariant:

```text
program text and mutable rules ∈ C0 and Alphabet
∧ every mutation target ∈ W and every dependency ∈ R
∧ SimpleProgram.rule is immutable
∧ application performs no machine or mutable-rule family dispatch
```

## PX08 — One-shot evaluation

### F021 hash lookup

```text
C0:
  table.bucket[0] = [("a", 7)]
  query = "a"
  result = Unset
  phase = Query
  hash_fold[v1]("a") = 0
```

For read-only lookup, `W = {result, phase}` and `R` contains the query,
reachable collision path, exact key equality, and the output of the closed,
versioned `hash_fold` descriptor. `RC` has one
`Advanced + Stop(Completed)` derivation replacing `result→Hit(7)` and
`phase→Done`. Application yields `AC(1, 1, 1)`.

Required one-shot variants:

| Family | Terminal-ready tiny execution | Expected result |
|---|---|---|
| F011 | Current enumerated candidate `4` satisfies the closed query predicate | Write the first witness and return `Advanced + Stop`; failure to find one under a bound is not a negative denotation |
| F013 | Input `AAA`, maximal-run grammar | Emit record `(A,3)` and finish this closed input; the epsilon output, if valid, would still be one successor |
| F014 | One CNOT gate over `(1,0)` | Replace addressed wires and cursor, `Advanced + Stop`; PX09 checks the gate algebra |
| F015 | Complete finite-model relation over a one-element domain | Each exact model is a stopped successor; a certified empty model set is typed terminal zero |
| F025 | One observed local step with one exact predecessor | Return the witnessed reconstruction once; branch/prune work, if represented, is visible state |
| F036 | Store `{0,2}`, query `1` | Return two tied result witnesses and stop; an empty store is typed exact zero, not invalid |
| F045 | Observed `11`, surrogate `10`, closed `SumBits` program descriptor, empty evaluator frames, phase `EvaluateObserved` | Use the Rule-owned evaluator and visible work state below; external resource/realization limits cannot alter the denotation or closed replicate count |

For F045, `SumBits` is closed Rule data, not a nested `SimpleProgram`
callback. The same immutable evaluator Rule:

1. reads observed `11`, writes result `2`, and advances the visible phase;
2. reads surrogate `10`, writes result `1`, and advances to calibration; then
3. compares the recorded results, writes the calibrated decision, and returns
   `Advanced + Stop(Completed)`.

Each application resolves only that phase's work/result/control `W` and
input/frame/result `R`, returns finite `ExactlyOne`, and yields
`AC(1, 1, 1)`. If evaluation needs more microsteps, its frames and
continuations remain in `C`; Rule never calls `apply` recursively. Provenance
joins both results to the same program descriptor and their respective input.
This closed-code/evaluator contract is the library meaning of Goal 5's
arbitrary executable program; it does not narrow the family to a fixed
statistic language or authorize callbacks.

Exact invariant:

```text
Stop may accompany a real successor
∧ one application can be the complete use of a program
∧ no fake trajectory field, second state, or mandatory rollout is introduced
∧ timeout/resource limits do not fabricate Rule outcomes
```

## PX09 — Fixed gate networks

```text
C0:
  wires x=1, y=0
  gate[0] = CNOT(control=x, target=y)
  cursor = 0
```

`W = {x, y, cursor}`. `R` contains the addressed old wire values, cursor, and
fixed tagged gate descriptor. `RC` has one `Advanced + Stop(Completed)`
derivation replacing `x→1`, `y→1`, and `cursor→Done`; application yields
`AC(1, 1, 1)`.

The suite repeats the same generic path for:

- compare-exchange over an ordered-value Alphabet;
- reversible Boolean gates over bit tuples; and
- a unitary gate over an exact complex-amplitude vector.

The representations and gate laws remain different tagged descriptors.
Only an explicit terminal measurement supplies a probability law.

For the terminal-measurement case, use exact qubit state
`|+⟩=(|0⟩+|1⟩)/√2` and computational-basis measurement. `W` contains the
measured register, classical result, and cursor; `R` contains the complete old
amplitude vector and tagged measurement gate. `RC` is a normalized finite law
with two total `Advanced + Stop(Completed)` atoms of mass `1/2`, one for each
collapsed state/result. Application yields `AC(2, 2, 2)` before any external
realization chooses an atom.

Exact invariant:

```text
fixed wiring and schedule do not depend on runtime values
∧ every addressed wire has one atomic disposition
∧ different gate algebras are not silently coerced
∧ generic application is unchanged across the algebras
```

## PX10 — Distinct codec mechanics

### F057 prefix blocks

For input block `A` and prefix tree `A→0, B→10, C→11`, `W` contains the
fresh output bit and cursor, while `R` contains the current block and complete
tree. `RC` is finite `ExactlyOne`: one `Advanced + Stop` atom has a total
disposition that creates bit `0` and advances the cursor. Application yields
`AC(1, 1, 1)`.

### F058 nested interval

For input `AB`, `P(A)=P(B)=1/2`, interval `[0,1]`, and cursor `0`, `W`
contains the shared interval and cursor. `R` contains the next symbol and
cumulative partition. The first `RC` is finite `ExactlyOne`; its total
`Advanced + Continue` disposition replaces the interval by `[0,1/2]` and
advances the cursor, yielding `AC(1, 1, 1)`. The second application refines
that same interval to `[1/4,1/2]`; its finite `ExactlyOne` `RC` has a total
`Advanced + Stop(Completed)` disposition that sets the cursor to `Done`, and
it also yields `AC(1, 1, 1)`. The coding probabilities do not create a Rule
probability law.

Required codec variants:

| Family | Tiny exact case | Distinct mechanics asserted |
|---|---|---|
| F013 | `AAABB → [(A,3),(B,2)]` | Maximal homogeneous extent and self-delimiting records |
| F059 | `ABAB → literal(A), literal(B), ref(offset=2,length=2)` | Prior-history search and pointer-copy reconstruction |
| F060 | Uniform `2×2` array | One region-tree leaf; a nonuniform array creates explicit child regions |
| F061 | Vector `(1,1)` under exact two-vector Walsh basis | Global projection yields exact coefficients `(1,0)`; any quantization is explicitly lossy |
| F062 | Samples `(1,2,3)` with previous-sample predictor | Visible model/history yields residuals `(1,1,1)` and exact reconstruction |
| F063 | `101 XOR 011 = 110` | Aligned generator/cursor state is explicit; the same transform returns `101` |

Exact invariant:

```text
record, tree, interval, history, region, basis, predictor, and XOR state
produce distinct W/R/Rule skeletons
∧ shared purpose (“codec”) creates no codec executor
∧ exact inverse-on-image and declared lossy profiles remain distinguishable
```

## PX11 — Shared priority and injury

```text
C0:
  approximation O has default 0 and no explicit O[0]
  P0 = Ready, priority 0
  P1 = Running, priority 1, use={O[0]=0}
  scheduler.next = P0
```

P0's diagonal requirement enumerates `O[0]=1`, invalidating P1's use.
`W` contains fresh `O[0]`, both requirement states, P1's work record, and
scheduler state. `R` contains the selected runs, finite approximation, use,
and priority bookkeeping.

`RC` has one witnessed `Advanced + Continue` derivation that creates
`O[0]=1`, marks P0 satisfied, marks P1 injured, resets P1's work, and advances
the scheduler. Application yields `AC(1, 1, 1)`.

Exact invariant:

```text
shared write and every induced injury commit atomically
∧ fairness, priority, and scheduler are visible state or closed Rule data
∧ application neither discovers injury nor chooses the next requirement
```

## PX12 — Executable construction versus observer/interface role

### F004 executable causal transform

```text
C0:
  trace/e0 writes x=1
  trace/e1 reads x and writes y
  cursor = trace/e1
  producer[x] = causal/e0
  causal graph already contains causal/e0
```

`W` contains fresh graph node `causal/e1`, fresh edge
`causal/e0→causal/e1`, `producer[y]`, and cursor/end control. `R` contains
trace event `trace/e1`, its read set, and the current producer of `x`. One
`Advanced + Stop(Completed)` derivation creates the scoped graph node and
edge, updates `producer[y]→causal/e1`, and finishes. Application yields
`AC(1, 1, 1)`. Trace-event and causal-graph namespaces are distinct, so the
fresh graph identity does not collide with its source record.

F045 is also executable: surrogate generation, Rule-owned closed evaluation,
visible evaluator work, aggregation, and calibrated decision have explicit
writable state and an invariant result commit. PX08 proves that this needs no
recursive `apply`.

The negative half is intentional:

- F010's encode/evolve/decode interface has no family-owned `W`, `R`, `RC`, or
  `AC`; it is tooling around an unchanged target.
- F042's percolation-connectivity observation reads a completed sample but has
  no construction frontier or transition result.

A concrete encoder, decoder, or analyzer with its own state and invariant
commit can be an ordinary program—normally in `media`—without turning either
role entry into a family.

Exact invariant:

```text
an executable family owns an invariant semantic commit
∧ a pure wrapper/property observer gains no constructor merely for naming
∧ RoleEntry metadata is callable-free and never participates in apply
```

## Single-pass 60-family audit join

This is a coverage join to the canonical catalog matrix, not a replacement for
its definitions. Every SPF appears in exactly one primary pressure partition.
Secondary joins below exercise deliberate cross-cutting obligations.

| Primary fixture | Canonical families |
|---|---|
| PX01 coupled writes (11) | SPF001/F001, SPF003/F003, SPF007/F007, SPF008/F008, SPF011/F012, SPF021/F022, SPF030/F031, SPF032/F033, SPF045/F048, SPF050/F053, SPF052/F055 |
| PX02 variable structure (11) | SPF002/F002, SPF005/F005, SPF016/F017, SPF022/F023, SPF023/F024, SPF025/F026, SPF028/F029, SPF031/F032, SPF037/F038, SPF038/F040, SPF049/F052 |
| PX03 nonlocal reads (7) | SPF017/F018, SPF019/F020, SPF027/F028, SPF035/F036, SPF040/F043, SPF046/F049, SPF051/F054 |
| PX04 zero/one/many (6) | SPF014/F015, SPF018/F019, SPF024/F025, SPF026/F027, SPF029/F030, SPF033/F034 |
| PX05 continuous (3) | SPF006/F006, SPF036/F037, SPF039/F041 |
| PX06 stochastic (5) | SPF009/F009, SPF015/F016, SPF041/F044, SPF043/F046, SPF047/F050 |
| PX07 mutable program state (2) | SPF034/F035, SPF048/F051 |
| PX08 one-shot (3) | SPF010/F011, SPF020/F021, SPF044/F047 |
| PX09 fixed gates (1) | SPF013/F014 |
| PX10 codecs (8) | SPF012/F013, SPF054/F057, SPF055/F058, SPF056/F059, SPF057/F060, SPF058/F061, SPF059/F062, SPF060/F063 |
| PX11 priority (1) | SPF053/F056 |
| PX12 observer boundary (2) | SPF004/F004, SPF042/F045 |

The primary counts sum to 60, with no hole or duplicate. Required secondary
joins are:

- SPF018/F019 also runs PX03;
- SPF039/F041 also runs PX04; and
- SPF012/F013, SPF013/F014, SPF014/F015, SPF024/F025, SPF035/F036,
  and SPF042/F045 also run PX08.

F010 and F042 remain the two Goal 5 close roles and have no SPF. T08 is the
separate retired Seed role. Neither set is smuggled into the executable count.

For each primary row, `test_family_coverage.py` must:

1. call the exact canonical constructor with one closed representative
   argument set;
2. assert the return value is an ordinary five-field `SimpleProgram`;
3. recursively validate descriptor closure and cross-field compatibility;
4. join its SPF, F provenance, home, and source/pressure references to the
   metadata-only entry; and
5. run the named fixture assertion through the same generic `apply` or, when
   the complete result is intensional, through the same denotational
   application contract.

This is one parameterized mechanics test, not 60 executor implementations.

## Reusable Goal 7 test suites

The following target layout is normative by responsibility, not by exact
helper spelling:

```text
tests/conformance/
├── helpers.py
├── test_program_boundary.py
├── test_descriptor_closure.py
├── test_validation_phases.py
├── test_atomic_application.py
├── test_outcome_cardinality.py
├── test_probability_replay.py
├── test_fresh_identity.py
├── test_witness_quotient.py
├── test_serialization_contract.py
├── test_representation_commutation.py
├── test_catalog_expansion.py
├── test_native_generic_equivalence.py
├── test_import_and_dispatch.py
├── test_observer_boundary.py
└── test_family_coverage.py
```

Shared assertions compare semantic records, not renderings:

```python
assert_closed_descriptor(value)
assert_full_application_equal(left, right)
assert_no_authoritative_commit(result, original)
assert_canonical_roundtrip(value)
assert_representation_commutes(representation, native, represented, source)
assert_catalog_expansion(public_constructor, canonical_constructor, arguments)
```

### CT01 — Exact five-field boundary

```python
assert tuple(field.name for field in fields(SimpleProgram)) == (
    "seed",
    "alphabet",
    "frontier",
    "neighborhood",
    "rule",
)
assert type(ca.catalog.eca(rule=30)) is SimpleProgram
```

Reject stored semantic sidecars or receipts for configuration, domain,
topology, boundary, scheduler, solver, RNG, time, trajectory, update/result
policy, observer, catalog identity, or invoked constructor. Rollout horizon and
replay coordinates remain invocation data.

### CT02 — Descriptor closure and compatibility

For every component produced by all 60 canonical constructors, assert stable
tag/version, exact fields, canonical encoding, bound references, explicit
exactness, local invariants, no opaque callable, and no ambient entropy.

Program construction must establish:

```text
Seed output unifies with C
∧ Seed values conform to Alphabet
∧ Frontier and Neighborhood accept that C
∧ Rule accepts exactly their R/W join
∧ reads(Rule) ⊆ Neighborhood
∧ effects(Rule) ⊆ Frontier
∧ representation/exactness/entropy profiles agree
```

Negative generated cases independently violate each clause and must fail at
construction or at the exact unresolved conformance boundary—never by
family-name lookup.

### CT03 — Validation phases and no-commit failure

Use private phase-handler spies or sentinel failures around ordinary closed
test descriptors, not stateful/logging descriptors or a public observer
argument, to prove the phase order:

```text
Program → Input → Frontier → Neighborhood → Join → Rule denotation
→ Result validation → Fresh binding → Commit → Successor → Quotient/measure
```

For one fault generated at every phase, assert later phases do not execute,
the immutable input is unchanged, no authoritative successor/cardinality is
published, and the canonical fault names the first failing generic phase. A
finite Rule space containing one valid and one invalid atom rejects as a
whole.

### CT04 — Atomic application and preserve-outside

Run PX01 and PX02 plus generated overlap, missing-disposition, unauthorized
target, conflicting-write, and invalid-successor cases. For every successful
derivation:

```text
successor|outside(W) = C0|outside(W)
successor|inside(W) = reconstruction(C0, total_disposition, fresh_bindings)
valid_C(successor)
```

Commit may not choose a schedule, resolve a collision, cascade a deletion,
invent a default, or discard a bad branch.

### CT05 — Outcome and cardinality algebra

Run PX04 and PX08 and generated cases for deterministic change, quiescent
identity, eventful identity, stopped successor, terminal, undefined, declared
failure, certified divergence, empty output value, exact-zero relation, and
undetermined intensional relation.

Assert all three cardinalities independently. A bare exact empty finite
support is invalid; `ResourceExhausted` exists only in bounded external
query/realization/rollout results.

### CT06 — Probability, Seed realization, and replay

Run PX06 and PX09's terminal-measurement variant. Assert:

```text
RuleComplete contains a normalized law and no draw
full applied-atom mass = 1
successor mass + no-successor mass = 1
derived submeasures are not renormalized
```

The same `(law, application, input lineage, replay key, sampler/profile
version)` reproduces the same atom and evidence. Worker order, traversal
order, ambient RNG, lazy/eager presentation, and unrelated draws cannot alter
the law or semantic result. Trace lineage may affect a later draw coordinate;
it cannot affect denotation or fresh identity.

Seed laws cross the same explicit realization boundary. A Bernoulli Seed over
a two-locus carrier supplies this generated case:

```text
Seed descriptor = closed normalized law, with no materialized draw
no root replay key = retain the complete initial law/outcome space
same root key + representation/sampler profile = same C and draw evidence
explicit initial C = bypass Seed realization, then validate normally
```

Ambient RNG state, worker/traversal order, and unrelated draws cannot change
the realization for the same key. A different key may select a different
initial configuration but cannot change the Seed descriptor or law.
Missing/invalid replay evidence cannot be silently replaced by a hidden
generator.

One intensional-law case exercises the only valid unavailable measure view.
When the source law and full applied-atom mapping are valid and measurable,
but measurability of the semantic-successor quotient is not established:

```text
applied_atom_measure = Available
no_successor_submeasure = Available
successor_submeasure = Unavailable(reason, retained mapping evidence)
```

An invalid source law, normalization, measurable atom space, reconstruction
map, or applied mapping instead rejects the application. `Unavailable` is
permitted only for that derived successor-quotient view; it is never a
catch-all for malformed probability semantics.

### CT07 — Fresh identities

For PX02 and generated structural cases:

```python
a = bind(input_id, rule_id, witness, parent, namespace, "x")
b = bind(input_id, rule_id, witness, parent, namespace, "x")
c = bind(input_id, rule_id, witness, parent, namespace, "y")
assert a == b
assert a != c
```

Repeat under reverse traversal, different worker counts, lazy/eager
materialization, and unrelated allocations. Reject unauthorized namespace or
parent use and collisions with no commit. Alpha-equivalence may group
successors later, but raw bindings remain in applied evidence.

### CT08 — Witnesses, fibers, and quotient

Run the PX04 diamond and assert:

```text
outcome atoms = 2
derivations = 2
distinct successors = 1
successor fiber contains both stable witnesses
```

Permutation of Rule/match enumeration cannot change the quotient or fiber.
Semantic equality cannot be replaced by hash, storage order, approximate
numeric equality, display form, or catalog name. Equal-successor probability
mass sums without erasing source atoms.

### CT09 — Exact, fail-closed serialization

Every public descriptor and every Rule/Application/result variant satisfies:

```python
blob = dumps(value)
decoded = loads(blob)
assert decoded == Decoded(value)
assert dumps(decoded.value) == blob
```

The canonical program payload has exactly the five field keys. Round trips
preserve large signed integers, rationals and represented numerics, tagged
products, order/multiplicity/absence/defaults, structural identity and
interfaces, intensional ASTs, laws versus draw evidence, dispositions,
witnesses, fresh bindings, fibers, lineage, cardinalities, submeasures,
reconstruction obligations, and representation relations.

Unknown tags, versions, primitives, missing/extra/duplicate fields, lossy
migrations, and stale forged digests return `DecodeRejected`; they never
produce partial objects or convenient defaults. Catalog spelling and
constructor arguments are absent from canonical program serialization.

### CT10 — Representation commutation

An exact representation claim requires inverse-on-image and full-result
one-step commutation:

```python
assert decode(encode(source)) == source
assert_full_application_equal(
    map_complete_result(
        apply(represented_program, encode(source)),
        decode,
    ),
    apply(native_program, source),
)
```

The comparison includes outcomes, total dispositions, all cardinalities,
witnesses, provenance, progress/continuation, probabilities, submeasures,
no-successor atoms, fresh bindings, fibers, and lineage modulo the declared
map. A lossy, approximate, or out-of-image translation remains an explicit
relation or qualified realization, never an alias.

### CT11 — Catalog expansion and T01–T45 migration

Every canonical constructor returns one validated expanded program and has
exactly one SPF target. For callable kinds:

```text
A: same normalized arguments and exactly equal expanded payload as delegate
P: payload equals its canonical family after declared closed bindings
K: total, lossless legacy-argument translation over its advertised domain
C: the exact canonical constructor
```

`M` is never callable. Metadata records contain no callable, component,
program, executor, Rule tag, or registry hook. T08 alone has zero SPF targets;
T40 alone has two explicitly named preset branches and no umbrella callable or
`kind=` dispatch; every other T row has one target. Deprecated `K` spellings
are category-qualified and not flat. Alias/preset invocation history never
enters program equality, serialization, or application.

One parameterized expected-migration manifest must assert the ledger
row-by-row rather than testing only those generic invariants:

- legacy IDs are exactly T01–T45;
- target cardinality is `0` for T08, `2` for T40, and `1` for each of the
  other 43 entries;
- the 49 callable relations count exactly `C=5`, `P=39`, `A=4`, and `K=1`;
- each relation has the ledger's exact spelling, kind, SPF target, owner
  module, closed binding/translation, and flat-export flag;
- all 48 `C/P/A` names are explicit flat catalog exports, the sole `K` is
  category-qualified only, and every `M` relation is non-callable; and
- T32 and T44 are specifically `P`, not `A`: each binds a narrower closed
  representation of its family rather than accepting the canonical
  constructor's unchanged arguments.

The expected manifest is test data transcribed from
`catalog-migration.md`; it does not become a runtime registry or a second
semantic catalog.

### CT12 — Independent native/generic equivalence

Where a current implementation or canonical fixture supplies an independent
one-step oracle:

```python
expected = reference_step(fixture)  # test-only
actual = apply(canonical_or_preset_program, fixture.configuration)
assert_full_application_equal(actual, expected)
```

The comparison is the complete application result, not just a displayed state.
The generic implementation may not call the reference oracle. At minimum,
retain independent fixtures for cellular/mobile/Turing automata,
substitutions, multiway systems, constraints, variable support, stochastic
laws, and differential/intensional representations.

Differential and intensional oracle cases are deliberately tiny closed
fixtures whose expected relation has a canonical structural AST or exact
finite characterization. They do not require a general solver, extensional
equality for arbitrary intensional relations, or a new equivalence-proving
framework; unsupported/undetermined equivalence remains explicit.

### CT13 — Import ownership and no dispatch

Static dependency tests assert:

- `loci`, `alphabets`, `seeds`, `frontiers`, and `neighborhoods` do not import
  `rules`, `program`, or `catalog`;
- `rules.py` does not import `program` or `catalog`;
- semantic owner modules do not import `serialization`; codecs depend on
  owners, never the reverse;
- `program.py` and `serialization.py` do not import `catalog`;
- core does not import datasets, RNG, generation, or visualization;
- package internals do not import through root `ca`;
- category modules do not import `catalog.entries`; `catalog.__init__` is the
  sole join point for constructors and metadata;
- `apply` dispatches only on sealed generic descriptor/result operations; and
- generic application never inspects SPF/F/T ID, category, constructor name,
  Book source, semantic family, carrier label, locus kind, or Rule tag to
  choose a family-specific algorithm.

Behavioral tests apply and decode already constructed programs while catalog
imports are blocked. Public-surface tests assert `ca.rollout` is callable,
there is no shadowing public `ca.rollout` submodule, catalog constructors are
not flattened to root `ca`, and obsolete public
`configuration/regions/replacement/results/engine/run/updates` modules do not
appear. Exact signature tests admit only:

```text
apply(program, input)
rollout(program, *, steps, initial=None, replay_key=None)
```

Solver, RNG, update, observer, renderer, branch-selection, resource, and
result-policy keywords are forbidden on these two base operations. Qualified
external query/realization tools may own typed requests without changing
either signature.

For one deterministic and one branching fixture, compare `rollout(...,
steps=n)` with manual expansion by repeated calls to the owned `program.apply`,
including raw configurations, outcomes, witnesses, lineage, continuation, and
derivation fibers. A test-only spy on the owned `apply` binding plus static
call-graph inspection must prove rollout has no legacy `apply_rule`, tensor,
family, or duplicated generic-looking one-step path.

Descriptor-owning modules may, of course, interpret their recognized sealed
locus, selector, Rule-AST, and result variants; the prohibition is against the
executor using those tags as a disguised semantic-family switch.

### CT14 — Observer boundary

Run PX12 and assert F004/F045 are executable ordinary programs, while F010 and
F042 resolve only to callable-free role entries. Pure observers, renderers,
exporters, and interfaces cannot occupy a program field, change semantic
identity, affect application, appear in canonical serialization, or gain a
family constructor merely because they inspect a run.

## Public-contract and pseudocode audit

The Stage 6 inspection covers `api.md`, `simple_programs.md`,
`ref/notes/ca-scaffold.py`, and the normative application in
`architecture.md`.

The target documents pass these checks:

- every normative `SimpleProgram` has exactly the five stored fields;
- support/topology/boundary/control/program text live in configurations
  produced by Seed, not a sidecar;
- `ApplicationInput`, lineage, compatibility certificates, reconstruction
  plans, results, and rollout requests are application evidence or tooling,
  not fields;
- Rule denotes laws and intensional relations but performs no random draw,
  solver search, or numerical integration;
- `apply` contains no semantic-family, catalog, carrier, locus-kind, or Rule-tag
  branch;
- Rule-side records stay in `rules.py`, application-side records and both
  public operations stay in `program.py`, and codecs stay in
  `serialization.py`;
- aliases expand before application and canonical serialization stores only
  expanded five-field payloads; and
- the retained runtime README is explicitly historical/current-runtime
  documentation rather than a competing target.

The following are hard tripwires for Goal 7:

- any sixth stored field or semantic sidecar/constructor receipt;
- Frontier narrowed to firing sources rather than the possible-write envelope;
- commit-time scheduling, arbitration, collision repair, or inferred writes;
- Rule-side draws, ambient RNG, hidden partial solver behavior, or silent float
  exactness;
- mutable program/control state outside `C`;
- family/carrier/catalog dispatch or a compatibility executor fork;
- observer/property logic promoted to a family without its own commit; or
- an alias claim without exact expansion, or a representation claim without
  full-result commutation.

## Stage 6 conclusion

All twelve pressure categories pass the same five contracts and one
family-blind application law. The 60-family partition has no hole or duplicate;
the eight secondary joins expose deliberate cross-cutting pressure. No fixture
requires a sixth field, firing-source Frontier, update/result/scheduler policy,
hidden entropy or solver, implicit structural repair, catalog dispatch, or a
second execution path.

Goal 7 can therefore organize conformance around fourteen reusable semantic
suites plus one parameterized 60-family constructor/coverage join, rather than
sixty executors or a second audit system.
