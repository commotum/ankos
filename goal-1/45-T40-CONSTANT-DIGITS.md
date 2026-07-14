# 45-T40-CONSTANT-DIGITS

Status: **IN PROGRESS — ARCHITECTURE RESOLVED; ORACLE AND HOSTILE-REVIEW CLOSURE PENDING**

## Current Facts

- T40 is CSV physical line 41, `Mathematical-Constant Digit Systems`; `ref/notes/CA-Types.md` section 40 supplies search vocabulary, not primary mechanics.
- The canonical main section is `BOOK:1665-1832`. T39 ends at `BOOK:1663`; T41 begins at `BOOK:1834`. Native Notes are `BOOK:12921-13144`; T41 Notes begin at `BOOK:13146`.
- The clean Chapter 4 split at lines 247-291 is materially abridged. It omits the page-154 long-division and page-156 square-root procedures and assets, so it cannot replace the monolith for semantic closure.
- The Book distinguishes a simple exact definition of a number from its positional digits, the procedure used to compute them, and downstream walks/statistics/randomness claims (`BOOK:1667-1687`, `1796-1832`). These are different semantic roles even when one implementation calculates all of them together.
- Positional representation is parameterized by a base and a normalization convention. A terminating rational has an infinite trailing-zero expansion under the strict source convention; suppressing those zeros is rendering, not native completion (`BOOK:1689-1707`).
- The source gives an explicit base-2 long-division procedure with visible remainder `r`: compare `2r` with `q`, emit a digit, and replace `r` by `2r` or `2r-q` (`BOOK:1709-1715`). This is an ordinary exact `t+0D` SimpleProgram realization, not the identity of the rational number or of T40 as a whole.
- The source gives an explicit square-root procedure over visible product state `(r,s)` (`BOOK:1738-1746`). Both components are read from one old snapshot and assigned atomically. The coefficient prefix alone is not complete work state.
- Positional digits and simple continued fractions are different representations of the same exact value. Continued-fraction coefficients are unbounded; rational continued fractions complete after finitely many terms, whereas irrational ones continue (`BOOK:1776-1794`, `13030-13038`).
- A simple continued fraction has signed integer `a0=floor(x)` and positive tail coefficients. The page-903 relation is stated for any irrational `h`; page 162's positive ratios do not justify a globally nonnegative coefficient schema (`BOOK:12587-12589`).
- The Notes explicitly describe direct nth-digit methods that need not generate preceding digits (`BOOK:12943-12958`). Therefore a T37-style append trace is one possible evaluator realization, not T40's universal native state or event.
- Exact, certified, approximate, probable, unknown, unsupported, and resource-limited coefficient results must remain distinct. The direct-digit example is described only as overwhelmingly probable under finite precision; it is not silently exact.
- Digit rows, walks, histograms, term-size plots, rational approximants, regularity, randomness, and normality claims are observers. Finite data do not prove randomness or normality, and normality depends on the base (`BOOK:12972-12976`).
- T40 adds no new execution algebra. Its semantic umbrella is an immutable exact denotation plus a pure representation query/result. Any explicit generation algorithm is a separately identified SimpleProgram using the already shared DOMAIN/ALPHABET/FRONTIER/NEIGHBORHOOD/RULE/UPDATE axes.

## Source Defect That Must Remain Visible

The Notes claim that the printed square-root rule works for every rational `1 <= n < 4` (`BOOK:12982`). The literal main rule branches on `r>s` and writes `4(r-s-1)` in the true arm. This is safe for integer `r,s`, where `r>s` implies `r>=s+1`, but it is false for arbitrary rationals. For `n=11/5`:

```text
(11/5,0) -> (24/5,4) -> (-4/5,12)
```

The algebraic identity still propagates, but the nonnegative-remainder and approximation-bound invariants are lost on the second event. A rational extension can instead test `r>=s+1`, but that is a repaired sibling and must not be attributed silently to the printed `r>s` rule. Strict source conformance therefore qualifies the literal work machine to its integer-safe profile and records the broader Notes claim as falsified.

## Updated Assumptions

