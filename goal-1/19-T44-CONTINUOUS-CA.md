# 19-T44-CONTINUOUS-CA

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T44, CSV line 45, `Continuous Cellular Automata`; taxonomy vocabulary is `ref/notes/CA-Types.md:1215-1245`. T45 begins at taxonomy line 1247.
- Canonical strict main `Continuous Cellular Automata` is `BOOK:1948-2014`; T45 begins at `2016`. The clean chapter duplicate is `Systems-Based-on-Numbers.md:405-471`, with T45 at 473.
- Native Notes are `BOOK:13281-13315`; T45 Notes begin at `13316`. The useful line-oriented duplicate is `BACK-MATTER/Index/Index.md:1184-1217`, with T45 at 1219. The actual Index begins at `BOOK:20826`.
- The strict construction is a fixed one-dimensional lattice with a gray value at every cell and discrete synchronous time. Each event reads the old left/self/right values, forms their average, applies one fixed scalar mapping, and assigns the result to the same cell in parallel.
- Strict value language is continuous gray from white `0` through black `1`. This is a real interval, not a finite float alphabet or a rendered gray palette.
- The three strict map profiles are identity on the average, `FractionalPart[3 average/2]`, and `FractionalPart[average+c]`; the displayed additive family includes exact `c=1/4` and a parameter gallery.
- The average-only profile is linear diffusion. The `3/2` profile composes T44 neighborhood aggregation with T43 strict map `(a)`. The constant-add profile has a uniform background `FractionalPart[c t]`, but nonuniform deviations can be complex.
- A single black cell on white background is the strict seed. Program, initial field, boundary/realization, requested horizon, numerical profile, and rendering remain separate.
- Notes implementation maps a scalar function over `(RotateLeft[list]+list+RotateRight[list])/3` and uses `NestList`, directly supporting old-snapshot averaging, simultaneous assignment, and initial-inclusive traces.
- `RotateLeft`/`RotateRight` implements a finite periodic-list realization. Whether the strict native figures instead denote the ordinary infinite line with a finite crop/light cone must be resolved from rasters and CA context rather than silently inferred from the implementation helper.
- T01 already establishes fixed-lattice all-site old-snapshot reads and atomic parallel assignment. T44 appears to reuse that public update law with exact/declared real values, a closed aggregate-plus-map rule, and a new continuous value carrier; no new update law is presumed.
- T43 supplies reusable scalar map-expression and numerical-realization responsibilities, but T44 is not a packed collection of independent T43 states: every new cell value depends on a neighborhood aggregate.
- Native Notes state that exact rationals are essential for detailed profiles: ordinary 64-bit double precision makes the lower page-157 pattern qualitatively wrong and nearly every page-160 parameter panel wrong. Numerical realization therefore affects feedback semantics over the whole field.
- The strict source exposes a potential two-level realization identity: the ideal exact field construction and a fully declared finite-arithmetic field recurrence. T43's ideal/tracked/fixed distinction must be lifted without conflating cell values, computation work state, or rendered gray levels.
- The `c=1/4` background repeats every four events. Notes generalize this to rational `c`, with period equal to the reduced denominator; irrational `c` never repeats. Background periodicity is an observer/property, not a native halt.
- Notes add an additive profile `Mod[RotateLeft[list]+RotateRight[list],1]`. With a single nonzero value `1/k`, it relates coefficients to Pascal's triangle and finite versus equidistributed value sets. The displayed formula/text's exact normalization and possible reciprocal/modulus defect are under audit.
- Parameter scans, center-cell plots, background plots, adjacent-cell differences, localized-structure views, value equality, and pattern classes are observers. The page-175 difference image cannot replace the underlying field.
- Coupled map lattices/lattice dynamical systems are a historical related family. Probabilistic cellular automata are explicitly an alternative discrete-value stochastic construction, not a T44 flag.
- T45 removes discrete cells and discrete time and must remain a distinct continuous-space/time differential-equation category. A finite-difference approximation or PDE limit is a relation, not T44 native identity.
- Six strict image links and two native-Notes image links are identified. Their dimensions, hashes, grids, constants, horizons, exact pixels, source repairs, and missing/cropped status are under parallel audit.
- Current finite lattice selectors and parallel assignment are closer to T44 than to T43, but current alphabets discretize floats, current rules admit callbacks, current rollout uses family branches/NumPy rounding, and current exporters treat arrays/renders as the public result. Exact continuous-field semantics are absent.

