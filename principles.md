# Design Principles

## 0. Intent Outranks Wording

Optimize for the simplest coherent design, not compliance with prior wording. Requirements and abstractions are hypotheses. When a real construction does not compose naturally, stop. Identify the violated assumption, re-derive the model, and present the necessary divergence before continuing.

A blocker honestly reported is preferable to a working implementation built from exceptions, duplicated paths, or concealed incompatibilities.

## 1. Discover Constructions; Do Not Assume Them

Seek the smallest shared construction mechanisms demonstrated by the catalog. Begin with the existing SimpleProgram axes and require a concrete semantic counterexample before adding a new execution algebra.

Catalog labels do not create executors. Different names, semantic roles, or state decompositions should resolve to shared constructions whenever a lossless one-step mapping preserves the complete state and transition semantics without hidden interpretation.

## 2. Share Execution Only Where Semantics Are Shared

Use one family-blind application law wherever systems genuinely share the
five-field algebra. Never create family-specific application or rollout paths,
but never conceal fundamentally different semantics behind an empty universal
interface.

For executable constructions, the common process is:

```text
writable = FRONTIER.resolve(snapshot)
readable = NEIGHBORHOOD.resolve(snapshot)
outcomes = RULE.denote(readable, writable)
result   = APPLY.validate_and_atomically_reconstruct(snapshot, outcomes)
```

Frontier and Neighborhood resolve independently from the same immutable
snapshot. Rule returns complete typed alternatives, and `apply` performs only
family-blind validation, reconstruction, commit, quotient, and measure
projection. If supporting a family requires `Any`, family switches, hidden
engines, duplicated semantics, or global-state smuggling, stop and reconsider
the algebra.

## 3. Give Each Component One Responsibility

Within the common five-field algebra:

- `SEED`: where valid initial configurations or laws over them come from.
- `ALPHABET`: which closed semantic values and equality laws are valid.
- `FRONTIER`: every existing or potential component a Rule alternative may
  change.
- `NEIGHBORHOOD`: the complete identity-preserving view Rule may observe.
- `RULE`: applicability, scheduling, conflicts, stochastic laws, stopping,
  and complete typed atomic dispositions.
- `APPLY`: generic validation, fresh binding, reconstruction, successor
  validation, quotienting, and measure projection; it is an operation, not a
  sixth stored component.

These boundaries are hypotheses too. Redraw them if a real construction demonstrates that the responsibilities are wrong.

## 4. Make Rule Results Explicit and Typed

Same-site assignment is one possible effect, not universal implicit behavior. Mutation-producing rules return explicit effects that may write, move, insert, delete, splice, rewire, or otherwise modify their state model.

Do not relabel constraints, derivatives, distributions, or observations as effects merely to force them through one interface. Their types must preserve their actual semantics.

## 5. State Contains Everything Needed to Advance

For structured state:

```text
CONFIGURATION = SUPPORT/TOPOLOGY + VISIBLE STATE DATA + INVARIANTS
```

Heads, active markers, instruction pointers, cyclic counters, and any memory required to make the process Markovian are semantic roles inside visible state, not hidden executor state. They may be represented losslessly as tagged/product values, as named factors of a configuration, or through another explicit isomorphism. A role does not require a separate runtime class.

The alphabet defines possible values. It does not by itself define where values exist, how locations relate, or what control state is active.

## 6. Keep Domain, Addresses, and Topology Separate

Domain is a descriptive property of a construction's carrier—scalar, line,
plane, graph, field, and so on—not a stored program axis. CONFIGURATION owns
the support/topology that realizes it, with discrete or continuous character
explicit. Alphabets, value sets, parameter sets, and serialization addresses
are not domains.

The program core does not privilege a serialization address. Sequence order, graph adjacency, tree structure, and higher-dimensional geometry must remain explicit in state or metadata rather than being inferred accidentally from integer proximity.

ANKoS may encode traces as `[t,x,y,z]` where that encoding preserves every distinction required by the experiment. If a construction exposes the encoding as inadequate, change the experiment schema rather than distort the program.

