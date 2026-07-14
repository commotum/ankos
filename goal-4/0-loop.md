# Goal 4 Execution Loop

Use this protocol for every stage in `goal-4/0-plan.md`. The purpose is to produce a source-faithful repaired edition while keeping the legacy corpus immutable and every change evidence-traceable.

## Phase Boundaries

### Foundations: Stages 1–7

Define the fidelity contract, freeze the explicit raw-input allowlist, census authoritative page witnesses, build the reversible pipeline, reconstruct the document tree, close asset handling, and validate the Markdown style.

Stages 4–7 may proceed while particular witness pages remain blocked. No witness-dependent batch may touch an uncovered region, but fully witnessed batches may proceed independently. The Stage 5/6 output is a zero-content-repair structural baseline; Stage 42 remains blocked until the complete witness/authorial-region gate passes.

### Sequential content repair: Stages 8–36

Repair bookends, every main chapter, every Notes section, and every part of the Index against authoritative page evidence.

Each batch reviews every assigned block in order. A batch is not complete merely because automated candidates were fixed.

### Specialist and closure passes: Stages 37–42

Audit technical notation, figures/captions, and navigation globally; reach residual-defect saturation; conduct hostile review; and publish a deterministic release.

## Repeatable Loop

1. Sync current state with actual files, hashes, ledgers, tests, witnesses, worktree scope, and prior stage results.
2. Update `goal-4/0-plan.md` with current facts before starting the next stage.
3. Select the lowest-numbered incomplete stage whose dependencies and assigned witness regions are satisfied, skipping explicitly blocked but dependency-independent work and keeping at most one stage `IN_PROGRESS`.
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
- Keep the explicit 19-Markdown/1,444-JPEG legacy allowlist under `ref/A-New-Kind-of-Science/` byte-for-byte unchanged; never rediscover raw inputs with a recursive glob that could include `ref/A-New-Kind-of-Science-Repaired/`.
- Never use repaired/generated output as input to the next build.
- Never apply a repair to a stale or non-unique preimage.
- Every canonical author-text output span must map to raw text or a source-verified anchored insertion, and every authoritative page region must map to canonical output, an enumerated/evidenced/independently reviewed non-authorial `NOT_APPLICABLE` reason, or a release blocker. Illegible or untranscribed authorial content is never `NOT_APPLICABLE`.
- Generated anchors, page markers, navigation, and alt text must be typed as editorial metadata.
- Canonical author text, derived aggregate, errata/editorial sidecars, and search normalization are distinct targets with class-enforced overlays.
- Never treat the current split and monolith as independent OCR witnesses.
- Never treat language plausibility, OCR confidence, spell-checking, parsing, rendering, code execution, or mathematical consistency as source proof.
- Never silently correct an apparent authorial error.
- Every author-text token/layout change requires per-occurrence authoritative witness evidence; `APPLIED_MECHANICALLY_PROVEN` is limited to non-author-text structure/path/generated metadata or byte-preserving transformations.
- Formula, code, rule-table, data, caption-association, and Index edits require authoritative evidence and machine-enforced independent review.
- Preserve every legacy image byte; never infer caption/group ownership from proximity or filenames alone, and do not call the visual edition complete while a witness-visible plate/component is missing.
- Any unresolved source-needed ambiguity affecting an authorial layer remains a release blocker unless the user explicitly changes the objective.
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

Record explicit dependencies in every stage file. At most one stage is `IN_PROGRESS`. A blocked stage may be bypassed only by a stage whose dependency row in `0-plan.md` does not require the blocked material.

## Start-Of-Stage Sync

Before implementing a stage:

1. Read `0-plan.md`, `0-loop.md`, the current stage file if present, and all prior stage result summaries that constrain it.
2. Run `git status --short` and identify unrelated changes that must remain untouched.
3. Recompute the explicit governed raw allowlist hashes and compare them with `corpus-manifest.json`; confirm the sibling repaired folder is excluded.
4. Verify required witness page-region hashes, legibility, permissions, and audit-mount availability for the stage.
5. Validate every governed ledger and ensure there is no stale generated-output dependency.
6. Rebuild the latest accepted output from raw inputs plus overlays into a fresh directory.
7. Confirm stage prerequisites and outstanding blockers.
8. Update scaffold-time facts or assumptions that no longer match the filesystem.

If raw or witness hashes drift unexpectedly, stop content repair and diagnose the change. Do not “refresh” expected hashes merely to regain green checks.

## Repair Record Protocol

Every proposed repair gets a stable ID before application.

Required fields:

