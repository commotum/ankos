# Goal 7: Five-Field Runtime Implementation

Shorthand: **Runtime Cutover**

Status: **IN PROGRESS — G7-02 MECHANICS**

## Big-Picture Objective

Implement and ship the architecture frozen by Goal 6:

```python
SimpleProgram(
    seed=...,
    alphabet=...,
    frontier=...,
    neighborhood=...,
    rule=...,
)
```

The finished `ca` package must have one immutable five-field program value,
one family-blind one-step operation, and one rollout operation that repeatedly
uses that same step:

```python
result = ca.apply(program, input)
episode = ca.rollout(program, steps=100)
```

All 60 audited semantic families must be constructible as ordinary expanded
`SimpleProgram` values through the six catalog namespaces. The implementation
must replace the current `Dynamics`/family-dispatch runtime in place, preserve
useful behavior through independent oracles rather than compatibility
execution, provide fail-closed canonical serialization, and ship as one
coherent `0.2.0` API.

This is the implementation goal. Its inert declarations and skipped tests are
starting material, not completed behavior or conformance evidence.

## Authority and Scope

Read these sources in order:

1. [`goal-6/goal-7-handoff.md`](../goal-6/goal-7-handoff.md) is the exact
   mechanics-first implementation contract and stage dependency graph.
2. [`goal-6/architecture.md`](../goal-6/architecture.md) owns semantic
   contracts, validation, application, results, ownership, and import
   direction.
3. [`goal-6/catalog-migration.md`](../goal-6/catalog-migration.md) owns the
   exact SPF001–SPF060 constructors, signatures, homes, sources, exports, and
   T01–T45 migration ledger.
4. [`goal-6/conformance.md`](../goal-6/conformance.md) owns PX01–PX12,
   CT01–CT14, independent fixtures, and the 60-family coverage join.
5. [`api.md`](../api.md), [`simple_programs.md`](../simple_programs.md), and
   [`ref/notes/ca-scaffold.py`](../ref/notes/ca-scaffold.py) are the public,
   conceptual, and compact code-shaped projections of that contract.
6. [`goal-5/integration-handoff.md`](../goal-5/integration-handoff.md) is
   consulted only to verify the remaster boundary. Goal 5 remains semantic
   authority.

Goal 2 is frozen comparison evidence only for strengths explicitly preserved
by Goal 6. Goal 4 and Book rediscovery are outside this goal. If this execution
plan appears to contradict a higher-authority source, stop, record the exact
conflict, and reconcile the plan before changing runtime behavior.

## Current Facts

- Goal 6 is complete and its Goal 7 handoff is frozen.
- The implementation-start baseline is commit
  `1562041e4dab0a6d9e51d730222de0a4f1b52038`.
- The clean Goal 7 scaffold and actual execution-start commit is
  `95ba134ee8f9671181c237cd2975004f3442efbe`.
- G7-00 froze 16 independent oracle cases and closed with
  `114 passed, 96 skipped`.
- G7-01 is complete. Its durable transaction record and exact evidence are in
  [`2-CUTOVER.md`](2-CUTOVER.md).
- The live package is now the five-field runtime: `SimpleProgram` stores
  exactly `seed`, `alphabet`, `frontier`, `neighborhood`, and `rule`;
  `program.apply` is the sole family-blind step law; and callable root
  `rollout` traverses only through it.
- The root exposes exactly ten names: the three operations/value names and
  seven core namespaces. It does not eagerly import datasets, RNG,
  visualization, serialization, or catalog.
- `src/ca` has 28 tracked paths. `specs.py` and public `rollout.py` are
  physically absent, as is `tests/test_specs.py`; `ca.rollout` and `ca.specs`
  have no importable submodule spec.
- Exact/constructive/partial/law/intensional Seeds, reusable writable/readable
  contracts, finite/intensional Rule results, atomic reconstruction,
  cardinalities, measures, deterministic fresh identity, lineage, and replay
  evidence are authoritative for the G7-01 kernel.
- All six retained Rule presets and six Neighborhood presets execute through
  generic application and agree with independent complete-result fixtures.
- Datasets, RNG helpers, tensor projections, and visualization are downstream
  consumers of ordinary programs and explicit rollout views.