## 7. Match Support to the Construction

Fixed lattices remain fixed. Growing sequences and networks grow naturally. Sparse systems remain sparse when sparsity is semantic.

Padding, truncation, and capacity limits belong only at explicit finite-computation, batching, or serialization boundaries. They must not masquerade as program semantics.

## 8. Separate Semantics From Representation

A system fitting into a tensor does not mean its construction is tensor-local. Any lowering into canonical addresses must preserve every semantic distinction required by the task and remain inspectable.

For evolving systems, the strongest reuse evidence is a lossless map `e` with an explicit inverse on its valid image and a one-step commuting law:

```text
e(step_A(state)) = step_B(e(state))
```

The mapping must preserve the complete state and typed step result—including successor cardinality, schedule/terminal meaning, and derivation witnesses—require no hidden interpreter or phase clock, and use one native step on each side. Encodability establishes a representation; it does not make two differently factored rule tables identical.

Lossy projections are acceptable only when loss is the declared purpose, as in visualization or a chosen observable. They are not valid substitutes for the underlying state.

## 9. Separate Only Genuinely Independent Choices

Geometry, alphabet, frontier, neighborhood, rule reduction, determinism, update semantics, seed, and boundary behavior should compose when they are semantically independent.

Some choices are intrinsically coupled: rule tables depend on neighborhood arity, effects depend on the state model, and symmetries depend on topology. Represent genuine coupling through explicit invariants and strict validation rather than pretending every component combines freely.

## 10. Use Presets Without Hiding Behavior

The catalog should configure common systems and validate parameters strictly
while returning an ordinary `SimpleProgram`. A preset is declarative
convenience, not an alternate implementation.

Every catalog entry should remain discoverable, but multiple entries may resolve to the same construction with different parameters, restrictions, seeds, or validation rules.

## 11. Separate Incidental Algorithms From Defining Semantics

A constraint is distinct from its solver. A PDE is distinct from its discretization and integrator. A stochastic rule is distinct from its RNG implementation.

But synchronous update, first-match order, replacement order, and other execution choices remain part of a system whenever changing them changes the system. Do not extract defining semantics merely to make an interface look cleaner.

## 12. Keep Dataset Concerns Outside Program Semantics

The intended flow is explicit and one-way:

```text
program -> application/rollout result -> experiment encoding -> batch/visualization
```

Flattening, padding, token ordering, type prefixes, coordinate metadata, loss masks, and visualization operate on generated traces. They must not distort the generator API or become hidden inputs to program execution.

## 13. Generalize From Adversarial Constructions

Implement the smallest set of examples that exercises every suspected primitive and difficult interaction. Choose examples likely to break the design, not merely typical examples.

Let those examples reveal the actual component contracts, invariants, and
genuinely different Rule compositions. Expand to all 60 audited executable
families only after the common mechanisms survive these tests without
exceptions or duplicated paths.

## 14. Treat Failed Composition as Design Information

When an implementation requires duplicated rule logic, a special flag, an exception path, hidden state, fake padding, a conversion fallback, or a test weakened to permit it, stop implementation immediately.

Determine whether the abstraction, requirement, or proposed family grouping is wrong. Delete or redesign incorrect work rather than protecting sunk cost.

## 15. Validate Constructive Fidelity

Tests should verify canonical book examples, transition semantics, effect application, structural invariants, and interactions among components. A system is covered only when its native specification maps cleanly into the chosen construction.

Tests describe intended semantics. Never rewrite a test merely to accommodate an implementation that violated them; revise a test only when first-principles analysis shows that the stated semantics were wrong.

## 16. Distinguish Architecture From Patching

A single explicit, total, and tested mapping between layers is an architectural boundary. A fallback conversion introduced because one construction does not fit is a shim.

A named construction parameter is legitimate when it describes real semantics. A flag that selects incompatible internal paths or patches an abstraction failure is not.

## Summary

> Share only what is genuinely shared. Make irreducible differences explicit. Never purchase apparent uniformity by hiding the real system inside an escape hatch.
