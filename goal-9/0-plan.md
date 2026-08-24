# Goal 9 — Primitive Kernel Refactor

Status: stages 1 through 5 complete; `6-CUTOVER` is in progress.

## Big Picture Objective

Replace the current type-heavy ANKoS runtime with a small, executable kernel
derived from the useful primitive split in `ref/notes/generator.md` and the
new API decisions:

```text
SPACE + ALPHABET + NEIGHBORHOOD + RULE -> SIMPLEPROGRAM
SEEDS -> SEED
SIMPLEPROGRAM + SEED -> TRAJECTORY
rollout(TRAJECTORY, limit/resources) -> EPISODE
```

The new kernel should use ordinary Python values wherever possible:

```text
SPACE          small frozen record: coordinates, extent law, boundary
ALPHABET       frozenset or simple membership function
NEIGHBORHOOD   tuple of offsets or small address function
RULE           ordinary callable with an identifying name/index
SEED           concrete shape/support and complete initial values
```

Only values that genuinely need to travel together should become small frozen
records. Inheritance hierarchies, generic proof machinery, semantic classes
for coordinate shapes, and family-specific runtime types are not part of the
target.

The goal ends when the core is ready for canonical presets to be implemented
one at a time. It does **not** implement any preset or claim that a canonical
family is complete.

## Target Runtime Meaning

- `SPACE` defines explicit time coordinates, non-temporal coordinate rules,
  the finite/infinite/support law, and boundary resolution.
- Concrete finite shape or realized support belongs to `SEED`.
- For relational shapes, Seed may carry the concrete relation data needed to
  realize its shape, while Space defines how those coordinates are interpreted.
- `ALPHABET` is the admitted set or membership rule for values.
- `NEIGHBORHOOD` selects prior addresses to read. It is not a write selector.
- `RULE` is one exact selected callable, not a rule-family object awaiting an
  index.
- `SIMPLEPROGRAM` contains exactly one definite Space, Alphabet, Neighborhood,
  and Rule. It does not contain a Seed.
- `TRAJECTORY` pairs one SimpleProgram with one compatible Seed.
- `EPISODE` contains the complete immutable states actually produced by
  rollout.
- Time is explicit. Constructing `t+1` never overwrites anything at `t`.
- There is no semantic `FRONTIER`. Dynamic activity is represented by
  Alphabet values such as active/inactive tags and interpreted by Rule.

## Non-Negotiable Constraints

1. **No presets in this goal.** Do not create ECA, Turing-machine, canonical
   family, or dataset preset implementations. Hand-constructed anonymous
   fixtures are allowed only to verify the kernel.
2. **No `Preset` class.** Plural sources are ordinary iterables, tuples, or
   generator functions.
3. **Coordinate-first selectors.** Replace `src/ca/loci.py` with
   `src/ca/selector.py`. This is a replacement, not a rename that carries the
   old hierarchy forward.
4. **No semantic locus hierarchy where an address works.** Coordinates are
   ordinary immutable values such as `(t, x)`, `(t, x, y)`, or `(t, vertex)`.
5. **No compatibility/proof bureaucracy.** Do not recreate contracts,
   capabilities, certificates, evidence trees, denotations, profiles, or a
   general constraint solver.
6. **No inheritance or generics initially.** Introduce neither unless a
   concrete implemented behavior cannot be expressed clearly without them;
   no preset work in this goal may be used to manufacture that need.
7. **No legacy fallback.** The new public execution path must not wrap or call
   the old `loci`, `frontiers`, Rule-expression, denotation, or application
   machinery.
8. **No `Configuration` terminology.** A complete value assignment at one
   explicit time is a `State`.
9. **No mutation semantics.** No replace/delete/preserve CRUD actions against
   an old State. A step constructs a complete new State at new time addresses.
10. **No fake catalog completion.** Canonical names may remain as honest
    progress stubs, but an unimplemented entry must fail explicitly and must
    not return a generic SimpleProgram.
11. **Behavioral verification only.** Tests must prove transition behavior,
    coordinate selection, boundary resolution, compatibility, or immutability.
    Tests that merely reward signatures, class inventories, stubs, or catalog
    surface area do not count.
12. **Do not preserve backwards compatibility by default.** Preserve it only
    if Stage 1 identifies a real in-scope consumer and the user explicitly
    chooses to keep it.

## Current Facts

These facts were observed when this scaffold was created:

- The repository currently has `goal-1` through `goal-8`; this is `goal-9`.
- The current `src/ca` implementation is approximately 31,600 lines before
  visualization assets.
- `src/ca/rules.py` is approximately 7,100 lines,
  `src/ca/program.py` approximately 3,800 lines, and `src/ca/loci.py`
  approximately 2,770 lines.
