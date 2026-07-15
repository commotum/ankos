# 2-FOUNDATION

Status: COMPLETE

## Current Facts

- Stage 1 is complete; `goal-4/` is absent and the legacy corpus hash is
  unchanged.
- The raw monolith is 3,780,628 bytes and 22,498 logical lines with SHA-256
  `55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20`.
- The 29 source-confirmed ranges cover every monolith byte and line exactly
  once, and every segment hash matches.
- The image map contains 1,444 ordered references to 1,444 physical JPEGs; each
  live asset hash and referenced monolith line matches.
- `ref/A-New-Kind-of-Science-Repaired/` now contains the generated
  zero-correction baseline: 29 author-text documents, 1,444 JPEGs, and two
  clearly editorial navigation/readme files.
- The complete local fixed-layout witness is
  `A New Kind of Science/A New Kind of Science.pdf`, SHA-256
  `a3cc5dd60e12d6b563aee86ea31a15b03f9cddfd4869b8f965d3a11bbc61a0d6`:
  57,779,240 bytes, 1,280 pages, First edition, First printing, ISBN
  `1-57955-008-8`. It matches the legacy monolith's stated edition and is
  explicitly authorized by the user for local Goal 5 comparison and repaired
  workspace output. It remains Git-ignored and is not authorized here for
  redistribution.
- Ghostscript rendered all 1,280 pages successfully. The source contains the
  fixed-layout four-column Index and complete Colophon; representative prose,
  technical, figure, Notes, Index, and Colophon regions are visually legible.
  The PDF's embedded text is diagnostic only because custom glyphs and columns
  extract incorrectly.

## Updated Assumptions

- The source-confirmed 29-range layout is frozen. PDF pages 1–1,280 form one
  gapless partition. For Arabic-numbered material the logical printed-page
  mapping is one-based PDF page − 16; the Index leaves themselves are
  unfoliated.
- Chapter opener numbers/images at raw lines 166, 398, 680, 1368, 2142, 2700,
  3420, 4336, 5164, 6586, 7692, and 8608 belong to the chapter they introduce,
  not the preceding document.
- The monolith, never repaired output, is the only build input.
- The 1,444-row image map is a frozen legacy inventory, not proof that the
  authoritative edition contains no omitted, replaced, or differently placed
  visual. Source-confirmed visual changes must be recorded explicitly later.
- A builder that slices 29 byte ranges, applies ordered exact-preimage
  corrections, and copies the mapped images is sufficient.
- A validator needs only check the facts that can make this book build wrong:
  raw drift, range coverage, guarded corrections, coverage rows, output bytes,
  assets, generated navigation, and deterministic reproduction.

## Big Picture Objective

Create the smallest understandable 29-document build and validation workflow,
pin its complete fixed-layout source, and freeze semantically correct document
and image ownership before content correction begins.

## Detailed Implementation Plan

1. Add a small standard-library `build.py` that reads the immutable monolith,
   validates the 29 ranges, applies only source-verified corrections anchored
   by absolute raw byte offset and exact preimage, copies the 1,444 mapped
   assets beside their documents, and writes simple generated README/Contents
   files.
2. Add a focused `validate.py` that independently checks inputs, coverage,
   expected document bytes, image targets, generated navigation, and the exact
   output file set.
3. Add empty `corrections.jsonl`, one baseline `coverage.csv` row per
   document, and `unresolved.md` for explicit source or content ambiguities.
4. Add focused tests for raw drift, gaps/overlaps, duplicate output ownership,
   correction preimages, incomplete correction evidence, skipped coverage,
   output mutation, and reproducibility.
5. Produce and validate the zero-correction baseline without describing it as
   a corrected edition.
6. Pin and validate the complete source identity, local-use boundary, page
   partition, fixed-layout Index, and legibility before beginning content
   correction.

## No-Cheating Checks

- A correction without an exact preimage, expected count, authoritative
  location, reason, reviewer type, and source-verified status is rejected.
