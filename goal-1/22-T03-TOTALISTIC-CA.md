# 22-T03-TOTALISTIC-CA

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T03, CSV line 4, `Totalistic Cellular Automata`; taxonomy vocabulary is `ref/notes/CA-Types.md:68-99` and remains a search seed rather than book evidence.
- The strict transition at `BOOK:772-776` distinguishes unrestricted three-color tables from totalistic rules. It assigns the colors exact values `0,1,2`, makes the next value depend only on the average of left/self/right, and orders the seven output cases from sum `0` at the least-significant/rightmost base-3 digit through sum `6` at the most-significant/leftmost digit.
- The Notes give the direct generalization. For `k` colors and radius `r`, fixed arity is `q=2r+1`, reachable sums are `0..q(k-1)`, table length is `M=1+q(k-1)`, and the rule count is `R=k^M` (`BOOK:11897,11902-11916`). The structural output for sum `s` is digit `floor(n/k^s) mod k`; average `s/q` is an exact alternate label for the same case, not a floating computation.
- T01/T02 and D111-D114 already supply fixed ordered one-dimensional support, `AllSites`, old-snapshot reads, typed same-site assignment, atomic parallel commit, successor, seed, realization, trace/view separation, ordered alphabets, and arbitrary-precision integer serialization. T03 changes the rule's input quotient and program identity, not the executor or update law.
- `simple_programs.md:1964-2027` groups numeric sums, active counts, and color histograms under one broad `TOTALISTIC` label. That API responsibility is wider than source T03: equal-sum contexts such as `(0,2,0)` and `(1,0,1)` must merge even though their color histograms differ.
- The current runtime can sum an `int64` read vector, but `rules.totalistic` does not derive its case count, `_channel_state` ignores the declared `sum` versus `count` mode, generic `lookup` is not executable, spatial output remains binary right-shift/`&1`, and batch rule IDs are forced through `numpy.int64`. No current test executes a standalone three-color totalistic table or validates its codec.
- Controlled search, source-repair, and asset closure are concurrent evidence dependencies. The architecture below uses only the strict definition and intact Notes formulas; exact gallery initial conditions, raster settings, and any additional variant claims remain unresolved until their protected sections close.

## Updated Assumptions

- Treat source T03 as one closed equal-weight integer-sum aggregate followed by a complete finite sum-case table. “Permutation invariant” alone is insufficient: a color histogram, set, nonzero count, minimum, or arbitrary reducer preserves different information.
- Make a numeric color valuation `nu:A->{0,...,k-1}` explicit and program-defining. The v1 source profile uses the canonical contiguous valuation; symbolic relabeling is supported only through an explicit validated bijection, never host iteration order, alphabet rank by accident, or palette tone.
- Normalize execution to integer sum `s`. Average is the exact rational label `s/(2r+1)` and cannot introduce float division, rounding, tolerance, or a second case table.
- Keep the complete structural `(valuation,aggregate,table)` rule primary. A padded arbitrary-precision base-`k` integer is a lossless source codec/provenance value, not the only in-memory rule form or an execution register.
- Strict T03 and T04 pin `r=1`; direct Notes evidence supports the same aggregate-table construction for validated `r>=1`. T04 (`k=3`) and T05 (higher `k`) remain discoverable parameter presets unless their own evidence introduces different mechanics.
- Do not import the single-gray seed, white-background filter, symmetric appearance, palette, gallery horizon, behavior class, or emulation into program identity. In particular, a zero background is stable only when the sum-zero output is zero.
- T06 quiescence, T07 reflection symmetry, additive formulas/proofs, outer/semi-totalistic summaries, histograms, unequal weights, threshold rules, higher-dimensional stencils, and T44 continuous aggregation retain separate predicates, analyzers, relations, or construction ownership. Any broader reuse remains unresolved pending its own evidence.

## Big Picture Objective

Reconstruct totalistic cellular automata exhaustively from strict text, captions, Notes, actual Index, implementations, formulas, galleries, restrictions, applications, and cross-references; determine the exact aggregate/table/code semantics and the smallest honest reuse of T01/T02 without a `totalistic` rollout branch.

