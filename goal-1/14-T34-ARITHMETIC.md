# 14-T34-ARITHMETIC

Status: **REOPENED — ARCHITECTURE AUDIT; EVIDENCE CLOSED**

The evidence/search closure and conformance fixtures remain valid. T34 is a `t+0D` closed unary-map preset over an exact numeric value carrier and generic assignment, not a separate scalar executor.

## Current Facts

- Exact catalog row: T34, CSV line 35, `Arithmetic Iteration Systems`; taxonomy seed `ref/notes/CA-Types.md:937-964`. The taxonomy supplies search vocabulary, not authoritative mechanics.
- The book never uses the catalog title. The scoped source construction is the first part of Chapter 4 `Elementary Arithmetic`, `BOOK:1439-1495`; `Systems Based on Numbers` is a Chapter 4 umbrella and `arithmetic systems/recurrences` generally route to T35.
- Native state is one exact scalar. The strict program repeatedly applies one fixed `AddConstant` or `MultiplyConstant`; seed `1`, addends `1..8`, multipliers `2`, `3`, and `3/2` are canonical presets.
- Digit rows, digit counts/frequencies/lengths, leading digits, numeric/log-size plots, residues, and fractional parts are observers. Base, radix alignment, crop, padding, palette, and plot lines are not state and never feed back.
- The canonical exact carriers are arbitrary-precision integers and reduced rationals. The main text supplies no fixed-precision-real preset; general real/irrational Notes require an explicit exact or declared numerical domain rather than host floats.
- Every valid strict event has exactly one successor and no native halt. Identity, fixed points, or principled negative-factor cycles remain eventful; horizon and resource failure are external.
- The add-one image contains states `1..63`; the add-constant panels contain 84 rows; the two short integer-multiplication panels contain 64 rows; the long powers-of-three view contains 500 rows and is cropped only in presentation; the `3/2` digit view contains 256 exact rational rows.
- T35 begins semantically at `BOOK:1497-1503` when parity selects an arithmetic branch. T36 makes digits/base rule-visible, T37/T38 store numeric history, and T43 feeds a nonlinear/fractional interval map back into the state.
- Rightmost-digit truncation yields an explicit finite `MultiplyMod`/linear-congruential sibling. Special digit/base pairs can compile to cellular automata. Neither replaces unbounded T34.
- No canonical T34 `NestList` implementation is printed; the first such program in the Notes is already the T35 parity branch at `BOOK:12598`.
- The current `formulaic` callback, modular AR2, temporal 0D neighborhoods, fixed NumPy dtypes, family rollout, finite alphabets, and rectangular raw episodes do not implement this construction. Generic typed assignment responsibilities and T19/T27 exact-number work can be reused.
- Exact textual, Notes, actual-Index, split, history, program, alias, relation, and figure audits have zero unresolved T34 candidates.

## Updated Assumptions

- Exact integer/rational arithmetic is semantic in the strict profiles. Finite-precision and arbitrary exact-real behavior are separate typed domains and never silent implementation modes.
- Public arithmetic updates are the closed structural sum `AddConstant | MultiplyConstant`, not unrestricted host-language callbacks or a generic affine/expression AST.
- Typed state identity is domain-tagged; cross-domain numeric equivalence is an observer. Program identity is structural, so extensionally identical `Add(0)` and `Multiply(1)` remain distinct.
- State-sequence equality, full trace identity, and visual equality are different relations.
- Exact big integers and rational components serialize as decimal strings, avoiding JSON/JavaScript precision loss.
- Representation-base digits and display geometry remain downstream. The explicit `MultiplyMod` quotient is a related program, not a view flag.
- Horizon, fixed/cycle observers, overflow/resource outcomes, precision contexts, and rendering policies remain distinct from the mathematical recurrence.
- A fast closed-form/random-access evaluator may reuse associativity and repeated squaring but cannot fabricate or skip requested trace events.

## Big Picture Objective

Reconstruct arithmetic iteration as a native scalar transition construction. Pin down number domains, closed operations, seeds, exactness, successor and outcome semantics, trajectory representation, digit/value renderings, canonical examples, termination and cycle observations, relations to piecewise maps and other scalar systems, and the smallest honest extension of the shared runtime.

## Catalog Identity

- Stable ID: T34.
- Exact name: Arithmetic Iteration Systems.
- CSV provenance: `ref/notes/CA-Types.csv:35`; taxonomy provenance: `ref/notes/CA-Types.md:937-964`.
- Canonical main section: `Elementary Arithmetic`, strict core `BOOK:1439-1495`; clean duplicate `CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:43-99`.
- Native Notes: `BOOK:12538-12597`; the T35 implementation begins at `12598`. Supporting relations are grouped in E09-E31 below.
- Entry kind: deterministic unary scalar transition construction with a fixed closed arithmetic operation.
- Strict profiles: constant addition over exact integers; constant multiplication over exact integers; exact rational multiplication by `3/2`.
- Explicit sibling/relation: finite residue-ring `MultiplyMod`; certified-real/declared-precision domains are constrained extensions rather than strict presets.
- Aliases/vocabulary: elementary arithmetic, arithmetic process, systems based on numbers, add/addition/successive numbers/binary counter, multiply/multiplication/powers, `2`, `3`, `3/2`, integer/rational/real, digit sequence/base/radix/carry, fractional part/size/length/leading digit, `IntegerDigits`, `Mod`, linear congruential, repeated squaring/power CA, locality/nonlocality, exactness/precision, and the neighboring names dispositioned below.

## Search Log

