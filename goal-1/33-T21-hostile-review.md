# T21 Final Hostile Integration Review

Review target: `33-T21-2D-CA.md` and its source, asset, semantic, design-ledger, architecture-audit, plan, and evidence-index integration.

Review posture: independent and adversarial. The deliberately open stage/plan/evidence completion markers were treated as sequencing until this report exists, not as evidence defects.

## Findings

No material finding remains.

One low-severity runtime-audit wording error was found during review: the original `33-T21-2D-CA.md:284` said the 2D rollout tests exercised only rule `0`, while `tests/test_rollout.py` also exercises Dyadaxes rule `91` in its batch/loop parity case. The stage now says exactly what the tests establish: Dyadaxes-only coverage, direct rule-0 output, and rule-0/rule-91 batch parity. This repair does not affect D127.

## Source Closure

- The source oracle freezes the canonical Book, Atlas, catalog, and taxonomy hashes before interpreting evidence.
- Its 19-query union contains 283 unique lines: 222 pre-Index and 61 actual-Index.
- The pre-Index partition is exact: 180 retained plus 42 excluded. The exclusion classes close at `26 + 6 + 4 + 5 + 1 = 42`, with no remainder.
- The 158 governed continuations are disjoint from the 180 retained query hits, giving the repaired 338-line evidence set.
- The retained evidence partition is exact: `130 native + 75 relation + 133 control = 338`.
- The retained digest is `b6e1ac355e48891cf644372ba96271e6fcb637dcc15d9212e118612b0e82e227` everywhere it is cited.
- The 26-line seed/background/trace/realization repair has the frozen digest `9898b607ccc3a32a8dfc380f7efb5f68806c56dbe9af7e3b7c1932e33d6e45a7`.
- All 17 split documents are manifest-bound. The query reverse join closes at 281 records (`266 exact + 15 declared nonexact`), and retained evidence closes at `270 exact + 68 nonexact`; 66 nonexact records have explicit reverse joins and the remaining two are guarded monolith-only lines.
- Raw Book offsets, the distinct 10/6/32-case rule forms, parallel old-state update, discrete `t+2D`, configuration/support facts, seed/realization facts, and T22/T23/T24/Life controls are separately guarded. Neither actual-Index material nor close-family controls are silently promoted into strict T21 semantics.

Result: source closure is zero-remainder and its arithmetic, hashes, classifications, and cross-file description agree.

## Asset Closure

- The independent radius-four candidate universe contains 113 assets and partitions exactly as `53 governed + 60 adjacency-only`.
- The governed partition is `C10/C6/O/R/X22/X23/X24 = 10/2/4/12/14/8/3`, totaling 53.
- The separately retained adjacency ledger partitions as `30 typed boundary/relation + 5 application/property + 25 other construction`, totaling 60.
- Every one of the 113 candidates has one monolith reference, one split reference, one unique physical JPEG, byte count, dimensions, SHA-256, and an explicit role or exclusion reason. The combined reference count is therefore 226; the physical-file and unique-hash counts are both 113.
- The strict 16-asset subledger, 53-asset governed ledger, and 60-asset adjacency ledger reproduce the universe and metadata digests cited by the stage.
- Fourteen transcription records consume the declared gallery-code, slice, growth-count, offset, panel-label, and checkpoint tuples. Every record binds its tuple to both a governing retained source-line hash and a physical-asset hash. The transcript digest is `861b62b711faa82a7aee2d80a25921928b47c509f15e2c4d33bd8d18d5f10eba`.
- The audit is explicit that those records are `HASH_BOUND_NOT_PIXEL_REPLAYED`. It replays only source-determined code-1022/code-942 predicates, one-cell seeds, count checkpoints, background facts, and rule-schema facts.
- The random equal-sum gallery is correctly marked unreplayable because no serialized PRNG, seed, crop, or boundary is supplied. No pixel pattern is promoted into RULE or execution semantics.
- Printed-page/physical-filename offsets and the Notes/actual-Index split mispartition are guarded rather than assumed.

Result: `113 = 53 + 60` is an honest candidate closure, and the transcription evidence makes no machine-decoding or pixel-replay overclaim.

## Semantic and Representation Audit

