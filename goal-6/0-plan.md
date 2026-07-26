# Goal 6: Five-Field Architecture Remaster

Shorthand: **Architecture Remaster**

## Big-Picture Objective

Remaster the frozen Goal 2 architecture and implementation plan around:

```python
SimpleProgram(
    seed=...,
    alphabet=...,
    frontier=...,
    neighborhood=...,
    rule=...,
)
```

The result must be an implementation-ready design for the agreed package and
catalog structure, covering all 60 executable semantic families established by
Goal 5. Goal 5 supplies the semantic truth and API pressure; Goal 2 is only a
frozen source of explicitly reusable design work.

Goal 6 is an architecture, documentation, conformance-design, and implementation
planning goal. It may update planning/reference documentation, but it does not
begin the behavioral implementation under `src/ca`. That work belongs to a
separately authorized Goal 7.

## Authority and Scope

Use the following source order:

1. `goal-5/taxonomy-census.md` and `goal-5/11-FAMILIES.md` define the final
   inventory: 60 executable semantic families and two close non-family roles.
2. `goal-5/api-pressure.md` defines the family-by-family pressure on the
   five-field abstraction.
3. `goal-5/integration-handoff.md` defines how to integrate those results into
   a remastered architecture and what may be recovered from Goal 2.
4. `goal-5/10-RECONCILE.md` defines the exact T01–T45 migration obligations.
5. `goal-5/candidates.md` and `goal-5/source-decision-matrix.csv` are consulted
   only when a catalog or conformance decision needs candidate-level mechanics
   or source traceability.
6. `simple_programs.md`, `api.md`, and `ref/notes/ca-scaffold.py` are design
   inputs to be clarified and remastered, not independent authorities over the
   completed Goal 5 findings.
7. `goal-2/goal-2-handoff.md` is a frozen comparison baseline. Recover only the
   preserve-list identified by the Goal 5 integration handoff; do not revive
   superseded architecture merely because Goal 2 specified it in more detail.

Do not reopen the Book taxonomy, reread the Book for discovery, or import Goal
4's audit machinery. A concrete contradiction in a canonical source may be
recorded and escalated; implementation inconvenience and naming preference are
not reasons to reopen Goal 5.

## Non-Negotiable Constraints

1. **Exactly five stored program fields.** The public program contract is
   `seed`, `alphabet`, `frontier`, `neighborhood`, and `rule`.
   Configuration, carrier, support, topology, boundary behavior, schedule,
   outcome, time, solver policy, observer policy, and randomness may be typed
   data or run concerns, but are not additional `SimpleProgram` fields.
2. **Seed owns initial configurations.** `Seed` may be exact, constructive,
   partial, or probabilistic. The configuration it produces carries support,
   topology, geometry, defaults, invariants, and visible control state. Do not
   add `configuration.py` merely to house those ideas.
3. **Alphabet is structural.** `Alphabet` describes closed value structure,
   including finite, numeric, tagged, product, word, graph, field,
   instruction, probability, and symbolic values.
4. **Frontier means writable envelope.** It is the complete region a rule is
   authorized to create, remove, replace, or relabel this application—not a
   separate selector of loci that happen to fire.
5. **Neighborhood means readable region.** It may be local, global, historical,
   graph-relative, metric, differential, structured, dynamic, or intensional.
6. **Rule owns update semantics.** `Rule` is a closed relation from the readable
   view to complete atomic replacements of the writable envelope. Scheduling,
   conflict resolution, stochastic choice, and simultaneous commit semantics
   belong to its closed data and result relation, not to `UpdatePolicy`.
7. **One family-blind application law.** The generic application operation may
   validate types and writes, but must not switch on catalog ID, family name,
   semantic class, carrier kind, or Book chapter.
8. **Closed, serializable representations.** Preserve Goal 2's commitment to
   structural descriptors, exact numeric semantics, lossless versioned codecs,
   explicit representation relations, visible entropy/control state, and
   unknown-tag failure. No unrestricted callbacks, `Any`, hidden host-language
   evaluation, silent float fallback, or general CAS escape hatch.
