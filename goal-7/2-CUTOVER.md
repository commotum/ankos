# Goal 7 Stage 2 — Atomic Five-Field Core Cutover

Status: **COMPLETE**

Handoff stage: **G7-01**

This is the live transaction record for replacing the 0.1 tensor/family
runtime with the settled five-field program model. It is an atomic completion
boundary: internal work may be ordered, but this stage is not complete until
the old executor is physically absent, every migrated consumer uses the one
generic application law, and the complete active suite is green.

## Authority

In descending order:

1. [`0-plan.md`](0-plan.md) and [`0-loop.md`](0-loop.md)
2. [`../goal-6/goal-7-handoff.md`](../goal-6/goal-7-handoff.md), G7-01
3. [`../goal-6/architecture.md`](../goal-6/architecture.md)
4. [`../goal-6/conformance.md`](../goal-6/conformance.md)
5. [`../api.md`](../api.md), [`../simple_programs.md`](../simple_programs.md),
   and [`../ref/notes/ca-scaffold.py`](../ref/notes/ca-scaffold.py)
6. [`1-ORACLES.md`](1-ORACLES.md) and
   [`../tests/conformance/test_oracles.py`](../tests/conformance/test_oracles.py)

Goal 5 taxonomy and Goal 6 architecture remain frozen inputs. This stage
implements their generic kernel; it does not revise family identity, invent
catalog-specific engines, or pull later catalog/codec work forward.

## Starting State

- Starting Git commit: `7226c49`
- Stage 1 oracle inventory: 16 independent cases; 12 active oracle tests
- Pre-cutover active suite: 114 passed, 96 skipped
- Live runtime version: 0.1 implementation plus inert Goal 7 declarations
- Obsolete executor modules still present at start:
  `src/ca/specs.py` and `src/ca/rollout.py`
- Target `src/ca/program.py` exists only as an inert declaration scaffold

The starting worktree was clean.

## Atomic Internal Order

```text
loci + Alphabet kernel
→ Seed/WritableRegion/ReadableRegion
→ Rule denotation/result algebra
→ SimpleProgram/application/Seed binding/rollout
→ retained native component presets
→ root + datasets/RNG/viz + active tests
→ physical old-executor deletion
```

No intermediate checkpoint is represented as a completed stage. The old and
new runtimes may coexist only inside this unfinished transaction.

## Required Result

### Structural kernel

- Closed, versioned identities cover coordinates, occurrences, paths, spans,
  ports, interfaces, products, continuous regions, intensional references,
  and deterministic fresh references.
- Alphabet covers exact scalar and structural schemas, including represented
  numeric, tag, product, record, word, map, graph, field, instruction,
  pattern, equation, distribution, and symbolic forms.
- Semantic equality is structural and independent of Python identity, hash or
  mapping order, storage order, and rendering.

### Five local components

- Seed denotes exact, constructive, partial, law-valued, and intensional
  initial configurations without ambient entropy or dataset rendering.
- WritableRegion resolves the complete existing/fresh effect envelope and
  grants no read authority.
- ReadableRegion resolves identity-preserving old-snapshot views and grants no
  write authority.
- Rule is a closed, versioned denotation with finite/intensional support,
  cardinality, optional probability law, total dispositions, derivations and
  no-successor atoms, progress, continuation, witnesses, provenance, and typed
  faults.
- Component identity contains no callback, opaque executable, mutable recipe
  bag, semantic family/name dispatch, or hidden random state.

### One program and one application law

- `SimpleProgram` is frozen and stores exactly:
  `seed`, `alphabet`, `frontier`, `neighborhood`, and `rule`.
- Construction performs five-way compatibility validation without storing a
  sixth component or certificate.
- `apply` follows the fixed generic phase order and is family-blind.
- Every derivation reads one old snapshot, supplies one total disposition,
  binds fresh identities deterministically, reconstructs atomically, preserves
  everything outside the writable envelope, validates the successor, and is
  retained before semantic quotienting.
- Result spaces preserve no-successor outcomes, three independent
  cardinalities, derivation fibers, and exact probability submeasures.
