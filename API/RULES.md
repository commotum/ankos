# RULES and RULE

## Definition

```text
RULES -> RULE
```

`RULES` is a source of one or more definite Rules. `RULE` is one exact,
selected transition law.

The distinction is essential:

- `RULES` may describe a range to enumerate, sample, or construct.
- `RULE` contains no remaining choice of rule table, rule number,
  coefficients, thresholds, gates, or other mechanics parameters.
- A `SimpleProgram` contains one `RULE`, never unresolved `RULES`.

A change from one generated Rule to another creates a different
`SimpleProgram`, even when both Rules came from the same scheme and Preset.

## Rule Schemes

A **rule scheme** describes how Neighborhood observations are turned into
outputs and therefore how a set of definite Rules can be generated. Examples
include:

```text
EXHAUSTIVE
TOTALISTIC
OUTER_TOTALISTIC
THRESHOLD
GATED
ALGEBRAIC
```

A scheme belongs to rule generation. It is not a substitute for a definite
Rule.

For example, `EXHAUSTIVE` says to consider every mapping from the possible
Neighborhood observations to the possible outputs. It does not select one of
those mappings. `RULES` performs that enumeration and yields each selected
mapping as a separate `RULE`.

Likewise, a totalistic scheme becomes definite only after its aggregation
law, output mapping, and any parameters have been selected. A formula can be
a definite Rule; it does not have to be expanded into a table, provided the
formula has no unresolved choices.

## Generation Context

Rule generation may depend on the already resolved:

```text
SPACE
ALPHABET
NEIGHBORHOOD
```

Those values determine the inputs a Rule can observe, the values it may
produce, and the coordinate relations in which it operates. A useful
conceptual interface is:

```python
def generate_rules(*, space, alphabet, neighborhood):
    yield definite_rule
```

This is a semantic contract, not a required class or function signature. A
plain tuple, iterator, generator function, or small data object is sufficient.

A Rule source need not use every item in the context. For example, elementary
cellular-automaton rule tables depend on the binary Alphabet and three-cell
Neighborhood but can be reused across several compatible boundary behaviors.

## Contract for RULES

A configured `RULES` source:

1. Generates definite `RULE` values.
2. Generates at least one Rule for every context it claims to support.
3. Resolves every scheme parameter and selection before yielding a Rule.
4. Yields only Rules compatible with the resolved Space, Alphabet, and
   Neighborhood.
5. Has a stable, reproducible order when it represents an enumeration.
6. Keeps provenance sufficient to identify how a Rule was selected when that
   information is useful.

Stable enumeration order is useful for reproduction, but a Rule's meaning
must not depend solely on its position in that order.

## Contract for RULE

One `RULE` defines one exact transition law. For an ordinary discrete local
system, it determines the value at every coordinate in the complete new time
slice from the resolved Neighborhood observation at that coordinate:

\[
X_{t+1}(c) = r\!\left(N(X_t,c)\right).
\]

The resulting values live at new coordinates such as `(t+1, c)`. Nothing at
`(t, c)` is changed. If a logical value remains the same, the Rule still
constructs that value at the new time coordinate:

\[
X_{t+1}(c)=X_t(c).
\]

For a family whose support changes, the Rule defines the complete successor
support and its values. Earlier time slices remain intact.

This describes the ordinary discrete case. A definite Rule in another family
may instead be an exact relation, stochastic law, continuous law, or
event-driven law. How rollout realizes those laws is deliberately deferred.

A definite Rule must therefore settle:

- the exact observation-to-output mapping or other exact transition law;
- all selected constants, coefficients, table entries, gates, and thresholds;
- any state-dependent activity expressed through Alphabet values; and
- any family-specific choice that changes the transition law.

The Rule operates with Space and Neighborhood semantics already established.
It does not redefine coordinate rank, concrete initial extent, boundary
behavior, Alphabet membership, or Neighborhood structure.

## No Frontier and No CRUD Actions

`FRONTIER` is not a semantic component of this API.

When activity moves or changes, activity is encoded in the state vocabulary.
For example, an Alphabet can distinguish:

```text
Inactive(symbol)
Active(controller_state, symbol)
```

The Rule defines complete successor state semantics using those values. It
does not issue `KEEP`, `CREATE`, `UPDATE`, `REPLACE`, or `DELETE` commands
against an existing state.

An implementation may derive active coordinates to avoid unnecessary work,
but that is an execution optimization and not part of Rule or SimpleProgram
identity.

## Compatibility

A generated Rule is compatible with its context when:

- it accepts exactly the observations described by the Neighborhood;
- all values it can produce are admitted by the Alphabet;
- its use of coordinates and support is admitted by the Space; and
- any boundary values visible through the Neighborhood are meaningful to the
  Rule and Alphabet.

Compatibility is a direct property of the selected values. It does not
require a general constraint language or solver.

Concrete initial shape is not a Rule-generation parameter. Shape belongs to
the Seed and is introduced when a Seed is paired with a SimpleProgram to form
a Trajectory. A Rule may require a broad extent condition such as “at least
three cells,” but it is not specialized separately to every compatible Seed
length.

## Example: Elementary Cellular Automata

Take:

```text
ALPHABET     = {0, 1}
NEIGHBORHOOD = ordered offsets (-1, 0, +1)
SCHEME       = EXHAUSTIVE
```

There are `2^3 = 8` possible Neighborhood observations:

```text
111 110 101 100 011 010 001 000
```

Each observation can map to either `0` or `1`, so `RULES` generates:

\[
2^8 = 256
\]

definite Rules. Rule 30 is one yielded Rule:

```text
input:  111 110 101 100 011 010 001 000
output:  0   0   0   1   1   1   1   0
```

Rule 90 is another yielded Rule. They are separate definite Rules and produce
separate SimplePrograms.

The same Rule can be combined with compatible Spaces whose boundaries are,
for example:

```text
fixed(0)
fixed(1)
periodic
```

Those are three definite Spaces and therefore three different
SimplePrograms. The Rule itself need not be regenerated merely because the
boundary differs, unless its generation actually depends on that boundary.
The concrete line length still comes later from the Seed.

## Identity and Provenance

A Rule should expose enough information to distinguish its exact transition
law. Depending on the scheme, this may be a complete table, a normalized
formula with resolved parameters, or another exact representation.

Optional provenance can record:

- the source or Preset that generated it;
- the rule scheme;
- a conventional rule number or name; and
- the selections used to resolve it.

Provenance describes where the Rule came from. It does not replace the Rule's
definite semantics. In particular, a bare rule number is meaningful only with
the Alphabet, Neighborhood ordering, and enumeration convention that give it
an interpretation.

## Non-goals

`RULES` and `RULE` do not define:

- Seeds or concrete initial shapes;
- Preset sampling across whole SimplePrograms;
- rollout limits or compute resources;
- Episode storage or serialization;
- downstream selection, batching, serialization, or model examples;
- a semantic Frontier or write-permission layer; or
- a universal hierarchy of Rule subclasses.

The goal is only to generate exact transition laws and place one of them in
each definite SimpleProgram.
