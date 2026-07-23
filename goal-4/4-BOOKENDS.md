# 4-BOOKENDS

Status: **IN PROGRESS**.

## Current Facts

- Stages 1–3 are complete and independently signed off.
- The live blind ledgers are still the reproducible initial state:
  14,311 pending source units, 1,607 pending physical images, 0 candidates,
  0 routes, and 0 search rounds.
- Stage 4 owns four canonical documents in manifest order:
  - `FRONT-MATTER/00-Publication-and-Contents.md`;
  - `FRONT-MATTER/01-Preface.md`;
  - `BACK-MATTER/NOTES/00-General-Notes.md`;
  - `BACK-MATTER/Colophon.md`.
- Those paths contain 157 deterministic source units and own 2 physical
  images.
- The stage will be one epoch-1 `INITIAL` review transaction followed by one
  or more epoch-1 `LOCAL` search transactions and any locally resolvable route
  transactions.

## Updated Assumptions

- Bookends are likely to contain more framing, publication, navigation, and
  historical material than complete mechanics, but that is only a workload
  expectation. It does not authorize bulk `NO_CONSTRUCTION` dispositions.
- Printed contents, Preface prose, General Notes, colophon text, and both
  images must still be read or screened individually.
- A source unit that may specify mechanics is captured provisionally rather
  than excluded to preserve a preferred count.
- Page, section, chapter, Notes, or alias references that could lead to
  mechanics are explicit routes; memory is not a substitute for the route
  ledger.

## Big Picture Objective

Blindly screen the publication/contents material, Preface, General Notes, and
Colophon for construction-bearing material while establishing the exact
sequential-review, image-screening, LOCAL-search, and route-closure discipline
that later chapter stages will reuse.

## Allowed Inputs And Scope

Allowed:

- Goal 4 plan, loop, guardrails, corpus map, Stage 3 schemas/tools, and the
  empty blind ledgers;
- only the four assigned canonical Book documents, their 157 source units,
  and their 2 owned images;
- deterministic LOCAL searches over those four paths after sequential review.

Forbidden during this stage:

- current catalog mappings or identifiers;
- prior type conclusions;
- API-fit, runtime-support, or executor conclusions;
- unassigned Book ranges except through a queued route that a later owning
  stage will resolve.

All writes remain under `goal-4/`; temporary sealed review material may be
created under `/tmp`.

## Source Coverage

Starting coverage:

| Obligation | Assigned | Completed |
|---|---:|---:|
| Source units | 157 | 0 |
| Physical images | 2 | 0 |
| LOCAL search scopes | 4 paths | 0 |
| Search hits | 0 | 0 |
| Within-stage routes | 0 | 0 |
| Cross-range routes | 0 | 0 |

Each source unit will receive one primary reading disposition, explicit source
status, secondary roles, concise evidence statement, epoch/stage/reviewer
metadata, and exact candidate/route links. Each image will receive an explicit
visual role, risk flags, source status, inspection depth, evidence statement,
and exact links.

## Candidate Changes

No candidate has been created. Any Stage 4 discovery will use worker-local
`W####` identities in the sealed review output and will receive global
`B####` identities only in the coordinator preview/apply transaction.

## Search And Evidence Log

No Stage 4 search has run. LOCAL queries begin only after all 157 units have
been read and both images screened. Query specifications, exact result IDs,
hit dispositions, digests, vocabulary deltas, and semantic changes will be
recorded here after execution.

## Detailed Implementation Plan

1. Build and verify one sealed epoch-1 Stage 4 bundle for all four paths.
2. Prepare the nonsemantic 157-row/2-asset review worksheet.
3. Read every source unit in canonical order and fill only source-grounded
   dispositions, roles, links, evidence, and uncertainties.
4. Screen both images; use original resolution and checked transcription when
   the risk contract requires them.
5. Complete provisional candidate fingerprints and pending route records.
6. Verify the completed bundle, preview the `INITIAL` merge, then apply it.
7. Execute frozen Stage 4 LOCAL query families, disposition every hit, and
   append search/evidence changes atomically until the local vocabulary and
   semantic delta close.
8. Resolve every Stage 4 `WITHIN_STAGE` route; leave legitimate
   `CROSS_RANGE` routes pending for their owning stages.
9. Run ordinary and optimized Stage 4 gates, mutation/self-tests, source hash
   checks, and diff/scope checks.
10. Record results here and fold the exact next Stage 5 state into
    `0-plan.md`.

## No-Cheating Checks

- Sequential review precedes all construction searches.
- The worksheet supplies no semantic defaults.
- Every row and asset retains its hash-bound assignment identity.
- Candidate and route IDs are allocated only by the coordinator.
- Blind outputs are scanned recursively for reconciliation/API/runtime
  leakage.
- LOCAL query scopes must cover exactly the four reviewed paths for epoch 1.
- A green validator does not substitute for reading each unit and visually
  screening each image.

## Completion Requirements

- All 157 source units are individually reviewed.
- Both physical images are visually screened and risk requirements are
  satisfied.
- Every source-grounded candidate has complete provisional evidence and
  fingerprint fields.
- Every relevant reference is resolved locally or queued as a typed
  cross-range route.
- Every LOCAL hit has a final blind disposition and the Stage 4 LOCAL scope is
  exact.
- No Stage 4 `WITHIN_STAGE` route remains pending.
- `validate_audit.py --require-stage 4` passes in ordinary and optimized
  Python.

## Stage Results

In progress. The exact commands, transaction IDs, counts, searches, candidate
changes, routes, findings, and verification outcomes will be added as work
completes.