- **Retained:** an exact constant or closed arity-zero expression is immutable denotation data. It is not a mutable scalar configuration merely because an evaluator performs repeated work.
- **Retained:** representation, base, sign/radix convention, rational canonicalization, requested coefficient indices, evaluator identity, resources, and rendering occupy separate typed roles.
- **Retained:** a finite prefix is a query result and is necessarily lossy as a representation of an arbitrary exact real. Many distinct values share the same positional or continued-fraction prefix.
- **Retained:** structural definition identity, certified denotational equality, representation equality, equal queried prefixes, and equal rendered pixels are different relations.
- **Retained:** a coefficient evaluator may expose explicit work state and a SimpleProgram trace, but it must be connected to the query by a replayable realization/certification relation. Work state never becomes the constant's identity.
- **Retained:** unsupported exact evaluation returns a typed query result. A named constant does not authorize a host CAS callback, machine float, hidden lazy evaluator, or invented coefficients.
- **Rejected:** a `ConstantDigitsState`, T40 FRONTIER, T40 NEIGHBORHOOD, T40 UPDATE, constant executor, family branch, fake no-op evolution, mandatory prefix append, opaque CAS object, hidden remainder, object-array packing, or observer-fed evolution.

## Big Picture Objective

Reconstruct T40 as exact mathematical denotations with explicit positional and simple-continued-fraction representation queries, while treating the Book's long-division, square-root, positional-tail, continued-fraction, and direct-digit methods as separately identified evaluator realizations. Exhaustively close main text, Notes, actual Index, split ownership, assets, algorithms, canonicalization, exactness/certification, work-state invariants, observers, T34/T36/T37/T41/T42/T43 boundaries, current runtime fit, and the Goal 2 handoff. Add a semantic component only where a concrete counterexample defeats the smallest reusable construction.

## Catalog Identity

- Stable ID: T40.
- Exact CSV name: Mathematical-Constant Digit Systems.
- CSV physical line: 41.
- Taxonomy section: 40.
- Canonical main core: `BOOK:1665-1832`.
- Native Notes core: `BOOK:12921-13144`.
- Entry kind: immutable exact numeric denotation plus typed representation query; explicit generation procedures are optional work SimplePrograms.
- Native transition DOMAIN: not applicable to the denotation/query. Iterative realizations shown here use discrete `t+0D` work configurations.

## Final Semantic Model

The declarative layer is:

```text
ExactDenotation =
    ClosedArityZeroExpression
    x ExactValueSchema
    x PrimitiveRegistryVersion
    x DefinitionProvenance

Representation =
    Positional(base >= 2,
               sign_and_radix_convention,
               canonical_terminating_zero_tail)
  | SimpleContinuedFraction(canonical_finite_tail)

ExpansionQuery =
    ExactDenotationRef
    x Representation
    x (Prefix(count) | CoefficientAt(index))
    x EvaluationContext

ExpansionResult =
    ExactCoefficients
  | CertifiedCoefficients
  | ApproximateOrProbableCoefficients
  | FiniteCompletion
  | Unsupported | Unknown | ResourceLimit | Failure
```

`EvaluationContext` identifies the method/realization, numeric backend, precision or enclosure policy, resource budget, and certificate requirements. It does not enter the exact denotation's identity. The requested index/count belongs to query identity and horizon, not configuration, control, or the constant.

For positional representations, the canonical convention chooses the expansion that is not eventually all `base-1`; terminating rationals therefore continue with zeros. Thus `0.5000...`, not `0.4999...`, is canonical in base 10. A renderer may suppress the trailing zeros without changing the representation denotation.

For finite simple continued fractions, require the final coefficient to exceed one whenever the representation has more than one term. This chooses one side of

```text
[a0,...,a_n] = [a0,...,a_(n-1), a_n-1, 1]  when a_n > 1.
```

The leading simple-continued-fraction coefficient is a signed integer; only coefficients after `a0` must be positive. This matters at the T42 seam: the page-903 Notes construction is stated for any irrational `h`, uses `a0=floor(h)` only as an output offset, and derives its substitution schedule from the positive tail. Page 162's positive ratios are a restriction, not the generic coefficient schema.

The exact value and its full canonical representation are connected losslessly at the denotational level when the required exact expansion exists. A finite queried prefix is never claimed to be a lossless encoding of the value.

## Explicit Work SimplePrograms and Commuting Relations

### Positional residual map

For `0 <= f < 1` and base `b >= 2`, one ordinary T43-style unary map event is

```text
d  = floor(b f)
f' = b f - d
```

The digit `d` is a replayable event/query witness. With canonical expansion `e_b`, `e_b(f') = tail(e_b(f))`. This is a named restriction of the existing exact scalar-map machinery, not a T40 state or executor. A numerical implementation that cannot certify `floor(bf)` returns a typed query failure and commits no asserted exact digit.

### Rational long division

