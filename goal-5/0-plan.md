# Goal 5: Practical ANKoS Corpus Repair

Shorthand: `LEAN-BOOK-REPAIR`

## Big-Picture Objective

Replace the overbuilt Goal 4 effort with a small, finishable workflow that makes
the local *A New Kind of Science* corpus correctly partitioned, readable,
navigable, and reproducible for use inside this repository.

Begin by removing Goal 4 machinery that does not contribute directly to that
deliverable. Then build a repaired sibling corpus from the immutable legacy
inputs, correct known structural and Markdown defects, make every local image
reference resolve, add useful navigation, and document remaining OCR or source
uncertainty honestly.

This is a practical repository edition, not a publication-grade critical
edition or a claim that every character has been checked against every printed
page. Exhaustive witness certification can be pursued later as a separate goal
if a properly licensed source and reviewers become available.

## Scope

### In scope

- Remove the superseded Goal 4 plans, generated ledgers, locks, schemas,
  pipeline code, tests, bytecode, and empty/staged output that are not needed by
  this lean workflow.
- Preserve the current `ref/A-New-Kind-of-Science/` tree byte-for-byte.
- Generate a repaired sibling at
  `ref/A-New-Kind-of-Science-Repaired/`.
- Partition the corpus into 29 plainly named author-text documents:
  publication/contents, Preface, 12 chapters, General Notes, 12 chapter Notes
  documents, Index, and Colophon.
- Correct the known chapter/Notes/Index/Colophon boundary failures.
- Preserve and resolve all 1,444 legacy image references without duplicating
  image bytes unless portability is later made an explicit requirement.
- Repair Markdown structure and source-backed transcription defects that
  materially affect readability or meaning.
- Add a contents page, stable headings/anchors, and useful main-text/Notes
  navigation.
- Record unresolved OCR, formula, code, caption, figure, and Index limitations
  in a short human-readable document.
- Provide a deterministic build and focused validation proportional to a local
  reference corpus.

### Out of scope

- Certifying every unchanged block against an edition-identical page witness.
- A physical census of covers, leaves, blanks, endpapers, plates, trim, bleed,
  or spread geometry.
- Claiming a facsimile, scholarly critical edition, or ambiguity-free
  transcription.
- Independent specialist review of every formula, code token, caption, or
  Index entry.
- Security-hardening a local document build against malicious callers,
  filesystem races, inode substitution, or forged authority records.
- Recreating Goal 4's schema graph, proof locks, hostile mutation matrix,
  reviewer-authority model, or per-block provenance database.
- Replacing the legacy corpus, migrating Goal 1/3 consumers, or changing exact
  legacy citations.
- Duplicating approximately 100 MiB of JPEG assets merely to make the repaired
  tree self-contained.

## Non-Negotiable Constraints

1. **Legacy input is immutable.** Goal 5 must not modify, rename, delete, or
   reformat anything under `ref/A-New-Kind-of-Science/`.
2. **Unrelated work is protected.** Cleanup may remove superseded Goal 4 work,
   but it must not discard changes outside Goal 4 or the empty repaired-output
   target. Inspect `git status` and relevant diffs before deletion.
3. **Goal 4 cleanup is intentional and bounded.** Git history is the archive.
   Transfer only compact, independently rechecked facts that Goal 5 genuinely
   needs; do not retain machinery merely because it already exists.
4. **Build beside the legacy corpus.** All repaired output belongs under
   `ref/A-New-Kind-of-Science-Repaired/`, never inside the legacy root.
5. **Always build from raw inputs.** A clean build starts from the legacy
   monolith/assets plus a small explicit repair specification, never from a
   previous repaired output.
6. **Do not silently invent author text.** Textual changes require permitted,
   inspectable evidence. When evidence is insufficient, preserve the raw text
   and disclose the limitation.
7. **Structure is not transcription proof.** Successful parsing, rendering,
   syntax checking, or plausible wording does not establish what the book
   printed.
8. **Keep the implementation small.** Prefer one understandable builder, one
   focused validator, a compact repair file, and targeted tests. Every new
   abstraction must serve a current acceptance criterion.
9. **No framework-first work.** Do not build generalized AST, workflow,
   authority, review, provenance, or release frameworks before a concrete
   corpus repair requires them.
10. **No false completion claim.** The repaired edition must describe itself as
    structurally repaired and practically reviewed, with any unresolved source
    fidelity limitations visible.

## Current Facts To Reverify

These are planning facts, not trusted acceptance fixtures. Stage 2 must
rederive the facts it uses after Stage 1 cleanup.

- The legacy corpus currently contains 19 Markdown files and 1,444 JPEGs.
- The monolith is approximately 3.78 MB and 22,498 logical lines.
- The monolith contains 1,444 image references with unique basenames, while the
  split corpus omits three references and has misleading back-matter splits.