- Seed binding/replay and lineage live in `program.py`; core never imports
  downstream `rng.py`.
- `rollout(program, *, steps, initial=None, replay_key=None)` traverses only by
  calling the owned `apply`.

### Migration

- Preserve only the six named Rule presets and six named Neighborhood presets
  listed by G7-01, now as closed module-qualified components with concrete
  `rule=` data.
- Replace dataset executor switches with four explicit ordinary-program recipe
  builders and downstream tensor projections.
- Visualization accepts only explicit `DatasetEpisode`/`DatasetBatch` views
  while retaining viewer-bundle wire version 1.
- Narrow root to the seven core namespaces plus `SimpleProgram`, `apply`, and
  callable `rollout`; catalog and serialization stay inert and unexposed until
  their stages.
- Delete `src/ca/specs.py`, `src/ca/rollout.py`, and `tests/test_specs.py`.
- Remove the old façades, family kernels, broad root constructors, unresolved
  rule-family queries, and public Seed rendering/deduplication helpers.
- Set version 0.2.0, use a general simple-program description, and move pytest
  into the development dependency group.

## No-Cheating Conditions

- No parallel, fallback, compatibility, catalog, tensor, or family-specific
  one-step executor survives.
- Generic application does not inspect SPF/F/T IDs, catalog metadata, family
  strings, constructor names, carrier labels, locus kinds, or Rule tags to
  select an algorithm.
- Commit does not select matches, schedules, winners, destinations, collision
  behavior, deletion cascades, topology repair, endpoint selection, solver
  execution, or random draws.
- A partial enumeration is never reported as a complete denotation.
- A draw is never confused with a probability law.
- A horizon or resource bound is never reported as semantic terminality.
- No G7-01-owned test remains skipped when the stage closes.

## Work Ledger

| Workstream | State | Evidence |
|---|---|---|
| Authority and live dependency audit | Complete | Starting tree `7226c49`; Goal 2/5/6 remained frozen |
| Loci and Alphabet kernel | Complete | Closed structural identities, carriers, exact schemas, and focused unit coverage |
| Seed, WritableRegion, ReadableRegion | Complete | Exact/constructive/partial/law/intensional sources and identity-preserving capability/view contracts |
| Rule denotation/result algebra | Complete | Closed ASTs, finite/intensional support, dispositions, laws, witnesses, faults, and native presets |
| Program, apply, Seed binding, rollout | Complete | Exact five-field value, one family-blind `apply`, replayable Seed realization, and apply-owned rollout |
| Native preset migration | Complete | Six Rule and six Neighborhood presets agree with independent complete-result fixtures |
| Root, datasets, RNG, visualization | Complete | Narrow lazy root; explicit downstream recipes, projections, RNG helpers, and viewer records |
| Active unit/conformance migration | Complete | `225 passed`; no G7-01-owned skip |
| Old-executor physical deletion | Complete | `specs.py`, `rollout.py`, and `test_specs.py` absent; module specs absent |
| Packaging/version cutover | Complete | Source/lock metadata at `0.2.0`; NumPy runtime and pytest development dependency |
| Final hostile review | Complete | Two independent static/dynamic reviews and adversarial edge regressions found no remaining G7-01 blocker |

## Completion Gates

At minimum:

```text
uv run pytest -q tests
uv lock --check
git diff --check
```

The closeout must additionally prove:

- CT01 and kernel CT02–CT08, CT12, and CT13 are active and green.
- Native fixtures match independent complete-result oracles.
- `ca.rollout` is callable and `import ca.rollout` fails.
- A fresh `import ca` does not load `ca.datasets`, `ca.rng`, or `ca.viz`.
- Static inspection finds one executable step law and no forbidden semantic
  callback, `Any`, mutable bag, family dispatch, or stale executor copy.
- The diff contains no unrelated Goal 2, Goal 5, Goal 6, or packaging-release
  work beyond the authorized G7-01 version/dependency change.

Only after every gate passes may this file, the stage index, and the top-level
Goal 7 status record G7-01 as complete.

