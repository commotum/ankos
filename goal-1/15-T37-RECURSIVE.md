# 15-T37-RECURSIVE

Status: **REOPENED — ARCHITECTURE AUDIT; EVIDENCE CLOSED**

The evidence/search closure and conformance fixtures remain valid. The stage's own sufficient-window result reopens the claim that a full prefix is the only canonical Markov state; endpoint growth is an UPDATE choice inside the shared runner, not a recursive-sequence executor.

## Current Facts

- Exact catalog row: T37, CSV line 38, `Recursive Sequences`; taxonomy seed `ref/notes/CA-Types.md:1022-1048`. The taxonomy supplies search vocabulary, not authoritative mechanics.
- The canonical strict source is `BOOK:1555-1567`, with a clean duplicate at `CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:159-171`. T38 begins semantically at `BOOK:1569`, despite sharing the printed section heading, when a term value computes an earlier index.
- The book defines an indexed sequence `f[1],f[2],...`, computes one new `f[n]` from fixed-distance earlier terms, and preserves those terms as the generated sequence. The honest semantic state is therefore the complete indexed prefix, not only its last scalar and not a hidden trajectory history.
- The strict page-143 figure contains six linear affine fixed-lag recurrences. It has exact displayed horizons `38,48,22,26,44,27`, including seeds; the unequal horizons are layout choices followed by ellipses, not native stop conditions.
- The figure gives row (e) as `f[n]=f[n-1]-f[n-2]` and row (f) as `f[n]=-f[n-1]+f[n-2]`. `BOOK:12690` and the official Note incorrectly call row (f)'s characteristic equation case (e). This is a source erratum, not repository OCR damage.
- A normalized `AffineFixedLag` program covers every strict row and noncontiguous fixed lags such as Perrin. The Notes' factorial example justifies a separately named closed fixed-lag arithmetic-expression extension; it does not justify a host callback.
- Each valid event reads only old prefix terms, computes exactly one value, and append-preserves the entire old prefix. This requires a ninth public update law, `AppendOnlySequenceUpdate`; T34 assignment, T16 matched-span splice, and T17 prefix-consume/tail-append have different validators and mutation laws.
- A lag window plus the next absolute index is future-sufficient for a fixed-lag program, but it is a lossy transition quotient. It is not canonical prefix equality and cannot reconstruct discarded terms without the seed/checkpoint and complete append log.
- Every valid exact recurrence event has one successor forever. A repeated numeric term or periodic suffix never creates an unchanged state or full-state cycle because the indexed prefix grows.
- Exact signed integers and reduced rationals reuse T34 value/domain/string-codec obligations. Fixed-width NumPy arithmetic, implicit modulus, floats, and unsafe JSON numbers cannot represent the strict construction.
- Current AR2 code is a related finite modular two-lag recurrence, not T37: it hides one seed value, reads trajectory times, decodes coefficients from a finite rule ID, coerces to `np.int64`, applies a modulus, and emits scalar samples rather than prefix states.
- The direct-name union found 48 occurrences on 42 lines, the fixed-lag token query 23/13, the focused semantics query 32/20, the literal program token 20/20, the alias/control query 10/10, and named saturation 160/118. Every candidate is dispositioned and strict mechanics have zero unresolved search gaps.

## Updated Assumptions

- `NumericPrefix(domain,index_origin,terms)` is canonical semantic state. The term at tuple position `i` has mathematical index `index_origin+i`.
- A canonical fresh seed contains exactly `max_lag` contiguous terms. A longer prefix is a separately typed checkpoint and must be verified from the minimal seed before it can be resumed.
- The strict public rule is `AffineFixedLag(domain,bias,coefficients)`, where coefficients are a canonical sparse map from positive literal lags to exact scalars. At least one nonzero coefficient is required.
- `FixedLagArithmeticExpr` is a named Notes extension with only literals, target index, positive literal lag references, negation, addition, subtraction, and multiplication. Computed indices, callbacks, branches, division, powers, and arbitrary recursive calls remain excluded.
- Static validation rejects lag zero, negative lags, current/future references, duplicate lag entries, mixed domains, empty/short fresh seeds, and hidden defaults. Strict T37 needs no runtime invalid-index policy.
- Exact program identity is structural after constructor normalization. Mathematical equivalence of two recurrence formulas, characteristic roots, or closed forms is an observer and does not quotient program identity.
- A compact seed-plus-append-event record may encode the full trace without materializing quadratically many nested prefixes. Storage compression does not change state semantics.
- The book's final displayed row is a term-stream/prefix observer. A rollout trace is the nested sequence of prefix states and append events; these are not interchangeable.
- Horizon, cancellation, resource exhaustion, backend failure, characteristic analysis, periodicity, plotting, sounds, ratios, differences, and closed-form evaluation remain explicit run outcomes or observers.
- T34 can yield the same last-term stream as rows (a) or (c), and T43 can yield the same values as a logistic recurrence, without making their native states, events, programs, or traces equal.

## Big Picture Objective

Reconstruct fixed-dependency recursive sequences as an exact append construction. Pin down indexed prefix state, fresh seeds and verified checkpoints, a closed recurrence algebra, old-prefix dependency reads, one-term append results, the ninth update law, deterministic outcomes, equality and serialization, compact trace storage, lag-window quotients, canonical figure oracles, related nonlinear examples, neighboring construction boundaries, and the smallest honest Goal 2 integration.

## Catalog Identity

- Stable ID: T37.
- Exact name: Recursive Sequences.
- CSV provenance: `ref/notes/CA-Types.csv:38`; taxonomy provenance: `ref/notes/CA-Types.md:1022-1048`.
- Canonical strict main range: `BOOK:1555-1567`; clean chapter split `Systems-Based-on-Numbers.md:159-171`.
- Strict Page-128 Notes range: `BOOK:12688-12718`; the full printed Notes heading continues through Ulam at `12844`, while Page-129/T38 computation Notes begin at `12720` and T39 Notes at `12846`.
- Entry kind: deterministic append-only construction over a consecutive indexed exact numeric prefix.
- Strict profile: affine linear recurrence over statically known positive lags.
- Named Notes extension: closed nonlinear/index-coefficient arithmetic over the same fixed positive lag footprint, exemplified by factorial.
- Relations rather than strict profiles: logistic recurrence/T43, multivariate Ackermann recursion, global-history Ulam candidate search, characteristic/closed-form solvers, generating functions, memoized evaluators, sounds, time-series models, and finite modular AR2/generalized-Fibonacci RNGs.
- Vocabulary: recursive sequence, recurrence/recursion relation, fixed lag/distance/offset, previous/earlier term, initial condition/term, `f[n]`, Fibonacci, Lucas, Perrin, factorial, Ackermann, logistic, linear recurrence, characteristic equation/root, generating function, difference equation, history/memoization, sequence/prefix/term, and all neighboring routes dispositioned below.