- Chapter 12 currently runs into General Notes; nominal Notes, Index, and
  Colophon files contain displaced Notes and back matter.
- The actual Index is column-flattened and cannot honestly be called a faithful
  reconstruction without stronger layout evidence.
- Goal 4 currently contains dozens of generated artifacts and roughly 21,000
  lines of Python/schema/test machinery, while author-text repair remains
  blocked.
- At scaffold validation, Goal 4 has modifications in
  `pipeline-contract.json`, `tools/pipeline_schema_lib.py`, and
  `tools/validate_stage4.py`, plus untracked
  `schemas/execution-receipt.schema.json` and
  `tools/execution_receipt_runner.py`. Goal 4 may still be changing, so Stage 1
  must resync rather than trust this snapshot. These paths are within the
  user-authorized cleanup scope, but their diffs/content must be inspected
  before deletion to confirm they contain no unrelated work.
- `ref/A-New-Kind-of-Science-Repaired/` currently exists as an empty publication
  target.
- No licensed complete fixed-layout witness is presently available for an
  exhaustive AI-assisted fidelity audit.

## Assumptions To Challenge

- The monolith contains the complete author-text sequence needed for all 29
  documents despite local OCR defects.
- The known line boundaries remain correct when independently rederived.
- Referencing immutable legacy JPEGs by relative path is acceptable for this
  repository-local repaired edition.
- A small explicit set of structural transforms can fix the major usability
  defects without rewriting author text.
- CommonMark-compatible output plus narrowly documented extensions is adequate
  for the corpus.
- The damaged Index can be made useful without pretending its printed column
  order has been fully certified.
- Existing Goal 1/3 consumers remain unaffected because the sibling output is
  outside the legacy root.

## Proposed Minimal Output

The exact filenames are frozen in Stage 2, but the intended shape is:

```text
ref/A-New-Kind-of-Science-Repaired/
├── README.md
├── Contents.md
├── FRONT-MATTER/
│   ├── Publication-and-Contents.md
│   └── Preface.md
├── CHAPTERS/
│   ├── 01-The-Foundations-for-a-New-Kind-of-Science.md
│   ├── ...
│   └── 12-The-Principle-of-Computational-Equivalence.md
└── BACK-MATTER/
    ├── NOTES/
    │   ├── 00-General-Notes.md
    │   ├── ...
    │   └── 12-The-Principle-of-Computational-Equivalence-Notes.md
    ├── Index.md
    └── Colophon.md
```

Goal-owned implementation should remain similarly small:

```text
goal-5/
├── 0-plan.md
├── 0-loop.md
├── 0-prompt.md
├── build.py                 # expected, not mandatory if a simpler form wins
├── validate.py              # expected, focused acceptance checks
├── repairs.jsonl            # text-changing repairs only
├── known-limitations.md
└── tests/                   # focused fixtures for real failure modes
```

Generated metadata may be added only when a stage demonstrates why it is
needed. There is no requirement to reproduce this sketch mechanically.

## Success Metrics

- Superseded Goal 4 machinery is removed after bounded diff inspection, with no
  changes to the legacy corpus or unrelated work.
- A clean command builds exactly 29 author-text documents plus clearly labeled
  generated navigation/readme files in the repaired sibling.
- The front matter, Chapters 1–12, General Notes, chapter Notes 1–12, Index, and
  Colophon have correct ownership and ordering.
- Every raw author-text span selected for the 29 documents is conserved exactly
  once, except for changes listed in the compact repair file.
- Every text-changing repair records its source location, before/after text,
  reason, and evidence; structural path/heading generation does not require a
  per-block provenance record.
- All 1,444 legacy image references are accounted for, appear at the intended
  corpus positions, and resolve from the repaired Markdown.
- The three references missing from the old split corpus are present in the
  repaired edition.
- Known malformed boundaries, accidental prose fences, broken headings, and
  other selected structural sentinels are fixed or explicitly documented.
- Local links, image links, headings, anchors, fences, and expected document
  counts pass focused validation.
- Two builds from the same legacy inputs produce byte-identical text output.
- The repaired README clearly distinguishes completed structural repair from
  unresolved exhaustive OCR/layout certification.
- Goal 1/3 behavior and the complete legacy tree remain unchanged.

## Verification Requirements

- Record pre-cleanup `git status`, inspect diffs under Goal 4, and compare the
  post-cleanup diff against the explicit removal scope.
- Hash the legacy tree before cleanup and after final release using an
  independently understandable command or small validator.
- Recompute corpus counts, monolith boundaries, image-reference counts, and
  back-matter anomalies rather than importing Goal 4 locks as authority.
