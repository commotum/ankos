# Presets

## Preset is a module convention, not a class

A preset is ordinary Python that names useful sources and combinations. The
kernel does not need a `Preset` runtime value.

Field-level sources may use plural names when they produce genuine variation:

```text
SPACES        -> SPACE
ALPHABETS     -> ALPHABET
NEIGHBORHOODS -> NEIGHBORHOOD
RULES         -> RULE
SEEDS         -> SEED
```

A program preset combines selected values into definite SimplePrograms:

```text
SPACES + ALPHABETS + NEIGHBORHOODS + RULES -> SIMPLEPROGRAMS
```

A Seed source remains separate because Seed is not part of SimpleProgram.
Higher-level workload code may combine generated SimplePrograms and Seeds into
Trajectories.

## Plain Python composition

The intended style is explicit and unsurprising. There is no requirement that
all four inputs be plural. A family with one Alphabet and one Neighborhood can
keep those values as constants:

```python
def programs(spaces, numbers=range(256)):
    for space in spaces:
        for rule in rules(numbers):
            yield SimpleProgram(
                space=space,
                alphabet=ALPHABET,
                neighborhood=NEIGHBORHOOD,
                rule=rule,
            )
```

Dependencies appear in function arguments. Compatibility filters appear next
to the loop that needs them. There is no hidden Cartesian product, dependency
injection container, factory protocol, or constraint solver.

## Field sources

Modules may provide reusable sources at any level where choices really vary:

- `spaces()` yields boundary and coordinate-law variants;
- `alphabets()` yields definite admitted value sets;
- `neighborhoods(space)` yields Neighborhoods matching the coordinate rank;
- `rules(alphabet, neighborhood)` yields exact Rule values;
- `seeds()` yields shapes and complete initial States.

These names describe capabilities, not an interface every catalog module must
implement. Do not add `alphabets()` or `neighborhoods()` functions that merely
yield one module constant.

For example, a Space source may yield fixed-zero, fixed-one, and periodic
boundary laws. It does not yield 5x5 and 11x11 variants merely to change size;
those realized shapes belong to `seeds()`.

A rules source may implement an exhaustive or totalistic enumeration. Those
are generation schemes. Every yielded Rule is already one selected stable
callable value.

## Seed presets and program presets

“Preset” can describe either kind of source module without implying one common
object:

- a program preset yields SimplePrograms from the four dynamics sources;
- a seed preset yields Seeds, possibly across shapes and initialization laws;
- a workload function pairs compatible outputs to yield Trajectories;
- rollout materializes Episodes at a chosen limit.

This is more precise than saying either that all presets contain Seeds or that
presets categorically exclude them. The actual returned value determines the
role.

## First concrete preset

`ca.catalog.automata.elementary_ca` accepts a selected compatible t+1D Space.
It exposes its binary Alphabet and ordered spatial left/self/right Neighborhood
as constants, exact Wolfram-numbered Rule values through `rule()` and `rules()`,
and genuine SimpleProgram sweeps through `programs()`.

```python
from ca import spaces
from ca.catalog.automata import elementary_ca


periodic = spaces.cartesian(
    ("t", "x"), boundary=spaces.periodic()
)
program_30 = elementary_ca.program(30, space=periodic)
study = elementary_ca.programs(
    numbers=(30, 90, 110),
    spaces=(elementary_ca.DEFAULT_SPACE, periodic),
)
```

Finite width remains in Seed rather than Space or SimpleProgram. Dense Seed
construction is generic library functionality; a catalog-level centered
single-cell pattern, if provided, is only a convenience. The current executor
runs these programs over finite fixed support under the selected boundary law.

Additional presets should still be added one at a time from concrete documented
families. Do not add placeholder preset classes or builders merely to reserve
names.