## Search Log

1. Verified CSV line 38, read taxonomy section 37 in full, and used it only to seed search vocabulary.
2. Read the canonical Chapter 4 scope around `BOOK:1555-1619`, the clean chapter duplicate, the page-143 raster at original resolution, native Notes from `12688` through the Page-129 boundary, related Fibonacci Notes, the actual Index, and relevant chapter/back-matter splits.
3. Confirmed that the semantic T37/T38 split is content-based: `BOOK:1569-1575` introduces `f[n-f[n-1]]` and possibly meaningless `f[0]`/negative references. No second heading marks the split.
4. Independently decoded the six rule labels, seeds, signs, cell counts, and endpoints from `_page_143_Figure_6.jpeg` (`1231x382`, SHA-256 `731de2a621d5b227026c1b1ac4ed488ce96afc26be0fd5fcb0495297f5ed650b`). The Markdown has no textual transcription of the formulas, so the raster is primary evidence.
5. Read `BOOK:12690` and the official Wolfram Note. Both attach row (f)'s equation `t^n=-t^(n-1)+t^(n-2)` to case (e), while the clean figure and exact term rows prove the label is wrong. Recorded an explicit erratum and a characteristic-polynomial guard.
6. Followed the Page-128 factorial/logistic/Ackermann material, the official Chapter 4 CDF, Fibonacci/Lucas/Perrin facts, generating functions, time-series and sound relations, history, actual Index routes, and every cross-reference discovered there.
7. The CDF confirms factorial terms `1!..10!` and a logistic exact-integer orbit for declared rational parameters, but contains no hidden generator for the six strict raster rows. Ackermann is multivariate nested recursion, not a one-dimensional fixed-lag prefix preset.
8. Verified that the history paragraph at `BOOK:12767` discusses the later variable-index figure labels: its Conway/Hofstadter cases cannot be the strict powers-of-two/period-six rows. It belongs to T38/history rather than T37 strict mechanics.
9. Read all relevant `simple_programs.md`, `src/ca`, and tests. The document says memory belongs in current state, while current AR2/history code contradictorily addresses trajectory slices and hides seed history. Classified each responsibility below.
10. Independent exact Python generation checked all six figure prefixes, factorial/Lucas/Perrin fixtures, append/trace cardinalities, characteristic mappings, overflow anchors, and compact-window counterexamples.
11. The direct union `Recursive Sequences?|Recurrence Relations?|Linear Recurrences?|Recursive Definitions?|Fixed Distance Back` found **48 occurrences/42 lines**: `27/22` before the actual Index and `21/20` inside it. Components were recursive sequence `23/22`, recurrence relation `16/13`, linear recurrence `9/9`, recursive definition `3/3`, and fixed distance back `2/2`. Every line was classified.
12. The literal fixed-lag regex `f[n-k]` for positive decimal `k` found **23/13**, all pre-Index. The focused mechanics union found **32/20**, all pre-Index. The literal program token `f[n_{-}]` found **20/20**, all pre-Index. Each strict, T38, relation, or false-positive occurrence is routed here.
13. The alias/control union for arithmetic/recursion/recurrence/sequence/difference equations found **10/10** (`3/3` pre-Index, `7/7` Index); only `Recursion relations, 128` is a T37 alias. Named saturation over Fibonacci/factorial/Ackermann/Ulam/Perrin/Lucas/logistic found **160/118** (`98/74` pre, `62/44` Index) and every construction-relevant named route is dispositioned.
14. The 22 pre-Index direct-union lines split into strict main `1555,1567`; T38 boundary `1569,1575`; history/CA relations `11517,11570`; Fibonacci support `12138,12167,12187,12190,12192`; Notes `12688,12690,12692,12698,12726,12767`; and other relations `14021,16058,17518,17533,17585`. The 20 Index lines are individually routed under E16. Zero unresolved candidates remain.

Representative commands used `rg -n -i` over the monolith for the vocabulary unions, Perl occurrence counters with the actual-Index split at line `20826`, `sed` for every context, `rg --files` for splits/assets, original-resolution image inspection, SHA-256 verification, and exact `python3` integer recurrence generation. The nominal `BACK-MATTER/Index/Index.md` is a Notes duplicate; the actual OCR-interleaved Index is in the monolith and `BACK-MATTER/Colophon/Colophon.md:3383+`.

## Book Excerpts

`BOOK` below means `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`. The groups distinguish native fixed-lag mechanics from T38, nonlinear relations, evaluators, and observers.

### E01 — Indexed prefix and one-next-term rule

- Provenance: `BOOK:1555-1559`, Chapter 4 `Recursive Sequences`.
- Fact: the source names the first two values `f[1]` and `f[2]`, calls the nth value `f[n]`, and defines a rule for getting the next number from previous numbers. Indices identify persistent sequence terms rather than rollout-time scalar slots.

### E02 — Fixed positive lags

- Provenance: `BOOK:1561`.
- Fact: the simplest rules use `f[n-1]`; other rules also use `f[n-2]` and still earlier terms. These are fixed distances behind the target index and directly justify positive literal lag reads.

### E03 — Six strict linear rows

- Provenance: `BOOK:1563-1567`; `_page_143_Figure_6.jpeg`.
- Fact: the figure supplies all six exact rules, seeds, term rows, signs, and finite display horizons. The caption identifies (c) as powers of two and (d) as Fibonacci and says these rules admit power-based explicit descriptions. Ellipses show continuation rather than halt.

### E04 — Data-dependent references begin T38

- Provenance: `BOOK:1569-1575`; `_page_144_Figure_3.jpeg`.
- Fact: complexity begins when the rule looks a non-fixed distance back, for example `f[n-f[n-1]]`; nonpositive computed indices can be meaningless. This establishes the strict T37 exclusion and the T38 runtime-invalid-reference obligation.

### E05 — Linear recurrence Notes and source erratum

- Provenance: `BOOK:12688-12690`, Notes to page 128.
- Fact: all page-128 figure rules are linear recurrences, and explicit nth-term formulas can be obtained through a characteristic algebraic equation. The stated equation is mathematically row (f)'s `r^2+r-1=0`, despite being mislabeled case (e). The clean figure and regenerated terms control the repair.