- Verify the 29 source ranges are ordered, nonoverlapping, and cover the chosen
  author-text stream exactly once.
- Reassemble the 29 raw projections before repairs and compare them with the
  selected monolith spans.
- Validate every repair preimage and expected occurrence count before applying
  it; fail when the raw input drifts.
- Build twice into fresh temporary directories and recursively compare the text
  outputs.
- Check all relative Markdown and image links from their actual document
  locations.
- Parse headings and fence delimiters, check duplicate anchors, and test the
  known boundary/image/fence regressions.
- Run repository tests affected by the sibling corpus, plus direct
  `git diff --check` and scope inspection.
- Perform a human-readable spot check across front matter, every chapter,
  General Notes, every chapter Notes document, Index, and Colophon. Record the
  sampling method and findings without labeling it exhaustive review.

## Stages

### 1-CLEANUP

#### Big Picture Objective

Remove the superseded Goal 4 implementation and leave a clean, understood base
for the lean repair without harming legacy sources or unrelated work.

#### Detailed Implementation Plan

- Sync `git status`, enumerate Goal 4 and repaired-output artifacts, measure
  their size, and inspect all modified Goal 4 diffs.
- Confirm that the modified Goal 4 files contain only superseded Goal 4 work.
  If anything unrelated is found, preserve or relocate it before removal.
- Extract into Goal 5 only compact facts that are still useful, and mark them
  for independent Stage 2 reverification.
- Remove `goal-4/**`, including plans, stage reports, generated JSON/JSONL,
  schemas, locks, tools, tests, and bytecode caches.
- Remove the repaired sibling only if it is still empty or contains only
  unverified Goal 4 staging output; never delete an owned release without
  inspecting it.
- Check for Goal 4 references elsewhere and update only references that would
  otherwise become broken or misleading. Do not migrate unrelated consumers.
- Record the exact removal and preservation decisions in the stage report.

#### Completion Requirements

- Pre-cleanup status and modified-file diffs are recorded in the stage report.
- `goal-4/` and its superseded generated machinery are absent; Git history
  remains the archive.
- No file under the legacy corpus changed by path, mode, or bytes.
- No unrelated worktree modification was deleted or overwritten.
- No `__pycache__`, stale Goal 4 staging output, or broken live documentation
  reference remains.
- `git diff --check` and explicit scope inspection pass.
- Stage 2 has a short list of facts to rederive, not a dependency on Goal 4
  locks or validators.

### 2-BASELINE

#### Big Picture Objective

Establish the smallest trustworthy corpus map and freeze the repaired document
layout without recreating Goal 4's audit framework.

#### Detailed Implementation Plan

- Independently enumerate and hash the explicit legacy Markdown/image inputs.
- Recompute the monolith's line/byte properties, the 29 document boundaries,
  image-reference sequence, and known split/back-matter anomalies.
- Compare split files with the monolith only as routing evidence; do not treat
  agreement between them as independent transcription proof.
- Freeze the 29 repaired paths/order and define how their relative image links
  reach immutable legacy assets.
- Create a compact baseline artifact only if the builder or validator consumes
  it directly; otherwise keep the values in readable code/data.
- Write the repaired-edition fidelity statement and initial known-limitations
  list before changing content.
- Add focused tests for incorrect boundaries, missing image references, and raw
  input drift.

#### Completion Requirements

- All legacy inputs used by the build are explicit and hash-checked.
- Exactly 29 ordered, nonoverlapping source ranges are defined and independently
  checked against the monolith.
- Image counts and the three known split omissions are reproduced.
- Actual Notes, Index, and Colophon boundaries are reproduced from local
  evidence.
- Output paths and asset-link policy are fixed and collision-free.
- The limitations statement forbids claims of exhaustive transcription or
  fixed-layout Index fidelity.
- Baseline code/data remains compact and directly tied to acceptance criteria.

### 3-STRUCTURE

#### Big Picture Objective

Build the 29-document repaired corpus with correct boundaries and byte-conserved
raw author text before undertaking optional textual corrections.

#### Detailed Implementation Plan

- Implement a straightforward clean builder from the frozen monolith ranges.
- Emit the 29 documents in the frozen order with minimal generated envelopes.
- Correct document ownership and boundary placement for Chapter 12, General
  Notes, chapter Notes, Index, and Colophon.
- Restore all monolith image references in source order and rewrite their paths
  so they resolve to immutable legacy images.
- Generate a small README and Contents page clearly labeled as editorial
  navigation rather than author text.
- Implement an independent-enough conservation check that reassembles raw
  projections and detects gaps, overlaps, duplication, or reordering.
- Test clean builds from repository root and one temporary output location.

#### Completion Requirements

