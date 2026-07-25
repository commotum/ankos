# 5-CATALOG

Status: **IN PROGRESS**

## Current Facts

- Stages 1–4 are complete. The first clean autosave after Stage 4 completion is
  commit `954a30467eb5e0c3892e5a8c4f920b505b2a16b8`.
- Goal 5 fixes the inventory at 60 executable semantic families, 19 with some
  current-catalog coverage, 41 family additions, and two close non-family
  roles. It also gives every T01–T45 row exactly one disposition.
- `goal-6/catalog-migration.md` does not yet exist. Stage 5 must make it the
  canonical implementation-facing catalog map without reproducing Goal 5's
  taxonomy research.
- The current runtime has no `catalog/` package. Its `specs.py` recognizes six
  Phase 1 family strings and its root broadly re-exports constructors. Those
  are Goal 7 migration inputs, not a surface Stage 5 may change.
- Stage 4 fixed the six category owners, metadata-only `entries.py`, explicit
  collision-free re-exports, ordinary five-field constructor expansion, and
  the prohibition on catalog-driven execution.

## Updated Assumptions

- All 60 families have one defensible dominant-mechanic home among
  `automata`, `substitua`, `machina`, `media`, `criteria`, and `dynamica`.
- Canonical family identity should be independent of Goal 5's research IDs,
  legacy T01–T45 entry IDs, Python constructor names, and implementation
  classes.
- T01–T45 can remain stable legacy entry identities while a normalized family
  table gives split, merged, aliased, repaired, and retired rows unambiguous
  targets.
- One matrix can carry family construction, migration, pressure, and source
  obligations compactly enough that Stage 6 need not build a second taxonomy.

## Big Picture Objective

Turn the completed Goal 5 taxonomy into an exact, collision-free constructor
and migration plan across the six catalog modules, with all 60 executable
families and every T01–T45 action accounted for as ordinary five-field program
construction rather than runtime ontology.

## Detailed Implementation Plan

- Define canonical family-ID, legacy-ID, constructor, preset, alias,
  compatibility, re-export, and collision policy.
- Create `goal-6/catalog-migration.md` with exactly one canonical row per
  executable family. Each row must carry its Goal 5 identity and name,
  canonical module and constructor, covered/addition status, closed parameter
  surface, five-field construction skeleton, representation/result pressure,
  source anchors, and legacy/compatibility relations.
- Give F010 and F042 separate role dispositions outside the executable family
  matrix.
- Create one T01–T45 migration table preserving every legacy ID and exact Goal
  5 action while resolving it to canonical constructors, presets, aliases,
  metadata tombstones, or split targets.
- Preserve every T row's Goal 5 candidate join and the narrow source anchors
  required by its named callable; family-level anchors do not stand in for
  preset-specific evidence.
- Resolve T40's two-family split and any broad legacy-row ambiguity without
  assigning one canonical family row two mechanics.
- Record how `catalog/entries.py`, category modules, `catalog/__init__.py`,
  canonical serialization, and Goal 7 tests consume the matrix without engine
  dispatch or hidden invocation state.
- Conduct one focused hostile review of row uniqueness, module placement,
  naming, parameters, five-field fit, T actions, additions, roles, stable IDs,
  and public-name collisions.

Files expected to change:

- `api.md`
- `goal-6/2-CONTRACTS.md`
- `goal-6/catalog-migration.md`
- `goal-6/5-CATALOG.md`
- `goal-6/architecture.md`
- `goal-6/0-plan.md`
- `ref/notes/ca-scaffold.py`

The three non-stage artifacts above receive only hostile-review consistency
repairs: removal of the unsupported construction-receipt idea and alignment of
the reference constructor/preset/alias chain. They remain target
documentation, not runtime implementation.

## No-Cheating Checks

- No executable family is omitted, duplicated across modules, or represented
  only by a legacy umbrella name.
- F010 and F042 do not enter the 60-family count or acquire fake transition
  mechanics.
- No constructor returns a subclass, registers an executor, or adds a sixth
  stored field; every constructor expands to an ordinary `SimpleProgram`.
- Catalog IDs, family names, categories, aliases, and metadata never affect
  `apply` or `rollout`.
- Presets and compatibility names narrow or delegate to canonical
  constructors; they do not duplicate component or application logic.
- Stable IDs are never recycled, derived from Python class names, or silently
  reassigned by sorting.
- T01–T45 each have one and only one recorded disposition, including an
  explicit non-callable treatment where a role or ambiguous umbrella is
  retired.
- No Goal 4 audit machinery, Book rediscovery, behavioral `src/ca` change,
  frozen Goal 2 edit, Stage 6 conformance artifact, or Goal 7 implementation is
  introduced.

## Completion Requirements

- [ ] The canonical matrix has exactly 60 unique executable rows and 60 unique
      stable family IDs, research IDs, constructors, and primary homes.
- [ ] Status counts are exactly 19 covered and 41 additions.
- [ ] F010 and F042 are recorded as exactly two separate close roles.
- [ ] Every row has closed parameters, a valid five-field skeleton, pressure
      and result obligations, source anchors, and explicit legacy relations.
- [ ] T01–T45 appear exactly once with disposition counts
      `15/21/2/3/2/1/1` for retain-family, retain-preset, merge, repair, alias,
      retire-role, and split.
- [ ] Every T disposition has a non-conflicting canonical target and exact
      callable, metadata-only, alias, preset, merged, repaired, retired, or
      split treatment.
- [ ] Every T entry preserves its Goal 5 candidate provenance and the source
      anchors required for the named family, preset, repair, alias, or role.
- [ ] Stable-ID, collision, re-export, alias, serialization, and metadata
      policies are implementation-ready and cannot become execution dispatch.
- [ ] Hostile review, exact count checks, link/path checks, terminology,
      whitespace/diff, frozen hashes, and behavioral-tree checks pass.
- [ ] Stage 6 can pressure-test this matrix without reopening taxonomy,
      catalog ownership, or constructor naming.

## Stage Results

To be completed after the canonical matrix, reconciliation, hostile review,
and verification pass.
