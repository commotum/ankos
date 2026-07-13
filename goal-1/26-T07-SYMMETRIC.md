# 26-T07-SYMMETRIC

Status: **IN PROGRESS — SOURCE AND PROPERTY-BOUNDARY AUDIT ACTIVE**

## Current Facts

- Exact catalog row: T07, CSV line 8, `Left-Right Symmetric Cellular Automata`; taxonomy section 7 at `ref/notes/CA-Types.md:160-176` is search vocabulary only, not book evidence.
- T01 already records reflection of ordered reads `(left,self,right) -> (right,self,left)`, the elementary-rule survey's 88 combined reflection/color-conjugacy orbits, and the historical 32-rule intersection of left-right symmetry with T06 blank preservation. T06 independently proves that 64 elementary rules are fixed by reflection and exactly 32 are also zero-background preserving.
- T03/T04/T05 establish that an equal-weight sum over a reflection-closed stencil is unchanged by reversal. That is a structural proof of a property of the resolved rule, not a runtime flag or another executor.
- D114 and D118 reserve reflection/symmetry predicates or transforms for T07. D119 supplies a generic nonexecution property layer whose reuse must be proved rather than assumed.
- `simple_programs.md:1833-1863` proposes an `ISOTROPIC` orbit-table rule representation for a chosen symmetry group. The current `src/ca` runtime has no corresponding structural rule evaluator or property checker; `datasets.invariance_transforms` supplies reflection metadata for dataset streams only.
- Goal 1 changes only `goal-1/`; no runtime, root documentation, or test implementation occurs in this stage.

## Updated Assumptions

- Working hypothesis: T07 is primarily a semantic property/restriction on an eligible resolved CA program relative to an explicit validated reflection action, plus a lossless reflected-program transform/orbit relation. It adds no state, frontier, read, rule result, update, successor, halt, or runner branch.
- Working hypothesis: for scalar labels on a one-dimensional centered stencil, the local obligation is `evaluate_P(v) = evaluate_P(reverse(v))` for every complete local read `v`. A global reflected-trajectory theorem additionally requires support, frontier, update, boundary/realization, and seed compatibility.
- Working hypothesis: a compact orbit table is a lossless representation of a passing finite rule, not a second execution algebra. Whether T07 itself requires that representation, or merely validates existing exhaustive/aggregate forms, remains open until source evidence and the current-API audit close.
- Reflection of spatial positions, permutation of neighborhood slots, any action on oriented alphabet values, rule-table transformation, program equivalence, symmetric seeds, symmetric trajectories, visual pattern symmetry, rotation/isotropy, and color conjugation are distinct responsibilities unless evidence explicitly couples them.

## Big Picture Objective

Determine exactly what the book means by left-right symmetry, distinguish a rule fixed by reflection from a reflected rule transform, combined equivalence orbit, symmetric initial condition, and symmetric observed pattern, and produce the smallest implementation-ready Goal 2 property/representation handoff without adding family execution semantics.

## Catalog Identity

- Stable ID: T07.
- Exact CSV name: `Left-Right Symmetric Cellular Automata`.
- Taxonomy section: 7, vocabulary seed only.
- Provisional entry kind: property/restriction over an eligible CA program and reflection action; possible lossless orbit-table representation and rule-transform relation.
- Initial vocabulary: left-right/right-left symmetry, symmetric/asymmetric rules, reflection/reflected/reflective, mirror/mirrored, reversal/reversed, interchange left and right, equivalent/inequivalent rules, conjugate/color interchange, isotropic/rotational invariance, totalistic symmetry, symmetric initial conditions/patterns, and quiescent-symmetric rules.

## Search Log

IN PROGRESS. The canonical monolith, captions, Notes, actual Index, split mirrors, history, rule-equivalence material, totalistic relations, higher-dimensional controls, and governed assets are being saturated with reproducible scoped queries.

## Book Excerpts

IN PROGRESS. No source hypothesis becomes architecture until its exact canonical provenance and role are closed.

## Construction Model

IN PROGRESS. The audit will separately reconstruct:

