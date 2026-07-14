# Goal 4 Fidelity Contract

Contract ID: `ANKOS-FIDELITY-1`

Status: Frozen by Stage 1; witness identity and region rows are populated in Stage 3.

## Source layers

The immutable legacy root is `ref/A-New-Kind-of-Science/`. Stage 2 must enumerate exactly 19 Markdown files and 1,444 JPEG identities into an explicit path-and-hash allowlist. That manifest, not a recursive build-time scan, is the sole raw-input authority.

The legacy monolith is the only raw author-text conservation stream. Its split Markdown derivatives are routing witnesses whose differences require dispositions, not additional author-text copies. `ANKoS-Atlas.md` is interpretive metadata. The monolith, split files, and Atlas are correlated derivatives and never independent proof of a correction.

The local JPEGs are governed legacy assets and visual/caption candidates, not complete page witnesses. Their filenames, proximity, pixels, OCR, or agreement with prose cannot establish surrounding text, full-plate completeness, column order, or caption ownership.

## Primary witness identity

Stage 3 may certify a witness only after recording:

- title, author, publisher, ISBN, edition, printing, and copyright-page fingerprint;
- complete physical leaf/page/plate census and printed-numbering scheme;
- whole-object identity plus per-page/per-region hashes;
- acquisition source/date, access method, and license state;
- legibility separately for prose/punctuation, formulas/code/data, figures/captions/color, and Index columns.

An official/licensed page image or edition-identical primary text may be authoritative. A bare hash, inaccessible remote preview, model reconstruction, correlated OCR, parser success, execution result, mathematical plausibility, or spell-check result is not content evidence.

## Witness region classes

Every physical witness region receives exactly one class:

- `AUTHOR_TEXT`
- `AUTHOR_VISUAL`
- `SEMANTIC_LAYOUT`
- `PAGE_FURNITURE`
- `BLANK`
- `NONCONTENT_ARTIFACT`

Every `AUTHOR_TEXT`, `AUTHOR_VISUAL`, or `SEMANTIC_LAYOUT` region maps to canonical output or an explicit release blocker. `NOT_APPLICABLE` is allowed only for a legible, evidenced non-authorial region with one of these closed reasons:

- `BLANK_PAGE`
- `RUNNING_HEADER`
- `PRINTED_PAGE_NUMBER`
- `SCANNER_OR_EXTRACTION_ARTIFACT`
- `NONAUTHORIAL_BINDING_OR_CROP`

The reason and evidence require independent review. Missing, illegible, cropped, ambiguous, untranscribed, or unreviewed authorial material can never be `NOT_APPLICABLE`.

## Exact preservation obligations

Canonical transcription preserves every witness-established distinction, including:

- characters, punctuation, quote/dash forms, capitalization, spelling, and source-significant whitespace;
- paragraph, heading, list, table, note, Index, and column hierarchy;
- lexical hyphens versus line/column/page-break hyphenation;
- formulas, code, rule tables, operators, digits, colors, sequences, seeds, and meaningful indentation;
- figure grouping, component order, scale/orientation significance, captions, and meaningful color;
- the printed distinction among source text, page furniture, Index, Notes, and publication matter.

Literal source errors stay in canonical author text. Editorial corrections belong only in `EDITORIAL/Errata.md`. Search normalization and generated accessibility text remain separate derivatives.

## Bidirectional conservation

The final ledgers must prove all three directions:

1. Every raw monolith block maps once to one of the 29 canonical documents or an enumerated typed exclusion that does not hide author text.
2. Every authoritative witness region maps to canonical output, an independently reviewed non-authorial `NOT_APPLICABLE` reason, or a release blocker.
3. Every canonical author-text span maps to immutable raw content or a source-verified insertion.

Gaps, overlaps, unlogged reorderings, silent deletions, and unexplained duplications fail. The derived aggregate is a declared duplicate view and is excluded from the canonical exactly-once domain.

## Text repair and insertion

Every author-text change is per occurrence and needs:

- immutable raw file/block/hash and exact preimage/count, or unique two-sided anchors for text absent from raw;
- edition/page/region identity and evidence hash;
- exact before/witness/after projection;
- forward and inverse operation;
- independent authoritative-source review by a principal other than the creator;
- a final workflow state and disposition.

High risk is the union of repair class and operation/AST impact. Formula, code, data, every structure boundary or authorial hierarchy/Markdown/heading change, Index, caption, visual, and witness-only author-text insertion additionally need a blind pre-proposal decision and the required specialist review. Repeated spelling or dehyphenation is never authorized as one global author-text operation.

## Witness-only binary assets

A source-visible visual component absent from the 1,444 legacy assets is a binary insertion, not an ordinary copy. Its record contains:

- stable asset and repair IDs;
- witness edition/page/region identity and source-byte hash;
- exact binary payload hash, byte size, dimensions, color mode, and permitted transformations (normally none);
- license state and redistribution permission;
- canonical reference insertion anchors and expected adjacency/order;
- creator, independent visual/source reviewer, and disagreement state;
- forward operation that adds the namespaced asset and reference;
- inverse operation that removes both without touching legacy bytes.

Witness-only assets use the separate `ASSETS/WITNESS/` namespace. They cannot enter a published release without explicit redistribution permission. If a required component cannot lawfully be included, visual completion remains source-blocked.

## Full-repair criterion

An unqualified “fully repaired” claim requires exact canonical representation for every authorial witness region, complete raw/witness/output joins, zero unresolved authorial ambiguity of any severity, complete independent review, all required visual components, and a passing audit-mode recheck against the authorized witness. Offline reproducibility alone can produce an `UNCERTIFIED` build but cannot establish fidelity.