- Source and lock metadata are at `0.2.0`, NumPy is a runtime dependency, and
  pytest is development-only. This is an internal checkpoint, not a release.
- G7-02 began from clean commit
  `130b230` with `uv run pytest -q tests` reporting
  `225 passed, 36 skipped`. Every remaining skip has an explicit G7-02–G7-05
  owner; G7-01 owns none.
- Serialization and catalog files remain inert, unexposed shells. G7-02 has
  started; its live plan and evidence record is
  [`3-MECHANICS.md`](3-MECHANICS.md).
- Goal 5 established exactly 60 executable families, two close non-family
  roles, 19 covered families, and 41 additions. No family requires a sixth
  program field.
- F010 and F042 remain callable-free interface/observer roles. F039 remains an
  unused audit ID. T08 remains a retired Seed role.
- General numerical solvers and integrators are not core runtime services.
  Exact or intensional denotations are core; optional realization tooling is
  external and evidence-producing.

## Working Assumptions

- The preimplementation shells are disposable declarations. Their provisional
  records do not outrank `architecture.md`.
- Useful 0.1 behavior can be preserved by independently specified results
  without retaining any 0.1 executor or canonical-manifest fallback.
- G7-01 is a single atomic completion boundary. Internal work may be ordered
  and committed, but no partial cutover is a completed stage or release state.
- G7-02 has three workstreams but one aggregate completion barrier.
- Catalog files may physically exist before G7-04, but they remain inert,
  unexposed shells until all required mechanics and codecs are complete.
- Stages G7-00 through G7-05 are internal checkpoints. Only the reconciled
  G7-06 result may be published as `0.2.0`.
- A concrete counterexample changes assumptions; implementation inconvenience
  does not.

## Non-Negotiable Constraints and No-Cheating Rules

1. `SimpleProgram` stores exactly `seed`, `alphabet`, `frontier`,
   `neighborhood`, and `rule`.
2. Seed owns initial configuration sources. Support, topology, geometry,
   defaults, invariants, and visible control live in Seed-produced
   configuration data and shared closed structures, not extra program fields.
3. Alphabet is a closed structural value schema with exact semantic equality.
4. Frontier is the complete possible-write envelope, not merely the loci that
   fire.
5. Neighborhood is the identity-preserving readable region from one immutable
   snapshot.
6. Rule owns applicability, scheduling, conflict, stochastic law, stopping,
   and complete atomic replacement semantics.
7. `apply` owns only family-blind validation, reconstruction, commit,
   successor validation, quotienting, and measure projection.
8. Neither `apply` nor any second engine may dispatch on SPF/F/T ID, catalog
   name, constructor spelling, family, carrier, locus kind, or Book category.
   Owner modules may interpret their own sealed generic descriptors.
9. `rollout` must demonstrably call the one owned `apply`; no second one-step
   path survives.
10. Semantic data is closed, versioned, exact, and serializable. No callback,
    `Any` recipe bag, `eval`, host CAS escape, ambient RNG, silent float
    fallback, or unrestricted extension hook enters a descriptor.
11. Rule results preserve zero/one/many/intensional support, distinct
    no-successor meanings, exact cardinalities, probability laws, replay
    evidence, fresh identity, witnesses, provenance, and derivation fibers
    before successor deduplication.
12. Every one of the 60 families is coverage and a constructor, never a
    runtime subclass or engine branch.
13. Serialization is catalog-free, alias-independent, fail-closed, and stores
    exactly the five expanded program fields.
14. Catalog metadata is callable-free. Category modules do not import
    `catalog.entries`; `catalog.__init__` is the sole metadata/callable join.
15. Datasets, RNG, and visualization remain downstream consumers and are not
    eagerly imported by the root façade.
16. `specs.py`, public `rollout.py`, `Dynamics`, the old executor, and the old
    manifest decoder are deleted rather than retained behind private or
    compatibility names.
17. Goal 2 and Goal 5 remain byte-for-byte frozen. Do not reopen taxonomy or
    import Goal 4 machinery.
18. Independent test oracles may not call the implementation, catalog
    constructor, runtime evaluator, or private commit helper they judge.
19. A planned skipped test is never counted as passing conformance. Remove
    each Goal 7 skip when its owning behavior becomes authoritative.
