# 24-T05-HIGHERCOLOR-TOTALISTIC

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T05, CSV line 6, `Higher-Color Totalistic Cellular Automata`; taxonomy section 5 at `ref/notes/CA-Types.md:126-145` is search vocabulary only, not book evidence.
- The taxonomy hypothesis is a radius-one totalistic profile with four, five, or more values. It claims no new support, read, update, successor, or halt semantics beyond T03; the book audit must prove or revise that grouping.
- The strict five-color comparison states 13 sum cases and `5^13 = 1,220,703,125` possible rules, while a separate Notes/application example names four-color totalistic code `1004600`. The complete audit closes these and every alias, formula, caption, Notes, Index, split, application, control, and linked-asset route at 11 queries, 142 lexical lines, five governed prose continuations, and 25 assets: 172 candidates with zero remainder.
- Canonical values `A_k=(0,...,k-1)`, `nu_k(i)=i`, `r=1`, and explicit “four or more colors” establish exactly the concrete finite range `k>=4`. T03 then gives arity `q=3`, sum domain `0..3(k-1)`, table length `M=3k-2`, and rule count `R=k^(3k-2)`. The general formula derives the otherwise nonliteral `k=4` values `M=10`, `R=4^10`; `k=5` is independently direct.
- T01/T02/T03/T04 already establish fixed ordered support, all-site old-snapshot reads, typed same-site assignment, atomic parallel update, structural table identity, arbitrary-precision tagged code identity, and the preset/restriction/property/run/view boundary. T05 confirms D118: it is the strict canonical higher-color radius-one preset over T03, not a distinct construction.
- The current API/runtime remains semantically incomplete for this profile: `simple_programs.md` and `src/ca/rules.py` conflate exact numeric sums with counts/histograms; spatial rollout is family-dispatched and binary-decoded; batch rule IDs use `numpy.int64`; no current test executes a four-or-more-color totalistic sum table.
- T05 exposed one bounded T03 source-closure omission: code `1004600`'s Notes continuation and two plots. T03 was repaired, independently reviewed, and reclosed at 312 candidates and 118 assets without changing its semantics; T04 remained complete.
- Goal 1 remains evidence/design only. This stage edits only `goal-1/` and does not implement a T05 runtime family.

## Updated Assumptions

- Validated result: T05 is a strict catalog preset/range fixing `r=1`, canonical integer alphabet/valuation, and `k>=4`, then resolving to an ordinary generic T03 program with identical structural identity and executor types.
- A finite `k` is required for every concrete program. “Four, five, or more” does not authorize an unbounded or lazily partial table, wildcard rows, implicit defaults, or fake fixed capacity.
- Structural sum-table identity remains primary. The optional numeric code is an arbitrary-precision relation whose digit count grows with `k`; fixed-width integers, floating values, or JSON numbers cannot define identity.
- Alphabet order, exact numeric valuation, palette, and displayed color names remain distinct. Noncanonical valuations belong to generic T03 unless the source proves them part of T05.
- Rule program, seed/background, finite realization, behavior class, property/proof, gallery selection, raster, and application relation remain separate identities.
- Exhaustive evidence does not contradict D115-D118 or prove a new semantic responsibility. D118 is sharpened with the exact preset boundary; no D119 is needed.

## Big Picture Objective

Determine the exact higher-color totalistic parameter domain and evidence bundle, prove whether it is only a strict T03 preset/range, and produce the smallest implementation-ready Goal 2 constructor and conformance plan without a higher-color executor or fixed-width shortcut.

## Catalog Identity

- Stable ID: T05.
- Exact CSV name: `Higher-Color Totalistic Cellular Automata` at `ref/notes/CA-Types.csv:6`.
- Taxonomy section: 5, vocabulary seed only.
- Entry hypothesis: parameter-range preset/profile over T03, presently expected to fix radius one, canonical valuation, and `k>=4`.
- Initial vocabulary: higher-color/higher colour, more colors, four-color/4-color, five-color/5-color, four/five possible colors, `k=4`, `k=5`, `r=1`, 10 cases, 13 cases, `4^10`, `5^13`, `1,048,576`, `1,220,703,125`, code `1004600`, totalistic, average color, assignment of values to colors, rule complexity, dying out/undecidability, class behavior, and related non-totalistic color-count controls.

## Search Log

Closed with zero remainder. `BOOK` below means the canonical monolith at `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`; its actual Index begins at physical line 20826. Eleven controlled query families produce exactly 142 distinct lexical candidates: 127 before the actual Index and 15 in it. Their disjoint lexical disposition is `4 native / 14 generic-parent / 23 lower-color totalistic / 33 other-totalistic / 14 higher-color relations / 39 controls / 15 Index`. Five governed prose continuations and 25 linked rasters expand this to exactly 172 candidates, with full disposition `11 / 16 / 23 / 33 / 27 / 47 / 15` and assets `5 included / 13 relation-only / 7 excluded`.

The literal absences are part of the result: contextual searches find no occurrence of the catalog phrase `higher-color`, `10 cases`, `4^10`, or `5^13`. The `k=4` values `M=10` and `R=4^10` are derived from the general formula at `BOOK:11897`; `k=5`, 13 cases, and `1,220,703,125` are direct at `BOOK:1282`. Numeric collisions at `BOOK:3034,8356` are controls. Code `1004600` occurs exactly at `BOOK:9166,19234,20980`; application prose continues at `9168,9170`, and the Notes link plots at `19236,19238`.

| Q | Controlled family | Pre-Index | Actual Index |
|---:|---|---:|---:|
| 01 | four/4-color spellings | 26 | 4 |
| 02 | five/5-color spellings | 8 | 0 |
| 03 | more/higher/four-or-more colors | 13 | 2 |
| 04 | any-number/increasing-number color phrases | 5 | 0 |
| 05 | literal `totalistic` saturation | 74 | 10 |
| 06 | 10/13 cases and `4^10`/`5^13` numeric forms | 3 | 0 |
| 07 | named code `1004600` | 2 | 1 |
| 08 | average/implementation/value-assignment/general-count aliases | 10 | 0 |
| 09 | explicit `k=4/5, r=1` adjacency | 3 | 0 |
| 10 | complexity/class/death/growth property phrases | 4 | 0 |
| 11 | heading/Index drift guard | 11 | 6 |

Q11 adds no new line to the union. The full 172-candidate closure overlaps T03 on 114 lines and T04 on 107; T05 therefore contributes respectively 58 and 65 independently found candidates beyond those inherited manifests. Neither prior stage can stand in for this stage's closure.

