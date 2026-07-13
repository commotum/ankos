# 22-T03-TOTALISTIC-CA

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T03, CSV line 4, `Totalistic Cellular Automata`; taxonomy vocabulary is `ref/notes/CA-Types.md:68-99` and remains a search seed rather than book evidence.
- The strict transition at `BOOK:772-776` distinguishes unrestricted three-color tables from totalistic rules. It assigns the colors exact values `0,1,2`, makes the next value depend only on the average of left/self/right, and orders the seven output cases from sum `0` at the least-significant/rightmost base-3 digit through sum `6` at the most-significant/leftmost digit.
- The Notes give the direct generalization. For `k` colors and radius `r`, fixed arity is `q=2r+1`, reachable sums are `0..q(k-1)`, table length is `M=1+q(k-1)`, and the rule count is `R=k^M` (`BOOK:11897,11902-11916`). The structural output for sum `s` is digit `floor(n/k^s) mod k`; average `s/q` is an exact alternate label for the same case, not a floating computation.
- T01/T02 and D111-D114 already supply fixed ordered one-dimensional support, `AllSites`, old-snapshot reads, typed same-site assignment, atomic parallel commit, successor, seed, realization, trace/view separation, ordered alphabets, and arbitrary-precision integer serialization. T03 changes the rule's input quotient and program identity, not the executor or update law.
- `simple_programs.md:1964-2027` groups numeric sums, active counts, and color histograms under one broad `TOTALISTIC` label. That API responsibility is wider than source T03: equal-sum contexts such as `(0,2,0)` and `(1,0,1)` must merge even though their color histograms differ.
- The current runtime can sum an `int64` read vector, but `rules.totalistic` does not derive its case count, `_channel_state` ignores the declared `sum` versus `count` mode, generic `lookup` is not executable, spatial output remains binary right-shift/`&1`, and batch rule IDs are forced through `numpy.int64`. No current test executes a standalone three-color totalistic table or validates its codec.
- Controlled search, source-repair, and asset closure are concurrent evidence dependencies. The architecture below uses only the strict definition and intact Notes formulas; exact gallery initial conditions, raster settings, and any additional variant claims remain unresolved until their protected sections close.

## Updated Assumptions

- Treat source T03 as one closed equal-weight integer-sum aggregate followed by a complete finite sum-case table. “Permutation invariant” alone is insufficient: a color histogram, set, nonzero count, minimum, or arbitrary reducer preserves different information.
- Make a numeric color valuation `nu:A->{0,...,k-1}` explicit and program-defining. The v1 source profile uses the canonical contiguous valuation; symbolic relabeling is supported only through an explicit validated bijection, never host iteration order, alphabet rank by accident, or palette tone.
- Normalize execution to integer sum `s`. Average is the exact rational label `s/(2r+1)` and cannot introduce float division, rounding, tolerance, or a second case table.
- Keep the complete structural `(valuation,aggregate,table)` rule primary. A padded arbitrary-precision base-`k` integer is a lossless source codec/provenance value, not the only in-memory rule form or an execution register.
- Strict T03 and T04 pin `r=1`; direct Notes evidence supports the same aggregate-table construction for validated `r>=1`. T04 (`k=3`) and T05 (higher `k`) remain discoverable parameter presets unless their own evidence introduces different mechanics.
- Do not import the single-gray seed, white-background filter, symmetric appearance, palette, gallery horizon, behavior class, or emulation into program identity. In particular, a zero background is stable only when the sum-zero output is zero.
- T06 quiescence, T07 reflection symmetry, additive formulas/proofs, outer/semi-totalistic summaries, histograms, unequal weights, threshold rules, higher-dimensional stencils, and T44 continuous aggregation retain separate predicates, analyzers, relations, or construction ownership. Any broader reuse remains unresolved pending its own evidence.

## Big Picture Objective

Reconstruct totalistic cellular automata exhaustively from strict text, captions, Notes, actual Index, implementations, formulas, galleries, restrictions, applications, and cross-references; determine the exact aggregate/table/code semantics and the smallest honest reuse of T01/T02 without a `totalistic` rollout branch.

## Catalog Identity

- Stable ID: T03.
- Exact CSV name: `Totalistic Cellular Automata` at `ref/notes/CA-Types.csv:4`.
- Taxonomy: `ref/notes/CA-Types.md:68-99`; vocabulary seed only.
- Candidate entry kind: permutation-invariant local-rule construction/description over fixed-lattice synchronous assignment, subject to evidence audit.
- Initial vocabulary: totalistic/totalistic rule, sum, average, total/aggregate of neighboring colors, code, base-`k`, `3k-2`, `k^(1+(k-1)(2r+1))`, `2187`, `16`, `64`, `5^13`, three/five colors, range `r`, outer totalistic, weighted totalistic, symmetric, additive, quiescent, and named example codes `777`, `867`, `420`, `1599`, `1815`.

## Search Log

In progress. The controlled search must separately cover strict definition/captions, general count and implementation Notes, actual-Index routes, split duplicates, aliases (`sum`, `average`, `outer totalistic`, weighted forms), color/range variants, code examples, symmetry/background restrictions, applications/emulations, and all linked assets. Every candidate will receive a disjoint included/sibling/relation/false-positive disposition.

## Book Excerpts

In progress. No excerpt will be treated as canonical until its complete candidate family and source repairs are closed.

## Construction Model

### Native semantics

| Dimension | Reconstructed T03 semantics |
|---|---|
| State | `STATE = SUPPORT + VALUES`; no control, accumulator, code register, or history. Support is the same fixed ordered one-dimensional regular lattice as T01/T02, and values form a total field over a finite color alphabet `A`. |
| Alphabet/value assignment | `k=card(A)>=2`. A total bijection `nu:A->{0,...,k-1}` supplies arithmetic color values and is part of program identity; the canonical source alphabet is the integer range itself. Palette is representation. |
| Active loci | Every semantic site on every event. Finite cycle/segment/causal-window lowering retains the T01/T02 distinction between native support, realization, work extent, and observation crop. |
| Read | For radius `r>=1`, read the fixed old-snapshot neighborhood at offsets `-r,...,0,...,+r`, including self exactly once. Its arity/multiplicity `q=2r+1` is defining even though aggregate output is permutation invariant. Strict T03 has `r=1`. |
| Aggregate/cases | `s=sum_i nu(read_i)`. Every integer `s` in `0..q(k-1)` is reachable, giving exactly `M=1+q(k-1)` cases. The exact average label is `s/q`; it does not change case identity. |
| Rule | One immutable complete structural table `U:{0,...,M-1}->A`. Equal sums must select the same row regardless of order or histogram. No missing row, default, wildcard, callback, gate, modulus, threshold, or formula is implicit. |
| Result/update | One typed same-site `Assign(U(s))` per active site; T01's atomic parallel fixed-field commit applies all assignments from the same old field. T03 adds no update law. |
| Successor/halting | One deterministic successor for every valid field/table, including unchanged fields. There is no branch, rejection, randomness, intrinsic halt, fixed-point stop, or background stop; finite horizon and resource outcomes are external. |
| Seed/background/boundary | The initial total field and finite realization are independent run data. A single gray cell, random field, or uniform background does not identify the rule. A canonical zero background evolves whenever `U(0)!=nu^-1(0)`; T06 owns the stable-background restriction. |
| Observers/provenance | Spacetime/raster views, exact-average labels, palette, symmetry and additivity claims, behavior class, period/growth/death analysis, gallery filters, emulation, search work, and code display remain outside state and native events. |

### Sum-table and Wolfram code invariants

Let `q=2r+1`, `M=1+(k-1)q`, and let `U_s` be the output color for integer sum `s`.

```text
output(n,s) = nu^-1(floor(n/k^s) mod k)
code(U)     = sum_{s=0}^{M-1} nu(U_s) * k^s
```

- Valid codes are exactly `0..k^M-1`; the rule space has `R=k^M` members.
- Sum zero is the least-significant/rightmost displayed digit. A padded source display is ordered `U_(M-1),...,U_1,U_0`, so leading zero digits are required table rows.
- Strict `k=3,r=1` has `q=3`, `M=7`, and `R=3^7=2187`. `k=2,r=1` has 16 rules; `k=2,r=2` has 64; `k=5,r=1` has `5^13=1,220,703,125`.
- General `k,r` requires arbitrary precision even though the strict codes are small: `k=8,r=1` already has `R=8^22=2^66`. Program/batch records therefore use stable structural references or tagged decimal strings rather than `int64`, float, or JSON numbers.
- The source code/table is losslessly expandable to an exhaustive table by `T(a_-r,...,a_r)=U(sum_i nu(a_i))`, but that expansion is an explicit verified relation. It cannot replace the aggregate, valuation, and sum-table identity.

### Variant disposition

