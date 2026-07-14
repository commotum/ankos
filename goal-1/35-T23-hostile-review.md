# T23 Final Hostile Integration Review

Review target: `35-T23-3D-CA.md`, its source, asset, and semantic oracles, D129 in `design-ledger.md`, the D129/T23 rows in `architecture-audit.md`, and T23's plan/evidence-index integration.

Review posture: independent and adversarial. The review treats `src/ca` as the current namespace and Phase 1 realization of the broader SimpleProgram library, never as the semantic boundary of a cellular-automaton-only library. A catalog name, source vocabulary, dimensionality, or differently shaped state decomposition does not justify a new state class, UPDATE algebra, or executor without a concrete one-step nonfit.

## Findings

No material finding remains.

Seven bounded defect groups were found and repaired during review:

1. **Medium — source closure and source-versus-inference provenance were incomplete.** The first source audit omitted the actual-Index route at `BOOK:21473` for localized structures in three dimensions. Query Q18 now freezes that route, and every union, partition, digest, split join, stage, ledger, architecture, plan, and evidence-index count was repaired. The Book's literal `(4,5,5)` tuple is now kept distinct from the derived canonical spelling `B5/S45`; the latter no longer appears in the source transcript.
2. **Medium — the asset universe was described as a fixed point that the oracle did not compute.** The oracle actually applies one source-proximity step around the complete retained set. The claim is now the exact declared one-hop radius-four universe: 42 plates, comprising ten governed and 32 adjacency-only candidates. It no longer implies iterative closure or a radius centered only on governed images.
3. **Medium — shell-only access had been silently widened with an unused Self read.** Direct six-face and twenty-six-neighbor shell predicates now declare no Self. Product and positional schemas declare exactly one Self. The typed read carrier permits either case and rejects mismatched access/schema combinations. This preserves the source distinction without adding an executor path.
4. **Medium — native/generic commutation originally left meaningful RULE rows unfired.** Small periodic quotients prove alias multiplicity but cannot realize every aggregate count. Separate nonaliasing `3x3x3` fixtures now fire all 14 face-product, seven face-shell, 54 full-product, and 27 full-shell indices with matching unit tables. The ternary fixtures now vary shell sums at fixed Self and require different outputs; majority and Carter Bays fixtures trigger nonvacuously instead of passing on all-zero successors. An asymmetric projection witness also proves that naive coordinate re-sorting without table permutation changes the program.
5. **Medium — large-table and compact-fiber claims were overstated or arithmetically imprecise.** A binary 27-position table has `2^27` finite rows and can be represented compactly; the astronomical quantity is the `2^(2^27)` rule space. D129 now requires immutable complete bounded data with exact lookup and serialization rather than an unrestricted callback or `numpy.int64` identity. Each individual full product fiber `(Self,n)` has multiplicity `binomial(26,n)`, while the combined Self pair has `2*binomial(26,n)` members. Compact bases are no longer described as exhaustive enumeration of arbitrary positional rules.
6. **Low — realization, seed, and runtime boundaries were too broad.** Exact evolving `(background, finite deviations)` representations no longer require quiescence; only carriers that fix or elide background evolution do. The strict source fixtures are now separated from derived axis choices and projection variants. Current scalar alphabets are correctly reported as sufficient for strict T23, while product/tagged alphabets remain a broader Goal 2 gap. Runtime citations now distinguish the mechanically rank-generic old-state kernel from the existing family-name dispatch around it.
7. **Low — final integration wording and counts lagged the repaired proof.** “Exact source coverage” was narrowed to the semantic oracle's actual selected-site/write claim. The commutation total was updated from 5,118 to 5,139 everywhere, all 102 explicitly fired compact indices are reported, and stale 81-index language was removed. T23, D129, the architecture audit, plan, evidence index, and T24 handoff now agree.

These repairs strengthen closure, provenance, representation fidelity, and conformance. They do not change D129's architecture classification.

## Source Closure

