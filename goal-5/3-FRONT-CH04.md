# 3-FRONT-CH04

Status: IN_PROGRESS

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
- `PUBLICATION_AND_CONTENTS` and `PREFACE` are two-pass complete over PDF pages
  1–16 with 79 guarded corrections. The remaining four Stage 3 coverage rows
  remain `NO/NO`.
- Source-review packs exist under `/tmp/ankos-stage3-publication/` and
  `/tmp/ankos-stage3-preface/`. Page rasters are authoritative; native PDF text
  is only a navigation/detection aid because its custom glyph and column
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
| 1 | `CH01` | 17–38 | `30320 → 79330` | NOT_STARTED | — | `pdf:0017` |
| 2 | `CH01` | 17–38 | final rebuilt document | NOT_STARTED | — | `pdf:0017` |
| 1 | `CH02` | 39–66 | `79330 → 119521` | NOT_STARTED | — | `pdf:0039` |
| 2 | `CH02` | 39–66 | final rebuilt document | NOT_STARTED | — | `pdf:0039` |
| 1 | `CH03` | 67–130 | `119521 → 199880` | NOT_STARTED | — | `pdf:0067` |
| 2 | `CH03` | 67–130 | final rebuilt document | NOT_STARTED | — | `pdf:0067` |
| 1 | `CH04` | 131–184 | `199880 → 355646` | NOT_STARTED | — | `pdf:0131` |
| 2 | `CH04` | 131–184 | final rebuilt document | NOT_STARTED | — | `pdf:0131` |

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

- [ ] Every source page from PDF 1 through 184 is accounted for in a complete
  forward first pass.
- [ ] All six documents have a separate complete forward second pass against
  the final rebuilt Markdown.
- [ ] Every discovered author-text, structure, formula/code, caption, figure,
  table, and reading-order discrepancy is source-resolved, guarded, rebuilt,
  and verified.
- [ ] All Stage 3 detector hits have source-backed dispositions and every new
  defect pattern has been searched backward over completed material.
- [ ] Stage 3 has zero unresolved author-text ambiguity.
- [ ] All six `coverage.csv` rows say `YES/YES` with reviewer type `agent` and
  exact pass evidence.
- [ ] Focused tests, cumulative build/validation, legacy-tree hash,
  deterministic builds, Markdown/render checks, `git diff --check`, and scope
  inspection pass.

## Stage Results

In progress. Foundation gates were rerun on 2026-07-15 before content review:
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

Exact resume point: first pass of `CH01`, beginning at `pdf:0017`, raw line 166
and byte 30320. Its 22-page raster review pack is prepared under
`/tmp/ankos-stage3-ch01/`; no CH01 coverage claim has yet closed.