9. **Results retain semantics.** The rule/result algebra must distinguish zero,
   one, and many replacements; quiescence, termination, invalidity,
   undefinedness, and divergence/resource exhaustion; probabilities and replay
   evidence; derivation witnesses before successor deduplication; exact fresh
   identities; and symbolic or intensional results.
10. **Sixty families are coverage, not classes.** All 60 executable families
    must map to the architecture and catalog, but named constructors return
    ordinary `SimpleProgram` values. Do not build 60 runtime subclasses or a
    parallel semantic ontology.
11. **Catalog is navigation and construction.** Each family has one canonical
    home in the agreed six-module catalog. Presets, compatibility names, and
    aliases remain explicit metadata and constructors, never engine dispatch.
12. **Preserve Goal 2 unchanged.** Record a compact preserve/replace/defer
    disposition in Goal 6; do not rewrite the frozen handoff.
13. **Exclude Goal 4 ceremony.** Do not create audit ledgers, transaction
    histories, search archives, replay frameworks, bespoke paragraph
    dispositions, or generalized verification infrastructure.
14. **Core and catalog first.** Settle the core public API, file ownership, and
    catalog. Keep generation, datasets, streams, RNG placement, visualization,
    and export internals outside this goal except where a minimal public
    boundary is required for the Goal 7 plan.
15. **Locked names require evidence to change.** The agreed core and catalog
    names below remain fixed unless an actual family counterexample makes them
    incoherent. Aesthetic reconsideration alone is out of scope.
16. **Planning only.** Goal 6 may change `GOALS.md`, root design documentation,
    Goal 6 documents, and the reference scaffold. It must not make behavioral
    changes under `src/ca`, migrate runtime data, or start Goal 7.
17. **Lean artifacts.** Reuse Goal 5's completed tables rather than recreating
    semantic fingerprints. Prefer a few canonical documents and exact matrices
    over duplicated prose or tooling.
18. **No false completion.** An unmapped family, unresolved T01–T45
    disposition, contradictory public document, unspecified result case,
    family-dependent engine branch, or vague Goal 7 stage keeps Goal 6 open.

## Locked Target Surface

The architecture must organize around this core and catalog:

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

The plural component modules expose constructor algebras whose composed values
fill one corresponding `SimpleProgram` field. `loci.py` owns the shared
region/locus algebra. `program.py` owns `SimpleProgram` and the smallest
family-blind application contract justified by the design. `serialization.py`
owns cross-cutting wire/storage codecs without becoming a sixth field.

The catalog names have these stable navigation meanings:

| Module | Dominant construction mechanic |
|---|---|
| `automata.py` | Persistent carriers updated in place or in parallel |
| `substitua.py` | Matched structure replaced, grown, deleted, or branched |
| `machina.py` | Visible heads, control states, instructions, stacks, or schedules |
| `media.py` | Information transformed between distinct representations |
| `criteria.py` | Admissibility, constraints, witnesses, solutions, or weighted alternatives |
| `dynamica.py` | Continuous differential, field, event, or flow laws |

This grouping is for discovery and constructor ownership. It is not a runtime
type hierarchy, and secondary traits belong in metadata rather than duplicate
homes.

The intended public reading remains:

```python
import ca

program = ca.SimpleProgram(
    seed=ca.seeds.bernoulli(...),
    alphabet=ca.alphabets.boolean(),
    frontier=ca.frontiers.everywhere(),
    neighborhood=ca.neighborhoods.eca(),
    rule=ca.rules.elementary(30),
)

same_program = ca.catalog.eca(rule=30)
episode = ca.rollout(same_program, steps=100)
```

`ca.rollout` is a public run/tooling boundary, not a sixth program component.
Goal 6 must specify its relationship to one-step application, while avoiding
premature decisions about the eventual organization of datasets, generators,
streams, RNG helpers, or visualization.

## Current Facts

- Goal 5 is complete and reports 60 executable families plus two close
  non-family roles.
- Nineteen of those executable families are represented by the current
  T01–T45 catalog in some form; 41 are missing.
- T01–T45 require exact retain-family, retain-preset, merge, repair, alias,
  retire-role, and split dispositions recorded in the Goal 5 handoff.
