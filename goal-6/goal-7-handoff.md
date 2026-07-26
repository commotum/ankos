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
G7-01 loci identities/regions + exact Alphabet values
  |
  v
G7-02 Seed/WritableRegion/ReadableRegion contracts + Rule result algebra
  |
  v
G7-03 SimpleProgram + validation + family-blind apply + apply-owned rollout
  |
  v
G7-04A existing-support and visible-control mechanics
  |
  v
G7-04B dynamic-structure and representation-workspace mechanics
  |
  v
G7-04C global/law/intensional mechanics
  |
  v
G7-05 canonical serialization
  |
  v
G7-06 catalog assembly and T migration
  |
  v
G7-07 atomic public/downstream cutover
  |
  v
G7-08 complete conformance
  |
  v
G7-09 documentation, packaging, and cleanup
```

The three G7-04 waves are ordered by reusable capability, not by Book subject
or catalog home. Each wave builds on the prior capability layer. G7-05 follows
the closed semantic variants so codecs are not designed around temporary
records. G7-06 composes already-tested mechanics.

The work occurs on one non-release branch. Before G7-07, the old executor may
remain only as a frozen baseline while the unexported target is assembled. No
new file may call it, adapt to it, or fall back to it. G7-07 deletes it in the
same cutover that exposes the new root surface; no intermediate state is a
release candidate.

## File-Level Migration

### Runtime and package files

| Current or target path | Action | Stage | Final responsibility |
|---|---|---:|---|
| `src/ca/loci.py` | Retain and revise in place | G7-01, G7-04 | Closed identities, occurrences, paths, spans, ports, selectors, lenses, region algebra, and fresh references; replace callable predicates as semantic identity, while finite tensor helpers become representations rather than the ontology |
| `src/ca/alphabets.py` | Retain and revise in place | G7-01, G7-04 | Closed exact scalar and structural value schemas, equality, composition, and represented-number profiles; no mutable `Mapping[str, Any]` identity or silent Python-float exactness |
| `src/ca/seeds.py` | Retain and revise in place | G7-02, G7-04 | Exact, constructive, partial, law-valued, and intensional configuration sources; move current drawing/render/dedupe/catalog-generation work downstream where it is realization rather than denotation |
| `src/ca/frontiers.py` | Retain and replace its contract | G7-02, G7-04 | `WritableRegion`, complete possible-write envelopes, structural capability schemas, fresh namespaces, and composition |
| `src/ca/neighborhoods.py` | Retain and generalize | G7-02, G7-04 | `ReadableRegion`, identity-preserving local/global/historical/structural/differential views, and composition |
| `src/ca/rules.py` | Retain and generalize | G7-02, G7-04 | Closed Rule ASTs/combinators plus Rule results, atoms, total dispositions, outcomes, measures, witnesses, provenance, progress, and continuation; remove callable `fn`, `instantiate`, and `family`/`rule_id` execution dispatch |
| `src/ca/program.py` | Add | G7-03 | Exactly-five-field `SimpleProgram`, compatibility validation, application inputs/results, family-blind `apply`, private reconstruction/commit/quotient, raw trace graph, and callable `rollout` |
| `src/ca/serialization.py` | Add | G7-05 | Versioned fail-closed codecs for every semantic owner; typed decode results; no catalog resolution |
| `src/ca/catalog/entries.py` | Add | G7-06 | Immutable callable-free SPF/F/T/name/source metadata |
| six catalog category files | Add | G7-06 | Canonical whole-program constructors, presets, aliases, and the one lossless compatibility adapter; no execution logic |
| `src/ca/catalog/__init__.py` | Add | G7-06 | Explicit namespace and collision-free convenience re-exports; the sole constructor/metadata join |
| `src/ca/__init__.py` | Replace broad façade atomically | G7-07 | Only core namespaces plus root `SimpleProgram`, `apply`, and callable `rollout` |
| `src/ca/specs.py` | Delete | G7-07 | `Dynamics` and family-string decoding have no target role |
| `src/ca/rollout.py` | Delete physically | G7-07 | Prevent `ca.rollout` submodule shadowing; no old tensor/family branch or `apply_rule` survives |
| `src/ca/datasets.py` | Retain as downstream and revise | G7-07 | Dataset planning/materialization over catalog programs and generic rollout; no family switch or semantic identity |
| `src/ca/rng.py` | Retain as downstream and narrow | G7-07 | Dataset/external realization helpers only; Seed/Rule law identity and replay contracts do not depend on this module |
| `src/ca/viz/__init__.py` | Retain and revise exports | G7-07 | Downstream visualization surface only |
| `src/ca/viz/export.py` | Retain and adapt | G7-07 | Explicit views of rollout or dataset materializations; never a semantic result definition |
| `src/ca/viz/format.py` | Retain unless its independent bundle version requires a documented bump | G7-07 | Visualization wire format only |
| `src/ca/viz/server.py` and `viz/static/*` | Retain | G7-07 | Presentation only |
| `src/ca/py.typed` | Retain unchanged | all | PEP 561 marker |
| `pyproject.toml` | Revise at cutover | G7-07 | Version `0.2.0`, general simple-program description, unchanged `ca` module identity, and test tooling moved out of runtime dependencies |

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
| `tests/test_datasets.py` | Retain and adapt to catalog construction plus downstream materialization |
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
responsibility and test file must exist by G7-08.

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

### G7-01 — Structural identity and exact values

Files: `loci.py`, `alphabets.py`, `tests/test_loci.py`, new
`tests/test_alphabets.py`, and closure helpers.

Implement:

- recognized, versioned structural locus variants for finite coordinates,
  occurrence identity, paths, spans, ports, interfaces, products, continuous
  regions, and intensional references;
- composition, semantic equality, deterministic ordering where declared,
  stable identity, alpha-equivalence contracts, and representation relations;
- exact Alphabet schemas for integers, rationals, modular/algebraic and
  declared real/complex representations, finite enums, tags, products,
  records, words, maps, graphs, fields, instructions, patterns, equations,
  distributions, and symbolic syntax; and
- validation that rejects opaque Python values, callbacks, unknown variants,
  silent float exactness, and ambiguous absence/unknown values.

Exit:

- CT02's primitive closure and negative exactness cases pass;
- canonical equality does not depend on Python object identity, hash order, or
  display form;
- no new file imports `program`, `catalog`, datasets, RNG, or visualization;
  and
- existing finite tensor behavior retained as an explicit representation still
  passes its focused tests.

### G7-02 — Five component contracts and Rule result algebra

Files: `seeds.py`, `frontiers.py`, `neighborhoods.py`, `rules.py`, their
focused tests, and new `tests/test_frontiers.py`.

Implement:

- closed Seed descriptors for exact, constructive, partial, probability-law,
  and intensional initial configurations;
- `WritableRegion` resolution with complete existing/fresh capability
  envelopes, total write schemas, and no read authority;
- `ReadableRegion` resolution from the same immutable snapshot, with no write
  authority;
- sealed Rule descriptors and combinators whose denotation consumes only
  `(R, W)`;
- `RuleComplete`, `RuleRejected`, `RuleFault`, finite/intensional support,
  exact cardinalities, probability laws, `Derivation`/`NoSuccessor`, complete
  dispositions, progress, continuation, witnesses, and provenance; and
- structural compatibility declarations linking Seed output, Alphabet values,
  Frontier capabilities, Neighborhood reads, and Rule's typed join.

Exit:

- component-level CT02 cases and CT05 Rule-side cases pass;
- a bare empty finite Rule support is rejected;
- every omission in a disposition has an explicit closed default;
- Seed and Rule laws contain no draw; and
- component modules remain upstream of `program` and `catalog`.

### G7-03 — Universal application and traversal

Files: new `program.py`, new `tests/test_program.py`, and the application-side
conformance tests.

Implement:

- frozen `SimpleProgram` with exactly the five fields and construction-time
  compatibility validation;
- `ApplicationInput`, canonical lineage, application result sums, applied
  atoms, fresh bindings, reconstruction evidence, successor fibers,
  submeasures, and faults;
- the exact phase order:

```text
Program → Input → Frontier → Neighborhood → Join → Rule denotation
→ Result validation → Fresh binding → Commit → Successor → Quotient/measure
```

- old-snapshot resolution, complete-result validation, deterministic fresh
  binding, per-derivation reconstruction, atomic commit, preserve-outside,
  successor validation, and witness-preserving quotient;
- callable `rollout(program, *, steps, initial=None, replay_key=None)` and raw
  trace records implemented solely by repeated calls to the owned `apply`; and
- typed complete, truncated, and rejected rollout results without confusing a
  horizon or resource bound with terminality.

Exit:

- CT01, CT03, CT04, CT05, CT07, and CT08 pass for generic fixtures;
- deterministic and branching rollout equal manual repeated `apply`;
- a spy and static inspection prove no second one-step path;
- no application branch observes family, carrier, catalog, constructor, Book,
  SPF/F/T, or semantic-category data; and
- no partial branch commits when any atom or phase is invalid.

### G7-04A — Existing-support and visible-control mechanics

Implement reusable descriptors/combinators in the plural component modules
for:

- finite and fixed-support carriers;
- whole-region and coupled writes over already described support;
- local, historical, indexed, and fixed-wiring reads;
- table, totalistic, guarded, phased, instruction, and gate Rules;
- visible head, phase, schedule, cursor, instruction, and mutable-program
  state; and
- one-shot stopped successors.

This wave owns 15 SPF rows listed in the mechanics-assignment table below.
PX09 closes here; other pressure groups close only when their last required
structural or intensional mechanic lands.

Exit:

- those pressure fixtures pass through generic `apply`;
- fixed wiring does not become runtime dispatch;
- mutable code is data in `C` under an immutable interpreter Rule; and
- one-shot success returns a real stopped successor rather than a fake
  trajectory or empty result.

### G7-04B — Dynamic structure, representation workspaces, and branching

Implement reusable mechanics for:

- words, occurrence-preserving splices, generation replacement, graph/tree
  patches, ports/interfaces, fresh children, deletion, and dynamic support;
- match, overlap, collision, ordering, priority, and injury as closed Rule
  data/results rather than commit behavior, except that global priority/injury
  closure lands in G7-04C;
- zero/one/many relational support, witness-bearing branches, and semantic
  successor quotient where finite structural presentation is closed; and
- exact record, tree, interval, history-pointer, region, basis, predictor, and
  aligned-XOR workspaces as distinct Rule skeletons, with the global basis
  exactness boundary completed in G7-04C.

This wave owns 30 SPF rows listed below. It closes PX01, PX02, PX07, and the
primary PX08 set.

Exit:

- fresh identities are traversal, worker, and materialization independent;
- every structural side effect and interface repair is authorized and
  explicit;
- the multiway diamond retains both derivations in one successor fiber; and
- “codec” or “rewrite” purpose creates no shared executor.

### G7-04C — Nonlocal, exact continuous, intensional, and composed-law mechanics

Implement reusable mechanics for:

- global, metric, whole-history, factor, constraint, equation, objective, and
  differential read views;
- exact finite and intensional solution relations;
- probability laws, explicit realization/replay evidence, and tagged
  submeasures;
- event-selected continuous segments, maximal flows, differential fields, and
  explicit represented numerical relations; and
- Rule-owned closed evaluators with visible frames/work state, without
  recursive `apply`; and
- global exact representation transforms plus fair dovetailing, shared
  approximations, priority, and injury.

This wave owns 15 SPF rows listed below. It closes PX03–PX06 and PX10–PX12,
plus all required secondary pressure joins.

Exit:

- no Rule performs a draw, solver search, numerical integration, or ambient
  lookup;
- event time or endpoint is selected only by closed semantics;
- intensional completeness is not confused with enumeration or a cardinality
  guess;
- the unavailable-measure case is limited to the derived measurable quotient;
  and
- F004/F045 have executable commits while F010/F042 remain roles.

### G7-05 — Canonical serialization and representation relations

Files: new `serialization.py`, new `tests/test_serialization.py`, CT09, and
CT10.

Implement:

- canonical tag `ca.simple-program` at schema version `1`;
- a payload with exactly the keys `seed`, `alphabet`, `frontier`,
  `neighborhood`, and `rule`;
- versioned encoding for every public descriptor, Rule/Application/result,
  evidence, law, trace, exact value, structural identity, and intensional AST;
- `Decoded`, `DecodeRejected`, and `DecodeFault`;
- canonical re-encoding, unknown-tag/version/field/primitive rejection,
  forged-digest rejection, and only total validated lossless migrations; and
- explicit inverse-on-image and full-result commutation records for exact
  representations.

Exit:

- CT09 and CT10 pass over every public variant;
- catalog import is blocked during encode/decode tests;
- SPF/F/T IDs, source metadata, invoked spelling, constructor arguments, and
  invocation receipts are absent from program payloads; and
- no 0.1 `Dynamics` manifest is accepted as a canonical program.

### G7-06 — Catalog assembly and exact legacy migration

Files: all eight `catalog/` files, new `tests/test_catalog.py`, CT11, CT14, and
the constructor half of `test_family_coverage.py`.

Implement:

- exactly 60 canonical exact-slug constructors, each once in its primary home;
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
  exact candidate and named-source join retained;
- F010 and F042 are callable-free roles; T08 has zero targets; T40 has two
  named targets; every other T row has one;
- the 49 callable legacy relations count exactly `C=5`, `P=39`, `A=4`,
  `K=1`; all 48 C/P/A spellings are explicit flat exports, K is
  category-qualified only, and M is non-callable;
- T32 and T44 are presets, not aliases;
- every callable expansion is an ordinary validated five-field value and
  passes its exact delegate/binding/translation equality; and
- there is no `construct(id)`, umbrella `kind=`, registration hook, callable
  metadata, or catalog execution path.

### G7-07 — Atomic public and downstream cutover

Files: `__init__.py`, `datasets.py`, `rng.py`, `viz/`, `pyproject.toml`,
current runtime tests, and deletion of `specs.py` and `rollout.py`.

Perform one cutover:

1. migrate the current scalar/Dyad* constructions to direct or catalog
   five-field construction and prove their independent one-step equivalence;
   old `rule_id` values become Rule-constructor data, old
   domain/shape/boundary values become configuration/support/topology data, and
   plural old neighborhoods compose into one `ReadableRegion`;
2. adapt datasets to build programs, supply replay input externally, invoke
   generic rollout, and materialize downstream arrays without a family switch;
3. move dense episode/batch view records to `datasets.py` as
   `DatasetEpisode` and `DatasetBatch`, not semantic core results or root
   exports;
4. adapt visualization to `RolloutResult` and those explicit downstream views;
5. remove root `Dynamics`, `RawEpisode`, `RawBatch`, `dynamics_from_spec`,
   `rollout_batch`, `apply_rule`, `canonical_coords`, and component-constructor
   clutter;
6. delete `specs.py` and physically delete `rollout.py`;
7. export only the agreed root façade and catalog surface; and
8. bump the package to `0.2.0`.

Exit:

- there is exactly one runtime application path;
- `ca.rollout` is callable before and after supported imports, and
  `import ca.rollout` fails because no such submodule exists;
- dataset, RNG, and visualization modules are not imported by semantic core or
  initial root import;
- no current family string or `Rule.family` branch selects behavior;
- current useful native behavior passes through generic application; and
- the obsolete public names and modules fail the explicit negative tests.

### G7-08 — Complete conformance

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

### G7-09 — Documentation, packaging, and cleanup

Files: `README-V2.md`, `api.md`, `simple_programs.md`, public docstrings,
`ref/notes/ca-scaffold.py`, packaging metadata, and the goal index when Goal 7
itself closes.

Actions:

- make `README-V2.md` document the implemented five-field runtime, while
  retaining `README-V1.md` only as an explicitly historical snapshot;
- remove “pending target” language from `api.md` without changing its contract;
- verify conceptual prose and scaffold against exact public signatures,
  ownership, schema version, and catalog exports;
- generate no second API reference or taxonomy document;
- remove dead imports, obsolete family switches, compatibility scaffolding,
  and stale current-runtime examples; and
- run the full test, import, packaging, link, code-fence, formatting, and
  whitespace gates.

Exit:

- a fresh reader sees one implemented API story;
- source, tests, docs, and installed-wheel behavior agree;
- no obsolete module or second executor remains; and
- Goal 7 may be marked complete only under its own separately authorized
  completion contract.

## Exact 60-Family Mechanics Assignment

Every canonical row receives one primary implementation wave. This assignment
tracks the deepest reusable capability required by the family, not its catalog
home or its primary conformance pressure.

| Mechanics wave | Capability boundary | Exact canonical rows |
|---|---|---|
| G7-04A | Existing support, local/fixed topology, and visible finite control | SPF001, SPF003, SPF007, SPF009, SPF010, SPF011, SPF013, SPF026, SPF030, SPF032, SPF035, SPF045, SPF048, SPF050, SPF052 |
| G7-04B | Fresh/deleted support, structural replacement, representation workspaces, and witnessed structural branching | SPF002, SPF004, SPF005, SPF008, SPF012, SPF015, SPF016, SPF019, SPF020, SPF021, SPF022, SPF023, SPF025, SPF028, SPF031, SPF033, SPF034, SPF037, SPF038, SPF040, SPF043, SPF044, SPF046, SPF049, SPF054, SPF055, SPF056, SPF057, SPF059, SPF060 |
| G7-04C | Intensional/global/continuous relations, composed laws, priority/injury, and global representation exactness | SPF006, SPF014, SPF017, SPF018, SPF024, SPF027, SPF029, SPF036, SPF039, SPF041, SPF042, SPF047, SPF051, SPF053, SPF058 |

Counts are `15 + 30 + 15 = 60`, with no duplicate or omission. G7-06 then
assembles the canonical constructor for every row from its implemented
mechanics.

The conformance pressures close at these mechanics gates:

| Pressure | Mechanics-ready stage |
|---|---:|
| PX01 coupled writes | G7-04B |
| PX02 variable structure | G7-04B |
| PX03 nonlocal reads | G7-04C |
| PX04 zero/one/many | G7-04C |
| PX05 continuous | G7-04C |
| PX06 stochastic | G7-04C |
| PX07 mutable program state | G7-04B |
| PX08 one-shot primary set | G7-04B |
| PX09 fixed gates | G7-04A |
| PX10 distinct codecs | G7-04C |
| PX11 shared priority | G7-04C |
| PX12 observer boundary | G7-04C |

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
| CT01 exact five-field boundary | G7-03; public half G7-07 | Exactly five dataclass fields; catalog values are ordinary programs; root signatures exact |
| CT02 descriptor closure/compatibility | G7-01–02; all variants G7-06 | Recursive closed tags/versions/exactness and every positive/negative cross-field compatibility clause |
| CT03 validation/no-commit failure | G7-03 | Exact phase order; first fault wins; no partial result or commit |
| CT04 atomic application | G7-03; pressures G7-04A/B | Total dispositions, authorized writes, preserve-outside, no hidden collision/repair |
| CT05 outcomes/cardinalities | G7-02–03; relations G7-04B/C | All outcome distinctions and three independent cardinalities |
| CT06 probability/Seed replay | G7-04C | Law/draw separation, Seed realization, replay evidence, submeasures, narrow unavailable view |
| CT07 fresh identities | G7-03; structures G7-04B | Deterministic binding, collision rejection, traversal independence, retained raw identities |
| CT08 witnesses/quotient | G7-03; branching G7-04B | Pre-quotient witnesses/fibers, semantic equality, measure aggregation |
| CT09 serialization | G7-05; full variants G7-06 | Exact fail-closed round trip of every public semantic record; five-key payload |
| CT10 representation commutation | G7-05; mechanics G7-04B/C | Inverse-on-image and complete one-step result commutation |
| CT11 catalog/T migration | G7-06 | Exact row manifest, callable kinds, targets, bindings, owners, and exports |
| CT12 independent equivalence | Oracles G7-00; execution G7-07–08 | Independent complete-result reference cases across required mechanics |
| CT13 imports/no dispatch | Each stage; final G7-07–08 | Dependency DAG, blocked catalog, one apply path, root/submodule/signature contract |
| CT14 observer boundary | G7-04C and G7-06 | F004/F045 executable; F010/F042 roles; tooling cannot affect identity/application |
| 60-family coverage | Mechanics G7-04; constructors G7-06; execution G7-08 | Exact constructor, descriptor, metadata, provenance, and generic fixture join |

G7-08 reruns all obligations together; it does not postpone their first
implementation until the end.

## Goal 2 Strengths: Explicit Destinations

| Preserved strength | Implementation owner | Proof owner |
|---|---|---|
| Closed versioned structural descriptors and validation | G7-01–02 semantic owners | CT02, CT09 |
| No callbacks, `Any`, `eval`, formula strings, host CAS, generators, or iterator escape | G7-01–04 closed variants | CT02, CT13 |
| Exact numeric semantics; no silent float fallback | `alphabets.py`, closed Rule/value data | CT02, CT09–10 |
| Visible head/control/instruction/phase/schedule/program state | Seed-produced `C`, G7-04A mechanics | PX01, PX07–09 |
| Visible laws, entropy boundary, and replay evidence | `seeds.py`, `rules.py`, `program.py` | CT06 |
| One generic branch-free application path | `program.py`; old executor deleted G7-07 | CT03–04, CT13 |
| Typed cardinality/outcome/failure/witness/lineage/provenance | `rules.py` and `program.py` | CT05, CT08–09 |
| Witnesses retained before successor deduplication | `program.py` quotient | CT08 |
| Raw structural traces before tensor/rendered views | `program.py`; downstream adapters | CT12–14 |
| Inverse-on-image and full-result one-step commutation | semantic representation records | CT10 |
| Lossless codecs, unknown-tag failure, derived IDs/digests | `serialization.py` | CT09 |
| Presets construct data; no executor registry | `catalog/` explicit callables | CT11, CT13 |
| In-place migration with no second/fallback executor | G7-07 cutover | CT12–13 |
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
| `Dynamics` façade | None. `Dynamics` cannot by itself losslessly supply Seed, Alphabet, or the moved configuration structure. Delete it at G7-07 rather than preserve a misleading partial program |
| `dynamics_from_spec` and 0.1 manifests | Retire. They were construction recipes, not a canonical codec. Document a one-time source migration to catalog constructors or explicit five-field construction; `serialization.loads` rejects them |
| Canonical serialization | First canonical schema is `ca.simple-program` version `1`; there is no version-0 semantic payload to migrate |
| Package version | Ship the breaking pre-1.0 cutover as `0.2.0` |
| `RawEpisode` / `RawBatch` | Remove from semantic core and root. Dense dataset views become downstream `DatasetEpisode` / `DatasetBatch`; canonical traversal returns `program.RolloutResult` |
| `rollout_batch` | Remove from core/root. Dataset batching is external iteration/materialization over the one rollout path |
| `apply_rule` | Remove. One-step semantics are only `program.apply` |
| `canonical_coords` | Remove from root. Coordinate/tensor materialization remains a loci/dataset/viz representation helper |
| public `rollout.py` | Physically delete; do not merely omit from `__all__` and do not retain the old executor in a private module |
| `Frontier` / `Neighborhood` class names | Retire them at the 0.2.0 cutover. Their old meanings are not lossless spelling aliases. Canonical owner-module names are only `WritableRegion` / `ReadableRegion`; the stored field names remain `frontier` / `neighborhood` |
| `time_slice` frontier | Do not preserve as an alias because its old firing-source/implicit-next-time meaning is not the new writable-envelope contract. Migrate callers to an exact writable-region constructor such as `everywhere` or the appropriate structural envelope |
| `seeds.render(..., rng=None)` | Remove as semantic behavior. Explicit downstream realization requires a replay/sampler input and returns evidence; deterministic view materialization may remain downstream |
| broad root constructors/types | Remove at G7-07. Component constructors are module-qualified; whole-program names are under `ca.catalog` |
| current Dyad*/AR2 names | Retain only as closed component presets or catalog programs where their expansion meets the new contracts; never as root executors or family switches |
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
- core never imports catalog, datasets, RNG helpers, or visualization;
- serialization never imports catalog or reconstructs a constructor call;
- category modules never import `catalog.entries`; `catalog.__init__` is the
  sole join;
