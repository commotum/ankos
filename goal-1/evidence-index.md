# Goal 1 Evidence Index

This ledger is the authoritative coverage join between `ref/notes/CA-Types.csv`, the numbered taxonomy sections in `ref/notes/CA-Types.md`, Goal 1 evidence stages, and the eventual Goal 2 conformance obligations. `CA-Types.md` supplies search vocabulary only; book evidence must come from the canonical monolith.

## Status Vocabulary

- `PENDING`: the type stage has not begun.
- `IN PROGRESS`: the stage file exists but at least one completion requirement remains unproved.
- `REOPENED`: later evidence invalidated a completed conclusion and the stage must be re-derived.
- `COMPLETE`: every candidate match is resolved, all unique construction-relevant excerpts are recorded, the construction and variants are reconstructed, API/runtime/principles fits are audited, the Goal 2 handoff is implementation-ready, and global integration is current.

Only `COMPLETE` counts toward the 45-type coverage total. A search hit, a taxonomy summary, or a plausible API fit never changes status by itself.

## Evidence Record Contract

Each type stage must make the following auditable:

1. Exact CSV identity, taxonomy section, aliases, variants, examples, parameters, and cross-referenced systems.
2. Reproducible searches of `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`, including direct terms, captions, Notes, Index entries, and vocabulary discovered from cross-references.
3. Disposition of every candidate as included evidence, duplicate, followed cross-reference, or false positive, with no silent remainder.
4. Every unique construction-relevant excerpt verbatim with canonical path, exact line range, section context, and the fact it establishes.
5. Evidence-first construction reconstruction, current API/runtime comparison, principles audit, rejected shortcuts, no-cheating checks, and Goal 2 implementation/conformance handoff.
6. Re-integration into this ledger, `design-ledger.md`, and `0-plan.md`, including any reopened stage.

## Catalog Coverage

