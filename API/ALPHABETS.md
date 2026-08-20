# `ALPHABETS -> ALPHABET`

This document specifies the Alphabet source and the definite Alphabet value in
the target ANKoS API.

```text
ALPHABETS -> one or more ALPHABET values

SPACE + ALPHABET + NEIGHBORHOOD + RULE
    -> SIMPLEPROGRAM
```

The uppercase plural and singular names describe semantic roles. They do not
require separate class hierarchies. An `ALPHABETS` source may be a tuple, an
iterator, a generator function, or a small declarative recipe.

## The distinction

| Name | Meaning |
|---|---|
| `ALPHABETS` | A source that yields at least one definite Alphabet |
| `ALPHABET` | One definite vocabulary or value schema admitted by a SimpleProgram |

A definite Alphabet need not be a small, eagerly enumerated set. These are all
possible definite Alphabets:

- the finite set `{0, 1}`;
- an exact integer or real interval;
- a product such as `Color x Orientation`;
- a tagged union such as `Inactive(Symbol) | Active(HeadState, Symbol)`; or
- another exact, plain description of the values a program admits.

"Definite" means that no choice such as the number of symbols or head states
remains unresolved in the `SimpleProgram`. It does not mean that every value
must be stored in a Python collection.

## What Alphabet owns

One `ALPHABET` owns the semantic vocabulary available at each realized Space
coordinate. It defines:

- which values are admitted;
- the components of product values;
- the alternatives and payloads of tagged values; and
- state roles that are carried by values, such as `Active` and `Inactive`.

Dynamic activity is ordinary state. A mobile head, cursor, walker, or other
active locus can therefore be represented directly in Alphabet values instead
of requiring a separate `Frontier` field.

Alphabet describes possible values, not which values actually occur. A Seed
supplies the exact values at `t=0`, and Rule constructs later values.

## What Alphabet does not own

Alphabet does not define:

- coordinates, rank, topology, finite extent, or shape;
- boundary or out-of-range access behavior;
- the initial state;
- which coordinates a Neighborhood observes;
- how observations map to the next state;
- a write region or Frontier; or
- model tokens, serialization layouts, or batch representations.

Alphabet also need not become a global invariant or defensive-validation
framework. For example, an Alphabet can admit `Active(...)` values without
itself enforcing that exactly one coordinate is active. A compatible Seed can
establish that condition, and the selected Rule can preserve it. Such
family-specific behavior should remain in the family definition rather than
forcing every Alphabet through a general constraint system.

## Generator behavior

An `ALPHABETS` source:

1. yields at least one definite `ALPHABET`;
2. may enumerate a finite collection or generate values lazily;
3. may expose ordinary arguments that determine which Alphabets it yields;
4. leaves no generator choice unresolved in an emitted Alphabet; and
5. remains reusable across Presets and compatible Spaces, Neighborhoods,
   Rules, and Seeds.

For example, a machine-Alphabet source might accept sets of controller-state
counts and tape-symbol counts:

```text
head counts   = {2, 3}
symbol counts = {2}
```

and yield two definite Alphabets:

```text
machine_alphabet(head_states=2, symbols=2)
machine_alphabet(head_states=3, symbols=2)
```

The generator may construct these values with an ordinary Python function.
No universal `AlphabetGenerator` base class is required.

## Compatibility and dependencies

Alphabet generation is independent in the architectural sense: an Alphabet
is not owned by one Space, Rule, or Seed. Compatibility is checked when values
are combined.

The important compatibility relationships are:

- Every value present in a Seed must be admitted by the selected Alphabet.
- Values supplied by a fixed Space boundary must be admitted by the selected
  Alphabet.
- A Rule must understand the Alphabet values its Neighborhood exposes.
- Every value a Rule places in the next state must belong to the selected
  Alphabet.
- A rule scheme may use the selected Alphabet to generate its definite Rules.

One Seed may therefore be compatible with several Alphabets, and one Alphabet
may be reused across many Spaces, Neighborhoods, and Rules. Preset expansion
can omit incompatible combinations directly; it does not require a
general-purpose constraint solver.

## Identity

The semantic value vocabulary identifies an Alphabet. Changing its admitted
values, cardinality, product components, or meaningful tags produces a
different definite Alphabet and therefore a different SimpleProgram.

Incidental Python representation is not the point of identity. Two
constructors may describe equivalent vocabularies even if one uses integers
and another uses enum members internally. If ordering or numeric coding is
used to enumerate Rules, however, that ordering is part of the exact
Alphabet-to-Rule generation convention and must be stable.

## Examples

### Binary cellular Alphabet

```text
ALPHABET = {0, 1}
```

The same definite binary Alphabet can be used with multiple finite extents,
boundaries, Neighborhoods, Rules, and binary Seeds.

### Tagged Turing-machine Alphabet

Let `Gamma` be the tape-symbol set and `Q` the controller-state set. Encode
activity at a coordinate as:

\[
A = \operatorname{Inactive}(\Gamma)
    \cup
    \operatorname{Active}(Q \times \Gamma).
\]

For two controller states and two tape symbols, the definite Alphabet is:

```text
Inactive(0)
Inactive(1)
Active(0, 0)
Active(0, 1)
Active(1, 0)
Active(1, 1)
```

Its size is:

\[
|A| = |\Gamma| + |Q||\Gamma|
    = (|Q| + 1)|\Gamma|.
\]

A source can generate binary-head, ternary-head, or other definite versions.
Each emitted Alphabet fixes `Q` and `Gamma`; the SimpleProgram contains that
one selected Alphabet.

The tag says whether a coordinate is active. It does not add a semantic
Frontier, and it does not force ANKoS to introduce a special Turing-machine
state class.

## Minimal implementation principle

Start with the smallest representation that states the admitted values
clearly. Add specialized objects only when a real family needs behavior that
plain data and functions cannot express cleanly.
