# 34-T22-MOORE-CA

Status: **IN PROGRESS — SOURCE, ASSET, AND SEMANTIC EVIDENCE CLOSED; ARCHITECTURE INTEGRATION AND HOSTILE REVIEW OPEN**

## Current Facts

- T22 is CSV line 23, `Moore-Neighborhood Cellular Automata`. The taxonomy is search vocabulary; the Book, source-bound assets, and independently checked semantics remain authoritative.
- Chapter 5 explicitly changes T21's four surrounding cardinal cells to eight surrounding cells “including diagonals” (`BOOK:2212`). The center is retained separately by the rule. This is initial evidence for a NEIGHBORHOOD/RULE parameterization, not another executor.
- The direct examples use center-conditioned black-neighbor counts and codes `175850`, `746`, and `174826` (`BOOK:2226-2234`). Seeds, horizons, shapes, and stopped growth are run data/observers until exact evidence says otherwise.
- The Notes call this the `9-neighbor` profile because the eight surrounding cells plus self participate in the read. Their convolution assigns neighbor weight `2` and self weight `1`, yielding an 18-case `SelfValue x MooreCount` table (`BOOK:13475-13481`).
- The same Notes definition generalizes to alphabet size `k` and spatial dimension `d` as `self + k*FullTotal`, with `3^d-1` surrounding values, table length `k*((3^d-1)*(k-1)+1)`, and therefore `k^(k*((3^d-1)*(k-1)+1))` tables. Strict T22 is the `d=2,k=2` profile; this generalization is a typed valuation/access parameterization and a T23 control, not a new executor.
- The Notes distinguish `2^512` general positional rules, `2^18` outer-totalistic rules, `2^10` equal-sum totalistic rules, and `2^9` growth-totalistic rules for the nine-position square (`BOOK:13542-13549`). Those are distinct schema-tagged RULE representations/restrictions, not family modes.
- T21/D127 already proves the branch-free fixed-lattice runner, explicit Self access, square-grid support/realization separation, Book-frame ordering, and basis/table permutation. Its semantic oracle includes a same-runner T22 control, but T22 still requires its own exhaustive source/assets/rule fixtures and architecture closure.
- The current `dyadaxes_2d` access includes self, four cardinal, and four diagonal cells, so its geometry is a candidate realization. Its majority-gated cardinal/diagonal RULE is not automatically the Book's count table or a canonical T22 preset.
- The governing event remains:

  ```text
  active = FRONTIER.select(configuration)
  reads  = NEIGHBORHOOD.read(configuration, active)
  writes = RULE(active, reads)
  next   = UPDATE.apply(configuration, active, writes)
  ```

## Updated Assumptions

- DOMAIN remains discrete `t+2D`. Square `Z^2` support/topology belongs to CONFIGURATION. A finite array, periodic quotient, fixed exterior, sparse background representation, crop, and raster remain explicit realizations/views.
- Strict Moore access is a declared composition containing exactly one `SelfAt` and the eight unique offsets in `{-1,0,1}^2 \ {(0,0)}`. No center read is implicit, and equal resolved cells on a small torus remain distinct read occurrences.
- Raw Book row/column tuples plus their coordinate-frame tag are authoritative. Mapping to ENU must preserve order or permute every positional table; symmetric count rules cannot validate orientation.
- The 18-case center-conditioned count table is not the same schema as the ten-case equal sum of all nine values, and neither is the arbitrary 512-context positional table.
- Game of Life is source-confirmed as the ordinary `B3/S23` nine-neighbor outer-totalistic code-`224` preset over T22's same construction (`BOOK:14239-14249`). Its structures, sparse algorithm, history, behavior class, and universality claims remain relations/implementations/observers. Other weighted/partitioned diagonal rules, block rules, stochastic rules, properties, growth shapes, and biological analogies remain separately typed at their evidence-backed boundaries.
- A pattern that stops growing may still update to an unchanged successor. No fixed point or bounded picture silently becomes native halt.

## Big Picture Objective

Reconstruct Moore-neighborhood cellular automata from primary evidence and prove whether T22 is exactly the T21/T01 fixed-lattice CA preset with eight surrounding offsets and source-pinned RULE schemas. Produce an implementation-ready Goal 2 handoff without a Moore state class, executor, update law, hidden center, implicit boundary, or `dyadaxes_2d` semantic shortcut.

