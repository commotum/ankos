# 45-T40-CONSTANT-DIGITS

Status: **IN PROGRESS — ARCHITECTURE RESOLVED; ORACLE AND HOSTILE-REVIEW CLOSURE PENDING**

## Current Facts

- T40 is CSV physical line 41, `Mathematical-Constant Digit Systems`; `ref/notes/CA-Types.md` section 40 supplies search vocabulary, not primary mechanics.
- The canonical main section is `BOOK:1665-1832`. T39 ends at `BOOK:1663`; T41 begins at `BOOK:1834`. Native Notes are `BOOK:12921-13144`; T41 Notes begin at `BOOK:13146`.
- The clean Chapter 4 split at lines 247-291 is materially abridged. It omits the page-154 long-division and page-156 square-root procedures and assets, so it cannot replace the monolith for semantic closure.
- The Book distinguishes a simple exact definition of a number from its positional digits, the procedure used to compute them, and downstream walks/statistics/randomness claims (`BOOK:1667-1687`, `1796-1832`). These are different semantic roles even when one implementation calculates all of them together.
- Positional representation is parameterized by a base and a normalization convention. A terminating rational has an infinite trailing-zero expansion under the strict source convention; suppressing those zeros is rendering, not native completion (`BOOK:1689-1707`).
- The followed representation evidence includes whole/fractional positional encoders and inverses, arbitrary positive bases, Gray-code ordering, negative bases, non-power bases, multiplicative digit schemes, unary, self-delimiting length prefixes, binary-coded base 3, Fibonacci/Zeckendorf words, and their length/completeness/distribution properties (`BOOK:12503-12555`, `17130-17178`, `20507`, actual Index). Strict T40 v1 deliberately closes only positive-integer-radix positional digits and simple continued fractions. The other schemes are explicit relations or future representation-schema extensions, not proof of a new executor and not silently claimed by `Positional(base>=2)`.
- The source gives an explicit base-2 long-division procedure with visible remainder `r`: compare `2r` with `q`, emit a digit, and replace `r` by `2r` or `2r-q` (`BOOK:1709-1715`). This is an ordinary exact `t+0D` SimpleProgram realization, not the identity of the rational number or of T40 as a whole.
- The source gives an explicit square-root procedure over visible product state `(r,s)` (`BOOK:1738-1746`). Both components are read from one old snapshot and assigned atomically. This direct source representation is faithful, but not uniquely minimal: for a fixed declared radicand/profile, reachable normalized state is also losslessly represented by `s`, because phase, prefix, and `r` reconstruct from the invariant.
- Positional digits and simple continued fractions are different representations of the same exact value. Continued-fraction coefficients are unbounded; rational continued fractions complete after finitely many terms, whereas irrational ones continue (`BOOK:1776-1794`, `13030-13038`).
- A simple continued fraction has signed integer `a0=floor(x)` and positive tail coefficients. The page-903 relation is stated for any irrational `h`; page 162's positive ratios do not justify a globally nonnegative coefficient schema (`BOOK:12587-12589`).
- The Notes explicitly describe direct nth-digit methods that need not generate preceding digits (`BOOK:12943-12958`). Therefore a T37-style append trace is one possible evaluator realization, not T40's universal native state or event.
- Exact, certified, approximate, probable, unknown, unsupported, and resource-limited coefficient results must remain distinct. The direct-digit example is described only as overwhelmingly probable under finite precision; it is not silently exact.
- Digit rows, walks, histograms, term-size plots, rational approximants, regularity, randomness, and normality claims are observers. Finite data do not prove randomness or normality, and normality depends on the base (`BOOK:12972-12976`).
- T40 adds no new execution algebra. Its semantic umbrella is an immutable exact denotation plus a pure representation query/result. Any explicit generation algorithm is a separately identified SimpleProgram using the already shared DOMAIN/ALPHABET/FRONTIER/NEIGHBORHOOD/RULE/UPDATE axes.
- In this audit, DOMAIN retains the project meaning of dimensional task/program space (`t+0D`, `t+1D`, and so on), whether discrete or continuous. It is not renamed to mean support or topology: the declarative T40 query has no transition DOMAIN, while each iterative coefficient realization shown here is discrete `t+0D`.

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

