# Goal 4 Execution Loop

This loop governs every stage in `goal-4/0-plan.md`. The plan is authoritative but revisable when direct Book evidence or verification invalidates an assumption. Goal 4 audits and classifies; it does not implement runtime changes or mutate the existing catalog without separate authorization.

## Phase Boundaries

### Blind discovery: Stages 1–18

- Discovery uses `principles.md`, the canonical Book corpus, Goal 4 guardrails, and Goal 4 ledger schemas.
- Discovery candidates use provisional `B####` IDs.
- Do not consult or import T01–T45 mappings, `CA-Types.md` summaries, Goal 1 type conclusions, Goal 2 plans, `api.md`, `simple_programs.md`, or `src/ca` to decide what the Book contains.
- Do not claim cognitive amnesia. Instead, make the artifacts structurally independent: no T-ID mapping columns, API-fit fields, or existing-family dispositions are allowed before the blind candidate ledger is frozen.

### Reconciliation and semantics: Stages 19–21

- Freeze hashes of blind discovery artifacts before opening current taxonomy and architecture materials.
- Reveal and reconcile T01–T45 without rewriting the blind evidence record.
- Assign orthogonal catalog, semantic-role, and family actions before grouping semantic families.
- Evaluate API pressure only after Book taxonomy has been decided.

### Hostile closure and reporting: Stages 22–23

- Independent review may reopen any earlier stage.
- No waiver, deadline, preferred count, or green validator substitutes for resolving a substantive finding.
- Final integration outside `goal-4/` remains a handoff unless the user explicitly authorizes it.

## Repeatable Loop

1. Sync current state with actual repository files, source hashes, Git diff, completed stage files, ledgers, work queues, and verification results.
2. Read `principles.md`, `goal-4/0-baseline.md`, and update `goal-4/0-plan.md` with current facts before starting the next stage.
3. Select the first incomplete stage whose dependencies are satisfied; reopen an earlier stage first when later evidence invalidates it.
4. Create or refresh `goal-4/[INDEX]-[SHORTHAND].md` from the stage template below.
5. Implement only that stage. In Goal 4, implementation means corpus accounting, sequential reading, evidence capture, classification, verification, or reporting—not runtime or catalog integration.
6. Add verification and no-cheating checks that directly cover the stage requirements.
7. Run focused checks, the current full audit-verifier set, relevant mutation/relocation checks, and whitespace/diff checks.
8. Record facts, searches, source coverage, candidate changes, cross-references, classifications, commands, and outcomes in the stage file.
9. Fold results back into `goal-4/0-plan.md` and the shared Goal 4 ledgers; update assumptions and reopen contradicted stages.
10. Continue toward the original objective. If stopping for the session, leave the goal resumable with exact ledger state, open queues, next source unit/stage, failed checks, unblock actions, and assumptions to challenge.

## Global Invariants

- Do not narrow the user's objective without saying so.
- Do not mark a stage complete without requirement-level evidence.
- Do not use search counts, hashes, tests, or green checks as evidence unless they cover the actual requirement.
- Prefer small, low-complexity stages that narrow uncertainty.
- Convert blockers into work items: decompose them, route around them, or turn them into explicit proof, source-repair, and verification tasks.
- Preserve the distinction between Book evidence, taxonomy, semantic equivalence, API fit, implementation, verifier, diagnostic, and fallback paths.
- Preserve the distinction between a coverage entry and a semantic family.
- Do not protect the current count of 45 or pursue a larger count as a success metric.
- Do not infer mechanics from a name, Index entry, nearby image, historical mention, or external definition.
- Do not classify by current API convenience or runtime support.
- Do not call two constructions equivalent through opaque state packing, arbitrary callbacks, hidden schedules, source interpreters, lossy projections, or multi-step emulation.
- Do not fabricate semantics when the Book is incomplete or contradictory.
- Do not treat random initial conditions, stochastic transition laws, external draw streams, finite PRNG realizations, and observed distributions as interchangeable.
- Do not treat a solver trace as a constraint's native evolution, a numerical integrator as a PDE's identity, a renderer as a construction, or an emulation as the emulated system's native mechanics.
- Do not edit Book files, `ref/notes`, Goal 1, Goal 2, root API documents, `src/ca`, or tests during Goal 4 without explicit authorization.
- Do not create empty future stage files. Create a stage file only when its stage begins.

## Start-of-Stage Sync

Before any stage work:

1. Read `goal-4/0-plan.md`, this loop, the previous completed stage, and current shared-ledger summaries.
2. Run `git status --short` and identify all pre-existing user changes. Preserve them.
3. Verify canonical Book and asset hashes against `corpus-manifest.json` once that artifact exists.
4. Run current Goal 4 validators before editing.
5. Confirm the stage's allowed source inputs and phase boundary.
6. Record the exact starting counts for source units, reviewed units, candidates, cross-reference queue, asset queue, search hits, catalog/role/family classifications, and hostile findings as applicable.
7. If source drift is detected, stop classification work and reopen `2-CORPUS-MAP` and `3-AUDIT-HARNESS`.

## Source-Unit Review Procedure

For every assigned canonical range:

1. Load source units in canonical order; do not start from search results.
2. Read the complete unit and enough surrounding context to understand its role.
3. Classify the unit's reading-ledger role:
   - `CANDIDATE`
   - `SUPPORTS_CANDIDATE`
   - `CROSS_REFERENCE`
   - `REPRESENTATION_OR_OBSERVER`
   - `APPLICATION_OR_EMULATION`
   - `HISTORICAL_ONLY`
   - `NO_CONSTRUCTION`
   - `SOURCE_DEFECT_OR_AMBIGUITY`
4. Create or link a B candidate whenever the source may specify mechanics. Err toward capture during discovery; final exclusion happens later.
5. Record canonical path, logical line span, page/section if recoverable, unit ID/hash, evidence role, and a concise evidence statement.
6. Inspect every owned image reference. Link its physical basename/path/hash, caption/context, evidence role, and whether visual inspection was necessary.
7. Queue every relevant page, section, Notes, alias, or Index route. Never rely on memory to follow it later.
8. After sequential reading, run the range-local trigger and alias searches and reconcile every hit to a reviewed unit.
9. Verify all assigned units/images have dispositions and all local hits are governed before the stage can close.

## Candidate Evidence Contract

Each `B####` candidate must contain:

- stable ID and provisional source-derived name;
- all names, aliases, spellings, and named variants found;
- canonical source units and split/image witnesses;
- evidence role and strength for each source;
- complete semantic fingerprint fields from `0-plan.md`;
- known parameters, profiles, and underdetermined variants;
- exact uncertainty and missing-mechanics fields;
- related candidate IDs without premature equivalence;
- all queued and resolved cross-references;
- no T mapping or API-fit judgment before Stage 19.

Short excerpts may be retained when necessary to pin exact mechanics, but do not duplicate large Book passages. Provenance, concise paraphrase, formulas, and figure identity should carry most of the ledger.

## Cross-Reference Protocol

- Give every relevant route a stable ID.
- Record the source unit, literal target wording/page, route kind, expected topic, owning stage, and status.
- Resolve a route only after reading the target in context.
- If a target is missing or OCR-corrupt, record searches attempted and the evidence boundary.
- A route that discovers new vocabulary must seed the next saturation round.
- Stage 18 cannot complete until the queue is empty or every missing target has a final explicit defect record.

## Asset Protocol

- Map every canonical image reference to its resolved physical file and hash.
- Give every reference an asset-ledger row even when the image is non-constructional.
- Visually screen every physical image at least once; contact-sheet or thumbnail review is acceptable for initial screening.
- Classify the image role as `NATIVE_EVIDENCE`, `RELATION`, `CONTROL`, `OBSERVER`, `DECORATIVE`, or `SOURCE_DEFECT`.
- Record total `visually_screened` status. Inspect construction-bearing, text-bearing, ambiguous, or caption-incomplete images at original resolution and record whether limited transcription was required.
- Do not derive hidden rule tables, exact colors, coordinates, or timings from pixels unless the image visibly and unambiguously establishes them and the transcription is independently checked.
- Proximity to candidate prose does not make an image native evidence.

## Search-Saturation Protocol

1. Freeze each search family and tool/version assumptions.
2. Search headings, captions, Notes labels, Index vocabulary, construction nouns, mechanism verbs, schedules, probability language, constraints, generators, equations, inputs/outputs, implementations, and all candidate-derived aliases.
3. Store result IDs/digests and partition every hit into:
   - governed candidate/support;
   - duplicate;
   - cross-reference;
   - control/relationship;
   - exclusion.
4. Inspect context; search hits alone are not evidence.
5. Add newly discovered aliases, operations, examples, and parameters to the next round.
6. Repeat until a full round adds no vocabulary, candidate, evidence, or unresolved route.
7. Mutation-test removal of a hit disposition so the verifier proves there is no silent remainder.

## Orthogonal Reconciliation Fields