### Exact reproducible source and split manifest

```bash
python3 - <<'PY'
import re
from pathlib import Path

B=Path('ref/A-New-Kind-of-Science')
P=B/'A-New-Kind-of-Science.md'
L=P.read_text().splitlines(); IX=20826
def xs(s): return [] if s=='-' else list(map(int,s.split(',')))
rows=[
(r'(?i)(?<![a-z0-9])(?:four|4)[ -]?(?:possible[ -]?)?colou?rs?(?![a-z0-9])',
 '1042,1046,2868,3946,7930,8490,8494,8530,8532,9166,9508,10395,10397,10399,14099,14388,15311,16294,16483,16489,16646,17473,18361,18670,18755,19794',
 '20828,21193,21815,21990'),
(r'(?i)(?<![a-z0-9])(?:five|5)[ -]?(?:possible[ -]?)?colou?rs?(?![a-z0-9])',
 '1282,7986,8278,8504,8510,8520,8526,8558','-'),
(r'(?i)(?:more than (?:two|three)|(?:four|4) or more|more|higher)[ -](?:possible[ -])?colou?rs',
 '1282,7900,8072,8318,11283,12055,12311,12313,13619,15245,18339,18592,18755',
 '20965,22372'),
(r'(?i)(?:any number of colou?rs|any set of rules.{0,100}how many colou?rs|number of colou?rs increases)',
 '1282,7902,8080,18806,19322','-'),
(r'(?i)totalistic',
 '772,774,776,784,790,796,800,804,808,824,834,846,1282,1954,2170,2802,2806,2822,2852,2868,2922,3902,3914,5638,6340,6644,7912,8320,8936,9166,10261,11037,11056,11060,11068,11070,11072,11168,11178,11509,11585,11625,11897,11902,11904,11908,11910,11912,11916,13536,13538,13547,13548,13549,13601,13613,13650,13654,13658,14223,14224,14239,14241,14632,15221,15301,15321,15359,15955,15959,16024,17431,18672,18748',
 '20965,20969,20972,20980,21233,21731,22030,22146,22352,22392'),
(r'(?i)(?:10 cases|13 cases|4\s*\^\s*10|5\s*\^\s*13|1,?048,?576|1,?220,?703,?125)',
 '1282,3034,8356','-'),
(r'(?i)(?:code(?: number)?\s*1004,?600|1004,?600)',
 '9166,19234','20980'),
(r'(?i)(?:average (?:color|of (?:the previous colors|cells in its neighborhood))|TotalisticCARule|ToTotalisticCARule|specific assignment of values to colors|k\^\{1\+\(k-1\)\(2r\+1\)\})',
 '774,776,2170,5082,5088,8320,11897,11904,11908,11912','-'),
(r'(?i)k\s*=\s*(?:4|5).{0,100}?r\s*=\s*1(?![0-9/])',
 '14394,16024,16049','-'),
(r'(?i)(?:rules of varying complexity|transitions between rules with different classes of behavior|dies out after 36 steps|steady growth at about 0\.035)',
 '1282,2868,9166,19234','-'),
(r'(?i)(?:Cellular automata.{0,100}with more colors|emulating more colors|Code 1004600|Sum \(totalistic\) rules|Totalistic cellular automata)',
 '784,808,834,2802,2806,9166,11037,11902,14224,18748,19234',
 '20969,20980,22146,22352,22372,22392'),
]
query_sets=[]
for q,(pat,pre_s,idx_s) in enumerate(rows,1):
    found=[i for i,s in enumerate(L,1) if re.search(pat,s)]
    pre=[i for i in found if i<IX]; idx=[i for i in found if i>=IX]
    assert pre==xs(pre_s),(q,pre,xs(pre_s))
    assert idx==xs(idx_s),(q,idx,xs(idx_s))
    query_sets.append(set(found))
lex=set().union(*query_sets)
assert len(lex)==142 and len({i for i in lex if i<IX})==127

native= set(xs('1282,2868,9166,19234'))
parent= set(xs('772,774,776,8320,11037,11056,11060,11897,11902,11904,11908,11910,11912,11916'))
lower=  set(xs('784,790,796,800,804,808,824,834,846,2802,2806,2822,2852,6340,7912,8936,11168,11509,11585,11625,14223,14632,18672'))
other=  set(xs('1954,2170,2922,3902,3914,5082,5088,5638,6644,10261,11068,11070,11072,11178,13536,13538,13547,13548,13549,13601,13613,13650,13654,13658,14239,14241,15221,15301,15321,15359,15955,15959,17431'))
relation=set(xs('7900,7902,7930,7986,8318,11283,14224,14388,14394,16024,18361,18670,18748,18755'))
control=set(xs('1042,1046,3034,3946,8072,8080,8278,8356,8490,8494,8504,8510,8520,8526,8530,8532,8558,9508,10395,10397,10399,12055,12311,12313,13619,14099,15245,15311,16049,16294,16483,16489,16646,17473,18339,18592,18806,19322,19794'))
index=set(xs('20828,20965,20969,20972,20980,21193,21233,21731,21815,21990,22030,22146,22352,22372,22392'))
roles=[native,parent,lower,other,relation,control,index]
assert [len(x) for x in roles]==[4,14,23,33,14,39,15]
assert set().union(*roles)==lex and sum(map(len,roles))==len(lex)

follow={9168,9170,10411,11077,11914}
I={1280,2866,9164,19236,19238}
R={778,7928,7932,7934,7984,11170,11297,14226,14228,14230,14232,14390,18759}
X={3944,10393,10409,15313,15315,15317,15319}
asset_names={
778:'_page_75_Figure_6.jpeg',1280:'_page_122_Figure_2.jpeg',2866:'_page_256_Figure_2.jpeg',
3944:'_page_354_Picture_2.jpeg',7928:'_page_672_Picture_1.jpeg',7932:'_page_672_Picture_3.jpeg',
7934:'_page_672_Picture_4.jpeg',7984:'_page_677_Figure_2.jpeg',9164:'_page_769_Figure_1.jpeg',
10393:'_page_847_Figure_1.jpeg',10409:'_page_848_Figure_2.jpeg',11170:'_page_883_Picture_25.jpeg',
11297:'_page_885_Picture_21.jpeg',14390:'_page_967_Picture_22.jpeg',15313:'_page_996_Picture_6.jpeg',
14226:'_page_963_Picture_8.jpeg',14228:'_page_963_Picture_9.jpeg',
14230:'_page_963_Picture_10.jpeg',14232:'_page_963_Picture_11.jpeg',
15315:'_page_996_Picture_7.jpeg',15317:'_page_996_Picture_8.jpeg',15319:'_page_996_Picture_9.jpeg',
18759:'_page_1132_Figure_9.jpeg',19236:'_page_1152_Figure_5.jpeg',19238:'_page_1152_Figure_6.jpeg'}
assets=I|R|X
assert [len(I),len(R),len(X)]==[5,13,7] and assets==set(asset_names)
for n,name in asset_names.items(): assert L[n-1].strip()==f'![]({name})',(n,L[n-1])
assert not (lex&follow or lex&assets or follow&assets)
expanded=lex|follow|assets
full=[native|{9168,9170}|I,parent|{11077,11914},lower,other,relation|R,control|{10411}|X,index]
assert [len(x) for x in full]==[11,16,23,33,27,47,15]
assert set().union(*full)==expanded and sum(map(len,full))==len(expanded)==172

split_expected={
'BACK-MATTER/Colophon/Colophon.md':'30,896,918,1149,1227,1229,1305,1312,1363,1791,1879,2351,3385,3522,3526,3529,3537,3750,3790,4288,4372,4547,4587,4703,4909,4929,4949',
'BACK-MATTER/Index/Index.md':'216,218,1437,1439,1448,1449,1450,1502,1514,1520,1551,1555,1559,2000,2124,2125,2140,2142,2289,2295,2533,3122,3146,3202,3212,3222,3260,3856,3860,3925,3950,4195,4384,4390,4547,5334',
'CHAPTERS/10-Processes-of-Perception-and-Analysis/Processes-of-Perception-and-Analysis.md':'57',
'CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md':'199,201,211,229,285,361,367,563,601,603,633,765,769,779,781,789,795,799,801,825',
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md':'319,549,891,1642,1776,1778,1780,2418,2437,2441,2449,2451,2453,2549,2559,2664,2890,2966,3006,3278,3283,3285,3289,3291,3293,3297,3436',
'CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md':'89,91,93,101,107,113,117,121,125,141,151,163,359,363,599',
'CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md':'411',
'CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md':'27',
'CHAPTERS/6-Starting-from-Randomness/Starting-from-Randomness.md':'101,105,121,149,165,219,331',
'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Mechanisms-in-Programs-and-Nature.md':'479,491,523',
'CHAPTERS/8-Implications-for-Everyday-Systems/Implications-for-Everyday-Systems.md':'719,725',
'CHAPTERS/9-Fundamental-Physics/Fundamental-Physics.md':'473,1169',
}
expected={(rel,n) for rel,ns in split_expected.items() for n in xs(ns)}
found=set()
for p in B.rglob('*.md'):
    rel=str(p.relative_to(B))
    if rel in {'A-New-Kind-of-Science.md','ANKoS-Atlas.md'}: continue
    for n,line in enumerate(p.read_text().splitlines(),1):
        if any(re.search(pat,line) for pat,_,_ in rows): found.add((rel,n))
assert found==expected,(len(found),len(expected),sorted(found^expected)[:10])
assert len(found)==142
print('T05 source manifest: PASS',len(rows),'queries;',len(lex),'lexical;',len(follow),'text follow;',len(assets),'assets;',len(expanded),'total')
print('lexical partition=',*[len(x) for x in roles],'; full partition=',*[len(x) for x in full])
print('assets=',len(I),len(R),len(X),'; split=',len(found))
PY
```

