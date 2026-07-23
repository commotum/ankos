# 2-CORPUS-MAP

Status: **COMPLETE**.

## Current Facts

- Stage 1 guardrails validate and the blind phase remains active.
- `Contents.md` contains exactly 29 unique ordered book-document links.
- The physical source tree contains exactly 1,638 files:
  - 29 book documents;
  - 2 navigation documents;
  - 1,607 JPEG images;
  - 0 other files.
- The 29 book documents contain 38,168 physical/logical Markdown lines.
- Deterministic structural partitioning yields 14,311 source units.
- The 31 Markdown files contain 1,344 local Markdown links:
  - 1,314 image references;
  - 30 document links;
  - 0 broken links.
- The 1,314 image references resolve to 1,314 distinct physical images.
  Another 293 physical images are intentionally retained in the inventory as
  `UNREFERENCED_PHYSICAL`; they have no live Markdown owner and remain mandatory
  Stage 3 asset rows and visual-screening obligations rather than being silently
  discarded.

## Updated Assumptions

- The inherited 22,498-line logical map was not the current canonical physical
  Markdown line map. Independent parsing establishes 38,168 lines; the plan now
  records the actual document spans.
- Blank-line paragraphs alone were too coarse for the Index. Top-level list
  items, numbered list items, and headings are structural source-unit
  boundaries; indented Index subentries remain with their owning headword.
- Navigation files belong in the source manifest and link checks but are not
  book-text source units.
- Unreferenced physical images are inventory obligations, not evidence of a
  broken link or permission to infer an owner.

## Big Picture Objective

Create a deterministic, independently verified corpus map that accounts for
every canonical file, byte, line, source unit, document/image link, physical
image, document order, and chapter↔Notes pairing without performing taxonomy
discovery.

## Allowed Inputs And Scope

Allowed:

- canonical `README.md` and `Contents.md`;
- all canonical Book Markdown files as bytes/structural Markdown;
- all canonical image files as paths/bytes/hashes;
- Stage 1 guardrails and Stage 2 tools/artifacts.

This stage parsed structure and links but did not disposition construction
content, search for mechanisms, create candidates, or inspect the current
catalog/API/runtime.

Writes were limited to `goal-4/`.

## Source Coverage

### Ordered documents

The manifest records all 29 documents in exact `Contents.md` order and assigns:

- canonical order and title;
- semantic-neutral document kind;
- chapter number where applicable;
- bytes, lines, SHA-256, and global line span;
- deterministic source-unit IDs;
- local link IDs and image-reference paths.

Twelve chapter↔Notes pairs are explicit and independently verified.

### Source-unit partition

Each source unit records:

- stable `U000001`-style ID in canonical order;
- document path/order;
- block kind;
- half-open byte range;
- inclusive document and global line ranges;
- SHA-256 of the exact byte slice.

Units split on blank-delimited blocks, headings, and top-level bullet/numbered
items while preserving fenced-code blocks and indented subitems. The verifier
uses a separately implemented parser and proves that ordered unit ranges cover
every document byte and line exactly once with no gap or overlap.

### Images and links

Every JPEG row records physical path, bytes, hash, reference count, reverse
references, and either `REFERENCED` or `UNREFERENCED_PHYSICAL`. Every Book link
is joined to its containing source unit. Navigation links intentionally have no
source-unit ID.

Starting counts were zero generated units/assets. Ending structural counts:

- source units: 14,311;
- image rows: 1,607;
- link rows: 1,344;
- image-reference rows: 1,314;
- chapter↔Notes pairs: 12.

No cross-reference or candidate queue was opened; page/section semantic routes
begin only during reading stages.

## Candidate Changes

No candidate was created, linked, merged, split, mapped, or classified.

## Search And Evidence Log

No construction vocabulary search was run. Structural inspection was limited
to:

- parsing the 29 explicit navigation entries;
- locating all Markdown links/images;
- detecting headings, fences, blank blocks, and top-level list items;
- hashing and range accounting.