## Stage Results

### Authoritative behavior

- `SimpleProgram` is a frozen value with exactly `seed`, `alphabet`,
  `frontier`, `neighborhood`, and `rule`.
- `program.apply` is the sole executable one-step law. It validates one old
  snapshot, resolves writable and readable bindings, validates complete Rule
  results, binds fresh identities, commits atomically, validates successors,
  preserves derivation fibers, and projects exact measures without family
  dispatch.
- `program.rollout` is the only rollout operation and calls the owned `apply`.
  Seed denotation, keyed realization, draw evidence, replay coordinates, and
  trace lineage remain in `program.py`; core does not import downstream RNG.
- Exact, constructive, partial, finite-law, and intensional Seed forms now
  retain their actual semantics. Partial sources remain non-enumerated until
  their unresolved roles and obligations are discharged. Large uniform laws
  use bounded direct rejection sampling rather than materializing their value
  domain.
- Finite application records reject contradictory source/applied mappings,
  partitions, cardinalities, fibers, identities, lineages, bindings, and
  measures. Intensional applied, no-successor, successor, and measure
  relations are separately filtered and bound to the application context.
- The six retained native Rule presets and six corresponding Neighborhood
  presets execute through that same generic law. Lag-count bands are exposed
  chronologically, with the Rule selecting history positions explicitly.
- Dataset construction, deterministic planning helpers, tensor projections,
  and visualization remain explicit downstream consumers. None is eagerly
  imported by `ca`.

### Files and migration

- Replaced the provisional kernels in `loci.py`, `alphabets.py`, `seeds.py`,
  `frontiers.py`, `neighborhoods.py`, `rules.py`, and `program.py`.
- Narrowed `ca.__all__` to `SimpleProgram`, `apply`, callable `rollout`, and
  the seven core namespaces.
- Migrated `datasets.py`, `rng.py`, and `viz/` to the new downstream boundary.
- Deleted `src/ca/specs.py`, `src/ca/rollout.py`, and `tests/test_specs.py`.
- Left serialization and catalog declarations inert and unexposed for their
  owning later stages.
- Updated package metadata and the lockfile to source version `0.2.0`. This
  internal checkpoint is not a release or publication.

### Verification

The completed tree passed:

```text
UV_CACHE_DIR=/tmp/ankos-uv-cache uv run --no-sync pytest -q tests -rs
→ 225 passed, 36 skipped

UV_CACHE_DIR=/tmp/ankos-uv-cache uv lock --check
→ Resolved 12 packages

git diff --check
→ pass

python -m compileall -q src/ca tests
→ pass
```

Focused public/import/descriptor and repaired edge suites passed 24 tests.
The final independent audits additionally established:

- zero G7-01-owned skips;
- exactly one `apply` definition and exactly one rollout call to it;
- no alternate step executor, old module, callback/`Any` core descriptor,
  mutable semantic field, or family/catalog/carrier/locus dispatch in
  `apply`;
- the seven-owner import DAG, narrow ten-name root, and lazy auxiliary
  boundary;
- callable `ca.rollout` with no `ca.rollout` or `ca.specs` module spec;
- exactly 28 tracked `src/ca` paths and physical absence of the retired
  executor files; and
- no changes under Goal 2, Goal 5, Goal 6, `api.md`,
  `simple_programs.md`, or the reference scaffold.

The 36 retained skips are explicitly later-stage work: serialization and
representation in G7-03; catalog assembly in G7-04; observer/family joins
across G7-02/G7-04/G7-05; and two named CT12 mechanics/catalog cases in
G7-02/G7-04.

### Changed assumptions and next action

The five-field architecture did not require revision. Hostile review did
invalidate several implementation assumptions: descriptor acceptance must
imply a valid Seed execution path; partial configuration metadata cannot be
dropped into a complete leaf; intensional projections must carry the complete
application context; and complete-result records need cross-space validation.
Those defects are now regression-tested.

G7-01 is closed. The first next action is to refresh current facts and create
`3-MECHANICS.md` for G7-02; no G7-02 implementation began in this stage.
