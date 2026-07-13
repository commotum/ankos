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
11637:'and right, and the fourth entry the rule obtained by applying both operations',
11897:'Numbers of rules',
18770:'quiescent symmetric elementary rules can emulate which',
}
for n,fragment in guards.items(): assert fragment in M[n-1],(n,fragment)
assert '$k^{1/2}k^{r+1}$' in M[11896]
assert 'left-right symmetry implies  $p_1 = p_2$' in M[16202]
assert 'c (f[x-dx, t] + f[x+dx, t])' in M[16204]
assert M[20825]=='#### Index'
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

## Asset and Raster Audit

The direction-sensitive source-to-asset closure contains 22 physical JPEGs and 44 exact monolith/split references. The partition is `4 included / 7 relation-only / 11 excluded-control`.

| Class | BOOK links | Role |
|---|---|---|
| Included/direct (`I`, 4) | `778,782,2796,5062` | totalistic rule structure, centered totalistic gallery, exact 32-rule T06/T07 intersection, and exact 64-rule T07 gallery |
| Relation-only (`R`, 7) | `732,734,3334,11641,14334,14729,18772` | all-256 combined equivalence survey, reflected structures, four-column rule transforms, conjugate/reflection period relation, state-network observer, and emulation graph |
| Excluded/control (`X`, 11) | `488,748,2598,2606,2626,2628,2800,5804,8206,17991,18768` | rule-30 counterexample, extraction stops, constraint/model-set rotations, sibling radius-two gallery, spacetime symmetry, display/encoding reversal, formula subsection, and preceding rule-41 figure |

Direction-sensitive findings:

- `BOOK:490` governs `488`, the visible rule-30 asymmetry counterexample.
- `BOOK:746` governs the preceding two-page all-256 run at `732,734`; `748` is the next six-rule nested gallery and an explicit stop.
- `BOOK:774-784` governs `778,782`. The latter visibly carries the 50 codes `993,996,...,1140`, but centered seed/background compatibility participates in the displayed pattern symmetry.
- `BOOK:2798` governs `2796`, whose 32 labels exactly match the independently derived reflection-fixed/zero-preserving intersection. `2800` starts a separately captioned radius-two totalistic gallery.
- `BOOK:3336` governs `3334`; reflected structures are a seed/trajectory consequence, not the rule predicate.
- `BOOK:5064,5066` govern `5062`, whose labels exactly match all 64 reflection-fixed ECAs.
- `BOOK:11636-11637` governs `11641`, the four-column original/color-conjugate/left-right/both transform table. It is not a table of 88 fixed rules.
- `BOOK:13534-13561` is a textual 2D symmetry table with no governed raster; `13565` begins a separate growth-rule subsection.
- `BOOK:14332` governs `14334`; `14733` retrospectively governs `14729`. Both are analysis relations.
- `BOOK:17995-18001` governs no image; `17991` belongs the preceding formula subsection.
- `BOOK:18770` says “network below”, so it governs only `18772`; `18768` is the preceding rule-41 control.

The constraint/model-set images at `2598,2606,2626,2628`, spacetime-symmetry image `5804`, and emulation/display reversal at `8206` demonstrate why a generic transformation vocabulary cannot be collapsed into T07.

### Exact asset, metadata, and reverse-reference oracle

