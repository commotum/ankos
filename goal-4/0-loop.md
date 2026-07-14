# Goal 4 Execution Loop

Use this protocol for every stage in `goal-4/0-plan.md`. The purpose is to produce a source-faithful repaired edition while keeping the legacy corpus immutable and every change evidence-traceable.

## Phase Boundaries

### Foundations: Stages 1–7

Define the fidelity contract, freeze raw inputs, secure authoritative page witnesses, build the reversible pipeline, reconstruct the document tree, close asset handling, and establish the Markdown style.

No witness-dependent author-text repair begins before Stages 1–7 pass. The Stage 5/6 output is a zero-content-repair structural baseline.

### Sequential content repair: Stages 8–36

Repair bookends, every main chapter, every Notes section, and every part of the Index against authoritative page evidence.

Each batch reviews every assigned block in order. A batch is not complete merely because automated candidates were fixed.

### Specialist and closure passes: Stages 37–42

Audit technical notation, figures/captions, and navigation globally; reach residual-defect saturation; conduct hostile review; and publish a deterministic release.

## Repeatable Loop

1. Sync current state with actual files, hashes, ledgers, tests, witnesses, worktree scope, and prior stage results.
2. Update `goal-4/0-plan.md` with current facts before starting the next stage.
3. Select the first incomplete stage whose prerequisites are satisfied.
4. Create or refresh `goal-4/[INDEX]-[SHORTHAND].md` from the stage template below.
5. Implement only that stage, starting every build from frozen raw inputs rather than prior generated output.
6. Add verification, provenance, inverse, visual-review, and no-cheating checks proportional to the stage's risks.
7. Run focused tests, full applicable verification, mutation tests, render checks, and whitespace/diff/scope checks.
8. Record commands, results, evidence, repairs, unresolved items, review state, and failures in the stage file and governed ledgers.
9. Fold observed facts, changed assumptions, stage status, and newly required work back into `0-plan.md`.
10. Continue toward the original full-repair objective. If stopping for the session, leave exact current evidence, hashes, open repairs, source needs, next experiments, unblock actions, and assumptions to challenge.

## Global Invariants

- Do not narrow “full repair” to “correct file cuts,” “clean Markdown,” “passes lint,” or another easier subset without explicit user agreement.
- Do not mark a stage complete without requirement-by-requirement evidence.
- Do not use tests or green checks as evidence for properties they do not cover.
- Prefer small, low-complexity changes that narrow uncertainty and remain independently reviewable.
- Convert blockers into concrete work: alternate authoritative witnesses, narrower diagnostics, proof obligations, review queues, or acquisition steps.
- Preserve the distinction between immutable input, repair overlay, derived author text, source errata annotation, search normalization, generated metadata, verifier, diagnostic, and fallback path.
- Keep all legacy `ref/A-New-Kind-of-Science/**` inputs byte-for-byte unchanged throughout Goal 4.
- Never use repaired/generated output as input to the next build.
- Never apply a repair to a stale or non-unique preimage.
- Every author-text output block must map to a raw block plus zero or more explicit repairs.
- Generated anchors, page markers, navigation, and alt text must be typed as editorial metadata.
- Never treat the current split and monolith as independent OCR witnesses.
- Never treat language plausibility, OCR confidence, spell-checking, parsing, rendering, code execution, or mathematical consistency as source proof.
- Never silently correct an apparent authorial error.
- Formula, code, rule-table, data, caption-association, and Index edits require authoritative evidence and independent review.
- Preserve every raw image byte; never infer caption/group ownership from proximity or filenames alone.
- An unresolved high-risk ambiguity remains a release blocker unless the user explicitly changes the objective.
- Do not claim human review when the review was automated or agent-only.
- Do not migrate existing Goal 1/3 paths, hashes, or line citations during Goal 4.
- Preserve unrelated dirty work and inspect scope before and after every stage.

## Stage Status Model

Use one of these states in `0-plan.md` and the stage file:

- `NOT_STARTED`
- `IN_PROGRESS`
- `SOURCE_BLOCKED`
- `REVIEW_BLOCKED`
- `COMPLETE`

`SOURCE_BLOCKED` and `REVIEW_BLOCKED` are evidence-bearing states, not completion. Record the exact missing witness/review, affected blocks, impact, attempted alternatives, and unblock action.

## Start-Of-Stage Sync

Before implementing a stage:

1. Read `0-plan.md`, `0-loop.md`, the current stage file if present, and all prior stage result summaries that constrain it.
2. Run `git status --short` and identify unrelated changes that must remain untouched.
3. Recompute governed raw hashes and compare them with `corpus-manifest.json`.
4. Verify required witness pages/hashes and permissions for the stage.
5. Validate every governed ledger and ensure there is no stale generated-output dependency.
6. Rebuild the latest accepted output from raw inputs plus overlays into a fresh directory.
7. Confirm stage prerequisites and outstanding blockers.
8. Update scaffold-time facts or assumptions that no longer match the filesystem.

If raw or witness hashes drift unexpectedly, stop content repair and diagnose the change. Do not “refresh” expected hashes merely to regain green checks.

## Repair Record Protocol

Every proposed repair gets a stable ID before application.

Required fields:

- repair ID and class;
- risk level;
- immutable raw file/hash;
- raw byte/block ID and logical lines;
- exact preimage and expected occurrence count;
- proposed after-text or typed metadata;
- authoritative witness edition/page/location/hash;
- explanation and confidence;
- author/editorial/source-erratum layer;
- creator and reviewer type/identity;
- dependencies and ordering;
- forward and inverse operation;
- before/witness/after render references when applicable;
- disposition and verification results.

Allowed final dispositions:

- `APPLIED_MECHANICALLY_PROVEN`
- `APPLIED_WITNESS_VERIFIED`
- `ANNOTATED_SOURCE_ERRATUM`
- `REJECTED_VALID_SOURCE_TEXT`
- `DUPLICATE_CANDIDATE`
- `UNRESOLVED_SOURCE_NEEDED`

A record is not “verified” merely because its patch applies. It must also satisfy evidence, rendering, provenance, inverse, review, and mutation requirements appropriate to its risk.

## Sequential Batch Review Procedure

Use this procedure for Stages 8–36:

1. Freeze the stage's raw block list and authoritative page list.
2. Open the raw block, split routing witnesses, primary page witness, and current repaired render together.
3. Compare the entire block sequentially, not only detector hits.
4. Identify candidate defects in:
   - text and punctuation;
   - paragraph/list continuity and hyphenation;
   - headings and page furniture;
   - formulas, symbols, rule tables, and numeric data;
   - Wolfram Language and other code;
   - images, figure groups, and captions;
   - page/section/Notes/Index cross-references;
   - Markdown syntax and rendering.
5. Create repair records or explicit valid-text/source-needed dispositions.
6. Apply only source-authorized repairs through the overlay pipeline.
7. Generate and inspect before/witness/after views for changed blocks.
8. Add technical and figure items to their specialist ledgers.
9. Rebuild from raw, run focused verification, and reverse the overlay.
10. Review all changed blocks and a stratified unchanged sample.
11. Require independent review for every high-risk edit.
12. Close the batch matrix: every raw block, witness page, candidate, repair, unresolved item, figure group, and technical span has one governed status.

## Evidence Policy

### Mechanically provable changes

Examples include structural partitioning from independently verified boundaries, deterministic path rewriting, generated navigation metadata, or final-newline policy.

They still require:

- frozen raw hash;
- exact scope and expected counts;
- author-text conservation;
- inverse;
- independent validator;
- mutation test.

### Prose OCR and layout

Corrections require an edition-identical primary witness. Candidate detectors may find:

- word splits across blank lines/images/fences;
- suspicious joins or hyphens;
- OCR confusions;
- page furniture;
- broken list/paragraph continuity;
- malformed headings;
- punctuation/case anomalies.

