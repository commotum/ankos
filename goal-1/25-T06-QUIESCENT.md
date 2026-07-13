# 25-T06-QUIESCENT

Status: **IN PROGRESS — ARCHITECTURE AUDIT COMPLETE**

The architecture prerequisite is complete and its dependent handoffs are reintegrated. T06 resumes through the common SimpleProgram runner and CA-preset axes; T03/T04's bounded asset repairs remain independently active.

## Current Facts

- Exact catalog row: T06, CSV line 7, `Quiescent-Background-Preserving Cellular Automata`; taxonomy section 6 at `ref/notes/CA-Types.md:145-158` is search vocabulary only, not book evidence.
- The taxonomy hypothesis calls this a construction filter: a designated blank value must reproduce itself from the uniform blank local context. For canonical elementary and totalistic codes this suggests the least-significant output digit is zero, but the full source, variant, and representation audit is not yet closed.
- Inherited direct candidates include the three-color gallery exclusion at `BOOK:784`, the historical 32-rule intersection at `BOOK:1346`, the all-white-state gallery statement at `BOOK:2798`, the two-dimensional relation at `BOOK:2926`, the invariant-uniform-state discussion at `BOOK:4070`, and the literal quiescent-symmetric emulation relation at `BOOK:18770`. These are leads, not an exhaustive T06 evidence claim.
- T01/T02/T03 already establish immutable complete local rules, fixed ordered support, old-snapshot reads, typed same-site assignment, atomic parallel update, and uninterrupted deterministic continuation. D114 and D118 reserve quiescent/background-preserving predicates for T06 rather than base-rule flags.
- A uniform blank field being invariant is provisionally a property of `(rule, designated blank)`; a finite nonblank seed, constant exterior, observation crop, stopping-on-fixed-point policy, behavior class, and the outcome word “quiescent” used by other constructions are distinct responsibilities unless direct evidence proves otherwise.
- Current API/runtime and test support for structural rule predicates, designated-background validation, and restriction serialization remain under active audit. Goal 1 changes only `goal-1/`; no runtime, documentation, or test implementation occurs in this stage.

## Updated Assumptions

- Working hypothesis: T06 adds no state, read, result, executor, update, successor, or halt semantic. It validates an existing complete local rule against one explicit uniform-background fixed-point obligation.
- Working hypothesis: the general structural test is `T(b,...,b)=b`. Canonical T01/T02 and T03 code congruences are derived codec accelerators, not the primary meaning and not valid when the blank is not codec rank/value zero.
- Working hypothesis: the designated blank belongs to a restriction/run-background profile, not to the underlying rule's structural identity. Whether a separately identified validated restriction record is needed remains to be settled by evidence and the Goal 2 integration audit.
- The claims above remain revisable under Principle 0 until aliases, captions, Notes, actual Index, splits, assets, current code, tests, and prior decision boundaries close with zero remainder.

## Big Picture Objective

Determine exactly what source evidence means by a blank/white background staying unchanged, reconstruct the smallest generic rule restriction that preserves that distinction across elementary, multicolor, totalistic, and related CA profiles, and produce an implementation-ready Goal 2 validation/property handoff without freezing a boundary, seed, trace, or executor.

## Catalog Identity

- Stable ID: T06.
- Exact CSV name: `Quiescent-Background-Preserving Cellular Automata`.
- Taxonomy section: 6, vocabulary seed only.
- Provisional entry kind: restriction/property over a complete local CA rule plus a designated blank value; not a distinct transition construction.
- Initial vocabulary: quiescent/quiescence, blank/white/all-white/uniform background, background stays/remains unchanged, rules that change/do not change the background, invariant uniform state, stable zero, finite/localized seed, single black/gray cell, symmetric blank-background searches, and code/table least-significant output conditions.

## Search Log

IN PROGRESS. The exact monolith, split, Notes, Index, cross-reference, and linked-asset manifests will replace this marker after every candidate has a recorded disposition.

## Book Excerpts

IN PROGRESS. Excerpt groups will be added only after provenance, exact fragments, and split mirrors are mechanically verified.

## Construction Model

### Native restriction semantics

