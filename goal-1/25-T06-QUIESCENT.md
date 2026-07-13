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

The original nine-family pass below is retained as a reproducible narrow diagnostic, not as closure. Independent saturation showed that it missed generic initial-condition, periodic-background, fixed-point, and actual-Index aliases named by this stage's own vocabulary. The authoritative closure is the 19-family, 280-line manifest later in this section.

| Q | Controlled family | Retained lines |
|---:|---|---:|
| 01 | `background` within 160 characters of a rule/state/pattern/structure/localized/blank/white/uniform term, in either direction | 66 |
| 02 | invariant state/configuration in either order | 13 |
| 03 | uniform white/black/state/configuration/background in either order | 20 |
| 04 | literal `unchanged` | 22 |
| 05 | literal all-white/all-black spellings | 8 |
| 06 | literal `quiescent`/`quiescence` | 1 |
| 07 | the exact only-white-state/unchanged phrase | 1 |
| 08 | single-cell blank/white-background and localized-structure background aliases | 3 |
| 09 | literal stable state/states | 9 |

The query counts overlap. Their union is 128, partitioned as 7 direct/native lines, 63 property/application/control relations, 45 nonfits, and 13 actual-Index routes. The 18 removed raw controls are generic uses of “uniform”, “background”, or “invariant” that do not name the candidate property; keeping them explicit prevents a hand-tuned regex from silently hiding its false-positive boundary.

### Initial narrow diagnostic — reproducible but not exhaustive

```bash
python3 - <<'PY'
import re
from pathlib import Path

P=Path('ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md')
L=P.read_text().splitlines()

queries=[
r'(?i)(?:background.{0,160}(?:cellular autom|rule|pattern|white|blank|initial|structure|localized|repetitive|uniform|state)|(?:cellular autom|rule|pattern|white|blank|initial|structure|localized|repetitive|uniform|state).{0,160}background)',
r'(?i)invariant.{0,80}(?:state|configuration)|(?:state|configuration).{0,80}invariant',
r'(?i)uniform.{0,80}(?:white|black|state|configuration|background)|(?:white|black|state|configuration|background).{0,80}uniform',
r'(?i)unchanged',
r'(?i)all[- ]white|all[- ]black',
r'(?i)quiescent|quiescence',
r'(?i)state.{0,80}only white.{0,80}unchanged',
r'(?i)single (?:black|gray) cell.{0,160}(?:white|blank) background|(?:white|blank) background.{0,160}single (?:black|gray) cell|initial condition used contains a single gray cell|localized structures.{0,160}(?:blank|white) background|(?:blank|white) background.{0,160}localized structures',
r'(?i)stable state(?:s)?',
]

# Deliberately broad lexical controls inspected before exclusion.
controls={418,432,434,2180,2794,3236,3668,4166,4168,4642,4908,6200,
          14827,14878,19266,20812,20914,21515}
sets=[{i for i,s in enumerate(L,1) if re.search(q,s)}-controls
      for q in queries]
assert [len(s) for s in sets]==[66,13,20,22,8,1,1,3,9]

direct={784,1346,2798,2926,3114,14046,18770}
relation={500,538,790,2002,2036,2102,2714,2720,2722,2726,2728,2730,
2742,2750,2914,2916,2918,3310,3382,3388,3402,3406,3792,3958,4068,
4070,4072,4078,4082,4084,4152,4176,4178,5206,6340,8406,8410,8416,
8430,11124,11140,11277,13265,13300,13304,13377,14099,14113,14241,
14341,14349,14536,14764,14768,14776,14795,15581,16060,18749,18764,
18765,19072,20118}
nonfit={1170,2372,2438,2446,3976,4032,4034,4086,4480,5058,5232,
5278,5316,6320,6332,6392,6510,6512,6526,6538,6548,6842,7028,12065,
13060,13722,14693,16105,16241,16257,16691,16737,16739,16940,17033,
17045,17439,17481,17813,18113,18453,18850,19702,20149,20521}
index={20965,21050,21080,21335,21517,21877,21994,22000,22016,22064,
       22120,22136,22304}
parts=[direct,relation,nonfit,index]
union=set().union(*sets)
assert len(union)==128
assert [len(x) for x in parts]==[7,63,45,13]
assert sum(map(len,parts))==len(set().union(*parts))==128
assert union==set().union(*parts)

# Prose immediately governing retained assets but outside the regex union.
follows={2868,2922,2930,14243,18766}
assert follows.isdisjoint(union)
assert L[2867].startswith('A sequence of totalistic rules involving nearest neighbors and four possible colors')
assert L[2921].startswith('Examples of the evolution of two-dimensional cellular automata')
assert L[2929].startswith('One-dimensional slices through the evolution')
assert L[14242].startswith('■ Page 249 · Game of Life.')
assert L[18765].startswith('- Rule 41.')
print('T06 text manifest: PASS 9 queries; 128 lexical; partition=7,63,45,13; governed=5')
PY
```

