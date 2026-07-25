# Simple Programs: The Five-Field Model

A simple program is one closed construction with five parts:

```text
SimpleProgram(
    seed,
    alphabet,
    frontier,
    neighborhood,
    rule,
)
```

The five fields describe where configurations come from, what values they may
contain, what may be changed, what may be observed, and which complete
replacement relation connects one configuration to its possible results.

This is the conceptual model. `api.md` gives the public library spelling;
`goal-6/architecture.md` gives the full internal contracts and application algebra.

## The program boundary

The five stored fields are:

| Field | Conceptual responsibility |
|---|---|
| `seed: Seed` | Denote valid initial configurations or a law over them |
| `alphabet: Alphabet` | Define the closed universe and equality of semantic values |
| `frontier: WritableRegion` | Resolve the complete writable capability envelope |
| `neighborhood: ReadableRegion` | Resolve the complete readable view |
| `rule: Rule` | Denote complete, typed, atomic alternatives over those views |

Four symbols describe relationships among those components:

| Symbol | Meaning |
|---|---|
| `C` | One immutable, invariant-bearing configuration |
| `V` | The semantic values admitted inside `C` and in replacements |
| `W` | The writable capability resolved for one application |
| `R` | The identity-preserving readable view resolved for that application |

They are type relationships, not additional program fields. In particular,
`C` is not a stored configuration-schema axis, and `W` and `R` are not cached
program state.

In prose, *Frontier* and *Neighborhood* name the two field responsibilities;
their canonical component types are `WritableRegion` and `ReadableRegion`.

Conceptually:

```text
Seed[C]                       denotes initial C values, sets, or laws
Alphabet[V]                   validates semantic values within C
WritableRegion[C, W](C)       resolves W
ReadableRegion[C, R](C)       resolves R
Rule[R, W, C](R, W)           denotes typed replacements or outcomes
```

Every component is immutable, closed, and serializable structural data.
“Closed” does not mean finite: a descriptor may denote an infinite set,
continuous field, recursive structure, probability measure, or symbolic
relation through a recognized, versioned expression tree. It does not contain
an unrestricted host-language callback, iterator, generator, solver, or hidden
source of randomness.

## Configurations and loci

The configuration `C` carries the state that the mechanics acts upon. Depending
on the construction, it may be:

- a finite or default-backed lattice;
- a word, sequence, tree, or graph;
- a product of registers, wires, stacks, tapes, or control records;
- a partial assignment with explicit unknown roles;
- a continuous field with geometry and side data; or
- an intensional symbolic object.

Configuration data owns the carrier and support, topology, geometry, defaults,
boundary behavior, invariants, and visible control state used by the
construction. Time, phase, schedule, head position, program counter, mutable
program text, or draw state belongs in `C` only when later mechanics can read
or change it.

The shared loci algebra names parts of these configurations without imposing a
single coordinate system. Loci may be coordinates, record fields, sequence
occurrences, spans, tree paths, graph vertices or ports, field regions,
differential germs, event identities, or potential fresh components.

Identity is structural:

- equal values at different occurrences remain distinct when mechanics cares;
- ordered structures retain order and bags retain multiplicity;
- graph and binder equivalence is explicit;
- fresh identities derive from the old configuration, Rule, witness,
  interface, namespace, and local key; and
- process IDs, UUIDs, traversal positions, and memory addresses never define
  semantic identity.

A locus selector by itself grants neither read nor write access. Frontier wraps
selected structure as capabilities; Neighborhood wraps selected structure as
observations.

## Seed

`Seed[C]` is a closed source of initial configurations. It may denote:

- one exact configuration;
- a constructive structural recipe;
- a partial configuration with explicit unknowns or obligations;
- a probability law with an explicit replay interface; or
- an intensional initial object.

A constructive Seed is data describing a construction, not a Python generator.
A probabilistic Seed stores the law, not a mutable random-number generator.
Realization receives an external replay key and records draw evidence.

Seed composition still produces one Seed. Products, overlays, refinements,
mixtures, and explicitly independent product laws state their combination
semantics rather than relying on tuple position or ambient convention.

## Alphabet

`Alphabet[V]` defines valid semantic values, canonical equality, and any
declared order or algebra. It may describe:

- finite colors or symbols;
- integers, rationals, modular values, algebraic values, or represented reals;
- tagged sums, products, records, words, maps, and sequences;
- addresses, instructions, gates, ports, probabilities, and control values;
- symbolic expressions, patterns, equations, and differential syntax; or
- fields, tensors, distributions, and other composite payloads.

Alphabet need not be finite or enumerable. Machine floats are valid only under
an explicit represented-number profile; they do not silently stand for exact
real numbers.

Carrier absence and structural deletion are normally not Alphabet values.
Likewise, an unknown value exists only when the Alphabet explicitly admits an
unknown or unresolved variant.

## Frontier

The `frontier` field holds a `WritableRegion[C, W]`, which resolves the
complete writable capability envelope for one application.

The envelope includes every existing component that any permitted Rule
alternative may replace, relabel, reroute, or delete, and every fresh
component, edge, child, span, field region, or result slot that an alternative
may create.

