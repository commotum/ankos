# ankos

> **Runtime status:** This README documents the currently implemented 0.1.0
> runtime and its tests. The settled five-field target API is specified in
> [`api.md`](api.md) and remains pending Goal 7 implementation. The runtime
> axes and examples below are therefore current usage, not target
> architecture.

ANKoS is a small Python lab for the central experiment in *A New Kind of
Science*: take a very simple rule, run it for a while, and look at what it
actually does.

The bet of the project is the same bet Wolfram makes in the book. Equations and
closed-form analysis are only one way to do science. Another way is to search
the space of simple programs directly. Some rules die out, some repeat, some
make nested structure, some look random, and a few make persistent moving
structures that are hard to predict without just running them.

This package gives those experiments one common spine:

```text
domain:        scalar, line, plane, or volume through time
shape:         the finite extent of the run
alphabet:      the possible cell states
seed:          the initial state
boundary:      what happens at the edge
frontier:      which cells update
neighborhood:  what each updated cell reads
rule:          how reads become the next state
```

Import it as `ca`.

## Quick Start

Install dependencies:

```bash
uv sync
```

Run the tests:

```bash
uv run pytest -q
```

Roll a scalar second-order recurrence:

```python
import numpy as np

import ca

dynamics = ca.Dynamics(
    domain="t+0d",
    shape=(),
    rule=ca.ar2_modular_0d(modulus=97),
    neighborhoods=(),
    frontier=ca.time_slice(()),
)

episode = ca.rollout(
    dynamics=dynamics,
    rule_id=0,
    seed_state=np.array([1, 2]),
    steps=4,
)

print(episode.states.tolist())
# [2, 3, 4, 5]
```

Roll a two-dimensional Dyadaxes system:

```python
import numpy as np

import ca

dynamics = ca.Dynamics(
    domain="t+2d",
    shape=(3, 3),
    rule=ca.dyadaxes_2d_rule(),
    neighborhoods=(ca.dyadaxes_2d_neighborhood(),),
    frontier=ca.time_slice((3, 3)),
    boundary={"policy": "fixed", "value": 0},
)

seed_state = np.array(
    [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ],
    dtype=np.int64,
)

episode = ca.rollout(dynamics, rule_id=37, seed_state=seed_state, steps=8)

print(episode.states.shape)
# (8, 3, 3)
```

The important thing is not that this tiny example is impressive. The important
thing is that the same API scales across the little families you want to sweep:
change the rule id, seed, shape, dimension, boundary, or neighborhood, then
look at the trajectory.

## What This Is For

ANKoS is not trying to be a giant CA framework. It is a fixed-grid trajectory
generator and construction API for experiments inspired by the book:

- Chapter 2's crucial experiment: simple cellular automata do not always behave
  simply.
- Chapter 3's broader claim: the same behavior types recur across many simple
  program families.
- Chapter 5's dimensional question: higher dimensions add geometry, but not a
  totally different story.
- Chapter 6's random-start experiments: order, randomness, and localized
  structures can be studied systematically.
- Chapter 7 and 8's modeling lesson: simple local rules can be explanatory
  mechanisms, not just curve-fitting devices.
- Chapter 10 through 12's computational lesson: perception, prediction,
  randomness, universality, and irreducibility are part of the same story.

The code is deliberately small so the moving parts stay visible. If you want to
understand a run, read the rule, the neighborhood, the seed, and the rollout.
There should not be much else hiding behind the curtain.

## Mental Model

An episode is a full-state trajectory over canonical coordinates:

```text
[t, x, y, z]
```

Unused spatial axes are fixed at zero:

```text
t+0D: [t, 0, 0, 0]
t+1D: [t, x, 0, 0]
t+2D: [t, x, y, 0]
t+3D: [t, x, y, z]
```

ANKoS follows Wolfram's next-state convention:

```text
state t -> state t + 1
```

At each update time:

1. The frontier selects current-state sites.
2. The neighborhood reads offsets around each selected site.
3. The rule maps those reads to a next value.
4. The result is written at the same spatial coordinate on time `t + 1`.

Temporal recurrences can also read earlier source times such as `t - 1`.

## API

The main runtime path is:

```text
ca.Dynamics + rule_id + seed_state + steps
    -> ca.rollout(...)
    -> ca.RawEpisode
```

`ca.Dynamics` describes the reusable mechanics:

- `domain`: `t+0d`, `t+1d`, `t+2d`, or `t+3d`
- `shape`: native spatial shape
- `rule`: rule family
- `neighborhoods`: read stencils
- `frontier`: update-site selector
- `boundary`: spatial read behavior
- `metadata`: optional result metadata

`ca.RawEpisode` returns raw states, flattened canonical coordinates, and
metadata. State arrays keep their native rank:

```text
t+0d: (steps,)
t+1d: (steps, x)
t+2d: (steps, x, y)
t+3d: (steps, x, y, z)
```

