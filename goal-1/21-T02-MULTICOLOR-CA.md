# 21-T02-MULTICOLOR-CA

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T02, CSV line 3, `Multi-Color Nearest-Neighbor Cellular Automata`; taxonomy vocabulary is `ref/notes/CA-Types.md:45-66` and remains a search/API seed rather than book evidence.
- The strict Chapter 3 transition at `BOOK:770-776` directly states three colors, the exact count `7,625,597,484,987`, and the ordered-neighborhood/totalistic contrast. Most immediately following examples are totalistic and belong primarily to T03/T04, so their rule aggregation cannot be imported into T02.
- `BOOK:4684` directly describes arbitrary three-color nearest-neighbor tables over all 27 ordered three-cell neighborhoods and a mutation profile that adds or changes individual neighborhood entries.
- `BOOK:5218-5222` directly identifies all `3^27` three-color nearest-neighbor rules and the 1,800 reversible members. Reversibility is a property/restriction, not a different forward update construction.
- T01 already establishes a fixed ordered one-dimensional lattice, total field, synchronous old left/self/right reads, arbitrary finite lookup, typed same-site assignment, atomic parallel commit, and separate native/finite support, seed, trace, and view identities.
- The central question is therefore whether T02 is exactly T01 parameterized by a finite alphabet of cardinality `k>2` plus a base-`k` ordered table codec, or whether direct evidence forces any new state/read/update primitive.
- Current runtime alphabet declarations can represent finite integer/symbolic colors, but the documented/executable exhaustive binary codec and family-dispatched rollout were already defective for T01. Existing nominal color capacity is not proof of an executable general `k^(k^3)` rule table.

## Updated Assumptions

- Treat `k=3` as the strict directly enumerated profile. General `k` remains a candidate generalization until the Notes/Index/general-definition evidence is audited.
- Preserve colors as distinct symbols or validated digits `0..k-1`; visual white/gray/black tones are a view convention unless a numeric aggregate such as totalistic averaging explicitly gives them arithmetic meaning.
- Preserve ordered neighborhoods. A totalistic, semi-totalistic, symmetric, reversible, background-preserving, mutation-generated, or emulation profile is a restriction/property/relation unless evidence makes it defining.
- Do not infer a single-gray-cell seed, unchanged white background, random seed, finite periodic boundary, or figure horizon as native T02 semantics.
- Do not add an eleventh update law unless T02 evidence contradicts T01's fixed-effects atomic commit.

## Big Picture Objective

Determine exhaustively whether multi-color nearest-neighbor cellular automata are the finite-alphabet/base-`k` parameterization of the T01 construction, while preserving exact table ordering/coding, background/seed/reversibility restrictions, mutation provenance, numerical-versus-symbolic color roles, support/realization/trace/view boundaries, and implementation-ready Goal 2 conformance without a family rollout branch.

## Catalog Identity

- Stable ID: T02.
- Exact CSV name: `Multi-Color Nearest-Neighbor Cellular Automata` at `ref/notes/CA-Types.csv:3`.
- Taxonomy: `ref/notes/CA-Types.md:45-66`; vocabulary seed only.
- Candidate entry kind: parameterized fixed-lattice parallel lookup construction, subject to complete evidence audit.
- Initial vocabulary: multi-color/multicolor, three/four/many colors, possible colors/states, nearest-neighbor rules, 27 possible three-cell neighborhoods, `7,625,597,484,987`, base-3 rule/table/code, reversible three-color CA, mutation of neighborhood rules, color encoding, and emulation of colors.

## Search Log

The actual Index begins at `BOOK:20826`. The controlled oracle below asserts 29 regex manifests across the complete monolith and a disjoint disposition of their 157 unique physical candidate lines. Counts are candidate-line counts, not raw substring occurrences:

| Q | Search family | Pre-Index | Actual Index |
|---:|---|---:|---:|
| 01 | spelled `three-color` / `three colors` | 28 | 3 |
| 02 | numeric `3-color` / `3 colors` | 18 | 2 |
| 03 | more than two / more / several colors | 14 | 2 |
| 04 | `k-color` / `k colors` | 29 | 0 |
| 05 | multi-color/multicolor | 1 | 3 |
| 06 | numeric colors near nearest-neighbor | 7 | 0 |
| 07 | spelled color counts near nearest-neighbor | 9 | 0 |
| 08 | possible colors near nearest-neighbor | 15 | 0 |
| 09 | exact full count / `8 trillion` | 5 | 0 |
| 10 | 27 possible neighborhoods | 1 | 0 |
| 11 | general `k^(k^(2r+1))` formula | 3 | 0 |
| 12 | general nearest-neighbor rule signature | 1 | 0 |
| 13 | general-CA implementation phrases | 2 | 0 |
| 14 | fixed line/array/organization | 2 | 0 |
| 15 | old-neighbor/parallel-update phrases | 7 | 0 |
| 16 | immediate neighbors | 15 | 0 |
| 17 | general `k,r` rule phrases | 4 | 0 |
| 18 | three/`k` colors near totalistic | 17 | 0 |
| 19 | two-cell neighborhood boundary | 2 | 0 |
| 20 | explicit/general implementation tokens | 3 | 0 |
| 21 | `k=3,r=1` | 13 | 0 |
| 22 | source rule numbers | 4 | 0 |
| 23 | 27 neighborhoods/cases | 2 | 0 |
| 24 | rules involving three colors | 4 | 0 |
| 25 | CA `state` alias probe | 0 | 0 |
| 26 | asymmetry / left-right positional probe | 5 | 0 |
| 27 | literal `ordered neighborhood` probe | 0 | 0 |
| 28 | `{n,k}` / `{k^2,k,1}` positional codec | 1 | 0 |
| 29 | broad arbitrary-CA/neighborhood saturation | 4 | 0 |

The exact reproducible oracle is intentionally self-contained:

```bash
python3 - <<'PY'
import re
from pathlib import Path

L=Path('ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md').read_text().splitlines()
IX=20826
def xs(s): return [] if s=='-' else list(map(int,s.split(',')))
rows=[
(r'(?i)\bthree[- ]color(?:ed)?\b|\bthree (?:possible )?colors\b','772,774,776,780,784,790,796,800,804,808,824,846,1282,2806,2822,2852,3352,5218,5222,5482,5486,7900,7912,10399,10411,11375,15972,18339','20967,21134,21933'),
(r'(?i)\b3[- ]color(?:ed)?\b|\b3 (?:possible )?colors\b','3320,3324,4684,6340,8020,8040,8534,8544,8546,8560,8936,10395,12055,15661,18476,18744,18823,18877','20846,20972'),
(r'(?i)\bmore than two (?:possible )?colors\b|\bmore colors\b|\bseveral colors\b','1282,7900,8072,8318,11283,12055,12311,12313,13619,15245,18339,18348,18592,18755','20965,22372'),
(r'(?i)\bk[- ]color\b|\bk possible colors\b|\bk colors\b','11051,11052,11056,11060,11283,11889,11897,12042,12308,13483,13513,14040,14046,14285,14301,14352,14488,14512,14661,14672,16016,16123,16175,16429,17533,18363,18532,18672,20027','-'),
(r'(?i)multi[- ]?colou?rs?','18532','21187,21323,21542'),
(r'(?i)(?:\b\d+\s*-?\s*colors?.{0,100}nearest[- ]neighbor|nearest[- ]neighbor.{0,100}\b\d+\s*-?\s*colors?)','3316,3320,3324,7960,8144,18670,18672','-'),
(r'(?i)(?:\b(?:three|four|five|seven|seventeen|eighteen|nineteen|twenty-eight)\s*-?\s*(?:possible )?colors?.{0,100}nearest[- ]neighbor|nearest[- ]neighbor.{0,100}\b(?:three|four|five|seven|seventeen|eighteen|nineteen|twenty-eight)\s*-?\s*(?:possible )?colors?)','2806,2822,2852,2868,5218,5222,7912,7986,18339','-'),
(r'(?i)(?:possible colors.{0,80}nearest[- ]neighbor|nearest[- ]neighbor.{0,80}possible colors)','2798,2802,2806,2822,2852,2868,4684,7892,7912,7914,7986,8010,8140,8318,15307','-'),
(r'7,625,597,484,987|7625597484987|8 trillion','772,5218,10399,10411,11897','-'),
(r'(?i)27 possible.{0,30}neighborhood','4684','-'),
(r'k\^\{k\^\{2r\+1\}\}','11897,14352,18348','-'),
(r'(?i)general nearest[- ]neighbor rule with k colors','11051','-'),
(r'(?i)implementation of general cellular automata|possible blocks of cells in each neighborhood','11004,11898','-'),
(r'(?i)cellular automaton consists of a line of cells|fixed array of cells|underlying number and organization of cells','422,982','-'),
(r'(?i)old values of neighbors|old value of (?:the )?left-hand neighbor|updated in parallel|all the cells.{0,20}updated in parallel','850,1254,5830,10984,10996,13889,16446','-'),
(r'(?i)immediate neighbors','430,716,776,856,882,1533,1956,1960,1986,2002,2922,3956,6218,7884,15207','-'),
(r'(?i)allowing k possible colors.{0,80}r neighbors on each side|general rule with k colors and range r|original rule with \*k\* colors and \*r\* neighbors|rules with k colors and range r','11052,11897,14352,18348','-'),
(r'(?i)(?:three[- ]color|three possible colors|k[- ]color|k possible colors).{0,100}totalistic|totalistic.{0,100}(?:three[- ]color|three possible colors|k[- ]color|k possible colors)','774,776,784,790,796,800,804,808,824,846,1282,2806,2822,2852,7912,11056,11060','-'),
(r'(?i)two-cell neighborhoods|2-neighbor rules|two rather than three neighboring cells','11881,18744','-'),
(r'(?i)explicit replacements for all|Transpose\[\{RotateRight\[a\], a, RotateLeft\[a\]\}\]|IntegerDigits\[num, k, k\^2r\^1\]','11002,11014,11900','-'),
(r'(?i)k\s*=\s*3\s*,\s*r\s*=\s*1|k=3\s*,\s*r=1','11164,11168,11897,14541,15493,16020,16024,16025,16027,18348,18748,20573,20577','-'),
(r'921408|5407067979|1340716537107','10395,11164,20573,20577','-'),
(r'(?i)27 (?:possible )?(?:3-cell neighborhoods|cases)','4684,20577','-'),
(r'(?i)rules? (?:that )?(?:involve|involving|with) three colors|rules? with three colors|three-color rules?','772,7912,10399,10411','-'),
(r'(?i)(?:(?:cellular automata|cellular automaton).{0,100}(?:more than two|three|3|k) (?:possible )?states|(?:more than two|three|3|k) (?:possible )?states.{0,100}(?:cellular automata|cellular automaton))','-','-'),
(r'(?i)asymmetr(?:y|ic).{0,100}(?:cellular automaton )?rule|(?:cellular automaton )?rule.{0,100}asymmetr(?:y|ic)|left neighbor.{0,100}right neighbor','452,490,498,10988,17995','-'),
(r'(?i)ordered.{0,100}neighborhood|neighborhood.{0,100}ordered','-','-'),
(r'(?i)CellularAutomaton\[\{n, k\}|\{k\^2, k, 1\}','11066','-'),
(r'(?i)arbitrary.{0,100}(?:cellular automaton|neighborhood)|(?:cellular automaton|neighborhood).{0,100}arbitrary','7156,14216,17431,19588','-'),
]
sets=[]
for q,(pattern,pre_s,idx_s) in enumerate(rows,1):
    found=[i for i,line in enumerate(L,1) if re.search(pattern,line)]
    pre=[i for i in found if i<IX]; idx=[i for i in found if i>=IX]
    assert pre==xs(pre_s),(q,pre,xs(pre_s))
    assert idx==xs(idx_s),(q,idx,xs(idx_s))
    sets.append(set(found))
    print(f'Q{q:02d} pre={len(pre)} idx={len(idx)}')

parts={
'core':'422,430,452,490,498,716,772,850,982,1254,1533,4684,6218,7884,10984,10988,11002,11004,11014,11051,11052,11066,11164,11897,11898,11900,13513,16446,18348,20577',
'target':'5218,5222,7900,7960,7986,8144,8318,10395,10399,10411,14216,15493,16016,16020,16024,16025,16027,16123,18339,18670,18672,20573',
'totalistic':'774,776,780,784,790,796,800,804,808,824,846,1282,2802,2806,2822,2852,2868,3320,3324,3352,6340,7912,8936,11056,11060,11168,18748',
'additive':'11283,14352,14488,14512,20027,20846',
'other_ca':'1956,1960,1986,2002,2798,2922,3316,3956,5482,5486,7156,7892,7914,8010,8140,10996,11881,11889,13483,13619,14046,14285,14301,14541,14661,15307,15661,15972,16175,17431,18744,18755,19588',
'false':'856,882,5830,8020,8040,8072,8534,8544,8546,8560,11375,12042,12055,12308,12311,12313,13889,14040,14672,15207,15245,16429,17533,18363,18476,18532,18592,18823,18877',
'index_target':'20965,20967,21134,21187,21323,21542,21933,22372',
'index_sibling':'20972',
'incidental':'17995',
}
partition={name:xs(value) for name,value in parts.items()}
flat=[i for values in partition.values() for i in values]
union=set().union(*sets)
assert len(rows)==29 and len(union)==157
assert len(flat)==len(set(flat))==157 and set(flat)==union
assert [len(partition[k]) for k in partition]==[30,22,27,6,33,29,8,1,1]
print('T02 literal search oracle: PASS 29 queries; 157 unique candidate lines')
print('partition=30,22,27,6,33,29,8,1,1')
PY
```

The command ends:

```text
T02 literal search oracle: PASS 29 queries; 157 unique candidate lines
partition=30,22,27,6,33,29,8,1,1
```

### Complete candidate disposition