## Catalog Identity

- Stable ID: T03.
- Exact CSV name: `Totalistic Cellular Automata` at `ref/notes/CA-Types.csv:4`.
- Taxonomy: `ref/notes/CA-Types.md:68-99`; vocabulary seed only.
- Candidate entry kind: permutation-invariant local-rule construction/description over fixed-lattice synchronous assignment, subject to evidence audit.
- Initial vocabulary: totalistic/totalistic rule, sum, average, total/aggregate of neighboring colors, code, base-`k`, `3k-2`, `k^(1+(k-1)(2r+1))`, `2187`, `16`, `64`, `5^13`, three/five colors, range `r`, outer totalistic, weighted totalistic, symmetric, additive, quiescent, and named example codes `777`, `867`, `420`, `1599`, `1815`.

## Search Log

In progress. The controlled search must separately cover strict definition/captions, general count and implementation Notes, actual-Index routes, split duplicates, aliases (`sum`, `average`, `outer totalistic`, weighted forms), color/range variants, code examples, symmetry/background restrictions, applications/emulations, and all linked assets. Every candidate will receive a disjoint included/sibling/relation/false-positive disposition.

## Book Excerpts

In progress. No excerpt will be treated as canonical until its complete candidate family and source repairs are closed.

## Construction Model

### Native semantics

| Dimension | Reconstructed T03 semantics |
|---|---|
| State | `STATE = SUPPORT + VALUES`; no control, accumulator, code register, or history. Support is the same fixed ordered one-dimensional regular lattice as T01/T02, and values form a total field over a finite color alphabet `A`. |
| Alphabet/value assignment | `k=card(A)>=2`. A total bijection `nu:A->{0,...,k-1}` supplies arithmetic color values and is part of program identity; the canonical source alphabet is the integer range itself. Palette is representation. |
| Active loci | Every semantic site on every event. Finite cycle/segment/causal-window lowering retains the T01/T02 distinction between native support, realization, work extent, and observation crop. |
| Read | For radius `r>=1`, read the fixed old-snapshot neighborhood at offsets `-r,...,0,...,+r`, including self exactly once. Its arity/multiplicity `q=2r+1` is defining even though aggregate output is permutation invariant. Strict T03 has `r=1`. |
| Aggregate/cases | `s=sum_i nu(read_i)`. Every integer `s` in `0..q(k-1)` is reachable, giving exactly `M=1+q(k-1)` cases. The exact average label is `s/q`; it does not change case identity. |
| Rule | One immutable complete structural table `U:{0,...,M-1}->A`. Equal sums must select the same row regardless of order or histogram. No missing row, default, wildcard, callback, gate, modulus, threshold, or formula is implicit. |
| Result/update | One typed same-site `Assign(U(s))` per active site; T01's atomic parallel fixed-field commit applies all assignments from the same old field. T03 adds no update law. |
| Successor/halting | One deterministic successor for every valid field/table, including unchanged fields. There is no branch, rejection, randomness, intrinsic halt, fixed-point stop, or background stop; finite horizon and resource outcomes are external. |
| Seed/background/boundary | The initial total field and finite realization are independent run data. A single gray cell, random field, or uniform background does not identify the rule. A canonical zero background evolves whenever `U(0)!=nu^-1(0)`; T06 owns the stable-background restriction. |
| Observers/provenance | Spacetime/raster views, exact-average labels, palette, symmetry and additivity claims, behavior class, period/growth/death analysis, gallery filters, emulation, search work, and code display remain outside state and native events. |

### Sum-table and Wolfram code invariants

Let `q=2r+1`, `M=1+(k-1)q`, and let `U_s` be the output color for integer sum `s`.

```text
output(n,s) = nu^-1(floor(n/k^s) mod k)
code(U)     = sum_{s=0}^{M-1} nu(U_s) * k^s
```