Recorded output:

```text
T06 text manifest: PASS 9 queries; 128 lexical; partition=7,63,45,13; governed=5
```

### Initial narrow disposition — superseded by saturation

- **Direct/native (7):** `784,1346,2798,2926,3114,14046,18770`. These state an unchanged white/blank selection, the 32-rule symmetric intersection, uniform-white invariance, the local invariant-block criterion, or the literal quiescent-symmetric relation.
- **Property, application, and boundary controls (63):** `500,538,790,2002,2036,2102,2714,2720,2722,2726,2728,2730,2742,2750,2914,2916,2918,3310,3382,3388,3402,3406,3792,3958,4068,4070,4072,4078,4082,4084,4152,4176,4178,5206,6340,8406,8410,8416,8430,11124,11140,11277,13265,13300,13304,13377,14099,14113,14241,14341,14349,14536,14764,14768,14776,14795,15581,16060,18749,18764,18765,19072,20118`. These distinguish seed, periodic background, convergence, global invariant configurations, perturbation stability, reversibility, localized structures, application geometry, and boundary realization from the local T06 predicate.
- **Nonfits (45):** `1170,2372,2438,2446,3976,4032,4034,4086,4480,5058,5232,5278,5316,6320,6332,6392,6510,6512,6526,6538,6548,6842,7028,12065,13060,13722,14693,16105,16241,16257,16691,16737,16739,16940,17033,17045,17439,17481,17813,18113,18453,18850,19702,20149,20521`. These are substitution, mobile, network, physics, packing, perception, arithmetic, language, and generic unchanged/stable/background usages with no T06 local-rule claim.
- **Actual-Index routes (13):** `20965,21050,21080,21335,21517,21877,21994,22000,22016,22064,22120,22136,22304`. They route to already dispositioned invariant-state, background, Life, rule-110, or totalistic material and add no mechanics.

These 128 lines have no remainder inside the narrow query union, but that union is not the evidence universe. `2868,2922,2930,14243,18766` remain useful governed continuations; the authoritative classification below absorbs the broader aliases and replaces the narrow `7/63/45/13` architecture count.

### Authoritative 19-family saturation manifest

`BOOK` means `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`; the actual Index begins at physical `BOOK:20826`. Nineteen controlled families close 280 unique canonical lines: 212 pre-Index and 68 actual-Index. Counts are distinct physical lines and overlap between families.

| Q | Controlled family | Pre-Index | Actual Index |
|---:|---|---:|---:|
| 01 | `quiescen*` | 1 | 0 |
| 02 | background within 100 characters of unchanged/remain/stay/preserve/invariant/stable, plus change-white/blank-background | 3 | 1 |
| 03 | blank within 80 characters of background, either order | 2 | 0 |
| 04 | white/black within 40 characters of background, either order | 14 | 0 |
| 05 | all-white/all-black/only-white/only-black state phrases | 12 | 0 |
| 06 | uniform state/configuration/color/final-state phrases | 12 | 0 |
| 07 | invariant within 40 characters of state/configuration | 9 | 5 |
| 08 | stable within 40 characters of state/configuration | 9 | 3 |
| 09 | cellular automaton within 180 characters of unchanged | 5 | 0 |
| 10 | white/blank within 100 characters of unchanged/remain/stay | 7 | 0 |
| 11 | single black/gray/white cell; simple/finite/localized initial condition; initial condition near white/blank background | 105 | 2 |
| 12 | repetitive/periodic/random/regular and governed background aliases | 23 | 2 |
| 13 | fixed point/state/configuration and remain-fixed aliases | 23 | 1 |
| 14–19 | actual-Index drift guards: CA+initial/invariant/background; named initial-condition headings; background phases; invariant; stable/bistable/metastable; uniformity/state | — | 68-line union |

The resulting disjoint semantic disposition is `4/25/111/66/6/68`: direct native evidence, CA invariant-property relations, CA seed/background/profile/view evidence, non-CA SimpleProgram aliases, general controls, and actual-Index routes. This classification is deliberately strict: a line enters the CA-axis groups only when its subject is a cellular automaton or an explicit CA relation. The same words in substitutions, symbolic systems, PDEs, physics, networks, or generic data analysis remain non-CA aliases or controls.

