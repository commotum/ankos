# Episode

## Definition

An `Episode` is the materialized result of rolling out one Trajectory:

```python
@dataclass(frozen=True)
class Episode:
    states: tuple[object, ...]
```

```text
rollout(TRAJECTORY, limit) -> EPISODE
```

The initial kernel uses a nonnegative integer step limit. The Episode contains
the Seed State followed by exactly that many successor States, so
`limit=3` produces four complete States.

## State contract

Each State is a complete immutable mapping at exactly one explicit time:

```text
State 0: {(0, ...): value, ...}
State 1: {(1, ...): value, ...}
State 2: {(2, ...): value, ...}
```

Times are consecutive. Every realized coordinate in a State has a value.

Execution never changes an earlier State. Even when a logical value is equal
at consecutive times, the second occurrence belongs to a new coordinate in a
new complete slice.

## What Episode is not

Episode is not:

- a plan awaiting execution;
- a mutable simulation object;
- a stream-row wrapper containing both planned and runtime forms;
- a collection of patches, replacements, deletions, or `KEEP` actions;
- a projected tensor or serialized downstream example.

Tensor projection, batching, serialization, and PE-specific metadata can be
downstream operations over Episode rather than responsibilities of the kernel.

## Rollout boundary

The initial operation is deliberately small:

```python
episode = rollout(trajectory, limit=8)
```

Questions such as wall-clock resources, memory budgets, solver tolerances,
event termination, and non-discrete time remain future execution work. They
should be added only with a concrete family and an exact result contract. The
discrete kernel does not pretend that `t+1` already solves those cases.
