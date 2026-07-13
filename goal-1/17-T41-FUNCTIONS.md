# 17-T41-FUNCTIONS

Status: **REOPENED — ARCHITECTURE AUDIT; EVIDENCE CLOSED**

Architecture authority: the T41 row and declarative-category handoff in `architecture-audit.md` supersede construction-specific class proliferation below; the non-transition finding remains authoritative.

The evidence/search closure and conformance fixtures remain valid. T41 remains non-transition, while function forms and pure queries are being consolidated under generic closed-function and query/result records.

## Current Facts

- Exact catalog row: T41, CSV line 42, `Function-Combination Systems`; taxonomy vocabulary is `ref/notes/CA-Types.md:1132-1158`. T42 begins at taxonomy line 1160.
- Canonical main section `Mathematical Functions` is `BOOK:1834-1866`. T43 begins cleanly at `BOOK:1868`; the clean chapter duplicate is `CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:293-325`.
- Native Notes are `BOOK:13146-13214`; T43 Notes begin at `13215`. The useful line-oriented duplicate is misleadingly stored at `BACK-MATTER/Index/Index.md:1049-1117`; `BACK-MATTER/Notes/Notes.md` is one concatenated physical line and is unsuitable for provenance.
- The actual Index begins at `BOOK:20826`, not in the nominal Index split. All actual-Index matches are routes or homonyms and add no hidden execution mechanics.
- The four strict main rasters name six standard functions, four sine combinations, four cosine-difference/substitution bridges, and one Riemann-Siegel Z curve. Eight Notes-only rasters add parametric Lissajous curves, complex zeros, zero-spacing distributions, finite Fourier/lacunary sums, and approximations to weighted infinite sums.
- The monolithic Markdown's four strict image links and eight Notes image links are bare and broken relative paths. The clean chapter/Notes duplicate resolves them through its local `Images/` directories. Canonical text provenance and split asset provenance must therefore be recorded separately.
- Standard curves, finite combinations, an exact mathematical zero set, and the Riemann-Siegel curve are mathematical objects, not evolving states. Traversing an x-axis or evaluating a mesh does not create semantic time.
- T41 is a pure specification/query category: an immutable closed mathematical-function definition is separate from point evaluation, curve sampling, exact or certified zero finding, crossing classification, plotting, sound rendering, spacing histograms, and spectral analysis.
- A mathematical domain, a query interval or complex region, a sampling mesh, and a rendered viewport are different scopes. None of the twelve rasters states a sampling mesh, adaptivity rule, numerical precision, or error tolerance; raster dimensions cannot supply them.
- `Tan` and `Sec` have poles; `Zeta` and complex powers require domain/continuation/branch conventions. An evaluator must return typed undefined/failure outcomes rather than draw clipped near-vertical strokes as function values.
- The page-161 two-sine functions have exact factorization, periods, and zero families. Inclusive `[0,250]` root counts are exactly `120`, `114`, and `113`; strictly interior counts are one smaller because `x=0` is included in the former convention.
- The page-161 three-sine row has 112 numerically observed roots on inclusive `[0,250]`, but that result is approximate and non-certified. The book's much larger `0<x<10^6` count is a source-reported observer, not an independently certified strict-page oracle.
- Page 162 must be split by clause. T41 owns each source function, exact zero families, crossing/touch classification, and interval-count query. T42 owns the continued-fraction coefficient stream, black/white word, per-step rule selection, substitutions, nested state, and generated trace.
- In `Cos[x]-Cos[alpha x]`, `x=0` is a double zero/touch, not a sign crossing. The caption's general phrase “axis crossing” cannot override exact multiplicity; endpoint and crossing conventions belong in the query/result record.
- The main zeta Dirichlet series converges only for `Re(s)>1`, so it does not define the plotted critical-line values by itself. Native Notes explicitly supply analytic continuation and the Riemann-Siegel phase factor.
- The source's `Arg[Gamma[...]]` notation for `RiemannSiegelTheta` requires the named continuous phase convention. A generic principal-`Arg` implementation would introduce jumps and is not an interchangeable primitive.
- The Notes' ODE profile is internally inconsistent: `Sin[x]+Sin[sqrt(2)x]` has `y'(0)=1+sqrt(2)`, not `2`. The printed IVP instead solves to `Sin[x]+Sin[sqrt(2)x]/sqrt(2)`. Literal and corrected profiles must remain explicit.
- The weighted Weierstrass caption says the curves are “approximations.” Its displayed `a=0` ordinary infinite series fails the term test generically; an implementation must require an explicit finite truncation or nonstandard summation profile rather than claim ordinary convergence.
- Current `FormulaRule` and selector callbacks can hide an evaluator, but they are opaque and update-oriented. Current `Dynamics`, rollout arrays, finite float alphabets, rank-4 loci, family dispatch, and viewer export cannot represent a closed real/complex function spec or typed query result without semantic distortion.
- The exhaustive textual and raster audits found zero unresolved candidate. Native strict and Notes scopes contain no `update` or `evolution` vocabulary and no sampling vocabulary; all `step`/`rule` hits in the strict range are T42 substitution language.

## Updated Assumptions

- Use a versioned, closed `MathematicalFunctionSpec`, not `Callable`, `eval`, a formula string, a host CAS object, pickle, or precomputed samples.
- Reuse T20's ordered-tree carrier and exact structural codec responsibilities only. T41 expressions denote functions and are not T20 pattern-rewrite state or transition traces.
- A strict function spec declares one argument, exact parameters, real/complex argument space, mathematical domain restrictions, scalar or fixed-vector codomain, closed output expressions, primitive registry version, partiality, and branch/continuation conventions. Multivariate arguments remain a later evidence question.
- Primitive calls have declared arity and domain. The strict registry must at least cover `Sin`, `Cos`, `Tan`, `Sec`, `SinIntegral`, `BesselJ`, `AiryAi`, `Exp`, `Log`, `Arg`, `Gamma`, `Zeta`, and named `RiemannSiegelTheta`/`RiemannSiegelZ` profiles.
- Exact integers, reduced rationals, named constants, algebraic constructions, declared-precision decimals, and typed complex numbers remain distinct values. Binary floats never silently replace exact coefficients such as `3/2`, `10/7`, `sqrt(2)`, or `pi`.
- Point evaluation, sampled curve, real-zero, complex-zero, crossing, extremum, spacing, plot, sound, and spectrum requests are different query/observer types rather than one callback with mode flags.
- Every numerical query declares arithmetic mode, precision, rounding/error targets, method profile, resource limit, scope, and endpoint convention. Certification is explicit; an approximate answer is never relabeled exact or complete.
- Sampled sign changes are root candidates only. They may miss tangent/even-multiplicity roots and may mistake a pole for a crossing.
- Zero events distinguish zero from sign crossing, direction, tangent contact, multiplicity known/unknown, exact/certified/approximate location, and endpoint membership. A zero-set result separately declares completeness/certification status.
- Structural identity, certified functional equivalence on a declared domain, and equality of a particular observation are different relations. Factored and expanded expressions need not have identical spec IDs even when a proof relates their denotations.
- Finite sums may be expanded into the strict finite AST or represented by a closed bounded binder. Infinite series require a separate convergence/summation profile and cannot be smuggled into the strict AST through an unbounded loop.
- T42 substitution, T43 iteration, T44 continuous lattice updates, T45 PDE definitions/solution queries, differential-equation alternate definitions, and numerical solvers remain explicit typed boundaries.

## Big Picture Objective

Reconstruct function-combination systems as inspectable mathematical definitions with separately typed evaluation and observation. Pin down exact expression syntax, domains/codomains, named-function semantics, singularities and branches, exact versus numerical outcomes, zero/crossing queries, sampling and rendering scopes, figure presets, series convergence, T42/T43/T44/T45 boundaries, current API/runtime pressure, and the smallest honest Goal 2 category without inventing an eleventh update law.

## Catalog Identity

- Stable ID: T41.
- Exact CSV name: `Function-Combination Systems` at `ref/notes/CA-Types.csv:42`.
- Taxonomy vocabulary: `ref/notes/CA-Types.md:1132-1158`; this is a search seed, not book evidence.
- Canonical strict main: `BOOK:1834-1866`; clean chapter duplicate `Systems-Based-on-Numbers.md:293-325`.
- Native Notes: `BOOK:13146-13214`; T43 Notes begin at `13215`.
- Entry kind: a pure mathematical-specification family plus typed queries and downstream observers; no transition state, source, result, update, successor, or halting semantics.
- Strict profiles: six named real curves, four finite sine combinations, four two-cosine source curves shared with the T42 bridge, and a named Riemann-Siegel real curve derived from complex zeta.
- Supplementary variants: fixed-vector parametric/Lissajous curves, complex-domain zero queries, rational and irrational frequency sums, finite Fourier sums, lacunary/Weierstrass sums, weighted convergent series, FM composition, and analytic continuation.
- Aliases/routes: mathematical functions, standard functions, function combinations, sine/cosine functions, axis crossings/zeros, Lissajous/Bowditch, Fourier series, Gibbs phenomenon, Weierstrass/Zygmund series, quasiperiodicity/almost-periodic functions, waveforms/chords, zeta, Riemann-Siegel, and Riemann Hypothesis.

## Search Log

1. Read CSV line 42 and taxonomy section 41 in full, then the strict main section, clean chapter duplicate, native Notes, line-oriented Notes duplicate, all twelve linked rasters at original resolution, actual Index, historical/support passages, current program document, runtime, tests, and every followed cross-reference.
2. Confirmed boundaries: strict T41 is `BOOK:1834-1866`; T43 starts `1868`. Native Notes are `13146-13214`; T43 Notes start `13215`. T41/T42 ownership is clause-split across main `1850-1858` and Notes `13170-13172`, not page-split.
3. Exact `function[- ]combination systems?` and `function combinations?` found **0/0** occurrences/unique lines. The conservative direct-name union with `mathematical functions?` and flexible combinations found **59/51**: `50/45` pre-Index and `9/6` actual Index.
4. `mathematical functions?` alone found **56/48** (`47/42 + 9/6`). The only three flexible “combinations of ... functions” hits are native `1844`, integer-function formula material `11311`, and Boolean decision diagrams `18003`; only the first is direct T41 evidence.
5. `sine functions?` found **12/10**, `cosine functions?` **1/1**, and exact `Mathematical Functions` headings **2/2**. The second heading is native Notes, not a second construction section.
6. Strict `_page_160..163_` links found exactly **4/4**; native-Notes `_page_932..933_` links exactly **8/8**. File enumeration found no additional copy in scope.
7. A formula-literal union over `Sin[`, `Cos[`, `Zeta[`, Riemann-Siegel spellings, and page-145 named functions found **176/83**, all pre-Index. Its 83 lines partition into strict T41 `1850,1856,1866`; native T41/T42 Notes `13148,13153,13154,13156,13162,13164,13170,13172,13174,13178,13182,13186,13190,13195,13197,13201,13213`; and explicitly dispositioned T43, PDE, geometry, number/substitution, dynamical-zeta, chaos, gravity, quantum, audio/compression, evaluation, and radio contexts.
8. Crossing/rule mechanics found **19/9**. Mixed T41/T42 evidence is `1850,1856,1858,13156,13170,13172`; `12587,16418,16446` are unrelated substitution uses. Literal `zero-crossing` occurs only at `14971` in a three-body/PDE context; T41 says “axis crossings” or “zeros.”
9. `generalized substitution systems?` found **7/5**. `continued fractions?` found **78/58** (`46/30 + 32/28`); `continued fraction representations?` **13/11**. Only the page-162 bridge clauses are relevant here, and their state/rule mechanics are assigned to T42.
10. Named families found: `Lissajous|Bowditch` **9/7**, `Fourier` **40/29**, `Fourier series` **4/3**, `Gibbs phenomenon` **5/5**, `Weierstrass` **12/9**, `(Riemann )?zeta function` **21/15**, Riemann-Siegel spellings **9/5**, `Riemann Hypothesis` **9/8**, and `BesselJ|AiryAi|JacobiSN|MathieuC` **14/9**. Every native, history, relation, homonym, and Index route is classified below.
11. Fifth/tritone aliases found **12/7**. Quasiperiodic/almost-periodic/trigonometric/Zygmund aliases found **8/8**. Native music hits are `1848,13155`; actual Index routes include quasiperiodicity at `21877`, almost-periodic functions at `21086`, and Zygmund series at `22456`; none adds mechanics.
12. Direct-name pre-Index lines partition into native strict `1834,1836,1838,1842,1844,1860`; T43 boundary `1870`; native Notes `13146,13148`; T40 boundary `12976,13144`; 22 support/history/evaluation lines; and 12 other-system or lexical false positives. No candidate is silently omitted.
13. The 29 actual-Index candidate lines are `20850,20864,20918,21068,21080,21090,21150,21193,21195,21223,21251,21364,21450,21471,21477,21511,21683,21713,21771,21795,21944,22114,22120,22132,22352,22392,22416,22432,22456`. All are routes or homonyms; no Index entry supplies transition or sampling semantics.
14. Native-scope lexical controls: strict `1834-1866` has `function` **20/11**, `curve` **21/9**, and `update|evolution`, `sample*`, `expression` all **0/0**. Notes `13146-13214` have `function` **18/9**, `curve` **6/5**, and those three control families **0/0**. Apparent `state` hits are grammatical statements of the Riemann Hypothesis.
15. Supporting passages establish named function primitives (`17794-17798`), waveform/Fourier/sound relations (`17273,17277,17499,17505-17511`), Weierstrass history and `1/f` relation (`13786,14878`), definition/evaluation separation (`19185-19187`), and the already repaired T39 zeta/prime relation (`12869`). These are relations, not additional T41 execution profiles.
16. Independent symbolic/numerical checks regenerated two-sine periods and zero counts, the page-162 factorizations/continued fractions/count words, page-160 function anchors, the page-161 three-sine approximate roots, and Riemann-Siegel values/zero counts. Exact, certified, source-reported, and approximate claims are labeled separately.
17. Zero unresolved textual, raster, split, Notes, Index, history, alias, variant, or relation candidate remains. Counts use only the canonical monolith, so split duplicates are not double-counted.

Representative commands used case-insensitive Perl occurrence/unique-line counters split at `BOOK:20826`, `rg -n -i` vocabulary unions, `sed` context reads, `rg --files`, `file`, `sha256sum`, original-resolution inspection, exact symbolic formulas, and independent arbitrary-precision numerical evaluation.

## Book Excerpts

`BOOK` below means `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`. Quotations preserve source wording and extraction artifacts; repairs and semantic dispositions follow them.

### E01 — Named functions as plotted curves

- Provenance: `BOOK:1836-1842`, strict main.
- Establishes: the primary object is a function viewed as a curve; named ordinary examples are largely repetitive.

> “The pictures below show curves obtained by plotting standard mathematical functions. All of these curves have fairly simple, essentially repetitive forms. And indeed it turns out that almost all the standard mathematical functions that are defined, for example, in *Mathematica*, yield similarly simple curves.”

> “The top row shows three trigonometric functions. The bottom row shows three so-called special functions that are commonly encountered in mathematical physics and other areas of traditional science.”

“Essentially repetitive” is qualitative; `SinIntegral`, `BesselJ`, and `AiryAi` are not thereby declared periodic.

### E02 — Combinations and waveform interpretation

- Provenance: `BOOK:1844-1848`, strict main/caption.
- Establishes: arithmetic combination changes qualitative curve behavior; sound/chord interpretation is downstream of the same function.

> “But if one looks at combinations of these standard functions, it is fairly easy to get more complicated results. The pictures on the next page show what happens, for example, if one adds together various sine functions.”

> “Curves obtained by adding together various sine functions. In the first two cases, the curves are ultimately repetitive; in the second two cases they are not. If viewed as waveforms for sounds, then these curves correspond to chords.”

The first two displayed finite rational-frequency sums are exactly periodic, not merely eventually periodic.

### E03 — Axis crossings and continued-fraction source

- Provenance: `BOOK:1850-1852`, strict main.
- Establishes: crossings derive from the curve; a distinct continued-fraction representation supplies T42's rule schedule.

> “In the third picture, however, the points where the curve crosses the axis come in two regularly spaced families. And as the pictures on the facing page indicate, for any curve like  $Sin[x] + Sin[\alpha x]$  the relative arrangements of these crossing points turn out to be related to the output of a generalized substitution system in which the rule at each step is obtained from a term in the continued fraction representation of  $(\alpha - 1)/(\alpha + 1)$ .”

> “When  $\alpha$  is a square root, then as discussed in the previous section, the continued fraction representation is purely repetitive,”

The raster's first two coefficients are affine quadratic irrationals, so “square root” is imprecise shorthand; periodic continued fractions are the operative property.

### E04 — Exact T41/T42 boundary

- Provenance: `BOOK:1856-1858`, page-162 caption and continuation.
- Establishes: T42 reproduces a T41 crossing word; the special relation stops beyond two terms.

> “Curves obtained by adding or subtracting exactly two sine or cosine functions turn out to have a pattern of axis crossings that can be reproduced by a generalized substitution system. In general there is an axis crossing within an interval when the corresponding element in the generalized substitution system is black, and there is not when the element is white.”

> “In the case of  $Cos[x]-Cos[\alpha x]$  each step in the generalized substitution system has a rule determined as shown on the left from a term in the continued fraction representation of  $(\alpha-1)/(\alpha+1)$ .”

> “And if more than two sine functions are involved there no longer seems to be any particular connection to generalized substitution systems or continued fractions.”

### E05 — Zeta and Riemann-Siegel in the strict section

- Provenance: `BOOK:1860-1866`, strict main/caption.
- Establishes: a named complex function defines a complicated real curve without a transition.

> “Many of these are related to the so-called Riemann zeta function, a version of which is shown in the picture below.”

> “The basic definition of this function is fairly simple. But in the end the function turns out to be related to the distribution of primes—and the curve it generates is quite complicated.”

> “The curve shown here is the so-called Riemann-Siegel Z function, which is essentially Zeta[1/2 + it].”

The main Dirichlet-series formula is not valid on the plotted line by ordinary convergence, “essentially” omits a phase, and its peak/valley RH wording is qualitative. E14-E15 supply the repairs.

### E06 — Oscillatory standard-function variants

- Provenance: `BOOK:13148`, native Notes.
- Establishes: elementary and special functions have distinct asymptotics and complex-direction qualifications.

> “BesselJ[0, x] goes like  $Sin[x]/\sqrt{x}$  for large x while AiryAi[-x]goes like  $Sin[x^{3/2}]/x^{1/4}$ . Other standard mathematical functions that oscillate at large x include JacobiSN and MathieuC. Most hypergeometric-type functions either increase or decrease exponentially for large arguments, though in the directions of Stokes lines in the complex plane they can oscillate sinusoidally.”

### E07 — Lissajous/Bowditch parametric curves

- Provenance: `BOOK:13149`, native Notes.
- Establishes: multiple coordinate functions form a fixed-vector parametric curve; closure is a property, not an evolution halt.

> “Plotting multiple sine functions each on different coordinate axes yields so-called Lissajous or Bowditch figures, as illustrated below. If the coefficients inside all the sine functions are rational, then going from t = 0 to  $t = 2 \pi Apply[LCM, Map[Denominator, list]]$  yields a closed curve. Irrational ratios of coefficients lead to curves that never close and eventually fill space uniformly.”

### E08 — Exact two-sine zero families

- Provenance: `BOOK:13153`, native Notes.
- Establishes: exact symbolic factorization yields a zero-set observer.

> “Sin[ax] + Sin[bx] can be rewritten as 2 Sin[1/2(a+b)x] Cos[1/2(a-b)x] (using TrigFactor), implying that the function has two families of equally spaced zeros:  $2 \pi n/(a+b)$  and  $2 \pi (n+1/2)/(b-a)$ .”

### E09 — Differential-equation and chord relations

- Provenance: `BOOK:13154-13155`, native Notes.
- Establishes: alternate definition and auditory interpretation are relations, not changes to the function spec.

> “The function  $Sin[x] + Sin[\sqrt{2} x]$  can be obtained as the solution of the differential equation y''[x] + 2y[x] - Sin[x] == 0 with the initial conditions y[0] == 0, y'[0] == 2.”

> “In a so-called equal temperament scale the 12 standard musical notes that make up an octave have a progression of frequencies  $2^{n/12}$ .”

> “diminished fifth or tritone chords that consist of two notes (such as C and Gb) with frequency ratio  $\sqrt{2}$  have generally been avoided as sounding discordant.”

The ODE sentence is a source inconsistency. Substitution shows that the printed IVP yields `Sin[x]+Sin[sqrt(2)x]/sqrt(2)`; the stated target instead requires `y'[0]=1+sqrt(2)`. Goal 2 preserves a literal-source relation record and a separately named corrected relation.

### E10 — Three-term zero behavior

- Provenance: `BOOK:13156-13164`, native Notes.
- Establishes: arity and coefficient arithmetic affect real/complex zeros, periodicity, and spacing observations.

> “All zeros of the function Sin[ax] + Sin[bx] lie on the real axis. But for Sin[ax] + Sin[bx] + Sin[cx], there are usually zeros off the real axis”

> “If a, b and c are rational, Sin[ax] + Sin[bx] + Sin[cx] is periodic with period  $2\pi/GCD[a, b, c]$ , and there are a limited number of different spacings between zeros.”

> “For  $0 < x < 10^6$  there are a total of 448,494 zeros, with maximum spacing  $\simeq 4.6$  and minimum spacing  $\simeq 0.013$ .”

### E11 — Zero-spacing sequence and T42 substitution

- Provenance: `BOOK:13170-13172`, native Notes.
- Establishes: exact cosine zero families are T41; the interval word and substitution realization cross into T42.

> “Cos[ax] - Cos[bx] has two families of zeros:  $2\pi n/(a+b)$  and  $2\pi n/(b-a)$ . Assuming b > a > 0, the number of zeros from the second family which appear between the  $n^{th}$  and  $n + 1^{th}$  zero from the first family is (Floor[(n+1)#] - Floor[n#] &)[(b-a)/(a+b)]”

> “and as discussed on page 903 this sequence can be obtained by applying a sequence of substitution rules. For Sin[ax] + Sin[bx] a more complicated sequence of substitution rules yields the analogous sequence in which -1/2 is inserted in each Floor.”

### E12 — Fourier coefficient support

- Provenance: `BOOK:13174-13184`, native Notes.
- Establishes: coefficient schedule and finite term count are part of the expression; limits and plots remain distinct.

> “Adding many sine functions yields a so-called Fourier series (see page 1074). The pictures below show  $Sum[Sin[nx]/n, \{n, k\}]$  for various numbers of terms k. Apart from a glitch that gets narrower with increasing k (the so-called Gibbs phenomenon), the result has a simple triangular form.”

> “The pictures below show  $Sum[Sin[n^2 x]/n^2, \{n, k\}]$ , where in effect all coefficients of Sin[mx] other than those where m is a perfect square are set to zero. The result is a much more complicated curve.”

### E13 — Weierstrass families and FM composition

- Provenance: `BOOK:13186-13194`, native Notes.
- Establishes: lacunary frequency schedules create nested curves; weighting changes observer properties; FM is another explicit composition family.

> “The pictures below show  $Sum[Cos[2^n x], \{n, k\}]$  (as studied by Karl Weierstrass in 1872). The curves obtained in this case show a definite nested structure, in which the value at a point x is essentially determined directly from the base 2 digit sequence of x.”

> “The curves below are approximations to  $Sum[Cos[2^n x]/2^{an}, \{n, \infty\}]$ . They can be thought of as having dimensions 2-a and smoothed power spectra  $\omega^{-(1+2a)}$ .”

> “More complicated curves can be obtained for example using FM synthesis, as discussed on page 1079.”

“Approximations” is essential: the `a=0` ordinary infinite series is not convergent.

### E14 — Zeta continuation and exact RH statement

- Provenance: `BOOK:13195`, native Notes.
- Establishes: series/product domains, analytic continuation, prime relation, and exact root-line statement.

> “For real s the Riemann zeta function Zeta[s] is given by  $Sum[1/n^s, \{n, \infty\}]$  or  $Product[1/(1-Prime[n]^s), \{n, \infty\}]$ . The zeta function as analytically continued for complex s was studied by Bernhard Riemann in 1859”

> “The Riemann Hypothesis then states that all r[i] satisfy Re[r[i]] = 1/2”

This line contains OCR-lost subtraction signs in later prime-count formulas; T39's recorded repairs remain authoritative.

### E15 — Exact Riemann-Siegel definition and evaluator cost

- Provenance: `BOOK:13197-13203`, native Notes.
- Establishes: the real plotted function includes a phase; approximation and work belong to evaluator profiles.

> “The picture in the main text shows RiemannSiegelZ[t], defined as Zeta[1/2 + it] Exp[i RiemannSiegelTheta[t]], where RiemannSiegelTheta[t_] =”

> “ $Arg[Gamma[1/4 + it/2]] - 1/2t Log[\pi]$ ”

> “The first term in an approximation to `RiemannSiegelZ[t]` is `2Cos[RiemannSiegelTheta[t]]`; to get results to a given precision requires summing a number of terms that increases like  $\sqrt{t}$ ”

### E16 — Riemann-Siegel observations and universality

- Provenance: `BOOK:13205-13213`, native Notes.
- Establishes: zero spacing/amplitude are derived measurements; random-matrix comparison and Voronin universality are relations.

> “The average spacing between zeros decreases like 1/Log[t].”

> “The amplitude of wiggles grows with t, but more slowly than  $t^{0.16}$ .”

> “the spacings between zeros are distributed like the spacings between eigenvalues of random unitary matrices”

> “there always in principle exists some t ... for which it can reproduce to any specified precision ... any analytic function without zeros.”

### E17 — Meaning of a standard mathematical function

- Provenance: `BOOK:17794-17798`, supporting Notes/history.
- Establishes: named functions are accepted symbolic formula primitives with varied origins.

> “There are an infinite number of possible functions with integer or continuous arguments. But in practice there is a definite set of standard named mathematical functions that are considered reasonable to include as primitives in formulas”

> “The socalled elementary functions (logarithms, exponentials, trigonometric and hyperbolic functions, and their inverses) were mostly introduced before about 1700. In the 1700s and 1800s another several hundred so-called special functions were introduced.”

> “Most arose first as solutions to specific differential equations, typically in physics and astronomy; some arose as products, sums of series or inverses of other functions.”

### E18 — Definition/evaluation/precision separation

- Provenance: `BOOK:19185-19187`, supporting evaluation Note.
- Establishes: definition, evaluation algorithm, precision, approximation, and cost are separate responsibilities.

> “The main issue in evaluating those that exhibit regular oscillations at large x is to find their oscillation period with sufficient precision.”

> “Thus for example if x is an integer with n digits then evaluating Sin[x] or FractionalPart[x c] requires respectively finding  $\pi$  or c to n-digit precision.”

> “Known methods for high-precision evaluation of special functions—usually based in the end on series representations—typically require of order  $n^{1/s} m[n]$ operations”

> “The best-known algorithms for evaluating Zeta[1/2 + ix] ... to fixed precision take roughly  $\sqrt{x}$  operations”

## Construction Model

### Category and applicability

| Construction question | T41 answer |
|---|---|
| Semantic object | Immutable closed mathematical-function specification; optionally scalar or fixed-vector valued |
| State/control/frontier | `NOT APPLICABLE`; no mutable state, cursor, control, or active locus |
| Read/rule/result/update | `NOT APPLICABLE`; evaluation is a query over a definition, not a transition |
| Successor/halting | `NOT APPLICABLE`; finite query completion/resource outcomes are not system halts |
| Native support | Declared real or complex argument space and mathematical domain restriction |
| Native values | Exact/named/algebraic/declared-precision real or complex values; fixed vectors when declared |
| Records | Function spec, query, typed evaluation/zero result, proof/certificate/diagnostic, and downstream observation |
| Rendering | External finite view with explicit interval, sampling, segmentation, and numerical context |

### Closed function specification

The minimum public data model is:

```text
MathematicalFunctionSpec = {
  argument: ArgumentDecl,
  parameters: OrderedTuple[ExactOrDeclaredNumericParameter],
  argument_space: Real | Complex,
  domain: ClosedDomainSpec,
  codomain: Real | Complex | FixedVector[Real|Complex, dimension],
  outputs: NonEmptyTuple[FunctionExpr],
  primitive_registry_version: Identifier,
  partiality: PartialityProfile,
  branch_conventions: OrderedTuple[BranchConvention]
}

FunctionExpr =
    ArgumentRef | ParameterRef | NumericLiteral | NamedConstant
  | Neg(expr) | Add(nonempty_exprs) | Mul(nonempty_exprs)
  | Sub(left,right) | Div(numerator,denominator) | Pow(base,exponent)
  | PrimitiveCall(tag, ordered_args)
  | BoundedFiniteSum(index, lower, upper, body)
```

- Strict scalar profiles use one output. Lissajous profiles use two or three output expressions sharing one parameter; they are not sampled point bags or T27 occurrence state.
- The primitive registry is a versioned closed table of tags, arities, mathematical domains, codomains, continuation semantics, and evaluator contracts. Unsupported calls fail validation; no fallback invokes a host function by name.
- `BoundedFiniteSum` is exact finite syntax. It may normalize to an expanded `Add` for small constant bounds. An infinite-series definition is a separate `SeriesFunctionSpec` with convergence domain and summation mode; `upper=infinity` is invalid in the finite node.
- The closed domain predicate supports intervals, half-planes, finite exclusions such as trigonometric poles, products, and named analytic-continuation domains. It is structural data, not a predicate callback.
- Domain and codomain are part of identity. A real restriction of a complex function and the complex function itself are different specs even if their formulas serialize similarly.

### Numeric and branch semantics

- Exact numeric nodes include arbitrary-precision integers, reduced rationals, named `Pi`, `E`, and `I`, and structural algebraic values such as `Sqrt(2)` or `CubeRoot(5)`. They serialize as tagged strings/nodes rather than JSON binary numbers.
- A decimal literal carries its original decimal string, declared precision, and rounding provenance. A complex value is a tagged pair of typed real components.
- `Tan`/`Sec` return `Undefined(Pole)` at `pi/2+k*pi`; plot segmentation must not connect samples across those exclusions.
- `Zeta` distinguishes the ordinary Dirichlet-series definition/domain from named analytic continuation. `RiemannSiegelZ` references the continued zeta function and the continuous `RiemannSiegelTheta` phase convention.
- Complex `Log`, fractional `Pow`, roots, `Arg`, `LogGamma`, and related branch-bearing primitives name their branch conventions. `Gamma` itself is single-valued meromorphic and instead declares analytic continuation and poles. A generic library default cannot silently determine portable semantics.

### Pure query algebra

The common query header declares `function_id`, scope, arithmetic mode, precision/rounding, absolute/relative error targets, method profile, certification request, and resource limits. Query members are:

1. `PointEvaluation(argument)`;
2. `SampleCurve(interval_or_path, endpoint_policy, mesh_strategy, segmentation_policy)`;
3. `RealZeroQuery(interval, endpoint_policy, multiplicity_policy, completeness_request)`;
4. `ComplexZeroQuery(region, boundary_policy, multiplicity_policy, completeness_request)`;
5. `CrossingQuery(interval, endpoint_policy, direction_policy)`;
6. `ExtremumQuery(scope, classification_policy)`.

Point results form a closed sum:

```text
ExactValue(value)
CertifiedEnclosure(enclosure, proof_or_method)
ApproximateValue(value, error_estimate, context)
UndefinedValue(Pole | BranchCut | OutsideDomain | Indeterminate)
EvaluationFailure(Unsupported | NonConvergence | ResourceLimit | Diagnostic)
```

Sampling results are ordered argument/value records with segment breaks and per-point status. They never become the function's definition or equality witness.

### Zero and crossing records

```text
ZeroEvent = {
  location: ExactValue | CertifiedEnclosure | ApproximateValue,
  multiplicity: PositiveInteger | Unknown,
  classification: Crossing(direction) | Tangent | ZeroUnclassified,
  endpoint_membership: Interior | IncludedLeft | IncludedRight | Exterior,
  certification: Exact | Certified | Approximate
}

ZeroSetResult = {
  query_id,
  ordered_events,
  status: CompleteExact | CompleteCertified | Partial | Unknown | ResourceLimit,
  diagnostics
}
```

- A zero and a sign crossing are not synonyms. Page 162's `x=0` double zero is `Tangent`; page 161's `x=0` simple zeros have global crossing classification even when a finite interval exposes only one side.
- A sign-change bracket is a candidate witness, not completeness. Even-multiplicity roots may not change sign; a pole may change apparent sample sign without any zero.
- A complex-root query returns a finite multiset in a declared region with multiplicity and boundary policy. A contour raster with unspecified levels is not a certified root list.
- Root-spacing histograms consume a zero result plus explicit ordering, normalization, horizon, and bin policy. They are observers, not query state.

### Identity, equivalence, and serialization

1. **Structural identity** compares normalized tagged function-spec data: the argument, parameter order/values, domain, codomain, ordered output AST, primitive registry version, partiality, and branches.
2. **Functional equivalence** is a separately typed claim over a declared domain, supported by an exact derivation or certificate. It never rewrites IDs automatically.
3. **Observation equality** compares one query/result under its complete numerical context. Equal samples do not prove function equality.
4. AST child order is preserved, including for mathematically commutative operators. Commutation, factoring, and reassociation require a separately certified equivalence; no general algebraic quotient, tolerance, sample hash, or host simplifier determines spec identity.
5. Specs, queries, results, certificates, and renderings have separate tagged JSON schemas. Nonfinite values, arbitrary integers, rationals, algebraics, complex values, error bounds, and undefined reasons are lossless and explicit.

### Outcomes and trace

- T41 has no evolution trace. A reproducible query record contains spec ID, query data, evaluator/method version, result, certificate/diagnostic, and resource accounting.
- Adaptive sampling/root-finding internals may optionally emit a diagnostic algorithm trace, but that trace is not a mathematical state trajectory and is excluded from function identity.
- Cancellation/resource exhaustion returns a partial typed result and does not mutate the function spec or claim completeness.

## Exact Book Presets and Oracles

### Strict raster inventory

The four assets exist only under `ref/A-New-Kind-of-Science/CHAPTERS/4-Systems-Based-on-Numbers/Images/`:

| Printed page / asset | Bytes | Dimensions | SHA-256 |
|---|---:|---:|---|
| 145 / `_page_160_Figure_4.jpeg` | 67,171 | 1101x493 RGB | `e80986ddce2b14d7c8498430ac776995354e3d26ffdddbf22195a2410f91926a` |
| 146 / `_page_161_Figure_1.jpeg` | 156,748 | 1210x909 RGB | `a478c2818f9c720ae68e528849ef3cda2f904c9a837ef97a8018f151e655e328` |
| 147 / `_page_162_Figure_1.jpeg` | 206,693 | 1050x1155 RGB | `ab5e7bbab2a14b3d4fb832dad43842ceb4f206653810d7dfcd23238095741cfe` |
| 148 / `_page_163_Figure_4.jpeg` | 60,361 | 1121x458 RGB | `3b8879b482cc1bd331e2ac6213fa07bc962aee901564cf42163bbc2a1add4a25` |

All are JFIF 1.01, density `1x1`, with no DPI/EXIF. Filename page numbers are 15 greater than printed page numbers. Pixel dimensions are asset facts only.

### Page 160 named curves

| Function | Raster x window | Domain/segmentation | Independent anchors |
|---|---|---|---|
| `Sin[x]` | `[-15,15]` | whole real | `Sin(15)=0.6502878402` |
| `Tan[x]` | `[-10,10]` | exclude `pi/2+k*pi`; segment at poles | `Tan(10)=0.6483608275` |
| `Sec[x]` | `[-13,13]` | exclude `pi/2+k*pi`; segment at poles | `Sec(13)=1.1019929989` |
| `SinIntegral[x]` | `[-30,30]` | whole real, odd | `Si(30)=1.5667565400` |
| `BesselJ[0,x]` | `[-30,30]` | whole real, even | `J0(0)=1`; `J0(30)=-0.08636798358`; first positive root `2.4048255577` |
| `AiryAi[x]` | `[-20,5]` | whole real | `Ai(-20)=-0.1764061271`; `Ai(0)=0.3550280539`; `Ai(5)=0.00010834443` |

The windows are rendering/query presets, not mathematical domains. Near-vertical clipped `Tan`/`Sec` strokes are separate branches, not values at poles. No mesh or precision is stated.

### Page 161 sine combinations

All panels use x window `[0,250]`. The first three have y ticks at `+/-2`; the fourth at `+/-3`.

| Function | Period | Exact real-zero result on inclusive `[0,250]` | Endpoint value |
|---|---|---|---|
| `Sin[x]+Sin[3x/2]` | minimal `4*pi` | `120 = 100 + 20`; `119` strictly interior | `-1.8834855712245155` |
| `Sin[x]+Sin[10x/7]` | minimal `14*pi` | `114 = 97 + 17`; `113` strictly interior | `-1.8112988058299115` |
| `Sin[x]+Sin[sqrt(2)x]` | none | `113 = 97 + 16`; `112` strictly interior | `0.021766955859316206` |
| `Sin[x]+Sin[sqrt(2)x]+Sin[sqrt(3)x]` | none | approximately `112` inclusive / `111` interior; non-certified | approximately `-0.4812485562` |

For `Sin[x]+Sin[alpha x]`, `alpha>1`, the exact families are

```text
A_n = 2*pi*n/(1+alpha),       n >= 0
B_n = 2*pi*(n+1/2)/(alpha-1), n >= 0.
```

There are no family collisions or roots at 250 in the first three presets; all listed roots are simple. For the fourth row, an independent dense sign/critical-point search found last root approximately `248.0195005660`, minimum observed spacing `0.25134310`, and closest tested extremum to zero about `0.01224`; those are explicitly non-certified numerical observations.

### Page 162 source/query bridge to T42

Top-to-bottom source functions are:

1. `Cos[x]-Cos[(1+sqrt(2))x]`;
2. `Cos[x]-Cos[(2+sqrt(5))x]`;
3. `Cos[x]-Cos[(2+cuberoot(5))x]`;
4. `Cos[x]-Cos[(1+sqrt(e))x]`.

For coefficient `alpha`, let `r=(alpha-1)/(alpha+1)`. Then

```text
Cos[x]-Cos[alpha*x]
  = 2*Sin[(1+alpha)*x/2]*Sin[(alpha-1)*x/2]

A_n = 2*pi*n/(1+alpha), n in Z
B_m = 2*pi*m/(alpha-1), m in Z.
```

Only `x=0` overlaps for these irrational coefficients; it is a double tangent zero. Every nonzero root is simple and crossing. For the positive-axis interval word use `n,m>=0`. In the open interval `(A_n,A_(n+1))`, the B-family count is exactly

```text
c_n = floor((n+1)*r) - floor(n*r) in {0,1}.
```

T41 owns that exact count query. T42 owns interpreting `c_n` as a black/white word and generating it through substitutions. The sine-sum bridge uses the source-stated half-shift:

```text
floor((n+1)*r - 1/2) - floor(n*r - 1/2).
```

The continued-fraction anchors are:

| Coefficient | Exact/declared `r` | Continued fraction / visible terms |
|---|---|---|
| `1+sqrt(2)` | `sqrt(2)-1` | `[0; overline(2)]`; five visible `2`s |
| `2+sqrt(5)` | `(sqrt(5)-1)/2` | `[0; overline(1)]`; nine visible `1`s |
| `2+cuberoot(5)` | `0.575369381363576556...` | `[0;1,1,2,1,4,2,...]` |
| `1+sqrt(e)` | `0.451862761877606044...` | `[0;2,4,1,2,3,...]` |

The raster shows substitution steps bottom-to-top and coefficients alongside them top-to-bottom in reverse visible order. It prints no numeric x window; substitution-aligned pixel geometry cannot safely reconstruct one.

### Page 163 Riemann-Siegel curve

- One `RiemannSiegelZ[t]` curve is split into `[0,250]` and `[250,500]`, sharing `t=250`.
- Independent 50-decimal arbitrary-precision anchors are:

```text
Z(0)   = -1.4603545088095868128894991525152980124672293310126...
Z(50)  = -0.34073500595502498275331663975081487813966342667268...
Z(100) =  2.6926970566644634749953798286850324206190216376727...
Z(250) = -0.91863341835615242704537890685860604320384086356064...
Z(500) =  1.4724478510550852726639853209181484029747580350961...
```

- Independent 60-decimal arbitrary-precision enumeration found 108 positive critical-line zeros `<=250` and 269 `<=500` under the named Riemann-Siegel convention. These totals are strong numerical oracles, not certified exact counts. Zero 269 is `498.580782429686542016675082912487905...`; zero 270 is `500.309084941690495539309390725171446...`.
- The count and endpoint anchors verify the declared curve, not the raster's unspecified sampling. Main prose about all peaks/valleys is not used as an exact oracle.

### Notes-only raster inventory

These eight supplementary assets exist only under `ref/A-New-Kind-of-Science/BACK-MATTER/Index/Images/`:

| Asset | Bytes / dimensions | SHA-256 | Semantic disposition |
|---|---|---|---|
| `_page_932_Figure_6.jpeg` | 16,896 / 574x122 | `9882322b9ccf3b74542b76a719a3a8862c63e896b75e55792a68a8ea812978bf` | Five 2D/3D Lissajous specs; exact closure horizons `2*pi,4*pi,14*pi,2*pi,12*pi` |
| `_page_932_Figure_12.jpeg` | 20,617 / 575x148 | `93775e8c29085edca1f612d86f9a4df2529d07ae577472fc4a616b95edec06e0` | Complex contour observer for `Sin[z]+Sin[sqrt(2)z]`, `Re z in [0,50]`, `Im z in [-2,2]`; levels unspecified |
| `_page_932_Picture_15.jpeg` | 5,015 / 270x106 | `03e8f1c0c52fefe9567f2457b58c55b5f9875f214d973d887a1a00028a7d11f6` | Three-sine zero-spacing distribution; x-axis `0..5`; source horizon/count known, y normalization unstated |
| `_page_932_Figure_16.jpeg` | 5,044 / 277x111 | `8c6560d0ef0a383c49163c8d166165e3e42df3cbd8b5fa507ba6ec33786e1e3d` | Spacing distribution for `Sin[x]+Sin[cuberoot(2)x]+Sin[sqrt(2)x]`; horizon/y convention unstated |
| `_page_932_Figure_20.jpeg` | 9,656 / 569x93 | `7c09373aca26faa2aa83dbf9f78a63764ba23fb91f89826466058a22175b7085` | finite `sum Sin(nx)/n`, `k=2,5,25` |
| `_page_933_Figure_3.jpeg` | 9,829 / 583x96 | `d4b2db7fc6334bb39845e30ae47c901d630f68c13a5c0c500a5175e3c78da6f1` | finite `sum Sin(n^2 x)/n^2`, `k=2,5,25` |
| `_page_933_Figure_5.jpeg` | 12,510 / 584x88 | `430b3d6fd1302429d93134a3bb2fa4ed38473c16ef83325dcae459978e1d2e47` | finite `sum Cos(2^n x)`, `k=3,5,8` |
| `_page_933_Figure_7.jpeg` | 11,660 / 575x96 | `c66bce1e15f169047cd8752917168f705b88c7742c5d78fa1a2fa8b61867fc1c` | approximations to weighted infinite sums, `a=0,1/2,1`; truncation unstated; `a=0` not ordinarily convergent |

The Lissajous coordinates are `(sin t,sin 2t)`, `(sin t,sin 3t/2)`, `(sin t,sin 10t/7)`, `(sin t,sin 3t,sin 2t)`, and `(sin t,sin 5t/3,sin 3t/2)`, each with coordinate range `[-1,1]`. The last four rasters do not print an x window; a visually likely `[0,2*pi]` is not promoted to evidence.

## Variants, Relations, and Boundaries

- **Named elementary/special functions:** strict primitive calls with declared domains and versions, not arbitrary callbacks.
- **Finite sums:** exact closed expressions with explicit term count and coefficient/frequency schedule. The finite raster is not an infinite-limit claim.
- **Infinite series:** separate `SeriesFunctionSpec` with convergence domain, summation definition, and evaluator context. `a>0` weighted lacunary sums converge absolutely; displayed `a=0` needs explicit truncation/other summation.
- **Parametric/Lissajous curves:** fixed-vector codomain over one parameter. Closure horizon is an observer; irrational nonclosure is not nonhalting execution.
- **Complex zeros:** region-scoped query with multiplicity and completeness, not a two-dimensional raster or T31 constraint state.
- **ODE alternate definition:** the source-stated relation is inconsistent. A corrected relation uses `y'(0)=1+sqrt(2)` for the target, while the literal `y'(0)=2` IVP denotes `Sin[x]+Sin[sqrt(2)x]/sqrt(2)`. T45 may own differential operator/solution semantics; T41 retains the denoted closed function and explicit repair.
- **Fourier/Gibbs/spectrum:** coefficient specs and downstream observers. A transform or power spectrum does not enter function identity unless it is the declared definition.
- **Sound/FM/chords:** waveform sampling and audio rendering consume a function/query. Sample rate, duration, phase, amplitude, and codec are observer parameters.
- **T20 symbolic systems:** tree/codec responsibility can be reused; no pattern matching, rewrite pass, quiescence, or tree-update semantics apply.
- **T27 point maps:** its closed expression responsibility is reusable privately, but a map applied to mutable point-bag state is not a mathematical function query.
- **T31 constraints:** a zero equation can induce a constraint/query, but T41's function and zero result are not a solution-set state or solver callback.
- **T34 arithmetic:** exact numeric/codecs are dependencies. T41 does not repeatedly assign a scalar.
- **T39 number theory:** zeta/prime relations and exact measurements remain observers/relations; a prime sieve is not a zeta evaluator.
- **T40 digit systems:** base-digit dependence of Weierstrass values is an analysis relation, not digit state hidden inside the function.
- **T42 continued-fraction substitution:** owns coefficient expansion, symbol sequence, rule schedule, word states, and trace; T41 owns source functions and root/count queries.
- **T43 iterated maps:** owns repeated application and evolving scalar state. A T41 expression may define the map, but its denotation alone has no orbit.
- **T44 continuous CA:** owns spatial continuous-valued state and local update. A continuous codomain does not make T41 a cellular automaton.
- **T45 PDE:** owns differential equations, fields, boundary/initial conditions, solution definitions, and numerical solvers. Named special functions may be solutions without absorbing PDE execution.
- **Plot/sampling/root algorithms:** external, versioned query implementations. Their diagnostic work traces do not replace semantic definitions or prove function equality.

## Current API Fit

| Responsibility | Current document | Fit | Consequence |
|---|---|---|---|
| Persistent trajectory field and explicit time | `simple_programs.md:1-22,87-110` | `SEMANTIC MISMATCH` | T41 has a mathematical argument, not update time or stored states. |
| Fixed rank-0..3 domain/shape | `simple_programs.md:1-22,138-176` | `SEMANTIC MISMATCH` | Real/complex domains and finite query regions are not dense spacetime shapes. |
| Formulaic next-cell function | `simple_programs.md:2036-2071` | `SEMANTIC MISMATCH` | It is an unrestricted host function returning a next state, not portable closed mathematical syntax. |
| T20 ordered structural tree responsibility | completed Goal 1 design | `DIRECT` dependency | Reuse typed tree paths/codecs privately without rewrite semantics. |
| T27 closed numeric expression responsibility | completed Goal 1 design | `PARAMETERIZATION` | Share exact literals/operators where meanings agree; add named special functions, domains, branches, and query semantics. |
| T31 query/outcome/certificate separation | completed Goal 1 design | `DIRECT` responsibility | Reuse pure scoped-result discipline, but zero/evaluation result types remain distinct. |
| T34 exact numeric/codecs | completed Goal 1 design | `DIRECT` dependency | Reuse tagged arbitrary integers/rationals and exact-domain identity. |
| Function spec and numerical query algebra | no current documented component | `PRINCIPLED EXTENSION` | Add outside transition execution; no function rollout family. |
| Rendering/observers | current schema treats states as render source | `SEMANTIC MISMATCH` | Add explicit function/query adapters rather than pretending samples are trajectory state. |

## Current Runtime Fit

| Runtime element | Fit | Evidence and consequence |
|---|---|---|
| `src/ca/rules.py:25-30,64-78,316-328` `Callable`/`Rule.fn`/`formulaic` | `SEMANTIC MISMATCH` | Opaque host callables and next-state semantics fail closed identity, serialization, domains, branches, and query separation. |
| `src/ca/specs.py:23-81` `Dynamics`/`RawEpisode`/`RawBatch` | `SEMANTIC MISMATCH` | Shape, steps, rule IDs, and NumPy state arrays do not model a mathematical definition or partial evaluation result. |
| `src/ca/rollout.py:40-85,145-165` | `SEMANTIC MISMATCH` | Positive finite steps and explicit family branches would create fake time and a prohibited `functions` branch. |
| `src/ca/alphabets.py:88-126` `float_range_alphabet` | `SEMANTIC MISMATCH` | It explicitly represents a finite discretized set, not a continuous real/complex domain or error-bounded value. |
| `src/ca/loci.py:1-50,283-318` selectors | `SEMANTIC MISMATCH` | Finite rank-4 arrays and predicate callbacks cannot encode mathematical domains or certified roots; mesh selection may reuse only the responsibility split. |
| `src/ca/viz/export.py:58-72,139-184` | `SEMANTIC MISMATCH` | Export accepts episodes/batches and rejects float arrays; it has no segmented function-curve or typed undefined-value representation. |
| Existing special-function/numerical stack | `NOT APPLICABLE` | `pyproject.toml:7-10` declares only NumPy and pytest; no arbitrary-precision/special-function dependency or internal evaluator exists. |
| Existing tests | `NOT APPLICABLE` | No function-expression, domain, pole, branch, root, sampling, Lissajous, Fourier, or Riemann-Siegel conformance tests exist. |

Existing CA runtime behavior remains valid for its scope. A future viewer may accept a distinct sampled-curve payload, but native T41 conformance cannot route through `RawEpisode`, object cells, a function callback, or rule-family dispatch.

## Principles Audit

1. Evidence forces a second pure-specification/query category alongside T31/T39 pure records. Giving T41 a source/read/result/update shell would make every transition field vacuous.
2. A closed expression tree is necessary but insufficient. Domains, codomains, branches, continuation, named primitive versions, and exact parameters determine the mathematical object.
3. Numerical context belongs to a query/result, not the function. The same spec supports exact symbolic, arbitrary-precision, certified interval, and approximate evaluation without changing identity.
4. Zero finding is not sampling. Page-162's double zero and `Tan`/`Sec` poles are direct adversaries to sign-change-only logic.
5. Structural equality must stay conservative. Exact factorization proves a relation without requiring a universal simplifier or making sample equality semantic; the inconsistent ODE Note proves alternate definitions also require independent verification.
6. T42's bridge remains compositional: a pure T41 interval-count query can feed T42's closed initial/driver data, but T41 does not inherit substitution state.
7. Infinite series require convergence/summation semantics. The source's `a=0` approximation prevents a permissive infinity bound or silent truncation.
8. Named special functions can be closed primitive tags even when algorithms are complex. The source explicitly separates accepted primitives from high-precision evaluation cost.
9. The strict profiles require real/complex partiality and phase conventions. Dropping undefined/branch results to fit NumPy floats would erase mathematical distinctions.
10. No eleventh update law is added. The universal design becomes simpler by recognizing mathematical denotation and query records outside rollout.

### Re-integration audit

1. Prior assumption invalidated: none. T31 already proved that not every catalog type is a transition; T41 strengthens that categorical split.
2. Reuse: T20 tree/codec responsibilities, T27 numeric expression nodes where meanings match, T31 scoped outcomes/certificates, and T34 exact numeric codecs retain their meanings.
3. New capability: a closed mathematical-function spec, primitive registry, domain/branch profiles, and pure evaluation/zero queries. No flag, family branch, arbitrary callback, or hidden state is introduced.
4. Advance-relevant state is not applicable. Query algorithms may have internal work state, but it is implementation diagnostic data and cannot enter mathematical identity.
5. Argument space/domain, value/codomain, expression/program, query scope, numerical method, and rendering remain separated.
6. Defining formulas and named analytic continuation stay in the spec; incidental sampling, root algorithms, and evaluator cost remain external. Infinite series include their convergence definition rather than an incidental truncation.
7. The encoding preserves exact/declared coefficients, real/complex domains, partiality, branches, endpoints, multiplicity, completeness, and certification.
8. No completed stage must reopen. T20/T27/T31/T34/T39 remain valid under responsibility-level reuse.
9. Goal 2 gains shared numeric-value, mathematical-expression/function, numerical-context, query/result, function-evaluation, and curve-view work before T41 conformance; T42 consumes only a typed query result.
10. The API is more coherent because immutable definitions and pure queries no longer masquerade as CA episodes.

## Detailed Implementation Plan

1. Record the exhaustive search, eighteen evidence groups, four strict/eight Notes raster identities, source repairs, exact formulas, and independent numerical anchors.
2. Add closed function spec, primitive registry, exact numeric/branch/domain semantics, pure query/result algebra, zero events, and conservative identity/equivalence distinctions to the design inventory.
3. Record sampling, plotting, sound, spectrum, ODE, infinite-series, and analytic-solver boundaries.
4. Split page 162 clause-by-clause between T41 source/query semantics and T42 driver/update semantics.
5. Map current API/runtime/tests and write an implementation-ready Goal 2 dependency/conformance stage without callbacks, fake time, or rollout family dispatch.
6. Integrate `0-plan.md`, `evidence-index.md`, and `design-ledger.md`; run source/oracle, hash, fence, coverage, diff, and repository verification before closure.

## Goal 2 Implementation Stage

### Objective and dependencies

Implement lossless exact/declared numeric values, a versioned closed mathematical-function AST and primitive registry, real/complex domain/branch semantics, pure evaluation/sampling/zero query records, evaluator interfaces, curve observers, strict presets, and conformance tests. Depend on T20 structural tree/codecs, T27 compatible numeric expression nodes, T31 query/certificate discipline, and T34 exact numeric codecs. Do not depend on transition rollout.

### Proposed files and order

1. `src/ankos/numeric_values.py`: tagged integer/rational/named/algebraic/decimal/complex values, enclosures, and JSON codecs shared with T34/T37.
2. `src/ankos/function_expr.py`: closed expression nodes, bounded finite sums, primitive registry/versioning, arity/type/domain validation, and structural normalization.
3. `src/ankos/functions.py`: `MathematicalFunctionSpec`, argument/domain/codomain/partiality/branch profiles, IDs, and equivalence-claim records.
4. `src/ankos/numerical_context.py`: exact/arbitrary/fixed/certified modes, precision, rounding, tolerances, method IDs, resources, and deterministic metadata.
5. `src/ankos/function_queries.py`: point/sample/real-zero/complex-zero/crossing/extremum query and typed result/event/status schemas.
6. `src/ankos/function_eval.py`: evaluator registry and reference implementations; no evaluator objects in semantic specs and no generic host-call fallback.
7. `src/ankos/function_series.py`: explicit infinite-series/convergence/summation profiles after strict finite syntax is working.
8. `src/ankos/viz/functions.py`: segmented sampled-curve/contour/spacing payloads and raster adapters distinct from `RawEpisode`.
9. `src/ankos/presets/functions.py`: page-160/161/162/163 and Notes profiles, source repairs, and stable conformance IDs.
10. `tests/test_t41_functions.py`: exact structure, domain, branch, query, zero, serialization, figure oracle, boundary, and no-cheating suites.

Paths are dependency targets for synthesis; later evidence may consolidate modules, but the spec/query/result/render boundaries and conformance IDs must remain traceable.

### Required implementation behavior

- Constructors reject unknown primitive tags, wrong arity, unbound variables, inconsistent real/complex types, invalid closed domain specs, missing branch conventions, unsafe JSON numbers, unbounded finite sums, multivariate strict specs, and callbacks/host objects.
- Evaluators are selected outside the spec by explicit versioned profiles. Missing capabilities return typed failures; no library fallback silently changes semantics.
- Pole/branch/outside-domain outcomes survive serialization and sampling. Segmenters never connect across undefined intervals.
- Root results record endpoint policy, multiplicity/classification, certification, completeness, and diagnostics. Approximate sign scans cannot claim exact completeness.
- Structural IDs are deterministic and independent of sampling, evaluator, plot resolution, platform float formatting, or mutable registry order.
- Resource interruption returns the last complete certified subset or explicit partial result without altering the spec.
- T42 adapters consume a finalized T41 zero/count result with declared convention; they cannot reach into evaluator callbacks or reinterpret raster pixels.

### Canonical conformance suites

- Page 160: all six exact ASTs/windows/domains; endpoint anchors; `Tan`/`Sec` poles and segmentation; special-function declared precision.
- Page 161: exact periods, factorizations, family counts, endpoint inclusion, simple crossings, three-sine approximate/non-certified status, and sample-independence adversaries.
- Page 162: four exact source specs, factorization, `x=0` tangent, nonzero crossings, exact `r`/continued fractions/count words, and strict T41/T42 ownership.
- Page 163: analytic-continuation/phase spec, five high-precision values, independently numerical 108/269 zero counts, zero 269/270 locations, panel seam, certification labels, and no Dirichlet-series-on-critical-line shortcut.
- Notes: five Lissajous vectors/closure horizons, complex-region query, reported spacing metadata, finite sum term counts, `a>0` convergence, and rejection of ordinary infinite `a=0`.
- Equality/codec: factored versus expanded structural inequality plus certified equivalence; exact rational/algebraic round trips; declared decimal/complex/enclosure/undefined round trips; same-sample/different-function rejection.

## No-Cheating Checks

- No `Callable`, `eval`, formula string, pickle, host CAS expression, dynamic import, primitive-name reflection, or generic fallback may satisfy function-spec conformance.
- Mathematical argument traversal cannot become rollout time; no seed, frontier, rule ID, step count, or state array is required for a function.
- A sampled array, bitmap, contour, sound, zero-spacing histogram, spectrum, or cached table cannot stand in for the function definition.
- Finite viewport, mesh, raster width, root-search horizon, and requested precision never become mathematical domain or function identity.
- Binary `float` cannot silently encode exact `3/2`, `10/7`, `sqrt(2)`, `cuberoot(5)`, `sqrt(e)`, or `pi`.
- `Tan`/`Sec` pole sign changes are not zeros; plot branches are segmented and undefined points remain typed.
- A uniform/adaptive sign scan cannot certify all roots without an independent proof/isolation contract; even roots and narrow crossings are adversarial cases.
- Page-161 inclusive and interior counts must differ by exactly the declared endpoint event; a plotter cannot guess convention.
- Page-162 `x=0` must be a double tangent zero, not a crossing or two duplicate simple events.
- T42's substitution rules/steps/word cannot be embedded in T41 query state; T41's root/count result cannot be regenerated from the page-162 bitmap.
- The zeta Dirichlet series cannot be evaluated ordinarily at `1/2+it`; analytic continuation and named continuous phase are mandatory.
- A principal-`Arg` phase with jumps cannot pass `RiemannSiegelZ` conformance merely by matching isolated magnitudes.
- Infinite series must declare convergence/summation. The `a=0` raster requires explicit approximation/truncation and cannot pass as an ordinarily convergent infinite preset.
- The literal ODE initial derivative cannot certify the stated target. Conformance must distinguish the printed IVP from the corrected `y'(0)=1+sqrt(2)` relation and verify both exact solutions.
- Structural identity cannot depend on samples, tolerances, algebraic simplification by a host system, evaluator version, or rendering.
- Approximate values/results cannot lose precision/error/method metadata or be promoted to exact/certified/complete status.
- No `"functions"` rollout branch, object-cell packing, finite float alphabet, fixed four-coordinate lattice, or `RawEpisode` adapter may be the native conformance path.
- Goal 1 changes only `goal-1/`; no runtime/test/document implementation occurs during this stage.

## Completion Requirements

- [x] CSV/taxonomy identity, strict/Notes/T43 boundaries, aliases, variants, parameters, and relations are exact.
- [x] Strict main, native Notes, splits, actual Index, history, formula/evaluation relations, and all vocabulary candidates are dispositioned with zero unresolved matches.
- [x] All four strict and eight Notes rasters have identities, hashes, formulas, horizons or explicit uncertainty, source repairs, and independent anchors where possible.
- [x] Function spec, domains/codomains, exact/declared values, primitive/branch semantics, finite/infinite sums, identity, equivalence, and serialization are explicit.
- [x] Point/sample/zero/crossing/extremum queries and exact/certified/approximate/undefined/failure outcomes are explicit.
- [x] Page-160/161/162/163 presets, root conventions, T41/T42 seam, and Riemann-Siegel repairs are independently verified.
- [x] T20/T27/T31/T34/T39/T42/T43/T44/T45, ODE, sampling, plotting, sound, spectrum, and solver boundaries are explicit.
- [x] Current API/runtime fit and an implementation-ready Goal 2 file/dependency/test/no-cheating handoff are complete.
- [x] Global ledgers, exact verification commands, hashes, fence checks, coverage consistency, diff checks, and repository tests pass.

## Stage Results

- Exhaustive searches closed with zero unresolved source candidate. The direct-name union found `59/51`; formula literals `176/83`; crossing/rule mechanics `19/9`; all continued-fraction, Lissajous, Fourier/Gibbs/Weierstrass, zeta/Riemann-Siegel, music, quasiperiodic, actual-Index, history, evaluation, relation, and false-positive families are dispositioned in eighteen excerpt groups.
- All four strict and eight supplementary rasters were inspected at original resolution. Their byte sizes, dimensions, formulas, parameters, windows or explicit uncertainty, and SHA-256 hashes are recorded. The broken monolith image links, 15-page filename offset, unspecified sampling, unlabeled observer conventions, and `a=0` approximation are explicit.
- The design establishes a closed unary `MathematicalFunctionSpec` plus pure point/sample/real-zero/complex-zero/crossing/extremum queries. Exact/certified/approximate/undefined/failure values, multiplicity-aware zero events, completeness statuses, proofs/diagnostics, and rendering payloads stay separate from definitions and from transition execution.
- Exact values, real/complex definition domains, scalar/fixed-vector codomains, primitive versions, partiality, analytic continuation, poles, branch conventions, ordered structural identity, certified equivalence, lossless codecs, bounded finite sums, and explicit infinite-series profiles are implementation-ready.
- Page 161's first three exact inclusive root counts are `120/114/113` with interior counts one lower; the approximate three-sine observation is correctly non-certified. Page 162's four functions, factorizations, double tangent at zero, nonzero crossings, continued fractions, and interval-count bridge are pinned without absorbing T42 state.
- The ODE Note was independently falsified as printed: derivative `2` yields `Sin[x]+Sin[sqrt(2)x]/sqrt(2)`, while the stated target needs `1+sqrt(2)`. Zeta's critical-line continuation, named continuous Riemann-Siegel phase, five 60-decimal values, and numerical `108/269` zero totals are likewise explicitly repaired/qualified.
- Independent arbitrary-precision verification reported `T41 exact/declared-precision oracle: PASS; three-sine observed roots inclusive=112` and `T41 ODE source-repair oracle: PASS`. Focused search controls reproduced `mathematical functions 56/48`, strict/Notes image links `4/4` and `8/8`, and the native no-update/no-sampling result.
- SHA-256 verification reproduced all twelve recorded asset hashes. Markdown fence parity passed for this stage and all `goal-1/*.md`; `git diff --check -- goal-1` passed.
- Repository verification passed: `uv run pytest -q` reported `102 passed in 1.19s`.

## Integration Results

- `0-plan.md` now records the non-transition function/query category, exact source/figure repairs, implementation-ready stage result, 16/45 completed types, and T43 as next work.
- `evidence-index.md` records T41 complete with exact search counts, eighteen evidence groups, four strict/eight Notes rasters, all semantic/boundary/runtime obligations, and zero unresolved candidates; coverage is 16/45.
- `design-ledger.md` adds the T41 construction record, function/denotation inventory category, D082-D087, current-dimension refinements, source-derived rejection criteria, open-question updates, and completed integration entry. The transition family remains at ten update laws.
- T20/T27/T31/T34/T39 were re-audited and remain valid under responsibility-level reuse. No completed stage reopened. Next: T43 Iterated Maps.
