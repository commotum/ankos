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
- A lossless executable representation labels every word occurrence by the same phase: `(cursor,(b0,...,bn)) <-> ((cursor,b0),...,(cursor,bn))`. On its uniform-phase invariant image, each live event with `cursor < len(schedule)` is exactly an ordinary T13 all-occurrence/self-read/nonempty-word replacement followed by source-ordered concatenation. Exhaustion is the shared terminal envelope, not a T13 morphism event.
- T42 therefore has discrete `t+1D` DOMAIN. Its changing finite ordered support is CONFIGURATION structure; binary data and finite phase are ALPHABET factors.
- Schedule exhaustion is a typed terminal result. It is not an empty word, fixed point, quiescence, failure, external horizon, or resource limit. Strict morphisms are nonempty, so native evolution never extinguishes the word.
- `Floor[h]` is an observer offset that maps binary symbols to the two mechanical-sequence values `Floor[h]` and `Floor[h]+1`. It is not substitution state and does not alter the rule.
- A constant or periodic quadratic-irrational schedule has a fixed-morphism-equivalent live prefix, and a period block may be represented by a fixed macro. The finite T42 horizon and terminal outcome remain part of the construction: even a constant schedule does not globally become a nonhalting T13 program. A multi-coefficient macro represents several T42 events and cannot be called a one-step T42 representation without an explicit step-scale relation.
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

StrictSourcePreset =
    ScheduledMorphismProgram
  + initial_configuration=(phase=0, word=(0,))

Configuration = (cursor, nonempty_binary_word)
Invariant     = 0 <= cursor <= len(schedule)