Do not globally repair a token because it looks wrong. Proper names, compounds, historical spelling, and intentional typography require witness review.

### Formulas, code, rules, and data

Every changed token requires page evidence and independent review. Preserve exact operators, signs, digits, braces, pattern syntax, subscripts, superscripts, colors, seeds, state tables, and sequence values.

Parsing/rendering/execution can detect inconsistency but cannot authorize a replacement. If the printed source itself appears wrong, preserve it and use `SOURCE_ERRATUM_ANNOTATION`.

### Figures and captions

Use full page context. One printed figure may map to multiple cropped JPEGs. A JPEG may be only a caption or partial plate.

Track:

- printed page and figure identity;
- ordered component images;
- byte hash/dimensions;
- caption raw span;
- ownership evidence;
- crop/missing-plate status;
- author caption versus generated alt text.

### Index

Read authoritative page columns in print order. Do not use flattened OCR order or body search to reconstruct authorial entries.

Track entries, subentries, page ranges, personal names, symbols, `see`/`see also` relations, column/page source, and raw fragment mappings. Entry-count reconciliation is a check, not a substitute for page review.

## Safe Automation Protocol

Automation is permitted for:

- strict UTF-8/hash/count validation;
- raw-block segmentation and no-gap/no-overlap checks;
- unique image-basename/hash joins;
- deterministic link/path rewriting;
- exact guarded repair application;
- parser/render/link diagnostics;
- candidate detection;
- ledger/schema/coverage validation;
- reproducible build and inverse replay.

A candidate-generating detector must never write author text directly.

An automated repair rule requires:

1. a named rule and repair class;
2. frozen input hash;
3. bounded contexts;
4. exact expected match count;
5. complete hit inventory;
6. false-positive review;
7. authoritative evidence where author text changes;
8. forward and inverse operations;
9. mutation fixtures;
10. post-build visual/AST review.

Formula/code/data/Index/caption-association changes may not be authorized solely by an automated rule.

## Review Protocol

For each stage, distinguish:

- automated validation;
- agent visual/source review;
- independent agent review;
- human review.

High-risk changes require a reviewer independent of the change author. Disagreements remain open until resolved against evidence.

The review ledger must include:

- block/repair ID;
- reviewer identity/type;
- evidence viewed;
- decision;
- disagreement;
- follow-up;
- closure.

Do not record a blanket “reviewed” flag without enumerated coverage.

## Provenance And Conservation Checks

Every build must prove:

- all raw inputs match frozen hashes;
- every raw author-text block maps exactly once;
- all exclusions are typed and justified;
- output author text contains no unlogged change;
- repair order is deterministic;
- generated metadata is distinguishable and removable;
- inverse replay recovers raw block hashes/order;
- old raw locations map to stable repaired anchors;
- output never becomes the next input.

The conservation verifier must be independently implemented from the builder's own bookkeeping or cross-checked through a second derivation.

## Asset Checks

For all 1,444 JPEGs:

- basename;
- current raw path;
- byte size;
- dimensions;
- SHA-256;
- raw reference ordinal;
- repaired reference;
- author-text document owner;
- printed page/figure group;
- caption association;
- crop/completeness status;
- accessibility metadata status.

Required negative tests include:

- delete an asset;
- alter bytes;
- duplicate a basename;
- swap two same-page references;
- reorder component images;
- attach a caption to the wrong group;
- omit one of the three known split-reference gaps;
- silently recompress/copy with hash drift.

## Focused Verification By Stage Kind

### Guardrails, baseline, and witnesses

- Confirm architecture/scope against actual consumers.
- Independently hash inputs and witnesses.
- Verify edition/page coverage and licensing/provenance records.
- Test missing/tampered input and witness failures.

### Pipeline, structure, media, and style

- Build zero-repair output twice.
- Prove 29-segment coverage and inverse reconstruction.
- Verify all assets/references and structural ownership.
- Run parser/render fixtures and all core mutations.

### Main-text and Notes batches

