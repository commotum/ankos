# Goal 4: Whole-Book ANKoS Construction Taxonomy Audit

Shorthand: `BOOK-TAXONOMY`

## Big-Picture Objective

Audit the complete local *A New Kind of Science* corpus independently of the existing T01–T45 catalog and determine every book-grounded construction, generator, relation, constraint, input-processing mechanism, or other finitely described formal system that deserves traceable coverage.

The audit must answer two different questions:

1. What named constructions, presets, restrictions, seed/input classes, declarative systems, and materially distinct variants does the Book require the project to cover?
2. What is the smaller set of genuinely distinct semantic families after aliases, presets, properties, representations, observers, applications, and lossless parameterizations are separated?

Success is not a preferred count. Success is an evidence-complete census in which every part of the Book has been screened, every candidate has a source-grounded semantic fingerprint and orthogonal catalog/role/family classifications, every relevant cross-reference and image has been accounted for, the existing 45 entries are independently rediscovered or diagnosed, and every proposed addition or close exclusion survives hostile review.

Goal 4 is a research, taxonomy, and architecture-pressure audit. It does not implement runtime changes, rewrite Goal 1, renumber T01–T45, or modify the Book sources or current catalog unless the user later authorizes a separate integration step.

## Governing Questions

1. Is the current 45-row catalog exhaustive for the whole Book, rather than merely exhaustive for its original Chapters 3–5 seed scope?
2. Which unlisted passages specify genuinely new constructions, and which are variants, compositions, properties, seed classes, observers, applications, or emulations of existing constructions?
3. Which Book names deserve distinct catalog coverage even when they share one semantic implementation family?
4. Which apparently similar systems differ in state, history, update schedule, probability semantics, structural mutation, branching, completion, or witness requirements?
5. Do any newly discovered constructions invalidate the current proposed SimpleProgram API or require a principled clarification?
6. What exact changes should a later authorized integration make to `ref/notes/CA-Types.csv`, Goal 1, Goal 2, and API planning?

## Non-Negotiable Constraints

1. **Book-first discovery.** Do not use T01–T45, `CA-Types.md`, Goal 1 stage conclusions, the proposed API, or runtime capabilities to decide what exists in the Book during the blind discovery phase.
2. **Artifact-level independence, not a false claim of amnesia.** Prior context is known, but blind discovery artifacts use provisional `B####` candidate IDs and contain no T-ID mappings or API-fit decisions until Stage 19.
3. **Sequential coverage precedes search saturation.** Keyword searches, headings, and Index terms can find omissions but cannot substitute for reading every source unit in order.
4. **The ordered 29-document corpus is canonical.** Start from `ref/A-New-Kind-of-Science/Contents.md`, follow its document order, and use those linked Markdown files for completeness and provenance.
5. **Main text and Notes are paired.** Review each chapter document together with its corresponding Notes document.
6. **Figures count as evidence.** Visually screen every image at least once, using contact sheets or thumbnails where appropriate. Inspect construction-bearing, text-bearing, ambiguous, or caption-incomplete figures at original resolution with their surrounding context; do not infer exact rules from pixels when the source does not establish them.
7. **No count target.** Do not protect 45, inflate the number of additions, or collapse candidates merely to preserve an elegant API.
8. **Coverage catalog and semantic families remain separate.** A named preset can deserve a catalog row without a new executor. Conversely, two systems can fit the same five fields while remaining semantically distinct.
9. **Names do not establish identity.** Different names may be aliases or presets; the same name may cover several constructions.
10. **API fit does not establish taxonomy.** Do not decide that two systems are one type merely because both fit `seed/alphabet/frontier/neighborhood/rule`.
11. **Equivalence requires a real proof.** Claims of same-family reuse require
    maps on valid program/specification data and configurations/inputs, an
    inverse on the valid image, and preservation of one native semantic
    judgment—including schedule, branching/probability, completion, and
    witnesses—without a hidden source interpreter. The preservation law must
    match the object kind: transition, stochastic kernel, successor relation,
    satisfaction/model relation, partial function, or denotation/flow.
12. **New-family claims require a counterexample.** Show a concrete native event or denotation that the nearest existing family cannot preserve honestly. Opaque packing, callbacks, phase hidden in an executor, or multi-step simulation are not evidence of reuse.
13. **Do not conflate semantic roles.** Keep construction, property/restriction, seed/input/boundary class, representation, observer/analyzer, solver, application, emulation, and historical mention distinct.
14. **Randomness distinctions are explicit.** Separate random initial data, a stochastic transition law, an external draw stream, a finite PRNG realization, and a downstream distribution.
15. **Declarative objects are not fake trajectories.** A constraint, function, constant, equation, or model set may be in scope without a native update.
16. **Insufficient source evidence is a resolved boundary, not permission to invent.** Record the exact missing mechanics and classify the candidate as `INSUFFICIENT_BOOK_EVIDENCE` after exhaustive review.
17. **External sources are auxiliary only.** They may clarify terminology or document a source defect, but they cannot create Book coverage or silently fill absent Book semantics.
18. **Preserve the canonical source.** Do not edit the Book corpus during the taxonomy audit. Record any apparent textual, visual, or semantic ambiguity as an audit finding rather than silently changing source material.
19. **Scope writes to Goal 4.** During execution, preserve current dirty work and write audit artifacts only under `goal-4/` unless the user explicitly authorizes integration elsewhere.
20. **No stage completes on green tooling alone.** Validators prove ledger integrity; they do not prove that a human or agent read and correctly understood the source.

