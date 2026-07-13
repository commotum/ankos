# 2-T01-ELEMENTARY

Status: **COMPLETE — EVIDENCE AND ARCHITECTURE RECLOSED**

Architecture authority: the T01 row and runner contract in `architecture-audit.md` supersede any executor/class claims below; evidence, construction facts, and conformance fixtures remain authoritative.

The evidence/search closure and conformance fixtures remain valid. D004/D007 and the Goal 2 handoff were revised and reclosed to separate generic atomic assignment from T01's fixed-lattice/table presets.

## Current Facts

- Exact catalog row: T01, CSV line 2, `Elementary Cellular Automata`.
- Complete taxonomy seed: `ref/notes/CA-Types.md:25-43`.
- Canonical source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md` (abbreviated `BOOK` below). It contains main text, Notes, Index, and Colophon through numbered line 22,498 (`wc -l` is 22,497 because the last line lacks a terminating newline).
- T01 is a construction family: a fixed one-dimensional binary lattice, one homogeneous radius-one rule, ordered left/self/right reads from the old state, same-site assignment, and synchronous parallel commit.
- An elementary rule is an arbitrary total map `{0,1}^3 -> {0,1}`. Its Wolfram number `n` is in `0..255`, and its oracle is `T_n(left,self,right) = (n >> (4*left + 2*self + right)) & 1`.
- The usual centered black cell, random fields, finite rings, and uniform or repeating backgrounds are initial-condition or realization choices. They are not part of elementary rule identity.
- Left/right reflection and black/white conjugation are analysis transformations on the same 256-rule space. They give 88 orbits, not 88 executable rules.
- The current runtime has correct ECA stencil geometry, but its exhaustive digit codec reverses asymmetric Wolfram rules, its arity-three exhaustive channel declares four rather than 256 rules, and generic lookup is not executable.

## Updated Assumptions

- “Elementary” is the book's later name for “two-color nearest-neighbor cellular automata”; direct-name searches alone are incomplete.
- The native mathematical support can be the integer line. A finite array, cyclic ring, fixed exterior, or displayed crop is an explicit computation/observation realization and must not silently replace that support.
- The semantic frontier is all sites, potentially infinite. A reference executor enumerates only an explicit finite realization or the exact causal cone required by a finite observation request.
- Rule-table digit significance is not the same concern as neighborhood ordering. Both must be explicit and validated together.
- Additive, totalistic, symmetric, blank-preserving, and one-input rules are restrictions or alternate descriptions of the same table construction. They require no specialized executor.
- T01 validates `all sites -> ordered local read -> exhaustive lookup -> Assign -> parallel update` for fixed-lattice assignment systems only. Later types may reopen or split this algebra.

## Big Picture Objective

Exhaustively recover the elementary cellular automaton construction and every construction-relevant local variant, then produce the smallest honest fixed-lattice synchronous-assignment baseline and a Goal 2 conformance handoff without an ECA-specific rollout.

## Catalog Identity

- Stable ID: T01.
- Exact name: Elementary Cellular Automata.
- Taxonomy section: 1, `ref/notes/CA-Types.md:25-43`.
- Entry kind: construction plus a finite rule family. Seed classes, boundary realizations, restrictions, equivalent rule descriptions, and observables remain separate axes.
- Search vocabulary: elementary cellular automaton(s), elementary rule(s), binary cellular automata (Index alias), two-color/two-colour nearest-neighbor cellular automata, black-and-white CA, one-dimensional/1D line, fixed/rigid array, `k=2,r=1`, three-cell neighborhood, eight cases, 256 rules, Wolfram number/order, binary digits, parallel/synchronous/old values, single black cell, random initial condition, periodic/cyclic/infinite background, rule equivalence/conjugate/reflection, rules 30/45/51/60/90/105/110/150/170/204/240/250/254, additive/linear/XOR, totalistic, symmetric, and blank-preserving. The acronym `ECA` has no standalone canonical-book match.

## Search Log

### Sources and reproducible method

The complete taxonomy section was read before searching. Fixed-string, case-insensitive `rg -n -i -F '<term>' BOOK` searches were run for every vocabulary family below; regex was used only to group spelling or spacing variants. Every hit was inspected in context with numbered lines. Cross-references were followed to Notes for pages 53, 55, 58, 60, 264, 866–867, 883, 951–952, 955, and 1087. Index entries were navigation only.

| Query family | Literal/variant terms inspected | Resolution |
|---|---|---|
| Direct identity | `elementary cellular`, `elementary rule`, `binary cellular automata`, `two-color`, `2-color`, `two colors and nearest neighbors`, `k = 2, r = 1`, `k=2,r=1`, standalone `ECA` | Included identity at `11635`, `11050`, `17993`; Index alias at `20914`; no standalone acronym match; behavioral and historical mentions dispositioned below |
| State/support | `line of cells`, `single line of cells`, `one-dimensional`, `fixed array`, `rigid array`, `black or white`, `0 corresponds to a white cell`, `same rule` | Included at `422`, `538`, `982`, `1254`, `2168`, `8832`, `10899` |
| Local map | `cell and its two neighbors`, `immediate left and right neighbors`, `each possible combination`, `eight possible`, `3-cell`, `range r` | Included at `422-430`, `712-720`, `8148-8152`, `10988`, `11897-11900`, `13513-13520` |
| Enumeration | `256 possible`, `256 rules`, `0 to 255`, `base 2`, `binary digits`, `IntegerDigits[num, 2, 8]`, `Boolean functions`, `rule orderings` | Included at `718-720`, `10906-10916`, `11846`, `11897`, `17993` |
| Schedule | `updated in parallel`, `parallel at every step`, `old values of neighbors`, `simultaneous`, `synchronous` | Included at `850-854`, `10984`, `1254`, `16446`; hardware-bit parallelism excluded |
| Equivalence | `fundamentally inequivalent`, `rule equivalences`, `interchanging black and white`, `left and right`, `conjugates`, `reflections`, `left-right symmetry` | Included at `746`, `11636-11637`; rule-specific repetitions are duplicates |
| Restrictions/variants | `special rules`, `additive`, `generalized additivity`, `one-sided additive`, `partially additive`, `totalistic`, `blank backgrounds stay unchanged`, `depend on one cell` | Included at `1346`, `11638`, `11855`, `11897`, `14350-14366`, `14376`, `17640`, `17663`, `17956`; terminology conflict preserved |
| Seeds/realizations | `single black cell`, `single 1 surrounded by 0`, `random initial`, `white background`, `boundary condition`, `cyclic`, `periodic`, `leftmost`, `rightmost`, `infinite`, `assumed cyclic`, `repeating background` | Included at `418`, `746`, `2706-2712`, `3026`, `3042`, `3126-3128`, `10986`, `11077-11087`, `11124`, `11128-11140`, `11250-11256`, `14336` |
| Named examples | `rule 254`, `rule 250`, `rule 90`, `rule 30`, `rule 110`, special-rule numbers | Canonical mechanics/captions included at `418-518`, formulas at `11209-11240`, special rules at `11638`; behavior-only repetitions excluded |

Representative direct-hit counts on the canonical monolith were recorded before context filtering: `elementary cellular` 64, `elementary rule` 42, `two-color` 6, `2-color` 13, `nearest-neighbor` 22, `nearest neighbor` 32, `256 possible rules` 2, `256 rules` 6, `left-right` 4, and `additive rules` 30. Named-rule searches were deliberately broad (`rule 30` 181, `rule 90` 101, `rule 110` 138) so construction statements could be separated from behavior and application mentions.

### Repository and split-file audit

- The canonical monolith is authoritative. Main text runs through line 10,621, `General Notes` begins at 10,623 and runs through 20,825, and the actual Index begins at 20,826.
- Split chapter hits in Chapters 2, 3, 6, and 9 map back to the monolith (for example split Chapter 2 line 21 -> monolith `422`; split Chapter 3 lines 29/35/37/63 -> `712/718/720/746`). They add no unique excerpt.
- Split boundaries are malformed: Chapter 12 continues into Notes (`CHAPTERS/12-C...` line 2004 -> monolith `10623`, line 2280 -> `10899`, and line 3462 -> `12081`); `BACK-MATTER/Notes/Notes.md` contains only monolith `12085`; `BACK-MATTER/Index/Index.md` contains monolith `12089-17442`; and `BACK-MATTER/Colophon/Colophon.md` begins at monolith `17444`, contains the actual Index header at its line 3383 / monolith `20826`, and then the actual Colophon header at its line 5015 / monolith `22458`. All were searched as navigation aids; none overrides monolith provenance.
- `ANKoS-Atlas.md` mentions rules 30 and 110 as examples/behavior, but adds no construction semantics.

### Candidate disposition and closure

| Disposition | Canonical candidates | Reason |
|---|---|---|
| Included construction evidence | `418-430`, `538`, `712-720`, `746`, `850-854`, `982-984`, `1254-1256`, `1346-1350`, `2168`, `2706-2712`, `3026`, `3042`, `3126-3128`, `8148-8152`, `8832`, `10899-10916`, `10984-10992`, `11050-11056`, `11077-11087`, `11124`, `11128-11140`, `11209-11256`, `11635-11638`, `11846-11900`, `13513-13520`, `14336`, `14350-14366`, `14376`, `16446-16448`, `17640`, `17663`, `17955-17956`, `17993` | Each establishes identity, state/support, local reads, table/order, commit, seed/realization separation, restriction, equivalence, or exact example |
| Corroborating captions/examples retained as conformance evidence | `440`, `448-450`, `466-472`, `498`, `518` | Precise rule mechanics and seed conventions for 250, 90, 30, and 110; not separate executors |
| Inspected duplicate/corroboration | `724-768`, `1342`, `1350`, `1533`, `3190-3192`, `8318`, `10946-10952`, `11128-11140`, `11276`, `11283-11295`, `14487`, `18337` | Repeats an included construction fact, implementation formula, equivalence, seed, or count; line references retained here so no hit is silent |
| Behavior/property only | `784-808`, `1342`, `4078`, `4124`, `5212-5216`, `5456-5460`, `5552`, `6912`, `7428-7462`, `8326-8382`, `9058`, `9811`, `11889`, `12676`, `14417`, `14537`, `14673`, `16129`, `17636-17663`, `17700-17710`, `20303` | Complexity class, universality, reversibility, conservation, density, period, predecessor, cryptography, or visualization does not alter construction; alternate rule formulas already captured where relevant |
| Adjacent construction/emulation | mobile/Turing/substitution/higher-color/totalistic/2D/continuous references, `8008-8010`, `8438-8480`, `17688`, `18109`, `18167`, `18457+`, `18976`, `20600` | Cross-type construction or emulation is not native T01 coverage; contrast sentences at `850`, `982`, and `16446` were retained only for the axis they establish |
| Optimization, not semantics | `10996-11000` | Bit packing/bitwise parallel hardware is explicitly an implementation optimization, not state or schedule semantics |
| Corrupted or navigation-only | corrupted repeated rule-30 table around `11007`; Index/Colophon `20826-22498` | Clean equivalents exist at `10906-10916`, `10988`, and `11229-11240`; Index links were followed but are not primary evidence |

The terminology conflict is explicit: `14350` gives the strict eight modulo-2 additive rules and omits rule 105, while `11855` and `17956` call rule 105 additive as negated XOR. Goal 2 must not silently merge strict linearity with affine/negated-XOR or generalized additivity.

**Search closure:** every candidate produced by the logged direct names, aliases, named examples, parameter terms, captions, Notes, Index, and followed cross-references is included, recorded as a duplicate, or excluded with a reason. There are zero unresolved T01 evidence candidates.

## Book Excerpts

All excerpts below are verbatim from `BOOK`; OCR defects are preserved and called out rather than silently repaired.

### E01 — line, values, seed, ordered local read, and next-cell assignment

`BOOK:418-430`, Chapter 2, “How Do Simple Programs Behave?” establishes the base construction and rule 254 example:

> At the first step the cell in the center is black and all other cells are white. Then on each successive step, a particular cell is made black whenever it or either of its neighbors were black on the step before.
>
> The cellular automaton consists of a line of cells, each colored either black or white. At every step there is then a definite rule that determines the color of a given cell from the color of that cell and its immediate left and right neighbors on the step before.
>
> The top row in each box gives one of the possible combinations of colors for a cell and its immediate neighbors. The bottom row then specifies what color the center cell should be on the next step in each of these cases. In the numbering scheme described in Chapter 3, this is cellular automaton rule 254.

### E02 — canonical named-rule mechanics and captions

`BOOK:440`, `448-450`, `466-472`, `498`, and `518` give executable examples without changing the construction:

> The rule makes a particular cell black if either of its neighbors was black on the step before, and makes the cell white if both its neighbors were white. Starting from a single black cell, this rule leads to a checkerboard pattern. In the numbering scheme of Chapter 3, this is cellular automaton rule 250.
>
> The rule in this case is that a cell should be black whenever one or the other, but not both, of its neighbors were black on the step before. ... The particular rule used here can be described by the formula  $a_i' = Mod[a_{i-1} + a_{i+1}, 2]$ . In the numbering scheme of Chapter 3, it is cellular automaton rule 90.
>
> The rule used—that I call rule 30—is of exactly the same kind as before, and can be described as follows. First, look at each cell and its right-hand neighbor. If both of these were white on the previous step, then take the new color of the cell to be whatever the previous color of its left-hand neighbor was. Otherwise, take the new color to be the opposite of that.
>
> The rule used is of the same type as in the previous examples, and the cellular automaton is again started from a single black cell. ... the cellular automaton shown here is rule 30.
>
> the specific rule used—that I call rule 110—takes the new color of a cell to be black in every case except when the previous colors of the cell and its two neighbors were all the same, or when the left neighbor was black and the cell and its right neighbor were both white.
>
> The picture is obtained by applying the simple rule shown for a total of 150 steps, starting with a single black cell. ... In the scheme defined in Chapter 3, the rule is number 110.

### E03 — one homogeneous rule

`BOOK:538`, same chapter:

> all the cells in a cellular automaton follow exactly the same rule

### E04 — eight cases, 256 tables, and rule-number digits

`BOOK:712-720`, Chapter 3, “More Cellular Automata”:

> The overall structure of these rules is the same in each case; what differs is the specific choice of new colors for each possible combination of previous colors for a cell and its two neighbors.
>
> There turn out to be a total of 256 possible sets of choices that can be made. And following my original work on cellular automata these choices can be numbered from 0 to 255
>
> The number assigned is such that when written in base 2, it gives a sequence of 0's and 1's that correspond to the sequence of new colors chosen for each of the eight possible cases covered by the rule.

### E05 — survey seed and 88 equivalence orbits

`BOOK:746`, same section:

> The behavior of all 256 possible cellular automata with rules involving two colors and nearest neighbors. In each case, thirty steps of evolution are shown, starting from a single black cell. Note that some of the rules are related just by interchange of left and right or black and white (e.g. rules 2 and 16 or rules 126 and 129). There are 88 fundamentally inequivalent such elementary rules.

### E06 — all-site parallel schedule and fixed topology

`BOOK:850-854`, “Mobile Automata”; `982-984`, “Substitution Systems”; `1254-1256`, Chapter 4; and `2168`, Chapter 5:

> One of the basic features of a cellular automaton is that the colors of all the cells it contains are updated in parallel at every step in its evolution.
>
> cellular automata, mobile automata and Turing machines all have in common ... a fixed array of cells. ... the colors of these cells can be updated according to a wide range of different possible rules, [but] the underlying number and organization of cells always stays the same.
>
> All their elements ... are always arranged in a rigid array, and are always updated in parallel at each step.
>
> The cellular automata that we have discussed so far in this book are all purely one-dimensional, so that at each step, they involve only a single line of cells.

### E07 — restricted intersections are rule subsets

`BOOK:1346-1348`, Chapter 3 history:

> at first I looked only at the 32 rules which had left-right symmetry and made blank backgrounds stay unchanged.

The sentence identifies the T06/T07 intersection inside the 256 tables; it does not change the executor.

### E08 — initial conditions are independent experiments

`BOOK:2706-2712`, Chapter 6, “Starting from Randomness”:

> we have usually started with just a single black cell.
>
> My purpose in this chapter is ... to consider completely random initial conditions, in which, for example, every cell is chosen to be black or white at random.
>
> a cellular automaton ... starts from a typical random initial condition, then evolves ... according to the very simple rule that a cell becomes black if either of its neighbors are black.

### E09 — finite rings and infinite periodic backgrounds

`BOOK:3026`, `3042`, and `3126-3128`, Chapter 6:

> cellular automata that have a limited number of cells. In each case the cells are in effect arranged around a circle, so that the right neighbor of the rightmost cell is the leftmost cell and vice versa.
>
> In each case the right neighbor of the rightmost cell is taken to be the leftmost cell and vice versa.
>
> initial conditions which consist just of a fixed block of cells repeated forever will lead to simple repetitive behavior. ... The right-hand neighbor of the rightmost cell in any particular block is the leftmost cell in the next block, but since all the blocks are identical, this cell always has the same color as the leftmost cell in the block itself. And as a result, the block evolves just like one of the systems of limited size

### E10 — infinite local state

`BOOK:8832`, Chapter 11:

> even a one-dimensional cellular automaton can be viewed as updating an infinite sequence of cells at every step in its evolution. But one feature of this process is that it is fundamentally local: each cell behaves in a way that is determined purely by cells in a local neighborhood around it.

### E11 — concrete state, rule table, and one-step implementation

`BOOK:10899-10916`, Notes for Chapter 2:

> It is convenient to represent the state of a cellular automaton at each step by a list such as  $\{0, 0, 1, 0, 0\}$ , where 0 corresponds to a white cell and 1 to a black cell.
>
> rule 30 ... corresponds to the list {0, 0, 0, 1, 1, 1, 1, 0}.

```text
ElementaryRule[num_Integer] := IntegerDigits[num, 2, 8]
CAStep[rule_List, a_List] :=
rule[[8 - (RotateLeft[a] + 2 (a + 2 RotateRight[a]))]]
```

### E12 — old-snapshot commit, finite boundary, and exact bit index

`BOOK:10984-10992`, same Notes section:

> cellular automaton rules are always defined to use the old values of neighbors in determining the new value of any particular cell. ... it is necessary to store the old value ... (Another approach ... is to maintain two copies of the array of cells, and to interchange pointers to them after every step ...)
>
> Since in a practical computer one can use only a finite array of cells, one must decide how the cellular automaton rule is to be applied to the cells at each end of the array. ... we effectively use a cyclic array, in which the left neighbor of the leftmost cell is taken to be rightmost cell, and vice versa.
>
> if the value of a particular cell is q, the value of its left neighbor is p, and the value of its right neighbor is r, then the element at position 8 - (r + 2(q + 2p)) in the list obtained from ElementaryRule will give the new value of the cell.

Thus the least-significant rule bit has index `right + 2*self + 4*left`, and the displayed digit order is `111,110,101,100,011,010,001,000`.

### E13 — typed elementary parameters and seed/background forms

`BOOK:11050-11053` and `11077-11087`, built-in function Notes:

```text
n                         k = 2, r = 1, elementary rule
{n, k}                    general nearest-neighbor rule with k colors
{n, k, r}                 general rule with k colors and range r
```

```text
{a_1, a_2, ...}           explicit list of values a_i, assumed cyclic
{{a_1, a_2, ...}, b}      values a_i superimposed on a b background
{{a_1, a_2, ...}, {b_1, b_2, ...}}
                           values a_i superimposed on a background of
                           repetitions of b_1, b_2, ...
