# T22 Final Hostile Integration Review

Review target: `34-T22-MOORE-CA.md`, its source, asset, and semantic oracles, D128 in `design-ledger.md`, the D128/T22 rows in `architecture-audit.md`, and T22's plan/evidence-index integration.

Review posture: independent and adversarial. The review treats `src/ca` as the current namespace and Phase 1 realization of the broader SimpleProgram library, never as the semantic boundary of a cellular-automaton-only library.

## Findings

No material finding remains.

Three bounded defects were found and repaired during review:

1. **Medium — source closure omitted evidence used by the code-provenance conclusion.** The first draft cited `BOOK:11902-11912` to derive the fixed-width totalistic-code convention but did not include those lines in the frozen T22 retained set. The six nonblank governing lines are now native evidence. The repaired retained set is 270 lines, not 264, and every dependent count, digest, split join, asset-source guard, stage statement, ledger entry, architecture row, plan row, and evidence-index row was updated.
2. **Low — two architecture distinctions were correct but insufficiently executable.** WireWorld's label-predicate count and the existing Dyadaxes majority-gate loss were initially prose/Goal 2 obligations only. The semantic oracle now checks every one of WireWorld's `4^9 = 262,144` local contexts, one native/generic complete step, an equal-numeric-sum/different-predicate-count collision, and an explicit Dyadaxes collision whose Moore counts are 0 and 3 but whose required code-174826 outputs differ.
3. **Low — provenance wording misstated the high part of code 3702.** The text now says high quotient 3, equivalently two excess high bits, rather than “three high radix blocks.”

These repairs strengthen evidence and conformance only. They do not change D128's architecture classification.

## Source Closure

- The source oracle freezes the canonical Book, Atlas, catalog, taxonomy, and all 17 split-document hashes before interpreting evidence.
- Its 17-query union contains 164 unique lines: 117 pre-Index and 47 actual-Index.
- The pre-Index query partition is exact: 93 retained matches plus 24 classified exclusions, with no remainder. The exclusions are `12 generic 1D/code-update + 7 physical/aggregation-background + 5 other-construction` collisions.
- The six repaired totalistic-codec lines join 171 prior governed continuations, giving 177 governed continuations and 270 retained lines total.
- The retained semantic partition is exact: `96 native + 102 relation + 72 control = 270`.
- The retained-set digest is `edb307531cd8afc3bdd188dc675f211b1651ebf202f11dc56b0e467918dd7709` everywhere it is cited.
- The actual-Index routes remain navigation-only and partition as `9 T22 geometry/code + 28 Life + 5 T23 + 2 T24 + 3 numeric false collisions = 47`.
- The query reverse join closes at 162 split records (`151 exact + 11 mapped variants`). Retained evidence closes at `192 exact + 78 mapped variants`; no retained line is monolith-only.
- `BOOK:11902-11912` now explicitly guards the exact-sum evaluator and fixed-width `IntegerDigits` representation. Combined with the ten-case binary nine-position schema and right-edge lookup, it derives printed `3702` as canonical table code `630` while retaining `3702` as source provenance.
- General positional order, the 512/140/102/18/10/9 rule counts, named codes, old-snapshot update, finite realizations, Life mechanics, stochastic relations, and T21/T23/T24/constraint controls remain separately classified. Source facts are not silently promoted into architecture conclusions.

Result: the repaired source closure is zero-remainder, and its arithmetic, hashes, classifications, provenance adapter, and cross-file descriptions agree.

## Asset Closure

- The radius-four asset candidate universe contains 95 physical plates and partitions exactly as `68 governed + 27 adjacency-only`.
- The governed partition is `C18/C512/O/R/P-Life/S-stochastic/X21/X23/X24/X-constraint = 4/0/8/17/19/5/1/9/4/1`.
- The empty C512 raster class is explicit: the complete positional schema is text-grounded, but no governed raster can prove its positional order.
- Life's 19 plates remain a named-preset/relation subledger over the same T22 algebra. They are not a separate family or control construction.
- The five stochastic plates remain evolving relations with missing RNG/distribution/configuration replay data; they are not declared SimpleProgram nonfits. The pure `3x3` template constraint is the actual nonstep control.
- Every candidate has one monolith reference, one split reference, a physical JPEG hash, dimensions, and a governed role or adjacency reason. Thus 190 references reduce to 95 physical files and 95 unique hashes.
- The 28-record transcript ledger binds every declared code, seed, checkpoint, continuation label, and observation to both source-line and physical-asset hashes. Its digest is `981e0e0391310b9f3b86cd0f8863589bbf7423ddd1da87525da10d2ae704c4e3`.
- The claim boundary is honest: `HASH_BOUND=95`, `TRANSCRIBED=28`, and `PIXEL_REPLAYED=0`. Random/stochastic plates are not replayed without serialized inputs and probability machinery.
- Printed-page/file offsets and the unusual Notes/split-Index join are guarded explicitly.

Result: the asset closure supports the stated mechanics and boundaries without importing proximity candidates, raster semantics, or unreplayable randomness.

## Semantic and Representation Audit

