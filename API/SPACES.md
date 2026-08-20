# `SPACES -> SPACE`

## Purpose

`SPACES` is a source of one or more definite `SPACE` values. A `SPACE`
describes the coordinate world in which a SimpleProgram operates.

```text
SPACES -> SPACE
```

The plural name is the generator. The singular name is one resolved choice.
The generator may be a tuple, iterator, generator function, or small
declarative object. This distinction does not require a hierarchy of runtime
classes.

## One Definite Space

A `SPACE` owns the coordinate rules that remain fixed for the dynamics:

- explicit time coordinates and their ordering;
- non-temporal rank and axes;
- coordinate relations, such as adjacency or incidence;
- the extent law: finite, infinite, or dynamically changing;
- the support law: which coordinate sets constitute valid slices; and
- boundary and out-of-range access behavior when boundaries exist.

Common coordinate forms include:

```text
(t)
(t, x)
(t, x, y)
(t, x, y, z)
(t, vertex)
```

Names such as point, line, grid, or graph may be useful constructors. The
semantic result is still a coherent coordinate Space, not a requirement for a
different runtime subsystem for every name.

`SPACE` is definite when all of its coordinate rules and policies are
selected. It may nevertheless accept more than one concrete finite extent.
Shape polymorphism is not an unresolved Space choice.

## Shape and Extent Ownership

Concrete finite shape belongs to `SEED`, not `SPACE`.

A finite rectangular Space can state:

```text
time             = discrete
spatial axes     = (x, y)
extent law       = finite rectangle supplied by Seed
boundary         = periodic
```

It does not need to choose `5x5` or `11x11`. A compatible Seed supplies that
realized extent when it is paired with the SimpleProgram.

This distinction lets one SimpleProgram operate on multiple input sizes. It
is analogous to a convolution whose operation is definite even though its
input image dimensions are not fixed in advance.

The extent law still belongs to Space:

- A **finite** Space says that Seed supplies the complete bounded extent.
- An **infinite** Space says that the world is infinite; a Seed's finite
  footprint is not the world extent.
- A **dynamic-support** Space says how later slices may have a different
  support from the initial slice.

Space may constrain admissible extents, such as requiring a nonempty
rectangle or a particular rank. Such a constraint is not the concrete extent
itself.

## Boundary Behavior

Boundary behavior belongs to Space because it changes how coordinates are
read at the edge of a finite world.

Examples include:

- `periodic`, which wraps using the concrete extent supplied by Seed;
- `fixed(0)` or `fixed(1)`, which returns a selected exterior value;
- reflection or clamping, when a family requires them; and
- no boundary for an infinite Space.

Changing the boundary policy changes `SPACE` and therefore changes the
SimpleProgram. Changing only the compatible Seed shape does not.

A fixed boundary value must be admitted by the selected Alphabet. Boundary
reads do not add hidden cells to Seed and do not rewrite its initial values.

## What Space Does Not Own

Space does not own:

- the concrete finite dimensions of an initial state;
- the initial values at coordinates;
- the admitted value vocabulary;
- the Neighborhood observed by the Rule;
- the selected transition Rule;
- a semantic Frontier or active-site list; or
- rollout limits, resources, batching, or serialization.

In particular, a `5x5` world and an `11x11` world can instantiate the same
finite, shape-polymorphic Space.

## Generator Behavior

A usable `SPACES` source yields at least one `SPACE`. Each yielded value has
one selected rank, coordinate relation, extent law, support law, and boundary
policy.

For example:

```python
SPACES = spaces.rectangular(
    rank=2,
    extent="finite-from-seed",
    boundaries=(fixed(0), fixed(1), periodic),
)
```

Conceptually, this yields three Spaces:

```text
SPACE(t+2D, finite-from-seed, fixed(0))
SPACE(t+2D, finite-from-seed, fixed(1))
SPACE(t+2D, finite-from-seed, periodic)
```

It does not yield separate `5x5` and `11x11` Spaces. Those dimensions belong
to Seeds.

The spelling above is illustrative. The first API does not need a general
parameter framework or constraint solver.

## Compatibility

Space participates in two stages of compatibility.

During Preset expansion:

- Alphabet must admit any literal boundary values.
- Neighborhood coordinates and relations must make sense in the Space.
- Rule outputs must obey the Space's support and coordinate laws.

When a SimpleProgram is paired with a Seed:

- Seed coordinates must use the Space's axes and rank;
- a finite Seed extent must satisfy the Space's finite-extent law; and
- an infinite or dynamic-support Seed representation must satisfy the
  corresponding support law.

Compatibility should be expressed by the smallest direct checks needed by a
family. It is not a mandate for a defensive capability framework.

## Identity

Two Spaces are semantically different when any coordinate rule that affects
evolution differs, including:

- time or spatial rank;
- axis or relational structure;
- finite, infinite, or dynamic extent law;
- support law; or
- boundary behavior.

For a shape-polymorphic finite Space, concrete dimensions are not part of
Space identity. The same Space paired with differently shaped Seeds still
belongs to the same SimpleProgram.

## Relationship to the Other Objects

```text
SPACES + ALPHABETS + NEIGHBORHOODS + RULES -> PRESET

SPACE + ALPHABET + NEIGHBORHOOD + RULE -> SIMPLEPROGRAM

SIMPLEPROGRAM + compatible SEED -> TRAJECTORY
```

Space supplies the coordinate laws. Seed later realizes the initial extent
and values. Their compatibility is established when a Trajectory is formed.
