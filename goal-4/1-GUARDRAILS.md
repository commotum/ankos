# 1-GUARDRAILS

Status: **COMPLETE**.

## Current Facts

- Stage start was repository commit
  `9b4a529ff96458afbbf65171217fc58e94699461` with a clean worktree.
- No taxonomy-audit stage, candidate, source-unit, reading, search,
  cross-reference, asset, classification, or family artifact existed.
- The pre-audit corpus tree, handoff blob, catalog blob, API-document blobs,
  reference-scaffold blob, independent SHA-256 values, aggregate corpus digest,
  and file counts all match `0-baseline.md`.
- The corpus contains 1,638 files: 31 Markdown files and 1,607 JPEGs. This stage
  verified only names, counts, hashes, and Git objects; it did not inspect book
  content for constructions.
- `guardrails.json` schema version 1 is the machine-readable authority for
  blind discovery. `tools/validate_guardrails.py` validates its exact
  vocabularies, phase barriers, proof cases, worker-isolation contract, and
  required closure conditions.

## Updated Assumptions

- The scaffold's conceptual distinction between coverage catalog and semantic
  family is sound.
- One source-unit disposition cannot also carry source quality, evidence
  completeness, subtype, and final taxonomy. These are now orthogonal fields.
- "One native event" was too transition-specific. Reuse proofs now preserve one
  native semantic judgment appropriate to the object kind.
- The prior semantic-role vocabulary could not classify an independently
  specified solver or numerical method without conflation. The frozen final
  vocabulary now includes `SOLVER_OR_NUMERICAL_METHOD`.
- A coverage obligation such as a property, seed class, observer, application,
  or emulation need not falsely become a family member. Typed family relations
  now express how it bears on one or more families.
- Failure to prove family reuse is not proof of family novelty. The third
  resolved outcome is source-insufficient family evidence.
- Prompt-only restrictions in a shared repository do not prove worker
  isolation. Delegated blind reading, if used, requires sealed hash-bound
  bundles and a filesystem/OS sandbox.

## Big Picture Objective

Freeze necessary-and-sufficient discovery criteria, evidence and identity
contracts, blind-phase boundaries, object-kind-appropriate reuse proofs, and
closure gates before reading any Book range for additions.

## Allowed Inputs And Scope

Allowed:

- `principles.md`;
- `goal-4/0-plan.md`;
- `goal-4/0-loop.md`;
- `goal-4/0-baseline.md`;
- repository status, Git objects, file counts, and input hashes;
- independent reviews limited to those same files.

Forbidden during this stage:

- reading canonical Book units for construction discovery;
- opening `ref/notes/CA-Types.csv`, `ref/notes/CA-Types.md`, Goal 1, Goal 2,
  `api.md`, `simple_programs.md`, or `src/ca` for semantic content;
- accepting, rejecting, naming, or mapping a current candidate;
- adding T mappings, API-fit judgments, implementation targets, or family
  verdicts to blind artifacts.

Writes were limited to `goal-4/`.

## Source Coverage

- Assigned canonical source units: 0.
- Assigned images: 0.
- Starting and ending reviewed units: 0.
- Starting and ending candidates: 0.
- Starting and ending cross-reference/search/asset queues: 0.
- No source-content search was run.

## Candidate Changes

No B candidate was created, accepted, rejected, merged, split, mapped, or
classified.

The candidate lifecycle is now append-only:

- workers use local W identifiers;
- the root merge allocates B IDs by first discovery-anchor occurrence in the
  frozen audit traversal: Stage 4 bookends in Contents order; each Stage 5–16
  chapter followed by its paired Notes, with units in document order and owned
  images in manifest order; Stage 17 Index; then Stage 18 saturation
  round/result order;
- every candidate stores an immutable discovery epoch, typed discovery anchor
  (`SOURCE_UNIT`, `IMAGE`, or a stage-owned `SEARCH_HIT`), and one-based
  within-anchor ordinal so allocation order and discovery stage can be
  mechanically rechecked; epoch 1 is the initial traversal and each formally
  reopened blind pass increments the epoch before allocating further IDs;
- a split tombstones the parent and allocates new children;
- a merge requires explicit alias/co-reference or proved duplicate capture,
  keeps the earliest ID active, and retains redirect provenance;
- every tombstone records an exact old-evidence-to-target-evidence
  reassignment map; lineage may have multiple later supersession layers but
  must remain acyclic, preserve unit/image/route coverage, and terminate in
  active descendants;
- same behavior, same API shape, same implementation family, or even lossless
  semantic equivalence never establishes Book candidate identity by itself.

## Search And Evidence Log

No Book search was performed. Evidence work consisted only of:

- reading all governing documents in full;
- re-deriving baseline hashes/counts;
- two independent, read-only reviews of the guardrail contract;
- mutation-testing the machine-readable guardrails.

The independent reviews inspected none of the Book, current catalog, Goal 1,
Goal 2, API documents, or runtime.

## Operational Discovery Contract

### Candidate capture

Capture a candidate iff canonical evidence supplies both:

1. an **identity anchor**—an explicit/co-referential name, finite
   specification, unambiguously delimited unnamed referent, or credible route
   to one; and
2. a **semantic anchor**—a native law/denotation or an explicitly isolated
   coverage-bearing relation to such an object.

Incomplete mechanics do not block capture. A concrete source defect or
contradiction around an otherwise credible anchored referent is also captured
with the exact missing facts.

Names, history, analogy, behavior, incidental equations, display conventions,
applications, or external terminology alone are not candidates. A formula
qualifies only when its function/relation/model set/query is itself the formal
object under discussion. An unnamed explicit mechanism can qualify; a named
historical mention cannot.

### Unit disposition and source quality

Each atomic source unit receives exactly one primary reading disposition from:

- `CANDIDATE`;
- `SUPPORTS_CANDIDATE`;
- `CROSS_REFERENCE`;
- `REPRESENTATION_OR_OBSERVER`;
- `APPLICATION_OR_EMULATION`;
- `HISTORICAL_ONLY`;
- `NO_CONSTRUCTION`;
- `SOURCE_DEFECT_OR_AMBIGUITY`.

`source_status` is separately one of `CLEAR`, `AMBIGUOUS`, `DEFECTIVE`, or
`CONFLICTING`. Secondary blind roles separately record properties, seed/input/
boundary classes, behavior, representation, observation, application,
emulation, coupling, implementation details, controls, history, external-only
mentions, and source defects.

If one extracted unit contains multiple atomic claims requiring different
primary dispositions, Stage 2 must split it rather than select a convenient
catch-all. `SOURCE_DEFECT_OR_AMBIGUITY` is primary only when the defect prevents
a sound ordinary disposition; otherwise use the substantive disposition plus
the non-clear source status.

### Evidence completeness

Evidence strength is per claim and per fingerprint field:

- `LEAD_ONLY`;
- `DIRECT_IDENTITY`;
- `DIRECT_PARTIAL_MECHANICS`;
- `DIRECT_COMPLETE_MECHANICS`;
- `CORROBORATING`;
- `CONTEXTUAL`;
- `DEFECT_LIMITED`.

Each fingerprint field is `SUPPORTED`, `NOT_APPLICABLE`,
`UNKNOWN_FROM_SOURCE`, or `CONFLICTING_SOURCE`. Repeated weak citations never
become a complete specification by accumulation. Images carry direct mechanics
strength only after original-resolution inspection, contextual anchoring, and
independent transcription/check.

Every candidate record contains every frozen fingerprint field. Unknown and
conflicting values state the exact missing fact and routes attempted; blanks
are invalid.

### Final-axis and family rules

Final classification remains separate from blind evidence and begins only
after Stage 18 freezes hashes. Every candidate eventually receives exactly one
catalog action, one primary semantic role, and one family action. Insufficiency
is decided independently per axis.

Combined roles require a subtype. Native and declarative constructions have one
own-family membership. Properties, restrictions, seeds, representations,
observers, applications, emulations, solvers, compositions, and aliases use
typed family relations rather than false membership.

### Reuse and novelty

Same-family reuse accepts exactly two proof forms:

1. a lossless correspondence on valid program/specification data and
   configurations/inputs, with an inverse on the valid image and a commuting
   native-judgment law; or
2. membership in one substantive typed parameterized schema with explicit
   parameter domains/invariants and unchanged native judgment mechanics.

Preservation is object-kind-specific:

- deterministic transitions commute one native event for one native event;
- stochastic kernels agree under pushforward, including correlations;
- nondeterministic successors preserve multiplicity and witnesses;
- relations/constraints preserve satisfaction, models, and witnesses;
- partial functions preserve domain, undefinedness, and outputs;
- continuous/denotational objects preserve their native flow or denotation.

Both proof forms preserve program data, complete state/denotation, topology,
history/control, schedule, read snapshot, atomicity/conflicts, effects,
branching/probability, completion/failure, outputs, witnesses, and native
granularity. Callbacks, source interpreters, family switches, `Any`, opaque
packing, hidden clocks, inaccessible history, lossy projections, and multi-step
emulation are disallowed.

A new-family packet defines the plausible comparison set, identifies the
nearest family, supplies a concrete non-preservation witness, discharges
parameter/property/seed/representation/composition/application/emulation
explanations, and receives hostile review. A failed reuse proof alone yields no
novelty conclusion.