| ID | CSV line | Catalog type | Taxonomy section | Execution stage and file | Status | Searches / excerpts / unresolved candidates |
|---|---:|---|---:|---|---|---|
| T01 | 2 | Elementary Cellular Automata | 1 | `2-T01-ELEMENTARY.md` | COMPLETE | 8 search families; 23 excerpt groups; all split/Notes/Index/cross-reference candidates dispositioned; 0 unresolved |
| T02 | 3 | Multi-Color Nearest-Neighbor Cellular Automata | 2 | `21-T02-MULTICOLOR-CA.md` | COMPLETE | Exact 29-query/157-candidate partition; 21 evidence groups; 48 verbatim fragments; ordered `k^3` table/base-`k` codec; 11 included/6 excluded/2 relation-only assets; seven source/semantic/metadata/Voronoi/reversible/raster oracles; 0 unresolved |
| T03 | 4 | Totalistic Cellular Automata | 3 | `22-T03-TOTALISTIC-CA.md` | REOPENED | T06 reverse traversal found retained caption BOOK:18770's omitted direct network raster at BOOK:18772; widening the prior 312-candidate/118-asset closure; semantic sum/table/codec result unchanged |
| T04 | 5 | Three-Color Totalistic Cellular Automata | 4 | `23-T04-THREECOLOR-TOTALISTIC.md` | COMPLETE | Exact 12-query/243-candidate partition; 15 evidence groups; 253 cited provenance lines, 92 quote fragments, 90 quote lines; 72 assets at 35 included/32 excluded/5 relation-only; exact `k=3,r=1,A=(0,1,2),nu(i)=i` T03 preset, 2,187-code domain, source trajectories/properties/gallery distinctions, corrected labels, six embedded oracles, Goal 2 handoff, independent review, and 102 tests; 0 unresolved candidates |
| T05 | 6 | Higher-Color Totalistic Cellular Automata | 5 | `24-T05-HIGHERCOLOR-TOTALISTIC.md` | COMPLETE | Exact 11-query/142-lexical-line partition plus five governed follows and 25 assets = 172 candidates; 12 evidence groups at 47 provenance/47 fragments/40 quote lines; assets 5 included/13 relation-only/7 excluded; strict finite `k>=4,r=1` canonical T03 preset, code-1004600/cardinality/bigint/snapshot fixtures, five embedded oracles, independent review, and 102 tests; 0 unresolved candidates |
| T06 | 7 | Quiescent-Background-Preserving Cellular Automata | 6 | `25-T06-QUIESCENT.md` | IN PROGRESS | Exact blank/white-background, invariant-state, rule-predicate, asset, API, and runtime audit active |
| T07 | 8 | Left-Right Symmetric Cellular Automata | 7 | `26-T07-SYMMETRIC.md` | PENDING | Not started |
| T08 | 9 | Initial-Condition Classes | 8 | `27-T08-INITIAL-CONDITIONS.md` | PENDING | Not started |
| T09 | 10 | Mobile Automata | 9 | `3-T09-MOBILE.md` | COMPLETE | 19 direct query terms/families; 14 excerpt groups; 135 combined candidates plus targeted remainders/splits dispositioned; 0 unresolved |
| T10 | 11 | Extended Mobile Automata | 10 | `28-T10-EXTENDED-MOBILE.md` | PENDING | Not started |
| T11 | 12 | Generalized Mobile Automata | 11 | `29-T11-GENERALIZED-MOBILE.md` | PENDING | Not started |
| T12 | 13 | Turing Machines | 12 | `4-T12-TURING.md` | COMPLETE | 278 direct-name lines plus all 74 halt lines/parameter/Notes/Index/split/emulation candidates dispositioned; 16 excerpt groups; 0 unresolved |
| T13 | 14 | Neighbor-Independent Substitution Systems | 13 | `5-T13-PARALLEL-SUBSTITUTION.md` | COMPLETE | 288 direct-name lines plus definition/replacement/alias/Notes/Index/split/rendering/growth/infinite/stochastic/emulation candidates dispositioned; 26 excerpt groups; 0 unresolved |
| T14 | 15 | Neighbor-Dependent Substitution Systems | 14 | `30-T14-CONTEXTUAL-SUBSTITUTION.md` | PENDING | Not started |
| T15 | 16 | Creation-Destruction Substitution Systems | 15 | `31-T15-CREATION-DESTRUCTION.md` | PENDING | Not started |
| T16 | 17 | Sequential Substitution Systems | 16 | `6-T16-SEQUENTIAL-SUBSTITUTION.md` | COMPLETE | 51 direct-name lines plus rule/position order, captions, Notes, aliases/history, Index/splits, stopping, overlap/confluence, finite-input, causal, generalized/multiway, and emulation routes dispositioned; 21 excerpt groups; 0 unresolved |
| T17 | 18 | Tag Systems | 17 | `7-T17-TAG.md` | COMPLETE | 175 direct occurrences on 111 unique lines plus full-prefix/deletion/tail-order, captions/figure, Notes, Index/splits, Post/Wang/cyclic/multiway boundaries, halt/extinction, count, finite-input, and emulation routes dispositioned; 21 excerpt groups; 0 unresolved |
| T18 | 19 | Cyclic Tag Systems | 18 | `32-T18-CYCLIC-TAG.md` | PENDING | Not started |
| T19 | 20 | Register Machines | 19 | `8-T19-REGISTER.md` | COMPLETE | 129 direct occurrences on 94 lines and 135 direct/alias occurrences on 95 lines plus mechanics, figures, Notes/official OCR repairs, Index/splits/history, count/control/end/halting, seeds, observers, variants, and emulations dispositioned; 25 excerpt groups; 0 unresolved |
| T20 | 21 | Symbolic Systems | 20 | `9-T20-SYMBOLIC.md` | COMPLETE | 73 exact-name occurrences on 60 lines; conservative combined direct/alias search 272 occurrences on 166 lines; 24 excerpt groups; all mechanics, figures, Notes/actual Index/splits, patterns/order/overlap, fixed points, seeds, representations, combinator/operator variants, observers, and emulations dispositioned; 0 unresolved |
| T21 | 22 | Two-Dimensional Cellular Automata | 21 | `33-T21-2D-CA.md` | PENDING | Not started |
| T22 | 23 | Moore-Neighborhood Cellular Automata | 22 | `34-T22-MOORE-CA.md` | PENDING | Not started |
| T23 | 24 | Three-Dimensional Cellular Automata | 23 | `35-T23-3D-CA.md` | PENDING | Not started |
| T24 | 25 | Higher-Dimensional Lattice Cellular Automata | 24 | `36-T24-HIGHERDIM-CA.md` | PENDING | Not started |
| T25 | 26 | Two-Dimensional Turing Machines | 25 | `37-T25-2D-TURING.md` | PENDING | Not started |
| T26 | 27 | Two-Dimensional Substitution Systems | 26 | `38-T26-2D-SUBSTITUTION.md` | PENDING | Not started |
| T27 | 28 | Geometric Replacement And Fractal Systems | 27 | `10-T27-GEOMETRIC.md` | COMPLETE | Conservative core regex 46 occurrences/37 lines; expanded alias/observer search 129/88; 18 excerpt groups; all mechanics, original figures, Notes/actual Index/splits, exact and approximate affine rules, overlap/orientation, complex/IFS variants, dimensions, history, limits, observers, and relations dispositioned; 0 unresolved |
| T28 | 29 | Neighbor-Dependent Two-Dimensional Substitution Systems | 28 | `39-T28-CONTEXTUAL-2D-SUBSTITUTION.md` | PENDING | Not started |
| T29 | 30 | Network Systems | 29 | `11-T29-NETWORK.md` | COMPLETE | 44 direct occurrences/40 lines; conservative family audit 290/217; expanded graph/network audit 1,278/654; executable-symbol audit 27/19; 27 excerpt groups; all topology/port/path/reroute/create/projection mechanics, figures, Notes/programs, actual Index/splits, exact rules/counts/periods, identity, observers, variants, and relations dispositioned; 0 unresolved parallel mechanics; 1 explicit sequential primary-source limitation |
| T30 | 31 | Multiway Systems | 30 | `12-T30-MULTIWAY.md` | COMPLETE | Exact phrase 267 occurrences/182 lines; broader token 277/186; expanded alias/confluence 388/224; core implementation symbols 18/16; 25 excerpt groups; all literal branching/overlap/one-splice/exact-merge/dead/epsilon/recurrence mechanics, figures, Notes/programs, actual Index/splits, histories, graphs, confluence, variants, and relations dispositioned; 0 unresolved base mechanics |
| T31 | 32 | Local Constraint Systems | 31 | `13-T31-CONSTRAINTS.md` | COMPLETE | Direct-name union 29 occurrences/27 lines; conservative family 162/134; expanded audit 815/415; 28 excerpt groups; all count-relation/model-set mechanics, page-225/226/227 figures, Notes/Index/splits, periodic/de Bruijn witnesses, verifier/certificate/solver boundary, complexity qualifications, T32/T33 boundaries, variants, observers, and relations dispositioned; 0 unresolved strict mechanics |
| T32 | 33 | Template Constraint Systems | 32 | `40-T32-TEMPLATE-CONSTRAINTS.md` | PENDING | Not started |
| T33 | 34 | Seeded Template Constraint Systems | 33 | `41-T33-SEEDED-CONSTRAINTS.md` | PENDING | Not started |
| T34 | 35 | Arithmetic Iteration Systems | 34 | `14-T34-ARITHMETIC.md` | COMPLETE | Direct-name union 65 occurrences/55 lines; mechanics 27/26; focused native 13/12; code observers 6/6; 30 excerpt groups; all scalar/add/multiply/domain/exactness mechanics, seven main figures and Notes figures, programs/actual Index/splits/history, digit/fraction/size/crop/quotient/CA/substitution/fast-forward relations, T35/T36/T37/T38/T43 boundaries, and exact oracles dispositioned; 0 unresolved |
| T35 | 36 | Piecewise Integer Maps | 35 | `42-T35-PIECEWISE-INTEGER.md` | PENDING | Not started |
| T36 | 37 | Digit-Reversal Arithmetic Systems | 36 | `43-T36-DIGIT-REVERSAL.md` | PENDING | Not started |
| T37 | 38 | Recursive Sequences | 37 | `15-T37-RECURSIVE.md` | COMPLETE | Direct union 48 occurrences/42 lines; fixed-lag tokens 23/13; focused mechanics 32/20; literal programs 20/20; aliases 10/10; named saturation 160/118; 19 excerpt groups; all strict main/raster rows, Notes/actual Index/splits, fixed/nonlinear/modular/global-history variants, source erratum, prefix/seed/checkpoint/read/append/trace/window semantics, programs/history/observers/boundaries, and exact oracles dispositioned; 0 unresolved strict mechanics |
| T38 | 39 | Variable-Index Recursive Sequences | 38 | `44-T38-VARIABLE-RECURRENCE.md` | PENDING | Not started |
| T39 | 40 | Number-Theoretic Filtering Systems | 39 | `16-T39-FILTERS.md` | COMPLETE | Prime search 221 occurrences/134 lines; high-signal union 144/84; exact sieve/Eratosthenes each 6/6 plus complete predicate/measurement/history/Index families; 19 excerpt groups; all strict main, seven rasters/twelve profiles, Notes/actual Index/split, consecutive-stage masks, source repairs, finite/intensional scopes, filter/stream/measurement distinctions, Ulam composition, algorithms/emulations/boundaries, current API/runtime, and exact oracles dispositioned; 0 unresolved source candidates |
| T40 | 41 | Mathematical-Constant Digit Systems | 40 | `45-T40-CONSTANT-DIGITS.md` | PENDING | Not started |
| T41 | 42 | Function-Combination Systems | 41 | `17-T41-FUNCTIONS.md` | COMPLETE | Direct-name union 59 occurrences/51 lines; formula-literal union 176/83; crossing/rule union 19/9; 18 excerpt groups; all strict main, four strict/eight Notes rasters, native Notes/actual Index/splits, named functions/series/zeros/branches/evaluation, ODE/source repairs, page-162 T42 seam, current API/runtime, and exact/declared-precision oracles dispositioned; 0 unresolved candidates |
| T42 | 43 | Continued-Fraction-Driven Substitution Systems | 42 | `46-T42-CF-SUBSTITUTION.md` | PENDING | Not started |
| T43 | 44 | Iterated Maps | 43 | `18-T43-ITERATED-MAPS.md` | COMPLETE | Direct map/mapping 106 occurrences/89 lines; controlled iteration union 214/155; high-signal map/chaos/precision/analysis union 332/210; 19 excerpt groups; all strict main, eight strict/three Notes assets, native Notes/actual Index/splits, exact/realized/tracked state, closed map/invariance/update/trace/analyzer semantics, precision profiles, source repairs, T34/T41/T44 boundaries, current API/runtime, exact-rational page-165 and declared-180-decimal page-168/page-170 cell oracles dispositioned; 0 unresolved candidates |
| T44 | 45 | Continuous Cellular Automata | 44 | `19-T44-CONTINUOUS-CA.md` | COMPLETE | Literal 21-query oracle; 25 evidence groups; all strict/Notes/actual-Index/split/history/alias/program/profile/application/noise/complex/PDE candidates; total `[0,1]` fixed-lattice field, closed affine aggregate plus scalar map, T01 parallel assignment reuse, exact/certified/tracked/represented distinctions, support/work/crop split, 17 included assets plus page-339 exclusion, semantic and raster oracles, D096-D102 boundaries, current API/runtime, and Goal 2 handoff dispositioned; 0 unresolved candidates |
| T45 | 46 | Partial Differential Equation Systems | 45 | `20-T45-PDE.md` | COMPLETE | Exact 27-query manifest oracle; 28 evidence groups; all strict/Notes/actual-Index/split/equation/condition/method/solution/continuum/history/application candidates; declarative real/complex/fixed-vector differential problems and Classical solution sets; closed multivariate/candidate/trace syntax; explicit class/locus/admissibility claims; proof-strength queries; numerical/scope/observer separation; 23 included assets plus Chapter 5 exclusion; semantic, metadata, and heat raster oracles; D103-D110 boundaries; 0 unresolved candidates |

## Coverage Summary

- Foundation: complete in `1-FOUNDATION.md`.
- Type stages complete: 22 / 45.
- Type stages reopened: 1.
- Type stages unresolved: 21 pending, 1 in progress.
- Synthesis: pending.
- Goal 2 handoff: pending.

## Reopened-Stage Log

- T03 reopened and reclosed during T05: named code-`1004600` had been included as a four-color totalistic profile, but its Notes continuation at canonical line 19234 and linked lines 19236/19238 were absent from the claimed 309-candidate/116-asset closure. The repaired 18-query/312-candidate and 118-asset manifest, all six checks, fresh independent review, and 102 tests pass; the semantic result remains unchanged.
- T03 reopened again during T06: the stage retained the quiescent-symmetric elementary emulation caption at `BOOK:18770` but omitted its explicit network raster link at `BOOK:18772`. The bounded source/asset/reverse-join repair and independent re-review are active; no semantic conclusion has changed.