```bash
python3 - <<'PY'
import re
from hashlib import sha256
from pathlib import Path

ROOT=Path('ref/A-New-Kind-of-Science')
BOOK=(ROOT/'A-New-Kind-of-Science.md').read_text().splitlines()
items={
'CHAPTERS/2-The-Crucial-Experiment/Images/_page_44_Picture_1.jpeg':(488,450259,1199,1347,'8c185b67ff67a82145f6657b9767df10b5c5d234358d0187bbae21166ef32aa8','X','CHAPTERS/2-The-Crucial-Experiment/The-Crucial-Experiment.md',79),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_70_Picture_2.jpeg':(732,305792,1183,1505,'9827975022d3b4b9b0eab40a00cd3b8e9e6fc562541169a894d898838a45d811','R','CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md',49),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_71_Picture_2.jpeg':(734,254855,1178,1519,'b55c911ef358b73a04f59a5c090f49f4527729eed0e00c09d9c9bb99659c66ca','R','CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md',51),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_73_Figure_1.jpeg':(748,156812,1156,953,'f3eb6b029f208043f572df79a5e5de8877939888bb6baf6958322560c932da57','X','CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md',65),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_75_Figure_6.jpeg':(778,51178,610,446,'acb13963632286960ca61b616ff2f45a940750f3ab7deb5e6fbf696543015c15','I','CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md',95),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_76_Figure_2.jpeg':(782,174691,1109,1279,'8c11659c8bd63d37a972c5ffab376b62948f7c4e05f9fd10f239e51464f4084d','I','CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md',99),
'CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_226_Picture_9.jpeg':(2598,37372,480,342,'6d25b292bb7a1d01eb7a745fde1eafd36416133e23e7852773abc205a246717b','X','CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md',427),
'CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_227_Figure_3.jpeg':(2606,306964,1143,1089,'36beded6e40b45e1007ef8d8b631ed24d492bd8f411ae069eeca2614ced3d682','X','CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md',435),
'CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_229_Picture_1.jpeg':(2626,528780,1239,1462,'e9e718444e44af1d3a41a229e44927d65d3691aaf098c8d964f0d88e7e01dc79','X','CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md',451),
'CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_230_Figure_2.jpeg':(2628,470834,1165,1226,'2af86815dd48d0c17257587b822add600b9a1736d18f17b20c2dbfcaae7a043b','X','CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md',453),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_247_Figure_2.jpeg':(2796,261973,1086,1387,'00f9660bac37681f214cbf4b234dffeab446e3d23e4de2a7c49ff7011f7db6a0','I','CHAPTERS/6-Starting-from-Randomness/Starting-from-Randomness.md',95),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_248_Figure_2.jpeg':(2800,281697,1086,1389,'b2a20cb8095eb211fedd963d622222ca98fe0428f397b71bef90db8fa6871957','X','CHAPTERS/6-Starting-from-Randomness/Starting-from-Randomness.md',99),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_299_Picture_3.jpeg':(3334,127700,1150,600,'32d4ed4b16a083fb731c37cc80c64efb9995756808c316a0ced0dea0e9bd5475','R','CHAPTERS/6-Starting-from-Randomness/Starting-from-Randomness.md',629),
'CHAPTERS/8-Implications-for-Everyday-Systems/Images/_page_439_Figure_3.jpeg':(5062,214555,1170,896,'6bb82abcca21ce0ffbf44e3a4eb5976f83f296494ec8bc51c9c54544be756f9b','I','CHAPTERS/8-Implications-for-Everyday-Systems/Implications-for-Everyday-Systems.md',699),
'CHAPTERS/9-Fundamental-Physics/Images/_page_500_Figure_3.jpeg':(5804,244257,895,1014,'bcacb0823dbd5f4d883ec53e87d7a61229d4c39baba4916c0fe0948c34d07c7a','X','CHAPTERS/9-Fundamental-Physics/Fundamental-Physics.md',639),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_696_Picture_2.jpeg':(8206,545148,1128,1250,'1f525dab46619a2782a7275d179fd3e27f28fe67ac9e84e949af058c52edd38f','X','CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md',495),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_898_Picture_8.jpeg':(11641,232644,1205,753,'243e9c966fb2cbba13168318664eba2307e577da3c1f356297658ee5081634a4','R','CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md',3022),
'BACK-MATTER/Index/Images/_page_966_Figure_12.jpeg':(14334,15102,594,139,'43c4548e91dd3597641c8bff4653418da5993ac422fe6486ea43802ca3f941d2','R','BACK-MATTER/Index/Index.md',2235),
'BACK-MATTER/Index/Images/_page_978_Figure_2.jpeg':(14729,38767,587,399,'a7fc2a3f9c7a5a8dd1894863d0c1b614d7a87cceae3ffd198325330d4b4c2be4','R','BACK-MATTER/Index/Index.md',2630),
'BACK-MATTER/Colophon/Images/_page_1112_Picture_5.jpeg':(17991,17941,564,127,'981fbbd63ca8134a3a0b1dd8d5673b7d8111a95650834f5ef0bb5e0e5af73257','X','BACK-MATTER/Colophon/Colophon.md',548),
'BACK-MATTER/Colophon/Images/_page_1133_Picture_6.jpeg':(18768,18262,569,136,'11dde5ae83b89e5879a0c7b02e06b759443ce65bc372fa426ee388b927aea33f','X','BACK-MATTER/Colophon/Colophon.md',1325),
'BACK-MATTER/Colophon/Images/_page_1133_Picture_8.jpeg':(18772,23917,424,349,'9f933b79fdc7dd17b803ec2f9bc1a0e851500b6a14b7f494ccc3cf32d3e3290c','R','BACK-MATTER/Colophon/Colophon.md',1329),
}

def jpeg_size(data):
    assert data[:2]==b'\xff\xd8'
    sof={0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf}
    i=2
    while i<len(data):
        while i<len(data) and data[i]!=0xff: i+=1
        while i<len(data) and data[i]==0xff: i+=1
        assert i<len(data); marker=data[i]; i+=1
        if marker in {0x00,0x01} or 0xd0<=marker<=0xd9: continue
        size=int.from_bytes(data[i:i+2],'big')
        if marker in sof:
            return (int.from_bytes(data[i+5:i+7],'big'),
                    int.from_bytes(data[i+3:i+5],'big'))
        i+=size
    raise AssertionError('JPEG SOF marker not found')

counts={'I':0,'R':0,'X':0}; digests=set(); refs={}
for path,(book,size,w,h,digest,kind,split,split_line) in items.items():
    p=ROOT/path; data=p.read_bytes(); name=p.name
    assert BOOK[book-1]==f'![]({name})'
    assert (len(data),*jpeg_size(data),sha256(data).hexdigest())==(size,w,h,digest)
    assert digest not in digests; digests.add(digest); counts[kind]+=1
    found=[]
    for md in ROOT.rglob('*.md'):
        for line_no,line in enumerate(md.read_text().splitlines(),1):
            if re.fullmatch(r'!\[\]\((?:Images/)?'+re.escape(name)+r'\)',line):
                found.append((md.relative_to(ROOT).as_posix(),line_no))
    assert set(found)=={('A-New-Kind-of-Science.md',book),(split,split_line)},(path,found)
    refs[name]=found
assert len(items)==22 and counts=={'I':4,'R':7,'X':11}
assert sum(map(len,refs.values()))==44 and all(len(v)==2 for v in refs.values())
print('T07 asset oracle: PASS 22 assets; refs=44; classes=4,7,11; unique_hashes=22')
PY
```

