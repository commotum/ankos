# Goal 5: Reliable ANKoS Markdown Source

Shorthand: `BOOK-SOURCE`

## Big-Picture Objective

Create a reliable Markdown source of the complete *A New Kind of Science* book
with the OCR errors corrected.

The result must preserve the book's actual text and organization across front
matter, all 12 chapters, General Notes, all 12 chapter Notes sections, formulas,
Wolfram Language code, tables, captions, figures, Index, and Colophon. It must
also be easy to navigate and reproducibly build from preserved inputs.

Goal 5 keeps the fidelity objective that motivated Goal 4 while discarding the
process machinery that does not help correct or verify the book. The first
stage cleans up Goal 4's unnecessary schemas, locks, authority models, race
defenses, generated ledgers, tests, caches, and unfinished pipeline work. It
retains or migrates only source facts and tools that directly reduce the work
of producing and checking the corrected book.

Completion is not “best effort with disclosed OCR errors.” Completion means the
entire corpus has been reviewed against an authoritative source, all discovered
OCR errors have been corrected, all review coverage is accounted for, and no
known transcription ambiguity remains open. Literal errors present in the book
itself are preserved as source text rather than silently corrected.

## What “Reliable” Means

The repaired corpus is reliable when:

- every part of the book has received a sequential source comparison rather
  than only detector-driven spot checking;
- corrections are grounded in an authoritative edition-identical source, not
  language-model plausibility or agreement between correlated OCR derivatives;
- prose, punctuation, capitalization, spacing, headings, lists, formulas, code,
  rule tables, captions, Index entries, and reading order are all in scope;
- high-risk technical and multi-column material receives a dedicated second
  pass;
- automated searches are used to find residual defects but never treated as a
  substitute for reading;
- a separate verification pass confirms the corrected corpus and closes or
  reopens every discrepancy;
- the final Markdown builds deterministically, links and images resolve, and the
  legacy corpus remains byte-for-byte unchanged.

This is source-fidelity work, but it does not require a forensic publication
system. Reliability comes from complete comparison, careful correction, a
simple coverage record, focused review, and reproducible output—not from a
large schema graph or hostile-filesystem security model.

## In Scope

- Clean up Goal 4 artifacts that do not directly support book correction.
- Preserve the legacy corpus as immutable raw evidence.
- Establish a lawful, readable, edition-identical authoritative source for the
  complete book.
- Produce 29 correctly owned canonical Markdown documents: publication and
  contents, Preface, 12 chapters, General Notes, 12 chapter Notes documents,
  Index, and Colophon.
- Correct all OCR transcription errors found through complete sequential
  comparison and follow-up detector passes.
- Correct document boundaries, paragraph/list/heading structure, reading order,
  Markdown fences, formulas, code, captions, and Index column flattening where
  the authoritative source establishes the answer.
- Account for and correctly place every legacy image; add a missing visual only
  when a lawful authoritative source establishes that it belongs in the book
  and permits the chosen handling.
- Add generated contents and navigation without presenting editorial material
  as author text.
- Build and validate the repaired sibling corpus reproducibly.

## Out of Scope

- Correcting factual, mathematical, historical, or typographical errors that
  are actually present in the authoritative book. Those may be noted in a
  separate errata file, but the canonical transcription preserves them.
- Creating a generalized document compiler, workflow engine, evidence database,
  reviewer-identity system, or security boundary.
- A census of covers, endpapers, blank leaves, trim, bleed, file inodes, or
  other publication/security details that do not affect the Markdown book.
- Adversarial caller authorization, forged-ledger defense, atomic no-replace
  race handling, implementation proof locks, or large mutation matrices.
- Migrating Goal 1/3 consumers or replacing the immutable legacy corpus.
- Claiming human review when work was performed by an agent.

## Non-Negotiable Constraints

1. **Preserve the legacy corpus.** Do not modify, rename, delete, or reformat
   `ref/A-New-Kind-of-Science/**`.
2. **Protect unrelated work.** Inspect `git status` and diffs before cleanup or
   bulk changes. Goal 4 files may be changing concurrently; never assume an old
   inventory is current.
3. **Clean up by utility.** Retain a Goal 4 artifact only if it is directly used
   to locate, correct, build, or verify book content and is simpler to retain
   than to replace. Git history is sufficient archival storage for discarded
   process machinery.
4. **Use an authoritative source.** A transcription-changing decision must be
   checked against a lawful, edition-identical book source. The monolith, split
   files, and extracted JPEGs are correlated or incomplete OCR evidence and
   cannot alone prove corrected wording.
5. **Respect source permissions.** Do not scrape, bulk-download, commit, or send
   copyrighted source material to tools when the applicable license or user
   authorization does not permit it. A user-provided or mounted source must
   have a clear allowed-use boundary.
6. **Do not guess.** Plausibility, spell-checking, parsers, execution, rendering,
   and model consensus may identify candidates but cannot authorize a change.
7. **Preserve authorial errors.** Distinguish OCR error from an error printed in
   the book. Canonical Markdown transcribes the latter faithfully.
8. **Review everything.** Every canonical source span and every authoritative
   source region containing book content must belong to a completed review
   batch. Detectors and samples do not replace this coverage requirement.
9. **Use simple records.** Keep a compact correction log and coverage checklist.
   Do not recreate Goal 4's per-block authority, workflow, provenance, lock, or
   review schema system.
10. **Build from preserved inputs.** Never use a previous repaired tree as the
    source for the next build.
11. **Keep editorial additions separate.** Generated anchors, page markers,
    navigation, alternative text, and errata must not masquerade as book text.
12. **Do not release with known ambiguity.** An unreadable or unavailable
    authorial source region is a real blocker to the “without OCR errors” goal;
    obtain better evidence or continue the review rather than weakening the
    objective.

## Current Facts

These facts have been rechecked against the live worktree, immutable corpus,
and pinned fixed-layout source unless explicitly described as a review risk.

- The legacy corpus contains 19 Markdown files and 1,444 JPEGs.
- The monolith is 3,780,628 bytes and 22,498 logical lines.
- The monolith references 1,444 images; the split Markdown omits three image
  references.
- Chapter 12 runs into General Notes, and nominal Notes, Index, and Colophon
  files contain displaced Notes and actual back matter.
- The Index is flattened from multiple columns and requires layout-aware source
  comparison.
- Known defects include broken headings, word joins/splits, prose inside code
  fences, malformed formulas, damaged Wolfram Language, caption interleaving,
  OCR substitutions, and back-matter reading-order errors.
- Stage 1 removed Goal 4's generated planning, schema, lock, pipeline,
  validation, and test machinery after migrating four compact fact sets. Goal
  4 had not corrected the book text.
- The sibling `ref/A-New-Kind-of-Science-Repaired/` is reproducibly generated
  from the immutable monolith plus guarded corrections. It remains a partial
  repair worktree rather than a verified complete edition.
- A complete local First-edition, First-printing PDF is pinned as the
  user-authorized fixed-layout witness for local agent-assisted comparison and
  repaired workspace output. It is Git-ignored and is not authorized here for
  redistribution.

## Assumptions To Challenge

- The pinned edition-identical source remains readable at every location needed
  for the full comparison; any unreadable region must be carried as a blocker.
- The raw monolith contains all author text even where its transcription or
  layout is damaged.
- The proposed 29-document organization accounts for all book content.
- Existing JPEGs cover all printed figures and are associated with the correct
  captions.
- A CommonMark-oriented representation can preserve the relevant structure of
  formulas, code, tables, captions, and Index entries.
