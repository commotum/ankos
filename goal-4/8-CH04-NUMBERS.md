# 8-CH04-NUMBERS

Status: **IN PROGRESS**.

## Current Facts

- Stages 1–7 are complete. Stage 8 begins from the verified Stage 7 terminal
  state; no Chapter 4 source unit or owned image has been read or visually
  inspected during this setup.
- The live blind-discovery state contains 14,311 source units, 1,441 reviewed
  units, 320 active blind candidates, 178 routes (37 resolved and 141
  pending), 1,607 physical images of which 216 are screened, and 8 closed
  LOCAL rounds containing 4,098 fully dispositioned hits.
- Review history is complete through `V000015`. Stage 8 has not yet created an
  `INITIAL`, `ROUTE_RESOLUTION`, or `SEARCH_APPEND` transaction.
- Stage 8 owns exactly two canonical documents:
  - `CHAPTERS/04-Systems-Based-on-Numbers.md`;
  - `BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes.md`.
- The main chapter contains 306 source units, `U000641..U000946`, and owns 63
  referenced physical images.
- The Notes contain 439 source units, `U005637..U006075`, and own 82 physical
  images: 52 referenced images and 30 unreferenced physical images assigned
  by unique directory/page range.
- The paired assignment therefore contains exactly 745 source units and 145
  physical images. All 745 reading rows and all 145 asset rows are still
  `PENDING`.
- The Stage 7 gate passes at this starting point:

  ```text
  validated blind audit harness: units=14311 reviewed=1441 candidates=320
  routes=178 assets=1607 screened=216 rounds=8
  ```

- The six mutable-ledger starting hashes are:
  - `reading-ledger.csv`:
    `a68b84be9a697c4af1e6f3b82f8c54042968946265db45a5015fd5c6b20446fc`;
  - `candidate-ledger.jsonl`:
    `4a67a6d222fe9582ef0ef4351b45fe81cb8716b3d6a539e680fc91d36677c4f0`;
  - `cross-reference-ledger.csv`:
    `29912d497b1fb1d2ca3c18c32510b88109c91d8f22f4854703c3afd0b26fbd28`;
  - `asset-ledger.csv`:
    `c9a057710a4b0a18504b77b21e177f036e19df15dcb26a44201d46fc0548bfaa`;
  - `search-rounds.json`:
    `9561cfe25932ca5da92634ce220e61ac1644cc29f1d0ad75a67bcd49fdefe76f`;
  - `review-history.jsonl`:
    `78ccf5b2dc59b51dae89252529f5c68642ccd2bec08b0d5f1ae769a4c6d06d90`.

## Updated Assumptions

- The Chapter 4 main text and Notes must be treated as one paired discovery
  stage, but their blind reviews should be isolated in separate sealed
  bundles so neither review imports the other's candidate framing.
- The categories named in the plan—definitions, queries, procedures,
  sequences, filters, maps, continuous systems, equations, observations, and
  numerical methods—are review prompts, not findings or candidate identities.
- A displayed formula, computation, sequence, or plot is not automatically a
  construction. Candidate capture still requires both an identity anchor and
  a semantic anchor under `guardrails.json`.
- Native iteration, an algorithm used to obtain a result, a declarative
  denotation, a partial function, a relation or model set, a numerical
  approximation, and an observer must remain distinct unless the assigned
  source itself establishes their relationship.
- Exactness, undefinedness, termination, convergence, completion, failure,
  and hidden work state may be identity-critical. They must be recorded
  explicitly rather than normalized to an assumed step-by-step trajectory.
- Image filenames, captions in isolation, nearby prose, and visual similarity
  cannot establish hidden mechanics.

## Big Picture Objective

Blindly audit the complete Chapter 4 main-text and Notes assignment for every
source-grounded construction, generator, relation, constraint, immutable
definition, query, input-processing procedure, preset, restriction,
representation, observer, application, numerical method, and genuine source
boundary, while preserving the distinctions among native results, algorithms,
trajectories, denotations, and observations.

## Allowed Inputs And Scope

The stage-opening setup may use only:

- `goal-4/0-plan.md`, `goal-4/0-loop.md`, and completed Stage 7 facts;
- Goal 4 guardrails, corpus manifest, and current blind ledgers;
- Goal 4 schemas and coordinator tooling needed to create and verify sealed
  review bundles.

Once sequential review begins, each isolated reviewer may additionally use
only its own sealed assignment:

- the main reviewer: `U000641..U000946` and the 63 images owned by
  `CHAPTERS/04-Systems-Based-on-Numbers.md`;
- the Notes reviewer: `U005637..U006075` and the 82 images owned by
  `BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes.md`;
- sanitized blind-discovery instructions, blind schemas, and write-free
  verification material included in the sealed bundle.

After both sequential reviews are complete, LOCAL search may read exactly the
same two canonical paths and no other Book path.