1. Verified CSV line 35, read taxonomy section 34 in full, and used it only to seed vocabulary. The exact book phrase `Arithmetic Iteration Systems` has `0` occurrences.
2. Read canonical Chapter 4 framing/core `BOOK:1370-1503`, clean duplicate lines `1-107`, every extracted page-117 through page-122 raster, native Notes `BOOK:12538-12597`, and the first T35 Notes/program line `12598`.
3. The direct-name union `Arithmetic Iteration Systems|Systems? Based on Numbers?|Elementary Arithmetic|Arithmetic Systems?|Arithmetic Process(?:es)?|Arithmetic Recurrences?` found 65 occurrences on 55 lines: 52/43 before the actual Index and 13/12 in it. All 55 lines were classified. Six pre-Index lines are strict/core, 20 are Chapter 4 umbrella context, three are direct T34 relations, nine are T35, five are other constructions/false positives; every Index line was routed. Zero unresolved.
4. Component counts were: exact title `0/0`; `Systems? Based on Numbers?` `39/35` (35/31 pre-Index, 4/4 Index); `Elementary Arithmetic` `3/3`; `Arithmetic Systems?` `20/16` (13/9 pre, 7/7 Index); `Arithmetic Process(?:es)?` `1/1`; `Arithmetic Recurrences?` `2/2`, both Index.
5. A conservative mechanics query for progressively/successively adding, successively multiplying, powers of `2/3/3/2`, multiplication factors, and fractional parts found 27 occurrences on 26 lines: 26/25 pre-Index and 1/1 Index. It classified 8/7 strict-main hits, 2/2 native Notes hits, 3/3 T34 relations, 13/13 lexical geometry/growth false positives, and one Index hit. Zero unresolved.
6. A focused native query for the exact add/multiply phrases, first 500 powers, `IntegerDigits[3^n,2]`, and `Mod[(3/2)^n,1]` found 13 occurrences on 12 pre-Index lines: 10/9 main, one RNG relation, and 2/2 Notes. The exact code/observer union for integer/real digits, power rows, fractional parts, residues, and digit-cell formulas found 6/6 pre-Index lines at `7388,12503,12507,12559,12565,12570`.
7. The actual Index begins at `BOOK:20826`. Resolved direct routes for powers `3`/`3/2`, addition/multiplication in digit sequences, arithmetic processes/nonlocality, bases 2/6/10, binary counters, digit sequences, LCGs, numbers, powers, reversibility, uniform distribution, and all mixed umbrella hits. The misnamed split `BACK-MATTER/Index/Index.md:402-500` is a Notes duplicate, not the Index; the actual split Index is OCR-interleaved under `BACK-MATTER/Colophon/Colophon.md:3383+`.
8. Followed substitution/counter relations `BOOK:4260,12054,12117-12122`; random-generator relation `3722-3744`; power formulas/local CAs/repeated squaring `7380-7424`; CA emulation `7974-7980`; nonlocal arithmetic `1531-1537,8828-8842`; reducibility `9058,9080`; exact digit codecs `12503-12513`; T43 precision boundary `13217-13247`; reversibility `16066-16072`; and power/evaluation-chain material `17849-17920`.
9. Searched executable/reference forms `IntegerDigits[3^n,2]`, `Mod[(3/2)^n,1]`, `Mod[3^n,2^s]`, and `Mod[Quotient[m^t,k^n],k]`. No T34 `NestList` program exists. Logged OCR corruption in the inverse digit fold near `12505` and power fold near `17857`; used surrounding prose, clean duplicates, mathematics, and independent generated values as guards rather than treating damaged token strings as APIs.
10. Read `simple_programs.md`, every relevant `src/ca` module, tests, prior T19/T27 decisions, and the completed construction ledger. Classified `UniqueScalar`/typed assignment as responsibility-level reuse and every current finite/callback/history/dense execution route as mismatch or not applicable.
11. Independent exact arithmetic regenerated the add, multiply, `3/2`, fractional, suffix-period, overflow, crop, and rendering anchors in this stage. Exact T34 mechanics have zero unresolved textual/Notes/Index/search candidates.
12. Checked the official Chapter 4 programs CDF against the Notes/reference formulas. It confirms the implementation/CA relations and contains no hidden main-figure generator or additional T34 update mechanic.

Representative reproducible commands used `rg -n -i` over the monolith with the regex unions above, `awk -F: '$1 >= 20826'` to isolate the actual Index, `sed`/`nl` for every context range, `rg --files` for splits/rasters, `view_image` for all seven canonical images, and exact `python3` integer/`Fraction` calculations for independent oracles.

## Book Excerpts

`BOOK` below means `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`. These groups separate native mechanics from observers, exact quotients, compilers, and neighboring constructions.

### E01 — Numbers and digit representations are distinct

- Provenance: `BOOK:1390-1437`, Chapter 4 opening.
- Fact: a number is treated abstractly by size but represented in a computer by digits in a base. Operations change those digit sequences, and different bases expose different patterns. This motivates digits as views; it does not make the digit cells the native state.

### E02 — Fixed addition from seed one

- Provenance: `BOOK:1439-1451`, printed page 117; `_page_132_Figure_10.jpeg`.
- Fact: start at `1`, repeatedly add `1`, and include the initial value in the displayed succession. The exact scalar values are simple while their right-aligned base-2 rows form a nested pattern. The raster lists `1..63`.

### E03 — Addition constants one through eight

- Provenance: `BOOK:1453-1457`, printed page 118; `_page_133_Picture_2.jpeg`.
- Fact: all eight panels start at `1` and use `n -> n+c` for visible labels `c=1..8`. Independent pixel/digit extraction finds 84 rows, `t=0..83`; terminal values are `84,167,250,333,416,499,582,665`. Their different fine structure shares the stated nested organization.

### E04 — Multiplication by two and three

- Provenance: `BOOK:1459-1469`, printed page 119; `_page_134_Figure_2.jpeg`, `_page_134_Figure_3.jpeg`.
- Fact: both 64-row panels start at one. Multiplication by two shifts a base-2 row left and appends zero; multiplication by three produces the exact rows for `3^t` and a visually complex pattern. Shift behavior is a representation fact, not a different update.

### E05 — Five hundred complete powers of three with a cropped view

- Provenance: `BOOK:1471-1483`, printed page 120; `_page_135_Figure_2.jpeg`.
- Fact: the native row is the complete base-2 expansion of `3^t` for the first 500 powers. The page crops the expanding left side; the underlying integer does not truncate. Width grows with average slope `log_2(3)`.

### E06 — Exact rational multiplication

- Provenance: `BOOK:1475-1489`, printed page 121; `_page_136_Figure_2.jpeg`.
- Fact: starting at one and repeatedly multiplying by exact `3/2` yields `1,3/2,9/4,27/8,...`. The 256-row base-2 view aligns the radix point: integer digits lie to its left and fractional digits to its right. Division by two shifts places right, but the scalar update remains multiplication by `3/2`.

### E07 — Fractional part is a base-independent observer

- Provenance: `BOOK:1491-1495`, printed page 122; `_page_137_Figure_1.jpeg`.
- Fact: the plotted dots are the fractional parts of successive powers of `3/2`. The source explicitly says the samples are independent of representation base and that connecting lines/shading are visual aids only.

### E08 — T35 begins at the first branch

- Provenance: `BOOK:1497-1503`, printed page 122.
- Fact: the next example tests parity and chooses different formulas. Its state is still one integer, but predicate-controlled branching is construction-defining and belongs to T35. The shared section heading does not erase this semantic boundary.

### E09 — Substitution relation and digit-count observer

- Provenance: `BOOK:4260`, `12117-12122`, and `12538-12548`, Notes to page 117.
- Fact: the add-one digit picture is a rotated substitution-system pattern. The black-cell count on row `n` is `DigitCount[n,2,1]`, with stated bounds and formulas. Both are derived descriptions of the digit view, not extra arithmetic state.

