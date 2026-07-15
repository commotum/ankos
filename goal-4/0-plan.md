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

1. **Preserve an explicit legacy-input allowlist.** The 19 existing Markdown files and 1,444 existing JPEGs under `ref/A-New-Kind-of-Science/` are immutable evidence during Goal 4. Hash drift is a hard failure. Future output is never discovered as raw input through an unconstrained recursive glob.
2. **Use a new sibling folder.** Build the repaired edition at `ref/A-New-Kind-of-Science-Repaired/`, never inside the legacy root. This prevents repaired Markdown and copied assets from contaminating Goal 1's recursive file counts and basename checks.
3. **Do not migrate consumers implicitly.** Goal 1/3 oracles, exact line citations, and source paths continue to target the legacy layer. Goal 4 produces a compatibility map and snapshots consumer behavior but does not rewrite those consumers.
4. **Never use generated output as the next build's input.** Every build starts from the hash-pinned raw inputs and applies the declared transformation/repair overlay.
5. **Do not edit the only copy.** Structural extraction, repair application, and rendering happen in a fresh build tree before validated output is published atomically.
6. **Authoritative evidence is required for OCR correction.** Use an official/licensed page image, official edition text whose fidelity is established, or another edition-identical primary witness. Record edition, page, source, acquisition date, and hash.
7. **The current split files are not independent OCR witnesses.** They and the monolith generally derive from the same conversion. Agreement can aid routing but cannot prove correctness.
8. **The 1,444 JPEGs are illustrations/crops, not a complete page facsimile.** They cannot establish surrounding prose, column order, omitted figures, or unpictured symbols.
9. **Model guesses are candidate generators only.** Language plausibility, mathematical plausibility, spell-checking, OCR confidence, and syntax success may flag a defect but never authorize a correction.
10. **Do not silently correct the author.** Keep faithful transcription repair separate from source errata annotations and normalized search text. Apparent mathematical, factual, or historical errors remain author text unless the witness proves an OCR error.
11. **Every repair is explicit and reversible.** Each replacement, deletion, move, or source-verified insertion has a stable ID, guarded preimage or two-sided insertion anchors, occurrence count, raw/witness location and hashes, before/after text, classification, evidence, reviewer state, and inverse.
12. **Fail on preimage drift.** A repair must not apply if its expected raw text, count, source hash, or evidence hash changes.
13. **Conservation is two-way.** Every monolith author-text span appears exactly once in the canonical repaired documents or receives an explicit typed exclusion; every authoritative page region maps to repaired output, a narrowly typed `NOT_APPLICABLE` non-authorial reason, or a release-blocking source gap; and every repaired author-text span maps to raw text or an authoritative-witness insertion record. `NOT_APPLICABLE` reasons are enumerated, evidenced, and independently reviewed; illegible or untranscribed authorial content is always a blocker. Generated metadata is separately labeled.
14. **No unreviewed bulk replacement.** Mechanical rules need an allowlist, bounded contexts, exact expected counts, false-positive review, inverse operation, and mutation test. `APPLIED_MECHANICALLY_PROVEN` is restricted to non-author-text structure/path/metadata or byte-preserving transformations; every author-text token change, including repeated dehyphenation, is `APPLIED_WITNESS_VERIFIED` per occurrence.
15. **Formula and code edits are high risk.** Every changed token needs authoritative visual/textual evidence and independently recorded review by someone other than the change author. Parsing, rendering, or execution is necessary where useful but never proof of source fidelity.
16. **Index reconstruction requires page-level column evidence.** Do not infer authorial Index order from the flattened OCR or regenerate the Index from body text.
17. **Caption ownership requires evidence.** Filename page numbers and nearest-image proximity are hypotheses. Track printed figure groups because one printed figure may contain several extracted JPEGs.
18. **Legacy assets remain byte-identical.** Do not recompress or silently rename images. The sibling repaired folder may contain manifest-governed byte-identical copies and source-verified replacement/full-plate assets; distinct asset IDs must never be silently deduplicated merely because bytes match.
19. **Accessibility text is editorial metadata.** Generated alt text, summaries, anchors, backlinks, and page markers must not be presented as author text.
20. **Preserve source notation.** Do not rewrite formulas or code into an equivalent modern style. Preserve meaningful punctuation, Unicode, whitespace, and Wolfram Language syntax.
21. **No green-check shortcut.** Link resolution, parser success, balanced fences, and clean rendering prove structural properties only, not transcription accuracy.
22. **Do not claim human review unless a human performed it.** Agent review and automated checks must be labeled accurately.
23. **Separate build and audit modes.** Reproducible build mode uses frozen raw inputs plus overlays without a network dependency. Audit mode mounts the authorized primary witness read-only and rechecks the content evidence. A bare witness hash proves identity, not content; an unavailable licensed witness permits rebuilding but blocks fresh fidelity certification.
24. **Respect licensing.** Do not commit external scans or copyrighted witness material unless permitted. Store only permitted evidence metadata or bounded review artifacts; otherwise record the authorized witness-mount contract.
25. **Preserve unrelated work.** Scope execution changes to `goal-4/**` and `ref/A-New-Kind-of-Science-Repaired/**` unless the user explicitly authorizes more.
26. **Promotion is separate.** Replacing legacy files, deleting malformed splits, moving existing assets, or switching existing oracles requires explicit user authorization after the repaired release passes.
27. **An unqualified full-repair claim has no authorial ambiguity.** Any `UNRESOLVED_SOURCE_NEEDED` item affecting author text, typography/layout, structure, formula/code/data, visual content/caption ownership, or Index order blocks “fully repaired.” Only optional editorial enhancements may remain unresolved.

## Evidence And Repair Model

### Source Roles

