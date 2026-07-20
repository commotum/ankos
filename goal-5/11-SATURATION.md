# 11-SATURATION

Status: COMPLETE

## Current Facts

- The authoritative source is the 1,280-page PDF with SHA-256
  `a3cc5dd60e12d6b563aee86ea31a15b03f9cddfd4869b8f965d3a11bbc61a0d6`.
- The candidate corpus contains exactly 29 canonical Markdown documents.
  Stage 9 closed all 29 rotated technical passes. Round 1 then found and
  repaired nine N12 defects and one N06 table defect; two apparent N06
  formula/subscript findings were disproved at high resolution and rolled back.
  The affected N06 and N12 technical/document passes were restarted and
  accepted. Round 2 subsequently repeated all three complete lanes from zero
  review credit and found no new discrepancy or ambiguity.
- The current deterministic zero-credit preflight is
  `/tmp/g5-stage11-round2-final-preflight-20260720-a1`. It was generated only
  after Round 1 closed and freezes 29
  documents, all 1,280 source pages, 28 detector families, 812
  document-detector runs, and 35,479 occurrence/inventory candidates. Its
  15-member manifest SHA-256 is
  `941ef2ef335512872de16a3d7f0b425affc8b00afc63f96e31dbbefe39553ecc`;
  root reproduced semantic verification and two strict replays, including all
  20 mutation rejections and the explicit closed-Stage-9 and accepted-Round-1
  gates. Every one of its 37,603 work rows remains `UNREVIEWED` with `NONE`
  review credit and no inherited Round 1 disposition.
- The preflight includes nine repeated-word candidates, 26 trailing-whitespace
  lines, 1,314 live image references, and explicit zero-hit detector runs.
  These are candidates and denominators, never defects or inherited clean
  verdicts; every row must receive a fresh source-backed or
  serialization-backed disposition in each credited round.
- Stage 10 is complete: its Index, Colophon, and reopened figure work is
  integrated; the final visual and `INDEX` technical closures are sealed; all
  29 coverage rows are `YES/YES`; and the cumulative checks pass.

## Big-Picture Objective

Find and eliminate any residual OCR, transcription, ordering, or Markdown
serialization defect in the assembled book. After the last correction, repeat
the entire detector and 29-document verification round and require that fresh
round to find nothing new.

## Execution Plan

1. Wait for Stage 9 to close, then freeze the final 29 target hashes,
   correction ledger, builder, source ranges, PDF hash, and detector versions.
2. Generate exhaustive, verdict-free detector ledgers for OCR substitutions,
   improbable tokens, repeated words, broken joins/splits, punctuation and
   Unicode anomalies, malformed Markdown/HTML/math/code, heading and caption
   anomalies, page references, Index forms, links, and image references.
3. Source-disposition every detector row. A parser, dictionary, extraction,
   prior report, or model judgment may route attention but cannot decide the
   printed transcription.
4. Assign wholly fresh document-atomic reviewers three balanced lanes:
   - Lane 1: `CH12`, `CH06`, `CH03`, `CH04`, `CH02`, `N07`, `N05`, `N03`,
     `PUBLICATION_AND_CONTENTS`, `N01`.
   - Lane 2: `CH09`, `N12`, `CH07`, `CH05`, `N10`, `N08`, `CH01`, `N02`,
     `PREFACE`, `COLOPHON`.
   - Lane 3: `CH10`, `CH11`, `CH08`, `INDEX`, `N09`, `N04`, `N06`, `N11`,
     `GENERAL_NOTES`.
5. In each lane compare every assigned source page sequentially with the final
   Markdown, including unchanged context around prior repairs. Record explicit
   page, detector, finding, ambiguity, and document-completion receipts.
6. Apply every source-backed correction through guarded corrections, rebuild,
   and restart the owning document's Stage 9/10 and Stage 11 coverage whenever
   the changed content invalidates it.
7. After the last repair, discard prior verdicts and repeat all detectors and
   the complete 29-document sequential pass against a newly frozen target.

## No-Cheating Checks

- Preflight output grants no review credit and may not carry a clean verdict
  into either saturation round.
