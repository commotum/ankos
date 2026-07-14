# 46-T42-CF-SUBSTITUTION

Status: **IN PROGRESS — SOURCE, ASSET, SEMANTIC, ARCHITECTURE, AND HOSTILE-REVIEW CLOSURE PENDING**

## Current Facts

- T42 is CSV physical line 43, `Continued-Fraction-Driven Substitution Systems`; `ref/notes/CA-Types.md` section 42 supplies search vocabulary, not primary mechanics.
- The strict main evidence is the page-162 bridge at `BOOK:1850-1858`. It states that a continued-fraction term determines the generalized-substitution rule used at each step and restricts the illustrated connection to exactly two sine or cosine functions.
- The executable source rule is in the page-903 Notes at `BOOK:12587-12595`. For an irrational `h`, it constructs a finite rule schedule from `Reverse[Rest[ContinuedFraction[h,m]]]`, starts from `{0}`, applies each selected morphism in parallel, and adds `Floor[h]` only when interpreting the resulting binary word.
- If the finalized natural simple-continued-fraction prefix is `(a0,a1,...,a[m-1])`, strict execution order is `(a[m-1],...,a1)`. The reversal happens exactly once when the immutable finite program is constructed; coefficients are not pulled lazily during rollout.
- Coefficient `a>0` denotes the total nonempty binary morphism `rho_a(0)=0^(a-1)1`, `rho_a(1)=0^(a-1)10`. This is a closed injective coefficient-to-table codec, not a callback.
- `ContinuedFraction[h,m]` has `m` terms under the source's own definition at `BOOK:13030-13034`; `Rest` therefore supplies `m-1` rule events. The prose claim “first m rules” at `BOOK:12587` is an off-by-one source defect and must remain visible.
- The strict source fixes seed `(0,)`. A caller-selected seed, empty seed, nonbinary word, zero/nonpositive tail coefficient, rational-complete continued fraction, repeated-last-rule policy, cyclic wrap, or hidden infinite coefficient stream is a different profile.
- T40 already supplies the correct cross-stage contract: a T42 source carries a complete immutable replay-verified T40 `ExpansionResult`/coefficient handoff for a natural-order simple-CF prefix beginning at `a0`, with complete exact or complete certified proof strength and `prefix_of_infinite` termination. Detached IDs or a free coefficient tuple cannot impersonate that result.
- Explicit execution-ordered schedules are useful closed program data, but they require a separately tagged source schema. They must not fabricate T40 query provenance, `a0`, requested counts, or proof strength.
- The finite horizon is program identity. Extending a natural prefix prepends a rule after reversal, so an `m`-term run is not generally a resumable prefix of an `(m+1)`-term run.
- The Markov configuration is a nonempty finite binary word plus a visible schedule cursor. The cursor is configuration state, not DOMAIN, trace time, executor memory, or producer state.
- A lossless executable representation labels every word occurrence by the same phase: `(cursor,(b0,...,bn)) <-> ((cursor,b0),...,(cursor,bn))`. On its uniform-phase invariant image, one event is exactly an ordinary T13 all-occurrence/self-read/nonempty-word replacement followed by source-ordered concatenation.
- T42 therefore has discrete `t+1D` DOMAIN. Its changing finite ordered support is CONFIGURATION structure; binary data and finite phase are ALPHABET factors.
- Schedule exhaustion is a typed terminal result. It is not an empty word, fixed point, quiescence, failure, external horizon, or resource limit. Strict morphisms are nonempty, so native evolution never extinguishes the word.
- `Floor[h]` is an observer offset that maps binary symbols to the two mechanical-sequence values `Floor[h]` and `Floor[h]+1`. It is not substitution state and does not alter the rule.
- Quadratic-irrational coefficient repetition may collapse to ordinary fixed morphisms or fixed period-block macros. A multi-coefficient macro represents several T42 events and cannot be called a one-step T42 representation without an explicit step-scale relation.
- The digital-slope, cosine-axis-crossing, and billiard constructions are exact or source-stated relations/observers. The sine half-shift sibling is under-specified at `BOOK:13170-13172`; it does not authorize an invented rule generator.
- The page-162 raster is hash-bound and additionally limited-transcribed: the four displayed functions, visible execution-order coefficients, black/gray convention, and rule icons come from the plate. The prose supplies the general relation and the page-903 Notes supply the executable rule formula. Raster geometry never supplies a hidden program, window, coefficient evaluator, or pixel-derived transition.
- T42 adds no new execution algebra. It composes finalized program data, a product/tagged ALPHABET invariant, visible phase, T13 `AllOccurrences`/`Self`, a closed scheduled morphism table, and D019 `OrderedGenerationConcat` through the branch-free runner.
- In this audit, DOMAIN retains the project meaning of dimensional task/program space (`t+0D`, `t+1D`, and so on), whether discrete or continuous. It is not a name for the coefficient set, schedule, word support, or storage schema.