## Definitions

### Source Unit

A deterministic, hash-bound unit of one canonical book document: heading, paragraph, list item, code/formula block, caption, table-like block, image reference, or other indivisible review unit. Source units must partition the ordered 29-document corpus without silent gaps or overlaps.

### Candidate

A source-grounded possibility that the Book specifies a construction or a catalog-worthy semantic role. Candidates use stable provisional IDs `B0001`, `B0002`, and so on until final reconciliation.

### Semantic Fingerprint

Every candidate records:

- object kind and native notion of time, if any;
- carrier, support, topology, and structural invariants;
- alphabet or value schema;
- complete state, visible history, and control;
- seed, input, boundary, and external data;
- frontier, activation, or schedule;
- readable dependencies or neighborhood;
- rule, relation, constraint, function, or probability law;
- writes, replacement, assembly, or commit semantics;
- successor cardinality, determinism, branching, or stochastic measure;
- termination, completion, failure, and witness semantics;
- parameters and variants;
- observers and representations kept outside native identity;
- evidence strength and any missing mechanics.

### Coverage Catalog

The traceable inventory of Book constructions and separately named coverage obligations. It may include presets, restrictions, seed classes, or declarative categories that do not require distinct execution machinery.

### Semantic Family

A group whose native/declarative members either have an explicit lossless
structural/relational correspondence preserving program data and complete
native judgments, or are proved instances/restrictions of the same substantive
typed parameterized semantic schema with unchanged mechanics. Similar behavior,
a shared renderer, emulation, an auditor-invented universal schema, or a common
top-level API shape is insufficient. Properties, seeds, representations,
observers, applications, emulations, solvers, aliases, and compositions use
typed relations to affected families rather than being forced into false
membership.

### Orthogonal Final Classification

Every candidate must receive three independent final fields so catalog coverage is never confused with semantic-family novelty.

`catalog_action` has exactly one value:

- `EXISTING_ENTRY_SUFFICIENT`
- `EXISTING_ENTRY_NEEDS_CORRECTION`
- `ADD_CATALOG_ENTRY`
- `NO_SEPARATE_CATALOG_ENTRY`
- `INSUFFICIENT_BOOK_EVIDENCE`

`semantic_role` has exactly one primary value, with optional secondary tags:

- `NATIVE_TRANSITION_OR_GENERATOR`
- `STOCHASTIC_OR_BRANCHING_PROCESS`
- `INPUT_PROCESSOR_OR_TRANSDUCER`
- `RELATION_CONSTRAINT_OR_MODEL_SET`
- `IMMUTABLE_DEFINITION_OR_QUERY`
- `SPECIALIZATION_OR_PRESET`
- `PROPERTY_OR_RESTRICTION`
- `SEED_INPUT_OR_BOUNDARY_CLASS`
- `COMPOSITION_OR_HYBRID`
- `REPRESENTATION_CODEC_OR_OBSERVER`
- `APPLICATION_OR_EMULATION`
- `SOLVER_OR_NUMERICAL_METHOD`
- `DUPLICATE_OR_ALIAS`
- `SOURCE_INSUFFICIENT_ROLE`

`family_action` has exactly one value:

- `EXISTING_SEMANTIC_FAMILY`
- `NEW_SEMANTIC_FAMILY`
- `SOURCE_INSUFFICIENT_FOR_FAMILY`

A candidate may therefore justify a new catalog entry while remaining a preset, property, seed class, composition, declarative object, or other member of an existing semantic family. A new-family counterexample is required only for `NEW_SEMANTIC_FAMILY`, never merely because `catalog_action=ADD_CATALOG_ENTRY`.

## Authoritative Inputs

- User directions and `principles.md`.
- [The pre-audit baseline](0-baseline.md), used only to detect input drift and
  reverified independently during Stages 1–2.
- [Canonical source overview](../ref/A-New-Kind-of-Science/README.md).
- [Ordered contents](../ref/A-New-Kind-of-Science/Contents.md), linking all 29 canonical book documents.
- The 1,607 colocated Book images referenced by those documents.
- [The canonical Index](../ref/A-New-Kind-of-Science/BACK-MATTER/Index.md): alias and cross-reference discovery, not construction proof by itself.
- `ref/notes/CA-Types.csv`, `ref/notes/CA-Types.md`, Goal 1, Goal 2, `api.md`, `simple_programs.md`, and `src/ca`: withheld during blind discovery and opened only for reconciliation and architecture-pressure analysis.

## Current Facts

These are current cutover facts to reverify and hash-pin in Stage 2:

- The taxonomy scaffold was re-indexed from Goal 3 to Goal 4 before execution;
  no taxonomy-audit stage or generated audit artifact had begun.
- Stage 1 is complete in `1-GUARDRAILS.md`. The frozen machine-readable
  discovery contract is `guardrails.json`; it adds orthogonal source/evidence
  status, object-kind native-judgment proofs, an explicit solver role, typed
  family relations, allowlist-only blind schemas, and sealed-worker isolation.