### E06 — Factorial is a fixed-lag nonlinear extension

- Provenance: `BOOK:12692-12696`.
- Fact: factorial is named as a standard nonlinear recursive sequence with `f[1]=1` and `f[n]=n f[n-1]`. It reads a fixed lag and the target index, so a closed `TargetIndex * Lag(1)` extension covers it without computed term addressing.

### E07 — Logistic recurrence is also an iterated map

- Provenance: `BOOK:12698-12702`.
- Fact: `f[0]=x; f[n]=a f[n-1](1-f[n-1])` is explicitly identified with the iterated-map construction discussed on page 920. A prefix interpretation and T43 scalar-map interpretation can share value streams while retaining different states.

### E08 — Ackermann is not the strict prefix profile

- Provenance: `BOOK:12704-12718`.
- Fact: Ackermann definitions use multiple arguments, nested calls, and recursion whose call addresses are not a fixed positive lag in a single sequence. They establish a broad recursive-function relation, not permission for arbitrary callbacks in T37.

### E09 — Memoization and invalid evaluation order belong to T38

- Provenance: `BOOK:12720-12726`, Notes to page 129.
- Fact: the Notes store previously computed `f[n]` values to avoid recomputation for data-dependent recurrences and discuss how evaluation order changes whether invalid references are demanded. T37's static lags and complete seed coverage avoid this runtime ambiguity.

### E10 — Fibonacci exact recurrence and alternate evaluators

- Provenance: `BOOK:12138-12169`.
- Fact: Fibonacci is explicitly `f[n]=f[n-1]+f[n-2]`, `f[1]=f[2]=1`, with exact initial terms and multiple closed, matrix, generating-function, and fast-evaluation forms. Those forms are analyzers/evaluators and do not alter append-event traces.

### E11 — Same program, different seed; noncontiguous lags

- Provenance: `BOOK:12187-12192`.
- Fact: Lucas uses the Fibonacci recurrence with seeds `1,3`, while Perrin uses `f[n]=f[n-2]+f[n-3]` and origin-zero seeds `3,0,2`. Seeds and origins are separate from program identity, and lags need not be contiguous even though seed coverage is.

### E12 — Generating functions are derived descriptions

- Provenance: `BOOK:17780` and the Fibonacci formulas at `BOOK:12146-12163`.
- Fact: coefficient extraction from `1/(1-t-t^2)`, matrix powers, algebraic roots, and bit-based fast algorithms recover Fibonacci terms. They are exact random-access relations, not native state or a license to skip requested append events.

### E13 — Time-series recurrences add stochastic modeling policy

- Provenance: `BOOK:17585`.
- Fact: linear recurrence models for time series often add random noise and estimate parameters from observations. Noise distributions, inference, and fitted coefficients are separate stochastic/modeling constructions, not strict deterministic T37 semantics.

### E14 — Sounds and plots are observers

- Provenance: `BOOK:17518` and actual Index route `Recursive sequences ... sounds from, 1080`.
- Fact: variable-index page-130 sequences can be rendered as sounds. Sonification, plots, finite row width, typography, and display ellipses consume a term stream and never select the next term.

### E15 — History paragraph is scoped to later variable-index examples

- Provenance: `BOOK:12767`.
- Fact: the cited Conway sequence (c) and Hofstadter sequence (e) are the complex later-page cases, not strict row (c) powers of two or strict row (e)'s six-cycle. The paragraph remains T38/history evidence and does not change T37's fixed-lag program.

### E16 — Actual Index routes preserve the split

- Provenance: actual Index at `BOOK:21172,21185,21461,21915,21923`.
- Fact: routes include Fibonacci as a recursive sequence, factorial as a recursive sequence, linear and general recurrence relations, and recursive sequences on pages 128-131. These routes led to all included material but do not merge the page-128 fixed-lag and pages-129..131 data-dependent constructions.

The 20 direct-union Index lines route as follows: algebraic/linear recurrence analysis (`20850`), Fibonacci and factorial (`21172,21185,21461`), head entries/aliases (`21915,21923`), T38 history/evaluation/dependency/randomness (`21050,21090,21114,21162,21193,21253,21329,21683,21899`), T43 (`21360`), general induction/recursive-function theory (`21275,21793,22340`), and an inverse/program relation (`21074`). Multi-column OCR adjacency is never treated as semantic context.

### E17 — Ulam is a global-history append relation

- Provenance: `BOOK:12840-12844`, final material under the broad Recursive Sequences Notes heading.
- Fact: starting from `(1,2)`, Ulam appends the smallest integer with a unique representation as a sum of two distinct previous terms. It is genuinely append-only, but its rule searches candidates and queries an unbounded set of prior pairs rather than fixed term offsets. It is deferred as a T37-append/T39-filter composition candidate; it does not widen the strict recurrence read to an arbitrary callback.

### E18 — Finite generalized-Fibonacci generators are explicit variants

- Provenance: `BOOK:15049-15053` and finite-field/LFSR history `BOOK:11517`.
- Fact: fixed-lag generalized Fibonacci generators operate modulo `2^k` and can be realized as shift registers. The lag structure is related, but modulus, finite state, seed convention, periods, and RNG interpretation are semantic parameters absent from the strict exact-integer profile.

### E19 — Other linear-recurrence occurrences are derived or external

- Provenance: `BOOK:14021,16058,17533,17585`.
- Fact: number-based multiway systems are “somewhat related”; CA analyses and substitution spectra can obey derived linear recurrences; time-series models add noise. None changes native deterministic prefix append semantics.

## Construction Model

### State and support

For exact numeric domain `D`, define

```text
NumericPrefix(D, o, (v_0, ..., v_(m-1)))
```

where `m>0`, every `v_i` is canonical in `D`, and tuple position `i` denotes the stable term index `o+i`. The support is the consecutive integer interval `[o,o+m-1]`; it grows only at its high endpoint. There is no spatial boundary, fill value, control state, cursor, hidden clock, or mutable program.

Prefix equality includes the domain tag, absolute origin, length, and every ordered exact term. Two equal last-lag windows or equal newest values do not make prefixes equal. The complete run configuration also includes the immutable program; two configurations may share a state value while having different future behavior.

### Strict recurrence program

```text
AffineFixedLag(
    domain=D,
    bias=b,
    coefficients=((k_1,c_1), ..., (k_q,c_q))
)
```