- Fixed-layout margin figures require an explicit one-dimensional
  serialization: place each image and caption after the earliest complete
  paragraph that explicitly refers to it (or, when there is no reference,
  after the closest complete paragraph beside it), without splitting printed
  prose. This is a documented canonical Markdown choice, not a claim that the
  two-dimensional page has one uniquely implied linear order.
- When one or more full-page plates interrupt a prose paragraph in the raw
  extraction, join the complete printed paragraph first, then serialize the
  ordered plate group immediately after it. Preserve the source order and keep
  each lead caption, continuation marker, image subgroup, and back caption with
  the plate sequence it governs. This is likewise an explicit canonical
  one-dimensional choice rather than an alteration of printed prose.
- Four-chapter review batches are small enough to review carefully without
  losing continuity or skipping content.
- A fresh second review plus targeted detectors can reach zero open OCR
  discrepancies without requiring Goal 4's formal machinery.

## Minimal Working Architecture

The exact shape is frozen in Stage 2, but the intended system is small:

```text
goal-5/
├── 0-plan.md
├── 0-loop.md
├── 0-prompt.md
├── build.py
├── validate.py
├── corrections.jsonl
├── added-assets.jsonl
├── coverage.csv
├── unresolved.md
└── tests/

ref/A-New-Kind-of-Science-Repaired/
├── README.md
├── Contents.md
├── FRONT-MATTER/
├── CHAPTERS/
└── BACK-MATTER/
    ├── NOTES/
    ├── Index.md
    └── Colophon.md
```

`corrections.jsonl` records actual author-text changes with an absolute raw
byte offset, exact before/after text, source page/location, reason, and reviewer
status.
`added-assets.jsonl` pins the small number of authoritative visuals absent from
the immutable legacy extraction by owner, source location, hash, and decoded
dimensions; zero-correction builds deliberately exclude them.
`coverage.csv` records sequential review ranges and second-pass completion.
Neither file is a generalized workflow database.

## Success Metrics

- Unnecessary Goal 4 machinery is removed without harming useful source facts,
  the legacy corpus, or unrelated work.
- A lawful edition-identical source covers the complete book text, technical
  material, figures/captions, Index, and Colophon at readable quality.
- Exactly 29 canonical author-text Markdown documents contain the complete book
  in correct order and ownership.
- Every canonical span is included in a sequential authoritative-source review
  batch, and every batch is complete.
- Every authoritative book-content region maps to the corrected Markdown; no
  paragraph, heading, formula, code block, caption, table, Index entry, or
  Colophon text is silently omitted.
- Every applied transcription change has an exact preimage, source location,
  rationale, and completed verification state.
- Every high-risk formula, Wolfram Language block, rule table, caption, and
  reconstructed Index region receives a dedicated second comparison.
- All 1,444 legacy assets are accounted for, all repaired image references
  resolve, and figure/caption placement agrees with the authoritative source.
- Residual OCR detectors have no unexplained hits, and repeated full review
  rounds produce no new discrepancies.
- Zero known or unresolved transcription ambiguity remains at release.
- The repaired Markdown parses/renders as intended, navigation resolves, and
  two clean builds are byte-identical.
- The complete legacy tree and existing Goal 1/3 consumers remain unchanged.

## Verification Requirements

- Hash the legacy corpus before cleanup and after release.
- Inspect all modified/untracked Goal 4 content before deletion and record the
  keep/delete/migrate decision.
- Verify authoritative source identity, completeness, legibility, and allowed
  use without constructing a physical-book forensics system.
- Partition both raw and authoritative book content into simple, ordered review
  ranges and prove no range is skipped or duplicated.
- Build a zero-correction 29-document projection first and prove raw-content
  conservation before applying corrections.
- Guard every correction by exact preimage and expected occurrence count.
- For every content batch, perform a complete forward source comparison, run
  focused detectors, render changed material, and perform a separate second
  pass before closing it.
- Compare technical material character/token by character/token where ordinary
  prose review is insufficient.
- Compare the Index in printed column/entry order against fixed-layout evidence.
- Verify image order, file identity, caption association, and link resolution.
- Run corpus-wide searches for common OCR confusions, broken words,
  punctuation/Unicode anomalies, malformed Markdown/math/code, and suspicious
  vocabulary; disposition every hit.
- Repeat the final review/detector pass after the last correction until a full
  pass finds no new discrepancy.
- Build twice in fresh directories, compare outputs, run focused tests and
  affected repository tests, and run `git diff --check` plus scope inspection.

## Current Execution State

- Synced: 2026-07-18 (America/Los_Angeles).
- Active stage: `8-NOTES-09-12` (`IN_PROGRESS`), activated after clean Stage 7
  closure through `N08`.
- Stage 1 is complete. All 78 tracked Goal 4 files, 45 ignored bytecode caches,
  and the empty `goal-4/` directory were removed by exact path. No commit
  range was reverted, and Goal 4 had corrected no book text.
- The legacy tree currently contains exactly 1,463 files: 19 Markdown and 1,444
  JPEG. A sorted path-and-file-digest snapshot hashes to
  `b9ff7b9b507790f1d519593baf2b2d2f24dd6cd49dc0fe10f0ac629278ea42f4`.
- The monolith remains 3,780,628 bytes with SHA-256
  `55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20`.
- `ref/A-New-Kind-of-Science-Repaired/` contains 29 generated author-text
  documents, 1,444 mapped image positions, 148 source-added images, and
  generated README/Contents files. The current manifests include 3,575 guarded
  source-verified corrections but is not a complete OCR-corrected edition.
- A repository-wide scan found no code, test, or document outside Goal 4 that
  consumes a specific Goal 4 artifact, module, schema, or contract. Goal 5 has
  intentional historical cleanup references to Goal 4 and intentional repaired
  sibling references, but no dependency on its machinery.
- Goal 5 contains four compact working datasets: 29 source-confirmed raw/PDF
  ranges, 57 known-defect/guardrail candidates, a 1,444-row image-to-asset map,
  and a concise legacy/routing/source summary. Content claims remain pending
  until their sequential comparison passes.
- `known-defects.jsonl` is a routing/intake inventory, not the live owner-pass
  disposition ledger. Its per-row status records the state in which a candidate
  entered Goal 5; current repair and closure evidence lives in
  `corrections.jsonl`, `coverage.csv`, focused tests, and stage results.
- The pinned source is `A New Kind of Science/A New Kind of Science.pdf`, a
  complete, readable 1,280-page First-edition, First-printing fixed-layout
  witness whose copyright-page identity matches the immutable monolith. Its
  SHA-256 is
  `a3cc5dd60e12d6b563aee86ea31a15b03f9cddfd4869b8f965d3a11bbc61a0d6`.
- Stage 2 is complete. The zero-correction build conserves all monolith bytes;
  two fresh builds match; the focused validator protects the legacy snapshot,
  exact source identity, 29 raw/PDF partitions, correction evidence, and image
  ownership; `10` tests plus `26` mutation subtests pass.
- Source comparison corrected twelve chapter-start raw boundaries and eight
  opener-image owners. All 1,444 image filenames now place their source page
  inside their owning canonical document. `FOUNDATION-SOURCE-001` is closed.
- `PUBLICATION_AND_CONTENTS` is complete after two sequential agent passes over
  PDF pages 1–8 and a clean closing pass against the rebuilt Markdown. Its 20
  guarded corrections are `G5-C-0001`–`G5-C-0020`; focused render and tests
  pass.
