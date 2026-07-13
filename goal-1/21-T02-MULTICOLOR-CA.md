# 21-T02-MULTICOLOR-CA

Status: **REOPENED — ARCHITECTURE AUDIT; EVIDENCE CLOSED**

Architecture authority: the T02 row and runner contract in `architecture-audit.md` supersede any executor/class claims below; evidence, construction facts, and conformance fixtures remain authoritative.

The evidence/search closure and conformance fixtures remain valid. Composite finite alphabets and semantic-table versus rank-codec identity are being reintegrated without a T02-specific runtime class.

## Current Facts

- Exact catalog row: T02, CSV line 3, `Multi-Color Nearest-Neighbor Cellular Automata`; taxonomy vocabulary is `ref/notes/CA-Types.md:45-66` and remains a search/API seed rather than book evidence.
- The strict Chapter 3 transition at `BOOK:770-776` directly states three colors, the exact count `7,625,597,484,987`, and the ordered-neighborhood/totalistic contrast. Most immediately following examples are totalistic and belong primarily to T03/T04, so their rule aggregation cannot be imported into T02.
- `BOOK:4684` directly describes arbitrary three-color nearest-neighbor tables over all 27 ordered three-cell neighborhoods and a mutation profile that adds or changes individual neighborhood entries.
- `BOOK:5218-5222` directly identifies all `3^27` three-color nearest-neighbor rules and the 1,800 reversible members. Reversibility is a property/restriction, not a different forward update construction.
- T01 already establishes a fixed ordered one-dimensional lattice, total field, synchronous old left/self/right reads, arbitrary finite lookup, typed same-site assignment, atomic parallel commit, and separate native/finite support, seed, trace, and view identities.
- The completed evidence chain proves that T02 is exactly T01 parameterized by a finite ordered alphabet of cardinality `k>=3` plus a complete ordered table and optional base-`k` codec. No new state, read, result, update, successor, executor, or halt primitive is required.
- Current runtime alphabet declarations can represent finite integer/symbolic colors, but the documented/executable exhaustive binary codec and family-dispatched rollout were already defective for T01. Existing nominal color capacity is not proof of an executable general `k^(k^3)` rule table.

## Updated Assumptions

- Treat `k=3` as the strict directly enumerated profile and general `k>=3`, range one, as the directly audited Notes generalization. `k=2` remains T01; general range, dimension, and alternate neighborhood geometry remain separate parameterizations/stages.
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

### E19 — An ordered priority rule still denotes a complete table

- Provenance: `BOOK:15493-15495`, discrete-Voronoi Notes.
- Establishes: a direct `k=3,r=1` instance may be written compactly as ordered overlapping patterns. Expanding priority produces one ordinary complete 27-entry T02 table; the derived Voronoi behavior is an application, not a new update construction.

> `■ **Discrete Voronoi diagrams.** The k = 3, r = 1 cellular automaton`

> ` $\{\{0 \mid 1, n : (0 \mid 1), 0 \mid 1\} \rightarrow n, \{\_, 0, \_\} \rightarrow 2, \{\_, n\_, \_\} \rightarrow n-1\}$ is an example of a system that generates discrete 1D Voronoi diagrams by having regions that grow from every initial black cell, but stop whenever they meet, as shown below.`

### E20 — Actual-Index routes add no new mechanics

- Provenance: actual Index `BOOK:20965,20967,21134,21187,21323,21542,21933,22372`.
- Establishes: the Index routes more-color, three-color, encoding/emulation, and reversible-three-color vocabulary back to the inspected main/Notes passages. These are routing evidence only.

> “with more colors, 107”

> “three-color, 60”

> “of three colors by two, 655, 1111”

> “multicolor encodings, 1111”

> “emulating multicolor, 1115”

> “three-color, 436”

> “emulating more colors, 669, 1113,”

