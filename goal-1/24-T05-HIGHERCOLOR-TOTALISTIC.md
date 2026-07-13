# 24-T05-HIGHERCOLOR-TOTALISTIC

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T05, CSV line 6, `Higher-Color Totalistic Cellular Automata`; taxonomy section 5 at `ref/notes/CA-Types.md:126-145` is search vocabulary only, not book evidence.
- The taxonomy hypothesis is a radius-one totalistic profile with four, five, or more values. It claims no new support, read, update, successor, or halt semantics beyond T03; the book audit must prove or revise that grouping.
- The strict five-color comparison states 13 sum cases and `5^13 = 1,220,703,125` possible rules, while a separate Notes/application example names a four-color totalistic code `1004600`. These are initial evidence routes, not yet an exhaustive closure.
- If canonical values are `A_k=(0,...,k-1)` with `nu_k(i)=i` and `r=1`, T03 gives arity `q=3`, sum domain `0..3(k-1)`, table length `M=3k-2`, and rule count `R=k^(3k-2)`. The stage must independently verify the color valuation, range, code direction, examples, and whether “higher-color” means exactly `k>=4`.
- T01/T02/T03/T04 already establish fixed ordered support, all-site old-snapshot reads, typed same-site assignment, atomic parallel update, structural table identity, arbitrary-precision tagged code identity, and the preset/restriction/property/run/view boundary. D118 currently predicts that T05 is the higher-color radius-one preset over T03; this is a hypothesis under evidence audit.
- The current API/runtime remains semantically incomplete for this profile: `simple_programs.md` and `src/ca/rules.py` conflate exact numeric sums with counts/histograms; spatial rollout is family-dispatched and binary-decoded; batch rule IDs use `numpy.int64`; no current test executes a four-or-more-color totalistic sum table.
- Goal 1 remains evidence/design only. This stage may edit only `goal-1/` and must not implement a T05 runtime family.

## Updated Assumptions

- Working hypothesis: T05 is a strictly validated catalog preset/range fixing `r=1`, canonical integer alphabet/valuation, and `k>=4`, then resolving to an ordinary generic T03 program with identical structural identity and executor types.
- A finite `k` is required for every concrete program. “Four, five, or more” does not authorize an unbounded or lazily partial table, wildcard rows, implicit defaults, or fake fixed capacity.
- Structural sum-table identity remains primary. The optional numeric code is an arbitrary-precision relation whose digit count grows with `k`; fixed-width integers, floating values, or JSON numbers cannot define identity.
- Alphabet order, exact numeric valuation, palette, and displayed color names remain distinct. Noncanonical valuations belong to generic T03 unless the source proves them part of T05.
- Rule program, seed/background, finite realization, behavior class, property/proof, gallery selection, raster, and application relation remain separate identities.
- No new decision will be added unless exhaustive evidence contradicts D115-D118 or proves a genuinely new semantic responsibility.

## Big Picture Objective

Determine the exact higher-color totalistic parameter domain and evidence bundle, prove whether it is only a strict T03 preset/range, and produce the smallest implementation-ready Goal 2 constructor and conformance plan without a higher-color executor or fixed-width shortcut.

## Catalog Identity

- Stable ID: T05.
- Exact CSV name: `Higher-Color Totalistic Cellular Automata` at `ref/notes/CA-Types.csv:6`.
- Taxonomy section: 5, vocabulary seed only.
- Entry hypothesis: parameter-range preset/profile over T03, presently expected to fix radius one, canonical valuation, and `k>=4`.
- Initial vocabulary: higher-color/higher colour, more colors, four-color/4-color, five-color/5-color, four/five possible colors, `k=4`, `k=5`, `r=1`, 10 cases, 13 cases, `4^10`, `5^13`, `1,048,576`, `1,220,703,125`, code `1004600`, totalistic, average color, assignment of values to colors, rule complexity, dying out/undecidability, class behavior, and related non-totalistic color-count controls.

## Search Log

IN PROGRESS. Direct terms, aliases, formulas, examples, captions, Notes, actual Index, split files, linked assets, and cross-references are being saturated. Every candidate will be placed in one exact manifest with zero remainder.

## Book Excerpts