### E10 — Alternative numeral systems

- Provenance: `BOOK:12503-12513,12550-12557`.
- Fact: the Notes give whole-number `IntegerDigits`/`FromDigits` intent and a bounded fractional-digit codec, then discuss negative bases, non-power positional weights, and multiplicative prime-factor digit sequences. The sideways negabinary image spans integers `-42..85`, the range representable with at most seven shown digits; multiplicative digits are shown through 100. Non-power representations may be nonunique, and the bounded real-digit inverse is only approximate. These require explicit view codecs and cannot silently redefine state equality. OCR damage near `12505` is not treated as executable syntax.

### E11 — Exact powers-of-three row formula and statistics

- Provenance: `BOOK:12559-12563`.
- Fact: row `n` is exactly `IntegerDigits[3^n,2]`. The fraction of ones appears to approach one half, and suffix columns repeat with a period growing exponentially in the retained width. Apparent randomness/frequency claims are observers, while the row formula is an exact oracle.

### E12 — Finite suffix quotient

- Provenance: `BOOK:12563-12565`.
- Fact: the rightmost `s` columns are `3^n mod 2^s`, a linear congruential generator with geometric regularities. This justifies an explicit finite quotient/observer relation and forbids hidden truncation of the native power trace.

### E13 — Special local CA lowering for powers of three

- Provenance: `BOOK:12567` and `BOOK:7382-7406`.
- Fact: in base six, multiplying by three admits a six-color local CA rule. The general later discussion gives the digit formula `Mod[Quotient[m^t,k^n],k]`, says only special base/multiplier pairs eliminate arbitrarily propagating carries, and supplies other examples. Locality is conditional on the representation pair.

### E14 — Leading digits

- Provenance: `BOOK:12569`.
- Fact: leading digits of powers follow a logarithmic rather than uniform distribution. This is a scalar-trace statistic and never selects a successor.

### E15 — Exact fractional formula and qualified uniformity

- Provenance: `BOOK:12570`.
- Fact: the page-122 sample is exactly `Mod[(3/2)^n,1]`. Uniform distribution is reported as suggested by measurements and still unproved, so it cannot be a required finite-run invariant.

### E16 — Base-six CA relation for `3/2`

- Provenance: `BOOK:12572-12578`.
- Fact: the Notes give an invertible base-six CA formula for `(3/2)^n` and discuss special multipliers `u`. This is an exact representation/compiler relation with a separate CA initial field, not evidence that the arithmetic state contains a digit lattice.

### E17 — General real powers

- Provenance: `BOOK:12580`.
- Fact: the fractional parts of `h^n` are discussed for general real `h`, including exceptional Pisot numbers. This supports a domain-polymorphic arithmetic construction only when exact/approximate real semantics are declared; statistical theorems do not supply a finite real codec.

### E18 — Irrational additive orbits and substitution codings

- Provenance: `BOOK:12581-12595`.
- Fact: `Mod[h*n,1]` repeats for rational `h` and is nonrepeating/uniform for irrational `h`. Difference codings can be generated by substitution schedules derived from continued fractions, with fixed substitutions for quadratic irrationals. These are fractional/difference observers and T42 relations over the underlying addition trace.

The corresponding Notes figure uses `h=11/17`, `sqrt(2)`, `GoldenRatio`, and `cuberoot(4)`; only the rational case repeats.

### E19 — Other uniform sequences are relations, not T34 presets

- Provenance: `BOOK:12597`.
- Fact: `sqrt(n)`, `n log n`, `log(Fibonacci[n])`, and other sequences can also be uniformly distributed modulo one. They are not obtained by the strict fixed-add/fixed-multiply program merely because they share an observer statistic.

### E20 — Notes boundary to piecewise integer maps

- Provenance: `BOOK:12598-12640`.
- Fact: the Notes implementation from `12598` onward uses `If[EvenQ[...]]`, discusses 3n+1 variants, cycles, reconstruction, and reversible branches. Those are T35 evidence. None supplies a halt/cycle condition or branch to T34.

### E21 — Linear congruential random-number relation

- Provenance: `BOOK:3718-3752`, Chapter 7.
- Fact: repeated multiplication followed by retention of the rightmost 31 base-2 digits creates finite repeating generators and visible higher-dimensional regularities. The truncation/modulus is precisely why the generator differs from unbounded multiplication.

### E22 — Direct power evaluation and computational reducibility

- Provenance: `BOOK:7408-7424`, `9058-9080`, and `17849-17920`.
- Fact: a digit at time `t` has a direct power formula, and exponentiation by squaring computes a requested power using the bits of `t`. A later powers-of-two example contrasts random-access work with explicit row-by-row evolution; the evaluation-chain material explicitly uses start-one/add-one and fixed multiplication and exploits associativity. The OCR-damaged fold near `17857` is repaired from the surrounding mathematics. These support a separate exact query evaluator, not altered event semantics.

### E23 — CA emulation with explicit carry machinery

- Provenance: `BOOK:7968-7980` and counter relation `BOOK:12054`.
- Fact: a cellular automaton with 11 colors emulates repeated multiplication by three in base two; its complication propagates carries. Separately, a Turing machine can display reversed successive-number digits as a binary counter. Both require added representation/control state and do not collapse T34 into T01 or T12.

### E24 — Arithmetic over digit sequences is generally nonlocal

- Provenance: `BOOK:1531-1537` and `8828-8842`.
- Fact: carries in addition can propagate arbitrarily far, and general functions can make almost every input digit affect almost every output digit. This directly rules out assuming a finite digit neighborhood from scalar arithmetic syntax.

### E25 — Historical/exactness context

- Provenance: `BOOK:12532-12536`.
- Fact: practical computations require explicit finite representations while continuum approximations can break down in complex behavior. The Notes trace digit-system history and distinguish whole, rational, and continuous numbers. Numeric representation/precision must therefore be explicit in an implementation.

### E26 — Actual Index routes

- Provenance: actual monolith Index beginning near `BOOK:20826`.
- Fact: direct routes include `3, powers of` to pages 119/903; `3/2, powers of` to 121/903; `Addition ... in digit sequences` to 118; `Arithmetic ... processes of` to 117; `Arithmetic ... non-locality of` to 124/731; `Base 6, powers of 3 in` to 614/903; `Binary counter ... pattern made by` to 117; `Uniform distribution ... of powers` and `... of multiplicative sequences` to 903; and `Linear congruential generators` routes to the Chapter 7/Notes material. Every route resolves to a group above or a separately dispositioned relation.

### E27 — Source repairs and figure authority