- **Core/definition (30):** `422,430,452,490,498,716,772,850,982,1254,1533,4684,6218,7884,10984,10988,11002,11004,11014,11051,11052,11066,11164,11897,11898,11900,13513,16446,18348,20577`. These establish fixed line/support, positional left/self/right reads, asymmetry, old-snapshot parallel update, arbitrary explicit/general rule forms, alphabet/range syntax, positional weights, exact count, implementation, and 27-case search semantics; unique mechanics are excerpted below.
- **Valid T02 instances/corroboration (22):** `5218,5222,7900,7960,7986,8144,8318,10395,10399,10411,14216,15493,16016,16020,16024,16025,16027,16123,18339,18670,18672,20573`. These supply reversible members, arbitrary-color instances/emulators, purpose/search rules, general `k=3,r=1` profiles, encoding, and history. They cannot add hidden state or change base execution.
- **Totalistic sibling (27):** `774,776,780,784,790,796,800,804,808,824,846,1282,2802,2806,2822,2852,2868,3320,3324,3352,6340,7912,8936,11056,11060,11168,18748`. These are members of the full table space but use a distinct aggregate rule description owned by T03/T04/T05. The page-75 figure and its single-gray/background convention do not define T02.
- **Additive/associative sibling (6):** `11283,14352,14488,14512,20027,20846`. These are algebraic subfamilies/properties, with the last an Index pointer; no distinct T02 mechanics.
- **Other CA construction/geometry/range/schedule or ancillary (33):** `1956,1960,1986,2002,2798,2922,3316,3956,5482,5486,7156,7892,7914,8010,8140,10996,11881,11889,13483,13619,14046,14285,14301,14541,14661,15307,15661,15972,16175,17431,18744,18755,19588`. These concern higher range, staggered two-cell, block/sequential/2D/continuous/probabilistic constructions, arbitrary initial conditions, or general implementation context and are bounded explicitly rather than imported.
- **Other system/false positive (29):** `856,882,5830,8020,8040,8072,8534,8544,8546,8560,11375,12042,12055,12308,12311,12313,13889,14040,14672,15207,15245,16429,17533,18363,18476,18532,18592,18823,18877`. These are mobile/Turing/substitution/tag/multiway/physical/network/color-encoding contexts or unrelated uses of colors/states.
- **Relevant actual-Index cross-references (8):** `20965,20967,21134,21187,21323,21542,21933,22372`. They route more-colors, three-colors, encoding/emulation, and reversibility vocabulary to already inspected passages but add no construction text.
- **Actual-Index sibling (1):** `20972` routes a `3-color` Turing-machine entry, not T02.
- **Incidental asymmetry false hit (1):** `17995` concerns an unrelated algebraic asymmetry statement.

No candidate remains unresolved. The zero-hit probes are informative: the source does not literally say `ordered neighborhood` and uses `colors`, not a T02 `states` alias. Ordered dependence is a source-derived structural inference from positional left/center/right rules, asymmetric cases, sorted offsets, and the explicit `{k^2,k,1}` weights; it is not presented as a verbatim phrase.

### Split and routing audit

- Strict `BOOK:772` maps to Chapter 3 split line 89; `BOOK:422`, `850`, `982`, `4684`, `5218`, `7900/7912`, and `10411` route to the expected Chapter 2/3/8/9/11/12 duplicates. Minor split wording does not replace canonical monolith provenance.
- The Chapter 12 split duplicates only part of the Notes through the source's printed-page-904 region and omits later Notes; `BACK-MATTER/Notes/Notes.md` is an unrelated one-line fragment. `BACK-MATTER/Index/Index.md` contains misrouted Notes and is not the actual Index.
- Actual Index starts at `BOOK:20826`; all eight relevant pointers route to included/corroborating passages above. No duplicate excerpt is counted twice.

## Book Excerpts

### E1 — Three colors and the full rule-space count

- Provenance: `BOOK:772`, strict Chapter 3 transition.
- Establishes: more than two cell colors and the exact full three-color rule count; totalistic rules are a smaller restriction.

> “The 256 "elementary" rules that we have discussed so far are by most measures the simplest possible—and were the first ones I studied. But one can for example also look at rules that involve three colors, rather than two, so that cells can not only be black and white, but also gray. The total number of possible rules of this kind turns out to be immense—7,625,597,484,987 in all—but by considering only so-called "totalistic" ones, the number becomes much more manageable.”

### E2 — Explicit 27-neighborhood arbitrary-table profile

- Provenance: `BOOK:4684`, supporting caption.
- Establishes: three colors, nearest-neighbor rules, all 27 possible ordered three-cell neighborhoods, and mutations that add or modify individual table entries. A dot means retain the center color in this figure's sparse rule representation.

> “The behavior of a sequence of cellular automaton programs obtained by successive random mutations. The first program contains no rules for changing the color of a cell with any neighborhood. Mutations in successive programs add rules for changing the colors of cells with specific neighborhoods, or modify these rules. Each program in the sequence differs from the previous one by a single mutation, made completely at random. The sequence provides a very simple idealization of biological evolution without explicit natural selection. The cellular automata shown here all have 3 possible colors and nearest-neighbor rules. The label for each picture gives a representation of the rules for each of the 27 possible 3-cell neighborhoods. A dot signifies that the rule does not change the color of the center cell in the neighborhood.”

### E3 — Reversibility is a subset property

- Provenance: `BOOK:5218-5222`, supporting Chapter 9 discussion/caption.
- Establishes: the full three-color nearest-neighbor space has the same exact count, 1,800 members are reversible, and forward complexity does not erase backwards determinability.

> “So is it possible to get more complex behavior while maintaining reversibility? There are a total of 7,625,597,484,987 cellular automata with three colors and nearest-neighbor rules, and searching through these one finds just 1800 that are reversible. Of these 1800, many again exhibit simple behavior, much like the pictures above. But some exhibit more complex behavior, as in the pictures below.”

> “Examples of some of the 1800 reversible cellular automata with three colors and nearest-neighbor rules. Even though these systems exhibit complex behavior that scrambles the initial conditions, all of them are still reversible, so that starting from the configuration of cells at the bottom of each picture, it is always possible to deduce the configurations on all previous steps.”

### E4 — Inherited line and nearest-neighbor read

- Provenance: `BOOK:422,430`, inherited Chapter 2 construction.
- Establishes: a one-dimensional line; the old left/self/right neighborhood; and a case table whose output is the next color of the center cell. The black/white alphabet in this introductory example is specialized by E1/E2, not retained as a T02 limit.

> “The cellular automaton consists of a line of cells, each colored either black or white. At every step there is then a definite rule that determines the color of a given cell from the color of that cell and its immediate left and right neighbors on the step before.”

> “gives one of the possible combinations of colors for a cell and its immediate neighbors. The bottom row then specifies what color the center cell should be on the next step in each of these cases. In the numbering scheme described in Chapter 3, this is cellular automaton rule 254.”

### E5 — Left, center, and right are positional

- Provenance: `BOOK:490,498`, inherited Chapter 2 behavior/rule description.
- Establishes: left-right asymmetry can be encoded in the rule, and a rule case can distinguish the left neighbor from the center and right neighbor. This is evidence for ordered context even though the literal phrase `ordered neighborhood` never occurs.

> “The asymmetry between the left and right-hand sides is a direct consequence of asymmetry that exists in the particular underlying cellular automaton rule used.”

> “But now the specific rule used—that I call rule 110—takes the new color of a cell to be black in every case except when the previous colors of the cell and its two neighbors were all the same, or when the left neighbor was black and the cell and its right neighbor were both white.”

### E6 — Fixed organization and parallel update

- Provenance: `BOOK:850,982`, inherited Chapter 3 construction contrast.
- Establishes: all cells update in parallel, while the underlying array organization remains fixed.

> “One of the basic features of a cellular automaton is that the colors of all the cells it contains are updated in parallel at every step in its evolution.”

> “One of the features that cellular automata, mobile automata and Turing machines all have in common is that at the lowest level they consist of a fixed array of cells. And this means that while the colors of these cells can be updated according to a wide range of different possible rules, the underlying number and organization of cells always stays the same.”

### E7 — Parallel update reads the old field

- Provenance: `BOOK:10984`, Notes implementation warning.
- Establishes: a cellular-automaton rule reads old neighbor values; an in-place sequential implementation must preserve those values or use two arrays. This is direct support for snapshot evaluation followed by atomic commit.