- `CA-Types.md` explicitly says its source scope is Chapters 3–5. Goal 1 makes the 45-row CSV exhaustive relative to that seed catalog, not relative to an independent whole-book discovery pass.
- The current catalog has stable identifiers T01–T45, and Goal 1 reports all 45 type stages plus synthesis and the implementation handoff complete.
- The canonical source tree contains exactly 29 ordered book documents, plus `README.md` and `Contents.md`.
- The 29 documents cover publication information and printed contents, Preface, Chapters 1–12, General Notes, Notes for Chapters 1–12, Index, and Colophon.
- The canonical source tree contains 1,607 JPEGs colocated with their owning document groups.
- The source documents and their image references were validated before canonical cutover; Stage 2 must independently reverify counts, hashes, ordering, and link resolution rather than inherit that verdict.
- Stage 2 is complete in `2-CORPUS-MAP.md`. Independent parsing found 38,168
  physical Markdown lines partitioned into 14,311 deterministic source units.
  The inherited 22,498-line table used a different historical concatenation
  convention and is replaced below.
- The EPUB briefly inspected in the repository was deleted and is not an audit source.
- Existing Goal 1 stages already record some systems as siblings, future work, unsupported execution, or separate constructions. Those records are valuable only after blind discovery is frozen.
- Preliminary examples such as sequential/asynchronous cellular automata, second-order cellular automata, block cellular automata, probabilistic cellular automata and substitutions, random walks, aggregation processes, input-consuming finite automata, probabilistic generators, evolving rules, and later network constructions are hypotheses to investigate—not accepted additions.

## Canonical Corpus Map

Stage 2 independently derived this map from the canonical files:

| Material | Canonical path | Physical/logical lines |
|---|---|---:|
| Publication and printed contents | `FRONT-MATTER/00-Publication-and-Contents.md` | 1–94 |
| Preface | `FRONT-MATTER/01-Preface.md` | 95–167 |
| Chapter 1 | `CHAPTERS/01-The-Foundations-for-a-New-Kind-of-Science.md` | 168–375 |
| Chapter 2 | `CHAPTERS/02-The-Crucial-Experiment.md` | 376–639 |
| Chapter 3 | `CHAPTERS/03-The-World-of-Simple-Programs.md` | 640–1309 |
| Chapter 4 | `CHAPTERS/04-Systems-Based-on-Numbers.md` | 1310–2045 |
| Chapter 5 | `CHAPTERS/05-Two-Dimensions-and-Beyond.md` | 2046–2601 |
| Chapter 6 | `CHAPTERS/06-Starting-from-Randomness.md` | 2602–3311 |
| Chapter 7 | `CHAPTERS/07-Mechanisms-in-Programs-and-Nature.md` | 3312–4183 |
| Chapter 8 | `CHAPTERS/08-Implications-for-Everyday-Systems.md` | 4184–4953 |
| Chapter 9 | `CHAPTERS/09-Fundamental-Physics.md` | 4954–6327 |
| Chapter 10 | `CHAPTERS/10-Processes-of-Perception-and-Analysis.md` | 6328–7341 |
| Chapter 11 | `CHAPTERS/11-The-Notion-of-Computation.md` | 7342–8215 |
| Chapter 12 | `CHAPTERS/12-The-Principle-of-Computational-Equivalence.md` | 8216–9901 |
| General Notes | `BACK-MATTER/NOTES/00-General-Notes.md` | 9902–10092 |
| Chapter 1 Notes | `BACK-MATTER/NOTES/01-The-Foundations-for-a-New-Kind-of-Science-Notes.md` | 10093–10167 |
| Chapter 2 Notes | `BACK-MATTER/NOTES/02-The-Crucial-Experiment-Notes.md` | 10168–11082 |
| Chapter 3 Notes | `BACK-MATTER/NOTES/03-The-World-of-Simple-Programs-Notes.md` | 11083–11949 |
| Chapter 4 Notes | `BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes.md` | 11950–12989 |
| Chapter 5 Notes | `BACK-MATTER/NOTES/05-Two-Dimensions-and-Beyond-Notes.md` | 12990–13746 |
| Chapter 6 Notes | `BACK-MATTER/NOTES/06-Starting-from-Randomness-Notes.md` | 13747–14412 |
| Chapter 7 Notes | `BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes.md` | 14413–15104 |
| Chapter 8 Notes | `BACK-MATTER/NOTES/08-Implications-for-Everyday-Systems-Notes.md` | 15105–15462 |
| Chapter 9 Notes | `BACK-MATTER/NOTES/09-Fundamental-Physics-Notes.md` | 15463–16462 |
| Chapter 10 Notes | `BACK-MATTER/NOTES/10-Processes-of-Perception-and-Analysis-Notes.md` | 16463–17560 |
| Chapter 11 Notes | `BACK-MATTER/NOTES/11-The-Notion-of-Computation-Notes.md` | 17561–18546 |
| Chapter 12 Notes | `BACK-MATTER/NOTES/12-The-Principle-of-Computational-Equivalence-Notes.md` | 18547–20389 |
| Index | `BACK-MATTER/Index.md` | 20390–38129 |
| Colophon | `BACK-MATTER/Colophon.md` | 38130–38168 |

## Assumptions To Challenge

- The current 45 entries are all independently recoverable from a blind Book pass.
- The Book provides enough mechanics to settle every candidate rather than only name it.
- Every important construction appears in prose or headings rather than only in captions, code, formulas, or images.
- Chapter boundaries and Book terminology align with semantic-family boundaries.
- Applications in Chapters 7–10 only reuse earlier mechanics rather than defining new coupled or stochastic constructions.
- Reversibility, conservation, symmetry, universality, and behavior classes are always properties rather than sometimes being enforced by a different construction.
- A schedule can always be treated as ordinary visible state without changing the construction's semantic family.
- Probability-bearing rules, structural mutation, multi-time state, and input streams fit existing families without semantic loss.
- The final five-field API can express every new candidate without hidden state, a separate update policy, or a vacuous callback.
- One catalog row should correspond to one semantic family.