- Verify total raw-block and witness-page coverage.
- Inspect every repair and unresolved disposition.
- Run changed-block and unchanged-sample reviews.
- Run technical, figure, provenance, inverse, render, and link checks.

### Index batches

- Verify every authoritative page/column and raw fragment.
- Check entry hierarchy, ordering, page-reference parsing, cross-references, and count reconciliation.
- Mutation-test omitted/merged/reordered entries and column swaps.

### Specialist and navigation stages

- Reconcile all technical spans, figure groups, assets, captions, links, anchors, page routes, and compatibility mappings.
- Require token-level/visual review and relevant mutations.

### Saturation, hostile review, and release

- Rerun all detectors to a documented fixed point.
- Review stratified changed/unchanged samples.
- Run every mutation and full offline/relocated build.
- Compare two fresh releases byte-for-byte.
- Verify raw scope and final claims.

## Stage File Template

```markdown
# [INDEX]-[SHORTHAND]

## Current Facts

- Facts from current code, tests, docs, witnesses, ledgers, and previous stage results.

## Updated Assumptions

- Assumptions that still look valid.
- Assumptions that changed.
- Assumptions that need tests before being trusted.

## Big Picture Objective

- Restate the stage objective, adjusted for current facts.

## Detailed Implementation Plan

- Concrete code/doc/test/ledger/review changes for this stage.
- Files expected to change.
- New tests, witness checks, review artifacts, or commands required.

## No-Cheating Checks

- Explicit checks proving immutable raw inputs remain unchanged.
- Checks proving repairs use authoritative evidence rather than plausibility or correlated OCR.
- Checks proving generated output is not reused as input.
- Checks proving high-risk review and inverse coverage.

## Completion Requirements

- Requirement-by-requirement checks.
- Required test/build/render/review commands.
- Documentation and ledger updates required.

## Stage Results

- Fill in at the end of the stage.
- Include tests, builds, mutations, renders, and review outcomes.
- Include repair/unresolved counts and governed hashes.
- Include what was learned.
- Include what should change in 0-plan.md before the next stage.
```

## Final Verification

Before Stage 42 may complete:

1. Recompute all legacy raw hashes and compare with the frozen manifest.
2. Verify authoritative witness coverage, identity, and hashes for every reviewed page.
3. Validate every ledger schema, unique ID, join, status, and digest.
4. Prove all 22,498 raw logical lines and every raw block map exactly once.
5. Verify exactly 29 ordered repaired author-text documents.
6. Verify every repair preimage, evidence, inverse, review, and disposition.
7. Require zero unqualified high-risk unresolved item.
8. Verify all 1,444 asset hashes and repaired references, including the three restored omissions.
9. Parse and render all Markdown; check headings, fences, HTML, math delimiters, code blocks, figures, and Index structure.
10. Verify all links, unique anchors, page routes, Notes routes, Index routes, navigation reachability, and legacy compatibility mappings.
11. Run every mutation fixture and inspect that it fails for the intended reason.
12. Build twice from raw in clean fresh directories and compare outputs byte-for-byte.
13. Run offline, relocated, and optimized-mode checks where applicable.
14. Reverse all repair overlays and recover raw block hashes/order.
15. Run direct trailing-whitespace and fence checks over tracked and untracked Goal 4/repaired files.
16. Run `git diff --check` and inspect `git status --short` for scope.
17. Confirm legacy raw, Goal 1, Goal 2, Goal 3, runtime, and unrelated references are unchanged.
18. Read the final report's claims against actual unresolved/review ledgers.

## Session Stop / Resume Contract

When stopping before Goal 4 is complete, leave:

- the active stage and precise status;
- current raw, witness, overlay, tool, ledger, and output hashes;
- last successful clean build and verification commands;
- exact open repair/unresolved/review queues;
- failed commands and preserved output;
- next smallest action;
- required source acquisition or reviewer action;
- assumptions to challenge;
- confirmation that legacy raw inputs remain unchanged.

Do not stop with unrecorded local decisions, a generated tree that cannot be reproduced, or repairs applied outside the governed overlay.
