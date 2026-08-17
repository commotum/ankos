# 8-CH04-NUMBERS

Status: **COMPLETE**.

## Current Facts

- Stages 1–8 are complete. The live blind-discovery state contains 14,311
  source units, 2,186 reviewed units, 656 active blind candidates, 202 routes
  (75 resolved and 127 pending), 1,607 physical images of which 361 are
  screened, and 12 closed LOCAL rounds.
- Review history is complete through `V000022`. Stage 8 owns `V000016`
  through `V000022`: one `INITIAL`, one `ROUTE_RESOLUTION`, two epoch-1
  `SEARCH_APPEND` transactions, one narrowly scoped epoch-2 `REOPEN`, and two
  epoch-2 `SEARCH_APPEND` transactions.
- Stage 8 owns exactly two canonical documents:
  - `CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md`;
  - `BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes.md`.
- The main chapter contains 306 source units, `U000641..U000946`, and owns 63
  referenced physical images.
- The Notes contain 439 source units, `U005637..U006075`, and own 82 physical
  images: 52 referenced images and 30 unreferenced physical images assigned
  by unique directory/page range.
- The paired assignment therefore contains exactly 745 source units and 145
  physical images. All 745 reading rows are reviewed and all 145 asset rows
  are screened. The main path is current at review epoch 2; the Notes path
  remains current at review epoch 1.
- The Stage 8 gate passes in ordinary and optimized Python:

  ```text
  validated blind audit harness: units=14311 reviewed=2186 candidates=656
  routes=202 assets=1607 screened=361 rounds=12
  ```

- The six mutable-ledger terminal hashes are:
  - `reading-ledger.csv`:
    `ffeada81cc7fd287920ba34a15a4c38ff11bc6763fc256f3f5c0942c85fa4b5b`;
  - `candidate-ledger.jsonl`:
    `11c1da78335cc690161e1f65cf1a4446cfd0915409c7d7164fd7b649440d32d9`;
  - `cross-reference-ledger.csv`:
    `7c4b254601904a04530ae1859cd528c54e834c57fe716af043e7697bc979137f`;
  - `asset-ledger.csv`:
    `ebe56581896a81e638a2e39f5b6f5d8567abe055464e85613ae6a5310a39ddf5`;
  - `search-rounds.json`:
    `c7e90fa50726bbc91eefe9630f26a60127b124950401cf6fba0ac2cbd4557fb5`;
  - `review-history.jsonl`:
    `3ceccad97e2a008e17f4ce3f9cc85fc51a6ee6675308f313dd02cf413c0f059d`.

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
  `CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md`;
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
| Chapter 4 main text | 306 | 306 | 63 referenced | 63 |
| Chapter 4 Notes | 439 | 439 | 52 referenced + 30 unreferenced | 82 |
| **Total** | **745** | **745** | **145** | **145** |

Terminal cross-reference state:

- 75 routes are resolved and 127 are pending globally.
- `V000017` resolved 38 routes: 23 incoming routes and all 15 Stage 8
  `WITHIN_STAGE` routes.
- Stage 8 created `R000179..R000202`; 15 are resolved and 9 typed
  `CROSS_RANGE` obligations remain pending for future assigned ranges.
- No Stage 8 within-stage route remains pending.

## Candidate Changes

- `V000016` allocated `B0321..B0656`: 336 deliberately uncollapsed,
  source-grounded candidates.
- The transaction allocated `E000747..E003238` and
  `G000747..G003238`: 2,492 evidence items/groups.
- No candidate was merged or split during blind Stage 8 review.
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

Sequential review, visual inspection, route closure, and both required LOCAL
closures are complete.

- Epoch 1 searched both assigned paths with 14 frozen families:
  - `S009`: 2,192 hits across 694 unique units; 84 new vocabulary terms;
  - `S010`: the identical normalized hit projection with no vocabulary,
    candidate, evidence, or route delta.
- The epoch-1 dispositions per round are 1,383 governed candidate/support,
  6 cross-reference, 367 control/relationship, and 436 exclusion hits.
- The main-only asset-role correction opened review epoch 2. Its exact local
  scope is therefore only `CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md`:
  - `S011`: 856 hits across 285 unique units with no semantic delta;
  - `S012`: the identical normalized hit projection and another zero delta.
- The epoch-2 dispositions per round are 435 governed candidate/support,
  6 cross-reference, 80 control/relationship, and 335 exclusion hits.
- These are range-local closures, not the Stage 18 whole-corpus saturation
  fixed point.

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
  **met**.
- All 63 main images and all 82 Notes images, including the 30 unreferenced
  physical assets, are screened at the required depth: **met**.
- Both sealed split outputs and their combined output pass ordinary and
  optimized verification with complete, disjoint row and asset coverage:
  **met**.
- Every candidate has complete source-limited provenance, per-field support,
  fingerprint, result kind, uncertainty, and missing-mechanics records:
  **met for Stage 8 capture**. The append-only Stage 18 correction obligation
  below preserves a post-merge evidentiary-strength repair without silently
  rewriting historical evidence.
- Exactly one previewed atomic Stage 8 `INITIAL` transaction is applied and
  the six-ledger state replays through the new history event: **met**.
- Every relevant incoming route whose target lies in the paired assignment
  and every Stage 8 `WITHIN_STAGE` route is resolved; all future targets are
  preserved as typed `CROSS_RANGE` routes: **met**.
- Every Stage 8 LOCAL hit is reproduced and dispositioned over the exact
  review-epoch scope, followed by an identical zero-delta rerun: **met** for
  the two-path epoch-1 scope and the reopened main-only epoch-2 scope.
