# 19-T44-CONTINUOUS-CA

Status: **REOPENED — ARCHITECTURE AUDIT; EVIDENCE CLOSED**

Architecture authority: the T44 row and runner contract in `architecture-audit.md` supersede continuous-DOMAIN or construction-specific field-class claims below.

The evidence/search closure and conformance fixtures remain valid. T44 has a discrete `t+1D` DOMAIN with continuous values and reuses the generic local-rule/assignment construction; deterministic profiles are closed rule presets.

## Current Facts

- Exact catalog row: T44, CSV line 45, `Continuous Cellular Automata`; taxonomy vocabulary is `ref/notes/CA-Types.md:1215-1245`. T45 begins at taxonomy line 1247.
- Canonical strict main `Continuous Cellular Automata` is `BOOK:1948-2014`; T45 begins at `2016`. The clean chapter duplicate is `Systems-Based-on-Numbers.md:405-471`, with T45 at 473.
- Native Notes are `BOOK:13281-13315`; T45 Notes begin at `13316`. The useful line-oriented duplicate is `BACK-MATTER/Index/Index.md:1184-1217`, with T45 at 1219. The actual Index begins at `BOOK:20826`.
- The direct-name audit found 34 pre-Index occurrences on 31 lines plus two actual-Index routes; the abbreviated Index has 20 occurrences on 18 lines. Controlled aliases, implementation symbols, formulas, parameters, precision, additive, stochastic, PDE, application, complex-block, and cardinality searches resolve into 25 excerpt groups with zero textual candidate left open.
- The strict construction is a fixed one-dimensional lattice with a gray value at every cell and discrete synchronous time. Each event reads the old left/self/right values, forms their average, applies one fixed scalar mapping, and assigns the result to the same cell in parallel.
- Strict value language is continuous gray from white `0` through black `1`. This is a real interval, not a finite float alphabet or a rendered gray palette.
- The three strict map profiles are identity on the average, `FractionalPart[3 average/2]`, and `FractionalPart[average+c]`; the displayed additive family includes exact `c=1/4` and a parameter gallery.
- The average-only profile is linear diffusion. The `3/2` profile composes T44 neighborhood aggregation with T43 strict map `(a)`. The constant-add profile has a uniform background `FractionalPart[c t]`, but nonuniform deviations can be complex.
- A single black cell on white background is the strict seed. Program, initial field, boundary/realization, requested horizon, numerical profile, and rendering remain separate.
- Notes implementation maps a scalar function over `(RotateLeft[list]+list+RotateRight[list])/3` and uses `NestList`, directly supporting old-snapshot averaging, simultaneous assignment, and initial-inclusive traces.
- `RotateLeft`/`RotateRight` implements a finite periodic-list realization. The ordinary integer line with a finite observation crop is the best strict-main interpretation from T01 context and the point-seed causal cone, but global topology is not explicit in the strict prose and the inference remains labeled.
- T01 already establishes fixed-lattice all-site old-snapshot reads and atomic parallel assignment. T44 appears to reuse that public update law with exact/declared real values, a closed aggregate-plus-map rule, and a new continuous value carrier; no new update law is presumed.
- T43 supplies reusable scalar map-expression and numerical-realization responsibilities, but T44 is not a packed collection of independent T43 states: every new cell value depends on a neighborhood aggregate.
- Native Notes state that exact rationals are essential for detailed profiles: ordinary 64-bit double precision makes the lower page-157 pattern qualitatively wrong and nearly every page-160 parameter panel wrong. Numerical realization therefore affects feedback semantics over the whole field.
- The strict source exposes a potential two-level realization identity: the ideal exact field construction and a fully declared finite-arithmetic field recurrence. T43's ideal/tracked/fixed distinction must be lifted without conflating cell values, computation work state, or rendered gray levels.
- The `c=1/4` background repeats every four events. On the source's admitted `c in [0,1]` family, Notes generalize this to rational `c`, with period equal to the reduced denominator; irrational `c` never repeats. Background periodicity is an observer/property, not a native halt.
- Notes add an additive profile `Mod[RotateLeft[list]+RotateRight[list],1]`. With seed `1/k`, its exact integer-line cells are normalized Pascal residues `FractionalPart[Binomial/k]`; the prose's “Pascal triangle modulo k” describes the unnormalized residues, and “all possible” for irrational `k` means dense/equidistributed coverage rather than literal continuum enumeration.
- Parameter scans, center-cell plots, background plots, adjacent-cell differences, localized-structure views, value equality, and pattern classes are observers. The page-175 difference image cannot replace the underlying field.
- Coupled map lattices/lattice dynamical systems are a historical related family. Probabilistic cellular automata are explicitly an alternative discrete-value stochastic construction, not a T44 flag.
- Supporting pages add declared neighbor multiplier `1.13`, random-field parameter/class scans, a boiling application profile, and explicit noisy continuous analogs of rules 90/30. Boiling leaves its exact-equality threshold ambiguous; the noisy formula can exceed `[0,1]` and no clamp is stated. Neither ambiguity is silently repaired.
- T45 removes discrete cells and discrete time and must remain a distinct continuous-space/time differential-equation category. A finite-difference approximation or PDE limit is a relation, not T44 native identity.
- Six strict and two native-Notes assets plus nine classification/noise/boiling/complex-block supporting assets are closed: all 17 have exact paths, hashes, dimensions, roles, grids/crops where recoverable, and explicit underdetermined render conventions.
- Current finite lattice selectors and parallel assignment are closer to T44 than to T43, but current alphabets discretize floats, current rules admit callbacks, current rollout uses family branches/NumPy rounding, and current exporters treat arrays/renders as the public result. Exact continuous-field semantics are absent.

## Updated Assumptions

- Strict ideal state is a total field from a declared 1D lattice support into mathematical point reals in `[0,1]`, with exact presentations where available and no control or stored history. Certified enclosures and tracked values are computation work/results; fixed represented values form separate realized state.
- A finite periodic list, a finite open segment, an infinite line with finite-support/default presentation, a causal window, and a rendered crop are distinct realizations/scopes.
- `AllSites` is the active source. Each site reads the complete ordered old triple `(left,self,right)`, computes an exact average, applies one closed scalar expression, and returns a typed same-site assignment. All results commit atomically.
- Offset/weight association, rational divisor `3`, map expression, exact/declared parameter, interval/endpoints, boundary, and numeric realization are reproducible data. Ideal exact addition has no host reduction order; a represented realization records its reduction tree and rounding. None is a callback or backend default.
- Source-spelled `FractionalPart` retains the T43/Wolfram `x-IntegerPart[x]` semantics. Strict aggregate/map arguments are nonnegative, where it agrees with modulo one; the additive Notes profile explicitly uses `Mod[...,1]` and remains a distinct primitive.
- Ideal exact field state, certified/tracked computation state, and fixed represented field state remain different. Per-operation rounding locations include addition, division/average, map arithmetic, comparison, and assignment.
- An unchanged field still represents a completed event. Diffusive convergence, exact background periods, repeated finite realizations, localized structures, and observer horizons do not halt the base construction.
- A complete run with `h` events has `h+1` field snapshots. Compact events may reconstruct fields, but a bitmap/float tensor is not the semantic codec.
- Exact field equality, realized-field equality, translational equivalence, observer equality, and visual equality are distinct.
- Parameter-family scans execute separately identified rules/runs. The parameter coordinate is not hidden control and a gallery is not one evolving field.
- Additive, coupled-map, stochastic, PDE-limit, higher-dimensional, alternate-neighborhood, affine-weighted, and asynchronous profiles are admitted only to the extent supported by evidence.

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
- Resolved vocabulary/routes: continuous cellular automata, abbreviated continuous CAs, coupled map lattices, lattice dynamical systems, Kaneko/Chaté/Manneville history, local average/fixed map, fractional/additive/Pascal rules, parameters/background, exact/machine precision, noisy analog rules, probabilistic alternatives, finite differences/PDE limits, boiling, complex block systems, and state cardinality. `continuous-valued`/`real-valued` have no local-book hit.

## Search Log

Canonical shorthand in this stage is `BOOK=ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`. The following is the literal, copy-paste search oracle. It uses `rg -oi` for occurrence counts and `rg -in` for distinct matching-line counts, split before the actual Index at line 20826; `LC_ALL=C` fixes byte-oriented case folding and line handling.

```bash
export LC_ALL=C
BOOK=ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
PRE=$(mktemp)
INDEX=$(mktemp)
sed -n '1,20825p' "$BOOK" > "$PRE"
sed -n '20826,$p' "$BOOK" > "$INDEX"

names=(
  direct abbreviated aliases implementation rotations local_average fixed_map
  exact_forms parameters background precision additive probabilistic pde noisy
  complex real_aliases applications cardinality history local_map_aliases
)
patterns=(
  'continuous cellular automata?'
  'continuous CAs?\b'
  'coupled map lattices?|lattice dynamical systems?'
  'CCAEvolve(?:Step|List)'
  'Rotate(?:Left|Right)\[list\]'
  'average gray level|averag(?:e|ing) (?:the )?gray levels|average of (?:its|the) (?:own )?(?:gray level|temperature)|average of its predecessor'
  'fixed mapping|fixed map|iterated map .*applied .*combination of neighboring'
  'FractionalPart\[3#/2\]|FractionalPart\[# \+ 1/4\]|FractionalPart\[at\]|Mod\[RotateLeft\[list\] \+ RotateRight\[list\], 1\]'
  'constant 1/4|a = n/500|a = 0\.[0-9]+|1\.13|parameter that can vary smoothly from 0 to 1'
  'background is FractionalPart\[at\]|background never repeats|cycling through Denominator\[a\]|background simply repeats'
  'exact rational numbers|machineprecision numbers|64-bit double-precision numbers|approximate numbers obtained using N'
  'Pascal.s triangle modulo k|Mod\[RotateLeft\[list\] \+ RotateRight\[list\], 1\]'
  'probabilistic cellular automata|probabilistic rules'
  'finite difference|limiting case of the continuous cellular automaton|Courant condition|continuous PDE'
  'Noisy cellular automata|randomly perturb(?:s|ed|ing)? the gray level|generalizations? of rules 90 and 30|Sign\[v'
  'continuous complex number value|continuous block cellular automaton'
  'continuous-valued|real-valued|gray-level automata|analog cellular automata'
  'corresponding exactly to a continuous cellular automaton|much as in a continuous cellular automaton'
  'Continuous cellular automata .*possible states'
  'Kaneko|Chat[eé]|Manneville'
  'local maps?|totalistic continuous rules?|diffusion(?:/| and )averaging CA|gray-level automata|analog CAs?\b'
)

for i in "${!names[@]}"; do
  p=${patterns[$i]}
  printf '%-18s %s/%s %s/%s\n' "${names[$i]}" \
    "$(rg -oi "$p" "$PRE" | wc -l)" "$(rg -in "$p" "$PRE" | wc -l)" \
    "$(rg -oi "$p" "$INDEX" | wc -l)" "$(rg -in "$p" "$INDEX" | wc -l)"
done
rm -f "$PRE" "$INDEX"
```