means

```text
f[n] = b + sum(c_i * f[n-k_i] for i=1..q).
```

Validation and normalization require:

1. `D` has the exact addition/multiplication operations used; initial support is arbitrary-precision signed integers and reduced rationals.
2. `b` and all `c_i` are canonical members of `D`; booleans and floats are not exact integers/rationals.
3. Each lag `k_i` is a positive literal integer, entries are sorted by increasing lag, and duplicate entries are rejected at the serialized boundary.
4. Zero coefficients are removed canonically, and at least one nonzero coefficient remains.
5. Program identity is the normalized domain, bias, and ordered sparse coefficient map—not a rule number, callback identity, closed-form equivalence class, or characteristic polynomial alone.

The dependency footprint is exactly the coefficient keys; `L=max(k_i)` is the recurrence order/required fresh-seed length. Noncontiguous maps such as `{2:1,3:1}` are valid.

### Named Notes expression extension

After strict affine conformance, the same prefix/read/append machinery may admit:

```text
FixedLagArithmeticExpr =
    Literal(value)
  | TargetIndex
  | Lag(positive_literal)
  | Neg(expr)
  | Add(nonempty_exprs)
  | Sub(left, right)
  | Mul(nonempty_exprs)
```

The dependency footprint is the set of literal `Lag(k)` nodes, and at least one lag is required. `TargetIndex` is injected exactly into `D`. This closed algebra covers factorial and can express the logistic recurrence under an exact rational profile. It deliberately excludes conditionals, comparisons, division, powers, modulus, absolute indices, term-value-computed indices, general function calls, evaluator strings, lambdas, and host arithmetic objects.

Expression identity is structural after literal/domain normalization and documented associative-node normalization; it is not quotient by symbolic algebra. Logistic's prefix program remains distinct from T43's scalar-map program.

### Seed and checkpoint

For a fresh run, `SequenceSeed(origin,terms)` contains exactly `L=max_lag` contiguous terms. This makes the first recurrence target unambiguous and prevents surplus initial values from silently postponing the recurrence.

A longer `VerifiedSequenceCheckpoint(program,origin,terms)` is a different input type. Construction verifies every term after the first `L` by replaying the program from the minimal seed. Only then can the terminal prefix resume. A checkpoint is neither a new seed definition nor a trusted cache blob.

The main six presets use origin `1`; Perrin uses origin `0`. Origin is always state-visible and becomes behavior-visible when an expression reads `TargetIndex`.

### Source, reads, and result

Each old snapshot has exactly one firing source:

```text
NextSequenceTerm(snapshot_id, target_index=o+len(terms))
```

`FixedLagRead` returns a canonical lag-keyed tuple of `TermRef(index=n-k,value=old[n-k])` for every required lag. All references are to the old prefix; no newborn/current/future term is readable. The expression extension additionally receives the exact target index.

The rule returns:

```text
AppendTerm(source, dependency_refs, exact_value)
```

Dependency references are provenance and validation witnesses as well as inputs. Reusing one lag multiple times in an expression reads the same old occurrence; it does not create multiple mutable terms.

### Ninth update law

`AppendOnlySequenceUpdate(old,result)` validates the snapshot/source, exact target index, complete dependency footprint, old values, result domain, and one-result cardinality. It then returns

```text
NumericPrefix(D, o, old.terms ++ (result.value,)).
```

Every old index/value is preserved exactly, exactly one fresh endpoint is created, and the commit is atomic. It is not T34 assignment because no old term is overwritten; not T16 splice because no nonempty match is consumed; and not T17 queue update because no prefix is deleted. A private persistent-vector endpoint-insert kernel may be shared without merging the public laws.

### Successors, invalidity, and outcomes

For a validated exact run, every event has exactly one `Advanced` successor. Structural change is always true because length increases, even when the appended value equals another term. There is no intrinsic halt, quiescent state, fixed-point stop, cycle stop, magnitude threshold, overflow, or display-width boundary.

Program/seed/checkpoint errors are pre-execution validation failures. Strict T37 has no runtime invalid-index policy: there is no default, zero padding, wrap, clamp, skip, or halt-on-missing behavior to choose.

Operational outcomes are `RequestedAppendsCompleted`, `Cancelled`, `ResourceExhausted`, and `BackendFailure`. Interruption retains the last fully appended prefix and event log; a partial append is impossible.

### Trace and compact encoding

For fresh seed length `L` and requested append count `h`:

```text
states       = S_0, ..., S_h        # h+1 semantic prefixes
len(S_j)     = L+j
events       = e_0, ..., e_(h-1)    # h append events
term stream  = seed ++ event values # L+h terms
```

The figure displays the last line of the term-stream projection, not all `S_j`. A lossless compact trace stores the normalized program, seed or verified checkpoint, ordered append events, and outcome once. `state_at(j)` reconstructs the appropriate prefix. This representation is linear in emitted terms instead of naively duplicating nested prefixes quadratically.

Trace equality includes program, initial input kind/data, ordered values and dependency witnesses, exact event count, and outcome. Term-stream equality, state-stream equality, origin-shift equivalence, and rendered equality are separate observers.

### Lag-window quotient

For `L=max_lag`, define

```text
Q_L(prefix) = (next_absolute_index, last_L_terms).
```

When every reference is a fixed positive lag at most `L`, arithmetic is deterministic, and the exact domain/program are retained, `Q_L` commutes with one append. If `TargetIndex` is absent, the next index may be irrelevant to value evaluation but remains required to recover typed addresses.

This quotient is future-sufficient and useful as an evaluator cache. It is lossy: prefixes `(1,1,2)` and `(9,1,2)` have the same last-two window and different state/history. A bare window cannot serialize a canonical prefix, answer arbitrary past-term queries, or reproduce the trace. The complete append log restores those abilities; a finite-domain window cycle still is not a growing-prefix cycle.

### Exact values and serialization

Reuse T34's tagged exact integers/reduced rationals and decimal-string components. Domain tags participate in equality. Index origins, lags, append counts, and large term indices also serialize without unsafe JSON-number assumptions.

Canonical decoding rejects duplicate lags, malformed signs/decimal strings, zero rational denominators, booleans, floats, mixed domains, unknown AST nodes, and hidden precision/modulus fields. A normalized program/prefix round trip is byte-stable at the canonical data level.

### Observers and analyzers