- **Legacy raw author text:** the current monolith, whose spans receive line/block provenance.
- **Legacy routing witnesses:** the 17 current split/front/back Markdown derivatives, which remain hash-pinned and receive routing/difference dispositions but are not duplicated into author text.
- **Interpretive metadata:** `ANKoS-Atlas.md`, preserved by hash but excluded from author-text conservation.
- **Legacy assets:** the current 1,444 JPEGs, held immutable.
- **Primary witness:** official/licensed edition-identical page evidence used to verify author text and layout.
- **Secondary routing evidence:** current split Markdown, Atlas, source-oracle crosswalks, dictionaries, parsers, spell-checkers, and OCR tools.
- **Repair overlay:** ordered, reversible records that transform raw blocks into repaired author text or typed metadata.
- **Canonical repaired documents:** the 29 author-text documents and the only domain for exactly-once author-text/reference accounting.
- **Derived aggregate:** an assembled monolith generated from the 29 canonical documents and excluded from canonical exactly-once counts.
- **Editorial sidecars:** errata, alt text, and review notes that never enter canonical author text by default.
- **Search normalization:** an optional separate output target for retrieval, never applied to faithful author text.

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

Workflow state is separate from final disposition:

- `CAPTURED`
- `EVIDENCE_READY`
- `PENDING_SPECIALIST_REVIEW`
- `PENDING_INDEPENDENT_REVIEW`
- `SOURCE_BLOCKED`
- `CLOSED`

A sequential batch may finish with a governed pending specialist/reviewer state only when the owning later stage is explicit. Release requires every authorial candidate to be `CLOSED` with a final disposition.

In stage completion language below, “reviewed and dispositioned” means either `CLOSED` with a final disposition or routed to one explicit governed pending state; it never means falsely declaring queued specialist work final. Each raw block is assigned to one content batch and reviewed at least once by every required role. Pages that straddle boundaries are divided into nonoverlapping witness regions rather than assigned exclusively as whole pages.

### Minimum Repair Record

Each record must contain:

- stable repair ID;
- operation type: replace, delete, move, split/merge, or anchored insert;
- source file and immutable file hash;
- raw byte/block identity and logical-line range;
- exact preimage and expected occurrence count, or stable left/right anchors and expected adjacency for text absent from raw OCR;
- repaired text or typed metadata;
- repair class and risk level;
- class-conditional evidence:
  - authoritative witness edition, page-region/location, and hash for author-text/layout changes;
  - independently reproducible mechanical proof for non-author-text structure/path/generated metadata;
- rationale and confidence;
- creator and reviewer identity/type;
- dependent repairs;
- before/witness/after render references where applicable;
- forward and inverse operation;
- final disposition and verification results.

## Proposed Output Architecture

Stage 1 must freeze all 29 canonical relative paths and their order. The legacy folder remains unchanged, and the repaired edition lives in a new sibling folder.

```text
ref/
├── A-New-Kind-of-Science/                 # immutable legacy corpus
└── A-New-Kind-of-Science-Repaired/        # new generated edition
    ├── README.md
    ├── corpus-manifest.json
    ├── release-manifest.json
    ├── CANONICAL/
    │   ├── FRONT-MATTER/
    │   │   ├── 00-Publication-and-Contents.md
    │   │   └── 01-Preface.md
    │   ├── CHAPTERS/
    │   │   ├── 01-The-Foundations-for-a-New-Kind-of-Science.md
    │   │   ├── ...
    │   │   └── 12-The-Principle-of-Computational-Equivalence.md
    │   └── BACK-MATTER/
    │       ├── NOTES/
    │       │   ├── 00-General-Notes.md
    │       │   ├── ...
    │       │   └── 12-The-Principle-of-Computational-Equivalence-Notes.md
    │       ├── Index.md
    │       └── Colophon.md
    ├── DERIVED/
    │   ├── A-New-Kind-of-Science.md
    │   └── Contents.md
    ├── EDITORIAL/
    │   ├── Errata.md
    │   └── Alt-Text.md
    ├── SEARCH/
    └── ASSETS/
```

The repaired tree has 29 ordered author-text documents:

- 2 front-matter documents: publication/printed contents and Preface;
- 12 main chapter documents;
- 13 Notes documents: General Notes plus Chapters 1–12;
- 2 back-matter documents: Index and Colophon.

The manifest assigns `CANONICAL_AUTHOR_TEXT` to exactly 29 documents, `DERIVED_AGGREGATE` to the assembled monolith, and `GENERATED_METADATA`/`EDITORIAL_SIDECAR`/`SEARCH_DERIVATIVE` to the other outputs. Validators count by role, never by an unrestricted `rglob("*.md")`. The derived monolith has its own expected span/reference counts and is intentionally excluded from canonical exactly-once accounting.

`goal-4/` owns the repair overlays, ledgers, review records, tools, tests, and fresh staging builds. A validated release is published atomically to the empty or manifest-owned sibling folder; pre-existing unowned content is never overwritten.

The portable repaired release uses manifest-governed asset files rather than hardlinks or fragile symlinks. Stage 6 preserves all 1,444 legacy asset identities and establishes the zero-repair reference baseline. Stage 38 separately determines the final witness-complete printed-figure/component inventory and any lawful source-verified replacements.

## Authoritative Inputs

- User instructions and this plan.
- `principles.md`, especially the requirements to preserve real distinctions and verify constructive fidelity.
- `ref/notes/context/REFACTOR_TARGET.md`, which keeps ANKoS references under `ref/A-New-Kind-of-Science` and preserves the front/chapter/back organization.
- The current `ref/A-New-Kind-of-Science/**` corpus as immutable raw input.
- An edition-identical authoritative witness acquired and pinned under the Stage 3 schema; acquisition is currently `SOURCE_BLOCKED` pending permission or a separately licensed witness.
- Existing Goal 1 source/asset oracles as diagnostic and compatibility evidence only; they do not authorize changing raw text.
- `goal-3/0-plan.md` for the independently observed corpus map and structural defects.

