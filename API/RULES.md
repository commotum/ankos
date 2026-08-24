# Rules

## Definition

A Rule is one exact stable callable value selected for a SimpleProgram. It
receives the ordered values read by Neighborhood for one source coordinate and
returns the one Alphabet value placed at the corresponding coordinate in the
successor State.

```python
def transition(observed):
    ...
    return successor_value
```

`observed` follows Neighborhood order. Coordinate and time arguments are not
part of the default contract because most local laws do not need them.

`ca.core.rules.Rule` is a tiny frozen callable value that pairs this function
with stable scientific identity such as a name and optional index. It is not a
Rule class hierarchy. Its purpose is to make equivalent selected Rules compare,
serialize, cache, and cross process boundaries without relying on a freshly
created closure or metadata attached with `setattr`.

```python
table_30 = tuple((30 >> pattern) & 1 for pattern in range(8))
exact_rule = Rule(
    name="eca_rule_30",
    function=apply_eca,
    parameters=(table_30,),
    index=30,
)
```

Calling `exact_rule(observed)` invokes `apply_eca(observed, table_30)`. The
selected Rule therefore carries its exact lookup table as well as its familiar
Wolfram index.

## Exact Rule versus rule source

An exhaustive table scheme, a totalistic scheme, and a threshold scheme are
ways to generate Rules. They are not themselves the exact Rule stored in a
SimpleProgram unless every parameter and table entry has already been
selected.

For an elementary cellular automaton:

- Alphabet supplies two admitted values;
- Neighborhood supplies the ordered left/self/right reads;
- a rules source enumerates or selects one of the 256 exact tables;
- one yielded stable Rule value becomes `SimpleProgram.rule`.

Changing from one table to another produces a different selected
SimpleProgram value within the same broader family or preset source.

## Complete immutable successor States

Rule returns a value, not a mutation instruction. The executor calls it for
each realized spatial coordinate and constructs a complete slice at `t+1`.

If the logical value is unchanged, Rule returns that same value. It is still
placed at a different spacetime coordinate:

```text
(t, x)   -> old value remains in the old State
(t+1, x) -> equal value appears in the new State
```

There is no `KEEP`, replace, delete, or CRUD result in the public model.

## Activity in state

For a family with a moving active site, Alphabet values can distinguish active
and inactive cases. Neighborhood exposes the local values required to move
that tag, and Rule emits the next complete set of values. This preserves the
family's dynamics without a universal Frontier component.

This rule is about representation, not a claim that every future system must
be forced into a local table. When a concrete family needs a different exact
call signature, that requirement should first be demonstrated by the family,
then added as a small extension.

## Dependencies

A Rule is meaningful relative to:

- Alphabet, which defines valid inputs and outputs;
- Neighborhood, which determines the arity and ordering of observations;
- Space, indirectly, because Neighborhood addresses are resolved there.

A rules source may therefore accept the selected dependencies explicitly:

```python
def rules(alphabet, neighborhood):
    for index in requested_indices:
        yield compile_table(index, alphabet, neighborhood)
```

Each yielded Rule is definite. Compatibility can be checked while
producing it or while constructing a SimpleProgram.

## Optional plural source

`RULES` is only an ordinary iterable or function that yields exact Rule values,
and is useful when choices really vary. A family with one law can expose one
Rule constant. It is not a parameter-solving framework, subclass tree, or
delayed Rule family stored inside `SimpleProgram`.
