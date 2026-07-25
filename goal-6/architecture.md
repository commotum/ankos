# Goal 6 Architecture

Status: **IN PROGRESS — CUTOVER COMPLETE; CONTRACTS NEXT**

This is the evolving canonical architecture specification for Goal 6. It
records settled decisions and points to later-stage artifacts rather than
duplicating the completed taxonomy.

## Purpose

Remaster the frozen Goal 2 implementation plan around one ordinary program
value:

```python
SimpleProgram(
    seed=...,
    alphabet=...,
    frontier=...,
    neighborhood=...,
    rule=...,
)
```

Goal 6 specifies this architecture and the mechanics-first implementation plan.
It does not change runtime behavior. Goal 7 will implement the result only
after separate authorization.

## Source Authority

| Priority | Source | Governing responsibility |
|---:|---|---|
| 1 | `goal-5/taxonomy-census.md` | Final counts and catalog scope |
| 1 | `goal-5/11-FAMILIES.md` | Family identities, boundaries, sources, and mechanics |
| 2 | `goal-5/api-pressure.md` | Five-field fit and family-by-family pressure |
| 3 | `goal-5/integration-handoff.md` | Remaster boundary and Goal 2 preserve/replace decisions |
| 4 | `goal-5/10-RECONCILE.md` | Exact T01–T45 dispositions |
| 5 | `goal-5/source-decision-matrix.csv` | Source traceability only when a decision needs it |
| 6 | `simple_programs.md`, `api.md`, `ref/notes/ca-scaffold.py` | Design inputs to clarify during Goal 6 |
| 7 | `goal-2/goal-2-handoff.md` | Frozen details for conclusions explicitly preserved by Goal 5 |

When sources conflict, the more authoritative Goal 5 result wins. A newly
identified canonical-source contradiction is escalated; implementation
convenience, current code, old plan detail, or naming preference cannot
override the completed audit.

Goal 4's plans, tools, ledgers, searches, and verification machinery have no
role in this architecture. No Book rediscovery is required.

## Settled Program Boundary

`SimpleProgram` stores exactly:

1. `seed`
2. `alphabet`
3. `frontier`
4. `neighborhood`
5. `rule`

`C`, `V`, `W`, and `R` are relationships among component types, not stored
axes. Configuration structure, support, topology, geometry, boundary behavior,
control, schedule, and visible entropy are data produced by `Seed` and
interpreted by the five components. Run horizon, query/solver strategy,
realization, replay key, resources, tracing, observation, rendering, and export
are invocation or tooling concerns.

Frontier is the complete possible-write envelope. Neighborhood is the readable
region. Rule is the closed relation that owns applicability, scheduling,
conflict, stochastic, result, and update semantics. Generic application
validates and atomically commits Rule results; it does not supply a sixth policy
axis.

These decisions are fixed by Goal 5. Their detailed protocols are the work of
Stages 2 and 3.

## Document Ownership

| Artifact | Role |
|---|---|
| `goal-6/0-plan.md` | Completion contract and staged strategy |
| `goal-6/0-loop.md` | Execution protocol and stage template |
| `goal-6/architecture.md` | Canonical internal architecture and ownership decisions |
| `api.md` | Stage 4 target: clean public API contract; currently a design input |
| `simple_programs.md` | Stage 4 target: conceptual specification/rationale without a competing API |
| `ref/notes/ca-scaffold.py` | Stage 4 target: one compact code-shaped architecture walkthrough |
| `goal-6/catalog-migration.md` | Stage 5 canonical 60-family/T01–T45 catalog mapping |
| `goal-6/conformance.md` | Stage 6 paper fixtures and Goal 7 test obligations |
| `goal-6/goal-7-handoff.md` | Stage 7 file-level implementation plan |
| `goal-2/` | Frozen historical comparison baseline; never current instructions |
| `GOALS.md` | Live status and execution sequence only |

Stage reports record evidence. They do not become competing specifications.

## Goal 2 Decision Ledger

The Goal 5 integration handoff already resolved the old plan's architecture.
This ledger makes every major Goal 2 concern explicit without importing its
obsolete stage machinery.

### Preserve

