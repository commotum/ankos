# 11-CH07-MECHANISMS

Status: **COMPLETE**.

## Current Facts

- Stage 11 completely reviews the paired Chapter 7 assignment without using
  the existing catalog, Goal 1/2 conclusions, API documents, or runtime
  capabilities as discovery evidence.
- All 713 assigned source units are reviewed:
  - 435 main-text units, `U001577..U002011`;
  - 278 Notes units, `U006592..U006869`.
- All 194 assigned physical images are screened at original resolution:
  - 92 referenced main-text images;
  - 102 Notes images, comprising 43 referenced images and 59 unreferenced
    physical images.
- The terminal review event is `V000034`, in discovery epoch 2. The valid live
  state contains 14,311 source units, 4,045 reviewed units, 1,413 active blind
  candidates, 708 routes, 1,607 physical images of which 882 are screened,
  and 18 closed LOCAL rounds.
- The four canonical Stage 11 transactions are:
  - `V000031` (`INITIAL`): reviewed both paths, screened all 194 assets,
    created `B1251..B1413`, appended 596 evidence records
    `E005191..E005786` in 367 groups `G004986..G005352`, and created
    `R000568..R000708`. Its event hash is
    `7ed422b6525a82a18c350b65724fb84d500f527da9789d57acdc7708ed765a8e`;
  - `V000032` (`ROUTE_RESOLUTION`): resolved all 41 Stage 11 within-stage
    routes and all 22 reachable incoming cross-range routes without changing
    candidates, readings, or assets. Its event hash is
    `8591957742594eaa43c969cab60b8b61a730854977910bdafc0c7088ac16c885`;
  - `V000033` (`SEARCH_APPEND`, `S017`): recorded 2,478 fully dispositioned
    hits and added 191 candidate-derived vocabulary terms with no new
    candidate, evidence, or route. Its event hash is
    `7be9a15996d4a682ecd4778c22ec79a5d93ead82b1edff8ec38e14aade61ae83`;
  - `V000034` (`SEARCH_APPEND`, `S018`): repeated the identical normalized
    search projection with zero vocabulary, candidate, evidence, route,
    reading, asset, or candidate-record delta. Its event hash is
    `d1f928b7fa742c246d5f63de164f56139b6a7fdf367a7575f75633e0239e6357`.
- Globally, all 1,413 candidates `B0001..B1413` are active. Of the 708 routes,
  335 are resolved and 373 are pending: 245 resolved `WITHIN_STAGE`, 90
  resolved `CROSS_RANGE`, and 373 pending `CROSS_RANGE`.
- The six terminal mutable-ledger hashes are:
  - `reading-ledger.csv`:
    `9bb64de8b08873355191bd404febc5895f9c6e772706c291865cb6e83607232d`;
  - `candidate-ledger.jsonl`:
    `8676464e94072acec5bcfa03b98d056018dfbc77bd7915d4a647bbfc46ec1442`;
  - `cross-reference-ledger.csv`:
    `8f3cd4b4bbd793410f511be5b899224a5a09b06f8b1ba053929f0b0774434748`;
  - `asset-ledger.csv`:
    `717e20c259292fab63f40e3a34de76cff7770c4c288d741a8310c491e58db881`;
  - `search-rounds.json`:
    `c2c0cdfb2992baa9ecb0038cb7a853706a7ef8c15db01efed72f8265283fc1e2`;
  - `review-history.jsonl`:
    `f64e62531e64c39a36cb4fd8ed83e271fe30fa267c9fccd016e634aa517d5e0f`.

## Updated Assumptions And Findings

- Random initial data, random event selection, stochastic transition laws,
  deterministic intrinsic randomness, finite realizations, ensemble
  distributions, and observers remain mechanically distinct.
- Physical interpretations and explanatory applications are not independent
  native constructions unless the reviewed source supplies an independent
  state, transition, coupling, event-selection, solution, or sampling law.
- Aggregation, constraint satisfaction, continuum relations, discrete
  approximations, optimization procedures, and observation protocols retain
  their native directionality, schedule, probability, stopping, and result
  semantics.
- The assignment independently supports construction-bearing records spanning
  randomness mechanisms and generators, mechanical maps, random walks,
  aggregation systems, cellular automata, constraint and optimization
  procedures, PDE relations and analyzers, statistical measures, geometric
  constructions, language relations, and sandpile systems. These records
  remain deliberately uncollapsed.
