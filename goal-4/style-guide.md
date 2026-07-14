# ANKoS Repaired Markdown Serialization Profile

Profile ID: `ANKOS-MD-1`

Status: Stage 1 contract frozen; Stage 7 corpus-fixture validation pending.

This profile defines how the reversible zero-repair pipeline may serialize book material without silently changing author text. Stage 7 must validate it against representative and adversarial corpus fixtures. Any semantic change to this profile reopens Stages 1 and 4–6 before content repair continues.

## Roles and conservation domain

Only files declared `CANONICAL_AUTHOR_TEXT` participate in exactly-once author-text conservation. There are exactly 29, in the order frozen by `guardrails.json`.

`DERIVED_AGGREGATE`, `GENERATED_METADATA`, `EDITORIAL_SIDECAR`, `SEARCH_DERIVATIVE`, governed assets, and release metadata are separate roles. They may reproduce or describe canonical content only in the ways their manifests declare. They never become a second canonical copy.

Every canonical byte/span is typed as one of:

- raw author text mapped to an immutable monolith block;
- author text inserted from an edition-identical authoritative witness through a guarded repair record;
- generated metadata that is manifest-typed, removable, and excluded from author-text projection.

No visual or textual styling convention is allowed to blur those types.

## Encoding and file bytes

- Encode Markdown as UTF-8 without a byte-order mark.
- Use LF (`U+000A`) line endings.
- Generated Markdown files end with one LF. This wrapper newline is generated metadata when it was absent from the raw source and is excluded from inverse author-text projection.
- Preserve authorial Unicode scalar values exactly. Do not apply NFC/NFKC normalization, smart-quote conversion, case folding, whitespace folding, tab expansion, or homoglyph replacement.
- Do not trim or reflow author text as an incidental serializer behavior.
- Trailing whitespace is forbidden in generated syntax. Source-significant trailing whitespace, if the witness establishes any, must use an explicit lossless representation approved through a witness-backed repair record rather than invisible trailing bytes.

## Canonical document envelope

Canonical files contain no YAML front matter. Role, order, source spans, hashes, page mappings, and review state live in manifests and ledgers.

Generated anchors or page markers may appear only through the reserved forms below and must be represented as `GENERATED_METADATA` spans in provenance:

```html
<a id="ankos-..."></a>
<!-- ankos-page: edition-id/page-id -->
```

Reserved generated identifiers begin with `ankos-`. Author HTML using the same lexical form must be escaped from the generated namespace in metadata, not rewritten in author text.

## Headings

- Use ATX headings with one space after the marker.
- Heading level follows the verified printed hierarchy, not OCR font size or a repository navigation preference.
- Do not add or remove authorial heading text mechanically.
- A generated document label or navigation title belongs in metadata unless the authoritative witness contains it as book text.
- Setext headings are not emitted by the serializer. A raw Setext-like span remains raw author text until a witness-backed structure record establishes its role.
- Explicit stable anchors precede headings when needed; generated anchors do not replace or alter the source heading.

## Paragraphs, lists, blockquotes, and tables

- Preserve authorial paragraph and line-break semantics from the witness.
- Separate Markdown blocks with a single generated blank line where required by the profile; record block boundaries and inverse projection explicitly.
- Use `-` for unordered-list syntax and `1.` for generated ordered-list syntax only after the printed list structure is witness-verified. Author-visible numbering remains exact author text.
- Do not infer a list from repeated punctuation, indentation, or OCR line shape alone.
- Use `>` only for a verified quotation/blockquote structure.
- Use pipe tables only where the authoritative layout is a true table and the representation preserves row/column order. Otherwise retain a typed structural block for Stage 7 or a release blocker; do not flatten semantic columns for rendering convenience.
- Nonbreaking spaces, em spaces, tabs, and alignment are preserved when source-significant and otherwise represented through typed generated layout metadata rather than silent normalization.

## Code and Wolfram Language

- Emit fenced code blocks with backticks. Choose a fence length strictly greater than the longest run of backticks in the source payload, with a minimum of three.
- The default info string for verified Wolfram Language input is `wolfram`. Other info strings require an enumerated profile entry.
- Fence delimiters and info strings are generated structure; payload bytes are protected author text.
- Preserve every payload token, case distinction, blank line, indentation, operator, bracket, pattern character, and comment exactly as verified.
- Never fence prose merely because the OCR placed it between existing fence delimiters. Fence ownership requires source evidence.
- Parsing or execution can diagnose a candidate but cannot authorize token repair.

## Mathematics, rules, and exact data

