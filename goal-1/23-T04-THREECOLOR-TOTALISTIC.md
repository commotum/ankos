# 23-T04-THREECOLOR-TOTALISTIC

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T04, CSV line 5, `Three-Color Totalistic Cellular Automata`; taxonomy section 4 at `ref/notes/CA-Types.md:102-122` is vocabulary only.
- Architecture verdict: **T04 is exactly the strict T03 preset `k=3,r=1` with canonical alphabet/valuation `A_3=(0,1,2)`, `nu_3(i)=i`**. Substitution into T03 gives arity `q=3`, reachable sums `0..6`, table length `M=7`, rule count `R=3^7=2187`, and valid codes `0..2186`; strict text and the general count independently pin the same profile (`BOOK:772-776,11897`).
- Native identity is the seven-row structural table `U:{0,...,6}->A_3`. The optional code is `n=sum_{s=0}^6 nu_3(U(s))3^s`, with sum zero least significant. Exact source fixtures are code `777 -> (0,1,2,1,0,0,1)` (`BOOK:776`), code `867 -> (0,1,0,2,1,0,1)` (`BOOK:11168`), and code `420 -> (0,2,1,0,2,1,0)` (`BOOK:11918`).
- No three-color-only state, read, rule result, update, successor, or boundary exists. The Notes use the same direct range-`r` totalistic signature, sum lookup, padded codec, and common convolution framework (`BOOK:11056,11902,11904,11908,11910,11912,11914,11916`); D115-D118 therefore make T04 a strict preset over the T01/T02/T03 construction, not a fourth CA executor.
- White-background preservation is the separate T06 predicate `U(0)=0`, equivalently `n mod 3=0`, and selects `3^6=729` of the 2,187 programs. The page-76 scan is only the 50-code selection `993,996,...,1140`, not the whole restriction (`BOOK:784`). The single-gray start is a T08/run profile (`BOOK:790`).
- White/gray/black names and tones are presentation labels for semantic values `0/1/2`, not a required palette (`BOOK:774-776`). Reflection is derived from the equal-weight symmetric stencil, additivity is a separately proved property of examples such as code 420, and classes, gallery order, crop, horizon, raster, and emulations remain analyzer/view/relation data (`BOOK:784,7912,11918`).
- Fresh API inspection confirms partial structural fit but no executable T04 surface: `simple_programs.md:643-645,1768-1791` require fixed-arity reads and one old snapshot, while `simple_programs.md:1964-2032` conflates exact numeric sum with active count and color histogram. `src/ca/rules.py:198-217,262-295` records a loose aggregate channel but derives neither the seven cases nor the 2,187-rule range.
- Fresh runtime inspection confirms that the correct radius-one stencil already exists (`src/ca/neighborhoods.py:551-569`; `tests/test_neighborhoods.py:86-98`), but spatial rollout is family-whitelisted and binary decoded (`src/ca/rollout.py:145-212,643-682`), batch rule IDs are coerced to `numpy.int64` (`src/ca/rollout.py:264-274`), and the manifest parser accepts only named Phase 1 families (`src/ca/specs.py:117-181`). No current test constructs, validates, or evolves a three-color seven-row program (`tests/test_rules.py:9-45`; `tests/test_rollout.py:263-424`).

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

In progress. The audit must independently close strict text/captions, all three-color gallery labels and continuations, Notes/implementations, actual Index, split duplicates, named codes, seed/background filters, properties, applications, emulations, and adjacent non-three-color controls.

## Book Excerpts

In progress. Record every unique construction- or preset-relevant passage verbatim with exact monolith provenance and transparent source repairs.

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

**Owned boundaries.** T04 fixes only the three numeric values, radius one, seven-row domain, and validation range. T06 owns `U(0)=0`; T07 consumes the reflection proof derived from equal weights on a symmetric stencil; T08 owns single-cell initial-condition profiles. Additivity, reversibility, universality, behavior class, frequency, gallery selection, emulation, seed/background, boundary, palette, raster, and observation remain separately typed claims or records.

## Current API Fit

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
- Scalar and batch spatial loops compute each new slice from `states[index-1]`, preserving the old-snapshot transition shape (`src/ca/rollout.py:576-640`). Existing scalar/batch parity tests are useful regression evidence (`tests/test_rollout.py:285-309,345-376,404-424`).
- The current point seed already represents the source single-gray-on-zero run as `point(value=1,fill_value=0)` without entering rule identity (`src/ca/seeds.py:260-313`; `tests/test_seeds.py:71-74`). Viewer palettes are explicit export arguments (`src/ca/viz/export.py:58-62,105-120,286-327`; `tests/test_viz_export.py:280-297`).