## Updated Assumptions

- Strict ideal state is a total field from a declared 1D lattice support into exact/certified values in `[0,1]`, with no control or stored history.
- A finite periodic list, a finite open segment, an infinite line with finite-support/default presentation, a causal window, and a rendered crop are distinct realizations/scopes.
- `AllSites` is the active source. Each site reads the complete ordered old triple `(left,self,right)`, computes an exact average, applies one closed scalar expression, and returns a typed same-site assignment. All results commit atomically.
- Aggregation order, rational divisor `3`, map expression, exact parameter, interval/endpoints, boundary, and numeric realization are reproducible data. They are not a formula callback or backend default.
- Source-spelled `FractionalPart` retains the T43/Wolfram `x-IntegerPart[x]` semantics. Strict aggregate/map arguments are nonnegative, where it agrees with modulo one; the additive Notes profile explicitly uses `Mod[...,1]` and remains a distinct primitive.
- Ideal exact field state, certified/tracked computation state, and fixed represented field state remain different. Per-operation rounding locations include addition, division/average, map arithmetic, comparison, and assignment.
- An unchanged field still represents a completed event. Diffusive convergence, exact background periods, repeated finite realizations, localized structures, and observer horizons do not halt the base construction.
- A complete run with `h` events has `h+1` field snapshots. Compact events may reconstruct fields, but a bitmap/float tensor is not the semantic codec.
- Exact field equality, realized-field equality, translational equivalence, observer equality, and visual equality are distinct.
- Parameter-family scans execute separately identified rules/runs. The parameter coordinate is not hidden control and a gallery is not one evolving field.
- Additive, coupled-map, stochastic, PDE-limit, higher-dimensional, alternate-neighborhood, weighted-average, and asynchronous profiles will be admitted only to the extent supported by evidence.

## Big Picture Objective

Reconstruct continuous cellular automata as exact or explicitly represented continuous-valued lattice evolution: fixed support, old-neighborhood aggregate, closed scalar map, parallel same-site commit, explicit boundary/seed/numerical realization, exact figures and parameter profiles, observer boundaries, T01/T43 composition, and the smallest honest Goal 2 extension without finite-float alphabets, callbacks, or a continuous-CA rollout branch.

## Catalog Identity

- Stable ID: T44.
- Exact CSV name: `Continuous Cellular Automata` at `ref/notes/CA-Types.csv:45`.
- Taxonomy vocabulary: `ref/notes/CA-Types.md:1215-1245`; search seed only.
- Canonical strict main: `BOOK:1948-2014`; clean duplicate `Systems-Based-on-Numbers.md:405-471`.
- Native Notes: `BOOK:13281-13315`; line-oriented duplicate `BACK-MATTER/Index/Index.md:1184-1217`.
- Entry kind: synchronous one-dimensional continuous-valued lattice transition construction with neighborhood aggregation followed by a scalar map.
- Strict profiles: mean/diffusion; fractional `3/2` mean; fractional mean-plus-constant family; single-black-cell seed; value/difference/parameter observers.
- Supplementary profiles: additive modulo-one rules, exact/approximate realizations, coupled map lattices, finite periodic implementation, irrational parameters, and PDE/probabilistic relations.
- Aliases/routes under audit: continuous cellular automata, continuous-valued/real-valued CA, coupled map lattices, lattice dynamical systems, analog CA, additive continuous rules, gray-level automata, diffusion/averaging CA, Kaneko lattices, local maps, totalistic continuous rules, and finite-difference relations.

## Search Log

Canonical shorthand in this stage is `BOOK=ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`. Searches used `rg -oi` for occurrence counts and `rg -in` for distinct matching-line counts, split before the actual Index at line 20826:

