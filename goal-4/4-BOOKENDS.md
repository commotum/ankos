# 4-BOOKENDS

Status: **COMPLETE**.

## Current Facts

- Stages 1–3 are complete and independently signed off. Stage 3 was narrowly
  reclosed after this stage exposed an interleaved-evidence allocation case;
  the worker verifier, coordinator mapping, and global traversal now agree.
- The live blind ledgers contain 157 reviewed source units, 2 screened
  physical images, 2 active candidates, 4 pending cross-range routes, and
  2 reproducible LOCAL search rounds.
- Stage 4 owns four canonical documents in manifest order:
  - `FRONT-MATTER/00-Publication-and-Contents.md`;
  - `FRONT-MATTER/01-Preface.md`;
  - `BACK-MATTER/NOTES/00-General-Notes.md`;
  - `BACK-MATTER/Colophon.md`.
- Those paths contain 157 deterministic source units and own 2 physical
  images.
- The stage is represented by one epoch-1 `INITIAL` transaction (`V000001`)
  and two epoch-1 `LOCAL` search transactions (`V000002` and `V000003`).

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
| Source units | 157 | 157 |
| Physical images | 2 | 2 |
| LOCAL search scopes | 4 paths | 4 |
| Search hits | 144 | 144 |
| Within-stage routes | 0 | 0 |
| Cross-range routes queued | 4 | 4 |

Each source unit will receive one primary reading disposition, explicit source
status, secondary roles, concise evidence statement, epoch/stage/reviewer
metadata, and exact candidate/route links. Each image will receive an explicit
visual role, risk flags, source status, inspection depth, evidence statement,
and exact links.

## Candidate Changes

The sealed review proposed two source-grounded candidates and the coordinator
allocated them without reconciliation:

- `B0001`, **Rule 30 cellular automaton preset**:
  discovered at `U004864`, supported by `U004873`, with evidence
  `E000001` and `E000003`. The bookends establish a one-dimensional binary,
  synchronous left/self/right construction, a single-black-cell seed, and
  named Rule 30 identity, but not the exact transition lookup or boundary
  convention.
- `B0002`, **Rule 110 cellular automaton preset**:
  discovered at `U004871`, supported by `U004872` and the original-resolution
  image `A000334`, with evidence `E000002` and `E000004`. The bookends
  establish the named binary construction, repeated-domain initial condition,
  and displayed long evolution, but not the exact transition lookup or
  boundary convention.

The uncaptioned Preface image `A001607` remains an explicitly ambiguous,
decorative cellular-automaton-like representation. It is not candidate
evidence.

## Search And Evidence Log

Search began only after the atomic sequential review completed.

- `S001` froze 9 query families over exactly the four Stage 4 paths, introduced
  42 candidate-derived and guardrail vocabulary terms, and reproduced 72
  query/unit hits. The dispositions were 14 governed candidate/support hits,
  34 control/relationship hits, and 24 exclusions. It added no candidate,
  evidence group, route, row, or asset semantics. Result and rerun digest:
  `d38f0df6f962915286871957dee2beb8adaef779c7c1c1a191b0dc5ffa30e594`.
- `S002` reran the same frozen families over the same exact scope using the
  next append-only query/hit IDs. It reproduced the same 72 semantic
  dispositions and added zero vocabulary, candidates, evidence groups,
  routes, or row/asset changes. Result and rerun digest:
  `0366f2afd221ead88fc17151593578e614846734609e09920d58744740b16660`.

The top-level vocabulary is the exact ordered 42-term replay from `S001`.
Stage 4 does not establish the Stage 18 fixed point.

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

The sealed review bundle was bound to content-set digest
`e53c60b50ac00aa9b1e2eb3bdf0c02c53ba89556a536557a39622993908ac8e7`.
Its completed output contained 157 reading rows, 2 asset rows, 2 candidate
proposals, 4 evidence records/groups, and 4 route proposals.

The coordinator allocated:

- `W0001..W0002` → `B0001..B0002`;
- source/image traversal `WE000001..WE000004` → `E000001..E000004`;
- `WG000001..WG000004` → `G000001..G000004`;
- `WR0001..WR0004` → `R000001..R000004`.

The four routes are legitimate pending `CROSS_RANGE` obligations:

- `R000001`: page 27 Rule 30 transition lookup/boundary;
- `R000002`: page 32 Rule 110 transition/native update;
- `R000003`: page 292 persistent-structure definitions;
- `R000004`: page 29 Rule 30 single-cell evolution/boundary context.

No `WITHIN_STAGE` route exists.

Key commands and results:

```text
python3 goal-4/tools/prepare_review_output.py \
  /tmp/ankos-goal4-stage4-e1-v2 --finalize-declaration
  finalized verified worker output declaration

python3 goal-4/tools/build_worker_bundle.py \
  --verify /tmp/ankos-goal4-stage4-e1-v2 --verify-output
  verified sealed blind-worker bundle and completed output

python3 goal-4/tools/merge_worker_output.py \
  /tmp/ankos-goal4-stage4-e1-v2 --goal-dir goal-4 --apply
  applied V000001: 157 readings, 2 assets, 2 candidates, 4 routes

python3 goal-4/tools/merge_worker_output.py \
  --search-append /tmp/ankos-stage4-search-S001.json \
  --goal-dir goal-4 --apply
  applied V000002 / S001

python3 goal-4/tools/merge_worker_output.py \
  --search-append /tmp/ankos-stage4-search-S002.json \
  --goal-dir goal-4 --apply
  applied V000003 / S002

python3 goal-4/tools/validate_audit.py --goal-dir goal-4 --require-stage 4
python3 -O goal-4/tools/validate_audit.py --goal-dir goal-4 --require-stage 4
  validated: units=14311 reviewed=157 candidates=2 routes=4
  assets=1607 screened=2 rounds=2

python3 goal-4/tools/validate_audit.py --self-test
python3 -O goal-4/tools/validate_audit.py --self-test
  validated the progressed live state and destructive mutation fixtures

uv run --with pytest pytest -q <all seven Goal 4 test modules>
  93 passed (36 coordinator tests plus 57 remaining tests)
```

The interleaved-evidence regression proves that candidate-grouped storage can
carry globally source-ordered evidence (`B0001`: `E000001`,`E000003`;
`B0002`: `E000002`,`E000004`) through worker verification, preview, apply,
history replay, and global validation. Gap, duplicate, group-order, and
out-of-traversal mutations remain rejected.

Independent search QA recomputed all 144 ordered query/unit pairs, confirmed
the exact 42-unit disposition partition (3 governed, 21 control, 18
exclusion), verified candidate links and vocabulary replay, and signed off on
the terminal zero-delta round. The complete regression suite was made
independent of whether the live ledgers are empty or progressed; no production
validation was relaxed.

All Stage 4 completion requirements are met. Exact next stage:
`5-CH01-FOUNDATIONS`, beginning with its paired main-text/Notes paths in
canonical order and no reconciliation inputs.