IN PROGRESS. Unique construction-relevant excerpts will be recorded verbatim with canonical line provenance after the candidate partition is closed.

## Construction Model

### Native semantics

| Dimension | Reconstructed T05 semantics |
|---|---|
| Entry kind | A discoverable parameter-range preset over T03. It fixes canonical finite integer colors, radius one, and `k>=4`; it is not a distinct construction, executor, or update law. |
| State | The ordinary T01/T02/T03 total field over fixed ordered one-dimensional support. No code register, aggregate accumulator, class label, survival flag, or hidden control exists. |
| Alphabet/valuation | For each concrete finite integer `k>=4`, `A_k=(0,...,k-1)` and the exact valuation is `nu_k(i)=i`. A noncanonical alphabet or valuation is an ordinary generic T03 program, not a T05 preset variant. |
| Active loci/read | `AllSites`; each event reads old values at offsets `(-1,0,+1)`, including self exactly once. The arity is exactly three even though the sum is permutation invariant. |
| Aggregate/cases | `s=nu(left)+nu(self)+nu(right)`. Every integer `0..3(k-1)` is reachable, so the complete case domain has `M=3k-2` rows. `s/3` is an exact average label, never a floating computation. |
| Rule | One immutable complete structural table `U:{0,...,3k-3}->A_k`. There is no sparse row, wildcard, default, gate, threshold, histogram, formula callback, or exhaustive-context table hidden behind the preset. |
| Result/update | One typed same-site `Assign(U(s))` per site; T01's old-snapshot atomic parallel fixed-field update applies unchanged. |
| Successor/halting | One deterministic successor always exists, including for unchanged or all-zero fields. “Dies out”, long survival, behavior class, and undecidability are analyzer/query claims, not native halts or executor state. |
| Run/realization/view | Initial field, zero background, finite segment/cycle/causal window, exterior policy, horizon, crop, palette, raster, gallery order, and plotted width/density remain separate run, observer, and view records. |

### Exact table/code invariants

For a concrete `k>=4`, let `M=3k-2`, and let `U_s` be the output for sum `s`.

```text
output(n,s) = floor(n/k^s) mod k
code(U)     = sum_{s=0}^{M-1} U_s k^s
```

- Valid codes are exactly `0..k^M-1`; there are `R=k^M=k^(3k-2)` rules.
- Sum zero is the least-significant digit. A source-style high-sum-to-low-sum digit list is `(U_(M-1),...,U_0)`; leading zero rows remain semantic.
- `k=4` gives `M=10`, `R=4^10=1,048,576`, and code `1004600` decodes low-sum first to `(0,2,3,0,0,1,1,1,3,3)` and high-sum first to `(3,3,1,1,1,0,0,3,2,0)`.
- `k=5` gives `M=13` and `R=5^13=1,220,703,125`, independently matching the strict five-color comparison.
- The parameter range has no semantic maximum. Already `k=8` gives `R=8^22=73,786,976,294,838,206,464`, beyond signed 64-bit. A concrete program still has a finite `k` and a finite complete table; resource limits are explicit realization concerns rather than a fake preset ceiling.
- For `k>10`, table digits may exceed nine, so structural rows and a tagged decimal integer code remain unambiguous while concatenated glyph strings do not.

### Profile and boundary disposition

| Profile | Ownership |
|---|---|
| `k=4,r=1` | T05 profile; includes the strict page-122 comparison, the 32-code class-transition gallery, and code `1004600`. |
| `k=5,r=1` | T05 profile; 13 rows and `5^13` programs, with the strict page-122 eight-code comparison. |
| Any finite `k>=6,r=1` | T05 parameter range justified by “four or more” plus the general finite-`k` T03 formula; no fixed maximum or speculative infinite alphabet is implied. |
| `k=2` or `k=3` | Generic T03 lower profiles; T04 owns the canonical `k=3,r=1` preset. T05 rejects them rather than silently widening its identity. |
| `r>1` | Generic T03, not T05. Changing radius changes arity/table length and cannot enter through a preset override. |
| Noncanonical valuation | Generic T03. Palette order, host ordering, symbolic labels, or an arbitrary numeric assignment cannot silently define T05. |
| Quiescent zero | T06 predicate `U(0)=0`, equivalently `code mod k=0`; it is not implied by T05. The class-transition codes and code `1004600` happen to satisfy it, while other T05 rules need not. |
| Reflection | Derived from the equal-weight symmetric stencil and owned by T07 as a proof/property boundary, not a runtime flag. |
| Initial conditions | T08/run data. The source plates do not turn a displayed point or finite seed strip into preset identity. |
| Behavior/death/undecidability | Analyzer and scoped property records. Code `1004600` continues to have a deterministic successor after a pattern becomes all zero; deciding eventual death is not an executor halt. |