- `PREFACE` is complete after a sequential first pass over PDF pages 9–16 and
  an independent clean second pass against the rebuilt Markdown. Its 59 guarded
  corrections are `G5-C-0021`–`G5-C-0079`; exact text/emphasis comparison,
  detector scans, rendering, deterministic builds, and focused tests pass.
- `CH01` is complete after a sequential first pass over PDF pages 17–38 and an
  independent clean second pass against the final rebuilt Markdown and assets.
  Its 27 guarded corrections are `G5-C-0080`–`G5-C-0106`; the exact prose-token
  sequence, punctuation, hierarchy, emphasis, paragraph joins, three figures,
  captions, and source-faithful repaired-only opener were rechecked.
- `CH02` is complete after a forward first pass, pre-closure residual review,
  and independent clean second pass over PDF pages 39–66. Its 26 guarded
  corrections are
  `G5-C-0107`–`G5-C-0132`; all 19 inherited figures/captions
  were checked, three source-backed missing visuals were restored, and two
  full-page plate sequences plus the rule-90 figure group were canonically
  serialized after complete prose paragraphs. The final source/candidate
  sequence matched at 6,685 tokens with no punctuation, technical, visual, or
  caption discrepancy.
- `CH03` is complete after a forward first pass and an independent clean second
  pass over all 64 PDF pages 67–130, including the intentional blank final
  page. Its 61 guarded corrections are `G5-C-0133`–`G5-C-0193`; all 248 final
  live-text blocks and 87 final images were independently verified, one omitted
  rules plate was restored, and three damaged/raster-text images use pinned
  repaired-only overrides. Focused tests, residual detectors, rendering,
  deterministic builds, and legacy checks pass. The final Markdown SHA-256 is
  `f948d0c45b8bec06b78e72e8e8fa8f807c37f7a0fd29d4b4dc43550bc8768f35`.
- `CH04` is complete after a forward first pass and a clean independent pass
  restarted against the post-`G5-C-0303` final document. Its 110 guarded
  corrections are `G5-C-0194`–`G5-C-0303`; all 243 live blocks, 172 TeX spans,
  11 reconstructed tables, and 63 assets were independently verified over all
  54 PDF pages 131–184. The final Markdown SHA-256 is
  `33b0521073b7d212d181903a71b1917b7647b006ef09618f93d89697f8942248`.
- `CH05` is complete after a forward first pass and an independent clean second
  pass over all 54 PDF pages 185–238, including the intentional blank final
  page. Its 52 guarded corrections are `G5-C-0304`–`G5-C-0355`; all 80 final
  image references were independently verified, including 11 repaired-only
  overrides and three restored source visuals. Focused detectors, rendering,
  two fresh deterministic builds, strict zero-correction validation, the
  cumulative 55-test Goal 5 suite, the complete 157-test repository suite,
  and legacy checks pass. The final Markdown SHA-256 is
  `79705293cb790968285d12f4d46f1f96337a0cff7f8eaeb87b142adc5bf751c1`.
- `CH06` is complete after a forward first pass and three independent clean
  closing audits over all 74 PDF pages 239–312. Its 44 guarded corrections are
  `G5-C-0356`–`G5-C-0399`; all author text and structure, 29 inline math
  spans, 105 accounting references, 99 mapped assets, six additions, seven
  repaired-only overrides, and the complete 85-page render were rechecked.
  Focused detectors, strict zero-correction validation, two fresh deterministic
  builds, the cumulative 62-test Goal 5 suite, the complete 164-test repository
  suite with 135 subtests, and legacy checks pass. The final Markdown SHA-256
  is `0eb4ebc5400c3e3ed39fb2dd8fd9c38a2977eaef1ffefb528fd4c2708a42dca5`.
- `CH07` is complete at `YES/YES` after a forward pass and fresh independent
  source, technical, and visual closing passes over all 66 PDF pages 313–378
  and all 92 accounting references. Its 53 guarded corrections are
  `G5-C-0400`–`G5-C-0452`; 12 source-backed mapped overrides repair incomplete
  or contaminated figures, and no source-added asset was required. The final
  closing visual traversal caught and repaired two truncated class-1 rule
  strips before restarting cleanly. All three final ledgers close with zero
  discrepancy or ambiguity. Default and zero-correction validation both pass
  with nine closed second-pass documents; two fresh normal builds are
  byte-identical, and the complete 171-test repository suite plus 171 subtests
  passes. The final Markdown SHA-256 is
  `e052f275ea7519f2e8c270f1dd68eac01d123aa3b73355eff5803f02708e542d`.
- `CH08` is complete at `YES/YES` after independent source, technical, and
  visual first passes, integration, and fresh independent source, technical,
  and visual closing passes over all 70 PDF pages 379–448. Its 47 guarded
  corrections are `G5-C-0453`–`G5-C-0499`; nine mapped overrides repair
  ordinals 444, 446–450, 452, 453, and 468, and additions `G5-A-0018` and
  `G5-A-0019` restore two omitted flow panels. All three final ledgers close
  with zero discrepancy or ambiguity across the final 770-line Markdown and
  all 45 live references. The focused six-test CH08 suite, 75-test Goal 5
  suite, complete 177-test repository suite, rendering, default and strict
  zero-correction validation, two fresh deterministic builds, legacy digest,
  and scope gates pass. The final Markdown SHA-256 is
  `5e794cedc877e539e30d9ef6102fea18f4533c56d3324f7d454326336e4a2004`.