- Goal 5 found no family counterexample to the five-field model.
- The frozen Goal 2 handoff contains useful work on structural descriptors,
  exact codecs, results, provenance, generic application, and conformance, but
  its public axes and sibling ontologies are superseded.
- The current repository already has a working `src/ca` package with plural
  component modules and rollout/tooling code. Goal 7 should evolve it in place
  rather than create a second runtime.
- `api.md` now states the settled target public contract,
  `simple_programs.md` explains the five-field model without a competing
  executor, and `ref/notes/ca-scaffold.py` walks the same architecture from
  closed loci through components, catalog construction, application, rollout,
  and serialization.
- `GOALS.md` now records Goal 5 as complete, Goal 6 as the active remaster, and
  Goal 7 as future implementation. Goal 4 is explicitly superseded and Goal 2
  remains frozen evidence.
- Stage 1 is complete. `goal-6/architecture.md` records the source hierarchy,
  document roles, an exhaustive Goal 2 preserve/replace/defer ledger, and the
  clean runtime/test/frozen-plan baseline at commit
  `318a5383cea0898421db3993257e5aec24b7f7dd`.
- The Stage 1 runtime baseline is 102 passing tests, `src/ca` tree
  `6e6b34769d60508c03d0a69fad1ede4fef75e217`, and `tests` tree
  `02ad081e039a46efbf61855fdeae60abb7bb70ad`.
- Stage 2 is complete. `goal-6/architecture.md` now defines
  `SimpleProgram[C, V, W, R]`, the five component protocols, configuration
  ownership, shared loci/region algebra, singular composition, four validation
  layers, exact fail-closed serialization, and five construction-class paper
  type-checks split into six concrete fixtures.
- The full 60-family API mapping yielded no sixth-field counterexample. F010
  remains a wrapper role and F042 an observer role unless either is explicitly
  constructed as an ordinary result-writing program.
- Frontier and Neighborhood resolve independently from the same immutable
  configuration but share its snapshot binding and canonical locus identities.
  Rule declares their typed join; Frontier grants no read capability and
  Neighborhood grants no write capability.
- The canonical Rule signature consumes `R` and `W`, not unrestricted `C`.
  Every alternative already denotes a total disposition over `W`, and static
  requirements prove or obligate both read and effect containment.
- Stage 3 is complete. The architecture now fixes sound-and-covering finite or
  intensional Rule results, typed outcomes and cardinalities, total
  dispositions, application-private closed reconstruction, phase-wide atomic
  application, witness-before-quotient semantics, probability/replay/fresh
  identity, and the application/rollout boundary.
- A hostile recheck and refreshed F001–F063 pressure scan found no
  application-semantic counterexample among all 60 executable families. F010
  and F042 remain close roles rather than executable families.
- Stage 2 deliberately left `api.md`, `simple_programs.md`, and
  `ref/notes/ca-scaffold.py` unchanged until application semantics closed;
  Stage 4 has now replaced all three in place as coherent projections of the
  canonical architecture.
- Stage 2 verification passed all 102 runtime tests, whitespace/diff checks,
  frozen Goal 2 hashes, and a hostile recheck of all 15 challenged contract
  points.
- Stage 3 began from clean autosave commit
  `96305d34cf2fb097e9d45e161375ebd20bf45999` and changed planning
  documentation only. Runtime/test/Goal 2 trees and frozen hashes remain at
  their Stage 1 values; the 102-test baseline was not rerun for docs-only work.
- Stage 4 (`4-SURFACE`) is complete. It began after autosave commit
  `53e813ddd251541e035b4f3e632133e215a6043b` and changed only the eight
  expected planning, public-documentation, README, and reference-scaffold
  files.
- Stage 4 assigns Rule-side sums to `rules.py`, application and rollout sums
  plus both public operations to `program.py`, codec results to
  `serialization.py`, component construction to the plural modules, and
  whole-program construction to the catalog. Distinct result sums avoid a
  dependency cycle, and retiring the public `rollout.py` module avoids
  shadowing callable `ca.rollout`.