## Current Facts

These scaffold-time facts must be independently reverified and hash-pinned in Stage 2:

- The local corpus contains 19 Markdown files and 1,444 JPEGs: 115,037,515 logical bytes (about 109.71 MiB) and 118,206,464 allocated bytes (about 112.73 MiB). JPEG payload is about 102.56 MiB.
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
- The monolith has 508 fence delimiter lines forming 254 balanced pairs; all 19 Markdown files contain 1,012 fence delimiter lines because split derivatives duplicate content. Some balanced blocks contain prose or corrupted code. Fence parity alone is insufficient.
- Known candidate defects include empty headings, page-furniture headings, split words across blank lines, false hyphen joins, malformed math delimiters, truncated formulas, corrupted logical operators, and damaged Wolfram Language definitions.
- Some extracted JPEGs are only caption crops or partial plates; physical file existence does not prove complete visual evidence.
- No local PDF, EPUB, complete page-scan set, general OCR cleanup script, or Markdown conversion pipeline was found at scaffold time.
- The current split and monolith are correlated derivatives, not independent witnesses.
- Goal 1 currently contains 58 `*-oracle.py` files at its root. At scaffold review, at least 39 recursively enumerated legacy Markdown and at least 24 recursively enumerated images/basenames; many also hardcode current paths, hashes, line counts, or malformed split paths.

## Known Defect Regression Sentinels

Stage 2 must freeze an exact regression row for every already observed defect, including at least:

- structural boundary drift: Chapter 12 split line 2004, the one-line nominal Notes file, Notes stored in nominal Index/Colophon, actual Index at Colophon split line 3383, and actual Colophon at split line 5015;
- the three missing split image references at monolith lines 680, 1711, and 1744, preserving raw reference ordinals;
- caption/prose interleaving at monolith lines 2130–2132;
- prose/math splitting at 12891/12893;
- prose accidentally fenced as code plus a hyphen split at 16433–16438;
- empty headings at 12083, 12087, 18328, and 18810;
- the complete observed page-furniture/false-heading inventory, including examples at 398, 1368, 2700, 6586, and 17444;
- corrupted Boolean-rule formulas at 11711–11841;
- truncated/mangled program and maxima material at 12377 and 12382;
- truncated PDE material at 13453;
- damaged Wolfram definitions at 17301 and 17442;
- damaged mathematical delimiters/notation at 19567;
- severe Index column flattening and merged entries at 21877;
- known joined/split-word candidates such as 10631, 12079, 12891–12893, 13294, 14031, 16429, 17273, 17793, and 20109.

These are regression sentinels, not preauthorized corrections. Each must be detected or manually routed and receive a source-backed final disposition in Stages 40/42.

## Canonical Raw Map

Stage 2 must rederive this provisional map independently and issue immutable segment IDs plus witness-backed start/end signatures. Downstream stages consume those IDs from the structure ledger, not copied line literals; the ranges below are scaffold routing hints and may include printed page-furniture lines at chapter edges.

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
- `goal-4/witness-manifest.json`: authoritative sources, edition fingerprint, complete physical-page/plate census, page-region coverage/legibility, acquisition metadata, hashes, permissions, mount contract, and trust roles.
- `goal-4/witness-region-ledger.jsonl`: every authoritative page/column/figure/text region to canonical repaired output, an evidenced/independently reviewed non-authorial `NOT_APPLICABLE` reason, or a release-blocking gap.
- `goal-4/structure-ledger.jsonl`: the 29 documents, stable raw blocks, boundaries, headings, page associations, and ownership.
- `goal-4/provenance-map.jsonl`: bidirectional raw/witness-region↔repaired-span mappings and inverse operations.
- `goal-4/repair-ledger.jsonl`: all reversible repair candidates, evidence, dispositions, and application order.
- `goal-4/unresolved-ledger.jsonl`: source gaps, ambiguities, missing plates, impacts, and unblock actions.
- `goal-4/known-defect-regression.jsonl`: exact baseline sentinels, required routes, mutations, and final dispositions.
- `goal-4/quality-evaluation.json`: pre-frozen sample frame, manifest-derived random seed, per-document/risk quotas, severity definitions, blind transcription/adjudication, projections, and thresholds.
- `goal-4/formula-code-ledger.jsonl`: high-risk token evidence, parse/render status, and independent review.
- `goal-4/figure-caption-asset-ledger.jsonl`: image hashes, printed groups, caption spans, ownership evidence, and alt-text role.
- `goal-4/navigation-ledger.jsonl`: contents, headings, stable anchors, page mappings, Notes links, Index routes, and compatibility targets.
- `goal-4/review-ledger.jsonl`: changed/unchanged review samples, reviewer type, disagreements, and closure.
- `goal-4/compatibility-baseline.json`: affected Goal 1 oracle commands/output digests before the sibling repaired folder exists and after release.
- `goal-4/release-manifest.json`: input/overlay/tool/output hashes, commands, versions, determinism checks, and rollback data.
- `goal-4/style-guide.md`: the exact Markdown dialect and source/editorial separation rules.
- `goal-4/tools/` and `goal-4/tests/`: deterministic builder, validators, render checks, detector suites, and mutation fixtures.
- `goal-4/reports/`: per-batch coverage, residual-defect, hostile-review, compatibility, and final repair reports.
- `ref/A-New-Kind-of-Science-Repaired/`: the validated repaired edition and release-safe manifests.

