# Taxonomy and API Integration Handoff

## Decision

Do not implement the frozen Goal 2 handoff as written.

Its source research remains useful and auditable, but its six-axis program
model (`CONFIGURATION_SCHEMA`, firing `FRONTIER`, `NEIGHBORHOOD`, `RULE`,
`UPDATE`, plus domain machinery) is superseded by the whole-book result:

```python
class SimpleProgram:
    seed: Seed
    alphabet: Alphabet
    frontier: WritableRegion
    neighborhood: ReadableRegion
    rule: Rule
```

Goal 5 changes no catalog, API, runtime, tests, or predecessor goal. This file
is the dependency boundary for a separately authorized remaster.

## Recommended Goal Sequence

1. **Goal 6 — remaster the Goal 2 design and implementation plan.** Rebuild the
   target architecture around the five fields, incorporate the 52-family
   coverage inventory, revise the catalog plan, and define conformance
   obligations. Preserve Goal 2 as historical evidence rather than editing it
   into a different plan.
2. **Goal 7 — implement the remastered plan.** Build the generic protocols,
   universal application engine, structural representations, and presets in
   dependency order. Implementation begins only after Goal 6 closes the
   contracts.

No Book rediscovery is required for either goal. A newly discovered canonical
source contradiction may reopen a decision; implementation inconvenience may
not.

## Goal 6 Input Set

Use:

- `goal-5/taxonomy-census.md` for final counts and catalog scope;
- `goal-5/11-FAMILIES.md` for all family definitions, candidate membership,
  sources, and boundary tests;
- `goal-5/api-pressure.md` for the five-field contract and every family mapping;
- `goal-5/10-RECONCILE.md` for exact T01–T45 actions;
- `goal-5/source-decision-matrix.csv` only when source-to-decision traceability
  is needed;
- `simple_programs.md` and `api.md` as design inputs; and
- the frozen Goal 2 handoff only to recover reusable design work identified
  below.

Do not import Goal 4's process machinery, verification system, search archive,
or completion contract into Goal 6.

## Public Program Contract to Specify

### Components

| Component | Required contract |
|---|---|
| `Seed[C]` | Produces typed exact, constructive, partial, or probability-law configurations. The configuration carries support, topology, geometry, defaults, invariants, and visible control state. |
| `Alphabet[V]` | Closed structural value schema for finite, numeric, tagged, product, word, graph, field, instruction, probability, and symbolic values. |
| `WritableRegion[C, W]` | Resolves the complete possible-write envelope, including structured, dynamic, intensional, continuous, or fresh components. |
| `ReadableRegion[C, R]` | Resolves the readable view, including local, global, historical, graph, metric, boundary, or differential dependencies. |
| `Rule[R, W, C]` | Closed relation from the readable view to complete atomic replacements of the writable envelope. |

`C`, `V`, `W`, and `R` are type relationships, not additional stored program
axes.

### Rule result

Specify one generic result algebra that can retain:

- zero, one, or many complete replacements;
- a probability measure or explicit replayable draw evidence;
- `Advanced`, `Quiescent`, `Terminal`, `Invalid`, `Undefined`, or equivalent
  typed outcomes;
- separate derivation witnesses before successor deduplication;
- exact structural writes and fresh-component identities; and
- symbolic or intensional solution sets where enumeration is not finite.

This result is the `Rule` codomain and engine output. It is not a
`ResultPolicy` component.

### Universal application

The engine must:

1. obtain and validate an immutable input configuration;
2. resolve the complete writable and readable regions;
3. evaluate the closed rule relation;
4. reject writes outside the frontier;
5. atomically commit every complete replacement while preserving everything
   outside the frontier; and
6. preserve outcomes, probabilities, provenance, witnesses, and terminal
   reasons.

It must not switch on a catalog ID, family name, or semantic construction
class.

### Run and tooling boundary

Keep horizon, query, solver strategy, finite realization, replay key, resource
limit, trace request, observer, renderer, and export format outside
`SimpleProgram`. A solver or evaluator with its own transition state is itself
an ordinary `SimpleProgram`; a choice of how to query an intensional relation
is run/tooling policy.

## Catalog Integration

Retain the stable T01–T45 identifiers while applying these exact actions:

| Action | IDs |
|---|---|
| Retain as family | T01, T11–T14, T17, T19–T20, T29–T31, T37, T39, T43, T45 |
| Retain as preset | T02–T04, T06–T07, T09, T16, T18, T21–T26, T28, T33–T36, T38, T42 |
| Merge | T05 into F053; T15 into F038 |
| Repair | T10 as neighbor-updating mobile mechanics; T27 as geometric substitution rather than a “fractal” family |
| Alias | T32 to F030; T44 to F053 |
| Retire role | T08 as Seed data/laws; T41 as a misleading catalog role while retaining F047 |
| Split | T40 between F002 and F008 |

Add the 33 missing family rows listed in `taxonomy-census.md`. Assign fresh
stable IDs after the catalog naming and ordering convention is chosen; do not
recycle retired IDs or make IDs depend on implementation class names.

Each catalog row should identify:

- one semantic family;
- whether the row is a family, preset, alias, or compatibility name;
- its closed data parameters;
- canonical source anchors;
- its five-field mapping; and
- any representation or result requirements.

Do not create 52 public runtime subclasses. Named constructors should return
ordinary `SimpleProgram` specifications.

## Goal 2 Work to Preserve

Carry forward these design conclusions:

- closed, serializable structural descriptors rather than callbacks,
  unrestricted `Any`, host-language evaluation, or a CAS escape hatch;
- versioned, lossless codecs and explicit representation relations;
- exact numeric semantics with no silent floating fallback;
- visible control, schedule, phase, and stored-program state;
- one branch-free generic engine;
- typed successor cardinality, outcomes, failures, witnesses, and provenance;
- derivation witnesses kept distinct from successor deduplication;
- raw structural traces before downstream views or encodings;
- lossless one-step commutation tests between native presets and generic
  semantics; and
- canonical Book sources as the authority for presets and claims.

## Goal 2 Work to Replace

Do not carry forward:

- a public configurable `UPDATE` or `UpdatePolicy`;
- a firing-source meaning of `Frontier`;
- separate public `Domain`, `Shape`, `Boundary`, or
  `ConfigurationSchema` program axes;
- fixed `Z4`, finite coordinate, scalar-per-cell, or mandatory synchronous-step
  restrictions;
- a sibling ontology for constraints, uniterated functions, or PDE relations;
- catalog-family runtime dispatch;
- semantic names as implementation classes;
- hidden randomness, implicit solver behavior, or untyped empty successor
  results; or
- observers, renderers, properties, and seed recipes promoted to construction
  families.

## Required Goal 6 Pressure Fixtures

The remastered contract should be executable on paper against at least these
fixtures before implementation:

| Pressure | Representative families | Required proof |
|---|---|---|
| Coupled source/destination writes | F031, F007 | Frontier contains every possible writable locus and Rule returns one atomic coupled replacement. |
| Variable support and structure | F017, F029, F038, F040, F052 | Fresh/deleted components and preserve-outside semantics are unambiguous without an update axis. |
| Global or nonlocal reads | F018–F020, F028, F036, F054 | Neighborhood can expose the complete required relation without pretending it is geometrically local. |
| Zero/one/many relations | F015, F019, F030, F034, F041 | Cardinality, witness, terminal, and symbolic-solution semantics remain distinct. |
| Continuous evolution | F006, F037, F041 | Continuous state and event/flow results do not require a top-level time axis. |
| Stochastic mechanics | F016, F044, F046, F050 | Probability law and replay entropy are explicit and lossless. |
| Mutable program state | F035, F051 | Program text is ordinary tagged writable state under a closed interpreter Rule. |
| One-shot evaluation | F011, F013–F015, F021, F025, F036, F045 | A single Rule application is legitimate without inventing repeated dynamics. |
| Observer boundary | F004, F010, F042 | Useful transforms remain available without inflating the semantic-family catalog. |

## Goal 6 Completion Contract

Goal 6 is ready to hand to implementation only when:

- the five component protocols and their type relationships are explicit;
- every F001–F055 row still has one valid mapping or a concrete documented
  counterexample;
- atomic replacement, preserve-outside behavior, result cardinality,
  stochastic replay, continuous/intensional objects, and dynamic support are
  specified;
- T01–T45 and the 33 additions have an exact catalog migration plan;
- no public component or family class exists only for naming convenience;
- the engine pseudocode contains no catalog/family switch; and
- the implementation stages are ordered around reusable mechanics, not Book
  chapter order or semantic labels.

That remaster can be substantially smaller than the frozen Goal 2 plan because
the Book discovery, taxonomy, family boundaries, and API pressure work are now
closed.
