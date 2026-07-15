# 3-WITNESSES

Status: IN_PROGRESS

Dependencies:

- Stage 1 fidelity/evidence/licensing contracts: COMPLETE.
- Stage 2 raw manifest, proposed structure, held-out sample, and externally pinned baseline lock: COMPLETE.

## Current Facts

- Stage sync date is 2026-07-14 in `America/Los_Angeles`.
- Stage 2 independently froze all 1,463 legacy inputs, 29 proposed author-text segments, 20,430 raw blocks, 1,444 image references, 55 known-defect sentinels, and 1,125 pre-repair held-out IDs under lock SHA-256 `57224a1f1ba8333bbc900b23ff6127a189649feb01c279f30fac05a305658863`.
- No PDF, EPUB, DjVu, archive, page-image set, witness directory, or other page-level edition witness currently exists in the repository. The previously discussed EPUB is absent.
- The 1,444 legacy JPEGs are cropped illustrations/components, not complete pages. They cannot establish surrounding prose, punctuation, blank/figure-only pages, page furniture, full captions, Index column order, or omitted plates.
- The monolith and 17 split Markdown files share an OCR lineage and are routing evidence only, not independent transcription witnesses.
- The repaired sibling remains absent. Stage 3 writes only witness metadata, acquisition/audit tooling, tests, and permitted bounded review artifacts under `goal-4/**`; it does not create canonical repaired author text.
- An independent search for an official/licensed edition-identical source, stable page-level access, edition identity, permissions, and complete page/plate coverage is in progress.

## Updated Assumptions

- The official 2002 print edition or an official edition-identical online rendering is the preferred primary witness; edition identity must be proven rather than inferred from title alone.
- A searchable HTML transcription is useful only if its relationship to the printed edition, source notation, images, pagination, and Index layout is explicit. It cannot by itself authorize layout- or symbol-sensitive repairs.
- A downloadable file or stable online page endpoint does not automatically authorize committing or redistributing the witness. The audit mount may need to remain external/read-only with only hashes, page metadata, and bounded permitted review artifacts committed.
- The Colophon's 1,280-page statement is a reconciliation clue, not a count to force. Covers, publication matter, roman/Arabic numbering, blanks, plates, and digital-only units require an explicit counting definition.
- Witness coverage can be built incrementally, but every uncovered or illegible authorial region remains a typed batch/release blocker. Dependency-independent Stages 4–7 may continue once the witness schema and mount contract are frozen.

## Big Picture Objective

Acquire and validate authoritative, edition-identical page-level evidence sufficient to verify every authorial region, technical token, visual component/caption, and Index column without relying on OCR plausibility or correlated derivatives.

## Detailed Implementation Plan

- Identify candidate official/licensed witnesses and record direct provenance, edition/ISBN/publication identity, access date, owner/provider, terms, permitted local use, and stability risks.
- Define a read-only witness-mount contract and a versioned witness manifest. Do not commit bulk copyrighted page content unless the source terms explicitly permit it.
- Derive the complete physical/digital unit universe independently from the witness: covers, publication matter, numbered and unnumbered pages, blanks, figure-only pages, plates, Notes, Index, and Colophon.
- Give every unit a stable witness ID and record source locator, printed/digital numbering, ordered position, byte/render hash, dimensions, color profile where relevant, duplicate/missing status, and edition binding.
- Partition every unit into nonoverlapping regions typed as prose/punctuation, heading/furniture, formula/code/data, figure/caption/color, Index column, or demonstrably non-authorial material.
- Record region geometry/locator, content hash or permitted bounded evidence hash, raw block/segment candidates, legibility by risk dimension, reviewer state, and release impact.
- Require independently reviewed enumerated reasons for `NOT_APPLICABLE`; blank, figure-only, illegible, or untranscribed authorial regions never qualify automatically.
- Reconcile the derived unit/page definitions to the Colophon's 1,280-page clue and record any difference without coercing the census.
- Freeze the blind held-out transcription/adjudication packets from the already selected 1,125 raw IDs before reviewers see proposed repairs. Enforce reviewer/proposer separation and permitted evidence handling.
- Implement independent validators for manifest schemas, path/URL safety, edition identity, unit order/coverage, nonoverlapping regions, hashes, mount drift, duplicate/missing units, legibility closure, licensing metadata, held-out blinding, and raw/segment joins.
- Add mutations for missing/duplicated/reordered/tampered pages, page-number aliasing, swapped page images, cropped regions, illegal committed witness payloads, false `NOT_APPLICABLE`, changed permissions/hash, formula/Index legibility downgrades, and outcome leakage.
- If the preferred witness is unavailable or incomplete, pursue alternate authoritative sources and record exact gaps/unblock actions. Do not fill any source gap from model inference, OCR agreement, or mathematical/language plausibility.

