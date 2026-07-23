# Goal 1 Execution Loop

This loop governs every stage in `goal-1/0-plan.md`. The plan is authoritative but revisable: `principles.md` Principle 0 requires re-derivation whenever evidence exposes a bad assumption.

## Architecture Audit Overlay

Future stages use the broad SimpleProgram abstraction established in `architecture-audit.md`:

```text
active = FRONTIER.select(configuration)
reads  = NEIGHBORHOOD.read(configuration, active)
writes = RULE(active, reads)
next   = UPDATE.apply(configuration, active, writes)  # StepResult[Configuration]
```

`src/ca` is the current namespace and Phase 1 realization of this SimplePrograms library, not a claim that cellular automata delimit the architecture. Its present fixed-lattice shapes and family branches are implementation facts to audit. A catalog construction does not earn a new top-level class or executor merely because it departs from those defaults; first attempt the smallest explicit ALPHABET, CONFIGURATION/invariant, FRONTIER, NEIGHBORHOOD, RULE-result, UPDATE, or loci-selector extension inside the common algebra.

DOMAIN is the task/program's dimensional space (`t+0D`, `t+1D`, and so on), with discreteness or continuity explicit. CONFIGURATION declares the native support/topology that inhabits that DOMAIN plus structural invariants. ALPHABET is its label/value schema and may be a product or tagged union. FRONTIER selects rule-firing loci/occurrences/matches, RULE returns typed writes/replacements, and UPDATE returns one structured result containing zero, one, or many successor configurations plus typed outcome/event/witness data. These are axes of one branch-free runner, not family executors.

Distinct source names or semantic roles do not imply distinct runtime classes. Prefer parameterizations, named roles, invariants, and lossless structural representations. For a claimed equivalence, require a complete-state map `e` with an explicit inverse on its invariant-valid image, one-step-granularity commuting successor sets, and no hidden source interpreter. Reject opaque whole-state packing, callbacks, lossy quotients, family dispatch, invented behavior, and altered schedules.

## Repeatable Loop

1. Sync current state with the actual repository files, current Git diff, completed stage files, and verification results.
2. Read `principles.md` and update `goal-1/0-plan.md` with current facts before starting the next stage.
3. Select the first incomplete stage whose dependencies are satisfied. Reopen an earlier stage first when later evidence invalidates it.
4. Create or refresh `goal-1/[INDEX]-[SHORTHAND].md` from the stage template below.
5. Implement only that stage. In Goal 1, "implement" means evidence collection, analysis, design integration, and Goal 2 planning, not runtime changes.
6. Add verification and no-cheating checks that directly cover the stage requirements.
7. Run focused evidence checks, repository-wide coverage checks appropriate to the current stage, and whitespace/diff checks.
8. Record searches, excerpts, decisions, rejected alternatives, commands, and outcomes in the stage file.
9. Fold results back into `goal-1/0-plan.md`, `goal-1/evidence-index.md`, and `goal-1/design-ledger.md`. Update affected assumptions and reopen contradicted stages.
10. Continue toward the original objective. If stopping for the session, leave the goal resumable with current evidence, unresolved candidate matches, next searches, integration consequences, and assumptions to challenge.

## Invariants

- Do not narrow the objective without saying so.
- Do not mark a stage complete without requirement-level evidence.
- Do not use search counts, tests, or green checks as evidence unless they cover the actual requirement.
- Prefer small, low-complexity decisions that narrow uncertainty.
- Convert apparent blockers into explicit evidence questions, diagnostics, alternate formulations, proof obligations, or re-derivation work.
- Preserve the distinction between program semantics, implementation, verifier, diagnostic, solver, numerical approximation, experiment encoding, and fallback paths.
- Do not treat `CA-Types.md` summaries as book evidence.
- Do not infer construction semantics from a catalog name when the book is ambiguous.
- Do not call evidence exhaustive until aliases, variants, captions, Notes, Index references, and cross-references have been checked and all candidates resolved.
- Do not preserve an abstraction merely because an earlier stage introduced it.
- Do not edit `src/ca`, `tests`, `simple_programs.md`, or `principles.md` during Goal 1. Record proposed changes for Goal 2.
- Do not create family-specific rollouts, compatibility paths, fake capacity, opaque packing, or unrestricted callbacks in the proposed design.
- Do not fabricate steps to force declarative nonfits through the SimpleProgram runner.
- Do not create empty future stage files. Create a stage file when its work begins.

## Type-Stage Evidence Procedure

For stages `T01` through `T45`:

1. Read the corresponding CSV row and complete `CA-Types.md` section.
2. Build a search vocabulary containing the direct name, aliases, singular/plural forms, named variants, example rule names, defining operations, parameter names, and cross-referenced systems.
3. Search the full monolithic book for every vocabulary item. Record every command or equivalent query.
4. Inspect context around every hit and classify it as included evidence, duplicate, cross-reference to follow, or false positive.
5. Search section headings, captions, Notes, and Index material separately when broad terms produce noisy results.
6. Follow relevant page and section cross-references and add any new vocabulary discovered there.
7. Record each unique relevant excerpt verbatim with exact source path, line provenance, section context, and the construction fact it establishes.
8. Reconstruct the type from evidence before comparing it with the API or runtime.
9. Read every relevant section of `simple_programs.md`, `src/ca`, and tests rather than relying on previous summaries.
10. Search `design-ledger.md` and completed stages for an existing semantic primitive before proposing a new one.
11. Write the Goal 2 implementation/conformance handoff and update global integration artifacts.

## Type-Stage Fit Labels

Use these labels consistently:

- `DIRECT`: the existing semantic component expresses the construction without reinterpretation.
- `PARAMETERIZATION`: existing semantics suffice; only data, validation, or a named preset is required.
- `PRINCIPLED EXTENSION`: a new semantic capability is required and is justified directly by evidence.
- `SEMANTIC MISMATCH`: the current abstraction expresses a different construction or requires prohibited packing, inversion, fallback, or hidden behavior.
- `NOT APPLICABLE`: the component is genuinely absent from this construction; do not invent a placeholder.
- `UNRESOLVED`: evidence is insufficient or contradictory; the stage cannot complete until resolved or honestly blocked.

## Re-Integration Audit

After every completed type stage, answer all of the following in the stage file and update the plan:

1. Did this evidence invalidate a prior assumption, primitive, type grouping, or executor boundary?
2. Can the proposed capability reuse an existing primitive without changing that primitive's meaning?
3. Does the proposal introduce an exception, flag, hidden state, duplicate path, or arbitrary callback?
4. Does state still contain all information required to advance and reproduce the trace?
5. Are support, topology, values, control, and representation still separated correctly?
6. Is a defining algorithm being incorrectly separated from the mathematical system, or an incidental solver being incorrectly fused into it?
7. Does the proposed ANKoS encoding preserve every distinction required by the type?
8. Which completed stages must be reopened?
9. Which Goal 2 stages or dependencies change?
10. Is the overall API simpler and more coherent after incorporating this type? If not, stop and re-derive.

## Stage File Template

```markdown
# [INDEX]-[SHORTHAND]

## Current Facts

- Facts from current code, tests, docs, taxonomy, book evidence, and previous stage results.

## Updated Assumptions

- Assumptions that still look valid.
- Assumptions that changed.
- Assumptions that need evidence or tests before being trusted.

## Big Picture Objective

- Restate the stage objective, adjusted for current facts.

## Catalog Identity

- Stable type index and exact CSV name.
- Entry kind: construction, specialization, restriction, seed class, observable, solver-defined system, or unresolved.
- Aliases, variants, and parameter vocabulary.

## Search Log

- Every search query or command used.
- Candidate matches inspected.
- Cross-references followed.
- False positives and duplicates excluded with reasons.
- Remaining unresolved candidates.

## Book Excerpts

### Excerpt [N]: [Short description]

- Source: `[path:line]`
- Section/context: [book section, caption, Note, or Index entry]
- Establishes: [construction fact]

> [Complete relevant excerpt]

## Construction Model

- State.
- Support/topology.
- Values/alphabet.
- Control state.
- Active loci/frontier.
- Reads/neighborhood/access pattern.
- Rule inputs and semantic results.
- Update/commit semantics.
- Successor structure and halting.
- Boundary and initial conditions.
- Core variants and parameters.
- Observables distinguished from program state.

## Current API Fit

- Map each construction element to `simple_programs.md` with `DIRECT`, `PARAMETERIZATION`, `PRINCIPLED EXTENSION`, `SEMANTIC MISMATCH`, `NOT APPLICABLE`, or `UNRESOLVED`.
- Include exact document references.

## Current Runtime Fit

- Map each construction element to concrete `src/ca` modules, functions/classes, and tests using the same fit labels.
- Identify existing behavior that must be retained.

## Principles Audit

- Relevant principles and tensions.
- Smallest honest semantic model.
- Existing primitives reused.
- New primitives proposed and evidence requiring them.
- Alternatives rejected, especially packing, global formula bypasses, family switches, fixed-capacity simulations, or vacuous callbacks.

## Detailed Implementation Plan

- Goal 1 evidence/design work for this stage.
- Files expected to change inside `goal-1/`.
- Verification commands required.

## Goal 2 Implementation Stage

- Objective and dependencies.
- Shared primitives consumed or introduced.
- Concrete API, runtime, migration, and test changes.
- Canonical book examples and conformance tests.
- Completion requirements and no-cheating verification.
- Effects on other planned Goal 2 stages.

## No-Cheating Checks

- Explicit checks proving the design does not route through forbidden fallback paths.
- Checks that excerpts and construction semantics, not catalog labels, justify the proposal.
- Checks that shared primitives are not duplicated under type-specific names.

## Completion Requirements

- Requirement-by-requirement checks.
- Required evidence and verification commands.
- Documentation and ledger updates required.

## Stage Results

- Fill in at the end of the stage.
- Include searches and verification run with outcomes.
- Include what was learned.
- Include changes made to `0-plan.md`, `evidence-index.md`, and `design-ledger.md`.
- Include reopened stages and altered Goal 2 dependencies.
- Leave explicit next work and assumptions to challenge.
```

## Foundation Verification

- CSV contains exactly 45 unique nonempty `ca_type` values.
- Every CSV row has one stable `TNN` identifier and one planned type stage.
- `evidence-index.md` and `design-ledger.md` exist before T01 begins.
- All top-level runtime modules and corresponding tests have been read and recorded.

## Per-Type Verification

- Search log is reproducible and has no unresolved candidate match.
- Every excerpt has a resolvable source and line reference.
- Construction model accounts for all variants and parameters found.
- API and runtime comparisons cite actual definitions and tests.
- Every new primitive has direct evidence and no existing semantic equivalent.
- Goal 2 handoff has files, dependencies, tests, examples, and completion evidence.
- Global ledgers and `0-plan.md` reflect the result.

## Final Verification

- Mechanically compare the 45 CSV names with completed stage files, `evidence-index.md`, and `../goal-2/goal-2-handoff.md`.
- Audit duplicate excerpts and unresolved search candidates.
- Audit proposed abstractions for family branches, `Any`, unrestricted callbacks, hidden state, fake capacity, global formula bypasses, and semantic padding.
- Confirm all contradictions and reopened stages are resolved.
- Confirm Goal 1 changed only `goal-1/` unless the user explicitly authorized otherwise.
- Run `git diff --check` and inspect the final diff.
