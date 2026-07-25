# `ca` Target Public API

Status: **settled Goal 6 design contract; implementation is pending Goal 7**

This is the public API that Goal 7 will implement, not a claim that the current
0.1.0 `Dynamics` runtime already provides it.

The complete validation, reconstruction, measure, and intensional contract is
in [`goal-6/architecture.md`](goal-6/architecture.md).

## One Program Value

Every executable construction is one immutable value with exactly five stored
fields:

```python
@dataclass(frozen=True)
class SimpleProgram(Generic[C, V, W, R]):
    seed: Seed[C]
    alphabet: Alphabet[V]
    frontier: WritableRegion[C, W]
    neighborhood: ReadableRegion[C, R]
    rule: Rule[R, W, C]
```

The fields have one responsibility each:

| Field | Public meaning |
|---|---|
| `seed` | A closed source of valid initial configurations |
| `alphabet` | The closed structural universe of semantic values |
| `frontier` | The complete writable capability envelope for one application |
| `neighborhood` | The complete readable view for one application |
| `rule` | The closed relation from the readable/writable binding to typed atomic results |

`C`, `V`, `W`, and `R` are type relationships, not additional fields.
Configuration support, topology, geometry, defaults, boundary behavior,
invariants, control, schedule, mutable program text, and visible entropy are
ordinary typed data where the construction requires them.

There is no `Domain`, `Shape`, `Boundary`, `ConfigurationSchema`,
`UpdatePolicy`, scheduler, solver, RNG, or result-policy field.

`Seed` produces immutable configurations. A configuration carries the
structural information its program needs: carrier support, topology,
geometry, defaults, side data, stable identities, invariants, and visible
control state.
Successors have the same configuration contract as their inputs, but they do
not need to remain in the initial Seed's support. Seed governs initialization;
Rule governs the transition or relation codomain.

All five components are built from recognized, versioned structural
descriptors. Closed does not mean finite: a descriptor may denote an infinite
set, continuous field, probability measure, recursive object, or symbolic
relation through a closed AST.
Semantic descriptors may not contain arbitrary Python callbacks, generators,
iterators, `Any`, executable formula strings, host CAS objects, ambient RNG
state, or hidden solvers. Exact and represented numerical profiles remain
explicit; machine floats never silently stand in for exact reals.

## Constructing Programs

The plural component modules construct one value for each program field:

```python
import ca

program = ca.SimpleProgram(
    seed=ca.seeds.bernoulli(...),
    alphabet=ca.alphabets.boolean(),
    frontier=ca.frontiers.everywhere(),
    neighborhood=ca.neighborhoods.eca(),
    rule=ca.rules.elementary(30),
)
```

Within each plural module, the public progression is primitives, compounds,
general constructors, then component presets.

Composition always returns one component value. A product of several readable
views is one `ReadableRegion`; a union of writable capabilities is one
`WritableRegion`; a composition of clauses is one `Rule`. Construction does
not add more fields to `SimpleProgram`.

`loci.py` supplies shared identity and selector vocabulary for coordinates,
spans, words, trees, graphs, products, fields, histories, and fresh
components. A raw locus or selector grants neither read nor write permission.
`frontiers.py` turns selectors into write capabilities;
`neighborhoods.py` turns them into read views.

## Catalog Constructors

Whole-program semantic names live under `ca.catalog`:

```python
same_kind_of_program = ca.catalog.eca(rule=30)
```

The preferred convenience spelling is `ca.catalog.<constructor>`. Each
constructor has exactly one source owner in one of six navigation modules:

| Module | Dominant construction mechanic |
|---|---|
| `ca.catalog.automata` | Persistent carriers updated in place or in parallel |
| `ca.catalog.substitua` | Matched structure replaced, grown, deleted, or branched |
| `ca.catalog.machina` | Visible heads, control states, instructions, stacks, or schedules |
| `ca.catalog.media` | Information transformed between distinct representations |
| `ca.catalog.criteria` | Admissibility, constraints, witnesses, solutions, or weighted alternatives |
| `ca.catalog.dynamica` | Continuous differential, field, event, or flow laws |

