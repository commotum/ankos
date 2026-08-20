# `NEIGHBORHOODS -> NEIGHBORHOOD`

This document specifies the Neighborhood source and the definite Neighborhood
value in the target ANKoS API.

```text
NEIGHBORHOODS -> one or more NEIGHBORHOOD values

SPACE + ALPHABET + NEIGHBORHOOD + RULE
    -> SIMPLEPROGRAM
```

The uppercase plural and singular names describe semantic roles, not a
required hierarchy of generator and runtime classes.

## The distinction

| Name | Meaning |
|---|---|
| `NEIGHBORHOODS` | A source that yields at least one definite Neighborhood |
| `NEIGHBORHOOD` | One exact observation or dependency relation used by a Rule |

A Neighborhood can be definite without enumerating every absolute coordinate
of every possible Seed. For example, the ordered offsets
`(-1, 0, +1)` completely specify the elementary-cellular-automaton
Neighborhood for any compatible one-dimensional extent.

## What Neighborhood owns

One `NEIGHBORHOOD` defines what prior information is presented to the Rule
when the Rule constructs a new state. Depending on the family, it may define:

- relative coordinate offsets;
- whether observed positions are ordered or unordered;
- named parts of a compound observation;
- a graph-relative adjacency query;
- an address derived from state; or
- a deliberately global or historical observation.

For the ordinary discrete local case, an output coordinate `(t + 1, x)` may
observe coordinates in the previous slice:

\[
N(t+1,x)=\bigl((t,x-1),(t,x),(t,x+1)\bigr).
\]

The Rule receives the values found through that relation. Time remains an
explicit Space coordinate; Neighborhood merely states the dependency between
the new coordinate and earlier coordinates.

The exact organization of the observation matters. An ordered tuple,
unordered collection, and named compound observation are not interchangeable
when the Rule distinguishes their parts.

## Shape-polymorphic resolution

Concrete initial shape or finite extent belongs to Seed, not Neighborhood.
Neighborhood should therefore be shape-polymorphic whenever its relation does
not inherently require a fixed size.

Suppose a Neighborhood contains the relative offsets `(-1, 0, +1)`. The same
definite Neighborhood can be combined with a five-cell Seed or an eleven-cell
Seed. When a Trajectory combines a SimpleProgram and Seed:

1. Seed supplies the realized finite extent;
2. Space supplies the coordinate and boundary/access law; and
3. Neighborhood resolves its offsets through that Space law.

At the left edge, for example:

- a periodic Space maps `x - 1` to the last realized coordinate;
- a fixed-boundary Space supplies its fixed boundary value; and
- an infinite Space treats `x - 1` as another ordinary coordinate.

Neighborhood does not own any of those choices. Nor does it infer that the
Seed's represented support is a boundary when Space says the coordinate space
is infinite or growing.

## What Neighborhood does not own

Neighborhood does not define:

- Space rank, axes, topology, extent law, or boundary behavior;
- Seed shape, initial support, or initial values;
- the admitted Alphabet values;
- the selected transition mapping;
- the next state's complete support or values;
- a set of writable or active sites; or
- mutation permissions, CRUD operations, or a semantic Frontier.

In particular, Neighborhood is not a write selector. It says what is read,
not what is updated. Dynamic activity can be carried by tagged Alphabet
values, and an executor may derive active coordinates as an optimization,
without making them part of Neighborhood or SimpleProgram identity.

Neighborhood also does not decide whether a mapping is `EXHAUSTIVE`,
`TOTALISTIC`, `OUTER_TOTALISTIC`, or another rule scheme. `RULES` owns that
choice. Neighborhood supplies the observations over which the scheme defines
or generates mappings.

## Generator behavior

A `NEIGHBORHOODS` source:

1. yields at least one definite `NEIGHBORHOOD`;
2. may be a tuple, iterator, generator function, or small recipe;
3. may generate alternatives such as several radii or offset patterns;
4. emits an exact relation with no unresolved selection; and
5. may use a selected Space when construction genuinely depends on its axes
   or relational structure.

For example:

```text
radii = {1, 2}
```

could yield:

```text
ordered_offsets(-1, 0, +1)
ordered_offsets(-2, -1, 0, +1, +2)
```

Both are definite and remain independent of whether a later compatible Seed
has length 5, 11, or 101.

No universal `NeighborhoodGenerator` superclass is required. Presets may use
small family-specific generator functions.

## Compatibility and dependencies

The important compatibility relationships are:

- Space must support the axes, coordinate relations, or adjacency operations
  used by the Neighborhood.
- Space resolves boundary and access behavior after Seed supplies any
  concrete finite extent.
- The selected Rule must accept the Neighborhood's observation organization
  and Alphabet values.
- A rule scheme may use the selected Neighborhood and Alphabet to enumerate
  or construct definite Rules.

Neighborhood normally does not depend on one Seed. Seed becomes relevant only
when a SimpleProgram and Seed form a Trajectory and relative reads must be
resolved against the realized initial extent or support.

Preset expansion should directly generate or retain coherent combinations.
It need not implement a general capability or constraint framework.

## Identity

A Neighborhood is identified by its exact observation relation and the
meaningful organization of its result. Changing the observed offsets,
adjacency relation, temporal dependency, ordering, or named components creates
a different definite Neighborhood and therefore a different SimpleProgram.

Changing only the concrete Seed extent does not change a shape-polymorphic
Neighborhood. Likewise, changing a Space from periodic to fixed boundary does
not rewrite the Neighborhood relation; it changes how Space resolves reads at
the realized edge and therefore produces a different SimpleProgram through
its different Space.

Equivalent implementation strategies need not become different semantic
Neighborhoods. A cached offset table and an on-demand offset function may
represent the same relation.

## Examples

### Elementary cellular automaton

For a successor coordinate `(t + 1, x)`, the exact ordered Neighborhood is:

```text
(t, x - 1)
(t, x)
(t, x + 1)
```

or, relative to `x`:

```text
(-1, 0, +1)
```

With the binary Alphabet `{0, 1}`, there are eight possible ordered
observations:

```text
111 110 101 100 011 010 001 000
```

`RULES`, not Neighborhood, decides to use exhaustive binary lookup tables and
thereby generate the 256 definite elementary Rules. The same Neighborhood is
valid for every compatible Seed length and for multiple one-dimensional Space
boundary laws.

### Two-dimensional local Neighborhoods

A source may yield a definite von Neumann offset relation and a definite Moore
offset relation. These are two Neighborhoods because they expose different
coordinates. Neither fixes an `n x m` shape; a compatible Seed supplies that
extent later.

### State-addressed observation

A family may read an address carried in an Alphabet value. The Neighborhood
can define that indirection as its exact observation relation while remaining
generic about the semantic family. This is still a read dependency, not a
separate active-site or write-authority system.

## Minimal implementation principle

Represent common Neighborhoods as plain offsets or small functions. Add
special machinery only after a concrete family demonstrates that those forms
are insufficient.
