# Goal 4: Source-Faithful ANKoS Markdown Repair

Shorthand: `BOOK-REPAIR`

## Big-Picture Objective

Produce a source-faithful, well-organized, navigable, and deterministically reproducible Markdown edition of the complete local *A New Kind of Science* corpus.

The repaired edition must correct the known split-boundary failures, restore complete and resolvable image coverage, repair Markdown structure, and correct OCR/layout defects across prose, headings, lists, formulas, Wolfram Language code, captions, Notes, and the multi-column Index. Every change must be reversible and traceable to an immutable raw span plus authoritative evidence.

The existing corpus is already used by Goal 1 source oracles and line citations. Goal 4 therefore preserves it byte-for-byte as the legacy raw layer and builds a repaired edition alongside it. Replacing the legacy files or migrating existing citations is a separate future action, not an implicit part of this goal.

Success means an evidence-complete repaired edition, not merely Markdown that renders without errors. If authoritative page-level evidence cannot be obtained for an ambiguous passage, the passage remains explicitly unresolved; plausibility, syntax, model output, and agreement between two derivatives of the same OCR are not transcription proof.

## Required Outcome

Goal 4 must deliver all of the following:

1. An immutable, hash-pinned manifest of every current Markdown and image input.
2. A repaired corpus with correct front matter, 12 chapters, General Notes, 12 chapter Notes sections, Index, and Colophon.
3. A deterministic, reversible build from immutable inputs plus explicit repair records.
4. A complete raw-to-repaired provenance map with no gaps, overlaps, silent deletion, or unexplained duplication.
5. Complete, byte-preserving image accounting and resolvable image references.
6. Sequential, authoritative-witness review of every book-text block.
7. Stricter token-level review of formulas, code, rule tables, captions, and Index entries.
8. Stable navigation, anchors, page mappings, Notes links, and compatibility mappings.
9. An unresolved-defect ledger that prevents unsupported claims of completeness.
10. An independently reviewed, reproducible release with rollback information.

## Non-Negotiable Constraints

1. **Preserve the legacy corpus.** The existing `ref/A-New-Kind-of-Science/**` files are immutable evidence during Goal 4. Hash drift is a hard failure.
2. **Build a repaired edition alongside the legacy files.** The proposed release root is `ref/A-New-Kind-of-Science/REPAIRED/`. Stage 1 must confirm the exact layout without breaking `ref/notes/context/REFACTOR_TARGET.md`.
3. **Do not migrate consumers implicitly.** Goal 1/3 oracles, exact line citations, and source paths continue to target the legacy layer. Goal 4 produces a compatibility map but does not rewrite those consumers.
4. **Never use generated output as the next build's input.** Every build starts from the hash-pinned raw inputs and applies the declared transformation/repair overlay.
5. **Do not edit the only copy.** Structural extraction, repair application, and rendering happen in a fresh build tree before validated output is published atomically.
6. **Authoritative evidence is required for OCR correction.** Use an official/licensed page image, official edition text whose fidelity is established, or another edition-identical primary witness. Record edition, page, source, acquisition date, and hash.
7. **The current split files are not independent OCR witnesses.** They and the monolith generally derive from the same conversion. Agreement can aid routing but cannot prove correctness.
8. **The 1,444 JPEGs are illustrations/crops, not a complete page facsimile.** They cannot establish surrounding prose, column order, omitted figures, or unpictured symbols.
9. **Model guesses are candidate generators only.** Language plausibility, mathematical plausibility, spell-checking, OCR confidence, and syntax success may flag a defect but never authorize a correction.
10. **Do not silently correct the author.** Keep faithful transcription repair separate from source errata annotations and normalized search text. Apparent mathematical, factual, or historical errors remain author text unless the witness proves an OCR error.
11. **Every repair is explicit and reversible.** Each repair has a stable ID, exact preimage, occurrence count, raw location/hash, before/after text, classification, evidence, reviewer state, and inverse.
12. **Fail on preimage drift.** A repair must not apply if its expected raw text, count, source hash, or evidence hash changes.
13. **Structural conservation is exact.** Every raw content span appears exactly once in repaired author text or receives an explicit typed exclusion. Generated metadata is separately labeled.
14. **No unreviewed bulk replacement.** Mechanical rules need an allowlist, bounded contexts, exact expected counts, false-positive review, inverse operation, and mutation test.
15. **Formula and code edits are high risk.** Every changed token needs authoritative visual/textual evidence and independent review. Parsing, rendering, or execution is necessary where useful but never proof of source fidelity.
16. **Index reconstruction requires page-level column evidence.** Do not infer authorial Index order from the flattened OCR or regenerate the Index from body text.
17. **Caption ownership requires evidence.** Filename page numbers and nearest-image proximity are hypotheses. Track printed figure groups because one printed figure may contain several extracted JPEGs.
18. **Assets remain byte-identical.** Do not recompress or silently rename images. Any copy, link, or relocation must preserve SHA-256 and have a manifest mapping.
19. **Accessibility text is editorial metadata.** Generated alt text, summaries, anchors, backlinks, and page markers must not be presented as author text.
20. **Preserve source notation.** Do not rewrite formulas or code into an equivalent modern style. Preserve meaningful punctuation, Unicode, whitespace, and Wolfram Language syntax.
21. **No green-check shortcut.** Link resolution, parser success, balanced fences, and clean rendering prove structural properties only, not transcription accuracy.
22. **Do not claim human review unless a human performed it.** Agent review and automated checks must be labeled accurately.
23. **External witnesses are pinned.** The final build cannot depend on mutable live web content. Record a permitted snapshot or immutable hash/provenance reference.
24. **Respect licensing.** Do not commit external scans or copyrighted witness material unless permitted. Store only the evidence metadata or bounded review artifacts allowed by the source.
25. **Preserve unrelated work.** Scope execution changes to `goal-4/**` and the agreed repaired-output subtree unless the user explicitly authorizes more.
26. **Promotion is separate.** Replacing legacy files, deleting malformed splits, moving existing assets, or switching existing oracles requires explicit user authorization after the repaired release passes.

## Evidence And Repair Model

### Source Roles

- **Legacy raw:** the current 19 Markdown files and 1,444 JPEGs, held immutable.
- **Primary witness:** official/licensed edition-identical page evidence used to verify author text and layout.
- **Secondary routing evidence:** current split Markdown, Atlas, source-oracle crosswalks, dictionaries, parsers, spell-checkers, and OCR tools.
- **Repair overlay:** ordered, reversible records that transform raw blocks into repaired author text or typed metadata.
- **Repaired edition:** deterministically generated output; never an independent historical source.
- **Search normalization:** optional derivative for retrieval, kept separate from faithful book text.

