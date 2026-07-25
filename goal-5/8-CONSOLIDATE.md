# 8-CONSOLIDATE

## Current Facts

- The register contains 1,563 raw leads.
- Current statuses are 81 `SERIOUS`, 33 `RESOLVED`, 19 `WEAK`, and 1,430
  `UNREVIEWED`.
- Of the unreviewed rows, 1,413 are inherited pre-Chapter-8 leads and 17 are
  explicit later dependencies from Chapters 8–12.
- All chapters and Notes have now been read, so those dependencies can be
  resolved during mechanics consolidation.

## Updated Assumptions

- Most inherited leads will collapse into presets, seeds, observers, properties,
  examples, aliases, or repeated evidence for a much smaller number of
  mechanics clusters.
- The 180-character Book-derived trigger is sufficient for obvious cheap
  dispositions; ambiguous or serious cases require inspection of their
  canonical anchors.
- Four non-overlapping batches can classify inherited leads without duplicate
  source reading.

## Big Picture Objective

Map every raw lead to a mechanics cluster or concise non-construction
disposition, then create full fingerprints only for the resulting serious
candidate clusters.

## Detailed Implementation Plan

- Classify inherited leads in four disjoint batches:
  `L0001–L0320`, `L0321–L0656`, `L0657–L1069`, and `L1070–L1413`.
- For each lead, use the compact trigger first and inspect canonical anchors
  only when the status or mechanics are genuinely ambiguous.
- Emit one ephemeral row per lead with ID, status, concise mechanics cluster,
  and short reason; validate exact batch coverage.
- Resolve the 17 later dependencies from Chapters 8–12 against the now-complete
  source discoveries.
- Merge aliases and repeated descriptions across all batches and newer serious
  leads.
- Update `raw-leads.csv` statuses.
- Create `source-decision-matrix.csv` with one terminal mapping per raw lead.
- Create `candidates.md` with full fingerprints only for serious mechanics
  clusters, retaining representative lead IDs and canonical anchors.
- Delete ephemeral batch files after the verified merge.

## No-Cheating Checks

- Keep discovery blind to T01–T45, the proposed API, runtime, and prior-goal
  material.
- Do not ask two readers to classify the same lead range.
- Do not open predecessor candidate prose or fingerprints.
- Do not write a full fingerprint for a weak, resolved, or duplicate lead.
- Do not preserve intermediate model chatter, raw prompts, or batch histories.
- Do not treat a Book name, application, visual pattern, or property as a
  mechanics cluster without executable or relation-defining evidence.

## Completion Requirements

- Every `L0001–L1563` row has exactly one terminal mapping.
- Batch ranges are complete, disjoint, and validated before merge.
- Every serious candidate cluster has a full semantic fingerprint,
  representative canonical anchors, and a distinguishing question or example.
- Every weak/resolved lead has only a concise category/reason.
- Aliases and repeated evidence do not create duplicate candidates.
- All 17 later dependencies are resolved or remain explicit serious
  uncertainties with the missing decision stated.
- `raw-leads.csv`, `source-decision-matrix.csv`, and `candidates.md` agree on
  status and membership.
- No ephemeral batch file remains.
- Changes remain confined to Goal 5, `git diff --check` passes, and artifacts
  remain compact.

## Stage Results

- Classified the 1,413 inherited leads in four disjoint ranges. The raw
  source-row result was 106 serious, 822 resolved, 485 weak, and zero
  unreviewed.
- Resolved all 17 later dependencies after Chapters 8–12 were available:
  seven remained serious mechanics, eight collapsed into already represented
  mechanics, and two lacked an executable rule.
- Split the two overpacked Chapter 8 source groups before final membership.
  Crystal-growth material became DLA, its conserved-particle CA realization,
  and a continuous boiling CA; fracture material became a minimum-path
  relation, spring-failure dynamics, a CA preset, and stochastic binary
  fragmentation.
- Merged exact or mechanically parameterized aliases before fingerprinting,
  including numeric map variants, synchronous local-state automata, block
  automata, independent substitutions, stochastic CA, differential-equation
  variants, local constraints, register-machine variants, tag variants, and
  finite codecs.
- Final hostile review corrected one weak lead (sorting networks) to serious,
  added one source-anchored priority-construction lead, and split the bundled
  codec fingerprint along its seven already recorded mechanics. The terminal
  register now contains 190 serious source leads, 867 resolved leads, and 507
  weak leads. They form 102 directly reviewable mechanics candidates with
  complete fingerprints.
- Created `candidates.md` and `source-decision-matrix.csv`. Every `L0001–L1564`
  row has one terminal status and decision; every serious row maps to exactly
  one candidate; candidate IDs and matrix membership agree.
- Deleted the four ephemeral batch files after validating exact, disjoint
  coverage. No predecessor taxonomy, catalog, API, or runtime material was
  opened.
- Structural checks and `git diff --check` passed.
