# 2-BASELINE

Status: IN_PROGRESS

Dependencies:

- Stage 1 guardrails and compatibility baseline: COMPLETE.

## Current Facts

- Stage sync date is 2026-07-14 in `America/Los_Angeles`.
- The immutable legacy root is `ref/A-New-Kind-of-Science/`; the repaired sibling `ref/A-New-Kind-of-Science-Repaired/` is absent and excluded from every raw-input discovery rule.
- The Stage 1 census records exactly 1,463 regular legacy files: 19 Markdown inputs and 1,444 JPEG assets, with zero symlinks.
- The frozen legacy Git tree is `52b84494ab310afd64762bf0983106414419655e`; the Stage 1 content fingerprint is `6da649210cbdb601caddae6e7fb230404565efb224cb0741dd595343f3a6632d`.
- The source monolith is provisionally expected to contain 22,498 logical lines and 29 canonical author-text segments. Both facts must be independently re-derived rather than copied into the baseline.
- Current split files and the monolith are routing derivatives of one OCR lineage, not independent textual witnesses.
- Stage 1 froze the 29 canonical output paths, ID/serialization rules, held-out sampling algorithm, evidence policy, and compatibility closure. Stage 2 must consume those contracts without changing them merely to make the census pass.
- Goal 1, Goal 2, Goal 3, the legacy corpus, and unrelated repository work remain outside this stage's write scope.

## Updated Assumptions

- Git object identity, filesystem metadata, decoded text facts, and image dimensions can be independently recomputed from the explicit frozen allowlist.
- The 29 provisional segment ranges can be replaced by immutable segment IDs and exact boundary signatures with gap-free, overlap-free coverage.
- A stable raw-block universe can be derived before any author-text correction and can therefore materialize the held-out sample without outcome leakage.
- Known defects can be frozen as detection/routing sentinels without asserting a correction or treating correlated OCR as source evidence.
- The three omitted split-reference ordinals, Atlas routing anomaly, broken monolith links, and split/monolith divergences need explicit baseline rows rather than prose-only notes.

## Big Picture Objective

Create an independently reproducible, immutable census of every governed raw input, every proposed canonical segment and raw block, every known structural/OCR risk, and every pre-repair quality sample member—without creating or modifying repaired author text.

## Detailed Implementation Plan

- Create a deterministic raw manifest from the Stage 1 explicit allowlist, recording path, role, mode/type, logical and allocated bytes, line/encoding facts, SHA-256, Git blob identity, basename, and JPEG dimensions where applicable.
- Derive a monolith line map and all 29 canonical segment records from exact start/end signatures; assign immutable segment and raw-block IDs and prove that every one of the independently counted logical lines belongs to exactly one segment.
- Inventory all 17 split routing derivatives, Atlas, the three omitted reference ordinals, broken links, consumer-sensitive paths, and every observed split/image anomaly.
- Freeze `known-defect-regression.jsonl` with exact raw sentinels, expected detection classes, routes, and immutable source hashes, without proposing repairs.
- Materialize the Stage 1 predeclared held-out sample IDs from the raw-block universe and record selection inputs, seed/ranks, strata, quotas, and membership independently of later changed/unchanged outcomes.
- Run baseline-only candidate detectors and record every hit and route. Detectors may identify review candidates but may not rewrite author text or manufacture source evidence.
- Record tool/environment versions and the exact pre-stage repository scope needed for deterministic reproduction.
- Add independent validators and mutation tests for count/path/hash/metadata drift, line gaps/overlaps, signature ambiguity, stale Git objects, altered raw inputs, sample-selection drift, omitted known sentinels, and accidental inclusion of the repaired sibling.

Expected Stage 2 writes are restricted to `goal-4/**`, including baseline ledgers, schemas, tools, tests, and this report. No file under either edition root is an input-side write target in this stage.

## No-Cheating Checks

- Discover inputs only from the exact Stage 1 allowlist; never recurse over `ref/` or a parent that could admit the repaired sibling.
- Independently hash the legacy tree before and after the stage and require the frozen Git tree/content fingerprints to remain unchanged.
- Reject missing, extra, renamed, symlinked, non-regular, mode-drifted, byte-drifted, dimension-drifted, or Git-identity-drifted allowlist entries.
- Derive segment boundaries from raw bytes and exact signatures; reject copied line-number assertions that do not reproduce, ambiguous signatures, gaps, overlaps, reordered segments, or uncovered logical lines.
- Treat split Markdown only as routing evidence. Never use agreement between split and monolith text to authorize an OCR correction.
- Freeze raw blocks, known-defect rows, and held-out sample membership before any repair overlay exists; reject outcome-aware resampling.
- Keep every detector output diagnostic. It may route a candidate but may not change canonical text or claim witness verification.
- Prove that mutating any governed raw input, adding a temporary repaired sibling file, or contaminating the legacy fixture causes the appropriate baseline/compatibility verifier to fail.
- Do not create `ref/A-New-Kind-of-Science-Repaired/` during Stage 2.

## Completion Requirements

- The manifest accounts for exactly 19 Markdown files and 1,444 JPEGs, or records and guardrail-resyncs a source-evidenced count change before proceeding.
- Every allowlisted input has reproducible byte, filesystem, decoded-text/image, and Git identity metadata under a versioned deterministic schema.
- The monolith hash and logical line count are independently reproduced; exactly 29 ordered segment records cover all logical lines once with no gap or overlap.
- Every raw block has one stable ID and one segment owner, and mutation of a boundary/signature/order is rejected.
- All 17 split routing derivatives, Atlas, all known image-reference gaps, broken links, and known structural/OCR sentinels have enumerated baseline records and deterministic routes.
- `known-defect-regression.jsonl` and the held-out sample membership are frozen and hash-bound before correction; selection reproduces exactly from the raw block universe and Stage 1 contract.
- Baseline detector output is complete, non-mutating, and schema-valid; known-defect recall is measured without treating detector output as truth.
- The manifest explicitly excludes the repaired sibling and mutation of any governed raw input fails validation.
- Focused tests, full Stage 1 validation, optimized/relocated checks where applicable, direct whitespace checks, `git diff --check`, scope inspection, and an independent hostile review pass.
- Legacy bytes and Goal 1/2/3 inputs remain unchanged, and no repaired corpus content or repair record is produced.

## Stage Results

- In progress. No Stage 2 baseline artifact is final until the independent allowlist, structure, defect, sample, and mutation audits reconcile.
