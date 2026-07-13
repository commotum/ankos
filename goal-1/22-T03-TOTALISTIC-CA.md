# 22-T03-TOTALISTIC-CA

Status: **COMPLETE**

## Current Facts

- Exact catalog row: T03, CSV line 4, `Totalistic Cellular Automata`; taxonomy vocabulary is `ref/notes/CA-Types.md:68-99` and remains a search seed rather than book evidence.
- The strict transition at `BOOK:772-776` distinguishes unrestricted three-color tables from totalistic rules. It assigns the colors exact values `0,1,2`, makes the next value depend only on the average of left/self/right, and orders the seven output cases from sum `0` at the least-significant/rightmost base-3 digit through sum `6` at the most-significant/leftmost digit.
- The Notes give the direct generalization. For `k` colors and radius `r`, fixed arity is `q=2r+1`, reachable sums are `0..q(k-1)`, table length is `M=1+q(k-1)`, and the rule count is `R=k^M` (`BOOK:11897,11902-11916`). The structural output for sum `s` is digit `floor(n/k^s) mod k`; average `s/q` is an exact alternate label for the same case, not a floating computation.
- The binary radius-two fixtures exercise that same generic six-row codec rather than a special profile: code `10 -> (0,1,0,1,0,0)` is stated directly as black on sums `1` and `3` (`BOOK:11625`); the labelled codes `20 -> (0,0,1,0,1,0)` and `52 -> (0,0,1,0,1,1)` follow exactly from the general codec plus their `k=2,r=2` source identities. Code 20 is textual at `BOOK:3316`; code 52 is visible in the hashed page-707 asset linked at `BOOK:8306`, with class-4 context at `BOOK:8308`; `BOOK:18748` names both as universality candidates. Their class, search, survival, and universality annotations are property/provenance fixtures, not trajectory goldens or run defaults.
- T01/T02 and D111-D114 already supply fixed ordered one-dimensional support, `AllSites`, old-snapshot reads, typed same-site assignment, atomic parallel commit, successor, seed, realization, trace/view separation, ordered alphabets, and arbitrary-precision integer serialization. T03 changes the rule's input quotient and program identity, not the executor or update law.
- `simple_programs.md:1964-2027` groups numeric sums, active counts, and color histograms under one broad `TOTALISTIC` label. That API responsibility is wider than source T03: equal-sum contexts such as `(0,2,0)` and `(1,0,1)` must merge even though their color histograms differ.
- The current runtime can sum an `int64` read vector, but `rules.totalistic` does not derive its case count, `_channel_state` ignores the declared `sum` versus `count` mode, generic `lookup` is not executable, spatial output remains binary right-shift/`&1`, and batch rule IDs are forced through `numpy.int64`. No current test executes a standalone three-color totalistic table or validates its codec.
- The former 16-query/118-candidate and 17-query/309-candidate closures are historical and superseded. The completed bounded repair closes 18 queries, 312 disjoint candidates, 22 evidence groups, 89 verbatim fragments on 86 source lines, five official PDFs, and 118 source-linked rasters partitioned as 50 included, 60 excluded, and 8 relation-only. The two new included rasters are the explicit Notes continuation for four-color totalistic code `1004600`; aggregate and execution semantics are unchanged. Fresh independent review, global reintegration, and every gate pass.

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
- Entry kind: exact finite-sum local-rule description over the T01/T02 fixed-lattice synchronous construction; it introduces a rule-input quotient/table identity but no executor or update law.
- Initial vocabulary: totalistic/totalistic rule, sum, average, total/aggregate of neighboring colors, code, base-`k`, `3k-2`, `k^(1+(k-1)(2r+1))`, `2187`, `16`, `64`, `5^13`, three/five colors, range `r`, outer totalistic, weighted totalistic, symmetric, additive, quiescent, and named example codes `777`, `867`, `420`, `1599`, `1815`.

## Search Log

Closed for the bounded code-`1004600` repair of the reopened canonical source audit. `BOOK` means `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`; its actual Index begins at physical `BOOK:20826`. Counts below are distinct physical lines, not raw matches. Eighteen controlled T03 queries produce 127 lines. An explicit, disjoint 185-line inspected follow-through then reconciles the complete T04 closure, generic binary-radius-two profiles, raster links, captions, Notes, and Index routes into an exact 312-line closure. The oracle separately proves that all 118 historical T03 candidates and all 243 final T04 candidates survive in the new union.

| Q | Search family | Pre-Index | Actual Index |
|---:|---|---:|---:|
| 01 | literal `totalistic` saturation | 74 | 10 |
| 02 | strict `average color` / `average of ... colors` aliases | 6 | 0 |
| 03 | exact counts `2187`, `1,220,703,125`, `3k-2`, `3^7`, `5^13` | 4 | 0 |
| 04 | general totalistic count formula | 1 | 0 |
| 05 | `TotalisticCARule` / `ToTotalisticCARule` implementation tokens | 3 | 0 |
| 06 | named codes `420,777,867,1599,1815` | 8 | 1 |
| 07 | `k=2..5` followed within 80 characters by `r=1..2` | 30 | 0 |
| 08 | `outer totalistic` | 17 | 1 |
| 09 | `growth totalistic` | 2 | 2 |
| 10 | weighted-totalistic / totalistic-weights wording | 1 | 1 |
| 11 | symmetry within 120 characters of totalistic | 4 | 0 |
| 12 | background within 120 characters of totalistic | 3 | 0 |
| 13 | additive within 120 characters, plus the code-420 follow-up | 2 | 0 |
| 14 | literal `quiescen...` control | 1 | 0 |
| 15 | exact sum/total aliases tied to totalistic construction | 3 | 1 |
| 16 | emulation/network/reversibility/application/universality boundary phrases | 6 | 0 |
| 17 | named binary radius-two codes `20` / `52`, including collision controls | 14 | 6 |
| 18 | named four-color totalistic code `1004600` | 2 | 1 |

The zero hits matter: neither `semi-totalistic` nor literal `3k-2` occurs, and code `777` occurs only in the strict figure, not OCR text. “Sum (totalistic) rules” is an actual-Index alias; the main strict text says average, while the implementation sums assigned integer values.

### Exact reproducible manifest

```bash
python3 - <<'PY'
import ast, re
from pathlib import Path

P=Path('ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md')
L=P.read_text().splitlines(); IX=20826
def xs(s): return [] if s=='-' else list(map(int,s.split(',')))
rows=[
(r'(?i)totalistic',
 '772,774,776,784,790,796,800,804,808,824,834,846,1282,1954,2170,2802,2806,2822,2852,2868,2922,3902,3914,5638,6340,6644,7912,8320,8936,9166,10261,11037,11056,11060,11068,11070,11072,11168,11178,11509,11585,11625,11897,11902,11904,11908,11910,11912,11916,13536,13538,13547,13548,13549,13601,13613,13650,13654,13658,14223,14224,14239,14241,14632,15221,15301,15321,15359,15955,15959,16024,17431,18672,18748',
 '20965,20969,20972,20980,21233,21731,22030,22146,22352,22392'),
(r'(?i)average (?:color|of (?:the previous colors|cells in its neighborhood))',
 '774,776,2170,5082,5088,8320','-'),
(r'2187|1,220,703,125|3k-2|3\^7|5\^13','774,1282,1427,11897','-'),
(r'k\^\{1\+\(k-1\)\(2r\+1\)\}','11897','-'),
(r'TotalisticCARule|ToTotalisticCARule','11904,11908,11912','-'),
(r'(?i)code(?: number)? (?:420|777|867|1599|1815)',
 '800,806,838,846,2826,7912,11168,11918','20980'),
(r'(?i)k\s*=\s*[2345].{0,80}?r\s*=\s*(?:1|2)(?![0-9/])',
 '11050,11164,11168,11509,11585,11625,11897,11919,14392,14394,14541,14673,14675,15493,16020,16024,16025,16027,16049,16129,16157,16448,18348,18672,18748,20573,20577,20590,20592,20600','-'),
(r'(?i)outer totalistic',
 '3902,5638,6644,10261,11072,13536,13538,13547,13601,13613,13650,13654,14239,14241,15301,15359,15959','21731'),
(r'(?i)growth totalistic','13536,13549','21233,22030'),
(r'(?i)(?:weights w.{0,180}totalistic|totalistic.{0,180}weights w|weighted totalistic)',
 '11916','20969'),
(r'(?i)(?:symmetr.{0,120}totalistic|totalistic.{0,120}symmetr)',
 '784,11897,13536,15321','-'),
(r'(?i)(?:background.{0,120}totalistic|totalistic.{0,120}background)',
 '784,6340,14241','-'),
(r'(?i)(?:additive.{0,120}totalistic|totalistic.{0,120}additive|Code 420 is an example of an additive rule)',
 '10261,11918','-'),
(r'(?i)quiescen','18770','-'),
(r'(?i)(?:total is exactly 4.{0,100}totalistic|totalistic.{0,100}total is exactly 4|total number of black cells.{0,150}totalistic|totalistic.{0,150}total number of black cells|Sum\[RotateLeft\[a, i\]|Sum \(totalistic\))',
 '3914,11908,13536','22146'),
(r'(?i)three-color rule illustrated here is totalistic|Code 420 is an example of an additive rule|If the connections at each node are not labelled, then only totalistic|no non-trivial totalistic rule|even-numbered totalistic 5-neighbor rules|totalistic cellular automata can be universal',
 '7912,11918,13658,16024,17431,18748','-'),
(r'(?i)code(?: number)?s?\s+(?:20|52)(?![0-9])',
 '3302,3310,3316,3330,3332,3336,3344,11509,14632,14760,15301,15321,18672,18748',
 '20980,21162,21241,21471,21517,22352'),
(r'(?i)1004600','9166,19234','20980'),
]
sets=[]
for q,(pat,pre_s,idx_s) in enumerate(rows,1):
    found=[i for i,s in enumerate(L,1) if re.search(pat,s)]
    pre=[i for i in found if i<IX]; idx=[i for i in found if i>=IX]
    assert pre==xs(pre_s),(q,pre,xs(pre_s))
    assert idx==xs(idx_s),(q,idx,xs(idx_s))
    sets.append(set(found))

# Explicit inspected follow-through: continuations, raster links, named-code
# profiles, captions, controls, and actual-Index routes not hit by the 18
# T03 lexical queries above.
follow={764,778,780,782,788,792,794,798,802,810,818,820,822,826,828,830,832,836,
840,842,844,858,860,1280,1419,1958,2172,2800,2804,2824,2828,2830,2832,2834,2836,2838,
2844,2846,2848,2850,2866,2920,2924,3298,3300,3304,3306,3308,3312,3314,3318,3320,3322,3324,
3326,3328,3334,3338,3340,3342,3348,3350,3352,3356,3360,3362,3364,3368,3370,3372,3374,3376,
3378,3380,3900,3908,3912,5086,5092,5218,5220,5222,5482,5484,5486,5636,6336,6338,6642,7900,7910,8306,
8308,8534,8544,8546,8560,8934,9164,10259,10393,10395,10399,10409,10411,11069,11071,11166,11170,11176,11182,11184,
11186,11188,11190,11297,11301,11303,11305,11307,11375,11627,11629,11914,12055,13540,13599,13603,13605,13607,
13609,13611,13615,13648,13652,13656,14226,14228,14230,14232,14762,14764,14766,14827,14829,14831,14833,15211,
15213,15215,15217,15219,15223,15225,15227,15229,15231,15235,15237,15239,15241,15243,15313,15315,15317,15319,
15661,15972,17139,17433,17874,18339,18476,18744,18746,18850,18877,19236,19238,20846,20967,21134,21223,21683,21933}
assert len(follow)==185

assets={
764:'![](_page_74_Picture_5.jpeg)',778:'![](_page_75_Figure_6.jpeg)',
782:'![](_page_76_Figure_2.jpeg)',792:'![](_page_77_Figure_6.jpeg)',
794:'![](_page_78_Figure_2.jpeg)',798:'![](_page_78_Figure_4.jpeg)',
802:'![](_page_79_Picture_2.jpeg)',818:'![](_page_81_Picture_1.jpeg)',
820:'![](_page_81_Picture_2.jpeg)',822:'![](_page_81_Picture_3.jpeg)',
826:'![](_page_82_Picture_1.jpeg)',830:'![](_page_83_Picture_1.jpeg)',
836:'![](_page_84_Picture_2.jpeg)',844:'![](_page_85_Picture_2.jpeg)',
858:'![](_page_86_Picture_7.jpeg)',860:'![](_page_86_Picture_8.jpeg)',
1280:'![](_page_122_Figure_2.jpeg)',1958:'![](_page_171_Picture_5.jpeg)',
2172:'![](_page_185_Picture_9.jpeg)',2800:'![](_page_248_Figure_2.jpeg)',
2804:'![](_page_249_Picture_1.jpeg)',2824:'![](_page_251_Picture_1.jpeg)',
2828:'![](_page_252_Picture_2.jpeg)',2832:'![](_page_253_Picture_1.jpeg)',
2836:'![](_page_254_Picture_1.jpeg)',2844:'![](_page_255_Picture_2.jpeg)',
2846:'![](_page_255_Picture_3.jpeg)',2848:'![](_page_255_Picture_4.jpeg)',
2850:'![](_page_255_Picture_5.jpeg)',2866:'![](_page_256_Figure_2.jpeg)',
2920:'![](_page_261_Figure_2.jpeg)',3314:'![](_page_297_Picture_2.jpeg)',
3318:'![](_page_297_Picture_4.jpeg)',3322:'![](_page_297_Picture_6.jpeg)',
3328:'![](_page_298_Figure_2.jpeg)',3334:'![](_page_299_Picture_3.jpeg)',
3342:'![](_page_300_Figure_1.jpeg)',3350:'![](_page_301_Picture_2.jpeg)',
3362:'![](_page_302_Picture_3.jpeg)',3368:'![](_page_303_Picture_2.jpeg)',
3376:'![](_page_304_Picture_2.jpeg)',3380:'![](_page_305_Picture_2.jpeg)',
6336:'![](_page_541_Picture_3.jpeg)',6338:'![](_page_541_Picture_4.jpeg)',
6642:'![](_page_566_Figure_2.jpeg)',7910:'![](_page_670_Figure_1.jpeg)',
8306:'![](_page_707_Figure_1.jpeg)',8934:'![](_page_753_Picture_3.jpeg)',
9164:'![](_page_769_Figure_1.jpeg)',11166:'![](_page_883_Picture_23.jpeg)',
11170:'![](_page_883_Picture_25.jpeg)',11176:'![](_page_883_Picture_28.jpeg)',
11182:'![](_page_883_Picture_31.jpeg)',11297:'![](_page_885_Picture_21.jpeg)',
11301:'![](_page_885_Picture_23.jpeg)',11303:'![](_page_885_Picture_24.jpeg)',
11305:'![](_page_885_Picture_25.jpeg)',11307:'![](_page_885_Picture_26.jpeg)',
11627:'![](_page_897_Picture_19.jpeg)',11629:'![](_page_897_Picture_20.jpeg)',
14226:'![](_page_963_Picture_8.jpeg)',14228:'![](_page_963_Picture_9.jpeg)',
14230:'![](_page_963_Picture_10.jpeg)',14232:'![](_page_963_Picture_11.jpeg)',
14762:'![](_page_979_Figure_4.jpeg)',14766:'![](_page_979_Picture_6.jpeg)',
14829:'![](_page_980_Picture_15.jpeg)',14831:'![](_page_980_Picture_16.jpeg)',
14833:'![](_page_980_Picture_17.jpeg)',18746:'![](_page_1132_Picture_2.jpeg)',
19236:'![](_page_1152_Figure_5.jpeg)',19238:'![](_page_1152_Figure_6.jpeg)',
}
assets.update({
2924:'![](_page_262_Figure_2.jpeg)',3900:'![](_page_349_Figure_1.jpeg)',
3908:'![](_page_350_Picture_4.jpeg)',3912:'![](_page_351_Figure_2.jpeg)',
5086:'![](_page_442_Figure_5.jpeg)',5092:'![](_page_443_Picture_1.jpeg)',
5220:'![](_page_451_Picture_6.jpeg)',5484:'![](_page_476_Figure_3.jpeg)',
5636:'![](_page_488_Figure_2.jpeg)',10259:'![](_page_839_Figure_4.jpeg)',
10393:'![](_page_847_Figure_1.jpeg)',10409:'![](_page_848_Figure_2.jpeg)',
11184:'![](_page_883_Picture_32.jpeg)',11186:'![](_page_883_Picture_33.jpeg)',
11188:'![](_page_883_Picture_34.jpeg)',11190:'![](_page_883_Picture_35.jpeg)',
13599:'![](_page_943_Picture_21.jpeg)',13603:'![](_page_944_Picture_3.jpeg)',
13605:'![](_page_944_Picture_4.jpeg)',13607:'![](_page_944_Picture_5.jpeg)',
13609:'![](_page_944_Picture_6.jpeg)',13611:'![](_page_944_Picture_7.jpeg)',
13615:'![](_page_944_Picture_9.jpeg)',13648:'![](_page_945_Picture_2.jpeg)',
13652:'![](_page_945_Picture_4.jpeg)',13656:'![](_page_945_Picture_6.jpeg)',
15211:'![](_page_994_Picture_3.jpeg)',15213:'![](_page_994_Picture_4.jpeg)',
15215:'![](_page_994_Picture_5.jpeg)',15217:'![](_page_994_Picture_6.jpeg)',
15219:'![](_page_994_Picture_7.jpeg)',15223:'![](_page_994_Picture_9.jpeg)',
15225:'![](_page_994_Picture_10.jpeg)',15227:'![](_page_994_Picture_11.jpeg)',
15229:'![](_page_994_Picture_12.jpeg)',15231:'![](_page_994_Picture_13.jpeg)',
15235:'![](_page_994_Picture_15.jpeg)',15237:'![](_page_994_Picture_16.jpeg)',
15239:'![](_page_994_Picture_17.jpeg)',15241:'![](_page_994_Picture_18.jpeg)',
15243:'![](_page_994_Picture_19.jpeg)',15313:'![](_page_996_Picture_6.jpeg)',
15315:'![](_page_996_Picture_7.jpeg)',15317:'![](_page_996_Picture_8.jpeg)',
15319:'![](_page_996_Picture_9.jpeg)',17433:'![](_page_1092_Picture_6.jpeg)',
})
for n,want in assets.items(): assert L[n-1]==want,(n,L[n-1])
assert len(assets)==118 and set(assets)<=follow

assert r'\{0, 1, 0\}, \{1, 1, 1\}, \{0, 1, 0\}' in L[11068]
assert r'\{0, k, 0\}, \{k, 1, k\}, \{0, k, 0\}' in L[11070]
assert L[11913].startswith('■ Common framework.')
assert L[13539].startswith('Apply[Plus, 2 ^ Join')
assert L[3315]=='2 colors, next-nearest neighbors, code 20'
assert L[14759].startswith('■ Page 283 · Survival data.')

parts={
'three_color':'772,774,776,778,780,782,784,788,790,792,794,796,798,800,802,804,806,808,810,818,820,822,824,826,828,830,832,834,836,838,840,842,844,846,1280,1282,2804,2806,2822,2824,2826,2828,2830,2832,2836,2838,2844,2846,2848,2850,2852,3318,3320,3322,3324,3348,3350,3352,3356,3360,3362,3364,3368,3370,3372,3374,3376,3378,6336,6338,6340,7900,7912,8306,8934,8936,11168,11170,11897,11918,14223,14224,14232,14827,16024,18348,18748',
'generic_parent':'8320,11037,11056,11060,11902,11904,11908,11910,11912,11914,11916',
'other_totalistic':'2800,2802,2866,2868,3298,3300,3302,3304,3306,3308,3310,3312,3314,3316,3326,3328,3330,3332,3334,3336,3338,3340,3342,3344,8308,9164,9166,11509,11585,11625,11627,11629,14226,14228,14230,14760,14762,18672,19234,19236,19238',
'sibling_application':'1954,1958,2170,2172,2920,2922,3902,3914,5082,5088,5638,6642,6644,7910,10259,10261,11068,11069,11070,11071,11072,11178,11182,11297,11301,11303,11305,11307,13536,13538,13540,13547,13548,13549,13601,13613,13650,13654,13658,14239,14241,14632,14829,14831,14833,15221,15301,15321,15359,15955,15959,17431,17433',
'controls':'764,858,860,1419,1427,2834,2924,3380,3900,3908,3912,5086,5092,5218,5220,5222,5482,5484,5486,5636,8534,8544,8546,8560,10393,10395,10399,10409,10411,11050,11164,11166,11176,11184,11186,11188,11190,11375,11919,12055,13599,13603,13605,13607,13609,13611,13615,13648,13652,13656,14392,14394,14541,14673,14675,14764,14766,15211,15213,15215,15217,15219,15223,15225,15227,15229,15231,15235,15237,15239,15241,15243,15313,15315,15317,15319,15493,15661,15972,16020,16025,16027,16049,16129,16157,16448,17139,17874,18339,18476,18744,18746,18770,18850,18877,20573,20577,20590,20592,20600',
'index':'20846,20965,20967,20969,20972,20980,21134,21162,21223,21233,21241,21471,21517,21683,21731,21933,22030,22146,22352,22392',
}
partition={k:xs(v) for k,v in parts.items()}
queried=set().union(*sets)
flat=[i for v in partition.values() for i in v]
union=queried|follow
assert not (queried&follow)
assert len(rows)==18 and len(queried)==127 and len(union)==312
assert len(flat)==len(set(flat))==312 and set(flat)==union
assert [len(partition[k]) for k in partition]==[87,11,41,53,100,20]

# Standalone set derivation plus a cross-stage drift guard. T03 defines its
# own explicit follow and partition data above; this reconciliation proves
# why the reopened union is 312 without importing T04's executable state.
t04_parts={
'strict':'772,774,776,778,780,782,784,788,790,792,794,796,798,800,802,804,806,808,810,818,820,822,824,826,828,830,832,834,836,838,840,842,844,846',
'preset_relation':'1280,1282,2804,2806,2822,2824,2826,2828,2830,2832,2836,2838,2844,2846,2848,2850,2852,3318,3320,3322,3324,3348,3350,3352,3356,3360,3362,3364,3368,3370,3372,3374,3376,3378,6336,6338,6340,7900,7912,8306,8934,8936,11168,11170,11897,11918,14223,14224,14232,14827,16024,18348,18748',
'parent':'8320,11037,11056,11060,11902,11904,11908,11910,11912,11914,11916',
'adjacent_totalistic':'2800,2802,2866,2868,3314,3316,3328,3334,3342,9164,9166,11509,11585,11625,11627,11629,14226,14228,14230,18672',
'sibling_application':'1954,1958,2170,2172,2920,2922,3902,3914,5082,5088,5638,6642,6644,7910,10261,11068,11069,11070,11071,11072,11178,11182,11297,11301,11303,11305,11307,13536,13538,13540,13547,13548,13549,13601,13613,13650,13654,13658,14239,14241,14632,14829,14831,14833,15221,15301,15321,15359,15955,15959,17431',
'non_totalistic':'764,858,860,3380,5218,5220,5222,5482,5484,5486,8534,8544,8546,8560,10393,10395,10399,10409,10411,11164,11166,11176,12055,15661,15972,18339,18476,18744,18746,18877',
'false_control':'1419,1427,2834,11050,11375,11919,14392,14394,14541,14673,14675,15493,16020,16025,16027,16049,16129,16157,16448,17139,17874,18850,20573,20577,20590,20592,20600',
'index':'20846,20965,20967,20969,20972,20980,21134,21223,21233,21471,21683,21731,21933,22030,22146,22352,22392',
}
t04_union=set().union(*(set(xs(v)) for v in t04_parts.values()))
new23={3298,3300,3302,3304,3306,3308,3310,3312,3326,3330,3332,3336,
       3338,3340,3344,8308,14760,14762,14764,14766,21162,21241,21517}
asset_delta={2924,3900,3908,3912,5086,5092,5636,10259,11184,11186,11188,
11190,13599,13603,13605,13607,13609,13611,13615,13648,13652,13656,15211,
15213,15215,15217,15219,15223,15225,15227,15229,15231,15235,15237,15239,
15241,15243,15313,15315,15317,15319,17433}
historical=(set().union(*sets[:-2]))|{11069,11071,11914,13540}
assert len(t04_union)==243 and len(new23)==23 and len(asset_delta)==42 and len(historical)==118
assert union==t04_union|new23|asset_delta|{18770,19234,19236,19238} and historical<=union
t04_text=Path('goal-1/23-T04-THREECOLOR-TOTALISTIC.md').read_text()
t04_search=t04_text.split('## Search Log',1)[1].split('## Book Excerpts',1)[0]
m=re.search(r'\nparts=\{\n(.*?)\n\}\npartition=',t04_search,re.S); assert m
live_t04=ast.literal_eval('{'+m.group(1)+'}')
assert {k:set(xs(v)) for k,v in live_t04.items()}=={k:set(xs(v)) for k,v in t04_parts.items()}

# Exact 118-link join to the independent T03 metadata oracle.
stage=Path('goal-1/22-T03-TOTALISTIC-CA.md').read_text()
asset_audit=re.split(r'^## Asset and Raster Audit\s*$',stage,flags=re.M)[1]
items_src=asset_audit.split('\nitems={',1)[1].split('\n}\n\ndef jpeg_size',1)[0]
ledger_paths=set(re.findall(r"'([^']+\.jpeg)':\(",items_src))
manifest_names={re.fullmatch(r'!\[\]\(([^)]+)\)',v).group(1) for v in assets.values()}
assert len(ledger_paths)==len(manifest_names)==118
assert len({Path(p).name for p in ledger_paths})==118
assert {Path(p).name for p in ledger_paths}==manifest_names

root=Path('ref/A-New-Kind-of-Science')
split={
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
for rel,want in split.items():
    lines=(root/rel).read_text().splitlines()
    got=[i for i,s in enumerate(lines,1) if re.search(r'(?i)totalistic',s)]
    assert got==xs(want),(rel,got,xs(want))
assert sum(len(xs(v)) for v in split.values())==84
code1004600_split={
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md':'549',
'BACK-MATTER/Colophon/Colophon.md':'1791,3537',
}
for rel,want in code1004600_split.items():
    lines=(root/rel).read_text().splitlines()
    got=[i for i,s in enumerate(lines,1) if re.search(r'(?i)1004600',s)]
    assert got==xs(want),(rel,got,xs(want))
print('T03 source manifest: PASS 18 queries; 312 candidates; partition=87,11,41,53,100,20; assets=118; split=84; inherited=243/historical=118')
PY
```