Recorded output:

```text
T07 asset oracle: PASS 22 assets; refs=44; classes=4,7,11; unique_hashes=22
```

## Construction Model

### Architecture classification

| T07-related object | Audit class | Smallest reusable base | Consequence |
|---|---:|---|---|
| Left-right-symmetric catalog row | 2 — restriction/property | resolved T01/T02 finite-table CA plus D119 property records | selection returns exact unchanged program |
| T03/T04/T05 proof | 2 — derived property | equal-weight aggregate over reflection-closed stencil | no exhaustive expansion or runtime flag required |
| Reflected rule/program | 2 — transform/relation | slot permutation of the same typed local evaluator | ordinary target program; transform is involutive |
| Reflection-only and reflection/color orbits | 2 — analyzer/equivalence relation | finite group action on rule descriptions | 160 and 88 are analysis counts, not executable-family counts |
| Compact reflection-orbit table | 3 — lossless representation | ordinary finite local function plus validated action | optional rule descriptor; same shared evaluation/update algebra |
| Symmetric seed, boundary, trajectory, or raster | 2 — run invariant/view | ordinary seed, realization, run, and observer records | never property proof by itself |
| New state/frontier/neighborhood/update/executor | 4 only if a counterexample requires it | none found | no T07 execution semantic is authorized |

### Exact local action and predicate

Let the ordered static read offsets of an eligible program be

```text
Delta = (delta_1, ..., delta_q).
```

The catalog reflection `h` acts on the one-dimensional spatial coordinate by `h(delta)=-delta`. Eligibility requires reflection closure and therefore a unique slot involution `pi` satisfying

```text
h(delta_i) = delta_pi(i).
```

For ordinary T07 colors, reflection leaves ALPHABET values unchanged. The complete-read action is

```text
(rho v)_i = v_pi(i).
```

For a centered radius-`r` stencil this is ordinary vector reversal. If the resolved deterministic local evaluator is `T:A^q->A`, define

```text
T^R(v) = T(rho v).

LeftRightSymmetric(P,h)
    iff T(v) = T(rho v) for every v in A^q.
```

The property is universal over complete typed local reads. A sampled run, family name, Boolean flag, code-number shortcut, or palette cannot establish it.

The generic equivariant extension for oriented labels requires an explicit involution `alpha:A->A`:

```text
(rho_alpha v)_i = alpha(v_pi(i))
T^h(v)           = alpha(T(rho_alpha v))
T(rho_alpha v)   = alpha(T(v)).
```

That is not silently part of the scalar-color T07 catalog row. Black/white conjugation is explicitly separate in the source. An oriented tagged/product alphabet can support such an action, but the action, fixed outputs, and validation must be visible.

### DOMAIN, writes, and global covariance

T07's DOMAIN is the existing `t+1D` support/topology. Reflection is an automorphism of its spatial coordinate, not a new DOMAIN type. For a configuration action

```text
(H X)(x) = alpha(X(h x)),
```

and the corresponding typed write action

```text
(x, Assign(a)) -> (h x, Assign(alpha(a))),
```

the shared atomic update gives the transform identity

```text
H(Step_P(X)) = Step_(P^h)(H X).
```

Consequences are deliberately separated:

- If `P^h=P`, then `Step_P` commutes with reflection.
- If the seed also satisfies `H X_0=X_0`, every later state is symmetric.
- An asymmetric seed under a symmetric rule has a mirrored companion trajectory; it need not itself be symmetric.
- A reflection-invariant random seed distribution gives ensemble symmetry, not necessarily symmetric samples.
- A symmetric observed trace does not prove the rule symmetric; rule 30 on the all-zero field is a counterexample.
- Finite support, exterior/boundary, FRONTIER/schedule, and observation window must commute with the same action before a global trajectory/view theorem is valid.

`BOUNDARY=REFLECTIVE` folds out-of-range reads at an edge. It is not the global DOMAIN automorphism above. A fixed boundary can be compatible only when its two sides transform appropriately; hostile asymmetric exterior values can break an otherwise symmetric finite trajectory without falsifying the local rule property.

### Exact counts and codecs

For `k=|A|`, radius `r`, and `q=2r+1`, there are

```text
C = k^(2r+1)
```

ordered contexts. Reversal fixes exactly the palindromes:

```text
F = k^(r+1).
```

Burnside therefore gives

```text
O = (C+F)/2
  = 1/2 * k^(r+1) * (1+k^r)
```

context orbits, and exactly

```text
k^O
```

left-right-symmetric rule tables. This reconstructs the corrupted source formula at `BOOK:11897`.

Examples:

- `k=2,r=1`: `C=8`, `F=4`, `O=6`, hence 64 symmetric ECAs.
- `k=2,r=2`: `O=20`, hence 1,048,576 symmetric rules; the 64 totalistic rules are a strict subset.
- `k=3,r=1`: `O=18`, hence 387,420,489 symmetric rules; the 2,187 totalistic rules are a strict subset.
- Fixing one designated blank context orbit divides the symmetric count by `k`; ECA gives the source's 32-rule T06/T07 intersection.

For the ECA codec `i=4*l+2*c+r`, reflection maps `i` to `4*r+2*c+l`, swapping digit positions `1<->4` and `3<->6` while fixing `0,2,5,7`. Rule 30 reflects to rule 86; rules 2/16, 45/101, 60/102, 110/124, and 137/193 are other explicit pairs.