1. the reflection action on DOMAIN/support and ordered neighborhood slots;
2. the local rule-fixed-point predicate;
3. the involutive reflected-program transform and equivalence/orbit relation;
4. any compact orbit-table representation and its lossless expansion;
5. the extra seed/boundary conditions needed for symmetric trajectories; and
6. unsupported cases such as missing reflection closure, hidden callbacks, dynamic reads, oriented outputs without a declared action, or non-CA schedules.

## Current API Fit

IN PROGRESS. The audit will compare the generic property layer from T06, documented `ISOTROPIC` orbit reduction, explicit neighborhood ordering, dataset-only affine transforms, and the absence of a structural current-runtime checker/evaluator.

## Current Runtime Fit

IN PROGRESS. No current family name, boundary reflection, dataset transform, palette flip, or sampled trace will be accepted as proof of rule symmetry.

## Principles Audit

IN PROGRESS. The central adversaries are an asymmetric rule and its distinct mirror, a rule fixed only under a combined reflection/color transform, a symmetric rule with an asymmetric seed or hostile boundary, a non-reflection-closed stencil, a totalistic proof versus exhaustive enumeration, and oriented alphabet values whose reflection action is nontrivial.

## Detailed Implementation Plan

1. Close an exact canonical text manifest over direct names, aliases, descriptions, captions, Notes, actual Index, splits, equivalence/history, totalistic, higher-dimensional, seed/pattern, and unrelated symmetry controls.
2. Follow every relevant governed asset in both directions and classify direct property evidence, transform/orbit relations, seed/pattern relations, and exclusions.
3. Derive exact elementary and general finite-alphabet reflection counts, reflection-transform codecs, fixed-rule lists, and T06 intersection; preserve combined color-conjugacy as a distinct group action.
4. Reconstruct the strict eligible CA scope, local predicate, reflected-program involution, orbit representation, typed claim/evidence/result identities, and global trajectory qualifications.
5. Audit current documentation/runtime/tests and every T01-T06/T21-T24 boundary affected by reflection, isotropy, or dimensional action.
6. Write the concrete Goal 2 generic property/transform/representation handoff, adversarial conformance plan, serialization/identity rules, and no-cheating checks.
7. Run embedded source/evidence/semantic/asset checks, independent review, repository tests, Markdown/diff/status gates, and global reintegration.

## Goal 2 Implementation Stage

IN PROGRESS. The handoff will name concrete generic property, transform, orbit-table, structural evaluator, serialization, migration, and conformance responsibilities only after the evidence determines which are required.

## No-Cheating Checks

- No T07/symmetric/isotropic family executor, update law, runtime flag, hidden coordinate transform, or special rollout.
- No sampled symmetric trajectory, symmetric seed, symmetric boundary, totalistic family name, palette reflection, or displayed raster accepted by itself as proof of local rule symmetry.
- No conflation of left-right reflection, black/white conjugation, rotations, arbitrary neighborhood permutations, boundary reflection, or dataset augmentation.
- No orbit quotient without a validated group action, canonical orbit keys, complete table, and lossless expansion that denotes exactly the same local function.
- No opaque callback, code-number shortcut, family dispatch, or trusted Boolean metadata substituted for structural checking.

## Completion Requirements

- [ ] Every direct/alias/caption/Notes/actual-Index/split/cross-reference/equivalence/seed/pattern/control candidate is dispositioned with zero remainder under a declared reproducible protocol.
- [ ] Every relevant governed asset is hash-pinned and classified, with every source-permitted semantic/raster check closed.
- [ ] The rule predicate, reflection action, transform/orbit identities, exact counts/code relations, compact representation, and rule/seed/boundary/trajectory/view distinctions are proved across supported descriptions.
- [ ] Current API/runtime fit and a concrete Goal 2 property/transform/conformance stage are implementation-ready.
- [ ] Global ledgers, independent review, embedded checks, coverage/diff gates, and repository tests pass.

## Stage Results

IN PROGRESS.

## Integration Results

IN PROGRESS. The ten-question reintegration audit will be answered after evidence and design close.