### Repair Classes

Every repair record has exactly one primary class:

- `STRUCTURE_BOUNDARY`
- `MARKDOWN_STRUCTURE`
- `PROSE_OCR`
- `HEADING_OR_FURNITURE`
- `FORMULA_OR_SYMBOL`
- `WOLFRAM_CODE`
- `RULE_TABLE_OR_DATA`
- `FIGURE_OR_CAPTION`
- `INDEX_ENTRY`
- `NAVIGATION_METADATA`
- `SOURCE_ERRATUM_ANNOTATION`
- `SEARCH_NORMALIZATION`

Every candidate has exactly one disposition:

- `APPLIED_MECHANICALLY_PROVEN`
- `APPLIED_WITNESS_VERIFIED`
- `ANNOTATED_SOURCE_ERRATUM`
- `REJECTED_VALID_SOURCE_TEXT`
- `DUPLICATE_CANDIDATE`
- `UNRESOLVED_SOURCE_NEEDED`

`UNRESOLVED_SOURCE_NEEDED` is an honest result but blocks an unqualified “fully repaired” release when the ambiguity can affect author text, mathematics, code, structure, caption ownership, or Index order.

### Minimum Repair Record

Each record must contain:

- stable repair ID;
- source file and immutable file hash;
- raw byte/block identity and logical-line range;
- exact preimage and expected occurrence count;
- repaired text or typed metadata;
- repair class and risk level;
- authoritative witness edition, page/location, and hash;
- rationale and confidence;
- creator and reviewer identity/type;
- dependent repairs;
- before/witness/after render references where applicable;
- forward and inverse operation;
- final disposition and verification results.

## Proposed Output Architecture

Stage 1 must confirm this architecture against repository consumers. The legacy paths remain unchanged.

```text
ref/A-New-Kind-of-Science/
├── [legacy raw files and image directories, unchanged]
└── REPAIRED/
    ├── README.md
    ├── corpus-manifest.json
    ├── release-manifest.json
    ├── A-New-Kind-of-Science.md
    ├── FRONT-MATTER/
    ├── CHAPTERS/
    ├── NOTES/
    ├── BACK-MATTER/
    └── ASSETS/
```

The repaired tree has 29 ordered author-text documents:

- 2 front-matter documents: publication/printed contents and Preface;
- 12 main chapter documents;
- 13 Notes documents: General Notes plus Chapters 1–12;
- 2 back-matter documents: Index and Colophon.

`goal-4/` owns the repair overlays, ledgers, review records, tools, tests, and temporary build policy. Release-safe copies of relevant manifests may be generated into `REPAIRED/`.

Asset materialization—byte-identical copies, generated links, or another portable method—must be chosen in Stage 1 and verified in Stage 6. The released Markdown must have resolving, portable links without changing the legacy binaries.

## Authoritative Inputs

- User instructions and this plan.
- `principles.md`, especially the requirements to preserve real distinctions and verify constructive fidelity.
- `ref/notes/context/REFACTOR_TARGET.md`, which keeps ANKoS references under `ref/A-New-Kind-of-Science` and preserves the front/chapter/back organization.
- The current `ref/A-New-Kind-of-Science/**` corpus as immutable raw input.
- An edition-identical authoritative witness acquired and pinned in Stage 3.
- Existing Goal 1 source/asset oracles as diagnostic and compatibility evidence only; they do not authorize changing raw text.
- `goal-3/0-plan.md` for the independently observed corpus map and structural defects.

## Current Facts

These scaffold-time facts must be independently reverified and hash-pinned in Stage 2:

- The local corpus contains 19 Markdown files and 1,444 JPEGs and occupies about 113 MiB; images account for about 102.56 MiB.
- The complete monolith is 3,780,628 bytes, 22,498 logical lines, 22,497 newline bytes, and lacks a final newline.
- Its scaffold-time SHA-256 is `55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20`.
- Strict UTF-8 inspection found no U+FFFD replacement characters and no common UTF-8-as-Latin-1 mojibake signatures. The major defects are OCR, layout reconstruction, and Markdown structure rather than byte decoding.
- The monolith contains 1,444 image references with 1,444 globally unique basenames, but its bare image paths do not resolve from the monolith.
- The split Markdown contains 1,441 resolving image references. Three physical images are omitted from the split references: `_page_66_Picture_0.jpeg`, `_page_154_Figure_2.jpeg`, and `_page_156_Figure_1.jpeg`.
- Physical/reference ownership is 2 Preface images, 820 main-chapter images, and 622 Notes images. Index and Colophon contain no images.
- Chapter 12's split file crosses into General Notes at split line 2004, then contains Chapter 1 and 2 Notes and part of Chapter 3 Notes.
- `BACK-MATTER/Notes/Notes.md` is one stray Chapter 3 Notes sentence. The nominal `Index.md` contains later Notes. The nominal `Colophon.md` contains still later Notes, then the actual Index at split line 3383 and actual Colophon at split line 5015.
- The actual Index is severely column-flattened. Its opening explanatory sentence and unrelated entries are interleaved; later lines merge many entries and include OCR confusions such as “Ouantum”.
- The Colophon reports 1,280 pages, 583,313 words, 973 illustrations, 1,350 notes, 796 Mathematica programs, and 14,967 Index entries. These are reconciliation clues, not self-proving parser expectations.
- The raw Markdown has 508 fence delimiter lines forming 254 balanced pairs, but some balanced blocks contain prose or corrupted code. Fence parity alone is insufficient.
- Known candidate defects include empty headings, page-furniture headings, split words across blank lines, false hyphen joins, malformed math delimiters, truncated formulas, corrupted logical operators, and damaged Wolfram Language definitions.
- Some extracted JPEGs are only caption crops or partial plates; physical file existence does not prove complete visual evidence.
- No local PDF, EPUB, complete page-scan set, general OCR cleanup script, or Markdown conversion pipeline was found at scaffold time.
- The current split and monolith are correlated derivatives, not independent witnesses.
- Goal 1 contains 57 `*-oracle.py` files at its root, with several hardcoding the current book paths and hashes; many stage documents cite exact monolith lines and malformed split paths.

## Canonical Raw Map

Stage 2 must rederive this map independently:

| Author-text segment | Raw monolith logical lines |
|---|---:|
| Publication and printed contents | 1–85 |
| Preface | 86–167 |
| Chapter 1 | 168–399 |
| Chapter 2 | 400–681 |
| Chapter 3 | 682–1369 |
| Chapter 4 | 1370–2143 |
| Chapter 5 | 2144–2701 |
| Chapter 6 | 2702–3421 |
| Chapter 7 | 3422–4337 |
| Chapter 8 | 4338–5165 |
| Chapter 9 | 5166–6587 |
| Chapter 10 | 6588–7693 |
| Chapter 11 | 7694–8609 |
| Chapter 12 | 8610–10622 |
| General Notes | 10623–10817 |
| Chapter 1 Notes | 10818–10894 |
| Chapter 2 Notes | 10895–11630 |
| Chapter 3 Notes | 11631–12498 |
| Chapter 4 Notes | 12499–13459 |
| Chapter 5 Notes | 13460–14198 |
| Chapter 6 Notes | 14199–14847 |
| Chapter 7 Notes | 14848–15582 |
| Chapter 8 Notes | 15583–16011 |
| Chapter 9 Notes | 16012–17086 |
| Chapter 10 Notes | 17087–18194 |
| Chapter 11 Notes | 18195–19027 |
| Chapter 12 Notes | 19028–20825 |
| Actual Index | 20826–22457 |
| Actual Colophon | 22458–22498 |

## Assumptions To Challenge

- An official/licensed edition-identical page witness can be acquired for every physical page.
- The raw monolith is complete and globally ordered even where individual blocks are corrupted.
- The 29 proposed author-text partitions are sufficient and do not hide additional publication matter.
- Existing image basenames remain globally unique and image bytes are intact.
- A portable repaired release can avoid duplicating 102.56 MiB of assets, or any required duplication is acceptable and byte-verifiable.
- One declared Markdown dialect can represent all prose, formulas, code, lists, tables, figures, and Index structure without semantic loss.
- Printed-page order and raw block order can be related deterministically.
- Existing split formatting improvements can be distinguished from unsupported content changes.
- The reported 14,967 Index entries can be given an operational counting definition that agrees with the authoritative pages.
- Stable repaired anchors can coexist with legacy physical-line citations.
- Automated detectors can reach useful saturation without being treated as proof.
- A full review can distinguish OCR defects from literal authorial errors.

## Required Goal 4 Artifacts

Execution will create and maintain:

- `goal-4/corpus-manifest.json`: raw file hashes, sizes, line counts, roles, image dimensions, and Git identity.
- `goal-4/witness-manifest.json`: authoritative sources, edition/page coverage, acquisition metadata, hashes, permissions, and trust roles.
- `goal-4/structure-ledger.jsonl`: the 29 documents, stable raw blocks, boundaries, headings, page associations, and ownership.
- `goal-4/provenance-map.jsonl`: every raw span to repaired file/anchor and inverse mapping.
- `goal-4/repair-ledger.jsonl`: all reversible repair candidates, evidence, dispositions, and application order.
- `goal-4/unresolved-ledger.jsonl`: source gaps, ambiguities, missing plates, impacts, and unblock actions.
- `goal-4/formula-code-ledger.jsonl`: high-risk token evidence, parse/render status, and independent review.
- `goal-4/figure-caption-asset-ledger.jsonl`: image hashes, printed groups, caption spans, ownership evidence, and alt-text role.
- `goal-4/navigation-ledger.jsonl`: contents, headings, stable anchors, page mappings, Notes links, Index routes, and compatibility targets.
- `goal-4/review-ledger.jsonl`: changed/unchanged review samples, reviewer type, disagreements, and closure.
- `goal-4/release-manifest.json`: input/overlay/tool/output hashes, commands, versions, determinism checks, and rollback data.
- `goal-4/style-guide.md`: the exact Markdown dialect and source/editorial separation rules.
- `goal-4/tools/` and `goal-4/tests/`: deterministic builder, validators, render checks, detector suites, and mutation fixtures.
- `goal-4/reports/`: per-batch coverage, residual-defect, hostile-review, compatibility, and final repair reports.
- `ref/A-New-Kind-of-Science/REPAIRED/`: the validated repaired edition and release-safe manifests.

## Batch Repair Contract

Stages 8–36 process author text. Each assigned batch must:

1. Freeze its raw-block list and authoritative page coverage.
2. Compare every author-text block sequentially against the primary witness.
3. Classify prose, layout, heading, list, formula, code, data, caption, furniture, and cross-reference candidates.
4. Apply only mechanically proven or witness-verified changes through repair records.
5. Preserve literal source errors and add separate errata annotations only when justified.
6. Render before/witness/after views for every changed block.
7. Route formulas, code, rule tables, and figure/caption changes through their stricter ledgers.
8. Give every candidate a final disposition; unresolved high-risk candidates remain release blockers.
9. Rebuild from raw inputs and verify provenance, inverse replay, links, Markdown structure, and deterministic output.
10. Record a changed-block review and a stratified unchanged-block sample.

## Success Metrics

- All 19 legacy Markdown files and 1,444 legacy JPEGs match the frozen hashes.
- Every one of 22,498 raw logical lines and every deterministic raw block is mapped exactly once, with no silent gap, overlap, reorder, deletion, or duplication.
- Exactly 29 ordered repaired author-text documents exist: 2 front matter, 12 chapters, 13 Notes, Index, and Colophon.
- Chapter 12 contains only Chapter 12 main text; all 13 Notes documents have correct ownership; Index and Colophon begin at their actual boundaries.
- Every physical page or authoritative witness unit is covered by the witness and review ledgers.
- Every repair and every unresolved candidate has complete provenance and one final disposition.
- Zero high-risk `UNRESOLVED_SOURCE_NEEDED` items remain in a release claimed as fully repaired.
- All 1,444 image assets are uniquely hash-accounted, byte-identical, and referenced exactly once in canonical author-text order unless a source-proven figure grouping requires typed metadata.
- All 1,444 repaired image references resolve; there are zero missing, orphaned, or silently swapped assets.
- The three split-reference omissions are restored at the correct Chapter 2/4 positions.
- All 254 current fenced regions are classified; no prose remains accidentally fenced and no code is silently lost.
- All formula, code, rule-table, and semantic-data changes have token-level authoritative evidence and independent review.
- Every printed figure/caption group is reviewed with page context; generated alt text is labeled editorial.
- The reconstructed Index is page/column verified, alphabetically/order consistent, and reconciled to the official entry-count definition.
- All headings, fences, HTML, math delimiters, local links, anchors, contents links, Notes backlinks, page routes, and Index cross-references pass structural validation.
- Existing raw paths, raw hashes, Goal 1/3 citations, and source oracles remain valid.
- A clean offline build run twice produces byte-identical repaired output.
- Applying inverse repairs recovers the exact raw text/block hashes after generated metadata is stripped.
- Mutation tests catch raw drift, unlogged edits, missing/reordered blocks, evidence tampering, symbol changes, broken fences, swapped images, caption misassociation, missing assets, and broken/duplicate anchors.
- The final report accurately distinguishes faithful repair, source errata annotations, search normalization, generated metadata, and genuine remaining source limits.