## Current API Fit

| Construction element | Fit | Evidence and consequence |
|---|---|---|
| Finite canonical integer alphabet | DIRECT data shape | The schema separates `ALPHABET` and supports finite integer values (`simple_programs.md:200-230`), but it does not make the exact valuation a rule invariant. The preset must materialize `A_k` and `nu_k`, not infer them from a palette. |
| Fixed one-dimensional state and parallel old-snapshot step | DIRECT with T01 qualification | Current field and next-slice formulas preserve one old snapshot and parallel assignment (`simple_programs.md:87-113,1767-1793`); finite `SHAPE` remains a realization rather than native integer-line identity. |
| Fixed radius-one read | DIRECT/PARAMETERIZATION | Static fixed-arity compact reads are supported (`simple_programs.md:621-647`). T05 must pin `(-1,0,+1)`, center inclusion, current time, and arity three. |
| Broad `TOTALISTIC` category | PARAMETERIZATION / SEMANTIC MISMATCH | The schema has an aggregate-then-table shape (`simple_programs.md:1964-2008`) but treats active counts, numeric sums, and color histograms as sibling examples without typed case domains. T05 requires only the exact numeric sum; a histogram distinguishes contexts that T05 merges. |
| Exact sum image and complete table | PRINCIPLED EXTENSION inherited from G2-T03 | The preset derives `0..3(k-1)` and `M=3k-2`; current documentation has no validated aggregate-case domain, complete-table invariant, structural identity, or row order. |
| Base-`k` arbitrary-precision codec | PRINCIPLED EXTENSION inherited from G2-T03 | Sum zero is least significant, leading zero rows survive, and the structural table is primary. Fixed-width or JSON-number identity fails within T05 at `k=8`. |
| Typed assignment and atomic update | DIRECT T01 reuse | The rule still returns one same-site value, so no T05 result type, executor, or update law is justified. |
| Higher-color catalog preset | PRINCIPLED EXTENSION only at configuration boundary | A strict resolver may expose T05 discoverability if it returns the ordinary generic T03 spec and rejects all semantic overrides. It cannot survive as a rollout family name. |
| Seed/background/boundary/horizon/view | PARAMETERIZATION / NOT APPLICABLE to program | Existing concepts can describe finite runs, but class galleries, death/survival queries, density/width plots, palette, crop, and raster remain downstream. |

## Current Runtime Fit

| Component | Fit | Exact finding |
|---|---|---|
| `alphabets.int_range_alphabet(k,0)` | DIRECT primitive, incomplete wiring | It creates exactly `0..k-1` (`src/ca/alphabets.py:59-86`), but `Dynamics` carries no alphabet/valuation and spatial rollout validates neither seeds nor gathered/output values. |
| `neighborhoods.eca(radius=1)` | DIRECT finite geometry | It produces the ordered current-time left/self/right stencil (`src/ca/neighborhoods.py:551-569`), pinned by `tests/test_neighborhoods.py:86-112`. Native support and causal realization remain outside it. |
| `rules.totalistic(...,"sum")` | PARAMETERIZATION / incomplete rule | It records an aggregate token but no alphabet, valuation, fixed arity, reachable image, `state_count`, complete table, code, or program identity (`src/ca/rules.py:198-217`). |
| `_channel_state` | DIRECT integer-sum kernel only | It sums the gathered integers (`src/ca/rollout.py:742-777`) but ignores the declared sum/count distinction, coerces to `int64`, and checks no value or arity invariant. It is insufficient as the T05 construction. |
| `rules.lookup` / `_lookup_index` | SEMANTIC MISMATCH as implemented | The table helper cannot derive `M` because the channel has no state count, supports only a binary-bit codec, and composes channel indices by bit shifts (`src/ca/rules.py:262-295`; `src/ca/rollout.py:811-822`). |
| Spatial output | SEMANTIC MISMATCH | Both scalar and batch paths return `(rule_id >> index) & 1`, making values `2..k-1` impossible (`src/ca/rollout.py:643-682`). A base-`k` T05 conditional here would be another prohibited family patch. |
| Executor/spec routing | SEMANTIC MISMATCH | Rollout and spec parsing whitelist named Phase 1 families (`src/ca/rollout.py:145-212`; `src/ca/specs.py:117-181`). T05 cannot be added to these switches; G2-T03 must supply the shared typed executor/spec path. |
| Batch/program identity | SEMANTIC MISMATCH for the parameter range | Batch IDs normalize to `numpy.int64` (`src/ca/rollout.py:264-288`), datasets build `int64` ID arrays (`src/ca/datasets.py:319-335`), and raw results expose only numeric rule IDs (`src/ca/specs.py:58-81`). `k=8` already exceeds that identity space. |
| Existing tests | Regression evidence only | Rule tests cover 256-member binary named families (`tests/test_rules.py:9-45`); spatial tests cover binary outputs and scalar/batch parity (`tests/test_rollout.py:263-424`); spec tests cover only Phase 1 names (`tests/test_specs.py:8-116`). No test constructs, serializes, or executes a T05 table. |