- Detector-only review does not count as the sequential source pass.
- Existing Stage 3–10 packets may identify risk but cannot replace fresh page
  comparison or supply inherited verdicts.
- Each lane must prove exact page and document denominators, monotonic review,
  current target hashes, zero unreviewed detector rows, and zero missing or
  duplicated receipts.
- A correction invalidates the affected target hash and forces the required
  document restart; a verifier must reject stale hashes, omitted rows,
  duplicated rows, false clean statuses, and incomplete page coverage.
- Repaired output never becomes build input, and the immutable legacy corpus
  must retain its protected hash.

## Completion Requirements

- Every generated detector row has a source-backed or serialization-backed
  disposition with zero pending ambiguity.
- All 29 documents have a fresh complete sequential verification pass against
  one stable target.
- A second complete detector and 29-document round after the last correction
  finds zero new discrepancy.
- `unresolved.md` contains zero author-text transcription ambiguity.
- Build, validator, coverage joins, correction guards, links, images, Markdown
  structure/rendering, cumulative tests, legacy integrity, and
  `git diff --check` all pass.

## Stage Results

Complete. Round 1 found ten source-backed defects, all of which were guarded,
rebuilt, and re-reviewed. The required post-correction Round 2 then closed all
29 documents, all 1,280 PDF pages, 38,168 target lines, 812 detector runs,
35,479 candidates, and 1,314 live image references with zero finding and zero
ambiguity. Detector preflights supplied denominators only and received no
review credit in either round.

### Entry Freeze and Round 1 Launch

- The entry target contained 3,622,710 bytes and 38,182 logical LF-terminated
  lines. Its ordered target-record SHA-256 is
  `d872859e9a6ef6dde11307eb40f141a5e579a2853ede44ab430c1365dda27063`;
  the preflight target-corpus SHA-256 is
  `3d705f4fae1371c5b0fee5f201677ba54934d3ebeef5dbc37d924e04a5fc5494`.
- Root independently replayed the post-Stage-9 preflight from live repository
  bytes. It reproduces 29 documents, 1,280 pages, three lanes, 28 detector
  families, 812 document-detector runs, 35,481 candidates, the 16-member
  manifest, and all 15 mutation rejections.
- Three wholly fresh, fork-free agent reviewers started Round 1 with no
  inherited verdicts: Lane 1 at
  `/tmp/g5-stage11-round1-lane1-20260719-a1` (10 documents, 430 pages, 280
  detector runs, 5,271 candidates); Lane 2 at
  `/tmp/g5-stage11-round1-lane2-20260719-a1` (10 documents, 425 pages, 280
  detector runs, 6,354 candidates); and Lane 3 at
  `/tmp/g5-stage11-round1-lane3-20260719-a1` (nine documents, 425 pages, 252
  detector runs, 23,856 candidates).
- Round 1 is active. Root accepted ten source-backed defects and repaired them:
  nine in N12 and one in N06. Two apparent N06 findings were disproved with
  fresh high-resolution source evidence and rolled back. Every pre-repair N12
  and N06 verdict is invalid, and all lane seals must bind to the combined
  repair freeze before receiving current credit.

### Round 1 Finding and Post-Repair Freeze

- `L2-N12-001` was found independently on PDF page 1154 (printed page 1138),
  target line 234. The book prints the Wolfram Language symbol
  `$IterationLimit` in technical type beside `TimeConstraint`; the target had
  a literal backslash before the opening inline-code delimiter.
- Root opened the 216-DPI source page at original detail and reproduced the
  finding. Guard `G5-C-4600` now consumes raw preimage `\$IterationLimit` at
  byte 3,000,685 and emits `` `$IterationLimit` ``.
- The complete pre-repair N12 restart then reviewed all 76 PDF pages, all 1,857
  target lines, 2,470 N12 candidates across 28 runs, all 53 assets, and every
  one of 83 high-risk blank boundaries. It found eight additional defects:
  six source-continuous prose joins (`L2-N12-002` through `005`, `007`, and
  `008`), one tight-list boundary (`006`), and the false blank inside the
  two-line `Apply[Times, Map[…]]` display (`009`). Four findings extend
  overlapping existing guards and four add `G5-C-4831` through `G5-C-4834`.
  The PDF page 1195 ending “martian soil chemistry” genuinely has no printed
  period and remains source-faithful.