- The published/current and retained runtime READMEs are explicitly marked as
  runtime snapshots with a pointer to the pending target contract; neither can
  now be mistaken for Goal 7 architecture.
- The final Stage 4 scaffold compiles and executes, whitespace and scoped-diff
  checks pass, and independent API and concept/scaffold hostile reviews report
  no remaining blocker. Runtime, test, Goal 2, and Goal 5 trees are unchanged.
- Stage 5 (`5-CATALOG`) is complete. It began from clean autosave commit
  `954a30467eb5e0c3892e5a8c4f920b505b2a16b8` and produced the exact
  60-family/SPF and T01–T45 implementation map, candidate/source crosswalk,
  callable/export policy, and callable-free metadata contract.
- Stage 5 changed only the seven expected planning/API/reference files. Exact
  count and Goal 5 comparisons, the executable reference scaffold, two
  independent hostile reviews, whitespace, paths, and frozen-tree checks pass.
  Runtime, tests, Goal 2, Goal 5, and Stage 6–7 artifacts remain unchanged.
- Stage 6 (`6-CONFORMANCE`) is complete. It began from clean
  autosave commit `880e6c72281b1b11dc065a5c635fbf92c86df60e`; the frozen
  `src/ca`, `tests`, `goal-2`, and `goal-5` trees remain
  `6e6b34769d60508c03d0a69fad1ede4fef75e217`,
  `02ad081e039a46efbf61855fdeae60abb7bb70ad`,
  `48b6309655ec7c1d3aaa1a0ec5dfb700385e16d1`, and
  `ba62f20b8c620094a0ad683906a803c5404be5f2`.
- Stage 6 produced twelve concrete pressure executions, one exact
  SPF001–SPF060 audit join, fourteen reusable Goal 7 conformance suites, and
  row-exact T01–T45 migration assertions. The hostile review left no blocker
  after narrow corrections to higher-order evaluation, continuous Rule/read
  ownership, replay/measure boundaries, structural identity, import/signature
  gates, and the reference `apply` keyword.
- Stage 6 changed planning/reference documentation only. Count, local-link,
  terminology, import/signature, scaffold parse/run, whitespace, and scoped
  frozen-tree checks pass; the runtime suite was not rerun because behavioral
  trees are identical to the 102-test baseline.
- Stage 7 (`7-HANDOFF`) began from clean autosave commit
  `c544caaef9022ce39d562b93b5d5b907592925ad`. The frozen `src/ca`,
  `tests`, `goal-2`, and `goal-5` tree identities still match the Stage 1
  baseline.
- The Stage 7 runtime inventory confirms one in-place cutover: retain and
  generalize the five plural component modules and `loci.py`; replace
  `specs.py`/`Dynamics`; fold the public traversal contract out of
  `rollout.py`; add `program.py`, `serialization.py`, and `catalog/`; then
  adapt `datasets.py`, `rng.py`, and `viz/` without allowing them into the
  semantic core.
- Stage 7 (`7-HANDOFF`) is in progress. Its only new durable design output is
  `goal-6/goal-7-handoff.md`; it does not create or begin Goal 7.

## Assumptions To Challenge

- A single closed result algebra can represent deterministic, branching,
  stochastic, continuous, symbolic, terminal, invalid, and one-shot rules
  without family dispatch.
- Every executable family has one defensible primary catalog home among the six
  locked modules, with cross-cutting mechanics represented as metadata.
- `program.py`, the plural component modules, and the existing rollout boundary
  can own the necessary concepts without public `replacement.py`, `results.py`,
  `engine.py`, or `run.py` modules.
- One remastered reference scaffold can communicate the architecture more
  clearly than multiple competing examples.
- Downstream generation/dataset/viz structure can remain deferred without
  leaving a core or catalog contract ambiguous.

## Planned Durable Outputs

Goal 6 should leave:

- an accurate live goal index in `GOALS.md`;
- one canonical architecture specification in `goal-6/architecture.md`;
- a clean public API account in `api.md` and a clearly delineated conceptual
  role for `simple_programs.md`, with no document advertised as current while
  contradicting the remaster;