| Profile | Semantic relation |
|---|---|
| `k=2,r=1` | Sixteen-rule totalistic restriction of T01; same T03 aggregate/table evaluator and shared assignment executor. |
| `k=3,r=1` | Strict profile and T04 preset; seven rows and 2,187 codes. |
| Higher `k`, radius one | T05 parameterization; `M=3k-2`, with no new execution mechanics. |
| General finite `r>=1` | Direct Notes parameterization with `q=2r+1`; changes read geometry and table cardinality under strict validation, not commit semantics. |
| Exhaustive T01/T02 table | Explicit aggregate-expansion relation; many ordered contexts share one T03 row, so the exhaustive table is not native T03 identity. |
| Stable zero background | T06 predicate `U(0)=nu^-1(0)`, equivalently `code mod k=0` in the canonical codec; never a base validator or seed assumption. |
| Left-right/reflection symmetry | Implied property of equal-weight sum for the symmetric radius stencil; T07 owns general classification/transforms, not a T03 flag. |
| Code 420/additive profiles | A table may additionally satisfy an algebraic formula such as `U(s)=nu^-1((-s) mod 3)`; additivity is a property/proof or alternate description, not hidden formula execution. |
| Color histogram/nonzero count | Different quotient: `(0,2,0)` and `(1,0,1)` have equal sum but different histograms. Neither can substitute for source T03 when `k>2`. |
| Outer/semi-totalistic | Retains center or another designated value separately and therefore has a product case domain and different codec. |
| Unequal/negative weights or thresholding | Different aggregate/image and often different symmetry; source weighted examples and generic weighted built-in forms are siblings, not T03 parameters. |
| Higher-dimensional or continuous aggregates | Different geometry or value/rule codomain; T44's continuous aggregate-map feedback remains a separate construction. |

## Current API Fit

| Construction element | Fit | Evidence and consequence |
|---|---|---|
| Numeric `A={0,...,K-1}` alphabet | DIRECT data shape | The schema explicitly includes finite `K`-color integer alphabets (`simple_programs.md:200-230`). T03 additionally couples one exact numeric valuation to aggregate and codec identity. |
| Symbolic or arbitrary numeric colors | PRINCIPLED EXTENSION | The generic alphabet admits symbols, but T03 needs a validated bijection to canonical integer values. An alphabet order or palette alone cannot supply arithmetic meaning. |
| Fixed 1D state/support and all-site transition | DIRECT with T01 qualification | Current field/snapshot/parallel-next-slice semantics fit (`simple_programs.md:87-113,1767-1793,2156-2199`); finite `SHAPE` remains a realization, not native `Z`. |
| Fixed radius neighborhood | DIRECT/PARAMETERIZATION | Static compact relative selectors can express `[-r,...,+r]` (`simple_programs.md:360-450,620-650`). Center inclusion, multiplicity, current-time read, and arity must be pinned. |
| `TOTALISTIC` aggregate-plus-table responsibility | PARAMETERIZATION / PRINCIPLED EXTENSION | The schema has the right two-stage shape (`simple_programs.md:1964-1997`), but does not define the source numeric valuation, exact sum image, row order, completeness, or code. |
| Numeric sum versus exact average | PRINCIPLED EXTENSION | Numeric sum is listed, but the API needs one closed equal-weight sum descriptor and exact `s/q` labeling. A generic reducer/callback or floating mean is not source semantics. |
| K-color histogram example | SEMANTIC MISMATCH for T03 | The documented histogram (`simple_programs.md:2010-2027`) preserves distinctions the strict totalistic sum erases; it is a separate permutation-invariant rule quotient. |
| Complete sum table/cardinality | PRINCIPLED EXTENSION | Table arity must derive as `M=1+(k-1)(2r+1)` and validate every output in `A`; the current schema supplies no sum-case domain object. |
| Wolfram base-`k` sum codec | PRINCIPLED EXTENSION | Needs a total bidirectional arbitrary-precision codec with sum zero least significant and structural table identity primary. T02's bigint responsibility composes, but its ordered-context address does not. |
| Typed assignment and parallel commit | DIRECT T01 reuse | Aggregate lookup still returns one same-site value, so `Assign` plus atomic fixed-field update applies unchanged and no eleventh law is needed. |
| Seed, boundary, trace, and views | PARAMETERIZATION / NOT APPLICABLE to program | Existing finite seed/boundary/trace forms can realize runs, while background filtering, average labels, palette, raster, class, and horizons remain downstream. |
| Outer, weighted, histogram, additive, quiescent, symmetric profiles | NOT APPLICABLE to base T03 | These require separate summary types, properties, analyzers, or presets and cannot become permissive flags on the source aggregate. |

## Current Runtime Fit

| Component | Fit | Exact finding |
|---|---|---|
| `alphabets.int_range_alphabet(k,0)` | DIRECT primitive, incomplete wiring | Supplies the canonical values `0..k-1` (`src/ca/alphabets.py:59-86`), but `Dynamics` carries no alphabet or valuation and spatial rollout never validates membership. |
| `alphabets.symbolic(values)` | PRINCIPLED EXTENSION for T03 | Preserves deterministic values (`alphabets.py:145-179`) but supplies no numeric valuation; rollout coerces all spatial states to `int64`, so symbolic T03 cannot execute honestly. |
| `neighborhoods.eca(radius=r)` / selectors | DIRECT finite geometry | Produces a static current-time 1D radius stencil (`neighborhoods.py:551-569`). Strict presets must pin center inclusion and arity; native support/causal lowering remain absent. |
| `rules.totalistic(component,aggregate)` | PARAMETERIZATION / SEMANTIC MISMATCH as a T03 spec | Records `sum` or `count` but no alphabet, valuation, arity, reachable image, `state_count`, table, or code (`rules.py:198-216`). Consequently `lookup` cannot derive T03 `M`/`R`. |
| `rules.lookup` / `validate` | DIRECT counting helper, incomplete rule model | `validate(a,*S_i)` correctly computes `a^product(S_i)` from already-known channel sizes (`rules.py:128-166`), but lookup has only `lsb_rule_bits`, no structural aggregate table/base-`k` output, and no totalistic channel range (`rules.py:262-295`). |
| `_channel_state` totalistic step | DIRECT integer-sum kernel only | It sums all read integers (`rollout.py:742-777`), which matches canonical T03 locally, but ignores the declared aggregate mode, forces `int64`, and validates neither values nor fixed arity. Thus current `count` is merely sum outside binary alphabets. |
| `_lookup_index` | PARAMETERIZATION for one sum channel | One channel happens to pass sum through unchanged, but the helper bit-shifts multiple channels as binary positions (`rollout.py:811-822`) rather than using typed case domains or mixed radices. |
| Spatial rule output | SEMANTIC MISMATCH | Scalar and batch spatial paths always decode `(rule_id >> index) & 1` (`rollout.py:650-682`); they cannot return color `2`, use base `k`, or execute a structural sum table. |
| Generic rule/spec routing | SEMANTIC MISMATCH | Rollout/apply-rule whitelist named Phase 1 families and reject ordinary `lookup` (`rollout.py:145-212,292-331`); `specs.rule_from_spec` exposes only six named families (`specs.py:117-145`). Adding `totalistic` to these switches would repeat the architecture failure. |
| Rule IDs and raw batches | PARAMETERIZATION only for small profiles | Scalar Python `int` is unbounded, but batch normalization and `RawBatch.rule_ids` use `numpy.int64` (`rollout.py:264-288`, `specs.py:70-81`). General `k,r` needs structural program references and tagged decimal-string codes. |
| `Dynamics`, seeds, boundary, trace | PARAMETERIZATION / PRINCIPLED EXTENSION | Finite field mechanics are reusable, but alphabet/valuation, semantic support, typed rule/result/update, program identity, and observation scope are missing (`specs.py:23-81`). |
| Dyadrads/Dyadaxes/Lagcounts | NOT T03 conformance | These binary families use counts followed by gates or sampled/composed lookup (`rules.py:369-518`). They demonstrate a reusable reduction kernel only; their component products, gates, and 256-code spaces are not source T03. |

### Test fit

- `tests/test_rules.py:9-45` checks only declared counts for named binary families; it never constructs a pure totalistic channel plus complete output table or checks `M=3k-2`.
- `tests/test_rollout.py:263-435` covers rule-zero extinction and scalar/batch parity for gated binary spatial families. Binary output and shared-code parity cannot detect a base-3 decoder, sum-row order, histogram substitution, or evolving zero background.
- No test distinguishes equal-sum/different-histogram contexts, produces output color `2`, exercises `k=3,r=1` code 777/867/420, checks `k=2,r=2` code 10, round-trips a code above signed 64-bit, or proves old-snapshot totalistic assignment.
- There is no test that T04/T05 presets resolve to the same structural rule/executor, that T06 is exactly the sum-zero-row predicate, or that T07 symmetry is derived rather than a runtime flag.

## Principles Audit

