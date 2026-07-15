# 2-BASELINE

Status: COMPLETE

Dependencies:

- Stage 1 guardrails and compatibility baseline: COMPLETE.

## Current Facts

- Stage sync date is 2026-07-14 in `America/Los_Angeles`.
- The immutable legacy root is `ref/A-New-Kind-of-Science/`; the repaired sibling `ref/A-New-Kind-of-Science-Repaired/` is absent and excluded from every raw-input discovery rule.
- The Stage 1 census records exactly 1,463 regular legacy files: 19 Markdown inputs and 1,444 JPEG assets, with zero symlinks.
- The frozen legacy Git tree is `52b84494ab310afd64762bf0983106414419655e`; the Stage 1 content fingerprint is `6da649210cbdb601caddae6e7fb230404565efb224cb0741dd595343f3a6632d`.
- The source monolith independently reproduces at SHA-256 `55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20`, 3,780,628 bytes, 22,498 logical lines, and 22,497 LF bytes with no terminal LF.
- Exactly 29 ordered proposed canonical segments cover every monolith line and byte once. Their 58 frozen five-line boundary signatures are globally unique and resolve back to the expected focal lines. Their status remains `PROPOSED_RAW_BOUNDARY_PENDING_STAGE_3_5_WITNESS_VALIDATION`; Stage 2 does not falsely claim page-witness authority.
- Current split files and the monolith are routing derivatives of one OCR lineage, not independent textual witnesses.
- Stage 1 froze the 29 canonical output paths, ID/serialization rules, held-out sampling algorithm, evidence policy, and compatibility closure. Stage 2 must consume those contracts without changing them merely to make the census pass.
- Goal 1, Goal 2, Goal 3, the legacy corpus, and unrelated repository work remain outside this stage's write scope.

## Updated Assumptions

- Git object identity, filesystem metadata, strict UTF-8/LF facts, LFS pointer joins, full Pillow JPEG decoding, and image dimensions were independently recomputed for all 1,463 inputs.
- The raw lexer emits 20,430 immutable blocks with exact line/byte coverage. All 45 pipe-table blocks are conservatively typed `DATA_TABLE` and routed to technical risk except where Index priority governs.
- The pre-repair held-out set is materialized as a Stage 2 sidecar bound to the frozen Stage 1 quality-protocol hash. The lock root binds both artifacts without reopening or rewriting the Stage 1 protocol.
- Known defects are frozen only as non-authorizing detection/routing sentinels. Exact presence/routing is 55/55; generic Stage 2 candidate coverage is deliberately reported as 31/55 with 24 manual exact routes. Reserved or limited detector families remain explicit Stage 37/38/40 obligations rather than being described as implemented.
- The three omitted split-reference ordinals, Atlas role, all broken monolith links, split/monolith routing spans, and Contents anomalies now have hash-bound rows rather than prose-only notes.

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

- COMPLETE on 2026-07-14.

### Frozen artifacts