> “First, cellular automaton rules are always defined to use the old values of neighbors in determining the new value of any particular cell.”

> “Another approach to this problem is to maintain two copies of the array of cells, and to interchange pointers to them after every step in the cellular automaton evolution.”

### E8 — A general rule is an explicit neighborhood-case relation

- Provenance: `BOOK:11002-11004`, Notes general-rule definition.
- Establishes: general 1D CA rules are explicit replacements over all possible neighborhood blocks, not an aggregate reducer or callback.

> “In general, however, a 1D cellular automaton rule can be given as a set of explicit replacements for all”

> “possible blocks of cells in each neighborhood (see page 60).”

### E9 — The executable context is an ordered triple

- Provenance: `BOOK:11014`, Notes implementation.
- Establishes: the implementation constructs a three-position record before applying the rule. Position is preserved; no sum/average is taken.

> `Transpose[{RotateRight[a], a, RotateLeft[a]}]/. rule`

### E10 — General and totalistic rules have distinct signatures

- Provenance: `BOOK:11051-11056`, built-in-function Notes table.
- Establishes: `{n,k}` is the general nearest-neighbor rule form; `{n,k,r}` changes range; the totalistic form has a separately tagged `{k,1}` rule specification.

> `\{n, k\} general nearest-neighbor rule with k colors`

> `\{n, k, r\} general rule with k colors and range r`

> `\{n, \{k, 1\}\} k-color nearest-neighbor totalistic rule`

### E11 — Base-`k` positional weights

- Provenance: `BOOK:11066-11067`, Notes equivalence fragment.
- Establishes: the general nearest-neighbor codec uses positional weights `k^2,k,1`, so left/center/right permutations have distinct addresses. The source extraction breaks the expression across lines; only the intact equivalence and weight vector are used.

> `■ CellularAutomaton[{n, k},...] is equivalent to CellularAutomaton[{n, {k,`

> `\{k^2, k, 1\}\}, \dots Common forms for 2D cellular automata include:`

### E12 — Runnable general and totalistic `k=3,r=1` profiles

- Provenance: `BOOK:11164-11168`, Notes examples.
- Establishes: general rule number `921408` and totalistic code `867` use different rule signatures at the same alphabet size and range. The extracted invocations are OCR-damaged; their prose labels and rule identities are intact.

> “This runs the general k=3, r=1 rule with rule number 921408. In[10]:=Show[RasterGraphics[CellularAutomaton]{921408, 3, 1}, {{1}, 0}, 100]]]”

> “This runs the totalistic k=3, r=1 rule with code 867.  $ln[11]:=Show[RasterGraphics[CellularAutomaton]{867, {3, 1}, 1}, {{1}, 0}, 50]]]$ ”

### E13 — General rule-count theorem and exact specialization

- Provenance: `BOOK:11897`, page-60 Notes.
- Establishes: a `k`-color range-`r` general rule has `k^(k^(2r+1))` possibilities; `k=3,r=1` has exactly `7,625,597,484,987`; totalistic rules are a much smaller separately counted subset.

> “Allowing k possible colors for each cell and considering r neighbors on each side, there are  $k^{k^{2r+1}}$  possible cellular automaton rules in all”

> “And for k=3, r=1 there are 7,625,597,484,987 rules in all, with 2187 totalistic ones.”

> “Note that for k>2, a particular rule will in general be totalistic only for a specific assignment of values to colors.”

### E14 — General base-`k` step implementation

- Provenance: `BOOK:11898-11900`, page-60 Notes.
- Establishes: general evolution computes a positional neighborhood address with powers of `k` and indexes a rule digit sequence. The extracted digit-count exponent is malformed and repaired only by the intact count theorem in E13.

> “With *k* colors and *r* neighbors on each side, a single step in the evolution of a general cellular automaton is given by”

> `CAStep[CARule[rule\_List,  $k_r$ ,  $r_r$ ],  $a_r$ List] :=  $rule[-1 - ListConvolve[k^Range[0, 2r], a, r + 1]]]$  where rule is obtained from a rule number num by  $IntegerDigits[num, k, k^2r^1]$ . (See also page 927.)`

### E15 — Neighborhood offsets and colors share one order

- Provenance: `BOOK:13513`, general-rules Notes.
- Establishes: source offset lists have a defined ordering, and neighborhood colors are supplied in that same ordering.

> “In this book such offset lists are always taken to be in the order given by *Sort*”

> “One can specify a neighborhood configuration by giving in the same order as the offset list the color of each cell in the neighborhood.”

### E16 — Sequential CA is a different schedule

- Provenance: `BOOK:16446`, Notes construction contrast.
- Establishes: ordinary CA updates every cell in parallel from previous-step colors; sequential CA can observe newly written colors and is therefore a distinct construction, not a T02 option.

> “Ordinary cellular automata are set up so that every cell is updated in parallel at each step, based on the colors of neighboring cells on the previous step.”

> “in sequential cellular automata the new color of a particular cell can depend on new rather than old colors of neighboring cells.”

### E17 — Multicolor emulation is a relation, not native storage

- Provenance: `BOOK:18339-18348`, page-655 Notes.
- Establishes: a three-color nearest-neighbor rule can be encoded into a two-color larger-neighborhood rule, but the original general rule retains its own `k^(k^(2r+1))` information content. The encoding is not T02's native state representation.

> “Given a rule that involves three colors and nearest neighbors, the following converts each case of the rule to a collection of cases for a rule with two colors:”

> “Note that the original rule with *k* colors and *r* neighbors involves  $Log[2, k^{k^{2r+1}}]$  bits of information”

### E18 — General-rule search uses all 27 cases

- Provenance: `BOOK:20573-20579`, page-832/833 Notes.
- Establishes: rule `5407067979` is explicitly `k=3,r=1`; the full rule has 27 cases; search pruning and unvisited cases are experiment-specific and do not reduce native table arity.

> “Rule (c) is k = 3, r = 1 rule 5407067979”

> “General rules can show subtle bugs; rule 1340716537107 for example first fails at n = 24. The total number of k = 3, r = 1 rules that need to be searched can easily be reduced from  $3^{27}$  to  $3^{21}$ . Several different rules that work can behave identically, since up to 6 of the 27 cases in each rule are not sampled with the initial conditions used.”

> “rules that work, between 8 and 19 cases lead to a change in the color of a cell, with 14 cases being the most common.”

### E19 — Actual-Index routes add no new mechanics

- Provenance: actual Index `BOOK:20965,20967,21134,21187,21323,21542,21933,22372`.
- Establishes: the Index routes more-color, three-color, encoding/emulation, and reversible-three-color vocabulary back to the inspected main/Notes passages. These are routing evidence only.

> “with more colors, 107”

> “three-color, 60”

> “of three colors by two, 655, 1111”

> “multicolor encodings, 1111”

> “emulating multicolor, 1115”

> “three-color, 436”

> “emulating more colors, 669, 1113,”

### E20 — Explicit sibling and neighborhood boundaries

- Provenance: `BOOK:774,11881,18744`.
- Establishes: totalistic averaging discards individual-color order; staggered two-cell neighborhoods have a different rule count; and `3-color 2-neighbor` is named separately. None changes T02's ordered three-cell construction.

> “The idea of a totalistic rule is to take the new color of each cell to depend only on the average color of neighboring cells, and not on their individual colors.”

> “By having cells on successive steps be arranged like hexagons or staggered bricks, as in the pictures below, one can set up cellular automata in which the new color of each cell depends on the previous colors of two rather than three neighboring cells.”