## Required Goal 4 Artifacts

Execution of the stages will create, refine, and verify:

- `goal-4/corpus-manifest.json`: hashes, file/asset counts, canonical segments, split anomalies, and chapter↔Notes pairings.
- `goal-4/source-units.jsonl`: deterministic canonical source units with stable IDs and hashes.
- `goal-4/reading-ledger.csv`: one review disposition and candidate/support links for every source unit.
- `goal-4/candidate-ledger.jsonl`: stable B IDs, provenance, aliases, evidence strength, semantic fingerprints, and uncertainty.
- `goal-4/search-rounds.json`: reproducible query rounds, result digests, match dispositions, and fixed-point evidence.
- `goal-4/cross-reference-ledger.csv`: relevant page/section/Notes/Index routes and their reviewed targets.
- `goal-4/asset-ledger.csv`: image references, physical paths/hashes, source ownership, evidence role, inspection status, and uncertainty.
- `goal-4/classification-ledger.csv`: orthogonal `catalog_action`, `semantic_role`, and `family_action` fields plus proof for every candidate.
- `goal-4/coverage-matrix.csv`: B candidates, existing T01–T45 obligations, proposed additions, and source coverage joins.
- `goal-4/near-pair-matrix.md`: explicit comparisons among easily conflated candidates.
- `goal-4/whole-book-catalog.md`: the final traceable coverage catalog.
- `goal-4/semantic-families.md`: the deduplicated semantic-family inventory and equivalence/non-equivalence arguments.
- `goal-4/hostile-review.md`: independent findings and reclosure records.
- `goal-4/taxonomy-report.md`: final answer, counts, evidence limits, corrections, and integration consequences.
- `goal-4/integration-handoff.md`: proposed T46+ additions and Goal 1/2/API work, without performing those changes.
- Small validators/oracles under `goal-4/tools/` that fail closed when coverage, joins, hashes, or dispositions are incomplete.

## Success Metrics

- All 29 canonical book documents, both navigation documents, and all 1,607 physical images are present in the source manifest or explicitly diagnosed.
- Every canonical logical line belongs to exactly one segment and every deterministic source unit has exactly one reading-ledger disposition.
- Preface/bookends, 12/12 main chapters, General Notes, 12/12 chapter Notes documents, canonical Index, and Colophon are screened.
- Every image reference has an asset-ledger row and every physical image is visually screened at least once; construction-bearing, text-bearing, ambiguous, and caption-incomplete images receive original-resolution review with surrounding context.
- Every relevant cross-reference reaches a reviewed target or a documented missing target.
- Sequential discovery and recursive search reach a declared fixed point with no undispositioned search hit.
- Every candidate has complete provenance, a semantic fingerprint, and exactly one value for each final classification axis.
- Every T01–T45 entry is independently rediscovered or receives a source-backed diagnostic.
- Every proposed new catalog entry and every close collapse/exclusion receives independent hostile review.
- The final coverage-catalog count and semantic-family count are both reported and never conflated.
- Zero source units, candidates, search hits, cross-references, and required assets remain silently unresolved.
- Genuine `INSUFFICIENT_BOOK_EVIDENCE` dispositions identify the exact missing mechanics and the evidence boundary.
- Input hashes and all audit ledgers are reproducible; mutation tests prove the validators detect missing units, links, classifications, and source changes.

## Verification Requirements

- Independently parse all 29 ordered documents and compare them with the manifest and source-unit ledger; do not derive expected coverage from the same ledger being tested.
- Prove segment and source-unit union equals the canonical corpus with no gaps or overlaps.
- Verify every source reference, document link, image path, and hash resolves or has an explicit finding.
- Verify candidate IDs, source-unit links, cross-reference targets, search dispositions, classification rows, and coverage-matrix joins are total and unique.
- Verify blind artifacts were frozen before T reconciliation and contain no T-ID mapping or API-fit fields.
- Re-run all search rounds and compare query/result digests.
- Mutation-test deletion or corruption of a source unit, candidate link, search disposition, cross-reference, asset row, and classification; each mutation must fail verification.
- Run validators from the repository root and a relocated copy, byte-compile/import silently where applicable, fail closed under optimized Python if assertions are used, and avoid working-directory assumptions.
- Run direct trailing-whitespace, Markdown-fence, path, and schema checks over tracked and untracked `goal-4/**`; when files are intentionally staged, also run `git diff --cached --check -- goal-4`. Inspect scope with `git status --short`.
- Confirm Goal 4 did not edit Book sources, `ref/notes`, Goal 1, Goal 2, runtime, tests, or root API documents without explicit authorization.

## Stages

### 1-GUARDRAILS

Status: **COMPLETE** in `goal-4/1-GUARDRAILS.md`.

#### Big Picture Objective

Fix the audit's inclusion threshold, evidence model, candidate identity, disposition vocabulary, semantic-equivalence standard, blind-discovery boundary, and success/failure criteria before inspecting the Book for additions.

#### Detailed Implementation Plan

- Read `principles.md`, `0-baseline.md`, and this scaffold in full.
- Define construction-bearing eligibility broadly enough to include transitions, generators, input processors, stochastic laws, relations, constraints, functions/constants/equations, and structural replacement systems.
- Define exclusion and secondary-role categories without pre-classifying known examples.
- Freeze provisional B-ID allocation, source-evidence strength, semantic-fingerprint fields, and the three final classification vocabularies.
- Specify how isolated discovery workers receive only assigned Book ranges, Goal 4 guardrails, and ledger schemas.
- Define the proof obligations for same-family, specialization, composition, new construction, and insufficient evidence.