Expected terminal line:

```text
T03 source manifest: PASS 18 queries; 312 candidates; partition=87,11,41,53,100,20; assets=118; split=84; inherited=243/historical=118
```

### Complete disjoint disposition

- **Three-color strict, profile, and relation closure (87):** `772,774,776,778,780,782,784,788,790,792,794,796,798,800,802,804,806,808,810,818,820,822,824,826,828,830,832,834,836,838,840,842,844,846,1280,1282,2804,2806,2822,2824,2826,2828,2830,2832,2836,2838,2844,2846,2848,2850,2852,3318,3320,3322,3324,3348,3350,3352,3356,3360,3362,3364,3368,3370,3372,3374,3376,3378,6336,6338,6340,7900,7912,8306,8934,8936,11168,11170,11897,11918,14223,14224,14232,14827,16024,18348,18748`. This is the complete inherited T04 definition/gallery/class/property route, now direct evidence for the general T03 construction.
- **Generic construction and implementation (11):** `8320,11037,11056,11060,11902,11904,11908,11910,11912,11914,11916`. These establish the average alias, signatures, exact aggregate lookup, padded codec, and common-framework weight vector.
- **Other one-dimensional totalistic profiles (41):** `2800,2802,2866,2868,3298,3300,3302,3304,3306,3308,3310,3312,3314,3316,3326,3328,3330,3332,3334,3336,3338,3340,3342,3344,8308,9164,9166,11509,11585,11625,11627,11629,14226,14228,14230,14760,14762,18672,19234,19236,19238`. These close binary radius-two code `10`/`20` and higher/lower-color profiles, including persistent-structure searches, survival data, universality context, frequency controls, and the explicit code-`1004600` long-run Notes continuation.
- **Sibling geometry, aggregate, or application relations (53):** `1954,1958,2170,2172,2920,2922,3902,3914,5082,5088,5638,6642,6644,7910,10259,10261,11068,11069,11070,11071,11072,11178,11182,11297,11301,11303,11305,11307,13536,13538,13540,13547,13548,13549,13601,13613,13650,13654,13658,14239,14241,14632,14829,14831,14833,15221,15301,15321,15359,15955,15959,17431,17433`. These are continuous, two-dimensional, outer/growth/weighted, network, tiling, additive, block-emulation, Life-analogy, and feature-extraction relations. The two directly joined relation rasters are `10259` and `17433`.
- **Excluded/query and linked-raster controls (100):** `764,858,860,1419,1427,2834,2924,3380,3900,3908,3912,5086,5092,5218,5220,5222,5482,5484,5486,5636,8534,8544,8546,8560,10393,10395,10399,10409,10411,11050,11164,11166,11176,11184,11186,11188,11190,11375,11919,12055,13599,13603,13605,13607,13609,13611,13615,13648,13652,13656,14392,14394,14541,14673,14675,14764,14766,15211,15213,15215,15217,15219,15223,15225,15227,15229,15231,15235,15237,15239,15241,15243,15313,15315,15317,15319,15493,15661,15972,16020,16025,16027,16049,16129,16157,16448,17139,17874,18339,18476,18744,18746,18770,18850,18877,20573,20577,20590,20592,20600`. These are non-totalistic constructions, false lexical hits, geometry/application raster chains, and negative comparators. `18770` is retained explicitly as the quiescent symmetric elementary-rule emulation-network boundary.
- **Actual-Index routes (20):** `20846,20965,20967,20969,20972,20980,21134,21162,21223,21233,21241,21471,21517,21683,21731,21933,22030,22146,22352,22392`. They route to already audited direct, profile, relation, or control material and add no transition mechanics.

There is zero silent remainder: the six sets are pairwise disjoint and their union is the exact 312-candidate manifest.

### Actual-Index route closure

| Actual Index | Exact route | Disposition |
|---:|---|---|
| `20846` | additive cellular automata with three colors, page 886 | code-420 relation Notes |
| `20965` | implementation of totalistic, page 886 | direct Notes at `BOOK:11902-11916` |
| `20967` | cellular automata, three-color, page 60 | strict three-color profile |
| `20969` | totalistic cross-reference; weighted totalistic, page 427 | strict T03; weighted sibling at `BOOK:5082,5088` |
| `20972` | class 4 in 3-color totalistic CAs, page 948 | behavior/property Notes at `BOOK:14223-14224` |
| `20980` | code `1004600`, undecidability pages 754/1137; code 294 for totalistic CAs, page 60 | higher-color Notes route at `BOOK:9166,19234` and named three-color profile at `BOOK:6340`; the OCR line interleaves columns |
| `21134` | encoding of three colors by two, pages 655/1111 | block-emulation relation |
| `21162` | excluded blocks in code 20, page 958 | code-20 network property |
| `21223` | glider gun in code 1329, page 288 | three-color persistent-structure profile |
| `21233` | growth totalistic rules, page 928 | two-dimensional sibling at `BOOK:13536,13549` |
| `21241` | transients for code 20, page 964 | code-20 survival property |
| `21471` | localized structures in codes 357/1329 | three-color profile route |
| `21517` | Jonathan Millen and code 20, page 877 | historical binary-radius-two route |
| `21683` | networks of cellular-automaton emulations | emulation relation |
| `21731` | outer totalistic rules | two-dimensional sibling at `BOOK:13536-13547` |
| `21933` | rules with three colors | three-color profile/control route |
| `22030` | totalistic page 60; growth totalistic page 928 | strict definition and growth sibling |
| `22146` | Sum (totalistic) rules, page 60 | confirms `sum` as the Index alias for strict average cases |
| `22352` | Totalistic cellular automata page 60, 2D page 170, implementation page 886, non-reversibility page 1017 | routes to strict, sibling, implementation, and property passages already closed |
| `22392` | universality in totalistic cellular automata, page 693 | relation at `BOOK:18748` |

### Split, source, and asset routing

- The 84 literal-totalistic monolith lines have exactly 84 split-file counterparts, pinned by the oracle. Strict `BOOK:772,774,776` map to Chapter 3 split `89,91,93`; count/implementation `BOOK:11897,11902-11916` map to Chapter 12 split `3278,3283-3297`.
- The three code-`1004600` query hits map exactly as `BOOK:9166` to Chapter 12 split line `549`, and `BOOK:19234,20980` to Colophon split lines `1791,3537`. The latter actual-Index line retains interleaved-column OCR, while the Notes line is exact.
- `BACK-MATTER/Index/Index.md` is misrouted Notes and has no `#### Index` header. The real split Index begins in `BACK-MATTER/Colophon/Colophon.md:3383`; the ten literal-totalistic routes remain split lines `3522,3526,3529,3537,3790,4288,4587,4703,4909,4949`, while ten additional named-code/property routes are pinned by the 20-line monolith Index partition above.
- The only raster carrying construction data absent from OCR text is the strict figure referenced at `BOOK:778`: `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_75_Figure_6.jpeg`, JPEG `610x446`, SHA-256 `acb13963632286960ca61b616ff2f45a940750f3ab7deb5e6fbf696543015c15`. Direct inspection gives displayed digits `1,0,0,1,2,1,0` from high sum to low sum, hence code `777`; the caption, not pixel colors, remains semantic authority. The full manifest now traverses 118 linked rasters—50 included, 60 explicit controls, and eight relation-only—and asserts exact basename/path-set equality with the independent metadata ledger. The two added page-1152 plots are observer/property evidence for code `1004600`; they contribute no additional native rows, seed, boundary, or stopping rule. The remaining rasters are profile, property, application, or exclusion evidence with the same boundary.

## Book Excerpts

All verbatim monolith material is placed in blockquotes so the oracle below can check every fragment against the cited physical line.

### E1 — Strict restriction, aggregate, valuation, and code order

- Provenance: `BOOK:772,774,776`, strict Chapter 3 text and caption.
- Establishes: totalistic is a restriction of the full three-color table; output depends on average rather than the individual ordered colors; values are exactly `0,1,2`; self and immediate neighbors are included; sum/average zero is the rightmost, least-significant base-3 row.

> The 256 "elementary" rules that we have discussed so far are by most measures the simplest possible—and were the first ones I studied. But one can for example also look at rules that involve three colors, rather than two, so that cells can not only be black and white, but also gray. The total number of possible rules of this kind turns out to be immense—7,625,597,484,987 in all—but by considering only so-called "totalistic" ones, the number becomes much more manageable.

> The idea of a totalistic rule is to take the new color of each cell to depend only on the average color of neighboring cells, and not on their individual colors. The picture below shows one example of how this works. And with three possible colors for each cell, there are 2187 possible totalistic rules, each of which can conveniently be identified by a code number as illustrated in the picture. The facing page shows a representative sequence of such rules.

> Example of a totalistic cellular automaton with three possible colors for each cell. The rule is set up so that the new color of every cell is determined by the average of the previous colors of the cell and its immediate neighbors. With 0 representing white, 1 gray and 2 black, the rightmost element of the rule gives the result for average color 0, while the element immediately to its left gives the result for average color 1/3—and so on. Interpreting the sequence of new colors as a sequence of base 3 digits, one can assign a code number to each totalistic rule.

### E2 — Gallery restrictions are not program identity