## Verification Requirements

- Independently hash and count raw inputs; do not validate a manifest solely with the code that generated it.
- Independently parse the raw monolith and prove the 29 segment union covers it without gaps or overlaps.
- Build a zero-repair structural baseline first and prove reassembly/inverse equivalence before any OCR repair.
- Run every build from raw inputs into a fresh directory; compare two clean output trees byte-for-byte.
- Run the builder and validators from repository root, a relocated copy, offline, and under optimized Python if Python assertions exist.
- Verify every repair preimage, expected occurrence count, raw hash, witness hash, dependency, and inverse.
- Mutation-test deletion, duplication, reordering, unlogged replacement, witness drift, punctuation/symbol changes, and expected-count drift.
- Parse the repaired Markdown to an AST and render it; inspect unexpected AST/render differences instead of normalizing them away.
- Treat syntax/parser/render checks as structural evidence only.
- Visually review all changed blocks and 100% of formula, code, heading-boundary, figure/caption, image-reference, and Index changes.
- Independently review every high-risk change and a stratified sample of unchanged blocks across all 29 documents.
- Verify all 1,444 image basenames, paths, byte sizes, dimensions, hashes, reference ordinals, and printed-group associations.
- Mutation-test same-page image swaps and incorrect caption associations, not only missing files.
- Verify navigation graph reachability, unique/stable anchors, page mappings, Notes/main links, Index links, and legacy-to-repaired compatibility routes.
- Re-run all residual OCR/layout detectors and require every hit to have a disposition.
- Compare release hashes, tool versions, ledger digests, and commands in `release-manifest.json`.
- Run direct trailing-whitespace, fence, path, schema, and `git diff --check` checks over tracked and untracked Goal 4/repaired outputs.
- Inspect `git status --short` and prove that legacy raw files, Goal 1, Goal 2, Goal 3, runtime, and unrelated references were not modified.

## Stages

### 1-GUARDRAILS

#### Big Picture Objective

Freeze the fidelity contract, output architecture, evidence hierarchy, scope, and conditions under which “fully repaired” may honestly be claimed.

#### Detailed Implementation Plan

- Audit all path consumers and reconcile the proposed `REPAIRED/` tree with repository layout requirements.
- Define immutable/raw, repaired-author-text, errata, search-normalization, and generated-metadata layers.
- Finalize repair classes, risk levels, reviewer requirements, witness policy, licensing limits, and release blockers.
- Decide the portable, byte-preserving asset materialization strategy.
- Document what requires separate authorization: legacy promotion, deletion, relocation, and consumer migration.

#### Completion Requirements

- The architecture has one unambiguous source of build input and one repaired release location.
- No current path/hash consumer is silently invalidated.
- Evidence and waiver rules forbid unsupported OCR correction.
- Scope, rollback, promotion, and licensing rules are explicit and testable.
- Stage 2 can inventory inputs without making content changes.

### 2-BASELINE

#### Big Picture Objective

Create an independent, immutable census of the current corpus and all known structural/OCR risks.

#### Detailed Implementation Plan

- Hash every Markdown/image file and record bytes, logical lines, encoding, dimensions, image basenames, Git blob identity, and role.
- Re-derive the monolith hash/line map and all 29 raw segment boundaries.
- Inventory split ownership, the three omitted references, broken monolith links, path consumers, and known defect candidates.
- Establish raw block IDs and a baseline detector report without applying fixes.
- Record current tool/environment versions and clean/dirty worktree scope.

#### Completion Requirements

- The manifest accounts for 19 Markdown files and 1,444 JPEGs or explains any resynced count.
- Raw hashes and segment arithmetic are independently reproducible.
- All 22,498 logical lines belong to one proposed segment exactly once.
- Every known split/image anomaly has a baseline record.
- Mutation of any raw input causes the baseline verifier to fail.

### 3-WITNESSES

#### Big Picture Objective

Secure and validate authoritative, edition-identical page-level evidence sufficient for a full OCR/layout repair.

#### Detailed Implementation Plan

- Locate official/licensed page images, PDF, print-assisted captures, or equivalent authoritative evidence.
- Verify edition identity, page completeness, page-number mapping, resolution, color/symbol legibility, and Index column visibility.
- Record source URL/location, access date, permissions, file/page hashes, and immutable local review method.
- Compare a stratified sample of prose, formulas, code, figures, Notes, and Index pages against raw OCR to validate witness usefulness.
- Pursue alternate authoritative sources for missing/illegible pages; never fill gaps with inference.

#### Completion Requirements

- Every physical page needed for author-text verification has a pinned, readable witness and deterministic page mapping.
- Formula/code symbols and Index columns are legible in the relevant witness.
- Witness provenance and permitted storage/use are documented.
- Tampered or missing witness pages fail verification.
- If full coverage cannot be obtained, the stage records a decisive source blocker and downstream stages cannot claim a full repair.

### 4-PIPELINE

#### Big Picture Objective

Build the reversible overlay pipeline, ledgers, validators, and mutation suite before changing any author text.

#### Detailed Implementation Plan

- Define machine-readable schemas for structure, provenance, repair, unresolved, technical, figure, navigation, review, and release ledgers.
- Implement stable raw block IDs, exact guarded patches, dependency ordering, forward build, inverse replay, and atomic output publication.
- Build a zero-repair output and prove author-text conservation.
- Add independent validators for coverage, joins, hashes, drift, dispositions, and generated-metadata separation.
- Add mutations for missing/reordered blocks, unlogged edits, source/evidence drift, symbol changes, fences, assets, captions, and anchors.

#### Completion Requirements

- A zero-repair build is deterministic and inverse-recoverable.
- The pipeline refuses stale preimages, wrong occurrence counts, missing evidence, unresolved dependencies, and raw drift.
- Validators run from root and a relocated offline copy and fail closed under declared modes.
- Every required mutation produces a specific failure.
- No repair record has yet altered author text.

### 5-STRUCTURE

#### Big Picture Objective

Create the correctly partitioned 29-document repaired skeleton while preserving raw author text exactly.

#### Detailed Implementation Plan

- Extract the two front-matter, 12 chapter, 13 Notes, Index, and Colophon ranges from the raw monolith.
- Correct ownership boundaries, including the Chapter 12/General Notes transition and malformed nominal back matter.
- Establish heading/document identities, stable anchors, raw-span provenance, and deterministic assembly order.
- Compare existing split files and classify every difference without adopting unsupported content changes.
- Generate a structurally repaired monolith and per-document tree through the zero-content-repair pipeline.