- Stage 5 is complete over `CH09`–`CH12`: PDF pages 449–864, printed pages
  433–848, raw lines 5,164–10,622, bytes `[728322,1540232)`, and mapped
  ordinals 480–822. `CH09` is complete at `YES/YES` after forward first and
  fresh source, technical, and visual final-output passes over all 114 PDF
  pages 449–562. Its 77 guarded corrections are `G5-C-0500`–`G5-C-0576`;
  all 113 final JPEG references and the live rule-94 swatch close with zero
  discrepancy or ambiguity. One mapped override and additions `G5-A-0020`–
  `G5-A-0022` repair the PDF-493 and PDF-527 omissions. The final Markdown
  SHA-256 is
  `c4786895ea852253233767f683f69ffce0f6e5576e948e4bbe3bf33c26cbc66c`.
  `CH10` is complete at `YES/YES` after forward first passes and fresh
  independent source, technical, and visual final-output passes over all 90 PDF
  pages 563–652, including the blank closing leaf. Its 90 guarded corrections
  are `G5-C-0577`–`G5-C-0666`; five mapped overrides repair ordinals 610, 613,
  641, 651, and 652, while additions `G5-A-0023`–`G5-A-0033` restore eleven
  omitted source visuals. All three final ledgers close with zero discrepancy
  or ambiguity across 1,014 Markdown lines and all 78 final references. The
  final Markdown is 164,487 bytes with SHA-256
  `82217582690509ef97acd14ca12f0f9680e380ce6a1d8f8a0373e569114b2bc3`.
  Focused and cumulative tests, complete rendering, default and strict
  zero-correction validation, two fresh byte-identical builds, legacy digest,
  and scope gates pass. `CH11` is complete at `YES/YES` after forward first
  passes and wholly fresh independent source, technical, and visual
  final-output passes over all 78 PDF pages 653–730. Its 64 guarded corrections
  are `G5-C-0667`–`G5-C-0730`; 107 mapped references plus `G5-A-0034`
  produce 108 final references, with 14 mapped references using repaired-only
  overrides. The final 103,952-byte, 874-line Markdown hashes to
  `94e20302298935e73ad11c300d267d05ab23682bf14978e67fe0c3b09ef7080c`.
  Source, technical, and visual closing reports hash respectively to
  `47632497b0d234b3f4fecef81fe61398e66017d6304df9a13127fc5b33728b2a`,
  `5acbfc73fb485ac1faf4b2e347555d1a6340c4f94a8265deb6529bc5bd8e5b96`,
  and `3f8b746226b218af9cbfde2e5bfe68e73b76df3ff3e5845e89f5dc5b73d93095`;
  each closes with zero discrepancy and zero ambiguity. The 85-page render
  hashes to
  `b97e7ab8ce4fbca72866e09e54bb579255e3b23f2dbee1837be0e4aebad47937`.
  Nine focused tests, the 98-test Goal 5 suite, and the complete 200-test
  repository suite with 450 subtests pass. Two fresh normal builds and the
  published sibling are byte-identical at tree SHA-256
  `34ec72379ae65788d03dbc195708c71ae7743955de636261a118b61598d4f9b9`;
  strict zero-correction output hashes to
  `d787dc0a8ba4388b3a0f1c83f38ed5f5f3c56bc1741241518373b997d2937401`.
  Recurrence searches found both earlier `guite` instances already corrected
  in `CH07` and pinned two source-confirmed future instances to `N09` and
  `N10`; styled ordinal, technical-span, page-join, plate-placement, furniture,
  and visual-boundary detector families remain carried forward for their
  owning passes. `CH12` is complete at `YES/YES` after its full first pass and
  wholly fresh post-recrop source, technical, and visual closing passes over
  all 134 PDF pages 731–864. Its 131 guarded corrections are
  `G5-C-0731`–`G5-C-0861`; 59 mapped originals plus additions
  `G5-A-0035`–`G5-A-0041` produce 66 unique final references. The final
  252,955-byte, 1,686-line Markdown hashes to
  `a1384ad5ada245f65d5ba8c5ff2af275ec1101252775a33ad69a7279216688d7`.
  A final visual traversal reopened two theorem plates whose first crops omitted
  terminal continuation ellipses; both were recropped and all three closing
  passes restarted from PDF 731. Their final source, technical, and visual
  reports hash to
  `7ed3469133169de183c663d2366b6cd239a111c681842ccf11107248dd643166`,
  `8c638f311105881f0502170d7b5d70506fb9401706744e4405f4e1f2bedb134c`,
  and `5d551a5b503388fd4630a956bc6387b6358c9e5ba1eb01d55e3a94ba598b4be4`;
  every discrepancy and ambiguity ledger closes at zero. The final 119-page
  render hashes to
  `087f84eec6ee4a68f012568e301333e3853bc1aa413bb9937cce348be0db9a70`.
  Six focused CH12 tests, the 104-test Goal 5 suite, and the complete 206-test
  repository suite with 613 subtests pass. At Stage 5 closure, default
  validation reported 29 documents, 1,485 images, 861 corrections, and 14
  completed second passes.
  Two fresh normal builds and the published sibling were byte-identical at
  1,516 files with tree SHA-256
  `098f7979614a1bdfc4168491f68ae89e6de6ca1b2f764c1afdcb49f805086c2f`;
  strict zero-correction output remains
  `d787dc0a8ba4388b3a0f1c83f38ed5f5f3c56bc1741241518373b997d2937401`.
  Fourteen documents had both passes complete. Stage 6 started at
  `GENERAL_NOTES` PDF 865, raw line 10,623, byte 1540232, and its first mapped
  visual is ordinal 823 on PDF 867. The initial Stage 6 IDs were `G5-C-0862`
  and `G5-A-0042`.
- `GENERAL_NOTES` is complete at `YES/YES` after a full first pass and wholly
  fresh post-integration source, technical, and visual closing passes over PDF
  pages 865–874. Its 21 guarded corrections are `G5-C-0862`–`G5-C-0882`.
  The final 44,301-byte, 191-line Markdown hashes to
  `1a5b294ecc1be93f0ed1f565646eaedaab10775f87ca314e0225c76bad76a10c`;
  all 32 main notes, five program subgroups, 45 program expressions, 32 table
  cells, two inline patterns, and mapped ordinal 823 close with zero discrepancy
  and zero ambiguity. The closing source, technical, and visual reports hash to
  `bde3ca484129a34ae5f29ca07a9f76eb3c6ff344b36f9f0d76358d0076e14bb5`,
  `5d62c26ee888b0d1eb40dd1486d1a8d7c99c423de9c08f71874411e865c96c28`,
  and `dc8ca77ae8f9e215f9b97e91d096950d6a1f41f7da2ace2930fd8025cb2328ed`;
  the fresh 13-page render hashes to
  `44f10b9346c797850d07935be6a8a17eeef57bf046408eb17545f0e5f4ea9b29`.
  Default validation now reports 882 corrections and 15 completed second-pass
  documents. Five focused tests, the 109-test Goal 5 suite, and the complete
  211-test repository suite with 649 subtests pass. Two fresh normal builds and
  the published sibling are byte-identical at tree SHA-256
  `008e7a5a76abc7eba70832b0dc35277a84c0eeb067e7b37eb516f973c5c5f3ba`.
  This was the clean baseline used to start `N01`.
- `N01` is complete at `YES/YES` after a full first pass and wholly fresh
  post-italic-fix source, technical, and visual closing passes over PDF pages
  875–880. Its 23 guarded corrections are `G5-C-0883`–`G5-C-0905`. The final
  29,769-byte, 75-line Markdown hashes to
  `3321cc8267ac42e44506e911348764e0698e2bd0b147886e115decd994a12c47`;
  all 22 main notes, five Timeline subitems, nine italic spans, 65 references,
  155 numeric-bearing spans, punctuation, structure, and the source-confirmed
  absence of mapped images close with zero discrepancy and zero ambiguity. A
  fresh closing traversal found the John Ray title-final comma outside the
  Markdown emphasis; the guarded target was repaired and all three closing
  passes restarted from PDF 875. Their final source, technical, and visual
  reports hash respectively to
  `2fc709fd033ab8db237d79867816772c5afde05b16aaf5a8d8ddda63aa619b4c`,
  `8d91d25e466b24d7eb2667a37051b3f377971b156c4b45ece86139ec7546e9d5`,
  and `5c0a62c233453c8501e92254845ac7ab93cc735e2c438519e44bc82b64172a3f`;
  the fresh eight-page render hashes to
  `c4f1462d9589cf3c395a5d657d75abfe3acc3846263275f217b5e20d83959b0a`.
  Default validation now reports 905 corrections and 16 completed second-pass
  documents. Five focused tests, the 114-test Goal 5 suite, and the complete
  216-test repository suite with 690 subtests pass. Two fresh normal builds and
  the published sibling are byte-identical at tree SHA-256
  `1dde0107282feb217c20984c122e5218fdba4f28546e191179ec9d9291417d7a`;
  strict zero-correction output remains
  `d787dc0a8ba4388b3a0f1c83f38ed5f5f3c56bc1741241518373b997d2937401`.
