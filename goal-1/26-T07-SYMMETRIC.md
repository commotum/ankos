# 26-T07-SYMMETRIC

Status: **IN PROGRESS — EVIDENCE CLOSED; DESIGN AND INTEGRATION ACTIVE**

## Current Facts

- Exact catalog row: T07, CSV line 8, `Left-Right Symmetric Cellular Automata`; taxonomy section 7 at `ref/notes/CA-Types.md:160-176` is search vocabulary only, not book evidence.
- T07 is a validated property/restriction over an ordinary resolved CA program. Reflection of an asymmetric rule is a generic table transform/relation, and a compact orbit table is a lossless representation of a passing rule. None is a new executor or top-level state class.
- For the catalog's ordinary scalar colors and a centered one-dimensional stencil, the authoritative predicate is `T(v)=T(reverse(v))` for every complete local read `v`. The reflected table is `T^R(v)=T(reverse(v))`.
- A rule fixed by reflection, a reflected pair of rules, the 160 reflection-only ECA rule orbits, the source's 88 combined reflection/color-conjugacy orbits, a symmetric seed, and a symmetric observed pattern are distinct facts.
- T01/T02 supply the arbitrary finite ordered rule table. T03/T04/T05 supply a structural proof because an equal-weight sum over a reflection-closed stencil is invariant under reversal. T06 is an independent property whose intersection with T07 contains 32 ECAs.
- D114 and D118 reserve reflection/symmetry predicates or transforms for T07. D119's generic property boundary is reusable: invalid claims, `UnsupportedProperty`, `DoesNotHold`, and `Holds` stay distinct, and a passing selection resolves to the exact unchanged program.
- `simple_programs.md:1833-1863` proposes `ISOTROPIC`, but its independent per-neighborhood quotients can over-identify reads when one physical reflection must act diagonally on the complete read tuple. It also omits nontrivial output actions. Goal 2 must repair that representation, not create a T07 rollout path.
- Current `src/ca` has no structural reflection checker, transform, or orbit evaluator. Dataset `reflect-x` metadata and `BOUNDARY=REFLECTIVE` are separate observer/realization mechanisms and prove nothing about a rule.
- DOMAIN here means the task/program dimensional support: T07 acts on the spatial coordinate of a `t+1D` CA DOMAIN. ALPHABET remains the label/value schema; neither word denotes a new semantic family.
- Goal 1 changes only `goal-1/`; runtime, root documentation, and tests remain Goal 2 work.

## Big Picture Objective

Determine exactly what left-right symmetry constrains, distinguish local rule invariance from transforms, equivalence classes, seeds, boundaries, and views, and hand Goal 2 the smallest generic property/representation extension compatible with the branch-free SimpleProgram runner:

```text
active = FRONTIER.select(state)
reads  = NEIGHBORHOOD.read(state, active)
writes = RULE(active, reads)
next   = UPDATE.apply(state, active, writes)
```

T07 changes none of those four execution steps.

## Catalog Identity

- Stable ID: T07.
- Exact CSV name: `Left-Right Symmetric Cellular Automata`.
- Taxonomy section: 7, vocabulary seed only.
- Entry kind: class-2 validated property/restriction over an eligible resolved CA program and the canonical nonidentity one-dimensional reflection action.
- Related but separate artifacts: class-2 reflected-program transform/equivalence record and optional class-3 lossless orbit-table rule representation.
- Initial vocabulary: left-right/right-left symmetry, symmetric/asymmetric rules, reflection/reflected/reflective, mirror/mirrored, reversal/reversed, interchange left and right, equivalent/inequivalent rules, conjugate/color interchange, isotropic/rotational invariance, totalistic symmetry, symmetric initial conditions/patterns, and quiescent-symmetric rules.

## Search Log

`BOOK` means `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`. Body plus Notes occupy canonical physical lines `1-20825`, the actual Index is `20826-22457`, and the Colophon begins at `22458`. Ten controlled pre-Index families produce 268 unique lexical lines. Fifteen syntactically governed continuations and 74 actual-Index routes yield the authoritative 357-line text universe.