## Search Log

The frozen source audit records the exact regex text, line set, digest, partition, and misses for twenty bounded discovery lanes. Their 213-row union is useful recall evidence, but it is not the completeness boundary:

- `Q00` tests the external catalog label and deliberately finds no Book occurrence.
- `Q01-Q06` cover mathematical constants, displayed digit histories, rational repetition/long division, the `(r,s)` square-root procedure, other algebraic/transcendental digit profiles, and positional/continued-fraction representations.
- `Q07-Q08` cover direct nth-digit methods, exactness qualifications, randomness tests, normality, and named constructive normal numbers.
- `Q09-Q13` follow nested/concatenated/leading-digit relations, continued fractions, Euclidean and Gauss-map algorithms, Egyptian-fraction/nested-radical/digital-slope relations, substitution seams, noncomputable definitions, compression, resource bounds, and CA relations.
- `Q14` searches actual-Index vocabulary and page routes; `Q15-Q16` cover all 63 governed-or-excluded image names; `Q17` guards the T39/T41 section boundaries.
- `Q18` follows positional implementation/inversion, representation history, Gray-code, negative-base, non-power-base, multiplicative-digit, and alternative-notation relations; `Q19` independently catches reversed/plural Index aliases such as `60 (base)`, negative bases, unary, and Zeckendorf representation.

Search recall is not used as the completeness proof. Four independent closure mechanisms are routed:

1. every 117 nonblank row in the strict main section `BOOK:1665-1832`;
2. every 126 nonblank row in native Notes `BOOK:12921-13144`, plus the complete `BOOK:12587-12595` T40↔T42 seam and every followed relation/control continuation;
3. every 897 nonblank physical row in the actual flattened Index block `BOOK:20828-22456`, ending before the Colophon at `BOOK:22458`;
4. an independently defined Book-wide digit/base/representation/continued-fraction/computability/randomness/resource lane with 309 direct vocabulary matches (`242 pre-Index / 67 Index`), each retained or assigned to one of ten line-hash-bound sibling-exclusion groups.

Every row is classified as native, relation, control, structural, exclusion, or unrelated. The independently reproduced Index vocabulary, hostile page/alias/continuation set, and Book-wide lane must all be subsets of those explicit dispositions. This prevents regex misses, flattened-column wrapping, and cherry-picked cross-references from disappearing. The nominal Chapter 4 split is reverse-joined against the monolith, including its page-154/page-156 omissions. Retained captions govern their rasters; invoked pages and physical asset pages are recorded separately. Name collisions, unrelated representation prose, generic algorithm references, and adjacency-only material remain explicit exclusions rather than silent misses. The final frozen counts and digests appear under **Frozen Source Closure**; completion requires zero residual in every universe.

## Book Excerpts

These grouped passages are the construction-bearing core. The source oracle retains and guards the complete surrounding rows, tables, captions, Notes, Index routes, continuations, and exclusions.

### Excerpt 1 — definition, representation, and terminating-zero convention

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:1673-1689`
- Context: Chapter 4, **Mathematical Constants**.
- Establishes: a simple exact definition is not its digit sequence; base is representation data; a terminating rational still has an infinite canonical zero tail.

> One might suppose that at some level it must be quite simple and regular. For the value of π is specified by the simple definition of being the ratio of the circumference of any circle to its diameter.
>
> But it turns out that even though this definition is simple, the digit sequence of π is not simple at all.
>
> There are some numbers whose digit sequences effectively have limited length. Thus, for example, the digit sequence of 3/8 in base 10 is 0.375. (Strictly, the digit sequence is 0.3750000000..., but the 0's do not affect the value of the number, so are normally suppressed.)

### Excerpt 2 — exact long-division work state

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:1707-1715`
- Context: Chapter 4 rational-digit construction and page-154 caption.
- Establishes: the emitted digit and visible remainder transition are one exact scalar work SimpleProgram.

> The method is essentially standard long division, although it is somewhat simpler in base 2 than in the usual case of base 10. The idea is to have a number r which essentially keeps track of the remainder at each step in the division. One starts by setting r equal to p. Then at each step, one compares the values of 2r and q. If 2r is less than q, the digit generated at that step is 0, and r is replaced by 2r. Otherwise, r is replaced by 2r - q. With this procedure, the value of r is always less than q.