#### Completion Requirements

- Eligibility and all disposition categories have necessary and sufficient operational criteria.
- The distinction between coverage catalog and semantic family is explicit and testable.
- Blind-phase allowed/forbidden inputs are recorded.
- No current candidate is accepted, rejected, or mapped to T01–T45.
- The stage records commands, facts, and any changes folded back into this plan.

### 2-CORPUS-MAP

Status: **COMPLETE** in `goal-4/2-CORPUS-MAP.md`.

#### Big Picture Objective

Create a trustworthy, hash-pinned map of the complete canonical Book corpus.

#### Detailed Implementation Plan

- Inventory and hash all canonical Markdown and image files.
- Verify that `Contents.md` names exactly the 29 book documents in canonical order.
- Partition each document into deterministic source units and bind every unit to its document, byte range, logical-line range, and hash.
- Resolve every document and image link from its owning Markdown file.
- Reconcile the physical image inventory with all Markdown references without rewriting source files.

#### Completion Requirements

- `corpus-manifest.json` accounts for all 29 book documents, the two navigation documents, and all 1,607 physical images.
- Canonical source units cover every book-document byte and logical line exactly once.
- Every image reference resolves to its intended colocated file and hash or has an explicit finding.
- Document order and ownership mappings are machine-verifiable.
- Independent source-manifest verification and mutation checks pass.

### 3-AUDIT-HARNESS

#### Big Picture Objective

Build the ledgers and validators that make sequential reading, candidate capture, cross-reference closure, asset inspection, and final classification auditable.

#### Detailed Implementation Plan

- Deterministically extract source units with stable IDs and hashes.
- Create schemas for the reading, candidate, search-round, cross-reference, asset, classification, and coverage ledgers.
- Implement validators for total unit coverage, unique IDs, resolvable provenance, complete joins, empty work queues, and stale source hashes.
- Add mutation fixtures proving each required row/link is enforced.
- Keep discovery schemas free of T mappings and API-fit fields until Stage 19.

#### Completion Requirements

- Validators detect missing/duplicate source units, broken provenance, unresolved cross-references, undispositioned hits/candidates, missing assets, and stale hashes.
- The source-unit ledger partitions the canonical corpus without gaps or overlaps.
- The harness runs from root and a relocated copy and fails closed under declared modes.
- Stage 4 can begin with empty, valid, resumable ledgers.

### 4-BOOKENDS

#### Big Picture Objective

Blindly screen cover/contents, Preface, General Notes, and Colophon for construction-bearing material and establish the sequential review discipline before chapter work.

#### Detailed Implementation Plan

- Read every assigned source unit in order with no current-catalog reconciliation.
- Inspect each owned image and surrounding caption/context.
- Create B candidates with complete provisional fingerprints whenever mechanics may be present.
- Record supports, controls, applications, historical-only material, and no-construction units explicitly.
- Queue every relevant page/section/alias route that points outside the assigned spans.

#### Completion Requirements

- All assigned source units and images have review dispositions.
- Every candidate and support claim has canonical provenance.
- No within-stage cross-reference remains unreviewed; routed edges are in the global queue.
- The stage contains no T-ID mapping or API-fit conclusion.

### 5-CH01-FOUNDATIONS

#### Big Picture Objective

Blindly audit Chapter 1 main text and Chapter 1 Notes for construction-bearing systems.

#### Detailed Implementation Plan

- Sequentially review `CHAPTERS/01-The-Foundations-for-a-New-Kind-of-Science.md` and `BACK-MATTER/NOTES/01-The-Foundations-for-a-New-Kind-of-Science-Notes.md`.
- Inspect all owned captions, code/formulas, tables, and images in their canonical document context.
- Record B candidates and full provisional semantic fingerprints.
- Run a range-local trigger/alias search only after sequential reading.
- Queue cross-range references without consulting the existing catalog.

#### Completion Requirements

- Every source unit/image in the paired spans is dispositioned.
- Every local trigger hit is reconciled to a reviewed unit.
- Candidate provenance and fingerprints are complete to the limit of the source.
- No blind-phase boundary is violated.

### 6-CH02-EXPERIMENT

#### Big Picture Objective

Blindly audit Chapter 2 main text and Chapter 2 Notes.

#### Detailed Implementation Plan

- Sequentially review `CHAPTERS/02-The-Crucial-Experiment.md` and `BACK-MATTER/NOTES/02-The-Crucial-Experiment-Notes.md`.
- Apply the same source-unit, image, candidate, local-search, and cross-reference protocol established in Stage 5.
- Treat rules, initial conditions, behavior classes, properties, renderings, and historical commentary as distinct roles.

#### Completion Requirements

- The paired ranges have zero unreviewed units/images and zero undispositioned local search hits.
- Every construction candidate has a source-grounded fingerprint.
- Properties and observed behavior are not silently promoted to constructions.
- Cross-range routes are recorded for later closure.

### 7-CH03-PROGRAMS

#### Big Picture Objective

Blindly audit Chapter 3 main text and Chapter 3 Notes without using the catalog originally derived from this chapter.

#### Detailed Implementation Plan

- Sequentially review `CHAPTERS/03-The-World-of-Simple-Programs.md` and `BACK-MATTER/NOTES/03-The-World-of-Simple-Programs-Notes.md`.
- Inspect implementation code, rule tables, figure-only mechanics, variants, histories, and cross-system comparisons.
- Allocate B candidates independently of T IDs or familiar names.
- Preserve distinctions among native construction, restriction, representation, emulation, observer, and behavior.

