# Goal 5: Reliable ANKoS Markdown Source

Shorthand: `BOOK-SOURCE`

## Big-Picture Objective

Create a reliable Markdown source of the complete *A New Kind of Science* book
with the OCR errors corrected.

The result must preserve the book's actual text and organization across front
matter, all 12 chapters, General Notes, all 12 chapter Notes sections, formulas,
Wolfram Language code, tables, captions, figures, Index, and Colophon. It must
also be easy to navigate and reproducibly build from preserved inputs.

Goal 5 keeps the fidelity objective that motivated Goal 4 while discarding the
process machinery that does not help correct or verify the book. The first
stage cleans up Goal 4's unnecessary schemas, locks, authority models, race
defenses, generated ledgers, tests, caches, and unfinished pipeline work. It
retains or migrates only source facts and tools that directly reduce the work
of producing and checking the corrected book.

Completion is not “best effort with disclosed OCR errors.” Completion means the
entire corpus has been reviewed against an authoritative source, all discovered
OCR errors have been corrected, all review coverage is accounted for, and no
known transcription ambiguity remains open. Literal errors present in the book
itself are preserved as source text rather than silently corrected.

## What “Reliable” Means

The repaired corpus is reliable when:

- every part of the book has received a sequential source comparison rather
  than only detector-driven spot checking;
- corrections are grounded in an authoritative edition-identical source, not
  language-model plausibility or agreement between correlated OCR derivatives;
- prose, punctuation, capitalization, spacing, headings, lists, formulas, code,
  rule tables, captions, Index entries, and reading order are all in scope;
- high-risk technical and multi-column material receives a dedicated second
  pass;
- automated searches are used to find residual defects but never treated as a
  substitute for reading;
- a separate verification pass confirms the corrected corpus and closes or
  reopens every discrepancy;
- the final Markdown builds deterministically, links and images resolve, and the
  legacy corpus remains byte-for-byte unchanged.

This is source-fidelity work, but it does not require a forensic publication
system. Reliability comes from complete comparison, careful correction, a
simple coverage record, focused review, and reproducible output—not from a
large schema graph or hostile-filesystem security model.

## In Scope

- Clean up Goal 4 artifacts that do not directly support book correction.
- Preserve the legacy corpus as immutable raw evidence.
- Establish a lawful, readable, edition-identical authoritative source for the
  complete book.
- Produce 29 correctly owned canonical Markdown documents: publication and
  contents, Preface, 12 chapters, General Notes, 12 chapter Notes documents,
  Index, and Colophon.
- Correct all OCR transcription errors found through complete sequential
  comparison and follow-up detector passes.
- Correct document boundaries, paragraph/list/heading structure, reading order,
  Markdown fences, formulas, code, captions, and Index column flattening where
  the authoritative source establishes the answer.
- Account for and correctly place every legacy image; add a missing visual only
  when a lawful authoritative source establishes that it belongs in the book
  and permits the chosen handling.
- Add generated contents and navigation without presenting editorial material
  as author text.
- Build and validate the repaired sibling corpus reproducibly.

## Out of Scope

- Correcting factual, mathematical, historical, or typographical errors that
  are actually present in the authoritative book. Those may be noted in a
  separate errata file, but the canonical transcription preserves them.
- Creating a generalized document compiler, workflow engine, evidence database,
  reviewer-identity system, or security boundary.
- A census of covers, endpapers, blank leaves, trim, bleed, file inodes, or
  other publication/security details that do not affect the Markdown book.
- Adversarial caller authorization, forged-ledger defense, atomic no-replace
  race handling, implementation proof locks, or large mutation matrices.
- Migrating Goal 1/3 consumers or replacing the immutable legacy corpus.
- Claiming human review when work was performed by an agent.

## Non-Negotiable Constraints

1. **Preserve the legacy corpus.** Do not modify, rename, delete, or reformat
   `ref/A-New-Kind-of-Science/**`.