**Blocking mismatches inherited from T03:**

- `_channel_state` does compute an integer sum, but ignores the declared `sum` versus `count` mode, forces `int64`, and validates neither the explicit valuation nor arity/value domain (`src/ca/rollout.py:742-777`). This coincidentally gives the canonical local sum for legal `0/1/2` reads; it is not a sufficient T04 implementation.
- A single channel could numerically produce indices `0..6`, but `_next_spatial_state` always decodes one binary bit with `right_shift` and `&1`, so output color `2` is impossible (`src/ca/rollout.py:643-682`). Adding a ternary conditional here would duplicate T03 semantics and violate D117.
- Both scalar and batch rollout dispatch on named rule families, and generic `lookup` is not executable (`src/ca/rollout.py:145-212,292-330`). T04 cannot be added to either whitelist; G2-T03 must replace these switches with the shared typed rule/result/update protocol.
- Batch IDs are normalized to `numpy.int64` (`src/ca/rollout.py:264-274`). T04 codes happen to fit, but a T04-only exception would preserve the general T03 serialization defect. The preset must use the shared arbitrary-precision tagged-code/program-reference path.
- Seed states are converted to `int64` without validation against a dynamics alphabet/valuation (`src/ca/rollout.py:576-640`), and `RawEpisode`/`RawBatch` expose only numeric rule IDs (`src/ca/specs.py:58-81`). Goal 2 must validate all reads/seeds/fixed exterior values through G2-T03 and preserve the structural program reference.
- Current tests cover 256-rule binary named families only (`tests/test_rules.py:9-40`) and spatial binary outputs (`tests/test_rollout.py:263-424`). No test pins a seven-row table, ternary output, code direction/range, background-changing T04 rule, preset/generic identity, or separation from seed/filter/palette.

Conclusion: current selector, seed, boundary, trace shape, and parallel-loop scaffolding are reusable, but T04 is not executable today. Its implementation is blocked on G2-T03 rather than on any missing T04-specific runtime mechanism.

## Principles Audit

- **Principles 0, 1, and 10 — PASS as a preset.** Evidence shows genuine semantic identity with T03 after fixing `k=3,r=1,nu_3`; the catalog label remains discoverable through strict preset resolution without inventing an executor (`principles.md:3-13,83-87`).
- **Principles 2, 3, 4, and 11 — PASS only through G2-T03.** `AllSites`, the radius-one old read, exact-sum table rule, typed same-site assignment, and atomic update retain one responsibility each. Synchronous old-snapshot update is defining semantics, while no T04-specific result/update exists (`principles.md:15-45,89-93`).
- **Principles 5, 7, and 9 — PASS with explicit coupling.** Fixed support and field values are state; no hidden palette, seed, background, class, or cursor is allowed. `k=3`, canonical valuation, arity three, seven table rows, and output domain are intrinsically coupled and strictly validated; seed, boundary realization, horizon, and view remain independent (`principles.md:47-57,65-81`).
- **Principles 8 and 12 — PASS at the boundary, current export migration required.** Table/code identity must survive structural serialization, while gallery flattening, coordinates, palette, raster, crop, and batch form remain downstream (`principles.md:71-75,95-103`). Current numeric-only `rule_id` export must migrate through G2-T03 rather than becoming a T04 exception.
- **Principles 13 and 15 — REQUIRED conformance.** Code 777's ternary output/trajectory, code 1's evolving zero background, the 729-versus-50 filter distinction, equal-sum/different-histogram contexts, table/code equality, invalid preset overrides, and preset/generic structural equality are the adversaries that establish constructive fidelity (`principles.md:105-109,117-121`).
- **Principles 14 and 16 — HARD STOP gate.** A `three_color_totalistic` rollout branch, ternary bit-decoder patch, duplicated table/codec, hidden exhaustive expansion, or fixture-specific fallback means the T03 abstraction has not actually composed and must be redesigned (`principles.md:111-127`).

The audit finds no architectural divergence requiring a new construction. It does find a real implementation dependency: T04 cannot ship before the generic G2-T03 path removes the current family/binary restrictions.

