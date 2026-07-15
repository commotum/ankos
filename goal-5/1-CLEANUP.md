# 1-CLEANUP

Status: COMPLETE

## Current Facts

- Stage 1 began from a clean worktree at commit `f02753e`; no modified or
  untracked Goal 4 file was present when deletion planning started.
- All concurrent Stage 4 agents were stopped before inventory.
- Before removal, `goal-4/` had 123 files (about 26 MiB): 36 root artifacts,
  14 schemas, 19 tools, 9 source tests, and 45 bytecode-cache files. It is now
  absent.
- The repaired sibling exists and is empty.
- The pre-cleanup legacy snapshot is:
  - files: 1,463;
  - Markdown: 19;
  - JPEG: 1,444;
  - sorted path-and-file-digest SHA-256:
    `b9ff7b9b507790f1d519593baf2b2d2f24dd6cd49dc0fe10f0ac629278ea42f4`;
  - monolith bytes: 3,780,628;
  - monolith SHA-256:
    `55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20`.
- No code, test, or document outside `goal-4/` consumes a specific Goal 4
  artifact, module, schema, or contract. Goal 5 contains intentional historical
  cleanup references and repaired-sibling references, but no machinery
  dependency.
- Goal 4 has produced no corrected author text. Its source witness remains
  unavailable for lawful complete comparison.

## Updated Assumptions

- Git history is sufficient archival storage for deleted Goal 4 process
  machinery.
- The 29 provisional ranges and known defect locations are useful routing
  seeds, but are not authoritative transcription evidence.
- A fresh small builder/validator in Goal 5 will be easier to understand and
  safer to maintain than retaining any Goal 4 pipeline implementation.
- The complete source-access problem survives cleanup and must remain explicit.

## Big Picture Objective

Remove Goal 4's generalized publication/audit infrastructure while preserving
only compact, directly useful source facts for Goal 5.

## Detailed Implementation Plan

1. Complete a live inventory of every Goal 4 root artifact, schema, tool, test,
   report, and cache.
2. Record category-level `MIGRATE` or `DELETE` decisions and inspect every
   modified/untracked item individually (currently none).
3. Migrate only:
   - 29 provisional raw document ranges;
   - 55 known defect/guardrail candidates in simplified form;
   - a compact 1,444-row image-reference-to-asset map;
   - one concise legacy/image/routing/source-access summary.
4. Delete all Goal 4 schemas, locks, workflow/licensing/authority machinery,
   overlay/zero-build/promotion implementations, generated ledgers/reports,
   redundant validators/tests, stage plans, and caches.
5. Re-scan repository references, rehash the legacy tree, confirm the repaired
   sibling is empty, and inspect the final diff/scope.

## No-Cheating Checks

- Migrated facts are labeled provisional and cannot authorize a text change.
- No Goal 4 validator is retained merely to validate another Goal 4 artifact.
- No generalized schema, authority, reviewer, proof-lock, race-defense, or
  synthetic-overlay code is renamed into Goal 5.
- The legacy tree is compared against the exact pre-cleanup snapshot.
- The repaired sibling remains empty and never becomes build input.
- Any source-access gap remains explicit rather than being converted into a
  waived or inferred correction.

## Artifact Decisions

The live tree contains 78 tracked files and 45 ignored cache files. Decisions
are complete by closed category; there is no partial Goal 4 cluster to retain.

| Live category | Count | Decision | Directly useful payload preserved |
|---|---:|---|---|
| Goal/stage plans (`0-*`, `1-*`–`4-*`) | 7 | DELETE | Goal 5 plan/loop replace them; Git retains history. |
| General contracts/policies (`fidelity`, `guardrails`, `review`, `style`, `licensing`, `promotion`, `witness`, `pipeline`, `zero-repair`) | 12 | DELETE | Source-access blocker and author/editorial distinction summarized in `legacy-facts.json` and Goal 5 constraints. |
| Generated baselines, reports, samples, locks, and witness state | 12 | DELETE | Counts, monolith/tree hashes, and source-access state summarized in `legacy-facts.json`. |
| Large structure/image/routing/defect ledgers | 5 | MIGRATE, THEN DELETE | 29 ranges → `source-ranges.json`; 55 candidates → `known-defects.jsonl`; 1,444 direct image mappings → `image-map.jsonl`; image/routing totals/anomalies → `legacy-facts.json`. |
| Generalized JSON schemas | 14 | DELETE | None; Goal 5 uses simple JSONL/CSV formats only when implemented. |
| Pipeline/baseline/witness/overlay/receipt/zero-repair tools | 19 | DELETE | None; each belongs to an interdependent Goal 4 cluster. Stage 2 will implement a fresh small builder and validator. |
| Redundant component/mutation tests | 9 | DELETE | None; all import Goal 4-only modules. Goal 5 tests will target real book defects. |
| `__pycache__` bytecode | 45 | DELETE | None. |
| Goal 4 files kept in place | 0 | KEEP | No artifact directly corrects book text, and partial retention would leave stale internal dependencies. |

The 36 root artifacts are fully accounted for by the first four rows: 7 stage
documents, 12 contracts/policies, 12 generated state/report/lock artifacts,
and 5 migrated large ledgers. The other 42 tracked files are exactly 14 schemas,
19 tools, and 9 tests.

No modified or untracked Goal 4 file existed at the decision point. Recent
autosave commits mix Goal 4 with Goal 1 and Goal 5 work, so cleanup is strictly
path-level deletion; no commit range will be reverted.

## Completion Requirements

- [x] Complete keep/delete/migrate decisions are recorded by artifact category.
- [x] Every modified/untracked Goal 4 file present at cleanup time was inspected
  before deletion (current count: zero).
- [x] Compact migrated facts were independently sanity-checked against legacy
  inputs and contain no Goal 4 workflow state.
- [x] Goal 4 generalized pipeline/security/workflow infrastructure and caches
  are absent.
- [x] No unrelated file or legacy byte changes.
- [x] No stale external Goal 4 references.
- [x] Repaired sibling is empty.
- [x] `git diff --check` and explicit scope inspection pass.

## Stage Results

COMPLETE on 2026-07-14.

- Deleted all 78 tracked Goal 4 files by exact path and all 45 ignored `.pyc`
  files, then removed the empty `goal-4/` directory. No commit range was
  reverted.
- Preserved only four compact, provisional Goal 5 inputs:
  `source-ranges.json` (29 ranges), `known-defects.jsonl` (55 candidates),
  `image-map.jsonl` (1,444 image references), and `legacy-facts.json`.
- Removed Goal 4-only detector IDs, raw-block IDs, workflow status fields, and
  partial boundary-signature metadata from the migrated inputs.
- Direct validation passed for all 29 contiguous byte ranges and segment
  hashes, all 52 exact defect-span hashes, all 1,444 image files/hashes/source
  line references, and the 29-document image totals.
- The protected legacy tree still has 1,463 files and reproduces SHA-256
  `b9ff7b9b507790f1d519593baf2b2d2f24dd6cd49dc0fe10f0ac629278ea42f4`.
  The monolith remains 3,780,628 bytes with SHA-256
  `55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20`.
- A repository scan found no live external Goal 4 path, module, or validator
  references. Intentional historical references inside Goal 5 remain.
- The repaired sibling is empty, `git diff --check` passes, and scope is limited
  to deletion of `goal-4/` plus the three compact Goal 5 metadata cleanups.
- No book text was changed. The next stage must build a plain 29-document
  baseline and remains unable to complete without lawful, readable,
  edition-identical source evidence.