### E21 — Explicit sibling and neighborhood boundaries

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
12. **Actual Index:** the real Index begins at `BOOK:20826`. E20 pointers corroborate routing only and are not counted as independent construction evidence.
13. **Official-PDF normalization authority:** the official Chapter 3 PDF, [`nks-ch3.pdf`](https://files.wolframcdn.com/pub/www.wolframscience.com/nks/nks-ch3.pdf), was verified at SHA-256 `d4005b27774084c276e67d46a6c79106b93b785d4329893080223c9da8263e76`. Its printed page 886 visibly confirms the normalized general count `R = k^(k^(2r+1))`, the `ListConvolve[k^Range[0,2r], ...]` lookup, and `IntegerDigits[num,k,k^(2r+1)]`. The official all-Notes PDF, [`nks-notes.pdf`](https://files.wolframcdn.com/pub/www.wolframscience.com/nks/nks-notes.pdf), was verified at SHA-256 `549f043595653a7d276b07ba52d435700039b71427b4e1774a44b1a58eff4723`; its printed page 867 visibly confirms the `{n,k}` equivalence with positional weights `{k^2,k,1}`. These normalized forms repair E11/E14 but are deliberately not presented as verbatim `BOOK` blockquotes.
14. **Priority-pattern expansion:** the direct `BOOK:15493-15495` Voronoi rule uses overlapping Wolfram-language patterns in written priority order. It is source-level shorthand for a total table, not a callback or sparse fallback. Expansion yields descending base-3 digits `111000222111011200111011200` and code `3681845932419`; initial black-cell positions, figure horizon, grid transfer, and the right-hand Voronoi observer remain unstated view/run data.

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
    15493: ('Discrete Voronoi diagrams.', 'k = 3, r = 1 cellular automaton'),
    15495: ('generates discrete 1D Voronoi diagrams', 'grow from every initial black cell'),
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
assert 'total number of possible rules of this kind' in L[771]
assert 'The idea of a totalistic rule' in L[773]
print('T02 verbatim evidence oracle: PASS 34 lines; ordered addresses/count exact')
PY
```

Expected output:

```text
T02 verbatim evidence oracle: PASS 34 lines; ordered addresses/count exact
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

## Corrected Architecture and Goal 2 Handoff

T02 is a parameterization of the same CA preset by an arbitrary explicit finite ALPHABET, including product/tagged cells. The semantic RULE is the complete label table; rank and Wolfram integer code are lossless codec/provenance maps. No executor, update, or alphabet subclass per semantic role is introduced.

Revised G2-T02 generalizes finite alphabet/table validation and bigint codecs, preserves the exact rank/code oracles, and ensures composite alphabets can flow through the T01 axes. Existing evidence and tests remain authoritative.

## Historical Current API Fit (Superseded only on composite-alphabet/identity wording)

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

## Historical Current Runtime Fit (Evidence Retained)

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

## Historical Principles Audit (Superseded only on architecture wording)

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

## Asset and Raster Audit

The strict Chapter 3 transition has no full-table T02 picture. Its immediately following page-60/page-61 assets are totalistic and are material exclusions. The bounded included set instead consists of the direct discrete-Voronoi ordered-rule fixture, one exact general-rule Notes fixture, the purpose/search and mutation galleries, the reversible gallery and its inverse-range Notes panels, and one supporting purpose-search asset. Visual tone is never imported into the color algebra.

### Included asset manifest

| Asset path under `ref/A-New-Kind-of-Science/` | Bytes | Dimensions | SHA-256 | Source-permitted meaning |
|---|---:|---:|---|---|
| `BACK-MATTER/Index/Images/_page_1002_Picture_14.jpeg` | 16,254 | `581x97` | `c06ceb9699771663ab0e993ea17a5c3bf471bfca0328da88b83780dc61d619b0` | Direct `k=3,r=1` discrete-Voronoi fixture for the ordered three-clause rule at `BOOK:15493-15497`. Its left panel is a qualitative CA spacetime view and its right panel a Voronoi observer; exact seeds, horizon, boundary, grid transfer, and palette-to-digit map are not stated. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_23.jpeg` | 4,478 | `160x117` | `132528352f363e52a20e73e1e8341203126448c0c6c8545eed48626eaddac16c` | Exact Notes invocation of general `k=3,r=1` rule `921408`, point `1` on repeating-`0` background, 100 updates. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_847_Figure_1.jpeg` | 111,064 | `1041x385` | `2d36e7eaeb3b073e68621ef5f9c1c397ae24ddc74fe06f26e62546ccc3af2902` | Six-, four-, and three-color nearest-neighbor doubling constructions; case (c) is rule `5407067979`. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_848_Figure_2.jpeg` | 247,033 | `1194x1308` | `0bfecfeff1bd81072838e39704fc6572632dee083f91ddc4370909b0e2c5b5dd` | Full three-color rule examples drawn from the `4,277` doubling rules found among all `3^27`; printed numbers are rule labels, not observer IDs. |
| `CHAPTERS/8-Implications-for-Everyday-Systems/Images/_page_406_Picture_1.jpeg` | 200,732 | `1179x968` | `08c35506c17c24d45a9b00de910ea13674ee087fdaf827464e40bae81ba2fe23` | Three-color radius-one one-entry mutation sequence. Each label has 27 positions; a dot means retain the old center color. Exact random choices/tables are absent, so this is a disposition/provenance fixture rather than a golden trajectory. |
| `CHAPTERS/9-Fundamental-Physics/Images/_page_451_Picture_6.jpeg` | 187,275 | `1103x483` | `e7bbbefb729e76dd5d080d0b841a485ece898d9c3197780b4871c742d61a4e89` | Six reversible full-rule panels labelled `270361043509`, `277206003607`, `1123289366095`, `1123956776897`, `3097483878567`, and `3681848058291`. |
| `BACK-MATTER/Index/Images/_page_1032_Picture_10.jpeg` | 4,216 | `142x122` | `4a40921d9eb75316d5294c8cd22cefcd8649d12ffec3d5eb4df414835fbcf4ae` | Rule `2828556973047`; first of the inverse-neighborhood examples. |
| `BACK-MATTER/Index/Images/_page_1032_Picture_11.jpeg` | 3,016 | `117x125` | `2b6326f90f10d4f887be2cfeb69ec6f7712a72572868dd0a49fe0dd407ce6093` | Rule `3762560660157`; second inverse-neighborhood example. |
| `BACK-MATTER/Index/Images/_page_1032_Picture_12.jpeg` | 5,648 | `125x143` | `436feb4ebafa0c946142e22a2c45011d84ce23f0000e75e6cb5143969efba69c` | Rule `538556225233`; third inverse-neighborhood example. |
| `BACK-MATTER/Index/Images/_page_1032_Picture_13.jpeg` | 4,424 | `128x143` | `0ca11e29343741d99227175123d39260b87854891cb81be88e1df96ff12c64e7` | Rule `3066231781977`; fourth inverse-neighborhood example. |
| `BACK-MATTER/Colophon/Images/_page_1201_Picture_4.jpeg` | 18,451 | `386x261` | `5ce5638ca129527ea5c5fc2c7e2fe7e204c8af5fbf7349d3da60f445634292b7` | Supporting Notes panels labelled `304911688608`, `308527554123`, `1183925790477`, `2672802162657`; the first three yield `3n`, the last `2n-2`. Exact input/horizon is not restated there, so it is not a trajectory golden. |

Page 847/Notes count the source's `3n-1` displayed states for rule `5407067979`: executable first arrival is `3n-2` transition events. The existing exact semantic oracle preserves this event/state distinction.

For the Voronoi fixture, the three clauses are priority ordered. The first keeps the center only when all three inputs lie in `{0,1}`; the second applies to the remaining center-`0` contexts; the third applies to everything else. Once expanded, this is an ordinary total 27-entry T02 lookup, not a runtime callback or sparse fallback. The source's “initial black cell” is qualitative palette language: it does not identify the seed digit or fully specify the illustrated run/view, so the figure is not a trajectory or raster golden.

### Explicit exclusions and relation-only dispositions

| Asset path under `ref/A-New-Kind-of-Science/` | Bytes | Dimensions | SHA-256 | Disposition |
|---|---:|---:|---|---|
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_75_Figure_6.jpeg` | 51,178 | `610x446` | `acb13963632286960ca61b616ff2f45a940750f3ab7deb5e6fbf696543015c15` | Totalistic code `777`; T04 material exclusion. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_76_Figure_2.jpeg` | 174,691 | `1109x1279` | `8c11659c8bd63d37a972c5ffab376b62948f7c4e05f9fd10f239e51464f4084d` | Three-color totalistic gallery; T04 material exclusion. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_25.jpeg` | 5,511 | `211x117` | `d53637ce9ec50330d5fa6239b23f48d57b563266a0085a23517d4538020fd5fb` | Directly adjacent but explicitly totalistic `k=3` code `867`; not the general-rule fixture. |
| `CHAPTERS/11-The-Notion-of-Computation/Images/_page_670_Figure_1.jpeg` | 281,966 | `1064x1224` | `a1a2a5c04b509ecc0357273387b2950d179478c65406427751904987ec9e8d3e` | Totalistic code `1599` encoded into a binary larger-neighborhood CA; emulation relation, not a T02 transition golden. |
| `CHAPTERS/11-The-Notion-of-Computation/Images/_page_707_Figure_1.jpeg` | 327,160 | `1130x1111` | `974e12d28e8acc6fb4af26f7b1dd09eae1f30d802666a61f41abed8ec2d42e19` | Mixed gallery: ECA 110, second-order 37, two-color range-two totalistic 52, and three-color totalistic 1815. |
| `BACK-MATTER/Index/Images/_page_1002_Picture_16.jpeg` | 17,313 | `576x114` | `297f7bd1bd904418960e0ab9af4d4db98dd6eafef4005c929f872a1d23937b7a` | Directly adjacent but explicitly an analogous **2D** cellular automaton; it is not the one-dimensional ordered-triple T02 rule or an additional view of Picture 14. |
| `CHAPTERS/11-The-Notion-of-Computation/Images/_page_675_Figure_1.jpeg` | 231,351 | `987x946` | `fd5d18341f9bb6067319739ea18d34467bc3ef5a568a280ecbc8cb693204f38b` | Valid 28-color nearest-neighbor instance, but its subject is sequential-substitution emulation and its full table/settings are absent; relation-only. |
| `CHAPTERS/11-The-Notion-of-Computation/Images/_page_677_Figure_2.jpeg` | 173,594 | `1033x1034` | `8a59e423d080cdcfd5fbeb61170c099dc6ec904702e27385627427d56373f543` | Valid five-color nearest-neighbor instance, but its subject is logic-circuit emulation and its full table/settings are absent; relation-only. |

The monolith omits `Images/` from links. `_page_883_Picture_23.jpeg` is Notes-for-Chapter-2 evidence despite its Chapter-12 filesystem placement; the four page-1032 Notes assets are under `Index/Images`; the page-1201 Notes asset is under `Colophon/Images`. The split/misrouted copies are duplicate references to these same bytes, not extra evidence or assets.

The following dependency-free metadata oracle parses JPEG SOF markers directly and pins every included, excluded, and relation-only file:

```bash
python3 - <<'PY'
from hashlib import sha256
from pathlib import Path

ROOT=Path('ref/A-New-Kind-of-Science')
items={
'BACK-MATTER/Index/Images/_page_1002_Picture_14.jpeg':(16254,581,97,'c06ceb9699771663ab0e993ea17a5c3bf471bfca0328da88b83780dc61d619b0','I'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_23.jpeg':(4478,160,117,'132528352f363e52a20e73e1e8341203126448c0c6c8545eed48626eaddac16c','I'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_847_Figure_1.jpeg':(111064,1041,385,'2d36e7eaeb3b073e68621ef5f9c1c397ae24ddc74fe06f26e62546ccc3af2902','I'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_848_Figure_2.jpeg':(247033,1194,1308,'0bfecfeff1bd81072838e39704fc6572632dee083f91ddc4370909b0e2c5b5dd','I'),
'CHAPTERS/8-Implications-for-Everyday-Systems/Images/_page_406_Picture_1.jpeg':(200732,1179,968,'08c35506c17c24d45a9b00de910ea13674ee087fdaf827464e40bae81ba2fe23','I'),
'CHAPTERS/9-Fundamental-Physics/Images/_page_451_Picture_6.jpeg':(187275,1103,483,'e7bbbefb729e76dd5d080d0b841a485ece898d9c3197780b4871c742d61a4e89','I'),
'BACK-MATTER/Index/Images/_page_1032_Picture_10.jpeg':(4216,142,122,'4a40921d9eb75316d5294c8cd22cefcd8649d12ffec3d5eb4df414835fbcf4ae','I'),
'BACK-MATTER/Index/Images/_page_1032_Picture_11.jpeg':(3016,117,125,'2b6326f90f10d4f887be2cfeb69ec6f7712a72572868dd0a49fe0dd407ce6093','I'),
'BACK-MATTER/Index/Images/_page_1032_Picture_12.jpeg':(5648,125,143,'436feb4ebafa0c946142e22a2c45011d84ce23f0000e75e6cb5143969efba69c','I'),
'BACK-MATTER/Index/Images/_page_1032_Picture_13.jpeg':(4424,128,143,'0ca11e29343741d99227175123d39260b87854891cb81be88e1df96ff12c64e7','I'),
'BACK-MATTER/Colophon/Images/_page_1201_Picture_4.jpeg':(18451,386,261,'5ce5638ca129527ea5c5fc2c7e2fe7e204c8af5fbf7349d3da60f445634292b7','I'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_75_Figure_6.jpeg':(51178,610,446,'acb13963632286960ca61b616ff2f45a940750f3ab7deb5e6fbf696543015c15','X'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_76_Figure_2.jpeg':(174691,1109,1279,'8c11659c8bd63d37a972c5ffab376b62948f7c4e05f9fd10f239e51464f4084d','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_25.jpeg':(5511,211,117,'d53637ce9ec50330d5fa6239b23f48d57b563266a0085a23517d4538020fd5fb','X'),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_670_Figure_1.jpeg':(281966,1064,1224,'a1a2a5c04b509ecc0357273387b2950d179478c65406427751904987ec9e8d3e','X'),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_707_Figure_1.jpeg':(327160,1130,1111,'974e12d28e8acc6fb4af26f7b1dd09eae1f30d802666a61f41abed8ec2d42e19','X'),
'BACK-MATTER/Index/Images/_page_1002_Picture_16.jpeg':(17313,576,114,'297f7bd1bd904418960e0ab9af4d4db98dd6eafef4005c929f872a1d23937b7a','X'),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_675_Figure_1.jpeg':(231351,987,946,'fd5d18341f9bb6067319739ea18d34467bc3ef5a568a280ecbc8cb693204f38b','R'),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_677_Figure_2.jpeg':(173594,1033,1034,'8a59e423d080cdcfd5fbeb61170c099dc6ec904702e27385627427d56373f543','R'),
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
        if marker in {0x00,0x01} or 0xd0<=marker<=0xd9:
            continue
        size=int.from_bytes(data[i:i+2],'big')
        if marker in sof:
            h=int.from_bytes(data[i+3:i+5],'big')
            w=int.from_bytes(data[i+5:i+7],'big')
            return w,h
        i+=size
    raise AssertionError('JPEG SOF marker not found')

counts={'I':0,'X':0,'R':0}
for name,(size,w,h,digest,kind) in items.items():
    path=ROOT/name; data=path.read_bytes()
    assert (len(data),*jpeg_size(data),sha256(data).hexdigest())==(size,w,h,digest)
    counts[kind]+=1
assert counts=={'I':11,'X':6,'R':2}
print('T02 metadata oracle: PASS 11 included; 6 excluded; 2 relation-only')
PY
```

Recorded output:

```text
T02 metadata oracle: PASS 11 included; 6 excluded; 2 relation-only
```

The direct Voronoi rule has its own dependency-free priority-expansion oracle. `product(range(3), repeat=3)` enumerates `(left,self,right)` in increasing T02 address order `9*left+3*self+right`. The branch counts prove that all 27 contexts are covered exactly once after priority shadowing; in particular, the first clause must win over the center-`0` clause on contexts drawn wholly from `{0,1}`.

```bash
python3 - <<'PY'
from collections import Counter
from itertools import product

def source_rule(left,self,right):
    if left in (0,1) and self in (0,1) and right in (0,1):
        return self,'keep-01'
    if self==0:
        return 2,'remaining-zero'
    return self-1,'decrement'

contexts=list(product(range(3),repeat=3))
assert [9*l+3*c+r for l,c,r in contexts]==list(range(27))
resolved=[source_rule(*context) for context in contexts]
table=tuple(value for value,_ in resolved)
assert table==(0,0,2,1,1,0,1,1,1,
              0,0,2,1,1,0,1,1,1,
              2,2,2,0,0,0,1,1,1)
assert Counter(branch for _,branch in resolved)=={
    'keep-01':8,'remaining-zero':5,'decrement':14}
code=sum(value*3**address for address,value in enumerate(table))
display=''.join(map(str,reversed(table)))
assert code==3681845932419
assert display=='111000222111011200111011200'
print('voronoi_rule_code=',code)
print('voronoi_rule_display=',display)
print('voronoi_priority_branches=',(8,5,14))
print('T02 Voronoi priority oracle: PASS 27 total entries')
PY
```

Recorded output:

```text
voronoi_rule_code= 3681845932419
voronoi_rule_display= 111000222111011200111011200
voronoi_priority_branches= (8, 5, 14)
T02 Voronoi priority oracle: PASS 27 total entries
```

The printed reversible and inverse-range labels also have an independent, dependency-free semantic check. The Notes state that cyclic words through length nine suffice for `k=3,r=1`; the same finite domain recovers the four printed inverse-window sizes. A window `start` is relative to the predecessor cell whose value is reconstructed.

```bash
python3 - <<'PY'
from itertools import product

main=[270361043509,277206003607,1123289366095,
      1123956776897,3097483878567,3681848058291]
notes=[2828556973047,3762560660157,538556225233,3066231781977]

def table(code):
    out=[]
    for _ in range(27): out.append(code%3); code//=3
    assert code==0
    return out

def step(rule,state):
    n=len(state)
    return tuple(rule[9*state[(i-1)%n]+3*state[i]+state[(i+1)%n]]
                 for i in range(n))

for code in main+notes:
    rule=table(code)
    for n in range(1,10):
        assert len({step(rule,a) for a in product(range(3),repeat=n)})==3**n

def inverse_window(code):
    rule=table(code); n=9
    pairs=[(a,step(rule,a)) for a in product(range(3),repeat=n)]
    for width in range(1,7):
        for start in range(-6,7):
            seen={}; valid=True
            for old,new in pairs:
                for i,value in enumerate(old):
                    key=tuple(new[(i+start+j)%n] for j in range(width))
                    prior=seen.setdefault(key,value)
                    if prior!=value:
                        valid=False; break
                if not valid: break
            if valid: return width,start,len(seen)
    raise AssertionError(code)

windows=[inverse_window(code) for code in notes]
assert windows==[(3,1,27),(4,-1,81),(5,-2,243),(6,-2,729)]
print('reversible_label_codes=',len(main+notes))
print('inverse_windows=',windows)
print('T02 reversible-label oracle: PASS')
PY
```

Recorded output:

```text
reversible_label_codes= 10
inverse_windows= [(3, 1, 27), (4, -1, 81), (5, -2, 243), (6, -2, 729)]
T02 reversible-label oracle: PASS
```

### Official-source repair provenance

The official primary [all-notes PDF](https://files.wolframcdn.com/pub/www.wolframscience.com/nks/nks-notes.pdf) was used only to repair extraction damage and confirm image labels. PDF page 20 / printed page 868 confirms the exact rule-`921408` invocation and 100-update request. PDF page 135 / printed page 987 confirms the ordered discrete-Voronoi rule and the paired 1D illustration. PDF page 164 / printed page 1017 repairs `BOOK:16025` and the misrouted Index duplicate: the four rule labels are `2828556973047`, `3762560660157`, `538556225233`, `3066231781977`, and the examples are ordered by inverse neighborhood sizes `3,4,5,6`; the local repeated-`3` text is OCR corruption. PDF pages 330-331 / printed pages 1185-1186 confirm rule `5407067979`, the displayed-state count, and the four page-1201 labels. No web source changes native mechanics or supplies an unstated initial condition.

### Direct rule-921408 raster oracle

This is the sole source-permitted raster golden. It reconstructs the exact LSB-first base-3 table, 101 initial-inclusive states, and the actual 151-column nonzero support. The JPEG comparison uses half-open crop `(22,22,145,101)`, state-to-darkness values `0,128,255`, and bicubic resize from `151x101` to `123x79`. Tone and resampling are observer conventions only.

```bash
python3 - <<'PY'
from math import sqrt
from pathlib import Path
from PIL import Image

path=Path('ref/A-New-Kind-of-Science/CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_23.jpeg')
code=921408
rule=[]
for _ in range(27):
    rule.append(code%3); code//=3
assert code==0

state=[0]*201; state[100]=1; history=[]
for _ in range(101):
    history.append(state)
    state=[rule[9*(state[i-1] if i else 0)+3*state[i]
                +(state[i+1] if i+1<len(state) else 0)]
           for i in range(201)]
used=[i for row in history for i,value in enumerate(row) if value]
assert (min(used),max(used))==(50,200)
history=[row[50:201] for row in history]

expected=Image.new('L',(151,101))
expected.putdata([0 if v==0 else 128 if v==1 else 255
                  for row in history for v in row])
expected=list(expected.resize((123,79),Image.Resampling.BICUBIC).getdata())
observed=[255-v for v in Image.open(path).convert('L')
          .crop((22,22,145,101)).getdata()]
n=len(observed); sa=sum(observed); sb=sum(expected)
saa=sum(v*v for v in observed); sbb=sum(v*v for v in expected)
sab=sum(a*b for a,b in zip(observed,expected))
r=(n*sab-sa*sb)/sqrt((n*saa-sa*sa)*(n*sbb-sb*sb))
mae=sum(abs(a-b) for a,b in zip(observed,expected))/n
rmse=sqrt(sum((a-b)**2 for a,b in zip(observed,expected))/n)
print(f'rule921408: r={r:.12f}; mae={mae:.9f}; rmse={rmse:.9f}; crop=123x79')
assert r>=.985 and mae<=5.0 and rmse<=9.0
print('T02 direct raster oracle: PASS')
PY
```

Recorded output:

```text
rule921408: r=0.989621884093; mae=4.113100751; rmse=8.052767980; crop=123x79
T02 direct raster oracle: PASS
```

The discrete-Voronoi, mutation, reversible, doubling-search, inverse-range, and emulation images do not state enough renderer settings, exact initial arrays, random choices, full tables, or observer transforms for additional pixel goldens. Their permitted roles are exact table semantics where supplied, plus identity, property, provenance, and relation evidence only.

## Historical Detailed Implementation Plan (Superseded only on architecture wording)

1. Complete controlled searches and exact line manifests across strict, Notes, actual Index, splits, aliases, formulas, variants, applications, and emulation routes.
2. Record every unique construction-relevant excerpt verbatim and disposition every candidate.
3. Audit every relevant asset and exact/source-permitted semantic or raster oracle.
4. Reconstruct table ordering/code, state/update/successor/boundary/seed semantics and variants before evaluating reuse.
5. Audit current API/runtime/tests and completed decisions for exact reuse versus extension.
6. Write concrete Goal 2 files/tests and no-cheating gates; independently review and integrate all global ledgers.

## Historical Goal 2 Implementation Stage (Superseded by Corrected Handoff)

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

- [x] Every strict/Notes/split/actual-Index/alias/variant/application/emulation textual candidate is dispositioned with reproducible searches.
- [x] All relevant assets and source-permitted semantic/raster oracles are closed with hashes, geometry, labels, repairs, and exclusions.
- [x] Exact state/alphabet/table/code/read/update/successor/boundary/seed semantics and variants are explicit.
- [x] T01/T03/T04/T06/T07/reversible/emulation boundaries and current API/runtime fit are proved.
- [x] Goal 2 files/dependencies/tests and no-cheating gates are implementation-ready.
- [x] Global plan/evidence/design ledgers, independent review, diff checks, and repository tests are integrated.

## Stage Results

Complete. The exact 29-query oracle partitions all 157 candidate lines with no remainder, and E1-E21 preserve every unique construction-relevant strict, Notes, actual-Index, split, variant, implementation, property, search, and emulation passage. All 48 quoted fragments match the canonical monolith after presentation-only quote/whitespace normalization; the 34-line source oracle and all cited `BOOK:` bounds pass. Official PDFs repair only the visibly damaged positional weights, digit-count exponent, invocations, and inverse-rule labels; normalized repairs are never passed off as local quotations.

T02 is the `k>=3`, radius-one parameterization of T01: one total field over an explicit ordered finite alphabet, `AllSites`, ordered old `(left,self,right)` reads, one complete `k^3` table, typed same-site assignment, and T01 atomic commit. The optional Wolfram codec uses address `k^2*l+k*c+r`, has exactly `k^(k^3)` valid tables, and requires arbitrary-precision lossless identity. Rank, numeric aggregate, and palette are distinct. Seeds, backgrounds, finite realizations, horizons, mutation histories, reversibility claims, searches, behavior labels, rasters, and emulations remain independent records.

The semantic oracle proves the exact `3^27` count, all 256 T01 specializations, positional asymmetry, codes `921408` and `5407067979`, the identity/mutation table, `k=4` fixed-width pressure, exact purpose-doubling traces, and the 101-by-201 rule-921408 digest. Metadata pin 11 included, six excluded, and two relation-only assets. The direct Voronoi priority oracle expands all 27 contexts with branch counts `8/5/14`, display `111000222111011200111011200`, and code `3681845932419`. All ten printed reversible codes pass cyclic injectivity through length nine; the four Notes examples reproduce inverse windows `3,4,5,6`. The direct rule-921408 JPEG regression passes with `r=0.989621884093`, MAE `4.113100751`, and RMSE `8.052767980`. No source-permitted second pixel golden exists.

All seven embedded evidence/semantic/asset blocks pass, all Markdown fences are balanced, `git diff --check` passes, and all 102 repository tests pass. Independent review found the initially omitted direct Voronoi fixture; after its evidence, metadata, adjacent-2D exclusion, and priority-table oracle were added, re-review found no substantive blocker.

## Integration Results

The design ledger now contains the T02 construction row and D111-D114. T01 is generalized without changing its meaning; no completed stage is contradicted or reopened, no family branch or executor is introduced, and the public transition-update family remains at ten members. T03 owns aggregate rules, T04/T05 their color-count profiles, T06 background preservation, T07 reflection symmetry, and emulation/reversibility/search retain relation/property/analyzer identities. The Goal 2 handoff broadens the shared T01 table executor once, adds ordered alphabet rank/value and arbitrary-precision structural codecs, preserves evolving backgrounds and realization boundaries, and supplies exact binary/nonbinary/adversarial conformance tests.
