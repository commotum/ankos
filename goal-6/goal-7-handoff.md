# Goal 7 Implementation Handoff

Status: **Goal 6 final contract; Goal 7 not started**

This handoff turns the settled five-field architecture into one implementation
sequence. It is deliberately mechanics-first: shared descriptors and one
application law are implemented before whole-program names. Catalog categories
organize discovery only after the mechanics exist.

Nothing in this document authorizes implementation. Goal 7 requires a separate
user instruction and scaffold.

## Authoritative Inputs

Goal 7 reads these sources in order:

1. [architecture.md](architecture.md) for semantic contracts, application,
   ownership, and dependency direction;
2. [catalog-migration.md](catalog-migration.md) for the exact 60-family,
   constructor, source, export, and T01–T45 ledger;
3. [conformance.md](conformance.md) for PX01–PX12, CT01–CT14, and the exact
   SPF coverage join;
4. [api.md](../api.md) for public Python spelling;
5. [simple_programs.md](../simple_programs.md) for the conceptual explanation;
6. [ca-scaffold.py](../ref/notes/ca-scaffold.py) for a compact code-shaped
   projection; and
7. [Goal 5's integration handoff](../goal-5/integration-handoff.md) only when
   checking the remaster boundary.

Goal 5 remains semantic authority. Goal 2 is frozen evidence for the preserve
items listed below. Goal 4 and Book rediscovery are outside Goal 7.

## Target Outcome

Goal 7 ships one immutable program value:

```python
SimpleProgram(
    seed=...,
    alphabet=...,
    frontier=...,
    neighborhood=...,
    rule=...,
)
```

and one authoritative one-step operation:

```python
apply(program, input)
```

`rollout` repeatedly invokes that owned operation. Every one of the 60
canonical catalog constructors returns an ordinary expanded `SimpleProgram`.
No family, catalog ID, carrier label, constructor spelling, codec tag, or
legacy name selects an executor.

The final semantic package surface is:

```text
src/ca/
├── __init__.py
├── program.py
├── loci.py
├── alphabets.py
├── seeds.py
├── frontiers.py
├── neighborhoods.py
├── rules.py
├── serialization.py
├── py.typed
└── catalog/
    ├── __init__.py
    ├── entries.py
    ├── automata.py
    ├── substitua.py
    ├── machina.py
    ├── media.py
    ├── criteria.py
    └── dynamica.py
```

Current auxiliary `datasets.py`, `rng.py`, and `viz/` files remain downstream
consumers during Goal 7. They are not added to the semantic dependency graph
or promised as part of the new root façade.

## Dependency DAG

```text
G7-00 frozen behavior and independent test oracles
  |
  v
G7-01 atomic five-field core cutover
       (structural kernel → component contracts → Rule algebra → apply/rollout
        → current native presets → root/downstream/tests → delete old executor)
  |
  v
G7-02 reusable mechanics closure for all 60 rows
       (three mechanics workstreams; one aggregate completion barrier)
  |
  v
G7-03 canonical serialization and representation relations
  |
  v
G7-04 catalog assembly and exact T migration
  |
  v
G7-05 complete conformance
  |
  v
G7-06 documentation, packaging, and cleanup
```

G7-01 is intentionally one atomic stage even though its work is internally
dependency-ordered. The actual repository import chain makes smaller completed
stages dishonest: replacing loci/component/Rule contracts while retaining
`Dynamics`, `specs.py`, and the old executor would either break the active
suite or require a parallel compatibility architecture. No G7-01 substep is a
merge/release boundary.

G7-02 contains three mechanics workstreams, but they share one completion
barrier. A row's workstream is its primary implementation/test owner, not a
claim that the family has no cross-workstream dependencies. G7-03 follows the
closed semantic variants so codecs are not designed around temporary records.
G7-04 only composes already-tested mechanics.

G7-00 through G7-05 are internal implementation checkpoints, not release
candidates. Although G7-01 sets the source version for the breaking cutover,
only the fully reconciled G7-06 state may be packaged or shipped as `0.2.0`.

## File-Level Migration

### Runtime and package files

| Current or target path | Action | Stage | Final responsibility |
|---|---|---:|---|
| `src/ca/loci.py` | Retain and revise in place | G7-01, G7-02 | Closed identities, occurrences, paths, spans, ports, selectors, lenses, region algebra, and fresh references; replace callable predicates as semantic identity, while finite tensor helpers become representations rather than the ontology |
| `src/ca/alphabets.py` | Retain and revise in place | G7-01, G7-02 | Closed exact scalar and structural value schemas, equality, composition, and represented-number profiles; no mutable `Mapping[str, Any]` identity or silent Python-float exactness |
| `src/ca/seeds.py` | Retain and revise in place | G7-01, G7-02 | Exact, constructive, partial, law-valued, and intensional configuration sources; current drawing/render/dedupe/catalog-generation work moves to the exact downstream owners fixed below |
| `src/ca/frontiers.py` | Retain and replace its contract | G7-01, G7-02 | `WritableRegion`, complete possible-write envelopes, structural capability schemas, fresh namespaces, and composition |
| `src/ca/neighborhoods.py` | Retain and generalize | G7-01, G7-02 | `ReadableRegion`, identity-preserving local/global/historical/structural/differential views, and composition |
| `src/ca/rules.py` | Retain and generalize | G7-01, G7-02 | Closed Rule ASTs/combinators plus Rule results, atoms, total dispositions, outcomes, measures, witnesses, provenance, progress, and continuation; remove callable `fn`, `instantiate`, and `family`/`rule_id` recipe bags and execution dispatch |
| `src/ca/program.py` | Add | G7-01 | Exactly-five-field `SimpleProgram`, cross-field compatibility validation, Seed binding/realization evidence, application inputs/results, family-blind `apply`, private reconstruction/commit/quotient, raw trace graph, replay derivation, and callable `rollout` |
| `src/ca/serialization.py` | Add | G7-03 | Versioned fail-closed codecs for every semantic owner; typed decode results; no catalog resolution |
| `src/ca/catalog/entries.py` | Add | G7-04 | Immutable callable-free SPF/F/T/name/source metadata |
| six catalog category files | Add | G7-04 | Canonical whole-program constructors, presets, aliases, and the one lossless compatibility adapter; no execution logic |
| `src/ca/catalog/__init__.py` | Add | G7-04 | Explicit namespace and collision-free convenience re-exports; the sole constructor/metadata join |
| `src/ca/__init__.py` | Replace broad façade atomically, then add catalog/codec namespaces | G7-01, G7-03–04 | Only core namespaces plus root `SimpleProgram`, `apply`, and callable `rollout` |
| `src/ca/specs.py` | Delete | G7-01 | `Dynamics` and family-string decoding have no target role |
| `src/ca/rollout.py` | Delete physically | G7-01 | Prevent `ca.rollout` submodule shadowing; no old tensor/family branch or `apply_rule` survives |
| `src/ca/datasets.py` | Retain as downstream and revise | G7-01 | Four explicit dataset recipe builders, Seed realization requests, tensor projection/materialization, dataset episode/batch views, and external batching over generic rollout; no executor dispatch |
| `src/ca/rng.py` | Retain as downstream and narrow | G7-01 | Dataset planning helpers only; core replay coordinates/evidence are owned by `program.py` |
| `src/ca/viz/__init__.py` | Retain and revise exports | G7-01 | Downstream visualization surface only |
| `src/ca/viz/export.py` | Retain and adapt | G7-01 | Accept explicit dataset tensor views for viewer bundle v1; never infer a tensor projection from an arbitrary semantic result |
| `src/ca/viz/format.py` | Retain unchanged at bundle version 1 | G7-01 | Independent visualization wire format; not canonical semantic serialization |
| `src/ca/viz/server.py` and `viz/static/*` | Retain unchanged | G7-01 | Presentation only |
| `src/ca/py.typed` | Retain unchanged | all | PEP 561 marker |
| `pyproject.toml` and `uv.lock` | Revise together | G7-01, G7-06 | Version `0.2.0`, general simple-program description, unchanged `ca` module identity, and pytest moved to `[dependency-groups].dev` |

The target adds no public `configuration.py`, `regions.py`, `replacement.py`,
`results.py`, `engine.py`, `rollout.py`, `run.py`, `updates.py`, or second
package tree. With the current auxiliary files retained, ten semantic/catalog
files added, and `specs.py`/`rollout.py` removed, the tracked `src/ca` file
count moves from 20 to 28.

### Existing test disposition

| Current path | Goal 7 disposition |
|---|---|
| `tests/test_loci.py` | Retain and broaden from finite coordinates to structural identity/region invariants; keep current tensor cases as representation tests |
| `tests/test_neighborhoods.py` | Retain and migrate to `ReadableRegion`; preserve exact current stencil cases where they remain valid |
| `tests/test_rules.py` | Retain and expand around closed Rule descriptors and result algebra |
| `tests/test_seeds.py` | Retain and replace ambient RNG/render assumptions with closed Seed-law and explicit realization tests |
| `tests/test_specs.py` | Delete after its useful manifest cases become negative cutover tests in serialization/public-surface suites |
| `tests/test_rollout.py` | Rewrite around `SimpleProgram`, `apply`, and apply-owned rollout; move only independently derived expected steps into CT12 oracles |
| `tests/test_datasets.py` | Retain and adapt at G7-01 to direct program recipes plus downstream materialization; after G7-04, add catalog-delegate/equality cases without moving mechanics into the catalog |
| `tests/test_rng.py` | Retain for external deterministic helpers; assert the semantic core does not import it |
| `tests/test_viz_export.py` | Retain and adapt to explicit downstream view records |

Add:

```text
tests/test_alphabets.py
tests/test_frontiers.py
tests/test_program.py
tests/test_serialization.py
tests/test_public_api.py
tests/test_catalog.py
tests/conformance/
├── helpers.py
├── test_program_boundary.py
├── test_descriptor_closure.py
├── test_validation_phases.py
├── test_atomic_application.py
├── test_outcome_cardinality.py
├── test_probability_replay.py
├── test_fresh_identity.py
├── test_witness_quotient.py
├── test_serialization_contract.py
├── test_representation_commutation.py
├── test_catalog_expansion.py
├── test_native_generic_equivalence.py
├── test_import_and_dispatch.py
├── test_observer_boundary.py
└── test_family_coverage.py
```

Exact helper spelling may stay private, but each named conformance
responsibility and test file must exist by G7-05.

## Ordered Implementation Stages

### G7-00 — Freeze behavior and independent oracles

Purpose: preserve useful current behavior without preserving its architecture.

Actions:

- record the Goal 6 close commit, Python/NumPy versions, the 102-test baseline,
  and current tree identities;
- transcribe tiny independent one-step oracles for current scalar, cellular,
  and multidimensional examples into test-only code;
- add independent tiny expected results for mobile/Turing, substitution,
  multiway, constraint, variable-support, stochastic, and
  differential/intensional cases from `conformance.md`;
- prohibit test oracles from importing future `program.apply`, catalog
  constructors, runtime rule evaluators, or private commit helpers; and
- record the precise current public exports and obsolete modules for the later
  negative cutover test.

Exit:

- the existing 102 tests pass;
- every future CT12 oracle has an independently specified expected result or a
  named exact fixture;
- no runtime file changes; and
- the oracle dependency check proves independence.

### G7-01 — Atomic five-field core cutover

This stage is one non-splittable migration transaction. Its internal order is:

```text
loci + Alphabet kernel
→ local Seed/WritableRegion/ReadableRegion contracts
→ Rule denotation/result algebra
→ SimpleProgram/application/Seed binding/rollout
→ current native component presets
→ root + datasets/RNG/viz + active tests
→ physical old-executor deletion
```

Files:

- revise `loci.py`, `alphabets.py`, `seeds.py`, `frontiers.py`,
  `neighborhoods.py`, `rules.py`, `__init__.py`, `datasets.py`, `rng.py`,
  `viz/__init__.py`, and `viz/export.py`;
- add `program.py`, `tests/test_alphabets.py`, `tests/test_frontiers.py`,
  `tests/test_program.py`, and the initial CT01–CT08/CT12/CT13 tests;
- delete `specs.py`, `rollout.py`, and `tests/test_specs.py`;
- rewrite the obsolete portions of `tests/test_seeds.py`,
  `tests/test_rules.py`, `tests/test_rollout.py`, `tests/test_datasets.py`,
  and `tests/test_viz_export.py`; and
- update `pyproject.toml` and `uv.lock` together.

Implement the structural kernel:

- recognized, versioned identities for finite coordinates, occurrences, paths,
  spans, ports, interfaces, products, continuous regions, and intensional
  references;
- exact Alphabet schemas for scalar, represented numeric, tag, product,
  record, word, map, graph, field, instruction, pattern, equation,
  distribution, and symbolic values; and
- semantic equality independent of object identity, hash order, storage order,
  or display form.

Implement local component contracts:

- exact, constructive, partial, law-valued, and intensional Seeds;
- `WritableRegion` complete existing/fresh capability envelopes;
- `ReadableRegion` identity-preserving views from the same immutable snapshot;
- sealed Rule ASTs/combinators, finite/intensional support, exact
  cardinalities, laws, total dispositions, derivations/no-successor atoms,
  progress, continuation, witnesses, provenance, and Rule faults; and
- local schema/requirement declarations only. Components do not import one
  another downstream to perform five-way validation.

Implement `program.py`:

- frozen `SimpleProgram` with exactly five fields;
- cross-field unification and ephemeral compatibility evidence;
- `ApplicationInput`, application result sums, reconstruction evidence,
  fresh bindings, successor fibers, measures, lineage, and faults;
- the exact validation/commit/quotient phase order from `architecture.md`;
- family-blind `apply` with old-snapshot resolution, total-result validation,
  per-derivation reconstruction, atomic preserve-outside commit, successor
  validation, and witness-preserving quotient; and
- callable `rollout(program, *, steps, initial=None, replay_key=None)` that
  traverses only through the owned `apply`.

`rollout(initial=None)` first denotes and validates the program Seed source
space. With no key it retains the complete finite/intensional initial
space/law. With an authorized key it realizes only a realizable Seed law using
closed sampler/profile data and structurally derived replay coordinates,
recording the chosen source and evidence. An explicit `initial` bypasses Seed
realization and is validated normally. Replay derivation lives in
`program.py`; core never imports current `rng.py`.

Preserve the useful current experiments only as module-qualified component
presets:

```text
rules:
  ar2_modular_0d, dyadlags_0d, lagcounts_0d,
  dyadrads_1d, dyadaxes_2d, dyadaxes_3d

neighborhoods:
  ar2_0d, dyadlags_0d, lagcounts_0d,
  dyadrads_1d, dyadaxes_2d, dyadaxes_3d
```

Each Rule constructor receives its concrete `rule=` construction data before
application. None becomes a root export or an unaudited catalog entry.
`datasets.py` owns four explicit recipe builders keyed by the four existing
dataset IDs; recipe selection chooses constructors, never an executor. Every
builder returns an ordinary validated program before rollout.

Fix downstream ownership in the same transaction:

- remove public `seeds.render`, `seeds.dedupe`, and bulk `seeds.structured`;
  dataset-only structured recipe enumeration/deduplication moves to private
  `datasets._structured_seed_recipes` helpers, while semantic Seed
  denotation/realization remains in `program.py`;
- keep finite selector/materializer internals private to `loci.py`; move the
  current trajectory tensor projection and canonical coordinate-table helper
  to private dataset view code;
- define non-root `datasets.DatasetEpisode` and `DatasetBatch` as explicit
  tensor views produced from rollout traces; downstream batching loops/stacks
  generic rollout and never owns one-step semantics;
- preserve `ankos.viz.bundle` version 1 exactly. `viz.export` accepts only
  explicit `DatasetEpisode`/`DatasetBatch` tensor views and keeps legacy wire
  labels `RawEpisode`/`RawBatch`, `domain`, `rule_id`, shape, and coordinates
  as presentation metadata. It rejects an arbitrary `RolloutResult` until a
  caller supplies a supported explicit dataset projection; and
- keep `viz/format.py`, viewer JavaScript, server, and static assets unchanged.

Perform the cutover:

- narrow root to the available target core namespaces plus
  `SimpleProgram`, `apply`, and callable `rollout`; add serialization/catalog
  namespaces only when those files land;
- remove root `Dynamics`, `RawEpisode`, `RawBatch`, `dynamics_from_spec`,
  `rollout_batch`, `apply_rule`, `canonical_coords`, and flattened component
  constructors;
- physically delete `specs.py` and `rollout.py`;
- set package version `0.2.0`, update the general description, and move
  `pytest>=9.0.3` from runtime dependencies to
  `[dependency-groups].dev`; and
- replace every obsolete active test in this same stage. No knowingly red test
  interval or preserved compatibility structure is allowed.

Exit:

- the complete active suite is green;
- there is exactly one executable one-step law and no production copy of the
  current tensor/family kernels;
- current native fixtures match independent complete-result oracles;
- `ca.rollout` is callable and `import ca.rollout` fails because the physical
  submodule is gone;
- initial root import does not load datasets, RNG, or visualization;
- component schemas contain no callback, opaque `Any`, mutable recipe bag,
  ambient entropy, or semantic `family`/`name`/`params` dispatch;
- sealed generic AST/result-variant interpretation remains allowed in its
  owning semantic module, but `apply` contains no family/carrier/catalog
  algorithm switch; and
- CT01 and the kernel cases of CT02–CT08, CT12, and CT13 pass.

### G7-02 — Reusable mechanics closure

This stage changes `loci.py`, the five plural component modules, and focused
conformance tests. `program.py` changes only to correct a generic contract bug;
it never acquires family behavior. No catalog file exists yet.

Three primary workstreams assign every row exactly once:

- **M-A — coupled/existing-support/control:** finite and fixed carriers,
  whole-region/local/historical/indexed/fixed-wiring reads, coupled
  source/destination effects, tables, gates, instructions, visible phase/head/
  cursor/program state, and stopped one-shot successors;
- **M-B — dynamic structure/branching/representation work:** words, splices,
  generations, trees, graphs, ports, fresh/delete support, matches, overlap,
  structural output workspaces, and witnessed branching; and
- **M-C — global/intensional/law:** metric and whole-history dependency views,
  finite/intensional solution relations, continuous domains/events/flows/
  fields, probability laws, explicit realization evidence, exact/lossy
  representation relations, closed evaluators, priority, and injury.

Defining predicates, constraints, equations, objectives, flow laws, and
differential relations are closed Rule data. Neighborhoods expose only the
values, dependency scopes, geometry, side data, factor inputs, and differential
germs those Rules read.

Every new sealed variant must enter a codec-inventory checklist with its tag,
version, exact fields, local validator, equality law, and intended owner.
G7-03 implements the cross-cutting codecs; no variant may reach the catalog
without passing that inventory.

Stage-local tests:

- M-A: `test_atomic_application.py`, `test_outcome_cardinality.py`, current
  native oracle cases, and its assigned PX fixtures;
- M-B: `test_atomic_application.py`, `test_fresh_identity.py`,
  `test_witness_quotient.py`, `test_representation_commutation.py`, and its PX
  fixtures; and
- M-C: `test_outcome_cardinality.py`, `test_probability_replay.py`,
  `test_representation_commutation.py`, `test_observer_boundary.py`, and its
  PX fixtures.

The stage has one aggregate completion barrier: all three workstreams, all
twelve PX categories, and all required secondary joins pass through the same
generic application before G7-02 is complete. A workstream assignment is a
primary ownership/test destination, not a claim that a family has no
cross-workstream dependency.

The SPF-row owner owns that family's direct construction fixture and dominant
mechanical skeleton. The PX lead owns the shared cross-family pressure
invariant and suite. Both obligations land before the aggregate barrier, so
these two ownership views never create separate readiness claims.

Exit:

- all 60 mechanics assignments below are implemented without a family-named
  runtime class or executor;
- dynamic identities, interfaces, conflicts, schedules, laws, global reads,
  continuous/intensional results, mutable program state, and one-shot outcomes
  satisfy their pressure invariants;
- no Rule performs a draw, solver search, numerical integration, recursive
  `apply`, or ambient lookup;
- F004/F045 have executable commits while F010/F042 remain roles; and
- the full active suite remains green with exactly one application path.

General numerical solvers and integrators are not core runtime services.
Constraints, equations, objectives, flows, and differential laws ship as
exact or intensional Rule denotations. A finite numerical realization, when
desired, belongs to separately versioned external tooling and returns
evidence naming its method, parameters, tolerances, precision, and source
denotation. Tiny exact fixtures establish conformance; performance choices may
change realization cost but never program denotation, equality, or exact
outcomes.

### G7-03 — Canonical serialization and representation relations

Files: new `serialization.py`, root namespace update, new
`tests/test_serialization.py`, CT09, and CT10.

Implement:

- canonical tag `ca.simple-program` at schema version `1`;
- a payload with exactly the keys `seed`, `alphabet`, `frontier`,
  `neighborhood`, and `rule`;
- versioned encoding for every codec-inventory entry, Rule/Application/result,
  evidence, law, trace, exact value, structural identity, and intensional AST;
- `Decoded`, `DecodeRejected`, and `DecodeFault`;
- canonical re-encoding, unknown-tag/version/field/primitive rejection,
  forged-digest rejection, and only total validated lossless migrations; and
- inverse-on-image and full-result commutation records for exact
  representations.

Exit:

- every G7-01/02 codec-inventory entry is covered and CT09/CT10 pass;
- semantic owners do not import serialization;
- catalog import is impossible because the package does not yet exist;
- SPF/F/T IDs, source metadata, invoked spelling, constructor arguments, and
  invocation receipts are absent from program payloads; and
- no 0.1 `Dynamics` manifest is accepted as a canonical program.

### G7-04 — Catalog assembly and exact legacy migration

Files: all eight `catalog/` files, root catalog namespace, new
`tests/test_catalog.py`, CT11, CT14, and the constructor half of
`test_family_coverage.py`.

Implement:

- exactly 60 canonical exact-slug constructors, each once in its primary home;
- one explicit, closed Python signature and closed-parameter validator for
  every canonical constructor; no constructor accepts `*args`, `**kwargs`, an
  opaque recipe bag, ignored keywords, or silent coercions;
- immutable callable-free `FamilyEntry`, `RoleEntry`, `LegacyEntry`,
  `LegacyTarget`, and `NameEntry` values;
- canonical, preset, alias, and compatibility callables as explicit ordinary
  functions composing the existing component mechanics;
- explicit flat catalog exports and category namespaces, with no dynamic
  registry or synthesized function; and
- the exact T01–T45 migration ledger from `catalog-migration.md`.

Exit:

- SPF IDs are exactly SPF001–SPF060 and home counts are exactly
  `11 automata / 15 substitua / 8 machina / 14 media / 9 criteria /
  3 dynamica`;
- coverage is exactly 19 covered and 41 additions;
- executable audit IDs are exactly F001–F009, F011–F038, F040–F041, and
  F043–F063; F010/F042 are the two close roles and F039 remains unused;
- legacy dispositions count exactly 15 retain-family, 21 retain-preset,
  2 merge, 3 repair, 2 alias, 1 retire-role, and 1 split, with each row's
  exact candidate and named-source join retained, except for T08's explicit
  no-candidate/no-Book-construction-anchor role disposition;
- F010 and F042 are callable-free roles; T08 has zero targets; T40 has two
  named targets; every other T row has one;
- the 49 callable legacy relations count exactly `C=5`, `P=39`, `A=4`,
  `K=1`; all 48 C/P/A spellings are explicit flat exports, K is
  category-qualified only, and M is non-callable;
- T32 and T44 are presets, not aliases;
- every callable expansion is an ordinary validated five-field value and
  passes its exact delegate/binding/translation equality; and
- every constructor composes only G7-02 semantic variants already present in
  G7-03's completed codec inventory; discovering a missing mechanic reopens
  G7-02 and G7-03 before catalog work resumes; and
- there is no `construct(id)`, umbrella `kind=`, registration hook, callable
  metadata, or catalog execution path.

### G7-05 — Complete conformance

Complete the normative `tests/conformance/` layout and run:

- CT01–CT14;
- the primary SPF001–SPF060 family join;
- all eight required secondary pressure joins;
- the exact T01–T45 expected manifest;
- independent native/generic full-result oracles;
- static import/no-dispatch checks;
- blocked-catalog apply/decode checks;
- public signature and submodule-shadow checks; and
- wheel/install/type-marker smoke tests.

Exit:

- all fourteen suites and all 60 canonical family rows pass;
- every source result, applied derivation, no-successor atom, measure,
  witness, fresh binding, lineage, fiber, and cardinality comparison is full,
  not state-only;
- no test oracle shares implementation with the code it judges; and
- no expected unsupported backend is disguised as semantic undefinedness,
  exact zero, divergence, or completion.

### G7-06 — Documentation, packaging, and cleanup

Files: `README-V2.md`, `api.md`, `simple_programs.md`, public docstrings,
`ref/notes/ca-scaffold.py`, `pyproject.toml`, `uv.lock`, and the goal index when
Goal 7 itself closes.

Actions:

- make `README-V2.md` document the implemented five-field runtime, while
  retaining `README-V1.md` only as an explicitly historical snapshot;
- add the promised 0.1 source-migration note to `README-V2.md` and `api.md`:
  callers reconstruct programs through catalog constructors or explicit
  five-field construction; old `Dynamics` manifests are not canonical input;
- remove “pending target” language from `api.md` without changing its contract;
- verify conceptual prose and scaffold against exact public signatures,
  ownership, schema version, and catalog exports;
- generate no second API reference or taxonomy document;
- remove dead imports, obsolete family switches, compatibility scaffolding,
  and stale current-runtime examples; and
- run the full test, import, lockfile, packaging, link, code-fence, formatting,
  and whitespace gates.

Exit:

- a fresh reader sees one implemented API story;
- source, tests, lockfile, docs, and installed-wheel behavior agree;
- no obsolete module or second executor remains; and
- Goal 7 may be marked complete only under its own separately authorized
  completion contract.

## Exact 60-Family Mechanics Assignment

Every canonical row receives one primary G7-02 workstream owner. This is the
dominant implementation/test destination, not a claim that the family has no
dependency on another workstream. No workstream is independently complete;
all three share the G7-02 aggregate barrier.

| G7-02 workstream | Primary capability ownership | Exact canonical rows |
|---|---|---|
| M-A | Existing support, local/fixed topology, coupled effects, and visible finite control | SPF001, SPF003, SPF007, SPF009, SPF010, SPF011, SPF013, SPF026, SPF030, SPF032, SPF035, SPF045, SPF048, SPF050, SPF052 |
| M-B | Fresh/deleted support, structural replacement, representation workspaces, and witnessed structural branching | SPF002, SPF004, SPF005, SPF008, SPF012, SPF015, SPF016, SPF019, SPF020, SPF021, SPF022, SPF023, SPF025, SPF028, SPF031, SPF033, SPF034, SPF037, SPF038, SPF040, SPF043, SPF044, SPF046, SPF049, SPF054, SPF055, SPF056, SPF057, SPF059, SPF060 |
| M-C | Intensional/global/continuous relations, composed laws, priority/injury, and global representation exactness | SPF006, SPF014, SPF017, SPF018, SPF024, SPF027, SPF029, SPF036, SPF039, SPF041, SPF042, SPF047, SPF051, SPF053, SPF058 |

Counts are `15 + 30 + 15 = 60`, with no duplicate or omission. G7-04 then
assembles the canonical constructor for every row from its implemented
mechanics.

The conformance pressures have these lead workstreams, but all close only at
the single G7-02 barrier:

| Pressure | Lead workstream | Completion stage |
|---|---|---:|
| PX01 coupled writes | M-A with M-B structural support | G7-02 |
| PX02 variable structure | M-B | G7-02 |
| PX03 nonlocal reads | M-C | G7-02 |
| PX04 zero/one/many | M-C with M-B branching | G7-02 |
| PX05 continuous | M-C | G7-02 |
| PX06 stochastic | M-C | G7-02 |
| PX07 mutable program state | M-A + M-B | G7-02 |
| PX08 one-shot | M-A + M-B, with M-C secondary cases | G7-02 |
| PX09 fixed gates | M-A | G7-02 |
| PX10 distinct codecs | M-B + M-C | G7-02 |
| PX11 shared priority | M-C | G7-02 |
| PX12 observer boundary | M-B + M-C | G7-02 |

Required secondary tests remain:

- SPF018 also runs PX03;
- SPF039 also runs PX04; and
- SPF012, SPF013, SPF014, SPF024, SPF035, and SPF042 also run PX08.

F010 and F042 have no SPF and remain callable-free role entries. T08 remains a
retired Seed role. Those roles are not added to the 60-row implementation
count.

## Conformance Ownership

| Suite | First authoritative stage | Final obligation |
|---|---:|---|
| CT01 exact five-field boundary | G7-01; catalog assertion G7-04 | Exactly five dataclass fields; catalog values are ordinary programs; root signatures exact |
| CT02 descriptor closure/compatibility | G7-01; all mechanics variants G7-02 | Recursive closed tags/versions/exactness and every positive/negative cross-field compatibility clause |
| CT03 validation/no-commit failure | G7-01 | Exact phase order; first fault wins; no partial result or commit |
| CT04 atomic application | G7-01; all pressure variants G7-02 | Total dispositions, authorized writes, preserve-outside, no hidden collision/repair |
| CT05 outcomes/cardinalities | G7-01; all relation variants G7-02 | All outcome distinctions and three independent cardinalities |
| CT06 probability/Seed replay | Generic boundary G7-01; mechanics G7-02 | Law/draw separation, Seed realization, replay evidence, submeasures, narrow unavailable view |
| CT07 fresh identities | G7-01; structural variants G7-02 | Deterministic binding, collision rejection, traversal independence, retained raw identities |
| CT08 witnesses/quotient | G7-01; branching variants G7-02 | Pre-quotient witnesses/fibers, semantic equality, measure aggregation |
| CT09 serialization | G7-03 | Exact fail-closed round trip of every public semantic record; five-key payload |
| CT10 representation commutation | Mechanics claims G7-02; codecs/full proof G7-03 | Inverse-on-image and complete one-step result commutation |
| CT11 catalog/T migration | G7-04 | Exact row manifest, callable kinds, targets, bindings, owners, and exports |
| CT12 independent equivalence | Oracles G7-00; core G7-01; final G7-05 | Independent complete-result reference cases across required mechanics |
| CT13 imports/no dispatch | Every stage; final G7-05 | Dependency DAG, blocked catalog, one apply path, root/submodule/signature contract |
| CT14 observer boundary | Mechanics G7-02; role/catalog surface G7-04 | F004/F045 executable; F010/F042 roles; tooling cannot affect identity/application |
| 60-family coverage | Mechanics G7-02; constructors G7-04; final G7-05 | Exact constructor, descriptor, metadata, provenance, and generic fixture join |

G7-05 reruns all obligations together; it does not postpone their first
implementation until the end.

## Goal 2 Strengths: Explicit Destinations

| Preserved strength | Implementation owner | Proof owner |
|---|---|---|
| Closed versioned structural descriptors and validation | G7-01–02 semantic owners | CT02, CT09 |
| No callbacks, `Any`, `eval`, formula strings, host CAS, generators, or iterator escape | G7-01–04 closed variants | CT02, CT13 |
| Exact numeric semantics; no silent float fallback | `alphabets.py`, closed Rule/value data | CT02, CT09–10 |
| Visible head/control/instruction/phase/schedule/program state | Seed-produced `C`, G7-02 M-A/M-B mechanics | PX01, PX07–09 |
| Visible laws, entropy boundary, and replay evidence | `seeds.py`, `rules.py`, `program.py` | CT06 |
| One generic branch-free application path | `program.py`; old executor deleted G7-01 | CT03–04, CT13 |
| Typed cardinality/outcome/failure/witness/lineage/provenance | `rules.py` and `program.py` | CT05, CT08–09 |
| Witnesses retained before successor deduplication | `program.py` quotient | CT08 |
| Raw structural traces before tensor/rendered views | `program.py`; downstream adapters | CT12–14 |
| Inverse-on-image and full-result one-step commutation | semantic representation records | CT10 |
| Lossless codecs, unknown-tag failure, derived IDs/digests | `serialization.py` | CT09 |
| Presets construct data; no executor registry | `catalog/` explicit callables | CT11, CT13 |
| In-place migration with no second/fallback executor | G7-01 atomic cutover | CT12–13 |
| Typed unsupported/undefined instead of defaults | Rule/Application fault and outcome sums | CT03, CT05 |
| Canonical Book sources for claims without rediscovery | callable-free `entries.py` metadata | CT11 and 60-family join |

The superseded Goal 2 axes are negative gates: no public `Domain`,
`ConfigurationSchema`, `Update`, `UpdatePolicy`, construction-class hierarchy,
family registry executor, or constraint/function/PDE sibling ontology may
appear.

## Compatibility, Versioning, and Cutover Decisions

These decisions are closed; Goal 7 does not reopen them for convenience.

| Question | Decision |
|---|---|
| `Dynamics` façade | None. `Dynamics` cannot by itself losslessly supply Seed, Alphabet, or the moved configuration structure. Delete it at G7-01 rather than preserve a misleading partial program |
| `dynamics_from_spec` and 0.1 manifests | Retire. They were construction recipes, not a canonical codec. Document a one-time source migration to catalog constructors or explicit five-field construction; `serialization.loads` rejects them |
| Canonical serialization | First canonical schema is `ca.simple-program` version `1`; there is no version-0 semantic payload to migrate |
| Package version | Ship the breaking pre-1.0 cutover as `0.2.0` |
| `RawEpisode` / `RawBatch` | Remove from semantic core and root. Dense dataset views become downstream `DatasetEpisode` / `DatasetBatch`; canonical traversal returns `program.RolloutResult` |
| `rollout_batch` | Remove from core/root. Dataset batching is external iteration/materialization over the one rollout path |
| `apply_rule` | Remove. One-step semantics are only `program.apply` |
| `canonical_coords` | Remove from root. Canonical coordinate tables and trajectory tensor projections become private dataset-view helpers; finite selector materialization remains private to `loci.py` |
| public `rollout.py` | Physically delete; do not merely omit from `__all__` and do not retain the old executor in a private module |
| `Frontier` / `Neighborhood` class names | Retire them at the 0.2.0 cutover. Their old meanings are not lossless spelling aliases. Canonical owner-module names are only `WritableRegion` / `ReadableRegion`; the stored field names remain `frontier` / `neighborhood` |
| `time_slice` frontier | Do not preserve as an alias because its old firing-source/implicit-next-time meaning is not the new writable-envelope contract. Migrate callers to an exact writable-region constructor such as `everywhere` or the appropriate structural envelope |
| `seeds.render`, `seeds.dedupe`, bulk `seeds.structured` | Remove as public Seed behavior. Program-owned Seed realization requires an authorized key and returns evidence; dataset-only structured recipe enumeration/deduplication becomes private dataset helpers |
| broad root constructors/types | Remove at G7-01. Component constructors are module-qualified; whole-program names are under `ca.catalog` |
| current Dyad*/AR2 names | Retain exactly six Rule presets—`ar2_modular_0d`, `dyadlags_0d`, `lagcounts_0d`, `dyadrads_1d`, `dyadaxes_2d`, `dyadaxes_3d`—and six corresponding Neighborhood presets—`ar2_0d`, `dyadlags_0d`, `lagcounts_0d`, `dyadrads_1d`, `dyadaxes_2d`, `dyadaxes_3d`. They remain module-qualified components, never root exports, unaudited catalog rows, executors, or family switches |
| catalog compatibility | Implement exactly the catalog ledger. T10's `extended_mobile_automaton` is the sole `K`, category-qualified and deprecated; no additional guessed legacy callables |
| alias lifetime | True `A` aliases and declared `P` presets are stable catalog API. No temporary component type aliases are shipped |
| datasets | Retain current module during Goal 7, but build explicit programs and use generic rollout; no family strings choose mechanics |
| RNG helpers | Retain downstream only. Core laws and replay are owned by closed semantic records and application evidence |
| visualization | Retain downstream adapters and bundle tooling; views never define semantic results or influence application |
| invocation provenance | Optional user manifests stay outside canonical serialization and program equality |
| unexpected external 0.1 artifacts | A separately authorized offline, version-pinned source converter may emit canonical expanded payloads if real artifacts later require it; it is never imported by `ca`, is not `ca.compat`, and cannot become a fallback decoder |

There is no compatibility executor, dual decoder, silent old-manifest default,
or `try new then fall back to old` path.

## Stage-Wide No-Cheating Gates

At every stage:

- `SimpleProgram` has exactly five stored fields;
- configuration/support/topology/boundary/control remain within Seed-produced
  configuration data and shared structural contracts;
- Frontier is the full possible-write envelope, not the set that fires;
- Rule owns applicability, schedule, conflict, stochastic law, stopping, and
  total replacement semantics;
- application owns only generic validation/reconstruction/commit/quotient;
- `apply` does not dispatch on locus kind, Rule tag, family, carrier, or
  catalog identity. An owning component module may interpret its own sealed
  generic AST/result variants without selecting a second application law;
- the static import DAG is enforced: `loci`, `alphabets`, `seeds`,
  `frontiers`, and `neighborhoods` do not import `rules`, `program`, or
  catalog; `rules` does not import `program` or catalog; semantic owners never
  import `serialization`; `program` and `serialization` never import catalog;
  internals never import root `ca`; and core never imports datasets, RNG, or
  visualization;
- core never imports catalog, datasets, RNG helpers, or visualization;
- serialization never imports catalog or reconstructs a constructor call;
- category modules never import `catalog.entries`; `catalog.__init__` is the
  sole join;
- catalog metadata contains no callable or semantic object;
- no callback, hidden solver, ambient draw, silent float, partial branch
  commit, inferred structural repair, or result-policy keyword appears;
- F045 evaluator code is closed Rule data with visible work state and never
  recursively calls `apply`; and
- the test oracle never calls the implementation it judges;
- the complete active suite is green at every completed stage; and
- Goal 2 and Goal 5 remain byte-for-byte frozen throughout Goal 7.

## Final Goal 7 Completion Gate

Goal 7 is complete only when:

1. the target files and exports match this handoff;
2. `specs.py` and public `rollout.py` are absent;
3. exactly one application law exists and rollout demonstrably reuses it;
4. CT01–CT14, PX01–PX12, all eight named secondary pressure joins, and the
   60-family coverage test pass;
5. all exact SPF/F/T counts, homes, callable kinds, exports, and role
   boundaries match `catalog-migration.md`;
6. current useful native behavior commutes with generic semantics through
   independent full-result tests;
7. the canonical codec is fail-closed, five-key, alias-independent, and
   catalog-free;
8. datasets, RNG, and visualization remain downstream with no semantic or
   executor authority;
9. source, installed wheel, public signatures, docs, reference scaffold,
   `pyproject.toml`, and `uv.lock` agree; and
10. one final hostile review finds no covert sixth field, second executor,
    family dispatch, lossy compatibility path, or missing audited family.

If a concrete audited family breaks the contract, stop and report the exact
counterexample. Do not add a sixth field, family switch, compatibility engine,
or new taxonomy to make a test green.