2. **Protect unrelated work.** Inspect `git status` and diffs before cleanup or
   bulk changes. Goal 4 files may be changing concurrently; never assume an old
   inventory is current.
3. **Clean up by utility.** Retain a Goal 4 artifact only if it is directly used
   to locate, correct, build, or verify book content and is simpler to retain
   than to replace. Git history is sufficient archival storage for discarded
   process machinery.
4. **Use an authoritative source.** A transcription-changing decision must be
   checked against a lawful, edition-identical book source. The monolith, split
   files, and extracted JPEGs are correlated or incomplete OCR evidence and
   cannot alone prove corrected wording.
5. **Respect source permissions.** Do not scrape, bulk-download, commit, or send
   copyrighted source material to tools when the applicable license or user
   authorization does not permit it. A user-provided or mounted source must
   have a clear allowed-use boundary.
6. **Do not guess.** Plausibility, spell-checking, parsers, execution, rendering,
   and model consensus may identify candidates but cannot authorize a change.
7. **Preserve authorial errors.** Distinguish OCR error from an error printed in
   the book. Canonical Markdown transcribes the latter faithfully.
8. **Review everything.** Every canonical source span and every authoritative
   source region containing book content must belong to a completed review
   batch. Detectors and samples do not replace this coverage requirement.
9. **Use simple records.** Keep a compact correction log and coverage checklist.
   Do not recreate Goal 4's per-block authority, workflow, provenance, lock, or
   review schema system.
10. **Build from preserved inputs.** Never use a previous repaired tree as the
    source for the next build.
11. **Keep editorial additions separate.** Generated anchors, page markers,
    navigation, alternative text, and errata must not masquerade as book text.
12. **Do not release with known ambiguity.** An unreadable or unavailable
    authorial source region is a real blocker to the “without OCR errors” goal;
    obtain better evidence or continue the review rather than weakening the
    objective.

## Current Facts

These facts have been rechecked against the live worktree, immutable corpus,
and pinned fixed-layout source unless explicitly described as a review risk.

- The legacy corpus contains 19 Markdown files and 1,444 JPEGs.
- The monolith is 3,780,628 bytes and 22,498 logical lines.
- The monolith references 1,444 images; the split Markdown omits three image
  references.
- Chapter 12 runs into General Notes, and nominal Notes, Index, and Colophon
  files contain displaced Notes and actual back matter.
- The Index is flattened from multiple columns and requires layout-aware source
  comparison.
- Known defects include broken headings, word joins/splits, prose inside code
  fences, malformed formulas, damaged Wolfram Language, caption interleaving,
  OCR substitutions, and back-matter reading-order errors.
- Stage 1 removed Goal 4's generated planning, schema, lock, pipeline,
  validation, and test machinery after migrating four compact fact sets. Goal
  4 had not corrected the book text.
- The sibling `ref/A-New-Kind-of-Science-Repaired/` is reproducibly generated
  from the immutable monolith plus guarded corrections. It remains a partial
  repair worktree rather than a verified complete edition.
- A complete local First-edition, First-printing PDF is pinned as the
  user-authorized fixed-layout witness for local agent-assisted comparison and
  repaired workspace output. It is Git-ignored and is not authorized here for
  redistribution.

## Assumptions To Challenge

- The pinned edition-identical source remains readable at every location needed
  for the full comparison; any unreadable region must be carried as a blocker.
- The raw monolith contains all author text even where its transcription or
  layout is damaged.
- The proposed 29-document organization accounts for all book content.
- Existing JPEGs cover all printed figures and are associated with the correct
  captions.
- A CommonMark-oriented representation can preserve the relevant structure of
  formulas, code, tables, captions, and Index entries.
- Fixed-layout margin figures require an explicit one-dimensional
  serialization: place each image and caption after the earliest complete
  paragraph that explicitly refers to it (or, when there is no reference,
  after the closest complete paragraph beside it), without splitting printed
  prose. This is a documented canonical Markdown choice, not a claim that the
  two-dimensional page has one uniquely implied linear order.
