# ankos

ankos 0.2.0 is a Python library for constructing and applying closed simple
programs inspired by *A New Kind of Science*. Cellular automata, substitutions,
machines, transductions, constraints, and continuous relations share one
program boundary:

```python
SimpleProgram(
    seed=...,
    alphabet=...,
    frontier=...,
    neighborhood=...,
    rule=...,
)
```

Every named construction expands to those five fields. One family-blind
operation applies every program, and rollout repeats that same operation:

```python
result = ca.apply(program, configuration)
episode = ca.rollout(program, steps=100)
```

There are no family-specific executors, hidden update-policy field, or
compatibility runtime.

## Quick start

The project requires Python 3.10 or newer. From a checkout:

```bash
uv sync
uv run pytest -q
```

Construct and traverse elementary cellular automaton rule 30:

```python
import ca

program = ca.catalog.eca(rule=30, width=9)
episode = ca.rollout(
    program,
    steps=4,
    replay_key="readme-rule-30",
)

print(type(episode).__name__)
print(len(episode.raw_trace.applications.atoms))
# RolloutTruncated
# 4
```

The catalog constructor supplies a Bernoulli Seed. The replay key authorizes
one deterministic, reproducible realization of that law; it is execution
evidence, not a sixth program field. Reaching `steps=4` is a depth bound, so
the continuing run is correctly reported as `RolloutTruncated`, not as
terminal.

To apply an explicit configuration once:

```python
import ca

program = ca.catalog.eca(rule=30, width=5)
configuration = ca.loci.grid_configuration(
    (5,),
    (False, False, True, False, False),
    boundary=ca.loci.Boundary(
        ca.loci.BoundaryPolicy.FIXED,
        False,
    ),
)

result = ca.apply(program, configuration)

if isinstance(result, ca.program.ApplicationComplete):
    successors = result.successor_quotient_with_derivation_fibers
    next_configuration = successors.atoms[0].successor
else:
    raise ValueError(result.fault)
```

Application never mutates the input. It validates and atomically reconstructs
every alternative, retains complete derivation fibers, then groups equal
successors.

## The five fields

| Field | Responsibility |
|---|---|
| `seed` | A closed source of valid initial configurations or a law over them |
| `alphabet` | The closed structural universe and equality of semantic values |
| `frontier` | The complete writable capability envelope for one application |
| `neighborhood` | The complete identity-preserving readable view |
| `rule` | Applicability, schedules, conflicts, stochastic laws, stopping, and complete atomic replacements |

The field names *Frontier* and *Neighborhood* describe responsibilities. Their
public component types are `ca.frontiers.WritableRegion` and
`ca.neighborhoods.ReadableRegion`.

Frontier is not merely the set of loci that fire. It includes every existing
or potential component that any permitted Rule alternative may change. A
mobile automaton therefore authorizes the source and all possible
destinations; the active tag and Rule select the actual move, while every
unselected capability is preserved.

Neighborhood is not required to be geometrically local. It may describe a
stencil, a word span, a matched graph interface, a complete history, a global
aggregate, a differential germ, or an intensional relation.

Support, topology, geometry, defaults, boundary behavior, invariants, and
visible control state live in Seed-produced configurations. Scheduling,
branching, conflict resolution, stopping, and probability laws live in Rule.
They do not become extra fields.

See [`simple_programs.md`](simple_programs.md) for the conceptual model and
[`api.md`](api.md) for the exact public contract.

## Explicit five-field construction

Catalog names are ordinary compositions. This complete expansion is exactly
equal to `ca.catalog.eca(rule=30, width=79)`:

```python
from fractions import Fraction

import ca

carrier = ca.loci.CarrierContract(
    ca.loci.CarrierKind.GRID,
    rank=1,
    shape=(79,),
    axes=("x",),
)
alphabet = ca.alphabets.boolean()
boundary = ca.loci.Boundary(
    ca.loci.BoundaryPolicy.FIXED,
    False,
)

explicit = ca.SimpleProgram(
    seed=ca.seeds.bernoulli(
        ca.loci.literal(ca.loci.grid_loci((79,), axes=("x",))),
        Fraction(1, 2),
        configuration_contract=carrier,
        value_profile=alphabet.value_profile,
        boundary=boundary,
    ),
    alphabet=alphabet,
    frontier=ca.frontiers.everywhere(
        configuration_contract=carrier,
        value_profile=alphabet.value_profile,
    ),
    neighborhood=ca.neighborhoods.eca(
        configuration_contract=carrier,
        value_profile=alphabet.value_profile,
    ),
    rule=ca.rules.elementary(30),
)

named = ca.catalog.eca(rule=30, width=79)

assert explicit == named
assert explicit.canonical_identity == named.canonical_identity
```

The plural owner modules build singular components:

```text
ca.loci             structural identity and region vocabulary
ca.alphabets        Alphabet values and constructors
ca.seeds            Seed values and constructors
ca.frontiers        WritableRegion values and constructors
ca.neighborhoods    ReadableRegion values and constructors
ca.rules            Rule values, results, atoms, and constructors
```

They progress from closed primitives through composition to useful component
presets. Component constructors remain module-qualified, so
`ca.neighborhoods.eca()` means one readable component while
`ca.catalog.eca()` means one complete program.

## Catalog

The catalog contains one canonical constructor for each of the 60 audited
executable semantic families. The six namespaces organize discovery by
dominant mechanic; they do not define runtime classes:

| Namespace | Dominant mechanic |
|---|---|
| `ca.catalog.automata` | Persistent carriers updated in place or in parallel |
| `ca.catalog.substitua` | Matched structure replaced, grown, deleted, or branched |
| `ca.catalog.machina` | Visible heads, control, instructions, stacks, or schedules |
| `ca.catalog.media` | Information transformed between representations |
| `ca.catalog.criteria` | Admissibility, constraints, witnesses, or weighted alternatives |
| `ca.catalog.dynamica` | Continuous differential, field, event, or flow laws |

Canonical constructors are available both through their owner and through the
collision-free catalog façade:

```python
qualified = ca.catalog.automata.eca(rule=30, width=79)
convenient = ca.catalog.eca(rule=30, width=79)

assert qualified == convenient
```

Catalog metadata in `ca.catalog.entries` is immutable and callable-free.
Family, audit, and legacy IDs support provenance and navigation only; none can
select application behavior. Constructor spelling and arguments are not part
of program identity.

## Application results

`ca.apply(program, input)` returns one of the records owned by `ca.program`:

```text
ApplicationResult =
    ApplicationComplete(...)
  | ApplicationRejected(ApplicationFault(...))
```

A complete result retains:

- the Rule's complete source outcome space;
- applied derivations and typed no-successor atoms;
- outcome, derivation, and distinct-successor cardinalities;
- semantically equal successors with all derivation fibers;
- probability and submeasure views; and
- phase, identity, lineage, and reconstruction evidence.

`ApplicationRejected` means no authoritative successor was committed.
Terminality, undefinedness, declared construction failure, and certified
divergence are instead typed Rule outcomes inside a complete application.

Advanced callers may provide explicit lineage:

```python
application_input = ca.program.ApplicationInput(
    configuration=configuration,
)
result = ca.apply(program, application_input)
```

## Rollout

The exact convenience signature is:

```text
rollout(program, *, steps, initial=None, replay_key=None) -> RolloutResult
```

`ca.rollout` repeatedly calls the same `ca.program.apply`. It returns
`RolloutComplete`, `RolloutTruncated`, or `RolloutRejected`, all owned by
`ca.program`. A truncation cause is explicit: depth bound, intensional support,
resource exhaustion, cancellation, or pruning.

With no `initial`, rollout starts from the Seed denotation. A replay key
authorizes reproducible realization when a Seed or Rule law requires a draw.
Without a key, finite or intensional laws remain complete laws rather than
being sampled implicitly. A depth bound is application depth, not necessarily
physical time.

One-shot functions, constraint completions, representation transforms, and
many continuous relations are normally consumed with `ca.apply`; they do not
need a fake trajectory.