The number of reflection orbits of all rule tables is instead

```text
(k^(k^(2r+1)) + k^O)/2.
```

For ECA this is 160. The source's 88 comes from the four-element group generated by reflection and black/white conjugation, whose Burnside fixed counts are `256/64/16/16`. Rule 29 is fixed by the combined transform but not by reflection alone, so conflation is observably wrong.

### Totalistic proof

For strict T03, with explicit valuation `nu` and sum table `U`,

```text
s(v) = sum_i nu(v_i).
```

Reversal is a permutation of the same reflection-closed offsets, so

```text
s(rho v) = s(v)
U(s(rho v)) = U(s(v)).
```

Every valid T03/T04/T05 program therefore passes T07, independent of table rows and without trusting a `totalistic` family tag. Other structurally permutation-invariant summaries can prove the same property. Unequal weights are not categorically asymmetric: paired weights `w[-i]=w[i]` can pass, while an asymmetric weighting needs an actual counterexample. Structural action checking, not family dispatch, decides.

### Lossless orbit-table representation

With the catalog's identity output action, choose the canonical context key

```text
rep(v) = lexicographic_min(v, rho v).
```

A complete compact table

```text
T_hat : A^q / C2 -> A
```

has exactly `O` rows and expands losslessly as

```text
T(v) = T_hat(rep(v)).
```

This is an optional typed RULE representation of the same local function, not a second runner. An exhaustive passing program need not be rewritten or compressed during validation. Representation/provenance identity stays distinct even when a denotational semantic digest is shared.

For nontrivial `alpha`, a plain orbit-to-one-output table is not lossless. Outputs on a two-element orbit are related by `alpha`, and a fixed read must map to an `alpha`-fixed output. If `f=|Fix(alpha)|`, then `f*k^r` contexts are fixed by the combined read action and the number of equivariant tables is

```text
k^((k^(2r+1)-f*k^r)/2) * f^(f*k^r).
```

The representation must encode those stabilizer constraints explicitly.

The documented `ISOTROPIC` form also needs correction for multiple read components. Quotienting each component independently uses a product action and can over-collapse. One physical reflection must act diagonally on the complete read tuple, possibly permuting components. For example,

```text
(a_left and b_left) or (a_right and b_right)
```

is invariant when both components swap together, but not when just one swaps. Goal 2 must define one validated complete-read action, not unrelated per-component orbits.

### Eligibility, results, and identity

T07 v1 reuses T06's strict CA property eligibility and adds action closure. The resolved program must expose:

- a finite typed ordered alphabet;
- a fixed homogeneous `t+1D` support with the canonical spatial reflection;
- a static finite current-snapshot read schema closed under that reflection;
- a derived diagonal permutation of the complete read;
- a closed total deterministic structural evaluator;
- `AllSites`, exactly one typed same-site assignment per selected site, and old-snapshot parallel update; and
- the identity label/output action required by the catalog row.

Verdicts are exact:

1. **Invalid claim:** malformed/dangling program or action reference, inconsistent serialized slot map, wrong action version, nonidentity catalog action, or failed canonical resolution. No semantic verdict exists.
2. **`UnsupportedProperty`:** a valid claim references an opaque callback, non-reflection-closed schema, dynamic read, stochastic/multiway successor, asynchronous schedule, non-CA rewrite, or oriented labels without a supported explicit action. Unsupported is not evidence.
3. **`DoesNotHold`:** an eligible checker finds a canonical context whose typed output differs from its reflected mate.
4. **`Holds`:** exhaustive orbit comparison or a validated structural proof closes every obligation.

A constant rule over a one-sided stencil is the key unsupported-versus-false adversary: its global function may commute with reflection, but reflection is not an endomorphism of its declared read schema. The checker must not invent a missing left slot or emit `DoesNotHold`.

Keep these identities separate:

```text
Program
RulePropertyClaim(kind=ReflectionEquivariance, program_ref, action_ref, version)
ReflectionSymmetryEvidence
ValidatedProgramSelection
ReflectedProgramTransform
OrbitRuleRepresentation
Run / realization / observer
```

Evidence binds claim/program/action digests, checker/evaluator versions, method (`ExhaustiveOrbitCheck` or validated structural proof), `C/F/O`, a canonical context-orbit digest, and—for failure—the first canonical representative, reflected read, and unequal typed outputs. Cancellation or resource exhaustion is not `DoesNotHold`. Passing selection returns the exact unchanged `P`; producing `P^h` or a compact table is a separate explicit transform.

### Dependency-free semantic oracle