| Q | Controlled pre-Index family | Hits |
|---:|---|---:|
| 01 | left-right/right-left/interchange-left-right forms | 26 |
| 02 | symmetric/asymmetric near CA, totalistic, neighborhood, rule, or pattern | 50 |
| 03 | reflection near CA, neighborhood, rule, or pattern | 27 |
| 04 | mirror near CA, neighborhood, rule, or pattern | 2 |
| 05 | reverse/reversal near CA, neighborhood, rule, pattern, left, or right | 36 |
| 06 | isotropy/anisotropy/rotation near CA, neighborhood, rule, pattern, or lattice | 15 |
| 07 | totalistic/outer-totalistic | 74 |
| 08 | equivalence/conjugacy/orbit near CA, rule, or neighborhood | 62 |
| 09 | quiescent near symmetric/reflection | 1 |
| 10 | history/search/1981-84 near symmetry or totalistic | 22 |

The disjoint final disposition is `15/167/3/98/74`: direct T07 evidence, relevant CA property/transform/context relations, incidental CA implementation/view controls, sibling SimpleProgram or general alias controls, and actual-Index navigation routes. The 15 governed lines are classified inside those semantic groups; nothing is left in an untyped adjacency bucket.

### Exact canonical source oracle

```bash
python3 - <<'PY'
import re
from pathlib import Path

P=Path('ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md')
L=P.read_text().splitlines(); IX=20826; CO=22458
def ns(s): return set(map(int,s.split(','))) if s else set()

rows=[
('Q01',r'left[- ]right|right[- ]left|left/right|right/left|left and right|right and left|interchang(e|ing).{0,50}(left|right)|(left|right).{0,50}interchang',26),
('Q02',r'(symmetr(y|ies|ic|ical|ically|ize|ized|ization)|asymmetr(y|ies|ic|ical|ically)).{0,180}(cellular autom|totalistic|neighborhood|rule|pattern)|(cellular autom|totalistic|neighborhood|rule|pattern).{0,180}(symmetr(y|ies|ic|ical|ically|ize|ized|ization)|asymmetr(y|ies|ic|ical|ically))',50),
('Q03',r'reflect(ion|ions|ed|ing|ive|s)?.{0,180}(cellular autom|neighborhood|rule|pattern)|(cellular autom|neighborhood|rule|pattern).{0,180}reflect(ion|ions|ed|ing|ive|s)?',27),
('Q04',r'mirror(s|ed|ing)?.{0,180}(cellular autom|neighborhood|rule|pattern)|(cellular autom|neighborhood|rule|pattern).{0,180}mirror(s|ed|ing)?',2),
('Q05',r'(reversal|reverse(d|s|ing)?).{0,180}(cellular autom|neighborhood|rule|pattern|left|right)|(cellular autom|neighborhood|rule|pattern|left|right).{0,180}(reversal|reverse(d|s|ing)?)',36),
('Q06',r'(isotrop(y|ic|ically)|anisotrop(y|ic|ically)|rotational(ly)?|rotation(s|al)?).{0,180}(cellular autom|neighborhood|rule|pattern|lattice)|(cellular autom|neighborhood|rule|pattern|lattice).{0,180}(isotrop(y|ic|ically)|anisotrop(y|ic|ically)|rotational(ly)?|rotation(s|al)?)',15),
('Q07',r'totalistic|outer[- ]totalistic',74),
('Q08',r'(equivalent|inequivalent|equivalence|conjugate|conjugates|orbit|orbits).{0,180}(cellular autom|rule|neighborhood)|(cellular autom|rule|neighborhood).{0,180}(equivalent|inequivalent|equivalence|conjugate|conjugates|orbit|orbits)',62),
('Q09',r'quiescent.{0,180}(symmetric|symmetry|reflection)|(symmetric|symmetry|reflection).{0,180}quiescent',1),
('Q10',r'(history|historical|first|original|search|198[1-4]).{0,220}(left[- ]right|right[- ]left|symmetr|asymmetr|totalistic)|(left[- ]right|right[- ]left|symmetr|asymmetr|totalistic).{0,220}(history|historical|first|original|search|198[1-4])',22),
]
sets=[]
for name,pat,want in rows:
    hit={i for i,s in enumerate(L[:IX-1],1) if re.search(pat,s,re.I)}
    assert len(hit)==want,(name,len(hit),want); sets.append(hit)
union=set().union(*sets); assert len(union)==268

D=ns('490,746,768,784,1346,1348,2798,5064,5066,11585,11636,11637,11897,18770')
I=ns('10930,11875,18782')
N=ns('482,1545,2038,2600,2608,2630,3820,4020,4032,4084,4588,4878,4892,5566,5802,5808,6096,6360,6388,8646,8650,8658,8670,8708,8728,8904,9899,10227,10305,10543,10619,11391,12042,12054,12194,12210,12226,12279,12418,12424,12466,12589,12625,12637,13775,13990,13994,14054,14077,15149,15267,15283,15285,15291,15293,15295,15297,15615,15639,15738,15740,15747,15824,15977,16068,16082,16084,16090,16203,16234,16532,16601,16840,16916,16995,18111,18141,18369,18532,18582,18852,18904,18910,18914,19104,19137,19268,19294,19397,20168,20216,20218,20273,20274,20613')
R=ns('422,772,774,776,790,796,800,804,808,824,834,846,1282,1954,2170,2802,2806,2822,2852,2868,2922,3336,3406,3804,3902,3914,3950,4298,4414,5232,5638,5806,6340,6644,6956,7190,7260,7358,7406,7912,7970,8208,8220,8318,8320,8406,8410,8690,8760,8844,8936,9160,9166,9332,9336,9362,10261,10595,10601,10603,10636,10982,11000,11037,11056,11060,11068,11070,11072,11168,11178,11345,11365,11369,11493,11509,11523,11554,11625,11635,11889,11902,11904,11908,11910,11912,11916,11965,12613,13520,13534,13536,13538,13547,13548,13549,13551,13559,13601,13613,13617,13644,13650,13654,13658,13666,14223,14224,14238,14239,14241,14301,14332,14350,14445,14578,14632,14677,14693,14721,14733,14852,15207,15209,15221,15299,15301,15321,15359,15388,15708,15766,15955,15959,16022,16024,16027,16129,16157,16253,16255,16378,16724,17008,17409,17431,17660,17663,17995,18001,18672,18748,18749,19159,19561,20577')
assert [len(x) for x in (D,R,I,N)]==[14,156,3,95]
assert set().union(D,R,I,N)==union
assert sum(map(len,(D,R,I,N)))==268

index_pat=r'left[- ]right|right[- ]left|symmetr|asymmetr|reflect|mirror|reversal|reverse|isotrop|rotational|totalistic|inequivalent|equivalent rules|rule equivalen|conjugat|orbit|quiescent'
index={i for i,s in enumerate(L,1) if IX<=i<CO and re.search(index_pat,s,re.I)}
expected_index=ns('20828,20836,20846,20868,20900,20914,20918,20940,20946,20965,20967,20969,20972,20980,21038,21046,21050,21054,21074,21080,21086,21088,21090,21114,21130,21172,21185,21189,21193,21213,21233,21243,21253,21298,21338,21393,21450,21454,21471,21513,21521,21525,21614,21658,21731,21735,21763,21783,21819,21877,21893,21927,21933,21990,21992,21994,21998,22016,22028,22030,22070,22114,22132,22134,22136,22146,22148,22150,22323,22352,22378,22392,22394,22434')
assert index==expected_index and len(index)==74

gD=ns('1344')
gR=ns('13540,13542,13544,13545,13546,13554,13555,13556,13561,17997,20579')
gN=ns('16201,16205,16207')
governed=set().union(gD,gR,gN)
assert len(governed)==15 and governed.isdisjoint(union|index)
parts=[D|gD,R|gR,I,N|gN,index]
assert [len(x) for x in parts]==[15,167,3,98,74]
assert sum(map(len,parts))==len(set().union(*parts))==357
assert L[2795]=='![](_page_247_Figure_2.jpeg)'
assert L[5061]=='![](_page_439_Figure_3.jpeg)'
print('T07 source manifest: PASS 10 families; lexical=268; governed=15; index=74; total=357; partition=15,167,3,98,74')
PY
```

