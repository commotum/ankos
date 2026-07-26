# 6-CONFORMANCE

Status: **COMPLETE — pressure fixtures, 60-family join, and reusable test
contract verified**

## Current Facts

- Stages 1–5 are complete. `goal-6/architecture.md` owns the five contracts,
  result algebra, application law, surface, and serialization semantics;
  `goal-6/catalog-migration.md` owns the exact 60-family and T01–T45 map.
- Stage 6 began from clean autosave commit
  `880e6c72281b1b11dc065a5c635fbf92c86df60e`.
- The frozen tree identities are:
  `src/ca=6e6b34769d60508c03d0a69fad1ede4fef75e217`,
  `tests=02ad081e039a46efbf61855fdeae60abb7bb70ad`,
  `goal-2=48b6309655ec7c1d3aaa1a0ec5dfb700385e16d1`, and
  `goal-5=ba62f20b8c620094a0ad683906a803c5404be5f2`.
- Goal 5 selects twelve pressure categories and their representative families.
  This stage executes that selection once; it does not reopen family identity,
  catalog homes, constructor spelling, or Book discovery.
- The durable output is `goal-6/conformance.md`. It references the
  canonical 60-row matrix instead of creating a second taxonomy.

## Updated Assumptions

- Twelve concrete fixtures can cover the reusable mechanics without requiring
  one bespoke executor test per family.
- Every SPF family can be assigned to at least one fixture and one reusable
  suite obligation while continuing through the same family-blind `apply`.
- Test fixtures may use tiny closed descriptors and configurations without
  prescribing Goal 7's concrete Python record layout.
- Public examples required no semantic correction. Hostile review justified
  narrow consistency corrections to architecture, the F045 catalog skeleton,
  and the reference `apply` keyword; none reopens the five fields or catalog.

## Big Picture Objective

Try to break the remastered architecture with Goal 5's strongest
counterexamples, then freeze a compact, executable conformance contract for
Goal 7.

## Detailed Implementation Plan

- Define one paper-execution record shape and execute all twelve selected
  pressure categories with closed inputs, resolved `W` and `R`, complete Rule
  results, application/commit semantics, and exact invariants.
- Assign every SPF001–SPF060 entry in the canonical catalog matrix to the
  pressure pass exactly once at the audit boundary, allowing additional
  secondary fixture coverage without duplicating family definitions.
- Define reusable Goal 7 suites for closure and compatibility, application and
  atomicity, result cardinality, codecs, replay and probability, fresh
  identity, witnesses and quotienting, representation commutation, catalog
  expansion, native/generic equivalence, imports, and observer boundaries.
- Inspect the public contract, conceptual explanation, reference scaffold, and
  application pseudocode for covert sixth fields, hidden entropy or solver
  policy, family/carrier dispatch, and ownership drift.
- Conduct one independent hostile review and resolve every concrete blocker.

Files changed:

- `goal-6/conformance.md`
- `goal-6/6-CONFORMANCE.md`
- `goal-6/0-plan.md`
- `goal-6/architecture.md` for the proven F045 and test-harness boundaries
- `goal-6/catalog-migration.md` for the matching F045 five-field skeleton
- `ref/notes/ca-scaffold.py` to align the public `apply` keyword

## No-Cheating Checks

- No behavioral file under `src/ca`, test file, Goal 2 file, Goal 5 file, or
  Goal 7 handoff is changed.
- No sixth stored program field, family executor, carrier switch, solver,
  entropy authority, observer policy, or update policy is introduced.
- The 60-family audit is a compact join to `catalog-migration.md`, not a second
  taxonomy or semantic-fingerprint ledger.
- Fixtures test denotation and generic application; they do not rely on
  catalog identity to choose behavior.
- A law is not a draw, an intensional relation is not a solver enumeration,
  and a stopped one-shot successor is not an empty result.
- One hostile review closes the stage; no generalized verifier or Goal 4
  ceremony is created.

## Completion Requirements