```bash
python3 - <<'PY'
from itertools import product

def contexts(k,r): return tuple(product(range(k),repeat=2*r+1))
def index(v,k):
    out=0
    for x in v: out=out*k+x
    return out
def digits(n,k,m): return tuple((n//(k**i))%k for i in range(m))
def encode(ds,k): return sum(x*k**i for i,x in enumerate(ds))
def reflect_table(table,k,r):
    out=[0]*len(table)
    for v in contexts(k,r): out[index(v,k)]=table[index(v[::-1],k)]
    return tuple(out)
def symmetric(table,k,r): return tuple(table)==reflect_table(table,k,r)
def orbit_keys(k,r): return {min(v,v[::-1]) for v in contexts(k,r)}
def reflected_code(n,k=2,r=1):
    return encode(reflect_table(digits(n,k,k**(2*r+1)),k,r),k)

for k,r in ((2,1),(2,2),(3,1),(4,1)):
    C=k**(2*r+1); F=k**(r+1); O=(C+F)//2
    assert len(orbit_keys(k,r))==O
    assert k**O==k**((C+F)//2)
assert len(orbit_keys(2,1))==6 and 2**6==64
assert len(orbit_keys(3,1))==18 and 3**18==387420489

fixed=[n for n in range(256) if reflected_code(n)==n]
expected=[0,1,4,5,18,19,22,23,32,33,36,37,50,51,54,55,
72,73,76,77,90,91,94,95,104,105,108,109,122,123,126,127,
128,129,132,133,146,147,150,151,160,161,164,165,178,179,
182,183,200,201,204,205,218,219,222,223,232,233,236,237,
250,251,254,255]
assert fixed==expected
assert reflected_code(30)==86 and reflected_code(86)==30
assert reflected_code(2)==16 and reflected_code(60)==102
assert len({min(n,reflected_code(n)) for n in range(256)})==160

def conjugate_code(n):
    d=digits(n,2,8); out=[0]*8
    for v in contexts(2,1):
        inv=tuple(1-x for x in v)
        out[index(v,2)]=1-d[index(inv,2)]
    return encode(out,2)
assert sum(conjugate_code(n)==n for n in range(256))==16
assert sum(reflected_code(conjugate_code(n))==n for n in range(256))==16
assert len({min(n,reflected_code(n),conjugate_code(n),
                    reflected_code(conjugate_code(n))) for n in range(256)})==88
assert reflected_code(conjugate_code(29))==29 and reflected_code(29)!=29

zero_fixed=[n for n in fixed if digits(n,2,8)[0]==0]
assert zero_fixed==[0,4,18,22,32,36,50,54,72,76,90,94,104,108,122,126,
128,132,146,150,160,164,178,182,200,204,218,222,232,236,250,254]

for k,r in ((2,1),(2,2),(3,1),(4,1)):
    table=tuple((3*s+1)%k for s in range(1+(k-1)*(2*r+1)))
    for v in contexts(k,r): assert table[sum(v)]==table[sum(v[::-1])]

t90=digits(90,2,8)
compact={min(v,v[::-1]):t90[index(v,2)] for v in contexts(2,1)}
expanded=tuple(compact[min(v,v[::-1])] for v in contexts(2,1))
assert len(compact)==6 and expanded==t90 and symmetric(expanded,2,1)

def step(row,n,left=0,right=0):
    d=digits(n,2,8); ext=(left,*row,right)
    return tuple(d[index(ext[i:i+3],2)] for i in range(len(row)))
def rev(row): return tuple(reversed(row))
row=(0,1,1,0,1)
assert step(rev(row),reflected_code(30))==rev(step(row,30))
assert step(rev(row),90)==rev(step(row,90))
assert row!=rev(row) and step(row,90)!=rev(step(row,90))
hostile=step((0,0),90,left=1,right=0)
assert hostile==(1,0) and hostile!=rev(hostile)
assert {0,1}!={-x for x in {0,1}}

program={'kind':'eca','code':90,'table':t90}
def require(p):
    if not symmetric(p['table'],2,1): raise ValueError
    return p
assert require(program) is program
print('T07 semantic oracle: PASS')
print('eca=',len(fixed),'reflection_orbits=',160,'V4_orbits=',88,
      'quiescent_intersection=',len(zero_fixed),'r30_mirror=',reflected_code(30))
print('general=',{'k2r2':2**20,'k3r1':3**18},
      'totalistic_proof=PASS','hostile_boundary=',hostile)
PY
```

Recorded output:

```text
T07 semantic oracle: PASS
eca= 64 reflection_orbits= 160 V4_orbits= 88 quiescent_intersection= 32 r30_mirror= 86
general= {'k2r2': 1048576, 'k3r1': 387420489} totalistic_proof=PASS hostile_boundary= (1, 0)
```

## Current API Fit

| Current documented component | Fit | T07 consequence |
|---|---|---|
| DOMAIN, fixed support, ordered relative reads | DIRECT | Existing spatial coordinates and ordered offsets are sufficient to derive reflection and the slot involution (`simple_programs.md:26-38,360-384,590-607`). |
| Old-snapshot parallel RULE/UPDATE | DIRECT | Same-site writes already commute with a validated support action; no symmetric update law exists (`simple_programs.md:101-106,1767-1791`). |
| `EXHAUSTIVE` complete local table | PARAMETERIZATION | A structural finite evaluator can be checked orbit-by-orbit without changing the program (`simple_programs.md:1795-1831`). |
| `ISOTROPIC` | PRINCIPLED EXTENSION plus SEMANTIC REPAIR | Orbit lookup is the right representation idea, but independent component quotients over-collapse diagonal physical actions and output actions are absent (`simple_programs.md:1833-1863`). |
| `TOTALISTIC` | STRUCTURAL PROOF ADAPTER | Equal-weight aggregate on a reflection-closed stencil proves T07; no family flag or expansion is needed (`simple_programs.md:1964-2032`). |
| `BOUNDARY=REFLECTIVE` | NOT APPLICABLE to predicate | It maps exterior reads and is not global rule reflection (`simple_programs.md:292-358`). |
| Generic D119 property records | DIRECT generic boundary | T07 reuses claim/evidence/unsupported/selection identity separation, with a different universal obligation and action reference (`goal-1/design-ledger.md:871-881`). |