### Source insufficiency

Source insufficiency is a resolved boundary only after all canonical context,
images, chapter/Notes routes, Index leads, aliases, and saturation searches are
exhausted. The record states:

- exact unknown/conflicting fields;
- strongest supported facts and evidence ceiling;
- routes and searches checked;
- competing completions consistent with the Book, when possible;
- which classification axis each gap blocks;
- forbidden inference and concrete reopen trigger.

External definitions cannot select a completion. Insufficiency is not a silent
exclusion, collapse, or permission to import defaults.

### Blind-worker isolation

Delegated discovery workers must receive a sealed, hash-bound scratch bundle
containing only:

- sanitized guardrails and exact blind schemas;
- their assigned source units in canonical order;
- owned images/captions;
- an allowlist manifest and empty output files.

The bundle excludes `.git`, repository siblings, current catalogs/goals/API/
runtime/tests, other workers' results, priming hypotheses, and reconciliation
vocabulary. It runs in a filesystem/OS sandbox with network disabled. Workers
return bundle/prompt/schema/output hashes and a prohibited-input nonuse
declaration. The still-blind root merge alone allocates B IDs.

Blind schemas are allowlist-only, reject additional/generic extension fields,
and keep reconciliation schemas physically separate until Stage 19.

## Detailed Implementation Plan

Completed work:

1. Reverified every baseline object/hash/count without reading prohibited
   semantic content.
2. Defined the full contract in `guardrails.json`.
3. Added `tools/validate_guardrails.py`.
4. Added focused validation/mutation tests.
5. Ran two independent reviews and folded substantive findings into the
   contract.
6. Updated `0-plan.md` and `0-loop.md` where the reviews proved the scaffold
   incomplete: native-judgment preservation, solver role, and typed family
   relations.

## No-Cheating Checks

- Candidate count remains zero.
- No source-content query or chapter read occurred.
- The blind candidate allowlist has no overlap with forbidden final taxonomy,
  family, API, runtime, or implementation fields.
- Mutations that remove eligibility criteria, leak a final field, switch to
  T-style IDs, remove a novelty proof, weaken worker isolation, permit arbitrary
  schema fields, or remove the solver role all fail validation.
- Optimized Python runs the same checks without relying on `assert`.
- Independent reviewers declared their allowed inputs and prohibited-source
  nonuse.

## Completion Requirements

| Requirement | Evidence |
|---|---|
| Necessary/sufficient eligibility and dispositions | `candidate_capture_rule`, five eligibility criteria, exclusive disposition rules, orthogonal source status, and secondary roles in `guardrails.json` |
| Catalog/family distinction is explicit and testable | Candidate identity lifecycle, three final axes, family relations, and separate proof packets |
| Blind inputs and forbidden inputs are recorded | Sealed-bundle `worker_isolation` plus allowlist-only `blind_schema_policy` |
| No current candidate is decided or mapped | Zero source coverage/candidates and no Book/catalog semantic inspection |
| Proof obligations are complete | Seven validated proof packets, object-kind native-judgment preservation, and axis-local insufficiency |
| Requirement-level verification | Validator, optimized run, four focused tests, seven destructive guardrail mutations, and independent reviews |

## Stage Results

Commands and outcomes:

```text
git status --short
  clean at stage start

git rev-parse / sha256sum / aggregate corpus hash / file counts
  all baseline values reproduced
  1,638 files = 31 Markdown + 1,607 JPEG

python3 -m json.tool goal-4/guardrails.json
  passed

python3 goal-4/tools/validate_guardrails.py --self-test
  validated Goal 4 guardrails and mutation checks

python3 -O goal-4/tools/validate_guardrails.py --self-test
  validated Goal 4 guardrails and mutation checks

python3 -m py_compile ...
  passed silently

uv run pytest -q goal-4/tools/test_guardrails.py
  4 passed

git diff --check -- goal-4
  passed silently
```

Re-integration answers:

1. No corpus-map/source-unit defect was tested or exposed.
2. No Book vocabulary or route was introduced.
3. No candidate changed.
4. No units, hits, images, or routes were assigned.
5. No Book ambiguity was adjudicated.
6. Reuse proofs now preserve complete native judgments and program data.
7. No earlier stage exists to reopen.
8. The plan/loop gained the solver role, typed family relations, and generalized
   judgment preservation.
9. The audit remains independent of taxonomy count and API outcome.
10. Exact next stage: `2-CORPUS-MAP`, beginning with an independent parse of
    `Contents.md` and construction of the canonical file/source-unit manifest.