- `src/ca/frontiers.py` still exists even though Frontier is no longer part of
  the desired SimpleProgram.
- Current runtime modules contain many contracts, profiles, certificates,
  evidence structures, denotations, semantic value nodes, and selector/locus
  classes.
- The current test suite contains two files. One test joins all taxonomy rows
  to planned builder signatures; that rewards stub completeness rather than
  implemented behavior. The smoke test primarily exercises the old catalog,
  rollout result hierarchy, and serialization surface.
- `ref/types.csv` remains the book-ordered taxonomy and should remain the
  progress source of truth.
- `API/` contains desired-direction documents, but they are not automatically
  authoritative where they conflict with the decisions in this goal.
- The worktree was clean when this scaffold was created.
- Stage 1 found no in-repository production consumer or packaging entry point
  that requires backwards compatibility with the existing API.
- The four baseline tests pass but none asserts a successor State. Existing
  green status is therefore not evidence that the old dynamics are correct.
- The old core is mutually dependent through `loci` and `frontiers`; a clean
  coherent replacement is required rather than incremental compatibility
  wrappers.
- Relational Seed shape cannot be reconstructed from a bare State. The
  reference transition will therefore be `step(trajectory, state)`, allowing
  the Trajectory's Seed to provide realized bounds or adjacency while State
  remains a plain immutable explicit-time mapping.
- The new reference executor passes fourteen focused behavioral checks across
  Cartesian and relational spaces without importing any legacy execution
  machinery. Complete successor slices and explicit time are now implemented,
  not merely documented.
- Ordinary generator functions and explicit loops now demonstrably produce
  multiple definite values, SimplePrograms, and compatible Trajectories. No
  production plural-source abstraction or preset layer was necessary.

## Assumptions To Verify

- Breaking the current Python API is acceptable for this refactor. Stage 1
  found no in-repository consumer requiring compatibility; any external
  compatibility request must be separately evidenced and authorized.
- A plain immutable coordinate-to-value mapping is sufficient for the first
  reference executor. Dense arrays and graph-optimized storage can be added
  later without changing semantics.
- A boundary resolver on Space plus a coordinate selector is enough for the
  initial discrete kernel.
- Dynamic support, continuous time, distributions, structural rewrites, and
  differential systems should not be anticipated in the kernel before a
  later canonical preset demonstrates the exact missing operation.
- Serialization, visualization, PE dataset streaming, and optimized execution
  are downstream work unless the package cannot import cleanly without a
  minimal adjustment.

## Success Requirements

The goal is complete only when all of the following are true:

1. The public kernel exposes the agreed singular composition:

   ```text
   Space, SimpleProgram, Seed, Trajectory, Episode, step, rollout
   ```

   Alphabet, Neighborhood, and Rule may be ordinary values/callables rather
   than nominal classes.
2. `src/ca/selector.py` supplies coordinate- and relation-based selection with
   small functions or values.
3. `src/ca/loci.py` and `src/ca/frontiers.py` are absent from the completed
   implementation, and no compatibility shim silently routes through them.
4. A hand-constructed Cartesian local-update fixture proves offset selection,
   boundary reads, complete successor construction, and explicit immutable
   time.
5. A hand-constructed relational fixture using addresses `(t, v)` proves that
   adjacency selection does not require a graph/locus semantic class.
6. A Seed can supply two different concrete finite shapes to the same
   shape-polymorphic SimpleProgram when both are compatible.
7. Plural sources can be represented by plain iterables or generator
   functions and can yield definite singular values without a source-class
   hierarchy.
8. Canonical catalog entries that have not been rebuilt remain explicitly
   unimplemented; no stub is legitimized by a passing API-surface test.
9. Existing obsolete tests are removed or rewritten, and every remaining test
   protects meaningful behavior.
10. Package imports, focused tests, the full relevant test suite, and
    `git diff --check` pass.
11. A source scan confirms the public execution path does not import or invoke
    forbidden legacy machinery.
12. No canonical preset, family implementation, or dataset preset has been
    added. The final state is ready for that next goal rather than falsely
    claiming it has begun.

## Stages

### 1-CUTLINE

#### Big Picture Objective

Establish the exact replacement boundary before deleting or adapting code.
Identify what must survive for the minimal package to import and what is
merely legacy machinery.

#### Detailed Implementation Plan

- Inspect current public exports, internal imports, tests, examples, and any
  in-repository downstream consumers.
- Record a baseline of commands that currently pass or fail. Do not interpret
  old green tests as proof of correct semantics.
- Write the exact intended public call shape for hand-constructed values:

  ```text
  SimpleProgram(space, alphabet, neighborhood, rule)
  Trajectory(program, seed)
  rollout(trajectory, limit) -> Episode
  ```