```bash
python3 - <<'PY'
import re
from pathlib import Path

P=Path('ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md')
L=P.read_text().splitlines(); IX=20826
def ns(s): return set(map(int,s.split(','))) if s else set()

pre=ns('432,440,450,472,476,478,500,518,538,550,566,730,746,754,784,790,846,1238,1346,1348,1350,1886,1938,1956,1982,2102,2180,2184,2230,2256,2262,2706,2714,2720,2726,2728,2730,2742,2750,2794,2798,2914,2916,2918,2926,3046,3060,3066,3070,3072,3076,3082,3084,3086,3090,3152,3158,3204,3230,3234,3236,3310,3382,3388,3704,3780,3902,3958,3976,4032,4034,4068,4070,4072,4078,4082,4084,4086,4152,4264,4274,4306,4424,4480,4818,5058,5232,5238,5242,5258,5278,5280,5316,5360,5366,5488,5492,6200,6320,6332,6340,6510,6526,6532,6538,6548,6636,6644,6648,6684,6784,6788,6796,6836,6864,6978,7028,7232,7722,7744,8350,8400,8410,8416,8430,8578,8582,8584,8606,8664,8668,8744,8746,8748,8754,8990,9044,9178,10648,11505,11551,11579,11585,12065,12452,12457,12470,12915,13265,13296,13300,13579,13722,13798,14046,14113,14213,14241,14281,14317,14331,14341,14386,14429,14483,14536,14537,14699,14701,14717,14748,14764,14776,15191,15209,15326,15546,15550,15554,15570,15581,15641,15959,16052,16053,16060,16109,16173,16232,16241,16739,17103,17263,17813,18453,18486,18498,18749,18764,18770,18956,19060,19072,19240,19242,19264,19266,19584,20118,20126,20149,20586')
index=ns('20900,20914,20946,20965,20967,20972,21014,21042,21046,21050,21054,21068,21080,21130,21168,21187,21193,21195,21207,21213,21233,21265,21285,21287,21335,21473,21515,21521,21525,21550,21677,21683,21729,21771,21779,21813,21877,21891,21899,21907,21923,21929,21942,21990,21992,21994,21998,22000,22002,22010,22016,22028,22030,22052,22064,22086,22096,22114,22120,22136,22144,22150,22304,22352,22378,22390,22392,22454')

direct=ns('784,1346,2798,2926')
ca_property=ns('2714,2720,2726,2728,2730,2742,2750,2794,3230,3234,3236,3310,3958,4068,4070,4072,4078,4082,4084,4152,14046,14113,14717,18770,19266')
ca_profile=ns('432,440,450,472,476,500,518,538,550,566,730,746,754,790,846,1348,1350,1956,1982,2180,2184,2230,2256,2262,2914,2916,2918,3046,3060,3066,3070,3076,3082,3084,3086,3090,3152,3158,3382,3388,3704,3780,3902,4264,4274,4306,4424,4480,5058,5232,5238,5242,5278,5316,6340,6636,6644,6684,6784,6788,7232,7722,7744,8400,8410,8416,8430,8606,8668,8754,9044,10648,11505,11579,11585,12065,13296,13579,14213,14241,14281,14317,14331,14341,14429,14536,14537,14748,14764,14776,15326,15581,15641,15959,16052,16053,16060,16173,17103,17813,18486,18498,18749,18764,19060,19072,19264,19584,20118,20126,20586')
nonca=ns('478,1238,1886,1938,2102,2706,3072,3204,4032,4034,4086,4818,5258,5280,5360,5366,5488,5492,6200,6320,6332,6510,6526,6532,6538,6648,6796,6978,7028,8350,8578,8582,8584,8664,8744,8746,8748,8990,9178,11551,12452,12457,12470,12915,13265,13300,13722,13798,14386,14483,14699,14701,15191,15209,15546,15550,15554,15570,16109,16232,16241,18453,18956,19240,19242,20149')
controls=ns('3976,6548,6836,6864,16739,17263')
parts=[direct,ca_property,ca_profile,nonca,controls,index]
assert [len(x) for x in parts]==[4,25,111,66,6,68]
assert len(pre)==212 and len(index)==68 and max(pre)<IX<=min(index)
assert sum(map(len,parts))==len(set().union(*parts))==280
assert set().union(*parts)==pre|index

# Nineteen-family saturation guard. The exact canonical line ledger above is
# primary; this guard ensures no ledger line has drifted away from every
# controlled vocabulary family after corpus edits.
families=[
r'quiescen',r'background.{0,100}(?:unchang|remain|stay|preserv|invariant|stable)',
r'blank.{0,80}background|background.{0,80}blank',
r'(?:white|black).{0,40}background|background.{0,40}(?:white|black)',
r'all[- ]?(?:white|black)|only (?:white|black)',
r'uniform.{0,40}(?:state|configuration|color|final)',
r'invariant.{0,40}(?:state|configuration)|(?:state|configuration).{0,40}invariant',
r'stable.{0,40}(?:state|configuration)|(?:state|configuration).{0,40}stable',
r'cellular autom.{0,180}unchanged|unchanged.{0,180}cellular autom',
r'(?:white|blank).{0,100}(?:unchang|remain|stay)',
r'single (?:black|gray|white) cell|(?:simple|finite|localized) initial condition',
r'(?:repet|period|random|regular|localized|complicated).{0,80}background|background.{0,80}(?:repet|period|random|regular|localized|complicated)',
r'fixed.{0,20}(?:point|state|configuration)|remain.{0,20}fixed',
r'cellular autom',
r'(?:initial|random|repetitive|simple|changes in initial) conditions?',
r'background|phases',r'invariant',r'stable|bistable|metastable',r'uniformity|uniform state|uniform spectra']
assert len(families)==19
guard=re.compile('|'.join(f'(?:{x})' for x in families),re.I)
assert all(guard.search(L[n-1]) for n in pre|index)
print('T06 saturation manifest: PASS 19 families; 280 lines; pre/index=212/68; partition=4,25,111,66,6,68')
PY
```