## Catalog Identity

- Stable ID: T22.
- Exact catalog name: Moore-Neighborhood Cellular Automata.
- CSV line: 23.
- Taxonomy section: 22.
- Entry kind: fixed-support synchronous local transition construction; expected neighborhood/RULE parameterization pending evidence closure.
- Initial vocabulary: Moore neighborhood, nine-neighbor/9-neighbor square, eight neighbors, diagonals, immediate and diagonal neighbors, outer totalistic, totalistic, growth totalistic, code 175850, code 746, code 174826, Game of Life, rough surface, circle, rows of black cells, periodic boundary, symmetry, Notes implementation, actual Index.

## Search Log

`34-T22-source-oracle.py` freezes 17 overlapping queries. Their union contains 164 lines: 117 pre-Index candidates and 47 actual-Index routes. All 117 construction candidates are dispositioned as 93 retained matches plus 24 explicit broad-query exclusions; no pre-Index or Index candidate remains unresolved.

The 93 retained matches plus 171 governed continuations produce 264 source lines with digest `e54447c5ecdd87f896d65e5f05bbcd809de6908a357f35762a44aedb194c39e6`. The exact semantic partition is `90 native / 102 relation / 72 control`. Native evidence includes the Chapter 5 named codes, the nine-position implementation/counts/codecs, parallel update/realization evidence, and Life code `224` mechanics as a named preset. Life structures/history/universality remain relations; T21/T23/T24 and nonstep constraints remain controls.

The 24 exclusions partition as `12 generic 1D code/update collisions / 7 physical-or-aggregation background collisions / 5 other constructions`. The 47 actual-Index lines route as `9 T22 geometry/code / 28 Life / 5 T23 / 2 T24 / 3 numeric false collisions`; the Index supplies navigation only.

All 17 split Markdown sources are hash-bound. The query reverse join closes 162 records as `151 exact + 11 mapped variants`. Retained evidence closes as `186 exact + 78 mapped variants`, with no monolith-only retained line. The stable asset interface exposes 68 governed source-image lines, digest `d596854fe15fafe293038296ec2e5872612edda3033c08d6d2d314134ac3dd43`.

## Source-Bound Asset Audit

`34-T22-asset-oracle.py` derives a radius-four source-neighborhood candidate closure of 95 physical plates. The source oracle entitles 68 governed assets; 27 additional nearby plates are separately ledgered as adjacency-only rather than silently imported. The governed partition is:

```text
strict 18-case rule/access plates       4
strict 512-context raster plates        0
strict code-174826 continuation views    8
deterministic relations/observers       17
Life B3/S23 preset/relations            19
stochastic eight-neighbor controls       5
T21 cardinal control                     1
T23 three-dimensional controls           9
T24 other-lattice controls                4
constraint/model-set control              1
```

The empty 512-context raster class is a positive finding: the source defines that schema textually but supplies no governed positional-rule plate. Count-symmetric images cannot prove positional order. Life is not put in a distinct family/control class; its 19 assets form a named-preset/relation subledger over the same T22 algebra. Stochastic aggregation is separately marked as canonical evolution whose RNG/distribution semantics belong to its owning stage, while the pure constraint plate is the actual nonstep control.

All 95 candidates have one monolith and one split reference, for 190 references and 95 distinct physical hashes. The governed ledger digest is `0e88ca4aa91ea5599f71dbee0347ac7ea8bfa16d865a9bb4a6ac34f5cb317c13`; the adjacency-only universe/ledger digests are `7b95fd5481303cc5ebcb3f5e942f8c10a160562ed83bff429fa0028dcc868602` and `55e369f47d4108febd80b8e6b09f2ab5a7b50ff09bb5da8644a63909c079191d`.

A 28-record transcription ledger binds every declared code, seed, displayed checkpoint, continuation label, shape observation, and relation tuple to both the physical asset hash and governing source-line hash. Its digest is `981e0e0391310b9f3b86cd0f8863589bbf7423ddd1da87525da10d2ae704c4e3`. It is explicitly `HASH_BOUND_NOT_PIXEL_REPLAYED`. The code predicates independently reconstruct `175850`, `746`, `174826`, and Life `224` across all 18 cases, but no raster is claimed as decoded execution evidence.