- `N02` is complete at `YES/YES` after a complete first pass and wholly fresh
  post-Science-Citation source, technical, and visual closing passes over PDF
  pages 881–898, with PDF 880 and 899 checked as ownership boundaries. Its 43
  guarded corrections are `G5-C-0906`–`G5-C-0948`. The final 86,695-byte,
  915-line Markdown hashes to
  `8eab0420ff8fbe512d7731c6539742bf0c16bf28dab4ff27fec7dee2ae8f43b0`;
  54 mapped references plus `G5-A-0042` and `G5-A-0043` produce 56 final
  references, with eight mapped references using repaired-only overrides. All
  47 fenced blocks, 105 inline-code spans, 175 emphasis spans, and 27 reopened
  typography regions close with zero discrepancy, zero ambiguity, and zero
  source omission. The final source report, manifest, and `SHA256SUMS` hash
  respectively to
  `477bc5e764bc11c1dca9abaeddc504a19d5af08230221537f895edf1538d9f80`,
  `5ba7a8e990991c66a09f0723ac3de02afba3e4bb6d754a838bda56141ddad66d`,
  and `d3388b811a84fa34f16c3e43b4ebaf8d393b1b924535393763e8eca6b3483d03`.
  The final technical and visual reports hash to
  `067ebaf65e2a65a695508be3fb64744bc1268c739ddfe4e192a404ff76af9ee6`
  and `6a306875d15947cf7d4c5efd3ad7da2859bc38fb1585d6a01c2e687d59802d75`;
  the final render hashes to
  `d082121c86fa72a5c9b80375c90e4bc03cad3beb153eaba146b337cd9b9c8b7b`.
  Default validation reports 948 corrections and 17 completed second-pass
  documents. The focused N02, Goal 5, and complete repository suites pass at
  10, 124, and 226 tests with 768 repository subtests. Two fresh normal builds
  and the published sibling are byte-identical at 1,518 files with tree
  SHA-256
  `aad13eb645fcfb252b5ade650cbf2316c5c67c60139c78e518ae556c28bb92f6`.
  This was the clean baseline used to start `N03`.
- `N03` is complete at `YES/YES` after first-pass integration and wholly fresh
  post-operator source, technical, and visual closing passes over PDF pages
  899–916, including the intentional blank PDF 916 and both ownership
  boundaries. Its 25 guarded corrections are `G5-C-0949`–`G5-C-0973`. The
  final 82,769-byte, 867-line Markdown hashes to
  `897cae5d2988c0e4d746aad431cffc411a81d2766e057d184f2c47f718755007`.
  All 11 headings, 83 main notes, 39 subitems, 351 technical objects, 256
  Boolean rules, 135 printed page-reference phrases, and 45 live image
  references close with zero discrepancy, ambiguity, or source omission.
  Ordinal 894 is a source-confirmed rasterized-prose false positive; four
  mapped operator panels use source-isolated overrides, and additions
  `G5-A-0044`–`G5-A-0049` restore six omitted visuals. The fresh source,
  technical, and visual closing reports hash respectively to
  `d77aaaba75f41845e4a30ab21d93c4a075bce56a0a1b842b0f56f1de0e39b8bf`,
  `4d113c8b6037ac688017925f7d036cca4e281e21b059291f1c87b7afb5eacf26`,
  and `4ccb764d7bff13deb7cdec8a2a16387532dd0e00f4749d21c1d5216f0576051c`.
  Default validation reports 1,493 images, 973 corrections, and 18 completed
  second passes. The focused N03, Goal 5, and complete repository suites pass
  at 9, 133, and 235 tests with 1,097 repository subtests; two fresh normal
  builds and the published sibling are byte-identical at 1,524 files with tree
  SHA-256
  `6723d7eb843f6beb6d344591a5d36145f821f46c0146e7d319dd6b22705a19f8`.
  This was the clean baseline used to start `N04`.
- `N04` is complete at `YES/YES` after its complete first pass and repeated
  mandatory fresh source, technical, and visual closing restarts against the
  final rebuilt target over PDF pages 917–942, with both ownership boundaries
  checked. Its 76 guarded corrections are `G5-C-0974`–`G5-C-1049`; its final
  115,687-byte, 1,040-line Markdown hashes to
  `2c3aa3a04768d9472e365aafef9eac13a984e29cba9e91bafa5737307e7beeed`.
  All 71 mapped rows were source-dispositioned: 30 source-redundant partial
  crops are omitted, while 41 retained rows plus additions `G5-A-0050`–
  `G5-A-0060` produce 52 live image references. The final source, technical,
  and visual reports hash respectively to
  `3aa639f69edf93368798bccd1ca4e80c3b5ad0fba926c2c9a2d579bc8837b4c1`,
  `41095776bac647d7481c79149ee475681b3c8e4063fa3036b9d00bbaa1e034c6`,
  and `bc5192055c3fea1378944178ae12653d0f3b8e1f3031b110ca12b8f413b43660`.
  Every final ledger closes with zero discrepancy, zero ambiguity, and zero
  source omission. Post-coverage validation reports 29 documents, 1,504
  images, 1,049 corrections, and 19 completed second passes. The focused N04,
  Goal 5, and complete repository suites pass at 7, 140, and 242 tests; the
  latter two each report 1,305 subtests. Two fresh normal builds and the
  published sibling are byte-identical at 1,535 files with tree SHA-256
  `88b9fc5124f10a4defa30e9f641fa7550ff96538cb5b35a856b307623bdacb39`.
  These are inherited Stage 6 closure results; this Stage 7 activation edit did
  not rerun them.
- `N05` is complete at `YES/YES` after its complete forward first pass and
  wholly fresh post-repair source/content, technical, and visual closing
  restarts over PDF pages 943–962, with the N06 handoff on PDF 963 checked.
  Its 164 guarded corrections are `G5-C-1050`–`G5-C-1213`; 59 mapped rows
  include 33 source-redundant partial-crop dispositions and four repaired-only
  overrides, while additions `G5-A-0061`–`G5-A-0071` produce 37 final live
  references. The final 86,868-byte, 757-line Markdown hashes to
  `e1e7e6c733ee874c1d7dff7fdb86a18f36da5d7e55ac67a5a76f8f4fb1dcddaa`.
  The wholly fresh source/content, technical, and visual reports hash
  respectively to
  `210387869967a39d958dd5e87873e3ca2f642290ce7edbeeaf15ed1c97c1c675`,
  `5d065fa158442a7505067d73d39b455769ecc650fa41b7c07d2d980e2b6080bd`,
  and `e39ec0283abc03702312b7e20f1467751d7a4b21f74e03a6ccd76efd36724ed1`;
  each closes with zero discrepancy, zero ambiguity, and zero source omission.
  Default validation reports 29 documents, 1,515 images, 1,213 corrections,
  and 20 completed second passes. The focused N05, Goal 5, and complete
  repository suites pass at 6, 146, and 248 tests. Two fresh normal builds and
  the published sibling are byte-identical at 1,546 files with tree SHA-256
  `6deb5c50789cebcb265d8bfc4668c0b5d6b97d6d8dd4a5a483a0da622c4262f5`;
  strict zero-correction output remains
  `d787dc0a8ba4388b3a0f1c83f38ed5f5f3c56bc1741241518373b997d2937401`.