Recorded output:

```text
T06 saturation manifest: PASS 19 families; 280 lines; pre/index=212/68; partition=4,25,111,66,6,68
```

The split-corpus cross-check found 224 raw matches. Seventeen split-only punctuation/line-join variants and 18 monolith non-byte mirrors reconcile without a new semantic candidate; one combined split line mirrors both `BOOK:8578` and `BOOK:8584`. The actual split Index offset is `+17443` at Colophon line 3383. No split-only construction changes the six-way disposition.

## Book Excerpts

The following are canonical, role-separated excerpts. Short fragments are quoted to make the inference auditable; the structural reconstruction, not the source's color words or gallery layout, is authoritative.

**E01 — a gallery filter, not a rule family.** The three-color totalistic caption says rules that “change the white background are not included” (`BOOK:784`; Chapter 3 split `:101`). This directly supports a selection predicate over already defined rules. The adjacent single-gray start (`BOOK:790`) is initial-condition data, not part of that predicate.

**E02 — the exact elementary/reflection intersection.** The history says the original search used “32 rules” with left-right symmetry whose blank backgrounds stayed unchanged (`BOOK:1346`; Chapter 3 split `:663`). The exhaustive reconstruction gives 64 symmetric rules and 128 zero-preserving rules, with exactly 32 in their intersection; symmetry and T06 are therefore independent properties.

**E03 — unchanged all-white state.** The page-247 caption selects symmetric nearest-neighbor binary rules that leave states containing only white cells unchanged (`BOOK:2798`; Chapter 6 split `:97`). This is precisely a uniform-state fixed-point obligation, not a boundary, seed, halt condition, or special update.

**E04 — the same property in two dimensions.** The page-262 caption describes a gallery of rules that leave an only-white state unchanged (`BOOK:2926`; Chapter 6 split `:223`). The attached raster contains 30 even codes `2..60`, while the source sentence says “most of the 64 possibilities”; the repair is recorded below. The property survives the source defect because all 32 qualifying six-row tables are independently derivable and the displayed 30 are a proper selected subset.

**E05 — ordinary rule evaluation is the witness.** For rule 30, a uniformly white initial state yields uniform white forever (`BOOK:3114`; Chapter 6 split `:411`). The same paragraph's three “pictures below” show different repetitive initial conditions, so those assets are boundary controls: the uniform witness proves T06, while simple behavior from nonuniform starts does not.

**E06 — periodic background is a counter-boundary.** Rule 110 structures “do not exist on a blank background” and instead inhabit a 14-cell repeating pattern (`BOOK:3388`; Chapter 6 split `:683`). This proves that “background” can mean a nonuniform space-time phase relation and must not be collapsed into uniform-blank preservation.

