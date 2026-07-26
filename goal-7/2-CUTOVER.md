# Goal 7 Stage 2 — Atomic Five-Field Core Cutover

Status: **IN PROGRESS**

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
| Authority and live dependency audit | In progress | This record and source audit |
| Loci and Alphabet kernel | Pending | |
| Seed, WritableRegion, ReadableRegion | Pending | |
| Rule denotation/result algebra | Pending | |
| Program, apply, Seed binding, rollout | Pending | |
| Native preset migration | Pending | |
| Root, datasets, RNG, visualization | Pending | |
| Active unit/conformance migration | Pending | |
| Old-executor physical deletion | Pending | |
| Packaging/version cutover | Pending | |
| Final hostile review | Pending | |

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