- `N06` is complete at `YES/YES` after a full first pass and wholly fresh
  post-grouping-and-column-join R4 source, technical, and visual closing
  traversals over PDF 962–983. Its 188 guarded corrections are
  `G5-C-1214`–`G5-C-1401`; 64 mapped rows comprise 30 omitted redundant
  partials, 28 retained originals, and six repaired-only overrides, while
  additions `G5-A-0072`–`G5-A-0079` produce 42 live references. The final
  85,467-byte, 666-line Markdown hashes to
  `54bf7356136644c5040ffcc7945b49faab73a2bf5f2758dc51ff91b49e1eb437`.
  The final source, technical, and visual reports hash respectively to
  `1ad9878e74315fe246fd7077ddf62b9447edfb1689980dbd282e49c734850d8f`,
  `cc003058bb1ec22f4a896db2463908a8b5fa0adc71734fadabdaccddb9a61283`,
  and `6f313c25158310eeb03a5fc84fe518f319f897d699a82b4c065e8e382ea9af4b`;
  each closes with zero discrepancy, ambiguity, or omission. The 30-page
  final render hashes to
  `bb620243b6bd7076dcaa2922e15b552804cc27b585eae7402b485ff54409b9c8`.
  Post-coverage validation reports 29 documents, 1,523 images, 1,401
  corrections, and 21 completed second passes. The focused N06, Goal 5, and
  complete repository suites pass at 6, 152, and 254 tests with 318, 1,951,
  and 1,951 subtests. Two fresh normal builds and the published sibling are
  byte-identical at 1,554 files with tree SHA-256
  `dd188b36e430c60ed3e6192a93553c7ea64346d12250a62661dbba05343236b4`.
- `N07` is complete at `YES/YES` after its complete forward first pass and
  wholly fresh post-R2 source/content, technical, and visual R3 closing
  traversals over all 24 owned PDF pages 983–1006, with boundary pages 982 and
  1007 independently checked. Its 217 guarded corrections are
  `G5-C-1402`–`G5-C-1618`; the final 115,684-byte, 692-LF Markdown hashes to
  `fd8696100529789964578841267bbd841411691d05248840ede6e0b4b7bd69f3`.
  All 88 mapped rows were source-dispositioned as 59 omitted redundant
  partials, 20 retained originals, and nine repaired-only overrides; additions
  `G5-A-0080`–`G5-A-0093` produce 43 live references. The final source,
  technical, and visual reports hash respectively to
  `5f67608aa4bc0ccd9b2221ea6f5ec758e5d204397c308b2374a3681534dd45fb`,
  `67e46056a5748b30532a59339013c2270b87e47766931e78e09153a6e97bb28f`,
  and `33cf0cca3ab3055f1d99f9d681498860725804065a4fc3f03bba1d63e480c21c`;
  all final ledgers close with zero discrepancy, ambiguity, or source
  omission. Post-coverage validation reports 29 documents, 1,537 images,
  1,618 corrections, and 22 completed second passes. The focused N07,
  combined N06+N07, Goal 5, and repository suites pass at 6, 12, 158, and 260
  tests, with 2,395 repository subtests. Two fresh normal builds and the
  published sibling are byte-identical at 1,568 files with tree SHA-256
  `82410c48a7f8d362a64cb1e11e2b29dd6579f115d5e3de8f17e3043d18501c9f`.
- `N08` is complete at `YES/YES` after its 26-page first pass and wholly fresh
  post-five-repair source/content, technical, and visual closing restarts over
  PDF 1007–1032, with blank PDF 1032 and boundaries 1006/1033 checked. Its 293
  guarded corrections are `G5-C-1619`–`G5-C-1911`; the final 134,385-byte,
  358-LF Markdown hashes to
  `86e49c4265e2e00567d2964c83d1272575c5dc36a83d7acb7bece7e7aa7997cd`.
  The 32 mapped rows comprise 29 omitted redundant partials and three retained
  originals; additions `G5-A-0094`–`G5-A-0102` produce 12 live references.
  The fresh final source, technical, and visual reports hash respectively to
  `efc334026604a86540986ec293010067ad68db0a5bc5d501150cacb44644c43a`,
  `920374d14ca6b003a3d8dfc2bd615c8344dfd3c88d36817d8eb224b1517e71d4`,
  and `7fbb2e4c2439ee576ca7e74141ddd8fd8d8f3aa15cc68f095a10511cee516e71`;
  every final ledger closes at zero findings. Post-coverage validation reports
  29 documents, 1,546 images, 1,911 corrections, and 23 completed second
  passes; the Goal 5 and repository suites pass 168 and 270 tests with 2,800
  repository subtests. Two fresh normal builds and the published sibling are
  byte-identical at 1,577 files with tree SHA-256
  `17c5fb5f9c6c46acb50bad20098614eab536988cb27acc10bd6b8be84f5d08e8`.
- `N09` is complete at `YES/YES` after its complete forward first pass and
  wholly fresh post-punctuation-repair source/content, technical, and
  visual/caption closing traversals over PDF 1033–1082, with boundaries
  1032/1083 checked. Its 894 guarded corrections are
  `G5-C-1912`–`G5-C-2805`; the final 262,097-byte, 1,000-LF Markdown hashes to
  `72c07a44ac1c2879c123ee0871a68cef6ba28a0de6b284169353abb85915eda1`.
  The 70 mapped rows comprise 54 omitted redundant partials, 13 retained
  originals, and three repaired-only overrides; additions
  `G5-A-0103`–`G5-A-0118` produce 32 live references. The fresh final
  source/content, technical, and visual/caption reports hash respectively to
  `24135aef1c029ee4ffd771d41aa0e97a3ee3125436bfabda912fa5e5d85e0589`,
  `6b5e3e974c6b1711bf35f3707e34e9262d6ad7dfcac588b6a13026bba741caed`,
  and `d2ea2e16995a0badc2cb865d01a187c0e027e67e4dcb2087e078204b139ee598`;
  all close with zero discrepancy, ambiguity, or source omission. The technical
  manifest hashes to
  `467038260562900858efc14d814712a1ca9ca67e3b3c2ca1ce5e5df85069e505`
  and accounts for 558/558 objects. The final render report and 61-page PDF
  hash respectively to
  `680e9ff5710dc3f39db1ab9ad81ab9a8ac962e4efe8f7acbacdb300140380377`
  and `672fd099b2b2329ed6b0bb1f158186e1c2cd7f029cb74fd24353e992ba7e80b9`.
  Post-coverage validation reports 29 documents, 1,562 images, 2,805
  corrections, and 24 completed second passes; the focused N09, Goal 5, and
  repository suites pass at 7, 175, and 277 tests with 3,765 repository
  subtests. Two fresh normal builds and the published sibling are
  byte-identical at 1,593 files with length-prefixed tree SHA-256
  `def3951ddfd3c7fb4ab3666aaca1ac9e61631ac1c6110cbe9d03c0b9fa845861`;
  strict zero-correction output remains 1,475 files with length-prefixed tree
  SHA-256
  `1971cbef0d2c588ee94eb0d268e535c1e9fd2eb6bcc8864bd671ab40ca98729b`.
- `N10` is complete at `YES/YES` over PDF pages 1083–1122 after all late text
  and visual findings were integrated and every dependent closer restarted.
  Its 555 guarded corrections are `G5-C-2806`–`G5-C-3360`; its 23 pinned
  assets are `G5-A-0119`–`G5-A-0141`; all 91 mapped rows are dispositioned as
  57 omitted redundant partials, 33 retained originals, and one repaired-only
  override. The final 197,898-byte, 1,098-LF Markdown hashes to
  `96601763703c87874ec465245b55ed68ee5d59ecc560814ca6fbf078660b2e29`
  and contains 57 resolving image references, 49 fenced blocks, 93 inline-code
  spans, 209 inline-math spans, and five display-math blocks. Wholly fresh
  source/content, technical, and visual packets account for all 40 pages plus
  boundaries 1082/1123 and close with zero discrepancy, ambiguity, or source
  omission. Their report/verdict hashes are respectively
  `54befd3c9c44c894c98a5a8e9109bc228e7189aabbf346d7e4937fd97dd038c2`,
  `1312617c3f027fb9a8ca73336b7591bfdd7be8b0ce213246decb35d3d0936049`,
  and `20b27b225374bfe3e96056843c405849aa73c16260ac48283d50bd0d470baec2`.
  Post-coverage validation reports 29 documents, 1,585 images, 3,360
  corrections, and 25 completed second passes; the focused N10, Goal 5, and
  repository suites pass at 7, 182, and 284 tests with 4,414 cumulative
  subtests. Two fresh normal builds and the published sibling are
  byte-identical at 1,616 files with length-prefixed tree SHA-256
  `45b6d6075dd3a33dc1892be25cefc1e8746ac8cdce26241350daf9d0ef026d38`;
  strict-zero remains the frozen 1,475-file tree. The protected legacy tree
  remains the frozen 1,463-file digest.