For fixed `q>0`, `b>=2`, and `0<=r<q`:

```text
d  = floor(b r / q)
r' = b r - d q
```

The invariant is `0<=d<b`, `0<=r'<q`, and `br=dq+r'`. Under `phi_q(r)=r/q`, `phi_q(r')` is exactly the positional residual map. The source's base-2 procedure is this preset with `d in {0,1}`. The native work event is therefore:

```text
active = UniqueScalar.select(remainder)
reads  = Self.read(remainder, active)
writes = ClosedLongDivisionRule(b,q).apply(active, reads)
next   = AtomicAssign.apply(remainder, active, writes)
```

The digit belongs to the event witness/result stream; the complete work configuration is the exact remainder plus immutable program data. No hidden prefix or remainder is permitted.

### Square-root digit procedure

For the strict integer-safe source profile:

```text
configuration = Product(r,s)
active        = UniqueScalar.select(configuration)
reads         = Self.read(configuration, active)
writes        = if r>s
                  then Assign(active, Product(4(r-s-1), 2(s+2)))
                  else Assign(active, Product(4r,        2s))
next          = AtomicAssign.apply(configuration, active, writes)
```

Both product factors are assigned atomically from one old snapshot. With initial snapshot `(n,0)` numbered `t=0`, the strict work invariant is

```text
s_t^2 + 4 r_t = 4^(t+1) n
s_t <= 2^(t+1) sqrt(n) < s_t + 4.
```

For integer-safe runs, `s` is divisible by four. Writing `a=s/4` and `beta=[r>s]` gives `a'=2a+beta`, so each event exposes one more binary digit while retaining the residual needed for future events. Erasing `r` is lossy: reachable states `(5,4)` from seed `9/4` and `(4,4)` from seed `2` have the same `s`/prefix but successors with `s'=12` and `s'=8`. Consequently neither a bare prefix nor `s` alone is complete work state.

### Simple continued-fraction residual map

For exact `y`, emit `a=floor(y)`. If `y-a` is nonzero, write

```text
y' = 1 / (y-a).
```

This is a T43 unary-map realization of the continued-fraction query. If `y` is an exact integer, the query emits the final coefficient and returns `FiniteCompletion`; it does not invent another term or mislabel exact completion as a pole. A raw partial-map request may retain its ordinary undefined reciprocal outcome, but the expansion query has the stronger representation context needed to classify the boundary correctly.

### Direct coefficient evaluation

A certified random-access evaluator implements `CoefficientAt(index)` without fabricating preceding append events. Approximate or probabilistic algorithms retain that proof strength. If a caller explicitly requests a prefix-generation trace, a sequential evaluator may be chosen, but equality of final coefficients does not authorize invented events for a direct evaluator.

## First-Principles Architecture Matrix

| Responsibility | Class | Smallest reusable construction | T40 disposition |
|---|---:|---|---|
| Exact constant/expression | 1 | T41 closed exact expression/definition responsibilities plus T34 exact values | Arity-zero denotation with explicit primitive registry/provenance |
| Representation query/result | 2 | Generic T31/T41 scoped query/result/certificate envelope | Add positional/continued-fraction query schemas, coefficient carriers, completion, and canonicalization |
| Full representation relation | 3 | Lossless tagged representation relation where defined | Explicit base/convention and inverse; never promote a finite prefix to lossless value state |
| Positional codecs | 1/2 | T36 exact positional codecs | Query use only; T36's feedback RULE state is not imported |
| Positional residual iteration | 2 | T43 exact unary self-map preset | Visible residual state and certified digit witness |
| Rational long division | 2/3 | T34/T35/T43 exact scalar unary event | Fixed `(b,q)`, exact remainder invariant, ordinary assignment/update |
| Square-root procedure | 3 | Product ALPHABET plus T35/T43 closed piecewise tuple map | Atomic `(r,s)` assignment and guarded source profile; no T40 UPDATE |
| Continued-fraction iteration | 2 | T43 fractional-reciprocal map preset | Exact integer-tail completion belongs to query context |
| Direct nth coefficient | 2 | Pure evaluator query | No fabricated prefix history or hidden callback |
| Digit/coefficient prefix | 2 | Typed finite query result | Not T37 canonical state; finite prefix is lossy |
| Walks/statistics/randomness | 1/2 | Observer/analyzer records | Never feed evaluation or strengthen empirical claims |
| New execution algebra | Not established | Existing declarative category plus branch-free SimpleProgram runner for realizations | No T40 state/frontier/neighborhood/update/executor/family branch |