- `corpus-manifest.json` accounts for exactly 1,463 regular inputs: 19 Markdown and 1,444 JPEG. It records 115,037,515 logical bytes, 44,989 Markdown logical lines, capture-only allocation/mode/link diagnostics, path digests, Git/LFS identities, strict text profiles, and independently decoded JPEG metadata. The manifest SHA-256 is `ba11d6ddf71aea5fb6e47be88ab54d47e33e1b8118273fa835c1b788c2321b76`.
- All 1,444 JPEG identities remain distinct even though one byte-identical payload occurs at three paths. All payloads decode completely; every HEAD image blob is a strict LFS pointer whose OID and size match the working payload.
- `structure-ledger.jsonl` contains 29 segment rows plus 20,430 raw-block rows. Block kinds are: boundary 9,843; prose 6,050; list 1,279; inline math 1,075; image 1,444; heading 286; code 254; math block 135; data table 45; caption 11; blockquote 8. Risk counts are Index 1,468; technical/data 1,474; visual 1,455; layout 10,681; prose 5,352.
- `image-reference-ledger.jsonl` joins all 1,444 monolith references to assets and 1,441 split references. The only split omissions are ordinals/lines 24/680, 134/1711, and 135/1744. Physical asset paths total Preface 2, chapters 899, back matter 543; semantic ownership totals Preface 2, chapters 820, Notes 622.
- `routing-baseline.json` freezes 17 routing files, 32 dispositions (31 raw projections plus generated Contents), 16 Contents links with four semantic anomalies, five non-navigation formula/code link shapes, seven omitted transition spans, Atlas as non-authoritative interpretive metadata, and every relevant span hash.
- `known-defect-regression.jsonl` freezes 52 exact raw spans and three aggregate guardrails. Every row has `repair_authorized: false`, exact regression detector `D13_EXACT_SENTINEL`, and explicit content/specialist/workflow/closure stages.
- `held-out-sample.json` freezes seed `edb7d55b015326755574afbf5513e2bacefe04fbdad875fb8901555edf8e5f0d`, all 20,430 rankings, and 1,125 selected IDs across all 29 documents. The selected-order digest is `94e489a0ad2ecc85da9554478b417c771f5eeb5d901561ccf56781292f2ac9ad`; selected strata are Index 74, technical/data 92, visual 92, layout 580, prose 287.
- `baseline-detector-hits.jsonl` contains 1,729 non-mutating hits. `baseline-detector-report.json` distinguishes fatal checks, implemented baseline candidate detectors, limited detectors, reserved later-stage detectors, and exact regression from discovery.
- `baseline-environment.json` records Git 2.43.0, Python 3.12.3, Pillow 10.2.0, source hashes, stable capture inputs, and sibling absence.
- `baseline-lock.json` binds nine artifacts, four source/test files including transitive `guardrail_lib.py`, Stage 1 contracts, and the legacy Git tree. Its externally pinned SHA-256 is `57224a1f1ba8333bbc900b23ff6127a189649feb01c279f30fac05a305658863`; the validator is deliberately outside the lock to avoid a circular self-hash.

### Verification and hostile review

- `validate_baseline.py` passed in normal and optimized Python with sibling absence required: `blocks=20430 defects=55 images=1444 sample=1125 segments=29`.
- All 27 Stage 2 unit/mutation tests passed normally in 67.644 seconds and under `python -O` in 66.670 seconds. They cover raw drift, JPEG truncation/trailing data, dangling aliases, line/byte and lexical reclassification, complete sample rankings, Hamilton ties and NUL framing, strict lock schemas and replacement attacks, routing/Atlas mutations, image swaps/omissions/ownership, defect/workflow/authorization drift, D13 deletion, filesystem mode/link changes, and Git/LFS OID/size/mode changes.
- Stage 1 validation and all 39 Stage 1 mutation tests passed again in normal and optimized modes.
- A no-Git portable copy with all files `0444`, directories `0555`, and deliberately changed monolith allocation passed with full lock checking. A second run passed with the legacy tree relocated through `--legacy-root`; the default legacy path was absent, proving the override was used.
- Three hostile audit tracks passed. They independently replayed all 58 boundary signatures, 20,430 block classifications/risks, 20,430 held-out ranking rows, all image/LFS/dimension joins, routing and sentinel mutations, and both ordinary and self-consistent lock replacement attacks.
- `git diff --check`, scope inspection, sibling absence, legacy Git tree `52b84494ab310afd64762bf0983106414419655e`, and legacy shell digest `b9ff7b9b507790f1d519593baf2b2d2f24dd6cd49dc0fe10f0ac629278ea42f4` passed. The legacy corpus, Goal 1/2/3, and the repaired sibling were not modified or created.

### Forward obligations

- Stage 3 must obtain and fingerprint edition-identical authoritative page evidence. Stage 5 must validate proposed raw segment boundaries against that witness before treating them as authoritative structure.
- Stage 37/38/40 must implement the detector families explicitly marked limited/reserved and satisfy the final recall/saturation protocol; Stage 2 exact sentinel routing is not a final content-fidelity claim.