| Principle | T03 result |
|---|---|
| 0–2 | Evidence requires one new closed rule-input quotient, not a new executor. T01/T02 support, reads, assignment, commit, successor, realization, and trace semantics remain valid; a `totalistic` rollout branch would duplicate them. |
| 3–4 | Neighborhood gathers the fixed old stencil; the rule's closed aggregate maps it to one sum row and returns typed `Assign`; update commits all assignments atomically. The aggregate is not hidden in frontier/update. |
| 5 | State contains only fixed support and the current color field. Sum, average, table code, search state, background filter, and behavior class are program/derived/observer data, not hidden state. |
| 6–8, 12 | A finite `[t,x,0,0]` trace may represent a realization, but topology, numeric color valuation, code digits, palette tones, crop, and batch storage retain distinct identities. |
| 9 | `k`, valuation, fixed arity `q`, reachable sum image, `M`, complete table, and codec are genuinely coupled and must validate together. Palette, seed, boundary, horizon, and execution backend remain independent. |
| 10 | T03/T04/T05 presets may validate generic, three-color, and higher-color profiles only by returning the same ordinary aggregate-table rule and shared fixed-lattice spec. |
| 11 | Equal-weight exact sum and complete sum lookup are defining. Integer vectorization, exact-average labels, exhaustive expansion, table gather, bigint representation, and batching are incidental or explicit relations. |
| 13–15 | Canonical tests must use equal-sum/different-histogram contexts, nonbinary outputs, code-order fixtures, non-quiescent backgrounds, larger `r`, old-snapshot adversaries, and independent source codes. Pixels or scalar/batch parity alone are insufficient. |
| 16 | One typed valuation/aggregate/case-table/codec boundary is architecture. A callback reducer, histogram substitution, exhaustive-table-only storage, family switch, reversed digits, or binary fallback is a shim. |

D112's structural-table-first and arbitrary-precision policy composes at the finite-table/serialization responsibility level; T03 has a distinct sum-case domain and codec from T02's ordered context table. D114 is resolved concretely: T03 numeric valuation and aggregate are program semantics, ordered color identity supplies lossless values/code digits, and palette remains a view.

Evidence still unresolved for this architecture pass: exact gallery trajectories/raster parameters; whether any source profile requires noncanonical or non-bijective numeric color values; and whether radius zero, dynamic/masked arity, histogram, outer-totalistic, weighted, or higher-dimensional rules should share a later generalized aggregate interface. Goal 2 must expose these as typed unsupported or separate constructions until their own evidence closes, not infer defaults.

## Exact Semantic Oracle

For a declared arithmetic alphabet `0..k-1` and radius `r`, T03 addresses a neighborhood only by its numeric sum `s`. There are `M = 1 + (k-1)(2r+1)` attainable sums. The source code is the base-`k` encoding `n = sum_s u_s k^s`, so sum zero is the least-significant digit and `u_s = floor(n/k^s) mod k`. Consequently there are `k^M` rules. Division by the fixed neighborhood cardinality turns sum into the source's exact average labels without changing the cases; it is not a floating operation or permission to infer numeric values from a palette.

This dependency-free oracle pins the case/rule counts, exact code order, source examples, strict sum rather than histogram equivalence, permutation invariance, injective denotational lowering to T02, non-totalistic rejection, quiescent-background restriction, arbitrary-precision pressure, a radius-two example, and a reproducible rule-777 trajectory. Lowering is a compiler relation: the native T03 program remains its aggregate plus `M`-entry table, not a `k^(2r+1)` ordered table.

```bash
python3 - <<'PY'
from hashlib import sha256
from itertools import product, permutations

def cases(k,r): return 1+(k-1)*(2*r+1)
def rules(k,r): return k**cases(k,r)
def digits(code,k,r):
    assert 0<=code<rules(k,r)
    return tuple(code//(k**s)%k for s in range(cases(k,r)))
def display(code,k,r): return ''.join(map(str,reversed(digits(code,k,r))))
def out(code,k,r,neighborhood): return digits(code,k,r)[sum(neighborhood)]
def full(code,k,r):
    return tuple(out(code,k,r,q) for q in product(range(k),repeat=2*r+1))
def full_code(code,k,r):
    return sum(v*k**i for i,v in enumerate(full(code,k,r)))

assert [cases(k,r) for k,r in ((2,1),(2,2),(3,1),(5,1))]==[4,6,7,13]
assert [rules(k,r) for k,r in ((2,1),(2,2),(3,1),(5,1))]==[16,64,2187,1220703125]
assert digits(777,3,1)==(0,1,2,1,0,0,1)
assert display(777,3,1)=='1001210'
assert display(867,3,1)=='1012010'
assert display(420,3,1)=='0120120'
assert all(out(420,3,1,q)==(-sum(q))%3 for q in product(range(3),repeat=3))
assert digits(10,2,2)==(0,1,0,1,0,0)
assert all(out(10,2,2,q)==(sum(q) in (1,3))
           for q in product(range(2),repeat=5))

# Equal sum, unequal histograms: the strict aggregate must merge these.
assert out(777,3,1,(0,2,0))==out(777,3,1,(1,0,1))
assert sorted((0,2,0))!=sorted((1,0,1))
for code in range(rules(3,1)):
    for q in product(range(3),repeat=3):
        for p in set(permutations(q)):
            assert out(code,3,1,q)==out(code,3,1,p)

# Every totalistic table lowers injectively to, but is not identified with, T02.
seen=set()
for code in range(rules(3,1)):
    lowered=full_code(code,3,1)
    assert lowered not in seen
    seen.add(lowered)
    assert all((lowered//(3**i))%3==v
               for i,v in enumerate(full(code,3,1)))
assert len(seen)==2187

def ordered_out(code,k,q):
    i=0
    for x in q: i=k*i+x
    return code//(k**i)%k

# T02 rule 921408 distinguishes equal-sum permutations and must be rejected.
assert tuple(ordered_out(921408,3,q)
             for q in ((0,0,1),(0,1,0),(1,0,0)))==(2,1,1)

# Background preservation is a restriction, not part of base T03.
assert sum(1 for n in range(rules(3,1)) if n%3==0)==3**6
assert out(1,3,1,(0,0,0))==1
assert 8**22>2**63-1

def evolve(code,k,r,seed,events):
    pad=r*events+2
    state=[0]*pad+list(seed)+[0]*pad
    rows=[state]
    for _ in range(events):
        old=rows[-1]
        rows.append([
            out(code,k,r,tuple(old[x+d] if 0<=x+d<len(old) else 0
                               for d in range(-r,r+1)))
            for x in range(len(old))
        ])
    return rows,pad

# Source execution is one old-snapshot parallel event, not an in-place scan.
old=[1,0,0]
parallel=[out(2,2,1,tuple(old[x+d] if 0<=x+d<len(old) else 0
                          for d in (-1,0,1)))
          for x in range(len(old))]
in_place=old[:]
for x in range(len(in_place)):
    in_place[x]=out(2,2,1,tuple(in_place[x+d]
                                if 0<=x+d<len(in_place) else 0
                                for d in (-1,0,1)))
assert parallel==[1,1,0] and in_place==[1,1,1]

def word(row):
    used=[i for i,v in enumerate(row) if v]
    return ''.join(map(str,row[min(used):max(used)+1])) if used else ''

rows,pad=evolve(777,3,1,[1],8)
trace=[word(row) for row in rows]
assert trace==[
    '1','111','12121','1100011','122101221','11001210011',
    '1221110111221','110001222100011','12210110101101221'
]
rows,pad=evolve(777,3,1,[1],100)
crop=[row[pad-102:pad+103] for row in rows]
blob=bytes(v for row in crop for v in row)
assert len(crop)==101 and all(len(row)==205 for row in crop)
assert tuple(blob.count(v) for v in range(3))==(13972,4386,2347)
assert sha256(blob).hexdigest()==\
       '4e835285f8b44f62ff98ae3ed4eccf4083b93d565121c0ebbbcc7889fae8878e'

print('T03 semantic oracle: PASS')
print('case_counts=',(cases(2,1),cases(2,2),cases(3,1),cases(5,1)))
print('rule_counts=',(rules(2,1),rules(2,2),rules(3,1),rules(5,1)))
print('rule_777_digits=',digits(777,3,1))
print('rule_777_display=',display(777,3,1))
print('rule_420_display=',display(420,3,1))
print('rule_10_r2_digits=',digits(10,2,2))
print('rule_777_trace=',','.join(trace))
print('rule_777_counts=',tuple(blob.count(v) for v in range(3)))
print('rule_777_sha256=',sha256(blob).hexdigest())
PY
```

Recorded output:

```text
T03 semantic oracle: PASS
case_counts= (4, 6, 7, 13)
rule_counts= (16, 64, 2187, 1220703125)
rule_777_digits= (0, 1, 2, 1, 0, 0, 1)
rule_777_display= 1001210
rule_420_display= 0120120
rule_10_r2_digits= (0, 1, 0, 1, 0, 0)
rule_777_trace= 1,111,12121,1100011,122101221,11001210011,1221110111221,110001222100011,12210110101101221
rule_777_counts= (13972, 4386, 2347)
rule_777_sha256= 4e835285f8b44f62ff98ae3ed4eccf4083b93d565121c0ebbbcc7889fae8878e
```

## Asset and Raster Audit

The native asset boundary is one-dimensional, synchronous, finite-color totalistic evolution. The strict run begins with the rule-777 definition on printed page 60 and ends with the 9,000-step rule-1599 view on printed page 70. Printed page 71 changes construction to mobile automata with one active site and is excluded. Later one-dimensional totalistic galleries, exact Notes invocations, property illustrations, and emulation panels remain evidence, but a random seed, palette, crop, displayed-row count, or behavior label is never imported into rule identity.

### Included direct assets

All paths below are relative to `ref/A-New-Kind-of-Science/`.

| Asset path | Bytes | Dimensions | SHA-256 | Source-permitted role |
|---|---:|---:|---|---|
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_75_Figure_6.jpeg` | 51,178 | `610x446` | `acb13963632286960ca61b616ff2f45a940750f3ab7deb5e6fbf696543015c15` | Canonical code-`777` rule diagram and 43-by-22 initial-inclusive grid. The caption explicitly maps `0/1/2` to white/gray/black and orders sums `0..6`; this is the direct raster golden. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_76_Figure_2.jpeg` | 174,691 | `1109x1279` | `8c11659c8bd63d37a972c5ffab376b62948f7c4e05f9fd10f239e51464f4084d` | Fifty labelled three-color rules `993,996,...,1140`, filtered to preserve white background. Exact horizon is unstated, so labels/filter are golden but trajectories are not. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_77_Figure_6.jpeg` | 128,836 | `892x716` | `4c1f8894016156dc4d473e911e0fa5c7db16711a8c2873fa493fb7854ad41c66` | Single-gray finite/repeating examples labelled `600,843,870,1086,1167,1329,1572,1815,1842`; period/class and crop are observers. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_78_Figure_2.jpeg` | 90,930 | `1107x615` | `5c5ca56f3e8141c3aa4d7648f3ebe34a911515bf9dfc9118795135736f69b879` | Single-gray growing/repetitive examples `219,957,966,1884`; no exact displayed-row convention is stated. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_78_Figure_4.jpeg` | 81,348 | `1134x621` | `088016843cb7d74ad621ebed323401dfb9783ce061ece275ba36b0815c7dfa28` | Single-gray nested examples `237,420,948,1749`; “nested” is a behavior observer, not a rule flag. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_79_Picture_2.jpeg` | 278,065 | `886x1399` | `355d13fde85b89c2e3e26d1ae199e30ad2191b0bcbd3d4c89ac76785fa1ebc86` | Codes `177,912,2040`, with 300 steps described. Whether “steps shown” counts the initial state and the exact resampling/crop remain unstated. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_81_Picture_1.jpeg` | 75,030 | `826x446` | `0617e6b01a1faa43e968051ff8716171b665e79d087c8c13a47811c0520f3014` | Complex-behavior panel labelled code `1041`; identity/property evidence only. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_81_Picture_2.jpeg` | 86,949 | `816x429` | `6efe4dc8703a3045bd6189f930a0cdb44e59dc71f38dc91a52e8faa84e801a7e` | Complex-behavior panel labelled code `1635`; its later continuation is Picture 82/1. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_81_Picture_3.jpeg` | 75,408 | `869x470` | `b3812f8742bf08299270512de2cdffa57ac14be5b10a6cdefa60d4878173553c` | Complex-behavior panel labelled code `2049`; its later continuation is Picture 83/1. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_82_Picture_1.jpeg` | 423,048 | `1061x1381` | `aa534aa358e74235ef5de86980c5c6f0895bac2b616e990c1cda7253639a4511` | Long-run continuation of code `1635`; “3,000 steps” is a displayed view, not a successor limit. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_83_Picture_1.jpeg` | 513,252 | `1067x1387` | `cd4f0434c12f9b86bdde3730270451df2dfb503194d22bc04d0609973e9d3a77` | Long-run continuation of code `2049`; same disposition as Picture 82/1. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_84_Picture_2.jpeg` | 74,243 | `764x747` | `02782253cc66a9de075af5d1d02f224645e443040f5ff6001fef6467a7013cbe` | Edge-of-growth examples `357,600,1599,2058`, described as 250 steps; behavior outcome and view are not native semantics. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_85_Picture_2.jpeg` | 345,552 | `1107x1360` | `2374289d970042909316f68cf240379d6f2826ba90dab95db0a317e672b91b0f` | Code `1599` from a single gray cell, displayed as three 3,000-step columns. The 8,282-step resolution/31-structure claim is observer analysis, not a halt rule. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_122_Figure_2.jpeg` | 186,914 | `1098x1164` | `ccd7a43a495d01a22300c4b9abbb3ff1b13a3ef37389e77ca491ec805cbaa822` | Radius-one totalistic comparison: two-color codes `0..7`, three-color `578..585`, four-color `107395..107402`, five-color `180197741..180197748`. It confirms parameterization, not one shared palette/seed. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_248_Figure_2.jpeg` | 281,697 | `1086x1389` | `b2a20cb8095eb211fedd963d622222ca98fe0428f397b71bef90db8fa6871957` | Binary radius-two totalistic codes `0,2,...,62` from random conditions; exact PRNG/sample is absent. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_249_Picture_1.jpeg` | 273,017 | `1082x1403` | `f7b2834be41656cff9512b7affdd5fa57640bbbb6ecd93da1440202bf113f7ef` | Three-color radius-one codes `1002,1005,...,1095` from random conditions; overlaps Picture 76/2 in rule identity but not seed/view. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_251_Picture_1.jpeg` | 429,298 | `1123x1383` | `41cfc762284fdcd65e5663fb7631aa4c504aea46a746a8a4ed24407b76b89196` | Class-4 code `1815`, 1,500 displayed steps from an unspecified random initial condition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_252_Picture_2.jpeg` | 556,865 | `1121x1377` | `120e95a57f683744ff3e71981f4fa07ff850d0cad5633bf4d2f27906a76e909f` | Class-4 code `2007`, same random-run disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_253_Picture_1.jpeg` | 511,097 | `1227x1519` | `148a433a11b4889c91c1a7be3c6f00172a3961428e6d41c47a06954136245faf` | Class-4 code `238`, same random-run disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_254_Picture_1.jpeg` | 568,496 | `1117x1383` | `d32b7fc3dedc9f262e5a3d3d928d1d7d94d1a219fd75aeeefdb988c74869a168` | Class-4 code `2043`, same random-run disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_2.jpeg` | 7,400 | `273x171` | `b175f64e60cf41042d8ba6a11ed8d04eec4a8101bef8f9f231aae532eca6ca06` | Borderline-class code `219`; class assignment is an observer property. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_3.jpeg` | 13,612 | `259x167` | `00ef0063254d4f75734cd76d8f2d07de4ae1d6b041b9664197c2da99641d8b14` | Borderline-class code `438`; same disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_4.jpeg` | 9,310 | `267x186` | `700d71a0beb145c953ca87f4d8649aecd7b7d60df69ccd569cba02f6daeb1acc` | Borderline-class code `1380`; same disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_5.jpeg` | 11,188 | `273x165` | `ae44e4411841a03fced5b5114f6cef4be62793c6a58c9a4ce6c357d214c7ce35` | Borderline-class code `1622`; same disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_256_Figure_2.jpeg` | 328,297 | `1092x1367` | `1c4967f6967d8e813b2a281e2615dc8bef272eb57789b60e23c950de5e6bc01f` | Four-color radius-one totalistic sequence across behavior classes; the selection/class transition is downstream analysis. |
| `CHAPTERS/9-Fundamental-Physics/Images/_page_541_Picture_3.jpeg` | 37,411 | `436x268` | `83d828ba45f3f3e7390bf66183643a32c3c7b83646cc3880aedf099a49284c1e` | Code `294` persistent structures on a largely random background; random field is not serialized. |
| `CHAPTERS/9-Fundamental-Physics/Images/_page_541_Picture_4.jpeg` | 43,238 | `418x250` | `d96c865b43b912ce4e2d6f0c2ddf659eed32f17db48c151161c364187fcc7a1f` | Code `1893` persistent boundaries on a largely random background; same disposition. |
| `CHAPTERS/11-The-Notion-of-Computation/Images/_page_707_Figure_1.jpeg` | 327,160 | `1130x1111` | `974e12d28e8acc6fb4af26f7b1dd09eae1f30d802666a61f41abed8ec2d42e19` | Mixed class-4 gallery with direct T03 panels `(c)` binary radius-two code `52` and `(d)` three-color code `1815`; panels `(a,b)` are ECA/second-order siblings within the same asset. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_753_Picture_3.jpeg` | 164,036 | `912x565` | `8cfad05d53abb9791d37dd6d8262ec12dbc08bb1d72866ce34c46ecb99a94a88` | Codes `870,843,1599` used to illustrate reducibility; the property label is not executable rule data. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_769_Figure_1.jpeg` | 298,516 | `1065x1308` | `a980effe214906d991e8ca9180cb9f9d6eade2f978a8358487a60bb1728058f3` | Four-color code `1004600` with four illustrated finite seeds. Seed strips are not serialized as digit arrays, so death/unknown outcomes are property evidence only. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_25.jpeg` | 5,511 | `211x117` | `d53637ce9ec50330d5fa6239b23f48d57b563266a0085a23517d4538020fd5fb` | Exact Notes invocation `CellularAutomaton[{867,{3,1},1},{{1},0},50]`: code `867`, single `1`, repeating-`0` background, 50 updates. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_897_Picture_19.jpeg` | 37,091 | `553x155` | `2cedbff5433363c86786feea8804c95229179daf455f07ee8071d6345223894b` | Binary radius-two code `10`, whose table makes sums `1` and `3` black; source identifies a single-black start but not this panel's exact displayed-row convention. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_897_Picture_20.jpeg` | 77,026 | `543x329` | `ee9cadafa6b0b5a45d9cfb4ed310aff751e84f46a86277821e9f971f3c067b3f` | Long companion view for the same code-`10` Notes example; no independent rule or exact horizon. |
| `BACK-MATTER/Index/Images/_page_963_Picture_8.jpeg` | 3,114 | `144x152` | `1fb4f0b4c03d8ba9f9fdeb67a0bbda2d786ed7ceeb13cdd8c31337ccd54bcdfb` | First Notes frequency-of-classes chart for one-dimensional totalistic `k,r` profiles; aggregate property only. |
| `BACK-MATTER/Index/Images/_page_963_Picture_9.jpeg` | 3,226 | `136x148` | `515f5de1423a9164ed6def92d786346f64c15a0a87ba07b723c069e62829caf6` | Second frequency chart; same disposition. |
| `BACK-MATTER/Index/Images/_page_963_Picture_10.jpeg` | 3,654 | `138x158` | `4b5ff621a668c5b706cdec0481cf3849facb7395d256dfd7c39b471d95fd018f` | Third frequency chart; same disposition. |
| `BACK-MATTER/Index/Images/_page_963_Picture_11.jpeg` | 3,717 | `136x152` | `7c660bbbb03b2d3116aab32cd50a5a3ff094961d49b403148531b36759335d6b` | Fourth frequency chart; same disposition. |

