# Spaces

## Definition

A Space is one definite law for coordinates and boundaries.

It answers three questions:

1. Which coordinate axes does this program use?
2. How are the spatial addresses realized by a Seed enumerated?
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
    boundary: object
    coordinates: object
```

- `axes` names the coordinate components and always begins with `"t"`.
- `coordinates(seed)` enumerates the Seed's realized spatial addresses, without
  their time component.
- `boundary` is one selected exterior-read law, including any resolution it
  requires.

There is no descriptive `extent` string: concrete extent is already supplied
by Seed and behavior is supplied by `coordinates`. There is also no separate
`normalize` field that must be kept consistent with `boundary`. A periodic
boundary is itself responsible for wrapping an exterior address.

The record is intentionally small. Generic constructors cover common cases:

```python
finite_1d = spaces.cartesian(
    axes=("t", "x"),
    boundary=spaces.fixed(0),
)

periodic_2d = spaces.cartesian(
    axes=("t", "x", "y"),
    boundary=spaces.periodic(),
)
```

These are ordinary functions returning definite Space values, not semantic
`LineSpace` or `GridSpace` classes.

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
- no exterior resolution (`None`), requiring every selected address to remain
  inside realized support.

A fixed exterior value must be admitted by the Alphabet. Periodic resolution
uses the realized Seed shape. With `None`, an exterior read is a direct error
rather than an invented value.

Neighborhood is still responsible for selecting the candidate addresses.
Space is responsible for resolving them. Rule receives only the resulting
ordered values.

## Optional plural source

Use a plural Space source only when the module genuinely varies Space. For
example, a study may sweep boundary behavior:

```python
def spaces():
    yield spaces.cartesian(("t", "x"), boundary=spaces.fixed(0))
    yield spaces.cartesian(("t", "x"), boundary=spaces.fixed(1))
    yield spaces.cartesian(("t", "x"), boundary=spaces.periodic())
```

It should not vary concrete dimensions such as 5 versus 11; those variants
belong to a Seed source.

If a family uses one Space, expose that Space directly. A singleton `spaces()`
generator adds no information. No Space factory class, domain-kind hierarchy,
or parameter solver is needed.