## Big Picture Objective

Reconstruct T42 as a finite, visibly scheduled binary substitution SimpleProgram whose immutable schedule is derived from a complete replay-verified continued-fraction result or supplied as separately tagged closed data. Exhaustively close main text, Notes, actual Index, splits, assets, source defects, rule orientation, horizon identity, exact T13 lowering, lineage, termination, T13/T18/T40/T41 boundaries, current runtime fit, and the Goal 2 handoff. Add a semantic component only where a concrete counterexample defeats the smallest reusable construction.

## Catalog Identity

- Stable ID: T42.
- Exact CSV name: Continued-Fraction-Driven Substitution Systems.
- CSV physical line: 43.
- Taxonomy section: 42.
- Strict main core: `BOOK:1850-1858`.
- Native executable Notes core: `BOOK:12587-12595`.
- Entry kind: finite scheduled parallel word substitution.
- Native DOMAIN: discrete `t+1D`.

## Search and Closure Contract

The source oracle must freeze reproducible discovery queries but may not treat regex recall as completeness. Closure must independently route:

1. every nonblank row in `BOOK:1850-1858`;
2. every nonblank row in `BOOK:12587-12595` plus the defining continued-fraction count/canonicalization seam at `BOOK:13030-13034`;
3. every actual-Index row reached by continued-fraction/substitution, axis-crossing, digital-slope, billiard, and named quadratic routes;
4. every followed relation, control, continuation, and source limitation, including the opposite-direction substitution-to-CF construction at `BOOK:13062-13068`;
5. every monolith/split owner and governed or excluded raster candidate; and
6. an independent Book-wide vocabulary lane and hostile page/alias/continuation set.

Every candidate is classified native, relation, control, structural, excluded, or unrelated. Main prose, Notes code, raster transcription, T40 coefficient production, T41 function queries, T13 substitution mechanics, and observer relations retain separate provenance. Completion requires zero unexplained source rows, Index rows, split owners, image candidates, and extraction defects.

## Construction-Bearing Book Evidence

### Main bridge: a continued-fraction term chooses each rule

- Provenance: `BOOK:1850-1858`.
- Establishes: the rule varies by step according to continued-fraction terms; square-root profiles are repetitive/nested; non-square-root profiles can be less regular; the stated connection is for exactly two sine/cosine functions.
- Does not establish: the exact coefficient-to-morphism formula, a coefficient evaluator, an infinite online source, a seed, a page-window/index origin, or a rule for three or more sine functions.

### Executable Notes formula

- Provenance: `BOOK:12587-12595`.
- Establishes: irrational source, natural CF prefix, reverse-rest execution orientation, the two binary replacement blocks, parallel whole-word replacement, seed `{0}`, `Floor[h]` observer offset, and the fixed-rule quadratic siblings.
- Does not establish: rational input, arbitrary seed, epsilon output, wrap/repeat after schedule exhaustion, or host-language replacement defaults.

### Coefficient count and carrier

- Provenance: `BOOK:13030-13034`, `13052`.
- Establishes: the first `m` terms form an `m`-coefficient prefix; simple-CF terms are exact integers and tail terms can be arbitrarily large.
- Consequence: `Rest` yields `m-1` events, and coefficients cannot be packed into a fixed finite rank or machine integer.

### Mechanical-word and relation evidence

- Provenance: `BOOK:12581-12595`, `13111-13129`, `13170-13172`, `14923-14935`.
- Establishes: the substitution word represents the two-valued difference sequence; digital slopes and cosine crossings reuse that word; billiards are related through slope continued fractions.
- Boundary: renderings, line segments, zero locations, curve samples, and billiard paths are observers/relations, not transition state. The sine `-1/2` clause does not specify a complete morphism schedule.

## Source Defects and Limitations That Must Remain Visible

### “First m rules” is off by one

The literal source expression is:

```text
Reverse[Rest[ContinuedFraction[h,m]]]
```

Under `BOOK:13030-13034`, `ContinuedFraction[h,m]` returns `m` coefficients including `a0`; `Rest` therefore contains `m-1` positive tail coefficients. Strict conformance reports `m-1` events. It does not silently call the prefix length `m+1` or append an invented coefficient.