- Provenance: clean split `CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:1-115`; local original rasters for extracted pages 132-137.
- Fact: the canonical monolith's base-representation table is OCR-damaged, while the clean split repairs formulas and image paths. The rasters recover panel labels, row counts, radix alignment, and crop facts absent from prose. Canonical claims retain `BOOK` provenance; the split and raster are explicit repairs/independent guards.

### E28 — No canonical T34 evolution program

- Provenance: `BOOK:12598` immediately after the native Notes range.
- Fact: the first explicit `NestList` implementation under the `Elementary Arithmetic` Notes is already the parity-selected T35 rule. T34 supplies exact formulas/observers but no host callback to copy, strengthening the closed add/multiply algebra rather than weakening it.

### E29 — Fixed precision changes scalar-map behavior

- Provenance: `BOOK:13217-13247`, iterated-map Notes.
- Fact: finite stored digits and machine arithmetic can change exact real-map behavior. These passages belong to T43, but they establish why a finite-precision T34 extension must be separately typed and cannot silently implement exact `(3/2)^t`.

### E30 — Reversibility follows the operation

- Provenance: `BOOK:16066-16072`.
- Fact: systems based on numbers can be reversible when their operation is invertible; the page-121 multiplication by `3/2` reverses by division by `3/2`. Reversibility is a property/observer and does not add backward state or a second forward successor.

## Construction Model

### Semantic object

A strict arithmetic-iteration run is determined by:

```text
ArithmeticIterationProgram = {
    domain: ScalarDomain,
    operation: AddConstant(c) | MultiplyConstant(c)
}

ArithmeticRun = {
    program: ArithmeticIterationProgram,
    initial: ScalarValue(program.domain),
    event_count: Natural
}
```

Its state at event index `t` is one scalar `x_t`. There is no spatial support, alphabet of digit cells, cursor, head, branch control, mutable program, boundary condition, or hidden arithmetic accumulator. The canonical source is `UniqueScalar`, its read is the complete old scalar, the result is `Assign(ScalarSlot, x_next)`, and atomic single-slot replacement commits it. Thus T34 needs a scalar carrier and a closed arithmetic rule algebra, but not a ninth update law.

The two evidenced operations have exact semantics:

```text
step(AddConstant(c),      x) = x + c
step(MultiplyConstant(c), x) = x * c
```

The operation is the same at every event. `c`, the old value, and the result must all belong to the declared domain. There is no implicit modulus, truncation, saturation, rounding, base conversion, conditional branch, or change of constant.

### Scalar domains and exactness

The strict book presets use exact integers and rationals:

```text
ExactInteger  = arbitrary-precision signed integer
ExactRational = normalized (numerator: Integer, denominator: PositiveInteger)
```

An `ExactInteger` program accepts only integer initial values and constants. An `ExactRational` program accepts normalized rationals, with integers embedded canonically as denominator one. Rational normalization uses positive denominator and coprime numerator/denominator; `1/2` and `2/4` therefore serialize and compare as the same value.

The Notes also discuss general real multipliers and irrational additive orbits. That establishes a principled domain-polymorphic extension, not permission to use host floats silently. An exact-real profile must supply a closed, canonical, equality-preserving representation and total exact addition/multiplication for its admitted values, such as a certified algebraic-number domain. A declared finite-precision profile is a separate numerical approximation:

```text
DeclaredFinitePrecision = {
    radix, precision, rounding_mode, exponent_bounds,
    literal_provenance, overflow_policy
}
```

Its rounded state sequence is not semantic equality with an exact-real trajectory. NaN, infinity, subnormal handling, overflow, and rounding occur only according to the declared context. Arbitrary Python floats, tolerance equality, backend-default precision, and exact-to-approximate coercion are invalid.

Supporting negative or zero seeds/constants is a principled closure of exact addition and multiplication; all canonical main-text presets use positive seed `1` and positive constants. Any renderer for negative values must make the sign explicit rather than treating two's-complement width as native state.

### Validation and closed program identity

Validation is structural and occurs before execution:

- the domain tag is known and its value codec is canonical;
- the operation is exactly one closed algebra member;
- the constant and initial value belong to the same declared domain;
- exact rationals are finite and normalized;
- finite-precision contexts declare every rounding/overflow parameter;
- the requested event count is a nonnegative integer;
- no callable, expression evaluator, predicate, conditional arm, modulus, digit window, or stop test is embedded in the strict program.

Program identity is the tagged domain plus the normalized operation constant. A run identity additionally includes the normalized initial value. Event horizon and all observer settings are execution/view requests, not mathematical program identity.

Identity is structural and domain-tagged. `ExactInteger(1)` and `ExactRational(1/1)` may be related by an explicit cross-domain numeric-equivalence observer, but they are not the same typed state. Likewise, `AddConstant(0)` and `MultiplyConstant(1)` remain distinct programs even though both induce identity transitions.

### Event semantics and outcomes

One event is evaluated against one immutable old scalar:

```text
proposal = ArithmeticAssignment(
    source=UniqueScalar,
    old=x_t,
    operation=program.operation,
    value=step(program.operation, x_t),
)
x_(t+1) = proposal.value
```

Every valid strict exact event has exactly one successor. An identity event—`AddConstant(0)`, `MultiplyConstant(1)`, or multiplication of zero—still returns `Advanced(changed=false)` and records an event. There is no native halt, fixed-point stop, cycle stop, digit-width cap, target magnitude, or convergence threshold. Those are observers or run policies.

The mathematical transition remains total even when a concrete evaluator runs out of memory or time. `ResourceExhausted`, `Cancelled`, invalid input, and `BackendFailure` are operational outcomes outside the successor algebra and must retain the last complete exact state. A completed finite request returns `RequestedIterationsCompleted` after exactly the requested number of events; it does not relabel the last value as terminal.

### Trace and time indexing

For `event_count = h`, the reference trace contains `h+1` states:

```text
states = (x_0, x_1, ..., x_h)
events = (e_0, e_1, ..., e_(h-1))
```

The seed is `x_0`, and event `e_t` maps `x_t` to `x_(t+1)`. This explicit convention guards the current runtime's ambiguous use of `steps` as a requested number of serialized states. A trace uses arbitrary-precision tagged scalar values, not NumPy fixed-width integers or floats. Batches may share a program but do not pad digit rows or coerce values merely to become rectangular.

For the evidenced operations, independently computed closed forms provide conformance or random access:

```text
AddConstant(c):      x_t = x_0 + t*c
MultiplyConstant(c): x_t = x_0 * c^t
```

Fast exponentiation may answer a random-access query without replaying `t` events, but it does not change event semantics or erase intermediate states from a requested trace.

### Equality and serialization