The output, recorded as `pre-index occurrences/lines` then `actual-index occurrences/lines`, was:

| Query name | Pre-Index | Actual Index | Disposition |
|---|---:|---:|---|
| `direct` | 34/31 | 2/2 | Every line inspected |
| `abbreviated` | 0/0 | 20/18 | Every multi-column Index line resolved |
| `aliases` | 2/1 | 2/2 | Historical aliases and redirects |
| `implementation` | 3/3 | 0/0 | Native implementation |
| `rotations` | 5/3 | 0/0 | Periodic finite realization/additive rule |
| `local_average` | 10/9 | 0/0 | Strict law and applications |
| `fixed_map` | 3/3 | 0/0 | T01/T43 composition |
| `exact_forms` | 4/3 | 0/0 | Strict profiles/Notes |
| `parameters` | 8/6 | 0/0 | Gallery, background, weighted variant |
| `background` | 4/3 | 0/0 | Exact property |
| `precision` | 5/1 | 0/0 | Numeric-feedback semantics |
| `additive` | 2/2 | 0/0 | Supplementary rule/property |
| `probabilistic` | 9/7 | 2/2 | Explicit alternative |
| `pde` | 17/14 | 4/4 | T45 relation/boundary |
| `noisy` | 4/4 | 1/1 | Stochastic sibling |
| `complex` | 2/2 | 0/0 | Distinct block extension |
| `real_aliases` | 0/0 | 0/0 | No local-book alias hit |
| `applications` | 2/2 | 0/0 | Boiling/phyllotaxis disposition |
| `cardinality` | 1/1 | 0/0 | Configuration-cardinality property |
| `history` | 6/3 | 3/3 | Named historical routes |
| `local_map_aliases` | 0/0 | 0/0 | No additional controlled-alias hit |

The 31 pre-Index direct-name lines are `1948,1960,1982,1986,2002,2008,2014,2018,2036,2102,2878,2880,2884,2890,2904,3784,3804,13281,13283,13296,13314,13401,14234,14237,15074,15075,15644,15864,16237,17002,19072`. They resolve as follows:

- `1948-2014` is the strict construction; `2018` is the T45 boundary and `2036` its diffusion-limit relation. `2102` is only a PDE resemblance.
- `2878-2904`, `14234`, and `14237` supply parameter/class studies, random seeds, adjacent-difference views, and the neighbor-weight variant.
- `3784-3804` and `15074-15081` supply explicit perturbation/noisy continuous-rule siblings.
- `13281-13314` is native implementation/history/property/variant evidence; `13401-13403` is the PDE numerical boundary.
- `15644` is a genuine boiling preset. `15864` is only a phyllotaxis list analogy. `16237` is terminology/history without construction mechanics.
- `17002-17008` is a complex unitary block extension. `19072` is the state-cardinality property.

The two exact-name Index hits are the main entry at `BOOK:21046` and the lattice-dynamical redirect at `21434`. All 18 abbreviated `continuous CA` Index lines were followed: valid routes occur at `20972,21080,21086,21189,21195,21223,21405,21471,21475,21497,21711,21771,21815,21990,22352`; `20914,21735,21805` are multi-column collisions. In particular, the apparent “Particle accelerators for continuous CAs” at `21735` is not a sentence. Body/Notes resolve the intended parameter and precision routes. Zero textual candidate remains unresolved.

The repository-presence query was also literal and reproducible:

```bash
rg -in \
  -e 'continuous cellular automata?' -e 'continuous CAs?\b' \
  -e 'coupled map lattices?' -e 'lattice dynamical systems?' \
  -e 'CCAEvolve(?:Step|List)' -e 'FractionalPart' \
  -e 'Pascal.s triangle modulo k' -e 'exact rational' \
  -e 'machineprecision|machine precision|precision policy' \
  simple_programs.md src/ca tests
```

It produced no output and exit status `1`: there is no named T44 implementation or conformance test. Current API/runtime responsibilities were then inspected with these exact slices (their dispositions and concrete tests appear below rather than being counted as book evidence):

```bash
sed -n '115,494p;1502,1563p;1964,2122p;2156,2199p' simple_programs.md
sed -n '40,126p' src/ca/alphabets.py
sed -n '31,124p;531,614p' src/ca/loci.py
sed -n '110,230p;551,569p' src/ca/neighborhoods.py
sed -n '37,80p' src/ca/frontiers.py
sed -n '30,328p' src/ca/rules.py
sed -n '23,198p' src/ca/specs.py
sed -n '145,212p;576,682p;742,777p' src/ca/rollout.py
sed -n '39,55p;239,313p;879,939p' src/ca/seeds.py
sed -n '20,70p' src/ca/rng.py
sed -n '177,184p' src/ca/viz/export.py
sed -n '48,54p' tests/test_loci.py
sed -n '86,119p' tests/test_neighborhoods.py
sed -n '263,310p' tests/test_rollout.py
sed -n '8,23p' tests/test_rng.py
sed -n '71,82p' tests/test_seeds.py
sed -n '259,277p' tests/test_viz_export.py
```

## Book Excerpts

### E1 — Continuous values and aggregate-then-map construction

- Provenance: `BOOK:1954-1956`, strict main.
- Establishes: continuous cell values, radius-one mean, a fixed scalar map, and the point seed.

> “each cell is not just black or white, but instead can have any of a continuous range of possible levels of gray.”

> “rules that are in a sense a cross between the totalistic cellular automaton rules ... and the iterated maps”

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

> “Most often considered, notably by Kunihiko Kaneko and co-workers, were so-called ‘coupled map lattices’ or ‘lattice dynamical systems’ in which an iterated map (typically a logistic map) was applied at each step to a combination of neighboring cell value.”

> “A transition from regular class 2 to irregular class 3 behavior, with class 4 behavior involving localized structures in between, was observed, and was studied in detail by Hugues Chaté and Paul Manneville”

These names do not imply the strict radius-one mean, interval, or fractional map for every historical member.

### E15 — Exact background periods and a 501-rule scan

- Provenance: `BOOK:13300-13304`, native Notes.
- Establishes: background theorem, rational/irrational distinction, and parameter/background/center observers.

> “At step t the background is FractionalPart[at]. For rational a this always repeats, cycling through Denominator[a] possible values.”

> “The pictures below show successive colors of (a) the background ... and (b) the center cell for each a = n/500 from 0 to 1.”

> “If a is not a rational number the background never repeats.”

> “most cells whose values are not forced to be the same end up being at least slightly different—even in cases like a = 0.375.”

> “in cases like a = 0.475 there is some trace of a pattern at every step—but it only becomes obvious when it makes values wrap around from 1 to 0.”

The first is a finite-observation property, not an exact theorem that all unequal-role cells differ; the second distinguishes latent structure from the wrap event that makes it visually apparent.

### E16 — Additive modulo-one/Pascal sibling

- Provenance: `BOOK:13306-13310`, native Notes.
- Establishes: additivity of strict `c=0`, plus a separate no-center/no-division additive rule and its rational/irrational profiles.

> “In the case a = 0 the systems on page 159 are purely additive. A simpler example is the rule”

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

### E21 — Boiling application and equality ambiguity

- Provenance: `BOOK:15644`, supporting application Notes.
- Establishes: temperature interpretation of mean plus heating and a source-level equality ambiguity.

> “each cell having a temperature from 0 to 1, corresponding exactly to a continuous cellular automaton of the kind discussed on page 155.”

> “the temperature of every cell is given by the average of its temperature and the temperatures of its neighbors ... with a constant amount added to represent external heating.”

> “If the temperature of any cell exceeds 1, then only the fractional part is kept”

The prose cross-references the page-158 systems, but its literal conditional differs from unconditional `FractionalPart[mean+heating]` at exact value `1`. Preserve a literal threshold-conditional profile and a separately related strict-family reconstruction; the source/asset does not choose between them at equality.

### E22 — Phyllotaxis is only a list analogy

- Provenance: `BOOK:15864`, supporting phyllotaxis Notes.
- Establishes: an explicit false-positive boundary.

> “It is convenient to consider a line of discrete cells, much as in a continuous cellular automaton.”

Its sequential argmax placement, translated depletion profile, and decay define another construction.

### E23 — Complex unitary block extension

- Provenance: `BOOK:17002-17008`, supporting quantum Notes.
- Establishes: continuous complex values and block-pair updates as a distinct sibling.

> “One starts by assigning a continuous complex number value to each cell.”

> “the crucial constraint ... is unitarity: that the quantity Tr[Abs[list]<sup>2</sup>] representing total probability should be conserved.”

The extracted inline matrix expressions omit their multiplication operator and damage spacing. The following are explicitly normalized transcriptions, not verbatim quotes:

```text
diffusion: {{1-xi,xi},{xi,1-xi}} . {a1,a2}
unitary:   {{Cos[theta],i Sin[theta]},{i Sin[theta],Cos[theta]}} . {a1,a2}
```

> “in non-trivial cases most of the cells generated at each step end up having distinct values. One can generalize the setup to more dimensions” and to larger special-unitary matrices.

> “all rules based on matrices are additive ... Non-additive unitary rules can also be found. The analog of an external potential can be introduced by progressively changing values of certain cells at each step.”

The first matrix is the nonunitary diffusion relation; the second is the unitary quantum construction. Both change the strict update interface, and the latter also changes the value space; neither is hidden in the scalar gray constructor.