- Exact rule numbers, formulas, branch presets, probability measures, and
  construction-bearing image content were retained only where the reviewed
  source supports them. Missing laws and defective or conflicting source
  material remain explicit evidence boundaries.
- Image filenames use PDF-page numbers while route literals use printed-page
  numbers. Stage 11 route closure used the printed main range `297..360` and
  printed Notes range `969..990`; it did not infer targets from superficially
  similar image filenames.
- A route whose literal target spans reviewed and unreviewed pages is not
  partially resolved. The mixed `pages 1029 and 986` obligation remains
  pending until both targets have been reviewed.
- Candidate count is deliberately not a semantic-family count. No blind
  candidate was merged, mapped to a T identifier, assigned an API fit, or
  given a final catalog/family action in this stage.

## Source And Asset Coverage

| Assignment | Source units | Reviewed | Physical images | Screened |
|---|---:|---:|---:|---:|
| Chapter 7 main text | 435 | 435 | 92 referenced | 92 |
| Chapter 7 Notes | 278 | 278 | 43 referenced + 59 unreferenced | 102 |
| **Total** | **713** | **713** | **194** | **194** |

`A001041` and `A001057` are Stage 5-owned shared assets and were therefore not
pending Stage 11 work.

The final source-unit dispositions are:

| Disposition | Main | Notes | Total |
|---|---:|---:|---:|
| `SUPPORTS_CANDIDATE` | 97 | 152 | 249 |
| `CANDIDATE` | 71 | 77 | 148 |
| `NO_CONSTRUCTION` | 189 | 14 | 203 |
| `REPRESENTATION_OR_OBSERVER` | 73 | 14 | 87 |
| `CROSS_REFERENCE` | 1 | 9 | 10 |
| `APPLICATION_OR_EMULATION` | 0 | 7 | 7 |
| `SOURCE_DEFECT_OR_AMBIGUITY` | 4 | 3 | 7 |
| `HISTORICAL_ONLY` | 0 | 2 | 2 |
| **Total** | **435** | **278** | **713** |

The main-text units have 431 `CLEAR`, two `AMBIGUOUS`, and two `DEFECTIVE`
source statuses. The Notes units have 275 `CLEAR` and three `CONFLICTING`
source statuses.

The 194 image roles are:

| Visual role | Main | Notes | Total |
|---|---:|---:|---:|
| `RELATION` | 57 | 89 | 146 |
| `NATIVE_EVIDENCE` | 22 | 9 | 31 |
| `OBSERVER` | 7 | 4 | 11 |
| `CONTROL` | 4 | 0 | 4 |
| `SOURCE_DEFECT` | 1 | 0 | 1 |
| `DECORATIVE` | 1 | 0 | 1 |
| **Total** | **92** | **102** | **194** |

All 92 main images and all 102 Notes images received original-resolution
review. Transcription is `CHECKED` for 91 main and 89 Notes images and
`NOT_REQUIRED` for the remaining 14. Main asset source status is 90 `CLEAR`
and two `DEFECTIVE`; Notes asset source status is 43 `CLEAR` and 59
`AMBIGUOUS`. The 59 unreferenced Notes images remain ambiguous physical
source records rather than independent semantic authority.

## Candidate Changes And Evidence Boundaries

- Sequential review created 163 active candidates, `B1251..B1413`:
  - main: 82 candidates `B1251..B1332`, with 286 evidence records and 286
    groups, `E005191/G004986..E005476/G005271`;
  - Notes: 81 candidates `B1333..B1413`, with 310 evidence records
    `E005477..E005786` in 81 groups `G005272..G005352`.
- The 596 evidence records comprise 329 `DIRECT_PARTIAL_MECHANICS`, 33
  `DIRECT_COMPLETE_MECHANICS`, 27 `DIRECT_IDENTITY`, 109 `CORROBORATING`,
  and 98 `CONTEXTUAL` records. Their modalities are 403 prose, 135 image, 41
  code, and 17 formula records.
- The 4,564 fingerprint fields comprise 3,056 `SUPPORTED`, 502
  `UNKNOWN_FROM_SOURCE`, 1,002 `NOT_APPLICABLE`, and four
  `CONFLICTING_SOURCE` fields. No supported field relies only on weak
  evidence.
