# 3-FRONT-CH04

Status: COMPLETE

## Current Facts

- Foundation is complete. The ignored 1,280-page First-edition,
  First-printing PDF is pinned by path, size, and SHA-256 and is the
  authoritative fixed-layout witness for local comparison.
- Stage 3 owns the first six canonical documents: publication matter and
  printed Contents, Preface, and Chapters 1–4.
- Its complete source interval is PDF pages 1–184. Its complete immutable raw
  interval is lines 1–2,141, bytes `[0,355646)`, SHA-256
  `b25f2813c3c9d80e5dd0b877d9d1da2c986ce6a777ec2e8912eecfeefa9646b4`.
- All six document boundaries are source-confirmed. In particular, the Chapter
  1 and Chapter 3 opener images and the textual Chapter 2 and Chapter 4 opener
  numbers belong to the chapters they introduce.
- All six documents are two-pass complete over PDF pages 1–184 with 303
  guarded corrections. The `CH04` independent pass found and repaired one
  omitted continuation marker, then restarted from PDF page 131 against the
  new final document and completed cleanly through PDF page 184.
- Source-review packs exist under `/tmp/ankos-stage3-publication/`,
  `/tmp/ankos-stage3-preface/`, `/tmp/ankos-stage3-ch02/`, and
  `/tmp/ankos-stage3-ch03/`. Page rasters are authoritative; native PDF text is
  only a navigation/detection aid because its custom glyph and column
  extraction is unreliable.

## Updated Assumptions

- A canonical document is the natural coverage unit, with smaller consecutive
  page slices recorded here only to make interrupted work exactly resumable.
- Blank and image-only leaves count in sequential coverage even when they have
  no raw text span.
- Printed running heads and page numbers are checked and dispositioned, but
  need not be transcribed when they are page furniture rather than author text.
- Heading levels encode logical hierarchy rather than raw font size. Source
  bold/italic emphasis is preserved where it carries the presentation, while
  incidental line wrapping, rules, shading, and column geometry are not
  treated as author text. Paragraph, row, list, and table boundaries are.
- A source table without a header row uses a small raw-HTML table rather than
  promoting its first data row to a Markdown header.
- A margin figure and caption are serialized after the earliest complete
  paragraph that explicitly refers to them, or after the closest complete
  adjacent paragraph when there is no reference. This preserves semantic
  association and uninterrupted prose; it is a canonical Markdown
  linearization of a two-dimensional float, not a uniquely printed order.
- A full-page plate sequence that interrupts a raw-extracted sentence is
  serialized after the complete printed prose paragraph. Ordered plates remain
  together, with lead captions, continuation markers, component subgroups, and
  back captions attached to the sequence they govern.
- Title artwork, tables, formulas, code, captions, and text embedded in figures
  require direct visual inspection at sufficient zoom; `pdftotext` agreement
  cannot close them.
- Decorative cover/title-leaf artwork with no additional wording is accounted
  for in the page ledger but is not extracted from the PDF as a new repository
  asset under the current local-comparison-only authorization.
- A first pass and a second pass must each restart at the document's first PDF
  page and inspect the final rebuilt Markdown, not merely the correction list.

## Big Picture Objective

Correct and verify all author text and structure in publication matter,
Preface, and Chapters 1–4 through two complete sequential comparisons with the
fixed-layout source, while preserving the immutable legacy corpus and applying
every change through exact guarded corrections.

## Detailed Implementation Plan

| Document | PDF pages | Printed extent | Raw lines | Raw bytes |
|---|---:|---|---:|---:|
| `PUBLICATION_AND_CONTENTS` | 1–8 | unfoliated | 1–85 | `[0,6480)` |
| `PREFACE` | 9–16 | ix–xiv, divider, blank | 86–165 | `[6480,30320)` |
| `CH01` | 17–38 | 1–22 | 166–397 | `[30320,79330)` |
| `CH02` | 39–66 | 23–50 | 398–679 | `[79330,119521)` |
| `CH03` | 67–130 | 51–114 | 680–1,367 | `[119521,199880)` |
| `CH04` | 131–184 | 115–168 | 1,368–2,141 | `[199880,355646)` |