- Four-chapter review batches are small enough to review carefully without
  losing continuity or skipping content.
- A fresh second review plus targeted detectors can reach zero open OCR
  discrepancies without requiring Goal 4's formal machinery.

## Minimal Working Architecture

The exact shape is frozen in Stage 2, but the intended system is small:

```text
goal-5/
├── 0-plan.md
├── 0-loop.md
├── 0-prompt.md
├── build.py
├── validate.py
├── corrections.jsonl
├── coverage.csv
├── unresolved.md
└── tests/

ref/A-New-Kind-of-Science-Repaired/
├── README.md
├── Contents.md
├── FRONT-MATTER/
├── CHAPTERS/
└── BACK-MATTER/
    ├── NOTES/
    ├── Index.md
    └── Colophon.md
```

`corrections.jsonl` records actual author-text changes with an absolute raw
byte offset, exact before/after text, source page/location, reason, and reviewer
status.
`coverage.csv` records sequential review ranges and second-pass completion.
Neither file is a generalized workflow database.

## Success Metrics

- Unnecessary Goal 4 machinery is removed without harming useful source facts,
  the legacy corpus, or unrelated work.
- A lawful edition-identical source covers the complete book text, technical
  material, figures/captions, Index, and Colophon at readable quality.
- Exactly 29 canonical author-text Markdown documents contain the complete book
  in correct order and ownership.
- Every canonical span is included in a sequential authoritative-source review
  batch, and every batch is complete.
- Every authoritative book-content region maps to the corrected Markdown; no
  paragraph, heading, formula, code block, caption, table, Index entry, or
  Colophon text is silently omitted.
- Every applied transcription change has an exact preimage, source location,
  rationale, and completed verification state.
- Every high-risk formula, Wolfram Language block, rule table, caption, and
  reconstructed Index region receives a dedicated second comparison.
- All 1,444 legacy assets are accounted for, all repaired image references
  resolve, and figure/caption placement agrees with the authoritative source.
- Residual OCR detectors have no unexplained hits, and repeated full review
  rounds produce no new discrepancies.
- Zero known or unresolved transcription ambiguity remains at release.
- The repaired Markdown parses/renders as intended, navigation resolves, and
  two clean builds are byte-identical.
- The complete legacy tree and existing Goal 1/3 consumers remain unchanged.

## Verification Requirements

- Hash the legacy corpus before cleanup and after release.
- Inspect all modified/untracked Goal 4 content before deletion and record the
  keep/delete/migrate decision.
- Verify authoritative source identity, completeness, legibility, and allowed
  use without constructing a physical-book forensics system.
- Partition both raw and authoritative book content into simple, ordered review
  ranges and prove no range is skipped or duplicated.
- Build a zero-correction 29-document projection first and prove raw-content
  conservation before applying corrections.
- Guard every correction by exact preimage and expected occurrence count.
- For every content batch, perform a complete forward source comparison, run
  focused detectors, render changed material, and perform a separate second
  pass before closing it.
- Compare technical material character/token by character/token where ordinary
  prose review is insufficient.
- Compare the Index in printed column/entry order against fixed-layout evidence.
- Verify image order, file identity, caption association, and link resolution.
- Run corpus-wide searches for common OCR confusions, broken words,
  punctuation/Unicode anomalies, malformed Markdown/math/code, and suspicious
  vocabulary; disposition every hit.
- Repeat the final review/detector pass after the last correction until a full
  pass finds no new discrepancy.
- Build twice in fresh directories, compare outputs, run focused tests and
  affected repository tests, and run `git diff --check` plus scope inspection.

## Current Execution State

