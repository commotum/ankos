# Goal 6 Execution Loop

Use this loop to execute one Goal 6 stage at a time. Goal 6 remasters the
architecture and implementation plan; it does not implement the remaster.

## Context Startup

At the beginning of a fresh session:

1. Read `goal-6/0-plan.md` in full.
2. Read this file in full.
3. Inspect the actual repository state and the completed Goal 6 stage files.
4. Read only the authoritative inputs required by the first incomplete stage,
   using the precedence in `0-plan.md`.
5. Treat Goal 5 as completed evidence, Goal 2 as frozen selective input, Goal 4
   as superseded machinery, and Goal 7 as unauthorized implementation.

## Repeatable Loop

1. Sync current state with actual files and tests.
2. Update `goal-6/0-plan.md` with current facts before starting the next stage.
3. Select the first incomplete stage.
4. Create or refresh `goal-6/[INDEX]-[SHORTHAND].md` from the stage template.
5. Implement only that stage.
6. Add verification and no-cheating checks.
7. Run focused tests, full verification, and whitespace/diff checks appropriate
   to the repo.
8. Record results in the stage file.
9. Fold results back into `goal-6/0-plan.md`.
10. Continue toward the original objective. If stopping for the session, leave
    the goal in a resumable state with current evidence, next experiments,
    unblock actions, and assumptions to challenge.

## Invariants

- Do not narrow the user's objective without saying so.
- Do not mark a stage complete without evidence.
- Do not use tests or green checks as evidence unless they cover the
  requirement.
- Prefer small, low-complexity stages that narrow uncertainty.
- Convert blockers into work items: decompose them, route around them, or turn
  them into proof and verification tasks.
- Preserve the distinction between implementation, verifier, diagnostic, and
  fallback paths.
- Goal 5's taxonomy and API pressure outrank older architecture. Goal 2 may
  contribute only work explicitly preserved by the integration handoff.
- Do not reopen Book discovery, recreate semantic fingerprints, or import Goal
  4's plans, tools, ledgers, search archives, or verification ceremony.
- Keep `SimpleProgram` to exactly five stored fields. `C`, `V`, `W`, and `R`
  are type relationships, not hidden axes.
- Keep Frontier as the complete possible-write envelope and Neighborhood as the
  readable region. Rule owns applicability, scheduling, conflict, stochastic,
  and update semantics.
- Do not add a public abstraction or file merely because a concept can be
  named. Require a concrete ownership, cohesion, or dependency reason.
- Do not switch generic application on family, catalog, semantic class,
  carrier, or Book source.
- Do not turn the 60 semantic families or six catalog namespaces into runtime
  subclasses.
- Keep whole-program aliases in `catalog/`; keep reusable component constructors
  and presets in their plural component modules.
- Preserve closed descriptors, exact values, visible control/entropy,
  versioned lossless codecs, provenance, witnesses, and raw structural
  semantics.
- Preserve Goal 2 unchanged. Compare or cite it only as needed; do not edit it
  into the new plan.
- Lock the agreed core and catalog names unless a concrete audited-family
  counterexample requires escalation.
- Defer generation/datasets/streams/RNG/viz internals unless a stable public
  boundary is necessary to complete the core/catalog handoff.
- Make planning, reference, and documentation changes only. Do not make
  behavioral changes under `src/ca` or begin Goal 7.
- Reuse Goal 5's compact results. Do not create a second taxonomy matrix when
  the catalog migration matrix can carry the required mapping.
- Perform one complete pressure pass and one final hostile review, not repeated
  review systems.
- Preserve user changes and distinguish the Stage 1 baseline from Goal 6 edits.
- Unexpected artifact growth, duplicated contracts, or competing sources of
  truth are correctness problems.

## Verification Pattern

Use the smallest checks that prove the current stage:

- inspect current files, exports, tests, and `git status --short`;
- verify Markdown links and named paths exist;
- check the family matrix has exactly 60 unique executable rows, the two close
  roles are separate, all 41 additions are present, and T01–T45 each has one
  disposition;
- inspect canonical outputs for extra top-level program axes and conflicting
  meanings of Frontier, Neighborhood, or Rule;
- inspect application pseudocode for catalog/family/carrier dispatch;
- paper-execute only the representative pressure fixtures already selected by
  Goal 5;
- verify closed codec, replay, witness, deduplication, fresh-identity, alias
  expansion, and commutation obligations are testable;
- compare behavioral files under `src/ca` with the Stage 1 baseline;
- run focused repository tests only when a changed planning/reference artifact
  has an executable dependency;
- run `git diff --check` and inspect the final diff and status.

Do not run the full repository suite for documentation-only changes unless a
real dependency requires it. Do not build a validator framework to replace
direct count, link, table, and review checks.

## Stage File Template

```markdown
# [INDEX]-[SHORTHAND]

## Current Facts

- Facts from current code, tests, docs, and previous stage results.

## Updated Assumptions

- Assumptions that still look valid.
- Assumptions that changed.
- Assumptions that need tests before being trusted.

## Big Picture Objective

- Restate the stage objective, adjusted for current facts.

## Detailed Implementation Plan

- Concrete code/doc/test changes for this stage.
- Files expected to change.
- New tests or commands required.

## No-Cheating Checks

- Explicit checks proving the implementation does not route through forbidden
  fallback paths.

## Completion Requirements

- Requirement-by-requirement checks.
- Required test commands.
- Documentation updates required.

## Stage Results

- Fill in at the end of the stage.
- Include tests run and outcomes.
- Include what was learned.
- Include what should change in `0-plan.md` before the next stage.
```

For Goal 6, “implement only that stage” means implement that stage's planning,
reference, documentation, and verification artifacts. It never authorizes
behavioral implementation under `src/ca`.

## Stop Conditions

Stop the current stage and record explicit next work rather than improvising
when:

- a family lacks a valid five-field mapping;
- a proposed sixth axis appears necessary and no five-field representation has
  been tested;
- two catalog homes remain equally canonical without a stated precedence rule;
- application semantics require a family or carrier branch;
- a closed descriptor cannot represent required exact, stochastic, continuous,
  structural, or intensional semantics;
- a current user change overlaps a planned documentation edit;
- source evidence actually contradicts the completed taxonomy; or
- work starts expanding into taxonomy rediscovery, audit infrastructure, or
  Goal 7 implementation.

An apparent blocker does not lower the completion contract. Turn it into a
specific counterexample, ownership decision, paper execution, representation
test, or user escalation.