For each document:

1. Confirm its previous/next boundary and account for every source page,
   including intentional blanks.
2. Compare forward from the first page through the last page against the raw or
   rebuilt Markdown, inspecting headings, prose, punctuation, emphasis, lists,
   tables, formulas, code, captions, figures, page references, and reading
   order.
3. Record each author-text or structural transcription change with its absolute
   raw byte offset, exact preimage/replacement, occurrence guard, canonical
   `pdf:NNNN` location, source-backed rationale, agent reviewer type, and
   `SOURCE_VERIFIED` status.
4. Build and validate after each closed slice. Search the current and previously
   closed Stage 3 material for every newly discovered OCR pattern.
5. Run focused prose, punctuation, split/join, Markdown, formula/code,
   image/caption, and vocabulary detectors and source-disposition every hit.
6. Perform a separate forward second pass against the final rebuilt document.
   Mark its coverage row `YES/YES` only after no discrepancy or ambiguity
   remains.

## Sequential Review Ledger

| Pass | Document | PDF interval | Raw cursor before/after | Status | Correction IDs | Next source page |
|---|---|---:|---|---|---|---:|
| 1 | `PUBLICATION_AND_CONTENTS` | 1–8 | `0 → 6480` | COMPLETE | `G5-C-0001`–`G5-C-0020` | closed |
| 2 | `PUBLICATION_AND_CONTENTS` | 1–8 | final rebuilt document | COMPLETE | verified all 20 | closed |
| 1 | `PREFACE` | 9–16 | `6480 → 30320` | COMPLETE | `G5-C-0021`–`G5-C-0079` | closed |
| 2 | `PREFACE` | 9–16 | final rebuilt document | COMPLETE | all 59 verified; no new discrepancy | closed |
| 1 | `CH01` | 17–38 | `30320 → 79330` | COMPLETE | `G5-C-0080`–`G5-C-0106` | closed |
| 2 | `CH01` | 17–38 | final rebuilt document and assets | COMPLETE | all 27 verified; no new discrepancy | closed |
| 1 | `CH02` | 39–66 | `79330 → 119521` | COMPLETE | `G5-C-0107`–`G5-C-0132` | closed |
| 2 | `CH02` | 39–66 | final rebuilt document | COMPLETE | all 26 verified; no new discrepancy | closed |
| 1 | `CH03` | 67–130 | `119521 → 199880` | COMPLETE | `G5-C-0133`–`G5-C-0193` | closed |
| 2 | `CH03` | 67–130 | final rebuilt document and assets | COMPLETE | all 61 verified; no new discrepancy | closed |
| 1 | `CH04` | 131–184 | `199880 → 355646` | COMPLETE | `G5-C-0194`–`G5-C-0302` | closed |
| 2 | `CH04` | 131–184 | final rebuilt document and assets | COMPLETE | all 110 verified after `G5-C-0303` restart; no new discrepancy | closed |

The first slice's exact page-to-raw map is:

| PDF page | Source content | Raw location |
|---:|---|---|
| 1 | cover title | line 1, bytes `[0,39)` |
| 2 | intentional blank | none |
| 3 | title page | line 3, bytes `[40,79)` |
| 4 | publication, copyright, and CIP matter | lines 5–63, bytes `[80,5476)` |
| 5 | title page | line 65, bytes `[5477,5519)` |
| 6 | intentional blank | none |
| 7 | printed Contents | lines 67–85, bytes `[5520,6480)` |
| 8 | intentional blank | none |

## No-Cheating Checks

- Review pages monotonically and record blank pages; detector-driven jumps do
  not count as coverage.
- Use rendered page evidence for every decision. Native text, raw/split
  agreement, dictionaries, parsers, and model confidence can only raise a
  candidate.
- Preserve typographical or factual errors that are visibly printed in this
  First printing.
- Apply author-text and authorial-structure changes only through
  `corrections.jsonl`; never hand-edit generated repaired documents.
- Corrections must retain the immutable raw byte coordinate even when earlier
  replacements change rebuilt lengths.
