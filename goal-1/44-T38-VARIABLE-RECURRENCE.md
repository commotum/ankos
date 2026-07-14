# 44-T38-VARIABLE-RECURRENCE

Status: **COMPLETE — EVIDENCE, ASSETS, SEMANTICS, ARCHITECTURE, AND HOSTILE REVIEW CLOSED**

## Current Facts

- T38 is CSV physical line 39, `Variable-Index Recursive Sequences`; `ref/notes/CA-Types.md` section 38 supplies search vocabulary, not primary mechanics.
- The Book does not introduce a second printed heading for T38. The semantic boundary begins inside `Recursive Sequences` at `BOOK:1569`, where a term value determines which earlier index is read. T37's fixed-distance material ends at `BOOK:1567`.
- The native configuration remains T37's complete consecutive exact numeric prefix in discrete `t+1D`; term index is the spatial/indexed support coordinate and rollout event count remains `t`.
- The strict main evidence is `BOOK:1569-1617` plus `_page_144_Figure_3.jpeg` and `_page_145_Figure_1.jpeg`. Eight displayed rules use only integer constants, addition/subtraction, target index `n`, and nested reads of already-generated terms.
- The source explicitly warns that computed addresses may yield meaningless `f[0]`, `f[-1]`, or `f[-2]`, while stating that the eight displayed rules avoid this problem (`BOOK:1571-1575`). This is a runtime read-validity boundary, not evidence for wrap, clamp, padding, default values, or a catalog-specific halt.
- The Notes give the memoized definition for displayed case (e) and fix leftmost-innermost evaluation as the ordinary demand order (`BOOK:12720-12726`). An algebraic cancellation such as `f[-1]-f[-1]` does not license skipping those demanded reads under that evaluator.
- The Notes distinguish native recurrence from derived descriptions: exact formulae for case (d), binary-digit descriptions for cases (c)/(d), fluctuation statistics, address plots, and evaluation trees consume or analyze the sequence but do not select a different native UPDATE (`BOOK:12728-12767`).
- The Notes multiplicity list for case (d) at `BOOK:12738` omits the extra initial `1`; the main figure and the Notes' own largest-index formula at `BOOK:12742` independently contradict that extraction/source defect. Any repair must be explicit and guarded.
- The page-144 JPEG ends midway through its lower small-plot row: the eight formulas/seeds/term rows and panels (a)-(d) are present, but lower panels (e)-(h) are cropped. No missing curve samples or plot extents may be invented.
- The eight strict rules share T37's unique endpoint source and one-term persistent append. T38 changes the old-prefix access expression, not configuration topology, write shape, UPDATE, runner, or executor.
- The `invalid_index_policy` menu in the taxonomy note is not source authority. Primary-source conformance treats an actually demanded non-old-prefix reference as an undefined attempted step: the common no-commit error envelope retains the last complete prefix and commits no event.
- D138 is classes 1–3 only. T38 reuses T37's configuration, endpoint FRONTIER, endpoint write, trace semantics, and T16 splice; it adds a closed, program-coupled computed-address selector/read witness within the existing NEIGHBORHOOD/loci responsibility. No new execution algebra is established.

## Updated Assumptions

- **Retained:** strict origin is 1, values are arbitrary-precision positive integers, and every successful event appends exactly one positive integer at the next consecutive index.
- **Retained:** a term read is valid only when its fully evaluated exact integer address lies in the old prefix, `1 <= address < n`. The newborn `f[n]` is unavailable during its own event.
- **Retained:** computed-address syntax is closed structural data. `TermAt(TargetIndex - TermAt(TargetIndex - 1))` is inspectable and replayable; a callback, host expression, formula string, or hidden recursive interpreter is not.
- **Retained:** ordered leftmost-innermost demand and exact expression structure are preserved wherever partiality can distinguish algebraically equivalent formulae.
- **Retained:** the complete prefix is canonical state. A memo table is merely a direct implementation of that state; an evaluation tree, newest value, bounded suffix, or address cache is not a lossless replacement.
- **Retained:** successful endpoint append lowers through T37's `Val* · End(n)` encoding to T16 exactly-one ordered splice. Invalid demand returns before RULE write or UPDATE commit.
- **Rejected:** construction-specific T38 state, endpoint-update law, recursive executor, family branch, implicit memoization history, default `f[0]`, Python negative indexing, modulo/wrap/clamp, lazy cancellation that contradicts source evaluation order, and treating an observer formula as native random-access evolution.

