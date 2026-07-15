# 4-PIPELINE

Status: IN_PROGRESS

Dependencies:

- Stage 1 guardrails and compatibility baseline: COMPLETE.
- Stage 2 raw manifest, segment/block ledger, held-out set, and baseline lock: COMPLETE.
- Stage 3 witness schema and source-gap state: frozen; primary witness remains `SOURCE_BLOCKED`.

## Current Facts

- The immutable input remains the explicit 19-Markdown/1,444-JPEG allowlist under `ref/A-New-Kind-of-Science/`.
- `ref/A-New-Kind-of-Science-Repaired/` exists as an empty publication target. Stage 4 builds only into fresh temporary/staging roots; Stage 42 owns publication.
- The frozen monolith is 3,780,628 bytes, 22,498 logical lines, and SHA-256 `55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20`.
- Stage 2 supplies 29 proposed canonical segments and 20,430 contiguous raw blocks. Their page-level semantic authority is still pending Stage 3/5 witness closure.
- Stage 3 authorizes zero canonical token changes, witness-only insertions, witness assets, audit certification, or full-repair claims. Dependency-independent schema, pipeline, projection, inverse, and synthetic mutation work is allowed.
- The zero-repair projection tape is deliberately outside `ANKOS-AST-1`: `SOURCE_BLOCK` means opaque byte preservation, not a verified heading, formula, code block, figure, caption, or Index entry.
- A fresh hostile review found and reopened three implementation areas before Stage 4 closure: caller-minted synthetic overlay authority, weak cross-ledger/schema joins, and output-promotion/tool-provenance races. These findings are being fixed and mutation-locked rather than waived.

## Updated Assumptions

- A zero-repair compiler can partition the frozen byte stream without promoting Stage 2 lexical guesses to verified semantics.
- Builder and conservation verifier must be implementation-independent and externally hash-bound; dynamically recording whichever tools happen to run is not a trust root.
- A frozen dataclass and an unkeyed receipt chain provide exact in-process integrity, not external authenticity. Production applicability requires a registry bridge joined to actual baseline, witness, repair, and review rows.
- Atomic staging promotion is available only when the platform supplies a true no-replace rename primitive. A check followed by ordinary rename is not an acceptable fallback.
- Stage 4 can complete while the primary witness is source-blocked only if the production gate categorically refuses canonical authority and every witness-dependent release state remains impossible.

## Big Picture Objective

Implement the deterministic, reversible repair-overlay pipeline, strict ledgers/schemas, production registry boundary, independent conservation verifier, zero-repair compiler, and hostile mutation suite before changing any author text.

## Detailed Implementation Plan

- Freeze closed schemas for repair/workflow, AST nodes, provenance, unresolved items, technical spans, figures/assets, navigation, review, compatibility, corpus manifests, and release manifests.
- Validate record semantics across the frozen Stage 1–3 contracts: raw path/hash/span/block joins, role separation, workflow/final-disposition applicability, evidence and mechanical-proof requirements, risk-union derivation, reviewer independence/disagreement closure, and release/source-blocked gates.
- Implement guarded replace, delete, move, split, merge, and unique two-sided anchored insertion operations with exact target/block/preimage/count/adjacency hashes, dependency ordering, and inverse replay.
- Keep synthetic operation fixtures separate from production application. Production authority must come only from a bridge that reconstructs the actual 29-document/20,430-block state and validates exact baseline/witness/repair/review registry rows.
- Build a zero-repair staging tree from the frozen monolith and Stage 2 segment/block ledger. Emit 29 opaque canonical projections plus one typed/removable Colophon terminal LF; never read a prior output tree as input.
- Independently derive expected documents, tape rows, manifest, inverse stream, and tree inventory without importing compiler bookkeeping.
- Freeze implementation/tool hashes under an externally pinned lock and prove that the declared verifier is the verifier actually executed.
- Construct in a private same-filesystem tree, verify it, recheck an inode/stat/hash receipt, and promote only with descriptor-anchored atomic no-replace rename. Fail closed when that primitive is unavailable.
- Mutation-test stale inputs, wrong counts/anchors/dependencies, role leakage, fake evidence/reviews, source-blocked authority, raw/lock/tool drift, missing/reordered/changed blocks, self-consistent manifest forgeries, unsafe paths, symlinks/hardlinks/modes, target races, directory substitution, post-validation mutation, and comparator late entries.
- Freeze a Stage 4 implementation/proof lock only after independent hostile reruns close every finding.

