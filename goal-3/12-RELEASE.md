# 12-RELEASE

Status: COMPLETE

> **Historical release record.** The finished 29-document corpus is the
> repository's canonical source at `ref/A-New-Kind-of-Science/`. This work was
> executed as Goal 5 before being re-indexed as completed Goal 3, so later
> Goal 5 references in this release record are historical. Its build machinery
> and intermediary evidence remain recoverable from Git commit
> `bc4d240c9e12f73d11039f5f1a2a251e0174e804`.

## Big-Picture Objective

Release the corrected 29-document Markdown corpus with accurate generated
documentation, reproducible normal and zero-correction builds, zero open
transcription ambiguity, and final proof that the author-text/assets and legacy
corpus did not drift during release-only changes.

## Entry Facts

- Stage 11 is complete. Its wholly fresh final round covers 29 documents,
  1,280 PDF pages, 38,168 target lines, 812 detector runs, 35,479 candidates,
  and 1,314 live image references at zero finding and zero ambiguity.
- The stable author-text corpus is 3,622,684 bytes with concatenated SHA-256
  `ec7f22f801d157076d33446f2fb5ee01dadaa6b18f3e89d0a123acc0000f2725`.
- Before release-only documentation changes, the 1,636 generated author-text
  and image payload files (everything except generated `README.md` and
  `Contents.md`) have length-prefixed SHA-256
  `63d702f88f644df70158c1dbf31124bd56e9e2efa04325a8fbf754daf2bb8f61`.
- The pre-release full normal tree has length-prefixed SHA-256
  `a682973172db962f41e407f399090a7a0245a47163c550cdf35268054e331216`.
  Stage 11 binds the historical builder SHA-256
  `6399c819a4f4d485cd390eb14ba56d7cd8170095b3e517437aeacad0aa4cd16e`
  and this pre-release tree.
- The protected 1,463-file legacy tree must remain
  `b9ff7b9b507790f1d519593baf2b2d2f24dd6cd49dc0fe10f0ac629278ea42f4`.

## Implementation Plan

1. Make generated normal-release documentation state the completed review
   accurately and identify agent review without claiming human proofreading.
2. Give `--zero-corrections` its own explicit raw-diagnostic README so it
   cannot be mistaken for the corrected release.
3. Keep generated navigation visibly editorial and outside author text.
4. Add focused release assertions for the two README modes, coverage/reviewer
   state, record links, PDF-not-a-build-input behavior, and the release-only
   payload rebind.
5. Rebuild the published sibling, make two additional fresh normal builds and
   one fresh zero-correction build, validate them, and compare exact trees.
6. Recheck Markdown rendering, links, images, correction guards, unresolved
   state, source/PDF identity, the legacy digest, full tests, whitespace, Git
   scope, and ignored/untracked PDF state.

## Release-Only Rebind Rule

Changing the generated README/Contents implementation after Stage 11 changes
the builder and whole-tree hashes, so the Stage 11 builder/tree bindings become
historical rather than current. This does not restart author-text review only
if the release audit proves all 29 canonical documents and all 1,607 image
payloads byte-identical to the accepted Stage 11 tree and records the new
builder, validator, generated-document, normal-tree, and zero-tree hashes.

## No-Cheating Checks

- Never hand-edit generated output; rebuild it from preserved inputs.
- Never call the zero-correction projection a corrected or verified edition.
- Never claim human proofreading for agent work.
- Do not weaken “zero known ambiguity” or hide a failed release check behind a
  historical passing result.
- Do not treat the local PDF as a build input or redistribute it; it remains a
  pinned local review/validation witness.
- Do not accept matching normal trees without separately proving the raw
  zero-correction projection and the immutable legacy digest.

## Completion Requirements

- Stage 11 remains closed at `0/0`, and `unresolved.md` has no open author-text
  ambiguity.
- Generated normal and zero-correction documentation is accurate and
  mode-specific.
- Two fresh normal builds and the published sibling are byte-identical and
  validate; a fresh zero-correction build conserves the raw monolith and
  validates.
- All 29 documents, 1,607 release image payloads, links, generated contents,
  Markdown structure/rendering, guards, and coverage joins pass.
- The release-only payload rebind, protected legacy digest, ignored PDF state,
  focused tests, complete repository suite, `git diff --check`, and scope
  inspection pass.

## Stage Results

Completed on 2026-07-20 (America/Los_Angeles).

### Accurate Generated Documentation