```bash
sed -n '1,20825p' "$BOOK" | rg -oi 'PATTERN' | wc -l
sed -n '1,20825p' "$BOOK" | rg -in 'PATTERN' | wc -l
tail -n +20826 "$BOOK" | rg -oi 'PATTERN' | wc -l
tail -n +20826 "$BOOK" | rg -in 'PATTERN' | wc -l
```

| Controlled vocabulary | Pre-Index occurrences/lines | Actual Index occurrences/lines | Disposition |
|---|---:|---:|---|
| `continuous cellular automata?` | 34/31 | 2/2 | Every line inspected |
| `continuous CAs?\b` | 0/0 | 20/18 | Every multi-column Index line resolved |
| `coupled map lattices?|lattice dynamical systems?` | 2/1 | 2/2 | Historical aliases and redirects |
| `CCAEvolve(?:Step|List)` | 3/3 | 0/0 | Native implementation |
| `Rotate(?:Left|Right)\[list\]` | 5/3 | 0/0 | Periodic finite realization/additive rule |
| Local-average phrase union | 8/7 | 0/0 | Strict law and applications |
| Aggregate/fixed-map phrase union | 3/3 | 0/0 | T01/T43 composition |
| Four exact `FractionalPart[...]` forms | 4/3 | 0/0 | Strict profiles/Notes |
| `1/4|a\s*=|1\.13` controlled parameter union | 15/13 | 0/0 | Gallery, background, weighted variant |
| Background/cycle union | 4/4 | 0/0 | Exact property |
| Exact/machine-precision union | 6/2 | 0/0 | Numeric-feedback semantics |
| Additive/Pascal union | 2/2 | 1/1 | Supplementary rule/property |
| Probabilistic-CA union | 9/6 | 2/2 | Explicit alternative |
| Finite-difference/PDE union | 7/7 | 0/0 | T45 relation/boundary |
| Noisy-continuous-rule union | 4/3 | 0/0 | Stochastic sibling |
| Complex/block union | 2/2 | 0/0 | Distinct block extension |
| `continuous-valued|real-valued` aliases | 0/0 | 0/0 | No local-book alias hit |

The 31 pre-Index direct-name lines are `1948,1960,1982,1986,2002,2008,2014,2018,2036,2102,2878,2880,2884,2890,2904,3784,3804,13281,13283,13296,13314,13401,14234,14237,15074,15075,15644,15864,16237,17002,19072`. They resolve as follows:

- `1948-2014` is the strict construction; `2018` is the T45 boundary and `2036` its diffusion-limit relation. `2102` is only a PDE resemblance.
- `2878-2904`, `14234`, and `14237` supply parameter/class studies, random seeds, adjacent-difference views, and the neighbor-weight variant.
- `3784-3804` and `15074-15081` supply explicit perturbation/noisy continuous-rule siblings.
- `13281-13314` is native implementation/history/property/variant evidence; `13401-13403` is the PDE numerical boundary.
- `15644` is a genuine boiling preset. `15864` is only a phyllotaxis list analogy. `16237` is terminology/history without construction mechanics.
- `17002-17008` is a complex unitary block extension. `19072` is the state-cardinality property.

The two exact-name Index hits are the main entry at `BOOK:21046` and the lattice-dynamical redirect at `21434`. All 18 abbreviated `continuous CA` Index lines were followed: valid routes occur at `20972,21080,21086,21189,21195,21223,21405,21471,21475,21497,21711,21771,21815,21990,22352`; `20914,21735,21805` are multi-column collisions. In particular, the apparent “Particle accelerators for continuous CAs” at `21735` is not a sentence. Body/Notes resolve the intended parameter and precision routes. Zero textual candidate remains unresolved.

Separate searches over `simple_programs.md`, `src/ca`, and `tests` for the exact name, aliases, `CCAEvolve`, `FractionalPart`, Pascal, exact rational, and precision policy found no T44 implementation or conformance test. The current-code matches used for fit analysis are recorded below rather than counted as book evidence.

## Book Excerpts

### E1 — Continuous values and aggregate-then-map construction