**E07 — invariance is not convergence.** Two rules can both have all-white and all-black invariant states while only one reaches such a state from random input (`BOOK:4070,4078`; Chapter 7 split `:641,649`). Thus `T(b,...,b)=b` neither predicts attraction nor authorizes fixed-point stopping.

**E08 — local invariant-block criterion.** The Notes reduce invariant one-dimensional configurations to permitted local blocks whose center agrees before and after evolution (`BOOK:14046`; Index split `:1947`). At one step and on the uniform block this specializes exactly to the T06 witness. The printed `t`/width mismatch is repaired below rather than silently generalized.

**E09 — nonuniform invariant configurations are a sibling relation.** The two-dimensional Notes describe configurations assembled from neighborhoods whose center stays unchanged (`BOOK:14113`; Index split `:2014`). This classifies whole configurations and can include nonuniform repetitive states; it is not the designated uniform-blank predicate.

**E10 — still lifes are applications, not T06 semantics.** The Life Notes list small structures that remain unchanged at every step (`BOOK:14795`; Index split `:2696`). Their raster is relation-only evidence for fixed configurations under one T06-compatible rule, not a new update law or proof that all passing rules contain still lifes.

**E11 — “quiescent” is literal but still relational.** The Notes' emulation network is explicitly restricted to “quiescent symmetric elementary rules” (`BOOK:18770`; Colophon split `:1327`), while the nearby rule-73 note separately says “on a white background” (`BOOK:18764`; Colophon split `:1321`). The former confirms T06 vocabulary; neither emulation nor a run background belongs in the predicate.

### Source repairs

1. **Page 262 count/wording defect.** The repository text and the official Chapter 6 PDF both say “most of the 64 possibilities” at `BOOK:2926`. For a binary five-cell totalistic table there are `2^6=64` rules total and exactly `2^5=32` that preserve white. The raster at `BOOK:2924` visibly labels 30 even codes `2,4,...,60`, excluding `0` and `62`. This is a source wording/count inconsistency, not OCR. T06 records the prose faithfully, uses the independently proved 32-rule property count, and treats the 30-panel raster as a selected gallery.
2. **Invariant-block horizon defect.** `BOOK:14046` says “after `t` steps” but gives block width `2r+1`; the official Notes PDF has the same wording. The general width is `2rt+1`. T06 uses this evidence only at `t=1`, where the printed width is correct, and does not promote the erroneous general formula.
3. **Page 264 raster-only caption.** `_page_264_Picture_3.jpeg` contains a Life caption absent from the monolith OCR, including the 8-neighbor rule and outer-totalistic code 224. It is hash-pinned below as an application relation. No missing caption text is invented into the book corpus, and no Life-specific class enters T06.

## Asset and Raster Audit

The asset scope starts from the four direct and 25 CA invariant-property lines, then performs a direction-sensitive forward/reverse join through explicit picture pointers, adjacent captions, and their complete multi-panel runs. It includes the page-281 three-image run governed by `BOOK:3114`, the page-368 uniformity-mechanism chain surrounding `BOOK:4152`, both page-369 comparators, and the four-file page-246 panel governed by `BOOK:2790` after retained `BOOK:2794`. The join stops at the next separately captioned gallery; therefore page-248/page-249 assets at `BOOK:2800,2804` are outside T06's asset closure. The exact result is 45 physical JPEGs and 90 reverse references: each asset occurs once in the monolith and once in its split mirror.

| Class | BOOK links | Meaning |
|---|---|---|
| Included/direct (`I`, 5) | `778,782,2796,2866,2924` | rule-row/codec evidence and the four label-bearing quiescent gallery selections |
| Relation-only (`R`, 28) | `2716,2718,2724,2732,2782,2784,2786,2788,2920,2928,2932,2934,2936,2938,2940,3954,4074,4076,4134,4140,4146,4148,4150,4174,8408,14111,14797,18772` | convergence, class, geometry, observer, invariant-configuration, uniformity-mechanism, background, still-life, and emulation relations |
| Excluded/control (`X`, 12) | `3116,3118,3120,3380,4080,4156,4158,4160,4170,8414,14766,18768` | nonuniform repetitive starts, rule-110 periodic background, nonuniform invariant target, averaging/conservation, repetitive-background runs, and rule-41 controls |

The visual findings agree with the semantic oracle: page 247 contains exactly the 32 reflection-symmetric zero-preserving ECA labels; page 256 contains 32 displayed four-color codes divisible by four; page 262 contains 30 even labels `2..60`; page 263 is an observer slice of six rules; page 264 is a Life application; and the page-363 pair demonstrates that admitting a uniform invariant state does not imply reaching it.