> “Among 3-color 2-neighbor rules class 4 behavior seems to be comparatively rare; the picture at the top of the facing page shows an example with rule number 2144.”

## Source Repairs

1. **Strict boundary:** `BOOK:772` is the strict T02 paragraph. `BOOK:774` begins the totalistic sibling, so the page-75 totalistic figure, its base-3 aggregate code, excluded background-changing rules, and single-gray seed cannot define T02.
2. **Ordered is reconstructed vocabulary:** the controlled literal probe finds no `ordered neighborhood` phrase. E4/E5/E9/E11/E15 jointly establish position-sensitive left/self/right order; the stage must call this a source-derived structural inference, not a quotation.
3. **Color/state normalization:** the CA-specific `state`-alias probe has no hits. The book says `colors`; `state` is taxonomy/API normalization and must not imply a Turing-machine control state.
4. **Count formula repair:** the first general formula and exact `k=3,r=1` instance at `BOOK:11897` are intact. The adjacent extracted symmetric-count expression is malformed and is not used. At `BOOK:11900`, `k^2r^1` is a broken extraction of the rule-digit-count exponent; E13 and the positional address expression, not this token, establish `k^(2r+1)` entries.
5. **Invocation/codec extraction:** `BOOK:11066-11067` is split in the middle of the built-in equivalence, and both invocations at `BOOK:11164-11168` have bracket/OCR damage. Their prose labels, rule numbers, `k,r` values, and `{k^2,k,1}` vector are intact; any Goal 2 call syntax is a documented reconstruction rather than a verbatim executable expression.
6. **Search pruning:** `BOOK:20577` reduces one doubling search from `3^27` to `3^21` because up to six cases are unsampled by those initial conditions. It does not revise the general rule-space count or authorize partial tables/default outputs.
7. **Mutation dots:** at `BOOK:4684`, a dot means that the entry leaves the center color unchanged. It is not a wildcard, missing result, fourth color, or implicit default in the native table.
8. **Boundary/run separation:** cyclic finite arrays at `BOOK:10986`, figure horizons, and retained display windows are implementation/observation choices. The construction evidence fixes lattice organization and parallel local update but does not select a finite boundary condition.
9. **Seed separation:** no strict T02 seed convention is stated. Single-gray, random, uniform, sparse, periodic, and purpose-encoded initial fields remain independent profiles.
10. **Sibling overlap:** a totalistic table is mathematically one member of the full general table space, but the source and taxonomy give it a different rule description/signature. T02's canonical program form is the explicit positional lookup; T03/T04/T05 own the aggregate construction.
11. **Split routing:** the Chapter 3 split changes `can not only` to `can be not only` at its duplicate of `BOOK:772`; canonical quotation remains the monolith. The Chapter 12 split contains only an early Notes fragment; `BACK-MATTER/Notes/Notes.md` is one unrelated line, and `BACK-MATTER/Index/Index.md` contains misrouted Notes rather than the actual Index.
12. **Actual Index:** the real Index begins at `BOOK:20826`. E19 pointers corroborate routing only and are not counted as independent construction evidence.
13. **Official-PDF normalization authority:** the official Chapter 3 PDF, [`nks-ch3.pdf`](https://files.wolframcdn.com/pub/www.wolframscience.com/nks/nks-ch3.pdf), was verified at SHA-256 `d4005b27774084c276e67d46a6c79106b93b785d4329893080223c9da8263e76`. Its printed page 886 visibly confirms the normalized general count `R = k^(k^(2r+1))`, the `ListConvolve[k^Range[0,2r], ...]` lookup, and `IntegerDigits[num,k,k^(2r+1)]`. The official all-Notes PDF, [`nks-notes.pdf`](https://files.wolframcdn.com/pub/www.wolframscience.com/nks/nks-notes.pdf), was verified at SHA-256 `549f043595653a7d276b07ba52d435700039b71427b4e1774a44b1a58eff4723`; its printed page 867 visibly confirms the `{n,k}` equivalence with positional weights `{k^2,k,1}`. These normalized forms repair E11/E14 but are deliberately not presented as verbatim `BOOK` blockquotes.

### Verbatim excerpt and repair oracle

This dependency-free check pins the high-value quoted fragments to their physical monolith lines, verifies the strict/sibling boundary, and checks the exact combinatorics without trying to execute OCR-damaged Wolfram Language:

```bash
python3 - <<'PY'
from pathlib import Path

L = Path('ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md').read_text().splitlines()
checks = {
    422: ('The cellular automaton consists of a line of cells', 'immediate left and right neighbors on the step before'),
    430: ('possible combinations of colors for a cell and its immediate neighbors', 'what color the center cell should be on the next step'),
    490: ('asymmetry between the left and right-hand sides', 'underlying cellular automaton rule'),
    498: ('left neighbor was black', 'cell and its right neighbor were both white'),
    772: ('rules that involve three colors, rather than two', '7,625,597,484,987'),
    774: ('totalistic rule', 'average color of neighboring cells', 'not on their individual colors'),
    850: ('colors of all the cells', 'updated in parallel at every step'),
    982: ('fixed array of cells', 'underlying number and organization of cells always stays the same'),
    4684: ('3 possible colors and nearest-neighbor rules', '27 possible 3-cell neighborhoods', 'does not change the color of the center cell'),
    5218: ('7,625,597,484,987 cellular automata with three colors and nearest-neighbor rules', 'just 1800 that are reversible'),
    10984: ('always defined to use the old values of neighbors', 'maintain two copies of the array of cells'),
    11002: ('a 1D cellular automaton rule can be given as a set of explicit replacements for all',),
    11004: ('possible blocks of cells in each neighborhood',),
    11014: ('Transpose[{RotateRight[a], a, RotateLeft[a]}]/. rule',),
    11051: ('general nearest-neighbor rule with k colors',),
    11056: ('k-color nearest-neighbor totalistic rule',),
    11066: ('CellularAutomaton[{n, k},...] is equivalent to CellularAutomaton[{n, {k,',),
    11067: (r'\{k^2, k, 1\}',),
    11164: ('general k=3, r=1 rule with rule number 921408',),
    11168: ('totalistic k=3, r=1 rule with code 867',),
    11897: ('k^{k^{2r+1}}', 'And for k=3, r=1 there are 7,625,597,484,987 rules in all'),
    11898: ('single step in the evolution of a general cellular automaton',),
    11900: ('ListConvolve[k^Range[0, 2r], a, r + 1]', 'IntegerDigits[num, k, k^2r^1]'),
    13513: ('offset lists are always taken to be in the order given by *Sort*', 'in the same order as the offset list'),
    16446: ('every cell is updated in parallel at each step', 'colors of neighboring cells on the previous step'),
    18339: ('three colors and nearest neighbors', 'collection of cases for a rule with two colors'),
    18348: ('Log[2, k^{k^{2r+1}}]', 'minimum possible s for k = 3, r = 1 is about 2.2'),
    20573: ('k = 3, r = 1 rule 5407067979',),
    20577: ('reduced from  $3^{27}$  to  $3^{21}$', 'up to 6 of the 27 cases'),
    20967: ('three-color, 60',),
    21134: ('of three colors by two, 655, 1111',),
    21933: ('three-color, 436',),
}
for line_no, fragments in checks.items():
    line = L[line_no - 1]
    for fragment in fragments:
        assert fragment in line, (line_no, fragment)

k = 3
addresses = {k*k*left + k*center + right
             for left in range(k) for center in range(k) for right in range(k)}
assert addresses == set(range(k**3))
assert [k*k*l + k*c + r for l,c,r in ((0,1,2),(0,2,1),(1,0,2))] == [5,7,11]
assert k**(k**3) == 3**27 == 7_625_597_484_987
assert 'totalistic' not in L[771].lower()
assert 'totalistic' in L[773].lower()
print('T02 verbatim evidence oracle: PASS 32 lines; ordered addresses/count exact')
PY
```

Expected output:

```text
T02 verbatim evidence oracle: PASS 32 lines; ordered addresses/count exact
```

## Construction Model

### Native semantics

| Dimension | Reconstructed T02 semantics |
|---|---|
| State | `STATE = SUPPORT + VALUES`; no control. Support is the same fixed ordered one-dimensional regular lattice as T01. Values form a total field in one declared finite ordered alphabet `A`; strict T02 has `k=|A|>=3`. |
| Alphabet | Colors are distinct values. The ordered rank map `rho:A->{0,...,k-1}` is part of rule-code interpretation but does not make colors arithmetic magnitudes. Palette/tone is representation. |
| Active loci | Every semantic site on every event, with finite causal-window lowering separated exactly as in T01. |
| Read | The ordered old-snapshot triple `(left,self,right)`. Context order is semantic and homogeneous at every site. |
| Rule | One total structural table `T:A^3->A`, containing exactly `k^3` entries. No reducer, symmetry, background default, wildcard, mutation generator, callback, or inverse is implicit. |
| Result/update | One typed same-site `Assign(T(left,self,right))` per site; T01's atomic parallel fixed-effects commit applies all results from the same old field. No new update law. |
| Successor/halting | One deterministic successor per valid field, including unchanged fields; no intrinsic halt, branch, rejection, or randomness. A finite horizon is an observation request. |
| Seed | An independent total initial field. Single-gray, random, uniform, periodic, purpose-encoded, and sparse inputs are profiles, never program identity. |
| Support/realization | Native integer line and explicit finite cycle/segment/causal-window realizations retain T01 meanings. No rule number or color count chooses a boundary. |
| Observers/provenance | Spacetime/raster views, behavior class, reversibility, symmetry/color-relabelling orbit, purpose/optimality, emulation relation, and random table-mutation history remain separate from native state and events. |

### Ordered base-`k` rule codec

For ranked colors `l,c,r in {0,...,k-1}`:

```text
context_index(l,c,r) = k^2*l + k*c + r
output(n,l,c,r)      = floor(n/k^context_index) mod k
code(T)              = sum(T(l,c,r) * k^context_index(l,c,r))
```

- Context index zero is `000`; index `k^3-1` is `(k-1)(k-1)(k-1)`.
- The padded base-`k` display table is ordered from the highest context down to `000`, while the output for `000` is the least-significant digit. This reduces exactly to T01's `4*l+2*c+r` bit codec at `k=2`.
- There are `S=k^3` contexts, `R=k^S=k^(k^3)` total tables, and valid codes are exactly `0..R-1`. Leading zero digits are required table entries.
- Structural `(alphabet,ordered table)` data are primary. The integer is a lossless optional codec tied to the alphabet order. Relabeling colors requires conjugating the table; changing only the palette does not change the program.
- A sparse dot display such as `BOOK:4684` must first expand every dot to the explicit center output. A table mutation is a meta-level edit of exactly one context entry plus optional draw provenance; it is not a stochastic cell event or hidden fallback.
- General `k` requires arbitrary-precision codes: at `k=4`, `R=4^64=2^128`, already beyond signed 64-bit storage. Batches therefore reference structural programs/stable IDs or lossless arbitrary-precision code strings rather than coercing semantic rule codes into `numpy.int64`.

### Variant disposition

| Profile | Semantic relation |
|---|---|
| `k=2` | Exactly the completed T01 specialization; T02 retains catalog traceability for `k>=3` without duplicating execution. |
| `k=3`, all 27-entry tables | Direct strict profile; exact count `3^27=7,625,597,484,987`. |
| General `k`, range one | Direct Notes generalization through `{n,k}` and `k^(k^3)`; same construction. |
| General range `r`, two-cell staggered neighborhoods, or higher dimensions | Supporting general-CA siblings with different read geometry; not smuggled into T02's radius-one identity. |
| Totalistic/weighted rules | Restricted alternate rule descriptions whose meaning depends on numeric color assignment for `k>2`; T03/T04/T05 own them. |
| Blank-preserving or left-right symmetric tables | Validated restrictions over the same tables; T06/T07 own catalog evidence. |
| Reversible tables | Scoped global property/certificate of the induced map, not a native inverse step or trusted Boolean flag. |
| Random table-mutation sequence | Program-generation/provenance experiment producing successive immutable T02 tables, not CA state or RNG-driven cell evolution. |
| Binary block encoding/emulation | Explicit relation between different programs, supports, steps, and decoders; never the native multi-color representation. |
| Universal/purpose-doubling/mobile/Turing/substitution/computer examples | Named T02 program/seed/emulation profiles; their encoded machine, purpose, search work, or behavior is not extra T02 state. |

## Current API Fit

| Construction element | Fit | Evidence and consequence |
|---|---|---|
| `ALPHABET` with `{0,...,K-1}` or symbols | DIRECT | `simple_programs.md:200-230` explicitly includes `K`-color and symbolic states; semantic alphabet order must be preserved. |
| State/trace address | DIRECT with T01 qualification | A finite 1D trace fits `[t,x,0,0]`; finite `SHAPE` remains a realization, not native topology. |
| Independent seed and explicit finite boundary | PARAMETERIZATION | Existing seed/boundary schemas can express finite profiles but must not enter program identity or imply an edge on `Z`. |
| Ordered radius-one current read | DIRECT/PARAMETERIZATION | Relative selectors and the Wolfram source-time convention express old `(left,self,right)` when order is pinned. |
| `EXHAUSTIVE T:A^3->A` | DIRECT conceptually | `simple_programs.md:1795-1829` states the correct structural table, but gives no normative arbitrary-base codec or table validator. |
| Base-`k` rule codec/arbitrary-precision identity | PRINCIPLED EXTENSION | Required by `BOOK:11897-11900`; code depends on alphabet order and exceeds 64 bits for `k>=4`. |
| Typed assignment/parallel commit | DIRECT T01 reuse | Same source, result, conflict-free atomic update, and deterministic successor; no eleventh law. |
| Totalistic/symmetric/background/reversible/mutation/emulation data | NOT APPLICABLE to base execution | These are restrictions, claims, provenance, or relations rather than rule flags. |

## Current Runtime Fit

| Component | Fit | Exact finding |
|---|---|---|
| `alphabets.int_range_alphabet(k)` | DIRECT data primitive | Supplies ordered digit colors `0..k-1` (`src/ca/alphabets.py:42-73`) but `Dynamics` does not carry/validate an alphabet. |
| `alphabets.symbolic(values)` | DIRECT declaration, incomplete execution | Preserves explicit deterministic order (`alphabets.py:145-179`), while rollout coerces spatial fields/reads to `int64`; symbolic execution needs a validated rank/value layer rather than object cells. |
| `neighborhoods.eca()` / loci / frontier | DIRECT T01 geometry for finite realization | Correct ordered radius-one component and full finite slice; native support/observation lowering remain absent. |
| `rules.exhaustive(...,alphabet_size=k)` | SEMANTIC MISMATCH | Declares `state_count=k` regardless of three-read arity (`rules.py:173-195`), so it cannot derive `S=k^3` or `R=k^(k^3)`. |
| `_channel_state` | SEMANTIC MISMATCH | Weights physical ordered reads by `[1,k,k^2]` (`rollout.py:748-760`), reversing the required left-most-significant context index just as T01 found. |
| Spatial rule application | SEMANTIC MISMATCH | Uses binary right shifts and `&1` (`rollout.py:650-682`); it cannot decode base `k`, return general colors, or store a structural table. |
| Generic lookup execution | SEMANTIC MISMATCH | Family whitelists still reject an ordinary `lookup`; no T02 branch may be added. |
| `Rule.rule_id` / `RawEpisode.rule_id` | PARAMETERIZATION only for small codes | Python `int` is arbitrary precision, but batch normalization forces `numpy.int64` (`rollout.py:264-288`) and output contracts use a numeric rule-id array. General T02 requires structural program references/lossless codecs. |
| `Dynamics` / seeds / boundary | PARAMETERIZATION / PRINCIPLED EXTENSION | Finite field mechanics fit, but alphabet, semantic support, typed result/update, table identity, and observation scope are missing. |
| Tests | SEMANTIC MISMATCH as T02 evidence | Current rule/rollout tests cover binary named families and parity only; none checks `k=3`, 27 contexts, base-3 codes, symbolic order, or `>2^63` identities. |

## Principles Audit

- General `k` is directly supported by the Notes rule-count/implementation and `{n,k}` syntax; strict examples concentrate on `k=3`. T02 is therefore the `k>=3`, radius-one slice of the generic finite-alphabet lookup construction.
- Alphabet cardinality parameterizes T01 without changing support, source coverage, reads, result, commit, or successor. Adding a separate update/executor would duplicate semantics.
- A base-`k` integer is a codec for a complete table, not the rule's only in-memory form. Structural tables avoid fixed-width overflow and make validation/serialization inspectable.
- Color rank for the codec, numeric value for totalistic aggregation, and palette tone for rendering are three different responsibilities.
- A sparse mutation label, reversibility claim, behavior classification, purpose search, raster, or binary block encoding cannot replace or feed the mathematical table/field.
- T03/T04/T05 aggregation, T06 quiescence, T07 reflection, and emulation/property analyzers remain compositional siblings rather than T02 flags.

## Exact Semantic Oracle

This dependency-free oracle checks the positional codec, exact rule counts, T01 specialization, a direct non-totalistic ordered-context discriminator, arbitrary-precision pressure, the runnable Notes rule 921408, and the exact rule-5407067979 doubling profile. The finite arrays are causal-window realizations of the source profiles, not native support or rule identity.

```bash
python3 - <<'PY'
from hashlib import sha256

def contexts(k):
    return ((l,c,r) for l in range(k) for c in range(k) for r in range(k))

def address(k,l,c,r):
    return k*k*l+k*c+r

def output(code,k,l,c,r):
    return code//(k**address(k,l,c,r))%k

def table(code,k):
    return tuple(output(code,k,*q) for q in contexts(k))

def encode(outputs,k):
    return sum(value*k**i for i,value in enumerate(outputs))

assert [address(3,*q) for q in contexts(3)]==list(range(27))
assert (address(3,0,1,2),address(3,0,2,1),address(3,1,0,2))==(5,7,11)
assert 3**(3**3)==3**27==7625597484987

# T01 is exactly the k=2 specialization, including context significance.
for code in range(256):
    for l,c,r in contexts(2):
        assert output(code,2,l,c,r)==(code>>(4*l+2*c+r))&1

for code,display in (
    (921408,'000000000000001201210221020'),
    (5407067979,'000000111221211100111212000'),
):
    outputs=table(code,3)
    assert len(outputs)==27 and encode(outputs,3)==code
    assert ''.join(map(str,reversed(outputs)))==display

# Source rule 921408 distinguishes permutations with equal color sum.
assert output(921408,3,0,0,1)==2
assert output(921408,3,0,1,0)==1
assert output(921408,3,1,0,0)==1

# The dot-only mutation baseline expands to the total identity table.
identity=tuple(c for l,c,r in contexts(3))
identity_code=encode(identity,3)
assert identity_code==7479532539765
assert all(output(identity_code,3,l,c,r)==c for l,c,r in contexts(3))
mutated=list(identity)
i=address(3,2,0,1); old=mutated[i]; mutated[i]=(old+1)%3
assert sum(a!=b for a,b in zip(identity,mutated))==1
assert encode(mutated,3)-identity_code==(mutated[i]-old)*3**i

# General k is finite but not fixed-width: R(4)=2^128.
assert 4**(4**3)==2**128
assert 4**64-1>2**63-1

def evolve(code,seed,events):
    pad=events+3
    state=[0]*pad+list(seed)+[0]*pad
    rows=[state]
    for _ in range(events):
        old=rows[-1]
        rows.append([
            output(code,3,old[x-1] if x else 0,old[x],
                   old[x+1] if x+1<len(old) else 0)
            for x in range(len(old))
        ])
    return rows

def nonzero_word(row):
    used=[i for i,v in enumerate(row) if v]
    return ''.join(map(str,row[min(used):max(used)+1])) if used else ''

# BOOK:20573-20574 counts serialized states: 3m-1 states = 3m-2 events.
for m in range(1,33):
    rows=evolve(5407067979,[1]*(m-1)+[2],3*m-2)
    assert len(rows)==3*m-1
    assert nonzero_word(rows[-1])=='1'*(2*m)
trace=[nonzero_word(r) for r in evolve(5407067979,[1,1,2],7)]
assert trace==['112','1211','2201','1012','20211','11101','11102','111111']

# Exact 100-update causal window for the source's rule-921408 invocation.
rows=evolve(921408,[1],100)
crop=[row[3:204] for row in rows]  # width 201 around the centered seed
blob=bytes(v for row in crop for v in row)
assert len(crop)==101 and all(len(row)==201 for row in crop)
assert tuple(blob.count(v) for v in range(3))==(17840,1568,893)
assert sha256(blob).hexdigest()=='935f360febe2e58653bd52dff57139563bc706af963b2bdfbe0b116a7dbcacc3'

print('T02 semantic oracle: PASS')
print('rule_count_k3=',3**27)
print('rule_921408_display=', ''.join(map(str,reversed(table(921408,3)))))
print('rule_5407067979_display=', ''.join(map(str,reversed(table(5407067979,3)))))
print('identity_code_k3=',identity_code)
print('rule_5407067979_m3_trace=',','.join(trace))
print('rule_921408_counts=',tuple(blob.count(v) for v in range(3)))
print('rule_921408_sha256=',sha256(blob).hexdigest())
PY
```

Recorded output:

```text
T02 semantic oracle: PASS
rule_count_k3= 7625597484987
rule_921408_display= 000000000000001201210221020
rule_5407067979_display= 000000111221211100111212000
identity_code_k3= 7479532539765
rule_5407067979_m3_trace= 112,1211,2201,1012,20211,11101,11102,111111
rule_921408_counts= (17840, 1568, 893)
rule_921408_sha256= 935f360febe2e58653bd52dff57139563bc706af963b2bdfbe0b116a7dbcacc3
```

## Detailed Implementation Plan

1. Complete controlled searches and exact line manifests across strict, Notes, actual Index, splits, aliases, formulas, variants, applications, and emulation routes.
2. Record every unique construction-relevant excerpt verbatim and disposition every candidate.
3. Audit every relevant asset and exact/source-permitted semantic or raster oracle.
4. Reconstruct table ordering/code, state/update/successor/boundary/seed semantics and variants before evaluating reuse.
5. Audit current API/runtime/tests and completed decisions for exact reuse versus extension.
6. Write concrete Goal 2 files/tests and no-cheating gates; independently review and integrate all global ledgers.

## Goal 2 Implementation Stage

### G2-T02 — General finite-alphabet nearest-neighbor tables

**Objective:** broaden the T01 foundation once so `k=2` elementary and `k>=3` T02 programs share the same finite-alphabet ordered-table executor, exact positional codec, support lowering, typed assignment, and atomic update. A discoverable T02 preset returns an ordinary shared spec; it never dispatches on `multicolor`.

**Dependencies:** synthesis-selected T01 fixed-support/all-sites/assignment/update semantics; T34's lossless exact nonnegative-integer/decimal-string serialization responsibility; explicit finite ordered alphabets and stable program references. No T02-specific executor or new update law is required.

**Concrete files and changes:**

1. Extend `src/ca/alphabets.py` so an immutable ordered alphabet exposes validated `rank(value)`/`value(rank)` mappings and membership. Retain `int_range_alphabet(k,0)` as the canonical source color order; do not infer order from a palette or host set.
2. Add a synthesis-named `src/ca/rule_tables.py` containing immutable `ExhaustiveTable(alphabet_id,ordered_offsets,outputs)` and a versioned Wolfram positional codec. Validate exactly `k^3` outputs, all in the alphabet, fixed leading zeros, code range, and lossless arbitrary-precision encode/decode.
3. Refine `src/ca/rules.py`: exhaustive inputs know alphabet and arity; program identity contains the decoded structural table. A numeric code is codec/provenance data, not bit-shift execution state.
4. Replace named-family spatial dispatch in `src/ca/rollout.py` or the synthesis-selected executor with the generic T01/T02 protocol: gather one old snapshot, rank reads in declared order, table-gather outputs, emit typed assignments, and commit simultaneously. Scalar/batch execution shares this code and never stores semantic program codes in fixed-width NumPy shifts.
5. Extend `src/ca/specs.py` and the support/lowering module with alphabet, native fixed ordered support, `AllSites`, typed update, explicit cycle/segment/causal-window realization, evolving constant/repeating initial backgrounds, event/snapshot counts, and observation crop metadata.
6. Add `src/ca/presets/nearest_neighbor.py`: `elementary(n)` validates `k=2`; `multicolor_nearest_neighbor(k,code_or_table)` validates `k>=3`; both construct the same generic spec. Seed, horizon, boundary, palette, and mutation provenance remain run/view inputs.
7. Add pure rule-table transforms/provenance only where synthesis selects them: reflection/color relabelling, explicit one-entry edits, and scoped reversibility claims. Do not add backwards rollout or trust a Boolean reversible flag.
8. Update trace/export codecs to use stable program references and tagged decimal-string big integers. A viewer may use categorical palettes and sparse dot displays downstream, with explicit expansion back to a total table.
9. Add `tests/test_rule_tables.py`, `tests/test_t02_multicolor_ca.py`, and shared support/executor/codec fixtures; preserve all T01 asymmetric and current tests.

**Required conformance tests:**

1. Assert `S=k^3`, `R=k^S`, `R(3)=7,625,597,484,987`, exact valid ranges, fixed table lengths/leading zeros, and rejection of booleans, invalid `k`, out-of-alphabet outputs, `-1`, and `R`.
2. For every T01 code and all eight contexts, prove the generic `k=2` codec equals `(n>>(4*l+2*c+r))&1`. T02's preset rejects `k=2` while the shared construction accepts it.
3. Round-trip codes/tables `0`, `1`, `921408`, `5407067979`, `R-1`, deterministic sampled `k=3/4` cases, and a valid `k=4` code above `2^63-1` through structural, decimal-string, and JSON-safe records without NumPy/float loss.
4. Pin all 27 outputs and descending display digits of rules 921408 and 5407067979. Equal-sum contexts `(001,010,100)` must remain distinguishable; a mirrored context codec fails.
5. Reproduce the exact rule-5407067979 doubling trace for multiple `m`, including the eight `m=3` serialized states; require `3m-2` events and `3m-1` states.
6. Reproduce the 101-by-201 rule-921408 causal-window state digest/counts above and the source-permitted image oracle if retained by the asset audit.
7. Expand the all-dot mutation baseline to the exact identity table/code, apply one explicit entry edit, and prove only that context changes. Missing rows without an explicit display default are invalid.
8. Use a table with output color `2`, one with `T(000)!=0`, and an old-snapshot adversary to prove base-`k` output, evolving background, and atomic parallel semantics rather than binary masking, fixed-zero clamping, or in-place mutation.
9. Run one table with centered, explicit cyclic, finite-block-on-constant, and finite-block-on-repeating initial fields. Program identity stays fixed; run/realization identity changes. Compare exact causal crops against a larger halo.
10. Accept asymmetric, non-quiescent, non-totalistic tables in base T02. Validate totalistic/quiescent/symmetric restrictions only through their own explicit analyzers/presets; never require them for execution.
11. Inspect the resolved T01/T02 specs and executor: no callback, family branch, partial-row fallback, hidden seed/background/palette/mutation schedule, binary block encoding, right-shift decoder, fixed-width code, or artificial maximum `k`.
12. Preserve the full repository suite and exact finite `[t,x,0,0]` trace round-trips without weakening tests.

**Completion evidence:** generic table execution passes all binary and nonbinary adversaries; source codes/oracles reproduce; big codes round-trip losslessly; all seeds/support realizations remain explicit; static inspection finds no T01/T02 branch, callback, binary emulation, hidden default, or fixed-width identity; current tests pass unchanged.

## No-Cheating Checks

- No T02 family branch, binary packing/emulation, totalistic reduction, callback, sparse default hidden in the executor, or raster-decoded rule.
- No binary-only rule cardinality/bit-order helper advertised as general `k` support.
- No view tone or integer digit arithmetic substituted for symbolic color identity.
- No seed/background/boundary/reversibility restriction silently fused into the base rule.
- No finite figure width/horizon presented as native lattice capacity or halt.
- No `right_shift`, `&1`, float, JSON number, or `numpy.int64` path used as general rule-code identity.
- No frozen initial constant/repeating background: arbitrary tables may evolve the entire background.
- No artificial maximum `k`; inability to materialize a requested finite table is a typed resource outcome.

## Completion Requirements

- [ ] Every strict/Notes/split/actual-Index/alias/variant/application/emulation textual candidate is dispositioned with reproducible searches.
- [ ] All relevant assets and source-permitted semantic/raster oracles are closed with hashes, geometry, labels, repairs, and exclusions.
- [ ] Exact state/alphabet/table/code/read/update/successor/boundary/seed semantics and variants are explicit.
- [ ] T01/T03/T04/T06/T07/reversible/emulation boundaries and current API/runtime fit are proved.
- [ ] Goal 2 files/dependencies/tests and no-cheating gates are implementation-ready.
- [ ] Global plan/evidence/design ledgers, independent review, diff checks, and repository tests are integrated.

## Stage Results

In progress. Initial direct evidence supports a three-color ordered 27-entry lookup as the same forward construction shape as T01, but neither exhaustive search closure nor general-`k` status is yet proved.

## Integration Results

In progress. No completed stage is contradicted or reopened. T01 parameterization is a hypothesis under active evidence audit; the public transition-update family remains at ten members.