### E24 — Continuum configuration cardinality

- Provenance: `BOOK:19072`, supporting continuum Notes.
- Establishes: theoretical continuum configuration cardinality, not support size or a finite runtime capacity.

> “Continuous cellular automata (see page 155) also have `2^{N_0}` possible states.”

The extracted `N_0` is the book's damaged rendering of `aleph_0`, established by the immediately preceding cardinality definitions at `BOOK:19070`; the quote is not silently normalized. A single real-valued cell and every nonempty finite real vector already have this same cardinality, so the statement cannot prove unbounded lattice support. The strict-main integer-line interpretation rests instead on the explicitly labeled T01/point-seed context inference.

### E25 — Actual Index routes and extraction controls

- Provenance: `BOOK:21046,21054,21434`, actual Index.
- Establishes: all material routes and the two aliases.

> “Continuous cellular automata, 155-160 additive, 1092 cardinality of, 1128 classification of, 948 history of, 921 implementation of, 921 as models of boiling, 994 as models of phyllotaxis, 1007 and probabilistic rules, 976 for quantum mechanics, 1059 with random initial conditions, 2/13”

> “Coupled map lattices, 155–160, 922 see also Continuous cellular”

> “Lattice dynamical systems, 155–160, see also Continuous cellular automata”

The terminal `2/13` is OCR for page 243. The phyllotaxis route is a comparison, not a T44 program.

## Construction Model

### State, support, and program

The mathematical state is a total continuous-valued field over one fixed discrete lattice. The strict profile has no control state:

```text
ContinuousFieldState {
  support_id: FixedOneDimensionalSupportId,
  field: TotalField[CellCoordinate, MathematicalRealPoint]
}
```

The state contains no time counter, orbit prefix, parameter coordinate, RNG, precision context, difference field, class label, or bitmap. The immutable rule, independently serialized seed, support/realization, run request, numerical profile, trace, and observations remain separate.

The smallest closed strict program is:

```text
ContinuousCASpec {
  support: IntegerLine
         | FiniteCycle(length, labeled_origin)
         | FiniteSegment(interval),
  exterior: NoExterior
          | SegmentExterior(policy, exterior_id),
  value_space: ClosedRealInterval(0, 1),
  neighborhood: OrderedOffsets(-1, 0, +1),
  local_rule: AggregateThenMap {
    aggregate: AffineNeighborhoodAggregate {
      terms: ((-1, 1), (0, 1), (+1, 1)),
      divisor: 3
    },
    map: ClosedScalarExpr,
    primitive_registry_version,
    composite_closure_contract,
    validation_ref
  },
  source: AllSites,
  result: Assign(target=source_site, value=next_value),
  update: AtomicEffectsUpdate
}
```

Validation requires `NoExterior` for the integer line and intrinsic finite cycle, and one independently serialized `SegmentExterior` exactly for a finite segment. Thus the support ID, finite realization/topology ID, and exterior-read policy ID remain distinct even though one validated construction references all that it needs to advance.

The exact strict seed is `X_0(0)=1` and `X_0(i)=0` for `i!=0`. For deterministic spatially homogeneous point-seed profiles, a normalized uniform-default field with finite overrides is an exact presentation of this total field and of every finite-horizon state; it is not a finite-support redefinition of the semantic field. A random initial field or per-site noisy profile generally needs an explicit finite realization or a separately typed lazy total random field/draw source and does not inherit this finite-deviation claim.

The main section does not state a global topology explicitly. The ordinary-CA context, single black cell on white background, triangular causal cones, and T01 semantics make the integer line the best strict-main interpretation, but this remains a recorded inference rather than a quotation. The Notes' rotations prove a separately identified finite periodic cycle. A finite segment, causal work window, halo, and raster crop are also distinct.

The mean profile's “uniform” limit depends on that choice: on the integer line the conserved unit mass spreads and every fixed site tends to uniform white `0`; on an `n`-site cycle it tends to the uniform value `1/n`. The prose does not collapse these realizations.

For the strict admitted `c in [0,1]` family of `FractionalPart[mean+c]`, zero padding is especially invalid: outside the seed's causal cone the uniform background changes globally. If `b_0=0`, then `b_t=FractionalPart[t c]`; the finite data at time `t` are deviations from `b_t`, not values outside a fixed-zero array. This theorem is not extrapolated to negative parameters, where source-faithful `FractionalPart` is not modulo one and may leave `[0,1]`.

### Source, read, aggregate, map, result, and update

At every site `i`, one event performs:

```text
read_i      = (X_t(i-1), X_t(i), X_t(i+1))
aggregate_i = (read_i.left + read_i.self + read_i.right) / 3
next_i      = map(aggregate_i)
result_i    = Assign(CellSlot(i), next_i)
X_{t+1}     = AtomicEffectsUpdate(X_t, {result_i for every i})
```

Every read uses the same complete old snapshot. New values never affect another site in the same event. The physical offsets remain ordered even when the strict aggregate is permutation invariant. Exact ideal addition is canonical mathematics; host reduction trees, fused operations, and intermediate rounding belong only to a represented realization.

T44 reuses T01's `AllSites`, same-site `Assign`, and atomic parallel fixed-field commit without changing their meaning. It adds no eleventh update law. The new semantic capability is an exact affine neighborhood aggregate followed by a closed scalar expression. T43's expression/primitive/range-validation responsibilities compose, but its `IteratedMapSpec` does not: T44 feeds a neighborhood aggregate into the expression and commits a whole field.

Strict closure validates the complete composition

```text
[0,1]^3 -> aggregate range -> map -> [0,1]
```

rather than assuming the aggregate itself lies in the map's declared state interval. A trusted `closed=true` flag is invalid. Admission uses a known mechanically checked constructor or a replayable certificate tied to normalized support, value space, offsets/weights/divisor, ordered expression, exact/declared parameters, and primitive version.

The source-spelled `FractionalPart` remains T43's `x-IntegerPart[x]` primitive. All strict arguments are nonnegative, so it agrees extensionally with modulo one here; it remains structurally distinct from the Notes' explicit `Mod[...,1]`. It is applied at exact integers, including `FractionalPart[1]=0`, and never appears implicitly as an out-of-range boundary policy.

### Exact, certified, tracked, and represented fields

Four numerical categories remain distinct:

1. **Ideal exact field:** mathematical point values. The strict executable reference subset uses arbitrary-size reduced rationals; declared exact irrational profiles require an exact-real backend.
2. **Certified enclosure computation:** interval/set enclosures and refinement evidence approximate an ideal field. They are work/results, not exact point-state equality.
3. **Tracked-significance computation:** approximate values retain precision and error/reliability provenance. Unknown digits remain unknown.
4. **Represented feedback realization:** a different effective recurrence over a declared finite representation.

A represented field-transition identity records radix/format, literal conversion, reduction tree, intermediate and assignment rounding locations, division behavior, `FractionalPart`/comparison implementation, subnormal/nonfinite/overflow policy, evaluator version, and replayable represented-closure evidence. Because every represented result feeds the next neighborhood read, these choices are transition semantics, not rendering context.

If any required local evaluation fails, an atomic event commits no site. A partial or numerical sibling returns a typed outside-domain, uncertain-guard, nonfinite, resource, interruption, or backend outcome with the last complete field. Abstract infinite-field equality must not invent a global `changed` boolean; equality-decidable finite/compact presentations may report `Advanced(changed=...)`.

### Successors, traces, equality, and codecs

A validated strict rule has exactly one successor at every event, including an unchanged field. There is no native halt. A request for `h` events produces `h+1` complete field snapshots and `h` event records. Exact background periods, finite-cycle repetition, convergence, uniformity, class labels, or localized structures are observers and never suppress an event.

For deterministic homogeneous point-seed profiles, compact integer-line events may reference before/after total-field identities, the closed rule, background transition, finite causal-deviation region, and reconstruction evidence instead of enumerating infinitely many effects. Materialized finite-cycle events may carry every local read/result. Random/noisy fields require their own complete finite or lazy semantic presentations; a finite observation crop is not their full state. Any crop or compressed event must reconstruct the claimed snapshots and never becomes the canonical mathematical state.

Keep separate:

1. normalized ideal construction identity;
2. seed identity;
3. support, finite realization, boundary, work window, and crop identities;
4. represented numerical-transition identity;
5. structural aggregate/map identity and certified local-rule equivalence;
6. exact-field and represented-field equality;
7. translation, reflection, cycle rotation, and other field equivalences;
8. finite-observation equality;
9. visual equality.

A finite cycle retains its labeled origin; rotational equivalence is a relation. Tagged codecs preserve arbitrary integers/rationals, declared decimals and provenance, intervals/enclosures, represented bit patterns, total-field presentations, rules, validation refs, seeds, events, outcomes, and observers. JSON floats and NumPy arrays are not authoritative exact codecs.

### Seeds and observers

The strict point seed is independent from the rule. The supporting page-244 random field is a seed-distribution/sample boundary; after sampling, the strict transition is deterministic. The source does not state the distribution, correlations, generator, key, or finite realization. An IID-uniform/PRNG reconstruction must say so and cannot be presented as an exact sample from the mathematical continuum.

Raw gray fields, gray palettes/gamma, aggregate/map legends, center-cell traces, uniform-background traces, total mass, adjacent differences, wrap locations, sensitivity views, parameter sweeps, class labels, localized-structure detections, and renders are typed consumers. The page-175/page-245 source does not determine difference direction, signed versus absolute/modulo operation, wrap, or gray normalization; an observer declares those choices and never feeds them back.

## Exact Book Presets and Oracles

### Strict point-seed formulas and rows

For the mean-only profile on the integer line,

```text
X_t(i) = coefficient(z^i, (z^-1 + 1 + z)^t) / 3^t.
```

It is symmetric, supported on `[-t,t]`, and has exact total mass one. At time 5 on sites `-5..5`:

```text
[1,5,15,30,45,51,45,30,15,5,1] / 243
```

For `FractionalPart[3 mean/2]`, time 4 on `-4..4` is:

```text
1/16, 1/4, 5/8, 0, 3/16, 0, 5/8, 1/4, 1/16
```

and time 5 on `-5..5` is:

```text
1/32, 5/32, 15/32, 7/16, 13/32, 3/32,
13/32, 7/16, 15/32, 5/32, 1/32
```

The time-4 zeroes are a direct equality-threshold guard: they require `FractionalPart[1]=0`, contradicting a literal `if >1` implementation.

For `FractionalPart[mean+1/4]`, the background is

```text
0, 1/4, 1/2, 3/4, 0, ...
```

and time 4 on `-5..5` is:

```text
0, 1/81, 4/81, 10/81, 70/81, 73/81,
70/81, 10/81, 4/81, 1/81, 0
```

These exact rows repair the rounded and structurally corrupt Markdown tables. Within the admitted `c in [0,1]` family, reduced rational `c=p/q` gives the zero-background period `q`. Exact irrational `c` never repeats; represented arithmetic may.

### Supplementary algebraic anchors

The page-245 declared neighbor multiplier has the closed aggregate

```text
(1.13 L + C + 1.13 R) / 3.
```

The source literal `1.13` retains declared-decimal provenance. A separately identified exact reconstruction `w=113/100` has aggregate range `[0,163/150]`; division by `163/100` would normalize a different rule. `FractionalPart(aggregate+c)` still closes the composite into `[0,1)`.

For the additive sibling on the integer line, seed `1/k` at zero gives

```text
X_t(i) = FractionalPart(Binomial(t,(t+i)/2) / k)
```

when `|i|<=t` and `t+i` is even, and zero otherwise. For the source's interval-valued seed require `k>=1`; if reduced rational `k=p/q>=1`, at most `p` residues appear. This is Pascal's triangle modulo `k`, scaled back into `[0,1)`; it is not the strict `c=0` mean rule.

The noisy source profile exposes a precision-sensitive range defect:

```text
lambda(1) = 1 + Exp[-40] > 1.
```

Binary64 evaluates the first displayed sum as `1.0`, itself illustrating why implicit machine arithmetic cannot settle mathematical closure. The stochastic rule also pushes values away from `1/2`; no clamp is stated.

### Semantic oracle

This dependency-free command is the exact semantic oracle. It checks the printed rows, coefficient formula, symmetry, mass, period-four background, rational additive residues, weighted range, strict-versus-literal boiling equality divergence, and high-precision `lambda(1)` inequality:

```bash
python3 - <<'PY'
from decimal import Decimal, getcontext
from fractions import Fraction as F
from functools import lru_cache
from math import factorial

getcontext().prec = 80

def frac(x):
    return x - x.numerator // x.denominator

def recurrence(mode, c=F(0)):
    @lru_cache(None)
    def x(t, i):
        if t == 0:
            return F(1) if i == 0 else F(0)
        u = (x(t-1, i-1) + x(t-1, i) + x(t-1, i+1)) / 3
        return {'mean': u, 'scale': frac(3*u/2), 'add': frac(u+c)}[mode]
    return x

def trinomial(t, i):
    total = 0
    for left in range(t + 1):
        for right in range(t - left + 1):
            center = t - left - right
            if right - left == i:
                total += factorial(t)//(
                    factorial(left)*factorial(center)*factorial(right)
                )
    return total

mean = recurrence('mean')
scale = recurrence('scale')
addq = recurrence('add', F(1, 4))
mean_t5 = [mean(5, i) for i in range(-5, 6)]
scale_t4 = [scale(4, i) for i in range(-4, 5)]
scale_t5 = [scale(5, i) for i in range(-5, 6)]
addq_t4 = [addq(4, i) for i in range(-5, 6)]
assert mean_t5 == [F(n, 243) for n in (1,5,15,30,45,51,45,30,15,5,1)]
assert scale_t4 == [F(1,16),F(1,4),F(5,8),0,F(3,16),0,F(5,8),F(1,4),F(1,16)]
assert scale_t5 == [F(1,32),F(5,32),F(15,32),F(7,16),F(13,32),F(3,32),
                    F(13,32),F(7,16),F(15,32),F(5,32),F(1,32)]
assert addq_t4 == [0,F(1,81),F(4,81),F(10,81),F(70,81),F(73,81),
                   F(70,81),F(10,81),F(4,81),F(1,81),0]
for t in range(9):
    assert sum(mean(t, i) for i in range(-t, t+1)) == 1
    for i in range(-t, t+1):
        assert mean(t, i) == F(trinomial(t, i), 3**t)
        assert mean(t, i) == mean(t, -i)

def background(t, c):
    value, out = F(0), [F(0)]
    for _ in range(t):
        value = frac(value+c)
        out.append(value)
    return out

assert background(4, F(1,4)) == [0,F(1,4),F(1,2),F(3,4),0]
assert background(12, F(3,4))[0] == background(12, F(3,4))[4]

def additive(t, i, k):
    @lru_cache(None)
    def x(s, j):
        if s == 0:
            return 1/k if j == 0 else F(0)
        return frac(x(s-1, j-1)+x(s-1, j+1))
    return x(t, i)

for k in (F(2),F(3),F(7,3),F(81,73)):
    seen = set()
    for t in range(11):
        for i in range(-t, t+1):
            expected = F(0)
            if (t+i) % 2 == 0:
                expected = frac(F(
                    factorial(t),
                    factorial((t+i)//2)*factorial((t-i)//2)
                )/k)
            assert additive(t, i, k) == expected
            seen.add(expected)
    assert len(seen) <= k.numerator

weighted_max = (F(113,100)+1+F(113,100))/3
assert weighted_max == F(163,150)
strict_at_one = frac(F(1))
literal_at_one = F(1) if F(1) <= 1 else frac(F(1))
assert strict_at_one == 0 and literal_at_one == 1
lambda1 = Decimal(1)+(-Decimal(40)).exp()
assert lambda1 > 1

print('T44 semantic oracle PASS')
print('mean_t5', ','.join(map(str, mean_t5)))
print('scale_t4', ','.join(map(str, scale_t4)))
print('scale_t5', ','.join(map(str, scale_t5)))
print('add_quarter_background', ','.join(map(str, background(4, F(1,4)))))
print('add_quarter_t4', ','.join(map(str, addq_t4)))
print('weighted_max', weighted_max)
print('exact_one strict/literal', strict_at_one, literal_at_one)
PY
```

Recorded output:

```text
T44 semantic oracle PASS
mean_t5 1/243,5/243,5/81,10/81,5/27,17/81,5/27,10/81,5/81,5/243,1/243
scale_t4 1/16,1/4,5/8,0,3/16,0,5/8,1/4,1/16
scale_t5 1/32,5/32,15/32,7/16,13/32,3/32,13/32,7/16,15/32,5/32,1/32
add_quarter_background 0,1/4,1/2,3/4,0
add_quarter_t4 0,1/81,4/81,10/81,70/81,73/81,70/81,10/81,4/81,1/81,0
weighted_max 163/150
exact_one strict/literal 0 1
```

### Asset and raster audit

The native strict/Notes block contains exactly eight linked assets. Nine additional assets materially illustrate supporting classification/noise/application/block passages. Canonical text remains the monolith; exact asset roots are:

```text
SBN   = ref/A-New-Kind-of-Science/CHAPTERS/4-Systems-Based-on-Numbers/Images
RAND  = ref/A-New-Kind-of-Science/CHAPTERS/6-Starting-from-Randomness/Images
MECH  = ref/A-New-Kind-of-Science/CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images
NOTES = ref/A-New-Kind-of-Science/BACK-MATTER/Index/Images
```

Table rows 1-6 use `SBN`, 7-8 and 15-17 use `NOTES`, 9-12 use `RAND`, and 13-14 use `MECH`; thus every basename below resolves to one exact repository path.

| Asset | Role | Bytes | Dimensions | SHA-256 |
|---|---|---:|---:|---|
| `_page_171_Picture_5.jpeg` | identity-map rule diagram; diffusion evolution raster absent | 4,640 | 277x91 | `6695e1c946cf6adaa04a3915f2c720f69de4d18b74a81a01aaab346052119455` |
| `_page_172_Picture_1.jpeg` | `FractionalPart[3 mean/2]` rule, long field, early inset | 137,852 | 1192x911 | `55990561c9f118ca0cfd6c7818d845b19d027456af491fb036a8867a2dd343b2` |
| `_page_173_Picture_3.jpeg` | `FractionalPart[mean+1/4]` early periodic grid | 34,836 | 470x279 | `fe6e23666bf0136fd84d4c3e10f7ebdb716409fa9f2e76b9914ca963cd907459` |
| `_page_173_Picture_4.jpeg` | add-quarter rule diagram | 4,905 | 241x87 | `cfd37cb74c6c8d8c35b23b05f0125776536ac9ed20713a2577c7865ca50f44f0` |
| `_page_174_Picture_2.jpeg` | 21-member strict constant gallery | 210,694 | 1104x1455 | `8a3262ca6ce522946165605a13dd361cfdf1cba20862467b88d1c925089fcef3` |
| `_page_175_Figure_2.jpeg` | nine long profiles, including one difference view | 306,671 | 1199x1321 | `e286f430a42f9f5246120012b9bfb6b1e9508f59a63e8bc46ef75d5b7706aa4f` |
| Notes `_page_937_Picture_3.jpeg` | background/center parameter-time scans | 59,149 | 558x326 | `52fdb59e6b6dbd8cc6a076da5e04b20cbec39d85e9cc894f9397f5dae460c6f1` |
| Notes `_page_937_Picture_8.jpeg` | six additive Pascal profiles | 23,933 | 592x238 | `e1443f6b4aee358dad09728c67919c6ead43d3a8c583e8ff63c78b458e647ec7` |
| `_page_258_Figure_1.jpeg` | ten random-seed parameter/class panels | 264,239 | 1092x1280 | `6e7bd2166885376ea79dce59500a35ea01bf6e91fd51b6241812ef15e97243c3` |
| `_page_259_Picture_2.jpeg` | difference-view class-4 profile `c=.39` | 101,531 | 989x348 | `1797a19a5e12b8fd0f3165ecbdb9a6149646809ed71c6e1d8d8ae6f2414ab443` |
| `_page_259_Picture_4.jpeg` | difference-view class-4 profile `c=.4` | 100,962 | 994x344 | `3f138bccbbaedbcfe9865069685819d618234ba9525749dc1c7afaeed695d30f` |
| `_page_259_Picture_6.jpeg` | weighted profile `{c=.5,w=1.13}` difference view | 90,996 | 1000x343 | `7d9fd822a9dc2cabbdfc4c0030bef8b0f69d14f8ff9f5c8547bc2bf6010c9815` |
| `_page_340_Figure_2.jpeg` | noisy continuous rule-90/rule-30 galleries | 173,739 | 908x1238 | `b9e4ce7d19b3e1697c3b6597c7eb6bc87a51c289e77407b615d05cdae095d429` |
| `_page_340_Figure_4.jpeg` | smooth `lambda` rule graph | 4,761 | 208x142 | `30e81284df91ba52a7d0a401b868fa9a10a0f73ae5ed8d884a48bca8561a16d5` |
| `_page_1009_Picture_6.jpeg` | boiling/heating `c=.05` | 8,459 | 270x132 | `2e0309aed825ace57ba916bb3d2332d707af7e0d1105bd67637151854a76d7d5` |
| `_page_1009_Picture_7.jpeg` | boiling/heating `c=.1` | 10,078 | 263x134 | `733e4bfc8212ee9c7cce554e156fb3f62def9dd474277004a5f79711050d0047` |
| `_page_1075_Picture_3.jpeg` | distinct complex unitary block-CA sibling | 15,585 | 579x141 | `2abb1adb633919a13091fd89fb2598011eb7d6344de7ebc249b6d041632a16ed` |