- A single documented command generates the complete repaired tree from legacy
  inputs into a fresh destination.
- Exactly 29 author-text documents exist with correct ownership/order.
- Pre-repair reassembly matches the selected raw monolith stream exactly,
  allowing only one explicitly documented terminal-newline serialization rule
  if necessary.
- All 1,444 image references occur in the expected order and resolve.
- The legacy tree and existing consumer files are unchanged.
- Focused boundary, conservation, path-safety, stale-output, and input-drift
  tests pass.

### 4-REPAIR

#### Big Picture Objective

Improve practical Markdown readability and fix source-backed defects without
turning uncertainty into invented text or attempting exhaustive certification.

#### Detailed Implementation Plan

- Run simple detectors for empty headings, accidental prose fences, obvious
  delimiter imbalance, broken local markup, split boundary artifacts, and
  selected known defects.
- Review detector hits in context and prioritize defects that materially affect
  rendering, search, code/formula meaning, or comprehension.
- Represent every author-text change in one compact repair file with guarded
  preimage, expected count, location, rationale, and permitted evidence.
- Treat purely generated navigation/path changes separately from author-text
  repairs.
- Preserve uncertain OCR literally and add a concise limitation/candidate entry
  rather than guessing.
- Give formulas, Wolfram Language, data tables, captions, and Index content
  extra manual scrutiny when they are changed, but do not require a generalized
  specialist workflow engine.
- Render and inspect representative changed passages plus each high-risk change.

#### Completion Requirements

- Every applied author-text repair is explicit, preimage-guarded, reversible by
  inspection, and supported by recorded evidence.
- No unresolved candidate is silently changed merely because the result looks
  plausible or parses.
- Selected known structural/Markdown regression sentinels are fixed or listed
  in `known-limitations.md` with their practical impact.
- All changed high-risk formula/code/data/caption/Index passages receive an
  explicit visual/manual review note.
- Detector, builder, conservation, and focused rendering checks pass.
- The repair mechanism stays corpus-specific and substantially simpler than the
  removed Goal 4 framework.

### 5-NAVIGATION

#### Big Picture Objective

Make the repaired corpus pleasant to browse inside the repository while keeping
editorial navigation distinct from the book's author text.

#### Detailed Implementation Plan

- Finalize Contents links to all 29 documents and useful internal section
  headings.
- Create deterministic, collision-free anchors using the chosen Markdown
  renderer's actual behavior or explicit minimal anchors where necessary.
- Add clearly editorial main-chapter to chapter-Notes links and backlinks.
- Validate every Markdown link and image path relative to its containing file.
- Improve Index usability only as supported by available evidence; preserve and
  disclose column-order uncertainty instead of claiming print-faithful
  reconstruction.
- Perform a representative render/browse pass across all document classes.

#### Completion Requirements

- Contents reaches all 29 author-text documents and every target exists.
- Main/Notes navigation works for all 12 chapter pairs and General Notes is
  reachable.
- All local document/image links resolve with no duplicate explicit anchors.
- Index limitations are visible where a reader encounters the Index.
- Generated editorial material is distinguishable from author text.
- Navigation remains deterministic across two clean builds.

### 6-RELEASE

#### Big Picture Objective

Publish the practical repaired sibling, prove the lean acceptance criteria, and
leave an honest, maintainable handoff.

#### Detailed Implementation Plan

- Build twice from the immutable legacy corpus into fresh temporary directories
  and compare outputs byte-for-byte.
- Run focused Goal 5 tests, affected repository tests, link/Markdown checks,
  `git diff --check`, and scope inspection.
- Rehash the legacy tree and compare it with the pre-cleanup/pre-build state.
- Spot-check front matter, all 12 chapters, General Notes, all 12 chapter Notes
  documents, Index, and Colophon using a predeclared lightweight sample method.
- Publish the validated output to the sibling directory using a simple staged
  replacement appropriate to a local repository build; do not construct a
  hostile-filesystem transaction protocol.
- Write a concise final report in the repaired README or Goal 5 stage report:
  what was repaired, commands used, known limitations, and how to rebuild.
- Confirm no legacy consumer was silently migrated.

#### Completion Requirements

- Two fresh builds are byte-identical and the published sibling matches them.
- All success metrics and verification requirements in this plan are checked
  requirement-by-requirement.
- The legacy corpus matches its initial hashes and unrelated work is intact.
- Exactly 29 author-text documents are present, all required links/images
  resolve, and known regressions pass.
- The spot check covers every document class and records findings honestly.
- The README states that the edition is structurally repaired and practically
  reviewed, not exhaustively witness-certified.
- Build, validation, known limitations, and future optional scholarly-audit
  work are documented clearly enough for another session to continue.