Forbidden throughout Stage 8:

- T01–T45 mappings, the current catalog, and `CA-Types` conclusions;
- Goal 1 and Goal 2 conclusions;
- `api.md`, `simple_programs.md`, `src/ca`, or any API-fit, executor, runtime,
  or implementation-support judgment;
- any unassigned Book text or image, except that a reference to it may be
  recorded as a pending `CROSS_RANGE` route;
- the other reviewer's semantic output before both sealed reviews are
  finalized and returned to the root coordinator.

The only setup write is this stage file. Subsequent stage writes remain under
`goal-4/`, with sealed scratch material under `/tmp`; shared mutable ledgers
may change only through previewed atomic coordinator transactions.

## Source Coverage

| Assignment | Source units | Reviewed | Physical images | Screened |
|---|---:|---:|---:|---:|
| Chapter 4 main text | 306 | 0 | 63 referenced | 0 |
| Chapter 4 Notes | 439 | 0 | 52 referenced + 30 unreferenced | 0 |
| **Total** | **745** | **0** | **145** | **0** |

Starting cross-reference state:

- 37 routes are resolved and 141 are pending globally.
- The exact incoming Stage 8 subset will be resolved only after its target
  units have been reached in sequential review.
- No Stage 8 `WITHIN_STAGE` or outgoing `CROSS_RANGE` route has been created
  yet.
- Stage 8 search starts from 8 closed LOCAL rounds and 4,098 governed hits;
  no Stage 8 query or hit exists yet.

## Candidate Changes

- No candidate has been created, changed, split, or merged for Stage 8.
- Worker proposals will use independent ordered `W####`, `WE######`,
  `WG######`, and `WR####` identifiers. Only the coordinator may allocate
  global B, E, G, and R identifiers after both outputs have been verified and
  combined in canonical traversal order.
- Candidate capture will follow the guardrail identity-plus-semantic-anchor
  rule and err toward retaining a source-grounded, mechanically credible
  object when its mechanics are incomplete.
- Every proposed candidate must carry all fingerprint keys, per-field support
  status, evidence strength, exact result kind, partiality/completion/failure
  semantics, missing mechanics, uncertainties, image witnesses, and routes.
- Main-text and Notes proposals that look duplicative remain separate blind
  records unless the strict blind identity-proof contract is independently
  satisfied. No catalog or semantic-family reconciliation occurs here.

## Search And Evidence Log

No source review, visual inspection, route closure, or Stage 8 search has
begun.

The required order is:

1. finish and verify both complete sequential reviews;
2. combine and atomically merge their review output;
3. resolve incoming and within-stage routes whose targets are now reviewed;
4. freeze candidate-derived and guardrail query families;
5. run deterministic LOCAL search over exactly the two assigned paths;
6. disposition every query/unit hit in context;
7. rerun the same frozen search to a real zero-delta result.

The Stage 8 zero-delta rerun is range-local closure only. It must not be
reported as the Stage 18 whole-corpus saturation fixed point.

## Detailed Implementation Plan

1. Reconfirm the six starting ledger hashes, the `V000015` history tip, the
   corpus manifest, and the Stage 7 ordinary/optimized validation gates before
   any semantic work.
2. Build two sealed epoch-1 worker bundles from the same verified pending
   ledger state: one for the 306-unit/63-image main assignment and one for the
   439-unit/82-image Notes assignment. Verify their allowed-file manifests,
   source/asset partitions, hashes, prompts, and prohibited-input
   declarations.
3. Prepare nonsemantic worksheets with no default dispositions, candidates,
   visual roles, evidence strengths, or inferred mechanics.
4. Review each bundle independently and in source-unit order. Read every unit
   in full context before assigning its primary disposition; create or link a
   candidate whenever the guardrail capture rule is met.
5. Screen every owned physical image, including all 30 unreferenced Notes
   assets. Escalate construction-bearing, text-bearing, ambiguous, or
   caption-incomplete assets to original resolution and independently check
   any mechanics-bearing transcription.
6. Complete every source-limited fingerprint and uncertainty boundary.
   Explicitly distinguish native iteration from work procedure, function or
   relation from solver trace, exact result from approximation, and
   representation or observer from the object represented or observed.
7. Subject each completed split output to hostile semantic and provenance
   review. Repair the source authoring artifacts and regenerate a new sealed
   output rather than patching a finalized worker result.
8. Verify each constituent output, combine the disjoint bundles against the
   common pending ledgers in canonical traversal order, verify deterministic
   identifier rewriting and full row/asset coverage, and preview the combined
   merge in ordinary and optimized Python.
9. Apply exactly one atomic Stage 8 `INITIAL` transaction only after both
   previews are clean. Revalidate live-ledger replay and history-prefix
   integrity.