#### Completion Requirements

- Exactly 29 documents cover the raw author-text sequence once.
- Chapter 12, all Notes, Index, and Colophon begin/end at verified boundaries.
- Reassembly differs from raw only by declared structural wrappers/path placeholders/final-newline policy.
- Inverse replay recovers raw block bytes and order.
- Existing split differences all have structural/routing dispositions.

### 6-MEDIA

#### Big Picture Objective

Make all image assets portable, resolvable, byte-preserved, and correctly owned without inferring unsupported figure semantics.

#### Detailed Implementation Plan

- Build the 1,444-row asset manifest with basename, current path, bytes, dimensions, hash, raw reference ordinal, and proposed repaired owner.
- Implement the Stage 1 materialization strategy and deterministic link rewriting.
- Restore the three omitted Chapter 2/4 references from raw order.
- Detect duplicates, orphans, missing/cropped assets, same-page groups, and caption-association candidates.
- Mutation-test missing assets, hash drift, swapped same-page images, wrong links, and silent recompression.

#### Completion Requirements

- All 1,444 governed assets retain their exact bytes/hashes.
- Repaired documents have 1,444 resolving references in raw global order.
- There are zero missing, orphaned, duplicate-identity, or ambiguous basename rows.
- The three known omissions are restored at source-verified positions.
- Figure grouping/caption uncertainty remains typed for Stage 38 rather than guessed.

### 7-STYLE

#### Big Picture Objective

Define and validate a Markdown dialect that improves readability without changing authorial meaning.

#### Detailed Implementation Plan

- Specify heading hierarchy, paragraphs, lists, blockquotes, code fences, math delimiters, HTML, images, captions, tables, page markers, and editorial annotations.
- Separate mechanically safe formatting from witness-dependent text/symbol changes.
- Create fixtures for prose reflow, legitimate/source hyphens, page furniture, nested math, Wolfram code, figure groups, and Index structures.
- Select parser/render tools and define expected AST/render invariants.
- Define guarded formatting rules with exact contexts, counts, inverses, and false-positive tests.

#### Completion Requirements

- `style-guide.md` fully defines the canonical dialect and author/editorial boundary.
- All representative fixtures parse and render as intended.
- No style rule can alter formula/code/data tokens without high-risk evidence review.
- Automated formatting is deterministic, reversible, and mutation-tested.
- Content batches can apply one consistent contract.

### 8-BOOKENDS

#### Big Picture Objective

Repair publication matter, printed contents, Preface, and Colophon against authoritative pages.

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 1–167 and 22458–22498.
- Separate printed book contents from generated repository navigation.
- Verify publication data, names, typography, lists, page furniture, and the Colophon's reported counts.
- Preserve front/back images and distinguish source text from generated metadata.
- Route count discrepancies and publication errata explicitly.

#### Completion Requirements

- Every assigned block/page is witness-reviewed and provenance-mapped.
- Printed contents and generated navigation cannot be confused.
- Every repair/candidate has a final disposition and high-risk review where required.
- Colophon facts remain faithful to the witness, even when they are only reconciliation clues.
- Batch build, inverse, render, link, and review checks pass.

### 9-CH01

#### Big Picture Objective

Produce a witness-verified repaired Chapter 1, “The Foundations for a New Kind of Science.”

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 168–399.
- Verify headings, prose flow, punctuation, image placement, captions, and page furniture sequentially.
- Record all specialist formula/code/figure and navigation items for later closure.
- Rebuild and review the complete chapter in page order.

#### Completion Requirements

- Every Chapter 1 raw block and witness page is reviewed exactly once.
- Every candidate has a disposition; unresolved high-risk items remain release blockers.
- All applied changes are reversible and evidence-linked.
- Chapter render, provenance, links, inverse, and unchanged-sample checks pass.

### 10-CH02

#### Big Picture Objective

Produce a witness-verified repaired Chapter 2, “The Crucial Experiment.”

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 400–681.
- Verify prose, headings, layouts, figure/caption order, and the source position of `_page_66_Picture_0.jpeg`.
- Record specialist and navigation queues and rebuild the whole chapter.

#### Completion Requirements

- Every Chapter 2 block/page is reviewed and dispositioned.
- The previously dropped image reference is restored with source-backed placement.
- All repairs are reversible and evidence-linked.
- Chapter render, provenance, links, inverse, and review checks pass.

### 11-CH03

#### Big Picture Objective

Produce a witness-verified repaired Chapter 3, “The World of Simple Programs.”

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 682–1369.
- Verify system descriptions, rule tables, code-like notation, headings, prose, and figure/caption structures.
- Treat rule numbers, colors, seeds, and update descriptions as protected semantic data.
- Rebuild and review the chapter while routing technical items.

#### Completion Requirements

- Every Chapter 3 block/page is reviewed and dispositioned.
- Semantic data changes have token-level witness evidence.
- All repairs are reversible and evidence-linked.
- Chapter render, provenance, links, inverse, and review checks pass.

### 12-CH04

#### Big Picture Objective

Produce a witness-verified repaired Chapter 4, “Systems Based on Numbers.”

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 1370–2143.
- Verify numeric sequences, formulas, code, captions, and paragraph continuity with protected-token handling.
- Restore `_page_154_Figure_2.jpeg` and `_page_156_Figure_1.jpeg` at witness-backed positions.
- Preserve literal source claims separately from any errata annotation.

#### Completion Requirements

- Every Chapter 4 block/page is reviewed and dispositioned.
- Both previously dropped image references are restored correctly.
- Numeric/formula changes have authoritative token evidence and independent review.
- Chapter render, provenance, links, inverse, and review checks pass.

### 13-CH05

#### Big Picture Objective

Produce a witness-verified repaired Chapter 5, “Two Dimensions and Beyond.”

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 2144–2701.
- Verify multidimensional layouts, neighborhood diagrams, constraints, equations, prose, and captions.
- Protect dimensional notation, coordinates, and rule semantics.
- Rebuild and review the complete chapter.

#### Completion Requirements

- Every Chapter 5 block/page is reviewed and dispositioned.
- Technical and spatial notation changes have authoritative evidence.
- All repairs are reversible and evidence-linked.
- Chapter render, provenance, links, inverse, and review checks pass.

### 14-CH06

#### Big Picture Objective

Produce a witness-verified repaired Chapter 6, “Starting from Randomness.”

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 2702–3421.
- Verify probability/statistical notation, captions, plots, headings, and prose flow.
- Distinguish random source descriptions from OCR/layout artifacts.
- Rebuild and review the complete chapter.