## Batch Repair Contract

Stages 8–36 process author text. Each assigned batch must:

1. Freeze its unique raw-block assignments and nonoverlapping authoritative page-region coverage from the ledgers.
2. Compare every author-text block and every assigned witness region sequentially; source-visible content missing from raw OCR becomes a guarded insertion candidate.
3. Classify prose, layout, heading, list, formula, code, data, caption, furniture, and cross-reference candidates.
4. Apply mechanically proven changes only outside author text; apply every author-text token/layout change through a per-occurrence witness-verified repair record.
5. Preserve literal source errors and add separate errata annotations only when justified.
6. Render before/witness/after views for every changed block.
7. Route formulas, code, rule tables, and figure/caption changes through their stricter ledgers.
8. Give every candidate either a closed final disposition or a governed pending specialist/reviewer workflow state with an owning later stage. Any source-needed authorial item remains a release blocker.
9. Rebuild from raw inputs and verify provenance, inverse replay, links, Markdown structure, and deterministic output.
10. Record changed-block review and the pre-frozen held-out unchanged/changed sample without choosing samples after results are visible.

## Success Metrics

- All 19 legacy Markdown files and 1,444 legacy JPEGs match the frozen hashes.
- Every one of the monolith's 22,498 raw logical lines and every deterministic raw author-text block maps into the 29 `CANONICAL_AUTHOR_TEXT` documents exactly once, with no silent gap, overlap, reorder, deletion, or duplication; all 17 split derivatives have routing/difference dispositions and Atlas remains separate metadata.
- Exactly 29 ordered `CANONICAL_AUTHOR_TEXT` documents exist: 2 front matter, 12 chapters, 13 Notes, Index, and Colophon. The `DERIVED_AGGREGATE` monolith is excluded from this count and separately reproduces canonical sequence/counts.
- Chapter 12 contains only Chapter 12 main text; all 13 Notes documents have correct ownership; Index and Colophon begin at their actual boundaries.
- Every physical leaf/page/plate derived from the authoritative witness is present in the census with edition identity and per-region legibility or an independently reviewed non-authorial `NOT_APPLICABLE` status; no blank, figure-only, or Index page disappears silently. The witness-derived count is reconciled to the Colophon's 1,280-page clue under a documented counting definition rather than forced to equal it.
- Every repair and candidate has complete provenance, workflow closure, and one final disposition.
- Zero `UNRESOLVED_SOURCE_NEEDED` item affecting an authorial layer remains in a release claimed as fully repaired.
- The Stage 6 zero-repair canonical baseline contains the monolith's 1,444 legacy image references in identical order and ownership totals of Preface 2, chapters 820, Notes 622, and zero elsewhere; the derived aggregate independently mirrors that count/order.
- All 1,444 legacy assets retain distinct IDs and byte hashes. Final canonical visual references are governed by the Stage 38 printed-page/figure-component census, with every addition/replacement source-verified and no missing, orphaned, silently swapped, or incomplete authorial visual component in an unqualified full release.
- The three split-reference omissions are restored at the correct Chapter 2/4 positions.
- All 254 current fenced regions are classified; no prose remains accidentally fenced and no code is silently lost.
- All formula, code, rule-table, and semantic-data changes have token-level authoritative evidence and independent review.
- Every printed figure/caption group and component is reviewed with page context; generated alt text is labeled editorial. Operational counts for illustrations, Notes, programs, and Index entries are reconciled with the Colophon's 973/1,350/796/14,967 clues and differences are explained rather than forced.
- The reconstructed Index is page/column verified, alphabetically/order consistent, and reconciled to the official entry-count definition.
- All headings, fences, HTML, math delimiters, local links, anchors, contents links, Notes backlinks, page routes, and Index cross-references pass structural validation.
- Existing raw paths, raw hashes, Goal 1/3 citations, and affected Goal 1 source/asset-oracle output digests remain behaviorally identical after the sibling release is present.
- A clean offline build run twice produces byte-identical repaired output.
- Applying inverse repairs recovers the exact raw text/block hashes after generated metadata is stripped.
- Mutation tests catch raw drift, unlogged replacement/insertion/deletion, missing/reordered blocks or witness regions, evidence tampering, symbol changes, broken fences, swapped or missing/witness-only images, caption misassociation, generated-view double counting, accidental raw-census contamination, and broken/duplicate anchors.
- The pre-frozen independent gold set passes class-specific thresholds: exact author-text character projection, heading/paragraph/list boundary exactness, technical token exactness, Index entry/column sequence exactness, and figure/caption association exactness. Severity definitions and sample selection were fixed before repair results.
- The final report accurately distinguishes faithful repair, source errata annotations, search normalization, generated metadata, and genuine remaining source limits.

## Verification Requirements