10. Identify all pending incoming routes whose targets lie in the now-reviewed
    assignment and every new `WITHIN_STAGE` route. Resolve them from reviewed
    context, preview the exact route proposal, and apply one governed
    `ROUTE_RESOLUTION` transaction. Leave genuinely future targets as typed
    `CROSS_RANGE` obligations.
11. Freeze range-local guardrail and candidate-derived query families only
    after sequential review and route closure. Search exactly the two assigned
    paths, disposition every hit, apply one `SEARCH_APPEND`, and repeat the
    identical query set in a second zero-delta `SEARCH_APPEND`.
12. Run the Stage 8 ordinary/optimized audit gates, full Goal 4 regressions,
    corpus/hash verification, mutation/self-tests, byte-compilation/import
    checks, whitespace/fence checks, and exact scope inspection.
13. Record all final counts, IDs, hashes, routes, defects, search digests,
    commands, and outcomes here; then update `0-plan.md` to make the verified
    Stage 8 terminal state the exact Stage 9 input.

## No-Cheating Checks

- Preserve the recorded all-pending baseline: 745/745 assigned units and
  145/145 assigned assets must be accounted for by the Stage 8 review
  transaction, with no gap, overlap, semantic default, or pre-reviewed row.
- Main and Notes reviewers receive disjoint sealed source/asset bundles and
  cannot read the other reviewer's candidate output before coordinator merge.
- Every worker-local candidate, evidence group, evidence item, and route must
  follow immutable assigned traversal order; global identifiers are allocated
  only during coordinator preview/apply.
- No keyword, heading, caption, filename, or current pending route may replace
  sequential in-context reading. Search authoring and execution begin only
  after all 745 units and 145 assets have completed review.
- Any direct image mechanics claim requires original-resolution inspection,
  contextual anchoring, and independently checked transcription. Proximity or
  visual resemblance remains contextual evidence.
- Every `SOURCE_UNIT` or `IMAGE` anchor must match the exact Stage 8 review
  epoch and owning path. Evidence may not predate its candidate.
- The combined output must be invariant to constituent input order while
  retaining canonical assignment traversal, and it must reject overlap,
  omission, foreign paths, stale ledger hashes, or unrewritten worker IDs.
- An incoming or within-stage route may resolve only to a target already
  reviewed in context. No future range may be opened to make the queue look
  smaller.
- LOCAL query-scope union must equal exactly the two Stage 8 paths. Every
  query/unit pair must reproduce from the frozen query specification, every
  hit must have one final disposition, and the final rerun must be identical
  and zero-delta.
- Blind schemas and free-text checks must reject T mappings, catalog/family
  actions, API fit, executor/runtime conclusions, and all other forbidden
  blind fields.
- Green validators establish integrity only; they do not establish that the
  assigned source and images were understood correctly.

## Completion Requirements

- All 306 main-text units and all 439 Notes units are individually reviewed:
  **not yet met**.
- All 63 main images and all 82 Notes images, including the 30 unreferenced
  physical assets, are screened at the required depth: **not yet met**.
- Both sealed split outputs and their combined output pass ordinary and
  optimized verification with complete, disjoint row and asset coverage:
  **not yet met**.
- Every candidate has complete source-limited provenance, per-field support,
  fingerprint, result kind, uncertainty, and missing-mechanics records:
  **not yet met**.
- Exactly one previewed atomic Stage 8 `INITIAL` transaction is applied and
  the six-ledger state replays through the new history event: **not yet met**.
- Every relevant incoming route whose target lies in the paired assignment
  and every Stage 8 `WITHIN_STAGE` route is resolved; all future targets are
  preserved as typed `CROSS_RANGE` routes: **not yet met**.
- Every Stage 8 LOCAL hit is reproduced and dispositioned over the exact
  two-path scope, followed by an identical zero-delta rerun: **not yet met**.
- Denotations, algorithms, trajectories, queries, solvers, approximations,
  representations, and observers are not conflated: **not yet met**.
- Ordinary and optimized
  `validate_audit.py --goal-dir goal-4 --require-stage 8` pass, along with the
  current full regression, mutation, corpus, history, scope, and whitespace
  gates: **not yet met**.
- This file and `0-plan.md` record the verified ending counts, transaction
  IDs, candidate/route/search ranges, artifact hashes, source boundaries,
  reopened work, and exact Stage 9 handoff: **not yet met**.

## Stage Results

Stage 8 has been opened from the verified Stage 7 ledger state. The only work
completed so far is the blind-safe setup and exact assignment accounting
recorded above. No Chapter 4 source text, formula, caption, or image has yet
been inspected, and no semantic candidate or route conclusion has been made.

The next safe action is to build and verify the two sealed Stage 8 worker
bundles from the recorded all-pending assignment, then begin independent
sequential review with `U000641` in the main bundle and `U005637` in the Notes
bundle.
