# 23-T04-THREECOLOR-TOTALISTIC

Status: **REOPENED — ASSET REPAIR; ARCHITECTURE AUDIT COMPLETE**

Architecture authority: the T04 row and runner contract in `architecture-audit.md` supersede incompatible Goal 2 architecture below; the bounded asset repair remains independently open.

In addition to the bounded asset repair, the Goal 2 handoff is being reduced to a strict preset over the generic fixed-lattice local-rule construction.

## Current Facts

- Exact catalog row: T04, CSV line 5, `Three-Color Totalistic Cellular Automata`; taxonomy section 4 at `ref/notes/CA-Types.md:102-122` is vocabulary only.
- Architecture verdict: **T04 is exactly the strict T03 preset `k=3,r=1` with canonical alphabet/valuation `A_3=(0,1,2)`, `nu_3(i)=i`**. Substitution into T03 gives arity `q=3`, reachable sums `0..6`, table length `M=7`, rule count `R=3^7=2187`, and valid codes `0..2186`; strict text and the general count independently pin the same profile (`BOOK:772-776,11897`).
- Native identity is the seven-row structural table `U:{0,...,6}->A_3`. The optional code is `n=sum_{s=0}^6 nu_3(U(s))3^s`, with sum zero least significant. Exact source fixtures are code `777 -> (0,1,2,1,0,0,1)` (`BOOK:776`), code `867 -> (0,1,0,2,1,0,1)` (`BOOK:11168`), and code `420 -> (0,2,1,0,2,1,0)` (`BOOK:11918`).
- No three-color-only state, read, rule result, update, successor, or boundary exists. The Notes use the same direct range-`r` totalistic signature, sum lookup, padded codec, and common convolution framework (`BOOK:11056,11902,11904,11908,11910,11912,11914,11916`); D115-D118 therefore make T04 a strict preset over the T01/T02/T03 construction, not a fourth CA executor.
- White-background preservation is the separate T06 predicate `U(0)=0`, equivalently `n mod 3=0`, and selects `3^6=729` of the 2,187 programs. The page-76 scan is only the 50-code selection `993,996,...,1140`, not the whole restriction (`BOOK:784`). The single-gray start is a T08/run profile (`BOOK:790`).
- White/gray/black names and tones are presentation labels for semantic values `0/1/2`, not a required palette (`BOOK:774-776`). Reflection is derived from the equal-weight symmetric stencil, additivity is a separately proved property of examples such as code 420, and classes, gallery order, crop, horizon, raster, and emulations remain analyzer/view/relation data (`BOOK:784,7912,11918`).
- Fresh API inspection confirms partial structural fit but no executable T04 surface: `simple_programs.md:643-645,1768-1791` require fixed-arity reads and one old snapshot, while `simple_programs.md:1964-2032` conflates exact numeric sum with active count and color histogram. `src/ca/rules.py:198-217,262-295` records a loose aggregate channel but derives neither the seven cases nor the 2,187-rule range.
- Fresh runtime inspection confirms that the correct radius-one stencil already exists (`src/ca/neighborhoods.py:551-569`; `tests/test_neighborhoods.py:86-98`), but spatial rollout is family-whitelisted and binary decoded (`src/ca/rollout.py:145-212,643-682`), batch rule IDs are coerced to `numpy.int64` (`src/ca/rollout.py:264-274`), and the manifest parser accepts only named Phase 1 families (`src/ca/specs.py:117-181`). No current test constructs, validates, or evolves a three-color seven-row program (`tests/test_rules.py:9-45`; `tests/test_rollout.py:263-424`).
- T06's downstream reverse audit invalidated only T04's exhaustive asset-closure claim: retained `BOOK:17431` says `pictures below` but omits raster `BOOK:17433`, and retained `BOOK:2922` directly governs raster `BOOK:2924`, also omitted. The bounded source/asset/metadata/reverse-join repair is active. The strict three-color T03-preset semantics and D115-D118 remain unchanged.

## Updated Assumptions

- Replace the provisional hypothesis with the proved boundary: T04 is a discoverable, strictly validated constructor for one ordinary T03 specification, fixing `k=3`, `r=1`, and the explicit identity valuation over integer values `0,1,2`.
- The preset accepts exactly one complete seven-row table or one valid code. It does not accept overrides for `k`, `r`, valuation, aggregate, arity, code direction, output alphabet, executor, or update; callers needing other values use generic T03 or T05 rather than weakening T04 validation.
- Structural table identity remains primary and code remains a lossless relation. Leading zero rows are semantic, sum zero is least significant, and both table and code forms must resolve to the same shared T03 program identity.
- Program, run, selection, property, relation, and view identities remain disjoint: a T04 table/code is not a seed, initial/background value, boundary realization, T06 filter, T07 proof, T08 single-cell profile, class label, gallery subset/order, horizon, crop, palette, raster, or binary emulation.
- Canonical numeric values do not license palette inference. A caller may render `0,1,2` as white/gray/black or any other three distinct colors without changing the program reference; symbolic/noncanonical valuations belong to generic T03 and must remain explicit.
- T04 Goal 2 work depends on G2-T03's valuation, exact-sum descriptor, structural table/codec, shared executor, and stable program-reference migration. Implementing T04 first by exploiting its small code range would create a preset-only shim and is rejected.

## Big Picture Objective

Determine whether the emphasized three-color totalistic entry is exactly a strictly validated T03 preset, and close its complete source, gallery, seed/filter, code, API/runtime, and Goal 2 obligations without duplicate semantics.

## Catalog Identity

- Stable ID: T04.
- Exact CSV name: `Three-Color Totalistic Cellular Automata` at `ref/notes/CA-Types.csv:5`.
- Entry hypothesis: parameter preset and canonical evidence/profile bundle over T03, not a distinct executor or update law.
- Initial vocabulary: three-color/3-color totalistic, `k=3`, `r=1`, seven cases/sums, `2187`, base 3, white/gray/black, single gray cell, white background, rule/code `777`, `420`, `867`, `1329`, `1599`, `1635`, `1815`, `2049`, class galleries, symmetry, additivity, universality, emulation, and frequencies of classes.

## Search Log

Closed again for the bounded T06 asset repair. `BOOK` means `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`; its actual Index begins at physical `BOOK:20826`. Counts are distinct physical lines, not raw matches. Twelve controlled queries produce 162 unique monolith lines (145 pre-Index, 17 actual-Index). Eighty-four inspected asset, prose, and split-signature continuations produce an exact 246-candidate closure.

| Q | Search family | Pre-Index | Actual Index |
|---:|---|---:|---:|
| 01 | literal `three-color`, `3-color`, `three colors`, `three possible colors` | 42 | 6 |
| 02 | broad literal `totalistic` saturation, independently retained from T03 | 74 | 10 |
| 03 | strict `average color` / `average of ... colors` aliases | 6 | 0 |
| 04 | preset arithmetic/coding tokens `7,625,597,484,987`, `2187`, `3^7`, `7 cases`, `base 3` | 14 | 0 |
| 05 | exact `k=3,r=1` signatures within 80 characters | 12 | 0 |
| 06 | stable-white, single-gray, percentage, horizon, and long-continuation phrases | 7 | 0 |
| 07 | 87 strict/profile/class code numbers following literal `code` | 24 | 3 |
| 08 | `TotalisticCARule`, `ToTotalisticCARule`, assignment, implementation, and framework tokens | 6 | 0 |
| 09 | class/additivity/reversibility/irreducibility/universality/emulation property phrases | 7 | 0 |
| 10 | explicit lower/higher-color and range controls | 27 | 0 |
| 11 | actual-Index alias `of three colors by two` | 0 | 1 |
| 12 | non-totalistic three-color construction controls | 5 | 0 |

The zero is material: the emulation alias appears only in the actual Index; the main text instead describes blocks of three binary cells. Literal three-color candidates and broad totalistic reuse remain separate query families. Code `777` and the page-76 50-rule scan are raster text absent from the monolith OCR, so pinned asset lines are explicit inspected continuations rather than invented text hits.

### Exact reproducible manifest

```bash
python3 - <<'PY'
import re
from pathlib import Path

P=Path('ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md')
L=P.read_text().splitlines(); IX=20826
def xs(s): return [] if s=='-' else list(map(int,s.split(',')))

scan=list(range(993,1141,3))
gallery=[777,600,843,870,1086,1167,1329,1572,1815,1842,
         219,957,966,1884,237,420,948,1749,177,912,2040,
         1041,1635,2049,357,1599,2058]
other=[294,1893,867,438,792,924,1038,1380,1632,1659,1662,2007,2043]
codes=sorted(set(scan+gallery+other),reverse=True)

rows=[
(r'(?i)three[- ]color|3[- ]color|three possible colors|three colors',
 '772,774,776,780,784,790,796,800,804,808,824,846,1282,2806,2822,2852,3320,3324,3352,5218,5222,5482,5486,6340,7900,7912,8534,8544,8546,8560,8936,10395,10399,10411,11375,12055,15661,15972,18339,18476,18744,18877',
 '20846,20967,20972,21134,21683,21933'),
(r'(?i)totalistic',
 '772,774,776,784,790,796,800,804,808,824,834,846,1282,1954,2170,2802,2806,2822,2852,2868,2922,3902,3914,5638,6340,6644,7912,8320,8936,9166,10261,11037,11056,11060,11068,11070,11072,11168,11178,11509,11585,11625,11897,11902,11904,11908,11910,11912,11916,13536,13538,13547,13548,13549,13601,13613,13650,13654,13658,14223,14224,14239,14241,14632,15221,15301,15321,15359,15955,15959,16024,17431,18672,18748',
 '20965,20969,20972,20980,21233,21731,22030,22146,22352,22392'),
(r'(?i)average (?:color|of (?:the previous colors|cells in its neighborhood))',
 '774,776,2170,5082,5088,8320','-'),
(r'7,625,597,484,987|2187|3\^7|7 cases|base 3',
 '772,774,776,1282,1419,1427,3352,5218,10411,11897,17139,17874,18850,20577','-'),
(r'(?i)k\s*=\s*3.{0,80}?r\s*=\s*1(?![0-9/])',
 '11164,11168,11897,15493,16020,16024,16025,16027,18348,18748,20573,20577','-'),
(r'(?i)those that change the white background are not included|single gray cell|About 85% of all three-color|following pages continue these patterns for 3000 steps|edge between growth and extinction|after a total of 8282 steps|Nine thousand steps in the evolution of the three-color',
 '784,790,808,810,838,840,846','-'),
(r'(?i)code(?: number)?\s+(?:'+'|'.join(map(str,codes))+r')(?![0-9])',
 '790,800,806,828,832,838,846,2826,2830,2838,3320,3324,3348,3352,3356,3360,3364,3370,3374,3378,7912,11168,11918,14827',
 '20980,21223,21471'),
(r'TotalisticCARule|ToTotalisticCARule|specific assignment of values to colors|Implementation of totalistic cellular automata|totalistic rules in the same framework',
 '11897,11902,11904,11908,11912,11916','-'),
(r'(?i)Class 4 rules.{0,120}totalistic rules.{0,80}k.{0,10}3|Frequencies of classes.{0,120}1D totalistic|Code 420 is an example of an additive rule|no non-trivial totalistic rule|totalistic cellular automata can be universal|cellular automata shown here all have 3-color totalistic rules|three-color rule illustrated here is totalistic code 1599',
 '7912,8936,11918,14223,14224,16024,18748','-'),
(r'(?i)(?:two|2|four|4|five|5) (?:possible )?colors.{0,180}totalistic|totalistic.{0,180}(?:two|2|four|4|five|5) (?:possible )?colors|k\s*=\s*(?:2|4|5).{0,80}?r\s*=\s*(?:1|2)(?![0-9/])',
 '1282,2802,2868,11050,11509,11585,11625,11897,11919,14392,14394,14541,14673,14675,16020,16024,16025,16027,16049,16129,16157,16448,18672,18748,20590,20592,20600','-'),
(r'(?i)emulat.{0,120}(?:three colors|three-color)|(?:three colors|three-color).{0,120}emulat|encoding of three colors by two|of three colors by two',
 '-','21134'),
(r'(?i)7,625,597,484,987 cellular automata|general k=3, r=1 rule|reversible cellular automata with three colors|Block cellular automata with three possible colors|rules with three colors that achieve the purpose',
 '5218,5222,5486,10411,11164','-'),
]

sets=[]
for q,(pat,pre_s,idx_s) in enumerate(rows,1):
    found=[i for i,s in enumerate(L,1) if re.search(pat,s)]
    pre=[i for i in found if i<IX]; idx=[i for i in found if i>=IX]
    assert pre==xs(pre_s),(q,pre,xs(pre_s))
    assert idx==xs(idx_s),(q,idx,xs(idx_s))
    sets.append(set(found))

# Raster links and immediate continuations whose evidence is absent from,
# or split across, the controlled text hit lines.
follow={764,778,782,788,792,794,798,802,818,820,822,826,830,836,842,844,858,860,
        1280,1958,2172,
        2800,2804,2824,2828,2832,2834,2836,2844,2846,2848,2850,2866,
        3314,3316,3318,3322,3328,3334,3342,3350,3362,3368,3372,3376,3380,
        5220,5484,10393,10409,
        2920,2924,2928,6336,6338,6642,7910,8306,8934,9164,
        11069,11071,11166,11170,11176,11182,11297,11301,11303,11305,11307,
        11627,11629,11914,13540,14226,14228,14230,14232,
        14829,14831,14833,17433,18746}
assets={
764:'![](_page_74_Picture_5.jpeg)',
778:'![](_page_75_Figure_6.jpeg)',782:'![](_page_76_Figure_2.jpeg)',
792:'![](_page_77_Figure_6.jpeg)',794:'![](_page_78_Figure_2.jpeg)',
798:'![](_page_78_Figure_4.jpeg)',802:'![](_page_79_Picture_2.jpeg)',
818:'![](_page_81_Picture_1.jpeg)',820:'![](_page_81_Picture_2.jpeg)',
822:'![](_page_81_Picture_3.jpeg)',826:'![](_page_82_Picture_1.jpeg)',
830:'![](_page_83_Picture_1.jpeg)',836:'![](_page_84_Picture_2.jpeg)',
844:'![](_page_85_Picture_2.jpeg)',
858:'![](_page_86_Picture_7.jpeg)',860:'![](_page_86_Picture_8.jpeg)',
1280:'![](_page_122_Figure_2.jpeg)',1958:'![](_page_171_Picture_5.jpeg)',
2172:'![](_page_185_Picture_9.jpeg)',
2800:'![](_page_248_Figure_2.jpeg)',2804:'![](_page_249_Picture_1.jpeg)',
2824:'![](_page_251_Picture_1.jpeg)',2828:'![](_page_252_Picture_2.jpeg)',
2832:'![](_page_253_Picture_1.jpeg)',2836:'![](_page_254_Picture_1.jpeg)',
2844:'![](_page_255_Picture_2.jpeg)',2846:'![](_page_255_Picture_3.jpeg)',
2848:'![](_page_255_Picture_4.jpeg)',2850:'![](_page_255_Picture_5.jpeg)',
2866:'![](_page_256_Figure_2.jpeg)',
2920:'![](_page_261_Figure_2.jpeg)',2924:'![](_page_262_Figure_2.jpeg)',
2928:'![](_page_263_Figure_2.jpeg)',
3314:'![](_page_297_Picture_2.jpeg)',3318:'![](_page_297_Picture_4.jpeg)',
3322:'![](_page_297_Picture_6.jpeg)',3350:'![](_page_301_Picture_2.jpeg)',
3362:'![](_page_302_Picture_3.jpeg)',3368:'![](_page_303_Picture_2.jpeg)',
3376:'![](_page_304_Picture_2.jpeg)',11297:'![](_page_885_Picture_21.jpeg)',
3328:'![](_page_298_Figure_2.jpeg)',3334:'![](_page_299_Picture_3.jpeg)',
3342:'![](_page_300_Figure_1.jpeg)',3380:'![](_page_305_Picture_2.jpeg)',
6336:'![](_page_541_Picture_3.jpeg)',6338:'![](_page_541_Picture_4.jpeg)',
6642:'![](_page_566_Figure_2.jpeg)',7910:'![](_page_670_Figure_1.jpeg)',
8306:'![](_page_707_Figure_1.jpeg)',8934:'![](_page_753_Picture_3.jpeg)',
9164:'![](_page_769_Figure_1.jpeg)',
11166:'![](_page_883_Picture_23.jpeg)',11170:'![](_page_883_Picture_25.jpeg)',
11176:'![](_page_883_Picture_28.jpeg)',11182:'![](_page_883_Picture_31.jpeg)',
11301:'![](_page_885_Picture_23.jpeg)',11303:'![](_page_885_Picture_24.jpeg)',
11305:'![](_page_885_Picture_25.jpeg)',11307:'![](_page_885_Picture_26.jpeg)',
11627:'![](_page_897_Picture_19.jpeg)',11629:'![](_page_897_Picture_20.jpeg)',
14226:'![](_page_963_Picture_8.jpeg)',14228:'![](_page_963_Picture_9.jpeg)',
14230:'![](_page_963_Picture_10.jpeg)',14232:'![](_page_963_Picture_11.jpeg)',
14829:'![](_page_980_Picture_15.jpeg)',14831:'![](_page_980_Picture_16.jpeg)',
14833:'![](_page_980_Picture_17.jpeg)',17433:'![](_page_1092_Picture_6.jpeg)',
18746:'![](_page_1132_Picture_2.jpeg)',
}
assets.update({5220:'![](_page_451_Picture_6.jpeg)',5484:'![](_page_476_Figure_3.jpeg)',
               10393:'![](_page_847_Figure_1.jpeg)',10409:'![](_page_848_Figure_2.jpeg)'})
for n,want in assets.items(): assert L[n-1]==want,(n,L[n-1])
assert len(assets)==75
assert L[787].startswith('Using more complicated rules may be convenient')
assert L[841].startswith('<sup>◀</sup> Three thousand steps')
assert L[2833]=='238' # page/footer contamination; official/raster code is 1659
assert L[3315]=='2 colors, next-nearest neighbors, code 20'
assert L[3371]=='initial condition number 54,889'
assert r'\{0, 1, 0\}, \{1, 1, 1\}, \{0, 1, 0\}' in L[11068]
assert r'\{0, k, 0\}, \{k, 1, k\}, \{0, k, 0\}' in L[11070]
assert L[11913].startswith('■ Common framework.')
assert L[13539].startswith('Apply[Plus, 2 ^ Join')

parts={
'strict':'772,774,776,778,780,782,784,788,790,792,794,796,798,800,802,804,806,808,810,818,820,822,824,826,828,830,832,834,836,838,840,842,844,846',
'preset_relation':'1280,1282,2804,2806,2822,2824,2826,2828,2830,2832,2836,2838,2844,2846,2848,2850,2852,3318,3320,3322,3324,3348,3350,3352,3356,3360,3362,3364,3368,3370,3372,3374,3376,3378,6336,6338,6340,7900,7912,8306,8934,8936,11168,11170,11897,11918,14223,14224,14232,14827,16024,18348,18748',
'parent':'8320,11037,11056,11060,11902,11904,11908,11910,11912,11914,11916',
'adjacent_totalistic':'2800,2802,2866,2868,3314,3316,3328,3334,3342,9164,9166,11509,11585,11625,11627,11629,14226,14228,14230,18672',
'sibling_application':'1954,1958,2170,2172,2920,2922,2924,2928,3902,3914,5082,5088,5638,6642,6644,7910,10261,11068,11069,11070,11071,11072,11178,11182,11297,11301,11303,11305,11307,13536,13538,13540,13547,13548,13549,13601,13613,13650,13654,13658,14239,14241,14632,14829,14831,14833,15221,15301,15321,15359,15955,15959,17431,17433',
'non_totalistic':'764,858,860,3380,5218,5220,5222,5482,5484,5486,8534,8544,8546,8560,10393,10395,10399,10409,10411,11164,11166,11176,12055,15661,15972,18339,18476,18744,18746,18877',
'false_control':'1419,1427,2834,11050,11375,11919,14392,14394,14541,14673,14675,15493,16020,16025,16027,16049,16129,16157,16448,17139,17874,18850,20573,20577,20590,20592,20600',
'index':'20846,20965,20967,20969,20972,20980,21134,21223,21233,21471,21683,21731,21933,22030,22146,22352,22392',
}
partition={k:xs(v) for k,v in parts.items()}
queried=set().union(*sets); union=queried|follow
flat=[i for v in partition.values() for i in v]
assert len(rows)==12 and len(queried)==162 and len(union)==246
assert len(flat)==len(set(flat))==246 and set(flat)==union
assert [len(partition[k]) for k in partition]==[34,53,11,20,54,30,27,17]

# Mechanical join: every physical asset link in this source manifest must
# be exactly one item in the independent 75-item metadata oracle below.
stage=Path('goal-1/23-T04-THREECOLOR-TOTALISTIC.md').read_text()
asset_audit=stage.split('## Asset and Raster Audit',1)[1]
items_src=asset_audit.split('\nitems={',1)[1].split('\n}\n\ndef jpeg_size',1)[0]
ledger_paths=set(re.findall(r"'([^']+\.jpeg)':\(",items_src))
manifest_names={re.fullmatch(r'!\[\]\(([^)]+)\)',v).group(1) for v in assets.values()}
assert len(ledger_paths)==len(manifest_names)==75
assert {Path(p).name for p in ledger_paths}==manifest_names

# Every physical asset has exactly the monolith link and one split-corpus link.
# This direction-sensitive reverse audit follows the explicit same-kind bridge
# through BOOK:2926/2928/2930, then stops before the page-264 Life construction.
root=Path('ref/A-New-Kind-of-Science')
refs={name:[] for name in manifest_names}
for md in root.rglob('*.md'):
    for line_no,line in enumerate(md.read_text().splitlines(),1):
        for name in manifest_names:
            if re.fullmatch(r'!\[\]\((?:Images/)?'+re.escape(name)+r'\)',line):
                refs[name].append((md.relative_to(root).as_posix(),line_no))
assert all(len(v)==2 for v in refs.values())
assert sum(map(len,refs.values()))==150
assert refs['_page_262_Figure_2.jpeg']==[
 ('A-New-Kind-of-Science.md',2924),
 ('CHAPTERS/6-Starting-from-Randomness/Starting-from-Randomness.md',221)]
assert refs['_page_263_Figure_2.jpeg']==[
 ('A-New-Kind-of-Science.md',2928),
 ('CHAPTERS/6-Starting-from-Randomness/Starting-from-Randomness.md',225)]
assert refs['_page_1092_Picture_6.jpeg']==[
 ('A-New-Kind-of-Science.md',17433),('BACK-MATTER/Index/Index.md',5336)]

# Exact split-corpus saturation for the two core lexical families.
root=Path('ref/A-New-Kind-of-Science')
split_totalistic={
'CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md':'89,91,93,101,107,113,117,121,125,141,151,163,599',
'CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md':'411',
'CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md':'27',
'CHAPTERS/6-Starting-from-Randomness/Starting-from-Randomness.md':'101,105,121,149,165,219',
'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Mechanisms-in-Programs-and-Nature.md':'479,491',
'CHAPTERS/9-Fundamental-Physics/Fundamental-Physics.md':'473,1169',
'CHAPTERS/10-Processes-of-Perception-and-Analysis/Processes-of-Perception-and-Analysis.md':'57',
'CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md':'211,603',
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md':'319,549,1642,2418,2437,2441,2449,2451,2453,2549,2559,2890,2966,3006,3278,3283,3285,3289,3291,3293,3297',
'BACK-MATTER/Index/Index.md':'1437,1439,1448,1449,1450,1502,1514,1551,1555,1559,2124,2125,2140,2142,2533,3122,3202,3222,3260,3856,3860,3925,5334',
'BACK-MATTER/Colophon/Colophon.md':'1229,1305,3522,3526,3529,3537,3790,4288,4587,4703,4909,4949',
}
split_three={
'BACK-MATTER/Colophon/Colophon.md':'896,1033,1301,1434,3403,3524,3529,3691,4240,4490',
'BACK-MATTER/Index/Index.md':'3562,3873',
'CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md':'199,211,803,813,825',
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md':'319,1776,1780,1792,2756,3436',
'CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md':'89,91,93,97,101,107,113,117,121,125,141,163,599',
'CHAPTERS/6-Starting-from-Randomness/Starting-from-Randomness.md':'105,121,149,615,619,647',
'CHAPTERS/9-Fundamental-Physics/Fundamental-Physics.md':'53,57,317,321,1169',
}
for mapping,pat in ((split_totalistic,r'(?i)totalistic'),
                    (split_three,r'(?i)three[- ]color|3[- ]color|three possible colors|three colors')):
    for rel,want in mapping.items():
        lines=(root/rel).read_text().splitlines()
        got=[i for i,s in enumerate(lines,1) if re.search(pat,s)]
        assert got==xs(want),(rel,got,xs(want))
assert sum(len(xs(v)) for v in split_totalistic.values())==84
assert sum(len(xs(v)) for v in split_three.values())==47
print('T04 source manifest: PASS 12 queries; 246 candidates; partition=34,53,11,20,54,30,27,17; assets=75; refs=150; splits=84/47')
PY
```