Indexed term tables, final prefixes, last terms, differences, ratios with explicit zero policy, residues, signs, digit views, numeric/log plots, periodicity, growth, sonification, dependency DAGs, characteristic polynomials, generating functions, and closed/random-access formulas are downstream.

Characteristic-root or matrix algorithms may evaluate a requested term efficiently. They cannot change an `h`-event trace into one event, invent skipped dependency provenance, or replace exact arithmetic with approximate roots. Memoization and rolling windows are evaluator strategies, not hidden semantic state.

## Exact Book Presets and Oracles

All six use exact integers and origin `1`. Displayed counts include the seed terms.

| Case | `bias`; lag coefficients | Fresh seed | Exact displayed prefix | Display endpoint |
|---|---|---|---|---|
| (a) | `1`; `{1:1}` | `(1)` | `1..38` | `f[38]=38` |
| (b) | `1`; `{1:-1}` | `(1)` | `(1,0)` repeated 24 times | `f[48]=0` |
| (c) | `0`; `{1:2}` | `(1)` | `1,2,4,...,2097152` (22 terms) | `f[22]=2^21` |
| (d) | `0`; `{1:1,2:1}` | `(1,1)` | standard Fibonacci `F_1..F_26` | `f[26]=121393` |
| (e) | `0`; `{1:1,2:-1}` | `(1,1)` | seven copies of `(1,1,0,-1,-1,0)`, then `(1,1)` | `f[44]=1` |
| (f) | `0`; `{1:-1,2:1}` | `(1,1)` | `1,1,0,1,-1,2,-3,...,28657,-46368` (27 terms) | `f[27]=-46368` |

The complete nontrivial finite rows are:

```text
(c) 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048,
    4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288,
    1048576, 2097152

(d) 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610,
    987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368,
    75025, 121393

(f) 1, 1, 0, 1, -1, 2, -3, 5, -8, 13, -21, 34, -55, 89, -144,
    233, -377, 610, -987, 1597, -2584, 4181, -6765, 10946,
    -17711, 28657, -46368
```

Closed descriptions and characteristic guards are:

- (a) `f[n]=n`; the affine constant produces a polynomial-times-`1^n` form rather than a literal sum of distinct exponentials.
- (b) `f[n]=(1-(-1)^n)/2` after shifting by its fixed point.
- (c) `f[n]=2^(n-1)`, characteristic root `2`.
- (d) `f[n]=F_n`, characteristic `r^2-r-1`.
- (e) `f[n]=2/sqrt(3) sin(n*pi/3)`, characteristic `r^2-r+1`; exact period six.
- (f) for `n>=3`, `f[n]=(-1)^n F_(n-3)`, characteristic `r^2+r-1`.

The Notes' stated equation is the final polynomial above and must be attached to (f), not (e). The caption's general “sum of powers” statement needs repeated-root/polynomial qualification for (a), and “purely repetitive” describes (f)'s sign fluctuation rather than its growing magnitude.

Additional exact conformance fixtures:

1. Fibonacci `f[93]=12200160415121876738`, beyond signed 64-bit.
2. Lucas reuses `{1:1,2:1}` with origin-1 seed `(1,3)`, giving `1,3,4,7,11,18,...`.
3. Perrin uses origin `0`, map `{2:1,3:1}`, seed `(3,0,2)`, giving `3,0,2,3,2,5,5,7,10,...`.
4. Factorial expression `Mul(TargetIndex,Lag(1))`, origin-1 seed `(1)`, gives `1,2,6,24,120,720,5040,40320,362880,3628800` through index 10.
5. The Notes/CDF logistic relation with `f[0]=3`, `a=1/2` gives generated terms `-3,-6,-21,-231,-26796,-359026206,-64449908476890321` through index 7.
6. `h=0` yields one seed-prefix state, zero events, and exactly the seed term stream; general `h` yields the cardinalities stated above.
7. Row (e) repeats values every six terms but every event remains structurally `Advanced`.
8. Rows (a)/(c) agree in newest-value projection with corresponding T34 programs while typed states/programs/events remain unequal.
9. Two prefixes with the same last-`L` window but different discarded terms prove the window projection is non-injective.
10. A verified longer checkpoint reproduces the same resumed trace as replay from its minimal fresh seed; a malformed checkpoint is rejected.

## Variants, Relations, and Boundaries

### Native profiles and principled closure

- The six page-143 affine integer programs are the strict evidenced core.
- Other exact integer/rational biases, coefficients, origins, and seeds are a principled closure when the declared domain is closed and fresh-seed coverage is exact.
- Noncontiguous positive lags are native, as Perrin demonstrates.
- `FixedLagArithmeticExpr` is a named same-executor Notes extension for index-dependent coefficients and nonlinear arithmetic over fixed literal lags. Factorial is its canonical fixture.
- A residue-ring/modular affine recurrence is an explicit domain variant. It may reuse fixed-lag dependency structure, but modulus and finite equality/periods are never implicit performance options.
- Certified exact-real or declared finite-precision profiles require their own domain/equality context. Nothing in the strict figure justifies host-float defaults.

### Relations and excluded recursive forms

Logistic notation can be interpreted as a prefix recurrence or an iterated scalar map. The source explicitly supplies the latter relation. T37 and T43 may expose a checked term-stream projection without identifying state or event traces.

Ackermann and primitive/general recursive functions concern nested multiargument function evaluation and computability. They do not widen `FixedLagArithmeticExpr` into a universal evaluator.

Ulam is a genuine growing sequence but computes the next term by searching candidates against all pairs in the complete prefix. Its read is neither a fixed lag nor a value-computed single index. It is recorded as a future composition question: reuse T37's prefix/append law with whatever constructive filtering/global-history read T39 evidence establishes. T37 does not hide that search in a formula node, and T39 must reopen this boundary if its evidence does not compose.

Characteristic equations, generating functions, matrix powers, memoization, shift-register realizations, closed forms, and fast Fibonacci algorithms are analyzers, evaluator strategies, or compilers. Sonification, plots, ratios, periods, prime divisibility, and time-series fitting are observers or external models.

### Catalog and construction boundaries