- State equality is exact numeric equality within the declared scalar domain.
- Exact integers serialize in JSON as signed decimal **strings**, never lossy JSON number literals; exact rationals serialize as tagged normalized numerator/positive-denominator decimal-string pairs.
- Program tags and constants serialize as closed data; host function names, source code, pickles, and lambdas are forbidden.
- Exact and finite-precision values never compare equal across domain tags merely because a displayed decimal agrees.
- Trace identity includes program/run provenance, exact states, exact events, and the typed run outcome. State-sequence equality is a separate observer and may hold for structurally different programs such as the identity operations. A rendering, crop, base, color palette, padding choice, or plotted curve is not part of either comparison.
- Cycles and fixed points are detected on exact normalized state values. Rounded-display equality cannot establish recurrence.

### Digit and numeric observers

The figures make observers important, but no observer feeds back into the recurrence.

`IntegerDigitRow(base)` requires `base >= 2` and returns the most-significant-to-least-significant digits of a nonnegative exact integer. The sign, if permitted by an extended view, is separate metadata. Leading blank cells used for alignment are not zero digits and are not state.

`RationalDigitWindow(base, integer_places, fractional_places, repeat_policy)` renders a declared finite window around an explicit semantic radix position. A raster may visually omit the radix mark, as page 121 does, but metadata cannot. A rational has a terminating base-`b` expansion only when the reduced denominator divides some power of `b`; otherwise the exact expansion repeats indefinitely and the observer must either report a repeating cycle or use an explicit finite crop. It may never invent a finite exact row by truncation.

Digit arrays declare:

- base and digit order;
- time direction and whether `x_0` is included;
- alignment anchor: least-significant integer place or radix point;
- integer/fractional place interval;
- blank-versus-zero padding;
- crop side and whether omitted digits exist;
- color map, grid, labels, and interpolation as presentation only.

`FractionalPart(x) = x - floor(x)` is an exact scalar observer in `[0,1)` and is independent of display base. `DigitLength(base)`, population count, rightmost-`s` residue, numeric value, logarithmic size, leading digit, and digit-frequency statistics are other observers. Line segments and gray fill in a plot are decoration; the sampled points alone are values.

Reducing after each event modulo `b^s` creates the explicit sibling `MultiplyMod(multiplier, modulus=b^s)` over a finite `ResidueRing`. It exactly reproduces the rightmost `s` digits of an integer multiplication trace, but the quotient state/program is different and cannot replace the unbounded T34 scalar. It is also not the current second-order modular AR2 family. Likewise, a digit-level cellular automaton can be an exact compiler target for special multiplier/base pairs, not native T34 state.

## Exact Book Presets and Oracles

### Constant addition

The page-117/118 figures use exact seed `x_0=1`, base-2 digit rows, and operations `AddConstant(c)` for `c=1,2,...,8`. For every such preset:

```text
x_t = 1 + c*t
```

The `c=1` figure has 63 rows, `t=0..62`, and visibly lists states `1` through `63`; its first sixteen rows must decode as:

| `t` | `x_t` | base 2 |
|---:|---:|---|
| 0 | 1 | `1` |
| 1 | 2 | `10` |
| 2 | 3 | `11` |
| 3 | 4 | `100` |
| 4 | 5 | `101` |
| 5 | 6 | `110` |
| 6 | 7 | `111` |
| 7 | 8 | `1000` |
| 8 | 9 | `1001` |
| 9 | 10 | `1010` |
| 10 | 11 | `1011` |
| 11 | 12 | `1100` |
| 12 | 13 | `1101` |
| 13 | 14 | `1110` |
| 14 | 15 | `1111` |
| 15 | 16 | `10000` |

At `t=31`, the `c=1..8` values are respectively `32,63,94,125,156,187,218,249`, with rows `100000`, `111111`, `1011110`, `1111101`, `10011100`, `10111011`, `11011010`, and `11111001`. These anchors catch an off-by-one seed, reversed digit order, and accidental update-by-row-label.

The eight-panel page-118 image contains 84 rows, `t=0..83`. Its final values/rows are:

```text
c=1:  84 = 1010100       c=5: 416 = 110100000
c=2: 167 = 10100111      c=6: 499 = 111110011
c=3: 250 = 11111010      c=7: 582 = 1001000110
c=4: 333 = 101001101     c=8: 665 = 1010011001
```

### Integer multiplication

The page-119/120 presets use `x_0=1` and `MultiplyConstant(2)` or `MultiplyConstant(3)`. Their exact state is `x_t=2^t` or `3^t`. The first eleven base-2 rows are:

| `t` | `2^t` row | `3^t` row |
|---:|---|---|
| 0 | `1` | `1` |
| 1 | `10` | `11` |
| 2 | `100` | `1001` |
| 3 | `1000` | `11011` |
| 4 | `10000` | `1010001` |
| 5 | `100000` | `11110011` |
| 6 | `1000000` | `1011011001` |
| 7 | `10000000` | `100010001011` |
| 8 | `100000000` | `1100110100001` |
| 9 | `1000000000` | `100110011100011` |
| 10 | `10000000000` | `1110011010101001` |

For multiplier two, each event appends one zero in base 2. For multiplier three, row width is `floor(t*log_2(3))+1`; the 500-row figure is cropped on the left and therefore cannot be decoded as a bounded integer state. The complete exact row remains `IntegerDigits(3^t,2)`.

Both page-119 panels have 64 rows, `t=0..63`. Their last values are `2^63 = 9223372036854775808`, represented by one followed by 63 zero bits, and `3^63 = 1144561273430837494885949696427`, a 100-bit integer. The former is already one beyond the maximum signed 64-bit value. The page-120 long view uses `t=0..499`; its last complete row has 791 bits even though the page omits its left portion. Exact `3^499` crop guards are prefix `111011100011111000011101` and suffix `100111011111010001011011`.

For a rightmost eight-bit observer, the first sixteen residues of `3^t mod 256` are:

```text
1, 3, 9, 27, 81, 243, 217, 139,
161, 227, 169, 251, 241, 211, 121, 107
```

The sequence has exact period `64`. This is an observer/quotient oracle; the unbounded powers themselves never repeat.

### Rational multiplication by `3/2`

The page-121/122 preset is exact `x_0=1`, `MultiplyConstant(3/2)`, with `x_t=3^t/2^t`. Its first twelve exact rows are:

| `t` | exact value | exact base-2 form |
|---:|---:|---|
| 0 | `1` | `1` |
| 1 | `3/2` | `1.1` |
| 2 | `9/4` | `10.01` |
| 3 | `27/8` | `11.011` |
| 4 | `81/16` | `101.0001` |
| 5 | `243/32` | `111.10011` |
| 6 | `729/64` | `1011.011001` |
| 7 | `2187/128` | `10001.0001011` |
| 8 | `6561/256` | `11001.10100001` |
| 9 | `19683/512` | `100110.011100011` |
| 10 | `59049/1024` | `111001.1010101001` |
| 11 | `177147/2048` | `1010110.01111111011` |

