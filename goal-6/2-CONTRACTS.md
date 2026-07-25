# 2-CONTRACTS

Status: **COMPLETE**

## Current Facts

- Goal 5 already proves that all 60 executable families fit the five fields;
  F010 and F042 are close interface/observer roles rather than counterexamples.
- Stage 1 established `goal-6/architecture.md` as the canonical internal
  specification and froze the runtime, test, and Goal 2 baselines.
- The authoritative Goal 5 contract uses `Seed[C]`, `Alphabet[V]`,
  `WritableRegion[C, W]`, `ReadableRegion[C, R]`, and `Rule[R, W, C]`.
- The current `api.md` is a design-decision transcript,
  `simple_programs.md` is a useful but Z4/CA-specific specialization, and the
  old reference scaffold still uses `Dynamics`. Their clean public cutover
  belongs to Stage 4 after Stage 3 settles result/application semantics.
- No current runtime type implements the complete generalized contracts, and
  Goal 6 is not authorized to add one.

## Updated Assumptions

- One carrier-relative loci algebra can support both readable and writable
  region construction without merging their capabilities.
- Configuration can remain the shared type `C` produced by Seed and returned by
  Rule results; it does not require a sixth field or a public
  `configuration.py`.
- Frontier and Neighborhood should resolve independently from the same
  immutable `C`. They may reuse a closed anchor descriptor, while Rule checks
  the compatibility of their resolved `W` and `R`.
- Plural component modules can compose primitives into one singular value for
  each stored field; lists of neighborhoods, frontiers, or rules are not
  additional axes.
- Closed structural and intensional descriptors can cover infinite,
  continuous, stochastic, symbolic, graph, word, and tree semantics without
  callbacks or forced materialization.
- Sparse-versus-total replacement representation, result variants,
  witness/deduplication semantics, and exact commit mechanics must remain Stage
  3 work.

## Big Picture Objective

Specify the five component contracts and their shared structural/type algebra
before file layout, public examples, or application code hardens accidental
CA-only semantics.

## Detailed Implementation Plan

- Read the full Goal 5 family/API mapping and consolidate its 60-family
  pressures by reusable contract mechanics.
- Define `SimpleProgram[C, V, W, R]` with exactly five stored values.
- Define descriptor, denotation, resolution, and realization so closed
  structural semantics are not confused with runtime materializations.
- Specify configuration ownership and the contracts for Seed, Alphabet,
  WritableRegion, ReadableRegion, and Rule.
- Specify the shared carrier-relative locus/region algebra, including ordered,
  graph, tree, fresh, deleted, continuous, and intensional structure.
- Specify singular-component composition through the plural constructor
  modules.
- Define descriptor, program, configuration, and application validation layers
  and the required error categories.
- Define cross-cutting, versioned, exact, fail-closed serialization
  requirements.
- Type-check an ordinary CA, mobile automaton/Turing machine, structural
  rewrite, constraint completion, and continuous relation on paper.
- Keep `api.md`, `simple_programs.md`, and the reference scaffold unchanged
  until Stage 4 can replace them coherently after Stage 3.

Files changed:

- `goal-6/architecture.md`
- `goal-6/2-CONTRACTS.md`
- `goal-6/0-plan.md`

## No-Cheating Checks

- No Goal 4 artifact or Book source was opened or imported.
- The completed Goal 5 family mapping was reused; no second taxonomy or
  semantic-fingerprint matrix was created.
- Exactly five dataclass fields appear in the canonical signature. Type
  variables, associated contracts, validation evidence, codecs, aliases,
  provenance, and digests are explicitly non-fields.
- Configuration, Domain, Shape, Boundary, scheduler, RNG, solver, result,
  trajectory, time, and update policy did not reappear as stored program axes.
- Frontier remains the possible-write capability envelope, not firing loci or
  exact writes. Neighborhood remains independent read capability.
- Rule has no unrestricted access to `C`; every state dependency must be in
  `R`, while `W` grants no implicit read capability.
- Rule is not assumed to run once per cell or frontier member.
- Probability laws remain distinct from external realization keys and recorded
  draw evidence.
- No runtime or test file, frozen Goal 2 file, root API narrative, or reference
  scaffold was changed.
- Stage 2 states the minimum Rule result shape but does not preempt Stage 3's
  result and commit decisions.

## Completion Requirements

- [x] `SimpleProgram[C, V, W, R]` has exactly five stored fields and all type
      relationships are explicit.
- [x] Seed, Alphabet, WritableRegion, ReadableRegion, and Rule each have one
      clear denotation, ownership boundary, composition model, and validation
      contract.
- [x] Configuration support, topology, geometry, defaults, boundaries,
      invariants, control, program text, and identity have an explicit home
      without a sixth axis.
