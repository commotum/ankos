# Future presets

## Preset is a module convention, not a class

A preset is ordinary Python that names useful sources and combinations. The
kernel does not need a `Preset` runtime value.

Field-level sources use plural names:

```text
SPACES        -> SPACE
ALPHABETS     -> ALPHABET
NEIGHBORHOODS -> NEIGHBORHOOD
RULES         -> RULE
SEEDS         -> SEED
```

A program preset combines the first four into definite SimplePrograms:

```text
SPACES + ALPHABETS + NEIGHBORHOODS + RULES -> SIMPLEPROGRAMS
```

A Seed source remains separate because Seed is not part of SimpleProgram.
Higher-level workload code may combine generated SimplePrograms and Seeds into
Trajectories.

## Plain Python composition

The intended style is explicit and unsurprising:

```python
def programs():
    for space in spaces():
        for alphabet in alphabets():
            for neighborhood in neighborhoods(space):
                for rule in rules(alphabet, neighborhood):
                    yield SimpleProgram(
                        space=space,
                        alphabet=alphabet,
                        neighborhood=neighborhood,
                        rule=rule,
                    )
```

Dependencies appear in function arguments. Compatibility filters appear next
to the loop that needs them. There is no hidden Cartesian product, dependency
injection container, factory protocol, or constraint solver.

## Field sources

Future modules may provide reusable sources at any level:

- `spaces()` yields boundary and coordinate-law variants;
- `alphabets()` yields definite admitted value sets;
- `neighborhoods(space)` yields Neighborhoods matching the coordinate rank;
- `rules(alphabet, neighborhood)` yields exact callables;
- `seeds()` yields shapes and complete initial States.

For example, a Space source may yield fixed-zero, fixed-one, and periodic
boundary laws. It does not yield 5x5 and 11x11 variants merely to change size;
those realized shapes belong to `seeds()`.

A rules source may implement an exhaustive or totalistic enumeration. Those
are generation schemes. Every yielded Rule is already one selected callable.

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

## Goal 9 stopping point

Goal 9 makes the kernel ready for this code but does not implement canonical
preset modules. The first real presets should be added one at a time, starting
from a concrete documented family and tested through actual successor values.

Do not add placeholder preset classes or builders merely to reserve names.