- catalog metadata contains no callable or semantic object;
- no callback, hidden solver, ambient draw, silent float, partial branch
  commit, inferred structural repair, or result-policy keyword appears;
- F045 evaluator code is closed Rule data with visible work state and never
  recursively calls `apply`; and
- the test oracle never calls the implementation it judges.

## Final Goal 7 Completion Gate

Goal 7 is complete only when:

1. the target files and exports match this handoff;
2. `specs.py` and public `rollout.py` are absent;
3. exactly one application law exists and rollout demonstrably reuses it;
4. CT01–CT14 and the 60-family coverage test pass;
5. all exact SPF/F/T counts, homes, callable kinds, exports, and role
   boundaries match `catalog-migration.md`;
6. current useful native behavior commutes with generic semantics through
   independent full-result tests;
7. the canonical codec is fail-closed, five-key, alias-independent, and
   catalog-free;
8. datasets, RNG, and visualization remain downstream with no semantic or
   executor authority;
9. source, installed wheel, public signatures, docs, and reference scaffold
   agree; and
10. one final hostile review finds no covert sixth field, second executor,
    family dispatch, lossy compatibility path, or missing audited family.

If a concrete audited family breaks the contract, stop and report the exact
counterexample. Do not add a sixth field, family switch, compatibility engine,
or new taxonomy to make a test green.