- Inspect each source visual and caption in page order. Existing legacy image
  presence and filename ownership do not prove visual completeness or placement.
- Do not claim a complete document pass from a partial page slice, a candidate
  list, or two reviewers examining only known discrepancies.
- Rebuild only from the exact immutable monolith. Rehash the legacy tree and
  inspect Git scope after corrections.

## Completion Requirements

- [x] Every source page from PDF 1 through 184 is accounted for in a complete
  forward first pass.
- [x] All six documents have a separate complete forward second pass against
  the final rebuilt Markdown.
- [x] Every discovered author-text, structure, formula/code, caption, figure,
  table, and reading-order discrepancy is source-resolved, guarded, rebuilt,
  and verified.
- [x] All Stage 3 detector hits have source-backed dispositions and every new
  defect pattern has been searched backward over completed material.
- [x] Stage 3 has zero unresolved author-text ambiguity.
- [x] All six `coverage.csv` rows say `YES/YES` with reviewer type `agent` and
  exact pass evidence.
- [x] Focused tests, cumulative build/validation, legacy-tree hash,
  deterministic builds, Markdown/render checks, `git diff --check`, and scope
  inspection pass.

## Stage Results

Complete. Foundation gates were rerun on 2026-07-15 before content review:
`10 passed, 26 subtests passed`; default build and both normal and
zero-correction validation passed; the legacy snapshot remained
`b9ff7b9b507790f1d519593baf2b2d2f24dd6cd49dc0fe10f0ac629278ea42f4`.

`PUBLICATION_AND_CONTENTS` received two separate forward agent passes over PDF
pages 1–8. Pages 2, 6, and 8 are intentional blanks. Pages 1, 3, and 5 contain
decorative title-leaf designs but no wording beyond the transcribed titles; the
source-derived artwork was not extracted under the current authorization. The
passes found and source-verified 20 nonoverlapping guarded corrections covering
two title word joins, CIP digit confusions, an omitted copyright sentence,
punctuation and permanent-paper sign loss, source emphasis, publisher/CIP row
structure, title/Contents heading hierarchy, and a headerless Contents table.
A fresh closing pass against the rebuilt file found no remaining discrepancy.

The corrected Markdown rendered successfully with CommonMark raw HTML enabled;
the five software-name italics, raised registration sign, line structure,
permanent-paper sign, heading hierarchy, and 12 row headers were visibly
present. Four focused publication tests and all ten Foundation tests passed.

`PREFACE` received a complete forward first pass over PDF pages 9–16 and an
independent fresh second pass against the final rebuilt Markdown. Pages 9–14
contain the Preface and acknowledgments, page 15 is a captionless divider whose
existing asset visually matches the source, and page 16 is intentionally blank.
The 59 source-verified corrections `G5-C-0021`–`G5-C-0079` restore the logical
heading, signature/date and paragraph boundaries, one omitted word and period,
one surname OCR error, 31 date-range punctuation errors, nine software-name
italics, source em/en dashes and curly apostrophes, and five false column/page
breaks. Direct high-resolution inspection preserved the First printing's
`Cvitanovič` spelling instead of applying a misleading native-text extraction.

The final Preface text has 11 source-matching italic *Mathematica* spans and 37
four-digit en-dash ranges. CommonMark parsing, headless rendering, backward
defect-pattern scans over both closed documents, two byte-identical fresh
builds, cumulative validation, and five focused Preface tests passed. The
independent closing pass normalized 23,680 source and rebuilt characters to an
exact match and found no remaining discrepancy or ambiguity. The cumulative
suite now passes 19 tests; validation reports 29 documents, 1,444 images, 79
corrections, and two second-pass-complete documents. `git diff --check` passes.

