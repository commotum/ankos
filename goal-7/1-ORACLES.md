# 1-ORACLES

Handoff stage: **G7-00 — Freeze behavior and independent oracles**

Status: **COMPLETE**

## Current Facts

- Goal 6 closed at
  `60bde6da318f415e43e14fc98b5faa28f14cd945`.
- `1562041e4dab0a6d9e51d730222de0a4f1b52038` is the
  preimplementation-shell baseline named by the original Goal 7 plan.
- Actual Goal 7 execution starts from the clean scaffold commit
  `95ba134ee8f9671181c237cd2975004f3442efbe`.
- The execution-start environment is CPython `3.10.13` with NumPy `2.2.6`.
- Before Stage 1, `uv run pytest -q tests` reported
  `102 passed, 96 skipped`. The skips are inert Goal 7 obligation shells and
  prove no target behavior.
- Goal 6's pre-shell source and test trees are respectively
  `6e6b34769d60508c03d0a69fad1ede4fef75e217` and
  `02ad081e039a46efbf61855fdeae60abb7bb70ad`.
- The execution-start source and test trees are respectively
  `af9ae63c9b3683fd9b7ba1292d9127f647dc48f5` and
  `a77a8f6092c9b3f907a1bd6aee7c6b09c1055fa7`.
- Frozen Goal 2, Goal 5, and Goal 6 tree identities are respectively
  `48b6309655ec7c1d3aaa1a0ec5dfb700385e16d1`,
  `ba62f20b8c620094a0ad683906a803c5404be5f2`, and
  `dfeaa1d302acceb274a6dec815ae587dada7ac78`.
- The live package remains version `0.1.0`, with description
  `A New Kind of Science cellular automata library` and runtime dependencies
  `numpy>=2.2` and `pytest>=9.0.3`.
- The pre-cutover root has 67 ordered exports. Its canonical
  `{name,module,kind,signature}` manifest has SHA-256
  `fe4f136f50cf1471268278b5f62a33492bad090808605a9a3f7c048aed81a4f2`
  under CPython `3.10.13`.
- A fresh `import ca` eagerly loads `ca.specs`, `ca.rollout`, `ca.datasets`,
  `ca.rng`, and `ca.viz`. It does not load the target `ca.program`,
  `ca.serialization`, or `ca.catalog` surfaces.
- The physical obsolete modules are `ca.specs` and `ca.rollout`. The frozen
  execution-site inventory also records root imports, dataset
  `_rule`/`_neighborhood` branching, the visualization dependency on specs,
  and `rules.instantiate` family dispatch.

## Updated Assumptions

- The retained native surface is six concrete presets, not merely three broad
  shape representatives. All six therefore receive independent one-step
  fixtures.
- Mobile and Turing spellings share the same coupled head/write mechanic and
  one closed branching fixture; catalog aliasing will be tested separately.
- Exact differential completion and an intensional differential relation are
  distinct obligations and need separate fixtures.
- Stage 1 activates only fixture-schema, consistency, and independence tests.
  Behavioral comparisons against the new runtime remain future CT12 work.
- Closed frozen dataclasses, tagged structural terms, tuples, strings,
  integers, and `Fraction` values are sufficient oracle data. No callback,
  evaluator, solver, draw, catalog lookup, or runtime result is needed.

## Big Picture Objective

Freeze useful 0.1 behavior and all future CT12 reference expectations as
implementation-independent test data. Preserve the exact pre-cutover surface
for later negative cutover tests without retaining a compatibility executor.

## Detailed Implementation Plan

The completed implementation adds
[`test_oracles.py`](../tests/conformance/test_oracles.py), which owns:

- an exact pre-cutover snapshot containing commits, trees, environment,
  package metadata, ordered root exports, public-manifest hash, eager imports,
  obsolete modules/sites, and selected Git-blob and SHA-256 identities;
- a neutral complete-result schema for source outcomes, applied atoms,
  typed no-successor partitions, total dispositions, progress, continuation,
  successors, all three cardinalities, witnesses, provenance, lineage,
  certificates, fresh bindings, quotient fibers, evidence, and three explicit
  measure views;
- exact `absent`, `available`, and `unavailable` measure states so absence is
  never inferred from a nullable probability;