| Dimension | Reconstructed T06 meaning |
|---|---|
| Entry kind | A decidable local property of `(resolved deterministic local program, explicitly designated blank b)` and a catalog restriction that accepts only programs satisfying it. It is not a transition construction. |
| State | The ordinary CA total field from the referenced program. T06 adds no cell field, control, cache, active set, or background mask. |
| Support/topology | Whatever fixed regular support and realization the referenced CA already declares. The predicate itself is dimension- and boundary-independent. |
| Values | `b` must be one typed member of the referenced program's alphabet. “White”, zero, first rank, seed fill, and palette tone are not implicit synonyms. |
| Read witness | Construct the program's complete fixed-arity local read with every slot equal to `b`, preserving component structure, offset multiplicity, center inclusion, and declared arity. |
| Rule obligation | Evaluate through the same closed structural evaluator used by execution and require `rule(b,...,b)=b`. A property witness records the program reference, predicate version, typed blank, exact uniform input, actual output, and Boolean result. |
| Result/update | None added. A passing program still emits its ordinary typed assignments and uses its existing atomic update. A failing rule is rejected by the catalog restriction; its table is never patched. |
| Successor/halt | Every requested event remains an ordinary deterministic successor, including an unchanged all-blank successor. T06 does not introduce fixed-point stopping or the event-free `Quiescent` outcome used by unrelated constructions. |
| Seed/background | A finite nonblank seed on fill `b` is T08/run data. A constant exterior value is a finite-realization boundary choice. Neither proves or defines the local property. |
| Consequence | With a finite-radius stencil and a passing rule, a finite set of nonblank initial sites has finite causal dilation after every finite horizon. This does not imply monotonicity, eventual death, finite total activity, or halting. |
| Program identity | The restriction returns the exact referenced structural program, semantic hash, and typed axis/preset schemas unchanged. The restriction request and reproducible property evidence have separate identities. |
| Observers/relations | Gallery membership, symmetry, invariant-state classifications, emulation graphs, behavior classes, death/growth claims, crops, rasters, and horizons remain property/analyzer/relation/view records. |

### Structural forms and codec corollaries

For any fixed-arity ordered rule `T:A^q->A`, the authoritative test is

```text
QuiescentBackground(T,b)  iff  T(b,...,b)=b.
```

For a radius-one exhaustive table over ordered rank map `rho:A->{0,...,k-1}`, let `beta=rho(b)`. The uniform-blank row has positional index

```text
i_b = beta*k^2 + beta*k + beta = beta*(k^2+k+1).
```

If a Wolfram code `n` stores row `i` as its base-`k` digit `i`, the derived test is `floor(n/k^i_b) mod k = beta`. Only the canonical rank-zero blank reduces to `n mod k=0`. Thus exactly 128 of 256 elementary rules preserve zero; for a fixed blank in the general nearest-neighbor `k`-color space, exactly `k^(k^3-1)` of `k^(k^3)` tables pass.

For T03 with arity `q=2r+1`, valuation `nu`, and sum table `U`, the general test is

```text
U(q*nu(b)) = b.
```

The strict zero-background profile chooses `b=nu^-1(0)`, so it becomes `U(0)=b`, and the canonical totalistic codec again gives `n mod k=0`. Exactly `k^(M-1)` of `k^M` totalistic tables pass for that fixed zero background, where `M=1+(k-1)q`. This yields 729 T04 rules, 262,144 four-color T05 rules, and 244,140,625 five-color T05 rules. The page-76 50 codes and page-256 32 codes are selected passing galleries, not complete T06 catalogs.

### Boundary and invariant distinctions

- A passing rule plus a nonblank fixed exterior can change edge cells because edge reads are not uniform `b`; this does not falsify the rule property.
- A failing rule plus fixed exterior `b` still changes an interior all-blank region; the boundary cannot repair it.
- `b` being a fixed point of the uniform local rule is weaker than “the only invariant configurations are uniform”, convergence to a uniform state, eventual death, or stability under perturbations.
- A repeating nonuniform background may be preserved by a space-time phase relation without satisfying the T06 uniform-blank predicate. Rule 110's periodic background is an explicit counter-boundary.
- T07 reflection and T06 quiescence compose as independent evidence. There are 64 reflection-symmetric ECAs, 128 zero-quiescent ECAs, and exactly the source's 32-rule intersection.

### Dependency-free semantic oracle

This oracle proves the structural predicate, all canonical code corollaries, arbitrary-blank failure of modulus shortcuts, exact ECA/T07 intersection, T03/T04/T05 counts, source gallery label sets, boundary separation, finite causal dilation, and identity-preserving restriction behavior.

