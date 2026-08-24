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

## The five inputs

| Value | Minimal representation | Responsibility |
| --- | --- | --- |
| Space | small frozen record | Explicit axes, extent law, and boundary |
| Alphabet | `frozenset` or membership function | Values admitted at coordinates |
| Neighborhood | offset tuple or address function | Ordered coordinates read for one output coordinate |
| Rule | ordinary named callable | Exact map from observed values to a successor value |
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
from ca import Seed, SimpleProgram, Space, Trajectory, rollout
from ca import spaces


space = Space(
    axes=("t", "x"),
    extent="seed-sized finite box",
    boundary=spaces.fixed(0),
    coordinates=spaces.box_coordinates,
)

alphabet = frozenset({0, 1})

neighborhood = (
    (0, -1),
    (0,  0),
    (0,  1),
)


def any_observed_value(observed, source):
    del source
    return int(any(observed))


program = SimpleProgram(
    space=space,
    alphabet=alphabet,
    neighborhood=neighborhood,
    rule=any_observed_value,
)

seed = Seed(
    shape=(5,),
    values={
        (0, 0): 0,
        (0, 1): 0,
        (0, 2): 1,
        (0, 3): 0,
        (0, 4): 0,
    },
)

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

Space owns axes, coordinate interpretation, and boundary behavior. Seed owns
the concrete shape/support. The same periodic t+2D SimpleProgram can therefore
run on an 11x11 Seed and a 101x57 Seed.

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

A regular local Neighborhood is usually just an ordered offset tuple. Offsets
include a zero time component so reads remain in the current slice.

When adjacency is not a fixed translation, use a small function:

```python
def adjacent(source, seed):
    t, address = source
    return tuple(
        (t, neighbor)
        for neighbor in seed.relations["adjacent"][address]
    )
```

Space resolves selected addresses through the chosen boundary law. Rule then
receives the ordered observed values.

There is no separate Frontier in the SimpleProgram. A family with a moving
active site can encode active and inactive cases directly in Alphabet values.
Neighborhood reads the necessary local values, Rule moves the activity tag,
and every coordinate still receives a value in the next complete slice.

## A Rule is already selected

An exhaustive table, totalistic law, or threshold construction may generate
many Rules. `SimpleProgram.rule` is one exact callable produced by that source.

For an elementary cellular automaton, the binary Alphabet and ordered
three-cell Neighborhood determine eight possible inputs. A rules source may
generate 256 callables, but one SimpleProgram receives one selected table.

Rule has the small execution shape:

```python
def rule(observed, source):
    return one_alphabet_value
```

Its Python name can provide a human identifier. A table index can remain
ordinary attached metadata when useful.

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
- every value belongs to Alphabet;
- required relation data is available.

## Plural sources and future presets

Plural names describe ordinary source functions or iterables:

```text
SPACES        -> SPACE
ALPHABETS     -> ALPHABET
NEIGHBORHOODS -> NEIGHBORHOOD
RULES         -> RULE
SEEDS         -> SEED
```

A future program preset can be one normal module with explicit loops:

```python
def programs():
    for space in spaces():
        for alphabet in alphabets():
            for neighborhood in neighborhoods(space):
                for rule in rules(alphabet, neighborhood):
                    yield SimpleProgram(
                        space=space,
                        alphabet=alphabet,
                        neighborhood=neighborhood,
                        rule=rule,
                    )
```

A seed preset can independently yield structured or random Seeds over several
shapes. Workload code pairs compatible programs and Seeds to make
Trajectories, then selects a rollout limit to produce Episodes.

Preset is a module convention, not a required class. The initial refactor stops
at a preset-ready kernel and does not add canonical preset implementations.

## Execution scope

The initial reference executor provides:

```python
next_state = step(trajectory, state)
episode = rollout(trajectory, limit=steps)
```

`limit` is a nonnegative integer number of discrete successor steps. The Seed
State is included, so an Episode has `limit + 1` States.

Resource budgets, event stopping, solver controls, and non-discrete time are
intentionally deferred. They should be designed from concrete requirements
rather than anticipated through a larger universal type system.

## Documentation

The concise contract is in [api.md](api.md). Field-by-field specifications are
indexed in [API/README.md](API/README.md).
