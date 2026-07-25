# 4-SURFACE

Status: **COMPLETE — ownership, public/reference cutover, and hostile review verified**

## Current Facts

- Stages 1–3 are complete. `goal-6/architecture.md` is authoritative for the
  five component contracts, result algebra, generic application, and
  application/rollout boundary.
- The Stage 4 scoped baseline contains only the completed Stage 3 planning
  edits in `goal-6/0-plan.md`, `goal-6/3-APPLICATION.md`, and
  `goal-6/architecture.md`. No runtime file, frozen Goal 2 file, or Stage 4
  public/reference input was concurrently modified. The first autosave after
  Stage 3 completion is commit
  `53e813ddd251541e035b4f3e632133e215a6043b`.
- At the start of the stage, `api.md` was a 1,128-line question/answer design
  history, `simple_programs.md` was a 2,199-line fixed `t+N D` cellular-
  automata trajectory schema, and `ref/notes/ca-scaffold.py` was a 200-line
  `Component`/`Dynamics`-era template. They have now been replaced in place by
  target public, conceptual, and code-shaped projections of one architecture.
- The current runtime still exposes `Dynamics`, `RawEpisode`, `RawBatch`,
  component factories at package root, and a tensor-oriented `rollout.py`.
  Stage 4 may specify their target ownership/cutover but may not implement it.

## Updated Assumptions

- One cohesive `program.py` owns `SimpleProgram`, application-side records,
  family-blind one-step application, and private reconstruction while
  Rule-side result descriptors remain with `rules.py`. It also owns callable
  `ca.rollout` and its public records so a same-named submodule cannot shadow
  the function. Goal 7 folds or privatizes the existing `rollout.py`;
  separate public `results.py`, `replacement.py`, `engine.py`, or `run.py`
  modules are unnecessary.
- `loci.py` can own common immutable carrier/configuration identity and
  selector structure without creating `configuration.py`; `seeds.py` owns
  initial sources of those configurations.
- A small root namespace centered on plural constructor modules,
  `SimpleProgram`, `apply`, `rollout`, `serialization`, and `catalog` is more
  legible than re-exporting every component preset and catalog constructor.
- `simple_programs.md` can become the conceptual explanation of the model while
  `api.md` remains the exact public contract and `goal-6/architecture.md`
  remains the implementation-planning authority.
- Auxiliary generation/dataset/RNG/viz organization can remain deferred if the
  accepted input/output boundary is explicit and does not affect program
  identity or generic application.

## Big Picture Objective

Translate the settled contracts into one small, intuitive file/public API
surface and one readable code-shaped reference scaffold, so a fresh session
sees the five-field architecture without design-history contradictions.

## Detailed Implementation Plan

- Define exact ownership and dependency direction for every locked core and
  catalog file, the root namespace, and the public apply/rollout boundary.
- Assign Rule-side dispositions/outcomes to `rules.py`, application-side
  results and atomic application to `program.py`, repeated traversal to
  the same program-level public boundary, structural configuration/locus
  vocabulary to `loci.py`, and codecs to `serialization.py` without creating
  noun-per-concept modules.
- Define root imports, module-qualified component constructors, catalog
  re-exports, alias expansion, canonical serialization, and collision rules.
- Record how current `specs.py`, `rollout.py`, `Dynamics`, raw episode/batch
  types, and broad root re-exports migrate in Goal 7 without changing them now.
- Rewrite `api.md` as the concise normative public contract.
- Rewrite `simple_programs.md` as the current conceptual account: five fields,
  relational Rule semantics, configuration ownership, representative
  constructions, and semantic names as catalog constructors.
- Rewrite `ref/notes/ca-scaffold.py` in place as syntactically valid reference
  code ordered:
  `loci -> component primitives -> compounds -> general constructors/presets
  -> SimpleProgram -> catalog constructors/aliases -> apply -> rollout`.
- Add the durable ownership, imports, documentation roles, and deferred
  auxiliary boundary to `goal-6/architecture.md`.
- Conduct one focused hostile surface review and resolve substantive findings.

Files expected to change:

- `goal-6/architecture.md`
- `api.md`
- `simple_programs.md`
- `ref/notes/ca-scaffold.py`
- `README-V1.md`
- `README-V2.md`
- `goal-6/4-SURFACE.md`
- `goal-6/0-plan.md`

## No-Cheating Checks

- `SimpleProgram` has exactly five stored fields in every normative example.
- No `configuration.py`, `replacement.py`, `results.py`, `engine.py`, `run.py`,
  public `rollout.py`, sixth component, family executor, or catalog dispatch
  registry is introduced.
- Rule receives only resolved `R` and writable capability `W`; the scaffold
  does not regress to per-locus proposals or unrestricted configuration reads.
- Root convenience imports do not duplicate component construction logic or
  flatten all catalog/component names into one collision-prone namespace.
