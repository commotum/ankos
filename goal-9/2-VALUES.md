# 2-VALUES

## Current Facts

- Stage 1 established a clean break with no evidenced compatibility consumer.
- Relational realization data belongs to Seed and will be available to
  execution through Trajectory.
- Importing any submodule currently executes the legacy root initializer, so
  the root must stop eagerly importing the old runtime as soon as the new
  values exist.

## Updated Assumptions

- `State` does not need a nominal class. It can remain an immutable mapping
  from full explicit-time coordinate tuples to values.
- Space, SimpleProgram, Seed, Trajectory, and Episode genuinely bundle values
  and may be small frozen records.
- Alphabet may be any ordinary container or membership callable.
- Neighborhood may be a tuple of offsets or callable; Rule is callable.
- Seed will carry `shape`, complete initial values, and optional plain relation
  mappings. This is enough for both Cartesian and relational fixtures.

## Big Picture Objective

Create the minimal frozen composition values and disconnect root import from
the legacy runtime, without implementing selection, execution, or presets.

## Detailed Implementation Plan

- Add `src/ca/core.py` with the five small records and immutable mapping
  helpers.
- Validate only facts whose violation makes the value ambiguous: explicit
  coordinate time, complete Space support, Alphabet membership, and fixed
  boundary membership.
- Deeply detach mutable mappings/sequences supplied to Seed and Episode so
  later caller mutation cannot alter semantic States.
- Update `src/ca/__init__.py` to expose the new values and stop eager legacy
  imports. Execution exports will be added in Stage 4.
- Add focused behavior tests proving Seed independence, shape-polymorphic
  compatibility, defensive immutability, and direct rejection.

## No-Cheating Checks

- `core.py` must not import any legacy `ca` module.
- No Locus, Carrier, Region, Configuration, Frontier, proof, contract,
  capability, or semantic family class may be introduced.
- No preset or canonical Rule may be used in tests.
- A passing equality test alone is insufficient; mutation detachment and
  compatibility behavior must be exercised.

## Completion Requirements

- The new values construct from ordinary tuples, mappings, containers, and
  callables.
- Root import does not load legacy runtime modules.
- Changing only Seed leaves SimpleProgram unchanged.
- One SimpleProgram accepts two complete Seeds with different finite shapes.
- Incomplete support and Alphabet-invalid values fail directly.
- Focused tests pass; legacy-suite failures are recorded rather than hidden by
  adapters.

## Stage Results

- Added `src/ca/core.py` with only five frozen records: `Space`,
  `SimpleProgram`, `Seed`, `Trajectory`, and `Episode`. State remains a plain
  immutable mapping with full explicit-time coordinate keys.
- Alphabet is a container or predicate, Neighborhood is an offset tuple or
  callable, and Rule is an ordinary callable.
- Seed defensively detaches mutable values, shape data, and relation mappings.
- Trajectory directly checks complete realized support, coordinate rank, Seed
  Alphabet membership, and fixed-boundary Alphabet membership.
- Replaced the root initializer so a fresh `import ca` loads only `ca.core`.
- `uv run pytest -q tests/test_core_values.py` passed: 4 tests.
- A fresh import reported only `['ca.core']` under the `ca.*` module namespace.
- `git diff --check` passed.
- The full transitional suite reported 7 passed and 1 failed. The sole failure
  is the obsolete ECA/serialization smoke test requesting the removed old
  `ca.rollout(..., steps=..., replay_key=...)` API. No adapter was added.
- Stage 2 is complete. Stage 3 should add coordinate-only selection and keep
  boundary values out of Selector.