- a revised-in-place `ref/notes/ca-scaffold.py` that demonstrates the settled
  architecture from primitives through catalog aliases;
- `goal-6/catalog-migration.md`, mapping all 60 executable families and every
  T01–T45 action into the six catalog modules;
- `goal-6/conformance.md`, defining the representative paper fixtures,
  serialization checks, count checks, and family-blind application tests; and
- `goal-6/goal-7-handoff.md`, an exact mechanics-first implementation sequence
  for the existing repository.

Stage files record execution evidence. They must not become competing
architecture specifications.

## Success Metrics and Verification Requirements

Goal 6 is complete only when all of the following are true:

1. `SimpleProgram` has exactly five stored fields and each protocol, type
   relationship, invariant, and cross-field validation responsibility is
   explicit.
2. Configuration ownership, dynamic/fresh/deleted loci, structural carriers,
   exact values, and readable/writable region composition are specified without
   adding hidden public axes.
3. Rule results and universal application specify atomic replacement,
   preserve-outside behavior, successor cardinality, terminal/error outcomes,
   witnesses, deduplication, stochastic replay, continuous evolution, symbolic
   or intensional results, and one-shot application.
4. Application pseudocode contains no family/catalog dispatch and no semantic
   special case disguised as carrier or locus dispatch.
5. Every agreed core/catalog file has one clear responsibility, every public
   example resolves to that structure, and rejected extra modules have not
   reappeared merely to name concepts.
6. Each of the 60 executable families appears exactly once in the canonical
   family mapping; F010 and F042 are handled explicitly as close roles rather
   than silently counted as families.
7. All T01–T45 dispositions and all 41 missing-family additions have exact,
   non-conflicting migration actions, canonical homes, stable-ID treatment,
   constructor status, and source/API references.
8. Closed descriptors, exact values, versioned lossless codecs, unknown-tag
   failure, fresh identities, alias-expansion equivalence, expanded five-field
   forms, and round-trip/one-step commutation are covered by the conformance
   design.
9. Every pressure category required by
   `goal-5/integration-handoff.md` is executed on paper, with failures changing
   the architecture rather than being waived.
10. One strong final hostile review finds no unmapped family, covert sixth
    field, family switch, ambiguous file ownership, contradictory current doc,
    or untestable Goal 7 obligation.
11. The Goal 7 handoff names dependency-ordered file changes, migration/cutover
    steps, compatibility decisions, tests, documentation work, and completion
    criteria around reusable mechanics rather than Book chapters or catalog
    labels.
12. The Goal 6 diff contains no behavioral change under `src/ca`, preserves
    Goal 2 unchanged, passes link/count/whitespace checks, and leaves all
    current documents in a resumable, non-contradictory state.

Verification should use compact table/count checks, direct document review,
paper executions, focused repository inspection, `git diff --check`, and one
hostile review. Do not construct a new verification framework or rerun the
taxonomy audit.

## Indexed Stages

### 1-CUTOVER

Status: **COMPLETE — source authority, live goal index, Goal 2 disposition, and
runtime baseline recorded**

#### Big Picture Objective

Establish Goal 6 as the clean current planning authority, record the actual
repository baseline, and make the Goal 5 → Goal 6 → Goal 7 sequence explicit.

#### Detailed Implementation Plan

- Inspect current files, tests, public exports, repository status, and existing
  user changes before planning edits.
- Update `GOALS.md` to record Goal 5 as complete, Goal 6 as the active remaster,
  Goal 7 as later implementation, Goal 2 as frozen evidence, and Goal 4 as
  superseded rather than governing.
- Start `goal-6/architecture.md` with the source precedence and a compact
  preserve/replace/defer ledger. Derive the Goal 2 entries from
  `goal-5/integration-handoff.md`; consult the frozen handoff only where the
  preserved conclusion needs exact detail.
- Record the starting `src/ca` file/test baseline so the final no-implementation
  check can distinguish pre-existing work from Goal 6 changes.
- Identify which current documents claim architectural authority and assign
  each a future role. Do not yet rewrite contracts or code.

#### Completion Requirements