## Big Picture Objective

Reconstruct T38 as a closed data-dependent old-prefix access profile over T37's existing growing indexed sequence event. Exhaustively close the eight main rules, source-transcribed seeds/rows, runtime address guards, leftmost-innermost demand, Notes formulae, memoization, observers, evaluation trees, assets, actual Index/splits/history, current-runtime fit, lossless T16 lowering, generic error behavior, and Goal 2 handoff. Add a new semantic component only where a concrete one-step counterexample defeats the smallest reusable construction.

## Catalog Identity

- Stable ID: T38.
- Exact CSV name: Variable-Index Recursive Sequences.
- CSV physical line: 39.
- Taxonomy section: 38.
- Canonical main core: `BOOK:1569-1617`.
- Native Notes core: `BOOK:12720-12726`.
- Observer/relation Notes: `BOOK:12728-12767`.
- Entry kind: deterministic exact one-term append whose closed access expression computes old-prefix addresses from old values.
- Strict DOMAIN: discrete `t+1D` with finite consecutive support growing by one at each successful event.

## Primary Strict Profiles to Verify

The page-144 plate supplies the following eight rules and term-row horizons. The asset oracle independently hash-binds and transcribes them, the semantic oracle regenerates every displayed term from a separate structural program, and the integration gate equates all eight formulas, seeds, horizons, and 340 visible values.

| Row | Closed recurrence | Fresh seed | Visible terms |
|---|---|---|---:|
| (a) | `f[n] = 1 + f[n - f[n-1]]` | `f[1]=1` | 48 |
| (b) | `f[n] = 2 + f[n - f[n-1]]` | `f[1]=f[2]=1` | 44 |
| (c) | `f[n] = f[f[n-1]] + f[n - f[n-1]]` | `f[1]=f[2]=1` | 40 |
| (d) | `f[n] = f[n - f[n-1]] + f[n - f[n-2] - 1]` | `f[1]=f[2]=1` | 40 |
| (e) | `f[n] = f[n - f[n-1]] + f[n - f[n-2]]` | `f[1]=f[2]=1` | 40 |
| (f) | `f[n] = f[n - f[n-1] - 1] + f[n - f[n-2] - 1]` | `f[1]=f[2]=1` | 42 |
| (g) | `f[n] = f[f[n-1]] + f[n - f[n-2] - 1]` | `f[1]=f[2]=1` | 41 |
| (h) | `f[n] = f[f[n-1]] + f[n - 2 f[n-1] + 1]` | `f[1]=f[2]=1` | 45 |

Case (e) is independently text-backed at `BOOK:12722-12724`. Cases (c) through (h), rather than (a)/(b), are the six fluctuation profiles on page 145; its caption's shared two-term seed must not be misapplied to row (a).

## Initial Construction Model

Use the T37 lossless tagged-prefix representation:

```text
configuration = NumericPrefix(origin=1, terms=(v1, ..., v[n-1]))
encoding      = Val(1,v1) · ... · Val(n-1,v[n-1]) · End(n)

active   = UniqueEnd.select(configuration)
reads    = ComputedPrefixAccess(program.address_tree,
                                demand=LEFTMOST_INNERMOST)
              .read(configuration, active)
writes   = ClosedRecurrenceRule(program.value_tree).emit(active, reads)
next     = SingleSpliceUpdate.apply(configuration, active, writes)
```

`ComputedPrefixAccess` evaluates only closed integer address nodes and returns a replayable ordered read DAG. Each syntactic `TermAt(address_expr)` occurrence is retained and records the target index, evaluated address, source term handle/value, expression path, demand order, and exact program provenance. Fixed T37 lag `k` is the restriction `TermAt(TargetIndex - Literal(k))`; T38 generalizes this responsibility rather than creating a family executor. D022 already permits a typed program-coupled selector/access component when one authoritative closed program supplies both applicability and the value used by RULE; this is not a callback loophole.