- Independently hash and count raw inputs; do not validate a manifest solely with the code that generated it.
- Independently parse the raw monolith and prove the 29 segment union covers it without gaps or overlaps.
- Independently parse the witness page/region census and prove every authorial region maps to canonical output or a release blocker, every `NOT_APPLICABLE` region is demonstrably non-authorial, and every canonical span maps back to raw text or witness-backed insertion evidence.
- Build a zero-repair structural baseline first and prove reassembly/inverse equivalence before any OCR repair.
- Run every build from raw inputs into a fresh directory; compare two clean output trees byte-for-byte.
- Run the builder and validators from repository root, a relocated copy, offline, and under optimized Python if Python assertions exist.
- Verify every repair operation, guarded preimage/anchors, expected occurrence/adjacency count, raw hash, class-conditional evidence, witness hash where required, dependency, and inverse.
- Mutation-test deletion, duplication, reordering, unlogged replacement/insertion, witness drift, punctuation/symbol changes, and expected-count/anchor drift.
- Parse the repaired Markdown to an AST and render it; inspect unexpected AST/render differences instead of normalizing them away.
- Treat syntax/parser/render checks as structural evidence only.
- Visually review all changed blocks and 100% of formula, code, heading-boundary, figure/caption, image-reference, and Index changes.
- Machine-enforce creator ID ≠ reviewer ID for high-risk records, evidence-view hashes, independent pre-proposal transcription/association decisions, and zero unresolved disagreement.
- Independently review every high-risk change and the pre-frozen stratified unchanged/changed sample across all 29 documents.
- Verify all 1,444 legacy image asset IDs, basenames, paths, byte sizes, dimensions, hashes, reference ordinals, and final printed-group/component associations without assuming byte-hash uniqueness.
- Mutation-test same-page image swaps and incorrect caption associations, not only missing files.
- Verify navigation graph reachability, unique/stable anchors, page mappings, Notes/main links, Index links, and legacy-to-repaired compatibility routes.
- Re-run all residual OCR/layout detectors and require every hit to have a disposition.
- Require detector recall over the known-defect registry and seeded defect mutations, then two consecutive full manual+detector rounds with no new defect class and empty queues after the last newly discovered class.
- Compare release hashes, tool versions, ledger digests, and commands in `release-manifest.json`.
- Run direct trailing-whitespace, fence, path, schema, and `git diff --check` checks over tracked and untracked Goal 4/repaired outputs.
- Inspect `git status --short` and prove that legacy raw files, Goal 1, Goal 2, Goal 3, runtime, and unrelated references were not modified.
- Re-run and compare all affected Goal 1 oracle output digests; in a temporary legacy fixture, add a sentinel nested Markdown file and duplicate-basename JPEG and prove the compatibility validator detects behavioral contamination.

## Current Execution State

- Synced: 2026-07-14 (America/Los_Angeles).
- Active stage: `4-PIPELINE` (`IN_PROGRESS`).
- The sibling release root `ref/A-New-Kind-of-Science-Repaired/` exists as an empty publication target; no unverified partial release has been placed in it.
- Stage 1 completed with 59 Goal 1 root oracles classified, all 40 affected oracles behaviorally frozen, 1,510 governed dependency rows re-derived, 39 mutation tests passing, and three independent hostile reviews passing.
- Stage 2 completed with all 1,463 raw inputs independently hash/Git/LFS/JPEG verified; 29 proposed segments and 20,430 raw blocks frozen; 1,444 image references, 32 routing dispositions, 55 defect sentinels, and 1,125 held-out IDs bound under externally pinned lock `57224a1f1ba8333bbc900b23ff6127a189649feb01c279f30fac05a305658863`; 27 Stage 2 mutation tests and three hostile reviews passed in normal, optimized, portable no-Git, and relocated modes.
- Stage 3 froze the primary-witness, physical-unit, region, legibility, mount, licensing, and source-gap schemas. The official First Edition, Fourth Printing online surface was identified, but its posted terms do not authorize the required bulk or AI-assisted audit; no complete witness was acquired or retained. All 29 segments, 20,430 raw blocks, 1,444 legacy visual candidates, and 1,125 held-out items are explicitly source-blocked under externally pinned witness lock `f348e4dd0ebf328c48066696eb70359d954e07cbdfd7b7fd827286e3268ba449`; 30 Stage 3 mutation tests pass in normal and optimized modes. Witness-dependent author-text correction and an unqualified full-repair claim remain blocked, while dependency-independent Stages 4–7 may proceed.
- Protected unrelated Goal 1 work remains outside Goal 4's write scope.
- Goal 4 execution writes remain restricted to `goal-4/**` and, only in later owning stages, `ref/A-New-Kind-of-Science-Repaired/**`.

## Stage Dependencies And Status

Keep one current status per stage and at most one `IN_PROGRESS` stage. `SOURCE_BLOCKED`/`REVIEW_BLOCKED` stages do not prevent dependency-independent work; select the lowest-numbered incomplete stage whose actual prerequisites are ready.

| Stages | Current status | Prerequisites |
|---|---|---|
| 1 | `COMPLETE` | none |
| 2 | `COMPLETE` | 1 |
| 3 | `SOURCE_BLOCKED` | 1–2; written bulk/AI audit permission or a separately licensed complete witness is missing |
| 4 | `IN_PROGRESS` | 1–2; witness schema frozen, full witness coverage pending |
| 5 | `NOT_STARTED` | 1–2, 4 |
| 6 | `NOT_STARTED` | 1–2, 4–5 |
| 7 | `NOT_STARTED` | 1, 4–6 |
| 8–36 | `NOT_STARTED` | 2–7 plus complete witness-region coverage for the assigned batch; batches are otherwise independent |
| 37 | `NOT_STARTED` | all relevant 8–36 technical queues |
| 38 | `NOT_STARTED` | 6 plus all relevant 8–36 figure queues and page/plate evidence |
| 39 | `NOT_STARTED` | 5–7 and all 8–36 canonical documents |
| 40 | `NOT_STARTED` | 37–39 |
| 41 | `NOT_STARTED` | 40 |
| 42 | `NOT_STARTED` | 41 and zero release blocker |

Line ranges printed in stage descriptions are scaffold routing hints. Each content stage must use the immutable segment ID and current boundaries emitted by Stage 2/5, and fail if the hint and structure ledger diverge.

## Stages

### 1-GUARDRAILS

#### Big Picture Objective

Freeze the fidelity contract, output architecture, evidence hierarchy, scope, and conditions under which “fully repaired” may honestly be claimed.

#### Detailed Implementation Plan

