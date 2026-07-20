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

## Combined Rotated-Closure Matrix

`W1` is `/tmp/g5-stage9-rotated-closer-w1-20260719-a1`; `W2` is
`/tmp/g5-stage9-rotated-closer-w2-20260719-a1`; and `W3` is
`/tmp/g5-stage9-rotated-closer-w3-20260719-a1`. A SHA below is the SHA-256 of
the document seal or sealed document manifest that root replayed. `0/0` means
zero finding and zero ambiguity. Active and queued rows grant no credit.

| Document | Fresh closure packet | Sealed artifact SHA-256 | Root replay | Finding/ambiguity |
|---|---|---|---|---|
| `PUBLICATION_AND_CONTENTS` | `W1` | `bb825f106b14e800ebb619178ed64df0b9d35fdddb836d37b5836a49cbb451a0` | PASS | 0/0 |
| `PREFACE` | `W2/final/PREFACE` | `4ef585fbe7a7b9629aa50c54638ef4b9c24193d535e774916533a363c74a13c8` | PASS | 0/0 |
| `CH01` | `W2/final/CH01` | `7e03ef6598df79764da8aebb4da0bff84a21e7ece9255491ae15adef14d5053c` | PASS | 0/0 |
| `CH02` | `W2/final/CH02` | `2f99b7cd0df46e3acd99f2394d61588ade1f1e16a2b09585caada13c32af3e30` | PASS | 0/0 |
| `CH03` | `W2/final/CH03` | `79ad5f2fa1811fd2657b9c16eaefa1f0bb566deed30cbfedb57015b86f9d2b1e` | PASS | 0/0 |
| `CH04` | `W3` | `71dee26c9c142a8aa008b20326b3afe7099c829e7b49b05a8f50a5460066fee4` | PASS | 0/0 |
| `CH05` | queued | — | — | — |
| `CH06` | `W1` | `39a013bb69b73f7614caafae482edb27372b4757ed67890d2b28c3bfa8a674d0` | PASS | 0/0 |
| `CH07` | `/tmp/g5-stage9-ch07-rotated-closer-w3-20260719-a1` | `7d97487f4023363349fe32ffb24367a220d506b1837ee6a89a475833b3c5885d` | PASS | 0/0 |
| `CH08` | `/tmp/g5-stage9-ch08-rotated-closer-w2-20260719-a1` | `55e3572553f06057559cf8ca9a76ce89a2268a4d3f7413e0eee1d5b0f65be76a` | PASS | 0/0 |
| `CH09` | `W1` | `39a013bb69b73f7614caafae482edb27372b4757ed67890d2b28c3bfa8a674d0` | PASS | 0/0 |
| `CH10` | `W3` | `6d8c59dd79a97d89fd48d7cc06ee560a57071882a7a35aae71ac3cf8e81dc397` | PASS | 0/0 |
| `CH11` | `/tmp/g5-stage9-ch11-rotated-closer-w2-20260719-a1` | `099b7cf7c74430b792184c71ce81316454b11df1181c67c9c312846cc642ac36` | PASS | 0/0 |
| `CH12` | `W1` | `85f7a08cadfbe0dbe8c29a5f86eef7b4a1f2e2c195599c467bf64d7b156577f0` | PASS | 0/0 |
| `GENERAL_NOTES` | `/tmp/g5-stage9-rotated-closer-w3-general-notes-20260719-a1` | `91f484f58a2888db965252d09b9dcf784456ff326d3cb790c103788b06f5cbdb` | PASS | 0/0 |
| `N01` | `W2/final/N01` | `89071c64d3723fde0ca050e8e64247bd0962d7469b3540195277967bc4748d3e` | PASS | 0/0 |
| `N02` | `W1` | `0932cac622e3d8774bb4e1115834e1d081c6aa45629ff49cbb0b6197b6df9b13` | PASS | 0/0 |
| `N03` | `/tmp/g5-stage9-rotated-closer-w3-n03-20260719-a1` | `e4a7961a409a17a37bc6907b835c1101bfdf64584e63e789c3931be23420b67a` | PASS | 0/0 |
| `N04` | `/tmp/g5-stage9-rotated-closer-w3-n04-20260719-a1` | `f59e12fb4558731d6307f11693dda5e85e5adbe0b4401dc56c5d4d697585d679` | PASS | 0/0 |
| `N05` | `W1` | `3711d31d82a13e3807610410f27fda2f005cec77256f75c6c33d6b90b39f905d` | PASS | 0/0 |
| `N06` | queued | — | — | — |
| `N07` | `W1` | `f1ae8c8ec6fd437b9ced37ffb763f3e5662e2b326266778354b1b85de80dc94b` | PASS | 0/0 |
| `N08` | `/tmp/g5-stage9-rotated-closer-w3-n08-20260719-a1` | `2ae7a4ddbfd7e84cce29d402a2916e8457eace84cd1e03ac55d71063ba9ba249` | PASS | 0/0 |
| `N09` | `W1` | `fccbe7c6891a6085440c1765f80b8a813ee5a4a41308fde243027181a93c0651` | PASS | 0/0 |
| `N10` | `/tmp/g5-stage9-rotated-closer-w3-n10-20260719-b1` | `1284462b39247358c7f0be3c8573a058a4bd9b82f54238d5408894edb0bd29d8` | PASS | 0/0 |
| `N11` | `W1` | `1b140d7caf36fcfcc257079c80bc646ab835a5cfd02502dcf16582403c2c2fe6` | PASS | 0/0 |
| `N12` | `/tmp/g5-stage9-rotated-n12-closer-w1-20260719-a1` | active | — | — |
| `INDEX` | `/tmp/g5-stage9-rotated-closer-w3-index-20260719-a1` | `2d2736678d8f659802d7d2ad7bb22b2dc0abe7f72a7cf33a18b427993fc0c9be` | PASS | 0/0 |
| `COLOPHON` | `W2/final/COLOPHON` | `63e8991a2cdd4e59d7983e0d9ce3c6d7f0953e514da81b255046ef3fa64089f9` | PASS | 0/0 |