Recorded output:

```text
T05 source manifest: PASS 11 queries; 142 lexical; 5 text follow; 25 assets; 172 total
lexical partition= 4 14 23 33 14 39 15 ; full partition= 11 16 23 33 27 47 15
assets= 5 13 7 ; split= 142
```

## Book Excerpts

Twelve groups retain 47 provenance lines and 47 verbatim fragments on 40 unique canonical source lines. Seven linked/navigation lines are provenance rather than quote lines. The full 172-candidate disposition remains in the executable Search Log; these excerpts retain the construction, parameter, property, and boundary facts needed for the design.

### E1 — Inherited totalistic restriction, valuation, and code order

- Provenance: `BOOK:772,774,776,11037,11056,11060,11077`.
- Establishes: totalistic rules quotient ordered neighborhoods by an exact average/sum; the strict example includes left, self, and right; values `0,1,2` and least-significant sum-zero order are explicit. The built-in convention corroborates integer values `0..k-1` but does not make palette names semantic.

> The 256 "elementary" rules that we have discussed so far are by most measures the simplest possible—and were the first ones I studied. But one can for example also look at rules that involve three colors, rather than two, so that cells can not only be black and white, but also gray. The total number of possible rules of this kind turns out to be immense—7,625,597,484,987 in all—but by considering only so-called "totalistic" ones, the number becomes much more manageable.

> The idea of a totalistic rule is to take the new color of each cell to depend only on the average color of neighboring cells, and not on their individual colors. The picture below shows one example of how this works. And with three possible colors for each cell, there are 2187 possible totalistic rules, each of which can conveniently be identified by a code number as illustrated in the picture. The facing page shows a representative sequence of such rules.

> Example of a totalistic cellular automaton with three possible colors for each cell. The rule is set up so that the new color of every cell is determined by the average of the previous colors of the cell and its immediate neighbors. With 0 representing white, 1 gray and 2 black, the rightmost element of the rule gives the result for average color 0, while the element immediately to its left gives the result for average color 1/3—and so on. Interpreting the sequence of new colors as a sequence of base 3 digits, one can assign a code number to each totalistic rule.

> \{n, \{k, 1\}\} k-color nearest-neighbor totalistic rule

> \{n, \{k, 1\}, r\} k-color range r totalistic rule

> • Normally, all elements in init and the evolution list are integers between 0 and k-1. • But when a general function is used, the elements of init and the evolution list do not have to be integers. • The second argument passed to fun is the step number, starting at 0. • Initial conditions are constructed from init as follows:

### E2 — Strict higher-color comparison

- Provenance: `BOOK:1282`; linked plate `BOOK:1280`.
- Establishes: five colors directly require 13 cases and admit `1,220,703,125` rules; “four or more colors” is explicit source vocabulary. The caption's complexity observations are behavior properties. `k=4` having 10 cases and `4^10` rules is derived later, not literal here.
- Asset fact: the plate labels eight `k=4` codes `107395..107402` and eight `k=5` codes `180197741..180197748`; these are gallery selections, not defaults.