- Audit recursive path consumers and confirm the sibling `ref/A-New-Kind-of-Science-Repaired/` root.
- Freeze all 29 canonical filenames/order, output roles, separate faithful/derived/editorial/search targets, and refusal rules for a nonempty unowned release folder.
- Finalize the Markdown dialect needed by the Stage 4 serializer, repair/workflow classes, severity definitions, reviewer-independence rules, class-conditional evidence, witness/build modes, licensing limits, and release blockers.
- Freeze the held-out quality-evaluation sampling rule, manifest-derived seed, minimum per-document/risk quotas, blind adjudication protocol, and class-specific thresholds before repair results exist.
- Choose portable byte-identical legacy-asset copying plus a governed path for lawful witness-supplied replacement/full-plate assets.
- Snapshot commands and output digests for every affected Goal 1 recursive source/asset oracle.
- Document what requires separate authorization: legacy promotion, deletion, relocation, and consumer migration.

#### Completion Requirements

- The architecture has one unambiguous source of build input and one repaired release location.
- All 29 canonical paths/roles and every generated/sidecar role are frozen.
- Baseline affected-oracle outputs are captured, and an empty sibling release leaves them behaviorally unchanged.
- Evidence and waiver rules forbid unsupported OCR correction.
- The serialization dialect, severity scale, sample plan, independent-review rules, and build/audit modes are testable.
- Scope, rollback, promotion, and licensing rules are explicit and testable.
- Stage 2 can inventory inputs without making content changes.

### 2-BASELINE

#### Big Picture Objective

Create an independent, immutable census of the current corpus and all known structural/OCR risks.

#### Detailed Implementation Plan

- Hash the explicit allowlist of 19 Markdown/1,444 image inputs—never a future recursive root—and record logical/allocated bytes, lines, encoding, dimensions, basenames, Git blob identity, and role.
- Re-derive the monolith hash/line map and all 29 raw segment boundaries using exact heading/start/end signatures; emit immutable segment IDs.
- Inventory all 17 split routing derivatives, Atlas, the three omitted reference ordinals, broken monolith links, path consumers, and known defect candidates.
- Freeze `known-defect-regression.jsonl` with every exact sentinel and expected route.
- Materialize the predeclared held-out sample IDs from the raw-block universe without exposing repaired answers.
- Establish raw block IDs and a baseline detector report without applying fixes.
- Record current tool/environment versions and clean/dirty worktree scope.

#### Completion Requirements

- The manifest accounts for 19 Markdown files and 1,444 JPEGs or explains any resynced count.
- Raw hashes and segment arithmetic are independently reproducible.
- All 22,498 logical lines belong to one proposed segment exactly once.
- Every known split/image anomaly has a baseline record.
- Every known defect sentinel and held-out sample ID is frozen before correction.
- The raw manifest explicitly excludes the sibling repaired tree.
- Mutation of any raw input causes the baseline verifier to fail.

### 3-WITNESSES

#### Big Picture Objective

Secure and validate authoritative, edition-identical page-level evidence sufficient for a full OCR/layout repair.

#### Detailed Implementation Plan

- Locate official/licensed page images, PDF, print-assisted captures, or equivalent authoritative evidence.
- Fingerprint the edition and derive the complete leaf/page/plate universe from the witness, including covers, blanks, figure-only material, publication matter, and Index pages; detect missing/duplicate units and reconcile the result to the Colophon's 1,280-page clue under an explicit counting definition.
- Partition pages into nonoverlapping authorial regions and record per-region legibility for prose/punctuation, formulas/code/data, figures/captions/color, and Index columns.
- Record source URL/location, access date, permissions, file/page hashes, and immutable local review method.
- Independently transcribe/adjudicate the pre-frozen held-out sample from the witness before reviewers see proposed repairs.
- Pursue alternate authoritative sources for missing/illegible pages; never fill gaps with inference.

#### Completion Requirements

- Every witness-derived physical leaf/page/plate has a pinned mapping and each region has a legibility or independently reviewed enumerated non-authorial `NOT_APPLICABLE` reason; every illegible/untranscribed authorial region becomes a downstream/release blocker.
- Formula/code/data symbols, figure components/captions, and Index columns are legible in the relevant witness.
- Witness provenance and permitted storage/use are documented.
- Tampered or missing witness pages fail verification.
- If full coverage cannot be obtained, the manifest remains total, affected batches become `SOURCE_BLOCKED`, and dependency-independent Stages 4–7 or fully witnessed batches may proceed; Stage 42 cannot claim a full repair.

### 4-PIPELINE

#### Big Picture Objective

Build the reversible overlay pipeline, ledgers, validators, and mutation suite before changing any author text.

#### Detailed Implementation Plan

- Define machine-readable schemas for raw and witness regions, structure, bidirectional provenance, repair workflow/final disposition, unresolved, technical, figure, navigation, review, compatibility, and release ledgers.
- Implement replace/delete/move/split/merge and two-sided anchored insertion operations, exact guards, dependency ordering, target-specific overlays, forward build, inverse replay, and atomic output publication.
- Implement the Stage 1 Markdown dialect and reject errata/search/editorial overlay classes from `CANONICAL_AUTHOR_TEXT`.
- Build a zero-repair output and prove author-text conservation.
- Add independent validators for two-way raw+witness coverage, joins, hashes, drift, workflow/final dispositions, role counts, reviewer independence/disagreement, and generated/sidecar separation.
- Add mutations for missing/reordered blocks, unlogged edits, source/evidence drift, symbol changes, fences, assets, captions, and anchors.

#### Completion Requirements