The radix-aligned page-121 raster has 256 rows, `t=0..255`; its inset shows `t=0..15`. The final numerator `3^255` has 405 binary digits, split into 150 whole-number and 255 fractional places by the denominator `2^255`. Its final rational is exactly `3^255/2^255`; no finite-precision decimal trajectory can substitute for it.

The fractional-part plot is exactly:

```text
f_t = (3^t mod 2^t) / 2^t = FractionalPart((3/2)^t)
```

Its first sixteen values are:

```text
0, 1/2, 1/4, 3/8, 1/16, 19/32, 25/64, 11/128,
161/256, 227/512, 681/1024, 1019/2048,
3057/4096, 5075/8192, 15225/16384, 29291/32768
```

Changing the digit-rendering base must not change these rational samples. The source reports apparent uniformity as an unproved measurement claim; it is not a verifier oracle.

Pixel/value matching shows the page-122 graph contains 201 dots, `t=0..200` inclusive. Its final sample is:

```text
301238419698178094330228735350577461155754011486333945032865
/
1606938044258990275541962092341162602522202993782792835301376
```

This is exactly `(3^200 mod 2^200)/2^200`, approximately `0.187461128806`; using only 200 samples or shifting the seed to `t=1` is an off-by-one failure.

### Required metamorphic oracles

1. Iterative and closed-form evaluation agree for random exact seeds, constants, and horizons.
2. Decoding every uncropped canonical digit row returns the exact scalar state.
3. Base 2, base 3, and base 10 renderings of one trace decode to identical states.
4. Cropping the left side of an integer multiplication row preserves every retained rightmost residue and reports omitted digits.
5. Changing plot interpolation, color, or padding does not change state or samples.
6. `event_count=h` returns exactly `h+1` states and `h` events, including `h=0`.
7. Identity operations advance and record events without triggering a fixed-point halt.
8. Values beyond `2^63` remain exact; a fixed-width NumPy overflow is a test failure.
9. Rational normalization makes `3/2`, `6/4`, and `-3/-2` the same constant and trace.
10. An approximate context cannot compare equal to or silently replace the exact `3/2` preset.
11. `(2^k-1)+1 = 2^k` for large `k`, forcing an arbitrarily long carry without changing scalar event semantics.
12. Exact `1/3` in base two renders with repetend `01`, not as a finite exact digit row.
13. `MultiplyConstant(-1)` has an observed two-cycle for a nonzero seed but never stops natively.

## Variants, Relations, and Boundaries

### Native profiles and principled closure

- Fixed addition and fixed multiplication over exact integers/rationals are the strict evidenced core.
- Seed `1`, addends `1..8`, multipliers `2`, `3`, and `3/2`, and base-2 observations are canonical presets, not hard-coded executor branches.
- Other exact seeds/constants, including zero and negative values, are a principled closure of the same total operations when the declared domain is closed under them.
- Certified exact-real and declared finite-precision real domains are separate scalar profiles. They share the unary event shape only when their arithmetic/equality contracts are explicit.
- Fractional part, digit length/count/frequency, leading digits, residues, and numeric/log-size plots are observers.
- Negative bases, non-power positional systems, and multiplicative digit decompositions are alternative representation schemes. They do not change an addition or multiplication program.

### Quotients, direct formulas, and compilations

`x -> c*x mod b^s` is a finite modular quotient of integer multiplication. It reproduces a declared suffix of the digit observation and is useful as a linear congruential generator, but it discards higher digits and has cycles absent from unbounded `c^t`. Modulus and truncation therefore cannot be hidden performance options on T34.

The formulas `x_0+t*c` and `x_0*c^t` and exponentiation by squaring provide random-access evaluators. They are observationally equivalent at requested times; they do not redefine one recurrence event as a variable number of squarings.

For certain multiplier/base pairs, digit rows lower exactly to a local cellular automaton—for example multiplier three in base six. Other cases require carry propagation, and multiplication by three in base two can be emulated using a larger-state CA. These are compilers/emulations with explicit state/trace mappings, not proof that T34 is a finite-alphabet lattice program.

The nested add-one digit picture is related to a substitution pattern, and some irrational additive-orbit codings can be generated by continued-fraction-driven substitutions. Equality of a derived digit pattern does not identify the scalar recurrence with T13 or T42.

### Catalog boundaries

| Related type/construction | Shared part | Required separation |
|---|---|---|
| T01 elementary CA | deterministic events and typed assignment | fixed spatial lattice, finite alphabet, local neighbor read, simultaneous many-site commit |
| T13 substitution | some digit pictures have substitution descriptions | symbol sequence is rewritten/grown; scalar arithmetic and carries are not the substitution state |
| T19 register machine | arbitrary-precision integer carrier and typed slot assignment | multiple named registers plus program counter and branching instructions |
| T27 geometry | exact rational/algebraic/declared-precision scalar infrastructure | T34 has one numeric state, not occurrence bags/poses |
| T35 piecewise integer maps | same scalar carrier/source/effect shell | predicates and ordered arithmetic branches are rule-visible and begin at `BOOK:1497-1503` |
| T36 digit-reversal arithmetic | same integer carrier and digit codecs | base and digit transformation feed back into the next state |
| T37 recursive sequences | numeric values and fixed-lag formulas can reproduce powers | native state is a growing prefix/history and update appends a term |
| T38 variable-index recursion | numeric sequence values | data-dependent earlier-term addressing requires a growing prefix and guarded computed indices |
| T39 number-theoretic filters | integer arithmetic | filters/streams/sets of candidates, not one scalar successor |
| T40 constant digits | number representations | expansion procedure has no repeated mutable scalar update in the base case |
| T41 function combination | exact/approximate numeric expressions | native object is a function/curve; samples and crossings are observations |
| T42 continued-fraction substitution | irrational parameters and symbolic observers | coefficient stream schedules changing substitution rules |
| T43 iterated maps | unary scalar source, exactness concerns, assignment | broader nonlinear/piecewise interval maps and infinite-information real states need their own closed map algebra |
| T44 continuous CA | continuous values | fixed lattice, local aggregation, and parallel field update |
| T45 PDE | numeric fields | continuous space/time derivative constraint plus solver/discretization category |
| Linear congruential RNG | multiplication suffix quotient | finite modulus is semantic state loss; randomness tests/distributions are observers |

