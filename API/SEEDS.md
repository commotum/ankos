# `SEEDS -> SEED`

## Purpose

`SEEDS` is an independent source of one or more definite `SEED` values. A
`SEED` is one complete initial state, including its concrete realized shape or
support.

```text
SEEDS -> SEED
```

Seeds are generated separately from Presets and SimplePrograms. They are
paired with SimplePrograms later through compatibility.

## One Definite Seed

A `SEED` owns:

- the complete initial coordinate-to-value assignment;
- the concrete finite shape or extent, when the Space is finite;
- the realized initial support or footprint; and
- the definite starting time admitted by Space, ordinarily `t=0`.

For a finite dense grid, the Seed contains a value for every coordinate in its
shape. For example, an `11x11` Seed carries both the `11x11` extent and the 121
initial values.

For an infinite Space, a Seed must still denote a complete initial state. It
may do so intensionally, such as a default value plus finitely many overrides:

```python
seed = Seed(
    time=0,
    default=0,
    values={0: 1},
)
```

Here `{0: 1}` is the non-default footprint. It does not make the infinite
world one cell wide. Infinity is the Space's extent law; the initial values
and their compact representation belong to Seed.

## Shape Ownership

Concrete finite shape belongs to Seed.

This allows one shape-polymorphic SimpleProgram to be paired with Seeds of
different sizes:

```text
SEED(5x5, values=...)
SEED(11x11, values=...)
```

The finite Space declares what kind of extent is allowed, such as a finite
rectangle. The Seed selects and realizes one such extent.

The distinction between extent and footprint matters:

- In a finite Space, Seed shape is the complete world extent.
- In an infinite Space, the world extent comes from Space; Seed may have a
  finite non-default footprint inside it.
- In a dynamic-support Space, Seed supplies only the initial support; Space
  and Rule determine what supports later slices may have.

## What Seed Does Not Own

Seed does not own:

- spatial rank, axes, or coordinate relations;
- whether the world is finite, infinite, or dynamically supported;
- boundary behavior;
- the general value vocabulary;
- Neighborhood semantics;
- the selected Rule;
- rollout limits or resources; or
- downstream selection, serialization, or batching concerns.

A Seed may contain active values such as `Active(head_state, cell_state)`, but
those are ordinary values from a compatible Alphabet. Seed does not introduce
a separate Frontier.

## Generator Behavior

A usable `SEEDS` source yields at least one definite Seed. It may enumerate or
generate:

- several concrete shapes;
- hand-authored patterns;
- structured families such as centered, striped, or symmetric states;
- exhaustive finite initial states; or
- definite samples from a random recipe.

For example:

```python
SEEDS = seeds.rectangles(
    shapes=((5, 5), (11, 11)),
    patterns=(centered_one, bernoulli(0.5)),
)
```

Every yielded Seed has resolved coordinates and values. A random recipe may
use a realization key so that its outputs are reproducible, but the recipe is
not itself a definite Seed until its values have been realized.

`SEEDS` is not called as `SEEDS(SimpleProgram)`. It may be configured with
shapes, value choices, or generation methods of its own, while remaining
independent of any one selected Space, Alphabet, Neighborhood, or Rule.

This does not prohibit convenient helpers from accepting context. It means
that semantic Seed ownership and identity do not depend on one
SimpleProgram.

## Compatibility Rather Than Ownership

Plural sources may generate more values than can be paired. A Trajectory is
formed only from a compatible SimpleProgram and Seed.

The ordinary compatibility checks are:

- Seed coordinates and concrete extent satisfy the selected Space;
- Seed values are admitted by the selected Alphabet; and
- the Seed's initial support uses a representation allowed by Space.

There is normally no Seed dependency on one selected Rule or Neighborhood.
Those are parts of the reusable dynamics. If a particular family needs an
additional condition, it can state that condition directly without turning
all Seeds into program-specific objects.

For example, one binary `11x11` Seed can pair with all three of these Spaces:

```text
SPACE(t+2D, finite-from-seed, fixed(0))
SPACE(t+2D, finite-from-seed, fixed(1))
SPACE(t+2D, finite-from-seed, periodic)
```

The boundary policies change what happens during evolution. They do not
change the initial `11x11` values.

The same Seed may also pair with many selected Rules and with any Alphabet
that admits all of its values.

## Identity

Seed identity is determined by its definite initial state:

- starting time;
- realized finite extent or initial support; and
- value at every initial coordinate, whether stored explicitly or described
  by an exact intensional representation.

Changing any of these produces another Seed. Changing provenance, a generator
label, or the random recipe that happened to produce identical values does
not change the semantic initial state.

Changing only Seed changes the Trajectory, not the SimpleProgram.

## Relationship to the Other Objects

```text
PRESET -> SIMPLEPROGRAMS
SEEDS  -> SEED

SIMPLEPROGRAM + compatible SEED -> TRAJECTORY

rollout(TRAJECTORY, RESOURCES/LIMIT) -> EPISODE
```

Preset generation and Seed generation remain independent. Compatibility
filters their possible pairings; it does not make one generator own or produce
the other.