| Goal 2 conclusion | Goal 6 disposition |
|---|---|
| Closed structural descriptors with explicit validation and versions | Preserve across all five components and their codecs |
| No unrestricted callbacks, `Any`, `eval`, formula text, host CAS objects, generators, or iterator escape hatches | Preserve as a public semantic-data invariant |
| Exact integers, rationals, algebraic/declared representations, and no silent float fallback | Preserve in Alphabet/configuration structures and Rule data/results |
| Visible head, control, instruction, phase, schedule, and stored-program state | Preserve as ordinary tagged configuration/program data |
| Visible and replayable randomness | Preserve as explicit Seed laws or Rule probability/draw evidence |
| One generic branch-free application path | Preserve and generalize to every executable family |
| Typed cardinality, outcomes, failures, witnesses, lineage, and provenance | Preserve in the Rule codomain and application result |
| Derivation witnesses before successor deduplication | Preserve exactly |
| Raw structural traces before coordinate/tensor/rendered views | Preserve at the run/tooling boundary |
| Representation inverse-on-image and one-step full-result commutation | Preserve as conformance obligations |
| Versioned lossless codecs, unknown-tag failure, and derived rather than authoritative IDs/digests | Preserve in root `serialization.py` |
| Presets construct ordinary program data and never register executors | Preserve; named whole-program constructors move to `catalog/` |
| In-place migration with no second executor or fallback semantic path | Preserve for Goal 7 cutover planning |
| Typed unsupported/undefined results instead of invented defaults | Preserve and refine in Stages 2–3 |
| Canonical Book sources for preset claims and fixtures | Preserve for provenance; do not redo discovery |

### Replace

| Goal 2 element | Goal 6 replacement |
|---|---|
| Public `DOMAIN` axis | Carrier/support/topology/geometry descriptors in Seed-produced configuration and shared loci structures |
| Public `CONFIGURATION_SCHEMA` axis | Type relationship `C` and validated configuration data produced by `Seed`, not a sixth field |
| Fixed or scalar-centric value/carrier assumptions | Structural Alphabet/configuration schemas spanning words, trees, graphs, products, fields, and intensional objects |
| Firing-source `FRONTIER` | Complete writable capability envelope, including possible destinations and fresh/deleted components |
| Offset/snapshot-only `NEIGHBORHOOD` | Arbitrary typed readable region, local or nonlocal, structural or differential |
| Rule as proposal producer without commit semantics | Closed Rule relation returning complete atomic replacements and typed results |
| Public `UPDATE`/`UpdatePolicy` axis | Rule-owned scheduling/conflict/update semantics plus one invariant generic atomic commit |
| Separate sibling ontology for constraints, functions, constants, and PDEs | Ordinary five-field one-shot or iterated programs; query/realization policy remains outside the program |
| Fixed `Z4`, finite coordinates, one scalar per cell, and mandatory synchronous steps | General structural/intensional loci and configuration carriers |
| Construction-named runtime classes and family registry execution | Structural constructors returning ordinary `SimpleProgram` values; metadata never dispatches |
| T08 initial-condition “family” | `Seed` constructors/laws/realizations |
| Observers, renderers, properties, and representations treated as families | Tooling, views, metadata, or separate transforms when they have their own mechanics |
| Hidden solver behavior or untyped empty successor sets | Explicit run policy, evidence, cardinality, outcome, and terminal/undefined distinctions |
| Goal 2's 45-row implementation scope | All 60 executable families, two close-role boundaries, and the exact T01–T45 migration |
| Goal 2's chapter/type-oriented stage plan | Mechanics-first Goal 7 dependency plan |

### Defer Without Losing the Decision

| Question | Destination |
|---|---|
| Exact five component protocols and cross-field validation | Stage 2 |
| Lazy/intensional writable and readable regions, including how Rule exposes actual applicability inside the writable envelope | Stages 2–3 |
| Complete Rule result algebra and application pseudocode | Stage 3 |
| Fresh-identity allocation, overlapping-write ordering, and validation before/after commit | Stage 3 |
| Entropy authority across Seed laws, stochastic Rule laws, replay evidence, and external run requests | Stages 2–3 |
| Final ownership of helper/result types without public module inflation | Stage 4 |
| Root exports, alias spelling, and `ca.rollout` surface | Stage 4 |
| Stable catalog IDs, canonical constructor names, and six-module placement | Stage 5 |
| Legacy source/capability boundaries for adaptive subdivision, sequential network schedules, weak PDEs, and exact transcendental execution | Stages 5–6 |
| Pressure fixtures, codec/replay/commutation tests, and hostile review | Stage 6 |
| Compatibility, the optional `Dynamics` façade, deprecation, serialization cutover, and exact file migration | Stage 7 |
| Generation, datasets, streams, RNG-helper placement, visualization, and export internals | Goal 7 or later, except for stable public boundaries |
| Numerical/solver backend selection and performance strategy | Goal 7 implementation; exactness and evidence contracts are already fixed |

### Old Module-Area Coverage

This table proves that no Goal 2 subsystem is silently unreviewed.