- Root independently opened the original-detail source leaves for PDF pages
  1161, 1174, 1179, 1180, 1188, 1189, and 1192 and visually reproduced all
  eight boundary/display findings before accepting their guarded repairs.
- The combined N12 target is 398,142 bytes, 1,843 LF, and SHA-256
  `c999ad62007b5ccc16ca17509e11863dd61b5b996250b955c06e7dede9932e8d`.
- All pre-repair N12 receipts have `NONE_PRE_REPAIR_EVIDENCE_ONLY` credit. Its
  wholly fresh technical closure and complete 76-page Round 1 document restart
  against the combined bytes are accepted at `0/0`. The Lane 2 reviewer may
  retain firsthand work for its nine unchanged documents only after proving
  their identities and regenerating every corpus-bound receipt against the
  final Stage 11 packet.
- Lane 1 independently proved all ten assigned document hashes, byte counts,
  and LF counts unchanged, regenerated all receipts against the post-repair
  freeze, and closed 430 pages, 280 detector runs, and 5,271 candidates with
  zero findings or ambiguities. Its 18 resealed real-delta mutations are all
  rejected. Root replayed the final strict verifier twice and reproduced
  manifest SHA-256
  `959938268f5438e3349d7df2e7ba18b54c2c67e335eb585a92b4b9c0ae0d49c1`
  and seal SHA-256
  `211270e1b4c835e71f96a602604dbbb1ed0ab8d4f500d15315b733d942d02031`.
  This is a valid historical seal against the N12-only repair freeze, but the
  later combined repairs require the same reviewer to prove all ten Lane 1
  document identities and regenerate its global bindings before acceptance.
- The same reviewer completed that final rebind at
  `/tmp/g5-stage11-round1-lane1-final-rebind-20260720-a1`. Exact identity and
  context proofs preserve 430 firsthand page reviews while all 5,271 candidate
  and 280 detector-run receipts are regenerated against the final preflight.
  Root replayed all 23 real-delta mutation rejections and two final pristine
  verifiers. Manifest SHA-256 is
  `331b927d1d39f4dd29691f799c8f3a9aef8f880ca76801e9fb558b51e86d8b0f`;
  seal SHA-256 is
  `046fefe545ea7f4b8325307dee6b6db133d03c98530b25ff430e574a958c720f`.

### N06 Findings and Combined Freeze

- Lane 3 initially treated the PDF page 969 formula as having an inner
  exponent and root integrated that interpretation. The mandatory fresh N06
  source-first restart disproved it: a 600-DPI crop and independent text layer
  both show two closing parentheses before the exponent. `G5-C-1292` was
  restored to the source-printed outer grouping
  `1/2 (1 - (1 - 2 p))^(2^DigitCount[t, 2, 1])`.
- The same restart confirmed that PDF page 976 prints plain
  `$h \le 2r h_t$`, not an invented `$h_x` form. These two apparent findings
  are explicitly regression-pinned source oddities and do not count among the
  ten accepted discrepancies.
- Fresh 1,200-DPI review of PDF page 967 found one real N06 defect: the target
  period-ratio table had invented an `n = 31` / `ratio = 1` column. The source
  has exactly ten entries (`11, 13, 19, 25, 27, 29, 37, 41, 43, 53`).
  `G5-C-1262` now reproduces that table exactly.
- N06 is 85,452 bytes, 666 LF, and SHA-256
  `23b589b5e711b93d2e4eb85f78c36e6c39f5b418f73a72bd79697fe6575f5a93`.
  Its previous Lane 3 seal is invalid because it accepted the wrong formula
  grouping and pre-fix table; a full fresh 20-page restart is required.