Expected terminal line:

```text
T04 source manifest: PASS 12 queries; 246 candidates; partition=34,53,11,20,54,30,27,17; assets=75; refs=150; splits=84/47
```

### Complete disjoint disposition

- **Strict preset and gallery (34):** `772,774,776,778,780,782,784,788,790,792,794,796,798,800,802,804,806,808,810,818,820,822,824,826,828,830,832,834,836,838,840,842,844,846`. This is the complete Chapter 3 strict run: definition, code-777 rule figure, 50-rule page-76 scan, behavior galleries, captions, standalone continuation labels, seed/filter conventions, horizons, and the 1599 resolution. Asset links are candidates because most code labels exist only in their pixels.
- **T04 preset profiles, properties, and relations (53):** `1280,1282,2804,2806,2822,2824,2826,2828,2830,2832,2836,2838,2844,2846,2848,2850,2852,3318,3320,3322,3324,3348,3350,3352,3356,3360,3362,3364,3368,3370,3372,3374,3376,3378,6336,6338,6340,7900,7912,8306,8934,8936,11168,11170,11897,11918,14223,14224,14232,14827,16024,18348,18748`. These close exact counts, the complete linked three-color/class/borderline asset chain, every linked code-357/1329 structure/growth raster, mixed-rule comparisons, random-background views, the runnable code-867 example, class frequency, additivity, irreducibility, emulation, reversibility, and universality. They are profile/run/property evidence over the same preset, not extra successor mechanics.
- **Parent T03 construction and alias reuse (11):** `8320,11037,11056,11060,11902,11904,11908,11910,11912,11914,11916`. These give the generic average alias, symbolic signatures, aggregate lookup, codec, and shared framework. T04 specializes them with data; it does not duplicate them.
- **Adjacent lower/higher-color totalistic controls (20):** `2800,2802,2866,2868,3314,3316,3328,3334,3342,9164,9166,11509,11585,11625,11627,11629,14226,14228,14230,18672`. These are binary range-two, four-color, and other neighboring totalistic profiles, including directly linked code-20 enumeration/structure rasters and lower/higher-color frequency comparators. They prove the T03/T05 boundary and do not enter the T04 preset.
- **Sibling geometry or application (54):** `1954,1958,2170,2172,2920,2922,2924,2928,3902,3914,5082,5088,5638,6642,6644,7910,10261,11068,11069,11070,11071,11072,11178,11182,11297,11301,11303,11305,11307,13536,13538,13540,13547,13548,13549,13601,13613,13650,13654,13658,14239,14241,14632,14829,14831,14833,15221,15301,15321,15359,15955,15959,17431,17433`. These are continuous, two-dimensional, outer/growth/weighted, block-emulation, network, tiling, feature-extraction, additive-mod-3, post-Pascal modulo-2 comparisons, Life-analogy, and other application constructions. `2924` is the direct two-dimensional gallery raster governed by `2922`; `2928` is the same six-rule gallery's one-dimensional slice view governed by `2926,2930`; `17433` is the direct feature-extraction raster governed by `17431`. They bound the preset without changing its one-dimensional equal-weight rule.
- **Non-totalistic three-color controls (30):** `764,858,860,3380,5218,5220,5222,5482,5484,5486,8534,8544,8546,8560,10393,10395,10399,10409,10411,11164,11166,11176,12055,15661,15972,18339,18476,18744,18746,18877`. These are unrestricted, mobile, reversible, block, elementary-rule-110, Turing-machine, fracture, reaction-diffusion, tag-system, purpose-search, general-rule, or 3-color 2-neighbor examples. The four added rasters are the directly linked views governed by E14's reversible, block-conservation, and purpose-search captions. Matching “three colors” or asset adjacency is not enough to make them T04.
- **False/query controls (27):** `1419,1427,2834,11050,11375,11919,14392,14394,14541,14673,14675,15493,16020,16025,16027,16049,16129,16157,16448,17139,17874,18850,20573,20577,20590,20592,20600`. These are unrelated base-3 arithmetic, mosaic history, general/additive/reversible/search `k,r` contexts, plus the page-number artifact `238` at `BOOK:2834`. They contain no T04 construction.
- **Actual-Index routes (17):** `20846,20965,20967,20969,20972,20980,21134,21223,21233,21471,21683,21731,21933,22030,22146,22352,22392`. They route to already audited strict, Notes, property, sibling, or control material and add no mechanics.

There is zero silent remainder: the eight sets are pairwise disjoint and their union is the exact 246-candidate manifest.

### Strict gallery and asset closure

The strict asset sequence is complete and ordered by the 13 pinned monolith links:

| BOOK link | Strict asset | Visible semantic labels |
|---:|---|---|
| `778` | `_page_75_Figure_6.jpeg` | high-to-low digits `1,0,0,1,2,1,0`, `= 777` |
| `782` | `_page_76_Figure_2.jpeg` | exactly 50 codes: `993,996,...,1140` (step 3) |
| `792` | `_page_77_Figure_6.jpeg` | `600,843,870,1086,1167,1329,1572,1815,1842` |
| `794` | `_page_78_Figure_2.jpeg` | `219,957,966,1884` |
| `798` | `_page_78_Figure_4.jpeg` | `237,420,948,1749` |
| `802` | `_page_79_Picture_2.jpeg` | `177,912,2040` |
| `818,820,822` | three `_page_81_Picture_*.jpeg` files | `1041,1635,2049` |
| `826,830` | `_page_82_Picture_1.jpeg`, `_page_83_Picture_1.jpeg` | long continuations of `1635`, `2049` |
| `836` | `_page_84_Picture_2.jpeg` | `357,600,1599,2058` |
| `844` | `_page_85_Picture_2.jpeg` | three 3000-step columns for `1599` |

The page-76 scan is a display sample, not the preset catalog: all 50 codes are divisible by 3, so their least-significant ternary digit (the sum-zero/white-background output) is zero. This exactly realizes the caption's stable-white selection, but it is only 50 of the 729 T04 codes with a stable zero background, not all 2187 rules and not even all stable-background rules. The later galleries reuse codes across behavior views; repeated labels are not new programs.

The asset-scope rule is exact: include every local raster directly linked by a dispositioned T04 definition/gallery/property line or required to interpret its named relation, then retain its immediately adjacent/downstream comparator rasters as explicit controls. Applying that rule adds 62 pinned assets beyond the 13-image strict run. The first 31 are the original continuation closure:

| BOOK link | Asset | Geometry | SHA-256 | Disposition |
|---:|---|---:|---|---|
| `2800` | Chapter 6 `_page_248_Figure_2.jpeg` | `1086x1389` | `b2a20cb8095eb211fedd963d622222ca98fe0428f397b71bef90db8fa6871957` | adjacent binary range-two totalistic gallery control |
| `2804` | Chapter 6 `_page_249_Picture_1.jpeg` | `1082x1403` | `f7b2834be41656cff9512b7affdd5fa57640bbbb6ecd93da1440202bf113f7ef` | T04 sequence, exactly codes `1002..1095` step 3 |
| `2824` | Chapter 6 `_page_251_Picture_1.jpeg` | `1123x1383` | `41cfc762284fdcd65e5663fb7631aa4c504aea46a746a8a4ed24407b76b89196` | T04 class-4 code 1815 |
| `2828` | Chapter 6 `_page_252_Picture_2.jpeg` | `1121x1377` | `120e95a57f683744ff3e71981f4fa07ff850d0cad5633bf4d2f27906a76e909f` | T04 class-4 code 2007 |
| `2832` | Chapter 6 `_page_253_Picture_1.jpeg` | `1227x1519` | `148a433a11b4889c91c1a7be3c6f00172a3961428e6d41c47a06954136245faf` | T04 class-4 code 1659; repairs monolith `238` contamination |
| `2836` | Chapter 6 `_page_254_Picture_1.jpeg` | `1117x1383` | `d32b7fc3dedc9f262e5a3d3d928d1d7d94d1a219fd75aeeefdb988c74869a168` | T04 class-4 code 2043 |
| `2844` | Chapter 6 `_page_255_Picture_2.jpeg` | `273x171` | `b175f64e60cf41042d8ba6a11ed8d04eec4a8101bef8f9f231aae532eca6ca06` | T04 borderline code 219 |
| `2846` | Chapter 6 `_page_255_Picture_3.jpeg` | `259x167` | `00ef0063254d4f75734cd76d8f2d07de4ae1d6b041b9664197c2da99641d8b14` | T04 borderline code 438 |
| `2848` | Chapter 6 `_page_255_Picture_4.jpeg` | `267x186` | `700d71a0beb145c953ca87f4d8649aecd7b7d60df69ccd569cba02f6daeb1acc` | T04 borderline code 1380 |
| `2850` | Chapter 6 `_page_255_Picture_5.jpeg` | `273x165` | `ae44e4411841a03fced5b5114f6cef4be62793c6a58c9a4ce6c357d214c7ce35` | T04 borderline code 1632 |
| `2866` | Chapter 6 `_page_256_Figure_2.jpeg` | `1092x1367` | `1c4967f6967d8e813b2a281e2615dc8bef272eb57789b60e23c950de5e6bc01f` | adjacent four-color totalistic gallery control |
| `3314` | Chapter 6 `_page_297_Picture_2.jpeg` | `1111x408` | `953c15d2e64464aceadb6181639cf36973db9513d6e0b7fc3fb43564efc65be8` | adjacent binary range-two code-20 control |
| `3328` | Chapter 6 `_page_298_Figure_2.jpeg` | `1159x1297` | `7cacf2667a3f923d35106ec7eff09b9ce551d79dd828f8661458dd121bda09df` | downstream binary code-20 initial-condition enumeration control |
| `3334` | Chapter 6 `_page_299_Picture_3.jpeg` | `1150x600` | `32d4ed4b16a083fb731c37cc80c64efb9995756808c316a0ced0dea0e9bd5475` | downstream binary code-20 structures control |
| `3342` | Chapter 6 `_page_300_Figure_1.jpeg` | `1150x1192` | `ee5ea91d3855bf31bd793f02677c0c19d9203ac20532b3b7bb07df838065294c` | downstream binary code-20 exhaustive-period control |
| `3318` | Chapter 6 `_page_297_Picture_4.jpeg` | `1127x415` | `26b299987a91daf8d15fc226c845c7efa7d55b9aa4221a4e6d41646b8c384204` | code-357 class-4 overview |
| `3322` | Chapter 6 `_page_297_Picture_6.jpeg` | `1123x408` | `b94ac983e3496b023a1a991b15a701de9a1c4c5cba75a84b16254c497a1c76f1` | code-1329 class-4 overview |
| `3350` | Chapter 6 `_page_301_Picture_2.jpeg` | `906x699` | `3e9aec2832697e07ea20391c1454e022bc8578fcfb4c126bbb53e6fdfe3f6eb3` | six code-357 structure examples with initial-condition/period labels |
| `3362` | Chapter 6 `_page_302_Picture_3.jpeg` | `1036x712` | `4ec6db32d4f0b659a8519110b7885e05487e68d0348b390323daa55e7b322fd1` | nine code-1329 structure examples with initial-condition/period labels |
| `3368` | Chapter 6 `_page_303_Picture_2.jpeg` | `616x1053` | `26ec2731176f7ef4b471b4f395f3968eefa69e0eba88a3f672268129d68e07aa` | code-1329 unbounded growth, initial condition 54,889 |
| `3376` | Chapter 6 `_page_304_Picture_2.jpeg` | `1109x1363` | `21cc5432bcfcc379619d43c076f3102a3e12d64cd724d9fe5709055b72874ecf` | five code-1329 growth examples: initial conditions 54,889; 97,439; 166,426; 115,396; 2,069,116 |
| `3380` | Chapter 6 `_page_305_Picture_2.jpeg` | `1184x1342` | `7e75ba3d0cb57a0b35d5a7b29e803386617e1ede22eefae19ce6e21fc465a9c9` | downstream elementary-rule-110 random-background control |
| `11297` | Chapter 12 `_page_885_Picture_21.jpeg` | `583x225` | `5f829c7776b53963e578df5a783553320da171c4e1c4d92c470899ec5bb3e40d` | related additive `Mod[left+right,3]` Pascal pattern; not native code-420 execution |
| `11301` | Chapter 12 `_page_885_Picture_23.jpeg` | `139x141` | `f14931f6bb008435e34961947dce7b11d5ec6d0bd4cc5b936bcee81b830adc0a` | post-Pascal modulo-2 integer-function control |
| `11303` | Chapter 12 `_page_885_Picture_24.jpeg` | `135x138` | `5b302ed9d6c9cbee590270c7bdc169b62b554b0e186a94fdb3d1952a69c0f8c5` | post-Pascal modulo-2 integer-function control |
| `11305` | Chapter 12 `_page_885_Picture_25.jpeg` | `138x145` | `f5eb9593ba90b4b240dc6990bb0e7204066cc48e81e82b96186029ff866d40da` | post-Pascal modulo-2 integer-function control |
| `11307` | Chapter 12 `_page_885_Picture_26.jpeg` | `135x155` | `badba07cc053bdf7f4e5b41d7d90b2b248d8acd75b9728898e10c69a59c7ceec` | post-Pascal modulo-2 integer-function control |
| `14829` | Notes `_page_980_Picture_15.jpeg` | `160x195` | `641317f32d429dd61b8353e1ebe65bd80f30950df78f0ebdc3a7f99b6bd26cd9` | 2D Life “spacefiller” view, relation-only analogy to code 1329 |
| `14831` | Notes `_page_980_Picture_16.jpeg` | `172x187` | `90df3d1e1e99ed74dd1844654ff41b04b23f6fe22552cefa2b72f659cd0c5fda` | 2D Life “spacefiller” view, relation-only analogy to code 1329 |
| `14833` | Notes `_page_980_Picture_17.jpeg` | `223x207` | `3ad70eb7f740edf7749700ff107f08306830f3e3fd617f2df3f9e7e559178e21` | 2D Life “spacefiller” view, relation-only analogy to code 1329 |
| `18746` | Notes `_page_1132_Picture_2.jpeg` | `606x308` | `422ce8c21c465e2ffdffdb0f691f9521a21b9389897336dd4e4a2c716295c589` | unrestricted 3-color 2-neighbor rule 2144 control adjacent to universality Notes |

The independent metadata and reverse-link joins contribute the remaining 31 links. This table is the human-readable form of the exact set-equality assertion in the manifest; `I`, `R`, and `X` agree with the metadata oracle's included, relation-only, and excluded/control classes.

| BOOK link(s) | Asset(s) | Ledger class | Source role |
|---:|---|:---:|---|
| `1280` | Chapter 3 `_page_122_Figure_2.jpeg` | I | mixed-color comparison whose T04 column is codes `578..585` |
| `6336,6338` | Chapter 9 `_page_541_Picture_3.jpeg`, `_page_541_Picture_4.jpeg` | I | codes `294` and `1893` on random backgrounds |
| `8306` | Chapter 11 `_page_707_Figure_1.jpeg` | I | mixed class-4 comparison containing T04 code `1815` |
| `8934` | Chapter 12 `_page_753_Picture_3.jpeg` | I | codes `870,843,1599` in the reducibility comparison |
| `11170` | Chapter 12 `_page_883_Picture_25.jpeg` | I | exact code-`867` Notes invocation output |
| `14232` | Index `_page_963_Picture_11.jpeg` | I | `k=3,r=1` class-frequency chart |
| `7910` | Chapter 11 `_page_670_Figure_1.jpeg` | R | block-emulation relation for code `1599` |
| `764` | Chapter 3 `_page_74_Picture_5.jpeg` | X | elementary-rule-73 comparator |
| `858,860` | Chapter 3 `_page_86_Picture_7.jpeg`, `_page_86_Picture_8.jpeg` | X | mobile-rule comparator and diagram |
| `1958` | Chapter 4 `_page_171_Picture_5.jpeg` | X | continuous-system analog |
| `2172` | Chapter 5 `_page_185_Picture_9.jpeg` | X | two-dimensional form |
| `2920` | Chapter 6 `_page_261_Figure_2.jpeg` | X | two-dimensional totalistic gallery |
| `2924` | Chapter 6 `_page_262_Figure_2.jpeg` | X | direct continuation of the two-dimensional five-cell binary totalistic gallery; geometry/color-count control |
| `2928` | Chapter 6 `_page_263_Figure_2.jpeg` | X | one-dimensional slices of the same six-rule gallery (`4,12,24,38,30,52`); observer/geometry control |
| `6642` | Chapter 10 `_page_566_Figure_2.jpeg` | X | two-dimensional outer-totalistic codes `54,222,374` |
| `9164` | Chapter 12 `_page_769_Figure_1.jpeg` | X | four-color totalistic code `1004600` |
| `11166,11176,11182` | Chapter 12 `_page_883_Picture_23.jpeg`, `_page_883_Picture_28.jpeg`, `_page_883_Picture_31.jpeg` | X | general ordered `k=3,r=1`, callback-rule, and 2D nine-neighbor totalistic controls |
| `11627,11629` | Chapter 12 `_page_897_Picture_19.jpeg`, `_page_897_Picture_20.jpeg` | X | binary radius-two code-`10` controls |
| `14226,14228,14230` | Index `_page_963_Picture_8.jpeg`, `_page_963_Picture_9.jpeg`, `_page_963_Picture_10.jpeg` | X | lower-color/range class-frequency controls |
| `5220,5484` | Chapter 9 `_page_451_Picture_6.jpeg`, `_page_476_Figure_3.jpeg` | X | reversible three-color and conserved three-color block-rule controls governed by E14 captions |
| `10393,10409` | Chapter 12 `_page_847_Figure_1.jpeg`, `_page_848_Figure_2.jpeg` | X | three-color purpose-search controls governed by E14 captions |
| `17433` | Index `_page_1092_Picture_6.jpeg` | R | feature-extraction application of the 16 even-numbered binary five-neighbor totalistic rules governed by `BOOK:17431` |

The Chapter 6 class chain contains pictured codes `1815,2007,1659,2043` and borderline codes `219,438,1380,1632`; Notes code `1662` is a distinct, unpictured class-4 example. The six code-357/1329 property rasters contain initial-condition and repetition annotations, not additional rule rows. The additive modulo-3 picture is explicitly a related generalization of rule 90, the three Life pictures are two-dimensional analogies, and rule 2144 has a two-cell rather than three-cell neighborhood; all remain outside native T04 execution.