#### Completion Requirements

- Every Chapter 6 block/page is reviewed and dispositioned.
- Probability/data changes have source-backed token evidence.
- All repairs are reversible and evidence-linked.
- Chapter render, provenance, links, inverse, and review checks pass.

### 15-CH07

#### Big Picture Objective

Produce a witness-verified repaired Chapter 7, “Mechanisms in Programs and Nature.”

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 3422–4337.
- Verify program/natural-system terminology, tables, equations, images, and captions.
- Protect names, units, mechanism descriptions, and structured data.
- Rebuild and review the complete chapter.

#### Completion Requirements

- Every Chapter 7 block/page is reviewed and dispositioned.
- Technical changes have authoritative evidence and required review.
- All repairs are reversible and evidence-linked.
- Chapter render, provenance, links, inverse, and review checks pass.

### 16-CH08

#### Big Picture Objective

Produce a witness-verified repaired Chapter 8, “Implications for Everyday Systems.”

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 4338–5165.
- Verify prose, terminology, lists, diagrams, page furniture, and caption association.
- Protect proper names and domain-specific terms from overzealous normalization.
- Rebuild and review the complete chapter.

#### Completion Requirements

- Every Chapter 8 block/page is reviewed and dispositioned.
- Proper-name and terminology changes are witness-backed.
- All repairs are reversible and evidence-linked.
- Chapter render, provenance, links, inverse, and review checks pass.

### 17-CH09

#### Big Picture Objective

Produce a witness-verified repaired Chapter 9, “Fundamental Physics.”

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 5166–6587.
- Verify dense mathematical/physical notation, equations, units, names, figures, and captions.
- Separate source errata from OCR and protect all symbols/numeric data.
- Rebuild and review the complete chapter.

#### Completion Requirements

- Every Chapter 9 block/page is reviewed and dispositioned.
- Every changed symbol, equation, or unit has authoritative token evidence and independent review.
- All repairs are reversible and evidence-linked.
- Chapter render, provenance, links, inverse, and review checks pass.

### 18-CH10

#### Big Picture Objective

Produce a witness-verified repaired Chapter 10, “Processes of Perception and Analysis.”

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 6588–7693.
- Verify algorithms, images, perceptual terminology, formulas, headings, and captions.
- Protect program fragments and experimental labels.
- Rebuild and review the complete chapter.

#### Completion Requirements

- Every Chapter 10 block/page is reviewed and dispositioned.
- Algorithm/code/data changes meet the high-risk evidence contract.
- All repairs are reversible and evidence-linked.
- Chapter render, provenance, links, inverse, and review checks pass.

### 19-CH11

#### Big Picture Objective

Produce a witness-verified repaired Chapter 11, “The Notion of Computation.”

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 7694–8609.
- Verify logic/computation notation, Turing-machine data, code, diagrams, prose, and captions.
- Protect machine rules, state tables, symbols, names, and numerical claims.
- Rebuild and review the complete chapter.

#### Completion Requirements

- Every Chapter 11 block/page is reviewed and dispositioned.
- Machine/data/formula changes have token evidence and independent review.
- All repairs are reversible and evidence-linked.
- Chapter render, provenance, links, inverse, and review checks pass.

### 20-CH12

#### Big Picture Objective

Produce a witness-verified repaired Chapter 12, “The Principle of Computational Equivalence.”

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 8610–10622 only.
- Verify prose, logic/computation terminology, formulas, figures, and the true main-text ending.
- Ensure General Notes and later material cannot leak into the chapter.
- Rebuild and review the complete chapter.

#### Completion Requirements

- Every Chapter 12 main-text block/page is reviewed and dispositioned.
- The repaired chapter ends exactly at the source-backed boundary before General Notes.
- All repairs are reversible and evidence-linked.
- Chapter render, provenance, links, inverse, and review checks pass.

### 21-GENERAL-NOTES

#### Big Picture Objective

Produce witness-verified repaired General Notes as their own document.

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 10623–10817.
- Repair list/paragraph continuations, headings, publication commentary, code-like text, and page furniture.
- Verify the General Notes start/end and preserve their distinction from Chapter 12 and Chapter 1 Notes.
- Rebuild and review the complete document.

#### Completion Requirements

- Every General Notes block/page is reviewed and dispositioned.
- Broken list/paragraph continuations are repaired only with witness support.
- Ownership boundaries are exact and reversible.
- Render, provenance, links, inverse, and review checks pass.

### 22-N01

#### Big Picture Objective

Produce witness-verified repaired Notes for Chapter 1.

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 10818–10894.
- Verify headings, page references, prose, formulas, code, figures, and links back to Chapter 1.
- Rebuild and review the complete Notes document.

#### Completion Requirements

- Every Chapter 1 Notes block/page is reviewed and dispositioned.
- Main-text/page routes are evidence-backed.
- All repairs are reversible and evidence-linked.
- Notes render, provenance, links, inverse, and review checks pass.

### 23-N02

#### Big Picture Objective

Produce witness-verified repaired Notes for Chapter 2.

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 10895–11630.
- Verify headings, rule/data material, formulas, code, figures, captions, and Chapter 2 routes.
- Rebuild and review the complete Notes document.

#### Completion Requirements

- Every Chapter 2 Notes block/page is reviewed and dispositioned.
- Rule/data changes meet the high-risk evidence contract.
- All repairs are reversible and evidence-linked.
- Notes render, provenance, links, inverse, and review checks pass.

### 24-N03

#### Big Picture Objective

Produce witness-verified repaired Notes for Chapter 3.

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 11631–12498.
- Verify system rules, Boolean formulas, Busy Beaver material, Wolfram code, headings, figures, and Chapter 3 routes.
- Investigate empty headings and truncated/highly corrupted technical blocks only against page evidence.
- Rebuild and review the complete Notes document.

#### Completion Requirements

- Every Chapter 3 Notes block/page is reviewed and dispositioned.
- Formula/code/rule-table changes have token evidence and independent review.
- No source content is deleted merely because a heading/block is empty or malformed.
- Notes render, provenance, links, inverse, and review checks pass.

### 25-N04

#### Big Picture Objective

Produce witness-verified repaired Notes for Chapter 4.

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 12499–13459.
- Verify numeric systems, formulas, code, tables, split words, captions, and Chapter 4 routes.
- Review known nested-delimiter, truncated-program, and truncated-PDE candidates against primary pages.
- Rebuild and review the complete Notes document.

#### Completion Requirements

- Every Chapter 4 Notes block/page is reviewed and dispositioned.
- Numeric/formula/code changes meet the high-risk evidence contract.
- Literal source errors remain distinct from OCR repairs.
- Notes render, provenance, links, inverse, and review checks pass.