T34 is consequently neither “all formulaic 0D rules” nor “anything whose picture is made of digits.” Its closed operation and scalar-domain invariants are narrow enough to make exactness, totality, and serialization checkable.

## Current API Fit

| Responsibility | Current mechanism | Fit for T34 |
|---|---|---|
| Semantic domain | `Dynamics.domain="t+0d"` and rank-zero coordinate convention | `PARAMETERIZATION` only for the idea of one temporal scalar locus; current dense coordinate/tensor carrier is not exact scalar state |
| Values | finite `Alphabet`, contiguous integer/float families | `SEMANTIC MISMATCH`; T34 needs unbounded exact integers/rationals and explicit real contexts, not a finite alphabet |
| Source/frontier | fixed rank-zero site can act as one update site | `DIRECT` responsibility-level reuse as `UniqueScalar`; no spatial frontier policy is needed |
| Read | `self_at(0)` concept plus temporal `history` neighborhoods | current-value self read is conceptually direct; `ar2_0d`, `dyadlags_0d`, and `lagcounts_0d` are mismatches because T34 reads no older slice |
| Rule | `Rule`, `formulaic(fn)`, family strings, `rule_id` instantiation | `SEMANTIC MISMATCH`; add a closed `AddConstant`/`MultiplyConstant` algebra, never an unrestricted callable or sampled rule ID |
| Update | scalar result written to the current rank-zero slot | `DIRECT` typed assignment/atomic commit responsibility; no new update law |
| Seed | `pair`, `uniform_pair`, binary history seeds, ndarray rendering | `SEMANTIC MISMATCH`; use one normalized typed scalar run input |
| Boundary | boundary mapping normalized in `Dynamics` | `NOT APPLICABLE`; one scalar has no spatial edge |
| Episode | `RawEpisode(states: ndarray, rule_id, ...)` | `SEMANTIC MISMATCH`; fixed dtype cannot preserve large integers/rationals and `rule_id` is not program identity |
| Horizon | rollout `steps` means number of returned states | needs an explicit `event_count`/`state_count` split to avoid off-by-one ambiguity |
| Visualization | t+0D value plotting/export accepts integer NumPy arrays and rejects non-integers | reusable only downstream after typed scalar export; lacks rational/digit-window/radix/crop semantics |
| Exact scalar infrastructure | T19 arbitrary naturals and T27 rational/algebraic/precision design obligations | `PRINCIPLED EXTENSION` with substantial reusable value/codecs, while signed domains and arithmetic programs remain T34 work |
| Dataset/RNG | fixed family registry, finite rule pools, NumPy seed streams | `NOT APPLICABLE` to native semantics; later dataset plans must sample closed programs/values without changing them |

`simple_programs.md` allows a scalar `t+0D` address and `FORMULAIC`, but its finite state/alphabet assumptions and unrestricted formula route are not a sufficient construction. The source/read/result/update responsibilities survive; the current public data model does not.

## Current Runtime Fit

- `src/ca/rules.py:316-366` exposes an unrestricted `formulaic` callback and a special `ar2_modular_0d` family. The latter reads two temporal values, computes a second-order recurrence modulo `m`, decodes parameters from a finite rule ID, and is T37-like rather than T34.
- `src/ca/neighborhoods.py:617-685` makes temporal history explicit for AR2/dyad-lag/count-lag rules; none expresses the sole current-scalar read as a typed arithmetic program.
- `src/ca/rollout.py:157-198,334-574` dispatches by family and materializes fixed NumPy arrays. It will overflow or coerce the canonical unbounded/rational traces and cannot be retained as the T34 implementation path.
- `src/ca/specs.py:117-173` admits only current named Phase-1 rule/neighborhood families and carries irrelevant boundary/alphabet fields through `Dynamics`.
- `src/ca/seeds.py:136-179` defines two-value scalar history seeds rather than one typed exact initial value.
- `src/ca/specs.py:58-81` and visualization/export code treat raw episodes as rectangular arrays with an integer rule ID. Exact rational tags, arbitrary integer widths, operation identity, and ragged digit observations are absent.
- Existing tests demonstrate current mechanics only: modular AR2, binary temporal lookup/count bands, dtype validation, and basic t+0D plotting. None is evidence for `x+c`, `c*x`, exact `3/2`, observer independence, or unbounded growth.

Goal 2 should add closed scalar values/programs and route them through the generic typed executor responsibilities. It must not add `if family == "arithmetic"` to the current rollout or store a `Fraction`, Python function, digit string, or big integer in an object cell merely to pass the old array interface.

## Principles Audit

### Principle 0 — re-derive rather than preserve

T34 validates the general source/read/result/update responsibility split but rejects finite alphabets, temporal-history reads, current formula callbacks, modular AR2, dense fixed-width traces, and family dispatch. A single scalar slot with exact closed arithmetic is simpler and more faithful.

### Principle 1 — preserve meaning

The state is the number, not whichever digits happen to be visible. The operation is fixed arithmetic, not a bitmap transform. Exact and approximate domains, unbounded and modular systems, native recurrence and CA compilation, event traces and direct formulas, and values and renderings all remain separately typed.

### Principle 2 — closed and inspectable data

Programs are tagged constants and values are canonical tagged numbers. There are no lambdas, evaluator strings, predicates, backend-default floats, hidden modulus/width, or render-time feedback. Exact equality and program identity are serializable and replayable.

### Principle 3 — no hidden state or policy

The only Markov state is `x_t`. Time is a trace index; a recurrence need not store it. Horizon, cycle/fixed-point detection, resource limits, numeric context, radix, crop, padding, and plot styling are explicit run/observer inputs. There is no implicit carry buffer or cached exponent in semantic state.

### Principle 4 — test the construction, not a picture

Tests decode rows back to exact values, compare iterative and closed-form traces, cross rendering bases, exceed machine widths, check rational normalization, and distinguish quotient/approximate variants. Pixel resemblance alone is insufficient.

## Detailed Implementation Plan

1. Complete all primary-source, figure, Notes, Index, program, history, and relation searches.
2. Derive the minimal closed scalar-arithmetic operation and number-domain algebra.
3. Specify deterministic event, outcome, trace, equality, serialization, exactness, and resource semantics.
4. Reconstruct every canonical preset and independently verify numeric and rendering anchors.
5. Audit current APIs/runtime/tests and record the smallest Goal 2 integration.
6. Add adversarial no-cheating checks, update the global ledger/evidence/plan, and verify the repository.

## Goal 2 Implementation Stage

### Stage A — exact scalar values