> Examples of cellular automata with rules of varying complexity. The rules used are of the so-called totalistic type described on page 60. With two possible colors, just 4 cases need to be specified in such rules, and there are 16 possible rules in all. But as the number of colors increases, the rules rapidly become more complex. With three colors, there are 7 cases to be specified, and 2187 possible rules; with five colors, there are 13 cases to be specified, and 1,220,703,125 possible rules. But even though the underlying rules increase rapidly in complexity, the overall forms of behavior that we see do not change much. With two colors, it turns out that no totalistic rules yield anything other than repetitive or nested behavior. But as soon as three colors are allowed, much more complex behavior is immediately possible. Allowing four or more colors, however, does not further increase the complexity of the behavior, and, as the picture shows, even with five colors, simple repetitive and nested behavior can still occur.

### E3 — Direct four-color radius-one profile

- Provenance: `BOOK:2868`; linked plate `BOOK:2866`.
- Establishes: four colors and nearest neighbors directly identify `k=4,r=1`. Class transitions are gallery/property annotations, not rule state or execution semantics.
- Asset fact: the plate supplies 32 codes `1000816,1000820,...,1000940`; the selected sequence does not define all T05 rules.

> A sequence of totalistic rules involving nearest neighbors and four possible colors for each cell chosen to show transitions between rules with different classes of behavior. Note that class 4 seems to occur between class 2 and class 3.

### E4 — Code `1004600` identity versus run properties

- Provenance: `BOOK:9166,9168,9170`; linked plate `BOOK:9164`.
- Establishes: code `1004600` is directly a four-color totalistic program. Death times, widths, survival horizons, initial patterns, and undecidability are run/property evidence; they do not create a halt instruction or alter the successor rule.

> Cellular automaton evolution illustrating the phenomenon of undecidability. Pattern (a) dies out after 36 steps; pattern (b) takes 1017 steps. But what the final outcome in cases (c) and (d) will be is not clear after even a million steps. And in general there appears to be no finite computation that can guarantee to determine the final outcome of the evolution after an infinite number of steps. The cellular automaton rule used is a 4-color totalistic one with code 1004600. Whether a pattern in a cellular automaton ever dies out can be viewed as analogous to a version of the halting problem for Turing machines.

> dies out. But already in example (b) it is not so easy. One can go for 1000 steps and still not know what is going to happen. And only after 1017 steps does it finally become clear that the pattern in fact dies out.

> So what about examples (c) and (d)? What happens to these? After a million steps neither has died out; in fact they are respectively 31,000 and 39,718 cells wide. And after 10 million steps both are still going, now 339,028 and 390,023 cells wide. But even having traced the evolution this far, one still has no idea what its final outcome will be.

### E5 — “More colors” rule-90 relation

- Provenance: `BOOK:11283`; linked relation-only asset `BOOK:11297`.
- Establishes: the source also uses “more colors” for generalizations of rule 90. This is a relation route, not evidence that every higher-color CA is T05 or that T05 changes its inherited three-site totalistic construction.

> ■ More colors. The pictures below show generalizations of rule 90 to k possible colors using the rule

### E6 — General count and value-assignment requirement

- Provenance: `BOOK:11897`.
- Establishes: totalistic rule count is `k^(1+(k-1)(2r+1))`; for `r=1`, this derives `M=3k-2`. Thus `k=4` gives 10 cases and `4^10=1,048,576`, while `k=5` independently reproduces the direct count in E2. For `k>2`, totalistic identity depends on a specific value assignment.
- Boundary: neither `10 cases`, `4^10`, nor `1,048,576` appears literally as a T05 count in the book; all are exact substitutions into this formula.

> - **Page 60 · Numbers of rules.** Allowing k possible colors for each cell and considering r neighbors on each side, there are  $k^{k^{2r+1}}$  possible cellular automaton rules in all, of which  $k^{1/2}k^{r+1}$  are symmetric, and  $k^{1+(k-1)(2r+1)}$  are totalistic. (For k=2, r=1 there are therefore 256 possible rules altogether, of which 16 are totalistic. For k=2, r=2 there are 4,294,967,296 rules in all, of which 64 are totalistic. And for k=3, r=1 there are 7,625,597,484,987 rules in all, with 2187 totalistic ones.) Note that for k>2, a particular rule will in general be totalistic only for a specific assignment of values to colors. I first introduced totalistic rules in 1983.

### E7 — Direct sum lookup and padded base-`k` codec

- Provenance: `BOOK:11902,11904,11908,11910,11912`.
- Establishes: radius one sums left, self, and right; general radius sums offsets `-r..r`; the structural list has exactly `1+(k-1)(2r+1)` digits. Negative indexing plus E1's displayed order makes sum zero the least-significant code digit.
- Boundary: `RotateLeft` supplies a finite cyclic implementation example, not a mandatory native boundary condition.

> ■ Implementation of totalistic cellular automata. To handle totalistic rules that involve *k* colors and nearest neighbors, one can add the definition

> CAStep[TotalisticCARule[rule\_List, 1], a\_List] := rule[[-1 - (RotateLeft[a] + a + RotateRight[a])]]

> CAStep[TotalisticCARule[rule\_List, r\_Integer], a\_List] := rule[[-1 - Sum[RotateLeft[a, i], {i, -r, r}]]]

> One can generate the representation of totalistic rules used by these functions from code numbers using

>  $ToTotalisticCARule[num\_Integer, k\_Integer, r\_Integer] := TotalisticCARule[IntegerDigits[num, k, 1 + (k - 1)(2r + 1)], r]$

### E8 — Shared execution framework

- Provenance: `BOOK:11914,11916`.
- Establishes: ordinary and totalistic rules use one framework with different weight vectors. Higher color does not justify a new executor.
- Repair boundary: `BOOK:11916` contains the known OCR substitution `\wedge` for exponentiation; the all-one totalistic weight vector is intact.

> ■ Common framework. The *Mathematica* built-in function *CellularAutomaton* discussed on page 867 handles general and

> totalistic rules in the same framework by using ListConvolve[w, a, r+1] and taking the weights w to be respectively  $k \wedge Table[i-1, \{i, 2r+1\}]$  and  $Table[1, \{2r+1\}]$ .

### E9 — Higher-color class and property boundary

- Provenance: `BOOK:8318,8320,14224`.
- Establishes: allowing more than two colors supplies further class-4 examples, and totalistic rules are sufficient for such examples. Class frequencies remain analyzer/property evidence rather than construction fields, preset defaults, or executor state.

