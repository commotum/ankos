# Design Principles

## 0. Intent Outranks Wording

Optimize for the simplest coherent design, not compliance with prior wording. Requirements and abstractions are hypotheses. When a real construction does not compose naturally, stop. Identify the violated assumption, re-derive the model, and present the necessary divergence before continuing.

A blocker honestly reported is preferable to a working implementation built from exceptions, duplicated paths, or concealed incompatibilities.

## 1. Discover Constructions; Do Not Assume Them

Seek the smallest shared construction mechanisms demonstrated by the catalog. Treat the 45 types as evidence, not as proof that every entry is a preset of one preselected algebra.

Catalog labels do not create executors. Presets, restrictions, and aliases should resolve to shared constructions only when the constructions are genuinely the same.

## 2. Share Execution Only Where Semantics Are Shared

Use one reference executor wherever systems genuinely share an execution algebra. Never create family-specific rollouts, but never conceal fundamentally different semantics behind an empty universal interface.

For transition and rewrite systems, the candidate common process is:

```text
active  = FRONTIER.select(state)
reads   = NEIGHBORHOOD.read(state, active)
results = RULE(active, reads)
next    = UPDATE.apply(state, results)
```

This process must be validated against representative constructions. If supporting a family requires `Any`, family switches, hidden engines, duplicated semantics, or global-state smuggling, stop and reconsider the algebra.

## 3. Give Each Component One Responsibility

Within the common transition algebra:

- `FRONTIER`: where rules fire.
- `NEIGHBORHOOD`: what those loci can observe.
- `RULE`: what semantic results are proposed.
- `UPDATE`: how applicable results become the next state.

These boundaries are hypotheses too. Redraw them if a real construction demonstrates that the responsibilities are wrong.

## 4. Make Rule Results Explicit and Typed

Same-site assignment is one possible effect, not universal implicit behavior. Mutation-producing rules return explicit effects that may write, move, insert, delete, splice, rewire, or otherwise modify their state model.

Do not relabel constraints, derivatives, distributions, or observations as effects merely to force them through one interface. Their types must preserve their actual semantics.

## 5. State Contains Everything Needed to Advance

For structured state:

```text
STATE = SUPPORT/TOPOLOGY + VALUES + CONTROL
```

`CONTROL` includes heads, active markers, instruction pointers, cyclic counters, and any memory required to make the process Markovian. It is part of state, not hidden executor state.

The alphabet defines possible values. It does not by itself define where values exist, how locations relate, or what control state is active.

## 6. Keep Addresses Separate From Topology

The program core does not privilege a serialization address. Sequence order, graph adjacency, tree structure, and higher-dimensional geometry must remain explicit in state or metadata rather than being inferred accidentally from integer proximity.

ANKoS may encode traces as `[t,x,y,z]` where that encoding preserves every distinction required by the experiment. If a construction exposes the encoding as inadequate, change the experiment schema rather than distort the program.

## 7. Match Support to the Construction

Fixed lattices remain fixed. Growing sequences and networks grow naturally. Sparse systems remain sparse when sparsity is semantic.

Padding, truncation, and capacity limits belong only at explicit finite-computation, batching, or serialization boundaries. They must not masquerade as program semantics.

## 8. Separate Semantics From Representation

A system fitting into a tensor does not mean its construction is tensor-local. Any lowering into canonical addresses must preserve every semantic distinction required by the task and remain inspectable.

Lossy projections are acceptable only when loss is the declared purpose, as in visualization or a chosen observable. They are not valid substitutes for the underlying state.

## 9. Separate Only Genuinely Independent Choices

Geometry, alphabet, frontier, neighborhood, rule reduction, determinism, update semantics, seed, and boundary behavior should compose when they are semantically independent.

Some choices are intrinsically coupled: rule tables depend on neighborhood arity, effects depend on the state model, and symmetries depend on topology. Represent genuine coupling through explicit invariants and strict validation rather than pretending every component combines freely.

## 10. Use Presets Without Hiding Behavior

The family index should configure common systems and validate parameters strictly while returning an ordinary shared specification. A preset is declarative convenience, not an alternate implementation.

Every catalog entry should remain discoverable, but multiple entries may resolve to the same construction with different parameters, restrictions, seeds, or validation rules.

## 11. Separate Incidental Algorithms From Defining Semantics

A constraint is distinct from its solver. A PDE is distinct from its discretization and integrator. A stochastic rule is distinct from its RNG implementation.

But synchronous update, first-match order, replacement order, and other execution choices remain part of a system whenever changing them changes the system. Do not extract defining semantics merely to make an interface look cleaner.

## 12. Keep Dataset Concerns Outside Program Semantics

The intended flow is explicit and one-way:

```text
program -> trace -> experiment encoding -> batch/visualization
```

Flattening, padding, token ordering, type prefixes, coordinate metadata, loss masks, and visualization operate on generated traces. They must not distort the generator API or become hidden inputs to program execution.

## 13. Generalize From Adversarial Constructions

Implement the smallest set of examples that exercises every suspected primitive and difficult interaction. Choose examples likely to break the design, not merely typical examples.

Let those examples reveal the actual structural families. Expand to all 45 catalog entries only after the common mechanisms survive these tests without exceptions or duplicated paths.

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