#### Completion Requirements

- Every unit/image in both spans has a disposition.
- Every rule/mechanism passage and local search hit is linked to candidates or an explicit exclusion.
- No current taxonomy row or Goal 1 conclusion is used as discovery evidence.
- All outgoing cross-references are queued.

### 8-CH04-NUMBERS

#### Big Picture Objective

Blindly audit Chapter 4 main text and Chapter 4 Notes.

#### Detailed Implementation Plan

- Sequentially review `CHAPTERS/04-Systems-Based-on-Numbers.md` and `BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes.md`.
- Separate immutable definitions, representation queries, iterative work procedures, sequences, filters, maps, continuous systems, equations, observations, and numerical methods.
- Inspect every formula, implementation fragment, caption, and governed image.
- Record exactness, partiality, completion, and hidden-work-state requirements in candidate fingerprints.

#### Completion Requirements

- All paired source units/images and local search hits are dispositioned.
- Denotations, algorithms, trajectories, queries, and observers are not conflated.
- Every candidate has explicit result kind and evidence strength.
- Cross-range references are queued with no silent omissions.

### 9-CH05-DIMENSIONS

#### Big Picture Objective

Blindly audit Chapter 5 main text and Chapter 5 Notes.

#### Detailed Implementation Plan

- Sequentially review `CHAPTERS/05-Two-Dimensions-and-Beyond.md` and `BACK-MATTER/NOTES/05-Two-Dimensions-and-Beyond-Notes.md`.
- Record topology, dimensionality, structural replacement, graph identity, branching, constraints, schedules, and witness semantics explicitly.
- Inspect rule diagrams and construction-bearing images in full context.
- Preserve underdetermined variants rather than choosing convenient conventions.

#### Completion Requirements

- Every unit/image and local search hit in the paired spans is dispositioned.
- Structural variants have complete fingerprints or explicit missing-mechanics fields.
- Constraints, solvers, networks, multiway histories, and renderings remain distinct.
- All relevant outgoing references are queued.

### 10-CH06-RANDOMNESS

#### Big Picture Objective

Blindly audit Chapter 6 main text and Chapter 6 Notes.

#### Detailed Implementation Plan

- Sequentially review `CHAPTERS/06-Starting-from-Randomness.md` and `BACK-MATTER/NOTES/06-Starting-from-Randomness-Notes.md`.
- Distinguish behavior classes, ensembles, random seeds, attractors, perturbations, finite-size protocols, and any native construction changes.
- Record probability laws only where the Book specifies them.
- Inspect all captions/images and run local saturation after reading.

#### Completion Requirements

- All paired units/images and trigger hits are dispositioned.
- Initial-condition randomness is not confused with stochastic transition semantics.
- Behavior/property/analyzer records are separated from construction candidates.
- Cross-range references are completely queued.

### 11-CH07-MECHANISMS

#### Big Picture Objective

Blindly audit Chapter 7 main text and Chapter 7 Notes.

#### Detailed Implementation Plan

- Sequentially review `CHAPTERS/07-Mechanisms-in-Programs-and-Nature.md` and `BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes.md`.
- Pay explicit attention to stochastic movement, aggregation, constraint satisfaction, continuity/discreteness mechanisms, and systems introduced as explanatory examples.
- Record event selection, probability, frontier growth, and ensemble/observer distinctions.
- Inspect every construction-bearing figure and follow local references.

#### Completion Requirements

- All paired source units/images and search hits are dispositioned.
- Stochastic laws, random inputs, averaged observations, and deterministic intrinsic randomness are distinguished.
- Candidate fingerprints include draw/event timing and measure semantics where evidenced.
- No relevant reference is lost.

### 12-CH08-EVERYDAY

#### Big Picture Objective

Blindly audit Chapter 8 main text and Chapter 8 Notes.

#### Detailed Implementation Plan

- Sequentially review `CHAPTERS/08-Implications-for-Everyday-Systems.md` and `BACK-MATTER/NOTES/08-Implications-for-Everyday-Systems-Notes.md`.
- Determine whether each application merely instantiates earlier mechanics or specifies new coupling, mutation, global selection, growth, stochastic, or hybrid semantics.
- Keep physical interpretation and display conventions outside native construction identity unless the Book makes them causal.
- Inspect all figures and implementation details.

#### Completion Requirements

- Every paired unit/image and local trigger hit is dispositioned.
- Each application candidate states whether new mechanics are actually specified.
- Hybrid/composed systems identify component boundaries and coupling laws.
- All cross-range routes are queued.

### 13-CH09-PHYSICS

#### Big Picture Objective

Blindly audit Chapter 9 main text and Chapter 9 Notes.

#### Detailed Implementation Plan

- Sequentially review `CHAPTERS/09-Fundamental-Physics.md` and `BACK-MATTER/NOTES/09-Fundamental-Physics-Notes.md`.
- Record multi-time state, reversibility constructions, block schedules, conserved systems, network rewrites, causal event structures, branching, and sequencing evidence without forcing them into prior categories.
- Distinguish derived causal representations from native evolution and distinguish property restrictions from construction-enforced mechanics.
- Inspect all relevant rule diagrams, network figures, and formulas.

#### Completion Requirements

- Every paired unit/image and local search hit is dispositioned.
- Schedule, visible history, structural mutation, and causal witness semantics are explicit.
- Close property-versus-construction cases retain evidence on both sides.
- Outgoing references are fully queued.

