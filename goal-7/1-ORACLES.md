# 1-ORACLES

Handoff stage: **G7-00 — Freeze behavior and independent oracles**

Status: **IN PROGRESS**

## Current Facts

- Goal 6 closed at commit
  `60bde6da318f415e43e14fc98b5faa28f14cd945`.
- Goal 7 execution begins from clean scaffold commit
  `95ba134ee8f9671181c237cd2975004f3442efbe`.
- The execution-start environment is Python `3.10.13` with NumPy `2.2.6`.
- At execution start, `uv run pytest -q tests` reports
  `102 passed, 96 skipped`.
- The 96 skips are inert Goal 7 obligation shells and prove no target
  behavior.
- The execution-start source tree is
  `af9ae63c9b3683fd9b7ba1292d9127f647dc48f5`; its tests tree is
  `a77a8f6092c9b3f907a1bd6aee7c6b09c1055fa7`.
- The pre-shell Goal 6 runtime tree is
  `6e6b34769d60508c03d0a69fad1ede4fef75e217`; its tests tree is
  `02ad081e039a46efbf61855fdeae60abb7bb70ad`.
- Goal 2 and Goal 5 tree identities are respectively
  `48b6309655ec7c1d3aaa1a0ec5dfb700385e16d1` and
  `ba62f20b8c620094a0ad683906a803c5404be5f2`.
- The live package is version `0.1.0`, has 67 root exports, and still exposes
  physical `ca.specs` and `ca.rollout` modules.
- No prior Goal 7 stage file exists.

## Updated Assumptions

- The current scalar, one-dimensional, and multidimensional behavior can be
  frozen as tiny one-step expected data without importing the 0.1 executor.
- The PX fixtures in `goal-6/conformance.md` provide enough exact data to
  freeze mobile, Turing, substitution, multiway, constraint,
  variable-support, stochastic, and differential/intensional results.
- Test-only symbolic structural terms can state exact expected semantics before
  final runtime class spelling exists. They must contain no evaluator,
  callback, solver, or catalog lookup.
- Stage 1 should add active tests only for fixture completeness,
  self-consistency, and static independence. Actual native/generic CT12
  comparison remains owned by G7-01 and later.

## Big Picture Objective

Freeze useful 0.1 behavior and the required cross-family one-step expectations
as immutable, implementation-independent test data. Record the exact
pre-cutover public surface so G7-01 can prove its removal without retaining a
compatibility executor.

## Detailed Implementation Plan

- Add one test-only oracle module containing:
  - the exact pre-cutover commit, environment, tree, package, root-export, and
    obsolete-module snapshot;
  - current scalar, cellular, and multidimensional one-step expectations; and
  - named exact CT12 fixtures for mobile, Turing, substitution, multiway,
    constraint zero/one/many, variable support, stochastic laws, and
    differential/intensional relations.
- Represent complete expected results with exact source/read/write data,
  source atoms, total dispositions, successors or no-successor reasons,
  witnesses, provenance, lineage, cardinalities, successor fibers, measures,
  and intensional relation ASTs.
- Add active tests that prove:
  - the oracle source imports only the Python standard library;
  - it cannot call `ca`, `apply`, rollout, catalog, Rule evaluation, commit, or
    solver helpers;
  - all required CT12 mechanics have at least one named exact fixture;
  - finite cardinalities, fibers, dispositions, witnesses, and measures are
    internally consistent; and
  - the intensional fixture is a closed structural relation rather than a
    hidden computation.
- Point the skipped CT12 comparison shell at the frozen fixture module without
  treating that skip as evidence.
- Change no file under `src/ca`.

## No-Cheating Checks

- Parse the oracle test source with `ast`; reject non-stdlib imports and
  forbidden runtime/evaluator call targets.
- Keep fixture construction declarative. Helper functions may construct frozen
  records but may not step, evaluate, solve, draw, commit, or normalize a
  semantic result.
- Do not call the current executor to generate expected values.
- Compare the Stage 1 diff to the execution-start commit and require it to
  touch only `goal-7/` and `tests/`.
- Verify Goal 2, Goal 5, `src/ca`, `pyproject.toml`, and `uv.lock` are
  unchanged.
- Run the original active tests separately from the new oracle-consistency
  tests.

## Completion Requirements

- The original 102 tests pass.
- Every minimum future CT12 mechanics class has a named exact expected fixture.
- Oracle completeness, structural consistency, and static independence tests
  pass.
- The precise pre-cutover root exports, target root exports, obsolete modules,
  package metadata, environment, and tree identities are recorded.
- `uv run pytest -q tests` is green; the 96 future obligation skips remain
  visibly pending.
- `git diff --check` passes.
- The complete Stage 1 diff contains no runtime, packaging, Goal 2, or Goal 5
  change.

## Stage Results

- Pending implementation and verification.
