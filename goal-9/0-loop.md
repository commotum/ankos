# Goal 9 Execution Loop

Use this loop to execute `goal-9/0-plan.md`. The loop exists to keep the
refactor synchronized with the actual repository and to prevent apparent
architectural progress from replacing a working kernel.

## Repeatable Loop

1. Sync current state with actual files and tests.
2. Update `0-plan.md` with current facts before starting the next stage.
3. Select the first incomplete stage.
4. Create or refresh `goal-9/[INDEX]-[SHORTHAND].md` from the stage template.
5. Implement only that stage.
6. Add verification and no-cheating checks.
7. Run focused tests, full verification, and whitespace/diff checks appropriate
   to the repository.
8. Record results in the stage file.
9. Fold results back into `0-plan.md`.
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
- Do not substitute a new architecture document for working code.
- Do not create a compatibility layer merely to make old tests pass.
- Do not retain an old abstraction because deleting it makes the diff larger.
- Do not count a stub, import, signature, class, registry row, or serialization
  round-trip as implemented dynamics.
- Do not implement presets during this goal. Anonymous fixtures may prove the
  kernel but must not become hidden canonical builders.
- Do not create `Graph`, `Grid`, `Line`, `Locus`, `Region`, or per-family
  semantic classes where ordinary coordinates plus a selector suffice.
- Do not turn `selector.py` into `loci.py` with a new filename.
- Do not reintroduce Frontier as `active_sites`, `write_scope`, `capabilities`,
  or another required SimpleProgram field. Executor-local indexes may exist
  only as derived optimizations after semantics are correct.
- Do not use process artifacts, agent counts, stage counts, or line-count
  reduction as the proof of success. The proof is the live primitive execution
  path and its behavior.

## Routine Verification

Choose commands that match the files changed in the active stage. At minimum,
the final verification should include:

```text
uv run pytest -q
git diff --check
git status --short
```

Also inspect the live source rather than trusting names:

```text
rg -n "loci|frontier|Writable|Capability|Certificate|Denotation|Disposition" src/ca tests
rg -n "class .*Preset|Generic\[|Protocol" src/ca
rg --files src/ca tests
```

A search hit is not automatically a failure: documentation may explain a
removed term, and an explicitly isolated honest stub may mention it. Every hit
on the public execution path must nevertheless be inspected and justified.

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

## Stop Conditions

Do not declare the goal complete if any of the following is true:

- The new records exist but execution still routes through the old runtime.
- `loci.py` or `frontiers.py` remains required by the live kernel.
- A graph fixture succeeds only by constructing a semantic Graph/Locus object.
- A test passes because a stub has the expected signature.
- Earlier states are mutated or time is implicit in the semantic output.
- Concrete Seed shape has leaked back into SimpleProgram identity.
- A canonical preset has been implemented before the goal's final handoff.
- Downstream serialization or visualization appears healthy only because it is
  silently using the legacy model.
