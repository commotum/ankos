# ANKoS

ANKoS is a small coordinate-first kernel for defining and executing simple
programs.

The design begins with ordinary values:

```text
SPACE + ALPHABET + NEIGHBORHOOD + RULE -> SIMPLEPROGRAM
SIMPLEPROGRAM + SEED                    -> TRAJECTORY
rollout(TRAJECTORY, limit)               -> EPISODE
```

It deliberately does not begin with a hierarchy of automata, tapes, graphs,
fields, regions, or update mechanisms. Those are descriptions of particular
families. The shared runtime only needs coordinates, values, reads, and one
exact transition rule.

## Package organization

The five primitive value namespaces live together under `ca.core`:

```text
ca/core/
    spaces.py
    alphabets.py
    neighborhoods.py
    rules.py
    seeds.py
```

`ca.simpleprograms` composes the first four values. Root-level `ca.rollout`
pairs a SimpleProgram with a Seed as a Trajectory and produces an Episode.
`ca.utils.selector` supplies shared coordinate mathematics, while
`ca.utils.viz` is optional downstream presentation tooling. Named canonical
families and their runnable modules remain grouped under `ca.catalog`.

The root `ca` package re-exports the ordinary public interface, so this
internal organization does not add import ceremony for normal use.

## The five inputs

| Value | Minimal representation | Responsibility |
| --- | --- | --- |
| Space | small frozen record | Explicit axes, coordinate enumeration, and boundary |
| Alphabet | ordered tuple or membership function | Values admitted at coordinates |
| Neighborhood | offset tuple or address function | Ordered coordinates read for one output coordinate |
| Rule | small stable callable value | Exact map from observed values to a successor value |
| Seed | small frozen record | Realized shape/support and complete initial values |

A SimpleProgram contains the first four. Seed stays separate so the same
program can run from different initial values and over different compatible
realized shapes.

The only other records are the compositions:

```python
@dataclass(frozen=True)
class SimpleProgram:
    space: Space
    alphabet: object
    neighborhood: object
    rule: object


@dataclass(frozen=True)
class Trajectory:
    program: SimpleProgram
    seed: Seed


@dataclass(frozen=True)
class Episode:
    states: tuple[object, ...]
```

No inheritance or generic framework is necessary for the initial kernel.

## Quick example

This anonymous example uses a finite t+1D coordinate space. It is a fixture,
not a canonical preset.

```python
from ca import Rule, SimpleProgram, Trajectory, rollout
from ca import seeds, spaces


space = spaces.cartesian(
    axes=("t", "x"),
    boundary=spaces.fixed(0),
)

alphabet = (0, 1)

neighborhood = (
    (-1,),
    ( 0,),
    ( 1,),
)


def any_observed_value(observed):
    return int(any(observed))


program = SimpleProgram(
    space=space,
    alphabet=alphabet,
    neighborhood=neighborhood,
    rule=Rule(name="any_observed_value", function=any_observed_value),
)

seed = seeds.dense((0, 0, 1, 0, 0))

trajectory = Trajectory(program=program, seed=seed)
episode = rollout(trajectory, limit=2)
```

`episode.states` contains the complete State at `t=0`, followed by complete
States at `t=1` and `t=2`.

## Space means coordinate space

Space is not a semantic category such as “line,” “grid,” or “graph.” It is the
coordinate law required by execution.

Time is always explicit and first:

```text
(t,)          t-only
(t, x)        t+1D
(t, x, y)     t+2D
(t, x, y, z)  t+3D
(t, v)        time plus an arbitrary address
```

The `(t, v)` form covers relation-driven arrangements. `v` may be a string,
integer, tuple, or any other stable address. A Seed supplies the realized
addresses and plain relation mappings; a Neighborhood address function follows
them. There is no need to make `Graph`, `Vertex`, or tiling classes part of the
universal API.

Space owns axes, coordinate enumeration, and boundary behavior. It does not
carry a descriptive `extent` field or a separately coordinated normalization
hook. Generic constructors such as `spaces.cartesian(...)` build the ordinary
coordinate function, while boundary values such as `spaces.periodic()` own
their own resolution behavior. Seed owns the concrete shape/support. The same
periodic t+2D SimpleProgram can therefore run on an 11x11 Seed and a 101x57
Seed.

## States are complete immutable time slices

Every State maps full coordinates from one explicit time to values:

```text
X_t = {(t, ...): value, ...}
```

One step constructs a complete new State:

```text
X_t -> X_(t+1)
```

Nothing at time `t` is overwritten. If a logical cell is unchanged, its value
is copied to a new `(t+1, ...)` coordinate. Earlier States remain intact in the
Episode.

This is not a CRUD model. Rules do not return replacement, deletion, or
`KEEP` instructions. They return ordinary Alphabet values, and the executor
builds the complete successor slice.

## Neighborhoods select read addresses

