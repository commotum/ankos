# 7-HANDOFF

Status: **COMPLETE — implementation handoff and final reconciliation
verified**

## Current Facts

- Stages 1–6 are complete. `goal-6/architecture.md` owns the five contracts,
  result/application semantics, file ownership, and public surface;
  `goal-6/catalog-migration.md` owns the exact 60-family and T01–T45 map; and
  `goal-6/conformance.md` owns the twelve pressure fixtures and fourteen
  reusable Goal 7 suites.
- Stage 7 began from clean autosave commit
  `c544caaef9022ce39d562b93b5d5b907592925ad`.
- Frozen tree identities remain
  `src/ca=6e6b34769d60508c03d0a69fad1ede4fef75e217`,
  `tests=02ad081e039a46efbf61855fdeae60abb7bb70ad`,
  `goal-2=48b6309655ec7c1d3aaa1a0ec5dfb700385e16d1`, and
  `goal-5=ba62f20b8c620094a0ad683906a803c5404be5f2`.
- The current runtime has one `Dynamics` path in `specs.py`, family-switched
  tensor stepping in `rollout.py`, four dataset recipes that construct
  `Dynamics`, and visualization adapters over `RawEpisode`/`RawBatch`.
  Those are migration inputs, not a second architecture to preserve.
- Goal 7 is not scaffolded or authorized. This stage produces its
  dependency-ordered handoff only.

## Updated Assumptions

- The implementation can evolve the current package in place without a
  compatibility executor: legacy construction is removed or translated into
  expanded five-field values before the one generic `apply`.
- Reusable mechanics must be implemented before the catalog constructors that
  compose them; catalog module ownership is not an implementation order.
- Existing dataset and visualization behavior can be preserved through
  downstream adapters after the semantic cutover without retaining
  `Dynamics`, `RawEpisode`, `RawBatch`, or the public `ca.rollout` submodule as
  canonical core identities.
- Conformance tests should land with the dependency they protect and culminate
  in the exact CT01–CT14 and SPF001–SPF060 joins, not be postponed as one late
  test phase.

## Big Picture Objective

Convert the closed Goal 6 architecture, catalog, and conformance contracts into
one exact mechanics-first, file-level Goal 7 implementation handoff, then prove
that Goal 6 is complete without beginning implementation.

## Detailed Implementation Plan

- Write `goal-6/goal-7-handoff.md` with the authority boundary, dependency DAG,
  ordered implementation stages, exact file dispositions, stage-local tests,
  and no-cheating completion gates.
- Assign every preserved Goal 2 strength and every Goal 5 pressure category to
  a named implementation or conformance destination.
- Assign every SPF001–SPF060 row to a mechanics-bearing implementation wave and
  every CT01–CT14 suite to the stage where its subject becomes authoritative.
- Fix the compatibility decision, schema-version cutover, root/catalog export
  cutover, `specs.py`/`rollout.py` retirement, and downstream dataset/viz
  adaptation without leaving a dual runtime.
- Reconcile the six canonical architecture/public artifacts, then conduct one
  independent hostile review and direct count/path/frozen-tree verification.
- Only after all gates pass, mark Stage 7 and Goal 6 complete and update
  `GOALS.md` to make Goal 7 the next separately authorized goal.

Files expected to change:

- `goal-6/goal-7-handoff.md`
- `goal-6/7-HANDOFF.md`
- `goal-6/0-plan.md`
- `goal-6/architecture.md`
- `GOALS.md`, but only after every Goal 6 completion gate passes

## No-Cheating Checks

- No behavioral file under `src/ca`, test file, Goal 2 file, or Goal 5 file is
  changed.
- No Goal 7 folder, scaffold, implementation branch, or runtime code is
  created.
- No stage is organized by Book chapter, catalog module, or semantic-family
  label; catalog constructors depend on prior reusable mechanics.
- No temporary `Dynamics`, adapter, decoder, dataset path, or rollout helper
  may execute through a second one-step law.
- No catalog ID, family name, constructor spelling, or metadata record may
  dispatch application or canonical decoding.
- The handoff references the canonical 60-row and T ledgers rather than
  recreating taxonomy research or Goal 4 verification machinery.

## Completion Requirements

- [x] The handoff contains an exact dependency DAG, file-level edit map,
      implementation stages, tests, and exit criteria.
- [x] Every Goal 2 preserve item and Goal 5 pressure category has a named
      destination.