- Provenance: `BOOK:784,790`, strict captions.
- Establishes: white-background stability is an explicit gallery filter, reflection symmetry follows from the aggregate rule, and the single-gray cell is a figure convention.

> A sequence of totalistic cellular automata with three possible colors for each cell. Although their basic rules are more complicated, the cellular automata shown here do not seem to have fundamentally more complicated behavior than the two-color cellular automata shown on previous pages. Note that in the sequence of rules shown here, those that change the white background are not included. The symmetry of all the patterns is a consequence of the basic structure of totalistic rules. But in fact the behavior we see on the previous page is not unlike what we already saw in many elementary cellular automata a few pages back. Having more complicated underlying rules has not, it seems, led to much greater complexity in overall behavior.

> Examples of three-color totalistic rules that yield patterns which attain a certain size, then repeat forever. The maximum repetition period is found to be 78 steps, and is achieved by the rule with code number 1329. In the pictures shown here and on the following pages, the initial condition used contains a single gray cell.

### E3 — Exact counts and one-dimensional color/range variants

- Provenance: `BOOK:1282,2802,2806,2868`.
- Establishes: the `k=2,3,5`, radius-one counts and explicit two-color higher-range, three-color, and four-color one-dimensional variants.

> Examples of cellular automata with rules of varying complexity. The rules used are of the so-called totalistic type described on page 60. With two possible colors, just 4 cases need to be specified in such rules, and there are 16 possible rules in all. But as the number of colors increases, the rules rapidly become more complex. With three colors, there are 7 cases to be specified, and 2187 possible rules; with five colors, there are 13 cases to be specified, and 1,220,703,125 possible rules. But even though the underlying rules increase rapidly in complexity, the overall forms of behavior that we see do not change much. With two colors, it turns out that no totalistic rules yield anything other than repetitive or nested behavior. But as soon as three colors are allowed, much more complex behavior is immediately possible. Allowing four or more colors, however, does not further increase the complexity of the behavior, and, as the picture shows, even with five colors, simple repetitive and nested behavior can still occur.

> Totalistic cellular automata whose rules involve nearest and next-nearest neighbors, and where each cell has two possible colors.

> A sequence of totalistic cellular automata with rules that involve only nearest neighbors, but where each cell can have three possible colors.

> A sequence of totalistic rules involving nearest neighbors and four possible colors for each cell chosen to show transitions between rules with different classes of behavior. Note that class 4 seems to occur between class 2 and class 3.

### E4 — Continuous and two-dimensional siblings

- Provenance: `BOOK:1954,2170,2922`.
- Establishes: continuous gray-level systems are a cross-construction; the cited 2D profile has four neighbors plus self; its base-2 code uses totals from five down to zero. These do not silently redefine one-dimensional T03.

> And to address this question, what I will do in this section is to consider a generalization of cellular automata in which each cell is not just black or white, but instead can have any of a continuous range of possible levels of gray. One can update the gray level of each cell by using rules that are in a sense a cross between the totalistic cellular automaton rules that we discussed at the beginning of the last chapter and the iterated maps that we just discussed in the previous section.

> The form of the rule for a typical two-dimensional cellular automaton. In the cases discussed in this section, each cell is either black or white. Usually I consider so-called totalistic rules in which the new color of the center cell depends only on the average of the previous colors of its four neighbors, as well as on its own previous color.

> Examples of the evolution of two-dimensional cellular automata with various totalistic rules starting from random initial conditions. The rules involve a cell and its four immediate neighbors. Each successive base 2 digit in the code number for the rule gives the outcome when the total of the cell and its four neighbors runs from 5 down to 0.

### E5 — Outer and unequal-weight application boundaries

- Provenance: `BOOK:3902,3914,5088`.
- Establishes: outer totalistic can retain the center separately; a 2D totalistic caption is truncated in the monolith; negative unequal weights and thresholds form a separate application construction.

> A two-dimensional cellular automaton first shown on page 178 with the rule that if out of the eight neighbors (including diagonals) around a given cell, there are exactly three black cells, then the cell itself becomes black on the next step. If the cell has 1, 2 or 4 black neighbors, then it stays the same color as before, and if it has 5 or more black neighbors, then it becomes white on the next step. (Outer totalistic code 746.) This simple rule produces randomness through the mechanism of intrinsic randomness generation, and this randomness in turn leads to a pattern of growth that takes on an increasingly smooth more-or-less circular form.

> total is exactly 4, then it becomes black. (The rule has totalistic code 976.) The pictures show that on a large scale, the rule leads to regions of black and white whose boundaries behave in a seemingly smooth and continuous way. Note that each picture is 80 cells across, and is effectively wrapped around so that the left neighbor of the leftmost cell is the rightmost cell, and so on.

> Evolution of simple two-dimensional cellular automata in which the color of each cell at each step is determined by looking at a weighted sum of the average colors of cells up to distance 3 away. In both rules shown the cell itself and its nearest neighbors enter with weight 1. Cells at distances 2 and 3 enter with negative weights -- -0.4 per cell for the first rule, and -0.2 for the second. A cell becomes black if the weighted sum is positive, and white otherwise. Starting from random initial conditions, both rules quickly evolve to stationary states that look very much like pigmentation patterns seen in animals.

### E6 — Named profile, emulation, and definition corroboration

- Provenance: `BOOK:6340,7912,8320`.
- Establishes: codes 294/1893 are one-dimensional profiles; code 1599 can be block-emulated by a binary larger-range CA but remains native three-color T03; the average/not-individual-colors definition is repeated in the universality discussion.

> Examples of one-dimensional cellular automata that support various forms of persistent structures even on largely random backgrounds. These are 3-color totalistic rules with codes 294 and 1893.

> An example of how a cellular automaton with three possible colors and nearest-neighbor rules can be emulated by a cellular automaton with only two possible colors but a larger number of neighbors (in this case five on each side). The basic idea is to represent each cell in the three-color rule by a block of three cells in the two-color rule, according to the correspondence given on the left. The three-color rule illustrated here is totalistic code 1599 from page 70.

> In fact, as illustrated in the pictures on the facing page, it is sufficient in such cases just to use so-called totalistic rules in which the new color of a cell depends only on the average color of cells in its neighborhood, and not on their individual colors.

### E7 — Built-in signatures preserve construction distinctions

- Provenance: `BOOK:11037,11056,11060,11068-11072`.
- Establishes: direct one-dimensional nearest/range signatures are separate from 2D totalistic and outer-totalistic weighted-stencil signatures. The implementation pointer and the two multiline 2D forms require repairs below.

> I discuss the implementation of totalistic cellular automata on page 886, and of higher-dimensional cellular automata on

>             \{n, \{k, 1\}\} k-color nearest-neighbor totalistic rule

> \{n, \{k, 1\}, r\} k-color range r totalistic rule

>   {n, {k, 1}, {1, 1}} 9-neighbor totalistic rule

> \{n, \{k, \{\{0, 1, 0\}, \{1, 1, 1\}, \{0, 1, 0\}\}, \{1, 1\}\}\}\}

>                         5-neighbor totalistic rule

> \{n, \{k, \{\{0, k, 0\}, \{k, 1, k\}, \{0, k, 0\}\}, \{1, 1\}\}\}

>                        5-neighbor outer totalistic rule

### E8 — Runnable named examples

- Provenance: `BOOK:11168,11178`.
- Establishes: code 867 is directly identified as `k=3,r=1`; code 3702 is explicitly a 2D nine-neighbor sibling. The invocations are OCR-damaged and normalized below.

> This runs the totalistic k=3, r=1 rule with code 867.  $ln[11]:=Show[RasterGraphics[CellularAutomaton]{867, {3, 1}, 1}, {{1}, 0}, 50]]]$

> This runs 2D 9-neighbor totalistic code 3702 for 25 steps, giving the results for the last 5 steps.

### E9 — A concrete binary range-two table

- Provenance: `BOOK:11625`.
- Establishes: there are 64 binary range-two totalistic rules and code 10 outputs black exactly for sums 1 and 3 among five cells.

> - **Code 10.** Rule 30 is by many measures the simplest cellular automaton that generates randomness from a single black initial cell. But there are other simple examples—that historically I noticed slightly earlier than rule 30, though did not study—that occur in k = 2, r = 2 totalistic rules. And indeed among the 64 such rules, 13 show randomness. An example shown below is code 10, which specifies that if 1 or 3 cells out of 5 are black then the next cell is black; otherwise it is white.

### E10 — General rule count and value-assignment requirement

- Provenance: `BOOK:11897`, page-60 Notes.
- Establishes: exact general count `k^(1+(k-1)(2r+1))`, the `16/64/2187` checks, and the requirement that `k>2` totalistic identity is relative to a specific value assignment.

> - **Page 60 · Numbers of rules.** Allowing k possible colors for each cell and considering r neighbors on each side, there are  $k^{k^{2r+1}}$  possible cellular automaton rules in all, of which  $k^{1/2}k^{r+1}$  are symmetric, and  $k^{1+(k-1)(2r+1)}$  are totalistic. (For k=2, r=1 there are therefore 256 possible rules altogether, of which 16 are totalistic. For k=2, r=2 there are 4,294,967,296 rules in all, of which 64 are totalistic. And for k=3, r=1 there are 7,625,597,484,987 rules in all, with 2187 totalistic ones.) Note that for k>2, a particular rule will in general be totalistic only for a specific assignment of values to colors. I first introduced totalistic rules in 1983.

### E11 — Direct aggregate lookup and code conversion

- Provenance: `BOOK:11902,11904,11908,11910,11912`.
- Establishes: current-array rotations are summed over `-r..r`, the negative index selects sum rows in reverse list order, and the padded base-`k` digit length is exactly `1+(k-1)(2r+1)`.

> ■ Implementation of totalistic cellular automata. To handle totalistic rules that involve *k* colors and nearest neighbors, one can add the definition

> CAStep[TotalisticCARule[rule\_List, 1], a\_List] := rule[[-1 - (RotateLeft[a] + a + RotateRight[a])]]

> CAStep[TotalisticCARule[rule\_List, r\_Integer], a\_List] := rule[[-1 - Sum[RotateLeft[a, i], {i, -r, r}]]]

> One can generate the representation of totalistic rules used by these functions from code numbers using

>  $ToTotalisticCARule[num\_Integer, k\_Integer, r\_Integer] := TotalisticCARule[IntegerDigits[num, k, 1 + (k - 1)(2r + 1)], r]$

### E12 — One framework, different weights

- Provenance: `BOOK:11914,11916`.
- Establishes: the implementation framework can host both positional general-CA weights and all-one totalistic weights without making the two rule identities interchangeable.

> ■ Common framework. The *Mathematica* built-in function *CellularAutomaton* discussed on page 867 handles general and

> totalistic rules in the same framework by using ListConvolve[w, a, r+1] and taking the weights w to be respectively  $k \wedge Table[i-1, \{i, 2r+1\}]$  and  $Table[1, \{2r+1\}]$ .

### E13 — Additivity is a relation, not base execution

- Provenance: `BOOK:10261,11918`.
- Establishes: outer-totalistic code 204 and one-dimensional code 420 are additionally additive. The extra algebraic property does not define every totalistic rule.

> A two-dimensional cellular automaton that exhibits an almost trivial form of self-reproduction, in which multiple copies of any initial pattern appear every time the number of steps of evolution doubles. The rule used is additive, and takes a cell to be black whenever an odd number of its neighbors were black on the step before (outer totalistic code 204). The same basic self-reproduction phenomenon occurs in elementary rule 90, as well as in essentially any other additive rule, in any number of dimensions.

> - Page 63 · Mod 3 rule. Code 420 is an example of an additive rule, and yields a pattern corresponding to Pascal's triangle modulo 3, as discussed on page 870.

### E14 — Exact 2D outer/growth boundary

- Provenance: `BOOK:13536,13538,13540,13547-13549`.
- Establishes: binary 2D totalistic counts black cells; outer totalistic retains the center; growth totalistic makes black absorbing; their codecs/counts are sibling definitions.

> symmetric in the table below if they preserve any possible rotational symmetry consistent with the underlying arrangement of cells. Totalistic rules depend only on the total number of black cells in a neighborhood; outer totalistic rules (as in the previous note) also depend on the color of the center cell. Growth totalistic rules make any cell that becomes black remain black forever.

> In such a rule, given a list of how many neighbors around a given cell (out of s possible) make the cell turn black the outer totalistic code for the rule can be obtained from

> Apply[Plus, 2 ^ Join[2 list, 2 Range[s + 1] - 1]]

> | outer totalistic       | $2^{10} = 1024$               | $2^{18} \simeq 3 \times 10^5$     | $2^{14} = 16384$                  |

> | totalistic             | $2^6 = 64$                    | $2^{10} = 1024$                   | $2^8 = 256$                       |

> | growth totalistic      | $2^5 = 32$                    | $2^9 = 512$                       | $2^7 = 128$                       |

### E15 — Unlabelled-network applicability

- Provenance: `BOOK:13658`.
- Establishes: unlabelled equal-degree networks admit only aggregate rules, but topology can still affect behavior. This is an application relation, not permission to replace T03's line by an arbitrary graph.

> ■ Networks. Cellular automata can be set up so that each cell corresponds to a node in a network. (See page 936.) The only requirement is that around each node the network must have the same structure (or at least a limited number of possible structures). For nearest-neighbor rules, it suffices that each node has the same number of connections. For longer-range rules, the network must satisfy constraints of the kind discussed on page 483. (Cayley graphs of groups always have the necessary homogeneity.) If the connections at each node are not labelled, then only totalistic cellular automaton rules can be implemented. Many topological and geometrical properties of the underlying network can affect the overall behavior of a cellular automaton on it.

### E16 — Named codes and general `k,r` coverage

- Provenance: `BOOK:14223,14224`.
- Establishes: the complete cited class-4 code list and explicit one-dimensional `k`-color, range-`r` parameterization.

> - Page 235 · Class 4 rules. Other examples of class 4 totalistic rules with *k* = *3* colors include 357 (page 282), 438, 600, 792, 924, 1038, 1041, 1086, 1329 (page 282), 1572, 1599 (see page 70), 1635 (see page 67), 1662, 1815 (page 236), 2007 (page 237) and 2049 (see page 68).

> - **Frequencies of classes.** The pie charts below show results for 1D totalistic cellular automata with *k* colors and range *r*. Class 3 tends to become more common as the number of elements in the rule increases because as soon as any of these elements yield class 3 behavior, that behavior dominates the system.

### E17 — Reversibility, feature extraction, emulation, universality, and quiescence boundaries

- Provenance: `BOOK:16024,17431,18348,18748,18770`.
- Establishes: nontrivial totalistic rules are not reversible; 5-neighbor image rules are an application; binary block encoding is an emulation; universality is a property; the only literal quiescence hit is unrelated elementary-rule emulation.

> - **Numbers of reversible rules.** For k = 2, r = 1, there are 6 reversible rules, as shown on page 436. For k = 2, r = 2 there are 62 reversible rules, in 20 families inequivalent under symmetries, out of a total of  $2^{32}$  or about 4 billion possible rules. For k = 3, r = 1 there are 1800 reversible rules, in 172 families. For k = 4, r = 1, some of the reversible rules can be constructed from the second-order cellular automata below. Note that for any k and r, no non-trivial totalistic rule can ever be reversible.

> - Related models. Rather than requiring particular templates to be matched, one can consider applying arbitrary cellular automaton rules. The pictures below show results from a single step of the 16 even-numbered totalistic 5-neighbor rules. The results are surprisingly easy to interpret in terms of feature extraction.

> The problem of encoding cells with several colors by blocks of black and white cells is related to standard problems in coding theory (see page 560). One approach is to use {1, 1} to indicate the boundary of each block, and then within each block to use all possible digit sequences which do not contain {1, 1}, as in the Fibonacci number system discussed on page 892. Note that the original rule with *k* colors and *r* neighbors involves  $Log[2, k^{k^{2r+1}}]$  bits of information; the two-color rule that emulates it involves  $Log[2, 2^{2^{2s+1}}]$  bits. As a result, the minimum possible s for k = 3, r = 1 is about 2.2; in the specific example shown in the main text it is 5.

> - Totalistic rules. It is straightforward to show that totalistic cellular automata can be universal. Explicit simple candidates include k = 2, r = 2 rules with codes 20 and 52, as well as the various k = 3, r = 1 class 4 rules shown in Chapter 3.

> ■ Page 702 · Rule emulations. The network below shows which quiescent symmetric elementary rules can emulate which with blocks of length 8 or less. (Compare page 269.)

### E18 — Actual-Index routing fragments

- Provenance: `BOOK:20965,20969,20972,20980,21233,21731,22030,22146,22352,22392`.
- Establishes: all ten actual-Index candidates route to already audited strict, Notes, sibling, or relation passages.

> implementation of totalistic, 886

> totalistic see Totalistic cellular automata

> weighted totalistic, 427

> in 3-color totalistic CAs, 948

> Code 294 for totalistic CAs, 60

> Growth totalistic rules, 928

> Outer totalistic rules

> growth totalistic, 928

> totalistic, 60

> Sum (totalistic) rules, 60

> Totalistic cellular automata, 60

> in totalistic cellular automata, 693

### E19 — Complete binary radius-two code-20 profile route

- Provenance: `BOOK:3298,3300,3302,3304,3306,3308,3310,3312,3326,3330,3332,3336,3338,3340,3344`.
- Establishes: the code-20 profile includes its random class-4 overview, exhaustive sub-nine-cell starts, named persistent structures, 25-billion-start search, and systematic period-through-15 search. These are run/property records over the binary `k=2,r=2` table, not extra transition rows.

> The next page shows three typical examples of class 4 cellular automata.

> Most of these structures eventually die out, sometimes in rather complicated ways.

> And taking the code 20 cellular automaton from the top of the next page, the page that follows shows what happens in this system with each of the first couple of hundred possible initial conditions.

> But when we reach initial condition number 151 we finally see a structure that persists.