Reusable mechanics are the radius-one selector, explicit finite boundaries, finite state arrays, and old-snapshot loop shape. They do not make T05 currently executable. All valuation/table/codec/program-reference and shared executor work belongs to G2-T03; T05 adds strict resolution and conformance only.

## Principles Audit

- **Principles 0, 1, 2, and 10:** the evidence-backed candidate is a strict range preset returning T03. A catalog label, larger alphabet, or large code space does not create an executor.
- **Principles 3-5 and 11:** the fixed read, exact sum/table rule, typed assignment, and atomic old-snapshot update retain one responsibility each. Death, class, density, and undecidability are queries/properties, not effects, halts, or state.
- **Principles 7-9:** every concrete `k` has a naturally finite complete `3k-2`-row table. `k`, canonical valuation, arity, case image, output domain, and codec are genuinely coupled and validate together; seed, realization, and view remain independent.
- **Principles 8 and 12:** structural table and tagged bigint identity must survive serialization. Fixed `int64` batches, palette tones, crop, plots, and flattened traces cannot redefine the program.
- **Principles 13 and 15:** adversaries must include a four-color nonbinary output, equal-sum/different-histogram contexts, in-place-versus-old-snapshot divergence, `k=8` bigint identity, quiescent and nonquiescent rules, preset/generic equality, and exact source code-label sets.
- **Principles 14 and 16:** any higher-color rollout switch, hard maximum `k`, sparse/default table, binary decoder fallback, callback aggregate, or T05-only bigint path is a hard-stop architecture failure.

D115-D118 currently suffice: the construction is the same equal-weight sum quotient and complete structural table over the same assignment executor. Completion should sharpen D118 with the exact `k>=4,r=1,A_k,nu_k` preset boundary, but should add no D119 unless the remaining source/asset audit contradicts this model.

## Exact Semantic Oracle

This dependency-free oracle pins the preset domain, table/cardinality/code invariants, page-label sets, code `1004600`, nonbinary sum semantics, T06 separation, old-snapshot update, preset/generic identity, invalid inputs, and arbitrary-precision pressure. It intentionally does not manufacture trajectories from source plates whose finite seed digits, crop, or palette are not fully serialized.