- The source oracle freezes the canonical Book, Atlas, catalog, taxonomy, and all 17 split-document hashes before interpreting evidence.
- Its 19-query union contains 151 unique monolith lines: 104 before the actual Index and 47 actual-Index routes. The union digest is `03268aed2534b66f807af417c006cf1a9209d195bc5d7f36d36b7a17134ae875`.
- The pre-Index partition is exact: 72 retained matches plus 32 classified exclusions, with no remainder. The exclusions are `7 other SimpleProgram/dimension + 13 other CA family/observer + 7 random/statistical model + 4 other geometry/physics + 1 broad rule phrase`.
- Sixty-six governed continuation lines join the 72 retained matches, producing 138 retained evidence lines. Their exact semantic partition is `76 native + 16 relation + 46 control = 138`, and their digest is `92ce01dbf10875f7549f3eedb180a9001c72c588494247ec13d6b9f5d7160c07`.
- The 47 actual-Index routes partition as `8 T23 + 8 T22/T24 + 17 T44 + 7 stochastic + 7 symmetry`. Q18 explicitly guards the previously omitted `BOOK:21473` localized-structure route.
- The query reverse join closes all 151 records as `142 exact + 9 mapped variants`. The retained reverse join closes as `123 exact + 15 mapped variants`, with no monolith-only retained line.
- Source mechanics and architecture derivations remain visibly distinct. The Book supplies the cubic arrangement, shell predicates, `AxesTotal`/`FullTotal` formulas, positional ordering, display transform, Carter Bays tuples, and majority expression. `Z^3`, the `6/12/8` face/edge/corner decomposition, case/rule counts, the ENU adapter, integer serializations, and `B/S` spellings are derived and labeled as such.
- Direct shell rules, product rules, positional rules, seeds, old-snapshot update, finite realizations, observers, stochastic controls, other lattices, and T21/T22/T24 boundaries remain separately dispositioned.

Result: source closure is zero-remainder, reverse-closed, and provenance-safe. No catalog vocabulary or derived notation is presented as primary semantics.

## Asset Closure

- The declared candidate rule is one hop over every image line within four source lines of the complete 138-line retained set. It yields exactly 42 physical plates; it is not called an iterative fixed point.
- The candidate universe partitions without remainder as `10 governed + 32 adjacency-only`. The governed split is `2 six-face direct + 2 full-26 direct + 4 projection observers + 1 (4,5,5) moving-structure observer + 1 T24 control`.
- The adjacency-only split is `11 T22 + 1 T24 + 3 random-seed + 4 stochastic-update + 1 nonstep + 1 alternate-update + 11 relation`.
- Every candidate has one monolith and one split reference, giving 84 references, 42 physical files, 42 unique hashes, and no unresolved record.
- The nine-record transcript ledger binds the declared predicates, source-stated seeds/horizons, projection relations, and literal `(4,5,5)` label to source and asset hashes. Its digest is `07d1261a07ddd0f5ecb5fcf311335b2310d148174e1a09641070a6daa492deed`.
- The honest claim boundary is `HASH_BOUND=42`, `TRANSCRIBED=9`, and `PIXEL_REPLAYED=0`. No random configuration, probability distribution, renderer, crop, or voxel trajectory is reconstructed from an image.
- `B5/S45` is independently checked as a derived canonical spelling of `(4,5,5)`, not transcribed as Book wording. Printed-page offsets and the Notes reverse join are guarded.

Result: the asset audit supports only its declared mechanics and observer relations. Proximity, pixels, and missing stochastic state do not become transition semantics.

## Semantic and Representation Audit