For example, `eca` is owned by `ca.catalog.automata` and may be re-exported as
`ca.catalog.eca`. These modules are for navigation and constructor ownership,
not runtime classes.

Every canonical constructor, parameter preset, compatibility name, and alias
returns an ordinary five-field `SimpleProgram`, expands through ordinary
component constructors, records status and provenance as metadata, and has no
privileged executor or influence on `ca.apply`.

Reusable pieces remain in the component modules. In particular,
`ca.neighborhoods.eca()` is a Neighborhood preset, while
`ca.catalog.eca(...)` is a whole program. There is intentionally no ambiguous
root-level `ca.eca`.

`ca.catalog.entries` owns descriptive lookup, aliases, sources, and
construction receipts. It is not an execution registry, and catalog IDs or
family names never select an application algorithm.

The 60 audited executable semantic families are coverage obligations and
constructor destinations. They are not 60 subclasses, executor branches, or
top-level fields.

## Applying One Program

One family-blind operation is the semantic execution primitive:

```python
application_input = ca.program.ApplicationInput(
    configuration=configuration,
)

result = ca.apply(program, application_input)
```

`ApplicationInput` contains one immutable configuration and optional validated
trace lineage. Direct application can derive root lineage canonically when it
is omitted. Lineage is invocation evidence; it cannot alter Rule denotation,
fresh structural identities, or semantic successor equality.

Conceptually:

```text
w = frontier.resolve(configuration)
r = neighborhood.resolve(configuration)
rule_result = rule.denote(r, w)
application_result = validate_and_atomically_apply(rule_result)
```

Frontier and Neighborhood resolve independently from the same immutable
configuration. Rule receives only the readable view `R` and writable
capability `W`; Frontier does not expose old values, and Rule does not receive
unrestricted configuration access.

The framework validates and reconstructs Rule results. It never chooses a
match, schedule, collision winner, stochastic branch, deletion cascade, graph
repair, or continuous endpoint. Those choices must already be explicit in
Rule data and its result relation.

### Rule results

The public result model distinguishes a complete denotation from a rejected
boundary:

```text
Complete(payload)
Rejected(fault)
```

The envelope and application records are owned by `ca.program`; Rule-result
records and atoms are owned by `ca.rules`. They remain public there rather
than being flattened into the root namespace.

A complete Rule result has finite or intensional support containing:

```text
Derivation(
    TotalDisposition[W],
    Advanced | Quiescent,
    Continue | Stop(reason),
    witness,
    provenance,
)
NoSuccessor(Terminal | Undefined | DeclaredFailure | Divergent, reason, witness, provenance)
```

Each derivation gives a total disposition:

```text
existing writable capability -> Preserve | Replace(payload) | Delete
fresh writable capability    -> Absent   | Create(payload)
outside the frontier         -> Preserve
```

A sparse serialized form is allowed only when its declared defaults recover
that total meaning. Generic application never merges proposals or invents a
missing structural effect.

### Outcomes are not list lengths

| Case | Required representation |
|---|---|
| Ordinary change | `Advanced` derivation |
| Stable no-event identity | `Quiescent` identity derivation |
| Eventful same-state result | `Advanced` derivation with retained witness |
| Completed one-shot result | `Advanced + Stop(Completed)` |
| Exact halt or no solution | Typed `Terminal` atom |
| Partial mathematical domain | Typed `Undefined` atom |
| Construction-defined failure | Typed `DeclaredFailure` atom |
| Proven semantic noncompletion | Typed `Divergent` atom with certificate |
| Invalid or unsupported boundary | `Rejected(fault)` with no authoritative successors |

An exact zero-replacement result is never a bare empty list. It carries a
typed `NoSuccessor` atom. An intensional relation may instead be complete with
`Undetermined` cardinality; that does not justify inventing a terminal atom.