```bash
python3 - <<'PY'
from itertools import permutations, product

def check_k(k):
    if isinstance(k,bool) or not isinstance(k,int) or k<4:
        raise ValueError(k)
    return k

def cases(k):
    check_k(k)
    return 3*k-2

def rule_count(k):
    return k**cases(k)

def decode(code,k):
    check_k(k)
    if isinstance(code,bool) or not isinstance(code,int) or not 0<=code<rule_count(k):
        raise ValueError(code)
    return tuple(code//(k**s)%k for s in range(cases(k)))

def encode(table,k):
    check_k(k)
    table=tuple(table)
    if len(table)!=cases(k):
        raise ValueError(table)
    if any(isinstance(v,bool) or not isinstance(v,int) or not 0<=v<k for v in table):
        raise ValueError(table)
    return sum(v*k**s for s,v in enumerate(table))

def generic(k,table):
    table=tuple(table); encode(table,k)
    return ('aggregate_lookup',tuple(range(k)),tuple(range(k)),3,table)

def preset(k,table):
    check_k(k)
    return generic(k,table)

def ring_step(table,state):
    n=len(state)
    return tuple(table[state[(i-1)%n]+state[i]+state[(i+1)%n]] for i in range(n))

def in_place(table,state):
    out=list(state); n=len(out)
    for i in range(n):
        out[i]=table[out[(i-1)%n]+out[i]+out[(i+1)%n]]
    return tuple(out)

assert [(k,cases(k),rule_count(k)) for k in (4,5,8)]==[
    (4,10,1048576),(5,13,1220703125),(8,22,73786976294838206464)]
for k in (4,5,8,11):
    assert decode(0,k)==(0,)*cases(k)
    assert decode(rule_count(k)-1,k)==(k-1,)*cases(k)

table1004600=(0,2,3,0,0,1,1,1,3,3)
assert decode(1004600,4)==table1004600
assert encode(table1004600,4)==1004600
assert tuple(reversed(table1004600))==(3,3,1,1,1,0,0,3,2,0)
assert preset(4,table1004600)==generic(4,table1004600)

page122_k4=tuple(range(107395,107403))
page122_k5=tuple(range(180197741,180197749))
page256_k4=tuple(range(1000816,1000941,4))
assert (len(page122_k4),len(page122_k5),len(page256_k4))==(8,8,32)
for code in page122_k4+page256_k4: decode(code,4)
for code in page122_k5: decode(code,5)

# T06 is a predicate over T05 programs, not a base validator.
assert all(code%4==0 for code in page256_k4)
assert 1004600%4==0 and decode(1004600,4)[0]==0
assert len(page256_k4)<rule_count(4)//4==262144
assert decode(1,4)[0]==1
assert ring_step(decode(1,4),(0,0,0))==(1,1,1)
assert ring_step(table1004600,(0,0,0))==(0,0,0)

# Exact numeric sum merges different histograms and all permutations.
assert table1004600[sum((0,2,0))]==table1004600[sum((1,0,1))]==3
for p in set(permutations((0,1,2))):
    assert table1004600[sum(p)]==table1004600[3]

# Parallel old-snapshot assignment is defining, not an in-place scan.
assert ring_step(table1004600,(0,0,1))==(2,2,2)
assert in_place(table1004600,(0,0,1))==(2,0,0)

# Aggregate identity is not a hidden 64-row exhaustive table.
lowered=tuple(table1004600[sum(q)] for q in product(range(4),repeat=3))
assert len(table1004600)==10 and len(lowered)==64
assert lowered[(0*4+2)*4+0]==lowered[(1*4+0)*4+1]==3

# The preset range has no signed-int64 ceiling or single-glyph row encoding.
int64_max=2**63-1
assert rule_count(8)>int64_max
tagged={'kind':'nonnegative_integer','decimal':str(rule_count(8)-1)}
assert int(tagged['decimal'])==rule_count(8)-1
k11=(0,)*10+(10,)+(0,)*(cases(11)-11)
assert decode(encode(k11,11),11)==k11 and 10 in k11

bad=[
    lambda: preset(True,(0,)*10),
    lambda: preset(3,(0,)*7),
    lambda: preset(4.0,(0,)*10),
    lambda: decode(True,4),
    lambda: decode(-1,4),
    lambda: decode(rule_count(4),4),
    lambda: encode((0,)*9,4),
    lambda: encode((0,)*9+(4,),4),
    lambda: encode((0,)*9+(True,),4),
]
for f in bad:
    try: f()
    except (TypeError,ValueError): pass
    else: raise AssertionError(f)

print('T05 semantic oracle: PASS')
print('counts=',[(k,cases(k),rule_count(k)) for k in (4,5,8)])
print('code1004600_table=',table1004600,
      'display=',tuple(reversed(table1004600)))
print('page122_labels=',len(page122_k4),len(page122_k5),
      'page256_labels=',len(page256_k4),'quiescent_k4=',rule_count(4)//4)
print('old_snapshot=',ring_step(table1004600,(0,0,1)),
      'in_place_rejected=',in_place(table1004600,(0,0,1)))
PY
```

