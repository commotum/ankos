# 11-CH07-MECHANISMS

Status: **IN PROGRESS**.

## Current Facts

- Stage 10 is terminal at `V000030`, discovery epoch 2.
- The six immutable starting hashes are:
  - `reading-ledger.csv`:
    `e6fcdf7ca4ab1dbaf0f51aa29d4451eef98e15762f9fe22803d2c2121271303d`;
  - `candidate-ledger.jsonl`:
    `8ba1ffba5061a2e115063c6b552b10369e53a3fd3bf4fcb08d3bfcaf7c8bf1c7`;
  - `cross-reference-ledger.csv`:
    `fda975932dade9ffd2b78380d87f27347ef45d32736f53418318b719d117a6fc`;
  - `asset-ledger.csv`:
    `b57d00e4d9bc1cde61d79acf869b3968e5b2e5e871d9938de099d0bb035d8f4e`;
  - `search-rounds.json`:
    `f614cce2bff0e040fca38cd1a82036432d951c2082febfcb9cf0eb86c03ae94d`;
  - `review-history.jsonl`:
    `174f07cf729016aa3e921ce934836b05d11fe806b83fe26af51e43c9f9bd9e34`.
- The starting global state contains 14,311 source units, 3,332 reviewed
  units, 1,250 active blind candidates, 567 routes (272 resolved and 295
  pending), 1,607 physical images of which 688 are screened, and 16 closed
  LOCAL rounds.
- The exact Stage 11 assignment contains 713 pending source units and 194
  pending physical images.
- Five sealed epoch-2 bundles were built and verified normally and under
  optimized Python. The reproducible content-set hashes are:
  - main:
    `346d4da6a8f58c547a66371022de8806d0d55c6b652648c20928fafd53927f28`;
  - Notes:
    `91458ef7c19a113cc438becd33c013328e52346b9c5f57b52525d46759d99735`;
  - pristine paired union:
    `5f084566dfd0fbae8a1323aa5c7d43dda3d6ad1994c0c7d0eaee02d4b704985e`.
- The canonical source hashes are
  `e052f275ea7519f2e8c270f1dd68eac01d123aa3b73355eff5803f02708e542d`
  for the main path and
  `fd8696100529789964578841267bbd841411691d05248840ede6e0b4b7bd69f3`
  for the Notes path.
- No Stage 12 or later source may be opened while this stage is active.

## Updated Assumptions

- Stochastic movement, random initial data, random event selection,
  deterministic intrinsic randomness, and ensemble measurements remain
  distinct.
- A physical interpretation or explanatory application is not a new native
  construction unless the assigned source states an independent state,
  transition, coupling, event-selection, or solution law.
- Aggregation, constraint satisfaction, continuum relations, discrete
  approximations, and observation protocols must retain their native
  directionality, schedule, probability, and stopping semantics.
- Image filenames in this extraction use PDF-page numbers, while route
  literals use the Book's printed-page numbers. In the assigned Chapter 7
  spans the former are 15 greater than the latter. Incoming-route discovery
  therefore uses printed main pages `297..360` and printed Notes pages
  `969..990`, not the superficially similar filename ranges.
- A route whose literal target spans an assigned and an unassigned page is
  not partially resolved. For example, `Compare pages 1029 and 986` remains
  pending until both printed-page targets have been reviewed.
- Blind discovery remains independent of T identifiers, the existing catalog,
  API documents, runtime support, and final family judgments.

## Big Picture Objective

Blindly and exhaustively audit Chapter 7 main text and Chapter 7 Notes for
construction-bearing mechanics, supporting evidence, representations,
observers, applications, source defects, and cross-range obligations.

## Allowed Inputs And Scope

The two disjoint sequential-review assignments are:

| Assignment | Source units | Physical images |
|---|---:|---:|
| `CHAPTERS/07-Mechanisms-in-Programs-and-Nature.md` | 435, `U001577..U002011` | 92 referenced: `A001028..A001040`, `A001042..A001056`, `A001058..A001121` |
| `BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes.md` | 278, `U006592..U006869` | 43 referenced + 59 unreferenced: `A000001..A000018`, `A000661..A000744` |
| **Total** | **713** | **194** |

`A001041` and `A001057` are already Stage 5-owned shared assets and are not
pending Stage 11 work.

Workers may read only their sealed assignment bundle. The coordinator may use
Goal 4 ledgers, schemas, guardrails, tools, and the two assigned source paths.
Goal 1, Goal 2, the existing catalog, API documents, runtime code, and Stage 12
or later Book source remain prohibited.

## Source Coverage

| Assignment | Reviewed units | Screened images | State |
|---|---:|---:|---|
| Chapter 7 main text | 0 / 435 | 0 / 92 | pending |
| Chapter 7 Notes | 0 / 278 | 0 / 102 | pending |
| **Total** | **0 / 713** | **0 / 194** | **pending** |

## Candidate Changes

No Stage 11 candidates have been proposed or applied.

## Search And Evidence Log

No Stage 11 LOCAL search round has begun. Sequential review must be merged
before exact-scope trigger and alias searches are frozen.

## Detailed Implementation Plan

1. Reconfirm the Stage 10 terminal hashes and ordinary/optimized validators.
2. Build and verify two disjoint sealed epoch-2 bundles and one pristine union
   bundle from the exact Stage 11 assignment.
3. Independently review every main-text and Notes unit in canonical order and
   screen every owned image at the required depth.
4. Combine the two completed outputs, verify canonical disjoint coverage, and
   preview/apply exactly one Stage 11 `INITIAL` transaction.
5. Resolve every reachable incoming and within-stage route through a typed
   `ROUTE_RESOLUTION` transaction; preserve outgoing obligations.
6. Freeze and execute an exact paired-scope LOCAL search family, reconcile
   every hit, append any omissions, and rerun it identically to zero semantic
   delta.
7. Run hostile semantic, route, image, and mechanical review; repair findings
   through governed append-only events.
8. Record exact terminal counts, ranges, hashes, commands, and the Stage 12
   handoff here and in `0-plan.md`.

## No-Cheating Checks

- The two workers receive only sanitized sealed bundles for their assigned
  paths and cannot search or resolve routes.
- Candidate IDs, evidence IDs/groups, and route IDs remain worker-local until
  deterministic coordinator allocation.
- Every assigned unit and image must receive a nondefault disposition before
  merge.
- Search begins only after sequential review and uses exactly the paired Stage
  11 paths.
- No T mapping, catalog action, API-fit decision, or final family assignment is
  permitted.

## Completion Requirements

- All 713 assigned units and 194 physical images are dispositioned at the
  required depth.
- Random inputs, stochastic laws, event-selection processes, deterministic
  intrinsic randomness, ensembles, and observation protocols remain
  mechanically distinct.
- Every candidate has complete source-limited evidence and semantic
  fingerprint fields or explicit missing-mechanics boundaries.
- Every reachable incoming and within-stage route is resolved and every
  outgoing route is queued.
- Exact-scope LOCAL search reaches an identical zero-delta rerun.
- Ordinary and optimized validators, frozen specifications, full regression,
  compilation, Markdown, whitespace, and diff checks pass.
- This report and `0-plan.md` contain an exact Stage 12 handoff.

## Stage Results

Pending.