Recorded output:

```text
T07 source manifest: PASS 10 families; lexical=268; governed=15; index=74; total=357; partition=15,167,3,98,74
```

The actual Index is navigation-only. Its most useful routes are `BOOK:21130` (elementary equivalences), `21338` (isotropy), `21990` (rotational CA symmetry), `21992` (rule-30 asymmetry), `22070` (rule equivalences), `22146` (totalistic sums), `22150` (one- and two-dimensional symmetry), and `22352` (totalistic CA); none adds transition mechanics.

### Split-corpus and excerpt oracle

The same ten regexes produce 325 physical hits across `CHAPTERS` and `BACK-MATTER`. A mechanical audit finds 313 byte-exact monolith lines and 12 formatting/OCR/line-join variants, each mapped to one canonical line. This corrects an intermediate manual count that had grouped five byte-exact routed lines with the variants. The monolith remains authoritative and no split-only semantic candidate exists.

```bash
python3 - <<'PY'
import re
from pathlib import Path

ROOT=Path('ref/A-New-Kind-of-Science')
M=(ROOT/'A-New-Kind-of-Science.md').read_text().splitlines()
patterns=[
r'left[- ]right|right[- ]left|left/right|right/left|left and right|right and left|interchang(e|ing).{0,50}(left|right)|(left|right).{0,50}interchang',
r'(symmetr(y|ies|ic|ical|ically|ize|ized|ization)|asymmetr(y|ies|ic|ical|ically)).{0,180}(cellular autom|totalistic|neighborhood|rule|pattern)|(cellular autom|totalistic|neighborhood|rule|pattern).{0,180}(symmetr(y|ies|ic|ical|ically|ize|ized|ization)|asymmetr(y|ies|ic|ical|ically))',
r'reflect(ion|ions|ed|ing|ive|s)?.{0,180}(cellular autom|neighborhood|rule|pattern)|(cellular autom|neighborhood|rule|pattern).{0,180}reflect(ion|ions|ed|ing|ive|s)?',
r'mirror(s|ed|ing)?.{0,180}(cellular autom|neighborhood|rule|pattern)|(cellular autom|neighborhood|rule|pattern).{0,180}mirror(s|ed|ing)?',
r'(reversal|reverse(d|s|ing)?).{0,180}(cellular autom|neighborhood|rule|pattern|left|right)|(cellular autom|neighborhood|rule|pattern|left|right).{0,180}(reversal|reverse(d|s|ing)?)',
r'(isotrop(y|ic|ically)|anisotrop(y|ic|ically)|rotational(ly)?|rotation(s|al)?).{0,180}(cellular autom|neighborhood|rule|pattern|lattice)|(cellular autom|neighborhood|rule|pattern|lattice).{0,180}(isotrop(y|ic|ically)|anisotrop(y|ic|ically)|rotational(ly)?|rotation(s|al)?)',
r'totalistic|outer[- ]totalistic',
r'(equivalent|inequivalent|equivalence|conjugate|conjugates|orbit|orbits).{0,180}(cellular autom|rule|neighborhood)|(cellular autom|rule|neighborhood).{0,180}(equivalent|inequivalent|equivalence|conjugate|conjugates|orbit|orbits)',
r'quiescent.{0,180}(symmetric|symmetry|reflection)|(symmetric|symmetry|reflection).{0,180}quiescent',
r'(history|historical|first|original|search|198[1-4]).{0,220}(left[- ]right|right[- ]left|symmetr|asymmetr|totalistic)|(left[- ]right|right[- ]left|symmetr|asymmetr|totalistic).{0,220}(history|historical|first|original|search|198[1-4])',
]
rx=[re.compile(p,re.I) for p in patterns]
files=sorted((ROOT/'CHAPTERS').rglob('*.md'))+sorted((ROOT/'BACK-MATTER').rglob('*.md'))
hits={}
for p in files:
    rel=p.relative_to(ROOT).as_posix()
    for i,s in enumerate(p.read_text().splitlines(),1):
        if any(q.search(s) for q in rx): hits[(rel,i)]=s
variants={
('CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Mechanisms-in-Programs-and-Nature.md',491):3914,
('CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Mechanisms-in-Programs-and-Nature.md',655):4084,
('CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md',89):772,
('CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md',601):8318,
('CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md',687):8406,
('CHAPTERS/9-Fundamental-Physics/Fundamental-Physics.md',67):5232,
('CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md',39):8650,
('CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md',2750):11369,
('BACK-MATTER/Index/Index.md',540):12637,
('BACK-MATTER/Index/Index.md',2753):14852,
('BACK-MATTER/Index/Index.md',3194):15293,
('BACK-MATTER/Colophon/Colophon.md',4909):22352,
}
assert len(hits)==325 and len(variants)==12 and variants.keys()<=hits.keys()
assert all(hits[k]!=M[n-1] for k,n in variants.items())
exact={k:v for k,v in hits.items() if k not in variants}
assert len(exact)==313 and all(v in set(M) for v in exact.values())

guards={
490:'asymmetry between the left and right-hand sides is a direct consequence',
746:'interchange of left and right or black and white',
784:'symmetry of all the patterns is a consequence of the basic structure of totalistic rules',
1346:'32 rules which had left-right symmetry and made blank backgrounds stay unchanged',
1348:'rule 30 from page 27, as an example of a non-symmetric rule',
2798:'nearest neighbors in a symmetrical way',
5066:'all the possible symmetrical rules that involve two colors and nearest neighbors',
11636:'basic equivalences between elementary cellular automaton rules',
11637:'third entry is the rule obtained by interchanging left',
11897:'Numbers of rules',
18770:'quiescent symmetric elementary rules can emulate which',
}
for n,fragment in guards.items(): assert fragment in M[n-1],(n,fragment)
assert '$k^{1/2}k^{r+1}$' in M[11896]
assert 'left-right symmetry implies  $p_1 = p_2$' in M[16202]
assert 'c (f[x-dx, t] + f[x+dx, t])' in M[16204]
assert M[20825]=='# Index'
assert M[22457]=='#### Colophon'
print('T07 split/excerpt audit: PASS physical=325 exact=313 variants=12; 11 evidence guards; 2 source defects pinned')
PY
```