> Among the 256 so-called elementary cellular automata that allow only two possible colors for each cell and depend only on nearest neighbors, the only clear immediate example is rule 110—together with rules 124, 137 and 193 obtained by trivially reversing left and right or black and white. But as soon as one allows more than two possible colors, or allows dependence on more than just nearest neighbors, one immediately finds all sorts of further examples of class 4 behavior.

> In fact, as illustrated in the pictures on the facing page, it is sufficient in such cases just to use so-called totalistic rules in which the new color of a cell depends only on the average color of cells in its neighborhood, and not on their individual colors.

> - **Frequencies of classes.** The pie charts below show results for 1D totalistic cellular automata with *k* colors and range *r*. Class 3 tends to become more common as the number of elements in the rule increases because as soon as any of these elements yield class 3 behavior, that behavior dominates the system.

### E10 — Reversibility boundary

- Provenance: `BOOK:16024`.
- Establishes: the `k=4,r=1` reversible-rule clause concerns the unrestricted CA space; the final sentence says no nontrivial totalistic rule is reversible. The first clause must not be misclassified as a T05 example.

> - **Numbers of reversible rules.** For k = 2, r = 1, there are 6 reversible rules, as shown on page 436. For k = 2, r = 2 there are 62 reversible rules, in 20 families inequivalent under symmetries, out of a total of  $2^{32}$  or about 4 billion possible rules. For k = 3, r = 1 there are 1800 reversible rules, in 172 families. For k = 4, r = 1, some of the reversible rules can be constructed from the second-order cellular automata below. Note that for any k and r, no non-trivial totalistic rule can ever be reversible.

### E11 — Code-`1004600` Notes continuation

- Provenance: `BOOK:19234`; linked plots `BOOK:19236,19238`.
- Establishes: the Notes extend observations only through at least 20 million steps. Growth rates, non-white density, and fluctuations are observer/property data; they prove neither eventual survival nor a native stopping condition.

> - Page 755 · Code 1004600. In cases (c) and (d) steady growth at about 0.035 and 0.039 cells per step (of which 28% on average are non-white) is seen up to at least 20 million steps, though there continue to be fluctuations as shown below.

### E12 — Complete actual-Index routing

- Provenance: `BOOK:20828,20965,20969,20972,20980,21193,21233,21731,21815,21990,22030,22146,22352,22372,22392`.
- Establishes: all 15 actual-Index candidates are retained. They route to strict totalistic definitions, higher-color comparison, implementation, code `1004600`, reversibility, universality, sibling totalistic families, or explicit lexical controls. They add no transition semantics.
- OCR boundary: the actual Index is column-interleaved. Each blockquote is an exact fragment of its cited physical line, not a reconstructed sentence.

> 4-color theorem see Four-Color Theorem

> implementation of totalistic, 886

> with more colors, 107

> totalistic see Totalistic cellular automata

> weighted totalistic, 427

> in 3-color totalistic CAs, 948

> Code 1004600

> and undecidability, 754, 1137

> Code 294 for totalistic CAs, 60

> Five-neighbor rules (in CAs), 927

> Growth totalistic rules, 928

> Outer totalistic rules

> rosettes in 4-color, 1078

> in four-color printing, 1078

> growth totalistic, 928

> totalistic, 60

> Sum (totalistic) rules, 60

> Totalistic cellular automata, 60

> implementation of, 886

> as not reversible, 1017

> emulating more colors, 669, 1113,

> in totalistic cellular automata, 693

## Source Repairs and Evidence Oracle

- The canonical monolith omits `Images/` in its bare JPEG links; the split documents route those same references to the physical image files. They are one asset each, not duplicates.
- `BOOK:11037` is truncated in both the monolith and split after `higher-dimensional cellular automata on`; the audited official Notes source completes the navigation route with `page 927.` This is navigation evidence only and adds no T05 mechanics.
- `BOOK:11916` carries the OCR token `k \wedge Table[...]` where the general-rule weight vector requires exponentiation. T05 preserves the literal quote and uses the independently stated count/codec formulas at `BOOK:11897,11912`; the intact all-one totalistic vector is the only T05-relevant half of that sentence.
- `BOOK:20980` is interleaved printed-Index text. Only the exact routed fragments are used; column neighbors are not reconstructed into a false sentence.
- The page-122/page-256 code labels are visually recoverable from hash-pinned plates. The plates do not fully serialize seeds, horizons, crop, or palette, so they authorize label/table corpora but no invented cell trajectory.
- Split routing is navigation evidence. `BACK-MATTER/Index/Index.md` contains Notes material while the printed actual Index begins inside `BACK-MATTER/Colophon/Colophon.md`; canonical `BOOK` physical lines remain primary.