- Synced: 2026-07-15 (America/Los_Angeles).
- Active stage: `3-FRONT-CH04` (`IN_PROGRESS`).
- Stage 1 is complete. All 78 tracked Goal 4 files, 45 ignored bytecode caches,
  and the empty `goal-4/` directory were removed by exact path. No commit
  range was reverted, and Goal 4 had corrected no book text.
- The legacy tree currently contains exactly 1,463 files: 19 Markdown and 1,444
  JPEG. A sorted path-and-file-digest snapshot hashes to
  `b9ff7b9b507790f1d519593baf2b2d2f24dd6cd49dc0fe10f0ac629278ea42f4`.
- The monolith remains 3,780,628 bytes with SHA-256
  `55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20`.
- `ref/A-New-Kind-of-Science-Repaired/` contains 29 generated author-text
  documents, 1,444 JPEGs, and generated README/Contents files. It now includes
  the first source-verified corrections but is not a complete OCR-corrected
  edition.
- A repository-wide scan found no code, test, or document outside Goal 4 that
  consumes a specific Goal 4 artifact, module, schema, or contract. Goal 5 has
  intentional historical cleanup references to Goal 4 and intentional repaired
  sibling references, but no dependency on its machinery.
- Goal 5 contains four compact working datasets: 29 source-confirmed raw/PDF
  ranges, 55 known-defect/guardrail candidates, a 1,444-row image-to-asset map,
  and a concise legacy/routing/source summary. Content claims remain pending
  until their sequential comparison passes.
- The pinned source is `A New Kind of Science/A New Kind of Science.pdf`, a
  complete, readable 1,280-page First-edition, First-printing fixed-layout
  witness whose copyright-page identity matches the immutable monolith. Its
  SHA-256 is
  `a3cc5dd60e12d6b563aee86ea31a15b03f9cddfd4869b8f965d3a11bbc61a0d6`.
- Stage 2 is complete. The zero-correction build conserves all monolith bytes;
  two fresh builds match; the focused validator protects the legacy snapshot,
  exact source identity, 29 raw/PDF partitions, correction evidence, and image
  ownership; `10` tests plus `26` mutation subtests pass.
- Source comparison corrected twelve chapter-start raw boundaries and eight
  opener-image owners. All 1,444 image filenames now place their source page
  inside their owning canonical document. `FOUNDATION-SOURCE-001` is closed.
- `PUBLICATION_AND_CONTENTS` is complete after two sequential agent passes over
  PDF pages 1–8 and a clean closing pass against the rebuilt Markdown. Its 20
  guarded corrections are `G5-C-0001`–`G5-C-0020`; focused render and tests
  pass.
- `PREFACE` is complete after a sequential first pass over PDF pages 9–16 and
  an independent clean second pass against the rebuilt Markdown. Its 59 guarded
  corrections are `G5-C-0021`–`G5-C-0079`; exact text/emphasis comparison,
  detector scans, rendering, deterministic builds, and focused tests pass.
- `CH01` is complete after a sequential first pass over PDF pages 17–38 and an
  independent clean second pass against the final rebuilt Markdown and assets.
  Its 27 guarded corrections are `G5-C-0080`–`G5-C-0106`; the exact prose-token
  sequence, punctuation, hierarchy, emphasis, paragraph joins, three figures,
  captions, and source-faithful repaired-only opener were rechecked. Stage 3
  now continues with `CH02` at `pdf:0039`, raw line 398 and byte 79330.

## Stage Status

| Stage | Status | Prerequisites |
|---|---|---|
| 1-CLEANUP | `COMPLETE` | none |
| 2-FOUNDATION | `COMPLETE` | 1 |
| 3-FRONT-CH04 | `IN_PROGRESS` | 2 |
| 4-CH05-08 | `NOT_STARTED` | 2 |
| 5-CH09-12 | `NOT_STARTED` | 2 |
| 6-NOTES-00-04 | `NOT_STARTED` | 2 |
| 7-NOTES-05-08 | `NOT_STARTED` | 2 |
| 8-NOTES-09-12 | `NOT_STARTED` | 2 |
| 9-TECHNICAL | `NOT_STARTED` | 3–8 |
| 10-FIGURES-INDEX | `NOT_STARTED` | 3–8 plus fixed-layout source evidence |
| 11-SATURATION | `NOT_STARTED` | 3–10 |
| 12-RELEASE | `NOT_STARTED` | 11; zero open source ambiguity |