- The live goal index and Goal 6 source hierarchy are accurate.
- Goal 2 remains byte-for-byte unchanged and Goal 4 machinery is absent from
  the working contract.
- The preserve/replace/defer ledger contains no unreviewed Goal 2 axis.
- The starting runtime and dirty-worktree baseline is recorded.
- The next incomplete stage can begin without rediscovering project history.

### 2-CONTRACTS

Status: **COMPLETE — five protocols, configuration/loci ownership, validation,
serialization constraints, and paper type-checks recorded**

#### Big Picture Objective

Specify the five component contracts and their shared structural/type algebra
before allowing file layout or examples to harden accidental semantics.

#### Detailed Implementation Plan

- Define `SimpleProgram[C, V, W, R]` with exactly five stored values and explain
  why `C`, `V`, `W`, and `R` are type relationships rather than public axes.
- Define `Seed`, `Alphabet`, `WritableRegion`, `ReadableRegion`, and `Rule`
  protocols, including closed descriptor forms, invariants, composition, and
  cross-field validation.
- Place configuration support, topology, geometry, defaults, boundaries,
  invariants, control, and program text in the produced configuration and its
  structural descriptors—not in a sixth component.
- Specify `loci.py` as the common algebra for coordinates, named components,
  words, trees, graphs, products, fields, intervals, dynamic support, fresh
  identities, and intensional regions while preserving read/write capability
  distinctions.
- Explain how plural component modules construct one composed field value:
  primitives first, then compounds, then general constructors and useful
  component presets.
- Specify serialization requirements that constrain every component:
  versioning, exact values, unknown-tag failure, canonical structural forms,
  identity allocation, and lossless round trips.
- Update the canonical architecture document and the relevant conceptual/API
  documents; avoid duplicating the same contract in full across them.

#### Completion Requirements

- All five protocols, their generic relationships, ownership boundaries,
  invariants, and validation errors are explicit.
- Dynamic support, creation/deletion, global reads, continuous carriers, and
  symbolic/intensional regions have honest representations.
- No `Domain`, `Shape`, `Boundary`, `ConfigurationSchema`, scheduler, RNG,
  update, result, or solver axis has reappeared.
- Serialization is specified as a cross-cutting obligation rather than a
  component.
- At least one ordinary CA, mobile automaton, structural rewrite, constraint,
  and continuous example type-checks on paper against the contracts.

### 3-APPLICATION

Status: **COMPLETE — result/application and run/tool boundaries verified**

#### Big Picture Objective

Define one complete rule-result and atomic application law that works for
deterministic, branching, stochastic, structural, continuous, symbolic, and
one-shot programs.

#### Detailed Implementation Plan

- Specify the `Rule` codomain for zero, one, or many complete replacements,
  including exact writes, fresh/deleted components, probabilities, replay
  evidence, derivation witnesses, provenance, and symbolic/intensional
  solution sets.
- Distinguish quiescent identity, terminal completion, invalid input, undefined
  relation, explicit failure, and divergence/resource exhaustion. Do not
  encode all of them as an empty successor list.
- Define witness retention before successor deduplication and define what
  equality/canonicalization is allowed to deduplicate.
- Write family-blind application pseudocode: validate immutable input, resolve
  writable/readable structures, denote the closed relation, reject writes
  outside the frontier, atomically commit each complete replacement, preserve
  everything outside it, and retain result evidence.
- Make clear that Rule data owns firing/applicability, schedules, collision
  resolution, simultaneous semantics, and stochastic laws. The commit
  operation enforces the generic capability and atomicity contract only.
- Specify how continuous evolution, event resets, symbolic solutions,
  unbounded/intensional sets, and single-application functions cross the same
  boundary.
- Separate one-step application from horizon, query, realization, replay,
  resource, trace, observer, render, and export requests.

#### Completion Requirements

- Every result state and cardinality is distinguishable and testable.
- Coupled multi-locus writes, overlapping proposals, fresh identities,
  deletions, and preserve-outside behavior have unambiguous semantics.