### Exact source-link and reverse-reference oracle

```bash
python3 - <<'PY'
import re
from pathlib import Path

ROOT=Path('ref/A-New-Kind-of-Science')
BOOK=(ROOT/'A-New-Kind-of-Science.md').read_text().splitlines()
links={
778:'_page_75_Figure_6.jpeg',782:'_page_76_Figure_2.jpeg',
2716:'_page_239_Picture_1.jpeg',2718:'_page_239_Picture_2.jpeg',2724:'_page_239_Picture_5.jpeg',
2732:'_page_240_Figure_2.jpeg',2782:'_page_246_Picture_8.jpeg',2784:'_page_246_Picture_9.jpeg',
2786:'_page_246_Picture_10.jpeg',2788:'_page_246_Picture_11.jpeg',2796:'_page_247_Figure_2.jpeg',
2866:'_page_256_Figure_2.jpeg',2920:'_page_261_Figure_2.jpeg',2924:'_page_262_Figure_2.jpeg',
2928:'_page_263_Figure_2.jpeg',2932:'_page_264_Picture_2.jpeg',2934:'_page_264_Picture_3.jpeg',
2936:'_page_264_Picture_4.jpeg',2938:'_page_264_Picture_5.jpeg',2940:'_page_264_Picture_6.jpeg',
3116:'_page_281_Picture_6.jpeg',3118:'_page_281_Picture_7.jpeg',3120:'_page_281_Picture_8.jpeg',
3380:'_page_305_Picture_2.jpeg',3954:'_page_355_Figure_1.jpeg',4074:'_page_363_Picture_7.jpeg',
4076:'_page_363_Picture_9.jpeg',4080:'_page_364_Figure_2.jpeg',4134:'_page_368_Picture_3.jpeg',
4140:'_page_368_Picture_6.jpeg',4146:'_page_368_Picture_9.jpeg',4148:'_page_368_Picture_10.jpeg',
4150:'_page_368_Picture_11.jpeg',4156:'_page_368_Picture_14.jpeg',4158:'_page_368_Picture_15.jpeg',
4160:'_page_368_Picture_16.jpeg',4170:'_page_369_Picture_4.jpeg',4174:'_page_369_Picture_6.jpeg',
8408:'_page_715_Figure_1.jpeg',8414:'_page_715_Figure_4.jpeg',14111:'_page_957_Picture_14.jpeg',
14766:'_page_979_Picture_6.jpeg',14797:'_page_979_Picture_22.jpeg',
18768:'_page_1133_Picture_6.jpeg',18772:'_page_1133_Picture_8.jpeg'}
assert len(links)==45
for n,name in links.items(): assert BOOK[n-1]==f'![]({name})',(n,BOOK[n-1])

stage=Path('goal-1/25-T06-QUIESCENT.md').read_text()
src=stage.split('### Exact metadata oracle',1)[1].split('\nitems={',1)[1].split('\n}\n\ndef jpeg_size',1)[0]
paths=set(re.findall(r"'([^']+\.jpeg)':\(",src))
assert len(paths)==45 and {Path(p).name for p in paths}==set(links.values())

refs={name:[] for name in links.values()}
for md in ROOT.rglob('*.md'):
    for line_no,line in enumerate(md.read_text().splitlines(),1):
        for name in refs:
            if re.fullmatch(r'!\[\]\((?:Images/)?'+re.escape(name)+r'\)',line):
                refs[name].append((md.relative_to(ROOT).as_posix(),line_no))
assert all(len(v)==2 for v in refs.values()) and sum(map(len,refs.values()))==90
assert refs['_page_246_Picture_8.jpeg']==[
 ('A-New-Kind-of-Science.md',2782),
 ('CHAPTERS/6-Starting-from-Randomness/Starting-from-Randomness.md',81)]
assert refs['_page_264_Picture_3.jpeg']==[
 ('A-New-Kind-of-Science.md',2934),
 ('CHAPTERS/6-Starting-from-Randomness/Starting-from-Randomness.md',231)]
assert refs['_page_1133_Picture_8.jpeg']==[
 ('A-New-Kind-of-Science.md',18772),('BACK-MATTER/Colophon/Colophon.md',1329)]
print('T06 source/asset join: PASS 45 assets; refs=90; classes=5,28,12')
PY
```

Recorded output:

```text
T06 source/asset join: PASS 45 assets; refs=90; classes=5,28,12
```

### Exact metadata oracle