```bash
python3 - <<'PY'
from itertools import product

def digits(n,k,m): return tuple((n//(k**i))%k for i in range(m))
def encode(ds,k): return sum(v*k**i for i,v in enumerate(ds))
def idx(ctx,k):
    out=0
    for v in ctx: out=out*k+v
    return out

def exhaustive_quiescent(table,k,b,arity=3):
    return table[idx((b,)*arity,k)]==b

def totalistic_quiescent(table,valuation,b,q):
    return table[q*valuation[b]]==b

def symmetric_eca(n):
    d=digits(n,2,8)
    return all(d[idx((l,c,r),2)]==d[idx((r,c,l),2)]
               for l,c,r in product(range(2),repeat=3))

eca_q=[n for n in range(256)
       if exhaustive_quiescent(digits(n,2,8),2,0)]
eca_s=[n for n in range(256) if symmetric_eca(n)]
eca_qs=sorted(set(eca_q)&set(eca_s))
labels=(0,4,18,22,32,36,50,54,72,76,90,94,104,108,122,126,
        128,132,146,150,160,164,178,182,200,204,218,222,232,236,250,254)
assert len(eca_q)==128 and eca_q==list(range(0,256,2))
assert len(eca_s)==64 and len(eca_qs)==32 and tuple(eca_qs)==labels

k=3; beta=1; ib=beta*(k*k+k+1)
assert ib==13
zero=digits(0,k,k**3)
assert 0%k==0 and not exhaustive_quiescent(zero,k,beta)
custom=list(zero); custom[ib]=beta; custom[26]=2
custom=tuple(custom); code=encode(custom,k)
assert exhaustive_quiescent(custom,k,beta)
assert (code//k**ib)%k==beta and code%k==0
assert k**(k**3-1)==3**26

for k in (2,3,4,5,8):
    q=3; M=1+(k-1)*q
    assert k**(M-1)*k==k**M
assert 3**6==729 and 4**9==262144 and 5**12==244140625

def total_table(n,k,q=3): return digits(n,k,1+(k-1)*q)
for k,n in ((3,777),(3,420),(3,867),(4,1004600),(2,20)):
    q=5 if (k,n)==(2,20) else 3
    t=total_table(n,k,q)
    assert totalistic_quiescent(t,{i:i for i in range(k)},0,q)
assert not totalistic_quiescent(total_table(1,3),{0:0,1:1,2:2},0,3)

page76=tuple(range(993,1141,3))
page256=tuple(range(1000816,1000941,4))
page262=tuple(range(2,62,2))
assert len(page76)==50 and all(n%3==0 for n in page76)
assert len(page256)==32 and all(n%4==0 for n in page256)
assert len(page262)==30 and all(n%2==0 for n in page262)
assert set(page262)==set(range(0,64,2))-{0,62}

def eca_step(row,n,left=0,right=0):
    d=digits(n,2,8); ext=(left,*row,right)
    return tuple(d[idx(ext[i:i+3],2)] for i in range(len(row)))
assert eca_step((0,0,0),30)==(0,0,0)
assert eca_step((0,0,0),1)==(1,1,1)
assert eca_step((0,0,0),30,left=1,right=1)==(1,0,1)

row=(0,)*10+(1,)+(0,)*10
for h in range(1,6):
    row=eca_step(row,30)
    assert not any(row[:10-h]) and not any(row[11+h:])

program={'kind':'eca','code':30,'table':digits(30,2,8)}
def require(program,b):
    if not exhaustive_quiescent(program['table'],2,b): raise ValueError
    return program
assert require(program,0) is program
print('T06 semantic oracle: PASS')
print('eca=',len(eca_q),len(eca_s),len(eca_qs),'labels=',eca_qs)
print('counts=',3**26,3**6,4**9,5**12,'nonzero_blank_index=',ib)
print('galleries=',len(page76),len(page256),len(page262),
      'boundary_adversary=',eca_step((0,0,0),30,left=1,right=1))
PY
```

Recorded output:

```text
T06 semantic oracle: PASS
eca= 128 64 32 labels= [0, 4, 18, 22, 32, 36, 50, 54, 72, 76, 90, 94, 104, 108, 122, 126, 128, 132, 146, 150, 160, 164, 178, 182, 200, 204, 218, 222, 232, 236, 250, 254]
counts= 2541865828329 729 262144 244140625 nonzero_blank_index= 13
galleries= 50 32 30 boundary_adversary= (1, 0, 1)
```

## Current API Fit