- A zero-repair build is deterministic and inverse-recoverable.
- The pipeline refuses stale preimages, wrong occurrence counts, missing evidence, unresolved dependencies, and raw drift.
- Anchored insertions require unique adjacent anchors and witness-region evidence; inverse replay removes them exactly.
- Canonical, derived aggregate, editorial, and search targets cannot leak into one another.
- Validators run from root and a relocated offline copy and fail closed under declared modes.
- Every required mutation produces a specific failure.
- No repair record has yet altered author text.

### 5-STRUCTURE

#### Big Picture Objective

Create the correctly partitioned 29-document repaired skeleton while preserving raw author text exactly.

#### Detailed Implementation Plan

- Extract the two front-matter, 12 chapter, 13 Notes, Index, and Colophon segments by Stage 2 IDs/signatures rather than copied line literals.
- Correct ownership boundaries, including the Chapter 12/General Notes transition and malformed nominal back matter.
- Establish exact canonical paths/roles, heading/document identities, stable anchors, raw-span provenance, and deterministic assembly order using the Stage 1 dialect.
- Compare existing split files and classify every difference without adopting unsupported content changes.
- Generate the 29 canonical documents plus a separately typed aggregate monolith through the zero-content-repair pipeline.

#### Completion Requirements

- Exactly 29 `CANONICAL_AUTHOR_TEXT` documents cover the monolith author-text sequence once; the aggregate is excluded from canonical counts.
- Chapter 12, all Notes, Index, and Colophon begin/end at verified boundaries.
- Every segment has source-backed start/end signatures, not only range arithmetic.
- Reassembly differs from raw only by declared structural wrappers/path placeholders/final-newline policy.
- Inverse replay recovers raw block bytes and order.
- Existing split differences all have structural/routing dispositions.

### 6-MEDIA

#### Big Picture Objective

Make all image assets portable, resolvable, byte-preserved, and correctly owned without inferring unsupported figure semantics.

#### Detailed Implementation Plan

- Build the 1,444-row legacy asset manifest with distinct asset ID, basename, current path, bytes, dimensions, hash, raw reference ordinal, and proposed repaired owner.
- Materialize portable manifest-governed byte-identical copies in the sibling release and implement deterministic canonical/aggregate link rewriting.
- Restore the three omitted Chapter 2/4 references by exact raw reference ordinal.
- Detect duplicates, orphans, missing/cropped assets, same-page groups, and caption-association candidates.
- Mutation-test missing assets, hash drift, swapped same-page images, wrong links, and silent recompression.

#### Completion Requirements

- All 1,444 governed assets retain their exact bytes/hashes.
- The zero-repair canonical documents have 1,444 resolving references in raw global order, with ownership totals Preface 2, chapters 820, Notes 622, and zero elsewhere; the derived aggregate separately mirrors them.
- No Notes-owned reference is assigned to Chapter 12 merely because its physical legacy asset currently lives there.
- There are zero missing, orphaned, duplicate-ID, or ambiguous basename rows; identical byte hashes do not collapse distinct IDs.
- The three known omissions are restored at source-verified positions.
- Figure grouping/caption uncertainty remains typed for Stage 38 rather than guessed.

### 7-STYLE

#### Big Picture Objective

Validate and freeze the Stage 1/4 Markdown dialect against real corpus fixtures before author-text batches begin.

#### Detailed Implementation Plan

- Validate heading hierarchy, paragraphs, lists, blockquotes, code fences, math delimiters, HTML, images, captions, tables, page markers, and editorial annotations against representative corpus fixtures.
- Separate mechanically safe formatting from witness-dependent text/symbol changes.
- Create fixtures for prose reflow, legitimate/source hyphens, page furniture, nested math, Wolfram code, figure groups, and Index structures.
- Select/finalize parser/render tools and expected AST/render invariants.
- Define guarded formatting rules with exact contexts, counts, inverses, and false-positive tests.
- If the dialect changes, reopen and rebuild Stages 4–6 before any content batch starts.

#### Completion Requirements

- `style-guide.md` fully defines the canonical dialect and author/editorial boundary.
- All representative fixtures parse and render as intended.
- No style rule can alter formula/code/data tokens without high-risk evidence review.
- Automated formatting is deterministic, reversible, and mutation-tested.
- The Stage 4–6 zero-repair build conforms to the frozen style; no later style drift is accepted silently.
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
- Every candidate is closed or routed to an explicit specialist/reviewer queue; all source-needed authorial items remain release blockers.
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

- Every Chapter 1 raw block and assigned nonoverlapping witness region is reviewed at least once by every required role.
- Every candidate is closed or routed to an explicit specialist/reviewer queue; any unresolved source-needed authorial item remains a release blocker.
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
- Reconcile the operational complete-Notes count across General Notes and Chapters 1–12 with the Colophon's 1,350-note clue.
- Rebuild and review the complete Notes document.

#### Completion Requirements

- Every Chapter 12 Notes block/page is reviewed and dispositioned.
- Technical changes have authoritative token evidence and independent review.
- The document ends exactly before the actual Index.
- The operational Notes count and any difference from 1,350 are reproducibly explained.
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
- Independently review every changed technical token and the pre-frozen technical holdout.
- Define an operational program-count rule and reconcile it with the Colophon's 796 Mathematica-program clue without forcing equality.

#### Completion Requirements

- Every technical span has a witness, transcription status, parse/render status, and review disposition.
- Zero unreviewed delimiter, fence, formula, code, rule-table, or semantic-data candidate remains.
- Every technical edit is token-evidenced, reversible, and independently reviewed.
- The operational program count and any difference from 796 are reproducibly explained.
- Mutation of one operator, sign, digit, subscript, superscript, brace, or fence fails verification.

### 38-FIGURES

#### Big Picture Objective

Verify every printed figure/caption group, all 1,444 extracted assets, and their repaired placement/accessibility metadata.