```

### E14 — exact causal extent and canonical short rule-30 trace

`BOOK:11124` and `11128-11140`:

> With an initial condition specified by an aspec of width w, the region that can be affected after t steps by a cellular automaton with a rule of range r has width w + 2rt.
>
> This gives the array of values obtained by running rule 30 for 3 steps, starting from an initial condition consisting of a single 1 surrounded by 0's.

```text
{{0, 0, 0, 1, 0, 0, 0},
 {0, 0, 1, 1, 1, 0, 0},
 {0, 1, 1, 0, 0, 1, 0},
 {1, 1, 0, 1, 1, 1, 1}}
```

> If all values in the initial condition are given explicitly, they are in effect assumed to continue cyclically.
>
> This starts from  $\{1,1\}$  on an infinite background of repeating  $\{1,0,1,1\}$  blocks.

### E15 — formal recurrence and equivalent table/formula descriptions

`BOOK:11209-11240`, Notes:

> The value a[t, i] for a cell on step t at position i ... can be obtained from the definition

```text
a[t, i] := f[a[t-1, i-1], a[t-1, i], a[t-1, i+1]]
```

> Different rules correspond to different choices of the function f. ... One can specify initial conditions for example by  $a[0, 0] = 1; a[0, \_] = 0$.
>
> The definition of the function f for rule 90 ... is essentially just a look-up table. But it is also possible to define this function in an algebraic way

```text
f[p_, q_, r_] := Mod[p + r, 2]
Rule 254: Or[p, q, r]
Rule 250: Or[p, r]
Rule 90: Xor[p, r]
Rule 30: Xor[p, Or[q, r]]
Rule 110: Xor[Or[p, q], And[p, q, r]]
```

The formulas are inspectable alternate descriptions that must lower to the same eight-case table, not unrestricted callbacks.

### E16 — native infinite support versus explicit periodic realization

`BOOK:11250-11256`, Notes:

> the state space of a 1D cellular automaton with an infinite number of cells can be viewed as a Cantor set. The cellular automaton rule then corresponds to a continuous mapping of this Cantor set to itself (continuity follows from the locality of the rule).
>
> Periodic boundary conditions are used, so that the a[t, i] can be viewed as corresponding precisely to digits of rational numbers.

### E17 — identity, exact equivalence transforms, and one-input rules

`BOOK:11635-11638`, Notes for page 53/55:

> I termed two-color nearest-neighbor cellular automata "elementary" to reflect the idea that their rules are as simple as possible.
>
> the second entry is the rule obtained by interchanging black and white, the third entry is the rule obtained by interchanging left and right, and the fourth entry the rule obtained by applying both operations.
>
> Rule 51: complement; rule 170: left shift; rule 204: identity; rule 240: right shift. These rules only ever depend on one cell in each neighborhood.

The OCR string for the black/white list transform on line 11637 is malformed (`1 Reverse[list]`), so the unambiguous main-text operation and truth-table oracle govern.

### E18 — general cardinality and ordered exhaustive implementation

`BOOK:11897-11900`, Notes for page 60:

> Allowing k possible colors for each cell and considering r neighbors on each side, there are  $k^{k^{2r+1}}$  possible cellular automaton rules in all ... (For k=2, r=1 there are therefore 256 possible rules altogether, of which 16 are totalistic.)
>
> With k colors and r neighbors on each side, a single step in the evolution of a general cellular automaton is given by

```text
CAStep[CARule[rule_List, k, r], a_List] :=
  rule[[-1 - ListConvolve[k^Range[0, 2r], a, r + 1]]]
