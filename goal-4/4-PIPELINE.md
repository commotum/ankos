# 4-PIPELINE

Status: IN_PROGRESS

## Objective

Implement the deterministic, reversible repair-overlay pipeline and validators before changing any author text. The first product is a zero-repair staging build derived only from the frozen legacy manifest and Stage 2 segment/block identities.

The publication target is the new, currently empty sibling `ref/A-New-Kind-of-Science-Repaired/`. Stage 4 constructs and verifies releases under a Goal 4 staging area; Stage 5 owns publication of the correctly partitioned 29-document zero-repair skeleton. The legacy folder remains immutable.

## Current Gates

- Stage 1 guardrails: COMPLETE.
- Stage 2 baseline: COMPLETE.
- Stage 3 witness schema: frozen; primary witness `SOURCE_BLOCKED`.
- Author-text token changes: forbidden.
- Witness-only insertions/assets: forbidden.
- Structural zero-repair serialization and reversible pipeline work: allowed.

## Planned Stage 4 Outputs

- strict schemas for repairs, workflow state, provenance, structure, unresolved items, technical queues, figures, navigation, review, compatibility, and release metadata;
- guarded replace/delete/move/split/merge and two-sided anchored insertion primitives;
- dependency ordering, target-role separation, forward build, inverse replay, and atomic publication support;
- a zero-repair staging build with exact raw author-text projection and no witness-dependent claims;
- independent validators for hashes, joins, role counts, source/evidence gates, reviewer independence, and generated/editorial/search separation;
- mutation fixtures for stale preimages, occurrence drift, missing/reordered blocks, leakage, symbol changes, unsafe paths, assets, captions, links, and anchors.

## Immediate Work

Freeze the Stage 4 machine schemas and operation semantics, then implement a minimal zero-repair compiler against synthetic fixtures before applying it to the 20,430-block corpus. No canonical author-text output will be published until forward/inverse conservation and target ownership pass.