#### Detailed Implementation Plan

- Build an independent witness-page census of every printed illustration/group/component, rather than assuming the 1,444 extracted files are complete.
- Visually compare page witness, caption text, repaired page context, and component images for every printed figure group.
- Confirm image order, crop completeness, scaling/rotation assumptions, caption ownership, and multi-image grouping.
- Identify missing/full-plate limitations separately from available caption crops.
- Add generated alt text only as typed editorial metadata with review status.
- Review same-page swaps and proximity-based associations adversarially.

#### Completion Requirements

- Every legacy asset and every witness-visible printed figure/group/component has page/context evidence and final association/completeness status.
- All 1,444 legacy asset IDs/bytes/hashes remain correct; the Stage 6 baseline references remain reproducible, while the final canonical reference set is separately manifest-defined and source-verified.
- Caption text is faithful author text; generated alt text is visibly separate.
- The operational printed-illustration count is reconciled with the Colophon's 973 figure clue and any difference is explained.
- Zero missing/cropped authorial visual component remains in an unqualified full release; a licensing/source gap blocks full visual completion rather than becoming a footnote.
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

- Re-run candidate detectors for blank/furniture headings, numeric-only lines, joined/split words, hyphens, OCR confusions, caption/prose or column interleaving, semantic block misclassification, long Index lines, delimiters, brackets, fences, orphan continuations, and malformed links.
- Add new detector rounds from defects found during manual review and rerun them over all 29 documents.
- Give every hit a confirmed/rejected/duplicate/unresolved disposition with exact scope.
- Evaluate the pre-frozen, manifest-seeded held-out sample: at least 5% of eligible blocks with a minimum 20 per canonical document (or all blocks for smaller documents), stratified by changed/unchanged and risk class, independently transcribed/adjudicated from the witness before comparison.
- Measure exact author-text character projection/CER/WER, heading/paragraph/list boundary exactness, technical token exactness, Index entry/column sequence exactness, and figure/caption association exactness against thresholds frozen in Stage 1.
- Measure detector recall against `known-defect-regression.jsonl` and seeded defect mutations.
- After every newly discovered defect class, rerun the full manual+detector protocol until two consecutive complete rounds produce no new class and every queue is empty.

#### Completion Requirements

- Two consecutive full rounds after the last new class produce no new defect class and zero open queue.
- Every detector hit and every known regression sentinel has a final route/disposition; detector mutations prove recall for governed classes.
- The held-out methodology, seed, quotas, blind adjudication, projections, and results are reproducible; exact class-specific full-release thresholds pass without post-hoc severity changes.
- All ledgers join totally and every raw/output/evidence block is accounted for.
- Any remaining source limitation is explicit and blocks an overbroad completeness claim.

### 41-HOSTILE

#### Big Picture Objective

Independently attempt to falsify the repaired edition's fidelity, completeness, reversibility, and reproducibility.

#### Detailed Implementation Plan

- Review every high-risk repair plus the pre-frozen changed/unchanged samples across all 29 documents, enforcing creator/reviewer separation and disagreement closure.
- Attack boundary ownership, two-way raw+witness conservation, insertion anchors, output-role leakage, witness identity, repair inverses, formula/code tokens, Index columns, figures/captions, links, and compatibility routes.
- Run the full mutation suite and add mutations for every newly discovered validator weakness.
- Compare rendered raw/witness/repaired triptychs and investigate every unexpected difference.
- Reopen prior stages and record closure for all hostile findings.

#### Completion Requirements

- Every hostile finding is fixed, disproved with evidence, or remains an explicit release blocker.
- All required mutations fail for the intended reason.
- Independent review coverage and reviewer type are truthfully recorded.
- A fresh hostile rerun finds no unclosed authorial discrepancy of any severity.
- Legacy raw scope remains untouched.

### 42-RELEASE

#### Big Picture Objective

Publish a deterministic, source-faithful repaired edition with complete provenance, rollback, limitations, and compatibility documentation.

#### Detailed Implementation Plan

- Build twice from frozen raw inputs and repair overlays in fresh offline/relocated environments.
- Run audit mode against the authorized witness mount and prove the complete page/region evidence joins; build-mode reproducibility alone is insufficient for fidelity certification.
- Compare output bytes, manifests, ledgers, navigation, rendered artifacts, and tool versions.
- Run all structural, content, asset, review, mutation, whitespace, and Git-scope checks.
- Re-run every affected Goal 1 oracle and compare its output digest with the pre-release compatibility baseline.
- Publish from a fresh validated staging tree to `ref/A-New-Kind-of-Science-Repaired/` only if the target is empty or manifest-owned; retain prior release manifests/snapshots under `goal-4/releases/` and never overwrite unowned work.
- Document exact rollback/rebuild/previous-release-selection commands, remaining optional editorial work, and future legacy-promotion/migration work.

#### Completion Requirements

- Two clean builds are byte-identical and inverse replay recovers the frozen raw text/block hashes.
- All 29 canonical documents, derived aggregate, 1,444 legacy assets/baseline references, final printed-figure component inventory, ledgers, links, anchors, two-way evidence joins, and review gates pass with role-specific counts.
- No `UNRESOLVED_SOURCE_NEEDED` item affecting an authorial layer remains in a release called fully repaired.
- All known defect sentinels are found and source-backed; Colophon illustration/Notes/program/Index counts are operationally reconciled.
- Legacy raw hashes/paths, affected Goal 1 oracle behavior, and all unrelated repository files remain unchanged.
- The final report clearly distinguishes repaired transcription, source errata, generated metadata, search normalization, and any residual limits.
- Completion reflects the original full-repair objective rather than a structurally cleaner but unverified subset.