| Current documented component | Fit | T06 consequence |
|---|---|---|
| Separate `ALPHABET`, `SEED`, `BOUNDARY`, and `RULE` fields | DIRECT responsibility split | The schema already prevents seed fill and exterior policy from being rule-table fields (`simple_programs.md:26-38`). Goal 2 must preserve that split while separating program identity from a run record. |
| Finite binary/K-color/symbolic alphabets | DIRECT value carrier / PRINCIPLED EXTENSION | `A` can contain the blank, but the schema has no typed designated-blank reference or membership-bound property witness (`simple_programs.md:200-230`). |
| Seed support, assignment, and `a_init` fill | DIRECT run data / NOT APPLICABLE to predicate | Correctly supplies point/finite/random initial fields; `a_init` must never be inferred as the T06 blank or used as certification (`simple_programs.md:235-292`). |
| Fixed/periodic/reflective boundary and `a_bdry` | DIRECT realization data / NOT APPLICABLE to predicate | Correctly controls exterior reads. A fixed value equal to `b` can realize a blank exterior but cannot make a failing rule pass (`simple_programs.md:292-348,697-701`). |
| One-snapshot parallel rule/update | DIRECT shared semantics | Uniform input is evaluated through the ordinary rule; passing T06 changes no event or commit (`simple_programs.md:101-106,1767-1791,2124-2152`). |
| `EXHAUSTIVE` complete ordered table | PARAMETERIZATION | Its total `T` has the correct structural row, but the document has no rule-property/check layer and no structural program reference (`simple_programs.md:1795-1831`). |
| Broad `TOTALISTIC` aggregate/table | SEMANTIC MISMATCH for exact T03, reusable evaluator shape | Count, histogram, and numeric sum are conflated, so T06 must consume the synthesis-corrected typed T03 program rather than special-case this broad bucket (`simple_programs.md:1964-2032`). |
| Rule restriction/property evidence | PRINCIPLED EXTENSION | Add one recomputable, versioned, program-bound property record. Do not add `QUIESCENT` to `RULETYPE` or the executor. |
| Complete generator object includes seed/boundary | SEMANTIC MISMATCH as program identity | Useful as a run configuration, but a T06 claim must bind only the structural program and blank, while seed/boundary/horizon vary independently (`simple_programs.md:2156-2211`). |

## Current Runtime Fit

| Runtime surface | Fit | Evidence and consequence |
|---|---|---|
| `alphabets.Alphabet`, integer/Boolean/symbolic constructors | DIRECT carrier, incomplete program wiring | Ordered values exist and the module explicitly refuses to make blank/quiescent roles alphabet families (`src/ca/alphabets.py:25-29,43-56,59-86,129-176`). T06 still needs an explicit member reference. |
| `seeds.Seed` support/value/fill separation | DIRECT run responsibility | Fill defaults to zero but remains seed data, never a property proof (`src/ca/seeds.py:1-18,39-55,260-313`). |
| Radius-one ordered neighborhood | DIRECT geometry | The existing selector can describe left/self/right, but current rule objects do not expose a generic structural evaluator (`src/ca/neighborhoods.py:551-569`). |
| `rules.Rule` family/ID/callable metadata | SEMANTIC MISMATCH | No inspectable alphabet, complete structural table, typed input/case schema, or stable program reference exists; opaque callbacks cannot be certified (`src/ca/rules.py:30-33,64-78`). |
| `rules.exhaustive` / `totalistic` / `lookup` | PARAMETERIZATION / SEMANTIC MISMATCH | Shapes suggest reusable evaluation, but arity/table/valuation are incomplete, totalistic meanings are conflated, and final lookup is binary-code oriented (`src/ca/rules.py:173-217,262-280`). |
| `specs.Dynamics` | PARAMETERIZATION | Rule and boundary are separate and episode inputs are excluded, but alphabet/program reference/property evidence is absent (`src/ca/specs.py:23-55`). |
| Spec parsing and rollout | SEMANTIC MISMATCH | Both dispatch on family strings; spatial lookup uses binary shifts/`&1`, and batch IDs coerce to `numpy.int64`. No T06 branch may patch these gaps (`src/ca/specs.py:117-144`; `src/ca/rollout.py:145-212,264-288,292-331,643-682`). |
| Boundary normalization | DIRECT run mechanism with dangerous incidental default | Omitted fixed-boundary values become zero; that convenience must not designate the T06 blank (`src/ca/specs.py:227-247`). |
| Current rollout tests | NOT SUFFICIENT | Rule-zero extinction under fixed zero and scalar/batch parity do not test a nonzero passing rule, a failing rule, arbitrary blank, structural evidence, identity preservation, or boundary separation (`tests/test_rollout.py:263-424`). |

