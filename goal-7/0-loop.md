# Goal 7 Execution Loop

Use this protocol to implement one Goal 7 stage at a time. The objective is the
complete five-field `0.2.0` runtime, not merely replacing the current skipped
tests with passing tests.

## Context Startup

At the beginning of a fresh session:

1. Read `goal-7/0-plan.md` in full.
2. Read this file in full.
3. Inspect the actual repository state, current diff, active tests, and every
   completed Goal 7 stage file.
4. Read `goal-6/goal-7-handoff.md` in full when starting Goal 7. For later
   stages, reread its stage, no-cheating, and final-gate sections plus the
   authoritative Goal 6 documents routed by `0-plan.md`.
5. Treat Goal 5 as semantic authority, Goal 6 as the frozen architecture and
   implementation contract, Goal 2 as frozen selective evidence, and Goal 4
   as superseded.
6. Treat inert declarations, pending-name inventories, skipped tests, and
   `_pending()` bodies as unfinished work.

## Repeatable Loop

1. Sync current state with actual files and tests.
2. Update `goal-7/0-plan.md` with current facts before starting the next stage.
3. Select the first incomplete stage.
4. Create or refresh `goal-7/[INDEX]-[SHORTHAND].md` from the stage template.
5. Implement only that stage.
6. Add verification and no-cheating checks.
7. Run focused tests, full active verification, and whitespace/diff checks
   appropriate to the repository and stage.
8. Record results in the stage file.
9. Fold durable results back into `goal-7/0-plan.md`.
10. Continue toward the original objective. If stopping for the session, leave
    the goal in a resumable state with current evidence, next work, unblock
    actions, and assumptions to challenge.

## Stage Sequencing Rules

- Execute stages in order:
  `1-ORACLES → 2-CUTOVER → 3-MECHANICS → 4-CODECS → 5-CATALOG →
  6-CONFORMANCE → 7-RELEASE`.
- Do not begin a later stage because its shell already exists.
- G7-01/`2-CUTOVER` is one atomic completion boundary. Internal commits and
  dependency-ordered work are allowed, but no partial cutover is a completed
  stage or publishable state.
- G7-02/`3-MECHANICS` has three workstreams and one aggregate completion
  barrier. Do not mark it complete when only one workstream or primary family
  fixture passes.
- Codec inventory precedes codecs; completed codecs precede catalog behavior.
  A missing mechanic discovered during catalog work reopens mechanics and
  codecs before catalog work resumes.
- Remove each Goal 7 test skip when its owning contract becomes
  authoritative. Do not bulk-unskip tests that still contain `_pending()`.
- Stages 1–6 are internal checkpoints, not release candidates. Only
  `7-RELEASE` can close Goal 7.

## Invariants

- Do not narrow the user's objective without saying so.
- Do not mark a stage complete without requirement-specific evidence.
- Do not use green checks as evidence unless they cover the requirement.
- Prefer the smallest implementation that satisfies the frozen contract.
- Convert blockers into work items, proof obligations, diagnostics, or user
  escalations; do not erase them from the completion contract.
- Preserve the distinction between implementation, test oracle, verifier,
  diagnostic, representation adapter, and optional external realization.
- Preserve unrelated user changes and inspect a dirty worktree before editing.
- Keep `SimpleProgram` to exactly five stored fields.
- Keep Frontier as the complete possible-write envelope and Neighborhood as
  the identity-preserving readable region.
- Keep Rule responsible for applicability, scheduling, conflicts, stochastic
  laws, stopping, and complete replacements.
- Keep `apply` family-blind and rollout dependent on that one operation.
- Keep semantic descriptors closed, versioned, exact, immutable, and
  serializable.
- Keep configuration structure and visible control in Seed-produced state,
  not extra program axes.
- Keep all 60 families as ordinary constructor coverage, not subclasses,
  engines, or dispatch tags.
- Keep metadata callable-free and serialization catalog-free.
- Keep datasets, RNG, and visualization downstream and out of eager root
  imports.
