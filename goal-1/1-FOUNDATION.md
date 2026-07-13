# 1-FOUNDATION

Status: **COMPLETE — EVIDENCE AND ARCHITECTURE RECLOSED**

Architecture authority: D000-D003, the governing algebra, and the runner/nonfit boundaries in `architecture-audit.md` supersede Foundation-time uncertainty about whether a common transition/rewrite protocol would survive type evidence.

## Current Facts

- The `types` worktree was clean at stage start. `goal-1/` contained only `0-plan.md`, `0-loop.md`, and `0-prompt.md`; no prior stage was in progress or reopened.
- `ref/notes/CA-Types.csv` contains one header and 45 nonempty unique `ca_type` rows (`:1-46`). Its `compatible` field is empty for every row and supplies no semantic evidence.
- `ref/notes/CA-Types.md` contains numbered sections 1 through 45 whose titles match the CSV rows exactly (`:25-1279`). It is a taxonomy and vocabulary guide, never a substitute for the canonical book.
- The plan contains each stable ID `T01` through `T45` once. Execution stages 2 through 46 each own one unique type; the execution order is deliberately adversarial rather than CSV order (`0-plan.md:136-793`).
- `principles.md` contains Principle 0 plus Principles 1 through 16 (`:3-127`). They require evidence-first construction discovery, honest executor boundaries, typed results, complete visible state, separation of topology/representation/datasets, and re-derivation rather than patches.
- `simple_programs.md` is a 2,199-line fixed-support trajectory proposal, not an established universal API.
- The eleven top-level `src/ca` Python modules total 5,338 lines. The nine `tests/test_*.py` files total 1,685 lines and contain 97 statically named tests.
- The canonical local book monolith has numbered content through line 22,498 (`wc -l` reports 22,497 because the final line has no terminating newline). Foundation validates the source and procedure but does not collect type evidence; excerpt collection begins in T01.

## Foundation-Time Assumptions (Historical)

- Still valid as hypotheses: support/topology, values, and control should be distinguished; grouped ordered reads may be reusable; a selector can be useful for finite loci; dataset and visualization concerns should remain downstream.
- Changed: the current runtime does not implement the single documented per-target algebra. It dispatches on named rule families, and several temporal paths bypass declared neighborhood components.
- Changed: the current trace is not always complete Markov state. AR2 omits one seed-history value, Dyadlags omits two, and Lagcounts later maintains a packed ten-bit history inside its executor.
- Changed: `simple_programs.md` itself lacks an explicit `UPDATE` component and defines `FORMULAIC`/`STOCHASTIC` over the full field, so it cannot be treated as a safe implementation blueprint under the no-callback/no-smuggling constraints.
- Needs type evidence: whether one substantive transition/rewrite algebra survives; whether canonical rank-0..3 coordinates preserve all required structure; which entries are constructions versus restrictions, seeds, observables, or solver-defined systems; which current primitives retain their meanings.

## Architecture-Reclosed Foundation Disposition

Evidence through T45 resolves the Foundation hypotheses without weakening its evidence discipline:

- one branch-free `SimpleProgram` runner survives for every evidenced transition/rewrite construction;
- DOMAIN is the task/program dimensional space with support/topology, while ALPHABET is its label/value schema and may use transparent products or tagged unions;
- FRONTIER selects firing loci/occurrences/matches, NEIGHBORHOOD supplies access, RULE returns typed writes/replacements, and UPDATE returns a structured `StepResult[Configuration]` containing successor(s), outcome, and event/witness data;
- CA is one fixed-lattice/all-sites/local-stencil/same-site-write/snapshot-parallel preset, not the library boundary;
- catalog identity never selects a runtime class or executor;
- model sets, uniterated function definitions, and unposed general PDE relations are declarative nonfits rather than fake programs;
- the evidence-first procedure, stable T01-T45 join, source discipline, fit labels, and separation of execution/trace/encoding/solvers/views remain valid unchanged.

## Big Picture Objective

Establish an auditable, evidence-first baseline before judging any catalog type: prove the catalog/stage join, read and inventory governing documents and current executable contracts, define reproducible evidence and fit standards, create the global ledgers, expose contradictions without resolving them prematurely, and leave T01 ready to execute.

## Catalog Baseline