A regular local Neighborhood is usually just an ordered tuple of spatial
offsets. For a t+1D Space, left/self/right is `((-1,), (0,), (1,))`. The
executor reads those offsets from the current slice; the Neighborhood does not
repeat a meaningless zero time displacement. State coordinates still contain
explicit time.

When adjacency is not a fixed translation, use a small function:

```python
def adjacent(spatial, seed):
    (address,) = spatial
    return tuple(
        (neighbor,)
        for neighbor in seed.relations["adjacent"][address]
    )
```

Neighborhood callables follow the same rule as offset tuples: they accept and
return spatial addresses only. The resolver keeps the explicit source time,
forms full State coordinates, and resolves them through the chosen Space
boundary law. Rule then receives the ordered observed values.

The package separates two implementation layers without adding another
SimpleProgram field:

- `ca.selector` contains reusable coordinate predicates, metrics, filtering,
  translation, relation following, and ordering;
- `ca.neighborhoods` resolves one definite Neighborhood for execution and
  provides common relation-based constructions.

These are ordinary function libraries. There is no `Selector` or
`Neighborhood` class hierarchy.

There is no separate Frontier in the SimpleProgram. A family with a moving
active site can encode active and inactive cases directly in Alphabet values.
Neighborhood reads the necessary local values, Rule moves the activity tag,
and every coordinate still receives a value in the next complete slice.

## A Rule is already selected

An exhaustive table, totalistic law, or threshold construction may generate
many Rules. `SimpleProgram.rule` is one exact stable Rule value produced by that
source.

For an elementary cellular automaton, the binary Alphabet and ordered
three-cell Neighborhood determine eight possible inputs. A rules source may
generate 256 Rule values, but one SimpleProgram receives one selected table.

The default Rule has the small execution shape:

```python
def rule(observed):
    return one_alphabet_value
```

`ca.core.rules.Rule` is a tiny immutable callable value that gives the function
a stable name and optional index. This avoids manufacturing a new anonymous
closure and attaching identity with `setattr` every time a selected Rule is
requested. Coordinate-aware calling conventions should be added only when a
concrete family demonstrates that it needs one.

## Seed is initialization, not dynamics

Seed realizes the concrete support and assigns every initial value. For a
finite Cartesian Space, `shape=(11, 11)` supplies the dimensions. For `(t, v)`,
shape may instead be an ordered address collection.

Changing Seed shape, random draw, or structured pattern creates a different
Trajectory, not a different SimpleProgram. Changing boundary law, Alphabet,
Neighborhood, or exact Rule changes the SimpleProgram.

Compatibility is checked when a program and Seed meet:

- coordinate rank and support match Space;
- the initial State is complete at one explicit time;
- every value belongs to Alphabet.

Plain relation data is validated when a relation-based Neighborhood actually
selects from it.

## Sources and presets

Plural names describe ordinary source functions or iterables only where real
variation exists:

```text
SPACES        -> SPACE
ALPHABETS     -> ALPHABET
NEIGHBORHOODS -> NEIGHBORHOOD
RULES         -> RULE
SEEDS         -> SEED
```

A module should not wrap a single constant in a one-item generator merely to
make every field look uniform. For example, an ECA module can expose one
`ALPHABET` and one `NEIGHBORHOOD`, while `rules()` and `programs()` enumerate
genuine choices. When several inputs really do vary, composition remains
ordinary explicit loops:

```python
def programs(selected_spaces, numbers):
    for space in selected_spaces:
        for rule in rules(numbers):
            yield SimpleProgram(
                space=space,
                alphabet=ALPHABET,
                neighborhood=NEIGHBORHOOD,
                rule=rule,
            )
```

A seed preset can independently yield structured or random Seeds over several
shapes. Workload code pairs compatible programs and Seeds to make
Trajectories, then selects a rollout limit to produce Episodes.

Preset is a module convention, not a required class. The first concrete module
is `ca.catalog.automata.elementary_ca`. It accepts a selected compatible Space,
keeps its binary Alphabet and left/self/right Neighborhood as constants, and
provides real sweeps over exact Wolfram-numbered Rules and SimplePrograms.
Generic Seed helpers construct dense finite initial rows; a centered impulse is
only a convenience built from that generic operation.

## Execution scope

The initial reference executor provides:

```python
next_state = step(trajectory, state)
episode = rollout(trajectory, limit=steps)
```

`limit` is a nonnegative integer number of discrete successor steps. The Seed
State is included, so an Episode has `limit + 1` States.

This executor currently constructs each successor over the same finite support
realized by the Seed. Thus the ECA module executes finite-width ECA under the
selected boundary law. It does not yet claim to execute an infinite integer
line or dynamically changing support.

Resource budgets, event stopping, solver controls, and non-discrete time are
intentionally deferred. They should be designed from concrete requirements
rather than anticipated through a larger universal type system.

## Documentation

The concise contract is in [api.md](api.md). Field-by-field specifications are
indexed in [API/README.md](API/README.md).