### Excerpt 3 — square-root product transition

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:1738-1746`
- Context: Chapter 4 procedure and page-156 caption.
- Establishes: the literal source uses simultaneous visible `(r,s)` updates; it supplies a faithful direct product representation, not proof that every lossless implementation must store both factors.

> It involves two numbers r and s, which are initially set to be n and 0, respectively. At each step it compares the values of r and s, and if r is larger than s it replaces r and s by 4(r-s-1) and 2(s+2) respectively; otherwise it replaces them just by 4r and 2s.
>
> To find √n one starts by setting r=n and s=0. Then at each step one applies the rule `{r,s} -> If{r>s, {4(r-s-1), 2(s+2)}, {4r,2s}}`.

### Excerpt 4 — positional and continued-fraction representations

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:1776-1798`
- Context: Chapter 4 representation discussion.
- Establishes: representation is a construction procedure; rational continued fractions are finite, irrational ones infinite; symbolic definition and evaluation effort remain distinct.

> Any representation for a number can in a sense be thought of as specifying a procedure for constructing that number.
>
> A common example are so-called continued fraction representations, in which the operations of addition and division are used.
>
> In the case of rational numbers, the results are always of limited length. But for other numbers, they go on forever.
>
> At some level, one can always use symbolic expressions like √2 + e^√3 to represent numbers. And almost by definition, numbers that can be obtained by simple mathematical operations will correspond to simple such expressions. But the problem is that there is no telling how difficult it may be to compute the actual value of a number from the symbolic expression that is used to represent it.

### Excerpt 5 — direct access and proof strength

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:12943-12958`
- Context: Notes for page 137, **Computing nth digits directly**.
- Establishes: prefix generation is not T40's universal state/trace, and finite-precision agreement is probable rather than exact.

> Most methods for computing mathematical constants progressively generate each additional digit. But ... it is sometimes possible to generate, at least with overwhelming probability, the nth digit without explicitly finding previous ones.
>
> Note that with finite-precision arithmetic, some exponentially small probability exists that truncation of numbers will lead to incorrect results.

### Excerpt 6 — empirical claims and the square-root source defect

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:12972-12982`
- Context: Notes for pages 139 and 141.
- Establishes: finite randomness/normality evidence has bounded proof strength; the Notes state the invariant and the overbroad rational claim that the executable counterexample below falsifies.

> Empirical evidence for the randomness of the digit sequences of √n, π, etc. ... is based on applying various standard statistical tests of randomness, and remains somewhat haphazard.
>
> Note that the fact that a number is normal in one base does not imply anything about its normality in another base.
>
> The basic idea is at every step t to maintain the relation s² + 4r = 4^t n, keeping r as small as possible so as to make s ≤ 2^t √n < s + 4. Note that the method works not only for integers, but for any rational number n for which 1 ≤ n < 4.