### A longer horizon is not a resumed shorter run

For natural prefixes `p_m=(a0,...,a[m-1])` and `p_(m+1)=p_m+(a[m])`:

```text
schedule(p_m)     = (a[m-1],...,a1)
schedule(p_(m+1)) = (a[m],a[m-1],...,a1)
```

The extra rule appears at the beginning. A checkpoint from the shorter program therefore cannot continue as the longer program without changing already executed history. Requested term count and full source result remain program identity.

### Raster and sine-sibling limits

The four page-162 fixture identities and displayed coefficient sequences are limited manual transcription from `_page_162_Figure_1.jpeg`. The text independently supplies only the general bridge and executable Notes formula. At `BOOK:13172`, inserting `-1/2` into the mechanical-floor expression describes a sine observer but does not give a complete substitution rule generator; that sibling remains under-specified.

## Exact Normalization

Let a complete accepted natural simple-CF prefix be

```text
P = (a0,a1,...,a[m-1])
```

with signed integer `a0`, positive integer tail, proof strength `CompleteExact | CompleteCertified`, natural orientation, coefficient start zero, and `prefix_of_infinite` termination. Then:

```text
S = reverse(P.tail) = (a[m-1],...,a1)

rho_a(0) = 0^(a-1) 1
rho_a(1) = 0^(a-1) 1 0
```

`a0` remains source/result provenance and the observer offset. It is not executed as a rule. `m=1` yields the valid empty schedule and immediate `ScheduleExhausted` result from seed `(0,)`.

## Final Semantic Model

```text
ScheduleSource =
    T40ResultSource(complete replay-verified T40 coefficient handoff)
  | ExplicitExecutionSchedule(positive coefficients, structural provenance)

ScheduledMorphismProgram =
    source
  + execution_order_coefficients
  + rho_codec_version
  + strict_seed=(0,)

Configuration = (cursor, nonempty_binary_word)
Invariant     = 0 <= cursor <= len(schedule)

active = FRONTIER.select(configuration)
reads  = NEIGHBORHOOD.read(configuration, active)
writes = RULE(active, reads)
next   = UPDATE.apply(configuration, active, writes)
```

For `cursor < len(schedule)`, every old word occurrence fires once. Its read is its old binary value plus the visible current phase (directly or through the lossless replicated-phase representation). RULE emits the nonempty `rho_schedule[cursor](bit)` block with child ordinals. UPDATE consumes the old generation, concatenates blocks in source order, and advances the phase atomically. Newborns never fire in the same event. When `cursor == len(schedule)`, FRONTIER selects no rule-firing data occurrences and the common result reports `ScheduleExhausted` without an invented self-step.

## Lossless T13 Representation

Define

```text
e(i,(b0,...,bn)) = ((i,b0),...,(i,bn))
```

on the invariant image of nonempty words whose phase components are all equal. The inverse reads the shared phase and strips it from each data label. The compiled closed morphism is

```text
(i,b) -> [(i+1,c) for c in rho_schedule[i](b)]
```

for active phases. Thus:

```text
e(step_direct(program,state)) = step_T13(compiled(program),e(state))
```

one event for one event, preserving the complete word, phase, source-order children, lineage, outcome, and schedule exhaustion. The representation uses T13 `AllOccurrences`, a self read, nonempty block emission, and D019 `OrderedGenerationConcat`; it does not pack the word into a scalar or delegate to a hidden interpreter.

The compact `(cursor,word)` form and a tagged `Cursor(cursor) · Data*` form are also lossless interfaces when their exact inverse and atomic two-factor commit are retained. The uniform phase-product word is the smallest direct T13 lowering because every firing occurrence can read all rule-relevant state locally.

## Identity, Provenance, and Handoffs

- T40-sourced program identity retains the complete accepted T40 result/handoff and replays its query, context, representation, coefficient payload, proof outcome, termination, source kind, and orientation. A SHA is derived display/cache metadata, never authority.
- Explicit schedules carry their complete ordered positive coefficients and a distinct structural source tag. They do not carry fake T40 IDs or claims.
- Natural coefficient order, reversed execution order, and already-execution-ordered explicit data are different tagged roles. Reversal is neither implicit nor repeatable.
- The strict seed, schedule horizon, codec version, and source schema are program identity. Cursor and complete word are configuration identity.
- Occurrence IDs, child ordinals, source spans, and snapshot scope are replayable lineage/provenance. They do not change semantic word equality.
- T41 may produce the exact ratio `(alpha-1)/(alpha+1)` as definition/query data; T40 may expand it; T42 consumes only the finalized verified coefficient result. Producer work state, evaluator callbacks, curve samples, and root-finder state never enter T42.