This is not an exception to the SimpleProgram architecture. The exact iterative procedures are SimplePrograms and use the same runner. The umbrella catalog entry also names an immutable denotation/query relation, just as T41 contains uniterated function definitions without inventing argument-as-time evolution. That declarative boundary was already established by D082/T41, so D139 uses classes 1–3 relative to the current architecture and adds no new class-4 category or execution algebra.

## Cross-Type Boundaries

- **T34:** supplies exact scalar carriers and arithmetic. A constant definition is not a scalar being repeatedly overwritten; long division is a separately identified T34/T43-like work realization.
- **T36:** supplies positional codecs and proves that representation can be RULE-visible. T40 uses those codecs in a pure query unless an explicit residual algorithm feeds work state back.
- **T37:** its source rule semantically depends on and preserves a complete old prefix, and every append is the requested system event. T40 prefixes are query results; direct nth-digit methods and multiple incompatible evaluator states defeat a universal append identity.
- **T38:** computed prefix addresses remain recurrence RULE semantics. They are not a general mechanism for querying arbitrary constant coefficients.
- **T39:** a prime stream can be a source to a leading-digit observer; that observation neither changes the prime construction nor becomes T40 state.
- **T41:** supplies immutable closed expression and pure query/certificate responsibilities. T40 specializes arity-zero exact values and representation coefficients; it does not repeatedly evaluate a function argument.
- **T42:** consumes a replay-verified finalized T40 irrational continued-fraction prefix or an explicitly typed schedule source, separates signed `a0` from the positive tail, and owns schedule derivation, symbols, rule selection, substitution configuration, events, and trace. The strict Book construction rejects rational-complete continued fractions and does not own generic continued-fraction expansion.
- **T43:** owns explicit residual-map work configurations and feedback semantics. A Gauss/positional orbit can realize a T40 query but is not the exact constant or coefficient result itself.
- **Noncomputable exact definitions:** an exact symbolic definition alone does not imply executable coefficient access. Chaitin-type digit definitions require `Unsupported` unless a closed admitted evaluator/certificate exists.

## Current Runtime Fit

The current `src/ca` package exposes names resembling the shared axes, but its executable realization remains CA-shaped and family-dispatched. T40 therefore exercises shared migrations and declarative modules, not a `constant_digits` rollout branch.

| Responsibility | Current mechanism | Goal 2 disposition |
|---|---|---|
| Declarative definition/query | `Dynamics` requires domain, shape, rule, neighborhoods, and frontier (`specs.py:23-55`) | Reuse/generalize the T41 closed denotation and query/result modules outside rollout; do not fabricate missing transition axes |
| Values/coefficients | finite `int|float|str` alphabets; NumPy episode arrays | Add tagged exact integers/rationals/algebraics/named constants/enclosures and unbounded coefficient codecs outside fixed arrays |
| FRONTIER/NEIGHBORHOOD | only `time_slice` construction and coordinate-array access | Reuse singleton/self access only for explicit work SimplePrograms; add no T40 selector |
| RULE | six hard-coded families plus unrestricted `formulaic` callable | Add closed expression/representation/evaluator schemas; callbacks and host CAS objects are invalid semantic identity |
| UPDATE/runner | positive-step ndarray trajectories and named-family dispatch (`rollout.py:40-213`) | Realizations use the shared structural runner after Goal 2 migration; pure queries bypass rollout by category, not by a family special case |
| Rule/value identity | rule IDs normalized to signed `int64` | Use structural tagged IDs and arbitrary-precision codecs; base/representation belong to query identity, not a numeric family ID |
| Seeds | `seeds.constant` fills an integer array | Do not confuse this spatial fill preset with a mathematical constant definition |
| Viewer | rejects object/float arrays and stores at most `uint16` symbol codes | Keep unbounded CF terms, exact values, rows, walks, histograms, and crops in typed result/view encoders, not native state arrays |

## Corrected Goal 2 Handoff