Use `ca.canonical_coords(domain, shape, steps)` when you want the flattened
`[t, x, y, z]` coordinate table directly.

For homogeneous batches, use:

```python
batch = ca.rollout_batch(
    dynamics=dynamics,
    rule_ids=np.array([0, 37, 255]),
    seed_states=seed_states,
    steps=32,
)
```

Batch rows may use different rule ids and seeds. They share one `Dynamics`,
shape, and horizon.

## Loading From A Manifest

```python
import numpy as np

import ca

manifest = {
    "domain": "t+2d",
    "shape": [3, 3],
    "dynamics": {
        "neighborhood": {"family": "dyadaxes_2d"},
        "frontier": {"family": "time_slice"},
        "rule": {"family": "dyadaxes_2d"},
        "boundary": {"policy": "fixed", "value": 0},
    },
}

dynamics = ca.dynamics_from_spec(manifest)
seed_state = np.ones((3, 3), dtype=np.int64)
episode = ca.rollout(dynamics, rule_id=0, seed_state=seed_state, steps=2)
```

## Coordinates

Spatial axes are centered:

```text
shape (3,) -> x = -1, 0, 1
shape (4,) -> x = -1, 0, 1, 2
```

This makes odd-sized grids naturally center on zero while even-sized grids keep
a deterministic integer convention.

## Built-Ins

Rules:

- `ar2_modular_0d`
- `dyadlags_0d`
- `dyadrads_1d`
- `dyadaxes_2d`
- `dyadaxes_3d`

Neighborhoods:

- `self_at`, `literal_offsets`, `metric_radius`, `shell`, `axis_shell`
- `l1_shell`, `change_count_shell`, `directional_line`, `directional_fov`
- `eca`, `moore`, `von_neumann`, `history`
- `ar2_0d`, `dyadlags_0d`, `dyadrads_1d`, `dyadaxes_2d`, `dyadaxes_3d`

Seeds:

- `pair`, `uniform_pair`, `uniform_bits`, `constant`, `point`, `bernoulli`,
  `selector_seed`
- `subspace`, `finite_segment`, `body`, `compound`, `region`, `periodic`
- `path`, `transform`, `structured`

Alphabets:

- `int_range_alphabet`
- `float_range_alphabet`
- `boolean`
- `symbolic`

Boundary policies:

```python
{"policy": "none"}
{"policy": "fixed", "value": 0}
{"policy": "periodic"}
{"policy": "reflective"}
```

## File Structure

```text
src/ca
|-- loci.py            canonical coordinates, selectors, masks, gathering
|-- alphabets.py       finite raw value spaces
|-- seeds.py           seed specs and rendering
|-- neighborhoods.py   read stencils
|-- frontiers.py       update-site selectors
|-- rules.py           rule channels and families
|-- rollout.py         NumPy rollout and batched rollout
|-- specs.py           manifests and result types
|-- rng.py             reproducible RNG helpers
`-- __init__.py        public exports
```

The shortest path through the code is:

```text
README-V2.md -> src/ca/specs.py -> src/ca/neighborhoods.py
             -> src/ca/rules.py -> src/ca/rollout.py
```

For seed experiments, add `src/ca/seeds.py`. For coordinate behavior, start in
`src/ca/loci.py`.

## Reproducible Seeds

Use `ca.rng` to derive NumPy generators for stochastic seed rendering:

```python
import ca

rng = ca.numpy_rng({"policy": "splitmix64", "base_rng": 12345}, episode_index=7)
seed_state = ca.render(ca.bernoulli(p_low=0.5, p_high=0.5), shape=(16,), rng=rng)
```

Pass the rendered `seed_state` to `ca.rollout(...)`.

## Current Scope

The implemented runtime is intentionally narrower than the full generator
schema in `ref/notes/generator.md`.

Currently supported:

- fixed-grid trajectories in `t+0d`, `t+1d`, `t+2d`, and `t+3d`
- compact neighborhood reads
- full time-slice frontiers
- fixed, periodic, reflective, and no-boundary policies
- named Phase 1 families: AR2, Dyadlags, Dyadrads, and Dyadaxes
- raw NumPy rollout and same-dynamics batched rollout

Not yet the full story:

- arbitrary state-dependent frontiers
- fixed-support neighborhoods with masks
- clamp boundary policy
- generic isotropic, semi-totalistic, totalistic, formulaic, or stochastic
  rule manifests
- non-grid systems such as mobile automata, substitution systems, networks, or
  multiway systems

Those are natural extensions, but the present package keeps the first surface
small and testable.

## References

```text
ref/A-New-Kind-of-Science/Contents.md     canonical book contents and navigation
ref/notes/generator.md                    trajectory generator schema
ref/notes/CA-Types.md                     construction taxonomy
```

## Development

```bash
uv run pytest -q
```