- Every catalog constructor and alias expands to an ordinary five-field
  `SimpleProgram`; canonical serialization never depends on alias lookup.
- `rollout` remains tooling over repeated `apply`, and one-shot use requires
  no trajectory.
- Auxiliary datasets/generation/RNG/viz internals are not redesigned or used
  to hide a core ownership decision.
- No behavioral `src/ca`, frozen Goal 2, Stage 5 catalog-migration, Stage 6
  conformance, or Goal 7 implementation file is changed.

## Completion Requirements

- [x] Every locked file and public boundary has one cohesive, nonduplicated
      responsibility and an acyclic dependency direction.
- [x] The core/catalog tree and six catalog module names match the locked
      target exactly.
- [x] Root, component-module, catalog-module, and alias import conventions are
      explicit and the intended examples have one obvious spelling.
- [x] `api.md`, `simple_programs.md`, `goal-6/architecture.md`, and the
      reference scaffold describe one architecture with distinct document
      roles.
- [x] The scaffold is syntactically valid, readable top-to-bottom, and contains
      no obsolete program axis, unrestricted callback, family dispatch, or
      alternate executor.
- [x] Current runtime migration sources have target dispositions without
      performing Goal 7 work.
- [x] Deferred auxiliary organization has a stable dependency boundary and no
      unresolved core/catalog responsibility.
- [x] Hostile review, path/link/import examples, syntax, terminology,
      whitespace/diff, frozen hashes, and behavioral-tree checks pass.
- [x] Stage 5 can create the exact 60-family catalog matrix without reopening
      surface ownership or public naming conventions.

## Stage Results

- The target tree now has one acyclic responsibility split. `loci.py` owns
  shared identity/region structure; the five plural component modules own
  their closed descriptor algebras; `rules.py` owns Rule-side outcomes;
  `program.py` owns the exactly-five-field `SimpleProgram`, application-side
  outcomes, family-blind `apply`, rollout records, and the root-callable
  `rollout`; `serialization.py` owns fail-closed codecs; and `catalog/` owns
  ordinary whole-program constructors plus metadata-only entries.
- The root exposes the component and catalog namespaces plus only
  `SimpleProgram`, `apply`, and `rollout` as direct conveniences. Component
  presets remain module-qualified. Catalog constructors remain category-
  qualified, with only unique explicit convenience re-exports such as
  `ca.catalog.eca`; aliases always expand to ordinary five-field values.
- There is no target public `rollout.py`. Goal 7 must physically fold the
  current traversal into `program.py` or rename helpers to a private,
  nonconflicting path; merely excluding the submodule from `__all__` would
  still allow it to shadow callable `ca.rollout`.
- `api.md` is now the concise normative target contract,
  `simple_programs.md` is the conceptual five-field account,
  `goal-6/architecture.md` is the detailed implementation-planning authority,
  and both READMEs identify the current and retained runtime accurately
  without presenting it as the Goal 7 target.
- `ref/notes/ca-scaffold.py` is one executable, code-shaped walkthrough ordered
  from loci through component construction, five-field composition, catalog
  aliases, application, rollout, serialization, and the root surface. It has
  631 lines / 587 nonblank lines. Independent hostile review judged that to be
  the upper edge of compact but still one readable progression; further
  compression would remove contract-bearing distinctions.
- Hostile review found and resolved the substantive risks: a same-named
  rollout submodule, a shared result envelope that created an ownership cycle,
  raw-input normalization drift, optional-lineage and initial-state mismatch,
  ambiguous catalog exports, callable metadata entries, decode construction
  before validation, lossy/intentionally finite rollout sketches, and
  unrepresentable or collapsed owner-specific result records. The final API
  consistency and concept/scaffold reviews both returned a clean pass.
- `python3 -m py_compile ref/notes/ca-scaffold.py`,
  `python3 ref/notes/ca-scaffold.py`, Markdown fence parity, path inspection,
  import/example inspection, and `git diff --check` pass. No full runtime test
  run was warranted because Stage 4 changes only documentation and reference
  material.
- Relative to the Stage 4 baseline, only the eight expected files changed.
  `src/ca`, `tests`, `goal-2`, and `goal-5` have no diff. Their frozen tree
  hashes remain `6e6b34769d60508c03d0a69fad1ede4fef75e217`,
  `02ad081e039a46efbf61855fdeae60abb7bb70ad`, and
  `48b6309655ec7c1d3aaa1a0ec5dfb700385e16d1` for the first three
  respectively. Goal 2 handoff and README SHA-256 values remain
  `5792ac1810dafdd0be6343e1d03c4b1ab20c48551efd73400fea5a1812a9f192`
  and `e063609c7a52d32bd0a4d3bb384cd5da233c34f57a169e2db6cce197c76e0c4d`.
- Stage 5 is now the first incomplete stage. It can map the 60 audited
  executable families into the six locked catalog modules without reopening
  core ownership, public naming, or application semantics.