## Stages

### 1-CLEANUP

#### Big Picture Objective

Remove Goal 4 process overhead while preserving any compact source facts or
content-oriented tools that genuinely help produce the reliable book.

#### Detailed Implementation Plan

- Sync the live worktree and inspect every modified/untracked Goal 4 file.
- Inventory Goal 4 artifacts by purpose: source fact, content detector/builder,
  or process machinery.
- Keep or migrate only directly useful corpus manifests, boundary facts, known
  defect locations, image mappings, or small content checks after independently
  validating them.
- Remove generalized schemas, proof/implementation locks, licensing/workflow
  state machines, authority and reviewer models, synthetic overlay systems,
  promotion-race defenses, redundant validators/tests, generated reports,
  caches, and unfinished pipeline work.
- Inspect the repaired sibling and remove only unverified Goal 4 output so Goal
  5 starts from a clean build target.
- Confirm no live documentation or consumer is left pointing at removed Goal 4
  machinery.

#### Completion Requirements

- The stage report records pre-cleanup status and a complete keep/delete/migrate
  decision by artifact category.
- No unrelated modification is lost and the legacy corpus hash is unchanged.
- No retained artifact exists merely to validate another retained Goal 4
  artifact; every retained item directly supports correction or verification.
- Goal 4's generalized pipeline/security/workflow infrastructure and caches are
  absent.
- Goal 5 has a short, understandable starting dataset rather than a dependency
  on Goal 4's trust chain.
- `git diff --check`, broken-reference inspection, and explicit scope review
  pass.

### 2-FOUNDATION

#### Big Picture Objective

Secure the complete authoritative source, freeze the 29-document layout, and
implement the minimal reproducible build and coverage model.

#### Detailed Implementation Plan

- Recompute the legacy corpus inventory, hashes, document boundaries, image
  sequence, and known structural failures.
- Establish a complete lawful edition-identical source and document its edition,
  access boundary, page/location convention, completeness, and legibility.
- Define ordered review ranges that cover all book content without requiring a
  per-block evidence graph.
- Freeze the 29 output paths and a minimal Markdown serialization policy.
- Implement a straightforward builder that projects raw content into 29
  documents and then applies guarded corrections.
- Implement a focused validator for source range coverage, correction preimages,
  document counts, image/link resolution, and deterministic output.
- Create the initial `coverage.csv`, `corrections.jsonl`, and `unresolved.md`
  formats with only fields used by the workflow.

#### Completion Requirements

- The complete authoritative source is lawful, edition-matched, readable, and
  sufficient for all later batches; otherwise the stage stays blocked with an
  exact acquisition action.
- Exactly 29 ordered source/output ranges cover the complete raw book stream
  without gap, overlap, or duplication.
- A zero-correction build succeeds and reassembles to the selected raw stream.
- All 1,444 raw image references and physical legacy assets are inventoried.
- Builder, validator, correction record, and coverage record are small and
  documented.
- Focused raw-drift, boundary, skipped-range, duplicate-range, and correction-
  preimage tests pass.

### 3-FRONT-CH04

#### Big Picture Objective

Correct and verify publication matter, Preface, and Chapters 1–4 against the
authoritative source.

#### Detailed Implementation Plan

- Review every assigned range sequentially, including headings, page furniture,
  prose, lists, formulas, code, captions, tables, and images.
- Record and apply exact source-backed corrections.
- Run prose, punctuation, word-split, fence, math, code, and image/caption
  detectors over the batch.