- The generic route follows the governing four-axis event directly: all-sites selection, explicit old-snapshot reads, closed typed RULE evaluation, and atomic same-site commit. It contains no catalog/family switch.
- The native row/column evaluator is independent of the generic program/rule path. It reads literal Book positions and implements positional, outer-totalistic, equal-sum, finite-`k`, and WireWorld formulas separately.
- Strict access contains exactly one declared Self and eight unique Moore offsets. The center is neither hidden nor duplicated, and periodic aliases retain read-occurrence multiplicity.
- The distinct binary rule domains remain complete 512-context positional, 140-orbit C4-restricted, 102-orbit D4-restricted, 18-case `(SelfValue,MooreCount)`, ten-case all-nine sum, and nine-free-bit growth forms. Their rule counts are `2^512`, `2^140`, `2^102`, `2^18`, `2^10`, and `2^9`.
- Burnside fixed-point counts and explicit context partitions independently derive 140 C4 and 102 D4 orbits. Zero/full/unit bases close expansion and factorization at 142 and 104 cases, and one-row disagreements are rejected.
- All 262,144 outer signatures round-trip, all 1,024 equal-sum tables expand/factor, and 514 zero/full/unit general-code bases cover every positional table row.
- The 1,419 native/generic commutations reconcile as `320 outer + 192 equal-sum + 514 general + 225 directional + 5 named/source-spelled + 1 WireWorld + 81 ternary projection + 81 ternary FullTotal`.
- The finite-`k,d` formula `k*((3^d-1)*(k-1)+1)` is checked on seven profiles. The ternary 2D profile covers all `3^9 = 19,683` contexts and exactly 51 product cases.
- The Book basis change `(row,column) -> (x=column,y=-row)` yields `runtime_to_book=(6,3,0,7,4,1,8,5,2)` and its inverse. All 4,608 projection/context cases and 512 table-unit bases commute; an asymmetric counterexample proves that naive re-sorting without table permutation changes the program.
- Named predicates reconstruct codes `175850`, `746`, `174826`, and Life `224`; Life's blinker is reproduced through the same fixed-lattice route. Printed `3702` is represented by a provenance adapter whose ten low sum digits produce canonical code `630`; the strict ten-case codec rejects raw 3702 rather than silently normalizing it.
- WireWorld uses the closed predicate `neighbor_label == 1`, not numeric neighbor-value sum. All 262,144 local contexts and 36 `(Self,predicate_count)` fibers pass, and equal numeric sum 2 yields different outputs for two heads versus one label-2 neighbor.
- The current Dyadaxes geometry is lossless, but its RULE summary is not: Moore counts 0 and 3 can both map to `(self=0, cardinal_majority=false, diagonal_majority=false)`, while code 174826 requires outputs 0 and 1.
- Old-snapshot versus in-place traversal, fixed versus periodic boundary, exact `Z^2` versus finite work, evolving versus quiescent sparse background, stale/foreign handles, malformed writes, and T21/T22/T23 use of one generic step function are all adversarially checked.

Result: T22 changes access data and RULE representations/restrictions only; the semantic evidence supplies no new UPDATE algebra or executor.

## Architecture and Runtime Integration

- D128 follows the governing SimpleProgram interpretation. `src/ca` is a namespace/current realization, not the abstraction boundary; CA is the fixed-lattice/all-sites/local-read/same-site-write/snapshot-parallel preset.
- DOMAIN remains discrete `t+2D`. Square `Z^2` support/topology and its invariants belong to CONFIGURATION; finite shapes, quotients, exteriors, sparse lowerings, crops, and rasters remain realizations or views.
- The audit categories are exact: DOMAIN/configuration/FRONTIER/RULE-result/UPDATE/outcome are category 1 direct reuse; Moore access, presets, predicates, and restrictions are category 2; coordinate, compact-table, orbit-table, and code/provenance maps are category 3 lossless representations on their declared images. No category-4 execution algebra is introduced.
- Life `224` is the ordinary `B3/S23` value of the same 18-case schema. Stochastic eight-neighbor evolution remains a canonical evolving relation whose probability/RNG semantics belong to its owning stage. Only the pure template/model set lacks a canonical successor here.
- The runtime citations are accurate: `moore()` supplies the eight-cell shell, `self_at()`/`compose()` preserve Self as a role, and `dyadaxes_2d()` exposes the same raw geometry before `rules.dyadaxes_2d()` discards information through two strict-majority gates.
- The current spatial kernel is mechanically reusable but entered through family-name branches; general positional significance is reversed relative to Book order and batch rule IDs are narrowed to `numpy.int64`. The Goal 2 handoff correctly treats those as shared realization/codec defects rather than reasons for a Moore branch.
- The stage, D128 ledger entry, architecture matrix/disposition, `0-plan.md`, and `evidence-index.md` agree on the 270-source/95-asset/1,419-commutation result, categories 1–3, and no-reopen conclusion.
- No `MooreState`, `SingleControl`, `TransitionControl`, Moore/Life/symmetry executor, family dispatch, hidden center/boundary, Dyadaxes shortcut, or raster-defined rule is proposed.

Result: D128 is active and implementation-ready. It is a parameterization/restriction/representation decision over T01/T02/T03/T08/T21, not a new top-level construction.

## Verification Gates

- Source, asset, and semantic oracles pass from the repository root.
- All three oracles pass from a relocated `/tmp` tree linked only to the frozen `ref` corpus.
- All three optimized-mode executions fail closed before stripped assertions could create false passes.
- Silent imports and byte compilation to `/tmp` pass.
- Markdown fence parity and `git diff --check` pass.
- Changed paths remain inside `goal-1/`; no runtime, test, or root-document implementation was made for T22.
- `uv run pytest -q` passes: `102 passed`.

Verdict: **CLEAN**
