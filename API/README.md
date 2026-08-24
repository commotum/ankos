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

The singular values are fully selected. The plural names are ordinary source
functions or iterables that may produce several singular values.

## Documents

- [SPACES.md](SPACES.md): explicit coordinate axes, extent law, and boundary.
- [ALPHABETS.md](ALPHABETS.md): admitted values.
- [NEIGHBORHOODS.md](NEIGHBORHOODS.md): ordered read-address selection.
- [RULES.md](RULES.md): one exact successor-value callable.
- [SEEDS.md](SEEDS.md): realized support and complete initial values.
- [SIMPLEPROGRAM.md](SIMPLEPROGRAM.md): reusable composition of the four
  dynamics values.
- [TRAJECTORY.md](TRAJECTORY.md): one program paired with one Seed.
- [EPISODE.md](EPISODE.md): the complete immutable States produced by rollout.
- [PRESET.md](PRESET.md): future ordinary source modules, not a class.

## Design line

Coordinates remain ordinary tuples. Time is the first component of every
coordinate. Shape and support belong to Seed; boundary behavior belongs to
Space. Neighborhood reads addresses, and Rule maps the selected values to one
new value.

The executor creates a complete new time slice and leaves every prior slice
untouched. No public Frontier, mutation operation, semantic coordinate class,
inheritance tree, or generic framework is part of this design.