The controlled union deliberately retains all of those downstream links. `BOOK:3328,3334,3342` remain binary code-20 controls; `BOOK:3380` is identified by `BOOK:3382` as elementary rule 110, not code 1329; and `BOOK:11301,11303,11305,11307` are identified by `BOOK:11309` as other integer functions reduced modulo 2, not further views of the three-color additive rule. Their inclusion makes the asset continuation closure auditable without broadening T04.

### Actual-Index route closure

| Actual Index | Exact route(s) | Disposition |
|---:|---|---|
| `20846` | additive cellular automata with 3 colors, page 886 | code-420 property Notes at `BOOK:11918` |
| `20965` | implementation of totalistic, page 886 | generic parent implementation at `BOOK:11902-11916` |
| `20967` | cellular automata, three-color, page 60 | strict T04 at `BOOK:772-846` |
| `20969` | totalistic; weighted totalistic, page 427 | strict parent; weighted sibling at `BOOK:5082,5088` |
| `20972` | class 4 in 3-color totalistic CAs, page 948 | class/property Notes at `BOOK:14223-14224` |
| `20980` | 22 named routes from codes 177 through 2058, including code 1659 at page 238 | strict/profile examples already closed; code 867 routes to the runnable Notes example |
| `21134` | encoding of three colors by two, pages 655, 1111 | emulation relation at `BOOK:7900,7912,18348` |
| `21223` | glider gun in code 1329, page 288 | persistent-structure profile at `BOOK:3360-3378` |
| `21233` | growth totalistic rules, page 928 | two-dimensional sibling |
| `21471` | localized structures in code 357/code 1329, pages 286/287 | T04 property/run profiles at `BOOK:3348-3378` |
| `21683` | networks of CA emulations, page 1118 | emulation/application relation |
| `21731` | outer totalistic rules | two-dimensional sibling |
| `21933` | reversible cellular automata, three-color, page 436 | non-totalistic control plus totalistic non-reversibility at `BOOK:16024` |
| `22030` | totalistic page 60; growth totalistic page 928 | strict parent plus growth sibling |
| `22146` | Sum (totalistic) rules, page 60 | confirms exact-sum alias |
| `22352` | Totalistic cellular automata, pages 60/170/886/1017 | strict, sibling, implementation, and property routes already closed |
| `22392` | universality in totalistic cellular automata, page 693 | property relation at `BOOK:18748` |

### Split routing

- The broad `totalistic` family has exactly 84 split-file hits, and the literal three-/3-color family has exactly 47; both lists are pinned in the manifest. Strict `BOOK:772,774,776,780,784,790,796,800,804,808,824,846` map to Chapter 3 split `89,91,93,97,101,107,113,117,121,125,141,163`.
- `BACK-MATTER/Index/Index.md` is misrouted Notes, not the actual Index. The real split Index begins at `BACK-MATTER/Colophon/Colophon.md:3383`; canonical monolith physical lines remain primary.

## Book Excerpts

All verbatim monolith material is in blockquotes so the oracle below can check every fragment against its cited physical line.

### E1 — Strict preset definition, valuation, aggregate, and codec

- Provenance: `BOOK:772,774,776`.
- Establishes: the emphasized entry is the totalistic restriction of unrestricted three-color nearest-neighbor rules; states are assigned values `0,1,2`; the aggregate covers self plus immediate neighbors; seven average/sum cases are encoded as base-3 digits with sum zero at the rightmost/least-significant end.

> The 256 "elementary" rules that we have discussed so far are by most measures the simplest possible—and were the first ones I studied. But one can for example also look at rules that involve three colors, rather than two, so that cells can not only be black and white, but also gray. The total number of possible rules of this kind turns out to be immense—7,625,597,484,987 in all—but by considering only so-called "totalistic" ones, the number becomes much more manageable.

> The idea of a totalistic rule is to take the new color of each cell to depend only on the average color of neighboring cells, and not on their individual colors. The picture below shows one example of how this works. And with three possible colors for each cell, there are 2187 possible totalistic rules, each of which can conveniently be identified by a code number as illustrated in the picture. The facing page shows a representative sequence of such rules.

> Example of a totalistic cellular automaton with three possible colors for each cell. The rule is set up so that the new color of every cell is determined by the average of the previous colors of the cell and its immediate neighbors. With 0 representing white, 1 gray and 2 black, the rightmost element of the rule gives the result for average color 0, while the element immediately to its left gives the result for average color 1/3—and so on. Interpreting the sequence of new colors as a sequence of base 3 digits, one can assign a code number to each totalistic rule.

### E2 — Gallery selection and seed are run controls

- Provenance: `BOOK:780,784,788,790`.
- Establishes: the facing-page scan is representative, excludes background-changing rules, and uses a single gray cell; reflection symmetry is a consequence of equal-weight aggregation. The filter, seed, palette, repetition measurement, and behavior grouping do not become program identity.

> We might have expected that by allowing three colors rather than two we would immediately get noticeably more complicated behavior.

> A sequence of totalistic cellular automata with three possible colors for each cell. Although their basic rules are more complicated, the cellular automata shown here do not seem to have fundamentally more complicated behavior than the two-color cellular automata shown on previous pages. Note that in the sequence of rules shown here, those that change the white background are not included. The symmetry of all the patterns is a consequence of the basic structure of totalistic rules. But in fact the behavior we see on the previous page is not unlike what we already saw in many elementary cellular automata a few pages back. Having more complicated underlying rules has not, it seems, led to much greater complexity in overall behavior.

> Using more complicated rules may be convenient if one wants, say, to reproduce the details of particular natural systems, but it does not add fundamentally new features. Indeed, looking at the pictures on the previous page one sees exactly the same basic themes as in elementary cellular automata. There are some patterns that attain a definite size, then repeat forever, as shown below, others that continue to grow, but have a repetitive form, as at the top of the facing page, and still others that produce nested or fractal patterns, as at the bottom of the page.

> Examples of three-color totalistic rules that yield patterns which attain a certain size, then repeat forever. The maximum repetition period is found to be 78 steps, and is achieved by the rule with code number 1329. In the pictures shown here and on the following pages, the initial condition used contains a single gray cell.

### E3 — Repetitive, nested, random, and mixed-complexity views

- Provenance: `BOOK:796,800,804,806,808,810,824`.
- Establishes: gallery classes, codes, percentages, horizons, and eventual behavior are observations/profiles. They supply canonical examples, not distinct update laws.

> Examples of three-color totalistic rules that yield patterns which grow forever but have a fundamentally repetitive structure.

> Examples of three-color totalistic rules which yield nested patterns. In most cases, these patterns have an overall form that is similar to what was found with two-color rules. But code 420, for example, yields a pattern with a slightly different structure.

> Examples of three-color totalistic rules that yield patterns with seemingly random features. Three hundred steps of evolution are shown in each case.

> In detail, some of the patterns are definitely more complicated than those seen in elementary rules. But at the level of overall behavior, there are no fundamental differences. And in the case of nested patterns even the specific structures seen are usually the same as for elementary rules. Thus, for example, the structure in codes 237 and 948 is the most common, followed by the one in code 1749. The only new structure not already seen in elementary rules is the one in code 420—but this occurs only quite rarely.

> About 85% of all three-color totalistic cellular automata produce behavior that is ultimately quite regular. But just as in elementary cellular automata, there are some rules that yield behavior that seems in many respects random. A few examples of this are given on the facing page.

> Beyond fairly uniform random behavior, there are also cases similar to elementary rule 110 in which definite structures are produced that interact in complicated ways. The next page gives a few examples. In the first case shown, the pattern becomes repetitive after about 150 steps. In the other two cases, however, it is much less clear what will ultimately happen. The following pages continue these patterns for 3000 steps. But even after this many steps it is still quite unclear what the final behavior will be.

> Examples of three-color totalistic rules with highly complex behavior showing a mixture of regularity and irregularity. The partitioning into identifiable structures is similar to what we saw in rule 110 on page 32.

### E4 — Long continuations and growth/extinction

- Provenance: `BOOK:828,832,834,838,840,842,846`.
- Establishes: `1635`, `2049`, and `1599` continuation identities; fixed view horizons; and the observed 1599 resolution at step 8282. None is a stopping rule.

> code 1635

> code 2049

> The pictures below show totalistic cellular automata whose overall patterns of growth seem, at least at first, quite complicated. But it turns out that after only about 100 steps, three out of four of these patterns have resolved into simple forms.

> Examples of rules that yield patterns which seem to be on the edge between growth and extinction. For all but code 1599, the fate of these patterns in fact becomes clear after less than 100 steps. A total of 250 steps are shown here.

> The one remaining pattern is, however, much more complicated. As shown on the next page, for several thousand steps it simply grows, albeit somewhat irregularly. But then its growth becomes slower. And inside the pattern parts begin to die out. Yet there continue to be occasional bursts of growth. But finally, after a total of 8282 steps, the pattern resolves into 31 simple repetitive structures.

> <sup>◀</sup> Three thousand steps in the evolution of the last two cellular automata from page 66. Despite the simplicity of their underlying rules, the final patterns produced show immense complexity. In neither case is it clear what the final outcome will be—whether apparent randomness will take over, or whether a simple repetitive form will emerge.

> Nine thousand steps in the evolution of the three-color totalistic cellular automaton with code number 1599. Starting from a single gray cell, each column corresponds to 3000 steps. The outcome of the evolution finally becomes clear after 8282 steps, when the pattern resolves into 31 simple repetitive structures.

### E5 — Exact color-count boundary

- Provenance: `BOOK:1282`.
- Establishes: radius-one totals have `4/7/13` cases for `k=2/3/5`, yielding `16/2187/1,220,703,125` rules; three colors are the first totalistic radius-one setting in this comparison with complex behavior, while more colors do not define a new update mechanism.

> Examples of cellular automata with rules of varying complexity. The rules used are of the so-called totalistic type described on page 60. With two possible colors, just 4 cases need to be specified in such rules, and there are 16 possible rules in all. But as the number of colors increases, the rules rapidly become more complex. With three colors, there are 7 cases to be specified, and 2187 possible rules; with five colors, there are 13 cases to be specified, and 1,220,703,125 possible rules. But even though the underlying rules increase rapidly in complexity, the overall forms of behavior that we see do not change much. With two colors, it turns out that no totalistic rules yield anything other than repetitive or nested behavior. But as soon as three colors are allowed, much more complex behavior is immediately possible. Allowing four or more colors, however, does not further increase the complexity of the behavior, and, as the picture shows, even with five colors, simple repetitive and nested behavior can still occur.

### E6 — Class and borderline galleries

- Provenance: `BOOK:2806,2822,2826,2830,2838,2852`.
- Establishes: nearest-neighbor three-color gallery identity, random initial conditions and 1500-step class-4 view, named codes 1815/2007, and the observer-dependent nature of borderline class labels.

> A sequence of totalistic cellular automata with rules that involve only nearest neighbors, but where each cell can have three possible colors.

> Examples of class 4 cellular automata with totalistic rules involving nearest neighbors and three possible colors for each cell. Each picture shows 1500 steps of evolution from random initial conditions.

> code 1815

> code 2007

> code 2043

> Rare examples of borderline cellular automata that do not fit squarely into any one of the four basic classes described in the text. Different definitions based on different specific properties will place these cellular automata into different classes. The rules shown are totalistic ones involving nearest neighbors and three possible colors for each cell. The first rule can be either class 2 or class 4, the second class 3 or 4, the third class 2 or 3 and the fourth class 1, 2 or 3.

### E7 — Persistent-structure and growth profiles

- Provenance: `BOOK:3320,3324,3348,3352,3356,3360,3364,3370,3372,3374,3378`.
- Establishes: codes 357 and 1329 remain T04 programs while searches, initial-condition numbers, periods, moving structures, and growth outcomes are run/property evidence.

> 3 colors, nearest neighbors, code 357

> 3 colors, nearest neighbors, code 1329

> The picture below shows the structures one finds by explicitly testing the first two billion possible initial conditions for the code 357 cellular automaton from page 282.

> Persistent structures in the code 357 cellular automaton from page 282 obtained by testing the first two billion possible initial conditions. This cellular automaton allows three possible colors for each cell; the initial conditions thus correspond to the base 3 digits of the numbers given. No persistent structures of any size exist in this cellular automaton with repetition periods of less than 5 steps.

> So are moving structures in fact possible in the code 357 cellular automaton? My experience with many different rules is that whenever sufficiently complicated persistent structures occur, structures that move can eventually be found. And indeed with code 357, initial condition 4,803,890 yields just such a structure.

> The picture below shows the first few persistent structures found in the code 1329 cellular automaton from the bottom of page 282. The smallest structures are stationary, but at initial condition 916 a structure is found that moves—all much the same as in the two other class 4 cellular automata that we have just discussed.

> Persistent structures in the code 1329 cellular automaton shown on page 282.

> Unbounded growth in code 1329. The initial condition contains a block of 10 cells. The right-hand side of the pattern repeats every 256 steps, and as it moves it leaves behind an infinite sequence of persistent structures.

> initial condition number 54,889

> Yet looking at the picture above, one might suppose that when unlimited growth occurs, the pattern produced must be fairly complicated. But once again code 1329 has a surprise in store. For the facing page shows that when one reaches initial condition 97,439 there is again unlimited growth—but now the pattern that is produced is very simple. And in fact if one were just to see this pattern, one would probably assume that it came from a rule whose typical behavior is vastly simpler than code 1329.

> Further examples of unbounded growth in code 1329. Most of the patterns produced are complex—but some are simple.

### E8 — Random backgrounds, binary emulation, and irreducibility

- Provenance: `BOOK:6340,7900,7912,8936`.
- Establishes: codes 294/1893 on largely random backgrounds, block emulation of code 1599 by a binary range-five rule, and computational irreducibility as explicit relations/properties.

> Examples of one-dimensional cellular automata that support various forms of persistent structures even on largely random backgrounds. These are 3-color totalistic rules with codes 294 and 1893.

> What about rules that have more than two possible colors for each cell? It turns out that there is a general way of emulating such rules by using rules that have just two colors but a larger number of neighbors. The picture on the facing page shows an example. The idea is that each cell in the three-color cellular automaton is represented by a block of three cells in the two-color cellular automaton. And by looking at neighbors out to distance five on each side, the two-color cellular automaton can update these blocks at each step in direct correspondence with the rules of the three-color cellular automaton.

> An example of how a cellular automaton with three possible colors and nearest-neighbor rules can be emulated by a cellular automaton with only two possible colors but a larger number of neighbors (in this case five on each side). The basic idea is to represent each cell in the three-color rule by a block of three cells in the two-color rule, according to the correspondence given on the left. The three-color rule illustrated here is totalistic code 1599 from page 70.

> Examples of computational reducibility and irreducibility in the evolution of cellular automata. The first two rules yield simple repetitive computationally reducible behavior in which the outcome after many steps can readily be deduced without tracing each step. The third rule yields behavior that appears to be computationally irreducible, so that its outcome can effectively be found only by explicitly tracing each step. The cellular automata shown here all have 3-color totalistic rules.

### E9 — General signature and runnable preset example

- Provenance: `BOOK:8320,11056,11060,11168`.
- Establishes: average-color alias, generic nearest-neighbor/range signatures, and an explicit `k=3,r=1`, code-867 invocation. The invocation is transparently repaired below.

> In fact, as illustrated in the pictures on the facing page, it is sufficient in such cases just to use so-called totalistic rules in which the new color of a cell depends only on the average color of cells in its neighborhood, and not on their individual colors.

> \{n, \{k, 1\}\} k-color nearest-neighbor totalistic rule

> \{n, \{k, 1\}, r\} k-color range r totalistic rule

> This runs the totalistic k=3, r=1 rule with code 867.  $ln[11]:=Show[RasterGraphics[CellularAutomaton]{867, {3, 1}, 1}, {{1}, 0}, 50]]]$

### E10 — General count, assignment sensitivity, lookup, and codec

- Provenance: `BOOK:11897,11902,11904,11908,11910,11912,11914,11916`.
- Establishes: exact rule cardinality, the special role of a value assignment for `k>2`, direct sum lookup, padded base-`k` digits, and reuse of the same framework. The symmetric formula and one general-rule operator have OCR damage repaired below; the totalistic formula/vector are intact.

> - **Page 60 · Numbers of rules.** Allowing k possible colors for each cell and considering r neighbors on each side, there are  $k^{k^{2r+1}}$  possible cellular automaton rules in all, of which  $k^{1/2}k^{r+1}$  are symmetric, and  $k^{1+(k-1)(2r+1)}$  are totalistic. (For k=2, r=1 there are therefore 256 possible rules altogether, of which 16 are totalistic. For k=2, r=2 there are 4,294,967,296 rules in all, of which 64 are totalistic. And for k=3, r=1 there are 7,625,597,484,987 rules in all, with 2187 totalistic ones.) Note that for k>2, a particular rule will in general be totalistic only for a specific assignment of values to colors. I first introduced totalistic rules in 1983.

> ■ Implementation of totalistic cellular automata. To handle totalistic rules that involve *k* colors and nearest neighbors, one can add the definition

> CAStep[TotalisticCARule[rule\_List, 1], a\_List] := rule[[-1 - (RotateLeft[a] + a + RotateRight[a])]]

> CAStep[TotalisticCARule[rule\_List, r\_Integer], a\_List] := rule[[-1 - Sum[RotateLeft[a, i], {i, -r, r}]]]

> One can generate the representation of totalistic rules used by these functions from code numbers using

> $ToTotalisticCARule[num\_Integer, k\_Integer, r\_Integer] := TotalisticCARule[IntegerDigits[num, k, 1 + (k - 1)(2r + 1)], r]$

> ■ Common framework. The *Mathematica* built-in function *CellularAutomaton* discussed on page 867 handles general and

> totalistic rules in the same framework by using ListConvolve[w, a, r+1] and taking the weights w to be respectively  $k \wedge Table[i-1, \{i, 2r+1\}]$  and  $Table[1, \{2r+1\}]$ .

### E11 — Additivity and behavior classes are properties

- Provenance: `BOOK:11918,14223,14224`.
- Establishes: code 420's additive/Pascal-mod-3 relation, the complete cited `k=3` class-4 code list, and class-frequency observations. None changes ordinary totalistic execution.

> - Page 63 · Mod 3 rule. Code 420 is an example of an additive rule, and yields a pattern corresponding to Pascal's triangle modulo 3, as discussed on page 870.

> - Page 235 · Class 4 rules. Other examples of class 4 totalistic rules with *k* = *3* colors include 357 (page 282), 438, 600, 792, 924, 1038, 1041, 1086, 1329 (page 282), 1572, 1599 (see page 70), 1635 (see page 67), 1662, 1815 (page 236), 2007 (page 237) and 2049 (see page 68).

> - **Frequencies of classes.** The pie charts below show results for 1D totalistic cellular automata with *k* colors and range *r*. Class 3 tends to become more common as the number of elements in the rule increases because as soon as any of these elements yield class 3 behavior, that behavior dominates the system.

### E12 — Reversibility, emulation cost, and universality

- Provenance: `BOOK:16024,18348,18748`.
- Establishes: the 1800 reversible `k=3,r=1` rules are unrestricted controls while no nontrivial totalistic rule is reversible; binary emulation expands range; and universality is a property of candidate rules, not preset execution.

> - **Numbers of reversible rules.** For k = 2, r = 1, there are 6 reversible rules, as shown on page 436. For k = 2, r = 2 there are 62 reversible rules, in 20 families inequivalent under symmetries, out of a total of  $2^{32}$  or about 4 billion possible rules. For k = 3, r = 1 there are 1800 reversible rules, in 172 families. For k = 4, r = 1, some of the reversible rules can be constructed from the second-order cellular automata below. Note that for any k and r, no non-trivial totalistic rule can ever be reversible.

> The problem of encoding cells with several colors by blocks of black and white cells is related to standard problems in coding theory (see page 560). One approach is to use {1, 1} to indicate the boundary of each block, and then within each block to use all possible digit sequences which do not contain {1, 1}, as in the Fibonacci number system discussed on page 892. Note that the original rule with *k* colors and *r* neighbors involves  $Log[2, k^{k^{2r+1}}]$  bits of information; the two-color rule that emulates it involves  $Log[2, 2^{2^{2s+1}}]$  bits. As a result, the minimum possible s for k = 3, r = 1 is about 2.2; in the specific example shown in the main text it is 5.

> - Totalistic rules. It is straightforward to show that totalistic cellular automata can be universal. Explicit simple candidates include k = 2, r = 2 rules with codes 20 and 52, as well as the various k = 3, r = 1 class 4 rules shown in Chapter 3.

### E13 — Lower- and higher-color totalistic controls

- Provenance: `BOOK:2802,2868,3316,9166,11625,18672`.
- Establishes: binary range-two and four-color totalistic rules are adjacent profiles, including separate universality/undecidability examples. They do not widen T04 beyond `k=3,r=1`.

> Totalistic cellular automata whose rules involve nearest and next-nearest neighbors, and where each cell has two possible colors.

> A sequence of totalistic rules involving nearest neighbors and four possible colors for each cell chosen to show transitions between rules with different classes of behavior. Note that class 4 seems to occur between class 2 and class 3.

> 2 colors, next-nearest neighbors, code 20