Support cardinality and probability are separate. A result can have exactly
zero, exactly one, many, or undetermined derivations, with or without a
probability law over its typed atoms.

### Atomic application

Before exposing any successor, application validates result completeness,
witnesses, dispositions, values, and laws; binds fresh identities; reconstructs
every alternative from the same snapshot; validates every successor and
continuation; and only then groups semantically equal successors. A fault in
any phase rejects the complete application. No partial commit or selected
valid-looking subset becomes authoritative.

Equal successors retain their complete derivation fibers. A two-path diamond
can therefore have two witnessed derivations and one distinct successor
without losing either path, probability contribution, or continuation flag.

## Compact Semantic Examples

### Mobile head

Suppose a tagged head is at `h` and can move left or right:

```text
W = {h - 1, h, h + 1}
R = old values and identities at {h - 1, h, h + 1}
```

For a right move, one Rule derivation returns:

```text
h - 1 -> Preserve
h     -> Replace(Plain(new_symbol))
h + 1 -> Replace(Head(new_control, old_right_symbol))
```

The Rule is denoted once over the structured `(R, W)`. The runtime does not
run it once per cell, collect proposals, or resolve a collision afterward.

### One-shot function and constraint

A function evaluation can use input and output slots in one configuration:

```text
Input(3) -> Output(9), Advanced + Stop(Completed)
```

It is complete after one `ca.apply`; it does not need a fake second step to
discover that it should stop. Iteration is a different composed Rule/program
that writes feedback state and returns `Continue`.

A constraint Rule denotes every valid completion of its writable unknown
region. Its result may be finite or intensional. Certified unsatisfiability is
`Terminal(NoSolution)` with coverage evidence. A bounded solver may return
verified members or partial evidence, but partial enumeration never
masquerades as the complete Rule result.

### Continuous relation

A continuous Rule may return an exact or represented flow, event segment, or
intensional solution relation. It may commit an endpoint only when a duration
or selector is closed Rule data, visible in the readable configuration, or
intrinsically determined by an event or singularity.

Without such a selector, an event-free flow normally returns its maximal
flow/solution object as a one-shot result. An external time query may inspect
that object; a rollout horizon cannot silently choose and commit a semantic
endpoint.

## Rollout, Sampling, and Queries

`ca.rollout` is tooling built by repeatedly invoking the same family-blind
`ca.apply` relation:

```python
episode = ca.rollout(
    same_kind_of_program,
    steps=100,
    replay_key=1234,
)
```

`steps` bounds application depth. It is not necessarily physical time, and
reaching it produces a typed truncated run with continuing leaves rather than
a false terminal outcome.

Rollout realizes or binds the Seed with root replay evidence, expands every
continuing configuration/lineage derivation fiber, retains raw applications
and witnesses, propagates exact measures or replay subkeys, and stops a branch
only on its own `Stop` or typed no-successor atom.

A probability law is descriptor data; a draw is an external realization.
The replay key, sampler/profile version, selected witness, and derived subkey
are evidence in the realized trace. No ambient RNG state contributes
semantics.

Exhaustive rollout of a branching or intensional relation is itself branching
or intensional. A query may sample, bound, or project it, but that request does
not replace the complete denotation. Resource exhaustion, cancellation,
pruning, and approximation do not prove terminality, divergence,
unsatisfiability, or exact cardinality.

One-shot functions, constraint completions, media transforms, and many
continuous relations are normally consumed with `ca.apply`, not mandatory
rollout.

The public callable is `ca.rollout`. The existing `rollout.py` may remain the
auxiliary implementation behind that root function, but the target API does
not promise a `ca.rollout` module namespace or a `run.py`.

## Serialization

Serialization is cross-cutting infrastructure, not a program component or
execution registry:

```python
payload = ca.serialization.dumps(same_kind_of_program)
restored = ca.serialization.loads(payload)
```

The canonical program payload always contains the validated, expanded
`seed`, `alphabet`, `frontier`, `neighborhood`, and `rule` fields.

