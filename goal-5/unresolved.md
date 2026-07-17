# Unresolved items

There is no open Foundation source blocker or author-text ambiguity. Content
review discrepancies are added here only when source comparison cannot resolve
them; all twenty-one documents through Notes for Chapter 6 closed without an
unresolved item.

## FOUNDATION-SOURCE-001 — complete authoritative source

Status: CLOSED on 2026-07-15.

The user authorized the complete local PDF for resuming Goal 5's agent-assisted
comparison and repaired workspace output. The source remains Git-ignored and
outside both the immutable legacy tree and generated repaired tree; this local
authorization does not authorize redistribution of the PDF.

Pinned source facts are in `source-ranges.json`:

- path: `A New Kind of Science/A New Kind of Science.pdf`
- SHA-256:
  `a3cc5dd60e12d6b563aee86ea31a15b03f9cddfd4869b8f965d3a11bbc61a0d6`
- size: 57,779,240 bytes
- identity: First edition, First printing, ISBN `1-57955-008-8`, matching the
  immutable OCR monolith
- extent: 1,280 one-based PDF pages, covering publication matter, Preface,
  Chapters 1–12, General and chapter Notes, fixed-layout four-column Index, and
  Colophon
- location rule: for Arabic-numbered material, logical printed page = PDF page
  − 16 (the Index leaves are unfoliated); legacy `_page_N_` asset names refer
  to one-based PDF page `N + 1`

Ghostscript rendered all 1,280 pages successfully. Twenty-six pages without
extractable text were accounted for as raster title/divider leaves or
intentional blanks. Representative prose, technical, figure, Notes, Index, and
Colophon regions are visually legible. Poppler's 127 bad-annotation-destination
warnings affect PDF links, not rendered content.

The container was reprocessed with pdftk/iText and is not claimed to be an
untouched publisher master. It is documented as a user-authorized,
edition-identical fixed-layout witness. Its embedded text layer is diagnostic
only because custom math glyphs and columns extract incorrectly; visual source
comparison remains authoritative.