After Stage 18 freezes blind discovery, assign every candidate one value on each axis.

`catalog_action`:

- `EXISTING_ENTRY_SUFFICIENT`
- `EXISTING_ENTRY_NEEDS_CORRECTION`
- `ADD_CATALOG_ENTRY`
- `NO_SEPARATE_CATALOG_ENTRY`
- `INSUFFICIENT_BOOK_EVIDENCE`

`semantic_role`:

- `NATIVE_TRANSITION_OR_GENERATOR`
- `STOCHASTIC_OR_BRANCHING_PROCESS`
- `INPUT_PROCESSOR_OR_TRANSDUCER`
- `RELATION_CONSTRAINT_OR_MODEL_SET`
- `IMMUTABLE_DEFINITION_OR_QUERY`
- `SPECIALIZATION_OR_PRESET`
- `PROPERTY_OR_RESTRICTION`
- `SEED_INPUT_OR_BOUNDARY_CLASS`
- `COMPOSITION_OR_HYBRID`
- `REPRESENTATION_CODEC_OR_OBSERVER`
- `APPLICATION_OR_EMULATION`
- `DUPLICATE_OR_ALIAS`
- `SOURCE_INSUFFICIENT_ROLE`

`family_action`:

- `EXISTING_SEMANTIC_FAMILY`
- `NEW_SEMANTIC_FAMILY`
- `SOURCE_INSUFFICIENT_FOR_FAMILY`

Do not retain `AMBIGUOUS` or `UNRESOLVED` on any axis at final closure. If the Book genuinely does not decide the mechanics after exhaustive search, the source-insufficient values are the honest resolved result and must state exactly what is missing. `ADD_CATALOG_ENTRY` does not imply `NEW_SEMANTIC_FAMILY`.

## Distinctness and Reuse Tests

### Exact existing coverage / same semantic family

Require:

- complete source-grounded fingerprints for both sides; and either:
  - an explicit total structural map on valid configurations/denotations, an inverse on the mapped image, and one-native-event/result commutation; or
  - proof that both are instances/restrictions of the same explicit parameterized semantic schema with unchanged native mechanics.
- In both cases preserve immutable program data, invariants, target selection, schedule, read snapshot, writes/replacement, branching/probability, failure/completion, witnesses, and event granularity without a hidden source interpreter.

### Specialization, preset, property, or seed class

Require:

- named base construction;
- exact parameter restriction, predicate, constructor, or input law;
- proof that native mechanics are otherwise unchanged;
- separate evidence identity when the Book name still deserves catalog coverage.

### Composition or hybrid

Require:

- named component constructions;
- an explicit coupling law, data flow, and schedule;
- proof whether composition is generic reuse or introduces a new coupling algebra;
- no hiding one component inside another's value.

### Representation, observer, application, or emulation

Require:

- exact source role;
- absence of a new native construction law, or an explicit map to the construction being observed/applied/emulated;
- no promotion of rendering, measurement, solver, or decoding steps into native events.

### New catalog entry

Require:

- sufficient Book identity and evidence to justify independent traceable coverage;
- a stated semantic role and family action;
- a source-grounded reason that folding the name into another catalog row would lose a Book obligation.

A new catalog entry may reuse an existing semantic family. It does not need a family-novelty counterexample.

### New semantic family

Require:

- sufficient Book evidence to instantiate the construction;
- nearest existing candidate/family comparison;
- a concrete event, result, or denotation whose state, schedule, reads, probability, structure, successor cardinality, completion, or witnesses cannot be preserved by the nearest family;
- proof that the difference is not merely a parameter, property, seed, representation, composition, observer, or another instance of one explicit parameterized schema;
- independent hostile review.

## Re-Integration Questions

At the end of every stage, answer:

1. Did this stage expose a corpus-map or source-unit defect?
2. Did it introduce new vocabulary or cross-references requiring earlier/later review?
3. Did it split or merge a provisional candidate?
4. Are all assigned units, hits, images, and routes governed?
5. Did a source ambiguity become resolvable, or must it remain explicit?
6. During reconciliation, does a reuse claim preserve complete native semantics one event for one event?
7. Which completed stages must reopen?
8. Which shared ledgers and final-report assumptions change?
9. Is the audit still independent of a preferred taxonomy count or API outcome?
10. What is the exact next resumable unit/stage?

## Stage File Template

