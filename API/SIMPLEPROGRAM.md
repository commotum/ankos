# SimpleProgram

## Definition

A `SimpleProgram` is one definite reusable composition of four values:

```python
@dataclass(frozen=True)
class SimpleProgram:
    space: Space
    alphabet: object
    neighborhood: object
    rule: object
```

Equivalently:

```text
SPACE + ALPHABET + NEIGHBORHOOD + RULE -> SIMPLEPROGRAM
```

Each field is already selected:

- Space has one coordinate, extent, and boundary law;
- Alphabet has one exact membership definition;
- Neighborhood has one exact ordered address selection;
- Rule is one exact callable, not an unresolved scheme or index range.

## Seed is separate

SimpleProgram does not contain initial values or a concrete shape. Those belong
to Seed. This makes the program reusable across compatible initial conditions
and realized extents.

```text
same SimpleProgram + length-5 Seed  -> one Trajectory
same SimpleProgram + length-100 Seed -> another Trajectory
```

The Space still knows how to interpret each shape and resolve its boundary.

## Definite does not mean one shape

A finite coordinate law can be completely selected even though a Seed has not
yet supplied its dimensions. “Definite” means there are no unresolved choices
inside the four fields. It does not mean the reusable program owns episode
initialization.

For example, a definite t+1D cellular rule can specify:

- axes `(t, x)`;
- periodic boundary normalization;
- binary Alphabet;
- offsets `((0,-1), (0,0), (0,1))`;
- one exact Rule table.

It remains valid for multiple finite lengths.

## Construction and compatibility

Construction should be direct. The value does not need a builder, registry,
semantic family class, or proof object.

Checks that involve only the four fields can happen immediately. For example,
a fixed boundary value must belong to Alphabet, and Neighborhood offsets must
have the Space's coordinate rank. Shape, complete support, and initial-value
membership are checked when a Seed is paired in a Trajectory.

## Identity

Catalog names and family labels may describe how SimplePrograms were
generated, but they do not add runtime semantics. Two SimpleProgram values are
distinguished by their selected four components, including the exact Rule.

## From plural sources

Source code combines definite values with explicit loops:

```python
for space in spaces():
    for alphabet in alphabets():
        for neighborhood in neighborhoods(space):
            for rule in rules(alphabet, neighborhood):
                yield SimpleProgram(space, alphabet, neighborhood, rule)
```

Dependencies and compatibility filters may be written directly in those
loops. `ca.catalog.automata.elementary_ca` is the first concrete example.