- 16 closed fixtures:

  | Fixture | Authority and mechanic |
  |---|---|
  | `native.scalar.ar2-modular` | retained AR2 scalar |
  | `native.temporal.dyadlags-rule-150` | retained 3-lag lookup |
  | `native.temporal.lagcounts-rule-91` | retained count-banded temporal lookup |
  | `native.cellular.dyadrads-rule-30` | retained 1-D cellular lookup |
  | `native.multidimensional.dyadaxes-2d-rule-128` | retained 2-D lookup |
  | `native.multidimensional.dyadaxes-3d-rule-128` | retained 3-D lookup |
  | `px01.mobile-head-branching` | PX01/F031 mobile and Turing coupled writes |
  | `px02.parallel-substitution` | PX02/F038 old-snapshot structural substitution |
  | `px04.multiway-diamond` | PX04/F034 derivation quotient |
  | `px04.constraint-mod3-zero` | PX04/F019 certified zero |
  | `px04.constraint-mod3-one` | PX04/F019 exactly one |
  | `px04.constraint-mod3-many` | PX04/F019 finite many |
  | `px02.graph-interface-replacement` | PX02/F029 variable support and fresh IDs |
  | `px06.stochastic-search-law` | PX06/F050 exact law and submeasures |
  | `px05.exact-differential-flow` | PX05/F037 exact maximal solution |
  | `px05.constant-field-intensional` | PX04/PX05 F041 uncountable relation |

The Stage 1 diff allowlist is exactly:

```text
goal-7/0-plan.md
goal-7/1-ORACLES.md
tests/conformance/test_oracles.py
```

The oracle fixture source itself is frozen at close with:

```text
Git blob:  83f0926ddc5ce7e1ab0a1482a9e6441fc29b6d77
SHA-256:   addb4bc2c630b6822ec871bccbd31ede153d1387ba54939d5f52768ef4dbe3b5
```

## No-Cheating Checks

- The oracle source is parsed with `ast`. Imports outside the Python standard
  library and calls to runtime/evaluator/solver/commit/rollout helpers are
  rejected.
- Dynamic-import and code-execution escapes including `__import__`,
  `import_module`, `eval`, `exec`, `compile`, `globals`, `locals`, and
  reflective `getattr` are rejected.
- A recursive data check proves no callable is embedded in the pre-cutover
  snapshot or any fixture.
- The reverse dependency is checked too: every `src/ca/**/*.py` file is
  parsed, and production may not import or mention the test oracle.
- Finite fixtures must enumerate exact source/applied atom IDs, the
  no-successor partition, total writable dispositions, exact cardinalities,
  complete successor fibers, unique fresh bindings, and structurally valid
  measures.
- The frozen 16-case ID tuple prevents later quiet deletion or substitution
  of an oracle.
- The complete diff is compared with execution start and must touch only the
  Stage 1 allowlist. Goal 2, Goal 5, Goal 6, `src/ca`, `pyproject.toml`, and
  `uv.lock` remain unchanged.

## Completion Requirements

- The original active suite remains exactly `102 passed, 96 skipped`.
- All 16 future CT12 reference cases have exact closed expected data.
- Oracle schema, consistency, no-callback, and bidirectional independence
  tests pass.
- Pre-cutover exports, signatures, imports, obsolete execution sites,
  metadata, environment, commits, trees, and selected content identities are
  frozen.
- The full suite reports the original 102 passes plus 12 new active oracle
  checks, while all 96 future obligations remain visibly skipped.
- `git diff --check` passes and the complete Stage 1 diff stays inside the
  exact allowlist.

## Stage Results

- Stage 1 made the independent oracle contract authoritative; it changed no
  runtime, package, lockfile, or frozen prior-goal content.
- Added one test-only module with 16 complete fixtures and 12 active
  schema/independence tests.
- Verification results:
  - `python3 -m py_compile tests/conformance/test_oracles.py` — passed.
  - `uv run pytest -q tests/conformance/test_oracles.py` —
    `12 passed`.
  - `uv run pytest -q tests --ignore=tests/conformance/test_oracles.py` —
    `102 passed, 96 skipped`.
  - `uv run pytest -q tests` — `114 passed, 96 skipped`.
  - `git diff --check 95ba134ee8f9671181c237cd2975004f3442efbe` —
    passed.
- No Goal 7 obligation skip was removed. The remaining 96 skips are owned by
  G7-01 through G7-05 and remain non-evidence.
- No assumption was invalidated and no earlier obligation reopened.
- First next action: create `goal-7/2-CUTOVER.md`, resync the exact G7-01
  cutover contract, and perform the single atomic five-field runtime
  replacement. No G7-01 implementation began in this stage.