> And indeed at initial condition 187 we see a considerably more complicated structure, that instead of staying still moves systematically to the right, repeating its basic form only every 9 steps.

> The existence of structures that move is a fundamental feature of class 4 systems.

> It turns out, however, that initial condition 189 suddenly yields a much simpler structure—that just stays unchanged in one position at every step.

> But going on to initial condition 195, we again find a more complicated structure—this time one that repeats only every 22 steps.

> Three typical examples of class 4 cellular automata. In each case various kinds of persistent structures are seen.

> The behavior of the code 20 cellular automaton from the top of the facing page for all initial conditions with black cells in a region of size less than nine.

> So just what set of structures does the code 20 cellular automaton ultimately support?

> Persistent structures found by testing the first twenty-five billion possible initial conditions for the code 20 cellular automaton shown on the previous page.

> The largest structure in the picture above starts from a block that is 30 cells wide.

> The picture on the facing page shows the results of using this procedure for repetition periods up to 15.

> All the persistent structures with repetition periods up to 15 steps in the code 20 cellular automaton.

### E20 — Universality, excluded-block network, and survival properties

- Provenance: `BOOK:8308,14632,14760`.
- Establishes: class-4 universality is a conjectural/property context; the code-20 excluded-block network and survival counts are measured properties. The `t=2` range typo in the second excerpt is repaired against the official Notes below.

> Examples of cellular automata with class 4 overall behavior, as discussed in Chapter 6. I strongly suspect that all class 4 rules, like rule 110, will turn out to be universal.

> The k = 2, t = 2 totalistic rule with code 20 gives a network with 65535 nodes after just 1 step.

> (The shortest excluded block for code 20 is of length 36.)

> ■ Page 283 · Survival data. The number of steps for which the pattern produced by each of the first 1000 initial conditions in code 20 survive are indicated in the picture below. 72 of these initial conditions lead to persistent structures. Among the first million initial conditions, 60,171 lead to persistent structures and among the first billion initial conditions the number is 71,079,205.

### E21 — Post-profile boundary and actual-Index code-20 routes

- Provenance: `BOOK:14764,21162,21241,21517`.
- Establishes: the page-979 rule-110 background begins a distinct non-totalistic boundary; the actual Index routes code 20 to excluded blocks, transients, and Jonathan Millen's historical profile without adding mechanics.

> ■ **Page 290 · Background.** At every step the background pattern in rule 110 consists of repetitions of the block  $b = \{1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0\}$ , as shown in the picture below.

> in code 20, 958

> for code 20, 964

> Millen, Jonathan K. (USA, 1942–) and code 20 CA, 877

### E22 — Code-`1004600` Notes continuation

- Provenance: `BOOK:19234,19236,19238`.
- Establishes: the previously audited four-color totalistic program has an explicit long-run observer continuation. The measured growth rates, non-white fraction, 20-million-step horizon, fluctuation plots, seeds, and views are property/run/view evidence, not rule rows, execution defaults, or a halting decision procedure.

> - Page 755 · Code 1004600. In cases (c) and (d) steady growth at about 0.035 and 0.039 cells per step (of which 28% on average are non-white) is seen up to at least 20 million steps, though there continue to be fluctuations as shown below.

## Source Repairs

