# 44-T38-VARIABLE-RECURRENCE

Status: **IN PROGRESS — FIRST-PRINCIPLES SOURCE, ACCESS, AND REPRESENTATION AUDIT ACTIVE**

## Current Facts

- T38 is CSV physical line 39, `Variable-Index Recursive Sequences`; `ref/notes/CA-Types.md` section 38 supplies search vocabulary, not primary mechanics.
- The Book does not introduce a second printed heading for T38. The semantic boundary begins inside `Recursive Sequences` at `BOOK:1569`, where a term value determines which earlier index is read. T37's fixed-distance material ends at `BOOK:1567`.
- The native configuration remains T37's complete consecutive exact numeric prefix in discrete `t+1D`; term index is the spatial/indexed support coordinate and rollout event count remains `t`.
- The strict main evidence is `BOOK:1569-1617` plus `_page_144_Figure_3.jpeg` and `_page_145_Figure_1.jpeg`. Eight displayed rules use only integer constants, addition/subtraction, target index `n`, and nested reads of already-generated terms.
- The source explicitly warns that computed addresses may yield meaningless `f[0]`, `f[-1]`, or `f[-2]`, while stating that the eight displayed rules avoid this problem (`BOOK:1571-1575`). This is a runtime read-validity boundary, not evidence for wrap, clamp, padding, default values, or a catalog-specific halt.
- The Notes give the memoized definition for displayed case (e) and fix leftmost-innermost evaluation as the ordinary demand order (`BOOK:12720-12726`). An algebraic cancellation such as `f[-1]-f[-1]` does not license skipping those demanded reads under that evaluator.
- The Notes distinguish native recurrence from derived descriptions: exact formulae for case (d), binary-digit descriptions for cases (c)/(d), fluctuation statistics, address plots, and evaluation trees consume or analyze the sequence but do not select a different native UPDATE (`BOOK:12728-12767`).
- The eight strict rules share T37's unique endpoint source and one-term persistent append. T38 changes the old-prefix access expression, not configuration topology, write shape, UPDATE, runner, or executor.
- The `invalid_index_policy` menu in the taxonomy note is not source authority. Primary-source conformance treats an actually demanded non-old-prefix reference as an undefined attempted step: the common no-commit error envelope retains the last complete prefix and commits no event.

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

The page-144 plate visibly supplies the following eight rules. These transcriptions remain provisional until the asset oracle independently binds every glyph, seed, visible row, and regenerated prefix.

| Row | Closed recurrence | Fresh seed |
|---|---|---|
| (a) | `f[n] = 1 + f[n - f[n-1]]` | `f[1]=1` |
| (b) | `f[n] = 2 + f[n - f[n-1]]` | `f[1]=f[2]=1` |
| (c) | `f[n] = f[f[n-1]] + f[n - f[n-1]]` | `f[1]=f[2]=1` |
| (d) | `f[n] = f[n - f[n-1]] + f[n - f[n-2] - 1]` | `f[1]=f[2]=1` |
| (e) | `f[n] = f[n - f[n-1]] + f[n - f[n-2]]` | `f[1]=f[2]=1` |
| (f) | `f[n] = f[n - f[n-1] - 1] + f[n - f[n-2] - 1]` | `f[1]=f[2]=1` |
| (g) | `f[n] = f[f[n-1]] + f[n - f[n-2] - 1]` | `f[1]=f[2]=1` |
| (h) | `f[n] = f[f[n-1]] + f[n - 2 f[n-1] + 1]` | `f[1]=f[2]=1` |

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

`ComputedPrefixAccess` evaluates only closed integer address nodes and returns a replayable ordered read DAG. Each `TermAt(address_expr)` records the target index, evaluated address, source term handle/value, expression path, and exact program provenance. Fixed T37 lag `k` is the restriction `TermAt(TargetIndex - Literal(k))`; T38 generalizes this responsibility rather than creating a family executor.

On success, RULE replaces `End(n)` with `Val(n,next_value) · End(n+1)`, and T16's atomic single splice preserves every old value. If a demanded address is nonintegral, below the origin, current/future, or otherwise absent, access returns the common zero-successor `Error(UndefinedTermReference)` with the complete old prefix and ordered failure witness. No write or event exists, and UPDATE is not invoked.

## First-Principles Architecture Matrix