- `N11` first-pass source, technical, and visual work over PDF pages 1123–1140
  is integrated but not closed. The 147 source and 100 technical proposals
  initially merged into 213 nonoverlapping guarded corrections; all 26
  cross-lane overlap components preserve both lanes. The first wholly fresh
  closing round then independently found two omitted source connectives,
  “With the choice” on PDF 1131 and “or” on PDF 1137. Repairs
  `G5-C-3574`–`G5-C-3575` bring N11 to 215 corrections,
  `G5-C-3361`–`G5-C-3575`. All
  14 mapped visuals are retained, and additions `G5-A-0142`–`G5-A-0148`
  restore seven missing source visuals. The repaired 87,989-byte, 986-LF target
  hashes to
  `03de4e8dbb7873d764ace90eedc136d161f045aae7001423a631fd529d9c3a9f`
  and contains 21 resolving image references and 66 fenced programs. An
  independent reconstruction of the initial integration closed with zero
  discrepancy before the two fresh-round findings. Two fresh post-repair
  normal builds are byte-identical at
  1,623 files with length-prefixed tree SHA-256
  `dc4df2dd03f4155cf37b56c79d0a8403979b325304f2a3a4d2cc6779acf4cb97`;
  strict zero-correction output remains the frozen 1,475-file tree. Coverage
  intentionally remains `NO/NO`; all source, technical, and visual closers must
  restart from PDF 1123 after the repaired target is published.
- Stage 7 is complete. Stage 8 remains active with `N09` and `N10` closed and
  `N11` awaiting its restarted final closing round. The next available IDs are `G5-C-3576`
  and `G5-A-0149`.

## Stage Status

| Stage | Status | Prerequisites |
|---|---|---|
| 1-CLEANUP | `COMPLETE` | none |
| 2-FOUNDATION | `COMPLETE` | 1 |
| 3-FRONT-CH04 | `COMPLETE` | 2 |
| 4-CH05-08 | `COMPLETE` | 2 |
| 5-CH09-12 | `COMPLETE` | 2 |
| 6-NOTES-00-04 | `COMPLETE` | 2 |
| 7-NOTES-05-08 | `COMPLETE` | 2 |
| 8-NOTES-09-12 | `IN_PROGRESS` | 2 |
| 9-TECHNICAL | `NOT_STARTED` | 3–8 |
| 10-FIGURES-INDEX | `NOT_STARTED` | 3–8 plus fixed-layout source evidence |
| 11-SATURATION | `NOT_STARTED` | 3–10 |
| 12-RELEASE | `NOT_STARTED` | 11; zero open source ambiguity |

## Stages

### 1-CLEANUP

#### Big Picture Objective

Remove Goal 4 process overhead while preserving any compact source facts or
content-oriented tools that genuinely help produce the reliable book.

#### Detailed Implementation Plan

- Sync the live worktree and inspect every modified/untracked Goal 4 file.
- Inventory Goal 4 artifacts by purpose: source fact, content detector/builder,
  or process machinery.
- Keep or migrate only directly useful corpus manifests, boundary facts, known
  defect locations, image mappings, or small content checks after independently
  validating them.
- Remove generalized schemas, proof/implementation locks, licensing/workflow
  state machines, authority and reviewer models, synthetic overlay systems,
  promotion-race defenses, redundant validators/tests, generated reports,
  caches, and unfinished pipeline work.
- Inspect the repaired sibling and remove only unverified Goal 4 output so Goal
  5 starts from a clean build target.
- Confirm no live documentation or consumer is left pointing at removed Goal 4
  machinery.

#### Completion Requirements

- The stage report records pre-cleanup status and a complete keep/delete/migrate
  decision by artifact category.
- No unrelated modification is lost and the legacy corpus hash is unchanged.
- No retained artifact exists merely to validate another retained Goal 4
  artifact; every retained item directly supports correction or verification.
- Goal 4's generalized pipeline/security/workflow infrastructure and caches are
  absent.
- Goal 5 has a short, understandable starting dataset rather than a dependency
  on Goal 4's trust chain.
- `git diff --check`, broken-reference inspection, and explicit scope review
  pass.

### 2-FOUNDATION

#### Big Picture Objective

Secure the complete authoritative source, freeze the 29-document layout, and
implement the minimal reproducible build and coverage model.

#### Detailed Implementation Plan

- Recompute the legacy corpus inventory, hashes, document boundaries, image
  sequence, and known structural failures.
- Establish a complete lawful edition-identical source and document its edition,
  access boundary, page/location convention, completeness, and legibility.
- Define ordered review ranges that cover all book content without requiring a
  per-block evidence graph.
- Freeze the 29 output paths and a minimal Markdown serialization policy.
- Implement a straightforward builder that projects raw content into 29
  documents and then applies guarded corrections.
- Implement a focused validator for source range coverage, correction preimages,
  document counts, image/link resolution, and deterministic output.
- Create the initial `coverage.csv`, `corrections.jsonl`, and `unresolved.md`
  formats with only fields used by the workflow.

#### Completion Requirements

- The complete authoritative source is lawful, edition-matched, readable, and
  sufficient for all later batches; otherwise the stage stays blocked with an
  exact acquisition action.
- Exactly 29 ordered source/output ranges cover the complete raw book stream
  without gap, overlap, or duplication.
- A zero-correction build succeeds and reassembles to the selected raw stream.
- All 1,444 raw image references and physical legacy assets are inventoried.
- Builder, validator, correction record, and coverage record are small and
  documented.
- Focused raw-drift, boundary, skipped-range, duplicate-range, and correction-
  preimage tests pass.

### 3-FRONT-CH04

#### Big Picture Objective

Correct and verify publication matter, Preface, and Chapters 1–4 against the
authoritative source.

#### Detailed Implementation Plan

- Review every assigned range sequentially, including headings, page furniture,
  prose, lists, formulas, code, captions, tables, and images.
- Record and apply exact source-backed corrections.
- Run prose, punctuation, word-split, fence, math, code, and image/caption
  detectors over the batch.
- Render changed and structurally complex regions.
- Perform a separate second comparison of the complete batch and close all
  discrepancies.

#### Completion Requirements

- Every assigned source range has first- and second-pass coverage.
- All discovered OCR/layout discrepancies are corrected and verified.
- Every correction is guarded and source-located.
- No unresolved author-text item remains in the batch.
- Focused detectors, rendering checks, builder, and validator pass.

### 4-CH05-08

#### Big Picture Objective

Correct and verify Chapters 5–8 against the authoritative source.

#### Detailed Implementation Plan

- Apply the complete sequential comparison, correction, detector, rendering,
  and separate second-pass procedure from Stage 3.
