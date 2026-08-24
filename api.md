# ANKoS API

This document specifies the desired coordinate-first ANKoS kernel.

The architecture is:

```text
SPACES        -> SPACE
ALPHABETS     -> ALPHABET
NEIGHBORHOODS -> NEIGHBORHOOD
RULES         -> RULE

SPACE + ALPHABET + NEIGHBORHOOD + RULE -> SIMPLEPROGRAM
SEEDS                                      -> SEED
SIMPLEPROGRAM + SEED                       -> TRAJECTORY
rollout(TRAJECTORY, limit)                  -> EPISODE
```

Every singular value is definite. A `SimpleProgram` contains one selected
Space, one selected Alphabet, one selected Neighborhood, and one selected
Rule. A Seed is deliberately separate because changing an initial condition
does not change the program.

## Ordinary values first

Use the smallest ordinary Python value that expresses each part:

| Name | Representation | Meaning |
| --- | --- | --- |
| `SPACE` | small frozen record | Coordinate axes, extent law, and boundary law |
| `ALPHABET` | `frozenset` or membership function | Values admitted at coordinates |
| `NEIGHBORHOOD` | tuple of offsets or address function | Ordered coordinates read for one output coordinate |
| `RULE` | ordinary named callable | One exact map from observed values to one successor value |
| `SEED` | small frozen record | Realized shape/support and complete initial values |

Only compositions need their own records:

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

No inheritance hierarchy or generic framework is required.

## Package layers

The five primitive namespaces live under `ca.core`: `spaces`, `alphabets`,
`neighborhoods`, `rules`, and `seeds`. Root-level `ca.simpleprograms` owns
composition, while root-level `ca.rollout` owns Trajectory, Episode, and
execution. Shared selection mathematics and optional visualization live under
`ca.utils`; canonical named families live under `ca.catalog`.

The root `ca` package re-exports the normal public names.

## Space and Seed divide responsibility

Space defines the coordinate law, not a semantic kind of world. Its axes
always include time explicitly and begin with `t`:

```text
(t,)          t-only
(t, x)        t+1D
(t, x, y)     t+2D
(t, x, y, z)  t+3D
(t, v)        time plus an arbitrary address
```

The final form is enough for relation-driven structures: `v` is an ordinary
address, while a Seed may supply the realized addresses and their relations.
It does not require a `Graph`, `Vertex`, or other semantic coordinate class.

Space owns:

- the axes and coordinate rank;
- the law for enumerating or interpreting coordinates;
- whether an exterior exists and how exterior reads resolve.

Seed owns:

- the realized shape or support;
- every value in the initial state;
- any concrete relation data needed to interpret those addresses.

Consequently, changing a Seed from length 5 to length 100 does not create a
new SimpleProgram. Changing fixed boundary behavior to periodic behavior does.

## Explicit time and immutable states

Time is never implicit. A State is a complete mapping from coordinates at one
time to values. Execution preserves all earlier States and constructs a new,
complete slice at the next time:

```text
State at t -> complete State at t+1
```

An unchanged logical value is copied to its new `(t+1, ...)` coordinate. It is
not an update to the old coordinate. There are no replace, delete, CRUD, or
`KEEP` operations in the public semantics.

`step(trajectory, state)` constructs one successor State. `rollout` includes
the Seed State and then calls `step` exactly `limit` times.

## Selection and activity

A Neighborhood selects read addresses. Regular spaces usually use ordered
offset tuples; relation-driven spaces use a small address function. Space
resolves any selected address through its boundary law before the Rule sees
the observed values.

`ca.selector` provides shared coordinate mathematics beneath these values:
predicate composition, metrics, filtering, translation, relation following,
and deterministic ordering. Spaces, Neighborhoods, and Seed sources may use
those helpers. Selector is not a sixth input and has no runtime object model.

There is no separate Frontier field. When only some logical sites are active,
activity is represented in ordinary Alphabet values and interpreted by the
Rule. Every realized coordinate still receives a value at the new explicit
time.

## Plural sources and future presets

Plural names mean ordinary iterables or functions that yield singular values:

```text
SPACES        -> one or more definite Space values
ALPHABETS     -> one or more definite Alphabet values
NEIGHBORHOODS -> one or more definite Neighborhood values
RULES         -> one or more definite Rule callables
SEEDS         -> one or more definite Seed values
```

A future preset is a normal Python module containing such functions and
explicit loops. It is not a `Preset` class, parameter solver, or hidden product
engine. A program preset may combine the first four sources into
`SimpleProgram` values. A separate Seed source may then be paired with any
compatible program to form Trajectories.

Compatibility is checked where values meet. Sources may accept dependencies
directly—for example, `neighborhoods(space)` and
`rules(alphabet, neighborhood)`—instead of encoding a new framework.

Goal 9 stops at this preset-ready interface. It does not ship canonical preset
implementations.

## Deferred execution questions

The initial executor advances discrete integer time and accepts a nonnegative
step `limit`. Wall-clock budgets, solver resources, event-driven time, and
continuous-time integration are later execution designs. They should not make
the small discrete kernel more abstract before a concrete family requires it.

The detailed contracts are in [API/README.md](API/README.md).