- Classify current modules into replace, temporarily downstream and
  disconnected, delete because their semantics are rejected, or retain only
  as taxonomy/progress data.
- Identify actual compatibility obligations. Do not create adapters for
  hypothetical users.
- Update the plan with any discovered facts before Stage 2.

#### Completion Requirements

- The stage file records the current import graph, test baseline, public
  consumers, and exact cutover list.
- Every retained legacy module has a concrete reason tied to this goal.
- Any backwards-compatibility requirement is evidenced and explicitly
  approved; otherwise the plan continues as a clean break.
- No preset or replacement abstraction has been implemented yet.

### 2-VALUES

#### Big Picture Objective

Implement the smallest ordinary-value model capable of expressing one
definite SimpleProgram, Seed, Trajectory, and Episode without execution or
family semantics.

#### Detailed Implementation Plan

- Replace the composition model with small frozen records only where values
  genuinely need to travel together.
- Represent coordinates as ordinary immutable tuples rather than `Locus`
  objects.
- Represent a State as a complete immutable coordinate-to-value assignment at
  one explicit time.
- Keep Alphabet as a plain finite collection or membership callable.
- Keep Neighborhood and Rule as ordinary values/callables with optional plain
  identifying metadata only when needed for inspection.
- Define Seed as concrete initial support/shape and a complete initial State.
- Ensure concrete shape remains outside SimpleProgram.
- Add direct construction and equality tests only for semantically meaningful
  behavior; do not test dataclass implementation details.

#### Completion Requirements

- The target objects can be constructed without importing the old contracts,
  loci, frontier, rule-denotation, or application result hierarchies.
- No new inheritance hierarchy, Protocol lattice, generic parameter system,
  or semantic family class is introduced.
- Invalid values are rejected with direct, local checks only where execution
  would otherwise become ambiguous or wrong.
- Tests demonstrate that changing only Seed does not change SimpleProgram.

### 3-SELECTOR

#### Big Picture Objective

Replace the semantic locus/region subsystem with small coordinate selection
functions in `src/ca/selector.py`.

#### Detailed Implementation Plan

- Create `src/ca/selector.py` from scratch; do not mechanically transplant
  `loci.py`.
- Support the minimum selector forms required to verify the kernel:
  - fixed ordered relative offsets;
  - selection of the current address when needed;
  - adjacency lookup from plain relation data supplied with realized shape;
  - deterministic ordering when Rule distinguishes observed positions.
- Keep translation and address construction explicit about time. Spatial
  offsets read the selected source time unless a selector explicitly requests
  historical time.
- Keep boundary resolution in Space; Selector chooses addresses and does not
  invent values.
- Ensure `[t, x]`, `[t, x, y]`, and `[t, v]` are ordinary coordinates, not
  different locus subclasses.
- Add focused offset and adjacency tests using anonymous fixtures.
- Redirect the new kernel to `selector.py`; do not add a `loci.py` facade.

#### Completion Requirements

- The new kernel has no import from `ca.loci`.
- Cartesian and relational selectors both operate on ordinary coordinates.
- Graph adjacency works from a plain mapping or relation without `Graph`,
  `Vertex`, `Locus`, `Region`, or Carrier semantic classes.
- Selector contains no write permissions, Frontier, capability system, fresh
  namespace machinery, or configuration identity proofs.
- Tests cover selector ordering and preserve explicit source-time addresses.

### 4-EXECUTE

#### Big Picture Objective

Implement one transparent reference transition and rollout path that constructs
complete immutable successor States.

#### Detailed Implementation Plan

- Implement direct Space reads, including exact finite boundary behavior.
- Implement `step(trajectory, state)` as complete successor construction:
  - enumerate every required successor coordinate;
  - obtain prior addresses from Neighborhood;
  - read through Space boundary resolution;
  - invoke the exact Rule callable;
  - construct a fresh complete State at the next explicit time.
- Implement `Trajectory(program, seed)` compatibility checks using small direct
  conditions: coordinate form/rank, realized extent/support, and Alphabet
  membership.
- Implement `rollout(trajectory, limit)` returning an Episode of complete
  immutable States.
- Use anonymous hand-built rules rather than importing or creating presets.
- Add a Cartesian fixture and a relational `[t,v]` fixture.
- Confirm that values outside any logically active pattern still appear at
  new time coordinates; no `KEEP`, mutation, deletion, or preservation action
  should exist.

#### Completion Requirements

- The exact expected successor State is asserted for Cartesian and relational
  fixtures.
- Earlier States remain equal before and after later rollout steps.
- Every stored value has an explicit semantic time address.
- Two compatible Seed shapes run under the same SimpleProgram.
- Boundary behavior has at least one direct expected-value test.
- No execution path imports or calls Frontier, writable capabilities,
  dispositions, Rule denotations, or the old `apply`/rollout machinery.

