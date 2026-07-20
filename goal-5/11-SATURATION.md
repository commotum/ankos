# 11-SATURATION

Status: IN_PROGRESS

## Current Facts

- The authoritative source is the 1,280-page PDF with SHA-256
  `a3cc5dd60e12d6b563aee86ea31a15b03f9cddfd4869b8f965d3a11bbc61a0d6`.
- The candidate corpus contains exactly 29 canonical Markdown documents.
  Stage 9 reached 29 accepted rotated technical closures at entry. Round 1 has
  since found one N12 defect and two N06 defects. Both documents' technical and
  saturation closures are reopened; the other 27 document hashes are
  unchanged.
- The current deterministic zero-credit preflight is
  `/tmp/g5-stage11-postn06-preflight-20260719-a1`. It freezes 29 documents, all
  1,280 source pages, 28 detector families, 812 document-detector runs, and
  35,480 occurrence/inventory candidates. Its 16-member manifest SHA-256 is
  `5e0c9730880e34a455911e8cc3f6ecc4cd36a927ee189362f92fdb9228f6e4ab`;
  root reproduced the strict replay, including all 15 real-delta mutation
  rejections. Every one of its 37,604 work rows remains `UNREVIEWED` with
  `NONE` review credit.
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

In progress. Any detector-generator preflight remains deliberately excluded
from completion credit. Round 1 and its document-atomic fresh reviewer receipts
start only from the post-Stage-9 stable target.

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
- Round 1 is active. Root accepted three source-backed findings and repaired
  them. Every pre-repair N12 and N06 verdict is invalid, and all lane seals must
  bind to the latest post-N06 freeze before receiving current credit.

### Round 1 Finding and Post-Repair Freeze

- `L2-N12-001` was found independently on PDF page 1154 (printed page 1138),
  target line 234. The book prints the Wolfram Language symbol
  `$IterationLimit` in technical type beside `TimeConstraint`; the target had
  a literal backslash before the opening inline-code delimiter.
- Root opened the 216-DPI source page at original detail and reproduced the
  finding. Guard `G5-C-4600` now consumes raw preimage `\$IterationLimit` at
  byte 3,000,685 and emits `` `$IterationLimit` ``. The rebuilt N12 target is
  398,152 bytes, 1,857 LF, and SHA-256
  `90d4ddcb566aae8515b0515221a10b4d7c2d96f353b429e52010cc93222bbdfa`.
  The focused N12 suite passes nine tests and 1,400 subtests.
- A direct comparison of all 29 old and new target records proves N12 is the
  only changed document. The repaired 1,638-file tree has length-prefixed
  SHA-256
  `03c052c18a8d0c274d62a6fd1c8e0d57267ec9714d9be704c9ba19705e19128e`.
- The zero-credit detector packet was regenerated at
  `/tmp/g5-stage11-postfix-preflight-20260719-a1`. It has 35,480 candidates
  (Lane 1: 5,271; Lane 2: 6,353; Lane 3: 23,856), all 812 detector runs, and
  manifest SHA-256
  `dc964d2e5daafc6285e5ce9153c9d359fbee882f541ff19b5ea77f8824911677`;
  strict replay and all 15 mutations pass. Its target-corpus SHA-256 is
  `206efb8c5c8b608150937ad60fa5b609776b325fd6b69d111e1d0f58ce6279c4`.
- All pre-repair N12 receipts have `NONE_PRE_REPAIR_EVIDENCE_ONLY` credit. N12
  must receive a fresh technical closure and a complete 76-page Round 1 restart
  against the new packet. Unchanged-document reviewers may retain firsthand
  page work only after proving their assigned document hashes are identical and
  regenerating every corpus-bound receipt against the new freeze.
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
  later N06 repair requires the same reviewer to prove all ten Lane 1 document
  identities and regenerate its global bindings before current acceptance.

### N06 Findings and Current Freeze

- Lane 3 independently found `S11-PF-00009000` on PDF page 969 (printed 953).
  The target serialized
  `1/2 (1 - (1 - 2 p))^(2^DigitCount[t, 2, 1])`; the printed exponent instead
  applies to the inner `(1 - 2 p)` term, inside the outer subtraction.
- It independently found `S11-PF-00008972` on PDF page 976 (printed 960).
  The target serialized `$h \le 2r h_t$`; the source prints
  `$h_x \le 2r h_t$`. The missing subscript changes the inequality's variable.
- Root opened both 240-DPI source pages at original detail and confirmed the
  findings. `G5-C-1292` now emits the correct grouping, and new source guard
  `G5-C-4831` restores `_x`. N06 is now 85,469 bytes, 666 LF, and SHA-256
  `b66bbd9e04137e3056992b8bdb5e74e40291af09fa3f609f7545a9c246995161`.
  The focused N06/N12 regression gate passes 15 tests and 1,721 subtests.
- A direct comparison of all 29 target records proves N06 is the only document
  changed by this repair. N12 remains 398,152 bytes at SHA-256
  `90d4ddcb566aae8515b0515221a10b4d7c2d96f353b429e52010cc93222bbdfa`.
  The current 1,638-file tree has length-prefixed SHA-256
  `51324abb98d1b34b077680a6d5698811fc2372eb78ff1e2f2d6fbb352aea6077`;
  the correction ledger contains 4,831 rows and has SHA-256
  `778fedcda0cd35e3bdcb1b8b52f20671c99bff85c4bdb10abcd5ae54e5c70a6b`.
- The current zero-credit packet at
  `/tmp/g5-stage11-postn06-preflight-20260719-a1` has manifest SHA-256
  `5e0c9730880e34a455911e8cc3f6ecc4cd36a927ee189362f92fdb9228f6e4ab`,
  target-corpus SHA-256
  `17b757ef2699233ec4c3c05359b42245fb3919e062286ecb3cc2ec2dd3d4678a`,
  and target-record SHA-256
  `ebf0aca5a7deecff4ca8a3f5fc19319b5810b9d0371677582e6cff754d62a381`.
  Strict replay and all 15 mutations pass.
- All pre-repair N06 receipts have zero credit. Lane 3 must repeat all 20 N06
  pages, 646 candidates, and 28 detector runs from scratch. Every lane must
  rebind unchanged-document receipts to this current freeze; N12 still requires
  both its fresh technical closure and Lane 2's complete 76-page restart.

### Credited Round Matrix

Active rows grant no credit. A lane is accepted only after all assigned pages,
documents, detector runs, and candidates close against one live target freeze;
root must reproduce the strict verifier, mutation suite, seal, and member
hashes.

| Round | Lane | Fresh packet | Documents/pages | Detector runs/candidates | Root replay | Finding/ambiguity | State |
|---|---|---|---:|---:|---|---|---|
| 1 | 1 | `/tmp/g5-stage11-round1-lane1-20260719-a1` | 10/430 | 280/5,271 | prior PASS | 0/0 | REBASE REQUIRED; zero current credit |
| 1 | 2 | `/tmp/g5-stage11-round1-lane2-20260719-a1` | 10/425 | 280/6,353 | — | 1/0 | REBASING + N12 RESTART; zero credit |
| 1 | 3 | `/tmp/g5-stage11-round1-lane3-20260719-a1` | 9/425 | 252/23,856 | — | 2/0 | REBASING + N06 RESTART; zero credit |
| 2 | 1 | — | 10/430 | to regenerate | — | — | NOT STARTED |
| 2 | 2 | — | 10/425 | to regenerate | — | — | NOT STARTED |
| 2 | 3 | — | 9/425 | to regenerate | — | — | NOT STARTED |