### 26-N05

#### Big Picture Objective

Produce witness-verified repaired Notes for Chapter 5.

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 13460–14198.
- Verify multidimensional notation, neighborhood/rule data, equations, code, captions, and Chapter 5 routes.
- Protect dimensions, coordinates, topology, and exact operators.
- Rebuild and review the complete Notes document.

#### Completion Requirements

- Every Chapter 5 Notes block/page is reviewed and dispositioned.
- Spatial/technical changes have authoritative token evidence.
- All repairs are reversible and evidence-linked.
- Notes render, provenance, links, inverse, and review checks pass.

### 27-N06

#### Big Picture Objective

Produce witness-verified repaired Notes for Chapter 6.

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 14199–14847.
- Verify stochastic/statistical formulas, code, plots, captions, headings, and Chapter 6 routes.
- Preserve exact probability and distribution semantics.
- Rebuild and review the complete Notes document.

#### Completion Requirements

- Every Chapter 6 Notes block/page is reviewed and dispositioned.
- Probability/data changes have authoritative token evidence.
- All repairs are reversible and evidence-linked.
- Notes render, provenance, links, inverse, and review checks pass.

### 28-N07

#### Big Picture Objective

Produce witness-verified repaired Notes for Chapter 7.

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 14848–15582.
- Verify mechanism descriptions, formulas, programs, figures, captions, names, and Chapter 7 routes.
- Protect units, parameters, and structured rule/data content.
- Rebuild and review the complete Notes document.

#### Completion Requirements

- Every Chapter 7 Notes block/page is reviewed and dispositioned.
- Technical changes satisfy the high-risk evidence contract.
- All repairs are reversible and evidence-linked.
- Notes render, provenance, links, inverse, and review checks pass.

### 29-N08

#### Big Picture Objective

Produce witness-verified repaired Notes for Chapter 8.

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 15583–16011.
- Verify prose, algorithms, names, figures, captions, code, and Chapter 8 routes.
- Protect proper names and domain-specific terms.
- Rebuild and review the complete Notes document.

#### Completion Requirements

- Every Chapter 8 Notes block/page is reviewed and dispositioned.
- Name/algorithm/code changes are witness-backed.
- All repairs are reversible and evidence-linked.
- Notes render, provenance, links, inverse, and review checks pass.

### 30-N09

#### Big Picture Objective

Produce witness-verified repaired Notes for Chapter 9.

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 16012–17086.
- Verify dense physics/mathematics, code, page furniture, figures, captions, and Chapter 9 routes.
- Inspect prose accidentally fenced as code and all symbol-heavy blocks against primary pages.
- Rebuild and review the complete Notes document.

#### Completion Requirements

- Every Chapter 9 Notes block/page is reviewed and dispositioned.
- Misfenced prose and every changed symbol/formula/code token are source-verified.
- Literal author errors remain separate from OCR repair.
- Notes render, provenance, links, inverse, and review checks pass.

### 31-N10

#### Big Picture Objective

Produce witness-verified repaired Notes for Chapter 10.

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 17087–18194.
- Verify algorithms, perceptual data, figures, captions, formulas, code, and Chapter 10 routes.
- Review known malformed Wolfram definitions and page-furniture boundaries against primary pages.
- Rebuild and review the complete Notes document.

#### Completion Requirements

- Every Chapter 10 Notes block/page is reviewed and dispositioned.
- Algorithm/formula/code changes have token evidence and independent review.
- All repairs are reversible and evidence-linked.
- Notes render, provenance, links, inverse, and review checks pass.

### 32-N11

#### Big Picture Objective

Produce witness-verified repaired Notes for Chapter 11.

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 18195–19027.
- Verify computation/logic material, machine tables, formulas, code, figures, captions, and Chapter 11 routes.
- Investigate empty headings and corrupted structured data without deleting uncertain content.
- Rebuild and review the complete Notes document.

#### Completion Requirements

- Every Chapter 11 Notes block/page is reviewed and dispositioned.
- Logic/machine/formula changes satisfy the high-risk evidence contract.
- Empty/malformed blocks have source-backed repairs or explicit blockers.
- Notes render, provenance, links, inverse, and review checks pass.

### 33-N12

#### Big Picture Objective

Produce witness-verified repaired Notes for Chapter 12.

#### Detailed Implementation Plan

- Apply the Batch Repair Contract to raw lines 19028–20825.
- Verify computation-equivalence material, formulas, code, figures, captions, names, and Chapter 12 routes.
- Preserve the true Notes/Index boundary and review all high-risk technical content.
- Rebuild and review the complete Notes document.

#### Completion Requirements

- Every Chapter 12 Notes block/page is reviewed and dispositioned.
- Technical changes have authoritative token evidence and independent review.
- The document ends exactly before the actual Index.
- Notes render, provenance, links, inverse, and review checks pass.

### 34-INDEX-AF

#### Big Picture Objective

Reconstruct and verify the numeric/A–F portion of the actual Index from authoritative multi-column pages.

#### Detailed Implementation Plan

- Establish the source-backed range for numeric through F entries within raw lines 20826–22457.
- Read page columns in authorial order; recover entries, subentries, page ranges, “see”, and “see also” relations.
- Record raw flattened fragments and repaired structured entries without deriving content from body search.
- Verify alphabetical/order monotonicity and page-reference syntax.

#### Completion Requirements

- Every assigned Index page/column and raw fragment is mapped and reviewed.
- Entries and cross-references have page-level evidence and reversible repair records.
- No column order is inferred solely from flattened OCR.
- Count/order/link validators and independent Index review pass.

### 35-INDEX-GM

#### Big Picture Objective

Reconstruct and verify the G–M portion of the actual Index from authoritative multi-column pages.

#### Detailed Implementation Plan

- Apply the Index reconstruction contract to the source-backed G–M range.
- Preserve names, symbols, indentation, page ranges, and cross-reference hierarchy.
- Resolve merged/split entries through page-column evidence and maintain raw-fragment provenance.

#### Completion Requirements

- Every assigned Index page/column and raw fragment is mapped and reviewed.
- All entries/cross-references are evidence-backed and reversible.
- Ordering and reference validators detect merges, omissions, and column swaps.
- Independent Index review passes.

### 36-INDEX-NZ

#### Big Picture Objective

Reconstruct and verify the N–Z portion of the actual Index and close whole-Index reconciliation.

#### Detailed Implementation Plan

