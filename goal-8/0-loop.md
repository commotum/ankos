# Goal 8 Execution Loop

Use this loop to execute [`0-plan.md`](0-plan.md). The purpose of the loop is
resumability, not ceremony.

## Repeatable Loop

1. Sync current state with actual files and tests.
2. Update `0-plan.md` with current facts before starting the next stage.
3. Select the first incomplete stage.
4. Create or refresh `goal-8/[INDEX]-[SHORTHAND].md` from the stage template.
5. Implement only that stage.
6. Add verification and no-cheating checks.
7. Run focused tests, full verification, and whitespace/diff checks appropriate
   to the repo.
8. Record results in the stage file.
9. Fold results back into `0-plan.md`.
10. Continue toward the original objective. If stopping for the session, leave
    the goal in a resumable state with current evidence, next experiments,
    unblock actions, and assumptions to challenge.

Keep stage records short. Do not duplicate `spaces.csv` or `findings.md` in a
stage file.

## Per-Family Work

For each `ref/types.csv` row in the stage's `book_index` range:

1. Read the row and its starting source references.
2. Use Goal 5's family/candidate records to locate relevant variants and Book
   passages.
3. Read the actual Book passages and any cross-reference that can change the
   Space answer.
4. Answer the five questions in `0-plan.md`.
5. Add or revise the family's `spaces.csv` rows immediately.
6. Put only substantial proofs, ambiguity, or cross-family reasoning in
   `findings.md`.

Move to the next family when the per-family completion test passes. Do not
inventory irrelevant historical leads.

## Invariants

- Do not narrow the user's objective without saying so.
- Do not mark a stage complete without evidence.
- Do not use tests or green checks as evidence unless they cover the
  requirement.
- Prefer small, low-complexity work that narrows uncertainty.
- Convert blockers into targeted searches, proofs, counterexamples, or honest
  bounded unknowns.
- Preserve the distinction between implementation, verifier, diagnostic, and
  fallback paths.
- Time is explicit in every admitted Space.
- Book evidence and written proofs decide claims; metadata and code do not.
- Encodings and observers do not become native Space by convenience.
- Do not add ledgers, scripts, reports, or stage ceremonies unless they remove
  a demonstrated obstacle to finishing the 60-family answer.
- Keep `ref/types.csv`, prior goals, runtime code, tests, and the Book corpus
  unchanged.

## Verification

During family stages, verify citations and inspect completed rows. At the end,
run only checks relevant to this documentation/research scope:

- parse `spaces.csv`;
- compare its family set with `ref/types.csv`;
- check unique claim keys and allowed values;
- confirm cited paths exist;
- inspect supported claims for evidence or proofs;
- run `git diff --check`; and
- inspect the final changed-file set.

Do not create a permanent verifier unless repeated manual checking becomes a
real source of errors.

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

- Explicit checks proving the implementation does not route through forbidden fallback paths.

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

## If Work Stops

Record the last completed `book_index`, incomplete family IDs, exact unresolved
questions, and next source or proof to inspect. Do not replace unfinished
analysis with a new planning stage.
