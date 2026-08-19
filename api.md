# `ca` 0.2.0 Target Public API

Status: **accepted architectural direction; implementation pending**

This document defines the target semantic API for ANKoS. It replaces the
current five-field runtime, which still contains `Seed`, `Frontier`, and
patch/disposition machinery.

The target architecture stops at the input to `rollout`. The exact rollout
limit, resource controls, and returned Episode representation will be designed
later, when the families that need them are implemented.

## Architecture

The complete object graph is:

```text
SPACES        -> SPACE
ALPHABETS     -> ALPHABET
NEIGHBORHOODS -> NEIGHBORHOOD
RULES         -> RULE

SPACES + ALPHABETS + NEIGHBORHOODS + RULES
    -> PRESET

SPACE + ALPHABET + NEIGHBORHOOD + RULE
    -> SIMPLEPROGRAM

PRESET
    -> SIMPLEPROGRAMS

SEEDS
    -> SEED

SIMPLEPROGRAM + SEED
    -> TRAJECTORY

rollout(TRAJECTORY, RESOURCES/LIMIT)
    -> EPISODE
```

The first four plural names denote sources of possible values. The singular
names denote one definite selected value. A Preset combines the four plural
sources and generates definite SimplePrograms. Seeds remain separate.

## Keep the Implementation Plain

These names describe semantic roles, not a required hierarchy of classes.
`SPACES`, for example, may be a tuple, iterator, generator function, or small
declarative object that yields `SPACE` values.

Use ordinary Python data and functions wherever possible. Type hints may make
interfaces easier to understand, but the architecture does not require a deep
type lattice, capability system, validation framework, or a special class for
every family.

A useful Preset must generate at least one SimpleProgram. A plural source may
contain exactly one value; singleton sources keep the same composition model
without forcing a separate API.

## Plural Sources and Singular Values

### `SPACES -> SPACE`

`SPACES` generates definite coordinate Spaces. One `SPACE` owns:

- the explicit time coordinate;
- non-temporal axes or relational coordinates;
- rank and coordinate relations;
- finite extent or shape when applicable;
- support rules; and
- boundary/access behavior when applicable.

Time is not implicit. Ordinary discrete examples use coordinate forms such as:

```text
(t)
(t, x)
(t, x, y)
(t, x, y, z)
(t, vertex)
```

Names such as line, grid, or graph may be convenient constructors, but they do
not require unrelated runtime subclasses. They resolve to coherent coordinate
Spaces.

For example, one source may combine:

```text
shapes     = {5x5, 11x11}
boundaries = {fixed(0), fixed(1), periodic}
```

and yield six definite Spaces:

```text
SPACE(5x5,  fixed(0))
SPACE(5x5,  fixed(1))
SPACE(5x5,  periodic)
SPACE(11x11, fixed(0))
SPACE(11x11, fixed(1))
SPACE(11x11, periodic)
```

Shape belongs to Space because it determines which coordinates exist.
Boundary behavior belongs to Space because it determines how reads behave at
the limits of those coordinates.

### `ALPHABETS -> ALPHABET`

`ALPHABETS` generates definite Alphabets. One `ALPHABET` is the exact set or
value vocabulary admitted at Space coordinates.

An Alphabet can be a finite set, numeric range, tagged union, product, or
another simple value description. Dynamic activity belongs in state values
rather than in a separate Frontier.

For a Turing-style machine with tape symbols `Gamma` and controller states
`Q`, a useful per-coordinate Alphabet is:

\[
A=\operatorname{Inactive}(\Gamma)
  \cup
  \operatorname{Active}(Q\times\Gamma).
\]

With two tape symbols and two controller states, it contains six values:

```text
Inactive(0)
Inactive(1)
Active(0, 0)
Active(0, 1)
Active(1, 0)
Active(1, 1)
```

An Alphabet source can generate binary, ternary, or larger definite
Alphabets. Each generated Alphabet remains reusable anywhere its values are
compatible.

### `NEIGHBORHOODS -> NEIGHBORHOOD`

`NEIGHBORHOODS` generates definite read/dependency relations. One
`NEIGHBORHOOD` defines exactly what a Rule observes when constructing the next
state.

Examples include:

- an ordered offset tuple such as `(left, self, right)`;
- a compound collection of separately summarized regions;
- a graph-relative neighborhood;
- an indirect lookup whose address is stored in state;
- a temporal lookup into earlier slices; or
- a global observation when a family genuinely requires one.

Neighborhood is an input description. It does not grant write permission and
does not select mutable sites.

### `RULES -> RULE`

`RULES` generates definite Rules. One `RULE` is one selected transition law,
not an unresolved rule family or rule number.

The Rule source may use a rule scheme such as:

```text
EXHAUSTIVE
TOTALISTIC
OUTER_TOTALISTIC
THRESHOLD
GATED
ALGEBRAIC
```

The scheme determines how the resolved Alphabet and Neighborhood define the
space of possible mappings. The Rule source then enumerates, samples, or
otherwise constructs individual definite Rules from that space.