The metadata table is reproducible with Pillow and the standard library:

```bash
python3 - <<'PY'
from hashlib import sha256
from pathlib import Path
from PIL import Image

roots = {
    'SBN': Path('ref/A-New-Kind-of-Science/CHAPTERS/4-Systems-Based-on-Numbers/Images'),
    'RAND': Path('ref/A-New-Kind-of-Science/CHAPTERS/6-Starting-from-Randomness/Images'),
    'MECH': Path('ref/A-New-Kind-of-Science/CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images'),
    'NOTES': Path('ref/A-New-Kind-of-Science/BACK-MATTER/Index/Images'),
}
assets = [
 ('SBN','_page_171_Picture_5.jpeg'), ('SBN','_page_172_Picture_1.jpeg'),
 ('SBN','_page_173_Picture_3.jpeg'), ('SBN','_page_173_Picture_4.jpeg'),
 ('SBN','_page_174_Picture_2.jpeg'), ('SBN','_page_175_Figure_2.jpeg'),
 ('NOTES','_page_937_Picture_3.jpeg'), ('NOTES','_page_937_Picture_8.jpeg'),
 ('RAND','_page_258_Figure_1.jpeg'), ('RAND','_page_259_Picture_2.jpeg'),
 ('RAND','_page_259_Picture_4.jpeg'), ('RAND','_page_259_Picture_6.jpeg'),
 ('MECH','_page_340_Figure_2.jpeg'), ('MECH','_page_340_Figure_4.jpeg'),
 ('NOTES','_page_1009_Picture_6.jpeg'), ('NOTES','_page_1009_Picture_7.jpeg'),
 ('NOTES','_page_1075_Picture_3.jpeg'),
]
for root, name in assets:
    path = roots[root]/name
    print(path, path.stat().st_size, Image.open(path).size, sha256(path.read_bytes()).hexdigest())
excluded = roots['MECH']/'_page_339_Figure_1.jpeg'
print('EXCLUDED', excluded, excluded.stat().st_size, Image.open(excluded).size,
      sha256(excluded.read_bytes()).hexdigest())
PY
```

The following command was run verbatim from the repository root. It fixes the half-open crop convention, white/black transfer `round(255*(1-u))`, bilinear resampling, exact rational recurrence, score computation, and permissive JPEG thresholds; it writes no repository file:

```bash
uv run --with pillow --with numpy python - <<'PY'
from fractions import Fraction
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path('/home/jake/Developer/ankos')
STRICT = ROOT / 'ref/A-New-Kind-of-Science/CHAPTERS/4-Systems-Based-on-Numbers/Images'
NOTES = ROOT / 'ref/A-New-Kind-of-Science/BACK-MATTER/Index/Images'

def gray(path):
    return np.asarray(Image.open(path).convert('L'), dtype=np.float64)

def render(q, shape):
    h, w = shape
    return np.asarray(
        Image.fromarray(q).resize((w, h), Image.Resampling.BILINEAR),
        dtype=np.float64,
    )

def score(name, obs, exp, r_min, mae_max):
    r = float(np.corrcoef(obs.ravel(), exp.ravel())[0, 1])
    mae = float(np.mean(np.abs(obs - exp)))
    print(f'{name}: r={r:.12f}; mae={mae:.9f}; shape={obs.shape}')
    assert obs.shape == exp.shape
    assert r >= r_min, (name, r, r_min)
    assert mae <= mae_max, (name, mae, mae_max)

def evolve(width, seed, states, mode, c=Fraction(0)):
    u = [Fraction(0) for _ in range(width)]
    u[seed] = Fraction(1)
    rows = []
    for _ in range(states):
        rows.append([float(x) for x in u])
        if mode == 'mul32':
            u = [((u[(i-1)%width]+u[i]+u[(i+1)%width])/2)%1
                 for i in range(width)]
        elif mode == 'addc':
            u = [((u[(i-1)%width]+u[i]+u[(i+1)%width])/3+c)%1
                 for i in range(width)]
        elif mode == 'additive':
            u = [(u[(i-1)%width]+u[(i+1)%width])%1
                 for i in range(width)]
        else:
            raise ValueError(mode)
    return np.asarray(rows, dtype=np.float64)

def q8(u):
    return np.rint(255.0*(1.0-u)).astype(np.uint8)

def signed_q8(u):
    return np.rint(127.5*(1.0-u)).clip(0,255).astype(np.uint8)

# Page 172 main: 151 states; wide exact field, central 203-column crop.
g = gray(STRICT/'_page_172_Picture_1.jpeg')
u = evolve(601,300,151,'mul32')[:,199:402]
obs = g[47:874,39:1151]
exp = render(q8(u),obs.shape)
score('p172-main-lower-unoccluded',obs[300:],exp[300:],.990,6.0)

# Page 172 31x23 inset, direct cell-center samples.
xb=np.rint(np.linspace(805,1127,32)).astype(int)
yb=np.rint(np.linspace(64,304,24)).astype(int)
xs=(xb[:-1]+xb[1:])//2
ys=(yb[:-1]+yb[1:])//2
obs=g[np.ix_(ys,xs)]
u=evolve(31,15,23,'mul32')
score('p172-inset-centers',obs,255.0*(1.0-u),.993,6.0)

# Page 173 50x30 direct cell-center samples.
g=gray(STRICT/'_page_173_Picture_3.jpeg')
xb=np.rint(np.linspace(29,444,51)).astype(int)
yb=np.rint(np.linspace(16,265,31)).astype(int)
xs=(xb[:-1]+xb[1:])//2
ys=(yb[:-1]+yb[1:])//2
obs=g[np.ix_(ys,xs)]
u=evolve(50,24,30,'addc',Fraction(1,4))
score('p173-centers',obs,255.0*(1.0-u),.993,7.0)

# Page 174 representative c=.1, 101x51.
g=gray(STRICT/'_page_174_Picture_2.jpeg')
u=evolve(101,50,51,'addc',Fraction(1,10))
obs=g[259:398,413:693]
score('p174-c0.1',obs,render(q8(u),obs.shape),.995,3.0)

# Page 175 c=.1 state, 201 states, central 184-column reconstruction.
g=gray(STRICT/'_page_175_Figure_2.jpeg')
u=evolve(501,250,201,'addc',Fraction(1,10))[:,158:342]
obs=g[69:424,63:384]
score('p175-c0.1-state',obs,render(q8(u),obs.shape),.985,5.0)

# Page 175 declared .3299, rational oracle, absolute right difference.
u=evolve(501,250,201,'addc',Fraction(3299,10000))
d=np.abs(u[:,158:343]-u[:,159:344])
obs=g[475:829,437:763]
score('p175-c0.3299-abs-right',obs,render(q8(d),obs.shape),.990,5.0)

# Same crop, declared transfers: discriminate plausible source-understated views.
alternatives = {
    'abs-right': (d, False),
    'abs-left': (np.abs(u[:,158:343]-u[:,157:342]), False),
    'mod-right': ((u[:,158:343]-u[:,159:344])%1, False),
    'signed-right': (u[:,158:343]-u[:,159:344], True),
    'raw-field': (u[:,158:343], False),
}
alt_r = {}
for name,(values,signed) in alternatives.items():
    expected = render(signed_q8(values) if signed else q8(values), obs.shape)
    alt_r[name] = float(np.corrcoef(obs.ravel(), expected.ravel())[0,1])
    print(f'p175-discriminator-{name}: r={alt_r[name]:.12f}')
assert alt_r['abs-right'] > max(v for k,v in alt_r.items() if k != 'abs-right')

# Notes page 937 top: a=n/500 columns, t=1..150 rows.
g=gray(NOTES/'_page_937_Picture_3.jpeg')
n=np.arange(501,dtype=np.int64)[None,:]
t=np.arange(1,151,dtype=np.int64)[:,None]
u=((t*n)%500)/500.0
obs=g[23:143,42:543]
score('notes937-background',obs,render(q8(u),obs.shape),.700,30.0)

# Notes page 937 additive first three exact-rational panels, 101x51.
g=gray(NOTES/'_page_937_Picture_8.jpeg')
for label,k,box in [
    ('k2',Fraction(2),(33,29,191,106)),
    ('k3',Fraction(3),(217,29,375,106)),
    ('k7over3',Fraction(7,3),(402,29,560,106)),
]:
    u=[Fraction(0) for _ in range(101)]
    u[50]=Fraction(1)/k
    rows=[]
    for _ in range(51):
        rows.append([float(x) for x in u])
        u=[(u[(i-1)%101]+u[(i+1)%101])%1 for i in range(101)]
    rows=np.asarray(rows,dtype=np.float64)
    x0,y0,x1,y1=box
    obs=g[y0:y1,x0:x1]
    score(f'notes937-additive-{label}',obs,render(q8(rows),obs.shape),.800,9.0)

print('T44 core raster oracle: PASS')
PY
```

