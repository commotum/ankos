# 1-CUTLINE

## Current Facts

- The baseline command `uv run pytest -q` passed four tests in 0.83 seconds.
  None of those tests asserts a generated successor State.
- `tests/test_smoke.py` exercises the forbidden ECA preset, old rollout result
  hierarchy, and old serialization round-trip. It is not a compatibility
  obligation for the new kernel.
- The first test in `tests/test_catalog_progress.py` checks the ordering and
  uniqueness of `ref/types.csv`; that is useful metadata integrity. The second
  test rewards the existence and signatures of 60 planned builders and must
  not survive as implementation evidence.
- The only executable example, `examples/export_viz_samples.py`, consumes old
  dataset presets and visualization projections. It is downstream work, not a
  core compatibility obligation.
- No tracked in-repository production consumer depends on the current `ca`
  runtime API. `pyproject.toml` declares no scripts, entry points, or workspace
  dependents.
- `README-V2.md` is the configured project readme and documents the rejected
  five-field/Frontier/loci API. It must be rewritten rather than used to force
  compatibility.
- `import ca` currently imports the old mutually dependent semantic system,
  including `loci`, `frontiers`, `program`, catalog implementations, and
  serialization.
- Current `SimpleProgram` contains Seed and Frontier. Current rollout calls the
  old `apply` machinery and returns a proof/result hierarchy. Neither is
  adaptable to the target without preserving rejected semantics.
- `loci` is a base dependency of alphabets, seeds, frontiers, neighborhoods,
  rules, program, datasets, serialization, and catalog modules. The live core
  must therefore be replaced as one coherent island rather than peeled away
  behind adapters.
- A bare State cannot supply a graph Seed's realized adjacency. The clean
  reference signature is `step(trajectory, state)`: Trajectory supplies the
  program and Seed realization while State remains only an immutable explicit-
  time coordinate-to-value slice.

## Updated Assumptions

- A clean break is justified: no evidenced in-scope consumer requires the old
  API. Any newly discovered external compatibility request requires explicit
  user authorization rather than an automatic adapter.
- State will remain a plain immutable mapping whose full coordinate keys share
  one explicit time.
- `step(trajectory, state)` will use `trajectory.seed.shape` for realized
  bounds or relational adjacency. It will not duplicate this context inside
  every State.
- The first kernel will support one available source-time slice. Historical
  reads are explicitly rejected until a future family demonstrates that need.
- Datasets, serialization, preset catalog implementations, and viz export can
  be disconnected or removed during cutover. Independent low-level assets do
  not justify keeping a broken public subsystem.

## Big Picture Objective

Fix the clean replacement boundary so the following stages cannot drift into
compatibility wrappers or retain legacy machinery simply because existing
tests import it.

## Detailed Implementation Plan

- Replace the live public kernel rather than adding a parallel v2 namespace.
- Retain the package name `ca`, packaging metadata, `py.typed`, reference
  documentation, and `ref/types.csv`.
- Replace `__init__.py`, alphabets, seeds, neighborhoods, rules, and execution
  with the ordinary-value kernel.
- Add Space, selector, and rollout modules required by the target model.
- Delete `loci.py` and `frontiers.py` with no facades.
- Remove or disconnect old datasets, serialization, catalog implementations,
  and the visualization example. Preserve taxonomy identity only as honest
  unavailable entries.
- Rewrite tests around anonymous Cartesian and relational behavior. Retain
  taxonomy order/uniqueness checking without requiring stub call signatures.
- Rewrite the configured README and target API documents at cutover.

## No-Cheating Checks

- Do not make `import ca` select a new path while leaving the old path callable
  through another root export.
- Do not preserve `apply`, `steps`, `replay_key`, `Rollout*`, old codec records,
  dataset IDs, ECA aliases, or semantic loci/frontiers for old tests.
- Do not close a relational Neighborhood over one concrete graph. That would
  make Seed shape part of SimpleProgram identity.
- Do not interpret the current four green tests as behavioral validation.

## Completion Requirements

- [x] Current public and internal imports were inspected.
- [x] In-repository consumers and examples were inspected.
- [x] The baseline test command and its evidentiary limits were recorded.
- [x] Every retained category has a goal-specific reason.
- [x] No backwards-compatibility obligation was found.
- [x] The relational realization issue was resolved as
  `step(trajectory, state)`.
- [x] No replacement code or preset was implemented during this stage.

## Stage Results

- Stage 1 is complete.
- The project will proceed as a clean replacement, not an adapter migration.
- Stage 2 should implement only the small immutable values and direct local
  validation required by the target composition.
- Stage 4's provisional `step(program, state)` wording must be interpreted and
  updated as `step(trajectory, state)`.