1. Add normalized arbitrary-precision signed integer and rational value codecs, domain membership, exact comparison/hash, and JSON-safe serialization.
2. Reuse compatible T19/T27 numeric infrastructure rather than create arithmetic-only duplicate types.
3. Define an explicit certified-exact-real interface and declared finite-precision context boundary; implement only profiles whose equality/arithmetic contract is actually available.

### Stage B — closed arithmetic programs

4. Add `ArithmeticIterationProgram(domain, AddConstant|MultiplyConstant)` with structural validation and stable identity.
5. Add one typed scalar initial-value run input. Reject callables, branch predicates, modulus, representation fields, and mixed domains.
6. Evaluate through `UniqueScalar -> CurrentScalar -> ArithmeticAssignment -> atomic Assign`, reusing generic assignment/effect responsibilities without a family switch.

### Stage C — outcomes and traces

7. Add an arbitrary-precision typed scalar trace with `h+1` states and `h` events, exact event provenance, and `Advanced(changed)` semantics.
8. Keep horizon, cancellation, resource exhaustion, invalid input, and backend failures separate. Preserve the last complete exact state on operational interruption.
9. Provide optional exact random-access evaluation from the closed forms, checked against iterative stepping.

### Stage D — observers

10. Add integer digit rows and rational digit windows with explicit radix, place range, alignment, blank/zero padding, sign, repeating/truncation, and crop metadata.
11. Add exact fractional-part, residue, digit-length/count/frequency, numeric/log-size, and leading-digit observers. Never mutate or round the source trace.
12. Export typed scalar traces and ragged digit rows to visualization without squeezing them into current finite NumPy state arrays.

### Stage E — conformance

13. Implement the addition `c=1..8`, multiplication `2/3`, 500-row powers-of-three, exact `3/2`, fractional sequence, modulo-suffix, horizon/identity, overflow, normalization, and rendering metamorphic oracles in this stage.
14. Add negative tests for T35 predicates, T36 digit feedback, T37 history recurrence, T43 nonlinear maps, modular quotient substitution, and CA lowering masquerading as T34.
15. Retain current Phase-1 tests during refactoring, but do not treat them as T34 evidence or add an arithmetic rollout branch.

## No-Cheating Checks

- No unrestricted host callback, expression evaluator, pickle, or family-name dispatch.
- No finite rule ID used to encode an unbounded arithmetic constant/program.
- No digit string, raster row, fixed-width bit vector, or object-typed NumPy cell masquerading as the scalar state.
- No finite alphabet used to claim exact unbounded integers or rationals.
- No `int64`/`uint64` overflow, saturation, wrap, or implicit modulus.
- No silent float conversion of exact integers/rationals and no tolerance equality.
- No undeclared precision, rounding, exponent range, NaN, infinity, or platform-dependent decimal parsing.
- No temporal-history seed/read for a first-order scalar recurrence.
- No hidden time counter, carry register, cached power, digit width, or radix in semantic state.
- No representation base, crop, padding, palette, interpolation, or plot scale affecting `x_(t+1)`.
- No trailing/leading blank cell reinterpreted as a significant zero digit.
- No truncation of a repeating rational expansion labeled exact.
- No two's-complement width selected implicitly for negative numbers.
- No fixed-point/cycle/target/digit-width/magnitude stop added to the native program.
- No horizon endpoint mislabeled as a mathematical halt.
- No identity operation collapsed into an event-free stutter.
- No direct `x_0*c^t` evaluator changing trace event counts or inventing intermediate events.
- No left-cropped powers-of-three image presented as the complete numeric state.
- No modulo suffix quotient presented as the unbounded multiplication program.
- No CA emulation/local multiplier-base special case presented as native arithmetic state.
- No substitution description of a digit picture presented as native scalar evolution.
- No ordered predicate/update arms from T35 hidden in a generic formula.
- No base-sensitive digit transformation from T36 admitted as plain arithmetic.
- No prior-term buffer from T37 packed into one nominal scalar.
- No nonlinear/fractional-part interval map from T43 smuggled into the strict add/multiply sum.
- No weakening of current tests or duplicate T34-only assignment/executor primitive.

## Completion Requirements

- [x] Every native main-text, figure, Notes, actual Index, program, history, and relation candidate is dispositioned.
- [x] Number domains, closed operations, seeds, transition/outcome semantics, equality, traces, and observers are explicit.
- [x] Every canonical preset has independently checked exact anchors and adversarial tests.
- [x] T34/T35 and all neighboring construction boundaries are explicit.
- [x] Current API/runtime fit and Goal 2 work are implementation-ready.
- [x] Design ledger, evidence index, global plan, diff checks, and tests are integrated.

## Stage Results

T34 is complete. The direct-name union found 65 occurrences on 55 lines, conservative mechanics 27/26, focused native forms 13/12, and exact code/observer forms 6/6. Thirty excerpt groups cover the scoped main core, all seven canonical main figures, Notes figures, Notes/programs/history, actual Index/splits, exact and approximate domain boundaries, nonlocality, representations, suffix quotients, CA/substitution/counter relations, reversibility, and fast evaluation. Every candidate is classified and strict mechanics have zero unresolved gaps.

The reconstruction is one domain-tagged exact scalar plus a closed `AddConstant | MultiplyConstant` program. It uses `UniqueScalar`, a complete current read, `ArithmeticAssignment`, and the existing atomic typed assignment update. Every valid event has one successor, including identity events; no halt, boundary, modulus, capacity, digit base, or cycle stop is native. Exact integers/rationals, decimal-string codecs, structural program identity, typed trace/outcomes, and explicit exact/declared numerical profiles close the value model.

The page-117 through page-122 oracles pin 63 add-one rows, 84 rows for each addend `1..8`, 64 short power rows, 500 complete powers of three behind a left crop, 256 exact `3/2` rows, and 201 exact fractional samples. Independent `python3` integer/`Fraction` checks passed for all listed sequences/endpoints, 791-bit `3^499` crop guards, `3^255` bit length, exact `f_200`, and the 64-period eight-bit suffix. `git diff --check -- goal-1` passed, Markdown fences are balanced, and `uv run pytest -q` passed all 102 tests in 1.18 seconds.

## Integration Results

`design-ledger.md` now records T34, D064-D069, scalar/value/source/read/result/update/outcome/trace inventory changes, rejected numeric/rendering shortcuts, and the completed integration entry. `evidence-index.md` records T34 complete and 13/45 completed types. `0-plan.md` records the stage result and T37 as next.

T19/T27 numeric obligations and the generic typed assignment/effect responsibility are reused without changing meaning. T34 adds no ninth update law, family branch, callback, hidden state, or dense packing. `MultiplyMod`, direct powers, CA/substitution encodings, and all digit/value views remain distinct. T35/T36/T37/T38/T43 boundaries are sharper; no prior stage is contradicted or reopened.