On success, RULE receives the resolved read tree, computes only the exact value, and replaces `End(n)` with `Val(n,next_value) · End(n+1)`; T16's atomic single splice preserves every old value. The strict integer AST cannot produce a nonintegral address: noninteger nodes are construction-invalid. If an evaluated exact address is below the origin, current/future, or otherwise absent, access returns the common zero-successor `Error(UndefinedTermReference)` with the complete old prefix and ordered failure witness. No write or event exists, and UPDATE is not invoked. This follows T35/T43 partial-evaluation precedent. `Invalid` remains appropriate for malformed AST/type/seed inputs before execution; T26's `Invalid(IncompatibleMosaic)` is an UPDATE-composition failure and is not the T38 analogue.

## Final First-Principles Architecture Matrix

| Responsibility | Class | Smallest reusable construction | Closed T38 delta |
|---|---:|---|---|
| DOMAIN/configuration | 1 | D070/T37 complete consecutive exact prefix in discrete `t+1D` | Strict origin-one positive-integer preset only |
| FRONTIER | 1 | T37 unique tagged `End(n)` | No T38 selector |
| NEIGHBORHOOD/access | 2 | T37 old-prefix term access | Closed value-computed address expressions, ordered nested demand, dynamic validity witnesses |
| RULE/write | 1/2 | T37 closed arithmetic expression and `End -> Val · End` write | Address results feed the same closed exact arithmetic/append result |
| UPDATE | 1/3 | D072 one-step lowering to T16 `SingleSpliceUpdate` | Same prefix/tag commuting square; no endpoint UPDATE |
| Invalid demand | 1/2 | Common no-commit `Error` result | Typed `UndefinedTermReference` reason and ordered read-path witness; not native halt/default |
| Trace/checkpoint | 1 | D073 compact prefix trace and verified checkpoints | Preserve adaptive read DAG per successful event/error attempt |
| Observers | 1/2 | Existing term/difference/digit/statistics/evaluation analyzers | Explicit c/d digit formulae, p/q address plots, evaluation tree, empirical qualifiers |
| New execution algebra | Not established | Branch-free SimpleProgram runner | No T38 executor, family branch, state class, or UPDATE law |

The computed access cannot be replaced by one T37 fixed lag: row (a) demands lag 1 at `n=2`, lag 2 at `n=3`, and progressively different value-selected distances under the same immutable program. Reading the complete prefix is semantically sufficient but does not justify a callback; the structural address AST and exact demand witness retain inspectability and program identity.

## Current Runtime Fit to Audit

| Responsibility | Current `src/ca` mechanism | T38 disposition |
|---|---|---|
| DOMAIN/support | Dense fixed shapes over canonical `[t,x,y,z]` | Add/reuse T37 dynamic ordered `t+1D` prefix support; term index is not stored rollout time |
| ALPHABET/value | Finite enumerated `int/float/str` values | Reuse planned arbitrary-precision exact positive-integer values; no object-array packing |
| FRONTIER | Fixed time-slice selection | Reuse the unique endpoint responsibility through a structural `End` selector |
| NEIGHBORHOOD/loci | Static coordinate offsets and callable predicates | Generalize loci with closed state-dependent address selectors/read DAGs; never use Python indexing or an unrestricted predicate |
| RULE | Family strings, finite tables, unrestricted `formulaic` callable | Use a closed recurrence/address AST with exact integer operations and structural identity |
| UPDATE | Fixed-support assignment/copy-forward | Reuse T16 single-splice lowering proved by T37/D072 |
| Runner | Named-family branches for current temporal families | Migrate through the shared structural runner; no `variable_recurrence` branch |
| Seeds/traces | Packed scalar history pairs and fixed NumPy episodes | Use exact consecutive seeds/checkpoints and compact prefix+append events/read DAGs |