```bash
python3 - <<'PY'
from hashlib import sha256
from pathlib import Path

ROOT=Path('ref/A-New-Kind-of-Science')
items={
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_75_Figure_6.jpeg':(51178,610,446,'acb13963632286960ca61b616ff2f45a940750f3ab7deb5e6fbf696543015c15','I'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_76_Figure_2.jpeg':(174691,1109,1279,'8c11659c8bd63d37a972c5ffab376b62948f7c4e05f9fd10f239e51464f4084d','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_239_Picture_1.jpeg':(3942,319,57,'1deb7b9038593be7ba55e70b84971dde44870415855c4d3f40a26306ad64a554','R'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_239_Picture_2.jpeg':(20462,701,140,'1cd11949b7917044fdaa9016c17b824ff3a829cf6306cbe5393786d7b7357d49','R'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_239_Picture_5.jpeg':(106823,1076,454,'71aa61335dcfa8b4d98f2c5f9ea0da38a478ad9dffc4f9622dc0b075de0153d9','R'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_240_Figure_2.jpeg':(206223,1077,950,'5ee29923c1db72b296464ee0a8f9f5801c63f4495d1ec330563d42452acfda31','R'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_246_Picture_8.jpeg':(5532,276,238,'afada8215843e18ad2d2dd9fbc1fe4f7e346105f65b1587f044d409f171ec143','R'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_246_Picture_9.jpeg':(16742,279,250,'0ca74ea450ce582651a26b7c6ff42ad7ffbcf3a296bec697c651cceeb2411e21','R'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_246_Picture_10.jpeg':(27545,276,252,'273f21dcf1e47bc7ce45ab61aa238dd64a75ea239f71d33c3bea62c8bfc1e4bb','R'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_246_Picture_11.jpeg':(11989,269,245,'3a6868e15ad61245797bb4f643c76411af8b3afa426f2e4be84146d56376df63','R'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_247_Figure_2.jpeg':(261973,1086,1387,'00f9660bac37681f214cbf4b234dffeab446e3d23e4de2a7c49ff7011f7db6a0','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_256_Figure_2.jpeg':(328297,1092,1367,'1c4967f6967d8e813b2a281e2615dc8bef272eb57789b60e23c950de5e6bc01f','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_261_Figure_2.jpeg':(309273,1109,1297,'49f35fe65202ef7fbfee2da92b7460d36fc329b66a553782ebf8991f237944dd','R'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_262_Figure_2.jpeg':(240733,1013,1291,'23df7e86bf96a148a17c13847eb53c773a24f86cc5a24f2e1a550f79b94439e3','I'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_263_Figure_2.jpeg':(295433,1195,1355,'71f5ac8784f493b664a93aff52e157e1ac7bf94a6b2e910f98de9fef663736ec','R'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_264_Picture_2.jpeg':(171688,701,1133,'795c798b4c9b2bbd24febea8333176ebd7bc33852a4905894e5bff4a1426a757','R'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_264_Picture_3.jpeg':(50190,651,254,'0689cd062ff648358aaef8ac0fae47cfb64538e5c0ed55a2c5fe660e6943eeb5','R'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_264_Picture_4.jpeg':(39728,414,415,'21b2edf19eb92f099b5db53a8fe8f6b234545ec7d8710aa64aa9270dc4774eda','R'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_264_Picture_5.jpeg':(34580,404,411,'4a80f0e1f845b5d74455ea2845a32de05be03083850520e54106b658b3a8289e','R'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_264_Picture_6.jpeg':(25093,404,393,'225339081568d6d5bf0a17c073aba8851f7379ba968949985a3082c585c8cc17','R'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_281_Picture_6.jpeg':(40810,391,320,'707d3732669d57d3aa10cd945671485dd53db3b7bb1dd666293e71ba3e53f7be','X'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_281_Picture_7.jpeg':(43369,336,311,'93e9bfbdb7f040a94074e6f459183fc5e971e7dd57892569df4c99687d8299d0','X'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_281_Picture_8.jpeg':(43441,380,313,'32d4b866d2a0cc3dc60a0099a5a0e4bd93a8f7e010f016e97f9e6222ee54295a','X'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_305_Picture_2.jpeg':(642889,1184,1342,'7e75ba3d0cb57a0b35d5a7b29e803386617e1ede22eefae19ce6e21fc465a9c9','X'),
'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_355_Figure_1.jpeg':(265941,1158,1246,'978ea2b646179f403328044f369d041e9176b325ec303bf8a764ac266ccec216','R'),
'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_363_Picture_7.jpeg':(6991,220,142,'4b7812c66ba736164526457f476a999582bc8ffb37aa5cb9b3a1699eff29b31c','R'),
'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_363_Picture_9.jpeg':(15637,228,159,'d87280d6d085c7284ee5f6b8870c39a6f96f35a53e2798801d59dd306a639d33','R'),
'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_364_Figure_2.jpeg':(116597,989,397,'81bf29a27913353b89e4e32d4b9ccf8a8af86c863077527b912a773c58c968d2','X'),
'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_368_Picture_3.jpeg':(17987,405,157,'03f73ec39a1f110309a6d0d21ac6080e66700b7a792f5cb335f457c33eddeba6','R'),
'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_368_Picture_6.jpeg':(23918,491,154,'200f432e58a61dce0026f3f2a69f5fc83bbe16783e1fd030cdba682d3a9d68c1','R'),
'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_368_Picture_9.jpeg':(10203,205,113,'df69630ae9a102b7d314d5fe8daf38b40234abfcb3a9268b72934184e428572f','R'),
'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_368_Picture_10.jpeg':(8904,167,120,'712a3d8ac7aca56b40a6e8d36ae1edbe100516f95eb2756ec208832d9527599e','R'),
'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_368_Picture_11.jpeg':(6347,200,138,'28db7bac60808ac25231693e4b45d8e50698d94401f6bd5ba2c23280d2656555','R'),
'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_368_Picture_14.jpeg':(11542,277,145,'19dd016835d4f6a05d11a7f7d2aa039ced8ed5a973eb90ed1d1fb1e832d9af22','X'),
'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_368_Picture_15.jpeg':(6506,288,149,'cc1d2fb0c980f1d4c2b9e7b4547c20114e91b31770a7ba798028f7d55b192102','X'),
'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_368_Picture_16.jpeg':(5432,279,141,'ae917b81e1b46322311b919c8e91a2a8881ee6b20b52642ccea9d63dd1a53eda','X'),
'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_369_Picture_4.jpeg':(21395,599,163,'2648b7a00fddf8cb0ec7a3d9fa9012006a67e86c0652d7a0dff83054dbfeeae2','X'),
'CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_369_Picture_6.jpeg':(15663,950,172,'d1a0e734fc7ebb8474a3cfc93c626e7d082f51418939236214b2e71d05a6c621','R'),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_715_Figure_1.jpeg':(201204,1123,468,'534b1e558bce374329e94da6ec9626bad2e7b67fb181a3322f691d8727a549d9','R'),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_715_Figure_4.jpeg':(171594,1135,419,'1ce3e584535e776132894ff1b5ade249cf1fcf4ffcf5cff8141e1985af0221a1','X'),
'BACK-MATTER/Index/Images/_page_957_Picture_14.jpeg':(11244,560,84,'957c224462a36129efb03f2413788e4bc4a4f0606372f27dc67ca1df05b87b35','R'),
'BACK-MATTER/Index/Images/_page_979_Picture_6.jpeg':(23347,579,111,'f9fe6970d82502f70cf371b503160c71047d290954ca19d5d37b4fd65c12fdc1','X'),
'BACK-MATTER/Index/Images/_page_979_Picture_22.jpeg':(10029,568,45,'3fbf48b08d926e273073ff2e1610dc628528573156d8265ba2327602bfaed42a','R'),
'BACK-MATTER/Colophon/Images/_page_1133_Picture_6.jpeg':(18262,569,136,'11dde5ae83b89e5879a0c7b02e06b759443ce65bc372fa426ee388b927aea33f','X'),
'BACK-MATTER/Colophon/Images/_page_1133_Picture_8.jpeg':(23917,424,349,'9f933b79fdc7dd17b803ec2f9bc1a0e851500b6a14b7f494ccc3cf32d3e3290c','R'),
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

counts={'I':0,'R':0,'X':0}; digests=set()
for name,(size,w,h,digest,kind) in items.items():
    data=(ROOT/name).read_bytes()
    assert (len(data),*jpeg_size(data),sha256(data).hexdigest())==(size,w,h,digest)
    assert digest not in digests; digests.add(digest); counts[kind]+=1
assert len(items)==45 and counts=={'I':5,'R':28,'X':12}
print('T06 metadata oracle: PASS 5 included; 28 relation-only; 12 excluded')
PY
```

Recorded output:

```text
T06 metadata oracle: PASS 5 included; 28 relation-only; 12 excluded
```

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
