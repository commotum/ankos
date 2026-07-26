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
- Active `src/` and `tests/` contain no pytest skip or xfail marker. The three
  unused scaffold helpers formerly routed through `_not_implemented()` were
  deleted: the dedicated CT09, CT10, and CT11 suites are their stronger live
  replacements.
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

## Requirement-to-Evidence Audit

| Obligation | Direct aggregate evidence | Audit result |
|---|---|---|
| CT01 five-field boundary | `test_program_boundary.py`, `test_serialization_contract.py`, `test_catalog_expansion.py`, `test_import_and_dispatch.py` | Direct |
| CT02 closure/compatibility | `test_descriptor_closure.py`; all 60 programs joined in `test_family_coverage.py` | Repaired |
| CT03 phases/no commit | Eleven phase sentinels plus finite all-or-nothing rejection in `test_validation_phases.py` | Repaired |
| CT04 atomic reconstruction | `test_atomic_application.py`, `test_anchored_rule_kernel.py`, PX01/PX02 mechanics joins | Direct |
| CT05 outcomes/cardinalities | `test_outcome_cardinality.py`, including eventful identity, empty value, and all four applied no-successor variants | Repaired |
| CT06 laws/replay | `test_probability_replay.py`, including terminal measurement and perturbation invariance | Repaired |
| CT07 fresh identity | `test_fresh_identity.py`, including every identity coordinate, ordering/workers, and application-level rejection | Repaired |
| CT08 witnesses/quotient | `test_witness_quotient.py`, including full permutation equality and hostile equality distinctions | Repaired |
| CT09 serialization | `test_codec_inventory.py`, `test_serialization_contract.py`, and `test_serialization.py` | Direct |
| CT10 representation | `test_representation_commutation.py` over the eight literal PX10 relations | Direct |
| CT11 catalog/migration | `test_catalog_expansion.py` plus independent `g7_catalog_manifest.py` | Direct |
| CT12 independent equivalence | `test_oracles.py` and `test_native_generic_equivalence.py` | Hardening in progress |
| CT13 ownership/no dispatch | `test_import_and_dispatch.py` plus `installed_wheel_smoke.py` | Repaired; final wheel pending |
| CT14 observer boundary | `test_observer_boundary.py` plus catalog and codec role joins | Direct |
| PX01–PX12 | `g7_mechanics.py` exercised by `test_family_coverage.py` | Exact |
| SPF001–SPF060 | Independent catalog/mechanics manifests joined in `test_family_coverage.py` | Exact |
| Eight secondary joins | Literal `SECONDARY_JOINS` executed in `test_family_coverage.py` | Exact |
| T01–T45 | Literal independent migration manifest in `test_catalog_expansion.py` | Exact |

The audit found no missing pressure row, family row, secondary join, or
migration row. Its substantive false positives were instead inside CT02,
CT03, CT05–CT08, CT12, and CT13; every row except the still-active CT12
hardening now has a direct repair.

## No-Cheating Checks

- [x] No test is skipped, xfailed, inert, or routed through
      `_not_implemented()`/`NotImplementedError`.
- [ ] Independent oracles do not call the implementation, catalog constructor,
      evaluator, commit helper, or codec relation they judge.
- [ ] Full-result comparisons cover all authoritative result fields required
      by their suite rather than comparing rendered state alone.
- [x] Exactly one production `apply` exists; rollout demonstrably invokes it;
      blocked catalog imports cannot affect application or decoding.
- [x] No behavior dispatches on SPF/F/T ID, catalog name, constructor
      spelling, family, carrier, locus kind, or Book class.
- [x] Catalog metadata remains callable-free, serialization catalog-free, and
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

In progress. The requirement audit and the CT02/CT03/CT05–CT08/CT13 repairs
are complete. The interim aggregate conformance slice reports `253 passed`;
CT12 hardening, the final wheel built from the reconciled source state, the
complete active suite, and the final hostile review remain before any
completion claim.