### 14-CH10-PERCEPTION

#### Big Picture Objective

Blindly audit Chapter 10 main text and Chapter 10 Notes.

#### Detailed Implementation Plan

- Sequentially review `CHAPTERS/10-Processes-of-Perception-and-Analysis.md` and `BACK-MATTER/NOTES/10-Processes-of-Perception-and-Analysis-Notes.md`.
- Separate analyzers and compression/view procedures from generative probabilistic models, transducers, automata, and stochastic cellular systems.
- Record consumed input, hidden state, output semantics, likelihood/probability roles, and learning/fitting procedures where specified.
- Inspect code, formulas, captions, and all governed images.

#### Completion Requirements

- All paired units/images and search hits are dispositioned.
- Model definitions, inference algorithms, observers, and data transformations are not conflated.
- Input-processing candidates have complete input/state/output fingerprints.
- Every relevant reference is queued.

### 15-CH11-COMPUTATION

#### Big Picture Objective

Blindly audit Chapter 11 main text and Chapter 11 Notes.

#### Detailed Implementation Plan

- Sequentially review `CHAPTERS/11-The-Notion-of-Computation.md` and `BACK-MATTER/NOTES/11-The-Notion-of-Computation-Notes.md`.
- Distinguish native constructions from emulations, universal presets, encodings, proof artifacts, and computational properties.
- Record any construction mechanics introduced only to establish universality.
- Inspect all diagrams, encodings, implementation passages, and cross-references.

#### Completion Requirements

- Every paired unit/image and local trigger hit is dispositioned.
- Emulation and universality do not create false native types.
- Any genuinely specified machine/system has a complete provisional fingerprint.
- Cross-range routes are fully queued.

### 16-CH12-EQUIVALENCE

#### Big Picture Objective

Blindly audit Chapter 12 main text and Chapter 12 Notes.

#### Detailed Implementation Plan

- Sequentially review `CHAPTERS/12-The-Principle-of-Computational-Equivalence.md` and `BACK-MATTER/NOTES/12-The-Principle-of-Computational-Equivalence-Notes.md`.
- Separate philosophical claims, mathematical examples, axiom systems, proof/search relations, computations, and actual formal constructions.
- Record any explicitly instantiated rewrite, proof, equation, machine, or generative mechanism.
- Inspect all images and follow every locally resolvable route.

#### Completion Requirements

- Every paired unit/image and local search hit is dispositioned.
- Abstract discussion is not mistaken for executable mechanics, and declarative formal systems are not discarded merely for lacking time evolution.
- Candidate evidence boundaries are explicit.
- All outgoing routes are queued for Stage 18.

### 17-INDEX-CLOSURE

#### Big Picture Objective

Screen the complete canonical Index for names, aliases, cross-references, and sections missed by sequential reading without treating Index entries alone as primary construction evidence.

#### Detailed Implementation Plan

- Sequentially inspect every source unit and headword in `BACK-MATTER/Index.md`, assigning explicit no-construction dispositions where appropriate.
- Follow every construction-relevant page route to an already reviewed source unit or reopen the owning chapter stage.
- Record Index-only leads, false positives, and unresolved routes.

#### Completion Requirements

- Every actual-Index source unit/headword is screened; every construction-relevant route is mapped, excluded with reason, or assigned a documented missing target.
- Any missed construction reopens and re-closes its owning stage.
- Index text is never the sole mechanics evidence for an accepted candidate.

### 18-SATURATION

#### Big Picture Objective

Reach a reproducible vocabulary and cross-reference fixed point across the full corpus after sequential discovery is complete.

#### Detailed Implementation Plan

- Run frozen search families over headings, captions, Notes labels, mechanism nouns, update verbs, schedules, probability terms, constraints, generators, equations, and input/output language.
- Add every alias, operation, named example, and parameter learned from reviewed candidates to the next search round.
- Partition every hit into governed candidate/support, duplicate, cross-reference, control, or exclusion.
- Drain all page/section/alias cross-reference queues and inspect every remaining construction-adjacent image.
- Repeat until a full round adds no new vocabulary, candidate, evidence group, or unresolved route.

#### Completion Requirements

- `search-rounds.json` reproduces every round and result digest.
- Every search hit has a disposition and there is no remainder.
- The final round adds zero vocabulary, candidates, evidence, or routes.
- All cross-reference and asset work queues are empty.
- Blind B-candidate artifacts are frozen before Stage 19.

### 19-REDISCOVERY

#### Big Picture Objective

Reveal the existing catalog only after blind discovery, then test whether T01–T45 were independently recovered from the Book.

#### Detailed Implementation Plan

- Snapshot current `CA-Types.csv`, `CA-Types.md`, Goal 1 ledgers/stages, Goal 2 plans, and relevant architecture documents.
- Map each T entry to one or more frozen B candidates without changing blind records.
- Identify T entries not independently rediscovered and diagnose whether the blind pass failed, the catalog is a preset/property rather than a construction, or source support is defective.
- Mine existing exclusion/boundary/future-stage records for candidates the blind audit may have missed; reopen owning discovery stages as needed.

#### Completion Requirements

- Every T01–T45 row has a unique reconciliation record and source-backed result.
- Every B candidate is linked to zero or more T entries without premature final classification.
- Missed Book evidence reopens and re-closes the responsible stage.
- The baseline snapshot and joins are hash-pinned and reproducible.

### 20-DISPOSITIONS

#### Big Picture Objective