- Valid codes are exactly `0..k^M-1`; the rule space has `R=k^M` members.
- Sum zero is the least-significant/rightmost displayed digit. A padded source display is ordered `U_(M-1),...,U_1,U_0`, so leading zero digits are required table rows.
- Strict `k=3,r=1` has `q=3`, `M=7`, and `R=3^7=2187`. `k=2,r=1` has 16 rules; `k=2,r=2` has 64; `k=5,r=1` has `5^13=1,220,703,125`.
- General `k,r` requires arbitrary precision even though the strict codes are small: `k=8,r=1` already has `R=8^22=2^66`. Program/batch records therefore use stable structural references or tagged decimal strings rather than `int64`, float, or JSON numbers.
- The source code/table is losslessly expandable to an exhaustive table by `T(a_-r,...,a_r)=U(sum_i nu(a_i))`, but that expansion is an explicit verified relation. It cannot replace the aggregate, valuation, and sum-table identity.

### Variant disposition

| Profile | Semantic relation |
|---|---|
| `k=2,r=1` | Sixteen-rule totalistic restriction of T01; same T03 aggregate/table evaluator and shared assignment executor. |
| `k=3,r=1` | Strict profile and T04 preset; seven rows and 2,187 codes. |
| Higher `k`, radius one | T05 parameterization; `M=3k-2`, with no new execution mechanics. |
| General finite `r>=1` | Direct Notes parameterization with `q=2r+1`; changes read geometry and table cardinality under strict validation, not commit semantics. |
| Exhaustive T01/T02 table | Explicit aggregate-expansion relation; many ordered contexts share one T03 row, so the exhaustive table is not native T03 identity. |
| Stable zero background | T06 predicate `U(0)=nu^-1(0)`, equivalently `code mod k=0` in the canonical codec; never a base validator or seed assumption. |
| Left-right/reflection symmetry | Implied property of equal-weight sum for the symmetric radius stencil; T07 owns general classification/transforms, not a T03 flag. |
| Code 420/additive profiles | A table may additionally satisfy an algebraic formula such as `U(s)=nu^-1((-s) mod 3)`; additivity is a property/proof or alternate description, not hidden formula execution. |
| Color histogram/nonzero count | Different quotient: `(0,2,0)` and `(1,0,1)` have equal sum but different histograms. Neither can substitute for source T03 when `k>2`. |
| Outer/semi-totalistic | Retains center or another designated value separately and therefore has a product case domain and different codec. |
| Unequal/negative weights or thresholding | Different aggregate/image and often different symmetry; source weighted examples and generic weighted built-in forms are siblings, not T03 parameters. |
| Higher-dimensional or continuous aggregates | Different geometry or value/rule codomain; T44's continuous aggregate-map feedback remains a separate construction. |

## Current API Fit