The audit also freezes the fifteen-page physical-file offset for printed pages 177–181 and the unusual Notes/split-Index reverse join. Random and stochastic plates remain unreplayable because the Book does not serialize a complete initial configuration or RNG/distribution/seed; no crop, boundary, palette, or renderer is invented.

## Initial Book Excerpts

### Excerpt 1 — eight surrounding neighbors including diagonals

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:2212-2218`
- Establishes: strict T22 changes the surrounding access set to eight cells and keeps the old center as a separate rule input.

> exactly three of its eight neighbors—including diagonals—are black, and otherwise it should stay the same color as it was before

### Excerpt 2 — named codes and independent seeds/horizons

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:2226-2234`
- Establishes: codes `175850`, `746`, and `174826` use the eight-neighbor center-conditioned convention; row lengths and step counts are run data; roughness, circularity, growth, and stopping are observations.

### Excerpt 3 — direct 18-case implementation

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:13475-13481`
- Establishes: neighbor weight `2`, self weight `1`, and an 18-digit binary table implement the direct nine-position profile.

```text
ListConvolve[{{2,2,2},{2,1,2},{2,2,2}}, a, 2]
IntegerDigits[code, 2, 18]
```

### Excerpt 4 — the 512/18/10 schema split

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:13534-13549`
- Establishes: general positional, outer-totalistic, equal-sum totalistic, symmetry-reduced, and growth rules are distinct restrictions/representations over the same nine declared positions.

### Excerpt 5 — dimension/alphabet generalization

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:13475-13503`
- Establishes: `FullTotal` reads every surrounding position in the `3^d` cube, while self remains a separate radix-`k` factor. The rule table has `k*((3^d-1)*(k-1)+1)` cases. This is direct evidence that dimension, alphabet valuation, access, and compact RULE data are parameters of the same runner.

### Excerpt 6 — growth restriction

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:13542-13563`
- Establishes: growth-totalistic rules keep every black cell black, leaving nine birth-count choices for an eight-neighbor binary shell and therefore `2^9` rules. Code `174826` is the exactly-three-birth member, not another update law.

### Excerpt 7 — Game of Life is an ordinary T22 preset

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:14239-14249`
- Establishes: the Book explicitly lists Life as 9-neighbor outer-totalistic code `224` and implements each event from the old center plus the sum over the full `3x3` square. `#2==3` births a white center with three neighbors and preserves a black center with two; `#1==1 && #2==4` preserves a black center with three. This is `B3/S23` over the same 18 cases.

### Excerpt 8 — sparse Life is a realization, not different semantics

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:14243-14261`
- Establishes: the complete-array Life step and the more efficient list-of-black-positions step are alternate implementations of the same event. Sparse execution is admissible only with a proved commuting relation and compatible background; it does not replace the complete configuration or create a Life executor.

## Construction Model

- DOMAIN: expected discrete `t+2D` reuse.
- Configuration/support: expected total finite-alphabet field on fixed square-grid `Z^2`; finite realizations explicit.
- ALPHABET: expected binary strict profiles over the reusable finite alphabet axis.
- FRONTIER: expected `AllSites` direct reuse.
- NEIGHBORHOOD: expected explicit composition of one Self plus eight ordered Moore offsets.
- RULE: expected distinct complete 512-context positional, 18-case `SelfValue x MooreCount`, and ten-case self-plus-eight sum schemas; exact source code order must be frozen.
- UPDATE: expected one same-site assignment per source under old-snapshot parallel commit.
- Successor: expected one deterministic configuration; fixed points do not imply halt.
- Seed/realization: exact configurations, constructors/laws, boundary/work/horizon/viewport remain separate.
- Observers/relations: shapes, outlines, radius fits, growth stops, classes, Life structures, applications, histories, and renderings do not feed execution.

## First-Principles Fit Standard

The `src/ca` namespace and its Phase 1 fixed-lattice implementation do not define the library's semantic boundary. The intended library is the common SimpleProgram algebra reconstructed from the Book. Catalog names identify evidence obligations and presets; they never select runtime families.

T22 therefore passes by **native axis instantiation**, not merely because a Moore rule can be encoded in some cellular automaton. The required proof is that its complete configuration and one native event are already expressed by the shared axes:

```text
AllSites.select(X)
    -> (SelfAt + eight declared offsets).read(X, active)
    -> closed table writes one complete label per active site
    -> SnapshotParallelSameSite.apply(X, active, writes)