- Stable identity is CSV row order: CSV line 2 is T01 and line 46 is T45.
- `evidence-index.md` records every exact CSV name, CSV line, matching taxonomy section, adversarial execution stage, future stage filename, and status.
- Stage filenames use `[execution stage]-TNN-[SHORTHAND].md`, so taxonomy identity never changes when dependency order changes.
- Initial status is 45 `PENDING`, 0 `IN PROGRESS`, 0 `REOPENED`, and 0 `COMPLETE`.
- A type becomes complete only through the evidence record contract in `evidence-index.md`; neither a stage file nor green tests are sufficient alone.

## Source Read Coverage

All required Foundation sources were read or mechanically checked from the current worktree.

| Source | Coverage | Foundation use |
|---|---:|---|
| `principles.md` | 131 / 131 lines | Governing architecture and no-cheating constraints |
| `simple_programs.md` | 2,199 / 2,199 lines | Current documented API hypothesis |
| `ref/notes/CA-Types.csv` | 46 / 46 lines | Authoritative 45-row coverage join |
| `ref/notes/CA-Types.md` | All numbered headings and exact section spans checked | Vocabulary/taxonomy navigation only |
| `src/ca/__init__.py` | 93 / 93 lines | Public runtime exports |
| `src/ca/alphabets.py` | 177 / 177 lines | Finite raw value spaces |
| `src/ca/datasets.py` | 842 / 842 lines | Dataset plan/stream boundary |
| `src/ca/frontiers.py` | 80 / 80 lines | Current update-site support |
| `src/ca/loci.py` | 636 / 636 lines | Coordinate spaces, selectors, masks, gather |
| `src/ca/neighborhoods.py` | 766 / 766 lines | Grouped spatial and temporal read specifications |
| `src/ca/rng.py` | 79 / 79 lines | Deterministic RNG mechanics |
| `src/ca/rollout.py` | 831 / 831 lines | Executable family dispatch and raw trajectory generation |
| `src/ca/rules.py` | 515 / 515 lines | Channel summaries, lookup/callable rules, named families |
| `src/ca/seeds.py` | 1,056 / 1,056 lines | Seed specifications, selectors, rendering, structured catalog |
| `src/ca/specs.py` | 263 / 263 lines | Dynamics/results and manifest resolution |
| `tests/test_datasets.py` | 137 / 137 lines | Four dataset recipes and stream contracts |
| `tests/test_loci.py` | 83 / 83 lines | Coordinate/selector/gather/boundary contracts |
| `tests/test_neighborhoods.py` | 288 / 288 lines | Read component and stencil contracts |
| `tests/test_rng.py` | 27 / 27 lines | Stable RNG derivation |
| `tests/test_rollout.py` | 582 / 582 lines | Family-specific scalar/batch execution contracts |
| `tests/test_rules.py` | 45 / 45 lines | Finite rule metadata |
| `tests/test_seeds.py` | 111 / 111 lines | Selected seed/render contracts |
| `tests/test_specs.py` | 115 / 115 lines | Six named family resolvers and one frontier |
| `tests/test_viz_export.py` | 297 / 297 lines | Downstream raw-result encoding boundary |

## Sync and Inspection Log

Commands used for the Foundation baseline:

```text
git status --short --branch
rg --files goal-1 | sort
find src/ca -maxdepth 1 -type f -print | sort
find tests -maxdepth 2 -type f -print | sort
wc -l goal-1/0-loop.md goal-1/0-plan.md ref/notes/CA-Types.csv
wc -l principles.md simple_programs.md ref/notes/CA-Types.md ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
wc -l src/ca/*.py tests/test_*.py
sed -n '1,214p' goal-1/0-loop.md
sed -n '1,814p' goal-1/0-plan.md
sed -n '1,131p' principles.md
sed -n '1,2199p' simple_programs.md
sed -n '1,46p' ref/notes/CA-Types.csv
rg -n '^#{1,6} ' ref/notes/CA-Types.md
sed -n '<full file range>' src/ca/<each top-level module>.py
sed -n '<full file range>' tests/test_<each source file>.py
rg -n '^(class |def |    def |[A-Z][A-Z_]+ *=|__all__)' src/ca/*.py
rg -n '^def test_' tests/test_*.py
```

No book term search was performed or claimed for a type in Foundation.

## Governing Principles Audit