- The candidates retain 502 explicit missing-mechanics occurrences across 322
  distinct source-limited statements, ranging from zero to ten per candidate.
  These are evidence boundaries, not unresolved sequential-review work.
- The candidate suffix records 118 typed parameters and 140 typed variants.
  Parameters and variants remain source-specific rather than being generalized
  across superficially similar candidates.

## Route Closure

- The complete Stage 11 relationship universe contains 163 routes: 141 owned
  routes `R000568..R000708` and 22 reachable incoming routes.
- The 141 owned routes comprise 41 `WITHIN_STAGE` routes and 100
  `CROSS_RANGE` obligations; 137 are page routes and four are section routes.
- `V000032` resolves all 41 within-stage routes and these 22 incoming routes:
  `R000008`, `R000049`, `R000065`, `R000077`, `R000083`, `R000090`,
  `R000147`, `R000168`, `R000177`, `R000230`, `R000244`, `R000289`,
  `R000296`, `R000297`, `R000320`, `R000416`, `R000424`, `R000497`,
  `R000507`, `R000514`, `R000515`, and `R000516`.
- The final Stage 11 relationship split is therefore 41 resolved
  `WITHIN_STAGE`, 22 resolved incoming `CROSS_RANGE`, and 100 pending outgoing
  `CROSS_RANGE`. One existing mixed-range obligation remains deliberately
  deferred rather than partially resolved.
- The 163 candidates carry 120 candidate-to-route links to 108 unique owned
  routes. Every one of the 141 owned routes is also attached to exactly one
  reviewed source unit.
- The frozen route specification digest is
  `b302292926ebba64e44857aa9b5481d5308713d846d1af5bb4eed9fc480cc8a2`;
  the preservation digest covering the 100 untouched outgoing routes and one
  deferred mixed-range route is
  `c2d2b5eed2f0a19fe1072cbfd32dd0ee78e79058d4ba5a5164196a6fb0d897ac`.

## Search And Evidence Log

`S017` and `S018` each use 15 frozen query families over exactly the two
assigned paths. Each round contains 2,478 fully dispositioned query/unit pairs
across 704 of the 713 source units:

| Scope | Query/unit pairs | Unique units |
|---|---:|---:|
| Chapter 7 main text | 1,419 | 432 / 435 |
| Chapter 7 Notes | 1,059 | 272 / 278 |
| **Total** | **2,478** | **704 / 713** |

The per-family hit vector in both rounds is:

```text
[104, 282, 78, 84, 89, 84, 59, 36, 210, 645, 200, 160, 83, 209, 155]
```

Each round has 1,692 `GOVERNED_CANDIDATE_OR_SUPPORT` hits, 644 `EXCLUSION`
hits, 97 `CROSS_REFERENCE` hits, and 45 `CONTROL_OR_RELATIONSHIP` hits. Each
round also reproduces 2,063 candidate links and 1,077 route links.

- `S017` uses `Q0209..Q0223` and `H018631..H021108`. It adds 191
  candidate-derived vocabulary terms, taking the global vocabulary from 716
  to 907, with no new candidate, evidence group, or route. Its ID-sensitive
  result/rerun digest is
  `468f300c470f61dedbe0493a60d54e02f3eb74894ed08036570390b7749827db`.
- `S018` uses `Q0224..Q0238` and `H021109..H023586`. It adds no vocabulary
  and no semantic delta. Its ID-sensitive result/rerun digest is
  `a546b8f88ecde0d3d44ae5550b53bea022c13df4fec2e67a7caf01bf82ede434`;
  after normalizing allocated query and hit IDs, its source-result and semantic
  projections are byte-identical to `S017`.

The frozen search projections are:

- query specification:
  `9a7790adeeb39626e5234f06596b731571e0f6729ab1b3e58eee4e03f5a4502c`;
- Stage 11 vocabulary suffix:
  `992dd09abae87cf800a3401591d28d3a2068a9133a39bcac33103bbc0ad74005`;
- terminal 907-term vocabulary:
  `786ca2acc4b7aba9545363c7fbc6fec49b6c95eea267153de081f2af7cf337cd`;
- Stage 11 unit IDs:
  `60046d02679da034b9579d21b8aee9bedc9a2de89251af3cfa9a6683eb14ad05`;