| Construction element | Fit | Evidence and consequence |
|---|---|---|
| Numeric `A={0,...,K-1}` alphabet | DIRECT data shape | The schema explicitly includes finite `K`-color integer alphabets (`simple_programs.md:200-230`). T03 additionally couples one exact numeric valuation to aggregate and codec identity. |
| Symbolic or arbitrary numeric colors | PRINCIPLED EXTENSION | The generic alphabet admits symbols, but T03 needs a validated bijection to canonical integer values. An alphabet order or palette alone cannot supply arithmetic meaning. |
| Fixed 1D state/support and all-site transition | DIRECT with T01 qualification | Current field/snapshot/parallel-next-slice semantics fit (`simple_programs.md:87-113,1767-1793,2156-2199`); finite `SHAPE` remains a realization, not native `Z`. |
| Fixed radius neighborhood | DIRECT/PARAMETERIZATION | Static compact relative selectors can express `[-r,...,+r]` (`simple_programs.md:360-450,620-650`). Center inclusion, multiplicity, current-time read, and arity must be pinned. |
| `TOTALISTIC` aggregate-plus-table responsibility | PARAMETERIZATION / PRINCIPLED EXTENSION | The schema has the right two-stage shape (`simple_programs.md:1964-1997`), but does not define the source numeric valuation, exact sum image, row order, completeness, or code. |
| Numeric sum versus exact average | PRINCIPLED EXTENSION | Numeric sum is listed, but the API needs one closed equal-weight sum descriptor and exact `s/q` labeling. A generic reducer/callback or floating mean is not source semantics. |
| K-color histogram example | SEMANTIC MISMATCH for T03 | The documented histogram (`simple_programs.md:2010-2027`) preserves distinctions the strict totalistic sum erases; it is a separate permutation-invariant rule quotient. |
| Complete sum table/cardinality | PRINCIPLED EXTENSION | Table arity must derive as `M=1+(k-1)(2r+1)` and validate every output in `A`; the current schema supplies no sum-case domain object. |
| Wolfram base-`k` sum codec | PRINCIPLED EXTENSION | Needs a total bidirectional arbitrary-precision codec with sum zero least significant and structural table identity primary. T02's bigint responsibility composes, but its ordered-context address does not. |
| Typed assignment and parallel commit | DIRECT T01 reuse | Aggregate lookup still returns one same-site value, so `Assign` plus atomic fixed-field update applies unchanged and no eleventh law is needed. |
| Seed, boundary, trace, and views | PARAMETERIZATION / NOT APPLICABLE to program | Existing finite seed/boundary/trace forms can realize runs, while background filtering, average labels, palette, raster, class, and horizons remain downstream. |
| Outer, weighted, histogram, additive, quiescent, symmetric profiles | NOT APPLICABLE to base T03 | These require separate summary types, properties, analyzers, or presets and cannot become permissive flags on the source aggregate. |

## Current Runtime Fit

| Component | Fit | Exact finding |
|---|---|---|
| `alphabets.int_range_alphabet(k,0)` | DIRECT primitive, incomplete wiring | Supplies the canonical values `0..k-1` (`src/ca/alphabets.py:59-86`), but `Dynamics` carries no alphabet or valuation and spatial rollout never validates membership. |
| `alphabets.symbolic(values)` | PRINCIPLED EXTENSION for T03 | Preserves deterministic values (`alphabets.py:145-179`) but supplies no numeric valuation; rollout coerces all spatial states to `int64`, so symbolic T03 cannot execute honestly. |
| `neighborhoods.eca(radius=r)` / selectors | DIRECT finite geometry | Produces a static current-time 1D radius stencil (`neighborhoods.py:551-569`). Strict presets must pin center inclusion and arity; native support/causal lowering remain absent. |
| `rules.totalistic(component,aggregate)` | PARAMETERIZATION / SEMANTIC MISMATCH as a T03 spec | Records `sum` or `count` but no alphabet, valuation, arity, reachable image, `state_count`, table, or code (`rules.py:198-216`). Consequently `lookup` cannot derive T03 `M`/`R`. |
| `rules.lookup` / `validate` | DIRECT counting helper, incomplete rule model | `validate(a,*S_i)` correctly computes `a^product(S_i)` from already-known channel sizes (`rules.py:128-166`), but lookup has only `lsb_rule_bits`, no structural aggregate table/base-`k` output, and no totalistic channel range (`rules.py:262-295`). |
| `_channel_state` totalistic step | DIRECT integer-sum kernel only | It sums all read integers (`rollout.py:742-777`), which matches canonical T03 locally, but ignores the declared aggregate mode, forces `int64`, and validates neither values nor fixed arity. Thus current `count` is merely sum outside binary alphabets. |
| `_lookup_index` | PARAMETERIZATION for one sum channel | One channel happens to pass sum through unchanged, but the helper bit-shifts multiple channels as binary positions (`rollout.py:811-822`) rather than using typed case domains or mixed radices. |
| Spatial rule output | SEMANTIC MISMATCH | Scalar and batch spatial paths always decode `(rule_id >> index) & 1` (`rollout.py:650-682`); they cannot return color `2`, use base `k`, or execute a structural sum table. |
| Generic rule/spec routing | SEMANTIC MISMATCH | Rollout/apply-rule whitelist named Phase 1 families and reject ordinary `lookup` (`rollout.py:145-212,292-331`); `specs.rule_from_spec` exposes only six named families (`specs.py:117-145`). Adding `totalistic` to these switches would repeat the architecture failure. |
| Rule IDs and raw batches | PARAMETERIZATION only for small profiles | Scalar Python `int` is unbounded, but batch normalization and `RawBatch.rule_ids` use `numpy.int64` (`rollout.py:264-288`, `specs.py:70-81`). General `k,r` needs structural program references and tagged decimal-string codes. |
| `Dynamics`, seeds, boundary, trace | PARAMETERIZATION / PRINCIPLED EXTENSION | Finite field mechanics are reusable, but alphabet/valuation, semantic support, typed rule/result/update, program identity, and observation scope are missing (`specs.py:23-81`). |
| Dyadrads/Dyadaxes/Lagcounts | NOT T03 conformance | These binary families use counts followed by gates or sampled/composed lookup (`rules.py:369-518`). They demonstrate a reusable reduction kernel only; their component products, gates, and 256-code spaces are not source T03. |

