# Goal 5 Execution Loop

Use this loop to execute `goal-5/0-plan.md` without rebuilding the process
overhead that Goal 5 is intended to remove.

## Repeatable Loop

1. Sync current state with the actual files, `git status`, relevant diffs,
   corpus counts, and tests.
2. Update `goal-5/0-plan.md` with current facts before starting the next stage.
3. Select the first incomplete stage whose prerequisites are ready.
4. Create or refresh `goal-5/[INDEX]-[SHORTHAND].md` from the template below.
5. Implement only that stage.
6. Add verification and no-cheating checks tied directly to that stage's
   completion requirements.
7. Run focused tests, appropriate affected repository tests, and whitespace/diff
   checks.
8. Record commands, results, discoveries, and remaining limitations in the
   stage file.
9. Fold durable results and changed assumptions back into `0-plan.md`.
10. Continue toward the original objective. If stopping, leave the goal
    resumable with current evidence, the next action, unblock steps, and
    assumptions still needing tests.

## Global Invariants

- Do not narrow the user's objective without saying so.
- Do not mark a stage complete without evidence for each completion
  requirement.
- Do not treat a green test as evidence for a requirement the test does not
  exercise.
- Prefer small, low-complexity stages that narrow uncertainty and produce a
  useful corpus increment.
- Convert blockers into explicit work items, bounded deferrals, or honest known
  limitations; do not conceal them behind tooling.
- Preserve the distinction between implementation, validator, diagnostic, and
  fallback paths.
- Keep `ref/A-New-Kind-of-Science/` byte-for-byte immutable.
- Protect unrelated worktree changes. Inspect before deleting, especially in
  Stage 1.
- Never use repaired output as the next build's source.
- Never infer missing author text from plausibility, parser success, or model
  preference.
- Keep generated navigation and explanations visibly separate from author text.
- Do not recreate Goal 4's general schema, lock, authority, review, provenance,
  race-defense, or mutation infrastructure.
- Add a tool, abstraction, ledger, or test only when it protects a named Goal 5
  acceptance criterion.
- The practical release may retain disclosed OCR/layout uncertainty. It may not
  claim exhaustive source fidelity while that uncertainty exists.

## Stage Discipline

- Only one stage is `IN_PROGRESS` at a time.
- A stage file is an execution record, not a second expanding master plan.
- Prefer a direct corpus-specific implementation over a reusable framework.
- Reuse a Goal 4 fact only after rederiving or independently checking it; do
  not preserve Goal 4 machinery as its own justification.
- Keep repair records proportional: author-text changes need guarded evidence;
  generated paths and navigation need deterministic tests, not scholarly
  provenance rows.
- When a fixed-layout witness is unavailable, preserve uncertain source text
  and document the limitation. Do not block unrelated structural progress.
- Review stage scope with `git diff --name-status` and `git diff --check` before
  declaring completion.

## Verification Selection

Every stage runs the checks named in its completion requirements. In addition:

- Stage 1 checks deletion scope, protected diffs, legacy hashes, stale caches,
  and broken references.
- Stage 2 checks corpus inventory, boundaries, image counts, path layout, and
  baseline drift fixtures.
- Stage 3 checks 29-document coverage, source ordering, conservation, image
  resolution, and clean-build behavior.
- Stage 4 checks every repair preimage, changed-passage evidence, known defect
  sentinels, rendering, and unresolved-candidate disclosure.
- Stage 5 checks the complete navigation graph, image paths, anchors, and
  representative rendered documents.
- Stage 6 reruns all Goal 5 checks, affected repository tests, two-build
  comparison, legacy hash comparison, scope inspection, and the declared spot
  review.

Avoid automatic escalation from a real defect to a generalized framework. Add
the smallest check that would have caught the actual defect and a nearby
regression.

## Stage File Template

```markdown
# [INDEX]-[SHORTHAND]

Status: NOT_STARTED

## Current Facts

- Facts from current code, tests, documents, Git state, and previous stages.

## Updated Assumptions

- Assumptions that still look valid.
- Assumptions that changed.
- Assumptions that need tests before being trusted.

## Big Picture Objective

- Restate the stage objective, adjusted for current facts.

## Detailed Implementation Plan

- Concrete code, document, data, cleanup, and test changes for this stage.
- Files expected to change or be removed.
- Focused commands and manual inspections required.

## No-Cheating Checks

- Checks that prove protected legacy/unrelated work was not altered.
- Checks that prove the build uses raw legacy input, not repaired output.
- Checks that prevent unsupported author-text changes or false fidelity claims.
- Stage-specific forbidden shortcuts and how they are detected.

## Completion Requirements

- Requirement-by-requirement evidence.
- Required test and validation commands.
- Documentation or known-limitation updates.
- Scope and whitespace/diff checks.

## Stage Results

- Fill in at the end of the stage.
- List commands run and their outcomes.
- Record what changed and what was deliberately left unchanged.
- Record what was learned and any new limitation.
- State what must change in `0-plan.md` before the next stage.
```

## Stop And Resume Contract

When stopping before the goal is complete:

- Leave at most one stage marked `IN_PROGRESS`.
- Record the exact current Git state and files intentionally modified.
- Record the last passing and failing commands without overstating coverage.
- Name the next concrete action, not merely the next stage title.
- Carry source uncertainty into `known-limitations.md` or the active stage file.
- Do not call the repaired corpus released until Stage 6 requirements pass.