Repository-wide search finds no implemented quiescent-background restriction API. These are expected Goal 2 gaps and do not reopen T01-T05.

## Principles Audit

- **Principles 0 and 1:** the catalog label does not create a construction. Direct evidence treats unchanged backgrounds as a subset/filter over otherwise ordinary rules, validating the initial grouping.
- **Principles 2-4:** one local evaluator and the existing typed assignment/update path remain authoritative. A property checker invokes that evaluator once on a constructed witness; it does not become a rule result or executor path.
- **Principles 5 and 7:** no hidden “background active” bit or sparse work mask enters state. Finite causal dilation is a theorem from locality plus the predicate, not fake finite support or permission to skip blank assignments.
- **Principles 8 and 12:** codec congruences, labels, galleries, rasters, crops, padding, and batch IDs are representations/observers. Structural rule application is primary.
- **Principles 9 and 10:** the predicate genuinely couples one resolved program with one typed blank. Seed, boundary, horizon, palette, and fixed-point stopping remain independent. The catalog resolver validates and returns the ordinary program.
- **Principle 11:** evaluating the uniform local witness defines the decidable property. Search enumeration and gallery rendering are incidental; ordinary synchronous update remains defining CA semantics.
- **Principles 13 and 15:** adversaries include rule 30 versus rule 1, nonzero symbolic blank, noncanonical valuation, nonblank exterior, 128/64/32 ECA counts, T04/T05 counts, source label corpora, identity preservation, and continued all-blank events.
- **Principle 16:** one versioned `RulePropertyEvidence` boundary is architecture. A trusted Boolean flag, even-code branch, background-freezing optimization, table patch, family switch, or boundary-derived shortcut is a shim.

D111-D118 remain valid. T06 requires one new decision, provisionally D119: uniform-background preservation is a program-bound local property/restriction with explicit blank and reproducible witness; it changes neither structural program identity nor execution. The decision will be activated only after source/asset closure and independent review.

## Detailed Implementation Plan

1. Close an exact text manifest across direct names, aliases, descriptions, captions, Notes, actual Index, splits, code relations, invariant-state material, and unrelated blank/quiescent controls.
2. Follow every relevant source-linked asset in both directions; pin exact file identity and classify direct evidence, relation-only material, and exclusions.
3. Prove structural predicates and counts for elementary, generic ordered-table, and totalistic rules, including nonzero/symbolic blank adversaries and code-congruence limits.
4. Audit current documentation, runtime, tests, D111-D118, completed T01-T05 stages, and T07/T08 plus higher-dimensional boundaries.
5. Write the concrete Goal 2 property/restriction API, serialization, migration, conformance, and no-cheating plan.
6. Run embedded source/evidence/semantic/asset checks, independent review, repository tests, fence/status/coverage/diff gates, then reintegrate all global ledgers.

## Goal 2 Implementation Stage

IN PROGRESS. The handoff will name concrete files, dependencies, structural validation, source fixtures, adversarial tests, serialization/identity rules, and static checks after evidence closure.

## No-Cheating Checks

- No T06/quiescent family branch, executor, update law, background-freezing rule, implicit default row, sparse table, or fixed-capacity simulation.
- No seed fill, exterior boundary, crop, palette, fixed-point stop, behavior class, or gallery selection used as proof of rule-level background preservation.
- No code parity/modulus used as the primary predicate when alphabet rank, designated blank, valuation, case-schema order, or codec differs.
- No acceptance based on a sampled finite run; the complete local uniform-blank row must be checked structurally.
- No duplicate predicate under elementary, multicolor, totalistic, higher-color, or dimensional family names when one typed rule-application obligation is sufficient.

## Completion Requirements

- [ ] Every direct/alias/caption/Notes/actual-Index/split/cross-reference/invariant/application/control candidate is dispositioned with zero remainder.
- [ ] Every relevant source-linked asset is hash-pinned and classified, with every source-permitted semantic/raster oracle closed.
- [ ] The exact predicate, designated-blank identity, counts/code relations, and rule/seed/background/boundary/halt/property distinctions are proved across supported rule descriptions.
- [ ] Current API/runtime fit and a concrete Goal 2 restriction/conformance stage are implementation-ready.
- [ ] Global ledgers, independent review, embedded checks, coverage/diff gates, and repository tests pass.

## Stage Results

IN PROGRESS. No completion or architecture decision is recorded until all requirements close.

## Integration Results

IN PROGRESS. The ten-question reintegration audit will be answered after evidence and design close.
