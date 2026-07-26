# 7-RELEASE

Status: **IN PROGRESS**

## Current Facts

- G7-06 began from clean commit
  `1c92123cf3c04a421759f5acd84141a6074a6fbe`.
- G7-00 through G7-05 are complete. Their durable evidence is recorded in
  `1-ORACLES.md` through `6-CONFORMANCE.md`.
- The stage-entry conformance directory reports `270 passed`; the complete
  active suite reports `1042 passed`, both with no skips or xfails.
- The G7-05 ephemeral wheel installed into a clean CPython 3.10 environment
  and passed public import, signature, codec, catalog, application, rollout,
  dependency, and `py.typed` checks.
- Source and lock metadata already declare `0.2.0`, but that checkpoint did
  not reconcile the public documentation or authorize a release-candidate
  claim.
- G7-06 owns documentation reconciliation, release cleanup, final source and
  installed-package agreement, and the final hostile review.
- Goal 2 and Goal 5 remain frozen. Goal 4 and Book rediscovery remain outside
  this stage.

## Updated Assumptions

- Runtime and semantic changes are out of scope unless release reconciliation
  exposes a concrete generic defect.
- `README-V1.md` remains useful only as an explicitly historical 0.1
  snapshot; it must not read as the current API.
- Source migration means reconstructing programs through catalog constructors
  or explicit five-field construction. It does not authorize a `Dynamics`
  compatibility façade or old-manifest decoder.
- Existing green conformance is necessary but insufficient: documentation,
  source signatures, lock metadata, wheel contents, links, code fences, and
  clean-install behavior must agree.
- `GOALS.md` must remain unchanged until every other G7-06 completion gate
  passes.

## Big Picture Objective

Reconcile source, documentation, packaging, and installed behavior into one
coherent release-ready `0.2.0` story. A fresh reader must encounter exactly
the implemented five-field API, one family-blind `apply`, rollout through that
operation, fail-closed expanded serialization, and the explicit 60-family
catalog—without transitional scaffolding or a competing compatibility path.

## Detailed Implementation Plan

1. Audit `README-V1.md`, `README-V2.md`, `api.md`, `simple_programs.md`,
   public docstrings, `ref/notes/ca-scaffold.py`, `pyproject.toml`, `uv.lock`,
   package exports, and the tracked source tree against the live runtime and
   frozen Goal 6 contract.
2. Make `README-V2.md` the concise implemented-runtime entry point; label
   `README-V1.md` as a historical 0.1 snapshot and add an explicit 0.1 source
   migration note with no fallback decoder.
3. Remove pending-target language from `api.md`, then reconcile its examples,
   exact signatures, ownership, codec schema, and catalog surface.
4. Reconcile the conceptual guide, public docstrings, and reference scaffold
   with the same implemented surface. Do not create a second API reference or
   taxonomy document.
5. Remove only demonstrably dead imports, stale current-runtime examples,
   compatibility scaffolding, obsolete family switches, or duplicate
   contracts found by the audit.
6. Run documentation/static checks, focused tests, the full active suite,
   lock validation, compilation, whitespace/diff checks, wheel build, clean
   installation, and installed public-surface smoke tests.
7. Conduct a hostile completion review against every final Goal 7 gate,
   repair any blocker, and rerun affected checks.
8. Only after all preceding evidence passes, update `GOALS.md`,
   `goal-7/0-plan.md`, and this record to close G7-06 and Goal 7.

Expected changes are limited to release-owned documentation, public
docstrings, packaging metadata if actual drift is found, this stage record,
`goal-7/0-plan.md`, and `GOALS.md` after closure. Goal 2, Goal 5, and Goal 4
must remain untouched.

## No-Cheating Checks

- [ ] `SimpleProgram` stores exactly the five authorized fields.
- [ ] Exactly one production `apply` exists and rollout reuses it.
- [ ] No source or documentation presents `Dynamics`, `apply_rule`, a
      manifest decoder, a second executor, or a broad root façade as current.
- [ ] `serialization` remains catalog-free and accepts only the canonical
      expanded five-key schema.
- [ ] Catalog counts, exports, signatures, aliases, presets, compatibility
      spelling, and role boundaries remain exact.
- [ ] Datasets, RNG, and visualization remain downstream and absent from
      eager root imports.
- [ ] Active source/tests contain no pending stub, skip, xfail, obsolete
      family dispatch, or compatibility fallback.
- [ ] Goal 2 and Goal 5 are byte-for-byte unchanged; Goal 4 machinery is not
      used.
- [ ] The installed-wheel smoke imports only the clean installation, not the
      checkout, build tree, or an ambient editable package.

## Completion Requirements

- [ ] `README-V2.md`, `api.md`, `simple_programs.md`, public docstrings, and
      `ref/notes/ca-scaffold.py` tell one implemented API story.
- [ ] `README-V1.md` is unmistakably historical and the 0.1 source migration
      path is explicit without a compatibility runtime or decoder.
- [ ] Source, tests, signatures, schema version, package metadata, lockfile,
      wheel, exports, assets, and `py.typed` agree on `0.2.0`.
- [ ] Documentation links and fenced examples pass structural checks; all
      executable examples chosen for validation run against the public API.
- [ ] `uv run pytest -q tests`, `uv lock --check`, compilation, build,
      clean-install smoke, and `git diff --check` pass.
- [ ] One final hostile review finds no sixth field, second executor, family
      dispatch, lossy migration, observer/tooling leak, missing audited
      family, or competing API story.
- [ ] `GOALS.md` is updated only after every other requirement passes.

## Stage Results

In progress. The first action is the release-surface audit; no release
reconciliation claim has yet been made.
