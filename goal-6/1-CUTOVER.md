# 1-CUTOVER

Status: **COMPLETE**

## Current Facts

- Goal 5 is complete: 60 executable semantic families, two close roles, 41
  family-level additions, and zero unresolved taxonomy/API questions.
- Goal 2 is a two-file frozen comparison baseline.
- Goal 4 remains on disk as superseded historical material but is not a live
  source, dependency, or methodology.
- Goal 6 began from Git commit
  `318a5383cea0898421db3993257e5aec24b7f7dd` with a clean worktree.
- The current runtime is the earlier tensor-oriented CA implementation. It
  exports `Dynamics`, not `SimpleProgram`, and has no catalog package.
- Nine runtime test files collect 102 passing cases under the installed test
  environment.
- `GOALS.md` described the obsolete Goal 4 → Goal 5 → Goal 6 sequence before
  this stage.

## Updated Assumptions

- Goal 5's completed artifacts are sufficient to remaster Goal 2 without Book
  rediscovery.
- Goal 2's reusable strengths can be separated cleanly from its superseded
  public axes and sibling ontology.
- The current runtime can be evolved in place during Goal 7; Goal 6 does not
  need a parallel package or executor.
- Goal 2's stale future-tense README can remain untouched because `GOALS.md`
  and Goal 6 now state the live sequence unambiguously.
- The detailed ownership of result helpers and the rollout implementation
  should remain open until contracts are settled, without reopening the five
  program fields.

## Big Picture Objective

Establish Goal 6 as the clean current planning authority, record the actual
repository baseline, and make Goal 5 → Goal 6 → Goal 7 explicit.

## Detailed Implementation Plan

- Inspect current goal folders, status documents, package files, exports,
  tests, and repository state.
- Update `GOALS.md` to reflect the completed, frozen, superseded, active, and
  future goals accurately.
- Create `goal-6/architecture.md` with source precedence, document ownership,
  and the compact Goal 2 preserve/replace/defer ledger.
- Record immutable tree/file hashes for the runtime, tests, and Goal 2 so the
  final Goal 6 audit can prove no behavioral or frozen-baseline change.
- Run the focused current runtime tests and record their baseline.
- Fold the results into `goal-6/0-plan.md`.

Files changed:

- `GOALS.md`
- `goal-6/architecture.md`
- `goal-6/1-CUTOVER.md`
- `goal-6/0-plan.md`

## No-Cheating Checks

- Goal 4 was inspected only enough to establish its superseded folder/status;
  none of its plans, tools, ledgers, searches, or verification contracts were
  imported.
- No Book document was read for discovery.
- `goal-2/` was read selectively for details already preserved or replaced by
  `goal-5/integration-handoff.md`; it was not edited.
- No behavioral file under `src/ca` or `tests` was edited.
- The preserve/replace/defer ledger addresses every old public axis and every
  Goal 2 planned module area.
- Stage 1 records current implementation shortcomings as migration facts; it
  does not implement Stage 2 contracts or Goal 7 code.

## Completion Requirements

- [x] The live goal index and Goal 6 source hierarchy are accurate.
- [x] Goal 2 remains unchanged and Goal 4 machinery is absent from the working
      contract.
- [x] Every Goal 2 public axis and planned module area has a preserve, replace,
      or defer disposition.
- [x] The starting runtime, tests, Goal 2, commit, and worktree state are
      recorded with reproducible evidence.
- [x] Current runtime tests pass.
- [x] Stage 2 can start from `goal-6/architecture.md` without rediscovering
      project history.

## Stage Results

### Goal and source state

- `GOALS.md` now records Goals 1, 3, and 5 as complete; Goal 2 as frozen; Goal
  4 as superseded; Goal 6 as active; and Goal 7 as future and unauthorized.
- The canonical Book entry point remains
  `ref/A-New-Kind-of-Science/Contents.md`; its 29 document links resolve.
- `goal-6/architecture.md` is now the evolving internal architecture authority.
  It gives `api.md`, `simple_programs.md`, the reference scaffold, catalog
  migration, conformance, and handoff non-overlapping roles.

### Baseline evidence

| Check | Result |
|---|---|
| `git status --short` before edits | Clean |
| `git rev-parse HEAD` | `318a5383cea0898421db3993257e5aec24b7f7dd` |
| `git rev-parse HEAD:src/ca` | `6e6b34769d60508c03d0a69fad1ede4fef75e217` |
| `git rev-parse HEAD:tests` | `02ad081e039a46efbf61855fdeae60abb7bb70ad` |
| `git rev-parse HEAD:goal-2` | `48b6309655ec7c1d3aaa1a0ec5dfb700385e16d1` |
| `sha256sum goal-2/goal-2-handoff.md` | `5792ac1810dafdd0be6343e1d03c4b1ab20c48551efd73400fea5a1812a9f192` |
| `sha256sum goal-2/README.md` | `e063609c7a52d32bd0a4d3bb384cd5da233c34f57a169e2db6cce197c76e0c4d` |
| `uv run pytest -q tests` | `102 passed in 1.10s` |

The unqualified `pytest` executable is not installed on `PATH`; the
repository's `uv run pytest` environment is the authoritative test command.

### Learned

- The live runtime already has the plural component-module direction and a
  shared locus substrate worth evolving.
- Its `Dynamics(domain, shape, rule, neighborhoods, frontier, boundary)`
  contract, family decoder, tensor raw results, and missing catalog are exactly
  the migration work Goal 7 must replace.
- Goal 2's strongest reusable material is orthogonal to its old six-axis
  surface: closed data, exactness, visibility, generic execution, typed
  evidence/results, serialization, commutation, and atomic cutover all survive.
- Stage 2 is next. It must settle component contracts and configuration/loci
  ownership before the reference scaffold or file surface is rewritten.