| Related type/construction | Shared part | Required separation |
|---|---|---|
| T13 parallel substitution | ordered persistent values and lineage ideas | every old symbol is replaced in parallel; no numeric fixed-lag append source |
| T16 sequential substitution | private persistent-vector mechanics may implement an endpoint edit | one nonempty program match is consumed/replaced and no-match can terminate |
| T17 tag systems | an old suffix may persist and new values appear at the tail | a positive prefix is consumed; queue prefix tables and insufficient-prefix termination differ |
| T19 register machines | exact integer values and program/value separation | finite named bank, control address, instruction branches, and assignment effects |
| T30 multiway systems | exact structured traces and provenance | set-valued branch layers and exact child merge, not one deterministic numeric append |
| T34 arithmetic iteration | exact scalar domains; rows (a)/(c) share newest-value streams | T34 overwrites one scalar and has no retained indexed prefix/dependency references |
| T35 piecewise integer maps | exact scalar arithmetic | predicate-selected arms over one scalar, not fixed-lag prefix reads |
| T36 digit-reversal arithmetic | exact integer terms and digit observers | representation base/digit transformation feeds back into one scalar update |
| T38 variable-index recursion | exact prefix, append result/update, term references | dependency addresses are computed from term values and can be invalid at runtime |
| T39 numeric filtering | ordered candidate streams and possible Ulam composition | native filtering/sieving policy must be evidenced; it is not a fixed-lag recurrence |
| T40 constant digits | indexed exact output stream | digit-production/approximation semantics, not recurrence state by default |
| T41 function combination | formulas and numeric samples | function/curve is native object; samples are observations |
| T43 iterated maps | logistic can produce the same newest values | one scalar is iterated; prefix history is a trace, not native map state |
| Linear feedback/RNG | fixed lag arithmetic can be shared | finite residue ring, shift register, stochastic-use metadata, and period observers are explicit |
| Closed-form solver | exact requested terms | random access cannot replace or fabricate requested append events |

## Current API Fit

| Responsibility | Current mechanism | Fit for T37 |
|---|---|---|
| Semantic state | `simple_programs.md:87-113` persistent dense trajectory field | `SEMANTIC MISMATCH`; T37 needs one growing indexed prefix as each Markov state, not scalar cells across stored rollout time |
| Address/domain | canonical `[t,x,y,z]`, including `t+0D` | `PARAMETERIZATION` only for a downstream term-stream view; rollout time and term index must not be conflated |
| Values | finite alphabets, bounded integers/floats | `SEMANTIC MISMATCH`; strict rows require arbitrary signed exact integers and overflow-free growth |
| Source/frontier | writable next-time coordinates and `time_slice` | `PRINCIPLED EXTENSION`; add the sole logical source `NextSequenceTerm` at the prefix endpoint |
| Reads | ordered relative spatial/temporal offsets | `PARAMETERIZATION` at the responsibility level; fixed lag order is useful, but reads must address terms in current prefix state, never stored trajectory slices |
| Rule | exhaustive/aggregate/formulaic rules and finite rule IDs | `SEMANTIC MISMATCH`; add normalized `AffineFixedLag` and closed Notes AST, with no callback/rule-number encoding |
| Result | bare next scalar for current formulaic families | `PRINCIPLED EXTENSION`; add `AppendTerm` with target/dependency witnesses and exact value |
| Update | fixed-support assignment/copy-forward | `SEMANTIC MISMATCH`; add the ninth `AppendOnlySequenceUpdate` law |
| Seed | scalar site, pair/history, and selector-rendered values | `SEMANTIC MISMATCH`; add exact contiguous fresh seed and verified-checkpoint input types |
| Boundary | fixed/periodic/reflective spatial policies | `NOT APPLICABLE`; missing dependencies are invalid configuration, not a boundary policy |
| Episode | rectangular `RawEpisode(states: ndarray,rule_id,steps)` | `SEMANTIC MISMATCH`; it lacks nested prefix/event semantics, exact big values, origins, structural program identity, and append counts |
| Memory convention | `simple_programs.md:386-392,703-731` says memory belongs in current state | `DIRECT` principle-level support for visible prefix state; current negative-temporal code violates it |
| Visualization | t+0D scalar rows/plots | usable only as downstream term-stream observers after typed exact export |
| Exact values | T34's planned domain-tagged integer/rational codecs | `DIRECT` design reuse; T37 adds prefix/index/program/update, not another numeric tower |

The documented source/read/rule/update responsibilities remain useful. The dense next-slice schema and unrestricted `FORMULAIC` escape hatch do not implement the construction.

## Current Runtime Fit

- `src/ca/neighborhoods.py:524-543` preserves ordered temporal components, and `:617-636` defines a current/previous AR2 read. These offsets address trajectory times, not stable indices in current prefix state, so only the idea of ordered lag roles is reusable.
- `src/ca/rules.py:336-365` computes `next=(a*x[t]+b*x[t-1]+constant) mod modulus`, decodes `a,b` from a finite rule ID, and fixes a coefficient grid. This is a finite modular two-lag relation, not the strict exact program.
- `src/ca/rules.py:316-328` exposes an unrestricted `formulaic(fn)`. A callable can conceal computed indices, branches, state packing, or an entire alternate engine and is rejected.
- `src/ca/rollout.py:145-213` dispatches on family names instead of executing typed source/read/result/update contracts.
- `src/ca/rollout.py:334-356` coerces to `np.int64`, interprets `(x[-1],x[0])` as hidden history, omits the first seed term from output, and emits `steps` scalar samples. It neither preserves the full seed nor returns prefix states/events.
- `src/ca/rollout.py:542-573` repeats the fixed-width/modular assumptions in batch form.
- `src/ca/seeds.py:136-179` provides only two-value finite-integer pair/uniform-pair recipes and leaves placement to a hidden temporal convention.
- `src/ca/specs.py:23-81` couples `Dynamics`, `RawEpisode`, and `RawBatch` to dense NumPy arrays and numeric rule IDs.
- `tests/test_rollout.py:68-97` makes the mismatch executable: seed `[1,2]`, rule ID `0`, and `steps=4` returns `[2,3,4,5]`. A T37 two-term seed plus four append events must preserve six total terms and five prefix snapshots.
- `tests/test_neighborhoods.py:42-66` proves current negative-time components are preserved, not that the history is visible in state. `tests/test_rules.py:7-12` proves a declared pool of 256 current rules, not arbitrary structural recurrence programs.
- Binary `dyadlags_0d` and count-banded `lagcounts_0d` are finite lookup constructions. Their history length, alphabets, and rule tables do not cover exact affine numeric recurrences.
- Current visualization/export rejects object/rational states or coerces to bounded integer storage. Existing scalar arrays can be a lossy/typed term-stream export only after exact values and metadata are preserved elsewhere.