Frontier answers:

> What could this Rule be authorized to change from this configuration?

It does not answer:

> Which part fires, which destination is selected, or what actually changes?

Those decisions belong to Rule. A mobile automaton therefore places the source
and all possible destinations in `W`. The active tag in the readable state and
the Rule transition determine the selected move; unselected writable members
receive explicit preserve dispositions.

Frontier may be finite or intensional. It can describe all sites in a field,
all unknown variables, a matched graph interface plus a fresh namespace, or a
continuous solution region without first enumerating it.

## Neighborhood

The `neighborhood` field holds a `ReadableRegion[C, R]`, which resolves the
complete readable view from the same immutable configuration.

Neighborhood answers:

> What may Rule observe in order to determine its complete result?

It may expose a local stencil, indexed stencils, a word span, graph path,
matched interface, complete prefix, global aggregate, history relation,
boundary field, differential germ, or symbolic solution context.
“Neighborhood” does not imply geometric locality.

The view preserves identity, order, grouping, multiplicity, masks, defaults,
incidence, paths, and other distinctions Rule needs. If Rule needs the old
value of a writable component, Neighborhood must include that value. Frontier
grants write authority but never grants read authority.

Frontier and Neighborhood resolve independently from one immutable snapshot.
Their resolved identities and the Rule-declared join must agree, but neither
resolver consumes the other's output.

## A small selector example

A reusable selector can be understood as closed structural data containing:

```text
candidate region
closed inclusion expression
composition mode
identity/order/multiplicity contract
finite or intensional presentation
```

For an ordinary one-dimensional cellular automaton, configuration data may
describe an integer-indexed line and its boundary/default law. One relative
selector denotes offsets `{-1, 0, +1}`. Neighborhood lifts that selector into
an identity-indexed read stencil around every output site. Another selector
denotes the complete output region, and Frontier lifts it into writable
capabilities.

The same selector algebra can instead name a sequence span, graph incidence
region, record projection, fresh child namespace, or differential region.
Read and write meaning comes from the Neighborhood or Frontier wrapper, not
from special coordinate syntax.

## Rule

`Rule[R, W, C]` is one closed relation over the resolved readable view and
writable capability:

```text
(R, W) -> RuleResult[C, W]
```

Rule owns:

- applicability and clause priority;
- match, branch, and destination choice;
- schedule and simultaneous or sequential meaning within one application;
- overlap, collision, and conflict resolution;
- stochastic laws;
- stopping and progress meaning; and
- the complete atomic disposition of every writable capability.

For each derivation, existing writable capabilities are explicitly preserved,
replaced, or deleted. Fresh capabilities are explicitly absent or created.
Everything outside `W` is preserved.

```text
existing capability -> Preserve | Replace(payload) | Delete
fresh capability    -> Absent   | Create(payload)
outside W           -> Preserve
```

The payload may be a stored value or a structural object such as an edge,
ordering relation, subtree, field restriction, or result object. Every payload
must conform to the configuration and Alphabet contracts.

A sparse storage form is acceptable only when its declared defaults recover
this total meaning. Generic application never chooses a winner among
conflicting proposals, fills an unspecified gap, cascades a deletion, selects
a stochastic branch, or repairs an interface. Rule has already resolved those
semantics.

Rule denotation may produce zero, one, or many derivations with finite or
intensional presentation. It can additionally carry a probability law over
the complete outcome space. The law is not a concrete draw.

Typed outcomes distinguish:

- an `Advanced` derivation from an identity `Quiescent` derivation;
- `Continue` from `Stop`;
- terminal completion from undefinedness;
- a declared construction failure from invalid input; and
- certified semantic divergence from resource exhaustion.

An exact empty successor relation therefore carries a typed reason. A
quiescent identity remains one derivation and one successor. An intensional
relation may honestly have undetermined cardinality without fabricating either
a solution or a terminal outcome.

Each derivation has a structural witness before equal successors are grouped.
If two different matches produce the same successor, their witnesses,
provenance, continuation states, and probability mass remain available in the
successor's complete derivation fiber.

## Generic atomic application

One family-blind operation applies every simple program:

```text
1. Validate the five descriptors and their compatibility.
2. Freeze and validate one input configuration.
3. Resolve W and R from that same snapshot.
4. Validate their identities and Rule-declared join.
5. Ask Rule for its complete closed outcome space.
6. Validate every atom, witness, disposition, payload, law, and cardinality.
7. Bind every fresh identity structurally.
8. Reconstruct every alternative independently from the old snapshot.
9. Validate every successor.
10. Group semantically equal successors only after retaining derivations.
```

All alternatives observe the same old configuration. No alternative observes
another alternative's output, and the input is never mutated.

The reconstruction operation is a closed structural lens derived from the
configuration and Frontier contracts. It applies an already complete
disposition simultaneously; it is not a configurable update policy.

If any generic phase rejects the complete result, no authoritative successor
space is committed. Application may dispatch on sealed descriptor and result
variants, but it never switches on catalog name, semantic family, Book source,
carrier label, or constructor name.