- Provenance: `BOOK:1954-1956`, strict main.
- Establishes: continuous cell values, radius-one mean, a fixed scalar map, and the point seed.

> “each cell is not just black or white, but instead can have any of a continuous range of possible levels of gray.”

> “The idea is to look at the average gray level of a cell and its immediate neighbors, and then to get the gray level for that cell at the next step by applying a fixed mapping to the result.”

> “Starting from a single black cell, what happens in this case is that the gray essentially just diffuses away, leaving in the end a uniform pattern.”

### E2 — Strict interval and mean profile

- Provenance: `BOOK:1960`, strict caption.
- Establishes: `[0,1]` and the identity map on the aggregate.

> “each cell can have any level of gray between white (0) and black (1). The rule shown here takes the new gray level of each cell to be the average of its own gray level and those of its immediate neighbors.”

### E3 — Fractional `3/2` profile and T43 seam

- Provenance: `BOOK:1970,1982`, strict prose/caption.
- Establishes: `FractionalPart[3 mean/2]` and explicit reuse of T43 map `(a)`.

> “the average gray level is multiplied by 3/2, and then only the fractional part is kept if the result of this is greater than 1.”

> “The rule takes the new gray level of each cell to be the fractional part of the average gray level of the cell and its neighbors multiplied by 3/2.”

> “the operation performed on individual average gray levels is exactly iterated map (a) from page 150.”

The first sentence is imprecise at exact result `1`: caption, formula, Notes, and the exact row require unconditional `FractionalPart[1]=0`.

### E4 — Add-constant family and background

- Provenance: `BOOK:1986,2002-2008`, strict main/captions.
- Establishes: `FractionalPart[mean+c]`, `c=1/4`, independent parameter runs, period-four background, and localized profiles.

> “adding the constant 1/4 to the average gray level for the cell and its immediate neighbors, and then taking the fractional part of the result.”

> “The background simply repeats every 4 steps, but the main pattern has a complex and in many respects random form.”

> “The facing page and the one after show what happens when one chooses different values for the constant that is added.”

> “it is even possible to find cases that exhibit localized structures very much like those occasionally seen in ordinary cellular automata.”

> “it is not so much the size of the constant as properties like its digit sequence that seem to determine the overall form of behavior produced in each case.”

### E5 — Adjacent difference is a view

- Provenance: `BOOK:2014`, strict caption.
- Establishes: the page-175 middle panel is a derived observer, not field state.

> “In order to remove the uniform stripes, the picture in the middle shows the difference between the gray level of each cell and its immediate neighbor.”

### E6 — T44 retains discrete space and time

- Provenance: `BOOK:2018`, transition to T45.
- Establishes: the categorical T44/T45 boundary.

> “a continuous cellular automaton is still made up of discrete cells that are updated in discrete time steps.”

### E7 — Diffusion equation is a limiting relation

- Provenance: `BOOK:2036`, T45 main.
- Establishes: the mean CCA and diffusion PDE are related, not identical.

> “The first picture shows the diffusion equation, which can be viewed as a limiting case of the continuous cellular automaton on page 156.”

### E8 — Smooth parameters, random fields, and class observations

- Provenance: `BOOK:2878-2890`, supporting classification main.
- Establishes: parameter ranges, random initial fields, and class labels as experiment/analysis data.

> “The underlying rules in such systems involve a parameter that can vary smoothly from 0 to 1.”

> “one can ask what sequence of classes of behavior one ends up seeing.”

> “Examples of the evolution of continuous cellular automata from random initial conditions.”

> “the gray level of a given cell is determined by averaging the gray levels of the cell and its two neighbors, adding the specified constant, and then keeping only the fractional part of the result.”

### E9 — Weighted-neighbor variant

- Provenance: `BOOK:2904`, supporting class-4 caption.
- Establishes: explicit local weights and another adjacent-difference view.

> “in the third case shown here, the gray level of each neighboring cell is multiplied by 1.13 before the average is done.”

> “the actual gray levels in these pictures are obtained by taking the difference between the gray level of each cell and its neighbor”