- repair ID and class;
- workflow state and owning closure stage;
- risk level;
- immutable raw file/hash;
- raw byte/block ID and logical lines;
- operation type;
- exact preimage and expected occurrence count, or stable two-sided anchors and expected adjacency for source-visible content absent from raw;
- proposed after-text or typed metadata;
- class-conditional evidence: authoritative witness edition/page-region/location/hash for author-text/layout, or independently reproducible proof for non-author-text mechanical/generated changes;
- explanation and confidence;
- author/editorial/source-erratum layer;
- creator and reviewer type/identity;
- dependencies and ordering;
- forward and inverse operation;
- before/witness/after render references when applicable;
- disposition and verification results.

Workflow states are `CAPTURED`, `EVIDENCE_READY`, `PENDING_SPECIALIST_REVIEW`, `PENDING_INDEPENDENT_REVIEW`, `SOURCE_BLOCKED`, and `CLOSED`. Final dispositions are assigned only when `CLOSED`.

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

1. Freeze the stage's unique raw-block assignments and nonoverlapping authoritative page-region list.
2. Open the raw block, split routing witnesses, primary page witness, and current repaired render together.
3. Compare every raw block and every witness region sequentially, not only detector hits; create an anchored insertion candidate for witness content wholly missing from raw.
4. Identify candidate defects in:
   - text and punctuation;
   - paragraph/list continuity and hyphenation;
   - headings and page furniture;
   - formulas, symbols, rule tables, and numeric data;
   - Wolfram Language and other code;
   - images, figure groups, and captions;
   - page/section/Notes/Index cross-references;
   - Markdown syntax and rendering.
5. Create repair records, pending specialist/reviewer routes, or explicit valid-text/source-needed dispositions.
6. Apply only source-authorized repairs through the overlay pipeline.
7. Generate and inspect before/witness/after views for changed blocks.
8. Add technical and figure items to their specialist ledgers.
9. Rebuild from raw, run focused verification, and reverse the overlay.
10. Review all changed blocks and the pre-frozen manifest-seeded changed/unchanged holdout.
11. Require an independently recorded witness decision for every high-risk edit by a reviewer ID different from the creator; unresolved disagreement blocks closure.
12. Close the batch matrix: every raw block, witness region, candidate, repair, unresolved item, figure group, and technical span is closed or has one governed pending state and owning later stage.

## Evidence Policy

### Mechanically provable changes

Examples include structural partitioning from independently verified boundaries, deterministic path rewriting, generated navigation metadata, or final-newline policy.

`APPLIED_MECHANICALLY_PROVEN` cannot change an author-text token or source-significant layout. Even a repeated spelling/dehyphenation change requires `APPLIED_WITNESS_VERIFIED` per occurrence.

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

Build mode applies frozen overlays without requiring network/live evidence. Audit mode mounts the authorized pinned witness and rechecks source content. A witness hash without readable authorized content is not evidence that a repair is correct.

### Formulas, code, rules, and data

Every changed token requires page evidence and independent review. Preserve exact operators, signs, digits, braces, pattern syntax, subscripts, superscripts, colors, seeds, state tables, and sequence values.

Parsing/rendering/execution can detect inconsistency but cannot authorize a replacement. If the printed source itself appears wrong, preserve it and use `SOURCE_ERRATUM_ANNOTATION`.

### Figures and captions

Use full page context. One printed figure may map to multiple cropped JPEGs. A JPEG may be only a caption or partial plate. Independently census every witness-visible printed figure/component; preserving 1,444 local assets alone does not prove visual completeness.

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
7. per-occurrence authoritative evidence for every author-text/layout change;
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

High-risk changes require creator ID ≠ reviewer ID, an evidence-view hash, and preferably a blind witness transcription/association decision recorded before the proposed repair is shown. Validators reject self-review and unresolved disagreements.

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
- every monolith author-text block maps exactly once into `CANONICAL_AUTHOR_TEXT`;
- every authoritative authorial page region maps to canonical output or a release blocker, and every `NOT_APPLICABLE` region is demonstrably non-authorial;
- every canonical author-text span maps to raw content or witness-backed insertion evidence;
- all exclusions are typed and justified;
- output author text contains no unlogged change;
- repair order is deterministic;
- generated metadata is distinguishable and removable;
- the derived aggregate duplicates canonical content only as an explicitly excluded serialized view;
- errata/editorial/search overlays cannot enter canonical author text;
- inverse replay recovers raw block hashes/order;
- old raw locations map to stable repaired anchors;
- output never becomes the next input.

The conservation verifier must be independently implemented from the builder's own bookkeeping or cross-checked through a second derivation.

## Asset Checks

For all 1,444 legacy JPEGs:

- distinct asset ID;
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