- Stage 11 source-unit projection:
  `7b04501d101772fa173b4472e6cade05244322c86d2cda3580680d62b37ab849`;
- normalized query/unit results:
  `c604632660a66ca6c815be6ecb03e6a6d0c2505b95082ee010a8154429fcb69d`;
- result-unit IDs:
  `effa31eb78c02cfc76773c2b58fe7a26de2778aefb9facb12132c9a0089a8e8b`;
- reviewed-reading projection:
  `aefbfea99a0e698e1e30112cd703a1c732b368f474d818f03ce53218c055d4dd`;
- screened-asset projection:
  `b7b4e5ff2489d64701bb07b4d9b82688fca33d86bcbe42a80f56a633c584d864`;
- Stage 11 candidate IDs:
  `f7fdb657ab7bb6e59118c8a7367ec8d5da7a09caa6ad80ab169b66503e6a0890`;
- search triage:
  `3309da9bb6b23203230d95d954ebd35cd5e1fb3af1363841296df1a5a5a6ca50`;
- candidate coverage:
  `3496212836e9a84a6b01f393f7b8b65937f0f868d2cb594251e5e909811532b4`;
- 489-item omission challenge:
  `9ac5e8254b78d9303fc096775517b67fbe35375bebc45a0149dc7d4072a3c044`;
- 163-route coverage projection:
  `3f919f6a25195bb972da04af1675b7faff64bc17cfbb0bd026d51b5acff462ab`;
- normalized hit projection:
  `0aa120c8aa645bd7846f789a7126066a9fdff14465b84ee153fbe2cefdd67946`.

These rounds establish local Stage 11 closure. `fixed_point` remains null; the
whole-corpus fixed point is reserved for Stage 18.

## Frozen Review Artifacts

- The canonical source hashes are
  `e052f275ea7519f2e8c270f1dd68eac01d123aa3b73355eff5803f02708e542d`
  for the main path and
  `fd8696100529789964578841267bbd841411691d05248840ede6e0b4b7bd69f3`
  for the Notes path.
- Main review:
  - sealed content-set hash:
    `346d4da6a8f58c547a66371022de8806d0d55c6b652648c20928fafd53927f28`;
  - final output hash:
    `0e848b333344c9eeb5615cfeb7a419e561f0d5418be071c711b618fe5e0cd723`;
  - authoring-helper hash:
    `4a23eab311869c65b4e94be86cc2f57a63d77d1858f2bc671275110d91e59d2f`.
- Notes review:
  - sealed content-set hash:
    `91458ef7c19a113cc438becd33c013328e52346b9c5f57b52525d46759d99735`;
  - final output hash:
    `a6ab83da23a5edfd412ded53b10931c95c43acee6bcabe5412003079447617a6`;
  - authoring-helper hash:
    `a633f3c5d6ab0a1272f8a48f17409653da4a8d726e3708d1de40728d7b9210cb`.
- The pristine paired-union content-set hash is
  `5f084566dfd0fbae8a1323aa5c7d43dda3d6ad1994c0c7d0eaee02d4b704985e`.
  The finalized paired-union output hash is
  `496a83a797358545d2d6a4443aa8cdec349ab5a6372a25cb815818436a20395a`.
  Independently regenerated original, fresh, ordinary, and optimized outputs
  are byte-identical at 713 readings, 194 assets, 163 candidates, and 141
  routes.
- The frozen route-helper hash is
  `60070032daa6d39d663c4de5c9a60f109a15f040a9a1d17fdde5f4684b18d1f8`;
  its 63-update proposal hash is
  `6fc08356f0f7fbd5a47a0d85cbbf331ab53255638c4236c5c2bac344cd9001d8`.
- The frozen search-helper hash is
  `b67b5034878b272f7b09046273c141c667fa4e7b5f9425737fca3c2da5a57d7d`;
  the `S017` and `S018` proposal hashes are respectively
  `27fe6ec66c384195aa160e5352c60cd78c6e5959032958cefcbf2dbb73db5de8`
  and
  `41cc1d5281cf4ca6d10a42aa733d3bbfda7f8303ed419afd1219dcbd27731e9a`.

## Verification And No-Cheating Checks