### Test fit

- `tests/test_rules.py:9-45` checks only declared counts for named binary families; it never constructs a pure totalistic channel plus complete output table or checks `M=3k-2`.
- `tests/test_rollout.py:263-435` covers rule-zero extinction and scalar/batch parity for gated binary spatial families. Binary output and shared-code parity cannot detect a base-3 decoder, sum-row order, histogram substitution, or evolving zero background.
- No test distinguishes equal-sum/different-histogram contexts, produces output color `2`, exercises `k=3,r=1` code 777/867/420, checks `k=2,r=2` code 10, round-trips a code above signed 64-bit, or proves old-snapshot totalistic assignment.
- There is no test that T04/T05 presets resolve to the same structural rule/executor, that T06 is exactly the sum-zero-row predicate, or that T07 symmetry is derived rather than a runtime flag.

## Principles Audit

| Principle | T03 result |
|---|---|
| 0–2 | Evidence requires one new closed rule-input quotient, not a new executor. T01/T02 support, reads, assignment, commit, successor, realization, and trace semantics remain valid; a `totalistic` rollout branch would duplicate them. |
| 3–4 | Neighborhood gathers the fixed old stencil; the rule's closed aggregate maps it to one sum row and returns typed `Assign`; update commits all assignments atomically. The aggregate is not hidden in frontier/update. |
| 5 | State contains only fixed support and the current color field. Sum, average, table code, search state, background filter, and behavior class are program/derived/observer data, not hidden state. |
| 6–8, 12 | A finite `[t,x,0,0]` trace may represent a realization, but topology, numeric color valuation, code digits, palette tones, crop, and batch storage retain distinct identities. |
| 9 | `k`, valuation, fixed arity `q`, reachable sum image, `M`, complete table, and codec are genuinely coupled and must validate together. Palette, seed, boundary, horizon, and execution backend remain independent. |
| 10 | T03/T04/T05 presets may validate generic, three-color, and higher-color profiles only by returning the same ordinary aggregate-table rule and shared fixed-lattice spec. |
| 11 | Equal-weight exact sum and complete sum lookup are defining. Integer vectorization, exact-average labels, exhaustive expansion, table gather, bigint representation, and batching are incidental or explicit relations. |
| 13–15 | Canonical tests must use equal-sum/different-histogram contexts, nonbinary outputs, code-order fixtures, non-quiescent backgrounds, larger `r`, old-snapshot adversaries, and independent source codes. Pixels or scalar/batch parity alone are insufficient. |
| 16 | One typed valuation/aggregate/case-table/codec boundary is architecture. A callback reducer, histogram substitution, exhaustive-table-only storage, family switch, reversed digits, or binary fallback is a shim. |

D112's structural-table-first and arbitrary-precision policy composes at the finite-table/serialization responsibility level; T03 has a distinct sum-case domain and codec from T02's ordered context table. D114 is resolved concretely: T03 numeric valuation and aggregate are program semantics, ordered color identity supplies lossless values/code digits, and palette remains a view.