| Responsibility | Provisional class | Smallest reusable construction | T38 delta to prove |
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
| NEIGHBORHOOD/loci | Static coordinate offsets and callable predicates | Add closed state-dependent address selectors/read DAGs; never use Python indexing or an unrestricted predicate |
| RULE | Family strings, finite tables, unrestricted `formulaic` callable | Use a closed recurrence/address AST with exact integer operations and structural identity |
| UPDATE | Fixed-support assignment/copy-forward | Reuse T16 single-splice lowering proved by T37/D072 |
| Runner | Named-family branches for current temporal families | Migrate through the shared structural runner; no `variable_recurrence` branch |
| Seeds/traces | Packed scalar history pairs and fixed NumPy episodes | Use exact consecutive seeds/checkpoints and compact prefix+append events/read DAGs |

## Evidence and Oracle Work Plan

1. Build redundant source-query lanes for the main prose, dynamic-reference formulae, meaningless-index boundary, exact asset names, Notes memoization/evaluation, cases (c)/(d)/(e)/(f), p/q address plots, evaluation trees, Conway/Hofstadter history, actual Index aliases, and broad recursive-function false positives.
2. Partition every pre-Index and actual-Index hit into native, relation, control, or exclusion; reverse-close every governed line to a unique structural split owner with explicit OCR repairs and zero unresolved candidates.
3. Bind `_page_144_Figure_3.jpeg`, `_page_145_Figure_1.jpeg`, `_page_922_Figure_2.jpeg`, every adjacent candidate, monolith/split reference, path, size, dimensions, SHA, role, assembly, and pixel-semantics boundary.
4. Independently transcribe and regenerate all eight rules, seeds, visible prefixes, page-145 formulas, and any exact p/q/evaluation-tree data recoverable from the governed assets. Keep plotted/statistical claims qualified where pixels do not yield exact samples.
5. Evaluate each program two ways: a direct mathematical recurrence and a generic structural access/read-DAG/RULE/splice path. Commute complete `StepResult`, prefix/tag state, reads, writes, lineage, and compact traces one event at a time.
6. Exhaustively exercise every address-expression node, nested read, leftmost-innermost order, same-value/different-index occurrence, old-snapshot restriction, malformed/noninteger/current/future/nonpositive address, invalid demanded versus algebraically cancelable reference, and cross-program replay.
7. Generate long exact traces for all eight source presets; check every address before access, positivity, one-term growth, source statements, arbitrary precision, page-131 exact formulae, and observer boundaries without strengthening empirical claims.
8. Audit `simple_programs.md`, `src/ca`, T16/T37/T39/T43, the design ledger, architecture audit, plan, evidence index, and Goal 2 handoff before proposing any new public type.

## Provisional Corrected Goal 2 Handoff

- Reuse D070's `NumericPrefix`, origin/index/value invariants, exact seeds/checkpoints, tagged `Val* · End`, unique endpoint FRONTIER, append event, compact trace, and D072/T16 one-splice lowering.
- Generalize T37 fixed-lag access into closed `TermAt(AddressExpr)` nodes over exact `Literal`, `TargetIndex`, ordered `Add/Sub/Mul`, and nested old-prefix term reads. T37 fixed lag remains a named restriction.
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

- [ ] Every main, Notes, history, actual-Index, split, asset, alias, relation, control, and false-positive candidate is dispositioned with zero unresolved mechanics.
- [ ] All eight raster rules/seeds/visible rows and every text-backed formula are independently transcribed, regenerated, and provenance-bound.
- [ ] Complete prefix, origin/carrier, endpoint, computed access, ordered demand, RULE/write, UPDATE lowering, outcome, trace, and checkpoint semantics are exact.
- [ ] Successful generic events commute one step at a time with direct recurrences and the T16 tagged-prefix representation.
- [ ] Invalid addresses, evaluation order, partiality, source safety claims, observer/evaluator boundaries, and empirical qualifications are explicit and adversarially tested.
- [ ] Source, asset, semantic, runtime-fit, hostile, portability, fail-closed, mode, Markdown, diff, scope, and repository-test gates pass.
- [ ] D138, plan, evidence index, design ledger, architecture audit, and Goal 2 handoff are synchronized without a T38 state/update/executor.

## Stage Results

In progress. The primary semantic boundary and smallest reusable architecture are reconstructed; exhaustive source, asset, semantic, runtime, integration, and hostile-review closure remain pending.