- The main and Notes reviews were completed as disjoint sealed epoch-2
  assignments before their semantic outputs were combined. Their original,
  fresh, ordinary, and optimized projections agree exactly.
- All 713 reading rows and 194 asset rows have explicit nondefault
  dispositions; every original-resolution transcription and direct image
  evidence link is traceable.
- Search began only after sequential review and route closure. Its scope is
  exactly the paired Stage 11 paths, every hit reproduces, and every hit has
  one disposition.
- Main, Notes, paired-union, route, and search hostile terminal reviews all
  returned `ACCEPT`.
- Ordinary and optimized validation both pass with the identical exact output:
  `validated blind audit harness: units=14311 reviewed=4045 candidates=1413
  routes=708 assets=1607 screened=882 rounds=18`.
- Ordinary and optimized corpus verification both retain exactly 29
  documents, 1,607 physical images, and 14,311 source units.
- The complete regression suite passes: `110 passed in 769.66s`.
- The review-history chain replays through `V000034`, and the six terminal
  ledger hashes in **Current Facts** are exact.
- Blind artifacts contain no T mappings, catalog actions, API-fit fields, or
  runtime conclusions. Goal 1, Goal 2, the catalog, API documents, runtime
  code, and Stage 12 or later Book source were not used or opened during
  Stage 11.

## Completion Requirements

- All 435 main and 278 Notes units are individually reviewed: **met**.
- All 92 main and 102 Notes images are screened at required depth: **met**.
- Both split outputs and their canonical union pass complete disjoint
  coverage and verification: **met**.
- Every candidate has source-limited provenance, a complete fingerprint,
  result kind, parameter/variant support, and explicit evidence limits:
  **met**.
- Exactly one Stage 11 `INITIAL` transaction is applied and replays: **met**.
- Every reachable incoming and within-stage route is resolved: **met**.
- Every exact-scope LOCAL hit is dispositioned and an identical normalized
  zero-delta rerun is applied: **met**.
- Ordinary/optimized audit, corpus, route, history, scope, hostile,
  full-regression, compilation, Markdown, and whitespace gates pass: **met**.
- This report and `0-plan.md` record the exact Stage 12 handoff: **met**.

## Stage Results And Stage 12 Handoff

Stage 11 is terminal at `V000034`, epoch 2, with 4,045/14,311 source units
reviewed, 882/1,607 images screened, 1,413 active candidates, 708 routes
(335 resolved and 373 pending), and 18 LOCAL rounds. The six terminal hashes
in **Current Facts** are the only valid Stage 12 starting hashes.

Stage 12 owns exactly two still-pending canonical assignments:

| Assignment | Source units | Physical images |
|---|---:|---:|
| `CHAPTERS/08-Implications-for-Everyday-Systems/08-Implications-for-Everyday-Systems.md` | 385, `U002012..U002396` | 45 referenced: `A001122..A001126`, `A001128..A001138`, `A001142..A001143`, `A001148..A001151`, `A001153..A001162`, `A001165..A001177` |
| `BACK-MATTER/NOTES/08-Implications-for-Everyday-Systems-Notes/08-Implications-for-Everyday-Systems-Notes.md` | 125, `U006870..U006994` | 12 referenced + 29 unreferenced: referenced `A000019`, `A000024`, `A000034..A000038`, `A000046`, `A000049`, `A000054..A000055`, `A000059`; unreferenced `A000020..A000023`, `A000025..A000033`, `A000039..A000045`, `A000047..A000048`, `A000050..A000053`, `A000056..A000058` |
| **Total** | **510** | **86** |

The main source hash is
`5e794cedc877e539e30d9ef6102fea18f4533c56d3324f7d454326336e4a2004`;
the Notes source hash is
`3acc85433fca526eca898e6a0f116fc1017b88bb7b0048fc8f96f7d0afcead53`.
All 510 reading rows and all 86 asset rows are `PENDING`; no asset in this
assignment is shared or already owned by an earlier stage.

This handoff was derived only from the terminal Goal 4 ledgers and corpus
manifest. No Stage 12 Book source was opened. The next safe action is to
create the Stage 12 report from this hash-pinned ledger-only baseline,
reconfirm the ordinary/optimized terminal gates, build two disjoint sealed
epoch-2 bundles, and begin independent sequential review at `U002012` and
`U006870`.