20. No completed stage may knowingly leave the active suite red, expose two
    competing APIs, or claim release readiness.

## Target Package Boundary

The final semantic package surface is:

```text
src/ca/
├── __init__.py
├── program.py
├── loci.py
├── alphabets.py
├── seeds.py
├── frontiers.py
├── neighborhoods.py
├── rules.py
├── serialization.py
├── py.typed
└── catalog/
    ├── __init__.py
    ├── entries.py
    ├── automata.py
    ├── substitua.py
    ├── machina.py
    ├── media.py
    ├── criteria.py
    └── dynamica.py
```

`datasets.py`, `rng.py`, and `viz/` remain auxiliary downstream modules. Do
not add public `configuration.py`, `regions.py`, `replacement.py`,
`results.py`, `engine.py`, `rollout.py`, `run.py`, `updates.py`, or a second
package tree.

## Success Metrics and Final Verification

Goal 7 is complete only when all of the following are true:

- the target file and export surface matches the Goal 6 handoff;
- `SimpleProgram` has exactly five stored fields;
- `specs.py`, public `rollout.py`, and every production copy of the old
  executor are absent;
- exactly one family-blind `apply` exists and rollout is proven to reuse it;
- CT01–CT14, PX01–PX12, all eight required secondary pressure joins, and the
  SPF001–SPF060 coverage join pass;
- catalog counts, homes, role boundaries, callable kinds, exports, aliases,
  presets, compatibility spelling, and T01–T45 dispositions exactly match
  `catalog-migration.md`;
- all useful native fixtures agree with independent complete-result oracles;
- every public semantic record round-trips through the fail-closed five-key
  codec and every claimed representation relation commutes over a full step;
- datasets, RNG, and visualization remain downstream and cannot affect
  program identity or application;
- no Goal 7 pending skip, `_pending()` body, inert constructor, or
  scaffold-only `NotImplementedError` remains in active source/tests;
- source, installed wheel, public signatures, docs, reference scaffold,
  `pyproject.toml`, and `uv.lock` agree on `0.2.0`; and
- one final hostile review finds no covert sixth field, second executor,
  family dispatch, lossy compatibility path, or missing audited family.

Required final checks include:

```text
uv run pytest -q tests
uv lock --check
git diff --check
```

G7-06 must also build a wheel, install it into a clean environment, exercise
the public imports/signatures and `py.typed`, validate documentation links and
code fences, and inspect the final diff. Exact focused commands belong in each
stage file and may evolve with the implementation.

## Stage Index

| Stage | Handoff stage | Status | Completion boundary |
|---|---|---|---|
| `1-ORACLES` | G7-00 | Complete | Frozen behavior and independent expected results |
| `2-CUTOVER` | G7-01 | Complete | Atomic five-field runtime replacement |
| `3-MECHANICS` | G7-02 | In Progress | All 60 rows supported by reusable mechanics |
| `4-CODECS` | G7-03 | Pending | Canonical serialization and representation proofs |
| `5-CATALOG` | G7-04 | Pending | Exact constructors, metadata, exports, and migration |
| `6-CONFORMANCE` | G7-05 | Pending | All normative suites and joins pass together |
| `7-RELEASE` | G7-06 | Pending | Docs, packaging, cleanup, and hostile final gate |

No stage file exists until that stage begins.

### 1-ORACLES

Handoff stage: **G7-00 — Freeze behavior and independent oracles**

Stage status: **Complete.** Durable evidence and the exact 16-case inventory
are recorded in [`1-ORACLES.md`](1-ORACLES.md).

#### Big Picture Objective

Freeze the useful behavior and public facts of the 0.1 runtime without
preserving its architecture, so the cutover can be judged independently.

#### Detailed Implementation Plan

- Record the starting commit, Python/NumPy versions, active test result,
  `src/ca` and `tests` tree identities, current root exports, obsolete modules,
  and package metadata in `goal-7/1-ORACLES.md`.
- Transcribe tiny exact expected results for the current scalar, cellular,
  and multidimensional examples.
- Add independent expected results or named exact fixtures for mobile/Turing,
  substitution, multiway, constraint, variable-support, stochastic, and
  differential/intensional cases selected by `conformance.md`.
