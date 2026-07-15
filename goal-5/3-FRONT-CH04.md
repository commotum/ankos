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
- The repaired tree is currently a zero-correction projection. All six Stage 3
  coverage rows say `NO/NO`; `corrections.jsonl` is empty.
- A source-review pack for the first canonical document exists under
  `/tmp/ankos-stage3-publication/`. Page rasters are authoritative; native PDF
  text is only a navigation/detection aid because its custom glyph and column
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
| 1 | `PUBLICATION_AND_CONTENTS` | 1–8 | `0 → 6480` | IN_PROGRESS | pending | `pdf:0001` |
| 2 | `PUBLICATION_AND_CONTENTS` | 1–8 | final rebuilt document | NOT_STARTED | pending | `pdf:0001` |
| 1 | `PREFACE` | 9–16 | `6480 → 30320` | NOT_STARTED | — | `pdf:0009` |
| 2 | `PREFACE` | 9–16 | final rebuilt document | NOT_STARTED | — | `pdf:0009` |
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

In progress. Foundation gates were rerun on 2026-07-15 before the first content
comparison: `10 passed, 26 subtests passed`; default build and both normal and
zero-correction validation passed; the legacy snapshot remained
`b9ff7b9b507790f1d519593baf2b2d2f24dd6cd49dc0fe10f0ac629278ea42f4`.

Exact resume point: first pass of `PUBLICATION_AND_CONTENTS`, beginning at
`pdf:0001`, raw byte 0. No Stage 3 correction or coverage claim has yet closed.
