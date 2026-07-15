# Goal 5 Execution Loop

Use this loop to execute `goal-5/0-plan.md`. The objective is full-book OCR
correction with complete source comparison, implemented with the smallest
workflow that can support that claim.

## Repeatable Loop

1. Sync current state with the actual files, source availability, coverage
   records, corrections, tests, and `git status`.
2. Update `goal-5/0-plan.md` with current facts before starting the next stage.
3. Select the first incomplete stage whose prerequisites are ready.
4. Create or refresh `goal-5/[INDEX]-[SHORTHAND].md` from the template below.
5. Implement only that stage.
6. Add verification and no-cheating checks tied to its completion requirements.
7. Run focused tests, cumulative validation, affected repository tests where
   appropriate, and whitespace/diff checks.
8. Record exact review coverage, corrections, commands, results, and remaining
   issues in the stage file.
9. Fold durable findings, new defect patterns, and changed assumptions back into
   `0-plan.md`.
10. Continue toward the original objective. If stopping, leave the goal
    resumable with current evidence, next source range, open discrepancies,
    unblock actions, and assumptions to challenge.

## Global Invariants

- Do not narrow “reliable Markdown source without OCR errors” into structural
  cleanup, best effort, sampling, or a corpus with accepted known ambiguities.
- Do not mark a stage complete without evidence for every completion
  requirement.
- Do not treat tests, parsing, rendering, execution, or model confidence as
  transcription proof unless an authoritative source establishes the text.
- Prefer small, low-complexity stages that correct concrete book content.
- Convert blockers into explicit source-acquisition, legibility, comparison, or
  verification work; do not hide them behind process artifacts.
- Preserve the distinction between raw input, authoritative source, correction,
  generated navigation, diagnostic, verifier, and source erratum.
- Keep `ref/A-New-Kind-of-Science/` byte-for-byte immutable.
- Protect unrelated worktree changes, especially during Goal 4 cleanup.
- Never use repaired output as the next build's source.
- Preserve literal author errors and notation when the source shows them.
- Do not claim human review for agent work.
- Do not recreate Goal 4's generalized schema, proof-lock, workflow-authority,
  review-identity, or hostile-race infrastructure.
- Add a record field, tool, abstraction, or test only when it directly protects
  a named Goal 5 acceptance criterion.

## Content Batch Procedure

Stages 3–8 use this procedure for every assigned source range:

1. Confirm the raw range, authoritative source range, and previous/next boundary.
2. Read forward sequentially; do not jump only among detector hits.
3. Compare headings, prose, punctuation, lists, formulas, code, tables,
   captions, images, page references, and reading order.
4. Record each correction with exact preimage, replacement, expected count, raw
   location, authoritative page/location, rationale, and reviewer type.
5. Apply corrections only through the guarded correction mechanism.
6. Run relevant OCR, Markdown, formula/code, image, and vocabulary detectors.
7. Check every detector hit against the authoritative source.
8. Render changed and structurally complex regions.
9. Perform a separate second sequential pass over the complete assigned range.
10. Close the batch only when coverage is complete and no discrepancy or
    ambiguity remains.

If a new OCR pattern is discovered, search already completed batches as well as
future batches and reopen any affected stage.

## Evidence Rules

- The authoritative source must be edition-identical, readable for the decision
  being made, and lawfully usable in the workflow.
- Raw/split agreement is routing evidence, not independent correction evidence.
- A dictionary, language model, parser, renderer, or executable result may flag
  a candidate but does not decide the transcription.
- Technical material is compared at the token or character level when prose
  reading can miss meaningful differences.
- Index order requires fixed-layout or equivalently authoritative column-order
  evidence.
- Unreadable source content stays open and blocks final completion; it is not
  guessed or waived.

## Verification By Stage Type

- Cleanup: diff inspection, keep/delete rationale, legacy hash, stale-reference
  scan, caches, and scope checks.
- Foundation: source identity/access, raw inventory, 29-range coverage,
  zero-correction conservation, image inventory, and build/validator tests.
- Content batches: complete two-pass range coverage, guarded corrections,
  detector dispositions, rendering, and cumulative validation.
- Technical: total technical-region inventory, token comparison, diagnostics,
  reopened batch closure, and zero ambiguity.
- Figures/Index: complete visual/caption disposition, fixed-layout Index review,
  Colophon boundary/content, and second pass.
- Saturation: full-corpus detector disposition, fresh 29-document pass, reopened
  corrections, and a final complete round with no new discrepancy.
- Release: two clean builds, all coverage joins, links/assets/rendering, legacy
  hashes, affected tests, diff/scope checks, and accurate documentation.

## Stage File Template

```markdown
# [INDEX]-[SHORTHAND]

Status: NOT_STARTED

## Current Facts

- Facts from current code, sources, coverage, corrections, tests, Git state,
  and previous stage results.

## Updated Assumptions

- Assumptions that still look valid.
- Assumptions that changed.
- Assumptions that need tests or source comparison before being trusted.

## Big Picture Objective

- Restate the stage objective, adjusted for current facts.

## Detailed Implementation Plan

- Exact source ranges and corpus files in scope.
- Concrete cleanup, build, correction, document, and test changes.
- Detectors, rendering, and first/second review passes required.

## No-Cheating Checks

- Prove review proceeds sequentially rather than only through detector hits.
- Prove corrections use authoritative source evidence and guarded preimages.
- Prove no repaired output becomes build input.
- Prove protected legacy and unrelated work remain unchanged.
- List stage-specific shortcuts that must fail.

## Completion Requirements

- Requirement-by-requirement evidence.
- First- and second-pass coverage totals where applicable.
- Correction and unresolved-item closure.
- Required build, validation, test, render, and diff/scope commands.

## Stage Results

- Fill in at the end of the stage.
- Record exact source ranges reviewed and reviewer type.
- List corrections and detector findings by stable ID or range.
- Record commands and outcomes.
- Record what was learned, reopened work, and remaining blockers.
- State what must change in `0-plan.md` before the next stage.
```

## Stop And Resume Contract

When stopping before completion:

- Leave at most one stage marked `IN_PROGRESS`.
- Record the exact current Git state and files intentionally changed.
- Record the last fully reviewed source location and the next range to compare.
- Record open discrepancies without guessing or downgrading them.
- Record the last passing/failing commands without overstating their coverage.
- Name the next concrete action and source needed to perform it.
- Do not call the repaired corpus complete until Stage 12 passes.

