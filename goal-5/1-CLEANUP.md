# 1-CLEANUP

Status: IN_PROGRESS

## Current Facts

- Stage 1 began from a clean worktree at commit `f02753e`; no modified or
  untracked Goal 4 file was present when deletion planning started.
- All concurrent Stage 4 agents were stopped before inventory.
- `goal-4/` has 123 files (about 26 MiB): 36 root artifacts, 14 schemas, 19
  tools, 9 source tests, and 45 bytecode-cache files.
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
- No repository file outside `goal-4/` refers to Goal 4 artifacts. Goal 5
  refers only to the repaired sibling destination.
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

## Completion Requirements

- [ ] Complete keep/delete/migrate decisions are recorded by artifact category.
- [ ] Every modified/untracked Goal 4 file present at cleanup time is inspected
  before deletion (current count: zero).
- [ ] Compact migrated facts are independently sanity-checked against legacy
  inputs and contain no Goal 4 workflow state.
- [ ] Goal 4 generalized pipeline/security/workflow infrastructure and caches
  are absent.
- [ ] No unrelated file or legacy byte changes.
- [ ] No stale external Goal 4 references.
- [ ] Repaired sibling is empty.
- [ ] `git diff --check` and explicit scope inspection pass.

## Stage Results

IN_PROGRESS. Inventory and migration decisions are being completed before any
deletion.