## No-Cheating Checks

- Recompute the explicit legacy allowlist and Stage 1–3 external locks before accepting any Stage 4 proof.
- Reject recursive discovery that can include the repaired sibling and reject the legacy root, its descendants, the repaired sibling, or prior output as a build target/input.
- Keep the sibling empty and compare its state before/after every Stage 4 full verification.
- Refuse every canonical operation while `witness-state.json` is `SOURCE_BLOCKED`, including caller-supplied booleans, fabricated hashes, and synthetic test authority.
- Treat the current split Markdown, local JPEGs, model output, parsing, rendering, and mathematical/program plausibility as nonauthorizing diagnostics.
- Require the production bridge to reconstruct target IDs, paths, block bytes, spans, and row hashes from the frozen Stage 2 artifacts rather than trusting caller-created objects.
- Require source and specialist reviewers to be distinct from the creator and from one another where specialist review is required; bind exact closed review-row hashes and evidence-view hashes.
- Derive high risk from the frozen union of repair class, validated operation tags, and validated AST impact; do not allow caller downgrades or blanket specialist overclaiming.
- Verify forward and inverse results from raw inputs through an independent implementation, and externally bind the ordered operation/receipt/tool records before treating them as release evidence.
- Leave every witness region and authorial ambiguity explicitly blocked; do not create a repair ledger row merely to make coverage totals look complete.

## Completion Requirements

- [ ] All Stage 4 schemas are closed, externally locked, root/relocation safe, duplicate-key safe, and semantically mutation-tested.
- [ ] Raw, witness, repair, provenance, review, technical, figure, navigation, compatibility, corpus, and release records fail closed on missing/forged joins and on the current source-blocked state.
- [ ] The production registry bridge reconstructs only the frozen 29 document targets/20,430 blocks and refuses all current canonical authority.
- [ ] Replace/delete/move/split/merge/anchored-insert primitives pass exact guard, dependency, target-role, evidence, risk, review, inverse, and mutation tests in normal and optimized modes.
- [ ] Production `apply_overlays` cannot execute with test-only authority; synthetic fixtures use a separate private path.
- [ ] Two fresh zero-repair builds are byte-identical, contain exactly 29 canonical projections and 20,431 tape rows, and recover the exact monolith under independent inverse replay.
- [ ] The independent verifier is executed from its locked declared path and does not import compiler bookkeeping.
- [ ] Atomic no-replace promotion, identity-safe cleanup, validation-to-promotion receipt recheck, and strict full-tree comparison survive hostile race/type/link mutations or fail closed when unsupported.
- [ ] Validators/tests pass from repository root and `/tmp`, offline/relocated/no-Git/read-only-input fixtures, and `python3 -O` where applicable.
- [ ] A Stage 4 implementation/proof lock externally binds every accepted schema, tool, test, contract, and stable proof digest without a circular self-hash.
- [ ] Applicable Stage 1–3 validators, direct whitespace checks, `git diff --check`, scope inspection, legacy hashes, and sibling-emptiness checks pass.
- [ ] No repair record or generated output has altered author text, and no Stage 4 artifact claims witness coverage or release certification.

## Stage Results

IN_PROGRESS. The following are implemented but remain subject to the final lock and hostile closure:

- strict pipeline schemas and semantic validation;
- document-specific guarded overlay primitives and exact inverse receipts;
- an opaque zero-repair compiler and separately implemented conservation verifier;
- private-tree transactional construction and mutation suites;
- current source-blocked witness/permission gates.

Open closure work:

- finish and independently rerun the schema/ledger hardening;
- finish the actual registry-to-authority bridge and prove current categorical refusal;
- close zero-repair tool identity, no-replace, cleanup-identity, validation/promotion, and comparator race findings;
- freeze the outer Stage 4 implementation/proof lock;
- run the full normal/optimized/relocated verification matrix and record exact hashes/results here and in `0-plan.md`.