> Cellular automaton evolution illustrating the phenomenon of undecidability. Pattern (a) dies out after 36 steps; pattern (b) takes 1017 steps. But what the final outcome in cases (c) and (d) will be is not clear after even a million steps. And in general there appears to be no finite computation that can guarantee to determine the final outcome of the evolution after an infinite number of steps. The cellular automaton rule used is a 4-color totalistic one with code 1004600. Whether a pattern in a cellular automaton ever dies out can be viewed as analogous to a version of the halting problem for Turing machines.

> - **Code 10.** Rule 30 is by many measures the simplest cellular automaton that generates randomness from a single black initial cell. But there are other simple examples—that historically I noticed slightly earlier than rule 30, though did not study—that occur in k = 2, r = 2 totalistic rules. And indeed among the 64 such rules, 13 show randomness. An example shown below is code 10, which specifies that if 1 or 3 cells out of 5 are black then the next cell is black; otherwise it is white.

> In 1984 I suggested that cellular automata showing what I called class 4 behavior should be universal-and I identified some simple rules (such as k = 2, r = 2 totalistic code 20) as explicit candidates.

### E14 — Non-totalistic three-color boundaries

- Provenance: `BOOK:5218,5222,5486,10395,10411,11164`.
- Establishes: unrestricted reversible rules, block rules, purpose-search rules, and the general `k=3,r=1` invocation are adjacent constructions with a vastly larger code range. Literal color count alone does not select T04.

> So is it possible to get more complex behavior while maintaining reversibility? There are a total of 7,625,597,484,987 cellular automata with three colors and nearest-neighbor rules, and searching through these one finds just 1800 that are reversible. Of these 1800, many again exhibit simple behavior, much like the pictures above. But some exhibit more complex behavior, as in the pictures below.

> Examples of some of the 1800 reversible cellular automata with three colors and nearest-neighbor rules. Even though these systems exhibit complex behavior that scrambles the initial conditions, all of them are still reversible, so that starting from the configuration of cells at the bottom of each picture, it is always possible to deduce the configurations on all previous steps.

> Block cellular automata with three possible colors which conserve the combined number of black and gray cells. In rule (a), black and gray cells remain in localized regions. In rule (b), they move in fairly simple ways, and in rules (c) and (d), they move in a seemingly somewhat random way. The rules shown here are reversible, although their behavior is similar to that of non-reversible rules, at least after a few steps.

> Examples of cellular automata that can be viewed as achieving the purpose of doubling the width of the pattern given in their input. Rule (a) involves 6 colors, and works sequentially, much as a typical traditional engineering system might. Rule (b) involves 4 colors, and works in parallel. Rule (c) was found by a large search, and involves only 3 colors. It takes the fewest steps of any 3-color rule to generate its result. Its rule number is 5407067979.

> Examples of rules with three colors that achieve the purpose of doubling the width of the pattern given in their input. These examples are taken from the 4277 found in effect by searching exhaustively all 7,625,597,484,987 possible rules with three colors. In most cases the number of steps to generate the final pattern increases roughly linearly with the width of the input—although in the case of the fourth-to-last rule on the second row it is  $2(n^2 - n + 1)$  for width n.

> This runs the general k=3, r=1 rule with rule number 921408. In[10]:=Show[RasterGraphics[CellularAutomaton]{921408, 3, 1}, {{1}, 0}, 100]]]

### E15 — Actual-Index routing fragments

- Provenance: `BOOK:20846,20965,20967,20969,20972,20980,21134,21223,21233,21471,21683,21731,21933,22030,22146,22352,22392`.
- Establishes: all 17 actual-Index physical lines route to strict, Notes, profile, property, emulation, or sibling evidence already dispositioned.

> Additive cellular automata with 3 colors, 886

> implementation of totalistic, 886

> three-color, 60

> weighted totalistic, 427

> in 3-color totalistic CAs, 948

> Code 294 for totalistic CAs, 60

> Code 1599

> Code 1659, class 4 behavior in, 238

> of three colors by two, 655, 1111

> Glider gun in code 1329, 288

> Growth totalistic rules, 928

> in code 357 CA, 286

> of CA emulations, 1118

> Outer totalistic rules

> three-color, 436

> growth totalistic, 928

> Sum (totalistic) rules, 60

> Totalistic cellular automata, 60

> in totalistic cellular automata, 693

## Source Repairs