### Relations, exclusions, and routing

| Asset path | Bytes | Dimensions | SHA-256 | Disposition |
|---|---:|---:|---|---|
| `CHAPTERS/11-The-Notion-of-Computation/Images/_page_670_Figure_1.jpeg` | 281,966 | `1064x1224` | `a1a2a5c04b509ecc0357273387b2950d179478c65406427751904987ec9e8d3e` | Relation-only: code `1599` is block-emulated by a binary radius-five CA. Encoding/decoding and the emulator are not T03 native events. |
| `CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_171_Picture_5.jpeg` | 4,640 | `277x91` | `6695e1c946cf6adaa04a3915f2c720f69de4d18b74a81a01aaab346052119455` | Relation-only continuous average-map analog; continuous values/codomain belong to T44. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_74_Picture_5.jpeg` | 134,131 | `858x423` | `713c4c55c6a004d76c5e47f1f39513bb1656f35feb0fe9aa72c4503ca311cdc6` | Immediate preceding rule-73 ECA material; exhaustive ordered binary rule, not a totalistic fixture. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_86_Picture_7.jpeg` | 30,221 | `240x500` | `59213fbf1a0e6904a6566043c889acd32853d799d5a71bfec1e2d0c45bb1eec5` | First post-boundary mobile-automaton evolution: one active site and sequential movement, not all-site T03. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_86_Picture_8.jpeg` | 7,295 | `506x51` | `d844f2419d7ff2a748a93e4ae6dd09c947bf5ed0723aa1defb4354c810b1fb25` | Mobile-automaton rule diagram paired with Picture 86/7; same exclusion. All later page-86+ mobile galleries inherit this construction boundary. |
| `CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_185_Picture_9.jpeg` | 3,425 | `213x114` | `abfbc90a8bdab839ac452194adf8f7e30258e877967a79ac71db59b1a716df75` | Two-dimensional center-plus-four-neighbor totalistic form; different support geometry. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_261_Figure_2.jpeg` | 309,273 | `1109x1297` | `49f35fe65202ef7fbfee2da92b7460d36fc329b66a553782ebf8991f237944dd` | Two-dimensional five-cell totalistic random gallery; geometry sibling, not a T03 raster. |
| `CHAPTERS/10-Processes-of-Perception-and-Analysis/Images/_page_566_Figure_2.jpeg` | 140,400 | `1032x699` | `6d66d95c8e3c286272cded005d60557ce7a075ffebfd268486c23abe13a29a1e` | Two-dimensional **outer** totalistic rules `54,222,374`; center is retained separately and the codec differs. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_23.jpeg` | 4,478 | `160x117` | `132528352f363e52a20e73e1e8341203126448c0c6c8545eed48626eaddac16c` | Adjacent exact general ordered-table rule `921408`; T02, not aggregate identity. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_28.jpeg` | 5,342 | `205x110` | `2da239aceec3720e5aeccd5de8898c37fe7e975230814c0b3a8e3dcacbde9096` | Adjacent function-callback neighborhood rule; callback execution is explicitly not T03. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_31.jpeg` | 4,370 | `117x117` | `ca086555513a6d8ba5bcbe92d97af26e55aa899cf629e0ab61d8fa8c71b81586` | Adjacent 2D nine-neighbor totalistic code `3702`; geometry exclusion. |
| `BACK-MATTER/Colophon/Images/_page_1132_Picture_2.jpeg` | 68,468 | `606x308` | `422ce8c21c465e2ffdffdb0f691f9521a21b9389897336dd4e4a2c716295c589` | Adjacent three-color two-neighbor general rule `2144`; its totalistic-universality paragraph names candidates but this picture is not one. |

The monolith omits `Images/` from links. Chapter split files route to the same physical JPEGs and are duplicate references, not additional assets. The page-883 and page-897 files are Notes-for-Chapter-2 evidence despite their Chapter-12 placement. The four page-963 Notes charts live under `BACK-MATTER/Index/Images`, while the page-1132 sibling lives under `BACK-MATTER/Colophon/Images`. No two audited files have identical bytes.

The dependency-free metadata oracle parses JPEG SOF markers and pins all 37 included, ten excluded, and two relation-only files:

```bash
python3 - <<'PY'
from hashlib import sha256
from pathlib import Path