```bash
python3 - <<'PY'
import re
from pathlib import Path

book=Path('ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md').read_text().splitlines()
stage=Path('goal-1/24-T05-HIGHERCOLOR-TOTALISTIC.md').read_text().splitlines()
quotes=[line[2:] for line in stage if line.startswith('> ')]
quote_lines=(
    772,774,776,11056,11060,11077,
    1282,
    2868,
    9166,9168,9170,
    11283,
    11897,
    11902,11904,11908,11910,11912,
    11914,11916,
    8318,8320,14224,
    16024,
    19234,
    20828,
    20965,20965,
    20969,20969,
    20972,
    20980,20980,20980,
    21193,21233,21731,21815,21990,
    22030,22030,
    22146,
    22352,22352,22352,
    22372,22392,
)
expected_provenance={
    772,774,776,1280,1282,2866,2868,8318,8320,
    9164,9166,9168,9170,
    11037,11056,11060,11077,
    11283,11297,
    11897,11902,11904,11908,11910,11912,11914,11916,
    14224,16024,
    19234,19236,19238,
    20828,20965,20969,20972,20980,21193,21233,21731,
    21815,21990,22030,22146,22352,22372,22392,
}
provenance_only={1280,2866,9164,11037,11297,19236,19238}
provenance=set()
for line in stage:
    if line.startswith('- Provenance:'):
        for body in re.findall(r'`BOOK:([^`]+)`',line):
            provenance.update(map(int,re.findall(r'\d+',body)))
groups=[line for line in stage if re.match(r'^### E\d+ —',line)]
assert len(groups)==12
assert len(expected_provenance)==47
assert len(quotes)==len(quote_lines)==47
assert len(set(quote_lines))==40
assert set(quote_lines)==expected_provenance-provenance_only
assert provenance==expected_provenance
assert provenance.isdisjoint({14226,14228,14230,14232})
for fragment,n in zip(quotes,quote_lines):
    assert fragment.strip() in book[n-1].strip(),(n,fragment)

assert 'k \\wedge Table' in book[11916-1]
assert 'k^{1+(k-1)(2r+1)}' in book[11897-1]
assert 'IntegerDigits[num, k, 1 + (k - 1)(2r + 1)]' in book[11912-1]
assert all(token not in '\n'.join(book).lower() for token in ('higher-color','10 cases','4^10','5^13'))
assert [i for i,s in enumerate(book,1) if re.search(r'(?i)1004,?600',s)]==[9166,19234,20980]

split_checks={
'CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md':{599:'five colors'},
'CHAPTERS/6-Starting-from-Randomness/Starting-from-Randomness.md':{165:'four possible colors'},
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md':{
549:'code 1004600',551:'1017 steps',553:'10 million steps',2458:'integers between 0 and k-1',
3278:'specific assignment of values to colors',3283:'Implementation of totalistic cellular automata',
3285:'RotateLeft[a] + a + RotateRight[a]',3289:'Sum[RotateLeft[a, i]',3293:'IntegerDigits[num, k',
3295:'Common framework',3297:r'Table[1, \{2r+1\}]'},
'BACK-MATTER/Index/Index.md':{3925:'no non-trivial totalistic rule'},
'BACK-MATTER/Colophon/Colophon.md':{1791:'Code 1004600',3522:'with more colors',3537:'Code 1004600',4909:'Totalistic cellular automata'},
}
root=Path('ref/A-New-Kind-of-Science')
for rel,checks in split_checks.items():
    lines=(root/rel).read_text().splitlines()
    for n,fragment in checks.items(): assert fragment in lines[n-1],(rel,n,fragment)

print('T05 evidence oracle: PASS groups=',len(groups),'provenance=',len(provenance),'fragments=',len(quotes),'quote_lines=',len(set(quote_lines)))
print('source_repairs=4 split_checks=',sum(map(len,split_checks.values())))
PY
```

Recorded output:

```text
T05 evidence oracle: PASS groups= 12 provenance= 47 fragments= 47 quote_lines= 40
source_repairs=4 split_checks= 18
```

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

D115-D118 suffice: the construction is the same equal-weight sum quotient and complete structural table over the same assignment executor. D118 is sharpened with the exact `k>=4,r=1,A_k,nu_k` preset boundary; no D119 or new update law is justified.

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

## Asset and Raster Audit

The closed bidirectional join contains 25 unique physical JPEGs: five direct T05 assets, thirteen relation-only assets, and seven excluded controls. The canonical monolith omits the Images/ directory component; each split link resolves to the single physical file pinned below. Basenames and digests are unique.

| Disposition | Canonical link lines | Governed role |
|---|---|---|
| Included (5) | BOOK:1280,2866,9164,19236,19238 | Page-122 four/five-color labels; page-256 four-color labels/classes; code-1004600 finite-run and 20-million-step property plots |
| Relation-only (13) | BOOK:778,7928,7932,7934,7984,11170,11297,14226,14228,14230,14232,14390,18759 | Generic/lower code order, emulations, additive and class-frequency profiles, commutative-monoid relation, and WireWorld application |
| Excluded controls (7) | BOOK:3944,10393,10409,15313,15315,15317,15319 | Unrestricted four/higher-color rules, input-doubling comparators, and a non-totalistic phase-transition run |

The four page-963 class-frequency charts are included relation-only because BOOK:14224 explicitly says “pie charts below.” Their visible labels are lower/generic comparators, but silently dropping their direct image run would invalidate linked-asset exhaustion.

### Exact metadata and routing oracle

~~~bash
python3 - <<'PY'
from hashlib import sha256
from pathlib import Path

ROOT=Path('ref/A-New-Kind-of-Science')
book=(ROOT/'A-New-Kind-of-Science.md').read_text().splitlines()

# relative path: (bytes,width,height,sha256,disposition)
items={
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_75_Figure_6.jpeg':(51178,610,446,'acb13963632286960ca61b616ff2f45a940750f3ab7deb5e6fbf696543015c15','R'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_122_Figure_2.jpeg':(186914,1098,1164,'ccd7a43a495d01a22300c4b9abbb3ff1b13a3ef37389e77ca491ec805cbaa822','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_256_Figure_2.jpeg':(328297,1092,1367,'1c4967f6967d8e813b2a281e2615dc8bef272eb57789b60e23c950de5e6bc01f','I'),
'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_354_Picture_2.jpeg':(81505,1179,678,'81ebd51ac98816c63105d46e9cf279dd4450ace2dc1acd9261d87a0a20510695','X'),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_672_Picture_1.jpeg':(52915,487,481,'7eaddca4f7e868881728f3ca94f5c6818daaaca2f8ebc2b34d7f5886cdc59813','R'),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_672_Picture_3.jpeg':(6676,463,50,'9a6eeba3b31aa9d265993d036bea9f1febef1427a989f7a4154438300393ee39','R'),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_672_Picture_4.jpeg':(13036,1071,35,'91b2a78cc9bfc00cdef4408a8db23ed252b5aae4e3cfd34eebfa5341bc50fcd2','R'),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_677_Figure_2.jpeg':(173594,1033,1034,'8a59e423d080cdcfd5fbeb61170c099dc6ec904702e27385627427d56373f543','R'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_769_Figure_1.jpeg':(298516,1065,1308,'a980effe214906d991e8ca9180cb9f9d6eade2f978a8358487a60bb1728058f3','I'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_847_Figure_1.jpeg':(111064,1041,385,'2d36e7eaeb3b073e68621ef5f9c1c397ae24ddc74fe06f26e62546ccc3af2902','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_848_Figure_2.jpeg':(247033,1194,1308,'0bfecfeff1bd81072838e39704fc6572632dee083f91ddc4370909b0e2c5b5dd','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_25.jpeg':(5511,211,117,'d53637ce9ec50330d5fa6239b23f48d57b563266a0085a23517d4538020fd5fb','R'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_21.jpeg':(25918,583,225,'5f829c7776b53963e578df5a783553320da171c4e1c4d92c470899ec5bb3e40d','R'),
'BACK-MATTER/Index/Images/_page_963_Picture_8.jpeg':(3114,144,152,'1fb4f0b4c03d8ba9f9fdeb67a0bbda2d786ed7ceeb13cdd8c31337ccd54bcdfb','R'),
'BACK-MATTER/Index/Images/_page_963_Picture_9.jpeg':(3226,136,148,'515f5de1423a9164ed6def92d786346f64c15a0a87ba07b723c069e62829caf6','R'),
'BACK-MATTER/Index/Images/_page_963_Picture_10.jpeg':(3654,138,158,'4b5ff621a668c5b706cdec0481cf3849facb7395d256dfd7c39b471d95fd018f','R'),
'BACK-MATTER/Index/Images/_page_963_Picture_11.jpeg':(3717,136,152,'7c660bbbb03b2d3116aab32cd50a5a3ff094961d49b403148531b36759335d6b','R'),
'BACK-MATTER/Index/Images/_page_967_Picture_22.jpeg':(9241,572,91,'c0819ec54636ca9e86d45baddd00ac0036c844c36d91461512997f53d9658742','R'),
'BACK-MATTER/Index/Images/_page_996_Picture_6.jpeg':(9894,138,266,'b6d70c3a060261bb96c276ef158fd7bf7a3c1706b1003f5ab48621760baa299f','X'),
'BACK-MATTER/Index/Images/_page_996_Picture_7.jpeg':(8413,131,266,'3d14c1bbb64711d9de00fdec771f592203daee10845daf0db519acdcbbe967e4','X'),
'BACK-MATTER/Index/Images/_page_996_Picture_8.jpeg':(8414,123,260,'6a39699460a0c9e5314801b0de51c7e5f41a41466f10abe9d83edc03dc3e3feb','X'),
'BACK-MATTER/Index/Images/_page_996_Picture_9.jpeg':(11018,145,256,'7595102ac69dcfab3a9b4817373c9ca2441e99f495b6b4c260e76d6f5da8aa26','X'),
'BACK-MATTER/Colophon/Images/_page_1132_Figure_9.jpeg':(34740,562,307,'f32fa3e02c9c00f5b0b23ac0d67df82f9f8cb41ecf4abb8dcfecc65d821685ac','R'),
'BACK-MATTER/Colophon/Images/_page_1152_Figure_5.jpeg':(7164,284,95,'b9c448472b4f1c2059e542b73a754cd44d7ca8460cea4a665ad206e93f680114','I'),
'BACK-MATTER/Colophon/Images/_page_1152_Figure_6.jpeg':(6185,268,93,'c21b0f6c3ab30d2ff50c0384efedaa7c1fe2c1a576301ac3481a29b229cf778e','I'),
}

# BOOK line: (split document, split line, physical item)
routes={
778:('CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md',95,'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_75_Figure_6.jpeg'),
1280:('CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md',597,'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_122_Figure_2.jpeg'),
2866:('CHAPTERS/6-Starting-from-Randomness/Starting-from-Randomness.md',163,'CHAPTERS/6-Starting-from-Randomness/Images/_page_256_Figure_2.jpeg'),
3944:('CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Mechanisms-in-Programs-and-Nature.md',521,'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_354_Picture_2.jpeg'),
7928:('CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md',227,'CHAPTERS/11-The-Notion-of-Computation/Images/_page_672_Picture_1.jpeg'),
7932:('CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md',231,'CHAPTERS/11-The-Notion-of-Computation/Images/_page_672_Picture_3.jpeg'),
7934:('CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md',233,'CHAPTERS/11-The-Notion-of-Computation/Images/_page_672_Picture_4.jpeg'),
7984:('CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md',283,'CHAPTERS/11-The-Notion-of-Computation/Images/_page_677_Figure_2.jpeg'),
9164:('CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md',547,'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_769_Figure_1.jpeg'),
10393:('CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md',1774,'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_847_Figure_1.jpeg'),
10409:('CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md',1790,'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_848_Figure_2.jpeg'),
11170:('CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md',2551,'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_25.jpeg'),
11297:('CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md',2678,'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_885_Picture_21.jpeg'),
14226:('BACK-MATTER/Index/Index.md',2127,'BACK-MATTER/Index/Images/_page_963_Picture_8.jpeg'),
14228:('BACK-MATTER/Index/Index.md',2129,'BACK-MATTER/Index/Images/_page_963_Picture_9.jpeg'),
14230:('BACK-MATTER/Index/Index.md',2131,'BACK-MATTER/Index/Images/_page_963_Picture_10.jpeg'),
14232:('BACK-MATTER/Index/Index.md',2133,'BACK-MATTER/Index/Images/_page_963_Picture_11.jpeg'),
14390:('BACK-MATTER/Index/Index.md',2291,'BACK-MATTER/Index/Images/_page_967_Picture_22.jpeg'),
15313:('BACK-MATTER/Index/Index.md',3214,'BACK-MATTER/Index/Images/_page_996_Picture_6.jpeg'),
15315:('BACK-MATTER/Index/Index.md',3216,'BACK-MATTER/Index/Images/_page_996_Picture_7.jpeg'),
15317:('BACK-MATTER/Index/Index.md',3218,'BACK-MATTER/Index/Images/_page_996_Picture_8.jpeg'),
15319:('BACK-MATTER/Index/Index.md',3220,'BACK-MATTER/Index/Images/_page_996_Picture_9.jpeg'),
18759:('BACK-MATTER/Colophon/Colophon.md',1316,'BACK-MATTER/Colophon/Images/_page_1132_Figure_9.jpeg'),
19236:('BACK-MATTER/Colophon/Colophon.md',1793,'BACK-MATTER/Colophon/Images/_page_1152_Figure_5.jpeg'),
19238:('BACK-MATTER/Colophon/Colophon.md',1795,'BACK-MATTER/Colophon/Images/_page_1152_Figure_6.jpeg'),
}

def jpeg_size(data):
    assert data[:2]==b'\xff\xd8'
    sof={0xC0,0xC1,0xC2,0xC3,0xC5,0xC6,0xC7,0xC9,0xCA,0xCB,0xCD,0xCE,0xCF}
    i=2
    while i<len(data):
        while i<len(data) and data[i]!=0xFF: i+=1
        while i<len(data) and data[i]==0xFF: i+=1
        marker=data[i]; i+=1
        if marker in sof:
            return (int.from_bytes(data[i+5:i+7],'big'),
                    int.from_bytes(data[i+3:i+5],'big'))
        if marker in {0x01,0xD8,0xD9} or 0xD0<=marker<=0xD7: continue
        length=int.from_bytes(data[i:i+2],'big')
        assert length>=2
        i+=length
    raise AssertionError('JPEG SOF not found')

assert len(items)==len(routes)==25
assert set(items)=={v[2] for v in routes.values()}
assert len({Path(p).name for p in items})==25
assert len({v[3] for v in items.values()})==25
assert {s:sum(v[4]==s for v in items.values()) for s in 'IRX'}=={'I':5,'R':13,'X':7}
for n,(split_rel,split_n,asset_rel) in routes.items():
    name=Path(asset_rel).name
    assert book[n-1].strip()==f'![]({name})'
    split=(ROOT/split_rel).read_text().splitlines()
    assert split[split_n-1].strip()==f'![](Images/{name})'
for rel,(size,w,h,digest,_) in items.items():
    data=(ROOT/rel).read_bytes()
    assert len(data)==size
    assert jpeg_size(data)==(w,h)
    assert sha256(data).hexdigest()==digest
print('T05 metadata oracle: PASS 25 assets; 5 included; 13 relation-only; 7 excluded')
PY
~~~

Recorded output:

~~~text
T05 metadata oracle: PASS 25 assets; 5 included; 13 relation-only; 7 excluded
~~~

### Exact asset semantic oracle

The direct plates authorize three exact code-label/table corpora and three property rasters. They do not jointly serialize seed values, palette-to-value mapping, horizon, crop/resampling, or a numeric plot series, so the number of source-authorized exact cell-trajectory goldens is zero.

~~~bash
python3 - <<'PY'
from hashlib import sha256
from pathlib import Path

book=Path('ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md').read_text().splitlines()
def cases(k): return 3*k-2
def rule_count(k): return k**cases(k)
def table(code,k):
    assert 0<=code<rule_count(k)
    return tuple(code//k**s%k for s in range(cases(k)))
def corpus_hash(codes,k):
    blob='\n'.join(f'{n}:{",".join(map(str,table(n,k)))}' for n in codes).encode()
    return sha256(blob).hexdigest()

p122_k4=tuple(range(107395,107403))
p122_k5=tuple(range(180197741,180197749))
p256_k4=tuple(range(1000816,1000941,4))
assert (len(p122_k4),len(p122_k5),len(p256_k4))==(8,8,32)
assert (cases(4),rule_count(4),cases(5),rule_count(5))==(10,1048576,13,1220703125)
assert table(p122_k4[0],4)==(3,0,0,2,3,0,2,2,1,0)
assert table(p122_k4[-1],4)==(2,2,0,2,3,0,2,2,1,0)
assert table(p122_k5[0],5)==(1,3,4,1,1,3,2,1,1,2,3,3,0)
assert table(p122_k5[-1],5)==(3,4,4,1,1,3,2,1,1,2,3,3,0)
assert table(p256_k4[0],4)==(0,0,3,1,1,1,0,1,3,3)
assert table(p256_k4[-1],4)==(0,3,2,3,1,1,0,1,3,3)
assert all(table(n,4)[0]==0 for n in p256_k4)
assert corpus_hash(p122_k4,4)=='fa4dc8a897879f316780d166e26ff5549a9d1e8242ec323979d78adf69d82abd'
assert corpus_hash(p122_k5,5)=='06a040bce47ad991e7223275eccd7b43f22bceb8579dedebe636d4d256053222'
assert corpus_hash(p256_k4,4)=='8b2c14a1a62591c80fcdcd98da0de6d6b352f867e373515f88695813803b79d0'

table1004600=(0,2,3,0,0,1,1,1,3,3)
assert table(1004600,4)==table1004600
assert ''.join(map(str,reversed(table1004600)))=='3311100320'
assert corpus_hash((1004600,),4)=='ffa5b12995ff8284f065ee95438ac673eb07234eb9674ebc0f48b4e4436a644b'
properties={
 'death_steps':{'a':36,'b':1017},
 'reported_widths':{1000000:{'c':31000,'d':39718},
                    10000000:{'c':339028,'d':390023}},
 'through_at_least_steps':20000000,
 'growth_cells_per_step':{'c':0.035,'d':0.039},
 'mean_nonwhite_fraction':0.28,
 'continued_fluctuations':True,
}
assert properties['death_steps']=={'a':36,'b':1017}
assert properties['reported_widths'][10000000]=={'c':339028,'d':390023}
assert properties['through_at_least_steps']==20000000
assert properties['mean_nonwhite_fraction']==0.28
for n,tokens in {
1282:('13 cases','1,220,703,125','Allowing four or more colors'),
2868:('totalistic rules','nearest neighbors','four possible colors'),
9166:('36 steps','1017 steps','a million steps','code 1004600'),
9170:('31,000','39,718','10 million','339,028','390,023'),
19234:('0.035','0.039','28%','at least 20 million steps','fluctuations'),
}.items():
    assert all(t in book[n-1] for t in tokens)

direct_label_corpora=(('p122-k4',p122_k4),('p122-k5',p122_k5),('p256-k4',p256_k4))
direct_property_links=(9164,19236,19238)
missing_for_trajectory={
1280:{'serialized_seed','sampling_rule','palette_to_value','horizon','crop_resampling'},
2866:{'serialized_seed','palette_to_value','horizon','crop_resampling'},
9164:{'serialized_seed','palette_to_value','initial_row_convention','crop_resampling'},
19236:{'numeric_series'},19238:{'numeric_series'},
}
direct_exact_cell_goldens=()
assert len(direct_label_corpora)==3
assert direct_property_links==(9164,19236,19238)
assert set(missing_for_trajectory)=={1280,2866,9164,19236,19238}
assert all(missing_for_trajectory.values())
assert len(direct_exact_cell_goldens)==0
print('T05 asset semantic oracle: PASS')
print('label_corpora=',tuple((name,len(codes)) for name,codes in direct_label_corpora))
print('corpus_hashes=',corpus_hash(p122_k4,4),corpus_hash(p122_k5,5),corpus_hash(p256_k4,4))
print('code1004600=',table1004600,'display=3311100320')
print('direct_property_links=',direct_property_links,'direct_exact_cell_goldens=',len(direct_exact_cell_goldens))
PY
~~~

Recorded output:

~~~text
T05 asset semantic oracle: PASS
label_corpora= (('p122-k4', 8), ('p122-k5', 8), ('p256-k4', 32))
corpus_hashes= fa4dc8a897879f316780d166e26ff5549a9d1e8242ec323979d78adf69d82abd 06a040bce47ad991e7223275eccd7b43f22bceb8579dedebe636d4d256053222 8b2c14a1a62591c80fcdcd98da0de6d6b352f867e373515f88695813803b79d0
code1004600= (0, 2, 3, 0, 0, 1, 1, 1, 3, 3) display=3311100320
direct_property_links= (9164, 19236, 19238) direct_exact_cell_goldens= 0
~~~

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