The documentation repair must replace independent `G_j` orbits with one action on the complete typed read. A product action remains expressible when it is deliberately declared; it cannot be inferred from multiple neighborhood components.

## Current Runtime Fit

| Runtime surface | Fit | Evidence and consequence |
|---|---|---|
| `neighborhoods.eca` and literal/metric offsets | DIRECT geometry | The centered radius stencil and explicit offsets can derive `pi`; no stored “reverse order” flag is needed (`src/ca/neighborhoods.py:140-176,551-569`). |
| `rules.Rule` and callbacks | SEMANTIC MISMATCH | Family/params/callable metadata does not expose a complete typed evaluator or stable program identity, so callbacks cannot be certified (`src/ca/rules.py:30-33,64-78`). |
| `rules.exhaustive` / `totalistic` channel shapes | PARAMETERIZATION / INCOMPLETE | They suggest reusable descriptors, but omit complete arity/table/action semantics and inherit T01/T03 codec defects (`src/ca/rules.py:173-217`). |
| `_channel_state` exhaustive codec | SEMANTIC MISMATCH | Low-significance-first weights mirror asymmetric Wolfram tables; rule 30 would be confused with 86 if code equality were trusted (`src/ca/rollout.py:742-760`). |
| Family-dispatched rollout | SEMANTIC MISMATCH | No T07 branch may be added to the current family switch; Goal 2 must use the shared structural evaluator (`src/ca/rollout.py:145-212,264-331`). |
| `datasets.invariance_transforms` / `reflect-x` | OBSERVER METADATA ONLY | It supplies an affine dataset transform, not a rule claim, evaluator proof, transformed program, or finite-realization center (`src/ca/datasets.py:640-706`). |
| Reflective boundary gathering | DIRECT realization, NOT proof | The explicit edge mapping remains run data and can coexist with symmetric or asymmetric rules (`src/ca/loci.py:589-596`; `tests/test_loci.py:54`). |
| Existing tests | NOT SUFFICIENT | Tests cover family counts, boundary gathering, and one 2D dataset rotation, but no reflection predicate, rule transform, orbit table, totalistic proof, identity, or trajectory qualification (`tests/test_rules.py:9-46`; `tests/test_datasets.py:124-138`). |

Repository-wide inspection finds no implemented T07 property or transform API. These are Goal 2 gaps, not reasons to create a family executor.

## Principles Audit

- **Principles 0-1:** the catalog name creates no construction. The source filters ordinary tables and relates them by explicit transforms.
- **Principles 2-4:** the property reads the existing complete local evaluator; passing programs keep ordinary writes and atomic update. The runner is unchanged.
- **Principles 5-7:** no hidden mirrored-state bit, orientation cache, symmetric seed default, or reflected-boundary assumption enters state. DOMAIN action and ALPHABET action are typed separately.
- **Principles 8 and 12:** code numbers, 64/160/88 lists, gallery order, palettes, random samples, crops, rasters, and BDD sizes are codecs or analyses. The structural equality over typed reads is authoritative.
- **Principles 9-10:** the predicate genuinely couples a resolved program with the canonical reflection action. Seed, boundary, horizon, observer, and later run identity remain independent.
- **Principle 11:** `T(v)=T(rho v)` and the corresponding one-step commuting diagram define the property. Search history and pictures do not.
- **Principles 13-15:** rule 30/86, rule 29, rule 90, hostile exterior, a one-sided schema, a diagonal two-component action, exact counts, and object identity are explicit adversaries. Current tests do not already prove them.
- **Principle 16:** one generic action/property/transform/orbit-representation boundary is architecture. A `symmetric` flag, family branch, reversed selector, independent component quotient, or seed-based shortcut is a shim.

D111-D119 remain valid. T07 closes the following post-audit decision for global integration:

### D120 — Left-right symmetry is a validated program property over an explicit action; orbit lookup is representation, not execution semantics

- **Basis:** the source distinguishes nonsymmetric rule 30 (`BOOK:490,1348`), left/right table transformation and combined equivalence (`746,11636-11637`), the independent blank-preserving conjunction (`1346,2798`), totalistic structural symmetry (`784,11902-11916`), and all 64 symmetric elementary rules (`5064-5066`). No source supplies a distinct successor or update.
- **Eligibility and predicate:** T07 v1 binds one resolved finite deterministic homogeneous `t+1D` CA program `P` to the canonical nonidentity spatial reflection with identity ALPHABET action. The declared static local-read offsets must be reflection-closed and induce one diagonal complete-read involution `rho`. `Holds` iff the ordinary structural evaluator satisfies `T(v)=T(rho v)` for every complete typed read.
- **Verdict and evidence:** invalid claims, `UnsupportedProperty`, `ReflectionSymmetryEvidence(DoesNotHold)`, and `ReflectionSymmetryEvidence(Holds)` are distinct. Evidence records action/program/schema digests, proof method, context/orbit counts and digest, and the first canonical mismatch on failure. Unsupported or incomplete checking is not evidence.
- **Transform and trajectory:** the reflected evaluator `T^R=T∘rho` is an ordinary program transform and involution. `H(Step_P X)=Step_(P^R)(H X)`; a fixed rule commutes with reflection, while a symmetric trajectory additionally requires compatible seed, realization/boundary, frontier/schedule, and view.
- **Representation:** for identity output action, a complete canonical orbit table with `(k^(2r+1)+k^(r+1))/2` rows is a lossless RULE representation. Complete-read actions are diagonal; nontrivial output actions require stabilizer-aware equivariant rows. Representation/provenance, transform, claim, evidence, selection, program, and run identities remain separate.
- **Consequence:** T07 adds no state, FRONTIER, NEIGHBORHOOD read, RULE result, UPDATE, executor, successor, outcome, halt, seed, boundary, observer, or family dispatch. A passing catalog selection resolves to the exact unchanged `P`; optional reflection or compaction is a separate explicit operation.

