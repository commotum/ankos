# 1-CUTOVER

## Current Facts

- The repaired canonical Book contains 29 discovery documents, 14,311 mapped
  source units, and the extracted figures needed by later selective review.
- The inherited raw store contains 1,488 unique leads.
- Every inherited lead names at least one opaque source-unit ID.
- A data-only source-unit map translates those IDs to canonical document and
  line ranges.
- Before this stage, Goal 5 contained only its plan, loop, and continuation
  prompt.

## Updated Assumptions

- The inherited count of 1,488 leads is confirmed.
- The source anchors can be translated without using predecessor judgments,
  reports, tools, histories, or verification machinery.
- A five-column CSV is sufficient to preserve discovery coverage without
  importing semantic conclusions.
- Earlier bookend and Chapter 1–7 coverage remains an accepted starting fact;
  Chapter 8 receives a fresh compact closure next.

## Big Picture Objective

Establish Goal 5 as the clean, lean completion contract and preserve prior
discovery through a compact, conclusion-free source bridge.

## Detailed Implementation Plan

- Confirm the Goal 5 scaffold and canonical Book documents.
- Stream only inherited lead IDs and source-unit IDs.
- Translate source-unit IDs through the data-only source map.
- Derive line ranges and surface triggers directly from canonical Markdown.
- Write `raw-leads.csv` with:
  `lead_id`, `inherited_id`, `canonical_anchors`, `surface_trigger`, and
  `status`.
- Create the heading-level baseline in `coverage.md`.
- Verify counts, uniqueness, status values, and a deterministic anchor sample.
- Confirm repository changes remain confined to Goal 5.

## No-Cheating Checks

- No inherited candidate name, alias, fingerprint, parameter, variant,
  disposition, confidence score, evidence claim, or uncertainty appears in
  `raw-leads.csv`.
- No predecessor plan, stage report, history, search archive, route data,
  validator, helper, or generated accepted output is a Goal 5 input.
- The field projector reads only inherited lead ID/source-unit ID pairs and the
  data-only source map.
- Surface triggers come from canonical Markdown at the mapped line ranges.
- No paragraph-level negative ledger, replay system, or generalized validation
  framework was created.

## Completion Requirements

- The clean context boundary is explicit in the Goal 5 plan and this stage
  result.
- Exactly 1,488 inherited leads appear once each in `raw-leads.csv`.
- Goal 5 IDs and inherited IDs are each unique.
- All initial statuses are `UNREVIEWED`.
- Canonical source anchors resolve, and sampled surface triggers exactly match
  their source ranges.
- `coverage.md` accounts for all 29 discovery documents at heading level.
- Earlier artifacts and all non-Goal-5 files remain unchanged.
- `git diff --check` passes and Goal 5 remains compact.

## Stage Results

- Projected 1,488 leads into a five-column CSV containing no inherited
  judgments.
- Verified 1,488 unique Goal 5 IDs, 1,488 unique inherited IDs, and 1,488
  `UNREVIEWED` statuses.
- Verified the complete data-only mapping of 14,311 source units across 29
  canonical documents.
- Deterministically checked the first, middle, and last lead anchors and
  confirmed their surface triggers exactly match canonical Markdown.
- Created a 29-document heading-level coverage map. Chapter 8 and its Notes are
  explicitly next; Chapters 9–12 and the Index remain pending.
- The raw register is approximately 532 KB. Goal 5 remains a compact
  human-readable working set.
- No earlier artifact was modified. Goal 5 now supersedes every earlier
  unfinished taxonomy-audit completion contract.
- Next: Stage 2, `CH08-CLOSE`.

