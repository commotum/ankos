# Alphabets

## Definition

An Alphabet is the exact set of values that may appear at one realized
coordinate in a SimpleProgram.

Use an ordinary Python value:

```python
binary = (0, 1)
```

For finite enumerable Alphabets, prefer an ordered tuple. Membership still
works normally, and the order gives exhaustive schemes a canonical basis for
enumerating inputs and Rule tables. An unordered `frozenset` silently discards
that scientifically meaningful order.

When the admitted set is naturally described rather than enumerated, use a
membership function:

```python
def unit_interval(value):
    return isinstance(value, float) and 0.0 <= value <= 1.0
```

The runtime needs one operation: determine whether a Seed value, fixed
boundary value, or Rule output belongs to the Alphabet.

## One selected Alphabet

A SimpleProgram contains one definite Alphabet. Parameters such as the number
of cell symbols or head states have already been selected by then.

For example, a binary cell and binary active-state encoding may use six plain
values:

```text
Inactive(0)
Inactive(1)
Active(0, 0)
Active(0, 1)
Active(1, 0)
Active(1, 1)
```

These can be strings, tuples, integers, or another small immutable encoding.
They do not require an object hierarchy.

This encoding is also how a dynamic logical activity set can remain part of
the ordinary state. The Rule reads whether a value is active and emits the
appropriate successor values. No separate Frontier value is necessary.

## What Alphabet owns

Alphabet owns per-coordinate value membership. It does not own:

- coordinate axes or boundary behavior;
- concrete shape or support;
- address relations;
- initial values;
- the mapping from observed values to successor values.

Constraints involving several coordinates—such as exactly one active head—are
properties of compatible Seeds and Rule behavior, not membership of one value.
They can be checked where a family actually needs them, without expanding the
base API.

## Optional plural source

Use an Alphabet source when the Alphabet genuinely varies:

```python
def machine_alphabets(head_counts, cell_counts):
    for head_count in head_counts:
        for cell_count in cell_counts:
            yield machine_values(head_count, cell_count)
```

Each yielded value is already concrete. The source may generate binary,
ternary, and larger alternatives; a `SimpleProgram` receives exactly one.

When a family has one Alphabet, expose it directly as a constant. A function
that yields that same constant once is ceremony, not a useful generator.

No `Alphabet` superclass, rule-family wrapper, or general constraint language
is required.