Evidence still unresolved for this architecture pass: exact gallery trajectories/raster parameters; whether any source profile requires noncanonical or non-bijective numeric color values; and whether radius zero, dynamic/masked arity, histogram, outer-totalistic, weighted, or higher-dimensional rules should share a later generalized aggregate interface. Goal 2 must expose these as typed unsupported or separate constructions until their own evidence closes, not infer defaults.

## Detailed Implementation Plan

1. Build and execute a complete literal/regex manifest across the canonical monolith; disposition every candidate and follow all relevant references.
2. Record every unique construction-relevant passage verbatim with exact provenance and explicit source repairs.
3. Inventory all direct, sibling, relation-only, duplicate, and excluded assets; add only source-permitted semantic/raster oracles.
4. Derive aggregate case space, ordering, code, rule counts, state/update/successor, boundary/seed, variants, and observer separation before evaluating reuse.
5. Audit current API/runtime/tests and completed T01/T02/D111-D114 decisions for direct reuse, parameterization, extension, or mismatch.
6. Write an implementation-ready Goal 2 stage, no-cheating gates, independent review, and global ledger integration.

## Goal 2 Implementation Stage

### G2-T03 — Exact finite-sum rule descriptions over the shared fixed-lattice executor

**Objective:** add one inspectable equal-weight integer-sum aggregate and complete sum-case table so generic T03, T04 `k=3`, T05 higher-color, and direct range-`r` profiles execute through the T01/T02 fixed-lattice `Assign`/atomic-update protocol. A preset is discoverable, but neither rollout nor rule application dispatches on `totalistic`.

**Dependencies:** synthesis-selected G2-T01 fixed regular support, `AllSites`, typed same-site assignment, atomic parallel update, finite realization/causal-window lowering, and event/snapshot trace semantics; G2-T02 ordered finite alphabets, structural finite-table identity, stable program references, and arbitrary-precision decimal-string codecs; T34's lossless exact nonnegative-integer serialization responsibility. T03 adds no update law.

**Concrete files and changes:**

1. Extend `src/ca/alphabets.py` with an immutable validated numeric color valuation. The canonical constructor maps the declared colors bijectively to `0..k-1`; any symbolic relabeling stores the explicit forward/inverse map. Do not derive it from palette, a host set, or incidental array order.
2. Add `src/ca/aggregates.py` with a closed `EqualWeightIntegerSum` descriptor/evaluator carrying valuation identity, fixed arity `q`, and exact image `0..q(k-1)`. It accepts no callback, float mean, dynamic mask, histogram, gate, or arbitrary weights. The exact average is a separate label/query `s/q`.
3. Extend the synthesis-selected `src/ca/rule_tables.py` with a typed aggregate-case domain and immutable complete table `U[0..M-1]`. Reuse a generic finite-table carrier only if exhaustive-context and aggregate-sum domain tags cannot be confused. Validate `M=1+(k-1)q`, every output, leading zeros, stable identity, and lossless structural serialization.
4. Add a versioned `WolframTotalisticCodec(k,q,valuation)` alongside—not inside—the table. Decode/encode with sum zero least significant, validate `0<=n<k^M`, and serialize arbitrary-precision codes as tagged decimal strings. Reuse bigint primitives, not T02's context-index formula.
5. Refine `src/ca/rules.py` so a structural `AggregateLookupRule(aggregate,table)` derives `M/R`, evaluates sum then table, and returns an ordinary typed assignment value. Replace the current loose `totalistic` channel contract or constrain it behind this typed form; retain binary active-count/gate constructs only under their honest names.
6. Replace family-whitelisted spatial routing in `src/ca/rollout.py` (or the synthesis-selected executor) with the shared rule/result/update protocol. Scalar and batch paths gather one old snapshot, invoke the closed rule object, emit same-site assignments, and commit together. They never decode T03 with `right_shift`/`&1`, expand it invisibly to an exhaustive table, or add a T03 branch.
7. Extend `src/ca/specs.py` with alphabet/valuation, semantic support, typed rule/result/update, realization, and stable program-reference fields. Add `src/ca/presets/totalistic.py`: `totalistic(k,code_or_table,r=1)`, `three_color_totalistic(...)`, and `higher_color_totalistic(...)` validate their scopes and return the same generic spec. Seed, boundary, horizon, palette, and gallery filter remain run/view inputs.
8. Update `RawEpisode`/`RawBatch` and `src/ca/viz/export.py` to reference structural programs and optional tagged code strings rather than requiring numeric `int64` rule IDs. Preserve finite `[t,x,0,0]` traces and keep exact-average labels/palettes downstream.
9. Add `tests/test_aggregates.py`, extend `tests/test_rule_tables.py`, and add `tests/test_t03_totalistic_ca.py` plus shared executor/spec/codec tests. Preserve all T01/T02 conformance and current named-family behavior until those families receive their own honest migrations.