The literal divisor remains three; normalization by `2w+1` would be a different rule.

### E10 — External perturbation experiments

- Provenance: `BOOK:3784-3804`, supporting randomness main.
- Establishes: continuous analogs of rules 90/30 and explicit per-event perturbations.

> “investigate what happens if at every step one randomly perturbs the gray level of each cell by a small amount.”

> “For the generalization of rule 90, the values of the left and right cells are added together, and the value of the cell on the next step is then found by applying the continuous generalization of the modulo 2 function shown at the right.”

> “In both cases, every value at each step is also perturbed by a random amount up to the percentage indicated for each picture.”

### E11 — Mean-profile mass conservation

- Provenance: `BOOK:4168`, supporting thermodynamics main.
- Establishes: a derived invariant under non-leaking topology.

> “With each cell at each step having a gray level that is the average of its predecessor and its two neighbors the total amount of black is conserved, but eventually becomes spread uniformly throughout the system.”

This assumes an infinite summable field or a non-leaking finite topology; it does not authorize arbitrary finite edges.

### E12 — Finite periodic implementation and initial-inclusive traces

- Provenance: `BOOK:13283-13292`, native Notes.
- Establishes: list state, periodic reads, parallel evaluation, exact functions, and `t+1` snapshots.

> “The state of a continuous cellular automaton at a particular step can be represented by a list of numbers, each lying between 0 and 1.”

```wolfram
CCAEvolveStep[f_, list_List] :=
 Map[f, (RotateLeft[list] + list + RotateRight[list])/3]
CCAEvolveList[f . init List. t Integer] :=
 NestList[CCAEvolveStep[f, #] &, init, t]
```