- The combined 1,638-file tree has length-prefixed SHA-256
  `a682973172db962f41e407f399090a7a0245a47163c550cdf35268054e331216`.
  The correction ledger contains 4,834 rows and has SHA-256
  `0206a1f4e109293ef348d7435b075eb1a9a18a80523dcbde0cc11d25e23bb509`.
  Validation passes, and the complete suite passes 304 tests and 6,185
  subtests.
- The final zero-credit Round 1 preflight at
  `/tmp/g5-stage11-round1-final-preflight-20260720-a1` covers 29 documents,
  1,280 pages, 812 detector runs, and 35,479 candidates (Lane 1: 5,271; Lane 2:
  6,352; Lane 3: 23,856). Its manifest SHA-256 is
  `25616b366b8f48a981d15eb4d6b3e4fdecd06b0d0255084a609cce15d8571884`,
  target-corpus SHA-256 is
  `3f8a39b721b6f407201bf3ea442cc716ec843094a6ea2adec2630344f425c98e`,
  and target-record SHA-256 is
  `974aca4828f9c58bad009bead3b13e05402001706be2d7c615a1342fc8408cc1`.
  Semantic verification, two root replays, and all 16 verifier mutations pass.
  Its Stage 9 gate is `SATISFIED_BEFORE_GENERATION`; the packet remains
  deliberately zero-credit because only lane review receipts can grant review
  credit.
- The replacement N06 technical packet closes 6,348 source rows and 21,934
  target rows; root rejected 38/38 real-file mutations and replayed its seal.
  The replacement N12 technical packet closes 387,693 JSONL rows plus all 76
  pages and 53 assets; after root exposed and required repair of a manifest
  self-reference, its deterministic suite rejected 32/32 mutations and two
  root pristine replays passed. Stage 9 is complete across all 29 documents.
- The same Lane 2 reviewer then bound its nine exact-identity-proven documents
  and 349 firsthand pages to the accepted fresh 76-page N12 restart at
  `/tmp/g5-stage11-round1-lane2-final-rebind-20260720-a1`. Root replayed all
  49 meaningful resealed mutations and two pristine verifiers over 10
  documents, 425 pages, 6,352 candidates, 280 runs, and 467 assets at `0/0`.
  Manifest SHA-256 is
  `436d87633f27fca65921eb8846556eadd2ff9070a4a5a2cb8e39342c4a9f593d`;
  seal SHA-256 is
  `eb801bc2e030dba620db96ecf8e0cf326332e4b3cae12ce76e5d6a58b749e990`.
- Lane 3 performed a new source-first N06 review from empty verdict-bearing
  directories, covering all 20 pages, 646 N06 candidates, 28 runs, and 42
  assets. It then combined that work with exact context/byte proofs for the
  other eight documents' 405 firsthand pages at
  `/tmp/g5-stage11-round1-lane3-final-restart-20260720-b1`. Root replayed all
  35 resealed mutations and two pristine verifiers over 9 documents, 425
  pages, 23,856 candidates, 252 runs, and 379 assets at `0/0`. Manifest
  SHA-256 is
  `957ff78c8dbbacac807ca437f6bff056e998b56651dcdc7cca9bd94c3b00ae0e`;
  seal SHA-256 is
  `7f6353dfe87af1b6fc5a2c0e9af7985a747c072bec8ec6c3860a6e98ddd9183f`.
- Round 1 is accepted across all 29 documents, 1,280 pages, 812 detector runs,
  and 35,479 candidates with zero finding and zero ambiguity. The required
  next gate is a wholly fresh Round 2 whose reviewers inherit none of these
  dispositions.

### Round 2 Clean Closure

- Lane 1 closed at
  `/tmp/g5-stage11-round2-lane1-fresh-20260720-a1`: 10 documents, 430
  pages, 6,551 target lines, 5,271 candidates, 280 detector runs, and 468
  live image references at `0/0`. Root replayed all 14 real mutations and two
  complete strict verifiers, each regenerating 860 text extractions and 430
  source renders. Manifest SHA-256 is
  `958a2bf4d3d7a79b307a55f3b306f7cbec3ad91adb677e75bfec55f028ea62c5`;
  seal SHA-256 is
  `2b0c3b91ca334c8eb5315d12a1ffa00013062f995f4d3bd56afb705a7a7ab6f8`.
