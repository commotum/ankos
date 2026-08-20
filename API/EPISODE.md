# EPISODE

Status: **reserved target concept; detailed contract deferred**

## Settled Relationship

```text
rollout(TRAJECTORY, RESOURCES/LIMIT) -> EPISODE
```

Episode is the name reserved for the output of rollout. Nothing beyond that
relationship is fixed by the present architecture.

## Why This Specification Is Intentionally Small

The nine core documents can define program generation, initial conditions, and
Trajectory identity without prematurely choosing one execution model for every
family.

Different families may eventually require different notions of:

- a limit, such as steps, duration, depth, events, or convergence;
- a resource, such as memory, solver effort, or branch budget; and
- a realized result, such as dense slices, sparse states, paths, branches, or
  another exact representation.

Those requirements should be learned from real implementations. This document
does not invent abstractions for them in advance.

## Deliberately Unspecified

The following are open:

- the signature of `rollout`;
- whether `RESOURCES` and `LIMIT` are one argument, several arguments, or
  family-specific controls;
- whether Episode has `states`, `coordinates`, or another representation;
- whether Episode is always finite;
- branching and stochastic realization;
- continuous, event-driven, relational, and solver-backed realization;
- stopping and partial-result behavior;
- batching and parallel execution; and
- serialization.

No provisional field or wrapper should become part of the public API merely to
fill this gap.

## What Episode Is Not Yet

Episode is not currently specified as:

- a downstream training example or serialized dataset record;
- a batch element;
- a fixed dense array type;
- an `initial state + horizon` request object.

These may be downstream uses or future design options, but none is part of the
settled semantic definition.

## Future Completion Criterion

This specification should be expanded only after representative
SimplePrograms expose the smallest rollout contract that works across their
actual needs. At that point the design must preserve the already settled
relationship:

```text
TRAJECTORY identifies the path
rollout applies a later execution request
EPISODE is the result
```

The future design must not move Seed back into SimpleProgram or move rollout
limits into Trajectory identity.

## Relationships

See [TRAJECTORY.md](TRAJECTORY.md). Rollout remains outside the resolved scope
of the other generator and value specifications.