- Preserve the printed notation rather than converting it to an equivalent modern notation.
- Inline math uses `$...$` and display math uses `$$...$$` only when Stage 7 proves the representation is unambiguous and lossless for the source region.
- When dollar delimiters would be ambiguous or the source uses layout not expressible losslessly, retain a typed raw/HTML math block selected by Stage 7; never guess a formula to satisfy a parser.
- Delimiters are generated structure only when provenance maps the enclosed token sequence exactly to the witness.
- Rule tables, state tables, sequences, coordinates, colors, seeds, and numeric values are protected semantic data. Every changed token is high risk.

## Raw HTML

- Preserve verified authorial HTML-like source text as author text.
- Generated HTML must carry a reserved `data-ankos-generated` attribute or use one of the reserved anchor/page-marker forms.
- Sanitization is a render-layer operation. It must not rewrite the canonical Markdown payload.
- Scripts, event attributes, or network-loading embeds are never generated. If present as literal source material, they are rendered inert while their canonical transcription remains separately typed.

## Images, figures, and captions

- Canonical image links use repository-relative POSIX paths to manifest-governed assets under `ASSETS/`.
- The link target is generated path metadata; asset reference order and the source caption are authorial evidence.
- Do not invent authorial alt text. If the printed source supplies no equivalent text, canonical Markdown uses empty alt syntax and `EDITORIAL/Alt-Text.md` carries generated accessibility text with review status.
- One printed figure may contain multiple governed assets. Figure grouping and component order live in `figure-caption-asset-ledger.jsonl` and require page evidence.
- Do not infer caption ownership from filename page numbers or proximity.
- Byte-identical legacy assets are copied without recompression or metadata rewriting. Witness-only replacements/full plates require lawful provenance and a distinct asset ID.

## Page furniture and page breaks

- Printed running heads, page numbers, and other furniture remain author text only when the edition treats them as content required for faithful transcription; otherwise record them as an evidenced, independently reviewed non-authorial exclusion.
- Page boundaries are generated metadata tied to the witness page census. They do not create blank author paragraphs.
- Hyphenation across a page or column break is never repaired mechanically. Each author-text join or preserved hyphen needs per-occurrence witness evidence.

## Index

- Reconstruct Index entries from authoritative page columns in printed order.
- Represent entry, subentry, page range, and `see`/`see also` hierarchy without deriving content from body search.
- Generated anchors and links may augment entries but never replace printed page references or alter entry order.
- A representation that cannot preserve multi-column order and indentation exactly is rejected rather than flattened.

## Derived aggregate

`DERIVED/A-New-Kind-of-Science.md` is generated only from the ordered 29 canonical payloads in the same clean build. It is never build input.

The aggregate may add reserved generated separation markers between documents. After removing typed generated markers, its author-text projection must equal the concatenated canonical projections exactly. It has its own image-reference count and is excluded from canonical exactly-once counts.

## Editorial and search outputs

- `EDITORIAL/Errata.md` records apparent source errors without changing canonical author text.
- `EDITORIAL/Alt-Text.md` records generated accessibility descriptions.
- `SEARCH/**` may normalize spelling, hyphenation, Unicode, or tokenization only as an explicitly lossy derivative with links back to canonical spans.
- None of these overlays may target `CANONICAL_AUTHOR_TEXT`.

## Mechanically permitted transformations

Before witness-backed author-text repairs begin, automation may only:

- partition immutable raw blocks at independently verified boundaries;
- add/remove manifest-typed document envelopes, anchors, page markers, and block separators;
- rewrite image paths while preserving reference identity and order;
- assemble/disassemble the derived aggregate;
- copy governed assets byte-for-byte;
- enforce the generated-file LF policy.

Every operation needs exact input guards, expected counts, provenance, an inverse, and mutation coverage. No mechanically proven operation may change an author-text token or source-significant layout.

## Fail-closed behavior

The serializer refuses:

- stale hashes, nonunique preimages, or ambiguous insertion anchors;
- an unknown role, profile version, repair class, or generated namespace;
- author-text output not accounted for by raw provenance or a witness-backed insertion;
- editorial/search overlays aimed at canonical author text;
- use of an existing repaired tree as input;
- a nonempty unowned publication target;
- unresolved source or independent-review requirements.

Parser success and attractive rendering establish only structural properties. Fidelity remains a page-witness and provenance claim.

## Stage 7 validation obligation

Stage 7 must create and visually inspect fixtures for prose reflow, source hyphens, page furniture, nested/delimiter-heavy math, Wolfram code, rule/data tables, raw HTML, multi-component figures/captions, and multi-column Index entries. It must prove forward/inverse projection and mutation failures for each. A required profile change reopens this contract and all dependent zero-repair stages.