`CH01` then received a complete forward first pass and a separate fresh pass
over every one of PDF pages 17–38 against the final rebuilt Markdown. Its 27
source-verified corrections restore logical heading levels, seven omitted bold
field labels, source quotes/apostrophe and *Mathematica* emphasis, false
page-turn paragraph breaks plus one spurious OCR glyph, and canonical
linearization of two margin figures with their exact captions. A squashed
legacy opener crop is preserved in the immutable tree while the repaired build
uses a deterministic 154×200 source-faithful composite containing the printed
chapter numeral. The second pass found no new discrepancy or ambiguity: its
8,675-token diagnostic sequence matches exactly, all 25 bold labels and seven
italic *Mathematica* occurrences agree, and all three figures/captions match
visually. Running heads and folios were dispositioned as page furniture.

The repaired-asset path now checks its basename, evidence fields, content hash,
and decoded dimensions. Explicit zero-correction builds copy and validate all
legacy image bytes rather than using repaired overrides; the normal build still
uses the repaired opener. Mutation tests and an independent re-audit confirmed
both modes. The margin-figure placement rule is documented as a canonical
one-dimensional Markdown serialization rather than a uniquely printed order.

`CH02` received a complete forward prose, punctuation, structure, formula, and
visual first pass over PDF pages 39–66. Its 26 source-verified corrections
`G5-C-0107`–`G5-C-0132` restore the chapter opener and hierarchy, remove a
running head, join caption and page-turn breaks, preserve source quotation and
ellipsis forms, normalize two inline formulas, restore two vector-only rule
strips, canonically linearize a rule-90 figure group and the rule-30/rule-110
full-page plate sequences without splitting printed prose, and remove two
residual doubled-space wrappers around inline π symbols. The rule-110 arrows
now govern the correct five-page sequence and separate 3,200-step summary
composite.

All 19 inherited Chapter 2 assets were checked in page order against the PDF;
their files and hashes match, and no swap, omission, or caption mismatch
remains. Three repaired-only source assets are pinned by hash and decoded
dimensions: the 154×200 opener composite (including the live numeral) and two
376×39 vector-only eight-case rule strips. Geometry was independently checked
against the PDF MediaBox. The default rebuild now contains 1,447 images and
132 corrections. A fresh independent second pass then restarted from PDF page
39 against final Markdown SHA-256
`e7a4620f434ab79e259dc6d02bd3157690d97590ceb0c3ec50b85654dcb07a10`
and inspected all 28 pages at 240 DPI. Its non-math source and candidate streams
each contained 6,685 tokens with zero delta; punctuation counts, four math
spans, *Mathematica* emphasis, all step/count values, all 22 assets, and all 12
caption blocks matched. It found no discrepancy or ambiguity.

Focused CommonMark/headless rendering, residual OCR and whitespace detectors,
two byte-identical fresh normal builds, a strict zero-correction build, the
complete 31-test suite, validation, legacy digest, and diff checks pass.

`CH03` received a complete forward first pass over all 64 PDF pages 67–130;
PDF 130 is intentionally blank. Its 61 source-verified corrections
`G5-C-0133`–`G5-C-0193` restore the logical heading hierarchy, source
punctuation and emphasis, character-level technical notation, eleven false
page/plate paragraph breaks, and canonical ordering for multipart figures and
full-page plate sequences. The rules 100–139 plate omitted from the legacy
extraction is restored as `G5-A-0004`. All 86 mapped visuals were inspected;
two truncated/contaminated legacy crops use repaired-only overrides, and the
page 118 symbolic-system figure now masks its raster-only caption while the
exact caption appears once as searchable live Markdown.

The rebuilt Chapter 3 document has SHA-256
`f948d0c45b8bec06b78e72e8e8fa8f807c37f7a0fd29d4b4dc43550bc8768f35`, 87
unique image references, 12 logical subsection headings, 20 balanced math
spans, and no unexplained OCR, Unicode, whitespace, Markdown, vocabulary, or
manifest detector hit. Backward searches found no recurrence of the new
defect patterns in the four closed documents. Seven focused Chapter 3 tests
and all 38 cumulative tests pass. CommonMark/headless rendering produced an
85-page artifact with all images loaded. Two fresh normal builds and the
default output have the identical 1,479-file tree digest
`7bfdb64de9ab3cbe8ba50db64a11d87f593ca8beb837882188b60bb7b4b2ef26`;
the strict zero-correction build validates with 1,444 images. The immutable
legacy tree remains
`b9ff7b9b507790f1d519593baf2b2d2f24dd6cd49dc0fe10f0ac629278ea42f4`
over 1,463 files.