```markdown
# [INDEX]-[SHORTHAND]

## Current Facts

- Facts from current source manifests, ledgers, repository state, and previous stage results.

## Updated Assumptions

- Assumptions that still look valid.
- Assumptions that changed.
- Assumptions that need evidence or tests before being trusted.

## Big Picture Objective

- Restate the stage objective, adjusted for current facts.

## Allowed Inputs And Scope

- Files/ranges this phase may read.
- Files this stage may change.
- Blind/reconciliation boundary applicable to the stage.

## Source Coverage

- Canonical ranges and source-unit IDs assigned.
- Images/assets assigned.
- Starting and ending review counts.
- Cross-references opened and closed.

## Candidate Changes

- Candidates created, updated, split, merged, or left source-insufficient.
- Semantic-fingerprint fields changed.
- No final taxonomy mapping during blind stages.

## Search And Evidence Log

- Sequential review record.
- Queries/search rounds run after reading.
- Match dispositions and new vocabulary.
- Source defects and split/image witnesses.

## Detailed Implementation Plan

- Concrete audit, ledger, tool, and documentation changes for this stage.
- Files expected to change.
- New validators or commands required.

## No-Cheating Checks

- Checks proving sequential coverage was not replaced by keyword search.
- Checks enforcing the current phase boundary.
- Checks preventing unsupported semantic inference or convenient API fitting.

## Completion Requirements

- Requirement-by-requirement evidence.
- Required verification and mutation commands.
- Ledger and plan updates required.

## Stage Results

- Fill in at the end of the stage.
- Include commands run and outcomes.
- Include what was learned.
- Include ledgers and plan sections updated.
- Include reopened stages.
- Leave exact next work and assumptions to challenge.
```

## Focused Verification By Stage Kind

### Guardrails/corpus/harness

- Input hashes and file counts are independently derived.
- Segment/source-unit coverage has no gap or overlap.
- Split anomalies and asset joins are explicit.
- Schema/validator mutation cases fail as intended.

### Blind reading stages

- Assigned source-unit count equals dispositioned-unit count.
- Assigned image-reference count equals asset-ledger count.
- Every range-local search hit maps to a reviewed unit and disposition.
- Candidate links and provenance resolve.
- No T-ID mapping or API-fit fields were added.

### Index and saturation

- Every Index source unit/headword is screened, and every relevant Index lead and cross-reference has a final route record.
- Search result sets reproduce from frozen queries.
- Every hit is partitioned with no remainder.
- The final iteration is a real fixed point.

### Reconciliation/disposition/family stages

- Every T entry and B candidate participates in required joins.
- Every candidate has exactly one catalog action, semantic role, and family action.
- Proposed catalog additions have evidence packets and catalog-identity arguments.
- Proposed new families have nearest-family counterexamples.
- Same-family claims carry lossless native-result proofs or explicit shared-parameterized-schema proofs.
- Near-pair comparisons cover high-risk distinctions.

### Hostile/final stages

- Independent reviewers cover every proposed addition and close exclusion/collapse.
- Sampling spans every canonical segment and every value used on the three classification axes.
- All findings are resolved through owning-stage reclosure.
- Reports and counts are generated from verified ledgers.
- Scope, Markdown, diff, relocation, optimized-mode, and mutation gates pass.

## Final Verification

- Re-hash and independently parse the complete canonical corpus.
- Verify all 29 book documents, both navigation documents, all canonical logical lines, all 1,607 physical images, and every image reference are accounted for.
- Verify all source units have reading dispositions.
- Verify all search hits and relevant cross-references have final dispositions.
- Verify all candidates have complete provenance, fingerprints, and one value on each final classification axis.
- Verify all T01–T45 entries are independently rediscovered or diagnosed.
- Verify every proposed T46+ entry and close exclusion/collapse has hostile review; require nearest-family counterexamples only for new semantic families.
- Verify catalog and semantic-family counts are separately derived from ledgers.
- Verify no unsupported Book claim was silently repaired or inferred.
- Run all Goal 4 validators, mutation cases, relocation checks, byte-compilation/import checks, direct whitespace/fence checks over tracked and untracked `goal-4/**`, staged-diff checks when intentionally staged, and final scope inspection.
- Confirm only `goal-4/` changed unless the user separately authorized integration.

## Session Stop / Resume Contract

If work stops before completion, record in the active stage:

- last fully reviewed source-unit ID and canonical range;
- ledger hashes and row counts;
- open candidate, cross-reference, asset, and search queues;
- failing verification commands and exact output;
- source drift or dirty-worktree concerns;
- next safe command or source unit;
- assumptions most likely to fail next.

Never report the goal complete merely because the session ended, the source is large, or validators are green over an incomplete ledger.