```

No hidden interpreter, microstep simulation, family test, alternate trace clock, or opaque whole-program packing occurs. A new closed implementation of an existing axis can be justified by evidence, but it remains an axis implementation. A new top-level semantic class or runner requires a concrete counterexample showing that the common protocol cannot retain T22's complete state and one-step semantics. No such counterexample is presently visible.

## Direct Named-Code Reconstruction

For binary outer-totalistic T22 rules, let `s in {0,1}` be the old center and `n in {0,...,8}` the number of black surrounding cells. The Notes convolution assigns self weight `1` and every surrounding cell weight `2`, so the table address is

```text
j = 2*n + s
output = bit_j(code)
```

This makes the prose/code relation inspectable rather than a family convention:

- The rule “stay unchanged except become black at neighbor counts 3 or 5” sets every odd bit `j=2*n+1` and also bits `6` and `10`: `174762 + 64 + 1024 = 175850`.
- The rule “stay unchanged except become black at count 3” sets every odd bit and bit `6`: `174762 + 64 = 174826`.
- Code `746` sets both count-3 bits `6,7` and the old-black bits for counts `0,1,2,4`, namely `1,3,5,9`: `64+128+2+8+32+512 = 746`. Thus count 3 becomes black, counts 0/1/2/4 retain self, and counts 5 through 8 become white.
- Life `B3/S23` sets the white-center birth bit `6` and the black-center survival bits `5,7`: `64+32+128 = 224`. The named Life program is therefore an ordinary value in the same 18-case schema.

The semantic oracle must derive these values independently and reject swapped center/count significance, digit reversal, a hidden-center convention, and accidental agreement on symmetric fixtures.

## Current Runtime/API Fit Audit

- `src/ca/neighborhoods.py:572-593` already constructs the radius-one `L_infinity` shell as the eight-cell Moore access. `compose((self_at(), moore()))` therefore preserves the exact two semantic input roles needed by the 18-case table without a T22 neighborhood class.
- `src/ca/neighborhoods.py:717-741` exposes the same nine raw positions as explicit self, four cardinals, and four diagonals. This is a lossless regrouping of geometry, but `src/ca/rules.py:472-493` majority-gates the two four-cell groups before lookup. That `dyadaxes_2d` RULE discards exact counts and positional information, so it is not a canonical T22 rule preset.
- The current rule-channel machinery can describe an exhaustive self channel plus an eight-cell count channel, and its mixed address `self + 2*count` matches the Notes. The current rollout nevertheless accepts spatial execution only for three named Dyadrads/Dyadaxes families (`src/ca/rollout.py:166-174,201-213`). Goal 2 must execute the closed channel/table specification generically; adding a `moore` family branch would preserve the defect.
- The Book's arbitrary positional rule orders its nine offsets lexicographically and treats the first position as the most-significant context digit (`BOOK:13491-13531`). The current exhaustive channel assigns its first gathered value the least-significant weight (`src/ca/rollout.py:750-759`). Goal 2 needs one explicit order/codec correction or table permutation, shared with T01/T21, not a T22 reversal shim.
- Scalar Python integers can hold a 512-bit general-rule code, but the batch path normalizes rule IDs to `numpy.int64` (`src/ca/rollout.py:264-274`). Complete typed tables or arbitrary-precision tagged codecs are the semantic representation; machine-width batch IDs are a realization limit, not a reason to shrink the rule family.
- Current fixed `shape`, boundary, dense arrays, canonical coordinates, and rasters are finite computation/trace realizations. They do not replace native square-grid support, the chosen exterior/background law, or the complete mathematical configuration.

| Current area | Audited fit | Goal 2 disposition |
|---|---|---|
| `simple_programs.md` | DIRECT/PARAMETERIZATION for its documented fixed dense scope: it already describes `t+2D`, old boundary-extended snapshots, ordered local offsets, exhaustive/aggregate rules, and synchronous assignments. Its hard-coded writable next slice and scalar same-site result are one preset, not the SimpleProgram boundary. | Retain the evidenced fixed-lattice preset while moving support/topology, realization/boundary, RULE-result schema, and UPDATE into their owning broad axes. |
| `loci.py` | DIRECT finite-realization mechanics: coordinate spaces and `gather` handle rank-two centered coordinates and fixed/periodic/reflective reads. | Reuse as a lowering. Do not identify array coordinates/order or finite shape with native square `Z^2` semantics. |
| `frontiers.py` | DIRECT for a finite all-sites realization: `time_slice(shape)` enumerates the full old spatial slice. | Expose semantic `AllSites`; do not create `MooreFrontier` or retain writable-target terminology as the abstraction. |
| `neighborhoods.py` | DIRECT/PARAMETERIZATION: `moore()` is the exact eight-cell `L_infinity` shell; `self_at()` and `compose()` preserve the center role. `dyadaxes_2d()` exposes the same raw nine positions under a different grouping. | Reuse ordinary selectors/components. A named Moore preset may return structural data only. |
| `rules.py` | PARTIAL: finite channels, totalistic aggregation, and lookup metadata exist. Dyadaxes majority gates are lossy for T22, and current metadata does not establish the three complete T22 case schemas or arbitrary-precision identities. | Add closed complete tables, factor descriptors, schema-tagged codecs, and strict validators; no rule-family executor. |
| `rollout.py` | MECHANICAL reuse behind an architectural mismatch: spatial gathering and fresh-array assignment already operate rank-generically from one snapshot, but family strings choose entry, only `time_slice` is admitted, general positional significance is reversed, and batch codes are `int64`. | Lower the branch-free typed runner through the vectorized kernel after fixing the shared codec and validation. No `moore`/Life branch. |
| `specs.py` | PARTIAL: `Dynamics` carries dimension, finite shape, rule, neighborhoods, frontier, and boundary, but JSON resolution accepts only named Phase 1 families. | Decode structural typed axes/presets and stable program identity rather than catalog/family strings. |
| `seeds.py` | DIRECT finite constructors/realizations, governed by D121. | Keep seeds, laws, horizons, crops, and backgrounds independent from the T22 program. |
| `datasets.py` | CONTROL only: `2d-dyadaxes` fixes an `11x11` tensor, majority-gated rule, selected seeds, and fixed-zero boundary. | Preserve its experiment identity; do not rename it T22 or use it as conformance evidence. |
| Current tests | PARTIAL: neighborhood tests pin the eight lexicographic offsets, while rollout tests exercise only Dyadaxes rule `0` and batch parity with rule `91`. | Add source predicates/codes/traces, general orientation, factor rejection, alias multiplicity, snapshot, boundary/support, arbitrary-precision, Life, and T21/T23 same-runner conformance. |

## Provisional Axis Classification

| Concern | Fit | Smallest reusable base | T22-specific obligation |
|---|---|---|---|
| DOMAIN | DIRECT | D127 discrete `t+2D` | none; Moore is not another dimensional space |
| CONFIGURATION/support | DIRECT / PARAMETERIZATION | fixed square `Z^2` lattice plus explicit realization relation | preserve square topology, total support/background, and any finite quotient/exterior separately |
| ALPHABET | DIRECT | T02 finite typed alphabet; strict profile is `Bit` | retain label rank, numeric valuation, and palette as different roles |
| FRONTIER | DIRECT | `AllSites` | one firing occurrence per semantic site; finite enumeration is only a realization |
| NEIGHBORHOOD | PARAMETERIZATION | D127 explicit composed local access | exactly one declared Self and eight unique Moore offsets in source order |
| RULE input/representation | PARAMETERIZATION / LOSSLESS REPRESENTATION | T02 complete ordered table plus D115-D118 factor maps | keep 512-context, 18-case outer-totalistic, ten-case totalistic, and nine-free-bit growth restrictions schema-tagged |
| RULE result | DIRECT | one complete same-site label assignment | no raster, shape, or behavior result |
| UPDATE | DIRECT | D004/D117/D127 old-snapshot parallel same-site commit | preserve complete source coverage and fixed topology; no T22 update law |
| seed/run/observers | DIRECT / PARAMETERIZATION | D121 configurations, constructors, laws, realizations, traces, and observers | keep row/point/random seeds, horizon, boundary, growth stop, outlines, and slices outside program identity |
| outcome | DIRECT | deterministic `StepResult[Configuration]` | an unchanged successor remains an event result, not an inferred halt |

The expected final classification is class 3 only because ordered-coordinate and compact-table representations require explicit isomorphisms. Execution itself is direct reuse. This remains provisional until the three evidence oracles and hostile review close.

## Ordered-Position and Basis Obligations

The Book's raw array-frame order for the complete radius-one square is

```text
BookNine =
  ((-1,-1), (-1,0), (-1,1),
   ( 0,-1), ( 0,0), ( 0,1),
   ( 1,-1), ( 1,0), ( 1,1))