1. **Primary files and hashes.** Strict text/captions were checked against the official [`nks-ch3.pdf`](https://files.wolframcdn.com/pub/www.wolframscience.com/nks/nks-ch3.pdf), SHA-256 `d4005b27774084c276e67d46a6c79106b93b785d4329893080223c9da8263e76`. The pictured class-4 and code-20/357/1329 profiles were checked against official [`nks-ch6.pdf`](https://files.wolframcdn.com/pub/www.wolframscience.com/nks/nks-ch6.pdf), SHA-256 `5af1e53860bd4a6877961681cf49b16058a53ee55a2bfa8c64ac7cc13174bca0`. Chapter 3 Notes page 886 was checked against official [`nks-nts-ch3.pdf`](https://files.wolframcdn.com/pub/www.wolframscience.com/nks/nks-nts-ch3.pdf), SHA-256 `21666aa07f49e47483cdc9883e285b8cd47d397dd18eea0b72f05d4d3272a009`. Built-in examples were checked against official [`nks-notes.pdf`](https://files.wolframcdn.com/pub/www.wolframscience.com/nks/nks-notes.pdf), SHA-256 `549f043595653a7d276b07ba52d435700039b71427b4e1774a44b1a58eff4723`. The truncated 2D caption was checked against official [`nks-ch7.pdf`](https://files.wolframcdn.com/pub/www.wolframscience.com/nks/nks-ch7.pdf), SHA-256 `44d1eebd831f780da80bd8a383016aa9cec6aa7ff666fd33690f679c8479210f`.
2. **`BOOK:3914` truncation.** The monolith retains only the caption tail beginning `total is exactly 4`. The official Chapter 7 caption restores: a random initial condition; the nine-cell neighborhood of self plus eight adjacent cells including diagonals; white for totals below 4; black for totals above 6; white for total 5; and black for total 4. The Chapter 7 split line 491 also restores an opening clause but compresses away most of this official rule, so it is corroboration, not normalization authority.
3. **`BOOK:11037` truncation.** The official all-Notes page continues the sentence with `page 927.` The normalized pointer is: totalistic implementation page 886; higher-dimensional implementation page 927. It carries routing only.
4. **`BOOK:11168` invocation OCR.** `ln[11]`, displaced brackets, and the call shape are extraction errors. Official all-Notes gives normalized `In[11] := Show[RasterGraphics[CellularAutomaton[{867, {3, 1}, 1}, {{1}, 0}, 50]]]`. The prose identity `code 867`, `k=3`, `r=1` is intact in the monolith.
5. **`BOOK:11897` formula OCR.** The totalistic formula `k^(1+(k-1)(2r+1))` and all three numeric checks are intact. The adjacent symmetric-count extraction `$k^{1/2}k^{r+1}$` is malformed; official page 886 shows `k^(1/2 k^(r+1) (1+k^r))`. That sibling formula is not used to derive T03.
6. **`BOOK:11916` operator OCR.** The monolith's `$k \wedge Table[i-1,...]$` must be `$k^Table[i-1,...]$`; official page 886 visibly confirms the caret. The totalistic all-one vector `Table[1,{2r+1}]` is intact.
7. **Average/sum reconciliation.** This is normalization, not a textual repair. With the required value assignment and fixed arity `q=2r+1`, average is exactly `sum/q`, so it induces the same ordered cases. No float arithmetic is licensed. For `k>2`, changing the values assigned to colors can change which rules are totalistic, exactly as `BOOK:11897` warns.
8. **Digit direction.** `BOOK:776` puts average/sum zero at the rightmost displayed element. `IntegerDigits[num,k,M]` at `BOOK:11912` returns most-significant-first digits, and negative indexing at `BOOK:11904,11908` selects the rightmost digit for sum zero. Thus `U_s=floor(num/k^s) mod k`; leading zero digits are real rows, not omitted defaults.
9. **Strict figure/code 777.** The OCR text never says `777`; the pinned strict raster visibly shows high-to-low digits `1,0,0,1,2,1,0`. Reversing into sum order gives `0,1,2,1,0,0,1`, whose base-3 value is 777. This repairs a missing text label only; raster tone and geometry remain observer data.
10. **Split wording and routing.** Chapter 3 split line 89 changes strict `can not only` to `can be not only`; the official PDF agrees with the monolith. `BACK-MATTER/Index/Index.md` is Notes, while the actual split Index is embedded in `BACK-MATTER/Colophon/Colophon.md` from line 3383. Canonical `BOOK` physical lines remain primary.
11. **Boundary discipline.** White-background filtering and the single-gray seed are gallery controls; additive, reversible, universal, quiescent, weighted, outer, growth, continuous, 2D, network, application, and emulation evidence is explicitly relation/sibling material. None supplies a default row, seed, boundary, stopping condition, alternate reducer, or T03 executor branch.
12. **`BOOK:14632` radius OCR.** The monolith says `k = 2, t = 2 totalistic rule with code 20`, but `t` is an extraction substitution. Official all-Notes page 958 says `k = 2, r = 2 totalistic rule with code 20`. The same official passage confirms a 65,535-node network after one step and shortest excluded block length 36. The repair identifies the already-audited binary radius-two profile; the network size and excluded-block length remain properties, not transition semantics.
13. **Bidirectional source/asset closure.** Reverse traversal from every non-control textual disposition, across directly adjacent and contiguous same-construction image runs, now adds 48 physical links beyond the earlier 70-link ledger: `BOOK:2924,3900,3908,3912,5086,5092,5220,5484,5636,10259,10393,10409,11184,11186,11188,11190,13599,13603,13605,13607,13609,13611,13615,13648,13652,13656,15211,15213,15215,15217,15219,15223,15225,15227,15229,15231,15235,15237,15239,15241,15243,15313,15315,15317,15319,17433,19236,19238`. The additive self-reproduction and feature-extraction rasters (`10259,17433`) are relation-only; 44 are explicit geometry/application/non-totalistic controls; and the two page-1152 plots are included property continuations for code `1004600`. The final source oracle and independent metadata oracle assert exact equality over all 118 link targets, with ledger partition `50 I / 60 X / 8 R`.
14. **Code-`1004600` route repair.** `BOOK:9166` names the four-color totalistic rule and its undecidability application; `BOOK:20980` interleaves the actual-Index route `Code 1004600 ... undecidability, 754, 1137` with neighboring columns; `BOOK:19234` is the direct Notes continuation and `BOOK:19236,19238` are its two plots. The source states measurements through at least 20 million steps, not eventual outcomes. This repairs evidence closure without adding transition semantics.

### Citation, verbatim, source-repair, asset, and combinatoric oracle

This check expands every `BOOK:` citation anywhere in this stage, verifies every monolith blockquote against its nearest provenance, pins all damaged monolith forms and official downloads, and checks the strict codec independently.

```bash
python3 - <<'PY'
import ast, hashlib, re, subprocess
from pathlib import Path
from PIL import Image

book=Path('ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md')
stage=Path('goal-1/22-T03-TOTALISTIC-CA.md')
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

# Every cited physical line is explicitly traversed, including ranges in
# sections maintained by other audit workers.
cited=refs(text)
assert cited and all(1 <= n <= len(L) for n in cited)
assert len(cited)==211
for n in sorted(cited):
    _=L[n-1]

# All verbatim monolith material in Book Excerpts is a blockquote. Each
# fragment must occur on one of the immediately preceding provenance lines.
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
assert quote_count==89 and len(quote_lines)==86

# Pin every monolith defect normalized above.
assert L[3913].startswith('total is exactly 4, then it becomes black.')
assert L[11036].endswith('higher-dimensional cellular automata on')
assert '$ln[11]' in L[11167] and 'code 867' in L[11167]
assert '$k^{1/2}k^{r+1}$' in L[11896]
assert '$k^{1+(k-1)(2r+1)}$' in L[11896]
assert r'$k \wedge Table[i-1, \{i, 2r+1\}]$' in L[11915]
assert 'k = 2, t = 2 totalistic rule with code 20' in L[14631]

official={
'/tmp/nks-ch3.pdf':'d4005b27774084c276e67d46a6c79106b93b785d4329893080223c9da8263e76',
'/tmp/nks-ch6.pdf':'5af1e53860bd4a6877961681cf49b16058a53ee55a2bfa8c64ac7cc13174bca0',
'/tmp/nks-nts-ch3.pdf':'21666aa07f49e47483cdc9883e285b8cd47d397dd18eea0b72f05d4d3272a009',
'/tmp/nks-notes.pdf':'549f043595653a7d276b07ba52d435700039b71427b4e1774a44b1a58eff4723',
'/tmp/nks-ch7.pdf':'44d1eebd831f780da80bd8a383016aa9cec6aa7ff666fd33690f679c8479210f',
}
for name,want in official.items():
    data=Path(name).read_bytes()
    assert hashlib.sha256(data).hexdigest()==want,name

def pdf_text(name):
    raw=subprocess.check_output(['pdftotext','-layout',name,'-'],text=True,errors='replace')
    return re.sub(r'\s+',' ',raw)
strict=pdf_text('/tmp/nks-ch3.pdf')
ch6=pdf_text('/tmp/nks-ch6.pdf')
nts=pdf_text('/tmp/nks-nts-ch3.pdf')
notes=pdf_text('/tmp/nks-notes.pdf')
ch7=pdf_text('/tmp/nks-ch7.pdf')
assert 'The idea of a totalistic rule is to take the new color of each cell to' in strict
for c in (20,357,1329,1659,1632): assert f'code {c}' in ch6,c
assert 'condition number 151 we finally see a structure that persists.' in ch6
assert 'evolution from the first twenty-five billion possible initial conditions.' in ch6
assert 'repetition periods up to 15' in ch6
assert 'specific assignment of values to colors' in nts
assert 'respectively k ^Table[i - 1, {i, 2 r + 1}] and Table[1, {2 r + 1}]' in nts
assert 'page 927.' in notes
assert 'This runs the totalistic k=3 , r =1 rule with code 867.' in notes
assert 'In[11] : = Show[RasterGraphics[CellularAutomaton[{867, {3, 1}, 1}, {{1}, 0}, 50]]]' in notes
assert 'largest network, with 280 nodes and 551 arcs. The k = 2 , r = 2' in notes
assert 'totalistic rule with code 20 gives a network with 65535 nodes' in notes
assert 'sequences. (The shortest excluded block for code 20 is of' in notes
assert 'length 36.)' in notes
assert 'Behavior of a two-dimensional cellular automaton starting from a random initial condition.' in ch7
assert '9-cell neighborhood consisting of the cell itself and the 8 cells adjacent to it (including diagonals).' in ch7
for fragment in ('If this total is less than 4','if the total is greater than 6',
                 'exactly 5, then the cell becomes white','total is exactly 4, then it becomes black.'):
    assert fragment in ch7
asset=Path('ref/A-New-Kind-of-Science/CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_75_Figure_6.jpeg')
assert hashlib.sha256(asset.read_bytes()).hexdigest()=='acb13963632286960ca61b616ff2f45a940750f3ab7deb5e6fbf696543015c15'

# Independently replay the exact 118-link source/metadata join, then hash
# and dimension-check every physical raster named by the metadata ledger.
search=re.split(r'^## Search Log\s*$',text,flags=re.M)[1]
search=re.split(r'^## Book Excerpts\s*$',search,flags=re.M)[0]
asset_code=search.split('assets={',1)[1].split('for n,want in assets.items()',1)[0]
source_assets={int(n):v for n,v in re.findall(r"(\d+):'(!\[\]\([^)]+\.jpeg\))'",asset_code)}
assert len(source_assets)==118
for n,want in source_assets.items(): assert L[n-1]==want,(n,L[n-1],want)
manifest_names={re.fullmatch(r'!\[\]\(([^)]+)\)',v).group(1) for v in source_assets.values()}
audit=re.split(r'^## Asset and Raster Audit\s*$',text,flags=re.M)[1]
items_src=audit.split('\nitems={',1)[1].split('\n}\n\ndef jpeg_size',1)[0]
items=ast.literal_eval('{'+items_src+'}')
assert len(items)==118 and len({Path(p).name for p in items})==118
assert {Path(p).name for p in items}==manifest_names
counts={'I':0,'X':0,'R':0}
base=Path('ref/A-New-Kind-of-Science')
for rel,(size,w,h,digest,kind) in items.items():
    p=base/rel; data=p.read_bytes()
    assert len(data)==size and hashlib.sha256(data).hexdigest()==digest,rel
    with Image.open(p) as im: assert im.size==(w,h),(rel,im.size,(w,h))
    counts[kind]+=1
assert counts=={'I':50,'X':60,'R':8}

# Independent finite arithmetic checks.
assert 2**4==16 and 2**6==64 and 3**7==2187 and 5**13==1_220_703_125
assert (2**3 + 2**2)//2 == (2**(1+1)*(1+2**1))//2 == 6
sum_digits=[0,1,2,1,0,0,1]
assert sum(d*3**s for s,d in enumerate(sum_digits))==777
for k,r in ((2,1),(2,2),(3,1),(5,1),(8,1)):
    q=2*r+1; M=1+(k-1)*q
    reachable={sum(v) for v in __import__('itertools').product(range(k),repeat=q)}
    assert reachable==set(range(M))
    assert k**M==k**(1+(k-1)*(2*r+1))
assert 8**22==2**66
print(f'T03 evidence oracle: PASS cited={len(cited)} quote_fragments={quote_count} quote_lines={len(quote_lines)} assets={len(items)} repairs=6 pdfs=5')
PY
```

Expected terminal line:

```text
T03 evidence oracle: PASS cited=211 quote_fragments=89 quote_lines=86 assets=118 repairs=6 pdfs=5
```

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

D112's structural-table-first and arbitrary-precision policy composes at the finite-table/serialization responsibility level; T03 has a distinct sum-case domain and codec from T02's ordered context table. D114 is resolved concretely: T03's explicit valuation `nu` supplies both aggregate summands and output-code digits; T02 alphabet rank remains an independent identity and may coincide with `nu` only in the canonical integer profile; palette remains a view.

Evidence closure supplies an exact strict code-777 cell raster and exact code-777/code-867 trajectories. Other galleries intentionally remain label/property fixtures because the source omits at least one of seed serialization, boundary, horizon convention, crop, palette, or resampling. No audited source requires a non-bijective valuation, radius zero, dynamic/masked arity, histogram, outer-totalistic, unequal weights, or higher-dimensional geometry; Goal 2 therefore exposes those as typed unsupported or separate constructions until their own stages justify sharing, rather than inferring defaults.

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

# A noncanonical valuation is semantic; tuple rank must not replace it.
alphabet=('red','green','blue')
rank={value:i for i,value in enumerate(alphabet)}
nu={'red':2,'green':0,'blue':1}
inverse={number:value for value,number in nu.items()}
symbolic=tuple(inverse[number] for number in digits(777,3,1))
assert symbolic==('green','blue','red','blue','green','green','blue')
assert sum(nu[value]*3**s for s,value in enumerate(symbolic))==777
assert tuple(inverse[number] for number in digits(777,3,1))==symbolic
context=('red','red','red')
assert sum(nu[value] for value in context)==6
assert symbolic[sum(nu[value] for value in context)]=='blue'
assert symbolic[sum(rank[value] for value in context)]=='green'
try:
    nu['outside']
    raise AssertionError('out-of-domain value accepted')
except KeyError:
    pass

assert all(out(420,3,1,q)==(-sum(q))%3 for q in product(range(3),repeat=3))
r2_tables={
    10:((0,1,0,1,0,0),{1,3}),
    20:((0,0,1,0,1,0),{2,4}),
    52:((0,0,1,0,1,1),{2,4,5}),
}
for code,(want,black_sums) in r2_tables.items():
    got=digits(code,2,2)
    assert got==want
    assert sum(value*2**s for s,value in enumerate(got))==code
    assert all(out(code,2,2,q)==(sum(q) in black_sums)
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
print('rule_10_20_52_r2_digits=',tuple(digits(code,2,2) for code in (10,20,52)))
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
rule_10_20_52_r2_digits= ((0, 1, 0, 1, 0, 0), (0, 0, 1, 0, 1, 0), (0, 0, 1, 0, 1, 1))
rule_777_trace= 1,111,12121,1100011,122101221,11001210011,1221110111221,110001222100011,12210110101101221
rule_777_counts= (13972, 4386, 2347)
rule_777_sha256= 4e835285f8b44f62ff98ae3ed4eccf4083b93d565121c0ebbbcc7889fae8878e
```

## Asset and Raster Audit

The native asset boundary is one-dimensional, synchronous, finite-color totalistic evolution. The strict run begins with the rule-777 definition on printed page 60 and ends with the 9,000-step rule-1599 view on printed page 70. Printed page 71 changes construction to mobile automata with one active site and is excluded. Later one-dimensional totalistic galleries include the complete Chapter 6 binary-radius-two code-`20` and three-color code-`357`/`1329` structure sequence; exact Notes invocations, property illustrations, and relation panels also remain evidence. A numbered or random seed, search bound, palette, crop, displayed-row count, period, or behavior label is never imported into rule identity.

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
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_253_Picture_1.jpeg` | 511,097 | `1227x1519` | `148a433a11b4889c91c1a7be3c6f00172a3961428e6d41c47a06954136245faf` | Class-4 code `1659`; its visible label and the Actual Index repair monolith `BOOK:2834`'s isolated OCR/page-number contamination `238`. Notes code `1662` is distinct and unpictured. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_254_Picture_1.jpeg` | 568,496 | `1117x1383` | `d32b7fc3dedc9f262e5a3d3d928d1d7d94d1a219fd75aeeefdb988c74869a168` | Class-4 code `2043`, same random-run disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_2.jpeg` | 7,400 | `273x171` | `b175f64e60cf41042d8ba6a11ed8d04eec4a8101bef8f9f231aae532eca6ca06` | Borderline-class code `219`; class assignment is an observer property. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_3.jpeg` | 13,612 | `259x167` | `00ef0063254d4f75734cd76d8f2d07de4ae1d6b041b9664197c2da99641d8b14` | Borderline-class code `438`; same disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_4.jpeg` | 9,310 | `267x186` | `700d71a0beb145c953ca87f4d8649aecd7b7d60df69ccd569cba02f6daeb1acc` | Borderline-class code `1380`; same disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_5.jpeg` | 11,188 | `273x165` | `ae44e4411841a03fced5b5114f6cef4be62793c6a58c9a4ce6c357d214c7ce35` | Borderline-class code `1632`; same disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_256_Figure_2.jpeg` | 328,297 | `1092x1367` | `1c4967f6967d8e813b2a281e2615dc8bef272eb57789b60e23c950de5e6bc01f` | Four-color radius-one totalistic sequence across behavior classes; the selection/class transition is downstream analysis. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_297_Picture_2.jpeg` | 50,047 | `1111x408` | `953c15d2e64464aceadb6181639cf36973db9513d6e0b7fc3fb43564efc65be8` | Binary radius-two code `20` from a completely random initial condition; direct T03 program/property evidence. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_297_Picture_4.jpeg` | 117,894 | `1127x415` | `26b299987a91daf8d15fc226c845c7efa7d55b9aa4221a4e6d41646b8c384204` | Three-color radius-one code `357` companion under the same random-run/class-4 disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_297_Picture_6.jpeg` | 156,786 | `1123x408` | `b94ac983e3496b023a1a991b15a701de9a1c4c5cba75a84b16254c497a1c76f1` | Three-color radius-one code `1329` companion. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_298_Figure_2.jpeg` | 209,088 | `1159x1297` | `7cacf2667a3f923d35106ec7eff09b9ce551d79dd828f8661458dd121bda09df` | Code `20` for every binary initial condition supported in a region of size below nine; initial-condition numbers are base-2 run data. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_299_Picture_3.jpeg` | 127,700 | `1150x600` | `32d4ed4b16a083fb731c37cc80c64efb9995756808c316a0ced0dea0e9bd5475` | Persistent code-`20` structures found by testing the first 25 billion initial conditions; reflected copies remain possible. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_300_Figure_1.jpeg` | 286,267 | `1150x1192` | `ee5ea91d3855bf31bd793f02677c0c19d9203ac20532b3b7bb07df838065294c` | All code-`20` persistent structures with periods through 15, found systematically; search result, not successor mechanics. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_301_Picture_2.jpeg` | 134,324 | `906x699` | `3e9aec2832697e07ea20391c1454e022bc8578fcfb4c126bbb53e6fdfe3f6eb3` | Code-`357` base-3 search labels six initial-condition/period pairs, including moving `4,803,890/41R` and `514,454,827/48L`; no period below 5 exists. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_302_Picture_3.jpeg` | 123,792 | `1036x712` | `4ec6db32d4f0b659a8519110b7885e05487e68d0348b390323daa55e7b322fd1` | Code-`1329` labels nine structures, including moving `916/31R` and `2,669/48R`; label/direction data are property fixtures. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_303_Picture_2.jpeg` | 136,635 | `616x1053` | `26ec2731176f7ef4b471b4f395f3968eefa69e0eba88a3f672268129d68e07aa` | Code `1329`, initial condition `54,889`: a 10-cell block grows without bound; its moving right part has period 256 and leaves infinitely many persistent structures. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_304_Picture_2.jpeg` | 179,601 | `1109x1363` | `21cc5432bcfcc379619d43c076f3102a3e12d64cd724d9fe5709055b72874ecf` | Further code-`1329` unbounded-growth profiles from `54,889`, `97,439`, `166,426`, `115,396`, and `2,069,116`, spanning complex and simple outcomes. |
| `CHAPTERS/9-Fundamental-Physics/Images/_page_541_Picture_3.jpeg` | 37,411 | `436x268` | `83d828ba45f3f3e7390bf66183643a32c3c7b83646cc3880aedf099a49284c1e` | Code `294` persistent structures on a largely random background; random field is not serialized. |
| `CHAPTERS/9-Fundamental-Physics/Images/_page_541_Picture_4.jpeg` | 43,238 | `418x250` | `d96c865b43b912ce4e2d6f0c2ddf659eed32f17db48c151161c364187fcc7a1f` | Code `1893` persistent boundaries on a largely random background; same disposition. |
| `CHAPTERS/11-The-Notion-of-Computation/Images/_page_707_Figure_1.jpeg` | 327,160 | `1130x1111` | `974e12d28e8acc6fb4af26f7b1dd09eae1f30d802666a61f41abed8ec2d42e19` | Mixed class-4 gallery with direct T03 panels `(c)` binary radius-two code `52` and `(d)` three-color code `1815`; panels `(a,b)` are ECA/second-order siblings within the same asset. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_753_Picture_3.jpeg` | 164,036 | `912x565` | `8cfad05d53abb9791d37dd6d8262ec12dbc08bb1d72866ce34c46ecb99a94a88` | Codes `870,843,1599` used to illustrate reducibility; the property label is not executable rule data. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_769_Figure_1.jpeg` | 298,516 | `1065x1308` | `a980effe214906d991e8ca9180cb9f9d6eade2f978a8358487a60bb1728058f3` | Four-color code `1004600` with four illustrated finite seeds. Seed strips are not serialized as digit arrays, so death/unknown outcomes are property evidence only. |
| `BACK-MATTER/Colophon/Images/_page_1152_Figure_5.jpeg` | 7,164 | `284x95` | `b9c448472b4f1c2059e542b73a754cd44d7ca8460cea4a665ad206e93f680114` | Notes continuation for code `1004600`, case (c): fluctuations through at least 20 million steps. This is an included measured-property view, not a trajectory or outcome golden. |
| `BACK-MATTER/Colophon/Images/_page_1152_Figure_6.jpeg` | 6,185 | `268x93` | `c21b0f6c3ab30d2ff50c0384efedaa7c1fe2c1a576301ac3481a29b229cf778e` | Notes continuation for code `1004600`, case (d); same observer-only disposition. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_25.jpeg` | 5,511 | `211x117` | `d53637ce9ec50330d5fa6239b23f48d57b563266a0085a23517d4538020fd5fb` | Exact Notes invocation `CellularAutomaton[{867,{3,1},1},{{1},0},50]`: code `867`, single `1`, repeating-`0` background, 50 updates. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_897_Picture_19.jpeg` | 37,091 | `553x155` | `2cedbff5433363c86786feea8804c95229179daf455f07ee8071d6345223894b` | Binary radius-two code `10`, whose table makes sums `1` and `3` black; source identifies a single-black start but not this panel's exact displayed-row convention. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_897_Picture_20.jpeg` | 77,026 | `543x329` | `ee9cadafa6b0b5a45d9cfb4ed310aff751e84f46a86277821e9f971f3c067b3f` | Long companion view for the same code-`10` Notes example; no independent rule or exact horizon. |
| `BACK-MATTER/Index/Images/_page_963_Picture_8.jpeg` | 3,114 | `144x152` | `1fb4f0b4c03d8ba9f9fdeb67a0bbda2d786ed7ceeb13cdd8c31337ccd54bcdfb` | First Notes frequency-of-classes chart for one-dimensional totalistic `k,r` profiles; aggregate property only. |
| `BACK-MATTER/Index/Images/_page_963_Picture_9.jpeg` | 3,226 | `136x148` | `515f5de1423a9164ed6def92d786346f64c15a0a87ba07b723c069e62829caf6` | Second frequency chart; same disposition. |
| `BACK-MATTER/Index/Images/_page_963_Picture_10.jpeg` | 3,654 | `138x158` | `4b5ff621a668c5b706cdec0481cf3849facb7395d256dfd7c39b471d95fd018f` | Third frequency chart; same disposition. |
| `BACK-MATTER/Index/Images/_page_963_Picture_11.jpeg` | 3,717 | `136x152` | `7c660bbbb03b2d3116aab32cd50a5a3ff094961d49b403148531b36759335d6b` | Fourth frequency chart; same disposition. |
| `BACK-MATTER/Index/Images/_page_979_Figure_4.jpeg` | 16,090 | `573x120` | `acbfe15808099d36b2802a8aa10a946bf4f70870241799b795f8b4d1dfcab132` | Direct code-`20` survival-data chart: 72 of the first 1,000 initial conditions persist; source also records `60,171/1,000,000` and `71,079,205/1,000,000,000`. |

### Relations, exclusions, and routing

| Asset path | Bytes | Dimensions | SHA-256 | Disposition |
|---|---:|---:|---|---|
| `CHAPTERS/11-The-Notion-of-Computation/Images/_page_670_Figure_1.jpeg` | 281,966 | `1064x1224` | `a1a2a5c04b509ecc0357273387b2950d179478c65406427751904987ec9e8d3e` | Relation-only: code `1599` is block-emulated by a binary radius-five CA. Encoding/decoding and the emulator are not T03 native events. |
| `CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_171_Picture_5.jpeg` | 4,640 | `277x91` | `6695e1c946cf6adaa04a3915f2c720f69de4d18b74a81a01aaab346052119455` | Relation-only continuous average-map analog; continuous values/codomain belong to T44. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_21.jpeg` | 25,918 | `583x225` | `5f829c7776b53963e578df5a783553320da171c4e1c4d92c470899ec5bb3e40d` | Relation-only `k=2..7` additive/Pascal-modulo-`k` gallery. Its `k=3` panel supplies the comparison cited for T03 code `420`, but the displayed rule is not a native equal-weight total over self plus neighbors. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_839_Figure_4.jpeg` | 36,753 | `1154x277` | `851cf63cb497d076054d9b3cedf0db108f0cb439a7876726075eb82b5cfe0f6c` | Relation-only two-dimensional additive outer-totalistic code `204` self-reproduction example. It illustrates the cited additive construction, but its geometry and center-separated rule are not T03. |
| `BACK-MATTER/Index/Images/_page_980_Picture_15.jpeg` | 4,385 | `160x195` | `641317f32d429dd61b8353e1ebe65bd80f30950df78f0ebdc3a7f99b6bd26cd9` | Relation-only Life-spacefiller step 5, explicitly called analogous to code-`1329` unbounded growth. Two-dimensional Life is not T03. |
| `BACK-MATTER/Index/Images/_page_980_Picture_16.jpeg` | 5,858 | `172x187` | `90df3d1e1e99ed74dd1844654ff41b04b23f6fe22552cefa2b72f659cd0c5fda` | Relation-only step-50 companion of the same analogy. |
| `BACK-MATTER/Index/Images/_page_980_Picture_17.jpeg` | 8,261 | `223x207` | `3ad70eb7f740edf7749700ff107f08306830f3e3fd617f2df3f9e7e559178e21` | Relation-only history view of the Life spacefiller. |
| `BACK-MATTER/Index/Images/_page_1092_Picture_6.jpeg` | 21,682 | `583x141` | `b13e50f8bb2f7e905b8580ea94d93c7295e5967125aa8042defe76936bdb1dd6` | Relation-only feature-extraction application using the 16 even-numbered five-neighbor totalistic rules. The named rule family is relevant, but the image-analysis pipeline is not native T03 evolution. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_74_Picture_5.jpeg` | 134,131 | `858x423` | `713c4c55c6a004d76c5e47f1f39513bb1656f35feb0fe9aa72c4503ca311cdc6` | Immediate preceding rule-73 ECA material; exhaustive ordered binary rule, not a totalistic fixture. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_86_Picture_7.jpeg` | 30,221 | `240x500` | `59213fbf1a0e6904a6566043c889acd32853d799d5a71bfec1e2d0c45bb1eec5` | First post-boundary mobile-automaton evolution: one active site and sequential movement, not all-site T03. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_86_Picture_8.jpeg` | 7,295 | `506x51` | `d844f2419d7ff2a748a93e4ae6dd09c947bf5ed0723aa1defb4354c810b1fb25` | Mobile-automaton rule diagram paired with Picture 86/7; same exclusion. All later page-86+ mobile galleries inherit this construction boundary. |
| `CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_185_Picture_9.jpeg` | 3,425 | `213x114` | `abfbc90a8bdab839ac452194adf8f7e30258e877967a79ac71db59b1a716df75` | Two-dimensional center-plus-four-neighbor totalistic form; different support geometry. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_261_Figure_2.jpeg` | 309,273 | `1109x1297` | `49f35fe65202ef7fbfee2da92b7460d36fc329b66a553782ebf8991f237944dd` | Two-dimensional five-cell totalistic random gallery; geometry sibling, not a T03 raster. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_262_Figure_2.jpeg` | 240,733 | `1013x1291` | `23df7e86bf96a148a17c13847eb53c773a24f86cc5a24f2e1a550f79b94439e3` | Continuation of the two-dimensional totalistic random gallery; same geometry exclusion. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_305_Picture_2.jpeg` | 642,889 | `1184x1342` | `7e75ba3d0cb57a0b35d5a7b29e803386617e1ede22eefae19ce6e21fc465a9c9` | Rule-`110` binary boundary immediately after the code-`1329` sequence; a general ordered ECA, not totalistic. |
| `CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_349_Figure_1.jpeg` | 303,889 | `1145x1301` | `318e1b2d307bb11fe72981139b9e27bc9ce2123c95cd79b259cb8f75bebe6f2b` | Two-dimensional outer-totalistic code `746` construction; geometry and center-separated codec exclude it. |
| `CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_350_Picture_4.jpeg` | 85,362 | `1170x692` | `83000d21d7b66a38db4198b1340b5106c403df7f60e8d626b3bd00a68becdfa3` | Domain/initial-condition bridge in the same code-`976` two-dimensional construction continued on the next page; excluded with that construction. |
| `CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_351_Figure_2.jpeg` | 230,794 | `1143x1255` | `617cf03ce1508fd00b3b54473d469849141efb77b84ed37ff9110bb6b082b3f2` | Two-dimensional totalistic code `976` continuation; different geometry. |
| `CHAPTERS/8-Implications-for-Everyday-Systems/Images/_page_442_Figure_5.jpeg` | 86,047 | `1087x355` | `2c78e0ade6f15b54c6f693aeccc052a0aea3a326fc4c28c73988fb712e7c0d59` | Two-dimensional unequal/negative-weight cellular automaton; weighted sums are outside T03 equal-weight identity. |
| `CHAPTERS/8-Implications-for-Everyday-Systems/Images/_page_443_Picture_1.jpeg` | 254,542 | `1147x952` | `9c82adac1ac31b45d85e3228a2000d06bf84edc6afc1a84bedf036e51b3d78c8` | Next-page weight-grid continuation of the same unequal-weight construction; excluded with it. |
| `CHAPTERS/9-Fundamental-Physics/Images/_page_451_Picture_6.jpeg` | 187,275 | `1103x483` | `e7bbbefb729e76dd5d080d0b841a485ece898d9c3197780b4871c742d61a4e89` | Three-color nearest-neighbor reversible general rules inherited from T04's governing caption; unrestricted ordered tables, not totalistic. |
| `CHAPTERS/9-Fundamental-Physics/Images/_page_476_Figure_3.jpeg` | 295,434 | `1149x988` | `e661d9c28572ba62f75cf4b8a085e1580caf88b7c1c88bdd3c60a018e32ab108` | Three-color number-conserving reversible block cellular automata; block updates are outside T03. |
| `CHAPTERS/9-Fundamental-Physics/Images/_page_488_Figure_2.jpeg` | 119,358 | `1117x857` | `3589b325d67688d05fe0d9daa22eb1d0894fc119eff367426b00f08b509c0640` | Two-dimensional outer-totalistic codes `468,686,746` shown under different lattice orientations; geometry/orientation sibling only. |
| `CHAPTERS/10-Processes-of-Perception-and-Analysis/Images/_page_566_Figure_2.jpeg` | 140,400 | `1032x699` | `6d66d95c8e3c286272cded005d60557ce7a075ffebfd268486c23abe13a29a1e` | Two-dimensional **outer** totalistic rules `54,222,374`; center is retained separately and the codec differs. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_23.jpeg` | 4,478 | `160x117` | `132528352f363e52a20e73e1e8341203126448c0c6c8545eed48626eaddac16c` | Adjacent exact general ordered-table rule `921408`; T02, not aggregate identity. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_28.jpeg` | 5,342 | `205x110` | `2da239aceec3720e5aeccd5de8898c37fe7e975230814c0b3a8e3dcacbde9096` | Adjacent function-callback neighborhood rule; callback execution is explicitly not T03. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_31.jpeg` | 4,370 | `117x117` | `ca086555513a6d8ba5bcbe92d97af26e55aa899cf629e0ab61d8fa8c71b81586` | Adjacent 2D nine-neighbor totalistic code `3702`; geometry exclusion. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_32.jpeg` | 4,243 | `96x106` | `3acedb131c18307a21a76f249839dc24ad0838672ff715bb23816d1867164830` | Second panel in the contiguous code-`3702` two-dimensional Notes run; same geometry exclusion. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_33.jpeg` | 4,287 | `99x104` | `ab5cc8d4ecaab3970bedea51d269b13bf68f051765a0d98dc3980c6471adafae` | Third panel in the code-`3702` run; same exclusion. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_34.jpeg` | 4,514 | `105x106` | `ee453b116f28fbd33a87f8d372380b88d334f04164c873f0daf7fdf87425eed1` | Fourth panel in the code-`3702` run; same exclusion. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_35.jpeg` | 4,793 | `106x108` | `f13b56a4eab2a216cab3b59670dbac309108d3ffc3c5e16883fdc6c12a235e1f` | Fifth panel in the code-`3702` run; same exclusion. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_847_Figure_1.jpeg` | 111,064 | `1041x385` | `2d36e7eaeb3b073e68621ef5f9c1c397ae24ddc74fe06f26e62546ccc3af2902` | Purpose/doubling comparison containing a searched three-color general rule `5407067979`; application and unrestricted identity exclude it. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_848_Figure_2.jpeg` | 247,033 | `1194x1308` | `0bfecfeff1bd81072838e39704fc6572632dee083f91ddc4370909b0e2c5b5dd` | Gallery of three-color general rules selected to double an input; inherited T04 purpose/search control. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_23.jpeg` | 4,207 | `139x141` | `f14931f6bb008435e34961947dce7b11d5ec6d0bd4cc5b936bcee81b830adc0a` | First post-Pascal boundary: modulo-2 integer-function image, not a finite-color CA evolution. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_24.jpeg` | 5,507 | `135x138` | `5b302ed9d6c9cbee590270c7bdc169b62b554b0e186a94fdb3d1952a69c0f8c5` | `Multinomial[m,n]` modulo-2 companion; same exclusion. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_25.jpeg` | 4,057 | `138x145` | `f5eb9593ba90b4b240dc6990bb0e7204066cc48e81e82b96186029ff866d40da` | `StirlingS1[m,n]` modulo-2 companion; same exclusion. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_26.jpeg` | 4,999 | `135x155` | `badba07cc053bdf7f4e5b41d7d90b2b248d8acd75b9728898e10c69a59c7ceec` | `StirlingS2[m,n]` modulo-2 companion; same exclusion. |
| `BACK-MATTER/Index/Images/_page_979_Picture_6.jpeg` | 23,347 | `579x111` | `f9fe6970d82502f70cf371b503160c71047d290954ca19d5d37b4fd65c12fdc1` | Immediate post-code-`20` Notes boundary: rule-`110` background blocks, a general ECA view. |
| `BACK-MATTER/Index/Images/_page_943_Picture_21.jpeg` | 15,999 | `446x169` | `e83235d4ef16c1d9b077223255ed4cc7850d406e16142097313ae0b3b1beb1bb` | Historical complicated Ulam-system illustration; application context, not native T03 evidence. |
| `BACK-MATTER/Index/Images/_page_944_Picture_3.jpeg` | 3,576 | `114x102` | `df3027b377ea701cf677fe6aff772e6206887b1aa0f3c6b145d58ab33d330465` | First simplified component in the Ulam-system comparison run; construction sibling only. |
| `BACK-MATTER/Index/Images/_page_944_Picture_4.jpeg` | 3,646 | `94x114` | `48c13120c73f3af3bb1f257533f710b85dfdd8c8ba73ad7f83f2bd1c29affad4` | Second simplified component; same exclusion. |
| `BACK-MATTER/Index/Images/_page_944_Picture_5.jpeg` | 1,588 | `95x130` | `bf627766e988753602792aa2c26f3d16ecfc47e70a2b1dff98880ccc87cc146d` | Third simplified component; same exclusion. |
| `BACK-MATTER/Index/Images/_page_944_Picture_6.jpeg` | 4,200 | `107x124` | `3b777980e3dc09d80687d2c171b837d4bc4239dfc83d586e0076590dd3dd1b27` | Fourth simplified component, a two-dimensional outer-totalistic code-`686` sibling. |
| `BACK-MATTER/Index/Images/_page_944_Picture_7.jpeg` | 3,785 | `91x123` | `bb254f61cbcc53e56e7f90b3f62cafebf988e34d089caa74cb59ad233be59f20` | Fifth simplified component, including a one-dimensional rule-`90` boundary rather than T03. |
| `BACK-MATTER/Index/Images/_page_944_Picture_9.jpeg` | 25,952 | `577x243` | `6f09976c3f5eed3bb1c845bb621c323e7ddb53df0e537f16e6f21ee99f5cc813` | Two-dimensional outer-totalistic code `12`; geometry/codec sibling. |
| `BACK-MATTER/Index/Images/_page_945_Picture_2.jpeg` | 25,176 | `548x175` | `2b17dc927842b7cefa8d1aa777b46fb2a8634f4fc62386c00e301482add40743` | Lattice/geometry construction diagram adjacent to totalistic applications; not a T03 evolution. |
| `BACK-MATTER/Index/Images/_page_945_Picture_4.jpeg` | 38,810 | `545x247` | `6d138c039f5d319f8f8635d19b33cabbd6dbff7a68249de6810c7adfa79d5a71` | Pentagonal-tiling outer-totalistic code `4094`; non-one-dimensional support. |
| `BACK-MATTER/Index/Images/_page_945_Picture_6.jpeg` | 40,329 | `573x225` | `350a3c7090182a8c74d8890e4a92bc38cd51da2c72b648aca0084f44cc529a8b` | Penrose-tiling outer-totalistic code `254`; nonregular two-dimensional support. |
| `BACK-MATTER/Index/Images/_page_994_Picture_3.jpeg` | 3,818 | `119x109` | `bbae1064a5c23d5e9638c8587d33c804de3eb0f7cd907b7d5065d89693831c4d` | First panel of the generalized aggregation/rule-shape comparison; not a native T03 profile. |
| `BACK-MATTER/Index/Images/_page_994_Picture_4.jpeg` | 3,789 | `107x112` | `b1430c29bed143b063fbc07a34f1b5232d87fc479d90b2beca1afd87df5abd6f` | Second generalized-aggregation panel; same exclusion. |
| `BACK-MATTER/Index/Images/_page_994_Picture_5.jpeg` | 3,379 | `110x119` | `7d47e459b95d2f9765ab732968f40db589be265d0691f06b267b75aa487962a9` | Third generalized-aggregation panel; same exclusion. |
| `BACK-MATTER/Index/Images/_page_994_Picture_6.jpeg` | 2,430 | `107x115` | `c7214b5edb00142fdf7b117089a2fa8fe763aafbeac051c0575e9d1a1eb76d5a` | Fourth generalized-aggregation panel; same exclusion. |
| `BACK-MATTER/Index/Images/_page_994_Picture_7.jpeg` | 2,528 | `100x136` | `301f9a8a252bfc39f65c0fe450c17ca5a9cd6a961bb020b590f40d4e40c08e31` | Fifth generalized-aggregation panel; same exclusion. |
| `BACK-MATTER/Index/Images/_page_994_Picture_9.jpeg` | 5,035 | `183x77` | `cfc169f6a14d82765024f97c4243fba07e701120b4bfda59a010ac6c2bd8d6b6` | First panel of the totalistic constraint-`242` stalled-cluster construction; construction/application evidence only. |
| `BACK-MATTER/Index/Images/_page_994_Picture_10.jpeg` | 2,912 | `107x82` | `f75756db8ca610ad57e570a4974f651ba441f87d8221a55a8b849f8f292b2c62` | Second constraint-`242` stalled-cluster panel; same exclusion. |
| `BACK-MATTER/Index/Images/_page_994_Picture_11.jpeg` | 4,189 | `154x98` | `2494697ab01fc243d1b92a3f4079943780348309e86b7fa250dac67331e3a4cf` | Third constraint-`242` stalled-cluster panel; same exclusion. |
| `BACK-MATTER/Index/Images/_page_994_Picture_12.jpeg` | 2,747 | `89x74` | `f1a42e9a257ad91313b0093366d9f53237fdbedb5990f262d9d78066defb4eca` | Fourth constraint-`242` stalled-cluster panel; same exclusion. |
| `BACK-MATTER/Index/Images/_page_994_Picture_13.jpeg` | 1,602 | `68x78` | `42de6c6c444417416834e76ccf5081d74c39c406e6c69f12744fdab39a87dc4d` | Fifth constraint-`242` stalled-cluster panel; same exclusion. |
| `BACK-MATTER/Index/Images/_page_994_Picture_15.jpeg` | 3,434 | `119x113` | `75640a3f1ff18594d23a2c36bc5d80bb88f56efe2f0f1e028ac8609e661c06ff` | First successful-growth continuation of the same totalistic constraint-`242` construction; application-only. |
| `BACK-MATTER/Index/Images/_page_994_Picture_16.jpeg` | 2,760 | `99x125` | `11e152c786dfdc81aef5e3712d5313fa83ede32fbc2076162ad39ba9df18d728` | Second successful-growth panel; same exclusion. |
| `BACK-MATTER/Index/Images/_page_994_Picture_17.jpeg` | 3,823 | `102x134` | `941d67d3a4bc47e7b97e2b484e7cc356c45f0d295b67fe686e18738add871130` | Third successful-growth panel; same exclusion. |
| `BACK-MATTER/Index/Images/_page_994_Picture_18.jpeg` | 3,893 | `105x125` | `b13beb4041b967b60132de63976f2af13f276564476351c0091002711f4ed37a` | Fourth successful-growth panel; same exclusion. |
| `BACK-MATTER/Index/Images/_page_994_Picture_19.jpeg` | 3,955 | `93x117` | `e5b6d42985f1eafaa432f7c346aee085d1b1500b16b899e4f1a869046b94a667` | Fifth successful-growth panel; same exclusion. |
| `BACK-MATTER/Index/Images/_page_996_Picture_6.jpeg` | 9,894 | `138x266` | `b6d70c3a060261bb96c276ef158fd7bf7a3c1706b1003f5ab48621760baa299f` | First panel in the adjacent four-panel one-dimensional transition-rule control run; not the later named two-dimensional code-`52` alternative. |
| `BACK-MATTER/Index/Images/_page_996_Picture_7.jpeg` | 8,413 | `131x266` | `3d14c1bbb64711d9de00fdec771f592203daee10845daf0db519acdcbbe967e4` | Second transition-control panel; same exclusion. |
| `BACK-MATTER/Index/Images/_page_996_Picture_8.jpeg` | 8,414 | `123x260` | `6a39699460a0c9e5314801b0de51c7e5f41a41466f10abe9d83edc03dc3e3feb` | Third transition-control panel; same exclusion. |
| `BACK-MATTER/Index/Images/_page_996_Picture_9.jpeg` | 11,018 | `145x256` | `7595102ac69dcfab3a9b4817373c9ca2441e99f495b6b4c260e76d6f5da8aa26` | Fourth transition-control panel; same exclusion. |
| `BACK-MATTER/Colophon/Images/_page_1132_Picture_2.jpeg` | 68,468 | `606x308` | `422ce8c21c465e2ffdffdb0f691f9521a21b9389897336dd4e4a2c716295c589` | Adjacent three-color two-neighbor general rule `2144`; its totalistic-universality paragraph names candidates but this picture is not one. |

The monolith omits `Images/` from links. Chapter split files route to the same physical JPEGs and are duplicate references, not additional assets. The page-883/885 and page-897 files are Notes-for-Chapter-2 evidence despite their Chapter-12 placement. Page-943 onward Notes assets live under `BACK-MATTER/Index/Images`, while the page-1132 sibling lives under `BACK-MATTER/Colophon/Images`. The full code-`20` route includes the random overview, all sub-nine-cell starts, 25-billion search, systematic period-15 set, and survival chart; code `52` remains present in both the radius-two gallery and the mixed class-4 panel. The reverse join is finite and mechanical: start from every dispositioned textual candidate outside the query-false `controls` and index partitions, follow links at distance two, close contiguous image-only runs, and add only explicit prose-declared same-construction continuations. Images reachable solely from query-false controls remain outside this mandatory join unless separately selected as a boundary control. No two audited files have identical bytes.

The dependency-free metadata oracle parses JPEG SOF markers and pins all 50 included, 60 excluded, and eight relation-only files:

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
'CHAPTERS/6-Starting-from-Randomness/Images/_page_297_Picture_2.jpeg':(50047,1111,408,'953c15d2e64464aceadb6181639cf36973db9513d6e0b7fc3fb43564efc65be8','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_297_Picture_4.jpeg':(117894,1127,415,'26b299987a91daf8d15fc226c845c7efa7d55b9aa4221a4e6d41646b8c384204','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_297_Picture_6.jpeg':(156786,1123,408,'b94ac983e3496b023a1a991b15a701de9a1c4c5cba75a84b16254c497a1c76f1','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_298_Figure_2.jpeg':(209088,1159,1297,'7cacf2667a3f923d35106ec7eff09b9ce551d79dd828f8661458dd121bda09df','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_299_Picture_3.jpeg':(127700,1150,600,'32d4ed4b16a083fb731c37cc80c64efb9995756808c316a0ced0dea0e9bd5475','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_300_Figure_1.jpeg':(286267,1150,1192,'ee5ea91d3855bf31bd793f02677c0c19d9203ac20532b3b7bb07df838065294c','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_301_Picture_2.jpeg':(134324,906,699,'3e9aec2832697e07ea20391c1454e022bc8578fcfb4c126bbb53e6fdfe3f6eb3','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_302_Picture_3.jpeg':(123792,1036,712,'4ec6db32d4f0b659a8519110b7885e05487e68d0348b390323daa55e7b322fd1','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_303_Picture_2.jpeg':(136635,616,1053,'26ec2731176f7ef4b471b4f395f3968eefa69e0eba88a3f672268129d68e07aa','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_304_Picture_2.jpeg':(179601,1109,1363,'21cc5432bcfcc379619d43c076f3102a3e12d64cd724d9fe5709055b72874ecf','I'),
'CHAPTERS/9-Fundamental-Physics/Images/_page_541_Picture_3.jpeg':(37411,436,268,'83d828ba45f3f3e7390bf66183643a32c3c7b83646cc3880aedf099a49284c1e','I'),
'CHAPTERS/9-Fundamental-Physics/Images/_page_541_Picture_4.jpeg':(43238,418,250,'d96c865b43b912ce4e2d6f0c2ddf659eed32f17db48c151161c364187fcc7a1f','I'),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_707_Figure_1.jpeg':(327160,1130,1111,'974e12d28e8acc6fb4af26f7b1dd09eae1f30d802666a61f41abed8ec2d42e19','I'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_753_Picture_3.jpeg':(164036,912,565,'8cfad05d53abb9791d37dd6d8262ec12dbc08bb1d72866ce34c46ecb99a94a88','I'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_769_Figure_1.jpeg':(298516,1065,1308,'a980effe214906d991e8ca9180cb9f9d6eade2f978a8358487a60bb1728058f3','I'),
'BACK-MATTER/Colophon/Images/_page_1152_Figure_5.jpeg':(7164,284,95,'b9c448472b4f1c2059e542b73a754cd44d7ca8460cea4a665ad206e93f680114','I'),
'BACK-MATTER/Colophon/Images/_page_1152_Figure_6.jpeg':(6185,268,93,'c21b0f6c3ab30d2ff50c0384efedaa7c1fe2c1a576301ac3481a29b229cf778e','I'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_25.jpeg':(5511,211,117,'d53637ce9ec50330d5fa6239b23f48d57b563266a0085a23517d4538020fd5fb','I'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_897_Picture_19.jpeg':(37091,553,155,'2cedbff5433363c86786feea8804c95229179daf455f07ee8071d6345223894b','I'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_897_Picture_20.jpeg':(77026,543,329,'ee9cadafa6b0b5a45d9cfb4ed310aff751e84f46a86277821e9f971f3c067b3f','I'),
'BACK-MATTER/Index/Images/_page_963_Picture_8.jpeg':(3114,144,152,'1fb4f0b4c03d8ba9f9fdeb67a0bbda2d786ed7ceeb13cdd8c31337ccd54bcdfb','I'),
'BACK-MATTER/Index/Images/_page_963_Picture_9.jpeg':(3226,136,148,'515f5de1423a9164ed6def92d786346f64c15a0a87ba07b723c069e62829caf6','I'),
'BACK-MATTER/Index/Images/_page_963_Picture_10.jpeg':(3654,138,158,'4b5ff621a668c5b706cdec0481cf3849facb7395d256dfd7c39b471d95fd018f','I'),
'BACK-MATTER/Index/Images/_page_963_Picture_11.jpeg':(3717,136,152,'7c660bbbb03b2d3116aab32cd50a5a3ff094961d49b403148531b36759335d6b','I'),
'BACK-MATTER/Index/Images/_page_979_Figure_4.jpeg':(16090,573,120,'acbfe15808099d36b2802a8aa10a946bf4f70870241799b795f8b4d1dfcab132','I'),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_670_Figure_1.jpeg':(281966,1064,1224,'a1a2a5c04b509ecc0357273387b2950d179478c65406427751904987ec9e8d3e','R'),
'CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_171_Picture_5.jpeg':(4640,277,91,'6695e1c946cf6adaa04a3915f2c720f69de4d18b74a81a01aaab346052119455','R'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_21.jpeg':(25918,583,225,'5f829c7776b53963e578df5a783553320da171c4e1c4d92c470899ec5bb3e40d','R'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_839_Figure_4.jpeg':(36753,1154,277,'851cf63cb497d076054d9b3cedf0db108f0cb439a7876726075eb82b5cfe0f6c','R'),
'BACK-MATTER/Index/Images/_page_980_Picture_15.jpeg':(4385,160,195,'641317f32d429dd61b8353e1ebe65bd80f30950df78f0ebdc3a7f99b6bd26cd9','R'),
'BACK-MATTER/Index/Images/_page_980_Picture_16.jpeg':(5858,172,187,'90df3d1e1e99ed74dd1844654ff41b04b23f6fe22552cefa2b72f659cd0c5fda','R'),
'BACK-MATTER/Index/Images/_page_980_Picture_17.jpeg':(8261,223,207,'3ad70eb7f740edf7749700ff107f08306830f3e3fd617f2df3f9e7e559178e21','R'),
'BACK-MATTER/Index/Images/_page_1092_Picture_6.jpeg':(21682,583,141,'b13e50f8bb2f7e905b8580ea94d93c7295e5967125aa8042defe76936bdb1dd6','R'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_74_Picture_5.jpeg':(134131,858,423,'713c4c55c6a004d76c5e47f1f39513bb1656f35feb0fe9aa72c4503ca311cdc6','X'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_86_Picture_7.jpeg':(30221,240,500,'59213fbf1a0e6904a6566043c889acd32853d799d5a71bfec1e2d0c45bb1eec5','X'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_86_Picture_8.jpeg':(7295,506,51,'d844f2419d7ff2a748a93e4ae6dd09c947bf5ed0723aa1defb4354c810b1fb25','X'),
'CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_185_Picture_9.jpeg':(3425,213,114,'abfbc90a8bdab839ac452194adf8f7e30258e877967a79ac71db59b1a716df75','X'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_261_Figure_2.jpeg':(309273,1109,1297,'49f35fe65202ef7fbfee2da92b7460d36fc329b66a553782ebf8991f237944dd','X'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_262_Figure_2.jpeg':(240733,1013,1291,'23df7e86bf96a148a17c13847eb53c773a24f86cc5a24f2e1a550f79b94439e3','X'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_305_Picture_2.jpeg':(642889,1184,1342,'7e75ba3d0cb57a0b35d5a7b29e803386617e1ede22eefae19ce6e21fc465a9c9','X'),
'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_349_Figure_1.jpeg':(303889,1145,1301,'318e1b2d307bb11fe72981139b9e27bc9ce2123c95cd79b259cb8f75bebe6f2b','X'),
'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_350_Picture_4.jpeg':(85362,1170,692,'83000d21d7b66a38db4198b1340b5106c403df7f60e8d626b3bd00a68becdfa3','X'),
'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_351_Figure_2.jpeg':(230794,1143,1255,'617cf03ce1508fd00b3b54473d469849141efb77b84ed37ff9110bb6b082b3f2','X'),
'CHAPTERS/8-Implications-for-Everyday-Systems/Images/_page_442_Figure_5.jpeg':(86047,1087,355,'2c78e0ade6f15b54c6f693aeccc052a0aea3a326fc4c28c73988fb712e7c0d59','X'),
'CHAPTERS/8-Implications-for-Everyday-Systems/Images/_page_443_Picture_1.jpeg':(254542,1147,952,'9c82adac1ac31b45d85e3228a2000d06bf84edc6afc1a84bedf036e51b3d78c8','X'),
'CHAPTERS/9-Fundamental-Physics/Images/_page_451_Picture_6.jpeg':(187275,1103,483,'e7bbbefb729e76dd5d080d0b841a485ece898d9c3197780b4871c742d61a4e89','X'),
'CHAPTERS/9-Fundamental-Physics/Images/_page_476_Figure_3.jpeg':(295434,1149,988,'e661d9c28572ba62f75cf4b8a085e1580caf88b7c1c88bdd3c60a018e32ab108','X'),
'CHAPTERS/9-Fundamental-Physics/Images/_page_488_Figure_2.jpeg':(119358,1117,857,'3589b325d67688d05fe0d9daa22eb1d0894fc119eff367426b00f08b509c0640','X'),
'CHAPTERS/10-Processes-of-Perception-and-Analysis/Images/_page_566_Figure_2.jpeg':(140400,1032,699,'6d66d95c8e3c286272cded005d60557ce7a075ffebfd268486c23abe13a29a1e','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_23.jpeg':(4478,160,117,'132528352f363e52a20e73e1e8341203126448c0c6c8545eed48626eaddac16c','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_28.jpeg':(5342,205,110,'2da239aceec3720e5aeccd5de8898c37fe7e975230814c0b3a8e3dcacbde9096','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_31.jpeg':(4370,117,117,'ca086555513a6d8ba5bcbe92d97af26e55aa899cf629e0ab61d8fa8c71b81586','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_32.jpeg':(4243,96,106,'3acedb131c18307a21a76f249839dc24ad0838672ff715bb23816d1867164830','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_33.jpeg':(4287,99,104,'ab5cc8d4ecaab3970bedea51d269b13bf68f051765a0d98dc3980c6471adafae','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_34.jpeg':(4514,105,106,'ee453b116f28fbd33a87f8d372380b88d334f04164c873f0daf7fdf87425eed1','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_35.jpeg':(4793,106,108,'f13b56a4eab2a216cab3b59670dbac309108d3ffc3c5e16883fdc6c12a235e1f','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_847_Figure_1.jpeg':(111064,1041,385,'2d36e7eaeb3b073e68621ef5f9c1c397ae24ddc74fe06f26e62546ccc3af2902','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_848_Figure_2.jpeg':(247033,1194,1308,'0bfecfeff1bd81072838e39704fc6572632dee083f91ddc4370909b0e2c5b5dd','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_23.jpeg':(4207,139,141,'f14931f6bb008435e34961947dce7b11d5ec6d0bd4cc5b936bcee81b830adc0a','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_24.jpeg':(5507,135,138,'5b302ed9d6c9cbee590270c7bdc169b62b554b0e186a94fdb3d1952a69c0f8c5','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_25.jpeg':(4057,138,145,'f5eb9593ba90b4b240dc6990bb0e7204066cc48e81e82b96186029ff866d40da','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_26.jpeg':(4999,135,155,'badba07cc053bdf7f4e5b41d7d90b2b248d8acd75b9728898e10c69a59c7ceec','X'),
'BACK-MATTER/Index/Images/_page_979_Picture_6.jpeg':(23347,579,111,'f9fe6970d82502f70cf371b503160c71047d290954ca19d5d37b4fd65c12fdc1','X'),
'BACK-MATTER/Index/Images/_page_943_Picture_21.jpeg':(15999,446,169,'e83235d4ef16c1d9b077223255ed4cc7850d406e16142097313ae0b3b1beb1bb','X'),
'BACK-MATTER/Index/Images/_page_944_Picture_3.jpeg':(3576,114,102,'df3027b377ea701cf677fe6aff772e6206887b1aa0f3c6b145d58ab33d330465','X'),
'BACK-MATTER/Index/Images/_page_944_Picture_4.jpeg':(3646,94,114,'48c13120c73f3af3bb1f257533f710b85dfdd8c8ba73ad7f83f2bd1c29affad4','X'),
'BACK-MATTER/Index/Images/_page_944_Picture_5.jpeg':(1588,95,130,'bf627766e988753602792aa2c26f3d16ecfc47e70a2b1dff98880ccc87cc146d','X'),
'BACK-MATTER/Index/Images/_page_944_Picture_6.jpeg':(4200,107,124,'3b777980e3dc09d80687d2c171b837d4bc4239dfc83d586e0076590dd3dd1b27','X'),
'BACK-MATTER/Index/Images/_page_944_Picture_7.jpeg':(3785,91,123,'bb254f61cbcc53e56e7f90b3f62cafebf988e34d089caa74cb59ad233be59f20','X'),
'BACK-MATTER/Index/Images/_page_944_Picture_9.jpeg':(25952,577,243,'6f09976c3f5eed3bb1c845bb621c323e7ddb53df0e537f16e6f21ee99f5cc813','X'),
'BACK-MATTER/Index/Images/_page_945_Picture_2.jpeg':(25176,548,175,'2b17dc927842b7cefa8d1aa777b46fb2a8634f4fc62386c00e301482add40743','X'),
'BACK-MATTER/Index/Images/_page_945_Picture_4.jpeg':(38810,545,247,'6d138c039f5d319f8f8635d19b33cabbd6dbff7a68249de6810c7adfa79d5a71','X'),
'BACK-MATTER/Index/Images/_page_945_Picture_6.jpeg':(40329,573,225,'350a3c7090182a8c74d8890e4a92bc38cd51da2c72b648aca0084f44cc529a8b','X'),
'BACK-MATTER/Index/Images/_page_994_Picture_3.jpeg':(3818,119,109,'bbae1064a5c23d5e9638c8587d33c804de3eb0f7cd907b7d5065d89693831c4d','X'),
'BACK-MATTER/Index/Images/_page_994_Picture_4.jpeg':(3789,107,112,'b1430c29bed143b063fbc07a34f1b5232d87fc479d90b2beca1afd87df5abd6f','X'),
'BACK-MATTER/Index/Images/_page_994_Picture_5.jpeg':(3379,110,119,'7d47e459b95d2f9765ab732968f40db589be265d0691f06b267b75aa487962a9','X'),
'BACK-MATTER/Index/Images/_page_994_Picture_6.jpeg':(2430,107,115,'c7214b5edb00142fdf7b117089a2fa8fe763aafbeac051c0575e9d1a1eb76d5a','X'),
'BACK-MATTER/Index/Images/_page_994_Picture_7.jpeg':(2528,100,136,'301f9a8a252bfc39f65c0fe450c17ca5a9cd6a961bb020b590f40d4e40c08e31','X'),
'BACK-MATTER/Index/Images/_page_994_Picture_9.jpeg':(5035,183,77,'cfc169f6a14d82765024f97c4243fba07e701120b4bfda59a010ac6c2bd8d6b6','X'),
'BACK-MATTER/Index/Images/_page_994_Picture_10.jpeg':(2912,107,82,'f75756db8ca610ad57e570a4974f651ba441f87d8221a55a8b849f8f292b2c62','X'),
'BACK-MATTER/Index/Images/_page_994_Picture_11.jpeg':(4189,154,98,'2494697ab01fc243d1b92a3f4079943780348309e86b7fa250dac67331e3a4cf','X'),
'BACK-MATTER/Index/Images/_page_994_Picture_12.jpeg':(2747,89,74,'f1a42e9a257ad91313b0093366d9f53237fdbedb5990f262d9d78066defb4eca','X'),
'BACK-MATTER/Index/Images/_page_994_Picture_13.jpeg':(1602,68,78,'42de6c6c444417416834e76ccf5081d74c39c406e6c69f12744fdab39a87dc4d','X'),
'BACK-MATTER/Index/Images/_page_994_Picture_15.jpeg':(3434,119,113,'75640a3f1ff18594d23a2c36bc5d80bb88f56efe2f0f1e028ac8609e661c06ff','X'),
'BACK-MATTER/Index/Images/_page_994_Picture_16.jpeg':(2760,99,125,'11e152c786dfdc81aef5e3712d5313fa83ede32fbc2076162ad39ba9df18d728','X'),
'BACK-MATTER/Index/Images/_page_994_Picture_17.jpeg':(3823,102,134,'941d67d3a4bc47e7b97e2b484e7cc356c45f0d295b67fe686e18738add871130','X'),
'BACK-MATTER/Index/Images/_page_994_Picture_18.jpeg':(3893,105,125,'b13beb4041b967b60132de63976f2af13f276564476351c0091002711f4ed37a','X'),
'BACK-MATTER/Index/Images/_page_994_Picture_19.jpeg':(3955,93,117,'e5b6d42985f1eafaa432f7c346aee085d1b1500b16b899e4f1a869046b94a667','X'),
'BACK-MATTER/Index/Images/_page_996_Picture_6.jpeg':(9894,138,266,'b6d70c3a060261bb96c276ef158fd7bf7a3c1706b1003f5ab48621760baa299f','X'),
'BACK-MATTER/Index/Images/_page_996_Picture_7.jpeg':(8413,131,266,'3d14c1bbb64711d9de00fdec771f592203daee10845daf0db519acdcbbe967e4','X'),
'BACK-MATTER/Index/Images/_page_996_Picture_8.jpeg':(8414,123,260,'6a39699460a0c9e5314801b0de51c7e5f41a41466f10abe9d83edc03dc3e3feb','X'),
'BACK-MATTER/Index/Images/_page_996_Picture_9.jpeg':(11018,145,256,'7595102ac69dcfab3a9b4817373c9ca2441e99f495b6b4c260e76d6f5da8aa26','X'),
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
assert counts=={'I':50,'X':60,'R':8}
print('T03 metadata oracle: PASS 50 included; 60 excluded; 8 relation-only')
PY
```

Recorded output:

```text
T03 metadata oracle: PASS 50 included; 60 excluded; 8 relation-only
```

### Exact asset semantic oracle

This dependency-free check independently reconstructs the strict code-`777` table and early single-gray trajectory, the exact 50-update Notes invocation for code `867`, binary radius-two codes `10`, `20`, and `52`, and all strict labelled gallery identities. It also pins the Chapter 6 structure/search labels, code-`20` survival counts, code-`420` additivity, all 70 explicitly followed continuation/boundary links, and a mechanical reverse join from the textual partition into 104 mandatory raster links. Tables are LSB-first by integer sum; displays reverse them.

```bash
python3 - <<'PY'
import ast, re
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
3900:'![](_page_349_Figure_1.jpeg)',
3908:'![](_page_350_Picture_4.jpeg)',
3912:'![](_page_351_Figure_2.jpeg)',
5086:'![](_page_442_Figure_5.jpeg)',
5092:'![](_page_443_Picture_1.jpeg)',
5220:'![](_page_451_Picture_6.jpeg)',
5484:'![](_page_476_Figure_3.jpeg)',
5636:'![](_page_488_Figure_2.jpeg)',
10259:'![](_page_839_Figure_4.jpeg)',
10393:'![](_page_847_Figure_1.jpeg)',
10409:'![](_page_848_Figure_2.jpeg)',
11184:'![](_page_883_Picture_32.jpeg)',
11186:'![](_page_883_Picture_33.jpeg)',
11188:'![](_page_883_Picture_34.jpeg)',
11190:'![](_page_883_Picture_35.jpeg)',
11297:'![](_page_885_Picture_21.jpeg)',
11301:'![](_page_885_Picture_23.jpeg)',
11303:'![](_page_885_Picture_24.jpeg)',
11305:'![](_page_885_Picture_25.jpeg)',
11307:'![](_page_885_Picture_26.jpeg)',
14762:'![](_page_979_Figure_4.jpeg)',
14766:'![](_page_979_Picture_6.jpeg)',
14829:'![](_page_980_Picture_15.jpeg)',
14831:'![](_page_980_Picture_16.jpeg)',
14833:'![](_page_980_Picture_17.jpeg)',
13599:'![](_page_943_Picture_21.jpeg)',
13603:'![](_page_944_Picture_3.jpeg)',
13605:'![](_page_944_Picture_4.jpeg)',
13607:'![](_page_944_Picture_5.jpeg)',
13609:'![](_page_944_Picture_6.jpeg)',
13611:'![](_page_944_Picture_7.jpeg)',
13615:'![](_page_944_Picture_9.jpeg)',
13648:'![](_page_945_Picture_2.jpeg)',
13652:'![](_page_945_Picture_4.jpeg)',
13656:'![](_page_945_Picture_6.jpeg)',
15211:'![](_page_994_Picture_3.jpeg)',
15213:'![](_page_994_Picture_4.jpeg)',
15215:'![](_page_994_Picture_5.jpeg)',
15217:'![](_page_994_Picture_6.jpeg)',
15219:'![](_page_994_Picture_7.jpeg)',
15223:'![](_page_994_Picture_9.jpeg)',
15225:'![](_page_994_Picture_10.jpeg)',
15227:'![](_page_994_Picture_11.jpeg)',
15229:'![](_page_994_Picture_12.jpeg)',
15231:'![](_page_994_Picture_13.jpeg)',
15235:'![](_page_994_Picture_15.jpeg)',
15237:'![](_page_994_Picture_16.jpeg)',
15239:'![](_page_994_Picture_17.jpeg)',
15241:'![](_page_994_Picture_18.jpeg)',
15243:'![](_page_994_Picture_19.jpeg)',
15313:'![](_page_996_Picture_6.jpeg)',
15315:'![](_page_996_Picture_7.jpeg)',
15317:'![](_page_996_Picture_8.jpeg)',
15319:'![](_page_996_Picture_9.jpeg)',
17433:'![](_page_1092_Picture_6.jpeg)',
18746:'![](_page_1132_Picture_2.jpeg)',
19236:'![](_page_1152_Figure_5.jpeg)',
19238:'![](_page_1152_Figure_6.jpeg)',
}
assert all(book[n-1]==want for n,want in links.items())

# Reverse join: non-control/non-index textual dispositions govern image links
# at distance two; image-only runs then close transitively. Four prose-declared
# construction bridges seed runs interrupted by code or explanatory text.
stage=Path('goal-1/22-T03-TOTALISTIC-CA.md').read_text()
search=stage.split('### Exact reproducible manifest',1)[1].split('## Book Excerpts',1)[0]
m=re.search(r'\nparts=\{\n(.*?)\n\}\npartition=',search,re.S); assert m
raw_parts=ast.literal_eval('{'+m.group(1)+'}')
def line_set(value):
    return set() if value=='-' else set(map(int,value.split(',')))
partition={name:line_set(value) for name,value in raw_parts.items()}
image_names={n:re.fullmatch(r'!\[\]\(([^)]+)\)',line).group(1)
             for n,line in enumerate(book,1)
             if re.fullmatch(r'!\[\]\([^)]+\)',line)}
image_lines=set(image_names)
positive=set().union(*(partition[name] for name in
    ('three_color','generic_parent','other_totalistic','sibling_application')))
positive-=image_lines

def adjacent_images(anchors):
    return {m for n in anchors for m in (n-2,n+2)
            if m in image_lines and book[(n+m)//2-1].strip()==''}

def close_image_runs(seed):
    result=set(seed)
    while True:
        expanded=result|adjacent_images(result)
        if expanded==result: return result
        result=expanded

assert 'pictures on the next page' in book[3903].lower()
assert 'next page shows the final patterns' in book[5089].lower()
assert 'last 5 steps' in book[11177] and 'GraphicsArray' in book[11179]
assert 'rule illustrated above' in book[15232] and 'pictures below' in book[15232]
bridge_seeds={3908,5092,11182,15235}
reverse_required=close_image_runs(adjacent_images(positive)|bridge_seeds)
repair_delta={2924,3900,3908,3912,5086,5092,5636,10259,11184,11186,
11188,11190,13599,13603,13605,13607,13609,13611,13615,13648,13652,
13656,15211,15213,15215,15217,15219,15223,15225,15227,15229,15231,
15235,15237,15239,15241,15243,15313,15315,15317,15319,17433,19236,19238}
assert len(reverse_required)==104 and len(repair_delta)==44 and repair_delta<=reverse_required

items_src=stage.split('\nitems={',1)[1].split('\n}\n\ndef jpeg_size',1)[0]
ledger_names={Path(path).name for path in re.findall(r"'([^']+\.jpeg)':\(",items_src)}
ledger_lines={n for n,name in image_names.items() if name in ledger_names}
assert len(ledger_names)==len(ledger_lines)==118 and reverse_required<=ledger_lines

# Query-false controls form a separately computed frontier. Twenty-three
# visual siblings remain outside; the five selected members are explicit
# inherited/boundary controls, not accidental gaps in the positive join.
control_required=close_image_runs(adjacent_images(partition['controls']-image_lines))
control_only=control_required-reverse_required
assert len(control_only)==28
assert control_only&ledger_lines=={5220,5484,10393,10409,14766}
assert len(control_only-ledger_lines)==23

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
assert table(20,2,2)==(0,0,1,0,1,0)
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
assert 20 in range(0,64,2) and 52 in range(0,64,2)
for code,k,r in [(1815,3,1),(2007,3,1),(1659,3,1),(2043,3,1),
                 (219,3,1),(438,3,1),(1380,3,1),(1632,3,1),
                 (294,3,1),(1893,3,1),(1004600,4,1)]:
    table(code,k,r)
r1004600=table(1004600,4,1)
assert r1004600==(0,2,3,0,0,1,1,1,3,3)

r420=table(420,3,1)
assert r420==(0,2,1,0,2,1,0)
for a in product(range(3),repeat=3):
    for b in product(range(3),repeat=3):
        ab=tuple((x+y)%3 for x,y in zip(a,b))
        assert r420[sum(ab)]==(r420[sum(a)]+r420[sum(b)])%3

structures357=((28,'48'),(7795,'19'),(1706588,'26'),
               (4803890,'41R'),(154596664,'12'),(514454827,'48L'))
structures1329=((1,'78'),(52,'7'),(400,'2'),(800,'12'),(916,'31R'),
                (2617,'9'),(2669,'48R'),(97357,'2'),(659197,'9'))
growth1329=(54889,97439,166426,115396,2069116)
survival20=((1000,72),(1000000,60171),(1000000000,71079205))
assert structures357[3]==(4803890,'41R') and structures357[-1]==(514454827,'48L')
assert structures1329[4]==(916,'31R') and structures1329[6]==(2669,'48R')
assert len(set(growth1329))==5 and survival20[0]==(1000,72)

print('code777_table=',r777,'display=1001210')
print('code777_t0_t8=',','.join(words))
print('code867_51x101_sha256=',sha256(blob).hexdigest())
print('code20_table=',table(20,2,2),'code52_table=',table(52,2,2))
print('chapter6_structure_labels=',len(structures357)+len(structures1329),
      'growth_labels=',len(growth1329),'audited_links=',len(links))
print('reverse_join_required=',len(reverse_required),'repair_delta=',len(repair_delta),
      'query_false_only_omitted=',len(control_only-ledger_lines))
print('code20_survival=',survival20,'code420_additive_mod3= PASS')
print('code1004600_table=',r1004600,'display=3311100320')
print('pictured_class4_code=1659; borderline_code=1632; notes_only_code=1662')
print('T03 asset semantic oracle: PASS')
PY
```

Recorded output:

```text
code777_table= (0, 1, 2, 1, 0, 0, 1) display=1001210
code777_t0_t8= 1,111,12121,1100011,122101221,11001210011,1221110111221,110001222100011,12210110101101221
code867_51x101_sha256= 185170c0866f76d129fbf3a8843cc731f98b9f012cb98286f01e420532fb53d9
code20_table= (0, 0, 1, 0, 1, 0) code52_table= (0, 0, 1, 0, 1, 1)
chapter6_structure_labels= 15 growth_labels= 5 audited_links= 70
reverse_join_required= 104 repair_delta= 44 query_false_only_omitted= 23
code20_survival= ((1000, 72), (1000000, 60171), (1000000000, 71079205)) code420_additive_mod3= PASS
code1004600_table= (0, 2, 3, 0, 0, 1, 1, 1, 3, 3) display=3311100320
pictured_class4_code=1659; borderline_code=1632; notes_only_code=1662
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

Picture 253/1 is repaired to visible code `1659`: the Actual Index routes 1659 to printed page 238, while monolith `BOOK:2834` contains only the contaminated page number `238`; Notes code `1662` is a distinct unpictured example. Picture 255/5 visibly supplies borderline code `1632`. No other included figure supplies all of exact serialized seed, spatial digit orientation/padding, boundary/background, event-versus-state horizon, spatial crop, palette, and resampling. Consequently the numbered structure searches and remaining galleries have metadata, labels, filters, search bounds, and source-stated properties pinned, but no fabricated pixel or trajectory golden.

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

1. Extend `src/ca/alphabets.py` with an immutable validated numeric color valuation. The canonical constructor maps the declared colors bijectively to `0..k-1`; any symbolic relabeling stores the explicit forward/inverse map. Do not derive it from palette, a host set, incidental array order, or the independent T02 rank. Validate every rule output, seed value, fixed boundary/background value, and gathered read against the valuation domain.
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

1. For validated `k>=2,r>=1`, derive `q=2r+1`, `M=1+(k-1)q`, and `R=k^M`; pin `R(2,1)=16`, `R(3,1)=2187`, `R(2,2)=64`, and `R(5,1)=1,220,703,125`. Reject booleans, invalid `k/r`, malformed valuations, wrong table lengths, out-of-alphabet outputs, out-of-domain seed/boundary/read values, `-1`, and `R`.
2. Prove every sum `0..q(k-1)` reachable for representative `k/r`, and that every permutation of one read multiset gives the same sum/output. Fixed arity, center inclusion, and repeated positions remain inspectable.
3. Use `(0,2,0)` and `(1,0,1)` at `k=3`: both must address sum row `2` despite different histograms. A histogram-keyed implementation must fail this oracle.
4. Declare alphabet order `('red','green','blue')` but valuation `{'red':2,'green':0,'blue':1}`. Pin a context whose valuation-sum differs from rank-sum, all seven code-777 symbolic outputs, execution, and encode/decode round-trip. An implementation that silently substitutes tuple rank must fail.
5. Round-trip structural tables/codes `0`, `1`, `420`, `777`, `867`, `R-1`, all three binary radius-two fixtures `(10,20,52)`, deterministic sampled `k/r` profiles, and a valid `k=8,r=1` code above `2^63-1` through table, tagged decimal string, and JSON-safe records without NumPy/float loss.
6. Pin code 777's least-significant-first outputs as `(0,1,2,1,0,0,1)`. Assert `output(n,s)=floor(n/3^s) mod 3`, source display order is the reverse padded sequence, and color `2` survives execution.
7. Prove code 420 has `U(s)=(-s) mod 3` for `s=0..6`, while remaining a normal structural table plus an additive property claim. No modulo formula may replace arbitrary T03 execution.
8. For `k=2,r=2`, pin the exact low-sum-first tables `10 -> (0,1,0,1,0,0)`, `20 -> (0,0,1,0,1,0)`, and `52 -> (0,0,1,0,1,1)`. Prove code/table/tagged-string construction yields the same ordinary `AggregateLookupRule`, resolved spec, semantic program identity, and executor for all three. This catches a radius-one/seven-row or code-10-only special case; no panel trajectory is a golden.
9. Expand representative aggregate tables to T01/T02 exhaustive tables and compare all local contexts and several exact trajectories. The native T03 record must still serialize as valuation + aggregate + `M` rows, not the expansion.
10. Run code 1 from an all-zero field and prove the entire background evolves; then validate T06 separately as `U(0)=0`, equivalently `code mod k=0`. No seed or finite-support shortcut may assume quiescence.
11. Use binary radius-one code 2 on `[1,0,0]` with explicit fixed exterior: parallel old-snapshot update yields `[1,1,0]`, while left-to-right in-place mutation would yield `[1,1,1]`.
12. Run one structural program with centered, explicit, random, periodic, finite-block-on-constant, and finite-block-on-repeating initial fields and with cycle/segment/causal-window realizations. Program identity stays fixed; run/realization/view identities change. Separately retain code-20 initial-condition/period/search/survival records and code-52 class/universality labels as analyzer/provenance data; none may become a program field, seed, boundary, horizon, or preset default.
13. Assert T04 and T05 presets return the same aggregate-rule/spec types as generic T03; T07 reflection is derived from equal-weight sum; outer, histogram, weighted, threshold, dynamic-arity, and continuous profiles are rejected or routed to their own typed constructions.
14. Inspect the resolved spec/executor: no callback, family branch, partial-row fallback, hidden valuation/seed/background/palette, exhaustive-only identity, binary decoder, float mean, fixed-width rule code, or artificial maximum `k/r`.
15. Preserve the full repository suite, T01/T02 asymmetric/nonbinary tests, scalar/batch parity as regression evidence, and finite trace/export round trips without weakening expectations.

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
- No code-`10`/`20`/`52` dispatch or fixture-only evaluator; all three radius-two examples resolve through the generic six-row codec, aggregate rule, spec, and executor.
- No hidden seed, boundary, horizon, palette, background-freezing, behavior class, search work, RNG, or accumulator in state/execution.
- No T06 quiescence or T07 symmetry flag fused into validation; no additive formula, outer/semi-totalistic center channel, unequal weight, threshold, higher-dimensional, or T44 continuous rule smuggled behind an aggregate option.
- No proof from pixels, symmetric examples, rule zero, scalar/batch self-parity, or T01/T02 exhaustive expansion alone; independent sum/code/nonbinary/background/old-snapshot oracles are mandatory.
- No weakening current tests, retaining parallel semantic paths, or relabeling Dyadrads/Dyadaxes/Lagcounts as T03.

## Completion Requirements

- [x] Every strict/Notes/split/actual-Index/alias/variant/application/emulation textual candidate is dispositioned reproducibly.
- [x] Every currently identified relevant asset and source-permitted oracle is closed with hashes, geometry, repairs, and exclusions.
- [x] Aggregate/value/case/table/code/read/update/successor/boundary/seed semantics and variants are explicit.
- [x] T01/T02/T04/T05/T06/T07/additive/weighted/emulation boundaries and current API/runtime fit are proved.
- [x] Goal 2 files/dependencies/tests and no-cheating gates are implementation-ready.
- [x] Global ledgers, independent review, diff checks, and repository tests are integrated.

## Stage Results

**COMPLETE after the bounded T05 repair and fresh independent review.** The T05 higher-color audit found the direct code-`1004600` Notes continuation at `BOOK:19234` and its two linked 20-million-step fluctuation plots at `BOOK:19236,19238`. T03 already treated code `1004600` as an included four-color totalistic profile, so omitting its named-code continuation invalidated the former 309-candidate/116-asset exhaustive closure even though aggregate semantics were unchanged. Q18 and the two linked plots now close an exact 18-query/312-candidate source manifest, 22 evidence groups with 89 verbatim fragments on 86 source lines, and 118 rasters at `50 included / 60 excluded / 8 relation-only`. All six embedded blocks, independent review, global reintegration, fence/diff checks, and all 102 repository tests pass.

T04's named code-357/code-1329 routes at `BOOK:3320-3378` and binary radius-two code-20 follow-through first exposed omissions in T03's former exhaustive-manifest/superset claim; the subsequent bidirectional audit also found two-dimensional, weighted, Notes-chain, application, and inherited T04 E14 controls. That prior source and physical audit closed 17 queries, 309 dispositioned candidates, 21 evidence groups, 88 verbatim fragments on 85 source lines, five official PDFs, and 116 rasters at `48 included / 60 excluded / 8 relation-only`; those figures are retained only as historical provenance for the now-explicit three-line/two-asset delta.

T03 is one exact finite-sum rule description over the T01/T02 fixed-lattice construction. A program declares finite alphabet `A`, explicit bijection `nu:A->{0,...,k-1}`, fixed radius `r`, exact sum of the `2r+1` old reads, and one complete `M=1+(k-1)(2r+1)`-row structural table. Sum zero is the least-significant base-`k` digit. The source average is the exact label `s/(2r+1)`, not a float. T03 adds neither an executor nor an update law; T04/T05 are presets, T06/T07 restrictions/properties, and histogram, outer, weighted, higher-dimensional, continuous, additive, emulation, seed, class, and view material remains explicitly typed outside base execution.

The repaired asset blocks pass. They cover `50/60/8` disjoint physical dispositions, 70 explicitly followed continuation/boundary links, the 104-link mechanical reverse-join closure, 23 mechanically outside query-false-only siblings, binary radius-two codes `10/20/52`, the exact code-`1004600` table and long-run observer continuation, code-20 survival counts, code-357/code-1329 structure labels, code-420 additivity, exact code-777/code-867 trajectories, and all 946 cells of the strict code-777 raster with zero mismatch. The former 16-query/118-candidate and 17-query/309-candidate exhaustion claims are superseded by the widened 18-query/312-candidate partition; the current broad API and binary/family-dispatched runtime remain documented as mismatches rather than preserved through a shim.

G2-T03 names concrete alphabet, aggregate, table/codec, rule, executor, spec/preset, trace/export, migration, and test work with 15 adversarial conformance obligations, including exact generic radius-two codes `10/20/52`. D115-D118 and the rank-versus-valuation repair remain active. All six embedded blocks and the widened bidirectional source/asset checks pass. Fresh independent review found no content defect after the status/count refresh, and global closure is restored.

## Integration Results

1. No prior assumption or primitive is invalidated. D114 is concretized: T02 rank and T03 numeric valuation are independent identities, while palette remains representation.
2. T03 directly reuses T01/T02 support, `AllSites`, old-snapshot gathering, typed same-site assignment, atomic commit, successor, realization, and trace semantics without changing their meanings.
3. The proposal adds no family branch, callback, flag, hidden state, duplicate executor, fallback, binary decoder, or exhaustive-table masquerade.
4. State remains only support plus the current total color field; the immutable valuation/aggregate/table is program data and all information needed to reproduce a trace is explicit.
5. Support, topology, values, numeric valuation, aggregate cases, structural table, code, run controls, representation, properties, and relations remain separately typed.
6. Equal-weight fixed-arity sum followed by complete lookup is defining rule semantics and remains native. Integer vectorization, exact-average labels, bigint code, exhaustive lowering, solvers, gallery selection, and rasterization remain explicit incidental or relation layers.
7. The proposed encoding preserves alphabet identity, independent `nu`, arity/radius, every sum row including leading zeros, arbitrary-precision code direction, run identity, and observation scope. The noncanonical symbolic fixture prevents rank collapse.
8. T03 was reopened by the T05 code-`1004600` Notes/asset omission and is now reclosed after the widened manifest and fresh independent review passed. T01/T02 and T04 remain completed; the higher-color observer continuation does not alter their native semantics.
9. Goal 2 gains G2-T03 after the shared T01/T02 alphabet/table/executor responsibilities. T04/T05 depend on it as presets; T06/T07 consume predicates/proofs rather than flags; outer/weighted/histogram/higher-dimensional profiles remain separately staged.
10. The overall API becomes simpler: one closed `valuation -> exact sum -> typed table` rule composes with the existing fixed-field executor, replacing the current loose `TOTALISTIC` bucket and binary family routing without adding an eleventh update law.