- NEIGHBORHOOD is complete: `LocalAccess` requires exactly one explicit `SelfAccess` and unique ordered `OffsetAccess` components. Both finite and sparse reads iterate only those declared components; there is no hidden center read.
- The generic path uses all-sites selection, opaque snapshot-scoped handles, closed rule data, typed same-site assignments, validation against the exact old snapshot, and atomic parallel commit.
- The native 2D reference is genuinely independent of the generic rule path. It uses a row-major native carrier, literal Book row/column reads, and direct numeric formulas for the 32-context code, `Self + 2*CardinalCount`, and the five-value sum. It does not call the generic `CAProgram`, `LocalRead`, offsets, or `rule.evaluate` machinery.
- The 17,728 native/generic commutations reconcile exactly as `16,384 outer + 1,024 equal-sum + 80 positional + 34 general-basis + 125 nonaliasing directional + 81 ternary`.
- The five exact projection codes are pinned as `FFFF0000`, `FF00FF00`, `F0F0F0F0`, `CCCCCCCC`, and `AAAAAAAA`.
- Directional validation is not confined to an aliasing `2x2` torus. All five projections are checked from every one-hot source in a nonaliasing `5x5` box, and one-hot rows of the full 32-bit general codec are exercised in separate `5x5` states.
- The Book basis change is literal: `(row,column) -> (x=column,y=-row)`. The derived permutations are `runtime_to_book=(1,4,2,0,3)` and `book_to_runtime=(3,0,2,4,1)`. Five projections across all 32 contexts give 160 permutation cases.
- A concrete asymmetric `5x5` counterexample proves that re-sorting transformed offsets while reusing the Book table changes north projection into west projection. Applying the certified table permutation restores one-step commutation.
- All 1,024 `SelfValue x CardinalCount` tables expand and factor exactly; all 64 self-plus-cardinals sum tables do likewise. Directional, center-sensitive equal-total, and one-row-mutation adversaries prevent invalid quotienting.
- Native `Z^2`, finite periodic/fixed-boundary realizations, and uniform-background-plus-finite-deviations representations remain distinct. Code 1022 produces the exact `t0..t6` diamond supports; an evolving uniform background is represented visibly, while a fixed-background sparse lowering requires a quiescence proof.
- Old-snapshot versus in-place update, periodic versus fixed boundary, wrapped-slot multiplicity, exact type/snapshot provenance, and one/two/three-dimensional use of the same kernel are all adversarially checked.
- T22 changes the declared access to Self plus eight Moore offsets and runs through the same generic step function; it supplies a neighborhood boundary, not a new executor.

Result: the semantic evidence establishes three distinct schema-tagged 32/10/6-case RULE descriptions over one fixed-lattice CA execution algebra.

## Architecture and Runtime Integration

- D127 keeps DOMAIN as discrete `t+2D` only. CONFIGURATION owns fixed square-`Z^2` support/topology; finite boxes, quotients, exteriors, sparse backgrounds, work regions, axis maps, crops, and rasters are explicit realizations or views.
- The D127 RULE classification is class 3: the compact count/sum carriers are restrictions and lossless representations only for qualifying exhaustive maps. Their code integers are not cross-schema identities.
- FRONTIER is `AllSites`; NEIGHBORHOOD is explicit Self plus ordered cardinal offsets; UPDATE directly reuses old-snapshot parallel same-site assignment. No new execution algebra or shared semantic axis is introduced.
- T01/T02/T03/T08 are the smallest reusable composition. T22/T23/T24, Life, other lattices, weighted rules, stochastic profiles, observers, and relations remain explicit later-stage boundaries.
- The design-ledger D127 entry, architecture-audit D127 row, stage classification matrix, construction model, API-fit table, and Goal 2 composition agree on those responsibilities.
- The current runtime audit is accurate after the one wording repair: geometry/select/gather/vectorized-write mechanics are substantially reusable; named family dispatch, implicit finite-array identities, missing strict table schemas, and the unrelated majority-gated Dyadaxes preset are correctly identified as current limitations.
- The Goal 2 handoff is implementation-ready: it specifies the structural component composition, Book-frame access and ENU adapter, exact three rule schemas, factor/codec requirements, support/realization validation, conformance tests, and explicit no-cheating boundaries without prescribing a T21 executor.

Result: D127's class-3/no-new-UPDATE/no-new-executor conclusion follows from the evidence and does not reopen a completed stage.

## Verification Gates

- Source, asset, and semantic oracles pass from the repository root.
- All three oracles pass from a relocated `/tmp` tree bound back to the frozen source corpus.
- Optimized-mode executions fail closed before relying on stripped assertions.
- Silent imports and syntax compilation pass.
- Markdown fence parity and `git diff --check` pass.
- Scope remains inside `goal-1/`; no runtime, test, or root-document implementation was made by T21.
- `uv run pytest -q` passes: `102 passed`.

Verdict: CLEAN