- Keep Goal 2 and Goal 5 byte-for-byte frozen.
- Do not reopen Book discovery or use Goal 4 plans, tools, ledgers, archived
  tests, or audit ceremony.
- Do not run unrelated historical Goal 4 tooling as part of the active runtime
  gate. The authoritative active suite is `tests/` unless a stage names another
  focused check.
- Do not retain the 0.1 executor, manifest decoder, or broad façade as a
  fallback.
- Do not publish, deploy, or claim release readiness before `7-RELEASE`.

## Per-Stage Working Pattern

Before editing:

- record `git status --short`, current commit, and overlapping user changes;
- run the smallest active baseline that can detect regression;
- inspect the owning skeleton and the exact Goal 6 contract;
- identify which skipped obligations become active in this stage; and
- list forbidden dependencies or fallback paths to test.

During implementation:

- replace provisional shells from the inside out rather than building a
  parallel package;
- keep public names absent until their owning behavior is authoritative;
- add focused positive and negative tests with implementation-independent
  expected results;
- make validation failures typed and non-committing;
- preserve exact witnesses, identities, laws, and evidence through results;
  and
- update the stage file when a fact or assumption changes materially.

Before stage completion:

- run focused tests for every changed owner;
- run `uv run pytest -q tests`;
- run relevant static import, closure, no-dispatch, and pending-skip searches;
- run packaging/lockfile checks only when that stage owns them;
- run `git diff --check`;
- inspect the complete stage diff for unrelated edits and forbidden fallback
  code;
- record commands and exact outcomes in the stage file; and
- update `0-plan.md` current facts and stage status.

## Evidence Rules

A stage result must state:

- what behavior or contract became authoritative;
- which files changed and why;
- which tests were activated, added, removed, or retained;
- exact commands and outcomes;
- which no-cheating checks ran;
- remaining skipped Goal 7 obligations and their future owners;
- any changed assumption;
- any reopened earlier-stage obligation; and
- the first concrete next action.

The following do not count as completion evidence:

- importing a declaration that still raises `NotImplementedError`;
- a module-level skipped test;
- testing only a rendered state when the contract includes witnesses, fibers,
  measures, faults, or provenance;
- comparing catalog constructors to one another without an independent
  mechanics fixture;
- encoding and decoding with shared mutable or catalog-backed state;
- a manual inspection where an exact structural/static check is available; or
- a green test that routes through the same implementation as its oracle.

## Stage File Template

```markdown
# [INDEX]-[SHORTHAND]

## Current Facts

- Facts from current code, tests, docs, and previous stage results.

## Updated Assumptions

- Assumptions that still look valid.
- Assumptions that changed.
- Assumptions that need tests before being trusted.

## Big Picture Objective

- Restate the stage objective, adjusted for current facts.

## Detailed Implementation Plan

- Concrete code/doc/test changes for this stage.
- Files expected to change.
- New tests or commands required.

## No-Cheating Checks

- Explicit checks proving the implementation does not route through forbidden
  fallback paths.

## Completion Requirements

- Requirement-by-requirement checks.
- Required test commands.
- Documentation updates required.

## Stage Results

- Fill in at the end of the stage.
- Include tests run and outcomes.
- Include what was learned.
- Include what should change in `0-plan.md` before the next stage.
```

## Stop Conditions

Stop the current stage and leave explicit resumable work rather than
improvising when:

- a concrete audited family appears not to fit the five-field contract;
- generic application appears to require family, carrier, locus-kind, or
  catalog dispatch;
- a required semantic object appears to require an unrestricted callback,
  opaque host object, hidden solver, ambient draw, or silent approximation;
- source authority contradicts the current plan;
- an earlier stage's claimed invariant is disproved;
- a user-owned overlapping change cannot be preserved safely;
- completion requires a new external service, publishing authority, or
  separately scoped compatibility tool; or
- the work starts expanding into taxonomy rediscovery or a second runtime.

Record the exact counterexample, affected contract, evidence, attempted safe
alternatives, and required decision. Never lower the final completion gate to
make the stage appear complete.