## Detailed Implementation Plan

1. **Complete:** close the ten-family 268-line lexical union, 15 governed continuations, 74 actual-Index routes, 325 split hits, 12 split variants, and exact `15/167/3/98/74` disposition.
2. **Complete:** close the direction-sensitive 22-file/44-reference asset ledger at `4/7/11`, with exact metadata, hashes, visual label findings, and stop boundaries.
3. **Complete:** derive the reflection action, local fixed-point predicate, reflected-program involution, global covariance qualifications, exact counts/codecs, totalistic proof, and orbit representation.
4. **Complete:** audit current documentation/runtime/tests and the T01-T06, two-dimensional/isotropy, seed, boundary, observer, and emulation boundaries.
5. **Complete:** specify typed claims, evidence, unsupported results, validated selection, transform/representation identity, serialization, and migration.
6. **Complete locally:** run the four embedded oracles, independent review, repository tests, Markdown fences, diff/status gates, and then integrate D120 and the Goal 2 handoff globally.

## Goal 2 Implementation Stage

**G2-T07 — generic finite-action rule properties, transforms, and orbit representations.** Implement after G2-T01/T02 establish structural finite CA programs/evaluators and alongside the generic D119 property layer. T03 supplies a proof adapter; it is not a dependency on a totalistic runtime family.

| Goal 2 surface | Required work |
|---|---|
| `simple_programs.md` action model | Define a versioned support/read/write action on the complete typed local interface. Correct `ISOTROPIC` from independent component orbits to a declared diagonal complete-read action; specify optional component permutations and output actions. |
| structural program/rule schema | Expose finite ordered offsets, ALPHABET identity, complete total evaluator, same-site typed writes, and canonical program identity. Opaque callbacks remain uncertifiable. |
| generic action module | Validate involution/group closure, support automorphism, reflection-closed offsets, derived slot/component permutation, label/output action, canonical action digest, and transformed-program construction. |
| generic property module | Add `RulePropertyClaim(kind=ReflectionEquivariance)`, invalid/unsupported/result boundaries, exhaustive-orbit and structural-proof checkers, canonical mismatch witnesses, and resource-incomplete handling. |
| exhaustive and T03 adapters | Exhaustive tables compare one representative and mate per orbit. Equal-weight T03 descriptors emit a validated permutation-invariance proof without expansion. Paired weighted summaries may prove the same fact structurally. |
| orbit-rule representation | Add a complete canonical orbit-key table for trivial output action and a stabilizer-aware equivariant form when nontrivial actions are supported. Validate cardinality, keys, outputs, action ID, expansion, and denotational equivalence. |
| catalog/resolver | The T07 convenience constructor binds the canonical one-dimensional nonidentity reflection and identity label action. Recompute evidence; accept only fresh `Holds`; return exact unchanged `P`. |
| serialization/identity | Version and round-trip action, claim, evidence, transform, representation, and selection separately. Preserve program/run separation and reject stale/tampered action maps or proof digests. |
| rollout/executor | No T07 change. Static checks reject symmetry flags, mirrored selector shims, reflected table patches, seed/boundary assumptions, and property branches. |
| tests/source fixtures | Add the 18 acceptance groups below, exact source/count/list/hash fixtures, the two source-repair guards, and full metamorphic/identity/static checks. |

### Eighteen acceptance groups