```

Under the declared basis map `(row,column) -> (x=column,y=-row)`, preserving that sequence and sorting the resulting ENU offsets are different operations. A direct derivation gives the candidate permutations

```text
runtime_to_book = (6,3,0,7,4,1,8,5,2)
book_to_runtime = (2,5,8,1,4,7,0,3,6)
```

The semantic oracle must derive rather than assume them, prove that they are inverses, permute all 512 positional rows, and exhibit an asymmetric counterexample where re-sorting offsets while retaining the Book table changes the program. Count and sum tables are invariant under these position permutations and therefore cannot establish orientation.

The complete positional address uses the first `BookNine` value as the most-significant binary digit and the last as the least-significant digit. Small periodic quotients may resolve several offsets to the same physical cell; those remain distinct access occurrences and retain their multiplicity. Deduplicating resolved coordinates would change the nine-input program and its count semantics.

## Candidate Strict RULE Schemas

```text
GeneralNineRule:
    cases = Bit^9 in BookNine order
    table = CompleteMap(cases, Bit)
    rule_count = 2^512

OuterMooreRule:
    cases = SelfValue x MooreCount[0..8]
    table = CompleteMap(cases, Bit)
    index = 2*MooreCount + SelfValue
    rule_count = 2^18

ValuedOuterMooreRule[k]:
    valuation = Alphabet <-> {0,...,k-1}
    cases = SelfValue x NeighborValueSum[0..8*(k-1)]
    index = SelfValue + k*NeighborValueSum
    case_count = k*(8*(k-1)+1)
    rule_count = k^(k*(8*(k-1)+1))