Recorded output:

```text
p172-main-lower-unoccluded: r=0.993334649229; mae=5.274019494; shape=(527, 1112)
p172-inset-centers: r=0.995882643601; mae=5.422086611; shape=(23, 31)
p173-centers: r=0.994562593262; mae=6.603864422; shape=(30, 50)
p174-c0.1: r=0.997868874924; mae=2.114080164; shape=(139, 280)
p175-c0.1-state: r=0.987791869483; mae=4.398157167; shape=(355, 321)
p175-c0.3299-abs-right: r=0.992953791832; mae=3.803447021; shape=(354, 326)
p175-discriminator-abs-right: r=0.992953791832
p175-discriminator-abs-left: r=0.673256323467
p175-discriminator-mod-right: r=0.250179257169
p175-discriminator-signed-right: r=0.002777415336
p175-discriminator-raw-field: r=0.140263839365
notes937-background: r=0.720128343531; mae=26.222272122; shape=(120, 501)
notes937-additive-k2: r=0.872066279505; mae=5.039536413; shape=(77, 158)
notes937-additive-k3: r=0.836592450795; mae=5.971395693; shape=(77, 158)
notes937-additive-k7over3: r=0.877814246188; mae=7.491533783; shape=(77, 158)
T44 core raster oracle: PASS
```

The strict geometry and exact regeneration establish:

- Page 171's extraction contains only the identity map diagram. The six-row diffusion evolution survives as rounded text; exact rows come from the trinomial oracle above.
- Page 172 contains 151 initial-inclusive states `t=0..150` over a 203-cell visible central window. Resize the exact 151x203 gray array to half-open crop `x=39:1151,y=47:874` and compare only relative rows `300:` because the insets occlude the upper main raster: `r=.993335`, MAE `5.27/255`. Its inset is exactly 31 cells by 23 states `t=0..22`, seed at index 15; boundaries are rounded `linspace(805,1127,32)` and `linspace(64,304,24)`, with integer midpoint samples. Exact dyadic regeneration gives `r=.9958826436`, MAE `5.42209/255`. JPEG, grid/overlay, scaling, and unstated tone transfer preclude a literal byte-for-value claim. The main computation boundary is outside the visible crop.
- Page 173 Picture 3 has 50 visible cells by 30 initial-inclusive rows `t=0..29`, seed index 24. Center samples use rounded boundaries `linspace(29,444,51)` and `linspace(16,265,31)`. All 1,500 centers against the exact Notes ring give `r=.9945625933`, MAE `6.60386/255`. Because this is a central finite raster and strict prose states no edge behavior, it does not establish the global boundary. Picture 4 places the map discontinuity at `x=3/4`.
- Page 174 contains 21 row-major labeled rules whose mathematical constants are `c=n/40`, `n=0..20`, displayed `0,.025,...,.5`. Each panel shows 101 cells by 51 states `t=0..50` from the point seed. The representative `c=1/10` exact-rational reconstruction, bilinearly resized to `x=413:693,y=259:398`, gives `r=.99787`, MAE `2.11/255`. This matches geometry/appearance but does not establish the source's numeric storage. The mathematical background is `FractionalPart[t c]`.
- Page 175 labels `c={.1,.3,.325,.3299,.3299 differences,.35,.475,.495,.9}`. Each panel shows 201 states `t=0..200` over a resampled central crop of about 184-185 cells. The `c=1/10` exact-rational field reconstruction on 184 columns against `x=63:384,y=69:424` gives `r=.98779`, MAE `4.40/255`. The duplicate declared-decimal `.3299` entries are one trajectory and an adjacent absolute-right-difference observer: 185 reconstructed columns against `x=437:763,y=475:829` give `r=.99295`, MAE `3.80/255`. On that same crop and under the oracle's explicit transfers, absolute-right `r=.99295` decisively exceeds absolute-left `.67326`, modulo-right `.25018`, signed-right `.00278`, and raw field `.14026`. The convention is therefore strong raster inference—prose says only “difference.” `3299/10000` is a reconstruction, not proven source identity; the raster cannot identify its stored numeric representation. Native Notes say exact rationals are essential and double precision makes almost every page-160 profile wrong, with this localized-structure panel as the exception.
- Notes page 937 Picture 3 has two matrices over exact mathematical parameters `c=n/500`, `n=0..500`: uniform background and center cell. Columns are exactly `x=42+n`. The top represents `t=1..150`; bilinearly resizing its exact 150x501 background array into `x=42:543,y=23:143` gives `r=.72013`, MAE `26.22/255`. Axes/JPEG and 150-to-120 vertical downsampling make this a visual check, not exact cell identity. The bottom uses the same axes/horizon for the exact center family.
- Notes page 937 Picture 8 labels `k={2,3,7/3,81/73,Sqrt[2],Pi}` for the additive sibling. Each row-major panel encodes `t=0..50` and a 101-cell window in a 158x77 crop: `k=2` at `33:191,29:106`, `k=3` at `217:375,29:106`, `k=7/3` at `402:560,29:106`, `k=81/73` at `33:191,140:217`, `Sqrt[2]` at `217:375,140:217`, and `Pi` at `402:560,140:217`. Exact-rational fits for the first three are respectively `r=.87207/.83659/.87781`, MAE `5.04/5.97/7.49`. Finite-raster precision of the denser fourth and irrational panels remains underdetermined, and appearance is not proof of equidistribution.

The supporting page-258 gallery directly labels deterministic add-constant rules `c=0,.1,...,.9` and random initial fields, but width/horizon, field measure, generator, and seed are absent; its roughly 250x100 panel cadence is raster inference only. Page 259 directly labels `.39`, `.4`, and `{.5,1.13}`, all with random initial fields and neighbor-difference views; the last means the divisor-three rule `FractionalPart[(1.13L+C+1.13R)/3+.5]`, not division by `3.26`. Page 340 Figure 2 labels rule-90 perturbations `0%,5%,10%,15%` and rule-30 perturbations `0%,.5%,.8%,1%,2%,5%`; the full `Random[]` draws are unrecoverable, and a roughly 101-state/201-cell geometry is only an aspect-ratio inference. Figure 4 is the source `lambda` icon over about `[0,4]`, not evidence of `[0,1]` closure. Boiling directly labels heating rates `.05` and `.1`, but initial field, boundary, width, horizon, RNG, and numeric storage are absent. Its literal threshold-conditional wrap is transition semantics; emitted wrap/bubble-event records and their rendering are observers. The complex asset is a distinct alternating pair-block unitary sibling and cannot test the strict gray rule.

Page 339 Figure 1 is explicitly excluded: it is discrete ECA rule 30 with varying counts of initial black cells, not continuous state (`108,161` bytes, `1105x410`, SHA-256 `8f3f13473abc794bc49321891b3c2ed636a9277c3faff84826772b74cd0e7ba9`). Probabilistic-CA page 591, PDE limits, and historical mentions are likewise distinct types or textual context. The cross-reference and raster audit is closed at 17 included assets and this one material exclusion; no semantic conclusion depends on an unstated renderer setting.

### Source and extraction repairs

1. Monolith image links omit `Images/`; clean split directories provide asset provenance while monolith lines remain canonical text provenance.
2. Notes assets for pages 937, 1009, and 1075 are physically under `BACK-MATTER/Index/Images`, and the line-oriented Notes prose is duplicated in `BACK-MATTER/Index/Index.md`; neither filesystem placement changes canonical provenance.
3. Page 171 promises a diffusion evolution, but its extracted asset contains only the 277x91 identity-map icon. The six-row text table is the surviving evolution oracle.
4. Early tables lose nonzero cells: pages 171/173 omit the time-zero center `1`; page 172 time 4 loses two `5/8` cells; page 173 time 2 loses two `11/18` cells. The split sometimes converts or misaligns blanks as zeros. Exact recurrence repairs them; rounded text is never exact state.
5. `BOOK:1970`'s “greater than 1” threshold conflicts with caption, formula, Notes, and exact rows at equality.
6. `BOOK:13288` corrupts Wolfram pattern separators in the `CCAEvolveList` signature; the `NestList` intent remains clear.
7. `BOOK:13298`'s singular “neighboring cell value” is a grammar/extraction defect.
8. `machineprecision` and `wrong-with` at `13294` have missing spacing/punctuation.
9. `BOOK:13310`'s “all possible values” is not literal continuum enumeration.
10. The actual Index is multi-column-spliced; apparent collisions are not prose. Its `2/13` is OCR for page 243.
11. Page-259 parameter labels are detached from their assets; order resolves Picture 2 as `.39`, Picture 4 as `.4`, and Picture 6 as `{.5,1.13}`.
12. Finite periodic boundary is explicit only in Notes code, not strict prose or central raster crops.
13. The page-245 difference convention and random-field measure are not stated. Absolute-right difference is a raster-derived reconstruction, not a repaired quote.
14. The page-325 `x_-` is an extraction of Wolfram pattern syntax. `Random[]` fixes a uniform pseudorandom real marginal on `[0,1]`, but draw independence/correlation, exact seed/draws, call order, fully pinned historical generator, finite boundary, and out-of-range handling remain unstated.
15. Exact precision, reduction order, supporting horizons, raster transfer curves, and some crop conventions are unstated and cannot be recovered by appearance alone.
16. The boiling passage's “exceeds 1” threshold is not equivalent to the strict unconditional add-constant map at exact one. Its page-158 cross-reference suggests a repair but does not prove it; literal and reconstructed profiles stay separate.
17. The page-325 and boiling random/supporting rasters lack replay seeds or complete initial fields and therefore support preset/disposition evidence, not golden transition arrays.

## Variants, Relations, and Boundaries

### Strict and supplementary T44 profiles