### Excerpt 7 — finalized continued fractions feed T42

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:12587-12595`
- Context: Notes for page 122, **Relation to substitution systems**.
- Establishes: strict T42 accepts irrational `h`, reverses the positive continued-fraction tail once to form a finite schedule, applies substitutions from seed `{0}`, and uses `Floor[h]` only as an output offset.

> The first m rules ... are obtained for any h that is not a rational number from the continued fraction form of h by `Reverse[Rest[ContinuedFraction[h,m]]]`.
>
> Given these rules, the original sequence is given by `Floor[h] + Fold[Flatten[#1 /. #2] &, {0}, rules]`.

### Excerpt 8 — an exact definition need not be computable as digits

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:17101`
- Context: Notes on algorithmic randomness and Chaitin's Ω.
- Establishes: formal exact denotation does not authorize an executable coefficient callback.

> Even though one can never expect to construct them explicitly, one can still give formal descriptions of sequences that are algorithmically random. An example due to Gregory Chaitin is the digits of the fraction Ω of initial conditions for which a universal system halts.

### Excerpt 9 — positional inversion and non-positional representation boundaries

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:12503-12555`, `17130-17178`, `20507`
- Context: Notes for pages 116–117 and the later discussion of mathematical notation.
- Establishes: ordinary positive-radix digits have explicit forward/residual/inverse procedures, while negative-base, non-power-base, multiplicative, unary, Gray-code, and Zeckendorf schemes are genuinely different representation schemas. They widen representation data and validation where adopted; they do not by themselves require another transition runner.

> For a number x between 0 and 1, the first m digits in its digit sequence in base k are given by RealDigits[x, k, m] or Floor[k NestList[Mod[k#, 1] &, x, m-1]].
>
> Given a suitable list of digits from 0 to k-1 one can obtain any positive or negative number using From Digits[list, -k].
>
> - **Non-power bases.** One can consider representing numbers by  $Sum[a[n]f[n], \{n, 0, \infty\}]$  where the f[n] need not be  $k^n$ .
>
> (c) Length prefixed. Starting with an ordinary base 2 digit sequence, one prepends a unary specification of its length, then a specification of that length specification, and so on:
>
> (e) *Fibonacci encoding*. Instead of decomposing a number into a sum of powers of an integer base, one decomposes it into a sum of Fibonacci numbers (see page 902). This decomposition becomes unique when one requires that no pair of 1's appear together.
>
> If one successively reads 0's and 1's from an infinite sequence then the representations (c), (d) and (e) have the property that eventually one will always accumulate a valid representation for some number or another.
>
> But as pages 560 and 916 show, there are many other quite different ways to represent numbers, each with different levels of convenience for different purposes.

### Excerpt 10 — representation schemas are chosen for downstream access

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:6766-6782`
- Context: Chapter 10, page 560–561 run-length encoding discussion followed from the page-1201 representation route.
- Establishes: unary, ordinary binary, length-prefixed, binary-coded-ternary, and Fibonacci encodings are distinct finite schemas; self-delimitation is a representation invariant needed by a consumer, not a reason to invent another execution algebra.

> Various representations of numbers from 1 to 30. (a) is unary ... (b) is ordinary binary or base 2 representation. (c), (d) and (e) are set up to be self-delimiting, so that the end of a number can be recognized purely by looking at the cells within it.
>
> Indeed, any digit sequence can be thought of as providing a short representation for a number. But for run-length encoding it turns out that ordinary base 2 digit sequences do not quite work. For if the numbers corresponding to the lengths of successive runs are given one after another then there is no way to tell where the digits of one number end and the next begin.

### Excerpt 11 — exact real definitions, computation, and oracle boundaries

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:19066-19087`
- Context: Notes for page 729, **Computable reals**, **Diagonal arguments**, **Continuous computation**, and **Initial conditions**.
- Establishes: nth-coefficient computability is a finite-step property, not a consequence of exact denotation; continuous carriers do not erase finite program description or discrete choices; arbitrary real initial data can hide an oracle unless its construction is supplied.

> The stated purpose of Alan Turing's original 1936 paper on computation was to introduce the notion of computable real numbers, whose nth digit for any n could be found by a Turing machine in a finite number of steps. ... the overwhelming majority of all possible real numbers are not computable.
>
> Most of the types of programs that I have discussed in this book can be generalized to allow continuous data ... But the programs themselves normally remain discrete, typically involving discrete choices made at discrete steps.
>
> Traditional mathematics tends to assume that real numbers with absolutely any digit sequence can be set up. And if this were the case, then the digits of an initial condition could for example be the table for an oracle ... any reasonably complete theory must address how such an initial condition could have been constructed.

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

`Positional(base>=2)` is the strict v1 positive-integer-radix schema. It does not pretend that base 1, negative radix, mixed/non-power weights, Gray-code order, multiplicative prime-exponent words, or Zeckendorf words are parameters of that exact codec. Those followed relations would require their own closed representation tags, inverse/normalization rules, and ambiguity invariants, while continuing to use pure queries or ordinary existing work-program axes as appropriate.

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

For integer-safe runs, `s` is divisible by four. Writing `a=s/4` and `beta=[r>s]` gives `a'=2a+beta`, so each event exposes one more binary digit. The direct `(r,s)` product is source-faithful. On reachable normalized states of one fixed declared program, however, the smaller representation `(n,profile,s)` is lossless:

```text
t = 0                              if s = 0
t = bit_length(s/4)                otherwise
r = (4^(t+1)n - s^2) / 4
bits = base2(s/4) at width t.
```

The oracle proves this inverse and one-step commutation for all 390 audited states. The states `(5,4)` for `n=9/4` and `(4,4)` for `n=2` still prove that bare `s` without immutable program identity is lossy, but they do not prove that `r` is necessary within a fixed program. Thus product state and the invariant-valid quotient are alternative transparent representations; neither licenses a universal T40 prefix state for direct nth-digit or unrelated evaluator methods.

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
| Alternative number representations | 2/3 | Generic closed representation/query envelope | Gray-code ordering is a relation/observer; unary, negative-radix, non-power, multiplicative, and Zeckendorf schemes require separately tagged codecs and canonicalization before support, not a T40 executor |
| Positional residual iteration | 2 | T43 exact unary self-map preset | Visible residual state and certified digit witness |
| Rational long division | 2/3 | T34/T35/T43 exact scalar unary event | Fixed `(b,q)`, exact remainder invariant, ordinary assignment/update |
| Square-root procedure | 3 | Product ALPHABET plus T35/T43 closed piecewise tuple map | Atomic direct-source `(r,s)` assignment; lossless reachable `(n,profile,s)` quotient with explicit inverse; guarded source profile; no T40 UPDATE |
| Continued-fraction iteration | 2 | T43 fractional-reciprocal map preset | Exact integer-tail completion belongs to query context |
| Direct nth coefficient | 2 | Pure evaluator query | No fabricated prefix history or hidden callback |
| Digit/coefficient prefix | 2 | Typed finite query result | Not T37 canonical state; finite prefix is lossy |
| Walks/statistics/randomness | 1/2 | Observer/analyzer records | Never feed evaluation or strengthen empirical claims |
| New execution algebra | Not established | Existing declarative category plus branch-free SimpleProgram runner for realizations | No T40 state/frontier/neighborhood/update/executor/family branch |

This is not an exception to the SimpleProgram architecture. The exact iterative procedures are SimplePrograms and use the same runner. The umbrella catalog entry also names an immutable denotation/query relation, just as T41 contains uniterated function definitions without inventing argument-as-time evolution. That declarative boundary was already established by D082/T41, so D139 uses classes 1–3 relative to the current architecture and adds no new class-4 category or execution algebra.

## Principles Audit

- **Principles 0–1 — re-derive and preserve the construction.** T40 is not assumed to be a digit-append automaton merely because its figures show successive prefixes. The source separates exact denotation, representation, an optional computation procedure, queried coefficients, and observers. Explicit long-division, square-root, positional-residual, and continued-fraction procedures remain ordinary SimplePrograms; the immutable denotation/query layer is the already established declarative category (`principles.md:3-13`).
- **Principles 2–4 — closed visible responsibilities.** Every iterative realization uses the shared `FRONTIER.select -> NEIGHBORHOOD.read -> RULE -> UPDATE.apply` protocol with visible scalar or product work state and atomic assignment. Representation schemas, evaluator identity, proof strength, completion, and event witnesses are typed data. No host CAS callback, hidden remainder, fabricated prefix history, or T40 family switch supplies semantics (`principles.md:15-45`).
- **Principles 5–7 — state, invariants, and intrinsic coupling.** Exact denotation, immutable program data, work configuration, coefficient result, and rendering are kept distinct. Long division couples `(base, denominator)` to the remainder invariant; the strict square-root preset couples its declared radicand/profile to either direct `(r,s)` or the proved lossless reachable-state quotient; a continued-fraction tail couples signed `a0`, positive later terms, and its finite/infinite status. Query horizon and resource budget do not become state or native control (`principles.md:47-69`).
- **Principles 8–10 — lossless mappings before new classes.** T36 codecs, T34/T35 exact values, T41 definitions/query envelopes, and T43 scalar/product maps are reused directly or by restriction. The long-division/residual and fixed-program square-root commuting relations establish representation equivalence; finite prefixes are explicitly non-injective and therefore cannot replace exact values. These results justify classes 1–3 only and no new semantic class or executor (`principles.md:71-87`).
- **Principles 11–12 — execution and observation remain downstream.** One branch-free runner can execute each declared work program. Direct nth-coefficient evaluation is a typed pure query, not a fake rollout. Walks, histograms, statistical tests, normality claims, crops, palettes, and suppressed trailing zeros neither feed evaluation nor strengthen proof status (`principles.md:89-103`).
- **Principles 13–16 — adversarial fidelity is the closure gate.** Signed values, unbounded continued-fraction terms, terminating positional zero tails, rational continued-fraction completion, direct-access methods, source-defect counterexamples, prefix collisions, fixed-program quotient inversion, unsupported exact definitions, and the T42 rational rejection exercise the abstraction. Any opaque packing, float/CAS fallback, callback, family dispatch, hidden state, fixed-capacity simulation, or invented event is a hard failure rather than a compatibility route (`principles.md:105-127`).

The smallest honest model is therefore an immutable exact denotation plus a typed representation query/result, with optional closed evaluator realizations expressed through existing SimpleProgram axes. The direct source representations may remain named presets, but source vocabulary alone does not prove a new runtime class; only a concrete failure of every lossless parameterization, restriction, or tagged/product representation would do so, and T40 supplies no such counterexample.

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

`src/ca` is the current implementation location of the intended SimplePrograms library, not a claim that every catalog construction is semantically a cellular automaton. Its executable realization nevertheless remains CA-shaped and family-dispatched today. T40 therefore exercises shared migrations and declarative modules, not a `constant_digits` rollout branch.

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
- Declare v1 scope as positive-integer-radix positional plus simple continued fraction. Preserve unary, negative-radix, non-power/mixed-weight, multiplicative, Gray-code, and Zeckendorf evidence as explicit relation profiles for later separately tagged codecs; do not force them through the v1 positional tag or treat them as new executors.
- Reuse T36 positional codecs without importing T36 transition state. Keep sign, integer part, radix point, leading/trailing-zero policy, and dual-expansion normalization explicit.
- Represent unsupported/certified/approximate/probable/unknown/resource/failure outcomes without silent float or CAS fallback. A coefficient is exact only when its floor or equivalent separation is certified.
- Model long division, positional residual iteration, strict integer-safe square-root extraction, and continued-fraction residual iteration as named closed work SimplePrograms over existing singleton/product map axes. Bind each to the query by an explicit realization certificate and event-witness replay.
- Preserve evaluator work configuration, exact denotation, generated coefficients, finite queried prefix, full representation denotation, trace, and rendering as distinct records.
- Give T40 ownership of generic positional/continued-fraction expansion and coefficient queries, including signed `a0` with positive tail coefficients. The T42 seam carries the complete immutable replay-verified result, proof strength, typed irrational-prefix/finite-completion status, natural coefficient orientation, and count; strict T42 rejects rational completion, then owns schedule derivation plus substitution-side state/update/trace.
- Add no `ConstantDigitsState`, expansion FRONTIER/NEIGHBORHOOD, coefficient-append UPDATE, executor, rollout family, arbitrary callback, hidden prefix/remainder, host CAS object, float coercion, or object-array escape hatch.

## No-Cheating Checks

- No exact constant represented by an approximate float, rendered digit string, finite prefix, raster, host symbolic object, or opaque callback.
- No base, sign/radix convention, canonicalization, evaluator version, precision, or certificate context left implicit.
- No unary, negative-radix, non-power/mixed-weight, multiplicative, Gray-code, self-delimiting, or Fibonacci/Zeckendorf representation mislabeled as strict v1 `Positional(base>=2)`; each future codec needs its own closed tag, inverse, and ambiguity/completeness invariants.
- No `term_count` used as state, control, capacity, native halt, or constant identity; it is a query horizon.
- No terminating positional expansion mislabeled finite when the strict representation includes trailing zeros; suppression remains rendering.
- No rational continued fraction extended after exact finite completion; no reciprocal-of-zero failure substituted for the query's normal completion.
- No unbounded continued-fraction coefficient forced through finite alphabet ranks, `uint16`, signed `int64`, or palette codes.
- No finite prefix claimed lossless, random, normal, or sufficient work state.
- No sequential prefix events fabricated for a direct nth-digit evaluator; no approximate/probable result promoted to exact.
- No square-root residual hidden: use direct `(r,s)` or the proved invariant-valid fixed-program `(n,profile,s)` quotient with explicit inverse. Do not use bare `s` across programs, and do not silently accept the false arbitrary-rational source claim.
- No long-division remainder, Gauss residual, evaluator cache, precision state, or resource counter hidden outside a declared work configuration/context.
- No T40-specific state, DOMAIN, FRONTIER, NEIGHBORHOOD, RULE-result wrapper, UPDATE, executor, family branch, or identity/no-op rollout.

## Frozen Source Closure

`45-T40-source-oracle.py` freezes 20 discovery lanes and their 213-row union, but completeness no longer depends on those searches. A fixed strict-main universe routes every one of the 117 nonblank `BOOK:1665-1832` rows as `102 native / 15 structural`; a second fixed universe routes all 126 native-Notes rows as `58 native / 67 relation / 1 control`. The complete 897-row actual Index block is partitioned `30 native / 102 relation / 4 control / 16 excluded / 745 unrelated`, with a line-bound disposition record for every physical row. Its 136-row semantic universe contains 81 relevant rows missed by the ordinary query candidates; an independently reproduced 114-row broad vocabulary set plus 70 hostile page/alias/continuation candidates closes 150 audit rows with zero unexplained row.

The independent Book-wide lane closes 309 direct-vocabulary matches at `242 pre-Index / 67 Index`: all 242 pre-Index rows are either among 110 retained direct hits or one of 132 line-hash-bound sibling exclusions, while the 67 Index hits enter the complete Index partition. Total retained governed evidence is 447 rows at `169 native / 238 relation / 40 control`. It binds 140 semantic guards, eight auxiliary guards, 30 extraction/source-defect records, 42 source-model records, 14 exclusion hashes, 136 Index guards, 63 image-role records, 18 image-assembly boundaries, and seven exact-logic contracts. The complete split disposition has 1,359 rows at `1,175 exact / 51 image-basename / 28 normalized / 16 summary / 89 omitted`, normalized minimum `0.995885`, with zero unresolved. Its audit digest is `5eeb98409dc44e07284e142355054d9dde66e7566fde4c9f36e35c0642840623`; script SHA-256 is `9209966474b1da250949cf74dbd2d4f844fb4b87f994be0806d4b8b79c87859c`.

The exact logic contract covers 2,079 long-division states, rational finite continued-fraction completion, finite-prefix loss, 96 strict square-root events, the extracted square-root bit divergence, and the `n=11/5` rational counterexample. Normal and JSON modes pass independently. The oracle is deterministic, standard-library-only, repo-relative, and explicitly rejects optimized mode; whole-source, auxiliary, split, candidate-asset, exact-partition, zero-unresolved, missing/duplicate-file, and malformed-usage failures are closed rather than repaired. The 63-candidate asset interface is frozen for the independent asset join below.

## Frozen Asset Closure

`45-T40-asset-oracle.py` closes exactly 27 governed images at `11 native / 15 relation / 1 control`, 52 references at `27 monolith / 25 split`, 27 distinct physical files and hashes totaling 612,140 bytes, and four multi-file assemblies spanning 16 files. The followed Gray-code, negative-base, and multiplicative-digit figures are relation-only evidence; the page-154 and page-156 split-link omissions are explicit. Every asset is `HASH_BOUND`; none is pixel-replayed or used as executable program data. The structural, ordered, and normalized textual-replay digests are respectively `9fb44dd3086ff0c853d09a867ccdfdd60716037fc4f52d527f6ec1bc217d6ffc`, `3e6e66a5730caae3371b21706ea124e4f19480925efc01e98cb6ee530124c9b5`, and `6fd8578623171650e57a405f2d3e9740b895724609fceb38132ceb202055c1fa`; ledger digest is `02ea3bb0e6519b2fcc78172a8f97dfded0d4a96148e2398056441640c4a79824`, and script SHA-256 is `85bd9225b5c36c7d6f0cc9a77e7c16be386a18cfc0095625b26f9b7fe15657d7`.

Its independent textual replay checks 8,255 long-division states and 96 strict-integer square-root events, guards all three mismatches between the extracted square-root bit string and the exact algorithm, and retains the rational source-claim counterexample. Source guards, semantic manifests, import, compilation, relocation, optimized mode, bad usage, hash mutation, and the real source-oracle interface pass.

## Frozen Semantic Closure

`45-T40-semantic-oracle.py` independently reproduces the asset interface at 8,255 long-division states, 96 strict square-root events, and three guarded extraction mismatches. It closes nine signed and unsigned exact rational positional cases, nine canonical round trips, 225 signed-prefix cylinders, 60 certified decimal and 96 certified binary digits of pi, 30 certified pi continued-fraction coefficients, five quadratic-surd periods/400 coefficients, a 120-term exact continued fraction for `e`, and an 80-term exact negative-surd prefix. Explicit work checks cover 255 long-division events, 390 square-root commutations/780 invariant checks, 390 inverse/step commutations for the fixed-program `s` quotient, and 24 Gauss-map commutations across six signed and unsigned sources. The `(5,4)` versus `(4,4)` witness is correctly scoped to loss of program identity; the surviving algebraic identity under the literal `11/5` misuse and both failed nonnegative/enclosure obligations remain executable guards.

The query audit checks 159 prefix/random-access agreements plus 36 certified random-access agreements, separate positional and continued-fraction prefix-loss cylinders, exact/certified/partial/resource outcomes at `1/1/1/2`, unsupported/unknown/approximate/probable/failure outcomes at `4/1/1/1/1`, and eight proof-nonpromotion rejections. Three strict T42 handoffs carry 32 exact and 12 certified finalized coefficients without an evaluator callback; one exercises signed `a0` with an otherwise positive irrational continued-fraction tail, while a signed rational-complete prefix is explicitly rejected without losing its typed completion status. The interface carries the complete immutable replay-verified result, so source/result identity, proof strength, source kind, orientation, and requested count cannot be replaced by opaque forged IDs. Exact rational-equivalence certificates likewise carry and replay both complete denotation specifications rather than trusting detached provenance IDs or an asserted common value. Positional sign is a separate `leading_minus_magnitude` convention/result component rather than a negative digit, and simple continued fractions admit any signed integer `a0` while rejecting nonpositive tail coefficients. Canonical terminating positional values are classified `eventually_zero_infinite`, never finite completion; genuine `finite_terminated` remains confined to rational continued fractions, and every certified/partial/resource Pi result is forced to retain `prefix_of_infinite`. The public surface contains 35 declarative/work dataclasses, three optional work-record types, and zero native T40 execution roles. The no-class-4 result is a reviewed architecture classification supported by the commuting realizations, not a circular executable cardinality. Seventy-two hostile rejections close invalid carriers, forged certificates, hidden roles, floats, sign/termination mistakes, silent source repairs, untyped boundary tags, and noncanonical strings nested inside recursive provenance keys. Semantic digest is `024c75c38de22ee74c41f54fd3b4be957e0c0fb6dec44c4c7cfc8b0f658b5608`; script SHA-256 is `016a0afff8469d96387bd5e9e97df61d6cb1f5e37ef0c9321e711ed33e0635d7`.

## Completion Requirements

- [ ] Every strict main, Notes, actual-Index, split, history, relation, control, exclusion, and extraction-defect candidate is dispositioned with zero unresolved mechanics.
- [ ] The complete 27-asset/52-reference universe is hash-bound with followed representation relations, split omissions, and source limitations explicit.
- [ ] Positional and continued-fraction definitions, canonicalization, coefficient queries, exactness levels, completion, work realizations, and observers are independently verified.
- [ ] Long division, square-root product/invariant and fixed-program quotient, positional/Gauss maps, direct nth access, and finite-prefix loss are adversarially tested.
- [ ] T34/T36/T37/T39/T41/T42/T43 and current-runtime boundaries are synchronized.
- [ ] Source, asset, semantic, cross-interface, mutation, portability, fail-closed, mode, Markdown, diff, scope, repository-test, and independent hostile-review gates pass.
- [ ] D139, plan, evidence index, design ledger, architecture audit, and Goal 2 handoffs are synchronized with no new execution algebra.

## Stage Results

Pending oracle and hostile-review closure.
