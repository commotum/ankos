# Goal Index

## Completed and Preserved

1. [Goal 1](goal-1/0-plan.md) — book-grounded investigation and architecture
   planning for the original 45-entry construction catalog. Complete; it
   produced the frozen Goal 2 handoff.
2. [Goal 2](goal-2/README.md) — the original implementation and conformance
   handoff. Frozen as a comparison baseline; it is evidence for the completed
   Goal 6 remaster and completed Goal 7 implementation, not the current plan
   to execute.
3. [Goal 3](goal-3/0-plan.md) — source-verified correction and release of the
   canonical *A New Kind of Science* Markdown corpus. Complete; its compact
   historical plan and release record remain.
4. [Goal 4](goal-4/README.md) — retired whole-book audit attempt. Its stale
   generated machinery was removed; one archival record remains.
5. [Goal 5](goal-5/taxonomy-census.md) — completed whole-book construction
   taxonomy and five-field API audit. Complete: 60 executable semantic
   families, two close non-family roles, 41 family-level additions, and no
   unresolved taxonomy/API questions. Its remaster boundary is
   [integration-handoff.md](goal-5/integration-handoff.md).
6. [Goal 6](goal-6/0-plan.md) — completed architecture remaster. It rebuilds
   the frozen Goal 2 plan around
   `SimpleProgram(seed, alphabet, frontier, neighborhood, rule)`, the finalized
   core/catalog structure, and the design inventory for all 60 audited
   families without changing runtime behavior. Its exact mechanics-first
   implementation contract is
   [goal-7-handoff.md](goal-6/goal-7-handoff.md).

## Reopened

7. [Goal 7](goal-7/0-plan.md) — five-field runtime implementation. The
   immutable `SimpleProgram`, family-blind `apply`, rollout, serialization,
   and individually implemented presets are preserved. The prior claim that
   callable wrappers implemented all 60 audited families is withdrawn: the 60
   canonical family names are development stubs and progress markers, not
   completed family builders or validators. Consequently the catalog portion
   of Goal 7 is reopened and `0.2.0` is not a release candidate. The historical
   stage and release records remain in `goal-7/` as records of the superseded
   conclusion.

## Current State

Goal 5 remains the semantic authority and Goal 6 remains the architecture
baseline. Goal 7's runtime core is preserved, but its catalog implementation
is incomplete. No later numbered goal is scaffolded and there is currently no
release candidate. Future progress must distinguish implemented presets from
canonical family stubs and must not count a taxonomy name as an implementation.
Goal 2 remains frozen evidence; Goal 4 is superseded and excluded from the live
path.

The canonical book source used by current and future work begins at
[Contents.md](ref/A-New-Kind-of-Science/Contents.md), whose 29 document links
resolve.