Goal 2 may migrate current AR2 into an explicit residue-ring `AffineFixedLag` variant after decoding its coefficients and retaining its whole seed. It must not reuse the hidden-history rollout as the reference T37 executor or add `if family == "recursive"`.

## Principles Audit

### Principle 0 — re-derive the state

The catalog taxonomy suggested whole history, while a conventional recurrence evaluator needs only a lag window. Primary evidence exposes stable indexed prior terms and a growing sequence but does not dictate storage layout. Canonical prefix plus a proved lag-window transition quotient preserves both meanings without pretending the quotient is invertible.

### Principles 1–4 — preserve a distinct construction and result

Equal scalar streams do not collapse T37 into T34/T43. The source is a new endpoint, the read names earlier term occurrences, the result is `AppendTerm`, and commit appends without consumption. A typed ninth update law is smaller and more honest than weakening assignment/splice/queue contracts.

### Principles 5–8 — visible history and natural growth

All data required to advance is in the prefix or an explicit proved quotient. There is no executor-local prior term, negative trajectory lookup, padded capacity, scalar packing, or object-cell history. Term indices are semantic addresses, while rollout-frame coordinates and tensor layouts remain representations.

### Principles 9–10 — strict coupling and ordinary presets

Program lag footprint and seed arity are coupled and validated together. The six named rows are ordinary affine programs plus seeds/horizons for conformance, not alternate executor branches or rule IDs.

### Principles 11–12 — evaluators and views stay downstream

Rolling windows, memoization, characteristic roots, matrix powers, generating functions, plots, sound, padding, and batching do not redefine the append event. Compact trace encoding remains lossless and inspectable.

### Principles 13–16 — adversarial fidelity

Rows (e)/(f), origin-zero Perrin, factorial, machine-width Fibonacci, repeated values, malformed checkpoints, and the non-injective lag window exercise the abstraction. The source erratum is guarded rather than copied. A closed AST and typed update are architecture; a formula callback, family switch, or hidden AR2 seed is a shim.

### Re-integration answers

1. T37 invalidates the assumption that a numeric term stream stored across rollout time is automatically the semantic state; the full prefix is state and the stream is a projection.
2. T34 exact scalar domains, generic source/read/result/update orchestration, ordered-support persistence internals, outcomes, and trace responsibilities are reusable without changing their meanings.
3. The proposal adds no flag, callback, compatibility fallback, or hidden state. It adds one public result/update pair and one named closed expression extension.
4. Prefix state contains everything needed to advance and reproduce history; a lag window alone does not and is labeled a quotient/cache.
5. Consecutive support, exact values, absent control, append semantics, and representation remain separate.
6. Fixed-lag dependency and append are defining. Characteristic solvers, memoization, rolling windows, and closed forms are incidental algorithms.
7. ANKoS encodings must retain origin, all terms/events, exact value tags, and nested-prefix reconstruction. A `[t,0,0,0]` scalar stream is only a declared projection.
8. No completed stage is contradicted or reopened. T34's T37 boundary is confirmed; T16/T17 public updates remain unchanged.
9. Goal 2 gains exact numeric prefixes, fixed-lag reads, append effects/update, compact prefix traces, and a future T38 reuse point. T39 must audit whether Ulam composes with filtering.
10. The API is simpler because strict affine data is normalized and recurrence history is no longer split between seeds, trajectory storage, and family-specific rollout locals.

## Detailed Implementation Plan

1. Complete direct-name, fixed-lag, named, Notes, actual-Index, split, program, history, alias, and relation searches.
2. Decode all six raster rows and independently verify horizons, values, signs, endpoints, characteristic mappings, and source errata.
3. Derive `NumericPrefix`, strict affine data, the closed Notes extension, fresh-seed/checkpoint validation, and fixed-lag reads.
4. Specify `AppendTerm`, the ninth update law, exact outcomes, equality, serialization, compact traces, and lag-window quotient proof obligations.
5. Audit variants/observers/boundaries and current API/runtime/tests.
6. Write the Goal 2 work package and adversarial suite; integrate global ledgers and verify the repository.

## Goal 2 Implementation Stage

### Stage A — exact indexed prefix values

1. Reuse the T34 exact integer/rational domain and JSON-safe scalar codecs in a shared value module.
2. Add `SequenceIndex`, `NumericPrefix`, consecutive-support validation, exact prefix equality/hash, and canonical serialization.
3. Add exact fresh `SequenceSeed` and replay-checked `VerifiedSequenceCheckpoint`; reject surplus fresh seeds and trusted opaque checkpoints.

### Stage B — closed recurrence programs

4. Add normalized `AffineFixedLagProgram(domain,bias,coefficients)`, dependency-footprint calculation, exact evaluator, and page-143/Lucas/Perrin presets.
5. After strict conformance passes, add the named `FixedLagArithmeticExpr` extension with only the evidenced nodes and factorial preset.
6. Reject callables, strings, computed/absolute term indices, branches, unapproved operators, mixed domains, duplicate/nonpositive lags, implicit modulus, and rule-ID coefficient encodings.

Suggested responsibility files are a shared exact-value module, `numeric_sequences.py`, `recurrences.py`, optional `recurrence_expressions.py`, generic source/read/result/update modules, and numeric observers. Exact paths should follow the Goal 2 synthesis package layout rather than creating a T37 family subtree.

### Stage C — source/read/result/update execution

7. Add `NextSequenceTerm`, `FixedLagRead`, stable `TermRef`, and typed `AppendTerm` to the generic transition protocol.
8. Add `AppendOnlySequenceUpdate` as the ninth validated sibling law. A private endpoint-insert kernel may be shared, while T16/T17 validators remain intact.
9. Execute through typed component dispatch, never a rule-family branch. Retain current Phase-1 behavior during migration through honest specifications, not fallbacks.

### Stage D — outcomes and traces

10. Add `append_count` with exact `h/h+1/L+h` event/state/term cardinalities and explicit completion/cancel/resource/backend outcomes.
11. Add compact seed/checkpoint-plus-events traces with `state_at(j)` reconstruction, dependency provenance, and last-complete-prefix interruption semantics.
12. Add the optional lag-window evaluator only behind a checked commuting-law interface; never serialize it as the canonical prefix without the full log.

### Stage E — observers, variants, and conformance

