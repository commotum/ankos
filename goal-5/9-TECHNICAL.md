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

## Target Inventory Freeze

The sealed read-only target freeze at
`/tmp/g5-stage9-freeze-20260718-a1` has inventory SHA-256
`20af574b2db81a8789f82516440a3b5542c36ae1263ed4e3dd89388b3409e9b0`
and packet seal
`7940b12ffc64f673f4d40c6e6d012be18bc948cd23a3556e41cebc3506a5b98c`.
Root reproduced its manifest and verifier; all ten negative mutation fixtures
pass. All 14,872 status fields are exactly `UNREVIEWED`.

The mutually exclusive explicit stream contains 4,447 objects and 181,634
literal bytes: 485 fenced blocks, 1,099 backtick-code spans, one raw-HTML code
span, 2,707 inline-math spans, 28 display-math objects, 73
parenthesized-math objects, 42 superscript spans, and 12 subscript spans. The
new raw-HTML object is the required 25-byte `<code>ListConvolve</code>` span.
The freeze also records 26 structural tables with 257 data rows, 1,189 review
cells, 1,560 ordered members, and 242 object/cell joins; 1,314 resolved asset
references with 83 provisional technical signals; 3,153 nonoverlapping bare
candidates; and 2,817 exact longest-first operator tokens.

The deterministic provisional three-lane assignment hashes to
`489d43bed6d3dcce381887b25c2c58462cfd559ab2bd7649b69c62cd0e361b1e`
with maximum frozen-axis deviation 7.4853%. It will be rebalanced if the fresh
source or target-detector denominators materially change document loads. The
canonical source-object denominator remains explicitly pending and no region
is reviewed by this freeze.

## Source Inventory Freeze

The fresh all-page source packet at
`/tmp/g5-stage9-source-inventory-20260718-a1` has manifest SHA-256
`f80f45dba99594c3dac4bc57f2c0b27aa7c66c2ca1ea27c2e1502e8b7f16b52d`
and seal SHA-256
`2c1ec46c160b390eacbbd374ceffb4ec1acb15297f41f652402b8a97e131f676`.
Root reproduced its manifest and `verify.py --self-test`; omission, duplicate,
and document-drift mutations are all rejected. Every candidate field is
`UNREVIEWED` and the packet grants zero Stage 9 review credit.

Fresh raw, layout, bbox, XML/font, image-region, and raster evidence covers all
1,280 pages. The canonical denominator is 190,199 XML text runs; 679,281 bbox
words are non-creating crosswalk aids. The packet inventories 134,632
technical/source-only candidates, 56,769 operator/special-glyph rows, 10,304
script candidates, 13,609 aligned data regions, 47,456 technical
font/position clusters, 22,064 hidden/overlap candidates, 8,062 extracted
image regions, and 1,910 raster-derived vector candidates. Exactly 20 pages
are dispositioned as blank at inventory level.

The source-object sequence hashes to
`6667b453f203a82c61ae6b5fcc364dc201045f13d44b369349c07ac8f50508aa`.
Target and source packets use different documented manifest-framing algorithms;
their identical 1,638-file and 158,900,442-byte target-tree totals are the
cross-packet compatibility check, not equality of those framing hashes.

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

The target and source freezes and the integrated first pass are complete.
Fresh rotated closers have formally sealed 11 of the 29 documents with zero
finding and zero ambiguity: `PREFACE`, `CH01`, `CH02`, `CH04`, `CH06`, `CH09`,
`CH10`, `GENERAL_NOTES`, `N01`, `N03`, and `COLOPHON`. Root independently
replayed the corresponding baseline verifiers, mutation suites, seals, and
member hashes before accepting them. Eighteen documents remain; the final
`INDEX` technical closure is active and all other remaining documents continue
in the two chapter/Notes lanes. Stage 9 stays `IN_PROGRESS` until all 29 fresh
rotated closures are sealed against the final integrated target.
