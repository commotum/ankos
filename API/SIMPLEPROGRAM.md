# SIMPLEPROGRAM

Status: **normative target specification**

## Definition

```text
SPACE + ALPHABET + NEIGHBORHOOD + RULE -> SIMPLEPROGRAM
```

A SimpleProgram is one definite dynamics. It states where evolution occurs,
which values may occur, what information is observed, and one exact law that
maps those observations into the next state.

```python
SimpleProgram(
    space=space,
    alphabet=alphabet,
    neighborhood=neighborhood,
    rule=rule,
)
```

This spelling is conceptual. The specification does not require a particular
Python class hierarchy.

## Fields

| Field | Meaning |
|---|---|
| `SPACE` | One definite coordinate and boundary law |
| `ALPHABET` | One definite vocabulary of admissible values |
| `NEIGHBORHOOD` | One definite observation/dependency relation |
| `RULE` | One definite selected transition law |

Every field is singular and selected. A SimpleProgram never contains a range
of boundaries, several candidate Alphabets, an unresolved rule scheme, or a
rule ID that still needs to be chosen.

## What “Definite” Means

Definite means that every law has been selected. It does **not** mean that
every compatible input has the same concrete shape.

A finite rectangular two-dimensional Space with periodic boundaries can be
fully specified without deciding whether a later Seed is `5x5`, `11x11`, or
`100x80`. The Space already says how coordinates and boundaries behave; the
Seed supplies the concrete initial extent.

This is ordinary input polymorphism, not an unresolved program parameter. A
convolution kernel can be definite without fixing image size, and a
SimpleProgram can be definite without fixing Seed shape.

## Ownership

A SimpleProgram owns the complete reusable dynamics:

- coordinate rank and relations through Space;
- finite, infinite, fixed-support, or changing-support law through Space;
- boundary behavior through Space;
- admitted values through Alphabet;
- observations through Neighborhood; and
- one exact transition through Rule.

A SimpleProgram does **not** own:

- a Seed;
- concrete finite dimensions supplied by a Seed;
- initial values or initial realized support;
- a rollout horizon or resource budget;
- an Episode;
- batching, streams, manifests, or serialization; or
- a semantic Frontier.

## Coherence

The four selected values must describe one coherent dynamics:

- Neighborhood coordinates and relations must make sense in Space.
- Neighborhood observations must be values that Rule understands.
- Rule outputs must belong to Alphabet.
- Any value used by a fixed boundary law must belong to Alphabet.
- Rule must respect the support and coordinate laws declared by Space.

These are semantic relationships, not a requirement for a general constraint
solver or defensive runtime framework. A Preset may guarantee coherence by
construction.

## Identity

Changing any of the four fields creates a different SimpleProgram:

```text
different SPACE        -> different SIMPLEPROGRAM
different ALPHABET     -> different SIMPLEPROGRAM
different NEIGHBORHOOD -> different SIMPLEPROGRAM
different RULE         -> different SIMPLEPROGRAM
```

Changing only Seed, Seed shape, rollout limit, or later execution resources
does not change the SimpleProgram.

Two SimplePrograms may still belong to the same Preset or canonical family.
Taxonomy membership is broader than SimpleProgram identity.

## Example: Elementary Cellular Automaton

One definite elementary cellular automaton might contain:

```text
SPACE
    explicit discrete time
    one spatial integer axis
    finite extent supplied by Seed
    periodic boundary

ALPHABET
    {0, 1}

NEIGHBORHOOD
    ordered offsets (-1, 0, +1)

RULE
    exact lookup table selected as Rule 30
```

This is one SimpleProgram. It can be paired with a length-5 Seed, a length-101
Seed, or any other compatible finite Seed without changing its dynamics.

Replacing periodic boundary behavior with fixed-zero boundary behavior creates
another Space and therefore another SimpleProgram. Replacing only the Seed
creates another Trajectory under the same SimpleProgram.

## Relationships

```text
PRESET -> SIMPLEPROGRAMS

SIMPLEPROGRAM + SEED -> TRAJECTORY
```

See [PRESET.md](PRESET.md), [SEEDS.md](SEEDS.md), and
[TRAJECTORY.md](TRAJECTORY.md).