13. Add indexed-term/final-prefix, difference, ratio, residue, sign, digit, growth, plot, characteristic, generating-function, and exact random-access observer interfaces as independently typed layers.
14. Express current modular AR2 later as an explicit residue-domain affine recurrence if migration is required; preserve decoded coefficients, complete seed, and its distinct term-stream compatibility view.
15. Implement `tests/test_t37_recursive_sequences.py` with the six exact figure rows/horizons, erratum guards, Fibonacci overflow, Lucas/Perrin/factorial, checkpoint, window, trace, outcome, serialization, and negative-boundary tests below.
16. Add static guards proving the new path does not call current formulaic/AR2 family rollout, use `np.int64`/object arrays, or read negative trajectory time.

### Goal 2 completion evidence

- Every exact preset round-trips structurally and reproduces its independently generated terms.
- Every append preserves all old terms and adds exactly one indexed value from complete old-prefix witnesses.
- Fresh seeds/checkpoints, origins, lags, domains, event counts, and outcomes pass property/adversarial tests.
- Compact and materialized traces are observationally identical; a bare lag window is proven non-injective.
- T34/T38/T39/T43 boundaries and current AR2 migration are explicit with no family branch or hidden compatibility behavior.

## No-Cheating Checks

- No unrestricted callback, evaluator string, symbolic host expression, pickle, or family-name rollout dispatch.
- No scalar, byte string, Python object cell, digit row, fixed tensor, or rule ID packing the whole prefix/program.
- No `np.int64`/`uint64` overflow, saturation, implicit wrap, or hidden modulus in the exact profile.
- No float conversion, tolerance equality, platform numeric context, or unsafe JSON numeric big integer.
- No temporal trajectory read or hidden `(x[-1],x[0])` seed convention; every dependency is a visible old-prefix `TermRef`.
- No lag zero, negative lag, current/future term, absolute term reference, term-value-computed lag, implicit `f[0]`, padding, clamp, wrap, or default.
- No insufficient/empty fresh seed and no extra fresh seed terms that silently delay recurrence start.
- No trusted longer prefix; checkpoint suffixes are replay-verified before resumption.
- No newborn term read in its own event and no more or fewer than one append result.
- No mutation, deletion, reindexing, deduplication, or overwrite of any old term.
- No public reuse of T34 assignment, T16 nonempty splice, or T17 consume/append that weakens their validators.
- No collapsing equal-valued occurrences; index makes every appended occurrence distinct even in rows (b)/(e).
- No fixed-point/cycle/repetition/magnitude/digit-width stop in native execution.
- No finite display horizon or ellipsis interpreted as a semantic halt.
- No confusion of the figure's one final term row with the nested rollout state trace.
- No lag window called canonical state or lossless serialization without the complete seed/checkpoint and append log.
- No memoization table, characteristic root, matrix state, generating function, or closed form fed back as native prefix state.
- No fast evaluator skipping requested events or inventing dependency witnesses.
- No approximate characteristic-root calculation used to generate exact integer presets.
- No source erratum copied into the (e)/(f) program mapping.
- No caption claim strengthened beyond the exact mathematics; affine repeated-root and growing-amplitude qualifications remain visible.
- No T34 scalar iteration, T43 scalar logistic map, T38 computed index, T39 filter, Ulam search, Ackermann recursion, or RNG modulus hidden as a T37 mode flag.
- No Ulam/global-history rule smuggled into the fixed-lag AST; its future composition boundary remains explicit.
- No modulo/finite-field AR2 presented as exact unbounded integer recurrence.
- No object-array export or rectangular padding presented as exact prefix state.
- No duplicate T37-only exact-number, trace, outcome, persistent-vector, or executor infrastructure where shared components already suffice.
- No weakening of current tests or canonical book oracles to accommodate implementation constraints.

## Completion Requirements

- [x] Every strict main-text, raster, Notes, actual Index, split, program, history, alias, named variant, observer, and relation candidate is dispositioned.
- [x] Prefix/index/domain, strict and extended program, seed/checkpoint, dependency, append, outcome, equality, serialization, trace, and quotient semantics are explicit.
- [x] Every strict figure row and high-value variant has independently checked exact oracles and adversarial boundaries.
- [x] The source erratum and overbroad caption claims are repaired transparently and guarded.
- [x] T34/T38/T39/T43, Ulam, Ackermann, modular RNG, solver, and observer boundaries are explicit.
- [x] Current API/runtime fit and a no-family-branch Goal 2 handoff are implementation-ready.
- [x] Design ledger, evidence index, global plan, diff checks, and repository tests are integrated.

## Stage Results

T37 is complete. The direct union found 48 occurrences on 42 lines, fixed-lag tokens 23/13, focused mechanics 32/20, literal recurrence programs 20/20, alias/control forms 10/10, and named saturation 160/118. Nineteen excerpt groups disposition the strict main/raster, full recursive-sequence Notes cluster, actual Index/splits, programs/history, fixed/nonlinear/modular/global-history variants, analyzers, observers, and neighboring constructions. Strict mechanics have zero unresolved search candidates.

The reconstruction is a consecutive domain-tagged exact `NumericPrefix` plus a normalized `AffineFixedLag` program. Minimal fresh seeds and replay-verified checkpoints make recurrence start unambiguous. `NextSequenceTerm -> FixedLagRead -> AppendTerm -> AppendOnlySequenceUpdate` preserves every old indexed term and adds exactly one endpoint, establishing the ninth update law. The factorial-capable expression extension is closed; runtime invalid indices, callbacks, fixed widths, modulus, and hidden trajectory history stay out of the strict profile.

Exact Python oracles regenerated all six raster rows at horizons `38/48/22/26/44/27`, their endpoints, `Fibonacci[93]`, Lucas, Perrin, factorial, the exact logistic relation, append/state/term cardinalities, checkpoint replay, lag-window non-injectivity/commutation, and the raster SHA-256. They passed. Markdown fences are balanced, `git diff --check -- goal-1` passed, and `uv run pytest -q` passed all 102 tests in 1.17 seconds.

## Integration Results

`design-ledger.md` now records the T37 construction, the ninth update member, D070-D075, numeric-prefix inventory changes, rejected shortcuts, Ulam's open composition question, and the completed integration entry. `evidence-index.md` records T37 complete and 14/45 completed types. `0-plan.md` records the implementation-ready result and T39 as next.

T34 exact scalar values and shared orchestration/outcomes/traces are reused without changing meaning. T16/T17 public edit laws remain distinct. T38 can reuse prefix/append while adding computed-index reads and runtime reference outcomes; T39 must audit Ulam composition. Current AR2 remains an explicit modular migration relation. No prior stage is contradicted or reopened.
