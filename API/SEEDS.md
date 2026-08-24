# Seeds

## Definition

A Seed is one concrete initial realization:

```python
@dataclass(frozen=True)
class Seed:
    shape: object
    values: object
    relations: object = ...
```

It contains:

- the realized shape or support;
- a complete immutable value for every realized coordinate at one explicit
  initial time;
- optional plain relation data used by address-based Neighborhoods.

For a finite t+1D realization:

```python
Seed(
    shape=(5,),
    values={
        (0, 0): 0,
        (0, 1): 0,
        (0, 2): 1,
        (0, 3): 0,
        (0, 4): 0,
    },
)
```

The common dense case should not be rebuilt by every catalog family. A generic
helper can derive shape and explicit initial coordinates from ordinary nested
values:

```python
seed = seeds.dense((0, 0, 1, 0, 0))
```

This is the same complete finite row as the expanded mapping above. Family
modules may provide named patterns such as a centered impulse, but those are
thin conveniences over generic Seed construction rather than competing Seed
representations.

For `(t, v)`, `shape` may be an ordered set of realized addresses rather than
a Cartesian dimension tuple, with adjacency supplied as a mapping in
`relations`.

## Why shape belongs here

A SimpleProgram can be fully specified before choosing a finite realization.
The same coordinate and boundary laws may run on a 5-cell, 11-cell, or
100-cell Seed. Concrete shape therefore varies with initial realization, not
with the reusable program.

Space still defines how the Seed's shape is interpreted and how exterior reads
behave. Seed supplies the concrete extent.

## Completeness

A Seed assigns every realized coordinate exactly once at its initial time. It
is not a sparse patch to be merged into mutable storage. The initial State is
already the first complete slice of an Episode.

Every Seed value must belong to the chosen Alphabet before execution. Its
coordinate rank and support must match the chosen Space.

These checks happen when `SimpleProgram` and Seed meet in a Trajectory.
Relation data is validated when a relation-based Neighborhood reads it during
execution. The Seed source does not need to know one exact Rule in advance.

## Independence

Seed is not a `SimpleProgram` field. Changing initial values or realized shape
does not change the four selected dynamics components.

A Seed also need not be generated for only one boundary variant. An 11x11
binary Seed can be compatible with fixed-zero, fixed-one, or periodic Spaces,
provided its values and coordinate rank satisfy each resulting program.

## Optional plural source

Use a Seed source when initial conditions or shapes genuinely vary:

```python
def seeds(shapes, random_keys):
    for shape in shapes:
        yield centered_impulse(shape)
        for key in random_keys:
            yield random_binary(shape, key)
```

The source may generate structured and random initial values over several
shapes. Any random choice should already be resolved in each yielded Seed so
the singular value remains definite and reproducible.

No Seed-generator superclass or coupling to one Rule is required.

## What Seed does not own

Seed does not own:

- boundary behavior;
- coordinate axes or coordinate law;
- Neighborhood or Rule;
- rollout limit or execution resources;
- successor States.