- **Mean/diffusion:** strict exact mean followed by identity; point-seed coefficient and mass invariant.
- **Fractional `3/2`:** strict exact mean followed by the T43 `(a)` expression; exact rational primary conformance.
- **Add-constant family:** strict exact mean followed by `FractionalPart[u+c]`; parameter is immutable rule data and each gallery panel is an independent run.
- **Weighted neighbors:** closed affine aggregate `((w,L),(1,C),(w,R))/3` followed by the add-constant map. This does not justify an arbitrary reducer callback.
- **Boiling:** mean plus heating with latent-heat interpretation. Literal threshold-conditional and unconditional strict-family reconstruction agree except at exact one and share the executor, but remain different closed rule identities until evidence resolves the equality convention.
- **Additive Pascal:** `Mod[L+R,1]`, excluding center and divisor. It can share fixed-field execution and closed arithmetic but is a distinct local-rule constructor.
- **Coupled-map/lattice-dynamical systems:** broader closed combinations plus closed scalar maps such as logistic. The historical alias does not make all combinations strict presets.
- **Noisy rule analogs:** a stochastic real-field sibling with closed lambda/rule expressions and explicit draws. After draws are resolved it uses the same parallel assignment commit; stochasticity is not roundoff.
- **Complex unitary block CA:** complex amplitudes and pair-block unitary update. This needs the later block-CA update evidence and cannot be packed into scalar gray state.

### Stochastic profile boundary

The page-325 source profile is:

```text
lambda(x) = Exp[-10(x-1)^2] + Exp[-10(x-3)^2]
rule90 base: lambda(L+R)
rule30 base: lambda(L+C+R+C*R)
result: v + Sign(v-1/2) * U * delta
```

The legacy Wolfram `Random[]` primitive fixes `U`'s marginal as a uniformly distributed pseudorandom real from 0 to 1; this is corroborated by the [official obsolete-symbol reference](https://reference.wolfram.com/language/ref/Random.html). A sampled realization still records primitive/version, seed or draw witnesses, generator, call/index order, and a coordinate-stable map from `(event,site,draw_slot)` to draws. Neither mathematical independence nor a fully pinned historical generator follows from the expression alone. Evaluation enumeration must not alter a declared coordinate-indexed reconstruction. The literal source does not close over `[0,1]`; use a widened/partial profile or typed range failure, never silent clamp. The Notes' probabilistic CA instead has discrete values and random rule selection and remains an explicit alternative.

### Cross-type boundaries

- **T01:** directly supplies fixed 1D support responsibilities, ordered old reads, `AllSites`, same-site assignment, parallel commit, causal halos, and support/realization/crop separation.
- **T03/T04/T05 and totalistic CA:** finite discrete totalistic tables may share an aggregation responsibility but not continuous value/range/numeric semantics. Later evidence owns their exact restrictions.
- **T34:** shares exact numeric values and assignment-effect responsibility, not spatial fields.
- **T41:** shares closed expression, primitive, exact/declared value, domain, and evaluator records. A pure function query is not field evolution.
- **T43:** shares scalar expression and fixed-feedback numerical discipline. T44 is not a vector of independent iterated maps; each output reads neighboring cells.
- **T45:** owns continuous space/time, derivatives, initial/boundary conditions, solution concepts, solvers, and integration. Finite-difference schemes and continuum limits are typed relations, not identity.
- **Block CA:** the complex unitary variant updates pairs and awaits the block construction's own phase/schedule evidence.
- **Phyllotaxis:** sequential argmax placement and depletion update is only a list analogy.
- **Random fields and noise:** seed sampling and transition draws are separate random sources. Neither is numerical error.

## Current API Fit

| Construction concern | Fit | Evidence against current document |
|---|---|---|
| `DOMAIN`/`SHAPE` | `PARAMETERIZATION` for finite realizations; `PRINCIPLED EXTENSION` for native line | Finite 1D arrays fit explicit rings/segments but conflate support, work, crop, and trace (`simple_programs.md:115-198`) |
| `ALPHABET` | `DIRECT` responsibility / `PRINCIPLED EXTENSION` | The abstract value-set responsibility fits, but the document supplies no continuous interval/exact-real contract (`simple_programs.md:200-233`) |
| `SEED` | `DIRECT` responsibility / `PRINCIPLED EXTENSION` | Support/fill separation fits; exact continuous fields and random-real measures are absent (`simple_programs.md:235-290`) |
| `BOUNDARY` | `DIRECT` for the three explicit finite policies; `PRINCIPLED EXTENSION` for native line | Periodic matches Notes; fixed/reflective are distinct finite siblings. No-boundary integer-line semantics is absent (`simple_programs.md:292-358`) |
| `NEIGHBORHOOD` | `DIRECT` | Radius-one current-snapshot offsets fit (`simple_programs.md:360-494`) |
| `FRONTIER` | `DIRECT` for a finite time slice; `PRINCIPLED EXTENSION` for semantic unbounded `AllSites` | Full finite slices are directly expressible (`simple_programs.md:1502-1510,1538-1563`); T01's source interpretation and integer line remain extensions |
| Totalistic concept | `PARAMETERIZATION` at responsibility level | Permutation-invariant sum concept composes, but exact mean/divisor/range contract is absent (`simple_programs.md:1964-1995`) |
| Formulaic rule | `SEMANTIC MISMATCH` | Existing global-field callback is far too powerful and not stable closed data (`simple_programs.md:2036-2065`) |
| Same-site commit | `DIRECT` behavior / `PRINCIPLED EXTENSION` for typed result data | Parallel same-site writes are correct, but the document returns bare values rather than T01's explicit `Assign` (`simple_programs.md:2156-2199`) |
| Precision/realization | `PRINCIPLED EXTENSION` | The alphabet and rule schemas contain no exact/certified/tracked/represented feedback identity (`simple_programs.md:200-233,2036-2122`) |
| Stochastic local rule | `PRINCIPLED EXTENSION` | Distributional value return is documented (`simple_programs.md:2075-2122`), but randomness lacks coordinate-stable semantic draw records |
| Persistent trace | `PARAMETERIZATION` / `PRINCIPLED EXTENSION` | Initial-inclusive dense episodes help, but state/trace/render scope and exact values are conflated (`simple_programs.md:89-166`) |

## Current Runtime Fit

- `src/ca/alphabets.py:40-126` — `SEMANTIC MISMATCH`: every alphabet is finite; `float_range_alphabet` explicitly discretizes a range.
- `src/ca/loci.py:31-124,531-614` — `DIRECT` for finite coordinates and explicit periodic/fixed/reflective gathering; `PRINCIPLED EXTENSION` for integer-line/causal-window lowering. Runtime policy `none` raises on an out-of-bounds read and is not native infinity.
- `src/ca/neighborhoods.py:110-230,551-569` — `DIRECT`: radius-one old-snapshot reads are reusable.
- `src/ca/frontiers.py:37-80` — `DIRECT`: a full finite time slice is the correct finite source realization.
- `src/ca/rules.py:30-328` — `SEMANTIC MISMATCH`: aggregates are `sum/count`, formulaic rules are callbacks, and executable spatial paths end in finite lookup.
- `src/ca/specs.py:23-198` — `PRINCIPLED EXTENSION`: finite mechanics exist, but no semantic support, continuous value space, aggregate/map contract, numeric realization, seed measure, or typed local outcome exists.
- `src/ca/rollout.py:145-212,576-682,742-777` — `SEMANTIC MISMATCH`: family dispatch, `int64` coercion, integer aggregation, and binary lookup cannot execute T44.
- `src/ca/seeds.py:39-55,239-313,879-939` — `DIRECT` point-support responsibility; `SEMANTIC MISMATCH` for integer-only values/rendering and absent random-real seed semantics.
- `src/ca/rng.py:20-70` — `PARAMETERIZATION` as an episode-seed helper only; it lacks distribution, generator-version, coordinate/time draw identity, and exact sampling semantics.
- `RawEpisode`/`RawBatch` (`src/ca/specs.py:58-81`) — `PARAMETERIZATION` as finite containers, but integer rule IDs, ndarray state, and absent event/outcome records are insufficient.
- `src/ca/viz/export.py:177-184` — `SEMANTIC MISMATCH`: float/object states are rejected rather than exported through a typed continuous-field view.
- Concrete tests establish fixed/periodic/reflective gathering (`tests/test_loci.py:48-54`), radius-one old-time stencils (`tests/test_neighborhoods.py:86-119`), finite integer lookup and batching (`tests/test_rollout.py:263-310`), deterministic episode-level NumPy RNG derivation (`tests/test_rng.py:8-23`), integer point/Bernoulli seed rendering (`tests/test_seeds.py:71-82`), and deliberate rejection of float/object viewer states (`tests/test_viz_export.py:259-277`). No test covers interval state, rational field evolution, aggregate-then-map, fixed-precision divergence, weighted rules, additive continuous rules, coordinate-indexed stochastic draws, or typed gray-field views.

## Principles Audit

### Clear ontological basis

T44 is one fixed discrete lattice, one total real field, one immutable closed aggregate-plus-map program, old local reads, typed same-site results, and atomic parallel commit. Support, values, rule, seed, realization, numeric feedback, trace, and observations have independent identities.

### Minimal truthful reuse

T01 supplies the full update law and support/crop discipline. T41/T43 supply compatible exact value, closed syntax, primitive, evaluator, and validation responsibilities. T44 adds only the exact affine local aggregate, total continuous field carrier, composite closure, field numeric realization, and typed field observers. No new commit algebra, callback, or family rollout appears.

### Replayability and numerical honesty

Exact rows use reduced rationals; declared decimals retain spelling/provenance; represented recurrences record every feedback-relevant arithmetic choice. Random seed sampling and transition draws are reproducible semantic records. A raster, float tensor, or unspecified `N` result is never elevated to exact state.

### Mechanism separated from observation

Background, center, difference, class, localized structure, palette, parameter gallery, and PDE-limit records consume rules/runs. They never select rules, mutate fields, define support, or halt execution.

### Honest limits

The strict global topology, random-field law, difference convention, fixed machine reduction order, exact long-raster render recipe, irrational backend, page-325 range repair, and general coupled-map closure are not fully specified by the source. Goal 2 must expose typed unsupported/unknown/declared-reconstruction cases rather than supply hidden defaults.

## Re-Integration Audit

