# 14-T34-ARITHMETIC

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T34, CSV line 35, `Arithmetic Iteration Systems`; taxonomy seed `ref/notes/CA-Types.md:937-964`. The taxonomy supplies search vocabulary, not authoritative mechanics.
- The native state is one number advanced by repeated arithmetic, not a cell field. Digit rows, curves, value plots, lengths, and fractional-part plots are candidate observers until the primary text proves otherwise.
- T35 piecewise integer maps begins at taxonomy section 35 and is a separate branch-selected construction. T34 must not absorb it merely because both evolve one scalar.
- Canonical prose, figures, Notes, Index routes, exact arithmetic domains, presets, termination/cycle behavior, rendering semantics, repository fit, and conformance oracles remain under active audit.

## Updated Assumptions

- Exact integer and rational arithmetic will be preferred wherever the source specifies it; finite-precision and arbitrary real behavior will not be conflated without evidence.
- Arithmetic updates will be represented as closed structural data rather than unrestricted host-language callbacks.
- State equality and trace semantics will be defined on the scalar values. Representation-base digits and display geometry will remain downstream unless a rule explicitly reads them.
- Horizon, cycle detection, overflow/resource limits, and rendering policies will remain distinct from the mathematical recurrence.

## Big Picture Objective

Reconstruct arithmetic iteration as a native scalar transition construction. Pin down number domains, closed operations, seeds, exactness, successor and outcome semantics, trajectory representation, digit/value renderings, canonical examples, termination and cycle observations, relations to piecewise maps and other scalar systems, and the smallest honest extension of the shared runtime.

## Catalog Identity

- Stable ID: T34.
- Exact name: Arithmetic Iteration Systems.
- CSV provenance: `ref/notes/CA-Types.csv:35`; taxonomy provenance: `ref/notes/CA-Types.md:937-964`.
- Canonical section, Notes, actual Index, figures, programs, and construction boundary: under audit.

## Search Log

1. Verified the CSV/taxonomy identity and read the complete taxonomy seed.
2. Opened parallel audits for primary figures, Notes/Index/search coverage, and architecture/runtime fit.
3. Remaining exhaustive searches and disposition counts are in progress.

## Book Excerpts

Canonical excerpt groups are under audit.

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

The mathematical transition remains total even when a concrete evaluator runs out of memory or time. `ResourceLimit`, cancellation, invalid input, and backend error are operational outcomes outside the successor algebra and must retain the last complete exact state. A finite horizon returns `HorizonReached` after exactly the requested number of events; it does not relabel the last value as terminal.

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
- Exact integers serialize as signed decimal integers; exact rationals serialize as normalized numerator/positive-denominator pairs.
- Program tags and constants serialize as closed data; host function names, source code, pickles, and lambdas are forbidden.
- Exact and finite-precision values never compare equal across domain tags merely because a displayed decimal agrees.
- A whole trace compares its exact state sequence and events. A rendering, crop, base, color palette, padding choice, or plotted curve is not part of trace equality.
- Cycles and fixed points are detected on exact normalized state values. Rounded-display equality cannot establish recurrence.

### Digit and numeric observers

The figures make observers important, but no observer feeds back into the recurrence.

`IntegerDigitRow(base)` requires `base >= 2` and returns the most-significant-to-least-significant digits of a nonnegative exact integer. The sign, if permitted by an extended view, is separate metadata. Leading blank cells used for alignment are not zero digits and are not state.

`RationalDigitWindow(base, integer_places, fractional_places, repeat_policy)` renders a declared finite window around an explicit radix point. A rational has a terminating base-`b` expansion only when the reduced denominator divides some power of `b`; otherwise the exact expansion repeats indefinitely and the observer must either report a repeating cycle or use an explicit finite crop. It may never invent a finite exact row by truncation.

Digit arrays declare:

- base and digit order;
- time direction and whether `x_0` is included;
- alignment anchor: least-significant integer place or radix point;
- integer/fractional place interval;
- blank-versus-zero padding;
- crop side and whether omitted digits exist;
- color map, grid, labels, and interpolation as presentation only.

`FractionalPart(x) = x - floor(x)` is an exact scalar observer in `[0,1)` and is independent of display base. `DigitLength(base)`, population count, rightmost-`s` residue, numeric value, logarithmic size, leading digit, and digit-frequency statistics are other observers. Line segments and gray fill in a plot are decoration; the sampled points alone are values.

Reducing after each event modulo `b^s` creates a finite quotient system/linear congruential generator. It exactly reproduces the rightmost `s` digits of an integer multiplication trace, but the quotient state is a different program and cannot replace the unbounded T34 scalar. Likewise, a digit-level cellular automaton can be an exact compiler target for special multiplier/base pairs, not native T34 state.

## Exact Book Presets and Oracles

### Constant addition

The page-117/118 figures use exact seed `x_0=1`, base-2 digit rows, and operations `AddConstant(c)` for `c=1,2,...,8`. For every such preset:

```text
x_t = 1 + c*t
```

The `c=1` figure visibly lists states `1` through `63`; its first sixteen rows must decode as:

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

## Variants, Relations, and Boundaries

T35 branching integer maps, digit systems, iterated maps, continuous systems, substitution systems, and cellular automata are under audit as relations rather than assumed flags.

## Current API Fit

The repository API audit is in progress.

## Current Runtime Fit

The repository runtime audit is in progress.

## Principles Audit

No conclusions are closed until scalar state, exact arithmetic, closed programs, rendering boundaries, and source-complete evidence have been checked.

## Detailed Implementation Plan

1. Complete all primary-source, figure, Notes, Index, program, history, and relation searches.
2. Derive the minimal closed scalar-arithmetic operation and number-domain algebra.
3. Specify deterministic event, outcome, trace, equality, serialization, exactness, and resource semantics.
4. Reconstruct every canonical preset and independently verify numeric and rendering anchors.
5. Audit current APIs/runtime/tests and record the smallest Goal 2 integration.
6. Add adversarial no-cheating checks, update the global ledger/evidence/plan, and verify the repository.

## Goal 2 Implementation Stage

The implementation handoff is pending the evidence audit.

## No-Cheating Checks

The final suite must at minimum reject opaque arithmetic callbacks, digit-state conflation, silent floating-point substitution for exact arithmetic, hidden stop/cycle rules, T35 branching smuggled into T34, and rendering-dependent transitions.

## Completion Requirements

- [ ] Every native main-text, figure, Notes, actual Index, program, history, and relation candidate is dispositioned.
- [ ] Number domains, closed operations, seeds, transition/outcome semantics, equality, traces, and observers are explicit.
- [ ] Every canonical preset has independently checked exact anchors and adversarial tests.
- [ ] T34/T35 and all neighboring construction boundaries are explicit.
- [ ] Current API/runtime fit and Goal 2 work are implementation-ready.
- [ ] Design ledger, evidence index, global plan, diff checks, and tests are integrated.

## Stage Results

In progress.

## Integration Results

In progress.