```

### E19 — explicit offset/configuration order and rule number

`BOOK:13513-13520`, general-rule Notes:

> One can specify the neighborhood for any rule in any dimension by giving a list of the offsets for the cells used to update a given cell. For 1D elementary rules the list is ... In this book such offset lists are always taken to be in the order given by Sort ... One can specify a neighborhood configuration by giving in the same order as the offset list the color of each cell in the neighborhood.
>
> If a cellular automaton rule takes the new color of a cell with neighborhood configuration IntegerDigits[i, k, Length[os]] to be u[i+1], then one can define its rule number to be FromDigits[Reverse[u], k].

The first displayed 1D offset is OCR-mangled as `(-1, 0)`; the surrounding recurrence and exact index establish `[-1,0,+1]` unambiguously.

### E20 — boundary choices are distinct

`BOOK:14336`, Notes:

> 0's outside of a width n can be implemented by applying  $BitAnd[a, 2^n - 1]$  at each step. Cyclic boundary conditions can be implemented efficiently

This distinguishes a fixed-zero exterior from a cyclic finite topology.

### E21 — strict, affine, and generalized additivity variants

`BOOK:14350-14366`, `14376`, `17640`, `17663`, `11855`, and `17956`:

> Of the 256 elementary cellular automata 8 are additive: {0, 60, 90, 102, 150, 170, 204, 240}.
>
> each [additive rule is] obtained by taking the cells in the neighborhood and adding them modulo k with weights between 0 and k-1.
>
> $\phi[u \oplus v] = \phi[u] \oplus \phi[v]$
>
> some elementary rules show additivity with respect to other addition operations. An example ... is rule 250 with  $u \oplus v$  taken as Max[u, v] (Or).
>
> Rule 30 can be written in the form  $p \supseteq (q \lor r)$ ... and thus exhibits a kind of one-sided additivity on the left.
>
> Rule 45 shares with rule 30 the property of one-sided additivity.
>
> rules 60, 105 and 150 are additive, like rule 90.
>
> Rules 150 and 105 are additive, and correspond to Xor and its negation.

The strict eight-rule linear list, affine/negated-XOR usage for 105, generalized operation for 250, and one-sided property for 30/45 are recorded as distinct predicates/alternate descriptions.

### E22 — parallel and sequential update are different systems

`BOOK:16446-16448`, Notes, “Sequential cellular automata”:

> Ordinary cellular automata are set up so that every cell is updated in parallel at each step, based on the colors of neighboring cells on the previous step. But ... one can also consider sequential cellular automata ... The behavior of such systems is usually very different ... because ... the new color of a particular cell can depend on new rather than old colors of neighboring cells.

### E23 — Boolean-function closure

`BOOK:17993`, Notes:

> For 1 step, the elementary cellular automaton rules are exactly the 256 n = 3 Boolean functions.

## Construction Model

### Native semantics

| Dimension | Reconstructed T01 semantics |
|---|---|
| State | `STATE = SUPPORT + VALUES`; no control. Support/topology is a fixed ordered 1D regular lattice. Values are a total binary field on that support. |
| Support variants | Canonical mathematical support is `Z`. Exact finite constructions include a cycle `Z/nZ`; a finite segment requires an explicit exterior/boundary rule. Support size and adjacency do not change during evolution. |
| Alphabet | Exactly `{0,1}` (white/black). Palette is representation, not semantics. |
| Active loci | Every site of the semantic support at every step. A finite observation executor evaluates the finite target/cause region requested; it does not redefine the semantic frontier. |
| Read | Ordered old-snapshot triple `(x-1,x,x+1)`, equivalently `(left,self,right)`. Read order is part of rule-code interpretation. |
| Rule | One homogeneous total table `T:{0,1}^3->{0,1}`. Rule number `n` is the eight-bit table with oracle `T_n(l,c,r)=(n>>(4l+2c+r))&1`. |
| Result | Explicit same-site `Assign(value)` for the active locus. |
| Update | Apply all assignments atomically/parallel to a fresh state. No update may observe another result from the same step. There is exactly one assignment per site and therefore no conflict policy is exercised. |
| Successor/halting | One deterministic successor per state; no branching, rejection, or intrinsic halt. A run horizon is an observation request. |
| Seed | Independent initial field. Centered one on zero background is a canonical example; arbitrary explicit, random, uniform, and periodic fields use the same program. |
| Boundary/realization | None on `Z`; wraparound on a finite cycle; an explicit fixed exterior is a distinct finite realization. For a finite observed window and horizon `h`, a radius-`h` initial halo yields an exact crop. |
| Observables | Spacetime diagram, page crop, density/classification, symmetry orbit, period, and causal-cone crop are downstream trace/analysis, not program state. |

### Rule-code invariants

- `arity = 3`, `|A| = 2`, neighborhood states `S = 2^3 = 8`, rule count `R = 2^8 = 256`.
- Ordered pattern index is `4*left + 2*self + right`; bit zero is `000`, bit seven is `111`.
- Padded display order is `111,110,101,100,011,010,001,000`.
- Valid rule IDs are exactly `0..255`; leading zero bits are semantically required.
- Reflection maps inputs `(l,c,r)` to `(r,c,l)`. Black/white conjugation maps `T` to `1-T(1-l,1-c,1-r)`. The group they generate has 88 orbits over all 256 tables (mechanically verified during this stage).

### Variant disposition

| Variant | Semantic relation |
|---|---|
| Centered-one, random, uniform, explicit, or repeating initial field | Seed choice; same executor and rule |
| Infinite line, finite cycle, finite segment with fixed exterior | Explicit support/realization choice; never an implicit padding trick |
| Left/right reflection, black/white conjugation, both | Rule-table transformation/analysis; same executor |
| Left-right symmetric or blank-preserving | Validated table predicate/restriction; T07/T06 retain separate catalog traceability |
| Totalistic elementary rules | Alternate restricted rule description; T03 covers general totalistic construction |
| Strict additive, affine/negated-XOR, generalized-operation, one-sided additivity | Distinct table properties or alternate descriptions; all lower to explicit tables |
| Rules 51/170/204/240 | One-input degeneracies within the arity-three table family, not reduced neighborhoods at execution |
| Rule 30/90/110/250/254 | Canonical conformance presets/examples, not rollout families |
| Sequential cellular automata | Different update semantics and therefore a different construction, not a T01 option |

## Corrected Architecture and Goal 2 Handoff

T01 is the cellular-automaton preset of the common SimpleProgram runner: discrete fixed `t+1D` DOMAIN, Boolean ALPHABET, all-site FRONTIER, ordered radius-one NEIGHBORHOOD, complete scalar-label RULE, and snapshot-parallel UPDATE. Its evidence and tests remain unchanged; the only correction is that this tuple is a preset of the runner rather than the first separate executor algebra.

Revised G2-T01 fixes table cardinality/ordering, makes support/realization/trace explicit, implements the typed axes and branch-free runner, and exposes `elementary(n)` as ordinary preset data. It must leave extension points in ALPHABET/FRONTIER/NEIGHBORHOOD/RULE/UPDATE structural rather than CA-family branches.

## Historical Current API Fit (Superseded only on executor classification)

| Construction element | Fit | Evidence and consequence |
|---|---|---|
| `[t,x,0,0]` trace address | DIRECT | Lossless for a 1D finite trace (`simple_programs.md:1-24,115-167,2140-2152`); address is not topology |
| Native fixed integer-line support | PRINCIPLED EXTENSION | Current `SHAPE` is finite (`:138-198`); it is a valid explicit realization/window, not native infinity |
| Current configuration | DIRECT | A field-valued binary snapshot fits (`:87-113,200-230`); persistent trajectory must remain trace rather than Markov state |
| Boolean alphabet | DIRECT | Explicit finite alphabet fits (`:200-230`) |
| Control | NOT APPLICABLE | T01 has no head, pointer, counter, or hidden memory |
| Centered point seed | PARAMETERIZATION | Selector plus fill expresses it (`:235-290`); seed must remain separate |
| Boundary | PARAMETERIZATION for finite realizations | `PERIODIC` and `FIXED` can express explicit finite choices (`:292-358`); no native boundary exists on `Z` |
| Ordered radius-one current read | DIRECT/PARAMETERIZATION | Relative selectors express `[-1,0,+1]` (`:360-394,595-645,703-720`) when order is pinned |
| Semantic all-sites frontier | PRINCIPLED EXTENSION | Full finite next slice fits (`:1502-1510,1538-1563`), but unbounded `AllSites` and observation lowering are not separated |
| Exhaustive table | DIRECT conceptually | Schema has exhaustive rules (`:1767-1829`) but lacks a normative Wolfram codec |
| Rule-number codec | PRINCIPLED EXTENSION | Must be explicit, total, bidirectional, and validated against ordered reads |
| `Assign` result | PRINCIPLED EXTENSION architecturally | Bare next value has the correct T01 outcome but Principles 3/4 require an explicit typed result |
| Parallel commit | DIRECT for behavior | Current same-site fresh-slice semantics fit (`:1767-1793,2156-2199`) once made an explicit update algebra |
| Deterministic successor | DIRECT | One next state; no halt/branch/RNG/solver |
| Spacetime/crop/equivalence | NOT APPLICABLE to execution | Belongs after `program -> trace`, not in program state |

## Historical Current Runtime Fit (Evidence Retained)

| Component | Fit | Exact finding |
|---|---|---|
| `alphabets.boolean()` | DIRECT primitive, incomplete wiring | Correct `{0,1}` at `src/ca/alphabets.py:129-143`; `Dynamics` has no alphabet and rollout merely coerces `int64` (`specs.py:23-55`, `rollout.py:576-588`) |
| `loci.coordinate_space((n,))` | PARAMETERIZATION / SEMANTIC MISMATCH if native | Correct finite centered x realization and gathers (`loci.py:31-125,179-221,531-614`); cannot stand for `Z` without explicit lowering |
| `seeds.point(... value=1, fill=0)` | DIRECT | Correct canonical finite seed and separation (`seeds.py:1-19,260-313,879-930`) |
| `neighborhoods.eca()` | DIRECT geometry | Defaults select `[left,self,right]` at current time (`neighborhoods.py:551-569`); elementary preset must pin radius 1/time 0/center true |
| `frontiers.time_slice(shape)` | DIRECT finite behavior | Full finite slice (`frontiers.py:54-80`), though rollout only family-checks it (`rollout.py:825-831`) |
| `rules.exhaustive` cardinality | SEMANTIC MISMATCH | It records `state_count=alphabet_size`, ignoring component arity (`rules.py:173-195`); one binary arity-three channel makes `lookup` derive `S=2,R=4`, not `S=8,R=256` (`:262-295`) |
| Exhaustive digit codec | SEMANTIC MISMATCH | `_channel_state` weights lex reads `[1,2,4]` (`rollout.py:742-760`), producing `left+2*self+4*right`; Wolfram requires `4*left+2*self+right`. Current rule 30 is reflected to rule 86. |
| Generic lookup execution | SEMANTIC MISMATCH | Scalar/batch rollout whitelists named families and rejects `lookup` (`rollout.py:145-212`); `apply_rule` repeats named dispatch (`:292-331`); specs resolve only six Phase 1 families (`specs.py:117-181`) |
| Shared spatial step mechanics | DIRECT candidate | Reads one previous array and creates a next array with boundary gathering (`rollout.py:576-729`); must be reached through semantics rather than family name |
| `Dynamics` | PARAMETERIZATION / PRINCIPLED EXTENSION | Finite `t+1d` and shape fit a realization, but alphabet, semantic support, result/update, and observation extent are absent (`specs.py:23-55`) |
| Raw episode/batch/coords | DIRECT downstream | Preserve as trace boundary (`specs.py:58-81`, `rollout.py:40-142,215-289`) |
| datasets/RNG/viz | NOT APPLICABLE | Dataset recipes and rendering are downstream; deterministic transition does not use RNG. Random initial condition belongs to seed sampling. |

### Test fit

- Current direct pieces: centered x coordinates (`tests/test_loci.py:16-32`), finite boundary policies (`:48-54`), radius-one ECA geometry (`tests/test_neighborhoods.py:86-99`), and point seed `[0,1,0]` (`tests/test_seeds.py:65-74`).
- The named `eca` test at `tests/test_neighborhoods.py:101-119` deliberately uses radius 2 and time offset -1. It tests the general stencil convenience, not strict T01.
- Rule tests assert counts for current named families but never generic exhaustive lookup (`tests/test_rules.py:9-45`).
- The only spatial rollout semantic oracle is rule-zero extinction for Dyadrads (`tests/test_rollout.py:263-283`). Its nonzero batch test compares batch against the same scalar implementation (`:285-310`), so it cannot catch shared bit-order defects.
- There is no ECA rule-number, asymmetric trajectory, old-snapshot, 88-orbit, or preset test. The current suite passed (`uv run pytest -q`: `102 passed`), which proves no T01 rollout conformance.

## Historical Principles Audit (Superseded only on executor classification)

| Principle | T01 result |
|---|---|
| 0–2 | Evidence validates one substantive fixed-lattice assignment executor. Adding an ECA branch would violate shared execution; declaring this algebra universal would exceed the evidence. |
| 3–4 | Frontier selects all sites, neighborhood reads ordered old values, rule returns typed `Assign`, update commits in parallel. Bare values are not declared universal effects. |
| 5 | State visibly contains fixed topology and binary values; T01 has no control. No history is hidden in rollout. |
| 6, 8, 12 | `x` is a valid trace address here, but semantic topology, finite realization, and emitted spacetime tensor remain separate. |
| 7 | The fixed lattice stays fixed. Finite crop, causal halo, cyclic ring, and fixed exterior are explicit boundaries, never fake native capacity. |
| 9 | Alphabet, seed, and observation compose independently; arity and table cardinality, topology and reflection, and support and boundary carry strict invariants. |
| 10 | `elementary(n)` may be a discoverable strict preset only if it returns the ordinary shared spec. |
| 11 | Synchronous old-snapshot commit is defining semantics. Bit packing, vectorization, batching, and display crop are incidental algorithms. |
| 13–14 | Rule 30 is the mandatory adversarial example because symmetric/trivial rules conceal digit reversal. Any ECA-only reversal or family switch is design failure. |
| 15 | Canonical table cases, rule-30 rows, boundary/halo semantics, rule restrictions, and equivalence orbits must be tested independently of the implementation. |
| 16 | One explicit Wolfram codec is an architectural boundary. Reversing a stencil only for ECA or using a fallback callback is a shim. |

No Foundation stage is reopened because it committed no type algebra. Its hypotheses of dense finite support and finite selector-produced active sets are now qualified in the global ledger.

## Historical Detailed Implementation Plan (Superseded only on executor classification)

1. Represent fixed regular support independently from finite execution and trace shape. For `Z` observations, compute the exact radius-times-horizon causal halo and crop; alternatively execute an explicitly finite cycle/segment.
2. Make ordered exhaustive patterns validate `arity` with alphabet cardinality. For binary arity three, derive exactly 8 neighborhood states and 256 tables.
3. Implement a single inspectable Wolfram table codec with `index=4l+2c+r`; do not change the ECA stencil to compensate for the current reversed codec.
4. Make rule results typed same-site assignments and commit them through explicit parallel update using one old snapshot.
5. Route T01 through the generic shared transition protocol. Keep `elementary(rule_number)` as a strict preset that returns that ordinary specification.
6. Preserve current general selectors, stencils, seeds, boundary gathering, raw results, batching, and visualization only where their semantics already match.
7. Add independent exhaustive and trajectory oracles before migrating any current family. Later type stages decide which current family behavior can enter the same executor.

## Historical Goal 2 Implementation Stage (Superseded by Corrected Handoff)

### G2-T01 — Generic fixed-lattice synchronous assignment and Elementary conformance

**Objective:** execute T01 as a declarative preset of one generic fixed-lattice assignment protocol with exact Wolfram numbering and explicit finite realization. Never add `if rule.family == "elementary"`.

**Dependencies:** the synthesis-equivalent forms of (a) fixed regular 1D support plus symbolic `AllSites`, (b) typed same-site `Assign`, (c) explicit `ParallelUpdate`, (d) ordered exhaustive lookup with validated arity/cardinality, and (e) exact observation-window/halo lowering. Names remain provisional; these semantics are fixed by T01 evidence.

**Concrete files and changes:**

- `src/ca/rules.py`: give exhaustive channels explicit/read-validated arity; derive `state_count=|A|^arity`; encode ordered digits most-significant-first so `[left,self,right] -> 4l+2c+r`; derive `R=256`; validate `0..255`; store the table as data.
- `src/ca/rollout.py` or the synthesis-chosen executor module: execute generic `lookup -> Assign -> ParallelUpdate` from one current snapshot for scalar and batch use. No T01 or family-name switch.
- `src/ca/specs.py` and the synthesis-chosen preset index: add alphabet, semantic support, result/update, and realization metadata. `elementary(n)` returns an ordinary shared spec with Boolean alphabet, fixed 1D support, `AllSites`, pinned offsets `[-1,0,+1]`, one arity-three exhaustive table, and parallel assignment. Seed remains an episode argument.
- `src/ca/loci.py` or a new synthesis-selected support/lowering module: distinguish integer-line topology, finite cycle/segment, observation window, causal halo, crop, and trace coordinates. Record realization/boundary metadata.
- Reuse `neighborhoods.metric_radius`, `alphabets.boolean`, `seeds.point`, boundary gathers, `RawEpisode`/`RawBatch`, and visualization boundaries. Export the preset from `src/ca/__init__.py` only after it resolves to generic semantics.
- Add `tests/test_t01_elementary.py` plus focused generic rule/update/lowering tests.

**Migration/removal:**

- Replace the current low-significance-first exhaustive codec; do not reverse ECA selectors as a compatibility shim.
- Generic lookup must no longer be rejected by family dispatch. Do not add an interim `lookup`/`elementary` branch that duplicates the protocol.
- Do not delete current named-family behavior until its own completed type stages provide honest state/result/update migrations. Final Goal 2 synthesis removes the dispatch liability dependency-wise.

**Canonical tests:**

1. For every `n in range(256)` and all eight `(l,c,r)`, assert `output == (n >> (4*l+2*c+r)) & 1`; assert exactly 256 valid IDs and reject `-1`/`256`.
2. Assert rule 30 from a centered one yields the exact book rows at `BOOK:11128-11130`. With a width-13 zero-background causal halo, the mandatory longer asymmetric fixture is `0000001000000`, `0000011100000`, `0000110010000`, `0001101111000`, `0011001000100`, `0110111101110`, `1100100001001`; this independently decoded oracle cannot pass if rule 30 is reflected to rule 86.
3. Assert rule 90 equals `l XOR r`; rule 250 equals `l OR r`; rule 254 equals `l OR c OR r`; and rule 110 matches its eight cases/formula.
4. Prove old-snapshot semantics with a case that differs under left-to-right in-place mutation. Check rules 51/170/204/240 as complement/shift/identity oracles.
5. Run the same elementary spec with a centered point and a distinct explicit/random initial field. No seed may be embedded in the preset.
6. Check an exact observation crop against a larger causal-halo oracle for an asymmetric rule and a non-blank-preserving rule such as rule 1. Fixed zero at the displayed edge is not a valid oracle for all 256 rules.
7. Mechanically generate reflection/conjugation orbits and assert 88; keep all 256 executable IDs.
8. Assert the strict additive eight, totalistic/symmetric/blank-preserving predicates, generalized rule-250 property, and the explicit rule-105 terminology distinction lower to ordinary tables.
9. Inspect the preset: ordinary generic spec, Boolean alphabet, arity three, all-site synchronous assignment, no callable, hidden state, or family executor. Scalar/batch parity is regression evidence, not the only oracle.
10. Preserve the existing suite and `[t,x,0,0]` trace round-trip for finite results.

**Completion evidence:** tests above pass; static inspection finds no ECA/lookup family branch or callable rule bypass; all 256 tables round-trip; rule 30 is not mirrored; semantic support and finite realization are separately inspectable; existing tests pass without weakening.

## No-Cheating Checks

- No `eca`/`elementary` family branch in rollout or rule application.
- No relabeling Dyadlags or Dyadrads as ECA; their time/radius/gating semantics differ.
- No ECA-only stencil reversal to compensate for a globally wrong digit codec.
- No 256 hard-coded functions, formula callbacks, predicate escape hatch, or table hidden in metadata.
- No proof using only rule 0/255, symmetric rule 90, images, or batch-versus-same-code parity.
- No finite periodic/fixed-zero tensor presented as the native integer line; no fixed-zero edge oracle for every rule.
- No centered-one seed baked into program identity.
- No quotient from 256 executable tables to 88 representatives.
- No palette-only treatment of black/white conjugation.
- No bit packing as semantic state and no restriction to blank-preserving rules to make support appear finite.
- No weakening current tests or retaining two execution paths.

## Completion Requirements

- [x] All aliases, examples, captions, Notes, Index entries, cross-references, duplicates, and false positives are resolved.
- [x] All unique construction-relevant excerpts have exact canonical provenance.
- [x] Construction and variants are reconstructed before API/runtime comparison.
- [x] Wolfram case order and all 256 rule IDs have an explicit conformance oracle.
- [x] Current ECA geometry, lookup cardinality, bit order, rollout, seeds, boundaries, and tests are mapped exactly.
- [x] Goal 2 handoff has dependencies, files, migrations, canonical examples, tests, completion evidence, and no-cheating checks.
- [x] `0-plan.md`, `evidence-index.md`, and `design-ledger.md` are re-integrated and verified.

## Architecture-Reclosed Stage Result

**COMPLETE.** T01 is the fixed-lattice/all-sites/local-stencil/same-site-write/snapshot-parallel CA preset of the common branch-free SimpleProgram runner. Its evidence, codecs, trajectories, and runtime defects remain closed; the corrected architecture and Goal 2 handoff above supersede any earlier claim that this preset bounds the library abstraction.

## Historical Stage Results (Evidence Retained; Architecture Superseded)

T01 is complete with zero unresolved evidence candidates. It validates the first substantive shared transition algebra: fixed regular support, all-site ordered current-snapshot reads, an explicit finite table, typed same-site assignment, and atomic parallel update. It also disproves three current-runtime assumptions: finite `shape` cannot simultaneously mean native support, computation extent, and trace extent; ordered selector values cannot silently define rule-number digit significance; and a family-dispatched spatial lookup is not a generic executor. The implementation handoff uses a strict preset over shared semantics, exact causal-window lowering, and asymmetric independent oracles. No earlier type stage was reopened. Next in adversarial execution order: T09 Mobile Automata.
