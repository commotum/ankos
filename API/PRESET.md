# PRESET

## Definition

```text
SPACES + ALPHABETS + NEIGHBORHOODS + RULES -> PRESET

PRESET -> SIMPLEPROGRAMS
```

A `PRESET` combines four plural sources and generates one or more definite
`SIMPLEPROGRAM` values:

```text
SPACES        -> SPACE
ALPHABETS     -> ALPHABET
NEIGHBORHOODS -> NEIGHBORHOOD
RULES         -> RULE

SPACE + ALPHABET + NEIGHBORHOOD + RULE
    -> SIMPLEPROGRAM
```

A Preset is the recipe for a coherent program family. It is not itself a
SimpleProgram and is not executable dynamics. Every SimpleProgram it yields
contains one definite selection for each of the four fields.

## What “Definite” Means

Nothing inside a generated SimpleProgram remains to be selected:

- `SPACE` is one exact coordinate-space law, rank, support law, and boundary
  behavior.
- `ALPHABET` is one exact value vocabulary.
- `NEIGHBORHOOD` is one exact observation relation.
- `RULE` is one exact selected transition law.

Concrete initial extent or shape is intentionally absent. A finite Space can
state that its realized extent is supplied by the Seed while still defining
the exact rank, coordinate relations, extent law, and boundary behavior.
That is shape-polymorphism, not an unresolved mechanics selection.

## The Four Sources

### SPACES

`SPACES` generates definite coordinate-space laws. It may vary:

- time and spatial coordinate structure;
- rank or relational topology;
- finite, infinite, or growing extent law;
- support behavior; and
- boundary/access behavior.

It does **not** enumerate concrete Seed dimensions. A `5x5` and an `11x11`
initial state can use the same two-dimensional finite Space when both supply
valid realized extents.

### ALPHABETS

`ALPHABETS` generates definite value vocabularies. It may vary symbol counts,
numeric ranges, product components, or tagged states such as active and
inactive values.

### NEIGHBORHOODS

`NEIGHBORHOODS` generates definite observation relations. A Neighborhood
source may use the selected Space to construct only coordinate-relative
observations that make sense there.

### RULES

`RULES` generates definite selected transition laws. Rule generation may use
the resolved Space, Alphabet, and Neighborhood. Schemes such as `EXHAUSTIVE`
and `TOTALISTIC` guide generation but never remain unresolved inside a
SimpleProgram.

See [RULES.md](RULES.md) for the Rule contract.

## Expansion

Preset expansion is compatibility-aware. It is not necessarily the blind
Cartesian product of every candidate from every source.

Conceptually:

```python
for space in spaces():
    for alphabet in alphabets():
        for neighborhood in neighborhoods(space=space, alphabet=alphabet):
            for rule in rules(
                space=space,
                alphabet=alphabet,
                neighborhood=neighborhood,
            ):
                if compatible(space, alphabet, neighborhood, rule):
                    yield SimpleProgram(
                        space=space,
                        alphabet=alphabet,
                        neighborhood=neighborhood,
                        rule=rule,
                    )
```

This pseudocode explains dependency order; it does not require these exact
functions. Sources can be tuples, iterators, generator functions, or small
declarative values.

Direct construction is preferable to a general constraint solver. A Preset
can simply enumerate the combinations appropriate to its family and omit
combinations it knows are incoherent.

## Compatibility

A Preset yields a combination only when:

- the Neighborhood is meaningful in the Space;
- the Neighborhood observations use values described by the Alphabet;
- the Rule consumes those observations and produces admitted Alphabet values;
- the Rule's support behavior is permitted by the Space; and
- boundary values and boundary observations agree with the Alphabet and Rule.

Compatibility belongs to the relationships among the four definite values.
It does not add a fifth mechanics field to `SimpleProgram`.

A configured Preset must yield at least one SimpleProgram. If its sources have
no compatible combination, it is not a useful valid Preset and should report
that plainly rather than silently representing an empty family.

## Example: Boundary Variants and ECA Rules

Consider an elementary-cellular-automaton Preset:

```text
SPACES =
    finite t+1D, extent supplied by Seed, fixed(0)
    finite t+1D, extent supplied by Seed, fixed(1)
    finite t+1D, extent supplied by Seed, periodic

ALPHABETS =
    {0, 1}

NEIGHBORHOODS =
    ordered offsets (-1, 0, +1)

RULES =
    all 256 definite exhaustive binary lookup tables
```

All combinations are compatible, so the Preset yields:

\[
3 \times 1 \times 1 \times 256 = 768
\]

definite SimplePrograms.

The concrete lengths are not Space variants. Independent Seeds might later
supply a length-5 initial state and a length-11 initial state. Either Seed can
pair with every compatible program above, producing different Trajectories
without changing the Preset or any SimpleProgram.

For one selected rule, the Preset yields these three programs:

```text
SimpleProgram(finite t+1D fixed(0), binary, radius-1, Rule 30)
SimpleProgram(finite t+1D fixed(1), binary, radius-1, Rule 30)
SimpleProgram(finite t+1D periodic, binary, radius-1, Rule 30)
```

A `5`-cell Seed or `11`-cell Seed is paired only afterward.

## Dependency Is Not Ownership

Generation dependencies do not move fields into one another.

- A Neighborhood source may inspect Space, but Neighborhood remains a
  separate SimpleProgram field.
- A Rule source may inspect Space, Alphabet, and Neighborhood, but Rule
  remains a separate field.
- A fixed boundary value may need to belong to Alphabet, but boundary behavior
  remains part of Space.

The dependency order exists so generators can make coherent selections. It
does not require a class hierarchy or a special semantic category for every
family.

## Ordering and Cardinality

A Preset may be small, large, or lazily generated. It need not materialize all
SimplePrograms at once.

When expansion is enumerable, it should have a stable order so that runs can
be reproduced. That order is an enumeration convenience, not semantic
identity. The meaning of a SimpleProgram comes from its definite Space,
Alphabet, Neighborhood, and Rule, not from “item 37” in a Preset.

If two source paths produce the same four definite values, they denote the
same dynamics even if their provenance differs. An implementation may
deduplicate them, but Preset semantics do not require an elaborate canonical
hashing system.

## Identity and Provenance

A Preset should have a human-readable name or stable identifier. Generated
SimplePrograms may retain lightweight provenance recording:

- the Preset that generated them;
- the selected source entries; and
- conventional family or rule labels.

Preset identity and provenance help reproduce an enumeration. They do not add
fields to the SimpleProgram and do not override the meaning of its four
definite values.

## Seeds Are Separate

Neither `SEEDS` nor `SEED` belongs to a Preset:

```text
PRESET -> SIMPLEPROGRAMS
SEEDS  -> SEED

SIMPLEPROGRAM + compatible SEED -> TRAJECTORY
```

Seed sources are independent. A Seed is not generated by one selected Rule,
Neighborhood, Alphabet, or boundary variant. One Seed may be compatible with
many SimplePrograms, and one SimpleProgram may accept many Seeds.

Concrete realized shape is supplied by Seed. Space supplies the coordinate
and extent law under which that shape is interpreted.

## Non-goals

A Preset does not contain or define:

- Seeds or concrete Seed shapes;
- Trajectories;
- rollout resources or limits;
- Episodes or serialization layouts;
- selection streams, manifests, train/evaluation splits, or batches;
- a semantic Frontier; or
- a universal constraint solver or type hierarchy.

Those concerns occur either before Preset construction, when configuring its
four sources, or afterward, when generated SimplePrograms are paired with
Seeds and eventually realized.

## Summary

```text
PRESET = SPACES + ALPHABETS + NEIGHBORHOODS + RULES

PRESET -> one or more compatible, definite SIMPLEPROGRAMS

SIMPLEPROGRAM = SPACE + ALPHABET + NEIGHBORHOOD + RULE
```

The Preset owns generation. The SimpleProgram owns one exact dynamics. Seed
shape, rollout, and downstream data handling remain outside both.
