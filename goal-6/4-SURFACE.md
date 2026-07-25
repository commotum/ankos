# 4-SURFACE

Status: **IN PROGRESS**

## Current Facts

- Stages 1–3 are complete. `goal-6/architecture.md` is authoritative for the
  five component contracts, result algebra, generic application, and
  application/rollout boundary.
- The Stage 4 scoped baseline contains only the completed Stage 3 planning
  edits in `goal-6/0-plan.md`, `goal-6/3-APPLICATION.md`, and
  `goal-6/architecture.md`. No runtime file, frozen Goal 2 file, or Stage 4
  public/reference input is concurrently modified.
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
  Rule-side result descriptors remain with `rules.py`. The existing
  `rollout.py` remains an auxiliary traversal file behind callable
  `ca.rollout`; separate public `results.py`, `replacement.py`, `engine.py`,
  or `run.py` modules are unnecessary.
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
  auxiliary `rollout.py`, structural configuration/locus vocabulary to
  `loci.py`, and codecs to `serialization.py` without creating
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
- `goal-6/4-SURFACE.md`
- `goal-6/0-plan.md`

## No-Cheating Checks

- `SimpleProgram` has exactly five stored fields in every normative example.
- No `configuration.py`, `replacement.py`, `results.py`, `engine.py`, `run.py`,
  sixth component, family executor, or catalog dispatch registry is introduced.
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

- [ ] Every locked file and public boundary has one cohesive, nonduplicated
      responsibility and an acyclic dependency direction.
- [ ] The core/catalog tree and six catalog module names match the locked
      target exactly.
- [ ] Root, component-module, catalog-module, and alias import conventions are
      explicit and the intended examples have one obvious spelling.
- [ ] `api.md`, `simple_programs.md`, `goal-6/architecture.md`, and the
      reference scaffold describe one architecture with distinct document
      roles.
- [ ] The scaffold is syntactically valid, readable top-to-bottom, and contains
      no obsolete program axis, unrestricted callback, family dispatch, or
      alternate executor.
- [ ] Current runtime migration sources have target dispositions without
      performing Goal 7 work.
- [ ] Deferred auxiliary organization has a stable dependency boundary and no
      unresolved core/catalog responsibility.
- [ ] Hostile review, path/link/import examples, syntax, terminology,
      whitespace/diff, frozen hashes, and behavioral-tree checks pass.
- [ ] Stage 5 can create the exact 60-family catalog matrix without reopening
      surface ownership or public naming conventions.

## Stage Results

To be completed after the ownership, document/scaffold cutover, hostile review,
and verification pass.
