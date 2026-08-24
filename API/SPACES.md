# Spaces

## Definition

A Space is one definite law for coordinates, extents, and boundaries.

It answers three questions:

1. Which coordinate axes does this program use?
2. How does a Seed realize and enumerate valid addresses on those axes?
3. What happens when a Neighborhood reads beyond the realized support?

A Space does not classify the world as a line, grid, tape, graph, tiling, or
field. Those may be useful descriptions in prose, but the runtime needs only
coordinates and the functions that interpret them.

## Minimal value

The initial implementation can be a small frozen record:

```python
@dataclass(frozen=True)
class Space:
    axes: tuple[str, ...]
    extent: str
    boundary: object
    coordinates: object
    normalize: object | None = None
```

- `axes` names the coordinate components and always begins with `"t"`.
- `extent` identifies the selected extent law. It is descriptive data, not a
  semantic subclass.
- `coordinates(seed)` enumerates the Seed's realized spatial addresses, without
  their time component.
- `boundary` is one selected exterior-read law.
- `normalize(address, seed)`, when required, maps an exterior spatial address
  back onto realized support.

The record is intentionally small. Specialized behavior remains in ordinary
functions.

## Coordinate forms

```text
axes                 full coordinate
-------------------  ------------------------
("t",)               (t,)
("t", "x")           (t, x)
("t", "x", "y")      (t, x, y)
("t", "x", "y", "z") (t, x, y, z)
("t", "v")           (t, v)
```

`v` may be any stable address admitted by the Seed. A relation-driven setup
can therefore use `(t, v)` plus plain relation mappings supplied by the Seed.
No `GraphSpace`, `Vertex`, or `Edge` runtime classes are required.

Irregular tilings work the same way. Addresses may be integer pairs, axial
coordinates, or opaque stable labels. Neighborhood decides which addresses
are adjacent; Space only states how those addresses exist and how boundary
reads resolve.

## Explicit time

Time is part of every address, not metadata outside the State. A State contains
coordinates from exactly one time. Execution maps:

```text
{(t, ...): value} -> {(t+1, ...): value}
```

The earlier coordinates remain unchanged and available in the Episode.

## Shape and support belong to Seed

Space defines how a shape is interpreted, but does not choose its concrete
size. For the same t+1D Space, different Seeds might realize lengths 5, 11,
and 100. For `(t, v)`, different Seeds might realize different address sets and
relations.

This distinction is deliberate:

```text
Space: zero-based finite t+2D coordinates with periodic boundary
Seed:  shape=(11, 11), complete values at t=0
```

Changing the Seed's shape does not change the SimpleProgram. Changing the
boundary law does.

## Boundary laws

Boundary behavior belongs to Space because it determines how Neighborhood
addresses are interpreted.

Examples include:

- fixed exterior value;
- periodic normalization;
- no exterior boundary for an unbounded coordinate law.

A fixed exterior value must be admitted by the Alphabet. Periodic and
normalization uses the realized Seed shape. A coordinate law with no exterior
need not invent a boundary value.

Neighborhood is still responsible for selecting the candidate addresses.
Space is responsible for resolving them. Rule receives only the resulting
ordered values.

## Plural source

`SPACES` means an ordinary iterable or function yielding definite Space
values. A future source might vary boundary behavior:

```python
def spaces():
    yield Space(..., boundary=fixed(0), ...)
    yield Space(..., boundary=fixed(1), ...)
    yield Space(..., boundary="periodic", normalize=wrap)
```

It should not vary concrete dimensions such as 5 versus 11; those variants
belong to a Seed source.

No Space factory class, domain-kind hierarchy, or parameter solver is needed.