For an elementary cellular automaton:

```text
ALPHABET    = {0, 1}
NEIGHBORHOOD = (left, self, right)
RULES       = exhaustive binary lookup tables
```

There are eight possible Neighborhood inputs and therefore 256 definite
Rules. Rule 30 and Rule 90 are two different `RULE` values and produce two
different SimplePrograms.

A Rule constructs the next complete state. It does not return CRUD patches,
replacement instructions, `KEEP`, or a semantic Frontier.

## Preset

A `PRESET` is the coherent combination of:

```text
SPACES
ALPHABETS
NEIGHBORHOODS
RULES
```

It generates definite SimplePrograms:

```text
PRESET -> SIMPLEPROGRAMS
```

Preset expansion is compatibility-aware rather than an unconditional
Cartesian product. Rule generation may depend on the selected Space,
Alphabet, and Neighborhood. A two-dimensional Neighborhood is not paired with
a one-dimensional Space, and a binary exhaustive Rule is not paired with an
Alphabet it cannot consume.

Conceptually:

```python
for space in SPACES:
    for alphabet in ALPHABETS:
        for neighborhood in NEIGHBORHOODS:
            for rule in RULES(space, alphabet, neighborhood):
                if compatible(space, alphabet, neighborhood, rule):
                    yield SimpleProgram(
                        space=space,
                        alphabet=alphabet,
                        neighborhood=neighborhood,
                        rule=rule,
                    )
```

This is explanatory pseudocode, not a requirement to build a general-purpose
constraint solver. Presets may use direct generators tailored to the family
they describe.

A Preset can be declared in an ordinary Python module, much like the existing
PE config and dataset recipe files. It describes a reusable family of definite
SimplePrograms; it is not itself executable dynamics.

## SimpleProgram and Dynamics

One `SIMPLEPROGRAM` contains exactly four definite values:

```python
@dataclass(frozen=True)
class SimpleProgram:
    space: Space
    alphabet: Alphabet
    neighborhood: Neighborhood
    rule: Rule
```

Conceptually:

```text
SIMPLEPROGRAM = SPACE + ALPHABET + NEIGHBORHOOD + RULE
```

A SimpleProgram is one definite **Dynamics**: it defines the admissible state
world and one exact law of evolution. `Dynamics` is the mathematical role of a
SimpleProgram, not an additional required field or wrapper.

Nothing inside a SimpleProgram remains to be selected:

- Space has one exact coordinate system, extent, and boundary behavior.
- Alphabet has one exact value vocabulary.
- Neighborhood has one exact observation relation.
- Rule is one exact selected mapping.

Changing any of these produces another SimpleProgram, though both may remain
members of the same Preset and canonical taxonomy family.

Seed is deliberately absent. Changing the initial condition does not change
the dynamics.

## Seeds

`SEEDS` is a separate source of definite `SEED` values:

```text
SEEDS -> SEED
```

One Seed is one definite initial state. A Seed source may generate structured,
random, enumerated, or hand-authored initial states.

Seeds are not generated *by* one SimpleProgram. The two sources are
independent and are paired by compatibility later. One Seed may work with
many Spaces, Alphabets, Neighborhoods, and Rules.

For example, the same binary `11x11` Seed can be paired with:

```text
SPACE(11x11, fixed(0))
SPACE(11x11, fixed(1))
SPACE(11x11, periodic)
```

Boundary behavior changes the dynamics at the edge; it does not change the
initial values inside the `11x11` coordinate set.

Seed compatibility ordinarily asks only whether:

- its initial coordinates/support fit the selected Space; and
- its values are admitted by the selected Alphabet.

A Seed can therefore be compatible with multiple Spaces and multiple
Alphabets. It is not tied to a single Rule.

Space remains the owner of geometry. A Seed has coordinate-indexed initial
values and therefore has a realized footprint, but it does not define boundary
behavior or the meaning of the surrounding coordinate world.

## Trajectory

A `TRAJECTORY` combines one definite SimpleProgram and one definite compatible
Seed:

```text
SIMPLEPROGRAM + SEED -> TRAJECTORY
```

Mathematically, the Dynamics plus its initial condition determines a path
through state space. A Trajectory denotes that path whether or not every state
has already been materialized.

The compatible Trajectories formed from plural sources are:

\[
\{(P,S)\in\mathrm{SIMPLEPROGRAMS}\times\mathrm{SEEDS}
  \mid S\text{ is compatible with }P\}.
\]

A minimal target value is therefore:

```python
@dataclass(frozen=True)
class Trajectory:
    program: SimpleProgram
    seed: Seed
```

Trajectory has no rollout horizon, batching policy, serialization format, or
PE metadata. Those concerns do not change the path selected by its Dynamics
and initial condition.

## Explicit Time and Immutable State

For the ordinary discrete case, Seed supplies the complete state at `t=0`.
The Rule constructs a complete new state at `t+1` from Neighborhood
observations over earlier state.