A versioned outer envelope may carry provenance, a derived digest, and an
optional verified catalog construction receipt. An alias-only recipe is never
the authoritative lossless representation, and execution never dispatches on
an alias.

Canonical codecs:

- preserve exact values, structural identities, order, multiplicity, and
  explicit absence/unknown roles;
- preserve finite and intensional descriptors without forced enumeration;
- keep probability laws separate from concrete draw/replay evidence;
- preserve typed results, cardinalities, dispositions, witnesses, fresh
  bindings, successor fibers, and trace lineage;
- reject unknown tags, versions, fields, primitives, or lossy migrations; and
- derive identifiers and digests from validated canonical structure.

Python class names, object addresses, host hashes, locale, NumPy defaults, and
machine floating behavior are never semantic identity.

## Package and Import Ownership

The target core is:

```text
src/ca/
├── __init__.py
├── program.py
├── loci.py
├── alphabets.py
├── seeds.py
├── frontiers.py
├── neighborhoods.py
├── rules.py
├── serialization.py
├── rollout.py                  # auxiliary implementation behind ca.rollout
├── py.typed
└── catalog/
    ├── __init__.py
    ├── entries.py
    ├── automata.py
    ├── substitua.py
    ├── machina.py
    ├── media.py
    ├── criteria.py
    └── dynamica.py
```

| File or namespace | Cohesive responsibility |
|---|---|
| `ca.__init__` | Root façade and stable re-exports |
| `program.py` | `SimpleProgram`, application inputs/results, `apply`, validation, and private family-blind reconstruction/commit |
| `loci.py` | Shared closed locus, identity, selector, and region vocabulary |
| `alphabets.py` | Alphabet descriptors, composition, and presets |
| `seeds.py` | Seed descriptors, composition, and presets |
| `frontiers.py` | WritableRegion descriptors, capability resolution, composition, and presets |
| `neighborhoods.py` | ReadableRegion descriptors, read resolution, composition, and presets |
| `rules.py` | Rule descriptors, Rule results/atoms, total dispositions, composition, and presets |
| `serialization.py` | Versioned canonical codecs and migrations |
| `rollout.py` | Non-semantic traversal implementation behind the root callable |
| `py.typed` | Static-typing package marker; no runtime behavior |
| `catalog/entries.py` | Descriptive constructor/alias/provenance metadata |
| six catalog modules | Canonical whole-program constructor ownership |

The root façade re-exports only:

- `ca.SimpleProgram`;
- `ca.apply`;
- `ca.rollout`; and
- the `program`, `loci`, plural component, `serialization`, and `catalog`
  module namespaces.

Application/result records remain under `ca.program`; Rule result records and
atoms remain under `ca.rules`. Component constructors remain under their
plural modules, and whole-program constructors remain under `ca.catalog`.

There is no need for public `configuration.py`, `replacement.py`, `results.py`,
`engine.py`, or `run.py`. Their legitimate responsibilities are already owned
by Seed-produced configurations, `rules.py`, `program.py`, and the root
rollout boundary.

## Deliberately Deferred Auxiliaries

Goal 6 does not promise a final internal organization for generation,
datasets, streams, RNG helpers, visualization, observers, renderers, or
exporters.

Those tools may consume Seeds, programs, application results, rollout traces,
and canonical serialization. They may not become hidden program fields,
alternate executors, entropy authorities, or definitions of semantic
configuration/result identity.

No target imports such as `ca.generation`, `ca.datasets`, `ca.streams`,
`ca.rng`, or `ca.viz` are established here. Goal 7 may evolve auxiliary code
in place while preserving the boundaries above.

## Documentation Roles

`api.md` is the target public contract; `goal-6/architecture.md` is the
canonical internal specification; `simple_programs.md` supplies non-competing
conceptual rationale; and `ref/notes/ca-scaffold.py` is the compact code-shaped
walkthrough.

Together they describe one architecture: five stored program fields, closed
structural data, one family-blind application law, named catalog
constructions, and tooling outside the semantic program value.