Assign every B candidate orthogonal catalog, semantic-role, and family actions and identify proposed catalog additions without conflating them with new semantic families.

#### Detailed Implementation Plan

- Assign one `catalog_action`, one primary `semantic_role`, and one `family_action` to every candidate.
- Assign the exact subtype required by combined roles and typed family
  relations for non-member coverage obligations.
- Compare every candidate against its nearest existing and newly discovered neighbors.
- Require explicit base construction and parameter/predicate for presets and restrictions.
- Require absence of native mechanics for observer/application/emulation roles.
- Require exact missing facts for source-insufficient actions.
- Require a concrete non-preservation counterexample only for `NEW_SEMANTIC_FAMILY`.
- Permit `ADD_CATALOG_ENTRY` for source-important presets, restrictions, seed classes, compositions, declarative categories, or other coverage obligations that reuse an existing family.
- Allocate proposed T46+ identifiers only after all earlier IDs remain stable.

#### Completion Requirements

- Every B candidate has exactly one value on all three classification axes with evidence-backed rationale.
- No `AMBIGUOUS`, `UNREVIEWED`, or silent catch-all row remains on any axis.
- Every proposed T46+ entry has a complete Book evidence packet and justified catalog-level identity.
- Every `NEW_SEMANTIC_FAMILY` row has a nearest-family counterexample; existing-family T46+ rows name their reused family and exact role.
- Every close exclusion/collapse is flagged for hostile review.

### 21-SEMANTIC-FAMILIES

#### Big Picture Objective

Build the deduplicated semantic-family inventory and test newly discovered constructions against the proposed API without allowing API convenience to rewrite the taxonomy.

#### Detailed Implementation Plan

- Group native/declarative catalog entries when either complete fingerprints
  and lossless native-judgment correspondences justify it, or both are proved
  instances/restrictions of the same substantive typed parameterized semantic
  schema with unchanged native mechanics.
- Attach properties, restrictions, seeds, representations, observers,
  applications, emulations, solvers, aliases, and compositions through typed
  `MEMBER_OF`/`INSTANCE_OF`/`RESTRICTS`/`SEEDS`/`REPRESENTS`/`OBSERVES`/
  `APPLIES`/`EMULATES`/`SOLVES`/`COMPOSES`/`ALIASES` relations instead of
  inventing family membership.
- Build near-pair comparisons for schedule, history, branching/probability, structural mutation, input consumption, completion, and witness differences.
- Map each accepted construction to the minimal API fields and result semantics.
- Record where the five-field design fits directly, needs clarification, or genuinely fails.
- State implementation sharing separately from Book catalog identity.

#### Completion Requirements

- Every native or declarative construction has exactly one own-family
  membership; every secondary coverage obligation has at least one typed,
  evidence-backed family relation and no false membership.
- Every same-family claim includes either a lossless native-judgment
  correspondence or a proof of membership in the same substantive typed
  parameterized schema with unchanged mechanics.
- Every close non-equivalence includes a concrete counterexample.
- Every accepted addition has an honest API-pressure disposition with no callback or opaque-packing escape hatch.

### 22-HOSTILE-REVIEW

#### Big Picture Objective

Independently challenge source coverage, every proposed addition, every close exclusion/collapse, every semantic-family grouping, and the audit validators.

#### Detailed Implementation Plan

- Give independent reviewers raw source ranges, frozen ledgers, and explicit challenge assignments.
- Re-read all proposed-new evidence and nearest-family evidence.
- Sample exclusions and no-construction source units across every chapter.
- Test high-risk distinctions: property versus mechanics, seed versus stochastic law, synchronous versus sequential/block schedule, hidden history, graph label evolution versus graph rewrite, application versus coupling, equation versus flow/solver, and emulation versus native construction.
- Run independent coverage arithmetic and destructive mutation tests against copies of the ledgers.
- Route every finding back to the owning stage; no waiver closes a failure.

#### Completion Requirements

- Every proposed addition and close classification has at least one independent review record.
- Sampling covers every canonical segment and every value used on all three final classification axes.
- All validator mutation tests fail when required evidence is removed or corrupted.
- Every hostile finding is resolved by re-opening/re-closing its owning stage.
- `hostile-review.md` has zero unresolved blocking findings.

### 23-FINAL-CENSUS

#### Big Picture Objective

Produce the final evidence-backed whole-book catalog, semantic-family inventory, exact coverage proof, and a non-mutating integration handoff.

#### Detailed Implementation Plan

- Freeze source, ledger, search, classification, and report hashes.
- Generate final catalog and semantic-family counts from verified ledger rows rather than handwritten summaries.
- Report every T01–T45 correction, every proposed T46+ addition, every insufficient-evidence boundary, and every API pressure.
- Explain why every high-risk candidate was included, collapsed, or excluded.
- Write a dependency-aware handoff for later authorized changes to `ref/notes`, Goal 1, Goal 2, API documents, and runtime planning.
- Run all final source, join, mutation, relocation, Markdown, diff, and scope gates.

#### Completion Requirements

- The coverage catalog and semantic-family inventory are complete, internally consistent, and separately counted.
- Every source unit, image, search hit, cross-reference, candidate, T entry, proposed addition, and family join is accounted for.
- No unresolved hostile finding or silent evidence gap remains.
- Final reports state limitations honestly and do not convert insufficient evidence into invented semantics.
- Only `goal-4/` changed unless separate integration was explicitly authorized.
- The original objective—determining whether and how the whole Book expands or corrects the current taxonomy—is actually answered.