Nothing at time `t` is updated, replaced, deleted, or overwritten. Even an
unchanged logical value has a new occurrence at a new coordinate:

\[
X_{t+1}(c)=X_t(c),
\]

where `(t,c)` and `(t+1,c)` are distinct addresses. Earlier time coordinates
remain immutable.

For a fixed finite Space, every admitted spatial coordinate receives a value
in the new slice. An implementation may share persistent structure or use a
lossless compressed representation, but those are implementation details.

There is no semantic `FRONTIER`. Dynamic activity is represented by Alphabet
values or derived from values, coordinates, and support. A compiler may derive
active sites as an optimization without adding them to SimpleProgram identity.

## Rollout and Episode: Deliberately Deferred

The only settled relationship is:

```text
rollout(TRAJECTORY, RESOURCES/LIMIT) -> EPISODE
```

No semantics beyond that relationship are settled here. In particular, this
document does not yet define what counts as a resource or limit, how rollout
evaluates a Trajectory, or what an Episode contains.

The following are intentionally **not** specified yet:

- whether the public limit is named `steps`, `limit`, duration, depth, event
  count, or something family-specific;
- whether resource controls belong in the same call;
- the concrete Episode fields and array layout;
- branching, stochastic, continuous, or solver-specific realization details;
- batching and streaming; and
- serialization into PE examples.

No provisional `RolloutPlan`, `Trace`, `Stream`, or ANKoS-level manifest object
is introduced. Those names are unnecessary for the settled semantic graph.

Until rollout is designed, the conceptual spelling is only:

```python
trajectory = ca.Trajectory(program=simple_program, seed=seed)
episode = ca.rollout(trajectory, ...)
```

The ellipsis is intentional.

## Relationship to PE

ANKoS defines:

```text
PRESET
SIMPLEPROGRAM
SEEDS / SEED
TRAJECTORY
rollout(...)
EPISODE
```

PE may later define manifests, selection policies, streams, serialization,
train/evaluation splits, and batches around those objects. The current PE
`Dynamics`, `PlannedEpisode`, and `RuntimeEpisode` implementation does not
dictate ANKoS terminology and can be repaired after the semantic API is stable.

In particular, PE should eventually resolve one definite Rule before creating
a SimpleProgram, pair that program with a definite Seed to create a
Trajectory, and ask ANKoS to realize an Episode. What PE does with the returned
Episode remains a downstream concern.

## Catalog and Taxonomy

The canonical SPF families remain descriptive taxonomy and development
obligations. A family may provide Presets, but a family ID is not an executor,
runtime subclass, or additional SimpleProgram field.

The levels are distinct:

```text
canonical family     descriptive mechanics/taxonomy family
Preset               generator of definite SimplePrograms
SimpleProgram        one definite Dynamics
Trajectory           one Dynamics paired with one initial condition
Episode              eventual output of rollout; definition deferred
```

Changing a selected Space, Alphabet, Neighborhood, or Rule creates another
SimpleProgram. Changing only Seed creates another Trajectory under the same
SimpleProgram. The effect of changing eventual rollout limits or resources is
left to the later rollout design.

## Migration Direction

The current runtime should eventually move as follows:

| Current concept | Target concept |
|---|---|
| `CarrierContract` plus Carrier boundary | definite Space |
| configuration geometry mixed into Seed | Space owns geometry; Seed owns initial values |
| `WritableRegion` / `Frontier` | removed from semantic API |
| active-site selection | Alphabet/state or a derived execution optimization |
| patch dispositions | complete next-state construction |
| Seed inside `SimpleProgram` | Seed paired later in `Trajectory` |
| parameterized catalog builder | Preset producing definite SimplePrograms |
| selected rule ID outside the dynamics | definite Rule inside `SimpleProgram` |
| PE planning and serialization types | downstream integration, redesigned later |

This document does not authorize a mechanical migration that preserves empty
builders or vacuous catalog stubs. Implement each abstraction only when it has
real semantics.

## Short Form

```text
SPACES        -> SPACE
ALPHABETS     -> ALPHABET
NEIGHBORHOODS -> NEIGHBORHOOD
RULES         -> RULE

SPACES + ALPHABETS + NEIGHBORHOODS + RULES -> PRESET

SPACE + ALPHABET + NEIGHBORHOOD + RULE -> SIMPLEPROGRAM

PRESET -> SIMPLEPROGRAMS
SEEDS  -> SEED

SIMPLEPROGRAM + SEED -> TRAJECTORY

rollout(TRAJECTORY, RESOURCES/LIMIT) -> EPISODE
```

Space owns coordinates, explicit time, shape, support, and boundary behavior.
Alphabet owns admitted values. Neighborhood owns observation. Rule is one
definite selected transition law. Seed remains independent. Preset generates
SimplePrograms; compatible program/Seed pairs define Trajectories. Rollout and
Episode remain intentionally unresolved beyond their relationship.