Recorded output:

```text
T05 semantic oracle: PASS
counts= [(4, 10, 1048576), (5, 13, 1220703125), (8, 22, 73786976294838206464)]
code1004600_table= (0, 2, 3, 0, 0, 1, 1, 1, 3, 3) display= (3, 3, 1, 1, 1, 0, 0, 3, 2, 0)
page122_labels= 8 8 page256_labels= 32 quiescent_k4= 262144
old_snapshot= (2, 2, 2) in_place_rejected= (2, 0, 0)
```

## Detailed Implementation Plan

1. Close an exact source query manifest across strict text, captions, Notes, actual Index, splits, aliases, named codes, formulas, applications, and neighboring non-totalistic controls.
2. Close a bidirectional linked-asset manifest with exact file identity, dimensions, hashes, caption/provenance roles, inclusion status, and source-permitted semantic or raster checks.
3. Reconstruct the precise `k`/radius/value/sum/table/code state and prove all finite validation/count boundaries with adversarial examples.
4. Re-audit current documentation, runtime, tests, prior decisions, and T03/T04/T06/T07/T08 boundaries.
5. Write the concrete Goal 2 constructor, migration, conformance, rejection, and no-cheating plan.
6. Run embedded evidence/semantic/asset checks, independent review, repository tests, coverage/fence/diff gates, then reintegrate all global ledgers.

## Goal 2 Implementation Stage

### G2-T05 — Strict higher-color radius-one range preset over G2-T03

**Objective:** make T05 discoverable through `higher_color_totalistic(k, code_or_table)` for concrete integer `k>=4`, while resolving to exactly the generic T03 program `totalistic(k=k,r=1,valuation={i:i},...)`. Add no state, aggregate, table, codec, result, update, executor, trace, analyzer, or view path.

**Dependencies:** completed G2-T01 fixed support/`AllSites`/typed assignment/atomic update/realization/trace contracts; G2-T02 finite alphabet/table and stable references; all G2-T03 valuation, `EqualWeightIntegerSum`, aggregate-case table, totalistic codec, generic rule, executor, spec serialization, and arbitrary-precision work. G2-T05 is sequenced after G2-T03 and may be delivered beside G2-T04, but neither preset may implement a fallback for missing generic infrastructure.

**Concrete files and API:**

1. Extend the G2-T03 `src/ca/presets/totalistic.py` with `higher_color_totalistic(k, code_or_table)`. Reject booleans/nonintegers and `k<4`; construct immutable `A_k=(0,...,k-1)`, identity valuation, and `r=1`; then delegate exactly once to generic T03. Accept no radius, valuation, alphabet, aggregate, executor, update, seed, boundary, filter, class, or view override.
2. Export the resolver through `src/ca/presets/__init__.py`, `src/ca/__init__.py`, and the synthesis-selected catalog registry. The preset name and T05 ID may survive only as nonsemantic provenance; resolved rule/runtime classes, structural serialization, program reference, and semantic hash must equal generic T03.
3. Extend `src/ca/specs.py` only at the pre-resolution configuration boundary. A JSON-safe request must use a discriminated table record or tagged nonnegative-decimal code; reject unknown/conflicting fields. The resolved record contains explicit `k`, valuation, arity three, `3k-2` structural rows, and optional codec relation—not a `family="higher_color_totalistic"` dispatch token.
4. Make no T05-specific changes to alphabets, aggregates, rule tables, rules, executor/rollout, updates/effects, datasets, export, or visualization. Those modules change only for shared G2-T03. Static inspection must find no T05, higher-color, `k>=4`, four-color, five-color, or code-`1004600` execution branch.
5. Update `simple_programs.md` to document T05 under strict presets and show its resolved T03 form. Split numeric sum from histogram/count summaries, preserve complete case-domain and bigint-code requirements, and keep run/query/view records outside the preset.
6. Add transparent source fixtures under `tests/fixtures/t05_higher_color_totalistic.json` and conformance in `tests/test_t05_higher_color_totalistic.py`, reusing generic G2-T03 executor/codec tests rather than copying implementation. Asset hashes/labels and long-run claims belong only in reference fixtures/tests.