ROOT=Path('ref/A-New-Kind-of-Science')
items={
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_75_Figure_6.jpeg':(51178,610,446,'acb13963632286960ca61b616ff2f45a940750f3ab7deb5e6fbf696543015c15','I'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_76_Figure_2.jpeg':(174691,1109,1279,'8c11659c8bd63d37a972c5ffab376b62948f7c4e05f9fd10f239e51464f4084d','I'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_77_Figure_6.jpeg':(128836,892,716,'4c1f8894016156dc4d473e911e0fa5c7db16711a8c2873fa493fb7854ad41c66','I'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_78_Figure_2.jpeg':(90930,1107,615,'5c5ca56f3e8141c3aa4d7648f3ebe34a911515bf9dfc9118795135736f69b879','I'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_78_Figure_4.jpeg':(81348,1134,621,'088016843cb7d74ad621ebed323401dfb9783ce061ece275ba36b0815c7dfa28','I'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_79_Picture_2.jpeg':(278065,886,1399,'355d13fde85b89c2e3e26d1ae199e30ad2191b0bcbd3d4c89ac76785fa1ebc86','I'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_81_Picture_1.jpeg':(75030,826,446,'0617e6b01a1faa43e968051ff8716171b665e79d087c8c13a47811c0520f3014','I'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_81_Picture_2.jpeg':(86949,816,429,'6efe4dc8703a3045bd6189f930a0cdb44e59dc71f38dc91a52e8faa84e801a7e','I'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_81_Picture_3.jpeg':(75408,869,470,'b3812f8742bf08299270512de2cdffa57ac14be5b10a6cdefa60d4878173553c','I'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_82_Picture_1.jpeg':(423048,1061,1381,'aa534aa358e74235ef5de86980c5c6f0895bac2b616e990c1cda7253639a4511','I'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_83_Picture_1.jpeg':(513252,1067,1387,'cd4f0434c12f9b86bdde3730270451df2dfb503194d22bc04d0609973e9d3a77','I'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_84_Picture_2.jpeg':(74243,764,747,'02782253cc66a9de075af5d1d02f224645e443040f5ff6001fef6467a7013cbe','I'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_85_Picture_2.jpeg':(345552,1107,1360,'2374289d970042909316f68cf240379d6f2826ba90dab95db0a317e672b91b0f','I'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_122_Figure_2.jpeg':(186914,1098,1164,'ccd7a43a495d01a22300c4b9abbb3ff1b13a3ef37389e77ca491ec805cbaa822','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_248_Figure_2.jpeg':(281697,1086,1389,'b2a20cb8095eb211fedd963d622222ca98fe0428f397b71bef90db8fa6871957','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_249_Picture_1.jpeg':(273017,1082,1403,'f7b2834be41656cff9512b7affdd5fa57640bbbb6ecd93da1440202bf113f7ef','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_251_Picture_1.jpeg':(429298,1123,1383,'41cfc762284fdcd65e5663fb7631aa4c504aea46a746a8a4ed24407b76b89196','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_252_Picture_2.jpeg':(556865,1121,1377,'120e95a57f683744ff3e71981f4fa07ff850d0cad5633bf4d2f27906a76e909f','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_253_Picture_1.jpeg':(511097,1227,1519,'148a433a11b4889c91c1a7be3c6f00172a3961428e6d41c47a06954136245faf','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_254_Picture_1.jpeg':(568496,1117,1383,'d32b7fc3dedc9f262e5a3d3d928d1d7d94d1a219fd75aeeefdb988c74869a168','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_2.jpeg':(7400,273,171,'b175f64e60cf41042d8ba6a11ed8d04eec4a8101bef8f9f231aae532eca6ca06','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_3.jpeg':(13612,259,167,'00ef0063254d4f75734cd76d8f2d07de4ae1d6b041b9664197c2da99641d8b14','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_4.jpeg':(9310,267,186,'700d71a0beb145c953ca87f4d8649aecd7b7d60df69ccd569cba02f6daeb1acc','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_5.jpeg':(11188,273,165,'ae44e4411841a03fced5b5114f6cef4be62793c6a58c9a4ce6c357d214c7ce35','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_256_Figure_2.jpeg':(328297,1092,1367,'1c4967f6967d8e813b2a281e2615dc8bef272eb57789b60e23c950de5e6bc01f','I'),
'CHAPTERS/9-Fundamental-Physics/Images/_page_541_Picture_3.jpeg':(37411,436,268,'83d828ba45f3f3e7390bf66183643a32c3c7b83646cc3880aedf099a49284c1e','I'),
'CHAPTERS/9-Fundamental-Physics/Images/_page_541_Picture_4.jpeg':(43238,418,250,'d96c865b43b912ce4e2d6f0c2ddf659eed32f17db48c151161c364187fcc7a1f','I'),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_707_Figure_1.jpeg':(327160,1130,1111,'974e12d28e8acc6fb4af26f7b1dd09eae1f30d802666a61f41abed8ec2d42e19','I'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_753_Picture_3.jpeg':(164036,912,565,'8cfad05d53abb9791d37dd6d8262ec12dbc08bb1d72866ce34c46ecb99a94a88','I'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_769_Figure_1.jpeg':(298516,1065,1308,'a980effe214906d991e8ca9180cb9f9d6eade2f978a8358487a60bb1728058f3','I'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_25.jpeg':(5511,211,117,'d53637ce9ec50330d5fa6239b23f48d57b563266a0085a23517d4538020fd5fb','I'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_897_Picture_19.jpeg':(37091,553,155,'2cedbff5433363c86786feea8804c95229179daf455f07ee8071d6345223894b','I'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_897_Picture_20.jpeg':(77026,543,329,'ee9cadafa6b0b5a45d9cfb4ed310aff751e84f46a86277821e9f971f3c067b3f','I'),
'BACK-MATTER/Index/Images/_page_963_Picture_8.jpeg':(3114,144,152,'1fb4f0b4c03d8ba9f9fdeb67a0bbda2d786ed7ceeb13cdd8c31337ccd54bcdfb','I'),
'BACK-MATTER/Index/Images/_page_963_Picture_9.jpeg':(3226,136,148,'515f5de1423a9164ed6def92d786346f64c15a0a87ba07b723c069e62829caf6','I'),
'BACK-MATTER/Index/Images/_page_963_Picture_10.jpeg':(3654,138,158,'4b5ff621a668c5b706cdec0481cf3849facb7395d256dfd7c39b471d95fd018f','I'),
'BACK-MATTER/Index/Images/_page_963_Picture_11.jpeg':(3717,136,152,'7c660bbbb03b2d3116aab32cd50a5a3ff094961d49b403148531b36759335d6b','I'),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_670_Figure_1.jpeg':(281966,1064,1224,'a1a2a5c04b509ecc0357273387b2950d179478c65406427751904987ec9e8d3e','R'),
'CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_171_Picture_5.jpeg':(4640,277,91,'6695e1c946cf6adaa04a3915f2c720f69de4d18b74a81a01aaab346052119455','R'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_74_Picture_5.jpeg':(134131,858,423,'713c4c55c6a004d76c5e47f1f39513bb1656f35feb0fe9aa72c4503ca311cdc6','X'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_86_Picture_7.jpeg':(30221,240,500,'59213fbf1a0e6904a6566043c889acd32853d799d5a71bfec1e2d0c45bb1eec5','X'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_86_Picture_8.jpeg':(7295,506,51,'d844f2419d7ff2a748a93e4ae6dd09c947bf5ed0723aa1defb4354c810b1fb25','X'),
'CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_185_Picture_9.jpeg':(3425,213,114,'abfbc90a8bdab839ac452194adf8f7e30258e877967a79ac71db59b1a716df75','X'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_261_Figure_2.jpeg':(309273,1109,1297,'49f35fe65202ef7fbfee2da92b7460d36fc329b66a553782ebf8991f237944dd','X'),
'CHAPTERS/10-Processes-of-Perception-and-Analysis/Images/_page_566_Figure_2.jpeg':(140400,1032,699,'6d66d95c8e3c286272cded005d60557ce7a075ffebfd268486c23abe13a29a1e','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_23.jpeg':(4478,160,117,'132528352f363e52a20e73e1e8341203126448c0c6c8545eed48626eaddac16c','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_28.jpeg':(5342,205,110,'2da239aceec3720e5aeccd5de8898c37fe7e975230814c0b3a8e3dcacbde9096','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_31.jpeg':(4370,117,117,'ca086555513a6d8ba5bcbe92d97af26e55aa899cf629e0ab61d8fa8c71b81586','X'),
'BACK-MATTER/Colophon/Images/_page_1132_Picture_2.jpeg':(68468,606,308,'422ce8c21c465e2ffdffdb0f691f9521a21b9389897336dd4e4a2c716295c589','X'),
}

def jpeg_size(data):
    assert data[:2]==b'\xff\xd8'
    sof={0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf}
    i=2
    while i<len(data):
        while i<len(data) and data[i]!=0xff: i+=1
        while i<len(data) and data[i]==0xff: i+=1
        assert i<len(data)
        marker=data[i]; i+=1
        if marker in {0x00,0x01} or 0xd0<=marker<=0xd9: continue
        size=int.from_bytes(data[i:i+2],'big')
        if marker in sof:
            h=int.from_bytes(data[i+3:i+5],'big')
            w=int.from_bytes(data[i+5:i+7],'big')
            return w,h
        i+=size
    raise AssertionError('JPEG SOF marker not found')

counts={'I':0,'X':0,'R':0}; digests=set()
for name,(size,w,h,digest,kind) in items.items():
    data=(ROOT/name).read_bytes()
    assert (len(data),*jpeg_size(data),sha256(data).hexdigest())==(size,w,h,digest)
    assert digest not in digests; digests.add(digest); counts[kind]+=1
assert counts=={'I':37,'X':10,'R':2}
print('T03 metadata oracle: PASS 37 included; 10 excluded; 2 relation-only')
PY
```

Recorded output:

```text
T03 metadata oracle: PASS 37 included; 10 excluded; 2 relation-only
```

### Exact asset semantic oracle

This dependency-free check independently reconstructs the strict code-`777` table and early single-gray trajectory, the exact 50-update Notes invocation for code `867`, the binary radius-two code-`10` rule, and all strict labelled gallery identities. Tables are LSB-first by integer sum; displays reverse them.

```bash
python3 - <<'PY'
from hashlib import sha256

def table(code,k,r):
    width=1+(k-1)*(2*r+1); out=[]
    for _ in range(width): out.append(code%k); code//=k
    assert code==0
    return tuple(out)

def advance(rule,r,state):
    n=len(state)
    return [rule[sum(state[j] if 0<=j<n else 0
                     for j in range(i-r,i+r+1))]
            for i in range(n)]

r777=table(777,3,1)
assert r777==(0,1,2,1,0,0,1)
assert ''.join(map(str,reversed(r777)))=='1001210'
state=[0]*17; state[8]=1; words=[]
for _ in range(9):
    used=[i for i,value in enumerate(state) if value]
    words.append(''.join(map(str,state[min(used):max(used)+1])))
    state=advance(r777,1,state)
assert words==['1','111','12121','1100011','122101221',
 '11001210011','1221110111221','110001222100011',
 '12210110101101221']

r867=table(867,3,1)
assert r867==(0,1,0,2,1,0,1)
state=[0]*101; state[50]=1; blob=bytearray()
for _ in range(51):
    blob.extend(state); state=advance(r867,1,state)
assert tuple(blob.count(v) for v in range(3))==(3692,958,501)
assert sha256(blob).hexdigest()=='185170c0866f76d129fbf3a8843cc731f98b9f012cb98286f01e420532fb53d9'

assert table(10,2,2)==(0,1,0,1,0,0)  # black iff sum is 1 or 3
assert table(52,2,2)==(0,0,1,0,1,1)
strict={
 'p76':tuple(range(993,1141,3)),
 'p77':(600,843,870,1086,1167,1329,1572,1815,1842),
 'p78-growing':(219,957,966,1884),
 'p78-nested':(237,420,948,1749),
 'p79':(177,912,2040),
 'p81':(1041,1635,2049),
 'p84':(357,600,1599,2058),
 'p85':(1599,),
}
assert tuple(map(len,strict.values()))==(50,9,4,4,3,3,4,1)
assert all(table(code,3,1)[0]==0 for codes in strict.values() for code in codes)

comparative={
 2:tuple(range(0,8)), 3:tuple(range(578,586)),
 4:tuple(range(107395,107403)), 5:tuple(range(180197741,180197749))}
for k,codes in comparative.items():
    assert len(codes)==8
    for code in codes: table(code,k,1)
assert len(tuple(range(0,64,2)))==32
assert len(tuple(range(1002,1096,3)))==32
for code,k,r in [(1815,3,1),(2007,3,1),(238,3,1),(2043,3,1),
                 (294,3,1),(1893,3,1),(1004600,4,1)]:
    table(code,k,r)

print('code777_table=',r777,'display=1001210')
print('code777_t0_t8=',','.join(words))
print('code867_51x101_sha256=',sha256(blob).hexdigest())
print('T03 asset semantic oracle: PASS')
PY
```

Recorded output:

```text
code777_table= (0, 1, 2, 1, 0, 0, 1) display=1001210
code777_t0_t8= 1,111,12121,1100011,122101221,11001210011,1221110111221,110001222100011,12210110101101221
code867_51x101_sha256= 185170c0866f76d129fbf3a8843cc731f98b9f012cb98286f01e420532fb53d9
T03 asset semantic oracle: PASS
```

### Strict code-777 raster oracle

Picture 75/6 is source-permitted at cell level without fitting a crop or resampling model: the printed grid itself provides 44 vertical and 23 horizontal boundary lines, hence 43 columns and 22 initial-inclusive rows. The source caption supplies the palette-to-digit mapping. Sampling only cell centers leaves wide non-overlapping JPEG luminance ranges, so the thresholds below are robustness gaps rather than inferred semantics.

```bash
python3 - <<'PY'
from collections import defaultdict
from pathlib import Path
from PIL import Image

path=Path('ref/A-New-Kind-of-Science/CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_75_Figure_6.jpeg')
image=Image.open(path).convert('L')
xs=(37,50,63,76,88,101,114,127,139,152,165,178,190,203,216,
    229,241,254,267,280,292,305,318,331,344,356,369,382,395,
    407,420,433,446,458,471,484,497,509,522,535,548,560,573,586)
ys=(43,56,69,82,95,108,120,133,146,159,171,184,197,210,222,
    235,248,261,273,286,299,312,324)
assert (len(xs)-1,len(ys)-1)==(43,22)
assert all(sum(image.getpixel((x,y))<180 for y in range(43,325))>=275 for x in xs)
assert all(sum(image.getpixel((x,y))<180 for x in range(37,587))>=525 for y in ys)

rule=(0,1,2,1,0,0,1)
state=[0]*43; state[21]=1; history=[]
for _ in range(22):
    history.append(state)
    state=[rule[(state[i-1] if i else 0)+state[i]
                +(state[i+1] if i+1<len(state) else 0)]
           for i in range(len(state))]

seen=defaultdict(list); errors=[]
for row,state in enumerate(history):
    for col,want in enumerate(state):
        x=(xs[col]+xs[col+1])//2; y=(ys[row]+ys[row+1])//2
        lum=image.getpixel((x,y)); seen[want].append(lum)
        got=2 if lum<64 else 1 if lum<192 else 0
        if got!=want: errors.append((row,col,want,got,lum))
assert not errors
ranges=tuple((min(seen[v]),max(seen[v])) for v in range(3))
assert ranges==((247,255),(118,138),(0,10))
print('code777_grid=43x22; sampled_cells=946; luminance_ranges=',ranges)
print('T03 code-777 raster oracle: PASS 0 mismatches')
PY
```

Recorded output:

```text
code777_grid=43x22; sampled_cells=946; luminance_ranges= ((247, 255), (118, 138), (0, 10))
T03 code-777 raster oracle: PASS 0 mismatches
```

The official primary [Chapter 3 PDF](https://files.wolframcdn.com/pub/www.wolframscience.com/nks/nks-ch3.pdf) confirms the strict sequence on PDF pages 11–21 / printed pages 60–70 and the mobile-automaton boundary on PDF page 22 / printed page 71. The official [all-notes PDF](https://files.wolframcdn.com/pub/www.wolframscience.com/nks/nks-notes.pdf) confirms the exact code-`867` invocation on PDF page 20 / printed page 868, code `10` on PDF page 34 / printed page 882, and the frequency charts on PDF page 97 / printed page 948. The extracted `_page_...` filenames are routing identifiers, not printed-page claims.

No other included figure supplies all of exact serialized seed, boundary/background, event-versus-state horizon, spatial crop, palette, and resampling. Consequently the remaining galleries have metadata, labels, filters, and source-stated properties pinned, but no fabricated pixel or trajectory golden.

## Detailed Implementation Plan

1. Build and execute a complete literal/regex manifest across the canonical monolith; disposition every candidate and follow all relevant references.
2. Record every unique construction-relevant passage verbatim with exact provenance and explicit source repairs.
3. Inventory all direct, sibling, relation-only, duplicate, and excluded assets; add only source-permitted semantic/raster oracles.
4. Derive aggregate case space, ordering, code, rule counts, state/update/successor, boundary/seed, variants, and observer separation before evaluating reuse.
5. Audit current API/runtime/tests and completed T01/T02/D111-D114 decisions for direct reuse, parameterization, extension, or mismatch.
6. Write an implementation-ready Goal 2 stage, no-cheating gates, independent review, and global ledger integration.

## Goal 2 Implementation Stage

### G2-T03 — Exact finite-sum rule descriptions over the shared fixed-lattice executor

**Objective:** add one inspectable equal-weight integer-sum aggregate and complete sum-case table so generic T03, T04 `k=3`, T05 higher-color, and direct range-`r` profiles execute through the T01/T02 fixed-lattice `Assign`/atomic-update protocol. A preset is discoverable, but neither rollout nor rule application dispatches on `totalistic`.

**Dependencies:** synthesis-selected G2-T01 fixed regular support, `AllSites`, typed same-site assignment, atomic parallel update, finite realization/causal-window lowering, and event/snapshot trace semantics; G2-T02 ordered finite alphabets, structural finite-table identity, stable program references, and arbitrary-precision decimal-string codecs; T34's lossless exact nonnegative-integer serialization responsibility. T03 adds no update law.

**Concrete files and changes:**

1. Extend `src/ca/alphabets.py` with an immutable validated numeric color valuation. The canonical constructor maps the declared colors bijectively to `0..k-1`; any symbolic relabeling stores the explicit forward/inverse map. Do not derive it from palette, a host set, or incidental array order.
2. Add `src/ca/aggregates.py` with a closed `EqualWeightIntegerSum` descriptor/evaluator carrying valuation identity, fixed arity `q`, and exact image `0..q(k-1)`. It accepts no callback, float mean, dynamic mask, histogram, gate, or arbitrary weights. The exact average is a separate label/query `s/q`.
3. Extend the synthesis-selected `src/ca/rule_tables.py` with a typed aggregate-case domain and immutable complete table `U[0..M-1]`. Reuse a generic finite-table carrier only if exhaustive-context and aggregate-sum domain tags cannot be confused. Validate `M=1+(k-1)q`, every output, leading zeros, stable identity, and lossless structural serialization.
4. Add a versioned `WolframTotalisticCodec(k,q,valuation)` alongside—not inside—the table. Decode/encode with sum zero least significant, validate `0<=n<k^M`, and serialize arbitrary-precision codes as tagged decimal strings. Reuse bigint primitives, not T02's context-index formula.
5. Refine `src/ca/rules.py` so a structural `AggregateLookupRule(aggregate,table)` derives `M/R`, evaluates sum then table, and returns an ordinary typed assignment value. Replace the current loose `totalistic` channel contract or constrain it behind this typed form; retain binary active-count/gate constructs only under their honest names.
6. Replace family-whitelisted spatial routing in `src/ca/rollout.py` (or the synthesis-selected executor) with the shared rule/result/update protocol. Scalar and batch paths gather one old snapshot, invoke the closed rule object, emit same-site assignments, and commit together. They never decode T03 with `right_shift`/`&1`, expand it invisibly to an exhaustive table, or add a T03 branch.
7. Extend `src/ca/specs.py` with alphabet/valuation, semantic support, typed rule/result/update, realization, and stable program-reference fields. Add `src/ca/presets/totalistic.py`: `totalistic(k,code_or_table,r=1)`, `three_color_totalistic(...)`, and `higher_color_totalistic(...)` validate their scopes and return the same generic spec. Seed, boundary, horizon, palette, and gallery filter remain run/view inputs.
8. Update `RawEpisode`/`RawBatch` and `src/ca/viz/export.py` to reference structural programs and optional tagged code strings rather than requiring numeric `int64` rule IDs. Preserve finite `[t,x,0,0]` traces and keep exact-average labels/palettes downstream.
9. Add `tests/test_aggregates.py`, extend `tests/test_rule_tables.py`, and add `tests/test_t03_totalistic_ca.py` plus shared executor/spec/codec tests. Preserve all T01/T02 conformance and current named-family behavior until those families receive their own honest migrations.

**Migration and removal:**

- Do not reinterpret the documented K-color histogram as T03. Give histogram, nonzero count, and binary active count distinct closed summary identities.
- Remove the assumption that every summarized channel is binary or that spatial output is one rule-ID bit. A one-channel sum may index directly, but all case domains and table outputs remain typed.
- Generic `lookup`/aggregate rules must no longer be rejected by family switches. Do not add an interim `lookup` or `totalistic` switch as a compatibility path.
- Preserve Dyadrads/Dyadaxes/Lagcounts semantics as separate composed/gated profiles; do not rename them T03 or use their 256 sampled rules as totalistic evidence.
- Keep an explicit aggregate-to-exhaustive expansion utility only as a verified relation/analyzer. Structural T03 records must reconstruct valuation, aggregate, and sum table without an exponential ordered table.

**Required conformance tests:**

1. For validated `k>=2,r>=1`, derive `q=2r+1`, `M=1+(k-1)q`, and `R=k^M`; pin `R(2,1)=16`, `R(3,1)=2187`, `R(2,2)=64`, and `R(5,1)=1,220,703,125`. Reject booleans, invalid `k/r`, malformed valuations, wrong table lengths, out-of-alphabet outputs, `-1`, and `R`.
2. Prove every sum `0..q(k-1)` reachable for representative `k/r`, and that every permutation of one read multiset gives the same sum/output. Fixed arity, center inclusion, and repeated positions remain inspectable.
3. Use `(0,2,0)` and `(1,0,1)` at `k=3`: both must address sum row `2` despite different histograms. A histogram-keyed implementation must fail this oracle.
4. Round-trip structural tables/codes `0`, `1`, `420`, `777`, `867`, `R-1`, deterministic sampled `k/r` profiles, and a valid `k=8,r=1` code above `2^63-1` through table, tagged decimal string, and JSON-safe records without NumPy/float loss.
5. Pin code 777's least-significant-first outputs as `(0,1,2,1,0,0,1)`. Assert `output(n,s)=floor(n/3^s) mod 3`, source display order is the reverse padded sequence, and color `2` survives execution.
6. Prove code 420 has `U(s)=(-s) mod 3` for `s=0..6`, while remaining a normal structural table plus an additive property claim. No modulo formula may replace arbitrary T03 execution.
7. For `k=2,r=2`, prove code 10 outputs one exactly for sums `1` and `3`. This catches a hard-coded radius-one/seven-row codec.
8. Expand representative aggregate tables to T01/T02 exhaustive tables and compare all local contexts and several exact trajectories. The native T03 record must still serialize as valuation + aggregate + `M` rows, not the expansion.
9. Run code 1 from an all-zero field and prove the entire background evolves; then validate T06 separately as `U(0)=0`, equivalently `code mod k=0`. No seed or finite-support shortcut may assume quiescence.
10. Use binary radius-one code 2 on `[1,0,0]` with explicit fixed exterior: parallel old-snapshot update yields `[1,1,0]`, while left-to-right in-place mutation would yield `[1,1,1]`.
11. Run one structural program with centered, explicit, random, periodic, finite-block-on-constant, and finite-block-on-repeating initial fields and with cycle/segment/causal-window realizations. Program identity stays fixed; run/realization/view identities change.
12. Assert T04 and T05 presets return the same aggregate-rule/spec types as generic T03; T07 reflection is derived from equal-weight sum; outer, histogram, weighted, threshold, dynamic-arity, and continuous profiles are rejected or routed to their own typed constructions.
13. Inspect the resolved spec/executor: no callback, family branch, partial-row fallback, hidden valuation/seed/background/palette, exhaustive-only identity, binary decoder, float mean, fixed-width rule code, or artificial maximum `k/r`.
14. Preserve the full repository suite, T01/T02 asymmetric/nonbinary tests, scalar/batch parity as regression evidence, and finite trace/export round trips without weakening expectations.

**Completion evidence:** all structural/count/codec and independent trajectory oracles pass; equal-sum/different-histogram behavior is pinned; general big codes round-trip losslessly; non-quiescent backgrounds and nonbinary outputs execute; T04/T05 inspect as presets of one ordinary rule/spec; static inspection finds no totalistic/lookup branch, callback, histogram substitution, exhaustive masquerade, binary fallback, or hidden default; existing tests pass unchanged.

## No-Cheating Checks

- No `totalistic`/T03/lookup family branch, second fixed-lattice executor, or new update law.
- No callback reducer, evaluator string, host `sum` object, formula escape hatch, or opaque aggregate metadata.
- No K-color histogram, multiset, set, nonzero count, min/max, gate, or ordered exhaustive table substituted for source numeric-sum identity; `(0,2,0)` and `(1,0,1)` must merge.
- No aggregate-to-exhaustive expansion as the only stored program or as proof that T03 has ordered-context identity.
- No palette, host ordering, incidental rank, or display tone inferred as arithmetic magnitude; valuation is explicit, total, bijective, and versioned.
- No floating average, tolerance, rounding, normalized-by-variable-count mean, dynamic/masked arity, omitted center, or duplicate-offset collapse.
- No reversed sum-digit order: sum zero is least significant/rightmost, leading zeros are complete rows, and codes are range checked.
- No partial sum table, implicit output/center/background default, wildcard, sparse mutation display, raster-decoded rule, or fixed gallery filter.
- No binary `right_shift`/`&1`, float, JSON number, `numpy.int64`, or artificial `k/r` cap used for general program identity or output.
- No hidden seed, boundary, horizon, palette, background-freezing, behavior class, search work, RNG, or accumulator in state/execution.
- No T06 quiescence or T07 symmetry flag fused into validation; no additive formula, outer/semi-totalistic center channel, unequal weight, threshold, higher-dimensional, or T44 continuous rule smuggled behind an aggregate option.
- No proof from pixels, symmetric examples, rule zero, scalar/batch self-parity, or T01/T02 exhaustive expansion alone; independent sum/code/nonbinary/background/old-snapshot oracles are mandatory.
- No weakening current tests, retaining parallel semantic paths, or relabeling Dyadrads/Dyadaxes/Lagcounts as T03.

## Completion Requirements

- [ ] Every strict/Notes/split/actual-Index/alias/variant/application/emulation textual candidate is dispositioned reproducibly.
- [ ] Every relevant asset and source-permitted oracle is closed with hashes, geometry, repairs, and exclusions.
- [ ] Aggregate/value/case/table/code/read/update/successor/boundary/seed semantics and variants are explicit.
- [ ] T01/T02/T04/T05/T06/T07/additive/weighted/emulation boundaries and current API/runtime fit are proved.
- [ ] Goal 2 files/dependencies/tests and no-cheating gates are implementation-ready.
- [ ] Global ledgers, independent review, diff checks, and repository tests are integrated.

## Stage Results

In progress. Direct evidence currently supports aggregate-plus-table parameterization, but the general value/case/code semantics and complete variant boundary are not yet closed.

## Integration Results

In progress. No prior decision is changed until the complete evidence audit determines whether D114's aggregate responsibility is sufficient.