- Render changed and structurally complex regions.
- Perform a separate second comparison of the complete batch and close all
  discrepancies.

#### Completion Requirements

- Every assigned source range has first- and second-pass coverage.
- All discovered OCR/layout discrepancies are corrected and verified.
- Every correction is guarded and source-located.
- No unresolved author-text item remains in the batch.
- Focused detectors, rendering checks, builder, and validator pass.

### 4-CH05-08

#### Big Picture Objective

Correct and verify Chapters 5–8 against the authoritative source.

#### Detailed Implementation Plan

- Apply the complete sequential comparison, correction, detector, rendering,
  and separate second-pass procedure from Stage 3.
- Pay extra attention to higher-dimensional layouts, formulas, rule diagrams,
  scientific notation, captions, and application-specific vocabulary.
- Fold newly discovered OCR patterns into corpus-wide detector queries without
  treating matches as automatic corrections.

#### Completion Requirements

- Chapters 5–8 have complete first- and second-pass coverage.
- All discovered discrepancies are corrected and source-verified.
- New defect patterns are searched across already reviewed and future material.
- No unresolved author-text item remains in the batch.
- Focused and cumulative validation passes.

### 5-CH09-12

#### Big Picture Objective

Correct and verify Chapters 9–12 against the authoritative source.

#### Detailed Implementation Plan

- Apply the complete batch procedure from Stage 3.
- Give formulas, symbolic notation, networks, computation diagrams, code, and
  Chapter 12's transition into General Notes explicit attention.
- Recheck any corpus-wide patterns discovered in earlier chapter batches.

#### Completion Requirements

- Chapters 9–12 have complete first- and second-pass coverage.
- All discovered discrepancies and the Chapter 12 ending boundary are correct.
- No unresolved author-text item remains in the batch.
- Focused and cumulative validation passes.

### 6-NOTES-00-04

#### Big Picture Objective

Correct and verify General Notes and Chapter 1–4 Notes.

#### Detailed Implementation Plan

- Review every Notes range sequentially with its printed page/source context.
- Preserve Notes headings, page references, cross-references, formulas, code,
  citations, captions, and image ownership accurately.
- Apply detectors and a separate full second pass, including prior corpus-wide
  defect patterns.

#### Completion Requirements

- General Notes and Chapter 1–4 Notes have complete two-pass coverage.
- Note ownership and main-text boundaries are correct.
- All discovered discrepancies are source-verified and corrected.
- No unresolved author-text item remains in the batch.
- Focused and cumulative validation passes.

### 7-NOTES-05-08

#### Big Picture Objective

Correct and verify Chapter 5–8 Notes.

#### Detailed Implementation Plan

- Apply the complete Notes review procedure from Stage 6.
- Recheck dense formulas, programs, references, and figure/caption associations
  with surrounding source context.

#### Completion Requirements

- Chapter 5–8 Notes have complete first- and second-pass coverage.
- All discovered discrepancies are corrected and source-verified.
- No unresolved author-text item remains in the batch.
- Focused and cumulative validation passes.

### 8-NOTES-09-12

#### Big Picture Objective

Correct and verify Chapter 9–12 Notes.

#### Detailed Implementation Plan

- Apply the complete Notes review procedure from Stage 6.
- Verify the displaced material currently found in nominal Index/Colophon files
  is assigned to the correct Notes document and source order.

#### Completion Requirements

- Chapter 9–12 Notes have complete first- and second-pass coverage.
- All displaced Notes boundaries and all discovered discrepancies are correct.
- No unresolved author-text item remains in the batch.
- Focused and cumulative validation passes.

### 9-TECHNICAL

#### Big Picture Objective

Perform a corpus-wide specialist-style fidelity pass over formulas, Wolfram
Language, rule tables, symbolic data, and other token-sensitive material.

#### Detailed Implementation Plan

- Enumerate technical regions from the corrected Markdown and compare each one
  directly with the authoritative source.