| Goal 2 area | Disposition |
|---|---|
| `domains.py` | Public area rejected; structural responsibility moves under Seed/configuration/loci |
| `alphabets.py`, `values.py` | Semantic work preserved and generalized; final public ownership is `alphabets.py` plus structural values |
| `configurations.py` | Public axis/module not presumed; semantic work belongs to Seed outputs and shared structures |
| `loci.py` | Preserved and generalized as the common locus/region algebra |
| `frontiers.py` | Preserved file, replaced firing-source contract |
| `neighborhoods.py` | Preserved file, generalized read contract |
| `rules.py`, `updates.py` | Rule descriptors preserved; update semantics absorbed into Rule/results and generic commit |
| `seeds.py` | Preserved and generalized from event-zero data to configuration sources/laws |
| `outcomes.py`, `traces.py` | Semantics preserved; Stage 4 decides minimal ownership without presuming public files |
| `expressions.py`, `relations.py`, `queries.py` | Closed data strengths preserved; sibling ontology rejected in favor of five-field programs and external run/query policy |
| `serialization.py` | Preserved as a root cross-cutting codec boundary |
| `specs.py` | Replaced by `program.py` and `SimpleProgram` |
| `rollout.py` | Generic traversal intent preserved; exact file/public ownership settled in Stage 4 |
| `datasets.py`, `rng.py`, `viz/` | Downstream behavior preserved until Goal 7; internal reorganization deferred |
| `tests/conformance/` | One-obligation rigor preserved, expanded and reorganized around reusable mechanics and 60-family coverage |

Goal 2's original deferred list is also resolved: stochastic and native
continuous mechanics are now required by the 60-family inventory; specific
unsupported source profiles remain typed rather than guessed; weak/approximate
PDE and transcendental backends remain exactness/evidence questions; and the
old “outside the 45 rows” boundary is replaced by the completed 60-family
census.

## Stage 1 Repository Baseline

Captured before Goal 6 execution edits:

| Evidence | Baseline |
|---|---|
| Git `HEAD` | `318a5383cea0898421db3993257e5aec24b7f7dd` |
| Initial worktree | Clean |
| `src/ca` tree | `6e6b34769d60508c03d0a69fad1ede4fef75e217` |
| `tests` tree | `02ad081e039a46efbf61855fdeae60abb7bb70ad` |
| `goal-2` tree | `48b6309655ec7c1d3aaa1a0ec5dfb700385e16d1` |
| Goal 2 handoff SHA-256 | `5792ac1810dafdd0be6343e1d03c4b1ab20c48551efd73400fea5a1812a9f192` |
| Goal 2 README SHA-256 | `e063609c7a52d32bd0a4d3bb384cd5da233c34f57a169e2db6cce197c76e0c4d` |
| Runtime test command | `uv run pytest -q tests` |
| Runtime test result | `102 passed in 1.10s` |

The tracked runtime has 20 files under `src/ca` and nine test files under
`tests`. The package is `ankos` 0.1.0, exposes module `ca`, requires Python
3.10+, and currently depends on NumPy.

The live API still exports `Dynamics`, `RawEpisode`, and `RawBatch`.
`Dynamics` stores `domain`, `shape`, `rule`, plural `neighborhoods`, `frontier`,
`boundary`, and metadata. `specs.py` decodes a small family registry, and
`rollout.py` provides the current tensor-oriented execution path. Rule-family
branches are present in `rollout.py`, with construction-time family decoding in
`specs.py` and dataset-family selection in `datasets.py`; these are baseline
migration targets, not acceptable parts of the remastered executor.

### Existing Pieces to Evolve In Place

- plural `alphabets.py`, `seeds.py`, `frontiers.py`, `neighborhoods.py`, and
  `rules.py`;
- the shared selector work in `loci.py`;
- the public `rollout` concept;
- `py.typed`; and
- downstream `datasets.py`, `rng.py`, and `viz/`, whose internals are deferred.

### Target Pieces Not Yet Present

- `program.py` and `SimpleProgram`;
- root `serialization.py`;
- `catalog/` and its agreed entry/category modules;
- five-field result/application semantics; and
- the remastered 60-family constructors and conformance coverage.

The current tests do not directly cover Alphabet or Frontier contracts and have
no `SimpleProgram`, catalog, serialization, five-field result-algebra, or
60-family coverage suites. Those omissions become Goal 7 test obligations
after Goal 6 specifies them.

This is expected migration evidence, not a defect to repair during Goal 6.
The final Goal 6 audit compares `src/ca`, `tests`, and Goal 2 against the hashes
above.

## Remaining Architecture Sections

The following sections become authoritative only when their named stage closes:

- Stage 2 — component protocols, shared locus algebra, configuration ownership,
  structural forms, and serialization constraints;
- Stage 3 — result algebra, atomic application, and run/tool boundary;
- Stage 4 — exact file ownership, public imports, documentation, and reference
  scaffold;
- Stage 5 — catalog construction and migration;
- Stage 6 — pressure fixtures and conformance;
- Stage 7 — implementation handoff and final reconciliation.
