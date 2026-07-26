# 6-CONFORMANCE

Status: **IN PROGRESS — REQUIREMENT AUDIT**

## Current Facts

- G7-05 began from clean commit
  `0be468ccfd3d46bb537d1bb90b185a7d509b29c3`.
- G7-00 through G7-04 are complete. Their durable evidence is recorded in
  `1-ORACLES.md` through `5-CATALOG.md`; no earlier stage is presumed correct
  merely because its focused tests are green.
- The stage-entry conformance directory reports `221 passed`.
- The stage-entry complete active suite reports `993 passed` with no skips.
- Active `src/` and `tests/` contain no pytest skip or xfail marker, but
  `tests/conformance/helpers.py` still contains three unused scaffold helpers
  routed through `_not_implemented()` and `NotImplementedError`. Those
  placeholders are not completion evidence and must be removed or replaced by
  stronger live assertions.
- G7-05 owns the aggregate proof that CT01–CT14, PX01–PX12, all sixty primary
  SPF rows, all eight named secondary joins, the exact T01–T45 manifest,
  independent full-result equivalence, static ownership/no-dispatch gates, and
  an ephemeral installed-wheel smoke gate pass together.
- G7-06 has not started. Documentation reconciliation, final release cleanup,
  and release-candidate claims remain out of scope.

## Updated Assumptions

- Existing unit and conformance tests are candidate evidence, not proof that
  every normative assertion is covered.
- A passing aggregate count cannot close G7-05 while scaffold-only helpers,
  weak joins, shared-oracle comparisons, or untested installed behavior
  remain.
- Dedicated CT09, CT10, and CT11 suites may supersede provisional generic
  helper functions, but only if the requirement audit proves their coverage
  is stronger and the dead placeholders are then deleted.
- The ephemeral wheel may validate the existing `0.2.0` package without
  starting G7-06; publishing, release documentation, and final cleanup remain
  forbidden.
- A discovered semantic defect reopens its owning earlier-stage invariant
  before conformance can close. Test-only aggregation gaps remain G7-05 work.

## Big Picture Objective

Close every normative Goal 6 conformance obligation together and prove that
the implemented five-field surface has no hidden alternate semantics,
false-passing oracle, missing family or migration row, tooling leak, or
source-versus-installed-package discrepancy.

## Detailed Implementation Plan

1. Build a requirement-to-evidence matrix for every assertion under CT01–CT14,
   PX01–PX12, the sixty primary family rows, the eight secondary joins, and
   T01–T45.
2. Inspect oracle dependencies and compare complete application records—not
   rendered configurations alone—where the contract requires outcomes,
   applied atoms, terminal partitions, cardinalities, measures, witnesses,
   fresh bindings, lineage, fibers, and evidence.
3. Remove superseded scaffold helpers or replace them with live independent
   assertions. Add only missing G7-05 tests or generic defect repairs.
4. Run blocked-catalog apply/decode, root/submodule/signature, one-`apply`,
   rollout/manual-apply, import-DAG, descriptor-closure, and forbidden-source
   static gates.
5. Build an ephemeral wheel, install it into a clean temporary environment,
   and smoke-test public imports, exact signatures, five fields, one-step and
   rollout behavior, canonical serialization, catalog construction, absence
   of obsolete submodules, and the installed `py.typed` marker.
6. Run the complete conformance slice and complete active suite together,
   followed by lockfile, compilation, whitespace, and hostile-review gates.
7. Record exact commands and outcomes, fold durable facts into `0-plan.md`,
   mark G7-05 complete only if every row has direct evidence, and leave G7-06
   as the first incomplete stage.

Expected files are limited to this stage record, `goal-7/0-plan.md`, active
conformance tests/helpers, and a production owner only if the audit exposes a
generic contract defect. G7-06 documentation and release files remain
untouched.

## No-Cheating Checks

- [ ] No test is skipped, xfailed, inert, or routed through
      `_not_implemented()`/`NotImplementedError`.
- [ ] Independent oracles do not call the implementation, catalog constructor,
      evaluator, commit helper, or codec relation they judge.
- [ ] Full-result comparisons cover all authoritative result fields required
      by their suite rather than comparing rendered state alone.
- [ ] Exactly one production `apply` exists; rollout demonstrably invokes it;
      blocked catalog imports cannot affect application or decoding.
- [ ] No behavior dispatches on SPF/F/T ID, catalog name, constructor
      spelling, family, carrier, locus kind, or Book class.
- [ ] Catalog metadata remains callable-free, serialization catalog-free, and
      datasets/RNG/visualization remain downstream.
- [ ] The installed-wheel smoke imports only the temporary installation, not
      the source checkout, build tree, or ambient editable package.
- [ ] Goal 2 and Goal 5 remain byte-for-byte frozen; Goal 4 machinery and
      G7-06 release work remain untouched.

## Completion Requirements

- [ ] CT01–CT14 pass with a requirement-to-test matrix and no missing
      assertion.
- [ ] PX01–PX12, all sixty primary SPF rows, and exactly the eight required
      secondary joins pass through the one family-blind application law.
- [ ] The literal test-owned T01–T45 manifest matches production metadata,
      callables, owners, targets, kinds, and exports exactly.
- [ ] CT12 independent equivalence and oracle-dependency gates withstand a
      hostile self-reference review.
- [ ] Static dependency, descriptor closure, single-apply, public-surface,
      rollout-reuse, blocked-catalog, and forbidden-token checks pass.
- [ ] The active source suite and clean ephemeral-wheel smoke suite are green.
- [ ] `uv lock --check`, package/test compilation, `git diff --check`, and the
      final G7-05 hostile review pass.
- [ ] `0-plan.md` records exact evidence and names G7-06 as the first
      incomplete stage without claiming release readiness.

## Stage Results

In progress. The first task is the requirement-to-evidence audit; no
completion claim has been made.