- Keep expected results in test-only fixtures or literal test data. Do not
  compute them by importing future `program.apply`, catalog constructors,
  runtime Rule evaluators, rollout kernels, or private commit helpers.
- Add a static dependency check proving oracle independence.
- Make no behavioral change under `src/ca`.

#### Completion Requirements

- The original 102 active tests still pass.
- Every future CT12 case has an independently specified expected result or a
  named exact fixture.
- Oracle-independence checks pass.
- The precise pre-cutover root surface and obsolete-module list are recorded
  for later negative tests.
- The stage diff contains test/fixture and Goal 7 documentation changes only.

### 2-CUTOVER

Handoff stage: **G7-01 — Atomic five-field core cutover**

Stage status: **Complete.** The implementation, migration, hostile review,
and exact verification evidence are recorded in
[`2-CUTOVER.md`](2-CUTOVER.md).

#### Big Picture Objective

Replace the live 0.1 runtime in one internally ordered transaction with the
five-field structural kernel, component contracts, one generic application
law, and migrated downstream consumers.

#### Detailed Implementation Plan

- Implement in this order:

  ```text
  loci + Alphabet
  → Seed/WritableRegion/ReadableRegion
  → Rule denotation and result algebra
  → SimpleProgram/apply/Seed binding/rollout
  → current native component presets
  → root/datasets/RNG/viz/tests
  → physical old-executor deletion
  ```

- Replace provisional shells with the exact closed structures in
  `architecture.md`; do not preserve provisional shapes merely because they
  already compile.
- Implement exact structural identities, region algebra, value schemas,
  source forms, readable/writable contracts, Rule ASTs, outcomes,
  cardinalities, dispositions, witnesses, provenance, continuation, and
  faults.
- Implement five-way compatibility validation and the exact application phase
  order: old-snapshot resolution, result validation, fresh binding, atomic
  commit, successor validation, witness-preserving quotient, and measures.
- Implement Seed denotation/realization and replay evidence in `program.py`;
  core must not import `rng.py`.
- Make rollout call only the owned `apply`.
- Preserve the six current Rule presets and six Neighborhood presets only as
  module-qualified components.
- Replace dataset family dispatch with four explicit program recipe builders;
  move tensor materialization and structured Seed planning to their settled
  private downstream owners.
- Adapt visualization to explicit `DatasetEpisode`/`DatasetBatch` views while
  retaining viewer bundle version 1.
- Atomically narrow the root façade; remove broad flattened component names
  and obsolete semantic records.
- Delete `src/ca/specs.py`, `src/ca/rollout.py`, and
  `tests/test_specs.py`.
- Set source version `0.2.0`, update the package description, and move pytest
  to the development dependency group. This is not permission to publish.
- Rewrite or activate every G7-01-owned unit and conformance test.

#### Completion Requirements

- The complete active suite is green with all G7-01-owned skips removed.
- There is exactly one executable step law and no production copy or fallback
  of the tensor/family executor.
- Independent native fixtures match complete generic results.
- `ca.rollout` is callable; `import ca.rollout` fails because no physical
  submodule exists.
- Initial `import ca` does not load datasets, RNG, or visualization.
- Core descriptors contain no callbacks, opaque `Any`, mutable recipe bags,
  ambient entropy, or semantic family/name dispatch.
- CT01, the kernel portions of CT02–CT08, CT12, and CT13 pass.
- No completed state exposes both the old and new runtime.

### 3-MECHANICS

Handoff stage: **G7-02 — Reusable mechanics closure**

#### Big Picture Objective

Complete the reusable component mechanics required by all 60 families without
adding family-specific runtime types or behavior to `program.py`.

#### Detailed Implementation Plan

- Complete the three handoff workstreams with their exact SPF assignments:
  M-A for coupled existing-support/control mechanics, M-B for dynamic
  structure/branching/representation work, and M-C for
  global/intensional/law mechanics.
- Implement required loci, Alphabet, Seed, WritableRegion, ReadableRegion, and
  Rule variants in their owning modules.
- Keep `program.py` family-blind; change it only to repair a demonstrated
  generic contract defect.