- The literal `Native3D` evaluator works in raw Book array coordinates and does not call the generic rule/program path. The generic route uses opaque snapshot-scoped site selection, declared access, a closed typed RULE, same-site writes, and atomic old-snapshot commit. Neither evaluator dispatches on a catalog family.
- Direct shell access contains six or 26 surrounding occurrences and no Self. Product and positional access contain exactly one Self plus the declared shell. Small-quotient aliases preserve occurrence multiplicity rather than deduplicating resolved coordinates.
- The 5,139 native/generic commutations reconcile exactly as `4,096 face quotient + 14 face-product fibers + 7 face-shell cases + 896 full quotient + 54 full-product fibers + 27 full-shell cases + 34 directional + 9 named + 2 ternary`.
- All `2^14 = 16,384` binary face-product tables are expanded over all 128 seven-position contexts, checking 2,097,152 rows. All 128 face-shell output tables factor through the equal-Self image, and a one-Self-row violation is rejected.
- The full profile proves 56 product and 29 shell zero/full/unit bases, all 54 product fibers, and all 27 shell cases. Nonaliasing fixtures explicitly fire all `14 + 7 + 54 + 27 = 102` compact indices with center output one and whole-state native/generic equality.
- Fiber arithmetic is exact: each `(Self,n)` full fiber contains `binomial(26,n)` positional contexts; combining both Self values gives `2*binomial(26,n)`, and the 27 combined sizes sum to `2^27`.
- The general positional domains remain honest. The face profile has 128 input rows and `2^128` binary rules. The full profile has `2^27 = 134,217,728` input rows and `2^(2^27)` binary rules. Exact mixed-radix address/decode witnesses and all 27 projections establish the domain without claiming to enumerate every context or table.
- The explicit `(layer,row,column) -> (x=column,y=-row,z=layer)` representation has a certified inverse and carries offsets, contexts, and tables. Position, context, table-basis, and digit-basis checks commute. The asymmetric `(-1,0,0)` Book projection yields native/certified/naive outputs `1/1/0`, proving that naive re-sorting is not a valid adapter. `Cuboid[-Reverse[position]]` remains display-only.
- All nine named structural profiles commute on mixed-label successors. Majority and the three Carter Bays rules have explicit synthetic central triggers because the source does not serialize their exact 3D seeds. Both ternary profiles include same-Self, different-shell-sum, different-output witnesses and produce all three labels.
- Old-snapshot versus in-place scanning, fixed versus periodic boundaries, native `Z^3` versus finite work and views, evolving sparse background, stale/foreign handles, malformed reads/writes, exact selected-site/write coverage, and one shared T21/T22/T23 step function are adversarially checked.
- Two explicit collisions prove that the current Dyadaxes majority/threshold summary loses distinctions required by exact face/full predicates. Its raw rank-three geometry is reusable; its RULE is not a general T23 representation.

Result: T23 varies dimension, cubic topology, access data, and closed RULE representations. The evidence supplies no new UPDATE algebra, successor form, or executor.

## Architecture and Runtime Integration

- D129 follows the governing SimpleProgram interpretation: DOMAIN is discrete `t+3D`; CONFIGURATION owns fixed cubic `Z^3` topology and its invariants; ALPHABET is the finite label/value schema; FRONTIER is `AllSites`; NEIGHBORHOOD is typed shell or Self-plus-shell access; RULE is closed shell/product/positional data; UPDATE is the inherited same-site snapshot-parallel commit.
- Finite boxes, periodic quotients, fixed exteriors, and causal work volumes are realizations. An exact evolving background-plus-deviations carrier and a coordinate frame are lossless representations. Crops, projections, rasters, depth shading, and moving-structure displays are views or relations.
- The audit classification is entirely categories 1–3: direct reuse, parameterization/restriction/preset, and lossless representation. No category-4 execution algebra is introduced and no completed stage reopens.
- `src/ca/loci.py` already admits rank-three coordinates; neighborhood constructors already provide six-face and twenty-six-shell geometry; the current spatial kernel is mechanically rank-generic. Existing family dispatch, schema-poor lookup, fixed-width `numpy.int64` identity, and the lossy Dyadaxes preset are shared Goal 2 implementation gaps, not evidence for a 3D branch.
- Current scalar alphabets cover strict T23. Product/tagged alphabets remain a broader shared-library requirement established elsewhere; they are not falsely claimed to exist in the current runtime.
- Large positional rules require an immutable complete carrier such as an arbitrary-precision integer, packed vector, or validated finite-domain default-plus-overrides value with exact bounds, outputs, lookup, and serialization. An unrestricted callback is not accepted as program identity.
- The stage, D129 ledger entry, architecture matrix/disposition, `0-plan.md`, and `evidence-index.md` agree on the 151-source/138-retained/42-asset/5,139-commutation result, categories 1–3, and no-reopen conclusion.
- No `ThreeDimensionalState`, control payload, new UPDATE, executor, rollout branch, hidden Self/boundary, Dyadaxes substitution, Life/majority engine, callback, or raster-defined rule is proposed.

Result: D129 is active and implementation-ready as a parameterization/representation decision over T01/T02/T03/T08/T21/T22 and the shared branch-free runner.

## Verification Gates

- Source, asset, and semantic oracles pass from the repository root.
- All three oracles pass from a relocated `/tmp` tree linked only to the frozen `ref` corpus.
- All three optimized-mode executions fail closed before stripped assertions could create false passes.
- Silent imports and byte compilation to `/tmp` pass.
- Markdown fence parity and `git diff --check` pass.
- Changed paths remain inside `goal-1/`; no runtime, test, or root-document implementation was made for T23.
- `uv run pytest -q` passes: `102 passed`.

Verdict: **CLEAN**
