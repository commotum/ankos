# Goal 8 Execution Loop

Use this protocol to execute
[`goal-8/0-plan.md`](0-plan.md) without losing source evidence, changing the
question, or confusing ledger integrity with semantic proof.

## Repeatable Loop

1. Sync current state with actual files and tests.
2. Update `0-plan.md` with current facts before starting the next stage.
3. Select the first incomplete stage.
4. Create or refresh `goal-8/[INDEX]-[SHORTHAND].md` from the stage template.
5. Implement only that stage.
6. Add verification and no-cheating checks.
7. Run focused tests, full verification, and whitespace/diff checks appropriate
   to the repo.
8. Record results in the stage file.
9. Fold results back into `0-plan.md`.
10. Continue toward the original objective. If stopping for the session, leave
    the goal in a resumable state with current evidence, next experiments,
    unblock actions, and assumptions to challenge.

## Goal-Specific Operating Protocol

At the start of every stage:

- re-read the stage's exact family list and completion requirements;
- join current `ref/types.csv` rather than copying identities from an older
  stage;
- consult the authority order in `0-plan.md`;
- verify that the canonical Book source paths still resolve; and
- inspect existing ledger rows before adding or changing claims.

For every family:

1. Start from its `ref/types.csv` identity and initial anchors.
2. Join its Goal 5 family, candidates, serious leads, and variants.
3. Join its Goal 6 SPF row and any Goal 1 legacy-family evidence.
4. Resolve all shorthand anchors to the canonical 29-document corpus.
5. Inspect the actual passage, enough surrounding context, captions, Notes,
   and followed cross-references.
6. Disposition each source candidate.
7. Write one normalized row for each distinct Space claim.
8. Classify the evidence independently as `DEMONSTRATED`, `STATED`,
   `ENTAILED`, `ENCODING_ONLY`, `CONJECTURAL`, `EXCLUDED`, or
   `UNDERDETERMINED`.
9. For every `ENTAILED` row, write the complete closure argument rather than a
   dimensional guess.
10. Update the one-row family summary only from validated claim IDs.

For discrete dynamics, every admitted claim must explicitly verify:

```text
preserve all coordinates through t
add a complete new slice at t+1
copy non-Frontier locations into that slice unchanged
apply effects only to the new slice
never overwrite time t
```

Continuous, event-driven, one-shot, and multiway families must state their
honest explicit-time analogue and may not pass by copying the discrete wording
without semantic justification.

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
- Preserve exact 60-family coverage and `book_index` presentation order.
- Keep prior goals unchanged; they are evidence inputs, not scratch space.
- Keep the canonical Book corpus unchanged.
- Keep `ref/types.csv` unchanged during the audit.
- Never use current Carrier categories, stubs, tests, or runtime limitations as
  semantic answers.
- Never count encodings, observers, renderings, or derived graphs as native
  Space without an explicit proof.
- Never count `CONJECTURAL`, `EXCLUDED`, `ENCODING_ONLY`, or
  `UNDERDETERMINED` claims as admitted family Space.
- Do not force multiple Space variants into one unstructured cell.
- Do not silently discard source candidates, contradictions, or negative
  evidence.
- A verifier may validate structure and joins; it may not contain a hidden
  hard-coded answer table that substitutes for the evidence ledger.

## Verification Layers

Run verification in this order when applicable:

1. CSV parsing, enum, uniqueness, and foreign-key checks.
2. Exact set equality against `ref/types.csv`.
3. Source path and line-range resolution against the canonical corpus.
4. Goal 5 serious-lead and candidate coverage.
5. Claim-to-source and summary-to-claim joins.
6. Explicit-time and evidence-status semantic checks.
7. Focused hostile review of the current stage's family conclusions.
8. `uv run python goal-8/verify_space_audit.py` once that verifier exists.
9. Focused repository tests only when a consumed reference or executable file
   is changed.
10. Full repository verification only when the actual change scope makes it
    relevant.
11. `git diff --check` and final changed-file inspection.

Record the exact commands, outputs, and scope in the stage file. A passing
parser does not prove that a Book passage entails a dimension. A semantic
claim does not pass until its cited evidence and reasoning have been inspected.

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

- Explicit checks proving the implementation does not route through forbidden fallback paths.

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

For source-audit stages, add these subsections beneath `Detailed
Implementation Plan` or `Stage Results` as appropriate:

```markdown
## Family Coverage

- Exact SPF/F/book-index rows covered.
- Candidate and serious-lead joins.

## Search and Source Dispositions

- Queries and followed cross-references.
- Included, variant, relation, encoding, observer, duplicate, control,
  false-positive, and unresolved candidates.

## Space Claims

- Demonstrated claims.
- Stated claims.
- Entailed claims and complete closure arguments.
- Encoding-only, conjectural, excluded, and underdetermined claims.

## Cross-Field Boundaries

- What belongs to Space.
- What belongs to Alphabet/value structure, Seed, concrete support/shape,
  Frontier, Neighborhood, Rule, realization, or observer output.
```

## Stop, Resume, and Escalation

Do not stop merely because the evidence is difficult or a family has several
possible representations. Convert the uncertainty into searches, cross-family
comparisons, counterexamples, or a bounded underdetermination proof.

Stop and request user direction only when:

- a newly discovered source contradicts the settled explicit-time Space
  semantics in a way that would change the objective;
- completing the audit requires editing the canonical Book corpus;
- a proposed stable `ref/` or runtime/API change would expand this research
  goal's authority; or
- two genuinely different family-boundary choices remain equally supported
  and the choice would materially change the final taxonomy.

When pausing, leave all ledgers parseable, record incomplete family IDs and
source candidates explicitly, update `0-plan.md`, and state the next exact
action. Never use a session boundary to mark incomplete work complete.