### 5-SOURCES

#### Big Picture Objective

Prove that the kernel is ready for plural generators without introducing a
Preset abstraction or any family implementation.

#### Detailed Implementation Plan

- Permit `SPACES`, `ALPHABETS`, `NEIGHBORHOODS`, `RULES`, and `SEEDS` to be
  ordinary tuples, iterables, or generator functions.
- Demonstrate the intended dependency order with anonymous test data:

  ```text
  SPACE -> compatible NEIGHBORHOODS
  ALPHABET + NEIGHBORHOOD -> definite RULES
  SPACE + ALPHABET + NEIGHBORHOOD + RULE -> SIMPLEPROGRAMS
  SIMPLEPROGRAMS x compatible SEEDS -> TRAJECTORIES
  ```

- Prefer explicit nested loops in a fixture over a universal Cartesian-product
  or constraint engine.
- Keep Seeds independently generatable and filter compatibility only when a
  Trajectory is formed.
- Add no `presets/` family file and no canonical name.
- Document the few lines a future preset module will need, as pseudocode or
  documentation rather than a live preset.

#### Completion Requirements

- Plain generators yield more than one definite Space, Rule, and Seed in a
  test without generator classes.
- Every yielded SimpleProgram is singular and fully selected.
- The test includes incompatible generated values and demonstrates a direct,
  understandable compatibility decision rather than a capability framework.
- There is no `Preset`, `PresetSpec`, `Factory`, `BuilderContract`, or general
  parameter-resolution class.
- No canonical program behavior has been implemented.

### 6-CUTOVER

#### Big Picture Objective

Make the primitive kernel the actual `ca` package rather than an unused clean
layer beside the old runtime.

#### Detailed Implementation Plan

- Update `src/ca/__init__.py` to export only the intended primitive public API
  and explicitly retained downstream surfaces.
- Remove the rejected old implementation rather than retaining wrappers:
  - `loci.py` after `selector.py` has replaced its necessary behavior;
  - `frontiers.py`;
  - compatibility evidence/proof machinery;
  - semantic Rule-expression/denotation machinery;
  - obsolete application and rollout result hierarchies;
  - obsolete tests that reward these surfaces.
- Simplify the catalog/progress surface so unimplemented canonical entries are
  honest stubs tied to `ref/types.csv`. Stub existence must not be tested as
  implementation completeness.
- Disconnect or minimally adapt serialization, datasets, examples, and
  visualization only as necessary for a coherent package. Do not rebuild
  those subsystems inside this kernel goal.
- Update desired API documentation to describe what now exists, removing
  claims that preserve rejected concepts such as semantic Frontier or
  configuration mutation.
- Search for stale imports and terminology.

#### Completion Requirements

- `import ca` reaches the new kernel and does not transitively import rejected
  machinery.
- `src/ca/loci.py` and `src/ca/frontiers.py` no longer exist.
- No legacy shim or alternate public entry point can silently execute the old
  implementation.
- Canonical unimplemented entries fail explicitly and are not counted as
  implemented by tests or documentation.
- The retained source tree is materially smaller and every remaining core
  module participates in the target runtime or has an evidenced downstream
  reason to remain.
- Focused and full relevant tests pass after obsolete tests are removed or
  rewritten.

### 7-PRESET-READY

#### Big Picture Objective

Verify the real finish line: a small, understandable, preset-ready kernel with
no preset implementation smuggled into the refactor.

#### Detailed Implementation Plan

- Re-read the objective and audit the public source for reintroduced ceremony,
  semantic coordinate classes, legacy fallbacks, mutation actions, and hidden
  Frontier behavior.
- Run the Cartesian and relational behavioral fixtures from clean imports.
- Run the complete relevant test suite and diff/whitespace checks.
- Inspect the final public API from a fresh Python process.
- Verify that a future preset can be written as a small module of ordinary
  generator functions and explicit nested composition without modifying the
  kernel.
- Verify that no actual preset, ECA implementation, canonical family builder,
  or dataset suite was added.
- Record remaining downstream work honestly: presets, family-by-family
  behavior, serialization, optimization, visualization, and PE streaming are
  future goals rather than partial accomplishments here.

#### Completion Requirements

- Every Success Requirement above is checked against concrete files or test
  output.
- `uv run pytest -q` (or the repository's current equivalent) passes for the
  relevant retained suite.
- `git diff --check` passes.
- A source search confirms absence from the live kernel of `loci`, `frontier`,
  writable capabilities, dispositions, proof/evidence scaffolding, and a
  Preset class.
- The stage records exact commands and outcomes; no result is inferred from an
  earlier stage.
- The goal ends with a clear next action: implement the first preset in a new
  goal, beginning with the first book-ordered family.