## Current Gate

The target and source freezes and the integrated first pass are complete.
Fresh rotated closers have formally sealed 26 of the 29 documents with zero
finding and zero ambiguity: `PUBLICATION_AND_CONTENTS`, `PREFACE`, `CH01`,
`CH02`, `CH03`, `CH04`, `CH06`, `CH07`, `CH08`, `CH09`, `CH10`, `CH11`, `CH12`,
`GENERAL_NOTES`, `N01`,
`N02`, `N03`, `N04`, `N05`, `N07`, `N08`, `N09`, `N10`, `N11`, `INDEX`, and
`COLOPHON`. Root
independently replayed the corresponding baseline verifiers, mutation suites,
seals, and member hashes before accepting them. The accepted N10 packet closes
12,303 source-ledger and 46,658 target-ledger rows; all 30 state-changing
mutations are rejected, both pristine verifier runs pass, and its seal SHA-256
is `1284462b39247358c7f0be3c8573a058a4bd9b82f54238d5408894edb0bd29d8`.
The accepted N04 packet closes 10,013 source-ledger and 31,369 target-ledger
rows; all 30 state-changing mutations are rejected, both pristine verifier
runs pass, and its seal SHA-256 is
`f59e12fb4558731d6307f11693dda5e85e5adbe0b4401dc56c5d4d697585d679`.
The accepted CH11 packet closes 7,510 source-ledger and 610 target-ledger rows,
including 17,041 exact lexical links and 296 custom-font visual tokens. All 50
state-changing mutations are rejected, two strict repository-root replays
pass, all 750 manifest members match, and its seal SHA-256 is
`099b7cf7c74430b792184c71ce81316454b11df1181c67c9c312846cc642ac36`.
The accepted N08 packet closes 4,372 source-ledger and 27,054 target-ledger
rows. All 26 pages, 168 crops, 12 target assets, and 33 extracted source images
were individually reviewed; all 30 state-changing mutations are rejected,
both pristine runs pass, and its seal SHA-256 is
`2ae7a4ddbfd7e84cce29d402a2916e8457eace84cd1e03ac55d71063ba9ba249`.
The accepted CH08 packet closes 4,544 source-ledger and 220 target-ledger rows,
including 21,220 lexical links and seven positional visual-only theta/pi
tokens. All 54 state-changing mutations are rejected, two repository-root
strict replays pass, all 2,239 manifest members match, and its seal SHA-256 is
`55e3572553f06057559cf8ca9a76ce89a2268a4d3f7413e0eee1d5b0f65be76a`.
The accepted CH07 packet closes 4,119 source-ledger and 22,936 target-ledger
rows. All 66 pages, 110 crops, 92 target assets, and 310 extracted source
images were individually reviewed; all 30 state-changing mutations are
rejected, two root strict replays pass, and its seal SHA-256 is
`7d97487f4023363349fe32ffb24367a220d506b1837ee6a89a475833b3c5885d`.
Three documents remain across
the three rebalanced chapter/Notes lanes. Stage 9 stays `IN_PROGRESS` until all
29 fresh rotated closures are sealed against the final integrated target.
