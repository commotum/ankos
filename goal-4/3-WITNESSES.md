# 3-WITNESSES

Status: SOURCE_BLOCKED

## Outcome

Stage 3 froze a complete witness schema and an exact source-gap state without acquiring, retaining, or fabricating a primary witness. Every one of the 29 proposed canonical documents and all 20,430 frozen raw blocks is explicitly represented by a `SEGMENT_SOURCE_GAP` row. No row claims a page, region, transcription, legibility result, independent review, or authorized repair.

Dependency-independent Stage 4 pipeline work may proceed. Every witness-dependent author-text correction, visual completeness decision, Index-column reconstruction, audit certificate, and unqualified full-repair claim remains blocked.

## Official Source Findings

The [official NKS Online edition](https://www.wolframscience.com/nks/) exposes page-numbered semantic HTML, responsive full-page images, and official section/chapter PDFs. The [official copyright leaf](https://www.wolframscience.com/nks/piv--copyright/) identifies the rendered book as Wolfram Media, copyright 2002, First edition, Fourth printing. The hardcover identifiers recorded for the target are ISBN-10 `1-57955-008-8` and ISBN-13 `978-1-57955-008-0`.

The public surface is useful but not a complete fixed-layout witness:

- semantic HTML is reflowed and cannot establish printed geometry;
- responsive page images may be inadequate for fine formula, code, or typographic distinctions;
- official chapter/section PDFs preserve fixed layout but no official public whole-book PDF or EPUB was identified;
- the public [Index](https://www.wolframscience.com/nks/index/0/) is reflowed HTML, and no public fixed-layout Index witness was identified;
- covers, inner covers, endpapers, blanks, full physical leaves, inserts, plates, foldouts, trim, bleed, and spread treatment have not been proven complete;
- official URLs are mutable locators, not content-addressed witness identities;
- equivalence between the official online printing and the local OCR lineage remains unproven.

Official count statements also remain deliberately unreconciled. The [Wolfram Media product page](https://www.wolfram-media.com/products/nks/) and the [official Colophon](https://www.wolframscience.com/nks/colophon/) state 1,280 pages; the [official citation page](https://www.wolframscience.com/nks/citation/) states 1,197 pages; and the Colophon begins at printed page 1264. These claims use undefined or differing scopes and are not a lawful physical/digital census.

## Licensing State

The official surface is recorded as `REMOTE_INTERACTIVE_ONLY` for bounded planning inspection. Complete bulk acquisition, hashing, archiving, or AI-assisted review is `USE_NOT_AUTHORIZED`, and the complete primary witness remains `NOT_ACQUIRED`.

The relevant official layers are:

- the [book copyright page](https://www.wolframscience.com/nks/piv--copyright/), which reserves full-text and illustration reproduction beyond its narrow provisions;
- the [Wolfram Science terms](https://www.wolfram.com/legal/terms/wolfram-science.html), which require advance permission for bulk reproduction, mirroring, or archiving;
- the [current general Wolfram terms](https://www.wolfram.com/legal/terms/wolfram/), which prohibit scraping, bulk downloading, and use with AI-powered tools absent a separate license.

A Creative Commons icon in a page footer has no adjacent scope statement that overrides these explicit terms. Public reachability and robots permission are not treated as copyright, archival, derivative, or AI-use authorization.

No official PDF, page raster, crop, site mirror, full-page transcription, credential, cookie, token, or private mount path was committed or retained.

## Frozen Artifacts

- `witness-contract.json` freezes target identity, source/unit/content classes, region and legibility semantics, `NOT_APPLICABLE` reasons, held-out blinding, storage restrictions, and stage gates.
- `witness-source-registry.json` records the official candidate, bounded public sentinels, count conflicts, permission evidence URLs, limitations, and exact unblock action.
- `witness-state.json` records the current `SOURCE_BLOCKED` acquisition, whole-corpus scope, five open blockers, and the limited permission for dependency-independent pipeline work.
- `witness-mount-contract.md` defines an external, read-only, credential-free, offline audit interface for a future authorized witness.
- `witness-region-ledger.jsonl` contains exactly 29 ordered segment source-gap rows whose block counts and ID hashes independently rederive all 20,430 blocks.
- `witness-unresolved.jsonl` contains four release-blocking unresolved records for acquisition, permission, edition identity, and physical/region census.
- `witness-lock.json` binds the Stage 3 artifacts, generator, validator library, tests, and all Stage 1/2 prerequisite hashes. Its externally pinned SHA-256 is `f348e4dd0ebf328c48066696eb70359d954e07cbdfd7b7fd827286e3268ba449`.
- `tools/capture_witness.py` deterministically regenerates the two ledgers and internal lock.
- `tools/validate_witness.py` enforces the external lock root, all source-gap and license gates, and absence of witness-like binary payloads.
- `tests/test_witness.py` contains 30 normal/optimized mutation tests.

## Exact Blockers

1. `WITNESS-PERMISSION`: no written or separate license covers the required bulk or AI-assisted acquisition, storage, comparison, retention, and derivative handling.
2. `WITNESS-COMPLETE-CENSUS`: no authorized complete edition-identical object or physical-surface census exists.
3. `WITNESS-INDEX-LAYOUT`: no authorized fixed-layout evidence establishes the printed Index columns.
4. `WITNESS-EDITION-MATCH`: the official online printing has not been proven identical to the local OCR lineage.
5. `WITNESS-INDEPENDENT-REVIEW`: no human transcriber/specialist/independent-review assignments or blind held-out adjudications exist.

The affected scope is exact: 29 segments, 20,430 raw blocks, 1,444 legacy visual candidates, and 1,125 frozen held-out items.

## Unblock Path

Obtain written permission from `ip@wolframscience.com` for a complete official born-digital witness or authorized bulk access, explicitly covering private storage, automated or AI-assisted fidelity review, retention, bounded evidence artifacts, and derivative/redistribution limits. Alternatively, supply a separately licensed complete edition-identical witness whose terms cover the same operations.

After authorization, Stage 3 must reopen and:

- fingerprint edition/printing identity;
- independently census physical and digital units without forcing a stated count;
- reconcile covers, endpapers, leaves, blanks, pages, plates, inserts, foldouts, page boxes, and Index leaves;
- partition every unit into total nonoverlapping regions;
- record per-axis legibility and independently reviewed non-authorial exclusions;
- freeze blind held-out evidence packets and human reviewer assignments;
- run tamper, missing, duplicate, reorder, crop, swap, terms-drift, and mount-safety mutations.

## Verification Results

- `python3 goal-4/tools/validate_witness.py`: PASS
- `python3 -O goal-4/tools/validate_witness.py`: PASS
- `python3 -m unittest goal-4/tests/test_witness.py`: 30 PASS
- `python3 -O -m unittest goal-4/tests/test_witness.py`: 30 PASS
- `python3 goal-4/tools/capture_witness.py --check`: PASS
- forbidden witness-like payload scan: zero findings
- primary witness units/regions acquired: zero
- author-text repairs authorized by Stage 3: zero

Stage 3 is therefore honestly `SOURCE_BLOCKED`, not incomplete by accident and not falsely complete. Stage 4 may implement reversible schemas, overlays, zero-repair construction, and synthetic fixtures; it may not change author text or claim witness coverage.
