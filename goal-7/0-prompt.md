# Goal 7 Continuation Prompt

```text
Work through goal-7/0-plan.md using goal-7/0-loop.md.

The objective is to implement and ship the Goal 6 architecture as one coherent
0.2.0 runtime: exactly
SimpleProgram(seed, alphabet, frontier, neighborhood, rule), one family-blind
apply operation, rollout implemented through that operation, fail-closed
canonical serialization, and explicit ordinary catalog constructors for all 60
audited semantic families.

Read goal-7/0-plan.md and goal-7/0-loop.md in full. Inspect the actual repository
state and completed Goal 7 stage files, update current facts, and execute only
the first incomplete stage. Use goal-6/goal-7-handoff.md as the detailed
implementation sequence, goal-6/architecture.md for semantic/application
contracts, goal-6/catalog-migration.md for the exact SPF/F/T catalog ledger,
and goal-6/conformance.md for PX01–PX12, CT01–CT14, and family coverage.
Goal 5 remains semantic authority. Goal 2 is frozen selective evidence; do not
modify it. Do not reopen Book discovery or use Goal 4 machinery.

The existing target modules and tests are inert preparation. Imports,
NotImplementedError stubs, pending-name inventories, and 96 skipped obligations
are not implementation or conformance evidence. Remove each skip only when its
owning behavior is real, independently tested, and stage-authoritative.

Keep exactly five stored program fields. Seed owns initial configuration
sources; Alphabet owns closed value structure; Frontier is the complete
possible-write envelope; Neighborhood is the readable immutable-snapshot view;
Rule owns applicability, scheduling, conflicts, stochastic laws, stopping, and
complete atomic replacements. apply owns only generic validation,
reconstruction, commit, quotient, and measure projection.

Never dispatch application by SPF/F/T ID, family, constructor spelling,
catalog, carrier, locus kind, or Book class. Do not add a sixth field, second
executor, compatibility runtime, old-manifest fallback, callback-valued
semantic descriptor, opaque Any recipe bag, hidden solver, ambient RNG, silent
float fallback, or catalog-backed codec. Rollout must demonstrably reuse the
one apply operation. Datasets, RNG, and visualization remain downstream.

Execute stages in order:
1-ORACLES, 2-CUTOVER, 3-MECHANICS, 4-CODECS, 5-CATALOG,
6-CONFORMANCE, 7-RELEASE.

For each stage: sync actual state, update the plan, create or refresh its stage
file from the loop template, implement only that stage, add focused positive
and negative tests, run its no-cheating checks and the full active tests,
record exact evidence, fold durable facts back into the plan, and leave the
next action resumable. G7-01 is one atomic cutover boundary; G7-02 has three
workstreams but one aggregate barrier. Stages before 7-RELEASE are not
publishable release states.

Goal completion means the old executor and obsolete modules are gone; exactly
one application law remains; CT01–CT14, PX01–PX12, all eight secondary joins,
all 60 family rows, and the exact T01–T45 manifest pass; codecs, imports,
signatures, docs, lockfile, and installed-wheel behavior agree; no Goal 7
pending skip or scaffold stub remains; and one final hostile review finds no
sixth field, family dispatch, lossy compatibility path, observer leak, or
missing family.

Carry open issues forward as explicit work. If a real audited-family
counterexample breaks the contract, stop and report it rather than weakening
the goal.
```