- Zero corrections must reproduce the monolith exactly when the 29 author-text
  files are concatenated in order.
- Repaired output is never accepted as an input path.
- Range gaps, overlaps, duplicate document IDs or paths, raw hash drift,
  missing/changed images, skipped coverage rows, and unlisted output files fail
  validation.
- The build can be called a baseline projection, not an OCR-corrected book.
- A missing, changed, mislocated, or unpinned source PDF fails validation.
- Every source PDF page and raw byte belongs to exactly one canonical document.
- Every `_page_N_` legacy asset must map to PDF page `N + 1` inside its owning
  document's authoritative page interval.
- Every correction location must begin with canonical `pdf:NNNN` and lie inside
  the correction's owning document range.
- Copying every legacy image does not prove figure order or caption association.
- A document's second-pass coverage can close only after every correction and
  technical/visual region in that document has been rechecked. The monotonic
  `pdf:NNNN` ranges are frozen, while all content-review rows remain `NO`.

## Completion Requirements

- [x] A user-authorized, edition-matched, complete, readable source is
  documented and pinned without committing the source payload.
- [x] Exactly 29 ordered ranges cover the complete raw stream without gap,
  overlap, or duplication.
- [x] A zero-correction build succeeds and reassembles to the raw stream.
- [x] All 1,444 raw image references and physical assets are inventoried and
  hash-checked.
- [x] The builder, validator, correction log, and coverage record are small and
  documented.
- [x] Focused drift, boundary, skipped/duplicate range, correction-preimage,
  output-mutation, and determinism tests pass.

## Stage Results

Completed on 2026-07-15 after the user authorized the complete local PDF and
the source, page partition, semantic boundaries, and image ownership were
verified. No author text has yet been corrected or claimed reviewed; all 29
content first/second-pass values remain `NO` for Stage 3 onward.

- Added `build.py` and `validate.py`, using only the Python standard library.
  Corrections are tied to an absolute monolith byte offset and exact nonempty
  preimage, checked against the original document, rejected on overlap, and
  applied from the end of each document backward.
- Added an empty `corrections.jsonl`, a 29-row ordered `coverage.csv` with both
  passes explicitly `NO`, canonical `pdf:NNNN` ranges, and `unresolved.md`
  recording closure of the former source blocker.
- The zero-correction build produced 29 author-text Markdown files and 1,444
  adjacent JPEGs. Concatenating the 29 files in range order reproduces all
  3,780,628 monolith bytes, including the absent terminal newline.
- The validator accepts exactly the expected 1,475 files, verifies every
  document and image byte, checks the ordered image-reference sequence and
  generated Contents targets, independently reconstructs corrected document
  bytes, verifies the complete 1,463-file legacy-tree snapshot, and reports zero
  corrections and zero completed second passes. It also pins the ignored PDF by
  path, size, and hash, enforces the 1–1,280 page partition, and rejects any
  image/correction source page outside its owning document.
- Two fresh temporary builds were byte-identical. Focused tests passed:
  `10 passed, 26 subtests passed`. Both scripts also support an explicit
  `--zero-corrections` baseline mode, and temporary builds refuse to replace
  an existing directory.
- Source comparison corrected twelve chapter-start raw boundaries and moved
  eight extracted opener-image ownership records. The rebuilt 29 documents
  still concatenate byte-for-byte to the immutable monolith. Every one of the
  1,444 `_page_N_` assets now maps to PDF page `N + 1` inside its owner's source
  interval.
- The earlier official online candidate is a later Fourth printing and is not
  used as transcription evidence. The active witness matches the legacy First
  printing. Its pdftk/iText container is documented as reprocessed rather than
  claimed to be an untouched publisher master.
- Passing commands after the final Foundation changes:
  `uv run pytest -q goal-5/tests/test_foundation.py`,
  `uv run python goal-5/build.py`, and
  `uv run python goal-5/validate.py`.