## Asset and Raster Audit

T03's audit is the physical superset; this section independently re-hashes and re-executes the strict `k=3,r=1` T04 subset. Native direct evidence begins with code `777` on printed page 60 and ends with code `1599` on printed page 70. Page 71 switches to mobile automata and is a construction boundary. A code label is program evidence; a single-gray start, stable-white selection, random field, behavior class, horizon, crop, and palette remain run/property/view evidence.

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
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_253_Picture_1.jpeg` | 511,097 | `1227x1519` | `148a433a11b4889c91c1a7be3c6f00172a3961428e6d41c47a06954136245faf` | Class-4 code `238`; same disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_254_Picture_1.jpeg` | 568,496 | `1117x1383` | `d32b7fc3dedc9f262e5a3d3d928d1d7d94d1a219fd75aeeefdb988c74869a168` | Class-4 code `2043`; same disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_2.jpeg` | 7,400 | `273x171` | `b175f64e60cf41042d8ba6a11ed8d04eec4a8101bef8f9f231aae532eca6ca06` | Borderline-class code `219`; classification is a property. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_3.jpeg` | 13,612 | `259x167` | `00ef0063254d4f75734cd76d8f2d07de4ae1d6b041b9664197c2da99641d8b14` | Borderline-class code `438`; same disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_4.jpeg` | 9,310 | `267x186` | `700d71a0beb145c953ca87f4d8649aecd7b7d60df69ccd569cba02f6daeb1acc` | Borderline-class code `1380`; same disposition. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_255_Picture_5.jpeg` | 11,188 | `273x165` | `ae44e4411841a03fced5b5114f6cef4be62793c6a58c9a4ce6c357d214c7ce35` | Borderline-class code `1622`; same disposition. |
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
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_74_Picture_5.jpeg` | 134,131 | `858x423` | `713c4c55c6a004d76c5e47f1f39513bb1656f35feb0fe9aa72c4503ca311cdc6` | Immediate preceding rule-73 ECA: two-color exhaustive ordered rule. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_86_Picture_7.jpeg` | 30,221 | `240x500` | `59213fbf1a0e6904a6566043c889acd32853d799d5a71bfec1e2d0c45bb1eec5` | First post-T04 mobile evolution: one active site and sequential movement. |
| `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_86_Picture_8.jpeg` | 7,295 | `506x51` | `d844f2419d7ff2a748a93e4ae6dd09c947bf5ed0723aa1defb4354c810b1fb25` | Mobile rule diagram paired with Picture 86/7; all later mobile galleries inherit this boundary. |
| `CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_171_Picture_5.jpeg` | 4,640 | `277x91` | `6695e1c946cf6adaa04a3915f2c720f69de4d18b74a81a01aaab346052119455` | Continuous gray average-map analog; continuous codomain, not three colors. |
| `CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_185_Picture_9.jpeg` | 3,425 | `213x114` | `abfbc90a8bdab839ac452194adf8f7e30258e877967a79ac71db59b1a716df75` | Two-dimensional center-plus-four-neighbor totalistic form; different support. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_248_Figure_2.jpeg` | 281,697 | `1086x1389` | `b2a20cb8095eb211fedd963d622222ca98fe0428f397b71bef90db8fa6871957` | Binary radius-two totalistic gallery; lower color count and larger radius. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_256_Figure_2.jpeg` | 328,297 | `1092x1367` | `1c4967f6967d8e813b2a281e2615dc8bef272eb57789b60e23c950de5e6bc01f` | Four-color radius-one totalistic class sequence; T05 rather than T04. |
| `CHAPTERS/6-Starting-from-Randomness/Images/_page_261_Figure_2.jpeg` | 309,273 | `1109x1297` | `49f35fe65202ef7fbfee2da92b7460d36fc329b66a553782ebf8991f237944dd` | Two-dimensional five-cell totalistic random gallery. |
| `CHAPTERS/10-Processes-of-Perception-and-Analysis/Images/_page_566_Figure_2.jpeg` | 140,400 | `1032x699` | `6d66d95c8e3c286272cded005d60557ce7a075ffebfd268486c23abe13a29a1e` | Two-dimensional outer-totalistic codes `54,222,374`; center is retained separately. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_769_Figure_1.jpeg` | 298,516 | `1065x1308` | `a980effe214906d991e8ca9180cb9f9d6eade2f978a8358487a60bb1728058f3` | Four-color totalistic code `1004600`; higher-color control. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_897_Picture_19.jpeg` | 37,091 | `553x155` | `2cedbff5433363c86786feea8804c95229179daf455f07ee8071d6345223894b` | Binary radius-two code `10`; direct T03 evidence but lower-color/radius control for T04. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_897_Picture_20.jpeg` | 77,026 | `543x329` | `ee9cadafa6b0b5a45d9cfb4ed310aff751e84f46a86277821e9f971f3c067b3f` | Long companion view of the same code-`10` control. |
| `BACK-MATTER/Index/Images/_page_963_Picture_8.jpeg` | 3,114 | `144x152` | `1fb4f0b4c03d8ba9f9fdeb67a0bbda2d786ed7ceeb13cdd8c31337ccd54bcdfb` | Frequency chart `k=2,r=1`; lower-color control. |
| `BACK-MATTER/Index/Images/_page_963_Picture_9.jpeg` | 3,226 | `136x148` | `515f5de1423a9164ed6def92d786346f64c15a0a87ba07b723c069e62829caf6` | Frequency chart `k=2,r=2`; lower-color/radius control. |
| `BACK-MATTER/Index/Images/_page_963_Picture_10.jpeg` | 3,654 | `138x158` | `4b5ff621a668c5b706cdec0481cf3849facb7395d256dfd7c39b471d95fd018f` | Frequency chart `k=2,r=3`; lower-color/radius control. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_23.jpeg` | 4,478 | `160x117` | `132528352f363e52a20e73e1e8341203126448c0c6c8545eed48626eaddac16c` | Adjacent `k=3,r=1` general ordered-table code `921408`; T02, not totalistic. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_28.jpeg` | 5,342 | `205x110` | `2da239aceec3720e5aeccd5de8898c37fe7e975230814c0b3a8e3dcacbde9096` | Adjacent function-callback neighborhood rule; not a seven-row T04 table. |
| `CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_31.jpeg` | 4,370 | `117x117` | `ca086555513a6d8ba5bcbe92d97af26e55aa899cf629e0ab61d8fa8c71b81586` | Adjacent 2D nine-neighbor totalistic code `3702`; different geometry. |

The monolith omits `Images/` from links; chapter splits reference these same bytes rather than duplicate files. Page-883 assets are Notes-for-Chapter-2 evidence despite Chapter-12 placement. Page-963 Notes charts are physically under `BACK-MATTER/Index/Images`. The T03 audit pins the superset, but the independent oracle below is authoritative for T04's 29 included, 18 excluded, and one relation-only dispositions.

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
'CHAPTERS/9-Fundamental-Physics/Images/_page_541_Picture_3.jpeg':(37411,436,268,'83d828ba45f3f3e7390bf66183643a32c3c7b83646cc3880aedf099a49284c1e','I'),
'CHAPTERS/9-Fundamental-Physics/Images/_page_541_Picture_4.jpeg':(43238,418,250,'d96c865b43b912ce4e2d6f0c2ddf659eed32f17db48c151161c364187fcc7a1f','I'),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_707_Figure_1.jpeg':(327160,1130,1111,'974e12d28e8acc6fb4af26f7b1dd09eae1f30d802666a61f41abed8ec2d42e19','I'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_753_Picture_3.jpeg':(164036,912,565,'8cfad05d53abb9791d37dd6d8262ec12dbc08bb1d72866ce34c46ecb99a94a88','I'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_25.jpeg':(5511,211,117,'d53637ce9ec50330d5fa6239b23f48d57b563266a0085a23517d4538020fd5fb','I'),
'BACK-MATTER/Index/Images/_page_963_Picture_11.jpeg':(3717,136,152,'7c660bbbb03b2d3116aab32cd50a5a3ff094961d49b403148531b36759335d6b','I'),
'CHAPTERS/11-The-Notion-of-Computation/Images/_page_670_Figure_1.jpeg':(281966,1064,1224,'a1a2a5c04b509ecc0357273387b2950d179478c65406427751904987ec9e8d3e','R'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_74_Picture_5.jpeg':(134131,858,423,'713c4c55c6a004d76c5e47f1f39513bb1656f35feb0fe9aa72c4503ca311cdc6','X'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_86_Picture_7.jpeg':(30221,240,500,'59213fbf1a0e6904a6566043c889acd32853d799d5a71bfec1e2d0c45bb1eec5','X'),
'CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_86_Picture_8.jpeg':(7295,506,51,'d844f2419d7ff2a748a93e4ae6dd09c947bf5ed0723aa1defb4354c810b1fb25','X'),
'CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_171_Picture_5.jpeg':(4640,277,91,'6695e1c946cf6adaa04a3915f2c720f69de4d18b74a81a01aaab346052119455','X'),
'CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_185_Picture_9.jpeg':(3425,213,114,'abfbc90a8bdab839ac452194adf8f7e30258e877967a79ac71db59b1a716df75','X'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_248_Figure_2.jpeg':(281697,1086,1389,'b2a20cb8095eb211fedd963d622222ca98fe0428f397b71bef90db8fa6871957','X'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_256_Figure_2.jpeg':(328297,1092,1367,'1c4967f6967d8e813b2a281e2615dc8bef272eb57789b60e23c950de5e6bc01f','X'),
'CHAPTERS/6-Starting-from-Randomness/Images/_page_261_Figure_2.jpeg':(309273,1109,1297,'49f35fe65202ef7fbfee2da92b7460d36fc329b66a553782ebf8991f237944dd','X'),
'CHAPTERS/10-Processes-of-Perception-and-Analysis/Images/_page_566_Figure_2.jpeg':(140400,1032,699,'6d66d95c8e3c286272cded005d60557ce7a075ffebfd268486c23abe13a29a1e','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_769_Figure_1.jpeg':(298516,1065,1308,'a980effe214906d991e8ca9180cb9f9d6eade2f978a8358487a60bb1728058f3','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_897_Picture_19.jpeg':(37091,553,155,'2cedbff5433363c86786feea8804c95229179daf455f07ee8071d6345223894b','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_897_Picture_20.jpeg':(77026,543,329,'ee9cadafa6b0b5a45d9cfb4ed310aff751e84f46a86277821e9f971f3c067b3f','X'),
'BACK-MATTER/Index/Images/_page_963_Picture_8.jpeg':(3114,144,152,'1fb4f0b4c03d8ba9f9fdeb67a0bbda2d786ed7ceeb13cdd8c31337ccd54bcdfb','X'),
'BACK-MATTER/Index/Images/_page_963_Picture_9.jpeg':(3226,136,148,'515f5de1423a9164ed6def92d786346f64c15a0a87ba07b723c069e62829caf6','X'),
'BACK-MATTER/Index/Images/_page_963_Picture_10.jpeg':(3654,138,158,'4b5ff621a668c5b706cdec0481cf3849facb7395d256dfd7c39b471d95fd018f','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_23.jpeg':(4478,160,117,'132528352f363e52a20e73e1e8341203126448c0c6c8545eed48626eaddac16c','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_28.jpeg':(5342,205,110,'2da239aceec3720e5aeccd5de8898c37fe7e975230814c0b3a8e3dcacbde9096','X'),
'CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_883_Picture_31.jpeg':(4370,117,117,'ca086555513a6d8ba5bcbe92d97af26e55aa899cf629e0ab61d8fa8c71b81586','X'),
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
assert counts=={'I':29,'X':18,'R':1}
print('T04 metadata oracle: PASS 29 included; 18 excluded; 1 relation-only')
PY
```