- Reuse T41's immutable closed-definition, exact-value, primitive-registry, structural-identity, certified-equivalence, query/result, certificate, partiality, and evaluator-context responsibilities; add an arity-zero exact-denotation member rather than a top-level T40 class.
- Add closed `Positional(base, convention)` and `SimpleContinuedFraction(convention)` representation specifications, `Prefix` and `CoefficientAt` requests, bounded and unbounded coefficient schemas, exact finite continued-fraction completion, eventually-zero infinite positional status, and canonical round-trip rules.
- Reuse T36 positional codecs without importing T36 transition state. Keep sign, integer part, radix point, leading/trailing-zero policy, and dual-expansion normalization explicit.
- Represent unsupported/certified/approximate/probable/unknown/resource/failure outcomes without silent float or CAS fallback. A coefficient is exact only when its floor or equivalent separation is certified.
- Model long division, positional residual iteration, strict integer-safe square-root extraction, and continued-fraction residual iteration as named closed work SimplePrograms over existing singleton/product map axes. Bind each to the query by an explicit realization certificate and event-witness replay.
- Preserve evaluator work configuration, exact denotation, generated coefficients, finite queried prefix, full representation denotation, trace, and rendering as distinct records.
- Give T40 ownership of generic positional/continued-fraction expansion and coefficient queries, including signed `a0` with positive tail coefficients. The T42 seam carries the complete immutable replay-verified result, proof strength, typed irrational-prefix/finite-completion status, natural coefficient orientation, and count; strict T42 rejects rational completion, then owns schedule derivation plus substitution-side state/update/trace.
- Add no `ConstantDigitsState`, expansion FRONTIER/NEIGHBORHOOD, coefficient-append UPDATE, executor, rollout family, arbitrary callback, hidden prefix/remainder, host CAS object, float coercion, or object-array escape hatch.

## No-Cheating Checks

- No exact constant represented by an approximate float, rendered digit string, finite prefix, raster, host symbolic object, or opaque callback.
- No base, sign/radix convention, canonicalization, evaluator version, precision, or certificate context left implicit.
- No `term_count` used as state, control, capacity, native halt, or constant identity; it is a query horizon.
- No terminating positional expansion mislabeled finite when the strict representation includes trailing zeros; suppression remains rendering.
- No rational continued fraction extended after exact finite completion; no reciprocal-of-zero failure substituted for the query's normal completion.
- No unbounded continued-fraction coefficient forced through finite alphabet ranks, `uint16`, signed `int64`, or palette codes.
- No finite prefix claimed lossless, random, normal, or sufficient work state.
- No sequential prefix events fabricated for a direct nth-digit evaluator; no approximate/probable result promoted to exact.
- No square-root `(r,s)` residual hidden, no `s`/digit prefix called complete work state, and no false arbitrary-rational source claim silently accepted.
- No long-division remainder, Gauss residual, evaluator cache, precision state, or resource counter hidden outside a declared work configuration/context.
- No T40-specific state, DOMAIN, FRONTIER, NEIGHBORHOOD, RULE-result wrapper, UPDATE, executor, family branch, or identity/no-op rollout.

## Frozen Source Closure

`45-T40-source-oracle.py` freezes 18 search lanes and their 144-line union, but completeness no longer depends on those searches. A fixed strict-main universe routes every one of the 117 nonblank `BOOK:1665-1832` rows as `102 native / 15 structural`, with zero closure residual. A separately derived actual-Index universe routes all 82 relevant rows as `25 native / 56 relation / 1 control`; 37 of those rows are deliberate search-lane misses, proving that the Index closure is not defined by the regex results. The retained governed evidence totals 262 rows at `169 native / 84 relation / 9 control`. Thirty-seven semantic guards, 24 extraction/source-defect records, 32 source-model records, five exclusion hashes, and seven exact-logic contracts are independently bound. The complete split disposition has 359 rows at `214 exact / 22 image-basename / 20 normalized / 14 summary / 89 omitted`, normalized minimum `0.999817`, with zero unresolved. Its audit digest is `a06531ed8bfcaf4a926ad4db4bc6eb32b2a2e77ed3171ee5f9be9e3c145f166e`; script SHA-256 is `a344c99af98756084344fa2f1a67d17c92091697dde1e743dc1c02b9e7125f8a`.

The exact logic contract covers 2,079 long-division states, rational finite continued-fraction completion, finite-prefix loss, 96 strict square-root events, the extracted square-root bit divergence, and the `n=11/5` rational counterexample. Normal and JSON modes, silent import, compilation, relocation with the corpus, source mutation, optimized mode, malformed usage, and the source/asset interface all pass fail-closed.

## Frozen Asset Closure