- Denotations, algorithms, trajectories, queries, solvers, approximations,
  representations, and observers are not conflated: **met**.
- Ordinary and optimized
  `validate_audit.py --goal-dir goal-4 --require-stage 8` pass, along with the
  current full regression, mutation, corpus, history, scope, and whitespace
  gates: **met**.
- This file and `0-plan.md` record the verified ending counts, transaction
  IDs, candidate/route/search ranges, artifact hashes, source boundaries,
  reopened work, and exact Stage 9 handoff: **met**.

## Stage Results

The verified epoch-1 constituent and union outputs have SHA-256 digests:

- main R5:
  `52881896e055d65bf0d3370ffbe4ff492012120d9ec6af991e2b248f76f6a111`;
- Notes R7:
  `329ad3d25d71d848c6d86f130368abee5e0184e1808cefabc47c8d945f93fa72`;
- combined union:
  `680d5356fe0e79ab3b7dc7af2c697014ec037495467b9aa76550c7d54be9644a`.

The coordinator applied:

- `V000016` (`INITIAL`): 745 reading rows, 145 assets,
  `B0321..B0656`, `E000747..E003238`, `G000747..G003238`, and
  `R000179..R000202`;
- `V000017` (`ROUTE_RESOLUTION`): 38 route transitions from proposal
  `6209c6e3c5c14f14128b1c68f7d6bb571077e17353d0e5a220fb9282661f0782`;
- `V000018`/`V000019`: epoch-1 `S009`/`S010`;
- `V000020` (`REOPEN`): the 306-unit/63-asset main path only, with no
  candidate or route proposal;
- `V000021`/`V000022`: epoch-2 `S011`/`S012`.

The reopen output digest is
`8f51700fb2a3ea7c9fd56e2cd16a4972ae4f648ae66bc2322215ce7038994bc0`.
It corrected eleven image roles whose checked embedded formulas, seed values,
or preset labels uniquely supply native evidence:

`A000797`, `A000799..A000802`, `A000810`, `A000811`,
`A000817`, `A000818`, `A000826`, and `A000827`.

The resulting main-path visual-role totals are 24 `NATIVE_EVIDENCE`, 31
`OBSERVER`, 6 `CONTROL`, 1 `DECORATIVE`, and 1 `SOURCE_DEFECT`. `A000806`
remains an observer whose checked π digits corroborate the independently
established positional representation. `A000821` remains a control/display;
the actual difference-observer mechanics are stated by caption `U000860`.

Search proposal digests are:

- `S009` proposal:
  `7634d67bd06c30fe5d743515719bf702053a8392590c0faf547ea74722ce3601`;
- `S010` proposal:
  `fd89edeafecd6eb36790f4eff2c5006f8a13a516b6fc72a57a8dc3c9b48863b6`;
- `S011` proposal:
  `575ac8d66f3a2a3902cee23bba8d4de00206f1212ed86d4e2b848fcb57aaf6b4`;
- `S012` proposal:
  `55b3e24887e819566b65289ba6f71f72f148590cabdc1dbb902b6111fa4cc2c3`.

All four proposals were byte-identical under ordinary and optimized Python
before apply. Their round-result digests are, in order:

`2dd1df7cd31432184ade51ee78f1f14f84abf252d4fa6219e5b5b081c235cae1`,
`26aafc5d678c793899766e1595ad3b51897db6ec499959fdaad4faff5cb50d07`,
`70dbb5972f19d06a6ccc474abc361a4dc763bf156e6eb8fd656055b7c36fa3ab`,
and
`74758e6065e6fa9b69b384451f5f29dac7497bea5d398f5448c4c1653d01b924`.

### Governed Stage 18 correction obligation

The initial transaction is retained as immutable history. The epoch-2 reopen
can correct reading/asset projections, but the contract permits existing
candidate-evidence enrichment only through Stage 18
`CANDIDATE_REVISION`. Stage 18 must therefore:

1. append epoch-2 direct image evidence, and repoint the affected fingerprint
   fields, for 46 candidates whose mechanics or identity are uniquely stated
   by the newly native images:
   - `B0371..B0372` from `A000797`;
   - `B0377..B0382` from `A000799`;
   - `B0383..B0385` from `A000800..A000802`;
   - `B0407..B0410` from `A000810`;
   - `B0411..B0415` from `A000811`;
   - `B0426`, specifically its two checked seed witnesses
     `A000817`/`A000818`;
   - `B0434..B0454` from `A000826`;
   - `B0455..B0458` from `A000827`;
2. append `U000860` as direct caption evidence for `B0428`, repoint all
   mechanics fields away from `E001107`, and append an explicit uncertainty
   noting that `E001107` incorrectly described the image unit as a caption
   and is only a visual witness.

The corrected source author remains
`tools/author_ch04_numbers_main_review.py`, SHA-256
`64e5ce2ea22626b10859b4838609a350a46dd4c75f9cba81f4eb40aefb505027`.
It removes the blanket direct-to-corroborating conversion, preserves the
invariant that non-native images cannot carry direct mechanics, and grounds
the `B0428` law in `U000860`.

The ordinary and optimized Stage 8 gates, corpus verification, corpus
mutation checks, audit mutation/history self-tests, byte compilation, and
whitespace checks pass. The ordinary and optimized full Goal 4 suites each
pass all 94 tests; optimized Python emits only pytest's expected warning that
assertions in test modules are disabled under `-O`.

Stage 9 may now open without reading any Chapter 5 source beforehand. Its
exact input is the six terminal hashes in **Current Facts**, active global
review epoch 2, review-history tip `V000022`, and the explicit Stage 18
candidate-revision obligation above.
