# 3-AUDIT-HARNESS

Status: **COMPLETE** after adversarial reclosure, independent system/history
signoff, and the Stage 4 interleaved-evidence regression.

## Current Facts

- Stage 1 fixes the blind-discovery vocabulary, evidence contract, lifecycle
  rules, and final proof obligations.
- Stage 2 binds the audit to 29 ordered Book documents, 14,311 deterministic
  source units, 1,607 physical images, and 1,314 live image references.
- The initial reading ledger has exactly one hash-bound `PENDING` row for every
  source unit.
- The initial asset ledger has exactly one `PENDING` row for every physical
  image, including all 293 unreferenced physical images.
- The initial candidate and search ledgers are empty, and the cross-reference
  ledger contains only its exact header.
- No reconciliation data file exists during blind discovery.
- Every later blind mutation is represented by one atomic, hash-chained
  `V######` transaction. Replaying those transactions from the empty initial
  state must reproduce all six mutable ledgers and the latest per-path
  snapshots exactly.
- The generated empty state remains byte-reproducible as the Stage 4 baseline.
  The live audit has since advanced validly through Stage 4: 157 reviewed
  units, 2 screened assets, 2 active candidates, 4 pending cross-range routes,
  2 LOCAL rounds, and 3 atomic review-history events.

## Updated Assumptions

- A syntactically valid ledger is not sufficient. The validator must recompute
  ownership, provenance, aggregate status, discovery order, reverse joins,
  search results, and lifecycle closure from canonical inputs.
- Candidate provenance may be text-only, image-only, or mixed. An image is
  direct mechanics evidence only after native-evidence classification,
  original-resolution inspection, and checked transcription.
- A frontier/source unit may discover a cross-stage route that cannot be closed
  immediately. Route scope therefore distinguishes `WITHIN_STAGE`, which must
  close at the owning stage gate, from `CROSS_RANGE`, which must close by Stage
  18.
- Candidate correction cannot silently rewrite identity. Merge and split
  tombstones preserve provenance and require explicit evidence reassignment to
  terminal active candidates.
- Search reproducibility requires an executable query language, not merely a
  stored prose query or result count.
- Final-state validity is not enough for append-only history. Every event
  prefix must independently satisfy candidate, evidence, lifecycle, route,
  search, provenance, and reverse-join invariants; a later transaction cannot
  legitimize an invalid earlier state.
- A final missing-target decision requires complete sequential review, complete
  asset screening, exact LOCAL search closure for every applicable
  stage/epoch, and a current-epoch Stage 18 SATURATION round whose query scopes
  cover exactly all 29 canonical documents.
- A search fixed point additionally requires zero pending routes, a final
  zero-delta full-corpus saturation rerun, and exact ordered replay of the
  top-level vocabulary from each round's declared `new_vocabulary`.
- Worker bundles can reduce accidental information leakage, but filesystem
  sealing is not an operating-system security boundary. Actual blind
  delegation requires a separately enforced runtime sandbox; otherwise reading
  remains coordinator-local.

## Big Picture Objective

Provide fail-closed, resumable audit ledgers and validators so that later
sequential reading, image inspection, candidate capture, route closure, local
search, saturation, and reconciliation can be checked against the canonical
corpus rather than accepted as narrative claims.

## Allowed Inputs And Scope

Allowed:

- Stage 1 guardrails and their machine-readable contract;
- Stage 2 corpus manifest and source-unit ledger;
- canonical Book bytes and images solely for hash/provenance verification;
- Goal 4 schemas, tools, generated ledgers, and tests.

No Book construction was classified. No T identifier, current taxonomy
mapping, API-fit judgment, Goal 1 conclusion, Goal 2 design, or runtime support
claim was added to a blind artifact. Writes remained under `goal-4/`.

## Source Coverage

The initializer created:

- 14,311 reading rows in canonical unit order;
- 1,607 asset rows in deterministic physical-path order;
- 0 candidates;
- 0 cross-reference rows;
- 0 search rounds.

Every reading row carries immutable source identity, assigned stage, discovery
epoch, review status, disposition fields, candidate/support/route joins, and
review metadata. Every asset row carries independently recomputable ownership,
physical hash, reference data, stage assignment, inspection state, visual
role/risk flags, candidate/route joins, and review metadata.