- Probability laws and concrete replayable draws remain distinct and lossless.
- The pseudocode contains no catalog, family, semantic-class, or carrier switch.
- A one-shot relation is valid without pretending it must produce a trajectory.
- The public `ca.rollout` boundary can be defined from repeated application
  without becoming part of `SimpleProgram`.

### 4-SURFACE

Status: **COMPLETE — ownership, public/reference cutover, and hostile review verified**

#### Big Picture Objective

Translate the settled contracts into a small, intuitive file/public API design
and a single code-shaped reference scaffold.

#### Detailed Implementation Plan

- Add an ownership table for `program.py`, `loci.py`, every plural component
  module, `serialization.py`, `py.typed`, the catalog package, root re-exports,
  and the public rollout boundary.
- Explicitly test whether any proposed responsibility truly requires a new
  public module. Do not add `configuration.py`, `replacement.py`, `results.py`,
  `engine.py`, or `run.py` merely because those concepts exist in prose.
- Set root import and catalog re-export conventions so the intended API example
  has one obvious spelling and aliases do not bypass ordinary construction.
- Revise `api.md` into a clean current public contract and assign
  `simple_programs.md` a non-conflicting conceptual/specification role.
- Revise `ref/notes/ca-scaffold.py` in place only after the contracts are
  settled. Preserve its useful progression:
  `loci → component primitives → compounds → general constructors →
  SimpleProgram → catalog constructors/aliases → family-blind apply/rollout`.
- Show that whole-program semantic names live in `catalog/`, while reusable
  component presets remain in their plural component modules.
- Deliberately defer generation/dataset/stream/RNG/viz internals, documenting
  only the stable boundary Goal 7 must respect.

#### Completion Requirements

- Every agreed file has one cohesive responsibility and no required
  responsibility is homeless or duplicated.
- The core/catalog tree and six catalog names match the locked target.
- Public examples compose directly from exported primitives and resolve named
  aliases through the catalog.
- The remastered scaffold contains no obsolete extra program axis or alternate
  executor and remains small enough to read top-to-bottom.
- Current documentation presents one architecture to a fresh session; retained
  historical/design material cannot be mistaken for competing instructions.
- Deferred auxiliary organization does not hide any unresolved core or catalog
  question.

### 5-CATALOG

Status: **COMPLETE — canonical family and T01–T45 mapping verified**

#### Big Picture Objective

Turn the completed taxonomy into an exact constructor and migration plan across
the six catalog modules without turning navigation categories into runtime
ontology.

#### Detailed Implementation Plan

- Create `goal-6/catalog-migration.md` with one row for every executable family:
  Goal 5 family ID/name, canonical catalog home, status, constructor name,
  closed parameters, five-field skeleton, representation/result pressures,
  source anchors, and compatibility names where relevant.
- Assign each family exactly one primary home among `automata`, `substitua`,
  `machina`, `media`, `criteria`, and `dynamica`. Record secondary traits as
  metadata, not duplicate definitions.
- Resolve all T01–T45 actions exactly as specified: retain family, retain
  preset, merge, repair, alias, retire role, or split.
- Add all 41 missing executable families and explicitly account for F010 and
  F042 as close roles outside the executable family count.
- Define stable-ID policy without assuming the research `F` identifiers must
  become public catalog IDs or recycling retired IDs.
- Define `catalog/entries.py` as descriptive lookup/provenance metadata, not a
  dispatch registry; define re-export and collision/precedence rules.
- Specify when a name is a canonical family constructor, parameter preset,
  alias, or compatibility name. All return ordinary five-field programs.
- Preserve each T row's exact Goal 5 candidate join and named-construction
  source anchors; do not treat a broad family source as proof of a narrower
  preset.

#### Completion Requirements

- Exact checks report 60 unique executable family rows, 41 additions, complete
  T01–T45 dispositions, and two separately identified close roles.
- Every family has one canonical module, one valid five-field mapping, closed
  parameters, and the source/pressure evidence needed by Goal 7.
- Every T row retains its Goal 5 candidate provenance and the source evidence
  required by its named callable or non-callable role.
- No family is duplicated to satisfy multiple catalog labels.
- No catalog category, entry, ID, or alias affects generic application.
- Constructor and stable-ID collisions are resolved explicitly.
- The migration can be implemented without rerunning taxonomy research.