| Principle | Foundation consequence |
|---|---|
| 0 | The plan, documented API, and runtime are hypotheses. A failed fit reopens prior work rather than creating a patch. |
| 1 | The 45 labels establish obligations, not executors or presets. |
| 2 | `FRONTIER -> NEIGHBORHOOD -> RULE -> UPDATE` remains a candidate only where it is substantive. |
| 3 | Current component responsibilities are recorded but may be redrawn by evidence. |
| 4 | Same-site values, effects, constraints, derivatives, distributions, and observations are not collapsed. |
| 5 | Support/topology, values, and control required to advance belong to visible state. |
| 6 | Canonical addresses do not define topology; inadequate ANKoS schemas must change. |
| 7 | Fixed, growing, sparse, and dynamic supports retain their actual semantics. |
| 8 | Tensor lowering and visualization do not define the construction. |
| 9 | Only independent choices compose freely; genuine coupling becomes validated invariants. |
| 10 | Presets may return a shared specification but never select hidden execution paths. |
| 11 | Solvers, integrators, and RNG implementations stay separate; defining order/update behavior stays semantic. |
| 12 | The flow remains `program -> trace -> experiment encoding -> batch/visualization`. |
| 13 | The adversarial stage order tests hard semantic boundaries early. |
| 14 | Flags, branches, hidden state, padding, fallbacks, duplicated logic, and weakened tests trigger re-derivation. |
| 15 | Goal 2 tests must use canonical construction examples and native semantics. |
| 16 | Explicit total mappings are boundaries; fallback conversions are shims. |

## Current API Model

`simple_programs.md` currently specifies:

- a finite dense domain with canonical `[t,x,y,z]` addresses and spatial rank zero through three (`:1-24`, `:115-198`);
- a field-valued trajectory and current snapshot (`:87-113`);
- finite alphabets, seed support/fill/distribution, and fixed/periodic/reflective spatial boundaries (`:200-358`);
- relative read selectors whose candidates, predicates, Boolean combiner, order, and read mode may depend on the current field (`:360-731`);
- absolute writable next-slice frontiers, also potentially state-dependent (`:1412-1765`);
- exhaustive, isotropic, semi-totalistic, totalistic, formulaic, and stochastic per-target value rules (`:1767-2122`);
- synchronous parallel same-site writes and copy-forward outside the frontier (`:2124-2199`).

Foundation fit assessment:

| Concern | Fit | Reason |
|---|---|---|
| Fixed dense rank-0..3 CA state | DIRECT for the documented scope | The domain, selectors, and value assignment describe this case directly. |
| Explicit `UPDATE` component | SEMANTIC MISMATCH | Principles name update/commit as a responsibility, while the document hard-codes same-site parallel assignment. |
| Complete visible control | SEMANTIC MISMATCH | The document has no explicit control-state model. |
| Dynamic support/topology | SEMANTIC MISMATCH | `D` and shape are allocated before execution; no insert/delete/rewire semantics exist. |
| Full-field formula/callback | SEMANTIC MISMATCH as a universality mechanism | `FORMULAIC` and `STOCHASTIC` can receive the whole field, which could smuggle an entire construction. Legitimate narrow formulas remain an evidence question. |
| Trace representation boundary | SEMANTIC MISMATCH | The canonical encoding is built into generator state rather than supplied as a separate lowering from arbitrary native state. |
| Masked adaptive reads | UNRESOLVED | Documented, but the current runtime accepts only compact neighborhood reads and no completed type requires the masked form yet. |

## Current Runtime Model

The module-level inventory is maintained in `design-ledger.md`. The cross-cutting facts that constrain later comparisons are:

1. `Dynamics` stores domain, fixed shape, rule, neighborhoods, frontier, boundary, and metadata, but not an alphabet, seed specification, explicit update algebra, or control-state schema (`src/ca/specs.py:24-57`).
2. The spec resolver hard-codes six Phase 1 rule/neighborhood families and only `time_slice` frontiers (`src/ca/specs.py:84-199`). A family index is therefore current dispatch, not a shared declarative preset mechanism.
3. `loci.Selector` is a finite coordinate selector with arbitrary Python predicate functions and no update/scatter algebra (`src/ca/loci.py:42-59`, `:257-319`).
4. Neighborhoods preserve grouped selector components and can represent negative-time offsets (`src/ca/neighborhoods.py:47-59`, `:501-549`), even though `simple_programs.md` forbids temporal reads and asks memory-bearing programs to put history in current state (`simple_programs.md:703-731`).
5. Frontiers expose only a full current time slice, while `simple_programs.md` describes absolute next-state coordinate selectors (`src/ca/frontiers.py:38-80`; `simple_programs.md:1412-1510`).
6. Rules expose structured channel pipelines, but callable `formulaic` rules and seed predicate callbacks can serve as unrestricted escape hatches if generalized (`src/ca/rules.py:316-334`; `src/ca/seeds.py:733-781`).
7. Scalar and batch rollout branch by `rule.family` (`src/ca/rollout.py:145-213`). Temporal families use dedicated local variables or bit packing rather than executing their declared neighborhood objects (`:334-574`).
8. Spatial rollout does gather declared selector components and apply rule-channel pipelines, but only for three named Dyadrads/Dyadaxes families and full-slice binary lookup (`src/ca/rollout.py:576-831`).
9. `RawEpisode`/`RawBatch` and visualization export demonstrate that dataset planning and file encoding can remain downstream, but only dense integer rank-0..3 traces are currently covered.

## Current Test Contracts and Limits

- Loci tests establish centered canonical coordinates, selector ordering, trajectory-time gathering, and three spatial boundary policies (`tests/test_loci.py:9-83`).
- Neighborhood tests establish negative-time component data and several spatial stencil constructors, but no generic temporal execution (`tests/test_neighborhoods.py:15-288`).
- Rollout tests lock AR2 hidden previous state, Dyadlags hidden two-value history, and Lagcounts visible prefix followed by executor-local packed history (`tests/test_rollout.py:68-260`).
- Spatial tests independently assert only rule-zero extinction; nonzero scalar/batch parity compares two paths in the same implementation and is not an external semantic oracle (`tests/test_rollout.py:263-424`).
- Rollout validation covers optional coordinates, batch/shape mismatches, boundary schema, unsupported frontiers, and domain/rank mismatch (`tests/test_rollout.py:427-582`).
- Specs tests cover selected named-family resolution; datasets tests cover four current PE recipes and stream metadata; neither supplies catalog coverage (`tests/test_specs.py:9-115`, `tests/test_datasets.py:9-137`).
- Visualization tests prove a separate raw-result encoding boundary and explicitly reject floats in the current exporter. That is an exporter limitation, not evidence against continuous semantic state (`tests/test_viz_export.py:81-297`).
- No current test maps to a stable Goal 1 type ID, and there is no current ECA rule-number/trajectory conformance test. Green current tests cannot prove any of the 45 type obligations.

## Evidence and Search Procedure

For every type, use the procedure in `0-loop.md` plus these concrete rules:

1. Read the exact CSV row and the complete matching `CA-Types.md` section before creating the vocabulary.
2. Record direct names, singular/plural and hyphen variants, aliases, historical terms, named examples, parameters, defining operations, captions, Notes and Index terms, and cross-referenced systems.
3. Search the canonical monolith with literal and case-insensitive fixed-string queries where possible. Use broad regex only when variants require it, and record the exact command.
4. Inspect enough context around every hit to identify a complete construction-relevant passage. Follow every relevant page/section reference and add newly discovered vocabulary.
5. Record canonical monolith excerpts once. Split-file duplicates are navigation aids and must be dispositioned as duplicates rather than copied twice.
6. Maintain a candidate table whose rows end as `INCLUDED`, `DUPLICATE`, `CROSS-REFERENCE FOLLOWED`, or `FALSE POSITIVE`. Any unresolved row keeps the stage incomplete.
7. After evidence reconstruction, compare exact document/runtime/test definitions using the Foundation fit labels. Search completed stages and `design-ledger.md` before proposing a primitive.
8. Update the three global artifacts and mechanically recheck the 45-row join after each stage.

Suggested reproducible search forms, adjusted per type:

```text
rg -n -i -F '<literal term>' ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
rg -n -i '<bounded variant regex>' ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
sed -n '<start>,<end>p' ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md
rg -n -i -F '<term>' ref/A-New-Kind-of-Science/BACK-MATTER/Notes/Notes.md ref/A-New-Kind-of-Science/BACK-MATTER/Index/Index.md
```

The actual local layout must be checked before using the final command; recorded searches must name the paths that actually existed.

## Detailed Implementation Plan