Recorded output:

```text
T07 split/excerpt audit: PASS physical=325 exact=313 variants=12; 11 evidence guards; 2 source defects pinned
```

## Book Excerpts and Evidence Groups

1. **Asymmetric rule versus symmetric-rule restriction (`BOOK:490,1348`).** Rule 30 is explicitly called nonsymmetric; the unequal left/right regions in its centered-seed picture are attributed to the underlying rule. This is a useful counterexample, not permission to infer a rule property from arbitrary pixels.
2. **Transform and orbit relation (`BOOK:746,768,11636-11637`).** Left/right interchange and black/white interchange are separate table operations. The 88 count concerns orbits under both operations, not the number of reflection-fixed rules and not the number of executors.
3. **General count (`BOOK:11897`).** Reversal/Burnside reconstruction gives the correct symmetric-table count. The Markdown formula `$k^{1/2}k^{r+1}$` is a local transcription defect; it is not used as algebra.
4. **Independent T06 conjunction (`BOOK:1344-1348,2796-2798,18770-18772`).** The historical 32 and page-247 gallery impose both reflection symmetry and blank preservation. “Quiescent symmetric” likewise names a conjunction of properties in an emulation relation.
5. **Totalistic implication (`BOOK:774-784,11902-11916`).** The source handles general and totalistic CA in one framework. Equal-weight summation over offsets `-r..r` is unchanged by reversal, so every strict T03/T04/T05 rule passes T07 without a flag.
6. **Complete 64-rule gallery (`BOOK:5062-5066`).** The figure labels all 64 reflection-fixed ECAs. Random initial conditions are a run profile; they do not make each displayed state spatially symmetric.
7. **Two-dimensional rotation relation (`BOOK:13534-13561`).** The 2D tables define rotational and complete symmetry under other groups. They validate a generic action abstraction but are not the identity of the one-dimensional T07 row.
8. **Isotropy boundary (`BOOK:15283-15297`).** Isotropy, rotation, and lattice symmetry are related action choices, not synonyms for the exact left-right reflection predicate.
9. **Rule/formula/pattern caution (`BOOK:17995-18001`).** Rule 254 is symmetric even though a derived NAND expression/result is described as asymmetric; reflecting rule 30 to rule 86 changes a downstream BDD sequence. Representations and observations do not replace the local table predicate.
10. **Historical selection (`BOOK:11585`).** Nonsymmetric rules were once excluded for display convenience. That history is evidence for a restriction, not a new transition construction.
11. **Source corrections (`BOOK:11897,16201-16207`).** The diffusion control assigns coefficients `p1,p2,p3` to left, center, right but says left-right symmetry implies `p1=p2`. Its next line uses equal outer coefficients, proving the intended relation is `p1=p3`. This PDE derivation is a control, not T07's definition.

The source statement that totalistic gallery patterns are symmetric is shorthand in a centered single-cell, compatible-background experiment. The exact theorem is rule covariance; a particular trajectory remains symmetric only when its seed and realization are also reflection-compatible.