## Evidence and Oracle Closure

1. Seventeen frozen source-query lanes close 102 unique monolith hits at `83 pre-Index / 19 actual-Index`. The pre-Index query partition is `14 native / 13 relation / 24 control / 32 exclusion`; the complete governed evidence partition is `20 / 36 / 44` with 49 explicit continuations. Actual Index closes at `3 / 9 / 6 / 1`, with the last row a guarded nested-sequence collision.
2. The complete retained/routed/guarded-image crosswalk closes 124 unique split owners at `98 exact / 15 image-basename / 11 normalized`, normalized minimum `0.999817`. Twenty-five Book semantic guards, five auxiliary guards, seven defect/limitation records, 22 source-model records, 15 image dispositions, and every query/partition/Index contract are digest-bound; unresolved count is zero.
3. Four governed rasters at `3 native / 1 relation / 0 control` and eleven exclusions bind 30 monolith/split references, 15 unique hashes, 653,438 bytes, and nine semantic assemblies. All four governed files are hash-bound; two are additionally limited-transcribed; none is pixel-replayed. Five semantic manifests freeze 51 records, including all eight rules/seeds/rows and the page-144 crop boundary.
4. The semantic oracle independently closes 325 visible append events and 1,122 ordered demands, 2,033 longer events and 7,114 demands, 325 prefix/tag/splice commutations, 97 fixed-lag restriction commutations, 64 bounded-window counterexamples, ten partiality/error cases within 14 hostile scenarios, 4,096 page-131 observer checks, 64 arbitrary-precision events up to 4,103 bits, ten compact lossless trace reconstructions, and 42 hostile rejections.
5. Direct literal equations and the generic `FRONTIER.select -> NEIGHBORHOOD.read -> RULE -> UPDATE.apply` path agree event by event. The asset/semantic integration gate equates eight formulas, eight seeds, eight horizons, and all 340 visible terms. The full witness trace is distinguished from D073's compact seed-plus-append projection, including zero-event and terminal-attempt replay.
6. Current-runtime inspection confirms the implementation delta belongs under closed loci/NEIGHBORHOOD selection and exact value/program schemas. Existing fixed tensor selectors and callable predicates do not yet encode dependent old-prefix addresses safely; this is a bounded generalization of an axis, not a T38 branch, state class, UPDATE, or executor.

## Corrected Goal 2 Handoff

- Reuse D070's `NumericPrefix`, origin/index/value invariants, exact seeds/checkpoints, tagged `Val* · End`, unique endpoint FRONTIER, append event, compact trace, and D072/T16 one-splice lowering.
- Generalize the existing loci/NEIGHBORHOOD access responsibility from T37 fixed lags into closed `TermAt(AddressExpr)` selectors over exact `Literal`, `TargetIndex`, ordered `Add/Sub/Mul`, and nested old-prefix term reads. T37 fixed lag remains a named restriction.
- Return ordered replayable access DAGs with stable old-prefix term handles, expression paths, exact address values, demanded order, and structural program provenance.
- Preserve source leftmost-innermost demand for partial expressions. Do not algebraically canonicalize across potentially failing reads or erase source order from structural identity.
- Route an actually demanded invalid address through the common no-commit `Error(UndefinedTermReference)` envelope with zero successors and no event. Add no T38-specific terminal/outcome class or policy menu.
- Add exact source presets (a)-(h), independent raster transcriptions, long-run conformance, address-safety checks, and page-131 observer/evaluator fixtures.
- Keep memoization as an implementation of visible complete-prefix state; keep p/q graphs, evaluation trees, binary-digit formulae, fluctuations, randomness tests, plots, and sounds downstream.
- Add no `VariableRecurrenceState`, new UPDATE, recursive executor, family branch, callback, host-language expression, hidden history/memo table, Python negative indexing, padding/default/wrap/clamp, or observer feedback.

## No-Cheating Checks