- Apply the Index reconstruction contract to N–Z, including known Q/O confusions and long merged lines.
- Reconcile all three Index batches, introductory notes, personal-name policy, entry hierarchy, and final ordering.
- Define and compare the operational extracted-entry count with the Colophon's 14,967 figure.
- Validate all “see” routes and parseable page references without inventing destinations.

#### Completion Requirements

- Every actual Index page/column and raw fragment has final coverage.
- The combined Index is source-ordered, structurally valid, and independently reviewed.
- Entry-count differences from 14,967 are either eliminated or precisely explained by a documented counting definition.
- Zero source-ambiguous Index reconstruction remains in a release claimed complete.

### 37-MATH-CODE

#### Big Picture Objective

Perform a corpus-wide specialist audit of every formula, symbol, rule table, data sequence, and Wolfram Language block.

#### Detailed Implementation Plan

- Enumerate every technical span across the 29 repaired documents and reconcile it with `formula-code-ledger.jsonl`.
- Compare every span token-by-token with authoritative pages, including blocks unchanged by earlier stages.
- Classify all 254 current fenced regions and repair misfenced prose, truncated code, escaped syntax, delimiters, operators, subscripts, and superscripts.
- Parse/render where possible, but retain visual/source review as the authority.
- Independently review every changed technical token and a stratified unchanged sample.

#### Completion Requirements

- Every technical span has a witness, transcription status, parse/render status, and review disposition.
- Zero unreviewed delimiter, fence, formula, code, rule-table, or semantic-data candidate remains.
- Every technical edit is token-evidenced, reversible, and independently reviewed.
- Mutation of one operator, sign, digit, subscript, superscript, brace, or fence fails verification.

### 38-FIGURES

#### Big Picture Objective

Verify every printed figure/caption group, all 1,444 extracted assets, and their repaired placement/accessibility metadata.

#### Detailed Implementation Plan

- Visually compare page witness, caption text, repaired page context, and component images for every printed figure group.
- Confirm image order, crop completeness, scaling/rotation assumptions, caption ownership, and multi-image grouping.
- Identify missing/full-plate limitations separately from available caption crops.
- Add generated alt text only as typed editorial metadata with review status.
- Review same-page swaps and proximity-based associations adversarially.

#### Completion Requirements

- Every asset and printed figure group has page/context evidence and final association status.
- All 1,444 bytes/hashes/references remain correct and resolving.
- Caption text is faithful author text; generated alt text is visibly separate.
- Missing/cropped plate limitations are explicit and cannot masquerade as complete evidence.
- Visual and mutation checks catch swapped images and wrong caption groups.

### 39-NAVIGATION

#### Big Picture Objective

Make the repaired edition coherently navigable while preserving printed-page and legacy-source distinctions.

#### Detailed Implementation Plan

- Generate repository contents, unique stable anchors, main↔Notes links, verified page routes, Index routes, and next/previous navigation.
- Build raw line/block to repaired anchor compatibility mappings for existing Goal 1/3 citations.
- Validate all local file/image links, anchors, page mappings, and graph reachability.
- Keep generated navigation and search normalization outside author text.
- Document how a future authorized migration could adopt repaired anchors.

#### Completion Requirements

- Every repaired document is reachable and all internal links/anchors resolve uniquely.
- Printed contents, generated contents, Index, and search normalization remain distinct.
- Every legacy cited raw block can map to a repaired anchor without changing the raw citation.
- Broken/duplicate anchors, bad page routes, and unreachable documents fail verification.
- No consumer migration occurs in this stage.

### 40-SATURATION

#### Big Picture Objective

Reach a documented fixed point for residual OCR, layout, markup, and provenance defects.

#### Detailed Implementation Plan

- Re-run candidate detectors for blank/furniture headings, numeric-only lines, word splits, hyphens, OCR confusions, long Index lines, delimiters, brackets, fences, orphan continuations, and malformed links.
- Add new detector rounds from defects found during manual review and rerun them over all 29 documents.
- Give every hit a confirmed/rejected/duplicate/unresolved disposition with exact scope.
- Build a stratified prose gold set across front/back matter, all chapters, all Notes, and Index; measure character/word error after defining the baseline.
- Reopen affected batches whenever the gold set or detector mutations reveal a material miss.

#### Completion Requirements

- Repeated detector/review rounds produce no new undispositioned defect class.
- Every detector hit has a ledger disposition and zero severity-1/2 defect remains.
- The gold-set methodology, coverage, and results are reproducible; zero material semantic error remains in it.
- All ledgers join totally and every raw/output/evidence block is accounted for.
- Any remaining source limitation is explicit and blocks an overbroad completeness claim.

### 41-HOSTILE

#### Big Picture Objective

Independently attempt to falsify the repaired edition's fidelity, completeness, reversibility, and reproducibility.

#### Detailed Implementation Plan

- Review every high-risk repair plus stratified changed/unchanged samples across all 29 documents.
- Attack boundary ownership, raw conservation, witness identity, repair inverses, formula/code tokens, Index columns, figures/captions, links, and compatibility routes.
- Run the full mutation suite and add mutations for every newly discovered validator weakness.
- Compare rendered raw/witness/repaired triptychs and investigate every unexpected difference.
- Reopen prior stages and record closure for all hostile findings.

#### Completion Requirements

- Every hostile finding is fixed, disproved with evidence, or remains an explicit release blocker.
- All required mutations fail for the intended reason.
- Independent review coverage and reviewer type are truthfully recorded.
- A fresh hostile rerun finds no unclosed high-risk discrepancy.
- Legacy raw scope remains untouched.

### 42-RELEASE

#### Big Picture Objective

Publish a deterministic, source-faithful repaired edition with complete provenance, rollback, limitations, and compatibility documentation.

#### Detailed Implementation Plan

- Build twice from frozen raw inputs and repair overlays in fresh offline/relocated environments.
- Compare output bytes, manifests, ledgers, navigation, rendered artifacts, and tool versions.
- Run all structural, content, asset, review, mutation, whitespace, and Git-scope checks.
- Publish atomically to the agreed `REPAIRED/` location and write the release manifest/final report.
- Document exact rollback/rebuild commands, remaining source limitations, and optional future legacy-promotion/migration work.

#### Completion Requirements

- Two clean builds are byte-identical and inverse replay recovers the frozen raw text/block hashes.
- All 29 documents, 1,444 assets/references, ledgers, links, anchors, evidence joins, and review gates pass.
- No high-risk unresolved item remains in a release called fully repaired.
- Legacy raw hashes/paths and all unrelated repository files remain unchanged.
- The final report clearly distinguishes repaired transcription, source errata, generated metadata, search normalization, and any residual limits.
- Completion reflects the original full-repair objective rather than a structurally cleaner but unverified subset.
