# 1-GUARDRAILS

Status: COMPLETE

Dependencies:

- None.

## Current Facts

- Stage sync date is 2026-07-14 in `America/Los_Angeles`.
- The immutable legacy root is `ref/A-New-Kind-of-Science/`; the repaired sibling root is `ref/A-New-Kind-of-Science-Repaired/`.
- The repaired sibling root does not exist at stage start.
- Only the three scaffold files existed under `goal-4/` at stage start.
- The worktree already contained unrelated Goal 1 changes in `45-T40-CONSTANT-DIGITS.md`, `45-T40-semantic-oracle.py`, and `45-T40-source-oracle.py`; they are protected and outside this stage's write scope.
- Goal 4's scaffold files were also modified relative to `HEAD` before execution began; their current bytes, not `HEAD`, define the active plan and loop.
- At stage start there were 58 root-level Goal 1 `*-oracle.py` programs. Static and behavioral affected-oracle classification had to be frozen explicitly rather than inferred from filename alone.
- The legacy corpus and the current Goal 1/3 consumers remain immutable during this stage.
- Goal 1 completed a T42 source-oracle addition while this stage was in progress. The closure was resynced only after that work became stable: the final frozen census is 59 root oracles, 40 recursively affected Markdown consumers, and 27 image/basename consumers.
- At closure, the repository-saved Goal 4 state validates against the live consumer/dependency closure and the repaired sibling is absent.

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
- Require an independent authoritative-source review for every later author-text change; high-risk changes additionally require a blind pre-proposal decision and specialist review where applicable.
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

- Completed on 2026-07-14.
- Froze the machine-readable architecture, evidence, review, repair, licensing, promotion, serialization, and quality contracts in `guardrails.json` and its six hash-pinned subsidiary contracts. The raw `guardrails.json` SHA-256 is `ba5357b6172c5740ed799bf53d65aa401c53750b0f5dc6ccc901d4149e5225cb`; its sorted semantic contract digest is `6270a5b17ad4b93b9e12eafe04aff24cea236b84ac0ebd563a3d220832bb3a29`.
- Froze exactly 29 ordered canonical author-text paths: 2 front-matter documents, 12 chapters, 13 Notes documents, Index, and Colophon. Canonical, aggregate, generated, editorial, search, asset, and release-metadata roles are disjoint and mutation-tested.
- Made `ANKOS-AST-1`/`ANKOS-MD-1` executable before Stage 4: explicit anchor slugs and injective ID encoding, source/generated links, deterministic text/code/math/table/list/figure/Index fallbacks, and component-safe cross-document `..` links are specified. Stage 7 still owns parser/renderer choice and corpus fixture validation.
- Froze the held-out sample before-repair selection rule, exact Hamilton allocation, NUL-framed seed/rank derivation, seed and rank known vectors, blind review protocol, exact thresholds, and post-repair CHANGED semantics. Outcome labels cannot alter sample membership.
- Expanded high risk to the union of class and operation/AST impact, including Markdown/heading hierarchy changes and every witness-only author-text insertion.
- Captured and raw-hash-bound `compatibility-baseline.json` (`51f0635f2c278854d11c5ee4391419e736929b1953570af6071348765a6f3a78`) under schema `1.1.0`. Its behavior digest is `e89ccb04eb23fb5fead402636b74e24c29fc7fc9a1a1e53647df3a89e68ba612`.
- The final compatibility census is 59 total Goal 1 oracles, 40 recursively affected, 40 recursive-Markdown, 27 recursive-image/basename, 2 direct-legacy semantic, and 17 no-legacy-path. All 40 affected oracles exited zero and repeated byte-identically.
- The validator re-derives all 59 classifications and every one of the 1,510 dependency rows from explicit contract lists. The frozen/current dependency fingerprint is `a08409016a916244318ca28a45d346458e11a40f44ec1269b8c6cab1dd64c3c4`.
- Proved an exact `ABSENT -> EMPTY -> ABSENT` sibling lifecycle, including cleanup on oracle failure and a post-removal behavior round. All three aggregate behavior digests match and `ref/A-New-Kind-of-Science-Repaired/` remains absent.
- Legacy evidence remained unchanged: 1,463 regular files, zero symlinks, Git tree `52b84494ab310afd64762bf0983106414419655e`, content fingerprint `6da649210cbdb601caddae6e7fb230404565efb224cb0741dd595343f3a6632d`, recursive signature `4b75fac434a1a052066687edfb918bb0b8b75203c1c0e6b254de26562cace61e`, and independent shell digest `b9ff7b9b507790f1d519593baf2b2d2f24dd6cd49dc0fe10f0ac629278ea42f4`.
- Publication validation now requires the exact sibling path and an exact-CJ1 trusted manifest from the non-symlinked `goal-4/releases/` registry; traversal, aliasing, caller/target-local manifests, unowned paths/directories, type/mode/hash drift, symlinks, and hardlinks fail.
- Verification passed in normal and optimized modes: `validate_guardrails.py`, 39 unit/mutation tests, invocation from `/tmp`, JSON byte-profile checks, trailing-whitespace search, `git diff --check`, legacy scope inspection, and sibling-absence check.
- Three independent hostile reviews separately passed compatibility/closure behavior, scope/publication/serialization exactness, and AST/quality/review totality after their reported counterexamples were fixed.
- No repaired corpus content, repair record, or author-text change was produced. Stage 2 owns the immutable raw manifest, segment/block ledger, defect census, and materialized held-out sample; Stage 3 still owns acquisition of authoritative edition-identical page evidence.
