# 11-SATURATION

Status: IN_PROGRESS

## Current Facts

- The authoritative source is the 1,280-page PDF with SHA-256
  `a3cc5dd60e12d6b563aee86ea31a15b03f9cddfd4869b8f965d3a11bbc61a0d6`.
- The candidate corpus contains exactly 29 canonical Markdown documents.
  Stage 9 is complete: every document has a fresh rotated technical closure,
  all 29 root replays pass with zero finding or ambiguity, and the stable
  target is now eligible for Stage 11 review credit.
- A deterministic read-only preflight was regenerated after Stage 9 closed at
  `/tmp/g5-stage11-preflight-generator-w1-20260719-a1`. It freezes 29
  documents, all 1,280 source pages, 28 detector families, 812 document-detector
  runs, and 35,481 occurrence/inventory candidates. Its 16-member manifest
  SHA-256 is
  `840d992d7d8eb1ca180437391b8a9462ed89c5984bb11a13f609f1f4c3633826`;
  root reproduced the strict replay, including all 15 real-delta mutation
  rejections. Every one of its 37,605 work rows remains `UNREVIEWED` with
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
