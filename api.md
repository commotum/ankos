# ANKoS Target API

Status: **normative greenfield architecture**

The detailed specifications live in [API/README.md](API/README.md). They define
the desired API directly, without inheriting object boundaries or terminology
from earlier implementations or downstream applications.

## Architecture

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

## Ownership

- Space owns explicit time, rank, axes, coordinate relations, extent law,
  support law, and boundary behavior.
- Seed owns the concrete initial shape or extent, initial values, and initial
  realized support.
- Alphabet owns the admitted values.
- Neighborhood owns the read/dependency relation.
- Rule is one exact selected transition law.
- SimpleProgram is one definite reusable dynamics.
- Trajectory is one SimpleProgram paired with one compatible Seed.
- Episode is the eventual result of rollout; its detailed contract is deferred.

For a finite shape-polymorphic Space, Seed supplies the concrete dimensions.
For an infinite Space, Seed support remains only the initial support and does
not become world extent.

## Specifications

| Document | Subject |
|---|---|
| [SPACES.md](API/SPACES.md) | `SPACES -> SPACE` |
| [ALPHABETS.md](API/ALPHABETS.md) | `ALPHABETS -> ALPHABET` |
| [NEIGHBORHOODS.md](API/NEIGHBORHOODS.md) | `NEIGHBORHOODS -> NEIGHBORHOOD` |
| [RULES.md](API/RULES.md) | `RULES -> RULE` |
| [SEEDS.md](API/SEEDS.md) | `SEEDS -> SEED` |
| [PRESET.md](API/PRESET.md) | plural program sources combined into a Preset |
| [SIMPLEPROGRAM.md](API/SIMPLEPROGRAM.md) | one definite four-field dynamics |
| [TRAJECTORY.md](API/TRAJECTORY.md) | one SimpleProgram plus one Seed |
| [EPISODE.md](API/EPISODE.md) | deferred rollout result |

## Rollout Boundary

Only this relationship is settled:

```text
rollout(TRAJECTORY, RESOURCES/LIMIT) -> EPISODE
```

The rollout signature, limit and resource vocabulary, execution behavior, and
Episode representation will be resolved later.
