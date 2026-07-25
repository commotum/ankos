# 5-CATALOG

Status: **COMPLETE**

## Current Facts

- Stages 1–4 are complete. The first clean autosave after Stage 4 completion is
  commit `954a30467eb5e0c3892e5a8c4f920b505b2a16b8`.
- Goal 5 fixes the inventory at 60 executable semantic families, 19 with some
  current-catalog coverage, 41 family additions, and two close non-family
  roles. It also gives every T01–T45 row exactly one disposition.
- At stage entry, `goal-6/catalog-migration.md` did not exist. It is now the
  canonical implementation-facing catalog map and joins Goal 5 results without
  reproducing its taxonomy research.
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

- [x] The canonical matrix has exactly 60 unique executable rows and 60 unique
      stable family IDs, research IDs, constructors, and primary homes.
- [x] Status counts are exactly 19 covered and 41 additions.
- [x] F010 and F042 are recorded as exactly two separate close roles.
- [x] Every row has closed parameters, a valid five-field skeleton, pressure
      and result obligations, source anchors, and explicit legacy relations.
- [x] T01–T45 appear exactly once with disposition counts
      `15/21/2/3/2/1/1` for retain-family, retain-preset, merge, repair, alias,
      retire-role, and split.
- [x] Every T disposition has a non-conflicting canonical target and exact
      callable, metadata-only, alias, preset, merged, repaired, retired, or
      split treatment.
- [x] Every T entry preserves its Goal 5 candidate provenance and the source
      anchors required for the named family, preset, repair, alias, or role.
- [x] Stable-ID, collision, re-export, alias, serialization, and metadata
      policies are implementation-ready and cannot become execution dispatch.
- [x] Hostile review, exact count checks, link/path checks, terminology,
      whitespace/diff, frozen hashes, and behavioral-tree checks pass.
- [x] Stage 6 can pressure-test this matrix without reopening taxonomy,
      catalog ownership, or constructor naming.

## Stage Results

- Created `catalog-migration.md` with SPF001–SPF060 assigned once in ascending
  executable F order. Goal 5 `F` IDs remain audit provenance and T01–T45 remain
  legacy migration identities; none is a runtime type or dispatch key.
- Assigned exactly 11 families to `automata`, 15 to `substitua`, 8 to
  `machina`, 14 to `media`, 9 to `criteria`, and 3 to `dynamica`. Canonical
  constructors use exact family slugs converted to `snake_case`.
- Reconciled all 45 T rows once with exact disposition, candidate provenance,
  named-construction sources, normalized targets, and callable treatment.
  T40 is a non-callable two-branch record; F055 has SPF052 without a fabricated
  T owner; T08, F010, and F042 remain callable-free roles.
- Fixed callable policy at five kinds: canonical `C`, closed preset `P`, true
  alias `A`, total lossless compatibility adapter `K`, and metadata-only `M`.
  All named `C`/`P`/`A` callables are explicit flat catalog exports; `K` is
  category-qualified and `M` is never callable.
- Defined callable-free `FamilyEntry`, `RoleEntry`, `LegacyEntry`,
  `LegacyTarget`, and `NameEntry` relations. Category functions are written
  explicitly; metadata cannot synthesize functions or drive application.
- Rejected optional construction receipts after hostile review exposed that
  the five-field API has no honest carrier for invocation history. Canonical
  codecs contain expanded semantic data only; applications may keep a separate
  user manifest.
- Tightened stochastic families to denote explicit probability laws while
  leaving draws to external realization, repaired F004 cursor writes, added
  preset-specific evidence, and aligned the reference scaffold to canonical
  family → `eca` preset → true alternate alias.
- Independent matrix and API hostile reviews report no remaining blocker. The
  exact validator reports `60` rows, `19/41` status, home counts
  `11/15/8/14/9/3`, `45` legacy rows, two close roles, and zero errors.
- `python3 -B -m py_compile ref/notes/ca-scaffold.py`,
  `python3 -B ref/notes/ca-scaffold.py`, Markdown fence, exact Goal 5 diff,
  link/path, and `git diff --check` checks pass. Runtime tests were not rerun
  because this stage changes planning/API/reference documents only.
- Against baseline `954a30467eb5e0c3892e5a8c4f920b505b2a16b8`,
  `src/ca`, `tests`, Goal 2, and Goal 5 retain tree hashes
  `6e6b34769d60508c03d0a69fad1ede4fef75e217`,
  `02ad081e039a46efbf61855fdeae60abb7bb70ad`,
  `48b6309655ec7c1d3aaa1a0ec5dfb700385e16d1`, and
  `ba62f20b8c620094a0ad683906a803c5404be5f2`.

Stage 6 is now the first incomplete stage. It may pressure-test this settled
catalog, but it must not reopen family identity, category ownership,
constructor spelling, or migration policy without a concrete contradiction.