- Exercise all PX01–PX12 primary fixtures and all eight required secondary
  joins through the same `apply`.
- Preserve F004 and F045 as executable constructions while F010 and F042
  remain non-executable roles.
- For every sealed variant, record a codec-inventory entry containing its tag,
  version, exact fields, owner, local validator, and equality law.
- Keep catalog modules inert and unexposed during this stage even though their
  physical shells already exist.
- Keep numerical search, integration, and approximation outside the semantic
  core; exact/intensional denotations remain authoritative.

#### Completion Requirements

- M-A, M-B, and M-C all close at one aggregate barrier.
- Every SPF001–SPF060 row has its assigned mechanics and direct fixture.
- All twelve pressure categories and eight secondary joins pass.
- Dynamic identity, fresh/delete support, conflicts, schedules, global reads,
  continuous/intensional results, laws, mutable program state, priority, and
  one-shot results satisfy their pressure contracts.
- No Rule performs a draw, solver search, numerical integration, recursive
  `apply`, or ambient lookup.
- The active suite remains green with exactly one application path.
- The codec inventory is complete before any catalog behavior is implemented.

### 4-CODECS

Handoff stage: **G7-03 — Canonical serialization and representation relations**

#### Big Picture Objective

Implement lossless, versioned, fail-closed serialization for every closed
semantic value and prove every claimed representation relation over complete
application results.

#### Detailed Implementation Plan

- Replace the serialization shell with canonical `dumps`/`loads` and typed
  `Decoded`, `DecodeRejected`, and `DecodeFault` results.
- Use tag `ca.simple-program`, schema version `1`, and exactly the payload keys
  `seed`, `alphabet`, `frontier`, `neighborhood`, and `rule`.
- Cover every G7-01/02 codec-inventory entry, including results, evidence,
  laws, traces, exact values, identities, and intensional ASTs.
- Enforce canonical ordering/re-encoding and reject unknown tags, versions,
  fields, primitives, forged digests, partial migrations, and 0.1 manifests.
- Implement only total validated lossless migrations.
- Add inverse-on-image and full-result commutation tests for each claimed
  representation.
- Add the serialization namespace to the root without importing catalog.

#### Completion Requirements

- CT09 and CT10 pass for every inventory entry.
- Decode failure is typed and exposes no partially restored authoritative
  value.
- Semantic owner modules do not import serialization.
- Serialization never imports catalog or records constructor provenance,
  SPF/F/T IDs, aliases, or invocation receipts.
- Canonical payloads have exactly five expanded program fields.
- No 0.1 `Dynamics` manifest is accepted.

### 5-CATALOG

Handoff stage: **G7-04 — Catalog assembly and exact legacy migration**

#### Big Picture Objective

Turn the audited catalog shells into explicit, ordinary constructors and
callable-free metadata over already-tested mechanics.

#### Detailed Implementation Plan

- Implement exactly 60 canonical exact-slug constructors in their primary
  homes with explicit closed keyword-only signatures.
- Replace private pending-name inventories with the exact authorized preset,
  alias, and compatibility functions from `catalog-migration.md`; do not guess
  an unresolved signature.
- Populate immutable callable-free `FamilyEntry`, `RoleEntry`, `LegacyEntry`,
  `LegacyTarget`, and `NameEntry` values.
- Implement explicit category exports and collision-free flat exports in
  `catalog.__init__`; do not synthesize functions or add a registry.
- Implement the exact T01–T45 migration ledger, including T08's zero targets,
  T40's two named branches, and the sole category-qualified deprecated K.
- Make every callable return an ordinary validated expanded `SimpleProgram`
  composed only from mechanics already covered by G7-03 codecs.
- Add the catalog namespace to the root without giving it execution authority.

#### Completion Requirements

- SPF IDs are exactly SPF001–SPF060 with home counts
  `11 / 15 / 8 / 14 / 9 / 3`.
- Coverage is exactly 19 covered and 41 additions.
- F010/F042 remain callable-free roles and F039 remains unused.
- Legacy dispositions and callable-kind counts exactly match
  `catalog-migration.md`, including `C=5`, `P=39`, `A=4`, and `K=1`.
- T32 and T44 are presets, not aliases.
- Every constructor/delegate expansion passes exact five-field equality.
- CT11, CT14's catalog boundary, and the constructor half of the 60-family
  coverage join pass.