- Lane 2 closed at
  `/tmp/g5-stage11-round2-lane2-fresh-20260720-a1`: 10 documents, 425
  pages, 7,336 target lines, 6,352 candidates, 280 detector runs, 467 live
  image references, and the exact nine zero-text pages at `0/0`. Root replayed
  all nine real mutations and two complete strict verifiers, each regenerating
  850 text extractions and 425 source renders. The final root-resealed manifest
  SHA-256 is
  `8adbe6e5fc1487678ad0489be3ed6955dddb9bf434ee7add5af944951a92e5df`;
  receipt SHA-256 is
  `aa17cb25db783a1afc65ad723d9cb97c09b7a9cd00b5bdab1ee2f49ba3541773`;
  seal SHA-256 is
  `070515f320f8bbea570cd7fefc7bafbc5a93df6349426fb33e71cfbff03a9ad7`.
- Lane 3 was copied from its completed review into the exact clean packet
  `/tmp/g5-stage11-round2-lane3-final-20260720-b1` after root rejected
  unmanifested scratch/cache files in the initial packet. It closes nine
  documents, 425 pages, 24,281 target lines, 23,856 candidates, 252 detector
  runs, 379 live image references, all 17,737 Index receipts, and all 20 N06
  page receipts at `0/0`. All 15 real mutation/topology cases were rejected;
  root reproduced two strict verifiers; and an independent replay regenerated
  425 raw, layout, bbox, and 300-DPI render artifacts with zero mismatch.
  Manifest SHA-256 is
  `7e17e9264c5f951fb95495e38f483abad86e7ea99bd674a4d7be2b02949915d2`;
  receipt SHA-256 is
  `01a96ee07bfb99b1f33eb2afa3b1fd41e496fbfd4088f8c82805e9a25bf5f94c`;
  seal SHA-256 is
  `98978e6961ea45e93d3b69366e681734e25a82990d7eaf15799da485f45fa0a8`.
- All three final packets have exact member inventories with no symlink,
  hardlink, cache, work, special, missing, or unmanifested member. Their
  aggregate is exactly 29 documents, 1,280 pages, 38,168 target lines, 812
  detector runs, 35,479 candidates, and 1,314 live references. The stable
  author-text corpus remains 3,622,684 bytes with concatenated SHA-256
  `ec7f22f801d157076d33446f2fb5ee01dadaa6b18f3e89d0a123acc0000f2725`.
  No Round 2 correction or unresolved item was created.

### Credited Round Matrix

Active rows grant no credit. A lane is accepted only after all assigned pages,
documents, detector runs, and candidates close against one live target freeze;
root must reproduce the strict verifier, mutation suite, seal, and member
hashes.

| Round | Lane | Fresh packet | Documents/pages | Detector runs/candidates | Root replay | Finding/ambiguity | State |
|---|---|---|---:|---:|---|---|---|
| 1 | 1 | `/tmp/g5-stage11-round1-lane1-final-rebind-20260720-a1` | 10/430 | 280/5,271 | PASS | 0/0 | ACCEPTED |
| 1 | 2 | `/tmp/g5-stage11-round1-lane2-final-rebind-20260720-a1` | 10/425 | 280/6,352 | PASS | 0/0 | ACCEPTED |
| 1 | 3 | `/tmp/g5-stage11-round1-lane3-final-restart-20260720-b1` | 9/425 | 252/23,856 | PASS | 0/0 | ACCEPTED |
| 2 | 1 | `/tmp/g5-stage11-round2-lane1-fresh-20260720-a1` | 10/430 | 280/5,271 | PASS | 0/0 | ACCEPTED |
| 2 | 2 | `/tmp/g5-stage11-round2-lane2-fresh-20260720-a1` | 10/425 | 280/6,352 | PASS | 0/0 | ACCEPTED |
| 2 | 3 | `/tmp/g5-stage11-round2-lane3-final-20260720-b1` | 9/425 | 252/23,856 | PASS | 0/0 | ACCEPTED |