1. No prior primitive is invalidated. T44 confirms T01's fixed-lattice commit and T43's numerical-feedback split while showing that a scalar map's input may be an aggregate outside its own state interval.
2. `AllSites`, ordered reads, `Assign`, `AtomicEffectsUpdate`, total default fields, causal halos, exact values, closed expressions, and primitive/version responsibilities are reused without reinterpretation.
3. No exception flag, hidden periodic edge, field pack, callback, or type-specific rollout is introduced. Weighted, additive, stochastic, coupled, and block profiles are closed tagged siblings.
4. The total field plus immutable rule/realization contains everything needed to advance; time, history, parameter index, draws, and views remain trace/run data. A stochastic state transition additionally consumes an explicit event draw record.
5. Support, topology, values, control absence, representation, finite work window, and rendering remain separate.
6. Neighborhood aggregation/map evaluation/parallel commit are defining mechanics. Parameter scanning, class analysis, difference rendering, finite differences, and PDE solvers are correctly separated.
7. Tagged exact/declared/represented values, total-field codecs, rule syntax, boundaries, events, draws, and observers preserve every evidenced distinction.
8. No completed stage reopens. T01/T34/T41/T43 compose at existing responsibilities; T45 and block evidence remain pending.
9. Goal 2 gains shared continuous-field, local-numeric-rule, field-realization, run, stochastic-source, analysis, preset, and view work. The exact-real/backend synthesis question remains open.
10. The API becomes more coherent by expressing T44 as ordinary fixed-field assignment with a typed local numeric program. A T44 family branch or finite float alphabet would be less coherent and is rejected.

## Detailed Implementation Plan

1. Extend the exact/declared numeric layer with rational fields, declared decimals, enclosures, tracked values, and represented formats without implicit float coercion.
2. Extend fixed support with normalized total-field presentations, integer-line causal lowering, finite rings/segments, and independent work/crop/trace records.
3. Add closed exact affine neighborhood aggregates, aggregate-range analysis, aggregate references in scalar syntax, and replayable composite closure.
4. Lower T44 local results through the generic T01 fixed-field executor; lift exact/certified/tracked/represented/stochastic evaluation without a family branch.
5. Add initial-inclusive field runs, compact reconstruction, interruption/atomic-failure outcomes, identity/codecs, and finite-window queries.
6. Add typed raw/difference/background/center/mass/parameter/class views and continuous-field visualization adapters.
7. Add strict, weighted, and additive presets; two separately identified boiling records for literal threshold-conditional and strict-family reconstruction; noisy widened/partial presets; and a typed coupled-map relation/general closed constructor requiring a user-declared aggregate/map. Do not promise a book-exact coupled preset, and defer the complex-block sibling.
8. Add exact row/formula, boundary/halo, numeric divergence, stochastic replay, observer separation, codec, and no-cheating conformance tests.

## Goal 2 Implementation Stage

Build on synthesis-selected T01/T41/T43 foundations without modifying the current family dispatch as a new T44 path:

1. extend `src/ca/numeric_values.py` for rational/declared/enclosure/tracked/represented values;
2. extend `src/ca/function_expr.py` for aggregate references and required closed primitives;
3. extend `src/ca/state_spaces.py` and the T01 support module for integer lines, finite cycles/segments, causal halos, and crops;
4. add `src/ca/continuous_fields.py` for total-field presentations and tagged codecs;
5. add `src/ca/local_numeric_rules.py` for affine aggregates, divisors, range analysis, `AggregateThenMap`, and closed local expressions;
6. add `src/ca/continuous_ca.py` for specs, validation, field state, reads/results, assignment lowering, identity, and outcomes;
7. extend the family-neutral fixed-field executor for exact/certified/tracked/represented/stochastic local evaluation;
8. add or extend `src/ca/random_sources.py` for semantic distributions and coordinate/time-indexed draw realizations;
9. add `src/ca/field_runs.py`, `src/ca/field_analysis.py`, `src/ca/viz/continuous_ca.py`, and `src/ca/presets/continuous_ca.py`;
10. add `tests/test_t44_continuous_ca.py` plus shared aggregate, exact-field, stochastic, codec, and causal-lowering fixtures.

No dependency is needed for a correctness-first rational strict subset. Certified irrational/transcendental fields and page-325 `Exp` require the synthesis backend decision; unsupported exact cases remain typed.

### Required conformance tests

- Match exact mean rows through time 5, coefficient formula, symmetry, and mass conservation.
- Match the `3/2` rows including zeroes from exact `FractionalPart[1]`.
- Match `c=1/4` rows/background and general reduced-rational background periods.
- Detect a left-to-right in-place mutation with an asymmetric fixture.
- Match a literal Notes `RotateLeft`/`RotateRight` finite-cycle step.
- Distinguish ring, segment/exterior, integer-line causal crop, and render crop identities/trajectories.
- Prove a crop from the exact halo, including a nonzero evolving background.
- Round-trip exact field/rule/run/event records without JSON floats.
- Replay strict closure evidence; reject a trusted closure boolean and atomically roll back one-site failure.
- Ensure unchanged fields emit events and `h` events yield `h+1` snapshots.
- Ensure independent parameter runs/rule IDs and observer changes do not change traces.
- Distinguish divisor-three `{w,1,w}` from normalized weights and declared `1.13` from exact `113/100`.
- Give the two boiling rules distinct identities/provenance; at aggregate-plus-heat exactly `1`, require literal `if >1` to yield `1` and the strict unconditional reconstruction to yield `0`, while checking agreement away from that equality seam.
- Match the additive Pascal formula and reject conflation with strict `c=0`.
- Distinguish represented transitions by reduction/rounding locations; never call binary64 exact.
- Separate random seed sampling from transition draws; make coordinate-indexed draws enumeration invariant.
- Replay page-325 draws, reject hidden global RNG, and type out-of-range results without clamp.
- Encode continuous rule-90/rule-30 expressions as closed data, not callbacks.
- Keep finite-difference/PDE relations distinct from T45 identity.

## No-Cheating Checks

Reject:

- finite float alphabets, NumPy float/object arrays, bitmaps, or palettes as the mathematical continuum/field;
- callbacks, lambdas, `eval`, formula strings, host CAS objects, arbitrary reducers, or raster-decoded rules;
- a `continuous_ca` rollout branch or packing the whole field into a T43 scalar/vector;
- hidden periodic boundaries, fixed-zero padding, fixed capacities, or a crop presented as native support;
- integer division or implicit float conversion of the mean;
- hidden reduction order, FMA, precision, rounding, literal conversion, overflow, or `FractionalPart` semantics;
- normalized weighted means substituted for the source's divisor-three rule;
- applying the strict `3/2` or add-constant `FractionalPart` only above one, silently choosing the boiling equality convention, or adding implicit clamp/saturation/reflection/modulo;
- in-place/asynchronous updates or partial site commits;
- history, time, parameter index, RNG seed, random draws, or differences stored as strict field state;
- parameter galleries presented as one evolving field or observer output fed back into execution;
- convergence, cycle, background-period, class, or localized-structure halts;
- numerical error disguised as stochastic perturbation or stochastic draws without distribution/replay provenance;
- finite PRNG values called exact continuum samples;
- discrete probabilistic CA conflated with continuous-state noise;
- additive neighbor-sum rules conflated with strict mean rules;
- page-325 values silently clipped into `[0,1]`;
- finite rasters treated as exact periods, class proofs, or rule definitions;
- finite-difference approximations presented as PDE identity;
- source gaps filled by hidden backend defaults.

## Completion Requirements

- [x] Every strict main/Notes/actual-Index/split passage, history item, alias, figure, program, variant, relation, and false positive is dispositioned.
- [x] Support/value/control, source/read/aggregate/map/result/update, boundary/seed, precision/outcome, equality/serialization, trace, and observer semantics are explicit.
- [x] All six strict and two Notes assets have source-permitted exact or declared oracles, hashes, measurements, and source repairs.
- [x] T01/totalistic/T43/additive/coupled/probabilistic/T45 boundaries and reuse are explicit.
- [x] Current API/runtime fit, Goal 2 files/dependencies/tests, global ledgers, diff checks, and repository tests are integrated.

## Stage Results

T44 is complete. The literal 21-query search oracle reproduces all occurrence/line counts; every direct, abbreviated, alias, program, formula, parameter, history, application, stochastic, complex, PDE, and Index candidate was inspected and resolved into 25 evidence groups with zero open textual candidate. The strict construction is a total `[0,1]` field on a fixed ordered one-dimensional lattice, read synchronously at left/self/right, passed through a closed affine aggregate and scalar map, returned as same-site `Assign`, and committed through T01's existing atomic fixed-effects update. No control, hidden history, family dispatch, callback, float alphabet, or eleventh update law is introduced.

The exact semantic oracle passes the mean/coefficient/mass rows, `3/2` fractional rows, `c=1/4` field/background, rational additive residues, divisor-three weighted range, boiling equality seam, and high-precision noisy-range guard. All 17 included asset identities plus the material page-339 exclusion reproduce their bytes, dimensions, and SHA-256 values. The end-to-end raster oracle passes page 172/173/174/175 and both Notes assets, including an explicit page-175 observer discriminator. Strict topology remains honestly inferential; Notes separately prove a ring. Exact, certified/tracked work, and represented feedback stay distinct. Boiling literal/reconstructed rules, additive, coupled-map relation, noisy/probabilistic, complex-block, and PDE boundaries retain separate identities.

Verification passed: literal search oracle; exact semantic oracle; 17-asset/exclusion metadata oracle; core raster oracle; 25-group/source-line and Markdown-fence checks; `git diff --check`; and all `102` repository tests. No unresolved source candidate, renderer-dependent semantic claim, or prior-stage contradiction remains.

## Integration Results

T01's source/read/assignment/atomic-update law, T34's typed assignment responsibility, and T41/T43's closed numeric syntax and realization discipline compose without reinterpretation. T44 adds total continuous-field presentations, exact affine neighborhood aggregates, composite closure/range validation, field-wide numeric realization, initial-inclusive field runs, coordinate-stable stochastic draw records, and field observers. The provisional public transition-update family remains at ten members.

Global decisions D096-D102 record the field carrier, aggregate-plus-map contract, update reuse, support/realization/exterior/crop split, numerical feedback, trace/observer separation, and typed sibling relations. No completed stage is reopened. T45 remains categorically responsible for continuous space/time, differential operators, solution concepts, boundary/initial data, solvers, and integrators; finite differences and limits are relations rather than identity. The global plan and evidence index advance to 18 of 45 completed types, with T45 next.