1. **Primary official files and hashes.** Strict pages 60–70 were checked against official [`nks-ch3.pdf`](https://files.wolframcdn.com/pub/www.wolframscience.com/nks/nks-ch3.pdf), SHA-256 `d4005b27774084c276e67d46a6c79106b93b785d4329893080223c9da8263e76`. The later code-357/1329 profiles were checked against official [`nks-ch6.pdf`](https://files.wolframcdn.com/pub/www.wolframscience.com/nks/nks-ch6.pdf), SHA-256 `5af1e53860bd4a6877961681cf49b16058a53ee55a2bfa8c64ac7cc13174bca0`. Chapter 3 Notes page 886 was checked against official [`nks-nts-ch3.pdf`](https://files.wolframcdn.com/pub/www.wolframscience.com/nks/nks-nts-ch3.pdf), SHA-256 `21666aa07f49e47483cdc9883e285b8cd47d397dd18eea0b72f05d4d3272a009`. Cross-chapter Notes, including class, reversibility, emulation, and universality routes, were checked against official [`nks-notes.pdf`](https://files.wolframcdn.com/pub/www.wolframscience.com/nks/nks-notes.pdf), SHA-256 `549f043595653a7d276b07ba52d435700039b71427b4e1774a44b1a58eff4723`.
2. **Strict raster label restoration.** The monolith OCR drops most labels embedded in gallery rasters. The official Chapter 3 PDF visibly and textually corroborates the labels. The pinned local assets are:

   | Asset | Geometry | SHA-256 | Restored semantic text |
   |---|---:|---|---|
   | `_page_75_Figure_6.jpeg` | `610x446` | `acb13963632286960ca61b616ff2f45a940750f3ab7deb5e6fbf696543015c15` | digits `1,0,0,1,2,1,0 = 777` |
   | `_page_76_Figure_2.jpeg` | `1109x1279` | `8c11659c8bd63d37a972c5ffab376b62948f7c4e05f9fd10f239e51464f4084d` | 50 codes `993..1140` step 3 |
   | `_page_77_Figure_6.jpeg` | `892x716` | `4c1f8894016156dc4d473e911e0fa5c7db16711a8c2873fa493fb7854ad41c66` | `600,843,870,1086,1167,1329,1572,1815,1842` |
   | `_page_78_Figure_2.jpeg` | `1107x615` | `5c5ca56f3e8141c3aa4d7648f3ebe34a911515bf9dfc9118795135736f69b879` | `219,957,966,1884` |
   | `_page_78_Figure_4.jpeg` | `1134x621` | `088016843cb7d74ad621ebed323401dfb9783ce061ece275ba36b0815c7dfa28` | `237,420,948,1749` |
   | `_page_79_Picture_2.jpeg` | `886x1399` | `355d13fde85b89c2e3e26d1ae199e30ad2191b0bcbd3d4c89ac76785fa1ebc86` | `177,912,2040` |
   | `_page_81_Picture_1.jpeg` | `826x446` | `0617e6b01a1faa43e968051ff8716171b665e79d087c8c13a47811c0520f3014` | `1041` |
   | `_page_81_Picture_2.jpeg` | `816x429` | `6efe4dc8703a3045bd6189f930a0cdb44e59dc71f38dc91a52e8faa84e801a7e` | `1635` |
   | `_page_81_Picture_3.jpeg` | `869x470` | `b3812f8742bf08299270512de2cdffa57ac14be5b10a6cdefa60d4878173553c` | `2049` |
   | `_page_82_Picture_1.jpeg` | `1061x1381` | `aa534aa358e74235ef5de86980c5c6f0895bac2b616e990c1cda7253639a4511` | continuation `1635` |
   | `_page_83_Picture_1.jpeg` | `1067x1387` | `cd4f0434c12f9b86bdde3730270451df2dfb503194d22bc04d0609973e9d3a77` | continuation `2049` |
   | `_page_84_Picture_2.jpeg` | `764x747` | `02782253cc66a9de075af5d1d02f224645e443040f5ff6001fef6467a7013cbe` | `357,600,1599,2058` |
   | `_page_85_Picture_2.jpeg` | `1107x1360` | `2374289d970042909316f68cf240379d6f2826ba90dab95db0a317e672b91b0f` | continuation `1599` |

3. **`BOOK:11168` invocation OCR.** `$ln[11]`, displaced braces, and the malformed call boundary are extraction errors. Official all-Notes gives normalized `In[11] := Show[RasterGraphics[CellularAutomaton[{867, {3, 1}, 1}, {{1}, 0}, 50]]]`. This is direct runnable evidence for a code-valued `k=3,r=1` totalistic preset; its `{{1},0}` seed/background and 50-step horizon remain run arguments.
4. **`BOOK:11897` formula OCR.** The totalistic formula `k^(1+(k-1)(2r+1))`, the specific-value-assignment warning, and the `k=3,r=1` numeric checks are intact. The adjacent symmetric-count extraction `$k^{1/2}k^{r+1}$` is malformed; official page 886 shows `k^(1/2 k^(r+1) (1+k^r))`. The sibling formula is not used for T04.
5. **`BOOK:11916` operator OCR.** The general-rule vector is `$k^Table[i-1,{i,2r+1}]$`, not the monolith's `$k \wedge Table[...]$`; official page 886 confirms the caret. The totalistic all-one weight vector is intact and is the only part used here.
6. **`BOOK:11037` truncation.** Official all-Notes completes the routing sentence with `page 927.` It adds no preset mechanics.
7. **Code 777 and digit direction.** The official strict figure shows high-sum-to-low-sum digits `1,0,0,1,2,1,0 = 777`. `BOOK:776` puts sum zero at the rightmost displayed element. Thus the sum-indexed table is `U_0..U_6=(0,1,2,1,0,0,1)` and `777=sum(U_s*3^s)`. This is a transparent raster-text restoration, not a palette-derived rule.
8. **Stable-white scan.** With state/value zero as white and sum zero at the least-significant digit, stable white means `U_0=0`, equivalently `code mod 3=0`. Every page-76 code `993+3i`, `0<=i<50`, satisfies that predicate. The caption licenses the selection predicate, not a default background, seed, horizon, or reduced code range.
9. **Preset arithmetic.** For `k=3,r=1`, three values in `0..2` produce every integer sum `0..6`; a complete rule has seven output rows, each in `0..2`, hence `3^7=2187` codes `0..2186`. Average and sum induce the same cases because the arity is fixed at three; no floating-point reducer is licensed.
10. **Program/run/property/view boundary.** The single-gray seed, stable-white scan, random backgrounds, finite horizons, palette, symmetry observation, class labels, additive identity, reversible prohibition, universality candidates, and binary emulation are explicit controls or relations. None creates a three-color executor, a hidden seed, a stopping condition, or a second codec.
11. **Split and Index routing.** The split wording has minor normalization differences, and image labels remain raster-bound. `BACK-MATTER/Index/Index.md` is Notes; the actual split Index begins at `BACK-MATTER/Colophon/Colophon.md:3383`. Canonical `BOOK` physical lines and official PDFs are the provenance authorities.
12. **Later property and relation assets.** `BOOK:3314-3378` interleaves code-20, code-357, and code-1329 rasters with captions. The official Chapter 6 page 287 contains a paragraph dropped by the monolith extraction: at initial condition 54,889, the repeating right-hand structure moves while leaving persistent structures, so the whole structure grows forever. This restores explanatory profile text only. The official all-Notes PDF also corroborates the related additive modulo-3 raster at `BOOK:11297`, the three Life-spacefiller analogy rasters at `BOOK:14829-14833`, and the unrestricted rule-2144 control at `BOOK:18746`. Their exact local hashes/geometries are pinned above and below; none supplies T04 rule rows.
13. **`BOOK:2834` page-number contamination.** The extracted lone `238` follows `_page_253_Picture_1.jpeg`; it is the printed page footer, not a rule code. The raster visibly labels `code 1659`, official Chapter 6 text extraction gives `code 1659` followed separately by page `238`, and actual Index `BOOK:20980` routes `Code 1659, class 4 behavior in, 238`. Notes code `1662` at `BOOK:14223` is a separate, unpictured example and must not be substituted for 1659.
14. **Metadata-to-source join repair.** An exact join against the independent 68-item raster ledger found 24 asset links that the earlier 44-asset source closure had not traversed: `BOOK:764,858,860,1280,1958,2172,2920,6336,6338,6642,7910,8306,8934,9164,11166,11170,11176,11182,11627,11629,14226,14228,14230,14232`. Seven are direct T04 evidence, one is an emulation relation, and sixteen are adjacent or negative controls. The manifest includes all 24 with exact source-to-ledger equality.
15. **E14 reverse-link repair.** A reverse audit then found four directly linked control rasters governed by already quoted E14 captions: `BOOK:5220,5484,10393,10409`. They show reversible three-color rules, conserved three-color block rules, and two purpose-search comparisons; none is totalistic. This produced the historical 72-link/243-candidate closure without adding T04 mechanics.
16. **T06 reverse-link repair.** The downstream audit found three links omitted from retained T04 routes. `BOOK:2922` directly governs two-dimensional binary totalistic raster `BOOK:2924`; `BOOK:2926` says the rules are the same kind as on the facing page, raster `BOOK:2928` visibly reuses codes `4,12,24,38,30,52`, and `BOOK:2930` identifies the panels as one-dimensional slices. Both rasters are excluded geometry/observer controls. Separately, `BOOK:17431` says `pictures below` and directly governs feature-extraction raster `BOOK:17433`, a relation-only application of 16 even-numbered binary five-neighbor totalistic rules. The same-construction frontier stops before `BOOK:2932`, where the page-264 Life/outer-totalistic chain begins. Adding the three links closes the final 75-link source/metadata equality and raises the disjoint source manifest to 246 without changing T04 mechanics.

### Citation, quote, source-repair, asset, and preset oracle

```bash
python3 - <<'PY'
import hashlib, itertools, re, subprocess
from pathlib import Path
from PIL import Image

book=Path('ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md')
stage=Path('goal-1/23-T04-THREECOLOR-TOTALISTIC.md')
L=book.read_text().splitlines(); text=stage.read_text()

def expand(spec):
    out=set()
    for item in spec.split(','):
        if '-' in item:
            a,b=map(int,item.split('-')); out.update(range(a,b+1))
        else: out.add(int(item))
    return out
def refs(s):
    out=set()
    for m in re.finditer(r'BOOK:([0-9]+(?:-[0-9]+)?(?:,[0-9]+(?:-[0-9]+)?)*)',s):
        out |= expand(m.group(1))
    return out

# Traverse every cited monolith line anywhere in this stage.
cited=refs(text)
assert cited and all(1 <= n <= len(L) for n in cited)
assert len(cited)==260
for n in sorted(cited): _=L[n-1]

# Every verbatim excerpt fragment must occur on a cited provenance line.
ex=text.split('## Book Excerpts',1)[1].split('## Source Repairs',1)[0]
current=set(); quote_count=0; quote_lines=set()
for row in ex.splitlines():
    if row.startswith('- Provenance:'):
        current=refs(row); assert current
    elif row.startswith('> '):
        q=row[2:].strip(); assert q and current
        hits={n for n in current if q in L[n-1].strip()}
        assert hits,(sorted(current),q)
        quote_lines |= hits; quote_count += 1

# Pin the monolith defects and intact semantic portions.
assert '$ln[11]' in L[11167] and 'code 867' in L[11167]
assert '$k^{1/2}k^{r+1}$' in L[11896]
assert '$k^{1+(k-1)(2r+1)}$' in L[11896]
assert r'$k \wedge Table[i-1, \{i, 2r+1\}]$' in L[11915]
assert L[11036].endswith('higher-dimensional cellular automata on')
assert L[2833]=='238' and L[2835]=='![](_page_254_Picture_1.jpeg)'

official={
'/tmp/nks-ch3.pdf':'d4005b27774084c276e67d46a6c79106b93b785d4329893080223c9da8263e76',
'/tmp/nks-ch6.pdf':'5af1e53860bd4a6877961681cf49b16058a53ee55a2bfa8c64ac7cc13174bca0',
'/tmp/nks-nts-ch3.pdf':'21666aa07f49e47483cdc9883e285b8cd47d397dd18eea0b72f05d4d3272a009',
'/tmp/nks-notes.pdf':'549f043595653a7d276b07ba52d435700039b71427b4e1774a44b1a58eff4723',
}
for name,want in official.items():
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==want,name
def pdf_text(name):
    raw=subprocess.check_output(['pdftotext','-layout',name,'-'],text=True,errors='replace')
    return re.sub(r'\s+',' ',raw)
strict=pdf_text('/tmp/nks-ch3.pdf')
ch6=pdf_text('/tmp/nks-ch6.pdf')
nts=pdf_text('/tmp/nks-nts-ch3.pdf')
notes=pdf_text('/tmp/nks-notes.pdf')
assert '1 0 0 1 2 1 0 = 777' in strict
assert 'those that change the white background are not included' in strict
assert 'initial condition used contains a single gray cell' in strict
scan=list(range(993,1141,3))
assert len(scan)==50 and all(f'code {c}' in strict for c in scan)
for c in (600,843,870,1086,1167,1329,1572,1815,1842,219,957,966,1884,
          237,420,948,1749,177,912,2040,1041,1635,2049,357,1599,2058):
    assert f'code {c}' in strict,c
chapter6_scan=list(range(1002,1096,3))
assert len(chapter6_scan)==32 and all(f'code {c}' in ch6 for c in chapter6_scan)
for c in (1815,2007,1659,2043,219,438,1380,1632,357,1329):
    assert f'code {c}' in ch6,c
assert 'initial condition 54,889 is reached' in ch6
assert 'initial condition 97,439' in ch6
assert 'specific assignment of values to colors' in nts
assert 'respectively k ^Table[i - 1, {i, 2 r + 1}] and Table[1, {2 r + 1}]' in nts
assert 'page 927.' in notes
assert 'This runs the totalistic k=3 , r =1 rule with code 867.' in notes
assert 'In[11] : = Show[RasterGraphics[CellularAutomaton[{867, {3, 1}, 1}, {{1}, 0}, 50]]]' in notes
assert 'Page 235 · Class 4 rules. Other examples of class 4 totalistic' in notes
assert 'rules with k = 3 colors include 357 (page 282)' in notes
assert '1662' in notes and 'rule number 2144' in notes
assert 'closely analogous to those shown for code 1329 on page 287' in notes
assert 'Other integer functions. The pictures above show patterns produced by reducing several integer functions modulo 2.' in notes

root=Path('ref/A-New-Kind-of-Science/CHAPTERS/3-The-World-of-Simple-Programs/Images')
assets={
'_page_75_Figure_6.jpeg':((610,446),'acb13963632286960ca61b616ff2f45a940750f3ab7deb5e6fbf696543015c15',[777]),
'_page_76_Figure_2.jpeg':((1109,1279),'8c11659c8bd63d37a972c5ffab376b62948f7c4e05f9fd10f239e51464f4084d',scan),
'_page_77_Figure_6.jpeg':((892,716),'4c1f8894016156dc4d473e911e0fa5c7db16711a8c2873fa493fb7854ad41c66',[600,843,870,1086,1167,1329,1572,1815,1842]),
'_page_78_Figure_2.jpeg':((1107,615),'5c5ca56f3e8141c3aa4d7648f3ebe34a911515bf9dfc9118795135736f69b879',[219,957,966,1884]),
'_page_78_Figure_4.jpeg':((1134,621),'088016843cb7d74ad621ebed323401dfb9783ce061ece275ba36b0815c7dfa28',[237,420,948,1749]),
'_page_79_Picture_2.jpeg':((886,1399),'355d13fde85b89c2e3e26d1ae199e30ad2191b0bcbd3d4c89ac76785fa1ebc86',[177,912,2040]),
'_page_81_Picture_1.jpeg':((826,446),'0617e6b01a1faa43e968051ff8716171b665e79d087c8c13a47811c0520f3014',[1041]),
'_page_81_Picture_2.jpeg':((816,429),'6efe4dc8703a3045bd6189f930a0cdb44e59dc71f38dc91a52e8faa84e801a7e',[1635]),
'_page_81_Picture_3.jpeg':((869,470),'b3812f8742bf08299270512de2cdffa57ac14be5b10a6cdefa60d4878173553c',[2049]),
'_page_82_Picture_1.jpeg':((1061,1381),'aa534aa358e74235ef5de86980c5c6f0895bac2b616e990c1cda7253639a4511',[1635]),
'_page_83_Picture_1.jpeg':((1067,1387),'cd4f0434c12f9b86bdde3730270451df2dfb503194d22bc04d0609973e9d3a77',[2049]),
'_page_84_Picture_2.jpeg':((764,747),'02782253cc66a9de075af5d1d02f224645e443040f5ff6001fef6467a7013cbe',[357,600,1599,2058]),
'_page_85_Picture_2.jpeg':((1107,1360),'2374289d970042909316f68cf240379d6f2826ba90dab95db0a317e672b91b0f',[1599]),
}
for name,(size,want,codes) in assets.items():
    p=root/name
    assert hashlib.sha256(p.read_bytes()).hexdigest()==want,name
    with Image.open(p) as im: assert im.size==size,(name,im.size,size)
    assert all(0 <= c < 2187 for c in codes)

base=Path('ref/A-New-Kind-of-Science')
extra_assets={
'CHAPTERS/6-Starting-from-Randomness/Images/_page_248_Figure_2.jpeg':((1086,1389),'b2a20cb8095eb211fedd963d622222ca98fe0428f397b71bef90db8fa6871957'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_249_Picture_1.jpeg':((1082,1403),'f7b2834be41656cff9512b7affdd5fa57640bbbb6ecd93da1440202bf113f7ef'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_251_Picture_1.jpeg':((1123,1383),'41cfc762284fdcd65e5663fb7631aa4c504aea46a746a8a4ed24407b76b89196'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_252_Picture_2.jpeg':((1121,1377),'120e95a57f683744ff3e71981f4fa07ff850d0cad5633bf4d2f27906a76e909f'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_253_Picture_1.jpeg':((1227,1519),'148a433a11b4889c91c1a7be3c6f00172a3961428e6d41c47a06954136245faf'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_254_Picture_1.jpeg':((1117,1383),'d32b7fc3dedc9f262e5a3d3d928d1d7d94d1a219fd75aeeefdb988c74869a168'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_2.jpeg':((273,171),'b175f64e60cf41042d8ba6a11ed8d04eec4a8101bef8f9f231aae532eca6ca06'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_3.jpeg':((259,167),'00ef0063254d4f75734cd76d8f2d07de4ae1d6b041b9664197c2da99641d8b14'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_4.jpeg':((267,186),'700d71a0beb145c953ca87f4d8649aecd7b7d60df69ccd569cba02f6daeb1acc'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_5.jpeg':((273,165),'ae44e4411841a03fced5b5114f6cef4be62793c6a58c9a4ce6c357d214c7ce35'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_256_Figure_2.jpeg':((1092,1367),'1c4967f6967d8e813b2a281e2615dc8bef272eb57789b60e23c950de5e6bc01f'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_297_Picture_2.jpeg':((1111,408),'953c15d2e64464aceadb6181639cf36973db9513d6e0b7fc3fb43564efc65be8'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_297_Picture_4.jpeg':((1127,415),'26b299987a91daf8d15fc226c845c7efa7d55b9aa4221a4e6d41646b8c384204'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_297_Picture_6.jpeg':((1123,408),'b94ac983e3496b023a1a991b15a701de9a1c4c5cba75a84b16254c497a1c76f1'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_298_Figure_2.jpeg':((1159,1297),'7cacf2667a3f923d35106ec7eff09b9ce551d79dd828f8661458dd121bda09df'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_299_Picture_3.jpeg':((1150,600),'32d4ed4b16a083fb731c37cc80c64efb9995756808c316a0ced0dea0e9bd5475'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_300_Figure_1.jpeg':((1150,1192),'ee5ea91d3855bf31bd793f02677c0c19d9203ac20532b3b7bb07df838065294c'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_301_Picture_2.jpeg':((906,699),'3e9aec2832697e07ea20391c1454e022bc8578fcfb4c126bbb53e6fdfe3f6eb3'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_302_Picture_3.jpeg':((1036,712),'4ec6db32d4f0b659a8519110b7885e05487e68d0348b390323daa55e7b322fd1'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_303_Picture_2.jpeg':((616,1053),'26ec2731176f7ef4b471b4f395f3968eefa69e0eba88a3f672268129d68e07aa'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_304_Picture_2.jpeg':((1109,1363),'21cc5432bcfcc379619d43c076f3102a3e12d64cd724d9fe5709055b72874ecf'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_305_Picture_2.jpeg':((1184,1342),'7e75ba3d0cb57a0b35d5a7b29e803386617e1ede22eefae19ce6e21fc465a9c9'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_21.jpeg':((583,225),'5f829c7776b53963e578df5a783553320da171c4e1c4d92c470899ec5bb3e40d'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_23.jpeg':((139,141),'f14931f6bb008435e34961947dce7b11d5ec6d0bd4cc5b936bcee81b830adc0a'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_24.jpeg':((135,138),'5b302ed9d6c9cbee590270c7bdc169b62b554b0e186a94fdb3d1952a69c0f8c5'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_25.jpeg':((138,145),'f5eb9593ba90b4b240dc6990bb0e7204066cc48e81e82b96186029ff866d40da'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_26.jpeg':((135,155),'badba07cc053bdf7f4e5b41d7d90b2b248d8acd75b9728898e10c69a59c7ceec'),
'BACK-MATTER/Index/Images/_page_980_Picture_15.jpeg':((160,195),'641317f32d429dd61b8353e1ebe65bd80f30950df78f0ebdc3a7f99b6bd26cd9'),
'BACK-MATTER/Index/Images/_page_980_Picture_16.jpeg':((172,187),'90df3d1e1e99ed74dd1844654ff41b04b23f6fe22552cefa2b72f659cd0c5fda'),
'BACK-MATTER/Index/Images/_page_980_Picture_17.jpeg':((223,207),'3ad70eb7f740edf7749700ff107f08306830f3e3fd617f2df3f9e7e559178e21'),
'BACK-MATTER/Colophon/Images/_page_1132_Picture_2.jpeg':((606,308),'422ce8c21c465e2ffdffdb0f691f9521a21b9389897336dd4e4a2c716295c589'),
}
joined_assets={
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_74_Picture_5.jpeg':((858,423),'713c4c55c6a004d76c5e47f1f39513bb1656f35feb0fe9aa72c4503ca311cdc6'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_86_Picture_7.jpeg':((240,500),'59213fbf1a0e6904a6566043c889acd32853d799d5a71bfec1e2d0c45bb1eec5'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_86_Picture_8.jpeg':((506,51),'d844f2419d7ff2a748a93e4ae6dd09c947bf5ed0723aa1defb4354c810b1fb25'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_122_Figure_2.jpeg':((1098,1164),'ccd7a43a495d01a22300c4b9abbb3ff1b13a3ef37389e77ca491ec805cbaa822'),
'CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_171_Picture_5.jpeg':((277,91),'6695e1c946cf6adaa04a3915f2c720f69de4d18b74a81a01aaab346052119455'),
'CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_185_Picture_9.jpeg':((213,114),'abfbc90a8bdab839ac452194adf8f7e30258e877967a79ac71db59b1a716df75'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_261_Figure_2.jpeg':((1109,1297),'49f35fe65202ef7fbfee2da92b7460d36fc329b66a553782ebf8991f237944dd'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_262_Figure_2.jpeg':((1013,1291),'23df7e86bf96a148a17c13847eb53c773a24f86cc5a24f2e1a550f79b94439e3'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_263_Figure_2.jpeg':((1195,1355),'71f5ac8784f493b664a93aff52e157e1ac7bf94a6b2e910f98de9fef663736ec'),
'CHAPTERS/9-Fundamental-Physics/Images/_page_541_Picture_3.jpeg':((436,268),'83d828ba45f3f3e7390bf66183643a32c3c7b83646cc3880aedf099a49284c1e'),
'CHAPTERS/9-Fundamental-Physics/Images/_page_541_Picture_4.jpeg':((418,250),'d96c865b43b912ce4e2d6f0c2ddf659eed32f17db48c151161c364187fcc7a1f'),
'CHAPTERS/10-Processes-of-Perception-and-Analysis/Images/_page_566_Figure_2.jpeg':((1032,699),'6d66d95c8e3c286272cded005d60557ce7a075ffebfd268486c23abe13a29a1e'),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_670_Figure_1.jpeg':((1064,1224),'a1a2a5c04b509ecc0357273387b2950d179478c65406427751904987ec9e8d3e'),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_707_Figure_1.jpeg':((1130,1111),'974e12d28e8acc6fb4af26f7b1dd09eae1f30d802666a61f41abed8ec2d42e19'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_753_Picture_3.jpeg':((912,565),'8cfad05d53abb9791d37dd6d8262ec12dbc08bb1d72866ce34c46ecb99a94a88'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_769_Figure_1.jpeg':((1065,1308),'a980effe214906d991e8ca9180cb9f9d6eade2f978a8358487a60bb1728058f3'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_23.jpeg':((160,117),'132528352f363e52a20e73e1e8341203126448c0c6c8545eed48626eaddac16c'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_25.jpeg':((211,117),'d53637ce9ec50330d5fa6239b23f48d57b563266a0085a23517d4538020fd5fb'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_28.jpeg':((205,110),'2da239aceec3720e5aeccd5de8898c37fe7e975230814c0b3a8e3dcacbde9096'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_31.jpeg':((117,117),'ca086555513a6d8ba5bcbe92d97af26e55aa899cf629e0ab61d8fa8c71b81586'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_897_Picture_19.jpeg':((553,155),'2cedbff5433363c86786feea8804c95229179daf455f07ee8071d6345223894b'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_897_Picture_20.jpeg':((543,329),'ee9cadafa6b0b5a45d9cfb4ed310aff751e84f46a86277821e9f971f3c067b3f'),
'BACK-MATTER/Index/Images/_page_963_Picture_8.jpeg':((144,152),'1fb4f0b4c03d8ba9f9fdeb67a0bbda2d786ed7ceeb13cdd8c31337ccd54bcdfb'),
'BACK-MATTER/Index/Images/_page_963_Picture_9.jpeg':((136,148),'515f5de1423a9164ed6def92d786346f64c15a0a87ba07b723c069e62829caf6'),
'BACK-MATTER/Index/Images/_page_963_Picture_10.jpeg':((138,158),'4b5ff621a668c5b706cdec0481cf3849facb7395d256dfd7c39b471d95fd018f'),
'BACK-MATTER/Index/Images/_page_963_Picture_11.jpeg':((136,152),'7c660bbbb03b2d3116aab32cd50a5a3ff094961d49b403148531b36759335d6b'),
'BACK-MATTER/Index/Images/_page_1092_Picture_6.jpeg':((583,141),'b13e50f8bb2f7e905b8580ea94d93c7295e5967125aa8042defe76936bdb1dd6'),
}
control_assets={
'CHAPTERS/9-Fundamental-Physics/Images/_page_451_Picture_6.jpeg':((1103,483),'e7bbbefb729e76dd5d080d0b841a485ece898d9c3197780b4871c742d61a4e89'),
'CHAPTERS/9-Fundamental-Physics/Images/_page_476_Figure_3.jpeg':((1149,988),'e661d9c28572ba62f75cf4b8a085e1580caf88b7c1c88bdd3c60a018e32ab108'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_847_Figure_1.jpeg':((1041,385),'2d36e7eaeb3b073e68621ef5f9c1c397ae24ddc74fe06f26e62546ccc3af2902'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_848_Figure_2.jpeg':((1194,1308),'0bfecfeff1bd81072838e39704fc6572632dee083f91ddc4370909b0e2c5b5dd'),
}
assert len(extra_assets)==31 and len(joined_assets)==27 and len(control_assets)==4
assert not (set(extra_assets)&set(joined_assets))
assert not ((set(extra_assets)|set(joined_assets))&set(control_assets))
all_extra={**extra_assets,**joined_assets,**control_assets}
for rel,(size,want) in all_extra.items():
    p=base/rel
    assert hashlib.sha256(p.read_bytes()).hexdigest()==want,rel
    with Image.open(p) as im: assert im.size==size,(rel,im.size,size)

# Exact source-manifest/metadata-ledger equality, including paths rather
# than only basenames or counts.
asset_audit=text.split('## Asset and Raster Audit',1)[1]
items_src=asset_audit.split('\nitems={',1)[1].split('\n}\n\ndef jpeg_size',1)[0]
ledger_paths=set(re.findall(r"'([^']+\.jpeg)':\(",items_src))
strict_paths={f'CHAPTERS/3-The-World-of-Simple-Programs/Images/{name}' for name in assets}
assert len(ledger_paths)==75
assert strict_paths|set(all_extra)==ledger_paths

# Independent preset/cardinality/codec checks.
k=3; r=1; q=2*r+1; M=1+(k-1)*q
reachable={sum(v) for v in itertools.product(range(k),repeat=q)}
assert q==3 and M==7 and reachable==set(range(7)) and k**M==2187
assert all(c%3==0 for c in scan) and len(range(0,2187,3))==729
sum_digits=[0,1,2,1,0,0,1]
assert sum(d*3**s for s,d in enumerate(sum_digits))==777
for code in range(2187):
    digits=[(code//(3**s))%3 for s in range(7)]
    assert len(digits)==7 and all(d in (0,1,2) for d in digits)

assert quote_count==92 and len(quote_lines)==90
asset_count=len(assets)+len(all_extra)
assert asset_count==75
print(f'T04 evidence oracle: PASS cited={len(cited)} quote_fragments={quote_count} quote_lines={len(quote_lines)} assets={asset_count} pdfs={len(official)}')
PY
```

Expected terminal line:

```text
T04 evidence oracle: PASS cited=260 quote_fragments=92 quote_lines=90 assets=75 pdfs=4
```

## Construction Model

**Preset proof.** T03 declares `q=2r+1`, `M=1+(k-1)q`, and `R=k^M`. Setting `k=3,r=1` yields `q=3`, `M=7`, and `R=2187`, exactly the strict three-color construction and count (`BOOK:772-776,11897`). The direct implementation sums the radius-one rotations and indexes the same padded table used by generic range-`r` totalistic rules (`BOOK:11902-11912`). There is therefore no residual T04 mechanism after the parameter values are fixed.

**Native program.** A resolved T04 program contains:

- the finite alphabet `A_3=(0,1,2)` and explicit canonical bijection `nu_3={0:0,1:1,2:2}`;
- fixed ordered 1D support semantics, `AllSites`, and the old radius-one read stencil `(-1,0,+1)` including self;
- the closed descriptor `EqualWeightIntegerSum(valuation=nu_3, arity=3)` with exact image `{0,...,6}` and exact-average labels `s/3` only as derived metadata;
- one immutable complete sum-case table `U:{0,...,6}->A_3`; and
- the ordinary T01/T02/T03 typed same-site `Assign` result and atomic parallel commit.

For old field `x`, the local result is `U(nu_3(x[i-1])+nu_3(x[i])+nu_3(x[i+1]))`. One event reads one old snapshot, assigns every active site, and commits together. It has one deterministic successor and no native halt; fixed segments, cycles, integer-line causal windows, exterior values, initial fields, event horizons, and crops are realization/run/view choices.

**Table/code relation.** `n=sum_{s=0}^6 nu_3(U(s))3^s`, so `0<=n<=2186`, `U(s)=floor(n/3^s) mod 3`, and displayed source digits run in the reverse high-sum-to-low-sum order. The resolved structural program, whether entered by table or code, is identical to `totalistic(k=3,r=1,valuation=nu_3,...)`; the T04 catalog label may remain provenance/discoverability metadata but cannot alter its semantic hash or runtime type.

**Owned boundaries.** T04 fixes only the three numeric values, radius one, seven-row case set, and validation range. T06 owns `U(0)=0`; T07 consumes the reflection proof derived from equal weights on a symmetric stencil; T08 owns single-cell initial-condition profiles. Additivity, reversibility, universality, behavior class, frequency, gallery selection, emulation, seed/background, boundary, palette, raster, and observation remain separately typed claims or records.

## Architecture Audit Disposition

T04 remains a strict data/validation preset over the corrected T03 factorized RULE representation and the generic CA runner. It introduces no state, axis implementation, class, or executor. The former Goal 2 handoff is valid only with that interpretation. Its bounded asset repair remains independently open.

## Historical Current API Fit (Evidence Retained)

The schema's separations are directionally correct: `ALPHABET`, `SEED`, `BOUNDARY`, `NEIGHBORHOOD`, `FRONTIER`, and `RULE` are distinct (`simple_programs.md:200-305`); lookup-like rules require fixed arity (`simple_programs.md:643-645`); and all writes use one old snapshot (`simple_programs.md:1768-1791`). Those contracts let the T04 preset return program data while callers choose seed, realization, and view.

Four API mismatches remain:

1. `ALPHABET` declares only a set of values and no rule-owned numeric valuation (`simple_programs.md:200-230`). Current `Alphabet` similarly stores ordered values/family metadata but no valuation (`src/ca/alphabets.py:43-56`), and `Dynamics` carries no alphabet at all (`src/ca/specs.py:23-55`). T04 must resolve to the G2-T03 explicit canonical valuation, not infer arithmetic from tuple rank.
2. The document's broad `TOTALISTIC` category treats active count, color histogram, and numeric sum as interchangeable examples (`simple_programs.md:1964-2032`). D115-D118 require distinct typed summaries; the T04 surface must name the exact equal-weight numeric sum and seven-row case domain. A histogram table has ten radius-one three-color histograms, not seven sum rows, and is not T04.
3. Current `rules.totalistic()` stores only `aggregate="sum"|"count"` and no valuation, arity, image, or case count (`src/ca/rules.py:32-33,198-217`). `rules.lookup()` supports only `lsb_rule_bits`, and because the channel lacks `state_count`, it cannot derive `M=7` or `R=2187` (`src/ca/rules.py:262-295`).
4. Current JSON specs dispatch a closed list of Phase 1 family names (`src/ca/specs.py:117-181`). Catalog discoverability needs a preset resolver at the configuration boundary, but the resolved record must contain the generic T03 rule/spec rather than `family="three_color_totalistic"` reaching rollout.

The required public convenience is therefore `three_color_totalistic(code_or_table)`. It fixes and materializes the canonical valuation, `r=1`, exact-sum descriptor, complete table, and generic shared fixed-lattice spec. It accepts neither seed nor boundary, shape, horizon, filter, class, palette, or view parameters. A manifest may retain `catalog_type="T04"` as nonsemantic provenance, while its structural program record must round-trip identically to the equivalent generic T03 record.

## Current Runtime Fit

**Reusable without T04-specific code:**

- `neighborhoods.eca(radius=1)` produces the exact old `[left,self,right]` selector (`src/ca/neighborhoods.py:551-569`), with its offsets pinned by `tests/test_neighborhoods.py:86-98`.
- `Dynamics` already keeps per-episode `rule_id`, seed state, and step count outside reusable mechanics (`src/ca/specs.py:23-55`; `src/ca/rollout.py:40-85`), and its fixed/periodic/reflective boundary mapping is explicit (`src/ca/specs.py:227-252`). These are useful run/realization boundaries even though Goal 2 must add stable structural program references.
- Single-episode and batch spatial loops compute each new slice from `states[index-1]`, preserving the old-snapshot transition shape (`src/ca/rollout.py:576-640`). Existing single-episode/batch parity tests are useful regression evidence (`tests/test_rollout.py:285-309,345-376,404-424`).
- The current point seed already represents the source single-gray-on-zero run as `point(value=1,fill_value=0)` without entering rule identity (`src/ca/seeds.py:260-313`; `tests/test_seeds.py:71-74`). Viewer palettes are explicit export arguments (`src/ca/viz/export.py:58-62,105-120,286-327`; `tests/test_viz_export.py:280-297`).

**Blocking mismatches inherited from T03:**

- `_channel_state` does compute an integer sum, but ignores the declared `sum` versus `count` mode, forces `int64`, and validates neither the explicit valuation nor the arity/value schema (`src/ca/rollout.py:742-777`). This coincidentally gives the canonical local sum for legal `0/1/2` reads; it is not a sufficient T04 implementation.
- A single channel could numerically produce indices `0..6`, but `_next_spatial_state` always decodes one binary bit with `right_shift` and `&1`, so output color `2` is impossible (`src/ca/rollout.py:643-682`). Adding a ternary conditional here would duplicate T03 semantics and violate D117.
- Both scalar and batch rollout dispatch on named rule families, and generic `lookup` is not executable (`src/ca/rollout.py:145-212,292-330`). T04 cannot be added to either whitelist; G2-T03 must replace these switches with the shared typed rule/result/update protocol.
- Batch IDs are normalized to `numpy.int64` (`src/ca/rollout.py:264-274`). T04 codes happen to fit, but a T04-only exception would preserve the general T03 serialization defect. The preset must use the shared arbitrary-precision tagged-code/program-reference path.
- Seed states are converted to `int64` without validation against a dynamics alphabet/valuation (`src/ca/rollout.py:576-640`), and `RawEpisode`/`RawBatch` expose only numeric rule IDs (`src/ca/specs.py:58-81`). Goal 2 must validate all reads/seeds/fixed exterior values through G2-T03 and preserve the structural program reference.
- Current tests cover 256-rule binary named families only (`tests/test_rules.py:9-40`) and spatial binary outputs (`tests/test_rollout.py:263-424`). No test pins a seven-row table, ternary output, code direction/range, background-changing T04 rule, preset/generic identity, or separation from seed/filter/palette.

Conclusion: current selector, seed, boundary, trace shape, and parallel-loop scaffolding are reusable, but T04 is not executable today. Its implementation is blocked on G2-T03 rather than on any missing T04-specific runtime mechanism.

## Principles Audit

- **Principles 0, 1, and 10 — PASS as a preset.** Evidence shows genuine semantic identity with T03 after fixing `k=3,r=1,nu_3`; the catalog label remains discoverable through strict preset resolution without inventing an executor (`principles.md:3-13,83-87`).
- **Principles 2, 3, 4, and 11 — PASS only through G2-T03.** `AllSites`, the radius-one old read, exact-sum table rule, typed same-site assignment, and atomic update retain one responsibility each. Synchronous old-snapshot update is defining semantics, while no T04-specific result/update exists (`principles.md:15-45,89-93`).
- **Principles 5, 7, and 9 — PASS with explicit coupling.** Fixed support and field values are state; no hidden palette, seed, background, class, or cursor is allowed. `k=3`, canonical valuation, arity three, seven table rows, and output value schema are intrinsically coupled and strictly validated; seed, boundary realization, horizon, and view remain independent (`principles.md:47-57,65-81`).
- **Principles 8 and 12 — PASS at the boundary, current export migration required.** Table/code identity must survive structural serialization, while gallery flattening, coordinates, palette, raster, crop, and batch form remain downstream (`principles.md:71-75,95-103`). Current numeric-only `rule_id` export must migrate through G2-T03 rather than becoming a T04 exception.
- **Principles 13 and 15 — REQUIRED conformance.** Code 777's ternary output/trajectory, code 1's evolving zero background, the 729-versus-50 filter distinction, equal-sum/different-histogram contexts, table/code equality, invalid preset overrides, and preset/generic structural equality are the adversaries that establish constructive fidelity (`principles.md:105-109,117-121`).
- **Principles 14 and 16 — HARD STOP gate.** A `three_color_totalistic` rollout branch, ternary bit-decoder patch, duplicated table/codec, hidden exhaustive expansion, or fixture-specific fallback means the T03 abstraction has not actually composed and must be redesigned (`principles.md:111-127`).

The audit finds no architectural divergence requiring a new construction. It does find a real implementation dependency: T04 cannot ship before the generic G2-T03 path removes the current family/binary restrictions.

## Exact Semantic Oracle

T04 is a strict constructor boundary, not a distinct transition. It fixes `K=3`, `r=1`, canonical valuation, seven sum rows, and codes `0..2186`, then returns the same structural table and shared specification as generic T03. This oracle exhausts all 2,187 programs and all 27 local contexts; checks code/table bijection, permutation invariance, invalid preset inputs, named source rules, T06 and gallery-selection separation, seed independence, exact source runs, and injective behavior-preserving lowering to T02.

```bash
python3 - <<'PY'
from hashlib import sha256
from itertools import product,permutations

K=3; RADIUS=1; M=7; RULES=3**7

def decode(code):
    if isinstance(code,bool) or not isinstance(code,int) or not 0<=code<RULES:
        raise ValueError(code)
    return tuple(code//3**s%3 for s in range(M))
def encode(table):
    if (len(table)!=M or any(isinstance(v,bool) or not isinstance(v,int)
                             or not 0<=v<3 for v in table)):
        raise ValueError(table)
    return sum(v*3**s for s,v in enumerate(table))
def output(code,q): return decode(code)[sum(q)]
def step(code,state):
    return [output(code,(state[i-1] if i else 0,state[i],
                         state[i+1] if i+1<len(state) else 0))
            for i in range(len(state))]
def evolve(code,seed,events,pad=None):
    pad=events+2 if pad is None else pad
    state=[0]*pad+list(seed)+[0]*pad; rows=[state]
    for _ in range(events):
        state=step(code,state); rows.append(state)
    return rows,pad
def word(row):
    used=[i for i,v in enumerate(row) if v]
    return ''.join(map(str,row[min(used):max(used)+1])) if used else ''

def generic_t03(*,k,r,alphabet,valuation,table):
    assert k==len(alphabet)==len(valuation)
    assert tuple(sorted(valuation))==tuple(range(k))
    assert len(table)==1+(k-1)*(2*r+1)
    return ('AggregateLookupRule',tuple(alphabet),tuple(valuation),
            ('EqualWeightIntegerSum',2*r+1),tuple(table),
            ('Assign','AtomicParallelUpdate'))

def t04_preset(code_or_table,**overrides):
    if overrides:
        raise ValueError(tuple(sorted(overrides)))
    table=decode(code_or_table) if isinstance(code_or_table,int) \
          and not isinstance(code_or_table,bool) else tuple(code_or_table)
    encode(table)  # complete canonical T04 validation
    return generic_t03(k=3,r=1,alphabet=(0,1,2),valuation=(0,1,2),
                       table=table)

assert (K,RADIUS,M,RULES)==(3,1,7,2187)
for code in range(RULES):
    table=decode(code)
    assert encode(table)==code
    for q in product(range(3),repeat=3):
        want=table[sum(q)]
        assert output(code,q)==want
        assert all(output(code,p)==want for p in set(permutations(q)))

for bad in (-1,2187,True,False,1.0,'777',None):
    try: decode(bad); raise AssertionError(bad)
    except ValueError: pass
    try: t04_preset(bad); raise AssertionError(('preset',bad))
    except (ValueError,TypeError): pass
for bad in ((0,)*6,(0,)*8,(0,0,0,0,0,0,3),
            (0,0,0,0,0,0,True)):
    try: encode(bad); raise AssertionError(bad)
    except ValueError: pass

# Preset resolution is semantic identity with generic T03, not a family tag.
generic777=generic_t03(k=3,r=1,alphabet=(0,1,2),valuation=(0,1,2),
                       table=decode(777))
assert t04_preset(777)==t04_preset(decode(777))==generic777
assert sha256(repr(t04_preset(777)).encode()).hexdigest()==\
       sha256(repr(generic777).encode()).hexdigest()
for field in ('k','r','valuation','aggregate','alphabet','arity','executor',
              'update','seed','boundary','filter','class_name','palette'):
    try:
        t04_preset(777,**{field:'override'})
        raise AssertionError(field)
    except ValueError:
        pass

assert decode(777)==(0,1,2,1,0,0,1)
assert ''.join(map(str,reversed(decode(777))))=='1001210'
assert decode(867)==(0,1,0,2,1,0,1)
assert decode(420)==(0,2,1,0,2,1,0)
assert all(output(420,q)==(-sum(q))%3
           for q in product(range(3),repeat=3))
assert any(output(421,q)!=(-sum(q))%3
           for q in product(range(3),repeat=3))

# T06 and the page-76 scan are restrictions/selections, never T04 identity.
assert sum(code%3==0 for code in range(RULES))==3**6==729
assert output(1,(0,0,0))==1
scan=tuple(range(993,1141,3))
assert len(scan)==50 and scan[0]==993 and scan[-1]==1140
assert all(code%3==0 for code in scan)
assert 990%3==1143%3==0 and 990 not in scan and 1143 not in scan

rows,pad=evolve(777,[1],8)
trace=tuple(word(row) for row in rows)
assert trace==('1','111','12121','1100011','122101221',
              '11001210011','1221110111221','110001222100011',
              '12210110101101221')
rows,pad=evolve(867,[1],50,pad=50)
blob=bytes(v for row in rows for v in row)
assert len(blob)==51*101
assert tuple(blob.count(v) for v in range(3))==(3692,958,501)
assert sha256(blob).hexdigest()==\
       '185170c0866f76d129fbf3a8843cc731f98b9f012cb98286f01e420532fb53d9'

# Seed is run data: one program admits distinct valid initial conditions.
program=decode(777)
run1,_=evolve(777,[1],4); run2,_=evolve(777,[2],4)
assert program==decode(777) and run1!=run2

# Exhaustive lowering preserves behavior but is not the preset's identity.
def address(q): return 9*q[0]+3*q[1]+q[2]
def lower(code):
    return tuple(output(code,q) for q in product(range(3),repeat=3))
seen=set()
for code in range(RULES):
    full=lower(code)
    full_code=sum(v*3**i for i,v in enumerate(full))
    assert full_code not in seen; seen.add(full_code)
    assert all(full[address(q)]==output(code,q)
               for q in product(range(3),repeat=3))
assert len(seen)==RULES

print('T04 semantic oracle: PASS')
print('rule_count=',RULES,'quiescent_count=',729,'gallery_count=',len(scan))
print('rule777_table=',decode(777),'trace=',','.join(trace))
print('rule867_51x101_sha256=',sha256(blob).hexdigest())
PY
```

Recorded output:

```text
T04 semantic oracle: PASS
rule_count= 2187 quiescent_count= 729 gallery_count= 50
rule777_table= (0, 1, 2, 1, 0, 0, 1) trace= 1,111,12121,1100011,122101221,11001210011,1221110111221,110001222100011,12210110101101221
rule867_51x101_sha256= 185170c0866f76d129fbf3a8843cc731f98b9f012cb98286f01e420532fb53d9
```

## Asset and Raster Audit

T03's audit is the physical superset; this section independently re-hashes and re-executes the strict `k=3,r=1` T04 subset. The strict Chapter 3 sequence begins with code `777` on printed page 60 and ends with code `1599` on printed page 70; page 71 switches to mobile automata. Later direct profile evidence includes the Chapter 6 code-`357`/`1329` structure-and-growth sequence, while the page-870 additive/Pascal panel and the Life spacefiller panels are relation-only. A code label is program evidence; a single-gray start, numbered or random field, search bound, behavior class, period, horizon, crop, and palette remain run/property/view evidence.

### Included direct T04 assets

All paths are relative to `ref/A-New-Kind-of-Science/`.

| Asset path | Bytes | Dimensions | SHA-256 | Exact source-permitted role |
|---|---:|---:|---|---|
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_75_Figure_6.jpeg` | 51,178 | `610x446` | `acb13963632286960ca61b616ff2f45a940750f3ab7deb5e6fbf696543015c15` | Canonical code-`777` rule/table and 43-by-22 initial-inclusive grid. Only this caption explicitly supplies `0/1/2 = white/gray/black`, sum order, and complete raster geometry. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_76_Figure_2.jpeg` | 174,691 | `1109x1279` | `8c11659c8bd63d37a972c5ffab376b62948f7c4e05f9fd10f239e51464f4084d` | Fifty labelled codes `993,996,...,1140`, selected from rules that preserve white background. This is a representative scan, not all 729 codes satisfying `U(0)=0`. Seed/horizon are not serialized. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_77_Figure_6.jpeg` | 128,836 | `892x716` | `4c1f8894016156dc4d473e911e0fa5c7db16711a8c2873fa493fb7854ad41c66` | Single-gray finite/repeating examples `600,843,870,1086,1167,1329,1572,1815,1842`; period/class/crop are observers. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_78_Figure_2.jpeg` | 90,930 | `1107x615` | `5c5ca56f3e8141c3aa4d7648f3ebe34a911515bf9dfc9118795135736f69b879` | Single-gray growing/repetitive examples `219,957,966,1884`; horizon convention is unstated. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_78_Figure_4.jpeg` | 81,348 | `1134x621` | `088016843cb7d74ad621ebed323401dfb9783ce061ece275ba36b0815c7dfa28` | Single-gray nested examples `237,420,948,1749`; nesting/additivity remain properties. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_79_Picture_2.jpeg` | 278,065 | `886x1399` | `355d13fde85b89c2e3e26d1ae199e30ad2191b0bcbd3d4c89ac76785fa1ebc86` | Codes `177,912,2040`, described as 300 steps. Initial-state inclusion and resampling/crop remain unstated. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_81_Picture_1.jpeg` | 75,030 | `826x446` | `0617e6b01a1faa43e968051ff8716171b665e79d087c8c13a47811c0520f3014` | Complex-behavior code `1041`; identity/property evidence only. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_81_Picture_2.jpeg` | 86,949 | `816x429` | `6efe4dc8703a3045bd6189f930a0cdb44e59dc71f38dc91a52e8faa84e801a7e` | Complex-behavior code `1635`; continued in Picture 82/1. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_81_Picture_3.jpeg` | 75,408 | `869x470` | `b3812f8742bf08299270512de2cdffa57ac14be5b10a6cdefa60d4878173553c` | Complex-behavior code `2049`; continued in Picture 83/1. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_82_Picture_1.jpeg` | 423,048 | `1061x1381` | `aa534aa358e74235ef5de86980c5c6f0895bac2b616e990c1cda7253639a4511` | Long code-`1635` continuation; “3,000 steps” is view provenance, not a successor limit. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_83_Picture_1.jpeg` | 513,252 | `1067x1387` | `cd4f0434c12f9b86bdde3730270451df2dfb503194d22bc04d0609973e9d3a77` | Long code-`2049` continuation; same disposition. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_84_Picture_2.jpeg` | 74,243 | `764x747` | `02782253cc66a9de075af5d1d02f224645e443040f5ff6001fef6467a7013cbe` | Codes `357,600,1599,2058`, described as 250 steps; edge-of-growth is an observer label. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_85_Picture_2.jpeg` | 345,552 | `1107x1360` | `2374289d970042909316f68cf240379d6f2826ba90dab95db0a317e672b91b0f` | Code `1599`, single-gray start, three 3,000-step columns. Resolution after 8,282 steps into 31 structures is analysis, not halting. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_122_Figure_2.jpeg` | 186,914 | `1098x1164` | `ccd7a43a495d01a22300c4b9abbb3ff1b13a3ef37389e77ca491ec805cbaa822` | Mixed-color comparison whose T04 column is codes `578..585`; two-, four-, and five-color columns are in-asset controls, not T04 programs. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_249_Picture_1.jpeg` | 273,017 | `1082x1403` | `f7b2834be41656cff9512b7affdd5fa57640bbbb6ecd93da1440202bf113f7ef` | Codes `1002,1005,...,1095` from an unspecified random field; it overlaps Picture 76/2 in code identity but has different run/view provenance. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_251_Picture_1.jpeg` | 429,298 | `1123x1383` | `41cfc762284fdcd65e5663fb7631aa4c504aea46a746a8a4ed24407b76b89196` | Class-4 code `1815`, 1,500 displayed steps from an unspecified random field. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_252_Picture_2.jpeg` | 556,865 | `1121x1377` | `120e95a57f683744ff3e71981f4fa07ff850d0cad5633bf4d2f27906a76e909f` | Class-4 code `2007`; same random-run disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_253_Picture_1.jpeg` | 511,097 | `1227x1519` | `148a433a11b4889c91c1a7be3c6f00172a3961428e6d41c47a06954136245faf` | Class-4 code `1659`; the visible label and Actual Index repair monolith `BOOK:2834`'s isolated OCR/page-number contamination `238`. Notes code `1662` is a separate, unpictured named rule. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_254_Picture_1.jpeg` | 568,496 | `1117x1383` | `d32b7fc3dedc9f262e5a3d3d928d1d7d94d1a219fd75aeeefdb988c74869a168` | Class-4 code `2043`; same disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_2.jpeg` | 7,400 | `273x171` | `b175f64e60cf41042d8ba6a11ed8d04eec4a8101bef8f9f231aae532eca6ca06` | Borderline-class code `219`; classification is a property. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_3.jpeg` | 13,612 | `259x167` | `00ef0063254d4f75734cd76d8f2d07de4ae1d6b041b9664197c2da99641d8b14` | Borderline-class code `438`; same disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_4.jpeg` | 9,310 | `267x186` | `700d71a0beb145c953ca87f4d8649aecd7b7d60df69ccd569cba02f6daeb1acc` | Borderline-class code `1380`; same disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_5.jpeg` | 11,188 | `273x165` | `ae44e4411841a03fced5b5114f6cef4be62793c6a58c9a4ce6c357d214c7ce35` | Borderline-class code `1632`; same disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_297_Picture_4.jpeg` | 117,894 | `1127x415` | `26b299987a91daf8d15fc226c845c7efa7d55b9aa4221a4e6d41646b8c384204` | Code `357` from a completely random initial condition, exhibiting the persistent structures used to introduce the later search. Random sample and crop are not serialized. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_297_Picture_6.jpeg` | 156,786 | `1123x408` | `b94ac983e3496b023a1a991b15a701de9a1c4c5cba75a84b16254c497a1c76f1` | Code `1329` companion under the same random-run/class-4 disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_301_Picture_2.jpeg` | 134,324 | `906x699` | `3e9aec2832697e07ea20391c1454e022bc8578fcfb4c126bbb53e6fdfe3f6eb3` | Code-`357` base-3 initial-condition search: labelled `(28,48)`, `(7,795,19)`, `(1,706,588,26)`, `(4,803,890,41R)`, `(154,596,664,12)`, `(514,454,827,48L)`; the first two billion were tested and no period below 5 exists. Labels are property fixtures, not six new programs. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_302_Picture_3.jpeg` | 123,792 | `1036x712` | `4ec6db32d4f0b659a8519110b7885e05487e68d0348b390323daa55e7b322fd1` | Code-`1329` structures labelled by initial condition/period: `1/78`, `52/7`, `400/2`, `800/12`, `916/31R`, `2,617/9`, `2,669/48R`, `97,357/2`, `659,197/9`. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_303_Picture_2.jpeg` | 136,635 | `616x1053` | `26ec2731176f7ef4b471b4f395f3968eefa69e0eba88a3f672268129d68e07aa` | Code `1329`, initial condition `54,889`: a 10-cell block produces unbounded growth whose moving right part has period 256 and leaves infinitely many persistent structures. No exact displayed horizon/crop is stated. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_304_Picture_2.jpeg` | 179,601 | `1109x1363` | `21cc5432bcfcc379619d43c076f3102a3e12d64cd724d9fe5709055b72874ecf` | Further code-`1329` unbounded-growth profiles from initial conditions `54,889`, `97,439`, `166,426`, `115,396`, and `2,069,116`, demonstrating both complex and simple outcomes. |
| `CHAPTERS/9-Fundamental-Physics/Images/_page_541_Picture_3.jpeg` | 37,411 | `436x268` | `83d828ba45f3f3e7390bf66183643a32c3c7b83646cc3880aedf099a49284c1e` | Code `294`, persistent structures on an unspecified largely random background. |
| `CHAPTERS/9-Fundamental-Physics/Images/_page_541_Picture_4.jpeg` | 43,238 | `418x250` | `d96c865b43b912ce4e2d6f0c2ddf659eed32f17db48c151161c364187fcc7a1f` | Code `1893`, persistent boundaries on an unspecified largely random background. |
| `CHAPTERS/11-The-Notion-of-Computation/Images/_page_707_Figure_1.jpeg` | 327,160 | `1130x1111` | `974e12d28e8acc6fb4af26f7b1dd09eae1f30d802666a61f41abed8ec2d42e19` | Mixed class-4 asset whose direct T04 panel `(d)` is code `1815`; ECA, second-order, and binary radius-two panels are in-asset controls. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_753_Picture_3.jpeg` | 164,036 | `912x565` | `8cfad05d53abb9791d37dd6d8262ec12dbc08bb1d72866ce34c46ecb99a94a88` | Codes `870,843,1599` illustrating reducibility/irreducibility; property labels are downstream. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_25.jpeg` | 5,511 | `211x117` | `d53637ce9ec50330d5fa6239b23f48d57b563266a0085a23517d4538020fd5fb` | Exact Notes invocation `CellularAutomaton[{867,{3,1},1},{{1},0},50]`: code `867`, one `1`, repeating-`0` background, 50 updates. |
| `BACK-MATTER/Index/Images/_page_963_Picture_11.jpeg` | 3,717 | `136x152` | `7c660bbbb03b2d3116aab32cd50a5a3ff094961d49b403148531b36759335d6b` | Notes frequency-of-classes chart explicitly labelled `k=3,r=1`; class frequency is aggregate evidence only. |

### Explicit exclusions and relation-only evidence

| Asset path | Bytes | Dimensions | SHA-256 | Disposition |
|---|---:|---:|---|---|
| `CHAPTERS/11-The-Notion-of-Computation/Images/_page_670_Figure_1.jpeg` | 281,966 | `1064x1224` | `a1a2a5c04b509ecc0357273387b2950d179478c65406427751904987ec9e8d3e` | Relation-only: T04 code `1599` is block-emulated by a binary radius-five CA. Encoding/decoding and emulator events are not T04. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_21.jpeg` | 25,918 | `583x225` | `5f829c7776b53963e578df5a783553320da171c4e1c4d92c470899ec5bb3e40d` | Relation-only: the `k=3` member of a `k=2..7` additive/Pascal-modulo-`k` gallery supplies the page-870 comparison cited for totalistic code `420`; the displayed rule is not labelled as code `420`. |
| `BACK-MATTER/Index/Images/_page_980_Picture_15.jpeg` | 4,385 | `160x195` | `641317f32d429dd61b8353e1ebe65bd80f30950df78f0ebdc3a7f99b6bd26cd9` | Relation-only: step 5 of Life's 206-cell two-dimensional spacefiller, explicitly described as analogous to the code-`1329` growth profiles. |
| `BACK-MATTER/Index/Images/_page_980_Picture_16.jpeg` | 5,858 | `172x187` | `90df3d1e1e99ed74dd1844654ff41b04b23f6fe22552cefa2b72f659cd0c5fda` | Relation-only: step 50 companion of the same Life analogy. |
| `BACK-MATTER/Index/Images/_page_980_Picture_17.jpeg` | 8,261 | `223x207` | `3ad70eb7f740edf7749700ff107f08306830f3e3fd617f2df3f9e7e559178e21` | Relation-only: history view of that spacefiller; two-dimensional Life mechanics remain outside T04. |
| `BACK-MATTER/Index/Images/_page_1092_Picture_6.jpeg` | 21,682 | `583x141` | `b13e50f8bb2f7e905b8580ea94d93c7295e5967125aa8042defe76936bdb1dd6` | Relation-only: feature-extraction application of the 16 even-numbered binary five-neighbor totalistic rules governed by `BOOK:17431`; not T04 execution. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_74_Picture_5.jpeg` | 134,131 | `858x423` | `713c4c55c6a004d76c5e47f1f39513bb1656f35feb0fe9aa72c4503ca311cdc6` | Immediate preceding rule-73 ECA: two-color exhaustive ordered rule. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_86_Picture_7.jpeg` | 30,221 | `240x500` | `59213fbf1a0e6904a6566043c889acd32853d799d5a71bfec1e2d0c45bb1eec5` | First post-T04 mobile evolution: one active site and sequential movement. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_86_Picture_8.jpeg` | 7,295 | `506x51` | `d844f2419d7ff2a748a93e4ae6dd09c947bf5ed0723aa1defb4354c810b1fb25` | Mobile rule diagram paired with Picture 86/7; all later mobile galleries inherit this boundary. |
| `CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_171_Picture_5.jpeg` | 4,640 | `277x91` | `6695e1c946cf6adaa04a3915f2c720f69de4d18b74a81a01aaab346052119455` | Continuous gray average-map analog; continuous value carrier, not three colors. |
| `CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_185_Picture_9.jpeg` | 3,425 | `213x114` | `abfbc90a8bdab839ac452194adf8f7e30258e877967a79ac71db59b1a716df75` | Two-dimensional center-plus-four-neighbor totalistic form; different support. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_248_Figure_2.jpeg` | 281,697 | `1086x1389` | `b2a20cb8095eb211fedd963d622222ca98fe0428f397b71bef90db8fa6871957` | Binary radius-two totalistic gallery; lower color count and larger radius. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_256_Figure_2.jpeg` | 328,297 | `1092x1367` | `1c4967f6967d8e813b2a281e2615dc8bef272eb57789b60e23c950de5e6bc01f` | Four-color radius-one totalistic class sequence; T05 rather than T04. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_261_Figure_2.jpeg` | 309,273 | `1109x1297` | `49f35fe65202ef7fbfee2da92b7460d36fc329b66a553782ebf8991f237944dd` | Two-dimensional five-cell totalistic random gallery. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_262_Figure_2.jpeg` | 240,733 | `1013x1291` | `23df7e86bf96a148a17c13847eb53c773a24f86cc5a24f2e1a550f79b94439e3` | Continuation of the two-dimensional binary five-cell totalistic random gallery; geometry/color-count control. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_263_Figure_2.jpeg` | 295,433 | `1195x1355` | `71f5ac8784f493b664a93aff52e157e1ac7bf94a6b2e910f98de9fef663736ec` | One-dimensional slice views of the same rules, visibly labelled `4,12,24,38,30,52`; observer/geometry control. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_297_Picture_2.jpeg` | 50,047 | `1111x408` | `953c15d2e64464aceadb6181639cf36973db9513d6e0b7fc3fb43564efc65be8` | Interleaved code-`20` binary radius-two class-4 control; direct generic-T03 evidence, not T04. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_298_Figure_2.jpeg` | 209,088 | `1159x1297` | `7cacf2667a3f923d35106ec7eff09b9ce551d79dd828f8661458dd121bda09df` | Code-`20` control over every binary initial condition supported in a region of size below nine. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_299_Picture_3.jpeg` | 127,700 | `1150x600` | `32d4ed4b16a083fb731c37cc80c64efb9995756808c316a0ced0dea0e9bd5475` | Code-`20` structures found by testing the first 25 billion binary initial conditions. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_300_Figure_1.jpeg` | 286,267 | `1150x1192` | `ee5ea91d3855bf31bd793f02677c0c19d9203ac20532b3b7bb07df838065294c` | Code-`20` exhaustive persistent-structure control through period 15. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_305_Picture_2.jpeg` | 642,889 | `1184x1342` | `7e75ba3d0cb57a0b35d5a7b29e803386617e1ede22eefae19ce6e21fc465a9c9` | Next-section rule-`110` binary boundary: random initial condition with 14-cell background blocks repeating every 7 steps. |
| `CHAPTERS/9-Fundamental-Physics/Images/_page_451_Picture_6.jpeg` | 187,275 | `1103x483` | `e7bbbefb729e76dd5d080d0b841a485ece898d9c3197780b4871c742d61a4e89` | Three-color nearest-neighbor reversible rules governed by the quoted E14 caption; unrestricted ordered tables, not seven-row totalistic rules. |
| `CHAPTERS/9-Fundamental-Physics/Images/_page_476_Figure_3.jpeg` | 295,434 | `1149x988` | `e661d9c28572ba62f75cf4b8a085e1580caf88b7c1c88bdd3c60a018e32ab108` | Three-color number-conserving reversible block cellular automata; block updates are outside T04. |
| `CHAPTERS/10-Processes-of-Perception-and-Analysis/Images/_page_566_Figure_2.jpeg` | 140,400 | `1032x699` | `6d66d95c8e3c286272cded005d60557ce7a075ffebfd268486c23abe13a29a1e` | Two-dimensional outer-totalistic codes `54,222,374`; center is retained separately. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_847_Figure_1.jpeg` | 111,064 | `1041x385` | `2d36e7eaeb3b073e68621ef5f9c1c397ae24ddc74fe06f26e62546ccc3af2902` | Purpose/doubling comparison containing a searched three-color general rule `5407067979`; application and unrestricted rule identity exclude it. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_848_Figure_2.jpeg` | 247,033 | `1194x1308` | `0bfecfeff1bd81072838e39704fc6572632dee083f91ddc4370909b0e2c5b5dd` | Gallery of three-color general rules selected to double an input; purpose/search evidence, not T04 programs. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_769_Figure_1.jpeg` | 298,516 | `1065x1308` | `a980effe214906d991e8ca9180cb9f9d6eade2f978a8358487a60bb1728058f3` | Four-color totalistic code `1004600`; higher-color control. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_897_Picture_19.jpeg` | 37,091 | `553x155` | `2cedbff5433363c86786feea8804c95229179daf455f07ee8071d6345223894b` | Binary radius-two code `10`; direct T03 evidence but lower-color/radius control for T04. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_897_Picture_20.jpeg` | 77,026 | `543x329` | `ee9cadafa6b0b5a45d9cfb4ed310aff751e84f46a86277821e9f971f3c067b3f` | Long companion view of the same code-`10` control. |
| `BACK-MATTER/Index/Images/_page_963_Picture_8.jpeg` | 3,114 | `144x152` | `1fb4f0b4c03d8ba9f9fdeb67a0bbda2d786ed7ceeb13cdd8c31337ccd54bcdfb` | Frequency chart `k=2,r=1`; lower-color control. |
| `BACK-MATTER/Index/Images/_page_963_Picture_9.jpeg` | 3,226 | `136x148` | `515f5de1423a9164ed6def92d786346f64c15a0a87ba07b723c069e62829caf6` | Frequency chart `k=2,r=2`; lower-color/radius control. |
| `BACK-MATTER/Index/Images/_page_963_Picture_10.jpeg` | 3,654 | `138x158` | `4b5ff621a668c5b706cdec0481cf3849facb7395d256dfd7c39b471d95fd018f` | Frequency chart `k=2,r=3`; lower-color/radius control. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_23.jpeg` | 4,478 | `160x117` | `132528352f363e52a20e73e1e8341203126448c0c6c8545eed48626eaddac16c` | Adjacent `k=3,r=1` general ordered-table code `921408`; T02, not totalistic. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_28.jpeg` | 5,342 | `205x110` | `2da239aceec3720e5aeccd5de8898c37fe7e975230814c0b3a8e3dcacbde9096` | Adjacent function-callback neighborhood rule; not a seven-row T04 table. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_31.jpeg` | 4,370 | `117x117` | `ca086555513a6d8ba5bcbe92d97af26e55aa899cf629e0ab61d8fa8c71b81586` | Adjacent 2D nine-neighbor totalistic code `3702`; different geometry. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_23.jpeg` | 4,207 | `139x141` | `f14931f6bb008435e34961947dce7b11d5ec6d0bd4cc5b936bcee81b830adc0a` | First post-Pascal boundary: a modulo-2 integer-function picture, not a three-color CA run. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_24.jpeg` | 5,507 | `135x138` | `5b302ed9d6c9cbee590270c7bdc169b62b554b0e186a94fdb3d1952a69c0f8c5` | `Multinomial[m,n]` modulo-2 companion; same exclusion. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_25.jpeg` | 4,057 | `138x145` | `f5eb9593ba90b4b240dc6990bb0e7204066cc48e81e82b96186029ff866d40da` | `StirlingS1[m,n]` modulo-2 companion; same exclusion. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_26.jpeg` | 4,999 | `135x155` | `badba07cc053bdf7f4e5b41d7d90b2b248d8acd75b9728898e10c69a59c7ceec` | `StirlingS2[m,n]` modulo-2 companion; same exclusion. |
| `BACK-MATTER/Colophon/Images/_page_1132_Picture_2.jpeg` | 68,468 | `606x308` | `422ce8c21c465e2ffdffdb0f691f9521a21b9389897336dd4e4a2c716295c589` | General three-color two-neighbor code `2144`; an ordered/unrestricted class-4 control, not a totalistic seven-row rule. |

The monolith omits `Images/` from links; chapter splits reference these same bytes rather than duplicate files. Page-883/885 assets are Notes-for-Chapter-2 evidence despite Chapter-12 placement. Page-963/980/1092 Notes images are physically under `BACK-MATTER/Index/Images`, while page 1132 is under `BACK-MATTER/Colophon/Images`. The Chapter 6 sequence at `BOOK:3314-3380` is deliberately interleaved: six code-`357`/`1329` assets are included, four code-`20` panels and the following rule-`110` panel are excluded. The page-261/262/263 gallery closes at the same six two-dimensional totalistic rules; page 264 switches to Life/outer-totalistic code 224. The four E14 image-governing captions at `BOOK:5222,5486,10395,10411` route to explicit reversible/block/purpose controls. The independent oracle below is authoritative for T04's 35 included, 34 excluded, and six relation-only dispositions.

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
'CHAPTERS/6-Starting-from-Randomness/Images/_page_249_Picture_1.jpeg':(273017,1082,1403,'f7b2834be41656cff9512b7affdd5fa57640bbbb6ecd93da1440202bf113f7ef','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_251_Picture_1.jpeg':(429298,1123,1383,'41cfc762284fdcd65e5663fb7631aa4c504aea46a746a8a4ed24407b76b89196','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_252_Picture_2.jpeg':(556865,1121,1377,'120e95a57f683744ff3e71981f4fa07ff850d0cad5633bf4d2f27906a76e909f','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_253_Picture_1.jpeg':(511097,1227,1519,'148a433a11b4889c91c1a7be3c6f00172a3961428e6d41c47a06954136245faf','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_254_Picture_1.jpeg':(568496,1117,1383,'d32b7fc3dedc9f262e5a3d3d928d1d7d94d1a219fd75aeeefdb988c74869a168','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_2.jpeg':(7400,273,171,'b175f64e60cf41042d8ba6a11ed8d04eec4a8101bef8f9f231aae532eca6ca06','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_3.jpeg':(13612,259,167,'00ef0063254d4f75734cd76d8f2d07de4ae1d6b041b9664197c2da99641d8b14','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_4.jpeg':(9310,267,186,'700d71a0beb145c953ca87f4d8649aecd7b7d60df69ccd569cba02f6daeb1acc','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_5.jpeg':(11188,273,165,'ae44e4411841a03fced5b5114f6cef4be62793c6a58c9a4ce6c357d214c7ce35','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_297_Picture_4.jpeg':(117894,1127,415,'26b299987a91daf8d15fc226c845c7efa7d55b9aa4221a4e6d41646b8c384204','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_297_Picture_6.jpeg':(156786,1123,408,'b94ac983e3496b023a1a991b15a701de9a1c4c5cba75a84b16254c497a1c76f1','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_301_Picture_2.jpeg':(134324,906,699,'3e9aec2832697e07ea20391c1454e022bc8578fcfb4c126bbb53e6fdfe3f6eb3','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_302_Picture_3.jpeg':(123792,1036,712,'4ec6db32d4f0b659a8519110b7885e05487e68d0348b390323daa55e7b322fd1','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_303_Picture_2.jpeg':(136635,616,1053,'26ec2731176f7ef4b471b4f395f3968eefa69e0eba88a3f672268129d68e07aa','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_304_Picture_2.jpeg':(179601,1109,1363,'21cc5432bcfcc379619d43c076f3102a3e12d64cd724d9fe5709055b72874ecf','I'),
'CHAPTERS/9-Fundamental-Physics/Images/_page_541_Picture_3.jpeg':(37411,436,268,'83d828ba45f3f3e7390bf66183643a32c3c7b83646cc3880aedf099a49284c1e','I'),
'CHAPTERS/9-Fundamental-Physics/Images/_page_541_Picture_4.jpeg':(43238,418,250,'d96c865b43b912ce4e2d6f0c2ddf659eed32f17db48c151161c364187fcc7a1f','I'),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_707_Figure_1.jpeg':(327160,1130,1111,'974e12d28e8acc6fb4af26f7b1dd09eae1f30d802666a61f41abed8ec2d42e19','I'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_753_Picture_3.jpeg':(164036,912,565,'8cfad05d53abb9791d37dd6d8262ec12dbc08bb1d72866ce34c46ecb99a94a88','I'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_25.jpeg':(5511,211,117,'d53637ce9ec50330d5fa6239b23f48d57b563266a0085a23517d4538020fd5fb','I'),
'BACK-MATTER/Index/Images/_page_963_Picture_11.jpeg':(3717,136,152,'7c660bbbb03b2d3116aab32cd50a5a3ff094961d49b403148531b36759335d6b','I'),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_670_Figure_1.jpeg':(281966,1064,1224,'a1a2a5c04b509ecc0357273387b2950d179478c65406427751904987ec9e8d3e','R'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_21.jpeg':(25918,583,225,'5f829c7776b53963e578df5a783553320da171c4e1c4d92c470899ec5bb3e40d','R'),
'BACK-MATTER/Index/Images/_page_980_Picture_15.jpeg':(4385,160,195,'641317f32d429dd61b8353e1ebe65bd80f30950df78f0ebdc3a7f99b6bd26cd9','R'),
'BACK-MATTER/Index/Images/_page_980_Picture_16.jpeg':(5858,172,187,'90df3d1e1e99ed74dd1844654ff41b04b23f6fe22552cefa2b72f659cd0c5fda','R'),
'BACK-MATTER/Index/Images/_page_980_Picture_17.jpeg':(8261,223,207,'3ad70eb7f740edf7749700ff107f08306830f3e3fd617f2df3f9e7e559178e21','R'),
'BACK-MATTER/Index/Images/_page_1092_Picture_6.jpeg':(21682,583,141,'b13e50f8bb2f7e905b8580ea94d93c7295e5967125aa8042defe76936bdb1dd6','R'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_74_Picture_5.jpeg':(134131,858,423,'713c4c55c6a004d76c5e47f1f39513bb1656f35feb0fe9aa72c4503ca311cdc6','X'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_86_Picture_7.jpeg':(30221,240,500,'59213fbf1a0e6904a6566043c889acd32853d799d5a71bfec1e2d0c45bb1eec5','X'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_86_Picture_8.jpeg':(7295,506,51,'d844f2419d7ff2a748a93e4ae6dd09c947bf5ed0723aa1defb4354c810b1fb25','X'),
'CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_171_Picture_5.jpeg':(4640,277,91,'6695e1c946cf6adaa04a3915f2c720f69de4d18b74a81a01aaab346052119455','X'),
'CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_185_Picture_9.jpeg':(3425,213,114,'abfbc90a8bdab839ac452194adf8f7e30258e877967a79ac71db59b1a716df75','X'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_248_Figure_2.jpeg':(281697,1086,1389,'b2a20cb8095eb211fedd963d622222ca98fe0428f397b71bef90db8fa6871957','X'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_256_Figure_2.jpeg':(328297,1092,1367,'1c4967f6967d8e813b2a281e2615dc8bef272eb57789b60e23c950de5e6bc01f','X'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_261_Figure_2.jpeg':(309273,1109,1297,'49f35fe65202ef7fbfee2da92b7460d36fc329b66a553782ebf8991f237944dd','X'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_262_Figure_2.jpeg':(240733,1013,1291,'23df7e86bf96a148a17c13847eb53c773a24f86cc5a24f2e1a550f79b94439e3','X'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_263_Figure_2.jpeg':(295433,1195,1355,'71f5ac8784f493b664a93aff52e157e1ac7bf94a6b2e910f98de9fef663736ec','X'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_297_Picture_2.jpeg':(50047,1111,408,'953c15d2e64464aceadb6181639cf36973db9513d6e0b7fc3fb43564efc65be8','X'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_298_Figure_2.jpeg':(209088,1159,1297,'7cacf2667a3f923d35106ec7eff09b9ce551d79dd828f8661458dd121bda09df','X'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_299_Picture_3.jpeg':(127700,1150,600,'32d4ed4b16a083fb731c37cc80c64efb9995756808c316a0ced0dea0e9bd5475','X'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_300_Figure_1.jpeg':(286267,1150,1192,'ee5ea91d3855bf31bd793f02677c0c19d9203ac20532b3b7bb07df838065294c','X'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_305_Picture_2.jpeg':(642889,1184,1342,'7e75ba3d0cb57a0b35d5a7b29e803386617e1ede22eefae19ce6e21fc465a9c9','X'),
'CHAPTERS/9-Fundamental-Physics/Images/_page_451_Picture_6.jpeg':(187275,1103,483,'e7bbbefb729e76dd5d080d0b841a485ece898d9c3197780b4871c742d61a4e89','X'),
'CHAPTERS/9-Fundamental-Physics/Images/_page_476_Figure_3.jpeg':(295434,1149,988,'e661d9c28572ba62f75cf4b8a085e1580caf88b7c1c88bdd3c60a018e32ab108','X'),
'CHAPTERS/10-Processes-of-Perception-and-Analysis/Images/_page_566_Figure_2.jpeg':(140400,1032,699,'6d66d95c8e3c286272cded005d60557ce7a075ffebfd268486c23abe13a29a1e','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_847_Figure_1.jpeg':(111064,1041,385,'2d36e7eaeb3b073e68621ef5f9c1c397ae24ddc74fe06f26e62546ccc3af2902','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_848_Figure_2.jpeg':(247033,1194,1308,'0bfecfeff1bd81072838e39704fc6572632dee083f91ddc4370909b0e2c5b5dd','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_769_Figure_1.jpeg':(298516,1065,1308,'a980effe214906d991e8ca9180cb9f9d6eade2f978a8358487a60bb1728058f3','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_897_Picture_19.jpeg':(37091,553,155,'2cedbff5433363c86786feea8804c95229179daf455f07ee8071d6345223894b','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_897_Picture_20.jpeg':(77026,543,329,'ee9cadafa6b0b5a45d9cfb4ed310aff751e84f46a86277821e9f971f3c067b3f','X'),
'BACK-MATTER/Index/Images/_page_963_Picture_8.jpeg':(3114,144,152,'1fb4f0b4c03d8ba9f9fdeb67a0bbda2d786ed7ceeb13cdd8c31337ccd54bcdfb','X'),
'BACK-MATTER/Index/Images/_page_963_Picture_9.jpeg':(3226,136,148,'515f5de1423a9164ed6def92d786346f64c15a0a87ba07b723c069e62829caf6','X'),
'BACK-MATTER/Index/Images/_page_963_Picture_10.jpeg':(3654,138,158,'4b5ff621a668c5b706cdec0481cf3849facb7395d256dfd7c39b471d95fd018f','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_23.jpeg':(4478,160,117,'132528352f363e52a20e73e1e8341203126448c0c6c8545eed48626eaddac16c','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_28.jpeg':(5342,205,110,'2da239aceec3720e5aeccd5de8898c37fe7e975230814c0b3a8e3dcacbde9096','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_31.jpeg':(4370,117,117,'ca086555513a6d8ba5bcbe92d97af26e55aa899cf629e0ab61d8fa8c71b81586','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_23.jpeg':(4207,139,141,'f14931f6bb008435e34961947dce7b11d5ec6d0bd4cc5b936bcee81b830adc0a','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_24.jpeg':(5507,135,138,'5b302ed9d6c9cbee590270c7bdc169b62b554b0e186a94fdb3d1952a69c0f8c5','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_25.jpeg':(4057,138,145,'f5eb9593ba90b4b240dc6990bb0e7204066cc48e81e82b96186029ff866d40da','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_26.jpeg':(4999,135,155,'badba07cc053bdf7f4e5b41d7d90b2b248d8acd75b9728898e10c69a59c7ceec','X'),
'BACK-MATTER/Colophon/Images/_page_1132_Picture_2.jpeg':(68468,606,308,'422ce8c21c465e2ffdffdb0f691f9521a21b9389897336dd4e4a2c716295c589','X'),
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

counts={'I':0,'X':0,'R':0}; digests=set()
for name,(size,w,h,digest,kind) in items.items():
    data=(ROOT/name).read_bytes()
    assert (len(data),*jpeg_size(data),sha256(data).hexdigest())==(size,w,h,digest)
    assert digest not in digests; digests.add(digest); counts[kind]+=1
assert counts=={'I':35,'X':34,'R':6}
print('T04 metadata oracle: PASS 35 included; 34 excluded; 6 relation-only')
PY
```

Recorded output:

```text
T04 metadata oracle: PASS 35 included; 34 excluded; 6 relation-only
```

### Exact T04 asset semantic oracle

This dependency-free oracle re-establishes the T04 subset rather than importing T03's result. It checks the seven-row base-3 codec, code `777`, the exact code-`867` Notes invocation, every strict labelled code, the 50-picture scan, the distinction between that scan and all 729 stable-zero-background T04 rules, code-`420` additivity, the later code-`357`/`1329` structure labels, and all 27 audited repair links. Initial-condition/period labels are pinned as property evidence; they are not trajectory goldens.

```bash
python3 - <<'PY'
from hashlib import sha256
from itertools import product
from pathlib import Path

book=Path('ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md').read_text().splitlines()
links={
3314:'![](_page_297_Picture_2.jpeg)',
3318:'![](_page_297_Picture_4.jpeg)',
3322:'![](_page_297_Picture_6.jpeg)',
3328:'![](_page_298_Figure_2.jpeg)',
3334:'![](_page_299_Picture_3.jpeg)',
3342:'![](_page_300_Figure_1.jpeg)',
3350:'![](_page_301_Picture_2.jpeg)',
3362:'![](_page_302_Picture_3.jpeg)',
3368:'![](_page_303_Picture_2.jpeg)',
3376:'![](_page_304_Picture_2.jpeg)',
3380:'![](_page_305_Picture_2.jpeg)',
2924:'![](_page_262_Figure_2.jpeg)',
2928:'![](_page_263_Figure_2.jpeg)',
5220:'![](_page_451_Picture_6.jpeg)',
5484:'![](_page_476_Figure_3.jpeg)',
10393:'![](_page_847_Figure_1.jpeg)',
10409:'![](_page_848_Figure_2.jpeg)',
11297:'![](_page_885_Picture_21.jpeg)',
11301:'![](_page_885_Picture_23.jpeg)',
11303:'![](_page_885_Picture_24.jpeg)',
11305:'![](_page_885_Picture_25.jpeg)',
11307:'![](_page_885_Picture_26.jpeg)',
14829:'![](_page_980_Picture_15.jpeg)',
14831:'![](_page_980_Picture_16.jpeg)',
14833:'![](_page_980_Picture_17.jpeg)',
17433:'![](_page_1092_Picture_6.jpeg)',
18746:'![](_page_1132_Picture_2.jpeg)',
}
assert all(book[n-1]==want for n,want in links.items())

def table(code):
    assert 0<=code<3**7; out=[]
    for _ in range(7): out.append(code%3); code//=3
    assert code==0
    return tuple(out)

def advance(rule,state):
    n=len(state)
    return [rule[(state[i-1] if i else 0)+state[i]
                 +(state[i+1] if i+1<n else 0)] for i in range(n)]

r777=table(777)
assert r777==(0,1,2,1,0,0,1)
assert ''.join(map(str,reversed(r777)))=='1001210'
state=[0]*17; state[8]=1; words=[]
for _ in range(9):
    used=[i for i,value in enumerate(state) if value]
    words.append(''.join(map(str,state[min(used):max(used)+1])))
    state=advance(r777,state)
assert words==['1','111','12121','1100011','122101221',
 '11001210011','1221110111221','110001222100011',
 '12210110101101221']

r867=table(867)
assert r867==(0,1,0,2,1,0,1)
state=[0]*101; state[50]=1; blob=bytearray()
for _ in range(51):
    blob.extend(state); state=advance(r867,state)
assert tuple(blob.count(v) for v in range(3))==(3692,958,501)
assert sha256(blob).hexdigest()=='185170c0866f76d129fbf3a8843cc731f98b9f012cb98286f01e420532fb53d9'

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
assert all(table(code)[0]==0 for codes in strict.values() for code in codes)
all_quiescent=[code for code in range(3**7) if table(code)[0]==0]
assert len(all_quiescent)==3**6==729
assert len(strict['p76'])==50 and set(strict['p76'])<set(all_quiescent)
assert tuple(range(1002,1096,3))==tuple(1002+3*i for i in range(32))
for code in (1815,2007,1659,2043,219,438,1380,1632,294,1893): table(code)
class4=(357,438,600,792,924,1038,1041,1086,1329,1572,1599,
        1635,1659,1662,1815,2007,2049)
assert all(0<=code<2187 for code in class4)

# BOOK:11918 calls code 420 additive.  Its aggregate table is linear over Z/3.
r420=table(420)
assert r420==(0,2,1,0,2,1,0)
for a in product(range(3),repeat=3):
    for b in product(range(3),repeat=3):
        ab=tuple((x+y)%3 for x,y in zip(a,b))
        assert r420[sum(ab)]==(r420[sum(a)]+r420[sum(b)])%3

# Visible base-3 initial-condition labels and their period/direction suffixes.
structures357=((28,'48'),(7795,'19'),(1706588,'26'),
               (4803890,'41R'),(154596664,'12'),(514454827,'48L'))
structures1329=((1,'78'),(52,'7'),(400,'2'),(800,'12'),(916,'31R'),
                (2617,'9'),(2669,'48R'),(97357,'2'),(659197,'9'))
growth1329=(54889,97439,166426,115396,2069116)
assert structures357[0]==(28,'48') and structures357[3]==(4803890,'41R')
assert structures1329[4]==(916,'31R') and structures1329[6]==(2669,'48R')
assert len(set(growth1329))==5 and growth1329[:2]==(54889,97439)
assert all(table(code)[0]==0 for code in (357,1329))

print('code777_table=',r777,'display=1001210')
print('code777_t0_t8=',','.join(words))
print('code867_51x101_sha256=',sha256(blob).hexdigest())
print('page76_selection=',len(strict['p76']),'all_quiescent=',len(all_quiescent))
print('chapter6_structure_labels=',len(structures357)+len(structures1329),
      'growth_labels=',len(growth1329),'audited_links=',len(links))
print('code420_additive_mod3= PASS; pictured_class4_code=1659; notes_only_code=1662')
print('T04 asset semantic oracle: PASS')
PY
```

Recorded output:

```text
code777_table= (0, 1, 2, 1, 0, 0, 1) display=1001210
code777_t0_t8= 1,111,12121,1100011,122101221,11001210011,1221110111221,110001222100011,12210110101101221
code867_51x101_sha256= 185170c0866f76d129fbf3a8843cc731f98b9f012cb98286f01e420532fb53d9
page76_selection= 50 all_quiescent= 729
chapter6_structure_labels= 15 growth_labels= 5 audited_links= 27
code420_additive_mod3= PASS; pictured_class4_code=1659; notes_only_code=1662
T04 asset semantic oracle: PASS
```

### Strict code-777 raster oracle

The code-`777` grid admits a cell-exact check without inventing resampling: 44 printed vertical boundaries and 23 horizontal boundaries define 43 columns and 22 initial-inclusive rows. The caption itself maps digits to white/gray/black. Cell-center samples have disjoint JPEG luminance intervals, so thresholds lie only in empty robustness gaps. Its standard-library core pins both the audited JPEG and independently generated 946-state grid by SHA-256; when Pillow is available, the same block additionally decodes and checks every cell center. Thus it remains runnable dependency-free without weakening the cryptographic raster identity.

```bash
python3 - <<'PY'
from collections import defaultdict
from hashlib import sha256
from pathlib import Path

path=Path('ref/A-New-Kind-of-Science/CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_75_Figure_6.jpeg')
data=path.read_bytes()
assert sha256(data).hexdigest()=='acb13963632286960ca61b616ff2f45a940750f3ab7deb5e6fbf696543015c15'
xs=(37,50,63,76,88,101,114,127,139,152,165,178,190,203,216,
    229,241,254,267,280,292,305,318,331,344,356,369,382,395,
    407,420,433,446,458,471,484,497,509,522,535,548,560,573,586)
ys=(43,56,69,82,95,108,120,133,146,159,171,184,197,210,222,
    235,248,261,273,286,299,312,324)
assert (len(xs)-1,len(ys)-1)==(43,22)

rule=(0,1,2,1,0,0,1)
state=[0]*43; state[21]=1; history=[]
for _ in range(22):
    history.append(state)
    state=[rule[(state[i-1] if i else 0)+state[i]
                +(state[i+1] if i+1<len(state) else 0)]
           for i in range(len(state))]
grid=bytes(value for state in history for value in state)
assert sha256(grid).hexdigest()=='52ecf352ade2cf0b412493b9391825f6443987ef0350e25ff714f83a913f8d44'

try:
    from PIL import Image
except ModuleNotFoundError:
    print('T04 code-777 raster oracle: PASS byte/grid hashes (Pillow decode unavailable)')
else:
    image=Image.open(path).convert('L')
    assert all(sum(image.getpixel((x,y))<180 for y in range(43,325))>=275 for x in xs)
    assert all(sum(image.getpixel((x,y))<180 for x in range(37,587))>=525 for y in ys)
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
    print('T04 code-777 raster oracle: PASS 0 mismatches')
PY
```

Recorded output:

```text
code777_grid=43x22; sampled_cells=946; luminance_ranges= ((247, 255), (118, 138), (0, 10))
T04 code-777 raster oracle: PASS 0 mismatches
```

The official primary [Chapter 3 PDF](https://files.wolframcdn.com/pub/www.wolframscience.com/nks/nks-ch3.pdf) confirms the strict T04 sequence on PDF pages 11–21 / printed pages 60–70 and the page-71 mobile boundary on PDF page 22. The official [all-notes PDF](https://files.wolframcdn.com/pub/www.wolframscience.com/nks/nks-notes.pdf) confirms the exact code-`867` invocation on PDF page 20 / printed page 868 and, on PDF page 97 / printed page 948, repairs the cropped chart labels to `k=2,r=1`, `k=2,r=2`, `k=2,r=3`, and `k=3,r=1`. Filename page numbers are extraction routing identifiers, not printed-page assertions.

Picture 883/25 has exact executable settings and therefore receives a semantic trajectory digest. Its tiny ungridded JPEG does not state crop/resampling, so it is not forced into a pixel fit. Picture 253/1 is repaired to visible code `1659`: the Actual Index routes code 1659 to printed page 238, while monolith `BOOK:2834` contains only the contaminated page number `238`; Notes code `1662` remains a distinct unpictured property example. The numbered code-`357`/`1329` panels provide exact base-3 initial-condition and period labels, but omit at least spatial digit orientation/padding or displayed horizon/crop. The remaining galleries likewise omit at least one of serialized seed/random sample, boundary/background, initial-state-versus-update horizon, crop, palette, or resampling, so no additional trajectory or raster golden is fabricated.

## Detailed Implementation Plan

1. Build and execute a complete controlled source manifest, disjoint dispositions, split/Index closure, and quote/source oracle.
2. Audit all strict three-color assets, named codes, continuations, seed/filter statements, and source-permitted semantic/raster fixtures.
3. Prove the exact relationship to T03/T05/T06/T07/T08, with program/run/property/view identities separate.
4. Re-audit current API/runtime/tests and write a concrete Goal 2 preset/migration/conformance handoff.
5. Run independent review, embedded oracles, global ledger integration, repository tests, and coverage/diff gates.

## Goal 2 Implementation Stage

### G2-T04 — Strict three-color radius-one preset over G2-T03

**Objective:** make catalog T04 discoverable through `three_color_totalistic(code_or_table)` while resolving to exactly the same structural program/spec and executor used by `totalistic(k=3,r=1,valuation={0:0,1:1,2:2},...)`. Add no state carrier, aggregate, table, codec, rule result, update law, rollout path, or trace format.

**Dependencies:** completed G2-T01 fixed ordered support, `AllSites`, typed same-site assignment, atomic old-snapshot update, realization, and trace contracts; G2-T02 finite-alphabet/table and stable program-reference work; all G2-T03 files (`NumericColorValuation`, `EqualWeightIntegerSum`, aggregate-case table, Wolfram totalistic codec, generic `AggregateLookupRule`, shared executor/spec serialization, arbitrary-precision tagged code, and validation). D115-D118 are mandatory. G2-T04 is sequenced after G2-T03 and adds no independent migration fallback.

**Concrete files and API:**

1. Extend the G2-T03 file `src/ca/presets/totalistic.py` with `three_color_totalistic(code_or_table)`. Internally create the explicit immutable canonical valuation `(0->0,1->1,2->2)` and delegate once to `totalistic(k=3,r=1,valuation=...,code_or_table=...)`. Do not accept `k`, `r`, valuation, aggregate, alphabet, seed, boundary, filter, class, or palette keyword overrides.
2. Export the resolver from `src/ca/presets/__init__.py` and `src/ca/__init__.py`. Add T04 to the catalog/preset registry as configuration-layer discoverability metadata. Registry resolution must return the generic T03 spec; `Rule.family`, executor dispatch, semantic serialization, and program hash must contain no T04/three-color branch tag.
3. Extend `src/ca/specs.py` only at the preset/configuration boundary so a JSON-safe record such as `{"preset":"three_color_totalistic","code":{"kind":"nonnegative_integer","decimal":"777"}}` resolves before `Dynamics` construction. The resolved record must serialize the explicit valuation, arity-three equal-sum case set, seven structural outputs, and optional tagged code exactly like generic T03. Reject unknown or conflicting fields rather than ignoring them.
4. Make no T04-specific changes in `src/ca/alphabets.py`, `aggregates.py`, `rule_tables.py`, `rules.py`, `rollout.py`, update/effects code, or visualization. Those files change only as required by G2-T03. Static inspection must show that neither `rollout` nor `apply_rule` mentions `T04`, `three_color`, or a preset name.
5. Migrate `simple_programs.md`: document T04 under presets, show its resolved exact-sum/table form, and split the current broad `TOTALISTIC` example so K-color histograms/counts are separately typed aggregates rather than aliases of T03/T04. Keep `SEED`, `BOUNDARY`, and palette/view inputs outside the preset.
6. Do not add a T04 seed or palette factory. The source single-gray profile uses existing/shared run data equivalent to `point(value=1,fill_value=0)`; other explicit/random initial fields remain valid. The page-76 white-background scan is a selection record over T06 results, not a `src/ca/datasets.py` default and not part of the preset.
7. Add `tests/fixtures/t04_three_color_totalistic.json` for transparent source-derived constants and `tests/test_t04_three_color_totalistic.py` for preset/API/conformance behavior. Reuse shared G2-T03 executor/codec fixtures rather than copying their implementation. Keep source asset path/hash/grid data in the fixture or reference-test layer, never runtime preset data.

**Exact fixtures:**

- constants `k=3`, `r=1`, `q=3`, sums `0..6`, `M=7`, `R=2187`, valid code endpoints `0/2186`, and tables `0 -> (0,0,0,0,0,0,0)`, `2186 -> (2,2,2,2,2,2,2)`;
- code `777 -> (0,1,2,1,0,0,1)`, high-to-low display `1001210`, and initial-inclusive single-`1` trace `1,111,12121,1100011,122101221,11001210011,1221110111221,110001222100011,12210110101101221` (`BOOK:776`);
- code `867 -> (0,1,0,2,1,0,1)` and the shared 51-by-101 trajectory hash `185170c0866f76d129fbf3a8843cc731f98b9f012cb98286f01e420532fb53d9` (`BOOK:11168`);
- code `420 -> (0,2,1,0,2,1,0)`, with additivity asserted only by the property/analyzer layer (`BOOK:11918`);
- T06 count `729`, page-76 selection `list(range(993,1141,3))` of length 50, and proof that the latter is a proper subset of the former (`BOOK:784`);
- the strict code-777 diagram reference `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_75_Figure_6.jpeg`, SHA-256 `acb13963632286960ca61b616ff2f45a940750f3ab7deb5e6fbf696543015c15`, with source-derived grid/raster expectations kept in reference tests rather than program identity.

**Required conformance and rejection tests:**

1. Assert preset and generic T03 construction compare structurally equal, share the same semantic program reference/hash and runtime classes, and generate identical single-episode and batch traces for both code and table input. Catalog provenance may differ; semantic identity may not.
2. Assert table/code round trips for `0,1,420,777,867,2186`; sum zero is least significant; leading zero rows survive; and output value `2` is produced. Reject codes `-1` and `2187`, booleans/floats/strings outside the tagged manifest codec, six/eight-row tables, sparse mappings, and outputs outside `0..2`.
3. Assert the preset has no `k`, `r`, valuation, aggregate, alphabet, arity, executor, update, seed, boundary, filter, class, or palette override path. Equivalent generic T03 with a noncanonical symbolic valuation remains valid but is not silently relabeled T04.
4. Execute code 777 from the single-gray run and match the exact early trace; execute code 867 and match the shared hash. Run the same program under point-`2`, explicit, random, all-zero, periodic, and fixed-exterior profiles and prove only run/realization identities change.
5. Execute code `1` from an all-zero field and prove the background changes. This rejects fusion of T06 or the page-76 filter. Independently assert exactly 729 codes satisfy `code mod 3=0`, while the 50 displayed codes equal `range(993,1141,3)` and do not exhaust them.
6. Evaluate `(0,2,0)` and `(1,0,1)` through a table whose row two is distinctive: both address sum row two despite different histograms. Reverse representative triples and prove equal output without a runtime `symmetric` flag; perform additivity checks for code 420 only in the analyzer/property API.
7. Render one unchanged episode with two palettes and prove the program reference and raw states are identical. Changing gallery labels, class records, crop, horizon, or raster metadata must likewise leave the program unchanged.
8. Static-scan resolved objects and runtime sources: no T04/three-color family dispatch, duplicate sum/table/codec, binary shift decoder, hidden `3^3=27` exhaustive table, callback, preset-specific `int64` exception, seed/filter/palette default, or test-only execution path.
9. Preserve all G2-T03 generic/radius/bigint adversaries and the full existing suite. T04's small values cannot weaken generic valuation, arbitrary-precision, old-snapshot, nonbinary, and single-episode/batch requirements.

**Completion evidence:** the preset resolves identically to generic T03; exact code/table/count/trace/selection fixtures pass; invalid codes/tables/overrides are rejected; seed, boundary, T06/T07/T08, property, gallery, palette, and view identities remain separate; static inspection finds no new runtime branch or duplicate semantics; focused and full repository tests pass unchanged.

## No-Cheating Checks

- No T04/three-color rule family, `if k==3` runtime case, duplicate aggregate/table/codec/executor/update, ternary patch beside the shared T03 rule, or preset-specific single-episode/batch path.
- No preset record that survives resolution as alternate semantics. `three_color_totalistic(777)` and generic T03 with `k=3,r=1,nu_3,777` must have the same structural program identity and executor types.
- No hidden ordered 27-context table, aggregate-to-exhaustive expansion as native identity, sparse/wildcard table, partial seven-row table, implicit output, or fallback row. Lowering may exist only as an explicit verified relation.
- No histogram, multiset, active/nonzero count, min/max, gate, callback, ordered tuple rank, or floating/tolerant average substituted for the exact `nu_3(left)+nu_3(self)+nu_3(right)` sum. `(0,2,0)` and `(1,0,1)` must merge.
- No palette/host order used as valuation. The resolved preset explicitly contains `0->0,1->1,2->2`; white/gray/black labels and tones remain view data.
- No reversed code convention, binary shift/`&1` decoder, float/JSON-number identity, fixed-width semantic rule ID, omitted leading zeros, or code outside `0..2186`. Sum zero is the least-significant base-3 digit.
- No fusion of the single-gray seed, zero background, finite crop, boundary, event horizon, page-76 selection, T06 predicate, T07 proof, T08 profile, additivity, class, frequency, gallery order, palette, raster, or emulation into program identity.
- No claim that the 50 page-76 codes are all white-preserving rules: exact tests must distinguish that selection from the 729-code T06 restriction.
- No assumption that zero is quiescent: code 1 from an all-zero field must evolve. No in-place scan: every T04 event reads one old snapshot and commits assignments together.
- No source-omitted boundary, crop, horizon, resampling, or palette invented to manufacture a gallery golden. Only source-complete code-777/code-867 semantic and pinned raster fixtures are canonical.
- No T04-first workaround for missing G2-T03 infrastructure. If the preset cannot resolve through the shared typed aggregate rule and executor, stop and repair G2-T03 rather than weakening the preset or tests.

## Completion Requirements

- [ ] Every strict/Notes/split/actual-Index/alias/code/gallery/property/application/emulation candidate is dispositioned with zero remainder.
- [ ] Every relevant asset and source-permitted oracle is closed with hashes, geometry, repairs, and explicit exclusions.
- [x] The exact preset/program/run/property/view boundary and T03/T05/T06/T07/T08 relationship are proved.
- [x] Current API/runtime fit and a concrete Goal 2 preset/conformance stage are implementation-ready.
- [ ] Global ledgers, independent review, embedded checks, coverage/diff gates, and repository tests pass.

## Stage Results

**REOPENED during T06.** The prior 243-candidate/72-asset closure omitted two rasters explicitly governed by already-retained T04 captions: `BOOK:17431 -> 17433` and `BOOK:2922 -> 2924`. Source/asset counts, metadata, reverse closure, globals, and independent review are being repaired before T04 can be complete again. Both additions are evidence relations/profiles and do not change the strict `k=3,r=1` preset semantics below.

The previous exact 12-query search oracle closed 243 candidates in the partition `34/53/11/20/51/30/27/17`; 15 evidence groups closed 253 cited provenance lines, 92 unique quote fragments, and 90 unique quote lines. Those historical source/asset totals are retained until the bounded repair is independently verified.

The construction is exactly the T03 preset `k=3`, `r=1`, `A=(0,1,2)`, and `nu(i)=i`, with seven sum cases, `3^7=2187` tables, and codes `0..2186`; preset resolution has the same structural program identity, hash, and executor types as the corresponding generic T03 program. It rejects valuation or parameter overrides. The page-76 50-code selection is not the 729-code T06 quiescent restriction, T07 reflection is derived, and T08 seed/run data remains separate. Exact code-777/code-867 trajectories and hashes, code-420 additivity, 15 structure plus five growth labels, and the corrected pictured-code labels 1659 and 1632 pass. Independent review, Markdown fences, `git diff --check`, and all 102 repository tests pass.

## Integration Results

1. T04 does not invalidate an earlier semantic conclusion. The T03 evidence gap discovered during this audit was repaired and independently reclosed before T04 completion.
2. No new state carrier, source selector, read, result, successor, termination, executor, or update law is required.
3. D115-D118 fully describe the construction and ownership boundary; no D119 is warranted.
4. T04 is a strict, zero-residue preset over the ordinary T03 structural identity, not a family or runtime dispatch name.
5. Canonical alphabet order and valuation are fixed to `(0,1,2)` and `nu(i)=i`; noncanonical three-symbol valuations remain generic T03 programs rather than T04 variants.
6. Rule restriction, proof/property, seed/run profile, gallery selection, palette, raster, and emulation records remain separate from program identity.
7. T05 remains the higher-color radius-one preset question; T06, T07, and T08 retain their restriction, derived-property, and seed-class responsibilities.
8. Goal 2 implements T04 only after the shared G2-T03 aggregate-rule construction and executor conformance, by adding a preset constructor plus identity/rejection fixtures rather than another execution path.
9. The widened T03 source/asset closure, exact T04 code and trace fixtures, 72-link asset manifest, independent review, and unchanged repository suite supply the conformance evidence.
10. The global API is simpler after reintegration: one fixed-lattice executor serves T01/T02/T03 and this T04 preset, while type traceability survives in preset and evidence metadata.