- `build.py` now emits distinct normal-release and zero-correction README
  files. The normal README identifies the complete source-verified repair,
  agent review, absence of human proofreading, preservation of source-printed
  errors, local PDF boundary, exact commands, and compact Goal 5 records. The
  zero README identifies an uncorrected diagnostic projection and cannot be
  mistaken for the release.
- `Contents.md` remains an exact 29-link ordered navigation file and now labels
  itself generated editorial material rather than author text. All README and
  Contents links resolve in the published sibling.
- Final SHA-256 values are:
  - builder:
    `516e36510488c785bdcc7e5cd1775e6a88d9c8f170550ac37632089a5c5ae693`
  - validator:
    `2e84ed042d10a87c88475575c676b262de3149b0dc77c86e2e5aa9c7c408fe12`
  - corrected README:
    `e56e77f3b18695d927f568655e54a37c6558fcab33021d566f86b0a2bb175ed0`
  - zero-correction README:
    `830ed517ba9e4b28971fedfe2f08337d55c96182d878e58223f740c2d309fe72`
  - Contents:
    `ec0584ac69c23f629a483680ada74a4b56829f2ac016b1de48e79c32877c9f32`

### Release-Only Rebind

- Stage 11's builder SHA-256 `6399c819...` and normal-tree SHA-256
  `a6829731...` are retained as historical saturation bindings. Stage 12
  changed the generator only for mode-aware README/Contents output and release
  validation; it made no author-text, correction, image-map, added-asset, or
  coverage change.
- Before and after that change, the exact 1,636-file author-text/image payload
  tree (29 documents plus 1,607 images, excluding only generated README and
  Contents) is
  `63d702f88f644df70158c1dbf31124bd56e9e2efa04325a8fbf754daf2bb8f61`.
- The 29 ordered canonical documents remain 3,622,684 bytes and 38,168 LF with
  concatenated SHA-256
  `ec7f22f801d157076d33446f2fb5ee01dadaa6b18f3e89d0a123acc0000f2725`.
  This satisfies the release-only rebind without reopening source review.

### Deterministic Builds

- The published sibling and fresh builds
  `/tmp/g5-stage12-normal-a-20260720-a1` and
  `/tmp/g5-stage12-normal-b-20260720-a1` are byte-identical at 1,638 files.
  Their length-prefixed tree SHA-256 is
  `d3d2d96b6d4516e76f37b1fbf28c31f524a65d41f3799dbba15a06f17d340660`.
  Each validates as 29 documents, 1,607 images, 4,834 corrections, and 29
  completed second-pass rows.
- `/tmp/g5-stage12-zero-20260720-a1` validates at 29 documents, 1,444 images,
  zero corrections, and 29 completed coverage rows. Its 1,475-file
  length-prefixed tree SHA-256 is
  `45cadbc5af59dd0c23e7fd8599ef663385159c5ae4b69ca3a37bd5ca1166609e`.
  Its ordered document bytes are exactly the 3,780,628-byte immutable monolith,
  SHA-256
  `55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20`.
- The correction ledger remains 4,834 rows at SHA-256
  `0206a1f4e109293ef348d7435b075eb1a9a18a80523dcbde0cc11d25e23bb509`;
  coverage remains 29 `YES/YES` agent rows at SHA-256
  `3157e4a88f424796edf3d4cd5f909b1d7f7d335e230f872445db7361051ecee6`.

### Final Verification

- Default, both fresh normal, and fresh zero-correction validation pass. Exact
  directory comparison reports no difference between the two fresh normal
  builds or between either one and the published sibling.
- CommonMark parsing/rendering passes all 31 Markdown files: 3,627,415 source
  bytes, 123,253 tokens, 3,915,770 rendered HTML bytes, and render-record
  SHA-256
  `7076c3dcd7a74b12787007e26263e4360c5e503df2c953631de21a0b9f37a240`.
  All 1,607 published JPEG files pass image decoding.
- Focused release/Foundation/N11/N12 checks pass 32 tests and 1,807 subtests.
  The complete repository suite passes 311 tests and 6,268 subtests.
- The protected legacy tree remains exactly 1,463 files at SHA-256
  `b9ff7b9b507790f1d519593baf2b2d2f24dd6cd49dc0fe10f0ac629278ea42f4`.
  Both local PDF copies remain 57,779,240 bytes, mode `0600`, Git-ignored and
  untracked, with SHA-256
  `a3cc5dd60e12d6b563aee86ea31a15b03f9cddfd4869b8f965d3a11bbc61a0d6`.
- `git diff --check` and final scope inspection pass. Changes are limited to
  Goal 5 records/builder/validator/tests plus the two generated navigation
  files; the immutable legacy corpus and all author-text/image payloads remain
  unchanged.
