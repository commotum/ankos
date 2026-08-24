# Desired API

These files define the desired minimal ANKoS API. They are the design target,
not a promise to preserve earlier abstractions.

## Data flow

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

## Package layers

The five primitive namespaces live under `ca.core`. Composition lives in
root-level `ca.simpleprograms`, and execution lives in root-level `ca.rollout`.
Mechanics-neutral selection helpers and optional visualization live under
`ca.utils`; named family implementations and their runnable compositions live
under `ca.catalog`. The root package re-exports the normal public API.

The singular values are fully selected. Plural names are ordinary source
functions or iterables used only when they produce several singular values;
they are not a mandatory interface for every catalog module.

## Documents

- [SPACES.md](SPACES.md): explicit coordinate axes, enumeration, and boundary.
- [ALPHABETS.md](ALPHABETS.md): admitted values and canonical finite ordering.
- [NEIGHBORHOODS.md](NEIGHBORHOODS.md): ordered read-address selection.
- [RULES.md](RULES.md): one exact stable successor-value callable.
- [SEEDS.md](SEEDS.md): realized support and complete initial values.
- [SIMPLEPROGRAM.md](SIMPLEPROGRAM.md): reusable composition of the four
  dynamics values.
- [TRAJECTORY.md](TRAJECTORY.md): one program paired with one Seed.
- [EPISODE.md](EPISODE.md): the complete immutable States produced by rollout.
- [PRESET.md](PRESET.md): ordinary catalog source modules, not a class.

## Design line

Coordinates remain ordinary tuples. Time is the first component of every
coordinate. Shape and support belong to Seed; boundary behavior belongs to
Space. Neighborhood offsets are spatial-only even though State coordinates
retain explicit time. Rule maps the selected values to one new value.

`ca.selector` is a supporting function library for coordinate predicates,
metrics, translation, filtering, relations, and ordering. Spaces,
Neighborhoods, and Seed sources may reuse it, but Selector is not an additional
SimpleProgram component.

The executor creates a complete new time slice and leaves every prior slice
untouched. No public Frontier, mutation operation, semantic coordinate class,
inheritance tree, or generic framework is part of this design.