The 293 unreferenced images receive deterministic document/stage ownership from
their unique directory and page-number range. The validator independently
rederives that assignment rather than trusting the generated row.

## Candidate Changes

No Book candidate was created at this stage. The candidate contract now
supports:

- stable `B####` allocation by immutable discovery epoch and frozen traversal;
- typed source-unit, image, and search-hit discovery anchors;
- exact source-unit/image/route provenance and reverse joins;
- stable `E######` evidence and `G######` evidence-group identities;
- text-only, image-only, and mixed evidence;
- complete closed semantic fingerprints with field-level evidence
  declarations;
- explicit source quality, evidence strength, uncertainty, missing mechanics,
  parameters, variants, and relations;
- active, merged, and split lifecycle states;
- acyclic multi-level lineage with terminal active descendants;
- provenance-preserving merge/split coverage and explicit evidence
  reassignment.

Tombstones retain their historical witnesses but cannot remain linked from live
reading or asset rows. Active candidates cannot carry a definitive lifecycle
edge.

## Search And Evidence Log

No construction query was executed, because sequential reading has not begun.
The harness freezes the future search language:

- query mode is `LITERAL` or Python Unicode multiline `REGEX`;
- case sensitivity, whole-word behavior, ordered scopes, query family, and
  assumptions are explicit;
- results are recomputed from canonical byte slices in query order and source
  unit order;
- every hit has a stable identity, context digest, and governed disposition;
- candidate, evidence-group, and route deltas use typed discovery anchors;
- local rounds are stage/range bound;
- saturation rounds begin only after complete reading and asset screening;
- the last Stage 18 round must reproduce a zero-delta fixed point over all 29
  documents.

Search result lists and digests cannot be self-reported: the validator reruns
the frozen queries and compares exact query/unit pairs and context hashes.

## Detailed Implementation Plan

Completed:

1. Added `tools/audit_contract.py` as the shared allowlist-only contract.
2. Added `tools/initialize_audit.py` and generated exact initial ledgers.
3. Generated seven blind schemas:
   - reading row;
   - asset row;
   - cross-reference row;
   - candidate record;
   - search rounds;
   - worker output;
   - atomic review-history event.
4. Generated two reconciliation-only schemas:
   - classification row;
   - coverage row.
5. Added `tools/validate_audit.py` for source binding, schemas, joins, stage
   gates, query replay, lifecycle closure, and mutation checks.
6. Added `tools/build_worker_bundle.py` for copied, hash-bound, read-only,
   range-limited worker inputs and exact completed-output validation.
7. Added `tools/merge_worker_output.py` for dry-run-first coordinator merges,
   stale-projection detection, worker-ID remapping, full proposed-state
   validation, and same-filesystem staged writes.
8. Added `tools/audit_transaction.py` for cooperative locking, durable
   journaling, atomic six-ledger replacement, and deterministic crash
   recovery.
9. Added focused tests for guardrails, corpus reconstruction, audit replay,
   coordinator operations, transactions, and initialization.

The review-history transaction modes are:

- `INITIAL`: atomically completes the next canonical unread path or path set;
- `REOPEN`: atomically replaces a previously reviewed path projection in a
  new epoch and clears a prior fixed point when applicable;
- `SEARCH_APPEND`: appends exactly one LOCAL or SATURATION round and atomically
  carries its row, asset, candidate, route, and evidence changes;
- `ROUTE_RESOLUTION`: performs the only governed pending-route transition;
- `CANDIDATE_REVISION`: performs Stage 18 append-only candidate enrichment,
  merge, or split changes with exact affected-path rewrites.

One `V######` identifies the whole coordinator transaction, including
multi-path review. Candidate, route, search, and path changes carry full
before/after snapshots and hash chains. Replay validates each closed prefix,
not just the terminal ledgers.

The worker namespace is deliberately separate:

- candidates: `W0001...`;
- routes: `WR0001...`;
- evidence: `WE000001...`;
- evidence groups: `WG000001...`.

The coordinator deterministically maps those append-only identities into the
global `B/R/E/G` namespaces and rewrites all nested joins. Worker output cannot
resolve routes, perform coordinator search, assign reconciliation fields, or
reassign tombstone evidence.