**Migration and removal:**

- Do not reinterpret the documented K-color histogram as T03. Give histogram, nonzero count, and binary active count distinct closed summary identities.
- Remove the assumption that every summarized channel is binary or that spatial output is one rule-ID bit. A one-channel sum may index directly, but all case domains and table outputs remain typed.
- Generic `lookup`/aggregate rules must no longer be rejected by family switches. Do not add an interim `lookup` or `totalistic` switch as a compatibility path.
- Preserve Dyadrads/Dyadaxes/Lagcounts semantics as separate composed/gated profiles; do not rename them T03 or use their 256 sampled rules as totalistic evidence.
- Keep an explicit aggregate-to-exhaustive expansion utility only as a verified relation/analyzer. Structural T03 records must reconstruct valuation, aggregate, and sum table without an exponential ordered table.

**Required conformance tests:**

1. For validated `k>=2,r>=1`, derive `q=2r+1`, `M=1+(k-1)q`, and `R=k^M`; pin `R(2,1)=16`, `R(3,1)=2187`, `R(2,2)=64`, and `R(5,1)=1,220,703,125`. Reject booleans, invalid `k/r`, malformed valuations, wrong table lengths, out-of-alphabet outputs, `-1`, and `R`.
2. Prove every sum `0..q(k-1)` reachable for representative `k/r`, and that every permutation of one read multiset gives the same sum/output. Fixed arity, center inclusion, and repeated positions remain inspectable.
3. Use `(0,2,0)` and `(1,0,1)` at `k=3`: both must address sum row `2` despite different histograms. A histogram-keyed implementation must fail this oracle.
4. Round-trip structural tables/codes `0`, `1`, `420`, `777`, `867`, `R-1`, deterministic sampled `k/r` profiles, and a valid `k=8,r=1` code above `2^63-1` through table, tagged decimal string, and JSON-safe records without NumPy/float loss.
5. Pin code 777's least-significant-first outputs as `(0,1,2,1,0,0,1)`. Assert `output(n,s)=floor(n/3^s) mod 3`, source display order is the reverse padded sequence, and color `2` survives execution.
6. Prove code 420 has `U(s)=(-s) mod 3` for `s=0..6`, while remaining a normal structural table plus an additive property claim. No modulo formula may replace arbitrary T03 execution.
7. For `k=2,r=2`, prove code 10 outputs one exactly for sums `1` and `3`. This catches a hard-coded radius-one/seven-row codec.
8. Expand representative aggregate tables to T01/T02 exhaustive tables and compare all local contexts and several exact trajectories. The native T03 record must still serialize as valuation + aggregate + `M` rows, not the expansion.
9. Run code 1 from an all-zero field and prove the entire background evolves; then validate T06 separately as `U(0)=0`, equivalently `code mod k=0`. No seed or finite-support shortcut may assume quiescence.
10. Use binary radius-one code 2 on `[1,0,0]` with explicit fixed exterior: parallel old-snapshot update yields `[1,1,0]`, while left-to-right in-place mutation would yield `[1,1,1]`.
11. Run one structural program with centered, explicit, random, periodic, finite-block-on-constant, and finite-block-on-repeating initial fields and with cycle/segment/causal-window realizations. Program identity stays fixed; run/realization/view identities change.
12. Assert T04 and T05 presets return the same aggregate-rule/spec types as generic T03; T07 reflection is derived from equal-weight sum; outer, histogram, weighted, threshold, dynamic-arity, and continuous profiles are rejected or routed to their own typed constructions.
13. Inspect the resolved spec/executor: no callback, family branch, partial-row fallback, hidden valuation/seed/background/palette, exhaustive-only identity, binary decoder, float mean, fixed-width rule code, or artificial maximum `k/r`.
14. Preserve the full repository suite, T01/T02 asymmetric/nonbinary tests, scalar/batch parity as regression evidence, and finite trace/export round trips without weakening expectations.