- Pay extra attention to higher-dimensional layouts, formulas, rule diagrams,
  scientific notation, captions, and application-specific vocabulary.
- Fold newly discovered OCR patterns into corpus-wide detector queries without
  treating matches as automatic corrections.

#### Completion Requirements

- Chapters 5–8 have complete first- and second-pass coverage.
- All discovered discrepancies are corrected and source-verified.
- New defect patterns are searched across already reviewed and future material.
- No unresolved author-text item remains in the batch.
- Focused and cumulative validation passes.

### 5-CH09-12

#### Big Picture Objective

Correct and verify Chapters 9–12 against the authoritative source.

#### Detailed Implementation Plan

- Apply the complete batch procedure from Stage 3.
- Give formulas, symbolic notation, networks, computation diagrams, code, and
  Chapter 12's transition into General Notes explicit attention.
- Recheck any corpus-wide patterns discovered in earlier chapter batches.

#### Completion Requirements

- Chapters 9–12 have complete first- and second-pass coverage.
- All discovered discrepancies and the Chapter 12 ending boundary are correct.
- No unresolved author-text item remains in the batch.
- Focused and cumulative validation passes.

### 6-NOTES-00-04

#### Big Picture Objective

Correct and verify General Notes and Chapter 1–4 Notes.

#### Detailed Implementation Plan

- Review every Notes range sequentially with its printed page/source context.
- Preserve Notes headings, page references, cross-references, formulas, code,
  citations, captions, and image ownership accurately.
- Apply detectors and a separate full second pass, including prior corpus-wide
  defect patterns.

#### Completion Requirements

- General Notes and Chapter 1–4 Notes have complete two-pass coverage.
- Note ownership and main-text boundaries are correct.
- All discovered discrepancies are source-verified and corrected.
- No unresolved author-text item remains in the batch.
- Focused and cumulative validation passes.

### 7-NOTES-05-08

#### Big Picture Objective

Correct and verify Chapter 5–8 Notes.

#### Detailed Implementation Plan

- Apply the complete two-pass Notes review procedure from Stage 6 to every
  source page, including blank and image-only pages.
- Recheck dense formulas, programs, references, and figure/caption associations
  with surrounding source context.
- Verify the `N04`/`N05` and `N08`/`N09` ownership boundaries and disposition
  every mapped row and every printed visual against the fixed-layout source.
- After the last correction or asset change, restart independent source,
  technical, and visual closing passes from the document's first source page.

#### Completion Requirements

- Chapter 5–8 Notes have complete first- and second-pass coverage.
- All discovered discrepancies are corrected and source-verified.
- All 243 mapped rows and every printed visual have explicit source
  dispositions, with correct identity, crop, order, ownership, and captions.
- No unresolved author-text item remains in the batch.
- Focused and cumulative validation passes.

### 8-NOTES-09-12

#### Big Picture Objective

Correct and verify Chapter 9–12 Notes.

#### Detailed Implementation Plan

- Apply the complete Notes review procedure from Stage 6.
- Verify the displaced material currently found in nominal Index/Colophon files
  is assigned to the correct Notes document and source order.

#### Completion Requirements

- Chapter 9–12 Notes have complete first- and second-pass coverage.
- All displaced Notes boundaries and all discovered discrepancies are correct.
- No unresolved author-text item remains in the batch.
- Focused and cumulative validation passes.

### 9-TECHNICAL

#### Big Picture Objective

Perform a corpus-wide specialist-style fidelity pass over formulas, Wolfram
Language, rule tables, symbolic data, and other token-sensitive material.

#### Detailed Implementation Plan

- Enumerate technical regions from the corrected Markdown and compare each one
  directly with the authoritative source.
- Check symbols, delimiters, superscripts/subscripts, whitespace where
  meaningful, row/column order, code identifiers, operators, and line wrapping.
- Parse, render, or execute material where useful for defect discovery, while
  keeping the source comparison authoritative.
- Reopen owning content batches for any newly discovered discrepancy.

#### Completion Requirements

- Every technical region is enumerated and receives a dedicated source check.
- Every changed token is source-verified and correction records are complete.
- Parsing/rendering diagnostics have no undispositioned hit.
- No unresolved technical transcription ambiguity remains.
- Reopened batch checks and cumulative validation pass.

### 10-FIGURES-INDEX

#### Big Picture Objective

Verify all figure/caption associations and reconstruct the Index and Colophon
accurately from layout-aware source evidence.

#### Detailed Implementation Plan

- Compare every printed figure and caption with the existing asset sequence,
  detecting missing, partial, swapped, duplicated, or misowned images.
- Correct caption text and placement from source evidence.
- Reconstruct the Index in printed column and entry order, preserving headings,
  subentries, cross-references, punctuation, and page ranges.
- Verify the Colophon and all actual Index/Colophon boundaries.
- Perform a separate second pass over the complete Index and all changed figure
  groups.

#### Completion Requirements

- Every printed figure/caption group has a checked Markdown/asset disposition.
- All image references resolve and agree with their source placement.
- The complete Index has two-pass fixed-layout coverage and correct entry order.
- Colophon content and boundaries match the authoritative source.
- No unresolved figure, caption, Index, or Colophon ambiguity remains.
- Focused and cumulative validation passes.

### 11-SATURATION

#### Big Picture Objective

Find and eliminate residual OCR errors across the assembled corrected corpus.

#### Detailed Implementation Plan

- Run corpus-wide detectors for common OCR substitutions, improbable tokens,
  broken joins/splits, punctuation/Unicode anomalies, malformed Markdown,
  formula/code errors, headings, captions, cross-references, and Index forms.
- Review every detector hit against the authoritative source.
- Conduct a fresh sequential verification pass over all 29 documents using the
  coverage checklist, with special attention to unchanged passages surrounding
  prior corrections.
- Reopen the owning stage for every discovered discrepancy.
- Repeat the complete detector and verification round after the last correction
  until a full round yields no new discrepancy.

#### Completion Requirements

- Every detector hit has a source-backed disposition.
- All 29 documents have a completed fresh verification pass.
- The final complete round finds no new discrepancy.
- `unresolved.md` contains zero author-text transcription ambiguity.
- Coverage, correction, structure, image, link, and cumulative tests pass.

### 12-RELEASE

#### Big Picture Objective

Publish the corrected Markdown source and prove the full-book reliability claim
without reintroducing Goal 4's process overhead.

#### Detailed Implementation Plan

- Build twice from immutable legacy inputs and the correction set into fresh
  directories; compare outputs byte-for-byte.
- Validate document/source coverage, corrections, technical regions,
  figures/captions, Index, navigation, assets, and Markdown rendering.
- Rehash the legacy corpus and compare it with the initial snapshot.
- Run focused Goal 5 tests, affected repository tests, `git diff --check`, and
  explicit scope inspection.
- Publish the verified sibling tree and write concise build, source, review,
  correction, and maintenance documentation.
- State reviewer types accurately and distinguish corrected OCR from optional
  source errata annotations.

#### Completion Requirements

- All prior stages are complete with zero open author-text ambiguity.
- Exactly 29 canonical documents contain the complete book in correct order.
- Complete first-pass, second-pass, technical, figure/Index, and saturation
  coverage is verified.
- Two clean builds are byte-identical and match the published sibling.
- All links and image references resolve and Markdown renders as intended.
- Legacy hashes and existing consumer behavior remain unchanged.
- The final documentation gives exact rebuild/validate commands and accurately
  supports the claim that known OCR errors have been removed.