1. **Catalog action integrity:** accept only the canonical nonidentity `t+1D` left-right reflection with identity label action; reject identity, wrong axis, noninvolutive, stale, or caller-invented slot maps.
2. **Strict eligibility:** accept resolved finite deterministic homogeneous CA programs; return `UnsupportedProperty` for opaque callbacks, dynamic reads, stochastic/multiway rules, asynchronous/partial schedules, and unrelated SimpleProgram shapes.
3. **Reflection closure:** derive slot permutation from offsets and reject duplicates/missing mates/inconsistent serialized maps. A one-sided constant-rule schema is unsupported, not false.
4. **Invalid versus semantic result:** malformed references produce validation diagnostics and no verdict; valid unsupported programs produce non-evidence; eligible programs produce `DoesNotHold` or `Holds` evidence.
5. **ECA failures and transforms:** rule 30 fails on a canonical reversed-context witness and transforms exactly to 86; 2/16, 45/101, 60/102, 110/124, and 137/193 are exact pairs; transform is involutive.
6. **Exact fixed tables:** assert the exact 64 ECA fixed labels and the page-439 asset hash/label fixture; rule 90 passes.
7. **Orbit-count separation:** assert 160 reflection-only ECA rule orbits and 88 combined reflection/color orbits with Burnside fixed counts `256/64/16/16`; rule 29 passes only the combined action.
8. **T06 composition:** assert the exact 32 reflection-fixed/zero-preserving ECA labels and page-247 asset fixture; neither property implies the other.
9. **General counts/source repair:** assert `k^((k^(2r+1)+k^(r+1))/2)` including `2^20` and `3^18`; pin the corrupted `BOOK:11897` string so it cannot become authority.
10. **Totalistic structural proof:** every small exhaustive expansion agrees with the T03 proof adapter; T04/T05 pass without table mutation or family dispatch; exact 16 binary radius-one totalistic rules are a strict subset of 64 symmetric rules.
11. **Weighted/summary boundary:** paired symmetric unequal weights may pass; an asymmetric weighting produces a canonical witness. Never decide by the word `weighted` or `totalistic` alone.
12. **Orbit representation:** complete compact tables expand losslessly; reject missing/duplicate/noncanonical keys, wrong row count/action ID, invalid values, bad fixed-orbit outputs, and independent-component overcollapse.
13. **Output-action adversary:** an oriented tagged alphabet with swap involution catches omitted input/output actions and fixed-output constraints; scalar T07 must not accept it under identity action by accident.
14. **Diagonal-action adversary:** the two-component `(aL and bL) or (aR and bR)` evaluator passes simultaneous reflection but fails an independent one-component swap; the documented overquotient cannot survive.
15. **Trajectory qualification:** rule 204 with asymmetric seed disproves rule-symmetric implies state-symmetric; rule 30 on all zero disproves state-symmetric implies rule-symmetric; rule 90 with hostile exterior disproves boundary-free trajectory claims.
16. **Identity separation:** property selection returns the exact original program object/hash; transforming or compacting creates separate artifacts; action, claim, evidence, selection, representation, program, and run IDs cannot collide.
17. **Evidence trust/serialization:** recompute rather than trust serialized `Holds`; reject tampered witness/action/evaluator versions; cancellation or resource exhaustion cannot become `DoesNotHold`; canonical round trips preserve all references.
18. **No-cheating/static:** no T07/symmetric/isotropic rollout branch, reverse-selector shim, code-number authority, table patch, seed default, boundary shortcut, dataset-transform proof, trusted Boolean, or sampled-raster proof.

## No-Cheating Checks

- No T07/symmetric/isotropic family executor, update law, runtime flag, hidden coordinate transform, or special rollout.
- No sampled symmetric trajectory, symmetric seed, reflective boundary, totalistic family name, palette reflection, dataset augmentation, or displayed raster accepted by itself as rule proof.
- No conflation of left-right reflection, black/white conjugation, rotation, arbitrary permutation, boundary reflection, spacetime symmetry, model-set equivalence, or display reversal.
- No independent per-component orbit quotient when one physical action is diagonal over the complete read.
- No orbit representation without a validated action, canonical complete keys, typed outputs, stabilizer rules when required, and lossless expansion.
- No opaque callback, mirrored Wolfram codec, family dispatch, trusted Boolean metadata, or code-number comparison substituted for structural checking.
- No invalid, unsupported, incomplete, `DoesNotHold`, and `Holds` result collapsed into one Boolean.
- No mutation of a passing program and no transform, compaction, seed, boundary, horizon, observer, or run field inside property identity.

## Completion Requirements

- [x] Every direct/alias/caption/Notes/actual-Index/split/cross-reference/equivalence/seed/pattern/control candidate is dispositioned with zero remainder under a declared reproducible protocol.
- [x] Every relevant governed asset is hash-pinned and classified, with every source-permitted semantic/raster check closed.
- [x] The rule predicate, reflection action, transform/orbit identities, exact counts/code relations, compact representation, and rule/seed/boundary/trajectory/view distinctions are proved across supported descriptions.
- [x] Current API/runtime fit and a concrete Goal 2 property/transform/conformance stage are implementation-ready.
- [ ] Global ledgers, independent final review, all embedded checks, coverage/diff gates, and repository tests pass.

## Stage Results

IN PROGRESS pending final verification and global integration.

## Integration Results

1. **Catalog kind:** class-2 restriction/property, not a new SimpleProgram construction.
2. **Smallest base:** the resolved finite ordered local CA program from T01/T02; T03 supplies a proof adapter.
3. **New state/read/result/update/executor:** none. A generic action/property layer inspects the existing complete evaluator.
4. **New generic records:** reflection action, claim/evidence, validated selection, transform artifact, and optional orbit representation; only the last is a RULE description, and it uses the same runner.
5. **DOMAIN/ALPHABET boundary:** reflection acts on `t+1D` spatial support; scalar labels use identity action; oriented labels require an explicit typed involution.
6. **T06/T08 boundary:** blank preservation is an independent property; initial-condition classes are independent run profiles.
7. **Representation boundary:** 64 fixed rules, 160 reflection orbits, 88 combined orbits, code permutations, galleries, rasters, and BDDs are distinct codecs/analyses.
8. **Global theorem boundary:** rule fixedness gives covariance; symmetric trajectories additionally require compatible seed, realization, frontier/schedule, and observer.
9. **Counterexamples:** rules 30/86 and 29, hostile exterior, asymmetric seed, symmetric all-zero trace, one-sided schema, nontrivial output action, and diagonal two-component action close the main cheats.
10. **Global integration:** pending D120, plan/evidence/ledger/architecture-audit updates, and advancement to T08.
