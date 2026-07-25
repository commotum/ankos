# Goal 5 Execution Loop

Use this loop to execute one Goal 5 stage at a time. Goal 5 is intentionally a
lean research workflow, not an audit-platform project.

## Context Startup

At the beginning of a fresh session:

1. Read `goal-5/0-plan.md` in full.
2. Read this file in full.
3. Inspect only the canonical source and compact Goal 5 artifacts required by
   the first incomplete stage.
4. Do not open predecessor goal folders, their prose, tools, histories,
   validators, search archives, or generated outputs.
5. The sole predecessor-data exception is the one-time Stage 1 streaming
   projection defined in the plan. It is mechanical and must not be loaded
   wholesale into model context.

## Repeatable Loop

1. Sync current state with actual files, repository status, and relevant
   lightweight checks.
2. Update `goal-5/0-plan.md` with current facts before starting the next stage.
3. Select the first incomplete stage.
4. Create or refresh `goal-5/[INDEX]-[SHORTHAND].md` from the template below.
5. Implement only that stage.
6. Add verification and no-cheating checks proportional to the actual research
   risk.
7. Run focused checks, final verification appropriate to the changed
   artifacts, and whitespace/diff checks.
8. Record results in the stage file.
9. Fold durable results, changed assumptions, and the next stage into
   `goal-5/0-plan.md`.
10. Continue toward the original objective. If stopping for the session, leave
    the goal resumable with current evidence, next work, unblock actions, and
    assumptions to challenge.

## Invariants

- Do not narrow the user's objective without saying so.
- Do not mark a stage complete without evidence that covers its completion
  requirements.
- Do not use tests or green checks as evidence unless they test the actual
  requirement.
- Prefer small, low-complexity stages that narrow uncertainty.
- Convert blockers into work items: decompose them, route around them, or turn
  them into explicit source or proof obligations.
- Preserve the distinction between source discovery, taxonomy decision, API
  analysis, verification, and later implementation.
- Preserve earlier artifacts, but do not inherit their methodology.
- Keep discovery blind to T01–T45 and the proposed API until Stage 10.
- Record heading-level coverage, not paragraph-level negative dispositions.
- Register raw leads cheaply. Spend full-analysis effort only on serious
  candidates and close decisions.
- Do not inspect an image without a taxonomy-bearing reason.
- Do not create replay systems, append-only histories, accepted-output programs,
  generalized validators, duplicate bundles, or redundant search reruns.
- Do not retain raw search dumps when a compact query-and-decision record is
  sufficient.
- Do not ask multiple agents to reread the same source. Delegation must be
  bounded and non-overlapping, except for the single independent hostile review.
- Do not load a large register wholesale when a field projection or bounded
  batch answers the question.
- Watch artifact size. Unexpected bulk is a correctness problem, not harmless
  bookkeeping.
- Do not modify the Book, catalog, API, runtime, tests, or prior goals without
  separate user authorization.

## Lightweight Verification Pattern

Use the smallest checks that prove the stage:

- source-anchor existence and excerpt spot checks;
- heading coverage against the assigned Markdown documents;
- uniqueness and referential-integrity checks for compact CSV registers;
- candidate and T01–T45 cardinality checks where applicable;
- targeted search commands whose summarized results are recorded once;
- direct inspection of only relevant original-resolution figures;
- `git diff --check`;
- `git status --short`;
- `du -sh goal-5` and a largest-file check.

Do not run a full repository test suite for documentation-only taxonomy changes
unless the stage changes executable code or a concrete repository dependency
requires it.

## Stage File Template

```markdown
# [INDEX]-[SHORTHAND]

## Current Facts

- Facts from current source, compact Goal 5 artifacts, and previous stage
  results.

## Updated Assumptions

- Assumptions that still look valid.
- Assumptions that changed.
- Assumptions that need source checks before being trusted.

## Big Picture Objective

- Restate the stage objective, adjusted for current facts.

## Detailed Implementation Plan

- Concrete research, document, and verification changes for this stage.
- Files expected to change.
- Source ranges, figures, or compact registers required.
- Checks required.

## No-Cheating Checks

- Prove discovery remained blind when required.
- Prove large predecessor or generated artifacts were not used as context.
- Prove no exhaustive negative ledger or redundant verification machinery was
  created.
- Prove retained claims resolve to canonical source.

## Completion Requirements

- Requirement-by-requirement evidence.
- Required source, structural, and diff checks.
- Documentation updates required.

## Stage Results

- Fill in at the end of the stage.
- Include checks run and outcomes.
- Include what was learned.
- Include artifact-size impact.
- Include what should change in `0-plan.md` before the next stage.
```

## Stop Conditions

Stop a stage and record the next concrete work rather than improvising when:

- canonical source evidence is missing or contradictory;
- a serious candidate cannot yet be distinguished from a neighboring family;
- a source cross-reference requires a later unread chapter;
- a proposed API gap lacks a concrete counterexample;
- a compact data transformation cannot be verified without importing forbidden
  predecessor context; or
- the working artifacts begin growing into infrastructure rather than answers.

An apparent blocker is not a reason to abandon the original objective. It
becomes an explicit source check, experiment, counterexample, or later-stage
dependency.