- No unrestricted callback, `eval`, host symbolic expression, formula string, pickle, or family-name rollout dispatch.
- No complete prefix/program packed into one opaque cell, object array, byte string, digest, or hidden executor closure.
- No term index conflated with rollout time; no reads from stored trajectory slices.
- No newest-value scalar, bounded suffix, memo cache, p/q plot, or evaluation tree called complete native state.
- No Python negative indexing, index zero, current/future/newborn read, modulo, wrap, clamp, pad, or implicit default.
- No algebraic cancellation/reordering that suppresses a source-demanded invalid read under leftmost-innermost semantics.
- No dynamic address chosen from partially updated/newborn state; all reads use one immutable old prefix.
- No missing/invalid address treated as identity, successful empty update, native halt, external stop, or invented boundary policy.
- No repeated equal values deduplicated; their indexed occurrences and read handles remain distinct.
- No finite display row, plot window, ellipsis, observed safety horizon, empirical randomness, or million-step sample strengthened into a halt/period/totality theorem.
- No source formula inferred solely from a raster without an explicit transcription record and independent regenerated prefix.
- No observer formula, closed form, binary-digit evaluator, memo strategy, or fast random-access method substituted for requested append-event provenance.
- No new state, FRONTIER, UPDATE, outcome algebra, executor, or runner branch merely because T38 has a separate catalog name.

## Completion Requirements

- [x] Every main, Notes, history, actual-Index, split, asset, alias, relation, control, and false-positive candidate is dispositioned with zero unresolved mechanics.
- [x] All eight raster rules/seeds/visible rows and every text-backed formula are independently transcribed, regenerated, and provenance-bound.
- [x] Complete prefix, origin/carrier, endpoint, computed access, ordered demand, RULE/write, UPDATE lowering, outcome, trace, and checkpoint semantics are exact.
- [x] Successful generic events commute one step at a time with direct recurrences and the T16 tagged-prefix representation.
- [x] Invalid addresses, evaluation order, partiality, source safety claims, observer/evaluator boundaries, and empirical qualifications are explicit and adversarially tested.
- [x] Source, asset, semantic, runtime-fit, hostile, portability, fail-closed, mode, Markdown, diff, scope, and repository-test gates pass.
- [x] D138, plan, evidence index, design ledger, architecture audit, and Goal 2 handoff are synchronized without a T38 state/update/executor.

## Stage Results

D138 closes T38 as a class-2 computed old-prefix access specialization over classes 1 and 3 reuse. Strict configuration is T37's complete positive origin-one `NumericPrefix` in discrete `t+1D`; FRONTIER is its unique `End(n)`; RULE emits its existing `End(n) -> Val(n,value) · End(n+1)` replacement; UPDATE is D072's lossless lowering to T16 exactly-one splice. The only new named responsibility is a closed dependent address selector/read DAG inside loci/NEIGHBORHOOD, with exact structural identity and leftmost-innermost occurrence witnesses. Fixed lag is a restriction of the same expression algebra.

An actually demanded address outside `[1,n)` returns the common zero-successor no-commit `Error(UndefinedTermReference)` and retains the last complete prefix; malformed programs and seeds remain construction-invalid. The strict AST admits only exact integers. Memoization is an implementation of visible prefix state, while digit formulae, fluctuation plots, p/q graphs, evaluation trees, sounds, and primitive-recursive classifications remain observers or relations. The guarded BOOK12738 repair prepends exactly one missing initial `1`, corroborated independently by BOOK12742; cropped pixels and empirical randomness/totality claims are not invented.

Oracle SHAs are source `1199125cd72abe8ba56a1d97534ee855a176acfc4fe510e5339912b45d3d1045`, asset `95a45d1d079309a0b56fff8411be3cae66aaf31fdd38d49411a62c50f5b887e2`, and semantic `8c18745fffe49d69e494ace35f2f44155cbf86f2c76c56d3a0a9bb340badfc80`; semantic digest is `faee16f26234a7b90da40e8642ddef63224898ac217e436efd9091df7f3764b9`. Root/relocated/import/compile/optimized/bad-usage, cross-interface, mutation, mode, Markdown, diff, scope, repository-test, and independent hostile-review gates pass. No prior stage reopens. Next: T40.