`45-T40-asset-oracle.py` closes exactly 24 governed images at `11 native / 12 relation / 1 control`, 46 references at `24 monolith / 22 split`, 24 distinct physical files and hashes totaling 574,761 bytes, and four multi-file assemblies spanning 16 files. The page-154 and page-156 split-link omissions are explicit. Every asset is `HASH_BOUND`; none is pixel-replayed or used as executable program data. The structural, ordered, and normalized textual-replay digests are respectively `1cbfe8ffc3de77048a2d407c7ef63896dac86a8fc3ec83c7b00c1ea84e6f019e`, `ecf178d94b0b34226592d3b460a2a1e2f0cf6893e1521877f3ada6818898fad6`, and `6fd8578623171650e57a405f2d3e9740b895724609fceb38132ceb202055c1fa`; script SHA-256 is `e2a0cbe8277ee663c81d9bea832336251c022203233fdcb32fc225bff4097f35`.

Its independent textual replay checks 8,255 long-division states and 96 strict-integer square-root events, guards all three mismatches between the extracted square-root bit string and the exact algorithm, and retains the rational source-claim counterexample. Source guards, semantic manifests, import, compilation, relocation, optimized mode, bad usage, hash mutation, and the real source-oracle interface pass.

## Frozen Semantic Closure

`45-T40-semantic-oracle.py` independently reproduces the asset interface at 8,255 long-division states, 96 strict square-root events, and three guarded extraction mismatches. It closes nine signed and unsigned exact rational positional cases, nine canonical round trips, 225 signed-prefix cylinders, 60 certified decimal and 96 certified binary digits of pi, 30 certified pi continued-fraction coefficients, five quadratic-surd periods/400 coefficients, a 120-term exact continued fraction for `e`, and an 80-term exact negative-surd prefix. Explicit work checks cover 255 long-division events, 390 square-root commutations/780 invariant checks, and 24 Gauss-map commutations across six signed and unsigned sources. The `(5,4)` versus `(4,4)` loss witness, the surviving algebraic identity under the literal `11/5` misuse, and both failed nonnegative/enclosure obligations are executable guards.

The query audit checks 159 prefix/random-access agreements plus 36 certified random-access agreements, separate positional and continued-fraction prefix-loss cylinders, exact/certified/partial/resource outcomes at `1/1/1/2`, unsupported/unknown/approximate/probable/failure outcomes at `4/1/1/1/1`, and eight proof-nonpromotion rejections. Three strict T42 handoffs carry 32 exact and 12 certified finalized coefficients without an evaluator callback; one exercises signed `a0` with an otherwise positive irrational continued-fraction tail, while a signed rational-complete prefix is explicitly rejected without losing its typed completion status. The interface carries the complete immutable replay-verified result, so source/result identity, proof strength, source kind, orientation, and requested count cannot be replaced by opaque forged IDs. Positional sign is a separate `leading_minus_magnitude` convention/result component rather than a negative digit, and simple continued fractions admit any signed integer `a0` while rejecting nonpositive tail coefficients. Canonical terminating positional values are classified `eventually_zero_infinite`, never finite completion; genuine `finite_terminated` remains confined to rational continued fractions. The public surface contains 35 declarative/work dataclasses, three optional work-record types, zero native T40 execution roles, and zero new class-4 algebras; 62 hostile rejections close invalid carriers, forged certificates, hidden roles, floats, sign/termination mistakes, and silent source repairs. Semantic digest is `b78dc3ff77018ee1aa57585621da14ef588e94554116517917986642f09a7e50`; script SHA-256 is `69a0d6a4722c9d97e4473610ce1acd002de30263ad94f5a90b15d9df2f63610a`.

## Completion Requirements

- [ ] Every strict main, Notes, actual-Index, split, history, relation, control, exclusion, and extraction-defect candidate is dispositioned with zero unresolved mechanics.
- [ ] The complete 24-asset/46-reference universe is hash-bound with split omissions and source limitations explicit.
- [ ] Positional and continued-fraction definitions, canonicalization, coefficient queries, exactness levels, completion, work realizations, and observers are independently verified.
- [ ] Long division, square-root product state/invariant/loss witness, positional/Gauss maps, direct nth access, and finite-prefix loss are adversarially tested.
- [ ] T34/T36/T37/T39/T41/T42/T43 and current-runtime boundaries are synchronized.
- [ ] Source, asset, semantic, cross-interface, mutation, portability, fail-closed, mode, Markdown, diff, scope, repository-test, and independent hostile-review gates pass.
- [ ] D139, plan, evidence index, design ledger, architecture audit, and Goal 2 handoffs are synchronized with no new execution algebra.

## Stage Results

Pending oracle and hostile-review closure.