- [x] All 60 SPF rows and CT01–CT14 obligations are assigned exactly.
- [x] Compatibility, deprecation, serialization versioning, root exports,
      catalog aliases, downstream adapters, and retirement steps are decided.
- [x] No unresolved core, catalog, migration, ownership, or execution-path
      question remains.
- [x] One hostile review and direct count, link, terminology, scaffold,
      whitespace, scoped-diff, and frozen-tree checks pass.
- [x] `0-plan.md`, `architecture.md`, and `GOALS.md` record Goal 6 complete and
      Goal 7 next but unauthorized; Goal 7 itself remains uncreated.

## Stage Results

- [`goal-7-handoff.md`](goal-7-handoff.md) now provides one exact seven-stage
  implementation DAG: freeze independent oracles; perform the non-splittable
  five-field core/test/downstream cutover; close reusable mechanics; implement
  codecs; assemble the catalog; join full conformance; and reconcile
  documentation, lockfile, package, and release.
- The hostile staging review exposed a real defect in the first draft:
  replacing component contracts before removing the old executor would have
  left broken checkpoints or required a forbidden parallel architecture.
  G7-01 now treats the structural kernel, components, Rule algebra,
  `SimpleProgram`/`apply`/`rollout`, native presets, root/downstream migration,
  active tests, and physical old-executor deletion as one atomic stage. No
  completed checkpoint may be red and no G7-00–G7-05 state may ship.
- The 60 families are assigned once to three primary mechanics owners with one
  aggregate barrier: `15 M-A / 30 M-B / 15 M-C`. The assignment has no hole or
  duplicate, matches every canonical SPF/F pair, and distinguishes direct
  family-fixture ownership from cross-family PX-suite ownership.
- PX01–PX12, all eight named secondary joins, CT01–CT14, the exact T01–T45
  manifest, all fifteen preserved Goal 2 strengths, and the two close-role
  boundaries have named implementation/test stages. Catalog work may compose
  only mechanics already closed and codec-inventoried earlier.
- File dispositions are exact for all 20 current tracked `src/ca` files and
  the target additions: evolve the plural components/loci in place, add
  `program.py` and `serialization.py`, add the eight catalog files, physically
  delete `specs.py` and `rollout.py`, retain `py.typed`, and keep
  datasets/RNG/visualization downstream. The resulting tracked source count is
  28.
- Compatibility is closed as a hard pre-1.0 cutover: package `0.2.0`,
  canonical `ca.simple-program` schema v1, no `Dynamics` façade, no
  old-manifest decoder/fallback, no temporary component aliases, no broad root
  compatibility exports, and T10 as the sole category-qualified `K`.
  Program-owned replay, direct-only dataset recipes, explicit dataset tensor
  views, and unchanged viewer bundle v1 have precise owners.
- The final independent reviews report no remaining API, family mapping,
  staging, import-DAG, numerical/solver, serialization, compatibility,
  downstream, release, or completion-contract defect.
- Direct checks report 60 unique family rows, homes
  `11/15/8/14/9/3`, `19 covered + 41 additions`, 45 unique T rows with
  dispositions `15/21/2/3/2/1/1`, twelve PX sections, fourteen CT suites, and
  exact 60-row conformance and mechanics joins. All 27 actual local file links
  resolve across the 19 checked canonical/stage Markdown files, all checked
  code-fence counts are even, the reference scaffold parses, compiles, runs,
  and has exact five-field/`apply`/`rollout` signatures, and
  `git diff --check` passes.
- Frozen trees remain
  `src/ca=6e6b34769d60508c03d0a69fad1ede4fef75e217`,
  `tests=02ad081e039a46efbf61855fdeae60abb7bb70ad`,
  `goal-2=48b6309655ec7c1d3aaa1a0ec5dfb700385e16d1`, and
  `goal-5=ba62f20b8c620094a0ad683906a803c5404be5f2`. Goal 2 handoff and README
  SHA-256 values remain
  `5792ac1810dafdd0be6343e1d03c4b1ab20c48551efd73400fea5a1812a9f192`
  and
  `e063609c7a52d32bd0a4d3bb384cd5da233c34f57a169e2db6cce197c76e0c4d`.
  Stage 7 did not rerun the 102 tests because both behavioral trees are
  identical to their tested baseline.
- Goal 6 is complete. No `goal-7/` folder, scaffold, runtime change, or
  implementation work was created.