- Update `0-plan.md` with synchronized current facts and Foundation status.
- Create this stage file, `evidence-index.md`, and `design-ledger.md` under `goal-1/`.
- Verify the 45-row CSV/taxonomy/plan/index joins mechanically.
- Run the current test suite as a baseline contract check; do not treat it as catalog evidence.
- Run `git diff --check` and prove Goal 1 changes are confined to `goal-1/`.
- On completion, mark Foundation complete in all three artifacts and select `2-T01-ELEMENTARY.md` next.

## Goal 2 Foundation Handoff

Goal 2 must consume Synthesis, not implement the current Foundation hypotheses directly. Its foundation stage will need to:

- introduce only primitives validated by completed type stages and the final design ledger;
- preserve current evidenced behavior through visible state and typed semantics, not family dispatch or hidden history;
- define native program state separately from trace/ANKoS encoding and dataset/export layers;
- replace any accepted callable mechanism with a bounded, inspectable semantic protocol or document why a narrow callable is the actual construction;
- provide catalog-independent core tests plus a traceable conformance obligation for every T01 through T45;
- include migrations/removals for current named-family branches only after their replacement semantics and canonical examples are proved.

Dependencies: all 45 type stages and Synthesis. No runtime file is authorized to change in Goal 1.

## No-Cheating Checks

- The 45 catalog names are joined mechanically, not inferred from stage filenames.
- All statuses begin pending; Foundation makes no type complete and records no book excerpt as type evidence.
- Current family branches, callbacks, fixed support, hidden history, and rank limits are named explicitly rather than wrapped in a cosmetic interface.
- Foundation did not prematurely declare an executor; the later completed type audit now establishes one common runner for step/rewrite systems and explicit declarative nonfits outside rollout.
- Test results are classified as current-runtime contracts only.
- No change is made to `src/ca`, `tests`, `principles.md`, `simple_programs.md`, or any non-`goal-1/` path.

## Completion Requirements

- [x] The CSV has exactly 45 unique nonempty types and numbered taxonomy headings match them.
- [x] Stable T01 through T45 mappings and unique execution stages are recorded.
- [x] `principles.md`, `simple_programs.md`, every top-level `src/ca` module, and all corresponding tests were read in full.
- [x] Current API/runtime responsibilities, contradictions, test contracts, and coverage gaps are recorded with file references.
- [x] `evidence-index.md` exists with 45 pending entries and an auditable status/evidence contract.
- [x] `design-ledger.md` exists without a premature construction-family conclusion.
- [x] Search, excerpt, disposition, fit-label, re-integration, and Goal 2 handoff standards are defined.
- [x] Mechanical join verification passes against the new ledgers.
- [x] Current tests pass as a baseline.
- [x] Whitespace and scope checks pass; Foundation status is folded into all global artifacts.

## Architecture-Reclosed Stage Result

**COMPLETE.** Foundation's evidence procedure and catalog join remain authoritative. D000-D003 are reclosed around the common SimpleProgram runner, structural type axes, catalog-independent execution, and explicit nonfits described above; no Foundation runtime implementation is introduced.

## Historical Stage Results (Foundation-Time Evidence Retained)

Foundation established the required evidence and architecture scaffolding without changing runtime semantics. It exposed three immediate liabilities to carry into type work: current family-dispatched execution, current hidden temporal state, and a documented fixed-support value-assignment model that lacks explicit update/control/topology semantics.

Created:

- `goal-1/1-FOUNDATION.md`
- `goal-1/evidence-index.md`
- `goal-1/design-ledger.md`

Updated:

- `goal-1/0-plan.md` current facts and execution status.

No stage was reopened. Next work after verification is T01 Elementary Cellular Automata, beginning from its exact CSV row and complete taxonomy section, then an exhaustive canonical-book search.

Verification outcomes:

```text
python -c '<catalog join check>'
  unavailable: `python` was not installed on PATH

python3 -c '<catalog join check>'
  {"csv_rows": 45, "unique_names": 45, "taxonomy_join": 45,
   "plan_type_stages": 45, "index_rows": 45,
   "statuses": {"PENDING": 45}}

pytest -q
  unavailable: `pytest` was not installed on PATH

uv run pytest -q
  102 passed in 1.18s

git diff --check
  passed with no output

git status --short
  only `goal-1/0-plan.md` plus the three new `goal-1/` artifacts

rg -n '^\| T[0-9]{2} \|' goal-1/evidence-index.md | wc -l
  45
```

Final Foundation status: **COMPLETE**. Type coverage remains 0 / 45 by design; T01 is the first incomplete stage.
