# Trajectory

## Definition

A `Trajectory` pairs one definite SimpleProgram with one definite compatible
Seed:

```python
@dataclass(frozen=True)
class Trajectory:
    program: SimpleProgram
    seed: Seed
```

```text
SIMPLEPROGRAM + SEED -> TRAJECTORY
```

It is the fully selected initial-value problem to execute. In this API,
Trajectory names the path determined by those conditions, before a particular
rollout limit has materialized all of its States.

## Compatibility boundary

Trajectory is where program and initialization first meet. Construction
checks that:

- Seed coordinates match Space axes;
- Seed shape/support can be interpreted by Space;
- Seed supplies exactly one complete initial slice;
- every Seed value belongs to Alphabet.

Trajectory construction does not execute Neighborhood functions. A
relation-based selector validates its required plain Seed relation when it is
used by `step`.

This allows Seed sources to remain reusable. They do not need to accept one
exact SimpleProgram merely to exist.

## No execution policy

Trajectory contains neither generated successor States nor a rollout limit.
The same Trajectory may be evaluated for one step during a quick check and for
many steps during dataset construction:

```python
short = rollout(trajectory, limit=1)
long = rollout(trajectory, limit=100)
```

Both executions begin with the same immutable Seed State.

## Step

`step(trajectory, state)` constructs exactly one complete successor State.
Trajectory supplies the Seed because Space enumeration, normalization, or
relation-based Neighborhood selection may need the realized shape/support even
after the first step.

The source State is never changed. All returned coordinates have explicit time
one greater than the source State.

## Pairing generated values

A future workload may pair program and Seed sources with ordinary loops:

```python
for program in programs():
    for seed in seeds():
        if compatible(program, seed):
            yield Trajectory(program, seed)
```

`compatible` need not become a framework object. Direct construction and a
small exception boundary are also sufficient for early preset code.