Expected Stage 3 writes are restricted to `goal-4/**`, including the witness manifest/schema, source/mount metadata, coverage and unresolved ledgers, acquisition/validation tools, tests, and this report. External licensed witness bytes remain outside the repository unless their terms explicitly authorize inclusion.

## No-Cheating Checks

- Recompute and compare the Stage 2 lock and explicit legacy manifest before and after every witness operation; never discover witness or repaired output as raw corpus input.
- Require a source/edition chain for every witness unit. Title similarity, page-number coincidence, or OCR agreement is not edition proof.
- Keep source bytes/read-only mounts separate from committed metadata and from future generated output. Never feed a repaired render back as witness input.
- Independently derive unit order and total coverage; do not copy the expected 1,280 number into the result or silently omit blanks, covers, plates, figure-only pages, or Index leaves.
- Require complete region partition arithmetic with no gap/overlap and an independently reviewed enumerated reason for every non-authorial exclusion.
- Treat legibility separately for prose, punctuation, technical notation, figures/captions/color, and Index columns; a page readable for prose may still be unusable for symbols or layout.
- Freeze held-out evidence packets and reviewer assignments before proposed repaired answers are visible. Reject any outcome/detector/repair field in sample selection or blind adjudication inputs.
- Reject tampered, missing, dynamically changed, unlicensed, or wrong-edition witness material. A hash proves identity only after the hashed content has been lawfully inspected and classified.
- Do not claim human or independent review for agent-only or automated work.

## Completion Requirements

- A versioned manifest covers every witness-derived physical/digital unit in deterministic order with source, edition, permission, locator, hash, dimensions, numbering, and duplicate/missing facts.
- Every unit is partitioned into total nonoverlapping regions; each authorial region is legible for its risk dimensions or has an explicit downstream/release blocker.
- Every `NOT_APPLICABLE` region is narrowly enumerated, evidenced as non-authorial, and independently reviewed.
- Formula/code/data symbols, figure components/captions/color, and Index columns are demonstrably legible in at least one authorized edition-identical primary witness.
- The census is reconciled to the 1,280-page clue under a documented counting definition rather than forced to match.
- Witness provenance, edition identity, licensing, permitted storage/use, audit-mount procedure, and offline rebuild behavior are documented and validated.
- The pre-frozen held-out sample has blind witness transcription/adjudication packets with no proposal leakage and governed reviewer identities/states.
- Missing, duplicated, reordered, swapped, cropped, wrong-edition, permission-drifted, and byte-tampered witness mutations fail for specific reasons.
- Full Stage 1/2 validation, normal/optimized/relocated witness validation, direct whitespace/diff/scope checks, and independent hostile review pass.
- If complete evidence cannot be obtained, the witness manifest remains total, exact affected blocks/regions become `SOURCE_BLOCKED`, dependency-independent Stage 4 may proceed, and Stage 42 remains barred from an unqualified full-repair claim.

## Stage Results

- In progress. Local witness discovery found no page-level PDF/EPUB/scan or audit mount in the repository. Official/licensed source and permission research is underway; no witness bytes or repaired author text have been created.
