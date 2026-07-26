# 7-RELEASE

Status: **COMPLETE**

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
- The reconciled worktree reports `270 passed` in `tests/conformance` and
  `1044 passed` in the complete active suite, both with no skips or xfails.
  The two tests added during this stage make documentation link, fence, and
  current Python-example structure durable release checks.
- The final wheel is
  `ankos-0.2.0-py3-none-any.whl`, 216540 bytes, with SHA-256
  `8eaa83a4553a10af42d4f572e1e16cea8359a5ec29b13c20dcb167aebc60d435`.
  It contains 36 paths and passes isolated clean-install checks under CPython
  3.10.13.
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
- `GOALS.md` was held unchanged until every other G7-06 completion gate
  passed.

## Authorized Contract Resolution

The hostile release audit found one implemented Goal 7 addition that conflicts
with Goal 6's exhaustive four-item truncation-cause sum at
`goal-6/architecture.md:1724`:
`TruncationCause.INTENSIONAL_SUPPORT`.

The concrete case is a positive-depth rollout whose complete Seed support, or
whose next Rule-result support, is intensional. Rollout can retain that valid
support but cannot enumerate its members for the next generic `apply` without
a separate query or realization operation. Calling the run complete or
rejected would erase a valid denotation. `RESOURCE_EXHAUSTED` would invent a
resource failure; `DEPTH_BOUND` would claim the requested application depth
was reached; and `CANCELLED` or `PRUNED` would invent caller actions.

The fifth cause is therefore the most faithful representation, and it does not
add a program field, semantic family, executor, solver, or realization path.
It is nevertheless a public sum variant, not merely a wording clarification.
On 2026-07-26 the user explicitly authorized retaining
`INTENSIONAL_SUPPORT`. Goal 7 therefore supersedes only the exhaustive
four-cause enumeration at `goal-6/architecture.md:1724`; every other Goal 6
contract remains authoritative and the Goal 6 tree remains byte-for-byte
frozen.

The related zero-step precedence defect found by the same audit is repaired:
`steps=0` now returns `DEPTH_BOUND` even for an intensional initial support,
because no enumeration or application was requested. Focused unit and
conformance tests cover both the zero-step and positive-depth cases.

The authorization resolves the hostile review's only contract blocker without
weakening the five-field architecture or adding an execution path.

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

- [x] `SimpleProgram` stores exactly the five authorized fields.
- [x] Exactly one production `apply` exists and rollout reuses it.
- [x] No source or documentation presents `Dynamics`, `apply_rule`, a
      manifest decoder, a second executor, or a broad root façade as current.
- [x] `serialization` remains catalog-free and accepts only the canonical
      expanded five-key schema.
- [x] Catalog counts, exports, signatures, aliases, presets, compatibility
      spelling, and role boundaries remain exact.
- [x] Datasets, RNG, and visualization remain downstream and absent from
      eager root imports.
- [x] Active source/tests contain no pending stub, skip, xfail, obsolete
      family dispatch, or compatibility fallback.
- [x] Goal 2 and Goal 5 are byte-for-byte unchanged; Goal 4 machinery is not
      used.
- [x] The installed-wheel smoke imports only the clean installation, not the
      checkout, build tree, or an ambient editable package.

## Completion Requirements

- [x] `README-V2.md`, `api.md`, `simple_programs.md`, public docstrings, and
      `ref/notes/ca-scaffold.py` tell one implemented API story.
- [x] `README-V1.md` is unmistakably historical and the 0.1 source migration
      path is explicit without a compatibility runtime or decoder.
- [x] Source, tests, signatures, schema version, package metadata, lockfile,
      wheel, exports, assets, and `py.typed` agree on `0.2.0`.
- [x] Documentation links and fenced examples pass structural checks; all
      executable examples chosen for validation run against the public API.
- [x] `uv run pytest -q tests`, `uv lock --check`, compilation, build,
      clean-install smoke, and `git diff --check` pass.
- [x] One final hostile review finds no sixth field, second executor, family
      dispatch, lossy migration, observer/tooling leak, missing audited
      family, or competing API story.
- [x] Explicit authority resolves the fifth truncation-cause conflict without
      editing the frozen Goal 6 tree.
- [x] `GOALS.md` is updated only after every other requirement passes.

## Verification Evidence

The final authorized release state was verified with:

| Gate | Exact command | Result |
|---|---|---|
| Focused release/runtime slice | `UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q tests/test_release_documentation.py tests/test_rollout.py tests/conformance/test_adversarial_runtime_edges.py tests/conformance/test_probability_replay.py tests/test_catalog_media_criteria_presets.py tests/test_public_api.py` | `56 passed` |
| Complete conformance | `UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q tests/conformance` | `270 passed` |
| Complete active suite | `UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q tests` | `1044 passed` |
| Lockfile | `UV_CACHE_DIR=/tmp/uv-cache uv lock --check` | 12 packages resolved; lock current |
| Compilation | `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall -q src tests examples ref/notes/ca-scaffold.py` | passed |
| Documentation structure | `UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q tests/test_release_documentation.py` | `2 passed`; 11 release documents checked, with current Python fences parsed in `README-V2.md` and `api.md` |
| Reference walkthrough | `UV_CACHE_DIR=/tmp/uv-cache uv run python ref/notes/ca-scaffold.py` | `ca-scaffold: ok` |
| Example CLI | `UV_CACHE_DIR=/tmp/uv-cache uv run python examples/export_viz_samples.py --help` | passed |
| Pending/stub scan | `rg -n 'pytest\\.skip\|pytest\\.mark\\.skip\|pytest\\.mark\\.xfail\|@pytest\\.mark\\.xfail\|NotImplementedError\|_pending\\(\|_not_implemented\\(\|not implemented' src tests --glob '*.py'` | no matches |
| Single operations | `rg -n '^def apply\\(' src/ca --glob '*.py'` and `rg -n '^def rollout\\(' src/ca --glob '*.py'` | exactly `program.py:1976` and `program.py:3588` |
| Frozen authority | `git diff --name-only 1c92123cf3c04a421759f5acd84141a6074a6fbe..HEAD -- goal-2 goal-4 goal-5 goal-6` | empty |
| Stage whitespace | `git diff --check 1c92123cf3c04a421759f5acd84141a6074a6fbe..HEAD` | passed |

No formatter is configured in `pyproject.toml`; compilation, structural
documentation tests, the complete suite, and stage-range `git diff --check`
are therefore the explicit formatting/syntax/whitespace gate.

The installed-package proof used:

```text
UV_CACHE_DIR=/tmp/uv-cache uv build --wheel \
  --out-dir /tmp/ankos-g7-release-final-a776efe-dist .
UV_CACHE_DIR=/tmp/uv-cache uv venv --python 3.10 \
  /tmp/ankos-g7-release-final-a776efe-venv
UV_CACHE_DIR=/tmp/uv-cache uv pip install \
  --python /tmp/ankos-g7-release-final-a776efe-venv/bin/python \
  /tmp/ankos-g7-release-final-a776efe-dist/ankos-0.2.0-py3-none-any.whl
UV_CACHE_DIR=/tmp/uv-cache uv pip check \
  --python /tmp/ankos-g7-release-final-a776efe-venv/bin/python
```

From `/tmp`, the clean interpreter then passed:

```text
/tmp/ankos-g7-release-final-a776efe-venv/bin/python -I \
  /home/jake/Developer/ankos/tests/conformance/installed_wheel_smoke.py
/tmp/ankos-g7-release-final-a776efe-venv/bin/python -I \
  /home/jake/Developer/ankos/ref/notes/ca-scaffold.py
```

Direct metadata and archive inspection confirms package name `ankos`, version
`0.2.0`, Python requirement `>=3.10`, sole runtime dependency `numpy>=2.2`,
36 wheel paths, `ca/py.typed`, all four visualization assets, and no
`specs.py`, `rollout.py`, `engine.py`, or `dynamics.py`.

## Hostile Review

Three independent hostile passes covered documentation accuracy, static
runtime cleanup, and the complete release contract:

- documentation now matches live record fields, enum names, signatures,
  codec-envelope fields, lineage evidence, exports, and catalog counts;
- the zero-step intensional-support precedence defect is repaired and covered
  by unit and conformance tests;
- six dead compatibility aliases and stale transitional wording were removed;
- no competing API story, covert sixth field, second executor, family
  dispatch, observer leak, missing family, or installed-package drift remains;
  and
- the fifth-cause authority conflict is resolved by the narrow user-authorized
  Goal 7 supersession recorded above.

## Stage Results

Complete. The release surface is reconciled, the generic zero-step defect is
repaired, the fifth truncation cause is explicitly authorized, every
completion and no-cheating gate passes, and the independent final hostile
audit reports no blocker. `GOALS.md` was updated only after the closing
verification rerun. Goal 7 now yields a coherent `0.2.0` release candidate;
no release was published.