Worker evidence allocation is global to the frozen discovery traversal, not
candidate-record order. A candidate may therefore own nonconsecutive worker
evidence IDs when another candidate is discovered between its first and later
support. The verifier flattens all evidence, requires the complete unique
`WE000001...` sequence, checks source/image anchor monotonicity in numeric WE
order, and orders WG groups by their first WE. The coordinator uses that same
numeric order for global `E/G` allocation. Stage 4 exercises the case
`B0001={E000001,E000003}` and `B0002={E000002,E000004}`.

Prepared merge plans are immutable mappings with a validation token covering
all original bytes/modes and all proposed ledger bytes. Apply recomputes that
token before entering the transaction. The initializer has no reset or
`--force` path and refuses to overwrite any existing mutable ledger.

The transaction layer uses a persistent advisory lock for cooperating tools,
fsynced `PREPARED`/`COMMITTED` journal states, complete base/proposed staging,
and deterministic recovery:

- all base files present: discard an uncommitted journal;
- all proposed files present: finalize a committed journal;
- mixed base/proposed state: restore the complete base state;
- any unknown target state: retain the journal and fail closed.

Unique mode-`0600` scratch files prevent read-only final modes from blocking a
crash retry; final modes are applied only at the atomic install boundary.
Consistent multi-ledger readers use the same read guard. This is a cooperative
durability contract, not a claim that arbitrary lock-free readers see six
POSIX renames as one filesystem operation.

## No-Cheating Checks

- Blind schemas reject unknown fields and recursively reject T-ID, catalog,
  family, API, runtime, and executor leakage.
- Static source fields and hashes are compared to the independent corpus map.
- Reading dispositions enforce exact candidate/support/route joins in both
  directions.
- Asset paths, hashes, reference ownership, and unreferenced-image assignment
  are independently recomputed.
- Construction-bearing, text-bearing, ambiguous, caption-incomplete, and source
  defect images trigger stronger original-resolution/transcription rules.
- Candidate source status and evidence strength are recomputed from linked text
  and images.
- Candidate/evidence discovery anchors must follow the frozen epoch traversal
  and contiguous global allocation.
- Every event prefix has contiguous `E######`/`G######` allocation, exact
  candidate/evidence joins, available discovery anchors, matching
  search-hit/source witnesses, and a complete provenance-preserving lifecycle
  graph.
- Merge/split graphs must be acyclic, provenance-covering, and terminate in
  active descendants; evidence reassignment preserves canonical witnesses.
- Cross-reference routes have typed sources/targets, exact backlinks, and
  stage-sensitive closure gates.
- Search rounds are replayed against canonical source bytes; stale result or
  context digests fail.
- Search vocabulary is the exact ordered concatenation of per-round declared
  additions; undeclared top-level terms fail.
- `MISSING_TARGET_FINAL` cannot be reached from partial review, missing LOCAL
  closure, a partial-corpus saturation round, or a saturation round from a
  stale pre-reopen epoch.
- A fixed point cannot coexist with a pending route or precede complete
  reading, screening, and LOCAL closure.
- Reconciliation files are forbidden before Stage 19, while their future
  schemas are already closed and enum-typed.
- Sealed bundles reject symlinks, hardlinks, special files, writable inputs,
  unexpected paths, stale projections, incomplete assignment coverage, and
  invalid worker-local identity sequences.
- Merge defaults to a non-mutating preview and validates the entire proposed
  global state before any explicit apply.
- The six-ledger apply path rejects stale or mutated prepared plans and
  recovers every tested crash boundary, including read-only target modes.
- The full harness runs from a byte-for-byte relocated corpus copy.
- Validation passes under ordinary and optimized Python; correctness does not
  depend on `assert`.

## Completion Requirements

| Requirement | Evidence |
|---|---|
| Detect missing/duplicate units and stale sources | Exact manifest/source-unit reconstruction plus destructive mutations |
| Enforce resolvable candidate provenance and complete joins | Closed candidate/evidence schemas and bidirectional reading/asset/route validation |
| Govern cross-reference and search queues | Typed routes, stage gates, executable search replay, and hit-disposition mutations |
| Govern every physical image | 1,607 exact initial rows, independent owner recomputation, and risk-sensitive inspection rules |
| Keep blind discovery free of reconciliation/API conclusions | Recursive forbidden-key/text scan and absence of reconciliation data files |
| Support safe resumable work | Non-overwriting initializer, stage gates, sealed range bundles, hash-chained event replay, immutable prepared plans, and journaled six-ledger coordinator |
| Fail under meaningful corruption | Source, link, asset, provenance, lifecycle, search, bundle, merge, and schema mutation cases |
| Run from root and a relocated copy | Focused test suite, including independent copied source tree |
| Leave a valid Stage 4 starting state | Initial artifacts reproduce byte-for-byte and global validator reports zero reviewed work with no unresolved invalid row |

