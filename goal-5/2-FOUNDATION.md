# 2-FOUNDATION

Status: IN_PROGRESS

## Current Facts

- Stage 1 is complete; `goal-4/` is absent and the legacy corpus hash is
  unchanged.
- The raw monolith is 3,780,628 bytes and 22,498 logical lines with SHA-256
  `55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20`.
- The 29 provisional ranges cover every monolith byte and line exactly once,
  and every segment hash matches.
- The image map contains 1,444 ordered references to 1,444 physical JPEGs; each
  live asset hash and referenced monolith line matches.
- `ref/A-New-Kind-of-Science-Repaired/` now contains the generated
  zero-correction baseline: 29 author-text documents, 1,444 JPEGs, and two
  clearly editorial navigation/readme files.
- No complete lawful, readable, edition-identical source is mounted. The
  official NKS Online site is a candidate to re-evaluate, but equivalence,
  complete access, permitted use, and fixed-layout Index evidence are unproven.

## Updated Assumptions

- The provisional 29-range layout is a suitable zero-correction baseline, but
  content-sensitive boundaries remain open until authoritative comparison.
- The monolith, never repaired output, is the only build input.
- A builder that slices 29 byte ranges, applies ordered exact-preimage
  corrections, and copies the mapped images is sufficient.
- A validator needs only check the facts that can make this book build wrong:
  raw drift, range coverage, guarded corrections, coverage rows, output bytes,
  assets, generated navigation, and deterministic reproduction.

## Big Picture Objective

Create the smallest understandable 29-document build and validation workflow,
while leaving the authoritative-source blocker explicit.

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
   document, and `unresolved.md` naming the source acquisition blocker.
4. Add focused tests for raw drift, gaps/overlaps, duplicate output ownership,
   correction preimages, incomplete correction evidence, skipped coverage,
   output mutation, and reproducibility.
5. Produce and validate the zero-correction baseline without describing it as
   a corrected edition.
6. Complete source identity/access/legibility work before marking this stage
   complete or beginning content correction.

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
- Source absence remains an open blocker; tests cannot waive it.

## Completion Requirements

- [ ] A lawful, edition-matched, complete, readable source is documented.
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

IN_PROGRESS. The source-access requirement is the only unmet Stage 2
completion requirement; no author text has been changed or reviewed against an
authoritative source.

- Added `build.py` and `validate.py`, using only the Python standard library.
  Corrections are tied to an absolute monolith byte offset and exact nonempty
  preimage, checked against the original document, rejected on overlap, and
  applied from the end of each document backward.
- Added an empty `corrections.jsonl`, a 29-row `coverage.csv` with both
  passes explicitly `NO`, and `unresolved.md` with the source blocker and
  next acquisition action.
- The zero-correction build produced 29 author-text Markdown files and 1,444
  adjacent JPEGs. Concatenating the 29 files in range order reproduces all
  3,780,628 monolith bytes, including the absent terminal newline.
- The validator accepts exactly the expected 1,475 files, verifies every
  document and image byte, checks the ordered image-reference sequence and
  generated Contents targets, and reports zero corrections and zero completed
  second passes.
- Two fresh temporary builds were byte-identical. Focused tests passed:
  `8 passed, 19 subtests passed`.
- A repository scan found no PDF, EPUB, MOBI, DJVU, CBZ, archive, or relevant
  HTML source; the only HTML file is the unrelated visualization UI at
  `src/ca/viz/static/index.html`.
- The next action is not more pipeline code. It is to authorize or provide a
  complete edition-identical source, including fixed-layout Index evidence,
  then record its identity/location convention and begin sequential comparison.