- [x] Every required pressure category has one concrete passing execution or a
      resolved architecture correction.
- [x] Every SPF001–SPF060 family is accounted for exactly once in the audit
      join, and both close roles remain outside the executable count.
- [x] Every required Goal 7 obligation is phrased as an executable assertion
      with a named fixture or generated case.
- [x] Public examples, application pseudocode, imports, and ownership contain
      no covert axis or family dispatch.
- [x] One independent hostile review leaves no concrete blocker.
- [x] Count, path/link, terminology, import, reference-syntax, whitespace,
      scoped-diff, and frozen-tree checks pass.
- [x] `goal-6/0-plan.md` records the verified result and identifies Stage 7 as
      the first incomplete stage.

## Stage Results

- `goal-6/conformance.md` now contains twelve concrete pressure executions.
  Each records closed input, resolved `W` and `R`, complete Rule/Application
  semantics, commit behavior, and an exact invariant. All Goal 5-named
  representatives are either executed directly or as an explicit fixture
  variant.
- The primary audit join matches all canonical SPF/F pairs exactly:
  SPF001–SPF060 appear once each, with zero hole, duplicate, or provenance
  mismatch. Eight intentional secondary joins cover cross-cutting one-shot,
  nonlocal, and relational pressure. F010/F042 remain close roles.
- Fourteen reusable Goal 7 suites plus one parameterized family-coverage test
  make descriptor closure, phase order, atomicity, cardinality, Seed/Rule
  replay, unavailable measure views, fresh identity, witness quotienting,
  exact codecs, representation commutation, catalog expansion,
  native/generic equivalence, dependency/no-dispatch rules, rollout reuse, and
  the observer boundary executable.
- The T01–T45 migration gate now requires a row-exact expected manifest:
  target counts are `0/2/1` for T08/T40/all others; callable relations count
  `C=5`, `P=39`, `A=4`, `K=1`; all 48 C/P/A names are flat, the sole K is
  category-only, M is non-callable, and T32/T44 remain presets rather than
  aliases.
- The hostile review exposed and closed substantive edge cases rather than
  adding abstractions: continuous defining laws stay in Rule rather than R;
  F045 uses closed evaluator code plus visible work state and never recursive
  `apply`; structural incidence is explicit; codec executions have complete
  RC/AC shapes; Seed realization and quotient-measure unavailability are
  tested; descriptor interpretation is distinguished from family dispatch;
  and rollout is proven to reuse the owned one-step operation.
- `architecture.md`, the F045 catalog row, and the reference scaffold received
  only those concrete consistency corrections. `api.md` and
  `simple_programs.md` required none. No Goal 7 handoff was started.
- Direct checks report 60 catalog family rows, 60 unique primary SPF IDs,
  45 legacy rows with disposition counts `15 retain-family`,
  `21 retain-preset`, `2 merge`, `3 repair`, `2 alias`, `1 retire-role`,
  and `1 split`, twelve PX sections, fourteen CT suites, valid local links,
  and even Markdown-fence parity.
- `python3` AST parsing and direct execution of
  `ref/notes/ca-scaffold.py`, its exact five-field AST check,
  `git diff --check`, and scoped baseline comparison pass. The scaffold uses
  public `apply(program, input)` consistently.
- Relative to baseline `880e6c72281b1b11dc065a5c635fbf92c86df60e`,
  `src/ca`, `tests`, `goal-2`, `goal-5`, and `pyproject.toml` have no diff.
  Their frozen tree identities remain
  `6e6b34769d60508c03d0a69fad1ede4fef75e217`,
  `02ad081e039a46efbf61855fdeae60abb7bb70ad`,
  `48b6309655ec7c1d3aaa1a0ec5dfb700385e16d1`, and
  `ba62f20b8c620094a0ad683906a803c5404be5f2`.
- The 102-test runtime baseline was not rerun because Stage 6 changed only
  planning/reference documentation and the frozen behavioral trees are
  identical. Stage 7 (`7-HANDOFF`) is now the first incomplete stage.