Separately census final witness-visible printed figure groups/components and source-verified canonical replacements. Identical hashes do not authorize deduplicating distinct asset IDs. Canonical-fragment and derived-aggregate reference counts are validated separately.

Required negative tests include:

- delete an asset;
- alter bytes;
- duplicate a basename;
- swap two same-page references;
- reorder component images;
- attach a caption to the wrong group;
- omit one of the three known split-reference gaps;
- silently recompress/copy with hash drift.
- omit a witness-only/missing plate;
- double-count references by mixing canonical and aggregate views;
- add repaired Markdown or a duplicate-basename image beneath a temporary legacy root without compatibility detection.

## Focused Verification By Stage Kind

### Guardrails, baseline, and witnesses

- Confirm architecture/scope against actual consumers.
- Independently hash the explicit inputs and witnesses.
- Verify the complete witness-derived leaf/page/plate and authorial-region census, its documented reconciliation to the 1,280-page clue, legibility, licensing/provenance, and build/audit modes.
- Test missing/tampered input and witness failures.

### Pipeline, structure, media, and style

- Build zero-repair output twice.
- Prove 29 canonical-segment coverage, separate aggregate counts, two-way provenance, and inverse reconstruction.
- Verify all legacy assets/reference ordinals, ownership totals, and structural signatures.
- Run parser/render fixtures and all core mutations.

### Main-text and Notes batches

- Verify total raw-block and nonoverlapping witness-region coverage.
- Inspect every closed repair/final disposition and governed pending specialist/reviewer route.
- Run changed-block and the pre-frozen unchanged/changed holdout.
- Run technical, figure, provenance, inverse, render, and link checks.

### Index batches

- Verify every authoritative page/column and raw fragment.
- Check entry hierarchy, ordering, page-reference parsing, cross-references, and count reconciliation.
- Mutation-test omitted/merged/reordered entries and column swaps.

### Specialist and navigation stages

- Reconcile all technical spans, figure groups, assets, captions, links, anchors, page routes, and compatibility mappings.
- Require token-level/visual review and relevant mutations.

### Saturation, hostile review, and release

- Rerun all detectors to two consecutive full no-new-class rounds and prove recall on known sentinels/mutations.
- Review the pre-frozen blind-adjudicated sample and class-specific thresholds.
- Run every mutation and full offline/relocated build.
- Compare two fresh releases byte-for-byte.
- Verify raw scope and final claims.

## Stage File Template

```markdown
# [INDEX]-[SHORTHAND]

Status: NOT_STARTED

Dependencies:

- Stage IDs, witness regions, reviews, or other prerequisites.

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
2. Verify the complete physical-page/plate/region witness census, identity, legibility, permissions, and hashes.
3. Validate every ledger schema, unique ID, join, status, and digest.
4. Prove all 22,498 monolith logical lines/raw blocks map exactly once into 29 canonical documents, and every witness authorial region maps back from canonical output.
5. Verify exactly 29 ordered `CANONICAL_AUTHOR_TEXT` documents and separate expected counts for `DERIVED_AGGREGATE` and metadata/sidecar targets.
6. Verify every repair operation/preimage or insertion anchor, class-conditional evidence, inverse, workflow closure, independent review, and final disposition.
7. Require zero unresolved source-needed item affecting any authorial layer and zero unresolved review disagreement.
8. Verify all 1,444 legacy asset IDs/hashes/baseline reference ordinals, the three restored omissions, and the final witness-complete printed-figure/component inventory.
9. Parse and render all Markdown; check headings, fences, HTML, math delimiters, code blocks, figures, and Index structure.
10. Verify all links, unique anchors, page routes, Notes routes, Index routes, navigation reachability, and legacy compatibility mappings.
11. Run every mutation and known-defect-regression fixture and inspect that it fails/routes for the intended reason.
12. Build twice from raw in clean fresh directories and compare outputs byte-for-byte.
13. Run offline, relocated, and optimized-mode checks where applicable.
14. Reverse all repair overlays and recover raw block hashes/order.
15. Run direct trailing-whitespace and fence checks over tracked and untracked Goal 4 and sibling repaired files.
16. Run `git diff --check` and inspect `git status --short` for scope.
17. Confirm legacy raw, Goal 1, Goal 2, Goal 3, runtime, and unrelated references are unchanged, and affected Goal 1 oracle output digests match the pre-release baseline.
18. Run audit mode against the authorized witness mount and pass the pre-frozen class-specific quality thresholds.
19. Reconcile operational illustration/Notes/program/Index counts with 973/1,350/796/14,967 and explain differences.
20. Read the final report's claims against actual unresolved/review/witness-region ledgers.

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