### 6-CONFORMANCE

Status: **COMPLETE — twelve pressure fixtures, exact 60-family join, and
reusable Goal 7 conformance suites verified**

#### Big Picture Objective

Try to break the remastered design using Goal 5's strongest counterexamples,
then freeze a compact conformance contract for Goal 7.

#### Detailed Implementation Plan

- Create `goal-6/conformance.md` from the required pressure categories in
  `goal-5/integration-handoff.md`: coupled writes, variable support, nonlocal
  reads, zero/one/many relations, continuous evolution, stochastic mechanics,
  mutable program state, one-shot evaluation, fixed gate networks, distinct
  codec mechanics, shared priority construction, and the observer boundary.
- Paper-execute the representative families already named by Goal 5. Record
  inputs, resolved regions, rule result, commit/result semantics, and the
  precise invariant demonstrated; do not recreate full semantic fingerprints.
- Audit the 60-row catalog matrix against the five contracts and result algebra,
  escalating any counterexample rather than adding a family switch.
- Define focused Goal 7 tests for descriptor closure, exact codec round trips,
  unknown tags, replay, fresh identities, witness/dedup behavior,
  representation commutation, alias expansion, and native/generic one-step
  equivalence.
- Check public examples and application pseudocode for covert sixth fields,
  hidden entropy/solver policy, family/carrier dispatch, and ambiguous module
  ownership.
- Conduct one independent hostile review of the complete architecture,
  catalog, conformance plan, and current documentation. Resolve every
  substantive finding in the canonical artifacts.

#### Completion Requirements

- Every required pressure category has a concrete passing paper execution or a
  resolved architecture correction.
- The complete 60-family mapping passes once; no parallel audit system or
  repeated taxonomy review is created.
- Serialization, replay, provenance, cardinality, witness, and commutation
  obligations are executable as tests rather than slogans.
- The hostile review leaves no unresolved concrete counterexample.
- Count, link, terminology, import-surface, and `git diff --check` verification
  pass.
- No behavioral `src/ca` change has occurred relative to the Stage 1 baseline.

### 7-HANDOFF

#### Big Picture Objective

Convert the settled architecture and conformance contract into one precise,
mechanics-first Goal 7 implementation handoff and close Goal 6 cleanly.

#### Detailed Implementation Plan

- Create `goal-6/goal-7-handoff.md` with a dependency DAG and ordered stages
  beginning with shared representations and contracts, then universal
  application, component constructors, serialization, catalog construction,
  migration, conformance, documentation, and cleanup.
- Name exact existing files to retain, revise, add, move, or retire. Explain how
  Goal 7 evolves the current runtime in place and avoids a second executor or
  compatibility architecture.
- Assign every Goal 6 conformance obligation to a Goal 7 test stage and every
  catalog row to a mechanics-bearing implementation stage.
- Specify cutover, compatibility, deprecation, serialization-version, and
  documentation steps, including how root exports and catalog aliases become
  canonical.
- Reconcile `api.md`, `simple_programs.md`,
  `ref/notes/ca-scaffold.py`, `goal-6/architecture.md`,
  `goal-6/catalog-migration.md`, and `goal-6/conformance.md` one final time.
- Update `GOALS.md` only after all Goal 6 completion requirements pass. Do not
  create or start Goal 7 without separate authorization.

#### Completion Requirements

- Goal 7 has an exact, dependency-ordered, file-level implementation plan with
  tests and completion criteria; no stage is organized merely by Book chapter,
  semantic label, or catalog module.
- Every preserved Goal 2 strength and every Goal 5 pressure has an explicit
  implementation or test destination.
- The handoff contains no unresolved core contract, catalog mapping, migration,
  ownership, or compatibility decision.
- All canonical documents agree, all links and counts pass, whitespace/diff
  checks pass, Goal 2 is unchanged, and the runtime matches the Stage 1
  baseline.
- `0-plan.md` records final facts and evidence, and `GOALS.md` identifies Goal 6
  as complete and Goal 7 as the next separately authorized goal.