An independent second pass restarted at PDF page 67 and traversed all 64 pages
through PDF page 130 in source order. It compared all 248 final live-text
blocks (179 prose paragraphs, 13 headings, 52 captions, and four live
figure-label blocks) and all 87 final images. Of the text blocks, 217 matched
the normalized source directly; the remaining 31 were individually resolved
as 12 page-turn joins, 11 math/emphasis/font-run cases, five printed
arrow/marker cases, and three native-PDF text-layer artifacts. The pass also
checked all source punctuation, emphasis, formulas, symbolic notation,
captions, figure order, repaired assets, and the intentionally blank final
page. It found no discrepancy or residual ambiguity, and the final document
hash remained unchanged.

`CH04` received a complete forward first pass over all 54 PDF pages 131–184.
Its first 109 source-verified corrections `G5-C-0194`–`G5-C-0302` restore the logical
heading hierarchy, source punctuation and emphasis, technical notation,
damaged numeric data, page-turn joins, compound figure captions, and canonical
reading order. All 59 mapped visuals were checked in source order. Four
source-added assets restore the chapter opener, a missing overview strip, a
digit matrix, and the complete 4,000-digit pi plate; one damaged iterated-map
asset uses a pinned repaired-only override. The final Markdown contains 63
unique image references.

Direct high-resolution source inspection reconstructed 11 headerless tables
with 91 rows and 289 cells, including three exact 6×11 continuous-cellular-
automaton matrices. Numeric sequences, base expansions, roots and logarithms,
continued fractions, iterated maps, and partial differential equations received
token-sensitive checks; continued-fraction values were independently
recomputed at 500-digit precision. CommonMark/headless rendering of the full
chapter and complex technical slices loaded every image and preserved the
intended order. Residual OCR, Unicode, Markdown, formula, page-split, and
backward defect-pattern scans found no unexplained hit. During the independent
pass, direct inspection of PDF page 174 found one omitted printed forward
continuation marker at the end of a lead caption. It is restored by guarded
correction `G5-C-0303`, and the complete pass restarted against the rebuilt
document whose SHA-256 is
`33b0521073b7d212d181903a71b1917b7647b006ef09618f93d89697f8942248`.

The restarted independent pass kept that hash unchanged while checking all 54
pages, all 243 live blocks, 172 TeX spans, 11 tables with 91 rows and 289
cells, all three 6×11 matrices, all nine printed PDE equations, and all 63
assets. A separate visual caption audit checked 45 caption blocks, 38
image-bearing associations, seven table/math-only captions, both printed
directional triangles, and ten marginal/side/foot placements. Both passes
found zero remaining discrepancy, unchecked item, or ambiguity.

The newly discovered missing-marker pattern was searched backward by direct
visual comparison over PDF pages 1–130. Exactly five prior direction markers
and eight additional explicit cross-page continuation captions were found; all
13 are already preserved and associated with the correct Stage 3 figure
groups. Register-machine arrow glyphs were separately dispositioned as
instruction symbols.

The final 47-test suite passes. Default and strict zero-correction validation
pass with six second-pass-complete documents. Two fresh normal builds and the
default output have the identical 1,483-file tree digest
`25c2b759018bdcd930c2aac41cc780384ff33f4490f6b7d0394cf35d53369626`;
the zero-correction build retains 1,444 images and reassembles the raw stream.
The immutable 1,463-file legacy digest remains
`b9ff7b9b507790f1d519593baf2b2d2f24dd6cd49dc0fe10f0ac629278ea42f4`.
The full 67-page Chapter 4 render loads all assets and visibly preserves the
restored forward marker. `git diff --check` and scope inspection pass.

Stage 3 is complete. Exact next action: begin `CH05` at `pdf:0185`, raw line
2,142 and byte 355646, by verifying the chapter opener and image-map ordinal
169 before advancing sequentially through PDF page 238.