**Required fixtures and tests:**

1. Pin `(k,M,R)=(4,10,1048576)`, `(5,13,1220703125)`, and `(8,22,73786976294838206464)`. Assert code endpoints, complete-table lengths, arbitrary-precision tagged round trips, leading zero rows, and unambiguous multi-integer rows for `k>10`.
2. Pin page-122 code sets `107395..107402` for `k=4` and `180197741..180197748` for `k=5`; pin the page-256 set `range(1000816,1000941,4)`; validate every label against its exact domain without treating gallery order as program semantics.
3. Pin code `1004600 -> (0,2,3,0,0,1,1,1,3,3)` low-sum first and the reverse source display. Round-trip it through table, tagged code, preset, generic T03, single execution, and batch execution with the same structural program reference and runtime types.
4. Reject `k=True`, nonintegers, `k=2/3`, code `-1`/`k^(3k-2)`, short/long/sparse tables, out-of-alphabet rows, both/neither code-table inputs, and all semantic override fields. Generic T03 remains available for lower `k`, other radii, and noncanonical valuations without being relabeled T05.
5. For code `1004600`, assert `(0,2,0)` and `(1,0,1)` both select sum row two and output `3`; reverse/permutate contexts without a symmetry flag. On a periodic three-cell field `(0,0,1)`, assert the old-snapshot successor `(2,2,2)` and reject the left-to-right in-place result `(2,0,0)`.
6. Prove T06 remains separate: all 32 page-256 codes and code `1004600` satisfy `code mod 4=0`, but code `1` evolves an all-zero field and is still a valid T05 rule. Prove “dies out” leaves a continuing all-zero fixed evolution rather than emitting a T05 halt.
7. Vary seed, finite realization/boundary, horizon, property/class records, gallery selection, density/width observations, and palette/view while holding one program fixed; its structural identity and raw semantics must not change. Do not turn the source's under-specified seed strips or plots into invented trajectory goldens.
8. Static-scan the resolved objects and sources for a T05 family, duplicate sum/table/codec, binary decoder, `int64` identity, hard maximum `k`, sparse/default rows, exhaustive-table masquerade, callback, or preset-specific scalar/batch path. Preserve all generic T03 and T04 conformance plus the existing repository suite.

**Completion evidence:** every valid preset resolves structurally and behaviorally to generic T03; exact count/code/table/source-label fixtures and rejections pass; arbitrary precision survives scalar/batch/serialization boundaries; run/property/view identities remain separate; static checks find no branch or duplicate semantics; focused and full tests pass.

## No-Cheating Checks

- No `higher_color`, `k>=4`, four-color, five-color, or code-`1004600` runtime branch, family dispatch, duplicate executor, or update law.
- No finite-capacity ceiling, sparse/partial table, wildcard/default row, opaque exhaustive-table substitution, fixed-width/float/JSON-number rule identity, or binary shift decoder.
- No palette-derived valuation, implicit alphabet ordering, histogram/nonzero-count substitute, tolerant average, callback escape, or global formula bypass.
- No seed, blank/quiescent condition, application outcome, dying-out predicate, behavior label, crop, horizon, raster, or view data fused into program identity.
- The preset and corresponding generic T03 program must resolve to identical structural identity and executor types; invalid `k`, radius, valuation, table, and code inputs must fail visibly.

## Completion Requirements

- [ ] Every direct/alias/formula/code/caption/Notes/actual-Index/split/cross-reference/application/control candidate is dispositioned with zero remainder.
- [ ] Every relevant source-linked asset is hash-pinned and classified, with every source-permitted semantic/raster oracle closed.
- [ ] The exact higher-color parameter domain, table/cardinality/code rules, canonical fixtures, and T03/T04/T06/T07/T08 boundaries are proved.
- [ ] Current API/runtime fit and a concrete Goal 2 preset/conformance stage are implementation-ready.
- [ ] Global ledgers, independent review, embedded checks, coverage/diff gates, and repository tests pass.

## Stage Results

IN PROGRESS. No completion or new architecture claim is made until all requirements close.

## Integration Results

IN PROGRESS. The ten-question reintegration audit will be answered after the evidence and design close.