Recorded output:

```text
T04 metadata oracle: PASS 29 included; 18 excluded; 1 relation-only
```

### Exact T04 asset semantic oracle

This dependency-free oracle re-establishes the T04 subset rather than importing T03's result. It checks the seven-row base-3 codec, code `777`, the exact code-`867` Notes invocation, every strict labelled code, the 50-picture scan, and the distinction between that scan and all 729 stable-zero-background T04 rules.

```bash
python3 - <<'PY'
from hashlib import sha256

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
for code in (1815,2007,238,2043,219,438,1380,1622,294,1893): table(code)
class4=(357,438,600,792,924,1038,1041,1086,1329,1572,1599,
        1635,1662,1815,2007,2049)
assert all(0<=code<2187 for code in class4)

print('code777_table=',r777,'display=1001210')
print('code777_t0_t8=',','.join(words))
print('code867_51x101_sha256=',sha256(blob).hexdigest())
print('page76_selection=',len(strict['p76']),'all_quiescent=',len(all_quiescent))
print('T04 asset semantic oracle: PASS')
PY
```

Recorded output:

```text
code777_table= (0, 1, 2, 1, 0, 0, 1) display=1001210
code777_t0_t8= 1,111,12121,1100011,122101221,11001210011,1221110111221,110001222100011,12210110101101221
code867_51x101_sha256= 185170c0866f76d129fbf3a8843cc731f98b9f012cb98286f01e420532fb53d9
page76_selection= 50 all_quiescent= 729
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

Picture 883/25 has exact executable settings and therefore receives a semantic trajectory digest. Its tiny ungridded JPEG does not state crop/resampling, so it is not forced into a pixel fit. The other galleries omit at least one of serialized seed/random sample, boundary/background, initial-state-versus-update horizon, crop, palette, or resampling; no additional trajectory or raster golden is fabricated.

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
3. Extend `src/ca/specs.py` only at the preset/configuration boundary so a JSON-safe record such as `{"preset":"three_color_totalistic","code":{"kind":"nonnegative_integer","decimal":"777"}}` resolves before `Dynamics` construction. The resolved record must serialize the explicit valuation, arity-three equal-sum domain, seven structural outputs, and optional tagged code exactly like generic T03. Reject unknown or conflicting fields rather than ignoring them.
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

1. Assert preset and generic T03 construction compare structurally equal, share the same semantic program reference/hash and runtime classes, and generate identical scalar and batch traces for both code and table input. Catalog provenance may differ; semantic identity may not.
2. Assert table/code round trips for `0,1,420,777,867,2186`; sum zero is least significant; leading zero rows survive; and output value `2` is produced. Reject codes `-1` and `2187`, booleans/floats/strings outside the tagged manifest codec, six/eight-row tables, sparse mappings, and outputs outside `0..2`.
3. Assert the preset has no `k`, `r`, valuation, aggregate, alphabet, arity, executor, update, seed, boundary, filter, class, or palette override path. Equivalent generic T03 with a noncanonical symbolic valuation remains valid but is not silently relabeled T04.
4. Execute code 777 from the single-gray run and match the exact early trace; execute code 867 and match the shared hash. Run the same program under point-`2`, explicit, random, all-zero, periodic, and fixed-exterior profiles and prove only run/realization identities change.
5. Execute code `1` from an all-zero field and prove the background changes. This rejects fusion of T06 or the page-76 filter. Independently assert exactly 729 codes satisfy `code mod 3=0`, while the 50 displayed codes equal `range(993,1141,3)` and do not exhaust them.
6. Evaluate `(0,2,0)` and `(1,0,1)` through a table whose row two is distinctive: both address sum row two despite different histograms. Reverse representative triples and prove equal output without a runtime `symmetric` flag; perform additivity checks for code 420 only in the analyzer/property API.
7. Render one unchanged episode with two palettes and prove the program reference and raw states are identical. Changing gallery labels, class records, crop, horizon, or raster metadata must likewise leave the program unchanged.
8. Static-scan resolved objects and runtime sources: no T04/three-color family dispatch, duplicate sum/table/codec, binary shift decoder, hidden `3^3=27` exhaustive table, callback, preset-specific `int64` exception, seed/filter/palette default, or test-only execution path.
9. Preserve all G2-T03 generic/radius/bigint adversaries and the full existing suite. T04's small values cannot weaken generic valuation, arbitrary-precision, old-snapshot, nonbinary, and scalar/batch requirements.

**Completion evidence:** the preset resolves identically to generic T03; exact code/table/count/trace/selection fixtures pass; invalid codes/tables/overrides are rejected; seed, boundary, T06/T07/T08, property, gallery, palette, and view identities remain separate; static inspection finds no new runtime branch or duplicate semantics; focused and full repository tests pass unchanged.

## No-Cheating Checks

- No T04/three-color rule family, `if k==3` runtime case, duplicate aggregate/table/codec/executor/update, ternary patch beside the shared T03 rule, or preset-specific scalar/batch path.
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
- [ ] The exact preset/program/run/property/view boundary and T03/T05/T06/T07/T08 relationship are proved.
- [ ] Current API/runtime fit and a concrete Goal 2 preset/conformance stage are implementation-ready.
- [ ] Global ledgers, independent review, embedded checks, coverage/diff gates, and repository tests pass.

## Stage Results

In progress. Initial evidence supports a strict T03 preset; exhaustive closure has not yet proved it.

## Integration Results

In progress. No global decision changes until the T04-specific audit closes.