- There is no `construct(id)`, umbrella `kind=`, registration hook, callable
  metadata, or catalog-selected executor.

### 6-CONFORMANCE

Handoff stage: **G7-05 — Complete conformance**

#### Big Picture Objective

Close every normative test obligation together and prove that the implemented
surface has no hidden alternate semantics.

#### Detailed Implementation Plan

- Complete and unskip CT01–CT14.
- Complete the primary SPF001–SPF060 join and all eight named secondary
  pressure joins.
- Verify the exact T01–T45 manifest, independent native/generic full-result
  equivalence, and all PX01–PX12 fixtures.
- Compare full source outcomes, applied atoms, no-successor partitions,
  cardinalities, measures, witnesses, fresh bindings, lineage, fibers, and
  evidence—not rendered states alone.
- Run static import/no-dispatch checks, blocked-catalog apply/decode checks,
  root signature/submodule-shadow checks, and rollout-versus-manual-apply
  proofs.
- Build an ephemeral wheel and run clean-install/import/type-marker smoke
  checks without publishing it.
- Search active source and tests for every remaining Goal 7 skip, `_pending`,
  scaffold-only `NotImplementedError`, legacy executor, and forbidden import.

#### Completion Requirements

- All fourteen CT suites, twelve pressure groups, sixty canonical rows, eight
  secondary joins, and exact legacy manifest pass together.
- No Goal 7 obligation remains skipped or false-passing.
- Test oracles remain independent of the code they judge.
- No unsupported realization is disguised as undefinedness, exact zero,
  divergence, or semantic completion.
- Static dependency, single-apply, public-surface, and blocked-catalog checks
  pass.
- The active source suite and ephemeral installed-wheel smoke suite are green.

### 7-RELEASE

Handoff stage: **G7-06 — Documentation, packaging, and cleanup**

#### Big Picture Objective

Reconcile source, documentation, packaging, and installed behavior into one
release-ready `0.2.0` story and remove all transitional scaffolding.

#### Detailed Implementation Plan

- Update `README-V2.md` to describe the implemented runtime; retain
  `README-V1.md` only as an explicit historical snapshot.
- Document source migration from 0.1 construction recipes to catalog
  constructors or explicit five-field construction. Do not add a fallback
  decoder.
- Remove pending-target language from `api.md` while preserving its contract.
- Reconcile `simple_programs.md`, public docstrings, and
  `ref/notes/ca-scaffold.py` with exact implemented signatures, exports,
  ownership, and schema version.
- Remove dead imports, compatibility scaffolding, stale runtime examples,
  family switches, and duplicate contracts.
- Reconcile `pyproject.toml` and `uv.lock`.
- Run focused and full active tests, lockfile checks, build/install smoke,
  link/code-fence checks, formatting, whitespace, and final diff inspection.
- Conduct one strong hostile review against every final completion gate.
- Update `GOALS.md` only after all evidence passes.

#### Completion Requirements

- A fresh reader sees one implemented five-field API story.
- Source, tests, docs, lockfile, wheel, signatures, and `py.typed` agree.
- No obsolete module, pending scaffold, second executor, or compatibility
  decoder remains.
- The complete final verification matrix passes from a clean checkout/install.
- The hostile review finds no sixth field, family dispatch, missing family,
  lossy migration, or observer/tooling leak.
- Only then may Goal 7 be marked complete and the result be considered a
  `0.2.0` release candidate.

## Stop and Escalation Conditions

Stop the current stage, preserve evidence, and request direction when:

- an audited family demonstrably cannot fit the five fields;
- correctness appears to require a family/carrier/catalog branch in `apply`;
- a required exact semantic value cannot be represented by closed data;
- Goal 5 and Goal 6 authorities contain a concrete contradiction;
- completing a stage would require changing frozen Goal 2 or Goal 5;
- a user-owned overlapping change cannot be preserved safely; or
- external authority is required to publish, release, or add optional solver
  infrastructure.

Do not resolve those conditions by weakening tests, adding a sixth field,
retaining the old executor, inventing a compatibility decoder, silently
approximating exact semantics, or reopening the taxonomy.
