# 9-TECHNICAL

Status: IN_PROGRESS

## Entry State

- Stages 1 through 8 are complete. All chapter and Notes documents have
  `YES/YES` source coverage; validation reports 27 completed second-pass
  documents. `INDEX` and `COLOPHON` remain deliberately open for Stage 10.
- The current correction ledger has 4,534 rows and SHA-256
  `80b89a99dbbd54b73682d07a6ffcb236d5c9c49ee36e23b317fb0305fe6dfbf6`.
- The authoritative 1,280-page PDF has SHA-256
  `a3cc5dd60e12d6b563aee86ea31a15b03f9cddfd4869b8f965d3a11bbc61a0d6`.
- The generated 29-document author-text corpus currently contains 3,568,446
  bytes and 22,075 LF. The final document manifest and every Stage 9 inventory
  will be regenerated and pinned before source review begins.
- Existing per-document technical packets are detector and schema references
  only. Their evidence and verdicts do not count as Stage 9 coverage.

## Frozen Inventory Contract

Stage 9 uses separate exhaustive denominators so nested technical material is
not silently omitted or double-counted:

1. Mutually exclusive syntax-delimited objects: fenced code; backtick and HTML
   code; inline and display math in every supported delimiter form; HTML
   superscript/subscript; and any parsed indented or raw-HTML code.
2. Structural containers: Markdown/HTML/ASCII tables; matrices; truth, rule,
   transition, axiom, theorem, and numeric-sequence tables; with exact row,
   column, cell, and member order.
3. Unmarked target candidates: Wolfram calls, Parts, patterns, slots, rules,
   assignments, relations, identifiers, strings, comments, bare mathematics,
   Greek/special symbols, scripts, numeric sequences, units, coordinates, and
   technical caption/prose lines.
4. Technical asset regions: rule tables, diagrams, matrices, axes, legends,
   formula plates, and other token-bearing image regions. Stage 9 owns token
   fidelity; Stage 10 owns identity, crop, caption, and placement.
5. Source-first candidates from fresh XML/bbox/font geometry and rasters:
   technical text, symbol/size/position clusters, aligned table data,
   technical image regions, hidden/overlapping text, and every source-only
   candidate.
6. Page coverage: every physical PDF page 1 through 1280 receives a source-first
   technical disposition, including pages with zero marked target objects.

Generated inventories must remain `UNREVIEWED`. Inventory code may not assign
source-match or clean verdicts.

## Provisional Target Baseline

The pre-freeze parser currently finds 4,446 explicit syntax objects containing
181,609 bytes: 485 fenced blocks, 1,099 inline-code spans, 2,707 inline-math
spans, 28 display-math objects, 73 parenthesized-math objects, 42 superscript
spans, and 12 subscript spans. It also finds 26 structural table containers
with 257 rows and 1,189 cells. These counts are provisional until the final
byte-interval parser, bare-candidate lane, technical-asset lane, and canonical
source inventory are frozen together.

## Execution

- Pin the PDF, correction ledger, builder, source ranges, all 29 document
  hashes, parser/detector hashes, Poppler version, and complete generated tree.
- Inventory exact UTF-8 byte intervals; prove primary-object non-overlap and
  lossless token reconstruction; preserve parent/member joins for containers.
- Generate one canonical source inventory from fresh XML/bbox geometry. Raw
  and layout extraction are routing aids only and cannot create duplicate
  source objects.
- Build monotonic target-to-page routes from document ranges and fresh token
  anchors; confirm every page transition against rasters. Correction page
  locations and embedded asset filenames are hints rather than proof.
- Freeze counts by document and kind before balancing three document-atomic
  first-pass lanes. Every lane performs both target-to-source and
  source-to-target review.
- Integrate source-backed findings through guarded corrections and restart the
  owning document after every change.
- After the last repair, rotate wholly fresh independent closers across the
  three lanes. Closers regenerate inventories and receive no prior verdict.
- Stage 9 may inventory Index/Colophon now but cannot finally close their
  technical content until Stage 10 stabilizes both documents. Any Stage 10
  change restarts affected Stage 9 coverage.

## Required Evidence and Verification

- Input/toolchain/document manifests and frozen count summary.
- Target object, token, structure, detector-hit, bare-region, table/cell,
  numeric-sequence, equality/operator, delimiter, and technical-asset ledgers.
- Fresh per-page raw/layout/XML/bbox/raster manifests; canonical source-object,
  font/glyph, overlap, and source-only ledgers.
- Exact target/source binding, page-review, finding, ambiguity, correction, and
  restart crosswalks with no pending or generic evidence-free match row.
- Per-lane first-pass and rotated-closure packets plus a combined coverage
  matrix proving every denominator closed.
- Read-only verifier, mutation fixtures, `MANIFEST.sha256`, seal, and concise
  report. Mutations must catch relation, digit, bracket, script, table-order,
  source-omission, page-binding, and document-hash drift.
- Cumulative build/validation/tests, two byte-identical clean builds,
  zero-correction conservation, legacy-hash preservation, and
  `git diff --check` after the final repair.

## Current Gate

Inventory/source-evidence generation is active. No Stage 9 technical region is
yet credited as reviewed, and Stage 9 cannot close before Stage 10 stabilizes
Index and Colophon.