For stochastic results, application preserves the normalized law over all
tagged outcomes. It derives unrenormalized successor and no-successor
submeasures. A later realization request supplies a replay key, selects an
atom, and records enough evidence to reproduce that selection.

## Application, realization, and trajectories

Application denotes one complete transition relation. It does not choose a
time horizon, solver, sample, numerical method, branch, projection, or
rendering.

A trajectory is a path through repeated applications. Rollout starts from the
Seed result space unless the caller supplies an explicit valid initial
configuration, then reapplies the same family-blind operation to continuing
successor-and-lineage fibers. Deterministic programs produce a path, multiway
programs produce a branching or intensional path space, and stochastic
programs additionally carry measures or replayable samples.

A rollout bound truncates traversal; it does not prove terminality. Likewise,
an external solver or numerical budget may return partial evidence or resource
exhaustion without changing the underlying Rule relation.

Not every useful construction needs repeated application. A constraint
completion, transform, hash, basis projection, or maximal-flow construction
may produce its complete result in one application and stop. It remains an
ordinary simple program.

## Composition and catalog construction

The plural `alphabets`, `seeds`, `frontiers`, `neighborhoods`, and `rules`
modules are constructor algebras for singular field values; `loci` supplies
their shared structural vocabulary. Each progresses from primitives through
compounds and general constructors to useful component presets.

For example, several value schemas compose into one Alphabet, several
writable selectors compose into one Frontier, and several clauses compose
into one Rule with explicit ordering or parallel semantics. `SimpleProgram`
does not store a tuple of unrelated frontiers or rules merely because its
construction used several pieces.

Whole-program names live in the catalog:

| Catalog module | Dominant construction mechanic |
|---|---|
| `automata` | Persistent carriers updated in place or in parallel |
| `substitua` | Matched structure replaced, grown, deleted, or branched |
| `machina` | Visible heads, control, instructions, stacks, or schedules |
| `media` | Information transformed between distinct representations |
| `criteria` | Constraints, witnesses, admissibility, or weighted alternatives |
| `dynamica` | Continuous differential, field, event, or flow laws |

A catalog constructor composes ordinary component values and returns an
ordinary `SimpleProgram`. An alias delegates to that construction. Catalog
entries may carry discovery and provenance metadata, but neither names nor
metadata control generic application.

## Representative constructions

| Construction | Five-field interpretation |
|---|---|
| Ordinary cellular automaton | Seed supplies a lattice and its support/default behavior; Alphabet supplies finite cell values; Frontier covers one output pass; Neighborhood supplies indexed old-snapshot stencils; Rule lifts a local table into one simultaneous replacement. |
| Mobile automaton or Turing machine | Seed establishes a default-backed tape and one tagged head; Alphabet includes symbols and control; Frontier contains the source and all possible destinations; Neighborhood exposes their old contents; Rule returns one coupled move. |
| Structural rewrite | Seed supplies a word, tree, or graph; Alphabet supplies labels and ports; Frontier covers matches, interfaces, deletions, and fresh structure; Neighborhood supplies occurrence and interface context; Rule returns witnessed replacements with explicit overlap and reconnection semantics. |
| Constraint completion | Seed supplies a partial assignment with explicit unknowns; Frontier covers all unknowns; Neighborhood exposes every constraint dependency; Rule denotes all satisfying total completions, finitely or intensionally. |
| PDE relation | Seed supplies a partial field, geometry, equations, and side data; Alphabet records exactness; Frontier denotes the unknown field region; Neighborhood exposes differential and global conditions; Rule denotes the complete solution relation. |
| Continuous flow | Seed supplies state, time, geometry, parameters, and events; Frontier covers a maximal-flow result and any semantically selected reset slots; Neighborhood exposes vector-field dependencies; Rule denotes maximal flows or event-selected segments. |
| One-shot transform | Seed supplies tagged input, workspace, and result slots; Frontier authorizes the result; Neighborhood exposes the complete input; Rule writes the output and stops. |

Lattice extent, boundary law, synchronous mapping, and visible control are
configuration or Rule data, not extra fields. The mobile source's active tag
determines applicability inside Rule; unselected destinations are preserved.
Structural birth, deletion, and rerouting are ordinary replacements inside
`W`.

No solution is a certified terminal constraint result, while a numerical PDE
mesh is a qualified realization rather than the exact relation. A flow without
a semantic endpoint selector returns its maximal flow object; an external
horizon may query it but cannot silently choose an endpoint. Hashing, lookup,
basis projection, parsing, and other one-shot relations use the same generic
application law without inventing a trajectory step.

## Stable boundaries

Serialization is cross-cutting infrastructure. Canonical program encoding
contains exactly the expanded five fields and preserves exact values, closed
descriptor versions, structural identities, result witnesses, probability
laws, and replay evidence without dispatching on an alias.

Run horizon, realization profile, solver strategy, replay key, resource
limits, tracing, observation, rendering, export, datasets, and batching remain
outside the stored program. They may consume or present its results, but they
do not become hidden semantic components.

The central invariant is therefore simple:

> Seed supplies configurations, Alphabet validates their values, Frontier
> grants write capability, Neighborhood grants read capability, Rule denotes
> complete atomic outcomes, and one family-blind application law connects
> them.