TotalisticNineRule:
    cases = SelfPlusMooreSum[0..9]
    table = CompleteMap(cases, Bit)
    index = SelfPlusMooreSum
    rule_count = 2^10

GrowthMooreRule:
    base = OuterMooreRule
    invariant = table(SelfValue=1, count) == 1 for every count
    free cases = table(SelfValue=0, count), count in 0..8
    rule_count = 2^9
```

An outer-totalistic table expands to a general table only when every positional context with equal `(self,neighbor_count)` has the same result. A totalistic table requires the stronger equal-total-sum fiber condition. Factoring must reject a single disagreeing row, retain the source schema and code identity, and round-trip exactly on its qualifying image.

## Independent Semantic Oracle

`34-T22-semantic-oracle.py` implements two separate paths. The literal native reference reads Book row/column positions and evaluates general, outer-totalistic, equal-sum, and generalized finite-`k` formulas directly. The generic path constructs opaque snapshot-scoped source handles, explicit Self-plus-offset access, typed closed rules, one same-site write per source, and atomic old-snapshot parallel commit. Neither path calls the other evaluator.

The closed oracle reports 1,417 native/generic commutations:

```text
outer compact bases          320
equal-sum compact bases      192
general positional bases     514
nonaliasing directional      225
named codes                    4
ternary positional projection 81
ternary FullTotal             81
```

Its representation proof covers all 262,144 18-bit outer signatures and independently proves the complete 512-context fiber map plus its 20 affine bit bases. It expands and factors all 1,024 equal-sum tables. The arbitrary 512-row schema is covered by zero, one, and all 512 unit table bases for 514 exact code round trips. This factorization avoids claiming a wasteful `2^18 * 512` Cartesian run while proving every independent table bit and every context fiber.

The coordinate proof covers all `9 * 512 = 4,608` projection/context cases and all 512 table unit bases. It derives `runtime_to_book=(6,3,0,7,4,1,8,5,2)` and its inverse, then demonstrates that naive ENU re-sorting moves the projected source in a complete asymmetric step while certified table permutation commutes.

The generalized Notes profile is checked for seven `(dimension,k)` pairs. For `d=2,k=3`, all `3^9 = 19,683` positional contexts hit exactly 51 `SelfValue x NeighborValueSum` cases with independently counted fibers, and 81 ternary native/generic steps commute. Binary overlap with the strict 18-case function is denotationally exact while the two schema types remain distinct. The named-rule partition reconstructs `175850`, `746`, `174826`, and Life `224`; the latter also reproduces a horizontal-three to vertical-three blinker through both native and generic routes.

Further adversaries preserve access-slot multiplicity on small periodic tori, separate fixed from periodic boundaries and native `Z^2` from finite realization, reject fixed-background sparse lowering without a quiescence proof, distinguish snapshot-parallel from in-place traversal, require exactly one explicit Self and eight unique offsets, reject malformed/stale/foreign source data and writes before commit, and execute T21/T22/T23 through one generic step function.

Root and relocated `/tmp` execution produce identical evidence; silent import, byte compilation, exact-type checks, and fail-closed optimized mode pass. The semantic decision matrix proposes D128 as access/RULE parameterization and lossless representation only.

## Audit Questions

1. Does any T22 evidence alter CONFIGURATION, FRONTIER, RULE result, UPDATE, successor cardinality, or outcome semantics rather than only access/RULE data?
2. What is the exact Book order of the nine raw positions, and how must it permute under the Book-row/column-to-ENU basis map?
3. Do named codes reconstruct exactly from their prose predicates under index `2 * MooreCount + SelfValue`?
4. Which rasters are strict fixtures, observers, T21/T23/T24 controls, Life relations, or mere adjacency candidates?
5. Does the current Dyadaxes access preserve all nine raw values, and where does its majority-gated RULE lose the Moore count or positional context?
6. Are finite periodic/fixed realizations and evolving backgrounds represented losslessly without becoming native support semantics?
7. Can every qualifying compact table expand/factor through the same `ClosedLocalMap`, with adversaries rejecting invalid quotients?
8. Is T23's 3D access a dimensional parameterization boundary and not a reason for another runner?

## Detailed Implementation Plan

1. Freeze direct/alias/mechanics/Notes/actual-Index/split source closure with explicit T21/T23/T24/Life controls and zero unresolved candidates.
2. Derive the complete source-bound asset candidate set, classify every governed/adjacent plate, bind metadata, and replay only source-determined fixtures.
3. Build an independent semantic oracle for direct 18-case codes, ten-case sums, positional order/basis permutation, and the generic Self-plus-eight access.
4. Audit current documents/modules/tests and D004-D008, D111-D121, and D127 from first principles.
5. Add D128 only if evidence warrants a T22 boundary; specify the smallest Goal 2 composition and conformance matrix.
6. Obtain final hostile review and run root/`/tmp`/optimized/import/compile/Markdown/diff/scope/status/test gates.

## Candidate Goal 2 Composition

```text
Domain        = DiscreteSpace(dimension=2)
Configuration = FixedLattice(SquareGrid(Z^2), Alphabet)
Frontier      = AllSites
Neighborhood  = Compose(
                    Offset(-1,-1), Offset(-1,0), Offset(-1,1),
                    Offset(0,-1), SelfAt, Offset(0,1),
                    Offset(1,-1), Offset(1,0), Offset(1,1))