## Outcomes and Trace

- `Advanced`: one schedule coefficient was selected, every old occurrence fired exactly once, one nonempty successor word was committed, and cursor advanced by one.
- `ScheduleExhausted`: no coefficient remains; zero successors/events are produced with the last complete configuration and source result intact.
- `Invalid`: malformed program/configuration, nonuniform phase representation, nonbinary word, nonpositive coefficient, wrong seed, cursor out of range, rational-complete strict source, or nonreplaying handoff.
- `Error`: a generic infrastructure/provenance failure before commit. No partial word or cursor update is committed.
- External horizon/resource cancellation is not native completion. A fixed or repeated word does not halt while a coefficient remains.
- A trace records complete ragged configurations, the coefficient and orientation, exact old occurrence handles/reads, emitted blocks, source-order child lineage, cursor transition, program/source identity, and outcome.

## Quadratic and Observer Boundaries

- Golden ratio tail coefficient `1` and `sqrt(2)` tail coefficient `2` reduce to repeated ordinary fixed `rho_1` and `rho_2` T13 programs.
- `sqrt(3)` has a period requiring a composition of coefficient rules. Its listed fixed substitution is a period macro: one macro event corresponds to more than one T42 event. The macro is valid only with an explicit step-scale/observation relation.
- The mechanical word plus `Floor[h]` reconstructs values in `{Floor[h],Floor[h]+1}`. This is an observer map.
- Digital slopes, axis crossings, nested plots, paths, rational approximants, coefficient statistics, and billiard itineraries are relation/query/rendering records. They do not alter native state, stopping, or rule selection.
- More-than-two-sine and under-specified sine-half-shift cases are exclusions/open relations, not callback escape hatches.

## Current Runtime Fit

`src/ca` is the intended SimplePrograms namespace, but its current executable surface remains limited to array-shaped fixed-support presets:

| Axis | Current surface | Smallest Goal 2 treatment |
|---|---|---|
| DOMAIN/configuration | rank-0..3 NumPy arrays with fixed shape | Reuse the already-required T13 finite ordered variable-support configuration and ragged trace |
| ALPHABET | flat finite `int | float | str` values | Add/reuse finite product/tagged schemas for `PhaseIndex x Bit` with a uniform-phase invariant |
| FRONTIER | executable `time_slice` only | Reuse T13 `AllOccurrences`, parameterized to select all data occurrences only while phase is active |
| NEIGHBORHOOD | `self_at` already exists, but only for array loci | Reuse self projection on typed word occurrences; no T42 access class |
| RULE | scalar-return families and callbacks | Add/reuse closed nonempty word-emission tables; compile the finite schedule into structural phase-indexed morphism data |
| UPDATE | fixed next-array writes/family rollout | Reuse D019 source-ordered old-snapshot generation concatenation and common terminal result |
| identity/serialization | family names, integer IDs, fixed arrays | Retain complete source result, schedule orientation/horizon, codec, phase, ragged word, and lineage structurally |

No runtime code is changed in Goal 1.

## First-Principles Classification

| Proposed responsibility | Class | Smallest reusable base | Required invariant / counterexample |
|---|---:|---|---|
| Discrete ordered word evolution | 1 | T13 finite ordered support and ragged trace | Complete nonempty old word retained |
| All-source firing/self read | 1 | T13 `AllOccurrences` + `Self` | Every old occurrence exactly once; no newborn reads |
| Ordered replacement UPDATE | 1 | D019 `OrderedGenerationConcat` | Source/block order and lineage preserved |
| Coefficient rule codec | 2/3 | Closed T13 morphism table schema | `a <-> (0->0^(a-1)1,1->0^(a-1)10)` round trip |
| Visible schedule phase | 2/3 | D032 visible program address + finite product/tagged label | Same word at distinct phases can have distinct successors; hidden generation is invalid |
| Compact versus replicated phase | 3 | `(cursor,word) <-> (PhaseIndex x Bit)+` | All phase labels equal; one-event commuting square |
| T40 coefficient source | 1/2 | D139 replay-verified result/handoff | Complete result replay; exact/certified prefix-of-infinite only |
| Explicit schedule source | 2 | Closed ordered positive tuple | Separate tag; no fabricated query provenance |
| Schedule exhaustion | 1/2 | Common zero-successor terminal outcome | Distinct from empty/fixed/quiescent/horizon/error |
| New execution algebra | Not established | T13/D019 plus D032 and D139 | No T42 UPDATE, executor, family branch, callback, or class-4 category |