- [x] Loci cover coordinates, names, sequences, trees, graphs, products,
      continuous regions, histories, fresh identities, and intensional
      selectors while preserving order/multiplicity/interface information.
- [x] Dynamic support, creation, deletion, global reads, continuous carriers,
      probability laws, and symbolic/intensional objects have honest closed
      representations.
- [x] Cross-field validation rejects incompatible types, missing reads,
      unauthorized write schemas, invalid values/invariants, hidden entropy,
      and unsupported exactness.
- [x] Serialization is versioned, canonical, lossless, exact, fail-closed, and
      cross-cutting rather than a program field.
- [x] Ordinary CA, mobile, structural rewrite, constraint, and continuous
      examples type-check without a sixth field.
- [x] The next stage can define Rule results and generic application without
      reopening component ownership.

## Stage Results

### Canonical type relationship

```python
@dataclass(frozen=True)
class SimpleProgram(Generic[C, V, W, R]):
    seed: Seed[C]
    alphabet: Alphabet[V]
    frontier: WritableRegion[C, W]
    neighborhood: ReadableRegion[C, R]
    rule: Rule[R, W, C]
```

Both region descriptors resolve independently from the same immutable `C`.
They may share structural anchors, and Rule consumes the resulting `R` and `W`
without receiving an undeclared state-reading channel.

### Ownership decisions

| Concern | Owner |
|---|---|
| Initial exact/set/law/intensional configurations | Seed |
| Support, topology, geometry, defaults, boundaries, invariants, visible state | Configuration `C` produced by Seed |
| Closed semantic value schemas and equality | Alphabet |
| Structural identity and selection vocabulary | Loci algebra |
| Complete possible-write capability | Frontier |
| Complete state-read capability | Neighborhood |
| Applicability, schedule, selection, conflict, probability law, stopping, and replacement semantics | Rule |
| Canonical codec/version/migration mechanics | Cross-cutting serialization |
| Horizon, realization key/bound, solver strategy, trace, observer, renderer, export | Run/tooling request |

### Sixty-family pressure consolidation

The full `goal-5/api-pressure.md` mapping was checked rather than copied. Its
contract pressures collapse into these reusable groups:

| Pressure | Contract destination |
|---|---|
| Fixed, ordered, graph/tree, product, continuous, and intensional carriers | `C`, Alphabet, and loci |
| Exact, constructive, partial, stochastic, and intensional initial objects | Seed |
| Tagged/product/exact/symbolic/program/control values | Alphabet |
| Fixed, noncontiguous, dynamic-address, fresh/delete, whole-structure, and continuous write envelopes | Frontier |
| Local, span, path, history, global, metric, differential, and intensional reads | Neighborhood |
| Coupled, structural, relational, stochastic, continuous, mutable-program, and one-shot transformation | Rule |
| Type unification, invariant preservation, exactness, entropy, and capability inclusion | Cross-field validation |
| Versioning, exact values, structural identity, laws/draws, and representation relations | Serialization |

F010 remains a wrapper role unless given its own explicit state transition.
F042 remains an observer unless represented as a one-shot result-writing
transform. Neither requires another component.

### Design-input disposition

- Retained from `simple_programs.md`: writable Frontier, readable
  Neighborhood, immutable old-state reads, atomic result intent, ordered/masked
  selector construction, and algebraic clarity.
- Rejected from it as universal assumptions: top-level Domain/Shape/Boundary,
  Z4 and 0–3D limits, time-as-trajectory carrier, finite universes,
  coordinate-at-a-time scalar Rule, mandatory parallel per-locus evaluation,
  and one next tensor slice.
- Retained from `api.md`: the five fields, Seed-as-source, writable-envelope
  Frontier, arbitrary Neighborhood, Rule-owned update semantics, and
  zero/one/many relational pressure.
- Rejected/deferred from it: `UpdatePolicy`, per-frontier-member engine loops,
  collapsed empty-result meanings, and its unresolved sparse-versus-total
  replacement sketches.
- Retained from `ref/notes/ca-scaffold.py`: ownership-first documentation,
  frozen inspectable descriptors, normalization, composition, and the
  primitives-to-alias progression.
- Deferred to Stage 4: full rewrites of all three inputs, public exports,
  constructor spelling, and scaffold/file-layout presentation.

### Verification evidence

- All five required paper type-checks are recorded in
  `goal-6/architecture.md`.
- The canonical architecture distinguishes descriptor, denotation, resolution,
  and realization; singular program fields from plural constructor modules;
  and raw selectors from read/write capabilities.
- Stage 3 is the first incomplete stage. It owns the complete Rule result
  algebra, atomic application law, outcome/cardinality distinctions,
  witness/deduplication semantics, probability realization, and run/tool
  boundary.
