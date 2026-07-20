# 12-RELEASE

Status: IN_PROGRESS

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

In progress. Exact release hashes and command outcomes will be recorded only
after the rebuilt published tree and all release gates pass.