> “for the rule on page 157 f is FractionalPart[3#/2]& while for the rule on page 158 it is FractionalPart[# + 1/4] &.”

The second signature is extraction-corrupt; the intended patterns are evidently `f_, init_List, t_Integer`.

### E13 — Exact rational and machine feedback differ

- Provenance: `BOOK:13294`, native Notes.
- Establishes: exact and approximate field recurrences are different declared realization profiles.

> “the elements of list can be either exact rational numbers, or approximate numbers obtained using N.”

> “for detailed calculations exact rational numbers are essential.”

> “the bottom of the picture on page 157 [would be] qualitatively wrong if just 64-bit double-precision numbers had been used.”

> “On page 160 the effect is much larger, and almost all the pictures would be completely wrong—with the notable exception of the one that shows localized structures.”

### E14 — Historical coupled-map aliases

- Provenance: `BOOK:13296-13298`, native Notes.
- Establishes: history, aliases, and the broader aggregate/map family.

> “Versions of continuous cellular automata arose in the mid-1970s as idealizations of coupled ordinary differential equations for arrays of nonlinear oscillators, and implicitly in finite difference approximations to partial differential equations.”

> “so-called ‘coupled map lattices’ or ‘lattice dynamical systems’ in which an iterated map (typically a logistic map) was applied at each step to a combination of neighboring cell value.”

These names do not imply the strict radius-one mean, interval, or fractional map for every historical member.

### E15 — Exact background periods and a 501-rule scan

- Provenance: `BOOK:13300-13304`, native Notes.
- Establishes: background theorem, rational/irrational distinction, and parameter/background/center observers.

> “At step t the background is FractionalPart[at]. For rational a this always repeats, cycling through Denominator[a] possible values.”

> “The pictures below show successive colors of (a) the background ... and (b) the center cell for each a = n/500 from 0 to 1.”

> “If a is not a rational number the background never repeats.”

### E16 — Additive modulo-one/Pascal sibling

- Provenance: `BOOK:13306-13310`, native Notes.
- Establishes: a separate no-center/no-division additive rule and its rational/irrational profiles.

```wolfram
Mod[RotateLeft[list] + RotateRight[list], 1]
```

> “With a single nonzero initial cell with value 1/k the pattern produced is just Pascal’s triangle modulo k.”

> “If k is a rational number only a limited set of values appear”

> “If k is irrational then equidistribution of Mod[Binomial[t, x], k] implies that all possible values eventually appear”

The last phrase means dense/equidistributed coverage, not literal enumeration of an uncountable continuum. Actual cell values are the normalized residues `FractionalPart[Binomial/k]`.

### E17 — Probabilistic CA is an alternative

- Provenance: `BOOK:13314`, native Notes.
- Establishes: discrete stochastic CA is not T44 with a flag.

> “As an alternative to having continuous values at each cell, one can consider ordinary cellular automata with discrete values, but introduce probabilities for, say, two different rules to be applied at each cell.”

### E18 — Finite differences are T45 solver machinery

- Provenance: `BOOK:13401-13403`, T45 Notes.
- Establishes: a discrete finite-difference system may resemble T44 while remaining a PDE approximation.

> “one sets up a system with discrete cells in space and time that is much like a continuous cellular automaton, and then hopes that when the cells in this system are made small enough its behavior will be close to that of the continuous PDE.”

> “Several things can go wrong”

### E19 — Continuous parameters can yield discrete class transitions

- Provenance: `BOOK:14234,14237`, supporting classification Notes.
- Establishes: historical class study and parameter-sweep observations.

> “the parameters of the rule can be varied smoothly. Nevertheless, it still turns out that there are discrete transitions in the overall behavior that is produced.”

> “there are usually ranges of parameter values that yield definite class 4 behavior.”

### E20 — Closed noisy rule-90/rule-30 formulas

- Provenance: `BOOK:15074-15081`, supporting randomness Notes.
- Establishes: the exact source expression for a stochastic continuous-field sibling and a PDE relation.

```text
lambda(x) = Exp[-10(x-1)^2] + Exp[-10(x-3)^2]
rule 90:  v = lambda(a+c)
rule 30:  v = lambda(a+b+c+b*c)
noise:    v + Sign[v-1/2] Random[] delta
```

> “the basic approach used here can be extended to allow discrete cellular automata to be approximated by partial differential equations where not only color but also space and time are continuous.”

The source formula has `lambda(1)=1+Exp[-40]>1`, and the perturbation can widen the range further. No clamp is stated.

### E21 — Boiling is a genuine strict-family preset

- Provenance: `BOOK:15644`, supporting application Notes.
- Establishes: temperature interpretation of `FractionalPart[mean+heating]`.

> “each cell having a temperature from 0 to 1, corresponding exactly to a continuous cellular automaton of the kind discussed on page 155.”

> “the temperature of every cell is given by the average of its temperature and the temperatures of its neighbors ... with a constant amount added to represent external heating.”

> “If the temperature of any cell exceeds 1, then only the fractional part is kept”

### E22 — Phyllotaxis is only a list analogy

- Provenance: `BOOK:15864`, supporting phyllotaxis Notes.
- Establishes: an explicit false-positive boundary.

> “It is convenient to consider a line of discrete cells, much as in a continuous cellular automaton.”

Its sequential argmax placement, translated depletion profile, and decay define another construction.

### E23 — Complex unitary block extension

- Provenance: `BOOK:17002-17008`, supporting quantum Notes.
- Establishes: continuous complex values and block-pair updates as a distinct sibling.

> “One starts by assigning a continuous complex number value to each cell.”

> “the crucial constraint ... is unitarity: that the quantity Tr[Abs[list]^2] representing total probability should be conserved.”

> “a continuous block cellular automaton in which the new value of each block is given by `{{1-xi,xi},{xi,1-xi}} . {a1,a2}`”

This changes value space and update interface; it is not hidden in the scalar gray constructor.

### E24 — Unbounded continuous-field state cardinality

- Provenance: `BOOK:19072`, supporting continuum Notes.
- Establishes: theoretical continuum cardinality, not a finite runtime capacity.

> “Continuous cellular automata ... also have `2^aleph_0` possible states.”

### E25 — Actual Index routes and extraction controls

- Provenance: `BOOK:21046,21054,21434`, actual Index.
- Establishes: all material routes and the two aliases.

> “Continuous cellular automata, 155-160 additive, 1092 cardinality of, 1128 classification of, 948 history of, 921 implementation of, 921 as models of boiling, 994 as models of phyllotaxis, 1007 and probabilistic rules, 976 for quantum mechanics, 1059 with random initial conditions, 2/13”

> “Coupled map lattices, 155–160, 922 see also Continuous cellular”

> “Lattice dynamical systems, 155–160, see also Continuous cellular automata”

The terminal `2/13` is OCR for page 243. The phyllotaxis route is a comparison, not a T44 program.

## Construction Model

The audit must resolve independently:

1. native lattice support versus finite periodic/open/infinite/default/crop realizations;
2. exact/certified/represented `[0,1]` field values, seeds, equality, and serialization;
3. `AllSites`, ordered radius-one old reads, exact mean reducer, closed scalar map, typed assignment, and parallel commit;
4. boundary, endpoints, fractional/modulo semantics, numeric rounding/uncertainty, failure, interruption, and trace outcomes;
5. parameter-family identity, background periods, additive profiles, compact reconstruction, and reproducible presets;
6. value/difference/center/background/parameter/localized-structure observers;
7. T01/T03/T04/T05/T43/T45, coupled maps, probabilistic CA, finite differences, and implementation-helper boundaries.

## Exact Book Presets and Oracles

Pages 171/172/173/174/175 and Notes page 937 assets, exact tables, rational horizons, parameter grids, hashes, pixel classifiers, and declared limitations are under reconstruction.

## Variants, Relations, and Boundaries

T01 fixed lattice assignment, totalistic aggregation, T43 scalar maps/realizations, additive modulo-one rules, coupled-map lattices, probabilistic alternatives, and T45 PDE limits are under audit for exact reuse versus explicit sibling status.

## Current API Fit

In progress.

## Current Runtime Fit

In progress.

## Principles Audit

The smallest current hypothesis composes T01's all-site old-snapshot parallel assignment with an exact mean reducer and T43's closed scalar-map/numerical-realization discipline. It must not replace continuous values with a finite float alphabet, hide exactness inside NumPy, treat periodic helper boundaries as native without evidence, or fuse observer galleries into state.

## Detailed Implementation Plan

1. Complete strict main/raster, Notes, actual Index, split, history, alias, variant, relation, program, and false-positive searches.
2. Decode every rule, seed, support/boundary, horizon, constant, color/difference convention, precision warning, and source defect; regenerate exact or declared oracles.
3. Derive ideal/realized field state, source/read/aggregate/map/result/update, numerical profiles, outcomes, equality, codecs, traces, and observers from evidence.
4. Resolve T01/T43 primitive reuse and T03/T04/T05/T45/additive/coupled/probabilistic boundaries without flags or family dispatch.
5. Audit current API/runtime/tests and write an implementation-ready Goal 2 handoff.
6. Integrate global artifacts and run source/oracle, hash, Markdown, coverage, diff, and repository verification before closure.

## Goal 2 Implementation Stage

Pending the evidence audit.

## No-Cheating Checks

The final stage must reject float-range alphabets as the continuum, opaque aggregate/map callbacks, NumPy arrays as exact field state, hidden periodic boundaries, hidden precision/rounding, render pixels as values, parameter galleries as one run, T43 scalar packing, observer-fed differences, PDE discretizations presented as PDE identity, probabilistic rules hidden as numerical noise, and a T44-specific rollout branch.

## Completion Requirements

- [ ] Every strict main/Notes/actual-Index/split passage, history item, alias, figure, program, variant, relation, and false positive is dispositioned.
- [ ] Support/value/control, source/read/aggregate/map/result/update, boundary/seed, precision/outcome, equality/serialization, trace, and observer semantics are explicit.
- [ ] All six strict and two Notes assets have source-permitted exact or declared oracles, hashes, measurements, and source repairs.
- [ ] T01/totalistic/T43/additive/coupled/probabilistic/T45 boundaries and reuse are explicit.
- [ ] Current API/runtime fit, Goal 2 files/dependencies/tests, global ledgers, diff checks, and repository tests are integrated.

## Stage Results

In progress.

## Integration Results

In progress.