Rule          = OrderedContextTable
              | ProductCaseTable(SelfValue, MooreCount)
              | SumCaseTable(SelfPlusMooreNeighbors)
Update        = SnapshotParallelSameSite
Seed          = IndependentValidatedConfiguration
```

This composition is a hypothesis to test, not a family API mandate. Public spelling remains a synthesis choice.

### Candidate Goal 2 implementation delta

1. Reuse the synthesis-selected T21 fixed square-lattice configuration, `AllSites`, complete old-snapshot reads, same-site label assignment, snapshot-parallel UPDATE, deterministic `StepResult`, support/realization separation, and coordinate-frame adapter unchanged.
2. Express the Moore shell through ordinary explicit offsets or the existing `L_infinity` radius constructor. If a named preset is exposed, it must return that structural access specification and may not select execution.
3. Reuse the complete ordered-context table for the nine-position general rule. Add only source-pinned case descriptors for `(SelfValue,NeighborValueSum)`, all-nine value sum, and the monotone-black growth restriction. Their expansion/factorization maps operate on closed table data.
4. Make table schema part of program/code identity. A bare integer such as `224`, `746`, or `174826` is insufficient without alphabet, access order/frame, case schema, digit convention, and table length.
5. Retain arbitrary-precision rule serialization and complete typed tables. Vectorized finite realizations may choose a different table storage, but `numpy.int64` cannot define the program range.
6. Keep Life, HighLife, named class-4 codes, code-746 circle/roughness observations, and code-174826 growth structures as presets or analyzers at the exact evidence-backed boundary. None changes the runner.
7. Permit sparse live-cell execution only as a separately proved lowering for a compatible background rule. The native configuration remains complete, and the sparse algorithm must commute with one native event.
8. Reuse T08 seed/configuration records for single cells, finite rows/blocks, random fields, and periodic realizations. Do not put the displayed seed, horizon, crop, or boundary into the Moore program preset.

### Required conformance areas

1. Reconstruct codes `175850`, `746`, and `174826` from their prose predicates and the exact `2*n+s` convention; if source closure admits Life, also reconstruct code `224` from `B3/S23`.
2. Compare a literal native evaluator with the generic SimpleProgram path on complete source-bound traces and on exhaustive local contexts.
3. Prove all compact table/code round trips at their natural finite cardinalities, and prove the address/fiber maps independently where enumerating every table-context Cartesian pair would add no coverage.
4. Reject compact factorization after changing one positional row inside an otherwise equal fiber; reject schema/code interchange even when two serialized integers happen to match.
5. Prove the full Book-array-to-ENU access and 512-row table permutation using asymmetric projections and an explicit naive-re-sort failure.
6. Test every one of the nine positional projections on a nonaliasing grid, including the declared center. Symmetric count rules cannot substitute for these cases.
7. Test `1x1`, `1x2`, `2x1`, and `2x2` periodic realizations so coincident resolved cells retain separate offset occurrences and count multiplicity.
8. Distinguish old-snapshot parallel commit from in-place scan order with a rule/seed that produces different successors.
9. Separate native `Z^2`, finite causal work with exterior values, and periodic quotients; validate any sparse background lowering against the complete field.
10. Validate the generalized `d,k` formula and a nonbinary valuation case, plus T21 cardinal and T23 three-dimensional same-runner controls.
11. Reject missing/duplicate offsets, implicit or duplicate Self, wrong arity/order/dimension, incomplete tables, out-of-alphabet values, stale reads, wrong targets, duplicate source coverage, and invalid realization mappings before commit.
12. Demonstrate that `dyadaxes_2d` has the same raw geometry but not the same RULE denotation by giving two neighborhoods with equal majority-gate outputs and different Moore counts/required results.

## No-Cheating Checks

- No `moore`, `nine_neighbor`, Life, or T22 rollout branch or executor.
- No hidden center read, flattened memory-order codec, or diagonal deduplication.
- No untagged interchange of 512-context, 18-case, and ten-case rule numbers.
- No symmetric/count-only fixture used as proof of positional orientation.
- No Dyadaxes majority gate substituted for an exact neighbor count or positional table.
- No finite tensor, periodic boundary, crop, palette, or raster presented as native `Z^2` semantics.
- No growth stop, circle fit, behavior class, Life structure, or application fed back into execution.

## Completion Requirements

- [ ] Exhaustive source/split/Notes/Index/alias audit closes with zero unresolved candidates.
- [ ] Source-bound asset fixed point closes without pixel or random-replay overclaims.
- [ ] Exact Moore access, three RULE schemas, named codes, and orientation mappings are proven.
- [ ] Smallest reusable base is classified without a family executor or duplicate UPDATE.
- [ ] Current API/runtime/principles audit and Goal 2 handoff are implementation-ready.
- [ ] Independent hostile review and all oracle/test/Markdown/diff/scope/coverage gates pass.
- [ ] `0-plan.md`, `evidence-index.md`, `design-ledger.md`, and `architecture-audit.md` agree.

## Stage Results

In progress.