- Check symbols, delimiters, superscripts/subscripts, whitespace where
  meaningful, row/column order, code identifiers, operators, and line wrapping.
- Parse, render, or execute material where useful for defect discovery, while
  keeping the source comparison authoritative.
- Reopen owning content batches for any newly discovered discrepancy.

#### Completion Requirements

- Every technical region is enumerated and receives a dedicated source check.
- Every changed token is source-verified and correction records are complete.
- Parsing/rendering diagnostics have no undispositioned hit.
- No unresolved technical transcription ambiguity remains.
- Reopened batch checks and cumulative validation pass.

### 10-FIGURES-INDEX

#### Big Picture Objective

Verify all figure/caption associations and reconstruct the Index and Colophon
accurately from layout-aware source evidence.

#### Detailed Implementation Plan

- Compare every printed figure and caption with the existing asset sequence,
  detecting missing, partial, swapped, duplicated, or misowned images.
- Correct caption text and placement from source evidence.
- Reconstruct the Index in printed column and entry order, preserving headings,
  subentries, cross-references, punctuation, and page ranges.
- Verify the Colophon and all actual Index/Colophon boundaries.
- Perform a separate second pass over the complete Index and all changed figure
  groups.

#### Completion Requirements

- Every printed figure/caption group has a checked Markdown/asset disposition.
- All image references resolve and agree with their source placement.
- The complete Index has two-pass fixed-layout coverage and correct entry order.
- Colophon content and boundaries match the authoritative source.
- No unresolved figure, caption, Index, or Colophon ambiguity remains.
- Focused and cumulative validation passes.

### 11-SATURATION

#### Big Picture Objective

Find and eliminate residual OCR errors across the assembled corrected corpus.

#### Detailed Implementation Plan

- Run corpus-wide detectors for common OCR substitutions, improbable tokens,
  broken joins/splits, punctuation/Unicode anomalies, malformed Markdown,
  formula/code errors, headings, captions, cross-references, and Index forms.
- Review every detector hit against the authoritative source.
- Conduct a fresh sequential verification pass over all 29 documents using the
  coverage checklist, with special attention to unchanged passages surrounding
  prior corrections.
- Reopen the owning stage for every discovered discrepancy.
- Repeat the complete detector and verification round after the last correction
  until a full round yields no new discrepancy.

#### Completion Requirements

- Every detector hit has a source-backed disposition.
- All 29 documents have a completed fresh verification pass.
- The final complete round finds no new discrepancy.
- `unresolved.md` contains zero author-text transcription ambiguity.
- Coverage, correction, structure, image, link, and cumulative tests pass.

### 12-RELEASE

#### Big Picture Objective

Publish the corrected Markdown source and prove the full-book reliability claim
without reintroducing Goal 4's process overhead.

#### Detailed Implementation Plan

- Build twice from immutable legacy inputs and the correction set into fresh
  directories; compare outputs byte-for-byte.
- Validate document/source coverage, corrections, technical regions,
  figures/captions, Index, navigation, assets, and Markdown rendering.
- Rehash the legacy corpus and compare it with the initial snapshot.
- Run focused Goal 5 tests, affected repository tests, `git diff --check`, and
  explicit scope inspection.
- Publish the verified sibling tree and write concise build, source, review,
  correction, and maintenance documentation.
- State reviewer types accurately and distinguish corrected OCR from optional
  source errata annotations.

#### Completion Requirements

- All prior stages are complete with zero open author-text ambiguity.
- Exactly 29 canonical documents contain the complete book in correct order.
- Complete first-pass, second-pass, technical, figure/Index, and saturation
  coverage is verified.
- Two clean builds are byte-identical and match the published sibling.
- All links and image references resolve and Markdown renders as intended.
- Legacy hashes and existing consumer behavior remain unchanged.
- The final documentation gives exact rebuild/validate commands and accurately
  supports the claim that known OCR errors have been removed.
