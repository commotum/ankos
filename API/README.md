# ANKoS Target API

Status: **normative greenfield specification**

These documents define the desired semantic API without inheriting vocabulary,
object boundaries, or implementation constraints from earlier runtimes or
downstream applications.

## Object Graph

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

## Documents

| Specification | Defines |
|---|---|
| [SPACES.md](SPACES.md) | Generation and meaning of coordinate and boundary laws |
| [ALPHABETS.md](ALPHABETS.md) | Generation and meaning of admissible values |
| [NEIGHBORHOODS.md](NEIGHBORHOODS.md) | Generation and meaning of observation relations |
| [RULES.md](RULES.md) | Rule schemes and generation of exact selected transition laws |
| [SEEDS.md](SEEDS.md) | Independent generation of exact initial states and concrete extents |
| [PRESET.md](PRESET.md) | Coherent generation of definite SimplePrograms |
| [SIMPLEPROGRAM.md](SIMPLEPROGRAM.md) | One definite reusable dynamics |
| [TRAJECTORY.md](TRAJECTORY.md) | One SimpleProgram paired with one Seed |
| [EPISODE.md](EPISODE.md) | Reserved rollout result whose detailed contract is deferred |

## Central Ownership

| Concern | Owner |
|---|---|
| Explicit time, rank, axes, coordinate relations | Space |
| Finite/infinite/dynamic extent law | Space |
| Boundary behavior | Space |
| Concrete initial shape or extent | Seed |
| Initial values and realized initial support | Seed |
| Admitted values | Alphabet |
| Read/dependency relation | Neighborhood |
| One exact selected transition law | Rule |
| Reusable dynamics | SimpleProgram |
| Dynamics plus initial condition | Trajectory |
| Rollout result | Episode, detailed meaning deferred |

For a finite shape-polymorphic Space, Seed supplies the concrete dimensions.
For an infinite Space, Seed support is only initial support and does not become
world extent.

## Plain Implementation Principle

The uppercase singular and plural words describe roles, not mandatory class
families. A plural source can be an ordinary iterable, generator function, or
small declarative value. A singular result can be plain immutable data or a
callable law.

Prefer the smallest representation that preserves the specified meaning. Do
not add framework layers, defensive type systems, or named intermediate
objects without a concrete semantic need.

## Rollout Boundary

The specification deliberately stops at:

```text
rollout(TRAJECTORY, RESOURCES/LIMIT) -> EPISODE
```

The exact rollout call and Episode representation will be resolved later.