**Completion evidence:** all structural/count/codec and independent trajectory oracles pass; equal-sum/different-histogram behavior is pinned; general big codes round-trip losslessly; non-quiescent backgrounds and nonbinary outputs execute; T04/T05 inspect as presets of one ordinary rule/spec; static inspection finds no totalistic/lookup branch, callback, histogram substitution, exhaustive masquerade, binary fallback, or hidden default; existing tests pass unchanged.

## No-Cheating Checks

- No `totalistic`/T03/lookup family branch, second fixed-lattice executor, or new update law.
- No callback reducer, evaluator string, host `sum` object, formula escape hatch, or opaque aggregate metadata.
- No K-color histogram, multiset, set, nonzero count, min/max, gate, or ordered exhaustive table substituted for source numeric-sum identity; `(0,2,0)` and `(1,0,1)` must merge.
- No aggregate-to-exhaustive expansion as the only stored program or as proof that T03 has ordered-context identity.
- No palette, host ordering, incidental rank, or display tone inferred as arithmetic magnitude; valuation is explicit, total, bijective, and versioned.
- No floating average, tolerance, rounding, normalized-by-variable-count mean, dynamic/masked arity, omitted center, or duplicate-offset collapse.
- No reversed sum-digit order: sum zero is least significant/rightmost, leading zeros are complete rows, and codes are range checked.
- No partial sum table, implicit output/center/background default, wildcard, sparse mutation display, raster-decoded rule, or fixed gallery filter.
- No binary `right_shift`/`&1`, float, JSON number, `numpy.int64`, or artificial `k/r` cap used for general program identity or output.
- No hidden seed, boundary, horizon, palette, background-freezing, behavior class, search work, RNG, or accumulator in state/execution.
- No T06 quiescence or T07 symmetry flag fused into validation; no additive formula, outer/semi-totalistic center channel, unequal weight, threshold, higher-dimensional, or T44 continuous rule smuggled behind an aggregate option.
- No proof from pixels, symmetric examples, rule zero, scalar/batch self-parity, or T01/T02 exhaustive expansion alone; independent sum/code/nonbinary/background/old-snapshot oracles are mandatory.
- No weakening current tests, retaining parallel semantic paths, or relabeling Dyadrads/Dyadaxes/Lagcounts as T03.

## Completion Requirements

- [ ] Every strict/Notes/split/actual-Index/alias/variant/application/emulation textual candidate is dispositioned reproducibly.
- [ ] Every relevant asset and source-permitted oracle is closed with hashes, geometry, repairs, and exclusions.
- [ ] Aggregate/value/case/table/code/read/update/successor/boundary/seed semantics and variants are explicit.
- [ ] T01/T02/T04/T05/T06/T07/additive/weighted/emulation boundaries and current API/runtime fit are proved.
- [ ] Goal 2 files/dependencies/tests and no-cheating gates are implementation-ready.
- [ ] Global ledgers, independent review, diff checks, and repository tests are integrated.

## Stage Results

In progress. Direct evidence currently supports aggregate-plus-table parameterization, but the general value/case/code semantics and complete variant boundary are not yet closed.

## Integration Results

In progress. No prior decision is changed until the complete evidence audit determines whether D114's aggregate responsibility is sufficient.