## Goal 2 Handoff

Goal 2 should:

1. Add or reuse a closed `ScheduledMorphism` preset over a finite immutable execution-order schedule of total nonempty binary morphisms.
2. Accept either a complete replay-verified D139/T40 coefficient handoff or a separately tagged explicit schedule. Never accept detached provenance IDs, a callback, generator, iterator, CAS object, or arbitrary host expression.
3. Normalize accepted natural simple-CF coefficients by dropping signed `a0` and reversing the positive tail exactly once. Preserve original result, requested count, source kind, proof strength, termination, and orientation.
4. Fix strict seed `(0,)`; model cursor visibly; report the valid zero-event `m=1` program and `m-1` event count.
5. Compile to the lossless uniform `PhaseIndex x Bit` T13 representation, or implement the isomorphic compact representation with an explicit inverse and full-result commuting conformance.
6. Reuse `AllOccurrences`, self reads, nonempty word emissions, D019 old-snapshot source-order concatenation, ragged traces, lineage, and common outcomes without T42 dispatch.
7. Preserve `ScheduleExhausted`, external horizon, invalid source, error, and resource cancellation as distinct results. Do not wrap, repeat, infer phase from time, or resume a longer reversed-prefix program from a shorter one.
8. Keep `Floor[h]`, digital slopes, axis crossings, quadratic macros, coefficient statistics, and billiards as observers/relations with exact step-scale and proof labels.
9. Bind the page-162 limited transcription and image hash as fixture provenance only. Never reconstruct a program, geometry, coefficient evaluator, or hidden state from raster pixels.

## Rejected Shortcuts

- A `CFSubstitutionState`, T42 UPDATE, executor, rollout-family branch, or second substitution runner.
- A detached query/result digest, user-asserted proof strength, or free coefficient tuple presented as a T40 result.
- A fake `QueryProvenance` wrapper for explicit schedules.
- Lazy producer callbacks, generators, streams, CAS objects, or evaluator work state consulted during rollout.
- Reversing twice, omitting reversal, consuming `a0` as a rule, or calling `m-1` events `m` events.
- Deriving cursor from event count, hiding it in executor state, repeating the last rule, cycling, wrapping, or silently extending the schedule.
- Arbitrary/empty seeds, epsilon blocks, unmatched-symbol identity, in-place replacement, newborn firing, unordered block union, or fixed-capacity padding.
- Packing the complete word into one scalar/object cell or compiling the construction to a CA merely to claim coverage.
- Treating a period-block macro as one native T42 event without a step-scale relation.
- Reading functions, coefficients, rules, words, windows, or transitions from pixels; feeding observer data back into evolution.
- Inventing the sine half-shift rule generator or extending the two-function claim to arbitrary function combinations.

## Frozen Source Closure

Pending the final source-oracle freeze and independent hostile review.

## Frozen Asset Closure

Pending final source-interface binding, limited-transcription correction, semantic-interface binding, and hostile review.

## Frozen Semantic Closure

Pending replacement of detached provenance with the complete replay-verified T40 handoff and final hostile review.

## Completion Requirements

- [ ] Every strict-main, native-Notes, actual-Index, split, relation, control, continuation, exclusion, and source-defect candidate is dispositioned with zero unresolved mechanics.
- [ ] Every governed or excluded raster candidate is hash-bound; the page-162 manual transcription and all nonauthority limits are explicit.
- [ ] Natural-prefix orientation, signed `a0`, positive unbounded tail, `m-1` event count, fixed seed, horizon identity, and exhaustion are independently verified.
- [ ] Direct compact, tagged, and uniform-phase T13 representations commute one event at a time with complete outcomes and lineage.
- [ ] T40 handoffs replay complete results and reject forged IDs, coefficients, outcomes, termination, callbacks, and producer state; explicit schedules use a separate schema.
- [ ] Quadratic macros, rational dual forms, mechanical-word observers, page-162 fixtures, and sine/digital-slope/billiard boundaries are adversarially tested.
- [ ] Source, asset, semantic, cross-interface, mutation, portability, fail-closed, mode, Markdown, diff, scope, repository-test, and independent hostile-review gates pass.
- [ ] D140, plan, evidence index, design ledger, architecture audit, and Goal 2 handoffs are synchronized with no new execution algebra.

## Stage Results

Pending oracle, architecture, integration, and hostile-review closure.