## Stage Results

Commands and outcomes:

```text
python3 goal-4/tools/initialize_audit.py --check-initial
  initial audit artifacts reproduce exactly

python3 goal-4/tools/validate_guardrails.py --self-test
  validated Goal 4 guardrails and mutation checks

python3 goal-4/tools/verify_corpus.py --self-test
  verified corpus map and mutation checks:
  documents=29 images=1607 units=14311

python3 goal-4/tools/validate_audit.py --self-test
  validated blind audit harness and mutation checks:
  units=14311 reviewed=0 candidates=0 routes=0
  assets=1607 screened=0 rounds=0

python3 -m py_compile goal-4/tools/*.py
  passed silently

uv run --with pytest pytest -q goal-4/tools/test_audit.py
  15 passed

uv run --with pytest pytest -q goal-4/tools/test_merge_worker_output.py
  36 passed

uv run --with pytest pytest -q goal-4/tools/test_prepare_review_output.py
  8 passed

uv run --with pytest pytest -q goal-4/tools/test_audit_transaction.py
  22 passed

uv run --with pytest pytest -q goal-4/tools/test_initialize_audit.py
  4 passed

git diff --check -- goal-4
  passed silently
```

The audit-validator mutation suite rejects, among other cases:

- a missing or stale reading row;
- broken candidate/source/image/route reverse provenance;
- a false field-evidence declaration;
- forbidden blind keys or text;
- an incorrectly assigned unreferenced image;
- high-risk image evidence without original-resolution review;
- stale query or context digests;
- an undispositioned or falsely governed search hit;
- invalid evidence groups;
- an open within-stage route;
- broken multi-level merge/split evidence reassignment.
- an invalid candidate or route at any historical `V` prefix even when a later
  transaction repairs the final ledger;
- evidence anchored to a future or mismatched search hit;
- noncontiguous prefix evidence/evidence-group allocation;
- undeclared top-level search vocabulary;
- premature fixed points and premature final-missing routes.

The coordinator tests additionally reject invalid completed bundles, stale
input projections, and global ID collisions, and prove that preview is
non-mutating, explicit apply uses validated staging, all four worker ID
families are rewritten, and search state is preserved. They also prove that:

- evidence allocation remains source/image ordered when support for one
  candidate is interleaved with another candidate's discovery, while gap,
  duplicate, group-order, and out-of-traversal mutations fail;
- final-missing route resolution remains reachable after full review, LOCAL
  closure, and a non-fixed current-epoch full-corpus saturation round;
- a 28/29-document saturation scope is rejected;
- a 29/29-document scope is accepted;
- epoch-1 saturation is stale after an epoch-2 reopen;
- a fixed point is rejected with missing LOCAL closure, a pending route, or
  undeclared vocabulary.

Independent final QA reproduced those same boundary cases through normal
coordinator operations. System QA passed 34 targeted regression checks and
signed off. History/replay QA passed its focused history subset, independently
observed `28/29` rejection, `29/29` acceptance, and stale-epoch rejection, and
signed off.

Re-integration answers:

1. No corpus-map defect was found.
2. No Book vocabulary or semantic route was opened.
3. No candidate was created, split, or merged.
4. Every initial unit and physical image has exactly one pending obligation;
   there are no hits or routes yet.
5. Source ambiguities will be captured as orthogonal source/evidence status,
   never silently repaired.
6. Semantic reuse was not evaluated.
7. Stages 1 and 2 remain closed.
8. The guardrail machine contract was strengthened for discovery epochs,
   visual risk, route closure, query replay, evidence groups, and lineage.
9. The audit remains independent of the current taxonomy count and API.
10. At original Stage 3 completion the exact next stage was `4-BOOKENDS`.
    That stage is now complete; the harness remains closed and the live audit
    resumes at `5-CH01-FOUNDATIONS`.