The Index's Markdown shape was inspected only to establish that top-level
headwords require individual units. No Index term was treated as evidence or
used to seed discovery.

## Detailed Implementation Plan

Completed:

1. Added `tools/build_corpus.py`.
2. Generated `corpus-manifest.json`.
3. Generated `source-units.jsonl`.
4. Added an independent verifier in `tools/verify_corpus.py`.
5. Added focused and relocation tests in `tools/test_corpus.py`.
6. Corrected the inherited line map in `0-plan.md`.

Canonical digests:

- source-tree aggregate:
  `b642dbded84170a0c3872622a19b55f6dc0ee4f5f7aff843e18eee175c85e62c`;
- concatenated 29-document text:
  `ec7f22f801d157076d33446f2fb5ee01dadaa6b18f3e89d0a123acc0000f2725`;
- generated source-unit JSONL:
  `8fe1e47076bf17b414c845f00d4cdc8637d8c248c5f2381d6cebd5c32ac2f261`.

## No-Cheating Checks

- The independent verifier does not import the builder.
- Physical file counts and Contents targets are independently enumerated.
- A separate structural parser reproduces every source-unit range.
- Document/image sets, hashes, bytes, line spans, link targets, unit joins,
  reverse image joins, navigation records, and chapter pairs are rederived from
  source rather than trusted from the manifest.
- Candidate and reading-ledger artifacts still do not exist.
- No current taxonomy/API/runtime input was opened for semantic content.

## Completion Requirements

| Requirement | Evidence |
|---|---|
| Account for 29 book documents, 2 navigation documents, and 1,607 images | Physical enumeration and exact manifest-set equality |
| Cover every byte and line exactly once | 14,311 ordered unit slices reproduced by independent parser |
| Resolve every document/image link | 1,344 independently reparsed links, zero broken |
| Reconcile physical images and references | 1,314 referenced plus 293 explicitly unreferenced rows equals 1,607 |
| Machine-verifiable order and ownership | Contents order, unit IDs, link/unit joins, reverse image joins, 12 chapter↔Notes pairs |
| Independent verification and mutation checks | Separate verifier, six destructive mutations, optimized run, and relocated-copy test |

## Stage Results

Commands and outcomes:

```text
python3 goal-4/tools/build_corpus.py
  built corpus artifacts: documents=29 images=1607 units=14311 lines=38168

python3 goal-4/tools/verify_corpus.py --self-test
  verified corpus map and mutation checks:
  documents=29 images=1607 units=14311

python3 goal-4/tools/build_corpus.py --check
  corpus artifacts reproduce exactly

python3 -O goal-4/tools/verify_corpus.py --self-test
  passed with identical counts

python3 -m py_compile ...
  passed silently

uv run pytest -q goal-4/tools/test_guardrails.py goal-4/tools/test_corpus.py
  7 passed

git diff --check -- goal-4
  passed silently
```

Mutation checks prove failure on:

- a missing document;
- a corrupt source-unit range;
- a missing source-unit row;
- a missing physical-image row;
- a stale/broken link record;
- a stale source-unit-file digest.

The focused suite also runs the copied verifier and copied artifacts against a
hard-linked relocated source tree from an unrelated working directory.

Re-integration answers:

1. The inherited line-map convention was incorrect for the canonical files and
   has been replaced.
2. No construction vocabulary/route was introduced.
3. No candidate changed.
4. Every structural unit, local link, and physical image is governed by the
   manifest; semantic reading/image queues begin in Stage 3.
5. The 293 unreferenced physical images remain explicit ownership unknowns, not
   semantic ambiguities.
6. Reuse was not evaluated.
7. Stage 1 remains closed.
8. Corpus counts and line-map assumptions changed as recorded.
9. The audit remains blind to preferred taxonomy count and API outcome.
10. Exact next stage: `3-AUDIT-HARNESS`, using these immutable source-unit,
    link, and image identities to create allowlist-only ledgers and validators.
