# 1-GUARDRAILS

Status: IN_PROGRESS

Dependencies:

- None.

## Current Facts

- Stage sync date is 2026-07-14 in `America/Los_Angeles`.
- The immutable legacy root is `ref/A-New-Kind-of-Science/`; the repaired sibling root is `ref/A-New-Kind-of-Science-Repaired/`.
- The repaired sibling root does not exist at stage start.
- Only the three scaffold files existed under `goal-4/` at stage start.
- The worktree already contained unrelated Goal 1 changes in `45-T40-CONSTANT-DIGITS.md`, `45-T40-semantic-oracle.py`, and `45-T40-source-oracle.py`; they are protected and outside this stage's write scope.
- Goal 4's scaffold files were also modified relative to `HEAD` before execution began; their current bytes, not `HEAD`, define the active plan and loop.
- There are 58 root-level Goal 1 `*-oracle.py` programs. Static and behavioral affected-oracle classification must be frozen rather than inferred from filename alone.
- The legacy corpus and the current Goal 1/3 consumers remain immutable during this stage.

## Updated Assumptions

- A sibling release root can remain invisible to consumers recursively rooted at the legacy directory; this still requires behavioral baseline evidence.
- Portable byte-identical asset copies are acceptable in the sibling release, subject to later manifest and licensing checks.
- The 29 canonical author-text documents can be the sole exactly-once conservation domain while the assembled monolith is explicitly derived.
- A precise CommonMark-oriented serialization profile can represent the zero-repair corpus; Stage 7 must validate it against adversarial fixtures before content repair.
- No authoritative page witness is required to freeze policy, roles, names, or compatibility baselines in this stage.

## Big Picture Objective

Freeze an executable fidelity contract: immutable input and output boundaries, exact document roles and paths, evidence/review rules, serialization constraints, predeclared quality sampling, compatibility baselines, release ownership, rollback, licensing, and separately authorized promotion.

## Detailed Implementation Plan

- Freeze the 29 canonical paths and their order in a machine-readable architecture contract.
- Freeze output roles for canonical author text, derived aggregates, generated metadata, editorial sidecars, search derivatives, governed assets, and release metadata.
- Freeze evidence hierarchy, author-text refusal rules, workflow/final states, severity, reviewer independence, build/audit modes, witness licensing, and release blockers.
- Freeze the Stage 1 serialization profile required by the zero-repair builder, with Stage 7 fixture validation explicitly required before author-text batches.
- Freeze the held-out sample frame, manifest-derived seed procedure, per-document/risk quotas, blind transcription/adjudication protocol, projections, and release thresholds before results exist.
- Audit affected Goal 1 recursive consumers and capture deterministic command/output/status digests before any sibling release exists.
- Prove that an empty sibling directory leaves affected consumer behavior unchanged, without changing any legacy file.
- Implement independent Stage 1 contract validation and negative tests for wrong roots, role/count drift, path collisions, weak review, unsupported evidence, unsafe ownership, or implicit promotion.
- Record exact commands and results here and fold verified facts into `0-plan.md`.

## No-Cheating Checks

- Hash the legacy tree before and after Stage 1 with a read-only independent command and require equality.
- Discover raw inputs only from the frozen explicit allowlist contract, never by recursively scanning a parent that can include generated output.
- Keep the sibling output outside the legacy root and reject path containment or symlink aliasing back into it.
- Do not create a repair record or alter author text in this stage.
- Reject author-text correction based on the monolith, split derivatives, local crops, model judgment, syntax, rendering, or mathematical plausibility alone.
- Require creator/reviewer identity inequality and authoritative evidence for every later high-risk author-text change.
- Treat the aggregate, navigation, editorial, and search outputs as noncanonical roles and exclude them from exactly-once author-text counts.
- Refuse publication into any nonempty target that is not already manifest-owned.
- Treat legacy promotion, deletion, relocation, and consumer migration as separate user-authorized work.

## Completion Requirements

- A machine-readable contract freezes all 29 ordered canonical paths, every role, roots, ownership rules, evidence/review policy, serialization profile, sample protocol, and release blockers.
- Independent validation proves the contract is internally total and rejects representative policy mutations.
- The affected Goal 1 oracle set, exact invocations, exit statuses, and byte-level output digests are captured reproducibly.
- A before/empty-sibling/after comparison proves no affected consumer behavior changes.
- Legacy raw hashes are identical before and after the stage.
- Stage-local tests, whitespace checks, `git diff --check`, and write-scope inspection pass.
- No repaired corpus content or author-text repair is produced.

## Stage Results

- Pending implementation and verification.