## Canonical serialization

Serialization is fail-closed and catalog-free:

```python
payload = ca.serialization.dumps(program)
decoded = ca.serialization.loads(payload)

match decoded:
    case ca.serialization.Decoded(value=restored):
        assert restored == program
    case ca.serialization.DecodeRejected(fault=fault):
        raise ValueError(fault)
```

The canonical program tag is `ca.simple-program`, and its schema version is
`1`. Its payload contains exactly:

```text
seed, alphabet, frontier, neighborhood, rule
```

The schema version is independent of the package version `0.2.0`. The same
closed codec also serializes supported component, Rule-result, application,
rollout, evidence, and trace records. Unknown tags, versions, fields,
primitives, noncanonical encodings, and forged digests produce
`DecodeRejected`; no partial value escapes.

Serialized programs contain expanded components. They do not contain catalog
IDs, constructor receipts, aliases, or invocation history.

## Migrating source from 0.1

The 0.1 construction surface was a source recipe, not an earlier canonical
semantic format. Migrate source deliberately:

| Removed 0.1 spelling | 0.2.0 replacement |
|---|---|
| `ca.Dynamics(...)` plus `rule_id` | A matching `ca.catalog.<constructor>(...)`, or explicit `ca.SimpleProgram(...)` |
| `ca.rollout(dynamics=..., rule_id=..., seed_state=..., steps=...)` | `ca.rollout(program, steps=..., initial=..., replay_key=...)` |
| `ca.RawEpisode` / `ca.RawBatch` | `ca.program.RolloutComplete`, `RolloutTruncated`, or `RolloutRejected`; downstream dataset views when dense tensors are needed |
| root component helpers | Their plural owner modules, such as `ca.rules.elementary(...)` |
| `ca.apply_rule` | `ca.apply` |

Old `Dynamics` manifest dictionaries are not accepted by
`ca.serialization.loads`. Reconstruct them in source through a catalog
constructor or explicit five-field composition, then serialize the expanded
program. ankos intentionally ships no fallback decoder, compatibility
executor, or silent “try old then new” path.

[`README-V1.md`](README-V1.md) preserves the old source surface only as
historical documentation.

## Package surface

The root façade intentionally exposes exactly three conveniences and nine
owner namespaces:

```python
ca.SimpleProgram
ca.apply
ca.rollout

ca.program
ca.catalog
ca.loci
ca.alphabets
ca.seeds
ca.frontiers
ca.neighborhoods
ca.rules
ca.serialization
```

There is no public `ca.rollout` submodule: the package attribute has one
meaning, the callable. Application and rollout records remain under
`ca.program`; Rule records remain under `ca.rules`; components remain under
their plural owners; complete programs remain under `ca.catalog`.

Auxiliary modules are explicit downstream imports and are not loaded by
`import ca`:

```python
from ca import datasets, rng, viz
```

They may plan, materialize, sample, or present semantic results. They do not
define program identity, perform an alternate transition, or contribute
ambient entropy to core semantics.

The installed package is organized as:

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
├── py.typed
├── catalog/
│   ├── __init__.py
│   ├── entries.py
│   ├── automata.py
│   ├── substitua.py
│   ├── machina.py
│   ├── media.py
│   ├── criteria.py
│   └── dynamica.py
├── datasets.py
├── rng.py
└── viz/
```

`py.typed` is the distributed PEP 561 marker for the inline type information.

## Documentation and development

- [`api.md`](api.md) — exact public behavior and ownership
- [`simple_programs.md`](simple_programs.md) — conceptual five-field model
- [`ref/notes/ca-scaffold.py`](ref/notes/ca-scaffold.py) — compact
  code-shaped walkthrough
- [`goal-5/taxonomy-census.md`](goal-5/taxonomy-census.md) — audited
  60-family taxonomy
- [`ref/A-New-Kind-of-Science/Contents.md`](ref/A-New-Kind-of-Science/Contents.md)
  — canonical book navigation

Development gates:

```bash
uv run pytest -q tests
uv lock --check
git diff --check
```