active = FRONTIER.select(configuration)
reads  = NEIGHBORHOOD.read(configuration, active)
writes = RULE(active, reads)
next   = UPDATE.apply(configuration, active, writes)
```

For `cursor < len(schedule)`, every old word occurrence fires once. Its read is its old binary value plus the visible current phase (directly or through the lossless replicated-phase representation). RULE emits the nonempty `rho_schedule[cursor](bit)` block with child ordinals. UPDATE consumes the old generation, concatenates blocks in source order, and advances the phase atomically. Newborns never fire in the same event. When `cursor == len(schedule)`, the shared terminal-result path reports `ScheduleExhausted` without invoking the T13 morphism/update path, inventing a self-step, or changing the final word. In particular, an empty selected set must not be passed to D019: its no-selected generation case consumes the old word, which would be the wrong terminal semantics here.

## Lossless T13 Representation

Define

```text
e(i,(b0,...,bn)) = ((i,b0),...,(i,bn))
```

on the invariant image of nonempty words whose phase components are all equal. The inverse reads the shared phase and strips it from each data label. The compiled closed morphism is

```text
(i,b) -> [(i+1,c) for c in rho_schedule[i](b)]
```

for active phases. Thus, for every live phase `i < len(schedule)`:

```text
e(step_direct(program,state)) = step_T13(compiled(program),e(state))
```

one event for one event, preserving the complete word, phase, source-order children, lineage, and `Advanced` outcome. At `i == len(schedule)`, the direct and represented configurations instead enter the same generic zero-successor `ScheduleExhausted` envelope with the complete final word retained and no D019 commit. The representation uses T13 `AllOccurrences`, a self read, nonempty block emission, and D019 `OrderedGenerationConcat` only for live phases; it does not pack the word into a scalar or delegate to a hidden interpreter.

The compact `(cursor,word)` form and a tagged `Cursor(cursor) · Data+` form are also lossless interfaces when their exact inverse and atomic two-factor commit are retained. They are not plain-self-read T13 execution carriers: direct execution would require generic shared-factor access and a compound phase/data commit. The uniform phase-product word is therefore the canonical executable lowering and the smallest direct T13 reuse because every firing occurrence can read all rule-relevant state locally.

The executable invariants are: a finite immutable schedule of exact positive coefficients; a nonempty word; one phase in `0..L` replicated uniformly across all labels; a total alphabet-closed nonempty emission table for every live phase; exact old-snapshot occurrence coverage; no newborn firing; stable source/child ordering and lineage; and deliberately nonfiring terminal-phase labels whose complete final word is retained.

## Identity, Provenance, and Handoffs

- T40-sourced program identity retains the complete accepted T40 result/handoff and replays its query, context, representation, coefficient payload, proof outcome, termination, source kind, and orientation. A SHA is derived display/cache metadata, never authority.
- Explicit schedules carry their complete ordered positive coefficients and a distinct structural source tag. They do not carry fake T40 IDs or claims.
- Natural coefficient order, reversed execution order, and already-execution-ordered explicit data are different tagged roles. Reversal is neither implicit nor repeatable.
- Schedule horizon, codec version, and source schema are transition-program identity. The strict seed `(0,)` is the initial configuration fixed by the source preset and belongs to preset/run identity, not the morphism transition key. Cursor and complete word are configuration identity.
- Occurrence IDs, child ordinals, source spans, and snapshot scope are replayable lineage/provenance. They do not change semantic word equality.
- T41 may produce the exact ratio `(alpha-1)/(alpha+1)` as definition/query data; T40 may expand it; T42 consumes only the finalized verified coefficient result. Producer work state, evaluator callbacks, curve samples, and root-finder state never enter T42.

## Outcomes and Trace

- `Advanced`: one schedule coefficient was selected, every old occurrence fired exactly once, one nonempty successor word was committed, and cursor advanced by one.
- `ScheduleExhausted`: no coefficient remains; the shared terminal envelope produces zero successors/events with the last complete configuration and source result intact, without calling D019 on an empty frontier.
- `Invalid`: malformed program/configuration, nonuniform phase representation, nonbinary word, nonpositive coefficient, wrong seed, cursor out of range, rational-complete strict source, or nonreplaying handoff.
- `Error`: a generic infrastructure/provenance failure before commit. No partial word or cursor update is committed.
- External horizon/resource cancellation is not native completion. A fixed or repeated word does not halt while a coefficient remains.
- A trace records complete ragged configurations, the coefficient and orientation, exact old occurrence handles/reads, emitted blocks, source-order child lineage, cursor transition, program/source identity, and outcome.

## Quadratic and Observer Boundaries

- Golden ratio tail coefficient `1` and `sqrt(2)` tail coefficient `2` give live prefixes equivalent to repeated ordinary fixed `rho_1` and `rho_2` T13 events; their declared finite horizons still end in `ScheduleExhausted`.
- `sqrt(3)` has a period requiring a composition of coefficient rules. Its listed fixed substitution is a period macro: one macro event corresponds to more than one T42 event. The macro is valid only with an explicit step-scale/observation relation.
- The mechanical word plus `Floor[h]` reconstructs values in `{Floor[h],Floor[h]+1}`. This is an observer map.
- Digital slopes, axis crossings, nested plots, paths, rational approximants, coefficient statistics, and billiard itineraries are relation/query/rendering records. They do not alter native state, stopping, or rule selection.
- More-than-two-sine and under-specified sine-half-shift cases are exclusions/open relations, not callback escape hatches.

## Current Runtime Fit

`src/ca` is the intended SimplePrograms namespace; CA is one preset. The Phase 1 implementation currently exposes array-shaped fixed-support presets, while the T13/D019 work below is already required shared SimplePrograms infrastructure rather than evidence that T42 falls outside the library:

| Axis | Current surface | Smallest Goal 2 treatment |
|---|---|---|
| DOMAIN/configuration | rank-0..3 NumPy arrays with fixed shape | Implement the already-required T13 finite ordered variable-support configuration and ragged trace |
| ALPHABET | flat finite `int | float | str` values | Implement the generic product/tagged schemas already required across SimplePrograms; T42 uses `PhaseIndex x Bit` plus a uniform-phase invariant |
| FRONTIER | executable `time_slice` only | Implement T13 `AllOccurrences`, optionally restricted by the generic live-phase predicate; no T42 selector class |
| NEIGHBORHOOD | `self_at` already exists, but only for array loci | Generalize the existing self projection to typed word occurrences; no T42 access class |
| RULE | scalar-return families and callbacks | Implement the already-required closed nonempty word-emission table and compile the finite schedule into structural phase-indexed morphism data |
| UPDATE | fixed next-array writes/family rollout | Implement/reuse D019 source-ordered old-snapshot generation concatenation for live phases and the common terminal envelope at exhaustion |
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
| Schedule exhaustion | 1/2 | Common zero-successor terminal outcome | Retains the final nonempty word; does not lower through D019's no-selected generation case; distinct from empty/fixed/quiescent/horizon/error |
| New execution algebra | Not established | T13/D019 plus D032 and D139 | No T42 UPDATE, executor, family branch, callback, or class-4 category |

## Goal 2 Handoff

Goal 2 should:

1. Add a closed constructor/preset over T13 for a finite immutable execution-order schedule of total nonempty binary morphisms; do not add a new `ScheduledMorphism` semantic class.
2. Accept either a complete replay-verified D139/T40 coefficient handoff or a separately tagged explicit schedule. Never accept detached provenance IDs, a callback, generator, iterator, CAS object, or arbitrary host expression.
3. Normalize accepted natural simple-CF coefficients by dropping signed `a0` and reversing the positive tail exactly once. Preserve original result, requested count, source kind, proof strength, termination, and orientation.
4. Fix strict seed `(0,)` in the source preset/run request, separately from transition-program identity; model cursor visibly; report the valid zero-event `m=1` construction and `m-1` event count.
5. Compile each live phase to the lossless uniform `PhaseIndex x Bit` T13 representation, or implement the isomorphic compact representation with an explicit inverse and full-result commuting conformance. At exhaustion use the shared terminal envelope and retain the final word; never route an empty active set through D019.
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

`46-T42-source-oracle.py` freezes fourteen discovery lanes and their 48-row union, but completeness is independent of search recall. The Book-wide lane closes 39 candidates with ten explicit exclusions and zero unresolved. Total retained evidence is 54 rows at `10 native / 21 relation / 23 control`; the fixed strict-main and executable-Notes cores each close five construction-bearing rows. The complete 897-row actual Index is dispositioned as `3 native / 8 relation / 78 control / 808 unrelated`, including 70 relevant rows missed by the ordinary query union. The 951-row split crosswalk closes at `927 exact / 12 image-basename / 9 normalized / 3 explicit omissions`, normalized minimum `0.995885`.

The source audit binds 21 semantic guards, twelve auxiliary guards, ten source-defect records, 25 source-model records, the complete Index disposition, every strict-core row, and the 12-image candidate interface. Its independent source-logic audit closes fifteen obligations, including signed `a0`, positive unbounded tail coefficients, reverse-rest orientation, the `m-1` event defect, strict seed, terminal horizon, observer offset, raster boundary, and under-specified sine sibling. Audit digest is `2726957389d256722469424e41ea2e92188ba5e30d7ab52c4df2598dd7250aa6`; script SHA-256 is `27dfafe8798ce65af8d282440c85f02ae7d8d591f0fec30350ad52e41a25270d`.

Normal, JSON, explicit-Book, silent-import, compilation, relocation, catalog/split/Index mutation, optimized-mode, and malformed-usage gates pass or fail closed as required. No source or image disposition remains unresolved.

## Frozen Asset Closure

`46-T42-asset-oracle.py` closes the twelve governed images at `1 native / 11 relation / 0 control`, 24 source references (`12 monolith / 12 split`), twelve unique files/hashes, 285,055 bytes, and two five-file relation assemblies. All twelve are `HASH_BOUND`; page 162 is additionally `LIMITED_TRANSCRIBED`; none is pixel-replayed. Every file is baseline JFIF 1.01, three-component RGB with its exact dimensions, byte count, and SHA-256 bound. The structural asset manifest is `881c5c67fbf2aa6eb6bc6b8b0417b77df0057e24d657e72a08aac4f58d8cd2f5`; ledger digest is `42e6fcc06ad821257a3fdaa81a1ca2cb8c71a1449a44dd4250f7644bc0d16b29`.

The limited-transcription interface carries four named page-162 fixture profiles, execution-order coefficient rows, ten rule-icon entries, and the black/gray convention. Independent text supplies `rho`; replay closes 25 events, 301 old-source firings, and 599 emitted children. The trace manifest, which now binds the `LIMITED_TRANSCRIBED` evidence label, is `df358b3c335e09333a1110b7d25f38bb4745dc6598b8095c7c4fa766d925ef12`; the semantic-interface manifest digest is `a29095461ff79de0d08ebd5d2347a5c0edd8ff3151363264ff2fe61892a88556`. Twelve byte mutations and ten manifest/interface mutations fail closed. Source and semantic interfaces pass; script SHA-256 is `116b1c7e95e71fb94921b85c303d0da70f79fa6d2d7c2653b7d1aaa02a34faeb`.

## Frozen Semantic Closure

`46-T42-semantic-oracle.py` accepts three complete replay-verified T40 handoffs carrying 32 exact plus twelve certified coefficients, including one signed-`a0` case, and rejects rational completion and every detached/forged identity, coefficient, proof, termination, certificate, callback, and producer-state variant. Explicit schedules use a separate structural schema. Eight natural-prefix cases prove 36 source terms produce 28 events and seven longer horizons prepend rather than resume.

The exact transition audit closes two terminal cases across six direct/tagged/product views, retaining three final symbols and rejecting two empty D019 commits. It replays four page-162 fixtures over 25 events/301 source firings/599 children; closes 630 active and 390 completion cases across thirteen bounded programs; proves all 630 canonical replicated-product T13 commutations with 5,145 children and exact lineage; and retains compact/tagged carriers only as lossless interfaces. Mechanical-word checks cover five positive and five signed-`a0` cases, two `d=1` alignments, and two guarded `d=0` mismatches. Rational dual forms, reversal, horizon, word/cursor loss, `m=1`, three quadratic tables/62 word cases, the two-event `sqrt(3)` macro, one false one-step rejection, 64 coefficient-table round trips, and 4,224 emitted codec symbols are independently guarded.

The public audit sees 35 dataclasses, zero forbidden native roles, zero class-4 algebras, and 69 hostile rejections. Strict seed is absent from transition-program identity; uniform `PhaseIndex x Bit` is the canonical executable carrier; exhaustion retains the final word through the common terminal envelope without invoking D019. No evaluator, raster program, family executor, or new UPDATE exists. Semantic digest is `6bc8f95d07c32b5983c8b0890c7f9b8a07e511c25d77b12c7963ce9fc36b5c1d`; script SHA-256 is `e4794537b9d5d3820c4a0bb484b89f6e4dd1f9b489c132653d82b9815b721213`. Normal, relocation, silent-import, compilation, optimized-mode, and malformed-usage gates pass or fail closed as required.

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
